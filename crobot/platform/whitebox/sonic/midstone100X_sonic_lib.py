import re
import os
import sys
import datetime
import CRobot
import time
import Logger
import YamlParse
import bios_menu_lib
from Device import Device
workDir = CRobot.getWorkDir()
sys.path.append(os.path.join(workDir, 'common', 'onie'))
import OnieVariable
import whitebox_lib
import midstone100X_sonic_variable as Var
from crobot.Decorator import logThis

device_obj = Device.getDeviceObject(Var.deviceType)
pc_info = YamlParse.getDeviceInfo()["PC"]
pc_ip = pc_info["managementIP"]
pc_user = pc_info["scpUsername"]
pc_password = pc_info["scpPassword"]


@logThis
def execute_cmd(cmd, timeout=30, local=False):
    """
    Send command and get the response
    :param cmd: command
    :param timeout: get the response timeout
    :param local:True-send cmd on PC
    :param mode: mode. e.g:openbmc, centos
    """
    if local:
        response = Device.execute_local_cmd(device_obj, cmd, timeout)
        return response
    cmd = 'time ' + cmd
    device_obj.flush()
    result = device_obj.sendCmdRegexp(cmd, r"sys\s.*\dm.*\ds", timeout)
    res = re.findall(r".*%s(.*)\n+real.*" % cmd, result, re.S)
    for i in res:
        if i == "":
            res.remove(i)
    if res:
        res_list = res[0].split("\n")
        response = ""
        for line in res_list:
            response = response + "\n" + line
        return response.strip()
    else:
        return result


@logThis
def InitOSUser():
    """
    Switch account to root
    """
    return whitebox_lib.set_root_hostname(Var.deviceType)


@logThis
def ToTopOnieMenuItem(output):
    """
    Determine whether sonic is installed according to the string information, and finally enter the Onie system
    :param output:str
    """
    sonic_os = re.findall(r"SONiC-OS-", output)
    if sonic_os:
        Logger.info("%d Sonics have been installed." % len(sonic_os))
        bios_menu_lib.send_key(Var.deviceType, "KEY_DOWN", len(sonic_os))
        bios_menu_lib.send_key(Var.deviceType, "KEY_ENTER")
        device_obj.read_until_regexp("ONIE: Embed ONIE", 20)
        Logger.info("Has entered the onie secondary directory")


@logThis
def RebootToOnieMode(mode, return_info=False):
    """
    Send 'reboot' to ONIE OS
    :param mode: install, rescue, uninstall, update,
    :param return_info:if True, will return all information when onie starts
    """
    try:
        device_obj.sendline("sudo -s")
        device_obj.sendline("cd /")
    except Exception:
        pass
    device_obj.sendline("reboot")
    output = device_obj.read_until_regexp("will be executed automatically in", 360)
    ToTopOnieMenuItem(output)
    time.sleep(1)
    info = ""
    if mode == "install":
        bios_menu_lib.send_key(Var.deviceType, "KEY_ENTER")
        info = device_obj.read_until_regexp(OnieVariable.STARTING_DISCOVERY_PROMPT, 200)
    elif mode == "rescue":
        bios_menu_lib.send_key(Var.deviceType, "KEY_DOWN", 1)
        bios_menu_lib.send_key(Var.deviceType, "KEY_ENTER")
        info = device_obj.read_until_regexp(OnieVariable.ACTIVATE_CONSOLE_PROMPT, 200)
    elif mode == "update":
        bios_menu_lib.send_key(Var.deviceType, "KEY_DOWN", 3)
        bios_menu_lib.send_key(Var.deviceType, "KEY_ENTER")
        info = device_obj.read_until_regexp(OnieVariable.STARTING_DISCOVERY_PROMPT, 200)
    elif mode == "uninstall":
        bios_menu_lib.send_key(Var.deviceType, "KEY_DOWN", 2)
        bios_menu_lib.send_key(Var.deviceType, "KEY_ENTER")
        device_obj.read_until_regexp("ONIE: OS Uninstall Mode ...", 200)
        info = device_obj.read_until_regexp("The system is going down NOW!", 1200)
        device_obj.read_until_regexp("ONIE: OS Install Mode ...", 300)
        device_obj.sendline('\n')
        device_obj.sendline("onie-discovery-stop")
    device_obj.sendline('\n')
    device_obj.sendline("onie-discovery-stop")
    if return_info:
        return info


