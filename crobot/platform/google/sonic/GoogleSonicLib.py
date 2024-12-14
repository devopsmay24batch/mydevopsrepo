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
import sys
import os
import re
import traceback
import CRobot
from time import sleep

workDir = CRobot.getWorkDir()
sys.path.append(workDir)
sys.path.append(os.path.join(workDir, 'common', 'commonlib'))
sys.path.append(os.path.join(workDir, 'platform', 'google'))
from crobot import Logger as log
try:
    from common.commonlib import CommonLib
    from common.commonlib import CommonKeywords
    from GoogleSonicVariable import *
    from GoogleCommonVariable import *
    import DeviceMgr
    from crobot.SwImage import SwImage
    from crobot.Decorator import logThis
except Exception as err:
    log.cprint(traceback.format_exc())

device = DeviceMgr.getDevice()
from SwImage import SwImage
from functools import partial
run_command = partial(CommonLib.run_command, deviceObj=device, prompt=device.promptDiagOS)

@logThis
def loginDevice():
    device.loginDiagOS()
    device.sendCmd('sudo su')


@logThis
def sonicDisconnect():
    return device.disconnect()


@logThis
def diagos_login_check():
    output = device.sendCmd('reboot', 'sonic login', timeout=240)
    sleep(10)
    if 'sonic login' in output:
        device.sendCmd('admin', 'Password:', timeout=15)
        device.sendCmd('pass', 'Login incorrect', timeout=15)
        device.sendCmd('admin', 'Password:', timeout=15)
        output = device.sendCmd('YourPaSsWoRd', 'admin@sonic', timeout=15)
        device.sendCmd('sudo su', 'root@sonic', timeout=15)
        for line in diagos_login_info:
            if line in output:
                continue
            else:
                raise RuntimeError('sonic login check test fail')
    else:
        raise RuntimeError('Cannot find sonic OS login line: "sonic login:"')


@logThis
def check_sonic_version(show_version_cmd, show_boot_cmd, uname_cmd):
    # show version
    output = device.executeCmd(show_version_cmd)
    for item in output.splitlines():
        if re.search('Serial Number:', item):
            item = item.strip()
            SerialNo_val = item.split(" ")
            SerialNo_val = SerialNo_val[-1]
        if re.search('Model Number:', item):
            item = item.strip()
            ModelNo_val = item.split(" ")
            ModelNo_val = ModelNo_val[-1]
        if re.search('Hardware Revision:', item):
            item = item.strip()
            HwRevision = item.split(" ")
            HwRevision = HwRevision[-1]

    log.info(f'From the show version cmd:\n sn= {SerialNo_val},\n mn = {ModelNo_val}, \n hw= {HwRevision} ')
    sleep(10)
    for line in output.splitlines():
        line = line.strip()
        match = re.search('SONiC Software Version', line)
        if match:
            log.success('Successfully find SONiC Software Version')
            break

    if not match:
        log.fail('can not find sonic version!')
        raise RuntimeError('can not find sonic version!')

    expected_version = SwImage.getSwImage(SwImage.BRIXIA_SONIC).newVersion
    exp_version = expected_version.replace('-OS-', '.')

    if exp_version not in line:
        raise RuntimeError('current version is not match the expected version {}!'.format(exp_version))
    else:
        log.success('check sonic version %s successfully.' % (exp_version))
    # show boot
    output = device.executeCmd(show_boot_cmd)
    for line in output.splitlines():
        line = line.strip()
        match = re.search('Current', line)
        if match:
            log.success('Successfully find SONiC Software Version in "show boot" cmd')
            break
    if not match:
        log.fail('can not find sonic version in "show boot" cmd!')
        raise RuntimeError('can not find sonic version in "show boot" cmd!')

    log.info(f'expected_version:{expected_version}, line :{line}')
    if expected_version not in line:
        raise RuntimeError(
            '"show boot" : current version is not match the expected version {}!'.format(expected_version))
    else:
        log.success('"show boot" : check sonic version %s successfully.' % (expected_version))
    # uname -v
    output = device.executeCmd(uname_cmd)
    if uname_value not in output:
        raise RuntimeError('"uname -v" : version is not match the expected value{}!'.format(uname_value))
    else:
        log.success('"uname -v"check sonic version %s successfully.' % (uname_value))
    # cls_diag_path cmd
    device.executeCmd(cls_diag_path)
    output = device.executeCmd(sys_info_test_cmd)
    for line in output.splitlines():
        line = line.strip()
        match = re.search('SONiC Software Version', line)
        if match:
            log.success('Successfully find SONiC Software Version')
            break

    if not match:
        log.fail('can not find sonic version!')
        raise RuntimeError('can not find sonic version!')

    if exp_version not in line:
        raise RuntimeError('sys info test , current version is not match the expected version {}!'.format(exp_version))
    else:
        log.success('sys-info-test,check sonic version %s successfully.' % (exp_version))
    # check serail no, model no, Hw revision are same with version cmd
    output = device.executeCmd(eeprom_cmd)
    for item in output.splitlines():
        if re.match('sn:', item):
            item = item.strip()
            baseboard_SerialNo_val = item.split(" ")
            baseboard_SerialNo_val = baseboard_SerialNo_val[-1]
        if re.match('pn:', item):
            item = item.strip()
            baseboard_ModelNo_val = item.split(" ")
            baseboard_ModelNo_val = baseboard_ModelNo_val[-1]
        if re.match('hw_revision:', item):
            item = item.strip()
            baseboard_HwRevision = item.split(" ")
            baseboard_HwRevision = baseboard_HwRevision[-1]

    log.info(
        f'From the eeprom cmd:\n sn= {baseboard_SerialNo_val},\n mn = {baseboard_ModelNo_val}, \n hw= {baseboard_HwRevision} ')
    sleep(10)

    if baseboard_SerialNo_val not in SerialNo_val:
        raise RuntimeError(f'The serial number does not match with eeprom baseboard value: {baseboard_SerialNo_val}')
    else:
        log.success(f'The serail no. match successfully with baseboard value: {baseboard_SerialNo_val}')
    if baseboard_ModelNo_val not in ModelNo_val:
        raise RuntimeError(f'The model no. does not match with eeprom baseboard value: {baseboard_ModelNo_val}')
    else:
        log.success(f'The  model no. match successfully with baseboard value: {baseboard_ModelNo_val}')
    if baseboard_HwRevision not in HwRevision:
        raise RuntimeError(f'The HwRevision does not match with eeprom baseboard value: {baseboard_HwRevision}')
    else:
        log.success(f'The  HwRevision match successfully with baseboard value: {baseboard_HwRevision}')


@logThis
def sonic_booting_info_check(coreboot_release_date):
    """
    reboot sonic and check booting info!
    """

    sw_issue_flag = False
    sw_issue_message = ""
    clock_issue_flag = False
    clock_issue_message = ""

    output = device.sendCmd('reboot', 'sonic login', timeout=240)
    device.loginToDiagOS()
    gotoSuperUser()
    if 'error' in output or 'fail' in output:
        sw_issue_flag = True
        sw_issue_message = 'A known SW Issue occured.\nSonic booting info has error or fail string:\n' + "".join(
            re.findall(r'.*?fail.*|.*?error.*', output))
        log.fail("SW issue occured.\nSonic booting info has error or fail.")
    output = device.executeCmd('date')
    if 'error' in output or 'fail' in output:
        raise RuntimeError('time output have error or fail strings')

    output = device.executeCmd('hwclock')
    if 'fail' in output:
        clock_issue_flag = True
        clock_issue_message = "Error in display hwclock command."
        log.fail(clock_issue_message)

    bios = device.executeCmd('dmidecode -t bios')
    if not clock_issue_flag:
        if re.search('Vendor: coreboot', bios):
            if coreboot_release_date in output:
                log.success('hwclock date is reset to coreboot release date')
            else:
                raise RuntimeError('hwclock date is not reset to coreboot release date')
        else:
            log.success('BIOS is linuxboot , date does not set to release date')

    if sw_issue_flag or clock_issue_flag:
        raise Exception(sw_issue_message + clock_issue_message)


@logThis
def check_dependent_software(diag_SW, sdk_SW):
    gotoSuperUser()
    run_command("cd /home/admin", prompt="root@sonic:.*", timeout=5)
    output = device.executeCmd('ls -la')
    if diag_SW in output and sdk_SW in output:
        log.success('The required dependent software - diag and sdk are present in DUT')
    else:
        raise RuntimeError('DIAG and SDK Sw are not present in the sonic test unit')


@logThis
def check_software_version():
    output = device.executeCmd('show platform firmware')
    if 'error' in output or 'fail' in output:
        raise RuntimeError('platfrom fw output have error or fail strings')

    # sw and bios version check
    sonic_fw_version = device.executeCmd(show_version_cmd)
    bios_fw_version = device.executeCmd(bios_cmd)
    expect_sonic_version = SwImage.getSwImage(SwImage.BRIXIA_SONIC).newVersion
    expect_sonic_version = expect_sonic_version.replace('-OS-', '.')
    expect_bios_version = CommonLib.get_swinfo_dict("BRIXIA_SONIC")
    expect_bios_version = expect_bios_version.get("BIOS").get("newVersion", "")
    log.info(f'expect_bios_version: {expect_bios_version}')
    if expect_sonic_version in sonic_fw_version:
        log.success(f'Expeced sonic version \'{expect_sonic_version}\' present in the dut')
    else:
        raise RuntimeError(f'Expeced sonic version \'{expect_sonic_version}\' not present in dut')
    if expect_bios_version in bios_fw_version:
        log.success(f'Expeced bios version\'{expect_bios_version}\' present in the dut')
    else:
        raise RuntimeError(f'Expeced bios version\'{expect_bios_version}\' not present in dut')

    # Diag Fw dependent check
    device.executeCmd(f'dpkg -i {diag_SW}')
    if 'error' in output or 'fail' in output:
        raise RuntimeError('diag package not installed')

    device.executeCmd('cd /usr/local/cls_diag/')
    output = device.executeCmd('./install -p brixia32')
    if 'error' in output or 'fail' in output:
        raise RuntimeError('error or fail string found during brixia32 installation')

    device.sendCmd('reboot', 'sonic login', timeout=240)
    device.loginToDiagOS()
    gotoSuperUser()
    device.executeCmd('cd /usr/local/cls_diag/bin')
    diag_fw_version = device.executeCmd('./cel-sysinfo-test --all')
    expect_diag_version = CommonLib.get_swinfo_dict("BRIXIA_SONIC")
    expect_diag_version = expect_diag_version.get("DIAG").get("newVersion", "")
    for line in diag_fw_version.splitlines():
        line = line.strip()
        match = re.search('Diag Version:', line)
        if match:
            log.success('Successfully find Diag Software Version')
            break

    if not match:
        log.fail('can not find diag version!')
        raise RuntimeError('can not find diag version!')
    if expect_diag_version in line:
        log.success(f'expected diag version \'{expect_diag_version}\' present in the dut')
    else:
        raise RuntimeError(f'expected diag version \'{expect_diag_version}\' not present in the dut')

    # SDk- libyaml check
    device.executeCmd('cd /home/admin/')
    output = device.executeCmd('dpkg -L libyaml-0-2:amd64')
    CommonKeywords.should_match_paired_regexp_list(output, libyaml_output)

    # sdk Fw dependent check
    install_sdk = device.executeCmd(f'dpkg -i {sdk_SW}')
    if 'error' in output or 'fail' in output:
        raise RuntimeError('diag package not installed')

    device.executeCmd('cd /usr/local/cls_sdk/')
    module = device.executeCmd('/etc/init.d/opennsl-modules stop')
    module_output = ['Unload OpenNSL kernel modules... done.']
    CommonKeywords.should_match_paired_regexp_list(module, module_output)

    autoload = device.executeCmd('./auto_load_user.sh')
    CommonKeywords.should_match_paired_regexp_list(autoload, autoload_output)

    device.sendCmd('./bcm.user -y brixiaV2-TH4G-256x1x100.yml', 'BCM.0>', timeout=10)
    bcm_output = run_command('version', prompt="BCM.0>", timeout=5)
    if bcm_sdk_version not in bcm_output:
        device.sendCmd('quit', 'root@sonic:/usr/local/cls_sdk', timeout=5)
        raise Exception("Error in reading SDK version.")
    device.sendCmd('quit', 'root@sonic:/usr/local/cls_sdk', timeout=5)

    # COM-E CPLD.
    come_fw_version = device.executeCmd('cat /sys/devices/platform/come_cpld/version')
    CommonKeywords.should_match_paired_regexp_list(come_fw_version, come_cpld_version)

    # current MMC CPLD.
    major = device.executeCmd('cat /sys/devices/platform/mmcpld/mmc_reg.3.auto/version_major')
    CommonKeywords.should_match_paired_regexp_list(major, mmc_major_version)

    minor = device.executeCmd('cat /sys/devices/platform/mmcpld/mmc_reg.3.auto/version_minor')
    CommonKeywords.should_match_paired_regexp_list(minor, mmc_minor_version)

    month = device.executeCmd('cat /sys/devices/platform/mmcpld/mmc_reg.3.auto/version_month')
    CommonKeywords.should_match_paired_regexp_list(month, mmc_month_version)

    date = device.executeCmd('cat /sys/devices/platform/mmcpld/mmc_reg.3.auto/version_date')
    CommonKeywords.should_match_paired_regexp_list(date, mmc_date_version)

    # currect FPGA.
    fpga_major = device.executeCmd('cat /sys/devices/gfpga-platform/majorrevision')
    CommonKeywords.should_match_paired_regexp_list(fpga_major, fpga_major_version)

    fpga_minor = device.executeCmd('cat /sys/devices/gfpga-platform/minorrevision')
    CommonKeywords.should_match_paired_regexp_list(fpga_minor, fpga_minor_version)


@logThis
def COMe_CPLD_register_access():
    #Powercycle device
    device.sendCmd('echo 0x4449454a > /sys/devices/gfpga-platform/board_powercycle', 'sonic login', timeout=220)
    device.loginToDiagOS()
    gotoSuperUser()

    device.executeCmd(tool_path)
    cpld_val_1 = device.executeCmd('./lpc_cpld_x64_64 blu r 0xa1e1')
    cat_come_val = device.executeCmd('cat /sys/devices/platform/come_cpld/scratch')
    condition1 = "0xde" not in cpld_val_1 or "0xde" not in cat_come_val #Should be False
    if condition1:
        raise RuntimeError("Error in reading CPLD scratch default value.\nIt's not 0xde.")
    else:
        log.success('The COMe cpld value has no errors.')

    device.executeCmd('echo 0xc0 > /sys/devices/platform/come_cpld/scratch')
    cat_come_val_1 = device.executeCmd('cat /sys/devices/platform/come_cpld/scratch')

    device.executeCmd('echo 0x83 > /sys/devices/platform/come_cpld/scratch')
    cat_come_val_2 = device.executeCmd('cat /sys/devices/platform/come_cpld/scratch')

    device.executeCmd('echo 0xcd > /sys/devices/platform/come_cpld/scratch')
    cat_come_val_3 = device.executeCmd('cat /sys/devices/platform/come_cpld/scratch')

    cpld_val_2 = device.executeCmd('./lpc_cpld_x64_64 blu r 0xa1e1')
    if 'error' in cpld_val_2 or 'Fail' in cpld_val_2:
        raise RuntimeError('Error string in the output of \'./lpc_cpld_x64_64 blu r 0xa1e1\' cli cmd')
    else:
        log.success('The COMe cpld value has no errors')

    if '0xc0' not in cat_come_val_1:
        raise RuntimeError('The set value \'0xc0\' is not present in come_cpld scratch')
    else:
        log.success('The value \'0xc0\' set successfully')
    if '0x83' not in cat_come_val_2:
        raise RuntimeError('The set value \'0x83\' is not present in come_cpld scratch')
    else:
        log.success('The value \'0x83\' set successfully')
    if '0xcd' not in cat_come_val_3:
        raise RuntimeError('The set value \'0xcd\' is not present in come_cpld scratch')
    else:
        log.success('The value \'0xcd\' set successfully')

