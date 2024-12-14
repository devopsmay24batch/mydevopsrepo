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
import re
from inspect import getframeinfo, stack
import os.path
import time
import yaml
import Logger as log
from SEASTONECommonLib import powercycle_pdu1
import CommonLib
import random
import Const
import bios_menu_lib
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
import CRobot
from ONL_variable import *
from BMC_variable import *
from datetime import datetime, timedelta
from dataStructure import nestedDict, parser
from errorsModule import noSuchClass, testFailed
import CommonKeywords
from SwImage import SwImage
from Server import Server
from pexpect import pxssh
from functools import partial
import sys
import getpass
import WhiteboxLibAdapter
import whitebox_lib
from crobot.Decorator import logThis
import pexpect
import multiprocessing
from TelnetDevice import TelnetDevice
import pexpect
from crobot.PowerCycler import PowerCycler
import SEASTONECommonLib
from  SEASTONECommonLib import powercycle_device
try:
    import parser_openbmc_lib as parserOpenbmc
    import DeviceMgr
    from Device import Device

except Exception as err:
    log.cprint(str(err))

deviceM = DeviceMgr.getDevice()
workDir = CRobot.getWorkDir()
tmpDir = '/tmp'
sys.path.append(os.path.join(workDir, 'common', 'commonlib'))
#sys.path.append(os.path.join(workDir, 'platform/edk2'))
sys.path.append(os.path.join(workDir, 'platform', 'seastone'))
sys.path.append(os.path.join(workDir, 'platform', 'seastone','diag'))
sys.path.append(os.path.join(workDir, 'platform', 'seastone','onl'))

run_command = partial(CommonLib.run_command, deviceObj=deviceM, prompt=deviceM.promptDiagOS)
time.sleep(10)

import Logger as log


def dump_device_data(device):
    device_obj = Device.getDeviceObject(device)
    device_obj.flush()
    cmd = 'onlpdump -ery > /root/temp.yml'
    Device.execCmd(device_obj, cmd)
    try:
        CommonLib.get_file_by_scp(device_obj.managementIP, device_obj.rootUserName,device_obj.rootPassword , '/root', 'temp.yml',tmpDir )
        with open('{}/temp.yml'.format(tmpDir), 'r') as r:
            input1 = yaml.safe_load(r)
            log.info(input1)
        os.remove('{}/temp.yml'.format(tmpDir))
        Device.execCmd(device_obj, 'rm /root/temp.yml')
        return input1
    except AssertionError:
        log.fail(f"Output couldnt dump properly")
        raise


def compare_device_data(exp_info, parsed_info):
    #Always Expected info first and parsed info second as parameters
    log.debug('Entering procedure compare_device_data with args : %s\n' %(str(locals())))
    flag = False
    for i in exp_info:
        if type(exp_info.get(i)) is dict:
            compare_device_data(exp_info.get(i),parsed_info.get(i))
        else:
            if str(exp_info.get(i)) == str(parsed_info.get(i)):
                log.success("Expected %s:%s and actual %s:%s are Equal" %(i,exp_info.get(i),i,parsed_info.get(i)))
            else:
                log.fail("Expected %s:%s and actual %s:%s are Not Equal" %(i,exp_info.get(i),i,parsed_info.get(i)))
                flag = True
                break
    if flag:
        raise testFailed

def verify_data_json_format(device):
    input1 = dump_device_data(device)
    if type(input1) is dict:
        log.success("Output is in json format")
    else:
        log.fail(f"Output is not in json format")
        raise

@logThis
def enter_into_bios_setup_now(device):
    log.debug('Entering procedure verify_bios_default_password with args : %s\n' %(str(locals())))
    bios_copy='EVALUATION COPY'
    deviceObj = Device.getDeviceObject(device)

    deviceObj.getPrompt("DIAGOS")
    deviceObj.sendline("")
    deviceObj.sendCmd("reboot")
    out=deviceObj.read_until_regexp('to enter setup',timeout=140)
    if not bios_copy in out:
        log.success('No EVALUATION COPY STRING PRESENT')
    else:
        raise RuntimeError('EVALUATION COPY STRING PRESENT')

    counter = 5
    while counter >= 0:
         bios_menu_lib.send_key(device, "KEY_DEL")
         counter -= 1
         time.sleep(1)


@logThis
def check_bios_basic(device):
    pat1='ESC: Exit'
    deviceObj = Device.getDeviceObject(device)
    out=deviceObj.read_until_regexp(pat1,timeout=10)
    print('The value of out',out)
@logThis
def exit_bios_now(device):
    deviceObj = Device.getDeviceObject(device)
    time.sleep(3)
    bios_menu_lib.send_key(device, "KEY_ESC")
    time.sleep(5)
    deviceObj.sendCmd('\r')
    #out=deviceObj.read_until_regexp('Shell>',timeout=50)
    #deviceObj.sendline('exit')
    time.sleep(10)
    deviceObj.sendline('\r')
    deviceObj.read_until_regexp('localhost login',timeout=80)
    deviceObj.loginToDiagOS()

def get_product_name(device):
    log.debug("Entering get_product_name details args : %s" %(str(locals())))
    cmd = f"onlpdump -s"
    device_obj = Device.getDeviceObject(device)
    output = Device.executeCmd(device_obj, cmd)
    log.info(output)
    product_name =re.search(r"Product Name:\s+(.*)",output,re.I|re.M)[1]
    return product_name.strip()

def get_bios_version(device):
    log.debug("Entering get_bios_version details args : %s" %(str(locals())))
    cmd = f"dmidecode -t bios"
    device_obj = Device.getDeviceObject(device)
    output = Device.executeCmd(device_obj, cmd)
    log.info(output)
    log.debug(seastone_diag_version)
    bios_version=re.search(r"Version:\s+(.*)",output,re.I|re.M)[1]
    return bios_version
    

def get_onie_version(device):
    log.debug("Entering get_onie_version details args : %s" %(str(locals())))
    cmd = f"onie-sysinfo"
    device_obj = Device.getDeviceObject(device)
    output = Device.executeCmd(device_obj, cmd)
    log.info(output)
    onie_version=re.search(r"(x86.*)",output,re.I|re.M)[1]
    return onie_version


def get_bmc_version_ipmitool(device):
    log.debug("Entering get_bmc_version_ipmitool details args : %s" %(str(locals())))
    cmd_FM_Version = f"ipmitool mc info"
    device_obj = Device.getDeviceObject(device)
    output = Device.executeCmd(device_obj, cmd_FM_Version)
    log.info(output)
    CurrentFWversion=re.search(r"Firmware Revision\s+:\s(\d+.\d+)",output,re.I|re.M)[1]
    return CurrentFWversion

def get_bmc_ip_address_from_ipmitool(device, eth_type='dedicated', ipv6=False):
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
    #output = openbmc_lib.execute(device_obj, cmd, mode=CENTOS_MODE)
    #output = Device.execute_local_cmd(device_obj, cmd)
    output = Device.executeCmd(device_obj, cmd)
    log.info("Output : %s" %output)
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


def get_fpga_version(device):
    log.debug("Entering get_fpga_version details args : %s" %(str(locals())))
    device_obj = Device.getDeviceObject(device)
    whitebox_lib.change_directory(device,"/home/cel_diag/seastone2v2/bin")
    cmd = f"./cel-cpld-test -r -d 4 -R 1 | sed -n 2p"
    output = Device.executeCmd(device_obj, cmd)
    log.info(output)
    fpga_version=re.search(r"FPGA Version:\s+([\d\.]+)",output,re.I|re.M)[1]
    return fpga_version