@logThis
def InstallDiagOS(protocol, version, timeout=600):
    """
    Copy the sonic installation file to the root directory of the corresponding folder for http/tftp installation,
    and finally delete it from the root directory
    :param protocol:http/tftp
    :param version: old/new
    :param timeout:out of time
    """
    # onie-nos-install tftp://10.10.10.138/onie-installer.bin
    destination_path = Var.tftp_file_path if protocol.lower() == "tftp" else Var.http_file_path
    if not destination_path.endswith("/"):
        destination_path = destination_path + "/"
    try:
        file_path = whitebox_lib.get_tool_path() + "/sonic/sonic_bin/%s" % version
        file_name = Device.execute_local_cmd(device_obj, "ls %s" % file_path).strip()

        Device.execute_local_cmd(device_obj, "cp %s/%s %sonie-installer.bin" % (file_path, file_name, destination_path))
        cmd = "onie-nos-install %s://%s/onie-installer.bin" % (protocol.lower(), Var.auto_server_ip)
        device_obj.sendline(cmd)
        device_obj.read_until_regexp(Var.diagos_install_msg, timeout=timeout)
        device_obj.read_until_regexp(Var.diagos_install_pass, timeout=int(timeout)-300)
        whitebox_lib.connect(Var.deviceType, 60, 120)
    finally:
        Device.execute_local_cmd(device_obj, "rm -rf %sonie-installer.bin" % destination_path)


@logThis
def InstallSonicWithOnie(version):
    execute_cmd("mkdir -p /home/test_for_sonic")
    RebootToOnieMode("install")
    InstallDiagOS("http", version)
    CheckCMDResponse("ls /home", "test_for_sonic", False)


@logThis
def GetSonicVersion():
    """
    Get Sonic Version
    :return: sonic version or sonic version list
    """
    cmd = r"sonic_installer list"
    res = execute_cmd(cmd)
    version = re.findall(r"Available:(.*)", res, re.S)
    if version:
        version = version[0].strip()
        if "\r\n" in version:
            version = version.split("\r\n")
        Logger.info("Get Sonic Version: %s" % str(version))
        return version[0] if len(version) == 1 else version
    else:
        Logger.error("Couldn't find it")


@logThis
def InstallSonicInSonic(version, enter_sonic=None):
    """
    If Sonic is already installed, install another Sonic in Sonic
    :param version:old/new
    :param enter_sonic: none: do nothing
                        1: Restart into the newly installed sonic
                        2: Restart and enter the previously installed sonic
    """
    file_path = whitebox_lib.get_tool_path() + "/sonic/sonic_bin/%s" % version
    file_name = execute_cmd("ls %s" % file_path, local=True)
    file_name = file_name.strip()
    execute_cmd("mkdir -p /home/whitebox")
    whitebox_lib.copy_files_from_pc_to_os(Var.deviceType, pc_user, pc_password, pc_ip, file_name, file_path,
                                          "/home/whitebox", 100)
    cmd = "echo Y | sonic_installer install /home/whitebox/%s" % file_name
    success_keyword = r"Done"
    CheckCMDResponse(cmd, success_keyword, True, True)
    if enter_sonic:
        device_obj.sendline("reboot")
        res = device_obj.read_until_regexp("will be executed automatically in", 360)
        sonic_info = re.findall(r"SONiC-OS-", res)
        if str(enter_sonic) == "2":
            Logger.info("Will Enter The Second Sonic: %s" % sonic_info[1])
            bios_menu_lib.send_key(Var.deviceType, "KEY_DOWN")
            bios_menu_lib.send_key(Var.deviceType, "KEY_ENTER")
        else:
            Logger.info("Will Enter The First Sonic: %s" % sonic_info[0])
        whitebox_lib.connect(Var.deviceType, 60, 120)


@logThis
def UninstallSonicInSonic(num_sonic):
    """
    If there are two sonics, uninstall one sonic from the other sonic
    :param num_sonic:The serial number of the sonic to be uninstalled in the selection interface
    """
    sonic_version = GetSonicVersion()
    if isinstance(sonic_version, list):
        cmd = r"echo y | sonic_installer remove %s" % sonic_version[int(num_sonic)-1]
    else:
        cmd = r"echo y | sonic_installer remove %s" % sonic_version
    CheckCMDResponse(cmd, "Image removed")


