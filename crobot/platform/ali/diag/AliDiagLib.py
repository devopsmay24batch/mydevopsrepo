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

import Logger as log
from crobot.Decorator import logThis
import CommonLib
import time
import os
import re
import Const
import AliConst
import CommonKeywords
from crobot.SwImage import SwImage
from crobot.Server import Server

devicename = os.environ.get("deviceName", "")
if "shamu" in devicename.lower():
    import AliDiagShamuVariable as shamu_var

try:
    import DeviceMgr
except Exception as err:
    log.cprint(str(err))

device = DeviceMgr.getDevice()

@logThis
def DiagOSConnect():
    device.loginDiagOS()
    return

@logThis
def DiagOSDisconnect():
    device.disconnect()
    return

@logThis
def avsOptionHelpTest():
    script_path = '/var/log/BMC_Diag/bin'
    device.sendCmd('cd ' + script_path)
    time.sleep(1)
    test_pattern1 = '-h show this help'
    test_pattern2 = '-t test AVS'
    command = './cel-avs-test -h'
    output = CommonLib.execute_command(command, timeout=60)
    log.info('output = %s ' %output)

    match1 = re.search(test_pattern1, output)
    match2 = re.search(test_pattern2, output)
    if match1 and match2:
        log.success('AVS Test Pass!')
    else:
        log.fail('AVS Option H Test Failed!')
        device.raiseException("Test avs fail!")

@logThis
def avsOptionTest():

    script = './cel-avs-test -t'
    output = CommonLib.execute_command(script, timeout=60)
    pattern = 'AVS test.*?PASS'
    match = re.search(pattern, output)
    if match:
        log.success('AVS Test Pass!')
    else:
        log.fail('AVS Option T Test Failed!')
        device.raiseException("Test avs fail!")

@logThis
def checkFanEepromInfo():
    path = '/var/log/BMC_Diag/utility/fan_fru_eeprom/'
    device.sendCmd('cd ' + path)
    for port in range(1,7):
        eeprom_tool_cmd = './eeprom_tool -d -f ' +str(port)
        output = CommonLib.execute_command(eeprom_tool_cmd, timeout=60)
        pattern = 'FAN\_\d FRU EEPROM ...'
        match = re.search(pattern, output)
        if match:
            log.debug('Fan eeprom port %s check pass!' % port)
        else:
            log.error('Fan eeprom port %s check fail!' % port)
            device.raiseException("Check fan eeprom info failed!")
    for port2 in range(1,7):
        fru_util_cmd = 'fru-util fan ' + str(port2)
        output2 = CommonLib.execute_command(fru_util_cmd, timeout=60)
        match2 = re.search('fail|error|no such file', output, re.I)
        if match2:
            log.error('Fru-util port %s check fail!' % port2)
            device.raiseException("Check fan eeprom info failed!")
        else:
            log.debug('Fru-util port %s check pass!' % port2)
            log.success("Check fan eeprom info pass!")

@logThis
def test40Loopback(port_pattern):
    path = '/usr/local/CPU_Diag/bin/'
    device.sendCmd('cd ' + path)

    count = 0
    test_cmd = './cel-port-test -P'
    output = CommonLib.execute_command(test_cmd, timeout=120)
    for line in output.splitlines():
        line = line.strip()
        for i in range(0, len(port_pattern)):
            match = re.search(port_pattern[i], line)
            if match:
                count += 1
    if count == len(port_pattern):
        log.success("40 ports status normal.")
    else:
        log.fail("port check fail, please check output!")
        device.raiseException("port check fail, please check output!")

@logThis
def checkConfighwskuFile():
    init_command = 'ls -l /usr/local/bin/config-hwsku.sh'
    output = CommonLib.execute_command(init_command, timeout=10)
    count = 0
    if '(?i)no such file' in output:
        log.debug("Cannot found /usr/local/bin/config-hwsku.sh")
        device.raiseException('Cannot found /usr/local/bin/config-hwsku.sh')
    else:
        limit_cmd = 'chmod 777 /usr/local/bin/config-hwsku.sh'
        device.sendCmd(limit_cmd)
        time.sleep(3)
        output = CommonLib.execute_command(init_command, timeout=10)
        match = re.search('-rwxrwxrwx', output)
        if match:
            log.debug('Modified the file success.')
            count = 1
    #copy the file to /home/admin
    if count == 1:
        device.sendCmd('cd /home/admin')
        cp_cmd = 'cp /usr/local/bin/config-hwsku.sh ./'
        time.sleep(3)
        device.sendCmd(cp_cmd)
        test_cmd = 'config-hwsku.sh -h '
        output = CommonLib.execute_command(test_cmd,timeout=60)
        hwsku_pattern = r'Usage\:[ \t]+config\-hwsku\.sh[ \t]+options[ \t]+\(\-h\|\-s\)'
        match2 = re.search(hwsku_pattern,output)
        if match2:
            log.debug('Copy & Test config-hwsku.sh pass!')
        else:
            device.raiseException('Check config-hwsku.sh fail!')
    else:
        device.raiseException('Output have log fail, please check!')

@logThis
def checkPortConsistent():
    device.sendCmd('killall -9 bcm.user')
    device.execCmd('config-hwsku.sh -s ' + '8x200G+64x25G')
    output = get_ps_result()
    CommonKeywords.should_match_ordered_regexp_list(output, [r'xe\d+.*?25G.*?RS528' for i in range(0, 64)])
    CommonKeywords.should_match_ordered_regexp_list(output, [r'cd\d+.*?200G.*?RS544-2xN' for i in range(0, 8)])
    device.execCmd('cel_bcmshell exit')

    device.sendCmd('killall -9 bcm.user')
    device.execCmd('config-hwsku.sh -s ' + '16x200G+48x50G')
    output = get_ps_result()
    CommonKeywords.should_match_ordered_regexp_list(output, [r'xe\d+.*?50G.*?RS528' for i in range(0, 48)])
    CommonKeywords.should_match_ordered_regexp_list(output, [r'cd\d+.*?200G.*?RS544-2xN' for i in range(0, 16)])
    device.execCmd('cel_bcmshell exit')

    device.sendCmd('killall -9 bcm.user')
    device.execCmd('config-hwsku.sh -s ' + '16x200G+48x100G')
    output = get_ps_result()
    CommonKeywords.should_match_ordered_regexp_list(output, [r'ce\d+.*?100G.*?RS544-1xN' for i in range(0, 48)])
    CommonKeywords.should_match_ordered_regexp_list(output, [r'cd\d+.*?200G.*?RS544-2xN' for i in range(0, 16)])
    device.execCmd('cel_bcmshell exit')

    device.sendCmd('killall -9 bcm.user')
    device.execCmd('config-hwsku.sh -s ' + '16x200G+24x100G')
    output = get_ps_result()
    CommonKeywords.should_match_ordered_regexp_list(output, [r'ce\d+.*?100G.*?RS528' for i in range(0, 24)])
    CommonKeywords.should_match_ordered_regexp_list(output, [r'cd\d+.*?200G.*?RS544-2xN' for i in range(0, 16)])
    device.execCmd('cel_bcmshell exit')

