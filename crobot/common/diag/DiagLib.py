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
import time
import Logger as log
import CRobot
import sys
import os
from functools import partial
from Decorator import *
import re
import Logger as log
import CommonLib 
import CommonKeywords
import Const
import time
from Server import Server

from Diag_OS_variable import *
import datetime
from dataStructure import nestedDict, parser
from SwImage import SwImage
from pexpect import pxssh
import sys
import getpass

try:
    from Device import Device
    import DeviceMgr
    import Const
    import CommonLib
except Exception as err:
    log.cprint(str(err))

device = DeviceMgr.getDevice()

run_command = partial(CommonLib.run_command, deviceObj=device, prompt=device.promptDiagOS)
time.sleep(10)

class DiagLib:
    def __init__(self, device):
        self.device = DeviceMgr.getDevice()


    # connection related API
    def loginDevice(self):
        log.debug("Entering DiagLib class procedure: loginDevice")
        return self.device.login()


    def disconnectDevice(self):
        log.debug("Entering DiagLib class procedure: disconnectDevice")
        return self.device.disconnect()


    def ssh_login_bmc(self):
        CommonLib.ssh_login_bmc(Const.DUT)
        self.device = DeviceMgr.getDevice()


    def ssh_disconnect(self):
        CommonLib.ssh_disconnect(Const.DUT)
        self.device = DeviceMgr.getDevice()


    # power cycle related wrapper API
    def wpl_powerCycleDeviceToDiagOS(self):
        log.debug("Entering DiagLib class procedure: powerCycleDeviceToDiagOS")
        output = self.wpl_powerCycleDevice()
        output1 = self.wpl_waitForDiagPrompt()
        output += output1
        return output


    def wpl_powerCycleDeviceToOnie(self):
        log.debug("Entering DiagLib class procedure: powerCycleDeviceToOnie")
        output = self.wpl_powerCycleDevice()
        output1 = self.wpl_waitForOniePrompt()
        output += output1
        return output


    def wpl_powerCycleDeviceToCentOS(self):
        log.debug("Entering DiagLib class procedure: powerCycleDeviceToCentOS")
        output = self.wpl_powerCycleDevice()
        output1 = self.wpl_waitForCentOSPrompt()
        output += output1
        return output


    def wpl_powerCycleDeviceToOpenBmc(self):
        log.debug("Entering DiagLib class procedure: powerCycleDeviceToOpenBmc")
        # we should use powerCycleChassis to power cycle chassis, because many unit do not connect with PDU
        return self.device.powerCycleChassis(Const.BOOT_MODE_OPENBMC)


    def wpl_powerCycleDevice(self):
        log.debug("Entering DiagLib class procedure: powerCycleDevice")
        return self.device.powerCycleDevice()


   ### boot mode related wrapper APIs
    def wpl_grubBootIntoDiagOS(self):
        log.debug("Entering DiagLib class procedure: grubBootIntoDiagOS")
        return self.device.grubBootIntoDiagOS()


    def wpl_grubBootIntoOnie(self):
        log.debug("Entering DiagLib class procedure: grubBootIntoOnie")
        return self.device.grubBootIntoOnieEnv()


    def wpl_bootIntoOnieInstallMode(self):
        log.debug("Entering DiagLib class procedure: bootIntoOnieInstallMode")
        return self.device.bootIntoOnieInstallMode()


    def wpl_bootIntoOnieRescueMode(self):
        log.debug("Entering DiagLib class procedure: bootIntoOnieRescueMode")
        return self.device.bootIntoOnieRescueMode()


    def wpl_bootIntoDiagOS(self):
        log.debug("Entering DiagLib class procedure: bootIntoDiagOS")
        return self.device.bootIntoDiagOS()


    def wpl_bootIntoBios(self):
        log.debug("Entering DiagLib class procedure: bootIntoBios")
        return self.device.bootIntoDiagOS()


    def wpl_getCurrentBootMode(self):
         return self.device.getCurrentBootMode()


    ### wait prompt related wrapper APIs
    def wpl_waitForDiagPrompt(self):
        log.debug("Entering DiagLib class procedure: waitForDiagPrompt")
        output = self.wpl_waitForGrubPrompt()
        output1 = self.wpl_grubBootIntoDiagOS()
        output += output1
        return output


    def wpl_waitForOniePrompt(self):
        log.debug("Entering DiagLib class procedure: waitForOniePrompt")
        output = self.wpl_waitForGrubPrompt()
        output1 = self.wpl_grubBootIntoOnie()
        output += output1
        return output


    def wpl_waitForCentOSPrompt(self):
        log.debug("Entering DiagLib class procedure: waitForCentOSPrompt")
        output = self.device.waitForLoginPrompt("centos", 600)
        return output


    def wpl_waitForOpenBmcPrompt(self):
        log.debug("Entering DiagLib class procedure: waitForOpenBmcPrompt")
        output = self.device.waitForLoginPrompt("openbmc", 600)
        return output


    def wpl_waitForGrubPrompt(self):
        log.debug("Entering DiagLib class procedure: waitForGrubPrompt")
        return self.device.waitForGrubPrompt()


    def wpl_getPrompt(self, mode=None, timeout=60, idleTimeout=60, logFile='None'):
        return self.device.getPrompt(mode, timeout, idleTimeout, logFile)


    def wpl_getCurrentPromptStr(self):
        return self.device.getCurrentPromptStr()


    def wpl_getDiagOSPromptStr(self):
        return self.device.promptDiagOS


    def wpl_getBmcPromptStr(self):
        return self.device.promptBmc


    ### send/receive related wrapper APIs ###
    def wpl_sendline(self, cmd, CR=True):
        if (CR == True):
            msg = (cmd + '\r')
        else:
            msg = cmd
        return self.device.sendMsg(msg)


    def wpl_transmit(self, cmd, CR=True):
        return self.wpl_sendline(cmd, CR)


    def wpl_sendCmd(self, cmd, prompt):
        return self.device.sendCmd(cmd, prompt)


    def wpl_execute(self, cmd, mode=None, timeout=60):
        return self.device.execute(cmd, mode, timeout)

    def wpl_execute_cmd(self, cmd, mode=None, timeout=60):
        return self.device.executeCmd(cmd, mode, timeout)

    def wpl_receive(self, rcv_str, timeout=60):
        return self.device.receive(rcv_str, timeout)


    def wpl_flush(self):
        return self.device.flush()


    ### log related wrapper APIs ###
    def wpl_log_debug(self, msg):
        return log.debug(msg)


    def wpl_log_error(self, msg):
        return log.error(msg)


    def wpl_log_info(self, msg):
        return log.info(msg)


    def wpl_log_success(self, msg):
        return log.success(msg)


    def wpl_log_fail(self, msg):
        return log.fail(msg)


    ### misc. wrapper API ###
    def wpl_raiseException(self, msg):
        raise RuntimeError(msg)


    def wpl_displayDiagOSversion(self):
        log.debug("Entering DiagLib class procedure: displayDiagOsversion")
        return self.device.displayDiagOSVersion()


    def set_verbose_level(self, verb_level):
        cmd = ('export VERB_LEVEL=' + str(verb_level))
        return self.wpl_execute(cmd)


@minipack3
def check_server_minipack3(device, host_ip, host_name, host_passwd, server_prompt):
    deviceObj = Device.getDeviceObject(device)
    devicePc = Device.getDeviceObject('PC')
    cmd = 'ssh ' + host_name + '@' + host_ip
    deviceObj.sendCmd(cmd)
    promptList = ["(y/n)", "(yes/no)", "password:"]
    patternList = re.compile('|'.join(promptList))
    output = deviceObj.read_until_regexp(patternList, 20)
    if re.search("(y/n)", output):
        deviceObj.sendCmd("yes")
        deviceObj.read_until_regexp("password:")
        deviceObj.sendCmd(host_passwd)
        deviceObj.read_until_regexp(server_prompt)
    elif re.search("(yes/no)", output):
        deviceObj.sendCmd("yes")
        deviceObj.read_until_regexp("password:")
        deviceObj.sendCmd(host_passwd)
        deviceObj.read_until_regexp(server_prompt)
    elif re.search("password:", output):
        deviceObj.sendCmd(host_passwd)
        deviceObj.read_until_regexp(server_prompt)
    else:
        log.fail("pattern mismatch")
    deviceObj.sendline('\n')

@minipack3
def checkin_device_from_server(device, host_ip, host_name):
    deviceObj = Device.getDeviceObject(device)
    devicePc = Device.getDeviceObject('PC')
    cmd = 'ssh ' + host_name + '@' + host_ip
    deviceObj.sendCmd(cmd)
    c1=deviceObj.read_until_regexp('press \[ a b c d e f g h i \] to run a test',timeout=60)
    deviceObj.sendline('q')
    time.sleep(5)
    deviceObj.sendline('\n')

@minipack3
def exit_the_server(device):
    device_obj = Device.getDeviceObject(device)
    device_obj.sendCmd('exit')
    c2=device_obj.read_until_regexp('closed',timeout=10)

@minipack3    
def get_minerva_diag_system_version_pattern(device):
    device=Device.getDeviceObject(device)
    minerva_bios_version = get_minerva_new_diag_version('DIAG','BIOS')
    minerva_bmc_version = get_minerva_new_diag_version('DIAG','BMC')
    minerva_i210_version = get_minerva_new_diag_version('DIAG','I210')
    minerva_sdk_version = get_minerva_new_diag_version('DIAG','SDK')
    minerva_bsp_version = get_minerva_new_diag_version('DIAG','BSP')
    minerva_udev_version = get_minerva_new_diag_version('DIAG','UDEV')
    minerva_os_version = get_minerva_new_diag_version('DIAG','OS')
    minerva_iob_fpga_version = get_minerva_new_diag_version('DIAG','IOB_FPGA')
    minerva_platform = get_minerva_new_diag_version('DIAG','Platform')
    minerva_dom_fpga_version = get_minerva_new_diag_version('DIAG','DOM_FPGA')
    minerva_smb1_cpld_version = get_minerva_new_diag_version('DIAG','SMB_CPLD1')
    minerva_smb2_cpld_version = get_minerva_new_diag_version('DIAG','SMB_CPLD2')
    minerva_pwr_cpld_version = get_minerva_new_diag_version('DIAG','PWR_CPLD')
    minerva_pn_version = get_minerva_new_diag_version('DIAG','PN')
    minerva_sn_version = get_minerva_new_diag_version('DIAG','SN')

    diag_system_version_pattern = ["(System Version.*)|(show_version.*)",
        "BIOS:\s+"+minerva_bios_version,
        "BMC:\s+"+minerva_bmc_version,
        "I210:\s+"+minerva_i210_version,
        "SDK:\s+"+minerva_sdk_version,
        "BSP:\s+"+minerva_bsp_version,
        "UDEV:\s+"+minerva_udev_version,
        "OS:\s+"+minerva_os_version,
        "",
        "Platform:\s+"+minerva_platform,
        "IOB FPGA:\s+"+minerva_iob_fpga_version,
        "DOM FPGA:\s+"+minerva_dom_fpga_version,
        "SMB CPLD 1:\s+"+minerva_smb1_cpld_version,
        "SMB CPLD 2:\s+"+minerva_smb2_cpld_version,
        "PWR CPLD:\s+"+minerva_pwr_cpld_version,
        #"PN:\s+"+minerva_pn_version,
        #"SN:\s+"+minerva_sn_version,
        
       
    ]
    return diag_system_version_pattern
    
@minipack3    
def get_minipack3_diag_system_version_pattern(device):
    device=Device.getDeviceObject(device)
    minipack3_bios_version = get_new_diag_version('DIAG','BIOS')
    minipack3_bmc_version = get_new_diag_version('DIAG','BMC')
    minipack3_i210_version = get_new_diag_version('DIAG','I210')
    minipack3_sdk_version = get_new_diag_version('DIAG','SDK')
    minipack3_bsp_version = get_new_diag_version('DIAG','BSP')
    minipack3_udev_version = get_new_diag_version('DIAG','UDEV')
    minipack3_os_version = get_new_diag_version('DIAG','OS')
    minipack3_iob_fpga_version = get_new_diag_version('DIAG','IOB_FPGA')
    minipack3_dom1_fpga_version = get_new_diag_version('DIAG','DOM1_FPGA')
    minipack3_dom2_fpga_version = get_new_diag_version('DIAG','DOM2_FPGA')
    minipack3_scm_cpld_version = get_new_diag_version('DIAG','SCM_CPLD')
    minipack3_smb_cpld_version = get_new_diag_version('DIAG','SMB_CPLD')
    minipack3_mcb_cpld_version = get_new_diag_version('DIAG','MCB_CPLD')
    minipack3_pn_version = get_new_diag_version('DIAG','PN')
    minipack3_sn_version = get_new_diag_version('DIAG','SN')

    diag_system_version_pattern = ["System Version   :|show_version    :",
        "BIOS:\s+"+minipack3_bios_version,
        "BMC:\s+"+minipack3_bmc_version,
        "I210:\s+"+minipack3_i210_version,
        "SDK:\s+"+minipack3_sdk_version,
        "BSP:\s+"+minipack3_bsp_version,
        "UDEV:\s+"+minipack3_udev_version,
        "OS:\s+"+minipack3_os_version,
        "",
        "IOB  FPGA :\s+"+minipack3_iob_fpga_version,
        "DOM1 FPGA :\s+"+minipack3_dom1_fpga_version,
        "DOM2 FPGA :\s+"+minipack3_dom2_fpga_version,
        "SCM CPLD :\s+"+minipack3_scm_cpld_version,
        "SMB CPLD :\s+"+minipack3_smb_cpld_version,
        "MCB CPLD :\s+"+minipack3_mcb_cpld_version,
        "PN:\s+"+minipack3_pn_version,
        "SN:\s+"+minipack3_sn_version,
    ]
    return diag_system_version_pattern
    
@minipack3    
def get_diag_system_version_pattern(device):
    deviceObj = Device.getDeviceObject(device)
    platform_name = deviceObj.name
    if (mp3 in platform_name):
        return get_minipack3_diag_system_version_pattern(device)
    if (minerva_janga in platform_name):
        return get_minerva_diag_system_version_pattern(device)
    if (minerva_tahan in platform_name):
        return None
     
@minipack3
def check_unidiag_system_versions(device):
    deviceObj=Device.getDeviceObject(device)
    diag_system_version_pattern = get_diag_system_version_pattern(device)

    c1=run_command('unidiag',prompt='>>>')
    print('The c1 is ',c1)
    try:
      CommonKeywords.should_match_ordered_regexp_list(c1,diag_system_version_pattern)
    except:
      raise RuntimeError("Unidiag actual and expected system versions mismatched" )
    time.sleep(5)
    log.success("Unidiag System versions are verifed successfully with latest versions.")
    
@minipack3
def exit_unidiag_interface(device):
   device= Device.getDeviceObject(device)
   for i in range(5):
       device.sendCmd('q')
       try:
           device.read_until_regexp('exit', timeout=5)
           break
       except Exception:
           continue
   device.sendCmd('\r')
   log.success("Exited from Unidiag interface successfully.")
    
# ---------------------------------- Test cases start from here ----------------------------

@minipack3
def check_system_i2c_scan(device):
    deviceObj = Device.getDeviceObject(device)
    get_into_unidiag_submenu_option(device, 'b', "System Test")
    platform_name = deviceObj.name
    if (mp3 in platform_name):
        pattern = i2c_system_scan_pattern
    elif (minerva_janga in platform_name):
        pattern = minerva_i2c_system_scan_pattern
    elif (minerva_tahan in platform_name):
        pattern = minerva_i2c_system_scan_pattern
        
        
    for iter_ in range(5):
        check_system_unidiag_option_status(device, 'c', "I2C Scan Test", pattern, iter_)
    log.success("system_i2c_scan test is executed successfully ")

