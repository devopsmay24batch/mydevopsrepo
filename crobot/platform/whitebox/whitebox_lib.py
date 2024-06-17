###############################################################################
# LEGALESE:   "Copyright (C) 2019-2020, Celestica Corp. All rights reserved." #
#                                                                             #
# This source code is confidential, proprietary, and contains trade           #
# secrets that are the sole property of Celestica Corp.                       #
# Copy and/or distribution of this source code or disassembly or reverse      #
# engineering of the resultant object code are strictly forbidden without     #
# engineering of the resultant object code are strictly forbidden without     #
# the written consent of Celestica Corp.                                      #
#                                                                             #
###############################################################################
import re
from inspect import getframeinfo, stack
import os.path
import time
import yaml
import Logger as log
import CommonLib
import random
import Const
import openbmc_lib
import Const
import YamlParse
import Logger as log
import pexpect
import getpass
import os
import traceback
import parser_openbmc_lib
import json
from BIOS_variable import *
from BMC_variable import *
from datetime import datetime, timedelta
from dataStructure import nestedDict, parser
from errorsModule import noSuchClass, testFailed
from SwImage import SwImage
from Server import Server
from pexpect import pxssh
import sys
import getpass
import WhiteboxLibAdapter

try:
    import parser_openbmc_lib as parserOpenbmc
    import DeviceMgr
    from Device import Device

except Exception as err:
    log.cprint(str(err))

deviceObj = DeviceMgr.getDevice()


def get_tool_path(file_name="midstone100X"):
    path_1 = os.getcwd()
    path_2 = path_1.split("/")
    path_2.pop()
    path_list = path_2 + ["platform/whitebox/tool/%s" % file_name]
    tool_path = "/".join(path_list)
    return tool_path


def PRINTE(*agr, decide=True):
    """
    Log output as an error stream and throw an exception
    :param agr: error description
    :param decide: if True,throw an exception
    Author Yagami
    """
    error_fun_name = stack()[1][3]
    log.error(*agr)
    if decide:
        raise RuntimeError("[%s]: Fail! Function Name:%s" % (datetime.now(), error_fun_name))


def execute(device, cmd, mode=None, timeout=60):
    log.debug('Entering Device execute with args : %s\n' % (str(locals())))
    deviceObj = Device.getDeviceObject(device)
    if mode != None:
        deviceObj.getPrompt(mode, timeout)
    cmd = 'time ' + cmd
    return deviceObj.sendCmdRegexp(cmd, Const.TIME_REG_PROMPT, timeout)


def mkdir_data_path(device, path, local=False):
    log.debug('Entering procedure mkdir_data_path with args : %s\n' % (str(locals())))
    cmd = 'mkdir -p ' + path
    if local:
        device_obj = Device.getDeviceObject(device)
        res = Device.execute_local_cmd(device_obj, cmd)
        log.info(res)
    else:
        res = execute(device, cmd, CENTOS_MODE)
        log.info(res)


def update_whitebox_bios(device, toolname, device_type, username=None, hostip=None, password=None, \
                         bmcip=None, isUpgrade=True, local=True, bmcusername='admin', bmcpassword='admin'):
    ###ipmitool_cmd(power cycle|power reset|power on)
    log.debug('Entering procedure update_whitebox_bios with args : %s\n' % (str(locals())))
    deviceObj = Device.getDeviceObject(device)
    imageObj = SwImage.getSwImage(SwImage.BIOS)
    device_version = {}
    device_version['BIOS_Version'] = imageObj.newVersion if isUpgrade else imageObj.oldVersion
    if not need_update_FW('DUT', device_type, device_version):
        log.info("Already at version " + device_version['BIOS_Version'] + ", no need update.")
        return
    online_update_bios(device, toolname, username, hostip, password, bmcip, isUpgrade, local, bmcusername, bmcpassword)
    time.sleep(10)


def update_whitebox_bmc(device, toolname, device_type, username=None, hostip=None, password=None, \
                        bmcip=None, isUpgrade=True, local=True, bmcusername='admin', bmcpassword='admin'):
    log.debug('Entering procedure update_whitebox_bmc with args : %s\n' % (str(locals())))
    deviceObj = Device.getDeviceObject(device)
    imageObj = SwImage.getSwImage(SwImage.BMC)
    device_version = {}
    device_version['BMC_Version'] = imageObj.newVersion if isUpgrade else imageObj.oldVersion
    if not need_update_FW('DUT', device_type, device_version):
        log.info("Already at version " + device_version['BMC_Version'] + ", no need update.")
        return
    online_update_bmc(device, toolname, username, hostip, password, bmcip, isUpgrade, local, bmcusername, bmcpassword)
    time.sleep(90)


def update_whitebox_bmc_force(device, toolname, device_type, username=None, hostip=None, password=None, \
                              bmcip=None, isUpgrade=True, local=True, bmcusername='admin', bmcpassword='admin'):
    log.debug('Entering procedure update_whitebox_bmc_force with args : %s\n' % (str(locals())))
    deviceObj = Device.getDeviceObject(device)
    imageObj = SwImage.getSwImage(SwImage.BMC)
    device_version = {}
    device_version['BMC_Version'] = imageObj.newVersion if isUpgrade else imageObj.oldVersion
    online_update_bmc(device, toolname, username, hostip, password, bmcip, isUpgrade, local, bmcusername, bmcpassword)
    time.sleep(90)


def get_sw_image_hostImageDir(device, swimage_type='BMC'):
    log.debug('Entering procedure get_sw_image_hostImageDir with args : %s\n' % (str(locals())))
    deviceObj = Device.getDeviceObject(device)
    if swimage_type == 'BMC':
        imageObj = SwImage.getSwImage(SwImage.BMC)
    elif swimage_type == 'BIOS':
        imageObj = SwImage.getSwImage(SwImage.BIOS)
    else:
        raise testFailed("Failure get_sw_image_hostImageDir")
    return imageObj.hostImageDir


def get_sw_image_localImageDir(device, swimage_type='BMC'):
    log.debug('Entering procedure get_sw_image_localImageDir with args : %s\n' % (str(locals())))
    deviceObj = Device.getDeviceObject(device)
    if swimage_type == 'BMC':
        imageObj = SwImage.getSwImage(SwImage.BMC)
    elif swimage_type == 'BIOS':
        imageObj = SwImage.getSwImage(SwImage.BIOS)
    else:
        raise testFailed("Failure get_sw_image_hostImageDir")
    return imageObj.localImageDir


def get_sw_image_version(device, swimage_type='BMC', isUpgrade=True):
    log.debug('Entering procedure get_sw_image_version with args : %s\n' % (str(locals())))
    deviceObj = Device.getDeviceObject(device)
    device_version = {}
    if swimage_type == 'BMC':
        imageObj = SwImage.getSwImage(SwImage.BMC)
        device_version['BMC_Version'] = imageObj.newVersion if isUpgrade else imageObj.oldVersion
    elif swimage_type == 'BIOS':
        imageObj = SwImage.getSwImage(SwImage.BIOS)
        device_version['BIOS_Version'] = imageObj.newVersion if isUpgrade else imageObj.oldVersion
    else:
        raise testFailed("Failure get_sw_image_hostImageDir")
    return device_version


def get_username_from_config(device):
    log.debug('Entering get_username_from_config with args : %s' % (str(locals())))
    deviceInfo = YamlParse.getDeviceInfo()
    deviceDict = deviceInfo[device]
    return deviceDict['rootUserName']


def get_password_from_config(device):
    log.debug('Entering get_password_from_config with args : %s' % (str(locals())))
    deviceInfo = YamlParse.getDeviceInfo()
    deviceDict = deviceInfo[device]
    return deviceDict['rootPassword']


def get_managementIP_from_config(device):
    log.debug('Entering get_password_from_config with args : %s' % (str(locals())))
    deviceInfo = YamlParse.getDeviceInfo()
    deviceDict = deviceInfo[device]
    return deviceDict['managementIP']


def power_cycle_os_by_ipmitool(device, username=None, hostip=None, password=None, bmcip=None, ipmitool_cmd=None,
                               mode='remote', bmcusername='admin', bmcpassword='admin'):
    ###mode(remote|local)
    log.debug("Entering power_cycle_os_by_ipmitool with args : %s" % (str(locals())))
    deviceObj = Device.getDeviceObject(device)
    pass_message = 'Chassis Power Control:'
    if mode == 'local':
        cmd = "time ipmitool %s" % (ipmitool_cmd)
        output = deviceObj.sendCmdRegexp(cmd, Const.TIME_REG_PROMPT, timeout=20)
        print(output)
    else:
        cmd = "ipmitool -H %s -U %s -P %s %s" % (bmcip, bmcusername, bmcpassword, ipmitool_cmd)
        child = ssh_command(username, hostip, password, cmd)
        child.expect(pexpect.EOF, timeout=180)
        output = child.before.strip().decode('utf-8')
        print(output)
    match = re.search(pass_message, output)
    if match:
        log.info("Successfully power on OS")
    else:
        log.info("fail to power on OS")
        raise RuntimeError("power_cycle_os_by_ipmitool FAIL")


def online_update_bios(device, toolname, username, hostip, password, bmcip, isUpgrade, local, bmcusername, bmcpassword):
    log.debug('Entering procedure online_update_bios with args : %s\n' % (str(locals())))
    imageObj = SwImage.getSwImage('BIOS')
    deviceObj = Device.getDeviceObject(device)
    if local:
        tool_path = get_sw_image_localImageDir(device, swimage_type='BIOS')
    else:
        tool_path = get_sw_image_hostImageDir(device, swimage_type='BIOS')
    p2 = "Cannot access"
    pass_message = 'Verifying Firmware Image : 100%... done'
    err_count = 0
    timeout = 500
    if device == 'DUT':
        deviceObj.getPrompt(CENTOS_MODE)
    if device == 'PC':
        pass
    if isUpgrade:
        package_file = imageObj.newImage
    else:
        package_file = imageObj.oldImage
    if local:
        cmd1 = 'time ' + tool_path + '/' + toolname + ' -cd -d 2 ' + tool_path + '/' + package_file + ' -fb'
        output = deviceObj.sendCmdRegexp(cmd1, Const.TIME_REG_PROMPT, timeout)
        log.cprint(str(output))
        match = re.search(pass_message, output)
        match2 = re.search(p2, output)
        if match:
            log.info("Successfully online_update_bios")
        elif match2:
            log.fail("Cannot access image file")
            err_count += 1
    else:
        cmd1 = 'time ' + tool_path + '/' + toolname + ' -nw -ip ' + bmcip + ' -u ' + bmcusername + ' -p ' \
               + bmcpassword + ' -d 2 ' + tool_path + '/' + package_file + ' -fb'
        print(cmd1)
        child = ssh_command(username, hostip, password, cmd1)
        child.expect(pexpect.EOF, timeout=500)
        output = child.before.strip().decode('utf-8')
        print(output)
        match = re.search(pass_message, output)
        match2 = re.search(p2, output)
        if match:
            log.info("Successfully remote_online_update_bios")
        else:
            log.fail("Cannot remote access image file")
            err_count += 1
    if err_count:
        raise testFailed("Failure online_update_bios")


def online_update_bmc(device, toolname, username=None, hostip=None, password=None, bmcip=None, isUpgrade=True,
                      local=True, \
                      bmcusername=None, bmcpassword=None):
    log.debug('Entering procedure online_update_bmc with args : %s\n' % (str(locals())))
    imageObj = SwImage.getSwImage('BMC')
    deviceObj = Device.getDeviceObject(device)
    if local:
        tool_path = get_sw_image_localImageDir(device, swimage_type='BMC')
    else:
        tool_path = get_sw_image_hostImageDir(device, swimage_type='BMC')
    p2 = "Cannot access"
    pass_message = 'Resetting the firmware'
    err_count = 0
    timeout = 800
    if device == 'DUT':
        deviceObj.getPrompt(CENTOS_MODE)
    if device == 'PC':
        pass
    if isUpgrade:
        package_file = imageObj.newImage
    else:
        package_file = imageObj.oldImage
    if local:
        cmd1 = 'time ' + tool_path + '/' + toolname + ' -cd ' + tool_path + '/' + package_file + ' -mse 3 -ieo -fb'
        output = deviceObj.sendCmdRegexp(cmd1, Const.TIME_REG_PROMPT, timeout)
        log.cprint(str(output))
        match = re.search(pass_message, output)
        match2 = re.search(p2, output)
        if match:
            log.info("Successfully online_update_bmc")
        elif match2:
            log.fail("Cannot access image file")
            err_count += 1
    else:
        cmd1 = 'time ' + tool_path + '/' + toolname + ' -nw -ip ' + bmcip + ' -u ' + bmcusername + ' -p ' \
               + bmcpassword + ' ' + tool_path + '/' + package_file + ' -mse 3 -ieo -fb -pc'
        print(cmd1)
        child = ssh_command(username, hostip, password, cmd1)
        child.expect(pexpect.EOF, timeout)
        output = child.before.strip().decode('utf-8')
        match = re.search(pass_message, output)
        match2 = re.search(p2, output)
        if match:
            log.info("Successfully remote_online_update_bmc")
        else:
            log.fail("Cannot remote access image file")
            err_count += 1
    if err_count:
        raise testFailed("Failure remote_online_update_bmc")


def verify_bios_version(device, bios_version=None):
    ### dmidecode --s bios-version
    log.debug('Entering procedure verify_bios_version with args : %s\n' % (str(locals())))
    if bios_version is None:
        bios_version = get_version_from_config('BIOS')
    err_count = 0
    cmd = 'dmidecode --s bios-version'
    output = execute(device, cmd, mode=CENTOS_MODE)
    log.cprint(output)
    p1 = r'time.+\n(\S+)'
    match = re.search(p1, output)
    if match:
        if bios_version != None:
            BIOS_version = match.group(1).strip()
            if BIOS_version == bios_version:
                log.info("Successfully verify_BIOS_version: %s" % (BIOS_version))
            else:
                log.error("BIOS_version mismatch: %s, %s" % (BIOS_version, bios_version))
                err_count += 1
    else:
        log.error("Fail to parse BIOS_version")
        err_count += 1
    if err_count:
        raise RuntimeError('verify_BIOS_version')


def verify_fw_version(device, device_type, device_version=None, isUpgrade=True):
    log.debug('Entering procedure verify_fw_version with args : %s\n' % (str(locals())))
    err_count = 0
    deviceObj = Device.getDeviceObject(device)
    device_version = {}
    if device_version is None:
        device_version = get_version_from_config(device_type)
    if device_type.upper() == "BMC":
        cmd = 'ipmitool mc info'
        output = execute(device, cmd, mode=CENTOS_MODE)
        parsed_output = parse_bmc_version(output)
        imageObj = SwImage.getSwImage(SwImage.BMC)
        device_version['BMC_Version'] = imageObj.newVersion if isUpgrade else imageObj.oldVersion
    elif device_type.upper() == 'BIOS':
        cmd = 'dmidecode --s bios-version'
        output = execute(device, cmd, mode=CENTOS_MODE)
        parsed_output = parse_bios_version(output)
        imageObj = SwImage.getSwImage(SwImage.BIOS)
        device_version['BIOS_Version'] = imageObj.newVersion if isUpgrade else imageObj.oldVersion
    err_count += CommonLib.compare_input_dict_to_parsed(parsed_output, device_version)
    if err_count:
        raise testFailed("Failure while verify_fw_version with result FAIL")


def parse_bmc_version(output):
    log.debug('Entering procedure parse_bmc_version with args : %s\n' % (str(locals())))
    outDict = parser()
    p1 = r'Firmware Revision\s+:\s+(\S+)'
    for line in output.splitlines():
        line = line.strip()
        match = re.search(p1, line)
        if match:
            outDict['BMC_Version'] = match.group(1)
            break
    log.info(outDict)
    return outDict


def parse_bios_version(output):
    log.debug('Entering procedure parse_bios_version with args : %s\n' % (str(locals())))
    outDict = parser()
    p1 = r'time.+\n(\S+)'
    match = re.search(p1, output)
    if match:
        outDict['BIOS_Version'] = match.group(1)
    #        break
    log.info(outDict)
    return outDict


def reboot_os(device):
    log.debug('Entering procedure reboot : %s\n ' % (str(locals())))
    deviceObj = Device.getDeviceObject(device)
    deviceObj.sendline("reboot")
    time.sleep(5)


def need_update_FW(device, device_type, device_version):
    log.debug('Entering procedure need_update_FW with args : %s\n' % (str(locals())))
    deviceObj = Device.getDeviceObject(device)
    deviceObj.flush()
    err_count = 0
    if device_type.upper() == "BMC":
        cmd = 'ipmitool mc info'
        output = execute(device, cmd)
        pattern = device_version['BMC_Version']
        match = re.search(pattern, output)
        if match:
            pass
        else:
            err_count += 1
    elif device_type.upper() == 'BIOS':
        cmd = 'dmidecode --s bios-version'
        output = execute(device, cmd)
        pattern = device_version['BIOS_Version']
        match = re.search(pattern, output)
        if match:
            pass
        else:
            err_count += 1
        # key = 'BIOS Version'
    return True if err_count > 0 else False


def copy_files_from_pc_to_os(device, username, password, server_ip, filename, filepath, destination_path, size_MB,
                             swap=False, ipv6=False, interface='None'):
    """
    if swap=True, function：copy file from dut to pc
    """
    log.debug('Entering procedure copy_files_from_pc_to_os : %s\n' % (str(locals())))
    mode = CENTOS_MODE
    ### assume avg speed is 0.5MB/s
    timeout = int(size_MB) * 3
    filelist = [filename]
    CommonLib.copy_files_through_scp(device, username, password, server_ip, filelist, \
                                     filepath, destination_path, CENTOS_MODE, swap, False, interface, timeout)


def chmod_file(device, filename):
    cmd1 = 'chmod 777 ' + filename
    cmd2 = 'ls -al ' + filename
    execute(device, cmd1)
    output = execute(device, cmd2)
    p = '-rwxrwxrwx'
    match = re.search(p, output)
    if match:
        log.info("Successfully chmod_file")
    else:
        log.fail("chmod_file failed")
        raise testFailed("chmod_file failed")


def delete_folder(device, path):
    log.debug("Entering delete_folder with args : %s" % (str(locals())))
    cmd = 'rm -rf ' + path
    execute(device, cmd)


def verify_bmc_product_id(device, expected_result=None):
    log.debug("Entering verify_bmc_product_id with args : %s" % (str(locals())))
    deviceObj = Device.getDeviceObject(device)
    err_count = 0
    cmd = "ipmitool mc info"
    p1 = r'Product ID\s+:\s+(\d+)\s+\S+'
    output = execute(device, cmd, mode=CENTOS_MODE)
    log.cprint(output)
    match = re.search(p1, output)
    if match:
        if expected_result != None:
            product_id = match.group(1).strip()
            if product_id == expected_result:
                log.info("Successfully verify_bmc_product_id: %s" % (product_id))
            else:
                log.error("bmc_product_id mismatch: %s, %s" % (product_id, expected_result))
                err_count += 1
    else:
        log.error("Fail to parse bmc_product_id")
        err_count += 1
    if err_count:
        raise RuntimeError('verify_bmc_product_id')


def verify_bmc_mac_address(device, cmd, expected_result=None):
    log.debug('Entering procedure verify_mac_address with args : %s\n' % (str(locals())))
    err_count = 0
    p1 = r'MAC Address\s+:\s(.+)'
    try:
        output = execute(device, cmd)
        log.cprint(output)
        match = re.search(p1, output)
        if match:
            if expected_result != None:
                mac_addr = match.group(1).strip()
                if mac_addr == expected_result:
                    log.info("Successfully verify bmc mac address: %s" % (mac_addr))
                else:
                    log.error("BMC mac address mismatch: %s, %s" % (mac_addr, expected_result))
                    err_count += 1
        else:
            log.error("Fail to parse bmc mac adrress")
            err_count += 1
        if err_count:
            raise RuntimeError('verify_bmc_mac_address')
    except:
        raise RuntimeError('verify_bmc_mac_address')


def verify_bmc_voltage_sensor(device):
    log.debug('Entering procedure verify_bmc_voltage_sensor with args : %s\n' % (str(locals())))
    #    deviceObj = Device.getDeviceObject(device)
    err_count = 0
    cmd = 'ipmitool sdr list'
    output = execute(device, cmd)
    log.cprint(output)
    p1 = r'(\S+Volt)\s+\W\s(.+)\s+\W\s(\S+)'
    match = re.findall(p1, output)
    if match:
        for index in range(len(match)):
            if match[index][2] != 'ok':
                err_count += 1
                log.info("%s %s %s is abnormal" % (match[index][0], match[index][1], match[index][2]))
    else:
        err_count += 1
        log.error("Fail to parse verify_bmc_voltage_sensor")
    if err_count:
        raise RuntimeError('verify_bmc_voltage_sensor')


def verify_bmc_tmp_sensor(device):
    log.debug('Entering procedure verify_bmc_tmp_sensor with args : %s\n' % (str(locals())))
    #    deviceObj = Device.getDeviceObject(device)
    err_count = 0
    cmd = 'ipmitool sdr list'
    output = execute(device, cmd)
    log.cprint(output)
    p1 = r'(\S+Temp\S+)\s+\W\s(.+)\s+\W\s(\S+)'
    p2 = r'(\S+Temp)\s+\W\s(.+)\s+\W\s(\S+)'
    match1 = re.findall(p1, output)
    match2 = re.findall(p2, output)
    match = match1 + match2
    if match:
        for index in range(len(match)):
            if match[index][2] != 'ok':
                err_count += 1
                log.info("%s %s %s is abnormal" % (match[index][0], match[index][1], match[index][2]))
    else:
        err_count += 1
        log.error("Fail to parse verify_bmc_tmp_sensor")
    if err_count:
        raise RuntimeError('verify_bmc_tmp_sensor')


def verify_bmc_version(device, expected_result=None):
    log.debug('Entering procedure verify_bmc_version with args : %s\n' % (str(locals())))
    err_count = 0
    cmd = 'ipmitool mc info'
    output = execute(device, cmd, mode=CENTOS_MODE)
    log.cprint(output)
    p1 = r'Firmware Revision\s+:\s+(\S+)'
    match = re.search(p1, output)
    if match:
        if expected_result != None:
            BMC_version = match.group(1).strip()
            if BMC_version == expected_result:
                log.info("Successfully verify_bmc_version: %s" % (BMC_version))
            else:
                log.error("bmc_version mismatch: %s, %s" % (BMC_version, expected_result))
                err_count += 1
    else:
        log.error("Fail to parse bmc_version")
        err_count += 1
    if err_count:
        raise RuntimeError('verify_bmc_version')


def verify_bmc_manufacturer_id(device, expected_result=None):
    log.debug('Entering procedure verify_bmc_manufacturer_id with args : %s\n' % (str(locals())))
    err_count = 0
    cmd = 'ipmitool mc info'
    output = execute(device, cmd, mode=CENTOS_MODE)
    log.cprint(output)
    p1 = r'Manufacturer ID\s+:\s+(\S+)'
    match = re.search(p1, output)
    if match:
        if expected_result != None:
            Manufacturer_ID = match.group(1).strip()
            if Manufacturer_ID == expected_result:
                log.info("Successfully verify_bmc_manufacturer_id: %s" % (Manufacturer_ID))
            else:
                log.error("BMC_Manufacturer_ID: %s, %s" % (Manufacturer_ID, expected_result))
                err_count += 1
    else:
        log.error("Fail to parse BMC_Manufacturer_ID")
        err_count += 1
    if err_count:
        raise RuntimeError('verify_bmc_manufacturer_id')


def check_mac_address(device, interface, expected_result=None):
    ### ifconfig [interface]
    log.debug('Entering procedure check_mac_address with args : %s\n' % (str(locals())))
    deviceObj = Device.getDeviceObject(device)
    err_count = 0
    cmd = 'ifconfig %s' % (interface)
    p = r'ether .* .*'
    p1 = r'ether (\S+)'
    try:
        output = deviceObj.sendCmdRegexp(cmd, p, 9)
        log.cprint(output)
        match = re.search(p1, output)
        if match:
            if expected_result != None:
                mac_addr = match.group(1).strip()
                if mac_addr == expected_result:
                    log.info("Successfully check mac address: %s" % (mac_addr))
                else:
                    log.error("Mac address mismatch: %s, %s" % (mac_addr, expected_result))
                    err_count += 1
        else:
            log.error("Fail to parse mac adrress")
            err_count += 1
        if err_count:
            raise RuntimeError('check_mac_address')
    except:
        raise RuntimeError('check_mac_address')


def verify_bmc_uuid(device, expected_result=None):
    log.debug('Entering procedure verify_bmc_uuid with args : %s\n' % (str(locals())))
    err_count = 0
    cmd = 'dmidecode -t 1'
    output = execute(device, cmd, mode=CENTOS_MODE)
    log.cprint(output)
    p1 = r'UUID:\s+(\S+)'
    match = re.search(p1, output)
    if match:
        if expected_result != None:
            BMC_UUID = match.group(1).strip()
            if BMC_UUID == expected_result:
                log.info("Successfully verify_bmc_uuid: %s" % (BMC_UUID))
            else:
                log.error("BMC_UUID mismatch: %s, %s" % (BMC_UUID, expected_result))
                err_count += 1
    else:
        log.error("Fail to parse bmc_uuid")
        err_count += 1
    if err_count:
        raise RuntimeError('verify_bmc_uuid')


def verify_pci_device_number(device, expected_result=None):
    log.debug('Entering procedure verify_pci_device_number with args : %s\n' % (str(locals())))
    err_count = 0
    cmd = 'lspci'
    output = execute(device, cmd, mode=CENTOS_MODE)
    log.cprint(output)
    p1 = r'\w{2}:\w{2}.\w'
    match = str(len(re.findall(p1, output)))
    if expected_result != None:
        if match == expected_result:
            log.info("Successfully verify_pci_device_number: %s" % (match))
        else:
            log.error("pci_device_number mismatch: %s, %s" % (match, expected_result))
            err_count += 1
    if err_count:
        raise RuntimeError('verify_pci_device_number')


def verify_cmd_output_message(device, cmd, messages_list):
    log.debug('Entering procedure verify_cmd_output_message with args : %s\n' % (str(locals())))
    output = execute(device, cmd, mode=CENTOS_MODE)
    err_count = 0
    messages_list = messages_list.split(",")
    for msg in messages_list:
        if parse_keywords(msg, output) == "fail":
            err_count += 1
    if err_count == 0:
        log.success("Successfully verify '%s' output message" % cmd)
    else:
        log.fail("verify_%s_output_message fail" % cmd)
        raise testFailed("verify '%s' output message fail" % cmd)


def parse_keywords(regex, output):
    log.debug('Entering procedure parse_simple_keyword with args : %s\n' % (str(locals())))
    match = re.search(regex, output)
    if match:
        log.fail("Found: %s" % (match.group(0)))
        return "fail"
    else:
        log.success("Not found keyword: %s" % (regex))
        return "success"


def check_bios_version(device, bios_version):
    ### dmidecode --s bios-version
    log.debug('Entering procedure check_bios_version with args : %s\n' % (str(locals())))
    cmd = 'dmidecode --s bios-version'
    output = execute(device, cmd, mode=CENTOS_MODE)
    match = re.search(bios_version, output)
    if match:
        log.info("Successfully check_bios_version")
    else:
        log.fail("check_bios_version failed")
        raise testFailed("check_bios_version failed")


def verify_processor_model_name(device, expected_result=None):
    log.debug('Entering procedure verify_processor_model_name with args : %s\n' % (str(locals())))
    err_count = 0
    cmd = 'cat /proc/cpuinfo'
    output = execute(device, cmd, mode=CENTOS_MODE)
    log.cprint(output)
    p1 = r'model name\s+:\s+(.+)'
    match = re.search(p1, output)
    if match:
        if expected_result != None:
            processor_model_name = match.group(1).strip()
            if processor_model_name == expected_result:
                log.info("Successfully verify_processor_model_name: %s" % (processor_model_name))
            else:
                log.error("processor_model_name mismatch: %s, %s" % (processor_model_name, expected_result))
                err_count += 1
    else:
        log.error("Fail to parse processor_model_name")
        err_count += 1
    if err_count:
        raise RuntimeError('verify_processor_model_name')


def verify_memory_size(device, expected_result=None):
    log.debug('Entering procedure verify_memory_size with args : %s\n' % (str(locals())))
    err_count = 0
    cmd = 'cat /proc/meminfo'
    output = execute(device, cmd, mode=CENTOS_MODE)
    log.cprint(output)
    p1 = r'MemTotal:\s+(\d+)\s+'
    match = re.search(p1, output)
    if match:
        if expected_result != None:
            memory_size_1 = int(match.group(1).strip())
            memory_size_2 = round(memory_size_1 / 1024 / 1024 / 16) * 16
            memory_size = str(memory_size_2) + 'G'
            log.info(memory_size)
            if memory_size == expected_result:
                log.info("Successfully verify_memory_sizee: %s" % (memory_size))
            else:
                log.error("memory_size mismatch: %s, %s" % (memory_size, expected_result))
                err_count += 1
    else:
        log.error("Fail to parse memory_size")
        err_count += 1
    if err_count:
        raise RuntimeError('verify_memory_size')


def verify_memory_size(device, expected_result=None):
    log.debug('Entering procedure verify_memory_size with args : %s\n' % (str(locals())))
    err_count = 0
    cmd = 'cat /proc/meminfo'
    output = execute(device, cmd, mode=CENTOS_MODE)
    log.cprint(output)
    p1 = r'MemTotal:\s+(\d+)\s+'
    match = re.search(p1, output)
    if match:
        if expected_result != None:
            memory_size_1 = int(match.group(1).strip())
            memory_size_2 = round(memory_size_1 / 1024 / 1024 / 16) * 16
            memory_size = str(memory_size_2) + 'G'
            log.info(memory_size)
            if memory_size == expected_result:
                log.info("Successfully verify_memory_sizee: %s" % (memory_size))
            else:
                log.error("memory_size mismatch: %s, %s" % (memory_size, expected_result))
                err_count += 1
    else:
        log.error("Fail to parse memory_size")
        err_count += 1
    if err_count:
        raise RuntimeError('verify_memory_size')


def run_ipmi_cmd_reset(device, username, hostip, password, cmd, expected='None'):
    log.debug('Entering procedure run_ipmi_cmd_reset with args : %s\n' % (str(locals())))
    deviceObj = Device.getDeviceObject(device)
    err_count = 0
    error_msg = r'(.*command failed.+error)'
    successful_msg = r'ACPI Power State'
    cmd2 = 'ipmitool sel list'
    child = ssh_command(username, hostip, password, cmd)
    child.expect(pexpect.EOF, timeout=180)
    output = child.before.strip().decode('utf-8')
    log.info(output)
    time.sleep(90)
    child_1 = ssh_command(username, hostip, password, cmd2)
    child_1.expect(pexpect.EOF, timeout=180)
    output1 = child_1.before.strip().decode('utf-8')
    log.info(output1)
    match_err = re.search(error_msg, output)
    if match_err:
        log.fail("Found error: %s" % (match_err.group(1)))
        err_count += 1
    match = re.search(successful_msg, output1)
    if expected == 'None':
        if match:
            log.info("run_ipmi_cmd_reset successfully")
        else:
            log.error("mismatch %s" % successful_msg)
            err_count += 1
    elif expected == 'loss':
        if match:
            log.error("Found error: %s" % successful_msg)
            err_count += 1
        else:
            log.info("run_ipmi_cmd_reset successfully")
    if err_count:
        raise testFailed("run_ipmi_cmd_reset FAIL")


def run_ipmi_cmd_sel_clear(device):
    log.debug('Entering procedure run_ipmi_cmd_sel_clear with args : %s\n' % (str(locals())))
    err_count = 0
    deviceObj = Device.getDeviceObject(device)
    cmd = 'ipmitool sel clear'
    cmd1 = 'ipmitool sel list'
    error_msg = r'(.*command failed.+error)'
    successful_msg_1 = 'Clearing SEL'
    successful_msg_2 = 'reset/cleared'
    output = execute(device, cmd, mode=CENTOS_MODE)
    time.sleep(10)
    output1 = execute(device, cmd1, mode=CENTOS_MODE)
    match_err = re.search(error_msg, output)
    if match_err:
        log.fail("Found error: %s" % (match_err.group(1)))
        err_count += 1
    match_1 = re.search(successful_msg_1, output)
    match_2 = re.search(successful_msg_2, output1)
    if match_1:
        log.info("run_ipmi_cmd_sel_clear")
    else:
        log.error("mismatch %s" % successful_msg_1)
        err_count += 1
    if match_2:
        log.info("run_ipmi_cmd_sel_clear")
    else:
        log.error("mismatch %s" % successful_msg_2)
        err_count += 1
    if err_count:
        raise testFailed("run_ipmi_cmd_sel_clear")


def change_directory(device, path=""):
    ## cd [path]
    log.debug('Entering procedure change_directory with args : %s\n' % (str(locals())))
    deviceObj = Device.getDeviceObject(device)
    cmd = "cd " + path
    deviceObj.flush()
    deviceObj.sendCmd(cmd)
    deviceObj.transmit("")
    output = deviceObj.readMsg()
    p1 = 'No such file or directory'
    match = re.search(p1, output)
    if match:
        log.fail("%s" % (p1))
        raise testFailed('change_directory')
    else:
        log.success('Successfully change directory %s' % (path))


