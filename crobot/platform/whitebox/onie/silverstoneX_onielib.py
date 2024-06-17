###############################################################################
# LEGALESE:   "Copyright (C) 2019-2021, Celestica Corp. All rights reserved." #
#                                                                             #
# This source code is confidential, proprietary, and contains trade           #
# secrets that are the sole property of Celestica Corp.                       #
# Copy and/or distribution of this source code or disassembly or reverse      #
# engineering of the resultant object code are strictly forbidden without     #
# the written consent of Celestica Corp.                                      #
#                                                                             #
###############################################################################
import os
import sys
import re
import time
import Logger
import CRobot
from crobot import Const
from Decorator import *
from crobot.Decorator import logThis

workDir = CRobot.getWorkDir()
sys.path.append(os.path.join(workDir, 'common', 'commonlib'))
sys.path.append(os.path.join(workDir, 'common', 'onie'))
sys.path.append(os.path.join(workDir, 'platform/whitebox'))
import midstone100X_variable
import bios_menu_lib
import OnieVariable
import whitebox_lib
import CommonKeywords
import CommonLib
import YamlParse
from Device import Device

device_obj = Device.getDeviceObject(midstone100X_variable.device_type)
pc_info = YamlParse.getDeviceInfo()["PC"]
pc_ip = pc_info["managementIP"]
pc_user = pc_info["scpUsername"]
pc_password = pc_info["scpPassword"]


@logThis
def exec_cmd(cmd, timeout=60, mode=None):
    try:
        device_obj.sendline("sudo -s")
        device_obj.sendline("cd ")
    except Exception:
        pass
    return whitebox_lib.execute(midstone100X_variable.device_type, cmd, mode=mode, timeout=timeout)


@logThis
def ExeWithoutRule(cmd, check_res=False, keyword=None, timeout=None):
    try:
        device_obj.sendline("sudo -s")
        device_obj.sendline("cd ")
    except Exception:
        pass
    return whitebox_lib.send_cmd_without_return_rule(midstone100X_variable.device_type,
                                                     cmd, check_res, keyword, timeout)


@logThis
def InstallDiagOS(protocol, timeout=600, bin_path="/onie/sonic_bin/"):
    """
    Copy the sonic installation file to the root directory of the corresponding folder for http/tftp installation,
    and finally delete it from the root directory
    :param protocol:http/tftp
    :param timeout:out of time
    :param bin_path: file of bin path
    """
    # onie-nos-install tftp://10.10.10.138/onie-installer.bin
    destination_path = midstone100X_variable.tftp_file_path if protocol.lower() == "tftp" \
        else midstone100X_variable.http_file_path
    if not destination_path.endswith("/"):
        destination_path = destination_path + "/"
    try:
        file_path = whitebox_lib.get_tool_path() + bin_path
        file_name = Device.execute_local_cmd(device_obj, "ls %s" % file_path).strip()

        Device.execute_local_cmd(device_obj, "cp %s%s %sonie-installer.bin" % (file_path, file_name, destination_path))
        cmd = "onie-nos-install %s://%s/onie-installer.bin" % (protocol.lower(), midstone100X_variable.auto_server_ip)
        device_obj.sendCmd(cmd + "\n")
        device_obj.read_until_regexp(midstone100X_variable.diagos_install_msg, timeout=timeout)
        device_obj.read_until_regexp(midstone100X_variable.diagos_install_pass, timeout=int(timeout)-300)
        connect("sonic", 60, 120)
    finally:
        Device.execute_local_cmd(device_obj, "rm -rf %sonie-installer.bin" % destination_path)


