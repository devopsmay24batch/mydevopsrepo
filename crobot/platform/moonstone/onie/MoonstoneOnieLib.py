###############################################################################
# LEGALESE:   "Copyright (C) 2019-2020, Celestica Corp. All rights reserved." #
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
import copy
from collections import OrderedDict
import Logger as log
import CRobot
from crobot import Const
from Decorator import *
from time import sleep
from functools import partial
import pexpect


import Const
import time
import MOONSTONECommonLib
import MoonstoneOnieVariable as var
from  MOONSTONECommonLib import powercycle_device
from MoonstoneOnieVariable import *

workDir = CRobot.getWorkDir()
sys.path.append(os.path.join(workDir, 'common', 'commonlib'))
sys.path.append(os.path.join(workDir, 'common', 'onie'))
sys.path.append(os.path.join(workDir, 'platform/moonstone'))
import bios_menu_lib
import OnieVariable
import CommonLib
from common.commonlib import CommonKeywords
from crobot.SwImage import SwImage

try:
    from Device import Device
    import DeviceMgr
except Exception as err:
    log.cprint(str(err))

device = DeviceMgr.getDevice()
run_command = partial(CommonLib.run_command, deviceObj=device, prompt=device.promptDiagOS)

exec_cmd = device.executeCmd

def OnieConnect():
    log.debug("Entering OnieTestCase procedure: OnieConnect")
    device.loginOnie()
    return


def OnieDisconnect():
    global libObj
    log.debug("Entering OnieTestCase procedure: OnieDisconnect")
    device.disconnect()
    return


@logThis
def Switch_ONIE_Mode(mode):
    """
    Select the Onie's interface: enter different Onie functions
    :param mode:installer/rescue/uninstall/update
    """
    time.sleep(10)
    mode = mode.lower()
    device.executeCmd("reboot")
    log.debug("going to onie:{} mode ...".format(mode))
    log.debug("now, rebooting the dut ...")
  
    device.read_until_regexp("Open Network Linux",120)
    time.sleep(1)
    bios_menu_lib.send_key(var.device_type, "KEY_DOWN", 1)
    bios_menu_lib.send_key(var.device_type, "KEY_ENTER", delay=3)
    device.read_until_regexp("GNU GRUB", 10)

    if mode == 'installer':
        log.debug('entering onie install mode ...')
        bios_menu_lib.send_key(var.device_type, "KEY_ENTER", delay=3)
        device.read_until_regexp("ONIE: OS Install Mode", 7)
        time.sleep(30)
        bios_menu_lib.send_key(var.device_type, "KEY_ENTER")
        device.executeCmd("onie-stop")
    elif mode == 'rescue':
        log.debug('entering onie rescue mode ...')
        bios_menu_lib.send_key(var.device_type, "KEY_DOWN", 1)
        bios_menu_lib.send_key(var.device_type, "KEY_ENTER", delay=3)
        device.read_until_regexp("ONIE: Rescue Mode", 7)
        time.sleep(30)
        bios_menu_lib.send_key(var.device_type, "KEY_ENTER")
        device.executeCmd("onie-stop")
    elif mode == 'uninstall':
        log.debug('entering onie uninstall mode ...')
        bios_menu_lib.send_key(var.device_type, "KEY_DOWN", 2)
        bios_menu_lib.send_key(var.device_type, "KEY_ENTER", delay=3)
        device.read_until_regexp("ONIE: OS Uninstall Mode", 7)
        """
        After uninstall device will boot into install mode
        """
        device.read_until_regexp("Uninstall complete", 300) 
        device.read_until_regexp("GNU GRUB", 100)
        log.debug('entering onie install mode ...')
        bios_menu_lib.send_key(var.device_type, "KEY_ENTER", delay=3)
        device.read_until_regexp("ONIE: OS Install Mode", 7)
        time.sleep(30)
        bios_menu_lib.send_key(var.device_type, "KEY_ENTER")
        device.executeCmd("onie-stop")
    elif mode == 'update':
        log.debug('entering onie update mode ...')
        bios_menu_lib.send_key(var.device_type, "KEY_DOWN", 3)
        bios_menu_lib.send_key(var.device_type, "KEY_ENTER", delay=3)
        device.read_until_regexp("ONIE: ONIE Update Mode", 7)
        time.sleep(30)
        bios_menu_lib.send_key(var.device_type, "KEY_ENTER")
        device.executeCmd("onie-stop")



@logThis
def SetOnieStaticIp(eth, ip_address):
    """
    Set onie to static IP (recover dynamic IP after restart)
    :param eth:0/1/2/3 ... as eth0, eth1...
    :param ip_address:ip
    """
    cmd = "ifconfig %s %s" % (eth, ip_address)
    for i in range(1, 4):
        device.executeCmd(cmd)
        time.sleep(10)
        res = exec_cmd("ifconfig")
        if ip_address in res:
            return True
        else:
            raise RuntimeError("Fail! Set Onie to static ip:{} fail".format(ip_address))