def get_baseboard_cpld_version(device):
    log.debug("Entering get_baseboard_cpld_version details args : %s" %(str(locals())))
    device_obj = Device.getDeviceObject(device)
    whitebox_lib.change_directory(device,"/home/cel_diag/seastone2v2/bin")
    cmd = f"./cel-cpld-test -r -d 1 -R 1 | sed -n 2p"
    output = Device.executeCmd(device_obj, cmd)
    log.info(output)
    baseboard_cpld_version=re.search(r"Baseboard_CPLD Version:\s+([\d\.]+)",output,re.I|re.M)[1]
    return baseboard_cpld_version

def get_come_cpld_version(device):
    log.debug("Entering get_come_cpld_version details args : %s" %(str(locals())))
    device_obj = Device.getDeviceObject(device)
    whitebox_lib.change_directory(device,"/home/cel_diag/seastone2v2/bin")
    cmd = f"./cel-cpld-test -r -d 5 -R 1 | sed -n 2p"
    output = Device.executeCmd(device_obj, cmd)
    log.info(output)
    come_cpld_version=re.search(r"COME_CPLD Version:\s+([\d\.]+)",output,re.I|re.M)[1]
    return come_cpld_version

def get_switch_cpld_version(device):
    log.debug("Entering get_switch_cpld_version details args : %s" %(str(locals())))
    device_obj = Device.getDeviceObject(device)
    whitebox_lib.change_directory(device,"/home/cel_diag/seastone2v2/bin")
    cmd = f"./cel-cpld-test -r -d 2 -R 1 | sed -n 2p"
    output = Device.executeCmd(device_obj, cmd)
    log.info(output)
    switch_cpld_version=re.search(r"MISC_CPLD1 Version:\s+([\d\.]+)",output,re.I|re.M)[1]
    return switch_cpld_version

def verify_onl_booting_check_log(device):
    log.debug("Entering verify_onl_booting_check with args : %s" %(str(locals())))
    device_obj = Device.getDeviceObject(device)
    cmd = f"dmesg | grep -i fail"
    output = Device.executeCmd(device_obj, cmd)
    log.info("output is %s" %output)
    try:
        fail_log=re.search(r"(.*fail.*)",output,re.I|re.M)[1]
    except:
        log.success("Pass, No failures seen")
    else:
        log.fail(fail_log)
        raise testFailed('verify_onl_booting_check_log')
    cmd = f"dmesg | grep -i error"
    output = Device.executeCmd(device_obj, cmd)
    log.info("output is %s" %output)
    try:
        error_log=re.search(r"(.*error.*)",output,re.I|re.M)[1]
    except:
        log.success("Pass, No errors seen")
    else:
        log.fail(error_log)
        raise testFailed('verify_onl_booting_check_log')

def verify_onl_login(device):
    device_obj = Device.getDeviceObject(device)
    device_obj.sendCmd('exit')
    time.sleep(5)
    device_obj.sendline('\r')
    device_obj.read_until_regexp('localhost login',timeout=80)
    device_obj.loginToDiagOS()

def get_onl_version(device):
    log.debug("Entering get_onl_version details args : %s" %(str(locals())))
    device_obj = Device.getDeviceObject(device)
    cmd = f"cat /etc/issue"
    output = Device.executeCmd(device_obj, cmd)
    log.info(output)
    onl_version=re.search(r"Open Network Linux OS (\S+)\,\s+\S+",output,re.I|re.M)[1]
    return onl_version

def get_onl_sysinfo(device):
    log.debug("Entering get_onl_sysinfo details args : %s" %(str(locals())))
    device_obj = Device.getDeviceObject(device)
    cmd = f"uname -a"
    output = Device.executeCmd(device_obj, cmd)
    log.info(output)
    onl_sysinfo=re.search(r"(Linux localhost 5.4.40-OpenNetworkLinux).*x86_64 GNU/Linux",output,re.I|re.M)[1]
    return onl_sysinfo

def get_system_info_detail(device):
    log.debug("Entering get_system_info details args : %s" %(str(locals())))
    device_obj = Device.getDeviceObject(device)
    cmd = f"onlpdump -s"
    output = Device.executeCmd(device_obj, cmd)
    log.info(output)
    system_info = {}
    p1 = 'Product Name: (\S+)'
    p2 = 'Part Number: (\S+)'
    p3 = 'Serial Number: (\S+)'
    p4 = 'MAC: (\S+)'
    p5 = 'MAC Range: (\S+)'
    p6 = 'Manufacturer: (\S+)'
    p7 = 'Manufacture Date: (\S+)'
    p8 = 'Vendor: (\S+)'
    p9 = 'Platform Name: (\S+)'
    p10 = 'Device Version: (\S+)'
    p11 = 'Label Revision: (\S+)'
    p12 = 'Country Code: (\S+)'
    p13 = 'Diag Version: (\S+)'
    p14 = 'Service Tag: (\S+)'
    p15 = 'ONIE Version: (\S+)'
    for line in output.splitlines():
        match = re.search(p1,line)
        if match:
            system_info['Product_Name'] = match.group(1)
        match = re.search(p2, line)
        if match:
            system_info['Part_Number'] = match.group(1)
        match = re.search(p3, line)
        if match:
            system_info['Serial_Number'] = match.group(1)
        match = re.search(p4, line)
        if match:
            system_info['MAC'] = match.group(1)
        match = re.search(p5, line)
        if match:
            system_info['MAC_Range'] = match.group(1)
        match = re.search(p6, line)
        if match:
            system_info['Manufacturer'] = match.group(1)
        match = re.search(p7, line)
        if match:
            system_info['Manufacturer_Date'] = match.group(1)
        match = re.search(p8, line)
        if match:
            system_info['Vendor'] = match.group(1)
        match = re.search(p9, line)
        if match:
            system_info['Platform_Name'] = match.group(1)
        match = re.search(p10, line)
        if match:
            system_info['Device_Version'] = match.group(1)
        match = re.search(p11, line)
        if match:
            system_info['Label_Revision'] = match.group(1)
        match = re.search(p12, line)
        if match:
            system_info['Country_Code'] = match.group(1)
        match = re.search(p13, line)
        if match:
            system_info['Diag_Version'] = match.group(1)
        match = re.search(p14, line)
        if match:
            system_info['Service_Tag'] = match.group(1)
        match = re.search(p15, line)
        if match:
            system_info['ONIE_Version'] = match.group(1)
    log.info(system_info)
    return system_info


@logThis
def burningTlvData_SV2(device,tlv_dict):
    devicename = os.environ.get("deviceName", "")
    #disable_fpga_cmd = 'echo 0 > /sys/bus/i2c/devices/15-0060/i2cfpga_eeprom_write_protect'
    #disable_wp_cmd = 'echo 0 > /sys/bus/i2c/devices/15-0060/system_eeprom_wp'
    #device.sendMsg(disable_wp_cmd+'\r\n')
    #time.sleep(3)
    #device.sendMsg(disable_fpga_cmd+'\r\n')
    #time.sleep(3)
    #device.sendMsg("cd /root/diag/" + "\r\n")
    log.debug("Entering burning Tlv Data args : %s" %(str(locals())))
    device_obj = Device.getDeviceObject(device)
    whitebox_lib.change_directory(device,"/home/cel_diag/seastone2v2/bin")
    for tlv_name, tlv_data in tlv_dict.items():
        if tlv_data[0] == "0x25":
            cmd = './cel-eeprom-test -w -t tlv -d 1 -A {} -D "{}"'.format(tlv_name, tlv_data)
        else:

            cmd = "./cel-eeprom-test -w -t tlv -d 1 -A {} -D {}".format(tlv_name, tlv_data)
            CommonLib.escapeString(tlv_data)
        check_pattern = "{}.*?{}".format(tlv_name, tlv_data)
        output = Device.executeCmd(device_obj, cmd)
        time.sleep(3)
        log.info(output)
        if not re.search(check_pattern, output):
            raise Exception("Burning EEPROM failed: {}".format(tlv_name))