@logThis
def MMc_CPLD_register_access():
    mmc_scratch_location = "/sys/devices/platform/mmcpld/mmc_reg.3.auto/scratch"
    read_mmc_cmd = "cat " + mmc_scratch_location


    MMc_val= device.executeCmd('./lpc_cpld_x64_64 blu r 0xa101')
    cat_mmc_val = device.executeCmd(read_mmc_cmd)
    if "0xde" not in cat_mmc_val:
        raise RuntimeError("Error in reading MMC CPLD default value.\nIt's not 0xde.")
    else:
        log.success('The mmc cpld value has no errors.')

    device.executeCmd('echo 0xbb > ' + mmc_scratch_location)
    cat_mmc_val_1 = device.executeCmd(read_mmc_cmd)

    device.executeCmd('echo 0x3c > ' + mmc_scratch_location)
    cat_mmc_val_2 =device.executeCmd(read_mmc_cmd)

    device.executeCmd('echo 0xcd > ' + mmc_scratch_location)
    cat_mmc_val_3 = device.executeCmd(read_mmc_cmd)

    MMc_val= run_command('./lpc_cpld_x64_64 blu r 0xa101', prompt='root@sonic:', timeout=5)
    if "0xcd" not in MMc_val:
        raise RuntimeError("Error in reading MMC CPLD latest value.\nIt's not 0xcd.")
    else:
        log.success('The mmc cpld value is latest.')

    if 'error' in MMc_val or 'Fail' in MMc_val:
        raise RuntimeError('Error string in the output of \'./lpc_cpld_x64_64 blu r 0xa101\' cli cmd')
    else:
        log.success('The mmc cpld value has no errors')

    if '0xbb' not in cat_mmc_val_1:
        raise RuntimeError('The set value \'0xbb\' is not present in mmc_cpld scratch')
    else:
        log.success('The value \'0xbb\' set successfully')
    if '0x3c' not in cat_mmc_val_2:
        raise RuntimeError('The set value \'0x3c\' is not present in mmc_cpld scratch')
    else:
        log.success('The value \'0x3c\' set successfully')
    if '0xcd' not in cat_mmc_val_3:
        raise RuntimeError('The set value \'0xcd\' is not present in mmc_cpld scratch')
    else:
        log.success('The value \'0xcd\' set successfully')

@logThis
def FPGA_register_access():
    fpga_location = "/sys/devices/gfpga-platform/scratch"
    read_fpga_cmd = "cat " + fpga_location


    fpga_val = device.executeCmd(read_fpga_cmd)
    if "0" not in fpga_val:
        raise RuntimeError('Error in reading default FPGA scratch default value.\n It should be 0.')
    else:
        log.success('FPGA scratch default value correct.')

    device.executeCmd('echo 0xff > ' + fpga_location)
    cat_fpga_val_1 = device.executeCmd(read_fpga_cmd)

    device.executeCmd('echo 0xCC1100DE > ' + fpga_location)
    cat_fpga_val_2 = device.executeCmd(read_fpga_cmd)

    device.executeCmd('echo 0xC001C0DE > ' + fpga_location)
    cat_fpga_val_3 = device.executeCmd(read_fpga_cmd)


    if 'error' in fpga_val or 'Fail' in fpga_val:
        raise RuntimeError('Error string in the output of fpga register')
    else:
        log.success('fpga register cmd ran successfully')

    if '255' not in cat_fpga_val_1:
        raise RuntimeError('The set value \'0xff\' is not present in fpga register')
    else:
        log.success('The value \'0xff\' set in fpga successfully')

    if '3423666398' not in cat_fpga_val_2:
        raise RuntimeError('The set value \'0xCC1100DE\'is not present in fpga register')
    else:
        log.success('The value \'0xCC1100DE\' set in fpga successfully')

    if '3221340382' not in cat_fpga_val_3:
        raise RuntimeError('The set value \'0xC001C0DE\'is not present in fpga register')
    else:
        log.success('The value \'0xC001C0DE\' set in fpga successfully')


@logThis
def check_platform():
    output = device.executeCmd('show platform summary')
    if platform in output:
        log.success(f'The platform {platform} is present')
    else:
        raise RuntimeError('The platform is incorrect')
    if ASIC in output:
        log.success(f'The ASIC chipset is correct {ASIC}')
    else:
        raise RuntimeError('The ASIC chipset is incorrect')
    if ASIC_Count in output:
        log.success("ASIC count is correct")
    else:
        raise RuntimeError('The ASIC Count is incorrect')
    if HwSKU in output:
        log.success(f'The sku {HwSKU} is correct')
    else:
        raise RuntimeError('The hwsku is incorrect')

@logThis
def check_cpu_info():
    output = device.executeCmd('cat /proc/cpuinfo')
    output_1 = device.executeCmd('show processes cpu')
    if cpu_info in output:
        log.success('The cpu info in the output is correct')
    else:
        raise RuntimeError('The cpu info is not correct')
    if 'error' in output_1 or 'Fail' in output_1:
        raise RuntimeError('The \'show processes cpu\' cmd have error string')


@logThis
def check_memory_info():
    output = device.executeCmd('cat /proc/meminfo')
    output_1 = device.executeCmd('show processes memory')
    pattern =['MemTotal: .*kB', 'MemFree:.*kB', 'MemAvailable:.*kB']
    if 'error' in output or 'Fail' in output:
        raise RuntimeError('error string present in memory info output')

    if 'error' in output_1 or 'Fail' in output_1:
        raise RuntimeError('error string present in \'show processes memory\' output')

    for item in pattern:
        if re.search(item, output):
            log.success('The required meminfo is present')
        else:
            raise RuntimeError(f'The string\'{item}\' not present in the meminfo details')

@logThis
def scan_i2c_device():
    output = device.executeCmd('i2cdetect -l')
    CommonKeywords.should_match_paired_regexp_list(output, i2c_l_pattern)
    log.success('I2cdetect list is shown correctly')
    output_1 = device.executeCmd('i2cdetect -y 0')
    log.success('I2cdetect list is shown correctly')
    CommonKeywords.should_match_paired_regexp_list(output_1, i2c_y0_pattern)
    output_2 = device.executeCmd('i2cdetect -y 1')
    CommonKeywords.should_match_paired_regexp_list(output_2, i2c_y1_pattern)
    log.success('I2cdetect list is shown correctly')


@logThis
def scan_pcie_device():
    output = device.executeCmd('lspci')
    for item in pcie_log:
        if re.search(item, output):
            log.success(f'required log \'{item}\'  present in lspci')
        else:
            raise RuntimeError(f'The string\'{item}\' not present in lspci')
    #TH4 PCI Properties
    output1= device.executeCmd('lspci -d 14e4:b996 -v')
    if re.search(th4_pci, output1):
        log.success(f'The Value {th4_pci} is present')
    else:
        raise RuntimeError(f'The value {th4_pci} is not present')

    output2 = device.executeCmd('lspci -d 14e4:b996 -vv | grep LnkSta')
    if re.search(th4_pci_speed_width, output2):
        log.success(f'The Value {th4_pci_speed_width} is present')
    else:
        raise RuntimeError(f'The value {th4_pci_speed_width} is not present')

    #GFPGA PCI Properties
    output3 = device.executeCmd('lspci -d 1ae0:0065 -v')
    if re.search(gfpga_pci, output3):
        log.success(f'The Value {gfpga_pci} is present')
    else:
        raise RuntimeError(f'The value {gfpga_pci} is not present')

    output4 = device.executeCmd('lspci -d 1ae0:0065 -vv | grep LnkSta')
    if re.search(gfpga_pci_speed_width, output4):
        log.success(f'The Value {gfpga_pci_speed_width} is present')
    else:
        raise RuntimeError(f'The value {gfpga_pci_speed_width} is not present')


@logThis
def check_storage_device():
    output= device.executeCmd('fdisk -l')
    if re.search(ssd , output):
        log.success("The ssd storage device is present in the unit")
    else:
        raise RuntimeError('The ssd storage device is not available')
    if re.search(msd, output):
        log.success("The msd storage device is present in the unit")
    else:
        raise RuntimeError('The msd storage device is not available')

@logThis
def check_mgmt_port():
    output1 = device.executeCmd('ifconfig -a')
    output2 = device.executeCmd('ifconfig')
    output3 = device.executeCmd('show ip interfaces')
    if 'Fail' in output1:
        raise RuntimeError('ifconfig -a : cli have error string in the output')
    else:
        log.success('ifconfig -a cmd succuessfully ran')
    if 'Fail' in output2:
        raise RuntimeError('ifconfig: cli have error string in the output')
    else:
        log.success('ifconfig cmd succuessfully ran')
    if 'Fail' in output3:
        raise RuntimeError('show ip interfaces: cli have error string in the output')
    else:
        log.success('show ip interfaces:cmd succuessfully ran')
    if re.search('eth0 .* up/up.*', output3):
        log.success("eth0 is active")
    else:
        raise RuntimeError('eth0 is not active')
    if re.search("eth1.*up/up", output3):
        raise RuntimeError('eth1 is active by default')
    else:
        log.success('eth1 is not active by default')


@logThis
def tlv_eeprom_from_diag_cmd():
    device.executeCmd('cd /usr/local/cls_diag/bin')
    diag_output1 = device.executeCmd('./cel-eeprom-test -r -d all -t tlv')
    diag_output2 = device.executeCmd('./cel-eeprom-test --dump -d all -t tlv')
    if 'error' in diag_output1 or 'Fail' in diag_output1:
        raise RuntimeError('error string in diag tlv eeprom cmd')
    else:
        log.success('diag eeprom info is present')
    if 'error' in diag_output2 or 'Fail' in diag_output2:
        raise RuntimeError('error string in diag tlv eeprom cmd')
    else:
        log.success('diag eeprom info is present')

@logThis
def tlv_eeprom_from_sonic_cmd():
    come1 = device.executeCmd('hd /sys/bus/i2c/devices/1-0050/eeprom-ro')
    come2 = device.executeCmd('hd /sys/bus/i2c/devices/1-0051/eeprom-ro')
    baseboard = device.executeCmd('hd /sys/bus/i2c/devices/19-0051/eeprom-ro')
    print('The basborad value is ',baseboard)
    switchboard = device.executeCmd('hd /sys/bus/i2c/devices/i2c-10001/10001-0050/eeprom-ro')
    fan1 = device.executeCmd('hd /sys/bus/i2c/devices/12-0050/eeprom-ro')
    fan2 =device.executeCmd('hd /sys/bus/i2c/devices/13-0050/eeprom-ro')
    fan3 = device.executeCmd('hd /sys/bus/i2c/devices/14-0050/eeprom-ro')
    fan4 = device.executeCmd('hd /sys/bus/i2c/devices/15-0050/eeprom-ro')

    if 'error' in come1 or 'error' in come2:
        raise RuntimeError('error string in come1,2')
    else:
        log.success('come1 and come2 cmd ran')

    if 'error' in baseboard or 'error' in switchboard:
        raise RuntimeError('error string in baseborad and switchboard sonic cmd')
    else:
        log.success('baseboard and switchboard sonic cmd ran successfully')

    if 'error' in fan1 or 'error' in fan2 or 'error' in fan3 or 'error' in fan4:
        raise RuntimeError('fan sonic cmd have error string')
    else:
        log.success('sonic fan cmd ran successfully')
    #compare the eeprom value
    diag_output2 = device.executeCmd('./cel-eeprom-test --dump -d all -t tlv')
    print('The diag_output2 is  ',diag_output2)
    if re.search(come1, diag_output2):
        log.success("sonic and diag cmd value for come1 is same")
    else:
        raise RuntimeError("sonic and diag cmd value for come1 are different!")
    if re.search(come2, diag_output2):
        log.success("sonic and diag cmd value for come2 is same")
    else:
        raise RuntimeError("sonic and diag cmd value for come2 are different!")

    baseboard=baseboard.splitlines()
    new=diag_output2.splitlines()
    if any(line in baseboard for line in new):
        log.success('diag and sonic output are same for baseboard')
    else:
        raise RuntimeError("sonic and diag cmd value for baseboard are different!")

    if re.search(switchboard, diag_output2):
        log.success('diag and sonic output are same for switchboard')
    else:
        raise RuntimeError("sonic and diag cmd value for switchboard are different!")

    fan1 = fan1.splitlines()
    fan2 = fan2.splitlines()
    fan3 = fan3.splitlines()
    fan4 = fan4.splitlines()
    diag_output2 = diag_output2.splitlines()

    if any(line in fan1 for line in diag_output2):
        log.success('diag and sonic output are same for fan1')
    else:
        raise RuntimeError("sonic and diag cmd value for switchboard are fan1!")
    
    if any(line in fan2 for line in diag_output2):
        log.success('diag and sonic output are same for fan2')
    else:
        raise RuntimeError("sonic and diag cmd value for switchboard are fan2!")

    if any(line in fan3 for line in diag_output2):
        log.success('diag and sonic output are same for fan3')
    else:
        raise RuntimeError("sonic and diag cmd value for switchboard are fan3!")

    if any(line in fan4 for line in diag_output2):
        log.success('diag and sonic output are same for fan4')
    else:
        raise RuntimeError("sonic and diag cmd value for switchboard are fan4!")

