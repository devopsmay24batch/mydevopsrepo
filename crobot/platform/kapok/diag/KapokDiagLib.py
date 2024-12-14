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
import CRobot
import sys
import os
from functools import partial
from Decorator import *
import re
import Logger as log
import CommonLib
import CommonKeywords
import KapokConst
import Const
import time
from collections import OrderedDict

try:
    from Device import Device
    import DeviceMgr
except Exception as err:
    log.cprint(str(err))

device = DeviceMgr.getDevice()
devicename = os.environ.get("deviceName", "")

workDir = CRobot.getWorkDir()
sys.path.append(os.path.join(workDir, 'common', 'commonlib'))
sys.path.append(os.path.join(workDir, 'platform/kapok'))
from KapokCommonVariable import fail_dict
import KapokCommonLib
import KapokDiagFhVariablesLatest as var
run_command = partial(CommonLib.run_command, deviceObj=device, prompt=device.promptDiagOS)


@logThis
def SetStaticAddress():
    ipaddr = CommonLib.Get_Not_Occupied_IP()
    cmd = 'setenv ipaddr ' + ipaddr + '\n'
    device.sendMsg(cmd)
    serverip = DeviceMgr.getServerInfo('PC').managementIP
    cmd = 'setenv serverip ' + serverip + '\n'
    device.sendMsg(cmd)
    device.read_until_regexp('setenv serverip (([01]{0,1}\d{0,1}\d|2[0-4]\d|25[0-5])\.){3}([01]{0,1}\d{0,1}\d|2[0-4]\d|25[0-5])')

@logThis
def UpdateBootImage():
    #cmd = 'setenv tftpdir {}'.format(KapokCommonLib.getUbootImageNamePrefix())
    #device.sendCmd(cmd)

    update_cmd = 'run bootupd' + '\n'
    device.sendMsg(update_cmd)
    device.read_until_regexp('done', timeout=90)
    time.sleep(10)
    reset_cmd = 'reset' + '\n'
    device.sendMsg(reset_cmd)
    device.read_until_regexp(KapokConst.STOP_AUTOBOOT_PROMPT, timeout=300)
    device.sendMsg(KapokConst.STOP_AUTOBOOT_KEY)
    device.getPrompt(Const.BOOT_MODE_UBOOT)
    cmd = 'env default -a' + '\n'
    device.sendMsg(cmd)
    device.read_until_regexp('Resetting to default environment', timeout=20)
    save_cmd = 'saveenv' + '\n'
    device.sendMsg(save_cmd)
    device.read_until_regexp('done', timeout=30)
    device.sendMsg('reset\n')
    #enter rescue mode
    device.read_until_regexp(KapokConst.STOP_AUTOBOOT_PROMPT, timeout=300)
    device.sendMsg(KapokConst.STOP_AUTOBOOT_KEY)
    device.sendCmdRegexp('run onie_rescue', 'Please press Enter to activate this console', timeout=900)
    device.sendMsg('\n')
    onie_discovery_stop_cmd = KapokConst.STOP_ONIE_DISCOVERY_KEY
    device.sendCmdRegexp(onie_discovery_stop_cmd, device.promptOnie, timeout=60)

@logThis
def tftp_download_image_to_unit(serverIp, hostPath, ImageFile, unitPath):
    #1. check unit path
    pathCmd = 'ls ' + unitPath
    mkdirCmd = 'mkdir -p ' + unitPath
    p1 = 'No such file or directory'
    output = device.executeCmd(pathCmd, timeout=60)
    if re.search(p1, output):
        device.sendCmd(mkdirCmd)
    #2. change the path
    cmd = 'cd ' + unitPath
    device.sendMsg(cmd)
    #3. tftp copy image
    copyCmd = 'tftp -g ' + serverIp + ' -r ' + hostPath + '/' + ImageFile
    device.executeCmd(copyCmd, timeout=60)

@logThis
def flash_uboot_partition(tool, flashDevice, imgFile, imgPath):
    pass_count = 0
    cmd = tool + ' -v ' + imgPath + '/' + imgFile + ' ' + flashDevice
    p1 = var.uboot_pattern
    output = device.executeCmd(cmd, timeout=180)
    # output = device.sendCmdRegexp(cmd, p1, timeout=180)
    for line in output.splitlines():
         line = line.strip()
         match = re.search(p1, line)
         if match:
             pass_count += 1
    if pass_count > 0:
        log.info('uboot update successfully!')
    else:
        log.fail('uboot udpate fail!')
        raise Exception("Failed flash_uboot_partition")

@logThis
def verifyBootImage(cmd):
    # device.getPrompt(Const.BOOT_MODE_ONIE)
    u_boot_version = CommonLib.get_swinfo_dict('UBOOT').get('newVersion')
    u_boot_version = CommonLib.escapeString(u_boot_version)
    pass_count = 0
    output = device.executeCmd(cmd, mode=Const.BOOT_MODE_DIAGOS)
    for line in output.splitlines():
        if re.search(u_boot_version, line):
            pass_count += 1
    if pass_count:
        log.success("check boot image version is passed")
    else:
        log.fail("check boot image version failed")
        device.raiseException("Failure while checking boot image version info")

@logThis
def check_uboot_version_in_onie_mode(cmd):
    # device.getPrompt(Const.BOOT_MODE_ONIE)
    u_boot_version = CommonLib.get_swinfo_dict('UBOOT').get('newVersion')
    u_boot_version = CommonLib.escapeString(u_boot_version)
    pass_count = 0
    output = device.executeCmd(cmd, mode=Const.BOOT_MODE_ONIE)
    for line in output.splitlines():
        if re.search(u_boot_version, line):
            pass_count += 1
    if pass_count:
        log.success("check boot image version is passed")
    else:
        log.fail("check boot image version failed")
        device.raiseException("Failure while checking boot image version info")

@logThis
def VerifyBootToEachMode():
    device.getPrompt(Const.BOOT_MODE_DIAGOS)
    device.getPrompt(Const.BOOT_MODE_UBOOT)
    device.getPrompt(Const.BOOT_MODE_ONIE)
    device.getPrompt(Const.BOOT_MODE_UBOOT)
    device.getPrompt(Const.ONIE_RESCUE_MODE)
    device.getPrompt(Const.BOOT_MODE_UBOOT)


@logThis
def ResetDefaultBootToDiag():
    reset_boot_cmd = 'setenv onie_boot_reason diag\n'
    device.sendMsg(reset_boot_cmd)
    device.read_until_regexp('setenv onie_boot_reason diag')
    save_cmd = 'save\n'
    device.sendMsg(save_cmd)
    device.read_until_regexp('save')
    boot_cmd = 'boot\n'
    device.sendMsg(boot_cmd)
    output = device.read_until_regexp(device.loginPromptDiagOS, timeout=300)
    if output:
        KapokCommonLib.powerCycleToUboot()
        log.success("set default boot to diag is passed")
    else:
        log.fail("set default boot to diag is failed")
        device.raiseException("Failure while set default boot to diag")


@logThis
def SetDefaultEnv():
    set_default_env_cmd = 'env default -a\n'
    device.sendMsg(set_default_env_cmd)
    device.read_until_regexp('env default -a')
    save_cmd = 'savee\n'
    device.sendMsg(save_cmd)
    device.read_until_regexp('savee')

@logThis
def checkUartMuxFunction(ucmd_list, duration=30):
    end_key = "D"
    for check_uc_cmd in ucmd_list:
        device.sendMsg(check_uc_cmd + '\r\n')
        time.sleep(duration)
    device.sendMsg(end_key)
    device.sendMsg("\n")
    finish_prompt = "{}[\s\S]+{}".format(check_uc_cmd[:5], device.promptDiagOS)
    output = device.read_until_regexp(finish_prompt, timeout=duration)
    uc_alive_pattern = "uC is alive for"
    find_uc_alive = re.findall(uc_alive_pattern, output)
    if not find_uc_alive:
        raise Exception("uC is not alive.")



def VerifyHwVersion(cmd_list, path, hw_dict, tool_name, option):
    for cmd in cmd_list:
        device.executeCmd(cmd)
    sys_cpld_version = CommonLib.get_swinfo_dict('CPLD').get('newVersion').get('SYSCPLD')
    cpld_dict = CommonLib.get_swinfo_dict('CPLD')
    led_cpld1_version = cpld_dict.get('newVersion').get('SWLEDCPLD1')
    led_cpld2_version = cpld_dict.get('newVersion').get('SWLEDCPLD2')
    fan_cpld = cpld_dict.get('newVersion').get('FANCPLD')
    #l = lambda x: str(hex(x))
    #g = lambda x: str(x/10)
    devicename = os.environ.get("deviceName", "")
    if "fenghuangv2" in devicename.lower():
        dev_type = DeviceMgr.getDevice(devicename).get('cardType')
        if dev_type == '1PPS':
            ic2fpga = CommonLib.get_swinfo_dict("ASC").get("1pps", "NotFound")
        else:
            ic2fpga = CommonLib.get_swinfo_dict("ASC").get("fpga", "NotFound")
        uc_app = CommonLib.get_swinfo_dict("UC").get("newVersion", "NotFound").get("uC_app")
        uC_bl = CommonLib.get_swinfo_dict("UC").get("newVersion", "NotFound").get("uC_bl")
        asc10_0 = CommonLib.get_swinfo_dict("ASC").get("newVersion", "NotFound").get("ASC10-0")
        asc10_1 = CommonLib.get_swinfo_dict("ASC").get("newVersion", "NotFound").get("ASC10-1")
        asc10_2 = CommonLib.get_swinfo_dict("ASC").get("newVersion", "NotFound").get("ASC10-2")
        hw_dict = {'uc_app': uc_app, 'uc_bl': uC_bl, 'ASC10-0': asc10_0, 'ASC10-1': asc10_1, 'ASC10-2': asc10_2, 'I2CFPGA': ic2fpga}
        cpld_version_dict = {'SYSCPLD' : sys_cpld_version, 'SWLEDCPLD1' : led_cpld1_version, 'SWLEDCPLD2' : led_cpld2_version,
                             'FANCPLD' : fan_cpld}
    else:
        uc_app = CommonLib.get_swinfo_dict("UC").get("newVersion", "NotFound").get("uC_app")
        uC_bl = CommonLib.get_swinfo_dict("UC").get("newVersion", "NotFound").get("uC_bl")
        asc1 = CommonLib.get_swinfo_dict("ASC").get("newVersion", "NotFound").get("ASC1")
        asc2 = CommonLib.get_swinfo_dict("ASC").get("newVersion", "NotFound").get("ASC2")
        hw_dict = {'uc_app': uc_app, 'uc_bl': uC_bl, 'ASC1': asc1, 'ASC2': asc2}
        cpld_version_dict = {'SystemCPLD': sys_cpld_version, 'SWLEDCPLD1': led_cpld1_version,
                            'SWLEDCPLD2': led_cpld2_version, 'FANCPLD': fan_cpld}
    hw_dict.update(cpld_version_dict)
    keys_list = list(hw_dict.keys())
    values_list = list(hw_dict.values())
    passpattern = list()
    if len(keys_list) == len(values_list):
        for i in range(0, len(keys_list)):
            passpattern.append(keys_list[i] + '.*' + values_list[i])
    else:
        log.fail("get HW versions is failed")
        device.raiseException("Failure while get HW versions info")
    log.debug('passpattern=%s' % passpattern)
    cmd = 'cd ' + path
    device.executeCmd(cmd)
    check_cmd = './' + tool_name + ' ' + option
    output = device.executeCmd(check_cmd)
    passCount = 0
    for line in output.splitlines():
        for pattern in passpattern:
            if re.search(pattern, line, re.IGNORECASE):
                log.debug('the matched version:%s' % line)
                passCount += 1
    if passCount == len(passpattern):
        log.success("verify HW version is passed")
    else:
        log.fail("verify HW versions is failed")
        device.raiseException("Failure while verify HW versions info")

@logThis
def checkPostInfo(pattern):
    pass_pattern = []
    uboot_dict = CommonLib.get_swinfo_dict('UBOOT')
    uboot_version = uboot_dict.get('newVersion')
    temp_str = ['-', '(', ')', '.', '+']
    for i in temp_str:
        if i in uboot_version:
            new_str = '\\' + i
            uboot_version = uboot_version.replace(i, new_str)
    pass_pattern.append(uboot_version)
    pass_pattern.extend(pattern)
    sys_cpld_version = CommonLib.get_swinfo_dict('CPLD').get('newVersion').get('SYSCPLD')
    SystemCPLD = sys_cpld_version[-2:]
    pass_pattern.append('^SystemCPLD.*' + SystemCPLD)
    cpld_dict = CommonLib.get_swinfo_dict('CPLD')
    led_cpld1_version = cpld_dict.get('newVersion').get('SWLEDCPLD1')
    SWLEDCPLD1 = led_cpld1_version[-1:]
    pass_pattern.append('^SWLEDCPLD1.*' + SWLEDCPLD1)
    led_cpld2_version = cpld_dict.get('newVersion').get('SWLEDCPLD2')
    SWLEDCPLD2 = led_cpld2_version[-1:]
    pass_pattern.append('^SWLEDCPLD2.*' + SWLEDCPLD2)
    fan_cpld = cpld_dict.get('newVersion').get('FANCPLD')
    FANCPLD = fan_cpld[-1:]
    pass_pattern.append('^FANCPLD.*' + FANCPLD)
    pass_count = 0
    error_count = 0
    device.sendMsg('reboot' + '\r\n')
    output = device.read_until_regexp(KapokConst.STOP_AUTOBOOT_PROMPT, timeout=60)
    device.sendMsg(KapokConst.STOP_AUTOBOOT_KEY)
    for pattern in pass_pattern:
        for line in output.splitlines():
            res = re.search(pattern, line, re.IGNORECASE)
            if res:
                pass_count += 1
                log.success('Get the version is %s successfully.'%pattern)
        if pass_count == 0:
            error_count += 1
            log.fail('Do not find match Value: %s'%pattern)
        else:
            pass_count = 0
    if error_count > 0:
        raise Exception('check post info failed')


@logThis
def checkMacAddress(mac_address=None):
    if 'tianhe' in devicename.lower():
        cmd_list = [
            "cd /root/diag",
            "ifconfig eth0",
            "export LD_LIBRARY_PATH=/root/diag/output",
            "export CEL_DIAG_PATH=/root/diag",
            "./cel-eeprom-test -r -t tlv -d 2",
            "./cel-phy-test -r -d 1 -t mac"
        ]
    else:
        cmd_list = [
            "cd /root/diag",
            "ifconfig eth0",
            "export LD_LIBRARY_PATH=/root/diag/output",
            "export CEL_DIAG_PATH=/root/diag",
            "./cel-eeprom-test -r -t tlv -d 1",
            "./cel-phy-test -r -d 1 -t mac"
            ]
    output = run_command(cmd_list)
    eeprom_mac_pattern = "Base MAC Address.*\s(((\d|[A-F]){2}\:){5}.*)" 
    xphy_mac_pattern = "'eth0' MAC =\s+(.*:.*)"
    xphy_mac_match = re.search(xphy_mac_pattern, output)
    eeprom_mac_match = re.search(eeprom_mac_pattern, output)
    if not eeprom_mac_match:
        raise Exception("Didn't find MAC info with tool cel-eeprom-test.")
    if not xphy_mac_match:
        raise Exception("Didn't find MAC info with tool cel-phy-test.")
    eeprom_mac = eeprom_mac_match.group(1).strip()
    xphy_mac = xphy_mac_match.group(1).strip()
    log.info("///////eeprom_mac = %s //////" % eeprom_mac)
    log.info("///////xphy_mac = %s //////" % xphy_mac)
    if eeprom_mac != xphy_mac:
        raise Exception("MAC info is mismatch between tools cel-eeprom-test and cel-phy-test.")
    if mac_address:
        if mac_address != xphy_mac:
            raise Exception("MAC expected: {}, current: {}".format(mac_address, xphy_mac))

    return xphy_mac