def test_CheckPSUStatus(device, PlatformEnv):
    TOTAL_PSU = int(PlatformEnv["PSU"]["Total"])
    all_psu_status = []
    condition = True

    for i in range(1, TOTAL_PSU+1):
        status = Get_PSU_Value(device, i, 'Status')
        all_psu_status.append(status)
        condition = condition and status == 'Running'

    try:
        assert condition
        log.info("All PSU has required 'Running' status.")
    except AssertionError:
        log.fail("One of the PSU not having required 'Running' status.\nAll status are %s" %(str(all_psu_status)))
        raise


def test_CheckPSUState(device, PlatformEnv):
    TOTAL_PSU = int(PlatformEnv["PSU"]["Total"])
    all_psu_state = []
    condition = True

    for i in range(1, TOTAL_PSU+1):
        state = Get_PSU_Value(device, i, 'State')
        all_psu_state.append(state)
        condition = condition and state == 'Present'

    try:
        assert condition
        log.info("All PSU has required 'Present' state.")
    except AssertionError:
        log.fail("One of the PSU not having required 'Present' state.\nAll state are %s" %str(all_psu_state))
        raise

def GetPSUInfo(device, Index, key):
    device_obj = Device.getDeviceObject(device)

    if Index == 1:
        cmd = '/lib/platform-config/current/onl/bin/onlpdump | grep -a \'psu @ 1 = {\' -A11 | grep -v \'psu @ 1 = {\''
    else:
        cmd = '/lib/platform-config/current/onl/bin/onlpdump | grep -a \'psu @ 2 = {\' -A11 | grep -v \'psu @ 2 = {\''

    output = Device.executeCmd(device_obj, cmd)
    output = re.sub('real\s+.*','',output)
    output = re.sub('user\s+.*', '', output)
    output = re.sub('sys\s+.*', '', output)
    log.info(output)
    temp = output.strip().split('\n')

    PSU = dict()

    for val in temp:
        PSU[val.strip().split(':')[0]] = str(val.strip().split(':')[1].strip())

    if key in PSU:
        return PSU[key]
    else:
        log.fail("Specified key is not present in the dictionary file : %s", key)
        return 0

def test_CheckPSUVoltage(device, PlatformEnv):
    TOTAL_PSU = int(PlatformEnv["PSU"]["Total"])
    all_psu_voltages = {}
    condition = True

    for i in range(1, TOTAL_PSU+1):
        voltage = int(GetPSUInfo(device, i, 'Vin'))
        current = int(GetPSUInfo(device, i, 'Iin'))
        power = int(GetPSUInfo(device, i, 'Pin'))
        all_psu_voltages["PSU-" + str(i)] = {"Voltage": voltage, "Current": current, "Power": power}
        condition = condition and voltage != 0 and current != 0 and power != 0

    try:
        assert condition
        log.info("All PSU voltages are as expected and test passed.\nVoltages are\n %s" %str(all_psu_voltages))
    except:
        log.fail("Error in PSU voltages. Some of them are 0.\nVoltages are\n %s" %str(all_psu_voltages))
        raise

def test_CheckPSUTypeTest(device, PlatformEnv):
    TOTAL_PSU = int(PlatformEnv["PSU"]["Total"])
    all_psu_types = []
    condition = True

    for i in range(1, TOTAL_PSU+1):
        psu_type = Get_PSU_Value(device, i, 'Type')
        all_psu_types.append(psu_type)
        condition = condition and psu_type in 'AC/DC' 

    try:
        assert condition
        log.info("All PSU types are as required.\nTypes: %s" %str(all_psu_types))
    except:
        log.fail("PSU Type not as required (AC/DC).\nFound: %s\n. " %str(all_psu_types))
        raise


def Get_PSU_Value(device, PSU, key):
    #DUT = Login(IPAddress, 'root', 'onl')

    #data = DUT.SendACommand('/lib/platform-config/current/onl/bin/onlpdump -ery')
    log.debug("Entering  GET PSU Value with args : %s" %(str(locals())))
    device_obj = Device.getDeviceObject(device)
    input1 = dump_device_data(device)
    PSU_Dict = input1["PSUs"]
    PSUIndex = PSU - 1

    if PSUIndex <= len(PSU_Dict):
        if key in PSU_Dict[PSUIndex]:
            log.info("PSU module %d and corresponding key and value is: %s - %s" %( PSU, key, PSU_Dict[PSUIndex][key]))
            return PSU_Dict[PSUIndex][key]
        else:
            log.fail("Specified key is not present in the dictionary file: %s" %key)
            return 0
    else:
        log.error("Specified PSU module Index value is not found: %d" %PSU)
        return -1

##########################################################################################################################
def test_FanNoAndDescTest(device, PlatformEnv):

    TOTAL_FANS = len(PlatformEnv["FAN"]["FAN_Index"])

    required_fan_names = [ f"Fan {i}" for i in PlatformEnv["FAN"]["FAN_Index"]]
    required_fan_desc = [ f"Chassis Fan {i}" for i in PlatformEnv["FAN"]["FAN_Index"]]

    fan_names = []
    fan_descs = []

    for i in PlatformEnv["FAN"]["FAN_Index"]:
        name = Get_Fan_Value(device, i, 'Name')
        fan_names.append(name)
        desc = Get_Fan_Value(device, i, 'Description')
        fan_descs.append(desc)

    if len(PlatformEnv["PSU"]["PSU-1"]["FAN_Index"]) > 0:

        for i in PlatformEnv["PSU"]["PSU-1"]["FAN_Index"]:
            required_fan_names.append(f"Fan {i}")

        for i in range(len(PlatformEnv["PSU"]["PSU-1"]["FAN_Index"])):
            required_fan_desc.append(f"PSU Fan {i+1}")


        for i in range(len(PlatformEnv["PSU"]["PSU-1"]["FAN_Index"])):
            name = Get_PSU_FAN_Value(device, 1, i, 'Name')
            fan_names.append(name)
            desc = Get_PSU_FAN_Value(device, 1, i, 'Description')
            fan_descs.append(desc)

    if len(PlatformEnv["PSU"]["PSU-2"]["FAN_Index"]) > 0:

        for i in PlatformEnv["PSU"]["PSU-2"]["FAN_Index"]:
            required_fan_names.append(f"Fan {i}")

        for i in range(len(PlatformEnv["PSU"]["PSU-2"]["FAN_Index"])):
            required_fan_desc.append(f"PSU Fan {i+2}")

        for i in range(len(PlatformEnv["PSU"]["PSU-2"]["FAN_Index"])):
            name = Get_PSU_FAN_Value(device, 2, i, 'Name')
            fan_names.append(name)
            desc = Get_PSU_FAN_Value(device, 2, i, 'Description')
            fan_descs.append(desc)


    condition1 = required_fan_names == fan_names
    condition2 = required_fan_desc == fan_descs

    try:
        assert condition1 and condition2
        log.info("Fan No. and Descriptions as required.\n %s \n %s" %(str(fan_names), str(fan_descs)))
    except AssertionError:
        log.fail("Fan No. and Descriptions NOT as required.\n %s \n %s" %(str(required_fan_names), str(required_fan_desc)))
        log.fail("Fan No. and Descriptions NOT as required.\n %s \n %s" %(str(fan_names), str(fan_descs)))
        raise

def Get_Fan_Value(device, FanIndex, key):
    log.debug("Entering  GET FAN Value with args : %s" %(str(locals())))
    input1 = dump_device_data(device)
    Fan_Dict = input1["Fans"]
    Index = FanIndex
    FanIndex = FanIndex - 1

    if FanIndex <= len(Fan_Dict):
        if key in Fan_Dict[FanIndex]:
            log.info("Fan-Module %d key and corresponding value is: %s - %s : " %(Index, key, Fan_Dict[FanIndex][key]))
            return Fan_Dict[FanIndex][key]
        else:
            log.fail("Specified key is not present in the dictionary file: %s" %key)
            return 0
    else:
        log.fail("Specified FAN module Index value is not found: %d" %FanIndex)
        return -1