@logThis
def get_ps_result():
    device.sendCmd('cel_bcmshell ps')
    output = device.read_until_regexp('xe\d+\( 78\).*?BASE-R', timeout=60)
    device.sendCmd('')
    return output

@logThis
def runAliDiagCenter():
    cmd = 'Ali_Diag -m rack'
    output = CommonLib.execute_command(cmd, timeout=1200)
    if 'Ali Test Fail Items....' in output:
        device.raiseException('There are some failure in output, please check!')
    else:
        log.debug('Rack Test Pass!')
    e_cmd = 'efibootmgr'
    output2 = CommonLib.execute_command(e_cmd,timeout=60)
    match_pattern = 'Boot.*?ONIE'
    match = re.search(match_pattern, output)
    if match:
        log.success('Rack Test Pass!')
    else:
        log.fail('Booting not ONIE')
        device.raiseException('Booting not ONIE')

@logThis
def emmcOptionHelpTest():
    emmc_path = '/var/log/BMC_Diag/utility/stress/'
    device.sendCmd('cd '+ emmc_path)
    cmd = './emmc_stress_test.sh -h'
    output = CommonLib.execute_command(cmd, timeout=60)
    match_pattern = 'Usage\:[ \t]+\.\/emmc\_stress\_test\.sh[ \t]+options.*?'
    unknown_pattern = 'unknown option'
    match = re.search(match_pattern, output)
    if unknown_pattern in output:
        device.raiseException('Unknown option, please check output!')
    elif match:
        log.success('Check option h pass!')
    else:
        device.raiseException('Unknown issue.')

@logThis
def emmcOptionTest():
    cmd = './emmc_stress_test.sh -t'
    output = CommonLib.execute_command(cmd, timeout = 3600)
    pattern = 'EMMC[ \t]+writing\/reading[ \t]+test[ \t]+Pass'
    match = re.search(pattern, output)
    if match:
        log.success('Check option t pass!')
    else:
        log.fail('command emmc_stress_test -t output have errors.')
        device.raiseException("command emmc_stress_test -t output have errors.")

@logThis
def emmcOptionCTest():
    cmd = './emmc_stress_test.sh -c'
    CommonLib.execute_command(cmd)

@logThis
def ddrOptionTest():
    ddr_path = '/var/log/BMC_Diag/utility/stress/'
    device.sendCmd('cd ' + ddr_path)
    cmd = './DDR_test.sh 60 60'
    output = CommonLib.execute_command(cmd, timeout=180)
    pattern = 'Status\:[ \t]+PASS'
    match = re.search(pattern,output)
    if match:
        log.success("DDR Stress Test check pass!")
    else:
        device.raiseException("DDR Stress Test check fail")

@logThis
def catDdrLog():
    cat_cmd = 'cat DDR_stress_test.log'
    output = CommonLib.execute_command(cat_cmd, timeout=180)
    pattern = 'Status\:[ \t]+PASS'
    match = re.search(pattern, output)
    if match:
        log.success("DDR Stress Test check pass!")
    else:
        device.raiseException("DDR Stress Test check fail")

def rtcOptionTest(param):
    device.sendCmd('cd /var/log/BMC_Diag/bin/')
    cmd = './cel-RTC-test ' + str(param)
    output = CommonLib.execute_command(cmd, timeout=60)
    fail_match = re.search('error|fail', output, re.I)
    if fail_match:
        device.raiseException('RTC test fail.')
    else:
        log.success('RTC test pass.')

@logThis
def ifconfigAndCat(param):
    output = CommonLib.execute_command('ifconfig')
    match = re.search('eth0',output,re.I)
    if not match:
        device.raiseException('ifconfig output have fails.')
    else:
        log.debug('ifconfig successed!')
        cmd = 'cat /etc/issue'
        output2 = CommonLib.execute_command(cmd,timeout=60)
        if param == 'openbmc':
            pass_pattern = 'OpenBMC[ \t]+Release[ \t]+AliBMC\-odm\-obmc\-cl\-v2.*?'
        elif param == 'diagos':
            pass_pattern = 'Debian[ \t]+GNU\/Linux.*?'
        match = re.search(pass_pattern, output2)
        if match:
            log.success('cat /etc/issue passed.')
        else:
            device.raiseException('cat /etc/issue failed.')

@logThis
def check_address_info():
    path = '/usr/local/CPU_Diag/bin/'
    device.sendCmd('cd ' + path)
    test_cmd = './cel-internal-usb-test'
    output = CommonLib.execute_command(test_cmd, timeout=120)
    math = r'Internal USB .*?PASS'
    match = re.search(math, output)
    if match:
        log.success("Internal USB Test Pass!")
    else:
        log.fail("Internal USB Test, please check output!")
        device.raiseException("port check fail, please check output!")

@logThis
def check_openbmc_master_info():
    path = 'source /usr/local/bin/openbmc-utils.sh'
    device.sendCmd(path)
    test_cmd = 'boot_info.sh'
    output = CommonLib.execute_command(test_cmd, timeout=120)
    re_math = r'Current.*Master Flash'
    math = re.search(re_math, output)
    if math:
        log.success("Master Bmc Pass")
    else:
        log.fail("Master Bmc Test, please check output!")
        device.raiseException("Master Bmc Test, please check output!")

@logThis
def check_openbmc_slave_info():
    path = 'source /usr/local/bin/openbmc-utils.sh'
    device.sendCmd(path)
    test_cmd = 'boot_info.sh'
    output = CommonLib.execute_command(test_cmd, timeout=120)
    re_math = r'Current.*Slave Flash'
    math = re.search(re_math, output)
    if math:
        log.success("Slave Bmc Pass")
    else:
        log.fail("Slave Bmc Test, please check output!")
        device.raiseException("Slave Bmc Test, please check output!")

@logThis
def boot_from_slave_openbmc(mode=Const.BOOT_MODE_OPENBMC, timeout=AliConst.BOOT_TIME):
    device.getPrompt(mode)
    device.sendCmd('source /usr/local/bin/openbmc-utils.sh')
    device.transmit("boot_from slave")
    output = device.read_until_regexp('login:', timeout)
    device.getPrompt(mode)
    time.sleep(40)
    return output


@logThis
def boot_from_master_openbmc(mode=Const.BOOT_MODE_OPENBMC, timeout=AliConst.BOOT_TIME):
    device.getPrompt(mode)
    device.sendCmd('source /usr/local/bin/openbmc-utils.sh')
    device.transmit("boot_from master")
    output = device.read_until_regexp('login:', timeout)
    device.getPrompt(mode)
    time.sleep(40)
    return output

