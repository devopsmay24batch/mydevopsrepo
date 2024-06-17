import re
import datetime
import CRobot
import time
import Logger as log
import whitebox_lib
import YamlParse
import bios_menu_lib
from SIT_variable import *
from Device import Device
import os
import Const
import CommonLib
import Logger

from crobot import Session

device_obj = Device.getDeviceObject(deviceType)
pc_info = YamlParse.getDeviceInfo()["PC"]
pc_ip = pc_info["managementIP"]
pc_user = pc_info["scpUsername"]
pc_password = pc_info["scpPassword"]
response_end_flag = r"sys\s.*\dm.*\ds"
KEY_DATA = {
    'KEY_DEL': '\x1b[3~',
    'KEY_F1': '\x1bOP',
    'KEY_F2': '\x1bOQ',
    'KEY_F3': '\x1bOR',
    'KEY_F4': '\x1bOS',
    'KEY_F7': '\x1b[18~',
    'KEY_F10': '\x1b[21~',
    'KEY_ESC': '\x1b',
    'KEY_ESC': '\x1b',
    'KEY_ENTER': '\r',
    'KEY_PLUS': '+',
    'KEY_MINUS': '-',
    'KEY_UP': '\x1b[A',
    'KEY_DOWN': '\x1b[B',
    'KEY_RIGHT': '\x1b[C',
    'KEY_LEFT': '\x1b[D',
    'KEY_1': '1',
    'KEY_2': '2',
    'KEY_3': '3',
    'KEY_4': '4',
    'KEY_5': '5',
    'KEY_6': '6',
    'KEY_7': '7',
    'KEY_8': '8',
    'KEY_9': '9',
    'KEY_0': '0'
}
"""
Most of the default parameters of the function come from SIT_variable.py
"""


def execute_cmd(cmd, timeout=300, local=False):
    """
    Send command and get the response
    :param cmd: command
    :param timeout: get the response timeout
    :param local:True-send cmd on PC
    """
    if local:
        response = Device.execute_local_cmd(device_obj, cmd, timeout)
        return response
    cmd = 'time ' + cmd
    device_obj.flush()
    result = device_obj.sendCmdRegexp(cmd, response_end_flag, timeout)
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
        return ""


def InitOSUser():
    """
    Switch account to root
    """
    return whitebox_lib.set_root_hostname(deviceType)


def RebootOS(wait_time=10, timeout=600):
    """
    Reboot OS and connect
    :param wait_time: Wait for a while before reboot os
    :param timeout:reboot os time out
    """
    device_obj.sendline("reboot")
    connect(wait_time, timeout)


def SetPowerStatus(status, ip=None, connection=False):
    """
    OS
    On the PC, send 'ipmitest chassis power' to bmc (bmc is not powered off) to power on and off the system
    :param status:on/off/reset/cycle
    :param ip: BMC IP of the tested product
    :param connection:Whether to connect DUT
    """
    status = status.lower()
    if ip:
        cmd = "ipmitool -I lanplus -H %s -U admin -P admin chassis power %s" % (ip, status)
        Device.execute_local_cmd(device_obj, cmd)
    else:
        cmd = "ipmitool chassis power %s" % status
        device_obj.sendline(cmd)
    if connection:
        connect()


def SetPduStatus(status, port):
    """
    Control the operation of PDU to power on, power off, and restart the device
    :param status: [on,off,reboot]
    :param port: The port number on the PDU of the device under test
    """
    return whitebox_lib.set_pdu_status(deviceType, status, port)


def SetPduStatusConnectOS(status, port, timeout, wait_time=None):
    """
    Connect os after pdu send command
    """
    return whitebox_lib.set_pdu_status_connect_os(deviceType, status, port, timeout, wait_time)


def CheckInfoEqual(info_1, info_2, decide=True):
    """
    Check whether the two messages (both will be converted to strings) are equal
    """
    return whitebox_lib.check_info_equal(info_1, info_2, decide)


def CheckCPUModeName(exp_mode_name=cpu_model_name):
    """
    Send 'cat /proc/cpuinfo' and check Is the 'model name' value in the response the same as expected
    :param exp_mode_name:Expected 'model name' value
    """
    cmd = r"cat /proc/cpuinfo"
    res = execute_cmd(cmd)
    model_name_list = re.findall(r"model name\s+: (.*)", res)
    if len(list(set(model_name_list))) > 1:
        whitebox_lib.PRINTE("Fail! CPU types are not the same")
    model_name = list(set(model_name_list))[0].strip()
    if model_name != exp_mode_name:
        whitebox_lib.PRINTE("Fail! The CPU model name expected:[%s], Actually:[%s]" % (exp_mode_name, model_name))


def CheckFullyBMCVersion(exp_version=full_bmc_version):
    """
    Get the complete BMC version, including 4 decimal places
    e.g:2.12.13
    :exp_version:Fully BMC version
    """
    cmd = "ipmitool mc info"
    res = execute_cmd(cmd)
    re_version = r'Firmware Revision\s+:\s+(\S+)'
    bmc_version = re.findall(re_version, res)[0]
    info_list = res.splitlines()
    version = ""
    for i in info_list:
        if "Aux Firmware Rev Info" in i:
            little_version_line = info_list.index(i) + 1
            little_version = (info_list[little_version_line]).strip().split("x")[1]
            version = "%s.%s" % (bmc_version, little_version)
    CheckInfoEqual(exp_version, version)


def CheckSensorList():
    """
    According to the configuration of 'status_error_list' in SIT_variable.py, confirm whether 'status_error_list'
    is included in 'ipmitool sdr' and check whether the sensor with a limited range is within the limited range
    """
    cmd = "ipmitool sensor list"
    res = execute_cmd(cmd, timeout=300)
    status_list = list()
    for i in res.splitlines():
        status = i.split("|")[3]
        status_list.append(status.strip())
    if status_error_list:
        error_info = [x for x in status_error_list if x in status_list]
        if error_info:
            whitebox_lib.PRINTE("Fail! %s in response! Response:\n%s" % (error_info, res))

    for x in res.splitlines():
        try:
            actual_value = float(x.split("|")[1])
            min_value = float(x.split("|")[5])
            max_value = float(x.split("|")[8])
            name = x.split("|")[0].strip()
        except ValueError:
            continue
        if min_value <= actual_value <= max_value:
            pass
        else:
            whitebox_lib.PRINTE("Fail! [%s] actual value is not within the limit. Response:\n%s" % (name, res))


def CheckFruListInfo():
    """
    Use 'diff' for text comparison. Before calling, you need to manually send the command 'ipmitool fru list' to
    the corresponding folder as a comparison standard file.
    """
    cmd = "ipmitool fru list"
    file_name = "fru_list_%s.log" % str(datetime.datetime.now()).split(".")[0].replace(" ", "_").replace(":", "-")
    dut_log_path = fru_list_standard_comparison_log.replace("/fru_list_standard.log", "")
    dut_log = fru_list_standard_comparison_log.replace("fru_list_standard.log", file_name)
    execute_cmd("%s > %s" % (cmd, dut_log))
    Logger.info("Standard File Information:")
    execute_cmd("cat %s" % fru_list_standard_comparison_log)
    res = execute_cmd("diff %s %s" % (fru_list_standard_comparison_log, dut_log))
    if ">" in res or "<" in res:
        if "---" in res:
            Logger.error("error File Information:")
            execute_cmd("cat %s" % dut_log)
            CopyFileToPC(dut_log_path, fru_list_standard_comparison_log.split("/")[-1], pc_path_fail_fru_list)
            CopyFileToPC(dut_log_path, file_name, pc_path_fail_fru_list)
            whitebox_lib.PRINTE("Fail! diff response:\n%s\n\nFail file PC path:[%s]" % (res, pc_path_fail_fru_list + "/"
                                                                                        + file_name))
    Logger.info("Now, will del %s" % dut_log)
    execute_cmd("rm -rf %s" % dut_log)


def GetBMCIp(eth_type='dedicated', ipv6=False):
    """
    Use IPMI command to get BMC IP address
    :param eth_type: Network port type: dedicated, shared
    :param ipv6: Whether to get IPV6, if False, get IPV4
    :return: IP address
    """
    return whitebox_lib.get_ip_address_from_ipmitool(deviceType, eth_type, ipv6)


def CheckBMCIP(exp_address_source=str_ip_address_source, exp_bmc_ip=str_bmc_ip, exp_subnet_mask=str_subnet_mask,
               exp_mac=str_mac):
    """
    Send 'ipmitool lan print 1' and check informations
    :param exp_address_source: expected IP Address Source
    :param exp_bmc_ip: expected IP Address
    :param exp_subnet_mask: expected Subnet Mask
    :param exp_mac: expected MAC Address
    """
    cmd = "ipmitool lan print 1"
    res = execute_cmd(cmd)
    ip_status = re.findall(r"IP Address Source\s+:\s+(.*)", res)[0].strip()
    bmc_ip = GetBMCIp()
    subnet_mask = re.findall(r"Subnet Mask\s+:\s+(.*)", res)[0].strip()
    mac = re.findall(r"MAC Address\s+:\s+(.*)", res)[0].strip()
    Logger.info("IP Address Source:%s, IP Address:%s, Subnet Mask:%s, MAC Address:%s" %
                (ip_status, bmc_ip, subnet_mask, mac))
    if exp_address_source:
        CheckInfoEqual(exp_address_source, ip_status)
    if exp_bmc_ip:
        CheckInfoEqual(exp_bmc_ip, bmc_ip)
    if exp_subnet_mask:
        CheckInfoEqual(exp_subnet_mask, subnet_mask)
    if exp_mac:
        CheckInfoEqual(exp_mac, mac)


def InitForLspciAndFru():
    """
    After running this function, you need to manually confirm whether the corresponding Lspci and Fru returns
    are correct
    """
    path = r"/home/sit/system_information"
    execute_cmd("mkdir -p %s" % path)
    execute_cmd("lspci > %s" % lspci_standard_comparison_log)
    execute_cmd("ipmitool fru list > %s" % fru_list_standard_comparison_log)
    # Logger.info("###################################################################################################\n"
    #             "'Lspci' and 'ipmitool fru list' log has been generated. Log path: /home/sit/system_information/..\n"
    #             "Whether both documents meet expectations(Y/N):")
    # result = input()
    # Logger.info("###################################################################################################")
    # if result.lower() == "n":
    #     whitebox_lib.PRINTE("Fail! Two documents did not meet expectations")


def CheckLspciAllInfo():
    """
    Check whether the number of rows responded by 'lspci' is equal to the expected
    """
    cmd = r"lspci"
    file_name = "lspci_%s.log" % str(datetime.datetime.now()).split(".")[0].replace(" ", "_").replace(":", "-")
    dut_log_path = lspci_standard_comparison_log.replace("/lspci_standard.log", "")
    dut_log = lspci_standard_comparison_log.replace("lspci_standard.log", file_name)
    device_obj.sendline("%s > %s" % (cmd, dut_log))
    Logger.info("Standard File Information:")
    execute_cmd("cat %s" % lspci_standard_comparison_log)
    res = execute_cmd("diff %s %s" % (lspci_standard_comparison_log, dut_log))
    if ">" in res or "<" in res:
        if "---" in res:
            Logger.error("error File Information:")
            execute_cmd("cat %s" % dut_log)
            CopyFileToPC(dut_log_path, lspci_standard_comparison_log.split("/")[-1], pc_path_fail_lspci)
            CopyFileToPC(dut_log_path, file_name, pc_path_fail_lspci)
            whitebox_lib.PRINTE("Fail! diff response:\n%s\n\nFail file PC path:[%s]" % (res, pc_path_fail_lspci + "/" +
                                                                                        file_name))
    Logger.info("Now, will del %s" % dut_log)
    execute_cmd("rm -rf %s" % dut_log)


def CheckLnKCapLnkSta(lnk_cap=lnkcap_list, lnk_sta=lnksta_list, error_ignore=ce_de_ue_ignore_list):
    """
    Send 'lspci -vvv' to check the 'Speed','width' field values in'LnkSta','LnkCap',
    And check the field values that cannot be included in the field values of'CESta','DevSta','UESta'
    :param lnk_cap: The value of'LnkCap' to be checked, list[dict{name:(Speed, width)}]
    :param lnk_sta: The value of'LnkSta' to be checked, list[dict{name:(Speed, width)}]
    :param error_ignore: Ignorable fields containing'+'.
                         e.g  [{device name: [[CESta ignore], [DevSta ignore], [UESta ignore]]}]
    """
    cmd = "lspci -vvv"
    res = execute_cmd(cmd, 60)
    lnkcap_info = list()
    lnksta_info = list()
    for line in res.split("\n\r\n"):
        if "LnkCap" and "LnkSta" in line:
            name = re.findall(r"(\w{2}:\w{2}\.\w)\s", line)[0]
            lnkcap = re.findall(r"LnkCap:.*Speed (.*), Width (.*?),", line)[0]
            lnksta = re.findall(r"LnkSta:.*Speed (.*), Width (.*?),", line)[0]
            lnkcap_info.append({name: lnkcap})
            lnksta_info.append({name: lnksta})
    Logger.info(r"lnkcap_info:%s" % str(lnkcap_info))
    Logger.info(r"lnksta_info:%s" % str(lnksta_info))
    if lnk_cap and lnk_sta:
        aaa = [x for x in lnk_cap if x not in lnkcap_info]
        bbb = [x for x in lnk_sta if x not in lnksta_info]
        if aaa:
            whitebox_lib.PRINTE("Fail! %s Not in the expected LnkCap configuration!" % aaa)
        if bbb:
            whitebox_lib.PRINTE("Fail! %s Not in the expected LnkSta configuration!" % bbb)

    error_name_list = list()
    error_value_list = list()
    for line in res.split("\n\r\n"):
        if "CESta" and "DevSta" and "UESta" in line:
            c_e = list()
            d_e = list()
            u_e = list()
            name = re.findall(r"(\w{2}:\w{2}\.\w)\s", line)[0]
            c_e_ = re.findall(r"CESta:\s+(.*)", line)
            if c_e_:
                c_e_list = c_e_[0].split(" ")
                for _ in c_e_list:
                    if "+" in _:
                        c_e.append(_)
            d_e_ = re.findall(r"DevSta:\s+(.*)", line)
            if d_e_:
                d_e_list = d_e_[0].split(" ")
                for _ in d_e_list:
                    if "+" in _:
                        d_e.append(_)
            u_e_ = re.findall(r"UESta:\s+(.*)", line)
            if u_e_:
                u_e_list = u_e_[0].split(" ")
                for _ in u_e_list:
                    if "+" in _:
                        u_e.append(_)
            error_name_list.append(name)
            error_value_list.append([c_e, d_e, u_e])
    for i in error_ignore:
        for key, value in i.items():
            try:
                error_value = error_value_list[error_name_list.index(key)]
                for j in error_value:
                    if j:
                        b = error_value.index(j)
                        a = [x for x in j if x not in value[b]]
                        if a:
                            whitebox_lib.PRINTE("get error info:{%s: %s}" % (key, error_value))
            except ValueError as E:
                Logger.info(str(E))
                whitebox_lib.PRINTE("Fail! [%s] No information of 'CESta' 'DevSta' 'UESta' " % key)


def CheckBIOSVersion(exp_version=bios_version, exp_vendor=vendor, rep_release_date=release_date):
    """
    Send 'dmidecode -t bios' and check information
    :param exp_version: bios version
    :param exp_vendor: Vendor
    :param rep_release_date: Release Date
    """
    cmd = r"dmidecode -t bios"
    res = execute_cmd(cmd)
    vendor_ = re.findall(r"Vendor:\s+(.*)", res)[0].strip()
    release_date_ = re.findall(r"Release Date:\s+(.*)", res)[0].strip()
    if exp_vendor != "":
        if exp_vendor != vendor_:
            whitebox_lib.PRINTE("Fail! exp vendor:[%s], got vendor:[%s]" % (exp_vendor, vendor_))
    if rep_release_date != "":
        if rep_release_date != release_date_:
            whitebox_lib.PRINTE("Fail! exp Release Date:[%s], got Release Date:[%s]"
                                % (rep_release_date, release_date_))
    bios = re.findall(r"Version:\s+(.*)", res)[0].strip()
    CheckInfoEqual(bios, exp_version)


def CheckOSIp(exp_ip_info=os_ip_list):
    """
    Check the IP information of the OS through "ifconfig -a"
    :param exp_ip_info: e.g[{"eth0": ("inet","netmask", "broadcast", "ether", "RX errors", "TX errors")}]
                        If the broadcast field does not exist, write "" in the 'broadcast' field value
    """
    cmd = "ifconfig -a"
    res = execute_cmd(cmd)
    info_list = res.split("\n\r\n")
    os_ip_info_list = list()
    for i in info_list:
        key = re.findall("(.*?): flags=", i)[0]
        os_ip = re.findall(r"inet\s+(\d+\.\d+\.\d+\.\d+)", i)
        if os_ip:
            os_ip = os_ip[0].strip()
            netmask = re.findall(r"netmask\s+(\d+\.\d+\.\d+\.\d+)", i)
            netmask = netmask[0].strip() if netmask else ""
            broadcast = re.findall(r"broadcast\s+(\d+\.\d+\.\d+\.\d+)", i)
            broadcast = broadcast[0].strip() if broadcast else ""
            ether = re.findall(r"ether\s(.*?)\s", i)
            ether = ether[0].strip() if ether else ""
            rx_errors = re.findall(r"RX errors\s+(\d+)\s+dropped", i)
            rx_errors = rx_errors[0].strip() if rx_errors else ""
            tx_errors = re.findall(r"TX errors\s+(\d+)\s+dropped", i)
            tx_errors = tx_errors[0].strip() if tx_errors else ""
            if os_ip != "127.0.0.1" and os_ip != "0.0.0.0":
                os_ip_info_list.append({key: (os_ip, netmask, broadcast, ether, rx_errors, tx_errors)})
    Logger.info("Got ip info dict: %s" % os_ip_info_list)
    if os_ip_info_list:
        if exp_ip_info:
            for _ in exp_ip_info:
                if _ not in os_ip_info_list:
                    whitebox_lib.PRINTE("Fail! %s doesn't match the OS IP information" % str(_))
    else:
        whitebox_lib.PRINTE("Fail! Couldn't got OS ip! Response:\n%s" % res)


def CheckEthtoolSpeedLinkStatus(ethtool_info_dict=ethool_speed_link_detected_dict):
    """
    Check 'ethtool network port name' info:Speed, Link detected
    :param ethtool_info_dict: dict. {'Network port name': 'speed Link detected'} e.g:{"ma1"：”1000 yes“}
    """
    ethtool_dict = dict()
    for key, value in ethtool_info_dict.items():
        cmd = "ethtool %s" % key
        res = execute_cmd(cmd)
        speed = re.findall(r"Speed:\s+(\d+)Mb/s", res)[0]
        status = re.findall(r".*Link detected:(.*)", res)[0]
        ethtool_dict.update({key: "%s%s" % (speed, status)})
    CheckInfoEqual(ethtool_dict, ethtool_info_dict)


def CheckMemtotalSize(memtotal=memtotal_G):
    """
    Check that the value of the 'memtotal' field in 'cat /proc/meminfo' is within the expected
    value plus or minus 1.(±1)
    :param memtotal:Expected memory value(G).±1
    """
    cmd = r"cat /proc/meminfo"
    res = execute_cmd(cmd)
    memory_size_kb = re.findall(r"MemTotal:\s+(\d+)\s+kB", res)[0]
    memory_size_g = int(memory_size_kb) / 1024 / 1024
    if int(memtotal) - 1 <= memory_size_g <= int(memtotal) + 1:
        pass
    else:
        whitebox_lib.PRINTE("Fail! Expected memory size:[%s, %s], actual:[%s].Response:\n%s" %
                            (int(memtotal) - 1, int(memtotal) + 1, memory_size_g, res))


def CheckMemFreeSize(memfree=free_g):
    """
    Check that the value of the 'memfree' field in 'cat /proc/meminfo' is within the expected
    value plus or minus 1.(±1)
    :param memfree:Expected memory free value(G).±1
    """
    cmd = r"cat /proc/meminfo"
    res = execute_cmd(cmd)
    memory_size_kb = re.findall(r"MemFree:\s+(\d+)\s+kB", res)[0]
    memory_size_g = int(memory_size_kb) / 1024 / 1024
    if int(memfree) - 1 <= memory_size_g <= int(memfree) + 1:
        pass
    else:
        whitebox_lib.PRINTE("Fail! Expected memory free size:[%s, %s], actual:[%s].Response:\n%s" %
                            (int(memfree) - 1, int(memfree) + 1, memory_size_g, res))


def SetElementAsString(list_name):
    x = list()
    for i in list_name:
        x.append(i.strip)
    return list(x)