def test_FanStateTest(device, PlatformEnv):
    TOTAL_FANS = len(PlatformEnv["FAN"]["FAN_Index"])
    all_fan_state = {}
    condition = True

    for i in range(TOTAL_FANS):
        state = Get_Fan_Value(device, i+1, 'State')
        all_fan_state["Fan-" + str(i+1)] = state
        condition  = condition and state == "Present"

    if len(PlatformEnv["PSU"]["PSU-1"]["FAN_Index"]) > 0:
        for i in range(len(PlatformEnv["PSU"]["PSU-1"]["FAN_Index"])):
            state = Get_PSU_FAN_Value(device, 1, i, 'State')
            all_fan_state["PSU Fan-" + str(i+1)] = state
            condition  = condition and state == "Present"

    if len(PlatformEnv["PSU"]["PSU-2"]["FAN_Index"]) > 0:
        for i in range(len(PlatformEnv["PSU"]["PSU-2"]["FAN_Index"])):
            state = Get_PSU_FAN_Value(device, 2, i, 'State')
            all_fan_state["PSU Fan-" + str(i+2)] = state
            condition  = condition and state == "Present"
    try:
        assert condition
        log.info("All fan state as required ('Present').\n%s" %str(all_fan_state))
    except AssertionError:
        log.fail("Some of the fan state NOT as required ('Present').\n%s" %str(all_fan_state))
        raise


def Get_PSU_FAN_Value(device, PSU, FAN, key):
    log.debug("Entering  GET PSU FAN Value with args : %s" %(str(locals())))

    input1 = dump_device_data(device)
    PSU_Dict = input1["PSUs"]

    PSUIndex = PSU - 1
    FANIndex = FAN - 1

    if PSU_Dict[PSUIndex]["Fans"] != None:
        if PSUIndex <= len(PSU_Dict):
            if FANIndex <= len(PSU_Dict[PSUIndex]["Fans"]):
                if key in PSU_Dict[PSUIndex]["Fans"][FANIndex]:
                    log.info("PSU %d's Fan module %d key and value is: %s - %s" %(PSU, FAN, key, PSU_Dict[PSUIndex]["Fans"][FANIndex][key]))
                    return PSU_Dict[PSUIndex]["Fans"][FANIndex][key]
                else:
                    log.fail("Specified key is not present in the dictionary file: %s"%key)
                    return 0
        else:
            log.fail("Specified FAN module Index value is not found: %d" %FAN)
            return -1
    else:
        log.info("No Fan modules found in the PSU")
        return -2

def test_FanRPMAndSpeedTest(device):
    all_fans_rpms = getAllFansRPM(device)
    condition = True
    for rpm in all_fans_rpms.values():
        condition = condition and int(rpm) > 1200 and int(rpm) < 16000

    try:
        assert condition
        log.info("All fans RPM as required.\n %s" %str(all_fans_rpms))
    except AssertionError:
        log.fail("Error in FAN speed RPMs one of them not in range.\n All fans RPMs given below.\n %s" %str(all_fans_rpms))
        raise

def getAllFansRPM(IPAddress):
    log.debug("Entering  GET PSU FAN Value with args : %s" %(str(locals())))
    device_obj = Device.getDeviceObject(device)
    cmd = 'onlpdump | grep -a "RPM:"'
    output = Device.executeCmd(device_obj, cmd)

    retval = output.split("\n")

    fan_rpms = {}
    rpm_list = []

    for i in retval:
        rpm_list.append(i.strip())

    while ("" in rpm_list):
        rpm_list.remove("")

    index = 1
    for item in rpm_list:
        val = item.split(":")[1].strip()
        fan_rpms["Fan-" + str(index)] = val
        index = index + 1
    return fan_rpms

def test_CheckSensorDescription(device, PlatformEnv):

    required_thermal_desc = PlatformEnv["Thermal"]["Thermal_Description"]

    thermals = PlatformEnv["Thermal"]["Thermal_Index"]
    total_psu = int(PlatformEnv["PSU"]["Total"])
    psu_thermals = []

    for i in range(1, total_psu+1):
        psu_thermals += PlatformEnv["PSU"]["PSU-" + str(i)]["Thermal_Index"]

    #TOTAL_THERMAL_SENSORS = thermals + psu_thermals

    thermal_descs = []

    # All sensors description are added to the list and compared.
    for i in thermals:
        desc = Get_Thermal_Value(device, i, 'Description')
        thermal_descs.append(desc)

    for j in range(1, total_psu+1):
        if len(PlatformEnv["PSU"]["PSU-" + str(j)]["Thermal_Index"]) > 1:
            for k in range(1, len(PlatformEnv["PSU"]["PSU-" + str(j)]["Thermal_Index"]) + 1):
                desc = Get_PSU_Thermal_Value(device, j, k, 'Description')
                thermal_descs.append(desc)

    try:
        log.info("All sensor description as required.\n%s" %str(thermal_descs))
        assert thermal_descs == required_thermal_desc
    except AssertionError:
        log.fail(f"Error in thermal description. Mismatch found.\n Required\n{required_thermal_desc}\nFound\n{thermal_descs}")
        raise

def test_SensorStatusTest(device, PlatformEnv):
    thermals = PlatformEnv["Thermal"]["Thermal_Index"]
    total_psu = int(PlatformEnv["PSU"]["Total"])
    psu_thermals = []

    for i in range(1, total_psu+1):
        psu_thermals += PlatformEnv["PSU"]["PSU-" + str(i)]["Thermal_Index"]

    thermal_status = []

    for i in thermals:
        status = Get_Thermal_Value(device, i, 'Status')
        if status == 0:
            thermal_status.append("Missing")
        else:
            thermal_status.append(status)

    for j in range(1, total_psu+1):
        if len(PlatformEnv["PSU"]["PSU-" + str(j)]["Thermal_Index"]) > 1:
            for k in range(1, len(PlatformEnv["PSU"]["PSU-" + str(j)]["Thermal_Index"]) + 1):
                status = Get_PSU_Thermal_Value(device, j, k, 'Status')
                if status == 0:
                    thermal_status.append("Missing")
                else:
                    thermal_status.append(status)

    Missing_Sensors = thermal_status.count("Missing")

    Working_Sensors = thermal_status.count("Functional")

    TOTAL_THERMAL_SENSORS = len(thermals) + len(psu_thermals)

    condition = Working_Sensors == (TOTAL_THERMAL_SENSORS - Missing_Sensors)

    try:
        assert condition
        log.info("All thermal status as required ('Functional').\n%s" %str(thermal_status))
        log.debug("Few sensors are missing. Check hardware specs for more information")
    except AssertionError:
        log.error(f"Error in thermal status. Mismatch found. All should be 'Functional'.\nBut found\n {thermal_status}")

def Get_PSU_Thermal_Value(device, PSU, Thermal, key):
    log.debug("Entering  GET PSU Thermal Value with args : %s" % (str(locals())))

    input1 = dump_device_data(device)
    PSU_Dict = input1["PSUs"]
    PSUIndex = PSU - 1
    ThermalIndex = Thermal - 1
    if PSU_Dict[PSUIndex]["Thermals"] != None:
        if PSUIndex <= len(PSU_Dict):
            if ThermalIndex <= len(PSU_Dict[PSUIndex]["Fans"]):
                if key in PSU_Dict[PSUIndex]["Thermals"][ThermalIndex]:
                    log.info("PSU %d's Thermal module %d key and value is: %s - %s" %(PSU, Thermal, key, PSU_Dict[PSUIndex]["Thermals"][ThermalIndex][key]))
                    return  PSU_Dict[PSUIndex]["Thermals"][ThermalIndex][key]
                else:
                    log.fail("Specified key is not present in the dictionary file : %s" %key)
                    return 0
        else:
            log.fail("Specified FAN module Index value is not found: %d" %Thermal)
            return -1
    else:
        log.info("No thermal modules found in the PSU")
        return -2

