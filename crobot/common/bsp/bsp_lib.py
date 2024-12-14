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
import CommonLib
import random
import Const
import subprocess
import json
import os
from Decorator import *
from bsp_variable import *
from datetime import datetime
from dataStructure import parser
#from errorsModule import testFailed
#from SensorCsv import SensorCsv
#from pkg_resources import parse_version
from SwImage import SwImage
import parser_bsp_lib as parserBsp

try:
    import DeviceMgr
    from Device import Device
except Exception as err:
    log.cprint(str(err))

deviceObj = DeviceMgr.getDevice()

@logThis
def DiagConnect():
    return deviceObj.login()

@logThis
def DiagDisconnect():
    return deviceObj.disconnect()

@logThis
def test_execute_command(device, test_cmd, mode, expected_result='None',timeout=60,found_flag=1):
    deviceObj = Device.getDeviceObject(device)
    output = deviceObj.executeCmd(test_cmd,mode,timeout)
    log.info("Output is:{}".format(output))
    if found_flag:
      if expected_result != 'None':
        for exp_val in expected_result:
           match = re.search(exp_val, output)
           if match:
               log.success("Found keyword: %s in output"%(match.group(0)))
           else:
               log.fail("Not found keyword: %s in output"%(exp_val))
               raise RuntimeError("test_execute_command: %s"%(test_cmd))
    else:
      if expected_result != 'None':
        for exp_val in expected_result:
           match = re.search(exp_val, output)
           if not match:
               log.success("Not Found keyword: %s in output"%(exp_val))
           else:
               log.fail("found keyword: %s in output"%(exp_val))
               raise RuntimeError("test_execute_command: %s"%(test_cmd))

@logThis
def verify_bsp_version(device, device_version=None):
    cmd = 'cat /etc/BSPVER'
    test_execute_command(device, cmd, CENTOS_MODE, device_version)

@logThis
def verify_fpga_version(device, device_type, device_version=None):
    if device_type.lower() == "dom1":
        cmd = 'cat /run/devmap/fpgas/IOB_FPGA/dom1_fpga_ver'
        test_execute_command(device, cmd, CENTOS_MODE, device_version)
    if device_type.lower() == "dom2":
        cmd = 'cat /run/devmap/fpgas/IOB_FPGA/dom2_fpga_ver'
        test_execute_command(device, cmd, CENTOS_MODE, device_version)
    if device_type.lower() == "iob":
        cmd = 'cat /run/devmap/fpgas/IOB_FPGA/fpga_ver'
        test_execute_command(device, cmd, CENTOS_MODE, device_version)
    if device_type.lower() == "dom":
        cmd = 'cat /run/devmap/fpgas/IOB_FPGA/dom_fpga_ver'
        test_execute_command(device, cmd, CENTOS_MODE, device_version)

@logThis
def verify_th5_version(device, th5_version):
    deviceObj = Device.getDeviceObject(device)
    err_count = 0
    CommonLib.change_dir('/usr/local/cls_diag/SDK', CENTOS_MODE)
    cmd = 'chmod +x auto_load_user.sh'
    deviceObj.sendline(cmd)
    cmd = './auto_load_user.sh'
    time.sleep(30)
    deviceObj.flush()
    deviceObj.sendline(cmd)
    cmd = 'dsh'
    deviceObj.sendline(cmd)
    deviceObj.flush()
    time.sleep(5)
    pcie_cmd = 'pciephy fwinfo'
    output = deviceObj.sendCmd(pcie_cmd)
    time.sleep(2)
    output += deviceObj.read_until_regexp('Failure logs:',timeout=30)
    deviceObj.sendline('exit')
    time.sleep(1)
    deviceObj.sendline('exit')
    time.sleep(1)
    deviceObj.sendline('cd \n')
    time.sleep(30)
    deviceObj.getPrompt(CENTOS_MODE)
    log.info("Output is:{}".format(output))
    parsed_output = parserBsp.parse_th5_version(output)
    log.info("parsed output is:{}".format(parsed_output))
    err_count += CommonLib.compare_input_dict_to_parsed(parsed_output, th5_version)
    if err_count:
        log.fail("Actual device output is {}".format(parsed_output))
        raise RuntimeError("Expected th5 version is not present in the system")
    else:
        log.success("Expected th5 version is present in the system")

@logThis
def verify_firmware_version(device, fw_type, expected_version):
    deviceObj = Device.getDeviceObject(device)
    output = deviceObj.sendCmd('unidiag\n')
    output += deviceObj.read_until_regexp('Exit Menu',timeout=10)
    log.info("Output is:{}".format(output))
    deviceObj.sendCmd('q')
    time.sleep(1)
    deviceObj.read_until_regexp('exit',timeout=5)
    deviceObj.sendCmd('q\r')
    device_scm_version = re.findall('SCM CPLD : (\S+)',output)
    device_smb_version = re.findall('SMB CPLD : (\S+)',output)
    device_mcb_version = re.findall('MCB CPLD : (\S+)',output)
    device_smb1_version = re.findall('SMB CPLD 1: (\S+)',output)
    device_smb2_version = re.findall('SMB CPLD 2: (\S+)',output)
    device_pwr_version = re.findall('PWR CPLD: *(\S+)',output)
    device_iob_version = re.findall('IOB  FPGA : *(\S+)',output)
    if device_iob_version == []:
        device_iob_version = re.findall('IOB FPGA: *(\S+)',output)
    device_dom1_version = re.findall('DOM1 FPGA : (\S+)',output)
    device_dom2_version = re.findall('DOM2 FPGA : (\S+)',output)
    device_dom_version = re.findall('DOM FPGA: *(\S+)',output)
    flag_value = 1
    actual_version = ""
    if 'mcb' in fw_type:
        if not device_mcb_version == expected_version:
            flag_value , actual_version = 0 , device_mcb_version
    elif 'scm' in fw_type:
        if not device_scm_version == expected_version:
            flag_value , actual_version = 0 , device_scm_version
    elif 'smb1' in fw_type:
        if not device_smb1_version == expected_version:
            flag_value , actual_version = 0 , device_smb1_version
    elif 'smb2' in fw_type:
        if not device_smb2_version == expected_version:
            flag_value , actual_version = 0 , device_smb2_version
    elif 'smb' in fw_type:
        if not device_smb_version == expected_version:
            flag_value , actual_version = 0 , device_smb_version
    elif 'pwr' in fw_type:
        if not device_pwr_version == expected_version:
            flag_value , actual_version = 0 , device_pwr_version
    elif 'iob' in fw_type:
        if not device_iob_version == expected_version:
            flag_value , actual_version = 0 , device_iob_version
    elif 'dom1' in fw_type:
        if not device_dom1_version == expected_version:
            flag_value , actual_version = 0 , device_dom1_version
    elif 'dom2' in fw_type:
        if not device_dom2_version == expected_version:
            flag_value , actual_version = 0 , device_dom2_version
    elif 'dom' in fw_type:
        if not device_dom_version == expected_version:
            flag_value , actual_version = 0 , device_dom_version

    if flag_value:
       log.success("Expected {} firmware version {} is present in the device".\
               format(fw_type,expected_version))
    else:
       log.fail("Expected {} firmware version {} is not present in the device".\
               format(fw_type,expected_version))
       raise RuntimeError("Actual {} firmware version {} is present in the device".\
               format(fw_type,actual_version))

