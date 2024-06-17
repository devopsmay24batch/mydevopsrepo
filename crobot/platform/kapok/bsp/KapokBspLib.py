import CRobot
import sys
import os
import re
import Logger as log
import CommonLib
from functools import partial
import KapokConst
import KapokCommonLib
import Const
import time
from KapokBspVariable import *
from Decorator import *

try:
    from Device import Device
    import DeviceMgr
except Exception as err:
    log.cprint(str(err))

device = DeviceMgr.getDevice()
devicename = os.environ.get("deviceName", "")

workDir = CRobot.getWorkDir()
sys.path.append(os.path.join(workDir, 'common', 'commonlib'))
run_command = partial(CommonLib.run_command, deviceObj=device, prompt=device.promptDiagOS)
def ModifyPortFile(pre, suf, partnum):
    log.debug("Entering BspTestCase procedure: ModifyPortFile")
    filename = pre + str(partnum) + suf
    return filename


def CheckOutput(passpattern, output):
    log.debug("Entering to check output is or not true")
    p_pass = []
    passcount = 0
    for line in output.splitlines():
        for pattern in passpattern:
            if re.search(pattern, line):
                passcount += 1
                p_pass.append(pattern)
    if passcount:
        if passcount == len(passpattern):
            return passcount
            log.debug('passpattern = %s' %passpattern)
        else:
            mismatch_pattern = set(passpattern) - set(p_pass)
            log.debug('mismatch is %s' % CommonLib.get_readable_strings(mismatch_pattern))
            return passcount
    else:
        log.fail("CheckOutput failed")
        device.raiseException("Failure while testing BSP tool")


def CatLoopFileInfo(path, pre='', suf='', part=32, passpattern=[], start_index=1):
    log.debug("Entering BspTestCase procedure: CatLoopFileInfo")
    if part > 1:
        part += 1
        for i in range(start_index, part):
            filename = ModifyPortFile(pre, suf, i)
            cmd = 'cat ' + path + filename
            #output = run_command(cmd,prompt='#')
            output = device.executeCmd(cmd, mode='Const.BOOT_MODE_DIAGOS')
            if CheckOutput(passpattern, output):
                log.success("cat %s info is passed" % filename)
            else:
                log.fail("cat %s info is failed" % filename)
                device.raiseException("Failure while checking %s info" % filename)
    else:
        time.sleep(3)
        cmd = 'cat ' + path + pre
        #output = run_command(cmd,prompt='#')
        output = device.executeCmd(cmd, mode='Const.BOOT_MODE_DIAGOS')
        if CheckOutput(passpattern, output):
            log.success("cat %s info is passed" % pre)
        else:
            log.fail("cat %s info is failed" % pre)
            device.raiseException("Failure while checking %s info" % pre)

@logThis
def checkQsfpType():
    cmd = 'qsfp'
    output = device.executeCmd(cmd)
    match_count = False
    for line in output.splitlines():
        if re.search('Vendor\: AWS', line):
            match_count = True
            break
    if match_count:
        return 'Eric ELB'
    else:
        return 'LEONI'

def PageSelectAndIntLConfig(pre='', suf='',page_pre='', page_suf='', part=132, start_index=101):
    log.debug("Entering BspTestCase procedure: PageSelectAndIntLConfig")
    qsfp_type = checkQsfpType()
    if qsfp_type == 'Eric ELB' and suf == ' 0x50 0xfe 0x20':
        suf = ' 0x50 0x41 0x02'
    elif qsfp_type == 'Eric ELB' and suf == ' 0x50 0xfe 0x30':
        suf = ' 0x50 0x41 0x12'

    if part > 1:
        part += 1
        for i in range(start_index, part):
            if qsfp_type == 'LEONI':
                cmd = page_pre + str(i) + page_suf
                device.executeCmd(cmd)
            cmd = pre + str(i) + suf
            device.executeCmd(cmd)
    else:
        time.sleep(3)
        cmd = page_pre + str(i) + page_suf
        device.executeCmd(cmd)
        cmd = pre + str(i) + suf
        device.executeCmd(cmd)

def EchoValueToFile(path, file, value):
    log.debug("Entering BspTestCase procedure: EchoValueToFile")
    cmd = 'echo ' + value + ' ' + '>' + ' ' + path + file
    #output = run_command(cmd,prompt='#')
    output = device.executeCmd(cmd, mode='Const.BOOT_MODE_DIAGOS')
    VerifyExeCmdNoOutput(output=output)
    return output


def ModifyResetFileValue(path, pre='', suf='', value='', part=32, start_index=1):
    log.debug("Entering BspTestCase procedure: ModifyResetFileValue")
    for i in range(start_index, part + 1):
        filename = ModifyPortFile(pre, suf, i)
        EchoValueToFile(path, filename, value)


def LoopToEchoValueToFile(path, file, value, loop_times=3):
    log.debug("Entering BspTestCase procedure: LoopToEchoValueToFile")
    for i in range(0, loop_times):
        EchoValueToFile(path, file, value)


def ReadUntilToDiagOS():
    log.debug("Entering BspTestCase procedure: ReadUntilToDiagOS")
    device.read_until_regexp(KapokConst.STOP_AUTOBOOT_PROMPT, 100)
    device.sendMsg(KapokConst.STOP_AUTOBOOT_KEY)
    device.getPrompt(Const.BOOT_MODE_DIAGOS)


def VerifyExeCmdNoOutput(cmd='', output=''):
    log.debug("Entering BspTestCase procedure: VerifyExeCmdNoOutput")
    if output == '':
        output = run_command(cmd,prompt='#')
    for line in output.splitlines():
        if re.search('No such file or directory', line):
            log.fail("verify %s info is failed" % output)
            device.raiseException("Failure while checking %s info" % output)
        elif re.search('command not found', line):
            log.fail("verify %s info is failed" % output)
            device.raiseException("Failure while checking %s info" % output)
        elif re.search('Permission denied', line):
            log.fail("verify %s info is failed" % output)
            device.raiseException("Failure while checking %s info" % output)
        else:
            pass


def VerifyCPLDVersions(filelist=[]):
    log.debug("Entering BspTestCase procedure: VerifyCPLDVersions")
    cpld_version_list = list()
    cpld_dict = CommonLib.get_swinfo_dict('CPLD')
    syscpld_version = cpld_dict.get('newVersion').get('SYSCPLD')
    log.debug("syscpld_version: %s" % syscpld_version)
    cpld_version_list.append(syscpld_version)
    cpld1_version = cpld_dict.get('newVersion').get('SWLEDCPLD1')
    log.debug("ledcpld1_version: %s" % cpld1_version)
    cpld_version_list.append(cpld1_version)
    cpld2_version = cpld_dict.get('newVersion').get('SWLEDCPLD2')
    log.debug("ledcpld2_version: %s" % cpld2_version)
    cpld_version_list.append(cpld2_version)
    match_count = 0
    log.debug("filelist type: %s, item[0]: %s"%(type(filelist), filelist[0]))
    for filename in filelist:
        cmd = 'cat ' + filename
        output = device.executeCmd(cmd)
        for line in output.splitlines():
            for version in cpld_version_list:
                if re.search(version, line):
                    log.debug("The versions of %s matches that of %s" %(filename, version))
                    match_count += 1
                    cpld_version_list.remove(version)
                    break
                else:
                    continue
    if match_count == len(filelist):
        log.success("verify CPLD versions is passed")
    else:
        log.fail("verify CPLD versions is failed")
        device.raiseException("Failure while checking CPLD versions")


def VerifyFanLabelInfo(path, file_pre, file_suf, pattern_pre, pattern_suf, start_index=1, part=12, step=2):
    log.debug("Entering BspTestCase procedure: VerifyFanLabelInfo")
    loop = 0
    passpattern = ['']
    for i in range(start_index, part+1, step):
        loop += 1
        filename = ModifyPortFile(file_pre, file_suf, i)
        pattern = ModifyPortFile(pattern_pre, pattern_suf, str(loop))
        passpattern[0] = pattern
        cmd = 'cat ' + path + filename
        output = run_command(cmd,prompt='#',timeout=60)
        if CheckOutput(passpattern, output):
            log.success("cat %s info is passed" % filename)
        else:
            log.fail("cat %s info is failed" % filename)
            device.raiseException("Failure while checking %s info" % filename)


def VerifyFanSpeedChange(path, tool_name, option1, option2, passpattern, default_passpattern):
    log.debug("Entering BspTestCase procedure: VerifyFanSpeedChange")
    cmd = 'cd ' + path
    run_command(cmd,prompt='#')
    cmd = './' + tool_name + ' ' + option1
    pass_count = 0
    VerifyExeCmdNoOutput(cmd)
    time.sleep(2)
    cmd = './' + tool_name + ' ' + option2
    output = run_command(cmd,prompt='#')
    for line in output.splitlines():
        for pattern in passpattern:
            if re.search(pattern, line):
                pass_count += 1
        for patterns in default_passpattern:
            if re.search(patterns, line):
                log.fail("use %s to set fan speed failed" % tool_name)
                device.raiseException("Failure while checking fan speed info")
    if pass_count >= 12:
        time.sleep(12)
        cmd = './' + tool_name + ' ' + option2
        output = run_command(cmd,prompt='#')
        match_count = 0
        for line in output.splitlines():
            for pattern in default_passpattern:
                if re.search(pattern, line):
                    match_count += 1
            for patterns in passpattern:
                if re.search(patterns, line):
                    log.fail("use %s to set fan speed failed" % tool_name)
                    device.raiseException("Failure while checking fan speed info")
    else:
        log.fail("use %s to set fan speed failed" % tool_name)
        device.raiseException("Failure while checking fan speed info")
    if match_count >= 12:
        log.success("test fan speed is passed")
    else:
        log.fail("use %s to set fan speed failed" % tool_name)
        device.raiseException("Failure while checking fan speed info")


def dhclientGetIP():
    log.debug("Entering BspTestCase procedure: dhclientGetIP")
    if 'tianhe' in devicename.lower():
        cmd1 = 'udhcpc'
    else:
        cmd1 = 'dhclient'
    cmd2 = 'echo $?'
    device.executeCmd(cmd1)
    output = device.executeCmd(cmd2)
    if re.search('0', output):
        log.success("set ip address is passed")
        device.executeCmd('ifconfig')
    else:
        log.fail("use dhclient to set ip address failed")
        device.raiseException("Failure while get ip address")

def sleep_time(timevalue):
    cmd = "time sleep " +str(timevalue)
    device.sendMsg(cmd)
    time.sleep(int(timevalue))

def fhv2_execute_reset_command(console=None, path=None, command=None,timeout=60):
    log.debug("Entering BspTestCase procedure: fhv2_execute_reset_command")
    if console != None:
        device.getPrompt(console, timeout)
    device.flush()
    if path != None:
        cdcmd = 'cd ' + path
        device.sendCmd(cdcmd)
    if device.currentBootMode == Const.BOOT_MODE_UBOOT:
        prompt = "{}[\s\S]+{}".format(command.lstrip()[:5], device.promptUboot)
        ret = device.sendCmdRegexp(command, prompt, timeout)
        # Ask U-Boot for does not repeat the last command for ENTER Key
        device.sendline(" ")

        return ret

    cmd = 'time ' + command
    return device.sendCmd(cmd, timeout=timeout)

def checkBootingOutput(mode=None):
    log.debug("Entering OnieLib class procedure: checkBootingOutput")

    detect_prompt = {"installer": 'discover: installer mode detected',
                     "update"  : 'discover: ONIE update mode detected',
                     "rescue"   : 'discover: Rescue mode detected',
                     "Uninstall": 'discover: Uninstall mode detected'
            }
    ACTIVATE_CONSOLE_PROMPT = 'Please press Enter to activate this console'
    if mode == "Uninstall":
        output = device.read_until_regexp(KapokConst.STOP_AUTOBOOT_PROMPT, timeout=KapokConst.BOOT_TIME)
        device.sendMsg("{}\n".format(KapokConst.STOP_AUTOBOOT_KEY))
        output += device.read_until_regexp(device.promptUboot, timeout=10)
    else:
        output = device.read_until_regexp(ACTIVATE_CONSOLE_PROMPT, timeout=KapokConst.BOOT_TIME)
        device.sendMsg("\n")
        output += device.read_until_regexp(device.promptOnie, timeout=10)

    updater_info = CommonLib.get_swinfo_dict("ONIE_updater")
    onie_version = updater_info.get("newVersion", "NotFound")
    check_pattern = {"Version : %s"%onie_version: "Version.*?%s"%onie_version }
    expect_prompt = detect_prompt.get(mode, "NotFound")
    check_pattern.update({ expect_prompt: expect_prompt })

    CommonLib.execute_check_dict("DUT", "", patterns_dict=check_pattern,
                                 timeout=60, check_output=output)


def switchAndCheckOutput(mode):
    log.debug("Entering OnieLib class procedure: switchAndCheckOutput")
    
    switch_onie_mode_cmd = { "installer": "powerCycle",
                 "update"  : "run onie_update",
                 "rescue"   : "run onie_rescue",
                 "Uninstall": "run onie_uninstall"
        }
    switch_cmd = switch_onie_mode_cmd.get(mode, "NotFound")
    if switch_cmd == "powerCycle":
        device.powerCycleDevice()
    else:
        device.sendMsg(switch_cmd)
        device.sendMsg("\n")

    checkBootingOutput(mode)

def set_And_Save_Mac_Address():

    set_env = 'setenv ipaddr 10.10.10.7'
    device.sendMsg(set_env+'\r\n')
    save_env = 'saveenv'
    savenv_pattern = {
        "save env": "Saving Environment to SPI Flash...",
        "erasing and writing flash": "Erasing SPI flash...Writing to SPI flash...done"
    }
    output = CommonLib.execute_command(save_env, timeout=30)
    CommonLib.execute_check_dict("DUT", "", patterns_dict=savenv_pattern, timeout=10, check_output=output)

def verifyCanFoundParameter():

    print_cmd = 'printenv'
    output = CommonLib.execute_command(print_cmd, timeout=30)
    test_str = 'ipaddr=10.10.10.7'
    if test_str in output:
        log.success('ipaddr found in output!')
    else:
        log.fail('can not found ipaddr!')

def printenvOnieUbootaddress():
    cmd = 'fw_printenv'
    output = CommonLib.execute_command(cmd, timeout=10)
    cmd_pattern = {
            "arch":"arch=arm",
            "autoload":"autoload=n",
            "ipaddr":"10.10.10.7"
    }
    CommonLib.execute_check_dict("DUT", "", patterns_dict=cmd_pattern, timeout=10, check_output=output)

@logThis
def check_onie_version():
    cmd='get_versions'
    Image_info_dict = CommonLib.get_swinfo_dict("ONIE_Installer")
    onie_version = Image_info_dict.get("newVersion", "NotFound")
    onie_version_pattern = {"ONIE  %s" % (onie_version): "^ONIE\s+%s" % (onie_version)}

    CommonLib.execute_check_dict('DUT',cmd , mode=Const.BOOT_MODE_ONIE, patterns_dict=onie_version_pattern, timeout=60)

@logThis
def upgrade_onie(image):
    mtd0_path = '/dev/mtd0'
    flash_update_cmd = 'flashcp ' + image + ' ' + mtd0_path
    output = CommonLib.execute_command(flash_update_cmd, timeout=600)
    CommonLib.execute_check_dict("DUT", "", patterns_dict={'error': 'error'}, timeout=1800, check_output=output, is_negative_test=True)

@logThis
def set_ipaddr_and_server(ipaddr, serverip):

    ip_cmd = 'setenv ipaddr ' + ipaddr
    server_cmd = 'setenv serverip ' + serverip
    device.sendMsg(ip_cmd + '\r\n')
    device.sendMsg(server_cmd + '\r\n')
    #devicename = os.environ.get("deviceName", "")
    #if "fenghuangv2" in devicename.lower():
        #device.sendMsg('setenv tftpdir celestica_cs8260-' + '\r\n')
    #elif "tianhe" in devicename.lower():
        #device.sendMsg('setenv tftpdir celestica_cs8264-' + '\r\n')



@logThis
def run_bootupd():

    bootupd_cmd = 'run bootupd'
    output = CommonLib.execute_command(bootupd_cmd, timeout=600)
    devicename = os.environ.get("deviceName", "")
    if 'tianhe' in devicename.lower():
        pattern = {
                'Loading' : "done",
                'SF' : ".*?Erased:.*?OK",
                'SF' : ".*?Written:.*?OK"
                }
    else:
        pattern = {
                'start_boot' : "al_eth1 Waiting for PHY auto negotiation to complete.*done",
                'bootupd' : "bootupd done"
                }
    CommonLib.execute_check_dict("DUT", "", patterns_dict=pattern, timeout=600, check_output=output)
    device.read_until_regexp(device.promptUboot)
    if 'tianhe' in devicename.lower():
        device.powerCycleDevice()
    else:
        device.sendMsg('reset' + '\r\n')
    device.read_until_regexp(KapokConst.STOP_AUTOBOOT_PROMPT, timeout=300)
    device.sendMsg(KapokConst.STOP_AUTOBOOT_KEY)

@logThis
def Check__Uboot_ver():
    cmd = 'print ver'
    Image_info_dict = CommonLib.get_swinfo_dict("UBOOT")
    Uboot_version = Image_info_dict.get("newVersion", "NotFound")
    output = CommonLib.execute_command(cmd, timeout=60)
    Uboot_pattern = Uboot_version
    if Uboot_pattern in output:
        log.success("Uboot version Matched")
    else:
        raise Exception("Uboot version Mismatched,expected {}".format(Uboot_pattern))




