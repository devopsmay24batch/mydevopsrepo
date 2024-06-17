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
sys.path.append(os.path.join(workDir, 'platform', 'ali'))
from crobot import Logger as log
try:
    from common.commonlib import CommonLib
    from common.commonlib import CommonKeywords
    from AliSonicVariable import *
    from AliCommonVariable import *
    import DeviceMgr
    from crobot.SwImage import SwImage
    from crobot.Decorator import logThis
except Exception as err:
    log.cprint(traceback.format_exc())

device = DeviceMgr.getDevice()


@logThis
def loginDevice():
    device.loginDiagOS()
    device.sendCmd('sudo su')


@logThis
def sonicDisconnect():
    return device.disconnect()


@logThis
def check_driver_tree(interfaces, os_cmd='ls'):
    output = device.executeCmd(os_cmd)
    log.cprint(output)
    interfaces_1 = []
    for interface in interfaces:
        if interface not in output:
            interfaces_1.append(interface)
    if not interfaces_1:
        log.success('check driver tree successfully.')
    else:
        raise RuntimeError('can not find interfaces:  ' + str(interfaces))


@logThis
def check_poap_file(poap_file):
    output = device.executeCmd('ls')
    log.cprint(output)
    interfaces_1 = []
    for interface in poap_file:
        if interface not in output:
            interfaces_1.append(interface)
    if not interfaces_1:
        log.success('check_fpga_driver_tree successfully.')
    else:
        raise RuntimeError('can not find interfaces: ' + str(poap_file))


@logThis
def read_fpga_version():
    device.executeCmd('echo 0x0000 > getreg')
    output = device.executeCmd(cat_getreg_cmd)
    match = re.search(r'0x\d+', output)
    if not match:
        raise RuntimeError('can not parse fpga version!')
    version = match.group(0).strip()
    expected_version = SwImage.getSwImage(SwImage.FPGA).newVersion
    if version != expected_version:
        raise RuntimeError('current version {} is not match the expected version {}!'.format(version, expected_version))
    else:
        log.success('read_fpga_version successfully.')


@logThis
def write_fpga_register():
    device.executeCmd('echo "0x0004 0x02" > setreg')
    device.executeCmd('echo 0x0004 > getreg')
    output = device.executeCmd(cat_getreg_cmd)
    if '0x00000002' in output:
        log.success('write_fpga_register successfully.')
    else:
        raise RuntimeError('write_fpga_register failed!')


@logThis
def read_cpld_version(read_version_cmd, cpld_name):
    output = device.executeCmd(read_version_cmd)
    match = re.search(r'0x[0-9a-fA-F]{2}', output)
    if not match:
        raise RuntimeError('can not parse cpld version!')
    version = match.group(0).strip()
    expected_version = SwImage.getSwImage(cpld_name).newVersion
    if version != expected_version:
        raise RuntimeError('current version {} is not match the expected version {}!'.format(version, expected_version))
    else:
        log.success('read_cpld_version successfully.')


@logThis
def write_cpld_register():
    output_1 = device.executeCmd(cat_scratch_cmd)
    device.executeCmd('echo 0xdf > scratch')
    output_2 = device.executeCmd(cat_scratch_cmd)
    if '0xde' in output_1:
        log.success('read_cpld_register successfully.')
    else:
        raise RuntimeError('read_cpld_register failed!')
    if '0xdf' in output_2:
        log.success('write_cpld_register successfully.')
    else:
        raise RuntimeError('write_cpld_register failed!')


@logThis
def check_sys_led(sys_led, sys_led_color):
    output_1 = device.executeCmd('cat sys_led')
    match1 = ''
    for line1 in output_1.splitlines():
        match1 = re.search("^on$|^off$|^1k$|^4k$", line1)
        if match1:
            log.cprint("system led is %s"%(match1.group(0)))
            break

    output_2 = device.executeCmd('cat sys_led_color')
    match2 = ''
    for line2 in output_2.splitlines():
        match2 = re.search("^off$|^yellow$|^green$|^both$", line2)
        if match2:
            log.cprint("system led color is %s"%(match2.group(0)))
            break

    if not match1 or not match2:
        raise RuntimeError('can not get sys led status!')
    current_sys_led = match1.group(0).strip()
    current_sys_led_color = match2.group(0).strip()
    expected_sys_led = sys_led
    expected_sys_led_color = sys_led_color
    if current_sys_led != expected_sys_led and current_sys_led_color != expected_sys_led_color:
        raise RuntimeError('current sys led {} and color {} are not match the expected sys led {} {}!'.format(\
            current_sys_led, current_sys_led_color, expected_sys_led, expected_sys_led_color))
    else:
        log.success('sys led status is correct.')