@logThis
def getMacAddress():
    #CommonLib.change_dir(var.diag_tools_path)
    output = run_command('cd /root/diag')
    if re.search("(No such file|can't cd)", output):
        raise Exception("Didn't found DIAG PATH")
    if 'tianhe' in devicename.lower():
        output = device.executeCmd('./cel-eeprom-test -r -t tlv -d 2')
    else:
        output = device.executeCmd('./cel-eeprom-test -r -t tlv -d 1')
    eeprom_mac_pattern = "Base MAC Address.*\s(((\d|[A-F]){2}\:){5}.*)"
    eeprom_mac_match = re.search(eeprom_mac_pattern, output)
    if not eeprom_mac_match:
        raise Exception("Didn't find MAC info with tool cel-eeprom-test.")
    eeprom_mac = eeprom_mac_match.group(1).strip()
    log.info("///////eeprom_mac = %s //////" % eeprom_mac)
    return eeprom_mac

@logThis
def switch_folder_path(path):
    cmd = 'cd ' + path
    p1 = "can't cd"
    output = device.executeCommand(cmd, device.promptDiagOS)
    if re.search(p1, output):
        log.fail('switch folder fail!')
        raise Exception('Change %s path failed!'%(path))
    else:
        log.info('Switch the folder successfully!')

@logThis
def check_current_file(path, logFile):
    cmd = 'ls ' + path + '/' + logFile
    p1 = 'No such file or directory'
    output = device.executeCmd(cmd)
    if re.search(p1, output):
        raise Exception('Do not find %s file' % (logFile))
    else:
        log.success('Find %s file.'%logFile)

@logThis
def disable_or_enable_protection(protectValue, COMeEEValue, SYSEEValue):
    p1 = '^(\d)'
    COMeCmd = 'echo ' + protectValue + ' > ' + COMeEEValue
    SYSCmd = 'echo ' + protectValue + ' > ' + SYSEEValue
    checkCOMeValue = 'cat ' + COMeEEValue
    checkSYSValue = 'cat ' + SYSEEValue
    COMeTlvCmd = COMeCmd + ' ; ' + checkCOMeValue
    SYSTlvCmd = SYSCmd + ' ; ' + checkSYSValue
    setProtectCmdlst = [COMeTlvCmd, SYSTlvCmd]
    for cmd in setProtectCmdlst:
        # output = run_command(cmd)
        output = device.executeCmd(cmd)
        time.sleep(2)
        for line in output.splitlines():
            line = line.strip()
            res = re.search(p1, line)
            if res:
                if str(res.group(1)) == protectValue:
                    if str(res.group(1)) == '1':
                        log.info('disable the write protection')
                    else:
                        log.info('enable the write protection')
                else:
                    log.fail('Write protection fail, getValue is %s, expectValue is %s'%(str(res.group(1)), protectValue))
                    raise Exception('Failed run %s command'%cmd)

@logThis
def erase_eeprom_then_read_eeprom_value(typeValue, eepromTool, eraseCmd, readCmd):
    error_count = 0
    p1 = r'Product Name[ \t]+0x21[ \t]+\d+[ \t]+\w+'
    p2 = 'Invalid TLV header found'
    COMeEraseCmd = './' + eepromTool + eraseCmd + '1'
    SYSEraseCmd = './' + eepromTool + eraseCmd + '2'
    readCOMeCmd = './' + eepromTool + readCmd + '1'
    readSYSCmd = './' + eepromTool + readCmd + '2'
    storeSYSCmd = readSYSCmd + ' > ' + var.storeFile
    eraseTlvCmd = [COMeEraseCmd, SYSEraseCmd]
    for cmd in eraseTlvCmd:
        time.sleep(1)
        device.executeCmd(cmd)
    readCmdLst = [readCOMeCmd, readSYSCmd]
    for cmd in readCmdLst:
        time.sleep(2)
        output = device.executeCmd(cmd)
        res1 = re.search(p1, output)
        res2 = re.search(p2, output)
        if res1 and typeValue == 'True':
            log.success('Get command [%s] the eeprom info'%cmd)
            if '2' in cmd:
                device.executeCmd(storeSYSCmd)
        elif res1 and typeValue == 'False':
            error_count += 1
            log.fail('Error: the write protection should be enable')
        elif res2 and typeValue == 'True':
            error_count += 1
            log.fail('Error: the write protection should be disable')
        elif res2 and typeValue == 'False':
            log.success('Have erased the eeprom data.')
    if error_count > 0:
        raise Exception('Failed run erase_eeprom_then_read_eeprom_value')

@logThis
def write_eeprom_data(eepromTool, writeCmd, logFile):
    error_count = 0
    pass_count = 0
    #1. check if the log file exists
    check_current_file(var.diag_tools_path, logFile)
    #2. check expect value dict
    p1 = r'(0x\w{2})[ \t]+\d+[ \t]+(.*)'
    p2 = r'0x01|0x03|0xFE|0xFD'
    p3 = '^ONIE[ \t]+(.*)'
    p4 = r'^Vendor Extension[ \t]+0xFD[ \t]+\d+[ \t]+(Amazon)$'
    p5 = r'Fail to write data to tlv eeprom'
    store_dict = {}
    storeCmd = 'cat ' + var.diag_tools_path + '/' + logFile
    output = device.executeCmd(storeCmd)
    for line in output.splitlines():
        line = line.strip()
        res = re.search(p1, line)
        if res:
            if re.search(p2, line):
                continue
            expectKey = res.group(1)
            expectValue = res.group(2)
            store_dict[expectKey] = expectValue
    log.info('#### get the expect eeprom value as the below: ####')
    log.info(store_dict)
    #3. write eeprom
    versionInfo = device.executeCmd(var.get_versions_cmd, timeout=60)
    for line in versionInfo.splitlines():
        line = line.strip()
        match = re.search(p3, line)
        if match:
            onieVer = match.group(1)
    for i in range(1, 3):
        time.sleep(1)
        for key, value in store_dict.items():
            if key == '0x25':
                cmd = './' + eepromTool + writeCmd + str(i) + ' -A ' + key + " -D '" + value + "'"
            else:
                cmd = './' + eepromTool + writeCmd + str(i) +' -A ' + key + ' -D ' + value
            time.sleep(1)
            output = device.executeCmd(cmd, timeout=120)
            if p5 in output:
                error_count += 1
                log.fail('%s write error.' % key)
            else:
                log.success('successfully write [%s] get the value is [%s]' % (key, value))
        #check onie version
        if '0x29' in store_dict:
            log.info('==== Have wrote ONIE version is [%s] ===='%store_dict['0x29'])
        else:
            # onieObj = SwImage.getSwImage('ONIE_Installer')
            # onieVer = onieObj.newVersion
            onieCmd = './' + eepromTool + writeCmd + str(i) + ' -A 0x29 -D ' + onieVer
            output = device.executeCmd(onieCmd, timeout=120)
            if '0x29' in output:
                log.success('successfully write [0x29] get the value is [%s]' % (onieVer))
            else:
                error_count += 1
                log.fail('0x29 write error.')
        #check 0xfd
        fdValueLst = var.fdValue
        initFdCmd = './' + eepromTool + writeCmd + str(i) + ' -A 0xfd'
        device.executeCmd(initFdCmd, timeout=120)
        for value in fdValueLst:
            fdCmd = './' + eepromTool + writeCmd + str(i) + " -A 0xfd -D '" + value + "'"
            time.sleep(1)
            output = device.executeCmd(fdCmd, timeout=120)
            for line in output.splitlines():
                line = line.strip()
                res = re.search(p4, line)
                if res:
                    pass_count += 1
                    log.success('successfully write [0xFD] get the value is [%s]' %(res.group(1)))
            if pass_count > 0:
                pass_count = 0
            else:
                log.fail('Write 0xFD fail.')
        #read tlv eeprom
        tlvCmd = './' + eepromTool + var.readTlvCmd + str(i)
        device.executeCmd(tlvCmd, timeout=120)
    if error_count > 0:
        raise Exception('Failed run write_eeprom_data')

@logThis
def disable_or_enable_All_Protect(typeValue, fanDevice):
    disable_protect_cmd = fanDevice
    for i in range(0,len(disable_protect_cmd)):
        if typeValue == '0':
            output = CommonLib.execute_command('echo 0 > '+disable_protect_cmd[i], timeout=60)
        elif typeValue == '1':
            output = CommonLib.execute_command('echo 1 > ' + disable_protect_cmd[i], timeout=60)
        fail_pattern = '\-bash\:.*?Permission denied'
        match = re.search(fail_pattern, output)
        if match:
            device.raiseException("Failure with disable %s " % disable_protect_cmd[i])
        else:
            log.info("Disable protect %s pass." % disable_protect_cmd[i])

@logThis
def write_sample_fan_eeprom(fanEeprom, defEeprom, fanSample, defSample):
    delCmd1 = 'rm -rf ' + fanSample
    delCmd2 = 'rm -rf ' + defSample
    device.sendMsg(delCmd1)
    device.sendMsg('\n')
    device.sendMsg(delCmd2)
    for line in fanEeprom:
        cmd = "echo -e %s >> %s" % (line, fanSample)
        CommonLib.execute_command(cmd, timeout=60)
    for line in defEeprom:
        cmd = "echo -e %s >> %s" % (line, defSample)
        CommonLib.execute_command(cmd, timeout=60)
    fanCmd = 'cat ' + fanSample
    defCmd = 'cat ' + defSample
    cmdLst = [fanCmd, defCmd]
    for cmd in cmdLst:
        CommonLib.execute_command(cmd, timeout=60)

@logThis
def write_and_read_then_store_fan_eeprom(typeValue, tool, writeCmd, readCmd, PathFile, storeCmd):
    error_count = 0
    p1 = r'Succeed to Write data to dev-\d+, count=\d+'
    p2 = r'Board Part Number[ \t]+:[ \t]+([\w-]+)'
    p3 = r'EEPROM Write protect is enabled, please disable first'
    ## write process
    for i in range(1, 12):
        cmd = './' + tool + writeCmd + str(i) + ' -f ' + PathFile
        output = device.executeCmd(cmd, timeout=60)
        if re.search(p1, output):
            log.success('Successfully write fan eeprom dev-%d.'%i)
        else:
            if typeValue == '1':
                if (i != 1) or (i != 2) or (i != 4):
                    if re.search(p3, output):
                        log.success('The write protection is enable, so dev-%s can not write the eerprom data.'%i)
                    else:
                        error_count += 1
                        log.fail('Failed dev-%d should not be able to write the eeprom data.'%i)
            else:
                error_count += 1
                log.fail('Failed write fan eeprom dev-%d'%i)
    ## read process
    for k in range(1, 12):
        cmd = './' + tool + readCmd + str(k) + ' -C 1024 |tee ' + storeCmd + str(k)
        output = device.executeCmd(cmd, timeout=60)
        if re.search(p2, output):
            log.success('Successfully read fan eeprom dev-%d.' % k)
        else:
            error_count += 1
            log.fail('Failed read fan eeprom dev-%d' % k)

@logThis
def compare_eeprom_data(store1, store2):
    ## fru-1/2/4 is diff
    error_count = 0
    p1 = r'Board Part Number[ \t]+:[ \t]+([\w-]+)'
    for i in range(1, 12):
        cmd1 = 'cat ' + store1 + str(i)
        cmd2 = 'cat ' + store2 + str(i)
        output1 = device.executeCmd(cmd1, timeout=60)
        output2 = device.executeCmd(cmd2, timeout=60)
        res1 = re.search(p1, output1)
        res2 = re.search(p1, output2)
        getPnValue1 = res1.group(1)
        getPnValue2 = res2.group(1)
        if (i == 1) or (i == 2) or (i == 4):
            if getPnValue1 != getPnValue2:
                log.success('Successfully the PN value is diff, value1=%s, value2=%s'%(getPnValue1, getPnValue2))
            else:
                error_count += 1
                log.fail('Failed get the same PN value by twice, value1=%s, value2=%s'%(getPnValue1, getPnValue2))
        else:
            if getPnValue1 == getPnValue2:
                log.success('Successfully the PN value is same, value1=%s, value2=%s'%(getPnValue1, getPnValue2))
            else:
                error_count += 1
                log.fail('Failed get the diff PN value by twice, value1=%s, value2=%s' % (getPnValue1, getPnValue2))
    if error_count > 0:
        raise Exception('Failed run compare_eeprom_data')

@logThis
def delete_log_file(path, logFile):
    cmd = 'rm -rf ' + path + '/' + logFile + '*'
    device.executeCmd(cmd, timeout=60)

@logThis
def check_fpga_and_board_version(fpgaTool, boardTool):
    error_count = 0
    fpgaVer = CommonLib.get_swinfo_dict("1PPS_FPGA").get('newVersion')
    fpgaCmd = 'cat ' + fpgaTool
    boardCmd = 'cat ' + boardTool
    cmdLst = [fpgaCmd, boardCmd]
    expectValueLst = [fpgaVer, var.boardVer]
    for i in range(0, 2):
        output = device.executeCmd(cmdLst[i], timeout=60)
        res = re.search(expectValueLst[i], output)
        if res:
            log.success('Get the version is %s'%expectValueLst[i])
        else:
            error_count += 1
            log.fail('Failed the version [%s] is not expect value [%s].'%(res.group(0), expectValueLst[i]))
    if error_count > 0:
        raise Exception('Failed run check_fpga_and_board_version')

@logThis
def qsfp_all_present_check(qsfpTool, option):
    pass_count = 0
    p1 = r'QSFP-DD[ \t]+\|[ \t]+Present'
    cmd = './' + qsfpTool + option
    output = device.executeCmd(cmd, timeout=60)
    for line in output.splitlines():
        line = line.strip()
        res = re.search(p1, line)
        if res:
            pass_count += 1
    if pass_count == 32:
        log.success('Have %d qsfp present'%pass_count)
    else:
        raise Exception('Failed run qsfp_all_present_check')

@logThis
def get_ipv4_address_from_dhcp(dhcpTool, ethDev):
    p1 = r'inet addr:([\d\.]+)[ \t]+Bcast:[\d\.]+'
    device.executeCmd(dhcpTool, timeout=60)
    ethCmd = 'ifconfig ' + ethDev
    output = device.executeCmd(ethCmd, timeout=60)
    res = re.search(p1, output)
    if res:
        getIpv4 = res.group(1)
    else:
        log.info('Failed can not get ipv4 address')
        raise Exception('Failed run get_ipv4_address_from_dhcp')
    return getIpv4

@logThis
def modify_phy_config_file(dhcpTool, ethDev, serverIp, phyFile):
    p1 = r'\w+_\w+: "(.*)"'
    #1. get ipv4
    getIp = get_ipv4_address_from_dhcp(dhcpTool, ethDev)
    #2. modify ip address in phy file
    phy_server_ip_cmd = 'cat configs/' + phyFile + ' |grep "server_ip"'
    phy_local_ip_cmd = "cat configs/" + phyFile + ' |grep "ip_addr"'

    phyCmdLst = [phy_server_ip_cmd, phy_local_ip_cmd]
    expectIpLst = [serverIp, getIp]
    for i in range(0, 2):
        output = device.executeCmd(phyCmdLst[i], timeout=60)
        res = re.search(p1, output)
        if res:
            phy_ip = res.group(1)
            if phy_ip == expectIpLst[i]:
                log.info('ip address is correct.')
            else:
                changeIpCmd = 'sed -i "s/' + phy_ip + '/' + expectIpLst[i] + '/" configs/' + phyFile
                device.executeCmd(changeIpCmd, timeout=60)
    device.executeCmd("cat configs/" + phyFile, timeout=60)