@logThis
def ifconfig_and_ping_address(ipaddr):

    device.sendMsg('ifconfig' + '\r\n')
    device.sendMsg('ping ' + ipaddr +' -w 5' '\r\n')
    output = device.read_until_regexp(device.promptOnie, timeout=30)
    fail_dict = {
        'fail' : 'fail',
        'error' : 'error',
        '100lost' : '100% packet loss'
    }
    CommonLib.execute_check_dict("DUT", "", patterns_dict=fail_dict, timeout=60, check_output=output, is_negative_test=True)

@logThis
def tftpUbootImage(server_ip, image):

    tftp_cmd = 'tftp -g ' + server_ip + ' -r ' + image
    device.sendMsg(tftp_cmd+'\r\n')


@logThis
def cat_dev_mtd_and_erase_mtd0():

    cat_cmd = 'cat /proc/mtd'
    device.sendMsg(cat_cmd+ " \n")
    device.read_until_regexp('uboot',timeout=60)

    erase_mtd0 = 'flash_erase /dev/mtd0 0 0'
    output = CommonLib.execute_command(erase_mtd0, timeout=1800)
    CommonLib.execute_check_dict("DUT", "", patterns_dict={'finish_prompt': '100\%[ \t]+complete'}, timeout=1800, check_output=output)

@logThis
def get_versions_to_check_onie(get_versions_cmd):
    cmd = get_versions_cmd
    Image_info_dict = CommonLib.get_swinfo_dict("ONIE_Installer")
    onie_version = Image_info_dict.get("newVersion", "NotFound")
    onie_version_pattern = {"ONIE  %s" % (onie_version): "^ONIE\s+%s" % (onie_version)}

    CommonLib.execute_check_dict('DUT', cmd, mode=Const.BOOT_MODE_ONIE, patterns_dict=onie_version_pattern, timeout=60)

@logThis
def addTestParameters(param=''):

    fw_cmd = 'fw_setenv'
    test_cmd = 'testenv' + param
    parameters_cmd = 'mytestenv' + param

    command = fw_cmd + ' ' + test_cmd + ' ' + parameters_cmd
    fail_dict = {
        "fail":"fail",
        "error":"error"
    }
    device.sendMsg(command+'\n')
    device.read_until_regexp('Proceed with update \[N\/y\]\? ', timeout=10)
    device.sendMsg("y\n")
    output = device.read_until_regexp("ONIE",timeout=10)
    CommonLib.execute_check_dict("DUT", "", patterns_dict=fail_dict, timeout=10, check_output=output, is_negative_test=True)

@logThis
def printenvOnUboot():
    set_default_env_cmd = 'env default -a\n'
    device.sendMsg(set_default_env_cmd)
    save_cmd = 'saveenv\n'
    device.sendMsg(save_cmd)
    cmd = "printenv"
    output = CommonLib.execute_command(cmd, timeout=10)
    pattern = {
        "printenv failed" : "Environment size:.*?"
    }
    CommonLib.execute_check_dict("DUT", "", patterns_dict=pattern, timeout=20, check_output=output)

@logThis
def check_reboot_boot_log_msg(test_pattern):

    KapokCommonLib.bootIntoDiagOSMode()
    device.sendMsg('reboot' + '\r\n')
    finish_prompt = 'Type 123<ENTER> to STOP'
    timeout = 300
    output = device.read_until_regexp(finish_prompt, timeout=timeout)
    log.info("output=%s" % output)
    CommonLib.execute_check_dict('DUT', "", patterns_dict=test_pattern, timeout=300, check_output=output)
    device.read_until_regexp("ONIE: Starting ONIE Service Discovery", timeout=300)
    device.sendMsg("\n \n \n onie-discovery-stop \n \n")
    device.read_until_regexp(device.promptOnie, timeout=20)

@logThis
def riser_board_eerpom_test():

    riser_test_cmd = {
        'read1':'hexdump -C /sys/bus/i2c/devices/33-0050/eeprom',
        'echo_read':'echo test > /sys/bus/i2c/devices/33-0050/eeprom',
        'read2':'hexdump -C /sys/bus/i2c/devices/33-0050/eeprom',
        'echo_read2':"echo -n -e '\\x01\\x00\\x00\\x01\\x00\\x00' > /sys/bus/i2c/devices/33-0050/eeprom",
        'read3':'hexdump -C /sys/bus/i2c/devices/33-0050/eeprom'
    }
    for key in riser_test_cmd:
        output = CommonLib.execute_command(riser_test_cmd[key], timeout=60)
        if '(?i)(fail|error|no such file)' not in output:
            if key == 'read2':
                read2_match = re.search('test', output)
                if read2_match:
                    log.info('done')
                else:
                    log.fail('echo test > /sys/bus/i2c/devices/33-0050/eeprom failed!')
            if key == 'read3':
                read3_match = re.search('01 00 00 01 00 00', output)
                if read3_match:
                    log.info('done')
                else:
                    log.fail("echo -n -e '\x01\x00\x00\x01\x00\x00' > /sys/bus/i2c/devices/33-0050/eeprom failed!")
            log.info('Test passed!')
        else:
            log.fail('Test failed!')

@logThis
def profileSpeedTest(path):
    passpattern1 = ['100000']
    passpattern2 = ['400000']
    passpattern3 = ['1000000']
    pass_pattern = [passpattern1, passpattern2, passpattern3]
    echo_value = ['100000', '400000', '1000000']
    port = 'port'
    pre = '_i2c_profile'
    suf = '_speed'
    filename_suf1 = ModifyPortFile(pre, suf, partnum=1)
    filename_suf2 = ModifyPortFile(pre, suf, partnum=2)
    for i in range(32):
        i += 1
        filename1 = ModifyPortFile(port, filename_suf1, partnum=i)
        filename2 = ModifyPortFile(port, filename_suf2, partnum=i)
        CatLoopFileInfo(path=path, pre=filename1, part=0, passpattern=pass_pattern[1])
        CatLoopFileInfo(path=path, pre=filename2, part=0, passpattern=pass_pattern[2])
        for j in range(3):
            EchoValueToFile(path, filename1, echo_value[j])
            EchoValueToFile(path, filename2, echo_value[j])
            CatLoopFileInfo(path=path, pre=filename1, part=0, passpattern=pass_pattern[j])
            CatLoopFileInfo(path=path, pre=filename2, part=0, passpattern=pass_pattern[j])
            j += 1

    for j in range(32):
        j += 1
        filename1 = 'port' + str(j) + '_i2c_profile1_speed'
        filename2 = 'port' + str(j) + '_i2c_profile2_speed'
        EchoValueToFile(path, filename1, echo_value[1])
        EchoValueToFile(path, filename2, echo_value[2])
        CatLoopFileInfo(path=path, pre=filename1, part=0, passpattern=pass_pattern[1])
        CatLoopFileInfo(path=path, pre=filename2, part=0, passpattern=pass_pattern[2])

def read_FAN_input(test_cmd):

    test_list = []
    cmd = ''
    device.sendMsg('cd /root/diag' + '\r\n')
    for fan_id in range(12):
        fan_id += 1
        if 'cat' in test_cmd:
            cmd = test_cmd + 'fan' + str(fan_id) +'_input'
        else:
            cmd = test_cmd + ' ' + str(fan_id)
        output = run_command(cmd,prompt='#',timeout=60)
        for line in output.splitlines():
            line = line.strip()
            match = re.findall('\d{5}', line)
            if match:
                match2 = "".join(match)
                test_list.append(match2)

    if len(test_list) == 12:
        log.info('system FAN input speed test pass!')
        return test_list
    else:
        log.fail('system FAN input speed test occurs error! %s' % test_list)

@logThis
def compare_system_and_diag_FAN_input():

    system_FAN_input_cmd = 'cat /sys/bus/i2c/devices/23-0066/'
    diag_FAN_input_cmd = './cel-fan-test -r -t speed -d'
    system_speed = read_FAN_input(system_FAN_input_cmd)
    diag_speed = read_FAN_input(diag_FAN_input_cmd)
    log.info("/////system_speed is %s" % system_speed)
    log.info("/////diag_speed is %s" % diag_speed)
    n = 0
    for sys_i in system_speed:
        sys1 = float(sys_i)* 1.02
        sys2 = float(sys_i)* 0.98
        diag = float(diag_speed[n])
        if diag >= sys2 and diag <= sys1:
            log.info('conform +-2%')
        else:
            log.fail('not conform +-2%')
        n += 1

@logThis
def fhv2DiagdownloadImagesAndRecoveryDiagOS():
    INSTALLER_MODE_DETECT_PROMPT = 'discover: installer mode detected'
    RECOVERY_DIAG_PATTERN = {"installer mode detected": "installer mode detected"}
    diagos_file_name = CommonLib.get_swinfo_dict("DIAGOS").get("newImage")
    hostImageDir = CommonLib.get_swinfo_dict("DIAGOS").get("hostImageDir")
    diagos_file = ["{}/{}".format(hostImageDir,diagos_file_name)]
    CommonLib.tftp_get_files(Const.DUT, file_list=diagos_file, dst_path="/root", timeout=400)
    install_diagos_cmd = "onie-nos-install {}".format(diagos_file_name)
    device.sendCmdRegexp(install_diagos_cmd, KapokConst.STOP_AUTOBOOT_PROMPT, timeout=900)
    device.sendMsg(KapokConst.STOP_AUTOBOOT_KEY)
    device.sendCmdRegexp('run diag_bootcmd', 'Please press Enter to activate this console', timeout=900)
    device.sendMsg('\n')

def configStaticIP(interface="eth0", mode=Const.ONIE_RESCUE_MODE):
    log.debug("Entering OnieLib class procedure: configStaticIP")

    deviceName = os.environ.get("deviceName", "")
    log.debug("deviceName: {}".format(deviceName))
    device_ip = CommonLib.Get_Not_Occupied_IP()
    if not device_ip:
        raise Exception("No available device_ip is found")
    else:
        log.info("Settting static IP: {}".format(device_ip))
    deviceInfo = CommonLib.get_device_info(deviceName)
    net_mask = deviceInfo.get("managementMask","")
    status = "up"
    CommonLib.config_management_interface("DUT", interface, device_ip, net_mask, status, mode)

def onieSelfUpdate(update="new"):
    log.debug("Entering OnieLib class procedure: onieSelfUpdate")

    updater_info_dict = CommonLib.get_swinfo_dict("ONIE_updater")
    if update == "new":
        filename = updater_info_dict.get("newImage", "NotFound")
        file_path = updater_info_dict.get("hostImageDir", "NotFound")
    else:
        filename = updater_info_dict.get("oldImage", "NotFound")
        file_path = updater_info_dict.get("oldhostImageDir", "NotFound")
    server_ip = CommonLib.get_device_info("PC").get("managementIP","")
    log.debug("Prompt: {}".format(device.promptOnie))
    if not server_ip:
        raise Exception("Didn't find server IP.")
    updater_cmd = "onie-self-update tftp://{}/{}".format(server_ip, os.path.join(file_path, filename))
    expect_message = KapokConst.ONIE_DISCOVERY_PROMPT
    timeout_message = "tftp: timeout|tftp: read error"
    finish_prompt = "{}|{}".format(expect_message, timeout_message)
    retry = 3
    for i in range(retry):
        output = device.sendCmdRegexp(updater_cmd, finish_prompt, timeout=2000)
        if re.search(expect_message, output):
            break
        elif re.search(timeout_message, output):
            log.info("{}, retry left {} times.".format(timeout_message, retry-i-1))
            if i == retry - 1:
                raise Exception("tftp failed, after tried {} times".format(retry))
            continue
    device.sendMsg("\n")
    onie_discovery_stop_cmd = KapokConst.STOP_ONIE_DISCOVERY_KEY

    device.sendCmdRegexp(onie_discovery_stop_cmd, device.promptOnie, timeout=10)

def verifyOnieAndCPLDVersion(version="new"):
    log.debug("Entering OnieLib class procedure: verifyOnieAndCPLDVersion")
    escapeString = CommonLib.escapeString

    cmd = "get_versions"
    Image_info_dict = CommonLib.get_swinfo_dict("ONIE_Installer")
    onie_version = Image_info_dict.get("%sVersion"%version, "NotFound")
    onie_version_pattern = { "ONIE  %s"%(onie_version): "^ONIE\s+%s"%(escapeString(onie_version))}
    CPLD_version_dict = CommonLib.get_swinfo_dict("CPLD").get("%sVersion"%version, {})
    Uboot_version = CommonLib.get_swinfo_dict("UBOOT").get("%sVersion"%version, "")
    Uboot_pattern = escapeString(Uboot_version)
    onie_version_pattern.update({ Uboot_version: Uboot_pattern })

    for key_type, value in CPLD_version_dict.items():
        pattern_name = "{}  {}".format(key_type, value)
        pattern = "{}\s+{}".format(key_type, escapeString(value))
        onie_version_pattern.update({pattern_name: pattern})


    CommonLib.execute_check_dict('DUT', cmd, mode=Const.BOOT_MODE_ONIE, patterns_dict=onie_version_pattern,
                                 timeout=6)

@logThis
def checkversionbeforethetest():
    sys_cpld_version = CommonLib.get_swinfo_dict('CPLD').get('newVersion').get('SYSCPLD')
    cpld_dict = CommonLib.get_swinfo_dict('CPLD')
    led_cpld1_version = cpld_dict.get('newVersion').get('SWLEDCPLD1')
    led_cpld2_version = cpld_dict.get('newVersion').get('SWLEDCPLD2')
    fan_cpld = cpld_dict.get('newVersion').get('FANCPLD')
    uboot_version = CommonLib.get_swinfo_dict("UBOOT").get("newVersion", "NotFound")
    onie_version = CommonLib.get_swinfo_dict("ONIE_Installer").get("newVersion", "NotFound")
    devicename = os.environ.get("deviceName", "")
    if "fenghuangv2" in devicename.lower():
        dev_type = DeviceMgr.getDevice(devicename).get('cardType')
        if dev_type == '1PPS':
            ASC_type = dev_type + '_ASC'
            ASC = CommonLib.get_swinfo_dict(ASC_type)
            ic2fpga = CommonLib.get_swinfo_dict(ASC_type).get("1pps", "NotFound")
        else:
            ASC_type = 'I2C_ASC'
            ic2fpga = CommonLib.get_swinfo_dict(ASC_type).get("fpga", "NotFound")
        uc_app = CommonLib.get_swinfo_dict("UC").get("newVersion", "NotFound").get("uC_app")
        uC_bl = CommonLib.get_swinfo_dict("UC").get("newVersion", "NotFound").get("uC_bl")
        asc10_0 = CommonLib.get_swinfo_dict(ASC_type).get("newVersion", "NotFound").get("ASC10-0")
        asc10_1 = CommonLib.get_swinfo_dict(ASC_type).get("newVersion", "NotFound").get("ASC10-1")
        asc10_2 = CommonLib.get_swinfo_dict(ASC_type).get("newVersion", "NotFound").get("ASC10-2")
        hw_dict = {'uc_app': uc_app, 'uc_bl': uC_bl, 'ASC10-0': asc10_0, 'ASC10-1': asc10_1, 'ASC10-2': asc10_2,
                   'I2CFPGA': ic2fpga}
        cpld_version_dict = {'SYSCPLD': sys_cpld_version, 'SWLEDCPLD1': led_cpld1_version,
                             'SWLEDCPLD2': led_cpld2_version,'U-BOOT': uboot_version,'ONIE': onie_version,
                             'FANCPLD': fan_cpld}
        check_version_cmd = 'get_versions'
        output = device.executeCmd(check_version_cmd)
    elif "tianhe" in devicename.lower():
        diagObj = CommonLib.get_swinfo_dict('DIAGOS')
        diag_version = diagObj.get('newVersion', 'NotFound')
        come_cpld_version = cpld_dict.get('newVersion').get('COMECPLD')
        dev_type = DeviceMgr.getDevice(devicename).get('cardType')
        if dev_type == '1PPS':
            ASC_type = dev_type + '_ASC'
            ppsObj = CommonLib.get_swinfo_dict(ASC_type)
            ic2fpga = ppsObj.get("1pps", "NotFound")
        else:
            ASC_type = 'I2C_ASC'
            ic2fpga = CommonLib.get_swinfo_dict(ASC_type).get("fpga", "NotFound")
        asc10_0 = ppsObj.get("newVersion", "NotFound").get("ASC10-0")
        asc10_1 = ppsObj.get("newVersion", "NotFound").get("ASC10-1")
        asc10_2 = ppsObj.get("newVersion", "NotFound").get("ASC10-2")
        asc10_3 = ppsObj.get("newVersion", "NotFound").get("ASC10-3")
        asc10_4 = ppsObj.get("newVersion", "NotFound").get("ASC10-4")
        hw_dict = {'ASC10-0': asc10_0, 'ASC10-1': asc10_1, 'ASC10-2': asc10_2, 'ASC10-3': asc10_3, 'ASC10-4': asc10_4, '1PPSFPGA': ic2fpga}
        cpld_version_dict = {'SYSCPLD': sys_cpld_version, 'COMECPLD': come_cpld_version, 'SWLEDCPLD1': led_cpld1_version,
                             'SWLEDCPLD2': led_cpld2_version, 'U-BOOT': uboot_version, 'ONIE': onie_version,
                             'FANCPLD': fan_cpld, 'DIAGOS': diag_version}
        check_version_cmd = 'get_versions'
        output = device.executeCmd(check_version_cmd)
    else:
        uc_app = CommonLib.get_swinfo_dict("UC").get("newVersion", "NotFound").get("uC_app")
        uC_bl = CommonLib.get_swinfo_dict("UC").get("newVersion", "NotFound").get("uC_bl")
        asc1 = CommonLib.get_swinfo_dict("ASC").get("newVersion", "NotFound").get("ASC1")
        asc2 = CommonLib.get_swinfo_dict("ASC").get("newVersion", "NotFound").get("ASC2")
        hw_dict = {'uc_app': uc_app, 'uc_bl': uC_bl, 'ASC1': asc1, 'ASC2': asc2}
        cpld_version_dict = {'SystemCPLD': sys_cpld_version, 'SWLEDCPLD1': led_cpld1_version,
                             'SWLEDCPLD2': led_cpld2_version, 'FANCPLD': fan_cpld,'U-BOOT': uboot_version,'ONIE': onie_version}
        export_cmd_list = ['export LD_LIBRARY_PATH=/root/diag/output', 'export CEL_DIAG_PATH=/root/diag']
        get_hw_version_path = '/root/diag'
        get_hw_versions_tool = 'cel-system-test'
        get_hw_versions_option = '--all'
        for cmd in export_cmd_list:
            device.executeCmd(cmd)
        cmd = 'cd ' + get_hw_version_path
        device.executeCmd(cmd)
        check_cmd = './' + get_hw_versions_tool + ' ' + get_hw_versions_option
        output = device.executeCmd(check_cmd)
    hw_dict.update(cpld_version_dict)
    keys_list = list(hw_dict.keys())
    values_list = list(hw_dict.values())
    passpattern = list()
    if len(keys_list) == len(values_list):
        for i in range(0, len(keys_list)):
            passpattern.append('^' + keys_list[i] + '.*' + CommonLib.escapeString(values_list[i]))
    else:
        log.fail("get versions is failed")
        device.raiseException("Failure while get versions info")
    log.debug('passpattern=%s' % passpattern)
    passCount = 0
    match_list = list()
    for line in output.splitlines():
        line = line.strip()
        for pattern in passpattern:
            if re.search(pattern, line, re.IGNORECASE):
                log.debug('the matched version:%s' % line)
                match_list.append(pattern)
                passCount += 1
    if passCount == len(passpattern):
        log.success("verify version is passed")
    else:
        log.fail("not match pattern is: %s" % list(set(passpattern) - set(match_list)))
        device.raiseException("Failure while verify versions info")