def Get_Thermal_Value(device, Thermal, key):
    log.debug("Entering  GET PSU Thermal Value with args : %s" % (str(locals())))
    input1 = dump_device_data(device)
    Thermal_Dict = input1["Thermals"]

    ThermalIndex = Thermal - 1

    if ThermalIndex <= len(Thermal_Dict):
        if key in Thermal_Dict[ThermalIndex]:
            log.info("Thermal index %d key and value : %s - %s" %(Thermal, key, Thermal_Dict[ThermalIndex][key]))
            return Thermal_Dict[ThermalIndex][key]
        else:
            log.fail("Specified key is not present in the dictionary file: %s" %key)
            return 0
    else:
        log.fail("Speficied thermal index value is not found: %d" %Thermal)
        return -1

def UpdateThermalData(device, Thermal_Index, PSU_Index=0):
    if PSU_Index == 0:
        temp = Get_Thermal_Value(device, Thermal_Index, 'Temperature')
    else:
        temp = Get_PSU_Thermal_Value(device, PSU_Index, Thermal_Index, 'Temperature')

    return temp

"""
    Test function to verify the thermal sensor TEMPERATURE and match with expected result.
"""

def test_SensorTemperatureTest(device, PlatformEnv):
    thermals = PlatformEnv["Thermal"]["Thermal_Index"]
    total_psu = int(PlatformEnv["PSU"]["Total"])
    psu_thermals = []
    for i in range(1, total_psu+1):
        psu_thermals += PlatformEnv["PSU"]["PSU-" + str(i)]["Thermal_Index"]

    TOTAL_THERMAL_SENSORS = len(thermals) + len(psu_thermals)

    thermal_temperatures = []
    condition = True

    retval_check = True

    for i in thermals:
        status = Get_Thermal_Value(device, i, 'Status')
        if status == "Functional":
            time.sleep(2)
            temp = Get_Thermal_Value(device, i, 'Temperature')

            if 'C' not in str(temp):
                continue
            r = re.findall("\d+", temp)

            if r == 0:
                while retval_check:
                    retval = UpdateThermalData(device, i)
                    if retval != 0:
                        r = retval
                        retval_check = False

            temp = float(r[0] + '.' + r[1])
            thermal_temperatures.append(temp)
        else:
            log.debug("Few thermal sensor objects are missing: %d - Missing", i)

    retval_check = True

    for j in range(1, total_psu+1):
        if len(PlatformEnv["PSU"]["PSU-" + str(j)]["Thermal_Index"]) > 1:
            for k in range(1, len(PlatformEnv["PSU"]["PSU-" + str(j)]["Thermal_Index"]) + 1):
                if status == "Functional":
                    time.sleep(2)
                    temp = Get_PSU_Thermal_Value(device, j, k, 'Temperature')

                    if 'C' not in str(temp):
                        continue
                    r = re.findall("\d+", temp)

                    if r == 0:
                        while retval_check:
                            retval = UpdateThermalData(device, i)
                            if retval != 0:
                                r = retval
                                retval_check = False

                    temp = float(r[0] + '.' + r[1])
                    thermal_temperatures.append(temp)
                else:
                    log.debug("Few thermal sensor objects are missing: %d - Missing" %i)

    for each in thermal_temperatures:
        condition = condition and each > 10 and each < 40

    try:
        assert condition
        log.info("All thermal temprature are as required ( >10 & <38 ).\n%s" %(str(thermal_temperatures)))
    except AssertionError:
        log.fail(f"Error in thermal temperature. All should be between 10-38.\nBut found\n{thermal_temperatures}")
        raise

def GetThermal_TemperatureInfo(device, Index, key):
    log.debug("Entering  GET Thermal Temperature info with args : %s" % (str(locals())))
    device_obj = Device.getDeviceObject(device)
    if Index == 1:
        cmd = 'onlpdump | grep -a \'thermal @ 1 = {\' -A4 | grep -a \'Temperature\' -A0'
    elif Index == 2:
        cmd = 'onlpdump | grep -a \'thermal @ 2 = {\' -A4 | grep -a \'Temperature\' -A0'
    elif Index == 3:
        cmd = 'onlpdump | grep -a \'thermal @ 3 = {\' -A4 | grep -a \'Temperature\' -A0'
    elif Index == 4:
        cmd = 'onlpdump | grep -a \'thermal @ 4 = {\' -A4 | grep -a \'Temperature\' -A0'
    elif Index == 5:
        cmd = 'onlpdump | grep -a \'thermal @ 5 = {\' -A4 | grep -a \'Temperature\' -A0'
    elif Index == 6:
        cmd = 'onlpdump | grep -a \'thermal @ 6 = {\' -A4 | grep -a \'Temperature\' -A0'
    elif Index == 7:
        cmd = 'onlpdump | grep -a \'thermal @ 7 = {\' -A4 | grep -a \'Temperature\' -A0'
    elif Index == 8:
        cmd = 'onlpdump | grep -a \'thermal @ 8 = {\' -A4 | grep -a \'Temperature\' -A0'
    elif Index == 9:
        cmd = 'onlpdump | grep -a \'thermal @ 9 = {\' -A4 | grep -a \'Temperature\' -A0'
    elif Index == 10:
        cmd = 'onlpdump | grep -a \'thermal @ 10 = {\' -A4 | grep -a \'Temperature\' -A0'
    elif Index == 11:
        cmd = 'onlpdump | grep -a \'thermal @ 11 = {\' -A4 | grep -a \'Temperature\' -A0'
    elif Index == 12:
        cmd = 'onlpdump | grep -a \'thermal @ 12 = {\' -A4 | grep -a \'Temperature\' -A0'
    elif Index == 13:
        cmd = 'onlpdump | grep -a \'thermal @ 13 = {\' -A4 | grep -a \'Temperature\' -A0'
    else:
        log.fail("Specified thermal index value is not found in the switch: %d" %Index)
        return 0
    output = Device.executeCmd(device_obj, cmd)
    # Search only if data is not 'None'.
    if output:
        val = re.search('Not present.', output)
        if val:
            print("Output is not present.")
            return 0
    else:
        return -1

    Thermal_Temperature = dict()

    match=re.search(r"(Temperature):\s+(\d+)",output,re.I|re.M)
    Thermal_Temperature[match.group(1)] = match.group(2)
    log.info("Thermal_Temperature : %s" %Thermal_Temperature)
    if key in Thermal_Temperature:
        return Thermal_Temperature[key]
    else:
        log.fail("Specified key is not present in the dictionary file: %s" %key)
        return 0