@logThis
def write_speed_and_ping_test(phyTool, option, speedTool, ethDev):
    error_count = 0
    p1 = r"Try to set the speed \[(\d+)\] for 'eth0'."
    p2 = r'Speed: (\d+)Mb/s'
    p3 = r'Phy test : Passed'
    speedLst = [10, 100, 1000]
    ethCmd = speedTool + ' ' + ethDev
    pingCmd = './' + phyTool + ' --all'
    for i in speedLst:
        time.sleep(2)
        WriteCmd = './' + phyTool + option + str(i)
        output = device.executeCmd(WriteCmd, timeout=60)
        res = re.search(p1, output)
        if res:
            setSpeed = res.group(1)
            output1 = device.executeCmd(ethCmd, timeout=60)
            res1 = re.search(p2, output1)
            if res1:
                getSpeed = res1.group(1)
                if getSpeed == setSpeed:
                    log.info('Check write speed [%s]Mb/s successfully!'%getSpeed)
                    output2 = device.executeCmd(pingCmd, timeout=120)
                    res2 = re.search(p3, output2)
                    if res2:
                        log.success('Ping [%s]Mb/s speed successfully!'%getSpeed)
                    else:
                        error_count += 1
                        log.fail('Ping [%s]Mb/s speed fail!'%getSpeed)
                else:
                    error_count += 1
                    log.fail('Get speed failed!')
        else:
            error_count += 1
            log.fail('Set speed failed!')
    if error_count > 0:
        raise Exception('Failed run write_speed_and_ping_test')

@logThis
def rtc_time_rollover_or_write_or_read_check(rtcTool, option, pattern):
    cmd = './' + rtcTool + option
    output = device.executeCmd(cmd, timeout=120)
    if re.search(pattern, output):
        log.success('Check [%s]!'%pattern)
    else:
        log.fail('Check rtc %s fail!'%str(pattern[4:9]))
        raise Exception('Failed run rtc_time_rollover_or_write_or_read_check')

@logThis
def check_diag_test_all(tool, option):
    p1 = r'cel-\w+-test[ \t]+\|.*\|[ \t]+Passed'
    pass_count = 0
    cmd = './' + tool + option
    output = device.executeCmd(cmd, timeout=1200)
    for line in output.splitlines():
        line = line.strip()
        res = re.search(p1, line)
        if res:
            pass_count += 1
    if pass_count == 20:
        log.success('Check diag all test successfully!')
    else:
        raise Exception('Failed run check_diag_test_all')

@logThis
def check_ssd_stress_test(tool, logFile, patternLst):
    error_count = 0
    cmd = './' + tool
    logCmd = 'cat ' + logFile
    device.executeCmd(cmd, timeout=1200)
    output = device.executeCmd(logCmd, timeout=120)
    if 'error' in output:
        error_count += 1
        log.fail('Find error info.')
    for line in patternLst:
        res = re.search(line, output)
        if res:
            log.info('Check ssd log file passed!')
        else:
            error_count += 1
            log.fail('Can not pattern the log file')
    if error_count > 0:
        raise Exception('Failed run check_ssd_stress_test')

@logThis
def verifyFANboardCPLDaccess():
    cmd_list = [
        "cd /root/diag",
        "./cel-cpld-test -s -d 5",
        "./cel-cpld-test --all",
    ]
    output = run_command(cmd_list)
    cpld_all_pattern = "CPLD test \: Passed"
    cpld_dump_pattern = "CPLD Scan \: Passed"
    cpld_all_match = re.search(cpld_all_pattern, output)
    cpld_dump_match = re.search(cpld_dump_pattern, output)
    if not cpld_all_match:
        raise Exception("Fan board CPLD access all test failed!")
    else:
        log.info("Fan board CPLD access all test successfully")
    if not cpld_dump_match:
        raise Exception("Fan board CPLD access dump test failed!")
    else:
        log.info("Fan board CPLD access dump test successfully")

@logThis
def verifyInterruptChecking():
    cmd_list = [
        "cd /root/diag",
        "./cel-irq-test --test -t lm75",
    ]
    output = run_command(cmd_list)
    interruput_pattern = "LM75 Interrupt test : Passed"
    interruput_match = re.search(interruput_pattern, output)
    if not interruput_match:
        raise Exception("Interrupt Checking test failed!")
    else:
        log.info("Interrupt Checking test successfully")
    if not interruput_match:
        raise Exception("Interrupt Checking test failed!")
    else:
        log.info("Interrupt Checking test successfully")

@logThis
def modifyMacAddress(write_mac=None):
    if not write_mac:
        import random
        random_mac = random.sample("0123456789ABCDEF", 10)
        write_mac = [ random_mac[i]+":" if i%2==1 else random_mac[i] for i in range(len(random_mac)) ]
        write_mac = "".join(write_mac).rstrip(":")
        write_mac = '00:' + write_mac
        log.info("Setting randome MAC: {}".format(write_mac))

    devicename = os.environ.get("deviceName", "")
    if "fenghuangv2" in devicename.lower():
        modify_mac_cmd = "./cel-eeprom-test -w -t tlv -d 1 -A 0x24 -D {}".format(write_mac)
        cmd_list = [
            "cd /root/diag",
            "echo 0 > /sys/bus/i2c/devices/8-0060/system_eeprom_wp",
            modify_mac_cmd,
            "rm /etc/udev/rules.d/70-persistent-net.rules"
        ]
    else:
        modify_mac_cmd = "./cel-eeprom-test -w -t tlv -d 2 -A 0x24 -D {}".format(write_mac)
        cmd_list = [
            "cd /root/diag",
            "echo 0 > /sys/bus/i2c/devices/19-0060/system_eeprom_wp",
            modify_mac_cmd
        ]
    output = run_command(cmd_list)
    CommonLib.execute_check_dict(Const.DUT, "", patterns_dict=fail_dict,
                                check_output=output, is_negative_test=True)

    KapokCommonLib.bootIntoUboot()
    KapokCommonLib.resetUbootEnv()
    KapokCommonLib.bootIntoDiagOSMode()
    checkMacAddress(write_mac)

@logThis
def verifyCPLDaccess():
    cmd_list = [
        "cd /root/diag",
        "export LD_LIBRARY_PATH=/root/diag/output",
        "export CEL_DIAG_PATH=/root/diag",
        "./cel-cpld-test --all",
        "./cel-cpld-test --dump -d 1",
        "./cel-cpld-test -s -d 1",
        "./cel-cpld-test --h"
    ]
    output = run_command(cmd_list)
    cpld_all_pattern = "CPLD test \: Passed"
    cpld_dump_pattern = "CPLD Scan \: Passed"
    cpld_all_match = re.search(cpld_all_pattern, output)
    cpld_dump_match = re.search(cpld_dump_pattern, output)
    if not cpld_all_match:
        raise Exception("CPLD access all test failed!")
    else:
        log.info("CPLD access all test successfully")
    if not cpld_dump_match:
        raise Exception("CPLD access dump test failed!")
    else:
        log.info("CPLD access dump test successfully")

@logThis
def VerifyDiagToolTestResult(path, tool_name, option, pattern, is_cmd=False, timeout=120):
    time.sleep(2)
    if path:
        cmd = 'cd ' + path
        run_command(cmd, prompt=device.promptDiagOS)
    if not is_cmd:
        cmd = './' + tool_name + ' ' + option
    else:
        cmd = tool_name + ' ' + option
    output = run_command(cmd, prompt=device.promptDiagOS, timeout=timeout)
    log.cprint(output)
    if 'list' in option:
        if "48v" in devicename.lower():
            pattern = var.temp_test_pattern2_48V
    CommonKeywords.should_match_ordered_regexp_list(output, pattern)
    log.success("DIAG Tool test is passed")

@logThis
def ExportEnvPath(cmd_list):
    it = iter(cmd_list)
    while True:
        try:
            device.sendCmd(next(it))
        except StopIteration:
            break


@logThis
def WaitForExecute(timestamp):
    time.sleep(timestamp)


@logThis
def VerifyI2cdetectWithL(tool_name, option):
    cmd = tool_name + ' ' + option
    fail_list = ['.*command not found.*', '.*Permission denied.*', '.*No such file or directory.*']
    output = device.executeCmd(cmd)
    for line in output.splitlines():
        if line.startswith('i2c'):
            if line.endswith('I2C adapter'):
                continue
            else :
                log.fail("i2cdetect test is failed")
                device.raiseException("Failure while Testing %s with %s" % (tool_name, option))
        elif line in fail_list:
            log.fail("i2cdetect test is failed")
            device.raiseException("Failure while Testing %s with %s" % (tool_name, option))


@logThis
def verifySystemWatchdog(cmd=None):
    if not cmd:
        reset_cmd = 'echo 0 > /sys/bus/i2c/devices/15-0060/system_watchdog_enable'
        CommonLib.check_cmd_no_output(reset_cmd)
        cmd = 'echo 1 > /sys/bus/i2c/devices/15-0060/system_watchdog_enable'
    count = 5
    while count:
        count -= 1
        time.sleep(5)
        CommonLib.check_cmd_no_output(cmd)
    try:
        device.read_until_regexp('U-Boot.*', timeout=180)
    except BaseException:
        log.fail("system can not power cycle")
        device.raiseException("Failure while checking system watchdog")
    else:
        device.getPrompt(Const.BOOT_MODE_ONIE,timeout=100)
        device.getPrompt(Const.BOOT_MODE_DIAGOS,timeout=100)


@logThis
def systemResetToDiag(cmd):
    if (cmd == 'hotswap-reboot') or (cmd == 'pwrcycle-reboot'):
        if ("tianhe-d01" in devicename.lower()) or ("tianhe-d02" in devicename.lower()):
            log.info('Pls skip the test, it only support tianhe_48V unit!!!')
        else:
            CommonLib.transmit(cmd)
            device.read_until_regexp(KapokConst.STOP_AUTOBOOT_PROMPT, 200)
            device.sendMsg(KapokConst.STOP_AUTOBOOT_KEY)
            device.getPrompt(Const.BOOT_MODE_DIAGOS)
    else:
        CommonLib.transmit(cmd)
        device.read_until_regexp(KapokConst.STOP_AUTOBOOT_PROMPT, 200)
        device.sendMsg(KapokConst.STOP_AUTOBOOT_KEY)
        device.getPrompt(Const.BOOT_MODE_DIAGOS)

@logThis
def prepareEepromBurning(param=''):
    cmd_list = param
    output = run_command(cmd_list)
    CommonLib.execute_check_dict(Const.DUT, "", patterns_dict=fail_dict,
            check_output=output, is_negative_test=True)
    # cmd2 no Passed output
    if len(param) == 5:
        check_eeprom_pattern = {"EEPROM test : Passed" : "EEPROM test.*?Passed"}
        CommonLib.execute_check_dict(Const.DUT, "", patterns_dict=check_eeprom_pattern,
            check_output=output)

@logThis
def TestEepromBurning(param=''):
    cmd_list = param
    output = run_command(cmd_list)
    CommonLib.execute_check_dict(Const.DUT, "", patterns_dict=fail_dict,
            check_output=output, is_negative_test=True)

@logThis
def verifyInitOuputSameAsD1(param1='', param2=''):
    d1_cmd = param1
    init_cmd = param2
    output1 = CommonLib.execute_command(d1_cmd)
    output2 = CommonLib.execute_command(init_cmd)
    d1_list = []
    init_list = []
    for line1 in output1.splitlines():
        line1 = line1.strip()
        if '0x' in line1:
            d1_list.append(line1)
    for line2 in output2.splitlines():
        line2 = line2.strip()
        if '0x' in line2:
            init_list.append(line2)
    log.info('//d1_list=%s' % d1_list)
    log.info('//init_list=%s' % init_list)
    d1_list.sort()
    init_list.sort()
    if d1_list == init_list:
        log.success('Init_ouput is same as another one.')
    else:
        log.fail('one output is different another, please check it.')

@logThis
def recoveryEepromToDefault():

    devicename = os.environ.get("deviceName", "")
    if "fenghuangv2" in devicename.lower():
        default_cmd = "./cel-eeprom-test --init"
    else:
        default_cmd = "./cel-eeprom-test --all"
    default_value_list = []
    fina_value_dict = {}
    output = CommonLib.execute_command(default_cmd)
    for line in output.splitlines():
        if '0x' in line:
            line = line.strip()
            default_value_list.append(line)
    log.info('default_value_list %s' % default_value_list)
    if len(default_value_list) == 0:
        raise Exception("Burning EEPROM failed1")
    else:
        for value in default_value_list:
            if '0xFE' not in value:
                key = value.split("  ")[-2].strip()
                value = value.split("  ")[-1][2:].strip()
                fina_value_dict[key] = value
        if len(fina_value_dict) == 0:
            raise Exception("Burning EEPROM failed2")
    log.info('fina_value_dict: %s' % fina_value_dict)
    return fina_value_dict

@logThis
def burningTlvData(tlv_dict=''):
    devicename = os.environ.get("deviceName", "")
    if "fenghuangv2" in devicename.lower():
        disable_wp_cmd = 'echo 0 > /sys/bus/i2c/devices/8-0060/system_eeprom_wp'
        disable_fpga_cmd = 'echo 0 > /sys/bus/i2c/devices/8-0060/i2cfpga_eeprom_write_protect'
    else:
        disable_fpga_cmd = 'echo 0 > /sys/bus/i2c/devices/15-0060/i2cfpga_eeprom_write_protect'
        disable_wp_cmd = 'echo 0 > /sys/bus/i2c/devices/15-0060/system_eeprom_wp'    
    device.sendMsg(disable_wp_cmd+'\r\n')
    time.sleep(3)
    device.sendMsg(disable_fpga_cmd+'\r\n')
    time.sleep(3)
    device.sendMsg("cd /root/diag/" + "\r\n")
    if tlv_dict == '':
        tlv_dict = recoveryEepromToDefault()
        log.info("tlv_dict %s" % tlv_dict)
        for tlv_name, tlv_data in tlv_dict.items():
            if tlv_name == "0x25":
                cmd = './cel-eeprom-test -w -t tlv -d 1 -A {} -D "{}"'.format(tlv_name, tlv_data)
            else:
                cmd = "./cel-eeprom-test -w -t tlv -d 1 -A {} -D {}".format(tlv_name, tlv_data)
            output = CommonLib.execute_command(cmd)
            check_pattern = "{}.*?{}".format(tlv_name, tlv_data)
            if not re.search(check_pattern, output):
                raise Exception("Burning EEPROM failed: {}".format(tlv_name))
    else:
        for tlv_name, tlv_data in tlv_dict.items():
            if tlv_data[0] == "0x25":
                cmd = './cel-eeprom-test -w -t tlv -d 1 -A {} -D "{}"'.format(tlv_data[0], tlv_data[1])
            else:
                cmd = "./cel-eeprom-test -w -t tlv -d 1 -A {} -D {}".format(tlv_data[0], tlv_data[1])
                CommonLib.escapeString(tlv_data[1])
            check_pattern = "{}.*?{}".format(tlv_name, tlv_data[0])
            output = CommonLib.execute_command(cmd)
            time.sleep(3)
            if not re.search(check_pattern, output):
                raise Exception("Burning EEPROM failed: {}".format(tlv_name))