@minipack3
def check_system_spi_scan(device):
    deviceObj= Device.getDeviceObject(device)
    get_into_unidiag_submenu_option(device, 'b', "System Test")
    platform_name = deviceObj.name
    if (mp3 in platform_name):
        pattern = system_spi_scan_test_pattern
    elif (minerva_janga in platform_name):
        pattern = minerva_system_spi_scan_test_pattern
    elif (minerva_tahan in platform_name):
        pattern = minerva_system_spi_scan_test_pattern
    for iter_ in range(5):
        check_system_unidiag_option_status(device, 'd', "SPI Scan Test", pattern, iter_)
    log.success("system_spi_scan test is executed successfully.")
    
@minipack3  
def check_system_pcie_scan(device):
    deviceObj = Device.getDeviceObject(device)
    get_into_unidiag_submenu_option(device, 'b', "System Test")
    platform_name = deviceObj.name
    if (mp3 in platform_name):
        pattern = system_pcie_scan_test_pattern
    elif (minerva_janga in platform_name):
        pattern = minerva_system_pcie_scan_test_pattern
    elif (minerva_tahan in platform_name):
        pattern = minerva_system_pcie_scan_test_pattern
    
    for iter_ in range(5):
        check_system_unidiag_option_status(device, 'e', "PCIE Scan Test", pattern, iter_)
    log.success("system_pcie_scan test is executed successfully.")
    
@minipack3    
def check_system_usb_network_test(device):
    deviceObj= Device.getDeviceObject(device)
    get_into_unidiag_submenu_option(device, 'b', "System Test")
    get_into_unidiag_submenu_option(device, 'h', "USB Test")    
    for iter_ in range(5):
        check_system_unidiag_option_status(device, 'c', "USB Network Test", system_usb_network_test_pattern, iter_)
    log.success("check_system_usb_network_test test is executed successfully.")
    
@minipack3
def check_system_oob_test(deviceM):
   device= Device.getDeviceObject(deviceM)
   get_into_unidiag_submenu_option(deviceM, 'b', "System Test")
    
   log.info("Pressing option 'l' to move in 'OOB Test' submenu ")
   device.sendCmd('l')
   c2=device.read_until_regexp("press any key to continue !", timeout=20)
   
   flag=False
   try:
       CommonKeywords.should_match_ordered_regexp_list(c2,system_oob_test_pattern)
   except :
       flag=True
       log.fail("Unable to ping device ip address.")
   try:
       CommonKeywords.should_match_a_regexp(c2,unidiag_case_pass)
   except :
       flag=True
       log.fail("'OOB test' option is showing 'FAIL' as overall status ")
   if flag:
       raise RuntimeError("Not able to ping device ip during OOB testing " )
  
   log.success("check_system_oob_test test is executed successfully.") 

@minipack3   
def get_into_osfp_submenu(device):
    get_into_unidiag_submenu_option(device, 'b', "System Test")
    get_into_unidiag_submenu_option(device, 'm', "OSFP Test")

@minipack3
def check_osfp_port_enable(device):  
    platform_name = deviceObj.name
    if (mp3 in platform_name):
        pattern = osfp_port_enable_pattern
    elif (minerva_janga in platform_name):
        pattern = minerva_osfp_port_enable_pattern
    elif (minerva_tahan in platform_name):
        pattern = minerva_osfp_port_enable_pattern
    
    check_system_unidiag_option_status(device, 'c', "OSFP/QSFP PORTS Enable", pattern)
    
@minipack3
def check_osfp_port_disable(device):
    platform_name = deviceObj.name
    if (mp3 in platform_name):
        pattern = osfp_port_disable_pattern
    elif (minerva_janga in platform_name):
        pattern = minerva_osfp_port_disable_pattern
    elif (minerva_tahan in platform_name):
        pattern = minerva_osfp_port_disable_pattern
    check_system_unidiag_option_status(device, 'd', "OSFP/QSFP PORTS Disable", pattern)

@minipack3
def check_osfp_i2c_scan(device):
    check_system_unidiag_option_status(device, 'b', "I2C SCAN Test", osfp_i2c_scan_pattern)
    
@minipack3
def check_osfp_port_present(device):
    platform_name = deviceObj.name
    if (mp3 in platform_name):
        pattern = ospf_ports_check_pattern
    elif (minerva_janga in platform_name):
        pattern = minerva_ospf_ports_check_pattern
    elif (minerva_tahan in platform_name):
        pattern = minerva_ospf_ports_check_pattern
    for iter_ in range(5):
        check_system_unidiag_option_status(device, 'e', "OSFP PORTS Present Check", pattern, iter_ )
    log.success("check osfp ports check test is executed successfully.")
    
@minipack3
def check_osfp_port_reset(device):
    for iter_ in range(5):
        check_system_unidiag_option_status(device, 'f', "OSFP PORTS Reset Check", ospf_ports_reset_check_pattern, iter_ )
    log.success("check osfp port reset test is executed successfully.")
 
@minipack3   
def check_osfp_port_lpmode_check(device, lpmode=False):
    platform_name = deviceObj.name
    if lpmode==True:
        if (mp3 in platform_name):
            pattern = ospf_ports_lpmode_check_lpmode_pattern
        elif (minerva_janga in platform_name):
            pattern = minerva_ospf_ports_lpmode_check_pattern
        elif (minerva_tahan in platform_name):
            pattern = minerva_ospf_ports_lpmode_check_pattern
    else:
        
        if (mp3 in platform_name):
            pattern = ospf_ports_lpmode_check_hpmode_pattern
        elif (minerva_janga in platform_name):
            pattern = minerva_ospf_ports_lpmode_check_pattern
        elif (minerva_tahan in platform_name):
            pattern = minerva_ospf_ports_lpmode_check_pattern
    
    for iter_ in range(3):
        check_system_unidiag_option_status(device, 'g', "OSFP/QSFP PORTS LPMODE Check", pattern, iter_ )
    log.success("check osfp port lpmode check test is executed successfully.")
    
@minipack3
def check_osfp_port_lpmode_test(device):
    platform_name = deviceObj.name
    if (mp3 in platform_name):
        pattern = ospf_ports_lpmode_test_pattern
    elif (minerva_janga in platform_name):
        pattern = minerva_ospf_ports_lpmode_test_pattern
    elif (minerva_tahan in platform_name):
        pattern = minerva_ospf_ports_lpmode_test_pattern
        
    for iter_ in range(3):
        check_system_unidiag_option_status(device, 'k', "OSFP PORTS LPMODE Test", pattern, iter_ )
    log.success("check osfp port lpmode test is executed successfully.")
    
@minipack3
def check_osfp_port_hpmode_test(device):
    platform_name = deviceObj.name
    if (mp3 in platform_name):
        pattern = ospf_ports_hpmode_test_pattern
    elif (minerva_janga in platform_name):
        pattern = minerva_ospf_ports_lpmode_test_pattern
    elif (minerva_tahan in platform_name):
        pattern = minerva_ospf_ports_hpmode_test_pattern
        
    for iter_ in range(3):
        check_system_unidiag_option_status(device, 'l', "OSFP PORTS HPMODE Test", pattern, iter_ )
    log.success("check osfp port hpmode test is executed successfully.")

def get_new_diag_version(image_type,name):
    updater_info_dict = CommonLib.get_swinfo_dict("DIAG")
    ver1= updater_info_dict.get('mp3_version').get(name,"")
    return ver1

def get_minerva_new_diag_version(image_type,name):
    updater_info_dict = CommonLib.get_swinfo_dict("DIAG")
    ver1= updater_info_dict.get('minerva_version').get(name,"")
    return ver1

@minipack3
def check_file_present(image_type,name):
   path1='/var/unidiag/firmware'
   path2='cd ' + path1
   c1=device.executeCmd(path2)
   file1 = get_new_diag_version(image_type,name)
   print('The value of file is',file1)
   c2= device.executeCmd('ls')
   if file1 in c2:
      log.success('File is present in the destination')
   else:
       raise RuntimeError('Please check if file is present')
       
def check_minerva_file_present(image_type,name):
   path1='/var/unidiag/firmware'
   path2='cd ' + path1
   c1=device.executeCmd(path2)
   file1 = get_minerva_new_diag_version(image_type,name)
   print('The value of file is',file1)
   c2= device.executeCmd('ls')
   str1="Please check if file " + file1 + " is present"
   if file1 in c2:
      log.success('File %s is present in the destination' %file1)
   else:
       raise RuntimeError(str1)

@minipack3
def copy_file_to_firmware(device,image_type,name):
    deviceObj= Device.getDeviceObject(device)
    path1="/var/unidiag/firmware"
    path2=latest_images_dir
    file1 = get_new_diag_version(image_type,name)
    cmd = "cp -r ~/"+latest_images_dir+"/"+file1+" ."
    deviceObj.executeCmd("cd "+path1)
    log.info("Copy the image to root directory..")
    c1 = deviceObj.executeCmd(cmd)
    c2 = deviceObj.executeCmd("ls")
    if file1 in c2:
       log.success('File is present in the destination')
    else:
       raise RuntimeError('Please check if file is present')
    flag=False
   
    
@minipack3
def check_sdk_path():
   path='/usr/local/cls_diag/SDK \r'
   str1= 'cd ' + path
   c1=device.executeCmd(str1)
   device.sendMsg('\n')
   if not re.search('rror', c1):
       log.success('Path changed successfully')
   else:
       raise RuntimeError('Path not changed')

@minipack3
def check_power_cycle_bmc(device):
    device= Device.getDeviceObject(device)
    device.switchToBmc()
    run_command('wedge_power.sh reset -s',prompt='login:',timeout=300)
    time.sleep(5)
    device.loginToNEWBMC()
    #device.switchToCpu()
    device.trySwitchToCpu()
    time.sleep(5)
    device.read_until_regexp("localhost login:", timeout=400)
    time.sleep(10)
    log.success("check power cycle test executed successfully")
    log.success('Successfully switched to CPU')
    c5=device.read_until_regexp('>>>', timeout=300)
    print('The value of c5 is',c5)
    for i in range(0,2):
        device.sendCmd('q')
        time.sleep(1)
    c6=device.read_until_regexp('exit',timeout=160)
    device.executeCmd('\r')
    log.success("Exited from Unidiag interface successfully.")

@minipack3
def check_th5_version():
    try:
        run_command('./auto_load_user.sh',prompt='BCM.0>')
        run_command('dsh', prompt='sdklt.0>')
    except:
        run_command('exit',prompt='#')
        run_command('cd')
        raise RuntimeError("Error while entering in BMC")
    
    c1=run_command('pciephy fwinfo',prompt='sdklt.0>')
    th5_version = get_new_diag_version("DIAG","TH5_Switch")
    pattern = "PCIe FW loader version: "+th5_version
    try:
        CommonKeywords.should_match_a_regexp(c1,pattern)
    except :
        raise RuntimeError("minipack3 version mismatch")
    
    run_command('exit',prompt='BCM.0>')
    run_command('exit',prompt='#')
    run_command('cd')
    log.success("TH5 Version is as expected.")

@minipack3
def check_firmware_flash_upgrade(deviceM, firmware_name, firmware_option, upgrade_pattern):

   device= Device.getDeviceObject(deviceM)
   check_unidiag_system_versions(deviceM)
   str3 = "User has cancelled upgrade."
   firmware_option_name="upgrade "+firmware_name
   get_into_unidiag_submenu_option(deviceM, 'f', "Firmware Upgrade")
   get_into_unidiag_submenu_option(deviceM, firmware_option, firmware_option_name)
   
   
   # Press n to cancel the upgrade
   device.read_until_regexp('to continue',timeout=20)
   device.sendCmd('n')
   time.sleep(5)
   c1=device.read_until_regexp("press any key to continue !", timeout=190)
   print('The value of c1 is ',c1)
   device.sendCmd('\r')
   if re.search(str3,c1) and  re.search(unidiag_case_pass,c1):
       log.success(firmware_name+' upgrade cancelled operation successful')
   else:
       exit_unidiag_interface(deviceM)
       raise RuntimeError(firmware_name+' upgrade cancellatation operation failed')
   
   # Press y to continue the upgrade
   time.sleep(10)
   get_into_unidiag_submenu_option(deviceM, firmware_option, firmware_option_name)
   device.read_until_regexp('to continue',timeout=20)
   device.sendCmd('y')
   time.sleep(5)
   c2=device.read_until_regexp("press any key to continue !", timeout=190)
   print('The value of c1 is ',c1)
   device.sendCmd('\r')
   try:
       CommonKeywords.should_match_ordered_regexp_list(c2,upgrade_pattern)
       CommonKeywords.should_match_a_regexp(c2,unidiag_case_pass)
       log.success(firmware_name+' upgrade successful')
   except:
       exit_unidiag_interface(deviceM)
       raise RuntimeError(firmware_name+' upgrade failed')
   # Exit unidiag menu
   exit_unidiag_interface(deviceM)

@minipack3
def check_unidiag_powercycle(device):
    deviceObj=Device.getDeviceObject(device)
    get_into_unidiag_submenu_option(device, 'b', "System Test")
    get_into_unidiag_submenu_option(device, 'n', "Power Test")
    get_into_unidiag_submenu_option(device, 'b', "Power Cycle the System")
    c10=deviceObj.read_until_regexp("proceed", timeout=30)
    deviceObj.sendCmd('y')
    time.sleep(5)
    log.debug('System is going down and rebooting')
    deviceObj.read_until_regexp('login', timeout=300)
    deviceObj.loginToNEWBMC()
    #device.switchToCpu()
    deviceObj.trySwitchToCpu()
    time.sleep(5)
    deviceObj.read_until_regexp("localhost login:", timeout=400)
    time.sleep(10)
    log.success('Successfully switched to CPU')
    c5=deviceObj.read_until_regexp('>>>', timeout=300)
    print('The value of c5 is',c5)
    for i in range(0,2):
        deviceObj.sendCmd('q')
        time.sleep(1)
    c6=deviceObj.read_until_regexp('exit',timeout=160)
    deviceObj.executeCmd('\r')
    log.success("Exited from Unidiag interface successfully.")


@minipack3    
def unidiag_version_check(device, unidiag_version):
    """
    Checks if the unidiag version on the given device matches the specified minipack_unidiag_version.

    Args:
        device (str): The device name or identifier.
        minipack_unidiag_version (str): The expected minipack unidiag version.

    Raises:
        RuntimeError: If the minipack_unidiag_version does not match the actual version.

    Returns:
        None
    """
    device = Device.getDeviceObject(device)
    c0 = device.executeCmd('unidiag -v')
    log.info(unidiag_version)
    flag=False
    try:
        CommonKeywords.should_match_a_regexp(c0,unidiag_version)
    except :
        flag=True
        log.fail("Unidiag version mismatch")
        
    if flag:
        raise RuntimeError("'Diag Script install reinstall Test' failed")
    log.success("unidiag version is matching successfully")
    
    