@logThis
def copy_bsp_package_files(device):
    deviceObj = Device.getDeviceObject(device)
    cmd = 'mkdir ' + bsp_package_file_path1
    deviceObj.sendCmd(cmd)
    cmd = 'mkdir ' + bsp_package_file_path2
    deviceObj.sendCmd(cmd)
    cmd = 'cd ' + bsp_folder
    deviceObj.sendCmd(cmd)
    cmd = 'mv ' + bsp_package_file1 + " " + bsp_package_file_path1
    deviceObj.sendCmd(cmd)
    cmd = 'mv ' + bsp_package_file1_zip + " " + bsp_package_file_path2
    deviceObj.sendCmd(cmd)
    cmd = 'mv ' + bsp_package_file2 + " " + bsp_package_file_path2
    deviceObj.sendCmd(cmd)
    cmd = 'mv ' + bsp_package_file2_zip + " " + bsp_package_file_path2
    deviceObj.sendCmd(cmd)
    file_name = SwImage.getSwImage(SwImage.BSP).libicuuc
    cmd = 'mv ' + file_name + " " + "/usr/lib64/"
    deviceObj.sendCmd(cmd)
    file_name = SwImage.getSwImage(SwImage.BSP).libicudata
    cmd = 'mv ' + file_name + " " + "/usr/lib64/"
    deviceObj.sendCmd(cmd)
    file_name = SwImage.getSwImage(SwImage.BSP).libicui18n
    cmd = 'mv ' + file_name + " " + "/usr/lib64/"
    deviceObj.sendCmd(cmd)
    cmd = 'cd '
    deviceObj.sendCmd(cmd)

@logThis
def bsp_driver_update(device, program_method, isUpgrade = True):
    deviceObj = Device.getDeviceObject(device)
    package_file_path = SwImage.getSwImage(SwImage.BSP).newlocalImageDir\
            if isUpgrade else SwImage.getSwImage(SwImage.BSP).oldlocalImageDir
    package_file = SwImage.getSwImage(SwImage.BSP).newImage \
                if isUpgrade else SwImage.getSwImage(SwImage.BSP).oldImage
    bsp_zip_file = SwImage.getSwImage(SwImage.BSP).newImageZip\
            if isUpgrade else SwImage.getSwImage(SwImage.BSP).oldImageZip
    cmd = 'cd ' + package_file_path
    deviceObj.sendCmd(cmd)
    if program_method == 'remove':
        if fb_variant == 'minerva':
           folder_name = re.sub('.tar', "", package_file)
           cmd = 'cd ' + folder_name
           deviceObj.sendCmd(cmd)
           cmd = 'cd fb*'
           deviceObj.sendCmd(cmd)
        cmd = './setupBSP remove'
        output = deviceObj.sendCmd(cmd)
        output += deviceObj.read_until_regexp('FBOSS BSP driver remove completed',timeout=60)
        cmd = 'cd \n'
        deviceObj.sendCmd(cmd)
    else:
        if fb_variant == 'minipack3' or fb_variant == 'minerva':
            cmd = 'unzip -o ' + str(bsp_zip_file)
            deviceObj.sendCmd(cmd)
            deviceObj.sendCmd(cmd)
            cmd = 'chmod +x setupBSP'
            deviceObj.sendCmd(cmd)
            cmd = './setupBSP install {}'.format(package_file)
            output = deviceObj.sendCmd(cmd)
            output += deviceObj.read_until_regexp('FBOSS BSP driver install completed',timeout=60)
            if isUpgrade:
               cmd = 'bootstrap.sh'
               output += deviceObj.sendCmd(cmd)
            else:
               if fb_variant == 'minipack3':
                  cmd = 'bootstrap.sh montblanc'
               elif fb_variant == 'minerva':
                  cmd = 'bootstrap.sh'
               output += deviceObj.sendCmd(cmd)
            output += deviceObj.read_until_regexp('attach spi7.0 to spidev driver',timeout=300)
        elif fb_variant == 'minerva':
           cmd = 'unzip -o ' + str(bsp_zip_file)
           deviceObj.sendCmd(cmd)
           folder_name = re.sub('.tar', "", package_file)
           cmd = 'mkdir ' + folder_name
           deviceObj.sendCmd(cmd)
           cmd = 'tar -xvf ' + package_file + " -C " + folder_name
           deviceObj.sendCmd(cmd)
           cmd = 'mv fbiob-util ' + folder_name + '/'
           deviceObj.sendCmd(cmd)
           cmd = 'mv setupBSP '  + folder_name + '/'
           deviceObj.sendCmd(cmd)
           cmd = 'cd ' + folder_name
           deviceObj.sendCmd(cmd)
           cmd = 'tar -xvf fboss-kmods.tar'
           deviceObj.sendCmd(cmd)
           cmd = 'chmod +x fbiob-util'
           deviceObj.sendCmd(cmd)
           cmd = 'chmod +x setupBSP'
           deviceObj.sendCmd(cmd)
           cmd = './setupBSP install'
           output = deviceObj.sendCmd(cmd)
           output += deviceObj.read_until_regexp('fboss bsp driver load completed',timeout=60)
           cmd = 'bootstrap.sh'
           output += deviceObj.sendCmd(cmd)
           output += deviceObj.read_until_regexp('Instantiated device adc128d818 at 0x35',timeout=300)
        cmd = 'cd \n'
        deviceObj.sendCmd(cmd)
    log.info("Output is:{}".format(output))
    if 'Error' in output:
        log.fail("Failed log is:" + "\n" + output)
        raise RuntimeError("BSP driver uninstall/install failed")
    else:
        log.success("BSP driver uninstall/install passed")