@logThis
def writeFanControlValue():
    prepare_config_cmd = """
cat >{}  <<'EOF'""".format("/root/diag/configs/fru-def-eeprom")
    prepare_config_cmd += """
[bia]
mfg_datetime = 12885120
manufacturer = CELESTICA
serial_number = R0000-X0000-00XX0123456789
part_number = R0000-X0000-012345
EOF
    """
    run_command(prepare_config_cmd)
    cmd_list = ["cd /root/diag",
                "export LD_LIBRARY_PATH=/root/diag/output",
                "export CEL_DIAG_PATH=/root/diag",
                "./cel-eeprom-test --dump -t fru -d 1",
                "cat /root/diag/configs/fru-def-eeprom",
                "./cel-eeprom-test -w -t fru -d 3 -f configs/fru-def-eeprom"
            ]
    output = run_command(cmd_list)
    CommonLib.execute_check_dict(Const.DUT, "", patterns_dict=fail_dict,
            check_output=output, is_negative_test=True)


@logThis
def checkFanControlValue():
    origin_dict = {
            "manufacturer" : "(.*?)$",
            "serial_number" : "(.*?)$",
            "part_number"   : "(.*?)$"
            }
    #V1.0.6
    check_dict = {
            #"Board Mfg Date" : "",
            "Board Mfg" : "(.*?)$",
            "Board Serial" : "(.*?)$",
            "Board Part Number" : "(.*?)$"
            }
    get_origin_config = "cat /root/diag/configs/fru-def-eeprom"
    get_new_config = "./cel-eeprom-test -r -t fru -d 3 -D 213"
    origin_config =  run_command(get_origin_config)
    new_config = run_command(get_new_config)
    origin_cfg_dict = CommonLib.parseDict(output=origin_config, pattern_dict=origin_dict, sep_field="=")
    if not origin_cfg_dict:
        raise Exception("Didn't get origin configuration.")
    new_cfg_dict = CommonLib.parseDict(output=new_config, pattern_dict=check_dict)
    if not new_cfg_dict:
        raise Exception("Didn't get modified configuration.")

    for key, value in new_cfg_dict.items():
        if value not in origin_cfg_dict.values():
            raise Exception("The value of {} is not as expected.".format(key))


@logThis
def checkHWInfo():
    expected_data = {
        "CPU"    : "16",
        "memory" : "7712",
        "OS"     : "Linux CEL-DiagOS 4.9.124+ #1 SMP PREEMPT Thu Jun 29 06:35:31 UTC 2023 aarch64 aarch64 aarch64 GNU/Linux",
        "UBOOT"  : CommonLib.get_swinfo_dict("UBOOT").get("newVersion", "NotFound"),
        "ONIE"   : CommonLib.get_swinfo_dict("ONIE_Installer").get("newVersion", "NotFound")
    }
    check_dict = {
            "CPU"    : "The number of processors configured is:\s+(\d+)",
            "memory" : "The memory\s+size\s+(\d+)\s+MB,",
            "OS"     : "--- Linux kernel version ---\s*\n(.*?)\n",
            "UBOOT"  : "ver=(.*?)\n",
            "ONIE"   : "ONIE\s+(\d+)",
            }
    cmd_list = ["cd /root/diag",
                "export LD_LIBRARY_PATH=/root/diag/output",
                "export CEL_DIAG_PATH=/root/diag",
                "./cel-system-test --all",
                "fw_printenv ver",
                "get_versions"
                ]
    output = run_command(cmd_list)
    if "tianhe" in devicename.lower():
        error_count = 0
        pass_pattern = "Sys test : Passed"
        cpu_pattern = r'The number of processors configured is:\s+(\d)'
        cpu_expect = '8'
        memory_pattern = r'The memory size (\d+) MB, Free Mem: (\d+) MB'
        memory_expect = 7500
        disk_pattern = r'Disk /dev/sda: (\d+)\.0 GB'
        disk_expect = '240'
        linux_kernel_pattern = r'Linux diagos-host\s+([\d.]+)\+'
        linux_kernel_expect = '5.10.90'
        device_pattern_lst = [cpu_pattern, memory_pattern, disk_pattern, linux_kernel_pattern]
        device_expect_lst = [cpu_expect, memory_expect ,disk_expect, linux_kernel_expect]
        #get expect fw version
        cpldObj = CommonLib.get_swinfo_dict("CPLD")
        ascObj = CommonLib.get_swinfo_dict("1PPS_ASC")
        sysCpldVer = cpldObj.get("newVersion", "NotFound").get("SYSCPLD", "NotFound")
        led1CpldVer = cpldObj.get("newVersion", "NotFound").get("SWLEDCPLD1", "NotFound")
        led2CpldVer = cpldObj.get("newVersion", "NotFound").get("SWLEDCPLD2", "NotFound")
        comeCpldVer = cpldObj.get("newVersion", "NotFound").get("COMECPLD", "NotFound")
        fanCpldVer = cpldObj.get("newVersion", "NotFound").get("FANCPLD", "NotFound")
        ppsVer = ascObj.get('1pps', "NotFound")
        asc0Ver = ascObj.get("newVersion", "NotFound").get('ASC10-0', "NotFound")
        asc1Ver = ascObj.get("newVersion", "NotFound").get('ASC10-1', "NotFound")
        asc2Ver = ascObj.get("newVersion", "NotFound").get('ASC10-2', "NotFound")
        asc3Ver = ascObj.get("newVersion", "NotFound").get('ASC10-3', "NotFound")
        asc4Ver = ascObj.get("newVersion", "NotFound").get('ASC10-4', "NotFound")
        ubootVer = CommonLib.get_swinfo_dict("UBOOT").get("newVersion", "NotFound")
        onieVer = CommonLib.get_swinfo_dict("ONIE_Installer").get("newVersion", "NotFound")
        diagVer = CommonLib.get_swinfo_dict("DIAGOS").get("newVersion", "NotFound")
        expectFwVerDict = {
            'SYSCPLD': sysCpldVer,
            'COMECPLD': comeCpldVer,
            'SWLEDCPLD1': led1CpldVer,
            'SWLEDCPLD2': led2CpldVer,
            'FANCPLD': fanCpldVer,
            '1PPSFPGA': ppsVer,
            'U-BOOT': ubootVer,
            'ONIE': onieVer,
            'DIAGOS': diagVer,
            'ASC10-0': asc0Ver,
            'ASC10-1': asc1Ver,
            'ASC10-2': asc2Ver,
            'ASC10-3': asc3Ver,
            'ASC10-4': asc4Ver
        }
        getFwVerDict = {}
        fw_pattern = [
            '(SYSCPLD)\s+(0x\d+)',
            '(COMECPLD)\s+(0x\d+)',
            '(SWLEDCPLD1)\s+(0x\d+)',
            '(SWLEDCPLD2)\s+(0x\d+)',
            '(FANCPLD)\s+(\d)',
            '(1PPSFPGA)\s+(0x\d+)',
            '(U-BOOT)\s+(U-Boot.*ONIE\s+[\d.]+)',
            '(ONIE)\s+([\d.]+)',
            '(DIAGOS)\s+(\d+)',
            '(ASC10-0)\s+(\w+)',
            '(ASC10-1)\s+(\w+)',
            '(ASC10-2)\s+(\w+)',
            '(ASC10-3)\s+(\w+)',
            '(ASC10-4)\s+(\w+)'
        ]
        #start to check
        if pass_pattern in output:
            log.success('Run system test all pass.')
        else:
            error_count += 1
            log.fail('Run system test all fail.')
        for i in range(0, len(device_pattern_lst)):
            res = re.search(device_pattern_lst[i], output)
            if res:
                getValue = res.group(1)
                if i == 1:
                    if int(getValue) > int(device_expect_lst[i]):
                        log.success('Check [%s] pass.' % str(res.group(0)))
                    else:
                        error_count += 1
                        log.fail('Check [%s] fail' % str(res.group(0)))
                else:
                    if str(getValue) == str(device_expect_lst[i]):
                        log.success('Check [%s] pass.'%str(res.group(0)))
                    else:
                        error_count += 1
                        log.fail('Check [%s] fail'%str(res.group(0)))
            else:
                error_count += 1
                log.fail('Can not match device info.')
        for line in output.splitlines():
            line = line.strip()
            for pattern in fw_pattern:
                mat = re.search(pattern, line)
                if mat:
                    getKey = mat.group(1)
                    getValue = mat.group(2)
                    getFwVerDict[getKey] = getValue
                    break
        log.info('#### Get the fw version: %s ####'%str(getFwVerDict))
        for key, value in getFwVerDict.items():
            if expectFwVerDict[key] == value:
                log.success('Check fw [%s] version [%s] is pass'%(key, value))
            else:
                error_count += 1
                log.fail('Check fw fail, GetVer: %s, expectVer: %s.'%(value, expectFwVerDict[key]))
        if error_count:
            raise Exception('Failed run checkHWInfo.')
    else:
        check_data = CommonLib.parseDict(output=output, pattern_dict=check_dict,
            use_value_pattern=True, line_mode=False)
        check_data.update({ "OS": check_data.get("OS", "NotFound")[:50]})
        for key, value in expected_data.items():
            if check_data[key] not in value:
                raise Exception("Information of {} is mismatch, \ncurrent: \n{}, \nexpeceted: \n{}".format(key,
                check_data[key], value))


@logThis
def checkSDKVersion():
    expected_data = {
        "SDK"         : CommonLib.get_swinfo_dict("SDK").get('newVersion', "NotFound"),
        "IFCS"        : CommonLib.get_swinfo_dict("SDK").get("IFCS", "NotFound").get('newVersion', "NotFound"),
        "releaseDate" : CommonLib.get_swinfo_dict("SDK").get("IFCS", "NotFound").get('releaseDate', "NotFound")
    }

    cmd_list = ["cat ReadMe", "./auto_load_user.sh", "ifcs show version"]
    output = run_command("cd /root/sdk/*_SDK")
    if re.search("No such file", output):
        raise Exception("Didn't found SDK PATH")
    SDK_PROMT = "IVM.*?>|" + device.promptDiagOS
    output = run_command(cmd_list, prompt=SDK_PROMT, timeout=60)
    run_command("quit")

    for each in expected_data:
        required = CommonLib.escapeString(expected_data[each])
        if not re.search(required, output):
            raise Exception("{} version is not as expected.\nRequired {}.\n".format(each, expected_data[each]))

@logThis
def checkPCIEFirmwareVersion():
    output = run_command("cd /root/sdk/*_SDK")
    if re.search("No such file", output):
        raise Exception("Didn't found SDK PATH")
    SDK_PROMT = "IVM.*?>"
    cmd_list = ["./auto_load_user.sh", "diagtest serdes aapl 1 0 'aapl serdes -display'"]
    pattern = 'Firmware: 0x10A5_208D_003'
    output = run_command(cmd_list, prompt=SDK_PROMT, timeout=60)
    run_command("quit")
    if not re.search(pattern, output):
        raise Exception("Check PCIE Firmware version failed.")

@logThis
def checkOnieVersion():
    expected_data = {
        "UBOOT"  : CommonLib.get_swinfo_dict("UBOOT").get("newVersion", "NotFound"),
        "ONIE"   : CommonLib.get_swinfo_dict("ONIE_Installer").get("newVersion", "NotFound")
        }

    check_dict = {"UBOOT"  : "ver=(.*?)\n","ONIE"   : "ONIE\s+(\d+)",}
    cmd_list = ["fw_printenv ver", "get_versions"]

    output = run_command(cmd_list,prompt=device.promptOnie)
    check_data = CommonLib.parseDict(output=output, pattern_dict=check_dict,
            use_value_pattern=True, line_mode=False)

    for key, value in expected_data.items():
        if check_data[key] not in value:
            raise Exception("Information of {} is mismatch, \ncurrent: \n{}, \nexpeceted: \n{}".format(key,
                check_data[key], value))


@logThis
def faultLogSramWR(cmd_list=None, check_dict=None, cmd=None):
    if cmd:
        cmd_list = cmd

    output = run_command(cmd_list)
    CommonLib.execute_check_dict(Const.DUT, "", patterns_dict=fail_dict,
            check_output=output, is_negative_test=True)
    if not check_dict:
        check_dict = {"0xaa": "^0xaa"}
    CommonLib.execute_check_dict(Const.DUT, "", patterns_dict=check_dict,
            check_output=output)


@logThis
def fhv2FaultLogSram(cmd_list=None, pattern1=None, pattern2=None):
    output = run_command(cmd_list)
    passCount1 = 0
    passCount2 = 0
    for line in output.splitlines():
        for pa in pattern1:
            if re.search(pa, line):
                passCount1 += 1
    if passCount1 == len(pattern1):
        KapokCommonLib.bootIntoUboot()
        KapokCommonLib.bootIntoDiagOSMode()
    else:
        raise Exception("check sram info failed")
    device.sendMsg('cd /root/diag \n')
    output = run_command(cmd_list[-1])
    if pattern2:
        pattern = pattern2
    else:
        pattern = pattern1
    for line in output.splitlines():
        for pa in pattern:
            if re.search(pa, line):
                passCount2 += 1
    if passCount2 != len(pattern):
        raise Exception("check sram info failed")

@logThis
def fhv2ConsoleLogSram(cmd_list1=None, cmd_list2=None, pattern1=None, pattern2=None):
    output = run_command(cmd_list1)
    passCount1 = 0
    passCount2 = 0
    for line in output.splitlines():
        for pa in pattern1:
            if re.search(pa, line):
                passCount1 += 1
    if passCount1 == len(pattern1):
        KapokCommonLib.powerCycleToDiagOS()
    else:
        raise Exception("check sram info failed")
    device.sendMsg('cd /root/diag \n')
    output = run_command(cmd_list2)
    if pattern2:
        pattern = pattern2
    else:
        pattern = pattern1
    for line in output.splitlines():
        for pa in pattern:
            if re.search(pa, line):
                passCount2 += 1
    if passCount2 != len(pattern):
        raise Exception("check sram info failed")

@logThis
def consoleLogSramWR(param):
    check_pattern = param
    cmd_list = [
            "i2cset -y -f 15 0x60 0x41 0x01",
            "i2cset -y -f 15 0x60 0x42 0x00",
            "i2cset -y -f 15 0x60 0x43 0x00",
            "i2cset -y -f 15 0x60 0x44 0xaa",
            "i2cset -y -f 15 0x60 0x40 0x01",
            "i2cset -y -f 15 0x60 0x40 0x03",
            "i2cget -y -f 15 0x60 0x45 ",
            "cd /root/diag",
            "./cel-log-test --dump -d 2"
            ]
    faultLogSramWR(cmd_list=cmd_list, check_dict=check_pattern)


@logThis
def checkMainBoardVersionByCPLD():
    cmd_list = [
            "cd /root/diag",
            "export LD_LIBRARY_PATH=/root/diag/output",
            "export CEL_DIAG_PATH=/root/diag"
            ]
    output1 = run_command(cmd_list)
    CommonLib.execute_check_dict(Const.DUT, "", patterns_dict=fail_dict,
            check_output=output1, is_negative_test=True)
    if 'tianhe' in device.name:
        cmd_list = "./cel-cpld-test -r -d 2 -i board_version"
    else:
        cmd_list = "./cel-cpld-test -r -d 1 -i board_version"
    output = run_command(cmd_list)
    CommonLib.execute_check_dict(Const.DUT, "", patterns_dict=fail_dict,
            check_output=output, is_negative_test=True)