@logThis
def UpdateOnie(version, protocol, timeout=1200):
    """
    Upgrade ONIE, eventually still in the update of Onie system
    :param version:new/old
    :param protocol:http/tftp
    :param timeout:time out
    :return:The version of ONIE after the upgrade
    """
    # onie-self-update tftp://10.10.10.138/onie-updater.bin
    update_version = None
    error_str = ""
    destination_path = midstone100X_variable.tftp_file_path if protocol.lower() == "tftp" \
        else midstone100X_variable.http_file_path
    if not destination_path.endswith("/"):
        destination_path = destination_path + "/"
    try:
        file_path = whitebox_lib.get_tool_path() + "/onie/onie_bin/%s/" % version
        file_name = Device.execute_local_cmd(device_obj, "ls %s" % file_path).strip()
        Device.execute_local_cmd(device_obj, "cp %s%s %sonie-updater.bin" % (file_path, file_name, destination_path))
        cmd = "onie-self-update %s://%s/onie-updater.bin" % (protocol.lower(), midstone100X_variable.auto_server_ip)
        device_obj.sendline(cmd)
        output = device_obj.read_until_regexp('ONIE: Success: Firmware update version:', timeout)
        if HasError(output):
            raise RuntimeError('Have error during update onie!')
        device_obj.read_until_regexp('ONIE: Rebooting...', timeout=30)
        output = device_obj.read_until_regexp("will be executed automatically in", 360)
        toTopOnieMenuItem(output)
        time.sleep(1)
        bios_menu_lib.send_key(midstone100X_variable.device_type, "KEY_DOWN", 3)
        bios_menu_lib.send_key(midstone100X_variable.device_type, "KEY_ENTER")
        device_obj.read_until_regexp(OnieVariable.STARTING_DISCOVERY_PROMPT, 200)
        SetWait(10)
        update_version = GetOnieVersion()
    except Exception as E:
        error_str = error_str + "\n%s" % str(E)
    finally:
        Device.execute_local_cmd(device_obj, "rm -rf %sonie-updater.bin" % destination_path)
        if update_version:
            return update_version
        else:
            whitebox_lib.PRINTE("Fail! %s" % error_str)


@logThis
def uninstallOS():
    """
    Uninstall OS
    """
    ExeWithoutRule("reboot")
    output = device_obj.read_until_regexp("will be executed automatically in", 360)
    toTopOnieMenuItem(output)
    time.sleep(1)
    boot_output = ''
    if 'SONiC-OS-' in output:
        bios_menu_lib.send_key(midstone100X_variable.device_type, "KEY_DOWN", 2)
        bios_menu_lib.send_key(midstone100X_variable.device_type, "KEY_ENTER")
        device_obj.read_until_regexp('Uninstall complete.  Rebooting...', 600)
        boot_output = device_obj.read_until_regexp("will be executed automatically in", 360)
    else:
        bios_menu_lib.send_key(midstone100X_variable.device_type, "KEY_ENTER")
    device_obj.read_until_regexp('Starting ONIE Service Discovery', 200)
    connect("onie", 80, 120)
    if 'SONiC-OS-' in boot_output:
        whitebox_lib.PRINTE("Fail! Uninstall OS failed!")