@logThis
def RebootOS(wait_time=10, timeout=600):
    """
    Reboot OS and connect
    :param wait_time: Wait for a while before reboot os
    :param timeout:reboot os time out
    """
    device_obj.sendline("reboot")
    whitebox_lib.connect(Var.deviceType, wait_time, timeout)


@logThis
def SetPowerStatus(status, ip=None, connect=False):
    return whitebox_lib.set_power_status(Var.deviceType, status, ip, connect)


@logThis
def SetPduStatus(status, port):
    """
    Control the operation of PDU to power on, power off, and restart the device
    :param status: [on,off,reboot]
    :param port: The port number on the PDU of the device under test
    """
    return whitebox_lib.set_pdu_status(Var.deviceType, status, port)


@logThis
def SetPduStatusConnectOS(status, port, timeout, wait_time=None):
    """
    Connect os after pdu send command
    """
    return whitebox_lib.set_pdu_status_connect_os(Var.deviceType, status, port, timeout, wait_time)


@logThis
def CheckInfoEqual(info_1, info_2, decide=True):
    """
    Check whether the two messages (both will be converted to strings) are equal
    """
    return whitebox_lib.check_info_equal(info_1, info_2, decide)


@logThis
def GetBMCIp(eth_type='dedicated', ipv6=False):
    """
    Use IPMI command to get BMC IP address
    :param eth_type: Network port type: dedicated, shared
    :param ipv6: Whether to get IPV6, if False, get IPV4
    :return: IP address
    """
    return whitebox_lib.get_ip_address_from_ipmitool(Var.deviceType, eth_type, ipv6)


@logThis
def SetSelClear(bmc_ip=None):
    return whitebox_lib.set_sel_clear(Var.deviceType, bmc_ip)


@logThis
def CheckCMDResponse(cmd, keyword, decide=True, re_s=False, pc=False, case_insensitive=False):
    """
    Send command and check keyword in response
    :param cmd: command
    :param keyword: keyword
    :param decide: True/False
    :param re_s: re.S or not
    :param pc: pc or dut
    :param case_insensitive:case insensitive or not
    """
    res = Device.execute_local_cmd(device_obj, cmd) if pc else execute_cmd(cmd, timeout=300)
    if case_insensitive:
        res = res.lower()
        keyword = [x.lower() for x in keyword]
    response = re.findall(r"%s" % keyword, res, re.S) if re_s else re.findall(r"%s" % keyword, res)
    if decide:
        if not response:
            whitebox_lib.PRINTE("Fail! Couldn't find keyword:[%s] in command[%s] response. response:\n%s"
                                % (keyword, cmd, res))
    else:
        if response:
            whitebox_lib.PRINTE("Fail! Find keyword:[%s] in command[%s] response. response:\n%s"
                                % (keyword, cmd, res))
    # for word in keyword:
    #     response = re.findall(r"%s" % word, res, re.S) if re_s else re.findall(r"%s" % word, res)
    #     if decide:
    #         if not response:
    #             whitebox_lib.PRINTE("Fail! Couldn't find keyword:[%s] in command[%s] response. response:\n%s"
    #                                 % (keyword, cmd, res))
    #     else:
    #         if response:
    #             whitebox_lib.PRINTE("Fail! Find keyword:[%s] in command[%s] response. response:\n%s"
    #                                 % (keyword, cmd, res))


@logThis
def SetWait(wait_time):
    return whitebox_lib.set_wait(wait_time)


@logThis
def KillProcess(process_name):
    """
    Kill process by pid
    :param process_name: process name
    """
    cmd = r"ps | grep %s" % process_name
    for i in range(1, 4):
        process_info = execute_cmd(cmd, 10)
        if process_info:
            process_list = process_info.splitlines()
            for process in process_list:
                pid = process.split(" ")[0]
                device_obj.sendline("kill %s" % pid)
                time.sleep(3)
                Logger.info("Done! Has killed %s, PID[%s]" % (process_name, pid))
            return
        else:
            time.sleep(2)
    else:
        Logger.info("Couldn't find process:%s" % process_name)


