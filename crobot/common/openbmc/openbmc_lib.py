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
import bios_menu_lib
from Openbmc_variable import *
from Sdk_variable import SDK_PATH, SDK_SCRIPT
from datetime import datetime
from dataStructure import parser
from errorsModule import testFailed
from SensorCsv import SensorCsv
from pkg_resources import parse_version
from SwImage import SwImage

try:
    import parser_openbmc_lib as parserOpenbmc
    import DeviceMgr
    from Device import Device
except Exception as err:
    log.cprint(str(err))

deviceObj = DeviceMgr.getDevice()

def execute(deviceObj, cmd, timeout=60, mode=OPENBMC_MODE):
    log.debug('Entering procedure execute with args : %s\n' %(str(locals())))
    deviceObj.getPrompt(mode, timeout)
    cmd = 'time ' + cmd
    deviceObj.flush()
    return deviceObj.sendCmdRegexp(cmd, Const.TIME_REG_PROMPT, timeout)
    # return deviceObj.execute(cmd, exe_timeout=timeout, mode=mode)

def execute_cmd(deviceObj, cmd, timeout=60):
    log.debug('Entering procedure execute_cmd with args : %s\n' %(str(locals())))
    cmd = 'time ' + cmd
    deviceObj.flush()
    return deviceObj.sendCmdRegexp(cmd, Const.TIME_REG_PROMPT, timeout)

def reset_power_chassis(device, mode=OPENBMC_MODE, check_string_flag=False):
    log.debug('Entering procedure reset_power_chassis with args : %s\n' %(str(locals())))
    deviceObj = Device.getDeviceObject(device)
    output = deviceObj.powerCycleChassis(mode)
    #if 'minipack2' in deviceObj.name or 'cloudripper' in deviceObj.name:
        ### need to run this command to link the driver when BMC boot up
     #   deviceObj.execute('ln -s ld-2.29.so /lib/ld-linux.so.3')
    if check_string_flag:
        reset_msg = RESET_MESSAGE
        if parserOpenbmc.parse_simple_keyword(reset_msg, output) != "":
            log.success("Successfully reset power chassis")
        else:
            show_unit_info(device)
            raise testFailed("reset_power_chassis")

def reset_bmc_os(device):
    log.debug('Entering procedure reset_bmc_os with args : %s\n' %(str(locals())))
    deviceObj = Device.getDeviceObject(device)
    set_fan_auto_control(device, 'disable')
    #execute(deviceObj, "devmem 0x1e785014 w 0x77")
    #time.sleep(1)
    #execute(deviceObj, "devmem 0x1e785034 w 0x77")
    time.sleep(1)
    execute(deviceObj, "devmem 0x1e785004 32 0x00989680")
    time.sleep(1)
    execute(deviceObj, "devmem 0x1e785008 32 0x4755")
    time.sleep(1)
    deviceObj.sendline("devmem 0x1e78500c 32 0x00000033")
    reset_msg = 'DRAM'
    booting_msg = 'Starting kernel ...'
    deviceObj.receive(reset_msg, timeout=60)
    deviceObj.receive(booting_msg, timeout=90)
    deviceObj.getPrompt(OPENBMC_MODE, timeout=Const.BOOTING_TIME)
    time.sleep(10)

def need_update(device, device_type, device_version):
    log.debug('Entering procedure need_update with args : %s\n' % (str(locals())))
    deviceObj = Device.getDeviceObject(device)
    deviceObj.flush()
    err_count = 0
    if device_type.upper() == "BMC":
        cmd = 'cat /etc/issue'
        output = execute(deviceObj, cmd)
        parsed_output = parserOpenbmc.parse_openbmc_version(output)
    elif device_type.upper() == 'BIOS' or device_type.upper() == 'BIC' or device_type.upper() == 'SCM':
        cmd = 'fw-util scm --version'
        output = execute(deviceObj, cmd)
        parsed_output = parserOpenbmc.parse_fw_version(output)
        # key = 'BIOS Version'
    elif device_type.upper() == 'CPLD':
        cmd = 'cpld_ver.sh'
        output = execute(deviceObj, cmd)
        parsed_output = parserOpenbmc.parse_fw_version(output)
    elif device_type.upper() == 'FPGA':
        cmd = 'fpga_ver.sh'
        output = execute(deviceObj, cmd)
        parsed_output = parserOpenbmc.parse_fw_version(output)
    err_count += CommonLib.compare_input_dict_to_parsed(parsed_output, device_version, False)
    return True if err_count > 0 else False

def clean_diag_rpm_package(device):
    log.debug('Entering procedure clean_diag_rpm_package with args : %s\n' % (str(locals())))
    deviceObj = Device.getDeviceObject(device)
    cmd = 'rpm -qa| grep Diag|xargs -I {} rpm -e {} &> /dev/null'
    execute(deviceObj, cmd, timeout=180, mode=CENTOS_MODE)
    time.sleep(5)
    Diag_package = os.popen('rpm -qa | grep Diag').read()
    for package in Diag_package:
        os.system('rpm -e' + package)
    cmd1 = 'rm -rf /usr/local/cls_diag/'
    execute(deviceObj, cmd1, mode=CENTOS_MODE)
    #CommonLib.switch_to_openbmc()
    cmd2 = 'rm -rf /mnt/data1/BMC_DIAG'
    execute(deviceObj, cmd2)
    CommonLib.switch_to_centos()

def install_diag_image(device, diagImageFile):
    log.debug('Entering procedure install_diag_package with args : %s\n' % (str(locals())))
    deviceObj = Device.getDeviceObject(device)
    deviceObj.sendline('cd /home')
    cmd = 'rpm -ivh ' +  diagImageFile + ' --nodeps --force'
    execute(deviceObj, cmd, mode=CENTOS_MODE, timeout=300)
    deviceObj.sendline('cd /usr/local/cls_diag/bin/')
    cmd = './cel-version-test -S'
    execute(deviceObj, cmd, mode=CENTOS_MODE)

def create_tmp_dir(path, mode):
    log.debug('Entering procedure create_dir with args : %s\n' %(str(locals())))
    if check_file_exist(path, mode):
        log.info("%s exists"%(path))
        return 0
    else:
        mkdir_cmd = 'mkdir -p ' + path
        change_permission_cmd = 'chmod 777 ' + path
        execute_command(mkdir_cmd, mode=mode)
        execute_command(change_permission_cmd, mode=mode)
        return 1

def update_bmc(device, bmc_flash, isUpgrade = True):
    log.debug('Entering procedure update_bmc with args : %s\n' %(str(locals())))
    check_cpu_alive(device, need_cd=True)
    imageObj = SwImage.getSwImage(SwImage.BMC)
    version = {}
    version[OPENBMC_VER] = imageObj.newVersion if isUpgrade else imageObj.oldVersion
    if bmc_flash.lower() == 'master':
        if not need_update(device, SwImage.BMC, version):
            log.info("Already at version " +  version[OPENBMC_VER] + ", need not update.")
            return
        verify_mac_address(device, 'eth0')
        online_update_bmc(device, bmc_flash, isUpgrade)
        check_cpu_alive(device)
        CommonLib.reboot(OPENBMC_MODE)
        time.sleep(10)
        verify_fw_version(device, SwImage.BMC, version)
        verify_current_boot_flash(device, bmc_flash)
        check_eth_ports(device)
        verify_mac_address(device, 'eth0')
        check_cpu_alive(device)
        # reset_power_chassis(device)
        # verify_fw_version(device, SwImage.BMC, version)
        # verify_current_boot_flash(device, bmc_flash)
        # check_eth_ports(device)
        # verify_mac_address(device, 'eth0')
    else:
        online_update_bmc(device, bmc_flash, isUpgrade)
        check_cpu_alive(device)
        switch_bmc_flash(device, SLAVE)
        verify_fw_version(device, SwImage.BMC, version)
        check_eth_ports(device)
        verify_mac_address(device, 'eth0')
        check_cpu_alive(device)
        if not isUpgrade:
            switch_bmc_flash(device, MASTER)
            check_eth_ports(device)
            verify_mac_address(device, 'eth0')
            check_cpu_alive(device)
        # verify_fw_version(device, SwImage.BMC, version)
        if isUpgrade:
            reset_power_chassis(device)
            # verify_fw_version(device, SwImage.BMC, version)
            verify_current_boot_flash(device, MASTER)
            check_eth_ports(device)
            verify_mac_address(device, 'eth0')


def online_update_bmc(device, bmc_flash, isUpgrade = True):
    log.debug('Entering procedure online_update_bmc with args : %s\n' %(str(locals())))
    deviceObj = Device.getDeviceObject(device)
    imageObj = SwImage.getSwImage(SwImage.BMC)
    command = 'cat /proc/mtd'
    output = execute(deviceObj, command,timeout=1200)
    for line in output.splitlines():
        line = line.strip()
        if "flash0" in line:
            master_dev = line.split(":")[0]
            if len(master_dev)!= 4:
                master_dev = MASTER_DEV
        elif "flash1" in line:
            slave_dev = line.split(":")[0]
            if len(master_dev)!= 4:
                master_dev = SLAVE_DEV
    if isUpgrade:
        package_file = imageObj.newImage
    else:
        package_file = imageObj.oldImage
    if bmc_flash.lower() == 'master':
        cmd = 'flashcp -v ' + imageObj.localImageDir + '/' + package_file + ' /dev/' + master_dev
    elif bmc_flash.lower() == 'slave':
        cmd = 'flashcp -v ' + imageObj.localImageDir + '/' + package_file + ' /dev/' + slave_dev
    else:
        show_unit_info(device)
        log.fail("bmc flash support only Master or Slave")
        raise testFailed("online_update_bmc failed")
    deviceObj.flush()
    timeout = 1200
    output = execute(deviceObj, cmd, timeout=timeout)
    pass_message = r'Verifying kb:.*100%'
    p1 = r"No such file or directory"
    match = re.search(pass_message, output)
    match2 = re.search(p1, output)
    if match:
        log.success("Successfully online_update_bmc")
    elif match2:
        log.fail("%s" %(p1))
        show_unit_info(device)
        raise testFailed("online_update_bmc failed")
    else:
        show_unit_info(device)
        raise testFailed("online_update_bmc failed")

def update_bios(device, bios_flash, isUpgrade = True):
    log.debug('Entering procedure update_bios with args : %s\n' %(str(locals())))
    imageObj = SwImage.getSwImage(SwImage.BIOS)
    deviceObj = Device.getDeviceObject(device)
    bios_version = {}
    bios_version[SwImage.BIOS_VER] = imageObj.newVersion if isUpgrade else imageObj.oldVersion
    if bios_flash.lower() == 'master':
        if not need_update_bios(device, bios_version):
            log.info("Already at version " +  bios_version[SwImage.BIOS_VER] + ", need not update.")
            deviceObj.getPrompt(mode=OPENBMC_MODE)
            return
    online_update_bios(device, bios_flash, isUpgrade)
    if bios_flash.lower() == 'master':
        verify_bios_boot(device, switch_console_flag=True)
    else:
        verify_power_control(device, 'off')
        switch_bios_flash(device, bios_flash)
        verify_power_control(device, 'on')
    verify_dmidecode_bios_version(device, bios_version)
    verify_current_bios_flash(device, bios_flash)
    verify_fw_version(device, SwImage.BIOS, bios_version)

def need_update_bios(device, bios_version):
    ### dmidecode --s bios-version
    log.debug('Entering procedure need_update_bios with args : %s\n' %(str(locals())))
    deviceObj = Device.getDeviceObject(device)
    err_count = 0
    cmd = 'dmidecode --s bios-version'
    output = execute(deviceObj, cmd, mode=CENTOS_MODE)
    parsed_output = parserOpenbmc.parse_dmidecode_bios_version(output)
    err_count += CommonLib.compare_input_dict_to_parsed(parsed_output, bios_version, False)
    return True if err_count > 0 else False

def online_update_bios(device, bios_flash, isUpgrade = True):
    log.debug('Entering procedure online_update_bios with args : %s\n' %(str(locals())))
    imageObj = SwImage.getSwImage('BIOS')
    deviceObj = Device.getDeviceObject(device)
    deviceObj.getPrompt(mode=OPENBMC_MODE)
    if isUpgrade:
        package_file = imageObj.newImage
    else:
        package_file = imageObj.oldImage
    if bios_flash.lower() == 'master':
        ### fw-util scm --update bios bios.bin
        cmd = 'fw-util scm --update bios ' + imageObj.localImageDir + '/' + package_file
        pass_message = 'Upgrade of scm : bios succeeded'

    elif bios_flash.lower() == 'slave':
        cmd = 'spi_util.sh write spi1 BIOS ' + imageObj.localImageDir + '/' + package_file
        # pass_message = r'Verifying flash...(\s.*)*VERIFIED'
        pass_message = SPI_UPDATE_PASS_MSG

    if 'minerva' in deviceObj.name:
        cmd = 'bios_update.sh write ' + imageObj.localImageDir + '/' + package_file
        pass_message = BIOS_UPDATE_PASS_MSG

    if 'minipack3' in deviceObj.name:
        cmd = 'spi_util.sh write spi1 COME_BIOS' + imageObj.localImageDir + '/' + package_file
        pass_message = BIOS_UPDATE_PASS_MSG

    err_count = 0
    timeout = 2400

    p2 = "Cannot access"

    try:
        output = execute(deviceObj, cmd, timeout=timeout)
        log.cprint(str(output))
        match = re.search(pass_message, output)
        match2 = re.search(p2, output)
        if match:
            imageObj.currentUpdateVer[SwImage.BIOS_VER] = imageObj.newVersion if isUpgrade else imageObj.oldVersion
            log.info("Successfully online_update_bios")
        elif match2:
            log.fail("Cannot access image file")
            show_unit_info(device)
            raise RuntimeError("Cannot access image file")
    except Exception as err:
        log.cprint(str(err))
        raise RuntimeError("online_update_bios failed")

def online_update_bic(device, package_file, package_file_path):
    log.debug('Entering procedure online_update_bic with args : %s\n' %(str(locals())))
    deviceObj = Device.getDeviceObject(device)
    cmd = 'fw-util scm --update bic ' + package_file_path + '/' + package_file
    timeout = 120
    output = execute(deviceObj, cmd, timeout=timeout)
    time.sleep(5)
    pass_message = 'Upgrade of scm : bic succeeded'
    # fail_message = 'Upgrade of scm : bic failed'
    match = re.search(pass_message, output)
    if match:
        log.info("Successfully online_update_bic")
    else:
        log.error("online_update_bic failed")
        show_unit_info(device)
        raise RuntimeError("online_update_bic failed")

def update_bic(device, bmc_flash, isUpgrade=True):
    log.debug('Entering procedure update_bic with args : %s\n' % (str(locals())))
    imageObj = SwImage.getSwImage(SwImage.BIC)
    bic_version = {}
    bic_version[SwImage.BIC_VER] = imageObj.newVersion if isUpgrade else imageObj.oldVersion
    if not need_update(device, SwImage.BIC, bic_version):
        log.info("Already at version " +  bic_version[SwImage.BIC_VER] + ", need not update.")
        return
    verify_current_boot_flash(device, 'Master')
    check_cpu_alive(device, need_cd=True)
    if isUpgrade:
        online_update_bic(device, imageObj.newImage, imageObj.localImageDir)
    else:
        online_update_bic(device, imageObj.oldImage, imageObj.localImageDir)
    check_cpu_alive(device)
    reset_power_chassis(device)
    verify_fw_version(device, SwImage.BIC, bic_version)

def need_update_fpga(device, fpga_version):
    log.debug('Entering procedure need_update_fpga with args : %s\n' %(str(locals())))
    deviceObj = Device.getDeviceObject(device)
    # cmd = 'fpga_ver.sh'
    err_count  = 0
    output = execute(deviceObj, FPGA_VER_CMD)
    parsed_output = parserOpenbmc.parse_fw_version(output)
    err_count += CommonLib.compare_input_dict_to_parsed(parsed_output, fpga_version, False)
    return True if err_count > 0 else False

def update_fpga_minipack2(device, isUpgrade = True):
    log.debug('Entering procedure update_fpga_minipack2 with args : %s\n' %(str(locals())))
    fpga_version = get_version_from_config(SwImage.FPGA, isNewVersion=isUpgrade)
    if not need_update_fpga(device, fpga_version):
        log.info("Already at version " + str(fpga_version) + ", need not update.")
        return
    fpga_type = 'IOB_FPGA'
    online_update_fpga(device, fpga_type, isUpgrade)
    str1 = r'No good frequency'
    str2 = 'spi-aspeed-smc 1e630000.spi: No good frequency, using dumb slow'
    cmd1 = 'dmesg |grep spi-aspeed-smc'
    output1 = execute(deviceObj, cmd1, timeout=60)
    match1 = re.search(str1, output1)
    if match1:
        log.info("TC_009 IOB_FPGA found keyword: '%s'" % (str2))
    #reset_power_chassis(device)

    fpga_type = 'DOM_FPGA_PIM1'
    online_update_fpga(device, fpga_type, isUpgrade)

    execute(deviceObj, PIM_REINIT_CMD)
    set_time_delay(15)
    reset_power_chassis(device)
    verify_fw_version(device, SwImage.FPGA, fpga_version)

def update_fpga_cloudripper(device, isUpgrade = True):
    log.debug('Entering procedure update_fpga_cloudripper with args : %s\n' %(str(locals())))
    check_cpu_alive(device, need_cd=True)
    fpga_version = get_version_from_config(SwImage.FPGA, isNewVersion=isUpgrade)
    if not need_update_fpga(device, fpga_version):
        log.info("Already at version " + str(fpga_version) + ", need not update.")
        return
    fpga_type = 'DOM_FPGA_FLASH1'
    online_update_fpga(device, fpga_type, isUpgrade)
    fpga_type = 'DOM_FPGA_FLASH2'
    online_update_fpga(device, fpga_type, isUpgrade)
    check_cpu_alive(device)
    reset_power_chassis(device)
    verify_fw_version(device, SwImage.FPGA, fpga_version)

def update_fpga(device, isUpgrade = True):
    log.debug('Entering procedure update_fpga with args : %s\n' %(str(locals())))
    check_cpu_alive(device, need_cd=True)
    fpga_version = get_version_from_config(SwImage.FPGA, isNewVersion=isUpgrade)
    if not need_update_fpga(device, fpga_version):
        log.info("Already at version " + str(fpga_version) + ", need not update.")
        return
    fpga_type = 'DOM_FPGA_FLASH1'
    online_update_fpga(device, fpga_type, isUpgrade)
    check_cpu_alive(device)
    reset_power_chassis(device)
    verify_fw_version(device, SwImage.FPGA, fpga_version)

def online_update_fpga(device, fpga_type, isUpgrade = True):
    ### spi_util.sh write spi1 DOM_FPGA_FLASH1 image.bit
    log.debug('Entering procedure online_update_fpga with args : %s\n' %(str(locals())))
    deviceObj = Device.getDeviceObject(device)
    imageObj = SwImage.getSwImage(SwImage.FPGA)
    package_file = imageObj.newImage if isUpgrade else imageObj.oldImage
    package_file_path = imageObj.localImageDir
    if isinstance(package_file, dict) and ('IOB_FPGA' in fpga_type):
        ### for support Minipack2 iob fpga
        package_file_name = package_file['iob']
        cmd = 'spi_util.sh write spi1 ' + fpga_type + ' ' + package_file_path + '/' + package_file_name
        pass_message = SPI_ERASE_WRITE_MSG
        fail_message = FPGA_UPDATE_FAIL_MSG
    elif isinstance(package_file, dict) and ('PIM' in fpga_type):
            ### for support Minipack2 pim fpga
            package_file_name = package_file['pim']
            cmd = PIM_UPDATE_CMD + ' ' + package_file_path + '/' + package_file_name
            pass_message = PIM_UPDATE_PASS_MSG
            fail_message = FPGA_UPDATE_FAIL_MSG
    else:
        ### for support Other platform, default is dom fpga
        package_file_name = package_file
        cmd = 'spi_util.sh write spi1 ' + fpga_type + ' ' + package_file_path + '/' + package_file_name
        pass_message = SPI_UPDATE_PASS_MSG
        fail_message = FPGA_UPDATE_FAIL_MSG
    timeout = 1000
    output = execute(deviceObj, cmd, timeout=timeout)
    match1 = re.search(pass_message, output)
    match2 = re.search(fail_message, output, re.IGNORECASE)
    #if match1 and not match2:
    if match1:
        log.success("Successfully online_update_fpga")
        time.sleep(3)
    else:
        log.fail("Not found keyword: '%s'"%(pass_message))
        show_unit_info(device)
        raise testFailed("online_update_fpga failed")

def online_update_th3(device, package_file, package_file_path):
    ### spi_util.sh write spi1 TH3_PCIE_FLASH TH3_image
    log.debug('Entering procedure online_update_th3 with args : %s\n' %(str(locals())))
    deviceObj = Device.getDeviceObject(device)
    cmd = 'spi_util.sh write spi1 TH3_PCIE_FLASH ' + package_file_path + '/' + package_file
    timeout = 1200
    output = execute(deviceObj, cmd, timeout=timeout)
    time.sleep(5)
    pass_message = 'Verifying flash... VERIFIED.'
    pass_message2 = 'Erase/write done.'
    match = re.search(pass_message, output)
    match2 = re.search(pass_message2, output)
    if match or match2:
        log.success("Successfully online_update_th3")
    else:
        log.fail("online_update_th3 failed")
        show_unit_info(device)
        raise testFailed("online_update_th3 failed")

def verify_current_boot_flash(device, bmc_flash):
    log.debug('Entering procedure verify_current_boot_flash : %s\n '%(str(locals())))
    deviceObj = Device.getDeviceObject(device)
    cmd = 'boot_info.sh bmc'
    output = execute(deviceObj, cmd)
    parsed_output = parserOpenbmc.parse_current_boot_flash(output)
    if parsed_output['Current Boot'].lower() == bmc_flash.lower():
        log.success("verify_current_boot_flash match: %s, %s" %(bmc_flash, parsed_output['Current Boot']))
    else:
        log.fail("verify_current_boot_flash mismatch: %s, %s"%(bmc_flash, parsed_output['Current Boot']))
        show_unit_info(device)
        raise testFailed("verify_current_boot_flash")

def verify_current_bios_flash(device, bios_flash):
    log.debug('Entering procedure verify_current_bios_flash : %s\n '%(str(locals())))
    deviceObj.switchToBmc()
    cmd = 'boot_info.sh bios'
    output = execute(deviceObj, cmd)
    parsed_output = parserOpenbmc.parse_current_bios_flash(output)
    if parsed_output['Current Bios'].lower() == bios_flash.lower():
        log.info("verify_current_bios_flash match: %s, %s" %(bios_flash, parsed_output['Current Bios']))
    else:
        log.error("verify_current_bios_flash mismatch: %s, %s"%(bios_flash, parsed_output['Current Bios']))
        show_unit_info(device)
        raise RuntimeError("verify_current_bios_flash")

def verify_dmidecode_bios_version(device, bios_version=None):
    ### dmidecode --s bios-version
    log.debug('Entering procedure verify_dmidecode_bios_version with args : %s\n' %(str(locals())))
    deviceObj = Device.getDeviceObject(device)
    if bios_version is None:
        bios_version = get_version_from_config('BIOS')
    err_count = 0
    cmd = 'dmidecode --s bios-version'
    output = execute(deviceObj, cmd, mode=CENTOS_MODE)
    parsed_output = parserOpenbmc.parse_dmidecode_bios_version(output)
    #if 'wedge400c_d1-13' in deviceObj.name:
        #bios_version = {'BIOS Version': 'XG1_3A12.01'}
    err_count += CommonLib.compare_input_dict_to_parsed(parsed_output, bios_version)
    if err_count:
        log.fail("verify_dmidecode_bios_version failed")
        show_unit_info(device)
        raise testFailed("verify_dmidecode_bios_version")

def verify_bios_boot(device, switch_console_flag=False):
    log.debug('Entering procedure verify_bios_boot with args : %s\n' %(str(locals())))
    deviceObj = Device.getDeviceObject(device)
    err_count = 0
    bios_message = 'Press <DEL> or <F2> to enter setup.'
    p0 = r'(Copyright \(C\) (\d+) American Megatrends)'
    p1 = r'BIOS Date.*Ver: (\w+)'
    p2 = r'(>>Checking Media Presence)'
    p3 = r'Welcome to GRUB'
    if 'minipack3' in deviceObj.name or 'minerva' in deviceObj.name:
        bios_message = 'Press <DEL> or <ESC> to enter setup.'
        p0 = r'(Copyright \(C\) (\d+) AMI)'
        p3 = r'error: ../../grub-core'
    ### Switch to CPU console
    if switch_console_flag:
        # deviceObj.flush()
        deviceObj.sendline("sol.sh")
        deviceObj.receive('CTRL-l + b : Send Break', timeout=10)
        deviceObj.sendline("\r")
    output = deviceObj.receive(bios_message, timeout=Const.BOOTING_TIME)
    match = re.search(p1, output)
    if match:
        bios_boot_version = match.group(1)
        log.success("Booting BIOS version: %s"%(bios_boot_version))
    else:
        log.fail("Booting BIOS failed")
        show_unit_info(device)
        err_count += 1
    match2 = re.search(p0, output)
    if match2:
        log.success("Found '%s'"%(match2.group(1)))
    else:
        log.fail("Not found keyword '%s'"%(p0))
        err_count += 1

    output2 = deviceObj.receive(p3, timeout=Const.BOOTING_TIME)
    log.success("Found '%s'"%(p3))
    match3 = re.search(p2, output2)
    if match3:
        log.success("Found '%s'"%(match3.group(1)))
    else:
        log.fail("Not found keyword '%s'"%(p2))
        err_count += 1

    time.sleep(90)
    deviceObj.getPrompt(CENTOS_MODE, timeout=Const.BOOTING_TIME)
    time.sleep(5)
    if err_count:
        show_unit_info(device)
        raise testFailed("verify_bios_boot")

def verify_fw_version(device, device_type, device_version=None, get_flag=False):
    log.debug('Entering procedure verify_fw_version with args : %s\n' %(str(locals())))
    deviceObj = Device.getDeviceObject(device)
    # deviceObj.flush()
    err_count = 0
    time.sleep(60)
    if device_version is None:
        device_version = get_version_from_config(device_type)
    if device_type.upper() == "BMC":
        cmd = 'cat /etc/issue'
        output = execute(deviceObj, cmd)
        parsed_output = parserOpenbmc.parse_openbmc_version(output)
        # key = 'BMC Version'
    elif device_type.upper() == 'BIOS' or device_type.upper() == 'BIC' or device_type.upper() == 'SCM':
        # cmd = 'fw-util scm --version'
        output = execute(deviceObj, SCM_VER_CMD, timeout=120)
        parsed_output = parserOpenbmc.parse_fw_version(output)
        # key = 'BIOS Version'
    elif device_type.upper() == 'CPLD':
        # cmd = 'cpld_ver.sh'
        output = execute(deviceObj, CPLD_VER_CMD)
        parsed_output = parserOpenbmc.parse_fw_version(output)
    elif device_type.upper() == 'FPGA':
        # cmd = 'fpga_ver.sh'
        output = execute(deviceObj, FPGA_VER_CMD)
        parsed_output = parserOpenbmc.parse_fw_version(output)
    if get_flag:
        return parsed_output
    #if 'wedge400c_d1-13' in deviceObj.name and device_type.upper() == 'BIOS':
        #device_version = {'BIOS Version': 'XG1_3A12.01'}
    err_count += CommonLib.compare_input_dict_to_parsed(parsed_output, device_version)
    if err_count:
        show_unit_info(device)
        raise testFailed("Failure while verify_fw_version with result FAIL")

def verify_TH3_version(device, th3_version):
    log.debug('Entering procedure verify_TH3_version with args : %s\n' %(str(locals())))
    deviceObj = Device.getDeviceObject(device)
    err_count = 0
    deviceObj.getPrompt(CENTOS_MODE, timeout=Const.BOOTING_TIME)
    CommonLib.change_dir('/root/SDK', CENTOS_MODE)
    deviceObj.flush()
    cmd = './auto_load_user.sh'
    pcie_cmd = 'pciephy fw version'
    deviceObj.sendline(cmd)
    deviceObj.receive(deviceObj.get('bcmPrompt'), timeout=10)
    deviceObj.flush()
    deviceObj.sendline(pcie_cmd)
    output = deviceObj.receive(deviceObj.get('bcmPrompt'))
    deviceObj.sendline('exit')
    deviceObj.sendline('cd')
    deviceObj.getPrompt(OPENBMC_MODE)
    parsed_output = parserOpenbmc.parse_th3_version(output)
    err_count += CommonLib.compare_input_dict_to_parsed(parsed_output, th3_version)
    if err_count:
        show_unit_info(device)
        raise testFailed("Failure while verify_TH3_version with result FAIL")

def verify_TH3_link_test(device):
    log.debug('Entering procedure verify_TH3_link_test with args : %s\n' %(str(locals())))
    deviceObj = Device.getDeviceObject(device)
    deviceObj.getPrompt(CENTOS_MODE, timeout=Const.BOOTING_TIME)
    CommonLib.change_dir('/root/SDK', CENTOS_MODE)
    deviceObj.flush()
    cmd = './auto_load_user.sh -d'
    test_cmd = './xeloopback.sh'
    kill_cmd = 'pkill bcm.user'
    enter_message = 'Enter daemon mode.'
    pass_message = r'Passed'
    output = execute(deviceObj, cmd, timeout=60, mode=CENTOS_MODE)
    match = re.search(enter_message, output)
    if match:
        log.info("%s"%(enter_message))
    else:
        log.fail("cannot %s"%(enter_message))
        show_unit_info(device)
        execute(deviceObj, kill_cmd, mode=CENTOS_MODE)
        raise testFailed("verify_TH3_link_test")
    output2 = execute(deviceObj, test_cmd, timeout=60, mode=CENTOS_MODE)
    execute(deviceObj, kill_cmd, mode=CENTOS_MODE)
    match2 = re.search(pass_message, output2)
    if match2:
        log.success("Sucessfully verify_TH3_link_test")
    else:
        log.fail("verify_TH3_link_test failed")
        show_unit_info(device)
        raise testFailed("verify_TH3_link_test")