@minipack3    
def install_reinstall_test(device):
    """
    Function to install and reinstall a test on a device.

    Args:
        device (str): The device on which the test will be installed.

    Returns:
        None
    """
    device= Device.getDeviceObject(device)
    minipack3_new_image = get_new_diag_version('DIAG','diagNewImage')
    cmd = "cp -r ~/"+latest_images_dir+"/"+minipack3_new_image+" ."
    log.info("Copy the unidiag package to root directory..")
    c1 = device.executeCmd(cmd)
    c2 = device.executeCmd("ls")
    
    flag=False
    try:
        CommonKeywords.should_match_a_regexp(c2,minipack3_new_image)
    except:
        flag=True
        log.fail(minipack3_new_image+" is not present")
        
    log.info("Enter into diag package")
    device.sendCmd('cd '+minipack3_new_image)
    time.sleep(5)
    c3 = device.executeCmd('ls')
    try:
        CommonKeywords.should_match_a_regexp(c3,packages_file_name)
    except:
        flag=True
        log.fail(packages_file_name+" is not present")
    log.info("Enter into "+packages_file_name)
    device.sendCmd('cd '+packages_file_name)
    c5=device.executeCmd('ls')
    try:
        CommonKeywords.should_match_a_regexp(c5,'install.sh')
    except:
        flag=True
        log.fail("'install.sh' file not present")
    device.sendCmd('chmod 777 install.sh')
    device.sendCmd('./install.sh')
    device.read_until_regexp(unidiag_install_success_regex, timeout=120)
    device.sendCmd('cd')

    

@minipack3    
def check_unidiag_system_version_from_submenu(deviceM):
    """
    Function to check the Unidiag system versions from the submenu.

    Args:
        device (str): The device to perform the check on.

    Raises:
        RuntimeError: If the 'Diag Script install/reinstall' fails.

    Returns:
        None
    """
    device= Device.getDeviceObject(deviceM)
    time.sleep(10)
    c1=run_command('unidiag')
    log.info(c1)
    flag=False
    diag_system_version_pattern = get_diag_system_version_pattern(deviceM)
    CommonKeywords.should_match_ordered_regexp_list(c1,diag_system_version_pattern)
    time.sleep(5)
    
    log.info("Unidiag System versions are verified successfully with latest versions.")
    get_into_unidiag_submenu_option(deviceM, 'b', "System Test")
    get_into_unidiag_submenu_option(deviceM, 'b', "System Version")
    c2=device.read_until_regexp("press any key to continue !", timeout=20)
    CommonKeywords.should_match_ordered_regexp_list(c2,diag_system_version_pattern)
    log.info("Unidiag System versions are verifed successfully with latest versions.")
    
    try:
        CommonKeywords.should_match_a_regexp(c2,unidiag_case_pass)
    except :
        flag=True
        log.fail("'System Version' option is showing 'FAIL' as overall status ")
    if flag:
        raise RuntimeError("'Diag Script install/reinstall' failed")
    
    log.success("Diag Script install/reinstall executes successfully") 

@minipack3    
def upgrade_iob_fpga_flash(deviceM):    
    device = Device.getDeviceObject(deviceM)
    str1 = "SPI device iob upgrade succeeded."
    str2 = "User has cancelled upgrade."
    check_unidiag_system_versions(deviceM)
    get_into_unidiag_submenu_option(deviceM, 'f', "Firmware Upgrade")
    get_into_unidiag_submenu_option(deviceM, 'k', "upgrade iob_fpga flash")
    time.sleep(5)
    device.sendCmd('n')
    device.sendCmd('\n')
    time.sleep(5)
    
    c1=device.read_until_regexp("press any key to continue !", timeout=60)
    get_into_unidiag_submenu_option(deviceM, 'k', "upgrade iob_fpga flash")
    time.sleep(5)
    device.sendCmd('y')
    device.sendCmd('\n')
    time.sleep(5)
    c2=device.read_until_regexp("press any key to continue !", timeout=60)
    device.sendCmd('\n')
    time.sleep(5)
    
    flag=False
    try:
        CommonKeywords.should_match_a_regexp(c1,unidiag_case_pass)
        CommonKeywords.should_match_a_regexp(c2,unidiag_case_pass)
        CommonKeywords.should_match_a_regexp(c1,str2)
        CommonKeywords.should_match_a_regexp(c2,str1)
    except :
        flag=True
        log.fail("'upgrade iob_fpga flash' option is showing 'FAIL' as overall status ")
    if flag:
        raise RuntimeError("'upgrade iob_fpga flash test' failed")
    log.success("upgrade iob_fpga flash test is executed successfully.")
    

@minipack3
def verify_fpga_unidiag_version(device, option):
    deviceObj = Device.getDeviceObject(device)
    time.sleep(5)
    if option=='b':
        fpga_type='IOB FPGA'
        dom_pattern=get_new_diag_version('DIAG','iob_file')
    elif option=='c':
        dom_pattern=get_new_diag_version('DIAG','dom_file')
        fpga_type='DOM FPGA'
    else:
        raise RuntimeError("Wrong option typed!!")
    log.info("Press 'd' to get into 'FPGA test' submenu")
    deviceObj.sendCmd('d')
    time.sleep(5)
    log.info("Press '%s' to get into '%s' submenu " %(option, fpga_type))
    deviceObj.sendCmd(option)
    time.sleep(5)
    log.info("Press 'b' to check DOM version ")
    deviceObj.sendCmd('b')
    
    c1=deviceObj.read_until_regexp("press any key to continue !", timeout=20)
    dom_pattern_list= dom_pattern.split('_')
    version=dom_pattern_list[-1].rsplit('.',1)[0]
    CommonKeywords.should_match_a_regexp(c1,version)
    log.success("%s version is as expected" %fpga_type)
    
@minipack3
def upgrade_dom_flash(deviceM):
   device= Device.getDeviceObject(deviceM)
   str1 ="SPI device dom1 upgrade succeeded"
   str2 ="SPI device dom2 upgrade succeeded."
   str3='total_funcs:  1 pass: 1  skip: 0  fail: 0'
   str4 = "User has cancelled upgrade"
   check_unidiag_system_versions(deviceM)
   get_into_unidiag_submenu_option(deviceM, 'f', "Firmware Upgrade")
   get_into_unidiag_submenu_option(deviceM, 'j', "upgrade dom flash")
   
   # Press n to cancel the upgrade
   device.read_until_regexp("input '.*' to continue",timeout=10)
   device.sendCmd('n')
   c1=device.read_until_regexp("press any key to continue !", timeout=60)
   
   log.info('The value of c1 is '+c1)
   if re.search(str3,c1) and  re.search(str4,c1):
       log.success('DOM1 and DOM2 FPGA upgrade cancelled operation successful')
   else:
       raise RuntimeError('DOM1 and DOM2 FPGA upgrade cancellitation operation failed')
   
   # Press y to continue the upgrade
   get_into_unidiag_submenu_option(deviceM, 'j', "upgrade dom flash")
   device.read_until_regexp("input '.*' to continue",timeout=20)
   device.sendCmd('y')
   device.sendCmd('y')
   
   c2=device.read_until_regexp("press any key to continue !", timeout=190)
   print('The value of c2 is ',c2)
   device.sendCmd('\r')
   if re.search(str1,c2) and  re.search(str3,c2)  :
       log.success('DOM1 and DOM2 FPGA upgrade successful')
   else:
       raise RuntimeError('DOM1 and DOM2 FPGA upgrade failed')
       
@minipack3
def check_a_submenu(device, key, submenu_name, submenu_pattern):
    deviceObj= Device.getDeviceObject(device)
    
    log.info("Pressing option '%s' to move in '%s' submenu " %(key, submenu_name))
    deviceObj.sendCmd(key)
    c1=deviceObj.read_until_regexp("============= \[\s+%s\s+\] =============" %submenu_name, timeout=20)
    log.info(c1)
    CommonKeywords.should_match_ordered_regexp_list(c1,submenu_pattern)
    log.success("%s submenu is as expected." %submenu_name)
    
@minipack3   
def return_from_a_submenu(device, submenu_name):
    deviceObj= Device.getDeviceObject(device)
    log.info("Returning back to '%s' submenu" %submenu_name)
    deviceObj.sendCmd('q')
    c1=deviceObj.read_until_regexp(submenu_name, timeout=20) 

@minipack3
def check_diag_script_ui_submenu(device):
    deviceObj= Device.getDeviceObject(device)
    
    check_a_submenu(device, 'b', "System Test", system_test_pattern)
    check_a_submenu(device, 'f', "LED Test", system_led_test_pattern)
    return_from_a_submenu(device, "System Test")
    check_a_submenu(device, 'g', "FAN Test", system_fan_test_pattern)
    return_from_a_submenu(device, "System Test")
    check_a_submenu(device, 'h', "USB Test", system_usb_test_pattern)
    return_from_a_submenu(device, "System Test")
    check_a_submenu(device, 'i', "Mac Test", system_mac_test_pattern)
    return_from_a_submenu(device, "System Test")
    check_a_submenu(device, 'm', "OSFP Test", system_osfp_test_pattern)
    return_from_a_submenu(device, "System Test")
    return_from_a_submenu(device, "Test Main")
    
    check_a_submenu(device, 'c', "Board Test", board_test_pattern)
    check_a_submenu(device, 'b', "MCB  Board Test", mcb_board_test_pattern)
    return_from_a_submenu(device, "Board Test")
    check_a_submenu(device, 'c', "SMB  Board Test", smb_board_test_pattern)
    return_from_a_submenu(device, "Board Test")
    check_a_submenu(device, 'd', "SCM  Board Test", scm_board_test_pattern)
    return_from_a_submenu(device, "Board Test")
    check_a_submenu(device, 'e', "PDB  Board Test", pdb_board_test_pattern)
    return_from_a_submenu(device, "Board Test")
    check_a_submenu(device, 'f', "FCB  Board Test", fcb_board_test_pattern)
    return_from_a_submenu(device, "Board Test")
    check_a_submenu(device, 'g', "COMe Board Test", come_board_test_pattern)
    return_from_a_submenu(device, "Board Test")
    check_a_submenu(device, 'h', "BMC  Board Test", bmc_board_test_pattern)
    return_from_a_submenu(device, "Board Test")
    return_from_a_submenu(device, "Test Main")
    
    check_a_submenu(device, 'd', "FPGA Test", fpga_test_pattern)
    check_a_submenu(device, 'b', "IOB\s+FPGA", iob_fpga_test_pattern)
    return_from_a_submenu(device, "FPGA Test")
    check_a_submenu(device, 'c', "DOM1\s+FPGA", dom1_fpga_test_pattern)
    return_from_a_submenu(device, "FPGA Test")
    check_a_submenu(device, 'd', "DOM2\s+FPGA", dom2_fpga_test_pattern)
    return_from_a_submenu(device, "FPGA Test")
    return_from_a_submenu(device, "Test Main")
    
    check_a_submenu(device, 'e', "CPLD Test", cpld_test_pattern)
    check_a_submenu(device, 'b', "MCB CPLD Test", mcb_cpld_test_pattern)
    return_from_a_submenu(device, "CPLD Test")
    check_a_submenu(device, 'c', "SMB CPLD Test", smb_cpld_test_pattern)
    return_from_a_submenu(device, "CPLD Test")
    check_a_submenu(device, 'd', "SCM CPLD Test", scm_cpld_test_pattern)
    return_from_a_submenu(device, "CPLD Test")
    return_from_a_submenu(device, "Test Main")
    
    check_a_submenu(device, 'f', "Firmware Upgrade", firmware_submenu_pattern)
    return_from_a_submenu(device, "Test Main")
    
    check_a_submenu(device, 'g', "Stress Test", stress_submenu_pattern)
    return_from_a_submenu(device, "Test Main")
 
@minipack3
def upgrade_i210_flash(device):
    device= Device.getDeviceObject(device)
    check_unidiag_system_versions(device)
    time.sleep(5)
    get_into_unidiag_submenu_option(device, 'f', "Firmware Upgrade")
    get_into_unidiag_submenu_option(device, 'l', "upgrade i210 flash")
    device.sendCmd('y')
    device.sendCmd('\n')
    time.sleep(5)
    
    c3=device.read_until_regexp("press any key to continue !", timeout=60)
    device.sendCmd('\n')
    time.sleep(5)
    
    flag=False
    try:
        CommonKeywords.should_match_a_regexp(c3,unidiag_case_pass)
    except :
        flag=True
        log.fail("'upgrade i210 flash' option is showing 'FAIL' as overall status ")
    if flag:
        raise RuntimeError("'upgrade i210 flash' failed")
    log.success("upgrade i210 flash test is executed successfully.")
    
@minipack3
def extract_ip_addresses(device):
    output = device.executeCmd('ifconfig eth0')
    ip_regex = r"((25[0-5]|(2[0-4]|1\d|[1-9]|)\d)\.?\b){4}"
    matches = re.search(ip_regex, output)
    return matches.group(0)
    
    
# *************************************************** Minerva Jinga *********************************
def get_pattern_for_meta_platform_variant(device , mp3_pattern=None, j3_pattern=None, th5_pattern=None):
    deviceObj = Device.getDeviceObject(device)
    platform_name = deviceObj.name
    if (mp3_pattern is not None) and (mp3 in platform_name):
        pattern = mp3_pattern
    if (j3_pattern is not None) and (minerva_janga in platform_name):
        pattern = j3_pattern
    if (th5_pattern is not None) and (minerva_tahan in platform_name):
        pattern = th5_pattern
    return pattern
    


def get_into_unidiag_submenu_option(device, option_key, option_name):
    deviceObj = Device.getDeviceObject(device)
    log.info("Pressing option '%s' to move in '%s' submenu " %(option_key, option_name))
    deviceObj.sendCmd(option_key)
    time.sleep(5)

def check_system_unidiag_option_status(device, option_key, option_name, pattern_list, iter_=None, enable=True):
    device= Device.getDeviceObject(device)
    log.info("Pressing option '%s' to run '%s' " %(option_key, option_name))
    device.sendCmd(option_key)
    c1=device.read_until_regexp("press any key to continue !", timeout=120)
    device.sendCmd('\n')
    time.sleep(5)
    flag=False
    try:
        CommonKeywords.should_match_ordered_regexp_list(c1,pattern_list)
    except :
        flag=True
        log.fail("There is mismatch in in actual and expected output of '%s'" %(option_name))
        
    if enable: 
        try:
            CommonKeywords.should_match_a_regexp(c1,unidiag_case_pass)
        except :
            flag=True
            log.fail("Overall status of '%s' has some failed cases." %(option_name))
    if flag: 
        if iter_!=None:
            raise RuntimeError("'%s' is not giving expected status on iteration : %s" %(option_name, str(iter_+1)) )
        else: 
            raise RuntimeError("'%s' is not giving expected status" %(option_name))
    if iter_!=None:
        log.success("'%s' test is executed successfully for iteration : %s "%(option_name, str(iter_+1)))
    else:
        log.success("'%s' test is executed successfully" %(option_name))
    return c1
    
