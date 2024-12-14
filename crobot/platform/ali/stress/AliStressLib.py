###############################################################################
# LEGALESE:   "Copyright (C) 2021, Celestica Corp. All rights reserved."      #
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

import Logger as log
from crobot.Decorator import logThis
import CRobot

workDir = CRobot.getWorkDir()
sys.path.append(os.path.join(workDir, 'platform', 'ali', 'openbmc'))

try:
    import DeviceMgr
    from crobot.SwImage import SwImage
    from ali.openbmc import AliOpenBmcLib
except Exception as err:
    log.cprint(str(err))
device = DeviceMgr.getDevice()


@logThis
def test_10gkr_stress(test_10gkr_cmd, platform, times_500):
    for i in range(1, times_500+1):
        device.executeCmd('echo ====================Test loop %s====================' % i)
        output = device.executeCmd(test_10gkr_cmd)
        if platform == 'migaloo':
            match = re.findall('(?i)10G KR test.*(?P<result>PASS)', output)
            if not match:
                raise RuntimeError('10GKR test failed!')
        if platform == 'shamu':
            match = re.findall(r'[a-z]+_[a-z]+_[a-z]+.*?\[ PASS \]', output)
            if len(match) != 3:
                raise RuntimeError('10GKR test failed!')


@logThis
def check_network_ping_log(ping_times, log_file, os_side='cpu_side'):
    """
    This is for stress cases TS_007, TS_008 and TS_009.
    :param ping_times: ping the network times
    :param log_file: log file
    :param os_side: It should be cpu_side or bmc_side.
    """
    if os_side == 'bmc_side':
        logfile_output = device.executeCmd('bmc-exec "tail -n 50 %s"' % log_file)
    else:
        logfile_output = device.executeCmd('tail -n 50 %s' % log_file)

    send_package = re.findall(r'(\d+)\s+packets transmitted', logfile_output)[0]
    received_package = re.findall(r'packets transmitted,\s+(\d+)\s+', logfile_output)[0]
    package_loss = re.findall(r'received,\s+(.*?)\s+packet loss', logfile_output)[0]

    log_check_status = True
    if int(send_package) != ping_times:
        log_check_status = False
    if int(received_package) != ping_times:
        log_check_status = False
    if package_loss != '0%':
        log_check_status = False

    if not log_check_status:
        raise RuntimeError('The network between CPU and BMC OS test failed, some packages are missing!')


@logThis
def get_ip_addr(get_ip_cmd):
    """
    This function can get the ip address.
    :param get_ip_cmd: get the ip address DUT, for example:
    get_ip_cmd = ip addr show eth0 |grep -E "inet.*scope global eth0" |awk -F "[ /]+" '{print $3}'
    """
    output = device.executeCmd(get_ip_cmd)
    for line in output.splitlines():
        match = re.findall(r'^[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}$', line)
        if match:
            ip_address = match[0]
            break
    return ip_address


def read_cpld_reg(output):
    for line in output.splitlines():
        ret = re.findall(r'0x[0-9a-fA-F]{1,2}$', line.strip())
        if ret:
            break
    return ret[0]