def CheckDmiMemoryInfo(mem_number=mem_num, mem_info_list=dmi_memory_info_list):
    """
    Send "dmidecode -t memory", check the number of memory modules and the information of all memory modules
    'size','manufacturer','serial number','part number','configured clock speed'
    :param mem_number:Expected memory number
    :param mem_info_list:All the check info. list[dict].
                         e.g:[{"speed":[speed1, speed2...]， {”manufacturer“: [manufacturer1, manufacturer2...], ...]
    """
    cmd = r"dmidecode -t memory"
    res = execute_cmd(cmd)
    count = res.count("Memory Device")
    if int(mem_number) != count:
        whitebox_lib.PRINTE("Fail! Expected the number of memory:[%s], actual:[%s].Response:\n%s" %
                            (mem_number, count, res))
    size_list_ = re.findall("Size: (.*)", res)
    size_list = list()
    for _ in size_list_:
        size_list.append(_.strip())
    manufacturer_list_ = re.findall("Manufacturer: (.*)", res)
    manufacturer_list = list()
    for _ in manufacturer_list_:
        manufacturer_list.append(_.strip())
    serial_number_list_ = re.findall("Serial Number: (.*)", res)
    serial_number_list = list()
    for _ in serial_number_list_:
        serial_number_list.append(_.strip())
    part_number_list_ = re.findall("Part Number: (.*)", res)
    part_number_list = list()
    for _ in part_number_list_:
        part_number_list.append(_.strip())
    configured_clock_speed_list_ = re.findall("Configured Clock Speed: (.*)", res)
    configured_clock_speed_list = list()
    for _ in configured_clock_speed_list_:
        configured_clock_speed_list.append(_.strip())
    speed_list = list()
    for _ in res.splitlines():
        if "Speed" in _ and "Configured Clock Speed" not in _:
            speed_list_ = re.findall(r"Speed:\s+(.*)", _)[0].strip()
            speed_list.append(speed_list_)

    CheckInfoEqual(mem_info_list[0]["size"], size_list)
    CheckInfoEqual(mem_info_list[1]["manufacturer"], manufacturer_list)
    CheckInfoEqual(mem_info_list[2]["serial_number"], serial_number_list)
    CheckInfoEqual(mem_info_list[3]["part_number"], part_number_list)
    CheckInfoEqual(mem_info_list[4]["configured_clock_speed"], configured_clock_speed_list)
    CheckInfoEqual(mem_info_list[5]["speed"], speed_list)


def CheckCpuInfo(info_list=cpu_info_list):
    """
    Send 'cat /proc/cpuinfo', check the value of 'cpu MHz', 'cache size', 'cpu cores' and the number of thread
    :param info_list: list[dict]. eg:[{'cpu_MHz': [800, 900]}, {"cache_size": 3072}]
    """
    CheckCPUModeName()
    cmd = r"cat /proc/cpuinfo"
    res = execute_cmd(cmd)

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
        if float(info_list[0]["cpu_MHz"][0])-50 <= float(i) <= float(info_list[0]["cpu_MHz"][1])+50:
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


def CheckLsBlk(ssd_num=M2_ssd_number):
    """
    Send 'lsblk', Confirm the number of hard drives
    :param ssd_num:Expected the number of hard drives
    :param ssd_num:Expected the number of hard drives
    """
    cmd = r"lsblk"
    res = execute_cmd(cmd)
    ssd_name = re.findall(r'sd([a-z])', res)[-1]
    CheckInfoEqual(ssd_num, a_z_number_correspondence[ssd_name])


def CheckSmartctlInfo(ssd_num=1, model=device_model, ser_num=serial_number,
                      fw_version=firmware_version, capacity=user_capacity):
    """
    Send ’smartctl -a /dev/sdX(a,b,c...)‘, check 'Device Model', 'Serial Number', 'Firmware Version', 'User Capacity'
    :param ssd_num:Expected the number of hard drives. int
    :param model:Device Model. List
    :param ser_num:Serial Number. List
    :param fw_version:Firmware Version. List
    :param capacity:User Capacity. List
    """
    end_device_name = ""
    device_list = list()
    serial_number_list = list()
    fw_version_list = list()
    user_capacity_list = list()
    for i in range(ord("a"), ord("z") + 1):
        if i - 96 == int(ssd_num):
            end_device_name = chr(i)
            break
    for name in range(ord("a"), ord(end_device_name) + 1):
        device_name = chr(name)
        cmd = r"smartctl -a /dev/sd%s" % device_name
        res = execute_cmd(cmd)
        device = re.findall(r"Device Model:\s+(.*)", res)[0].strip()
        serial_num = re.findall(r"Serial Number:\s+(.*)", res)[0].strip()
        fw_v = re.findall(r"Firmware Version:\s+(.*)", res)[0].strip()
        user_cap = re.findall(r"User Capacity:.*\[(.*)\sGB]", res)[0].strip()
        device_list.append(device)
        serial_number_list.append(serial_num)
        fw_version_list.append(fw_v)
        user_capacity_list.append(user_cap)
    CheckInfoEqual(model, device_list)
    CheckInfoEqual(ser_num, serial_number_list)
    CheckInfoEqual(fw_version, fw_version_list)
    CheckInfoEqual(capacity, user_capacity_list)


def SetDmesgClear():
    cmd = "dmesg -C"
    execute_cmd(cmd)


def SetBiosByStep(step_list, reboot=True, connect_os=False, done_flag=None):
    """
    Enter the bios interface and follow the steps to set U Disk/DVD-ROM as the first boot item
    :param step_list:Setup steps。List
    :param reboot:True/False
    :param connect_os:True/False
    :param done_flag:Flag to be checked after the step is completed
    """
    if reboot:
        device_obj.sendline("reboot")
    enter_bios_line = r"to enter setup."
    device_obj.read_until_regexp(enter_bios_line, timeout=150)
    bios_menu_lib.send_key(deviceType, "KEY_F2")
    for step in step_list:
        bios_menu_lib.send_key(deviceType, "KEY_%s" % step.upper())
        time.sleep(2)
    if done_flag:
        device_obj.read_until_regexp(done_flag, timeout=30)
    if connect_os:
        return connect()


def GetUSBDeviceName():
    """
    Get the drive letter name of the USB device (the last one)
    :return:Device name
    """
    tool_path = get_tool_path() + "/sit"
    file_name = "lsscsi"
    whitebox_lib.mkdir_data_path(deviceType, dut_file_path)
    whitebox_lib.copy_files_from_pc_to_os(deviceType, pc_user, pc_password, pc_ip, file_name,
                                          tool_path, dut_file_path, 5)
    whitebox_lib.chmod_file(deviceType, dut_file_path + "/" + file_name)
    device_obj.sendline("cd %s" % dut_file_path)
    res = execute_cmd("./%s" % file_name)
    disk_name = re.findall(r"(/dev/.*)", res)[-1]
    return disk_name


def CheckFileFromUDisk(disk_name=usb_mount_name):
    """
    Plug in the U disk, create a new 1024M file in the U disk and copy it to the device, use MD5 to calculate
    whether the two files are exactly the same
    """
    GetUSBDeviceName()
    respond = execute_cmd("mount %s /mnt" % disk_name)
    if 'not exist' not in respond:
        device_obj.sendline("cd /mnt")
        execute_cmd("dd if=/dev/zero of=test.file bs=1024M count=1")
        execute_cmd("cp test.file %s" % dut_file_path)
        device_obj.sendline("cd /")
        res_1 = execute_cmd("md5sum -t /mnt/test.file", timeout=10)
        res_2 = execute_cmd("md5sum -t %s/test.file" % dut_file_path, timeout=10)
        whitebox_lib.delete_folder(deviceType, "%s/test.file" % dut_file_path)
        device_obj.sendline("umount /mnt")
        Logger.info("Pls remove the USB flash drive!!!")
        if res_1.split("  ")[0] != res_2.split("  ")[0]:
            whitebox_lib.PRINTE("Fail! The MD5 value of the file in the U disk is different from that of the file"
                                " in the device.[U_Disk]: %s, [Device]: %s" % (res_1, res_2))
    else:
        whitebox_lib.PRINTE("Fail! The USB %s mount failed" % disk_name)


def CheckUSBTransferSpeed(min_speed=usb_min_speed, frequency=1, usb_name=cmd_usb_name):
    """
    Check whether the USB transmission speed is less than the expected minimum limit
    :param min_speed:Expected minimum limit
    :param frequency:Number of inspections
    :param usb_name:USB drive name
    """
    error_times = 0
    error_speed_list = list()
    for i in range(1, frequency + 1):
        device_obj.sendline('lsusb -t')
        for j in range(len(usb_name)):
            cmd = r"hdparm -t %s" % usb_name[j]
            res = execute_cmd(cmd)
            actual_speed = re.findall(r"seconds\s+=\s+(.*)\s+MB/sec", res)
            if actual_speed:
                float_speed = float(actual_speed[0])
                if float_speed < min_speed:
                    error_times += 1
                    error_speed_list.append({"%s th" % i: actual_speed})
            else:
                error_times += 1
                error_speed_list.append("Couldn't got USB device transfer speed")
                whitebox_lib.PRINTE("Fail! Couldn't got USB device transfer speed. response:\n%s" % res, decide=False)
    if error_times != 0:
        whitebox_lib.PRINTE("Fail! Fail times:[%s]. Expected minimum speed:[%s], Less than its speed:%s"
                            % (error_times, min_speed, error_speed_list))


def SetSelClear(bmc_ip=None):
    return whitebox_lib.set_sel_clear(deviceType, bmc_ip)


def GetCPULoad():
    """
    Got CPU Load by command 'top -d 1 -n 2'
    :return: cpu usage(float)
    """
    cmd = r"top -d 1 -n 2"
    device_obj.sendline(cmd)
    device_obj.read_until_regexp("us,", timeout=3)
    res = device_obj.read_until_regexp("us,", timeout=3)
    cpu_usage = float(re.findall(r"zombie.*Cpu.*\s+(.*)\s+.*", res, re.S)[0])
    Logger.info("Got CPU Load: %s" % str(cpu_usage))
    return cpu_usage


def RunStreamIray(min_num=expect_min_num):
    """
    Run 'stream-iray' and check response.
    :param min_num: The value that the response must be less than
    """
    tool_path = get_tool_path() + "/sit"
    file_name = "stream-iray"
    whitebox_lib.mkdir_data_path(deviceType, cpu_full_load_path)
    whitebox_lib.copy_files_from_pc_to_os(deviceType, pc_user, pc_password, pc_ip, file_name,
                                          tool_path, cpu_full_load_path, 5)
    whitebox_lib.chmod_file(deviceType, cpu_full_load_path + "/" + file_name)
    device_obj.sendline("cd %s" % cpu_full_load_path)
    res = execute_cmd("./%s" % file_name)
    info = re.findall(r".*:\s{6,}(.*?)\s+", res)
    if info:
        for i in info:
            i = float(i)
            if i < min_num:
                whitebox_lib.PRINTE("Fail! Expect min number:[%s], info:[%s]" % (min_num, info))
        device_obj.sendline("cd /")
        execute_cmd("rm -rf %s" % cpu_full_load_path)
    else:
        whitebox_lib.PRINTE("Fail! Couldn't got stream-iray response info!")


def RunOrKillCPUFullLoad(cpu_platform=dut_cpu_platform, kill=False, background=True):
    """
    Run the corresponding PTU program to make the CPU full or kill the corresponding process
    :param cpu_platform:CPU platform and architecture, reference 'SIT_variable.py' cpu_platform_dict
    :param kill:True/False
    :param background:Whether to run in the background
    """
    flag = " &" if background else ""
    if cpu_platform not in cpu_platform_dict.keys():
        whitebox_lib.PRINTE("Fail! CPU platform:[%s] not in platform information form.")
    cpu_info = cpu_platform_dict.get(cpu_platform)
    file_name_1 = cpu_info[1]
    file_name_2 = cpu_info[2] if len(cpu_info) > 2 else None
    if kill:
        KillProcess(file_name_1)
        if file_name_1 == "BroadwellPTU_Re":
            KillProcess("RunPTUT0")
            KillProcess("RunPTUT1")
        if file_name_2:
            KillProcess(file_name_2)
        return None
    execute_cmd("mkdir -p %s" % cpu_full_load_path)
    tool_path = get_tool_path() + "/sit/PTU/%s" % cpu_info[0]
    res = Device.execute_local_cmd(device_obj, "ls %s" % tool_path)
    file_list = res.splitlines()
    for file_name in file_list:
        whitebox_lib.copy_files_from_pc_to_os(deviceType, pc_user, pc_password, pc_ip, file_name,
                                              tool_path, cpu_full_load_path, 15)
        whitebox_lib.chmod_file(deviceType, cpu_full_load_path + "/" + file_name)
    device_obj.sendline("cd %s" % cpu_full_load_path)
    device_obj.sendline("echo y | ./%s%s" % (file_name_1, flag))
    SetWait(20)
    cpu_usage = get_cpu_usage()
    if cpu_usage < 80:
        whitebox_lib.PRINTE("Fail! CPU usage is less than 99%% after running %s, it's:%s%%" % (file_name_1, cpu_usage))
    if file_name_2:
        log_name = "%s%s.log" % (file_name_2, str(datetime.datetime.now()).split(" ")[0])
        device_obj.sendline("cd %s" % cpu_full_load_path)
        device_obj.sendline("echo y | ./%s > %s/%s%s" % (file_name_2, cpu_full_load_path, log_name, flag))
        time.sleep(5)
        Logger.info("%s running..." % file_name_2)
    device_obj.sendline("cd /")


def RunFio(background=True):
    """
    Run 'fio'
    :param background:Whether to run in the background
    """
    flag = " &" if background else ""
    tool_path = get_tool_path() + "/sit"
    file_name = "fio"
    whitebox_lib.mkdir_data_path(deviceType, cpu_full_load_path)
    whitebox_lib.copy_files_from_pc_to_os(deviceType, pc_user, pc_password, pc_ip, file_name,
                                          tool_path, cpu_full_load_path, 5)
    whitebox_lib.chmod_file(deviceType, cpu_full_load_path + "/" + file_name)
    device_obj.sendline("cd %s" % cpu_full_load_path)
    log_name = "fio_%s.log" % str(datetime.datetime.now()).split(" ")[0]
    cmd = r"fio --name=seq_read --filename=/dev/sda --direct=1 --thread=1 --numjobs=1 --iodepth=32 --rw=read " \
          r"--bs=128k --runtime=%sh --time_based=1 --group_reporting --log_avg_msec=1000 --bwavgtime=1000 " \
          r"--write_bw_log=seq_read > %s/%s%s" % (runing_time * 24, cpu_full_load_path, log_name, flag)
    device_obj.sendline("./%s" % cmd)
    time.sleep(5)
    Logger.info("%s running..." % file_name)
    device_obj.sendline("cd /")


def GetMemoryFree(unit="m"):
    """
    Got memory free size
    :param unit: g/m/k ...
    """
    cmd = r"free -%s" % unit.lower()
    res = execute_cmd(cmd)
    size = float(re.findall(r'Mem:\s+\d+\s+\d+\s+(\d+).*', res)[0])
    return size


def RunStressapptest(run_time=runing_time, background=True, project_name=r"midstone100X"):
    """
    Run 'stressapptest'
    :param project_name: Project tool folder name
    :param run_time: Running time .unit:day
    :param background:Whether to run in the background
    """
    flag = " &" if background else ""
    run_time = run_time * 24 * 60 * 60
    tool_path = get_tool_path(project_name) + "/sit"
    file_name = "stressapptest"
    whitebox_lib.mkdir_data_path(deviceType, cpu_full_load_path)
    whitebox_lib.copy_files_from_pc_to_os(deviceType, pc_user, pc_password, pc_ip, file_name,
                                          tool_path, cpu_full_load_path, 5)
    whitebox_lib.chmod_file(deviceType, cpu_full_load_path + "/" + file_name)
    device_obj.sendline("cd %s" % cpu_full_load_path)
    log_name = "stressapptest_%s.log" % str(datetime.datetime.now()).split(" ")[0]
    size = GetMemoryFree() * 0.9
    cmd = "%s -M %s -s %s > %s/%s%s" % (file_name, size, run_time, cpu_full_load_path, log_name, flag)
    device_obj.sendline("./%s" % cmd)
    time.sleep(5)
    Logger.info("%s running..." % file_name)
    device_obj.sendline("cd /")


def RunOrKillMemtester(background=True, kill=False):
    """
    Run 'memtester' or kill it
    :param background: Whether to run in the background
    :param kill: True/False
    """
    file_name = "memtester"
    flag = " &" if background else ""
    tool_path = get_tool_path() + "/sit"
    if kill:
        KillProcess(file_name)
        return
    whitebox_lib.mkdir_data_path(deviceType, cpu_full_load_path)
    whitebox_lib.copy_files_from_pc_to_os(deviceType, pc_user, pc_password, pc_ip, file_name,
                                          tool_path, cpu_full_load_path, 5)
    whitebox_lib.chmod_file(deviceType, cpu_full_load_path + "/" + file_name)
    device_obj.sendline("cd %s" % cpu_full_load_path)
    log_name = "memtester_%s.log" % str(datetime.datetime.now()).split(" ")[0]
    size = int(GetMemoryFree() * 0.9)
    cmd = "%s %sM %s > %s/%s%s" % (file_name, size, str(memtester_loop), cpu_full_load_path, log_name, flag)
    memtester_info = execute_cmd("./%s" % cmd, timeout=432000)
    Logger.info(memtester_info)
    time.sleep(5)
    Logger.info("%s running..." % file_name)
    device_obj.sendline("cd /")


def CopyFileToPC(filepath=cpu_full_load_path, filename=".log", destination_path=pc_log_path):
    """
    Copy a certain type of file to PC(DUT->PC)
    :param filepath: DUT file path
    :param filename: DUT file name
    :param destination_path: PC path
    """
    Device.execute_local_cmd(device_obj, "mkdir -p %s" % destination_path, timeout=10)
    device_obj.sendline("cd %s" % filepath)
    res = execute_cmd("ls | grep %s" % filename)
    for i in res.splitlines():
        whitebox_lib.copy_files_from_pc_to_os(deviceType, pc_user, pc_password, pc_ip, i.strip(), filepath,
                                              destination_path, 15, True)
    device_obj.sendline("cd /")


def GetFullFileName(filename, filepath=pc_log_path, pc=True):
    """
    Get file full name
    :param filename: Characters included in the file name
    :param filepath:file path
    :param pc:PC/DUT
    :return:file full name
    """
    cmd = "ls %s | grep %s" % (filepath, filename)
    res = Device.execute_local_cmd(device_obj, cmd) if pc else execute_cmd(cmd)
    return res.strip()


def CheckStressapptestLog(pass_keyword=stressapptest_pass_keyword):
    """
    check 'stressapptest' log
    """
    log_name = GetFullFileName("stressapptest_")
    with open(r"%s/%s" % (pc_log_path, log_name), "r") as f:
        all_info = f.read()
        if pass_keyword not in all_info:
            whitebox_lib.PRINTE("Fail! Couldn't find keyword:[%s] in %s" % (pass_keyword, log_name))


def CheckMemtesterLog():
    """
    check 'Memtester' log
    """
    log_name = GetFullFileName("memtester_")
    with open(r"%s/%s" % (pc_log_path, log_name), "r", encoding="UTF-8") as f:
        all_info = f.read()
        log.info(all_info)
        loop_count = all_info.count("Loop")
        if loop_count:
            ok_num = 18 * (loop_count - 1)
            actual_ok = all_info.count("ok")
        else:
            whitebox_lib.PRINTE("Fail! 'memtester' abnormal operation")

    with open(r"%s/%s" % (pc_log_path, log_name), "r", encoding="UTF-8") as ff:
        line_list = ff.readlines()
        ok_count = 0
        flag = False
        for line in line_list:
            if flag:
                if "ok" in line:
                    ok_count += 1
            else:
                if "Loop %s" % loop_count in line:
                    flag = True
    if (ok_num + ok_count) != actual_ok:
        whitebox_lib.PRINTE("Fail! '%s/%s' got Loop:[%s], 'ok'[%s]" % (pc_log_path, log_name, loop_count, actual_ok))


def CheckFioLog():
    log_name = GetFullFileName("fio_")
    with open(r"%s/%s" % (pc_log_path, log_name), "r", encoding="UTF-8") as f:
        info = f.read()
        if fio_pass_keyword not in info:
            whitebox_lib.PRINTE("Fail, Couldn't find keyword[%s] in log:%s" % (fio_pass_keyword, log_name))


def CheckCMDResponse(cmd, keyword, decide=True, re_s=False, pc=False, case_insensitive=False):
    """
    Send command and check keyword in response
    :param cmd: command
    :param keyword: keyword. List.
    :param decide: True/False
    :param re_s: re.S or not
    :param pc: pc or dut
    :param case_insensitive:case insensitive or not
    """
    res = Device.execute_local_cmd(device_obj, cmd) if pc else execute_cmd(cmd)
    if case_insensitive:
        res = res.lower()
        keyword = [x.lower() for x in keyword]
    for word in keyword:
        response = re.findall(r"%s" % word, res, re.S) if re_s else re.findall(r"%s" % word, res)
        if decide:
            if not response:
                whitebox_lib.PRINTE("Fail! Couldn't find keyword:[%s] in command[%s] response. response:\n%s"
                                    % (word, cmd, res))
        else:
            if response:
                whitebox_lib.PRINTE("Fail! Find keyword:[%s] in command[%s] response. response:\n%s"
                                    % (word, cmd, res))


def SetWait(wait_time):
    return whitebox_lib.set_wait(wait_time)


# ######################################### Caleb Start ############################################################
# ######################################### modify start ############################################################
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
                if process.strip(" ").split(" ")[-1] == process_name:
                    pid = process.strip(" ").split(" ")[0]  # add .strip(" ")
                    device_obj.sendline("kill -9 %s" % pid)
                    time.sleep(5)
                    send_key(deviceType, "KEY_ENTER", 3, 0)
                    Logger.info("Done! Has killed %s, PID[%s]" % (process_name, pid))
            return
        else:
            time.sleep(2)
    else:
        Logger.info("Couldn't find process:%s" % process_name)