@logThis
def check_bsp_device_folder(device, program_method, expected_list, isUpgrade = True):
    cmd = 'ls /run/devmap/'
    if program_method == 'remove':
        test_execute_command(device, cmd, CENTOS_MODE, expected_list,10,0)
    else:
        test_execute_command(device, cmd, CENTOS_MODE, expected_list,10)
    if isUpgrade:
        cmd = "ls /run/devmap/cplds/"
        test_execute_command(device, cmd, CENTOS_MODE, cplds_folder,10)
        cmd = "ls /run/devmap/eeprom/"
        test_execute_command(device, cmd, CENTOS_MODE, eeprom_folder,10)
        cmd = "ls /run/devmap/fpgas/"
        test_execute_command(device, cmd, CENTOS_MODE, fpgas_folder,10)
        cmd = "ls /run/devmap/flashes/"
        test_execute_command(device, cmd, CENTOS_MODE, flashes_folder,10)
        cmd = "ls /run/devmap/gpio/"
        test_execute_command(device, cmd, CENTOS_MODE, gpio_folder,10)
        cmd = "ls /run/devmap/i2c-busses/"
        test_execute_command(device, cmd, CENTOS_MODE, i2c_busses_folder,10)
        cmd = "ls /run/devmap/sensors/"
        test_execute_command(device, cmd, CENTOS_MODE, sensors_folder,10)
        cmd = "ls /run/devmap/xcvrs/"
        if xcvrs_folder_check:
           test_execute_command(device, cmd, CENTOS_MODE, xcvrs_folder,10)
        cmd = "ls /run/devmap/watchdogs/"
        test_execute_command(device, cmd, CENTOS_MODE, watchdogs_folder,10)


@logThis
def minipack3_online_update(device, fw_type, isUpgrade = True):
    if 'dom' in fw_type:
        package_file_path = SwImage.getSwImage(SwImage.FPGA).localImageDir
        package_file = SwImage.getSwImage(SwImage.FPGA).newImage \
                if isUpgrade else SwImage.getSwImage(SwImage.FPGA).oldImage
    elif 'iob' in fw_type:
        package_file_path = SwImage.getSwImage(SwImage.IOB).localImageDir
        package_file = SwImage.getSwImage(SwImage.IOB).newImage \
                if isUpgrade else SwImage.getSwImage(SwImage.IOB).oldImage
    elif 'th5' in fw_type:
        package_file_path = SwImage.getSwImage(SwImage.TH5).localImageDir
        package_file = SwImage.getSwImage(SwImage.TH5).newImage \
                if isUpgrade else SwImage.getSwImage(SwImage.TH5).oldImage
    elif 'mcb' in fw_type:
        package_file_path = SwImage.getSwImage(SwImage.MCB).localImageDir
        package_file = SwImage.getSwImage(SwImage.MCB).newImage \
                if isUpgrade else SwImage.getSwImage(SwImage.MCB).oldImage
    elif 'scm' in fw_type:
        package_file_path = SwImage.getSwImage(SwImage.SCM).localImageDir
        package_file = SwImage.getSwImage(SwImage.SCM).newImage \
                if isUpgrade else SwImage.getSwImage(SwImage.SCM).oldImage
    elif 'smb' in fw_type:
        package_file_path = SwImage.getSwImage(SwImage.SMB).localImageDir
        package_file = SwImage.getSwImage(SwImage.SMB).newImage \
                if isUpgrade else SwImage.getSwImage(SwImage.SMB).oldImage
    else:
        log.info("Unsupported firmware type")
        return
    if fw_type.lower()=='iob':
        cmd = package_file_path + '/' + 'spi-utils.sh ' + 'iob ' +\
                'program '  + package_file_path + '/' + package_file
        #***Work around for R4063-35 ****
        test_execute_command(device, cmd, CENTOS_MODE)
    elif fw_type.lower()=='dom1':
        cmd = package_file_path + '/' + 'spi-utils.sh ' + 'dom1 ' +\
                'program '  + package_file_path + '/' + package_file
    elif fw_type.lower()=='dom2':
        cmd = package_file_path + '/' + 'spi-utils.sh ' + 'dom2 ' +\
                'program '  + package_file_path + '/' + package_file
    elif fw_type.lower()=='th5':
        cmd = package_file_path + '/' + 'spi-utils.sh ' + 'th5 ' +\
                'program '  + package_file_path + '/' + package_file
    elif fw_type.lower()=='mcb':
        cmd = package_file_path + '/' + 'spi-utils.sh ' + 'mcbcpld ' +\
                'program '  + package_file_path + '/' + package_file
    elif fw_type.lower()=='scm':
        cmd = package_file_path + '/' + 'spi-utils.sh ' + 'scmcpld ' +\
                'program '  + package_file_path + '/' + package_file
    elif fw_type.lower()=='smb':
        cmd = package_file_path + '/' + 'spi-utils.sh ' + 'smbcpld ' +\
                'program '  + package_file_path + '/' + package_file
    else:
        log.info("Unsupported firmware type")
    test_execute_command(device, cmd, CENTOS_MODE, ["Erase/write done"],120)
    time.sleep(30)
    return