@logThis
def change_sys_led_command():
    device.executeCmd('echo "0xa162 0xCD" > setreg', timeout=5)
    check_sys_led(led_1k_blink, led_both)
    device.executeCmd('echo "0xa162 0xCE" > setreg', timeout=5)
    check_sys_led(led_4k_blink, led_both)
    device.executeCmd('echo "0xa162 0xDC" > setreg', timeout=5)
    check_sys_led(led_on, led_green)
    device.executeCmd('echo "0xa162 0xDD" > setreg', timeout=5)
    check_sys_led(led_1k_blink, led_green)
    device.executeCmd('echo "0xa162 0xDE" > setreg', timeout=5)
    check_sys_led(led_4k_blink, led_green)
    device.executeCmd('echo "0xa162 0xDF" > setreg', timeout=5)
    check_sys_led(led_off, led_green)
    device.executeCmd('echo "0xa162 0xEC" > setreg', timeout=5)
    check_sys_led(led_on, led_yellow)
    device.executeCmd('echo "0xa162 0xED" > setreg', timeout=5)
    check_sys_led(led_1k_blink, led_yellow)
    device.executeCmd('echo "0xa162 0xEE" > setreg', timeout=5)
    check_sys_led(led_4k_blink, led_yellow)
    device.executeCmd('echo "0xa162 0xEF" > setreg', timeout=5)
    check_sys_led(led_off, led_yellow)
    device.executeCmd('echo "0xa162 0xFF" > setreg', timeout=5)
    check_sys_led(led_off, led_off)
    device.sendCmd('bmc-exec "psu_off_on.sh -a"', 'sonic login', timeout=350)
    device.sendCmd('admin', 'Password', timeout=5)
    device.sendCmd('admin', 'admin@sonic', timeout=5)
    device.sendCmd('sudo su', 'root@sonic', timeout=5)


@logThis
def diagos_login_check():
    output = device.sendCmd('reboot', 'sonic login', timeout=240)
    sleep(10)
    if 'sonic login' in output:
        device.sendCmd('admin', 'Password:', timeout=15)
        output = device.sendCmd('admin', 'admin@sonic', timeout=15)
        device.sendCmd('sudo su', 'root@sonic', timeout=15)
        for line in diagos_login_info:
            if line in output:
                continue
            else:
                raise RuntimeError('sonic login check test fail')
    else:
        raise RuntimeError('Cannot find sonic OS login line: "sonic login:"')


@logThis
def sonic_booting_info_check(platform):
    """
    reboot sonic and check booting info!
    """
    output = device.sendCmd('reboot', 'sonic login', timeout=240)
    device.sendCmd('admin', 'Password', timeout=5)
    device.sendCmd('admin', 'admin@sonic', timeout=5)
    device.sendCmd('sudo su', 'root@sonic', timeout=5)
    if 'error' in output or 'fail' in output:
        raise RuntimeError('sonic booting info has error or fail string:', re.findall(r'.*?fail.*|.*?error.*', output))
    biosVer = re.findall(r'BIOS Date: .*? Ver: D0000.(.*?)\s+', output)
    cpu_cpld = re.findall(r'CPLD_C  Ver: (.*?)\s+', output)
    base_cpld = re.findall(r'CPLD_B  Ver: (.*?)\s+', output)
    cpu_cpld = '0x' + cpu_cpld[0].replace('.', '')
    if platform == 'migaloo':
        base_cpld = int(base_cpld[0].strip('0.'))
    if platform == 'shamu':
        base_cpld = int(base_cpld[0].replace('.', ''), 16)
    expected_bios = SwImage.getSwImage(SwImage.BIOS).newVersion
    expected_base_cpld = int(SwImage.getSwImage(SwImage.BASE_CPLD).newVersion, 16)
    expected_cpu_cpld = SwImage.getSwImage(SwImage.COME_CPLD).newVersion
    if biosVer[0] != expected_bios:
        raise RuntimeError('BIOS version check failed, expected version: %s' % expected_bios)
    if cpu_cpld != expected_cpu_cpld:
        raise RuntimeError('CPU CPLD version check failed, expected version: %s' % expected_cpu_cpld)
    if base_cpld != expected_base_cpld:
        raise RuntimeError('Base CPLD version check failed, expected version: %s' % SwImage.getSwImage\
            (SwImage.BASE_CPLD).newVersion)