def cpu_lpc_stress(platform, diag_utility_path, times_500):
    for _ in range(times_500+1):
        device.executeCmd('echo --------------times: %s---------------' % _)
        device.executeCmd('cd %s' % diag_utility_path)
        output = device.executeCmd('./lpc_cpld_x64_64 blu r 0xa100')
        base_cpld_version = read_cpld_reg(output)
        base_cpld_version = int(base_cpld_version, 16)

        output = device.executeCmd('./lpc_cpld_x64_64 blu r 0xa1e0')
        cpu_cpld_version = read_cpld_reg(output)
        cpu_cpld_version = int(cpu_cpld_version, 16)
        sw_cpld = list()
        if platform == 'migaloo':
            for i in range(1, 7):
                device.executeCmd('cd /sys/devices/platform/AS*.switchboard/CPLD%s' % i)
                output = device.executeCmd('cat getreg')
                sw_cpld.append(read_cpld_reg(output))
        else:
            for i in range(1, 3):
                device.executeCmd('cd /sys/devices/platform/AS*.switchboard/CPLD%s' % i)
                output = device.executeCmd('cat getreg')
                sw_cpld.append(read_cpld_reg(output))
        if len(list(set(sw_cpld))) != 1:
            raise RuntimeError('check the Switch/linecard failed!')
        sw_cpld = int(sw_cpld[0], 16)
        exp_base_cpld_version = int(SwImage.getSwImage(SwImage.BASE_CPLD).newVersion, 16)
        exp_cpu_cpld_version = int(SwImage.getSwImage(SwImage.COME_CPLD).newVersion, 16)
        exp_sw_cpld_version = int(SwImage.getSwImage(SwImage.SWITCH_CPLD).newVersion, 16)
        if base_cpld_version != exp_base_cpld_version:
            raise RuntimeError('base cpld version check failed!')
        if cpu_cpld_version != exp_cpu_cpld_version:
            raise RuntimeError('cpu cpld version check failed!')
        if sw_cpld != exp_sw_cpld_version:
            raise RuntimeError('switch & linecard cpld check failed!')

        device.executeCmd('cd %s' % diag_utility_path)
        output1 = device.executeCmd('./lpc_cpld_x64_64 blu w 0xa1e1 0xde;./lpc_cpld_x64_64 blu r 0xa1e1')
        output1 = read_cpld_reg(output1)
        output2 = device.executeCmd('./lpc_cpld_x64_64 blu w 0xa101 0xde;./lpc_cpld_x64_64 blu r 0xa101')
        output2 = read_cpld_reg(output2)
        if output1 != '0xde' or output2 != '0xde':
            raise RuntimeError('read CPLD register failed!')

        output1 = device.executeCmd('./lpc_cpld_x64_64 blu w 0xa1e1 0x21;./lpc_cpld_x64_64 blu r 0xa1e1')
        output1 = read_cpld_reg(output1)
        output2 = device.executeCmd('./lpc_cpld_x64_64 blu w 0xa101 0x21；./lpc_cpld_x64_64 blu r 0xa101')
        output2 = read_cpld_reg(output2)
        if output1 != '0x21' or output2 != '0x21':
            raise RuntimeError('R/W CPLD register failed!')