@logThis
def SwitchOnieModeAndCheckOutput(mode):
    """
    Select the rules in Onie's secondary interface: enter different Onie functions
    :param mode:installer/rescue/uninstall/update
    """
    mode = mode.lower()
    ExeWithoutRule("reboot")
    Logger.info("now, will reboot")
    output = device_obj.read_until_regexp("will be executed automatically in", 360)
    toTopOnieMenuItem(output)
    time.sleep(1)

    if mode == 'installer':
        bios_menu_lib.send_key(midstone100X_variable.device_type, "KEY_ENTER")
        out = getOnieBootMsg()
        CommonKeywords.should_match_a_regexp(out, 'ONIE: OS Install Mode ...')
        Logger.info('find word: ONIE: OS Install Mode ...')
        CommonKeywords.should_match_a_regexp(out, 'Version   : ')
        Logger.info('find word: Version   : ')
        CommonKeywords.should_match_a_regexp(out, OnieVariable.INSTALLER_MODE_DETECT_PROMPT)
        Logger.info('find word: ' + OnieVariable.INSTALLER_MODE_DETECT_PROMPT)
        time.sleep(5)
    elif mode == 'rescue':
        bios_menu_lib.send_key(midstone100X_variable.device_type, "KEY_DOWN", 1)
        bios_menu_lib.send_key(midstone100X_variable.device_type, "KEY_ENTER")
        out = getOnieBootMsg()
        CommonKeywords.should_match_a_regexp(out, 'ONIE: Rescue Mode ...')
        Logger.info('find word: ONIE: Rescue Mode ...')
        CommonKeywords.should_match_a_regexp(out, 'Version   : ')
        Logger.info('find word: Version   : ')
        CommonKeywords.should_match_a_regexp(out, OnieVariable.RESCUE_MODE_DETECT_PROMPT)
        Logger.info('find word: ' + OnieVariable.RESCUE_MODE_DETECT_PROMPT)
        if HasError(out):
            whitebox_lib.PRINTE("Fail! have error during boot to onie mode: %s" % mode)
        time.sleep(5)
    elif mode == 'uninstall':
        bios_menu_lib.send_key(midstone100X_variable.device_type, "KEY_DOWN", 2)
        bios_menu_lib.send_key(midstone100X_variable.device_type, "KEY_ENTER")
        out = getOnieBootMsg()
        CommonKeywords.should_match_a_regexp(out, 'ONIE: OS Uninstall Mode ...')
        Logger.info('find word: ONIE: OS Uninstall Mode ...')
        CommonKeywords.should_match_a_regexp(out, 'Version   : ')
        Logger.info('find word: Version   : ')
        CommonKeywords.should_match_a_regexp(out, OnieVariable.UNINSTALL_MODE_DETECT_PROMPT)
        Logger.info('find word: ' + OnieVariable.UNINSTALL_MODE_DETECT_PROMPT)
        time.sleep(5)
    elif mode == 'update':
        bios_menu_lib.send_key(midstone100X_variable.device_type, "KEY_DOWN", 3)
        bios_menu_lib.send_key(midstone100X_variable.device_type, "KEY_ENTER")
        out = getOnieBootMsg()
        CommonKeywords.should_match_a_regexp(out, 'ONIE: ONIE Update Mode ...')
        Logger.info('find word: ONIE: ONIE Update Mode ...')
        CommonKeywords.should_match_a_regexp(out, 'Version   : ')
        Logger.info('find word: Version   : ')
        CommonKeywords.should_match_a_regexp(out, OnieVariable.UPDATE_MODE_DETECT_PROMPT)
        Logger.info('find word: ' + OnieVariable.UPDATE_MODE_DETECT_PROMPT)
        time.sleep(5)


def getOnieBootMsg():
    out = device_obj.read_until_regexp(
        '|'.join([OnieVariable.ACTIVATE_CONSOLE_PROMPT, OnieVariable.STARTING_DISCOVERY_PROMPT]),
        timeout=420)
    device_obj.sendMsg("\n")
    out += device_obj.read_until_regexp(device_obj.promptOnie, timeout=10)
    out = re.sub(midstone100X_variable.ext4_fs_msg, '', out)  # @WORKAROUND avoid ext4_fs_msg break the line
    Logger.cprint(out)
    return out


def toTopOnieMenuItem(output):
    """
    Determine whether sonic is installed according to the string information, and finally enter the Onie system
    :param output:str
    """
    if 'SONiC-OS-' in output:
        Logger.info('SONIC installed.')
        bios_menu_lib.send_key(midstone100X_variable.device_type, "KEY_DOWN")
        bios_menu_lib.send_key(midstone100X_variable.device_type, "KEY_ENTER")
        device_obj.read_until_regexp("ONIE: Embed ONIE", 20)
        Logger.info("Has entered the onie secondary directory")


def keyDown(count):
    for i in range(count):
        device_obj.sendMsg(midstone100X_variable.KEY_DOWN)
        time.sleep(1)


def SetWait(wait_time):
    return whitebox_lib.set_wait(wait_time)


@logThis
def SetRootHostName():
    """
    Switch account to root
    """
    try:
        device_obj.sendline("sudo -s")
        device_obj.sendline("cd /")
    except Exception as E:
        whitebox_lib.PRINTE("Fail! Couldn't Switch to 'root' hostname", decide=False)
        Logger.error(str(E))