@logThis
def SendCmdWithoutRule(cmd, check_res=False, keyword=None, timeout=None):
    """
    Send cmd but don't Follow any return rules
    :param cmd:command
    :param check_res:True-got response and check it
    :param keyword:response keyword
    :param timeout:Check the timeout of keywords in the return
    """
    return whitebox_lib.send_cmd_without_return_rule(Var.deviceType, cmd, check_res, keyword, timeout)


@logThis
def CheckBSPSysfsInterfaces():
    """
    For midstone100X case: 9.1 BSP sysfs interfaces check
    Check whether the corresponding file path exists
    :return:
    """
    a = """
    /sys/bus
    /sys/bus/i2c
    /sys/bus/i2c/devices
    /sys/bus/i2c/devices/11-0070
    /sys/bus/i2c/devices/11-0071
    /sys/bus/i2c/devices/11-0072
    /sys/bus/i2c/devices/11-0073
    /sys/bus/i2c/devices/12-0070
    /sys/bus/i2c/devices/12-0071
    /sys/bus/i2c/devices/12-0072
    /sys/bus/i2c/devices/12-0073
    /sys/bus/i2c/devices/10-0030
    /sys/bus/i2c/devices/10-0031
    /sys/bus/i2c/devices/10-0032
    /sys/bus/i2c/devices/10-0033
    /sys/bus/i2c/devices/0-0056
    /sys/bus/i2c/devices/0-0056/eeprom
    """
    all_path = [x for x in a.split("\n") if x != ""]
    for i in range(0, 4):
        all_path.append("/sys/bus/i2c/devices/10-003%d" % i)
        for _ in ["scratch", "getreg", "setreg", "port_led_color", "port_led_mode"]:
            all_path.append("/sys/bus/i2c/devices/10-003%d/%s" % (i, _))

    all_path.append("/sys/class")
    all_path.append("/sys/class/SFF")
    for ii in range(1, 65):
        all_path.append("/sys/class/SFF/QSFP%d" % ii)
        for _ in ["qsfp_lpmode", "qsfp_modirq", "qsfp_modprs", "qsfp_modintl", "qsfp_reset"]:
            all_path.append("/sys/class/SFF/QSFP%d/%s" % (ii, _))
    d = """
    /sys/bus/platform
    /sys/bus/platform/devices
    /sys/bus/platform/devices/fpga-board
    /sys/bus/platform/devices/fpga-board/FPGA
    /sys/bus/platform/devices/fpga-board/FPGA/fpga_version
    /sys/bus/platform/devices/fpga-board/FPGA/scratch
    /sys/bus/platform/devices/fpga-board/FPGA/getreg
    /sys/bus/platform/devices/fpga-board/FPGA/setreg
    /sys/bus/platform/devices/cls-xcvr
    /sys/bus/platform/devices/cls-xcvr/SFP1
    /sys/bus/platform/devices/cls-xcvr/SFP1/sfp_rxlos
    /sys/bus/platform/devices/cls-xcvr/SFP1/sfp_txdisable
    /sys/bus/platform/devices/cls-xcvr/SFP1/sfp_absmod
    /sys/bus/platform/devices/cls-xcvr/SFP1/sfp_txfault
    /sys/bus/platform/devices/cls-xcvr/SFP2
    /sys/bus/platform/devices/cls-xcvr/SFP2/sfp_rxlos
    /sys/bus/platform/devices/cls-xcvr/SFP2/sfp_txdisable
    /sys/bus/platform/devices/cls-xcvr/SFP2/sfp_absmod
    /sys/bus/platform/devices/cls-xcvr/SFP2/sfp_txfault
    /sys/bus/platform/devices/sys-cpld
    /sys/bus/platform/devices/sys-cpld/scratch
    /sys/bus/platform/devices/sys-cpld/getreg
    /sys/bus/platform/devices/sys-cpld/setreg
    /sys/bus/platform/devices/sys-cpld/sys_led
    /sys/bus/platform/devices/sys-cpld/sys_led_color
    """
    d = [x for x in d.split("\n") if x != ""]
    all_path = all_path + d
    error_list = list()
    for file_path in all_path:
        file_path = file_path.strip()
        path_1 = file_path.split("/")[-1]
        path_2 = "/".join(file_path.split("/")[:-1])
        res = execute_cmd("ls %s" % path_2)
        if path_1 not in res:
            error_list.append(file_path)
    if error_list:
        whitebox_lib.PRINTE("Fail! The path that does not exist:\n%s" % error_list)