@logThis
def cpu_reset_check_info(platform, diag_i2c_test_pattern, cpld_test_pattern, lspci_list_count):
    """
    For DIAG OS Reboot/power cycle/AC power cycle stress, etc.
    Check the CPU side info.
    """
    device.executeCmd('bmc-exec "ifconfig eth0 192.168.0.11"')
    device.executeCmd('ifconfig eth0 192.168.0.10')
    time.sleep(1)
    device.executeCmd('ping -c 4 192.168.0.11')
    output = device.executeCmd('echo $?')
    exit_num = re.findall(r'\r\n0\r\n', output)
    if not exit_num:
        raise RuntimeError('CPU OS ping OpenBmc failed!')
    output = device.executeCmd('fdisk -l')
    fdisk_check_1 = re.findall(r'/dev/sda', output)
    fdisk_check_2 = re.findall(r'/dev/sdb', output)
    if not fdisk_check_1:
        raise RuntimeError('fdisk -l check failed!')
    if not fdisk_check_2:
        raise RuntimeError('Can not check the USB device!')
    if platform == 'migaloo':
        device.executeCmd('cd /usr/local/migaloo/CPU_Diag')
        output = device.executeCmd('./cel-i2c-test --all', timeout=120)
        i2c_test = re.findall(diag_i2c_test_pattern, output)
        output = device.executeCmd('./cel-cpld-test -a')
        cpld_test = re.findall(cpld_test_pattern, output)
        output = device.executeCmd('./cel-pci-test --all')
        pci_test = re.findall(r'\s+PCIe test.*?\[ PASS \]', output)
        output = device.executeCmd('./cel-version-test -S')
        base_cpld = re.findall(r'BaseBoard.*?:\s+(.*)\s+', output)
        cpu_cpld = re.findall(r'COMe CPLD.*?:\s+(.*)\s+', output)
        fan_cpld = re.findall(r'FAN.*?:\s+(.*)\s+', output)
        sw_cpld = re.findall(r'SW CPLD1.*?:\s+(.*)\s+', output)
        top_lc_cpld = re.findall(r'Top Line CPLD1.*?:\s+(.*)\s+', output)
        bot_lc_cpld = re.findall(r'BOT Line CPLD1.*?:\s+(.*)\s+', output)
        fpga_version = re.findall(r'FPGA.*?:\s+(.*)\s+', output)
        output = device.executeCmd('./cel-cpu-frequency-test -a')
        cpu_freq_result = re.findall(r'CPU Frequency.*?\[ PASS \]', output)
        if not cpu_freq_result:
            raise RuntimeError('check CPU Frequency failed!')
    else:
        device.executeCmd('cd /usr/local/CPU_Diag/bin')
        output = device.executeCmd('./cel-i2c-test -t')
        i2c_test = re.findall(diag_i2c_test_pattern, output)
        output = device.executeCmd('./cel-cpld-test -t')
        cpld_test = re.findall(cpld_test_pattern, output, re.S)
        output = device.executeCmd('./cel-cpld-test -v')
        base_cpld = re.findall(r'Base board.*?:\s+(.*)\s+', output)
        cpu_cpld = re.findall(r'COMe.*?:\s+(.*)\s+', output)
        sw_cpld = re.findall(r'Switch CPLD-1.*?:\s+(.*)\s+', output)
        output = device.executeCmd('./cel-fpga-test -v')
        fpga_version = re.findall(r'FPGA Version:\s+(.*)\s*', output)
        output = device.executeCmd('./cel-pcie-test -t')
        pci_test = re.findall(r'\s+PCI Test.*?\[ PASS \]', output)
        device.executeCmd('cd /usr/local/CPU_Diag/auto_test_tool')
        output = device.executeCmd('./cel-CPU-test')
        cpu_info_patten = r'CPU socket.*?\[ PASS \].*?CPU processor.*?\[ PASS \].*?CPU core.*?\[ PASS \].*?CPU model.*?\[ PASS \]'
        cpu_check_result = re.findall(cpu_info_patten, output, re.S)
        if not cpu_check_result:
            raise RuntimeError('Check CPU info failed!')
    if not i2c_test:
        raise RuntimeError('i2c test failed!')
    if not cpld_test:
        raise RuntimeError('cpld test failed!')
    if not pci_test:
        raise RuntimeError('pci test failed!')
    if base_cpld[0].strip('\r') != SwImage.getSwImage(SwImage.BASE_CPLD).newVersion:
        raise RuntimeError('BASE CPLD version check failed! The current ver: %s, The Exp ver: %s' % (base_cpld[0], \
        SwImage.getSwImage(SwImage.BASE_CPLD).newVersion))
    if cpu_cpld[0].strip('\r') != SwImage.getSwImage(SwImage.COME_CPLD).newVersion:
        raise RuntimeError('CPU CPLD version check failed! The current ver: %s, The Exp ver: %s' % (cpu_cpld[0], \
        SwImage.getSwImage(SwImage.COME_CPLD).newVersion))
    if sw_cpld[0].strip('\r') != SwImage.getSwImage(SwImage.SWITCH_CPLD).newVersion:
        raise RuntimeError('Switch CPLD version check failed!')
    if platform == 'migaloo':
        if fan_cpld[0].strip('\r') != SwImage.getSwImage(SwImage.FAN_CPLD).newVersion:
            raise RuntimeError('FAN CPLD version check failed!')
        # The SWITCH & TOP Line & BOT Line CPLD use one image, so they have same version.
        if top_lc_cpld[0].strip('\r') != SwImage.getSwImage(SwImage.SWITCH_CPLD).newVersion:
            raise RuntimeError('TOP Line Card CPLD vershon check failed!')
        if bot_lc_cpld[0].strip('\r') != SwImage.getSwImage(SwImage.SWITCH_CPLD).newVersion:
            raise RuntimeError('BOT Line Card CPLD vershon check failed!')
    if fpga_version[0].strip('\r') != SwImage.getSwImage(SwImage.FPGA).newVersion:
        raise RuntimeError('FPGA version check failed!')
    output = device.executeCmd('curl -g http://240.1.1.1:8080/api/bmc/info | python -m json.tool')
    bmc_info = re.findall(r'Flash.*?master.*"status":\s+"OK"', output, re.S)
    if not bmc_info:
        raise RuntimeError('Check BMC info failed!')
    output = device.executeCmd('bmc-exec "wedge_power.sh status"')
    power_status = re.findall(r'Microserver power is on', output)
    if not power_status:
        raise RuntimeError('Check COMe status is failed!')
    output = device.executeCmd(r"""curl -d '{"Command":"fru-util sys"}' http://240.1.1.1:8080/api/hw/rawcmd |python -m json.tool""")
    sys_fru_info = re.findall(r'data.*?message.*?OK.*?status.*?OK', output, re.S)
    if not sys_fru_info:
        raise RuntimeError('Read sys fru info failed!')
    output = device.executeCmd(r"""curl -g http://240.1.1.1:8080/api/fan/info | python -m json.tool""")
    fan_info = re.findall(r'data.*?message.*?OK.*?status.*?OK', output, re.S)
    if not fan_info:
        raise RuntimeError('Read fan info failed!')
    device.executeCmd(r'lspci')
    output = device.executeCmd(r'lspci |wc -l')
    lspci_list_num = re.findall(r'\r\n(\d+)\r\n', output)
    if lspci_list_num[0] != lspci_list_count:
        raise RuntimeError('Check lspci list failed! Exp list count: %s, current list count: %s' % (lspci_list_count, lspci_list_num[0]))


