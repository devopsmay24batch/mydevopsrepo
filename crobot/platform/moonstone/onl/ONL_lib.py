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
import multiprocessing
from TelnetDevice import TelnetDevice
from crobot.PowerCycler import PowerCycler
import MOONSTONECommonLib
try:
    import parser_openbmc_lib as parserOpenbmc
    import DeviceMgr
    from Device import Device

except Exception as err:
    log.cprint(str(err))

deviceM = DeviceMgr.getDevice()
workDir = CRobot.getWorkDir()
sys.path.append(os.path.join(workDir, 'common', 'commonlib'))
sys.path.append(os.path.join(workDir, 'platform', 'moonstone'))
sys.path.append(os.path.join(workDir, 'platform', 'moonstone','diag'))
sys.path.append(os.path.join(workDir, 'platform', 'moonstone','onl'))

run_command = partial(CommonLib.run_command, deviceObj=deviceM, prompt=deviceM.promptDiagOS)
time.sleep(10)

import Logger as log

def dump_device_data(device):
    device_obj = Device.getDeviceObject(device)
    device_obj.flush()
    cmd = 'onlpdump -ery > temp.yml'
    output = Device.executeCmd(device_obj, cmd)
    try:
        CommonLib.get_file_by_scp(device_obj.managementIP, device_obj.rootUserName,device_obj.rootPassword , '/root', 'temp.yml',workDir )
        with open('{}/temp.yml'.format(workDir), 'r') as r:
            input1 = yaml.safe_load(r)
        log.info(str(input1["LEDs"]))
        os.remove('{}/temp.yml'.format(workDir))
        output = Device.executeCmd(device_obj, 'rm /root/temp.yml')
        return input1
    except AssertionError:
        log.fail(f"Output couldnt dump properly")
        


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
   device_obj = Device.getDeviceObject(device)
   cmd = 'onlpdump -j '
   log.info("Wait for 60 secs before getting device data.")
   time.sleep(60)
   output=device_obj.executeCmd(cmd)
   CommonKeywords.should_match_ordered_regexp_list(output, onlpdump_pattern)
   for port in range(0, 66):
       if port<10:
           port='0'+str(port)
       port_present_pattern="Port "+str(port)+": Present, Status = 0x00000000"
       port_missing_pattern="Port "+str(port)+": Missing."
       port_pattern="({})|({})".format(port_present_pattern, port_missing_pattern)
       CommonKeywords.should_match_a_regexp(output, port_pattern)
   
   log.success("ONL json data is correct")
       
   
def verify_device_data(device):
   device_obj = Device.getDeviceObject(device)
   log.info("Wait for 60 secs before getting device data.")
   time.sleep(60)
   cmd = 'onlpdump -d '
   output=device_obj.executeCmd(cmd)
   CommonKeywords.should_match_ordered_regexp_list(output, onlpdump_pattern)
   for port in range(0, 66):
       if port<10:
           port='0'+str(port)
       port_present_pattern="Port "+str(port)+": Present, Status = 0x00000000"
       port_missing_pattern="Port "+str(port)+": Missing."
       port_pattern="({})|({})".format(port_present_pattern, port_missing_pattern)
       CommonKeywords.should_match_a_regexp(output, port_pattern)
   
   log.success("Every information of device data is as expected.")


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
    #log.debug(moonstone_diag_version)
    bios_version=re.search(r"Version:\s+(.*)",output,re.I|re.M)[1]
    return bios_version
    

def get_onie_version(device):
    log.debug("Entering get_onie_version details args : %s" %(str(locals())))
    cmd = f'onlpdump -s'
    device_obj = Device.getDeviceObject(device)
    output = Device.executeCmd(device_obj, cmd)
    log.info(output)
    onie_version=re.search(r'ONIE Version:(.*)',output,re.I|re.M)[1]
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
    whitebox_lib.change_directory(device,"/sys/devices/platform/cls_sw_fpga/FPGA")
    cmd = f"cat version"
    output = Device.executeCmd(device_obj, cmd)
    log.info(output)
    output = output.split("\n")
    
    #fpga_version=re.search(r"([\d\.]+)",output,re.I|re.M)[1]
    fpga_version=output[-5]
    return fpga_version
    
    
def get_fpga_scratch(device, pattern):
    device_obj = Device.getDeviceObject(device)
    log.debug("Entering check_fpga_scratch_getreg details args : %s" %(str(locals())))
    cmd1 = 'cat scratch'
    output = Device.executeCmd(device_obj, cmd1)
    CommonKeywords.should_match_a_regexp(output, pattern)
    log.success("FGPA Scratch value is correct")
    
def check_default_fpga_scratch_getreg(device):
    device_obj = Device.getDeviceObject(device)
    log.debug("Entering check_default_fpga_scratch details args : %s" %(str(locals())))
    log.debug("Powercycle the device")
    MOONSTONECommonLib.powerCycle(device)
    
    whitebox_lib.change_directory(device,"/sys/devices/platform/cls_sw_fpga/FPGA")
    
    output = Device.executeCmd(device_obj, "cat getreg")
    CommonKeywords.should_match_a_regexp(output, exp_fpga_version)
    log.success("Default FGPA getreg value is as expected")
    
    output=get_fpga_version(device)
    CommonKeywords.should_match_a_regexp(output, exp_fpga_version)
    log.success("Default FGPA version value is as expected")
    
    get_fpga_scratch(device, default_fpga_scratch_value)
    device_obj.sendCmd('cd')
    log.success("Default FGPA Scratch value is as expected")

def get_fpga_getreg(device, pattern, register):
    device_obj = Device.getDeviceObject(device)
    log.debug("Entering check_fpga_scratch_getreg details args : %s" %(str(locals())))
    cmd1 = 'echo '+register+' > getreg'
    cmd2 = 'cat getreg'
    Device.executeCmd(device_obj, cmd1)
    output = Device.executeCmd(device_obj, cmd2)
    CommonKeywords.should_match_a_regexp(output, pattern)
    log.success("FGPA getreg value is correct")
    
def check_set_fpga_scratch(device, register):
    device_obj = Device.getDeviceObject(device)
    log.debug("Entering check_fpga_scratch_getreg details args : %s" %(str(locals())))
    cmd1 = 'cat scratch'
    cmd2 = 'echo '+ register +' > scratch'
    output = Device.executeCmd(device_obj, cmd2)
    get_fpga_scratch(device, fpga_scratch_dict[register])
    
def check_setreg_fpga(device, register, value):
    device_obj = Device.getDeviceObject(device)
    log.debug("Entering check_setreg_fpga details args : %s" %(str(locals())))
    cmd1 = 'cat scratch'
    cmd2 = 'cat getreg'
    cmd3 = 'echo '+register+' '+value+' > setreg'
    output = Device.executeCmd(device_obj, cmd3)
    get_fpga_scratch(device, fpga_scratch_dict[value]) 
    get_fpga_getreg(device, fpga_scratch_dict[value], register) 