def verify_system_guid(device):
    log.debug('Entering procedure verify_system_guid with args : %s\n' % (str(locals())))
    err_count = 0
    deviceObj = Device.getDeviceObject(device)
    cmd1 = 'dmidecode -t 1'
    cmd2 = 'ipmitool raw 06 0x37'
    p1 = 'UUID:\s+(.*)'
    p2 = 'time.+\n\s(.+)'
    output = execute(device, cmd1, mode=CENTOS_MODE)
    match = re.search(p1, output)
    if match:
        System_GUID = match.group(1).strip().upper()
        log.info("Successfully get System_guid: %s" % (System_GUID))
    else:
        log.error("Fail to get System_guid")
        err_count += 1
    output1 = execute(device, cmd2, mode=CENTOS_MODE)
    match1 = re.search(p2, output1)
    if match1:
        rsp_list_1 = str(match1.group(1).strip().upper()).split(' ')
        rsp_list_2 = rsp_list_1[3] + rsp_list_1[2] + rsp_list_1[1] + rsp_list_1[0] + '-' + rsp_list_1[5] \
                     + rsp_list_1[4] + '-' + rsp_list_1[7] + rsp_list_1[6] + '-' + rsp_list_1[8] + rsp_list_1[9] + '-' + \
                     rsp_list_1[10] + rsp_list_1[11] + rsp_list_1[12] + rsp_list_1[13] + rsp_list_1[14] + rsp_list_1[15]
        log.info("Successfully get rsp_guid by ipmitool raw command")
    else:
        log.error("Fail to get rsp_guid by ipmitool raw command")
        err_count += 1
    if System_GUID == rsp_list_2:
        log.info("Successfully verify System_guid: %s" % (System_GUID))
    else:
        log.error("%s mismatch %s" % (System_GUID, rsp_list_2))
        err_count += 1
    if err_count:
        raise testFailed("verify_system_guid FAIL")


def ssh_command(username, hostip, password, command, title_p=False):
    key_password = "Password" if title_p else "password"
    ssh_newkey = 'Are you sure you want to continue connecting'
    child = pexpect.spawn('ssh -l %s %s %s' % (username, hostip, command))
    i = child.expect([pexpect.TIMEOUT, ssh_newkey, '%s: ' % key_password])
    if i == 0:  # Timeout
        print('ERROR_1!')
        print('SSH could not login. Here is what SSH said:')
        # print(child.before, child.after)
        return None
    if i == 1:  # SSH does not have the public key. Just accept it.
        child.sendline('yes')
        child.sendline('\r')
        child.expect('%s: ' % key_password)
        i = child.expect([pexpect.TIMEOUT, '%s: ' % key_password])
        if i == 0:
            # Timeout
            print('ERROR_2!')
            print('SSH could not login. Here is what SSH said:')
            #print(child.before, child.after)
            return None
        child.sendline(password)
        return child
    if i == 2:
        child.sendline(password)
        #        log.debug(str(child))
        return child


def ssh_command_test():
    username = 'root'
    hostip = '10.204.113.161'
    password = '111111'
    command = 'ls'
    child = ssh_command(username, hostip, password, command)
    print(child)
    child.expect(pexpect.EOF, timeout=180)
    print(child.before.strip().decode('utf-8'))


def ssh_command_run_ipmi_get_cmd(username, hostip, password, cmd, expected_result='None'):
    log.debug("Entering ssh_command_run_ipmi_get with args : %s" % (str(locals())))
    child = ssh_command(username, hostip, password, cmd)
    child.expect(pexpect.EOF, timeout=180)
    output = child.before.strip().decode('utf-8')
    print(output)
    if str(output) == str(expected_result):
        log.info("Successfully ssh_command_run_ipmi_get_cmd")
    else:
        log.info("fail to ssh_command_run_ipmi_get_cmd")
        raise RuntimeError("ssh_command_run_ipmi_get_cmd FAIL")


def ssh_command_run_ipmi_set_cmd(username=None, hostip=None, password=None, cmd=None, bmcusername=None, bmcip=None,
                                 bmcpassword=None, remote=False):
    log.debug("Entering ssh_command_run_ipmi_set_cmd with args : %s" % (str(locals())))
    if remote:
        cmd1 = 'ipmitool -H %s -U %s -P %s %s' % (bmcip, bmcusername, bmcpassword, cmd)
        child = ssh_command(username, hostip, password, cmd1)
        child.expect(pexpect.EOF, timeout=30)
        output = child.before.strip().decode('utf-8')
        log.info(output)
        test_name = 'remote_ssh_command_run_ipmi_set_cmd'
    else:
        child = ssh_command(username, hostip, password, cmd)
        child.expect(pexpect.EOF, timeout=30)
        output = child.before.strip().decode('utf-8')
        log.info(output)
        test_name = 'ssh_command_run_ipmi_set_cmd'
    parsed_output = parser_openbmc_lib.parse_oem_rsp_code(output)
    error_msg = r'.*No such file or directory'
    match_error = re.search(error_msg, output)
    time.sleep(1)
    if not parsed_output and match_error is None:
        log.success("Successfully %s, execute \'%s\'" % (test_name, cmd))
    else:
        #        log.fail("%s"%(match_error.group(0)))
        #        raise testFailed("Failed %s"%(test_name))
        if parsed_output["code"]:
            log.fail("Command error: rsp=\'%s\', \'%s\'\n" % (parsed_output["code"], parsed_output["message"]))
        elif "invalid" in parsed_output:
            log.fail("Invalid command: %s" % (parsed_output["invalid"]))
        elif match_error:
            log.fail("%s" % (match_error.group(0)))
        else:
            log.fail("Unknown error")
        raise testFailed("Failed %s" % (test_name))


def ssh_command_exec_ping(username, hostip, password, ipAddress, count, expected='None'):
    log.debug("Entering ssh_command_exec_ping with args : %s" % (str(locals())))
    log.debug("Execute the ping from Device:%s to ip:%s" % (hostip, ipAddress))
    cmd = "time ping %s -c %s" % (ipAddress, str(count))
    success_msg = '0% packet loss'
    loss_msg = '100% packet loss'
    child = ssh_command(username, hostip, password, cmd)
    child.expect(pexpect.EOF, timeout=180)
    output = child.before.strip().decode('utf-8')
    log.info(output)
    log.info('output: %s' % (output))
    if expected == 'None':
        match = re.search(success_msg, output)
        if match:
            log.success("Found: %s" % (match.group(0)))
            log.success("ping to %s" % ipAddress)
        else:
            log.fail("ping to %s" % ipAddress)
            raise testFailed("Ping to destination IP address failed")
    elif expected == 'loss':
        match = re.search(loss_msg, output)
        if match:
            log.success("Found: %s" % (match.group(0)))
            log.success("ping to " + ipAddress + " get 100% packet loss")
        else:
            log.fail("ping to " + ipAddress + " did not get 100% packet loss")
            raise testFailed("Ping to destination IP address with loss expected failed")


def whitebox_exit_bios_setup(device, centOS_linux=True):
    log.debug('Entering whitebox_exit_bios_setup with args : %s' % (str(locals())))
    deviceObj = Device.getDeviceObject(device)
    line1 = 'CentOS Linux'
    line2 = 'Yes'
    line3 = 'Quit without saving?'
    send_key(device, "KEY_ESC")
    deviceObj.read_until_regexp(line3, timeout=10)
    send_key(device, "KEY_ENTER")
    if centOS_linux:
        deviceObj.read_until_regexp(line1, timeout=20)
    deviceObj.getPrompt("centos", timeout=600)


def whitebox_save_bios_setup(device, connect=True):
    log.debug('Entering whitebox_exit_bios_setup with args : %s' % (str(locals())))
    deviceObj = Device.getDeviceObject(device)
    line1 = 'CentOS Linux'
    line2 = 'Yes'
    line3 = 'Save configuration and reset?'
    send_key(device, "KEY_LEFT")
    send_key(device, "KEY_ENTER")
    deviceObj.read_until_regexp(line2, timeout=10)
    send_key(device, "KEY_ENTER")
    if connect:
        deviceObj.getPrompt("centos", timeout=600)


def verify_ipmi_test(test_name, device, cmd, expected_result='None'):
    log.debug('Entering procedure verify_ipmi_test : %s\n' % (str(locals())))
    parsed_output = parser()
    err_count = 0
    output = openbmc_lib.run_ipmi_get_cmd(device, cmd)
    parser_command = 'parserOpenbmc.parse_rsp_to_byte_' + test_name + '(output)'
    log.debug("call parser: %s" % parser_command)
    parsed_output = eval(parser_command)
    if expected_result != 'None':
        if test_name == "get_device_id":
            expected_result['Firmware Revision'] = openbmc_lib.get_version_from_config('BMC')['BMC Version']
        elif test_name == "board_id":
            log.info("check board type")
            board_rev_id = openbmc_lib.get_brd_id_by_board_type(device)
            expected_result.update({"Board Revision ID": board_rev_id})
        err_count += CommonLib.compare_input_dict_to_parsed(parsed_output, expected_result)
    else:
        return parsed_output
    if err_count:
        raise testFailed("run_ipmi_get_test while testing %s" % (test_name))


def whitebox_enter_bios_setup(device, bios_password=None):
    log.debug('Entering whitebox_enter_bios_setup with args : %s' % (str(locals())))
    deviceObj = Device.getDeviceObject(device)

    # line1 = 'Press <DEL> or <F2> to enter setup.'
    line1 = 'Press <*>'
    line2 = 'Enter Setup...'
    line3 = '.*Aptio Setup Utility.*'
    line4 = 'Enter Password'
    line5 = '------'

    output = deviceObj.read_until_regexp(line5, timeout=600)
    log.info("output is:%s\n" % str(output))
    match = re.search(line4, output)
    match1 = re.search(line3, output)
    if match:
        log.debug("Found '%s'" % (line4))
        deviceObj.transmit(bios_password)
        send_key(device, "KEY_ENTER")
        deviceObj.read_until_regexp(line3, timeout=60)
        log.success("Successfully enter Bios Setup 1")
    elif match1:
        log.debug("Found '%s'" % (line3))
        log.success("Successfully enter Bios Setup 2")
    else:
        log.fail("Failed enter_whitebox_bios_setup")
        raise testFailed("enter_whitebox_bios_setup")


def verify_com0_bios_setting(device, keyword=None, baud_rate=None):
    log.debug('Entering verify_com0_bios_setting with args : %s' % (str(locals())))
    deviceObj = Device.getDeviceObject(device)
    err_count = 0
    p1 = 'Console Redirection\s+\[(\S+)\]'
    p2 = 'Bits per second\s+\[(\d+)\]'
    boundary_line = '(EMS)'
    deviceObj = Device.getDeviceObject(device)
    send_key(device, "KEY_ENTER")
    output = deviceObj.receive(boundary_line)
    output = escape_ansi(output)
    match = re.search(p1, output)
    log.info(output)
    if match:
        serial_port_setting = match.group(1).strip()
        log.info(serial_port_setting)
        if serial_port_setting == keyword:
            log.info("Successfully verify_com0_serial_port_setting: %s" % (keyword))
        else:
            log.error("FAIL to verify_com0_serial_port_setting: %s" % (keyword))
            err_count += 1
    else:
        log.error("FAIL to get com0_serial_port_status")
        err_count += 1
    send_key(device, "KEY_DOWN")
    send_key(device, "KEY_ENTER")
    output = deviceObj.receive("Flow Control")
    output = escape_ansi(output)
    match2 = re.search(p2, output)
    if match2:
        serial_port_baud_rate = match2.group(1).strip()
        log.info(serial_port_baud_rate)
        if serial_port_baud_rate == baud_rate:
            log.info("Successfully verify_com0_baud_rate: %s" % (baud_rate))
        else:
            log.error("FAIL to verify_com0_baud_rate: %s" % (baud_rate))
            err_count += 1
    else:
        log.error("FAIL to get com0_serial_baud_rate")
        err_count += 1
    if err_count:
        raise RuntimeError('Verify_com0_bios_setting_FAIL')


def verify_serial_port_baud_rate(username=None, hostip=None, password=None, bmcip=None, bmcusername='admin', \
                                 bmcpassword='admin', baud_rate='115200'):
    log.debug('Entering verify_serial_port_baud_rate with args : %s' % (str(locals())))
    err_count = 0
    p1 = 'Non-Volatile Bit Rate.+:\s+(\S+)'
    cmd = "ipmitool -I lanplus -H %s -U %s -P %s sol info" % (bmcip, bmcusername, bmcpassword)
    child = ssh_command(username, hostip, password, cmd)
    child.expect(pexpect.EOF, timeout=180)
    output = child.before.strip().decode('utf-8')
    log.info(output)
    match = re.search(p1, output)
    if match:
        serial_port_baud_rate = match.group(1).strip()
        serial_port_baud_rate_1 = int(float(serial_port_baud_rate) * 1000)
        log.info(serial_port_baud_rate_1)
        if str(serial_port_baud_rate_1) == baud_rate:
            log.info("Successfully verify_serial_port_baud_rate under OS: %s" % (baud_rate))
        else:
            log.error("FAIL: serial_port_baud_rate %s under OS mismatch %s" % (serial_port_baud_rate_1, baud_rate))
            err_count += 1
    else:
        log.error("FAIL to get serial_port_baud_rate under OS")
        err_count += 1
    if err_count:
        raise RuntimeError('verify_serial_port_baud_rate under OS FAIL')


def verify_sol_Function(hostip, username, password, bmcip, bmcusername, \
                        bmcpassword, dutusername, dutpassword):
    log.debug('Entering procedure verify_sol_function with args : %s\n' % (str(locals())))
    err_count = 0
    cmd1 = 'ipmitool -H %s -U %s -P %s -I lanplus sol activate' % (bmcip, bmcusername, bmcpassword)
    cmd2 = 'ipmitool -H %s -U %s -P %s -I lanplus sol deactivate' % (bmcip, bmcusername, bmcpassword)
    p1 = hostip
    p2 = bmcip
    p3 = 'SOL session closed by BMC'
    s = pxssh.pxssh()
    hostname = hostip
    s.login(hostname, username, password, login_timeout=60)
    s.sendline('ifconfig')
    s.prompt()
    output = s.before.strip().decode('utf-8')
    log.info(output)
    match = re.search(p1, output)
    if match:
        log.info("Successfully SSH login OS: %s" % (hostip))
    else:
        log.error("FAIL to login OS: %s" % (hostip))
        err_count += 1
    s.sendline(cmd1)
    s.prompt()
    s.sendline(username)
    s.prompt()
    time.sleep(1)
    s.sendline(password)
    s.prompt()
    s.sendline('ipmitool lan print 1')
    s.prompt()
    output = s.before.strip().decode('utf-8')
    log.info(output)
    match1 = re.search(p2, output)
    if match1:
        log.info("Successfully active SOL")
    else:
        log.error("FAIL to active SOL")
        err_count += 1
    s.sendline(cmd2)
    s.prompt()
    output = s.before.strip().decode('utf-8')
    log.info(output)
    match2 = re.search(p3, output)
    if match2:
        log.info("Successfully deactive SOL")
    else:
        log.error("FAIL to deactive SOL")
        err_count += 1
    s.logout()
    if err_count:
        raise RuntimeError('verify_sol_function FAIL')


def verify_current_bmc_user(username, hostip, password, bmcip, rsp_device_id):
    log.debug("Entering verify_current_bmc_user with args : %s" % (str(locals())))
    err_count = 0
    cmd1 = "ipmitool user list 1|awk 'NR==3'"
    child = ssh_command(username, hostip, password, cmd1)
    child.expect(pexpect.EOF, timeout=180)
    output = child.before.strip().decode('utf-8')
    log.info(output)
    output1 = output.split()
    bmcusername = output1[1]
    if bmcusername == 'sfabmc':
        bmcpassword = 'T1tnDdn7990'
    else:
        bmcpassword = 'admin'
    cmd2 = 'ipmitool -H %s -U %s -P %s raw 06 01' % (bmcip, bmcusername, bmcpassword)
    log.info(cmd2)
    child = ssh_command(username, hostip, password, cmd2)
    child.expect(pexpect.EOF, timeout=180)
    output = child.before.strip().decode('utf-8')
    log.info(output)
    if str(output) == rsp_device_id:
        log.info(
            "Successfully Use the username:%s and password:%s to communicate with BMC" % (bmcusername, bmcpassword))
    else:
        log.error("fail to Use the username:%s and password:%s to communicate with BMC" % (bmcusername, bmcpassword))
        err_count += 1
    if err_count:
        raise RuntimeError('verify_current_bmc_user')


def verify_add_bmc_user(device, username, hostip, password, bmcip, bmcusername, bmcpassword, bmcusrlist_id, \
                        rsp_device_id, new_username, create_success=True):
    log.debug("Entering verify_add_bmc_user with args : %s" % (str(locals())))
    deviceObj = Device.getDeviceObject(device)
    err_count = 0
    error_msg = r'.*No such file or directory'
    cmd1 = 'ipmitool user set name %s %s' % (bmcusrlist_id, bmcusername)
    cmd2 = 'ipmitool user set password %s %s' % (bmcusrlist_id, bmcpassword)
    cmd3 = 'ipmitool user enable %s' % (bmcusrlist_id)
    if bmcusrlist_id == '10':
        cmd4 = 'ipmitool raw 6 0x43 0x91 0xa 4 0'
        cmd5 = 'ipmitool raw 0x06 0x47 0x8a 0x02 0x74 0x65 0x73 0x74 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00'
        cmd6 = 'ipmitool raw 0x06 0x47 0x0a 0x02 0x74 0x65 0x73 0x74 00 00 00 00 00 00 00 00 00 00 00 00'
    else:
        cmd4 = 'ipmitool raw 6 0x43 0x91 0x%s 4 0' % (bmcusrlist_id)
        cmd5 = 'ipmitool raw 0x06 0x47 0x8%s 0x02 0x74 0x65 0x73 0x74 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00' % (
            bmcusrlist_id)
        cmd6 = 'ipmitool raw 0x06 0x47 0x0%s 0x02 0x74 0x65 0x73 0x74 00 00 00 00 00 00 00 00 00 00 00 00' % (
            bmcusrlist_id)
    cmd7 = 'ipmitool user set name %s %s' % (bmcusrlist_id, new_username)
    openbmc_lib.run_ipmi_set_cmd(device, cmd1)
    openbmc_lib.run_ipmi_set_cmd(device, cmd2)
    openbmc_lib.run_ipmi_set_cmd(device, cmd3)
    openbmc_lib.run_ipmi_set_cmd(device, cmd4)
    verify_user_password_is_valid(device, bmcusrlist_id, bmcpassword, byte='16', result=True)
    verify_user_password_is_valid(device, bmcusrlist_id, bmcpassword, byte='20', result=False)
    verify_bmc_user(username, hostip, password, bmcip, bmcusername, bmcpassword, rsp_device_id)
    openbmc_lib.run_ipmi_set_cmd(device, cmd5)
    openbmc_lib.run_ipmi_set_cmd(device, cmd6)
    verify_bmc_user(username, hostip, password, bmcip, bmcusername, 'test', rsp_device_id)
    openbmc_lib.run_ipmi_set_cmd(device, cmd7)
    verify_bmc_user(username, hostip, password, bmcip, new_username, 'test', rsp_device_id)


def modify_bmc_user_name(device, username, hostip, password):
    log.debug("Entering modify_bmc_user_name with args : %s" % (str(locals())))
    deviceObj = Device.getDeviceObject(device)
    cmd1 = 'ipmitool user set name 3 tester'
    cmd2 = "ipmitool user list 1|awk 'NR==4'"
    openbmc_lib.run_ipmi_set_cmd(device, cmd1)
    child = ssh_command(username, hostip, password, cmd2)
    child.expect(pexpect.EOF, timeout=180)
    output = child.before.strip().decode('utf-8')
    log.info(output)
    output1 = output.split()
    bmcusername = output1[1]
    if bmcusername == 'tester':
        log.info("Successfully modify_bmc_user_name to tester")
    else:
        raise testFailed("modify_bmc_user_name to tester FAIL")


def verify_user_password_is_valid(device, bmcusrlist_id, bmcpassword, byte, result):
    log.debug("Entering verify_user_password_is_valid with args : %s" % (str(locals())))
    deviceObj = Device.getDeviceObject(device)
    err_count = 0
    cmd1 = 'time ipmitool user test %s %s %s' % (bmcusrlist_id, byte, bmcpassword)
    p3 = 'Success'
    p4 = 'Failure: wrong password size'
    error_msg = r'.*No such file or directory'
    timeout = 30
    if result:
        output = deviceObj.sendCmdRegexp(cmd1, Const.TIME_REG_PROMPT, timeout)
        log.cprint(str(output))
        match = re.search(p3, output)
        if match:
            log.success("Successfully verify_user_password_is_valid: %s" % (match.group(0)))
        else:
            log.fail("Fail to find Success")
            err_count += 1
    else:
        output = deviceObj.sendCmdRegexp(cmd1, Const.TIME_REG_PROMPT, timeout)
        log.cprint(str(output))
        match = re.search(p4, output)
        if match:
            log.success("Successfully verify_user_password_is_not_valid: %s" % (match.group(0)))
        else:
            log.fail("Fail to find Failure: wrong password size")
            err_count += 1
    if err_count:
        raise RuntimeError('verify_user_password_is_valid FAIL')


def verify_bmc_user(username, hostip, password, bmcip, bmcusername, bmcpassword, rsp_device_id):
    log.debug("Entering verify_bmc_user with args : %s" % (str(locals())))
    err_count = 0
    cmd1 = 'ipmitool -H %s -U %s -P %s raw 06 01' % (bmcip, bmcusername, bmcpassword)
    log.info(cmd1)
    child = ssh_command(username, hostip, password, cmd1)
    child.expect(pexpect.EOF, timeout=180)
    output = child.before.strip().decode('utf-8')
    log.info(output)
    if str(output) == rsp_device_id:
        log.info(
            "Successfully Use the username:%s and password:%s to communicate with BMC" % (bmcusername, bmcpassword))
    else:
        log.error("fail to Use the username:%s and password:%s to communicate with BMC" % (bmcusername, bmcpassword))
        err_count += 1
    if err_count:
        raise RuntimeError('verify_bmc_user FAIL')


def verify_bmc_user_count(username, hostip, password):
    log.debug("Entering verify_bmc_user_count with args : %s" % (str(locals())))
    err_count = 0
    cmd1 = 'ipmitool user list 1|grep tester|wc'
    cmd2 = "'ipmitool user list 1|awk 'NR==11'"
    child = ssh_command(username, hostip, password, cmd1)
    child.expect(pexpect.EOF, timeout=180)
    output = child.before.strip().decode('utf-8')
    log.info(output)
    output = output.split()
    create_user = output[0]
    if create_user == '8':
        log.info("Successfully create_user_count: %s" % (create_user))
    else:
        log.error("create_user_count: %s mismatch 8" % (create_user))
        err_count += 1
    child = ssh_command(username, hostip, password, cmd2)
    child.expect(pexpect.EOF, timeout=180)
    output = child.before.strip().decode('utf-8')
    log.info(output)
    output = output.split()
    max_user_count = output[0]
    if max_user_count == '10':
        log.info("Successfully verify max_user_count: %s" % (max_user_count))
    else:
        log.error("max_user_count: %s mismatch 10" % (max_user_count))
        err_count += 1
    if err_count:
        raise RuntimeError('verify_bmc_user_count FAIL')


def wait_prompt(device, timeout=500):
    log.debug('Entering procedure wait_prompt with args : %s\n' % (str(locals())))
    err_count = 0
    deviceObj = Device.getDeviceObject(device)
    deviceObj.getPrompt(CENTOS_MODE, timeout)


def verify_smash_clp_command_help(username, hostip, password):
    log.debug('Entering verify_SMASH_CLP_Command_help with args : %s\n' % (str(locals())))
    cmd = 'help'
    p1 = 'shows the smash version'
    s = pxssh.pxssh()
    hostname = hostip
    s.login(hostname, username, password, auto_prompt_reset=False, sync_original_prompt=False,
            original_prompt=r"(?i)->", login_timeout=30)
    s.sendline(cmd)
    s.prompt()
    output = s.before.strip().decode('utf-8')
    log.info(str(output))
    match = re.search(p1, output)
    s.logout()
    if match:
        log.success("Successfully Verify_SMASH_CLP_Command_help: %s" % (match.group(0)))
    else:
        log.fail("Verify_SMASH_CLP_Command_help FAIL")
        raise testFailed("verify_SMASH_CLP_Command_help")


def verify_whitebox_power_control(username, hostip, password, bmcip, bmcusername, bmcpassword, command):
    log.debug("Entering verify_whitebox_power_control : %s" % (str(locals())))
    if command == 'power off':
        cmd = 'raw 00 02 00'
    elif command == 'power on':
        cmd = 'raw 00 02 01'
    elif command == 'power cycle':
        cmd = 'raw 00 02 02'
    elif command == 'hard reset':
        cmd = 'raw 00 02 03'
    elif command == 'trigger NMI interrupt':
        cmd = 'raw 00 02 04'
    elif command == 'soft shutdown':
        cmd = 'raw 00 02 05'
    ssh_command_run_ipmi_set_cmd(username, hostip, password, cmd, bmcusername, bmcip, bmcpassword, remote=True)
    time.sleep(10)


def verify_whitebox_power_status(username, hostip, password, bmcip, bmcusername, bmcpassword, expect_result):
    log.debug("Entering vverify_whitebox_power_status args : %s" % (str(locals())))
    err_count = 0
    cmd = 'ipmitool -I lanplus -H %s -U %s -P %s power status' % (bmcip, bmcusername, bmcpassword)
    cmd1 = 'ipmitool -I lanplus -H %s -U %s -P %s sel list' % (bmcip, bmcusername, bmcpassword)
    p1 = 'Chassis Power is (\w+)'
    if expect_result == 'off':
        p2 = 'Legacy OFF state'
    else:
        p2 = 'Legacy ON state'
    log.info(cmd)
    child = ssh_command(username, hostip, password, cmd)
    child.expect(pexpect.EOF, timeout=10)
    output = child.before.strip().decode('utf-8')
    log.info(output)
    match = re.search(p1, output)
    if match:
        power_status = match.group(1).strip()
        log.info(power_status)
        if power_status == expect_result:
            log.info("Successfully verify_power_status: %s" % (power_status))
        else:
            log.error("%s mismatch expect_result: %s" % (power_status, expect_result))
            err_count += 1
    else:
        log.error("FAIL to get power status")
        err_count += 1
    log.info(cmd1)
    child = ssh_command(username, hostip, password, cmd1)
    child.expect(pexpect.EOF, timeout=10)
    output = child.before.strip().decode('utf-8')
    log.info(output)
    match = re.search(p2, output)
    if match:
        log.info("Successfully verify Legacy %s state" % (expect_result))
    else:
        log.error("Fail to verify Legacy %s state" % (expect_result))
        err_count += 1
    if err_count:
        raise RuntimeError('verify_power_status FAIL')


def check_sel_list_unexpect_event(username, hostip, password, bmcip, bmcusername, bmcpassword, messages_list):
    log.debug('Entering procedure check_sel_list_unexpect_event with args : %s\n' % (str(locals())))
    err_count = 0
    cmd = 'ipmitool -H %s -U %s -P %s sel list' % (bmcip, bmcusername, bmcpassword)
    child = ssh_command(username, hostip, password, cmd)
    child.expect(pexpect.EOF, timeout=10)
    output = child.before.strip().decode('utf-8')
    log.info(output)
    messages_list = messages_list.split(",")
    for msg in messages_list:
        if parse_keywords(msg, output) == "fail":
            err_count += 1
    check_full_fan_speed(username, hostip, password, bmcip, bmcusername, bmcpassword)
    if err_count == 0:
        log.success("Successfully check_sel_list_unexpect_event")
    else:
        log.fail("check sel list unexpect event fail")
        raise testFailed("check_sel_list_unexpect_event fail")


def check_full_fan_speed(username, hostip, password, bmcip, bmcusername, bmcpassword, full_speed=False):
    log.debug('Entering procedure check_full_fan_speed with args : %s\n' % (str(locals())))
    err_count = 0
    p = '00 64'
    cmd = 'ipmitool -H %s -U %s -P %s raw 0x3a 0x35' % (bmcip, bmcusername, bmcpassword)
    child = ssh_command(username, hostip, password, cmd)
    child.expect(pexpect.EOF, timeout=10)
    output = child.before.strip().decode('utf-8')
    log.info(output)
    if full_speed:
        if str(output) == p:
            log.success("Successfully check_fan_speed is full")
        else:
            log.fail("current fan speed: %s is not full" % str(output))
            err_count += 1
    else:
        if str(output) != p:
            log.success("Successfully check_fan_speed is not full")
        else:
            log.fail("current fan speed: %s is full" % str(output))
            err_count += 1
    if err_count:
        raise testFailed("check_full_fan_speed fail")


def modify_bmc_lan_ipsrc(device, lan_id, mode='static'):
    log.debug("Entering modify_bmc_lan_ipsrc with args : %s" % (str(locals())))
    deviceObj = Device.getDeviceObject(device)
    err_count = 0
    cmd1 = 'ipmitool lan set %s ipsrc %s' % (lan_id, mode)
    cmd2 = 'time ipmitool lan print %s' % (lan_id)
    openbmc_lib.run_ipmi_set_cmd(device, cmd1)
    p1 = 'IP Address Source\s+:\s+(\w+)'
    if mode == 'static':
        p2 = 'Static'
    else:
        p2 = 'DHCP'
    timeout = 30
    output = deviceObj.sendCmdRegexp(cmd2, Const.TIME_REG_PROMPT, timeout)
    log.cprint(str(output))
    match = re.search(p1, output)
    if match:
        current_mode = match.group(1).strip()
        if current_mode == p2:
            log.success("Successfully modify_bmc_lan %s ipsrc to %s" % (lan_id, mode))
        else:
            log.fail("current_mode: %s mismatch expect mode: %s" % (current_mode, mode))
            err_count += 1
    else:
        log.fail("can't get the lan ipsrc mode")
        err_count += 1
    if err_count:
        raise RuntimeError('modify_bmc_lan_ipsrc')


def modify_bmc_lan_ipaddr(device, lan_id, ipaddr):
    log.debug("Entering modify_bmc_lan_ipaddr with args : %s" % (str(locals())))
    deviceObj = Device.getDeviceObject(device)
    err_count = 0
    cmd1 = 'ipmitool lan set %s ipaddr %s' % (lan_id, ipaddr)
    cmd2 = 'time ipmitool lan print %s' % (lan_id)
    openbmc_lib.run_ipmi_set_cmd(device, cmd1)
    p1 = 'IP Address\s+:\s+(.+)'
    timeout = 30
    output = deviceObj.sendCmdRegexp(cmd2, Const.TIME_REG_PROMPT, timeout)
    log.cprint(str(output))
    match = re.search(p1, output)
    if match:
        current_ip = match.group(1).strip()
        if current_ip == ipaddr:
            log.success("Successfully modify_bmc_lan %s ipaddr to %s" % (lan_id, ipaddr))
        else:
            log.fail("current_ip: %s mismatch expect ip: %s" % (current_ip, ipaddr))
            err_count += 1
    else:
        log.fail("can't get the lan ipaddr")
        err_count += 1
    if err_count:
        raise RuntimeError('modify_bmc_lan_ipaddr')


def modify_bmc_lan_netmask(device, lan_id, netmask):
    log.debug("Entering modify_bmc_lan_netmask with args : %s" % (str(locals())))
    deviceObj = Device.getDeviceObject(device)
    err_count = 0
    cmd1 = 'ipmitool lan set %s netmask %s' % (lan_id, netmask)
    cmd2 = 'time ipmitool lan print %s' % (lan_id)
    openbmc_lib.run_ipmi_set_cmd(device, cmd1)
    p1 = 'Subnet Mask\s+:\s+(.+)'
    timeout = 30
    output = deviceObj.sendCmdRegexp(cmd2, Const.TIME_REG_PROMPT, timeout)
    log.cprint(str(output))
    match = re.search(p1, output)
    if match:
        current_netmask = match.group(1).strip()
        if current_netmask == netmask:
            log.success("Successfully modify_bmc_lan %s netmask to %s" % (lan_id, netmask))
        else:
            log.fail("current_ip: %s mismatch expect netmask: %s" % (current_netmask, netmask))
            err_count += 1
    else:
        log.fail("can't get the lan netmask")
        err_count += 1
    if err_count:
        raise RuntimeError('modify_bmc_lan_netmask')


def ssh_command_ping(username, hostip, password, ipaddr, count, expected='None'):
    log.debug("Entering ssh_command_ping with args : %s" % (str(locals())))
    cmd = "ping %s -c %s" % (ipaddr, str(count))
    success_msg = str(count) + ' packets transmitted, ' + str(count) + ' (packets )?received, 0% packet loss'
    loss_msg = str(count) + ' packets transmitted, ' + '0 packets received, 100% packet loss'
    child = ssh_command(username, hostip, password, cmd)
    child.expect(pexpect.EOF, timeout=10)
    output = child.before.strip().decode('utf-8')
    log.info('output: %s' % (output))
    if expected == 'None':
        match = re.search(success_msg, output)
        if match:
            log.success("Found: %s" % (match.group(0)))
            log.success("ssh_command_ping to %s" % ipaddr)
        else:
            log.fail("ssh_command_ping to %s" % ipaddr)
            raise RuntimeError("ssh_command_ping to destination IP address failed")
    elif expected == 'loss':
        match = re.search(loss_msg, output)
        if match:
            log.success("Found: %s" % (match.group(0)))
            log.success("ssh_command_ping to " + ipaddr + " get 100% packet loss")
        else:
            log.fail("ssh_command_ping to " + ipaddr + " did not get 100% packet loss")
            raise RuntimeError("ssh_command_ping to destination IP address with loss expected failed")