@logThis
def checkdriverversion(pattern):
    check_driver_cmd = "lsmod"
    output = device.executeCmd(check_driver_cmd)
    CommonLib.execute_check_dict("DUT", "", patterns_dict=pattern, timeout=60,
                                check_output=output)

@logThis
def DiagformatDisk(fail_dict,cmd="mkfs.ext3 /dev/sda3", umount_mnt=True):

    if umount_mnt:
        output = run_command("mount", prompt=device.promptOnie,timeout=10)
        if re.search("/mnt", output):
            run_command(["cd /", "umount /mnt"], prompt=device.promptOnie,timeout=10)

    device.sendMsg(cmd + "\n")
    output = device.read_until_regexp("roceed anyway\? \(y,n\)\s+", timeout=90)
    device.sendMsg("y\n")
    output += device.read_until_regexp(device.promptOnie, timeout=60)
    fdisk_l_cmd = "fdisk -l \n"
    output += run_command(fdisk_l_cmd,prompt=device.promptOnie, timeout=5 )

    CommonLib.execute_check_dict("DUT", "", patterns_dict=fail_dict, timeout=10,
                                check_output=output, is_negative_test=True)

@logThis
def DiagmountDisk(fail_dict,cmd="mount /dev/sda3 /mnt"):

    cmd_list = ["cd /", "fdisk -l", cmd, "cd /mnt", "ls"]
    output = run_command(cmd_list, prompt=device.promptOnie,timeout=10)

    CommonLib.execute_check_dict("DUT", "", patterns_dict=fail_dict, timeout=10,
                                check_output=output, is_negative_test=True)

@logThis
def DiagdownloadImagesAndRecoveryDiagOS(fail_dict):

    diagos_files = CommonLib.get_swinfo_dict("DIAGOS").get("newImage")
    rootfs_file = diagos_files[:1]
    rename_files = ['rootfs.cpio.gz']
    run_command("cd /root",prompt=device.promptOnie )   #unzip file in /root to avoid space full issue
    log.info("rootfs_file: {}, rename_files: {}".format(rootfs_file, rename_files))
    CommonLib.tftp_get_files(Const.DUT, file_list=rootfs_file, renamed_file_list=rename_files, timeout=400)
    cmd_list = ["gunzip rootfs.cpio.gz", "cd /mnt", "cpio -i < /root/rootfs.cpio"]
    output = run_command(cmd_list, prompt=device.promptOnie,timeout=300)
    CommonLib.execute_check_dict("DUT", "", patterns_dict=fail_dict, timeout=10,
                                check_output=output, is_negative_test=True)
    run_command("rm /root/rootfs.cpio", prompt=device.promptOnie)
    run_command("rm -rf /mnt/root/*", prompt=device.promptOnie)
    run_command("cp -rf /root/* /mnt/root/", prompt=device.promptOnie)
    run_command("cd ./root",prompt=device.promptOnie)
    uimage_dtb = diagos_files[1:]
    rename_uimage_dtb = ["uImage", "celestica_cs8200-r0.dtb"]
    CommonLib.tftp_get_files(Const.DUT, file_list=uimage_dtb, renamed_file_list=rename_uimage_dtb, timeout=400)
    cmd_list = ["sync", "cd /", "umount /mnt"]
    output = run_command(cmd_list, prompt=device.promptOnie,timeout=300)
    CommonLib.execute_check_dict("DUT", "", patterns_dict=fail_dict, timeout=10,
                                check_output=output, is_negative_test=True)

@logThis
def checkWarmResetOnReboot(expect_status):
    output = device.executeCmd('cat /sys/bus/i2c/devices/8-0060/warm_reset_on_reboot')
    pattern  = r'^{}$'.format(expect_status)
    for line in output.splitlines():
        match = re.search(pattern, line)
        if match:
            log.success('warm_reset_on_reboot success')
            return
    raise RuntimeError('warm_reset_on_reboot failed')

@logThis
def checkColdResetOnReboot(expect_status):
    output = device.executeCmd('cat /sys/bus/i2c/devices/8-0060/cold_reset_on_reboot')
    pattern  = r'^{}$'.format(expect_status)
    for line in output.splitlines():
        match = re.search(pattern, line)
        if match:
            log.success('cold_reset_on_reboot success')
            return
    raise RuntimeError('cold_reset_on_reboot failed')

@logThis
def checki2cfpgaCardPresentStatus():
    devicename = os.environ.get("deviceName", "")
    if "tianhe" in devicename.lower():
        output = device.sendCmd('cat /sys/bus/i2c/devices/19-0060/i2cfpga_present')
    else:
        output = device.executeCmd('cat /sys/bus/i2c/devices/8-0060/i2cfpga_present')
    present  = r'^1$'.format()
    for line in output.splitlines():
        match = re.search(present, line)
        if match:
            log.success('i2cfpga_Card_Present')
            return
    raise RuntimeError('i2cfpga_Card_not_Present')



@logThis
def checki2cfpgalm75InterruptStatus():
    devicename = os.environ.get("deviceName", "")
    if "tianhe" in devicename.lower():
        output = device.sendCmd('cat /sys/bus/i2c/devices/19-0060/i2cfpga*_*lm75_interrupt')
    else:
        output = device.executeCmd('cat /sys/bus/i2c/devices/8-0060/i2cfpga*_*lm75_interrupt')

    nointerrupt  = r'^0$'.format()
    interrupt =  r'^1$'.format()
    for line in output.splitlines():
        matchnoint = re.search(nointerrupt, line)
        matchint = re.search(interrupt, line)
        if matchnoint:
            log.success('No interrupt')
            return
        elif matchint:
            log.success('Pending interrupt')
            return
    raise RuntimeError('No matching value to detect interrupt')

@logThis
def checkReadWriteScratchpadRegister():
    is_ipps = KapokCommonLib.is1ppsCard()
    if not is_ipps:
        log.info("============================================")
        log.info("This Device is not a 1PPS unit.")
        log.info("============================================")
        return
    default_val = device.executeCmd('cat /sys/devices/xilinx/pps-i2c/scratch')
    device.executeCmd('echo 0x87654321 > /sys/devices/xilinx/pps-i2c/scratch')
    read_val = device.executeCmd('cat /sys/devices/xilinx/pps-i2c/scratch')
    device.executeCmd('echo 0x12345678 > /sys/devices/xilinx/pps-i2c/scratch')
    write_val = device.executeCmd('cat /sys/devices/xilinx/pps-i2c/scratch')
    if '0x87654321' in read_val:
        log.success('read_scratchpad_register successfull.')
    else:
        raise RuntimeError('read_scratchpad_register failed!')
    if '0x12345678' in write_val:
        log.success('write_scratchpad_register successfull.')
    else:
        raise RuntimeError('write_scratchpad_register failed!')
    device.executeCmd('echo default_val > /sys/devices/xilinx/pps-i2c/scratch')

@logThis
def checkForFan7():
    if not KapokCommonLib.is19Inch():
       log.info('Fan 7 is not supported for 21" ')
    else:
       fan_module_eeprom_path = '/sys/bus/i2c/devices/31-0050/eeprom | hexdump -C'
       fan_module_eeprom_passpattern1 = ['000000.*\|\.+.*']
       fan_module_eeprom_passpattern2 = ['000000.*\|1234\.+.*']
       CatLoopFileInfo(path=fan_module_eeprom_path, part=0, passpattern=fan_module_eeprom_passpattern1)
       device.executeCmd('echo 1234 > /sys/bus/i2c/devices/31-0050/eeprom')
       CatLoopFileInfo(path=fan_module_eeprom_path, part=0, passpattern=fan_module_eeprom_passpattern2)
       device.executeCmd("echo -n -e '....' > /sys/bus/i2c/devices/31-0050/eeprom")
       CatLoopFileInfo(path=fan_module_eeprom_path, part=0, passpattern=fan_module_eeprom_passpattern1)
       log.success('Fan 7 (31-0050) read write successful')
    log.success('FAN tray EEPROM check successful')


@logThis
def checkcurrentversion():
    if not KapokCommonLib.is1ppsCard():
        log.info('This operation only supported on 1pps card!')
        return
    output= defaultval = device.executeCmd('cat /sys/devices/xilinx/pps-i2c/version')
    if not re.search(current_version,output):
        log.fail('Version should be ' + current_version)
    else:
        log.success('Version  is ' + current_version)


@logThis
def checkcurrentboardversion():
    if not KapokCommonLib.is1ppsCard():
        log.info('This operation only supported on 1pps card!')
        return
    output= default_val = device.executeCmd('cat /sys/devices/xilinx/pps-i2c/board_version')
    if not re.search(board_version,output):
        log.fail('Board version should be ' + board_version)
    else:
        log.success('Board version is ' +board_version)


@logThis
def checkcurrentimageversion():
    if not KapokCommonLib.is1ppsCard():
        log.info('This operation only supported on 1pps card!')
        return
    output= default_val = device.executeCmd('cat /sys/devices/xilinx/pps-i2c/image_version')
    if not re.search(image_version,output):
        log.fail('Image version should be '+ image_version)
    else:
        log.success('Image version is '+ image_version)



@logThis
def checkpcbversion():
    if not KapokCommonLib.is1ppsCard():
        log.info('This operation only supported on 1pps card!')
        return
    output= default_val = device.executeCmd('cat /sys/devices/xilinx/pps-i2c/pcb_version')
    if not re.search(pcb_version,output):
        log.fail('PCB version should be ' + pcb_version)
    else:
        log.success('PCB version is ' + pcb_version)

@logThis
def checkrawaccessinfo(output_value1,output_value2):
    if not KapokCommonLib.is1ppsCard():
        log.info('This operation only supported on 1pps card!')
        return
    val1 = device.executeCmd('cat /sys/devices/xilinx/pps-i2c/raw_access_data')
    val2 = device.executeCmd('cat /sys/devices/xilinx/pps-i2c/raw_access_addr')
    if re.search(output_value1,val1):
        log.success("The raw access data is correct  : " + output_value1)
    else:
        log.fail ("The raw acces data is incorrect.Should be : " + output_value1)

    if re.search(output_value2,val2):
        log.success("The raw access data is correct  : " + output_value2)
    else:
        log.fail ("The raw acces data is incorrect.Should be : " + output_value2)

@logThis
def Modifysysfsnote(path,value):
    is_fpga = KapokCommonLib.isFpgaCard()
    if not is_fpga:
        log.info("============================================")
        log.info("This Device is not a FPGA unit.")
        log.info("============================================")
        return
    log.debug("Entering BspTestCase procedure modifysysfsnote:")
    cmd = 'echo ' + value + ' ' + '>' + ' ' + path
    time.sleep(5)
    output = device.executeCmd(cmd)
    #VerifyExeCmdNoOutput(output=output)
    return output


@logThis
def checkaccelpcbversion():
    if KapokCommonLib.is1ppsCard():
        log.info('This operation not supported on 1pps card!')
        return
    output= default_val = device.executeCmd('cat /sys/devices/xilinx/accel-i2c/pcb_version')
    if not re.search(pcb_version,output):
        log.fail('PCB version should be ' + pcb_version)
    else:
        log.success('PCB version is ' + pcb_version)




@logThis
def checkaccelrawaccessinfo(output_value1,output_value2):
    is_fpga = KapokCommonLib.isFpgaCard()
    if not is_fpga:
        log.info("============================================")
        log.info("This Device is not a FPGA unit.")
        log.info("============================================")
        return
    val1 = device.executeCmd('cat /sys/devices/xilinx/accel-i2c/raw_access_data')
    val2 = device.executeCmd('cat /sys/devices/xilinx/accel-i2c/raw_access_addr')
    if re.search(output_value1,val1):
        log.success("The raw access data is correct  : " + output_value1)
    else:
        log.fail ("The raw acces data is incorrect.Should be : " + output_value1)

    if re.search(output_value2,val2):
        log.success("The raw access data is correct  : " + output_value2)
    else:
        log.fail ("The raw acces data is incorrect.Should be : " + output_value2)


@logThis
def getEntry(path, cmd):
    device.sendMsg(path + " \n")
    output = device.executeCmd(cmd)
    regx = re.findall("000000[0-8]0.*|",output)
    entry = []
    for each in regx:
        entry.append(each) if each != '' else None
    return entry

@logThis
def reboot():
    device.sendMsg("reboot \n")
    device.read_until_regexp("ONIE: Starting ONIE Service Discovery", timeout=260)
    device.sendMsg("\n \n \n onie-discovery-stop \n \n")

@logThis
def checkFaultLoggerFunction(fault_logger_path, fault_logger_cmd):
    
    entry1 = getEntry(fault_logger_path, fault_logger_cmd)
    device.sendMsg("echo 1 > fault_logger_reset \n")

    reboot()
    entry2 = getEntry(fault_logger_path, fault_logger_cmd)
    device.sendMsg("echo 1 > fault_logger_pause \n")

    reboot()
    entry3 = getEntry(fault_logger_path, fault_logger_cmd)
    device.sendMsg("echo 0 > fault_logger_pause \n")

    reboot()
    entry4 = getEntry(fault_logger_path, fault_logger_cmd)

    condition1 = "".join(entry1[:4]) != "".join(entry2[:4])
    condition2 = "".join(entry2) == "".join(entry3)
    condition3 = "".join(entry3[4:8]) != "".join(entry4[4:8])

    if condition1 and condition2 and condition3:
        log.success("The log function is correct.")
    else:
        log.fail("The log function is incorrect.")

@logThis
def hexdump(device_path):
    output = device.executeCmd("hexdump -C " + device_path)
    output = output.splitlines()
    for each in output:
        if "00000000" in each:
            return each[len(each)-18:]


@logThis
def check_eeprom(device_path):
    op1 = hexdump(device_path)
    device.sendMsg("echo 1234 > " + device_path + " \n")

    op2 = hexdump(device_path)
    device.sendMsg("echo -n -e '\\x01\\x00\\x00\\x01\\x00\\x00' > " + device_path + " \n")

    op3 = hexdump(device_path)

    if op1 == op3 and op2[1:5] == "1234":
        return True
    return False


@logThis
def busbarBoardEepromTest():
    device_path = "/sys/bus/i2c/devices/15-0054/eeprom"
    if check_eeprom(device_path):
        log.success("Busbar EEPROM is correct.")
    else:
        log.fail("Busbar EEPROM is incorrect.")


@logThis
def I2cfpgaBoardEepromTest():
    is_fpga = KapokCommonLib.isFpgaCard()
    if not is_fpga:
        log.info("============================================")
        log.info("This Device is not a FPGA unit.")
        log.info("============================================")
        return
    device_path = "/sys/bus/i2c/devices/6-0056/eeprom"
    eeprom_write_path = "/sys/bus/i2c/devices/8-0060/i2cfpga_eeprom_write_protect"

    output = device.executeCmd("cat " + eeprom_write_path)
    for each in output:
        if each == "1":
            device.sendMsg("echo 0 > " + eeprom_write_path + " \n")
            break

    if check_eeprom(device_path):
        device.sendMsg("echo 1 > " + eeprom_write_path + " \n")
        device.sendMsg("echo 1234 > " + device_path + " \n")
        if hexdump(device_path)[1:5] == "....":
            log.success("I2CFPGA Board EEPROM is correct.")
        else:
            log.fail("I2CFPGA Board EEPROM is incorrect.")
    else:
        log.fail("EEPROM data in incorrect.")