@logThis
def check_sonic_version(show_version_cmd, sonic_name):
    output = device.executeCmd(show_version_cmd)
    for line in output.splitlines():
        line = line.strip()
        match = re.search('SONiC Software Version', line)
        if match:
            log.success('Successfully find SONiC Software Version')
            break

    if not match:
        log.fail('can not find sonic version!')
        raise RuntimeError('can not find sonic version!')

    expected_version = SwImage.getSwImage(sonic_name).newVersion
    if expected_version not in line:
        raise RuntimeError('current version is not match the expected version {}!'.format(expected_version))
    else:
        log.success('check sonic version %s successfully.'%(expected_version))

@logThis
def check_software_version(platform):
    fw_version = device.executeCmd('./get_fw_version.py')
    cpu_cpld = re.search(r'CPLD_C\'.*?\'(.*?)\'', fw_version).group(1).replace(r'.', '')
    fan_cpld = re.search(r'CPLD_FAN\'.*?\'(.*?)\'', fw_version).group(1).replace(r'.', '')
    bmc_version = re.search(r'bmc_version:.*?-v(.*)', fw_version).group(1).strip()
    bios_version = re.search(r'bios_version.*?\.(.*)', fw_version).group(1).strip()
    onie_version = re.search(r'onie_version: (.*)', fw_version).group(1).strip()
    fpga_version = re.search(r'fpga_version:\s*(.*)', fw_version).group(1).strip()
    fpga_version_major = int(fpga_version.split('.')[0])
    fpga_version_minor = int(fpga_version.split('.')[1])

    expect_base_cpld = hex(int(SwImage.getSwImage(SwImage.BASE_CPLD).newVersion, 16))
    expect_cpu_cpld = SwImage.getSwImage(SwImage.COME_CPLD).newVersion.replace('0x', '')
    expect_fan_cpld = SwImage.getSwImage(SwImage.FAN_CPLD).newVersion.replace('0x', '')
    expect_switch_cpld = str(int(SwImage.getSwImage(SwImage.SWITCH_CPLD).newVersion, 16))
    expect_bmc_version = SwImage.getSwImage(SwImage.BMC).newVersion
    expect_bios_version = SwImage.getSwImage(SwImage.BIOS).newVersion
    expect_onie_version = SwImage.getSwImage(SwImage.ONIE).newVersion
    expect_fpga_version = SwImage.getSwImage(SwImage.FPGA).newVersion.replace('0x', '')
    expect_fpga_version_major = int(expect_fpga_version[:4], 16)
    expect_fpga_version_minor = int(expect_fpga_version[4:], 16)

    fail_cnt = 0
    if platform == 'migaloo':
        base_cpld = hex(int(re.search(r'CPLD_B\'.*?\'(.*?)\'', fw_version).group(1).replace(r'0.', '')))
        cpld1 = re.search(r'CPLD_1\'.*?\'(.*?)\'', fw_version).group(1).replace('0.', '')
        cpld2 = re.search(r'CPLD_2\'.*?\'(.*?)\'', fw_version).group(1).replace('0.', '')
        cpld3 = re.search(r'CPLD_3\'.*?\'(.*?)\'', fw_version).group(1).replace('0.', '')
        cpld4 = re.search(r'CPLD_4\'.*?\'(.*?)\'', fw_version).group(1).replace('0.', '')
        cpld5 = re.search(r'CPLD_5\'.*?\'(.*?)\'', fw_version).group(1).replace('0.', '')
        cpld6 = re.search(r'CPLD_6\'.*?\'(.*?)\'', fw_version).group(1).replace('0.', '')
        if len(set([cpld1, cpld2, cpld3, cpld4, cpld5, cpld6])) != 1 or cpld1 != expect_switch_cpld:
            fail_cnt = 1
            log.fail('Check switchcpld failed')

    if platform == 'shamu':
        base_cpld = hex(int(re.search(r'CPLD_B\'.*?\'(.*?)\'', fw_version).group(1).replace(r'.', ''), 16))
        cpld1 = re.search(r'CPLD_1\'.*?\'(.*?)\'', fw_version).group(1).replace(r'.', '').lstrip('0')
        cpld2 = re.search(r'CPLD_2\'.*?\'(.*?)\'', fw_version).group(1).replace(r'.', '').lstrip('0')
        if len(set([cpld1, cpld2])) != 1 or cpld1 != expect_switch_cpld:
            fail_cnt = 1
            log.fail('Check switchcpld failed')

    if base_cpld != expect_base_cpld:
        fail_cnt = 1
        log.fail('Check basecpld failed!')
    if cpu_cpld != expect_cpu_cpld:
        fail_cnt = 1
        log.fail('Check cpucpld failed!')
    if fan_cpld != expect_fan_cpld:
        fail_cnt = 1
        log.fail('Check fancpld failed!')
    if bmc_version != expect_bmc_version:
        fail_cnt = 1
        log.fail('Check bmc version failed!')
    if bios_version != expect_bios_version:
        fail_cnt = 1
        log.fail('check bios version failed!')
    if fpga_version_major != expect_fpga_version_major or fpga_version_minor != expect_fpga_version_minor:
        fail_cnt = 1
        log.fail('Check fpga version failed!')
    if onie_version != expect_onie_version:
        fail_cnt = 1
        log.fail('check onie failed!')
    if fail_cnt:
        raise RuntimeError('Check fw version failed!')