@logThis
def power_reset_chassis(device,pwr_cpld=False):
    deviceObj = Device.getDeviceObject(device)
    if pwr_cpld:
       cmd = 'i2cset -f -y {} {} {} {}'.\
           format(pwr_cpld_bus_no,pwr_cpld_addr,pwr_reset_reg_addr,pwr_reset_reg_val)
    else:
       deviceObj.getPrompt(OPENBMC_MODE)
       cmd = 'wedge_power.sh reset -s'
    booting_msg = 'OpenBMC Release.*'
    output = deviceObj.sendCmdRegexp(cmd, booting_msg, timeout=120)
    time.sleep(300)
    deviceObj.switchToBmc()
    deviceObj.sendCmd('sol.sh\r')
    deviceObj.sendCmd('\n')
    for i in range(0,3):
        deviceObj.sendCmd('q')
        time.sleep(1)
    deviceObj.read_until_regexp('exit',timeout=60)
    deviceObj.executeCmd('q\r')
    time.sleep(5)
    deviceObj.sendCmd('\n')
    deviceObj.switchToCpu()
    #Below workaround for eth0 nw issue
    deviceObj.executeCmd('ifconfig eth0 down \r')
    time.sleep(2)
    deviceObj.executeCmd('ifconfig eth0 up \r')
    time.sleep(30)
    return

@logThis
def reboot_come(device):
    deviceObj = Device.getDeviceObject(device)
    cmd = 'reboot'
    booting_msg = 'automatic login'
    output = deviceObj.sendCmdRegexp(cmd, booting_msg, timeout=360)
    time.sleep(90)
    deviceObj.sendCmd('\n')
    deviceObj.sendCmd('\n')
    for i in range(0,3):
        deviceObj.sendCmd('q')
        time.sleep(1)
    deviceObj.read_until_regexp('exit',timeout=60)
    deviceObj.executeCmd('q\r')
    time.sleep(5)
    deviceObj.sendCmd('\n')
    deviceObj.switchToCpu()
    #Below workaround for eth0 nw issue
    deviceObj.executeCmd('ifconfig eth0 down \r')
    time.sleep(2)
    deviceObj.executeCmd('ifconfig eth0 up \r')
    time.sleep(5)
    return

@logThis
def disable_write_protect(device, eeprom_type):
    deviceObj = Device.getDeviceObject(device)
    if 'OOB_EEPROM' in eeprom_type or '88E6321' in eeprom_type:
        if fb_variant == 'minipack3':
            cmd = 'i2cset -f -y {} {} {} {} '.\
            format(scm_cpld_bus_no,scm_cpld_addr,oob_reg_addr,oob_reg_val2)
            test_execute_command(device, cmd, CENTOS_MODE)
            cmd = 'gpioset gpiochip0 {}'.format(gpio_line)
            test_execute_command(device, cmd, CENTOS_MODE)
            cmd = 'echo {} {} > /sys/bus/i2c/devices/i2c-{}/new_device'.\
            format(eeprom_chip_type,scm_eeprom_addr,scm_eeprom_bus_no)
            test_execute_command(device, cmd, CENTOS_MODE, ["EEPROM, writable"],10)
    elif 'FCB' in eeprom_type:
        if fb_variant == 'minipack3':
            cmd = 'i2cset -f -y {} {} {} {} '.\
            format(mcb_cpld_bus_no,mcb_cpld_addr,fcb_reg_addr,fcb_reg_val2)
            test_execute_command(device, cmd, CENTOS_MODE)
    elif 'TH5' in eeprom_type:
        if fb_variant == 'minerva':
            cmd = 'echo {} > /sys/bus/i2c/devices/i2c-{}/delete_device'.\
            format(come_eeprom_addr,come_eeprom_bus_no)
            deviceObj.sendCmd(cmd)
            cmd = 'i2cset -f -y {} {} {} {} '.\
            format(scm_cpld_bus_no,scm_cpld_addr,come_reg_addr,come_reg_val2)
            test_execute_command(device, cmd, CENTOS_MODE)
            '''
            cmd = 'gpioset gpiochip0 {}'.format(gpio_line)
            test_execute_command(device, cmd, CENTOS_MODE)
            '''
            cmd = 'echo {} {} > /sys/bus/i2c/devices/i2c-{}/new_device'.\
            format(eeprom_chip_type,come_eeprom_addr,come_eeprom_bus_no)
            test_execute_command(device, cmd, CENTOS_MODE, ["EEPROM, writable"],10)
    elif 'SMB' in eeprom_type:
        if fb_variant == 'minerva':
            cmd = 'i2cset -f -y {} {} {} {} '.\
            format(smb_cpld_bus_no,smb_cpld_addr,smb_reg_addr,smb_reg_val2)
            test_execute_command(device, cmd, CENTOS_MODE)

@logThis
def enable_write_protect(device, eeprom_type):
    deviceObj = Device.getDeviceObject(device)
    if 'OOB_EEPROM' in eeprom_type or '88E6321' in eeprom_type:
        cmd = 'echo {} > /sys/bus/i2c/devices/i2c-{}/delete_device'.\
            format(scm_eeprom_addr,scm_eeprom_bus_no)
        test_execute_command(device, cmd, CENTOS_MODE, [" Deleting device"],10)
        if fb_variant == 'minipack3':
            cmd = 'i2cset -f -y {} {} {} {} '.\
            format(scm_cpld_bus_no,scm_cpld_addr,oob_reg_addr,oob_reg_val1)
            test_execute_command(device, cmd, CENTOS_MODE)
    elif 'FCB' in eeprom_type:
        if fb_variant == 'minipack3':
            cmd = 'i2cset -f -y {} {} {} {} '.\
            format(mcb_cpld_bus_no,mcb_cpld_addr,fcb_reg_addr,fcb_reg_val1)
            test_execute_command(device, cmd, CENTOS_MODE)
    elif 'TH5' in eeprom_type:
        cmd = 'echo {} > /sys/bus/i2c/devices/i2c-{}/delete_device'.\
            format(come_eeprom_addr,come_eeprom_bus_no)
        test_execute_command(device, cmd, CENTOS_MODE, [" Deleting device"],10)
        if fb_variant == 'minerva':
            cmd = 'i2cset -f -y {} {} {} {} '.\
            format(scm_cpld_bus_no,scm_cpld_addr,come_reg_addr,come_reg_val1)
            test_execute_command(device, cmd, CENTOS_MODE)
    elif 'SMB' in eeprom_type:
        if fb_variant == 'minerva':
            cmd = 'i2cset -f -y {} {} {} {} '.\
            format(smb_cpld_bus_no,smb_cpld_addr,smb_reg_addr,smb_reg_val1)
            test_execute_command(device, cmd, CENTOS_MODE)