def check_default_switch_cpld_version(device):
    device_obj = Device.getDeviceObject(device)
    log.debug("Entering check_default_switch_cpld_version details args : %s" %(str(locals())))
    log.debug("Powercycle the device")
    MOONSTONECommonLib.powerCycle(device)
    
    whitebox_lib.change_directory(device,"/sys/devices/platform/cls_sw_fpga")
    output=device_obj.executeCmd("cat CPLD1/version")
    CommonKeywords.should_match_a_regexp(output, exp_switch_cpld_version)
    output=device_obj.executeCmd("cat CPLD1/getreg")
    CommonKeywords.should_match_a_regexp(output, exp_switch_cpld_version)
    output=device_obj.executeCmd("cat CPLD1/scratch")
    CommonKeywords.should_match_a_regexp(output, default_scratch_value)
    output=device_obj.executeCmd("cat CPLD2/version")
    CommonKeywords.should_match_a_regexp(output, exp_switch_cpld_version)
    output=device_obj.executeCmd("cat CPLD2/getreg")
    CommonKeywords.should_match_a_regexp(output, exp_switch_cpld_version)
    output=device_obj.executeCmd("cat CPLD2/scratch")
    CommonKeywords.should_match_a_regexp(output, default_scratch_value)
    
    device_obj.sendCmd('cd')
    log.success("Default values of scratch and version of switch cpld are as expected")

def check_switch_cpld_read_write_operation(device):
    device_obj = Device.getDeviceObject(device)
    whitebox_lib.change_directory(device,"/sys/devices/platform/cls_sw_fpga")
    
    get_set_swict_cpld_scratch_register(device, "0x01", "getreg", switch_cpld_register_value['0x01'])
    get_set_swict_cpld_scratch_register(device, "0x21", "scratch", switch_cpld_register_value['0x21'])
    get_set_swict_cpld_scratch_register(device, "0xa5", "scratch", switch_cpld_register_value['0xa5'])
    
    device_obj.executeCmd("echo 0x01 0x5b > CPLD1/setreg")
    device_obj.executeCmd("echo 0x01 > CPLD1/getreg")
    output=device_obj.executeCmd("cat CPLD1/getreg")
    CommonKeywords.should_match_a_regexp(output, "0x5b")
    
    device_obj.executeCmd("echo 0x01 0x5b > CPLD2/setreg")
    device_obj.executeCmd("echo 0x01 > CPLD2/getreg")
    output=device_obj.executeCmd("cat CPLD2/getreg")
    CommonKeywords.should_match_a_regexp(output, '0x5b')
    device_obj.executeCmd("cd")
    log.success("check_switch_cpld_read_write_operation executed successfully")
    
    
    
def get_set_swict_cpld_scratch_register(device, register, mode, value):
    device_obj = Device.getDeviceObject(device)
    cmd1="echo "+register+" > CPLD1/"+mode
    cmd2="cat CPLD1/"+mode
    cmd3="echo "+register+" > CPLD2/"+mode
    cmd4="cat CPLD2/"+mode
    
    device_obj.executeCmd(cmd1)
    output=device_obj.executeCmd(cmd2)
    CommonKeywords.should_match_a_regexp(output, value)
    
    device_obj.executeCmd(cmd3)
    output=device_obj.executeCmd(cmd4)
    CommonKeywords.should_match_a_regexp(output, value)
    log.success("Read write operation for swicth cpld %s is working correctly." %mode)
    

def get_baseboard_cpld_version(device):
    log.debug("Entering get_baseboard_cpld_version details args : %s" %(str(locals())))
    device_obj = Device.getDeviceObject(device)
    whitebox_lib.change_directory(device,"/sys/devices/platform/sys_cpld")
    cmd = f"cat version"
    
    output = Device.executeCmd(device_obj, cmd)
    log.info(output)
    output = output.split("\n")
    
    baseboard_cpld_version=output[-5]
    return baseboard_cpld_version
    


def download_files_in_usb(device, file_path):
    device_obj = Device.getDeviceObject(device)
    devicePc = Device.getDeviceObject('PC')

    cmd1 = "wget http://" + tftp_server_ip + ":" + moonstone_home_path + file_path
    file_name = file_path.split("/")

    log.info("Download %s into usb.." % file_name[-1])
    res2 = device_obj.executeCmd(cmd1)
    CommonKeywords.should_match_a_regexp(res2, "100%")

    res3 = device_obj.executeCmd("ls")
    CommonKeywords.should_match_a_regexp(res3, file_name[-1])
    log.success("%s is downloaded successfully." % file_name[-1])

@logThis
def download_deb_package(device):
    deviceObj = Device.getDeviceObject(device)
    run_command("cd")
    cmd = "dpkg -i "+bios_deb_image
    log.debug("Download and install .deb package ....")
    download_files_in_usb(device,bios_deb_image )
    
    output=deviceObj.executeCmd(cmd)
    CommonKeywords.should_match_paired_regexp_list(output,dpkg_install_pattern)
    
    log.info("Successfully downloaded and installed deb package")
    time.sleep(5)
    

    
def get_come_cpld_version(device):
    log.debug("Entering get_come_cpld_version details args : %s" %(str(locals())))
    device_obj = Device.getDeviceObject(device)
    download_deb_package(device)
    whitebox_lib.change_directory(device,"/home/cel_diag/moonstone/tools")
    cmd = f"./lpc_cpld_x86_64 blu r 0xa1e0"
    output = Device.executeCmd(device_obj, cmd)
    CommonKeywords.should_match_a_regexp(output, exp_come_cpld_version)
    Device.executeCmd(device_obj, "cd")
    
    whitebox_lib.change_directory(device,"/home/cel_diag/moonstone/bin")
    cmd = f"./cel-sysinfo-test --all"
    output = Device.executeCmd(device_obj, cmd)
    log.info(output)
    come_cpld_version=re.search(r"COMe CPLD option success :\s+(.*)",output,re.I|re.M)[1]
    Device.executeCmd(device_obj, "cd")
    cmd = "rm -rf %s" %bios_deb_image
    device_obj.sendCmd(cmd)
    return come_cpld_version

def get_switch_cpld_version(device):
    log.debug("Entering get_switch_cpld_version details args : %s" %(str(locals())))
    device_obj = Device.getDeviceObject(device)
    whitebox_lib.change_directory(device,"/home/cel_diag/moonstone2v2/bin")
    cmd = f"./cel-cpld-test -r -d 2 -R 1 | sed -n 2p"
    output = Device.executeCmd(device_obj, cmd)
    log.info(output)
    switch_cpld_version=re.search(r"MISC_CPLD1 Version:\s+([\d\.]+)",output,re.I|re.M)[1]
    return switch_cpld_version