@logThis
def readMaskValues():
    path = "/sys/devices/xilinx/accel-i2c/port"
    output = ""
    values = []

    for i in range(1,33):
        cmd = "cat " + path + str(i) + "_module_interrupt_mask"
        output += "\n" + device.executeCmd(cmd)
    for each in output.splitlines():
        if each == "1" or each == "0":
            values.append(each)
    return values

@logThis
def PortModuleInterruptMaskTest():
    is_fpga = KapokCommonLib.isFpgaCard()
    if not is_fpga:
        log.info("============================================")
        log.info("This Device is not a FPGA unit.")
        log.info("============================================")
        return
    path = "/sys/devices/xilinx/accel-i2c/port"
    initial_values = readMaskValues()
    for i in range(1,33):
        cmd = "echo 0 > " + path + str(i) + "_module_interrupt_mask"
        device.sendMsg(cmd + " \n")

    changed_values = readMaskValues()

    for i in range(1,33):
        cmd = "echo " + initial_values[i-1] + " > " + path + str(i) + "_module_interrupt_mask"
        device.executeCmd(cmd)

    if changed_values.count("0") == 32:
        log.success("Read/Set the optical module interrupt mask value successful.")
    else:
        log.fail("Error in setting the optical module interrupt mask values.")
    log.success("Original values restored successfully.\n")


@logThis
def profileSpeedTestNew():
    devicename = os.environ.get("deviceName", "")
    if "fenghuangv2" in devicename.lower():
        dev_type = DeviceMgr.getDevice(devicename).get('cardType')
        if dev_type == 'FPGA':
            port_file_path = '/sys/devices/xilinx/accel-i2c/'
        else:
            port_file_path = '/sys/devices/xilinx/pps-i2c/'

    passpattern1 = ['100000']
    passpattern2 = ['400000']
    passpattern3 = ['1000000']
    pass_pattern = [passpattern1, passpattern2, passpattern3]
    echo_value = ['100000', '400000', '1000000']
    for i in range(0,32):
        i += 1
        filename1 = 'port' + str(i) + '_i2c_profile1_speed'
        filename2 = 'port' + str(i) + '_i2c_profile2_speed'
        EchoValueToFile(port_file_path, filename1, echo_value[0])
        EchoValueToFile(port_file_path, filename2, echo_value[0])
        CatLoopFileInfo(path=port_file_path, pre=filename1, part=0, passpattern=pass_pattern[0])
        CatLoopFileInfo(path=port_file_path, pre=filename2, part=0, passpattern=pass_pattern[0])
    for i in range(0,32):
        i += 1
        filename1 = 'port' + str(i) + '_i2c_profile1_speed'
        filename2 = 'port' + str(i) + '_i2c_profile2_speed'
        EchoValueToFile(port_file_path, filename1, echo_value[1])
        EchoValueToFile(port_file_path, filename2, echo_value[1])
        CatLoopFileInfo(path=port_file_path, pre=filename1, part=0, passpattern=pass_pattern[1])
        CatLoopFileInfo(path=port_file_path, pre=filename2, part=0, passpattern=pass_pattern[1])
    for i in range(0,32):
        i += 1
        filename1 = 'port' + str(i) + '_i2c_profile1_speed'
        filename2 = 'port' + str(i) + '_i2c_profile2_speed'
        EchoValueToFile(port_file_path, filename1, echo_value[2])
        EchoValueToFile(port_file_path, filename2, echo_value[2])
        CatLoopFileInfo(path=port_file_path, pre=filename1, part=0, passpattern=pass_pattern[2])
        CatLoopFileInfo(path=port_file_path, pre=filename2, part=0, passpattern=pass_pattern[2])






@logThis
def checkaccelimageversion():
    if KapokCommonLib.is1ppsCard():
        log.info('This operation only supported on 1pps card!')
        return
    output= default_val = device.executeCmd('cat /sys/devices/xilinx/accel-i2c/image_version')
    if not re.search(image_version,output):
        log.fail('Image version should be '+ image_version)
    else:
        log.success('Image version is '+ image_version)

@logThis
def runAsc10Commands(cmd, pattern1, pattern2 = None):
    output = ""
    for each in cmd:
        output += (device.executeCmd(each))

    output =  "".join(output.splitlines())
    if pattern2:
        return (re.findall(pattern1, output), re.findall(pattern2, output))
    return re.findall(pattern1, output)

@logThis
def CheckAsc10EepromAndCrc(fw_cmd, eeprom_cmd, cat_crc_cmd):
    output = ""

    fw_hex = ""
    eeprom_hex = ""
    fw_crc = ""
    eeprom_crc = ""

    fw_p1 = "Data row 0 ~ 13.{224}"
    fw_p2 = "CRC: .{4}"
    eeprom_pattern = "000000[0-6]0.{50}"
    crc_pattern = "crc.{4}"

    output = runAsc10Commands(fw_cmd, fw_p1,  fw_p2)
    for each in output[0]:
        fw_hex += each[len(each)-224:]

    for each in output[1]:
        fw_crc += each[5:9]

    output = runAsc10Commands(eeprom_cmd, eeprom_pattern)
    for each in output:
        eeprom_hex += each[10:].replace(" ","")

    output = runAsc10Commands(cat_crc_cmd, crc_pattern)
    for each in output:
        eeprom_crc += each[3:]
    
    if fw_hex == eeprom_hex and fw_crc == eeprom_crc:
        log.success("asc10 eeprom and crc sysfs node is correct.\nBoth HEX and CRC values are same.")
    else:
        log.fail("asc10 eeprom and crc sysfs node is not correct.\nThere are different HEX or CRC values.")

    log.info("Expected Output :---> Both HEX and CRC should be the same.")



@logThis
def masterResetTest():
    pa = '/sys/devices/xilinx/accel-i2c/port'
    flag = 1
    reset = 1
    if KapokCommonLib.is1ppsCard():
        log.info('This operation only supported on fpga card!')
        return
    start = 4176
    for i in range(1,33):
        out = run_command("cat " + pa + str(i)+ "_i2c_master_reset")
        out = out.split()
        for x in out:
            if x == '0':
                log.success("Master reset value for port " + str(i) + " is 0")
                flag = 0
        #else:
        #    log.fail("Master reset value for port " + str(i) + " should be  0"
        #    flag = 1
        device.executeCmd("echo " +  " 1" + " > " + pa + str(i) + "_i2c_master_reset" )
        out =  device.executeCmd("cat " + pa + str(i)+ "_i2c_master_reset")
        out = out.split()
        for x in out:
            if x == '0':
                log.success("Master reset value for port " + str(i) + " is 0")
                reset = 0
        #else:
        #    log.fail("Master reset value for port " + str(i) + " should be  0"
        #    reset = 1
    if flag == 0 and reset == 0:
        log.success("Master port reset worked for all ports")
    else:
        log.fail("Master reset failed for some ports")



@logThis
def setI2cProfileSpeed():
    if not KapokCommonLib.is1ppsCard():
        log.info('This operation only supported on 1pps card!')
        return
    start = 4176
    for i in range(1,33):
        device.executeCmd("echo " + hex(start) + " 0" + "> " + data_path)
        device.executeCmd("echo " + hex(start) + "> " + addr_path)
        print("\n")
        output = device.executeCmd("echo 1 " + "> " + i2c_path  + str(i) + "_i2c_9_clock")
        if re.search("Error|error",output):
            log.fail("Error executing command for port : " + str(i))
        start= start + 256


@logThis
def switchToDiagMode():
    device.read_until_regexp(device.promptUboot,timeout=60)
    device.sendMsg('\r')
    device.sendCmd('run diag_bootcmd')
    device.read_until_regexp("Please press Enter to activate this console.",timeout=200)
    device.sendCmd('\r','#',timeout=5)
    device.read_until_regexp(device.promptDiagOS)

@logThis
def VerifyBoardVersion():
    log.debug("Entering BspTestCase procedure: VerifyBoardVersions")
    board_version = CommonLib.get_swinfo_dict("Board_version").get("newVersion","NotFound")
    cmd = 'cd /sys/bus/i2c/devices/19-0060'
    device.sendCmd(cmd,timeout=5)
    ver_check_cmd = 'cat board_version'
    output = device.executeCmd(ver_check_cmd)
    if not board_version in output:
        raise Exception("Board version mismatched")
    log.success("Board version matched")

@logThis
def getOnieVersion():
    cmd='onie-sysinfo -v'
    Image_info_dict = CommonLib.get_swinfo_dict("ONIE_Installer")
    onie_version = Image_info_dict.get("newVersion", "NotFound")
    output =  run_command(cmd,prompt='#',timeout=10)
    if not onie_version in output:
        raise Exception("Onie version mismatched")
    log.success("Onie version matched")

@logThis
def check_or_reinstall_bsp_driver(driveVer):
    #1. check driver version
    p1 = r'Version <(.*)>'
    pass_count = 0
    error_count = 0
    p2 = 'No such file or directory'
    driveObj = CommonLib.get_swinfo_dict("BSP_DRIVER")
    driveHostPath = driveObj.get("hostImageDir", "NotFound")
    driveLocalPath = driveObj.get("localImageDir", "NotFound")
    driveImg = driveObj.get("newImage", "NotFound")
    drive_version = driveObj.get("newVersion", "NotFound")
    output = run_command(driveVer, timeout=60)
    for line in output.splitlines():
        line = line.strip()
        if re.search(p2, line):
            error_count += 1
            log.fail('Do not find drive version file.')
        res = re.search(p1, line)
        if res:
            get_ver = res.group(1)
            break
    if get_ver == drive_version:
        log.success('Check drive version [%s] pass.'%get_ver)
        output = CommonLib.execute_command('lsmod', timeout=60)
        check_drive_info(output)
    else:
        log.info('GetVer: %s, ExpectVer: %s, need to update drive.'%(get_ver, drive_version))
        #2. uninstall old drive
        switch_bsp_folder_path(driveLocalPath)
        CommonLib.execute_command('ls', timeout=60)
        CommonLib.execute_command(RMMODE_TOOL, timeout=60)
        #3. copy new drive package
        switch_bsp_folder_path('..')
        driveLst = [RMDRIVE, MKDIRVE]
        for cmd in driveLst:
            CommonLib.execute_command(cmd, timeout=60)
        switch_bsp_folder_path(driveLocalPath)
        download_cmd = 'tftp -g ' + server_ipv4 + ' -r ' + driveHostPath + '/' + driveImg
        CommonLib.execute_command(download_cmd, timeout=90)
        #4. install new drive
        untarLst = [DRIVXZ, DRIVETAR, DRIVEINST, 'ls']
        for cmd in untarLst:
            time.sleep(2)
            CommonLib.execute_command(cmd, timeout=60)
        output = CommonLib.execute_command('lsmod', timeout=60)
        check_drive_info(output)

@logThis
def read_cpld1_register(addrCmd, dataCmd, addrRes, dataRes):
    p1 = '0x\d+'
    error_count = 0
    rawCmdLst = [addrCmd, dataCmd]
    rawResLst = [addrRes, dataRes]
    for i in range(0, 2):
        output = CommonLib.execute_command(rawCmdLst[i], timeout=60)
        res = re.search(p1, output)
        if res:
            getRes = res.group(0)
            if getRes == rawResLst[i]:
                log.success('Get the value is %s.'%getRes)
            else:
                log.fail('Fail get value is %s, expect value is %s'%(getRes, rawResLst[i]))
    if error_count:
        raise Exception('Failed run read_cpld1_register')

@logThis
def write_cpld1_raw_register(dataCmd, addrCmd):
    rawLst = [dataCmd, addrCmd]
    for cmd in rawLst:
        CommonLib.execute_command(cmd, timeout=60)

@logThis
def check_the_console_logs(cmd, pattern_tool=''):
    error_count = 0
    p1 = '([\d.]+)\+'
    p2 = '(Disk|fdisk)'
    # p3 = '2048'
    p3 = '\|.*2048.*\|'
    p4 = 'echo 0 > console_logger_pause'
    if 'uname' in pattern_tool or 'fdisk' in pattern_tool:
        # output = CommonLib.execute_command(pattern_tool, timeout=120)
        output = device.executeCommand(pattern_tool, device.promptDiagOS, timeout=120)
        if 'uname' in pattern_tool:
            res = re.search(p1, output)
            if res:
                get_pattern = res.group(1)
                log.success('Get the operating system release number is %s' % get_pattern)
                output = device.executeCommand(cmd, device.promptDiagOS, timeout=120)
                if 'uname' in output:
                    log.success('Found keyword [%s] in console log.' % get_pattern)
                else:
                    error_count += 1
                    log.fail('Do not find the match [%s] value.' % get_pattern)
            else:
                error_count += 1
                log.fail('Do not match in console log.')
        else:
            res = re.search(p2, output)
            if res:
                # get_pattern = res.group(0)
                log.success('Get the disk info.')
                output = device.executeCommand(cmd, device.promptDiagOS, timeout=120)
                if p4 in output:
                    error_count += 1
                    log.fail('Do not should find the match [%s] value.'%p4)
            else:
                error_count += 1
                log.fail('Do not match in console log.')
    elif pattern_tool == 'bs':
        output = device.executeCommand(cmd, device.promptDiagOS, timeout=120)
        if re.search(p3, output):
            error_count += 1
            log.fail('Do not should find bs=2048 info.')
    else:
        device.executeCommand(cmd, device.promptDiagOS, timeout=120)
    if error_count:
        raise Exception('Failed run check_the_console_logs')

@logThis
def console_logger_reset_or_pause_or_start(cmd):
    # CommonLib.execute_command(cmd, timeout=60)
    device.executeCommand(cmd, device.promptDiagOS, timeout=120)

@logThis
def switch_bsp_folder_path(path):
    cmd = 'cd ' + path
    p1 = "can't cd"
    output = device.executeCommand(cmd, device.promptDiagOS)
    if re.search(p1, output):
        log.fail('switch folder fail!')
        raise Exception('Change %s path failed!' % (path))
    else:
        log.info('Switch the folder successfully!')

@logThis
def check_drive_info(output):
    pass_count = 0
    p1 = r'([\w_]+)\s+(\d+)\s+0\s+-\s+Live'
    for key, value in drive_pattern_dict.items():
        res = re.search(value, output)
        if res:
            pass_count += 1
            log.success('Check %s drive info pass.'%key)
    if pass_count == len(drive_pattern_dict):
        log.info('Check drive info pass!')
    else:
        raise Exception('Failed run check_drive_info')

@logThis
def write_and_read_fan_max_speed(tool, status):
    #1. write first
    cmd = 'echo ' + status + ' > ' + tool
    CommonLib.execute_command(cmd, timeout=60)
    #2. read
    cmd = 'cat ' + tool
    check_psu_voltage_status_test(cmd, status)

@logThis
def set_fan_speed(tool, option):
    cmd = './' + tool + option
    CommonLib.execute_command(cmd, timeout=60)

@logThis
def check_fan_max_speed_status(tool, pattern):
    check_psu_voltage_status_test(tool, pattern)

@logThis
def check_psu_voltage_status_test(tool, pattern):
    p1 = r'^\d+'
    output = CommonLib.execute_command(tool, timeout=60)
    for line in output.splitlines():
        line = line.strip()
        res = re.search(p1, line)
        if res:
            if res.group(0) == pattern:
                log.success('Check the value is %s' % res.group(0))
            else:
                log.fail('Check fail, the value is %s' % res.group(0))
                raise Exception('Failed run check_one_by_one_port_signal_status.')

@logThis
def write_register_to_reset_port_module(tool, option, pattern):
    for i in range(1, 33):
        cmd = 'echo ' + pattern + ' > ' + tool + str(i) + option
        CommonLib.execute_command(cmd, timeout=60)

@logThis
def check_one_by_one_port_signal_status(tool, option, pattern):
    error_count = 0
    p1 = r'^\d'
    for i in range(1, 33):
        cmd = tool + str(i) + option
        output = CommonLib.execute_command(cmd, timeout=120)
        for line in output.splitlines():
            line = line.strip()
            res = re.search(p1, line)
            if res:
                if res.group(0) == pattern:
                    log.success('Check the value is %s'%res.group(0))
                else:
                    error_count += 1
                    log.fail('Check fail, the value is %s'%res.group(0))
    if error_count:
        raise Exception('Failed run check_one_by_one_port_signal_status.')

@logThis
def check_IntL_signal_status(tool, option, pattern):
    error_count = 0
    p1 = r'\d+\s+\|\s+(port-\d+)\s+\|.*\|\s+(P\w+)\s+\|\s+\d\s+\|\s+(\d)\s+\|.*K'
    switch_bsp_folder_path('/root/diag/')
    cmd = './' + tool + option
    output = CommonLib.execute_command(cmd, timeout=120)
    for line in output.splitlines():
        line = line.strip()
        res = re.search(p1, line)
        if res:
            port_num = res.group(1)
            port_status = res.group(2)
            port_status_value = res.group(3)
            if port_status == 'Present' and port_status_value == pattern:
                log.success('Check %s status is %s, the value is %s'%(port_num, port_status, port_status_value))
            else:
                error_count += 1
                log.fail('Check %s fail, get the status is %s, value is %s'%(port_num, port_status, port_status_value))
    if error_count:
        raise Exception('Failed run check_IntL_signal_status.')

@logThis
def set_or_clear_IntL_signal_test(tool, option):
    for i in range(101, 133):
        cmd = tool + str(i) + option
        CommonLib.execute_command(cmd, timeout=60)


@logThis
def stop_fcs_before_test(tool):
    switch_bsp_folder_path(DIAG_PATH)
    cmd = 'pkill ' + tool
    CommonLib.execute_command(cmd, timeout=120)