def check_unidiag_option_with_user_confirmation_status(device, option_key, option_name, pattern_list, cancel_pattern=user_cancelled_unidiag_case):
    deviceObj= Device.getDeviceObject(device)
    log.info("Pressing option '%s' to run '%s' " %(option_key, option_name))
    deviceObj.sendCmd(option_key)
    deviceObj.read_until_regexp("\(y/n\)", timeout=30)
    log.info("Giving 'n' for breaking the case.")
    deviceObj.sendCmd('n\r')
    c1=deviceObj.read_until_regexp("press any key to continue", timeout=30)
    time.sleep(5)
    try:
        CommonKeywords.should_match_ordered_regexp_list(c1,cancel_pattern)
        CommonKeywords.should_match_a_regexp(c1,unidiag_case_pass)
    except :
        raise RuntimeError("'%s' is not giving expected status on user cancellation" %(option_name) )
    log.info("Pressing option '%s' to run '%s' " %(option_key, option_name))
    deviceObj.sendCmd(option_key)
    deviceObj.read_until_regexp("\(y/n\)", timeout=30)
    log.info("Giving 'y' to proceed")
    deviceObj.sendCmd('y\r')
    c2=deviceObj.read_until_regexp("press any key to continue", timeout=30)
    time.sleep(5)
    try:
        CommonKeywords.should_match_ordered_regexp_list(c2,pattern_list)
        CommonKeywords.should_match_a_regexp(c2,unidiag_case_pass)
    except :
        raise RuntimeError("'%s' is not giving expected status after user gave confirmation to proceed" %(option_name) )
    log.success("'%s' test is executed successfully" %(option_name))

def check_minerva_system_versions(device):
    deviceObj = Device.getDeviceObject(device)
    get_into_unidiag_submenu_option(device, 'b', "System Test")
    for iter_ in range(5):
        diag_system_version_pattern = get_diag_system_version_pattern(device)
        check_system_unidiag_option_status(device, 'b', "System Version", diag_system_version_pattern, iter_)
    log.success("check_minerva_system_versions test is executed successfully")


@minipack3   
def get_into_minerva_osfp_submenu(device):
    deviceObj = Device.getDeviceObject(device)
    get_into_unidiag_submenu_option(device, 'b', "System Test")
    get_into_unidiag_submenu_option(device, 'o', "OSFP/QSFP Test")
    
    
@minipack3
def check_minerva_osfp_port_reset_check(device, enabled=False):
    deviceObj= Device.getDeviceObject(device)
    if(enabled):
        reset_pattern = minerva_ospf_ports_reset_check_pattern 
    else:
        reset_pattern = minerva_ospf_ports_unreset_check_pattern
    check_system_unidiag_option_status(device, 'f', "OSFP PORTS Reset Check", reset_pattern)  
    
@minipack3
def check_minerva_osfp_port_reset_test(device, times='1'):
    deviceObj= Device.getDeviceObject(device)
    for iter_ in range(int(times)):
        check_system_unidiag_option_status(device, 'i', "OSFP PORTS Reset Test", minerva_osfp_set_reset_pattern, iter_)
    log.success("check osfp port reset test is executed successfully.")
  
@minipack3
def check_minerva_osfp_port_unreset_test(device, times='1'):
    for iter_ in range(int(times)):
        check_system_unidiag_option_status(device, 'j', "OSFP PORTS Unreset Test", minerva_osfp_set_unreset_pattern, iter_)
    log.success("check osfp port unreset test is executed successfully.")

@minipack3
def check_minerva_system_oob_test(device):
    deviceObj = Device.getDeviceObject(device)
    get_into_unidiag_submenu_option(device, 'b', "System Test")
    for iter_ in range(5):
        check_system_unidiag_option_status(device, 'm', "OOB Test", minerva_system_oob_test_pattern, iter_)
    log.success("check_ping_network test is executed successfully.")
    
def osfp_i2c_scan_after_disable_or_enable_ports(device, pattern, iter_, enable=True):
    check_system_unidiag_option_status(device, 'b', "I2C SCAN Test", pattern, iter_, enable)
    
def check_minerva_osfp_i2c_scan(device):
    deviceObj= Device.getDeviceObject(device)
    for iter_ in range(5):
        log.info("Disable the ports before checking OSFP i2c scan test")
        check_osfp_port_disable (device)
        osfp_i2c_scan_after_disable_or_enable_ports(device, minerva_osfp_i2c_scan_disable_port_pattern, iter_, enable=False)
        
        log.info("Enable the ports before checking OSFP i2c scan test")
        check_osfp_port_enable (device)
        osfp_i2c_scan_after_disable_or_enable_ports(device, minerva_osfp_i2c_scan_enable_port_pattern, iter_)
        log.success("check_minerva_osfp_i2c_scan executed successfully for iteration : %s" %(str(iter_)))      
        
def check_system_gpio_device_scan(device):
    deviceObj= Device.getDeviceObject(device)
    get_into_unidiag_submenu_option(device, 'b', "System Test")
    for iter_ in range(5):
        check_system_unidiag_option_status(device, 'f', "GPIO SCAN Test", minerva_system_gpio_scan_pattern, iter_)
    log.success("check_system_gpio_device_scan test is executed successfully")

def check_system_mdio_test(device):
    deviceObj= Device.getDeviceObject(device)
    get_into_unidiag_submenu_option(device, 'b', "System Test")
    for iter_ in range(5):
        check_system_unidiag_option_status(device, 'k', "MDIO Test", minerva_mdio_pattern, iter_)
    log.success("check_system_mdio_test is executed successfully")
    
def check_lpc_through_ipmitool(device):
    deviceObj= Device.getDeviceObject(device)
    cmd="ipmitool mc info"
    c1=deviceObj.executeCmd(cmd)
    CommonKeywords.should_match_ordered_regexp_list(c1, minerva_lpc_pattern)
    log.success("%s is successfully executed" %cmd)
    
def check_system_lpc_test(device):
    deviceObj= Device.getDeviceObject(device)
    get_into_unidiag_submenu_option(device, 'b', "System Test")
    for iter_ in range(5):
        check_system_unidiag_option_status(device, 'l', "LPC Test", minerva_lpc_pattern, iter_)
    log.success("check_system_lpc_test is executed successfully")

def check_osfp_port_int_check(device):
    for iter_ in range(5):
        check_system_unidiag_option_status(device, 'h', "OSFP/QSFP PORTS INT Check ", minerva_osfp_int_pattern, iter_)
    log.success("check_osfp_port_int_check is executed successfully")
    
def get_fpga_version_through_registers(device, component_path):
    deviceObj = Device.getDeviceObject(device)
    deviceObj.executeCmd("cd")
    deviceObj.executeCmd("cd "+component_path)
    c1=deviceObj.executeCmd("cat device_id")
    device_id=re.search("0x(\S+)", c1).group(1)
    c1=deviceObj.executeCmd("cat fpga_ver")
    fpga_ver_hex=re.search("0x(\S+)", c1).group(1)
    fpga_ver=int(fpga_ver_hex, 16)
    c1=deviceObj.executeCmd("cat board_id")
    board_id=re.search("0x(\S+)", c1).group(1)
    c1=deviceObj.executeCmd("cat board_rev")
    deviceObj.executeCmd("cd")
    board_rev=re.search("0x(\S+)", c1).group(1)
    board_id+=board_rev
    check_unidiag_system_versions(device)
    return [fpga_ver,board_id,device_id]

def check_unidiag_fpga_iob_version(device):
    deviceObj = Device.getDeviceObject(device)
    fpga_ver, board_id, device_id=get_fpga_version_through_registers(device, IOB_FPGA_Path)
    minerva_fpga_iob_version_pattern = [ "\(y\) iob_ver_show\s+:\s+IOB FPGA version: v0.%s, board id: 0x%s device id: 0x%s" %(fpga_ver, board_id, device_id)]
    get_into_unidiag_submenu_option(device, 'd', "FPGA Test")
    get_into_unidiag_submenu_option(device, 'b', "IOB FPGA")
    check_system_unidiag_option_status(device, 'b', "Show IOB Version", minerva_fpga_iob_version_pattern)
    log.success("IOB FPGA Version through Unidiag option and original register value is checked successfully.")
    log.success("check_unidiag_fpga_iob_version is executed successfully")
    
def check_unidiag_fpga_iob_scratch_test(device):
    deviceObj = Device.getDeviceObject(device)
    get_into_unidiag_submenu_option(device, 'd', "FPGA Test")
    get_into_unidiag_submenu_option(device, 'b', "IOB FPGA")
    
    for iter_ in range(5):
        check_system_unidiag_option_status(device, 'c', "IOB Scratch Test", minerva_fpga_iob_scratch_test_pattern, iter_)
    log.success("check_unidiag_fpga_iob_scratch_test is executed successfully")

def check_unidiag_fpga_dom_version(device):
    deviceObj = Device.getDeviceObject(device)
    fpga_ver, board_id, device_id=get_fpga_version_through_registers(device, DOM_FPGA_Path)
    minerva_fpga_dom_version_pattern = ["\(y\) dom_ver_show\s+: DOM FPGA version: v0.%s, board id: 0x%s device id: 0x%s" %(fpga_ver, board_id, device_id)]
    get_into_unidiag_submenu_option(device, 'd', "FPGA Test")
    get_into_unidiag_submenu_option(device, 'c', "DOM FPGA")
    check_system_unidiag_option_status(device, 'b', "Show DOM Version", minerva_fpga_dom_version_pattern)
    log.success("DOM FPGA Version through Unidiag option and original register value is checked successfully.")
    log.success("check_unidiag_fpga_dom_version is executed successfully")
     
def check_fpga_dom_version_through_command(device):
    deviceObj = Device.getDeviceObject(device)
    output = deviceObj.executeCmd("cat /run/devmap/fpgas/IOB_FPGA/dom1_fpga_ver")
 
def check_unidiag_fpga_dom_scratch_test(device):
    deviceObj = Device.getDeviceObject(device)
    get_into_unidiag_submenu_option(device, 'd', "FPGA Test")
    get_into_unidiag_submenu_option(device, 'c', "DOM FPGA")
    for iter_ in range(5):
        check_system_unidiag_option_status(device, 'c', "DOM Scratch Test", minerva_fpga_dom_scratch_test_pattern, iter_)
    log.success("check_unidiag_fpga_dom_scratch_test is executed successfully")

#def get_cpld_version_through_registers(device, component_path, major_ver_file_name="cpld_major_ver"):
def get_cpld_version_through_registers(device, component_path):
    deviceObj = Device.getDeviceObject(device)
    deviceObj.executeCmd("cd")
    try:
        deviceObj.executeCmd("cd "+component_path)
        c1=deviceObj.executeCmd("cat cpld_major_ver")
        major_ver=str(int(re.search("0x(\S+)", c1).group(1), 16))
        c1=deviceObj.executeCmd("cat cpld_minor_ver")
        minor_ver=str(int(re.search("0x(\S+)", c1).group(1),16)) 
        c1=deviceObj.executeCmd("cat cpld_sub_ver")
        sub_ver=str(int(re.search("0x(\S+)", c1).group(1),16))
    except:
        deviceObj.executeCmd("cd")
        raise RuntimeError("Not able to fetch all field for CPLD versions at path : %s" %component_path)
        
    deviceObj.executeCmd("cd")
    check_unidiag_system_versions(device)
    return major_ver+"."+minor_ver+"."+sub_ver

def check_unidiag_cpld1_smb_version(device):
    deviceObj = Device.getDeviceObject(device)
    cpld_smb1_ver=get_cpld_version_through_registers(device, CPLD_SMB1_Path)
    minerva_cpld1_smb_version_pattern = ["\(y\) smb_1_ver_show\s+:\s+SMB CPLD 1 firmware version is: v"+cpld_smb1_ver]
    get_into_unidiag_submenu_option(device, 'e', "CPLD Test")
    get_into_unidiag_submenu_option(device, 'b', "SMB CPLD 1 Test")
    check_system_unidiag_option_status(device, 'b', "Show SMB CPLD 1 Version", minerva_cpld1_smb_version_pattern)
    log.success("SMB1 CPLD Version through Unidiag option and original register value is checked successfully.")
    log.success("check_unidiag_cpld1_smb_version is executed successfully")
    
def check_unidiag_cpld1_smb_scratch_test(device):
    deviceObj = Device.getDeviceObject(device)
    get_into_unidiag_submenu_option(device, 'e', "CPLD Test")
    get_into_unidiag_submenu_option(device, 'b', "SMB CPLD 1 Test")
    for iter_ in range(5):
        check_system_unidiag_option_status(device, 'c', "SMB CPLD 1 Scratch Test", minerva_cpld1_smb_scratch_test_pattern, iter_)
    log.success("check_unidiag_cpld1_smb_scratch_test is executed successfully")
     
def check_unidiag_cpld2_smb_version(device):
    deviceObj = Device.getDeviceObject(device)
    #cpld_smb2_ver=get_cpld_version_through_registers(device, CPLD_SMB2_Path, major_ver_file_name)
    cpld_smb2_ver=get_cpld_version_through_registers(device, CPLD_SMB2_Path)
    minerva_cpld2_smb_version_pattern = ["\(y\) smb_2_ver_show\s+:\s+SMB CPLD 2 version is: "+cpld_smb2_ver]
    get_into_unidiag_submenu_option(device, 'e', "CPLD Test")
    get_into_unidiag_submenu_option(device, 'c', "SMB CPLD 2 Test")
    check_system_unidiag_option_status(device, 'b', "Show SMB CPLD 2 Version", minerva_cpld2_smb_version_pattern)
    log.success("SMB2 CPLD Version through Unidiag option and original register value is checked successfully.")
    log.success("check_unidiag_cpld2_smb_version is executed successfully")
    
    
def check_unidiag_cpld2_smb_scratch_test(device):
    deviceObj = Device.getDeviceObject(device)
    get_into_unidiag_submenu_option(device, 'e', "CPLD Test")
    get_into_unidiag_submenu_option(device, 'c', "SMB CPLD 2 Test")
    
    for iter_ in range(5):
        check_system_unidiag_option_status(device, 'c', "SMB CPLD 2 Scratch Test", minerva_cpld2_smb_scratch_test_pattern, iter_)
    log.success("check_unidiag_cpld2_smb_scratch_test is executed successfully")
    
def check_unidiag_cpld_pwr_version(device):
    deviceObj = Device.getDeviceObject(device)
    cpld_pwr_ver=get_cpld_version_through_registers(device, CPLD_PWR_Path)
    minerva_cpld_pwr_version_pattern = ["\(y\) pwr_ver_show\s+:\s+PWR CPLD firmware version is: v"+cpld_pwr_ver]
    get_into_unidiag_submenu_option(device, 'e', "CPLD Test")
    get_into_unidiag_submenu_option(device, 'd', "PWR CPLD Test")
    check_system_unidiag_option_status(device, 'b', "Show PWR CPLD Version", minerva_cpld_pwr_version_pattern)
    log.success("PWR CPLD Version through Unidiag option and original register value is checked successfully.")
    log.success("check_unidiag_cpld_pwr_version is executed successfully")
    
    
def check_unidiag_cpld_pwr_scratch_test(device):
    deviceObj = Device.getDeviceObject(device)
    get_into_unidiag_submenu_option(device, 'e', "CPLD Test")
    get_into_unidiag_submenu_option(device, 'd', "PWR CPLD Test")
    for iter_ in range(5):
        check_system_unidiag_option_status(device, 'c', "PWR CPLD Scratch Test", minerva_cpld_pwr_scratch_test_pattern, iter_)
    log.success("check_unidiag_cpld_pwr_scratch_test is executed successfully")
    
def check_unidiag_smb_board_i2c_scan_test(device):
    deviceObj = Device.getDeviceObject(device)
    get_into_unidiag_submenu_option(device, 'c', "Board Test")
    get_into_unidiag_submenu_option(device, 'b', "SMB Board Test")
    for iter_ in range(5):
        check_system_unidiag_option_status(device, 'b', "I2C SCAN Test", minerva_smb_board_i2c_scan_pattern , iter_)
    log.success("check_unidiag_smb_board_i2c_scan_test is executed successfully")
    