@logThis
def CheckNoErrorWhenOSStart(error_list=Var.keyword_can_ignore_when_sonic_start_list):
    """
    Check that the information printed when sonic is started cannot contain information that contains the keywords
    of 'error', 'failed', and 'failed' except for ignorable information.
    :param error_list: Ignore error messages
    """
    device_obj.sendline("reboot")
    error_info_list = list()
    all_info = device_obj.read_until_regexp("login:", timeout=360)
    if all_info:
        for info in all_info.split("\n"):
            error_line_list = re.findall(r"(error|fail|failed)", info, re.I)
            if error_line_list:
                for ignore_error_line in error_list:
                    if not re.findall(ignore_error_line, info, re.I):
                        error_info_list.append(info.strip())
        if error_info_list:
            whitebox_lib.PRINTE("Fail! The following error messages are obtained, and they are not included "
                                "in the ignorable error messages:\n%s" % str(error_info_list))
    else:
        whitebox_lib.PRINTE("Fail! Couldn't get the status information at startup")


@logThis
def CheckShowVersionInfo(platform=Var.expected_platform, baud_rate=Var.expected_baud_rate,
                         error_keywords=Var.keyword_error_in_show_version):
    """
    Send cmd 'show version' and check Is the sonic platform information correct or not
    :param platform:expected platform
    :param baud_rate:expected baud_rate
    :param error_keywords:the keyword can not in show version response
    """
    error_flag = False
    res = execute_cmd("show version")
    software_info = re.findall(r"SONiC Software Version: SONiC\.(.*)", res)
    if not software_info:
        whitebox_lib.PRINTE("Fail! Couldn't get sonic version information. Response:\n%s" % res)
    if not baud_rate.endswith(".0"):
        baud_rate = baud_rate + ".0"
    if platform not in software_info[0] or baud_rate not in software_info[0]:
        error_flag = True
    docker_info = re.findall(r".*SIZE(.*)", res, re.S)[0]
    c = list()
    a = docker_info.strip().split("\n")
    for i in a:
        b = i.strip().split(" ")
        x = [xx for xx in b if xx != ""]
        c.append(x[1])
    if len(list(set([j for j in c if j != "latest"]))) != 1:
        error_flag = True
    for keyword in error_keywords:
        if keyword in res:
            error_flag = True
    if error_flag:
        whitebox_lib.PRINTE("Fail! cmd[show version].Response:\n%s" % res)