@logThis
def verify_eeprom_readable(device, eeprom_type):
    deviceObj = Device.getDeviceObject(device)
    if 'OOB' in eeprom_type:
        cmd = "hexdump -C /sys/bus/i2c/devices/i2c-{}/{}-{}/eeprom".\
                format(scm_eeprom_bus_no,scm_eeprom_bus_no,scm_eeprom_addr2)
        output = deviceObj.sendCmd(cmd)
        output += deviceObj.read_until_regexp('00000100',timeout=30)
    log.info("Output is:{}".format(output))

@logThis
def oob_firmware_update(device, isUpgrade = True):
    deviceObj = Device.getDeviceObject(device)
    package_file_path = SwImage.getSwImage(SwImage.OOB).localImageDir
    package_file = SwImage.getSwImage(SwImage.OOB).newImage \
                if isUpgrade else SwImage.getSwImage(SwImage.OOB).oldImage
    input_file = package_file_path + '/' + package_file
    output_file = "/sys/bus/i2c/devices/i2c-{}/{}-{}/eeprom".\
                format(scm_eeprom_bus_no,scm_eeprom_bus_no,scm_eeprom_addr2)
    cmd = "dd if={} of={}".format(input_file,output_file)
    test_execute_command(device, cmd, CENTOS_MODE, ["bytes copied"],60)

@logThis
def get_ipv6_address(device, mode):
    deviceObj.getPrompt(mode)
    output = deviceObj.sendCmd('ifconfig')
    time.sleep(2)
    output += deviceObj.read_until_regexp('usb0',timeout=10)
    log.info("Output is:{}".format(output))
    parsed_output = parserBsp.parse_ifconfig(output)
    log.info("parsed output is:{}".format(parsed_output))
    cmd = 'ping6 -c 5 {}%eth0.4088'.format(parsed_output['Ipv6_address'])
    test_execute_command(device, cmd, OPENBMC_MODE, ["5 packets received"],30)
    deviceObj.getPrompt(CENTOS_MODE)

@logThis
def set_fan_speed(device, pwm_number, expected_speed):
    #Below formula for software expected speed
    #pwm_val = int((int(expected_speed) * fan_speen_cpld_max) / 100)
    #Below formula for adjusting to the actual pwm set provided in the JIRA
    pwm_val = int(((int(expected_speed) /100)* 50) - 1)
    pwm_val = str(pwm_val)
    cmd  = "echo {} > /run/devmap/cplds/FAN_CPLD/hwmon/{}/pwm{}".format(pwm_val,hw_monitor,pwm_number)
    test_execute_command(device, cmd, CENTOS_MODE)

@logThis
def get_fan_speed(device, pwm_number, expected_speed):
    #pwm_val = int((int(expected_speed) * fan_speen_cpld_max) / 100)
    #pwm_val = str(pwm_val)
    pwm_val = int(((int(expected_speed) /100)* 50) - 1)
    pwm_val = str(pwm_val)
    cmd  = "cat /run/devmap/cplds/FAN_CPLD/hwmon/{}/pwm{}".format(hw_monitor,pwm_number)
    test_execute_command(device, cmd, CENTOS_MODE, [pwm_val],5)

@logThis
def verify_fan_rpm_in_range(fan_num, rpm, min_rpm, max_rpm):
    if min_rpm <= rpm <= max_rpm:
        log.success("Fan %d RPM: %d is in range %d-%d"%(fan_num, rpm, min_rpm, max_rpm))
    else:
        log.fail("Fan %d RPM: %d is out of range %d-%d"%(fan_num, rpm, min_rpm, max_rpm))
        raise RuntimeError("Expected rpm is not present, fan number %d & rpm %d"%(fan_num,rpm))

@logThis
def verify_fan_speed(device, pwm_number, expected_speed):
    cmd = "time sensors {}".format(fan_sensor_name)
    output = deviceObj.sendCmd(cmd)
    output += deviceObj.read_until_regexp('sys',timeout=30)
    log.info("Output is:{}".format(output))
    expected_speed = int(expected_speed) / 100
    expected_rpm1 = int(fan_max_rpm1 * expected_speed)
    expected_rpm2 = int(fan_max_rpm2 * expected_speed)
    min_rpm1 = expected_rpm1 - int(expected_rpm1 * speed_deviation)
    max_rpm1 = expected_rpm1 + int(expected_rpm1 * speed_deviation)
    min_rpm2 = expected_rpm2 - int(expected_rpm2 * speed_deviation)
    max_rpm2 = expected_rpm2 + int(expected_rpm2 * speed_deviation)
    fan_num_list = [pwm_number*2-1 , pwm_number*2]
    for fan_num in fan_num_list:
       log.info("fan_num is:{}".format(fan_num))
       rpm_output = parserBsp.parse_fanSensor(fan_num,output)
       if fan_num_list.index(fan_num) == 0:
          log.info("Verify fan number{} with rpm range in min_rpm {}, max_rpm {} ".\
               format(fan_num,min_rpm1,max_rpm1))
          verify_fan_rpm_in_range(fan_num,rpm_output,min_rpm1,max_rpm1)
       else:
          log.info("Verify fan number{} with rpm range in min_rpm {}, max_rpm {} ".\
               format(fan_num,min_rpm2,max_rpm2))
          verify_fan_rpm_in_range(fan_num,rpm_output,min_rpm2,max_rpm2)