@logThis
def erase_and_program_tlv_eeprom():
    device.executeCmd('cd /home/admin/')
    output=device.executeCmd('ls -la')
    if re.search(file1, output):
        log.success(f"{file1} present in the test unit")
        device.sendCmd('chmod 777 '+file1)
    else:
        scp(file1)
        device.sendCmd('chmod 777 '+file1)

    if re.search(file2, output):
        log.success(f"{file2} present in the test unit")
        device.sendCmd('chmod 777 '+file2)
    else:
        scp(file2)
        device.sendCmd('chmod 777 '+file2)

    if re.search(file3, output):
        log.success(f"{file3} present in the test unit")
        device.sendCmd('chmod 777 '+file3)
    else:
        scp(file3)
        device.sendCmd('chmod 777 '+file3)

    device.executeCmd(r"sed -i -e 's/\r$//'  eeprom_test_01.sh")
    device.executeCmd(r"sed -i -e 's/\r$//'  eeprom_test_02.sh")
    device.executeCmd(r"sed -i -e 's/\r$//'  eeprom_test_03.sh")
    erase_write = ""
    erase_write = device.sendCmd('echo -e  "Continue\nDVT\n" | ./eeprom_test_01.sh','EEPROM Device: COMe', timeout ='5')
    erase_write = device.read_until_regexp('root@sonic', timeout='120')
    erase_write = erase_write.splitlines()
    if any(line in erase_write for line in f1_come1_pattern):
        log.success('come1 write is successful')
    else:
        raise RuntimeError('come1 write Failed!')

    if any(line in erase_write for line in f1_come2_pattern):
        log.success('come2 write is successful')
    else:
        raise RuntimeError('come2 write Failed!')
 
    if any(line in erase_write for line in f1_baseboard_pattern):
        log.success('baseboard write is successful')
    else:
        raise RuntimeError('baseboard write Failed!')
 
    if any(line in erase_write for line in f1_switchboard_pattern):
        log.success('switchboard write is successful')
    else:
        raise RuntimeError('switchboard write Failed!')

    if any(line in erase_write for line in f1_fan1_pattern):
        log.success('fan1 write is successful')
    else:
        raise RuntimeError('fan1 write Failed!')
 
    if any(line in erase_write for line in f1_fan2_pattern):
        log.success('fan2 write is successful')
    else:
        raise RuntimeError('fan2 write Failed!')

    if any(line in erase_write for line in f1_fan3_pattern):
        log.success('fan3 write is successful')
    else:
        raise RuntimeError('fan3 write Failed!')
   
    erase_write = device.sendCmd('echo -e  "Continue\nDVT\n" | ./eeprom_test_02.sh','EEPROM Device: COMe', timeout ='5')
    erase_write = device.read_until_regexp('root@sonic', timeout='120')
    
    erase_write = erase_write.splitlines()
    if any(line in erase_write for line in f2_come1_pattern):
        log.success('come1 write is successful')
    else:
        raise RuntimeError('come1 write Failed!')

    if any(line in erase_write for line in f2_come2_pattern):
        log.success('come2 write is successful')
    else:
        raise RuntimeError('come2 write Failed!')

    if any(line in erase_write for line in f2_baseboard_pattern):
        log.success('baseboard write is successful')
    else:
        raise RuntimeError('baseboard write Failed!')

    if any(line in erase_write for line in f2_switchboard_pattern):
        log.success('switchboard write is successful')
    else:
        raise RuntimeError('switchboard write Failed!')

    if any(line in erase_write for line in f2_fan1_pattern):
        log.success('fan1 write is successful')
    else:
        raise RuntimeError('fan1 write Failed!')

    if any(line in erase_write for line in f2_fan2_pattern):
        log.success('fan2 write is successful')
    else:
        raise RuntimeError('fan2 write Failed!')

    if any(line in erase_write for line in f2_fan3_pattern):
        log.success('fan3 write is successful')
    else:
        raise RuntimeError('fan3 write Failed!')


    erase_write = device.sendCmd('echo -e  "Continue\nDVT\n" | ./eeprom_test_03.sh','EEPROM Device: COMe', timeout ='5')
    erase_write = device.read_until_regexp('root@sonic', timeout='120')
    erase_write = erase_write.splitlines()
    if any(line in erase_write for line in f3_come1_pattern):
        log.success('come1 write is successful')
    else:
        raise RuntimeError('come1 write Failed!')

    if any(line in erase_write for line in f3_come2_pattern):
        log.success('come2 write is successful')
    else:
        raise RuntimeError('come2 write Failed!')

    if any(line in erase_write for line in f3_baseboard_pattern):
        log.success('baseboard write is successful')
    else:
        raise RuntimeError('baseboard write Failed!')

    if any(line in erase_write for line in f3_switchboard_pattern):
        log.success('switchboard write is successful')
    else:
        raise RuntimeError('switchboard write Failed!')

    if any(line in erase_write for line in f3_fan1_pattern):
        log.success('fan1 write is successful')
    else:
        raise RuntimeError('fan1 write Failed!')

    if any(line in erase_write for line in f3_fan2_pattern):
        log.success('fan2 write is successful')
    else:
        raise RuntimeError('fan2 write Failed!')

    if any(line in erase_write for line in f3_fan3_pattern):
        log.success('fan3 write is successful')
    else:
        raise RuntimeError('fan3 write Failed!')

		
@logThis
def tlv_eeprom_failover_check():
    diagos_login_check()
    tlv_eeprom_from_diag_cmd()
    tlv_eeprom_from_sonic_cmd()
@logThis
def ScanAllDrivers():
    device.sendMsg('reboot \n')
    device.read_until_regexp('.*Debian GNU/Linux 10 sonic ttyS0',timeout=1000)

@logThis
def CheckAllDriverStatus():
    diagos_login_check()
    device.sendMsg('fdisk -l \n')
    device.read_until_regexp('.*512 bytes',timeout=100)
    device.sendMsg('i2cdetect -y 0 \n')
    device.read_until_regexp('70:.*',timeout=10)
    device.sendMsg('i2cdetect -y 0 \n')
    device.read_until_regexp('70:.*',timeout=10)

@logThis
def WatchDogResetStressTest():
    device.sendMsg('service gfpga-watchdog status \n')
    device.read_until_regexp('.*(END)',timeout=10)
    for i in range(1):
        device.sendMsg(Const.KEY_CTRL_Z)
        try:
            d1=device.read_until_regexp('#', timeout=15)
            break
        except Exception:
            continue
    #device.sendCmd('kill -9 2260','root@sonic',timeout=15)




@logThis
def check_OSFPport_eeprom_info():
#    diagos_login_check()
    output = run_command('cat /sys/devices/gfpga-platform/osfp_pd_l',prompt='root@sonic')
    if re.search('\\b0\\b', output):
        log.success("All OSFP ports are connected in the test unit")
    else:
        raise RuntimeError("All OSFP ports are not connected in the test unit")

    device.executeCmd('i2c_devs=/sys/bus/i2c/devices')
    run_command('for i in {10101..10132}; do',prompt = '>')
    run_command('vname=$(cat $i2c_devs/$i-0050/vendor_name);',prompt = '>')
    run_command('vpart=$(cat $i2c_devs/$i-0050/vendor_part);',prompt = '>')
    run_command('temp=$(cat $i2c_devs/$i-0050/temp);',prompt = '>')
    device.sendCmd('echo -e "i2c-$i\\n  Vendor:$vname\\n  PN:$vpart\\n  SN:$vser\\n  Temp:$temp";',promptStr = '>')
    output1=run_command('done',prompt='root@sonic')

    portlist = ['i2c-10101','i2c-10102','i2c-10103','i2c-10104','i2c-10105','i2c-10106','i2c-10107','i2c-10108','i2c-10109','i2c-10110',
            'i2c-10111','i2c-10112','i2c-10113','i2c-10114','i2c-10115','i2c-10116','i2c-10117','i2c-10118','i2c-10119','i2c-10120',
            'i2c-10121','i2c-10122','i2c-10123','i2c-10124','i2c-10125','i2c-10126','i2c-10127','i2c-10128','i2c-10129','i2c-10130',
            'i2c-10131','i2c-10132']

    for item in portlist:
        if item in output1:
            CommonKeywords.should_match_paired_regexp_list(output1, osfp_info)
        else:
            raise RuntimeError(f'Port {item} not connected to the unit')
    log.success('OSPF EEprom passed for the following list')
    print([x for x in portlist])
    output2=device.executeCmd('cat /sys/devices/gfpga-platform/osfp_pd_l')
    if re.search('\\b0\\b', output2):
        log.success("All OSFP ports are connected status after eeprom read")
    else:
        raise RuntimeError("All OSFP ports are not connected status after eeprom read")

@logThis
def check_SFPplus_port_eeprom_info():
    output1 = run_command('cat /sys/devices/gfpga-platform/sfp_plus_32_pd_l',prompt='root@sonic')
    output2 = run_command('cat /sys/devices/gfpga-platform/sfp_plus_33_pd_l',prompt='root@sonic')
    run_command('i2c_devs=/sys/bus/i2c/devices',prompt='root@sonic')
    run_command('for i in {10133..10134}; do',prompt='>')
    device.sendCmd('echo "i2c-$i";',promptStr='>')
    run_command('hd $i2c_devs/$i-0050/eeprom-rw;',prompt='>')
    run_command('[[ -e $i2c_devs/$i-0051/eeprom-rw ]] && hd $i2c_devs/$i-0051/eeprom-rw;',prompt='>')
    output3= run_command('done',prompt='root@sonic')

    output4 = run_command('cat /sys/devices/gfpga-platform/sfp_plus_32_pd_l',prompt='root@sonic')
    output5 = run_command('cat /sys/devices/gfpga-platform/sfp_plus_33_pd_l',prompt='root@sonic')

    if re.search('\\b0\\b', output1) and  re.search('\\b0\\b', output2):
        log.success("All SFP+ ports are connected status before eeprom read")
    else:
        raise RuntimeError("All SFP+ ports are not connected status before eeprom read")

    if 'error' in output3:
        raise RuntimeError('pysical port 33,34 is not connected to sfp+ dac cable.\nsfp+ module is required for eeprom info')
    else:
        log.success('Passed: SFP+ modules is present , no error in eeprom output')

    if re.search('\\b0\\b', output3) and  re.search('\\b0\\b', output4):
        log.success("After eeprom read the sfp+ port status is correct")
    else:
        raise RuntimeError("After eeprom read the sfp+ port status is wrong")

@logThis
def temp_sensor_check():
    env = run_command('show environment', prompt='root@sonic')
    if re.search('coretemp', env) and re.search('tmp05', env) and re.search('I2Cool Inlet Temp', env) and ('error' not in env):
        log.success("All sensors are present in the 'show environment' cmd")
    else:
        raise RunTimeError("Not all sensors are present inthe 'show environment' cmd")

    core = run_command('sensors coretemp-*', prompt='root@sonic')
    tmp05 = run_command('sensors tmp05-*' ,prompt='root@sonic')
    i2cool = run_command('sensors max31725-i2c-10002-5c' ,prompt='root@sonic' )
    run_command('count=$(cat /sys/devices/gfpga-platform/th_max_temp)', prompt='root@sonic')
    th4 = run_command("perl -e '$temp=356.30734 - 0.047468 * int($ARGV[0]); print \"$temp C\n\"' $count", prompt='root@sonic')

    pattern = r'([^+-]?\d+\.\d+)\s?'
    for lines in core.splitlines():
        temp = re.findall(pattern,lines)

        if temp:
            for i in range(0, len(temp)):
                temp[i]= float(temp[i])

            core_temp = int(temp[0])

            if core_temp <= coretemp:
                log.success(f'{lines}\nThe core sensor temperature is below the max value {coretemp}: {core_temp}')
            else:
                raise RuntimeError(f'{lines}\nThe core sensor temperature is above the max value {coretemp}: {core_temp}')

    for lines in tmp05.splitlines():
        temp = re.findall(pattern,lines)

        if temp:
            for i in range(0, len(temp)):
                temp[i]= float(temp[i])

            tmp05_temp = int(temp[0])

            if tmp05_temp <= tmp05_max:
                log.success(f'{lines}\nThe tmp05 sensor temperature is below the max value {tmp05_max}: {tmp05_temp}')
            else:
                raise RuntimeError(f'{lines}\nThe tmp05 sensor temperature is above the max value {tmp05_max}: {tmp05_temp}')

    for lines in i2cool.splitlines():
        temp = re.findall(pattern,lines)

        if temp:
            for i in range(0, len(temp)):
                temp[i]= float(temp[i])

            i2cool_temp = int(temp[0])

            if i2cool_temp <= i2cool_max:
                log.success(f'{lines}\nThe i2cool sensor temperature is below the max value {i2cool_max}: {i2cool_temp}')
            else:
                raise RuntimeError(f'{lines}\nThe i2cool sensor temperature is above the max value {i2cool_max}: {i2cool_temp}')
    i = 0
    for lines in th4.splitlines():
        temp = re.findall(pattern,lines)

        if temp:
            i = i+1
            if i > 1:
                temp = float(temp[-1])
                if int(temp) < 0:
                    raise RuntimeError(f"th4 value is less than zero : {temp}")
                else:
                    log.success(f"th4 value is greater than zero: {temp}")

@logThis
def COMe_baseboard_powerbrick_sensor_check():
    env = run_command('show environment', prompt='root@sonic')
    if re.search(COMe, env) and re.search(COMe_U51, env) and  re.search(COMe_U59, env) and re.search(Baseboard, env) and re.search(PowerBrick_U33, env) and re.search(PowerBrick_U32, env) and re.search(UCD9090, env):
        log.success(f"The following voltage Sensors are present in the cmd :\n1.{COMe}\n2.{COMe_U51}\n3.{COMe_U59}\n4.{Baseboard}\n5.{PowerBrick_U33}\n6.{PowerBrick_U32}\n7.{UCD9090}")
    else:
        raise RuntimeError(f'one of the voltage sensors are not present')

    come = run_command('sensors '+ COMe, prompt='root@sonic')
    come_u51 = run_command('sensors '+ COMe_U51, prompt='root@sonic')
    come_u59 = run_command('sensors '+ COMe_U59,prompt='root@sonic')
    baseboard = run_command('sensors adm1272-i2c-*-10', prompt='root@sonic')
    powerbrick_u33 = run_command('sensors Q50SN12072-i2c-*-61', prompt='root@sonic')
    powerbrick_u32 = run_command('sensors Q50SN12072-i2c-*-60', prompt='root@sonic')
    ucd9090 = run_command('sensors ucd9090-i2c-*-41', prompt='root@sonic')

    #COMe
    pattern_value_check(come,'XP3R3V', XP3R3V)
    pattern_value_check(come,'XP1R5V', XP1R5V)
    pattern_value_check(come,'XP1R3V', XP1R3V)
    pattern_value_check(come,'XP12R0V', XP12R0V)
    pattern_value_check(come,'XP1R2V', XP1R2V)
    pattern_value_check(come,'XP1R7V', XP1R7V)
    pattern_value_check(come,'XP1R05V', XP1R05V)
    pattern_value_check(come,'XP2R5V', XP2R5V)
    pattern_value_check(come,'XP1R82V', XP1R82V)
    pattern_value_check(come,'XP1R05V_VCCSCSUS', XP1R05V_VCCSCSUS)

    #COMe_U51
    pattern_value_check(come_u51,'XP12R0V', u51_XP12R0V)
    pattern_value_check(come_u51,'XP1R82V', u51_XP1R82V)
    pattern_value_check(come_u51,'XP1R2V', u51_XP1R2V)
    pattern_value_check(come_u51,'Power XP1R82V', u51_Power_XP1R82V)
    pattern_value_check(come_u51,'Power XP1R2V', u51_Power_XP1R2V)
    pattern_value_check(come_u51,'Current XP1R82V', u51_Current_XP1R82V)
    pattern_value_check(come_u51,'Current XP1R2V',u51_Current_XP1R2V)

    #Come_U59
    pattern_value_check(come_u59,'XP12R0V', u59_XP12R0V)
    pattern_value_check(come_u59,'XP1R05V_VCCSCSUS', u59_XP1R05V_VCCSCSUS)
    pattern_value_check(come_u59,'XP1R05V', u59_XP1R05V)
    pattern_value_check(come_u59,'Power XP1R05V_VCCSCSUS', u59_Power_XP1R05V_VCCSCSUS)
    pattern_value_check(come_u59,'Power XP1R05V', u59_Power_XP1R05V)
    pattern_value_check(come_u59,'Current XP1R05V_VCCSCSUS', u59_Current_XP1R05V_VCCSCSUS)
    pattern_value_check(come_u59,'Current XP1R05V',u59_Current_XP1R05V)

    #Baseboard
    pattern_value_check(baseboard,'XP48R0V_IN', amd_XP48R0V_IN)
    pattern_value_check(baseboard,'XP48R0V_SWAP', amd_XP48R0V_SWAP)
    pattern_value_check(baseboard,'Power XP48R0V_SWAP', amd_Power_XP48R0V_SWAP)
    pattern_value_check(baseboard,'Current XP48R0V_SWAP', amd_Current_XP48R0V_SWAP)

    #Powerbrick U33
    pattern_value_check(powerbrick_u33,'XP48R0V_EMC_SW', pbU33_XP48R0V_EMC_SW)
    pattern_value_check(powerbrick_u33,'XP12R0V_SW', pbU33_XP12R0V_SW)
    pattern_value_check(powerbrick_u33,'Current XP12R0V_SW', pbU33_Current_XP12R0V_SW)

    #Powerbrick u32
    pattern_value_check(powerbrick_u32,'XP48R0V_EMC_BB', u32_XP48R0V_EMC_BB)
    pattern_value_check(powerbrick_u32,'XP12R0V_BB', u32_XP12R0V_BB)
    pattern_value_check(powerbrick_u32,'Current XP12R0V_BB', u32_Current_XP12R0V_BB)

    #UCD9090 Baseboard
    pattern_value_check(ucd9090,'XP12R0V_SW', ucd_XP12R0V_SW)
    pattern_value_check(ucd9090,'XP12R0V_BB', ucd_XP12R0V_BB)
    pattern_value_check(ucd9090,'XP12R0V_COME', ucd_XP12R0V_COME)
    pattern_value_check(ucd9090,'XP5R0V_COME', ucd_XP5R0V_COME)
    pattern_value_check(ucd9090,'XP3R3V', ucd_XP3R3V)
    pattern_value_check(ucd9090,'XP3R3V_STBY', ucd_XP3R3V_STBY)
    pattern_value_check(ucd9090,'XP3R3V_SSD', ucd_XP3R3V_SSD)