def verify_power_control(device, power_mode, power_status='None', option='None'):
    ### wedge_power.sh [status|off|on|reset]
    log.debug('Entering procedure verify_power_control with args : %s\n' %(str(locals())))
    deviceObj = Device.getDeviceObject(device)
    time.sleep(2)
    cmd = 'wedge_power.sh ' + power_mode
    err_count = 0
    # deviceObj.flush()
    if power_mode == 'status':
        output = execute(deviceObj, cmd, timeout=10)
        parsed_output = parserOpenbmc.parse_power_status2(output)
        if parsed_output['power status'] == power_status:
            log.success("Power Status is correct")
        else:
            log.fail("Power Status is incorrect")
            show_unit_info(device)
            raise testFailed("Power Status mismatch")
    elif power_mode == 'off':
        output = execute(deviceObj, cmd, timeout=10)
        parsed_output = parserOpenbmc.parse_power_control2(output)
        time.sleep(5)
        if parsed_output['power control'] == 'Done':
            log.success("Successfully power switched off")
        else:
            log.fail("Chassis not switched off")
            show_unit_info(device)
            raise testFailed("Chassis switch off failed")
    elif option and power_mode == 'reset':
        deviceObj.powerCycleChassis(OPENBMC_MODE)
        return
    elif power_mode == 'on' or power_mode == 'reset':
        output = execute(deviceObj, cmd, timeout=10)
        parsed_output = parserOpenbmc.parse_power_control2(output)
        time.sleep(5)
        if parsed_output['power control'] == 'Done':
            log.success("Successfully power switched %s"%(power_mode))
        elif 'Already on' in parsed_output['power control']:
            deviceObj.sendline("")
            log.info("Chassis is already on")
            return
        elif 'Skipped' in parsed_output['power control']:
            deviceObj.sendline("")
            log.info("Chassis is already on")
            return
        else:
            log.fail("Chassis not switched %s"%(power_mode))
            show_unit_info(device)
            raise testFailed("Chassis switch %s failed"%(power_mode))
        deviceObj.getPrompt(OPENBMC_MODE)
        verify_bios_boot(device, switch_console_flag=True)

def verify_watchdog_info(device, WDT):
    log.debug('Entering procedure verify_watchdog_info : %s\n '%(str(locals())))
    deviceObj = Device.getDeviceObject(device)
    err_count = 0
    cmd = 'boot_info.sh bmc'
    output = execute(deviceObj, cmd)
    parsed_output = parserOpenbmc.parse_watchdog_timer(output)
    err_count += CommonLib.compare_input_dict_to_parsed(parsed_output, WDT)
    if err_count:
        log.fail("verify_watchdog_info failed")
        show_unit_info(device)
        raise testFailed("verify_watchdog_info")

def get_fan_speed(device, fan_speed='None', fan_speed_max='None'):
    log.debug('Entering procedure get_fan_speed with args : %s\n' %(str(locals())))
    deviceObj = Device.getDeviceObject(device)
    cmd = "get_fan_speed.sh"
    err_count = 0
    output = execute(deviceObj, cmd)
    parsed_output = parserOpenbmc.parse_get_fan_speed(output)
    if fan_speed != 'None':
        for i in range(1, FAN_NUM + 1):
            key = 'Fan '+ str(i) + ' percentage'
            if key in parsed_output:
                parsed_speed = int(parsed_output[key])
                expected_speed = int(fan_speed)
                variance = 2
                if fan_speed_max == 'None':
                    if (expected_speed - variance) <= parsed_speed <= (expected_speed + variance):
                        log.success("get fan " + str(i) + " speed: " + str(parsed_speed) + '% (' + fan_speed + '%)')
                    else:
                        log.fail("fan " + str(i) + " speed: " + str(parsed_speed) + "% is over the range of expected speed: " + fan_speed + '%')
                        err_count += 1
                else:
                    max_speed = int(fan_speed_max)
                    if (expected_speed - variance) <= parsed_speed <= (max_speed + variance):
                        log.success("get fan " + str(i) + " speed: " + str(parsed_speed) + '% (' \
                                    + fan_speed + '% ~ ' + fan_speed_max + '%)')
                    else:
                        log.fail("fan " + str(i) + " speed: " + str(parsed_speed) + "% is over the range of expected speed: " \
                                    + fan_speed + '% ~ ' + fan_speed_max + '%')
                        err_count += 1
            else:
                log.fail("Not found: %s"%(key))
                err_count += 1

            key = 'Fan '+ str(i) + ' front'
            if key in parsed_output:
                parsed_rpm_front = int(parsed_output[key])
                err_count += verify_fan_rpm_in_range(i, parsed_rpm_front, MIN_RPM, MAX_RPM)
            else:
                log.fail("Not found: %s"%(key))
                err_count += 1

            key = 'Fan ' + str(i) + ' rear'
            if key in parsed_output:
                parsed_rpm_rear = int(parsed_output[key])
                err_count += verify_fan_rpm_in_range(i, parsed_rpm_rear, MIN_RPM, MAX_RPM)
            else:
                log.fail("Not found: %s"%(key))
                err_count += 1
    if err_count:
        show_unit_info(device)
        raise testFailed("get_fan_speed")

def verify_fan_rpm_in_range(fan_num, rpm, min_rpm, max_rpm):
    log.debug('Entering procedure verify_fan_rpm_in_range with args : %s\n' %(str(locals())))
    err_count = 0
    if min_rpm <= rpm <= max_rpm:
        log.success("Fan %d RPM: %d is in range %d-%d"%(fan_num, rpm, min_rpm, max_rpm))
    else:
        log.fail("Fan %d RPM: %d is out of range %d-%d"%(fan_num, rpm, min_rpm, max_rpm))
        show_unit_info(device)
        err_count += 1
    return err_count

def set_fan_speed(device, fan_speed):
    log.debug('Entering procedure set_fan_speed with args : %s\n' %(str(locals())))
    deviceObj = Device.getDeviceObject(device)
    cmd = 'set_fan_speed.sh ' + str(fan_speed)
    err_count = 0
    output = execute(deviceObj, cmd)
    parsed_output = parserOpenbmc.parse_set_fan_speed(output)
    time.sleep(3)
    for i in range(1, FAN_NUM + 1):
        if parsed_output['Fan '+ str(i) + ' percentage'] == fan_speed:
            log.success("set fan %s speed: %s"%(str(i), fan_speed) + '%')
        else:
            log.fail("set fan %s speed: %s"%(str(i), fan_speed))
            err_count += 1
    if err_count:
        show_unit_info(device)
        raise testFailed("set_fan_speed")

def set_fan_auto_control(device, control_mode):
    log.debug('Entering procedure set_fan_auto_control with args : %s\n' %(str(locals())))
    deviceObj = Device.getDeviceObject(device)
    # time_delay = 90
    err_count = 0
    ##### sv stop fscd;wdtcli stop
    ##### sv start fscd
    ##### ps|grep fscd
    if control_mode.lower() == 'disable':
        if 'cloudripper' in deviceObj.name or 'minipack2' in deviceObj.name:
            #cmd = "systemctl stop fscd;wdtcli stop"
            cmd = "systemctl stop restapi fscd;wdtcli stop"
            p1 = r'fail|error'
            output = execute(deviceObj, cmd)
            time.sleep(1)
            if parserOpenbmc.parse_simple_keyword_cr(p1, output) == "":
                log.success("Successfully disable fan auto control")
            else:
                log.fail("disable fan auto control")
                err_count += 1
        else:
            cmd = "sv stop fscd;wdtcli stop"
            p1 = r'ok: down: fscd: (\d+)s, normally up'
            output = execute(deviceObj, cmd)
            time.sleep(2)
            output = execute(deviceObj, cmd)
            time.sleep(1)
            if parserOpenbmc.parse_simple_keyword(p1, output) != "":
                log.success("Successfully disable fan auto control")
            else:
                log.fail("disable fan auto control")
                err_count += 1
    elif control_mode.lower() == 'enable':
        cmd1 = "sv start fscd"
        cmd2 = "ps | grep fscd"
        cmd3 = "systemctl start fscd"
        p1 = r'ok: run: fscd: \(pid (\d+)\) \d+s'
        p2 = 'runsv /etc/sv/fscd'
        p3 = r'error|fail'
        if 'cloudripper' in deviceObj.name or 'minipack2' in deviceObj.name:
            output = execute(deviceObj, cmd3, timeout=30)
            time.sleep(1)
            if parserOpenbmc.parse_simple_keyword_cr(p3, output) == "":
                log.success("Successfully run systemctl")
            else:
                log.fail("run systemctl fail!")
                err_count += 1
        else:
            output = execute(deviceObj, cmd1, timeout=30)
            time.sleep(1)
            if parserOpenbmc.parse_simple_keyword(p1, output) != "":
                log.success("Successfully run '%s'"%(cmd1))
            else:
                log.fail("run '%s'"%(cmd1))
                err_count += 1

        output = execute(deviceObj, cmd2, timeout=30)
        time.sleep(1)
        if 'cloudripper' in deviceObj.name or 'minipack2' in deviceObj.name:
            pass
        elif parserOpenbmc.parse_simple_keyword(p2, output) != "":
            log.success("Successfully run '%s'"%(cmd2))
        else:
            log.fail("run '%s'"%(cmd2))
            err_count += 1
        # log.info('wait %s sec for setting fan speed...'%(time_delay))
        # time.sleep(time_delay)
    if err_count:
        show_unit_info(device)
        raise testFailed("set_fan_auto_control")

def kill_process(device, keyword):
    log.debug('Entering procedure kill_process with args : %s\n' %(str(locals())))
    deviceObj = Device.getDeviceObject(device)
    show_cmd = 'ps | grep \'%s\''%(keyword)
    p1 = r'(\d+).+(\w)\s{2,}(%s)'%(keyword)
    output = execute(deviceObj, show_cmd)
    pid = parserOpenbmc.parse_pid(output, keyword)
    if pid:
        kill_cmd = 'kill -9 %s'%(pid)
        execute(deviceObj, kill_cmd)
        time.sleep(1)
    else:
        log.info('No such process, no need to kill')

def check_sel_event(device, event_keyword='None'):
    log.debug('Entering procedure check_sel_event : %s\n'%(str(locals())))
    deviceObj = Device.getDeviceObject(device)
    cmd = "ipmitool sel elist"
    output = execute(deviceObj, cmd, mode=CENTOS_MODE)
    if event_keyword != 'None':
        match = re.search(event_keyword, output)
        if match:
            log.success("%s is recorded"%(event_keyword))
        else:
            log.fail("%s is not recorded"%(event_keyword))
            show_unit_info(device)
            raise testFailed("check_sel_event")

def check_reboot_error_message(device, prompt, error_messages):
    log.debug('Entering procedure check_reboot_error_message : %s\n '%(str(locals())))
    deviceObj = Device.getDeviceObject(device)
    deviceObj.getPrompt(prompt)
    if prompt == 'openbmc':
        #booting_msg = 'OpenBMC Release.*'
        booting_msg = 'Starting kernel'
    else:
        booting_msg = 'CentOS Linux*'
    deviceObj.sendline("reboot")
    output = deviceObj.read_until_regexp(booting_msg, timeout=500)
    time.sleep(120)
    deviceObj.getPrompt(prompt, timeout=Const.BOOTING_TIME)
    time.sleep(35)
    deviceObj.sendline('\n')
    err_count = 0
    error_messages_list = error_messages.split(",")
    for error_message in error_messages_list:
        match = re.search(error_message, output)
        if match:
            print("Found error_message: *" + error_message + "* in the reboot log!" )
            err_count += 1
    if err_count == 0:
        log.success("Successfully check the reboot log, found no error!")
    else:
        log.info("check_reboot_error_messages_fail")
        show_unit_info(device)
        #raise testFailed("check_reboot_error_messages_fail")

def check_reboot_message(device, prompt, messages_list):
    log.debug('Entering procedure check_reboot_message : %s\n '%(str(locals())))
    deviceObj = Device.getDeviceObject(device)
    deviceObj.getPrompt(prompt)
    if prompt == 'openbmc':
        booting_msg = 'OpenBMC Release.*'
    else:
        booting_msg = 'CentOS Linux*'
    deviceObj.sendline("reboot")
    output = deviceObj.read_until_regexp(booting_msg, timeout=Const.BOOTING_TIME)
    deviceObj.getPrompt(prompt, timeout=Const.BOOTING_TIME)
    time.sleep(35)
    deviceObj.sendline('\n')
    err_count = 0
    for msg in messages_list:
        if parserOpenbmc.parse_simple_keyword(msg, output) == "":
            err_count += 1
    if err_count == 0:
        log.success("Successfully check the reboot log, found all messages!")
    else:
        log.fail("check_reboot_message fail")
        show_unit_info(device)
        raise testFailed("check_reboot_message fail")

def check_power_cycle_message(device, messages_list):
    log.debug('Entering procedure check_power_cycle_message with args : %s\n' %(str(locals())))
    deviceObj = Device.getDeviceObject(device)
    deviceObj.getPrompt(OPENBMC_MODE)
    cmd = 'wedge_power.sh reset -s'
    booting_msg = 'OpenBMC Release.*'
    deviceObj.sendline(cmd)
    output = deviceObj.read_until_regexp(booting_msg, timeout=Const.BOOTING_TIME)
    time.sleep(3)
    output += deviceObj.readMsg()
    output += deviceObj.getPrompt(OPENBMC_MODE, timeout=Const.BOOTING_TIME)
    deviceObj.getPrompt(CENTOS_MODE, timeout=Const.BOOTING_TIME)
    deviceObj.getPrompt(OPENBMC_MODE)
    err_count = 0
    for msg in messages_list:
        if parserOpenbmc.parse_simple_keyword(msg, output) == "":
            err_count += 1
    if err_count == 0:
        log.success("Successfully check the power cycle log, found all messages!")
    else:
        log.fail("check_power_cycle_message fail")
        show_unit_info(device)
        raise testFailed("check_power_cycle_message fail")

def clear_sel_event(device):
    log.debug('Entering procedure check_sel_event : %s\n'%(str(locals())))
    deviceObj = Device.getDeviceObject(device)
    cmd = "ipmitool sel clear"
    output = execute(deviceObj, cmd, mode=CENTOS_MODE)
    time.sleep(3)

def get_gpio_data(device, data_mode, expected_result):
    log.debug('Entering procedure get_gpio_data : %s\n'%(str(locals())))
    deviceObj = Device.getDeviceObject(device)
    cmd = "cat " + data_mode
    output = execute(deviceObj, cmd)
    parsed_output = parserOpenbmc.parse_gpio_data(output)
    log.debug("+++++++++++++++++++++++++++++++++++++++++++++++++++++++")
    log.debug("|                               | EXPECTED | RECEIVED |")
    log.debug("|-------------------------------|----------|----------|")
    log.debug("|GPIO %-9s                 |    %-3s   |    %-3s   |" %(data_mode, expected_result, parsed_output))
    log.debug("|-------------------------------|----------|----------|")
    if parsed_output == expected_result:
        log.success("get_gpio_data, result: \'%s\'"%(parsed_output))
    else:
        log.fail("gpio data mismatch: Found \'%s\' Expected \'%s\'\n"%(parsed_output, expected_result))
        show_unit_info(device)
        raise testFailed("Failed get_gpio_data")

def set_gpio_data(device, data_mode, value):
    log.debug('Entering procedure set_gpio_data : %s\n'%(str(locals())))
    deviceObj = Device.getDeviceObject(device)
    cmd = 'echo ' + value + ' > ' + data_mode
    execute(deviceObj, cmd)
    time.sleep(1)

def run_curl(device, option, restful_url, ip, interface='None', ipv6=False, mode=CENTOS_MODE, data='None'):
    log.debug('Entering procedure run_curl : %s\n'%(str(locals())))
    deviceObj = Device.getDeviceObject(device)
    pc_timeout = 20
    if option == GET:
        cmd = 'curl -g'
    elif option == POST:
        cmd = 'curl -d ' + data
        pc_timeout = 60
    elif option == Other:
        cmd = 'curl'
    else:
        log.fail('run_curl support only "get" or "post" option')
        raise testFailed("run_curl")
    cmd += ' http://'
    if ipv6:
        if ip.startswith('2001'):
            cmd += '[' + ip + ']'
        else:
            cmd += '[' + ip + '%' + interface + ']'
    else:
        cmd += ip
    # cmd += ':8080/api/sys/' + restful_url + ' |python -m json.tool'
    if option == Other:
        cmd += ':8080/redfish/v1/Chassis/1/' + restful_url
    else:
        cmd += ':8080/api/sys/' + restful_url
    log.debug('cmd: %s'%(cmd))
    time.sleep(1)
    if mode == 'None':
        done_msg = r'(.*Forbidden|]?}).*%s'%(deviceObj.prompt)
        try:
            deviceObj.transmit(cmd)
            deviceObj.transmit("")
            output = deviceObj.read_until_regexp(done_msg, timeout=pc_timeout)
            log.info('output: %s'%(output))
        except:
            log.fail("Cannot get curl output within %d s"%(pc_timeout))
            show_unit_info(device)
            raise RuntimeError('run_curl')
    else:
        output = execute(deviceObj, cmd, timeout=300, mode=mode)
    if option == Other:
        p1 = r'^real\s+0m(\d+)\.\d{3}s'
        p2 = r'fail|error|Error'
        for line in output.splitlines():
            line = line.strip()
            match = re.search(p1, line)
            match1 = re.search(p2, line)
            if match or match1:
                if match1:
                    log.fail('run cmd: [ %s ], finding some fail or error info.' % (cmd))
                    raise testFailed("Finding error or fail info.")
                else:
                    real_time = match.group(1).strip()
                    if int(real_time) > 45:
                        log.fail('run cmd: [ %s ], overrun 45s'%(cmd))
                        show_unit_info(device)
                        raise testFailed("run cmd timeout.")
    ### remove curl cmd from output for parsing only json string easily
    output = output.replace(cmd, '')
    if option == POST:
        output = output.replace(data, '')
    parsed_output = parserOpenbmc.parse_json_string2(output)
    if parsed_output == '':
        return
    parsed_json = parserOpenbmc.parse_json_object(parsed_output)
    return parsed_json

def compare_json_object(json1, json2, restful_url):
    log.debug('Entering procedure compare_json_object : %s\n'%(str(locals())))
    fail_count = 0
    if json1 == json2:
        log.success("restful response of '%s' match"%(restful_url))
    else:
        log.fail("restful response of '%s' mismatch"%(restful_url))
        show_unit_info(device)
        fail_count += 1
    return fail_count

def verify_restful(device, restful_url, ip, interface='None', ipv6=False, compare=False, mode=CENTOS_MODE):
    log.debug('Entering procedure verify_restful : %s\n'%(str(locals())))
    deviceObj = Device.getDeviceObject(device)
    err_count = 0

    if compare:
        json2 = run_curl(device, GET, restful_url, ip, interface, ipv6, mode=OPENBMC_MODE)
        ### compare 2 json objects
        # err_count += compare_json_object(json1, json2, restful_url)

        if restful_url == 'mb/fruid':
            cmd = 'weutil'
        elif restful_url == 'feutil/all':
            cmd = 'feutil all'
        else:
            cmd = restful_url
        output = execute(deviceObj, cmd)
        response_dict = json2['Information']
        ### compare json object and util output
        if restful_url == 'feutil/all':
            parsed_output = parserOpenbmc.parse_fan_util(output)
            for key in parsed_output.keys():
                log.info("comparing '%s' result"%(key))
                err_count += CommonLib.compare_input_dict_to_parsed(parsed_output[key], response_dict[key])
        else:
            parsed_output = parserOpenbmc.parse_util(output)
            err_count += CommonLib.compare_input_dict_to_parsed(parsed_output, response_dict)
    else:
        json2 = run_curl(device, GET, restful_url, ip, interface, ipv6, mode)
        if json2 is None:
            log.fail("No json object returned")
            err_count += 1
        else:
            log.success("Sucessfully get restful fru data")

    if err_count:
        show_unit_info(device)
        raise testFailed("verify_restful")

def verify_restful_fw(device, restful_url, ip, interface='None', ipv6=False, compare=False):
    log.debug('Entering procedure verify_restful_fw : %s\n'%(str(locals())))
    deviceObj = Device.getDeviceObject(device)
    err_count = 0

    if compare:
        json1 = run_curl(device, GET, restful_url, ip, interface, ipv6, mode=OPENBMC_MODE)
        # json2 = run_curl(device, GET, restful_url, LOCALHOST, mode=OPENBMC_MODE)
        ### compare 2 json objects
        # err_count += compare_json_object(json1, json2, restful_url)

        ### compare json object and util output
        response_dict = json1['Information']
        device_type = restful_url.split('/')[-1]
        if (device_type.lower() == 'cpld') and ('minipack2' not in deviceObj.name):
            if 'SMBCPLD' in response_dict:
                response_dict[SMB_CPLD_KEY] = response_dict.pop('SMBCPLD')
            if 'PWRCPLD' in response_dict:
                response_dict[PWR_CPLD_KEY] = response_dict.pop('PWRCPLD')
        verify_fw_version(device, device_type, response_dict)
    else:
        json1 = run_curl(device, GET, restful_url, ip, interface, ipv6)
        if json1 is None:
            log.fail("No json object returned")
            err_count += 1
        else:
            log.success("Sucessfully get restful status data")
    if err_count:
        show_unit_info(device)
        raise testFailed("verify_restful_fw")

def verify_restful_presence(device, ip, interface='None', ipv6=False, compare=False):
    log.debug('Entering procedure verify_restful_presence : %s\n'%(str(locals())))
    deviceObj = Device.getDeviceObject(device)
    err_count = 0
    restful_url = 'presence'

    if compare:
        json1 = run_curl(device, GET, restful_url, ip, interface, ipv6, mode=OPENBMC_MODE)
        # json2 = run_curl(device, GET, restful_url, LOCALHOST, mode=OPENBMC_MODE)
        ### compare 2 json objects
        # err_count += compare_json_object(json1, json2, restful_url)

        ### compare json object and util output
        response_dict = json1['Information']
        p1 = 'pem11|pem12'
        res = re.search(p1, str(response_dict))
        if res:
            err_count += 1
            log.fail("pem11 or pem12 is failed.")
        new_dict = {}
        for i in range(len(response_dict)):
            res_dict = {}
            for key in response_dict[i]:
                key1 = key.strip()
                res_dict[key1] = response_dict[i][key]
            new_dict.update(res_dict)
        #if 'wedge400c' in deviceObj.name or 'wedge400_' in deviceObj.name:
            #power_type = dc_power(device)
            #if power_type == 'AC':
                #new_dict.pop('pem1')
                #new_dict.pop('pem2')
        verify_presence_util(device, new_dict)
    else:
        json1 = run_curl(device, GET, restful_url, ip, interface, ipv6)
        if json1 is None:
            log.fail("No json object returned")
            err_count += 1
        else:
            log.success("Sucessfully get restful presence status data")
    if err_count:
        show_unit_info(device)
        raise testFailed("verify_restful_presence")

def verify_restful_mTerm(device, ip, interface='None', ipv6=False, mode=CENTOS_MODE):
    log.debug('Entering procedure verify_restful_mTerm : %s\n'%(str(locals())))
    deviceObj = Device.getDeviceObject(device)
    err_count = 0
    restful_url = 'mTerm_status'

    json1 = run_curl(device, GET, restful_url, ip, interface, ipv6, mode)
    # json2 = run_curl(device, GET, restful_url, LOCALHOST, mode=OPENBMC_MODE)
    ### compare 2 json objects
    # err_count += compare_json_object(json1, json2, restful_url)
    if json1 is None:
        log.fail("No json object returned")
        err_count += 1
    else:
        log.success("Sucessfully get restful mTerm status data")
    if err_count:
        show_unit_info(device)
        raise testFailed("verify_restful_mTerm")

def verify_restful_bmc(device, ip, cmd_get_device_id='None', interface='None', ipv6=False, compare=False):
    log.debug('Entering procedure verify_restful_bmc : %s\n'%(str(locals())))
    deviceObj = Device.getDeviceObject(device)
    err_count = 0
    restful_url = 'bmc'

    if compare:
        json2 = run_curl(device, GET, restful_url, ip, interface, ipv6, mode=OPENBMC_MODE)
        ### compare only 'OpenBMC Version' key
        # key = 'OpenBMC Version'

        parsed_device_id = run_ipmi_get_test("get_device_id", device, cmd_get_device_id)
        ### compare only 'OpenBMC Version' key with ipmitool get device id command
        # firmware_ver = parsed_device_id['Firmware Revision']
        # if firmware_ver == json2['Information'][key]:
        #     log.success("BMC version matched with ipmitool get device id response: '%s'"%(firmware_ver))
        # else:
        #     log.fail("BMC version mismatch: %s, %s"%(firmware_ver, json2['Information'][key]))
        #     err_count += 1

        parsed_output = run_ipmi_cmd_mc_info(device)
        firmware_ver = parse_version(parsed_output['Firmware Revision'])
        parsed_output.update({"Firmware Revision" : firmware_ver})
        ### compare only 'OpenBMC Version' key with ipmitool 'Firmware Revision'
        ### standard of version number in ipmitool is 'x.0x'
        # firmware_ver = parsed_output['Firmware Revision'].replace('.0', '.')
        # if firmware_ver == json2['Information'][key]:
        #     log.success("BMC version matched with dumped in BMC OS: '%s'"%(firmware_ver))
        # else:
        #     log.fail("BMC version mismatch: %s, %s"%(firmware_ver, json2['Information'][key]))
        #     err_count += 1
        err_count += CommonLib.compare_input_dict_to_parsed(parsed_output, parsed_device_id)
    else:
        json2 = run_curl(device, GET, restful_url, ip, interface, ipv6)
        if json2 is None:
            log.fail("No json object returned")
            err_count += 1
        else:
            log.success("Sucessfully get restful BMC info data")
    if err_count:
        show_unit_info(device)
        raise testFailed("verify_restful_bmc")

def run_ipmi_cmd_mc_info(device):
    log.debug('Entering procedure run_ipmi_cmd_mc_info : %s\n'%(str(locals())))
    cmd = 'ipmitool mc info'
    deviceObj = Device.getDeviceObject(device)
    output = execute(deviceObj, cmd, mode=CENTOS_MODE)
    parsed_output = parserOpenbmc.parse_ipmitool_mc_info(output)
    if parsed_output:
        log.success("Successfully execute '%s'"%(cmd))
        return parsed_output
    else:
        log.fail("execute '%s'"%(cmd))
        show_unit_info(device)
        raise testFailed("run_ipmi_cmd_mc_info")

def sensor_read_performance_test(device, ip, interface='None', ipv6=False, compare=False):
    log.debug('Entering procedure verify_restful_sensors : %s\n' % (str(locals())))
    deviceObj = Device.getDeviceObject(device)
    if 'wedge400c' in deviceObj.name or 'wedge400' in deviceObj.name or 'minipack2' in deviceObj.name:
        err_count = 0
        restful_url = 'Sensors'
        if compare:
            json1 = run_curl(device, Other, restful_url, ip, interface, ipv6, mode=OPENBMC_MODE)
            #json_sensors_list = json1['Information']

def verify_restful_sensors(device, ip, interface='None', ipv6=False, compare=False):
    log.debug('Entering procedure verify_restful_sensors : %s\n'%(str(locals())))
    deviceObj = Device.getDeviceObject(device)
    err_count = 0
    restful_url = 'sensors'

    if compare:
        json1 = run_curl(device, GET, restful_url, ip, interface, ipv6, mode=OPENBMC_MODE)
        # json2 = run_curl(device, GET, restful_url, LOCALHOST, mode=OPENBMC_MODE)
        # ### compare only keys of 2 json objects for each sensors type
        json_sensors_list = json1['Information']
        # for i in range(len(json_sensors_list)):
        #     diff = set(json_sensors_list[i]) - set(json2['Information'][i])
        #     if not diff:
        #         log.success("restful sensors '%s' response keys match"%(json_sensors_list[i]['name']))
        #     else:
        #         log.fail("missing sensors: %s"%str(diff))
        #         log.fail("restful sensors '%s' response keys mismatch"%(json_sensors_list[i]['name']))
        #         err_count += 1

        for i in range(len(json_sensors_list)):
            if isinstance(json_sensors_list, list):
                sensors_dict = json_sensors_list[i]
                sensor_type = sensors_dict['name']
                cmd = 'sensor-util ' + sensor_type
                output = execute(deviceObj, cmd)
                ### compare only keys of json objects and sensor-utill output
                parsed_output = parserOpenbmc.parse_sensor_util(output)
                if parsed_output:
                    del sensors_dict['Adapter']
                    del sensors_dict['name']
                    del sensors_dict['present']
                    diff = set(parsed_output) - set(sensors_dict)
                    if not diff:
                        log.success("restful sensors '%s' response keys match"%(sensor_type))
                    else:
                        log.fail("missing sensors: %s"%str(diff))
                        log.fail("restful sensors '%s' response keys mismatch"%(sensor_type))
                        err_count += 1
            else:
                log.fail("wrong format restful response")
                err_count += 1
    else:
        json1 = run_curl(device, GET, restful_url, ip, interface, ipv6)
        if json1 is None:
            log.fail("No json object returned")
            err_count += 1
        else:
            log.success("Sucessfully get restful sensor data")
    if err_count:
        show_unit_info(device)
        raise testFailed("verify_restful_sensors")

def verify_restful_server(device, ip, interface='None', ipv6=False, action='None', status='None', mode=CENTOS_MODE, device2='None'):
    log.debug('Entering procedure verify_restful_server : %s\n'%(str(locals())))
    deviceObj = Device.getDeviceObject(device)
    err_count = 0
    restful_url = 'server'
    # local_ip = '127.0.0.1'
    if action == 'None':
        json1 = run_curl(device, GET, restful_url, ip, interface, ipv6, mode)
        if json1 is None:
            log.fail("No json object returned")
            err_count += 1
        else:
            if json1["Information"]["status"] == status:
                log.success("restful response match '%s', '%s'"%(json1["Information"]["status"], status))
            else:
                log.fail("restful response mismatch '%s', '%s'"%(json1["Information"]["status"], status))
                err_count += 1
    else:
        data = '\'{"action":"power-%s"}\''%(action)
        json1 = run_curl(device, POST, restful_url, ip, interface, ipv6, mode, data)
        time.sleep(3)
        if json1 is None:
            log.fail("No json object returned")
            err_count += 1
        else:
            if ("result" in json1) and (json1["result"] == "success"):
                log.success("Successfully post restful power-%s"%(action))
                if action == 'on' or action == 'reset':
                    # verify_bios_boot(device2)
                    deviceObj_2 = Device.getDeviceObject(device2)
                    deviceObj_2.getPrompt(CENTOS_MODE, timeout=Const.BOOTING_TIME)
            else:
                log.fail("post restful power-%s failed"%(action))
                err_count += 1
    if err_count:
        show_unit_info(device)
        raise testFailed("verify_restful_server")

def verify_bic_util(device, option):
    log.debug('Entering procedure verify_bic_util : %s\n'%(str(locals())))
    deviceObj = Device.getDeviceObject(device)
    err_count = 0
    cmd = 'bic-util scm --' + option
    output = execute(deviceObj, cmd, timeout=300)
    if option == 'get_gpio_config':
        output = output.split(cmd+'\r\n')[-1]
        parsed_output = parserOpenbmc.parse_bic_gpio_config_util(output)
    elif option == 'read_sensor':
        parsed_output = parserOpenbmc.parse_bic_read_sensor(output)
    else:
        parsed_output = parserOpenbmc.parse_util(output)
    if parsed_output:
        log.success("Sucessfully execute %s"%(cmd))
    else:
        log.fail("failed to execute %s"%(cmd))
        show_unit_info(device)
        raise testFailed("verify_bic_util")