@logThis
def CheckCpuInfo(info_list=Var.cpu_info_list, memtotal=Var.memtotal_G):
    """
    Send 'cat /proc/cpuinfo', check the value of 'cpu MHz', 'cache size', 'cpu cores' and the number of thread
    :param info_list: list[dict]. eg:[{'cpu_MHz': [800, 900]}, {"cache_size": 3072}]
    :param memtotal：total memory. unit-G
    """
    cmd = r"cat /proc/cpuinfo"
    res = execute_cmd(cmd)
    model_name_list = re.findall(r"model name\s+: (.*)", res)
    if len(list(set(model_name_list))) > 1:
        whitebox_lib.PRINTE("Fail! CPU types are not the same")
    model_name = list(set(model_name_list))[0].strip()
    if model_name != info_list[4]["model_name"]:
        whitebox_lib.PRINTE("Fail! The CPU model name expected:[%s], Actually:[%s]"
                            % (info_list[4]["model_name"], model_name))
    cpu_mhz_list = re.findall(r"cpu MHz\s+:\s+(.*)\r", res)
    cache_size_list = re.findall(r"cache size\s+:\s+(.*)\sKB", res)
    cpu_cores_list = re.findall(r"cpu cores\s+:\s(.*)\r", res)
    thread_num_list = re.findall(r"processor\s+:\s(\d+)", res)
    Logger.info(str(cpu_mhz_list))
    Logger.info(str(cache_size_list))
    Logger.info(str(cpu_cores_list))
    Logger.info(str(thread_num_list))
    for i in cpu_mhz_list:
        i = float(i)
        if float(info_list[0]["cpu_MHz"][0]) <= float(i) <= float(info_list[0]["cpu_MHz"][1]):
            pass
        else:
            whitebox_lib.PRINTE("Fail! Expected cpu MHz range:%s, actual value is:%s.Response:\n%s" %
                                (info_list[0]["cpu_MHz"], cpu_mhz_list, res))
    cache_size_list_set = list(set(cache_size_list))
    if len(cache_size_list_set) > 1:
        whitebox_lib.PRINTE("Fail! CPU 'cache size' are not the same")
    CheckInfoEqual(info_list[1]["cache_size"], cache_size_list_set[0])

    cpu_cores_list_set = list(set(cpu_cores_list))
    if len(cpu_cores_list_set) > 1:
        whitebox_lib.PRINTE("Fail! CPU 'cpu cores' are not the same")
    CheckInfoEqual(info_list[2]["cpu_cores"], cpu_cores_list_set[0])
    thread_num = int(thread_num_list[-1]) + 1
    CheckInfoEqual(info_list[3]["thread_number"], thread_num)

    cmd = r"cat /proc/meminfo"
    res = execute_cmd(cmd)
    memory_size_kb = re.findall(r"MemTotal:\s+(\d+)\s+kB", res)[0]
    memory_size_g = int(memory_size_kb)/1024/1024
    if int(memtotal)-1 <= memory_size_g <= int(memtotal)+1:
        memfree = re.findall(r"MemFree:\s+(\d+)\s+kB", res)[0]
        if int(memfree) >= memory_size_kb:
            whitebox_lib.PRINTE("Fail! The remaining memory capacity: [%s] the total memory capacity:[%s].Response:\n%s"
                                % (memfree, memory_size_kb, res))
    else:
        whitebox_lib.PRINTE("Fail! Expected memory size:[%s, %s], actual:[%s].Response:\n%s" %
                            (int(memtotal)-1, int(memtotal)+1, memory_size_g, res))


@logThis
def CheckTLVEepromInfo(info_list=Var.tlv_info):
    """
    Check TLV information
    :param info_list: dict. e.g.{Product Name': 'Midstone100X'}
    """
    # TODO 后续删除下列注释内容
    #79.Midstone100X写TLV之前要先disable CPLD写保护：
    # echo 0xA131 > /sys/bus/platform/devices/sys_cpld/getreg
    # cat /sys/bus/platform/devices/sys_cpld/getreg
    # echo "0xA131 0x03" > /sys/bus/platform/devices/sys_cpld/setreg
    # cat /sys/bus/platform/devices/sys_cpld/getreg

    # cmd_disable_write_protection_1 = r"echo 0xA131 > /sys/bus/platform/devices/sys_cpld/getreg"
    # cmd_disable_write_protection_2 = r'echo "0xA131 0x03" > /sys/bus/platform/devices/sys_cpld/setreg'
    # device_obj.sendline(cmd_disable_write_protection_1)
    # SetWait(10)
    # device_obj.sendline(cmd_disable_write_protection_2)
    # SetWait(10)

    cmd_1 = r"decode-syseeprom"
    cmd_2 = r"show platform syseeprom"
    res_1 = execute_cmd(cmd_1)
    res_2 = execute_cmd(cmd_2)
    res_1_1, res_1_2 = res_1.split("--------------------")
    res_2_1, res_2_2 = res_2.split("--------------------")
    CheckInfoEqual(res_1_1, res_2_1)
    res_1_dict = dict()
    res_2_dict = dict()
    for line_1 in res_1_2.splitlines():
        a = re.findall(r"(.*)\s+(0x\w+)\s+\d+(.*)", line_1)
        if a:
            res_1_dict[a[0][0].strip()] = (a[0][0].strip(), a[0][2].strip())
    for line_2 in res_2_2.splitlines():
        b = re.findall(r"(.*)\s+(0x\w+)\s+\d+(.*)", line_2)
        if b:
            res_2_dict[b[0][0].strip()] = (b[0][0].strip(), b[0][2].strip())
    res_1_sorted = str(sorted(res_1_dict.items(), key=lambda key: key[0]))
    res_2_sorted = str(sorted(res_2_dict.items(), key=lambda key: key[0]))
    if res_1_sorted != res_2_sorted:
        whitebox_lib.PRINTE("cmd1:%s, cmd2:%s response don't equal. response-1:\n%s\nresponse-2:\n%s\n"
                            % (cmd_1, cmd_2, res_1, res_2))
    all_i2c_info = ParsingEepromInfo("/sys/bus/i2c/devices/0-0056")
    for key, value in info_list.items():
        info = re.findall("%s\s+\w+\s+\w+\s+(.*)" % key, res_1)[0]
        if info != value:
            whitebox_lib.PRINTE("Fail! Expected [%s] is size:[%s], actual:[%s].Response:\n%s" % (key, value, info, res_1))
        if value not in all_i2c_info:
            whitebox_lib.PRINTE("Fail! keyword:[%s] not in 'hexdump -C eeprom' response.Response:\n%s"
                                % (value, all_i2c_info))