def check_unidiag_smb_board_spi_scan_test(device):
    deviceObj = Device.getDeviceObject(device)
    get_into_unidiag_submenu_option(device, 'c', "Board Test")
    get_into_unidiag_submenu_option(device, 'b', "SMB Board Test")
    for iter_ in range(5):
        check_system_unidiag_option_status(device, 'c', "SPI SCAN Test", minerva_system_spi_scan_test_pattern , iter_)
    log.success("check_unidiag_smb_board_spi_scan_test is executed successfully")

def check_unidiag_smb_board_pcie_scan_test(device):
    deviceObj = Device.getDeviceObject(device)
    get_into_unidiag_submenu_option(device, 'c', "Board Test")
    get_into_unidiag_submenu_option(device, 'b', "SMB Board Test")
    for iter_ in range(5):
        check_system_unidiag_option_status(device, 'd', "PCIe SCAN Test", minerva_smb_board_pcie_scan_pattern , iter_)
    log.success("check_unidiag_smb_board_pcie_scan_test is executed successfully")

def check_unidiag_smb_board_nvme_test(device):
    deviceObj = Device.getDeviceObject(device)
    get_into_unidiag_submenu_option(device, 'c', "Board Test")
    get_into_unidiag_submenu_option(device, 'b', "SMB Board Test")
    get_into_unidiag_submenu_option(device, 'e', "NVMe Test")
    for iter_ in range(5):
        check_system_unidiag_option_status(device, 'b', "NVMe Info Test", minerva_smb_board_nvme_info_pattern , iter_)
        check_system_unidiag_option_status(device, 'c', "NVMe Storage Test", minerva_smb_board_nvme_storate_pattern , iter_)
    log.success("check_unidiag_smb_board_nvme_test is executed successfully")

def check_unidiag_pdb_board_i2c_scan_test(device):
    deviceObj = Device.getDeviceObject(device)
    get_into_unidiag_submenu_option(device, 'c', "Board Test")
    get_into_unidiag_submenu_option(device, 'c', "PDB Board Test")
    for iter_ in range(5):
        check_system_unidiag_option_status(device, 'b', "I2C SCAN Test", minerva_pdb_board_i2c_scan_pattern , iter_)
    log.success("check_unidiag_pdb_board_i2c_scan_test is executed successfully")

def check_unidiag_bmc_board_os_access_test(device):
    deviceObj = Device.getDeviceObject(device)
    get_into_unidiag_submenu_option(device, 'c', "Board Test")
    get_into_unidiag_submenu_option(device, 'e', "BMC Board Test")
    for iter_ in range(5):
        check_system_unidiag_option_status(device, 'b', "OS Access", minerva_bmc_board_os_access_pattern , iter_)
    log.success("check_unidiag_bmc_board_os_access_test is executed successfully")

def switchToBmcThenToComeAgain(device):
    device= Device.getDeviceObject(device)
    device.switchToBmc()
    time.sleep(5)
    device.trySwitchToCpu()
    time.sleep(5)
    log.success("switchToBmcThenToComeAgain executed successfully")

def check_unidiag_bmc_board_i2c_scan_test(device):
    deviceObj = Device.getDeviceObject(device)
    get_into_unidiag_submenu_option(device, 'c', "Board Test")
    get_into_unidiag_submenu_option(device, 'e', "BMC Board Test")
    for iter_ in range(5):
        check_system_unidiag_option_status(device, 'c', "I2C SCAN Test", minerva_bmc_board_i2c_scan_pattern , iter_)
    log.success("check_unidiag_bmc_board_i2c_scan_test is executed successfully")

def check_unidiag_bmc_board_spi_scan_test(device):
    deviceObj = Device.getDeviceObject(device)
    get_into_unidiag_submenu_option(device, 'c', "Board Test")
    get_into_unidiag_submenu_option(device, 'e', "BMC Board Test")
    for iter_ in range(5):
        check_system_unidiag_option_status(device, 'd', "SPI SCAN Test", minerva_bmc_board_spi_scan_pattern , iter_)
    log.success("check_unidiag_bmc_board_spi_scan_test is executed successfully")

def check_unidiag_bmc_board_cpu_test(device):
    deviceObj = Device.getDeviceObject(device)
    get_into_unidiag_submenu_option(device, 'c', "Board Test")
    get_into_unidiag_submenu_option(device, 'e', "BMC Board Test")
    get_into_unidiag_submenu_option(device, 'e', "CPU Test")
    for iter_ in range(5):
        check_system_unidiag_option_status(device, 'b', "info", minerva_bmc_board_cpu_info_pattern , iter_)
    log.success("check_unidiag_bmc_board_cpu_test is executed successfully")
    
def check_unidiag_bmc_board_memory_test(device):
    deviceObj = Device.getDeviceObject(device)
    get_into_unidiag_submenu_option(device, 'c', "Board Test")
    get_into_unidiag_submenu_option(device, 'e', "BMC Board Test")
    get_into_unidiag_submenu_option(device, 'f', "MEM Test")
    for iter_ in range(5):
        check_system_unidiag_option_status(device, 'b', "show meminfo", minerva_bmc_board_memory_info_pattern , iter_)
    log.success("check_unidiag_bmc_board_memory_test is executed successfully")

def check_unidiag_bmc_board_usb_network_test(device):
    deviceObj = Device.getDeviceObject(device)
    get_into_unidiag_submenu_option(device, 'c', "Board Test")
    get_into_unidiag_submenu_option(device, 'e', "BMC Board Test")
    get_into_unidiag_submenu_option(device, 'h', "USB Test")
    for iter_ in range(5):
        check_system_unidiag_option_status(device, 'b', "USB Network Test", minerva_bmc_board_usb_pattern , iter_)
    log.success("check_unidiag_bmc_board_usb_network_test  is executed successfully")
    
    
def check_unidiag_bmc_board_tpm_vendor_test(device):
    deviceObj = Device.getDeviceObject(device)
    get_into_unidiag_submenu_option(device, 'c', "Board Test")
    get_into_unidiag_submenu_option(device, 'e', "BMC Board Test")
    get_into_unidiag_submenu_option(device, 'g', "TPM Test")
    for iter_ in range(5):
        check_system_unidiag_option_status(device, 'b', "vendor", minerva_bmc_board_vender_pattern , iter_)
    log.success("check_unidiag_bmc_board_tpm_vendor_test  is executed successfully")    


def check_unidiag_bmc_board_bmc_version_test(device):
    deviceObj = Device.getDeviceObject(device)
    get_into_unidiag_submenu_option(device, 'c', "Board Test")
    get_into_unidiag_submenu_option(device, 'e', "BMC Board Test")
    for iter_ in range(5):
        check_system_unidiag_option_status(device, 'v', "show bmc version", minerva_bmc_board_bmc_version_pattern , iter_)
    log.success("check_unidiag_bmc_board_bmc_version_test  is executed successfully")



def check_unidiag_come_board_i2c_device_scan_test(device):
    deviceObj = Device.getDeviceObject(device)
    get_into_unidiag_submenu_option(device, 'c', "Board Test")
    get_into_unidiag_submenu_option(device, 'd', "COMe Board Test")
    for iter_ in range(5):
        check_system_unidiag_option_status(device, 'b', "I2C SCAN Test ", minerva_come_board_i2c_scan_pattern , iter_)
    log.success("check_unidiag_come_board_i2c_device_scan_test  is executed successfully")
  

def check_unidiag_come_board_bios_version_and_vendor_test(device):
    deviceObj = Device.getDeviceObject(device)
    get_into_unidiag_submenu_option(device, 'c', "Board Test")
    get_into_unidiag_submenu_option(device, 'd', "COMe Board Test")
    get_into_unidiag_submenu_option(device, 'c', "BIOS Test")
    check_system_unidiag_option_status(device, 'b', "Bios Version", minerva_come_board_bios_version_pattern)
    check_system_unidiag_option_status(device, 'c', "Bios vendor", minerva_come_board_bios_vendor_pattern)
    log.success("check_unidiag_come_board_bios_version_and_vendor_test  is executed successfully")


def check_unidiag_come_board_cpu_info_and_status_test(device):
    deviceObj = Device.getDeviceObject(device)
    get_into_unidiag_submenu_option(device, 'c', "Board Test")
    get_into_unidiag_submenu_option(device, 'd', "COMe Board Test")
    get_into_unidiag_submenu_option(device, 'd', "CPU Test")
    check_system_unidiag_option_status(device, 'b', "info", minerva_come_board_cpu_info_pattern)
    check_system_unidiag_option_status(device, 'c', "status", minerva_come_board_cpu_status_pattern)
    log.success("check_unidiag_come_board_cpu_info_and_status_test  is executed successfully")

def check_unidiag_come_board_tpm_vendor_test(device):
    deviceObj = Device.getDeviceObject(device)
    get_into_unidiag_submenu_option(device, 'c', "Board Test")
    get_into_unidiag_submenu_option(device, 'd', "COMe Board Test")
    get_into_unidiag_submenu_option(device, 'f', "TPM Test")
    check_system_unidiag_option_status(device, 'b', "vendor", minerva_come_board_tpm_vendor_pattern)
    log.success("check_unidiag_come_board_tpm_vendor_test  is executed successfully")

def check_unidiag_come_board_management_ethernet_test(device):
    deviceObj = Device.getDeviceObject(device)
    get_into_unidiag_submenu_option(device, 'c', "Board Test")
    get_into_unidiag_submenu_option(device, 'd', "COMe Board Test")
    
    log.info("Pressing option 'i' to move in 'Management Ethernet Port Connection Test' submenu ")
    deviceObj.sendCmd('i')
    deviceObj.read_until_regexp("please input IP or q quit:", timeout=10)
    deviceObj.sendCmd("q")
    c1=deviceObj.read_until_regexp("press any key to continue !", timeout=20)
    try:
        CommonKeywords.should_match_a_regexp(c1, unidiag_case_pass)
        log.success("Management ethernet quit option is working correctly.")
    except:
        raise RuntimeError("Error while quiting 'Management Ethernet Port Connection Test'")
    
    time.sleep(10)
    log.info("Pressing option 'i' to move in 'Management Ethernet Port Connection Test' submenu ")
    deviceObj.sendCmd('i')
    deviceObj.read_until_regexp("please input IP or q quit:", timeout=10)
    deviceObj.sendCmd(deviceObj.managementIP)
    c2=deviceObj.read_until_regexp("press any key to continue !", timeout=20)
    try:
        CommonKeywords.should_match_ordered_regexp_list(c2, minerva_conme_board_ethernet_port_pattern)
        CommonKeywords.should_match_a_regexp(c2, unidiag_case_pass)
        log.success("Management ethernet test with device ip is working correctly.")
    except:
        raise RuntimeError("Error while checking management ip connectivity through 'Management Ethernet Port Connection Test'")
    log.success("check_unidiag_come_board_management_ethernet_test  is executed successfully")
    
def check_unidiag_come_board_usb_internal_network_test(device):
    deviceObj = Device.getDeviceObject(device)
    get_into_unidiag_submenu_option(device, 'c', "Board Test")
    get_into_unidiag_submenu_option(device, 'd', "COMe Board Test")
    get_into_unidiag_submenu_option(device, 'h', "USB Test")
    check_system_unidiag_option_status(device, 'c', "USB Network Test", minerva_come_board_usb_internal_network_pattern)
    log.success("check_unidiag_come_board_usb_internal_network_test  is executed successfully")
    
def check_unidiag_come_board_rtc_test(device):
    deviceObj = Device.getDeviceObject(device)
    get_into_unidiag_submenu_option(device, 'c', "Board Test")
    get_into_unidiag_submenu_option(device, 'd', "COMe Board Test")
    get_into_unidiag_submenu_option(device, 'g', "RTC Test")
    check_system_unidiag_option_status(device, 'b', "epoch", minerva_come_board_rtc_epoch_pattern)
    check_system_unidiag_option_status(device, 'c', "timestamp", minerva_come_board_rtc_timestamp_pattern)
    check_system_unidiag_option_status(device, 'd', "hwclock", minerva_come_board_rtc_hwclock_pattern)
    log.success("check_unidiag_come_board_rtc_test  is executed successfully")
    
    
def check_unidiag_bcb_i2c_scan_via_come_test(device):
    deviceObj = Device.getDeviceObject(device)
    get_into_unidiag_submenu_option(device, 'g', "BCB Interface Test")
    for iter_ in range(5):
        check_system_unidiag_option_status(device, 'b', "BCB I2C SCAN Via COMe Test", minerva_bcb_i2c_scan_via_come_pattern , iter_)
    log.success("check_unidiag_bcb_i2c_scan_via_come_test is executed successfully")
  

def check_unidiag_bcb_i2c_scan_via_bmc_test(device):
    deviceObj = Device.getDeviceObject(device)
    get_into_unidiag_submenu_option(device, 'g', "BCB Interface Test")
    for iter_ in range(5):
        check_system_unidiag_option_status(device, 'c', "BCB I2C SCAN Via BMC Test", minerva_bcb_i2c_scan_via_bmc_pattern , iter_)
    log.success("check_unidiag_bcb_i2c_scan_via_bmc_test is executed successfully")
  
def check_unidiag_bcb_interface_network_blade_slot_id_check_test(device):
    deviceObj = Device.getDeviceObject(device)
    get_into_unidiag_submenu_option(device, 'g', "BCB Interface Test")
    for iter_ in range(5):
        check_system_unidiag_option_status(device, 'e', "Network Blade Slot ID Check", minerva_bcb_network_blade_slot_id_pattern , iter_)
    log.success("check_unidiag_bcb_interface_network_blade_slot_id_check_test is executed successfully")
    
    
def check_unidiag_bcb_cmm_present_signal_test(device):
    deviceObj = Device.getDeviceObject(device)
    get_into_unidiag_submenu_option(device, 'g', "BCB Interface Test")
    for iter_ in range(5):
        check_system_unidiag_option_status(device, 'd', "CMM Present Signal Check", minerva_bcb_cmm_present_signal_check_pattern , iter_)
    log.success("check_unidiag_bcb_cmm_present_signal_test is executed successfully")
    
  
def check_unidiag_bcb_network_blade_power_enable_signal_test(device):
    deviceObj = Device.getDeviceObject(device)
    get_into_unidiag_submenu_option(device, 'g', "BCB Interface Test")
    for iter_ in range(5):
        check_system_unidiag_option_status(device, 'f', "Network Blade Power Enable Signal Check", minerva_bcb_network_blade_power_enable_signal_pattern , iter_)
    log.success("check_unidiag_bcb_network_blade_power_enable_signal_test is executed successfully")
    

def check_unidiag_system_eeprom_show_board_fru_test(device):
    deviceObj = Device.getDeviceObject(device)
    get_into_unidiag_submenu_option(device, 'b', "System Test")
    get_into_unidiag_submenu_option(device, 'r', "EEPROM Test")
    for iter_ in range(5):
        check_system_unidiag_option_status(device, 'b', "Show Board FRU", minerva_system_eeprom_board_fru_pattern , iter_)
    log.success("check_unidiag_system_eeprom_show_board_fru_test is executed successfully")
    
    
def check_unidiag_system_eeprom_show_smb_fru1_test(device):
    deviceObj = Device.getDeviceObject(device)
    get_into_unidiag_submenu_option(device, 'b', "System Test")
    get_into_unidiag_submenu_option(device, 'r', "EEPROM Test")
    for iter_ in range(5):
        check_system_unidiag_option_status(device, 'c', "Show SMB FRU 1", minerva_system_eeprom_smb_fru1_pattern , iter_)
    log.success("check_unidiag_system_eeprom_show_smb_fru1_test is executed successfully")
    
  