@logThis
def check_openbmc_master_bios():
    path = 'source /usr/local/bin/openbmc-utils.sh'
    device.sendCmd(path)
    test_cmd = 'come_boot_info'
    output = CommonLib.execute_command(test_cmd, timeout=120)
    re_math = r'COMe.*BIOS Master flash'
    math = re.search(re_math, output)
    if math:
        log.success("BIOS Master Pass")
    else:
        log.fail("BIOS Master Test, please check output!")
        device.raiseException("BIOS Master Test, please check output!")

@logThis
def check_openbmc_slave_bios():
    path = 'source /usr/local/bin/openbmc-utils.sh'
    device.sendCmd(path)
    test_cmd = 'come_boot_info'
    output = CommonLib.execute_command(test_cmd, timeout=120)
    re_math = r'COMe.*BIOS Slave flash'
    math = re.search(re_math, output)
    if math:
        log.success("BIOS Slave Pass")
    else:
        log.fail("BIOS Slave Test, please check output!")
        device.raiseException("BIOS Slave Test, please check output!")

@logThis
def come_reset_slave():
    cmd = 'come_reset slave'
    device.sendCmd(cmd)

@logThis
def come_reset_master():
    cmd='come_reset master'
    device.sendCmd(cmd)

@logThis
def cel_emmc_test():
    path_cmd = 'cd /var/log/BMC_Diag/bin/'
    output = CommonLib.execute_command(path_cmd, timeout=120)
    if re.search("No such file", output):
        log.fail("Didn't found PATH, please check it!")
    else:
        test_cmd = './cel-emmc-test -h'
        output = CommonLib.execute_command(test_cmd, timeout=120)
        if 'error' in output or 'fail' in output:
            log.fail("EMMC test -h, please check output!")
            device.raiseException("EMMC  test -h, Didn't found PATH"
                                  "please check output!")
        else:
            log.success("EMMC test -h  pass")

@logThis
def cel_emmc_info():
    test_cmd1 = './cel-emmc-test -i'
    output = CommonLib.execute_command(test_cmd1, timeout=120)
    if 'error' in output or 'fail' in output:
        log.fail("EMMC test -i, please check output!")
        device.raiseException("EMMC  test -i, please check output!")

    else:
        log.success("EMMC test -i  pass")
    test_cmd2 = './cel-emmc-test -s'
    output = CommonLib.execute_command(test_cmd2, timeout=120)
    re_math = r'.*MB'
    math = re.search(re_math, output)
    if math:
        log.success("EMMC test -s Pass")
    else:
        log.fail("EMMC  test -s, please check output!")
        device.raiseException("EMMC  test -s, please check output!")

@logThis
def cel_emmc_pass():
    test_cmd1 = './cel-emmc-test -t'
    output = CommonLib.execute_command(test_cmd1, timeout=120)
    re_math = r' EMCC.*PASS'
    math = re.search(re_math, output)
    if math:
        log.success("EMMC-test -t  Pass")
    else:
        log.fail("EMMC-test -t, please check output!")
        device.raiseException("EMMC-test -t, please check output!")

@logThis
def check_help_option():
    path_cmd = 'cd /var/log/BMC_Diag/bin/'
    output = CommonLib.execute_command(path_cmd, timeout=120)
    if re.search("No such file", output):
        log.fail("Didn't found PATH, please check output!")
        device.raiseException("Didn't found PATH, please check output!")
    else:
        test_cmd = './cel-temperature-test -h'
        output = CommonLib.execute_command(test_cmd, timeout=120)
        if 'error' in output or 'fail' in output:
            log.fail("temperature-test -h, please check output!")
            device.raiseException("temperature-test -h, please check output!")
        else:
            log.success("temperature-test -h  pass")

@logThis
def run_cmd_sensors():
    cmd='sensors'
    output = CommonLib.execute_command(cmd, timeout=120)
    if 'error' in output or 'fail' in output:
        log.fail("run cmd sensors, please check output!")
        device.raiseException("run cmd sensors, please check output!")
    else:
        log.success("run cmd sensors Pass")

@logThis
def cel_temperature_test():
    test_cmd = './cel-temperature-test -t'
    output = CommonLib.execute_command(test_cmd, timeout=120)
    re_math = r'Temperature.*PASS'
    if re.search(re_math, output):
        log.success("temperature-test -t Pass")
    else:
        log.fail("temperature-test -t, please check output!")
        device.raiseException("temperature-test -t, please check output!")

@logThis
def check_power_monitor():
    path_cmd = 'cd /var/log/BMC_Diag/bin/'
    output = CommonLib.execute_command(path_cmd, timeout=120)
    if re.search("No such file", output):
        log.fail("Didn't found PATH, please check output!")
        device.raiseException("Didn't found PATH, please check output!")
    else:
        test_cmd = './cel-power-monitor-test -h'
        output = CommonLib.execute_command(test_cmd, timeout=120)
        if 'error' in output or 'fail' in output:
            log.fail("./cel-power-monitor-test -h, please check output!")
            device.raiseException("./cel-power-monitor-test -h, please check output!")
        else:
            log.success("./cel-power-monitor-test -h  pass")

@logThis
def run_power_monitor():
    test_cmd = './cel-power-monitor-test -t'
    output = CommonLib.execute_command(test_cmd, timeout=120)
    re_math = r'Power.*PASS'
    if re.search(re_math, output):
        log.success("power monitor test -t Pass")
    else:
        log.fail("power monitor test -t, please check output!")
        device.raiseException("power monitor test -t, please check output!")

@logThis
def run_cmd_sensors():
    cmd = 'sensors'
    output = CommonLib.execute_command(cmd, timeout=120)
    if 'error' in output or 'fail' in output:
        log.fail("run cmd sensors, please check output!")
        device.raiseException("run cmd sensors, please check output!")
    else:
        log.success("run cmd sensors Pass")

@logThis
def check_OS_version():
    cmd = 'show version'
    output = CommonLib.execute_command(cmd, timeout=120)
    if re.search('command not found', output):
        log.fail(" command not found , please check output!")
        device.raiseException("command not found, please check output!")
    elif 'error' in output or 'fail' in output:
        log.fail("run cmd show version, please check output!")
        device.raiseException("run cmd show version, please check output!")
    else:
        log.success("run cmd show version Pass")

@logThis
def run_version_dump():
    test_cmd = 'version_dump'
    output = CommonLib.execute_command(test_cmd, timeout=120)
    if re.search('command not found', output):
        log.fail(" command not found , please check output!")
        device.raiseException("command not found, please check output!")
    elif 'error' in output or 'fail' in output:
        log.fail("run version dump, please check output!")
        device.raiseException("run version dump, please check output!")
    else:
        log.success("run version dump Pass")