def verify_psu_util(device, psu, option, expected_result='None'):
    ### psu-util psu1 --get_psu_info
    log.debug('Entering procedure verify_psu_util : %s\n'%(str(locals())))
    deviceObj = Device.getDeviceObject(device)
    err_count = 0
    log.info('Checking %s status...'%(psu))
    cmd = 'psu-util %s --get_psu_info'%(psu)
    output = execute(deviceObj, cmd)
    if re.search('is not present', output):
        log.info('have no psu: ' + psu)
        return
    elif re.search('get status fail', output):
        log.fail(psu + ' get status fail!')
        err_count += 1
    cmd = 'psu-util %s --%s'%(psu, option)
    output = execute(deviceObj, cmd)
    parsed_output = parserOpenbmc.parse_psu_util(output)
    if expected_result != 'None':
        if 'wedge400c_dc' in deviceObj.name or 'wedge400_dc' in deviceObj.name:
            if 'Delta' in output and option == 'get_psu_info':
                if 'wedge400c_dc-01' in deviceObj.name or 'wedge400_dc-01' in deviceObj.name:
                    result3 = psu2_info_dict_tc_054_Delta_dc_new
                    if 'PRI_FW_VER' in str(expected_result):
                        result3.update(expected_result)
                    expected_result = result3
                else:
                    expected_result = psu2_info_dict_tc_054_Delta_dc
            if 'Liteon' in output and option == 'get_psu_info':
                result4 = psu2_info_dict_tc_054_Liteon_dc
                if 'PRI_FW_VER' in str(expected_result):
                    result4.update(expected_result)
                    expected_result = result4
                else:
                    expected_result = psu2_info_dict_tc_054_Liteon_dc
            if 'DELTA' in output and option == 'get_eeprom_info':
                if 'wedge400c_dc-01' in deviceObj.name or 'wedge400_dc-01' in deviceObj.name:
                    expected_result = psu2_eeprom_dict_tc_054_Delta_dc_rework_new
                else:
                    expected_result = psu2_eeprom_dict_tc_054_Delta_dc_rework
            if 'Liteon' in output and option == 'get_eeprom_info':
                if 'wedge400c_dc-02' in deviceObj.name or 'wedge400_dc-02' in deviceObj.name:
                    expected_result = psu2_eeprom_dict_tc_054_Liteon_dc_rework
                else:
                    expected_result = psu2_eeprom_dict_tc_054_Liteon_dc
        elif 'minipack2_dc' in deviceObj.name:
            if 'Delta' in output and option == 'get_psu_info':
                if psu == 'psu3':
                    if 'minipack2_dc-04' in deviceObj.name or 'minipack2_dc-02' in deviceObj.name or 'minipack2_dc-05' in deviceObj.name:
                        result1 = psu3_info_dict_tc_054_Delta_dc_new
                        if 'PRI_FW_VER' in str(expected_result):
                            result1.update(expected_result)
                        expected_result = result1
                    else:
                        expected_result = psu3_info_dict_tc_054_Delta_dc
                else:
                    if 'minipack2_dc-04' in deviceObj.name or 'minipack2_dc-02' in deviceObj.name or 'minipack2_dc-05' in deviceObj.name:
                        result2 = psu4_info_dict_tc_054_Delta_dc_new
                        if 'PRI_FW_VER' in str(expected_result):
                            result2.update(expected_result)
                        expected_result = result2
                    else:
                        expected_result = psu4_info_dict_tc_054_Delta_dc
            elif 'Liteon' in output and option == 'get_psu_info':
                if psu == 'psu3':
                    res1 = psu3_info_dict_tc_054_Liteon_dc
                    if 'PRI_FW_VER' in str(expected_result):
                        res1.update(expected_result)
                    if 'minipack2_dc-03' in deviceObj.name:
                        res1['MFR_REVISION       (0x9B)'] = 'X4'
                        expected_result = res1
                    else:
                        expected_result = res1
                else:
                    res2 = psu4_info_dict_tc_054_Liteon_dc
                    if 'PRI_FW_VER' in str(expected_result):
                        res2.update(expected_result)
                        expected_result = res2
                    else:
                        expected_result = psu4_info_dict_tc_054_Liteon_dc
            if 'DELTA' in output and option == 'get_eeprom_info':
                if psu == 'psu3':
                    if 'minipack2_dc-04' in deviceObj.name or 'minipack2_dc-02' in deviceObj.name:
                        expected_result = psu3_eeprom_dict_tc_054_Delta_dc_rework_new
                    elif 'minipack2_dc-05' in deviceObj.name:
                        expected_result = psu3_eeprom_dict_tc_054_Delta_dc_rework_new_second
                    else:
                        expected_result = psu3_eeprom_dict_tc_054_Delta_dc
                else:
                    if 'minipack2_dc-04' in deviceObj.name or 'minipack2_dc-02' in deviceObj.name or 'minipack2_dc-05' in deviceObj.name:
                        expected_result = psu4_eeprom_dict_tc_054_Delta_dc_rework_new
                    else:
                        expected_result = psu4_eeprom_dict_tc_054_Delta_dc
            elif 'Liteon' in output and option == 'get_eeprom_info':
                if psu == 'psu3':
                    if 'minipack2_dc-01' in deviceObj.name or 'minipack2_dc-03' in deviceObj.name:
                        expected_result = psu3_eeprom_dict_tc_054_Liteon_dc_rework
                    else:
                        expected_result = psu3_eeprom_dict_tc_054_Liteon_dc
                else:
                    if 'minipack2_dc-01' in deviceObj.name or 'minipack2_dc-03' in deviceObj.name:
                        expected_result = psu4_eeprom_dict_tc_054_Liteon_dc_rework
                    else:
                        expected_result = psu4_eeprom_dict_tc_054_Liteon_dc
        elif 'minipack2_rsp-11' in deviceObj.name:
            if option == 'get_psu_info':
                if psu == 'psu1':
                    expected_result = psu1_info_dict_tc_054_Liteon
                elif psu == 'psu2':
                    expected_result = psu2_info_dict_tc_054_Liteon
                elif psu == 'psu3':
                    expected_result = psu3_info_dict_tc_054_Liteon
                elif psu == 'psu4':
                    expected_result = psu4_info_dict_tc_054_Liteon
            if option == 'get_eeprom_info':
                if psu == 'psu1':
                    expected_result = psu1_eeprom_dict_tc_054_liteon
                elif psu == 'psu2':
                    expected_result = psu2_eeprom_dict_tc_054_liteon
                elif psu == 'psu3':
                    expected_result = psu3_eeprom_dict_tc_054_liteon
                elif psu == 'psu4':
                    expected_result = psu4_eeprom_dict_tc_054_liteon
        if option == 'get_psu_info' and \
            not PRI_FW_VER_KEY in expected_result and \
            not SEC_FW_VER_KEY in expected_result:
            psu_fw_ver = get_version_from_config('PSU')
            expected_result.update(psu_fw_ver)
        err_count += CommonLib.compare_input_dict_to_parsed(parsed_output, expected_result, highlight_fail=True)
        if err_count:
            show_unit_info(device)
            raise testFailed("verify_psu_util '%s' with option '%s' failed"%(psu, option))
    else:
        p1 = '.*error.*'
        match = re.search(p1, output)
        if parsed_output and match is None:
            log.success("Sucessfully execute %s"%(cmd))
            return parsed_output
        elif match:
            log.fail("Found: %s"%(match.group(0)))
            show_unit_info(device)
            raise testFailed("verify_psu_util")
        else:
            log.fail("failed to execute %s"%(cmd))
            show_unit_info(device)
            raise testFailed("verify_psu_util")

def verify_blackbox_psu_util(device, psu, option):
    ### psu-util psu1 --get_psu_info
    log.debug('Entering procedure verify_blackbox_psu_util : %s\n'%(str(locals())))
    deviceObj = Device.getDeviceObject(device)
    err_count = 0
    log.info('Checking %s status...'%(psu))
    cmd = 'psu-util %s --get_psu_info'%(psu)
    output = execute(deviceObj, cmd)
    if re.search('is not present', output):
        log.info('have no psu: ' + psu)
        return
    elif re.search('get status fail', output):
        log.fail(psu + ' get status fail!')
        err_count += 1
    cmd = 'psu-util %s --%s'%(psu, option)
    output = execute(deviceObj, cmd)
    parsed_output = parserOpenbmc.parse_psu_util(output)
    p1 = '.*error.*'
    match = re.search(p1, output)
    if parsed_output and match is None:
        if 'minipack2_dc-04' in deviceObj.name or 'minipack2_dc-02' in deviceObj.name or 'wedge400c_dc-01' in deviceObj.name or 'wedge400_dc-01' in deviceObj.name:
            status_key = 'STATUS_OTHER       (0x7F)'
            status_value = parsed_output[status_key]
            if status_value:
                log.success("Sucessfully execute %s" % (cmd))
            else:
                log.fail("Check %s status fail, the result is %s" % (option, status_value))
                show_unit_info(device)
                raise testFailed("check psu %s" % option)
        else:
            log.success("Sucessfully execute %s"%(cmd))
        return parsed_output
    elif match:
        log.fail("Found: %s"%(match.group(0)))
        show_unit_info(device)
        raise testFailed("verify_psu_util")
    else:
        log.fail("failed to execute %s"%(cmd))
        show_unit_info(device)
        raise testFailed("verify_psu_util")

def verify_presence_util(device, expected_result, pem1_presence=False, pem2_presence=False):
    log.debug('Entering procedure verify_presence_util : %s\n'%(str(locals())))
    deviceObj = Device.getDeviceObject(device)
    err_count = 0
    cmd = 'presence_util.sh'
    output = execute(deviceObj, cmd)
    parsed_output = parserOpenbmc.parse_util(output)
    if pem1_presence or pem2_presence:
        if not pem1_presence:
            expected_result.update({'psu1' : '0'})
        if not pem2_presence:
            expected_result.update({'psu2' : '0'})
    if 'minipack2_dc' in deviceObj.name:
        #if 'minipack2_dc-05' in deviceObj.name:
            #presence_dict_dc['pim6'] = '0'
            #expected_result = presence_dict_dc
        #else:
        expected_result = presence_dict_dc
    #if 'minipack2_rsp2-02' in deviceObj.name or 'minipack2_rsp2-03' in deviceObj.name or 'minipack2_rsp2-04' in deviceObj.name:
        #expected_result = presence_dict_dc
    if 'wedge400c' in deviceObj.name or 'wedge400_' in deviceObj.name:
        power_type = dc_power(device)
        if power_type == 'DC':
            expected_result = presence_dict_dc
        elif power_type == 'pem':
            expected_result = presence_dict_pem
        #elif power_type == 'AC':
            #expected_result.pop('pem11')
            #expected_result.pop('pem12')
    err_count += CommonLib.compare_input_dict_to_parsed(parsed_output, expected_result)
    if err_count:
        show_unit_info(device)
        raise testFailed("verify_presence_util")

def run_util(device, cmd_util, expected_result='None'):
    log.debug('Entering procedure run_util : %s\n'%(str(locals())))
    deviceObj = Device.getDeviceObject(device)
    err_count = 0
    pimNum = 0
    if 'minipack2' in deviceObj.name:
        pimNum = check_mp2_dc_pim(device)
        if pimNum == 5:
            if 'peutil 4' in cmd_util or 'peutil 5' in cmd_util or 'peutil 6' in cmd_util:
                return
        elif pimNum == 4:
            if 'peutil 4' in cmd_util or 'peutil 5' in cmd_util or 'peutil 6' in cmd_util or 'peutil 7' in cmd_util:
                return
    output = execute(deviceObj, cmd_util)
    if cmd_util == 'feutil all':
        parsed_output = parserOpenbmc.parse_fan_util(output)
    else:
        parsed_output = parserOpenbmc.parse_util(output)
    if expected_result != 'None':
        err_count += CommonLib.compare_input_dict_to_parsed(parsed_output, expected_result)
        if err_count:
            show_unit_info(device)
            raise testFailed("run_util")
    else:
        if not parsed_output:
            log.fail("failed to execute '%s'"%(cmd_util))
            show_unit_info(device)
            raise testFailed("run_util")
        return parsed_output

def verify_log_util(device, device_type, option):
    ### log-util scm --print
    log.debug('Entering procedure verify_log_util : %s\n'%(str(locals())))
    deviceObj = Device.getDeviceObject(device)
    timeout = 300
    err_count = 0
    cmd = 'log-util %s --%s'%(device_type, option)
    output = execute(deviceObj, cmd, timeout=timeout)
    if option == 'print':
        p1 = r'(FRU#\sFRU_NAME)|(\d+)\s+(%s)' %(device_type)
        match = re.search(p1, output)
        if match:
            log.success("Successfully execute '%s'" %(cmd))
        else:
            log.fail("failed to execute %s"%(cmd))
            err_count += 1
    elif option == 'clear':
        log.info('verify log %s is cleared'%(device_type))
        set_time_delay('5')
        cmd2 = 'log-util %s --print'%(device_type)
        output2 = execute(deviceObj, cmd2, timeout=timeout)
        # p2 = r'User cleared'
        p2 = r'(\d+)\s+(%s)\s+.*'%(device_type)
        match2 = re.search(p2, output2)
        if match2:
            log.fail("Still found %s"%(match2.group(0)))
            log.fail("failed to clear log %s"%(device_type))
            err_count += 1
        else:
            log.success("Successfully clear log %s" %(device_type))

    if err_count:
        show_unit_info(device)
        raise testFailed("verify_log_util")

def verify_log_util_watchdog(device, timer_use, timer_action, dont_log_flag=False):
    ### log-util scm --print
    log.debug('Entering procedure verify_log_util_watchdog : %s\n'%(str(locals())))
    deviceObj = Device.getDeviceObject(device)
    timeout = 300
    err_count = 0
    cmd = 'log-util scm --print'
    output = execute(deviceObj, cmd, timeout=timeout)
    if timer_action.lower() == 'no action':
        timer_action_key = 'Timer expired'
    else:
        timer_action_key = timer_action.title()
    p1 = r'(\d+)\s+(scm).+FRU: 1,\s(%s)\sWatchdog %s'%(timer_use, timer_action_key)
    match = re.search(p1, output)
    if dont_log_flag:
        if match:
            log.fail("failed to don't log '%s Watchdog %s'"%(timer_use, timer_action_key))
            err_count += 1
        else:
            log.success("Successfully don't log: '%s Watchdog %s'" %(timer_use, timer_action_key))
    else:
        if match:
            log.success("Successfully log: '%s Watchdog %s'" %(timer_use, timer_action_key))
        else:
            log.fail("failed to log '%s Watchdog %s'"%(timer_use, timer_action_key))
            err_count += 1
    if err_count:
        show_unit_info(device)
        raise testFailed("verify_log_util_watchdog")


def verify_sensor_util(device, device_type, option='None', expected_result='None', info_flag=False):
    ### log-util scm --print
    log.debug('Entering procedure verify_sensor_util : %s\n'%(str(locals())))
    deviceObj = Device.getDeviceObject(device)
    timeout = 300
    err_count = 0
    if device_type == 'psu1':
        if 'wedge400_dc' in deviceObj.name or 'wedge400c_dc' in deviceObj.name:
            power_type = dc_power(device)
            if power_type == 'DC':
                log.info('The power is DC unit, so skip the psu1 check!!!')
                return
    if 'minipack2' in deviceObj.name:
        power_type = dc_power(device)
        if power_type == 'DC':
            if device_type == 'psu1' or device_type == 'psu2':
                log.info('The power is DC unit, only support psu3&4!!!')
                return
    cmd = 'sensor-util %s'%(device_type)
    if option != 'None':
        cmd += ' --%s'%(option)
    output = execute(deviceObj, cmd, timeout=timeout)
    if option == 'threshold':
        parsed_output = parserOpenbmc.parse_sensor_util_threshold(output)
    elif 'history' in option:
        if 'clear' in option:
            return
        else:
            parsed_output = parserOpenbmc.parse_sensor_util_history(output)
    else:
        parsed_output = parserOpenbmc.parse_sensor_util_force(output)

    ##### ignore some sensors in comparison #####
    for ignore_key in SENSOR_IGNORE_KEY_LIST:
        if ignore_key in parsed_output:
            del parsed_output[ignore_key]

    if expected_result != 'None':
        expected_dict = SensorCsv.getSensorDictByType(expected_result)
        if not parsed_output and device_type == 'pem2':
            log.info('%s is not present, so skip the device.' % device_type)
            return
        if not parsed_output:
            log.fail("no sensor output return")
            err_count += 1
        for key in parsed_output.keys():
            if key in expected_dict:
                log.info("sensor name: %s matched in sensor spec"%(key))
                if info_flag:
                    log.info("compare info for sensor name: %s"%(key))
                    err_count += compare_sensor_info(parsed_output[key], expected_dict[key], key)

                if option == 'threshold':
                    ##### pop key 'Sensor Type', 'S0', 'S5' in comparison #####
                    if SensorCsv.THRESHOLD_S0 in expected_dict[key]:
                        expected_dict[key].pop(SensorCsv.THRESHOLD_S0)
                    if SensorCsv.THRESHOLD_S5 in expected_dict[key]:
                        expected_dict[key].pop(SensorCsv.THRESHOLD_S5)
                    if SensorCsv.SENSOR_TYPE in expected_dict[key]:
                        expected_dict[key].pop(SensorCsv.SENSOR_TYPE)
                    log.info("compare threshold for sensor name: %s"%(key))
                    err_count += compare_sensor_threshold(parsed_output[key], expected_dict[key])

            else:
                log.fail("sensor name: %s does not match in sensor spec"%(key))
                err_count += 1
    else:
        if parsed_output:
            log.success("Sucessfully execute %s"%(cmd))
            return parsed_output
        else:
            match = re.search('not present', output)
            if match:
                return
            log.fail("failed to execute %s"%(cmd))
            err_count += 1
    if err_count:
        show_unit_info(device)
        raise testFailed("verify_sensor_util")

@logThis
def prepare_minipack2_images(device, scp_ip, usrname, pasrd, local_path, scp_path):
    deviceObj = Device.getDeviceObject(device)
    cmd = 'scp -r ' + usrname + '@' + scp_ip + ':' + local_path + ' ' + scp_path
    deviceObj.sendCmd(cmd)
 
    log.info("////local path = %s " % local_path)
    log.info("////scp_path = %s " % scp_path)
    promptList = ["(yes/no)", "password:"]
    patternList = re.compile('|'.join(promptList))
    output1 = deviceObj.read_until_regexp(patternList, 120)
    log.info('output1: ' + str(output1))
    match1 = re.search("(yes/no)", output1)
    match3 = re.search("password:", output1)
    if match1:
        deviceObj.transmit("yes")
        deviceObj.receive("password:")
        deviceObj.transmit("%s" % pasrd)
    elif match3:
        deviceObj.transmit("%s" % pasrd)
    else:
        log.fail("pattern mismatch")
        show_unit_info(device)

def prepare_i2c_device(device, bus, addr, delete_flag=False):
    ### source /usr/local/bin/openbmc-utils.sh
    ### i2c_device_delete 31 0x51
    ### i2c_device_add 31 0x51 24c64
    log.debug('Entering procedure prepare_i2c_device : %s\n'%(str(locals())))
    deviceObj = Device.getDeviceObject(device)
    execute(deviceObj, "source /usr/local/bin/openbmc-utils.sh")
    if delete_flag:
        execute(deviceObj, "i2c_device_delete %s %s"%(bus, addr))
    execute(deviceObj, "i2c_device_add %s %s 24c64"%(bus, addr))
    time.sleep(1)

def get_eeprom_info(device, option, old_dict=None):
    log.debug('Entering procedure get_eeprom_info : %s\n'%(str(locals())))
    deviceObj = Device.getDeviceObject(device)
    cmd = './eeprom_tool -' + option
    output = execute(deviceObj, cmd)
    parsed_output = parserOpenbmc.parse_eeprom(output)
    for key, value in old_dict.items():
        old_dict[key] = parsed_output[key]
        log.cprint(old_dict[key])

def dc_power(device):
    log.debug('dc_power : %s\n' % (str(locals())))
    deviceObj = Device.getDeviceObject(device)
    cmd = 'pem-util pem2 --get_pem_info'
    output = execute(deviceObj, cmd)
    match = re.search('is not present|command not found', output)
    if match:
        if 'minipack2' in deviceObj.name:
            cmd1 = "sensor-util psu3 |grep 'PSU3_IN_VOLT' |awk '{print$4}'"
        else:
            cmd1 = "sensor-util psu2 |grep 'PSU2_IN_VOLT' |awk '{print$4}'"
        output1 = execute(deviceObj, cmd1)
        p1 = r'^\d+.*\d$'
        for line in output1.splitlines():
            line = line.strip()
            match1 = re.search(p1, line)
            if match1:
                volt_value = match1.group()
                if float(volt_value) > 60:
                    log.info("This unit use AC PSU")
                    return 'AC'
                else:
                    log.info("This unit use DC")
                    return 'DC'
    else:
        log.info("This unit use PEM")
        return 'pem'

def init_diag_config(device):
    log.debug('init_diag_config : %s\n' % (str(locals())))
    deviceObj = Device.getDeviceObject(device)
    time.sleep(2)
    if 'wedge400_dc' in deviceObj.name or 'wedge400c_dc' in deviceObj.name:
        log.info("It is DC power, so use '-d' parameter")
        cmd = './cel-diag-init -c'
    elif 'wedge400_mp' in deviceObj.name:
        log.info("It is Respin PEM power, so use '-m' parameter")
        cmd = './cel-diag-init -m'
    elif 'minipack2' in deviceObj.name:
        if 'rsp' in deviceObj.name:
            log.info("This unit is respin machine")
            cmd = './cel-diag-init -r'
        else:
            cmd = "sensor-util psu3 |grep 'PSU3_IN_VOLT' |awk '{print$4}'"
            output1 = execute(deviceObj, cmd)
            p1 = r'^\d+'
            for line in output1.splitlines():
                line = line.strip()
                match1 = re.search(p1, line)
                if match1:
                    volt_value = match1.group()
                    if float(volt_value) > 60:
                        log.info("This unit use AC PSU")
                        cmd = './cel-diag-init -a'
                    else:
                        log.info("This unit is DC machine.")
                        cmd = './cel-diag-init -c'
    else:
        power_type = dc_power(device)
        if power_type == 'AC':
            if 'rsp' in deviceObj.name:
                log.info("It is AC power respin unit, so use '-r' parameter")
                cmd = './cel-diag-init -r'
            else:
                log.info("It is AC power, so use '-a' parameter")
                cmd = './cel-diag-init -a'
        elif power_type == 'pem':
            if 'rsp' in deviceObj.name:
                log.info("It is pem power respin unit, so use '-m' parameter")
                cmd = './cel-diag-init -m'
            else:
                log.info("It is pem power unit, so use '-p' parameter")
                cmd = './cel-diag-init -p'
    output = execute(deviceObj, cmd)

def check_mp2_dc_pim(device):
    log.debug('Entering procedure check_mp2_dc_pim : %s\n'%(str(locals())))
    deviceObj = Device.getDeviceObject(device)
    pim_count = 0
    power_type = dc_power(device)
    if power_type == 'DC':
        cmd = 'fpga_ver.sh'
        output = execute(deviceObj, cmd)
        p1 = r'^DOMFPGA.*PIM\s(\d)\sis not inserted'
        for line in output.splitlines():
            line = line.strip()
            match = re.search(p1, line)
            if match:
                pim_count += 1
        return 8 - pim_count

def run_eeprom_tool(device, option, eeprom_type, fan='None', expected_result='None', flag='None'):
    log.debug('Entering procedure run_eeprom_tool : %s\n'%(str(locals())))
    deviceObj = Device.getDeviceObject(device)
    err_count = 0
    pimNum = 0
    if 'minipack2' in deviceObj.name or 'PEM' in eeprom_type:
        if 'PIM' in eeprom_type:
            pimNum = check_mp2_dc_pim(device)
            if pimNum == 5:
                if (str(fan) == '3') or (str(fan) == '4') or (str(fan) == '5'):
                    return
            elif pimNum == 4:
                if (str(fan) == '3') or (str(fan) == '4') or (str(fan) == '5') or (str(fan) == '6'):
                    return
        if flag == 'PIM':
            if 'FAN' in eeprom_type:
                pimNum = check_mp2_dc_pim(device)
                if pimNum == 5:
                    if (str(fan) == '3') or (str(fan) == '4') or (str(fan) == '5'):
                        return
                elif pimNum == 4:
                    if (str(fan) == '3') or (str(fan) == '4') or (str(fan) == '5') or (str(fan) == '6'):
                        return
        if fan != 'None':
            if option == 'd':
                cmd = './eeprom_tool -' + option + ' -f ' + str(fan)
            else:
                cmd = './eeprom_tool -w -f %s; ./eeprom_tool -u -f %s'%(str(fan), str(fan))
        else:
            if option == 'd':
                cmd = './eeprom_tool -' + option
            else:
                cmd = './eeprom_tool -w; ./eeprom_tool -u'
    else:
        if option == 'd':
            cmd = './eeprom_tool -%s -e %s'%(option, eeprom_type)
        else:
            cmd = './auto_eeprom %s'%(eeprom_type)
    if 'HOTSWAP' in eeprom_type:
        cmd = './hotswap_eeprom_tool -' + option
    output = execute(deviceObj, cmd)
    time.sleep(1)
    if option == 'd':
        if 'HOTSWAP' in eeprom_type:
            parsed_output = parserOpenbmc.parse_util(output)
        else:
            parsed_output = parserOpenbmc.parse_eeprom(output)
        if expected_result != 'None':
            if 'minipack2_dc' in deviceObj.name:
                if expected_result == sim_eeprom_product_name:
                    expected_result = sim_eeprom_product_name_dc
                elif expected_result == sim_eeprom_test:
                    expected_result = sim_eeprom_test_dc
                elif expected_result == sim_eeprom_test2:
                    expected_result = sim_eeprom_test2_dc
            elif 'wedge400c' in deviceObj.name or 'wedge400_' in deviceObj.name:
                power_type = dc_power(device)
                if power_type == 'DC':
                    if expected_result == smb_eeprom_product_name:
                        expected_result = smb_eeprom_product_name_dc
            expected_dict = CommonLib.get_eeprom_cfg_dict(expected_result)
            parsed_type = parserOpenbmc.parse_eeprom_type(output)
            if parsed_type == eeprom_type:
                log.success("EEPROM type match: %s, %s"%(parsed_type, eeprom_type))
            else:
                log.fail("EEPROM type mismatch: %s, %s"%(parsed_type, eeprom_type))
                err_count += 1
            err_count += CommonLib.compare_input_dict_to_parsed(parsed_output, expected_dict)
        else:
            if parsed_output:
                log.success("Successfully run_eeprom_tool")
                return parsed_output
            else:
                log.fail("No eeprom output returned")
                err_count += 1
    else:
        p1 = 'error|No such file or directory|fail'
        match = re.search(p1, output, re.IGNORECASE)
        if match:
            log.fail("found error in the output")
            err_count += 1
        else:
            log.success("Successfully run_eeprom_tool with option '%s'"%(option))
    if err_count:
        show_unit_info(device)
        raise testFailed("run_eeprom_tool")

def store_eeprom(device, eeprom_cfg_file, store_file, eeprom_path=None):
    log.debug('Entering procedure store_eeprom with args : %s\n' %(str(locals())))
    deviceObj = Device.getDeviceObject(device)
    if eeprom_path:
        execute(deviceObj, 'cd ' + eeprom_path)
    time.sleep(2)
    pimNum = check_mp2_dc_pim(device)
    if pimNum == 5:
        if 'eeprom_out' in eeprom_cfg_file:
            if 'store3' in store_file or 'store4' in store_file or 'store5' in store_file:
                return
        if store_file == 'eeprom.cfg':
            if 'store3' in eeprom_cfg_file or 'store4' in eeprom_cfg_file or 'store5' in eeprom_cfg_file:
                return
    elif pimNum == 4:
        if 'eeprom_out' in eeprom_cfg_file:
            if 'store3' in store_file or 'store4' in store_file or 'store5' in store_file or 'store6' in store_file:
                return
        if store_file == 'eeprom.cfg':
            if 'store3' in eeprom_cfg_file or 'store4' in eeprom_cfg_file or 'store5' in eeprom_cfg_file or 'store6' in eeprom_cfg_file:
                return
    cmd = "cp %s %s"%(eeprom_cfg_file, store_file)
    output = execute(deviceObj, cmd)
    p1 = 'No such file or directory'
    match = re.search(p1, output)
    if match:
        log.fail("Cannot store eeprom data")
        show_unit_info(device)
        raise testFailed("store_eeprom")
    else:
        log.success("Successfully store eeprom data")

def modify_eeprom_cfg(device, eeprom_name, eeprom_cfg_file):
    ### echo '''<eeprom_string>''' > eeprom.cfg
    log.debug('Entering procedure modify_eeprom_cfg with args : %s\n' %(str(locals())))
    deviceObj = Device.getDeviceObject(device)
    err_count = 0
    if 'minipack2' in deviceObj.name:
        power_type = dc_power(device)
        if power_type == 'DC':
            if eeprom_name == sim_eeprom_test:
                eeprom_name = sim_eeprom_test_dc
            elif eeprom_name == sim_eeprom_test2:
                eeprom_name = sim_eeprom_test2_dc
    eeprom_string = CommonLib.fb_generate_eeprom_cfg(eeprom_name)
    cmd = "echo -e \"%s\" > %s"%(eeprom_string, eeprom_cfg_file)
    execute(deviceObj, cmd, timeout=150)
    time.sleep(1)
    log.success("modify %s"%(eeprom_cfg_file))

def read_test_emmc(device, dump_name):
    log.debug('Entering procedure read_test_emmc with args : %s\n' %(str(locals())))
    deviceObj = Device.getDeviceObject(device)
    hexdump_cmd = 'hexdump -C ' + dump_name
    output = execute(deviceObj, hexdump_cmd)
    p1 = r'00000000  00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00  .*\s\*.*\s00100000'
    if parserOpenbmc.parse_simple_keyword(p1, output) != "":
        log.success("Successfully read_test_emmc")
    else:
        log.fail("read_test_emmc failed")
        show_unit_info(device)
        raise testFailed("read_test_emmc")

def set_ipmi_cmd(device, cmd):
    log.debug('Entering procedure set_ipmi_cmd : %s\n'%(str(locals())))
    deviceObj = Device.getDeviceObject(device)
    err_count = 0
    execute(deviceObj, cmd, mode=CENTOS_MODE)
    time.sleep(1)