def CheckLsCpu(ls_cpu_info=cpu_info_list):
    """
    Send 'lscpu'. Check 'Thread(s) per core', 'Model name', 'CPU MHz', 'L3 cache' value
    :param ls_cpu_info:list[dict] eg:[{'cpu_MHz': [800, 900]}, {"cache_size": 3072}]
    :return:
    """
    cmd = "lscpu"
    res = execute_cmd(cmd)
    thread_per_core = re.findall(r"Thread\(s\) per core:\s+(\d+)", res)[0]
    model_name = re.findall(r"Model name:\s+(.*)", res)[0].strip()
    cpu_mhz = re.findall(r"CPU MHz:\s+(.*)", res)[0].strip()
    cache_size = ls_cpu_info[1].get("cache_size")
    if cache_size:
        l3_cache = re.findall(r"L3 cache:\s+(.*)K", res)[0].strip()
        CheckInfoEqual(cache_size, l3_cache)
    CheckInfoEqual(int(int(ls_cpu_info[4]["thread_per_core"])), thread_per_core)
    CheckInfoEqual(cpu_model_name, model_name)
    if float(ls_cpu_info[0]["cpu_MHz"][0]) <= float(cpu_mhz) <= float(ls_cpu_info[0]["cpu_MHz"][1]):
        pass
    else:
        whitebox_lib.PRINTE("Fail! Expected range:%s, actual value is:%s.Response:\n%s" %
                            (ls_cpu_info[0]["cpu_MHz"], cpu_mhz, res))


def CheckDmesgInfo(error_keyword_list=dmesg_error_list):
    """
    Send 'dmesg' and check the response. Case insensitive
    :param error_keyword_list: error keyword. List
    """
    cmd = r"dmesg"
    res = execute_cmd(cmd)
    # info_list = res.split("\n")
    error_keyword_list_ = [x.lower() for x in error_keyword_list]
    # info_list_ = [z.lower() for z in info_list]
    info_list_ = res.lower()
    error_list = [j for j in error_keyword_list_ if j in info_list_]
    if error_list:
        Logger.error("Fail！ Find error keyword in 'dmesg' response(case insensitive)\n")
        for error_line in error_list:
            Logger.error(str(error_line))
        whitebox_lib.PRINTE("Fail! Find error keyword in 'dmesg' response!\n%s" % res)


def CheckSdrInfo():
    """
    According to the configuration of 'status_error_list' in SIT_variable.py, confirm whether 'status_error_list'
    is included in 'ipmitool sdr'
    """
    cmd = "ipmitool sdr"
    res = execute_cmd(cmd)
    status_list = list()
    for i in res.splitlines():
        # status = i.split("|")[1]
        status = i.split("|")[2]
        status_list.append(status.strip())
    if status_error_list:
        error_info = [x for x in status_error_list if x in status_list]
        if error_info:
            whitebox_lib.PRINTE("Fail! %s in response! Response:\n%s" % (error_info, res))


# ######################################### modify end ############################################################
def set_pdu_state(pdu_status, pdu_port, file_name="SilverstoneX"):
    """
    Control the operation of PDU to power on, power off, and restart the device
    :param file_name: tool directory name
    :param pdu_status:[on,off,reboot]
    :param pdu_port:The port number on the PDU of the device under test
    """
    tool_path = get_tool_path(file_name)
    status = pdu_status.lower()
    shell_name = ""
    if status == "on":
        shell_name = "PDU_ON.sh"
    elif status == "off":
        shell_name = "PDU_OFF.sh"
    elif status == "reboot":
        shell_name = "PDU_Reboot.sh"
    else:
        whitebox_lib.PRINTE("Fail! PDU status must be on,off,reboot!")
    pdu_shell_path = "%s/%s" % (tool_path, shell_name)
    cmd = "%s %s" % (pdu_shell_path, pdu_port)
    res = Device.execute_local_cmd(device_obj, cmd, timeout=60)
    if "Success" in res:
        Logger.info("[%s]: PDU has %s!" % (datetime.datetime.now(), status))
    else:
        whitebox_lib.PRINTE("Fail! PDU [%s] port [%s] fail!" % (pdu_status, pdu_port))


def set_pdu_state_connect_os(status, port, out_time=180, wait_time=None):
    """
    connec os after pdu send command
    :param status:[on,off,reboot]
    :param port:The port number on the PDU of the device under test
    :param out_time:connect os out time
    :param wait_time:Waiting time after operating PDU
    """
    set_pdu_state(status, port)
    connect(wait_time, timeout=out_time)
    whitebox_lib.set_os_ip_by_dhclient(deviceType)


def send_key(device, key_name, times=1, delay=2):
    Logger.debug('Entering send_key with args : %s' % (str(locals())))
    for i in range(times):
        Logger.debug("Sending %s #%d" % (key_name, i + 1))
        device_obj.sendline(KEY_DATA[key_name], CR=False)
        time.sleep(delay)


def get_tool_path(file_name="SilverstoneX"):
    path_1 = os.getcwd()
    path_2 = path_1.split("/")
    path_2.pop()
    path_list = path_2 + ["platform/whitebox/tool/%s" % file_name]
    tool_path = "/".join(path_list)
    return tool_path


def execute_cmd_without_deal(cmd, timeout=180, mode=None):
    Logger.debug('Entering Device execute with args : %s\n' % (str(locals())))
    if mode is not None:
        device_obj.getPrompt(mode, timeout)
    cmd = 'time ' + cmd
    return device_obj.sendCmdRegexp(cmd, response_end_flag, timeout)


def write_object_on_hdd(storage_name=cmd_storage_name):
    """
    Use Command "touch" to write a object in HDD and read it
    @Author: Caleb Mai <calebmai@celestica.com>
    :param storage_name: storage drive name. List
    """
    cmd_df = r"df -h"
    for i in range(len(storage_name)):
        if not re.findall(r"Disk\s+%s" % storage_name[i], execute_cmd_without_deal("fdisk -l")):
            whitebox_lib.PRINTE("Fail! No such drive: %s" % storage_name[i])
        if not re.findall(r"%s.*(/.*)\r" % storage_name[i], execute_cmd_without_deal(cmd_df)):
            execute_cmd_without_deal("mount %s /mnt" % storage_name[i])
        mount = re.findall(r"%s.*(/.*)\r" % storage_name[i], execute_cmd_without_deal(cmd_df))[0]
        ls = r"ls %s" % mount
        if re.findall(r"test100.txt", execute_cmd_without_deal(ls)):
            execute_cmd_without_deal("rm -rf %s/test100.txt" % mount)
            execute_cmd_without_deal(ls)
        cmd_touch = r"touch %s/test100.txt" % mount
        device_obj.sendline(cmd_touch)
        read_touch = execute_cmd_without_deal(ls)
        if not re.findall(r"test100.txt", read_touch):
            whitebox_lib.PRINTE("Fail! Couldn't read the object which write by command 'touch' at [%s]"
                                % storage_name[i])
        time.sleep(3)
        device_obj.sendline("rm -rf %s/test100.txt" % mount)
        device_obj.sendline("umount %s" % storage_name[i])


def check_storage_readwrite_speed(min_speed=storage_min_speed, frequency=1, storage_name=cmd_storage_name):
    """
        Check whether the hdd read/write speed is less than the expected minimum limit
        @Author: Caleb Mai <calebmai@celestica.com>
        :param min_speed:Expected minimum limit
        :param frequency:Number of inspections
        :param storage_name:storage drive name
    """
    error_times = 0
    error_speed_list = list()
    for i in range(1, frequency + 1):
        for j in range(len(storage_name)):
            cmd = r"hdparm -t %s" % storage_name[j]
            res = execute_cmd_without_deal(cmd)
            actual_speed = re.findall(r"seconds\s+=\s+(.*)\s+MB/sec", res)
            if actual_speed:
                float_speed = float(actual_speed[0])
                if float_speed < min_speed:
                    error_times += 1
                    error_speed_list.append({"%s th" % i: actual_speed})
            else:
                error_times += 1
                error_speed_list.append("Couldn't got HDD device read/write speed")
                whitebox_lib.PRINTE("Fail! Couldn't got HDD device read/write speed. response:\n%s" % res, decide=False)
    if error_times != 0:
        whitebox_lib.PRINTE("Fail! Fail times:[%s]. Expected minimum speed:[%s], Less than its speed:%s"
                            % (error_times, min_speed, error_speed_list))


def get_sandisk_usb_device_name(project_name=r"SilverstoneX"):
    """
    Get the drive letter of the fixed USB flash drive (SanDisk 3.0 64G)
    @Author: Caleb Mai <calebmai@celestica.com>
    :return:Device name. List
    """
    tool_path = get_tool_path(project_name) + "/sit"
    file_name = "lsscsi"
    whitebox_lib.mkdir_data_path(deviceType, dut_file_path)
    set_os_ip_by_dhclient(deviceType)
    whitebox_lib.copy_files_from_pc_to_os(deviceType, pc_user, pc_password, pc_ip, file_name,
                                          tool_path, dut_file_path, 5)
    whitebox_lib.chmod_file(deviceType, dut_file_path + "/" + file_name)
    device_obj.sendline("cd %s" % dut_file_path)
    res = execute_cmd_without_deal("./%s" % file_name)
    disk_name = re.findall(r"disk\s+SanDisk\s+Cruzer Glide 3\.0.*(/dev/sd.)", res)
    device_obj.sendline("cd /")
    if not disk_name:
        whitebox_lib.PRINTE("Fail! Could not find a 'SanDisk 3.0 64G' USB")
    return disk_name


def auto_detection_usb_device(usb_name):
    """
    check whether system can auto detection usb device
    @Author: Caleb Mai <calebmai@celestica.com>
    :param usb_name: USB Device name. List
    """
    error_num = 0
    error_list = list()
    cmd = r"fdisk -l"
    res = execute_cmd(cmd)
    for i in range(len(usb_name)):
        if not re.findall(r"Disk\s+%s" % usb_name[i], res):
            error_num += 1
            error_list.append("Can not auto detection the USB device : %s" % usb_name[i])
    if error_num != 0:
        whitebox_lib.PRINTE("Fail! %s" % error_list)


def run_fio_for_usb(usb_name, background=True, project_name=r"SilverstoneX"):
    """
    Run 'fio'
    @Author: Caleb Mai <calebmai@celestica.com>
    :param project_name: Project tool folder name
    :param usb_name: usb drive name
    :param background:Whether to run in the background
    """
    error_device = 0
    error_list = list()
    flag = " &" if background else ""
    tool_path = get_tool_path(project_name) + "/sit"
    file_name = "fio"
    whitebox_lib.mkdir_data_path(deviceType, USB_full_loading_path)
    set_os_ip_by_dhclient(deviceType)
    whitebox_lib.copy_files_from_pc_to_os(deviceType, pc_user, pc_password, pc_ip, file_name,
                                          tool_path, USB_full_loading_path, 5)
    whitebox_lib.chmod_file(deviceType, USB_full_loading_path + "/" + file_name)
    device_obj.sendline("cd %s" % USB_full_loading_path)
    for i in range(len(usb_name)):
        log_name = "fio_%s_%s.log" % (usb_name[i].split("/")[2], str(datetime.datetime.now()).split(" ")[0])
        cmd = r"fio --name=seq_read --filename=%s --direct=1 --thread=1 --numjobs=1 --iodepth=32 --rw=read " \
              r"--bs=128k --runtime=%s --time_based=1 --group_reporting --log_avg_msec=1000 --bwavgtime=1000 " \
              r"--write_bw_log=seq_read > %s/%s%s" % \
              (usb_name[i], usb_fio_running_time * 3600, USB_full_loading_path, log_name, flag)
        device_obj.sendline("./%s" % cmd)
        time.sleep(5)
    Logger.info("[%s]: %s running...pls wait %s hours"
                % (datetime.datetime.now(), file_name, usb_fio_running_time))
    time.sleep(usb_fio_running_time * 3600 + 5)
    device_obj.sendline("cd /")
    for i in range(len(usb_name)):
        log_name = "fio_%s_%s.log" % (usb_name[i].split("/")[2], str(datetime.datetime.now()).split(" ")[0])
        res = execute_cmd("cat %s/%s" % (USB_full_loading_path, log_name))
        actual_value = re.findall(r"READ: bw=\S+MiB/s\s+\((.*?)MB/s\)", res)
        if actual_value:
            actual_value = float(actual_value[0])
            if actual_value < fio_expected_value:
                error_device += 1
                error_list.append({"%s" % usb_name[i]: actual_value})
        else:
            error_device += 1
            error_list.append("Couldn't got USB device FIO read/write Speed")
            whitebox_lib.PRINTE("Fail! Couldn't got USB device FIO read/write Speed. response:\n%s" % res, decide=False)
    if error_device != 0:
        whitebox_lib.PRINTE("Fail! Fail times:[%s]. Expected minimum speed:[%s], Less than its speed:%s"
                            % (error_device, fio_expected_value, error_list))


def get_cpu_usage():
    """
    get cpu usage by command "top"
    @Author: Caleb Mai <calebmai@celestica.com>
    :return: cpu usage
    """
    cmd = r"top -n 2 -d 1|grep -i '%Cpu(s)'"
    for i in range(3):
        res = execute_cmd_without_deal(cmd)
        cpu_id = re.findall(r".*\s+(\d+\.\d+).*id", res)
        if cpu_id:
            return round(float(100) - float(cpu_id[1]), 2)
    whitebox_lib.PRINTE("Fail! Could not get cpu usage for three times")


def get_memory_usage():
    """
    get memory usage by command "free"
    @Author: Caleb Mai <calebmai@celestica.com>
    :return: memory usage
    """
    cmd = r"free -m | sed -n '2p' | awk '{print $3/$2*100}'"
    for i in range(3):
        res = re.findall(r"(.*)\r\n\r\nreal.*", execute_cmd_without_deal(cmd))
        if res:
            return res[0]
    whitebox_lib.PRINTE("Fail! Could not get memory usage for three times")


def check_cpu_usage(cpu_usage):
    """
    check cpu usage whether higher than 50%
    @Author: Caleb Mai <calebmai@celestica.com>
    :param cpu_usage: cpu usage. str without "%"
    """
    if float(cpu_usage) >= float(50):
        whitebox_lib.PRINTE("Fail! CPU usage higher than 50 percent. it was [%s]" % cpu_usage)


def check_memory_usage(memory_usage):
    """
    check memory usage whether higher than 50%
    @Author: Caleb Mai <calebmai@celestica.com>
    :param memory_usage:  memory usage. str without "%"
    """
    if float(memory_usage) >= float(50):
        whitebox_lib.PRINTE("Fail! Memory usage higher than 50 percent. it was[%s]" % memory_usage)


def enter_bios_setup(device, enter_bios_line="Press <DEL> or <ESC> to enter setup", timeout=600):
    """
    Enter bios setup
    :param enter_bios_line: enter bios line
    :param device: product under test
    :param timeout: time out
    """
    bios_gui_lin = r"System Date"
    device_obj.read_until_regexp(enter_bios_line, timeout=timeout)
    bios_menu_lib.send_key(device, "KEY_DEL")
    device_obj.read_until_regexp(bios_gui_lin, timeout=20)
    Logger.info("Pass! Enter bios setup1")


def set_speedstep_from_bios(enter_speedstep_list, setup_step_list, status,
                            reboot=True, connect_os=False, done_flag=None):
    """
    Enter the bios interface and follow the steps to set processor speedstep enable/disable
    @Author: Caleb Mai <calebmai@celestica.com>
    :param enter_speedstep_list: enter speedstep setup interface step list。 List
    :param setup_step_list: set processor speedstep enable/disable step list。 List
    :param status:  Enable or Disable
    :param reboot:True/False
    :param connect_os:True/False
    :param done_flag:Flag to be checked after the step is completed
    """
    current_status = ""
    if reboot:
        device_obj.sendline("reboot")
    enter_bios_setup(deviceType, "Press <F2> or <DEL> to enter setup.")
    boundary_line = '<match all>'
    for step in enter_speedstep_list:
        bios_menu_lib.send_key(deviceType, "KEY_%s" % step.upper())
        time.sleep(2)
    try:
        output = device_obj.receive(boundary_line)
        output = bios_menu_lib.escape_ansi(output)
        current_status = re.findall(r"EIST \(P-states\)\s+\[(.*?)]", output)[0]
    except Exception as E:
        Logger.error(str(E))
    if current_status == status:
        bios_menu_lib.send_key(deviceType, "KEY_ESC")
        line_exit = 'Quit without saving?'
        bios_menu_lib.send_key(deviceType, "KEY_ESC")
        device_obj.read_until_regexp(line_exit, timeout=30)
        bios_menu_lib.send_key(deviceType, "KEY_ENTER")
        Logger.info("rebooting...")
        device_obj.getPrompt(timeout=180)
        whitebox_lib.set_root_hostname(deviceType)
        return
    for step in setup_step_list:
        bios_menu_lib.send_key(deviceType, "KEY_%s" % step.upper())
        time.sleep(2)
    line_exit = 'Save configuration and exit?'
    bios_menu_lib.send_key(deviceType, "KEY_ENTER")
    device_obj.read_until_regexp(line_exit, timeout=30)
    bios_menu_lib.send_key(deviceType, "KEY_ENTER")
    Logger.info("rebooting...")
    device_obj.getPrompt(timeout=180)
    whitebox_lib.set_root_hostname(deviceType)
    if done_flag:
        device_obj.read_until_regexp(done_flag, timeout=30)
    if connect_os:
        return connect()


def run_or_kill_cpuburn(kill=False, log_path=Speedstep_path, background=True, project_name=r"SilverstoneX"):
    """
    Run or kill cpuburn
    @Author: Caleb Mai <calebmai@celestica.com>
    :param project_name: Project tool folder name
    :param log_path: log_path . Str
    :param background: Whether to run in the background
    :param kill: True or False
    :return: Log path/Log name. Str
    """
    flag = " &" if background else ""
    tool_path = get_tool_path(project_name) + "/sit"
    file_name = "cpuburn"
    if kill:
        KillProcess(file_name)
        return
    whitebox_lib.mkdir_data_path(deviceType, log_path)
    set_os_ip_by_dhclient(deviceType)
    whitebox_lib.copy_files_from_pc_to_os(deviceType, pc_user, pc_password, pc_ip, file_name,
                                          tool_path, log_path, 5)
    whitebox_lib.chmod_file(deviceType, log_path + "/" + file_name)
    device_obj.sendline("cd %s" % log_path)
    log_name = "cpuburn_%s.log" % str(datetime.datetime.now()).split(" ")[0]
    cmd = r"./cpuburn > %s/%s%s" % (log_path, log_name, flag)
    device_obj.sendline(cmd)
    time.sleep(20)
    Logger.info("%s running..." % file_name)
    device_obj.sendline("cd /")
    return "%s/%s" % (log_path, log_name)


def get_cpu_cores_frequency():
    """
    get cpu frequency
    @Author: Caleb Mai <calebmai@celestica.com>
    :return: cpu frequency. List
    """
    cmd = r'cat /proc/cpuinfo |grep -i "MHz" |tee  %s/cpu_frequency_%s' \
          % (Speedstep_path, str(datetime.datetime.now()).split(" ")[0])
    res = execute_cmd_without_deal(cmd)
    frequency = re.findall(r"cpu MHz\s+:\s+(\d+\.\d+)", res)
    return frequency


def check_frequency(expect_frequency, actual_frequency, status):
    """
    verify CPU cores’ frequency whether update the maximum value that the CPU spec defined (enable/disable speedstep).
    @Author: Caleb Mai <calebmai@celestica.com>
    :param expect_frequency: expect cpu frequency。List
    :param actual_frequency : cpu cores actual frequency
    :param status: enable or disable speedstep
    """
    error_time = 0
    error_list = list()
    for i in actual_frequency:
        if float(expect_frequency[0]) <= float(i) <= float(expect_frequency[1]):
            pass
        else:
            error_time += 1
            error_list.append("%s" % i)
    if error_time != 0:
        cmd = r"cat %s/cpu_frequency_%s" % (Speedstep_path, str(datetime.datetime.now()).split(" ")[0])
        res = execute_cmd_without_deal(cmd)
        whitebox_lib.PRINTE("Fail! Fail cores quantity:[%s]. Expected %s_expect_frequency:[%s], "
                            "Error frequency:%s. Response:\n %s"
                            % (error_time, status, expect_frequency, error_list, res))


def i2c_read(read_cmd):
    """
    send command "i2cget -y -f X X X" and get the i2c value
    @Author: Caleb Mai <calebmai@celestica.com>
    :param read_cmd: i2c read command . Str
    :return: the i2c value
    """
    value = ""
    res = execute_cmd_without_deal(read_cmd)
    if "Error: Read failed" in res:
        whitebox_lib.PRINTE("Fail! Read i2c fail.Send cmd [%s] ,get the Response:\n%s" % (read_cmd, res))
    result = re.findall(r".*%s\r\n(.*)\r\n\r\nreal.*" % read_cmd, res, re.S)
    if result:
        value = result[0]
    else:
        whitebox_lib.PRINTE("Fail! Can not get the i2c value.Send cmd [%s] ,get the Response:\n%s" % (read_cmd, res))
    return value