def get_poh_counter(device):
    log.debug("Entering get_poh_counter with args : %s" % (str(locals())))
    deviceObj = Device.getDeviceObject(device)
    err_count = 0
    cmd = 'time ipmitool chassis poh'
    p1 = 'POH Counter\s+:\s+(\d+)\s+days,\s+(\d+)\s+hours'
    timeout = 30
    output = deviceObj.sendCmdRegexp(cmd, Const.TIME_REG_PROMPT, timeout)
    log.cprint(str(output))
    match = re.search(p1, output)
    if match:
        days = match.group(1).strip()
        hours = match.group(2).strip()
        log.info(hours)
        time = float(days) * 24 + float(hours)
        log.success("Successfully get_poh_counter: %s hours" % (time))
        return time
    else:
        log.fail("fail to get_poh_counter value")
        raise RuntimeError('get_poh_counter')


def verify_poh_counter(time_before, time_after):
    log.debug("Entering verify_poh_counter with args : %s" % (str(locals())))
    if time_after != 0.0 and time_after >= time_before:
        log.success("Successfully verify_poh_counter")
    else:
        log.fail("POH_Counter was cleared after BMC FW update, before: %s, after: %s" % (time_before, time_after))
        raise RuntimeError('verify_poh_counter')


def verify_bmc_ssl_cipher_version(device, bmcip):
    log.debug("Entering verify_bmc_ssl_cipher_version args : %s" % (str(locals())))
    deviceObj = Device.getDeviceObject(device)
    err_count = 0
    cmd = 'time nmap --script ssl-enum-ciphers %s' % (bmcip)
    p1 = 'nmap: command not found'
    p2 = 'TLSv1.1'
    timeout = 120
    output = deviceObj.sendCmdRegexp(cmd, Const.TIME_REG_PROMPT, timeout)
    log.cprint(str(output))
    match = re.search(p1, output)
    if match:
        error_msg = match.group(0).strip()
        log.fail("please install nmap tool first: %s" % error_msg)
        err_count += 1
    match = re.search(p2, output)
    if match:
        error_msg = match.group(0).strip()
        log.fail("need to remove %s according to customer's requirement" % error_msg)
        err_count += 1
    if err_count:
        raise RuntimeError('verify_BMC_SSL_Cipher_Version')


def verify_bmc_suite_id_test(username, hostip, password, bmcip, bmcusername, bmcpassword, rsp_device_id, list_1,
                             list_2=None):
    log.debug("Entering verify_bmc_suite_id_test args : %s" % (str(locals())))
    err_count = 0
    list1 = list_1.split(",")
    p1 = 'Unsupported cipher suite ID :\s+(\S+)'
    for i in list1:
        cmd = 'ipmitool -I lanplus -H %s -U %s -P %s -C %s raw 6 1' % (bmcip, bmcusername, bmcpassword, i)
        log.info(cmd)
        child = ssh_command(username, hostip, password, cmd)
        child.expect(pexpect.EOF, timeout=180)
        output = child.before.strip().decode('utf-8')
        log.info(output)
        if str(output) == rsp_device_id:
            log.info("Successfully verify_BMC_suite_test: %s" % cmd)
        else:
            log.error("fail to verify_BMC_suite_test: %s" % cmd)
            err_count += 1
    if list_2 != None and list_2 != '':
        list2 = list_2.split(",")
        for i in list2:
            cmd = 'ipmitool -I lanplus -H %s -U %s -P %s -C %s raw 6 1' % (bmcip, bmcusername, bmcpassword, i)
            log.info(cmd)
            child = ssh_command(username, hostip, password, cmd)
            child.expect(pexpect.EOF, timeout=180)
            output = child.before.strip().decode('utf-8')
            log.info(output)
            match = re.search(p1, output)
            if match:
                suite_id = match.group(1).strip()
                log.info("Successfully verify_BMC_suite_id: %s, expect unsupported" % suite_id)
            else:
                log.fail("suite_id: %s fail to get unsupported information" % suite_id)
                err_count += 1
    if err_count:
        raise RuntimeError('verify_BMC_suite_id_test')


def verify_ssh_ping_function(username, hostip, password, ipaddr, count='5', ping_timeout='100', stress=True,
                             expected='None'):
    log.debug('Entering procedure verify_ssh_ping_Function with args : %s\n' % (str(locals())))
    err_count = 0
    success_msg = '(\d+)\s+packets transmitted,\s+(\d+)\s+received,\s+(\d+)% packet loss'
    loss_msg = str(count) + ' packets transmitted, ' + '0 packets received, 100% packet loss'
    if stress:
        cmd = "time ping %s -w %s" % (ipaddr, ping_timeout)
        timeout_1 = int(ping_timeout) + 30
    else:
        cmd = "time ping %s -c %s" % (ipaddr, count)
        timeout_1 = count
    s = pxssh.pxssh()
    hostname = hostip
    s.login(hostname, username, password, login_timeout=30)
    s.sendline(cmd)
    s.prompt(timeout=int(timeout_1))
    output = s.before.strip().decode('utf-8')
    s.logout()
    log.info(output)
    if expected == 'None':
        match = re.search(success_msg, output)
        if match:
            transmitted_packets = match.group(1).strip()
            received_packets = match.group(2).strip()
            rate = match.group(3).strip()
            if rate == '0':
                log.info("Found: %s" % (match.group(0)))
                log.success("ssh ping to %s" % ipaddr)
            else:
                if int(transmitted_packets) - int(received_packets) == 1:
                    log.info("Found: %s, one packet lost at the beginning is acceptable" % (match.group(0)))
                    log.success("ssh ping to %s" % ipaddr)
                else:
                    err_count += 1
                    log.fail("ssh ping to %s, %s" % (ipaddr, match.group(0)))
        else:
            err_count += 1
            log.fail("ssh ping to %s" % ipaddr)
    elif expected == 'loss':
        match = re.search(loss_msg, output)
        if match:
            log.success("Found: %s" % (match.group(0)))
            log.success("ssh ping to " + ipaddr + " get 100% packet loss")
        else:
            log.fail("ssh ping to " + ipaddr + " did not get 100% packet loss")
            raise RuntimeError("SSH Ping to destination IP address with loss expected failed")
    else:
        err_count += 1
        log.fail("Please input the right keywords")
    if err_count:
        raise RuntimeError("SSH Ping to destination IP address failed")


def verify_kcs_function(device, device_id, product_id, biospassword):
    log.debug("Entering verify_kcs_function with args : %s" % (str(locals())))
    deviceObj = Device.getDeviceObject(device)
    err_count = 0
    cmd1 = 'ipmitool raw 0x06 0x01'
    cmd2 = 'ipmitool sensor'
    verify_ipmi_test('get_device_id', device, cmd1, device_id)
    verify_ipmi_driver(device)
    verify_bmc_product_id(device, product_id)
    openbmc_lib.run_ipmi_set_cmd(device, cmd2)
    ###use ipmitool raw command to enter bios setup
    cmd_1_Set_System_Boot_Options = 'ipmitool raw 00 0x08 00 01'
    cmd_2_Set_System_Boot_Options = 'ipmitool raw 00 0x08 03 0x1f'
    cmd_3_Set_System_Boot_Options = 'ipmitool raw 00 0x08 05 0x80 0x18 00 00 00'
    cmd_4_Set_System_Boot_Options = 'ipmitool raw 00 0x08 00 00'
    openbmc_lib.run_ipmi_set_cmd(device, cmd_4_Set_System_Boot_Options)
    openbmc_lib.run_ipmi_set_cmd(device, cmd_1_Set_System_Boot_Options)
    openbmc_lib.run_ipmi_set_cmd(device, cmd_2_Set_System_Boot_Options)
    openbmc_lib.run_ipmi_set_cmd(device, cmd_3_Set_System_Boot_Options)
    openbmc_lib.run_ipmi_set_cmd(device, cmd_4_Set_System_Boot_Options)
    reboot_os(device)
    whitebox_enter_bios_setup(device, biospassword)


def verify_ipmi_driver(device):
    log.debug("Entering verify_ipmi_driver with args : %s" % (str(locals())))
    deviceObj = Device.getDeviceObject(device)
    err_count = 0
    cmd1 = 'modprobe ipmi_si'
    cmd2 = 'modprobe ipmi_devintf'
    cmd3 = 'time lsmod'
    openbmc_lib.run_ipmi_set_cmd(device, cmd1)
    openbmc_lib.run_ipmi_set_cmd(device, cmd2)
    p1 = 'ipmi_si'
    p2 = 'ipmi_devintf'
    timeout = 30
    output = deviceObj.sendCmdRegexp(cmd3, Const.TIME_REG_PROMPT, timeout)
    log.cprint(str(output))
    match = re.search(p1, output)
    if match:
        log.success("Found ipmi_si module")
    else:
        log.fail("can't get ipmi_si module")
        err_count += 1
    match = re.search(p2, output)
    if match:
        log.success("Found ipmi_devintf module")
    else:
        log.fail("can't get ipmi_devintf module")
        err_count += 1
    if err_count:
        raise RuntimeError('verify_ipmi_driver FAIL')


def verify_bmc_power_restore_policy(device, expected_result='always-on'):
    ###expected result: Power On(always-on)|Power Off(always-off)|Last State(previous)
    log.debug("Entering verify_BMC_Power_Restore_Policy args : %s" % (str(locals())))
    deviceObj = Device.getDeviceObject(device)
    err_count = 0
    cmd = 'time ipmitool chassis status'
    p = 'Power Restore Policy\s+:\s+(.+)'
    if expected_result == 'always-on' or expected_result == 'Power On':
        p1 = 'always-on'
        p2 = 'Power On'
    elif expected_result == 'always-off' or expected_result == 'Power Off':
        p1 = 'always-off'
        p2 = 'Power Off'
    elif expected_result == 'previous' or expected_result == 'Last State':
        p1 = 'previous'
        p2 = 'Last State'
    timeout = 30
    output = deviceObj.sendCmdRegexp(cmd, Const.TIME_REG_PROMPT, timeout)
    log.cprint(str(output))
    match = re.search(p, output)
    if match:
        current_status = match.group(1).strip()
        if current_status == p1 or current_status == p2:
            log.success(
                "verify_BMC_Power_Restore_Policy PASS, current: %s match expected: %s or %s" % (current_status, p1, p2))
        else:
            log.fail("verify_BMC_Power_Restore_Policy FAIL, current: %s mismatch expected: %s or %s" % (
                current_status, p1, p2))
            err_count += 1
    else:
        err_count += 1
        log.fail("can't find the patern related to: %s" % p)
    if err_count:
        raise RuntimeError('verify_BMC_Power_Restore_Policy')


def get_bmc_power_restore_policy(device):
    log.debug("Entering get_bmc_power_restore_policy args : %s" % (str(locals())))
    deviceObj = Device.getDeviceObject(device)
    err_count = 0
    cmd = 'time ipmitool chassis status'
    p = 'Power Restore Policy\s+:\s+(.+)'
    timeout = 30
    output = deviceObj.sendCmdRegexp(cmd, Const.TIME_REG_PROMPT, timeout)
    log.cprint(str(output))
    match = re.search(p, output)
    if match:
        current_status = match.group(1).strip()
        log.success("get_bmc_power_restore_policy PASS: %s" % current_status)
        return current_status
    else:
        err_count += 1
        log.fail("can't find the patern related to: %s" % p)
    if err_count:
        raise RuntimeError('get_bmc_power_restore_policy')


def verify_bios_power_restore_policy(device, expected_result=None):
    log.debug('Entering verify_bios_Power_Restore_Policy with args : %s' % (str(locals())))
    deviceObj = Device.getDeviceObject(device)
    err_count = 0
    if expected_result == 'always-on' or expected_result == 'Power On':
        p1 = 'always-on'
        p2 = 'Power On'
    elif expected_result == 'always-off' or expected_result == 'Power Off':
        p1 = 'always-off'
        p2 = 'Power Off'
    elif expected_result == 'previous' or expected_result == 'Last State':
        p1 = 'previous'
        p2 = 'Last State'
    else:
        err_count += 1
        log.fail("Please input the right expected_result:previous|always-on|always-off")
    p3 = 'AC Power Restore Policy\s+\[(\w+\s+\w+)\]'
    boundary_line = '<match all>'
    send_key(device, "KEY_RIGHT", 4)
    send_key(device, "KEY_DOWN", 4)
    output = deviceObj.receive(boundary_line)
    output = escape_ansi(output)
    log.info(output)
    match = re.search(p3, output)
    if match:
        status = match.group(1).strip()
        if status == p1 or status == p2:
            log.info("Successfully verify_bios_Power_Restore_Policy: %s" % status)
        else:
            log.error("Current: %s mismatch expected: %s or %s" % (status, p1, p2))
            err_count += 1
    else:
        log.error("FAIL to get the patern: %s" % p3)
        err_count += 1
    if err_count:
        raise RuntimeError('verify_bios_Power_Restore_Policy')


def modify_bios_power_restore_policy(device, expected_result):
    ### Power On(always-on)|Power Off(always-off)|Last State(previous)
    log.debug('Entering modify_bios_power_restore_policy with args : %s' % (str(locals())))
    deviceObj = Device.getDeviceObject(device)
    err_count = 0
    p1 = 'AC Power Restore Policy\s+\[(\w+\s+\w+)\]'
    boundary_line = '<match all>'
    send_key(device, "KEY_UP", 1)
    send_key(device, "KEY_DOWN", 1)
    output = deviceObj.receive(boundary_line)
    output = escape_ansi(output)
    log.info(output)
    match = re.search(p1, output)
    if match:
        status = match.group(1).strip()
        print(status)
        log.info("Successfully get_bios_power_restore_policy: %s" % status)
    else:
        log.error("FAIL to get_bios_power_restore_policy")
        err_count += 1
    send_key(device, "KEY_ENTER", 1)
    if status == 'Power On' and expected_result == 'always-on':
        pass
    elif status == 'Power On' and expected_result == 'always-off':
        send_key(device, "KEY_DOWN", 1)
    elif status == 'Power On' and expected_result == 'previous':
        send_key(device, "KEY_DOWN", 2)
    elif status == 'Power Off' and expected_result == 'always-on':
        send_key(device, "KEY_UP", 1)
    elif status == 'Power Off' and expected_result == 'always-off':
        pass
    elif status == 'Power Off' and expected_result == 'previous':
        send_key(device, "KEY_DOWN", 1)
    elif status == 'Last State' and expected_result == 'always-on':
        send_key(device, "KEY_DOWN", 1)
    elif status == 'Last State' and expected_result == 'always-off':
        send_key(device, "KEY_UP", 1)
    elif status == 'Last State' and expected_result == 'previous':
        pass
    elif status == 'Power On' and expected_result == 'Power On':
        pass
    elif status == 'Power On' and expected_result == 'Power Off':
        send_key(device, "KEY_DOWN", 1)
    elif status == 'Power On' and expected_result == 'Last State':
        send_key(device, "KEY_DOWN", 2)
    elif status == 'Power Off' and expected_result == 'Power On':
        send_key(device, "KEY_UP", 1)
    elif status == 'Power Off' and expected_result == 'Power Off':
        pass
    elif status == 'Power Off' and expected_result == 'Last State':
        send_key(device, "KEY_DOWN", 1)
    elif status == 'Last State' and expected_result == 'Power On':
        send_key(device, "KEY_DOWN", 1)
    elif status == 'Last State' and expected_result == 'Power Off':
        send_key(device, "KEY_UP", 1)
    elif status == 'Last State' and expected_result == 'Last State':
        pass
    send_key(device, "KEY_ENTER", 1)
    send_key(device, "KEY_RIGHT", 3)
    whitebox_save_bios_setup(device)
    wait_prompt(device)
    if err_count:
        raise RuntimeError('modify_bios_power_restore_policy')


def ssh_command_verify_bmc_version(username, hostip, password, bmcip=None, bmcusername=None, \
                                   bmcpassword=None, remote=False, expected_result=None):
    log.debug("Entering ssh_command_verify_bmc_version with args : %s" % (str(locals())))
    err_count = 0
    p = r'Firmware Revision\s+:\s+(\S+)'
    if remote:
        cmd = 'ipmitool -H %s -U %s -P %s mc info' % (bmcip, bmcusername, bmcpassword)
        child = ssh_command(username, hostip, password, cmd)
        child.expect(pexpect.EOF, timeout=30)
        output = child.before.strip().decode('utf-8')
        log.info(output)
    else:
        cmd = 'ipmitool mc info'
        child = ssh_command(username, hostip, password, cmd)
        child.expect(pexpect.EOF, timeout=30)
        output = child.before.strip().decode('utf-8')
        log.info(output)
    match = re.search(p, output)
    if match:
        if expected_result != None:
            BMC_version = match.group(1).strip()
            if BMC_version == expected_result:
                log.info("Successfully ssh_command_verify_bmc_version: %s" % (BMC_version))
            else:
                log.error("ssh_bmc_version mismatch: %s, %s" % (BMC_version, expected_result))
                err_count += 1
    else:
        log.error("Fail to parse ssh_bmc_version")
        err_count += 1
    if err_count:
        raise RuntimeError('ssh_command_verify_bmc_version')


def ssh_command_verify_bmc_product_id(username, hostip, password, bmcip=None, bmcusername=None, \
                                      bmcpassword=None, remote=False, expected_result=None):
    log.debug("Entering ssh_command_verify_bmc_product_id with args : %s" % (str(locals())))
    err_count = 0
    p = r'Product ID\s+:\s+(\d+)\s+\S+'
    if remote:
        cmd = 'ipmitool -H %s -U %s -P %s mc info' % (bmcip, bmcusername, bmcpassword)
        child = ssh_command(username, hostip, password, cmd)
        child.expect(pexpect.EOF, timeout=30)
        output = child.before.strip().decode('utf-8')
        log.info(output)
    else:
        cmd = 'ipmitool mc info'
        child = ssh_command(username, hostip, password, cmd)
        child.expect(pexpect.EOF, timeout=30)
        output = child.before.strip().decode('utf-8')
        log.info(output)
    match = re.search(p, output)
    if match:
        if expected_result != None:
            product_id = match.group(1).strip()
            if product_id == expected_result:
                log.info("Successfully ssh_command_verify_bmc_product_id: %s" % (product_id))
            else:
                log.error("ssh_bmc_product_id mismatch: %s, %s" % (product_id, expected_result))
                err_count += 1
    else:
        log.error("Fail to parse ssh_bmc_product_id")
        err_count += 1
    if err_count:
        raise RuntimeError('ssh_command_verify_bmc_product_id')


def ssh_command_verify_mc_reset(username, hostip, password, bmcip=None, bmcusername=None, \
                                bmcpassword=None, remote=False, expected_result='cold'):
    log.debug("Entering ssh_command_verify_mc_reset with args : %s" % (str(locals())))
    err_count = 0
    p = r'Sent\s+(\w+)\s+reset command to MC'
    if remote:
        cmd = 'ipmitool -H %s -U %s -P %s mc reset %s' % (bmcip, bmcusername, bmcpassword, expected_result)
        child = ssh_command(username, hostip, password, cmd)
        child.expect(pexpect.EOF, timeout=30)
        output = child.before.strip().decode('utf-8')
        log.info(output)
    else:
        cmd = 'ipmitool mc reset %s' % (expected_result)
        child = ssh_command(username, hostip, password, cmd)
        child.expect(pexpect.EOF, timeout=30)
        output = child.before.strip().decode('utf-8')
        log.info(output)
    match = re.search(p, output)
    if match:
        status = match.group(1).strip()
        if status == expected_result:
            log.info("Successfully ssh_command_verify_mc_reset: %s" % (status))
        else:
            log.error("ssh_command_verify_mc_reset actual %s mismatch %s" % (status, expected_result))
            err_count += 1
    else:
        log.error("Fail to parse ssh_command_verify_mc_reset")
        err_count += 1
    if err_count:
        raise RuntimeError('ssh_command_verify_mc_reset')


def verify_set_sensor_threshold(device, cmd):
    ###sensor 01 used to be tested
    log.debug("Entering verify_set_sensor_threshold args : %s" % (str(locals())))
    deviceObj = Device.getDeviceObject(device)
    err_count = 0
    sensor_number = cmd.split()[4]
    list1 = cmd.split()[-6:]
    list8 = cmd.split()[:6]
    cmd2 = 'time ipmitool raw 04 0x27 %s' % (sensor_number)
    output = deviceObj.sendCmdRegexp(cmd2, Const.TIME_REG_PROMPT, timeout=30)
    list2 = (find_following_line(output, cmd2)).split()[-6:]
    list3 = []
    list6 = []
    list7 = []
    openbmc_lib.run_ipmi_set_cmd(device, cmd)
    output = deviceObj.sendCmdRegexp(cmd2, Const.TIME_REG_PROMPT, timeout=30)
    list4 = (find_following_line(output, cmd2)).split()[-6:]
    list5 = ['lower non-critical', 'lower critical', 'lower non-recoverable', 'upper non-critical', 'upper critical',
             'upper non-recoverable']
    i = 0
    while i <= 5:
        list6.append(str(parser_openbmc_lib.parse_hex_to_int(list2[i])))
        list7.append(str(parser_openbmc_lib.parse_hex_to_int(list4[i])))
        i += 1
    newlist6 = ['00' if x == '0' else x for x in list6]
    newlist7 = ['00' if x == '0' else x for x in list7]
    m = 0
    while m <= 5:
        if list1[m] != '00':
            list3.append(newlist6[m])
            if list1[m] == newlist7[m]:
                log.info("Successfully verify_Set_Sensor_Threshold: %s" % (list5[m]))
            else:
                log.error("%s: acctual %s mismatch expected %s " % (list5[m], newlist7[m], list1[m]))
                err_count += 1
        else:
            list3.append('00')
        m += 1
    cmd3 = '%s %s' % (" ".join(str(i) for i in list8), " ".join(str(i) for i in list3))
    openbmc_lib.run_ipmi_set_cmd(device, cmd3)
    if err_count:
        raise RuntimeError('verify_set_sensor_threshold')


def verify_get_sensor_threshold(device, cmd, expected_result):
    ###expected_result need to be followed the spec
    log.debug("Entering verify_get_sensor_threshold args : %s" % (str(locals())))
    deviceObj = Device.getDeviceObject(device)
    err_count = 0
    cmd1 = 'time ' + cmd
    output = deviceObj.sendCmdRegexp(cmd1, Const.TIME_REG_PROMPT, timeout=30)
    list1 = (find_following_line(output, cmd1)).split()[-6:]
    list2 = " ".join(str(i) for i in list1)
    if list2 == expected_result:
        log.info("Successfully verify_get_sensor_threshold: %s" % (list2))
    else:
        log.error("acctual: %s mismatch expected: %s " % (list2, expected_result))
        raise RuntimeError('verify_get_sensor_threshold')


def find_following_line(output, pattern):
    log.debug("Entering find_following_line args : %s" % (str(locals())))
    lines = output.splitlines()
    for i, line in enumerate(lines):
        if re.search(pattern, line):
            return lines[i + 1]


def verify_get_sensor_reading(device, cmd):
    ###expected_result need to be followed the spec
    log.debug("Entering verify_get_sensor_reading args : %s" % (str(locals())))
    deviceObj = Device.getDeviceObject(device)
    sensor_number = cmd.split()[4]
    cmd1 = 'time ' + cmd
    cmd2 = "time ipmitool sdr list|awk 'NR==%s'" % (sensor_number)
    output = deviceObj.sendCmdRegexp(cmd1, Const.TIME_REG_PROMPT, timeout=30)
    list1 = (find_following_line(output, cmd1)).split()[0]
    list2 = int(list1, 16)
    output = deviceObj.sendCmdRegexp(cmd2, Const.TIME_REG_PROMPT, timeout=30)
    list3 = (find_following_line(output, cmd2)).split('|')[1]
    list4 = int(list3.strip().split()[0])
    if list2 == list4:
        log.info("Successfully verify_get_sensor_reading, sensor number:%s value:%s" % (sensor_number, list2))
    else:
        log.error("acctual: %s mismatch expected: %s " % (list4, list2))
        raise RuntimeError('verify_get_sensor_reading')


def verify_read_fru_data(device, expected_result=None):
    log.debug("Entering verify_read_fru_data args : %s" % (str(locals())))
    deviceObj = Device.getDeviceObject(device)
    err_count = 0
    cmd1 = 'time ipmitool raw 0x0a 0x11 01 00 00 10'
    error_msg_1 = '00 00 00 00 00 00 00 00 00 00'
    error_msg_2 = 'FF FF FF FF FF FF FF FF FF FF'
    error_msg_3 = 'ff ff ff ff ff ff ff ff ff ff'
    error_msg = [error_msg_1, error_msg_2, error_msg_3]
    openbmc_lib.run_ipmi_set_cmd(device, cmd1)
    output = deviceObj.sendCmdRegexp(cmd1, Const.TIME_REG_PROMPT, timeout=30)
    list1 = (find_following_line(output, cmd1)).split()[-10:]
    Read_FRU_data = " ".join(str(i) for i in list1)
    log.info(Read_FRU_data)
    for msg in error_msg:
        if Read_FRU_data == msg:
            log.error("FRU_Date is abnormal:%s" % msg)
            err_count += 1
    if expected_result != None:
        if Read_FRU_data == expected_result:
            log.info("Successfully verify_read_fru_data: %s" % expected_result)
        else:
            log.error(
                "Fail to verify_read_fru_data, acctual:%s mismatch expected: %s" % (Read_FRU_data, expected_result))
            err_count += 1
    if err_count:
        raise RuntimeError('verify_read_fru_data')


def verify_write_fru_data(device, cmd):
    log.debug("Entering verify_write_fru_data args : %s" % (str(locals())))
    deviceObj = Device.getDeviceObject(device)
    err_count = 0
    sensor_number = cmd.split()[4]
    cmd1 = 'time ipmitool raw 0x0a 0x11 %s 00 00 0x10' % sensor_number
    output = deviceObj.sendCmdRegexp(cmd1, Const.TIME_REG_PROMPT, timeout=30)
    list1 = (find_following_line(output, cmd1)).split()[-15:]
    new_list1 = []
    loop_append_string_to_list(list1, new_list1, '0x')
    cmd2 = " ".join(str(i) for i in cmd.split()[0:7]) + ' ' + " ".join(str(i) for i in new_list1)
    openbmc_lib.run_ipmi_set_cmd(device, cmd)
    openbmc_lib.run_ipmi_set_cmd(device, cmd1)
    output = deviceObj.sendCmdRegexp(cmd1, Const.TIME_REG_PROMPT, timeout=30)
    list2 = (find_following_line(output, cmd1)).split()[-15:]
    list3 = cmd.split()[-15:]
    new_list3 = []
    loop_replace_string_to_list(list3, new_list3, '0x', '')
    if list2 == new_list3:
        log.info("Successfully verify_write_fru_data")
    else:
        log.error("Fail to verify_write_fru_data, acctual:%s mismatch expected: %s" % (list2, new_list3))
        err_count += 1
    ###write back the original FRU_Data
    openbmc_lib.run_ipmi_set_cmd(device, cmd2)
    output = deviceObj.sendCmdRegexp(cmd1, Const.TIME_REG_PROMPT, timeout=30)
    list4 = (find_following_line(output, cmd1)).split()[-15:]
    if list1 == list4:
        log.info("Successfully write_back_original_FRU_Data")
    else:
        log.error("Fail to write_back_original_FRU_Data, acctual:%s mismatch expected: %s" % (list1, list4))
        err_count += 1
    if err_count:
        raise RuntimeError('verify_write_fru_data')


def loop_append_string_to_list(previous, new, string):
    log.debug("Entering loop_append_string_to_list args : %s" % (str(locals())))
    for m in previous:
        m = string + m
        new.append(m)


def loop_replace_string_to_list(previous, new, previous_string, new_string, count=1):
    log.debug("Entering loop_replace_string_to_list args : %s" % (str(locals())))
    for n in previous:
        n = n.replace(previous_string, new_string, count)
        new.append(n)


def verify_partial_add_sdr(device, cmd):
    log.debug("Entering verify_partial_add_sdr args : %s" % (str(locals())))
    cmd1 = 'time ' + cmd
    output = deviceObj.sendCmdRegexp(cmd1, Const.TIME_REG_PROMPT, timeout=30)
    list1 = (find_following_line(output, cmd1)).split()
    new_list1 = []
    loop_append_string_to_list(list1, new_list1, '0x')
    cmd2 = 'ipmitool raw 0x0a 0x25 ' + " ".join(str(i) for i in new_list1) + ' 00 00 00 00 01 02 03 04'
    openbmc_lib.run_ipmi_set_cmd(device, cmd2)


def verify_get_privilege(device, cmd, expected_result='04'):
    ###0h=reserved  1h=CALLBACK level  2h=USER level  3h=OPERATOR level  4h=ADMINISTRATOR level  5h=OEM Proprietary level
    log.debug("Entering verify_get_privilege with args : %s" % (str(locals())))
    deviceObj = Device.getDeviceObject(device)
    cmd1 = 'time ' + cmd
    output = deviceObj.sendCmdRegexp(cmd1, Const.TIME_REG_PROMPT, timeout=30)
    current = (find_following_line(output, cmd1)).split()[1]
    if current == expected_result:
        log.info("Successfully verify_get_privilege")
    else:
        log.error("Fail to verify_get_privilege, acctual:%s mismatch expected: %s" % (current, expected_result))
        raise RuntimeError('verify_get_privilege')


def verify_set_privilege(device, user_id, privilege_level='ADMINISTRATOR'):
    ###0h=reserved  1h=CALLBACK  2h=USER  3h=OPERATOR 4h=ADMINISTRATOR  5h=OEM
    log.debug("Entering verify_set_privilege with args : %s" % (str(locals())))
    deviceObj = Device.getDeviceObject(device)
    err_count = 0
    if privilege_level == 'ADMINISTRATOR':
        privilege = '04'
    elif privilege_level == 'OPERATOR':
        privilege = '03'
    elif privilege_level == 'USER':
        privilege = '02'
    elif privilege_level == 'CALLBACK':
        privilege = '01'
    elif privilege_level == 'OEM':
        privilege = '05'
    elif privilege_level == 'reserved':
        privilege = '00'
    else:
        err_count += 1
        log.error("please input the legal privilege_level")
    cmd1 = 'time ipmitool user priv %s %s 1' % (user_id, privilege)
    output = deviceObj.sendCmdRegexp(cmd1, Const.TIME_REG_PROMPT, timeout=30)
    pass_msg = 'successful'
    match = re.search(pass_msg, output)
    if match:
        log.info("Successfully verify_set_privilege")
    else:
        log.error("Fail to set User%s privilege %s" % (user_id, privilege_level))
        err_count += 1
    count = int(user_id) + 1
    cmd2 = "time ipmitool user list 1|awk 'NR==%s'" % count
    output = deviceObj.sendCmdRegexp(cmd2, Const.TIME_REG_PROMPT, timeout=30)
    match = re.search(privilege_level, output)
    if match:
        log.info("Successfully set privilege to %s" % privilege_level)
    else:
        log.error("Fail to set privilege to %s" % privilege_level)
        err_count += 1
    if err_count:
        raise RuntimeError('verify_set_privilege')


def verify_clear_sdr_repository(device, cmd):
    log.debug("Entering verify_clear_sdr_repository with args : %s" % (str(locals())))
    deviceObj = Device.getDeviceObject(device)
    cmd1 = 'time ' + cmd
    output = deviceObj.sendCmdRegexp(cmd1, Const.TIME_REG_PROMPT, timeout=30)
    list1 = (find_following_line(output, cmd1)).split()
    new_list1 = []
    loop_append_string_to_list(list1, new_list1, '0x')
    cmd2 = 'ipmitool raw 0x0a 0x27 ' + " ".join(str(i) for i in new_list1) + ' 0x43 0x4c 0x52 0xaa'
    openbmc_lib.run_ipmi_set_cmd(device, cmd2)