def run_ipmi_get_cmd(device, cmd, expected_result='None'):
    log.debug('Entering procedure run_ipmi_get_cmd with args : %s\n' %(str(locals())))
    deviceObj = Device.getDeviceObject(device)
    err_count = 0
    # output = execute(deviceObj, cmd, mode=CENTOS_MODE)
    for i in range(2):
        output = deviceObj.execute(cmd, mode=CENTOS_MODE)
        result = parserOpenbmc.parse_oem_output(output)
        error_msg = r'.*No such file or directory'
        if expected_result != 'None':
            if result == expected_result:
                log.success("run cmd \'%s\': result: \'%s\'"%(cmd, result))
            else:
                if i == 1 and cmd == 'ipmitool raw 0x06 0x04':
                    continue
                log.fail("Command result Mismatch: Found \'%s\' Expected \'%s\'\n"%(result, expected_result))
                err_count += 1
        else:
            if result != '' and re.search(error_msg, result) is None:
                log.success("Successfully execute '%s'"%(cmd))
                return result
            else:
                log.fail("failed to execute %s"%(cmd))
                err_count += 1
        if i == 1:
            if err_count:
                show_unit_info(device)
                raise testFailed("Failed run_ipmi_get_cmd")

def run_ipmi_set_cmd(device, cmd, test_name='None'):
    log.debug('Entering procedure run_ipmi_set_cmd : %s\n'%(str(locals())))
    deviceObj = Device.getDeviceObject(device)
    if test_name == 'None':
        test_name = 'run_ipmi_set_cmd'
    if 'wedge400c_rsp' in deviceObj.name or 'wedge400_rsp' in deviceObj.name or 'dc' in deviceObj.name or 'wedge400_d2-01' in deviceObj.name or 'wedge400c_d1-20' in deviceObj.name:
        if 'minipack2_dc-04' not in deviceObj.name:
            if '0x04' in cmd and '0x12' in cmd:
                cmd = cmd.split('0x04')[0] + '0x04 ' + cmd_DIMM_module_part_num_test_rsp
            if '0x06' in cmd and '0x12' in cmd:
                cmd = cmd.split('0x06')[0] + '0x06 ' + cmd_DIMM_module_manu_id_test_rsp
        else:
            if '0x04' in cmd and '0x12' in cmd:
                cmd = cmd.split('0x04')[0] + '0x04 ' + cmd_DIMM_module_part_num_test_dc
            if '0x06' in cmd and '0x12' in cmd:
                cmd = cmd.split('0x06')[0] + '0x06 ' + cmd_DIMM_module_manu_id_test_rsp_NewCOMe
    if 'wedge400c_d1-13' in deviceObj.name or 'wedge400_mp-03' in deviceObj.name or 'minipack2_d1-10' in deviceObj.name:
        if '0x04' in cmd and '0x12' in cmd:
            cmd = cmd.split('0x04')[0] + '0x04 ' + cmd_DIMM_module_part_num_test_rsp_newCOMe
        if '0x06' in cmd and '0x12' in cmd:
            cmd = cmd.split('0x06')[0] + '0x06 ' + cmd_DIMM_module_manu_id_test_rsp
    if 'wedge400c_d1-17' in deviceObj.name or 'wedge400_d2-02' in deviceObj.name:
        if '0x04' in cmd and '0x12' in cmd:
            cmd = cmd.split('0x04')[0] + '0x04 ' + cmd_DIMM_module_part_num_test_rsp_newCOMe_SKU1
        if '0x06' in cmd and '0x12' in cmd:
            cmd = cmd.split('0x06')[0] + '0x06 ' + cmd_DIMM_module_manu_id_test_rsp_NewCOMe
    if ('minipack2_rsp-11' in deviceObj.name) or ('minipack2_rsp-12' in deviceObj.name) or ('minipack2_rsp-13' in deviceObj.name) or ('minipack2_rsp2' in deviceObj.name):
        if '0x04' in cmd and '0x12' in cmd:
            cmd = cmd.split('0x04')[0] + '0x04 ' + cmd_DIMM_module_part_num_test_rsp
        if '0x06' in cmd and '0x12' in cmd:
            cmd = cmd.split('0x06')[0] + '0x06 ' + cmd_DIMM_module_manu_id_test_rsp
    output = execute(deviceObj, cmd, mode=CENTOS_MODE)
    parsed_output = parserOpenbmc.parse_oem_rsp_code(output)
    error_msg = r'.*No such file or directory'
    match_error = re.search(error_msg, output)
    time.sleep(1)
    if not parsed_output and match_error is None:
        log.success("Successfully %s, execute \'%s\'"%(test_name, cmd))
    else:
        if parsed_output["code"]:
            log.fail("Command error: rsp=\'%s\', \'%s\'\n"%(parsed_output["code"], parsed_output["message"]))
        elif "invalid" in parsed_output:
            log.fail("Invalid command: %s"%(parsed_output["invalid"]))
        elif match_error:
            log.fail("%s"%(match_error.group(0)))
        else:
            log.fail("Unknown error")
        show_unit_info(device)
        raise testFailed("Failed %s"%(test_name))

def run_ipmi_cmd_cold_reset(device, cmd):
    log.debug('Entering procedure run_ipmi_cmd_cold_reset with args : %s\n' %(str(locals())))
    err_count = 0
    deviceObj = Device.getDeviceObject(device)
    deviceObj.getPrompt(CENTOS_MODE)
    deviceObj.sendline(cmd)
    error_msg = r'(.*command failed.+error)'
    uboot_msg = 'U-Boot.*'
    booting_msg = 'Starting kernel ...'
    if 'minipack2' in deviceObj.name:
        time.sleep(15)
        deviceObj.sendline('\n')
    output2 = deviceObj.read_until_regexp(uboot_msg, timeout=60)
    match_err = re.search(error_msg, output2)
    if match_err:
        log.fail("Found error: %s"%(match_err.group(1)))
        err_count += 1
    deviceObj.read_until_regexp(booting_msg, timeout=90)
    time.sleep(200)
    deviceObj.getPrompt(OPENBMC_MODE, timeout=Const.BOOTING_TIME)
    #if 'minipack2' in deviceObj.name or 'cloudripper' in deviceObj.name:
        ### need to run this command to link the driver when BMC boot up
     #   deviceObj.execute('ln -s ld-2.29.so /lib/ld-linux.so.3')
    time.sleep(60)
    if err_count:
        show_unit_info(device)
        raise testFailed("run_ipmi_cmd_cold_reset")

def run_ipmi_clear_sel(device, cmd, reserve_id, request_cmd):
    log.debug('Entering procedure run_ipmi_clear_sel : %s\n'%(str(locals())))
    reserve_id_hex = reserve_id.split()
    reserve_id_hex = ['0x' + id for id in reserve_id_hex]
    reserve_id_hex = ' '.join(reserve_id_hex)
    clear_cmd = '%s %s %s'%(cmd, reserve_id_hex, request_cmd)
    run_ipmi_set_cmd(device, clear_cmd)

def run_ipmi_set_sys_info(device, cmd, isActualBios=True):
    log.debug('Entering procedure run_ipmi_set_sys_info : %s\n'%(str(locals())))
    bios_version = get_version_from_config('BIOS', isActualBios)
    cmd_bios_version = parserOpenbmc.parse_string_to_hex(bios_version['BIOS Version'])
    set_cmd = "%s %s"%(cmd, cmd_bios_version)
    log.debug("cmd: %s"%(set_cmd))
    run_ipmi_set_cmd(device, set_cmd)

def run_ipmi_get_sys_info(device, cmd, isActualBios=True):
    log.debug('Entering procedure run_ipmi_get_sys_info : %s\n'%(str(locals())))
    parsed_output = parser()
    err_count = 0
    output = run_ipmi_get_cmd(device, cmd)
    test_name = 'sys_info'
    parser_command = 'parserOpenbmc.parse_rsp_to_byte_' + test_name + '(output)'
    parsed_output = eval(parser_command)
    expected_result = get_version_from_config('BIOS', isActualBios)
    err_count += CommonLib.compare_input_dict_to_parsed(parsed_output, expected_result)
    if err_count:
        show_unit_info(device)
        raise testFailed("run_ipmi_get_sys_info while testing %s"%(test_name))

def run_ipmi_get_lan_config(device, cmd, expected_result, fail_result):
    log.debug('Entering procedure run_ipmi_get_lan_config : %s\n'%(str(locals())))
    parsed_output = parser()
    err_count = 0
    output = run_ipmi_get_cmd(device, cmd)
    test_name = 'get_lan_config'
    parser_command = 'parserOpenbmc.parse_rsp_to_byte_' + test_name + '(output)'
    parsed_output = eval(parser_command)
    parsed_output_1 = parsed_output.pop('byte4-21')
    err_count += CommonLib.compare_input_dict_to_parsed(parsed_output, expected_result)
    log.info('compare byte4 - byte21')
    if parsed_output_1 != fail_result:
        log.success("byte 4~21 does not match %s, found %s"%(fail_result, parsed_output_1))
    else:
        log.fail("byte 4~21 match %s, found %s"%(fail_result, parsed_output_1))
        err_count += 1
    if err_count:
        show_unit_info(device)
        raise testFailed("run_ipmi_get_lan_config while testing %s"%(test_name))

def run_ipmi_get_device_guid(device, cmd, expected_result):
    log.debug('Entering procedure run_ipmi_get_device_guid : %s\n'%(str(locals())))
    parsed_output = parser()
    success_count = 0
    output = run_ipmi_get_cmd(device, cmd)
    for exp in expected_result:
        if output == exp:
            log.success("run cmd '%s': result: '%s'"%(cmd, exp))
            success_count += 1
    if success_count == 0:
        log.fail("run cmd '%s': result does not match %s"%str(expected_result))
        show_unit_info(device)
        raise testFailed("run_ipmi_get_device_guid")

def run_ipmi_get_test(test_name, device, cmd, expected_result='None'):
    log.debug('Entering procedure run_ipmi_get_test : %s\n'%(str(locals())))
    parsed_output = parser()
    err_count = 0
    output = run_ipmi_get_cmd(device, cmd)
    parser_command = 'parserOpenbmc.parse_rsp_to_byte_' + test_name + '(output)'
    log.debug("call parser: %s" %parser_command)
    parsed_output = eval(parser_command)
    if expected_result != 'None':
        if test_name == "get_device_id":
            expected_result['Firmware Revision'] = parse_version(get_firmware_rev(device)['Firmware Revision'])
        elif test_name == "board_id" and ('minipack2' not in deviceObj.name):
            log.info("check board type")
            board_rev_id = get_brd_id_by_board_type(device)
            expected_result.update({"Board Revision ID" : board_rev_id})
        elif test_name == "dimm_module_part_num":
            if ('wedge400c_rsp' in deviceObj.name) or ('wedge400_rsp' in deviceObj.name) or ('dc' in deviceObj.name) or ('wedge400_d2-01' in deviceObj.name) or ('wedge400c_d1-20' in deviceObj.name):
                if 'minipack2_dc-04' in deviceObj.name:
                    expected_result = rsp_DIMM0_module_part_num
                else:
                    expected_result = rsp_DIMM0_module_part_num_rsp
            elif ('wedge400c_d1-13' in deviceObj.name) or ('wedge400_mp-03' in deviceObj.name) or ('minipack2_d1-10' in deviceObj.name):
                expected_result = rsp_DIMM0_module_part_num_rsp_newCOMe
            elif ('minipack2_rsp-11' in deviceObj.name) or ('minipack2_rsp-12' in deviceObj.name) or ('minipack2_rsp-13' in deviceObj.name) or ('minipack2_rsp2' in deviceObj.name):
                expected_result = rsp_DIMM0_module_part_num_rsp
            elif ('wedge400c_d1-17' in deviceObj.name) or ('wedge400_d2-02' in deviceObj.name):
                expected_result = rsp_DIMM0_module_part_num_rsp_newCOMe_SKU1
        elif test_name == "dimm_module_manu_id" and (('wedge400c_rsp' in deviceObj.name) or ('wedge400_d2-01' in deviceObj.name) or ('wedge400c_d1-20' in deviceObj.name) or ('wedge400_rsp' in deviceObj.name) or ('dc' in deviceObj.name)):
            if 'minipack2_dc-04' in deviceObj.name:
                expected_result = rsp_DIMM0_module_manu_id
            else:
                expected_result = rsp_DIMM0_module_manu_id_rsp
        elif test_name == "dimm_module_manu_id" and (('minipack2_rsp-11' in deviceObj.name) or ('minipack2_rsp-12' in deviceObj.name) or ('minipack2_rsp-13' in deviceObj.name) or ('minipack2_rsp2' in deviceObj.name)):
            expected_result = rsp_DIMM0_module_manu_id_rsp
        elif test_name == "dimm_module_manu_id" and (('wedge400c_d1-13' in deviceObj.name) or ('wedge400_mp-03' in deviceObj.name) or ('minipack2_d1-10' in deviceObj.name)):
            expected_result = rsp_DIMM0_module_manu_id_rsp
        elif test_name == "dimm_module_manu_id" and (('wedge400c_d1-17' in deviceObj.name) or ('wedge400_d2-02' in deviceObj.name)):
            expected_result = rsp_DIMM0_module_manu_id
        err_count += CommonLib.compare_input_dict_to_parsed(parsed_output, expected_result)
    else:
        return parsed_output
    if err_count:
        show_unit_info(device)
        raise testFailed("run_ipmi_get_test while testing %s"%(test_name))

def check_error_code(device, cmd, input_array):
    log.debug('Entering procedure check_error_code : %s\n'%(str(locals())))
    deviceObj = Device.getDeviceObject(device)
    output = execute(deviceObj, cmd, mode=CENTOS_MODE)
    parsed_output = parserOpenbmc.parse_oem_rsp_code(output)
    errCount = CommonLib.compare_input_dict_to_parsed(parsed_output, input_array)
    if errCount:
        log.fail("completion code Mismatch")
        show_unit_info(device)
        raise testFailed("Failed check_error_code")
    else:
        log.success("Successfully check_error_code")

def set_watchdog(device, cmd, timer_use, timer_action, pre_timer, timer_use_expr, countdown):
    log.debug('Entering procedure set_watchdog : %s\n'%(str(locals())))
    deviceObj = Device.getDeviceObject(device)
    set_cmd = '%s %s %s %s %s %s'%(cmd, timer_use, timer_action, pre_timer, timer_use_expr, countdown)
    run_ipmi_set_cmd(device, set_cmd)
    time.sleep(1)

def get_watchdog(device, cmd, expected_result, start_flag=False, previous_t=None):
    log.debug('Entering procedure get_watchdog : %s\n'%(str(locals())))
    err_count = 0
    if start_flag:
        start_bit = 1<<6
        expected_result = expected_result.split()
        expected_result[0] = hex(int(expected_result[0], 0) | start_bit)
        expected_result = ' '.join(expected_result)
        # log.debug('expected_result: %s'%(expected_result))
    expected_result = re.sub('0x', '', expected_result)
    log.info('expected result:')
    exp_wdt = parserOpenbmc.parse_rsp_to_byte_wdt(expected_result)

    parsed_output = run_ipmi_get_cmd(device, cmd)
    parsed_wdt = parserOpenbmc.parse_rsp_to_byte_wdt(parsed_output)

    err_count += CommonLib.compare_input_dict_to_parsed(parsed_wdt, exp_wdt)
    if start_flag:
        ### countdown value, lsbyte (100ms/count) ###
        if previous_t is None:
            previous_t = int("%s%s"%(parsed_wdt['init countdown msb'], parsed_wdt['init countdown lsb']), 16) * 0.1
        present_t = int("%s%s"%(parsed_wdt['present countdown msb'], parsed_wdt['present countdown lsb']), 16) * 0.1
        log.info("compare present countdown and previous countdown")
        if present_t < previous_t:
            log.success("present countdown: %f s is less than previous countdown: %f s"%(present_t, previous_t))
            return present_t
        else:
            log.fail("present countdown: %f s is greater than or equal previous countdown: %f s"%(present_t, previous_t))
            err_count += 1
    if err_count:
        show_unit_info(device)
        raise testFailed("get_watchdog")

def clear_cpu_log(device, log_path):
    log.debug('Entering procedure clear_cpu_log : %s\n'%(str(locals())))
    deviceObj = Device.getDeviceObject(device)
    cmd = 'rm %s'%(log_path)
    output = execute(deviceObj, cmd)
    p1 = 'No such file or directory'
    match = re.search(p1, output)
    if match:
        log.info("%s" %(p1))
        # raise testFailed("clear_cpu_log: %s"%(log_path))
    else:
        log.success("Successfully clear_cpu_log: %s"%(log_path))

def verify_cpu_log(device, log_path, test_cmd):
    log.debug('Entering procedure verify_cpu_log : %s\n'%(str(locals())))
    deviceObj = Device.getDeviceObject(device)
    err_count = 0
    cmd = 'cat %s'%(log_path)
    keys = ['OS loading', 'login prompt', 'CPU console', 'BIOS post', 'test executed command']
    deviceObj.getPrompt(OPENBMC_MODE)
    # deviceObj.flush()
    output = deviceObj.execute(cmd, exe_timeout=200, checkLoginPrompt=False)
    # output = deviceObj.receive(deviceObj.getCurrentPromptStr(), timeout=120)
    p1 = 'No such file or directory'
    match = re.search(p1, output)
    if match:
        log.fail("%s" %(p1))
        err_count += 1
    else:
        parsed_output = parserOpenbmc.parse_cpu_uart_log(output, test_cmd)
        for key in keys:
            if parsed_output[key]:
                log.success("Found %s in %s"%(key, log_path))
            else:
                log.fail("%s not found in %s"%(key, log_path))
                err_count += 1
    if err_count:
        show_unit_info(device)
        raise testFailed("verify_cpu_log: %s"%(log_path))
    else:
        log.success("Successfully verify_cpu_log: %s"%(log_path))

def verify_cpu_reboot_log(device, log_path, reboot_times):
    log.debug('Entering procedure verify_cpu_reboot_log : %s\n'%(str(locals())))
    deviceObj = Device.getDeviceObject(device)
    err_count = 0
    # cmd = 'cat %s'%(log_path)
    cmd = 'grep reboot %s'%(log_path)
    deviceObj.getPrompt(OPENBMC_MODE)
    output = deviceObj.execute(cmd, exe_timeout=20, checkLoginPrompt=False)
    # output = deviceObj.receive(deviceObj.getCurrentPromptStr(), timeout=timeout)
    p1 = 'No such file or directory'
    match = re.search(p1, output)
    if match:
        log.fail("%s" %(p1))
        err_count += 1
    else:
        parsed_output = parserOpenbmc.parse_cpu_uart_reboot_log(output)
        if len(parsed_output) == int(reboot_times):
            log.success("Found reboot log record %d time(s)"%(int(reboot_times)))
            for p_output in parsed_output:
                log.success("%s"%(p_output))
        else:
            log.fail("reboot log record mismatch")
            err_count += 1
    if err_count:
        show_unit_info(device)
        raise testFailed("verify_cpu_reboot_log: %s"%(log_path))
    else:
        log.success("Successfully verify_cpu_reboot_log: %s"%(log_path))

def run_memtester(device, mem_size, iteration):
    log.debug('Entering procedure run_memtester : %s\n'%(str(locals())))
    deviceObj = Device.getDeviceObject(device)
    err_count = 0
    timeout = int(mem_size.replace('M', '')) * 110
    if 'minipack3' in deviceObj.name or 'minerva' in deviceObj.name:
        change_per = 'chmod +x memtester'
        execute(deviceObj, change_per, timeout=timeout)
    cmd = './memtester %s %s'%(mem_size, iteration)
    output = execute(deviceObj, cmd, timeout=timeout)
    done_msg = 'Done.'
    match = re.search(done_msg, output)
    if match:
        log.success("Successfully run memtester")
    else:
        log.fail("run memtester failed")
        err_count += 1
    if err_count:
        show_unit_info(device)
        raise testFailed("run_memtester")

def run_i2ctool(device, option, bus, addr, reg, val='None', expected_result='None'):
    log.debug('Entering procedure run_i2ctool : %s\n'%(str(locals())))
    deviceObj = Device.getDeviceObject(device)
    deviceObj.receive('\n', timeout=60)
    err_count = 0
    err_msg = r'Error: .*'
    if val == 'None':
        cmd = 'i2c%s -f -y %s %s %s'%(option, bus, addr, reg)
    else:
        cmd = 'i2c%s -f -y %s %s %s %s'%(option, bus, addr, reg, val)
    #output = execute(deviceObj, cmd)
    cmd = 'time ' + cmd
    output = deviceObj.sendCmdRegexp(cmd, Const.TIME_REG_PROMPT, timeout=60)
    match = re.search(err_msg, output)
    if match:
        log.fail("found error")
        raise testFailed("run_i2ctool")
    parsed_output = parserOpenbmc.parse_oem_output(output)
    # print(parsed_output)
    if expected_result != 'None':
        if parsed_output == expected_result:
            log.success("result match: %s, %s"%(parsed_output, expected_result))
        else:
            log.fail("result mismatch: %s, %s"%(parsed_output, expected_result))
            show_unit_info(device)
            raise testFailed("run_i2ctool")

def test_execute_command(device, test_cmd, mode, expected_result='None'):
    log.debug('Entering procedure test_execute_command : %s\n'%(str(locals())))
    deviceObj = Device.getDeviceObject(device)
    output = execute(deviceObj, test_cmd, mode=mode)
    if expected_result != 'None':
        match = re.search(expected_result, output)
        if match:
            log.success("Found keyword: %s in output"%(match.group(0)))
        else:
            log.fail("Not found keyword: %s in output"%(expected_result))
            show_unit_info(device)
            raise testFailed("test_execute_command: %s"%(test_cmd))

def copy_files_from_bmc_to_cpu(device, cpu_ip, filename, filepath, destination_path, size_MB,
                            swap=False, ipv6=False, interface='None'):
    log.debug('Entering procedure copy_files_from_bmc_to_cpu : %s\n'%(str(locals())))
    deviceObj = Device.getDeviceObject(device)
    username = deviceObj.rootUserName
    password = deviceObj.rootPassword
    mode = OPENBMC_MODE
    ### assume avg speed is 0.5MB/s
    timeout = int(size_MB) * 3
    filelist = [filename]
    CommonLib.copy_files_through_scp(device, username, password, cpu_ip, filelist, \
        filepath, destination_path, OPENBMC_MODE, True, True, interface, timeout)

def copy_files_through_tftp(device, server_device, filename):
    log.debug("Entering copy_files_through_tftp with args : %s" %(str(locals())))
    deviceObj = Device.getDeviceObject(device)
    serverObj = Device.getDeviceObject(server_device)
    ip = serverObj.managementIPV6
    CommonLib.exec_ping6(device, 'eth0', ip, 5, OPENBMC_MODE)
    cmd = 'tftp -gr %s %s'%(filename, ip)
    output = execute(deviceObj, cmd)
    p1 = r'(tftp:.*)'
    match = re.search(p1, output)
    if match:
        log.fail(match.group(1))
        show_unit_info(device)
        raise testFailed("Failed copy_files_through_tftp: %s"%(filename))
    else:
        log.success("Successfully copy_files_through_tftp: %s"%(filename))

def compare_binary_file(device, bin1, bin2):
    ### diff bin1 bin2
    log.debug('Entering procedure compare_binary_file with args : %s\n' %(str(locals())))
    deviceObj = Device.getDeviceObject(device)
    cmd = 'diff ' + bin1 + ' ' + bin2
    diff_msg = 'differ'
    err_msg = 'No such file or directory'
    output = execute(deviceObj, cmd)
    match = re.search(diff_msg, output)
    match_err = re.search(err_msg, output)
    if match:
        log.fail("Files %s and %s differ"%(bin1, bin2))
        log.fail("compare_binary_file")
        for re_cmd in re_run_oob_command_list:
            re_ouput = execute(deviceObj, re_cmd)
            if 'fail' in re_ouput:
                raise testFailed("Failed run %s"%re_cmd)
        compare_cmd = 'diff' + ' ' + bin1 + ' ' + bin2
        output = execute(deviceObj, compare_cmd)
        match = re.search(diff_msg, output)
        if match:
            log.fail("Files %s and %s differ" % (bin1, bin2))
            raise testFailed("compare_binary_file")
    elif match_err:
        log.fail("%s"%(err_msg))
        show_unit_info(device)
        raise testFailed("compare_binary_file")
    else:
        log.success("Successfully compare_binary_file: %s and %s matched"%(bin1, bin2))

def clean_up_file(device, files, mode=OPENBMC_MODE, isDir=False):
    ### rm dump1 dump2 dump3
    log.debug('Entering procedure clean_up_file with args : %s\n' %(str(locals())))
    deviceObj = Device.getDeviceObject(device)
    log.info("clean up file: %s"%(files))
    if isDir:
        cmd = 'rm -r ' + files
    else:
        cmd = 'rm -f ' + files
    execute(deviceObj, cmd, mode=mode)

def create_test_file(device, filename, size_MB):
    ## dd if=/dev/zero of=/mnt/data1/test bs=1M count=6000
    log.debug('Entering procedure create_test_file with args : %s\n' %(str(locals())))

    deviceObj = Device.getDeviceObject(device)
    timeout = 2400
    err_count = 0
    cmd = 'dd if=/dev/zero of=%s bs=1M count=%s'%(filename, size_MB)
    p1 = r'(.+) records in'
    p2 = r'(.+) records out'
    p3 = 'No such file or directory'
    output = execute(deviceObj, cmd, timeout=timeout)
    time.sleep(1)
    if parserOpenbmc.parse_simple_keyword(p1, output) != "" and \
       parserOpenbmc.parse_simple_keyword(p2, output) != "":
        log.success("Successfully create_test_file")
    elif re.search(p3, output) is not None:
        log.fail("%s"%(p3))
        err_count +=1
    else:
        log.fail("Unknown error")
        err_count += 1
    if err_count:
        show_unit_info(device)
        raise testFailed("create_test_file")

def switch_bmc_flash(device, bmc_flash):
    ### boot_info.sh bmc reset [master|slave]
    log.debug('Entering procedure switch_bmc_flash with args : %s\n' %(str(locals())))
    deviceObj = Device.getDeviceObject(device)
    cmd = "boot_info.sh bmc reset " + bmc_flash.lower()
    output = execute(deviceObj, cmd, timeout=20)
    p1 = 'BMC will switch to %s after (\d+) seconds'%(bmc_flash.lower())
    p2 = 'Current boot source is %s, no need to switch.'%(bmc_flash.lower())
    booting_msg = 'Starting kernel ...'
    match = re.search(p1, output)
    match2 = re.search(p2, output)
    if match:
        log.info("switch_bmc_flash to %s" %(bmc_flash.lower()))
        ### rebooting
        deviceObj.receive(booting_msg, timeout=120)
        time.sleep(120)
        deviceObj.getPrompt(OPENBMC_MODE, timeout=Const.BOOTING_TIME)
        verify_current_boot_flash(device, bmc_flash)
        ### when rebooting, need sleep 2 mins that prevent issues pop up  --Jeff
        time.sleep(120)
    elif match2:
        log.info("switch_bmc_flash to %s" %(bmc_flash.lower()))
        verify_current_boot_flash(device, bmc_flash)
    else:
        log.fail("switch_bmc_flash failed")
        show_unit_info(device)
        raise testFailed("switch_bmc_flash")

def switch_bios_flash(device, bios_flash):
    ### boot_info.sh bios reset [master|slave]
    log.debug('Entering procedure switch_bios_flash with args : %s\n' %(str(locals())))
    deviceObj = Device.getDeviceObject(device)
    deviceObj.getPrompt(OPENBMC_MODE)
    time.sleep(2)
    cmd = "boot_info.sh bios reset " + bios_flash.lower()
    p1 = 'Bridge-IC is initialized SCL to 1Mhz'
    p2 = 'Current boot source is %s, no need to switch.'%(bios_flash.lower())
    p3 = 'Power on microserver ... Done'
    p = p2 + '|' + p3
    try:
        output = execute(deviceObj, cmd)
        match = re.search(p3, output)
        match2 = re.search(p2, output)
        if match:
            log.info("switch_bios_flash to %s" % (bios_flash.lower()))
            # deviceObj.receive(p1)
            time.sleep(2)
            verify_bios_boot(device, switch_console_flag=True)
            verify_current_bios_flash(device, bios_flash)
        elif match2:
            log.info("switch_bios_flash to %s" % (bios_flash.lower()))
            verify_current_bios_flash(device, bios_flash)
    except:
        log.fail("switch_bios_flash failed")
        show_unit_info(device)
        raise testFailed("switch_bios_flash")

def check_eth_ports(device):
    log.debug('Entering procedure check_eth_ports with args : %s\n' %(str(locals())))
    deviceObj = Device.getDeviceObject(device)
    out = execute(deviceObj, 'ifconfig', timeout=10)
    if 'eth0' in out and 'lo' in out and 'usb0' in out:
        log.info("Successfully verify ethernet ports")
    else:
        log.error("Verify ethernet ports failed !")
        show_unit_info(device)
        raise RuntimeError("Verify ethernet ports failed!")

def verify_mac_address(device, interface, expected_result=None):
    ### ifconfig [interface]
    log.debug('Entering procedure verify_mac_address with args : %s\n' %(str(locals())))
    deviceObj = Device.getDeviceObject(device)
    err_count = 0
    cmd = 'ifconfig %s'%(interface)
    # p = r'HWaddr .* .*'
    p1 = r'(HWaddr|ether) (\S+)'
    try:
        output = execute(deviceObj, cmd)
        log.cprint(output)
        match = re.search(p1, output)
        if match:
            if expected_result != None:
                mac_addr = match.group(2).strip()
                if mac_addr.upper() == expected_result:
                    log.info("Successfully verify mac address: %s"%(mac_addr.upper()))
                else:
                    log.error("Mac address mismatch: %s, %s"%(mac_addr, expected_result))
                    err_count += 1
        else:
            log.error("Fail to parse mac adrress")
            err_count += 1
        if err_count:
            show_unit_info(device)
            raise RuntimeError('verify_mac_address')
    except:
        show_unit_info(device)
        raise RuntimeError('verify_mac_address')

def verify_ipv6_address(device, interface, expected_result, mode=OPENBMC_MODE):
    log.debug('Entering procedure verify_ipv6_address with args : %s\n' %(str(locals())))
    err_count = 0
    try:
        ipv6_addr_list = CommonLib.get_ip_address_list(device, interface, mode=mode, ipv6=True)
        if ipv6_addr_list:
            if expected_result in ipv6_addr_list:
                log.info("Successfully verify ipv6 address: %s"%(expected_result))
            else:
                log.error("ipv6 address %s mismatch in: %s"%(expected_result, ipv6_addr_list))
                err_count += 1
        else:
            log.error("Fail to parse ipv6 adrress")
            err_count += 1
        if err_count:
            show_unit_info(device)
            raise RuntimeError('verify_ipv6_address')
    except:
        raise RuntimeError('verify_ipv6_address')