@logThis
def check_cpu_and_memory_info():
    device.executeCmd('cat /proc/cpuinfo')
    model_name_check = device.executeCmd('cat /proc/cpuinfo |grep "Intel(R) Xeon(R) CPU D-1533N @ 2.10GHz" |wc -l')
    model_name_check = re.findall(r'\n(12)\r', model_name_check)
    if not model_name_check:
        raise RuntimeError('The cpu model name or processor count is not right, expected model name: \
        Intel(R) Xeon(R) CPU D-1533N @ 2.10GHz, expected processor count: 12')
    microcode_check = device.executeCmd('cat /proc/cpuinfo |grep -E "microcode.*?0xe00000f" |wc -l')
    microcode_check = re.findall(r'\n(12)\r', microcode_check)
    if not microcode_check:
        raise RuntimeError('The microcode or processor count is not right, expected microcode: 0xe00000f, \
        expected count: 12')
    cache_size = device.executeCmd('cat /proc/cpuinfo | grep -E "cache size.*?9216 KB" |wc -l')
    cache_size = re.findall(r'\n(12)\r', cache_size)
    if not cache_size:
        raise RuntimeError('The cache size or processor count is not right, expected cache: 9216 KB, expected count: 12')
    cpu_processor_info = device.executeCmd('cat /proc/cpuinfo | grep processor')
    cpu_processor_count = ''
    for line in cpu_processor_info.splitlines():
        cpu_processor = re.search(r'^processor.*:(.*)', line)
        if cpu_processor:
            cpu_processor_count = int(cpu_processor.group(1).strip())
    if not cpu_processor_count:
        raise RuntimeError('can not parse cpu processor count!')
    log.cprint('cpu processor count is: %d'%(cpu_processor_count))
    if 11 == cpu_processor_count:
        log.cprint('cpu processor count %d is correct'%(cpu_processor_count+1))
    else:
        raise RuntimeError('cpu processor count %d is not correct'%(cpu_processor_count+1))

    cpu_frequence_info = device.executeCmd('cat /proc/cpuinfo | grep "cpu MHz"')
    cpu_frequence_list = []
    for line in cpu_frequence_info.splitlines():
        cpu_frequence = re.search(r'^cpu MHz.*:(.*)', line)
        if cpu_frequence:
            cpu_frequence = float(cpu_frequence.group(1).strip())
            cpu_frequence_list.append(cpu_frequence)
    if not cpu_frequence_list:
        raise RuntimeError('can not parse cpu frequence!')
    log.cprint("cpu frequence list is %s"%cpu_frequence_list)

    cpu_frequence_loop = 0
    cpu_frequence_check_fail = 0
    for cpu_frequence in cpu_frequence_list:
        if cpu_frequence < 2000 or cpu_frequence > 2100:
            cpu_frequence_check_fail = 1
            log.fail("cpu %d frequence %f is not correct"%(cpu_frequence_loop, cpu_frequence))
        cpu_frequence_loop += 1
    if 1 == cpu_frequence_check_fail:
        raise RuntimeError("cpu frequence check fail")
    else:
        log.cprint("cpu frequence check pass")

    memory_info = device.executeCmd('cat /proc/meminfo')
    memory_size = ''
    for line in memory_info.splitlines():
        memory_size = re.search(r'MemTotal:(.*)kB', line)
        if memory_size:
            memory_size = int(memory_size.group(1).strip())
            break
    if not memory_size:
        raise RuntimeError('can not parse memory size!')
    log.cprint('memory size is: %ld'%(memory_size))
    if 7*1024*1024 <= memory_size <= 8*1024*1024:
        log.cprint('memory size check pass')
    else:
        raise RuntimeError('memory size %ld check fail'%(memory_size))