@logThis
def check_software_test():
    path_cmd='cd /var/log/BMC_Diag/bin/'
    output = CommonLib.execute_command(path_cmd, timeout=120)
    if re.search("No such file", output):
        log.fail("Didn't found PATH, please check it!")
    else:
        test_cmd = './cel-software-test -h '
        output = CommonLib.execute_command(test_cmd, timeout=120)
        if 'error' in output or 'fail' in output:
            log.fail("cel software test -h, please check output!")
            device.raiseException("cel software test -h, please check output!")
        else:
            log.success("cel software test -h  pass")
    test_cmd1='cel-software-test -i'
    output=CommonLib.execute_command(test_cmd1,timeout=120)
    if 'error' in output or 'fail' in output:
        log.fail("cel software test -i,please check output!")
        device.raiseException("cel software test -i,please check output!")
    else:
        log.success("cel software test -i,pass")
@logThis
def check_cpu_information():
    cmd = 'lscpu'
    output = CommonLib.execute_command(cmd, timeout=120)
    if re.search('command not found', output):
        log.fail(" command not found , please check output!")
        device.raiseException("command not found, please check output!")
    elif 'error' in output or 'fail' in output:
        log.fail("run cmd lscpu, please check output!")
        device.raiseException("run cmd lscpu, please check output!")
    else:
        log.success("run cmd lscpu Pass")

@logThis
def check_cpu_option():
    path_cmd = 'cd /var/log/BMC_Diag/bin/'
    output = CommonLib.execute_command(path_cmd, timeout=120)
    if re.search("No such file", output):
        log.fail("Didn't found PATH, please check it!")
    else:
        test_cmd = './cel-CPU-test -h '
        output = CommonLib.execute_command(test_cmd, timeout=120)
        if 'error' in output or 'fail' in output:
            log.fail("cel CPU test -h, please check output!")
            device.raiseException("cel CPU test -h, please check output!")
        else:
            log.success("cel CPU test -h  pass")

@logThis
def show_cpu_info():
    test_cmd = './cel-CPU-test -i'
    output = CommonLib.execute_command(test_cmd, timeout=120)

    if 'error' in output or 'fail' in output:
        log.fail("run cmd cel-CPU-test -i, please check output!")
        device.raiseException("run cmd cel-CPU-test -i, please check output!")
    else:
        log.success("run cmd cel-CPU-test -i Pass")

@logThis
def cel_cpu_test():
    test_cmd = './cel-CPU-test -t '
    output = CommonLib.execute_command(test_cmd, timeout=120)
    re_math = r'.*cpu.*PASS'
    if re.search(re_math, output):
        log.success("cel-CPU-test -t,Pass")
    else:
        log.fail("cel-CPU-test -t,please check output!")
        device.raiseException("cel-CPU-test -t,please check output!")
@logThis
def test_10gkr_option_h():
    help_option = [
        '-h show this help',
        ' -i show 10G KR-devices status',
        ' -t test KR'
    ]
    cmd_h = './cel-10gKR-test -h'
    output = CommonLib.execute_command(cmd_h, timeout=120)
    CommonKeywords.should_match_ordered_regexp_list(output, help_option)

@logThis
def test_10gkr_option_i():
    cmd_i = './cel-10gKR-test -i'
    test_cmd_i = [
        r'eth1.*',
        r'eth2.*'
    ]
    output = CommonLib.execute_command(cmd_i, timeout=120)
    CommonKeywords.should_match_ordered_regexp_list(output, test_cmd_i)

@logThis
def auto_load_user():
    cmd = './auto_load_user.sh'
    device.sendMsg(cmd + '\n')
    device.read_until_regexp('BCM.*', timeout=60)
    test_cmd = 'sh'
    device.sendMsg(test_cmd + '\n')
    device.read_until_regexp('sonic', timeout=60)

@logThis
def test_10gkr_option_t():
    test_cmd = './cel-10gKR-test -t'
    output = CommonLib.execute_command(test_cmd, timeout=120)
    count = 0
    pattern = '\[[ \t]+PASS[ \t]+\]'
    for line in output.splitlines():
        match = re.search(pattern, line)
        log.cprint(match)
        if match:
            count += 1
    if count == 3:
        log.success("cel-10gKR-test -t,Pass")
    else:
        log.fail("cel-10gKR-test -t,please check output!")
        device.raiseException("cel-10gKR-test -t,please check output!")

@logThis
def kill_bcm_user():
    cmd_kill = 'killall -9 bcm.user'
    output = CommonLib.execute_command(cmd_kill)
    re_math = r'.*no.*found'
    if re.search(re_math, output):
        log.success('killall -9 bcm.user,Pass')
    else:
        log.fail("killall -9 bcm.user,please check output!")
        device.raiseException("killall -9 bcm.user,please check output!")

@logThis
def exit_this_program():
    exit_cmd = 'exit'
    device.sendMsg(exit_cmd + '\n')
    device.read_until_regexp('BCM.*', timeout=60)
    cmd = 'quit'
    device.sendMsg(cmd + '\n')

@logThis
def sata_test_option_h():
    cmd_h = ' ./cel-sata-test -h'
    output = CommonLib.execute_command(cmd_h)
    cmd_option_help = [
        '-h show help',
        '-t sata disk test'
    ]
    CommonKeywords.should_match_ordered_regexp_list(output, cmd_option_help)

@logThis
def sata_test_option_t():
    cmd_t = './cel-sata-test -t'
    output = CommonLib.execute_command(cmd_t, timeout=120)
    cmd_option_t = [
        r'SATA Disk size.*PASS',
        r'SATA Disk location test.*PASS',
        r'Device model test.*PASS'
    ]
    CommonKeywords.should_match_ordered_regexp_list(output, cmd_option_t)

@logThis
def curl_to_check_bmc_version(param):
    curl_cmd = 'curl -g http://240.1.1.1:8080/api/bmc/versions | python -m json.tool'
    new_ver = SwImage.getSwImage('BMC').newVersion
    old_ver = SwImage.getSwImage('BMC').oldVersion
    count = 0
    pattern = []
    if param == 'True':
        pattern = [
            r".*MasterVersion.*?" + old_ver,
            r".*SlaveVersion.*?" + new_ver
            ]
    elif param == 'False':
        pattern = [
            r".*MasterVersion.*?" + new_ver,
            r".*SlaveVersion.*?" + old_ver
        ]
    elif param == 'none':
        output = CommonLib.execute_command(curl_cmd, timeout=60)
        match = re.search('ok', output,re.I)
        if match:
            return
        else:
            raise RuntimeError('Curl failed, please check output.')
    else:
        raise RuntimeError('No assign true or false.')
    output = CommonLib.execute_command(curl_cmd, timeout=60)
    for line in output.splitlines():
        line = line.strip()
        for i in range(0, len(pattern)):
            match = re.search(pattern[i], line)
            if match:
                count += 1
    if count == len(pattern):
        log.success("It's correct of the bmc version.")
    else:
        raise RuntimeError('Bmc version is incorrect.')