def verify_dhcp_address(device, interface, ipv6=False, mode=OPENBMC_MODE):
    log.debug('Entering procedure verify_dhcp_address with args : %s\n' %(str(locals())))
    ip = CommonLib.get_ip_address(device, interface, mode, ipv6)
    if ip == '':
        log.fail("dhcp ip address does not set for %s"%(interface))
        show_unit_info(device)
        raise testFailed("verify_dhcp_address")
    else:
        log.success('Successfully get dhcp ip address for %s: %s'%(interface, ip))
        return ip

def verify_working_dir(device, path, mode):
    ### pwd
    log.debug('Entering procedure verify_working_dir with args : %s\n' %(str(locals())))
    deviceObj = Device.getDeviceObject(device)
    output = execute(deviceObj, "pwd", timeout=10, mode=mode)
    match = re.search(path, output)
    if match:
        log.success("Successfully verify_working_dir: %s"%(path))
    else:
        log.fail("verify_working_dir failed")
        show_unit_info(device)
        raise testFailed("verify_working_dir")

def check_file_exist_and_size(device, path, check_size_flag=False, expected_size='None', mode=None):
    log.debug('Entering procedure check_file_exist_and_size with args : %s\n' %(str(locals())))
    deviceObj = Device.getDeviceObject(device)
    err_count = 0
    if check_size_flag:
        cmd = "ls -la " + path + " | awk '{print $5}'"
    else:
        cmd = 'ls ' + path
    output = deviceObj.executeCmd(cmd, mode=mode)
    p1 = 'No such file or directory'
    match = re.search(p1, output)
    if match is None:
        log.success("%s exists"%(path))
        if check_size_flag:
            parsed_size = parserOpenbmc.parse_file_size(output)
            if expected_size == 'None':
                return parsed_size
            if parsed_size == expected_size:
                log.success("file size match: %s, %s"%(parsed_size, expected_size))
            else:
                log.fail("file size mismatch: %s, %s"%(parsed_size, expected_size))
                err_count += 1
    else:
        log.fail("%s does not exist"%(path))
        err_count += 1

    if err_count:
        show_unit_info(device)
        raise testFailed("check_file_exist_and_size")

def set_time_delay(seconds):
    log.debug('Entering procedure set_time_delay with args : %s\n' %(str(locals())))
    log.info('set time delay %s s'%(seconds))
    time.sleep(int(seconds))

def verify_no_cpu_prompt_return(device):
    log.debug('Entering procedure verify_no_cpu_prompt_return with args : %s\n' %(str(locals())))
    deviceObj = Device.getDeviceObject(device)
    p1 = '-----------------------------------------------------------'
    deviceObj.sendline("sol.sh")
    deviceObj.receive('CTRL-l + b : Send Break', timeout=10)
    deviceObj.read_until_regexp(p1, timeout=10)
    deviceObj.sendline("\r\n")
    time.sleep(1)
    deviceObj.sendline("\r\n")
    time.sleep(1)
    output = deviceObj.readMsg()
    log.debug("verify_no_cpu_prompt_return output: %s"%(output))
    match = re.search(deviceObj.promptDiagOS, output)
    if match:
        log.fail("Found promptDiagOS")
        show_unit_info(device)
        raise testFailed("verify_no_cpu_prompt_return")
    else:
        log.success("promptDiagOS does not appear")

def version_option_h(device, test_cmd, mode):
    log.debug('Entering version_option_h : %s\n' % (str(locals())))
    deviceObj = Device.getDeviceObject(device)
    output = execute(deviceObj, test_cmd, mode=mode)
    if 'error' in output.lower():
        log.fail('test version option h with error')
        show_unit_info(device)
        raise testFailed("test_execute_command: %s" % (test_cmd))
    elif 'fail' in output.lower():
        log.fail('test version option h with error')
        show_unit_info(device)
        raise testFailed("test_execute_command: %s" % (test_cmd))
    else:
        log.success('test version option h successful')

def check_disk_exist(device, disk_name, expected_size='None'):
    log.debug('Entering procedure check_disk_exist with args : %s\n' %(str(locals())))
    deviceObj = Device.getDeviceObject(device)
    err_count = 0
    cmd = 'fdisk -l'
    output = execute(deviceObj, cmd)
    parsed_size = parserOpenbmc.parse_disk_size(output, disk_name)
    if expected_size != 'None':
        if re.search(expected_size, parsed_size):
            log.success("Size match with expected: %s"%(parsed_size))
        else:
            log.fail("Size mismatch, found: %s, expected: %s"%(parsed_size, expected_size))
            err_count += 1
    else:
        if parsed_size != '':
            log.success("%s exist"%(disk_name))
        else:
            log.fail("%s does not exist"%(disk_name))
            err_count += 1
    if err_count:
        show_unit_info(device)
        raise testFailed("check_disk_exist")

def compare_util_and_eeprom(device, util_dict, eeprom_dict, map_key_dict=UTIL_EEPROM_MAP_KEY, flag='None'):
    log.debug('Entering procedure compare_util_and_eeprom with args : %s\n' %(str(locals())))
    outDict = parser()
    err_count = 0
    pimNum = 0
    log.info("##### changing util output to eeprom output format #####")
    pimNum = check_mp2_dc_pim(device)
    if pimNum == 5:
        if flag == 'pim3' or flag == 'pim4' or flag == 'pim5':
            return
    elif pimNum == 4:
        if flag == 'pim3' or flag == 'pim4' or flag == 'pim5' or flag == 'pim6':
            return
    for key, val in util_dict.items():
        if key in map_key_dict:
            mapping_key = map_key_dict[key]
        else:
            mapping_key = re.sub(r'\s|-', '_', key).lower()

        if mapping_key == 'product_name':
            outDict[mapping_key] = val
        elif mapping_key == 'format_version':
            outDict[mapping_key] = hex(int(val))
        elif mapping_key == 'system_manufacturing_date':
            outDict[mapping_key] = datetime.strptime(val, '%m-%d-%y').strftime('%Y%m%d')
        elif re.search(r'^N\/?-?A-?', val):
            outDict[mapping_key] = 'NA'
        else:
            outDict[mapping_key] = re.sub('-|:', '', val)
        outDict[mapping_key] = outDict[mapping_key].upper()
        log.info("%s: %s --> %s: %s"%(key, val, mapping_key, outDict[mapping_key]))

    ##### ignore 'magic_word in comparison #####
    if 'magic_word' in eeprom_dict:
        del eeprom_dict['magic_word']

    log.info("##### checking 'NA' format in eeprom output #####")
    for key, val in eeprom_dict.items():
        if re.search(r'^N\/?-?A-?', val) and val != 'NA':
            log.info("%s: %s --> %s: NA"%(key, val, key))
            eeprom_dict[key] = 'NA'
        eeprom_dict[key] = eeprom_dict[key].upper()

    log.info("##### comparing mapped util output with eeprom output #####")
    err_count += CommonLib.compare_input_dict_to_parsed(outDict, eeprom_dict, highlight_fail=True)
    if err_count:
        show_unit_info(device)
        raise testFailed("compare_util_and_eeprom")

def compare_sensor_threshold(sensor_dict, expected_dict):
    log.debug('Entering procedure compare_sensor_threshold : %s\n'%(str(locals())))
    fail_count = 0
    for key, value in zip(dict(expected_dict).keys(), expected_dict.values()):
        log.debug("Searching for %s = %s in parsed output" % (key, value))
        dict_value = sensor_dict.get(key)
        if dict_value is None:
            log.fail('For key = %s, Value %s not found in parsed output\n' %(key, value))
            fail_count += 1
        elif (isinstance(dict_value, (int,float)) and isinstance(value, (int,float))) \
             and (abs(value - dict_value) <= SensorCsv.ALLOW_DIFF):
            log.success('For key = %s, Values match %s, %s\n' %(str(key), str(value), str(dict_value)))
            continue
        elif isinstance(dict_value, str) and (dict_value == value):
            log.success('For key = %s, Values match %s, %s\n' %(key, value, dict_value))
            continue
        else:
            log.fail('For key = %s, Values do not match: Found \'%s\' Expected \'%s\'\n'
                        %(str(key), str(dict_value), str(value)))
            fail_count += 1
    return fail_count

def compare_sensor_info(sensor_dict, expected_dict, sensor_name):
    log.debug('Entering procedure compare_sensor_info : %s\n'%(str(locals())))
    err_count = 0
    SensorObj = SensorCsv()
    variance = SensorObj.VARIANCE
    ### compare unit
    sensor_unit = sensor_dict[SensorObj.UNIT]
    expected_unit = expected_dict[SensorObj.UNIT]
    if sensor_unit == expected_unit:
        log.success('sensor %s unit match %s, %s'%(sensor_name, sensor_unit, expected_unit))
    elif sensor_unit == SensorObj.NA_VALUE:
        log.fail('sensor %s unit is %s'%(sensor_name, sensor_unit))
        err_count += 1
    else:
        log.fail('sensor %s unit mismatch: found \'%s\', expected \'%s\''%(sensor_name, sensor_unit, expected_unit))
        err_count += 1

    ### compare value
    ### should be match value between 'LNC' and 'UNC'
    val = sensor_dict['value']
    s0_max = expected_dict[SensorObj.UNC]
    s0_min = expected_dict[SensorObj.LNC]
    s0_max_key = SensorObj.UNC
    s0_min_key = SensorObj.LNC
    if s0_max == SensorObj.NA_VALUE or s0_min == SensorObj.NA_VALUE:
        ### if 'LNC' or 'UNC' is NA, use 'HW Target Value under S0' instead
        ### parse 'HW Target Value under S0' from sensor spec dictionary (variance = 0.99 can be accepted)
        ### if 'HW Target Value under S0' is empty, will use 'LCR' and 'UCR' instead
        if SensorObj.THRESHOLD_S0 in expected_dict and expected_dict[SensorObj.THRESHOLD_S0] != '':
            value_s0 = expected_dict[SensorObj.THRESHOLD_S0]
            value_s0_list = value_s0.split('~')
            s0_max_key = SensorObj.THRESHOLD_S0
            s0_min_key = SensorObj.THRESHOLD_S0
            if len(value_s0_list) > 1:
                ### LCR~UCR, 0~15
                s0_min = expected_dict[SensorObj.LCR] if value_s0_list[0] == SensorObj.LCR else SensorObj.string_to_float(value_s0_list[0]) + variance
                s0_max = expected_dict[SensorObj.UCR] if value_s0_list[1] == SensorObj.UCR else SensorObj.string_to_float(value_s0_list[1]) + variance
            else:
                match = re.search(r'<(-?[0-9]*[0-9\.]+|UCR)', value_s0)
                match2 = re.search(r'>(-?[0-9]*[0-9\.]+|LCR)', value_s0)
                if match: ### <UCR, <16
                    s0_min = SensorObj.NA_VALUE
                    s0_max = expected_dict[SensorObj.UCR] if match.group(1) == SensorObj.UCR else SensorObj.string_to_float(match.group(1)) + variance
                elif match2: ### >LCR, >18.88, >0
                    s0_min = expected_dict[SensorObj.LCR] if match2.group(1) == SensorObj.LCR else SensorObj.string_to_float(match2.group(1)) + variance
                    s0_max = SensorObj.NA_VALUE
                elif value_s0 != SensorObj.NA_VALUE and value_s0 != 'N/A': ### 12
                    s0_min = SensorObj.NA_VALUE
                    s0_max = SensorObj.string_to_float(value_s0) + variance
                else: ### NA
                    s0_min = SensorObj.NA_VALUE
                    s0_max = SensorObj.NA_VALUE
        else:
            s0_min = expected_dict[SensorObj.LCR]
            s0_max = expected_dict[SensorObj.UCR]
            s0_min_key = SensorObj.LCR
            s0_max_key = SensorObj.UCR
    ### compare value from output and sensor spec
    if val != SensorObj.NA_VALUE:
        if s0_max != SensorObj.NA_VALUE and s0_max != 'N/A':
            if SensorObj.string_to_float(val) <= SensorObj.string_to_float(s0_max):
                log.success('sensor %s value: %s is in range %s: %s'%(sensor_name, val, s0_max_key, s0_max))
            else:
                log.fail('sensor %s value: %s is over than %s: %s'%(sensor_name, val, s0_max_key, s0_max))
                err_count += 1
        if s0_min != SensorObj.NA_VALUE:
            if SensorObj.string_to_float(val) >= SensorObj.string_to_float(s0_min):
                log.success('sensor %s value: %s is in range %s: %s'%(sensor_name, val, s0_min_key, s0_min))
            else:
                log.fail('sensor %s value: %s is lower than %s: %s'%(sensor_name, val, s0_min_key, s0_min))
                err_count += 1
    else:
        log.fail('sensor %s value is %s'%(sensor_name, val))
        err_count += 1

    ### compare status
    status = sensor_dict['status']
    if status == SENSOR_OK:
        log.success('sensor %s status is %s'%(sensor_name, status))
    else:
        log.fail('sensor %s status is %s'%(sensor_name, status))
        err_count += 1
    return err_count

def check_cpu_alive(device, need_cd=False, path='/etc'):
    log.debug('Entering procedure check_cpu_alive : %s\n'%(str(locals())))
    deviceObj = Device.getDeviceObject(device)
    deviceObj.getPrompt(CENTOS_MODE)
    if need_cd:
        CommonLib.change_dir(path, CENTOS_MODE)
    verify_working_dir(device, path, CENTOS_MODE)
    deviceObj.getPrompt(OPENBMC_MODE)


def get_version_from_config(image_type, isNewVersion=True):
    log.debug('Entering procedure get_version_from_config : %s\n'%(str(locals())))
    imageObj = SwImage.getSwImage(image_type.upper())
    if imageObj.isAutoBuild:
        imageObj.refreshImageInfo()

    image_version = {}
    image_version[image_type + ' Version'] = imageObj.newVersion if isNewVersion else imageObj.oldVersion
    if image_type == 'CPLD':
        image_version = image_version[image_type + ' Version']
        if 'fcm' in image_version:
            image_version['FCMCPLD'] = image_version.pop('fcm')
        if 'scm' in image_version:
            image_version['SCMCPLD'] = image_version.pop('scm')
        if 'smb' in image_version:
            image_version[SMB_CPLD_KEY] = image_version.pop('smb')
        if 'pwr' in image_version:
            image_version[PWR_CPLD_KEY] = image_version.pop('pwr')
    elif image_type in ['SCM', 'TH3', 'TH4_PCIE_FLASH']:
        image_version = image_version[image_type + ' Version']
    elif image_type == 'BIC':
        image_version['Bridge-IC Version'] = image_version.pop(image_type + ' Version')
    elif image_type == 'PSU':
        image_version = image_version[image_type + ' Version']
        if 'PRI_FW_VER' in image_version:
            image_version[PRI_FW_VER_KEY] = image_version.pop('PRI_FW_VER')
        if 'SEC_FW_VER' in image_version:
            image_version[SEC_FW_VER_KEY] = image_version.pop('SEC_FW_VER')
    elif image_type == 'FPGA':
        image_version = image_version[image_type + ' Version']
        if IOB_FPGA_DIAG_KEY in image_version:
            image_version[IOB_FPGA_KEY] = image_version.pop(IOB_FPGA_DIAG_KEY)
    log.info(image_version)
    return image_version

def create_random_mac_address(device, prompt):
    log.debug('Entering procedure create_random_mac_address with args : %s\n' %(str(locals())))
    deviceObj = Device.getDeviceObject(device)
    Maclist = ['A', 'A']
    for i in range(1,6):
        RANDSTR = "".join(random.sample("0123456789ABCDEF",2))
        Maclist.append(RANDSTR)
    if prompt == 'format_with_separator':
        RANDMAC = ":".join(Maclist)
        return RANDMAC
    elif prompt == 'format_without_separator':
        RANDMAC = "".join(Maclist)
        return RANDMAC
    else:
        log.fail("create_random_mac_address FAIL")
        show_unit_info(device)
        raise testFailed("create_random_mac_address FAIL")

def modify_eeprom_cfg_string(device, original, modified):
    log.debug('Entering procedure modify_eeprom_cfg with args : %s\n' %(str(locals())))
    deviceObj = Device.getDeviceObject(device)
    err_count = 0
    cmd = "sed -i 's/%s/%s/' eeprom.cfg"%(original, modified)
    output = execute(deviceObj, cmd)
    p1 = "No such file or directory"
    time.sleep(1)
    match = re.search(p1, output)
    if match:
        log.fail("%s" %(match.group(0)))
        err_count += 1
    else:
        log.success("modify eeprom.cfg_string '%s' = '%s'"%(original, modified))
    if err_count:
        show_unit_info(device)
        raise testFailed("modify eeprom.cfg_string failed")

def get_eeprom_value(device, cmd, key):
    log.debug('Entering procedure get_eeprom_value : %s\n'%(str(locals())))
    deviceObj = Device.getDeviceObject(device)
    output = execute(deviceObj, cmd)
    time.sleep(1)
    parsed_output = parserOpenbmc.parse_eeprom(output)
    value = parsed_output[key]
    if value:
        log.success("Successfully get_eeprom_value")
        return value
    else:
        show_unit_info(device)
        raise testFailed("get_eeprom_value")

def change_mac_fomat(device, original):
    log.debug('Entering procedure change_mac_fomat : %s\n'%(str(locals())))
    deviceObj = Device.getDeviceObject(device)
    string = original
    pattern = re.compile('.{2}')
    string_final = (':'.join(pattern.findall(string)))
    return string_final

def get_mac_address(device, prompt, interface):
    log.debug('Entering procedure get_mac_address with args : %s\n' %(str(locals())))
    deviceObj = Device.getDeviceObject(device)
    cmd = 'ifconfig %s'%(interface)
    # p = r'HWaddr .* .*'
    p1 = r'(HWaddr|ether) (\S+)'
    # p2 = r'ether .* .*'
    p3 = r'ether (\S+)'
    if prompt == 'openbmc' :
        output = execute(deviceObj, cmd)
        log.cprint(output)
        match = re.search(p1, output)
        if match:
            mac_addr = match.group(2).strip()
            return mac_addr.upper()
            log.info("Successfully get mac address: %s"%(mac_addr.upper()))
        else:
            show_unit_info(device)
            raise testFailed('get mac address FAIL')
    if prompt == 'centos' :
        output = execute(deviceObj, cmd)
        log.cprint(output)
        match = re.search(p3, output)
        if match:
            mac_addr = match.group(1).strip()
            return mac_addr.upper()
            log.info("Successfully get mac address: %s"%(mac_addr.upper()))
        else:
            show_unit_info(device)
            raise testFailed('get mac address FAIL')
    else:
        show_unit_info(device)
        raise RuntimeError('get_mac_address FAIL')

#######################################################################################################################
# Function Name: need_update_cpld
# Date         : 30th June 2020
# Author       : James Shi <jameshi@celestica.com>
#
# Procedure Revision Details:
#   Version : 1.0  - Initial Draft  - by James Shi <jameshi@celestica.com>
#######################################################################################################################
def need_update_cpld(device, CPLD_version, cpld_type):
    log.debug('Entering procedure need_update_cpld with args : %s\n' %(str(locals())))
    deviceObj = Device.getDeviceObject(device)
    # cmd = 'cpld_ver.sh'
    err_count  = 0
    output = execute(deviceObj, CPLD_VER_CMD)
    parsed_output = parserOpenbmc.parse_fw_version(output)
    if cpld_type == 'fcm' :
        cpld_type_2 = 'FCMCPLD'
    elif cpld_type == 'scm' :
        cpld_type_2 = 'SCMCPLD'
    elif cpld_type == 'smb' :
        cpld_type_2 = SMB_CPLD_KEY
    elif cpld_type == 'pwr' :
        cpld_type_2 = PWR_CPLD_KEY
    elif cpld_type.lower() == 'fcm-t' :
        cpld_type_2 = 'FCMCPLD T'
    elif cpld_type.lower() == 'fcm-b' :
        cpld_type_2 = 'FCMCPLD B'
    elif cpld_type.lower() == 'pwr-l' :
        cpld_type_2 = 'PWRCPLD L'
    elif cpld_type.lower() == 'pwr-r' :
        cpld_type_2 = 'PWRCPLD R'
    if parsed_output[cpld_type_2] != CPLD_version[cpld_type_2]:
        err_count += 1
        log.info("need to update %s" %(cpld_type))
    else:
        log.info("no need to update %s" %(cpld_type))
    return True if err_count > 0 else False

#######################################################################################################################
# Function Name: update_cpld
# Date         : 30th June 2020
# Author       : James Shi <jameshi@celestica.com>
#
# Procedure Revision Details:
#   Version : 1.0  - Initial Draft  - by James Shi <jameshi@celestica.com>
#######################################################################################################################
def update_cpld(device, update_mode, isUpgrade = True):
    log.debug('Entering procedure update_cpld with args : %s\n' %(str(locals())))
    update_count = 0
    check_cpu_alive(device, need_cd=True)
    CPLD_version = get_version_from_config(SwImage.CPLD, isNewVersion=isUpgrade)
    cpld_type = 'fcm'
    if need_update_cpld(device, CPLD_version, cpld_type):
        log.debug('Entering procedure update_cpld_fcm')
        online_update_cpld(device, isUpgrade, cpld_type, update_mode)
        update_count += 1
    cpld_type = 'scm'
    if need_update_cpld(device, CPLD_version, cpld_type):
        log.debug('Entering procedure update_cpld_scm')
        online_update_cpld(device, isUpgrade, cpld_type, update_mode)
        update_count += 1
    cpld_type = 'smb'
    if need_update_cpld(device, CPLD_version, cpld_type):
        log.debug('Entering procedure update_cpld_smb')
        online_update_cpld(device, isUpgrade, cpld_type, update_mode)
        update_count += 1
    cpld_type = 'pwr'
    if need_update_cpld(device, CPLD_version, cpld_type):
        log.debug('Entering procedure update_cpld_pwr')
        online_update_cpld(device, isUpgrade, cpld_type, update_mode)
        update_count += 1
    if update_count > 0:
        verify_fw_version(device, SwImage.CPLD, CPLD_version, get_flag=True)
        check_cpu_alive(device)
        reset_power_chassis(device)
        verify_fw_version(device, SwImage.CPLD, CPLD_version)

#######################################################################################################################
# Function Name: update_cpld_minipack2
# Date         : 29th September 2020
# Author       : Prapatsorn W. <pwisutti@celestica.com>
#
# Procedure Revision Details:
#   Version : 1.0  - Initial Draft  - by Prapatsorn W. <pwisutti@celestica.com>
#######################################################################################################################
def update_cpld_minipack2(device, isUpgrade=True):
    log.debug('Entering procedure update_cpld_minipack2 with args : %s\n' %(str(locals())))
    update_mode = 'sw'
    pwr_mode = 'i2c'
    update_count = 0
    check_cpu_alive(device, need_cd=True)
    CPLD_version = get_version_from_config(SwImage.CPLD, isNewVersion=isUpgrade)
    cpld_type = 'fcm-t'
    if need_update_cpld(device, CPLD_version, cpld_type):
        log.debug('need to update cpld %s'%(cpld_type))
        online_update_cpld(device, isUpgrade, cpld_type, update_mode)
        update_count += 1
    cpld_type = 'fcm-b'
    if need_update_cpld(device, CPLD_version, cpld_type):
        log.debug('need to update cpld %s'%(cpld_type))
        online_update_cpld(device, isUpgrade, cpld_type, update_mode)
        update_count += 1
    cpld_type = 'scm'
    if need_update_cpld(device, CPLD_version, cpld_type):
        log.debug('need to update cpld %s'%(cpld_type))
        online_update_cpld(device, isUpgrade, cpld_type, update_mode)
        update_count += 1
    cpld_type = 'smb'
    if need_update_cpld(device, CPLD_version, cpld_type):
        log.debug('need to update cpld %s'%(cpld_type))
        online_update_cpld(device, isUpgrade, cpld_type, update_mode)
        update_count += 1
    ### temporary disable because of pwr-l and pwr-r cpld updating takes long time issue
    cpld_type = 'pwr-l'
    if need_update_cpld(device, CPLD_version, cpld_type):
        log.debug('need to update cpld %s'%(cpld_type))
        online_update_cpld(device, isUpgrade, cpld_type, pwr_mode)
        update_count += 1
    cpld_type = 'pwr-r'
    if need_update_cpld(device, CPLD_version, cpld_type):
        log.debug('need to update cpld %s'%(cpld_type))
        online_update_cpld(device, isUpgrade, cpld_type, pwr_mode)
        update_count += 1
    if update_count > 0:
        verify_fw_version(device, SwImage.CPLD, CPLD_version, get_flag=True)
        check_cpu_alive(device)
        reset_power_chassis(device)
        verify_fw_version(device, SwImage.CPLD, CPLD_version)

#######################################################################################################################
# Function Name: online_update_cpld
# Date         : 30th June 2020
# Author       : James Shi <jameshi@celestica.com>
#
# Procedure Revision Details:
#   Version : 1.0  - Initial Draft  - by James Shi <jameshi@celestica.com>
#######################################################################################################################
def online_update_cpld(device, isUpgrade, cpld_type_1, update_mode):
    ### time scmcpld_update.sh /mnt/data1/CPLD/WEDGE400_SCM_CPLD_v4p0.jed hw
    log.debug('Entering procedure online_update_cpld with args : %s\n' %(str(locals())))
    deviceObj = Device.getDeviceObject(device)
    imageObj = SwImage.getSwImage(SwImage.CPLD)
    package_file = imageObj.newImage if isUpgrade else imageObj.oldImage
    package_file_path = imageObj.localImageDir
    if cpld_type_1.lower() == 'fcm':
        cmd = '%s %s/%s %s'%(FCM_CPLD_UPDATE_CMD, package_file_path, package_file['fcm'], update_mode)
    elif cpld_type_1.lower() == 'scm':
        cmd = '%s %s/%s %s'%(SCM_CPLD_UPDATE_CMD, package_file_path, package_file['scm'], update_mode)
    elif cpld_type_1.lower() == 'smb':
        cmd = '%s %s/%s %s'%(SMB_CPLD_UPDATE_CMD, package_file_path, package_file['smb'], update_mode)
    elif cpld_type_1.lower() == 'pwr':
        cmd = '%s %s/%s %s'%(PWR_CPLD_UPDATE_CMD, package_file_path, package_file['pwr'], update_mode)
    elif cpld_type_1.lower() == 'fcm-t':
        cmd = '%s %s/%s %s'%(FCM_T_CPLD_UPDATE_CMD, package_file_path, package_file['fcm'], update_mode)
    elif cpld_type_1.lower() == 'fcm-b':
        cmd = '%s %s/%s %s'%(FCM_B_CPLD_UPDATE_CMD, package_file_path, package_file['fcm'], update_mode)
    elif cpld_type_1.lower() == 'pwr-l':
        cmd = '%s %s/%s %s'%(PWR_L_CPLD_UPDATE_CMD, package_file_path, package_file['pwr'], update_mode)
    elif cpld_type_1.lower() == 'pwr-r':
        cmd = '%s %s/%s %s'%(PWR_R_CPLD_UPDATE_CMD, package_file_path, package_file['pwr'], update_mode)
    output = 'default_none'
    pass_message = 'PASS!|Upgrade successful'
    timeout = 1000
    try:
        log.cprint(cmd)
        output = execute(deviceObj, cmd, timeout=timeout)
        match = re.search(pass_message, output)
        if match:
            log.success("Successfully online_update_cpld %s" %(cpld_type_1))
            if "cloudripper" in deviceObj.name:
            ### set sleep 2 mins prevent issues pop up only on cloudripper ---Jeff
                time.sleep(120)
        else:
            log.fail("online_update_cpld_%s failed" %(cpld_type_1))
            show_unit_info(device)
            raise testFailed("online_update_cpld_%s" %(cpld_type_1))
    except:
        log.cprint(output)
        log.error("online_update_cpld_%s failed" %(cpld_type_1))
        show_unit_info(device)
        raise RuntimeError("online_update_cpld_%s" %(cpld_type_1))

#############################################################################################
# Function Name: get_board_type_rev
# Date         : 30th June 2020
# Author       : Prapatsorn W. <pwisutti@celestica.com>
#
# Procedure Revision Details:
#   Version : 1.0  - Initial Draft  - by Prapatsorn W. <pwisutti@celestica.com>
#############################################################################################
def get_board_type_rev(device):
    log.debug('Entering procedure get_board_type_rev with args : %s\n' %(str(locals())))
    deviceObj = Device.getDeviceObject(device)
    ### source /usr/local/bin/openbmc-utils.sh
    ### wedge_board_type_rev
    execute(deviceObj, "source /usr/local/bin/openbmc-utils.sh")
    output = execute(deviceObj, "wedge_board_type_rev")
    parsed_output = parserOpenbmc.parse_board_type_rev(output)
    return parsed_output

#############################################################################################
# Function Name: get_gpio_brd_rev0_by_board_type
# Date         : 30th June 2020
# Author       : Prapatsorn W. <pwisutti@celestica.com>
#
# Procedure Revision Details:
#   Version : 1.0  - Initial Draft  - by Prapatsorn W. <pwisutti@celestica.com>
#############################################################################################
def get_gpio_brd_rev0_by_board_type(device):
    log.debug('Entering procedure get_gpio_brd_rev0_by_board_type with args : %s\n' %(str(locals())))
    gpio_brd_rev0 = 0
    brd_type_dict = get_board_type_rev(device)
    if brd_type_dict:
        phase = brd_type_dict['phase']
        if brd_type_dict['project'] == 'WEDGE400':
            if phase in ['EVT', 'EVT3', 'DVT']:
                gpio_brd_rev0 = 0
            elif phase in ['DVT2', 'PVT1', 'PVT2', 'PVT3', 'MP', 'DVT2/PVT1/PV2', 'DVT2/PVT1/PV2 (With SCM_RESPIN)']:
                gpio_brd_rev0 = 1
        elif brd_type_dict['project'] == 'WEDGE400C':
            if phase in ['EVT', 'DVT', 'DVT (With SCM_RESPIN)']:
                gpio_brd_rev0 = 0
            elif phase in ['EVT2', 'PVT3', 'DVT2']:
                gpio_brd_rev0 = 1
        else:
            log.info("project type not support")
    return str(gpio_brd_rev0)