@logThis
def pattern_value_check(cmd, param, max_val):
    pattern = r'([^+-]?\d+\.\d+)\s?'
    for lines in cmd.splitlines():
        if 'Temp' not in lines and 'Power' not in lines and 'Current' not in lines:
            if re.findall(f'\\b{param}\\b', lines):
                voltage = re.findall(pattern,lines)
                if voltage:
                    for i in range(0, len(voltage)):
                        voltage[i]= float(voltage[i])
                    cmd_voltage = voltage[0]

                    if cmd_voltage <= max_val:
                        log.success(f'The sensor is normal for {param}: {cmd_voltage}')
                    else:
                        raise RuntimeError(f'The sensor is abnormal for {param}:  {cmd_voltage}')


@logThis
def check_ADM1266_sensor_via_both_FPGA_and_CPLD():
    output1 = run_command('sensors adm1266-i2c-10001-44', prompt='root@sonic')
    output2 = run_command('sensors adm1266-i2c-27-44', prompt='root@sonic')
    # validating the threshold
    pattern_value_check(output1,'VDD_12R0', VDD_12R0)
    pattern_value_check(output1,'VDD_12R0_OSFP', VDD_12R0_OSFP)
    pattern_value_check(output1,'VDD_5R0', VDD_5R0)
    pattern_value_check(output1,'VDD_3R3_AUX', VDD_3R3_AUX)
    pattern_value_check(output1,'VDD_3R3_A', VDD_3R3_A)
    pattern_value_check(output1,'VDD_3R3_B', VDD_3R3_B)
    pattern_value_check(output1,'ADD_AVS', ADD_AVS)
    pattern_value_check(output1,'AVDD_1R8', AVDD_1R8)
    pattern_value_check(output1,'VDD_1R8', VDD_1R8)
    pattern_value_check(output1,'VDD_1R2', VDD_1R2)
    pattern_value_check(output1,'AVDD_0R9_A', AVDD_0R9_A)
    pattern_value_check(output1,'AVDD_0R9_B', AVDD_0R9_B)
    pattern_value_check(output1,'AVDD_0R75_A', AVDD_0R75_A)
    pattern_value_check(output1,'VDD_1R8_OSC1', VDD_1R8_OSC1)
    pattern_value_check(output1,'VDD_1R8_OSC2', VDD_1R8_OSC2)
    pattern_value_check(output1,'AVDD_0R75_B', AVDD_0R75_B)

    if re.search(sensor_state, output2):
        log.success("The expected output is present!")
    else:
        raise RuntimeError("The unexpected error occured!")

@logThis
def switch_adm1266_to_baseboard_cpld():
    run_command('modprobe -r adm1266', prompt='root@sonic')
    run_command('echo 0x44 > /sys/bus/i2c/devices/i2c-10001/delete_device', prompt='root@sonic')
    run_command('echo 0 > /sys/devices/gfpga-platform/seq_mux_sel', prompt='root@sonic')
    run_command('sleep 1', prompt='root@sonic')
    run_command('echo adm1266 0x44 > /sys/bus/i2c/devices/i2c-27/new_device', prompt='root@sonic')
    run_command('sleep 1',prompt='root@sonic')
    output1 = run_command('sensors adm1266-i2c-27-44', prompt='root@sonic')
    output2 = run_command('sensors adm1266-i2c-10001-44', prompt='root@sonic')
    #via cpld
    pattern_value_check(output1,'VDD_12R0', VDD_12R0)
    pattern_value_check(output1,'VDD_12R0_OSFP', VDD_12R0_OSFP)
    pattern_value_check(output1,'VDD_5R0', VDD_5R0)
    pattern_value_check(output1,'VDD_3R3_AUX', VDD_3R3_AUX)
    pattern_value_check(output1,'VDD_3R3_A', VDD_3R3_A)
    pattern_value_check(output1,'VDD_3R3_B', VDD_3R3_B)
    pattern_value_check(output1,'ADD_AVS', ADD_AVS)
    pattern_value_check(output1,'AVDD_1R8', AVDD_1R8)
    pattern_value_check(output1,'VDD_1R8', VDD_1R8)
    pattern_value_check(output1,'VDD_1R2', VDD_1R2)
    pattern_value_check(output1,'AVDD_0R9_A', AVDD_0R9_A)
    pattern_value_check(output1,'AVDD_0R9_B', AVDD_0R9_B)
    pattern_value_check(output1,'AVDD_0R75_A', AVDD_0R75_A)
    pattern_value_check(output1,'VDD_1R8_OSC1', VDD_1R8_OSC1)
    pattern_value_check(output1,'VDD_1R8_OSC2', VDD_1R8_OSC2)
    pattern_value_check(output1,'AVDD_0R75_B', AVDD_0R75_B)
    #via fpga
    if re.search(sensor_state, output2):
        log.success("The expected output is present!")
    else:
        raise RuntimeError("The unexpected error occured!")

@logThis
def switch_adm1266_to_fpga_pmbus():
    run_command('modprobe -r adm1266', prompt='root@sonic')
    run_command('echo 0x44 > /sys/bus/i2c/devices/i2c-27/delete_device', prompt='root@sonic')
    run_command('echo 1 > /sys/devices/gfpga-platform/seq_mux_sel', prompt='root@sonic')
    run_command('sleep 1', prompt='root@sonic')
    run_command('echo adm1266 0x44 > /sys/bus/i2c/devices/i2c-10001/new_device', prompt='root@sonic')
    run_command('sleep 1',prompt='root@sonic')
    check_ADM1266_sensor_via_both_FPGA_and_CPLD()

@logThis
def check_switchboard_sensors():
    raa_sw = run_command('sensors raa228228-i2c-10001-60', prompt='root@sonic')

    pattern_value_check(raa_sw,'VDD_12R0_TH_FILT', raa_VDD_12R0_TH_FILT)
    pattern_value_check(raa_sw,'VDD_AVS', raa_VDD_AVS)
    pattern_value_check(raa_sw,'Power VDD_AVS', raa_Power_VDD_AVS)
    pattern_value_check(raa_sw,'Current VDD_AVS', raa_Current_VDD_AVS)

    isl1_sw = run_command('sensors isl68225-i2c-10002-62', prompt='root@sonic')

    pattern_value_check(isl1_sw,'VDD_12R0_OSFP_A_FILT', isl1_VDD_12R0_OSFP_A_FILT)
    pattern_value_check(isl1_sw,'VDD_12R0_TH_FILT', isl1_VDD_12R0_TH_FILT)
    pattern_value_check(isl1_sw,'VDD_3R3_A', isl1_VDD_3R3_A)
    pattern_value_check(isl1_sw,'AVDD_0R9_A', isl1_AVDD_0R9_A)
    pattern_value_check(isl1_sw,'Power VDD_3R3_A', isl1_Power_VDD_3R3_A)
    pattern_value_check(isl1_sw,'Power AVDD_0R9_A', isl1_Power_AVDD_0R9_A)
    pattern_value_check(isl1_sw,'Current VDD_3R3_A', isl1_Current_VDD_3R3_A)
    pattern_value_check(isl1_sw,'Current AVDD_0R9_A', isl1_Current_AVDD_0R9_A)

    isl2_sw = run_command('sensors isl68225-i2c-10002-63', prompt='root@sonic')

    pattern_value_check(isl2_sw,'VDD_12R0_OSFP_B_FILT', isl2_VDD_12R0_OSFP_B_FILT)
    pattern_value_check(isl2_sw,'VDD_12R0_TH_FILT', isl2_VDD_12R0_TH_FILT)
    pattern_value_check(isl2_sw,'VDD_3R3_B', isl2_VDD_3R3_B)
    pattern_value_check(isl2_sw,'AVDD_0R9_B', isl2_AVDD_0R9_B)
    pattern_value_check(isl2_sw,'Power VDD_3R3_B', isl2_Power_VDD_3R3_B)
    pattern_value_check(isl2_sw,'Power AVDD_0R9_B', isl2_Power_AVDD_0R9_B)
    pattern_value_check(isl2_sw,'Current VDD_3R3_B', isl2_Current_VDD_3R3_B)
    pattern_value_check(isl2_sw,'Current AVDD_0R9_B', isl2_Current_AVDD_0R9_B)

    u51_sw = run_command('sensors max20730-i2c-10001-53', prompt='root@sonic')

    pattern_value_check(u51_sw,'VDD_12R0', u51_VDD_12R0)
    pattern_value_check(u51_sw,'AVDD_0R75_A', u51_AVDD_0R75_A)
    pattern_value_check(u51_sw,'Current AVDD_0R75_A', u51_Current_AVDD_0R75_A)

    u199_sw = run_command('sensors max20730-i2c-10001-54', prompt='root@sonic')

    pattern_value_check(u199_sw,'VDD_12R0', u199_VDD_12R0)
    pattern_value_check(u199_sw,'AVDD_0R75_B', u199_AVDD_0R75_B)
    pattern_value_check(u199_sw,'Current AVDD_0R75_B', u199_Current_AVDD_0R75_B)

    u53_sw = run_command('sensors max20710-i2c-10001-55', prompt='root@sonic')

    pattern_value_check(u53_sw,'VDD_12R0', u53_VDD_12R0)
    pattern_value_check(u53_sw,'VDD_1R2', u53_VDD_1R2)
    pattern_value_check(u53_sw,'Current VDD_1R2', u53_Current_VDD_1R2)

    u54_sw = run_command('sensors max20710-i2c-10002-51', prompt='root@sonic')

    pattern_value_check(u54_sw,'VDD_12R0', u54_VDD_12R0)
    pattern_value_check(u54_sw,'VDD_1R8', u54_VDD_1R8)
    pattern_value_check(u54_sw,'Current VDD_1R8', u54_Current_VDD_1R8)

    u55_sw = run_command('sensors max20710-i2c-10002-52', prompt='root@sonic')

    pattern_value_check(u55_sw,'VDD_12R0', u55_VDD_12R0)
    pattern_value_check(u55_sw,'AVDD_1R8', u55_AVDD_1R8)
    pattern_value_check(u55_sw,'Current AVDD_1R8', u55_Current_AVDD_1R8)

@logThis
def Fan_Speed_Control():
    # Power cycle and check the fan speed
    sleep(120)
    output = device.sendCmd('echo 0x4449454a > /sys/devices/gfpga-platform/board_powercycle', 'sonic login', timeout=220)
    sleep(3)
    if 'sonic login' in output:
        device.sendCmd('admin', 'Password:', timeout=15)
        device.sendCmd('pass', 'Login incorrect', timeout=15)
        device.sendCmd('admin', 'Password:', timeout=15)
        output = device.sendCmd('YourPaSsWoRd', 'admin@sonic', timeout=15)
        device.sendCmd('sudo su', 'root@sonic', timeout=15)
        for line in diagos_login_info:
            if line in output:
                continue
            else:
                raise RuntimeError('sonic login check test fail')
    else:
        raise RuntimeError('Cannot find sonic OS login line: "sonic login:"')
    sleep(5)
    output = run_command('set_fan_speed.sh -g', prompt='root@sonic')
    if 'Error' in output:
        raise RuntimeError('Error string found in the output')
    else:
        log.success('Ran without any error')

    pattern = r'([^\.\s]\d+)\s?'
    for lines in output.splitlines():
        if lines.startswith('Inlet') or lines.startswith('Outlet'):
            fan = re.findall(pattern,lines)
            if fan:
                for i in range(0, len(fan)):
                    fan[i]= float(fan[i])
                Speed = fan[0]
                if int(Speed) > half_speed:
                    log.success(f'{lines}\nThe fan {Speed} is about 50%')
                else:
                    raise RuntimeError(f'{lines}\nThe fan {Speed} is not ~50%')

    #change fan speed 3 times and check the value changed correctly
    change_fan_Speed_check()
    change_fan_Speed_check()
    change_fan_Speed_check()

    #reboot and check fan speed is 25%
    diagos_login_check()
    sleep(50)
    output = run_command('set_fan_speed.sh -g', prompt='root@sonic')
    if 'Error' in output:
        raise RuntimeError('Error string found in the output')
    else:
        log.success('Ran without any error')

    pattern = r'([^\.\s]\d+)\s?'
    for lines in output.splitlines():
        if lines.startswith('Inlet') or lines.startswith('Outlet'):
            fan = re.findall(pattern,lines)
            if fan:
                for i in range(0, len(fan)):
                    fan[i]= float(fan[i])
                Speed = fan[0]
                if int(Speed) > quat_speed:
                    log.success(f'{lines}\nThe fan {Speed} is about 25%')
                else:
                    raise RuntimeError(f'{lines}\nThe fan {Speed} is not ~25%')