def GetThermal_ThresholdInfo(device, Index, key):
    log.debug("Entering  GET Thermal Threshold info with args : %s" % (str(locals())))
    device_obj = Device.getDeviceObject(device) 
    if Index == 1:
        cmd = 'onlpdump | grep -a \'thermal @ 1 = {\' -A9 | grep -v \'thermal @ 1 = {\' | grep -a \'thresholds = {\' -A3 | grep -v \'thresholds = {\''
    elif Index == 2:
        cmd = 'onlpdump | grep -a \'thermal @ 2 = {\' -A9 | grep -v \'thermal @ 2 = {\' | grep -a \'thresholds = {\' -A3 | grep -v \'thresholds = {\''
    elif Index == 3:
        cmd = 'onlpdump | grep -a \'thermal @ 3 = {\' -A9 | grep -v \'thermal @ 3 = {\' | grep -a \'thresholds = {\' -A3 | grep -v \'thresholds = {\''
    elif Index == 4:
        cmd = 'onlpdump | grep -a \'thermal @ 4 = {\' -A9 | grep -v \'thermal @ 4 = {\' | grep -a \'thresholds = {\' -A3 | grep -v \'thresholds = {\''
    elif Index == 5:
        cmd = 'onlpdump | grep -a \'thermal @ 5 = {\' -A9 | grep -v \'thermal @ 5 = {\' | grep -a \'thresholds = {\' -A3 | grep -v \'thresholds = {\''
    elif Index == 6:
        cmd = 'onlpdump | grep -a \'thermal @ 6 = {\' -A9 | grep -v \'thermal @ 6 = {\' | grep -a \'thresholds = {\' -A3 | grep -v \'thresholds = {\''
    elif Index == 7:
        cmd = 'onlpdump | grep -a \'thermal @ 7 = {\' -A9 | grep -v \'thermal @ 7 = {\' | grep -a \'thresholds = {\' -A3 | grep -v \'thresholds = {\''
    elif Index == 8:
        cmd = 'onlpdump | grep -a \'thermal @ 8 = {\' -A9 | grep -v \'thermal @ 8 = {\' | grep -a \'thresholds = {\' -A3 | grep -v \'thresholds = {\''
    elif Index == 9:
        cmd = 'onlpdump | grep -a \'thermal @ 9 = {\' -A9 | grep -v \'thermal @ 9 = {\' | grep -a \'thresholds = {\' -A3 | grep -v \'thresholds = {\''
    elif Index == 10:
        cmd = 'onlpdump | grep -a \'thermal @ 10 = {\' -A9 | grep -v \'thermal @ 10 = {\' | grep -a \'thresholds = {\' -A3 | grep -v \'thresholds = {\''
    elif Index == 11:
        cmd = 'onlpdump | grep -a \'thermal @ 11 = {\' -A9 | grep -v \'thermal @ 11 = {\' | grep -a \'thresholds = {\' -A3 | grep -v \'thresholds = {\''
    elif Index == 12:
        cmd = 'onlpdump | grep -a \'thermal @ 12 = {\' -A9 | grep -v \'thermal @ 12 = {\' | grep -a \'thresholds = {\' -A3 | grep -v \'thresholds = {\''
    elif Index == 13:
        cmd = 'onlpdump | grep -a \'thermal @ 13 = {\' -A9 | grep -v \'thermal @ 13 = {\' | grep -a \'thresholds = {\' -A3 | grep -v \'thresholds = {\''
    else:
        log.fail("Specified thermal index value is not found in the switch: %d" %Index)
        return 0
 
    output = Device.executeCmd(device_obj, cmd)
    # Search only if data is not 'None'.
    if output:
        val = re.search('Not present.', output)
        if val:
            log.info("Data is not present.")
            raise
    else:
        raise

    temp = output.strip().splitlines()

    Thermal_Threshold = dict()
    for val in temp:
        match=re.search(r"(\S+)\:\s+(\d+)",val)
        if match:
            Thermal_Threshold[match.group(1)] = match.group(2)
    log.info("Thermal Threshold: %s" %Thermal_Threshold)
    if key in Thermal_Threshold:
        return Thermal_Threshold[key]
    else:
        log.fail("Specified key is not present in the dictionary file: %s", key)
        return -1


def test_SensorThresholdTest(device, PlatformEnv):
    thermals = PlatformEnv["Thermal"]["Thermal_Index"]
    total_psu = int(PlatformEnv["PSU"]["Total"])
    psu_thermals = []
    for i in range(1, total_psu+1):
        psu_thermals += PlatformEnv["PSU"]["PSU-" + str(i)]["Thermal_Index"]

    TOTAL_THERMAL_SENSORS = thermals + psu_thermals

    # For each thermal sensor present.
    thermal_not_present = set()
    thermal_not_as_required = {}
    for i in thermals:

        # For each type of thermal data.
        for each in ['Warning', 'Error', 'Shutdown']:
            # Fetch thermal threshold data.
            threshold = GetThermal_ThresholdInfo(device, i, each)
            temperature = GetThermal_TemperatureInfo(device, i, "Temperature")

            # Check if thermal threshold data is present or not as required.
            if int(temperature) == 0:
                log.fail("Thermal%d Temperature cant be 0" %(i))
                raise
            if int(threshold) == 0:
                log.fail("Thermal%d %s Threshold cant be 0" %(i,each))
                raise
            if int(threshold) == -1:
                thermal_not_present.add("Thermal-" + str(i))
            elif int(threshold) < int(temperature):
                thermal_not_as_required["Thermal-" + str(i+1)] = temperature
                thermal_not_as_required["Thermal-" + str(i+1) + "-" + each] = threshold

    try:
        if len(thermal_not_present):
            log.fail("Below thermals are not present.\n %s" %str(thermal_not_present))
            raise
        if len(thermal_not_as_required):
            log.fail("Below thermal's temperature are NOT as required ( Should be < threshold ).\n %s" %str(thermal_not_as_required))
            raise
        assert len(thermal_not_as_required) == 0
        log.info("Thermal data collected for all thermal sensors: %s" %(thermal_not_as_required))
    except AssertionError:
        raise

def test_CheckSystemLED(device, PlatformEnv):

    """

    Test function to get current status and mode of the System LED and match with expected result

    """


    SYSTEM_LED_Index = PlatformEnv["LED"]["SYSTEM_LED"]

    Value = Get_LED_Value(device, SYSTEM_LED_Index, 'Description')

    """
        Matching return value with expected result.
        Assert Pass:  return nothing
        Assert Fail:  raise exception
    """
    result = StringMatch("System.*LED", Value)

    try:
        assert result == 1
        log.info("LED %d represent: %s" %(SYSTEM_LED_Index, Value))
    except AssertionError:
        log.fail("LED %d description is mismatch with expected result: %s" %(SYSTEM_LED_Index, Value))
        raise


    Value = Get_LED_Value(device, SYSTEM_LED_Index, 'State')

    """
        Matching return value with expected result.
        Assert Pass:  return nothing
        Assert Fail:  raise exception
    """
    try:
        assert Value == 'Present'
        log.info("LED %d state: %s" %(SYSTEM_LED_Index, Value))
    except AssertionError:
        log.fail("LED %d state: %s" %(SYSTEM_LED_Index, Value))
        raise

    Value = Get_LED_Value(device, SYSTEM_LED_Index, 'Mode')

    """
        Matching return value with expected result.
        Assert Pass:  return nothing
        Assert Fail:  raise exception
    """
    result = StringMatch("BLINKING", Value)

    try:
        assert result == 1
        log.info("LED %d mode is : %s" %(SYSTEM_LED_Index, Value))
    except AssertionError:
        log.fail("LED %d mode is : %s" %(SYSTEM_LED_Index, Value))
        raise

def Get_LED_Value(device, LED, key):
    log.debug("Entering  GET LED Value with args : %s" % (str(locals())))
    input1 = dump_device_data(device)
    LED_Dict = input1["LEDs"]

    LEDIndex = LED - 1

    if LEDIndex <= len(LED_Dict):
        if key in LED_Dict[LEDIndex]:
            log.info("LED %d's key and value: %s - %s" %(LED, key, LED_Dict[LEDIndex][key]))
            return LED_Dict[LEDIndex][key]
        else:
            log.fail("Specified key is not present in the dictionary file: %s" %key)
            return 0
    else:
        log.fail("Speficied LED index value is not found: %d" %LED)
        return -1

def test_CheckAlertLED(device, PlatformEnv):


    ALERT_LED_Index = PlatformEnv["LED"]["ALERT_LED"]

    Value = Get_LED_Value(device, ALERT_LED_Index, 'Description')

    """
        Matching return value with expected result.
        Assert Pass:  return nothing
        Assert Fail:  raise exception
    """
    try:
        assert Value == 'Alert LED (Front)'
        log.info("LED %d represent: %s" %(ALERT_LED_Index, Value))
    except AssertionError:
        log.fail("LED %d represent: %s" %(ALERT_LED_Index, Value))
        raise

    Value = Get_LED_Value(device, ALERT_LED_Index, 'State')

    """
        Matching return value with expected result.
        Assert Pass:  return nothing
        Assert Fail:  raise exception
    """
    try:
        assert Value == 'Present'
        log.info("LED %d state: %s" %(ALERT_LED_Index, Value))
    except AssertionError:
        log.fail("LED %d state: %s" %(ALERT_LED_Index, Value))
        raise

    Value = Get_LED_Value(device, ALERT_LED_Index, 'Mode')

    """
        Matching return value with expected result.
        Assert Pass:  return nothing
        Assert Fail:  raise exception
    """
    try:
        assert Value == 'GREEN'
        log.info("LED %d mode is :%s , Expected GREEN" %(ALERT_LED_Index, Value))
    except AssertionError:
        log.fail("LED %d mode is: %s , Expected GREEN" %(ALERT_LED_Index, Value))
        raise