@logThis
#def upgradeDiagCpld(vmetool_path, vmetool):
#    get_dhcp_ip_cmd = [
#            "ifconfig -a",
#            "dhclient",
#            "ifconfig -a"
#            ]
#    run_command(get_dhcp_ip_cmd)
#    filelist = ["default_vme_list.cfg", "default_vme_list_without_tpm.cfg", "vmetool_arm"]
#    sys_cpld_file = CommonLib.get_swinfo_dict("SYS_CPLD").get("newImage", "NotFound")
#    fan_cpld_file = CommonLib.get_swinfo_dict("FAN_CPLD").get("newImage", "NotFound")
#    filelist.extend([sys_cpld_file, fan_cpld_file])
#    filepath = CommonLib.get_swinfo_dict("FAN_CPLD").get("hostImageDir", "NotFound")
#    destination_path = vmetool_path
#
#    CommonLib.tftp_get_files(Const.DUT, file_list=filelist, src_path=filepath,
#                             dst_path=destination_path)
#
#    update_sys_cmd = "{} {}".format(vmetool, sys_cpld_file)
#    update_fan_cmd = "{} -f {}".format(vmetool, fan_cpld_file)
#    cmd_dict = OrderedDict({"SYS_CPLD": update_sys_cmd, "FAN_CPLD": update_fan_cmd})
#    pass_pattern = {"| PASS! |": "\|\s+PASS!\s+\|"}
#    for item, cmd in cmd_dict.items():
#        try:
#            CommonLib.execute_check_dict(Const.DUT, cmd, patterns_dict=pass_pattern,
#                    path=vmetool_path, timeout=400)
#        except:
#            raise Exception("Upgrade {} failed.".format(item))


@logThis
def upgradeDiagCpld(vmetool_path, vmetool):
    device.sendMsg("cd /root/fw/ \n")
    device.sendMsg("pkill cel-fan-test \n")
    sys_cpld_file = CommonLib.get_swinfo_dict("SYS_CPLD").get("newImage", "NotFound")
    led_cpld_file = CommonLib.get_swinfo_dict("SWLED_CPLD").get("newImage", "NotFound")
    fan_cpld_file = CommonLib.get_swinfo_dict("FAN_CPLD").get("newImage", "NotFound")
    devicename = os.environ.get("deviceName", "")
    if 'tianhe' in device.name:
        come_cpld_file = CommonLib.get_swinfo_dict("COME_CPLD").get("newImage", "NotFound")
        i2cfpga_cpld_file = CommonLib.get_swinfo_dict("1PPS_FPGA").get("newImage", "NotFound")
        update_come_cmd = "{} -c {}".format(vmetool, come_cpld_file)
        device.sendMsg(update_come_cmd)
        device.sendMsg("\n")
        device.read_until_regexp(r'\|\s+PASS!\s+\|', timeout=180)
    if "fenghuangv2" in device.name:
        dev_type = DeviceMgr.getDevice(devicename).get('cardType')
        if dev_type == '1PPS':
            FPGA_type = dev_type + '_FPGA'
            i2cfpga_cpld_file = CommonLib.get_swinfo_dict(FPGA_type).get("newImage", "NotFound")
        else:
            FPGA_type = 'I2C_FPGA'
            i2cfpga_cpld_file = CommonLib.get_swinfo_dict(FPGA_type).get("newImage", "NotFound")
    update_sys_cmd = "{} -s {}".format(vmetool, sys_cpld_file)
    update_led_cmd = "{} -l {}".format(vmetool, led_cpld_file)
    update_fan_cmd = "{} -f {}".format(vmetool, fan_cpld_file)
    update_i2cfpga_cmd = "flashcp -v {} /dev/mtd5".format(i2cfpga_cpld_file)
    device.sendMsg(update_i2cfpga_cmd)
    device.sendMsg("\n")
    device.read_until_regexp(r'Verifying .*: .*\/.* \(100%\)', timeout=600)
    cmd_dict = OrderedDict({"SYS_CPLD": update_sys_cmd,
                            "SWLED_CPLD": update_led_cmd,
                            "FAN_CPLD": update_fan_cmd})
    pass_pattern = {"| PASS! |": "\|\s+PASS!\s+\|"}
    for item, cmd in cmd_dict.items():
        try:
            CommonLib.execute_check_dict(Const.DUT, cmd, patterns_dict=pass_pattern,
                    path=vmetool_path, timeout=400)
        except:
            raise Exception("Upgrade {} failed.".format(item))

@logThis
def checkcpldversion():
    led1_cpld_version = CommonLib.get_swinfo_dict("CPLD").get("newVersion").get("SWLEDCPLD1","NotFound")
    led2_cpld_version = CommonLib.get_swinfo_dict("CPLD").get("newVersion").get("SWLEDCPLD2","NotFound")
    sys_cpld_version = CommonLib.get_swinfo_dict("CPLD").get("newVersion").get("SYSCPLD", "NotFound")
    fan_cpld_version = CommonLib.get_swinfo_dict("CPLD").get("newVersion").get("FANCPLD", "NotFound")
    check_syscpld_cmd = "cat /sys/bus/i2c/drivers/celestica-cpld/*-0060/cpld_version"
    check_led1cpld_cmd = "cat /sys/bus/i2c/drivers/celestica-cpld/*-0063/cpld_version"
    check_led2cpld_cmd = "cat /sys/bus/i2c/drivers/celestica-cpld/*-0064/cpld_version"
    check_fancpld_cmd = "cat /sys/bus/i2c/drivers/fan_cpld/*-0066/cpld_version"
    devicename = os.environ.get("deviceName", "")
    if 'tianhe' in device.name:
        come_cpld_version = CommonLib.get_swinfo_dict("COME_CPLD").get("newVersion", "NotFound")
        i2cfpga_cpld_version = CommonLib.get_swinfo_dict("1PPS_FPGA").get("newVersion", "NotFound")
        check_comecpld_cmd = "cat /sys/bus/i2c/drivers/come-cpld/*-0060/cpld_version"
        check_i2cfpga_cpld_cmd = "cat /sys/devices/xilinx/pps-i2c/version"
        comeoutput = run_command(check_comecpld_cmd)
        if re.search(come_cpld_version, comeoutput, re.IGNORECASE):
            log.success("Come_Version is: " + come_cpld_version)
        else:
            raise Exception("Come Cpld Version check Failed")
    if "fenghuangv2" in device.name:
        dev_type = DeviceMgr.getDevice(devicename).get('cardType')
        if dev_type == '1PPS':
            FPGA_type = dev_type + '_FPGA'
            i2cfpga_cpld_version = CommonLib.get_swinfo_dict(FPGA_type).get("newVersion", "NotFound")
            check_i2cfpga_cpld_cmd = "cat /sys/devices/xilinx/pps-i2c/version"
        else:
            FPGA_type = 'I2C_FPGA'
            i2cfpga_cpld_version = CommonLib.get_swinfo_dict(FPGA_type).get("newVersion", "NotFound")
            check_i2cfpga_cpld_cmd = "cat /sys/devices/xilinx/accel-i2c/version"
    sysoutput = run_command(check_syscpld_cmd)
    led1output = run_command(check_led1cpld_cmd)
    led2output = run_command(check_led2cpld_cmd)
    fanoutput = run_command(check_fancpld_cmd)
    ppsoutput = run_command(check_i2cfpga_cpld_cmd)
    if re.search(sys_cpld_version, sysoutput, re.IGNORECASE):
        log.success("Sys_Version is: " + sys_cpld_version)
    else:
        raise Exception("Sys Cpld Version check Failed")
    if re.search(led1_cpld_version, led1output, re.IGNORECASE):
        log.success("Led1_Version is: " + led1_cpld_version)
    else:
        raise Exception("Led1 Cpld Version check Failed")
    if re.search(led2_cpld_version, led2output, re.IGNORECASE):
        log.success("Led2_Version is: " + led2_cpld_version)
    else:
        raise Exception("Led2 Cpld Version check Failed")
    if re.search(fan_cpld_version, fanoutput, re.IGNORECASE):
        log.success("Fan_Version is: " + fan_cpld_version)
    else:
        raise Exception("Fan Cpld Version check Failed")
    if re.search(i2cfpga_cpld_version, ppsoutput, re.IGNORECASE):
        log.success("I2C_FPGA_Version is: " + i2cfpga_cpld_version)
    else:
        raise Exception("I2C FPGA Version check Failed")


@logThis
def setUbootIP():
    device_ip = CommonLib.Get_Not_Occupied_IP()
    cmd = "setenv ipaddr {}".format(device_ip)
    output = "fail"
    if device_ip:
        output = run_command(cmd, prompt=device.promptUboot)

    CommonLib.execute_check_dict(Const.DUT, "", patterns_dict=fail_dict,
            check_output=output, is_negative_test=True)


@logThis
def runSsdStressTest():
    cmd_list = [
            "cd /root/tools/stress_test",
            "./ssd_test.sh",
            ]
    output = run_command(cmd_list, timeout=600)

    CommonLib.execute_check_dict(Const.DUT, "", patterns_dict=fail_dict,
            check_output=output, is_negative_test=True)



@logThis
def verifyFanCtrlTest(path, tool_name, option, pattern):
    command = 'cd ' + path + '\n'
    device.sendMsg(command)
    command = Const.KEY_CTRL_C
    cmd = './' + tool_name + ' ' + option + '\n'
    device.sendMsg(cmd)
    try:
        for j in range(0, 3):
            for i in range(0, len(pattern)):
                j += 1
                device.read_until_regexp(pattern[i], timeout=60)
    except:
        device.sendMsg(command)
        raise Exception("can't find fan speed log info" )
    # send Ctrl-C
    device.sendMsg(command)
    if 'tianhe' in devicename.lower():
        device.read_until_regexp('.*diagos.*')
    else:
        device.read_until_regexp('.*DiagOS.*')

@logThis
def verifyDdrStressTest(cmd, regexp, pattern_dict):
    device.sendMsg(cmd)
    output = device.read_until_regexp(regexp, timeout=60)
    CommonLib.execute_check_dict('DUT', cmd="", mode=None, patterns_dict=pattern_dict, timeout=60, line_mode=True, check_output=output)


@logThis
def fhv2DiagdownloadImagesAndRecoveryDiagOS():
    INSTALLER_MODE_DETECT_PROMPT = 'discover: installer mode detected'
    RECOVERY_DIAG_PATTERN = {"installer mode detected": "installer mode detected"}
    diagos_file_name = CommonLib.get_swinfo_dict("DIAGOS").get("newImage")
    hostImageDir = CommonLib.get_swinfo_dict("DIAGOS").get("hostImageDir")
    diagos_file = ["{}/{}".format(hostImageDir,diagos_file_name)]
    CommonLib.tftp_get_files(Const.DUT, file_list=diagos_file, dst_path="/root", timeout=400)
    install_diagos_cmd = "onie-nos-install {}".format(diagos_file_name)
    #output = device.sendCmdRegexp(install_diagos_cmd, INSTALLER_MODE_DETECT_PROMPT, timeout=900)
    #CommonLib.execute_check_dict("DUT", "", patterns_dict=RECOVERY_DIAG_PATTERN, timeout=60, check_output=output)
    device.sendCmdRegexp(install_diagos_cmd, KapokConst.STOP_AUTOBOOT_PROMPT, timeout=900)
    # device.read_until_regexp(KapokConst.STOP_AUTOBOOT_PROMPT, timeout=300)
    device.sendMsg(KapokConst.STOP_AUTOBOOT_KEY)
    device.sendCmdRegexp('run diag_bootcmd', 'Please press Enter to activate this console', timeout=900)
    device.sendMsg('\n')

@logThis
def fhv2DiagdownloadstressAndRecoveryDiagOS():
    stress_file=["fenghuangv2/stress_test.tar.xz"]
    fail_dict = {"fail": "fail",
                 "ERROR": "ERROR",
                 "Failure": "Failure",
                 "cannot read file": "cannot read file",
                 "command not found": "command not found",
                 "No such file": "No such file",
                 "not found": "not found",
                 "Unknown command": "Unknown command",
                 "No space left on device": "No space left on device",
                 "Command exited with non-zero status": "Command exited with non-zero status"
                 }
    if 'tianhe' in device.name:
        run_command("udhcpc", timeout=20)
    else:
        run_command("dhclient", timeout=20)
    run_command("mkdir /root/tools")
    CommonLib.tftp_get_files(Const.DUT, dst_path="/root/tools",file_list=stress_file, timeout=400)
    cmd_list = ["tar -xf stress_test.tar.xz"]
    output = run_command(cmd_list, timeout=300)
    CommonLib.execute_check_dict("DUT", "", patterns_dict=fail_dict, timeout=10,
                                 check_output=output, is_negative_test=True)

def getDhcpIP(interface="eth0", mode=Const.BOOT_MODE_DIAGOS):
    log.debug("Entering OnieLib class procedure: getDhcpIP")
    fail_dict = {"fail": "fail",
                 "ERROR": "ERROR",
                 "Failure": "Failure",
                 "cannot read file": "cannot read file",
                 "command not found": "command not found",
                 "No such file": "No such file",
                 "not found": "not found",
                 "Unknown command": "Unknown command",
                 "No space left on device": "No space left on device",
                 "Command exited with non-zero status": "Command exited with non-zero status"
                 }

    if 'tianhe' in device.name:
        cmd = 'udhcpc'
    else:
        cmd = "dhclient"
    CommonLib.execute_check_dict('DUT', cmd, mode=mode, patterns_dict=fail_dict,
                                 timeout=15, is_negative_test=True)

@logThis
def run_asc_update_test():

    device.sendMsg("dhclient" + '\r\n')
    devicename = os.environ.get("deviceName", "")
    if "fenghuangv2" in devicename.lower():
        dev_type = DeviceMgr.getDevice(devicename).get('cardType')
        if dev_type == '1PPS':
            ASC_type = dev_type + '_ASC'
        else:
            ASC_type = 'I2C_ASC'
    destination_path = CommonLib.get_swinfo_dict(ASC_type).get("localImageDir", "NotFound")
    filelist = ["Phoenix_ASC0.hex", "Phoenix_ASC1.hex"]
    asc_path = CommonLib.get_swinfo_dict(ASC_type).get("hostImageDir", "NotFound")
    CommonLib.tftp_get_files(Const.DUT, file_list=filelist, src_path=asc_path, dst_path=destination_path)
    device.sendMsg("cd ../fw" + '\r\n')
    asc3_index = verify_asc3_exist('ls')
    log.info('asc3 exist %s' % asc3_index)
    asc_update_cmd0 = 'asc_fwupd_arm -w --bus 21 --addr 0x60 -f Phoenix_ASC0.hex --force'
    asc_update_cmd1 = 'asc_fwupd_arm -w --bus 21 --addr 0x61 -f Phoenix_ASC1.hex --force'
    asc_update_cmd2 = 'asc_fwupd_arm -w --bus 21 --addr 0x62 -f Phoenix_ASC2.hex --force'
    asc_update_cmd_list = []
    if asc3_index == 'yes':
        asc_update_cmd_list = [
            asc_update_cmd0, asc_update_cmd1, asc_update_cmd2
        ]
    else:
        asc_update_cmd_list = [
            asc_update_cmd0, asc_update_cmd1
        ]
    for asc_cmd in asc_update_cmd_list:
        passcount = 0
        output = CommonLib.execute_command(asc_cmd)
        keywords_pattern = ['\[100\%\]', 'PASS']
        for pattern in keywords_pattern:
            match = re.search(pattern, output)
            if match:
                passcount += 1

        if passcount == len(keywords_pattern):
            log.success("ASC command {} test Passed!".format(asc_cmd))
        else:
            raise Exception("ASC command {} test Failed!".format(asc_cmd))