@logThis
def connect(os_type="onie", wait_time=180, timeout=300):
    """
    Connect tested product
    :param os_type: 'onie' or other
    :param wait_time: wait some time before connect
    :param timeout: connect out time
    """
    if wait_time:
        SetWait(wait_time)
    start_time = time.time()
    while time.time() - start_time < int(timeout):
        try:
            if os_type.lower() == "onie":
                device_obj.getPrompt("ONIE", timeout=30)
                device_obj.sendCmd("onie-discovery-stop")
            else:
                device_obj.getPrompt("centos", timeout=30)
                SetRootHostName()
                whitebox_lib.check_bmc_ready(midstone100X_variable.device_type)
            break
        except Exception as E:
            Logger.info(str(E))
            SetWait(20)


def HasError(output):
    """
    Check whether there are keywords such as 'error' 'fail' in the string
    :param output:
    :return:
    """
    errors = ['error', 'fail']
    match_one = False
    for error in errors:
        for line in output.splitlines():
            res = re.search(error, line, re.IGNORECASE)
            if res:
                whitebox_lib.PRINTE('Find {} in: {}'.format(error, line))
                match_one = True
    return match_one


@logThis
def RebootToOnieMode(mode, return_version=False):
    """
    Send 'reboot' to ONIE OS
    :param mode: ONIE_UPDATE_MODE/ONIE_RESCUE_MODE/ONIE_INSTALL_MODE
    :param return_version: return onie version or not
    turn_info:if True, will return all information when onie starts
    """
    try:
        device_obj.sendCmd("sudo -s")
        device_obj.sendCmd("cd /")
    except Exception:
        pass
    device_obj.sendCmd("reboot")
    output = device_obj.read_until_regexp("will be executed automatically in", 360)
    toTopOnieMenuItem(output)
    time.sleep(1)
    if mode == midstone100X_variable.ONIE_INSTALL_MODE:
        bios_menu_lib.send_key(midstone100X_variable.device_type, "KEY_ENTER")
        device_obj.read_until_regexp(OnieVariable.STARTING_DISCOVERY_PROMPT, 200)
    elif mode == midstone100X_variable.ONIE_RESCUE_MODE:
        bios_menu_lib.send_key(midstone100X_variable.device_type, "KEY_DOWN", 1)
        bios_menu_lib.send_key(midstone100X_variable.device_type, "KEY_ENTER")
        device_obj.read_until_regexp(OnieVariable.ACTIVATE_CONSOLE_PROMPT, 200)
    elif mode == midstone100X_variable.ONIE_UPDATE_MODE:
        bios_menu_lib.send_key(midstone100X_variable.device_type, "KEY_DOWN", 3)
        bios_menu_lib.send_key(midstone100X_variable.device_type, "KEY_ENTER")
        device_obj.read_until_regexp(OnieVariable.STARTING_DISCOVERY_PROMPT, 200)
    device_obj.sendCmd('')
    device_obj.sendline("onie-discovery-stop")


@logThis
def ShouldHaveNoDiscoveryMessage():
    try:
        device_obj.read_until_regexp(OnieVariable.STARTING_DISCOVERY_PROMPT, timeout=60)
        raise RuntimeError("Find discovery message")
    except Exception:
        pass
    try:
        device_obj.read_until_regexp('Info: Attempting ', timeout=60)
        raise RuntimeError("Find discovery Attempting message")
    except Exception:
        pass


@logThis
def VerifyMacAddress(mac, keyword="HWaddr"):
    current_mac = CommonLib.get_mac_address('DUT', 'eth0', keyword)
    if current_mac != mac:
        raise RuntimeError('verify mac address failed, current mac: {}, expected mac: {}'.format(current_mac, mac))


@logThis
def RestoreMacAddress(mac):
    if mac is None:
        Logger.warning('mac is None!')
        return
    device_obj.runCmd('onie-syseeprom -s 0x24=' + mac)
    RebootToOnieMode(midstone100X_variable.ONIE_RESCUE_MODE)


@logThis
def Get100XToolPath():
    return whitebox_lib.get_tool_path()


@logThis
def GetOSIP(os_type="onie"):
    cmd = "ifconfig" if os_type == "onie" else "sudo -i ifconfig"
    for i in range(3):
        res = whitebox_lib.execute(midstone100X_variable.device_type, cmd)
        os_ip = re.findall(r"inet\s+(\d+\.\d+\.\d+\.\d+)\s+netmask.*broadcast.*", res)
        if os_ip:
            return os_ip[0]
        else:
            os_ip = re.findall(r"inet addr:(\d+\.\d+\.\d+\.\d+)\s+Bcast", res)
            if os_ip:
                return os_ip[0]
        time.sleep(10)
    whitebox_lib.PRINTE("Fail! Couldn't got OS IP!")