#############################################################################################
# Function Name: get_brd_id_by_board_type
# Date         : 13rd July 2020
# Author       : Prapatsorn W. <pwisutti@celestica.com>
#
# Procedure Revision Details:
#   Version : 1.0  - Initial Draft  - by Prapatsorn W. <pwisutti@celestica.com>
#############################################################################################
def get_brd_id_by_board_type(device):
    log.debug('Entering procedure get_brd_id_by_board_type with args : %s\n' %(str(locals())))
    board_rev_id = '01'
    brd_type_dict = get_board_type_rev(device)
    if brd_type_dict:
        phase = brd_type_dict['phase']
        if brd_type_dict['project'] == 'WEDGE400C':
            if phase in ['EVT2']:
                board_rev_id = '01'
            elif phase in ['DVT', 'DVT (With SCM_RESPIN)']:
                board_rev_id = '02'
            elif phase in ['DVT2']:
                board_rev_id = '03'
        elif brd_type_dict['project'] == 'WEDGE400C_MP':
            if phase in ['RESPIN']:
                board_rev_id = '04'
        elif brd_type_dict['project'] == 'Cloudripper':
            if phase in ['EVT3']:
                board_rev_id = '02'
            elif phase in ['DVT']:
                board_rev_id = '03'
            else:
                board_rev_id = '00'
        elif brd_type_dict['project'] == 'WEDGE400_MP':
            if phase in ['RESPIN']:
                board_rev_id = '06'
        elif brd_type_dict['project'] == 'WEDGE400':
            if phase in ['MP']:
                board_rev_id = '05'
            elif phase in ['DVT2/PVT1/PV2', 'DVT2/PVT1/PV2 (With SCM_RESPIN)']:
                board_rev_id = '03'
    return board_rev_id

#############################################################################################
# Function Name: run_enable_mdio
# Date         : 1st July 2020
# Author       : Prapatsorn W. <pwisutti@celestica.com>
#
# Procedure Revision Details:
#   Version : 1.0  - Initial Draft  - by Prapatsorn W. <pwisutti@celestica.com>
#############################################################################################
def run_enable_mdio(device):
    log.debug('Entering procedure run_enable_mdio with args : %s\n' %(str(locals())))
    deviceObj = Device.getDeviceObject(device)
    execute(deviceObj, "source /usr/local/bin/openbmc-utils.sh")
    execute(deviceObj, "devmem_set_bit 0x1e6e2088 31")
    time.sleep(1)
    execute(deviceObj, "devmem_set_bit 0x1e6e2088 30")
    time.sleep(1)
    execute(deviceObj, "devmem_set_bit 0x1e6e2088 2")
    time.sleep(1)
    execute(deviceObj, "devmem_clear_bit 0x1e6e200c 21")
    time.sleep(1)
    execute(deviceObj, "devmem_clear_bit 0x1e6e200c 20")
    time.sleep(1)
    cmd = 'ifconfig eth0 down'
    execute(deviceObj, cmd)
    time.sleep(1)

#############################################################################################
# Function Name: read_mdio
# Date         : 1st July 2020
# Author       : Prapatsorn W. <pwisutti@celestica.com>
#
# Procedure Revision Details:
#   Version : 1.0  - Initial Draft  - by Prapatsorn W. <pwisutti@celestica.com>
#############################################################################################
def read_mdio(device, reg, expected_val):
    log.debug('Entering procedure read_mdio with args : %s\n' %(str(locals())))
    deviceObj = Device.getDeviceObject(device)
    ### ast-mdio.py --mac 1 --phy 0xe read 0
    if 'rsp' in deviceObj.name or 'dc' in deviceObj.name:
        log.info('It is respin unit, pls skip!!!')
    else:
        cmd = "ast-mdio.py --mac 1 --phy %s read 0"%(reg)
        output = execute(deviceObj, cmd)
        parsed_val = parserOpenbmc.parse_read_write_mdio(output)
        if parsed_val != "" and int(parsed_val, 16) == int(expected_val, 16):
            log.success("Successfully read mdio, values match '%s', '%s'"%(parsed_val, expected_val))
        else:
            log.fail("read mdio value mismatch, found '%s', expected '%s'"%(parsed_val, expected_val))
            show_unit_info(device)
            raise testFailed('read mdio FAIL')

def read_mdio_rsp(device, mac_num, reg, read_value, expected_val):
    log.debug('Entering procedure read_mdio_rsp with args : %s\n' %(str(locals())))
    deviceObj = Device.getDeviceObject(device)
    ### ast-mdio.py --mac 2 --phy 0x0 read 2
    if 'rsp' in deviceObj.name or 'dc' in deviceObj.name:
        cmd = "ast-mdio.py --mac %s --phy %s read %s"%(mac_num, reg, read_value)
        output = execute(deviceObj, cmd)
        parsed_val = parserOpenbmc.parse_read_write_mdio(output)
        if parsed_val != "" and int(parsed_val, 16) == int(expected_val, 16):
            log.success("Successfully read mdio, values match '%s', '%s'"%(parsed_val, expected_val))
        else:
            log.fail("read mdio value mismatch, found '%s', expected '%s'"%(parsed_val, expected_val))
            show_unit_info(device)
            raise testFailed('read mdio FAIL')
    else:
        log.info('It only supports respin unit!')

#############################################################################################
# Function Name: write_mdio
# Date         : 1st July 2020
# Author       : Prapatsorn W. <pwisutti@celestica.com>
#
# Procedure Revision Details:
#   Version : 1.0  - Initial Draft  - by Prapatsorn W. <pwisutti@celestica.com>
#############################################################################################
def write_mdio(device, reg, val):
    log.debug('Entering procedure write_mdio with args : %s\n' %(str(locals())))
    deviceObj = Device.getDeviceObject(device)
    ### ast-mdio.py --mac 1 --phy 0xe write 0x00 0x00
    if 'rsp' in deviceObj.name or 'dc' in deviceObj.name:
        log.info('It is respin unit, pls skip!!!')
    else:
        cmd = "ast-mdio.py --mac 1 --phy %s write 0x00 %s"%(reg, val)
        output = execute(deviceObj, cmd)
        parsed_val = parserOpenbmc.parse_read_write_mdio(output)
        if parsed_val != "" and int(parsed_val, 16) == int(val, 16):
            log.success("Successfully write mdio, values match '%s', '%s'"%(parsed_val, val))
        else:
            log.fail("write mdio value mismatch, found '%s', expected '%s'"%(parsed_val, val))
            show_unit_info(device)
            raise testFailed('write mdio FAIL')

def write_mdio_rsp(device, mac_num, reg, value1, value2, val):
    log.debug('Entering procedure write_mdio_rsp with args : %s\n' %(str(locals())))
    deviceObj = Device.getDeviceObject(device)
    ### ast-mdio.py --mac 2 --phy 0x0 write 0x02 0x00
    if 'rsp' in deviceObj.name or 'dc' in deviceObj.name:
        cmd = "ast-mdio.py --mac %s --phy %s write %s %s" % (mac_num, reg, value1, value2)
        output = execute(deviceObj, cmd)
        parsed_val = parserOpenbmc.parse_read_write_mdio(output)
        if parsed_val != "" and int(parsed_val, 16) == int(val, 16):
            log.success("Successfully write mdio, values match '%s', '%s'" % (parsed_val, val))
        else:
            log.fail("write mdio value mismatch, found '%s', expected '%s'" % (parsed_val, val))
            show_unit_info(device)
            raise testFailed('write mdio FAIL')
    else:
        log.info('It only supports respin unit!')

def set_eth0_status(device, tool):
    log.debug('Entering procedure write_mdio_rsp with args : %s\n' % (str(locals())))
    deviceObj = Device.getDeviceObject(device)
    cmd = 'ifconfig eth0 %s' % (tool)
    deviceObj.sendline(cmd)
    time.sleep(6)
    deviceObj.getPrompt(OPENBMC_MODE, timeout=Const.BOOTING_TIME)

#############################################################################################
# Function Name: untar_file
# Date         : 1st July 2020
# Author       : Prapatsorn W. <pwisutti@celestica.com>
#
# Procedure Revision Details:
#   Version : 1.0  - Initial Draft  - by Prapatsorn W. <pwisutti@celestica.com>
#############################################################################################
def untar_file(device, imageName, pass_keyword='None'):
    log.debug('Entering procedure untar_file with args : %s\n' %(str(locals())))
    deviceObj = Device.getDeviceObject(device)
    imageObj = SwImage.getSwImage(imageName)
    images = imageObj.getImageList()
    err_count = 0
    dir_name = ''
    ### tar -xvf filename
    for fileName in images:
        if '.tar' in fileName:
            cmd = "tar -xvf %s/%s"%(imageObj.localImageDir, fileName)
        elif '.zip' in fileName:
            cmd = "unzip %s/%s"%(imageObj.localImageDir, fileName)
        output = execute(deviceObj, cmd, timeout=300)
        p1 = 'No such file or directory'
        match = re.search(p1, output)
        if match:
            log.fail("%s"%(p1))
            err_count += 1
        else:
            if '.tar' in fileName:
                dir_name = parserOpenbmc.parse_dir_from_untar(output)
            elif '.zip' in fileName:
                dir_name = fileName.split('.')[0]
            log.success('Successfully untar file %s/%s'%(imageObj.localImageDir, fileName))
            if pass_keyword != 'None':
                if parserOpenbmc.parse_simple_keyword(pass_keyword, output) == '':
                    err_count += 1
    if err_count:
        show_unit_info(device)
        raise testFailed('untar_file')
    return dir_name

#############################################################################################
# Function Name: run_tpm_test_all
# Date         : 1st July 2020
# Author       : Prapatsorn W. <pwisutti@celestica.com>
#
# Procedure Revision Details:
#   Version : 1.0  - Initial Draft  - by Prapatsorn W. <pwisutti@celestica.com>
#############################################################################################
def run_tpm_test_all(device, tpm_dir, pass_keyword, expected_result):
    log.debug('Entering procedure run_tpm_test_all with args : %s\n' %(str(locals())))
    deviceObj = Device.getDeviceObject(device)
    err_count = 0
    perssion_cmd = 'chmod -R 777 ' + tpm_dir
    deviceObj.transmit(perssion_cmd)
    CommonLib.change_dir(tpm_dir)
    cmd = './test_all.sh'
    timeout = 7200
    try:
        output = execute(deviceObj, cmd, timeout=timeout)
    except:
        log.fail("run_tpm_test_all exceed timeout %d minutes"%(timeout/60))
        show_unit_info(device)
        raise testFailed('run_tpm_test_all')
    if parserOpenbmc.parse_simple_keyword(pass_keyword, output) == '':
        err_count += 1
    parsed_output = parserOpenbmc.parse_tpm_result(output)
    err_count += CommonLib.compare_input_dict_to_parsed(parsed_output, expected_result)
    CommonLib.change_dir()
    if err_count:
        show_unit_info(device)
        raise testFailed('run_tpm_test_all')

#############################################################################################
# Function Name: prepare_tpm_test
# Date         : 21th September 2020
# Author       : Prapatsorn W. <pwisutti@celestica.com>
#
# Procedure Revision Details:
#   Version : 1.0  - Initial Draft  - by Prapatsorn W. <pwisutti@celestica.com>
#############################################################################################
def prepare_tpm_test(device):
    log.debug('Entering procedure prepare_tpm_test with args : %s\n' %(str(locals())))
    deviceObj = Device.getDeviceObject(device)
    if 'minipack2' in deviceObj.name or 'cloudripper' in deviceObj.name:
        ### need to check /dev/tpmrm1
        output = execute(deviceObj, CHECK_TPM_PATH_CMD)
        match =  re.search(TPMRM1_PATH, output)
        if match:
            log.info("Found: %s"%(TPMRM1_PATH))
            tpmrm_path = TPMRM1_PATH
        else:
            log.info("Not found: %s, use %s"%(TPMRM1_PATH, TPMRM0_PATH))
            tpmrm_path = TPMRM0_PATH
    else:
        tpmrm_path = TPMRM0_PATH
    execute(deviceObj, 'export TPM2TOOLS_TCTI_NAME=device')
    execute(deviceObj, 'export TPM2TOOLS_DEVICE_FILE=%s'%(tpmrm_path))

################################################################################
# Function Name: check_cmd_output_message
# Date         : 9th July 2020
# Author       : James Shi <jameshi@celestica.com>
#
# Procedure Revision Details:
#   Version : 1.0  - Initial Draft  - by James Shi <jameshi@celestica.com>
################################################################################
def check_cmd_output_message(device, cmd, messages_list):
    log.debug('Entering procedure check_cmd_output_message with args : %s\n' %(str(locals())))
    deviceObj = Device.getDeviceObject(device)
    output = execute(deviceObj, cmd, timeout=300)
    err_count = 0
    if (('rsp' in deviceObj.name) or ('dc' in deviceObj.name)) and 'dev' in cmd:
        messages_list = "ttyUSB1,ttyUSB2,ttyUSB3"
    messages_list_1 = messages_list.split(",")
    for msg in messages_list_1:
        if parserOpenbmc.parse_simple_keyword(msg, output) == "":
            err_count += 1
    if err_count == 0:
        log.success("Successfully check '%s' output message" %cmd)
    else:
        log.fail("check_%s_output_message fail" %cmd)
        show_unit_info(device)
        raise testFailed("check '%s' output message fail" %cmd)

#############################################################################################
# Function Name: check_psu_power_on
# Date         : 8th July 2020
# Author       : Prapatsorn W. <pwisutti@celestica.com>
#
# Procedure Revision Details:
#   Version : 1.0  - Initial Draft  - by Prapatsorn W. <pwisutti@celestica.com>
#############################################################################################
def check_psu_power_on(device, this_psu='None'):
    log.debug('Entering procedure check_psu_power_on with args : %s\n' %(str(locals())))
    isPlug_psu = 0
    for i in range(1, PSU_NUM + 1):
        psu_name = "psu%d"%(i)
        log.info("Check %s status"%(psu_name))
        psu_sensor = verify_sensor_util(device, psu_name)
        if psu_sensor is None:
            log.info("%s does not present, the test will not update fw"%(psu_sensor))
            return False
        is_zero_value = all(psu_sensor[key]['value'] == '0.00' for key in psu_sensor.keys())
        if psu_name == this_psu:
            isPlug_this_psu = not is_zero_value
            log.info('This psu (%s) is %s'%(this_psu, ('plugged' if isPlug_this_psu else 'unplugged')))
            if not isPlug_this_psu:
                log.info("the test will not update fw")
                return False
        isPlug_psu += not is_zero_value
    log.info('Plugged PSUs/All PSUs: %d/%d'%(isPlug_psu, PSU_NUM))
    if isPlug_psu > 1:
        log.info("this PSU power on and other PSUs power on at least two, continue update fw")
        return True
    else:
        log.info("PSUs does not power on at least two, the test will not update fw")
        return False

def check_dc_psu_power_on(device, this_psu='None'):
    log.debug('Entering procedure check_dc_psu_power_on with args : %s\n' %(str(locals())))
    deviceObj = Device.getDeviceObject(device)
    isPlug_psu = 0
    if 'minipack2_dc' in deviceObj.name:
        for i in range(3, PSU_NUM_DC + 3):
            psu_name = "psu%d" % (i)
            log.info("Check %s status" % (psu_name))
            psu_sensor = verify_sensor_util(device, psu_name)
            if psu_sensor is None:
                log.info("%s does not present, the test will not update fw" % (psu_sensor))
                return False
            is_zero_value = all(psu_sensor[key]['value'] == '0.00' for key in psu_sensor.keys())
            if psu_name == this_psu:
                isPlug_this_psu = not is_zero_value
                log.info('This psu (%s) is %s' % (this_psu, ('plugged' if isPlug_this_psu else 'unplugged')))
                if not isPlug_this_psu:
                    log.info("the test will not update fw")
                    return False
            isPlug_psu += not is_zero_value
    elif 'wedge400_dc' in deviceObj.name or 'wedge400c_dc' in deviceObj.name:
        for i in range(2, PSU_NUM_DC + 2):
            psu_name = "psu%d"%(i)
            log.info("Check %s status"%(psu_name))
            psu_sensor = verify_sensor_util(device, psu_name)
            if psu_sensor is None:
                log.info("%s does not present, the test will not update fw"%(psu_sensor))
                return False
            is_zero_value = all(psu_sensor[key]['value'] == '0.00' for key in psu_sensor.keys())
            if psu_name == this_psu:
                isPlug_this_psu = not is_zero_value
                log.info('This psu (%s) is %s'%(this_psu, ('plugged' if isPlug_this_psu else 'unplugged')))
                if not isPlug_this_psu:
                    log.info("the test will not update fw")
                    return False
            isPlug_psu += not is_zero_value
    log.info('Plugged PSUs/All PSUs: %d/%d'%(isPlug_psu, PSU_NUM_DC))
    if isPlug_psu >= 1:
        log.info("this PSU power on and other PSUs power on at least two, continue update fw")
        return True
    else:
        log.info("PSUs does not power on at least two, the test will not update fw")
        return False

#############################################################################################
# Function Name: need_update_psu_fw
# Date         : 8th July 2020
# Author       : Prapatsorn W. <pwisutti@celestica.com>
#
# Procedure Revision Details:
#   Version : 1.0  - Initial Draft  - by Prapatsorn W. <pwisutti@celestica.com>
#############################################################################################
def need_update_psu_fw(device, psu, psu_fw_version):
    log.debug('Entering procedure need_update_psu_fw with args : %s\n' %(str(locals())))
    ### check psu present ###
    log.info("Check %s present and check version"%(psu))
    psu_current_ver = verify_psu_util(device, psu, "get_psu_info")
    if psu_current_ver is None:
        return False
    ### check All PSUs power on ###
    if not check_psu_power_on(device, psu):
        return False
    ### check version ###
    need_update = 0
    need_update += CommonLib.compare_input_dict_to_parsed(psu_current_ver, psu_fw_version, False)
    if need_update:
        log.info("need to update %s" %(psu))
    else:
        log.info("no need to update %s" %(psu))
    return True if need_update > 0 else False

def need_update_dc_psu_fw(device, psu, psu_fw_version):
    log.debug('Entering procedure need_update_dc_psu_fw with args : %s\n' % (str(locals())))
    ### check psu present ###
    log.info("Check %s present and check version" % (psu))
    psu_current_ver = verify_psu_util(device, psu, "get_psu_info")
    if psu_current_ver is None:
        return False
    ### check All PSUs power on ###
    if not check_dc_psu_power_on(device, psu):
        return False
    ### check version ###
    need_update = 0
    need_update += CommonLib.compare_input_dict_to_parsed(psu_current_ver, psu_fw_version, False)
    if need_update:
        log.info("need to update %s" % (psu))
    else:
        log.info("no need to update %s" % (psu))
    return True if need_update > 0 else False

#############################################################################################
# Function Name: update_psu_fw
# Date         : 9th July 2020
# Author       : Prapatsorn W. <pwisutti@celestica.com>
#
# Procedure Revision Details:
#   Version : 1.0  - Initial Draft  - by Prapatsorn W. <pwisutti@celestica.com>
#############################################################################################
def update_psu_fw(device, psu, psu_type_name, isUpgrade=True):
    log.debug('Entering procedure update_psu_fw with args : %s\n' %(str(locals())))
    psu_ver = get_version_from_config('PSU', isUpgrade)
    if not need_update_psu_fw(device, psu, psu_ver):
        return
    online_update_psu_fw(device, psu, isUpgrade)
    verify_psu_util(device, psu, "get_psu_info", psu_ver)
    verify_sensor_util(device, psu, 'force', psu_type_name, info_flag=True)

def update_dc_psu_fw(device, psu, psu_type_name, isUpgrade=True):
    log.debug('Entering procedure update_dc_psu_fw with args : %s\n' %(str(locals())))
    deviceObj = Device.getDeviceObject(device)
    psu_ver = get_version_from_config('PSU', isUpgrade)
    power_type = dc_power(device)
    if power_type == 'DC':
        if 'minipack2_dc' in deviceObj.name:
            cmd1 = 'psu-util psu3 --get_psu_info'
            output1 = execute(deviceObj, cmd1, timeout=60)
            if 'Delta' in output1:
                log.info('The unit is Delta psu')
                if not need_update_dc_psu_fw(device, psu, psu_ver):
                    return
                online_update_psu_fw(device, psu, isUpgrade, timeout=300)
                verify_psu_util(device, psu, "get_psu_info", psu_ver)
                verify_sensor_util(device, psu, 'force', psu_type_name, info_flag=True)
            else:
                log.info('The unit is Liteon psu')
                if not need_update_dc_psu_fw(device, psu, psu_ver):
                    return
                online_update_psu_fw(device, psu, isUpgrade, timeout=900)
                verify_psu_util(device, psu, "get_psu_info", psu_ver)
                verify_sensor_util(device, psu, 'force', psu_type_name, info_flag=True)
        elif 'wedge400_dc' in deviceObj.name or 'wedge400c_dc' in deviceObj.name:
            cmd2 = 'psu-util psu2 --get_psu_info'
            output2 = execute(deviceObj, cmd2, timeout=60)
            if 'Delta' in output2:
                log.info('The unit is Delta psu for wedge')
                if not need_update_dc_psu_fw(device, psu, psu_ver):
                    return
                online_update_psu_fw(device, psu, isUpgrade, timeout=360)
                verify_psu_util(device, psu, "get_psu_info", psu_ver)
                verify_sensor_util(device, psu, 'force', psu_type_name, info_flag=True)
            else:
                log.info('The unit is Liteon psu for wedge')
                if not need_update_dc_psu_fw(device, psu, psu_ver):
                    return
                online_update_psu_fw(device, psu, isUpgrade, timeout=900)
                verify_psu_util(device, psu, "get_psu_info", psu_ver)
                verify_sensor_util(device, psu, 'force', psu_type_name, info_flag=True)

#############################################################################################
# Function Name: online_update_psu_fw
# Date         : 9th July 2020
# Author       : Prapatsorn W. <pwisutti@celestica.com>
#
# Procedure Revision Details:
#   Version : 1.0  - Initial Draft  - by Prapatsorn W. <pwisutti@celestica.com>
#############################################################################################
def online_update_psu_fw(device, psu, isUpgrade=True, timeout=300):
    log.debug('Entering procedure online_update_psu_fw with args : %s\n' %(str(locals())))
    deviceObj = Device.getDeviceObject(device)
    imageObj = SwImage.getSwImage(SwImage.PSU)
    package_file = imageObj.newImage if isUpgrade else imageObj.oldImage
    package_file_path = imageObj.localImageDir
    err_count = 0
    #timeout = 300
    ### update primary fw ###
    ### psu-util psu1 --update xxx.bin %%%
    cmd = 'psu-util %s --update %s/%s'%(psu, package_file_path, package_file['pri'])
    cmd2 = 'psu-util %s --update %s/%s'%(psu, package_file_path, package_file['sec'])
    if 'minipack2_dc' in deviceObj.name:
        cmd = 'psu-util %s --update %s/%s'%(psu, package_file_path, package_file['pri'])
    elif 'wedge400_dc' in deviceObj.name or 'wedge400c_dc' in deviceObj.name:
        cmd = 'psu-util %s --update %s/%s' % (psu, package_file_path, package_file['pri'])
    if 'minipack2_dc' in deviceObj.name:
        log.info("update %s primary fw" %(psu))
        output = execute(deviceObj, cmd, timeout=timeout)
        pass_message = '-- Upgrade Done --'
        match = re.search(pass_message, output)
        if match:
            log.success("Successfully update %s primary fw"%(psu))
        else:
            log.fail("update %s primary fw"%(psu))
            err_count += 1
        set_time_delay('20')
    elif 'wedge400_dc' in deviceObj.name or 'wedge400c_dc' in deviceObj.name:
        log.info("update %s primary fw" %(psu))
        deviceObj.sendline(cmd)
        #output = execute(deviceObj, cmd, timeout=timeout)
        pass_message = '-- Reset PSU --'
        deviceObj.receive(pass_message, timeout=timeout)
        booting_msg = 'Starting kernel ...'
        deviceObj.receive(booting_msg, timeout=Const.BOOTING_TIME)
        time.sleep(120)
        deviceObj.getPrompt(OPENBMC_MODE, timeout=Const.BOOTING_TIME)
        deviceObj.getPrompt(CENTOS_MODE, timeout=Const.BOOTING_TIME)
        deviceObj.getPrompt(OPENBMC_MODE, timeout=Const.BOOTING_TIME)
        time.sleep(10)
    else:
        log.info("update %s primary fw" % (psu))
        output = execute(deviceObj, cmd, timeout=timeout)
        pass_message = '-- Upgrade Done --'
        match = re.search(pass_message, output)
        if match:
            log.success("Successfully update %s primary fw" % (psu))
        else:
            log.fail("update %s primary fw" % (psu))
            err_count += 1
        set_time_delay('5')
        ## update second psu
        log.info("update %s secondary fw" %(psu))
        output2 = execute(deviceObj, cmd2, timeout=timeout)
        match2 = re.search(pass_message, output2)
        if match2:
            log.success("Successfully update %s secondary fw"%(psu))
        else:
            log.fail("update %s secondary fw"%(psu))
            err_count += 1
    if err_count:
        show_unit_info(device)
        raise testFailed('online_update_psu_fw')

#############################################################################################
# Function Name: check_pem_presence
# Date         : 9th July 2020
# Author       : Prapatsorn W. <pwisutti@celestica.com>
#
# Procedure Revision Details:
#   Version : 1.0  - Initial Draft  - by Prapatsorn W. <pwisutti@celestica.com>
#############################################################################################
def check_pem_presence(device, pem):
    log.debug('Entering procedure check_pem_presence with args : %s\n' %(str(locals())))
    pem_dict = verify_sensor_util(device, pem)
    if pem_dict:
        log.info("%s present"%(pem))
        return True
    log.info("%s is not present"%(pem))
    return False

#############################################################################################
# Function Name: run_sdk_init
# Date         : 13rd July 2020
# Author       : Prapatsorn W. <pwisutti@celestica.com>
#
# Procedure Revision Details:
#   Version : 1.0  - Initial Draft  - by Prapatsorn W. <pwisutti@celestica.com>
#############################################################################################
def run_sdk_init(device, exe_timeout=600, exit_flag=True):
    log.debug('Entering procedure run_sdk_init with args : %s\n' %(str(locals())))
    deviceObj = Device.getDeviceObject(device)
    deviceObj.getPrompt(CENTOS_MODE)
    deviceObj.sendline(SDK_INIT_CMD)
    try:
        deviceObj.read_until_regexp(SDK_PROMPT, timeout=exe_timeout)
        time.sleep(1)
    except:
        deviceObj.getPrompt(CENTOS_MODE)
        show_unit_info(device)
        raise testFailed("Failure while run_sdk_init with result FAIL")

    if exit_flag:
        deviceObj.sendline(SDK_EXIT_CMD)
        deviceObj.getPrompt(CENTOS_MODE)
    log.success("Successfully run_sdk_init")

#############################################################################################
# Function Name: copy_file_on_device
# Date         : 14th July 2020
# Author       : Prapatsorn W. <pwisutti@celestica.com>
#
# Procedure Revision Details:
#   Version : 1.0  - Initial Draft  - by Prapatsorn W. <pwisutti@celestica.com>
#############################################################################################
def copy_file_on_device(device, source_path, dest_path):
    log.debug('Entering procedure copy_file_on_device with args : %s\n' %(str(locals())))
    deviceObj = Device.getDeviceObject(device)
    cmd1 = 'find /usr/lib/ -name python3*'
    output1 = execute(deviceObj, cmd1)
    p2 = r'/usr/lib/python3'
    for line in output1.splitlines():
        line = line.strip()
        match = re.search(p2, line)
        if match:
            new_python_path = line + '/'
    if 'python' in dest_path:
        dest_path = new_python_path
    cmd = 'cp -rf %s %s'%(source_path, dest_path)
    deviceObj = Device.getDeviceObject(device)
    output = execute(deviceObj, cmd)
    p1 = 'No such file or directory'
    match = re.search(p1, output)
    if match:
        log.fail("%s"%match.group(0))
        log.fail("Cannot copy files %s to %s"%(source_path, dest_path))
        show_unit_info(device)
        raise testFailed("copy_file_on_device")
    else:
        log.success("Successfully copy file on device")

#############################################################################################
# Function Name: run_cit_test
# Date         : 14th July 2020
# Author       : Prapatsorn W. <pwisutti@celestica.com>
#
# Procedure Revision Details:
#   Version : 1.0  - Initial Draft  - by Prapatsorn W. <pwisutti@celestica.com>
#############################################################################################
def check_power_type_and_store(device):
    log.debug('Entering procedure check_power_type_and_store with args : %s\n' % (str(locals())))
    deviceObj = Device.getDeviceObject(device)
    cmd1 = 'source openbmc-utils.sh'
    cmd2 = 'wedge_power_supply_type'
    cmd_cat = 'cat /tmp/cache_store/power_type'
    deviceObj.sendline(cmd1)
    output = execute(deviceObj, cmd2)
    p1 = 'PSU48'
    p2 = 'PSU'
    p3 = 'PEM'
    mat1 = re.search(p1, output)
    mat2 = re.search(p2, output)
    if mat1:
        cmd3 = 'echo PSU48 > /tmp/cache_store/power_type'
    elif mat2:
        cmd3 = 'echo PSU > /tmp/cache_store/power_type'
    else:
        cmd3 = 'echo PEM > /tmp/cache_store/power_type'
    deviceObj.sendCmd(cmd3)
    output = execute(deviceObj, cmd_cat, timeout=30)


def run_cit_test(device, cmd, pem1_presence, pem2_presence):
    log.debug('Entering procedure run_cit_test with args : %s\n' %(str(locals())))
    deviceObj = Device.getDeviceObject(device)
    #if pem1_presence or pem2_presence:
    #    if 'wedge400c_rsp' in deviceObj.name:
    #        pass_keyword = CIT_PASS_PEM_RSP
    #    else:
    #        pass_keyword = CIT_PASS_PEM
    #else:
    #    if 'wedge400_rsp' in deviceObj.name:
    #        pass_keyword = CIT_PASS_PSU_RSP
    #    else:
    #        pass_keyword = CIT_PASS_PSU
    #if 'minipack2_rsp' in deviceObj.name:
        #cmd = cit_test_cmd_rsp
    #elif 'minipack2_dc' in deviceObj.name:
        #cmd = cit_test_cmd_dc
    pass_keyword = CIT_PASS
    output = execute(deviceObj, cmd, timeout=3000)
    if parserOpenbmc.parse_simple_keyword(pass_keyword, output) != '':
        log.success("Successfully run_cit_test")
    else:
        log.fail("run_cit_test")
        show_unit_info(device)
        raise testFailed("run_cit_test")

def set_the_log_level_to_debug(device, cmd):
    log.debug('Entering procedure set_the_log_level_to_debug with args : %s\n' % (str(locals())))
    deviceObj = Device.getDeviceObject(device)
    log.info('#### The cmd is [%s] ####'%cmd)
    execute(deviceObj, cmd, timeout=60)
    level_cmd = 'cat utils/cit_logger.py |grep "level"'
    maxBytes_cmd = 'cat utils/cit_logger.py |grep "maxBytes"'
    p1 = '"level": "DEBUG"'
    p2 = '"maxBytes": 1000000'
    cmdLst = [level_cmd, maxBytes_cmd]
    patternLst = [p1, p2]
    for i in range(0, len(cmdLst)):
        output = execute(deviceObj, cmdLst[i], timeout=60)
        res = re.search(patternLst[i], output)
        if res:
            log.success('Get the cit info: %s.'%res.group(0))
        else:
            log.fail('Set cit level to debug fail.')
            raise testFailed('Failed run set_the_log_level_to_debug')