@logThis
def flashcp_update_bmc_ver(mtd_id, ver):
    mdcmd=''
    fcpcmd=''
    if ver == 'old':
        mdcmd = 'md5sum ' + SwImage.getSwImage('BMC').oldImage
        if mtd_id == '5':
            fcpcmd = 'flashcp -v ' + SwImage.getSwImage('BMC').oldImage + ' /dev/mtd5'
        if mtd_id== '11':
            fcpcmd = 'flashcp -v ' + SwImage.getSwImage('BMC').oldImage + ' /dev/mtd11'
    if ver == 'new':
        mdcmd = 'md5sum ' + SwImage.getSwImage('BMC').newImage
        if mtd_id == '5':
            fcpcmd = 'flashcp -v ' + SwImage.getSwImage('BMC').newImage + ' /dev/mtd5'
        if mtd_id== '11':
            fcpcmd = 'flashcp -v ' + SwImage.getSwImage('BMC').newImage + ' /dev/mtd11'
    device.sendMsg(mdcmd + '\r\n')
    output = CommonLib.execute_command(fcpcmd, timeout=1800)
    match = re.search('(fail|error|no such file)', output, re.I)
    if match:
        raise RuntimeError('flashcp -v failed.')
    else:
        log.info('flashcp -v successed.')
    time.sleep(60)
    # test cpu status
    check_cmd = 'wedge_power.sh status'
    check_output = CommonLib.execute_command(check_cmd, timeout=60)
    check_match = re.search('Microserver power is on', check_output)
    if check_match:
        log.success('Cpu is running.')
    else:
        raise RuntimeError('Cpu is not running.')

@logThis
def verify_bmc_boot_info():
    cmd = 'boot_info.sh'
    out = CommonLib.execute_command(cmd,timeout=60)
    if 'Master' in out:
        return 'Master'
    elif 'Slave' in out:
        return 'Slave'
    else:
        raise RuntimeError('Can not get boot info.')

@logThis
def source_and_reboot_boot(mode):
    source_cmd = 'source /usr/local/bin/openbmc-utils.sh'
    device.sendMsg(source_cmd+'\r\n')
    judge = verify_bmc_boot_info()
    log.info("(((((((((judge=%s))))))))" % judge)
    if mode == 'Slave':
        if judge == 'Master':
            device.sendMsg('boot_from slave' + '\r\n')
            device.read_until_regexp('login:', timeout=1800)
            device.getPrompt(Const.BOOT_MODE_OPENBMC)
            time.sleep(40)
            info_cmd = 'boot_info.sh'
            outp = CommonLib.execute_command(info_cmd, timeout=30)
            match = re.search('slave', outp, re.I)
            if match:
                log.info("Switch successed, current mode is slave")
            else:
                raise RuntimeError('Failed, please check mode that used command boot_info.sh.')
        if judge == 'Slave':
            return
    if mode == 'Master':
        if judge == 'Master':
            return
        if judge == 'Slave':
            device.sendMsg('boot_from master' + '\r\n')
            device.read_until_regexp('login:', timeout=1800)
            device.getPrompt(Const.BOOT_MODE_OPENBMC)
            time.sleep(40)
            info_cmd = 'boot_info.sh'
            outp = CommonLib.execute_command(info_cmd, timeout=30)
            match = re.search('master', outp, re.I)
            if match:
                log.info("Switch successed, current mode is master")
            else:
                raise RuntimeError('Failed, please check mode that used command boot_info.sh.')

@logThis
def return_to_master_mode():
    path = '/var/log/BMC_Diag/bin'
    device.sendMsg('cd ' + path + '\r\n')
    device.sendMsg('source /usr/local/bin/openbmc-utils.sh' + '\r\n')
    device.sendMsg('boot_from master' + '\r\n')
    device.read_until_regexp('login:', timeout=600)
    device.getPrompt(Const.BOOT_MODE_OPENBMC)

@logThis
def cpuOptionTest():
    stress_path = '/usr/local/CPU_Diag/utility/stress/'
    device.sendCmd('cd ' + stress_path)
    cmd = './CPU_test.sh \n'
    device.sendMsg(cmd)
    device.read_until_regexp('root\s+\d+.*/usr/sbin/mcelog --daemon')
    time.sleep(30)
    pass_count = 0
    for i in range(3):
        device.sendMsg(Const.KEY_CTRL_C)
        try:
            device.read_until_regexp('root\@sonic', timeout=3)
            pass_count += 1
            break
        except Exception:
            continue
    if pass_count:
        log.success('cpu stress test passed')
    else:
        raise Exception('cpu stress test failed')

@logThis
def catCpuLog():
    cmd = 'cat ./CPU_stress_test.log | grep -E "errors|warnings"'
    out = CommonLib.execute_command(cmd)
    error_count = 0
    for line in out.splitlines():
        if re.search('.*Torture Test completed*\d+ errors, \d+ warnings', line):
            if re.search('.*0 errors, 0 warnings', line):
                continue
            else:
                error_count += 1
        else:
            continue
    if error_count:
        raise Exception('cpu stress test failed')
    else:
        log.success('cpu stress test passed')

@logThis
def qsfpI2cdumpStressTest():
    script_path = '/usr/local/CPU_Diag/utility/stress/qsfp_stress/'
    device.sendCmd('cd ' + script_path)
    cmd = './run_i2cdump_stress.sh 1 \n'
    fail_count = 0
    device.sendMsg(cmd)
    try:
        device.read_until_regexp('.*Error.*|error|fail', timeout=720)
        fail_count += 1
    except Exception:
        pass
    if fail_count:
        log.fail('qsfp i2cdump stress test failed')
        raise Exception('qsfp i2cdump stress test failed')
    else:
        log.success('qsfp i2cdump stress test passed')

def ssd_script_test():
    path = '/usr/local/CPU_Diag/utility/stress/'
    device.sendMsg('cd ' + path + '\r\n')
    script_cmd = './SSD_test.sh 2g'
    device.sendMsg(script_cmd+'\r\n')
    time.sleep(120)
    device.flush()
    count = 0
    for i in range(10):
        # must enter 4 CTRL + C quckily
        device.sendMsg(Const.KEY_CTRL_C)
        time.sleep(0.5)
        device.sendMsg(Const.KEY_CTRL_C)
        time.sleep(0.5)
        device.sendMsg(Const.KEY_CTRL_C)
        time.sleep(0.5)
        device.sendMsg(Const.KEY_CTRL_C)
        try:
            device.read_until_regexp('sonic', timeout=10)
            count += 1
            break
        except:
            continue
    if count == 1:
        log.success('SSD Stress test passed!')
    else:
        device.raiseException('SSD Stress test failed!')