@logThis
def CheckOnieDhcpIp():
    """
    Check onie to dhcp IP (get dynamic IP automatically))
    """
    time.sleep(10)
    exec_cmd("ifconfig")
    CommonLib.exec_local_ping(var.tftp_server_ip, 4)


@logThis
def GetOnieVersion():
    """
    Get Onie version in onie system
    :return: onie version
    """
    res = exec_cmd("onie-sysinfo -v")
    res= res.split("-")
    version=res[-2]
    if version:
        log.info("Get Onie version:%s" % version)
        return version
    else:
        raise RuntimeError("Fail! Couldn't get Onie version from 'onie-sysinfo -v' response:\n%s" % res)


@logThis
def ONIEBootLogVersion():
    """
    Get the ONIE Version From the ONIE Boot log
    """
    device.executeCmd("reboot")
    log.debug("now, rebooting the dut ...")

    device.read_until_regexp("Open Network Linux",90)
    time.sleep(1)
    bios_menu_lib.send_key(var.device_type, "KEY_DOWN", 1)
    bios_menu_lib.send_key(var.device_type, "KEY_ENTER", delay=3)
    device.read_until_regexp("GNU GRUB", 10)

    log.debug('entering onie install mode ...')
    bios_menu_lib.send_key(var.device_type, "KEY_ENTER", delay=3)
    output = device.read_until_regexp("Build Date.*", 5)
    time.sleep(30)
    bios_menu_lib.send_key(var.device_type, "KEY_ENTER")
    device.executeCmd("onie-stop")
    pass_count = 0
    log.debug("version log ----  {}".format(output))
    for lines in output.splitlines():
        log.debug("each loop-->{}".format(lines))
        if ("Version" in lines):
            pass_count += 1 
            log.info("Version is present in ONIE Booting:\n{}".format(lines))
            return version
        else:
            continue
    if (pass_count == 0):
        raise RuntimeError("Fail! Couldn't get Onie version in Onie booting log.")


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
            if res and not re.search('No error reported',line, re.IGNORECASE):
                log.fail('Find {} in: {}'.format(error, line))
                match_one = True
    return match_one


@logThis
def UpdateOnie(version, protocol, timeout=120):
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
    log.debug("check the ONIE version ,Image provided : {} and {} ".format(var.version, var.ONIEimage))
    if (protocol == 'tftp'):
        cmd = "onie-self-update %s://%s/%s" % (protocol.lower(), var.tftp_server_ip, var.ONIEimage)
    else:
        cmd = "onie-self-update %s://%s/%s" % (protocol.lower(), var.http_server_ip, var.ONIEimage)
    device.sendline(cmd)
    output = device.read_until_regexp('ONIE: Success: Firmware update version:', timeout)
    if HasError(output):
        log.fail('Have error during update onie!')
    device.read_until_regexp('ONIE: Rebooting...', timeout=30)
    device.read_until_regexp("Open Network Linux",90)
    time.sleep(1)
    bios_menu_lib.send_key(var.device_type, "KEY_DOWN", 1)
    bios_menu_lib.send_key(var.device_type, "KEY_ENTER", delay=3)
    device.read_until_regexp("GNU GRUB", 10)
    time.sleep(1)
    bios_menu_lib.send_key(var.device_type, "KEY_DOWN", 3)
    bios_menu_lib.send_key(var.device_type, "KEY_ENTER", delay=3)
    device.read_until_regexp("ONIE: ONIE Update Mode", 7)
    time.sleep(30)
    bios_menu_lib.send_key(var.device_type, "KEY_ENTER", delay=3)

    update_version = GetOnieVersion()
    if update_version:
        return update_version
    else:
        raise RuntimeError("Fail! %s" % error_str)


@logThis
def InstallDiagOS(version, protocol, timeout=600):
    """
    Update ONL OS
    :param protocol:http/tftp
    :param timeout:out of time
    :param bin_path: file of bin path
    """
    update_version = None
    error_str = ""
    log.debug("check the ONL version ,Image provided : {} and {} ".format(var.ONLversion, var.ONLimage))
    if (protocol == 'tftp'):
        cmd = "onie-nos-install %s://%s/%s" % (protocol.lower(), var.tftp_server_ip, var.ONLimage)
    else:
        cmd = "onie-nos-install %s://%s/%s" % (protocol.lower(), var.http_server_ip, var.ONLimage)
    device.sendline(cmd)
    output = device.read_until_regexp('ONL loader install successful.', timeout)
    device.read_until_regexp('Rebooting in 3s', timeout=30)
    device.read_until_regexp("Open Network Linux",90)
    bios_menu_lib.send_key(var.device_type, "KEY_ENTER", delay=3)
    device.read_until_regexp("localhost login",90)
    if HasError(output):
        log.fail('Have error during ONL Install!')
    device.loginDiagOS()