def i2c_write(write_cmd):
    """
    send command "i2cset -y -f X X X X" to the i2c value
    @Author: Caleb Mai <calebmai@celestica.com>
    :param write_cmd: i2c set command . Str
    """
    res = execute_cmd_without_deal(write_cmd)
    if "Error: Write failed" in res:
        whitebox_lib.PRINTE("Fail! Write i2c fail.Response:\n%s" % res)
    time.sleep(1)


def check_i2c_read(diag=False, read_and_exp=i2c_read_cmd_and_exp_res):
    """
    Verify i2c can be read correctly
    @Author: Caleb Mai <calebmai@celestica.com>
    :param read_and_exp: read cmd and expect result [dict]
    :param diag: True for test by diag tool false for test by i2cset/i2cget command
    """
    if diag:
        device_obj.sendline("cd %s/bin" % diag_tool_install_path)
        res = execute_cmd(diag_i2c_read_cmd)
        device_obj.sendline("cd /")
        if "Passed" not in res or "FAILED" in res:
            whitebox_lib.PRINTE("Fail! Read i2c fail! Response:\n%s" % res)
        return
    for cmd in read_and_exp:
        value = i2c_read(cmd)
        if read_and_exp[cmd] not in value:
            whitebox_lib.PRINTE("Fail! Read i2c fail, send [%s] expect result:[%s],actual result:[%s]."
                                % (cmd, read_and_exp[cmd], value))
        time.sleep(1)


def check_i2c_write(diag=False, write_cmd=i2c_write_cmd):
    """
    Verify i2c can be write correctly
    @Author: Caleb Mai <calebmai@celestica.com>
    :param write_cmd: write i2c cmd [list]
    :param diag: True for test by diag tool false for test by i2cset/i2cget command
    """
    if diag:
        device_obj.sendline("cd %s/bin" % diag_tool_install_path)
        res = execute_cmd(diag_i2c_write_cmd)
        device_obj.sendline("cd /")
        if "Passed" not in res or "FAILED" in res:
            whitebox_lib.PRINTE("Fail! Read i2c fail! Response:\n%s" % res)
        return
    for cmd in write_cmd:
        expect_value = cmd.split(" ")[-1]
        read_cmd = " ".join(cmd.split(" ")[0:-1]).replace("i2cset", "i2cget")
        original_value = i2c_read(read_cmd)
        i2c_write(cmd)
        new_value = i2c_read(read_cmd)
        if expect_value not in new_value:
            whitebox_lib.PRINTE("Fail! Write i2c fail,send command [%s],want to write:[%s],but actual read:[%s]."
                                % (cmd, expect_value, new_value))
        recovery_cmd = cmd.rstrip(expect_value) + original_value
        i2c_write(recovery_cmd)
        recovery_value = i2c_read(read_cmd)
        if recovery_value not in original_value:
            whitebox_lib.PRINTE("Fail! Recovery i2c fail,send command [%s], want to recovery:[%s],but actual read:[%s]."
                                % (recovery_cmd, original_value, recovery_value))


def i2c_stress(diag=False, hour=i2c_stress_running_time):
    """
    run i2c stress
    @Author: Caleb Mai <calebmai@celestica.com>
    :param hour: the time for run i2c stres
    :param diag: True for test by diag tool false for test by i2cset/i2cget command
    """
    start_time = time.time()
    while time.time() - start_time < 3600 * hour:
        check_i2c_read(diag, i2c_read_cmd_and_exp_res)
        check_i2c_write(diag, i2c_write_cmd)


def set_system_idle(idle_time=system_idle_time):
    """
    Idle the system for a period of time
    @Author: Caleb Mai <calebmai@celestica.com>
    :param idle_time: idle time . Int unit:hours
    """
    idle_start_time = re.findall(r".*date \+%s\r\n(.*)\r\n\r\nreal.*", execute_cmd_without_deal("date +%s"))[0]
    idle_start_time = int(float(idle_start_time))
    start_time = time.time()
    Logger.info("[%s]: System start idle...pls wait %s hours" % (datetime.datetime.now(), idle_time))
    while time.time() - start_time < idle_time * 3600:
        time.sleep(3600 * idle_time + 5)
    idle_stop_time = re.findall(r".*date \+%s\r\n(.*)\r\n\r\nreal.*", execute_cmd_without_deal("date +%s"))[0]
    idle_stop_time = int(float(idle_stop_time))
    if idle_stop_time - idle_start_time < idle_time * 3600:
        whitebox_lib.PRINTE("Fail! System idle at [%s], stop at [%s], system idle expect in total [%s seconds]."
                            "But actual in total [%s seconds]." % (idle_start_time, idle_stop_time, idle_time * 3600,
                                                                   idle_stop_time - idle_start_time))


def detected_ssd(ssd_device_name=LIST__ssd_name):
    """
    Check whether the SSD can be detected in the OS
    @Author: Caleb Mai <calebmai@celestica.com>
    :param ssd_device_name: SSD Device name. List
    """
    error_num = 0
    error_list = list()
    cmd = r"fdisk -l"
    res = execute_cmd(cmd)
    for i in range(len(ssd_device_name)):
        if not re.findall(r"Disk\s+%s" % ssd_device_name[i], res):
            error_num += 1
            error_list.append("%s" % ssd_device_name[i])
    if error_num != 0:
        whitebox_lib.PRINTE("Fail! The SSD %s can not be detected in the OS ,Response:\n%s" % (error_list, res))


def run_fio_from_config(run_fio_ssd_name, fio_config, file_name_id, background=True, project_name=r"SilverstoneX"):
    """
    Run 'fio' for ssd and return dut log path
    @Author: Caleb Mai <calebmai@celestica.com>
    :param project_name: Project tool folder name
    :param file_name_id: file name id . Str
    :param run_fio_ssd_name: run for witch ssd. Str
    :param fio_config: fio config. Str
    :param background:Whether to run in the background
    :return: log path
    """
    running_time = int(float(re.findall(r"--runtime=(\d+)", fio_config)[0]))
    flag = " &" if background else ""
    tool_path = get_tool_path(project_name) + "/sit"
    file_name = "fio"
    whitebox_lib.mkdir_data_path(deviceType, ssd_performance_path)
    set_os_ip_by_dhclient(deviceType)
    whitebox_lib.copy_files_from_pc_to_os(deviceType, pc_user, pc_password, pc_ip, file_name,
                                          tool_path, ssd_performance_path, 5)
    whitebox_lib.chmod_file(deviceType, ssd_performance_path + "/" + file_name)
    device_obj.sendline("cd %s" % ssd_performance_path)
    log_name = "fio_%s_%s_%s.log" % (run_fio_ssd_name.split("/")[-1], file_name_id,
                                     str(time.strftime('%Y-%m-%d_%H:%M:%S', time.localtime(time.time()))))
    cmd = r"fio --filename=%s %s > %s/%s%s" % (run_fio_ssd_name, fio_config, ssd_performance_path, log_name, flag)
    device_obj.sendline("./%s" % cmd)
    time.sleep(3)
    Logger.info("[%s]: %s running...pls wait %s seconds" % (datetime.datetime.now(), file_name, running_time))
    time.sleep(running_time)
    device_obj.sendline("cd /")
    return "%s/%s" % (ssd_performance_path, log_name)


def check_fio_log_from_dut(path, expect):
    """
    check the fio log in dut whether meet expect performance
    @Author: Caleb Mai <calebmai@celestica.com>
    :param path: log path. Str
    :param expect:expect performance. Dict
    """
    cmd = r"cat %s" % path
    res = execute_cmd_without_deal(cmd)
    actual_value = re.findall(r"\w+:\s+IOPS=(.*),\s+BW=.*\((.*)\)\(.*\)", res)
    if not actual_value:
        whitebox_lib.PRINTE("Fail! Can not get the iops and bw value.Response:\n%s" % res)
    actual_iops_value = actual_value[0][0]
    if "k" in actual_iops_value.lower():
        actual_iops_value = actual_iops_value.lower().strip("k")
        actual_iops_value = float(actual_iops_value) * 1000
    elif actual_iops_value[-1].isdigit():
        actual_iops_value = float(actual_iops_value)
    else:
        whitebox_lib.PRINTE("Fail! Get a error iops value [%s]. Response:\n%s" % (actual_value[0][0], res))
    actual_bw_value = actual_value[0][1]
    if "kb/s" in actual_bw_value.lower():
        actual_bw_value = float(actual_bw_value.lower().strip("kb/s")) / 1024
    elif "gb/s" in actual_bw_value.lower():
        actual_bw_value = float(actual_bw_value.lower().strip("gb/s")) * 1024
    elif "mb/s" in actual_bw_value.lower():
        actual_bw_value = float(actual_bw_value.lower().strip("mb/s"))
    else:
        whitebox_lib.PRINTE("Fail! Get a bw value with a error unit [%s]. Response:\n%s" % (actual_value[0][1], res))
    expect_iops = float(expect["min_IOPS"])
    expect_bw = float(expect["min_bw"])
    if actual_bw_value < expect_bw != 0:
        whitebox_lib.PRINTE("Fail! actual bw value is [%s],expect [%s].Response:\n%s"
                            % (actual_value[0][1], expect_bw, res))
    elif actual_iops_value < expect_iops != 0:
        whitebox_lib.PRINTE("Fail! actual iops value is [%s],expect [%s].Response:\n%s"
                            % (actual_value[0][0], expect_iops, res))


def format_ssd(ssd_device_name):
    """
    format the ssd which will be test performance
    @Author: Caleb Mai <calebmai@celestica.com>
    :param ssd_device_name: ssd decice name . Str
    """
    device_obj.sendline(r"umount %s" % ssd_device_name)
    cmd = r"sudo echo y| mkfs -t ext4  %s" % ssd_device_name
    res = execute_cmd(cmd)
    success_line = r"Writing superblocks and filesystem accounting information.*done"
    if not re.findall("%s" % success_line, res):
        whitebox_lib.PRINTE("Fail! Can not format the ssd.Response:\n%s" % res)


def get_usb_speed_from_hdparm(device_name):
    """
    get the usb speed from hdparm
    @Author: Caleb Mai <calebmai@celestica.com>
    :param device_name: usb device name
    :return: usb speed. float
    """
    float_speed = float(0)
    cmd = r"hdparm -t %s" % device_name
    res = execute_cmd_without_deal(cmd)
    actual_speed = re.findall(r"seconds\s+=\s+(.*)\s+MB/sec", res)
    if actual_speed:
        float_speed = float(actual_speed[0])
    else:
        whitebox_lib.PRINTE("Fail! Can not get the usb speed from hdparm. Response:\n%s" % res)
    return float_speed


def check_usb_performance(actual_speed, expect_speed, num=0):
    """
    check usb performance whether meet expect
    @Author: Caleb Mai <calebmai@celestica.com>
    :param actual_speed: usb actual speed
    :param expect_speed: usb expect speed
    :param num: time
    """
    expect_speed = float(expect_speed)
    if actual_speed < expect_speed:
        whitebox_lib.PRINTE("Fail! The [%s]times usb actual speed [%s], expect speed [%s]."
                            % (num, actual_speed, expect_speed))


def touch_object_on_usb(device_name):
    """
    @Author: Caleb Mai <calebmai@celestica.com>
    verify can use Command "touch" to write a object in device and read it
    :param device_name: usb drive name. Str
    """
    cmd_df = r"df -h"
    if not re.findall(r"Disk\s+%s" % device_name, execute_cmd_without_deal("fdisk -l")):
        whitebox_lib.PRINTE("Fail! No such drive: %s" % device_name)
    if not re.findall(r"%s.*(/.*)\r" % device_name, execute_cmd_without_deal(cmd_df)):
        execute_cmd_without_deal("mount %s /mnt" % device_name)
    mount = re.findall(r"%s.*(/.*)\r" % device_name, execute_cmd_without_deal(cmd_df))[0]
    ls = r"ls %s" % mount
    if re.findall(r"test100.txt", execute_cmd_without_deal(ls)):
        execute_cmd_without_deal("rm -rf %s/test100.txt" % mount)
    cmd_touch = r"touch %s/test100.txt" % mount
    device_obj.sendline(cmd_touch)
    time.sleep(1)
    read_touch = execute_cmd_without_deal(ls)
    if not re.findall(r"test100.txt", read_touch):
        whitebox_lib.PRINTE("Fail! Couldn't read the object which write by command 'touch' at [%s]"
                            % device_name)
    device_obj.sendline("rm -rf %s/test100.txt" % mount)
    device_obj.sendline("umount %s" % device_name)


def psu_redundant_test():
    """
    Sit psu redundant test case dedicated
    @Author: Caleb Mai <calebmai@celestica.com>
    """
    Logger.info("#################################################################################################")
    Logger.info("pls remove one of the psu power cable,then input y\n"
                "Have been removed?(Y/N):")
    while True:
        remove_confirm = input()
        if remove_confirm.lower() == "y":
            break
        else:
            Logger.info("What you input is not 'y',pls confirm remove one psu then input 'y'!\n"
                        "Have been removed?(Y/N):")
    Logger.info("[%s]: full loading,pls wait 12 hours" % datetime.datetime.now())


def recovery_psu():
    """
    Sit psu redundant test case dedicated
    @Author: Caleb Mai <calebmai@celestica.com>
    """
    Logger.info("#################################################################################################")
    Logger.info("pls re_insert the psu power cable,then input y\n"
                "Have been insert?(Y/N):")
    while True:
        re_insert_confirm = input()
        if re_insert_confirm.lower() == "y":
            break
        else:
            Logger.info("What you input is not 'y',pls confirm re_insert the psu then input 'y'!\n"
                        "Have been insert?(Y/N):")


def run_stressapptest_and_return_log_path(run_time=runing_time, background=True, project_name=r"SilverstoneX"):
    """
    Run or kill 'stressapptest'
    @Author: Caleb Mai <calebmai@celestica.com>
    :param project_name: Project tool folder name
    :param run_time: Running time .unit:hour
    :param background:Whether to run in the background
    """
    log_path = r"/home/white_box/stressapptest"
    flag = " &" if background else ""
    run_time = run_time * 60 * 60
    tool_path = get_tool_path(project_name) + "/sit"
    file_name = "stressapptest"
    KillProcess(file_name)
    whitebox_lib.mkdir_data_path(deviceType, log_path)
    whitebox_lib.copy_files_from_pc_to_os(deviceType, pc_user, pc_password, pc_ip, file_name,
                                          tool_path, log_path, 5)
    whitebox_lib.chmod_file(deviceType, log_path + "/" + file_name)
    device_obj.sendline("cd %s" % log_path)
    log_name = "stressapptest_%s.log" % str(datetime.datetime.now()).split(" ")[0]
    size = GetMemoryFree() * 0.9
    cmd = "%s -M %s -s %s > %s/%s%s" % (file_name, size, run_time, log_path, log_name, flag)
    device_obj.sendline("./%s" % cmd)
    time.sleep(20)
    Logger.info("%s running..." % file_name)
    device_obj.sendline("cd /")
    return "%s/%s" % (log_path, log_name)


def check_stressapptest_over(path, pass_keyword=stressapptest_pass_keyword):
    """
    check stressapptest whether over
    @Author: Caleb Mai <calebmai@celestica.com>
    :param path:log absolute path and log name. Str
    :param pass_keyword:stressapptest end sign
    :return:
    """
    log_name = path.split("/")[-1]
    cmd = r"cat %s" % path
    res = execute_cmd_without_deal(cmd)
    if pass_keyword not in res:
        whitebox_lib.PRINTE("Fail! Couldn't find keyword:[%s] in %s" % (pass_keyword, log_name))


def run_fio_for_all_disk(run_time, system_disk="/dev/sda", project_name=r"SilverstoneX"):
    """
    run fio for all disks except the system disk
    @Author: Caleb Mai <calebmai@celestica.com>
    :param project_name: Project tool folder name
    :param system_disk: system_disk
    :param run_time: fio running time .Str
    :return:all log path. List
    """
    path = r"/home/white_box/fio"
    log_path = list()
    run_time = float(run_time)
    file_name = "fio"
    KillProcess(file_name)
    tool_path = get_tool_path(project_name) + "/sit"
    whitebox_lib.mkdir_data_path(deviceType, path)
    whitebox_lib.copy_files_from_pc_to_os(deviceType, pc_user, pc_password, pc_ip, file_name,
                                          tool_path, path, 5)
    whitebox_lib.chmod_file(deviceType, path + "/" + file_name)
    device_obj.sendline("cd %s" % path)
    res = execute_cmd_without_deal("fdisk -l")
    disk_list = re.findall(r"Disk (/dev/sd.*):\s+", res)
    if system_disk in disk_list:
        disk_list.remove(system_disk)
    for i in disk_list:
        log_name = "%s_fio_%s.log" % (i.split("/")[-1],
                                      str(time.strftime('%Y-%m-%d_%H:%M:%S', time.localtime(time.time()))))
        cmd = r"fio --name=seq_read --filename=%s --direct=1 --thread=1 --numjobs=1 --iodepth=32 --rw=randread " \
              r"--bs=128k --runtime=%s --time_based=1 --group_reporting --log_avg_msec=1000 --bwavgtime=100 " \
              r"--write_bw_log=seq_read --size=100%s > %s/%s &" % (i, run_time, "%", path, log_name)
        device_obj.sendline("./%s" % cmd)
        time.sleep(5)
        Logger.info("%s running..." % file_name)
        log_path.append("%s/%s" % (path, log_name))
    device_obj.sendline("cd /")
    return log_path


def check_all_fio_run_success(*path, success_sign="Disk stats (read/write):"):
    """
    check all fio run success
    @Author: Caleb Mai <calebmai@celestica.com>
    :param path: fio log path
    :param success_sign: success_sign
    """
    if not path:
        whitebox_lib.PRINTE("Fail! Can not find fio log path!")
    for i in path:
        log_name = i.split("/")[-1]
        cmd = r"cat %s" % i
        res = execute_cmd_without_deal(cmd)
        if not res or success_sign not in res:
            whitebox_lib.PRINTE("Fail! Couldn't find keyword:[%s] in %s" % (success_sign, log_name))


def run_or_kill_memtester_and_return_path(background=True, kill=False, project_name=r"SilverstoneX"):
    """
    Run 'memtester' or kill it and return the log path
    @Author: Caleb Mai <calebmai@celestica.com>
    :param project_name: Project tool folder name
    :param background: Whether to run in the background
    :param kill: True/False
    """
    log_path = r"/home/white_box/memtester"
    file_name = "memtester"
    KillProcess(file_name)
    flag = " &" if background else ""
    tool_path = get_tool_path(project_name) + "/sit"
    if kill:
        KillProcess(file_name)
        return
    whitebox_lib.mkdir_data_path(deviceType, log_path)
    whitebox_lib.copy_files_from_pc_to_os(deviceType, pc_user, pc_password, pc_ip, file_name,
                                          tool_path, log_path, 5)
    whitebox_lib.chmod_file(deviceType, log_path + "/" + file_name)
    device_obj.sendline("cd %s" % log_path)
    log_name = "memtester_%s.log" % str(datetime.datetime.now()).split(" ")[0]
    size = int(GetMemoryFree() * 0.9)
    cmd = "%s %sM > %s/%s %s" % (file_name, size, log_path, log_name, flag)
    Logger.info(cmd)
    device_obj.sendline("./%s" % cmd)
    time.sleep(5)
    Logger.info("%s running..." % file_name)
    device_obj.sendline("cd /")
    return "%s/%s" % (log_path, log_name)


def check_memtester_success(path):
    """
    check memtester run success
    @Author: Caleb Mai <calebmai@celestica.com>
    :param path: memtester log .Str
    """
    filepath = path.rstrip(path.split("/")[-1]).rstrip("/")
    filename = path.split("/")[-1]
    Device.execute_local_cmd(device_obj, "mkdir -p %s" % pc_log_path, timeout=10)
    whitebox_lib.copy_files_from_pc_to_os(deviceType, pc_user, pc_password, pc_ip, filename, filepath,
                                          pc_log_path, 15, True)
    with open(r"%s/%s" % (pc_log_path, filename), "r", encoding="UTF-8") as f:
        all_info = f.read()
        loop_count = all_info.count("Loop")
        if loop_count:
            ok_num = 18 * (loop_count - 1)
            actual_ok = all_info.count("ok")
        else:
            whitebox_lib.PRINTE("Fail! 'memtester' abnormal operation")

    with open(r"%s/%s" % (pc_log_path, filename), "r", encoding="UTF-8") as ff:
        line_list = ff.readlines()
        ok_count = 0
        flag = False
        for line in line_list:
            if flag:
                if "ok" in line:
                    ok_count += 1
            else:
                if "Loop %s" % loop_count in line:
                    flag = True
    if (ok_num + ok_count) != actual_ok:
        whitebox_lib.PRINTE("Fail! '%s/%s' got Loop:[%s], 'ok'[%s]" % (pc_log_path, filename, loop_count, actual_ok))


def check_cpuburn_log(path):
    """
    check cpuburn run success
    @Author: Caleb Mai <calebmai@celestica.com>
    :param path: couburn log .Str
    """
    cmd = r"cat %s" % path
    res = execute_cmd_without_deal(cmd)
    if not re.findall(r"Burning \d+ CPUs/cores", res):
        whitebox_lib.PRINTE("Fail! cpuburn run fail! Response:\n%s" % res)


def is_float(num):
    num_list = str(num).split(".")
    if len(num_list) > 2:
        return False
    for i in num_list:
        if not i.isdigit():
            return False
    return True