@logThis
def cat_ssd_stress_log():
    cat_cmd = 'cat SSD_stress_test.log | grep -E "Fail|fail|Error|error" | wc -l'
    output = CommonLib.execute_command(cat_cmd, timeout=60)
    pattern = '^0$'
    count = 0
    for line in output.splitlines():
        line = line.strip()
        match = re.search(pattern,line)
        if match:
            count += 1
            break
        else:
            continue
    if count == 1:
        log.success('Cat ssd stress log passed')
    else:
        device.raiseException('Cat ssd stress log failed')

@logThis
def fpga_test_option_h():
    cmd = './cel-fpga-test -h'
    output = CommonLib.execute_command(cmd, timeout=120)
    fpga_option_h = [
        '-h help information',
        '-w <register> write to FPGA',
        '-r <register> read from FPGA',
        '-d data written to FPGA',
        '-v FPGA version',
        '-t test FPGA'
    ]
    CommonKeywords.should_match_ordered_regexp_list(output, fpga_option_h)

@logThis
def fpga_test_option_v():
    cmd = './cel-fpga-test -v'
    output = CommonLib.execute_command(cmd, timeout=120)
    # FPGA Version: 0x10000013
    math = r'FPGA Version\: (.*)'
    if re.search(math, output):
        log.success('fpga_test_option_v PASS.')
    else:
        raise RuntimeError('fpga_test_option_v failed!')

@logThis
def update_fpga_version(param):
    if param == 'old':
        image = SwImage.getSwImage('FPGA').oldImage
    else:
        image = SwImage.getSwImage('FPGA').newImage
    cmd_md5sum = 'md5sum' + ' ' + image
    CommonLib.execute_command(cmd_md5sum, timeout=120)
    cmd_fpga_prog = 'fpga_prog' + ' ' + image
    output = CommonLib.execute_command(cmd_fpga_prog, timeout=120)
    if re.search('Programing finish', output):
        log.success('update_fpga_version PASS')
    else:
        log.fail("update_fpga_version,please check output!")
        device.raiseException("update_fpga_version,please check output!")

@logThis
def check_fpga_old_version():
    version = ''
    cmd = './cel-fpga-test -v'
    output = CommonLib.execute_command(cmd, timeout=120)
    pattern = r'FPGA Version\: (.*)'
    for line in output.splitlines():
        match = re.search(pattern, line)
        if match:
            version = match.group(1).strip()
    if version == SwImage.getSwImage('FPGA').oldVersion:
        log.success('check_fpga_old_version success.')
    else:
        raise RuntimeError('check_fpga_old_version failed!')

@logThis
def cpld_test_option_h():
    cmd = './cel-cpld-test -h'
    output = CommonLib.execute_command(cmd, timeout=120)
    cpld_option_h = [
        r'-h .*',
        r'-w.*',
        r'-r.*',
        r'-a.*',
        r'-d.*',
        r'-v.*',
        r'-t.*'
    ]
    CommonKeywords.should_match_ordered_regexp_list(output, cpld_option_h)

@logThis
def cpld_test_option_v():
    cmd = ' ./cel-cpld-test -v'
    output = CommonLib.execute_command(cmd, timeout=120)
    cpld_version = [
        r'Base board CPLD version\:.*',
        r'COMe board CPLD version\: .*',
        r'Switch CPLD-1 version\:.*',
        r'Switch CPLD-2 version\:.*'
    ]
    CommonKeywords.should_match_ordered_regexp_list(output, cpld_version)

@logThis
def update_cpld_image_version(param):
    if param == 'old':
        cpld = SwImage.getSwImage('BASE_CPLD').oldImage
        come = SwImage.getSwImage('COME_CPLD').oldImage
        switch = SwImage.getSwImage('SWITCH_CPLD').oldImage
        fan = SwImage.getSwImage('FAN_CPLD').oldImage
    else:
        cpld = SwImage.getSwImage('BASE_CPLD').newImage
        come = SwImage.getSwImage('COME_CPLD').newImage
        switch = SwImage.getSwImage('SWITCH_CPLD').newImage
        fan = SwImage.getSwImage('FAN_CPLD').newImage

    cmd_list = [
        'ispvm -i 0' + ' ' + cpld,
        'ispvm -i 1' + ' ' + come,
        'ispvm -i 2' + ' ' + fan,
        'ispvm -i 3' + ' ' + switch
    ]
    for i in cmd_list:
        output = CommonLib.execute_command(i, timeout=120)
        math = r'.*PASS.*'
        if re.search(math, output):
            log.success(' update_cpld_image_version  pass')
        else:
            log.fail(' update_cpld_image_version  please check output!')
            device.raiseException('update_cpld_image_version please check output!')

@logThis
def check_cpld_image_version(param):
    if param == 'new':
        cpld_version_list = [
            SwImage.getSwImage('BASE_CPLD').newVersion,
            SwImage.getSwImage('COME_CPLD').newVersion,
            SwImage.getSwImage('SWITCH_CPLD').newVersion
        ]
    else:
        cpld_version_list = [
            SwImage.getSwImage('BASE_CPLD').oldVersion,
            SwImage.getSwImage('COME_CPLD').oldVersion,
            SwImage.getSwImage('SWITCH_CPLD').oldVersion]

    cmd = ' ./cel-cpld-test -v'
    output = CommonLib.execute_command(cmd, timeout=120)
    CommonKeywords.should_match_ordered_regexp_list(output, cpld_version_list)
    cmd = 'bmc-exec "version_dump"'
    output = CommonLib.execute_command(cmd, timeout=120)
    pattern = r'FAN CPLD Version\:(.*)'
    fan_cpld_version = ''
    for line in output.splitlines():
        match = re.search(pattern, line)
        if match:
            fan_cpld_version = match.group(1).strip()
    if fan_cpld_version == SwImage.getSwImage('FAN_CPLD').newVersion:
        log.success('check_cpld_image_version PASS')
    else:
        raise RuntimeError('check_cpld_image_version failed!')


@logThis
def check_current_fpga_version():
    version = ''
    cmd = './cel-fpga-test -v'
    output = CommonLib.execute_command(cmd, timeout=120)
    pattern = r'FPGA Version\: (.*)'
    for line in output.splitlines():
        match = re.search(pattern, line)
        if match:
            version = match.group(1).strip()
    if version == SwImage.getSwImage('FPGA').newVersion:
        log.success('check_current_fpga_version success.')
    else:
        raise RuntimeError('check_current_fpga_version failed!')


@logThis
def port_present_test():
    output = device.execCmd('./cel-port-test -P')
    CommonKeywords.should_match_ordered_regexp_list(output, shamu_var.port_present_pattern)