@logThis
def read_all_fan_speed(tool, option, pattern):
    time.sleep(10)
    error_count = 0
    p1 = r'PWM\s+\|\s+\d\s+\|\s+255\s+\|\s+(\d+)'
    cmd = './' + tool + option
    output = CommonLib.execute_command(cmd, timeout=120)
    for line in output.splitlines():
        line = line.strip()
        res = re.search(p1, line)
        if res:
            get_speed = res.group(1)
            if get_speed == pattern:
                log.success('Check fan speed is %s'%get_speed)
            else:
                error_count += 1
                log.fail('Check fail, get fan speed is %s, expect is %s'%(get_speed, pattern))
    if error_count:
        raise Exception('Failed run read_all_fan_speed')


@logThis
def check_the_system_watchdog_status(tool, pattern):
    time.sleep(20)
    p1 = r'^0x\w+|^(0x)?\d+'
    cmd = 'cat ' + tool
    output = CommonLib.execute_command(cmd, timeout=120)
    for line in output.splitlines():
        line = line.strip()
        res = re.search(p1, line)
        if res:
            get_value = res.group(0)
            if get_value == pattern:
                log.success('Get the watchdog enable status is %s'%get_value)
            else:
                raise Exception('Failed get watchdog status is %s, expect status is %s'%(get_value, pattern))


@logThis
def enable_or_disable_system_watchdog(tool, pattern):
    cmd = 'echo ' + pattern + ' > ' + tool
    CommonLib.execute_command(cmd, timeout=120)
    if pattern == '1':
        device.read_until_regexp(KapokConst.STOP_AUTOBOOT_PROMPT, timeout=180)
        device.sendMsg(KapokConst.STOP_AUTOBOOT_KEY)
        switchToDiagMode()

@logThis
def multi_enable_system_watchdog(tool, pattern1, pattern2):
    cmd = 'echo ' + pattern1 + ' > ' + tool
    sleep_5_cmd = 'sleep ' + pattern2
    sleep_10_cmd = 'sleep ' + TRIGGER_10_TIME
    for i in range(0, 3):
        CommonLib.execute_command(cmd, timeout=60)
        if i == 2:
            # CommonLib.execute_command(sleep_10_cmd, timeout=60)
            device.sendMsg(sleep_10_cmd)
            # device.executeCommand(sleep_10_cmd, device.promptDiagOS, timeout=60)
            device.read_until_regexp(KapokConst.STOP_AUTOBOOT_PROMPT, timeout=180)
            device.sendMsg(KapokConst.STOP_AUTOBOOT_KEY)
            switchToDiagMode()
        else:
            CommonLib.execute_command(sleep_5_cmd, timeout=60)

@logThis
def check_current_fan_watchdog(tool, pattern):
    time.sleep(2)
    check_the_system_watchdog_status(tool, pattern)

@logThis
def set_fan_watchdog_enable_or_disable(tool, pattern):
    cmd = 'echo ' + pattern + ' > ' + tool
    CommonLib.execute_command(cmd, timeout=120)

@logThis
def check_fan_speed_value(tool, option, pattern):
    read_all_fan_speed(tool, option, pattern)
    CommonLib.execute_command('sleep 120', timeout=150)
    read_all_fan_speed(tool, option, FAN_255_VALUE)

@logThis
def set_and_check_fan_speed(tool, option1, option2, pattern):
    CommonLib.execute_command('sleep 15', timeout=50)
    cmd = './' + tool + option1
    CommonLib.execute_command(cmd, timeout=60)
    error_count = 0
    p1 = r'PWM\s+\|\s+\d\s+\|\s+255\s+\|\s+(\d+)'
    cmd = './' + tool + option2
    output = CommonLib.execute_command(cmd, timeout=120)
    for line in output.splitlines():
        line = line.strip()
        res = re.search(p1, line)
        if res:
            get_speed = res.group(1)
            if get_speed == pattern:
                log.success('Check fan speed is %s' % get_speed)
            else:
                error_count += 1
                log.fail('Check fail, get fan speed is %s, expect is %s' % (get_speed, pattern))
    if error_count:
        raise Exception('Failed run read_all_fan_speed')
    CommonLib.execute_command('sleep 15', timeout=120)
    read_all_fan_speed(tool, option2, FAN_255_VALUE)


@logThis
def check_warm_or_cold_reset_test(cmd):
    CommonLib.execute_command(cmd, timeout=60)
    device.read_until_regexp(KapokConst.STOP_AUTOBOOT_PROMPT, timeout=300)
    device.sendMsg(KapokConst.STOP_AUTOBOOT_KEY)
    switchToDiagMode()

@logThis
def read_fan_reset_value(tool, pattern):
    check_the_system_watchdog_status(tool, pattern)

@logThis
def reset_fan_cpld_test(tool, pattern):
    set_fan_watchdog_enable_or_disable(tool, pattern)

@logThis
def check_led_cpld_reset(tool, pattern):
    check_the_system_watchdog_status(tool, pattern)

@logThis
def reset_led_cpld_test(tool, pattern):
    set_fan_watchdog_enable_or_disable(tool, pattern)

@logThis
def set_to_original_value(tool, pattern):
    set_fan_watchdog_enable_or_disable(tool, pattern)
    check_the_system_watchdog_status(tool, pattern)

@logThis
def check_switch_board_eeprom_status(tool, pattern):
    check_the_system_watchdog_status(tool, pattern)

@logThis
def disable_or_enable_write_protect(tool, pattern):
    set_fan_watchdog_enable_or_disable(tool, pattern)

@logThis
def read_switch_board_eeprom_test(tool, option, pattern):
    p1 = r'\|([\w.]+fo).*\|'
    cmd = tool + ' -C ' + option
    output = CommonLib.execute_command(cmd, timeout=60)
    res = re.search(p1, output)
    if res:
        get_value = res.group(1)
        if get_value == pattern:
            log.success('read switch eeprom value pass.')
        else:
            raise Exception('Failed get value is %s, expect value is %s.'%(get_value, pattern))

@logThis
def write_some_data_into_eeprom(tool, pattern):
    set_fan_watchdog_enable_or_disable(tool, pattern)

@logThis
def read_back_the_eeprom_data(tool, option, pattern):
    read_switch_board_eeprom_test(tool, option, pattern)

@logThis
def write_original_data_back_to_eeprom(tool, pattern):
    cmd = "echo -n -e '" + pattern + "' > "  + tool
    CommonLib.execute_command(cmd, timeout=120)

@logThis
def write_some_data_into_eeprom_again(tool, pattern1, pattern2):
    cmd = 'echo ' + pattern1 + ' > ' + tool
    output = CommonLib.execute_command(cmd, timeout=120)
    res = re.search(pattern2, output)
    if res:
        log.success('write protect is enable, so can not write data.')
    else:
        raise Exception('Failed run write_some_data_into_eeprom_again.')

@logThis
def check_fan_direction_test(tool, option, pattern):
    error_count = 0
    p1 = r'^\d+'
    for i in range(1, 13):
        cmd = 'cat ' + tool + str(i) + option
        output = CommonLib.execute_command(cmd, timeout=120)
        for line in output.splitlines():
            line = line.strip()
            res = re.search(p1, line)
            if res:
                get_value = res.group(0)
                if get_value == pattern:
                    log.success('Check fan-%d value is %s'%(i, get_value))
                else:
                    error_count += 1
                    log.fail('Check fan-%d fail, get value is %s, expect value is %s'%(i, get_value, pattern))
    if error_count:
        raise Exception('Failed run check_fan_direction_test.')

@logThis
def read_fan_maximum_speed(tool, option, pattern):
    check_fan_direction_test(tool, option, pattern)

@logThis
def check_current_maximum_fan_speed(tool, option, pattern1, pattern2):
    error_count = 0
    pass_count = 0
    p1 = r'^\d+'
    for i in range(1, 13):
        cmd = 'cat ' + tool + str(i) + option
        output = CommonLib.execute_command(cmd, timeout=120)
        for line in output.splitlines():
            line = line.strip()
            res = re.search(p1, line)
            if res:
                pass_count += 1
                get_value = res.group(0)
                if (i % 2) == 0:
                    if get_value == pattern2:
                        log.success('Check fan-%d value is %s' % (i, get_value))
                    else:
                        error_count += 1
                        log.fail('Check fan-%d fail, get value is %s, expect value is %s' % (i, get_value, pattern2))
                else:
                    if get_value == pattern1:
                        log.success('Check fan-%d value is %s' % (i, get_value))
                    else:
                        error_count += 1
                        log.fail('Check fan-%d fail, get value is %s, expect value is %s' % (i, get_value, pattern1))
    if error_count or pass_count == 0:
        raise Exception('Failed run check_current_maximum_fan_speed.')

@logThis
def set_maximum_fan_speed(tool, option, pattern):
    for i in range(1, 13):
        cmd = 'echo ' + pattern + ' > ' + tool + str(i) + option
        CommonLib.execute_command(cmd, timeout=120)

@logThis
def fan_speed_set_back_to_default(tool, option, pattern1, pattern2):
    for i in range(1, 13):
        if (i % 2) == 0:
            cmd = 'echo ' + pattern2 + ' > ' + tool + str(i) + option
        else:
            cmd = 'echo ' + pattern1 + ' > ' + tool + str(i) + option
        CommonLib.execute_command(cmd, timeout=120)
    check_current_maximum_fan_speed(tool, option, pattern1, pattern2)

@logThis
def fan_min_speed_set_back_to_default(tool, option, pattern):
    set_maximum_fan_speed(tool, option, pattern)
    time.sleep(2)
    read_fan_maximum_speed(tool, option, pattern)

@logThis
def check_the_fan_current_protect_status(tool, pattern):
    check_the_system_watchdog_status(tool, pattern)

@logThis
def set_and_read_fan_board_eeprom_protect_active_or_inactive(tool, pattern):
    set_fan_watchdog_enable_or_disable(tool, pattern)
    time.sleep(2)
    check_the_system_watchdog_status(tool, pattern)

@logThis
def check_fan_speed_pwm(tool, pattern):
    error_count = 0
    p1 = r'^\d+'
    for i in range(1, 13):
        cmd = 'cat ' + tool + str(i)
        output = CommonLib.execute_command(cmd, timeout=120)
        for line in output.splitlines():
            line = line.strip()
            res = re.search(p1, line)
            if res:
                get_value = res.group(0)
                if get_value == pattern:
                    log.success('Check fan-%d speed pwm value is %s'%(i, get_value))
                else:
                    error_count += 1
                    log.fail('Check fan-%d speed pwm fail, getValue: %s, expectValue: %s'%(i, get_value, pattern))
    if error_count:
        raise Exception('Failed run check_fan_speed_pwm.')

@logThis
def set_fan_speed_pwm_value(tool, pattern):
    for i in range(1, 13):
        cmd = 'echo ' + pattern + ' > ' + tool + str(i)
        CommonLib.execute_command(cmd, timeout=120)

@logThis
def fan_cpld_read_register_data(tool1, tool2, pattern1, pattern2):
    check_the_system_watchdog_status(tool1, pattern1)
    check_the_system_watchdog_status(tool2, pattern2)

@logThis
def fan_cpld_set_register_data(tool, pattern1, pattern2):
    cmd1 = 'echo ' + pattern1 + ' > ' + tool
    cmd2 = 'echo "' + pattern1 + ' ' + pattern2 + '" > ' + tool
    cmdLst = [cmd1, cmd2]
    for cmd in cmdLst:
        time.sleep(1)
        CommonLib.execute_command(cmd, timeout=120)

@logThis
def restore_to_original_fan_raw_access_value(tool1, tool2, pattern1, pattern2):
    fan_cpld_set_register_data(tool2, pattern2, pattern1)
    time.sleep(2)
    fan_cpld_read_register_data(tool1, tool2, pattern1, pattern2)

@logThis
def read_asc10_voltage_value(toolLst, option, minLst, maxLst):
    error_count = 0
    p1 = r'^\d+'
    for k in range(0, 5):
        time.sleep(1)
        for i in range(1, 11):
            cmd = 'cat ' + toolLst[k] + str(i) + option
            output = CommonLib.execute_command(cmd, timeout=120)
            for line in output.splitlines():
                line = line.strip()
                res = re.search(p1, line)
                if res:
                    get_value = res.group(0)
                    if minLst[k][i-1] == '0' or maxLst[k][i-1] == '0':
                        continue
                    if int(get_value) >= int(minLst[k][i-1]) and int(get_value) <= int(maxLst[k][i-1]):
                        log.success('Check [L-ASC10-%d] get (item-%d) Voltage value is %s'%(k, i, get_value))
                    else:
                        error_count += 1
                        log.fail('Check [L-ASC10-%d] fail, get (item-%d) value is %s, expect Voltage value is %s~%s.'%(k, i, get_value, minLst[k][i-1], maxLst[k][i-1]))
    if error_count:
        raise Exception('#### Failed run read_asc10_voltage_value ####')

@logThis
def diagtool_check_all_items(tool, option):
    p1 = r'DCDC\s+test\s+:\s+(\w+)'
    cmd = './' + tool + option
    output = CommonLib.execute_command(cmd, timeout=120)
    res = re.search(p1, output)
    if res:
        get_res = res.group(1)
        if get_res == 'FAILED':
            log.fail('Check diagtool all items fail.')
            raise Exception('#### Failed run diagtool_check_all_items ####')
        elif get_res == 'Passed':
            log.success('Check diagtool all items pass.')


@logThis
def mdio_read_register_test(tool, option):
    cmd = tool + ' ' + option
    sleep_tool = 'sleep 1'
    cmdLst = [cmd, sleep_tool]
    for i in range(0, 4):
        for cmd in cmdLst:
            CommonLib.execute_command(cmd, timeout=120)

@logThis
def download_image_file_in_uboot_by_tftp(serverIp, tftpFile, unitIp=None):
    if unitIp:
        cmdLst = [unitIp, serverIp, tftpFile]
    else:
        cmdLst = [serverIp, tftpFile]
    for cmd in cmdLst:
        time.sleep(1)
        CommonLib.execute_command(cmd, timeout=200)

@logThis
def check_uboot_reset_test(cmd):
    device.sendMsg(cmd + '\r\n')
    # CommonLib.execute_command(cmd, timeout=60)
    device.read_until_regexp(KapokConst.STOP_AUTOBOOT_PROMPT, timeout=180)
    device.sendMsg(KapokConst.STOP_AUTOBOOT_KEY)


@logThis
def set_ip_address_in_uboot_environment(ethCmd, ethAddr, saveEnv, printEnv, patternDict):
    error_count = 0
    set_eth_addr_cmd = ethCmd + ' ' + ethAddr
    cmdLst = [set_eth_addr_cmd, saveEnv]
    for cmd in cmdLst:
        output = CommonLib.execute_command(cmd, timeout=120)
    if 'OK' in output:
        log.success('Set eth1 address pass.')
    else:
        error_count += 1
        log.fail('Set eth1 address fail.')
    check_print_env_test(printEnv, patternDict, Const.BOOT_MODE_UBOOT)
    if error_count:
        raise Exception('#### Failed run set_ip_address_in_uboot_environment ####')


@logThis
def check_print_env_test(tool, patternDict, mode=Const.BOOT_MODE_ONIE):
    error_count = 0
    demo_dict = {}
    output = CommonLib.execute_command(tool, mode, timeout=120)
    p1 = r'baudrate=(\d+)'
    p2 = r'eth1addr=([\w:]+)'
    p3 = r'onie_version=([\d.]+)'
    p4 = r'ethaddr=([\w:]+)'
    p5 = r'eth0\s+Link encap:Ethernet\s+HWaddr\s+([\w:]+)'
    for line in output.splitlines():
        line = line.strip()
        res1 = re.search(p1, line)
        res2 = re.search(p2, line)
        res3 = re.search(p3, line)
        res4 = re.search(p4, line)
        if res1:
            demo_dict['baudrate'] = res1.group(1)
        elif res2:
            demo_dict['eth1addr'] = res2.group(1)
        elif res3:
            demo_dict['onie_version'] = res3.group(1)
        elif res4:
            uboot_eth_addr = res4.group(1)
            if 'fw' in tool:
                eth_cmd = 'ifconfig eth0'
                output = CommonLib.execute_command(eth_cmd, mode, timeout=120)
                res5 = re.search(p5, output)
                if res5:
                    onie_eth_addr = res5.group(1).lower()
                    if uboot_eth_addr == onie_eth_addr:
                        log.success('Check eth0 addr is [%s]'%uboot_eth_addr)
                    else:
                        error_count += 1
                        log.fail('Check eth0 addr fail, ubootAddr is %s, onieAddr is %s'%(uboot_eth_addr, onie_eth_addr))
    for key, value in demo_dict.items():
        if patternDict[key] == value:
            log.success('Check %s pass, value is %s.'%(key, value))
        else:
            error_count += 1
            log.fail('Check %s fail, getValue is %s, expectValue is %s.'%(key, value, patternDict[key]))
    if error_count:
        raise Exception('#### Failed run check_print_env_test ####')


@logThis
def switch_to_onie_rescue_mode(tool, pattern):
    device.sendMsg(tool + '\r')
    device.read_until_regexp(pattern, timeout=300)
    device.sendMsg('\r')


@logThis
def add_some_test_para_in_onie_mode(tool):
    for i in range(1, 5):
        cmd = tool + ' testenv' + str(i) + ' mytestenv' + str(i)
        device.sendMsg(cmd + '\n')
        device.read_until_regexp('Proceed with update \[N\/y\]\? ', timeout=10)
        device.sendMsg("y\n")
        device.read_until_regexp("ONIE", timeout=10)