def copy_cit_log_to_data1(device, cit_log):
    log.debug('Entering procedure copy_cit_log_to_data1 with args : %s\n' % (str(locals())))
    deviceObj = Device.getDeviceObject(device)
    error_count = 0
    p1 = r'\d{4}(-\d{2}){5}'
    p2 = r'No such file or directory'
    date_cmd = 'date +%Y-%m-%d-%H-%M-%S'
    #1. Check if /tmp/cit.log exists
    cmd1 = 'ls ' + cit_log
    output = execute(deviceObj, cmd1, timeout=60)
    if re.search(p2, output):
        error_count += 1
        log.fail('Do not find cit.log file.')
    #2. copy to /mnt/data1/
    #cmd = 'cp ' + cit_log + ' /mnt/data1/cit.log_'
    cmd = 'cp ' + cit_log + ' /mnt/data1/cit_'
    if ('minipack3' in deviceObj.name) or ('minerva' in deviceObj.name):
        cmd = 'cp ' + cit_log + ' /mnt/data/cit_'
    output = execute(deviceObj, date_cmd, timeout=60)
    res = re.search(p1, output)
    if res:
        date_name = res.group(0)
        cmd += date_name
        cmd += '.log'
        execute(deviceObj, cmd, timeout=120)
        cmd2 = 'ls /mnt/data1/cit_' + date_name + '.log'
        if ('minipack3' in deviceObj.name) or ('minerva' in deviceObj.name):
            cmd2 = 'ls /mnt/data/cit_' + date_name + '.log'
        output = execute(deviceObj, cmd2, timeout=60)
        if re.search(p2, output):
            error_count += 1
            log.fail('Copy cit log fail.')
    else:
        error_count += 1
        log.fail('Do not match date.')
    if error_count:
        raise testFailed('Failed run copy_cit_log_to_data1.')

################################################################################
# Function Name: check_spi_util_output
# Date         : 16th July 2020
# Author       : James Shi <jameshi@celestica.com>
# Procedure Revision Details:
#   Version : 1.0  - Initial Draft  - by James Shi <jameshi@celestica.com>
################################################################################
def check_spi_util_output(device, str_1, str_2):
    log.debug('Entering procedure check_spi_util_output with args : %s\n' %(str(locals())))
    deviceObj = Device.getDeviceObject(device)
    p1 = 'Usage:([\w\W]+)(bit|bin)'
    cmd = 'spi_util.sh'
    output = execute(deviceObj, cmd, timeout=10)
    match = re.search(p1, output)
    if match:
        str_list = match.group().splitlines()
        str_list_1 = str_1.split("||")
        str_list_2 = str_2.split("||")
        if str_list == str_list_1 or str_list == str_list_2:
            log.success("Successfully check_spi_util_output.")
        else:
            log.fail("the output is not the same as defined")
            log.info('option_1: %s'%str_list_1)
            log.info('option_2: %s'%str_list_2)
            show_unit_info(device)
            raise testFailed("check_spi_util_output fail")
    else:
        log.fail("Not found '%s' in output"%(p1))
        show_unit_info(device)
        raise testFailed("check_spi_util_output fail")

################################################################################
# Function Name: power_reset_enter_into_bios
# Date         : 15th July 2020
# Author       : James Shi <jameshi@celestica.com>
#
# Procedure Revision Details:
#   Version : 1.0  - Initial Draft  - by James Shi <jameshi@celestica.com>
################################################################################
def power_reset_enter_into_bios(device):
    ###reset come os by bmc side when come os enter into bios.
    log.debug('Entering procedure power_reset with args : %s\n' %(str(locals())))
    deviceObj = Device.getDeviceObject(device)
    cmd = 'wedge_power.sh reset'
    cmd1 = 'sol.sh'
    err_count = 0
    output = execute(deviceObj, cmd, timeout=10)
    deviceObj.getPrompt(OPENBMC_MODE)
    deviceObj.sendCmd(cmd1)
    log.debug('Entering enter_bios_setup with args : %s' %(str(locals())))
    line1 = 'Press <DEL> or <F2> to enter setup.'
    line2 = 'Enter Setup...'
    line3 = '.*Aptio Setup Utility.*'
    line4 = 'Enter Password'
    line5 = '------'
    deviceObj.read_until_regexp(line1, timeout=200)
    bios_menu_lib.send_key(device, "KEY_DEL")
    output = deviceObj.read_until_regexp(line5, timeout=60)
    match = re.search(line4, output)
    match1 = re.search(line3, output)
    if match:
        log.debug("Found '%s'"%(line4))
        bios_menu_lib.send_key(device, "KEY_ENTER")
        deviceObj.read_until_regexp(line3, timeout=60)
        log.success("Successfully enter Bios Setup")
    elif match1:
        log.debug("Found '%s'"%(line3))
        log.success("Successfully enter Bios Setup")
    else:
        log.fail("Failed enter Bios Setup")
        show_unit_info(device)
        raise testFailed("enter_bios_setup")

#############################################################################################
# Function Name: get_firmware_rev
# Date         : 3rd August 2020
# Author       : Prapatsorn W. <pwisutti@celestica.com>
#
# Procedure Revision Details:
#   Version : 1.0  - Initial Draft  - by Prapatsorn W. <pwisutti@celestica.com>
#############################################################################################
def get_firmware_rev(device, isNewVersion=True):
    log.debug('Entering procedure get_firmware_rev : %s\n'%(str(locals())))
    image_version = {}
    bmc_version = verify_fw_version(device, 'BMC', get_flag=True)['BMC Version']
    p1 = r'\d+\.\d+'
    isReleaseVersion = re.search(p1, bmc_version)
    if isReleaseVersion:
        log.info('getting firmware version from "cat /etc/issue"')
        image_version['Firmware Revision'] = isReleaseVersion.group(0)
    else:
        log.info('bmc is auto build image, firmware version is %s'%(AUTO_BUILD_FW_VER))
        image_version['Firmware Revision'] = AUTO_BUILD_FW_VER
    log.info(image_version)
    return image_version

#############################################################################################
# Function Name: check_th4_chip
# Date         : 3rd September 2020
# Author       : Prapatsorn W. <pwisutti@celestica.com>
#
# Procedure Revision Details:
#   Version : 1.0  - Initial Draft  - by Prapatsorn W. <pwisutti@celestica.com>
#############################################################################################
def check_th4_chip(device):
    log.debug('Entering procedure check_th4_chip : %s\n'%(str(locals())))
    deviceObj = Device.getDeviceObject(device)
    return deviceObj.isMinipack2TH4Presence()

#############################################################################################
# Function Name: read_spi_eeprom
# Date         : 14th September 2020
# Author       : Prapatsorn W. <pwisutti@celestica.com>
#
# Procedure Revision Details:
#   Version : 1.0  - Initial Draft  - by Prapatsorn W. <pwisutti@celestica.com>
#############################################################################################
def read_spi_eeprom(device, spi_type, eeprom_type, dump_name):
    ### spi_util.sh read spi1 BCM5389_EE dump1
    log.debug('Entering procedure read_spi_eeprom with args : %s\n' %(str(locals())))
    read_cmd = 'spi_util.sh read %s %s %s'%(spi_type, eeprom_type, dump_name)
    reading_msg = 'Reading flash... done'
    if eeprom_type == 'BCM5387_EE' or eeprom_type == 'BCM5389_EE':
        reading_msg = 'Reading (\w+) to %s'%(dump_name)
    output = execute(deviceObj, read_cmd, timeout=200)
    time.sleep(1)
    if parserOpenbmc.parse_simple_keyword(reading_msg, output) == '':
        log.fail("'%s' failed"%(read_cmd))
        show_unit_info(device)
        raise testFailed("read_spi_eeprom")
    else:
        log.success("Successfully read_spi_eeprom")

#############################################################################################
# Function Name: write_spi_eeprom
# Date         : 14th September 2020
# Author       : Prapatsorn W. <pwisutti@celestica.com>
#
# Procedure Revision Details:
#   Version : 1.0  - Initial Draft  - by Prapatsorn W. <pwisutti@celestica.com>
#############################################################################################
def write_spi_eeprom(device, spi_type, eeprom_type, isUpgrade=True, erase_flag=False):
    log.debug('Entering procedure write_spi_eeprom with args : %s\n' %(str(locals())))
    deviceObj = Device.getDeviceObject(device)
    if eeprom_type == 'BCM5387_EE' or eeprom_type == 'BCM5389_EE':
        imageObj = SwImage.getSwImage(SwImage.OOB)
    else:
        imageObj = SwImage.getSwImage(eeprom_type)
    if isUpgrade:
        package_file = imageObj.newImage
    else:
        package_file = imageObj.oldImage
    image_file = imageObj.localImageDir + '/' + package_file
    if erase_flag:
        cmd = 'spi_util.sh erase %s %s'%(spi_type, eeprom_type)
        pass_message = SPI_ERASE_WRITE_MSG
        if eeprom_type == 'BCM5387_EE' or eeprom_type == 'BCM5389_EE':
            pass_message = 'Erasing (\w+)|Done'
    else:
        cmd = 'spi_util.sh write %s %s %s'%(spi_type, eeprom_type, image_file)
        pass_message = SPI_UPDATE_PASS_MSG
        if eeprom_type == 'BCM5387_EE' or eeprom_type == 'BCM5389_EE':
            pass_message = 'Writing %s to (\w+)'%(image_file)

    output = execute(deviceObj, cmd, timeout=200)
    time.sleep(3)
    if parserOpenbmc.parse_simple_keyword(pass_message, output) == '':
        log.fail("'%s' failed"%(cmd))
        show_unit_info(device)
        raise testFailed("write_spi_eeprom")
    else:
        log.info("Successfully write_spi_eeprom")

#############################################################################################
# Function Name: compare_dump_data_and_image_bin
# Date         : 14th September 2020
# Author       : Prapatsorn W. <pwisutti@celestica.com>
#
# Procedure Revision Details:
#   Version : 1.0  - Initial Draft  - by Prapatsorn W. <pwisutti@celestica.com>
#############################################################################################
def compare_dump_data_and_image_bin(device, image_type, dump_file):
    log.debug('Entering procedure compare_dump_data_and_image_bin with args : %s\n' %(str(locals())))
    imageObj = SwImage.getSwImage(image_type)
    image_file = imageObj.localImageDir + '/' + imageObj.newImage
    compare_binary_file(device, dump_file, image_file)

#############################################################################################
# Function Name: run_hexdump
# Date         : 17th September 2020
# Author       : Prapatsorn W. <pwisutti@celestica.com>
#
# Procedure Revision Details:
#   Version : 1.0  - Initial Draft  - by Prapatsorn W. <pwisutti@celestica.com>
#############################################################################################
def run_hexdump(device, dump_name, erase_flag=False):
    log.debug('Entering procedure run_hexdump with args : %s\n' %(str(locals())))
    deviceObj = Device.getDeviceObject(device)
    if erase_flag:
        log.debug("erase_flag!")
        p1 = r'00000000  ff ff ff ff ff ff ff ff  ff ff ff ff ff ff ff ff'
    else:
        p1 = r'(( [0-9a-fA-F]{2}){8} ){2}'
    hexdump_cmd = 'hexdump -C ' + dump_name
    output = execute(deviceObj, hexdump_cmd, timeout=200)
    match = re.search(p1, output)
    if match:
        log.success("Successfully run_hexdump")
    else:
        log.fail("Not found pattern '%s'"%(p1))
        show_unit_info(device)
        raise testFailed("run_hexdump")

#############################################################################################
# Function Name: verify_TH4_version
# Date         : 17th September 2020
# Author       : Prapatsorn W. <pwisutti@celestica.com>
#
# Procedure Revision Details:
#   Version : 1.0  - Initial Draft  - by Prapatsorn W. <pwisutti@celestica.com>
#############################################################################################
def verify_TH4_version(device, th4_version, get_flag=False):
    log.debug('Entering procedure verify_TH4_version with args : %s\n' %(str(locals())))
    from Sdk_variable import SDKLT_array, BCM_promptstr
    err_count = 0
    deviceObj = Device.getDeviceObject(device)

    deviceObj.getPrompt(CENTOS_MODE)
    CommonLib.set_interface_link('usb0', 'up', CENTOS_MODE)
    CommonLib.check_file_exist(SDK_PATH, mode=CENTOS_MODE)
    CommonLib.change_dir(SDK_PATH, CENTOS_MODE)

    deviceObj.sendline("./%s"%(SDK_SCRIPT))
    deviceObj.read_until_regexp(BCM_promptstr, timeout=90)
    deviceObj.sendline(SDKLT_array['SDKLT_tool'])
    deviceObj.read_until_regexp(SDKLT_array['SDKLT_prompt'])
    deviceObj.sendline(SDKLT_array['PCIE_INFO_CMD'])
    time.sleep(0.5)
    output = deviceObj.readMsg()
    try:
        output += deviceObj.read_until_regexp(SDKLT_array['SDKLT_prompt'], timeout=90)
        time.sleep(1)
    except:
        deviceObj.sendline(SDK_EXIT_CMD)
        time.sleep(1)
        deviceObj.sendline(SDK_EXIT_CMD)
        time.sleep(1)
        raise testFailed("Failure while verify_TH4_version with result FAIL")

    deviceObj.sendline(SDK_EXIT_CMD)
    deviceObj.read_until_regexp(BCM_promptstr)
    deviceObj.sendline(SDK_EXIT_CMD)
    deviceObj.getPrompt(CENTOS_MODE)

    parsed_output = parserOpenbmc.parse_th3_version(output)
    if get_flag:
        return parsed_output
    err_count += CommonLib.compare_input_dict_to_parsed(parsed_output, th4_version)
    if err_count:
        show_unit_info(device)
        raise testFailed("Failure while verify_TH4_version with result FAIL")

#############################################################################################
# Function Name: need_update_th4
# Date         : 17th September 2020
# Author       : Prapatsorn W. <pwisutti@celestica.com>
#
# Procedure Revision Details:
#   Version : 1.0  - Initial Draft  - by Prapatsorn W. <pwisutti@celestica.com>
#############################################################################################
def need_update_th4(device, th4_version):
    log.debug('Entering procedure need_update_th4 with args : %s\n' %(str(locals())))
    err_count = 0
    parsed_output = verify_TH4_version(device, th4_version, get_flag=True)
    err_count += CommonLib.compare_input_dict_to_parsed(parsed_output, th4_version, False)
    return True if err_count > 0 else False

#############################################################################################
# Function Name: update_th4
# Date         : 17th September 2020
# Author       : Prapatsorn W. <pwisutti@celestica.com>
#
# Procedure Revision Details:
#   Version : 1.0  - Initial Draft  - by Prapatsorn W. <pwisutti@celestica.com>
#############################################################################################
def update_th4(device, isUpgrade=True):
    log.debug('Entering procedure update_th4 with args : %s\n' %(str(locals())))
    verify_current_boot_flash(device, 'master')

    th4_version = get_version_from_config(SwImage.TH4, isNewVersion=isUpgrade)
    #### temporary comment because TH4 now have only one version
    if not need_update_th4(device, th4_version):
         log.info("Already at version " + str(th4_version) + ", need not update.")
         return
    need_update_th4(device, th4_version)

    write_spi_eeprom(device, 'spi1', SwImage.TH4, isUpgrade=isUpgrade)
    reset_power_chassis(device)
    verify_TH4_version(device, SwImage.TH4, th4_version)

#############################################################################################
# Function Name: run_mdio_util
# Date         : 21th September 2020
# Author       : Prapatsorn W. <pwisutti@celestica.com>
#
# Procedure Revision Details:
#   Version : 1.0  - Initial Draft  - by Prapatsorn W. <pwisutti@celestica.com>
#############################################################################################
def run_mdio_util(device, mdio_bus, phy_addr, option, val):
    log.debug('Entering procedure run_mdio_util with args : %s\n' %(str(locals())))
    deviceObj = Device.getDeviceObject(device)
    ### mdio-util -m 2 -p 0x0a -r 0x0
    cmd = "mdio-util -m %s -p %s -%s 0x0"%(mdio_bus, phy_addr, option)
    if option == 'w':
        cmd += " -d %s"%(val)
    output = execute(deviceObj, cmd)
    parsed_val = parserOpenbmc.parse_read_write_mdio(output)
    if parsed_val != "" and int(parsed_val, 16) == int(val, 16):
        log.success("Successfully run mdio-util with option -%s, values match '%s', '%s'"%(option, parsed_val, val))
    else:
        log.fail("run mdio-util option -%s value mismatch, found '%s', expected '%s'"%(option, parsed_val, val))
        show_unit_info(device)
        raise testFailed('read mdio FAIL')

#############################################################################################
# Function Name: ping6_ip_test
# Date         : 2th March 2021
# Author       : Eric Zhang <zfzhang@celestica.com>
#
# Procedure Revision Details:
#   Version : 1.0  - Initial Draft  - by Eric Zhang <zfzhang@celestica.com>
#############################################################################################
def ping6_ip_test(device):
    log.debug('Entering procedure ping6_ip_test with args : %s\n' % (str(locals())))
    deviceObj = Device.getDeviceObject(device)

    cmd = 'ping6 -c5 fe80::ff:fe00:2%usb0'
    output = execute(deviceObj, cmd)
    if '0% packet loss' in output:
        log.success("ping usb0 interface successfully")
    else:
        log.fail("ping usb0 interface failed")
        show_unit_info(device)
        raise testFailed('ping failed')

################################################################################
# Function Name: run_curl_get
# Parameters :
#    resource           : Resource to be used for GET option
#                         exmaple format : /redfish/v1/Chassis/Self/LogServices/Logs
#    auth               : Flag if auth is required
#
# Description: This will execute curl command with GET option in CAP Server.
#              Just the resource/page location is required as input. It will 
#              return the JSON as a result of GET option in curl command
################################################################################

def run_curl_get(resource,auth=True):
   global device
   device = DeviceMgr.getDevice()
   cmd = "curl -k https://" + device.bmcIP + resource
   if auth:
       cmd = cmd + " -u " + device.bmcUserName + ":" + device.bmcPassword
   log.success(cmd)
   arg_list = cmd.split(' ')
   output = subprocess.check_output(arg_list)
   log.success(str(output))
   return json.loads(output)

################################################################################
# Function Name: find_keys
# Parameters :
#    node             : The dictionary in which key is to be found
#    kv               : Key
#
# Description: This generator function (recursive in nature) will return an 
#              iterator containing the value of the key. Later List can be 
#              constructed by the calling function
################################################################################

def find_keys(node, kv):
    if isinstance(node, list):
        for i in node:
            for x in find_keys(i, kv):
               yield x
    elif isinstance(node, dict):
        if kv in node:
            yield node[kv]
        for j in node.values():
            for x in find_keys(j, kv):
                yield x

################################################################################
# Function Name: get_key_value
# Parameters :
#    dictionary        : The dictionary in which key is to be found
#    key               : Key
#
# Description: This will use find_keys function to provide actual value of Key.
#              Alternatively the same function can be used to check if Key is 
#              present
################################################################################

def get_key_value(dictionary,key):
    tmp = list(find_keys(dictionary,key))
    if tmp != []:
       log.success("Key %s is Present" %(key))
       out = tmp[0]
       log.success(str(out))
       return out
    else:
        log.fail("Key %s is not Present" %(key))
        show_unit_info(device)
        raise testFailed("Key %s is not Present" %(key))

################################################################################
# Function Name: run_curl_patch
# Parameters :
#    resource           : Resource to be used for PATCH option
#                         exmaple format : /redfish/v1/Chassis/Self/LogServices/Logs
#    data               : The content the needs to be modified in JSON format
#    auth               : Flag if auth is required
#
# Description: This will execute curl command with PATCH option in CAP Server.
################################################################################

def run_curl_patch(resource,data,auth=True):
   global device
   device = DeviceMgr.getDevice()
   cmd = "curl -k -X PATCH https://" + device.bmcIP + resource + " -d " + data + " -H 'If-None-Match: xxxx'" + " -H 'Content-Type: application/json'"
   if auth:
       cmd = cmd + " -u " + device.bmcUserName + ":" + device.bmcPassword
   log.success(cmd)
   try:
      os.system(cmd)
   except:
      log.fail("Failed to execute curl PATCH command")
      show_unit_info(device)
      raise testFailed("Failed to execute curl PATCH command")

################################################################################
# Function Name: check_values_are_equal
################################################################################

def check_values_are_equal(actual, expected, expect=True):
    log.debug("Entering procedure check_values_are_equal details: %s" %(str(locals())))
    if expect:
        if actual == expected:
            log.info("Expected Value is present")
        else:
            log.fail("Expected Value is not present")
            show_unit_info(device)
            raise RuntimeError("Expected Value is not present")
    else:
        if actual == expected:
            log.fail("Expected Value is present")
            show_unit_info(device)
            raise RuntimeError("Expected Value is present")
        else:
            log.info("Expected Value is not present")

################################################################################
# Function Name: run_curl_post
# Parameters :
#    resource           : Resource to be used for POST option
#                         exmaple format : /redfish/v1/Chassis/Self/LogServices/Logs
#    data               : The content the needs to be modified in JSON format
#    auth               : Flag if auth is required
#
# Description: This will execute curl command with POST option in CAP Server.
################################################################################

def run_curl_post(resource,data,auth=True):
   global device
   device = DeviceMgr.getDevice()
   data = data.replace(" ", "")
   cmd = "curl -k -X POST https://" + device.bmcIP + resource + " -d " + data + " -H " + "If-None-Match:xxxx" + " -H " + "Content-Type:application/json"
   if auth:
       cmd = cmd + " -u " + device.bmcUserName + ":" + device.bmcPassword
   log.success(cmd)
   arg_list = cmd.split(' ')
   try:
      output = subprocess.check_output(arg_list)
   except:
      log.fail("Failed to execute curl POST command")
      show_unit_info(device)
      raise testFailed("Failed to execute curl POST command")
   log.success(str(output))
   return json.loads(output)

################################################################################
# Function Name: run_curl_delete
# Parameters :
#    resource           : Resource to be used for DELETE option
#                         exmaple format : /redfish/v1/Chassis/Self/LogServices/Logs
#    data               : The content the needs to be modified in JSON format
#    auth               : Flag if auth is required
#
# Description: This will execute curl command with DELETE option in CAP Server.
################################################################################

def run_curl_delete(resource,data=None,auth=True,output_required=False):
   global device
   device = DeviceMgr.getDevice()
   cmd = "curl -k -X DELETE https://" + device.bmcIP + resource
   if auth:
       cmd = cmd + " -u " + device.bmcUserName + ":" + device.bmcPassword
   log.success(cmd)
   arg_list = cmd.split(' ')
   try:
      output = subprocess.check_output(arg_list)
   except:
      log.fail("Failed to execute curl DELETE command")
      raise testFailed("Failed to execute curl DELETE command")
   log.success(str(output))
   if output_required:
      return json.loads(output)

################################################################################
# Function Name: check_output_from_curl
################################################################################
def check_output_from_curl(output,expected='OK'):
    log.debug(f'Entering procedure check_output_from_curl with args : {(str(locals()))}\n')
    p1 = 'OK'
    p2 = 'error'
    err_count = 0
    if expected == 'OK' and (re.search(p1, str(output))):
        log.success(f"Successfully verifed output from curl command, expected {p1}")
    elif expected == 'error' and (re.search(p2, str(output))):
        log.success(f"Successfully verifed output from curl command, expected {p2}: {output['error']}")
    else:
        if re.search(p2, str(output)):
            log.fail(f"Found error: {output['error']}")
            raise testFailed("Failed! verifed output from curl command")

#############################################################################################
# Function Name: run_curl_BMCIP_get
# Parameters :
#    resource           : Resource to be used for POST option
#                         exmaple format : /redfish/v1/Chassis/Self/LogServices/Logs
#    data               : The content the needs to be modified in JSON format
#    IP                 : BMC IP address is required which will get from ipmitool lan print 1
#    auth               : Flag if auth is required
#############################################################################################
def run_curl_BMCIP_get(resource,IP=None,auth=True):
   global device
   device = DeviceMgr.getDevice()
   if IP != None:
       cmd = "curl -k -X GET https://" + IP + resource
   else:
       cmd = "curl -k -X GET https://" + device.bmcIP + resource

   if auth:
       cmd = cmd + " -u " + device.bmcUserName + ":" + device.bmcPassword
   log.success(cmd)
   arg_list = cmd.split(' ')
   output = subprocess.check_output(arg_list)
   log.success(str(output))
   return json.loads(output)

#############################################################################################
# Function Name: get_members_message_curl_output
# Parameters :
#    resource           : Resource to be used for SEL entries
#                         exmaple format : /redfish/v1/Chassis/Self/LogServices/Logs/Entries
#    data               : Get the string content from message in member dictionary
#############################################################################################
def get_members_message_curl_output(curl_output,message_type):
    log.debug("Entering procedure get members message from curl output: %s" %(str(locals())))
    output_data= curl_output["Members"][0]['Message']
    pattern_Type = str(message_type) + "\s+:\s+(0x[0-9]+|\d+|\D+|\w),"
    try:
        object_Type = re.search(pattern_Type,output_data,re.I).group(1)
    except AttributeError as AE:
        raise Exception(f"Failed to get {message_type} from curl output")
    return object_Type

################################################################################
# Function Name: run_curl_post_BCMIP
# Description: This will execute curl command with POST option in CAP Server.
################################################################################

def run_curl_post_BCMIP(resource,data,IP=None,auth=True,output_required=True):
   global device
   device = DeviceMgr.getDevice()
   data = data.replace(" ", "")
   if IP != None:
       cmd = "curl -k -X POST https://" + IP + resource + " -d " + data + " -H " + "If-None-Match:xxxx" + " -H " + "Content-Type:application/json"
   else:
       cmd = "curl -k -X POST https://" + device.bmcIP + resource + " -d " + data + " -H " + "If-None-Match:xxxx" + " -H " + "Content-Type:application/json"
   if auth:
       cmd = cmd + " -u " + device.bmcUserName + ":" + device.bmcPassword
   log.success(cmd)
   arg_list = cmd.split(' ')
   try:
      output = subprocess.check_output(arg_list)
   except:
      log.fail("Failed to execute curl POST command")
      raise testFailed("Failed to execute curl POST command")
   if output_required:
       log.success(str(output))
       return json.loads(output)

################################################################################
# Function Name: run_curl_delete_BMCIP
# Description: This will execute curl command with DELETE option in CAP Server.
################################################################################

def run_curl_delete_BCMIP(resource,IP=None,data=None,auth=True,output_required=False):
   global device
   device = DeviceMgr.getDevice()
   if IP != None:
       cmd = "curl -k -X DELETE -k https://" + IP + resource
   else:
       cmd = "curl -k -X DELETE -k https://" + device.bmcIP + resource

   if auth:
       cmd = cmd + " -u " + device.bmcUserName + ":" + device.bmcPassword
   log.success(cmd)
   arg_list = cmd.split(' ')
   try:
      output = subprocess.check_output(arg_list)
   except:
      log.fail("Failed to execute curl DELETE command")
      raise testFailed("Failed to execute curl DELETE command")
   log.success(str(output))
   if output_required:
      return json.loads(output)

def login_to_centos():
    log.debug("Entering login to centos: %s" % (str(locals())))
    deviceObj.sendline("sol.sh")
    deviceObj.receive('CTRL-l + b : Send Break', timeout=10)
    deviceObj.sendline("\r")
    deviceObj.getPrompt(CENTOS_MODE, timeout=60)

def come_side_mac_address_test(device):
    log.debug("Entering come side mac address test: %s" % (str(locals())))
    deviceObj = Device.getDeviceObject(device)
    get_come_mac = ''
    p1 = r'\w{2}:.*:\w{2}'
    p2 = r'ether (\w{2}:.*:\w{2})\s*'
    cmd = 'wedge_us_mac.sh'
    output = execute(deviceObj, cmd)
    match = re.search(p1, output)
    cmd_mac_value = match.group()
    if ('minipack3' in deviceObj.name) or ('minerva' in deviceObj.name):
        cmd_mac_value = cmd_mac_value.lower()
    deviceObj.sendline("sol.sh")
    deviceObj.receive('CTRL-l + b : Send Break', timeout=10)
    deviceObj.sendline("\r")
    cmd1 = 'ifconfig eth0'
    output1 = execute(deviceObj, cmd1, mode=CENTOS_MODE)
    for line in output1.splitlines():
        line = line.strip()
        match1 = re.search(p2, line)
        if match1:
            get_come_mac = match1.group(1)
    time.sleep(1)
    if cmd_mac_value == get_come_mac:
        log.success("get COMe side mac value is %s" % (get_come_mac))
    else:
        log.fail("the mac address is diff: cmd_get_value: %s, COMe side value: %s"%(cmd_mac_value, get_come_mac))
        show_unit_info(device)
        raise testFailed("Failed to execute COMe side mac address test")

def ping6_bmc_from_dhcp(device, bmc_ipv6, mode=None):
    log.debug('Entering procedure ping6_bmc_from_dhcp with args : %s\n' %(str(locals())))
    deviceObj = Device.getDeviceObject(device)
    cmd = 'ping %s -c 5'%(bmc_ipv6)
    output = deviceObj.executeCmd(cmd, mode=mode)
    p1 = ' 0% packet loss'
    match = re.search(p1, output)
    if match:
        log.success("Ping success from dhcp server to bmc")
    else:
        log.fail("ping failed from dhcp to bmc")
        show_unit_info(device)
        raise testFailed("verify_dhcp_server")

def ssh_dhcp_server_from_bmc(dhcp_ipv6, usrname, passwrd, prmpt, mode=None):
    log.debug('Entering procedure ssh_dhcp_server_from_openbmc : %s\n' %(str(locals())))
    err_msg = 'Permission denied'
    cmd = 'ssh ' + usrname + '@' + dhcp_ipv6
    deviceObj.sendCmd(cmd)
    promptList = ["(y/n)", "(yes/no)", "password:"]
    patternList = re.compile('|'.join(promptList))
    output = deviceObj.read_until_regexp(patternList, 120)
    if re.search("(y/n)",output):
        deviceObj.sendCmd("yes")
        deviceObj.read_until_regexp("password:")
        deviceObj.sendCmd(passwrd)
    elif re.search("(yes/no)",output):
        deviceObj.sendCmd("yes")
        deviceObj.read_until_regexp("password:")
        deviceObj.sendCmd(passwrd)
    elif re.search("password:",output):
        deviceObj.sendCmd(passwrd)
    else:
        log.fail("pattern mismatch")

    promptList1 = [err_msg, prmpt]
    patternList1 = re.compile('|'.join(promptList1))
    output1 = deviceObj.read_until_regexp(patternList1, 10)

    if re.search(prmpt, output1):
        deviceObj.sendCmd("exit")
        log.success("SSH success from bmc to dhcp server")
    elif re.search(err_msg, output1):
        log.fail("SSH Permission denied")
        raise testFailed("verify_dhcp_credentials")
    else:
        log.fail("ssh failed from bmc to dhcp server")
        raise testFailed("verify_dhcp_server")