@logThis
def check_bmc_restful():
    for i in range(1, 15):
        output = device.executeCmd('bmc-exec "ifconfig eth0.4088"')
        if re.findall(r'240.1.1.1', output):
            break
        time.sleep(30)
        if i == 14:
            raise RuntimeError("Check the bmc restful failed!")


@logThis
def bmc_ddr_stress_test(bmc_ddr_result_pattern, loops):
    output = device.executeCmd('memtester 300M %s' % loops, timeout=int(loops) * 180 * 60)
    list_result = re.findall(bmc_ddr_result_pattern, output, re.S)
    if len(list_result) != int(loops):
        raise RuntimeError("BMC DDR stress test failed! Test loops: %s, Pass loops: %s" % (loops, len(list_result)))


@logThis
def bmc_reset_check_info(platform):
    device.executeCmd('source /usr/local/bin/openbmc-utils.sh')
    output = device.executeCmd('version_dump')
    cur_bmc_ver = re.findall(r'AliBMC-odm-obmc-cl-v(.*)\s+', output)
    exp_bmc_ver = SwImage.getSwImage(SwImage.BMC).newVersion
    if cur_bmc_ver[0].strip('\r') != exp_bmc_ver:
        raise RuntimeError('BMC version error! Current ver: %s, Exp ver: %s' % (cur_bmc_ver[0], exp_bmc_ver))
    output = device.executeCmd('boot_info.sh')
    bmc_boot_flash = re.findall(r'Master Flash', output)
    if not bmc_boot_flash:
        raise RuntimeError('The bmc boot flash is not Master Flash!')
    output = device.executeCmd('come_boot_info')
    come_boot_flash = re.findall(r'boots OK.*?Master flash', output, re.S)
    if not come_boot_flash:
        raise RuntimeError(r'Check COMe boot info failed!')
    device.executeCmd('cd /var/log/BMC_Diag/bin/')
    output = device.executeCmd('./cel-i2c-test -s', timeout=120)
    i2c_test_result = re.findall(r'All the I2C devices test.*?\[ PASS \]', output)
    if not i2c_test_result:
        raise RuntimeError('bmc i2c test failed!')
    if platform == 'migaloo':
        output = device.executeCmd('./cel-power-monitor-test -a')
        power_monitor = re.findall(r'Power monitor test.*\[ PASS \]', output)
        output = device.executeCmd(r'./cel-temperature-test -a')
        temp_test_result = re.findall(r'Temperature test.*\[ PASS \]', output)
    else:
        # platform == 'shamu'
        output = device.executeCmd('./cel-power-monitor-test -t')
        power_monitor = re.findall(r'Power monitor test.*\[ PASS \]', output)
        output = device.executeCmd('./cel-temperature-test -t')
        temp_test_result = re.findall(r'Temperature test.*\[ PASS \]', output)
    if not power_monitor:
        raise RuntimeError("Power monitor test failed!")
    if not temp_test_result:
        raise RuntimeError('Temperature test failed!')
    output = device.executeCmd('sensors')
    match = re.findall(r'N/A', output)
    if match:
        raise RuntimeError('Failed, some sensors status is: N/A')