@logThis
def GetONLVersion():
    output = device.getPrompt()
    log.debug("Current Prompt: {}".format(output))
    if re.search("ONIE", output):
        exec_cmd('reboot')
        log.debug("entering into ONL ...")
        device.read_until_regexp("localhost login:", 90)
        device.loginDiagOS()
    res=''
    res=exec_cmd('cat /etc/issue')
    res=res.replace(',', '')
    res= res.split(" ")
    Img=res[8]
    Img=Img.split('\r')[0]
    if(Img == var.ONLversion):
        return Img
    else:
        raise RuntimeError("Fail! ONL {} is not updated to {}!".format(var.ONLversion,Img))


@logThis
def Disable_write_protect():
    #NEw release will have the i2c set command for write protect enable and disable
    device.switchToBmc()
    device.executeCmd("i2cset -f -y 2 0x0d 0x31 0x0B")
    device.switchToCpu()

@logThis 
def Enable_write_protect():
    #New ONIE release will have the i2c set command for write protect enable and disable
    device.switchToBmc()
    device.executeCmd("i2cset -f -y 2 0x0d 0x31 0x0F")
    device.switchToCpu()


@logThis
def Burn_EEPROM():
    device.executeCmd("onie-syseeprom -s 0x21=Moonstone")
    device.executeCmd("onie-syseeprom -s 0x22=R4028-F9001-01")
    device.executeCmd("onie-syseeprom -s 0x23=R4028F2B143628GD200025")
    device.executeCmd("onie-syseeprom -s 0x24=00:A0:C9:08:02:16")
    device.executeCmd("onie-syseeprom -s 0x25='17/07/2023 14:30:00'")
    device.executeCmd("onie-syseeprom -s 0x26=10")
    device.executeCmd("onie-syseeprom -s 0x27=Moonstone")
    device.executeCmd("onie-syseeprom -s 0x28=DS5000")
    device.executeCmd("onie-syseeprom -s 0x29=2023.10")
    device.executeCmd("onie-syseeprom -s 0x2a=4")
    device.executeCmd("onie-syseeprom -s 0x2b=CELESTICA")
    device.executeCmd("onie-syseeprom -s 0x2c=CHN")
    device.executeCmd("onie-syseeprom -s 0x2d=CELESTICA")
    device.executeCmd("onie-syseeprom -s 0x2e=2.1.0")


@logThis
def Read_EEPROM():
    """
    Send 'onie-syseeprom' and get the {TLV Name: Value}
    :return: {TLV Name: Value}
    """
    output = device.executeCmd(var.ONIE_SYSEEPROM_CMD)
    info = re.findall(r"(.*)\s+0x\w+\s+\d+\s(.*)", output)
    if info:
        info_dict = dict()
        for i in info:
            info_dict[i[0].strip()] = i[1].strip()
        if "CRC-32" in info_dict.keys():
            info_dict.pop("CRC-32")  # Check code, cannot be written
        return info_dict
    else:
        raise RuntimeError("Fail! Couldn't get TVL information")


@logThis
def StabilityOnieRun():
    log.debug("going to onie:install mode ...")
    log.debug("now, rebooting the dut ...")
    device.sendCmd("reboot")

    device.read_until_regexp("Open Network Linux",90)
    time.sleep(1)
    bios_menu_lib.send_key(var.device_type, "KEY_DOWN", 1)
    bios_menu_lib.send_key(var.device_type, "KEY_ENTER", delay=3)
    device.read_until_regexp("GNU GRUB", 10)
    
    log.debug('entering onie install mode ...')
    bios_menu_lib.send_key(var.device_type, "KEY_ENTER", delay=3)
    device.read_until_regexp("ONIE: OS Install Mode", 7)
    time.sleep(10)
    output=device.executeCmd("onie-start")
    log.info('Change the sleep time here ...')
    log.info('    based  on how long onie-discovery has to run for stability check')
    time.sleep(10)
    bios_menu_lib.send_key(var.device_type, "KEY_ENTER")
    if HasError(output):
        log.fail('Have error in onie-discovery!')
    device.executeCmd("onie-stop\r")

    output = device.getPrompt()
    log.debug("Current Prompt: {}".format(output))
    if re.search("ONIE", output):
        log.info("onie-stop command  successfull")
    else:
        raise RuntimeError("onie-stop command failed!") 