def record_power_consumption():
    Logger.info("#################################################################################################")
    Logger.info("pls input the consumption from dynamometer now:\n")
    while True:
        consumption = input()
        if is_float(consumption):
            break
        else:
            Logger.info("What you input is not a number! pls input again")
            Logger.info(
                "#################################################################################################")
            Logger.info("pls input the consumption:\n")
    return consumption


def get_consumption_from_ipmitool():
    """
    send command 'ipmitool sensor list' to get PSU_PIn consumption
    @Author: Caleb Mai <calebmai@celestica.com>
    :return:psu total consumption. float
    """
    total_consumption = 0
    cmd = r"ipmitool sensor list | grep -i PSU |grep -i PIn"
    res = execute_cmd_c(cmd, timeout=300)
    for i in res.splitlines():
        if i.count("|") == 9:
            total_consumption += float(i.split("|")[1].strip())
    return total_consumption


def run_traffic():
    pass


def check_consumption(ipmitool_full, ipmitool_idle, meter_full, meter_idle, expect=expect_consumption):
    ipmitool_full = float(ipmitool_full)
    ipmitool_idle = float(ipmitool_idle)
    meter_full = float(meter_full)
    meter_idle = float(meter_idle)
    if not expect["idle_mode"][0] < ipmitool_idle < expect["idle_mode"][1]:
        whitebox_lib.PRINTE("Fail! idle mode expect consumption %s, but ipmitool get actual consumption [%s]" %
                            (expect["idle_mode"], ipmitool_idle))
    elif not expect["idle_mode"][0] < meter_idle < expect["idle_mode"][1]:
        whitebox_lib.PRINTE("Fail! idle mode expect consumption %s, but power meter get actual consumption [%s]" %
                            (expect["idle_mode"], meter_idle))
    elif not expect["full_loading"][0] < ipmitool_full < expect["full_loading"][1]:
        whitebox_lib.PRINTE("Fail! full_loading mode expect consumption %s, but ipmitool get actual consumption [%s]"
                            % (expect["full_loading"], meter_idle))
    elif not expect["full_loading"][0] < meter_full < expect["full_loading"][1]:
        whitebox_lib.PRINTE("Fail! full_loading mode expect consumption %s, but power meter get actual consumption [%s]"
                            % (expect["full_loading"], meter_idle))


def copy_folder_through_scp(device, username, password, server_ip, filelist: list, filepath, destination_path,
                            mode='None', swap=False, ipv6=False, interface='None', timeout=Const.COPYING_TIME, retry=2):
    Logger.debug("Entering copy_files_through_scp with args : %s" % (str(locals())))
    errCount = 0
    if mode != 'None':
        device_obj.getPrompt(mode)
    for fileName in filelist:
        if fileName == '':
            continue
        success = False
        for retryCount in range(retry):
            Logger.debug("retryCount: %d" % (retryCount))
            device_obj.flush()
            try:
                if swap:
                    if ipv6:
                        cmd = 'scp -r %s/%s %s@[%s' % (filepath, fileName, username, server_ip)
                        if server_ip.startswith('2001'):
                            cmd += ']:' + destination_path
                        else:
                            cmd += '%' + interface + ']:' + destination_path
                        Logger.cprint(cmd)
                        device_obj.sendCmd(cmd)
                    else:
                        device_obj.sendCmd(
                            "scp -r %s/%s %s@%s://%s" % (filepath, fileName, username, server_ip, destination_path))
                else:
                    if ipv6:
                        if not server_ip.startswith('2001'):
                            cmd = 'scp -r -6 %s@[%s' % (username, server_ip)
                            cmd += ('%' + interface + ']:' + filepath + '/' + fileName)
                            cmd += (' ' + destination_path + '/')
                        else:
                            cmd = 'scp -r -6 %s@[%s' % (username, server_ip)
                            cmd += (']:' + filepath + '/' + fileName)
                            cmd += (' ' + destination_path + '/')
                        Logger.cprint(cmd)
                        device_obj.sendCmd(cmd)
                    else:
                        device_obj.sendCmd(
                            "scp -r %s@%s://%s/%s %s" % (username, server_ip, filepath, fileName, destination_path))
                promptList = ["(y/n)", "(yes/no)", "password:"]
                patternList = re.compile('|'.join(promptList))
                output1 = device_obj.read_until_regexp(patternList, 180)
                Logger.info('output1: ' + str(output1))

                if re.search("(yes/no)", output1):
                    device_obj.transmit("yes")
                    device_obj.receive("password:")
                    device_obj.transmit("%s" % password)
                elif re.search("(y/n)", output1):
                    device_obj.transmit("y")
                    device_obj.receive("password:")
                    device_obj.transmit("%s" % password)
                elif re.search("password:", output1):
                    device_obj.transmit("%s" % password)
                else:
                    Logger.fail("pattern mismatch")

                currentPromptStr = device_obj.getCurrentPromptStr()
                currentPromptStr = currentPromptStr if currentPromptStr else "100%|No such file"
                output = device_obj.read_until_regexp(currentPromptStr, timeout=timeout)
                p0 = ".*100\%"
                p1 = "No such file or directory"
                if re.search(p0, output):
                    Logger.info("Successfully copy file: %s" % fileName)
                    success = True
                    break  # continue to copy next file
                elif re.search(p1, output):
                    Logger.error("%s" % p1)
                    raise RuntimeError(p1 + ': ' + fileName)
            except:
                if ipv6:
                    device_obj.executeCmd('ssh-keygen -R ' + server_ip + '%' + interface)
                else:
                    CommonLib.execute_local_cmd('ssh-keygen -R ' + server_ip)
                continue  # come to next try

        if not success:
            raise RuntimeError("Copy file {} through scp failed!".format(fileName))
    return 0


def copy_folder_from_pc_to_os(device, username, password, server_ip, filename, filepath, destination_path, size_MB,
                              swap=False, ipv6=False, interface='None'):
    """
    if swap=True, function：copy file from dut to pc
    """
    Logger.debug('Entering procedure copy_files_from_pc_to_os : %s\n' % (str(locals())))
    ### assume avg speed is 0.5MB/s
    timeout = int(size_MB) * 3
    filelist = [filename]
    copy_folder_through_scp(device, username, password, server_ip, filelist,
                            filepath, destination_path, CENTOS_MODE, swap, False, interface, timeout)


def install_diag_tool(name=deb_diag_name, install_path=diag_tool_install_path, project_name=r"SilverstoneX"):
    """
    install diag tool at dut
    @Author: Caleb Mai <calebmai@celestica.com>
    :param install_path: diag tool install path
    :param project_name: Project tool folder name
    :param name: diag tool name. Str (.deb file)
    """
    dut_diag_path = r"/home/white_box"
    file_name = name
    tool_path = get_tool_path(project_name)
    whitebox_lib.mkdir_data_path(deviceType, dut_diag_path)
    whitebox_lib.copy_files_from_pc_to_os(deviceType, pc_user, pc_password, pc_ip,
                                          file_name, tool_path, dut_diag_path, 500)
    execute_cmd("cd %s" % dut_diag_path)
    execute_cmd("chmod 777 *")
    execute_cmd("dpkg -i %s" % name)
    execute_cmd("cd %s" % install_path)
    execute_cmd("chmod 777 *")
    execute_cmd("cd ../")
    execute_cmd("chmod 777 *")
    execute_cmd("./diag.sh")
    device_obj.sendline("cd /")


def check_port_optical_module_eeprom_information(command=diag_check_eeprom_cmd, present_keywork=present_status):
    """
    check port optical module eeporm information
    @Author: Caleb Mai <calebmai@celestica.com>
    :param present_keywork: optical module status present key work
    :param command: command for get port optical module eeporm information
    :return: log_path + log_name. Str
    """
    log_path = r"/home/white_box/optical_module"
    whitebox_lib.mkdir_data_path(deviceType, log_path)
    log_name = "eeprom_information_%s.log" % str(time.strftime('%Y-%m-%d_%H:%M:%S', time.localtime(time.time())))
    device_obj.sendline("cd %s/bin" % diag_tool_install_path)
    execute_cmd("%s > %s/%s" % (command, log_path, log_name))
    device_obj.sendline("cd /")
    check_log_cmd = r"cat %s/%s" % (log_path, log_name)
    check = execute_cmd(check_log_cmd)
    if check.count(present_keywork) != qsfp_present_num + sfp_present_num:
        whitebox_lib.PRINTE("Fail! Port are not all present. Response:\n%s" % check)
    for i in check.splitlines():
        if i.lower().startswith("qsfp"):
            if qsfp_vendor_name not in i or qsfp_part_number not in i:
                whitebox_lib.PRINTE("Fail! QSFP Port eeporm information Error. Response:\n%s" % check)
        elif i.lower().startswith("sfp"):
            if sfp_vendor_name not in i or sfp_part_number not in i:
                whitebox_lib.PRINTE("Fail! SFP Port eeporm information Error. Response:\n%s" % check)
    return "%s/%s" % (log_path, log_name)


def check_file_equal(file_1, file_2, decide=True):
    """
    Check whether the two files are equal
    @Author: Caleb Mai <calebmai@celestica.com>
    :param file_1: file_path + file_name . Str
    :param file_2: file_path + file_name . Str
    :param decide: True for equal, False for diff
    """
    res = execute_cmd_without_deal("diff %s %s" % (file_1, file_2))
    if decide:
        if ">" in res or "<" in res:
            if "---" in res:
                file_1_ = execute_cmd_without_deal("cat %s" % file_1)
                file_2_ = execute_cmd_without_deal("cat %s" % file_2)
                whitebox_lib.PRINTE("Fail! [%s] is diff from [%s]. Response:\n%s\nFile_1:\n%s\nFile_2:\n%s\n"
                                    % (file_1, file_2, res, file_1_, file_2_))
    else:
        if (">" not in res or "<" not in res) and "---" not in res:
            file_1_ = execute_cmd_without_deal("cat %s" % file_1)
            file_2_ = execute_cmd_without_deal("cat %s" % file_2)
            whitebox_lib.PRINTE("Fail! [%s] is same to [%s].\nFile_1:\n%s\nFile_2:\n%s\n"
                                % (file_1, file_2, file_1_, file_2_))


def init_stty():
    """
    Initialize the serial port window size
    @Author: Caleb Mai <calebmai@celestica.com>
    """
    device_obj.sendline("stty rows 300")
    device_obj.sendline("stty cols 300")


def init_optical_module_hot_plug():
    """
    SIT optical module Hot Plug check(10 cycles) case dedicated
    @Author: Caleb Mai <calebmai@celestica.com>
    """
    Logger.info("#################################################################################################")
    Logger.info("############### Pls input optical module , then start test ##################################")
    Logger.info("#################################################################################################")
    Logger.info("Input How much port you want to test:\n")
    while True:
        port_num = input()
        if port_num.isdigit():
            break
        else:
            Logger.info("What you input is not a number! Pls input again:\n")
    return port_num


def optical_module_hot_plug(port, cycle, fast=True, name="Optical_module", num=1):
    """
    SIT optical module Hot Plug check(10 cycles) case dedicated
    @Author: Caleb Mai <calebmai@celestica.com>
    :param name: hot_plug_name
    :param port: test port num
    :param cycle: port test cycle num
    :param fast: True for fast hot plug, False for slow hot plug
    """
    port = int(float(port) + 1)
    cycle = int(float(cycle) + 1)
    if fast:
        Logger.info("################################################################################################")
        Logger.info("################## Fast Hot plug--remove and insert--Port:%s Cycle:%s ############################"
                    % (port, cycle))
        Logger.info("################################################################################################")
        Logger.info("Pls Remove %s and plug it back quickly(within one second),Then input 'y':\n" % name)
        while True:
            confirm = input()
            if confirm.lower() == "y":
                break
            else:
                Logger.info("What you input is not 'y'")
                Logger.info("Pls Remove %s and plug it back quickly(within one second),Then input 'y':\n" % name)
        check_ps_fio()
        check_info()
        check_optical_module_hot_plug(keywork_cnt=num)
        return
    Logger.info("#################################################################################################")
    Logger.info("###################### Slow Hot plug--remove--Port:%s Cycle:%s ####################################"
                % (port, cycle))
    Logger.info("#################################################################################################")
    Logger.info("Pls Remove %s,Then input 'y' and wait 1 min :\n" % name)
    while True:
        confirm = input()
        if confirm.lower() == "y":
            break
        else:
            Logger.info("What you input is not 'y'")
            Logger.info("Pls Remove %s,Then input 'y' and wait 1 min :\n" % name)
    check_ps_fio()
    check_info()
    Logger.info("Pls wait 1 min")
    time.sleep(60)
    Logger.info("#################################################################################################")
    Logger.info("###################### Slow Hot plug--insert--Port:%s Cycle:%s ####################################"
                % (port, cycle))
    Logger.info("#################################################################################################")
    Logger.info("Now Pls plug the %s back,Then input 'y'\n" % name)
    while True:
        input_confirm = input()
        if input_confirm.lower() == "y":
            break
        else:
            Logger.info("What you input is not 'y'")
            Logger.info("Now Pls plug the %s back,Then input 'y'\n" % name)
    check_ps_fio()
    check_info()
    check_optical_module_hot_plug(keywork_cnt=num)


def check_optical_module_hot_plug(command="./cel-qsfp-test --all", present_keywork="present", keywork_cnt=1):
    device_obj.sendline("cd %s/bin" % diag_tool_install_path)
    res = execute_cmd(command)
    if res.count(present_keywork) != keywork_cnt:
        whitebox_lib.PRINTE("Fail! Port are not present. Response:\n%s" % res)


def check_information():
    CheckDmesgInfo()
    CheckCMDResponse("ipmitool sel list", sel_error_list, False, False, False, True)
    CheckCMDResponse("cat /var/log/messages", messages_error_list, False, False, False, True)
    CheckFullyBMCVersion()
    CheckSensorList()
    CheckSdrInfo()
    CheckFruListInfo()
    CheckBMCIP()
    CheckLspciAllInfo()
    CheckLnKCapLnkSta()
    CheckBIOSVersion()
    CheckOSIp()
    CheckEthtoolSpeedLinkStatus()
    CheckMemtotalSize()
    CheckDmiMemoryInfo()
    CheckCpuInfo()
    CheckLsCpu()
    CheckLsBlk()
    CheckSmartctlInfo()


def get_nic_name_and_ip():
    """
    use command 'ifconfig' to get NIC name witch have correct ip
    @Author: Caleb Mai <calebmai@celestica.com>
    :return: nic name and ip . Dict
    """
    cmd = r"ifconfig"
    res = execute_cmd(cmd)
    nic_dict = dict()
    error_list = ["0.0.0.0", "127.0.0.1"]
    error_name = ["lo", "docker0", "virbr0"]
    nic_list = res.split("\r\n\r\n")
    for nic in nic_list:
        ip = re.findall(r"inet\s+(\d+\.\d+\.\d+\.\d+)", nic)
        if ip:
            nic_name = nic.split(":")[0].strip("\n")
            if ip[0] not in error_list and nic_name not in error_name and \
                    ip[0].rstrip(ip[0].split(".")[-1]) == pc_ip.rstrip(pc_ip.split(".")[-1]):
                nic_dict.update({"%s" % nic_name: "%s" % ip[0]})
    if len(nic_dict) == 0:
        whitebox_lib.PRINTE("Fail! Can not get the nic name and ip")
    return nic_dict


def set_lan_speed_auto_negotiation(nic_name, mode=None, auto_negotiation=False):
    """
    Set lan Speed and duplex and auto negotiation by command 'ethtool'
    @Author: Caleb Mai <calebmai@celestica.com>
    :param auto_negotiation: True for set autoneg on
    :param mode: link mode . List ["speed", "duplex"]
    :param nic_name: nic name
    """
    cmd = r"ethtool -s %s autoneg on" % nic_name if auto_negotiation else \
        r"ethtool -s %s speed %s duplex %s autoneg off" % (nic_name, mode[0], mode[1])
    res = execute_cmd(cmd)
    if "not setting" in res:
        whitebox_lib.PRINTE("Fail! can not set lan speed! Response:\n%s" % res)


def check_nic_work_status():
    """
    Check NIC work status with ping command
    @Author: Caleb Mai <calebmai@celestica.com>
    """
    cmd = r"ping %s -c 20" % pc_ip
    res = execute_cmd(cmd)
    if "0% packet loss" not in res:
        whitebox_lib.PRINTE("Fail! NIC can not work normally. Response:\n%s" % res)


def get_nic_speed_and_duplex_state(nic_name):
    """
    send command 'ethtool X(nic_name)' to get nic speed and duplex state
    @Author: Caleb Mai <calebmai@celestica.com>
    :param nic_name: nic name . Str
    :return: speed and duplex . List
    """
    cmd = r"ethtool %s" % nic_name
    res = execute_cmd(cmd)
    speed = re.findall(r"Speed: (\d+)Mb/s", res)
    duplex = re.findall(r"Duplex: (\w+)", res)
    if speed and duplex:
        return [speed[0], duplex[0].lower()]
    else:
        whitebox_lib.PRINTE("Fail! Can not get nic speed and duplex state. Response:\n%s" % res)


def check_nic_speed_and_duplex_state(actual_state, expect_state):
    """
    check nic speed and duplex whether meet expect
    @Author: Caleb Mai <calebmai@celestica.com>
    :param actual_state: actual state . List
    :param expect_state: expect state . List
    """
    if actual_state != expect_state:
        whitebox_lib.PRINTE("Fail! expect state [%s], but actually state [%s]" % (expect_state, actual_state))


def check_nic_speed_auto_negotiation(nic_name):
    """
    check nic speed auto negotiation setup
    @Author: Caleb Mai <calebmai@celestica.com>
    :param nic_name: nic name . Str
    """
    cmd = r"ethtool %s" % nic_name
    res = execute_cmd(cmd)
    if "Auto-negotiation: on" not in res:
        whitebox_lib.PRINTE("Fail! Set lan speed auto negotiation Fail. Response:\n%s" % res)


def get_supported_link_modes(nic_name):
    """
    get nic support link modes form command 'ethtool'
    @Author: Caleb Mai <calebmai@celestica.com>
    :return: support modes . List
    """
    cmd = r"ethtool %s" % nic_name
    res = execute_cmd(cmd)
    supported_modes = list()
    supported_link_modes = re.findall(r"Supported link modes:(.*)Supported pause frame use", res, re.S)[0]
    modes = re.findall(r"(\d+\w+/\w+)", supported_link_modes)
    for i in modes:
        i = i.lower()
        mode = i.split("baset/")
        supported_modes.append(mode)
    if len(supported_modes) == 0:
        whitebox_lib.PRINTE("Fail! Can not get supported link modes. Response:\n%s" % res)
    return supported_modes


def enter_sdk_c(options="-m PAM4_400G_32", project_name="SilverstoneX", remote=False,
                login_keywords="Enter daemon mode", file_name=sdk_filename):
    """
    enter sdk (for SilverstoneX)
    @Author: Caleb Mai <calebmai@celestica.com>
    :param options: enter sdk options ["-m portMode"]
    :param project_name: Project tool folder name
    :param remote:True for Run the SDK under remote shell
    :param login_keywords: Keywords for successfully entering sdk
    :param file_name:sdk file name (.zip)
    """
    KillProcess("innovium.user")
    sdk_install_path = r"/home/sdk"
    whitebox_lib.mkdir_data_path(deviceType, sdk_install_path)
    tool_path = get_tool_path(project_name)
    whitebox_lib.copy_files_from_pc_to_os(deviceType, pc_user, pc_password, pc_ip, file_name,
                                          tool_path, sdk_install_path, 500)
    execute_cmd("rm -rf %s/%s" % (sdk_install_path, file_name.rstrip(".zip")))
    execute_cmd("unzip -o %s/%s -d %s" % (sdk_install_path, file_name, sdk_install_path))
    device_obj.sendline("cd %s/%s" % (sdk_install_path, file_name.rstrip(".zip")))
    device_obj.sendline("cd /home/R3240-J0025-01_V2.0.2_SilverstoneX_SDK")
    execute_cmd("chmod 777 *")
    if remote:
        device_obj.sendline("./auto_load_user.sh %s -d" % options)
        device_obj.read_until_regexp(login_keywords, timeout=30)
        return
    device_obj.sendline("./auto_load_user.sh %s" % options)
    device_obj.read_until_regexp("IVM:0>", timeout=30)


def exit_sdk_c(remote=False):
    """
    exit sdk
    @Author: Caleb Mai <calebmai@celestica.com>
    :param remote:whether remote
    """
    if remote:
        execute_cmd("./%s exit" % cls_name)
    else:
        execute_sdk_cmd("exit")


def check_port_link_up(port_num_list):
    """
    check port whether link up
    @Author: Caleb Mai <calebmai@celestica.com>
    :param port_num_list: check port num list .List
    """
    time.sleep(5)
    for i in port_num_list:
        execute_sdk_cmd("port enable %s" % i, 0)
    port_info = execute_sdk_cmd("port info")
    port_info_line = port_info.splitlines()
    error_port = list()
    for i in port_info_line:
        if len(i.split("|")) > 12 and i.split("|")[1].strip() in port_num_list \
                and i.split("|")[11].strip() != "LINK_UP":
            error_port.append("%s" % i.split("|")[1].strip())
    if error_port:
        whitebox_lib.PRINTE("Fail! Port %s are not link up. Response:\n%s" % (error_port, port_info))