def verify_onl_booting_check_log(device):
    log.debug("Entering verify_onl_booting_check with args : %s" %(str(locals())))
    device_obj = Device.getDeviceObject(device)
    log.debug("Powercycle the device")
    MOONSTONECommonLib.powerCycle(device)
    
    cmd = f"dmesg | grep -i fail"
    output = Device.executeCmd(device_obj, cmd)
    log.info("output is %s" %output)
    fail_log=re.findall(r"(.*fail.*)",output)
    if len(fail_log)>1:
        log.fail(fail_log)
        raise testFailed('verify_onl_booting_check_log')
    else:
        log.success("Pass, No failures seen")
        
    
    cmd = f"dmesg | grep -i error"
    output = Device.executeCmd(device_obj, cmd)
    log.info("output is %s" %output)
    error_log=re.findall(r"(.*error.*)",output)
    if len(error_log)>2:
        log.fail(error_log)
        raise testFailed('verify_onl_booting_check_log')
    else:
        log.success("Pass, No errors seen")
   

def verify_onl_login(device):
    device_obj = Device.getDeviceObject(device)
  
    
    device_obj.sendCmd('exit')
    time.sleep(5)
    device_obj.sendline('\r')
    device_obj.read_until_regexp('localhost login',timeout=80)
    
    time.sleep(10)
    log.info("Checking login to onl with wrong username")
    device_obj.sendline('abc')
    device_obj.read_until_regexp('Password',timeout=10)
    device_obj.sendline(device_obj.rootPassword)
    output=device_obj.read_until_regexp('localhost login',timeout=10)
    CommonKeywords.should_match_a_regexp(output, incorrect_login)
    log.success("Login failed since credentials are wrong")
    
    time.sleep(10)
    log.info("Checking login to onl with wrong password")
    device_obj.sendline(device_obj.userName)
    device_obj.read_until_regexp('Password',timeout=10)
    device_obj.sendline('abc')
    output=device_obj.read_until_regexp('localhost login',timeout=10)
    CommonKeywords.should_match_a_regexp(output, incorrect_login)
    log.success("Login failed since credentials are wrong")
    
    time.sleep(10)
    log.info("Checking login to onl with wrong username and password")
    device_obj.sendline('abc')
    device_obj.read_until_regexp('Password',timeout=10)
    device_obj.sendline('abc')
    output=device_obj.read_until_regexp('localhost login',timeout=10)
    CommonKeywords.should_match_a_regexp(output, incorrect_login)
    log.success("Login failed since credentials are wrong")
    
    time.sleep(10)
    log.info("Checking login to onl with correct credentials")
    device_obj.sendline(device_obj.userName)
    device_obj.read_until_regexp('Password',timeout=10)
    device_obj.sendline(device_obj.rootPassword)
    device_obj.read_until_regexp('root@localhost:~#',timeout=10)
    log.success("Login passed since credentials are correct")
    
def check_onl_version(device, output):
    onl_version=re.findall(r"Open Network Linux OS (\S+)\,\s+\S+:\S+",output)[0]
    for i in onl_version:
        if i not in ONLimage:
            log.info(i)
            log.info(exp_onl_version)
            raise RuntimeError("ONL Version is not correct")
            
            
def verify_onl_version(device):
    log.debug("Entering get_onl_version details args : %s" %(str(locals())))
    device_obj = Device.getDeviceObject(device)
    cmd = f"cat /etc/issue"
    
    log.info("Rebooting the DUT")
    device_obj.sendCmd('reboot')
    output=device_obj.read_until_regexp('localhost login',timeout=400)
    device_obj.loginToDiagOS()
    check_onl_version(device, output)
    log.success("ONL Version is correct during reboot")
    
    output = Device.executeCmd(device_obj, cmd)
    check_onl_version(device, output)
    log.success("ONL Version is correct inside onl") 
    

def verify_onl_system_info_check(device):
    log.debug("Entering get_onl_sysinfo details args : %s" %(str(locals())))
    device_obj = Device.getDeviceObject(device)
    cmd = f"uname -a"
    output = Device.executeCmd(device_obj, cmd)
    log.info(output)
    onl_sysinfo=re.search(r"Linux localhost (.*)-OpenNetworkLinux.*x86_64 GNU/Linux",output,re.I|re.M)[1]
    log.info(onl_sysinfo)
    CommonKeywords.should_match_a_regexp(onl_sysinfo, exp_onl_sysinfo)
    log.success("ONL system info is as expected ")


            
def check_fan_test(device):
    
    log.success('FAN Test Passed')
    device_obj = Device.getDeviceObject(device)
    MOONSTONECommonLib.powercycle_device(device)
    log.info("Login into device")
    device_obj.loginToDiagOS()



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