@logThis
def change_fan_Speed_check():
    sleep(20)
    device.sendCmd('docker exec -ti pmon supervisorctl stop thermalctld','thermalctld: stopped',timeout=10)

    #100% fan speed
    full = run_command('set_fan_speed.sh -s 255',prompt='root@sonic',timeout=30)
    different_fan_speed_check(full, full_speed)
    fan1 = run_command('set_fan_speed.sh -g',prompt='root@sonic',timeout=10)
    different_fan_speed_check(fan1, full_speed)

    #50% fan speed
    half = run_command('set_fan_speed.sh -s 127',prompt='root@sonic', timeout=20)
    different_fan_speed_check(half, half_speed)
    fan2 = run_command('set_fan_speed.sh -g',prompt='root@sonic',timeout=10)
    different_fan_speed_check(fan2, half_speed)

    #25% fan speed
    quat = run_command('set_fan_speed.sh -s 64',prompt='root@sonic',timeout=20)
    different_fan_speed_check(quat, quat_speed)
    fan3 = run_command('set_fan_speed.sh -g',prompt='root@sonic',timeout=10)
    different_fan_speed_check(fan3, quat_speed)

    device.sendCmd('docker exec -ti pmon supervisorctl start thermalctld','thermalctld: started',timeout=30)
    different_fan_speed_check(fan3, quat_speed)

@logThis
def different_fan_speed_check(output, fan_speed):
    pattern = r'([^\.\s]\d+)\s?'
    for lines in output.splitlines():
        if lines.startswith('Inlet') or lines.startswith('Outlet'):
            fan = re.findall(pattern,lines)
            if fan:
                for i in range(0, len(fan)):
                    fan[i]= float(fan[i])
                Speed = fan[0]
                if int(Speed) > fan_speed:
                    log.success(f'{lines}\nThe fan {Speed} is correct')
                else:
                    raise RuntimeError(f'{lines}\nThe fan {Speed} is not correct!')





@logThis
def Powercycle_and_restart_wdt_service():
    sleep(120)
    output = device.sendCmd('echo 0x4449454a > /sys/devices/gfpga-platform/board_powercycle', 'sonic login', timeout=220)
    sleep(3)
    if 'sonic login' in output:
        device.sendCmd('admin', 'Password:', timeout=15)
        device.sendCmd('pass', 'Login incorrect', timeout=15)
        device.sendCmd('admin', 'Password:', timeout=15)
        output = device.sendCmd('YourPaSsWoRd', 'admin@sonic', timeout=15)
        device.sendCmd('sudo su', 'root@sonic', timeout=15)
        for line in diagos_login_info:
            if line in output:
                continue
            else:
                raise RuntimeError('sonic login check test fail')
    else:
        raise RuntimeError('Cannot find sonic OS login line: "sonic login:"')
    sleep(5)

    run_command('service gfpga-watchdog restart', prompt='root@sonic')
    output = run_command('service gfpga-watchdog status', prompt='lines')
    device.sendCmd('q')

    if re.search('Active: active \\(running\\)', output):
        log.success('WDT restart is successful, active and running')
    else:
        raise RuntimeError('WDT restart Failed!')

@logThis
def inspect_wdt_service():
    c1=device.sendCmd('cat /sys/devices/gfpga-platform/watchdog_enabled', wdt_enabled, timeout=2)
    c2=device.sendCmd('cat /sys/devices/gfpga-platform/watchdog_period', wdt_period, timeout=2)
    c3=device.sendCmd('cat /sys/devices/gfpga-platform/watchdog_expired', wdt_expired, timeout = 2)
    c4=device.sendCmd('cat /sys/devices/gfpga-platform/watchdog_sw_override_en', wdt_sw_en, timeout= 2)
    c5=device.sendCmd('cat /sys/devices/gfpga-platform/watchdog_sw_override', wdt_sw, timeout =2)

@logThis
def stop_wdt_service_and_check_system_is_stable():
    output= run_command('service gfpga-watchdog stop',prompt='root@sonic',timeout =60)
    if 'coreboot' not in output:
        log.success('system not reset on WDT service stop')
    else:
        raise RuntimeError('system reset on WDT service stop')


@logThis
def inspect_wdt_after_service_stopped_and_Start_service():
    device.sendCmd('cat /sys/devices/gfpga-platform/watchdog_enabled', enabled, timeout='2')
    device.sendCmd('cat /sys/devices/gfpga-platform/watchdog_period', period, timeout='2')
    device.sendCmd('cat /sys/devices/gfpga-platform/watchdog_expired', expired, timeout = '2')
    device.sendCmd('cat /sys/devices/gfpga-platform/watchdog_sw_override_en', sw_en, timeout= '2')
    device.sendCmd('cat /sys/devices/gfpga-platform/watchdog_sw_override', sw, timeout ='2')
    device.sendCmd('service gfpga-watchdog start')

@logThis
def check_status_kill_the_service_and_check_system_reset():
    output = run_command('service gfpga-watchdog status' , prompt='lines')
    device.sendCmd('q')


    if re.search('Active: active \\(running\\)', output):
        log.success('WDT restart is successful, active and running')
    else:
        raise RuntimeError('WDT restart Failed!')

    pattern = r'([^a-zA-Z\:\d]+\d+)\s?'

    for lines in output.splitlines():
        if lines.startswith('   Main PID'):
            pid = re.findall(pattern, lines)
            if pid:
                for i in range(0, len(pid)):
                    pid[i]= str(pid[i])
                pid = pid[0]

                output = run_command('kill -9 '+ pid,prompt= 'sonic login', timeout=240)
                if 'sonic login' in output:
                    device.sendCmd('admin', 'Password:', timeout=15)
                    device.sendCmd('pass', 'Login incorrect', timeout=15)
                    device.sendCmd('admin', 'Password:', timeout=15)
                    output = device.sendCmd('YourPaSsWoRd', 'admin@sonic', timeout=15)
                    device.sendCmd('sudo su', 'root@sonic', timeout=15)
                    for line in diagos_login_info:
                        if line in output:
                            continue
                        else:
                            raise RuntimeError('sonic login check test fail')
                else:
                    raise RuntimeError('Cannot find sonic OS login line: "sonic login:"')
            else:
                raise RuntimeError('no pid id is present in the status')


@logThis
def recheck_wdt_steps_2to4():
    sleep(10)
    run_command('service gfpga-watchdog restart', prompt='root@sonic')
    output = run_command('service gfpga-watchdog status', prompt='lines')
    device.sendCmd('q')

    if re.search('Active: active \\(running\\)', output):
        log.success('WDT restart is successful, active and running')
    else:
        raise RuntimeError('WDT restart Failed!')

    inspect_wdt_service()
    stop_wdt_service_and_check_system_is_stable()
    inspect_wdt_after_service_stopped_and_Start_service()

@logThis
def restart_wdt_and_repeat_step5():
    device.sendCmd('service gfpga-watchdog restart')
    check_status_kill_the_service_and_check_system_reset()


@logThis
def i2c_stress_test():
    #COMe CPLD
    log.info("\nCOMe CPLD MFD")
    log.info("\ni801 bus")
    device.executeCmd(path1)
    out1 = run_command('ls -l /sys/bus/i2c/devices/i2c-0', prompt='root@sonic')
    out2 = run_command('i2cdetect -y 0', prompt='root@sonic')
    out3 = run_command('ls -l /sys/bus/i2c/devices/i2c-0/0-0072', prompt='root@sonic')
    log.info("\ni2c-ocores bus")
    out4 = run_command('ls -l /sys/bus/i2c/devices/i2c-1', prompt='root@sonic')
    out5 = run_command('i2cdetect -y 1', prompt='root@sonic')
    sleep(1)

    #Baseboard CPLD
    log.info("\nMMC CPLD MFD")
    log.info("\nDevices list")

    out6 = run_command('ls -1d /sys/devices/platform/mmcpld/ocores-i2c.*.auto', prompt='root@sonic')
    out7 = run_command('ls -1d /sys/devices/platform/mmcpld/mmc_reg.*.auto', prompt='root@sonic')
    out8 = run_command('ls -1d /sys/devices/platform/mmcpld/tmp05.*.auto', prompt='root@sonic')
    out9 = run_command('ls -1d /sys/devices/platform/mmcpld/fantray.*.auto/hwmon/hwmon*', prompt='root@sonic')
    out10 = run_command('cat /sys/devices/platform/mmcpld/fantray.*.auto/hwmon/hwmon*/name', prompt='root@sonic')
    sleep(1)

    #FPGA
    log.info("\nFPGA MFD")
    log.info("\nI2C Sequencer Adaptors")
    out11 = run_command('ls -1 /sys/devices/gfpga-platform/gfpga-platform_i2c/gfpga-platform_i2c_adapter_1', prompt='root@sonic')
    out12 = run_command('ls -1 /sys/devices/gfpga-platform/gfpga-platform_i2c/gfpga-platform_i2c_adapter_2', prompt='root@sonic')
    sleep(1)

    #Diag
    log.info("\nI2C scan by Diag command")
    output = device.executeCmd(path2)
    if "No such file or directory" in output:
        raise RuntimeError('Diag package is required to run next cmd')
    else:
        out13 = run_command('./cel-i2c-test --all', prompt='root@sonic')
        CommonKeywords.should_match_paired_regexp_list(out13, cmd13)
    sleep(1)

    #verification
    CommonKeywords.should_match_a_regexp(out1, cmd1)
    CommonKeywords.should_match_paired_regexp_list(out2, i2c_y0_pattern)
    CommonKeywords.should_match_paired_regexp_list(out3, cmd3)
    CommonKeywords.should_match_a_regexp(out4, cmd4)
    CommonKeywords.should_match_paired_regexp_list(out5, i2c_y1_pattern)
    CommonKeywords.should_match_paired_regexp_list(out6, cmd6)
    CommonKeywords.should_match_paired_regexp_list(out7, cmd7)
    CommonKeywords.should_match_paired_regexp_list(out8, cmd8)
    CommonKeywords.should_match_paired_regexp_list(out9, cmd9)
    CommonKeywords.should_match_paired_regexp_list(out10, cmd10)
    CommonKeywords.should_match_paired_regexp_list(out11, cmd11)
    CommonKeywords.should_match_paired_regexp_list(out12, cmd12)
#    CommonKeywords.should_match_paired_regexp_list(out13, cmd13)


@logThis
def check_device_stability():
    check_storage_device()
    output1 = run_command('i2cdetect -y 0', prompt='root@sonic')
    output2 = run_command('i2cdetect -y 1', prompt='root@sonic')
    CommonKeywords.should_match_paired_regexp_list(output1, i2c_y0_pattern)
    log.success('I2c -y 0 detect output as expected')
    CommonKeywords.should_match_paired_regexp_list(output2, i2c_y1_pattern)
    log.success('I2c -y 1 detect output as expected')

@logThis
def scp(filename):
    password = 'intel@1234' 
    device.sendCmd(f'scp root@10.204.82.253:/home/brixia_image/{filename} .')
    promptList = ["(y/n)", "(yes/no)", "password:"]
    patternList = re.compile('|'.join(promptList))
    output1 = device.read_until_regexp(patternList, timeout= '180')
    log.info('output1: ' + str(output1))

    if re.search("(yes/no)",output1):
        device.transmit("yes")
        device.receive("password:")
        device.transmit("%s"%password)
    elif re.search("(y/n)",output1):
        device.transmit("y")
        device.receive("password:")
        device.transmit("%s"%password)
    elif re.search("password:",output1):
        device.transmit("%s"%password)
    else:
        log.fail("pattern mismatch")
    
    device.read_until_regexp('root@sonic', timeout='140')
    device.sendCmd('\n\n')
    output = run_command('ls -la', prompt='root@sonic')
    if filename in output:
        log.success(f"file {filename} successfully fetched!")
    else:
        raise RuntimeError(f"Please add the file {filename} in 10.204.82.21/root server or add the file to the unit and run the test!") 

@logThis
def warm_boot_reset_stress_test():
    diagos_login_check()
    output = run_command('ls -la', prompt='root@sonic')
    if filename in output:
        log.success(f"file {filename} present")
    else:
        scp(filename)

    device.sendCmd('chmod 777 '+ filename)
    device.sendCmd('cd ..')
    device.sendCmd('rm Check_Bus.txt count.log function_check.log')
    device.sendCmd('cd admin')
    output = run_command('./'+filename, prompt='sonic login', timeout = '700')

    sleep(10)
    if 'sonic login' in output:
        device.sendCmd('admin', 'Password:', timeout=15)
        output = device.sendCmd('YourPaSsWoRd', 'admin@sonic', timeout=15)
        device.sendCmd('sudo su', 'root@sonic', timeout=15)
        for line in diagos_login_info:
            if line in output:
                continue
            else:
                raise RuntimeError('sonic login check test fail after warm boot stress test')
    else:
        raise RuntimeError('Cannot find sonic OS login line: "sonic login:" after warm boot stress test')

    device.sendCmd('cd ..')
    output_count = run_command('cat count.log',prompt = 'root@sonic')
    if output_count != '0':
        log.success('warm-boot reset stress test ran successfully!')
    else:
        raise RuntimeError('warm-boot reset stress test not executed!')

    output_Bus = run_command('cat Check_Bus.txt',prompt = 'root@sonic')
    for line in bus_pattern:
        if re.search(line, output_Bus):
            log.success("Check_BUS log passed!")
        else:
            raise RuntimeError("check_bus log failed!")
    output_fun = run_command('cat function_check.log',prompt = 'root@sonic')
    patterns = [
            th4_pci,
	    th4_pci_speed_width,
            gfpga_pci,
            gfpga_pci_speed_width,
            ssd,
            msd,
            i2c_l,
            Temp,
            osfp,
            sfpplus,
            eth0,
            eth_speed,
            ping]
    for line in patterns:
        val = type(line)
        log.info(f'{line} is  {val}')
        if re.search(line, output_fun):
            log.success(f'{line} passed!')
        else:
            log.fail(f'{line} failed!')

    for line in pcie_log:
        if re.search(line, output_fun):
            log.success(f'{line} passed!')
        else:
            log.fail(f'{line} failed!')

    for line in i2c_y0_pattern:
        if re.search(line, output_fun):
            log.success(f'{line} passed!')
        else:
            log.fail(f'{line} failed!')

    for line in i2c_y1_pattern:
        if re.search(line, output_fun):
            log.success(f'{line} passed!')
        else:
            log.fail(f'{line} failed!')

    for line in cmd6:
        if re.search(line, output_fun):
            log.success(f'{line} passed!')
        else:
            log.fail(f'{line} failed!')

    for line in cmd7:
        if re.search(line, output_fun):
            log.success(f'{line} passed!')
        else:
            log.fail(f'{line} failed!')

    for line in cmd11:
        if re.search(line, output_fun):
            log.success(f'{line} passed!')
        else:
            log.fail(f'{line} failed!')

    for line in cmd12:
        if re.search(line, output_fun):
            log.success(f'{line} passed!')
        else:
            log.fail(f'{line} failed!')

    for line in cmd13:
        if re.search(line, output_fun):
            log.success(f'{line} passed!')
        else:
            log.fail(f'{line} failed!')

    for line in come_cpld_version:
        if re.search(line, output_fun):
            log.success(f'{line} passed!')
        else:
            log.fail(f'{line} failed!')

    for line in mmc_major_version:
        if re.search(line, output_fun):
            log.success(f'{line} passed!')
        else:
            log.fail(f'{line} failed!')

    for line in mmc_minor_version:
        if re.search(line, output_fun):
            log.success(f'{line} passed!')
        else:
            log.fail(f'{line} failed!')

    for line in fpga_major_version:
        if re.search(line, output_fun):
            log.success(f'{line} passed!')
        else:
            log.fail(f'{line} failed!')

    for line in fpga_minor_version:
        if re.search(line, output_fun):
            log.success(f'{line} passed!')
        else:
            log.fail(f'{line} failed!')

    for line in osfp_info:
        if re.search(line, output_fun):
            log.success(f'{line} passed!')
        else:
            log.fail(f'{line} failed!')
    device.sendCmd('rm Check_Bus.txt count.log function_check.log')
    check_storage_device()