def verify_user_privilege(device, bmcip):
    log.debug("Entering verify_user_privilege with args : %s" % (str(locals())))
    deviceObj = Device.getDeviceObject(device)
    ###add user 3
    cmd1 = 'ipmitool user set name 3 tester'
    cmd2 = 'ipmitool user set password 3 test'
    cmd3 = 'ipmitool user enable 3'
    cmd4 = 'ipmitool raw 6 0x43 0x91 3 4 0'
    verify_ipmi_set_cmd(device, cmd1)
    verify_ipmi_set_cmd(device, cmd2)
    verify_ipmi_set_cmd(device, cmd3)
    verify_ipmi_set_cmd(device, cmd4)
    verify_set_privilege(device, 3, 'ADMINISTRATOR')
    cmd5 = 'ipmitool -L administrator -H %s -U %s -P %s user set name 6 sky' % (bmcip, 'tester', 'test')
    cmd6 = 'ipmitool -L operator -H %s -U %s -P %s raw 6 0x24 01 03 00 0x3e 0x58 02' % (bmcip, 'tester', 'test')
    cmd7 = 'ipmitool -L operator -H %s -U %s -P %s raw 6 0x22' % (bmcip, 'tester', 'test')
    cmd8 = 'ipmitool -L user -H %s -U %s -P %s raw 6 0x25' % (bmcip, 'tester', 'test')
    verify_ipmi_set_cmd(device, cmd5)
    verify_ipmi_set_cmd(device, cmd6)
    verify_ipmi_set_cmd(device, cmd7)
    verify_ipmi_set_cmd(device, cmd8)
    verify_set_privilege(device, 3, 'OPERATOR')
    verify_ipmi_set_cmd(device, cmd5, expected='establish fail')
    verify_ipmi_set_cmd(device, cmd6)
    verify_ipmi_set_cmd(device, cmd7)
    verify_ipmi_set_cmd(device, cmd8)
    verify_set_privilege(device, 3, 'USER')
    verify_ipmi_set_cmd(device, cmd5, expected='establish fail')
    verify_ipmi_set_cmd(device, cmd6, expected='establish fail')
    verify_ipmi_set_cmd(device, cmd7, expected='establish fail')
    verify_ipmi_set_cmd(device, cmd8)


def verify_ipmi_set_cmd(device, cmd, test_name='None', expected='normal'):
    log.debug("Entering verify_ipmi_set_cmd with args : %s" % (str(locals())))
    deviceObj = Device.getDeviceObject(device)
    err_count = 0
    if test_name == 'None':
        test_name = 'verify_ipmi_set_cmd'
    error_msg = ['Unable to establish', '.*No such file or directory']
    error_msg_1 = 'Requested privilege level exceeds limit'
    match_error_list = []
    cmd1 = 'time ' + cmd
    output = deviceObj.sendCmdRegexp(cmd1, Const.TIME_REG_PROMPT, timeout=30)
    if expected == 'normal':
        parsed_output = parserOpenbmc.parse_oem_rsp_code(output)
        for msg in error_msg:
            match_error = re.search(msg, output)
            if match_error:
                match_error_list.append(match_error.group(0))
        time.sleep(1)
        if not parsed_output and not match_error_list:
            log.success("Successfully %s, execute \'%s\'" % (test_name, cmd))
        elif match_error_list:
            err_count += 1
            log.fail(output)
        elif "invalid" in parsed_output:
            err_count += 1
            log.fail("Invalid command: %s" % (parsed_output["invalid"]))
        elif parsed_output["code"]:
            err_count += 1
            log.fail("Command error: rsp=\'%s\', \'%s\'\n" % (parsed_output["code"], parsed_output["message"]))
        else:
            log.fail("Unknown error")
            err_count += 1
    elif expected == 'establish fail':
        match_error = re.search(error_msg_1, output)
        if match_error:
            log.success("Successfully %s, expect to establish fail" % test_name)
        else:
            log.fail(output)
            err_count += 1
    else:
        log.fail("Please input the right expected result: normal|establish fail")
        err_count += 1
    if err_count:
        raise testFailed("Failed %s" % (test_name))


def verify_get_sel_allocation_info(device, cmd, expected_result):
    ### check the return value from byte 1-4
    log.debug("Entering verify_get_sel_allocation_info with args : %s" % (str(locals())))
    deviceObj = Device.getDeviceObject(device)
    err_count = 0
    cmd1 = 'time ' + cmd
    output = deviceObj.sendCmdRegexp(cmd1, Const.TIME_REG_PROMPT, timeout=30)
    list1 = (find_following_line(output, cmd1)).split()[0:4]
    rsp = " ".join(str(i) for i in list1)
    if rsp == expected_result:
        log.success("Successfully verify_get_sel_allocation_info")
    else:
        log.error("Fail to verify_get_sel_allocation_info, acctual:%s mismatch expected: %s" % (rsp, expected_result))
        raise testFailed("Failed verify_get_sel_allocation_info")


def verify_get_sel_info(hostip, username, userpassword, expected_result):
    log.debug("Entering verify_get_sel_info with args : %s" % (str(locals())))
    err_count = 0
    cmd1 = 'ipmitool sel list|wc -l'
    output = parse_ssh_command_cmd(username, hostip, userpassword, cmd1)
    cmd2 = "ipmitool sel list|awk 'NR==%s'" % output
    sel_data = parse_sel_info_data(hostip, username, userpassword, cmd2)
    cmd3 = 'ipmitool raw 0x0a 0x40'
    output = parse_ssh_command_cmd(username, hostip, userpassword, cmd3)
    raw_data_1 = " ".join(output.split()[0:1])
    raw_data_2 = " ".join(output.split()[1:3])
    if raw_data_1 == expected_result:
        log.success("Successfully verify_get_sel_info: byte1 = %s" % expected_result)
    else:
        log.error("FAIL: raw_data byte1 %s mismatch expected %s" % (raw_data_1, expected_result))
        err_count += 1
    if raw_data_2 == sel_data:
        log.success("Successfully verify_get_sel_info: byte2-3: %s" % raw_data_2)
    else:
        log.error("FAIL: raw_data byte2-3 %s mismatch sel_data %s" % (raw_data_2, sel_data))
        err_count += 1
    if err_count:
        raise testFailed("Failed verify_get_sel_info")


def parse_sel_info_data(hostip, username, userpassword, cmd):
    log.debug("Entering parse_sel_info_data with args : %s" % (str(locals())))
    p = r'^(\S+)\s+.+'
    err_count = 0
    output = parse_ssh_command_cmd(username, hostip, userpassword, cmd)
    match = re.search(p, output)
    if match:
        value = match.group(1).strip()
        if len(value) == 1:
            new_value = '0' + value + ' 00'
            return new_value
        elif len(value) == 2:
            new_value = value + ' 00'
            return new_value
        elif len(value) == 3:
            new_value_1 = '0' + value
            new_value = "".join(list(new_value_1)[-2:]) + ' ' + "".join(list(new_value_1)[0:2])
            return new_value
        elif len(value) == 4:
            new_value = "".join(list(value)[-2:]) + ' ' + "".join(list(value)[0:2])
            return new_value
        else:
            log.error("the value is not correct, please check it maually")
            err_count += 1
    else:
        log.error("can't match your pattern")
        err_count += 1
    if err_count:
        raise testFailed("Failed parse_sel_info_data")


def verify_get_sel_entry(hostip, username, userpassword):
    log.debug("Entering verify_get_sel_entry with args : %s" % (str(locals())))
    err_count = 0
    cmd1 = 'ipmitool sel list|wc -l'
    output = parse_ssh_command_cmd(username, hostip, userpassword, cmd1)
    cmd2 = "ipmitool sel list|awk 'NR==%s'" % output
    cmd3 = "ipmitool sel list|awk 'NR==1'"
    sel_data_last = parse_sel_info_data(hostip, username, userpassword, cmd2)
    sel_data_first = parse_sel_info_data(hostip, username, userpassword, cmd3)
    log.info(sel_data_last)
    log.info(sel_data_first)
    ###get last entry
    cmd4 = 'ipmitool raw 0x0a 0x43 00 00 0xff 0xff 00 0xff'
    output = parse_ssh_command_cmd(username, hostip, userpassword, cmd4)
    raw_data_last = " ".join(output.split()[2:4])
    ###get first entry
    cmd5 = 'ipmitool raw 0x0a 0x43 00 00 00 00 00 0xff'
    output = parse_ssh_command_cmd(username, hostip, userpassword, cmd5)
    raw_data_first = " ".join(output.split()[2:4])
    log.info(raw_data_last)
    log.info(raw_data_first)
    if sel_data_last == raw_data_last:
        log.success("Successfully verify_Get_SEL_last_entry: byte3-4: %s" % raw_data_last)
    else:
        log.error("sel_data_last: %s mismatch raw_data_last: %s" % (sel_data_last, raw_data_last))
        err_count += 1
    if sel_data_first == raw_data_first:
        log.success("Successfully verify_get_sel_first_entry: byte3-4: %s" % raw_data_first)
    else:
        log.error("sel_data_first: %s mismatch raw_data_first: %s" % (sel_data_first, raw_data_first))
        err_count += 1
    if err_count:
        raise testFailed("Failed verify_get_sel_entry")


def parse_ssh_command_cmd(username, hostip, userpassword, cmd, title_p=False):
    log.debug("Entering parse_ssh_command_cmd with args : %s" % (str(locals())))
    child = ssh_command(username, hostip, userpassword, cmd, title_p=title_p)
    child.expect(pexpect.EOF, timeout=30)
    output = child.before.strip().decode('utf-8')
    log.info(output)
    return output


def verify_add_sel_entry(device, hostip, username, userpassword):
    log.debug("Entering verify_add_sel_entry with args : %s" % (str(locals())))
    deviceObj = Device.getDeviceObject(device)
    err_count = 0
    cmd1 = 'ipmitool sel list|wc -l'
    count_first = parse_ssh_command_cmd(username, hostip, userpassword, cmd1)
    ###add memory Correctable ECC logging limit reached sel log
    cmd2 = 'ipmitool raw 0x0a 0x44 00 04 02 0xf3 02 34 56 01 80 04 12 00 0x6f 05 00 00'
    verify_ipmi_set_cmd(device, cmd2)
    count_last = parse_ssh_command_cmd(username, hostip, userpassword, cmd1)
    p = 'Memory'
    if int(count_first) + 1 == int(count_last):
        log.success("Successfully create a sel log")
    else:
        log.error("fail to create a sel log")
        err_count += 1
    cmd3 = 'time ipmitool sel list'
    output = deviceObj.sendCmdRegexp(cmd3, Const.TIME_REG_PROMPT, timeout=30)
    match = re.search(p, output)
    if match:
        log.success("Successfully create sel log related to memory")
    else:
        log.error("FAIL: the sel log is not related to memory")
        err_count += 1
    if err_count:
        raise testFailed("Failed verify_add_sel_entry")


def verify_delete_sel_entry(device, hostip, username, userpassword):
    log.debug("Entering verify_delete_sel_entry with args : %s" % (str(locals())))
    deviceObj = Device.getDeviceObject(device)
    cmd1 = 'ipmitool sel list|wc -l'
    count_first = parse_ssh_command_cmd(username, hostip, userpassword, cmd1)
    cmd2 = 'ipmitool raw 0x0a 0x42'
    value = get_rsp_ipmi_cmd(device, cmd2)
    cmd3 = 'ipmitool raw 0x0a 0x46 0x%s 0x%s 0xff 0xff' % (value.split()[0], value.split()[1])
    verify_ipmi_set_cmd(device, cmd3)
    count_last = parse_ssh_command_cmd(username, hostip, userpassword, cmd1)
    if int(count_first) - 1 == int(count_last):
        log.success("Successfully delete a sel log")
    else:
        log.error("fail to delete a sel log")
        raise testFailed("Failed verify_delete_sel_entry")


def get_rsp_ipmi_cmd(device, cmd):
    log.debug("Entering get_rsp_ipmi_cmd with args : %s" % (str(locals())))
    deviceObj = Device.getDeviceObject(device)
    err_count = 0
    cmd1 = 'time ' + cmd
    output = deviceObj.sendCmdRegexp(cmd1, Const.TIME_REG_PROMPT, timeout=30)
    result = parserOpenbmc.parse_oem_output(output)
    return result


def verify_clear_sel(device, expected_result):
    log.debug("Entering verify_clear_sel with args : %s" % (str(locals())))
    deviceObj = Device.getDeviceObject(device)
    cmd1 = 'ipmitool raw 0x0a 0x42'
    value = get_rsp_ipmi_cmd(device, cmd1)
    cmd2 = 'ipmitool raw 0x0a 0x47 0x%s 0x%s 0x43 0x4c 0x52 0xaa' % (value.split()[0], value.split()[1])
    rsp = get_rsp_ipmi_cmd(device, cmd2)
    if rsp == expected_result:
        log.success("Successfully verify_clear_sel")
    else:
        log.error("fail to verify_clear_sel")
        raise testFailed("Failed verify_clear_sel")


def verify_get_sel_time(device):
    log.debug("Entering verify_get_sel_time with args : %s" % (str(locals())))
    deviceObj = Device.getDeviceObject(device)
    cmd1 = 'ln -sf /usr/share/zoneinfo/Europe/London /etc/localtime'
    cmd2 = 'ln -sf /usr/share/zoneinfo/Asia/Shanghai /etc/localtime'
    cmd3 = 'ipmitool raw 0x0a 0x48'
    deviceObj.sendCmd(cmd1)
    time.sleep(1)
    value = get_rsp_ipmi_cmd(device, cmd3)
    value_1 = value.split()
    value_1.reverse()
    value_2 = '0x' + "".join(value_1)
    cmd4 = 'echo $((%s))' % value_2
    value_3 = get_rsp_ipmi_cmd(device, cmd4)
    cmd5 = 'time ipmitool sel time get'
    output = deviceObj.sendCmdRegexp(cmd5, Const.TIME_REG_PROMPT, timeout=30)
    date = " ".join((find_following_line(output, cmd5)).split()[0:2])
    cmd6 = "date -d '%s' " % date + '+%s'
    value_4 = get_rsp_ipmi_cmd(device, cmd6)
    deviceObj.sendCmd(cmd2)
    time.sleep(1)
    if 0 <= int(value_4) - int(value_3) <= 1:
        log.success("Successfully verify_get_sel_time")
    else:
        log.error("fail to verify_get_sel_time, %s mismatch %s" % (cmd6, cmd3))
        raise testFailed("Failed verify_get_sel_time")


def verify_set_sel_time(device):
    log.debug("Entering verify_set_sel_time with args : %s" % (str(locals())))
    deviceObj = Device.getDeviceObject(device)
    cmd1 = 'ln -sf /usr/share/zoneinfo/Europe/London /etc/localtime'
    cmd2 = 'ln -sf /usr/share/zoneinfo/Asia/Shanghai /etc/localtime'
    cmd3 = 'ipmitool raw 0x0a 0x48'
    cmd4 = 'ipmitool raw 0x0a 0x49 00 00 00 00'
    deviceObj.sendCmd(cmd1)
    time.sleep(1)
    verify_ipmi_set_cmd(device, cmd4)
    value = get_rsp_ipmi_cmd(device, cmd3)
    value_1 = value.split()
    value_1.reverse()
    value_2 = '0x' + "".join(value_1)
    cmd4 = 'echo $((%s))' % value_2
    value_3 = get_rsp_ipmi_cmd(device, cmd4)
    deviceObj.sendCmd(cmd2)
    time.sleep(1)
    if int(value_3) < 5:
        log.success("Successfully verify_set_sel_time")
    else:
        log.error("fail to verify_set_sel_time: %s" % value_3)
        raise testFailed("Failed verify_set_sel_time")


def verify_set_sel_time_utc_offset(device, cmd):
    log.debug("Entering verify_set_sel_time_utc_offset with args : %s" % (str(locals())))
    deviceObj = Device.getDeviceObject(device)
    err_count = 0
    cmd1 = 'ipmitool raw 0xa 0x5c'
    original_value = get_rsp_ipmi_cmd(device, cmd1)
    cmd2 = 'ipmitool raw 0xa 0x5d 0x%s 0x%s' % (original_value.split()[0], original_value.split()[1])
    verify_ipmi_set_cmd(device, cmd)
    list1 = cmd.split()[-2:]
    new_list1 = []
    loop_replace_string_to_list(list1, new_list1, '0x', '')
    expected_result = " ".join(new_list1)
    value = get_rsp_ipmi_cmd(device, cmd1)
    if value == expected_result:
        log.success("Successfully verify_set_sel_time_utc_offset")
    else:
        log.error("FAIL, acctual: %s mismatch expected: %s" % (value, expected_result))
        err_count += 1
    verify_ipmi_set_cmd(device, cmd2)
    value_1 = get_rsp_ipmi_cmd(device, cmd1)
    if value_1 == original_value:
        log.success("Successfully write back sel_time_utc_offset")
    else:
        log.error("Write back FAIL, acctual: %s mismatch expected: %s" % (value_1, original_value))
        err_count += 1
    if err_count:
        raise testFailed("Failed verify_set_sel_time_utc_offset")


def delete_arp(device, ipaddr):
    log.debug("Entering delete_arp with args : %s" % (str(locals())))
    deviceObj = Device.getDeviceObject(device)
    cmd = 'arp -d %s' % ipaddr
    cmd1 = 'time arp -n'
    if not need_delete_arp(device, ipaddr):
        log.info("Not found arp %s, no need delete." % ipaddr)
        return
    verify_ipmi_set_cmd(device, cmd)
    output = deviceObj.sendCmdRegexp(cmd1, Const.TIME_REG_PROMPT, timeout=30)
    match = re.search(ipaddr, output)
    if match:
        log.error("delete_arp FAIL, %s is still there." % ipaddr)
        raise testFailed("Failed delete_arp")
    else:
        log.success("Successfully delete_arp")


def need_delete_arp(device, ipaddr):
    log.debug('Entering procedure need_delete_arp with args : %s\n' % (str(locals())))
    deviceObj = Device.getDeviceObject(device)
    err_count = 0
    cmd = 'time arp -n'
    output = deviceObj.sendCmdRegexp(cmd, Const.TIME_REG_PROMPT, timeout=30)
    match = re.search(ipaddr, output)
    if match:
        err_count += 1
    else:
        pass
    return True if err_count > 0 else False


def verify_set_bmc_lan_arp_respond(device, cmd, expected_result='on'):
    log.debug('Entering procedure verify_set_bmc_lan_arp_respond with args : %s\n' % (str(locals())))
    deviceObj = Device.getDeviceObject(device)
    if expected_result == 'on':
        p = 'Enabling BMC-generated ARP responses'
    else:
        p = 'Disabling BMC-generated ARP responses'
    cmd1 = 'time ' + cmd
    output = deviceObj.sendCmdRegexp(cmd1, Const.TIME_REG_PROMPT, timeout=30)
    match = re.search(p, output)
    if match:
        log.success("Successfully verify_set_bmc_lan_arp_respond")
    else:
        log.error("verify_set_bmc_lan_arp_respond FAIL")
        raise testFailed("Failed verify_set_bmc_lan_arp_respond")


def whitebox_exec_ping(device, ipAddress, count, mode, expected='None'):
    log.debug("Entering whitebox_exec_ping with args : %s" % (str(locals())))
    log.debug("Execute the ping from Device:%s to ip:%s" % (device, ipAddress))
    deviceObj = Device.getDeviceObject(device)
    cmd = "ping %s -c %s" % (ipAddress, str(count))
    success_msg = str(count) + ' packets transmitted, ' + str(count) + ' (packets )?received, 0% packet loss'
    loss_msg = '100% packet loss'

    output = deviceObj.executeCmd(cmd, mode=mode, timeout=30)
    log.info('output: %s' % (output))
    if expected == 'None':
        match = re.search(success_msg, output)
        if match:
            log.success("Found: %s" % (match.group(0)))
            log.success("ping to %s" % ipAddress)
        else:
            log.fail("ping to %s" % ipAddress)
            raise RuntimeError("Ping to destination IP address failed")
    elif expected == 'loss':
        match = re.search(loss_msg, output)
        if match:
            log.success("Found: %s" % (match.group(0)))
            log.success("ping to " + ipAddress + " get 100% packet loss")
        else:
            log.fail("ping to " + ipAddress + " did not get 100% packet loss")
            raise RuntimeError("Ping to destination IP address with loss expected failed")


def verify_bmc_lan_info(device, cmd, expected):
    log.debug('Entering procedure verify_bmc_lan_info with args : %s\n' % (str(locals())))
    deviceObj = Device.getDeviceObject(device)
    err_count = 0
    cmd1 = 'time ' + cmd
    output = deviceObj.sendCmdRegexp(cmd1, Const.TIME_REG_PROMPT, timeout=30)
    log.info('output: %s' % (output))
    for (k, v) in expected.items():
        p = '%s\s+:\s+(.+)' % k
        match = re.search(p, output)
        if match:
            value = match.group(1).strip()
            if value == v:
                log.success("Successfully verify_bmc_lan_info: expected[%s]=%s" % (k, v))
            else:
                err_count += 1
                log.fail("%s acctual: %s mismatch expected: %s" % (k, value, v))
        else:
            err_count += 1
            log.error("Can't find %s in the log" % k)
    if err_count:
        raise testFailed("Failed verify_bmc_lan_info")


def verify_bmc_api_call_test(device, cmd, expected='valid'):
    ###invalid|valid
    log.debug('Entering procedure verify_bmc_api_call_test with args : %s\n' % (str(locals())))
    deviceObj = Device.getDeviceObject(device)
    err_count = 0
    cmd1 = 'time ' + cmd
    p = '{.+}'
    p1 = 'Invalid API Call'
    p2 = 'ok'
    p3 = 'error'
    output = deviceObj.sendCmdRegexp(cmd1, Const.TIME_REG_PROMPT, timeout=30)
    match = re.search(p, output)
    if match:
        value = match.group(0).strip()
    else:
        err_count += 1
        log.error("The command doesn't work, please check it again.")
    d = json.loads(value)
    if expected == 'invalid':
        match = re.search(p1, value)
        if match:
            log.success("Successfully verify_bmc_api_call_test, expected error: %s" % p1)
        else:
            err_count += 1
            log.fail("Not found %s" % p1)
    elif expected == 'valid':
        match = re.search(p2, value)
        if match:
            log.success("Successfully verify_bmc_api_call_test, expected %s" % p2)
        else:
            err_count += 1
            log.fail("Not found %s" % p2)
            match = re.search(p3, value)
            if match:
                err_count += 1
                log.fail("Found error: %s" % d['error'])
    else:
        err_count += 1
        log.fail("please input the correct expected keyword")
    if err_count:
        raise testFailed("Failed verify_bmc_api_call_test")


def get_web_session_id(device, cmd):
    log.debug('Entering procedure get_web_session_id with args : %s\n' % (str(locals())))
    deviceObj = Device.getDeviceObject(device)
    err_count = 0
    cmd1 = 'time ' + cmd
    p = 'Set-Cookie:\s+QSESSIONID=(\S+);'
    output = deviceObj.sendCmdRegexp(cmd1, Const.TIME_REG_PROMPT, timeout=30)
    json_str = parse_json_string3(output)
    #    json = parser_openbmc_lib.parse_json_object(json_str)
    verify_output_from_curl(json_str)
    match = re.search(p, output)
    if match:
        Web_Session_ID = match.group(1).strip()
        log.success("Successfully get_web_session_id: %s" % Web_Session_ID)
        print(Web_Session_ID)
        return Web_Session_ID
    else:
        log.error("Not found %s" % p)
        raise testFailed("Failed get_web_session_id")


def verify_web_session_id(ID1, ID2):
    log.debug('Entering procedure verify_web_session_id with args : %s\n' % (str(locals())))
    if ID1 != ID2:
        log.success("Successfully verify_web_session_id, ID1:%s mismatch ID2:%s" % (ID1, ID2))
    else:
        log.fail("Fail unexpected ID1:%s==ID2:%s" % (ID1, ID2))
        raise testFailed("Failed verify_web_session_id")


def verify_output_from_curl(output, expected='ok'):
    log.debug('Entering procedure verify_output_from_curl with args : %s\n' % (str(locals())))
    p1 = 'ok'
    p2 = 'error'
    err_count = 0
    json = parser_openbmc_lib.parse_json_object(output)
    if expected == 'ok':
        match = re.search(p1, output)
        if match:
            log.success("Successfully verify_output_from_curl, expected %s" % p1)
        else:
            err_count += 1
            log.fail("Not found %s" % p1)
            match = re.search(p2, output)
            if match:
                err_count += 1
                log.fail("Found error: %s" % json['error'])
    elif expected == 'error':
        match = re.search(p2, output)
        if match:
            log.success("Successfully verify_output_from_curl, expected %s: %s" % (p2, json['error']))
        else:
            err_count += 1
            log.fail("Not found %s" % p2)
    else:
        err_count += 1
        log.fail("please input the correct expected keyword")
    if err_count:
        raise testFailed("Failed verify_output_from_curl")


def parse_json_string3(output):
    log.debug('Entering procedure parse_json_string3 with args : %s\n' % (str(locals())))
    p = '{.+}'
    match = re.search(p, output)
    if match:
        json_str = match.group(0).strip()
        return json_str
    else:
        log.error("Not found %s from output." % p)
        raise testFailed("Failed parse_json_string3")


def verify_get_session_challenge(device, bmcip, bmcusername='admin', bmcpassword='admin'):
    log.debug('Entering procedure verify_get_session_challenge with args : %s\n' % (str(locals())))
    deviceObj = Device.getDeviceObject(device)
    err_count = 0
    list1 = []
    list1 = [parser_openbmc_lib.parse_string_to_hex(i) for i in bmcusername.split()]
    [list1.append('00') for i in range(0, 16 - len(bmcusername))]
    cmd1 = " ".join(list1)
    cmd = 'ipmitool -H %s -U %s -P %s raw 0x6 0x39 2 %s' % (bmcip, bmcusername, bmcpassword, cmd1)
    verify_ipmi_set_cmd(device, cmd)


def set_wait(wait_time):
    log.info("[%s]: pls wait %s s" % (datetime.now(), wait_time))
    time.sleep(float(wait_time))


def common_parsing(response):
    """
    Parse strings similar to Set in progress: set-complete and return list(dict())
    :param response: the string to be parsed
    :return: return list(dict())
    """
    try:
        a = response.split("\n")
        b = list()
        for i in a:
            print(i)
            if i == "":
                continue
            else:
                key = (i.split(":")[0]).strip()
                value = (i.split(":")[1]).strip()
                b.append({key: value})
        return b
    except Exception as E:
        PRINTE("Fail! Non-compliant string:%s" % E)


def set_power_status(device, status, ip=None, connection=False):
    """
    OS
    On the PC, send 'ipmitest chassis power' to bmc (bmc is not powered off) to power on and off the system
    :param device: the name of the tested product
    :param status:on/off/reset/cycle
    :param ip: BMC IP of the tested product
    :param connection:Whether to connect DUT
    """
    status = status.lower()
    device_obj = Device.getDeviceObject(device)
    if ip:
        cmd = "ipmitool -I lanplus -H %s -U admin -P admin chassis power %s" % (ip, status)
        Device.execute_local_cmd(device_obj, cmd)
    else:
        cmd = "ipmitool chassis power %s" % status
        openbmc_lib.execute(device_obj, cmd, mode=CENTOS_MODE)
    if connection:
        connect(device)


def check_bmc_version(device, cmd, version):
    """
    Check whether the Firmware Revision field of the BMC version information meets expectations
    :param device: the name of the tested product
    :param cmd: cmd command for product check BMC version information
    :param version: expected version information
    """
    log.debug('Entering procedure check_bmc_version with args : %s\n' % (str(locals())))
    device_obj = Device.getDeviceObject(device)
    res = openbmc_lib.execute(device_obj, cmd, mode=CENTOS_MODE)
    log.cprint(res)
    re_version = r'Firmware Revision\s+:\s+(\S+)'
    bmc_version = re.findall(re_version, res)
    if bmc_version:
        if bmc_version[0] == str(version):
            log.info("Successfully verify_BMC_version: %s" % bmc_version)
        else:
            PRINTE("BMC_version Not Equal: %s, exp_version:%s" % (bmc_version, version))
    else:
        PRINTE("Fail to parse BMC_version:Not Found Keyword [Firmware Revision]")


def check_reset_sel_info(device, ip=None, restart_method=None):
    """
    check warm reset sel list info,must be including some information
    "Entity Presence", "Power Supply", "System ACPI Power State"
    :param device: the name of the tested product
    :param ip: bmc ip
    :param restart_method: warm/reboot/AC/cycle/off_on.Used to represent the number of 'System Event' events.
                           warm=0, reboot/AC/cycle/off_on==2,4, off=2
    """
    error_flag = False
    device_obj = Device.getDeviceObject(device)
    if ip:
        cmd = "ipmitool -I lanplus -H %s -U admin -P admin sel list" % ip
        res = Device.execute_local_cmd(device_obj, cmd)
    else:
        cmd = r"ipmitool sel list"
        res = openbmc_lib.execute(device_obj, cmd, mode=CENTOS_MODE)
    info_list = str(res).split("\n")
    cmd1 = "ipmitool raw 0x32 0x8f 0x07"
    res_1 = openbmc_lib.execute(device_obj, cmd1, mode=CENTOS_MODE)
    log.info("Get response:\n%s" % res_1)
    element_name_list = list()
    for i in info_list:
        record_list = i.split("|")
        if len(record_list) > 3:
            element_name = record_list[3].strip()
            if "#" in element_name:
                element_name = element_name.split("#")[0].strip()
            element_name_list.append(element_name)
    # When a large number of test cases are tested, the list variable will receive the
    # impact of the previous use case. And add new keyword. such as 'Event Logging Disabled'
    while "Event Logging Disabled" in exp_reset_sel_list:
        exp_reset_sel_list.remove("Event Logging Disabled")
    exp_element_list = exp_reset_sel_list
    if "Event Logging Disabled" in element_name_list:
        log.info("'Event Logging Disabled' was in 'sel list'! sel list response:\n%s" % res)
        exp_element_list.append("Event Logging Disabled")
    # Increase the judgment of the number of System Event events according to the restart method-BG
    if restart_method is not None:
        exp_element_list.append("System Event")
        if restart_method.lower() == "warm":
            event_sel_num = 0
            if element_name_list.count("System Event") != event_sel_num:
                PRINTE("Fail! Restart method is: '%s', the number of 'System Event' in the sel event is "
                       "expected to be: %s , Actually:%s. Response:\n%s"
                       % (restart_method, event_sel_num, element_name_list.count("System Event"), res))
        elif restart_method.lower() == "reboot":
            event_sel_num = 2   # or 4
            if element_name_list.count("System Event") != event_sel_num and \
                    element_name_list.count("System Event") != event_sel_num * 2:
                PRINTE("Fail! Restart method is: '%s', the number of 'System Event' in the sel event is "
                       "expected to be: %s(or x2) , Actually:%s. Response:\n%s"
                       % (restart_method, event_sel_num, element_name_list.count("System Event"), res))
        elif restart_method.lower() == "off":
            event_sel_num = 2
            if element_name_list.count("System Event") != event_sel_num:
                PRINTE("Fail! Restart method is: '%s', the number of 'System Event' in the sel event is "
                       "expected to be: %s , Actually:%s. Response:\n%s"
                       % (restart_method, event_sel_num, element_name_list.count("System Event"), res))
    # Increase the judgment of the number of System Event events according to the restart method-ED
        if restart_method.lower() != "warm":
            a = [x for x in element_name_list if x not in exp_element_list]
            b = [x for x in exp_element_list if x not in element_name_list]
            if a:
                error_flag = True
                PRINTE("Fail! Unknown information in the sel list:%s" % a, decide=False)
            if b:
                error_flag = True
                PRINTE("Fail! Missing fixed information in sel list:%s" % b, decide=False)
            if error_flag:
                PRINTE("Fail! sel list information doesn't meet expectations. sel list:\n%s" % res)


def set_reset_type(device, cmd, reset_type, check_sel_info=True):
    """
    Set the cold/hot start of the device under test
    :param device: product name
    :param reset_type: start method [cold,warm]
    :param cmd: cold/hot start command
    :param check_sel_info: check the sel info
    """
    if reset_type.lower() not in ["cold", "warm"]:
        PRINTE("Fail! set_reset_type args error, must be 'cold' or 'warm'")
    ip = get_ip_address_from_ipmitool(device)
    device_obj = Device.getDeviceObject(device)
    if check_sel_info:
        set_sel_clear(device, ip)
    res = openbmc_lib.execute(device_obj, cmd, mode=CENTOS_MODE)
    log.info("After 40 seconds, try to connect to DUT")
    time.sleep(40)
    if "Sent %s reset command to MC" % reset_type in res:
        check_bmc_ready(device)
        cmd = r"ipmitool mc info"
        res = openbmc_lib.execute(device_obj, cmd, mode=CENTOS_MODE)
        if "Device ID" in res:
            log.info("Pass! Switch To Cpu: Done")
            if check_sel_info:
                ip = get_ip_address_from_ipmitool(device)
                a = "warm" if reset_type.lower() == "warm" else "reboot"
                check_reset_sel_info(device, ip, a)
    else:
        PRINTE("Fail! set_reset_type  cmd:[%s]" % cmd)


def set_user_name(device, user_id, name):
    """
    Set (modify) account name as expected name
    :param device: the name of the tested product
    :param user_id: account number being set (modified)
    :param name: expected name
    """
    log.debug('Entering procedure set_user_name with args : %s\n' % (str(locals())))
    cmd = 'ipmitool user set name %s %s' % (str(user_id), name)
    try:
        device_obj = Device.getDeviceObject(device)
        openbmc_lib.execute(device_obj, cmd, mode=CENTOS_MODE)
        log.info("Pass! %s" % cmd)
    except Exception:
        PRINTE("Fail! Change user_id %s fail" % str(user_id))


def get_bmc_user_list(device, cmd):
    """
    get User List from BMC
    """
    device_obj = Device.getDeviceObject(device)
    res = openbmc_lib.execute(device_obj, cmd, mode=CENTOS_MODE)
    log.cprint(res)
    if "ADMINISTRATOR" in res:
        log.success("Pass! %s" % cmd)
    else:
        log.fail("Fail! %s" % cmd)
        raise testFailed("get_bmc_user_list")