@logThis
def check_test_env_value(tool, lst):
    error_count = 0
    output = CommonLib.execute_command(tool, timeout=60)
    for pattern in lst:
        if pattern in output:
            log.success('Check test env value is %s'%pattern)
        else:
            error_count += 1
            log.fail('Do not match test env value %s.'%pattern)
    if error_count:
        raise Exception('#### Failed run check_test_env_value ####')

@logThis
def reset_to_default_environment(toolLst, envTool, patternLst):
    error_count = 0
    pass_count = 0
    for cmd in toolLst:
        if cmd == 'reset':
            check_uboot_reset_test(cmd)
            output = CommonLib.execute_command(envTool, timeout=120)
            for pattern in patternLst:
                if pattern in output:
                    error_count += 1
                    log.fail('Do not should find the key %s.'%pattern)
                else:
                    pass_count += 1
            if pass_count:
                log.success('reset default env pass.')
        else:
            device.sendMsg(cmd + '\n')
            device.read_until_regexp('OK', timeout=60)
    if error_count:
        raise Exception('#### Failed run reset_to_default_environment ####')


@logThis
def uboot_set_to_default(toolLst):
    for cmd in toolLst:
        if cmd == 'reset':
            check_uboot_reset_test(cmd)
        else:
            device.sendMsg(cmd + '\n')
            device.read_until_regexp('OK', timeout=60)


@logThis
def check_uboot_ip_addr(tool, option, pattern):
    cmd = tool + ' ' + option
    output = CommonLib.execute_command(cmd, timeout=120)
    res = re.search(pattern, output)
    if res:
        log.success('Check uboot ipaddr result is %s'%(res.group(1)))
    else:
        raise Exception('Check uboot ipaddr fail.')


@logThis
def set_dhcp_class_user_by_uboot(tool, option1, option2):
    output = ''
    cmd1 = tool + ' ' + option1
    cmd2 = tool + ' ' + option2
    cmdLst = [cmd1, cmd2, SAVE_ENV2]
    for cmd in cmdLst:
        output += CommonLib.execute_command(cmd, timeout=60)
    if 'OK' in output:
        log.success('Set dhcp user pass.')
    else:
        raise Exception('Set dhcp user fail.')


@logThis
def uboot_get_ip_address_from_dhcp():
    p1 = r'DHCP client bound to address\s+([\d.]+)\s+\(\d+ ms\)'
    output = CommonLib.execute_command('dhcp', timeout=60)
    res = re.search(p1, output)
    if res:
        get_ip = res.group(1)
        log.success('Uboot get the ip is %s'%get_ip)
    else:
        raise Exception('Uboot get ip fail.')


@logThis
def uboot_ping_dhcp_server(ipAddr):
    p1 = r'host\s+([\d.]+)\s+is\s+alive'
    cmd = 'ping ' + ipAddr
    output = CommonLib.execute_command(cmd, timeout=60)
    res = re.search(p1, output)
    if res:
        log.success('Check ping server is passed.')
    else:
        raise Exception('Check ping server is failed.')


@logThis
def read_asic_reset_value(tool, pattern):
    check_the_system_watchdog_status(tool, pattern)

@logThis
def reset_and_read_asic_switch_chip(tool, pattern):
    if ('tianhe-d04' in device.name) or ('tianhe-d05' in device.name):
        cmd = 'echo ' + pattern + ' > ' + tool
        log.info('====== Will run cmd: [%s] ======'%cmd)
        device.sendMsg(cmd+'\n')
        device.read_until_regexp(KapokConst.STOP_AUTOBOOT_PROMPT, 300)
        device.sendMsg(KapokConst.STOP_AUTOBOOT_KEY)
        device.getPrompt(Const.BOOT_MODE_DIAGOS)
    else:
        set_fan_watchdog_enable_or_disable(tool, pattern)
    check_the_system_watchdog_status(tool, interrupt_value2)

@logThis
def check_the_current_i2c_reset_status(tool, pattern):
    check_the_system_watchdog_status(tool, pattern)

@logThis
def reset_and_read_i2c_test(tool, pattern):
    set_fan_watchdog_enable_or_disable(tool, pattern)
    check_the_system_watchdog_status(tool, interrupt_value2)

@logThis
def set_and_read_the_fan_board_eeprom_proect(tool, pattern):
    set_fan_watchdog_enable_or_disable(tool, pattern)
    check_the_system_watchdog_status(tool, pattern)

@logThis
def read_fan_board_eeprom(tool, pattern):
    pass_count = 0
    cmd = 'cat ' + tool
    output = CommonLib.execute_command(cmd, timeout=120)
    for line in output.splitlines():
        line = line.strip()
        if pattern == '0':
            res = re.search('\|\.{15}C\|', line)
        elif pattern == '1':
            res = re.search('\|1234\.{11}C\|', line)
        if res:
            pass_count += 1
            log.success('Check fan board eeprom data pass.')
    if pass_count == 0:
        raise Exception('Check fan board eeprom data fail.')

@logThis
def read_busbar_board_eeprom(tool, option, pattern):
    pass_count = 0
    cmd = tool + ' -C ' + option
    output = CommonLib.execute_command(cmd, timeout=120)
    for line in output.splitlines():
        line = line.strip()
        if pattern == '0':
            res = re.search('\|\..*C\|', line)
        elif pattern == '1':
            res = re.search('\|1234\..*C\|', line)
        if res:
            pass_count += 1
            log.success('Check fan board eeprom data pass.')
    if pass_count == 0:
        raise Exception('Check fan board eeprom data fail.')

@logThis
def restore_origianl_data_eeprom(tool):
    cmd = "echo -n -e '\\x01\\x00\\x00\\x01\\x00\\x00' > " + tool
    log.info('#### %s ####' % cmd)
    CommonLib.execute_command(cmd, timeout=60)

@logThis
def write_some_data_into_fan_eeprom(tool, pattern1):
    cmd = 'echo ' + pattern1 + ' > ' + tool
    CommonLib.execute_command(cmd, timeout=120)

@logThis
def read_fan_module_eeprom(tool, pattern):
    pass_count = 0
    cmd = 'cat /sys/bus/i2c/drivers/at24/' + tool + '/eeprom | hexdump -C'
    output = CommonLib.execute_command(cmd, timeout=120)
    for line in output.splitlines():
        line = line.strip()
        if pattern == '0':
            res = re.search('\|\..*C\|', line)
        elif pattern == '1':
            res = re.search('\|1234\..*C\|', line)
        if res:
            pass_count += 1
            log.success('Check fan board eeprom data pass.')
    if pass_count == 0:
        raise Exception('Check fan board eeprom data fail.')

@logThis
def write_some_data_to_fan_module_eeprom(tool, pattern):
    cmd = 'echo ' + pattern + ' > /sys/bus/i2c/drivers/at24/' + tool + '/eeprom'
    CommonLib.execute_command(cmd, timeout=120)

@logThis
def restore_fan_module_eeprom_data(tool):
    cmd = "echo -n -e '\\x01\\x00\\x00\\x01\\x08\\x00' > /sys/bus/i2c/drivers/at24/" + tool + "/eeprom"
    log.info('#### %s ####' % cmd)
    CommonLib.execute_command(cmd, timeout=60)

@logThis
def check_come_write_protect(tool, pattern):
    pass_count = 0
    p1 = r'^\d+'
    cmd = 'cat ' + tool
    output = CommonLib.execute_command(cmd, timeout=60)
    for line in output.splitlines():
        line = line.strip()
        res = re.search(p1, line)
        if res:
            get_value = res.group(0)
            if get_value == '1':
                log.info('Default write protect is enable, need to set disable.')
                set_fan_watchdog_enable_or_disable(tool, pattern)
            elif get_value == pattern:
                pass_count += 1
                log.success('Default write protect is [%s] disable status.'%get_value)
    if pass_count == 0:
        raise Exception('Failed run check_come_write_protect.')

@logThis
def read_come_card_eeprom(tool, option, pattern):
    read_switch_board_eeprom_test(tool, option, pattern)

@logThis
def restore_come_card_original_data(tool):
    cmd = "echo -n -e '\\x54\\x6c\\x76\\x49\\x6e\\x66' > " + tool
    log.info('#### %s ####' % cmd)
    CommonLib.execute_command(cmd, timeout=60)

@logThis
def enable_or_disable_come_card_write_protect(tool, pattern):
    set_fan_watchdog_enable_or_disable(tool, pattern)

@logThis
def read_riser_board_eerpom_test(tool, option, pattern):
    read_busbar_board_eeprom(tool, option, pattern)

@logThis
def write_some_data_to_riser_board_eeprom(tool, pattern):
    write_some_data_into_fan_eeprom(tool, pattern)

@logThis
def read_fan_eeprom_power_status(tool, pattern):
    check_the_system_watchdog_status(tool, pattern)

@logThis
def set_the_fan_eeprom_power_enable_or_disable(tool, pattern):
    set_fan_watchdog_enable_or_disable(tool, pattern)

@logThis
def read_fan_mux_reset_value(tool, pattern):
    check_the_system_watchdog_status(tool, pattern)

@logThis
def reset_fan_mux_status(tool, pattern):
    set_fan_watchdog_enable_or_disable(tool, pattern)

@logThis
def read_cpld_raw_access_test(addrTool, dataTool, addrPattern, dataPattern):
    check_the_system_watchdog_status(addrTool, addrPattern)
    check_the_system_watchdog_status(dataTool, dataPattern)

@logThis
def write_cpld_raw_access_test(addrTool, dataTool, pattern1, pattern2):
    cmd1 = 'echo ' + pattern1 + ' > ' + addrTool
    cmd2 = 'echo "' + pattern1 + ' ' + pattern2 + '" > ' + dataTool
    cmdLst = [cmd1, cmd2]
    for cmd in cmdLst:
        time.sleep(1)
        CommonLib.execute_command(cmd, timeout=120)

@logThis
def restore_to_default_cpld_raw_value():
    write_cpld_raw_access_test(CPLD2_RAW_ADDR, CPLD2_RAW_DATA, CPLD2_RAW_PATTERN1, CPLD2_RAW_PATTERN2)
    time.sleep(1)
    write_cpld_raw_access_test(CPLD3_RAW_ADDR, CPLD3_RAW_DATA, CPLD2_RAW_PATTERN1, CPLD3_RAW_PATTERN1)
    time.sleep(1)
    read_cpld_raw_access_test(CPLD2_RAW_ADDR, CPLD2_RAW_DATA, CPLD2_RAW_PATTERN1, CPLD2_RAW_PATTERN2)
    time.sleep(1)
    read_cpld_raw_access_test(CPLD3_RAW_ADDR, CPLD3_RAW_DATA, CPLD2_RAW_PATTERN1, CPLD3_RAW_PATTERN1)

@logThis
def check_cpld_led_enable_status(cpld2Tool, cpld3Tool, pattern):
    check_the_system_watchdog_status(cpld2Tool, pattern)
    time.sleep(1)
    check_the_system_watchdog_status(cpld3Tool, pattern)

@logThis
def set_cpld_led_enable_test(cpld2Tool, cpld3Tool, pattern):
    set_fan_watchdog_enable_or_disable(cpld2Tool, pattern)
    time.sleep(1)
    set_fan_watchdog_enable_or_disable(cpld3Tool, pattern)

@logThis
def restore_to_default_cpld_led_value(cpld2Tool, cpld3Tool, pattern):
    set_cpld_led_enable_test(cpld2Tool, cpld3Tool, pattern)
    time.sleep(1)
    check_cpld_led_enable_status(cpld2Tool, cpld3Tool, pattern)

@logThis
def check_port_led_status(cpld2Tool, cpld3Tool, pattern):
    error_count = 0
    toolLst = [cpld2Tool, cpld3Tool]
    for tool in toolLst:
        cmd = 'cat ' + tool
        output = CommonLib.execute_command(cmd, timeout=60)
        if pattern in output:
            log.success('Get the led status is %s'%pattern)
        else:
            error_count += 1
            log.fail('Do not match [%s] the value'%pattern)
    if error_count:
        raise Exception('Run fail check_port_led_status.')

@logThis
def set_and_read_port_led_color(cpld2Tool, cpld3Tool, pattern):
    error_count = 0
    toolLst = [cpld2Tool, cpld3Tool]
    for tool in toolLst:
        cmd = 'echo ' + pattern + ' > ' + tool
        CommonLib.execute_command(cmd, timeout=60)
        time.sleep(1)
        readCmd = 'cat ' + tool
        output = CommonLib.execute_command(readCmd, timeout=60)
        if pattern in output:
            log.success('Get the led status is %s'%pattern)
        else:
            error_count += 1
            log.fail('Do not match [%s] the value'%pattern)
    if error_count:
        raise Exception('Run fail set_and_read_port_led_color.')

@logThis
def read_voltage_value_test(tool, lm75Addr, HWOption, optionLst):
    pass_count = 0
    p1 = '^\d+'
    for i in range(0, len(optionLst)):
        cmd = 'cat ' + tool + lm75Addr + '/hwmon/' + HWOption + '/' + optionLst[i]
        output = CommonLib.execute_command(cmd, timeout=60)
        for line in output.splitlines():
            line = line.strip()
            res = re.search(p1, line)
            if res:
                pass_count += 1
                if i == 0:
                    temp_input = res.group(0)
                elif i == 1:
                    temp_max = res.group(0)
                elif i == 2:
                    temp_phy = res.group(0)
    if (pass_count == 3) and (temp_max > temp_input) and (temp_max > temp_phy):
        log.success('Check the LM75 temperature sensor pass.')
    else:
        raise Exception('Failed check LM75 sensor voltage, temp_input:%s, temp_max:%s, temp_phy:%s'%(temp_input, temp_max, temp_phy))

@logThis
def read_left_side_of_the_switch_board_tas_voltage(tool, lm75Addr, HWOption, optionLst):
    read_voltage_value_test(tool, lm75Addr, HWOption, optionLst)

@logThis
def read_left_side_of_the_switch_board_bas_voltage(tool, lm75Addr, HWOption, optionLst):
    read_voltage_value_test(tool, lm75Addr, HWOption, optionLst)

@logThis
def read_right_side_of_the_switch_board_tas_voltage(tool, lm75Addr, HWOption, optionLst):
    read_voltage_value_test(tool, lm75Addr, HWOption, optionLst)

@logThis
def read_middle_side_of_the_switch_board_tas_voltage(tool, lm75Addr, HWOption, optionLst):
    read_voltage_value_test(tool, lm75Addr, HWOption, optionLst)

@logThis
def read_right_side_of_the_switch_board_bas_voltage(tool, lm75Addr, HWOption, optionLst):
    read_voltage_value_test(tool, lm75Addr, HWOption, optionLst)

@logThis
def read_middle_side_of_fan_board_voltage(tool, lm75Addr, HWOption, optionLst):
    read_voltage_value_test(tool, lm75Addr, HWOption, optionLst)

@logThis
def read_right_side_of_fan_board_voltage(tool, lm75Addr, HWOption, optionLst):
    read_voltage_value_test(tool, lm75Addr, HWOption, optionLst)

@logThis
def read_left_side_of_fan_board_voltage(tool, lm75Addr, HWOption, optionLst):
    read_voltage_value_test(tool, lm75Addr, HWOption, optionLst)

@logThis
def read_sa5604_temperature_info(tool, lm90Addr, HWOption, optionLst):
    pass_count = 0
    # p1 = '^\d+$'
    p1 = r'^\d+$|vin|vout\d|iout1|iin|pin|pout1|^-\d+$|pout2|iout2'
    for i in range(0, len(optionLst)):
        cmd = 'cat ' + tool + '/' + lm90Addr + '/hwmon/' + HWOption + '/' + optionLst[i]
        output = CommonLib.execute_command(cmd, timeout=60)
        for line in output.splitlines():
            line = line.strip()
            res = re.search(p1, line)
            if res:
                pass_count += 1
                getVal = res.group(0)
                log.success('Get the temperature value is %s'%getVal)
    if pass_count != len(optionLst):
        raise Exception('Do not match temperature value, getValue: %d, expectValue: %d'%(pass_count, len(optionLst)))

@logThis
def read_ltc4282_voltage_test(tool, ltcAddr, HWOption, optionLst):
    read_sa5604_temperature_info(tool, ltcAddr, HWOption, optionLst)

@logThis
def check_tps53679_driver_value_test(tool, tpsAddr, HWOption, optionLst):
    read_sa5604_temperature_info(tool, tpsAddr, HWOption, optionLst)

@logThis
def check_come_cpld_version(tool, pattern):
    check_the_system_watchdog_status(tool, pattern)

@logThis
def check_page_select_value(tool, option, pattern):
    pass_count = 0
    p1 = r'^0x\w+|^(0x)?\d+'
    cmd = 'cat ' + tool
    output = CommonLib.execute_command(cmd, timeout=120)
    for line in output.splitlines():
        line = line.strip()
        res = re.search(p1, line)
        if res:
            pass_count += 1
            get_value = res.group(0)
            if get_value == '0x00':
                set_fan_watchdog_enable_or_disable(tool, option)
                check_the_system_watchdog_status(tool, pattern)
            elif get_value == pattern:
                log.success('Get the page_select value is %s'%pattern)
            else:
                log.fail('Do not find the page_select value.')
    if pass_count == 0:
        raise Exception('Failed run check_page_select_value.')

@logThis
def read_access_sysfs_note_test(AddrTool, DataTool, pattern):
    check_the_system_watchdog_status(AddrTool, pattern)
    check_the_system_watchdog_status(DataTool, pattern)