def test_CheckAlertLED_under_One_FAN_Missing(device):

    """
        Check Alert LED mode when only one FAN is absent
    """

    Value = Get_LED_Value(device, ALERT_LED_Index, 'Mode')

    """
        Matching return value with expected result.
        Assert Pass:  return nothing
        Assert Fail:  raise exception
    """
    try:
        assert Value == 'YELLOW_BLINKING'
        log.info("LED %d mode is changed to %s when one FAN module is removed from the switch " %(ALERT_LED_Index, Value))
    except AssertionError:
        log.fail("There is problem with ALERT LED. LED mode is not changed to %s when one of the FAN module is missing !!!" % Value)
        raise


def test_CheckAlertLED_under_morethan_One_FRU_failure(DUTsInfo):

    """
        Check Alert LED mode when multiple FAN is absent
    """

    Value = Get_LED_Value(device, ALERT_LED_Index, 'Mode')

    """
        Matching return value with expected result.
        Assert Pass:  return nothing
        Assert Fail:  raise exception
    """
    try:
        assert Value == 'YELLOW'
        log.info("LED %d mode is changed to %s when multiple FAN modules removed from the switch " %(ALERT_LED_Index, Value))
    except AssertionError:
        log.fail("There is problem with ALERT LED. LED mode is not changed to %s when multiple FAN modules are missing !!!" %Value)
        raise

def test_CheckPSULED(device, PlatformEnv):

    PSU_LED_Index = PlatformEnv["LED"]["PSU_LED"]

    for PSU in PSU_LED_Index:
        Value = Get_LED_Value(device, PSU, 'Description')
        """
            Matching return value with expected result.
            Assert Pass:  return nothing
            Assert Fail:  raise exception
        """
        returnval = StringMatch("PSU.*LED", Value)

        try:
            assert returnval == 1
            log.info("LED %d represent %s" %(PSU, Value))
        except AssertionError:
            log.fail("LED %d represent %s" %(PSU, Value))
            raise


    for PSU in PSU_LED_Index:
        Value = Get_LED_Value(device, PSU, 'State')

        """
            Matching return value with expected result.
            Assert Pass:  return nothing
            Assert Fail:  raise exception
        """
        try:
            assert Value == 'Present'
            log.info("LED %d mode: %s" %(PSU, Value))
        except AssertionError:
            log.fail("LED %d mode: %s" %(PSU, Value))
            raise


    for PSU in PSU_LED_Index:
        Value = Get_LED_Value(device, PSU, 'Mode')

        """
            Matching return value with expected result.
            Assert Pass:  return nothing
            Assert Fail:  raise exception
        """
        returnval = StringMatch("AUTO|GREEN", Value)

        try:
            assert returnval == 1
            log.info("LED %d mode: %s" %(PSU, Value))
        except AssertionError:
            log.fail("LED %d mode: %s" %(PSU, Value))
            raise

def CheckOpticsPresence(device, Port):

    log.debug("Entering  check Optics presence with args : %s" % (str(locals())))
    device_obj = Device.getDeviceObject(device)
    cmd = 'onlpdump | grep -a -i \'Port ' + str(Port) + '\'' + ' -A0'
    output = Device.executeCmd(device_obj, cmd)

    result = re.search("Present", output)

    if result:
        log.success("Optics found!")
        return 1
    else:
        log.fail("Optics not found!")
        return -1

def GetOpticsDetail(device):

    log.debug("Entering  check Optics detail with args : %s" % (str(locals())))
    device_obj = Device.getDeviceObject(device)
    cmd = 'onlpdump -S | grep -a \'Type*\' -A48 | grep -v \'Type*\''
    output = Device.executeCmd(device_obj, cmd)
    Optics = dict()
    output = output.splitlines()
    p1 = 'Port\s+Type\s+Media'
    p2 = '\d+\s+NONE'
    p3 = '(\d+)\s+(.*BASE\S+)\s+(Copper|Fiber)\s+(\d+m)\s+(\S+)\s+(\S+)\s+(\S+)'

    for line in output:
        match = re.search(p1,line)
        if match:
                continue
        match = re.search(p2,line)
        if match:
                continue
        match = re.search(p3,line)
        if match:
                port_n = match.group(1)
                Optics[port_n] = {}
                Optics[port_n]['Type'] = match.group(2)
                Optics[port_n]['Media'] = match.group(3)
                Optics[port_n]['Length'] = match.group(4)
                Optics[port_n]['Vendor'] = match.group(5)
                Optics[port_n]['Model'] = match.group(6)
                Optics[port_n]['SerialNumber'] = match.group(7)
    log.info("Optics: %s" %Optics)
    return Optics

def test_Check_Optics_Presence(device,portlist):
    try:
        for port in portlist:
            result1 = CheckOpticsPresence(device, port)
            assert result1 == 1
            log.info("Optics detected on port %s" %port)
            log.info("Optics connected")
        OpticInfo = GetOpticsDetail(device)
        for port in portlist:
            port = str(int(port))
            log.info("Optics Info: \n \
                        Port  : %s\n \
                        Type  : %s\n \
                        Media : %s\n \
                        Length: %s\n \
                        Vendor: %s\n \
                        Model : %s\n \
                        Serial Number: %s\n" %(port, OpticInfo[port]["Type"], OpticInfo[port]["Media"], OpticInfo[port]["Length"], OpticInfo[port]["Vendor"], OpticInfo[port]["Model"], OpticInfo[port]["SerialNumber"]))
    except AttributeError:
        log.fail("No Optics detected on port: %s" %port)
        raise

def test_stress_onl(device,reboot_count=2, timeout=300):
    device_obj = Device.getDeviceObject(device)
    actual_name = exp_product_name
    for each in range(reboot_count):
        log.info("Rebooting the DUT")
        device_obj.sendCmd('reboot')
        time.sleep(120)
        device_obj.sendline('\r')
        log.info("Checking device reachability ")
        device_obj.read_until_regexp('localhost login',timeout=80)
        device_obj.loginToDiagOS()
        cmd = 'dhclient -v'
        Device.execCmd(device_obj, cmd)
        sys_name = get_product_name(device)
        try:
            assert actual_name == sys_name
        except AssertionError:
            raise
        state_1 = Get_PSU_Value(device, 1, 'State')
        state_2 = Get_PSU_Value(device, 2, 'State')
        condition1 = state_1 == 'Present'
        condition2 = state_2 == 'Present'

        try:
            assert condition1 and condition2
        except AssertionError:
            raise
        Value = Get_LED_Value(device, 1, 'Description')
        result = StringMatch("System.*LED", Value)

        try:
            assert result == 1
        except AssertionError:
            raise