@logThis
def bios_update_test(flash_type, bios_file, is_bios_ver_new=False, upgrade=True):
    upgrade_version = SwImage.getSwImage(SwImage.BIOS).newVersion
    downgrade_version = SwImage.getSwImage(SwImage.BIOS).oldVersion
    output = device.executeCmd('dmidecode -s bios-version')
    bios_version = re.findall(r'D0000\.(.*)\s+', output)
    output = device.executeCmd(r'curl -g http://240.1.1.1:8080/api/misc/biosbootstatus |python -m json.tool')
    bios_flash = re.findall(r'Flash.*?:.*?"(.*?)",\s+', output)
    if bios_flash[0] != str(flash_type):
        raise RuntimeError('The BIOS flash is not "%s" flash!' % flash_type)
    if is_bios_ver_new:
        if bios_version[0].strip('\r') != upgrade_version:
            raise RuntimeError('BIOS version is incorrect! Cur ver: %s, Exp ver: %s' % (bios_version[0], upgrade_version))
    if not is_bios_ver_new:
        if bios_version[0].strip('\r') != downgrade_version:
            raise RuntimeError('BIOS version is incorrect! Cur ver: %s, Exp ver: %s' % (bios_version[0], downgrade_version))
    if upgrade:
        device.executeCmd("""curl -d '{"Name":"bios","Flash":"%s","Path":"%s"}' \
        http://240.1.1.1:8080/api/firmware/upgrade |python -m json.tool""" % (flash_type, bios_file), timeout=360)
    else:
        device.executeCmd("""curl -d '{"Name":"bios","Flash":"%s","Path":"%s"}' \
        http://240.1.1.1:8080/api/firmware/upgrade |python -m json.tool""" % (flash_type, bios_file), timeout=360)


@logThis
def check_bmc_info(flash_type, bmc_version):
    """
    This function check the BMC boot info and bmc version.
    :param flash_type: master/slave
    :param bmc_version: bmc version
    """
    output = device.executeCmd('boot_info.sh')
    boot_info = re.findall(r'%s Flash' % flash_type, output, re.I)
    if not boot_info:
        raise RuntimeError('Failed, the bmc boot info should be "%s"' % flash_type)
    output = device.executeCmd('version_dump')
    cur_bmc_version = re.findall(r'OpenBMC Release AliBMC.*?-v%s' % bmc_version, output)
    if not cur_bmc_version:
        raise RuntimeError('Failed, the bmc version should be "%s"' % bmc_version)


@logThis
def update_bmc(bmc_image, flash_dev):
    output = device.executeCmd('flashcp -v %s %s' % (bmc_image, flash_dev), timeout=1200)
    match = re.findall(r'Verifying kb:.*?\(100%\)', output)
    if not match:
        raise RuntimeError('Failed, Update BMC failed!')