def get_ip_address_from_ipmitool(device, eth_type='dedicated', ipv6=False):
    """
    Use IPMI command to get IP address
    :param device: product name
    :param eth_type: Network port type: dedicated, shared
    :param ipv6: Whether to get IPV6, if False, get IPV4
    :return: IP address
    """
    device_obj = Device.getDeviceObject(device)
    cmd1 = 'ipmitool lan print 1'
    cmd2 = 'ipmitool lan6 print 1'
    cmd3 = 'ipmitool lan print 8'
    cmd4 = 'ipmitool lan6 print 8'
    if ipv6:
        ip_re = r'IPv6 Dynamic Address 0.+\n.+\n.+Address:\s+(.+)/'
        cmd = cmd2 if eth_type == 'dedicated' else cmd4
    else:
        ip_re = r"IP Address\s+:\s+(\d+\..*\d+)"
        cmd = cmd1 if eth_type == 'dedicated' else cmd3
    output = openbmc_lib.execute(device_obj, cmd, mode=CENTOS_MODE)
    ip_res = re.findall(ip_re, output)
    if ip_res:
        ip = ip_res[0]
        if ip == "0.0.0.0":
            PRINTE("Fail! Got bmc ip:0.0.0.0")
        log.success('Pass! get ip address from ipmitool: %s' % ip)
        return ip
    else:
        log.fail('Fail! can not get ip address from ipmitool response:\n%s' % output)
        raise RuntimeError("Fail! get_ip_address_from_ipmitool")


def check_add_bmc_user(device, user_id, name, decide=True, len_8=False):
    """
    Add (modify) users in BMC and check whether the addition is successful
    :param device: product name
    :param user_id: the serial number of the new username
    :param name: username
    :param decide: whether the addition is expected to be successful
    :param len_8: password length
    """
    log.debug('Entering procedure verify_add_bmc_user with args : %s\n' % (str(locals())))
    device_obj = Device.getDeviceObject(device)
    flag = True
    cmd1 = 'ipmitool user set name %s %s' % (user_id, name)
    a = "testtest" if len_8 else "test"
    cmd2 = 'ipmitool user set password %s %s 20' % (user_id, a)
    cmd3 = 'ipmitool user enable %s' % user_id
    cmd4 = 'ipmitool raw 6 0x43 0x91 %s 4 0' % user_id
    output1 = openbmc_lib.execute(device_obj, cmd1, mode=CENTOS_MODE)
    time.sleep(3)
    output2 = openbmc_lib.execute(device_obj, cmd2, mode=CENTOS_MODE)
    openbmc_lib.execute(device_obj, cmd3, mode=CENTOS_MODE)
    openbmc_lib.execute(device_obj, cmd4, mode=CENTOS_MODE)
    log.cprint(output1)
    log.cprint(output2)
    p1 = r'(\ssuccessful\s)+\S(user+\s\d.*)\S'
    p2 = r'(user)+?[\s\w\S]+(\s\d?\d)'
    match = re.search(p1, output2)
    match_cmd = re.search(p2, cmd2)
    if match:
        bmc_user = match.group(2).strip()
        log.debug("bmc_user:%s" % bmc_user)
        cmd_user = (match_cmd.group(1).strip() + match_cmd.group(2)).strip()
        log.debug(" cmd_user:%s" % cmd_user)
        parse_out = match.group(1).strip()
        log.debug("parse_out:%s" % parse_out)
        if parse_out == 'successful':
            log.info("Successfully verify_add_bmc_user: %s" % bmc_user)
            bmc_ip = get_ip_address_from_ipmitool(device)
            device_pc = Device.getDeviceObject(device)
            cmd = "ipmitool -I lanplus -H %s -U %s -P %s mc info" % (bmc_ip, name, a)
            log.info(cmd)
            output = Device.execute_local_cmd(device_pc, cmd, timeout=10)
            if "Device ID" not in output:
                PRINTE("Fail! UserName: %s Not enabled" % name, decide=False)
                flag = False
        else:
            PRINTE("check_add_bmc_user: %s" % bmc_user, decide=False)
            flag = False
    else:
        if decide:
            PRINTE("check_add_bmc_user")
        else:
            flag = False
    if not flag:
        if decide:
            raise RuntimeError('check_add_bmc_user')


def del_user_info(device, user_id, decide=True):
    """
    Delete the account information of the corresponding serial number in the user list
    :param device: the name of the tested product
    :param user_id: delete the serial number of the account
    :param decide: whether the deletion is expected to be successful
    """
    cmd = "ipmitool raw 6 0x45 %s 0xff 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0" % str(user_id)
    device_obj = Device.getDeviceObject(device)
    res = openbmc_lib.execute(device_obj, cmd, mode=CENTOS_MODE)
    error_info = "Unable to send command: Invalid argument"
    log.info("response:\n%s" % res)
    if decide:
        if error_info in res:
            PRINTE("Fail! del_user_info fail")
    else:
        if error_info not in res:
            PRINTE("Fail! del_user_info fail")
    log.info("Pass! del_user_info")


def check_bmc_user_passwd(device, user_id, passwd, byte, decide=True):
    """
    Verify that the BMC user password (for testing convenience, the user name is consistent with the password)
    is the expected byte [16|20]
    :param device: product name
    :param user_id: username serial number
    :param passwd: username password
    :param byte:16/20
    :param decide: Is the expectation correct
    """
    byte = int(byte)
    device_obj = Device.getDeviceObject(device)
    if byte not in [16, 20]:
        PRINTE("Fail! password must be 16 or 20 byte")
    cmd = 'ipmitool user test %s %d %s' % (user_id, byte, passwd)
    res = openbmc_lib.execute(device_obj, cmd, mode=CENTOS_MODE)
    ans = re.findall(r"Success", res)
    if decide:
        if ans:
            log.info("Pass! check_bmc_user_passwd")
        else:
            PRINTE('Fail! cmd:%s, response:\n%s' % (cmd, res))
    else:
        if ans:
            PRINTE('Fail! cmd:%s, response:\n%s' % (cmd, res))
        else:
            log.info("Pass! check_bmc_user_passwd")


def set_bmc_passwd_byte(device, user_id, byte, len_8=False):
    """
    Set the password of a user to the expected number of bytes
    :param device: product under test
    :param user_id: the serial number of the user
    :param byte: 16/20
    :param len_8: password length
    """
    user_id = int(user_id)
    byte = int(byte)
    if byte not in [16, 20]:
        PRINTE("Fail! byte must be 16 or 20")
    device_obj = Device.getDeviceObject(device)
    a = "testtest" if len_8 else "test"
    cmd = "ipmitool user set password %d %s %d" % (user_id, a, byte)
    res = openbmc_lib.execute(device_obj, cmd, mode=CENTOS_MODE)
    if "successful" in res:
        log.info("Pass! %s" % res)
    else:
        PRINTE("Fail! response:\n%s" % res)


def set_reboot(device, timeout=600):
    """
    Set restart bmc
    :param device: product name
    :param timeout: restart waiting time
    """
    device_obj = Device.getDeviceObject(device)
    ip = get_ip_address_from_ipmitool(device)
    cmd = r"ipmitool -I lanplus -H %s -U admin -P admin raw 6 2" % ip
    Device.execute_local_cmd(device_obj, cmd, timeout=60)
    log.info("BMC will be reboot")
    connect(device, 50, timeout)


def check_psw_ascii(device, user_id, passwd, byte, decide=True, len_8=False):
    """
    Set the "test" account in a sequence number to 16/20 bytes and perform corresponding ascii code verification
    :param device: the name of the tested product
    :param user_id: the serial number of the test account
    :param passwd: user password
    :param byte: 16/20
    :param decide: True or False
    :param len_8: password length
    """
    byte = int(byte)
    if byte not in [16, 20]:
        PRINTE("Fail! byte must be 16 or 20")
    device_obj = Device.getDeviceObject(device)
    if byte == 20:
        # cmd = 'ipmitool raw 0x06 0x47 0x83 0x02 0x74 0x65 0x73 0x74 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00'
        cmd = "ipmitool raw 0x06 0x47 0x83 0x02 0x74 0x65 0x73 0x74 0x74 0x65 0x73 0x74 0x31 00 00 00 " \
              "00 00 00 00 00 00 00 00"
    else:
        # cmd = "ipmitool raw 0x06 0x47 0x03 0x02 0x74 0x65 0x73 0x74 00 00 00 00 00 00 00 00 00 00 00 00"
        cmd = "ipmitool raw 0x06 0x47 0x03 0x02 0x74 0x65 0x73 0x74 0x74 0x65 0x73 0x74 0x31 0x32 0x33 00 00 00 00 00"
    openbmc_lib.execute(device_obj, cmd, mode=CENTOS_MODE)
    set_bmc_passwd_byte(device, user_id, byte, len_8)
    check_bmc_user_passwd(device, user_id, passwd, byte, decide)


def check_bmc_reboot_user_list(device, reboot=False, decide=True, timeout=240):
    """
    Check whether the information obtained by the command 'ipmitool user list 1'
    before as same as  after the BMC restart
    :param device: the name of the tested product
    :param reboot: Whether to restart BMC
    :param decide: whether the expectations are the same
    :param timeout: restart timeout
    """
    cmd = 'ipmitool user list 1'
    res = get_bmc_user_list(device, cmd)
    if reboot:
        set_reboot(device, timeout)
    rep = get_bmc_user_list(device, cmd)
    if decide:
        if res == rep:
            log.info("Pass!  user information is not changed after BMC reset")
        else:
            PRINTE("Fail!  user information has changed after BMC reset")
    else:
        if res == rep:
            PRINTE("Fail!  user information is not changed after BMC reset")
        else:
            log.info("Pass!  user information is not changed after BMC reset")


def set_sel_clear(device, ip=None, wait=5):
    """
    Use 'ipmitool sel clear' to clear the boot status log and check that the sensor status is 0x0480
    :param device: product under test
    :param ip: Use direct control when it is None. Use remote control when it is not None
    :param wait: wait time
    """
    # Sensor status check, it must be 0x0480 after sending the clear command
    error_flag = False
    device_obj = Device.getDeviceObject(device)
    if ip:
        cmd_1 = 'ipmitool -I lanplus -H %s -U admin -P admin sel clear' % ip
        cmd_2 = "ipmitool -I lanplus -H %s -U admin -P admin sensor list | grep -i sel" % ip
    else:
        cmd_1 = 'ipmitool sel clear'
        cmd_2 = "ipmitool sensor list | grep -i sel"
    for i in range(3):
        try:
            if ip:
                res_1 = Device.execute_local_cmd(device_obj, cmd_1, timeout=60)
            else:
                res_1 = openbmc_lib.execute(device_obj, cmd_1, mode=CENTOS_MODE)
        except Exception:
            set_wait(30)
            continue
        if 'Clearing SEL' not in res_1:
            PRINTE("Fail! 'Clearing SEL' not in response.response:\n%s" % res_1)
        break
    set_wait(30)
    check_sel_info_only_clear(device, True, ip)
    for i in range(3):
        if ip:
            res_3 = Device.execute_local_cmd(device_obj, cmd_2, timeout=30)
        else:
            res_3 = openbmc_lib.execute(device_obj, cmd_2, mode=CENTOS_MODE)
        if '0x0480' not in res_3:
            error_flag = True
            PRINTE("Fail! Couldn't get the sensor status[0x0480], response:\n%s" % res_3, decide=False)
        else:
            error_flag = False
            break
        set_wait(30)
    if error_flag:
        PRINTE("Fail! '0x0480' not in response")


def check_sel_event_data(device, record_id, exp_num, decide=True, ip=None):
    """
    Use 'ipmitool sel get record id' to check that the first byte of sel event 1 event data (Event Data (RAW)) is
    the expected value
    :param device: product name
    :param record_id: Record_ID
    :param exp_num: expected value
    :param decide: whether the expectations are the same
    :param ip: bmc ip
    """
    device_obj = Device.getDeviceObject(device)
    if ip:
        cmd = "ipmitool -I lanplus -H %s -U admin -P admin sel get %s" % (ip, record_id)
        res = Device.execute_local_cmd(device_obj, cmd)
    else:
        cmd = 'ipmitool sel get %s' % record_id
        res = openbmc_lib.execute(device_obj, cmd, mode=CENTOS_MODE)
    event_data = re.findall(r"Event Data .*: (\w{6})", res)
    if event_data:
        event_data = event_data[0][:2]
    else:
        PRINTE("Fail! 'ipmitool sel get %s' couldn't get the keyword [Event Data]" % record_id)
    if decide:
        if str(exp_num) == event_data:
            log.info("Pass! check_sel_event_data")
        else:
            PRINTE('Fail! Event Data:%s, response:\n%s' % (event_data, res))
    else:
        if str(exp_num) == event_data:
            PRINTE('Fail! Event Data:%s, response:\n%s' % (event_data, res))
        else:
            log.info("Pass! check_sel_event_data")


def set_watchdog_timer(device, use, actions, timeout="1"):
    """
    Set watchdog timer: "timer use", "and timer action", "countdown value".
    :param device: the name of the tested product
    :param use:
             0:reserved reserved bit, useless
             1:BIOS FRB2
             2: BIOS/POST power-on self-test
             3: OS Land system loading
             4: SMS/OS
             5: Customized functions generated by OEM
    :param actions:
             0: do nothing
             1: BMC restart
             2: Power off the system (remember to power it back on at the end)
             3: system restart
    :param timeout: After the watchdog is set, the trigger time countdown, in seconds
    """
    device_obj = Device.getDeviceObject(device)
    cmd = r"ipmitool raw 0x06 0x24 0x%s 0x%s 0x%s 0x00 0x1f 0x00" % (use.zfill(2), actions.zfill(2), timeout.zfill(2))
    res = openbmc_lib.execute(device_obj, cmd, mode=CENTOS_MODE)
    if "Unable to send RAW command" in res:
        PRINTE("Fail! send cmd: %s \t response:\n%s" % (cmd, res))


def set_watchdog_start(device):
    """
    Send 'ipmitool raw 0x06 0x22' to start watchdog
    """
    cmd = "ipmitool raw 0x06 0x22"
    device_obj = Device.getDeviceObject(device)
    openbmc_lib.execute(device_obj, cmd, mode=CENTOS_MODE)


def check_watchdog_update(device, use, actions, timeout=1, decide=True):
    """
    Check whether the watchdog has been set successfully (check only the first three bytes returned by the command)
    :param device: the name of the tested product
    :param use: expected use, parameter range view set_watchdog_timer
    :param actions: expected actions, parameter range view set_watchdog_timer
    :param timeout: expected timeout, parameter range see set_watchdog_timer
    :param decide: whether it meets expectations
    """
    cmd = "ipmitool raw 0x06 0x25"
    device_obj = Device.getDeviceObject(device)
    res = openbmc_lib.execute(device_obj, cmd, mode=CENTOS_MODE)
    res_info = re.findall(r"\w+ \w+ \w+ \w+ \w+ \w+ \w+ \w+", res)
    if not res_info:
        PRINTE("Fail! can not get watchdog info. response:\n%s" % res)
    exp_set = "%s %s %s" % (use.zfill(2), actions.zfill(2), str(timeout).zfill(2))
    if exp_set == res_info[0][:8]:
        if decide:
            log.info("Pass!")
            return True
        else:
            PRINTE("Fail! response:\n%s,exp_set=%s" % (res_info, exp_set))
    else:
        if decide:
            PRINTE("Fail! response:\n%s,exp_set=%s" % (res_info, exp_set))
        else:
            log.info("Pass!")
            return True


def check_watchdog_counting_down(device, step=1, timeout=20, continue_wait=0, ip=None):
    """
    Check if the watchdog is counting down
    :param device: product under test
    :param step: wait time after each check
    :param timeout: check timeout
    :param continue_wait: Continue to wait after the timeout period. Generally used when the product is in the restart
                          waiting time after the watchdog expires
    :param ip: When there is no IP, telnet is the tested product, otherwise, enter BMC through IP to obtain information
    """
    device_obj = Device.getDeviceObject(device)
    if ip:
        cmd = "ipmitool -I lanplus -H %s -U admin -P admin  raw 0x06 0x25" % ip
    else:
        cmd = "ipmitool raw 0x06 0x25"
    count_list = list()
    start = time.time()
    while time.time() - start <= int(timeout):
        res = Device.execute_local_cmd(device_obj, cmd) if ip else openbmc_lib.execute(device_obj, cmd,
                                                                                       mode=CENTOS_MODE)
        res_info = re.findall(r"\w+ \w+ \w+ \w+ \w+ \w+ (\w+) \w+", res)
        if not res_info:
            PRINTE("Fail! can not get watchdog info. response:\n%s" % res)
        count_num = int(res_info[0], 16)
        if count_num != 0:
            count_list.append(count_num)
        else:
            break
        time.sleep(step)
    if len(list(set(count_list))) == 1:
        PRINTE("Fail! watchdog isn't counting down, got counting down info:%s" % str(count_list))
    count_list_old = count_list.copy()
    count_list.sort(reverse=True)
    if count_list != count_list_old:
        PRINTE("Fail! counting down list:%s, expected list:%s" % (str(count_list_old), str(count_list)))
    set_wait(continue_wait)


def check_bmc_sel_list_keyword(device, keyword, decide=True, ip=None):
    """
    Check whether there are expected keywords in the log records of ipmitool sel list in BMC.
    Please clear sel information before calling
    Avoid false detections
    :param device: the name of the tested product
    :param keyword: Incoming string, when multiple expected characters need to be checked, write them as the same string
                    separated by','
    :param decide: whether the expectation exists
    :param ip: When ip is None, use direct access to obtain information, otherwise use remote access to obtain information
    """
    res = get_sel_list(device, ip=ip, return_info=True)
    flag = True
    if "," in keyword:
        keyword_list = keyword.split(",")
        for word in keyword_list:
            res_re = re.findall(r"%s" % word, res)
            if len(res_re) > 1:
                PRINTE("Fail! Keyword:%s Frequency of occurrence is greater than 1" % word)
            if decide:
                if not res_re:
                    PRINTE("Fail! couldn't find the keyword:[%s].response:\n%s" % (word, res), decide=False)
                    flag = False
            else:
                if res_re:
                    PRINTE("Fail! find the keyword:[%s].response:\n%s" % (word, res), decide=False)
                    flag = False
    else:
        res_re = re.findall(r"%s" % keyword, res)
        if len(res_re) > 1:
            PRINTE("Fail! Keyword:%s Frequency of occurrence is greater than 1" % keyword)
        if decide:
            if not res_re:
                PRINTE("Fail! couldn't find the keyword:[%s].response:\n%s" % (keyword, res), decide=False)
                flag = False
        else:
            if res_re:
                PRINTE("Fail! find the keyword:[%s].response:\n%s" % (keyword, res), decide=False)
                flag = False
    if not flag:
        raise RuntimeError("Fail! check_bmc_sel_list_keyword")


def set_bmc_ip_status(device, ip_status):
    """
    Set BMC IP as static or dynamic
    :param device: the name of the tested product
    :param ip_status: dhcp(dynamic)/static(static)
    """
    ip_status = ip_status.lower()
    if ip_status not in ["dhcp", "static"]:
        PRINTE("Fail! set_bmc_ip_status parameter must be 'dhcp' or 'static'")
    ip_status = "static" if ip_status.lower() == "static" else "dhcp"
    cmd = "ipmitool lan set 1 ipsrc %s" % ip_status
    device_obj = Device.getDeviceObject(device)
    try:
        openbmc_lib.execute(device_obj, cmd, mode=CENTOS_MODE)
    except Exception as E:
        raise RuntimeError("Fail! set_bmv_dhcp. Error:%s" % E)


def check_info_equal(info_1, info_2, decide=True):
    """
    Check whether the two messages (both will be converted to strings) are equal
    """
    info_1 = str(info_1).strip()
    info_2 = str(info_2).strip()
    if decide:
        if info_1 != info_2:
            PRINTE("Fail!\ninfo_1: %s\ninfo_2: %s" % (info_1, info_2))
    else:
        if info_1 == info_2:
            PRINTE("Fail!\ninfo_1: %s\ninfo_2: %s" % (info_1, info_2))


def check_communication_lan_pc(device, ip=None):
    """
    Check if you can get the mc info information correctly
    :param device: product under test
    :param ip: Direct connection when it is None, otherwise remote command
    """
    device_obj = Device.getDeviceObject(device)
    try:
        for i in range(3):
            if ip:
                cmd = "ipmitool -I lanplus -H %s -U admin -P admin mc info" % ip
                res_1, res_2 = Device.execute_local_cmd(device_obj, cmd, timeout=30, return_errs=True)
                output = res_1 + res_2
            else:
                cmd = "ipmitool mc info"
                output = openbmc_lib.execute(device_obj, cmd)
            if "Device ID" in output:
                break
            else:
                time.sleep(10)
        else:
            PRINTE("Fail! Try three times, but couldn't get mc info")
    except Exception as E:
        log.error(str(E))


def set_bmc_ip(device, lan="1", ipaddr=None, netmask=None):
    """
    Set BMC IP information
    :param device: the name of the tested product
    :param lan: network channel 1-8
    :param ipaddr: IP address
    :param netmask: subnet mask
    """
    device_obj = Device.getDeviceObject(device)
    if ipaddr:
        cmd = r"ipmitool lan set %s ipaddr %s" % (lan, ipaddr)
        openbmc_lib.execute(device_obj, cmd, mode=CENTOS_MODE)
    if netmask:
        cmd = r" ipmitool lan set %s netmask %s" % (lan, netmask)
        openbmc_lib.execute(device_obj, cmd, mode=CENTOS_MODE)


def check_bmc_ip_info(device, ipaddr=None, netmask=None, decide=True):
    """
    Check whether the ip information obtained by ipmitool lan print 1 meets expectations
    :param device: product name
    :param ipaddr: expected ip address
    :param netmask: expected subnet mask
    :param decide: whether the expectation is correct
    """
    cmd = "ipmitool lan print 1"
    device_obj = Device.getDeviceObject(device)
    res = openbmc_lib.execute(device_obj, cmd, mode=CENTOS_MODE)
    if ipaddr:
        ip = re.findall(r"IP Address\s+:\s+(\d+\..*\d+)", res)
        if ip:
            ip = ip[0].strip()
            if decide:
                if ipaddr != ip:
                    PRINTE("Fail! get ip:%s, exp ip is:%s" % (ip, ipaddr))
            else:
                if ipaddr == ip:
                    PRINTE("Fail! get ip:%s, exp ip is:%s" % (ip, ipaddr))
        else:
            PRINTE("Fail! couldn't get ip info.response:\n" % res)
    if netmask:
        mask = re.findall(r"Subnet Mask\s+:\s+(\d+\..*\d+)", res)
        if mask:
            mask = mask[0].strip()
            if decide:
                if netmask != mask:
                    PRINTE("Fail! get Subnet Mask:%s, exp Subnet Mask is:%s" % (mask, netmask))
            else:
                if netmask == mask:
                    PRINTE("Fail! get Subnet Mask:%s, exp Subnet Mask is:%s" % (mask, netmask))
        else:
            PRINTE("Fail! couldn't get Subnet Mask info.response:\n" % res)


def set_sol_config_by_ip(device, enable="ture", non_volatile="115.2", volatile_bit="115.2"):
    """
    Set sol related information through BMC ip
    :param device: product name
    :param enable: ture-enable, false-disable
    :param non_volatile: non-volatile-bit-rate Value
    :param volatile_bit: volatile-bit-rate Value
    """
    ip = get_ip_address_from_ipmitool(device)
    device_obj = Device.getDeviceObject(device)
    log_out = WhiteboxLibAdapter.OSDisconnect()
    if log_out is not None:
        PRINTE("Fail! WhiteboxLibAdapter.OSDisconnect")
    flag = "1" if enable == "true" else "0"
    cmd_1 = r"ipmitool –I lanplus –H %s –U admin –P admin sol set enabled %s %s" % (ip, enable, flag)
    cmd_2 = r"ipmitool –I lanplus –H %s –U admin –P admin sol set non-volatile-bit-rate %s %s" % (ip, non_volatile,
                                                                                                  flag)
    cmd_3 = r"ipmitool –I lanplus –H %s –U admin –P admin sol set volatile-bit-rate %s %s" % (ip, volatile_bit, flag)
    Device.execute_local_cmd(device_obj, cmd_1, timeout=60)
    Device.execute_local_cmd(device_obj, cmd_2, timeout=60)
    Device.execute_local_cmd(device_obj, cmd_3, timeout=60)
    WhiteboxLibAdapter.OSConnect()


def get_sol_config(device, exp_key, ip=None):
    """
    Get the value of the corresponding key in the ipmitool sol info 1 information
    :param device: product under test
    :param exp_key: the key of the expected item
    :param ip: use remote command if ip is passed in, otherwise connect directly
    :return: the value of the key of the expected item
    """
    device_obj = Device.getDeviceObject(device)
    if ip:
        cmd = "ipmitool -I lanplus -H %s -U admin -P admin sol info 1" % ip
        res = Device.execute_local_cmd(device_obj, cmd)
    else:
        cmd = r"ipmitool sol info 1"
        res = openbmc_lib.execute(device_obj, cmd, mode=CENTOS_MODE)
    info_list = common_parsing(res)
    for i in info_list:
        if exp_key in i.keys():
            return i[exp_key]
    else:
        PRINTE("Fail! couldn't find the key[%s]" % str(exp_key))


def set_user_privilege(device, user_id, priv):
    """
    Modify account permissions to Callback, User, Operator, Administrator, OEM Proprietary, No Access
    :param device: the name of the tested product
    :param user_id: the serial number of the user account
    :param priv: Privilege level [Callback,User,Operator,Administrator,OEM Proprietary,No Access]
    """
    priv_dict = {"Callback": "0x1",
                 "User": "0x2",
                 "Operator": "0x3",
                 "Administrator": "0x4",
                 "OEM Proprietary": "0x5",
                 "No Access": "0xF"}
    if priv not in priv_dict.keys():
        PRINTE("Fail! parameter error!")
    cmd = "ipmitool raw 6 0x43 0x91 %s %s 0" % (user_id, priv_dict[priv])
    device_obj = Device.getDeviceObject(device)
    openbmc_lib.execute(device_obj, cmd, mode=CENTOS_MODE)
    cmd_1 = "ipmitool user list 1"
    res_1 = openbmc_lib.execute(device_obj, cmd_1, mode=CENTOS_MODE)
    if priv.upper() not in res_1:
        PRINTE("Fail! can't got the keyword:[%s],response:\n%s" % (priv, res_1))


def get_sel_list(device, ip=None, return_info=False):
    """
    get sel info
    :param device: the name of the tested product
    :param ip: BMC ip
    :param return_info: return info or not
    """
    device_obj = Device.getDeviceObject(device)
    if ip:
        cmd = "ipmitool -I lanplus -H %s -U admin -P admin sel list" % ip
        res = Device.execute_local_cmd(device_obj, cmd, 120)
    else:
        cmd = r"ipmitool sel list"
        res = openbmc_lib.execute(device_obj, cmd, timeout=120, mode=CENTOS_MODE)
    if return_info:
        return res


def set_channel_access(device):
    """
    Set the maximum privilege level that the channel can accept
    """
    cmd = r"ipmitool raw 0x06 0x41 0x01 0x40"
    device_obj = Device.getDeviceObject(device)
    res = openbmc_lib.execute(device_obj, cmd, mode=CENTOS_MODE)
    if "12 04" not in res:
        PRINTE("Fail! set_channel_access,response:\n%s" % res)


def check_session_status(device, lv, user_name, password, ip=None, decide=True):
    """
    Activate IPMI messaging sessions with different privilege levels through the user account, and check whether
    the session can be successfully established.
    AMININISTRATOR
    :param device: the name of the tested product
    :param lv:ADMINISTRATOR, OPERATOR, USER
    :param user_name: username
    :param password: user password
    :param ip:BMC IP
    :param decide: whether it is expected to establish a session
    """
    if not ip:
        ip = get_ip_address_from_ipmitool(device)
    cmd = "ipmitool -I lanplus -L %s -H %s -U %s -P %s mc info" % (lv, ip, user_name, password)
    device_obj = Device.getDeviceObject(device)
    res = Device.execute_local_cmd(device_obj, cmd, timeout=60)
    if decide:
        if "Device ID" not in res:
            PRINTE("Fail! send cmd:%s,response:\n%s" % (cmd, res))
    else:
        if "Device ID" in res:
            PRINTE("Fail! send cmd:%s,response:\n%s" % (cmd, res))


def get_chassis_power_status(device, ip=None):
    """
    Get the chassis power status through ipmitool chassis power status when no IP is passed in. Otherwise, obtain the
    chassis power status through the BMC IP
    :param device: product under test
    :param ip: BMC IP can not be passed in
    :return: chassis power status
    """
    device_obj = Device.getDeviceObject(device)
    if ip:
        cmd = "ipmitool -I lanplus -H %s -U admin -P admin chassis power status" % ip
        res = Device.execute_local_cmd(device_obj, cmd, timeout=60)
    else:
        cmd = "ipmitool chassis power status"
        res = openbmc_lib.execute(device_obj, cmd, mode=CENTOS_MODE)
    if res:
        power_status = re.findall(r"Chassis Power is (on|off)", res)[0]
        log.info("Pass! get chassis power status:%s" % power_status)
        return power_status
    else:
        PRINTE("Fail! couldn't get chassis power status.response:\n%s" % res)


def check_chassis_power_status(device, ip, exp_status):
    """
    Check whether the current chassis power state meets expectations
    :param device: product under test
    :param ip: BMC IP can not be passed in
    :param exp_status: Expected chassis power status
    """
    exp_status = exp_status.lower()
    power_status = get_chassis_power_status(device=device, ip=ip)
    if power_status != exp_status:
        PRINTE("Fail! exp_status:%s, chassis power status:%s" % (exp_status, power_status))


def check_power_status_cycle(device, timeout=30):
    """
    After sending ipmitool chassis power cycle
    Check that when the power is cycled, the power status can be obtained from the BMC in real time,
    and its status includes on and off (remote inspection on the PC side)
    :param device: product under test
    :param timeout: The timeout period for obtaining the power status
    """
    ip = get_ip_address_from_ipmitool(device)
    cmd = "ipmitool chassis power cycle"
    device_obj = Device.getDeviceObject(device)
    openbmc_lib.execute(device_obj, cmd, mode=CENTOS_MODE)
    start_time = time.time()
    status_list = list()
    while time.time() - start_time < int(timeout):
        power_status = get_chassis_power_status(device, ip)
        status_list.append(power_status)
        time.sleep(1.5)
    if "off" in status_list and "on" in status_list:
        log.info("Pass! get the power status include [on,off]")

    else:
        PRINTE("Fail! couldn't get all the power status")

    s_time = time.time()
    while time.time() - s_time <= 240:
        try:
            device_obj.tryLogin()
            set_root_hostname(device)
            break
        except Exception:
            time.sleep(10)


def check_power_status_bmc(device, ip, timeout=30):
    """
    Obtain the power status from BMC in real time, including on and off status (check directly on the BMC side),
    and check whether the lan bmc is normal after timeout
    :param device: product under test
    :param timeout: The timeout period for obtaining the power status
    :param ip: Confirm whether the BMC network is normal in some stages of BMC controlling power. BMC IP
    """
    start_time = time.time()
    status_list = list()
    while time.time() - start_time < int(timeout):
        power_status = get_chassis_power_status(device, ip)
        if power_status:
            status_list.append(power_status)
            time.sleep(1.5)
    if "off" in status_list and "on" in status_list:
        log.info("Pass! get the power status include on,off")
    else:
        PRINTE("Fail! couldn't get all the power status")


def set_sel_disabled(device, ip=None):
    """
    Set disable sel retainer configuration
    """
    device_obj = Device.getDeviceObject(device)
    if ip:
        cmd = "ipmitool -I lanplus -H %s -U admin -P admin raw 0x32 0x84 0x02" % ip
        res = Device.execute_local_cmd(device_obj, cmd)
    else:
        cmd = r"ipmitool raw 0x32 0x84 0x02"
        res = openbmc_lib.execute(device_obj, cmd, mode=CENTOS_MODE)
    if "00" not in res:
        PRINTE("Fail! response:\n%s" % res)


def get_bmc_version(device, primary=True, return_hex=False, ip=None, mc_info=False):
    """
    Obtain the version information of the active/standby BMC
    :param device: the name of the tested product
    :param primary: True: primary version, False: alternate version
    :param return_hex: whether to return hexadecimal
    :param ip: when it is None, it will connect directly, otherwise remote command
    :param mc_info: False-use ipmitool。True-mc info
    :return: return version information
    """
    device_obj = Device.getDeviceObject(device)
    if mc_info:
        res = get_mc_info(device, ip)
        re_version = re.findall(r'Firmware Revision\s+:\s+(\S+)', res)[0]
        return re_version
    else:
        machine = "1" if primary else "2"
        if ip:
            cmd = "ipmitool -I lanplus -H %s -U admin -P admin raw 0x32 0x8f 0x08 0x0%s" % (ip, machine)
            res = Device.execute_local_cmd(device_obj, cmd)
        else:
            cmd = r"ipmitool raw 0x32 0x8f 0x08 0x0%s" % machine
            res = openbmc_lib.execute(device_obj, cmd, mode=CENTOS_MODE)
        if return_hex:
            return res
        else:
            a = res.split(" ")
            if a:
                for i in a:
                    if i == "":
                        a.remove(i)
                    if "\n" in i:
                        a.remove(i)
                        i = i.replace("\n", "")
                        a.append(i)
                version = "%d.%d" % (int(a[0], 16), int(a[1], 16))
                return version
            else:
                PRINTE("Fail! couldn't get bmc version info")