@logThis
def write_access_sysfs_note_test(AddrTool, DataTool, pattern1, pattern2):
    write_cpld_raw_access_test(AddrTool, DataTool, pattern1, pattern2)

@logThis
def read_access_sysfs_note_test_again(AddrTool, DataTool, pattern1, pattern2):
    check_the_system_watchdog_status(AddrTool, pattern1)
    check_the_system_watchdog_status(DataTool, pattern2)

@logThis
def restore_to_default_come_cpld_raw_value(PageTool, AddrTool, DataTool, pattern):
    set_fan_watchdog_enable_or_disable(PageTool, interrupt_value2)
    check_the_system_watchdog_status(PageTool, pattern)
    cmd1 = 'echo ' + pattern + ' > ' + AddrTool
    cmd2 = 'echo "' + pattern + ' ' + pattern + '" > ' + DataTool
    cmdLst = [cmd1, cmd2]
    for cmd in cmdLst:
        time.sleep(1)
        CommonLib.execute_command(cmd, timeout=120)
    time.sleep(1)
    read_access_sysfs_note_test(AddrTool, DataTool, pattern)

@logThis
def read_hreset_value(tool, pattern):
    check_the_system_watchdog_status(tool, pattern)

@logThis
def write_hreset_value_test(tool, pattern):
    #set_fan_watchdog_enable_or_disable(tool, pattern)
    write_poreset_value_test(tool, pattern)

@logThis
def restore_to_default_hreset_value(tool, pattern):
    set_fan_watchdog_enable_or_disable(tool, pattern)
    time.sleep(1)
    check_the_system_watchdog_status(tool, pattern)

@logThis
def read_mcp3422_voltage_value(tool):
    p1 = r'error|fail'
    cmd = 'cat ' + tool
    output = CommonLib.execute_command(cmd, timeout=120)
    if re.search(p1, output):
        raise Exception('Find error or fail info.')
    else:
        log.success('Read MCP3422 info pass!')

@logThis
def check_the_i2cfpga_card_present_status(tool, pattern):
    check_the_system_watchdog_status(tool, pattern)

@logThis
def check_i2c_fpga_card_eeprom_write_protect_status(tool, pattern):
    check_the_system_watchdog_status(tool, pattern)

@logThis
def set_the_i2c_fpga_card_eeprom_write_protect(tool, pattern):
    set_fan_watchdog_enable_or_disable(tool, pattern)

@logThis
def write_data_to_i2c_fpga_card_eeprom(tool, pattern1):
    error_count = 0
    p1 = '/bin/sh: can\'t create.*nonexistent directory'
    p2 = 'No such file or directory'
    cmd = 'echo ' + pattern1 + ' > ' + tool
    output = CommonLib.execute_command(cmd, timeout=120)
    if re.search(p1, output):
        log.info('Can not write data to eeprom.')
    else:
        error_count += 1
        log.fail('Can write some data to eeprom.')
    cmd2 = 'hexdump -C ' + tool
    output = CommonLib.execute_command(cmd2, timeout=120)
    if re.search(p2, output):
        log.info('Can not hexdump data')
    else:
        error_count += 1
        log.fail('Can hexdump some data.')
    if error_count:
        raise Exception('Run fail write_data_to_i2c_fpga_card_eeprom.')

@logThis
def check_the_lm75_interrupt_status(tool, pattern):
    check_the_system_watchdog_status(tool, pattern)

@logThis
def get_swImage_version(ImageType):
    imageObj = CommonLib.get_swinfo_dict(ImageType)
    new_version = imageObj.get("newVersion", "NotFound")
    return new_version

@logThis
def check_1pps_fpga_version(tool, imageType):
    pass_count = 0
    error_count = 0
    expect_version = get_swImage_version(imageType)
    p1 = r'^0x\w+|^(0x)?\d+'
    cmd = 'cat ' + tool
    output = CommonLib.execute_command(cmd, timeout=120)
    for line in output.splitlines():
        line = line.strip()
        res = re.search(p1, line)
        if res:
            pass_count += 1
            getVer = res.group(0)
            if getVer == expect_version:
                log.success('Check 1pps fpga version pass, getVer: %s, ExpectVer: %s.'%(getVer, expect_version))
            else:
                error_count += 1
                log.fail('Compare version is diff, getVer: %s, ExpectVer: %s.'%(getVer, expect_version))
    if pass_count == 1 and error_count == 0:
        log.success('Check 1pps fpga version is passed!')
    else:
        raise Exception('Run fail check_1pps_fpga_version.')

@logThis
def read_i2c_raw_access_test(dataTool, addrTool, dataPattern, addrPattern):
    check_the_system_watchdog_status(dataTool, dataPattern)
    check_the_system_watchdog_status(addrTool, addrPattern)

@logThis
def write_i2c_raw_access_test(dataTool, addrTool, pattern1, pattern2):
    cmd1 = 'echo "' + pattern1 + ' ' + pattern2 + '" > ' + dataTool
    cmd2 = 'echo ' + pattern1 + ' > ' + addrTool
    cmdLst = [cmd1, cmd2]
    for cmd in cmdLst:
        time.sleep(1)
        CommonLib.execute_command(cmd, timeout=120)

@logThis
def restore_to_default_i2c_raw_value():
    write_i2c_raw_access_test(I2C_RAW_ACCESS_DATA, I2C_RAW_ACCESS_ADDR, I2C_RAW_PATTERN2, I2C_RAW_PATTERN1)
    time.sleep(1)
    read_i2c_raw_access_test(I2C_RAW_ACCESS_DATA, I2C_RAW_ACCESS_ADDR, I2C_RAW_PATTERN1, I2C_RAW_PATTERN2)

@logThis
def read_i2c_scratch_test(tool, pattern):
    check_the_system_watchdog_status(tool, pattern)

@logThis
def write_i2c_scratch_test(tool, pattern):
    set_fan_watchdog_enable_or_disable(tool, pattern)

@logThis
def restore_to_default_i2c_scratch_value(tool, pattern):
    set_fan_watchdog_enable_or_disable(tool, pattern)
    time.sleep(1)
    check_the_system_watchdog_status(tool, pattern)

@logThis
def read_the_current_profile_select(tool, option, pattern):
    pass_count = 0
    error_count = 0
    p1 = r'^\d+'
    for i in range(1, 33):
        cmd = 'cat ' + tool + str(i) + option
        output = CommonLib.execute_command(cmd, timeout=120)
        for line in output.splitlines():
            line = line.strip()
            res = re.search(p1, line)
            if res:
                pass_count += 1
                get_value = res.group(0)
                if get_value == pattern:
                    log.success('Check port-%d profile value is %s' % (i, get_value))
                else:
                    error_count += 1
                    log.fail('Check port-%d profile fail, get value is %s, expect value is %s' % (i, get_value, pattern))
    if error_count or pass_count == 0:
        raise Exception('Failed run read_the_current_profile_select.')

@logThis
def set_the_profile_select(tool, option, pattern):
    for i in range(1, 33):
        cmd = 'echo ' + pattern + ' > ' + tool + str(i) + option
        CommonLib.execute_command(cmd, timeout=120)

@logThis
def restore_to_default_i2c_profile_select_value(tool, option, pattern):
    set_the_profile_select(tool, option, pattern)
    time.sleep(2)
    read_the_current_profile_select(tool, option, pattern)

@logThis
def set_the_profile_speed(tool, option1, option2, pattern):
    for i in range(1, 33):
        for k in range(1, 3):
            cmd = 'echo "' + pattern + '" > ' + tool + str(i) + option1 + str(k) + option2
            CommonLib.execute_command(cmd, timeout=120)

@logThis
def read_the_profile_speed(tool, option1, option2, pattern):
    pass_count = 0
    error_count = 0
    p1 = r'^\d+'
    for i in range(1, 33):
        for k in range(1, 3):
            cmd = 'cat ' + tool + str(i) + option1 + str(k) + option2
            output = CommonLib.execute_command(cmd, timeout=120)
            for line in output.splitlines():
                line = line.strip()
                res = re.search(p1, line)
                if res:
                    pass_count += 1
                    get_value = res.group(0)
                    if get_value == pattern:
                        log.success('Check port-%d profile speed value is %s' % (i, get_value))
                    else:
                        error_count += 1
                        log.fail(
                            'Check port-%d profile speed fail, get value is %s, expect value is %s' % (i, get_value, pattern))
    if error_count or pass_count == 0:
        raise Exception('Failed run read_the_profile_speed.')

@logThis
def set_the_i2c_clock_speed(tool, option, pattern):
    set_the_profile_select(tool, option, pattern)

@logThis
def read_the_i2c_master_reset_test(tool, option, pattern):
    read_the_current_profile_select(tool, option, pattern)

@logThis
def set_the_i2c_master_reset_test(tool, option, pattern):
    set_the_profile_select(tool, option, pattern)

@logThis
def read_the_port_interrupt_mask_test(tool, option, pattern):
    read_the_current_profile_select(tool, option, pattern)

@logThis
def set_the_port_interrupt_mask_test(tool, option, pattern):
    set_the_profile_select(tool, option, pattern)

@logThis
def restore_to_default_port_interrupt_mask_test(tool, option, pattern):
    set_the_profile_select(tool, option, pattern)
    time.sleep(2)
    read_the_current_profile_select(tool, option, pattern)

@logThis
def read_the_port_lpmod_test(tool, option, pattern):
    read_the_current_profile_select(tool, option, pattern)

@logThis
def set_the_port_lpmod_test(tool, option, pattern):
    set_the_profile_select(tool, option, pattern)

@logThis
def restore_to_default_port_lpmod_test(tool, option, pattern):
    set_the_profile_select(tool, option, pattern)
    time.sleep(2)
    read_the_current_profile_select(tool, option, pattern)

@logThis
def get_asc_verison(imageName):
    newVerObj = get_swImage_version(imageName)
    asc10_0_Ver = newVerObj.get('ASC10-0', "NotFound")
    asc10_1_Ver = newVerObj.get('ASC10-1', "NotFound")
    asc10_2_Ver = newVerObj.get('ASC10-2', "NotFound")
    asc10_3_Ver = newVerObj.get('ASC10-3', "NotFound")
    asc10_4_Ver = newVerObj.get('ASC10-4', "NotFound")
    asc10Lst = [asc10_0_Ver, asc10_1_Ver, asc10_2_Ver, asc10_3_Ver, asc10_4_Ver]
    return asc10Lst

@logThis
def check_asc10_eeprom_and_crc_test(toolLst, eepromLst, crcLst):
    pass_count = 0
    error_count = 0
    p1 = 'CRC:\s+(\w+)'
    p2 = r'^(f|\d)\w+(\d|f)$'
    tempLst = []
    expect_ver_lst = get_asc_verison('1PPS_ASC')
    for i in range(0, len(toolLst)):
        log.info('############# Step1: Check ASC10 FW Test #############')
        cmd = toolLst[i]
        output = CommonLib.execute_command(cmd, timeout=120)
        for line in output.splitlines():
            line = line.strip()
            res = re.search(p1, line)
            res1 = re.search(p2, line)
            if res1:
                pass_count += 1
                tempLst.append(res1.group(0))
            if res:
                pass_count += 1
                get_ver = res.group(1)
                if get_ver == expect_ver_lst[i]:
                    log.success('Check ASC10-%d version pass, getVer:%s, expectVer:%s.'%(i, get_ver, expect_ver_lst[i]))
                else:
                    error_count += 1
                    log.fail('Check ASC10-%d version fail, getVer:%s, expectVer:%s.'%(i, get_ver, expect_ver_lst[i]))
        log.info('############# Step2: Check ASC10 EEPROM Test #############')
        output1 = CommonLib.execute_command(eepromLst[i], timeout=120)
        for str1 in tempLst:
            new_str = ''
            for k in range(0, len(str1), 2):
                new_str += str1[k:k + 2] + ' '
            if new_str in output1:
                log.success('Get the same eeprom result [%s]'%new_str)
            else:
                error_count += 1
                log.fail('Do not find eeprom:[%s] value.'%new_str)
        tempLst = []
        log.info('############# Step3: Check ASC10 CRC Version Test #############')
        CRC_CMD = 'cat ' + crcLst[i]
        output2 = CommonLib.execute_command(CRC_CMD, timeout=120)
        if expect_ver_lst[i] in output2:
            log.success('Check ASC10-%d CRC version pass, getVer is %s'%(i, expect_ver_lst[i]))
        else:
            error_count += 1
            log.fail('Do not match ASC10-%d CRC version, expectVer is %s.'%(i, expect_ver_lst[i]))
    if error_count or pass_count == 0:
        raise Exception('Failed run check_asc10_fw_test.')


@logThis
def check_the_type_of_connector(tool, option, pattern, caseType):
    error_count = 0
    for i in range(101, 133):
        cmd = 'cat ' + tool + str(i) + '-0050/' + option
        output = CommonLib.execute_command(cmd, timeout=120)
        if pattern in output:
            log.success('Check Port_%s %s pass, the value is [ %s ].'%(str(i) + '-0050', caseType, pattern))
        else:
            error_count += 1
            log.fail('Check Port_%s %s fail, expect value is [ %s ].'%(str(i) + '-0050', caseType, pattern))
    if error_count:
        raise Exception('Failed run check_the_type_of_connector.')

@logThis
def check_raw_eeprom_on_the_lower_128_bytes(tool, option, pattern, caseType):
    check_the_type_of_connector(tool, option, pattern, caseType)

@logThis
def check_raw_eeprom_on_the_upper_128_bytes(tool, option, pattern, caseType):
    check_the_type_of_connector(tool, option, pattern, caseType)

@logThis
def read_visible_page_number(tool, option, pattern, caseType):
    error_count = 0
    pass_count = 0
    p1 = '^\d+'
    for i in range(101, 133):
        cmd = 'cat ' + tool + str(i) + '-0050/' + option
        output = CommonLib.execute_command(cmd, timeout=120)
        for line in output.splitlines():
            line = line.strip()
            res = re.search(p1, line)
            if res:
                pass_count += 1
                get_value = res.group(0)
                if get_value == pattern:
                    log.success('Check %s pass, value is %s'%(caseType, get_value))
                else:
                    error_count += 1
                    log.fail('Check %s fail, Get value is %s, Expect value is %s'%(caseType, get_value, pattern))
    if error_count or pass_count == 0:
        raise Exception('Failed run read_visible_page_number.')

@logThis
def set_visible_page_number(tool, option, pattern):
    error_count = 0
    for i in range(101, 133):
        cmd = 'echo ' + pattern + ' > ' + tool + str(i) + '-0050/' + option
        output = CommonLib.execute_command(cmd, timeout=120)
        if 'Permission denied' in output:
            error_count += 1
            log.fail('Run cmd [%s] fail.'%cmd)
    if error_count:
        raise Exception('Failed run set_visible_page_number.')

@logThis
def restore_to_default_visible_page_number_test(tool, option, pattern, caseType):
    set_visible_page_number(tool, option, pattern)
    time.sleep(2)
    read_visible_page_number(tool, option, pattern, caseType)

@logThis
def read_eeprom_valid_test(tool, option, pattern, caseType):
    read_visible_page_number(tool, option, pattern, caseType)

@logThis
def read_high_power_class_enable(tool, option, pattern, caseType):
    read_visible_page_number(tool, option, pattern, caseType)

@logThis
def set_high_power_class_enable(tool, option, pattern):
    set_visible_page_number(tool, option, pattern)

@logThis
def read_in1_highest_test(tool, option, pattern, caseType):
    read_visible_page_number(tool, option, pattern, caseType)

@logThis
def read_in1_input_test(tool, option, pattern, caseType):
    read_visible_page_number(tool, option, pattern, caseType)

@logThis
def read_in1_lowest_test(tool, option, pattern, caseType):
    read_visible_page_number(tool, option, pattern, caseType)

@logThis
def read_in1_max_test(tool, option, pattern, caseType):
    read_visible_page_number(tool, option, pattern, caseType)

@logThis
def read_in1_min_test(tool, option, pattern, caseType):
    read_visible_page_number(tool, option, pattern, caseType)

@logThis
def set_in1_reset_history_test(tool, option, pattern):
    set_visible_page_number(tool, option, pattern)

@logThis
def read_lane_ctle_test(tool, option, pattern1, pattern2, caseType):
    error_count = 0
    pass_count = 0
    #p1 = '(^\d+|[\d.]+)'
    p1 = '^\d+\.?\d?'
    for i in range(101, 133):
        cmd = 'cat ' + tool + str(i) + '-0050/' + option
        output = CommonLib.execute_command(cmd, timeout=120)
        for line in output.splitlines():
            line = line.strip()
            res = re.search(p1, line)
            if res:
                pass_count += 1
                get_value = res.group(0)
                if caseType == 'Powerclass':
                    if (float(get_value) >= float(pattern1)) and (float(get_value) <= float(pattern2)):
                        log.success('Check Port_%s %s pass, get value is %s' % (str(i) + '-0050', caseType, get_value))
                    else:
                        error_count += 1
                        log.fail('Check Port_%s %s fail, get value is %s, it\'s not between %s and %s.' % (str(i) + '-0050', caseType, get_value, pattern1, pattern2))
                else:
                    if (int(get_value) >= int(pattern1)) and (int(get_value) <= int(pattern2)):
                        log.success('Check Port_%s %s pass, get value is %s'%(str(i) + '-0050', caseType, get_value))
                    else:
                        error_count += 1
                        log.fail('Check Port_%s %s fail, get value is %s, it\'s not between %s and %s.'%(str(i) + '-0050', caseType, get_value, pattern1, patter2))
    if error_count or pass_count == 0:
        raise Exception('Failed run read_lane_ctle_test.')