@logThis
def sensor_reading_stress(sensor_lines, test_time):
    start_time = time.time()
    while time.time() - start_time < test_time:
        output = device.executeCmd(r'sensors')
        match = re.findall(r'N/A', output)
        if match:
            raise RuntimeError('Failed, some sensors status is: N/A')
        output = device.executeCmd(r'sensors |wc -l')
        lines = re.findall(r'\r\n\d+\r\n', output)
        if lines[0].strip() != sensor_lines:
            raise RuntimeError('Failed, sensors lines is not correct! Exp: %s, Cur: %s' % (sensor_lines, lines[0].strip()))

@logThis
def fpga_update(image_name):
    """
    Update FPGA in SONiC OS
    :param image_name: The FPGA image name.
    """
    output = device.executeCmd('fpga_prog %s' % image_name, timeout=120)
    match = re.findall(r'Programing finish', output)
    if not match:
        raise RuntimeError('FPGA update failed, cannot find the msg "Programing finish".')

@logThis
def check_fpga_version(check_version_path, cmd, fpga_version):
    device.executeCmd('cd %s' % check_version_path)
    output = device.executeCmd('%s' % cmd)
    version_match = re.findall(r"FPGA\s*Version\s*:\s*(.*?)\r", output, re.I)
    if version_match[0].strip() != fpga_version:
        raise RuntimeError('Check FPGA version failed, Exp: %s, Cur: %s' % (fpga_version, version_match[0].strip()))

@logThis
def check_basecpld_version(check_version_path, read_cpld_cmd, version_new_or_old='new'):
    device.executeCmd('cd %s' % check_version_path)
    output = device.executeCmd('%s' % read_cpld_cmd)
    base_cpld_version = re.findall(r'Base.*?CPLD.*?(0x.*?)\r', output, re.I)[0].strip()
    exp_base_cpld_version = eval("SwImage.getSwImage(SwImage.BASE_CPLD).%sVersion" % version_new_or_old)
    if base_cpld_version != exp_base_cpld_version:
        raise RuntimeError('Check basecpld version failed, Exp: %s, Cur: %s' % (exp_base_cpld_version,
                                                                                base_cpld_version))