def set_update_bmc_primary_backup(device, primary=True, decide=True, ip=None):
    """
    Set and update the main/standby bmc, and check whether the setting is successful
    :param device: the name of the tested product
    :param primary: True-primary bmc False-backup bmc
    :param decide: whether the expected setting is successful
    :param ip: when it is None, it will connect directly, otherwise remote command
    """
    device_obj = Device.getDeviceObject(device)
    machine = "01" if primary else "02"
    if ip:
        cmd = "ipmitool -I lanplus -H %s -U admin -P admin raw 0x32 0x8f 0x03 0x%s" % (ip, machine)
        Device.execute_local_cmd(device_obj, cmd)
        cmd_check = r"ipmitool -I lanplus -H %s -U admin -P admin raw 0x32 0x8f 0x04" % ip
        res = Device.execute_local_cmd(device_obj, cmd_check)
    else:
        cmd = r"ipmitool raw 0x32 0x8f 0x03 0x%s" % machine
        openbmc_lib.execute(device_obj, cmd, mode=CENTOS_MODE)
        cmd_check = r"ipmitool raw 0x32 0x8f 0x04"
        res = openbmc_lib.execute(device_obj, cmd_check, mode=CENTOS_MODE)
    if decide:
        if machine not in res:
            PRINTE("Fail! couldn't get the [%s],response:\n%s" % (machine, res))
    else:
        if machine in res:
            PRINTE("Fail! get the [%s],response:\n%s" % (machine, res))


def update_bmc_by_hpm(device, hpm="old", ip=None):
    """
    Upgrade the bmc through the hpm file. When the IP is not None, the hpm file needs to be placed in the
    computer that sends the remote command. Otherwise, put it in the upgraded computer
    :param device: the name of the tested product
    :param hpm: The absolute path of the hpm file.
                old-use the files in the old folder of the python server,
                now-use the files in the now folder of the python server.
                Otherwise use the absolute path passed in
    :param ip: when it is None, it will connect directly, otherwise remote command
    """
    tool_path = get_tool_path()
    hpm = hpm.lower()
    device_obj = Device.getDeviceObject(device)
    shell_path = "%s/hpm/BMC_update.sh" % tool_path
    if hpm in ["old", "now"]:
        cmd = "ls %s/hpm/bmc/%s" % (tool_path, hpm)
        file_name = Device.execute_local_cmd(device_obj, cmd, timeout=60).strip()
        hpm = "%s/hpm/bmc/%s/%s" % (tool_path, hpm, file_name)
    if ip:
        cmd = "%s %s %s" % (shell_path, ip, hpm)
        res = Device.execute_local_cmd(device_obj, cmd, timeout=240)
        if "Firmware upgrade procedure successful" in res:
            log.info("Pass! update_bmc_by_hpm")
        else:
            PRINTE("Fail! BMC FW upgrade fail. response:\n%s" % res)
    else:
        PRINTE("Please enter bmc ip")


def get_mc_info(device, ip=None):
    """
    Send ‘mc info’ to get information
    :param device: product under test
    :param ip: when it is None, it will connect directly, otherwise remote command
    :return: related return
    """
    device_obj = Device.getDeviceObject(device)
    if ip:
        cmd = "ipmitool -I lanplus -H %s -U admin -P admin mc info" % ip
        res = Device.execute_local_cmd(device_obj, cmd)
    else:
        cmd = r"ipmitool mc info"
        res = openbmc_lib.execute(device_obj, cmd, mode=CENTOS_MODE)
    return res


def check_bmc_channel_medium_type(device, channel, medium=None, protocol=None, ip=None):
    """
    channel info check whether the Channel Medium Type of a channel meets expectations
    :param device: product under test
    :param channel: the channel to be checked, c is passed in decimal(it will be automatically converted to hexadecimal)
    :param medium: Channel Medium Type expected situation
    :param protocol: Channel Protocol Type expected situation
    :param ip: when it is None, it will connect directly, otherwise remote command
    """
    channel = hex(int(channel))
    device_obj = Device.getDeviceObject(device)
    if ip:
        cmd = "ipmitool -I lanplus -H %s -U admin -P admin channel info %s" % (ip, channel)
        res = Device.execute_local_cmd(device_obj, cmd)
    else:
        cmd = r"ipmitool channel info %s" % channel
        res = openbmc_lib.execute(device_obj, cmd, mode=CENTOS_MODE)
    if medium:
        if "Channel Medium Type" in res:
            a = re.findall(r"Channel Medium Type\s+:\s+(.*)", res)
            if medium != a[0].strip():
                PRINTE("Fail! expect Channel Medium Type:[%s], response Channel Medium Type:[%s]" % (medium, a[0]))
        else:
            PRINTE("Fail! couldn't get keyword [Channel Medium Type],response:\n%s" % res)
    if protocol:
        if "Channel Medium Type" in res:
            a = re.findall(r"Channel Protocol Type\s+:\s+(.*)", res)
            if protocol != a[0].strip():
                PRINTE("Fail! expect Channel Protocol Type:[%s], response Channel Protocol Type:[%s]" % (medium, a[0]))
        else:
            PRINTE("Fail! couldn't get keyword [Channel Protocol Type],response:\n%s" % res)


def check_ipmb_device(device, ip=None):
    """
    Check that the device id of the product can be successfully obtained
    :param device: product under test
    :param ip: when it is None, it will connect directly, otherwise remote command
    """
    device_obj = Device.getDeviceObject(device)
    if ip:
        cmd = "ipmitool -I lanplus -H %s -U admin -P admin -b 6 -t 0x2c raw 6 1" % ip
        Device.execute_local_cmd(device_obj, cmd)
    else:
        cmd = r"ipmitool -b 6 -t 0x2c raw 6 1"
        openbmc_lib.execute(device_obj, cmd, mode=CENTOS_MODE)


def check_fw_boot_selector(device, exp_fw, ip=None):
    """
    Check next FW boot selector
    :param device: product under test
    :param exp_fw: Expected firmware
    :param ip:bmc ip
    """
    device_obj = Device.getDeviceObject(device)
    if ip:
        cmd = "ipmitool -I lanplus -H %s -U admin -P admin raw 0x32 0x8f 0x02" % ip
        res = Device.execute_local_cmd(device_obj, cmd)
    else:
        cmd = r"ipmitool raw 0x32 0x8f 0x02"
        res = openbmc_lib.execute(device_obj, cmd, mode=CENTOS_MODE)
    if exp_fw not in res:
        PRINTE("Fail! firmware:%s,exp_fw:%s" % (res, exp_fw))


def check_current_active_image(device, exp_fw, ip=None):
    """
    Check current active image
    :param device: product under test
    :param exp_fw: Expected firmware
    :param ip:bmc ip
    """
    device_obj = Device.getDeviceObject(device)
    if ip:
        cmd = "ipmitool -I lanplus -H %s -U admin -P admin raw 0x32 0x8f 0x07" % ip
        res = Device.execute_local_cmd(device_obj, cmd)
    else:
        cmd = r"ipmitool raw 0x32 0x8f 0x07"
        res = openbmc_lib.execute(device_obj, cmd, mode=CENTOS_MODE)
    if exp_fw not in res:
        PRINTE("Fail! firmware:%s,exp_fw:%s" % (res, exp_fw))


def set_fw_boot_selector(device, exp_fw, ip=None):
    """
    set next FW boot selector,and Check it
    :param device: product under test
    :param exp_fw: Expected firmware[1,2]
    :param ip:bmc ip
    """
    device_obj = Device.getDeviceObject(device)
    if ip:
        cmd = "ipmitool -I lanplus -H %s -U admin -P admin raw 0x32 0x8f 0x01 0x0%s" % (ip, exp_fw)
        Device.execute_local_cmd(device_obj, cmd)
    else:
        cmd = r"ipmitool raw 0x32 0x8f 0x01 0x0%s" % exp_fw
        openbmc_lib.execute(device_obj, cmd, mode=CENTOS_MODE)
    check_fw_boot_selector(device, exp_fw, ip=None)


def send_cmd(device, cmd, ip=None, return_res=False):
    device_obj = Device.getDeviceObject(device)
    if ip:
        if "ipmitool " in cmd:
            cmd = cmd.replace("ipmitool ", "")
        cmd = "ipmitool -I lanplus -H %s -U admin -P admin %s" % (ip, cmd)
        res = Device.execute_local_cmd(device_obj, cmd)
    else:
        res = openbmc_lib.execute(device_obj, cmd, mode=CENTOS_MODE)
    if return_res:
        return res


def check_cmd_response(device, cmd, re_exp, decide=True, ip=None, re_S=False):
    """
    send cmd and check the return if re_exp in it.
    :param device: product under test
    :param cmd: send cmd
    :param re_exp: Expected return value, supports regular expressions
    :param decide: Does the expectation exist？
    :param ip:bmc ip
    :param re_S:re.S
    """
    device_obj = Device.getDeviceObject(device)
    if ip:
        if "ipmitool " in cmd:
            cmd = cmd.replace("ipmitool ", "")
        cmd = r"ipmitool -I lanplus -H %s -U admin -P admin %s" % (ip, cmd)
        res, errs = Device.execute_local_cmd(device_obj, cmd, return_errs=True)
        res = res + errs
        rec = re.findall("%s" % re_exp, res)
        if re_S:
            rec = re.findall("%s" % re_exp, res, re.S)
        if rec:
            if not decide:
                PRINTE("expected [%s] does not exist, but it actually exists：\n[%s]" % (re_exp, res))
        else:
            if decide:
                PRINTE("expected [%s] exist, but it does not actually exist. response:\n%s" % (re_exp, res))
    else:
        res = openbmc_lib.execute(device_obj, cmd, mode=CENTOS_MODE)
        if "ipmitool" in cmd:
            b = re.findall(".*ipmitool(.*)real.*", res, re.S)
        else:
            b = re.findall("time %s[\r|\n]*(.*)real.*" % cmd, res, re.S)
        a = b[0].split("\n")
        a.remove(a[0])
        res_c = ""
        for i in a:
            res_c += i + "\n"
        rec = re.findall(r"%s" % re_exp, res_c)
        if re_S:
            rec = re.findall(r"%s" % re_exp, res_c, re.S)
        if rec:
            if not decide:
                PRINTE("expected [%s] does not exist, but it actually exists[%s]" % (re_exp, res))
        else:
            if decide:
                PRINTE("expected [%s] exist, but it does not actually exist. response:\n%s" % (re_exp, res))


def set_get_gpio(device, num_list=change_gpio_num_list):
    """
    For midstone100x test case:9.13.4 Set/Get GPIO
    :param device:
    :param num: the number that you want to modify
    """
    device_obj = Device.getDeviceObject(device)
    direction_flag = True
    direction_input_list = list()
    direction_output_list = list()
    direction_list = list()
    data_low_list_init = list()
    data_high_list_init = list()
    data_low_list = list()
    data_high_list = list()
    data_list = list()
    for i in num_list:
        cmd_1 = "ipmitool raw 0x3a 0x24 0x01 %s" % i
        res_1 = openbmc_lib.execute(device_obj, cmd_1, mode=CENTOS_MODE)
        if " 00" in res_1:
            direction_input_list.append(i)
        elif " 01" in res_1:
            direction_output_list.append(i)
        else:
            PRINTE("Fail! Direction get response isn't [00,01]. it's[%s]" % res_1)
        cmd_2 = "ipmitool raw 0x3a 0x24 0x02 %s" % i
        res_2 = openbmc_lib.execute(device_obj, cmd_2, mode=CENTOS_MODE)
        if " 00" in res_2:
            data_low_list_init.append(i)
        elif " 01" in res_2:
            data_high_list_init.append(i)
        else:
            PRINTE("Fail! Data get response isn't [00,01]. it's[%s]" % res_2)
    if direction_input_list:
        log.info("[%s]: Direction initial attributes Input %s" % (datetime.now(), direction_input_list))
        direction_list.append(direction_input_list)
    if direction_output_list:
        log.info("[%s]: Direction initial attributes Output %s" % (datetime.now(), direction_output_list))
        direction_list.append(direction_output_list)
    if data_low_list_init:
        log.info("[%s]: Data initial attributes Low %s" % (datetime.now(), data_low_list_init))
    if data_high_list_init:
        log.info("[%s]: Data initial attributes High %s" % (datetime.now(), data_high_list_init))
    for _ in direction_list:  # direction transform
        initial = "input" if direction_list.index(_) == 0 else "output"
        set_num = "4" if direction_list.index(_) == 0 else "3"
        response = " 01" if direction_list.index(_) == 0 else " 00"  # response for direction input
        for j in _:  # set input to output:00->01, output to input:01->00
            cmd = "ipmitool raw 0x3a 0x24 0x0%s %s" % (set_num, j)
            openbmc_lib.execute(device_obj, cmd, mode=CENTOS_MODE)
        for k in _:  # Check if the set is successful
            cmd = "ipmitool raw 0x3a 0x24 0x01 %s" % k
            res = openbmc_lib.execute(device_obj, cmd, mode=CENTOS_MODE)
            if response not in res:
                PRINTE("Fail! [%s] Initial attributes: [%s].But the setting fails. response:\n%s\n"
                       "Now, will reboot bmc to recovery GPIO info" % (k, initial, res), decide=False)
                set_reboot(device)
                raise RuntimeError("Fail! GPIO Direction transform error")
    log.info("[%s]: After transform Direction, Re-acquire data information." % datetime.now())
    for i in num_list:
        cmd_2 = "ipmitool raw 0x3a 0x24 0x02 %s" % i
        res_2 = openbmc_lib.execute(device_obj, cmd_2, mode=CENTOS_MODE)
        if " 00" in res_2:
            data_low_list.append(i)
        elif " 01" in res_2:
            data_high_list.append(i)
        else:
            PRINTE("Fail! Now, will reboot bmc to recovery GPIO info", decide=False)
            set_reboot(device)
            PRINTE("Fail! After Direction transform, Data get response isn't [00,01]. it's[%s]" % res_2)

    for _ in data_list:  # for data transform
        initial = "low" if data_list.index(_) == 0 else "high"
        set_num = "6" if data_list.index(_) == 0 else "5"
        response = " 01" if data_list.index(_) == 0 else " 00"
        for j in _:  # set low to high:00->01, high to low:01->00
            cmd = "ipmitool raw 0x3a 0x24 0x0%s %s" % (set_num, j)
            openbmc_lib.execute(device_obj, cmd, mode=CENTOS_MODE)
        for k in _:  # Check if the setup is successful
            cmd = "ipmitool raw 0x3a 0x24 0x02 %s" % k
            res = openbmc_lib.execute(device_obj, cmd, mode=CENTOS_MODE)
            if response not in res:
                PRINTE("Fail! Now, will reboot bmc to recovery GPIO info", decide=False)
                set_reboot(device)
                PRINTE("Fail! [%s] Initial attributes: [%s].But the setting fails. response:\n%s" % (k, initial, res))
        set_num = "5" if data_list.index(_) == 0 else "6"
        response = " 00" if data_list.index(_) == 0 else " 01"
        for p in _:  # recovery data:00->01->00. 01->00->01
            cmd = "ipmitool raw 0x3a 0x24 0x0%s %s" % (set_num, p)
            openbmc_lib.execute(device_obj, cmd, mode=CENTOS_MODE)
        for k_p in _:  # check recovery has been done
            cmd = "ipmitool raw 0x3a 0x24 0x02 %s" % k_p
            res = openbmc_lib.execute(device_obj, cmd, mode=CENTOS_MODE)
            if response not in res:
                PRINTE("Fail! Now, will reboot bmc to recovery GPIO info", decide=False)
                set_reboot(device)
                PRINTE("Fail! [%s] Initial attributes: [%s]. But recovery failed. response:\n%s" % (k_p, initial, res))

    for _ in direction_list:  # for direction recovery
        initial = "input" if direction_list.index(_) == 0 else "output"
        set_num = "3" if direction_list.index(_) == 0 else "4"  # recovery:00->01->00. 01->00->01
        response = " 00" if direction_list.index(_) == 0 else " 01"
        for p in _:
            cmd = "ipmitool raw 0x3a 0x24 0x0%s %s" % (set_num, p)
            openbmc_lib.execute(device_obj, cmd, mode=CENTOS_MODE)
        for k_p in _:  # check recovery has been done
            cmd = "ipmitool raw 0x3a 0x24 0x01 %s" % k_p
            res = openbmc_lib.execute(device_obj, cmd, mode=CENTOS_MODE)
            if response not in res:
                PRINTE("Fail! [%s] Initial attributes: [%s]. Recovery failed."
                       "response:\n%s" % (k_p, initial, res), decide=False)
                direction_flag = False
        if not direction_flag:
            set_reboot(device)
            raise RuntimeError("Fail! GPIO Direction recovery error")
    log.info("[%s]: Pass! GPIO Direction OK" % datetime.now())


def check_bmc_virtual_usb_status(device, cmd=cmd_get_bmc_virtual_usb_status, enable=True):
    """
    Get BMC USB virtual device status, default:disabled(01)
    :param device:
    :param enable: True/Faile
    :return: usb status
    """
    device_obj = Device.getDeviceObject(device)
    res = openbmc_lib.execute(device_obj, cmd, mode=CENTOS_MODE)
    status = "00" if enable else "01"
    if status not in res.strip():
        PRINTE("Fail! Exp bmc status:[%s], got [%s]" % (status, res))


def get_ether_from_ifconfig(device, net_name="etho"):
    """
    Get all ether information through 'ifconfig'
    :param device:
    :param net_name:network name  e.g eth0,eth1
    :return:Information of ether corresponding to the network
    """
    ether_dict = dict()
    cmd = "ifconfig"
    device_obj = Device.getDeviceObject(device)
    response = openbmc_lib.execute(device_obj, cmd, mode=CENTOS_MODE)
    for _ in response.split("\n\r\n"):
        a = re.findall("(\w+):\s.*ether\s(.*)  txqueuelen", _, re.S)
        if a:
            ether_dict[a[0][0]] = a[0][1]
    log.info("get all ether info: %s" % str(ether_dict))
    return ether_dict[net_name]


def set_bmc_virtual_usb_device(device, enable=True, ip=None):
    """
    Enable/Disenable BMC Virtual USB device
    :param device:
    :param enable:True-enable,False-disenable
    :param ip:bmc ip
    """
    res = "00" if enable else "01"
    device_obj = Device.getDeviceObject(device)
    if ip:
        cmd = r"ipmitool -I lanplus -H %s -U admin -P admin raw 0x32 0xaa 0x%s" % (ip, res)
        Device.execute_local_cmd(device_obj, cmd)
        cmd = r"ipmitool -I lanplus -H %s -U admin -P admin raw 0x32 0xab" % ip
        response = Device.execute_local_cmd(device_obj, cmd)
    else:
        cmd = r"ipmitool raw 0x32 0xaa 0x%s" % res
        openbmc_lib.execute(device_obj, cmd, mode=CENTOS_MODE)
        cmd = r"ipmitool raw 0x32 0xab"
        response = openbmc_lib.execute(device_obj, cmd, mode=CENTOS_MODE)
    if res not in response:
        PRINTE("Fail! couldn't get [%s], response:\n%s" % (res, response))
    set_wait(20)


def set_update_bios_primary_backup(device, primary=True, decide=True, ip=None):
    """
    Set and update the main/standby bios, and check whether the setting is successful
    :param device: the name of the tested product
    :param primary: True-primary bios False-backup bios
    :param decide: whether the expected setting is successful
    :param ip: when it is None, it will connect directly, otherwise remote command
    """
    device_obj = Device.getDeviceObject(device)
    machine = "00" if primary else "01"
    if ip:
        cmd = "ipmitool -I lanplus -H %s -U admin -P admin raw 0x3a 0x05 0x01 0x%s" % (ip, machine)
        Device.execute_local_cmd(device_obj, cmd)
        cmd_check = r"ipmitool -I lanplus -H %s -U admin -P admin raw 0x3a 0x05 0x00" % ip
        res = Device.execute_local_cmd(device_obj, cmd_check)
    else:
        cmd = r"ipmitool raw 0x3a 0x05 0x01 0x%s" % machine
        openbmc_lib.execute(device_obj, cmd, mode=CENTOS_MODE)
        cmd_check = r"ipmitool raw 0x3a 0x05 0x00"
        res = openbmc_lib.execute(device_obj, cmd_check, mode=CENTOS_MODE)
    if decide:
        if machine not in res:
            PRINTE("Fail! couldn't get the [%s],response:\n%s" % (machine, res))
    else:
        if machine in res:
            PRINTE("Fail! get the [%s],response:\n%s" % (machine, res))


def set_start_bios_primary_backup(device, primary=True, ip=None):
    """
    Set the next boot from the main/standby BIOS
    :param device:the name of the tested productupdate_by_cfu
    :param primary:True-primary bios False-backup bios
    :param ip:bmc ip
    """
    machine_cmd = cmd_set_bios_next_start_primary if primary else cmd_set_bios_next_start_backup
    send_cmd(device, machine_cmd, ip)


def check_bmc_ready(device, wait_time=None):
    """
    Check whether the BMC is in a normal state (has been restarted)
    :param device:product under test
    :param wait_time:Waiting time before inspection
    """
    device_obj = Device.getDeviceObject(device)
    if wait_time:
        set_wait(wait_time)
    s_time = time.time()
    while time.time() - s_time <= 200:
        try:
            device_obj.switchToBmc()
            set_wait(40)
            cmd = "ipmitest mc info"
            res = openbmc_lib.execute(device_obj, cmd, mode="OPENBMC")
            if "Device ID" in res:
                log.info("BMC has ready!")
                break
        except Exception:
            time.sleep(10)
    device_obj.trySwitchToCpu()
    cmd = r"ipmitool mc info"
    res = openbmc_lib.execute(device_obj, cmd, mode=CENTOS_MODE)
    if "Device ID" not in res:
        log.info("Fail! Switch To Cpu: fail")


def update_by_cfu(device, update_type, primary=True, version="now", update_time=1200, bmc_ip=None, return_name=False):
    """
     Update bmc/cpld/bios version by cfu.
    :param device: product under test
    :param update_type: bmc,cpld,bios
    :param primary: True-primary;False-backup.if 'update_type' is cpld,the parameter is invalid
    :param version:now-higher version;old-lower version
    :param update_time:Upgrade timeout
    :param bmc_ip:bmc ip
    :param return_name:if True, will return the update file name
    """
    tool_path = get_tool_path()
    set_os_ip_by_dhclient(device)
    device_obj = Device.getDeviceObject(device)
    n = "1" if primary else "2"
    update_type = update_type.lower()
    if update_type not in ["bmc", "cpld", "bios"]:
        PRINTE("Fail! Parameter must be ‘bmc','cpld','bios'")
    if update_type == "bmc":
        done_keyword = r"Resetting the firmware.........."  # bmc upgrade completion sign word
    elif update_type == "cpld":
        done_keyword = r"Verifying Firmware Image"  # cpld upgrade completion sign word
    else:
        done_keyword = "Verifying Firmware Image : 100%... done"
    pc_version_path = r"%s/cfu/%s/%s" % (tool_path, update_type, version)
    cmd = "ls %s" % pc_version_path
    update_file_name = Device.execute_local_cmd(device_obj, cmd, timeout=60).strip()
    dut_file_path = r"/home/white_box"
    pc_user = python_server_user
    pc_password = python_server_password
    pc_ip = python_server_ip
    pc_cfu_path = r"%s/cfu" % tool_path
    pc_cfu_name = r"CFUFLASH"
    dut_cfu_path = r"%s/%s" % (dut_file_path, pc_cfu_name)
    dut_version_path = r"%s/%s" % (dut_file_path, update_file_name)
    if bmc_ip:
        if update_type == "bmc":
            cmd = "echo y | %s -nw -ip %s -U admin -P admin -d 1 -mse %s %s" % (pc_cfu_path + "/" + pc_cfu_name, bmc_ip,
                                                                                n, pc_version_path + "/" +
                                                                                update_file_name)
        elif update_type == "cpld":
            cmd = "echo y | %s -nw -ip %s -U admin -P admin -d 4 %s" % (pc_cfu_path + "/" + pc_cfu_name, bmc_ip,
                                                                        (pc_version_path + "/" + update_file_name))
        else:
            cmd = "echo y | %s -nw -ip %s -U admin -P admin -d 2 %s -mse %s -fb" \
                  % (pc_cfu_path + "/" + pc_cfu_name, bmc_ip, (pc_version_path + "/" + update_file_name), n)
        set_sel_clear(device, bmc_ip)
        res = Device.execute_local_cmd(device_obj, cmd, timeout=update_time)
        if update_type == "bmc":
            check_bmc_ready(device, 60)
            check_reset_sel_info(device, bmc_ip, "reboot")
        if done_keyword in res:
            log.info("Pass! update_by_cfu. Now, Pls wait for some time to confirm system is normal!")
            connect(device, 60, 540)
            check_bmc_ready(device, 60)
        else:
            PRINTE("Fail! %s upgrade by lan fail.response:\n%s" % (update_type, res))

    else:
        delete_folder(device, dut_file_path)
        res = openbmc_lib.execute(device_obj, "hostname -I", mode=CENTOS_MODE)
        os_ip = re.findall("(10\.10\.10\.\d+)\s+", res)[0].strip()
        mkdir_data_path(device, dut_file_path)
        copy_files_from_pc_to_os(device, pc_user, pc_password, pc_ip, update_file_name, pc_version_path, dut_file_path,
                                 50)
        copy_files_from_pc_to_os(device, pc_user, pc_password, pc_ip, pc_cfu_name, pc_cfu_path, dut_file_path, 50)
        chmod_file(device, dut_cfu_path)
        if update_type == "bmc":
            cmd = "echo y | %s -cd -d 1 -mse %s %s" % (dut_cfu_path, n, dut_version_path)
        elif update_type == "cpld":
            cmd = "echo y | %s -cd -d 4 %s" % (dut_cfu_path, dut_version_path)
        else:
            cmd = "echo y | %s -cd -d 2 %s" % (dut_cfu_path, dut_version_path)

        set_sel_clear(device)
        device_obj.sendline(cmd)
        output = device_obj.read_until_regexp(done_keyword, timeout=update_time)
        if update_type == "bmc":
            check_bmc_ready(device, 60)
            check_reset_sel_info(device, bmc_ip, "reboot")
            error_str_1 = "Maybe ok, but ipmi might run very slowly."
            error_str_2 = "Couldn't get irq info: d1."
            if error_str_1 in output:
                PRINTE("Fail! Error statement found during the upgrade process:[%s]" % error_str_1)
            if error_str_2 in output:
                PRINTE("Fail! Error statement found during the upgrade process:[%s]" % error_str_2)
        log.info("Pass! update_by_cfu")
        connect(device, 60, 540)
        openbmc_lib.execute(device_obj, "rm -rf %s" % dut_file_path, mode=CENTOS_MODE)
        set_root_hostname(device)
    if return_name:
        return update_file_name[:-4]


def set_pdu_status(device, pdu_status, pdu_port):
    """
    Control the operation of PDU to power on, power off, and restart the device
    :param device:product under test
    :param pdu_status:[on,off,reboot]
    :param pdu_port:The port number on the PDU of the device under test
    """
    tool_path = get_tool_path()
    device_obj = Device.getDeviceObject(device)
    status = pdu_status.lower()
    shell_name = ""
    if status == "on":
        shell_name = "PDU_ON.sh"
    elif status == "off":
        shell_name = "PDU_OFF.sh"
    elif status == "reboot":
        shell_name = "PDU_Reboot.sh"
    else:
        PRINTE("Fail! PDU status must be on,off,reboot!")
    pdu_shell_path = "%s/%s" % (tool_path, shell_name)
    cmd = "%s %s" % (pdu_shell_path, pdu_port)
    res = Device.execute_local_cmd(device_obj, cmd, timeout=60)
    if "Success" in res:
        log.info("[%s]: PDU has %s!" % (datetime.now(), status))
    else:
        PRINTE("Fail! PDU [%s] port [%s] fail!" % (pdu_status, pdu_port))


def set_os_ip_by_dhclient(device):
    """
    Obtain ip automatically, generally used in situations where the device needs to be
    re-obtained after restarting the device.
    """
    device_obj = Device.getDeviceObject(device)
    for i in range(3):
        openbmc_lib.execute(device_obj, "dhclient", mode=CENTOS_MODE)
        res = openbmc_lib.execute(device_obj, "ifconfig", mode=CENTOS_MODE)
        os_ip = re.findall(r"inet\s+(\d+\.\d+\.\d+\.\d+)\s+netmask.*broadcast.*", res)
        if os_ip:
            break
        else:
            os_ip = re.findall(r"inet addr:(\d+\.\d+\.\d+\.\d+)\s+Bcast", res)
            if os_ip:
                break
        time.sleep(10)
    else:
        PRINTE("Fail! Couldn't got OS IP!")


def set_pdu_status_connect_os(device, status, port, out_time=600, wait_time=None):
    """
    connec os after pdu send command
    :param device:product under test
    :param status:[on,off,reboot]
    :param port:The port number on the PDU of the device under test
    :param out_time:connect os out time
    :param wait_time:Waiting time after operating PDU
    """
    set_pdu_status(device, status, port)
    connect(device, wait_time, timeout=out_time)
    set_os_ip_by_dhclient(device)


def get_cpld_version_power_ac(device, pdu_port):
    """
    get CPLD_BaseBoard,CPLD_COMe version information when the device reboot,then connect OS
    :return: 'CPLD_BaseBoard CPLD_COMe'(string)
    """
    device_obj = Device.getDeviceObject(device)
    set_pdu_status(device, "reboot", pdu_port)
    output = device_obj.read_until_regexp("Press <DEL> or <ESC> to enter setup.", timeout=300)
    come_version = re.findall(r"CPLD_C version.*: (.*)", output)
    baseboard_version = re.findall(r"CPLD_B version.*: (.*)", output)
    if baseboard_version and come_version:
        baseboard_version = baseboard_version[0].strip()
        come_version = come_version[0].strip()
        version_info = "%s %s" % (baseboard_version, come_version)
        log.info("Pass! Got CPLD_BaseBoard version:[%s], CPLD_COMe version:[%s]"
                 % (baseboard_version, come_version))
        connect(device)
        check_reset_sel_info(device, restart_method="AC")
        return version_info
    else:
        device_obj.getPrompt(CENTOS_MODE, timeout=300)
        PRINTE("Fail! Couldn't got CPLD version info.response:\n%s" % output)


def get_cpld_version_in_os(device):
    """
    Get COMECPLD/Base board/switch board 1 2 3 4  version
    :return: string of cpld version. 'COMECPLD Base board switch board1 switch board2 switch board3 switch board4'
    """
    device_obj = Device.getDeviceObject(device)
    device_obj.sendline("echo 0xA1E0 > /sys/devices/platform/sys_cpld/getreg")
    cmd_list = ["cat /sys/devices/platform/sys_cpld/getreg", "ipmitool raw 0x3a 0x64 0 1 0",
                "cat /sys/bus/i2c/devices/i2c-10/10-0030/version",
                "cat /sys/bus/i2c/devices/i2c-10/10-0031/version",
                "cat /sys/bus/i2c/devices/i2c-10/10-0032/version",
                "cat /sys/bus/i2c/devices/i2c-10/10-0033/version"]
    all_cpld_version = list()
    for cmd in cmd_list:
        result = execute(device, cmd)
        res = re.findall(r".*%s(.*)\n+real.*" % cmd, result, re.S)
        for i in res:
            if i == "":
                res.remove(i)
        if res:
            res_list = res[0].split("\n")
            response = ""
            for line in res_list:
                response = response + "\n" + line
            all_cpld_version.append(response.strip())
        else:
            PRINTE("Fail! cmd[%s], response:\n%s" % (cmd, result))
    return " ".join(all_cpld_version)


def get_dmidecode_info(device):
    """
    Send cmd:dmidecode and retuen the response
    """
    device_obj = Device.getDeviceObject(device)
    set_root_hostname(device)
    cmd = "dmidecode"
    res = openbmc_lib.execute(device_obj, cmd, mode=CENTOS_MODE)
    res = res.strip()
    dmi_info = re.findall(r"(# dmidecode.*End Of Table)", res, re.S)
    if dmi_info:
        return dmi_info[0]
    else:
        PRINTE("Fail! Couldn't got dmidecode info, response:\n%s" % dmi_info)


def check_dmidecode_info_equal(str_1, str_2, decide=True):
    """
    Compare all information except bios 'Version' and bios 'Release Date' in dmidecode information
    :param str_1: dmidecode info 1
    :param str_2: dmidecode info 2
    :param decide: True ir False
    """
    str_1_re = str_1.replace(re.findall(r".*BIOS Information.*?(Vendor:.*?Version:.*?Release Date.*?Address)",
                                        str_1, re.S)[0], "")
    str_2_re = str_2.replace(re.findall(r".*BIOS Information.*?(Vendor:.*?Version:.*?Release Date.*?Address)",
                                        str_2, re.S)[0], "")
    if decide:
        if str_1_re != str_2_re:
            PRINTE("Fail!\ninfo_1: \n%s\ninfo_2: \n%s" % (str_1, str_2))
    else:
        if str_1_re == str_2_re:
            PRINTE("Fail!\ninfo_1: \n%s\ninfo_2: \n%s" % (str_1, str_2))