@logThis
def verify_gpio_controllers(device,gpio_chip):
    cmd = "gpiodetect"
    test_execute_command(device, cmd, CENTOS_MODE, [gpio_chip],5)

def verify_gpio_lines(device,gpio_lines):
    cmd = "time gpioinfo"
    output = deviceObj.sendCmd(cmd)
    output += deviceObj.read_until_regexp('sys',timeout=30)
    log.info("Output is:{}".format(output))
    for i in range(0,gpio_lines):
        status = parserBsp.parse_gpioLines(i,output)
        if status:
            log.success("gpio line number {} is detected properly".format(i))
        else:
            raise RuntimeError("gpio line number {} is not detected properly".format(i))

@logThis
def verify_i2c_buses(device,i2c_buses):
    cmd = "time i2cdetect -l"
    output = deviceObj.sendCmd(cmd)
    output += deviceObj.read_until_regexp('sys',timeout=30)
    log.info("Output is:{}".format(output))
    for i in range(0,i2c_buses+1):
        status = parserBsp.parse_i2cBuses(i,output)
        if status:
            log.success("i2c bus number {} is detected properly".format(i))
        else:
            raise RuntimeError("i2c bus number {} is not detected properly".format(i))

@logThis
def verify_gpio_line_status(device,gpio_line,expected_status):
    cmd = "time gpioinfo"
    output = deviceObj.sendCmd(cmd)
    output += deviceObj.read_until_regexp('sys',timeout=30)
    log.info("Output is:{}".format(output))
    out_status = parserBsp.parse_gpioLines(gpio_line,output,True)
    if out_status == expected_status:
       log.success("gpio line number {} is set properly as {}".format(gpio_line,out_status))
    else:
       raise RuntimeError("gpio line number {} is not set properly as {}".format(gpio_line,expected_status))


@logThis
def get_gpio_line(device,gpio_line,expected_value):
    cmd = "gpioget {} {}".format(gpio_chip,gpio_line)
    test_execute_command(device, cmd, CENTOS_MODE, [expected_value],5)

@logThis
def set_gpio_line(device,gpio_line,set_value):
    cmd = "gpioset {} {}={}".format(gpio_chip,gpio_line,set_value)
    test_execute_command(device, cmd, CENTOS_MODE)

@logThis
def unload_gpio_driver(device):
    cmd = "rmmod gpio_fbiob"
    test_execute_command(device, cmd, CENTOS_MODE)
    time.sleep(5)
    cmd = "time gpioinfo"
    output = deviceObj.sendCmd(cmd)
    output += deviceObj.read_until_regexp('sys',timeout=30)
    if not re.search("line.*active-high",output):
        log.success("gpio driver unload is successful")
    else:
       raise RuntimeError("gpio driver is not removed")

@logThis
def load_gpio_driver(device,check=True):
    cmd = "modprobe gpio_fbiob"
    if check:
       test_execute_command(device, cmd, CENTOS_MODE, ['registered'],10)
    else:
       test_execute_command(device, cmd, CENTOS_MODE)
    time.sleep(5)

@logThis
def spi_driver_override(device):
    cmd = "echo spidev > /sys/bus/spi/devices/{}/driver_override".format(spi_line_number)
    test_execute_command(device, cmd, CENTOS_MODE)

@logThis
def spi_driver_bind(device):
    cmd = "echo {} > /sys/bus/spi/drivers/spidev/bind".format(spi_line_number)
    test_execute_command(device, cmd, CENTOS_MODE)
    time.sleep(5)
    cmd = "ls -l {}".format(spi_dev_path)
    expected_output = "crw.* root root .* {}".format(spi_dev_path)
    test_execute_command(device, cmd, CENTOS_MODE, [expected_output],10)

@logThis
def spi_driver_unbind(device):
    cmd = "echo {} > /sys/bus/spi/drivers/spidev/unbind".format(spi_line_number)
    test_execute_command(device, cmd, CENTOS_MODE)
    time.sleep(5)
    cmd = "ls -l {}".format(spi_dev_path)
    expected_output = "crw.* root root .* {}".format(spi_dev_path)
    test_execute_command(device, cmd, CENTOS_MODE, [expected_output],10,0)

@logThis
def verify_cpld_read_write(device,cpld_type):
    if 'scm' in cpld_type:
        bus_no = scm_cpld_bus_no
        cpld_addr = scm_cpld_addr
        reg_addr = scm_reg_addr
        reg_val = scm_reg_val
    elif 'mcb' in cpld_type:
        bus_no = mcb_cpld_bus_no
        cpld_addr = mcb_cpld_addr
        reg_addr = mcb_reg_addr
        reg_val = mcb_reg_val
    elif 'smb1' in cpld_type:
        bus_no = smb1_cpld_bus_no
        cpld_addr = smb1_cpld_addr
        reg_addr = smb1_reg_addr
        reg_val = smb1_reg_val
    elif 'smb2' in cpld_type:
        bus_no = smb2_cpld_bus_no
        cpld_addr = smb2_cpld_addr
        reg_addr = smb2_reg_addr
        reg_val = smb2_reg_val
    elif 'smb' in cpld_type:
        bus_no = smb_cpld_bus_no
        cpld_addr = smb_cpld_addr
        reg_addr = smb_reg_addr
        reg_val = smb_reg_val
    elif 'pwr' in cpld_type:
        bus_no = pwr_cpld_bus_no
        cpld_addr = pwr_cpld_addr
        reg_addr = pwr_reg_addr
        reg_val = pwr_reg_val

    cmd = "i2cget -y -f {} {} {}".format(bus_no,cpld_addr,reg_addr)
    test_execute_command(device, cmd, CENTOS_MODE, [reg_val],10)
    cmd = 'i2cset -f -y {} {} {} {} '.format(bus_no,cpld_addr,reg_addr,cpld_write_val)
    test_execute_command(device, cmd, CENTOS_MODE)
    time.sleep(2)
    cmd = "i2cget -y -f {} {} {}".format(bus_no,cpld_addr,reg_addr)
    test_execute_command(device, cmd, CENTOS_MODE, [cpld_write_val],10)
    cmd = 'i2cset -f -y {} {} {} {} '.format(bus_no,cpld_addr,reg_addr,reg_val)
    test_execute_command(device, cmd, CENTOS_MODE)
    time.sleep(2)
    cmd = "i2cget -y -f {} {} {}".format(bus_no,cpld_addr,reg_addr)
    test_execute_command(device, cmd, CENTOS_MODE, [reg_val],10)