def execute_sdk_cmd(cmd, response_time=5):
    """
    Send command and get the response under bcm cli (for SilverstoneX)
    @Author: Caleb Mai <calebmai@celestica.com>
    :param cmd: command
    :param response_time:get response time
    :return: response
    """
    device_obj.flush()
    device_obj.readMsg()
    device_obj.sendline("%s\n" % cmd)
    time.sleep(response_time)
    result = device_obj.readMsg()
    res = re.findall(r"IVM:0>%s(.*?)\n+IVM:0>" % cmd, result, re.S)
    if res:
        return res[0]
    return ""


def config_snake(config="-p '129,130' -lb 'NONE' -v -b2"):
    """
    config snake before traffic
    @Author: Caleb Mai <calebmai@celestica.com>
    :param config: snake config
    """
    cmd = "diagtest snake config %s" % config
    res = execute_sdk_cmd(cmd)
    if "ERR:" in res or "failed" in res:
        whitebox_lib.PRINTE("Fail! config snake fail. Response:\n%s" % res)


def check_rate(min_rate, max_rate, cmd=r"ifcs show rate devport filter nz"):
    """
    check port rate
    @Author: Caleb Mai <calebmai@celestica.com>
    :param min_rate: exp min rate
    :param max_rate: exp max rate
    :param cmd: command for check rate
    """
    res = execute_sdk_cmd(cmd)
    res_list = res.splitlines()
    cnt = 0
    for i in range(len(res_list)):
        if res_list[i].count("|") == 8 and is_float(res_list[i].split("|")[3].strip()):
            cnt += 1
            if res_list[i].split("|")[4].strip() != "0.00":
                whitebox_lib.PRINTE("Fail! Input Err/sec not equal to '0.00'")
            if res_list[i].split("|")[7].strip() != "0.00":
                whitebox_lib.PRINTE("Fail! Output Err/sec not equal to '0.00'")
            if not float(min_rate) < float(res_list[i].split("|")[3].strip()) < float(max_rate) or \
                    not float(min_rate) < float(res_list[i].split("|")[6].strip()) < float(max_rate):
                whitebox_lib.PRINTE("Fail! Port rate can not meet expect. Response:\n%s" % res)
    if cnt == 0:
        whitebox_lib.PRINTE("Fail! Can not get Rate. Response:\n%s" % res)


def check_counters(cmd=r"ifcs show counters devport filter nz"):
    res = execute_sdk_cmd(cmd)
    rx_frames_err = list()
    tx_frames_err = list()
    res_lines = res.splitlines()
    cnt = 0
    for i in res_lines:
        if i.count("|") == 12 and i.split("|")[1].strip().isdigit():
            cnt += 1
            if i.split("|")[4].strip() != "0":
                rx_frames_err.append(i.split("|")[4].strip())
            if i.split("|")[9].strip() != "0":
                tx_frames_err.append(i.split("|")[9].strip())
    if rx_frames_err or tx_frames_err:
        whitebox_lib.PRINTE("Fail! rx_frames_err:%s, tx_frames_err:%s, Response:\n%s"
                            % (rx_frames_err, tx_frames_err, res))
    if cnt == 0:
        whitebox_lib.PRINTE("Fail! Can not get counter. Response:\n%s" % res)


def connect(wait_time=180, timeout=300, prodect_name="midstone100X"):
    """
    Connect tested product
    :param wait_time: wait some time before connect
    :param timeout: connect out time
    :param prodect_name: product name
    """
    prodect_info = YamlParse.getDeviceInfo()[prodect_name]
    login_prompt = prodect_info["loginPromptDiagOS"]
    all_info = ""
    if wait_time:
        Logger.info("pls wait %d s" % int(wait_time))
    start_time = time.time()
    while time.time() - start_time < int(timeout):
        try:
            part_info = device_obj.readMsg()
            if part_info:
                part_info = part_info.strip()
                all_info = all_info + "\n" + part_info
                if "System Date" and "System Time" and "Access Level" in all_info:
                    Logger.error("Fail! device has enter Bios!! Part of the information "
                                 "obtained during the waiting phase is:\n%s" % all_info)
                    whitebox_lib.whitebox_exit_bios_setup(deviceType)
                    break
                elif login_prompt in all_info:
                    device_obj.getPrompt(timeout=30)
                    break
        except Exception as E:
            Logger.info(str(E))
            SetWait(20)
    whitebox_lib.set_root_hostname(deviceType)
    #whitebox_lib.check_bmc_ready(deviceType)


def show_loop(loop):
    """
    :param loop: str.
    """
    Logger.info("--------------------------- Loop %s ---------------------------------" % loop)


def copy_lnkpack_to_dut(name=r"lnkpack3.011.zip", project_name=r"SilverstoneX"):
    """
    copy lnkpack tool to dut
    @Author: Caleb Mai <calebmai@celestica.com>
    :param name: lnkpack tool name (.zip)
    :param project_name: Project tool folder name
    """
    set_os_ip_by_dhclient(deviceType)
    dut_lnkpack_path = r"/home/cpu_performance"
    file_name = name
    tool_path = get_tool_path(project_name) + "/sit"
    whitebox_lib.mkdir_data_path(deviceType, dut_lnkpack_path)
    whitebox_lib.copy_files_from_pc_to_os(deviceType, pc_user, pc_password, pc_ip,
                                          file_name, tool_path, dut_lnkpack_path, 500)
    execute_cmd(r"cd %s" % dut_lnkpack_path)
    execute_cmd(r"chmod 777 *")
    execute_cmd(r"unzip -o %s" % name)


def config_and_run_lnkpack(name=r"lnkpack3.011.zip"):
    """
    config and run lnkpack,then check the result
    @Author: Caleb Mai <calebmai@celestica.com>
    :param name: lnkpack tool name (.zip)
    """
    dut_lnkpack_path = r"/home/cpu_performance"
    lnkpack_path = dut_lnkpack_path + "/" + name.strip(".zip")
    execute_cmd("cd %s" % lnkpack_path)
    ls = execute_cmd("ls")
    if "info.sh" not in ls:
        whitebox_lib.PRINTE("Fail!Can not find file <info.sh> in lnkpack tool. Response:\n%s" % ls)
    execute_cmd(r"chmod 777 info.sh")
    execute_cmd(r"cp info.sh /root")
    execute_cmd(r"cp run_linpack_ppw.sh %s/l_mklb_p_2018.3.011/benchmarks_2018/linux/mkl/benchmarks/mp_linpack"
                % lnkpack_path)
    execute_cmd(r"cd %s/l_mklb_p_2018.3.011/benchmarks_2018/linux/mkl/benchmarks/mp_linpack" % lnkpack_path)
    execute_cmd(r"chmod 777 *")
    execute_cmd(r"sed -i 's/#!\/bin\/sh/#\/bin\/bash/g' run_linpack_ppw.sh")
    execute_cmd(r"sed -i 's/psize=10000/psize=%s/g' run_linpack_ppw.sh" % psize)
    res = execute_cmd("./run_linpack_ppw.sh", 60)
    device_obj.sendline(r"cd /")
    if "PASSED" not in res:
        whitebox_lib.PRINTE("Fail! Run linpack fail! Response:\n%s" % res)
    actual_gflops = re.findall(r"\d+\.\d+e\+\d+", res)[-1]
    float_actual_gflops = float(actual_gflops.split("e+")[0]) * 10 ** float(actual_gflops.split("e+")[1].lstrip("0"))
    exp_actual_gflops = float(expect_min_gflops.split("e+")[0]) * \
                        10 ** float(expect_min_gflops.split("e+")[1].lstrip("0"))
    if float(float_actual_gflops) < float(exp_actual_gflops):
        whitebox_lib.PRINTE("Fail! expect gflops value [%s], actual gflops value [%s]. Response:\n%s"
                            % (expect_min_gflops, actual_gflops, res))


def check_port_if_disable_or_enable(enable=True, port_name="eth0"):
    """
    check command "ifconfig X up/down" if take effect
    @Author: Caleb Mai <calebmai@celestica.com>
    :param enable:True for check enable False for check disable
    :param port_name:port name
    """
    res = execute_cmd(r"ifconfig")
    if enable:
        if port_name not in res:
            whitebox_lib.PRINTE("Fail! port [%s] enable fail! Response:\n%s" % (port_name, res))
    else:
        if port_name in res:
            whitebox_lib.PRINTE("Fail! port [%s] disable fail! Response:\n%s" % (port_name, res))


def disable_or_enable_port(enable=True, port_name="eth0"):
    """
    use command "ifconfig X up/down" to set port enable or disable
    @Author: Caleb Mai <calebmai@celestica.com>
    :param enable: True for set enable False for set disable
    :param port_name: port name
    """
    enable_cmd = r"ifconfig %s up" % port_name
    disable_cmd = r"ifconfig %s down" % port_name
    if enable:
        execute_cmd(enable_cmd)
        check_port_if_disable_or_enable(enable, port_name)
    else:
        execute_cmd(disable_cmd)
        check_port_if_disable_or_enable(enable, port_name)


def tenG_port_enable_and_disable(port_name="eth0"):
    """
    check port disable and enable function
    @Author: Caleb Mai <calebmai@celestica.com>
    :param port_name: port name
    """
    status = True if port_name in execute_cmd(r"ifconfig") else False
    if status:
        disable_or_enable_port(False, port_name)
        SetWait(5)
        disable_or_enable_port(True, port_name)
    else:
        disable_or_enable_port(True, port_name)
        SetWait(5)
        disable_or_enable_port(False, port_name)


def config_dut_or_pc_ipv6(dut=True, nic_name=dut_nic_name, ipv6=dut_ipv6):
    """
    Configure ipv6 environment for dut or pc
    @Author: Caleb Mai <calebmai@celestica.com>
    :param dut:True for config dut . False for config pc
    :param nic_name:nic name
    :param ipv6:static ipv6 address
    """
    check_ipv6_cmd = '(test -f /proc/net/if_inet6 && echo "Current kernel is IPv6 ready")'
    check_res = execute_cmd_without_deal(check_ipv6_cmd) if dut else execute_cmd(check_ipv6_cmd, local=True)
    Logger.info("")
    if "Current kernel is IPv6 ready" not in check_res:
        whitebox_lib.PRINTE("Fail! your current running kernel does not supports IPv6. Response:\n%s" % check_res)
    execute_cmd(r"modprobe ipv6") if dut else execute_cmd(r"modprobe ipv6", local=True)
    add_ipv6_cmd = r"ifconfig %s inet6 add %s/64 up" % (nic_name, ipv6)
    execute_cmd(add_ipv6_cmd) if dut else execute_cmd(add_ipv6_cmd, local=True)


def check_LAN_port_connectivity():
    """
    Use command "ping6 " to check lan port connectivity(dut to pc / pc to dut / dut to local)
    @Author: Caleb Mai <calebmai@celestica.com>
    """
    dut_ping_pc_cmd = r"ping6 -c 60 %s" % pc_ipv6
    dut_ping_pc_res = execute_cmd(dut_ping_pc_cmd, 1000)
    if "0% packet loss" not in dut_ping_pc_res:
        whitebox_lib.PRINTE("Fail! DUT ping PC Fail. Response:\n%s" % dut_ping_pc_res)
    pc_ping_dut_cmd = r"ping6 -c 60 %s" % dut_ipv6
    pc_ping_dut_res = execute_cmd(pc_ping_dut_cmd, 1000, True)
    if "0% packet loss" not in pc_ping_dut_res:
        whitebox_lib.PRINTE("Fail! PC ping DUT Fail. Response:\n%s" % pc_ping_dut_res)
    ping_local_cmd = r"ping6 -c 60 -I %s %s" % (dut_nic_name, dut_ipv6)
    ping_local_res = execute_cmd(ping_local_cmd, 1000)
    if "0% packet loss" not in ping_local_res:
        whitebox_lib.PRINTE("Fail! PC ping DUT Fail. Response:\n%s" % ping_local_res)


def install_dut_netperf(project_name=r"SilverstoneX"):
    """
    install netperf for dut
    @Author: Caleb Mai <calebmai@celestica.com>
    :param project_name: Project tool folder name
    """
    dut_netperf_path = r"/home/white_box/netperf"
    file_name = dut_netperf_name
    tool_path = get_tool_path(project_name)
    whitebox_lib.mkdir_data_path(deviceType, dut_netperf_path)
    whitebox_lib.copy_files_from_pc_to_os(deviceType, pc_user, pc_password, pc_ip,
                                          file_name, tool_path, dut_netperf_path, 500)
    execute_cmd(r"cd %s" % dut_netperf_path)
    device_obj.sendline(r"chmod 777 *")
    if file_name.split(".")[-1] == "deb":
        res = execute_cmd("dpkg -i %s" % file_name)
        if "currently installed" not in res:
            whitebox_lib.PRINTE("Fail! install dut netperf fail! Response:\n%s" % res)
        return
    elif file_name.split(".")[-1] == "rpm":
        execute_cmd("rpm -ivh %s" % file_name)
    else:
        whitebox_lib.PRINTE("Fail! Tool netperf [%s] with wrong format!" % file_name)
    device_obj.sendline(r"cd /")


def install_pc_netperf(project_name=r"SilverstoneX"):
    """
    install netperf for pc
    @Author: Caleb Mai <calebmai@celestica.com>
    :param project_name: Project tool folder name
    """
    pc_netperf_path = r"/home/sit/netperf"
    file_name = pc_netperf_name
    tool_path = get_tool_path(project_name)
    whitebox_lib.mkdir_data_path(deviceType, pc_netperf_path, True)
    execute_cmd(r"cp -a %s/%s %s" % (tool_path, file_name, pc_netperf_path), local=True)
    execute_cmd("cd %s" % pc_netperf_path, local=True)
    execute_cmd(r"chmod 777 *", local=True)
    if file_name.split(".")[-1] == "deb":
        res = execute_cmd("dpkg -i %s" % file_name, local=True)
        if "currently installed" not in res:
            whitebox_lib.PRINTE("Fail! install pc netperf fail! Response:\n%s" % res)
        return
    elif file_name.split(".")[-1] == "rpm":
        execute_cmd("rpm -ivh %s" % file_name, local=True)
    else:
        whitebox_lib.PRINTE("Fail! Tool netperf [%s] with wrong format!" % file_name)
    execute_cmd("cd /", local=True)


def run_netperf(ip, run_netperf_time="60"):
    """
    run netperf and return the result
    @Author: Caleb Mai <calebmai@celestica.com>
    """
    execute_cmd(r"netserver", local=True)
    cmd = r"netperf -H %s -l %s -D 3" % (ip, run_netperf_time)
    res = execute_cmd(cmd, 1000)
    if "Throughput" not in res:
        whitebox_lib.PRINTE("Fail! run netperf Fail! Response:\n%s" % res)
    throughput = re.findall(r"\d+\.\d+", res)[-1]
    return float(throughput)


def get_dut_ipv6_from_dhcp(nic_name=dut_nic_name):
    """
    get ipv6 address from dut
    @Author: Caleb Mai <calebmai@celestica.com>
    :param nic_name:dut nic name
    """
    execute_cmd("ifdown %s" % nic_name)
    execute_cmd("ifup %s" % nic_name)
    cmd = r"ifconfig %s" % nic_name
    res = execute_cmd(cmd)
    ipv6 = re.findall(r"inet6\s+(.*?)\s+prefixlen", res)
    if not ipv6:
        whitebox_lib.PRINTE("Fail! Can not get ipv6 address. Response:\n%s" % res)
    return ipv6[0]


def get_pc_ipv6(dut_dhcp_ipv6, nic_name=pc_nic_name):
    """
    get ipv6 address from pc which same network segment with dut
    @Author: Caleb Mai <calebmai@celestica.com>
    :param dut_dhcp_ipv6:dut ipv6
    :param nic_name:pc nic name
    """
    cmd = r"ifconfig %s" % nic_name
    res = execute_cmd(cmd, local=True)
    ipv6 = re.findall(r"inet6\s+(.*?)\s+prefixlen", res)
    if not ipv6:
        whitebox_lib.PRINTE("Fail! Can not get ipv6 address. Response:\n%s" % res)
    for i in ipv6:
        if i.split(":")[0] == dut_dhcp_ipv6.split(":")[0]:
            return i
    whitebox_lib.PRINTE("Fail! Got pc ipv6 which same network segment with dut Fail! Response:\n%s" % res)


def check_ping_dhcp_ipv6(dut_dhcp_ipv6, pc_dhcp_ipv6):
    """
    check ping ipv6 from dhcp
    @Author: Caleb Mai <calebmai@celestica.com>
    :param dut_dhcp_ipv6: dut dhcp ipv6
    :param pc_dhcp_ipv6: pc dhcp ipv6
    """
    dut_cmd = r"ping6 -c 60 %s%s%s" % (pc_dhcp_ipv6, "%", dut_nic_name)
    res = execute_cmd(dut_cmd, 600)
    if "0% packet loss" not in res:
        whitebox_lib.PRINTE("Fail! Dut ping PC from dhcp Fail! Response:\n%s" % res)
    pc_cmd = r"ping6 -c 60 %s%s%s" % (dut_dhcp_ipv6, "%", pc_nic_name)
    res_pc = execute_cmd(pc_cmd, 600, local=True)
    if "0% packet loss" not in res_pc:
        whitebox_lib.PRINTE("Fail! PC ping Dut from dhcp Fail! Response:\n%s" % res)


def check_ps_fio():
    """
    Check fio process by command "ps"
    @Author: Caleb Mai <calebmai@celestica.com>
    """
    cmd = r"ps"
    res = execute_cmd(cmd)
    if "fio" not in res:
        whitebox_lib.PRINTE("Fail! The system does not have a fio process")


def check_hot_plug_action(unplug=True, unplug_flag="Presence detected | Deasserted",
                          insert_flag="Presence detected | Asserted", cmd=r"ipmitool sel list"):
    """
    check is the unplugging action being recorded by "ipmitool sel list" or "dmesg"
    @Author: Caleb Mai <calebmai@celestica.com>
    :param unplug_flag: unplug info flag
    :param insert_flag: insert info flag
    :param unplug:True for check unplug .False for check insert
    :param cmd:check hot plug action command
    :return: True for record. False for no record.
    """
    device_obj.flush()
    device_obj.readMsg()
    device_obj.sendline(cmd)
    time.sleep(0.3)
    res = device_obj.readMsg()
    if unplug:
        if unplug_flag not in res:
            return False
        else:
            return True
    else:
        if insert_flag not in res:
            return False
        else:
            return True


def execute_cmd_c(cmd, timeout=180, local=False):
    """
    Send command and get the response
    :param cmd: command
    :param timeout: get the response timeout
    :param local:True-send cmd on PC
    """
    if local:
        response = Device.execute_local_cmd(device_obj, cmd, timeout)
        return response
    cmd = 'time ' + cmd
    device_obj.flush()
    result = device_obj.sendCmdRegexp(cmd, response_end_flag, timeout)
    if "|" in cmd:
        cmd_list = cmd.split("|")
        cmd_c = ""
        for i in cmd_list:
            cmd_c += i + r"\|"
        cmd_c = cmd_c.strip(r"\|")
    else:
        cmd_c = cmd
    res = re.findall(r".*%s(.*)\n+real.*" % cmd_c, result, re.S)
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
        return ""


def check_psu_status(ok=True):
    """
    check psu status by "ipmitool sdr list" && "ipmitool sensor list"
    @Author: Caleb Mai <calebmai@celestica.com>
    :param ok: True for check "ok", False for check unplug
    """
    device_obj.switchToBmc()
    cmd_sdr = r"ipmitest sdr list | grep -i psu | grep -v Status"
    sdr_res = execute_openbmc_cmd(cmd_sdr, timeout=300)
    cmd_sensor = r"ipmitest sensor list | grep -i psu | grep -v Status"
    sensor_res = execute_openbmc_cmd(cmd_sensor, timeout=300)
    device_obj.trySwitchToCpu()
    sensor = 0
    for i in sensor_res.splitlines():
        if "ok" not in i.split("|")[3].strip():
            sensor += 1
    if ok:
        if 'no reading' in sdr_res:
            whitebox_lib.PRINTE("Fail! psu sdr status not all 'ok'. Response:\n%s" % sdr_res)
        if sensor != 0:
            whitebox_lib.PRINTE("Fail! psu sensor status not all 'ok'. Response:\n%s" % sensor_res)
    else:
        if "no reading" not in sdr_res:
            whitebox_lib.PRINTE("Fail! psu not unplug. Response:\n%s" % sdr_res)
        if sensor == 0:
            whitebox_lib.PRINTE("Fail! psu not unplug. Response:\n%s" % sensor_res)


def check_psu_cable(ok=True):
    """
    check psu cable status by "ipmitool sdr list" && "ipmitool sensor list"
    @Author: Caleb Mai <calebmai@celestica.com>
    :param ok: True for check "ok", False for check unplug
    """
    device_obj.switchToBmc()
    unplug_sdr = ["0 Volts", "0 Amps", "0 Watts", "0 RPM"]
    cmd_sdr = r"ipmitest sdr list | grep -i psu"
    cmd_sensor = r"ipmitest sensor list | grep -i psu"
    sdr_res = execute_openbmc_cmd(cmd_sdr, timeout=300)
    sensor_res = execute_openbmc_cmd(cmd_sensor, timeout=300)
    device_obj.trySwitchToCpu()
    sdr_value = list()
    for i in sdr_res.splitlines():
        sdr_value.append(i.split("|")[1].strip())
    sensor_list = list()
    for i in sensor_res.splitlines():
        sensor_list.append(i.split("|")[1].strip())
    if ok:
        for i in unplug_sdr:
            if i in sdr_value:
                whitebox_lib.PRINTE("Fail! psu cable not connect. Response:\n%s" % sdr_res)
        if "0.000" in sensor_list:
            whitebox_lib.PRINTE("Fail! psu cable not connect. Response:\n%s" % sensor_res)
    else:
        for i in unplug_sdr:
            if i not in sdr_value:
                whitebox_lib.PRINTE("Fail! psu cable not unplug. Response:\n%s" % sdr_res)
        if "0.000" not in sensor_list:
            whitebox_lib.PRINTE("Fail! psu cable not unplug. Response:\n%s" % sensor_res)