def ssh_bmc_from_dhcp_server(pc, device, bmc_ipv6, mode=None):
    log.debug('Entering procedure ssh_bmc_from_dhcp_server with args : %s\n' %(str(locals())))
    err_msg = 'Permission denied'
    deviceObj = DeviceMgr.getDevice(device)
    bmcUsrnme = deviceObj.bmcUserName
    bmcPasswrd = deviceObj.bmcPassword
    bmcPrmpt = deviceObj.promptBmc
    deviceObj = Device.getDeviceObject(pc)
    ## add delete know_hosts
    host_cmd = 'rm -rf /home/svt/.ssh/known_hosts; rm -rf /home/cap/.ssh/known_hosts'
    deviceObj.transmit(host_cmd)
    cmd = 'ssh ' + bmcUsrnme + '@' + bmc_ipv6
    deviceObj.sendCmd(cmd, timeout=5)
    promptList = ["(y/n)", "(yes/no)", "password:"]
    patternList = re.compile('|'.join(promptList))
    output = deviceObj.read_until_regexp(patternList, 30)
    if re.search("(y/n)",output):
        deviceObj.transmit("yes")
        deviceObj.receive("password:")
        deviceObj.transmit(bmcPasswrd)
    elif re.search("(yes/no)",output):
        deviceObj.transmit("yes")
        deviceObj.receive("password:")
        deviceObj.transmit(bmcPasswrd)
    elif re.search("password:",output):
        deviceObj.transmit(bmcPasswrd)
    else:
        log.fail("pattern mismatch")
    promptList1 = [err_msg, bmcPrmpt]
    patternList1 = re.compile('|'.join(promptList1))
    output1 = deviceObj.read_until_regexp(patternList1, 10)

    if re.search(bmcPrmpt, output1):
        deviceObj.sendCmd("exit")
        log.success("SSH success from dhcp server to bmc")
    elif re.search(err_msg, output1):
        log.fail("SSH Permission denied")
        raise testFailed("verify_bmc_credentials")
    else:
        log.fail("ssh failed from dhcp server to bmc")
        raise testFailed("verify_dhcp_server")

def bmc_autoboot_test(device):
    log.debug("Entering bmc autoboot test: %s" % (str(locals())))
    deviceObj = Device.getDeviceObject(device)
    str1 = 'autoboot in [23] seconds'
    str2 = 'fuji'
    if 'minipack3' in deviceObj.name:
        str2 = 'montblanc'
    if 'minerva_th5' in deviceObj.name:
        str2 = 'tahan'
    if 'minerva_j3' in deviceObj.name:
        str2 = 'janga'
    str3 = 'otp version'
    str6 = 'otp rid'
    str4 = 'Unknown command'
    str5 = 'Starting kernel ...'
    cmd1 = 'otp'
    cmd2 = 'boot'
    deviceObj.sendline('reboot')
    deviceObj.read_until_regexp(str1, timeout=80)
    bios_menu_lib.send_key(device, "KEY_DEL")
    deviceObj.read_until_regexp(str2, timeout=180)
    output = deviceObj.sendCmdRegexp(cmd1, str2, timeout=60)
    match1 = re.search(str3, output)
    match2 = re.search(str6, output)
    match3 = re.search(str4, output)
    if match2 and match1:
        log.success('otp command check pass')
        deviceObj.sendline('\n')
        deviceObj.sendline(cmd2)
        deviceObj.read_until_regexp(str5, timeout=600)
        time.sleep(200)
        deviceObj.sendline('\n')
        deviceObj.getPrompt(OPENBMC_MODE, timeout=60)
    elif match3:
        log.fail('otp command check fail, show Unknown command.')
        deviceObj.sendline('\n')
        deviceObj.sendline(cmd2)
        deviceObj.read_until_regexp(str5, timeout=600)
        time.sleep(200)
        deviceObj.sendline('\n')
        deviceObj.getPrompt(OPENBMC_MODE, timeout=60)
        raise testFailed("bmc_autoboot_test check fail")
    else:
        log.fail('run otp command fail.')
        deviceObj.sendline('\n')
        deviceObj.sendline(cmd2)
        deviceObj.read_until_regexp(str5, timeout=600)
        time.sleep(200)
        deviceObj.sendline('\n')
        deviceObj.getPrompt(OPENBMC_MODE, timeout=60)
        raise testFailed("run otp command fail in bmc_autoboot_test")

def prepare_cit_package(device, image_name, host_ip, host_name, host_passwd, host_prompt):
    log.debug("Entering bmc prepare_cit_package test: %s" % (str(locals())))
    deviceObj = Device.getDeviceObject(device)
    if ('minipack2_rsp2-02' in deviceObj.name) or ('minipack2_rsp-01' in deviceObj.name) or ('wedge400_mp-01' in deviceObj.name) or ('wedge400_rsp-01' in deviceObj.name) or ('wedge400c_d1-04' in deviceObj.name) or ('wedge400c_rsp-01' in deviceObj.name):
        if 'minipack2' in deviceObj.name or 'wedge400c' in deviceObj.name:
            unit_name = deviceObj.name[10:]
        else:
            unit_name = deviceObj.name[9:]
        server_prompt = host_prompt[4:]
        imageObj = SwImage.getSwImage(image_name)
        host_path = imageObj.hostImageDir
        fileName = imageObj.newImage
        err_count = 0
        #1. login jenkins server
        #deviceObj = Device.getDeviceObject('PC')
        cmd = 'ssh ' + host_name + '@' + host_ip
        deviceObj.sendCmd(cmd)
        promptList = ["(y/n)", "(yes/no)", "password:"]
        patternList = re.compile('|'.join(promptList))
        output = deviceObj.read_until_regexp(patternList, 120)
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
        unit_cmd = 'rm -rf /home/' + unit_name
        deviceObj.sendline(unit_cmd)

        #2. unzip cit
        create_folder = 'mkdir -p /home/' + unit_name
        execute_cmd(deviceObj, create_folder)
        copy_cmd = 'cp ' + host_path + '/' + fileName + ' /home/' + unit_name + '/'
        execute_cmd(deviceObj, copy_cmd)
        deviceObj.sendline('cd /home/' + unit_name)
        deviceObj.read_until_regexp(server_prompt)
        cmd1 = "unzip %s" % (fileName)
        output1 = execute_cmd(deviceObj, cmd1, timeout=300)
        p1 = 'No such file or directory'
        match = re.search(p1, output1)
        if match:
            log.fail("%s" % (p1))
            err_count += 1
        else:
            log.success('Successfully untar %s file.' % image_name)

        #3. check package
        if 'minipack2' in deviceObj.name:
            cmd2 = 'python tests2/cit_runner.py --platform fuji --list-tests --start-dir tests2/tests/'
        else:
            cmd2 = 'python tests2/cit_runner.py --platform wedge400 --list-tests --start-dir tests2/tests/'
        output2 = execute_cmd(deviceObj, cmd2, timeout=300)
        p2 = 'Failed|No module'
        match2 = re.search(p2, output2)
        if match2:
            log.fail("Found %s" % (p2))
            err_count += 1
        else:
            deviceObj.sendline('cd /home/')
            cmd3 = 'rm -rf ' + unit_name
            execute_cmd(deviceObj, cmd3)
            log.success('Successfully check %s package.' % image_name)
        # #4. exit the server
        execute_cmd(deviceObj, 'exit')
        output3 = deviceObj.read_until_regexp('bmc', 20)
        if re.search('bmc', output3):
            log.success("exit the jenkins server.")

        if err_count > 0:
            log.fail("check cit package fail.")
            #raise testFailed("check cit package fail.")

def copy_file_to_other_folder(device):
    log.debug("Entering bmc copy_file_to_other_folder test: %s" % (str(locals())))
    deviceObj = Device.getDeviceObject(device)
    imageObj = SwImage.getSwImage('SDK')
    imageName = imageObj.newImage
    original_path = imageObj.localImageDir
    goal_path = '/usr/local/cls_diag/SDK/cel_sdk/snake/'
    cmd = 'cp ' + original_path + '/' + imageName + ' ' + goal_path
    execute_cmd(deviceObj, cmd)

def print_log_info(msg):
    log.info(msg)

def show_unit_info(device):
    log.debug("Entering bmc show_unit_info test: %s" % (str(locals())))
    deviceObj = Device.getDeviceObject(device)
    CommonLib.switch_to_openbmc()
    cmd = 'showtech.sh'
    execute_cmd(deviceObj, cmd, timeout=300)

##########Functions added for Openbmc lite program
def copy_files_from_bmc_to_cpu_new(device, cpu_ip, filename, filepath, destination_path, size_MB,
                            swap=False, ipv6=False, interface='None'):
    log.debug('Entering procedure copy_files_from_bmc_to_cpu : %s\n'%(str(locals())))
    deviceObj = Device.getDeviceObject(device)
    username = deviceObj.rootUserName
    password = deviceObj.rootPassword
    mode = OPENBMC_MODE
    ### assume avg speed is 0.5MB/s
    timeout = int(size_MB) * 3
    filelist = [filename]
    copy_files_through_scp_without_password(device, username, password, cpu_ip, filelist, \
        filepath, destination_path, OPENBMC_MODE, True, True, interface, timeout)

def copy_files_through_scp_without_password(device, username, password,server_ip, filelist: list, filepath, destination_path, mode='None', swap=False, ipv6=False, interface='None', timeout=Const.COPYING_TIME, retry=2):
    log.debug("Entering copy_files_through_scp with args : %s" %(str(locals())))
    errCount = 0
    deviceObj = Device.getDeviceObject(device)
    if mode != 'None':
        deviceObj.getPrompt(mode)
    for fileName in filelist:
        if fileName == '':
            continue
        success = False
        for retryCount in range(retry):
            log.debug("retryCount: %d"%(retryCount))
            deviceObj.flush()
            try:
                if swap:
                    if ipv6:
                        cmd = 'scp %s/%s %s@[%s'%(filepath, fileName, username, server_ip)
                        if server_ip.startswith('2001'):
                            cmd += ']:' + destination_path
                        else:
                            cmd += '%' + interface + ']:' + destination_path
                        log.cprint(cmd)
                        deviceObj.sendCmd(cmd)
                    else:
                        deviceObj.sendCmd("scp %s/%s %s@%s://%s" % (filepath, fileName, username, server_ip, destination_path))
                else:
                    if ipv6:
                            cmd = 'scp -6 %s@[%s' % (username, server_ip)
                            cmd += (']:' + filepath + '/' + fileName)
                            cmd += (' ' + destination_path + '/')
                            log.cprint(cmd)
                            deviceObj.sendCmd(cmd)
                    else:
                        deviceObj.sendCmd("scp %s@%s://%s/%s %s" % (username, server_ip, filepath, fileName, destination_path))
                promptList = ["(y/n)", "(yes/no)"]
                patternList = re.compile('|'.join(promptList))
                output1 = deviceObj.read_until_regexp(patternList, 30)
                log.info('output1: ' + str(output1))

                if re.search("yes/no",output1):
                    deviceObj.transmit("yes")
                else :
                    deviceObj.transmit("y")

                currentPromptStr = deviceObj.getCurrentPromptStr()
                currentPromptStr = currentPromptStr if currentPromptStr else "100%|No such file"
                output = deviceObj.read_until_regexp(currentPromptStr,timeout=timeout)
                p0 = ".*100\%"
                p1 = "No such file or directory"
                if re.search(p0, output):
                    log.info("Successfully copy file: %s"%(fileName))
                    success = True
                    break    # continue to copy next file
                elif re.search(p1, output):
                    log.error("%s"%(p1))
                    raise RuntimeError(p1 + ': ' + fileName)
            except:
                if ipv6:
                    deviceObj.executeCmd('ssh-keygen -R ' + server_ip + '%' + interface)
                else:
                    execute_local_cmd('ssh-keygen -R ' + server_ip)
                continue   # come to next try

        if not success:
            raise RuntimeError("Copy file {} through scp failed!".format(fileName))
    return 0

def run_redfish(device, redfish_url, ip, option='other', interface='None', ipv6=False, mode=CENTOS_MODE, data='None'):
    log.debug('Entering procedure run_redfish : %s\n'%(str(locals())))
    deviceObj = Device.getDeviceObject(device)
    pc_timeout = 20
    if option == GET:
        cmd = 'curl -g'
    elif option == POST:
        cmd = 'curl -d ' + data
        pc_timeout = 60
    elif option == 'other':
        cmd = 'curl'
    else:
        log.fail('run_curl support only "get" or "post" option')
        raise testFailed("run_curl")
    cmd += ' http://'
    if ipv6:
        if ip.startswith('2001'):
            cmd += '[' + ip + ']'
        else:
            cmd += '[' + ip + '%' + interface + ']'
    else:
        cmd += ip
    cmd += ':8080/' + redfish_url
    log.debug('cmd: %s'%(cmd))
    time.sleep(1)
    if mode == 'None':
        done_msg = r'(.*Forbidden|]?}).*%s'%(deviceObj.prompt)
        try:
            deviceObj.transmit(cmd)
            deviceObj.transmit("")
            output = deviceObj.read_until_regexp(done_msg, timeout=pc_timeout)
            log.info('output: %s'%(output))
        except:
            log.fail("Cannot get curl output within %d s"%(pc_timeout))
            show_unit_info(device)
            raise RuntimeError('run_curl')
    output = execute(deviceObj, cmd, timeout=300, mode=mode)
    log.info('output: %s'%(output))
    p0 = r'\/redfish\/v1\/\$metadata'
    p1 = r'^real\s+0m(\d+)\.\d{3}s'
    p2 = r'fail|error|Error'
    for line in output.splitlines():
        line = line.strip()
        match = re.search(p1, line)
        match1 = re.search(p2, line)
        if match or match1:
            if match1:
                log.fail('run cmd: [ %s ], finding some fail or error info.' % (cmd))
                raise testFailed("Finding error or fail info.")
            else:
                real_time = match.group(1).strip()
                if int(real_time) > 45:
                    log.fail('run cmd: [ %s ], overrun 45s'%(cmd))
                    show_unit_info(device)
    match0 = re.search(p0, output)
    if match0:
	    log.success("redfish response of '%s' is successful"%(redfish_url))
    else:
	    raise testFailed("No redfish response")

def copy_files_from_cpu_to_bmc(device, cpu_ip, filename, filepath, destination_path,
                            swap=False, ipv6=False, interface='None'):
    log.debug('Entering procedure copy_files_from_cpu_to_bmc : %s\n'%(str(locals())))
    deviceObj = Device.getDeviceObject(device)
    username = deviceObj.bmcUserName
    password = deviceObj.bmcPassword
    mode = CENTOS_MODE
    filelist = [filename]
    CommonLib.copy_files_through_scp(device, username, password, cpu_ip, filelist, \
        filepath, destination_path, mode, swap, ipv6, interface)

def run_eeprom_tool_lite(device, eeprom_type, fan='None', expected_result='None', flag='None'):
    log.debug('Entering procedure run_eeprom_tool_lite : %s\n'%(str(locals())))
    deviceObj = Device.getDeviceObject(device)
    err_count = 0
    cmd = 'weutil -e %s'%(eeprom_type)
    output = execute(deviceObj, cmd)
    parsed_output = parserOpenbmc.parse_eeprom2(output)
    if expected_result != 'None':
        expected_dict = CommonLib.get_eeprom_cfg_dict(expected_result)
        #parsed_type = parserOpenbmc.parse_eeprom_type2(output)
        #if parsed_type == eeprom_type:
        #    log.success("EEPROM type match: %s, %s"%(parsed_type, eeprom_type))
        #else:
        #    log.fail("EEPROM type mismatch: %s, %s"%(parsed_type, eeprom_type))
        #    err_count += 1
        err_count += CommonLib.compare_input_dict_to_parsed(parsed_output, expected_dict)
    else:
        if parsed_output:
            log.success("Successfully run_eeprom_tool_lite")
            return parsed_output
        else:
            log.fail("No eeprom output returned")
            err_count += 1
    if err_count:
        show_unit_info(device)
        raise testFailed("run_eeprom_tool_lite")

def store_eeprom_lite(device, eeprom_cfg_file, store_file, eeprom_path=None):
    log.debug('Entering procedure store_eeprom with args : %s\n' %(str(locals())))
    deviceObj = Device.getDeviceObject(device)
    CommonLib.change_dir('/mnt/data/', OPENBMC_MODE)
    cmd = "./fb_eeprom -b %s > %s"%(eeprom_path, eeprom_cfg_file)
    output = execute(deviceObj, cmd)
    cmd = "cp %s %s"%(eeprom_cfg_file, store_file)
    output = execute(deviceObj, cmd)
    p1 = 'No such file or directory'
    match = re.search(p1, output)
    if match:
        log.fail("Cannot store eeprom data")
        show_unit_info(device)
        raise testFailed("store_eeprom")
    else:
        log.success("Successfully store eeprom data")

def modify_eeprom_cfg_lite(device, eeprom_name, eeprom_cfg_file, bin_file_name):
    log.debug('Entering procedure modify_eeprom_cfg_lite with args : %s\n' %(str(locals())))
    deviceObj = Device.getDeviceObject(device)
    err_count = 0
    eeprom_string = CommonLib.fb_generate_eeprom_cfg(eeprom_name)
    cmd = "echo -e \"%s\" > %s"%(eeprom_string, eeprom_cfg_file)
    execute(deviceObj, cmd, timeout=150)
    bin_cmd = "/mnt/data/fb_eeprom -p %s %s"%(eeprom_cfg_file, bin_file_name)
    execute(deviceObj, bin_cmd, timeout=150)
    time.sleep(1)
    log.success("modify %s"%(eeprom_cfg_file))

def update_modified_eeprom(device, bin_name, eeprom_path, disable_write_protection='None', enable_write_protection='None'):
    log.debug('Entering procedure update_modified_eeprom with args : %s\n' %(str(locals())))
    deviceObj = Device.getDeviceObject(device)
    err_count = 0
    ### Disable EEPROM write protection
    if disable_write_protection != 'None' and 'minerva' in deviceObj.name:
        execute(deviceObj, disable_write_protection, mode=OPENBMC_MODE)
    if disable_write_protection != 'None' and 'minipack3' in deviceObj.name:
        execute(deviceObj, disable_write_protection, mode=CENTOS_MODE)
    
    ### Write EEPROM values
    cmd="dd if=/var/unidiag/firmware/%s of=%s"%(bin_name, eeprom_path)
    output = execute(deviceObj, cmd, timeout=150, mode=OPENBMC_MODE)

    ### Enable EEPROM write protection
    if enable_write_protection != 'None' and 'minerva' in deviceObj.name:
        execute(deviceObj, enable_write_protection, mode=OPENBMC_MODE)
    if enable_write_protection != 'None' and 'minipack3' in deviceObj.name:
        execute(deviceObj, enable_write_protection, mode=CENTOS_MODE)
    
    p1 = 'error'
    match = re.search(p1, output)
    if match:
        log.fail("Cannot update eeprom data")
        show_unit_info(device)
        raise testFailed("update_modified_eeprom")
    else:
        log.success("Successfully updated modified eeprom data")

def restore_eeprom_lite(device, eeprom_cfg_file, bin_name):
    log.debug('Entering procedure restore_eeprom_lite with args : %s\n' %(str(locals())))
    deviceObj = Device.getDeviceObject(device)
    CommonLib.change_dir('/mnt/data/', OPENBMC_MODE)
    cmd = "./fb_eeprom -p %s %s"%(eeprom_cfg_file, bin_name)
    output = execute(deviceObj, cmd)
    cmd = "mv %s /var/unidiag/firmware"%(bin_name)
    output = execute(deviceObj, cmd)
    p1 = 'No such file or directory'
    match = re.search(p1, output)
    if match:
        log.fail("Cannot store eeprom data")
        show_unit_info(device)
        raise testFailed("store_eeprom")
    else:
        log.success("Successfully store eeprom data")

def get_board_name(device, expected_result):
    log.debug('Entering procedure get_board_name with args : %s\n' %(str(locals())))
    deviceObj = Device.getDeviceObject(device)
    execute(deviceObj, "source /usr/local/bin/openbmc-utils.sh")
    output = execute(deviceObj, "wedge_board_type")
    if re.search(expected_result, output):
        log.success("Successfully got board name: %s"%(expected_result))
    else:
        show_unit_info(device)
        log.fail("Failed to get board name")
        raise testFailed("get_board_name failed")

def create_bin_file(device, eeprom_cfg_file, bin_name):
    log.debug('Entering procedure create_bin_file with args : %s\n' %(str(locals())))
    deviceObj = Device.getDeviceObject(device)
    err_count = 0
    bin_cmd = "/mnt/data/fb_eeprom -p %s %s"%(eeprom_cfg_file, bin_name)
    execute(deviceObj, bin_cmd, timeout=150)
    cmd = "mv %s /var/unidiag/firmware"%(bin_name)
    output = execute(deviceObj, cmd)
    time.sleep(1)
    log.success("bin file created successfully %s"%(bin_name))

def get_eeprom_value2(device, cmd, key):
    log.debug('Entering procedure get_eeprom_value2 : %s\n'%(str(locals())))
    deviceObj = Device.getDeviceObject(device)
    output = execute(deviceObj, cmd)
    time.sleep(1)
    parsed_output = parserOpenbmc.parse_eeprom2(output)
    value = parsed_output[key]
    if value:
        log.success("Successfully get_eeprom_value")
        return value.upper()
    else:
        show_unit_info(device)
        raise testFailed("get_eeprom_value")

def update_bios_lite(device, bios_flash, isUpgrade = True):
    log.debug('Entering procedure update_bios_lite with args : %s\n' %(str(locals())))
    imageObj = SwImage.getSwImage(SwImage.BIOS)
    deviceObj = Device.getDeviceObject(device)
    bios_version = {}
    bios_version[SwImage.BIOS_VER] = imageObj.newVersion if isUpgrade else imageObj.oldVersion
    if bios_flash.lower() == 'master':
        if not need_update_bios(device, bios_version):
            log.info("Already at version " +  bios_version[SwImage.BIOS_VER] + ", need not update.")
            deviceObj.getPrompt(mode=OPENBMC_MODE)
            return
    online_update_bios(device, bios_flash, isUpgrade)
    verify_power_control(device, 'off')
    verify_power_control(device, 'on')
    verify_dmidecode_bios_version(device, bios_version)
    verify_current_bios_flash(device, bios_flash)

def update_fpga_lite(device, isUpgrade = True):
    log.debug('Entering procedure update_fpga_lite with args : %s\n' %(str(locals())))
    err_count = 0
    fpga_version = get_version_from_config(SwImage.FPGA, isNewVersion=isUpgrade)
    if not need_update_fpga_lite(device, fpga_version):
        log.info("Already at version " + str(fpga_version) + ", need not update.")
        return
    online_update_fpga_lite(device, isUpgrade)
    reset_power_chassis(device)
    err_count += verify_iob_fpga_version(device, fpga_version)
    if err_count:
        log.fail("verify_iob_fpga_version failed")
        show_unit_info(device)
        raise testFailed("verify_iob_fpga_version")
    else:
        log.success("IOB FPGA verification successful")

def need_update_fpga_lite(device, fpga_version):
    log.debug('Entering procedure need_update_fpga_lite with args : %s\n' %(str(locals())))
    err_count = 0
    err_count += verify_iob_fpga_version(device, fpga_version)
    return True if err_count > 0 else False

def verify_iob_fpga_version(device, fpga_version):
    log.debug('Entering procedure verify_iob_fpga_version with args : %s\n' %(str(locals())))
    deviceObj = Device.getDeviceObject(device)
    err_count = 0
    cmd = iob_fpga_version_cmd
    output = execute(deviceObj, cmd, mode=CENTOS_MODE)
    match = re.search(fpga_version, output)
    if not match:
        err_count += 1
    return err_count

def online_update_fpga_lite(device, isUpgrade = True):
    log.debug('Entering procedure online_update_fpga_lite with args : %s\n' %(str(locals())))
    deviceObj = Device.getDeviceObject(device)
    imageObj = SwImage.getSwImage(SwImage.FPGA)
    package_file = imageObj.newImage if isUpgrade else imageObj.oldImage
    package_file_path = imageObj.localImageDir
    cmd = IOB_UPDATE_CMD + ' write ' + package_file_path + '/' + package_file
    if 'minipack3' in deviceObj.name:
        cmd = IOB_UPDATE_CMD + ' ' +  package_file_path + '/' + package_file
    pass_message = SPI_UPDATE_PASS_MSG
    fail_message = FPGA_UPDATE_FAIL_MSG
    timeout = 1000
    if 'minerva' in deviceObj.name:
        change_permission = 'chmod 777 ' + IOB_UPDATE_CMD
        execute(deviceObj, change_permission, timeout=timeout)
    output = execute(deviceObj, cmd, timeout=timeout)
    match1 = re.search(pass_message, output)
    match2 = re.search(fail_message, output, re.IGNORECASE)
    if match1:
        log.success("Successfully online_update_fpga")
        time.sleep(3)
    else:
        log.fail("Not found keyword: '%s'"%(pass_message))
        show_unit_info(device)
        raise testFailed("online_update_fpga failed")

def update_come_cpld(device, isUpgrade = True):
    log.debug('Entering procedure update_come_cpld with args : %s\n' %(str(locals())))
    err_count = 0
    imageObj = SwImage.getSwImage(SwImage.COME_CPLD)
    package_file = imageObj.newImage if isUpgrade else imageObj.oldImage
    package_file_path = imageObj.localImageDir
    package_name = package_file_path + '/' + package_file
    if not need_update_come_cpld(device, package_name):
        log.info("Already at version " + str(package_file) + ", need not update.")
        return
    online_update_come_cpld(device, package_name, isUpgrade)
    err_count += verify_come_cpld_version(device, package_name)
    if err_count:
        log.fail("verify_come_cpld_version failed")
        show_unit_info(device)
        raise testFailed("verify_come_cpld_version")
    else:
        log.success("COMe CPLD verification successful")

def need_update_come_cpld(device, package_name):
    log.debug('Entering procedure need_update_come_cpld with args : %s\n' %(str(locals())))
    err_count = 0
    err_count += verify_come_cpld_version(device, package_name)
    return True if err_count > 0 else False

def verify_come_cpld_version(device, package_name):
    log.debug('Entering procedure verify_come_cpld_version with args : %s\n' %(str(locals())))
    deviceObj = Device.getDeviceObject(device)
    err_count = 0
    cmd = 'source /usr/local/bin/openbmc-utils.sh'
    cmd1 = 'setup_gpio MUX_JTAG_SEL_1 GPIOF5 out 1'
    cmd2 = COME_CPLD_VERSION_VERIFY + ' ' + package_name 
    execute(deviceObj, cmd)
    execute(deviceObj, cmd1)
    output = execute(deviceObj, cmd2)
    log.info(output)
    match = re.search('Success', output)
    match1 = re.search('can\'t access file', output)
    if match1:
        raise testFailed("Can not find CPLD image for version verificaion")
    if not match:
        err_count += 1
    return err_count

def online_update_come_cpld(device, package_name, isUpgrade = True):
    log.debug('Entering procedure online_update_come_cpld with args : %s\n' %(str(locals())))
    deviceObj = Device.getDeviceObject(device)
    change_permission = 'chmod 777' + CPLD_UPDATE_CMD
    cmd = CPLD_UPDATE_CMD + ' COME ' + package_name
    if 'minipack3' in deviceObj.name:
        cmd = CPLD_UPDATE_CMD + ' -s COME -f %s sw' % (package_name)
    pass_message = COMe_UPDATE_PASS_MSG
    timeout = 1000
    execute(deviceObj, change_permission, timeout=timeout)
    output = execute(deviceObj, cmd, timeout=timeout)
    log.info(output)
    match1 = re.search(pass_message, output)
    if match1:
        check_cpu_alive(device, need_cd=True)
        log.success("Successfully online_update_COMe_cpld")
        time.sleep(3)
    else:
        log.fail("Not found keyword: '%s'"%(pass_message))
        show_unit_info(device)
        raise testFailed("online_update_COMe_cpld failed")

def run_eeprom(eeprom_path, device):
    log.debug('Entering procedure run_eeprom with args : %s\n' %(str(locals())))
    deviceObj = Device.getDeviceObject(device)
    err_count = 0
    cmd = "/mnt/data/fb_eeprom -b %s"%(eeprom_path)
    output = execute(deviceObj, cmd)
    parsed_output = parserOpenbmc.parse_eeprom_from_file(output)
    return parsed_output

def compare_util_and_eeprom_lite(device, util_dict, eeprom_dict, map_key_dict=UTIL_EEPROM_MAP_KEY, flag='None'):
    log.debug('Entering procedure compare_util_and_eeprom_lite with args : %s\n' %(str(locals())))
    outDict = parser()
    err_count = 0
    for key, val in util_dict.items():
        if key in map_key_dict:
            mapping_key = map_key_dict[key]
        else:
            mapping_key = re.sub(r'\s|-', '_', key).lower()

        if mapping_key == 'extended_mac_address_size':
            outDict[mapping_key] = hex(int(val))
        elif re.search(r'^N\/?-?A-?', val):
            outDict[mapping_key] = 'NA'
        else:
           outDict[mapping_key] = re.sub('-', '', val)
        outDict[mapping_key] = outDict[mapping_key].upper()
        log.info("%s: %s --> %s: %s"%(key, val, mapping_key, outDict[mapping_key]))

    ##### remove hypen from eeprom file value ######
    for key, val in eeprom_dict.items():
        eeprom_dict[key] = val.replace('-', '')

    ##### ignore 'magic_word & format_version' in comparison #####
    if 'magic_word' in eeprom_dict:
        del eeprom_dict['magic_word']

    if 'format_version' in eeprom_dict:
        del eeprom_dict['format_version']

    log.info("##### checking 'NA' format in eeprom output #####")
    for key, val in eeprom_dict.items():
        if re.search(r'^N\/?-?A-?', val) and val != 'NA':
            log.info("%s: %s --> %s: NA"%(key, val, key))
            eeprom_dict[key] = 'NA'
        eeprom_dict[key] = eeprom_dict[key].upper()

    log.info("##### comparing mapped weutil output with eeprom output #####")
    err_count += CommonLib.compare_input_dict_to_parsed(outDict, eeprom_dict, highlight_fail=True)
    if err_count:
        show_unit_info(device)
        raise testFailed("compare_util_and_eeprom")