@logThis
def verify_asc3_exist(asc_cmd):

    output = CommonLib.execute_command(asc_cmd)
    true_message = 'Phoenix_ASC2.hex'
    count = ''
    if true_message in output:
        count = 'yes'
    else:
        count = 'no'

    return count

@logThis
def check_asc_version():

    device.sendMsg('cd /root/fw' + '\r\n')
    index = verify_asc3_exist('ls')
    log.info('asc3 exist %s ' % index)
    check_asc_cmd = []
    if index == 'yes':
        check_asc_cmd = ['asc_fwupd_arm -r --bus 21 --addr 0x60',
                         'asc_fwupd_arm -r --bus 21 --addr 0x61',
                         'asc_fwupd_arm -r --bus 21 --addr 0x62']
    else:
        check_asc_cmd = ['asc_fwupd_arm -r --bus 21 --addr 0x60',
                         'asc_fwupd_arm -r --bus 21 --addr 0x61']
    for cmd in check_asc_cmd:
        output = CommonLib.execute_command(cmd)
        match = re.search('fail|error', output, re.I)
        if not match:
            log.success("check asc {} version test Passed!".format(cmd))
        else:
            raise Exception("check asc {} version test Passed!".format(cmd))

@logThis
def checkversionbeforethetest():
    sys_cpld_version = CommonLib.get_swinfo_dict('CPLD').get('newVersion').get('SYSCPLD')
    cpld_dict = CommonLib.get_swinfo_dict('CPLD')
    led_cpld1_version = cpld_dict.get('newVersion').get('SWLEDCPLD1')
    led_cpld2_version = cpld_dict.get('newVersion').get('SWLEDCPLD2')
    fan_cpld = cpld_dict.get('newVersion').get('FANCPLD')
    uboot_version = CommonLib.get_swinfo_dict("UBOOT").get("newVersion", "NotFound")
    uboot_version = uboot_version.replace('(', '\(')
    uboot_version = uboot_version.replace(')', '\)')
    uboot_version = uboot_version.replace('+', '\+')
    log.cprint(uboot_version)
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
        come_cpld_version = cpld_dict.get('newVersion').get('COMECPLD', "NotFound")
        asc10_0 = CommonLib.get_swinfo_dict('1PPS_ASC').get("newVersion", "NotFound").get("ASC10-0")
        asc10_1 = CommonLib.get_swinfo_dict('1PPS_ASC').get("newVersion", "NotFound").get("ASC10-1")
        asc10_2 = CommonLib.get_swinfo_dict('1PPS_ASC').get("newVersion", "NotFound").get("ASC10-2")
        asc10_3 = CommonLib.get_swinfo_dict('1PPS_ASC').get("newVersion", "NotFound").get("ASC10-3")
        asc10_4 = CommonLib.get_swinfo_dict('1PPS_ASC').get("newVersion", "NotFound").get("ASC10-4")
        ppsfpga = CommonLib.get_swinfo_dict('1PPS_ASC').get("1pps", "NotFound")
        hw_dict = {
            'ASC10-0': asc10_0,
            'ASC10-1': asc10_1,
            'ASC10-2': asc10_2,
            'ASC10-3': asc10_3,
            'ASC10-4': asc10_4,
            '1PPSFPGA': ppsfpga
        }
        cpld_version_dict = {
            'SYSCPLD': sys_cpld_version,
            'COMECPLD': come_cpld_version,
            'SWLEDCPLD1': led_cpld1_version,
            'SWLEDCPLD2': led_cpld2_version,
            'U-BOOT': uboot_version,
            'ONIE': onie_version,
            'FANCPLD': fan_cpld
        }
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
            passpattern.append(keys_list[i] + '.*' + values_list[i])
    else:
        log.fail("get versions is failed")
        device.raiseException("Failure while get versions info")
    log.debug('passpattern=%s' % passpattern)
    passCount = 0
    fail_pattern = []

    for pattern in passpattern:
        found = False
        for line in output.splitlines():
            if re.search(pattern, line, re.IGNORECASE):
                log.debug('the matched version:%s' % line)
                found = True
                passCount += 1
                break
        if not found:
            fail_pattern.append(pattern.replace('.*', ': '))
    if passCount == len(passpattern):
        log.success("verify version is passed")
    else:
        log.fail("verify versions failed, not matched version: {}".format(str(fail_pattern)))
        device.raiseException("Failure while verify versions info")



@logThis
def checkdriverversion(pattern):
    check_driver_cmd = "lsmod"
    output = device.executeCmd(check_driver_cmd)
    CommonLib.execute_check_dict("DUT", "", patterns_dict=pattern, timeout=60,
                                check_output=output)
@logThis
def EraseSysCpldImage():
    if 'tianhe' in device.name:
        cmd_list=["cd /root/fw","udhcpc",
                  "tftp -g 192.168.0.5 -r /tianhe/fw/fhv2_sys_cpld_erase.vme",
                  "vmetool_arm -s fhv2_sys_cpld_erase.vme"]
    else:
        cmd_list=["cd /root/fw","vmetool_arm -s cs8260_sys_cpld_erase.vme"]
    output=run_command(cmd_list)
    pass_pattern ="{'| PASS! |': '\|\s+PASS!\s+\|'}"
    cpld_match=re.search(pass_pattern,output);
    if not cpld_match:
        raise Exception("SYS CPLD erase Image failed");
    else:
        log.success("erase cpld image successfully");

    KapokCommonLib.powerCycleToDiagOS()   

@logThis
def checkSysCpldVersion():
    sys_cpld_version = CommonLib.get_swinfo_dict('SYS_CPLD').get('initializeImage')
    if 'tianhe' in device.name:
        export_cmd_list=["cd /root/fw","i2cget -f -y 19 0x60 0x00"]
    else:
        export_cmd_list=["cd /root/fw","i2cget -f -y 8 0x60 0x00"]
    output=run_command(export_cmd_list)
    if re.search(sys_cpld_version,output,re.IGNORECASE):
        log.success("Sys_Version is: " +sys_cpld_version)
        return sys_cpld_version
    else:
        raise Exception("Sys Cpld Version check Failed")

@logThis
def restoreSysCpldImage():
    sys_cpld_file = CommonLib.get_swinfo_dict('SYS_CPLD').get('newImage','NotFound')
    update_sys_cmd = "vmetool_arm -s {}".format(sys_cpld_file)
    output2 = run_command(update_sys_cmd)
    pass_pattern = "{'| PASS! |': '\|\s+PASS!\s+\|'}"
    cpld_match=re.search(pass_pattern,output2)
    if not cpld_match:
       raise Exception("Restore Failed")
    else:
       log.success("Passed")
    KapokCommonLib.powerCycleToDiagOS()

@logThis
def verifyCpldVersion():
    if 'tianhe' in device.name:
        export_cmd_list="i2cget -f -y 19 0x60 0x00"
    else:
        export_cmd_list="i2cget -f -y 8 0x60 0x00"
    output1=run_command(export_cmd_list)
    output2= CommonLib.get_swinfo_dict('SYS_CPLD').get('newVersion')

    if re.search(output2,output1,re.IGNORECASE):
       log.success("CPLD Version matched")
    else:
       raise Exception("Version Match Failed")


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
        output = device.sendCmdRegexp(updater_cmd, finish_prompt, timeout=1200)
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
def diskl():
    cmd_list = ["fdisk -l"]
    output = run_command(cmd_list, prompt=device.promptDiagOS,timeout=10)
    CommonLib.execute_check_dict("DUT", "", patterns_dict=fail_dict, timeout=10, check_output=output, is_negative_test=True)
    output = run_command("smartctl -i /dev/sda", prompt=device.promptDiagOS, timeout=10)
    pass_pattern = "(current: 6.0 Gb/s)"
    if pass_pattern not in output:
        raise Exception("Sata link up speed not found to be 6.0Gbps.")

@logThis
def judgeTheTypeOfLoopback():
    output = run_command('cd /root/diag')
    if re.search("No such file", output):
        raise Exception("Didn't found DIAG PATH")
    judge_cmd = './cel-sfp-test --all'
    string = ''
    pattern = 'Vendor[ \t]+Name[ \t]+\:[ \t]+AWS'
    pattern2 = 'Vendor[ \t]+Name[ \t]+\:[ \t]+LEONI'
    output2 = CommonLib.execute_command(judge_cmd, timeout=120)
    match1 = re.search(pattern, output2)
    match2 = re.search(pattern2,output2)
    if match1:
        string = "AWS"
        return string
    elif match2:
        string = 'LEONI'
        return string
    else:
        raise Exception('No loopback!, please check!')

@logThis
def fruEepromAccessTest():
    output = run_command('cd /root/diag')
    if re.search("(No such file|can't cd)", output):
        raise Exception("Didn't found DIAG PATH")
    for i in range(1, 12):
        cmd = './cel-eeprom-test -r -t fru -d ' + str(i) + '\n'
        output = device.executeCmd(cmd)
        if re.search('.ERROR.', output):
            log.fail('check fru eeprom failed')
            raise Exception('check fru eeprom failed')
        else:
            log.info('run fruEepromAccessTest pass')

@logThis
def qsfpPageSelectAndRead():
    error_count = 0
    loopback_str = judgeTheTypeOfLoopback()
    if loopback_str == "AWS":
        for i in range(101,133):
            get_cmd = 'i2cget -y -f ' + str(i)+ " 0x50 0x41"
            pass_pattern = r'^0x\w+'
            output1 = CommonLib.execute_command(get_cmd,timeout=60)
            time.sleep(1)
            for line in output1.splitlines():
                line = line.strip()
                res = re.search(pass_pattern, line)
                if res:
                    get_hex_value = int(res.group(0), base=16)
                    pass_pattern_bin = bin(get_hex_value)
                    binValue = str(pass_pattern_bin)
                    res_bit0 = binValue[-1]
                    if res_bit0 == '0':
                        log.success('get the value is %s,bit 0 is %s' % (res.group(0), res_bit0))
                    else:
                        error_count += 1
                        log.fail('get the value is %s,bit 0 is %s' % (res.group(0), res_bit0))
        if error_count > 0:
           raise Exception('Failed run readAwsResetLStatus')
    elif loopback_str == "LEONI":
        for i in range(101,133):
            set_cmd = "i2cset -y -f " + str(i) + " 0x50 0x7f 0xff"
            CommonLib.execute_command(set_cmd, timeout=60)
            time.sleep(1)
        for i in range(101, 133):
            get_cmd = 'i2cget -y -f ' + str(i) + " 0x50 0xe1"
            pass_pattern = r'^0x\w+'
            output1 = CommonLib.execute_command(get_cmd, timeout=60)
            time.sleep(1)
            for line in output1.splitlines():
                line = line.strip()
                res = re.search(pass_pattern, line)
                if res:
                    get_hex_value = int(res.group(0), base=16)
                    pass_pattern_bin = bin(get_hex_value)
                    binValue = str(pass_pattern_bin)
                    res_bit2 = binValue[-3:-2]
                    if res_bit2 == '0':
                        log.success('get the value is %s,bit 2 is %s' % (res.group(0), res_bit2))
                    else:
                        error_count += 1
                        log.fail('get the value is %s,bit 2 is %s' % (res.group(0), res_bit2))
        if error_count > 0:
           raise Exception('Failed run readAwsResetLStatus')

@logThis
def qsfpOpticalModuleSetIntL():
    type_info = judgeTheTypeOfLoopback()
    if type_info == "LEONI":
        for i in range(101,133):
            set_cmd = "i2cset -y -f " + str(i) + " 0x50 0x7f 0xff"
            CommonLib.execute_command(set_cmd, timeout=60)
            time.sleep(1)
        for j in range(101,133):
            set_command = "i2cset -y -f " + str(j) + " 0x50 0xfe 0x20"
            CommonLib.execute_command(set_command, timeout=60)
            time.sleep(1)
            log.info("Set IntL port %s  passed." % j)
    elif type_info == "AWS":
        for m in range(101,133):
            set_command = "i2cset -y -f " + str(m) + " 0x50 0x41 0x02"
            CommonLib.execute_command(set_command, timeout=60)
            log.info("Set IntL port %s  passed." % m)

@logThis
def setAllAndSetOneByOne(param):
    set_cmd = './cel-sfp-test -w -t ' + str(param) + ' -D 1'
    CommonLib.execute_command(set_cmd, timeout=60)
    devicename = os.environ.get("deviceName", "")
    dev_type = DeviceMgr.getDevice(devicename).get('cardType')
    if dev_type == "1PPS":
        extra_cmd = "pps-i2c"
    elif dev_type == "FPGA":
        extra_cmd = "accel-i2c"
    else:
        raise Exception("Can not recognize the card_type.")
    for j in range(1, 33):
        if param == 'reset':
            sum_cmd = "echo 1 > /sys/devices/xilinx/" + extra_cmd + "/port" + str(j) + "_module_" + str(param)
        else:
            if 'tianhe' in devicename.lower():
                sum_cmd = "echo 1 > /sys/devices/xilinx/" + extra_cmd + "/port" + str(j) + "_" + str(param)
            else:
                sum_cmd = "echo 1 > /sys/devices/xilinx/" + extra_cmd + "/port" + str(j) + "_module_" + str(param)
        CommonLib.execute_command(sum_cmd, timeout=60)
        time.sleep(1)

@logThis
def unsetAllAndUnsetOneByOne(param):
    set_cmd = './cel-sfp-test -w -t ' + str(param) + ' -D 0'
    CommonLib.execute_command(set_cmd, timeout=60)
    devicename = os.environ.get("deviceName", "")
    dev_type = DeviceMgr.getDevice(devicename).get('cardType')
    if dev_type == "1PPS":
        extra_cmd = "pps-i2c"
    elif dev_type == "FPGA":
        extra_cmd = "accel-i2c"
    else:
        raise Exception("Can not recognize the card_type.")
    for j in range(1, 33):
        if param == 'reset':
            sum_cmd = "echo 0 > /sys/devices/xilinx/" + extra_cmd + "/port" + str(j) + "_module_" + str(param)
        else:
            if 'tianhe' in devicename.lower():
                sum_cmd = "echo 0 > /sys/devices/xilinx/" + extra_cmd + "/port" + str(j) + "_" + str(param)
            else:
                sum_cmd = "echo 0 > /sys/devices/xilinx/" + extra_cmd + "/port" + str(j) + "_module_" + str(param)
        CommonLib.execute_command(sum_cmd, timeout=60)
        time.sleep(1)