def Install_ONL_OS_from_ONIE(device,version, protocol, timeout=600):
    """
    Update ONL OS
    :param protocol:http/tftp
    :param timeout:out of time
    :param bin_path: file of bin path
    """
    log.debug("Entering ONL_Install_UnInstall_Mode details args : %s" %(str(locals())))
    device_obj = Device.getDeviceObject(device)

    update_version = None
    error_str = ""
    log.debug("check the ONL version ,Image provided : {} and {} ".format(ONLversion, ONLimage))
    if (protocol == 'tftp'):
        cmd = "onie-nos-install %s://%s/%s" % (protocol.lower(), tftp_server_ip, ONLimage)
    else:
        cmd = "onie-nos-install %s://%s/%s" % (protocol.lower(), http_server_ip, ONLimage)
    device_obj.sendline(cmd)
    output = device_obj.read_until_regexp('ONL loader install successful.', timeout)
    if HasError(output):
        log.fail('Have error during ONL Install!')
    device_obj.read_until_regexp('Rebooting in 3s', timeout=30)
    device_obj.read_until_regexp("Open Network Linux",70)
    bios_menu_lib.send_key(device_type, "KEY_ENTER")
    time.sleep(70)
    device_obj.loginDiagOS()

#######################
def get_device_OID(device):
    log.debug("Entering get_device_OID with args : %s" %(str(locals())))
    device_obj = Device.getDeviceObject(device)
    #whitebox_lib.change_directory(device,"/home/cel_diag/seastone2v2/bin")
    cmd = f"onl-platform-show"
    output = Device.executeCmd(device_obj, cmd)
    log.info(output)
    sys_OID=re.search(r"System Object Id:\s+([\d\.]+)",output,re.I|re.M)[1]
    return sys_OID 

def test_device_ONL_SNMP(device,device_OID):
    log.debug("Entering test_device_ONL_SNMP with args : %s" %(str(locals())))
    device_obj = Device.getDeviceObject(device)
    device_obj.sendCmd("onlp-snmpd -d")
    cmd = f"snmpwalk -v2c -c public 127.0.0.1 %s" %(device_OID)
    output = Device.executeCmd(device_obj, cmd)
    log.info(output)
    #device_obj.sendCmd(Const.KEY_CTRL_C)
    onlp_snmp=re.search(r"No Such Object available on this agent at this OID",output,re.I|re.M)
    if onlp_snmp:
        log.fail("snmp agent is not running")
        raise  RuntimeError("ONL SNMP failed")
    else:
        log.success("snmp agent pass")
    device_obj.sendCmd("pkill onlp-snmpd")
    cmd = f"snmpwalk -v2c -c public 127.0.0.1 %s" %(device_OID)
    output = Device.executeCmd(device_obj, cmd)
    log.info(output)
    onlp_snmp=re.search(r"No Such Object available on this agent at this OID",output,re.I|re.M)
    if onlp_snmp:
        log.success("snmp agent killed successfully")
    else:
        log.fail("snmp agent still running")
        raise  RuntimeError("ONL SNMP failed")
    device_obj.sendCmd("onlp-snmpd -d")


def test_device_reset(device,exp_device_data):
    log.debug("Entering test_device_reset with args : %s" %(str(locals())))
    device_obj = Device.getDeviceObject(device)
    parsed_output = dump_device_data(device)
    compare_device_data(exp_device_data,parsed_output)
    log.info("Rebooting the DUT")
    cmd = 'reboot'
    output = Device.sendCmd(device_obj, cmd)
    time.sleep(120)
    verify_onl_login(device)
    cmd = 'dhclient -v'
    output = Device.execCmd(device_obj, cmd)
    parsed_output = dump_device_data(device)
    compare_device_data(exp_device_data,parsed_output)

def exec_ipmitool_fru_print(device):
    log.debug("Entering test_ipmitool_fru with args : %s" %(str(locals())))
    device_obj = Device.getDeviceObject(device)
    cmd = f"ipmitool fru print"
    output = Device.executeCmd(device_obj, cmd)
    log.info("Output: %s" %output)
    pat1 = "FRU Device Description : (.*)"
    pat2 = "Board Mfg Date        : (.*)"
    pat3 = "Board Mfg             : (.*)"
    pat4 = "Board Product         : (.*)"
    pat5 = "Board Serial          : (.*)"
    pat6 = "Board Part Number     : (.*)"
    pat7 = "Board Extra           : ([A-Z]+\d+.*)"
    pat8 = "Board Extra           : (\d*)"
    pat9 = "Product Manufacturer  : (.*)"
    pat10 = "Product Name          : (.*)"
    pat11 = "Product Part Number   : (.*)"
    pat12 = "Product Serial        : (.*)"
    pat13 = "Product Extra         : (.*)"

    FRU_Device = {}
    for line in output.splitlines():
        match = re.search(pat1,line)
        if match:
            val1 = match.group(1)
            FRU_Device[val1] = {}
        match = re.search(pat2, line)
        if match:
            FRU_Device[val1]['Board Mfg Date'] = match.group(1)
        match = re.search(pat3, line)
        if match:
            FRU_Device[val1]['Board Mfg'] = match.group(1)
        match = re.search(pat4, line)
        if match:
            FRU_Device[val1]['Board Product'] = match.group(1)
        match = re.search(pat5, line)
        if match:
            FRU_Device[val1]['Board Serial'] = match.group(1)
        match = re.search(pat6, line)
        if match:
            FRU_Device[val1]['Board Part Number'] = match.group(1)
        match = re.search(pat7, line)
        if match:
            FRU_Device[val1]['Board Extra'] = match.group(1)
        match = re.search(pat9, line)
        if match:
            FRU_Device[val1]['Product Manufacturer'] = match.group(1)
        match = re.search(pat10, line)
        if match:
            FRU_Device[val1]['Product Name'] = match.group(1)
        match = re.search(pat11, line)
        if match:
            FRU_Device[val1]['Product Part Number'] = match.group(1)
        match = re.search(pat12, line)
        if match:
            FRU_Device[val1]['Product Serial'] = match.group(1)
        match = re.search(pat13, line)
        if match:
            FRU_Device[val1]['Product Extra'] = match.group(1)
    log.info("FRU Device Dictionary: %s" %FRU_Device)
    return FRU_Device

def ONL_Install_UnInstall_Mode(device,mode):
    """
    Select the Onie's interface: enter different Onie functions
    :param mode:installer/rescue/uninstall/update
    """
    log.debug("Entering ONL_Install_UnInstall_Mode details args : %s" %(str(locals())))
    device_obj = Device.getDeviceObject(device)

    mode = mode.lower()
    Device.sendCmd(device_obj,"reboot")
    log.debug("going to onie:{} mode ...".format(mode))
    log.debug("now, rebooting the dut ...")

    device_obj.read_until_regexp("Open Network Linux",120)
    bios_menu_lib.send_key(device_type, "KEY_DOWN", 1)
    bios_menu_lib.send_key(device_type, "KEY_ENTER")
    #device_obj.read_until_regexp("Welcome to GRUB", 10)

    if mode == 'installer':
        log.debug('entering onie install mode ...')
        #bios_menu_lib.send_key(device_type, "KEY_ENTER")
        device_obj.read_until_regexp("ONIE: Install OS", 7)
        bios_menu_lib.send_key(device_type, "KEY_ENTER")
        device_obj.read_until_regexp("Please press Enter to activate this console", 90)
        bios_menu_lib.send_key(device_type, "KEY_ENTER")
        Device.executeCmd(device_obj,"onie-stop")

    elif mode == 'uninstall':
        log.debug('entering onie uninstall mode ...')
        bios_menu_lib.send_key(device_type, "KEY_DOWN", 2)
        device_obj.read_until_regexp("ONIE: Uninstall OS", 7)
        bios_menu_lib.send_key(device_type, "KEY_ENTER")
        """
        After uninstall device will boot into install mode
        """
        time.sleep(180)
        device_obj.read_until_regexp("Please press Enter to activate this console", 150)
        log.debug('entering onie install mode ...')
        time.sleep(10)
        Device.executeCmd(device_obj,"onie-stop")

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
                #raise RuntimeError('Find {} in: {}'.format(error, line))
                log.fail('Find {} in: {}'.format(error, line))
                match_one = True
    return match_one

def StringMatch(inputstr, match):

    result = re.search(inputstr, match)

    if result:
        return 1;
    else:
        return -1