def check_sel_info_only_clear(device, decide=True, ip=None):
    """
    Confirm whether there is only sel cllear event record in the sel list
    :param device: product under test
    :param decide: True/False
    :param ip:bmc ip
    """
    device_obj = Device.getDeviceObject(device)
    if ip:
        cmd = "ipmitool -I lanplus -H %s -U admin -P admin sel list" % ip
        res = Device.execute_local_cmd(device_obj, cmd)
    else:
        cmd = "ipmitool sel list"
        res = openbmc_lib.execute(device_obj, cmd, mode=CENTOS_MODE)
    sel_num = re.findall(r"\s+(\d+)\s+", res)
    if decide:
        if len(sel_num) != 1:
            PRINTE("Fail! sel list more than 'sel clear' events recorded")
    else:
        if len(sel_num) == 1:
            PRINTE("Fail! sel list only 'sel clear' events recorded")


def set_boot_option_1(device, cycle_bios_gui=True, ip=None):
    """
    Enter the BIOS interface and set 'Boot Option #1 = P0：M.2 (S80)' in BOOT。
    :param device: product under test
    :param cycle_bios_gui: Whether to use the cycle of this function, when it is False,
                            please make sure that the device is in the restarting phase
    :param ip: BMC IP
    """
    output = ""
    page_1 = "System Date"
    page_2 = "USB Configuration"
    page_3 = r"may cause system to malfunction"
    page_4 = r"BMC network configuration"
    page_5 = r"Maximum length"
    page_6 = r"Boot Option #2"
    page_7 = r"Boot Override"
    page_list = [page_1, page_2, page_3, page_4, page_5, page_6, page_7]
    device_obj = Device.getDeviceObject(device)
    if cycle_bios_gui:
        # enter_bios_line = r"Press <F2> or <DEL> to enter setup."
        enter_bios_line = r"Press <DEL> or <ESC> to enter setup"
        set_power_status(device, "cycle", ip=ip)
        device_obj.read_until_regexp(enter_bios_line, timeout=300)
        send_key(device, "KEY_DEL")
        device_obj.read_until_regexp(page_1, timeout=30)
    for _ in range(1, 6):
        send_key(device, "KEY_RIGHT")
        if _ == 5:
            output = device_obj.read_until_regexp(page_list[_], timeout=30)
    if "M.2" not in output:
        for _ in range(3):
            send_key(device, "KEY_DOWN")
            time.sleep(1.5)
        send_key(device, "KEY_ENTER")
        if "AMI Virtual" in output:
            log.info("Boot Option #1:[AMI Virtual]")
            send_key(device, "KEY_DOWN")
            time.sleep(1.5)
        elif "UEFI" in output:
            log.info("Boot Option #1:[UEFI]")
            send_key(device, "KEY_UP")
            time.sleep(1.5)
        else:
            log.info("Boot Option #1:[Disabled]")
            send_key(device, "KEY_UP")
            time.sleep(1.5)
            send_key(device, "KEY_UP")
            time.sleep(1.5)
        send_key(device, "KEY_ENTER")
        time.sleep(2)
        save_bios_and_exit(device)
    else:
        line_exit = 'Quit without saving?'
        send_key(device, "KEY_ESC")
        device_obj.read_until_regexp(line_exit, timeout=30)
        send_key(device, "KEY_ENTER")
        device_obj.getPrompt(CENTOS_MODE, timeout=160)


def save_bios_and_exit(device, connection=True):
    """
    Save and exit the bios interface
    :param device:product under test
    :param connection:connect os
    """
    device_obj = Device.getDeviceObject(device)
    for _ in range(1, 8):
        try:
            send_key(device, "KEY_RIGHT")
            device_obj.read_until_regexp("Save Changes and Exit", timeout=5)
            break
        except Exception:
            pass
    send_key(device, "KEY_ENTER")
    device_obj.read_until_regexp("Save configuration and exit?", timeout=10)
    send_key(device, "KEY_ENTER")
    log.info("BIOS Step has saved")
    if connection:
        device_obj.getPrompt(CENTOS_MODE, timeout=300)


def enter_bios_setup(device, timeout=600):
    """
    Enter bios setup
    :param device: product under test
    :param timeout: time out
    """
    enter_bios_line = "Press <DEL> or <ESC> to enter setup"
    bios_gui_lin = r"System Date"
    device_obj = Device.getDeviceObject(device)
    device_obj.read_until_regexp(enter_bios_line, timeout=timeout)
    send_key(device, "KEY_DEL")
    device_obj.read_until_regexp(bios_gui_lin, timeout=20)
    log.info("Pass! Enter bios setup1")


def check_bios_info_power_cycle(device, exp_version, boot_bios="primary", ip=None):
    """
    When power cycle, check bios version, Boot from Primary/Backup BIOS.
    :param device:product under test
    :param exp_version:bios version
    :param boot_bios:primary/backup
    :param ip:bmc ip
    """
    enter_bios_line = "Press <DEL> or <ESC> to enter setup"
    bios_gui_lin = r"System Date"
    device_obj = Device.getDeviceObject(device)
    set_power_status(device, "cycle", ip=ip)
    output = device_obj.read_until_regexp(enter_bios_line, timeout=300)
    send_key(device, "KEY_DEL")
    res = device_obj.read_until_regexp(bios_gui_lin, timeout=20)
    bios_version = re.findall(r"BIOS Date:.* Ver:\s+(.*?)\s+\[3;1H.*\[4;1H", output, re.S)
    bios_version_ = re.findall(r"Project Version.*(COMe-Dnvt.*) x64", res)
    if not bios_version:
        PRINTE("Fail! Couldn't get BIOS version.response:\n%s" % output)
    bios_version = bios_version[0].strip()
    if not bios_version_:
        PRINTE("Fail! Couldn't get bios version from bios gui! Response:\n%s" % res)
    bios_version_ = bios_version_[0].strip()
    if bios_version_ != bios_version:
        PRINTE("Fail! The bios version information in the bios setting interface is different from the "
               "version information printed during the power cycle, respectively: [%s], [%s]"
               % (bios_version_, bios_version))
    primary_backup = re.findall(r"((?:Primary|Backup)) BIOS boot in progress", output)
    if not primary_backup:
        PRINTE("Fail! Couldn't get Boot BIOS.response:\n%s" % output)
    primary_backup = primary_backup[0].strip()
    if bios_version != exp_version:
        PRINTE("Fail! get bmc version:[%s], expect:[%s]" % (bios_version, exp_version))
    if primary_backup.lower() != boot_bios:
        PRINTE("Fail! get bmc version:[%s], expect:[%s]" % (primary_backup, boot_bios))


def check_bmc_kcs_communicate(device, decide=True):
    """
    Check if system can communicate with BMC with default KCS port 0xca0
    :param device:product under test
    :param decide: True/False
    """
    device_obj = Device.getDeviceObject(device)
    cmd = "dmesg | grep ipmi"
    res = openbmc_lib.execute(device_obj, cmd, mode=CENTOS_MODE)
    if "ipmi_si" not in res:
        if decide:
            PRINTE("Fail!  System can't communicate with BMC with default KCS port 0xca0. Response:\n%s" % res)


def get_pef_config(device, cmd):
    """
    9.8.1 PEF Configuration Test.
    Get PEF config and return them
    :param device: product under test
    :param cmd: get cmd
    :return: config
    """
    ip = get_ip_address_from_ipmitool(device)
    res = send_cmd(device, cmd, ip=ip, return_res=True)
    if "\n" in res:
        res = res.replace("\n", " ")
    return res


def set_pef_config(device, num, data):
    """
    Use with get_pef_config，Set PEF according to its return value
    :param device:product under test
    :param num:Location to be set
    :param data:get_pef_config  return value
    """
    data = re.findall(r"\s{0,}11(.*)", data)[0].strip()
    a = data.split(" ")
    all_info = ""
    for i in a:
        i = "0x%s" % i
        all_info = all_info + " %s" % i
    cmd = "ipmitool raw 04 0x12 0x%s %s" % (num, all_info)
    send_cmd(device, cmd)


def set_pef_filter_close(device, num):
    """
    Close PEF filter
    :param device: product under test
    :param num: Fill in the decimal number 1 to 40 or 'all' to close all filter
    """
    device_obj = Device.getDeviceObject(device)
    if num.lower() == "all":
        for i in range(1, 41):
            cmd = "ipmitool raw 0x04 0x12 0x06 %s 0x00 0x05 0x01 0x10 0x20 0x00 0x02 0xff 0xff 0xff 0xff 0 0 0 0 0 0 " \
                  "0 0 0" % str(hex(i))
            openbmc_lib.execute(device_obj, cmd, mode=CENTOS_MODE)
    else:
        num = str(hex(int(num)))
        cmd = "ipmitool raw 0x04 0x12 0x06 %s 0x00 0x05 0x01 0x10 0x20 0x00 0x02 0xff 0xff 0xff 0xff 0 0 0 0 0 0 0 " \
              "0 0" % num
        openbmc_lib.execute(device_obj, cmd, mode=CENTOS_MODE)


def copy_shell_to_dut(device, shell_name):
    """
    From PC copy shell to DUT
    :param device:product under test
    :param shell_name: Name of the shell script to be copied
    :return:
    """
    tool_path = get_tool_path()
    dut_file_path = r"/home/white_box"
    pc_user = python_server_user
    pc_password = python_server_password
    pc_ip = python_server_ip
    pc_shell_path = r"%s/shell" % tool_path
    delete_folder(device, dut_file_path)
    mkdir_data_path(device, dut_file_path)
    copy_files_from_pc_to_os(device, pc_user, pc_password, pc_ip, shell_name, pc_shell_path, dut_file_path, 50)
    chmod_file(device, "%s/%s" % (dut_file_path, shell_name))


def get_sel_information(device, ip=None, res_return=True):
    """
    Send 'ipmitool sel information' and record it
    :param device: the name of the tested product
    :param ip: BMC ip
    :param res_return: return it or not
    """
    device_obj = Device.getDeviceObject(device)
    if ip:
        cmd = "ipmitool -I lanplus -H %s -U admin -P admin sel information" % ip
        res = Device.execute_local_cmd(device_obj, cmd, timeout=60)
    else:
        cmd = r"ipmitool sel information"
        res = openbmc_lib.execute(device_obj, cmd, mode=CENTOS_MODE)
    if res_return:
        return res


def check_sel_shell_info_linear(device, timeout):
    """
    Linear: Fill up the sel event through the shell script, and check that its maximum serial number is 3639
    (hexadecimal e37),'Entries','Free Space','Percent Used' in the sel information
    are 3639, 0 bytes, 100% respectively
    :param device:the name of the tested product
    :param timeout:Execution timeout of shell script
    """
    a = ["3639", "0 bytes", "100%"]
    b = list()
    keyword_list = ["Entries\s+:(.*)", "Free Space\s+:(.*)", "Percent Used\s+:(.*)"]
    ip = get_ip_address_from_ipmitool(device)
    tool_path = get_tool_path()
    cmd = "%s/shell/SELPolicy.sh %s 0 3645" % (tool_path, ip)
    device_obj = Device.getDeviceObject(device)
    res = Device.execute_local_cmd(device_obj, cmd, timeout=int(timeout))
    if "Out of space" not in res and "Generate SEL: 3639" not in res:
        PRINTE("Fail! SEL linear error!, couldn't find keyword [Out of space], [Generate SEL: 3639], response:\n%s"
               % res)
    res_sel_list = get_sel_list(device, ip, True)
    if "e37" not in res_sel_list:
        PRINTE("Fail! The SEL linear maximum value after filling is not 'e37'")
    res_sel_information = get_sel_information(device, ip, True)
    for word in keyword_list:
        c = re.findall(word, res_sel_information)[0].strip()
        b.append(c)
    if a != b:
        PRINTE("Fail! Get sel information was error. response:\n%s" % res_sel_information)


def check_sel_shell_info_circular(device, timeout):
    """
    Circular: Fill up the sel event through the shell script, and check that its maximum serial number is 3639
    (hexadecimal fffe),'Entries','Free Space','Percent Used' in the sel information
    are 3639, 0 bytes, 100% respectively
    :param device:the name of the tested product
    :param timeout:Execution timeout of shell script
    """
    a = ["3639", "0 bytes", "100%"]
    b = list()
    keyword_list = ["Entries\s+:(.*)", "Free Space\s+:(.*)", "Percent Used\s+:(.*)"]
    ip = get_ip_address_from_ipmitool(device)
    tool_path = get_tool_path()
    cmd = "%s/shell/SELPolicy.sh %s 1 65538" % (tool_path, ip)
    device_obj = Device.getDeviceObject(device)
    log.info("[%s]: The shell script will be run, which takes several hours" % str(datetime.time()))
    res = Device.exe_local_cmd_by_os_popen(device_obj, cmd)
    if "Generate SEL: 65535" not in res:
        PRINTE("Fail! SEL circular error!")
    res_sel_list = get_sel_list(device, ip, True)
    if r"fffe" not in res_sel_list:
        PRINTE("Fail! 'fffe' not in sel list")
    sel_list_line_list = res_sel_list.splitlines()
    for line in sel_list_line_list:
        if "fffe |" in line:
            line_check = sel_list_line_list[sel_list_line_list.index(line) + 1]
            if not re.findall(r"\s+1\s\|", line_check):
                PRINTE("Fail! 'fffe' next line number isn't '1'.Next line:\n%s" % line_check)
    res_sel_information = get_sel_information(device, ip, True)
    for word in keyword_list:
        c = re.findall(word, res_sel_information)[0].strip()
        b.append(c)
    if a != b:
        PRINTE("Fail! Get sel information was error. response:\n%s" % res_sel_information)


def get_info_from_lan_print(device, item, bios=False, ip=None):
    """
    Get the information in 'lan print 1' to form a dictionary and return the value of
    the corresponding key
    :param device:the name of the tested product
    :param item: "IP Address Source", "IP Address", "Subnet Mask", "MAC Address"
    :param bios:Format when displayed on the bios interface
    :param ip:bmc ip
    :return:The key value
    """
    device_obj = Device.getDeviceObject(device)
    if ip:
        cmd = "ipmitool -I lanplus -H %s -U admin -P admin lan print 1" % ip
        res = Device.execute_local_cmd(device_obj, cmd)
    else:
        cmd = r"ipmitool lan print 1"
        res = openbmc_lib.execute(device_obj, cmd, mode=CENTOS_MODE)
    key_list = ["IP Address Source", "IP Address", "Subnet Mask", "MAC Address"]
    value_list = list()
    for info in key_list:
        value = re.findall(r"%s\s+:(.*)" % info, res)[0].strip()
        if ":" in value and bios:
            value = value.replace(":", "-")
        elif value == "DHCP Address" and bios:
            value = "DynamicAddressBmcDhcp"
        elif value == 'Static Address' and bios:
            value = "StaticAddress"
        value_list.append(value)
    info_dict = dict(zip(key_list, value_list))
    return info_dict[item]


def get_network_from_bios(device, currentconfiguration, stationipaddress, subnetmask, stationmacaddress):
    """
    Check bios Network informations`
    :param device:the name of the tested product
    :param currentconfiguration: Current Configuration
    :param stationipaddress: Station IP address
    :param subnetmask: Subnet mask
    :param stationmacaddress: Station MAC address
    """
    page_1 = "System Date"
    page_2 = "USB Configuration"
    page_3 = "South Bridge Chipset Configuration"
    page_4 = r"BMC network configuration"
    enter_flag = r"Router MAC address"
    enter_bios_line = "Press <DEL> or <ESC> to enter setup"
    device_obj = Device.getDeviceObject(device)
    set_power_status(device, "cycle")
    device_obj.read_until_regexp(enter_bios_line, timeout=200)
    send_key(device, "KEY_DEL")
    device_obj.read_until_regexp(page_1, timeout=20)
    send_key(device, "KEY_RIGHT")
    device_obj.read_until_regexp(page_2, timeout=20)
    send_key(device, "KEY_RIGHT")
    device_obj.read_until_regexp(page_3, timeout=20)
    send_key(device, "KEY_RIGHT")
    device_obj.read_until_regexp(page_4, timeout=20)
    send_key(device, "KEY_DOWN", 9)
    send_key(device, "KEY_ENTER")
    send_key(device, "KEY_DOWN", 1)
    all_info = device_obj.read_until_regexp(enter_flag, timeout=20)
    error_str = ""
    try:
        current_configuration = re.findall(r"Current.*((?:StaticAddress|DynamicAddressBmcDhcp))",
                                           all_info, re.S)
        if not current_configuration:
            error_str = error_str + "\nCouldn't find 'StaticAddress' or 'DynamicAddressBmcDhcp'"
        else:
            current_configuration = current_configuration[0]
            log.info("current_configuration:%s" % current_configuration)
        station_ip_address = re.findall(r"Station IP address.*?(\d+\.\d+\.\d+\.\d+)", all_info, re.S)
        if not station_ip_address:
            error_str = error_str + "\nCouldn't find 'Station IP address' info"
        else:
            station_ip_address = station_ip_address[0]
            log.info("station_ip_address:%s" % station_ip_address)
        subnet_mask = re.findall(r"Subnet mask.*?(\d+\.\d+\.\d+\.\d+)", all_info, re.S)
        if not subnet_mask:
            error_str = error_str + "\nCouldn't find 'Subnet mask' info"
        else:
            subnet_mask = subnet_mask[0]
            log.info("subnet_mask:%s" % subnet_mask)
        station_mac_address = re.findall(r"Station MAC address.*?47m(\w+-\w+-\w+-\w+-\w+-\w+)", all_info, re.S)
        if not station_mac_address:
            error_str = error_str + "\nCouldn't find 'Station MAC address' info"
        else:
            station_mac_address = station_mac_address[0]
            log.info("station_mac_address:%s" % station_mac_address)
        if currentconfiguration != current_configuration:
            error_str = error_str + "\nFail! 'Current Configuration', os:%s,bios:%s!" \
                        % (currentconfiguration, current_configuration)
        if stationipaddress != station_ip_address:
            error_str = error_str + "\nFail! 'Station IP address', os:%s,bios:%s!" \
                        % (stationipaddress, station_ip_address)
        if subnetmask != str(subnet_mask):
            error_str = error_str + "\nFail! 'Subnet mask', os:%s,bios:%s!" % (subnetmask, subnet_mask)
        if stationmacaddress != station_mac_address:
            error_str = error_str + "\nFail! 'Station MAC address', os:%s,bios:%s!" \
                        % (stationmacaddress, station_mac_address)
    except Exception as E:
        log.error(str(E))
    finally:
        send_key(device, "KEY_ESC")
        device_obj.read_until_regexp(page_4, timeout=20)
        line_exit = 'Quit without saving?'
        send_key(device, "KEY_ESC")
        device_obj.read_until_regexp(line_exit, timeout=30)
        send_key(device, "KEY_ENTER")
        device_obj.getPrompt(CENTOS_MODE, timeout=160)
        set_root_hostname(device)
    if error_str:
        PRINTE("Fail! The information in the OS is different from the bios display! error info:\n%s" % error_str)


def send_cmd_without_return_rule(device, cmd, check_res=False, keyword=None, timeout=None):
    """
    Send cmd but don't Follow any return rules
    :param device:the name of the tested product
    :param cmd:command
    :param check_res:True-got response and check it
    :param keyword:response keyword
    :param timeout:Check the timeout of keywords in the return
    """
    device_obj = Device.getDeviceObject(device)
    device_obj.sendline(cmd)
    if check_res:
        device_obj.read_until_regexp(keyword, timeout=timeout)


def connect(device, wait_time=180, timeout=300, prodect_name="midstone100X"):
    """
    Connect tested product
    :param device: the name of the tested product
    :param wait_time: wait some time before connect
    :param timeout: connect out time
    :param prodect_name: product name
    """
    device_obj = Device.getDeviceObject(device)
    prodect_info = YamlParse.getDeviceInfo()[prodect_name]
    login_prompt = prodect_info["loginPromptDiagOS"]
    all_info = ""
    if wait_time:
        log.info("pls wait %d s" % int(wait_time))
    start_time = time.time()
    while time.time() - start_time < int(timeout):
        try:
            part_info = device_obj.readMsg()
            if part_info:
                part_info = part_info.strip()
                all_info = all_info + "\n" + part_info
                if "System Date" and "System Time" and "Access Level" in all_info:
                    log.error("Fail! device has enter Bios!! Part of the information "
                              "obtained during the waiting phase is:\n%s" % all_info)
                    whitebox_exit_bios_setup(device)
                    break
                elif login_prompt in all_info:
                    device_obj.getPrompt(CENTOS_MODE, timeout=30)
                    break
        except Exception as E:
            log.info(str(E))
            set_wait(20)
    set_root_hostname(device)
    check_bmc_ready(device)


def check_psu_data(device, cmd, info_rules):
    """
    check Left psu and right psu,the response value was not all 'ff' or
    first three digits must be in digital form
    :param device:the name of the tested product
    :param cmd:command
    :param info_rules:ff-the response value was not all 'ff'
                      digits-first three digits must be in digital form
    """
    device_obj = Device.getDeviceObject(device)
    res = openbmc_lib.execute(device_obj, cmd, mode=CENTOS_MODE)
    b = re.findall(".*ipmitool(.*)real.*", res, re.S)
    a = b[0].split("\n")
    a.remove(a[0])
    res_c = ""
    for i in a:
        res_c += i + "\n"
    res_c = res_c.strip()
    if info_rules == "ff":
        b = [j for i in res_c.splitlines() for j in i.split(" ") if j != "ff"]
        if not b:
            PRINTE("Fail! PSU got data was all 'ff'. response:\n%s" % res_c)
    else:
        if not re.findall(r"^\d+ \d+ \d+.*", res_c):
            PRINTE("Fail! PSU data first three digits are not in digital form")


def set_fan_scan_status(device, enable=True, ip=None):
    """
    Set fan scan enable/disenable
    :param device: the name of the tested product
    :param enable: True-enable,False-Disable
    :param ip: BMC IP
    """
    status = "1" if enable else "0"
    cmd = "ipmitool raw 0x3a 0x02 0x0%s" % status
    send_cmd(device, cmd, ip)


def check_fan_data(device, fan_num, ip=None):
    """
    Check that the fan data is valid
    :param device:the name of the tested product
    :param fan_num:fan number
    :param ip:BMC IP
    """
    cmd = "ipmitool fru print %s" % fan_num
    res = send_cmd(device, cmd, ip, True)
    if "Unknown FRU header version" in res:
        PRINTE("Fail! Got fan data fail, fan number:%s. Please refresh the fru data" % fan_num)


def transfer_shell_for_stress(device, shell_path, loop, pass_keyword, fail_keyword, passing_rate, timeout=1,
                              local=False):
    """
    Stress test call shell script
    :param device:the name of the tested product
    :param shell_path:The absolute path of the shell on the PC
    :param loop:the count
    :param pass_keyword:the keyword of pass
    :param fail_keyword:the keyword of fail
    :param passing_rate:passing rate:[0-100]
    :param timeout:Timeout for running shell script.Unit/day
    :param local:True-Run the shell script on the PC, False-Run the shell script on the DUT(or other)
    """
    loop = int(loop)
    timeout = float(timeout) * 86400
    passing_rate = float(passing_rate)
    device_obj = Device.getDeviceObject(device)
    if local:
        res = Device.execute_local_cmd(device_obj, shell_path, timeout=timeout)
    else:
        set_os_ip_by_dhclient(device)
        tool_path = get_tool_path()
        dut_file_path = r"/home/white_box"
        pc_user = python_server_user
        pc_password = python_server_password
        pc_ip = python_server_ip
        pc_shell_name = shell_path.split("/")[-1:][0]
        pc_shell_path = r"%s/shell" % tool_path
        delete_folder(device, dut_file_path)
        mkdir_data_path(device, dut_file_path)
        copy_files_from_pc_to_os(device, pc_user, pc_password, pc_ip, pc_shell_name, pc_shell_path, dut_file_path, 50)
        chmod_file(device, "%s/%s" % (dut_file_path, pc_shell_name))
        device_obj.sendline("%s/%s %s" % (dut_file_path, pc_shell_name, loop))
        res = device_obj.read_until_regexp("Function END", timeout=timeout)
        delete_folder(device, dut_file_path)
    pass_count = res.count(pass_keyword)
    fail_count = res.count(fail_keyword)
    if float(pass_count / loop) >= (passing_rate / 100):
        log.info('Pass: {:.2%}, Fail: {:.2%}'.format(pass_count / loop, fail_count / loop))
    else:
        log.error('Pass: {:.2%}, Fail: {:.2%}'.format(pass_count / loop, fail_count / loop))
        PRINTE("Fail! The pass rate of the stress test is less than expected:[%s%%]" % passing_rate)


def unzip_sdk_zip_and_run(device, file_path=None, target_path=None):
    """
    unzip files
    :param device: the name of the tested product
    :param file_path: zip file path
    :param target_path: target path
    """
    device_obj = Device.getDeviceObject(device)
    pc_zip_path = get_tool_path() + "/shell/sdk_zip"
    pc_zip_name = Device.execute_local_cmd(device_obj, "ls %s" % pc_zip_path, timeout=10).strip()
    if file_path:
        pc_zip_name = file_path.split("/")[-1:][0]
        pc_zip_path = "/".join(file_path.split("/")[:-1])
    dut_path = r"/home/white_box"
    if target_path:
        dut_path = target_path
    zip_path = "%s/%s" % (dut_path, pc_zip_name)
    delete_folder(device, dut_path)
    mkdir_data_path(device, dut_path)
    set_os_ip_by_dhclient(device)
    pc_user = python_server_user
    pc_password = python_server_password
    pc_ip = python_server_ip
    copy_files_from_pc_to_os(device, pc_user, pc_password, pc_ip, pc_zip_name, pc_zip_path, dut_path, 50)
    device_obj.sendline("unzip -o %s -d %s" % (zip_path, dut_path + "/"))
    chmod_file(device, "%s/%s/*" % (dut_path, pc_zip_name.replace(".zip", "")))
    device_obj.sendline("cd %s" % dut_path + "/" + pc_zip_name.replace(".zip", ""))
    device_obj.sendline("./auto_load_user.sh")
    device_obj.read_until_regexp("BCM>|IVM:0>|IVM>", timeout=30)
    device_obj.sendline("sh")
    device_obj.sendline("cd /")
    set_sel_clear(device)


def set_root_hostname(device):
    """
    Switch account to root
    """
    device_obj = Device.getDeviceObject(device)
    cmd_list = ["sudo -s", "cd /"]
    for i in range(3):
        for cmd in cmd_list:
            device_obj.sendline(cmd)
        res = openbmc_lib.execute(device_obj, "ipmitool mc info", mode=CENTOS_MODE)
        if "Device ID" in res:
            return
        else:
            time.sleep(5)
    PRINTE("Fail! Couldn't Switch to 'root' hostname, cause couldn't send 'ipmitool' cmd")


def ssh_login_os(device, ip, username, userpassword):
    DeviceMgr.usingSsh = True
    deviceObj = DeviceMgr.getDevice(device)
    deviceObj.connect(username, ip)
    deviceObj.loginDev(username, userpassword)


def read_fan_fru(device, switch_cmd, read_cmd=cmd_read_fan_fru, bmc=False, return_str=False):
    """
    Get fan  fru
    :param device: the name of the tested product
    :param switch_cmd: Command to switch fan selector
    :param read_cmd: Command to read fan fru
    :param bmc: True-BMC,False-OS
    :param return_str: if True,will return string:eg '11 22 33' else will return '0x11 0x22 0x33'
    """
    device_obj = Device.getDeviceObject(device)
    if bmc:
        switch_cmd = switch_cmd.replace("ipmitool", "ipmitest")
        read_cmd = read_cmd.replace("ipmitool", "ipmitest")
        start_time = time.time()
        while time.time() - start_time < 300:
            try:
                device_obj.switchToBmc()
                log.info("Has switch to bmc!, pls wait 40s before bmc ready!")
                set_wait(40)
                break
            except Exception:
                set_wait(10)
        else:
            PRINTE("Fail! Couldn't switch to BMC")
        openbmc_lib.execute(device_obj, switch_cmd, mode="OPENBMC")
        res = openbmc_lib.execute(device_obj, read_cmd, mode="OPENBMC")
        device_obj.trySwitchToCpu()
    else:
        openbmc_lib.execute(device_obj, switch_cmd, mode=CENTOS_MODE)
        res = openbmc_lib.execute(device_obj, read_cmd, mode=CENTOS_MODE)
    res = re.findall(r".*%s(.*)\n+real.*" % read_cmd, res, re.S)
    for i in res:
        if i == "":
            res.remove(i)
    if res:
        res_list = res[0].split("\n")
        response = ""
        for line in res_list:
            response = response + "\n" + line
        if return_str:
            return " ".join(response.strip().split(" ")[:3])
        else:
            b = ""
            for i in response.strip().split(" ")[:3]:
                b = b + "0x%s " % i
            return b.strip()
    else:
        return ""


def check_fan_air_flow(device, cmd=cmd_get_fan_air_flow, airflow=airflow_list, fen_type=fen):
    """
    Check fan air flow
    :param device: the name of the tested product
    :param cmd:get fan air flow
    :param airflow:device. List
    :param fen_type:B2F/F2B. B2F：01, F2B: 00
    """
    device_obj = Device.getDeviceObject(device)
    a = "00" if fen_type == "B2F" else "01"
    b = "01" if fen_type == "B2F" else "00"
    for i in airflow:
        command = "%s %s" % (cmd, i)
        res_ = openbmc_lib.execute(device_obj, command, mode=CENTOS_MODE)
        res = re.findall(r"/# time %s(.*)\n+real" % command, res_, re.S)
        if res:
            if a == res[0].strip():
                PRINTE("Fail! Fan type:[%s]. cmd:[%s], response not all [%s] got error response:\n%s"
                       % (fen_type, command, b, res_))
        else:
            PRINTE("Fail! Couldn't get [%s] response. res:\n%s" % (command, res_))


def get_fru_info(device, fru_id, keyword=None):
    """
    Get FRU information by 'ipmitool fru print x' e.g: ipmitool fru print 1
    :param device: the name of the tested product
    :param fru_id: FRU ID. e.g:1,3,6
    :param keyword: Board Mfg Date/Board Mfg/Board Product/Board Serial/Board Part Number/Board Extra
    :return: 'keyword' value if keyword is True
    """
    device_obj = Device.getDeviceObject(device)
    cmd = r"ipmitool fru print %s" % fru_id
    res = openbmc_lib.execute(device_obj, cmd, mode=CENTOS_MODE)
    fru_info = re.findall(r".*ipmitool fru print %s(.*)\n.*real" % fru_id, res, re.S)[0].strip()
    if not fru_info:
        PRINTE("Fail! 'fru %s' need to write info" % fru_id)
    if keyword:
        keyword_info = re.findall(r"%s\s+:\s(.*)" % keyword, fru_info)[0].strip()
        return keyword_info
    return fru_info


def set_fru_write_by_ipmi(device, write_info=ipmi_write_fru_info):
    """
    Write FRU information by 'ipmitool' command. e.g:ipmitool fru edit 1 field b 1 "TEST BOARD"
    :param device:the name of the tested product
    :param write_info:write information.dict{}
    """
    device_obj = Device.getDeviceObject(device)
    for key, value in write_info.items():
        cmd = 'ipmitool fru edit %s field b 1 "%s"' % (key, value)
        res = openbmc_lib.execute(device_obj, cmd, mode=CENTOS_MODE)


def get_fru0_mac(device):
    """
    Get mac address by 'ipmitool fru print 0'
    :param device:the name of the tested product
    :return:mac address
    """
    cmd = r"ipmitool fru print 0"
    device_obj = Device.getDeviceObject(device)
    res = openbmc_lib.execute(device_obj, cmd, mode=CENTOS_MODE)
    board_list = re.findall(r"Board Extra\s+:\s+(.*)\n", res)
    if len(board_list) < 2:
        PRINTE("Fail! [%s] Insufficient information. Response:\n%s" % (cmd, res))
    return board_list[1]


def set_fru0_mac(device, info=write_fru0_mac):
    """
    Modify the mac address in fru0 by 'ipmitool fru edit 0 field b 6 xxxxx'
    :param device:the name of the tested product
    :param info:information of mac address
    """
    cmd = r"ipmitool fru edit 0 field b 6 %s" % info
    device_obj = Device.getDeviceObject(device)
    res = openbmc_lib.execute(device_obj, cmd, mode=CENTOS_MODE)