@logThis
def flashrom_version_check(device):
    cmd = "flashrom -v"
    test_execute_command(device, cmd, CENTOS_MODE, [flashrom_version],10)
    cmd = "flashrom -h"
    test_execute_command(device, cmd, CENTOS_MODE, ['You can specify one of .* or no operation'],10)

@logThis
def ddtool_version_check(device):
    cmd = "dd --version"
    test_execute_command(device, cmd, CENTOS_MODE, [ddtool_version],10)
    cmd = "dd --help"
    test_execute_command(device, cmd, CENTOS_MODE, ["info .*coreutils.* dd invocation"],10)


@logThis
def verify_system_version(device, check_all=1, fw_type=None, expected_version=None):
    deviceObj = Device.getDeviceObject(device)
    err_count = 0
    output = deviceObj.sendCmd('unidiag\n')
    output += deviceObj.read_until_regexp('Exit Menu',timeout=10)
    log.info("Output is:{}".format(output))
    deviceObj.sendCmd('q')
    time.sleep(1)
    deviceObj.read_until_regexp('exit',timeout=5)
    deviceObj.sendCmd('q\r')
    parsed_output = parserBsp.parse_unidiag_output(output)
    log.info("parsed output is:{}".format(parsed_output))
    err_count += CommonLib.compare_input_dict_to_parsed(parsed_output, unidiag_version)
    if err_count:
        log.fail("Actual device output is {}".format(parsed_output))
        raise RuntimeError("Expected system version is not present")
    else:
        log.success("Expected system version is present")

@logThis
def verify_i2cScan_unidiag_system_test(device):
    deviceObj = Device.getDeviceObject(device)
    flag=True
    output = deviceObj.sendCmd('unidiag\n')
    output += deviceObj.read_until_regexp('to run a test',timeout=10)
    output += deviceObj.sendCmd('b\n')
    output += deviceObj.read_until_regexp('to run a test',timeout=10)
    output += deviceObj.sendCmd('c\n')
    output += deviceObj.read_until_regexp('press any key to continue',timeout=60)
    output += deviceObj.sendCmd('q\n')
    for i in range(0,3):
        deviceObj.sendCmd('q')
        time.sleep(1)
    deviceObj.read_until_regexp('exit',timeout=10)
    deviceObj.executeCmd('q\r')
    log.info("Output is:{}".format(output))
    for pattern in i2c_system_scan_pattern:
        status = parserBsp.parse_i2cScanOutput(pattern,output)
        if status:
            log.success("Match in actual, expected {} I2C scan busses and their status".format(pattern))
        else:
            flag=False
            log.fail("Mismatch in actual, expected {} I2C scan busses and their status".format(pattern))
    if flag:
        log.success("Expected i2cscan patterns are present")
    else:
        raise RuntimeError("Expected i2cscan patterns are not present")

@logThis
def store_eeprom_content(device,eeprom_type,eeprom_path,eeprom_file):
    if fb_variant == 'minerva':
       cmd = "fb_eeprom -b /run/devmap/eeproms/{} {}/{}".\
            format(eeprom_type,eeprom_path,eeprom_file)
    elif fb_variant == 'minipack3':
       cmd = "fb_eeprom -b /run/devmap/eeprom/{} {}/{}".\
            format(eeprom_type,eeprom_path,eeprom_file)
    test_execute_command(device, cmd, CENTOS_MODE)

@logThis
def generate_eeprom_cfg(device,eeprom_path,eeprom_name,eeprom_cfg_file):
    eeprom_string = CommonLib.fb_generate_eeprom_cfg(eeprom_name)
    cmd = "echo -e \"%s\" > %s"%(eeprom_string, eeprom_cfg_file)
    test_execute_command(device, cmd, CENTOS_MODE)
    cmd = "mv {} {}".format(eeprom_cfg_file,eeprom_path)
    test_execute_command(device, cmd, CENTOS_MODE)


@logThis
def write_eeprom(device,eeprom_type,eeprom_path,eeprom_file):
    cmd = "fb_eeprom -p {}{} test_eeprom.bin".format(eeprom_path,eeprom_file)
    test_execute_command(device, cmd, CENTOS_MODE)
    if fb_variant == 'minerva':
       cmd = "dd if=test_eeprom.bin of=/run/devmap/eeproms/{}".format(eeprom_type)
    elif fb_variant == 'minipack3':
       cmd = "dd if=test_eeprom.bin of=/run/devmap/eeprom/{}".format(eeprom_type)
    test_execute_command(device, cmd, CENTOS_MODE, ['bytes copied'],30)
    test_execute_command(device, cmd, CENTOS_MODE, ['error writing'],30,0)