@logThis
def disableAllProtect():
    devicename = os.environ.get("deviceName", "")
    sizze = DeviceMgr.getDevice(devicename).get('size')
    disable_protect_cmd = []
    if sizze == '19':
        disable_protect_cmd = [
            '/sys/bus/i2c/devices/8-0060/i2cfpga_eeprom_write_protect',
            '/sys/bus/i2c/devices/23-0066/fan_board_eeprom_protect',
            '/sys/bus/i2c/devices/23-0066/fan1_eeprom_protect',
            '/sys/bus/i2c/devices/23-0066/fan3_eeprom_protect',
            '/sys/bus/i2c/devices/23-0066/fan5_eeprom_protect',
            '/sys/bus/i2c/devices/23-0066/fan7_eeprom_protect',
            '/sys/bus/i2c/devices/23-0066/fan9_eeprom_protect',
            '/sys/bus/i2c/devices/23-0066/fan11_eeprom_protect',
            '/sys/bus/i2c/devices/23-0066/fan13_eeprom_protect',
        ]
    elif sizze == '21':
        disable_protect_cmd = [
            '/sys/bus/i2c/devices/8-0060/i2cfpga_eeprom_write_protect',
            '/sys/bus/i2c/devices/23-0066/fan_board_eeprom_protect',
            '/sys/bus/i2c/devices/23-0066/fan1_eeprom_protect',
            '/sys/bus/i2c/devices/23-0066/fan3_eeprom_protect',
            '/sys/bus/i2c/devices/23-0066/fan5_eeprom_protect',
            '/sys/bus/i2c/devices/23-0066/fan7_eeprom_protect',
            '/sys/bus/i2c/devices/23-0066/fan9_eeprom_protect',
            '/sys/bus/i2c/devices/23-0066/fan11_eeprom_protect',
        ]
    elif sizze == 'SKU3':
        disable_protect_cmd = [
            '/sys/bus/i2c/devices/8-0060/i2cfpga_eeprom_write_protect',
            '/sys/bus/i2c/devices/23-0066/fan_board_eeprom_protect',
            '/sys/bus/i2c/devices/23-0066/fan1_eeprom_protect',
            '/sys/bus/i2c/devices/23-0066/fan3_eeprom_protect',
            '/sys/bus/i2c/devices/23-0066/fan5_eeprom_protect',
            '/sys/bus/i2c/devices/23-0066/fan7_eeprom_protect',
            '/sys/bus/i2c/devices/23-0066/fan9_eeprom_protect',
            '/sys/bus/i2c/devices/23-0066/fan11_eeprom_protect',
            '/sys/bus/i2c/devices/8-0060/i2cfpga_eeprom_write_protect'
        ]
    for i in range(0,len(disable_protect_cmd)):
        output = CommonLib.execute_command('echo 0 > '+disable_protect_cmd[i], timeout=60)
        fail_pattern = '\-bash\:.*?Permission denied'
        match = re.search(fail_pattern, output)
        if match:
            device.raiseException("Failure with disable %s " % disable_protect_cmd[i])
        else:
            log.info("Disable protect %s pass." % disable_protect_cmd[i])

@logThis
def readFanControlValue():
    path = '/root/diag'
    CommonLib.execute_command('cd ' + path)
    devicename = os.environ.get("deviceName", "")
    type = DeviceMgr.getDevice(devicename).get('cardType')
    default_list = []
    cycle_list=[]
    if type == '1PPS':
        cycle_list = ['1','2','3','4','5','6','7','8','9','11','12']
    elif type == 'FPGA':
        cycle_list = ['1','2','3','4','5','6','7','8','9','11']
    else:
        device.raiseException('Can not obtain the card_type.')
    log.info("///////cycle_list=%s/////////" % cycle_list)
    for cycle_num in cycle_list:
        read_cmd = './cel-eeprom-test -r -t fru -d ' + cycle_num
        output = CommonLib.execute_command(read_cmd,timeout=60)
        log.info('--------output=%s---------' % output)
        for line in output.splitlines():
            line = line.strip()
            if 'Board' in line or 'Product' in line:
                line = line.split(' :')[1]
                fin_line = line.strip()
                log.info('.....fin_line = %s .......' % fin_line)
                default_list.append(fin_line)
                log.info('.......default_list = %s .......' % default_list)
        spec_string = 'Extra'
        if spec_string in output:
            prepare_config_cmd = """
            cat >{}  <<'EOF'""".format("/root/diag/configs/fru-def-eeprom")
            prepare_config_cmd += """
            [bia]
            mfg_datetime = 12883158
            manufacturer = CELESTICA
            serial_number = R1276-G0006-01FH0520220236
            part_number = R0000-X0000-012345
            [pia]
            manufacturer = AVC
            part_number = R1276-FN021-020AW
            serial_number = DFPK0456B2GY053L23C002138
            product_custom_1 = 0 RPM
            product_custom_2 = 24700 RPM
            EOF
                """
        else:
            prepare_config_cmd = """
            cat >{}  <<'EOF'""".format("/root/diag/configs/fru-def-eeprom")
            prepare_config_cmd += """
            [bia]
            mfg_datetime = 12885120
            manufacturer = CELESTICA
            serial_number = R0000-X0000-00XX0123456789
            part_number = R0000-X0000-012345
            EOF
                """
        run_command(prepare_config_cmd)
        device.sendMsg(Const.KEY_CTRL_C) 
        time.sleep(2)
        output_again = run_command(read_cmd)
        if 'R0000-X0000-012345' in output_again:
            log.info('cycle port %s pass!' % cycle_num)
            #restore default value
            restore_cmd = './cel-eeprom-test -w -t fru -d '+cycle_num+' -f configs/fru-def-eeprom'
            restore_output = CommonLib.execute_command(restore_cmd,timeout=60)
            if restore_cmd != output_again:
                log.info('Restored port %s successfully.' % cycle_num)
        else:
            device.raiseException('cycle port %s modify failed! please check output!' % cycle_num)

@logThis
def pageSelectAndSetHighmode():
    for i in range(101,133):
        page_select_command = 'i2cset -y -f ' + str(i) + ' 0x50 0x7f 0x00'
        set_high_power_command = 'i2cset -y -f ' +str(i) + ' 0x50 0xc8 0x80'
        CommonLib.execute_command(page_select_command,timeout=60)
        time.sleep(1)
        CommonLib.execute_command(set_high_power_command,timeout=60)

@logThis
def pageSelectAndSetHighmodeNew():
    for i in range(101, 133):
        page_select_command = 'i2cset -y -f ' + str(i) + ' 0x50 0x7f 0xff'
        CommonLib.execute_command(page_select_command, timeout=60)
        time.sleep(1)

@logThis
def readAwsResetLStatus(pattern):
    error_count = 0
    for i in range(101, 133):
        pass_pattern = r'^0x\w+'
        read_cmd = 'i2cget -y -f ' + str(i) + ' 0x50 0x41'
        output = CommonLib.execute_command(read_cmd, timeout=60)
        for line in output.splitlines():
            line = line.strip()
            res = re.search(pass_pattern, line)
            if res:
                get_hex_value = int(res.group(0), base=16)
                pass_pattern_bin = bin(get_hex_value)
                binValue = str(pass_pattern_bin)
                res_bit1 = binValue[-2:-1]
                if (pattern == '0x1'):
                    if res_bit1 == '0':
                        log.success('get the value is %s,bit 1 is %s' % (res.group(0), res_bit1))
                    else:
                        error_count += 1
                        log.fail('get the value is %s,bit 1 is %s' % (res.group(0), res_bit1))
                else:
                    if res_bit1 == '1':
                        log.success('get the value is %s,bit 1 is %s' % (res.group(0), res_bit1))
                    else:
                        error_count += 1
                        log.fail('get the value is %s,bit 1 is %s' % (res.group(0), res_bit1))
    if error_count > 0:
        raise Exception('Failed run readAwsResetLStatus')

@logThis
def readAwsLPModeStatus(pattern):
    error_count = 0
    for i in range(101, 133):
        pass_pattern = r'^0x\w+'
        read_cmd = 'i2cget -y -f ' + str(i) + ' 0x50 0x41'
        output = CommonLib.execute_command(read_cmd, timeout=60)
        for line in output.splitlines():
            line = line.strip()
            res = re.search(pass_pattern, line)
            if res:
                get_hex_value = int(res.group(0), base=16)
                pass_pattern_bin = bin(get_hex_value)
                binValue = str(pass_pattern_bin)
                res_bit2 = binValue[-3:-2]
                if (pattern == '0x1'):
                    if res_bit2 == '1':
                        log.success('get the value is %s,bit 2 is %s' % (res.group(0), res_bit2))
                    else:
                        error_count += 1
                        log.fail('get the value is %s,bit 2 is %s' % (res.group(0), res_bit2))
                else:
                    if res_bit2 == '0':
                        log.success('get the value is %s,bit 2 is %s' % (res.group(0), res_bit2))
                    else:
                        error_count += 1
                        log.fail('get the value is %s,bit 2 is %s' % (res.group(0), res_bit2))
    if error_count > 0:
        raise Exception('Failed run readAwsResetLStatus')

@logThis
def opticalModuleautoTest(path, tool_name, pattern, is_cmd=False, timeout=120):
    time.sleep(2)
    if path:
        cmd = 'cd ' + path
        run_command(cmd, prompt=device.promptDiagOS)
    if not is_cmd:
        cmd = './' + tool_name
    else:
        cmd = tool_name
    output = device.executeCmd(cmd)
    log.cprint(output)
    CommonKeywords.should_match_ordered_regexp_list(output, pattern)
    log.success("QSFP Optical Module Signal Eric_ELB tset is passed")

@logThis
def readLeoniLPModeStatus(pattern):
    error_count = 0
    for i in range(101,133):
        pass_pattern = r'^0x\w+'
        read_cmd = 'i2cget -y -f ' + str(i) + ' 0x50 0xe1'
        output = CommonLib.execute_command(read_cmd, timeout=60)
        for line in output.splitlines():
            line = line.strip()
            res = re.search(pass_pattern, line)
            if res:
                get_hex_value = int(res.group(0), base=16)
                pass_pattern_bin = bin(get_hex_value)
                binValue = str(pass_pattern_bin)
                res_bit1 = binValue[-2:-1]
                if (pattern == '0x1'):
                    if res_bit1 == '1':
                        log.success('get the value is %s,bit 1 is %s' % (res.group(0), res_bit1))
                    else:
                        error_count += 1
                        log.fail('get the value is %s,bit 1 is %s' % (res.group(0), res_bit1))
                else:
                    if res_bit1 == '0':
                        log.success('get the value is %s,bit 1 is %s' % (res.group(0), res_bit1))
                    else:
                        error_count += 1
                        log.fail('get the value is %s,bit 1 is %s' % (res.group(0), res_bit1))
    if error_count > 0:
        raise Exception('Failed run readAwsResetLStatus')

@logThis
def readLeoniResetLStatus(pattern):
    for i in range(101,133):
        read_cmd = 'i2cget -y -f ' + str(i) + ' 0x50 0xe1'
        output = CommonLib.execute_command(read_cmd, timeout=60)
        pass_pattern = pattern
        match = re.search(pass_pattern, output)
        if match:
            log.info("set or unset port %s pass." % str(i))
        else:
            raise Exception("set or unset port %s fail." % str(i))

@logThis
def checkIntLSignalStatus(pattern):
    check_all_port_status_command = './cel-sfp-test --show -t present'
    all_match_pattern = '\d{2}[ \t]+\|[ \t]+port\-\d{2}.*Present.*?'
    all_output = CommonLib.execute_command(check_all_port_status_command, timeout=60)
    all_match = re.search(all_match_pattern, all_output)
    if all_match:
        log.info("Command ./cel-sfp-test --show -t present check all port status passed!")
    else:
        raise Exception("Command ./cel-sfp-test --show -t present check all port status failed!")
    devicename = os.environ.get("deviceName", "")
    dev_type = DeviceMgr.getDevice(devicename).get('cardType')
    if dev_type == "1PPS":
        extra_cmd = "pps-i2c"
        count = 0
        for i in range(1,33):
            sum_cmd = "cat /sys/devices/xilinx/" + extra_cmd + "/port"+ str(i) + "_module_interrupt"
            output = CommonLib.execute_command(sum_cmd,timeout=60)
            pass_pattern = pattern
            for line in output.splitlines():
                line = line.strip()
                match = re.search(pass_pattern,line)
                if match:
                    count += 1
        if count == 0:
            raise Exception("Existing Port Status value is 0, please check it.")
    elif dev_type == "FPGA":
        extra_cmd = "accel-i2c"
        count = 0
        for j in range(1, 33):
            sum_cmd = "cat /sys/devices/xilinx/" + extra_cmd + "/port" + str(j) + "_module_interrupt"
            output = CommonLib.execute_command(sum_cmd, timeout=60)
            pass_pattern = pattern
            for line in output.splitlines():
                line = line.strip()
                match = re.search(pass_pattern, line)
                if match:
                    count += 1
        if count == 0:
            raise Exception("Existing Port Status value is 0, please check it.")
    else:
        raise Exception("Card_Type from Swimage file no exist")

@logThis
def qsfpI2cPageSelectAndClear():
    loopback_str = judgeTheTypeOfLoopback()
    if loopback_str == "AWS":
        for i in range(101,133):
            clear_cmd = 'i2cset -y -f ' + str(i) + ' 0x50 0x41 0x12'
            CommonLib.execute_command(clear_cmd, timeout=60)
    elif loopback_str == "LEONI":
        for j in range(101,133):
            page_select_cmd = 'i2cset -y -f ' + str(j) + ' 0x50 0x7f 0xff'
            CommonLib.execute_command(page_select_cmd, timeout=60)
        for m in range(101,133):
            clear_cmd = 'i2cset -y -f ' + str(m) + ' 0x50 0xfe 0x30'
            CommonLib.execute_command(clear_cmd, timeout=60)
    else:
        raise Exception("Can not gain the loopback type. please check it with command ./cel-sfp-test --all under /root/diag.")


@logThis
def pcieBusTest():
    if not KapokCommonLib.is1ppsCard():
        log.info('This operation only supported on 1pps card!')
        return
    device.sendMsg('cd /root/diag \n')
    output = CommonLib.exec_cmd("./cel-pci-test --all")
    CommonKeywords.should_match_a_regexp(output, 'PCIe test : Passed')
    log.info('pcieBusTest successfully.')

@logThis
def tpmDeviceAccessTest():
    output = run_command('cd /root/diag')
    if re.search("(No such file|can't cd)", output):
        raise Exception("Didn't found DIAG PATH")
    tpmDeviceAccess = CommonLib.exec_cmd("./cel-tpm-test --all")
    CommonKeywords.should_match_a_regexp(tpmDeviceAccess, 'TPM test : Passed')
    log.info('TPM Device Access Test: To check vendor id, device id and the presence of TPM device is successful.')

@logThis
def cpuSDRAccessTest():
    output = run_command('cd /root/diag')
    if re.search("No such file", output):
        raise Exception("Didn't found DIAG PATH")
    cpuSDRAccess = CommonLib.exec_cmd("al_sdr_dump")
    CommonKeywords.should_match_a_regexp(cpuSDRAccess, 'Finished readig SDR data from uC')
    log.info('CPU SDR Access Test:Reading SDR data from uC successful.')

@logThis
def rovFunctionalTest():
    output = run_command('cd /root/diag')
    if re.search("No such file", output):
        raise Exception("Didn't found DIAG PATH")
    rovFunction = CommonLib.exec_cmd("./cel-rov-test --all")
    CommonKeywords.should_match_a_regexp(rovFunction, 'rov test : Passed')
    log.info('ROV Functional Test: To check the actual VDD core output against the target ROV is successful.')

@logThis
def reloadFPGA():
    if not KapokCommonLib.is1ppsCard():
        log.info('This operation only supported on 1pps card!')
        return
    output = run_command('cd /root/diag')
    if re.search("No such file", output):
        raise Exception("Didn't found DIAG PATH")
    fpgareload = CommonLib.exec_cmd("fpga_reload")
    CommonKeywords.should_match_a_regexp(fpgareload, 'Found ...')
    CommonKeywords.should_match_a_regexp(fpgareload, 'Check FPGA...i2c_accel_fpga')
    match = re.search('fail|error', fpgareload, re.I)
    if not match:
        log.success("Reload FPGA successful")
    else:
        raise Exception("Reload FPGA unsuccessful")