@logThis
def CopyFileFromPCToDut(file_name, file_path, destination_path, return_name=False, swap=False):
    """
    Copy file from pc to dut Root directory
    :param file_name:file name
    :param file_path:file path without file name
    :param destination_path:destination path
    :param return_name:if True-return file name
    :param swap:if swap=True, function：copy file from dut to pc
    """
    if swap:
        os_ip = GetOSIP()
        Device.execute_local_cmd(device_obj, "time scp %s/%s %s@%s://%s" % (file_path, file_name, "root", os_ip,
                                                                            destination_path), timeout=120)
        Logger.info("Successfully copy file: %s" % file_name)
    else:
        CommonLib.copy_files_through_scp(midstone100X_variable.device_type, pc_user, pc_password, pc_ip, [file_name],
                                         file_path, destination_path, timeout=120)
    if return_name:
        return file_name


@logThis
def CopyPCSonicToDut(sonic_name=False):
    """
    Copy the sonic installation package from the robot server to the DUT
    :param sonic_name:if True， will return sonic package name
    """
    file_path = Get100XToolPath() + r"/onie/sonic_bin"
    file_name = Device.execute_local_cmd(device_obj, "ls %s" % file_path, timeout=10).strip()
    if sonic_name:
        return CopyFileFromPCToDut(file_name, file_path, midstone100X_variable.dut_snoic_file_path, sonic_name, True)
    else:
        CopyFileFromPCToDut(file_name, file_path, midstone100X_variable.dut_snoic_file_path, sonic_name, True)


@logThis
def InstallSonicLocal():
    """
    Copy the sonic installation package from the robot server to the DUT in the Install mode in Onie, and install it
    """
    sonic_name = CopyPCSonicToDut(True)
    device_obj.sendCmd("onie-nos-install %s" % sonic_name)
    try:
        device_obj.read_until_regexp("reboot: Restarting system", 180)
        Logger.info("Get keyword: 'reboot: Restarting system'")
    except Exception:
        pass
    connect("sonic", 180, 120)
    res = whitebox_lib.execute(midstone100X_variable.device_type, "ipmitool mc info")
    if "Device ID" not in res:
        whitebox_lib.PRINTE("Fail! install sonic by local fail")


@logThis
def SetPduStatus(pdu_status, pdu_port):
    return whitebox_lib.set_pdu_status(midstone100X_variable.device_type, pdu_status, pdu_port)


@logThis
def SetPduStatusConnectOs(os_type, status, port, out_time=300, wait_time=None):
    """
    connec os after pdu send command
    :param os_type:'onie' or other
    :param status:[on,off,reboot]
    :param port:The port number on the PDU of the device under test
    :param out_time:connect os out time
    :param wait_time:Waiting time after operating PDU
    """
    SetPduStatus(status, port)
    connect(os_type, wait_time, timeout=out_time)


@logThis
def SetOnieStaticIp(eth, ip_address):
    """
    Set onie to static IP (recover dynamic IP after restart)
    :param eth:0/1/2/3 ... as eth0, eth1...
    :param ip_address:ip
    """
    cmd = "ifconfig %s %s" % (eth, ip_address)
    for i in range(1, 4):
        exec_cmd(cmd)
        SetWait(10)
        res = exec_cmd("ifconfig")
        if ip_address in res:
            return True
    whitebox_lib.PRINTE("Fail! Set Onie to static ip:%s fail" % ip_address)


@logThis
def GetOnieVersion():
    """
    Get Onie version in onie system
    :return: onie version
    """
    res = exec_cmd("onie-sysinfo -v")
    version = re.findall("\d{4}\.\d{2}\.\d{2}\.(.*)", res)
    if version:
        Logger.info("Get Onie version:%s" % version[0].strip())
        return version[0].strip()
    else:
        whitebox_lib.PRINTE("Fail! Couldn't get Onie version from 'onie-sysinfo -v' response:\n%s" % res)