def check_unidiag_system_eeprom_show_smb_fru2_test(device):
    deviceObj = Device.getDeviceObject(device)
    get_into_unidiag_submenu_option(device, 'b', "System Test")
    get_into_unidiag_submenu_option(device, 'r', "EEPROM Test")
    for iter_ in range(5):
        check_system_unidiag_option_status(device, 'd', "Show SMB FRU 2", minerva_system_eeprom_smb_fru2_pattern , iter_)
    log.success("check_unidiag_system_eeprom_show_smb_fru1_test is executed successfully")
    
@minipack3
def check_minerva_diag_script_ui_submenu(device):
    deviceObj= Device.getDeviceObject(device)
    
    check_a_submenu(device, 'b', "System Test", minerva_j3_system_test_pattern)
    check_a_submenu(device, 'g', "LED Test", minerva_j3_system_led_test_pattern)
    return_from_a_submenu(device, "System Test")
    check_a_submenu(device, 'h', "FAN Test", minerva_j3_system_fan_test_pattern)
    return_from_a_submenu(device, "System Test")
    check_a_submenu(device, 'i', "USB Test", minerva_j3_system_usb_test_pattern)
    return_from_a_submenu(device, "System Test")
    check_a_submenu(device, 'j', "Mac Test", minerva_j3_system_mac_test_pattern)
    return_from_a_submenu(device, "System Test")
    check_a_submenu(device, 'o', "OSFP/QSFP Test", minerva_j3_system_osfp_test_pattern)
    return_from_a_submenu(device, "System Test")
    check_a_submenu(device, 'p', "Power Cycle Test", minerva_j3_system_power_cycle_pattern)
    return_from_a_submenu(device, "System Test")
    check_a_submenu(device, 'r', "EEPROM Test", minerva_j3_system_eeprom_test_pattern)
    return_from_a_submenu(device, "System Test")
    check_a_submenu(device, 's', "Sensors Test", minerva_j3_system_sensor_test_pattern)
    return_from_a_submenu(device, "System Test")
    return_from_a_submenu(device, "Test Main")
    
    check_a_submenu(device, 'c', "Board Test", minerva_j3_board_test_pattern)
    check_a_submenu(device, 'b', "SMB  Board Test", minerva_j3_smb_board_test_pattern)
    time.sleep(5)
    return_from_a_submenu(device, "Board Test")
    time.sleep(5)
    check_a_submenu(device, 'd', "COMe Board Test", minerva_j3_come_board_test_pattern)
    time.sleep(5)
    return_from_a_submenu(device, "Board Test")
    time.sleep(5)
    check_a_submenu(device, 'e', "BMC  Board Test", minerva_j3_bmc_board_test_pattern)
    time.sleep(5)
    return_from_a_submenu(device, "Board Test")
    check_a_submenu(device, 'c', "PDB  Board Test", minerva_j3_pdb_board_test_pattern)
    time.sleep(5)
    return_from_a_submenu(device, "Board Test")
    time.sleep(5)
    return_from_a_submenu(device, "Test Main")
    
    check_a_submenu(device, 'd', "FPGA Test", minerva_j3_fpga_test_pattern)
    check_a_submenu(device, 'b', "IOB\s+FPGA", minerva_j3_iob_fpga_test_pattern)
    return_from_a_submenu(device, "FPGA Test")
    check_a_submenu(device, 'c', "DOM\s+FPGA", minerva_j3_dom_fpga_test_pattern)
    return_from_a_submenu(device, "FPGA Test")
    return_from_a_submenu(device, "Test Main")
    
    check_a_submenu(device, 'e', "CPLD Test", minerva_j3_cpld_test_pattern)
    check_a_submenu(device, 'b', "SMB CPLD 1 Test", minerva_j3_smb_cpld1_test_pattern)
    return_from_a_submenu(device, "CPLD Test")
    check_a_submenu(device, 'c', "SMB CPLD 2 Test", minerva_j3_smb_cpld2_test_pattern)
    return_from_a_submenu(device, "CPLD Test")
    check_a_submenu(device, 'd', "PWR CPLD Test", minerva_j3_pwr_cpld_test_pattern)
    return_from_a_submenu(device, "CPLD Test")
    return_from_a_submenu(device, "CPLD Test")
    return_from_a_submenu(device, "Test Main")
    
    check_a_submenu(device, 'f', "Firmware Upgrade", minerva_j3_firmware_submenu_pattern)
    return_from_a_submenu(device, "Test Main")
    
    check_a_submenu(device, 'h', "Stress Test", minerva_j3_stress_submenu_pattern)
    return_from_a_submenu(device, "Test Main")
    log.success("Minerva Unidiag script UI menu and submenu are verified successfully.")
  
   
def check_minerva_system_usb_network_test(device):
    deviceObj= Device.getDeviceObject(device)
    get_into_unidiag_submenu_option(device, 'b', "System Test")
    get_into_unidiag_submenu_option(device, 'i', "USB Test")
    for iter_ in range(5):
        check_system_unidiag_option_status(device, 'c', "USB Network Test", system_usb_network_test_pattern, iter_)
    log.success("check_minerva_system_usb_network_test test is executed successfully.")

def check_ping_from_bmc_come(device, ping_times="5"):
   deviceObj= Device.getDeviceObject(device)
   cmd1 = "ping -c "+ping_times+" fe80::ff:fe00:1%usb0"
   cmd2 = "ping -c "+ping_times+" fe80::ff:fe00:2%usb0"
   usb_ping_pattern = ping_times+ " packets transmitted, "+ping_times+" .*received, 0% packet loss"
   log.info("Ping BMC usb0 IP in COMe side directly by ping command")
   output = deviceObj.executeCmd(cmd1)
   CommonKeywords.should_match_a_regexp(output,usb_ping_pattern)
   log.success("Ping from COMe to BMC usb is successful.")
   
   log.info("Switch to BMC side")
   deviceObj.switchToBmc()
   deviceObj.loginToNEWBMC()
   log.info("Ping COMe usb0 IP in BMC side directly by ping command")
   output = deviceObj.executeCmd(cmd2)
   CommonKeywords.should_match_a_regexp(output,usb_ping_pattern)
   log.success("Ping from BMC to COMe usb is successful.")
   
   deviceObj.trySwitchToCpu()
   log.info("Switch to COMe side")
    
 
def check_minerva_system_come_mac_address(device):
    deviceObj= Device.getDeviceObject(device)
    get_into_unidiag_submenu_option(device, 'b', "System Test")
    get_into_unidiag_submenu_option(device, 'j', "MAC Test")
    come_mac_from_unidiag_pattern = "mac_come_check  : (\S+)"
    come_mac_from_command_pattern = "ether (\S+)  txqueuelen 1000  \(Ethernet\)"
    
    log.info("Getting Come mac address from unidiag.")
    output1=check_system_unidiag_option_status(device, 'b', "COMe MAC Addr Check", system_come_mac_addr_pattern )
    come_mac_from_unidiag=re.search(come_mac_from_unidiag_pattern, output1).group(1)
    exit_unidiag_interface(device)
    
    log.info("Getting Come mac address from ifconfig command.")
    output2 = deviceObj.executeCmd("ifconfig eth0")
    come_mac_from_command=re.search(come_mac_from_command_pattern, output2).group(1)
    
    if(come_mac_from_command.lower() != come_mac_from_unidiag.lower()):
        raise RuntimeError("Come Mac Address from unidiag option : '%s' and from ifconfig command : '%s' are different." %(come_mac_from_unidiag,        come_mac_from_command))
    else:
        log.success("Come Mac Address from unidiag option and from ifconfig command are same.")
    log.success("check_minerva_system_come_mac_address test is executed successfully.") 
   
def check_minerva_system_bmc_mac_address(device):
    deviceObj= Device.getDeviceObject(device)
    get_into_unidiag_submenu_option(device, 'b', "System Test")
    get_into_unidiag_submenu_option(device, 'j', "MAC Test")
    bmc_mac_from_unidiag_pattern = "mac_bmc_check   : check chassis mac addr (\S+)"
    bmc_mac_from_command_pattern = "Link encap:Ethernet  HWaddr (\S+)"
    
    log.info("Getting bmc mac address from unidiag.")
    output1=check_system_unidiag_option_status(device, 'c', "BMC MAC Addr Check", system_bmc_mac_addr_pattern )
    bmc_mac_from_unidiag=re.search(bmc_mac_from_unidiag_pattern, output1).group(1)
    exit_unidiag_interface(device)
    
    log.info("Switch to BMC side")
    deviceObj.switchToBmc()
    deviceObj.loginToNEWBMC()
    log.info("Getting bmc mac address from ifconfig command.")
    output2 = deviceObj.executeCmd("ifconfig eth0")
    bmc_mac_from_command=re.search(bmc_mac_from_command_pattern, output2).group(1)
    log.info("Switch to COMe side")
    deviceObj.trySwitchToCpu()
    
    if(bmc_mac_from_command.lower() != bmc_mac_from_unidiag.lower()):
        raise RuntimeError("BMC Mac Address from unidiag option : '%s' and from ifconfig command : '%s' are different." %(bmc_mac_from_unidiag,        bmc_mac_from_command))
    else:
        log.success("BMC Mac Address from unidiag option and from ifconfig command are same.")
    log.success("check_minerva_system_bmc_mac_address test is executed successfully.") 
   
def check_osfp_port_temperature_check(device):
    deviceObj= Device.getDeviceObject(device)
    for iter_ in range(3):
        check_system_unidiag_option_status(device, 'o', "OSFP/QSFP PORTS TEMPERATURE", minerva_osfp_port_temp_pattern, iter_ )
        check_system_unidiag_option_status(device, 'l', "OSFP/QSFP PORTS HPMODE Test", minerva_ospf_ports_hpmode_test_pattern, iter_ )
        check_system_unidiag_option_status(device, 'm', "OSFP/QSFP SET LOOPBACK to 16 Watt", minerva_ospf_ports_high_power_set_pattern, iter_ )
        time.sleep(15)
        check_system_unidiag_option_status(device, 'o', "OSFP/QSFP PORTS TEMPERATURE", minerva_osfp_port_temp_pattern, iter_ )
    log.success("check_osfp_port_temperature_check test is executed successfully.")
    
def check_osfp_port_current_check(device):
    deviceObj= Device.getDeviceObject(device)
    for iter_ in range(3):
        check_system_unidiag_option_status(device, 'r', "OSFP/QSFP PORTS CURRENT", minerva_osfp_port_current_pattern, iter_ )
        check_system_unidiag_option_status(device, 'l', "OSFP/QSFP PORTS HPMODE Test", minerva_ospf_ports_hpmode_test_pattern, iter_ )
        check_system_unidiag_option_status(device, 'm', "OSFP/QSFP SET LOOPBACK to 16 Watt", minerva_ospf_ports_high_power_set_pattern, iter_ )
        time.sleep(15)
        check_system_unidiag_option_status(device, 'r', "OSFP/QSFP PORTS CURRENT", minerva_osfp_port_current_pattern, iter_ )
    log.success("check_osfp_port_current_check test is executed successfully.")
    
def check_osfp_port_voltage_check(device):
    deviceObj= Device.getDeviceObject(device)
    for iter_ in range(3):
        check_system_unidiag_option_status(device, 'p', "OSFP/QSFP PORTS VOLTAGE", minerva_osfp_port_voltage_pattern, iter_ )
        check_system_unidiag_option_status(device, 'l', "OSFP/QSFP PORTS HPMODE Test", minerva_ospf_ports_hpmode_test_pattern, iter_ )
        check_system_unidiag_option_status(device, 'm', "OSFP/QSFP SET LOOPBACK to 16 Watt", minerva_ospf_ports_high_power_set_pattern, iter_ )
        time.sleep(15)
        check_system_unidiag_option_status(device, 'p', "OSFP/QSFP PORTS VOLTAGE", minerva_osfp_port_voltage_pattern, iter_ )
    log.success("check_osfp_port_voltage_check test is executed successfully.")

def check_unidiag_system_power_status(device):
    deviceObj= Device.getDeviceObject(device)
    get_into_unidiag_submenu_option(device, 'b', "System Test")
    get_into_unidiag_submenu_option(device, 'p', "Power Cycle Test")
    log.info("Checking Come Power status through unidiag")
    check_system_unidiag_option_status(device, 'b', "Power Status", minerva_power_status_pattern)
    exit_unidiag_interface(device)
    log.info("Checking come Power staqtus through bmc console command.")
    log.info("Switch to BMC side")
    deviceObj.switchToBmc()
    deviceObj.loginToNEWBMC()
    output1 = deviceObj.executeCmd("wedge_power.sh status")
    try:
        CommonKeywords.should_match_a_regexp(output1,wedge_power_status_pattern)
    except:
        log.info("Switch to COMe side")
        deviceObj.trySwitchToCpu()
        raise RuntimeError("Power status through wedge command is incorrect.")
    log.success("Power status through wedge command is correct.")
    log.info("Switch to COMe side")
    deviceObj.trySwitchToCpu()
    log.success("check_unidiag_system_power_status test is executed successfully.")
    
def check_unidiag_system_power_cycle_test(device):
    deviceObj= Device.getDeviceObject(device)
    str1=""
    get_into_unidiag_submenu_option(device, 'b', "System Test")
    get_into_unidiag_submenu_option(device, 'p', "Power Cycle Test")
    
    log.info("Pressing option c to run 'Power Cycle Test' ")
    deviceObj.sendCmd('c')
    deviceObj.read_until_regexp("Are you sure you want to proceed?", timeout=30)
    log.info("Giving 'n' for breaking the case.")
    deviceObj.sendCmd('n\r')
    c1=deviceObj.read_until_regexp("press any key to continue", timeout=30)
    time.sleep(5)
    try:
        CommonKeywords.should_match_ordered_regexp_list(c1,power_cycle_cancel_pattern)
        CommonKeywords.should_match_a_regexp(c1,unidiag_case_pass)
    except :
        raise RuntimeError("'power cycle test' is not giving expected status" )
    
    log.info("Pressing option c to run 'Power Cycle Test' ")
    deviceObj.sendCmd('c')
    deviceObj.read_until_regexp("Are you sure you want to proceed?", timeout=30)
    log.info("Giving 'y' to proceed")
    deviceObj.sendCmd('y\r')
    time.sleep(5)
    log.debug('System is going down and rebooting')
    deviceObj.read_until_regexp('login', timeout=300)
    deviceObj.loginToNEWBMC()
    deviceObj.trySwitchToCpu()
    time.sleep(5)
    deviceObj.read_until_regexp("localhost login:", timeout=400)
    time.sleep(10)
    log.success('Successfully switched to CPU')
    c5=deviceObj.read_until_regexp('>>>', timeout=300)
    print('The value of c5 is',c5)
    exit_unidiag_interface(device)
    log.success("'power cycle test' test is executed successfully")
    