@logThis
def port_reset_test():
    output = device.execCmd('./cel-port-test -r enable;sleep 3')
    CommonKeywords.should_match_ordered_regexp_list(output, shamu_var.port_reset_enable_pattern)
    output = device.executeCmd('./cel-i2c-test -s')
    CommonKeywords.should_match_ordered_regexp_list(output, shamu_var.qsfp_not_scanned_pattern)
    output = device.execCmd(' ./cel-port-test -r disable; sleep 3')
    CommonKeywords.should_match_ordered_regexp_list(output, shamu_var.port_reset_disable_pattern)
    output = device.execCmd('./cel-i2c-test -s')
    CommonKeywords.should_match_ordered_regexp_list(output, shamu_var.qsfp_scanned_pattern)


@logThis
def port_modsel_test():
    output = device.execCmd('./cel-port-test -s enable;sleep 3')
    CommonKeywords.should_match_ordered_regexp_list(output, shamu_var.port_modsel_enable_pattern)
    output = device.execCmd('./cel-i2c-test -s')
    CommonKeywords.should_match_ordered_regexp_list(output, shamu_var.qsfp_scanned_pattern)
    output = device.execCmd('./cel-port-test -s disable;sleep 3')
    CommonKeywords.should_match_ordered_regexp_list(output, shamu_var.port_modsel_disable_pattern)
    output = device.executeCmd('./cel-i2c-test -s')
    # time.sleep(30)

    # @ISSUE, this step will fail, should be SW issue !!
    CommonKeywords.should_match_ordered_regexp_list(output, shamu_var.qsfp_not_scanned_pattern)


@logThis
def port_lpmod_test():
    output = device.execCmd('./cel-port-test -l enable;sleep 3')
    CommonKeywords.should_match_ordered_regexp_list(output, shamu_var.port_lpmod_enable_pattern)
    check_bit3(output, should_zero=False)

    output = device.execCmd('./cel-port-test -l disable;sleep 3')
    CommonKeywords.should_match_ordered_regexp_list(output, shamu_var.port_lpmod_disable_pattern)
    check_bit3(output, should_zero=True)\


@logThis
def port_Interrupt_test():
    for i in range(13, 52): # @ISSUE as doc, it should be 61~100
        device.execCmd('i2cset -y -f {} 0x50 29 0x02'.format(i))
    output = device.execCmd('./cel-port-test -i')
    CommonKeywords.should_match_ordered_regexp_list(output, shamu_var.port_interrupt_high_pattern)

    for i in range(13, 52):
        device.execCmd('i2cset -y -f {} 0x50 29 0x00'.format(i))
    time.sleep(10)
    output = device.execCmd('./cel-port-test -i')
    # @ISSUE, this step will fail, should be SW issue !!
    CommonKeywords.should_match_ordered_regexp_list(output, shamu_var.port_interrupt_low_pattern)


def check_bit3(output, should_zero):
    pattern = r'^0x[0-9a-fA-F]{2}$'
    for i in range(13, 52):  # @ISSUE as doc, it should be 61~100
        output = device.execCmd('i2cget -y -f {} 0x50 28'.format(i))
        for line in output.splitlines():
            match = re.search(pattern, line)
            if match:
                value = match.group(0)
                log.info('value: ' + value)
                if should_zero:
                    if int(value, 16) & 8 == 8:
                        raise RuntimeError('bit 3 should be 0!')
                else:
                    if int(value, 16) & 8 != 8:
                        raise RuntimeError('bit 3 should be 1!')


@logThis
def sfputil_test_eeprom():
    output = device.execCmd('sfputil test eeprom')
    CommonKeywords.should_match_ordered_regexp_list(output, shamu_var.sfp_eeprom_detected)


@logThis
def optical_modules_stress_test():
    files = ['Optical_modules_Stress_Test.sh', 'run.sh']
    serverObj = Server.getServer('PC', needLogin=False)
    serverIP = serverObj.managementIP
    hostDir = '/var/lib/tftpboot/shamu/image/TOOLS'
    CommonLib.copy_files_through_scp(Const.DUT, serverObj.username, serverObj.password, serverIP, files, hostDir, "/home")
    device.execCmd('cd /home')
    for file in files:
        device.execCmd('chmod +x ' + file)
    device.execCmd('./run.sh')

    for i in range(6):
        if CommonLib.check_file_exist(shamu_var.optical_modules_test_fail_file):
            device.executeCmd('cat ' + shamu_var.optical_modules_test_fail_file)
            device.execCmd('killall Optical_modules_Stress_Test.sh')
            raise RuntimeError('optical_modules_stress_test failed!')
        time.sleep(60)

    log.success('optical_modules_stress_test successfully.')
    device.execCmd('killall Optical_modules_Stress_Test.sh')
    for i in range(1, 11):
        device.execCmd('rm -f Optical_modules_Stress_Test_{}.log'.format(i) )

    for file in files:
        device.execCmd('rm -f ' + file)
    device.execCmd('rm -f ' + shamu_var.optical_modules_test_fail_file)


@logThis
def software_test_option_h():
    cmd = './cel-software-test -h'
    output = CommonLib.execute_command(cmd, timeout=120)
    software__option_h = [
        ' -h help information',
        '-i show software information'
    ]
    CommonKeywords.should_match_ordered_regexp_list(output, software__option_h)


@logThis
def software_test_option_i(upgrade=False):
    cmd = './cel-software-test -i'
    output = CommonLib.execute_command(cmd, timeout=120)
    pattern = r'obmc-cl-v(\d\.\d\.\d)'
    for line in output.splitlines():
        match = re.search(pattern, line)
        if match:
            version = match.group(1)
            expected_ver = SwImage.getSwImage(SwImage.BMC).newVersion if upgrade else SwImage.getSwImage(SwImage.BMC).oldVersion
            if version == expected_ver:
                log.success('check version success, current version: {}, expected version: {}'.format(version, expected_ver))
                return
            else:
                raise RuntimeError('check version failed! current version: {}, expected version: {}'.format(version, expected_ver))
    raise RuntimeError('can not parse current version!')


@logThis
def check_boot_status(param):
    source = 'source /usr/local/bin/openbmc-utils.sh'
    CommonLib.execute_command(source)
    cmd = 'boot_info.sh'
    output = CommonLib.execute_command(cmd, timeout=120)
    math = r'.*' + param + ' Flash'
    if re.search(math, output):
        log.success("check_boot" + param + "_status  Pass")
    else:
        log.fail("check_boot" + param + "_status, please check output!")
        device.raiseException("check_boot" + param + "_status, please check output!")