@logThis
def check_all_cpld_version(platform, version_new_or_old='new'):
    if platform == 'migaloo':
        device.executeCmd('cd /usr/local/migaloo/CPU_Diag/')
        output = device.executeCmd(r'./cel-version-test -S')
        base_cpld_version = re.findall(r'Base.*?CPLD.*?(0x.*?)\r', output, re.I)[0].strip()
        cpu_cpld_version = re.findall(r'COMe.*?CPLD.*?(0x.*?)\r', output, re.I)[0].strip()
        fan_cpld_version = re.findall(r'FAN.*?CPLD.*?(0x.*?)\r', output, re.I)[0].strip()
        switch_cpld_version = re.findall(r'SW.*?CPLD.*?(0x.*?)\r', output, re.I)[0].strip()
        top_line_cpld_version = re.findall(r'TOP.*?CPLD.*?(0x.*?)\r', output, re.I)[0].strip()
        bot_line_cpld_version = re.findall(r'BOT.*?CPLD.*?(0x.*?)\r', output, re.I)[0].strip()
    if platform == 'shamu':
        device.executeCmd('cd /usr/local/CPU_Diag/bin/')
        output = device.executeCmd('./cel-cpld-test -v')
        base_cpld_version = re.findall(r'Base.*?CPLD.*?(0x.*?)\r', output, re.I)[0].strip()
        cpu_cpld_version = re.findall(r'COMe.*?CPLD.*?(0x.*?)\r', output, re.I)[0].strip()
        switch_cpld_version = re.findall(r'SW.*?CPLD.*?(0x.*?)\r', output, re.I)[0].strip()
        output = device.executeCmd('bmc-exec version_dump')
        fan_cpld_version = re.findall(r'FAN.*?CPLD.*?(0x.*?)\r', output, re.I)[0].strip()
    exp_base_cpld_version = eval("SwImage.getSwImage(SwImage.BASE_CPLD).%sVersion" % version_new_or_old)
    exp_cpu_cpld_version = eval("SwImage.getSwImage(SwImage.COME_CPLD).%sVersion" % version_new_or_old)
    exp_fan_cpld_version = eval("SwImage.getSwImage(SwImage.FAN_CPLD).%sVersion" % version_new_or_old)
    exp_switch_cpld_version = eval("SwImage.getSwImage(SwImage.SWITCH_CPLD).%sVersion" % version_new_or_old)
    if base_cpld_version != exp_base_cpld_version:
        raise RuntimeError('Failed, expected base cpld: %s, current base cpld: %s' % (exp_base_cpld_version,
                                                                                      base_cpld_version))
    if cpu_cpld_version != exp_cpu_cpld_version:
        raise RuntimeError('Failed, expected cpu cpld: %s, current cpu cpld: %s' % (exp_cpu_cpld_version,
                                                                                    cpu_cpld_version))
    if int(fan_cpld_version, 16) != int(exp_fan_cpld_version, 16):
        raise RuntimeError('Failed, expected fan cpld: %s, current fan cpld: %s' % (exp_fan_cpld_version,
                                                                                    fan_cpld_version))
    if switch_cpld_version != exp_switch_cpld_version:
        raise RuntimeError('Failed, expected switch cpld: %s, current switch cpld: %s' % (exp_switch_cpld_version,
                                                                                          switch_cpld_version))
    if platform == 'migaloo':
        # shamu no line card cpld, migaloo line card cpld version and switch cpld are the same.
        if top_line_cpld_version != exp_switch_cpld_version:
            raise RuntimeError('Failed, expected top line cpld: %s, current top line cpld: %s' %
                               (exp_switch_cpld_version, top_line_cpld_version))
        if bot_line_cpld_version != exp_switch_cpld_version:
            raise RuntimeError('Failed, expected bot line cpld: %s, current bot line cpld: %s' %
                               (exp_switch_cpld_version, bot_line_cpld_version))


def update_cpld_in_openbmc(program_cpld_cmd, refresh_cpld_cmd):
    device.sendCmd('python', '>>>', timeout=20)
    device.sendCmd('from hal.hal_firmware import *', '>>>', timeout=20)
    device.sendCmd('a=HalFirmware()')
    device.sendCmd('%s' % program_cpld_cmd, '\r\n0\r\n>>>', timeout=90*60)
    device.sendCmd('%s' % refresh_cpld_cmd, 'sonic login:', timeout=20*60)


def update_fpga_in_openbmc(program_fpga_cmd):
    device.sendCmd('python', '>>>', timeout=20)
    device.sendCmd('from hal.hal_firmware import *', '>>>', timeout=20)
    device.sendCmd('a=HalFirmware()')
    device.sendCmd('%s' % program_fpga_cmd, '\r\n0\r\n>>>', timeout=20 * 60)
    device.sendCmd('exit()', 'root@bmc', timeout=10)


def check_exit_code(error_msg='The exit code is not 0', exit_code_0=True):
    output = device.executeCmd('echo $?')
    exit_code = re.findall(r'\r\n0\r\n', output)
    if exit_code_0:
        if not exit_code:
            raise RuntimeError(error_msg)
    if not exit_code_0:
        if exit_code:
            raise RuntimeError(error_msg)