@logThis
def WDT_reset_stress_test():
    filename = 'WDT_Reset_Stress_Test.sh'
    output = run_command('ls -la', prompt='root@sonic')
    if filename in output:
        log.success(f"file {filename} present")
    else:
        scp(filename)

    device.sendCmd('chmod 777 '+ filename)
    run_command('service gfpga-watchdog restart', prompt='root@sonic')
    check_status_kill_the_service_and_check_system_reset()

    device.sendCmd('cd ..')
    device.sendCmd('rm Check_Bus.txt count.log function_check.log')
    device.sendCmd('cd admin')
    check = run_command('cat '+filename, prompt='root@sonic')

    content = 'reset.sh'
    if re.search(content, check):
        output = run_command('./'+filename,  prompt='sonic login', timeout = '360')

        sleep(10)
        if 'sonic login' in output:
            device.sendCmd('admin', 'Password:', timeout=15)
            output = device.sendCmd('YourPaSsWoRd', 'admin@sonic', timeout=15)
            device.sendCmd('sudo su', 'root@sonic', timeout=15)
            for line in diagos_login_info:
                if line in output:
                    continue
                else:
                    raise RuntimeError('sonic login check test fail after WDT reset stress test')
        else:
            raise RuntimeError('Cannot find sonic OS login line: "sonic login:" after WDT reset stress test')
    else:
        log.info(f'{filename} downloaded in binary format')
        device.sendCmd(f'rm {filename}')
        sleep(10)
        scp(filename)
        device.sendCmd('chmod 777 '+ filename)
        output = run_command('./'+filename,  prompt='sonic login', timeout = '360')

        sleep(10)
        if 'sonic login' in output:
            device.sendCmd('admin', 'Password:', timeout=15)
            output = device.sendCmd('YourPaSsWoRd', 'admin@sonic', timeout=15)
            device.sendCmd('sudo su', 'root@sonic', timeout=15)
            for line in diagos_login_info:
                if line in output:
                    continue
                else:
                    raise RuntimeError('sonic login check test fail after WDT reset stress test')
        else:
            raise RuntimeError('Cannot find sonic OS login line: "sonic login:" after WDT reset stress test')


    device.sendCmd('cd ..')
    output_count = run_command('cat count.log',prompt = 'root@sonic')
    if output_count != '0':
        log.success('WDT reset stress test ran successfully!')
    else:
        raise RuntimeError('WDT reset stress test not executed!')

    output_Bus = run_command('cat Check_Bus.txt',prompt = 'root@sonic')
    for line in bus_pattern:
        if re.search(line, output_Bus):
            log.success("Check_BUS log passed!")
        else:
            raise RuntimeError("check_bus log failed!")
    output_fun = run_command('cat function_check.log',prompt = 'root@sonic')
    patterns = [
            th4_pci,
            th4_pci_speed_width,
            gfpga_pci,
            gfpga_pci_speed_width,
            ssd,
            msd,
            i2c_l,
            Temp,
            osfp,
            sfpplus,
            eth0,
            eth_speed,
            ping]
    for line in patterns:
        val = type(line)
        log.info(f'{line} is  {val}')
        if re.search(line, output_fun):
            log.success(f'{line} passed!')
        else:
            log.fail(f'{line} failed!')

    for line in pcie_log:
        if re.search(line, output_fun):
            log.success(f'{line} passed!')
        else:
            log.fail(f'{line} failed!')

    for line in i2c_y0_pattern:
        if re.search(line, output_fun):
            log.success(f'{line} passed!')
        else:
            log.fail(f'{line} failed!')

    for line in i2c_y1_pattern:
        if re.search(line, output_fun):
            log.success(f'{line} passed!')
        else:
            log.fail(f'{line} failed!')

    for line in cmd6:
        if re.search(line, output_fun):
            log.success(f'{line} passed!')
        else:
            log.fail(f'{line} failed!')

    for line in cmd7:
        if re.search(line, output_fun):
            log.success(f'{line} passed!')
        else:
            log.fail(f'{line} failed!')

    for line in cmd11:
        if re.search(line, output_fun):
            log.success(f'{line} passed!')
        else:
            log.fail(f'{line} failed!')

    for line in cmd12:
        if re.search(line, output_fun):
            log.success(f'{line} passed!')
        else:
            log.fail(f'{line} failed!')

    for line in cmd13:
        if re.search(line, output_fun):
            log.success(f'{line} passed!')
        else:
            log.fail(f'{line} failed!')

    for line in come_cpld_version:
        if re.search(line, output_fun):
            log.success(f'{line} passed!')
        else:
            log.fail(f'{line} failed!')

    for line in mmc_major_version:
        if re.search(line, output_fun):
            log.success(f'{line} passed!')
        else:
            log.fail(f'{line} failed!')

    for line in mmc_minor_version:
        if re.search(line, output_fun):
            log.success(f'{line} passed!')
        else:
            log.fail(f'{line} failed!')

    for line in fpga_major_version:
        if re.search(line, output_fun):
            log.success(f'{line} passed!')
        else:
            log.fail(f'{line} failed!')

    for line in fpga_minor_version:
        if re.search(line, output_fun):
            log.success(f'{line} passed!')
        else:
            log.fail(f'{line} failed!')

    for line in osfp_info:
        if re.search(line, output_fun):
            log.success(f'{line} passed!')
        else:
            log.fail(f'{line} failed!')

    device.sendCmd('rm Check_Bus.txt count.log function_check.log')
    check_storage_device()



@logThis
def install_second_os(image):
    build_id = image[-2:]
    build = os_format+build_id+extension

    output = run_command('show version', prompt='root@sonic')
    if 'error' in output:
        raise RuntimeError('error string found in show version output')
    else:
        log.success('show version check passed')

    output = run_command('show boot', prompt='root@sonic')
    if 'error' in output:
        raise RuntimeError('error string found in show boot output')
    else:
        log.success('show boot check passed')

    scp(build)
    run_command('sonic-installer install '+build, prompt= 'continue?')
    output = run_command('y', prompt= 'root@sonic', timeout='180')
    if 'error' in output:
        raise RuntimeError('error string found when installing second os')
    else:
        log.success('second os installed successfully!')

    output = run_command('sonic-installer list', prompt='root@sonic')
    if re.search('Next: '+image, output):
        log.success('Next value is correct after installing the second os!')
    else:
        raise RuntimeError('Next value is incorrect in the sonic-installer-list!')

    diagos_login_check()

    output = run_command('show version', prompt='root@sonic')
    exp_version = image.replace('-OS-', '.')

    if exp_version not in output:
        raise RuntimeError('current version is not match the expected version {}!'.format(exp_version))
    else:
        log.success('check sonic version %s successfully.'%(exp_version))


    output = run_command('show boot', prompt='root@sonic')
    if re.search('Current: '+image, output) and re.search('Next: '+image, output):
        log.success('current version is switched to installed version')
    else:
        raise RuntimeError('current version is not updated to installed version!')

    output = device.executeCmd('show ip interface')
    if re.search('eth0 .* up/up.*', output):
        log.success('show ip interface check passed!')
    else:
        raise RuntimeError('show ip interface check Failed!')

    env = device.executeCmd('show environment')
    if re.search('coretemp', env) and re.search('tmp05', env) and re.search('I2Cool Inlet Temp', env) and ('error' not in env):
        log.success("All sensors are present in the 'show environment' cmd")
    else:
        raise RunTimeError("Not all sensors are present inthe 'show environment' cmd")

    output_1 = device.executeCmd('i2cdetect -y 0')
    CommonKeywords.should_match_paired_regexp_list(output_1, i2c_y0_pattern)
    output_2 = device.executeCmd('i2cdetect -y 1')
    CommonKeywords.should_match_paired_regexp_list(output_2, i2c_y1_pattern)
    check_storage_device()



@logThis
def uninstall_unused_os_version(version):
    run_command('sonic-installer remove '+version, prompt='Image will be removed')
    output = run_command('y', prompt='root@sonic')
    if re.search('Image removed', output):
        log.success('uninstalled the unused os version!')
    else:
        raise RuntimeError('uninstall failed!')

    output = run_command('show boot', prompt='root@sonic')
    if version not in output:
        log.success('show boot does not contain uninstalled image!')
    else:
        raise RuntimeError('show boot does contain uninstalled image!')

    diagos_login_check()

    output = run_command('show version', prompt='root@sonic')
    ver = version[-4:]
    if ver not in output:
        log.success('after reboot the installed version shows!')
    else:
        raise RuntimeError('after reboot the installed version is not there!')


@logThis
def IdentifyCorebootImage():
    output1=device.executeCmd('dmidecode -t bios')
    for item in output1.splitlines():
        match=re.search(coreboot_version,item)
        if match:
            log.success("The Coreboot Version is: 999999999.20220110.181349.1")
            break
    if not match:
        log.fail("Incorrect Coreboot Version")

    output2=device.executeCmd('ls -la /opt/google/h1tool/')
    for item in output2.splitlines():
        match=re.search('16821',item)
        if match:
            log.success("h1 Tool exists in Sonic Successfull")
            break
    if not match:
        log.fail("h1 Tool does not exists")
    output3=device.executeCmd("flash_erase /dev/mtd0 0x3f0000 16")
    for item in output3.splitlines():
        match=re.search(erase_mailbox,item)
        if match:
            log.success("Mailbox Erased Successfull")
            break
    if not match:
        log.fail("Erasing Fails")

    output4=device.executeCmd('''yes "_HVNMAIL" | tr -d '\n' | dd conv=notrunc bs=4096 seek=1008 count=16 of=/dev/mtd0''')
    for item in output4.splitlines():
        if not re.search('16+0',item):
            log.success("Recovering Flash Successfull")
            break
    output = device.sendCmd('reboot', 'sonic login', timeout=450)
    sleep(10)
    if 'sonic login' in output:
        device.sendCmd('admin', 'Password:', timeout=15)
        device.sendCmd('pass', 'Login incorrect', timeout=15)
        device.sendCmd('admin', 'Password:', timeout=15)
        output = device.sendCmd('YourPaSsWoRd', 'admin@sonic', timeout=15)
        device.sendCmd('sudo su', 'root@sonic', timeout=15)
    
    device.executeCmd('export CAPITAINE_HAVEN_FLAGS="--interface mtd --mtd_path /dev/mtd0 --haven_mailbox 0x3f0000"')
    device.executeCmd("/opt/google/h1tool/h1tool ${CAPITAINE_HAVEN_FLAGS} payload status")
    device.sendMsg(Const.KEY_CTRL_C)

@logThis
def UpdateCorebootImage():
    for i in range(3):
        device.sendMsg('cd .. \n')
    device.sendMsg('cd /usr/local/cls_diag/bin \n')
    device.sendCmd('./cel-upgrade-test --update -d 5 -f ../tools/firmware/capitaine-11-02-2021-4310-vendor.bios','root@sonic',timeout=500)
    device.read_until_regexp(".*Passed.*",timeout=500)
    log.info("DownGrade Coreboot Successfull")
    IdentifyCorebootImage()
    for i in range(3):
        device.sendMsg('cd .. \n')
    device.sendMsg('cd /usr/local/cls_diag/bin \n')
    device.sendCmd('./cel-upgrade-test --update -d 5 -f ../tools/firmware/capitaine-01-10-2022-vendor-6002.bios','root@sonic',timeout=500)
    device.read_until_regexp(".*Passed.*",timeout=500)
    log.info("UpGrade Coreboot Successfull")




@logThis
def checkCryptId():
    device.executeCmd("bios_vendor=$(cat /sys/class/dmi/id/bios_vendor)")
    device.sendMsg('if [[ "${bios_vendor}" -eq \'coreboot\' ]]; then')
    device.sendMsg("\n")
    #device.sendCmd("BIOS_MTD_PATH=$(sed -rn \'s/(mtd[0-9]).*(\"BIOS\")$/\/dev\/\1/p\' /proc/mtd);",'>',timeout=5)
    device.sendCmd('export CAPITAINE_HAVEN_FLAGS="--interface mtd --mtd_path $BIOS_MTD_PATH --haven_mailbox 0x3f0000";','>',timeout=5)
    device.sendCmd('/opt/google/h1tool/h1tool ${CAPITAINE_HAVEN_FLAGS} show crypta_id;','>',timeout=5)
    output1=device.sendCmd('fi','>',timeout=5)
    device.sendMsg("\n") 
    for item in output1.splitlines():
        match=re.search(cryptId,item)
        if match:
            log.success("The Cryptd Id verified")
            break
    if not match:
        log.fail("CryptdId not verified")

   
@logThis
def downgrade_Upgrade_SonicImage():
    pat='discover: installer mode detected'
    device.sendMsg('reboot \n')
    device.read_until_regexp('.*Hit ',timeout=450)
    for i in range(3):
        device.sendMsg(Const.KEY_CTRL_C)
        try:
            d1=device.read_until_regexp('>', timeout=15)
            break
        except Exception:
            continue
    device.sendCmd("pxeboot \n", '>', timeout=30)
    device.sendCmd("02",timeout=5)
    c1=device.read_until_regexp('Starting: discover',timeout=100)
    if re.search(pat,c1):
        log.success("Sucessfully entered installer mode")
    else:
        log.fail("Didnt load installer mode")
    m1=device.sendCmd(' onie-stop','ONIE-RECOVERY:/ #',timeout=30)
    device.sendMsg('ping 192.168.0.1 \n')
    sleep(10)
    device.sendMsg(Const.KEY_CTRL_C)
    device.sendMsg("\n")
    if not re.search(onie_stop,m1):
        log.success("Stopping Onie Done Successfully")
    else:
        log.fail("Onie-Stop Failed")

    m2=device.sendCmd('onie-nos-install http://192.168.0.1/onie-installer-x86_64.bin','ONIE-RECOVERY:/ #',timeout=320)
    output=device.read_until_regexp('sonic login:.* ',timeout=500)
    if not re.search(OS_Install,m2):
        log.success("Downgrade Sonic OS Installed Successfully in http Server")
    else:
        log.fail("Downgrade Sonic Failed")
    if 'sonic login' in output:
        device.sendCmd('admin', 'Password:', timeout=15)
        device.sendCmd('pass', 'Login incorrect', timeout=15)
        device.sendCmd('admin', 'Password:', timeout=15)
        output = device.sendCmd('YourPaSsWoRd', 'admin@sonic', timeout=15)
        device.sendCmd('sudo su', 'root@sonic', timeout=15)

    device.sendMsg('reboot \n')
    device.read_until_regexp('.*Hit ',timeout=450)
    for i in range(3):
        device.sendMsg(Const.KEY_CTRL_C)
        try:
            d1=device.read_until_regexp('>', timeout=15)
            break
        except Exception:
            continue


    device.sendCmd("pxeboot \n", '>', timeout=30)
    device.sendCmd("02",timeout=5)
    c1=device.read_until_regexp('Starting: discover',timeout=100)
    if re.search(pat,c1):
        log.success("Sucessfully entered installer mode")
    else:
        log.fail("Didnt load installer mode")

    m1=device.sendCmd(' onie-stop','ONIE-RECOVERY:/ #',timeout=30)
    device.sendMsg('ping 192.168.0.1 \n')
    sleep(10)
    device.sendMsg(Const.KEY_CTRL_C)
    device.sendMsg("\n")
    if not re.search(onie_stop,m1):
        log.success("Stopping Onie Done Successfully")
    else:
        log.fail("Onie-Stop Failed")

    m2=device.sendCmd('onie-nos-install http://192.168.0.1/onie-installer.bin','ONIE-RECOVERY:/ #',timeout=320)
    output=device.read_until_regexp('sonic login:.* ',timeout=500)
    if not re.search(OS_Install,m2):
        log.success("Upgrade Sonic OS Installed Successfully in http Server")
    else:
        log.fail("Upgrade Sonic Failed")

    sleep(10)
    if 'sonic login' in output:
        device.sendCmd('admin', 'Password:', timeout=15)
        device.sendCmd('pass', 'Login incorrect', timeout=15)
        device.sendCmd('admin', 'Password:', timeout=15)
        output = device.sendCmd('YourPaSsWoRd', 'admin@sonic', timeout=15)
        device.sendCmd('sudo su', 'root@sonic', timeout=15)
    
    check_sonic_version(show_version_cmd, show_boot_cmd)