def check_unidiag_come_power_cycle_test(device):
    deviceObj= Device.getDeviceObject(device)
    get_into_unidiag_submenu_option(device, 'b', "System Test")
    get_into_unidiag_submenu_option(device, 'p', "Power Cycle Test")
    
    log.info("Pressing option d to run 'COMe Power Cycle Test' ")
    deviceObj.sendCmd('d')
    deviceObj.read_until_regexp("Are you sure you want to proceed?", timeout=30)
    log.info("Giving 'n' for breaking the case.")
    deviceObj.sendCmd('n\r')
    c1=deviceObj.read_until_regexp("press any key to continue", timeout=30)
    time.sleep(5)
    try:
        CommonKeywords.should_match_ordered_regexp_list(c1,power_cycle_cancel_pattern)
        CommonKeywords.should_match_a_regexp(c1,unidiag_case_pass)
    except :
        raise RuntimeError("'Come power cycle test' is not giving expected status" )
    
    log.info("Pressing option d to run 'COMe Power Cycle Test' ")
    deviceObj.sendCmd('d')
    deviceObj.read_until_regexp("Are you sure you want to proceed?", timeout=30)
    log.info("Giving 'y' to proceed")
    deviceObj.sendCmd('y\r')
    time.sleep(5)
    log.debug('System is going down and rebooting')
    c2=deviceObj.read_until_regexp('>>>', timeout=500)
    exit_unidiag_interface(device)
    log.success("'come power cycle test' test is executed successfully")
    
def check_unidiag_sanity_test(device):
    deviceObj= Device.getDeviceObject(device)
    check_system_unidiag_option_status(device, 'i', "Sanity Test", minerva_sanity_pattern)
    log.success("check_unidiag_sanity_test test is executed successfully.")
    
def check_unidiag_snapshot_test(device):
    deviceObj= Device.getDeviceObject(device)
    check_system_unidiag_option_status(device, 'j', "Snapshot Test", minerva_snapshot_pattern)
    log.success("check_unidiag_snapshot_test test is executed successfully.")
    
def check_unidiag_fpga_auto_test(device):
    deviceObj= Device.getDeviceObject(device)
    get_into_unidiag_submenu_option(device, 'd', "FPGA Test")
    check_system_unidiag_option_status(device, 'a', "Auto Test", minerva_fpga_auto_test_pattern)
    log.success("check_unidiag_fpga_auto_test test is executed successfully.")

def check_unidiag_iob_fpga_auto_test(device):
    deviceObj= Device.getDeviceObject(device)
    get_into_unidiag_submenu_option(device, 'd', "FPGA Test")
    get_into_unidiag_submenu_option(device, 'b', "IOB FPGA")
    check_system_unidiag_option_status(device, 'a', "Auto Test", minerva_iob_fpga_auto_test_pattern)
    log.success("check_unidiag_iob_fpga_auto_test test is executed successfully.")
    
def check_unidiag_dom_fpga_auto_test(device):
    deviceObj= Device.getDeviceObject(device)
    get_into_unidiag_submenu_option(device, 'd', "FPGA Test")
    get_into_unidiag_submenu_option(device, 'c', "DOM FPGA")
    check_system_unidiag_option_status(device, 'a', "Auto Test", minerva_dom_fpga_auto_test_pattern)
    log.success("check_unidiag_dom_fpga_auto_test test is executed successfully.")
          
def check_unidiag_cpld_auto_test(device):
    deviceObj= Device.getDeviceObject(device)
    get_into_unidiag_submenu_option(device, 'e', "CPLD Test")
    check_system_unidiag_option_status(device, 'a', "Auto Test", minerva_cpld_auto_test_pattern)
    log.success("check_unidiag_cpld_auto_test test is executed successfully.")
      
def check_unidiag_smb_cpld1_auto_test(device):
    deviceObj= Device.getDeviceObject(device)
    get_into_unidiag_submenu_option(device, 'e', "CPLD Test")
    get_into_unidiag_submenu_option(device, 'b', "SMB CPLD 1 Test")
    check_system_unidiag_option_status(device, 'a', "Auto Test", minerva_smb_cpld1_auto_test_pattern)
    log.success("check_unidiag_smb_cpld1_auto_test test is executed successfully.")
    
def check_unidiag_smb_cpld2_auto_test(device):
    deviceObj= Device.getDeviceObject(device)
    get_into_unidiag_submenu_option(device, 'e', "CPLD Test")
    get_into_unidiag_submenu_option(device, 'c', "SMB CPLD 2 Test")
    check_system_unidiag_option_status(device, 'a', "Auto Test", minerva_smb_cpld2_auto_test_pattern)
    log.success("check_unidiag_smb_cpld2_auto_test test is executed successfully.")
    
def check_come_cpu_stress_test(device):
    deviceObj= Device.getDeviceObject(device)
    get_into_unidiag_submenu_option(device, 'h', "Stress Test")
    check_unidiag_option_with_user_confirmation_status(device, "b", "CPU Stress", cpu_stress_pattern, cpu_stress_cancel_pattern)
    log.success("check_come_cpu_stress_test test is executed successfully.")
   
def check_mem_stress_test(device):
    deviceObj= Device.getDeviceObject(device)
    get_into_unidiag_submenu_option(device, 'h', "Stress Test")
    check_unidiag_option_with_user_confirmation_status(device, "c", "MEM Stress", mem_stress_pattern, mem_stress_cancel_pattern)
    log.success("check_mem_stress_test test is executed successfully.")
    
def check_unidiag_mfg_test(device):
    deviceObj= Device.getDeviceObject(device)
    check_system_unidiag_option_status(device, "k", "MFG Test", mfg_pattern)
    log.success("check_unidiag_mfg_test test is executed successfully.")

def check_unidiag_main_auto_test(device):
    deviceObj= Device.getDeviceObject(device)
    check_system_unidiag_option_status(device, 'a', "Auto Test", minerva_test_main_auto_test_pattern)
    log.success("check_unidiag_main_auto_test test is executed successfully.")
    
def check_unidiag_system_auto_test(device):
    deviceObj= Device.getDeviceObject(device)
    get_into_unidiag_submenu_option(device, 'b', "System Test")
    check_system_unidiag_option_status(device, 'a', "Auto Test", minerva_system_auto_test_pattern)
    log.success("check_unidiag_system_auto_test test is executed successfully.")
    
def check_unidiag_system_mac_auto_test(device):
    deviceObj= Device.getDeviceObject(device)
    get_into_unidiag_submenu_option(device, 'b', "System Test")
    get_into_unidiag_submenu_option(device, 'j', "Mac Test")
    check_system_unidiag_option_status(device, 'a', "Auto Test", minerva_system_mac_auto_test_pattern)
    log.success("check_unidiag_system_mac_auto_test test is executed successfully.")
    
    
def upgrade_i210_MAC_addr(device, original_mac, new_dummy_mac):
     deviceObj= Device.getDeviceObject(device)
     check_unidiag_system_versions(device)
     new_mac_upper=new_dummy_mac.replace("-","")
     upgrade_pattern=["1: Updating Mac Address to %s.*Done" %new_mac_upper,"1: Updating Checksum and CRCs...Done."]

     get_into_unidiag_submenu_option(device, 'f', "Firmware Upgrade")
     log.info("Pressing option 'i' to move in 'upgrade i210 MAC addr' submenu ")
     deviceObj.sendCmd("i")
     regex="please input new mac addr %s" %original_mac
     try:
         deviceObj.read_until_regexp(regex,timeout=20)
         deviceObj.sendCmd(new_dummy_mac)
         output=deviceObj.read_until_regexp('press any key to continue !',timeout=90)
         time.sleep(10)
         deviceObj.sendCmd('\r')
         CommonKeywords.should_match_ordered_regexp_list(output,upgrade_pattern)
         CommonKeywords.should_match_a_regexp(output,unidiag_case_pass)
         log.success("Mac address has been successfully changed from %s to %s using 'i210 MAC addr' firmware upgrade " %(original_mac, new_dummy_mac))
     except:
         exit_unidiag_interface(device)
         raise RuntimeError("Not Able to update mac from %s to %s using 'i210 MAC addr' firmware upgrade "%(original_mac, new_dummy_mac))
     # Exit unidiag menu
     exit_unidiag_interface(device)

def get_formated_mac_address(mac_addr):
    mac_add=mac_addr.upper()
    formatted_mac=""
    for ind in range(len(mac_add)):
      formatted_mac+=mac_add[ind]
      if ind%2 and ind!=len(mac_add)-1:
          formatted_mac+="-"
    return formatted_mac
    
def get_formated_next_mac_address(device, formated_mac):
    values=["0", "1","2", "3", "4", "5", "6", "7", "8", "9", "A", "B", "C", "D","E", "F"]
    ind=values.index(formated_mac[-1])
    new_ind=(ind+1)%16
    new_mac=formated_mac[:-1]+values[new_ind]
    return new_mac
          
          
def update_i210_mac_address_firmware(device):
    deviceObj= Device.getDeviceObject(device)
    minerva_mac_addr = DeviceMgr.getDevice(devicename).get('macAddress')
    original_mac=get_formated_mac_address(minerva_mac_addr)
    new_dummy_mac=get_formated_next_mac_address(device, original_mac)
    try:
        log.info("Changing original mac to a new imaginary mac address")
        upgrade_i210_MAC_addr(device, original_mac, new_dummy_mac)
        check_power_cycle_bmc(device)
        verify_mac_address(device, new_dummy_mac)
        
        log.info("Changing imaginary mac back to its original mac address")
        upgrade_i210_MAC_addr(device, new_dummy_mac, original_mac)
        check_power_cycle_bmc(device)
        verify_mac_address(device,original_mac)
        log.success("Successfully updated and recovered original mac using 'i210 mac address' firmware update option")
    except:
        upgrade_i210_MAC_addr(device, new_dummy_mac, original_mac)
        check_power_cycle_bmc(device)
        raise RuntimeError("Not able to update with a new mac through 'i210 mac addr' firmware upgrade")
        

def get_mac_address(device):
    deviceObj= Device.getDeviceObject(device)
    output=deviceObj.executeCmd("ifconfig eth0")
    mac_regex="ether (.*)  txqueuelen 1000"
    mac_address=re.search(mac_regex,output).group(1)
    mac_address = mac_address.upper()
    return mac_address.replace(":", "-")
    
def verify_mac_address(device, exp_mac_add):
    deviceObj= Device.getDeviceObject(device)
    output=get_mac_address(device)
    CommonKeywords.should_match_a_regexp(output.lower(), exp_mac_add.lower())
    log.success("Expected mac address is matching with device mac.")

def update_internal_power_cpld_flash(deviceM, update_pattern):
    device= Device.getDeviceObject(deviceM)
    check_unidiag_system_versions(deviceM)
    str3 = "User cancelled upgrading PWR CPLD"
    get_into_unidiag_submenu_option(deviceM, 'f', "Firmware Upgrade")
    get_into_unidiag_submenu_option(deviceM, 'l', "upgrade power_cpld internal flash")
   
    # Press n to cancel the upgrade
    device.read_until_regexp('Please also be aware of that after the upgrade the system will be power cycled',timeout=20)
    device.sendCmd('n')
    time.sleep(5)
    c1=device.read_until_regexp("press any key to continue !", timeout=190)
    #print('The value of c1 is ',c1)
    device.sendCmd('\r')
    if re.search(str3,c1) and  re.search(unidiag_case_pass,c1):
        log.success('Internal power cpld flash upgrade cancelled operation successful')
    else:
        exit_unidiag_interface(deviceM)
        raise RuntimeError('Internal power cpld flash upgrade cancellatation operation failed')
   
    # Press y to continue the upgrade
    time.sleep(10)
    get_into_unidiag_submenu_option(deviceM, 'l', "upgrade power_cpld internal flash")
    device.read_until_regexp('Please also be aware of that after the upgrade the system will be power cycled',timeout=20)
    device.sendCmd('y')
    time.sleep(5)
    c2=device.read_until_regexp("bmc login:", timeout=400)
    device.loginToNEWBMC()
    device.trySwitchToCpu()
    time.sleep(5)
    device.read_until_regexp("localhost login:", timeout=400)
    time.sleep(10)
    log.success('Successfully switched to CPU')
    c5=device.read_until_regexp('>>>', timeout=300)

    # Exit unidiag menu
    exit_unidiag_interface(deviceM)
    device.executeCmd('\r')
    log.success("update_internal_power_cpld_flash is successful.")

def upgrade_bios_from_come(deviceM, upgrade_pattern):
    device= Device.getDeviceObject(deviceM)
    check_unidiag_system_versions(deviceM)
    str3 = "User has cancelled upgrade"
    get_into_unidiag_submenu_option(deviceM, 'f', "Firmware Upgrade")
    get_into_unidiag_submenu_option(deviceM, 'o', "upgrade bios flash")
    
    # Press n to cancel the upgrade
    device.read_until_regexp("Please confirm that your firmware is proper and input 'y' to continue",timeout=20)
    device.sendCmd('n')
    time.sleep(5)
    c1=device.read_until_regexp("press any key to continue !", timeout=190)
    device.sendCmd('\r')
    if re.search(str3,c1) and  re.search(unidiag_case_pass,c1):
        log.success('Bios upgrade via COMe cancelled operation is successful')
    else:
        exit_unidiag_interface(deviceM)
        raise RuntimeError('Bios upgrade via COMe cancellatation operation failed')
    
    # Press y to continue the upgrade
    time.sleep(10)
    get_into_unidiag_submenu_option(deviceM, 'o', "upgrade bios flash")
    device.read_until_regexp("Please confirm that your firmware is proper and input 'y' to continue",timeout=20)
    device.sendCmd('y')
    time.sleep(5)
    c2=device.read_until_regexp("press any key to continue !", timeout=2400)
    device.sendCmd('\r')
    try:
        CommonKeywords.should_match_ordered_regexp_list(c2,upgrade_pattern)
        CommonKeywords.should_match_a_regexp(c2,unidiag_case_pass)
        log.success("Bios upgrade via COMe is successful.")
    except:
        exit_unidiag_interface(deviceM)
        raise RuntimeError('Bios upgrade via COMe failed')
    # Exit unidiag menu
    exit_unidiag_interface(deviceM)
    
    
def upgrade_bios_from_bmc(deviceM, upgrade_pattern):
    device= Device.getDeviceObject(deviceM)
    check_unidiag_system_versions(deviceM)
    str3 = "User has cancelled upgrade"
    get_into_unidiag_submenu_option(deviceM, 'f', "Firmware Upgrade")
    get_into_unidiag_submenu_option(deviceM, 'd', "upgrade bios via bmc")
    
    # Press n to cancel the upgrade
    device.read_until_regexp("Please confirm that your firmware is proper and input 'y' to continue",timeout=20)
    device.sendCmd('n')
    time.sleep(5)
    c1=device.read_until_regexp("press any key to continue !", timeout=190)
    device.sendCmd('\r')
    if re.search(str3,c1) and  re.search(unidiag_case_pass,c1):
        log.success('Bios upgrade via BMC cancelled operation is successful')
    else:
        exit_unidiag_interface(deviceM)
        raise RuntimeError('Bios upgrade via BMC cancellatation operation failed')
    
    # Press y to continue the upgrade
    time.sleep(10)
    get_into_unidiag_submenu_option(deviceM, 'd', "upgrade bios via bmc")
    device.read_until_regexp("Please confirm that your firmware is proper and input 'y' to continue",timeout=20)
    device.sendCmd('y')
    time.sleep(5)
    c2=device.read_until_regexp("press any key to continue !", timeout=2400)
    device.sendCmd('\r')
    try:
        CommonKeywords.should_match_ordered_regexp_list(c2,upgrade_pattern)
        CommonKeywords.should_match_a_regexp(c2,unidiag_case_pass)
        log.success("Bios upgrade via BMC is successful.")
    except:
        exit_unidiag_interface(deviceM)
        raise RuntimeError('Bios upgrade via BMC failed')
    # Exit unidiag menu
    exit_unidiag_interface(deviceM)