def check_sensor_info(device):
    """
    For 9.6.1  SDR_Information_Test
    Written for Midstone100X: call the shell script that has been written,
    and check whether the sensor information matches the sensor list in the sop.

    Before use, you need to put the sensor list in a fixed format and put it in the corresponding path as 'csv'
    """
    device_obj = Device.getDeviceObject(device)
    standard_sensor_path = get_tool_path() + "/bmc_sensor/standard_sensor.csv"
    shell_name = "sdr_info_get.sh"
    shell_path = get_tool_path() + "/bmc_sensor"
    mkdir_data_path(device, dut_shell_path)
    set_os_ip_by_dhclient(device)
    pc_user = python_server_user
    pc_password = python_server_password
    pc_ip = python_server_ip
    copy_files_from_pc_to_os(device, pc_user, pc_password, pc_ip, shell_name, shell_path, dut_shell_path, 50)
    chmod_file(device, "%s/%s" % (dut_shell_path, shell_name))

    special_sensor_list = ["Fan1_Status", "Fan2_Status", "Fan3_Status", "Fan4_Status", "PSU1_Status", "PSU2_Status",
                           "PowerStatus", "SEL", "Watchdog2", "BMC_FW_Health"]

    with open(standard_sensor_path, "r", encoding="UTF-8", errors="ignore") as f:
        all_info = f.readlines()
    standard_dict = {}
    try:
        for info in all_info:
            if "sensor_name" in info:
                continue
            info = [x.strip() for x in info.split(",")]
            standard_dict[info[0]] = (info[1], info[2], info[3], info[4], info[5], info[6],
                                      info[7], info[8], info[9], info[10], info[11])
    except IndexError:
        PRINTE("[%s] the file content is incorrect! Pls check the file content" % standard_sensor_path)
    error_sensor_name = list()
    lost_keyword_sensor = list()

    reading_mask_dict = {
        "lower non-recoverable": "LNR",
        "lower critical": "LC",
        "lower non-critical": "LNC",
        "upper non-recoverable": "UNR",
        "upper critical": "UC",
        "upper non-critical": "UNC",
        "going high": "H",
        "going low": "L"
    }
    device_obj.sendline("%s/%s | tee -a %s/SDR_Information_Test.log" % (dut_shell_path, shell_name, dut_shell_path))
    all_info = device_obj.read_until_regexp("Test End", timeout=1200)
    split_info = all_info.split("*" * 135)
    for i in split_info:
        error_flag = False
        if "Sensor Name:" in i:
            a_flag, d_flag = True, True
            sensor_name = re.findall(r"Sensor Name: (.*)", i)[0].strip()
            sensor_number = re.findall(r"Sensor Number: (.*)", i)[0].strip()  # 0x01-01h
            sensor_type = re.findall(r"Sensor Type: (.*)", i)[0].strip()  # 0x01-0x1
            entity_id = re.findall(r"Entity ID: (.*)", i)[0].strip()  # 0x03-3
            entity_instance = re.findall(r"Entity Instance: (.*)", i)[0].strip()  # 0x02-0
            if sensor_name not in special_sensor_list:
                event_reading_type = re.findall(r"Event/Reading Type Code: (.*)", i)[0].strip()  # 0x01-0x01
            if sensor_name not in special_sensor_list:
                assertion_event_mask_list = re.findall(r"for threshold based sensors\):(.*)Threshold Deassertion", i,
                                                       re.S)
            else:
                assertion_event_mask_list = re.findall(r"for non-threshold based sensors\):(.*)Deassertion Event Mask",
                                                       i, re.S)
            if assertion_event_mask_list and assertion_event_mask_list != [' \n                            ']:
                assertion_event_mask_info = assertion_event_mask_list[0].replace("\n", "") \
                    .replace("                                                            : ", "").split(":")
                if sensor_name in special_sensor_list:
                    assertion_event_mask_info = [x.replace(":", "").strip() for x
                                                 in assertion_event_mask_list[0].split(" " * 63)]
                assertion_event_mask_info = [x for x in assertion_event_mask_info if x != ""]
            else:
                assertion_event_mask_info = list()
                a_flag = False
            if sensor_name not in special_sensor_list:
                deassertion_event_mask_list = re.findall(r"Deassertion Event Mask:(.*)Readable Threshold Mask", i, re.S)
            else:
                deassertion_event_mask_list = re.findall(r"Deassertion Event Mask\(for non-threshold based sensors\):"
                                                         r"(.*)Sensor Units2", i, re.S)
            if deassertion_event_mask_list and deassertion_event_mask_list != [' \n                            ']:
                deassertion_event_mask_info = deassertion_event_mask_list[0].replace("\n", "").replace(" ", "").split(
                    ":")
                if sensor_name in special_sensor_list:
                    deassertion_event_mask_info = [x.replace(":", "").strip() for x
                                                   in deassertion_event_mask_list[0].split(" " * 63)]
                deassertion_event_mask_info = [x for x in deassertion_event_mask_info if x != ""]
            else:
                deassertion_event_mask_info = list()
                d_flag = False

            if sensor_name in standard_dict.keys():
                standard_number = standard_dict[sensor_name][0]
                standard_number = standard_number.replace("h", "") if "h" in standard_number else standard_number
                if int(standard_number, 16) != int(sensor_number, 16):
                    error_flag = True
                standard_type = standard_dict[sensor_name][1]
                if standard_type:
                    if int(standard_type, 16) != int(sensor_type, 16):
                        error_flag = True
                else:
                    error_flag = True
                standard_id = standard_dict[sensor_name][2]
                if int(standard_id, 16) != int(entity_id, 16):
                    error_flag = True
                standard_instance = standard_dict[sensor_name][3]
                if int(standard_instance, 16) != int(entity_instance, 16):
                    error_flag = True
                if sensor_name not in special_sensor_list:
                    standard_reading_type = standard_dict[sensor_name][4]
                    if int(standard_reading_type, 16) != int(event_reading_type, 16):
                        error_flag = True
                if sensor_name not in special_sensor_list:
                    reading_mask_list = re.findall(r"\d+h-([a-zA-Z]+-[a-zA-Z]+)", standard_dict[sensor_name][5])
                    standard_assert_deassert = standard_dict[sensor_name][6]

                    if standard_assert_deassert == "A/D":
                        if all([a_flag, d_flag]):
                            if len(reading_mask_list) == len(assertion_event_mask_info) == len(
                                    deassertion_event_mask_info):
                                for assertion_line in assertion_event_mask_info:
                                    compare_info = re.findall(r"Assertion event for (.*) (going .*) supported",
                                                              assertion_line)
                                    if compare_info:
                                        a_d = ""
                                        for _ in compare_info[0]:
                                            a_d += reading_mask_dict[_] + "-"
                                        if a_d.rstrip("-") not in reading_mask_list:
                                            error_flag = True
                                for deassertion_line in deassertion_event_mask_info:
                                    compare_info = re.findall(r"Assertion event for (.*) (going .*) supported",
                                                              deassertion_line)
                                    if compare_info:
                                        a_d = ""
                                        for _ in compare_info[0]:
                                            a_d += reading_mask_dict[_] + "-"
                                        if a_d.rstrip("-") not in reading_mask_list:
                                            error_flag = True
                            else:
                                error_flag = True
                        else:
                            error_flag = True
                    elif standard_assert_deassert == "A":
                        if a_flag:
                            if len(reading_mask_list) == len(assertion_event_mask_info):
                                for assertion_line in assertion_event_mask_info:
                                    compare_info = re.findall(r"Assertion event for (.*) (going .*) supported",
                                                              assertion_line)
                                    if compare_info:
                                        a_d = ""
                                        for _ in compare_info[0]:
                                            a_d += reading_mask_dict[_] + "-"
                                        if a_d.rstrip("-") not in reading_mask_list:
                                            error_flag = True
                            else:
                                error_flag = True
                        else:
                            error_flag = True
                        if len(deassertion_event_mask_info) != 0:
                            error_flag = True
                    elif standard_assert_deassert == "D":
                        if d_flag:
                            if len(reading_mask_list) == len(deassertion_event_mask_info):
                                for deassertion_line in deassertion_event_mask_info:
                                    compare_info = re.findall(r"Assertion event for (.*) (going .*) supported",
                                                              deassertion_line)
                                    if compare_info:
                                        a_d = ""
                                        for _ in compare_info[0]:
                                            a_d += reading_mask_dict[_] + "-"
                                        if a_d.rstrip("-") not in reading_mask_list:
                                            error_flag = True
                            else:
                                error_flag = True
                        else:
                            error_flag = True
                        if len(deassertion_event_mask_info) != 0:
                            error_flag = True
                    else:
                        if a_flag or d_flag:
                            error_flag = True
                else:
                    standard_assert_deassert = standard_dict[sensor_name][8]
                    event_offset_triggers_list = standard_dict[sensor_name][9]
                    if event_offset_triggers_list == "":
                        PRINTE("Fail! There is an exception in the sensor standard file: %s" % sensor_name)
                    a = event_offset_triggers_list.split(")")
                    b = list()
                    number_list = list()
                    for _ in a:
                        if re.findall(r"(\d+).*", _):
                            b.append(int(re.findall(r"(\d+).*", _)[0]))
                    if standard_assert_deassert == "A/D":
                        if all([a_flag, d_flag]):
                            if len(b) == len(assertion_event_mask_info) == len(deassertion_event_mask_info):
                                for assertion_line in assertion_event_mask_info:
                                    compare_info = re.findall(r"Assertion event (\d+) can be generated by this sensor",
                                                              assertion_line)
                                    if compare_info:
                                        number_list.append(int(compare_info[0]))
                                if b.sort() != number_list.sort():
                                    error_flag = True
                                number_list.clear()
                                for deassertion_line in deassertion_event_mask_info:
                                    compare_info = re.findall(
                                        r"Deassertion event (\d+) can be generated by this sensor",
                                        deassertion_line)
                                    if compare_info:
                                        number_list.append(int(compare_info[0]))
                                if b.sort() != number_list.sort():
                                    error_flag = True
                                number_list.clear()
                            else:
                                error_flag = True
                        else:
                            error_flag = True

                    elif standard_assert_deassert == "A":

                        if a_flag:
                            print(b)
                            print(assertion_event_mask_info)
                            if len(b) == len(assertion_event_mask_info):
                                for assertion_line in assertion_event_mask_info:
                                    compare_info = re.findall(r"Assertion event (\d+) can be generated by this sensor",
                                                              assertion_line)
                                    if compare_info:
                                        number_list.append(int(compare_info[0]))
                                if b.sort() != number_list.sort():
                                    error_flag = True
                                number_list.clear()
                            else:
                                error_flag = True
                        else:
                            error_flag = True
                        if len(deassertion_event_mask_info) != 0:
                            print(deassertion_event_mask_info)
                            error_flag = True
                    elif standard_assert_deassert == "D":
                        if d_flag:
                            if len(b) == len(deassertion_event_mask_info):
                                for assertion_line in deassertion_event_mask_info:
                                    compare_info = re.findall(
                                        r"Deassertion event (\d+) can be generated by this sensor",
                                        assertion_line)
                                    if compare_info:
                                        number_list.append(int(compare_info[0]))
                                if b.sort() != number_list.sort():
                                    error_flag = True
                                number_list.clear()
                            else:
                                error_flag = True
                        else:
                            error_flag = True
                        if len(assertion_event_mask_info) != 0:
                            error_flag = True
                    else:
                        if a_flag or d_flag:
                            error_flag = True
                if error_flag:
                    error_sensor_name.append(sensor_name)
            else:
                lost_keyword_sensor.append(sensor_name)
    count = False
    if error_sensor_name:
        count = True
        log.error("Sensor info error: %s" % str(error_sensor_name))
    if lost_keyword_sensor:
        count = True
        log.error("Couldn't find sensor name in sensor list: %s" % str(lost_keyword_sensor))
    if count:
        raise RuntimeError("Fail! Function name: check_sensor_info")


def read_until(device, keyword, timeout=60):
    """
    Get the echo information on the screen
    :param device:the name of the tested product
    :param keyword: key word
    :param timeout:out time
    """
    device_obj = Device.getDeviceObject(device)
    out = device_obj.read_until_regexp(keyword, timeout)
    return out


def check_keyword_in_info(info, keyword, decide=True):
    if isinstance(keyword, list):
        for word in keyword:
            if word in info:
                if not decide:
                    PRINTE("Fail! Expected [%s] not to exist, but actually exists. Info:\n%s" % (word, info))
            else:
                if decide:
                    PRINTE("Fail! Expected [%s] exist, but actually not to exists. Info:\n%s" % (word, info))
    else:
        if keyword in info:
            if not decide:
                PRINTE("Fail! Expected [%s] not to exist, but actually exists. Info:\n%s" % (keyword, info))
        else:
            if decide:
                PRINTE("Fail! Expected [%s] exist, but actually not to exists. Info:\n%s" % (keyword, info))


def check_read_fru_data(device, cmd=cmd_get_read_fru_data):
    """
    Read the FRU data with IPMI command “Read FRU Data” to check if the data could be read correctly.
    :param device:the name of the tested product
    :param cmd: default-ipmitool raw 0x0a 0x11 0 0 0 0xff.
    """
    device_obj = Device.getDeviceObject(device)
    fru_print_info = openbmc_lib.execute(device_obj, r"ipmitool fru print 0", mode=CENTOS_MODE)
    board_extra_list = re.findall(r"Board Extra\s+: (.*)", fru_print_info)
    if not board_extra_list:
        PRINTE("Fail! Couldn't get 'Board Extra' info.Response:\n%s" % fru_print_info)
    board_extra_1, board_extra_2 = board_extra_list[1:3]
    res = openbmc_lib.execute(device_obj, cmd, mode=CENTOS_MODE)
    info = re.findall(r"cc\s(.*?)\sc2", res, re.S)
    if not info:
        PRINTE("Fail! Couldn't get 'read fru data' info.Response:\n%s" % res)
    info_list = info[0].replace("\r\n", "").split("e0")
    str_1, str_2 = "", ""
    for i in board_extra_1.strip():
        a = str(hex(ord(i))).replace("0x", " ")
        str_1 += a
    for j in board_extra_2.strip():
        b = str(hex(ord(j))).replace("0x", " ")
        str_2 += b
    if info_list[0].strip() != str_1.strip() or info_list[1].strip() != str_2.strip():
        PRINTE("Fail!\n'read fru data': %s\n'Board Extra': %s" % (fru_print_info, res))


def check_bmc_ip_normal(device, timeout=3):
    """
    Check whether the BMC IP is in the normal state, if not, then AC until
    the BMC IP is in the normal state or until it times out
    :param device:the name of the tested product
    :param timeout:unit-h
    :return:bmc ip
    """
    timeout = float(timeout) * 3600
    device_obj = Device.getDeviceObject(device)
    cmd = 'ipmitool lan print 1'
    ip_re = r"IP Address\s+:\s+(\d+\..*\d+)"
    start_time = time.time()
    for i in range(3):
        output = openbmc_lib.execute(device_obj, cmd, mode=CENTOS_MODE)
        ip_res = re.findall(ip_re, output)
        if ip_res:
            if ip_res[0] == "0.0.0.0":
                log.error("Fail! Got bmc ip:0.0.0.0")
                set_pdu_status_connect_os(device, "reboot", pdu_port, 600, 180)
                set_wait(60)
            else:
                log.success('Pass! get ip address from ipmitool: %s' % ip_res[0])
                return ip_res[0]
        else:
            set_pdu_status_connect_os(device, "reboot", pdu_port, 600, 180)
            set_wait(60)
    try_restore_bmc(device)


def set_ipv4_pxe_support_status(device, status="enable"):
    """
    Set bios config: bios->Advanced->NetWork Stack Configuration->Ipv4_pxe_support
    For Midstone100X Case: Boot_Option_Configuration_Test
    :param device:the name of the tested product
    :param status:enable/disabled
    """
    for _ in range(1, 7):
        send_key(device, "KEY_RIGHT")
        try:
            read_until(device, "CSM Configuration", timeout=5)
            break
        except Exception:
            pass
    send_key(device, "KEY_DOWN", 3)
    send_key(device, "KEY_ENTER")
    if status == "enable":
        try:
            out_put = read_until(device, "Ipv4 HTTP Support", timeout=5)
            if "Disabled" in out_put:
                send_key(device, "KEY_DOWN")
                send_key(device, "KEY_ENTER")
                send_key(device, "KEY_DOWN")
                send_key(device, "KEY_ENTER")
            send_key(device, "KEY_ESC")
        except Exception:
            send_key(device, "KEY_ENTER")
            send_key(device, "KEY_DOWN")
            send_key(device, "KEY_ENTER")
            send_key(device, "KEY_ESC")
            send_key(device, "KEY_ENTER")
            out_put = read_until(device, "Ipv4 HTTP Support", timeout=5)
            if "Disabled" in out_put:
                send_key(device, "KEY_DOWN")
                send_key(device, "KEY_ENTER")
                send_key(device, "KEY_DOWN")
                send_key(device, "KEY_ENTER")
            send_key(device, "KEY_ESC")
    else:
        try:
            read_until(device, "Ipv4 HTTP Support", timeout=5)
            send_key(device, "KEY_DOWN")
            send_key(device, "KEY_ENTER")
            send_key(device, "KEY_DOWN")
            send_key(device, "KEY_ENTER")
            send_key(device, "KEY_UP")
            send_key(device, "KEY_ENTER")
            send_key(device, "KEY_DOWN")
            send_key(device, "KEY_ENTER")
            send_key(device, "KEY_ESC")
        except Exception:
            send_key(device, "KEY_ESC")


def set_default_boot_option(device, ip, exp_str="SONiC-OS"):
    """
    Set the first startup item as expected
    For Midstone100X case: Boot_Option_Configuration_Test
    :param device: the name of the tested product
    :param ip: bmc ip
    :param exp_str: Expected string displayed by the first startup item
    """
    send_cmd(device, cmd_set_into_bios_step_always, ip)
    send_cmd(device, "ipmitool chassis bootdev bios", ip)
    send_cmd(device, "ipmitool raw 0 2 3", ip)
    read_until(device, "System Date", 300)
    set_ipv4_pxe_support_status(device, "disabled")
    send_key(device, "KEY_RIGHT", 5)
    send_key(device, "KEY_DOWN", 3)
    for _ in range(1, 20):
        send_key(device, "KEY_ENTER")
        send_key(device, "KEY_DOWN")
        send_key(device, "KEY_ENTER")
        send_key(device, "KEY_LEFT")
        send_key(device, "KEY_RIGHT")
        out_put = read_until(device, "Boot Option #2", timeout=5)
        if exp_str in out_put:
            log.info("has choose Boot option #1:%s" % exp_str)
            save_bios_and_exit(device, True)
            break


def check_hdd_startup_items(device):
    """
    After setting hdd, when the first startup item is sonic or onie, both are OK
    For Midstone100X Case:Boot_Option_Configuration_Test
    """
    device_obj = Device.getDeviceObject(device)
    sys_tem = ""
    start_time = time.time()
    info = ""
    while time.time() - start_time < 360:
        info += device_obj.readMsg()
        if "Install OS" in info and "ONIE" in info:
            log.info("After setting hdd to start, enter [ONIE]")
            sys_tem = "onie"
            break
        elif "sonic login" in info and "Loading SONiC-OS OS kernel":
            log.info("After setting hdd to start, enter [SONIC]")
            sys_tem = "sonic"
            break
    if sys_tem not in ["onie", "sonic"]:
        PRINTE("After the setting is started from hdd, it is not entered [onie] or [sonic], Start log:\n%s" % info)


def try_restore_bmc(device):
    """
    Re-burn bmc by 'socflash_x64' tool
    """
    log.error("ipmitool cannot be used, trying to re-flash BMC to solve the problem.")
    device_obj = Device.getDeviceObject(device)
    dut_file_path = r"/home/admin/BMC_Restore"
    bmc_bin_path = get_tool_path() + "/cfu/bmc/now"
    bmc_update_tool_path = get_tool_path() + "/socflash_x64"
    res = execute(device_obj, "ls %s" % bmc_bin_path, mode=CENTOS_MODE)
    res_2 = execute(device_obj, "ls %s" % bmc_update_tool_path, mode=CENTOS_MODE)
    bmc_bin_name = res.strip()
    bmc_update_tool_name = res_2.strip()
    delete_folder(device, dut_file_path)
    mkdir_data_path(device, dut_file_path)
    copy_files_from_pc_to_os(device, pc_user, pc_password, pc_ip, bmc_bin_name, bmc_bin_path, dut_file_path, 100)
    copy_files_from_pc_to_os(device, pc_user, pc_password, pc_ip, bmc_update_tool_name,
                             bmc_update_tool_path, dut_file_path, 100)
    chmod_file(device, "%s/%s" % (dut_file_path, bmc_update_tool_name))
    device_obj.sendline("cd %s" % dut_file_path)
    update_cmd = r"./socflash_x64 option=l lpcport=0x2e if=%s cs=0" % bmc_bin_name
    update_res = execute(device_obj, update_cmd, mode=CENTOS_MODE, timeout=3600)
    done_keyword = "Update Flash Chip O.K."
    set_pdu_status_connect_os(device, status="reboot", port=pdu_port)
    if done_keyword in update_res:
        log.info("Pass! Restore BMC %s successful!" % bmc_bin_name)
    else:
        PRINTE("Fail! Restore BMC %s fail!" % bmc_bin_name)

def powercycle_pdu(device):
    deviceObj =  Device.getDeviceObject(device)
    deviceObj.powerCycleDevice()

def powercycle_pdu1(device):
    deviceObj =  Device.getDeviceObject(device)
    deviceObj.powerCycleDevice1()

def upgrade_bios_image_using_CFUFLASH(device, toolname, device_type, isUpgrade=True, module='Athena_FW_BIOS_A'):
    log.debug("Entering procedure upgrade_whitebox_bios_using CFUFLASH")
    deviceObj = Device.getDeviceObject(device)
    imageObj = SwImage.getSwImage(module)
    device_version = {}
    device_version['BIOS_Version'] = imageObj.newVersion if isUpgrade else imageObj.oldVersion
    if not need_update_FW('DUT', device_type, device_version):
        log.info("Already at version " + device_version['BIOS_Version'] + ", no need update.")
        update = '0'
        log.info("-------")
        return
    upgrade_bios(device, toolname,isUpgrade,module)
    update = '1'
    return update

def upgrade_bios(device, toolname, isUpgrade, module):
    log.debug("Entering procedure upgrade_bios")
    deviceObj = Device.getDeviceObject(device)
    imageObj = SwImage.getSwImage(module)
    cmd="./ipmi_driver.sh"
    execute(device, cmd)
    cmd="rmmod ipmi_ssif"
    execute(device, cmd)
    cmd="rmmod acpi_ipmi"
    execute(device, cmd)
    err_count = 0
    timeout = 500
    if isUpgrade:
        package_file = imageObj.newImage
    else:
        package_file = imageObj.oldImage
    cmd="{} {}".format(toolname,package_file)
    log.info(cmd)
    msg="Enter your Option :"
    deviceObj.sendCmd(cmd,msg,500)
    cmd1="y"
    pr="#"
    output=deviceObj.sendCmd(cmd1,pr,1200)
    log.info(output)
    pass_message_1="Uploading Image : 100%... done"
    pass_message_2="Flashing  Firmware Image : 100%... done"
    pass_message_3="Verifying Firmware Image : 100%... done"
    pass_message_4="Beginning to Deactive flashMode...end"
    pass_message_5="Resetting the firmware........."
    match1=re.search(pass_message_1,output)
    match2=re.search(pass_message_2,output)
    match3=re.search(pass_message_3,output)
    match4=re.search(pass_message_4,output)
    match5=re.search(pass_message_5,output)
    if match1 and match2 and match3 and match4 and match5:
        log.success("BIOS upgraded successfully")
    else:
        raise RuntimeError("BIOS Upgrade Failed")

def verify_bios_version_athena(device, bios_version=None,  module='Athena_FW_BIOS_A'):
    log.debug('Entering procedure verify_bios_version with args : %s\n' % (str(locals())))
    deviceObj = Device.getDeviceObject(device)
    imageObj = SwImage.getSwImage(module)
    bios_version = imageObj.newVersion
    err_count = 0
    cmd = 'dmidecode --s bios-version'
    output = execute(device, cmd, mode=CENTOS_MODE)
    match= re.search(bios_version,output)
    if match:
        log.info("Successfully verify_BIOS_version")
    else:
        log.error("BIOS_version mismatch")
        raise RuntimeError('verify_BIOS_version failed')

def verify_bios_memory(device,mem_size,mem_speed,cfg_speed,Manufacturer):
    cmd = "dmidecode -t memory"
    output = execute(device, cmd, mode=CENTOS_MODE)
    log.cprint(output)
    match=re.search(mem_size,output)
    match1=re.search(mem_speed,output)
    match2=re.search(cfg_speed,output)
    match3=re.search(Manufacturer,output)
    if match and match1 and match2 and match3:
        log.success("Memory parameters validated successfully")
    else:
        raise RuntimeError("Expected values not present in Memory output")

def verify_UUID(device,expected_UUID_ipmitool_mc_guide_pattern,expected_UUID_ipmitool_raw_6_pattern,expected_UUID_dmidecode_pattern):
    cmd1="ipmitool mc guid"
    cmd2="ipmitool raw 6 0x37"
    cmd3="dmidecode -t 1 | grep -i UUID"
    output_ipmitool_mc_guide_cmd=execute(device, cmd1, mode=CENTOS_MODE)
    output_ipmitool_raw_6_cmd=execute(device, cmd2, mode=CENTOS_MODE)
    output_dmidecode_cmd=execute(device, cmd3, mode=CENTOS_MODE)
    match1=re.search(expected_UUID_ipmitool_mc_guide_pattern,output_ipmitool_mc_guide_cmd)
    match2=re.search(expected_UUID_ipmitool_raw_6_pattern,output_ipmitool_raw_6_cmd)
    match3=re.search(expected_UUID_dmidecode_pattern,output_dmidecode_cmd)
    if match1 and match2 and match3:
        log.success("UUID verification successful")
    else:
        log.fail("UUID verification Failed")
        raise RuntimeError("UUID verification Failed")

def verify_bios_ip_address(device, cmd, expected_result=None):
    log.debug('Entering procedure verify_ip_address with args : %s\n' % (str(locals())))
    err_count = 0
    p1 = r'IP Address\s+:\s(.+)'
    try:
        output = execute(device, cmd)
        log.cprint(output)
        match = re.search(p1, output)
        if match:
            if expected_result != None:
                IP_addr = match.group(1).strip()
                if IP_addr == expected_result:
                    log.info("Successfully verify bios ip address: %s" % (IP_addr))
                else:
                    log.error("BIOS IP address mismatch: %s, %s" % (IP_addr, expected_result))
                    err_count += 1
        else:
            log.error("Fail to parse bmc IP adrress")
            err_count += 1
        if err_count:
            raise RuntimeError('verify_IP_mac_address')
    except:
        raise RuntimeError('verify_IP_mac_address')

def verify_device_numbers(device,expected_result=None):
    cmd = "lspci -t -vv | wc -l"
    output = execute(device, cmd, mode=CENTOS_MODE)
    log.cprint(output)
    match=re.search(expected_result,output)
    if match:
        log.success("Device number value return as expected")
    else:
        raise RuntimeError("Expected values not present in output")

def verify_release_date(device,expected_result=None):
    cmd = "dmidecode -t 0 | grep \"Release Date\""
    output = execute(device, cmd, mode=CENTOS_MODE)
    log.cprint(output)
    match=re.search(expected_result,output)
    if match:
        log.success("Release date value return as expected")
    else:
        raise RuntimeError("Expected values not present in output")

def verify_bios_processor_version(device, expected_result=None):
    log.debug('Entering procedure verify_processor_version with args : %s\n' % (str(locals())))
    cmd = 'dmidecode -s processor-version'
    output = execute(device, cmd, mode=CENTOS_MODE)
    log.info(output)
    count = 0
    output1=output.splitlines()
    for line in output1:
            log.info(line)
            match=re.search(expected_result,line)
            if match:
                log.info(line)
                count=count+1
    if count == 2:
            log.info("Successfully verify_processor_version")
    else:
        log.error("Fail to parse processor_version")
        raise RuntimeError('verify_processor_version')

def upgrade_bios_image_using_AFUFLASH(device, update_cmd, toolname, device_type, isUpgrade=True, module='Athena_FW_BIOS_A'):
    log.debug("Entering procedure upgrade_whitebox_bios_using AFUFLASH")
    deviceObj = Device.getDeviceObject(device)
    imageObj = SwImage.getSwImage(module)
    device_version = {}
    device_version['BIOS_Version'] = imageObj.newVersion if isUpgrade else imageObj.oldVersion
    if not need_update_FW('DUT', device_type, device_version):
        log.info("Already at version " + device_version['BIOS_Version'] + ", no need update.")
        update = '0'
        log.info("-------")
        return
    upgrade_bios_and_me(device, update_cmd, toolname,isUpgrade,module)
    update = '1'
    return update

def upgrade_bios_and_me(device, update_cmd, toolname, isUpgrade, module):
    log.debug("Entering procedure upgrade_bios")
    deviceObj = Device.getDeviceObject(device)
    imageObj = SwImage.getSwImage(module)
    timeout = 500
    if isUpgrade:
        package_file = imageObj.newImage
    else:
        package_file = imageObj.oldImage
    cmd1 = toolname+" "+ package_file+" "+update_cmd
    log.info(cmd1)
    msg="Please select one of the options:"
    deviceObj.sendCmd(cmd1,msg,200)
    cmd1='e'
    pr="#"
    output=deviceObj.sendCmd(cmd1,pr,1200)
    log.info(output)
    error_message = "Problem opening file for reading"
    pass_message = 'Process completed'
    pass_message_1='Updating All Block .......... done'
    pass_message_2='Erasing All Block ........... done'
    pass_message_3='Verifying All Block ......... done'
    match=re.search(pass_message,output)
    match1=re.search(pass_message_1,output)
    match2=re.search(pass_message_2,output)
    match3=re.search(pass_message_3,output)
    match4=re.search(error_message,output)
    if match and match1 and match2 and match3:
        log.success("BIOS upgraded successfully")
    else:
        raise RuntimeError("BIOS Upgrade Failed")
    if match4:
        raise RuntimeError("Image cannot be accessed")

def get_cpu_microcode(device):
   cmd="dmesg | grep -i  microcode"
   output=execute(device, cmd, mode=CENTOS_MODE)
   pattern=".*revision=(\S+).*"
   match=re.search(pattern,output)
   if match:
         microcode_revision=match.group(1)
         log.debug("microcode_revision is : " )
         log.debug(microcode_revision)
         return microcode_revision
   else:
         log.fail("microcode_revision not available")
         raise RuntimeError("microcode_revision not available")

def GetBIOSImageName(key,module):
    log.debug("Entering GetBIOSImageName with args : %s" %(str(locals())))
    imageObj = SwImage.getSwImage(module)
    return  imageObj.localImageDir + '/' + imageObj.newImage[key]

def upgrade_bios_FW_with_save_config(device,module,key='BIN'):
    log.debug("Entering upgrade_bios_FW_with_save_config with args : %s" %(str(locals())))
    deviceObj = Device.getDeviceObject(device)
    imageObj = SwImage.getSwImage(module)
    localdir = imageObj.localImageDir
    deviceObj.sendline('cd %s' %(localdir))
    toolname='./CFUFLASH -pc -cd -d 2 -fb'

    cmd="./ipmi_driver.sh"
    execute(device, cmd)
    cmd="rmmod ipmi_ssif"
    execute(device, cmd)
    cmd="rmmod acpi_ipmi"
    execute(device, cmd)
    err_count = 0
    timeout = 500
    package_file = imageObj.newImage[key]
    cmd="{} {}".format(toolname,package_file)
    log.info(cmd)
    msg="BIOS Config preserved:1"
    deviceObj.sendCmd(cmd,msg,500)

def RemoveAthenaBIOSFwImage(device,module="Athena_FW"):
    log.debug("Entering RemoveAthenaBIOSFwImage with args : %s" %(str(locals())))
    deviceObj = Device.getDeviceObject(device)
    imageObj = SwImage.getSwImage(module)
    destinationDir = imageObj.localImageDir
    imgList = list(imageObj.newImage.values())
    for image in imgList:
       deviceObj.sendCmd("rm %s/%s" %(destinationDir,image))
     

KEY_DATA = {
    'KEY_DEL': '\x1b[3~',
    'KEY_F1': '\x1bOP',
    'KEY_F2': '\x1bOQ',
    'KEY_F3': '\x1bOR',
    'KEY_F4': '\x1bOS',
    'KEY_F5': '\x1b[15~',
    'KEY_F7': '\x1b[18~',
    'KEY_F9': '\x1b[20~',
    'KEY_F10': '\x1b[21~',
    'KEY_ESC': '\x1b',
    'KEY_ENTER': '\r',
    'KEY_PLUS': '+',
    'KEY_MINUS': '-',
    'KEY_UP': '\x1b[A',
    'KEY_DOWN': '\x1b[B',
    'KEY_RIGHT': '\x1b[C',
    'KEY_LEFT': '\x1b[D',
    'KEY_BKSP': '\x08',
    'KEY_DOT': '\x2E',
    #'KEY_7': '7',
    'KEY_2000': '2000',
    'KEY_1': '1',
    'KEY_2': '2',
    'KEY_3': '3',
    'KEY_4': '4',
    'KEY_5': '5',
    'KEY_6': '6',
    'KEY_7': '7',
    'KEY_8': '8',
    'KEY_9': '9',
    'KEY_0': '0',
    'KEY_s': 's',
    'KEY_y': 'y',
    'KEY_x': 'x'
}


def send_key(device, key_name, times=1, delay=2):
    log.debug('Entering send_key with args : %s' %(str(locals())))
    deviceObj = Device.getDeviceObject(device)
    for i in range(times):
        log.debug("Sending %s #%d"%(key_name, i+1))
        # deviceObj.flush()
        deviceObj.sendline(KEY_DATA[key_name], CR=False)
        time.sleep(delay)


def escape_ansi(output):
    ansi_escape = r'\x1b[\[][0-?]*[ -/]*[@-~]'
    return re.sub(ansi_escape, ' ', output)