@logThis
def CheckInfoEqual(info_1, info_2, decide=True):
    return whitebox_lib.check_info_equal(info_1, info_2, decide)


@logThis
def GetOnieTlvValue(code=False):
    """
    Send 'onie-syseeprom' and get the {TLV Name: Value}
    :return: {TLV Name: Value}
    """
    output = CommonLib.execute_command(midstone100X_variable.ONIE_SYSEEPROM_CMD, mode="onie")
    if code:
        info = re.findall(r"(.*)\s+(0x\w+)\s+\d+\s(.*)", output)
    else:
        info = re.findall(r"(.*)\s+0x\w+\s+\d+\s(.*)", output)
    if info:
        info_dict = dict()
        for i in info:
            if code:
                info_dict[i[0].strip()] = [i[1].strip(), i[2].strip()]
            else:
                info_dict[i[0].strip()] = i[1].strip()
        if "Vendor Extension" in info_dict.keys():
            whitebox_lib.PRINTE("Fail! Get error info:[Vendor Extension] by cmd: onie-syseeprom")
        if "CRC-32" in info_dict.keys():
            info_dict.pop("CRC-32")  # Check code, cannot be written
        return info_dict
    else:
        whitebox_lib.PRINTE("Fail! Couldn't get TVL information")


@logThis
def SetTlvWriteProtectionClose():
    """
    The tlv information write protection is turned on by default, and the write protection can be turned off by setting
    """
    start_time = time.time()
    while time.time() - start_time <= 300:
        try:
            device_obj.switchToBmc()
            SetWait(40)
            cmd = "ipmitest mc info"
            res = exec_cmd(cmd, 30, "OPENBMC")
            if "Device ID" in res:
                Logger.info("BMC has ready!")
                break
        except Exception:
            time.sleep(10)
    res_1 = exec_cmd("i2c-test -b 0 --scan", 30, "OPENBMC")
    if "(0x0d" not in res_1:
        whitebox_lib.PRINTE("Fail! cmd:[i2c-test -b 0 --scan] fail.Response:\n%s" % res_1)
    res_2 = exec_cmd("i2c-test -b 0 -s 0x0d -rc 1 -d 0x31", 30, "OPENBMC")
    if "0f" not in res_2:
        whitebox_lib.PRINTE("Fail! cmd:[i2c-test -b 0 -s 0x0d -rc 1 -d 0x31] fail.Response:\n%s" % res_2)
    exec_cmd("i2c-test -b 0 -s 0x0d -w -d 0x31 0x0b", 30, "OPENBMC")
    res_3 = exec_cmd("i2c-test -b 0 --scan", 30, "OPENBMC")
    if "0b" not in res_3:
        whitebox_lib.PRINTE("Fail! cmd:[i2c-test -b 0 --scan] fail.Response:\n%s" % res_3)
    Logger.info("Pass! Set tlv information write protection status close!")
    while time.time() - start_time <= 300:
        try:
            device_obj.trySwitchToCpu()
            cmd = "ipmitest mc info"
            res = exec_cmd(cmd, 30)
            if "ipmitest: not found" in res.strip():
                break
        except Exception:
            time.sleep(10)


@logThis
def SetOnieTlvValue(tlv_dict=midstone100X_variable.error_tlv_value, decide=True):
    """
    Set TLV Value by send 'onie-syseeprom-s code=value'
    :param tlv_dict: dict{tvl name: [code, value]}. e.g:{"Product Name": ["0x21", "Midstone 100X"]} or 'dict{list}'
    :param decide: Whether the information is written successfully
    """
    if isinstance(tlv_dict, str):
        b = re.findall(r'"(.*)": \["(.*)", "(.*)"\]', tlv_dict)
        tlv_dict = dict()
        for i in b:
            tlv_dict[i[0]] = [i[1], i[2]]
    for key, value in tlv_dict.items():
        cmd = "%s -s %s='%s'" % (midstone100X_variable.ONIE_SYSEEPROM_CMD, value[0], value[1])
        exec_cmd(cmd)
        SetWait(2)
    change_info_dict = GetOnieTlvValue(True)
    CheckInfoEqual(tlv_dict, change_info_dict, decide)