def upgrade_th5_and_switch_asic(deviceM, upgrade_pattern):
    device= Device.getDeviceObject(deviceM)
    check_unidiag_system_versions(deviceM)
    str3 = "Upgrading SPI device j3_2."
    get_into_unidiag_submenu_option(deviceM, 'f', "Firmware Upgrade")
    get_into_unidiag_submenu_option(deviceM, 'g', "upgrade switch ASIC flash")
    
    # Press y to continue the upgrade J3_1
    device.read_until_regexp("Please confirm that your firmware is proper and input 'y' to continue",timeout=20)
    device.sendCmd('y')
    time.sleep(5)
    c1=device.read_until_regexp("Please confirm that your firmware is proper and input 'y' to continue", timeout=120)
    if re.search(str3,c1):
        log.success('TH5 and switch ASIC J3_1 is updated successfully')
    else:
        exit_unidiag_interface(deviceM)
        raise RuntimeError('TH5 and switch ASIC J3_1 updation failed ')
        
    time.sleep(5)
    device.sendCmd('y')
    c2=device.read_until_regexp("press any key to continue !", timeout=120)
    device.sendCmd('\r')
    try:
        CommonKeywords.should_match_ordered_regexp_list(c2,upgrade_pattern)
        CommonKeywords.should_match_a_regexp(c2,unidiag_case_pass)
        log.success("TH5 and Switch ASIC upgrade is successful.")
    except:
        exit_unidiag_interface(deviceM)
        raise RuntimeError('TH5 and Switch ASIC upgrade failed')
    # Exit unidiag menu
    exit_unidiag_interface(deviceM)
    
    
def minerva_stress_test(device, stress_option, stress_name):
    deviceObj = Device.getDeviceObject(device)
    get_into_unidiag_submenu_option(device, 'h', "Stress Test")
    get_into_unidiag_submenu_option(device, stress_option, stress_name)
    
    deviceObj.read_until_regexp("Please input the mode you are going to run test", timeout=20)
    deviceObj.sendCmd("time")
    deviceObj.read_until_regexp("Please input the number of seconds you are going to run", timeout=10)
    deviceObj.sendCmd(TIME_SECONDS)
    deviceObj.read_until_regexp("All tests are finished. Press .*Enter.*to proceed", timeout=90)
    deviceObj.sendCmd("\n\r")
    output1=deviceObj.read_until_regexp("press any key to continue", timeout=20)
    try:
        CommonKeywords.should_match_ordered_regexp_list(output1,stress_time_loop_pattern)
        CommonKeywords.should_match_a_regexp(output1,unidiag_case_pass)
        log.success(stress_name+" time Test is successful.")
    except:
        raise RuntimeError(stress_name+' time Test failed')
    
    time.sleep(10)
    get_into_unidiag_submenu_option(device, stress_option, stress_name)
    deviceObj.read_until_regexp("Please input the mode you are going to run test", timeout=20)
    deviceObj.sendCmd("loop")
    deviceObj.read_until_regexp("Please input the number of loops you are going to run", timeout=10)
    deviceObj.sendCmd(LOOP_COUNT)
    deviceObj.read_until_regexp("All tests are finished. Press .*Enter.* to proceed", timeout=150)
    deviceObj.sendCmd("\n\r")
    output1=deviceObj.read_until_regexp("press any key to continue", timeout=20)
    try:
        CommonKeywords.should_match_ordered_regexp_list(output1,stress_time_loop_pattern)
        CommonKeywords.should_match_a_regexp(output1,unidiag_case_pass)
        log.success(stress_name+" loop Test is successful.")
    except:
        raise RuntimeError(stress_name+' loop Test failed')
    
def get_device_ip(device):
    deviceObj = Device.getDeviceObject(device)
    output=deviceObj.executeCmd("ifconfig eth0")
    ip_pattern="inet (.*)  netmask (.*)  broadcast (.*)"
    device_ip=re.search(ip_pattern, output).group(1)
    return device_ip
    
def prepare_images(device, workspace, imageName, mode=default_mode):
    deviceObj = Device.getDeviceObject(device)
    CommonLib.create_dir(workspace, mode) 
    CommonLib.download_images(device, imageName)

def copy_to_device_firmware(device, imageName, fileName):
    deviceObj = Device.getDeviceObject(device)
    source_file=SwImage.getSwImage(imageName).localImageDir+"/"+fileName
    dest_path="/var/unidiag/firmware"
    cmd="cp "+source_file+" ."
    deviceObj.executeCmd("cd")
    deviceObj.executeCmd("cd "+dest_path)
    deviceObj.executeCmd(cmd)
    output=deviceObj.executeCmd("ls")
    CommonKeywords.should_match_a_regexp(output, fileName)
    
def rename_file(device, oldFileName, newFileFormat):
    deviceObj = Device.getDeviceObject(device)
    newFileName=newFileFormat+oldFileName
    cmd = "mv "+ oldFileName + " " +  newFileName
    deviceObj.executeCmd(cmd)
    output=deviceObj.executeCmd("ls")
    CommonKeywords.should_match_a_regexp(output, newFileName)
    
def rename_i210_flash_file(device, oldFileName, newFileName):
    deviceObj = Device.getDeviceObject(device)
    cmd = "mv "+ oldFileName + " " +  newFileName
    deviceObj.executeCmd(cmd)
    output=deviceObj.executeCmd("ls")
    CommonKeywords.should_match_a_regexp(output, newFileName)
    
def cleanup_device_after_update(device):
    deviceObj = Device.getDeviceObject(device)
    for i in range(5):
        deviceObj.sendCmd("q")
        time.sleep(5)
    deviceObj.executeCmd("cd")
    deviceObj.executeCmd("cd /var/unidiag/firmware")
    output=deviceObj.executeCmd("pwd")
    if("/var/unidiag/firmware" in output):
        deviceObj.executeCmd("rm -rf fw_*")
    deviceObj.executeCmd("cd")
    deviceObj.executeCmd("rm -rf "+workspace)
    
    
def minerva_diag_install_reinstall(device, diag_image, diag_version):
    deviceObj = Device.getDeviceObject(device)
    deviceObj.executeCmd("cd automation/DIAG")
    c1=deviceObj.executeCmd("ls")
    try:
        CommonKeywords.should_match_a_regexp(c1, diag_image)
    except:
        raise RuntimeError(diag_image+" is not present in folder")
    log.info("Extract diag tar file")
    deviceObj.executeCmd("tar -zxf "+diag_image, timeout=90)
    c2=deviceObj.executeCmd('ls')
    try:
        CommonKeywords.should_match_a_regexp(c2,"packages-minerva")
    except:
        raise RuntimeError("packages-minerva is not present")
    deviceObj.sendCmd("cd packages-minerva")
    c3=deviceObj.executeCmd('ls')
    try:
        CommonKeywords.should_match_a_regexp(c3,'install.sh')
    except:
        raise RuntimeError("'install.sh' file not present")
    deviceObj.sendCmd('chmod 777 install.sh')
    deviceObj.sendCmd('./install.sh')
    deviceObj.read_until_regexp(unidiag_install_success_regex, timeout=120)
    deviceObj.executeCmd('cd')
    #check_power_cycle_bmc(device) 

    log.info("Check diag version after Update")
    unidiag_version_check(device,diag_version) 
    log.success("Unidiag updated to version %s successfully" %diag_version)
    
def transfer_iob_fpga_files_to_bmc(deviceM):
    device = Device.getDeviceObject(device)
    device.switchToBmc()
    
    device.executeCmd("cd")
    device.executeCmd("cd /usr/local/bin")
    device.executeCmd("scp root@[fe80::2%usb0]:/var/unidiag/firmware/iob_update.sh .")
    try:
        device.read_until_regexp("Are you sure you want to continue connecting", timeout=20)
        device.sendCmd("yes")
    except:
        pass
    
    device= Device.getDeviceObject(device)
    device.switchToBmc()
    run_command('wedge_power.sh reset -s',prompt='login:',timeout=300)
    time.sleep(5)
    device.loginToNEWBMC()
    #device.switchToCpu()
    device.trySwitchToCpu()
    time.sleep(5)
    device.read_until_regexp("localhost login:", timeout=400)
    time.sleep(10)
    log.success("check power cycle test executed successfully")
    log.success('Successfully switched to CPU')
    c5=device.read_until_regexp('>>>', timeout=300)
    print('The value of c5 is',c5)
    for i in range(0,2):
        device.sendCmd('q')
        time.sleep(1)
    c6=device.read_until_regexp('exit',timeout=160)
    device.executeCmd('\r')
    
    
def upgrade_iob_fpga_from_bmc(deviceM, upgrade_pattern):
    device= Device.getDeviceObject(deviceM)
    check_unidiag_system_versions(deviceM)
    str3 = "User has cancelled upgrade"
    get_into_unidiag_submenu_option(deviceM, 'f', "Firmware Upgrade")
    get_into_unidiag_submenu_option(deviceM, 'e', "upgrade iob_fpga flash via bmc")
    
    # Press n to cancel the upgrade
    device.read_until_regexp("Please confirm that your firmware is proper and input 'y' to continue",timeout=20)
    device.sendCmd('n')
    time.sleep(5)
    c1=device.read_until_regexp("press any key to continue !", timeout=190)
    device.sendCmd('\r')
    if re.search(str3,c1) and  re.search(unidiag_case_pass,c1):
        log.success('IOB FPGA upgrade via BMC cancelled operation is successful')
    else:
        exit_unidiag_interface(deviceM)
        raise RuntimeError('IOB FPGA upgrade via BMC cancellatation operation failed')
    
    # Press y to continue the upgrade
    time.sleep(10)
    get_into_unidiag_submenu_option(deviceM, 'e', "upgrade iob_fpga flash via bmc")
    device.read_until_regexp("Please confirm that your firmware is proper and input 'y' to continue",timeout=20)
    device.sendCmd('y')
    time.sleep(5)
    c2=device.read_until_regexp("press any key to continue !", timeout=2400)
    device.sendCmd('\r')
    try:
        CommonKeywords.should_match_ordered_regexp_list(c2,upgrade_pattern)
        CommonKeywords.should_match_a_regexp(c2,unidiag_case_pass)
        log.success("IOB FPGA upgrade via BMC is successful.")
    except:
        exit_unidiag_interface(deviceM)
        raise RuntimeError('IOB FPGA upgrade via BMC failed')
    # Exit unidiag menu
    exit_unidiag_interface(deviceM)
    
@minipack3
def check_firmware_flash_upgrade(deviceM, firmware_name, firmware_option, upgrade_pattern, timeOutPeriod=200):

   device= Device.getDeviceObject(deviceM)
   check_unidiag_system_versions(deviceM)
   str3 = "User has cancelled upgrade."
   firmware_option_name="upgrade "+firmware_name
   get_into_unidiag_submenu_option(deviceM, 'f', "Firmware Upgrade")
   get_into_unidiag_submenu_option(deviceM, firmware_option, firmware_option_name)
   
   
   # Press n to cancel the upgrade
   device.read_until_regexp('to continue',timeout=20)
   device.sendCmd('n')
   time.sleep(5)
   c1=device.read_until_regexp("press any key to continue !", timeout=90)
   print('The value of c1 is ',c1)
   device.sendCmd('\r')
   if re.search(str3,c1) and  re.search(unidiag_case_pass,c1):
       log.success(firmware_name+' upgrade cancelled operation successful')
   else:
       exit_unidiag_interface(deviceM)
       raise RuntimeError(firmware_name+' upgrade cancellatation operation failed')
   
   # Press y to continue the upgrade
   time.sleep(10)
   get_into_unidiag_submenu_option(deviceM, firmware_option, firmware_option_name)
   device.read_until_regexp('to continue',timeout=20)
   device.sendCmd('y')
   time.sleep(5)
   c2=device.read_until_regexp("press any key to continue !", timeout=int(timeOutPeriod))
   print('The value of c1 is ',c1)
   device.sendCmd('\r')
   try:
       CommonKeywords.should_match_ordered_regexp_list(c2,upgrade_pattern)
       CommonKeywords.should_match_a_regexp(c2,unidiag_case_pass)
       log.success(firmware_name+' upgrade successful')
   except:
       exit_unidiag_interface(deviceM)
       raise RuntimeError(firmware_name+' upgrade failed')
   # Exit unidiag menu
   exit_unidiag_interface(deviceM)
   deviceObj.executeCmd("cd")
   deviceObj.executeCmd("cd /var/unidiag/firmware")
   output=deviceObj.executeCmd("pwd")
   if("/var/unidiag/firmware" in output):
       deviceObj.executeCmd("rm -rf fw_*")
   deviceObj.executeCmd("cd")

def prepare_bios_image_in_bmc_side(device, workspace, imageName, mode=default_mode):
    deviceObj = Device.getDeviceObject(device)
    deviceObj.switchToBmc()
    deviceObj.loginToNEWBMC()
    
    deviceObj.executeCmd("bind 'set enable-bracketed-paste off'")
    CommonLib.create_dir(workspace, mode) 
    CommonLib.download_images(device, imageName)
    
    deviceObj.executeCmd("cd "+workspace)
    output=deviceObj.executeCmd("ls")
    rename_file(device, Bios_new_image, bios_from_bmc_image)
    
    output=deviceObj.executeCmd("ls")
    deviceObj.executeCmd("cd /var")
    deviceObj.executeCmd("mkdir -p unidiag/firmware")
    cmd="cp "+workspace+"/fw_bios_from_bmc.bin ."
    deviceObj.executeCmd("cd unidiag/firmware")
    deviceObj.executeCmd(cmd)
    
    
    deviceObj.executeCmd("cd")
    deviceObj.trySwitchToCpu()
    
def prepare_iob_fpga_image_in_bmc_side(device, workspace, imageName, mode=default_mode):
    deviceObj = Device.getDeviceObject(device)
    deviceObj.switchToBmc()
    deviceObj.loginToNEWBMC()
    
    deviceObj.executeCmd("bind 'set enable-bracketed-paste off'")
    CommonLib.create_dir(workspace, mode) 
    CommonLib.download_images(device, imageName)
    
    deviceObj.executeCmd("cd "+workspace)
    output=deviceObj.executeCmd("ls")
    rename_file(device, IOB_new_image, iob_from_bmc_image)
    
    output=deviceObj.executeCmd("ls")
    deviceObj.executeCmd("cd /var")
    deviceObj.executeCmd("mkdir -p unidiag/firmware")
    
    iob_bmc_name=get_minerva_new_diag_version("DIAG",iob_from_bmc_image)
    cmd="cp "+workspace+"/"+iob_bmc_name+" ."
    deviceObj.executeCmd("cd unidiag/firmware")
    deviceObj.executeCmd(cmd)
    
    deviceObj.executeCmd("cd /usr/local/bin")
    deviceObj.executeCmd("cp "+workspace+"/iob_update.sh .")
    deviceObj.executeCmd("chmod 777 iob_update.sh")
    deviceObj.executeCmd("cd")
    deviceObj.trySwitchToCpu()
    
    
def check_upgraded_component_version(device, component_name, upgrade_version):
    deviceObj=Device.getDeviceObject(device)
    c1=run_command('unidiag',prompt='>>>')
    current_component_version=re.search(component_name+":\s+(.*)", c1).group(1)
    time.sleep(3)
    if(CommonKeywords.should_match_a_regexp(current_component_version,upgrade_version)):
        raise RuntimeError("%s current version is %s but it should be upgraded to %s " %(component_name,current_component_version,upgrade_version))
    log.success("%s current version is upgrdaed to %s successfully." %(component_name, upgrade_version))
    
    
    
    
    
    
    
    
    