@logThis
def UpgradeSonicImage():
    pat='discover: installer mode detected'
    device.sendMsg('reboot \n')
    device.read_until_regexp('.*Hit ',timeout=450)
    for i in range(3):
        device.sendMsg(Const.KEY_CTRL_C)
        try:
            d1=device.read_until_regexp('>', timeout=15)
            break
        except Exception:
            continue
    device.sendCmd("pxeboot \n", '>', timeout=30)
    device.sendCmd("02",timeout=5)
    c1=device.read_until_regexp('Starting: discover',timeout=100)
    if re.search(pat,c1):
        log.success("Sucessfully entered installer mode")
    else:
        log.fail("Didnt load installer mode")
    m1=device.sendCmd(' onie-stop','ONIE-RECOVERY:/ #',timeout=30)
    device.sendMsg('ping 192.168.0.1 \n')
    sleep(10)
    device.sendMsg(Const.KEY_CTRL_C)
    device.sendMsg("\n")
    if not re.search(onie_stop,m1):
        log.success("Stopping Onie Done Successfully")
    else:
        log.fail("Onie-Stop Failed")

    m2=device.sendCmd('onie-nos-install http://192.168.0.1/onie-installer.bin','ONIE-RECOVERY:/ #',timeout=320)
    output=device.read_until_regexp('sonic login:.* ',timeout=500)
    if not re.search(OS_Install,m2):
        log.success("Upgrade Sonic OS Installed Successfully in http Server")
    else:
        log.fail("Upgrade Sonic Failed")
    
    sleep(10)
    if 'sonic login' in output:
        device.sendCmd('admin', 'Password:', timeout=15)
        device.sendCmd('pass', 'Login incorrect', timeout=15)
        device.sendCmd('admin', 'Password:', timeout=15)
        output = device.sendCmd('YourPaSsWoRd', 'admin@sonic', timeout=15)
        device.sendCmd('sudo su', 'root@sonic', timeout=15)
    
    check_sonic_version(show_version_cmd, show_boot_cmd)

    
@logThis
def checkUpdateDriverStatus():
    device.sendMsg('show ip interfaces \n')
    device.read_until_regexp('.*up.*',timeout=10)
    log.info("PASS: All IP Interfaces are up passed")
    device.sendMsg('show environment \n')
    device.read_until_regexp('.*Script version.*',timeout=20)
    log.info("PASS: All Environment Variables passed successfully")
    device.sendMsg('fdisk -l \n')
    device.read_until_regexp('.*512 bytes',timeout=100)
    log.info("PASS: Disk Information passed")
    device.sendMsg('i2cdetect -y 0 \n')
    device.read_until_regexp('70:.*',timeout=10)
    log.info("PASS:i2c Variables Passed") 
    device.sendMsg('i2cdetect -y 1 \n')
    device.read_until_regexp('70:.*',timeout=10)
    log.info("PASS:i2c Variables Passed") 


@logThis
def uninstallFirstSonic():
    pat='discover: Rescue mode detected'
    device.sendMsg('reboot \n')
    device.read_until_regexp('.*Hit ',timeout=450)
    for i in range(3):
        device.sendMsg(Const.KEY_CTRL_C)
        try:
            d1=device.read_until_regexp('>', timeout=15)
            break
        except Exception:
            continue
    device.sendCmd("pxeboot \n", '>', timeout=30)
    device.sendCmd("03",timeout=5)
    c1=device.read_until_regexp('.*Starting:.*',timeout=100)
    if not re.search(pat,c1):
        log.success("Sucessfully entered Onie mode")
    else:
        log.fail("Didnt load Onie mode")
    device.sendCmd("echo 1 > /sys/bus/pci/devices/0000:$(lspci | grep -i 1ae0 | cut -d ' ' -f 1)/enable",'ONIE-RECOVERY:/ #',timeout=10)
    device.sendCmd("offset=$(awk 'NR==1{print $1}' /sys/bus/pci/devices/0000:$(lspci | grep -i 1ae0 | cut -d ' ' -f 1)/resource)",'ONIE-RECOVERY:/ #',timeout=10)
    device.sendCmd("devmem $((offset + 0x40)) 32 0x8",'ONIE-RECOVERY:/ #',timeout=10)
    m1=device.sendCmd(' onie-stop','ONIE-RECOVERY:/ #',timeout=30)
    device.sendMsg('ping 192.168.0.1 \n')
    sleep(10)
    device.sendMsg(Const.KEY_CTRL_C)
    device.sendMsg("\n")
    if not re.search(onie_stop,m1):
        log.success("Stopping Onie Done Successfully")
    else:
        log.fail("Onie-Stop Failed")
    m2=device.sendCmd("onie-uninstaller",'ONIE-RECOVERY:/ #',timeout=1000)
    output=device.read_until_regexp('.*Percent complete:.*',timeout=1000)
    if re.search('Percent complete.*',output):
        log.success("Uninstall Successfull")
    else:
        log.fail("Uninstall Not Successfull")

@logThis
def lowerSonicImage():
    pat='discover: installer mode detected'
    device.sendMsg('reboot \n')
    output_2=device.read_until_regexp('.*Hit',timeout=1000)
    for i in range(3):
        device.sendMsg(Const.KEY_CTRL_C)
        try:
            d1=device.read_until_regexp('>', timeout=15)
            break
        except Exception:
            continue
    device.sendCmd("pxeboot \n", '>', timeout=30)
    device.sendCmd("02",timeout=5)
    c1=device.read_until_regexp('Starting: discover',timeout=100)
    if re.search(pat,c1):
        log.success("Sucessfully entered installer mode")
    else:
        log.fail("Didnt load installer mode")
    m1=device.sendCmd(' onie-stop','ONIE-RECOVERY:/ #',timeout=30)
    device.sendMsg('ping 192.168.0.1 \n')
    sleep(10)
    device.sendMsg(Const.KEY_CTRL_C)
    device.sendMsg("\n")
    if not re.search(onie_stop,m1):
        log.success("Stopping Onie Done Successfully")
    else:
        log.fail("Onie-Stop Failed")

    m2=device.sendCmd('onie-nos-install http://192.168.0.1/onie-installer-x86_64.bin','ONIE-RECOVERY:/ #',timeout=320)
    output=device.read_until_regexp('sonic login:.* ',timeout=500)
    if not re.search(OS_Install,m2):
        log.success("Lower Sonic OS Installed Successfully in http Server")
    else:
        log.fail("Lower Sonic Failed")

    sleep(10)
    if 'sonic login' in output:
        device.sendCmd('admin', 'Password:', timeout=15)
        device.sendCmd('pass', 'Login incorrect', timeout=15)
        device.sendCmd('admin', 'Password:', timeout=15)
        output = device.sendCmd('YourPaSsWoRd', 'admin@sonic', timeout=15)
        device.sendCmd('sudo su', 'root@sonic', timeout=15)

    check_sonic_version(show_version_cmd, show_boot_cmd)

@logThis
def fetchSonicImage():
    output = run_command("ls", prompt="root@sonic:.*", timeout=3)
    if "onie-installer-x86_64.bin" not in output:
        log.info("SONiC pb19 image not found\nFetching from server...\n")
        try:
            run_command(fetch_old_sonic, prompt="root@sonic:.*", timeout=80)
        except Exception as e:
            raise Exception("Error in fetching SONiC image from server.\n"+str(e))
        log.info("Sonic old image succesfully fetched from server.")
    elif "onie-installer.bin" not in output:
        log.info("SONiC pb20 image not found")
        try:
            run_command(fetch_new_sonic,prompt="root@sonic:.*",timeout=80)
        except Exception as e:
            raise Exception("Error in fetching new SONiC image")
        log.info("Sonic New Image successfully fetched from server")
    else:
        log.info("Sonic old image already present.")

@logThis
def gotoSuperUser():
    output = run_command("pwd", prompt="(root|admin)@sonic:.*")
    if "root@sonic:" in output:
        log.info("Already in super-user mode.")
    else:
        output = run_command("sudo -s", prompt="(root|admin)@sonic:.*")
        log.info("Entered Super-User mode.")

@logThis
def install_New_Sonic_OS():
    # Install SONiC 20
    fetchSonicImage()
    device.sendMsg('sonic-installer install onie-installer.bin \n')
    device.read_until_regexp("New image will be installed.*")
    device.sendMsg("y \r\n")
    output = device.read_until_regexp("Done", timeout=60)

    if not re.search("Installed SONiC base image SONiC-OS successfully|.*already installed.*", output):
        raise Exception("Error in Installing new SONiC version OS.")
    else:
        log.info("SONiC PB20 installed succesfully.")
    count=0
    output2=run_command('sonic-installer list',prompt='root@sonic')
    for i in sonic_list:
        match=re.search(i,output2)
        if match:
            count+=1
    if count!=len(sonic_list):
        log.success("Successfully Update Sonic List")
    else:
        log.fail("Sonic List Failed")

@logThis
def install_Previous_Sonic_OS():
    #gotoSuperUser()
    fetchSonicImage()

    # Install SONiC 19
    device.sendMsg('sonic-installer install onie-installer-x86_64.bin \n')
    device.read_until_regexp("New image will be installed.*")
    device.sendMsg("y \r\n")
    output = device.read_until_regexp("Done", timeout=60)

    if not re.search("Installed SONiC base image SONiC-OS successfully|.*already installed.*", output):
        raise Exception("Error in Installing older SONiC version OS.")
    else:
        log.info("SONiC PB19 installed succesfully.")

@logThis
def showTwoSonic():
    count=0
    device.sendCmd('reboot', 'sonic login', timeout=450)
    output=device.read_until_regexp(".*not found",timeout=500)
    for i in menu:
        if re.search(i,output):
            count+=1
    if count!=len(menu):
        log.success("On Rebooting, Grub shows 2 SONIC OS")
    else:
        log.fail("Grub shows 2 SONIC OS Failed")

    sleep(10)
    if 'not found' in output:
        device.sendCmd('admin', 'Password:', timeout=15)
        device.sendCmd('pass', 'Login incorrect', timeout=15)
        device.sendCmd('admin', 'Password:', timeout=15)
        output = device.sendCmd('YourPaSsWoRd', 'admin@sonic', timeout=15)
        device.sendCmd('sudo su', 'root@sonic', timeout=15)
        for line in diagos_login_info:
            if line in output:
                continue
            else:
                raise RuntimeError('sonic login check test fail')
    else:
        raise RuntimeError('Cannot find sonic OS login line: "sonic login:"')

@logThis
def checkBlockDevice():
    device.sendMsg("blkid \n")
    device.sendMsg('reboot \n')
    output_2=device.read_until_regexp('.*Hit',timeout=1000)
    for i in range(3):
        device.sendMsg(Const.KEY_CTRL_C)
        try:
            d1=device.read_until_regexp('>', timeout=15)
            break
        except Exception:
            continue
    device.sendCmd("pxeboot \n", '>', timeout=30)
    device.sendCmd("03",timeout=5)
    c1=device.read_until_regexp('.*Starting:.*',timeout=100)
    if not re.search(pat,c1):
        log.success("Sucessfully entered Onie mode")
    else:
        log.fail("Didnt load Onie mode")
    device.sendMsg("blkid \n")

@logThis
def uninstallAllSonic():
    device.sendCmd("echo 1 > /sys/bus/pci/devices/0000:$(lspci | grep -i 1ae0 | cut -d ' ' -f 1)/enable",'ONIE-RECOVERY:/ #',timeout=10)
    device.sendCmd("offset=$(awk 'NR==1{print $1}' /sys/bus/pci/devices/0000:$(lspci | grep -i 1ae0 | cut -d ' ' -f 1)/resource)",'ONIE-RECOVERY:/ #',timeout=10)
    device.sendCmd("devmem $((offset + 0x40)) 32 0x8",'ONIE-RECOVERY:/ #',timeout=10)
    device.sendMsg("onie-uninstaller \n")
    device.read_until_regexp(".*Cannot remove current image",timeout=500)
    log.info("Image Removed Successfully")


@logThis
def uninstallLowerSonic():
    device.sendMsg("sonic-installer remove SONiC-OS-202106-brixia.pb19 \n")
    device.read_until_regexp("Image will be removed.*")
    device.sendMsg("y \r\n")
    device.sendMsg("show boot \n")
    device.sendCmd('reboot', 'sonic login', timeout=450)
    output=device.read_until_regexp(".*not found",timeout=500)
    count=0
    for i in menu2:
        if re.search(i,output):
            count+=1
    if count!=len(menu):
        log.success("On Rebooting, Grub show only 1 SONIC OS")
    else:
        log.fail("Grub showing SONIC OS Failed")

    sleep(10)
    if 'not found' in output:
        device.sendCmd('admin', 'Password:', timeout=15)
        device.sendCmd('pass', 'Login incorrect', timeout=15)
        device.sendCmd('admin', 'Password:', timeout=15)
        output = device.sendCmd('YourPaSsWoRd', 'admin@sonic', timeout=15)
        device.sendCmd('sudo su', 'root@sonic', timeout=15)
        for line in diagos_login_info:
            if line in output:
                continue
            else:
                raise RuntimeError('sonic login check test fail')
    else:
        raise RuntimeError('Cannot find sonic OS login line: "sonic login:"')