def check_fan_status(ok=True, fan_num=1):
    """
    check fan status by "ipmitool sdr list" && "ipmitool sensor list"
    @Author: Caleb Mai <calebmai@celestica.com>
    :param fan_num: Number of fans hot plug in one time
    :param ok: True for check "ok", False for check unplug
    """
    SetWait(5)
    device_obj.switchToBmc()
    cmd_sdr = r"ipmitest sdr list | grep -i fan | grep -v PSU | grep -v Status"
    sdr_res = execute_openbmc_cmd(cmd_sdr, timeout=300)
    cmd_sensor = r"ipmitest sensor list | grep -i fan | grep -v PSU | grep -v Status"
    sensor_res = execute_openbmc_cmd(cmd_sensor, timeout=300)
    device_obj.trySwitchToCpu()
    if ok:
        if "no reading" in sdr_res:
            whitebox_lib.PRINTE("Fail! Fan sdr status not all 'ok'. Response:\n%s" % sdr_res)
        for i in sensor_res.splitlines():
            if "ok" not in i.split("|")[3].strip():
                whitebox_lib.PRINTE("Fail! Fan sensor status not all 'ok'. Response:\n%s" % sensor_res)
    else:
        if sdr_res.count("no reading") != 2*int(fan_num):
            whitebox_lib.PRINTE("Fail! Fan not unplug. Response:\n%s" % sdr_res)
        front_sdr_rpm_list = list()
        front_sensor_rpm_list = list()
        rear_sdr_rpm_list = list()
        rear_sensor_rpm_list = list()
        for i in sensor_res.strip("\n").splitlines():
            if "front" in i.lower():
                front_sensor_rpm_list.append(i.split("|")[1].strip())
            if "rear" in i.lower():
                rear_sensor_rpm_list.append(i.split("|")[1].strip())
        for i in sdr_res.strip("\n").splitlines():
            if "front" in i.lower():
                front_sdr_rpm_list.append(i.split("|")[1].strip().strip(" RPM"))
            if "rear" in i.lower():
                rear_sdr_rpm_list.append(i.split("|")[1].strip().strip(" RPM"))
        sensor_front_unplug = 0
        sensor_rear_unplug = 0
        sdr_front_unplug = 0
        sdr_rear_unplug = 0
        for i in front_sensor_rpm_list:
            if is_float(i):
                if not float(front_fan_max_rpm[0]) <= float(i) <= float(front_fan_max_rpm[1]):
                    whitebox_lib.PRINTE("Fail! Front Fan RPM is out of range. Response:\n%s" % sensor_res)
            else:
                sensor_front_unplug += 1
        for i in rear_sensor_rpm_list:
            if is_float(i):
                if not float(rear_fan_max_rpm[0]) <= float(i) <= float(rear_fan_max_rpm[1]):
                    whitebox_lib.PRINTE("Fail! Rear Fan RPM is out of range. Response:\n%s" % sensor_res)
            else:
                sensor_rear_unplug += 1
        for i in front_sdr_rpm_list:
            if is_float(i):
                if not float(front_fan_max_rpm[0]) <= float(i) <= float(front_fan_max_rpm[1]):
                    whitebox_lib.PRINTE("Fail! Front Fan RPM is out of range. Response:\n%s" % sensor_res)
            else:
                sdr_front_unplug += 1
        for i in rear_sdr_rpm_list:
            if is_float(i):
                if not float(rear_fan_max_rpm[0]) <= float(i) <= float(rear_fan_max_rpm[1]):
                    whitebox_lib.PRINTE("Fail! Rear Fan RPM is out of range. Response:\n%s" % sensor_res)
            else:
                sdr_rear_unplug += 1
        if not sensor_front_unplug == sensor_rear_unplug == sdr_front_unplug == sdr_rear_unplug == int(fan_num):
            whitebox_lib.PRINTE("Fail! Fan not unplug. Response:\n%s\n%s" % (sensor_res, sdr_res))


def hot_plug_sit(num, cycle, fast=True, unplug_flag=psu_unplug_flag, insert_flag=psu_insert_flag, name=r"PSU"):
    """
    SIT psu hot plug case
    @Author: Caleb Mai <calebmai@celestica.com>
    :param num: number of [PSU, PSU_Cable, Fan, Fan_tray, RJ45, USB]
    :param cycle: hotplug cycle for each [PSU, PSU_Cable, Fan, Fan_tray, RJ45, USB]
    :param fast: True for test fast hotplug, False for test slow hotplug
    :param unplug_flag:unplug flag by "ipmitool sel list" or "dmesg"
    :param insert_flag:insert flag by "ipmitool sel list" or "dmesg"
    :param name: hot plug name [PSU, PSU_Cable, Fan, Fan_tray, RJ45, USB]
    """
    psu = int(float(num) + 1)
    cycle = int(float(cycle) + 1)
    insert_time = 100
    unplug_time = 0
    out_cnt = 0
    in_cnt = 0
    if fast:
        Logger.info("################################################################################################")
        Logger.info("######################## Fast %s Hot plug------%s:%s Cycle:%s ##################################"
                    % (name, name, psu, cycle))
        Logger.info("############### Please remove %s_%s and plug it back quickly(within one second) ################"
                    % (name, psu))
        Logger.info("################################################################################################")
        start_time = time.time()
        while time.time() - start_time < 180:
            if name.lower() in ["psu", "psu_cable", "fan", "fan_tray"]:
                if check_hot_plug_action(True, unplug_flag, insert_flag, "ipmitool sel list"):
                    out_cnt += 1
                    unplug_time = time.time()
                    break
            elif name.lower() in ["rj45", "usb"]:
                if check_hot_plug_action(True, unplug_flag, insert_flag, "dmesg"):
                    out_cnt += 1
                    unplug_time = time.time()
                    break
            else:
                whitebox_lib.PRINTE("Fail! The parameter name is not in [PSU, PSU_Cable, Fan, Fan_tray, RJ45]")
        if out_cnt != 1:
            whitebox_lib.PRINTE("Fail! can not detect %s unplug info in 180 seconds." % name)
        while time.time() - start_time < 180:
            if name.lower() in ["psu", "psu_cable", "fan", "fan_tray"]:
                if check_hot_plug_action(False, unplug_flag, insert_flag, "ipmitool sel list"):
                    in_cnt += 1
                    insert_time = time.time()
                    break
            elif name.lower() in ["rj45", "usb"]:
                if check_hot_plug_action(False, unplug_flag, insert_flag, "dmesg"):
                    in_cnt += 1
                    insert_time = time.time()
                    break
            else:
                whitebox_lib.PRINTE("Fail! The parameter name is not in [PSU, PSU_Cable, Fan, Fan_tray, RJ45]")
        if in_cnt != 1:
            whitebox_lib.PRINTE("Fail! can not detect %s insert info in 180 seconds." % name)
        if insert_time - unplug_time > 10:
            whitebox_lib.PRINTE("Fail! Unplugging time is over 1 second.")
        if "psu" == name.lower():
            check_psu_status(True)
        elif "psu_cable" == name.lower():
            check_psu_cable(True)
        elif "fan" == name.lower():
            check_fan_status(True, 1)
        elif "fan_tray" == name.lower():
            check_fan_status(True, fan_num_in_tray)
        elif "rj45" == name.lower():
            check_rj(True)
        elif "usb" == name.lower():
            check_usb_hot_plug(True)
        else:
            whitebox_lib.PRINTE("Fail! The parameter name is not in [PSU, PSU_Cable, Fan, Fan_tray, RJ45]")
        check_ps_fio()
        check_info()
    else:
        Logger.info("################################################################################################")
        Logger.info("################# Slow %s Hot plug------%s:%s Cycle:%s #########################################"
                    % (name, name, psu, cycle))
        Logger.info("################# Please remove %s_%s, then wait for 1 minute and plug it back #################"
                    % (name, psu))
        Logger.info("################################################################################################")
        start_time = time.time()
        while time.time() - start_time < 180:
            if name.lower() in ["psu", "psu_cable", "fan", "fan_tray"]:
                if check_hot_plug_action(True, unplug_flag, insert_flag, "ipmitool sel list"):
                    out_cnt += 1
                    break
            elif name.lower() in ["rj45", "usb"]:
                if check_hot_plug_action(True, unplug_flag, insert_flag, "dmesg"):
                    out_cnt += 1
                    break
            else:
                whitebox_lib.PRINTE("Fail! The parameter name is not in [PSU, PSU_Cable, Fan, Fan_tray, RJ45]")
        if out_cnt != 1:
            whitebox_lib.PRINTE("Fail! can not detect %s unplug info in 180 seconds." % name)
        if "psu" == name.lower():
            check_psu_status(False)
        elif "psu_cable" == name.lower():
            check_psu_cable(False)
        elif "fan" == name.lower():
            check_fan_status(False, 1)
        elif "fan_tray" == name.lower():
            check_fan_status(False, fan_num_in_tray)
        elif "rj45" == name.lower():
            check_rj(False)
        elif "usb" == name.lower():
            check_usb_hot_plug(False)
        else:
            whitebox_lib.PRINTE("Fail! The parameter name is not in [PSU, PSU_Cable, Fan, Fan_tray, RJ45]")
        check_ps_fio()
        check_info()
        SetWait(60)
        Logger.info("################################################################################################")
        Logger.info("################# Slow %s Hot plug------%s:%s Cycle:%s #########################################"
                    % (name, name, psu, cycle))
        Logger.info("################# Now Please plug %s_%s back!  #################################################"
                    % (name, psu))
        Logger.info("################################################################################################")
        insert_start_time = time.time()
        while time.time() - insert_start_time < 180:
            if name.lower() in ["psu", "psu_cable", "fan", "fan_tray"]:
                if check_hot_plug_action(False, unplug_flag, insert_flag, "ipmitool sel list"):
                    in_cnt += 1
                    break
            elif name.lower() in ["rj45", "usb"]:
                if check_hot_plug_action(False, unplug_flag, insert_flag, "dmesg"):
                    in_cnt += 1
                    break
            else:
                whitebox_lib.PRINTE("Fail! The parameter name is not in [PSU, PSU_Cable, Fan, Fan_tray, RJ45]")
        if in_cnt != 1:
            whitebox_lib.PRINTE("Fail! can not detect %s insert info in 180 seconds." % name)
        if "psu" in name.lower():
            check_psu_status(True)
        elif "psu_cable" == name.lower():
            check_psu_cable(True)
        elif "fan" == name.lower():
            check_fan_status(True, 1)
        elif "fan_tray" == name.lower():
            check_fan_status(True, fan_num_in_tray)
        elif "rj45" == name.lower():
            check_rj(True)
        elif "usb" == name.lower():
            check_usb_hot_plug(True)
        else:
            whitebox_lib.PRINTE("Fail! The parameter name is not in [PSU, PSU_Cable, Fan, Fan_tray, RJ45]")
        check_ps_fio()
        check_info()


def save_log_then_clear(path=r"/home/hot_plug_log/"):
    """
    save system log to file then clear
    @Author: Caleb Mai <calebmai@celestica.com>
    :param path: save file path
    """
    whitebox_lib.mkdir_data_path(deviceType, path)
    device_obj.sendline("ipmitool sel list >> %s/sel_%s.log" % (path, str(datetime.datetime.now()).split(" ")[0]))
    device_obj.sendline("dmesg >> %s/dmesg_%s.log" % (path, str(datetime.datetime.now()).split(" ")[0]))
    device_obj.sendline(
        "cat /var/log/messages >> %s/message_%s.log" % (path, str(datetime.datetime.now()).split(" ")[0]))
    execute_cmd("ipmitool sel clear")
    time.sleep(5)
    SetDmesgClear()
    execute_cmd(r"cat /dev/null > /var/log/messages")


def check_info():
    """
    check info for hot plug
    @Author: Caleb Mai <calebmai@celestica.com>
    """
    CheckDmesgInfo()
    CheckCMDResponse("ipmitool sel list", hot_plug_sel_error_list, False, False, False, True)
    CheckCMDResponse("cat /var/log/messages", messages_error_list, False, False, False, True)


def run_iperf3_for_hot_plug(iperf_time=43200, log_path=r"/home/hot_plug_log/iperf", background=True):
    """
    run iperf3 for rj45 hot plug
    @Author: Caleb Mai <calebmai@celestica.com>
    """
    flag = " &" if background else ""
    tool_path = get_tool_path()
    file_name = r"iperf3_3.1.3-1_amd64.deb"
    pc_file_name = r"iperf3-3.1.3-1.fc24.x86_64.rpm"
    execute_cmd("chmod 777 %s/%s" % (tool_path, pc_file_name), local=True)
    execute_cmd("rpm -ivh %s/%s" % (tool_path, pc_file_name), local=True)
    os.system("iperf3 -s > /home/iperf.log &")
    whitebox_lib.mkdir_data_path(deviceType, log_path)
    whitebox_lib.copy_files_from_pc_to_os(deviceType, pc_user, pc_password, pc_ip, file_name,
                                          tool_path, log_path, 5)
    whitebox_lib.chmod_file(deviceType, log_path + "/" + file_name)
    device_obj.sendline("cd %s" % log_path)
    execute_cmd("dpkg -i %s" % file_name)
    cmd = r"iperf3 -c %s -t %s > /home/iperf3.log %s" % (pc_ip, iperf_time, flag)
    device_obj.sendline(cmd)
    time.sleep(5)
    device_obj.sendline("cd /")
    ps_res = execute_cmd("ps")
    if "iperf3" not in ps_res:
        whitebox_lib.PRINTE("Fail! Run iperf fail! Response:\n%s" % ps_res)


def check_rj(link=True):
    """
    check RJ45 status for rj45 hot plug
    @Author: Caleb Mai <calebmai@celestica.com>
    """
    iperf_status = execute_cmd(r"tail /home/iperf3.log")
    ps_res = execute_cmd("ps")
    if "terminated" in iperf_status or "iperf3" not in ps_res:
        whitebox_lib.PRINTE("Fail! iperf is terminated! Response:\n%s\n%s" % (ps_res, iperf_status))
    if link:
        ping_to_pc(deviceType, 10, pc_ip, "link")
    else:
        ping_to_pc(deviceType, 10, pc_ip, "loss")


def check_usb_hot_plug(insert=True):
    if insert:
        disk_name = get_sandisk_usb_device_name()
        auto_detection_usb_device(disk_name)
        touch_object_on_usb(disk_name[0])
    else:
        pass


def ping_to_pc_via_designated_port(device, ping_time=10, ip_address=pc_ip, expected='link', port="eth0"):
    """
    ping the PC IP 10s via Designated network port and determine whether the received packet is lost.
    :param port:Designated network port name
    :param device:the name of the tested product
    :param ip_address:service PC ip,str
    :param ping_time:test time unit:second
    :param expected:expect link or loss
    """
    log.debug("Entering whitebox_exec_ping with args : %s" % (str(locals())))
    log.debug("Execute the ping from Device:%s to ip:%s" % (device, ip_address))
    cmd = "ping -I %s %s -c %s" % (port, ip_address, str(ping_time))
    success_msg = str(ping_time) + ' packets transmitted, ' + str(ping_time) + ' (packets )?received, 0% packet loss'
    loss_msg = '100% packet loss'
    output = whitebox_lib.execute(device, cmd, None, ping_time + 30)
    try:
        for i in range(3):
            if expected == 'link':
                match = re.search(success_msg, output)
                if match:
                    log.info("Found: %s" % (match.group(0)))
                    log.info("ping to %s %s seconds pass!!!" % (ip_address, str(ping_time)))
                    break
            elif expected == 'loss':
                match = re.search(loss_msg, output)
                if match:
                    log.info("Found: %s" % (match.group(0)))
                    log.info("ping to " + ip_address + " get 100% packet loss")
                    break
        else:
            whitebox_lib.PRINTE("Fail!!! Try three times, but couldn't get the %s expect" % expected)
    except Exception as E:
        whitebox_lib.PRINTE(str(E))


def execute_openbmc_cmd(cmd, timeout=180):
    """
    Send command and get the response
    :param cmd: command
    :param timeout: get the response timeout
    """
    if "|" not in cmd:
        cmd = 'time ' + cmd
    else:
        cmd = cmd.rstrip(cmd.split("|")[-1]) + " time " + cmd.split("|")[-1]
    device_obj.flush()
    result = device_obj.sendCmdRegexp(cmd, response_end_flag, timeout)
    if "|" in cmd:
        cmd_list = cmd.split("|")
        cmd_c = ""
        for i in cmd_list:
            cmd_c += i + r"\|"
        cmd_c = cmd_c.strip(r"\|")
    else:
        cmd_c = cmd
    res = re.findall(r".*%s(.*)\n+real.*" % cmd_c, result, re.S)
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
        return ""


def getPrompt():
    device_obj.getPrompt(timeout=30)


def test():
    check_psu_status(True)
    # check_psu_status(False)
    # check_psu_cable(True)
    check_psu_cable(False)
    # check_fan_status(True)
    check_fan_status(False)
# ######################################### Caleb END ##############################################################


# ######################################### Janson Start ############################################################
def setroot(device):
    return whitebox_lib.set_root_hostname(device)


def check_bmc_ready(device):
    return whitebox_lib.check_bmc_ready(device)


# def GetBmcIP(device):
#     return whitebox_lib.get_ip_address_from_ipmitool(device)


def check_communication_lan_pc(device, ip):
    return whitebox_lib.check_communication_lan_pc(device, ip)


def set_os_ip_by_dhclient(device):
    return whitebox_lib.set_os_ip_by_dhclient(device)


def ping_to_pc(device, ping_time=10, ip_address=pc_ip, expected='link'):
    """
    author : Janson Jiang
    ping the PC IP 10s and determine whether the received packet is lost.
    :param device:the name of the tested product
    :param ip_address:service PC ip,str
    :param ping_time:test time unit:second
    :param expected:expect link or loss
    """
    log.debug("Entering whitebox_exec_ping with args : %s" % (str(locals())))
    log.debug("Execute the ping from Device:%s to ip:%s" % (device, ip_address))
    cmd = "ping %s -c %s" % (ip_address, str(ping_time))
    success_msg = str(ping_time) + ' packets transmitted, ' + str(ping_time) + ' (packets )?received, 0% packet loss'
    loss_msg = '100% packet loss'
    output = whitebox_lib.execute(device, cmd, None, ping_time+30)
    try:
        for i in range(3):
            if expected == 'link':
                match = re.search(success_msg, output)
                if match:
                    log.info("Found: %s" % (match.group(0)))
                    log.info("ping to %s %s seconds pass!!!" % (ip_address, str(ping_time)))
                    break
            elif expected == 'loss':
                match = re.search(loss_msg, output)
                if match:
                    log.info("Found: %s" % (match.group(0)))
                    log.info("ping to " + ip_address + " get 100% packet loss")
                    break
        else:
            whitebox_lib.PRINTE("Fail!!! Try three times, but couldn't get the %s expect" % expected)
    except Exception as E:
        whitebox_lib.PRINTE(str(E))


def set_static_ip(device, exp_eth='eth0', exp_eth_ip='10.10.10.89'):
    """
    author : Janson Jiang
    set lan static ip by command "ifconfig"
    :param device: the name of the tested product
    :param exp_eth: eth which want to set (default eth0),str
    :param exp_eth_ip: ip which want to set(default '10.10.10.89'),str
    """
    cmd = 'ifconfig %s %s' % (exp_eth, exp_eth_ip)
    execute_info = whitebox_lib.execute(device, cmd)
    log.info(str(execute_info))
    res = get_eth_ip_from_ifconfig(device, exp_eth)
    if res == exp_eth_ip:
        log.info("set static ip %s succeed!!" % exp_eth_ip)
    else:
        whitebox_lib.PRINTE("set static ip %s,but get %s" % (exp_eth_ip, res))


def get_eth_ip_from_ifconfig(device, net_name="eth0"):
    """
    author : Janson Jiang
    get all eth ip from ifconfig,and return net_name ip
    :param device: the name of the tested product
    :param net_name: net name which want to return ,str
    :return: net_name ip
    """
    ether_dict = dict()
    cmd = "ifconfig"
    response = whitebox_lib.execute(device, cmd)
    for _ in response.split("\n\r\n"):
        a = re.findall(r"(\w+):\s.*inet (.*?)  netmask", _, re.S)
        if a:
            ether_dict[a[0][0]] = a[0][1]
    log.info("Get all ether ip info: %s" % str(ether_dict))
    if net_name in ether_dict.keys():
        log.info("Get %s ip is [%s]" % (net_name, ether_dict[net_name]))
    else:
        whitebox_lib.PRINTE("Get %s ip fail!!! please check the net name and lan link status" % net_name)
    return ether_dict[net_name]