@logThis
def ParsingEepromInfo(i2c_path):
    """
    Enter the I2C path, send'hexdump -C eeprom', and parse the information in the rightmost column
    :param i2c_path:I2C path
    :return:str. Information string in the rightmost column
    """
    device_obj.sendline("cd %s" % i2c_path)
    res = execute_cmd("hexdump -C eeprom")
    info_str = r""
    for info in res.splitlines():
        if "|" in info:
            eeprom_info = re.findall(r"\|(.*)\|", info)[0]
            info_str = info_str + eeprom_info.strip()
    return info_str


@logThis
def SendCmdInBMC(cmd, switch_cpu=False):
    start_time = time.time()
    while time.time() - start_time < 300:
        try:
            device_obj.switchToBmc()
            Logger.info("Has switch to bmc!, pls wait 40s before bmc ready!")
            SetWait(40)
            break
        except Exception:
            SetWait(10)
    else:
        whitebox_lib.PRINTE("Fail! Couldn't switch to BMC")
    res = execute_cmd(cmd)
    if switch_cpu:
        start_time = time.time()
        while time.time() - start_time < 300:
            try:
                device_obj.trySwitchToCpu()
                Logger.info("Has switch to CPU!")
                break
            except Exception:
                SetWait(10)
    return res


@logThis
def CheckLoopBackPresent(present_num=Var.expected_present_num):
    """
    Send 'sfputil show presence' to check the number of loopback 'present'
    :param present_num:expected number of 'present' e.g 64
    """
    cmd = r"sfputil show presence"
    res = execute_cmd(cmd)
    present = res.count("present")
    not_present = res.count("Not present")
    if present != int(present_num):
        whitebox_lib.PRINTE("The expected number of 'present' is:[%s], Actual is:[%s]" % (present, not_present))


@logThis
def RunLoopbackModulePresentStress(timeout=24):
    """
    For SONIC function case: 9.23 Loopback_module_present_stress
    :param timeout: out of time  unit-h
    """
    wait_time = timeout*3600
    file_path = whitebox_lib.get_tool_path() + "/sonic/shell"
    file_name_1 = r"Port_device_present_stress.sh"
    file_name_2 = r"run.sh"
    device_obj.sendline("cd /")
    whitebox_lib.copy_files_from_pc_to_os(Var.deviceType, pc_user, pc_password, pc_ip, file_name_1, file_path,
                                          "/", 100)
    whitebox_lib.copy_files_from_pc_to_os(Var.deviceType, pc_user, pc_password, pc_ip, file_name_2, file_path,
                                          "/", 100)
    whitebox_lib.chmod_file(Var.deviceType, "/%s" % file_name_1)
    whitebox_lib.chmod_file(Var.deviceType, "/%s" % file_name_2)
    device_obj.sendline("./%s" % file_name_2)
    SetWait(wait_time/2)
    start_time = time.time()
    while time.time() - start_time < wait_time/2:
        try:
            res = execute_cmd("cat count.txt")
            if res.count("10000End") == 10:
                break
        except Exception:
            time.sleep(60*60)
    res_ = execute_cmd("ls /testlog")
    if "failedresult.txt" in res_:
        whitebox_lib.PRINTE("Fail! There is a fail test log, and its path is:'/testlog/failedresult.txt'")