@logThis
def check_tlv_eeprom_info(platform):
    tlv_eeprom_info = device.executeCmd('show platform syseeprom')
    ifconfig = device.executeCmd('ifconfig')
    actual_tlv = {}
    product_name = ''
    for line in tlv_eeprom_info.splitlines():
        product_name = re.search(r'Product Name(.*)', line)
        if product_name:
            product_name = product_name.group(1).split()[2].strip()
            break
    if not product_name:
        log.fail('can not parse product name!')
    log.cprint('product name is: %s'%product_name)
    actual_tlv['Product Name'] = product_name

    part_number = ''
    for line in tlv_eeprom_info.splitlines():
        part_number = re.search(r'Part Number(.*)', line)
        if part_number:
            part_number = part_number.group(1).split()[2].strip()
            break
    if not part_number:
        log.fail('can not parse part number!')
    log.cprint('part number is: %s'%part_number)
    actual_tlv['Part Number'] = part_number

    base_mac_address = ''
    for line in tlv_eeprom_info.splitlines():
        base_mac_address = re.search(r'Base MAC Address(.*)', line)
        if base_mac_address:
            base_mac_address = base_mac_address.group(1).split()[2].strip()
            break
    if not base_mac_address:
        log.fail('can not parse base mac address!')
    log.cprint('base mac address is: %s'%base_mac_address)
    actual_tlv['Base MAC Address'] = base_mac_address

    device_version = ''
    for line in tlv_eeprom_info.splitlines():
        device_version = re.search(r'Device Version(.*)', line)
        if device_version:
            device_version = device_version.group(1).split()[2].strip()
            break
    if not device_version:
        log.fail('can not parse device version!')
    log.cprint('device version is: %s'%device_version)
    actual_tlv['Device Version'] = device_version

    label_revision = ''
    for line in tlv_eeprom_info.splitlines():
        label_revision = re.search(r'Label Revision(.*)', line)
        if label_revision:
            label_revision = label_revision.group(1).split()[2].strip()
            break
    if not label_revision:
        log.fail('can not parse label revision!')
    log.cprint('label revision is: %s'%label_revision)
    actual_tlv['Label Revision'] = label_revision

    platform_name = ''
    for line in tlv_eeprom_info.splitlines():
        platform_name = re.search(r'Platform Name(.*)', line)
        if platform_name:
            platform_name = platform_name.group(1).split()[2].strip()
            break
    if not platform_name:
        log.fail('can not parse platform name!')
    log.cprint('platform name is: %s'%platform_name)
    actual_tlv['Platform Name'] = platform_name

    onie_version = ''
    for line in tlv_eeprom_info.splitlines():
        onie_version = re.search(r'ONIE Version(.*)', line)
        if onie_version:
            onie_version = onie_version.group(1).split()[2].strip()
            break
    if not onie_version:
        log.fail('can not parse onie version!')
    log.cprint('onie version is: %s'%onie_version)
    actual_tlv['ONIE Version'] = onie_version

    mac_addresses = ''
    for line in tlv_eeprom_info.splitlines():
        mac_addresses = re.search(r'MAC Addresses(.*)', line)
        if mac_addresses:
            mac_addresses = mac_addresses.group(1).split()[2].strip()
            break
    if not mac_addresses:
        log.fail('can not parse mac addresses!')
    log.cprint('mac addresses is: %s'%mac_addresses)
    actual_tlv['MAC Addresses'] = mac_addresses

    manufacturer = ''
    for line in tlv_eeprom_info.splitlines():
        manufacturer = re.search(r'Manufacturer(.*)', line)
        if manufacturer:
            manufacturer = manufacturer.group(1).split()[2].strip()
            break
    if not manufacturer:
        log.fail('can not parse manufacturer!')
    log.cprint('manufacturer is: %s'%manufacturer)
    actual_tlv['Manufacturer'] = manufacturer

    manufacture_country = ''
    for line in tlv_eeprom_info.splitlines():
        manufacture_country = re.search(r'Manufacture Country(.*)', line)
        if manufacture_country:
            manufacture_country = manufacture_country.group(1).split()[2].strip()
            break
    if not manufacture_country:
        log.fail('can not parse manufacture country!')
    log.cprint('manufacture country is: %s'%manufacture_country)
    actual_tlv['Manufacture Country'] = manufacture_country

    vendor_name = ''
    for line in tlv_eeprom_info.splitlines():
        vendor_name = re.search(r'Vendor Name(.*)', line)
        if vendor_name:
            vendor_name = vendor_name.group(1).split()[2].strip()
            break
    if not vendor_name:
        log.fail('can not parse vendor name!')
    log.cprint('vendor name is: %s'%vendor_name)
    actual_tlv['Vendor Name'] = vendor_name

    diag_version = ''
    for line in tlv_eeprom_info.splitlines():
        diag_version = re.search(r'Diag Version(.*)', line)
        if diag_version:
            diag_version = diag_version.group(1).split()[2].strip()
            break
    if not diag_version:
        log.fail('can not parse diag version!')
    log.cprint('diag version is: %s'%diag_version)
    actual_tlv['Diag Version'] = diag_version

    service_tag = ''
    for line in tlv_eeprom_info.splitlines():
        service_tag = re.search(r'Service Tag(.*)', line)
        if service_tag:
            service_tag = service_tag.group(1).split()[2].strip()
            break
    if not service_tag:
        log.fail('can not parse service_tag!')
    log.cprint('service_tag is: %s'%service_tag)
    actual_tlv['Service Tag'] = service_tag

    expected_tlv_eeprom = CommonLib.get_eeprom_cfg_dict('TLV_EEPROM_INFO')
    ifconfig = re.search(r'eth0:.*?ether(.*)', ifconfig, re.S)
    ether = ifconfig.group(1).split()[0].upper()
    log.cprint('ether is: %s'%ether)
    expected_tlv_eeprom['Base MAC Address'] = ether

    if platform == 'migaloo':
        device.executeCmd('cd /usr/local/migaloo/CPU_Diag')
        version_info = device.executeCmd('./cel-version-test -S')
        expected_diag_version = re.findall(r'Diag Version.*?: (.*)', version_info)[0].strip()
        expected_onie_version = re.findall(r'Onie Version.*?01\.(.*)', version_info)[0].strip()
        expected_tlv_eeprom['Diag Version'] = expected_diag_version
        expected_tlv_eeprom['ONIE Version'] = expected_onie_version
    if platform == 'shamu':
        device.executeCmd('cd /usr/local/CPU_Diag/bin')
        version_info = device.executeCmd('./cel-software-test -i')
        expected_diag_version = re.findall(r'Diag version.*?shamu-(.*)', version_info)[0].strip()
        expected_onie_version = re.findall(r'onie_version.*?01\.(.*)', version_info)[0].strip()
        expected_tlv_eeprom['Diag Version'] = expected_diag_version
        expected_tlv_eeprom['ONIE Version'] = expected_onie_version

    mismatch = False
    for key in actual_tlv.keys():
        if expected_tlv_eeprom[key] != actual_tlv[key]:
            log.error('mismatched item: {}, expected: {}, found: {}'.format(key, expected_tlv_eeprom[key], actual_tlv[key]))
            mismatch = True
    if mismatch:
        raise RuntimeError('Find mistacmed items')