def get_eth_mac_from_ifconfig(device, net_name="eth0"):
    """
    author : Janson Jiang
    get all eth mac from ifconfig,and return net_name mac address
    :param device: the name of the tested product
    :param net_name: net name which want to return ,str
    :return: net_name mac
    """
    ether_dict = dict()
    cmd = "ifconfig -a"
    response = whitebox_lib.execute(device, cmd)
    for _ in response.split("\n\r\n"):
        a = re.findall(r"(\w+):\s.*ether (.*?)  txqueuelen", _, re.S)
        if a:
            ether_dict[a[0][0]] = a[0][1]
    log.info("Get all ether mac address info: %s" % str(ether_dict))
    if net_name in ether_dict.keys():
        log.info("Get %s mac address info is [%s]" % (net_name, ether_dict[net_name]))
    else:
        whitebox_lib.PRINTE("Get %s mac fail!!! please check the net name" % net_name)
    return ether_dict[net_name]


def check_port_status(device, net_name="eth0"):
    """
    author : Janson Jiang
    check whether eth port is link up or link down
    :param device: the name of the tested product
    :param net_name: which port ststus want to check,str
    :return: Ture:link up;False:link down
    """
    cmd_1 = r"ifconfig"
    response = whitebox_lib.execute(device, cmd_1)
    res = re.findall(r"%s" % net_name, response, re.S)
    if res:
        log.info("%s port is link up ,can find port name" % net_name)
        return True
    else:
        log.info("%s port is link down ,can not find port name" % net_name)
        log.info(response)
        return False


def set_port_disable_then_enable(device, net_name="eth0"):
    """
    author : Janson Jiang
    set port (default eth0) disable and check the status,then set port enable.
    :param device:the name of the tested product
    :param net_name:which port want to check,str
    """
    cmd_1 = r"ifconfig %s down" % net_name
    cmd_2 = r"ifconfig %s up" % net_name
    port_status = check_port_status(device, net_name)
    if port_status:
        whitebox_lib.execute(device, cmd_1)
        res = check_port_status(device, net_name)
        if not res:
            log.info("Pass!!!,port %s is disable" % net_name)
            log.info("Now will enable the net port %s" % net_name)
            whitebox_lib.execute(device, cmd_2)
            SetWait(2)
            check_port_status(device, net_name)
        else:
            whitebox_lib.PRINTE("Fail!!!,port %s is still link up,[%s] command did not take effect" % (net_name, cmd_1))
    else:
        whitebox_lib.PRINTE("Please check the net name,make sure the %s is link up before test." % net_name)


def get_eth_speed_from_ethtool(device, net_name="eth0", exp_speed=None):
    """
    author : Janson Jiang
    get eth(default eth0) speed from ethtool,and return the speed.
    :param device: the name of the tested product
    :param net_name: which port want to check,str
    :param exp_speed: default None,can set to expect speed,such as "1000Mb/s"
    :return:net_name speed
    """
    cmd = r"ethtool %s" % net_name
    all_info = whitebox_lib.execute(device, cmd)
    speed_info = re.findall(r"Speed: (.*?Mb/s)", all_info, re.S)[0].strip()
    if exp_speed:
        if speed_info == exp_speed:
            log.info("Eth name [%s] speed is %s, same with the expect." % (net_name, speed_info))
            return speed_info
        else:
            whitebox_lib.PRINTE("Fail!!!expect eth [%s] speed %s,but get %s." % (net_name, exp_speed, speed_info))
    else:
        log.info("Eth name [%s] speed is %s." % (net_name, speed_info))
        return speed_info


def get_silverstonex_tool_path():
    """
    author : Janson Jiang
    get silverstoneX tool path
    """
    path_1 = os.getcwd()
    path_2 = path_1.split("/")
    path_2.pop()
    path_list = path_2 + ["platform/whitebox/tool/SilverstoneX"]
    tool_path = "/".join(path_list)
    return tool_path


def copy_tool_files_from_pc_to_os(file_name="*"):
    """
    author : Janson Jiang
    copy all file from pc to os
    """
    tool_path = get_silverstonex_tool_path()
    whitebox_lib.mkdir_data_path(deviceType, dut_file_path)
    whitebox_lib.copy_files_from_pc_to_os(deviceType, pc_user, pc_password, pc_ip, file_name,
                                          tool_path, dut_file_path, 1024)
    whitebox_lib.chmod_file(deviceType, dut_file_path + "/" + file_name)
    res = execute_cmd("ls -al %s" % dut_file_path)
    log.info(res)


def run_iperf(ping_time="30", background=None, expect_bw=1000):
    """
    author : Janson Jiang
    run iperf
    :param ping_time: time want to ping unit:second
    :param background: None or True
    :param expect_bw:expect bandwidth, unit:Mbit/sec
    """
    cmd_install = r"dpkg -i *.deb"
    device_obj.sendline("cd %s" % dut_file_path)
    execute_cmd(cmd_install)
    flag = " &" if background else ""
    os.system("iperf3 -s &")
    SetWait(1)
    cmd_client = r"iperf3 -c %s -t %s %s" % (pc_ip, ping_time, flag)
    res_iperf = execute_cmd(cmd_client, timeout=int(ping_time)+30)
    log.info(res_iperf)
    res = re.findall(r"- -.*sender.* (.*?) Mbits/sec", res_iperf, re.S)
    if int(float(res[0])) >= int(expect_bw) * 0.9:
        log.info("Iperf test pass!!!,actually bandwidth is %s Mbits/sec." % res[0])
    else:
        whitebox_lib.PRINTE('Iperf test fail!!!,actually bandwidth is %s Mbits/sec,'
                            'less than expect  bandwidth %s' % (res[0], '90%'))


def send_cmd(cmd, keyword=None, timeout=60):
    """
    Send cmd,if keyword is not None, check keyword in response and return response
    :param cmd:command
    :param keyword:response keyword
    :param timeout:Check the timeout of keywords in the return
    :return: res include keywords
    """
    device_obj.sendline(cmd)
    if keyword:
        try:
            res = device_obj.read_until_regexp(keyword, timeout=timeout)
            return res
        except Exception as E:
            whitebox_lib.PRINTE(str(E))


def enter_sdk(sdk_config="PAM4_400G_32", remote=False):
    """
    author : Janson Jiang
    set switch port enable or disable,for innovium ic.
    enter sdk bcm
    :param sdk_config:sdk config file, str
    :param remote:whether remote
    """
    KillProcess("innovium")
    device_obj.sendline("cd %s" % sdk_path)
    if remote:
        whitebox_lib.execute(deviceType, "./%s -d -m %s" % (sdk_sh, sdk_config))
        if whitebox_lib.execute(deviceType, "ps -aux|grep -i innovium"):
            log.info("Enter SDK BCM pass!!!")
            SetWait(3)
        else:
            whitebox_lib.PRINTE("Enter SDK BCM Fail!!!")
    else:
        device_obj.sendline("./%s -m %s" % (sdk_sh, sdk_config))
        try:
            res = device_obj.read_until_regexp("IVM:0", timeout=60)
            if 'IVM:0' in res:
                log.info(res)
                log.info("Enter SDK BCM pass!!!")
                SetWait(3)
        except Exception as E:
            whitebox_lib.PRINTE("Enter SDK BCM Fail!!!,error info is [%s]" % E)


def exit_sdk(remote=False):
    """
    author : Janson Jiang
    set switch port enable or disable,for innovium ic.
    exit sdk
    :param remote:whether remote
    """
    if remote:
        execute_cmd("./%s exit" % cls_name)
        log.info("Exit sdk bcm pass")
    else:
        send_cmd("exit", "Script done")
        log.info("Exit sdk bcm pass")


def send_cls_cmd(cmd, timeout=60):
    """
    author : Janson Jiang
    set switch port enable or disable,for innovium ic.
    send sdk bcm cls cmd
    :param cmd:cmd want to send
    :param timeout:timeout
    """
    cmd = "./" + cls_name + " " + str(cmd)
    res = whitebox_lib.execute(deviceType, cmd, timeout=timeout)
    return res


def set_switch_port_enable_or_disable(port_num, set_port="enable", remote=False):
    """
    author : Janson Jiang
    set switch port enable or disable,for innovium ic.
    :param set_port: set port "disable" or "enable"
    :param port_num: port num want to set
    :param remote: True or False
    """
    cmd_port_enable = "port enable 1-" + str(port_num)
    cmd_port_disable = "port disable 1-" + str(port_num)
    cmd_port_status = r"port info"
    if set_port == "enable":
        if remote:
            send_cls_cmd(cmd_port_enable)
            port_status = send_cls_cmd(cmd_port_status)
        else:
            send_cmd(cmd_port_enable)
            send_cmd("shell ls", "libifcs")
            port_status = send_cmd(cmd_port_status, "RECIRC")
        if int(port_status.count("LINK_UP")) >= port_num:
            log.info("set switch %s port enable pass!" % port_num)
        else:
            whitebox_lib.PRINTE("set switch %s port enable fail!" % port_num)
    if set_port == "disable":
        if remote:
            send_cls_cmd(cmd_port_disable)
            port_status = send_cls_cmd(cmd_port_status)
        else:
            send_cmd(cmd_port_disable)
            send_cmd("shell ls", "libifcs")
            port_status = send_cmd(cmd_port_status, "RECIRC")
        if int(port_status.count("DISABLED")) == port_num:
            log.info("set switch %s port disable pass!" % port_num)
        else:
            whitebox_lib.PRINTE("set switch %s port disable fail!" % port_num)


def check_docker_before_sdk():
    """
    author : Janson Jiang
    check docker in sonic before run sdk,if  exist "swss" or "syncd" process,stop it.
    """
    if "swss" or "syncd" in execute_cmd("docker ps"):
        execute_cmd("docker stop syncd")
        execute_cmd("docker stop swss")
        if "swss" and "syncd" not in execute_cmd("docker ps"):
            log.info("Already stop 'swss' and 'syncd' process")


def pre_emphasis_configure():
    """
    author : Janson Jiang
    pre emphasis configure for innovium ic.
    """
    enter_sdk()
    cmd_pre_emphasis = r'source cel_cmds/%s' % pre_emphasis_configure_file
    send_cmd(cmd_pre_emphasis)
    log.info("Pre emphasis configure pass!!!")


def run_loopback_traffic_for_innovium(port_num=15, exp_port_rate=400, test_time=3600, remote=False):
    """
    author : Janson Jiang
    run the sdk traffic for innovium ic with loopback
    :param port_num: port num want to set,int
    :param exp_port_rate:port rate expect,int
    :param test_time: traffic test time ,unit:second
    :param remote: True or False
    """
    if remote:
        send_cls_cmd("ifcs clear counters devport")
        send_cls_cmd("ifcs clear counters hardware")
        send_cls_cmd("diagtest snake config -p 1-%s -lb 'NONE' -v -id 1" % str(port_num))
        port_status = send_cls_cmd("port info")
        start = time.time()
        while time.time() - start <= 60:
            if int(port_status.count("LINK_UP")) >= int(port_num)+1:
                send_cls_cmd("diagtest snake start_traffic -n 500 -s 1518 -id 1 -payload stress")
                log.info("Start traffic!!! ")
                break
        else:
            log.info(str(port_status.count("LINK_UP")))
            log.info(str(port_num))
            whitebox_lib.PRINTE("already wait for 60s,but not %s port link up." % port_num)
        check_sdk_port_rate(exp_port_rate, remote)
        SetWait(test_time)
        send_cls_cmd("diagtest snake stop_traffic -id 1")
        check_sdk_counters(remote)

    else:
        send_cmd("ifcs clear counters devport")
        send_cmd("ifcs clear counters hardware")
        cmd_snake_config = r"diagtest snake config -p 1-%s -lb 'NONE' -v -id 1" % str(port_num)
        send_cmd(cmd_snake_config, "NONE :        1")
        port_status = send_cmd("port info", "RECIRC")
        log.info(port_status)
        start = time.time()
        while time.time() - start <= 60:
            if int(port_status.count("LINK_UP")) >= int(port_num)+1:
                send_cmd("diagtest snake start_traffic -n 500 -s 1518 -id 1 -payload stress")
                log.info("Start traffic!!! ")
                break
        else:
            whitebox_lib.PRINTE("already wait for 60s,but not %s port link up." % port_num)
        send_cmd("shell ls", "libifcs.so")
        check_sdk_port_rate(exp_port_rate, remote)
        SetWait(test_time-6)
        send_cmd("diagtest snake stop_traffic -id 1")
        check_sdk_counters(remote)


def check_sdk_port_rate(exp_port_rate, remote=False):
    """
    author : Janson Jiang
    check all sdk port rate whether meet expectations rate
    :param remote:remote True or Fault
    :param exp_port_rate:unit :G
    """
    dict_port_rate = dict()
    if remote:
        sdk_all_port_info = send_cls_cmd("ifcs show rate devport filter nz")
    else:
        send_cmd("ifcs show rate devport filter nz")
        SetWait(5)
        sdk_all_port_info = device_obj.readMsg()
        log.debug(sdk_all_port_info)
    for line_read in sdk_all_port_info.split("\n"):
        if line_read.count("|") == 8 and "/" not in line_read:
            list_line = line_read.split("|")
            dict_port_rate[list_line[1].strip()] = list_line[6].strip()
            for switch_port in dict_port_rate.keys():
                if not int(exp_port_rate) * 0.9 <= int(float(dict_port_rate[switch_port])) <= int(exp_port_rate) * 1.1:
                    whitebox_lib.PRINTE("port rate test fail!!! port rate is %s,"
                                        "expect rate is %s" % (dict_port_rate[switch_port], exp_port_rate))
                    break
    else:
        log.info("all port rate test pass!!!")


def check_sdk_counters(remote=False):
    """
    author : Janson Jiang
    send command in sdk and check all sdk port counters whether TX/RX Frames Err
    :param remote: True or False
    """
    if remote:
        sdk_all_counters_info = send_cls_cmd("ifcs show counters devport filter nz")
    else:
        send_cmd("ifcs show counters devport filter nz")
        SetWait(10)
        sdk_all_counters_info = device_obj.readMsg()
        log.debug(sdk_all_counters_info)
    for i in sdk_all_counters_info.split("\n"):
        if i.count("|") == 12 and "id" not in i:
            if i.split("|")[4].strip() != "0" or i.split("|")[9].strip() != "0":
                whitebox_lib.PRINTE("Frames Err,%s" % i)
                break
    else:
        log.info("test pass!!! all port counters is normal.")


def check_port_default_status(port_num, exp_port_rate):
    """
    author : Janson Jiang
    check port default status,whether all port is link up.
    :param port_num: port num want to set,int
    :param exp_port_rate:port rate expect,int
    """
    rate_port_num = 0
    port_status = send_cmd("port info", "RECIRC")
    log.info(port_status)
    port_msg_list = port_status.split("\n")
    for read_line in port_msg_list:
        if "ETH" in read_line:
            if read_line.split("|")[11].strip() == "LINK_UP":
                rate_port_num += 1
            if not read_line.split("|")[4].strip().strip("G") == str(exp_port_rate):
                whitebox_lib.PRINTE("port %s speed test fail,not %s" % (read_line.split("|")[1].strip()), exp_port_rate)
                break
    else:
        log.info("all port speed is %s G." % exp_port_rate)
    if rate_port_num == port_num:
        print("check port default status pass,%s of port is link up." % rate_port_num)
    else:
        whitebox_lib("check port default status fail,only %s of port is link up .expect %s" % (rate_port_num, port_num))


def check_link_speed_by_full_test(port_num, exp_port_rate):
    """
    author : Janson Jiang
    check all port link speed whether is up to full speed when full test traffic
    :param port_num: port num want to set,int
    :param exp_port_rate:port rate expect,int
    """
    cmd_snake_config = r"diagtest snake config -p 1-%s -lb 'NONE' -v -id 1" % str(port_num)
    send_cmd(cmd_snake_config, "NONE :        1")
    port_status = send_cmd("port info", "RECIRC")
    log.info(port_status)
    start = time.time()
    while time.time() - start <= 60:
        if int(port_status.count("LINK_UP")) >= int(port_num) + 1:
            send_cmd("diagtest snake start_traffic -n 500 -s 1518 -id 1 -payload stress")
            log.info("Start traffic!!! ")
            break
    else:
        whitebox_lib.PRINTE("already wait for 60s,but not %s port link up." % port_num)
    send_cmd("shell ls", "libifcs.so")
    check_sdk_port_rate(exp_port_rate)


def loopback_info_check(loopback_num, qsfp_vendor, qsfp_pn):
    """
    author : Janson Jiang
    check loopback info,such as loopback num,vendor and pn whether is same
    :param loopback_num: loopback num ,int
    :param qsfp_vendor: loopback vendor,str
    :param qsfp_pn: loopback pn.str
    """
    send_cmd("cd %s" % diag_path)
    if cel_qsfp_test in execute_cmd("ls"):
        qsfp_info = execute_cmd("./%s -a" % cel_qsfp_test)
        if qsfp_info.count("present") == int(loopback_num):
            if qsfp_info.count(qsfp_vendor) == qsfp_info.count(qsfp_pn) == loopback_num:
                log.info("loopback info check pass!!!")
            else:
                whitebox_lib("loopback info check error,get vendor num is %s,get pn num is %s ,expect num is %s"
                             % (str(qsfp_info.count(qsfp_vendor))), str(qsfp_info.count(qsfp_pn)), str(loopback_num))
        else:
            whitebox_lib.PRINTE("loopback num check error,want %s ,but get %s."
                                % (str(loopback_num), str(qsfp_info.count("present"))))
    else:
        whitebox_lib.PRINTE("couldn't find file [%s],please check the diag path and diag file." % cel_qsfp_test)


def run_dac_cable_traffic_for_innovium(port_num=14, exp_port_rate=400, test_time=43200, str_num=1):
    """
    author : Janson Jiang
    run the sdk traffic for innovium ic with dac-cable
    :param port_num: port num want to set,int
    :param exp_port_rate:port rate expect,int
    :param test_time: traffic test time ,unit:second
    :param str_num:num of traffic stream for cpu
    """
    send_cmd("ifcs clear counters devport")
    send_cmd("ifcs clear counters hardware")
    for stream_id in range(1, str_num+1):
        port_list = list()
        for port_id in range(stream_id, port_num+1, str_num):
            port_list.append(port_id)
        port_list.insert(0, port_list[-1])
        port_list.pop()
        port_list_str = [str(port_str) for port_str in port_list]
        port_config_dac = ",".join(port_list_str)
        cmd_snake_config = r"diagtest snake config -p '%s' -lb 'NONE' -v -b2 -id %s" % (port_config_dac, stream_id)
        send_cmd(cmd_snake_config, "NONE :")
    port_status = send_cmd("port info", "RECIRC")
    log.info(port_status)
    start = time.time()
    while time.time() - start <= 60:
        if int(port_status.count("LINK_UP")) == int(port_num)+1:
            for str_id in range(1, str_num+1):
                send_cmd("diagtest snake start_traffic -n 500 -id %s" % str_id)
                log.info("Start traffic id %s!!! " % str_id)
            break
    else:
        whitebox_lib.PRINTE("already wait for 60s,but not %s port link up." % port_num)
    send_cmd("shell ls", "libifcs.so")
    check_sdk_port_rate(exp_port_rate)
    SetWait(test_time-6)
    send_cmd("diagtest snake stop_traffic -id 1")
    check_sdk_counters()


def check_log_info():
    """
    author : Janson Jiang
    execute the script "check_info.sh"  and check the response.
    """
    log_info = execute_cmd("check_info.sh", timeout=300)
    log.info(execute_cmd("dmesg", timeout=300))
    log.info(execute_cmd("cat /var/log/messages.1", timeout=300))
    log.info(execute_cmd("ipmitool sel list", timeout=300))
    if log_info.count("Pass") == 3:
        log.info("check dmesg/message/sel log pass!!!")
    else:
        whitebox_lib.PRINTE("check dmesg/message/sel log fail!!!")


def i2c_diag_stress(hour=12):
    """
    author : Janson Jiang
    run i2c stress
    :param hour: the time for run i2c stres
    :param diag: True for test by diag tool false for test by i2cset/i2cget command
    """
    send_cmd("cd %s" % diag_path)
    start_time = time.time()
    while time.time() - start_time < 3600 * hour:
        log.info(execute_cmd("./cel-cpld-ipmi-test --all"))


def check_sw_main_or_minor(sw):
    """
    author : Janson Jiang
    check whether bmc sw boot from main or minor.
    :param sw :str,"BMC" or "BIOS"or
    """
    if sw == "BMC":
        res_bmc = execute_cmd(bmc_sw_main_minor)
        if "01" in res_bmc:
            log.info("the bmc boot from main sw,test pass!!!")
        else:
            log.info(res_bmc)
            whitebox_lib.PRINTE("the bmc boot not from main sw,test fail!!!")
    if sw == "BIOS":
        res_bios = execute_cmd(bios_sw_main_minor)
        if "01" in res_bios:
            log.info("the bios boot from main sw,test pass!!!")
        else:
            log.info(res_bios)
            whitebox_lib.PRINTE("the bios boot not from main sw,test fail!!!")


def check_res_nums_pass_or_fail(command=check_command, word=key_word,  num=exp_nums):
    res = execute_cmd(command)
    if not res.count(word) == num:
        whitebox_lib.PRINTE("test faill, want %s,but get %s" % (num, res.count(word)))






########################################## Janson End ############################################################