@logThis
def update_bmc_image_version(image_type, update_master=True):
    bmc_image = ''
    if image_type == 'old':
        bmc_image = SwImage.getSwImage('BMC').oldImage
    else:
        bmc_image = SwImage.getSwImage('BMC').newImage
    cmd = ' md5sum' + ' ' + bmc_image
    device.executeCmd(cmd)
    if update_master:
        command = "socflash_x64 -s if={} option=l lpcport=0x2e cs=0\n".format(bmc_image)
    else:
        command = "socflash_x64 -s if={} option=l lpcport=0x2e cs=1\n".format(bmc_image)
    device.sendMsg(command)
    # device.read_until_regexp('Press y to continue if you are agree', timeout=20)
    time.sleep(3)
    device.sendCmd('y')
    device.read_until_regexp('Update Flash Chip O.K.', timeout=900)
    log.success("update_" + image_type + "_bmc_image_version pass")


@logThis
def chmod_download_image(prarm):
    if prarm == 'old':
        bmc_image = SwImage.getSwImage('BMC').oldImage
    else:
        bmc_image = SwImage.getSwImage('BMC').newImage
    cmd = 'chmod 777' + ' ' + bmc_image
    device.sendMsg(cmd)

@logThis
def check_cpld_version():
    cmd = ' version_dump'
    output = CommonLib.execute_command(cmd, timeout=120)
    parten = [
        r'SYS CPLD Version\:.*',
        r'FAN CPLD Version\:.*'
    ]
    CommonKeywords.should_match_ordered_regexp_list(output, parten)

@logThis
def download_cpld_image_version(param):
    version_name = [
        'BASE_CPLD',
        'COME_CPLD',
        'FAN_CPLD',
        'SWITCH_CPLD'
    ]
    for name in version_name:
        CommonLib.download_image('DUT', name, upgrade=param)

@logThis
def update_base_cpld_version(image_version):
    BASE_CPLD = ''
    if image_version == 'old':
        BASE_CPLD = SwImage.getSwImage('BASE_CPLD').oldImage
    else:
        BASE_CPLD = SwImage.getSwImage('BASE_CPLD').newImage
    md5sum = 'md5sum ' + ' ' + BASE_CPLD
    CommonLib.execute_command(md5sum, timeout=60)
    source = 'source /usr/local/bin/openbmc-utils.sh'
    CommonLib.execute_command(source, timeout=60)
    command = 'program_cpld BASE_CPLD ' + ' ' + BASE_CPLD
    output = CommonLib.execute_command(command, timeout=600)
    math = r'.*PASS.*'
    if re.search(math, output):
        log.success("update_BASE_CPLD_" + image_version + "_version  pass")
    else:
        log.fail("update_BASE_CPLD_" + image_version + "_version fail  please check output!")
        device.raiseException("update_BASE_CPLD_" + image_version + "_version fail please check output!")

@logThis
def update_come_cpld_version(image_version):
    COME_CPLD = ''
    if image_version == 'old':
        COME_CPLD = SwImage.getSwImage('COME_CPLD').oldImage
    else:
        COME_CPLD = SwImage.getSwImage('COME_CPLD').newImage
    md5sum = 'md5sum ' + ' ' + COME_CPLD
    CommonLib.execute_command(md5sum, timeout=60)
    source = 'source /usr/local/bin/openbmc-utils.sh'
    CommonLib.execute_command(source, timeout=60)
    command = 'program_cpld CPU_CPLD ' + ' ' + COME_CPLD
    output = CommonLib.execute_command(command, timeout=600)
    math = r'.*PASS.*'
    if re.search(math, output):
        log.success("update_COME_CPLD_" + image_version + "_version  pass")
    else:
        log.fail("update_COME_CPLD_" + image_version + "_version fail  please check output!")
        device.raiseException("update_COME_CPLD_" + image_version + "_version fail please check output!")

@logThis
def update_switch_cpld_version(image_version):
    SWITCH_CPLD = ''
    if image_version == 'old':
        SWITCH_CPLD = SwImage.getSwImage('SWITCH_CPLD').oldImage
    else:
        SWITCH_CPLD = SwImage.getSwImage('SWITCH_CPLD').newImage
    md5sum = 'md5sum ' + ' ' + SWITCH_CPLD
    CommonLib.execute_command(md5sum, timeout=60)
    source = 'source /usr/local/bin/openbmc-utils.sh'
    CommonLib.execute_command(source, timeout=60)
    command = 'program_cpld SW_CPLD1' + ' ' + SWITCH_CPLD
    output = CommonLib.execute_command(command, timeout=600)
    math = r'.*PASS.*'
    if re.search(math, output):
        log.success("update_switch_CPLD_" + image_version + "_version  pass")
    else:
        log.fail("update_switch_CPLD_" + image_version + "_version fail  please check output!")
        device.raiseException("update_switch_CPLD_" + image_version + "_version fail please check output!")

@logThis
def update_fan_cpld_version(image_version):
    FAN_CPLD = ''
    if image_version == 'old':
        FAN_CPLD = SwImage.getSwImage('FAN_CPLD').oldImage
    else:
        FAN_CPLD = SwImage.getSwImage('FAN_CPLD').newImage

    md5sum = 'md5sum ' + ' ' + FAN_CPLD
    CommonLib.execute_command(md5sum, timeout=60)
    source = 'source /usr/local/bin/openbmc-utils.sh'
    CommonLib.execute_command(source, timeout=60)
    command = 'program_cpld FAN_CPLD' + ' ' + FAN_CPLD
    output = CommonLib.execute_command(command, timeout=600)
    math = r'.*PASS.*'
    if re.search(math, output):
        log.success("update_FAN_CPLD_" + image_version + "_version  pass")
    else:
        log.fail("update_FAN_CPLD_" + image_version + "_version fail  please check output!")
        device.raiseException("update_FAN_CPLD_" + image_version + "_version fail please check output!")

@logThis
def check_cpu_power_status():
    cmd = 'wedge_power.sh status'
    output = CommonLib.execute_command(cmd, timeout=120)
    partten = r'.* is on'
    if re.search(partten, output):
        log.success('check_cpu_power_status PASS')
    else:
        log.fail("check_cpu_power_status fail,please check output!")
        device.raiseException("check_cpu_power_status fail,please check output!")


@logThis
def update_basecpld_flash():
    """
    Update the basecpld to status 40% then shutdown the progress by CTRL+C.
    """
    log.info("###### online update base cpld ######")
    imageObj = SwImage.getSwImage("BASE_CPLD")
    image_path = imageObj.localImageDir + '/' + imageObj.newImage
    cmd = 'ispvm -i 0 ' + image_path

    ###### start flashing ######
    device.getPrompt('DIAGOS')
    device.sendCmd(cmd)
    device.read_until_regexp('40%', 120)

    ###### send CTRL+C ######
    device.sendCmd(Const.KEY_CTRL_C)
    device.getPrompt('DIAGOS')

    time.sleep(2)