@logThis
def check_loopback_temperature():
    sfp_presence_info = device.executeCmd('sfputil show presence')
    loopback_temperature_info = device.executeCmd('/usr/local/etc/read_optic_temp.py')
    loopback1_temperature_info = device.executeCmd('/usr/local/etc/read_optic_temp.py -p 1')

    sfp_presence = ''
    sfp_presence_list = []
    for line in sfp_presence_info.splitlines():
        sfp_presence = re.search(r'Ethernet.*?\s(.*)', line)
        if sfp_presence:
            sfp_presence = sfp_presence.group(1).strip()
            sfp_presence_list.append(sfp_presence)
    if not sfp_presence_list:
        raise RuntimeError('can not parse sfp presence!')
    log.cprint("sfp presence list is %s"%sfp_presence_list)

    port_number = 1
    port_number_list = []
    sfp_presence_check_fail = 0
    for sfp_presence in sfp_presence_list:
        if sfp_presence != 'Present':
            sfp_presence_check_fail = 1
            port_number_list.append(port_number)
        port_number += 1
    if 1 == sfp_presence_check_fail:
        log.fail("sfp not present list is %s"%port_number_list)
        raise RuntimeError('some sfp are not present!')

    loopback_temperature = ''
    loopback_temperature_list = []
    for line in loopback_temperature_info.splitlines():
        loopback_temperature = re.search(r'QSFP.*?\|(.*)\|', line)
        if loopback_temperature:
            loopback_temperature = float(loopback_temperature.group(1).strip())
            loopback_temperature_list.append(loopback_temperature)
    if not loopback_temperature_list:
        raise RuntimeError('can not parse loopback temperature!')
    log.cprint("loopback temperature list is %s"%loopback_temperature_list)

    loopback_number = 1
    loopback_number_list = []
    loopback_temperature_check_fail = 0
    for loopback_temperature in loopback_temperature_list:
        if loopback_temperature < 10 or loopback_temperature > 80:
            loopback_temperature_check_fail = 1
            loopback_number_list.append(loopback_number)
        loopback_number += 1
    if 1 == loopback_temperature_check_fail:
        log.fail("loopback number which temperature is too low or too high list is %s"%loopback_number_list)
        raise RuntimeError('loopback temperature check fail!')

    loopback1_temperature = ''
    for line in loopback1_temperature_info.splitlines():
        loopback1_temperature = re.search(r'QSFP.*?\|(.*)\|', line)
        if loopback1_temperature:
            loopback1_temperature = float(loopback1_temperature.group(1).strip())
            break
    if not loopback1_temperature:
        raise RuntimeError('can not parse loopback 1 temperature!')
    log.cprint("loopback 1 temperature is %f"%loopback1_temperature)

    loopback1_temperature_check_fail = 0
    if loopback1_temperature < 10 or loopback1_temperature > 80:
        loopback1_temperature_check_fail = 1
        log.fail("loopback 1 temperature %f is too low or too high"%loopback1_temperature)
        raise RuntimeError('loopback 1 temperature check fail!')