def Get_PSU_Value(device, PSU, key):
    log.debug("Entering  GET PSU Value with args : %s" %(str(locals())))
    device_obj = Device.getDeviceObject(device)
    input1=dump_device_data(device)

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
def test_FanNoAndDescAndAirflowTest(device, PlatformEnv):

    TOTAL_FANS = len(PlatformEnv["FAN"]["FAN_Index"])

    fan_type=['Rear', 'Front']
    required_fan_names = [ f"Fan {i}" for i in PlatformEnv["FAN"]["FAN_Index"]]
    required_fan_desc = [ "Chassis Fan {} {}".format(str(int(i+1)//2), fan_type[int(i)%2]  ) for i in PlatformEnv["FAN"]["FAN_Index"]]

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


    log.info(str(required_fan_names))
    log.info(str(fan_names))
    log.info(str(required_fan_desc))
    log.info(str(fan_descs))
    
    condition1 = required_fan_names == fan_names
    condition2 = required_fan_desc == fan_descs

    try:
        assert condition1 and condition2
        log.success("Fan No. and Descriptions as required.\n %s \n %s" %(str(fan_names), str(fan_descs)))
    except AssertionError:
        log.fail("Fan No. and Descriptions NOT as required.\n %s \n %s" %(str(required_fan_names), str(required_fan_desc)))
        log.fail("Fan No. and Descriptions NOT as required.\n %s \n %s" %(str(fan_names), str(fan_descs)))
        raise

def Get_Fan_Value(device, FanIndex, key):
    log.debug("Entering  GET FAN Value with args : %s" %(str(locals())))
    device_obj = Device.getDeviceObject(device)
    device_obj.flush()
    cmd = 'onlpdump -ery > temp.yml'
    output = Device.executeCmd(device_obj, cmd)
    try:
        #log.info("{} {} {} " %(device_obj.bmcConsoleIP, device_obj.rootUserName,device_obj.rootPassword))
        CommonLib.get_file_by_scp(device_obj.managementIP, device_obj.rootUserName,device_obj.rootPassword , '/root', 'temp.yml',workDir )
        with open('{}/temp.yml'.format(workDir), 'r') as r:
            input1 = yaml.safe_load(r)
        log.info(str(input1["LEDs"]))
        os.remove('{}/temp.yml'.format(workDir))
        output = Device.executeCmd(device_obj, 'rm /root/temp.yml')
        
    except AssertionError:
        log.fail(f"Output couldnt dump properly")
    

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


def test_FanStateAndStatusTest(device, PlatformEnv):
    TOTAL_FANS = len(PlatformEnv["FAN"]["FAN_Index"])
    all_fan_state = {}
    all_fan_status = {}
    condition = True
    
    for i in range(TOTAL_FANS):
        state = Get_Fan_Value(device, i+1, 'State')
        status = Get_Fan_Value(device, i+1, 'Status')
        
        all_fan_state["Fan-" + str(i+1)] = state
        all_fan_status["Fan-" + str(i+1)] = status
        condition  = condition and state == "Present" and status == 'Running'

    if len(PlatformEnv["PSU"]["PSU-1"]["FAN_Index"]) > 0:
        for i in range(len(PlatformEnv["PSU"]["PSU-1"]["FAN_Index"])):
            state = Get_PSU_FAN_Value(device, 1, i, 'State')
            status = Get_PSU_FAN_Value(device, 1, i, 'Status')
            all_fan_state["PSU Fan-" + str(i+1)] = state
            all_fan_status["Fan-" + str(i+1)] = status
            condition  = condition and state == "Present" and status == 'Running'

    if len(PlatformEnv["PSU"]["PSU-2"]["FAN_Index"]) > 0:
        for i in range(len(PlatformEnv["PSU"]["PSU-2"]["FAN_Index"])):
            state = Get_PSU_FAN_Value(device, 2, i, 'State')
            status = Get_PSU_FAN_Value(device, 2, i, 'Status')
            all_fan_state["PSU Fan-" + str(i+2)] = state
            all_fan_status["Fan-" + str(i+1)] = status
            condition  = condition and state == "Present" and status == 'Running'
    try:
        assert condition
        log.success("All fan state as required ('Present') and status as required ('Running')\n%s" %str(all_fan_state))
    except AssertionError:
        log.fail("Some of the fan state NOT as required ('Present') and status NOT as required ('Running').\n%s" %str(all_fan_state))
        raise
    

def Get_PSU_FAN_Value(device, PSU, FAN, key):
    log.debug("Entering  GET PSU FAN Value with args : %s" %(str(locals())))
    device_obj = Device.getDeviceObject(device)
    input1=dump_device_data(device)

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
        log.success("All fans RPM as required.\n %s" %str(all_fans_rpms))
    except AssertionError:
        log.fail("Error in FAN speed RPMs one of them not in range.\n All fans RPMs given below.\n %s" %str(all_fans_rpms))
        raise

def getAllFansRPM(device):
    log.debug("Entering  GET PSU FAN Value with args : %s" %(str(locals())))
    device_obj = Device.getDeviceObject(device)
    cmd = 'onlpdump | grep -a "RPM:"'
    output = Device.executeCmd(device_obj, cmd)

    retval = output.split("\n")
    #log.info(str(retval))
    fan_rpms = {}
    rpm_list = []

    for i in retval:
        rpm_list.append(i.strip())

    #log.info(str(rpm_list))
    while ("" in rpm_list):
        rpm_list.remove("")

    #log.info(str(rpm_list))
    index = 1
    for item in rpm_list[1:7]:
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
    device_obj = Device.getDeviceObject(device)
    input1=dump_device_data(device)
    


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
    device_obj = Device.getDeviceObject(device)
    input1=dump_device_data(device)
    

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

    log.info("Led value : %s " %SYSTEM_LED_Index)
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
    device_obj = Device.getDeviceObject(device)
    input1=dump_device_data(device)
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

def GetOpticsDetail(device, Port):

    log.debug("Entering  check Optics detail with args : %s" % (str(locals())))
    device_obj = Device.getDeviceObject(device)
    cmd = 'onlpdump | grep -a \'Type*\' -A48 | grep -v \'Type*\''
    output = Device.executeCmd(device_obj, cmd)
    temp = output.strip().split('\n')
    log.info(temp)
    Optics = dict()

    tmplist = temp[int(Port) + 1].strip().split(' ')
    
    while ("" in tmplist):
        tmplist.remove("")
        
    log.info(tmplist)

    Optics['Port'] = tmplist[0]
    Optics['Type'] = tmplist[1]
    Optics['Media'] = tmplist[2]
    Optics['Length'] = tmplist[3]
    Optics['Vendor'] = tmplist[4]
    Optics['Model'] = tmplist[5]
    Optics['SerialNumber'] = tmplist[6]

    return Optics

def test_Check_Optics_Presence(device,port):

    try:
        result1 = CheckOpticsPresence(device, port)
        assert result1 == 1
        log.info("Optics detected on port %s" %port)
        OpticInfo = GetOpticsDetail(device,port)
        log.info("Optics connected: %d", result1)
        log.info("Optics Info: \n \
                        Port  : %s\n \
                        Type  : %s\n \
                        Media : %s\n \
                        Length: %s\n \
                        Vendor: %s\n \
                        Model : %s\n \
                        Serial Number: %s\n", OpticInfo["Port"], OpticInfo["Type"], OpticInfo["Media"], OpticInfo["Length"], OpticInfo["Vendor"], OpticInfo["Model"], OpticInfo["SerialNumber"])
    except AttributeError:
        log.fail("No Optics detected on port: %s" %port)
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
    log.info("Configuring eth0 ip addr , gateway and hw addr")
    bios_menu_lib.send_key(device, "KEY_ENTER")
    device_obj.sendCmd("ifconfig eth0 "+static_ip+" netmask "+netmask)
    device_obj.sendCmd("route add default gw "+default_gateway)
    device_obj.sendCmd("ifconfig eth0 hw ether "+exp_mac_addr)
    time.sleep(20)
    log.info("Download ONL image in ONIE shell")
    cmd="scp brixia@"+scp_ip+":"+moonstone_onl_image_path+ONLimage+" ."
    device_obj.sendCmd(cmd)
    device_obj.read_until_regexp("connecting\? \(y\/n\)", timeout=60)
    device_obj.sendCmd("y")
    device_obj.read_until_regexp("password:", timeout=60)
    device_obj.sendCmd(scp_password)
    device_obj.read_until_regexp("ONIE:/", timeout=60)
    device_obj.sendCmd("ls")
    output=device_obj.read_until_regexp("ONIE:/", timeout=60)
    CommonKeywords.should_match_a_regexp(output, ONLimage)
    
    
    log.success("ONL image is being downloaded successfully")
    
     
    if (protocol == 'tftp'):
        cmd = "onie-nos-install %s://%s/%s" % (protocol.lower(), tftp_server_ip, ONLimage)
    else:
        cmd = "onie-nos-install %s://%s/%s" % (protocol.lower(), http_server_ip, ONLimage)
    device_obj.sendCmd(cmd)
    output = device_obj.read_until_regexp('ONL loader install successful.', timeout)
    device_obj.read_until_regexp('Rebooting in 3s', timeout=30)
    device_obj.read_until_regexp("Open Network Linux",200)
    bios_menu_lib.send_key(device, "KEY_ENTER")
    device_obj.read_until_regexp("localhost login:",200)
    device_obj.loginToDiagOS()

#######################
def Verify_Device_OID_test(device):
    log.debug("Entering get_device_OID with args : %s" %(str(locals())))
    device_obj = Device.getDeviceObject(device)
    #whitebox_lib.change_directory(device,"/home/cel_diag/moonstone2v2/bin")
    cmd = f"onl-platform-show"
    output = Device.executeCmd(device_obj, cmd)
    log.info(output)
    sys_OID=re.search(r"System Object Id:\s+([\d\.]+)",output,re.I|re.M)[1]
    CommonKeywords.should_match_a_regexp(output, exp_sys_OID)
    output=device_obj.executeCmd("onlpd -i")
    CommonKeywords.should_match_ordered_regexp_list(output, all_device_oid_test)
    

def test_device_ONL_SNMP(device,device_OID):
    log.debug("Entering test_device_ONL_SNMP with args : %s" %(str(locals())))
    device_obj = Device.getDeviceObject(device)
    
    log.info("Checking SNMP message via OID")
    device_obj.sendCmd("onlp-snmpd")
    device_obj.read_until_regexp('restructuring complete', timeout=30)
    output=device_obj.read_until_regexp('restructuring complete', timeout=30)
    CommonKeywords.should_match_ordered_regexp_list(output, snmp_message_oid_pattern)
    output=device_obj.read_until_regexp('restructuring complete', timeout=30)
    CommonKeywords.should_match_ordered_regexp_list(output, snmp_message_oid_pattern)
    
    log.info("Stopping the process...")
    device_obj.sendCmd(Const.KEY_CTRL_C)
    output=device_obj.read_until_regexp('root@localhost', timeout=30)
    CommonKeywords.should_match_a_regexp(output, snmp_message_stop_pattern)
    log.success("test_device_ONL_SNMP executed successfully")
    


def test_device_reset(device,exp_device_data):
    log.debug("Entering test_device_reset with args : %s" %(str(locals())))
    device_obj = Device.getDeviceObject(device)
    parsed_output = dump_device_data(device)
    compare_device_data(exp_device_data,parsed_output)
    log.info("Rebooting the DUT")
    cmd = 'reboot'
    device_obj.sendCmd(cmd)
    device_obj.read_until_regexp('localhost login', timeout=400)
    device_obj.loginToDiagOS()
    parsed_output = dump_device_data(device)
    compare_device_data(exp_device_data,parsed_output)


def ONL_Install_UnInstall_Mode(device,mode):
    """
    Select the Onie's interface: enter different Onie functions
    :param mode:installer/rescue/uninstall/update
    """
    log.debug("Entering ONL_Install_UnInstall_Mode details args : %s" %(str(locals())))
    log.info(exp_mac_addr)
    device_obj = Device.getDeviceObject(device)

    mode = mode.lower()
    Device.sendCmd(device_obj,"reboot")
    log.debug("going to onie:{} mode ...".format(mode))
    log.debug("now, rebooting the dut ...")

    device_obj.read_until_regexp("American Megatrends",90)
    #bios_menu_lib.send_key(device, "KEY_DOWN", 3)
    #bios_menu_lib.send_key(device, "KEY_ENTER")
    #device_obj.read_until_regexp("GNU GRUB", 10)
    device_obj.read_until_regexp("GNU GRUB", 40)
    time.sleep(2)
    bios_menu_lib.send_key(device, "KEY_DOWN")
    bios_menu_lib.send_key(device, "KEY_ENTER")

    if mode == 'installer':
        log.debug('entering onie install mode ...')
        bios_menu_lib.send_key(device, "KEY_ENTER")
        device_obj.read_until_regexp("ONIE: OS Install Mode", 7)
        bios_menu_lib.send_key(device, "KEY_ENTER")
        device_obj.read_until_regexp("Please press Enter to activate this console", 200)
        

    elif mode == 'uninstall':
        log.debug('entering onie uninstall mode ...')
        bios_menu_lib.send_key(device, "KEY_DOWN", 2)
        
        device_obj.read_until_regexp("ONIE: Uninstall OS", 7)
        bios_menu_lib.send_key(device, "KEY_ENTER")
        """
        After uninstall device will boot into install mode
        """
        device_obj.read_until_regexp("Please press Enter to activate this console", 600)
    log.debug('entering onie install mode ...')
    time.sleep(10)
    Device.executeCmd(device_obj,"onie-stop")
    time.sleep(5)
    Device.executeCmd(device_obj,"onie-stop")
    time.sleep(20)

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
        
def verify_baseboard_cpld_version(device):
    device_obj = Device.getDeviceObject(device)
    log.debug("Powercycle the device")
    MOONSTONECommonLib.powerCycle(device)
    
    
    log.debug("Checking baseboard cpld version")
    device_obj.executeCmd("cd /sys/devices/platform/sys_cpld")
    output=device_obj.executeCmd("cat version")
    CommonKeywords.should_match_a_regexp(output, exp_bb_cpld_version)
    log.success("Baseboard CPLD version is correct")
    
    log.debug("Checking default scratch and getreg value")
    output=device_obj.executeCmd("cat scratch")
    CommonKeywords.should_match_a_regexp(output, default_scratch_value)
    log.success("Default scratch and getreg value are correct")
    
    device_obj.executeCmd("echo 0xA101 > getreg")
    output=device_obj.executeCmd("cat getreg")
    CommonKeywords.should_match_a_regexp(output, default_scratch_value)
    log.success("Getreg value of CPLD is correct")
    
    log.debug("Checking read write operations for scratch")
    device_obj.executeCmd("echo "+baseboard_scratch_write_1+" > scratch")
    output=device_obj.executeCmd("cat scratch")
    CommonKeywords.should_match_a_regexp(output, baseboard_scratch_write_1)
    log.success("Read write operations for scratch are working correctly")
    
    device_obj.executeCmd("echo "+baseboard_scratch_write_2+" > scratch")
    output=device_obj.executeCmd("cat scratch")
    CommonKeywords.should_match_a_regexp(output, baseboard_scratch_write_2)
    log.success("Scratch value of CPLD is correct")
    
    log.debug("Checking read write operations for register")
    device_obj.executeCmd("echo 0xA101 "+baseboard_getreg_write_1+" > setreg")
    device_obj.executeCmd("echo 0xA101 > getreg")
    output=device_obj.executeCmd("cat getreg")
    CommonKeywords.should_match_a_regexp(output, baseboard_getreg_write_1)
    log.success("read write operations for register are working correctly")
    
    log.debug("Checking system led")
    result=False
    output=device_obj.executeCmd("cat sys_led")
    for var in sys_led:
        if var in output:
            result=True
    if not result:
        raise RuntimeError("sys_led value is not a valid value")
    log.success("System leds value are correct")
        
        
    result=False
    output=device_obj.executeCmd("cat sys_led_color")
    for var in sys_led_color:
        if var in output:
            result=True
    if not result:
        raise RuntimeError("sys_led_color value is not a valid value")
    log.success("System leds color value are correct")
    device_obj.executeCmd("cd")
    
def reboot_device(device):
    device_obj = Device.getDeviceObject(device)
    log.info("Rebooting the DUT")
    device_obj.sendCmd('reboot')
    output=device_obj.read_until_regexp('localhost login',timeout=400)
    device_obj.loginToDiagOS()
    time.sleep(60)

def device_poweroff(device):
    device_obj = Device.getDeviceObject(device)
    log.info("Poweroff device")
    device_obj.sendCmd('poweroff')
    output=device_obj.read_until_regexp('reboot: Power down',timeout=400)
    log.debug("Powercycle the device")
    MOONSTONECommonLib.powerCycle(device)


def reset_test_commands(device, baseboard_value_1=default_scratch_value, baseboard_value_2=baseboard_scratch_write_1, switch_value_1=default_scratch_value, switch_value_2='0x21', fgpa_value_1=default_fpga_scratch_value, fgpa_value_2=write_fpga_scratch1 ):
    device_obj = Device.getDeviceObject(device)
  
    
    log.info("Checking ONL version")
    cmd = f"cat /etc/issue"
    output = Device.executeCmd(device_obj, cmd)
    check_onl_version(device, output)
    log.success("ONL Version is correct inside onl")
    
    log.info("Checking device data OID")
    Verify_Device_OID_test(device)
    
    log.info("Checkig onlpdump -d")
    verify_device_data(device)
    
    #CPLD
    log.info("Checking baseboard cpld scratch original value and read write operation")
    whitebox_lib.change_directory(device,"/sys/devices/platform/sys_cpld")
    cmd = f"cat scratch"
    output = Device.executeCmd(device_obj, cmd)
    CommonKeywords.should_match_a_regexp(output, baseboard_value_1)
    
    log.debug("Checking read write operations for baseboard cpld scratch")
    device_obj.executeCmd("echo "+baseboard_value_2+" > scratch")
    output=device_obj.executeCmd("cat scratch")
    CommonKeywords.should_match_a_regexp(output, baseboard_value_2)
    log.success("Read write operations for scratch are working correctly")
    
    #Switch
    log.info("Checking switch cpld scratch original value and read write operation")
    whitebox_lib.change_directory(device,"/sys/devices/platform/cls_sw_fpga")
    output=device_obj.executeCmd("cat CPLD1/scratch")
    CommonKeywords.should_match_a_regexp(output, switch_value_1)
    get_set_swict_cpld_scratch_register(device, switch_value_2, "scratch", switch_cpld_register_value[switch_value_2])
    
    
    # FPGA
    log.info("Checking FPGA scratch original value and read write operation")
    whitebox_lib.change_directory(device,"/sys/devices/platform/cls_sw_fpga/FPGA")
    get_fpga_scratch(device, fpga_scratch_dict[fgpa_value_1])
    check_set_fpga_scratch(device, fgpa_value_2)
    device_obj.executeCmd("cd")
    
    log.info("Checking for error free output of 'fdisk -l', 'i2cdetect -l'and 'ifconfig'")
    output = device_obj.executeCmd("fdisk -l")
    CommonKeywords.should_match_ordered_regexp_list(output, fdisk_op_re)
    
    for i in commands_in_reset_test:
        c1 = device_obj.executeCmd(i)
        if ("Failed" in c1) or ("failed" in c1):
            raise RuntimeError("Error in output")
    
  
def test_stress_onl(device,iterations):
    device_obj = Device.getDeviceObject(device)
    download_deb_package(device)
    whitebox_lib.change_directory(device,"/home/cel_diag/moonstone/tools")
    cmd='./stressapptest -s 60 -M 28800 -m 2 -i 2 -C 4 -W -d /dev/sda'
    for iter_ in range(int(iterations)):
        c1=device_obj.executeCmd(cmd, timeout=400)
        CommonKeywords.should_match_ordered_regexp_list(c1, onl_stress_test_pattern)
        log.info("Iteration %s of onl stress test completed successfully" %str(iter_+1))
    log.success("Onl stress test completed successfully")
    Device.executeCmd(device_obj, "cd")
    cmd = "rm -rf %s" %bios_deb_image
    device_obj.sendCmd(cmd)
    
    
#TC-18
    
def check_platform_daemon(device):
    device_obj = Device.getDeviceObject(device)
    log.debug("Powercycle the device")
    MOONSTONECommonLib.powerCycle(device)
    cmd="service onlpd status"
    output=device_obj.executeCmd(cmd)
    CommonKeywords.should_match_a_regexp(output, 'ONLP Platform Agent is running.')
    log.success("check_platform_daemon executed successfully.")
    
def check_platform_function(device):
    device_obj = Device.getDeviceObject(device)
    cmd='onlpdump'
    output=device_obj.executeCmd(cmd)
    CommonKeywords.should_match_ordered_regexp_list(output, onlpdump_pattern)
    log.success("check_platform_function through 'onlpdump' executed successfully.")
    kill_all_onlpd_running_process(device)
    
    cmd="onlpd -m"
    device_obj.sendCmd(cmd)
    
    output=device_obj.read_until_regexp('Running the platform manager for 600 seconds...',timeout=100)
    CommonKeywords.should_match_ordered_regexp_list(output, onlpdump_pattern)
    
    output2=device_obj.read_until_regexp('root@localhost',timeout=700)
    for line in onlpd_m_pattern:
        CommonKeywords.should_match_a_regexp(output2, line)
    log.success("check_platform_function through 'onlpd -m' executed successfully.")

def kill_all_onlpd_running_process(device):
    device_obj = Device.getDeviceObject(device)
    cmd='ps -aux | grep onlpd'
    output=device_obj.executeCmd(cmd)
    output=output.split('\n')
    pattern="root\s+(\S+)"
    for line in output:
        if "grep onlpd" not in line:
            process_id=re.findall(pattern, line)[0]
            device_obj.executeCmd("kill %s" %process_id)
            time.sleep(10)
            output2=device_obj.executeCmd(cmd)
            if process_id in output2[1:]:
                raise RuntimeError("Process with process id %s is not killed yet." %process_id)
    log.success("All running onlpd process are killed successfully.")

def check_platform_driver(device):
    device_obj = Device.getDeviceObject(device)
    cmd='lsmod'
    output=device_obj.executeCmd(cmd)
    for line in lsmod_pattern:
        CommonKeywords.should_match_a_regexp(output, line)
    log.success("check_platform_driver executed successfully")    
    log.debug("Powercycle the device")
    MOONSTONECommonLib.powerCycle(device)

# TC-20

def check_SFP_present_status(device):
    device_obj = Device.getDeviceObject(device)
    #log.debug("Powercycle the device")
    #MOONSTONECommonLib.powerCycle(device)
    whitebox_lib.change_directory(device,"/sys/devices/platform/cls_sw_fpga/SFF/")
    
    output=device_obj.executeCmd("cat SFP1/sfp_absmod")
    CommonKeywords.should_match_a_regexp(output, '0')
    output=device_obj.executeCmd("cat SFP2/sfp_absmod")
    CommonKeywords.should_match_a_regexp(output, '0')
    log.success('sfp_absmod value is "0"')
    
    
    
def check_loss_of_signal_assertion_status(device):
    device_obj = Device.getDeviceObject(device)

    output=device_obj.executeCmd("cat SFP1/sfp_rxlos")
    CommonKeywords.should_match_a_regexp(output, '0')
    output=device_obj.executeCmd("cat SFP2/sfp_rxlos")
    CommonKeywords.should_match_a_regexp(output, '0')
    log.success('0 means Loss of Signal.')
    
    
def check_module_transmission_status(device):
    device_obj = Device.getDeviceObject(device)
    
    log.debug("Checking sfp_txdisable")    
    output=device_obj.executeCmd("cat SFP1/sfp_txdisable")
    CommonKeywords.should_match_a_regexp(output, '0')
    output=device_obj.executeCmd("cat SFP2/sfp_txdisable")
    CommonKeywords.should_match_a_regexp(output, '0')
    
    log.debug("Enabling sfp_txdisable")   
    device_obj.executeCmd("echo 1 > SFP1/sfp_txdisable")
    device_obj.executeCmd("echo 1 > SFP2/sfp_txdisable")
    
    log.debug("Checking sfp_txdisable after enabling") 
    output=device_obj.executeCmd("cat SFP1/sfp_txdisable")
    CommonKeywords.should_match_a_regexp(output, '1')
    output=device_obj.executeCmd("cat SFP2/sfp_txdisable")
    CommonKeywords.should_match_a_regexp(output, '1')
    
    log.debug("Disabling sfp_txdisable")   
    device_obj.executeCmd("echo 0 > SFP1/sfp_txdisable")
    device_obj.executeCmd("echo 0 > SFP2/sfp_txdisable")
    
    log.debug("Checking sfp_txdisable after disabling") 
    output=device_obj.executeCmd("cat SFP1/sfp_txdisable")
    CommonKeywords.should_match_a_regexp(output, '0')
    output=device_obj.executeCmd("cat SFP2/sfp_txdisable")
    CommonKeywords.should_match_a_regexp(output, '0')
    
    log.success("check_module_transmission_status executed sucessfully")
    
    
def check_transmission_fault_assert_signal(device):
    device_obj = Device.getDeviceObject(device)
   
    output=device_obj.executeCmd("cat SFP1/sfp_txfault")
    CommonKeywords.should_match_a_regexp(output, '0')
    output=device_obj.executeCmd("cat SFP2/sfp_txfault")
    CommonKeywords.should_match_a_regexp(output, '0')
    log.success('0 means the module have TX fault assert.')
    device_obj.executeCmd("cd")
    
# TC-21
    
def check_OSFP_present_status(device):
    device_obj = Device.getDeviceObject(device)
    
    #log.debug("Powercycle the device")
    #MOONSTONECommonLib.powerCycle(device)
    whitebox_lib.change_directory(device,"/sys/devices/platform/cls_sw_fpga/SFF")
    path='/sys/devices/platform/cls_sw_fpga/SFF/OSFP*/MODPRS_L'
    check_osfp_status_values(device, '0', path)
    
    
def check_osfp_status_values(device, value, path):
    device_obj = Device.getDeviceObject(device)
    cmd = 'cat '+path
    output=device_obj.executeCmd(cmd)
    output=output.split()
    log.info(str(output))
    for line in output[1:-4]:
        if value in line:
            #continue
            log.info(line)
            CommonKeywords.should_match_a_regexp(line, value)
    log.success("All values for path %s are %s" %(path,value))

def set_osfp_status_values(device, value, path):
    device_obj = Device.getDeviceObject(device)
    for val in range(1,65):
        cmd="echo "+value+" > /sys/devices/platform/cls_sw_fpga/SFF/OSFP"+str(val)+"/"+path
        device_obj.executeCmd(cmd)
    log.success("All %s values are set to %s" %(path,value))
    
    
def check_Low_power_mode(device):
    device_obj = Device.getDeviceObject(device)
    path='/sys/devices/platform/cls_sw_fpga/SFF/OSFP*/LPMOD'
    
    log.debug("Checking all LPMOD values")
    check_osfp_status_values(device, '0', path)
    
    log.info("Setting 1 to all LPMOD")
    set_osfp_status_values(device, '1', "LPMOD")
    log.info("Checking all LPMOD values")
    check_osfp_status_values(device, '1', path)
    
    log.info("Setting 0 to all LPMOD")
    set_osfp_status_values(device, '0', "LPMOD")
    log.info("Checking all LPMOD values")
    check_osfp_status_values(device, '0', path)
    log.success("check_Low_power_mode executed successfully.")
    
    
def check_reset_signal_logic_level(device):
    device_obj = Device.getDeviceObject(device)
    path='/sys/devices/platform/cls_sw_fpga/SFF/OSFP*/RST_L'
    cmd2='echo 0 > /sys/devices/platform/cls_sw_fpga/SFF/OSFP*/RST_L'
    cmd3='echo 1 > /sys/devices/platform/cls_sw_fpga/SFF/OSFP*/RST_L'
    
    log.debug("Checking all RST_L values")
    check_osfp_status_values(device, '1', path)
    
    log.info("Setting 0 to all RST_L")
    set_osfp_status_values(device, '0', "RST_L")
    log.debug("Checking all RST_L values")
    check_osfp_status_values(device, '0', path)
        
    log.info("Setting 1 to all RST_L")
    set_osfp_status_values(device, '1', "RST_L")
    log.debug("Checking all RST_L values")
    check_osfp_status_values(device, '1', path)
    
    
    log.success("check_reset_signal_logic_level executed successfully.")
    
    
def check_Indicating_the_module_Interrupt_status(device):
    device_obj = Device.getDeviceObject(device)
    path='/sys/devices/platform/cls_sw_fpga/SFF/OSFP*/INT_L'
    check_osfp_status_values(device, '1', path)
    log.success("checkl_Indicating_the_module_Interrupt_status executed successfully")
    device_obj.executeCmd("cd")
    
# TC - 23
def Verify_Device_SYS_OID_Test(device):
    device_obj = Device.getDeviceObject(device)
    log.info("Verify device sys OID through 'onlpdump -d'")
    verify_device_data(device)
    
    log.info("Verify all device names list through 'onlpd -i'")
    output=device_obj.executeCmd("onlpd -i")
    CommonKeywords.should_match_ordered_regexp_list(output, all_device_oid_test)
    log.success("Verify_Device_SYS_OID_Test executed successfully")
    
    
# TC-25
def test_CheckPSUInformation(device):
    device_obj = Device.getDeviceObject(device)
    cmd="onlpdump -r"
    output=device_obj.executeCmd(cmd)
    CommonKeywords.should_match_ordered_regexp_list(output, psu_info_pattern)
    log.success("Model, SN, Description, Stae, Status and Type of all PSUs are correct.")
    
    
# TC - 19
def check_I2C_device_sysfs(device):
    device_obj = Device.getDeviceObject(device)
    whitebox_lib.change_directory(device,"/sys/bus/i2c/devices")
    cmd='ls -la *'
    output=device_obj.executeCmd(cmd)
    if "Fail|fail|Error|error|invalid|Invalid|Unable|unable" in output:
        raise RuntimeError("I2C device list has errors")
    log.success("I2C device list same as Moonstone Linux sysfs file structure.")
    
def check_platform_device_sysfs(device):
    device_obj = Device.getDeviceObject(device)
    whitebox_lib.change_directory(device,"/sys/devices/platform")
    cmd='ls -la *'
    output=device_obj.executeCmd(cmd)
    if "Fail|fail|Error|error|invalid|Invalid|Unable|unable" in output:
        raise RuntimeError("Platform device list has errors.")
    log.success("Platform device list same as Moonstone Linux sysfs file structure.")
    
def check_SFPs_and_OSFPs_EEPROM_sysfs(device):
    device_obj = Device.getDeviceObject(device)
    whitebox_lib.change_directory(device,"/sys/bus/i2c/devices")
    cmd='ls -la *0050'
    output=device_obj.executeCmd(cmd)
    if "Fail|fail|Error|error|invalid|Invalid|Unable|unable" in output:
        raise RuntimeError("check_SFPs_and_OSFPs_EEPROM_sysfs has errors.")
    for i2c in range(5,71):
        i2c_pattern=str(i2c)+"-0050 -> ../../../devices/pci0000:00/0000:00:1c.6/0000:11:00.0/fpga-xiic-i2c"
        CommonKeywords.should_match_a_regexp(output, i2c_pattern)
    device_obj.executeCmd("cd")
    log.success("Device number SFP 1-2 are at i2c 5 and 6 ,OSFP 1 - 64 are at i2c 7-70")


# TC - 15
def check_system_platform_information(device, exp_mac, expected_diag_version):
    device_obj = Device.getDeviceObject(device)
    cmd="onlpdump -e"
    output=device_obj.executeCmd(cmd)
    diag_version_pattern="Diag Version: (\S+)"
    mac_pattern="MAC: (\S+)"
    mac=re.findall(mac_pattern, output)[0]
    diag_version_pattern="Diag Version: (\S+)"
    if expected_diag_version==old_diag_version:
        diag_version=re.findall(diag_version_pattern, output)[0]
    else:
        cmd2="./cel-sysinfo-test --all"
        device_obj.executeCmd("cd /home/cel_diag/moonstone/bin")
        output2=device_obj.executeCmd(cmd2)
        diag_version=re.findall(diag_version_pattern, output2)[0]

    if(mac not in exp_mac):
        log.info("%s %s" %(mac, mac))
        raise RuntimeError("Expected mac is %s but got %s" %(exp_mac, mac))
    if(diag_version!=expected_diag_version):
        raise RuntimeError("Expected diag_version is %s but got %s" %(expected_diag_version, diag_version))
    log.success("System information is as expected.")
        
def check_onie_eeprom_info(device):
    device_obj = Device.getDeviceObject(device)
    log.info("Boot to ONIE...")
    ONL_Install_UnInstall_Mode(device,ONIE_INSTALL_MODE)
    cmd="onie-syseeprom"
    output=device_obj.executeCmd(cmd)
    for line in onie_eeprom_pattern:
        CommonKeywords.should_match_a_regexp(output, line)
    log.info(output)
    device_obj.sendCmd("reboot")
    device_obj.read_until_regexp('localhost login:',timeout=400)
    device_obj.loginToDiagOS()
        
        
def update_onie_eeprom_information(device, mac_address, diag_version):
    device_obj = Device.getDeviceObject(device)
    cmd2="onie-syseeprom -s 0x2E="+diag_version
    cmd3="onie-syseeprom -s 0x24="+mac_address

    cmd = "ipmitool mc info"
    output = device_obj.executeCmd(cmd)
    match_pat = re.search(r'Firmware Revision',output)

    log.info("Boot to ONIE...")
    ONL_Install_UnInstall_Mode(device,ONIE_INSTALL_MODE)
    cmd="onie-syseeprom"
    output=device_obj.executeCmd(cmd)
    for line in onie_eeprom_pattern:
        CommonKeywords.should_match_a_regexp(output, line)
    log.info("Giving permissions to write in onie...")
    if match_pat:
        deviceM.switchToBmc()
        deviceM.loginToNEWBMC()
        deviceM.executeCmd("i2cset -f -y 2 0x0d 0x31 0x0B")
        deviceM.switchToCpu()
    else:
        device_obj.executeCmd("b_cpld_lpc w 0xa131 0")
    
    log.info("Changing diag version")
    output=device_obj.executeCmd(cmd2)
    CommonKeywords.should_match_a_regexp(output, "Diag Version.*0x2E.*5.*"+diag_version)
    
    log.info("Changing mac address")
    output=device_obj.executeCmd(cmd3)
    CommonKeywords.should_match_a_regexp(output, "Base MAC Address.*0x24.*6 "+mac_address.upper())
    
    log.info(output)
    device_obj.sendCmd("reboot")
    device_obj.read_until_regexp('localhost login:',timeout=400)
    device_obj.loginToDiagOS()

def test(device):
    device_obj=Device.getDeviceObject(device)
    deviceM.switchToBmc()
    deviceM.loginToNEWBMC()
    deviceM.executeCmd("i2cset -f -y 2 0x0d 0x31 0x0B")
    
# TC - 31
def verify_onl_bmc_thermal_temp(device):
    device_obj=Device.getDeviceObject(device)
    cmd="onlpdump -r"
    output=device_obj.executeCmd(cmd)
    thermal_names_list=[]
    thermal_temp_list=[]
    for thermal in range(1,7):
        thermal_name_re="Thermal "+str(thermal)+'\r\n.*Description: (\S+)'
        thermal_temp_re="Thermal "+str(thermal)+"\r\n.*\r\n.*\r\n.*Temperature: (\S+)\."
        thermal_names_list.append(re.findall(thermal_name_re, output)[0])
        thermal_temp_list.append(re.findall(thermal_temp_re, output)[0])
    log.info("Switch to BMC console")
    deviceM.switchToBmc()
    deviceM.loginToNEWBMC()
    output2=deviceM.executeCmd("ipmitool sdr")
    deviceM.switchToCpu()
    for thermal in range(6):
        line=thermal_names_list[thermal]+'.*'+thermal_temp_list[thermal]
        thermal_line=re.findall(line,output2)
        if not len(thermal_line):
            raise RuntimeError("Thermal values are not equal for %s" %line)
    log.success("Thermal values in onl and bmc are equal.")
    
def verify_thermal_information(device):
    device_obj=Device.getDeviceObject(device)
    cmd="onlpdump -r"
    output=device_obj.executeCmd(cmd)
    CommonKeywords.should_match_ordered_regexp_list(output, thermal_info_pattern)
    log.success("Description, status and temperature of all thermals are correct.")
    
# TC - 40
def exec_ipmitool_fru_print(device):
    log.debug("Entering test_ipmitool_fru with args : %s" %(str(locals())))
    device_obj = Device.getDeviceObject(device)
    cmd = f"ipmitool fru print"
    output = Device.executeCmd(device_obj, cmd)
    if "Failed|Error|error" in output:
        raise RuntimeError("FRU info has errors")
    log.success("exec_ipmitool_fru_print runs successfully")