@logThis
def checkFPGAFunctionAfterReset():
    output = run_command('cd /root/diag')
    if re.search("No such file", output):
        raise Exception("Didn't found DIAG PATH")
    time.sleep(10)
    pciTest = CommonLib.exec_cmd("./cel-pci-test --all")
    CommonKeywords.should_match_a_regexp(pciTest, 'PCIe test : Passed')
    log.info('PCI test successful')
    sfpTest = CommonLib.exec_cmd("./cel-sfp-test --all")
    CommonKeywords.should_match_a_regexp(sfpTest, 'SFP test : Passed')
    log.info('SFP test successful')
    log.info('FPGA function after reset successful')

@logThis
def checkFpgaBramAccess():
    if not KapokCommonLib.is1ppsCard():
        log.info('This operation only supported on 1pps card!')
        return
    output = run_command('cd /root/diag/output')
    if re.search("No such file", output):
        raise Exception("Didn't found DIAG PATH")
    fpgaBramAccess = CommonLib.exec_cmd("./fpga_bram_access.sh")
    CommonKeywords.should_match_a_regexp(fpgaBramAccess, 'FPGA BRAM READ/WRITE TEST : Passed')
    log.info('FPGA BRAM READ/WRITE TEST successful')

@logThis
def checkI2cRtcIrqStatus():
    if not KapokCommonLib.is1ppsCard():
        log.info('This operation only supported on 1pps card!')
        return
    output = run_command('cd /root/diag/output')
    if re.search("No such file", output):
        raise Exception("Didn't found DIAG PATH")
    rtcstatus = CommonLib.exec_cmd("./fpga_test_irq_i2c_rtc_irq.sh")
    CommonKeywords.should_match_a_regexp(rtcstatus, 'RTC \(Done\) Interrupt test : Passed')
    CommonKeywords.should_match_a_regexp(rtcstatus, 'RTC \(Error\) Interrupt test : Passed')
    log.info('I2C RTC Status/RTC Interrupt Mask/PCIe MSI status/MSI IRQ status test successful')

@logThis
def readAllFpgaRegisters():
    if not KapokCommonLib.is1ppsCard():
        log.info('This operation only supported on 1pps card!')
        return
    output = run_command('cd /root/diag/output')
    if re.search("No such file", output):
        raise Exception("Didn't found DIAG PATH")
    fpgabar0 = CommonLib.exec_cmd("./fpga_bar_dump.sh 0")
    fpgabar1 = CommonLib.exec_cmd("./fpga_bar_dump.sh 1")
    fpgabar2 = CommonLib.exec_cmd("./fpga_bar_dump.sh 2")
    fpgabar3 = CommonLib.exec_cmd("./fpga_bar_dump.sh 3")
    match0= re.search('fail|error', fpgabar0, re.I)
    if not match0:
        log.success("Reading fpgabar0 is successful")
    else:
        raise Exception("Reading fpgabar0 is unsuccessful")
    match1= re.search('fail|error', fpgabar1, re.I)
    if not match1:
        log.success("Reading fpgabar1 is successful")
    else:
        raise Exception("Reading fpgabar1 is unsuccessful")
    match2= re.search('fail|error', fpgabar2, re.I)
    if not match2:
        log.success("Reading fpgabar2 is successful")
    else:
        raise Exception("Reading fpgabar2 is unsuccessful")
    match3= re.search('fail|error', fpgabar2, re.I)
    if not match3:
        log.success("Reading fpgabar3 is successful")
    else:
        raise Exception("Reading fpgabar3 is unsuccessful")
    log.info('Read all FPGA registers successfully without error')

@logThis
def checkQsfpIrqStatus():
    if not KapokCommonLib.is1ppsCard():
        log.info('This operation only supported on 1pps card!')
        return
    loopback_str = judgeTheTypeOfLoopback()
    output = run_command('cd /root/diag/output')
    if re.search("No such file", output):
        raise Exception("Didn't found DIAG- PATH")
    if loopback_str == "AWS":
        qsfpirqstatus = CommonLib.exec_cmd("./fpga_test_irq_qsfp_irq.sh")
    elif loopback_str == "LEONI":
        qsfpirqstatus = CommonLib.exec_cmd("./fpga_test_irq_qsfp_irq.sh leoni")
    CommonKeywords.should_match_a_regexp(qsfpirqstatus, 'QSFP Interrupt test : Passed')
    log.info('QSFP Interrupt/Interrupt Mask register/PCIe MSI status/MSI IRQ status successful')

@logThis
def checkQsfpPresentInterruptStatus():
    if not KapokCommonLib.is1ppsCard():
        log.info('This operation only supported on 1pps card!')
        return
    loopback_str = judgeTheTypeOfLoopback()
    output = run_command('cd /root/diag/output')
    if re.search("No such file", output):
        raise Exception("Didn't found DIAG- PATH")
    if loopback_str == "AWS":
        qsfpirqstatus = CommonLib.exec_cmd("./fpga_test_irq_qsfp_present_irq.sh")
        CommonKeywords.should_match_a_regexp(qsfpirqstatus, 'QSFP Present Interrupt test : Passed')
    elif loopback_str == "LEONI":
        qsfpirqstatus = CommonLib.exec_cmd("./fpga_test_irq_qsfp_present_irq.sh leoni")
        CommonKeywords.should_match_a_regexp(qsfpirqstatus, 'QSFP Present Interrupt test : Passed')
    log.info('QSFP_Present_INTERRUPT/Present_interrupt_Mask_REGISTER/PCIe_MSI_status/MSI_IRQ_Status successful')

@logThis
def flashFpgaImage():
    if not KapokCommonLib.is1ppsCard():
        log.info('This operation only supported on 1pps card!')
        return
    filelist = CommonLib.get_swinfo_dict("1PPS_FPGA").get("newImage")
    filelists = [filelist]
    destination_path = CommonLib.get_swinfo_dict("1PPS_FPGA").get("localImageDir", "NotFound")
    asc_path = CommonLib.get_swinfo_dict("1PPS_FPGA").get("hostImageDir", "NotFound")
    CommonLib.check_ip_address(Const.DUT, 'eth0','DIAGOS')
    CommonLib.tftp_get_files(Const.DUT, file_list=filelists, src_path=asc_path, dst_path=destination_path)
    device.sendMsg("cd " + destination_path + '\r\n')
    path = CommonLib.execute_command("pwd")
    mtd_path = '/dev/mtd6'
    update_command = 'flashcp -v ' + filelist + ' ' + mtd_path
    output = device.executeCmd(update_command, timeout=300)
    pattern = [
        r'Erasing blocks.*?\(100\%\)',
        r'Writing data.*?\(100\%\)',
        r'Verifying data.*?\(100\%\)'
    ]
    pass_count = 0
    for line in output.splitlines():
        line = line.strip()
        for i in range(len(pattern)):
            match = re.search(pattern[i], line)
            if match:
                pass_count += 1
    log.info("passcount=%s" % pass_count)
    if pass_count >= len(pattern):
        log.info("Flash FPGA image Success!")
    else:
        log.fail("Flash FPGA image failed!")

@logThis
def checkFpgaIncludeInDev():
    if not KapokCommonLib.is1ppsCard():
        log.info('This operation only supported on 1pps card!')
        return
    output = CommonLib.exec_cmd("cat /proc/mtd")
    CommonKeywords.should_match_a_regexp(output, 'fpga')
    log.info('FPGA included in dev')

@logThis
def checkFpgaVersion():
    if not KapokCommonLib.is1ppsCard():
        log.info('This operation only supported on 1pps card!')
        return
    output = CommonLib.execute_command("cat /sys/devices/xilinx/pps-i2c/version")
    match = re.search("(fail|error)", output, re.I)
    if match:
        log.fail("log failed, FPGA version check failed ")
        raise Exception("log failed, FPGA version check failed")
    log.info('FPGA version check successful')

@logThis
def detect_all_PCIe_devices():
    run_command("cd /root/diag", prompt=device.promptDiagOS, timeout=5)
    pass_ptn = ""
    output = run_command("./cel-pci-test --all", prompt=device.promptDiagOS, timeout=10)
    if pass_ptn not in output:
        raise Exception("PCIE Detect test failed.\nNot found the pattern\n" + pass_ptn)

@logThis
def check_CPU_Riser_Card():
    device.sendMsg("echo $((`i2cget -f 19 0x60 0x09` & 0x80)) \n")
    device.read_until_regexp(".*Continue.*", timeout=5)
    output = run_command("y", prompt=device.promptDiagOS, timeout=10)
    if "0" not in output:
        raise Exception("Riser card status command did not return 0.")


@logThis
def check_all_PSU_status():
    pass_ptn = "PSU Test : Passed"
    output = run_command('cd /root/diag')
    if re.search("No such file", output):
        raise Exception("Didn't found DIAG PATH")

    output = run_command("./cel-psu-test --all", prompt=device.promptDiagOS, timeout=10)
    if pass_ptn not in output:
        raise Exception("PSU all test failed.")


@logThis
def show_all_PSU_values():
    pass_ptn = "DC-busbar present"
    output = run_command("./cel-psu-test --show", prompt=device.promptDiagOS, timeout=10)
    if pass_ptn not in output:
        raise Exception("Show PSU test failed.")

@logThis
def show_PSU1_values():
    pass_ptn = "DC-busbar present"
    output = run_command("./cel-psu-test -r -d 1", prompt=device.promptDiagOS, timeout=10)
    if pass_ptn not in output:
        raise Exception("Show PSU1 test failed.")
@logThis
def show_All_Fan_PWM_RPM():
    pass_ptn = "Fan test : Passed"
    output = run_command('cd /root/diag')
    if re.search("No such file", output):
        raise Exception("Didn't found DIAG PATH")

    output = run_command("./cel-fan-test --all", prompt=device.promptDiagOS, timeout=30)
    if pass_ptn not in output:
        raise Exception("FAN --all test failed.")

@logThis
def show_Fan_PWM_RPM(pattern):
    output = run_command("./cel-fan-test --show", prompt=device.promptDiagOS, timeout=10)
    CommonKeywords.should_match_ordered_regexp_list(output, pattern)
    log.info("Fan show test passed.")

@logThis
def set_All_FAN_PWM(pwm):
    cmd = "./cel-fan-test -w -t " + pwm
    run_command(cmd, prompt=device.promptDiagOS, timeout=10)

@logThis
def set_All_lpmode_power_mode(typeValue, option):
    cmd = './' + var.spi_test_tool + option + typeValue
    device.executeCmd(cmd)

@logThis
def read_lpmode_pin_status(bitSite, pattern, i2cTool, i2cOption):
    p1 = r'^0x\w+'
    error_count = 0
    for i in range(101, 133):
        time.sleep(1)
        cmd = i2cTool + str(i) + i2cOption
        # output = device.executeCmd(cmd)
        output = CommonLib.execute_command(cmd, timeout=60)
        for line in output.splitlines():
            line = line.strip()
            res = re.search(p1, line)
            if res:
                get_hex_value = int(res.group(0), base=16)
                pass_pattern_bin = bin(get_hex_value)
                binValue = str(pass_pattern_bin)
                bitLocal = int(bitSite)
                bitLocalBefore = bitLocal - 1
                startNum = int('-' + bitSite)
                endNum = int('-' + str(bitLocalBefore))
                bitRes= binValue[startNum:endNum]   #[-3:-2]
                if bitRes == pattern:
                    log.success('get the loopback-%s lpmode bin status value [%s] pass.'% (str(i)[1:], bitRes))
                else:
                    error_count += 1
                    log.fail('get the loopback-%s lpmode bin status value is %s, expect value is %s' % (str(i)[1:], bitRes, pattern))
    if error_count > 0:
        raise Exception('Failed run read_lpmode_pin_status')

@logThis
def set_lpmode_power_one_by_one(powerMode, i2cTool, i2cOption):
    for i in range(1, 33):
        time.sleep(1)
        cmd = 'echo ' + powerMode + ' > ' + i2cTool + str(i) + i2cOption
        device.executeCmd(cmd)

@logThis
def eric_lpmode_auto_test(lpmodeTool, register_pattern):
    switch_folder_path(var.tpm_output_path)
    cmd = './' + lpmodeTool
    output = device.executeCmd(cmd)
    if re.search(register_pattern, output):
        log.success('Check lpmode auto test pass.')
    else:
        log.fail('Check lpmode auto test fail.')
        raise Exception('Failed run eric_lpmode_auto_test.')

@logThis
def dump_tpm_test(path, tool, pattern):
    p1 = r'TPM MFG =\s+(\w+)'
    switch_folder_path(path)
    cmd = './' + tool
    output = device.executeCmd(cmd)
    res = re.search(p1, output)
    if res.group(1) == pattern:
        log.success('Check dump tpm pass.')
    else:
        raise Exception('Failed run dump_tpm_test')

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


@logThis
def hotswap_interrupt_test(tool, pattern):
    if ('tianhe_d04' in device.name) or ('tianhe_d05' in device.name):
        pass_count = 0
        error_count = 0
        p1 = r'0x\w+'
        cmd = './' + tool
        output = run_command(cmd, prompt=device.promptDiagOS, timeout=30)
        for line in output.splitlines():
            line = line.strip()
            res = re.search(p1, line)
            if res:
                pass_count += 1
                getValue = res.group(0)
            get_hex_value = int(getValue, base=16)
            get_bin_value = bin(get_hex_value)
            binValue = str(get_bin_value)
            res_bit1 = binValue[-1]
            log.info('======= Get the binary value is %s'%binValue)
            if int(res_bit1) == int(pattern):
                log.success('Check hotswap interrupt test pass, get the bit1 value is %s!' % res_bit1)
            else:
                error_count += 1
                log.fail('Check hotswap interrupt test fail, get the bit1 value is %s, expect value is %s!' % (res_bit1, pattern))
        if error_count or pass_count == 0:
            raise Exception('Failed run hotswap_interrupt_test!')
    else:
        log.info('It\'s only support tianhe V48 unit, other unit skip!!!')

@logThis
def set_ltc4287_alert_test(cmd):
    if ('tianhe_d04' in device.name) or ('tianhe_d05' in device.name):
        run_command(cmd, prompt=device.promptDiagOS, timeout=30)
    else:
        log.info('It\'s only support tianhe V48 unit, other unit skip!!!')

@logThis
def check_byte_burst_test(option1, option2, singleLst):
    p1 = r'SFP test : Passed'
    error_count = 0
    # single_lst = [1, 2, 8 ,16]
    for k in singleLst:
        for i in range(1, 33):
            cmd = './' + option1 + str(k) + ' -d ' + str(i) + ' ' + option2
            output = CommonLib.execute_command(cmd, timeout=60)
            if p1 not in output:
                error_count += 1
                log.fail('Check single-%d port-%d test fail'%(k, i))
    if error_count:
        raise Exception('Failed run check_byte_burst_test')

@logThis
def change_i2c_bus_speed(cmd):
    CommonLib.execute_command(cmd, timeout=60)

@logThis
def check_qsfp_real_time_access_test(cmd):
    pass_count = 0
    error_count = 0
    p1 = '(port|sfp)-(\d+) : (\w+)'
    output = CommonLib.execute_command(cmd, timeout=300)
    for line in output.splitlines():
        line = line.strip()
        res = re.search(p1, line)
        if res:
            portNum = res.group(2)
            getValue = res.group(3)
            if getValue == 'Passed':
                pass_count += 1
            else:
                error_count += 1
                log.fail('Check Port/sfp-%s real time access fail!'%portNum)
    if error_count or (pass_count != 34):
        raise Exception('Failed run check_qsfp_real_time_access_test!')