@logThis
def set_port_register(phy_port_cfg_list):
    for port_num in range(1, 21):
        offset = 80 + port_num - 1
        cmd = "echo 0x%d 0x%02x > setreg" \
              % (offset, phy_port_cfg_list[port_num-1])
        log.cprint("SET: %s" % cmd)
        device.executeCmd(cmd)
        sleep(1)

        # Read it back
        cmd = "echo 0x%d > getreg" %offset
        log.cprint("GET: %s" % cmd)
        device.executeCmd(cmd)

        cmd = "cat getreg"
        log.cprint("GET: %s" % cmd)
        output = device.executeCmd(cmd)
        read_value = "0xff"
        for line in output.splitlines():
            read_value = re.search(r'^0x(.*)', line)
            if read_value:
                read_value = read_value.group().strip()
                break

        msg = "Set port %2d with value %d, read back %s" % (port_num, \
              phy_port_cfg_list[port_num-1], read_value)
        log.cprint(msg)

        set_value = "0x%02x" %phy_port_cfg_list[port_num-1]
        if set_value != read_value:
            raise RuntimeError('write CPLD register value fail!')

    log.cprint("Set and Get done.")


@logThis
def sonic_sensors_info_check(platform):
    """
    Arguments: platform -> migaloo or shamu
    """
    device.executeCmd('cd /usr/local/etc/')
    output = device.executeCmd('python platformutil.py sensor status')
    if platform == 'migaloo':
        actual_ok_count = re.findall(r'.*? OK .*?', output)
        if 96 != len(actual_ok_count):
            raise RuntimeError('Check sensors info failed!')
    if platform == 'shamu':
        actual_ok_count = re.findall(r'.*? OK .*?', output)
        if 59 != len(actual_ok_count):
            raise RuntimeError('Check sensors info failed!')


@logThis
def test_CPLD_read_write():
    register_value_1 = [
        1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
        1, 1, 1, 1, 1, 1, 1, 1, 1, 1
    ]
    register_value_2 = [
        2, 2, 2, 2, 2, 2, 2, 2, 2, 2,
        2, 2, 2, 2, 2, 2, 2, 2, 2, 2
    ]

    set_port_register(register_value_2)
    set_port_register(register_value_1)