@logThis
def uninstallHigherSonic():
    device.sendMsg("sonic-installer remove SONiC-OS-202106-brixia.pb20 \n")
    device.read_until_regexp("Image will be removed.*")
    device.sendMsg("y \r\n")
    device.sendMsg("show boot \n")
    device.sendCmd('reboot', 'sonic login', timeout=450)
    output=device.read_until_regexp(".*not found",timeout=500)
    count=0
    for i in menu2:
        if re.search(i,output):
            count+=1
    if count!=len(menu):
        log.success("On Rebooting, Grub show only 1 SONIC OS")
    else:
        log.fail("Grub showing SONIC OS Failed")

    sleep(10)
    if 'not found' in output:
        device.sendCmd('admin', 'Password:', timeout=15)
        device.sendCmd('pass', 'Login incorrect', timeout=15)
        device.sendCmd('admin', 'Password:', timeout=15)
        output = device.sendCmd('YourPaSsWoRd', 'admin@sonic', timeout=15)
        device.sendCmd('sudo su', 'root@sonic', timeout=15)
        for line in diagos_login_info:
            if line in output:
                continue
            else:
                raise RuntimeError('sonic login check test fail')
    else:
        raise RuntimeError('Cannot find sonic OS login line: "sonic login:"')


@logThis
def downgrade_Sonic_Via_Current_Version():
    scp(filename3)
    sleep(30)
    device.sendMsg("reboot \n")
    output=device.read_until_regexp(".*sonic login",timeout=500)
    count=0
    for i in menu:
        if re.search(i,output):
            count+=1
    if count!=len(menu):
        log.success("On Rebooting, Grub shows 2 SONIC OS")
    else:
        log.fail("Grub shows 2 SONIC OS Failed")
    sleep(10)
    if 'sonic login' in output:
        device.sendCmd('admin', 'Password:', timeout=15)
        device.sendCmd('pass', 'Login incorrect', timeout=15)
        device.sendCmd('admin', 'Password:', timeout=15)
        output = device.sendCmd('YourPaSsWoRd', 'admin@sonic', timeout=15)
        device.sendCmd('sudo su', 'root@sonic', timeout=15)
        for line in diagos_login_info:
            if line in output:
                continue
            else:
                raise RuntimeError('sonic login check test fail')
    else:
        raise RuntimeError('Cannot find sonic OS login line: "sonic login:"')

    check_sonic_version(show_version_cmd, show_boot_cmd)
    scp(filename)
    sleep(30)
    device.sendMsg("sonic-installer install sonic-broadcom-pb18.bin \n")
    device.read_until_regexp("New image will be installed.*")
    device.sendMsg("y \r\n")
    output=device.read_until_regexp(".*Done",timeout=200)
    log.info("Sonic Installed Successfully")
    device.sendMsg("sonic-installer list \n")
    device.read_until_regexp(".*pb.*",timeout=5)
    log.info("Sonic List appeared Successfully")
    device.sendMsg("reboot \n")
    output_2=device.read_until_regexp('.*sonic login',timeout=500)
    #device.sendCmd("01",timeout=5)
    sleep(10)
    if 'sonic login' in output_2:
        device.sendCmd('admin', 'Password:', timeout=15)
        device.sendCmd('pass', 'Login incorrect', timeout=15)
        device.sendCmd('admin', 'Password:', timeout=15)
        output = device.sendCmd('YourPaSsWoRd', 'admin@sonic', timeout=15)
        device.sendCmd('sudo su', 'root@sonic', timeout=15)
        for line in diagos_login_info:
            if line in output:
                continue
            else:
                raise RuntimeError('sonic login check test fail')
    else:
        raise RuntimeError('Cannot find sonic OS login line: "sonic login:"')

    check_sonic_version(show_version_cmd, show_boot_cmd)

@logThis
def upgrade_SONiC_Via_Current_Version():
    scp(filename2)
    sleep(30)
    device.sendMsg("sonic-installer install sonic-broadcom-pb20.bin \n")
    device.read_until_regexp("New image will be installed.*")
    device.sendMsg("y \r\n")
    output=device.read_until_regexp(".*Done",timeout=200)
    device.sendMsg("show boot \n")
    device.read_until_regexp(".*pb.*",timeout=5)
    log.info("show boot command passed")
    device.sendMsg("reboot \n")
    output_1=device.read_until_regexp('.*Enter an option',timeout=450)
    for i in range(1):
        try:
            d1=device.read_until_regexp('>', timeout=15)
            break
        except Exception:
            continue
    device.sendCmd("02",timeout=5)
    output_2=device.read_until_regexp(".*sonic login",timeout=40)
    if output_2:
        device.sendCmd('admin', 'Password:', timeout=15)
        device.sendCmd('pass', 'Login incorrect', timeout=15)
        device.sendCmd('admin', 'Password:', timeout=15)
        output = device.sendCmd('YourPaSsWoRd', 'admin@sonic', timeout=15)
        device.sendCmd('sudo su', 'root@sonic', timeout=15)
        for line in diagos_login_info:
            if line in output:
                continue
            else:
                raise RuntimeError('sonic login check test fail')
    else:
        raise RuntimeError('Cannot find sonic OS login line: "sonic login:"')

    check_sonic_version(show_version_cmd, show_boot_cmd)
    sleep(60)

@logThis
def upgrade_SONiC_Via_Current_Version_2():
    scp(filename3)
    sleep(30)
    device.sendMsg("sonic-installer install sonic-broadcom-pb19.bin \n")
    device.read_until_regexp("New image will be installed.*")
    device.sendMsg("y \r\n")
    output=device.read_until_regexp(".*Done",timeout=200)
    log.info("Sonic Installed Successfully")
    device.sendMsg("sonic-installer list \n")
    device.read_until_regexp(".*pb.*",timeout=5)
    log.info("Sonic List appeared Successfully")
    device.sendMsg("reboot \n")
    output_1=device.read_until_regexp('.*Enter an option',timeout=450)
    for i in range(1):
        try:
            d1=device.read_until_regexp('>', timeout=15)
            break
        except Exception:
            continue
    device.sendCmd("01",timeout=5)
    output_2=device.read_until_regexp(".*sonic login",timeout=100)
    if output_2:
        device.sendCmd('admin', 'Password:', timeout=15)
        device.sendCmd('pass', 'Login incorrect', timeout=15)
        device.sendCmd('admin', 'Password:', timeout=15)
        output = device.sendCmd('YourPaSsWoRd', 'admin@sonic', timeout=15)
        device.sendCmd('sudo su', 'root@sonic', timeout=15)
        for line in diagos_login_info:
            if line in output:
                continue
            else:
                raise RuntimeError('sonic login check test fail')
    else:
        raise RuntimeError('Cannot find sonic OS login line: "sonic login:"')

    check_sonic_version(show_version_cmd, show_boot_cmd)
    sleep(60)

@logThis
def downgrade_Current_To_Older_Version():
    scp(filename)
    sleep(30)
    device.sendMsg("sonic-installer install sonic-broadcom-pb18.bin \n")
    device.read_until_regexp("New image will be installed.*")
    device.sendMsg("y \r\n")
    output=device.read_until_regexp(".*Done",timeout=200)
    log.info("Sonic Installed Successfully")
    device.sendMsg("sonic-installer list \n")
    device.read_until_regexp(".*pb.*",timeout=5)
    log.info("Sonic List appeared Successfully")
    device.sendMsg("reboot \n")
    output_2=device.read_until_regexp('.*sonic login',timeout=500)
    #device.sendCmd("01",timeout=5)
    sleep(10)
    if 'sonic login' in output_2:
        device.sendCmd('admin', 'Password:', timeout=15)
        device.sendCmd('pass', 'Login incorrect', timeout=15)
        device.sendCmd('admin', 'Password:', timeout=15)
        output = device.sendCmd('YourPaSsWoRd', 'admin@sonic', timeout=15)
        device.sendCmd('sudo su', 'root@sonic', timeout=15)
        for line in diagos_login_info:
            if line in output:
                continue
            else:
                raise RuntimeError('sonic login check test fail')
    else:
        raise RuntimeError('Cannot find sonic OS login line: "sonic login:"')
    check_sonic_version(show_version_cmd, show_boot_cmd)
    sleep(60)

@logThis
def upgrade_Older_To_Current_Version():
    scp(filename3)
    sleep(30)
    device.sendMsg("sonic-installer install sonic-broadcom-pb19.bin \n")
    device.read_until_regexp("New image will be installed.*")
    device.sendMsg("y \r\n")
    output=device.read_until_regexp(".*Done",timeout=200)
    log.info("Previous Sonic Set By default  Successfully")
    device.sendMsg("show boot \n")
    device.read_until_regexp(".*pb.*",timeout=5)
    log.info("show boot command passed")
    device.sendMsg("reboot \n")
    output_1=device.read_until_regexp('.*Enter an option',timeout=450)
    for i in range(1):
        try:
            d1=device.read_until_regexp('>', timeout=15)
            break
        except Exception:
            continue
    device.sendCmd("01",timeout=5)
    output_2=device.read_until_regexp(".*sonic login",timeout=100)
    if output_2:
        device.sendCmd('admin', 'Password:', timeout=15)
        device.sendCmd('pass', 'Login incorrect', timeout=15)
        device.sendCmd('admin', 'Password:', timeout=15)
        output = device.sendCmd('YourPaSsWoRd', 'admin@sonic', timeout=15)
        device.sendCmd('sudo su', 'root@sonic', timeout=15)
        for line in diagos_login_info:
            if line in output:
                continue
            else:
                raise RuntimeError('sonic login check test fail')
    else:
        raise RuntimeError('Cannot find sonic OS login line: "sonic login:"')
    sleep(40)
    scp(filename2)
    sleep(30)
    device.sendMsg("sonic-installer install sonic-broadcom-pb20.bin \n")
    device.read_until_regexp("New image will be installed.*")
    device.sendMsg("y \r\n")
    output=device.read_until_regexp(".*Done",timeout=200)
    log.info("Current Sonic Installed Successfully")
    device.sendMsg("sonic-installer list \n")
    device.read_until_regexp(".*pb20",timeout=5)
    log.info("Sonic List appeared Successfully")
    device.sendMsg("reboot \n")
    output_1=device.read_until_regexp('.*Enter an option',timeout=450)
    for i in range(1):
        try:
            d1=device.read_until_regexp('>', timeout=15)
            break
        except Exception:
            continue
    device.sendCmd("02",timeout=5)
    output_2=device.read_until_regexp(".*sonic login",timeout=100)
    if output_2:
        device.sendCmd('admin', 'Password:', timeout=15)
        device.sendCmd('pass', 'Login incorrect', timeout=15)
        device.sendCmd('admin', 'Password:', timeout=15)
        output = device.sendCmd('YourPaSsWoRd', 'admin@sonic', timeout=15)
        device.sendCmd('sudo su', 'root@sonic', timeout=15)
        for line in diagos_login_info:
            if line in output:
                continue
            else:
                raise RuntimeError('sonic login check test fail')
    else:
        raise RuntimeError('Cannot find sonic OS login line: "sonic login:"')

    sleep(40)
    check_sonic_version(show_version_cmd, show_boot_cmd)
    checkUpdateDriverStatus()



@logThis
def boot_Sonic_From_Usd():
    scp(filename2)
    sleep(30)
    scp(filename7)
    sleep(30)
    scp(filename4)
    sleep(30)
    scp(filename5)
    sleep(30)
    scp(filename6)
    sleep(30)
    device.sendMsg("dd if=/dev/zero of=/dev/sdb bs=1M count=10 \n")
    device.read_until_regexp(".*records out.*",timeout=5)
    log.success("Partition Table Deleted Successfully")
    device.sendMsg("dpkg -i "+filename4+" \n")
    device.read_until_regexp(".*Setting up libparted.*",timeout=10)
    log.success("Libparted unpack Successfull")
    device.sendMsg("dpkg -i "+filename5+" \n")
    device.read_until_regexp(".*Setting up parted.*",timeout=10)
    log.success("Parted unpack Successfull")
    device.sendMsg("dd if="+filename6+" of=/dev/sdb \n")
    device.read_until_regexp(".*out.*",timeout=350)
    log.success("Image Cloned to SD Card Successfully")
    device.sendMsg("parted -l \n")
    device.read_until_regexp(".*SONiC-OS.*",timeout=20)
    log.success("Parted List print Successfully")

@logThis
def expand_Sd_Card():
    device.sendMsg("gdisk /dev/sdb \n")
    device.read_until_regexp("GPT fdisk.*version 1.0.3.*",timeout=5)
    device.sendMsg("\n")

    device.read_until_regexp("Command.*",timeout=2)
    device.sendMsg("d \r\n")

    device.read_until_regexp("Using 1.*",timeout=5)
    device.sendMsg("3 \r\n")

    device.read_until_regexp(".*print this menu.*",timeout=5)
    device.sendMsg("n \r\n")

    device.read_until_regexp("Partition number.*",timeout=5)
    device.sendMsg("1 \r\n")

    device.read_until_regexp("First sector.*",timeout=3)
    device.sendMsg("\n")

    device.read_until_regexp("Last sector.*",timeout=3)
    device.sendMsg("\n")

    device.read_until_regexp("Current type.*",timeout=3)
    device.sendMsg("\n")

    device.read_until_regexp(".*Command.*",timeout=5)
    device.sendMsg("p \r\n")

    device.read_until_regexp("Disk /dev/sdb.*",timeout=10)
    device.sendMsg("w \r\n")

    device.read_until_regexp("Final checks complete.*",timeout=3)
    device.sendMsg("Y \r\n")

    device.read_until_regexp(".*completed successfully.*",timeout=10)
    log.success("Expand SD Card Successfully")
    device.sendMsg("resize2fs -fp /dev/sdb3 8G \n")

    device.read_until_regexp("resize2fs.*",timeout=10)
    log.success("Resize fs to 8G Successfully")
    device.sendMsg("reboot \n")
    output_1=device.read_until_regexp('.*Enter an option',timeout=450)
    for i in range(1):
        try:
            d1=device.read_until_regexp('>', timeout=15)
            break
        except Exception:
            continue
    device.sendCmd("01",timeout=5)
    output_2=device.read_until_regexp(".*sonic login",timeout=100)
    if output_2:
        device.sendCmd('admin', 'Password:', timeout=15)
        device.sendCmd('pass', 'Login incorrect', timeout=15)
        device.sendCmd('admin', 'Password:', timeout=15)
        output = device.sendCmd('YourPaSsWoRd', 'admin@sonic', timeout=15)
        device.sendCmd('sudo su', 'root@sonic', timeout=15)
        for line in diagos_login_info:
            if line in output:
                continue
            else:
                raise RuntimeError('sonic login check test fail')
    else:
        raise RuntimeError('Cannot find sonic OS login line: "sonic login:"')
    sleep(30)
    checkUpdateDriverStatus()

@logThis
def checkSdb():
    c1=run_command('umount /dev/sdb*',prompt='root@sonic|admin@sonic')
    if re.search('not mounted',c1):
        log.success("Operation unmount successful")
    else:
        log.fail('Unmount failed')

    c2=run_command('echo \'type=b\' | sudo sfdisk /dev/sdb',prompt='root@sonic|admin@sonic',timeout=10)
    if re.search('Created a new GPT disklabel',c2):
        log.success('Operation successful')
    else:
        log.fail('Operation fail')
    c3=run_command('mkfs /dev/sdb1 ',prompt='Proceed')
    device.sendMsg('y \n')
    c4=device.read_until_regexp('#',timeout=30)
    q1= re.search('Allocating group tables: done',c4) and \
        re.search('Writing inode tables: done',c4) and \
        re.search('Writing superblocks and filesystem accounting information: done',c4)
    if q1:
        log.success('Operation mkfs successful')
    else:
        log.fail('Operation mkfs failed')