def fru_info_reading_stress(platform, times_500):
    device.executeCmd('mkdir -p /var/log/STRESS')
    device.executeCmd('cd /var/log/STRESS')
    device.executeCmd('fru-util psu -a 2>&1 |tee -a psu_fru_standard_file')
    device.executeCmd('fru-util fan 1 2>&1 |tee -a fan_fru_standard_file')
    device.executeCmd('fru-util fan 2 2>&1 |tee -a fan_fru_standard_file')
    device.executeCmd('fru-util fan 3 2>&1 |tee -a fan_fru_standard_file')
    device.executeCmd('fru-util fan 4 2>&1 |tee -a fan_fru_standard_file')
    device.executeCmd('fru-util fan 5 2>&1 |tee -a fan_fru_standard_file')
    device.executeCmd('fru-util switch 2>&1 |tee -a switch_fru_standard_file')
    device.executeCmd('fru-util sys 2>&1 |tee -a sys_fru_standard_file')
    device.executeCmd('fru-util bmc 2>&1 |tee -a bmc_fru_standard_file')
    device.executeCmd('fru-util fb 2>&1 |tee -a fcb_fru_standard_file')
    device.executeCmd('fru-util come |tee -a come_fru_standard_file')
    if platform == 'migaloo':
        device.executeCmd('cd /var/log/BMC_Diag/utility/linecard_fru_eeprom')
        device.executeCmd('./eeprom_tool -d -l 1 |tee -a /var/log/STRESS/linecard_fru_standard_file')
        device.executeCmd('./eeprom_tool -d -l 2 |tee -a /var/log/STRESS/linecard_fru_standard_file')
    for i in range(times_500+1):
        device.executeCmd('cd /var/log/STRESS')
        device.executeCmd('rm -rf *current*')
        device.executeCmd('fru-util psu -a 2>&1 |tee -a psu_fru_current_file')
        device.executeCmd('fru-util fan 1 2>&1 |tee -a fan_fru_current_file')
        device.executeCmd('fru-util fan 2 2>&1 |tee -a fan_fru_current_file')
        device.executeCmd('fru-util fan 3 2>&1 |tee -a fan_fru_current_file')
        device.executeCmd('fru-util fan 4 2>&1 |tee -a fan_fru_current_file')
        device.executeCmd('fru-util fan 5 2>&1 |tee -a fan_fru_current_file')
        device.executeCmd('fru-util switch 2>&1 |tee -a switch_fru_current_file')
        device.executeCmd('fru-util sys 2>&1 |tee -a sys_fru_current_file')
        device.executeCmd('fru-util bmc 2>&1 |tee -a bmc_fru_current_file')
        device.executeCmd('fru-util fb 2>&1 |tee -a fcb_fru_current_file')
        device.executeCmd('fru-util come |tee -a come_fru_current_file')
        if platform == 'migaloo':
            device.executeCmd('cd /var/log/BMC_Diag/utility/linecard_fru_eeprom')
            device.executeCmd('./eeprom_tool -d -l 1 |tee -a /var/log/STRESS/linecard_fru_current_file')
            device.executeCmd('./eeprom_tool -d -l 2 |tee -a /var/log/STRESS/linecard_fru_current_file')
            device.executeCmd('cd /var/log/STRESS')
            device.executeCmd('diff linecard_fru_current_file linecard_fru_standard_file')
            check_exit_code('The linecard fru reading error!')
        device.executeCmd('diff psu_fru_current_file psu_fru_standard_file')
        check_exit_code('The psu fru reading error!')
        device.executeCmd('diff fan_fru_current_file fan_fru_standard_file')
        check_exit_code('The fan fru reading error!')
        device.executeCmd('diff switch_fru_current_file switch_fru_standard_file')
        check_exit_code('The switch fru reading error!')
        device.executeCmd('diff sys_fru_current_file sys_fru_standard_file')
        check_exit_code('The sys fru reading error!')
        device.executeCmd('diff bmc_fru_current_file bmc_fru_standard_file')
        check_exit_code('The bmc fru reading error!')
        device.executeCmd('diff fcb_fru_current_file fcb_fru_standard_file')
        check_exit_code('The fcb fru readling error!')
        device.executeCmd('diff come_fru_current_file come_fru_standard_file')
        check_exit_code('The come fru reading error!')


@logThis
def switchBmcFlash(bmc_flash):
    return AliOpenBmcLib.switchBmcFlash(bmc_flash)


@logThis
def DiagOSConnect():
    device.loginDiagOS()
    return

@logThis
def DiagOSDisconnect():
    device.disconnect()
    return