@logThis
def read_lane_rx_and_tx_los_test(tool, option, caseType):
    pass_count = 0
    error_count = 0
    p1 = '^\d+'
    for i in range(101, 133):
        for k in range(1, 9):
            cmd = 'cat ' + tool + str(i) + '-0050/lane' + str(k) + option
            output = CommonLib.execute_command(cmd, timeout=120)
            for line in output.splitlines():
                line = line.strip()
                res = re.search(p1, line)
                if res:
                    pass_count += 1
                    get_value = res.group(0)
                    if (int(get_value) == 0) or (int(get_value) == 1):
                        log.success('Check Port_%s/lane%d %s pass, get value is %s'%(str(i) + '-0050', k, caseType, get_value))
                    else:
                        error_count += 1
                        log.fail('Check Port_%s/lane%d %s fail, get value is %s'%(str(i) + '-0050', k, caseType, get_value))
    if error_count or pass_count == 0:
        raise Exception('Failed run read_lane_rx_and_tx_los_test.')

@logThis
def read_lane_rx_and_tx_power_highest_test(tool, option, caseType):
    pass_count = 0
    error_count = 0
    p1 = '^\d+'
    for i in range(101, 133):
        for k in range(1, 9):
            cmd = 'cat ' + tool + str(i) + '-0050/lane' + str(k) + option
            output = CommonLib.execute_command(cmd, timeout=120)
            for line in output.splitlines():
                line = line.strip()
                res = re.search(p1, line)
                if res:
                    pass_count += 1
                    get_value = res.group(0)
                    if (int(get_value) > 0) and (int(get_value) < 65535):
                        log.success('Check Port_%s/lane%d rx or tx power %s pass, get value is %s'%(str(i) + '-0050', k, caseType, get_value))
                    else:
                        error_count += 1
                        log.fail('Check Port_%s/lane%d rx or tx power %s fail, get value is %s' % (str(i) + '-0050', k, caseType, get_value))
    if error_count or pass_count == 0:
        raise Exception('Failed run read_lane_rx_and_tx_power_highest_test.')

@logThis
def read_lane_rx_and_tx_power_input_test(tool, option, caseType):
    read_lane_rx_and_tx_power_highest_test(tool, option, caseType)

@logThis
def read_lane_rx_and_tx_power_lowest_test(tool, option, caseType):
    read_lane_rx_and_tx_power_highest_test(tool, option, caseType)

@logThis
def check_the_cable_assembly_length(tool, option, pattern, caseType):
    read_visible_page_number(tool, option, pattern, caseType)

@logThis
def check_the_port_medium_type(tool, option, pattern, caseType):
    check_the_type_of_connector(tool, option, pattern, caseType)

@logThis
def check_the_port_module_type(tool, option, pattern, caseType):
    check_the_type_of_connector(tool, option, pattern, caseType)

@logThis
def check_the_wavelength(tool, option, pattern1, pattern2, caseType):
    read_lane_ctle_test(tool, option, pattern1, pattern2, caseType)

@logThis
def check_the_port_num_test(tool, option):
    error_count = 0
    pass_count = 0
    p1 = '^\d+'
    for i in range(101, 133):
        k = i - 100
        cmd = 'cat ' + tool + str(i) + '-0050/' + option
        output = CommonLib.execute_command(cmd, timeout=120)
        for line in output.splitlines():
            line = line.strip()
            res = re.search(p1, line)
            if res:
                pass_count += 1
                get_value = res.group(0)
                if int(get_value) == k:
                    log.success('Check Port-%s port_num pass, value is %s' % (str(i) + '-0050', get_value))
                else:
                    error_count += 1
                    log.fail('Check Port-%s port_num fail, Get value is %s, Expect value is %s' % (str(i) + '-0050', get_value, k))
    if error_count or pass_count == 0:
        raise Exception('Failed run check_the_port_num_test.')

@logThis
def check_power_override_test(tool, option, pattern, caseType):
    read_visible_page_number(tool, option, pattern, caseType)

@logThis
def set_power_override_test(tool, option, pattern):
    set_visible_page_number(tool, option, pattern)

@logThis
def check_power_set_test(tool, option, pattern, caseType):
    read_visible_page_number(tool, option, pattern, caseType)

@logThis
def set_power_set_test(tool, option, pattern):
    set_visible_page_number(tool, option, pattern)

@logThis
def check_the_power_class(tool, option, pattern1, pattern2, caseType):
    read_lane_ctle_test(tool, option, pattern1, pattern2, caseType)

@logThis
def check_the_temp1_higest_test(tool, option, pattern, caseType):
    error_count = 0
    pass_count = 0
    p1 = '^\d+'
    for i in range(101, 133):
        cmd = 'cat ' + tool + str(i) + '-0050/' + option
        output = CommonLib.execute_command(cmd, timeout=120)
        for line in output.splitlines():
            line = line.strip()
            res = re.search(p1, line)
            if res:
                pass_count += 1
                get_value = res.group(0)
                if int(get_value) > int(pattern):
                    log.success('Check Port_%s %s pass, value is %s'%(str(i)+ '-0050', caseType, get_value))
                else:
                    error_count += 1
                    log.fail('Check Port_%s %s fail, value is %s'%(str(i)+ '-0050', caseType, get_value))
    if error_count or pass_count == 0:
        raise Exception('Failed run check_the_temp1_higest_test.')

@logThis
def check_the_temp1_input_test(tool, option, pattern, caseType):
    check_the_temp1_higest_test(tool, option, pattern, caseType)

@logThis
def check_the_temp1_label_test(tool, option):
    error_count = 0
    pass_count = 0
    p1 = 'module\d+Temperature'
    for i in range(101, 133):
        k = i - 100
        expect_value = 'module' + str(k) + 'Temperature'
        cmd = 'cat ' + tool + str(i) + '-0050/' + option
        output = CommonLib.execute_command(cmd, timeout=120)
        for line in output.splitlines():
            line = line.strip()
            res = re.search(p1, line)
            if res:
                pass_count += 1
                get_value = res.group(0)
                if get_value == expect_value:
                    log.success('Check Port-%s temp1 label pass, value is %s' % (str(i) + '-0050', get_value))
                else:
                    error_count += 1
                    log.fail('Check Port-%s temp1 label fail, Get value is %s, Expect value is %s' % (str(i) + '-0050', get_value, expect_value))
    if error_count or pass_count == 0:
        raise Exception('Failed run check_the_port_num_test.')

@logThis
def check_the_temp1_lowest_test(tool, option, pattern, caseType):
    check_the_temp1_higest_test(tool, option, pattern, caseType)

@logThis
def set_the_temp1_reset_history_test(tool, option, pattern):
    set_visible_page_number(tool, option, pattern)

@logThis
def read_vendor_name_test(tool, option, pattern, caseType):
    check_the_type_of_connector(tool, option, pattern, caseType)

@logThis
def read_vendor_part_num_test(tool, option, pattern, caseType):
    check_the_type_of_connector(tool, option, pattern, caseType)

@logThis
def read_vendor_revision_num_test(tool, option, pattern, caseType):
    check_the_type_of_connector(tool, option, pattern, caseType)

@logThis
def read_vendor_serial_num_test(tool, option):
    p1 = r'^AL\d+'
    error_count = 0
    pass_count = 0
    for i in range(101, 133):
        cmd = 'cat ' + tool + str(i) + '-0050/' + option
        output = CommonLib.execute_command(cmd, timeout=120)
        for line in output.splitlines():
            line = line.strip()
            res = re.search(p1, line)
            if res:
                pass_count += 1
                get_value = res.group(0)
                if get_value:
                    log.success('Check Port-%s vendor serial num pass, value is %s'%(str(i)+ '-0050', get_value))
                else:
                    error_count += 1
                    log.fail('Do not get Port-%s vendor serial num'%(str(i)+ '-0050'))

    if error_count or pass_count == 0:
        raise Exception('Failed run read_vendor_serial_num_test.')

@logThis
def ac_power_on_dut():
    KapokCommonLib.powerCycleToOnieRescueMode()

@logThis
def read_psu1_input_value_test(tool, pattern):
    check_the_system_watchdog_status(tool, pattern)

@logThis
def read_psu1_output_value_test(tool, pattern):
    check_the_system_watchdog_status(tool, pattern)

@logThis
def read_psu_present_value_test(tool, pattern):
    check_the_system_watchdog_status(tool, pattern)


@logThis
def check_the_come_watchdog_status(tool, pattern):
    pass_count = 0
    p1 = r'^\d$'
    cmd = 'cat ' + tool
    output = CommonLib.execute_command(cmd, timeout=120)
    for line in output.splitlines():
        line = line.strip()
        res = re.search(p1, line)
        if res:
            pass_count += 1
            get_value = res.group(0)
            if get_value == pattern:
                log.success('Get the watchdog enable status is %s' % get_value)
            else:
                log.fail('Failed get watchdog status is %s, expect status is %s' % (get_value, pattern))
    if pass_count == 0:
        raise Exception('Failed run check_the_come_watchdog_status')

@logThis
def write_and_read_the_come_watchdog_status(tool, status):
    write_and_read_fan_max_speed(tool, status)

@logThis
def check_the_rsense_value_test(tool, pattern):
    p1 = r'04 a5'
    pass_count = 0
    error_count = 0
    output = CommonLib.execute_command(tool, timeout=120)
    for line in output.splitlines():
        line = line.strip()
        res = re.search(p1, line)
        if res:
            pass_count += 1
            getHexValue = res.group(0)
            get_hex_value = getHexValue.replace(' ', '')
            get_value = int(get_hex_value, 16)
            if int(get_value) == int(pattern):
                log.success('Check rsense value pass, get value is %s'%get_value)
            else:
                error_count += 1
                log.fail('Check rsense value fail, get value is %s'%get_value)
    if error_count or (pass_count == 0):
        raise Exception('Failed run check_the_rsense_value_test')

@logThis
def read_poreset_value_test(tool, pattern):
    check_the_come_watchdog_status(tool, pattern)

@logThis
def write_poreset_value_test(tool, pattern):
    cmd = 'echo ' + pattern + ' > ' + tool
    log.info('============= Run cmd: [%s] ==============='%cmd)
    device.sendMsg(cmd + '\n')
    # CommonLib.execute_command(cmd, timeout=120)
    device.read_until_regexp(KapokConst.STOP_AUTOBOOT_PROMPT, timeout=200)
    device.sendMsg(KapokConst.STOP_AUTOBOOT_KEY)
    switchToDiagMode()

@logThis
def set_and_read_come_watchdog_trigger_time(tool, status):
    write_and_read_fan_max_speed(tool, status)

@logThis
def enable_come_watchdog_test(tool, pattern):
    cmd1 = 'echo ' + pattern + ' > ' + tool + ' ; sleep 3'
    cmd2 = 'echo ' + pattern + ' > ' + tool + ' ; sleep 10'
    for i in range(1, 3):
        CommonLib.execute_command(cmd1, timeout=120)
    log.info('####### Run cmd: [%s] #######'%cmd2)
    device.sendMsg(cmd2 + '\n')
    device.read_until_regexp(KapokConst.STOP_AUTOBOOT_PROMPT, timeout=200)
    device.sendMsg(KapokConst.STOP_AUTOBOOT_KEY)
    switchToDiagMode()

@logThis
def reboot_to_diagos_test(cmd):
    device.sendMsg(cmd + '\n')
    device.read_until_regexp(KapokConst.STOP_AUTOBOOT_PROMPT, timeout=200)
    device.sendMsg(KapokConst.STOP_AUTOBOOT_KEY)
    switchToDiagMode()

@logThis
def dump_fault_logger_test(path, cmd):
    tempLst = []
    p1 = r'000000\d+\s+(.*)\s+\|\.'
    switch_bsp_folder_path(path)
    output = CommonLib.execute_command(cmd, timeout=120)
    for line in output.splitlines():
        line = line.strip()
        res = re.search(p1, line)
        if res:
            get_value = res.group(1)
            tempLst.append(get_value)
    return tempLst

@logThis
def check_come_fault_logger_test(path, tool1, tool2, tool3):
    pass_count = 0
    error_count = 0
    reset_cmd = 'echo 1 > ' + tool2
    pause_cmd = 'echo 1 > ' + tool3
    start_cmd = 'echo 0 > ' + tool3
    ##1. first dump logger
    firstLst = dump_fault_logger_test(path, tool1)
    if len(firstLst) == 0:
        error_count += 1
        log.fail('Can not get the first dump logger.')
    else:
        log.info('####### First get the value is %s ########'%str(firstLst))
    CommonLib.execute_command(reset_cmd, timeout=120)
    reboot_to_diagos_test('reboot')
    ##2. Second dump logger
    secondLst = dump_fault_logger_test(path, tool1)
    if len(secondLst) == 0:
        error_count += 1
        log.fail('Can not get the second dump logger.')
    else:
        log.info('####### Second get the value is %s ########'%str(secondLst))
    ##check result, the first entry is diff, other is same
    for i in range(0, len(firstLst)):
        if i == 0 or i == 1:
            if firstLst[i] != secondLst[i]:
                pass_count += 1
                log.success('The second read first entry is different from first read')
            else:
                error_count += 1
                log.fail('Get the same value the first time and the second time')
        else:
            if firstLst[i] == secondLst[i]:
                pass_count += 1
                log.success('Other value is same the frist time and the second time.')
            else:
                error_count += 1
                log.fail('Other value is diff from frist and second time, firstValue: [%s], sencondValue: [%s]'%(firstLst, secondLst))
    CommonLib.execute_command(pause_cmd, timeout=120)
    reboot_to_diagos_test('reboot')
    ##3. Third dump logger
    thirdLst = dump_fault_logger_test(path, tool1)
    if len(thirdLst) == 0:
        error_count += 1
        log.fail('Can not get the third dump logger.')
    else:
        log.info('####### Second get the value is %s ########' % str(thirdLst))
    ## check result, they are the same second and third time.
    if secondLst == thirdLst:
        pass_count += 1
        log.success('They are same value the second and third time.')
    else:
        error_count += 1
        log.fail('They are diff value the second and third time, secondValue: [%s], thirdValue: [%s]'%(secondLst, thirdLst))
    CommonLib.execute_command(start_cmd, timeout=120)
    reboot_to_diagos_test('reboot')
    fourthLst = dump_fault_logger_test(path, tool1)
    if len(fourthLst) == 0:
        error_count += 1
        log.fail('Can not get the fourth dump logger.')
    else:
        log.info('####### Second get the value is %s ########' % str(fourthLst))
    ##check result, the second entry is diff, other is same
    for i in range(0, len(thirdLst)):
        if i == 2 or i == 3:
            if thirdLst[i] != fourthLst[i]:
                pass_count += 1
                log.success('The fourth read second entry is different from third read')
            else:
                error_count += 1
                log.fail('Get the same value the third time and the fourth time')
        else:
            if thirdLst[i] == fourthLst[i]:
                pass_count += 1
                log.success('Other value is same the third time and the fourth time.')
            else:
                error_count += 1
                log.fail('Other value is diff from third and fourth time, thirdValue: [%s], fourthValue: [%s]'%(thirdLst, secondLst))
    if error_count or pass_count == 0:
        raise Exception('Run failed check_come_fault_logger_test')

@logThis
def check_lane_measured_tx_bias_current(tool, option, caseType):
    read_lane_rx_and_tx_power_highest_test(tool, option, caseType)

@logThis
def check_lane_tx_bias_input(tool, option, caseType):
    read_lane_rx_and_tx_power_highest_test(tool, option, caseType)

@logThis
def check_lane_tx_bias_lowest(tool, option, caseType):
    read_lane_rx_and_tx_power_highest_test(tool, option, caseType)

@logThis
def enable_or_disable_lane_tx_output(tool, option, pattern):
    for i in range(101, 133):
        for k in range(1, 9):
            cmd = 'echo ' + pattern + ' > ' + tool + str(i) + '-0050/lane'+ str(k) + option
            CommonLib.execute_command(cmd, timeout=120)

@logThis
def read_lane_tx_fault_test(tool, option, caseType):
    read_lane_rx_and_tx_los_test(tool, option, caseType)

@logThis
def update_diagos_and_onie_test():
    #1. check diag and onie version
    onie_version = CommonLib.get_swinfo_dict("ONIE_Installer").get("newVersion", "NotFound")
    diag_version = CommonLib.get_swinfo_dict("DIAGOS").get("newVersion", "NotFound")
    cmd = 'get_versions'
    p1 = r'DIAGOS\s+(\d+)'
    p2 = r'ONIE\s+([.\d]+)'
    output = run_command(cmd, prompt=device.promptDiagOS, timeout=30)
    for line in output.splitlines():
        line = line.strip()
        diagres = re.search(p1, line)
        onieres = re.search(p2, line)
        if onieres:
            getOnieVer = onieres.group(1)
            if getOnieVer == onie_version:
                log.info('Get the onie version [%s] is new, don\'t need to update!'%getOnieVer)
            else:
                log.info('Get the onie version [%s] is old, need to update to [%s]!'%(getOnieVer, onie_version))
                #2. do onie update
                KapokCommonLib.bootIntoOnieRescueMode()
                onieSelfUpdate('new')
                verifyOnieAndCPLDVersion('new')
        elif diagres:
            getDiagver = diagres.group(1)
            if getDiagver == diag_version:
                log.info('Get the diag version [%s] is new, don\'t need to update!' % getDiagver)
            else:
                log.info('Get the diag version [%s] is old, need to update to [%s]!' % (getDiagver, diag_version))
                #2. do diag update
                KapokCommonLib.bootIntoOnieRescueMode()
                fhv2DiagdownloadImagesAndRecoveryDiagOS()