@logThis
def verify_eeprom(device,eeprom_type,eeprom_path,eeprom_name="",expected_content=""):
    deviceObj = Device.getDeviceObject(device)
    err_count = 0
    if not eeprom_name == "":
       expected_content = CommonLib.get_eeprom_cfg_dict(eeprom_name)
       del expected_content['crc16']
    if fb_variant == 'minerva':
       cmd = "time fb_eeprom -b /run/devmap/eeproms/{}".format(eeprom_type)
    elif fb_variant == 'minipack3':
       cmd = "time fb_eeprom -b /run/devmap/eeprom/{}".format(eeprom_type)
    output = deviceObj.sendCmd(cmd)
    output += deviceObj.read_until_regexp('crc16',timeout=30)
    log.info("Output is:{}".format(output))
    parsed_output = parserBsp.parse_eepromCfg_output(output)
    log.info("parsed output is:{}".format(parsed_output))
    if not expected_content == "":
       err_count += CommonLib.compare_input_dict_to_parsed(parsed_output, expected_content)
    else:
       #To verify read eeprom content
       err_count += CommonLib.compare_input_dict_to_parsed(parsed_output, parsed_output)
    if err_count:
        log.fail("Actual device output is {}".format(parsed_output))
        raise RuntimeError("Expected system version is not present")
    else:
        log.success("Expected system version is present")

@logThis
def copy_weutil_files(device):
    deviceObj = Device.getDeviceObject(device)
    cmd = "cp {}/libicuuc.so.67 /usr/lib64/".format(bsp_folder)
    test_execute_command(device, cmd, CENTOS_MODE)
    cmd = "cp {}/libicudata.so.67 /usr/lib64/".format(bsp_folder)
    test_execute_command(device, cmd, CENTOS_MODE)
    cmd = "cp {}/libicui18n.so.67 /usr/lib64/".format(bsp_folder)
    test_execute_command(device, cmd, CENTOS_MODE)
    cmd = "cp {}/weutil /root/".format(bsp_folder)
    test_execute_command(device, cmd, CENTOS_MODE)
    cmd = "cp {}/weutil.json /root/".format(bsp_folder)
    test_execute_command(device, cmd, CENTOS_MODE)

@logThis
def verify_weutil_eeprom_output(device,eeprom_type,eeprom_name="",expected_content=""):
    deviceObj = Device.getDeviceObject(device)
    err_count = 0
    if not expected_content == "":
       expected_content = get_eeprom_cfg_dict(eeprom_name)
    cmd = "time ./weutil --eeprom {} --config_file weutil.json".format(eeprom_type)
    output = deviceObj.sendCmd(cmd)
    output += deviceObj.read_until_regexp('CRC16',timeout=30)
    log.info("Output is:{}".format(output))
    parsed_output = parserBsp.parse_weutil_output(output)
    log.info("parsed output is:{}".format(parsed_output))
    if not expected_content == "":
       err_count += CommonLib.compare_input_dict_to_parsed(parsed_output, expected_content)
    else:
       #To verify read eeprom content
       err_count += CommonLib.compare_input_dict_to_parsed(parsed_output, parsed_output)
    if err_count:
        log.fail("Actual device output is {}".format(parsed_output))
        raise RuntimeError("Expected system version is not present")
    else:
        log.success("Expected system version is present")


def minerva_online_update(device, fw_type, isUpgrade = True):
    if 'dom' in fw_type:
        package_file_path = SwImage.getSwImage(SwImage.FPGA).localImageDir
        package_file = SwImage.getSwImage(SwImage.FPGA).newImage \
                if isUpgrade else SwImage.getSwImage(SwImage.FPGA).oldImage
    elif 'iob' in fw_type:
        package_file_path = SwImage.getSwImage(SwImage.IOB).localImageDir
        package_file = SwImage.getSwImage(SwImage.IOB).newImage \
                if isUpgrade else SwImage.getSwImage(SwImage.IOB).oldImage
    elif 'th5' in fw_type:
        package_file_path = SwImage.getSwImage(SwImage.TH5).localImageDir
        package_file = SwImage.getSwImage(SwImage.TH5).newImage \
                if isUpgrade else SwImage.getSwImage(SwImage.TH5).oldImage
    elif 'pwr' in fw_type:
        package_file_path = SwImage.getSwImage(SwImage.PWR).localImageDir
        package_file = SwImage.getSwImage(SwImage.PWR).newImage \
                if isUpgrade else SwImage.getSwImage(SwImage.PWR).oldImage
    elif 'smb1' in fw_type:
        package_file_path = SwImage.getSwImage(SwImage.SMB1).localImageDir
        package_file = SwImage.getSwImage(SwImage.SMB1).newImage \
                if isUpgrade else SwImage.getSwImage(SwImage.SMB1).oldImage
    elif 'smb2' in fw_type:
        package_file_path = SwImage.getSwImage(SwImage.SMB2).localImageDir
        package_file = SwImage.getSwImage(SwImage.SMB2).newImage \
                if isUpgrade else SwImage.getSwImage(SwImage.SMB2).oldImage
    else:
        log.info("Unsupported firmware type")
        return
    if fw_type.lower()=='iob':
        cmd = package_file_path + '/' + 'spi-utils.sh ' + 'iob ' +\
                'program '  + package_file_path + '/' + package_file
        #***Work around for R4063-35 ****
        test_execute_command(device, cmd, CENTOS_MODE)
    elif fw_type.lower()=='dom':
        cmd = package_file_path + '/' + 'spi-utils.sh ' + 'dom ' +\
                'program '  + package_file_path + '/' + package_file
    elif fw_type.lower()=='th5':
        cmd = package_file_path + '/' + 'spi-utils.sh ' + 'th5 ' +\
                'program '  + package_file_path + '/' + package_file
    elif fw_type.lower()=='pwr':
        cmd = package_file_path + '/' + 'spi-utils.sh ' + 'pwrcpld ' +\
                'program '  + package_file_path + '/' + package_file
    elif fw_type.lower()=='smb1':
        cmd = package_file_path + '/' + 'spi-utils.sh ' + 'smb1cpld ' +\
                'program '  + package_file_path + '/' + package_file
    elif fw_type.lower()=='smb2':
        cmd = package_file_path + '/' + 'spi-utils.sh ' + 'smb2cpld ' +\
                'program '  + package_file_path + '/' + package_file
    else:
        log.info("Unsupported firmware type")
    test_execute_command(device, cmd, CENTOS_MODE, ["Erase/write done"],120)
    time.sleep(30)
    return
