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
import os
import sys
import re
import Logger as log
import CRobot
from Decorator import *
from time import sleep
from datetime import datetime
from crobot.Decorator import logThis

workDir = CRobot.getWorkDir()
sys.path.append(workDir)
sys.path.append(os.path.join(workDir, 'common', 'commonlib'))
sys.path.append(os.path.join(workDir, 'platform/ali'))
import CommonLib
from common.commonlib import CommonKeywords
import AliConst
from crobot import Const
import AliCommonLib
import AliCommonVariable as commonVar
from AliOpenBmcVariable import *
from SwImage import SwImage

try:
    import DeviceMgr
except Exception as err:
    log.cprint(str(err))

device = DeviceMgr.getDevice()

if 'shamu' in devicename:
    from AliOpenBmcShamuVariable import *

@logThis
def bmcConnect():
    device.loginBmc()
    return

@logThis
def bmcDisconnect():
    device.disconnect()
    return

@logThis
def loadOpenbmcUtils():
    return device.executeCmd('source /usr/local/bin/openbmc-utils.sh', commonVar.openbmc_mode)

@logThis
def changeToRootUserMode():
    device.getPrompt(commonVar.diagos_mode)
    device.sendCmd("sudo su\n")
    device.getPrompt(commonVar.diagos_mode)
    device.flush()

@logThis
def exitFromRootUserMode():
    device.getPrompt(commonVar.diagos_mode)
    device.sendCmd("exit\n")
    device.getPrompt(commonVar.diagos_mode)
    device.flush()

@logThis
def parseOneGroupKeyword(regex, output):
    match = re.search(regex, output)
    if match and match.group(1):
        log.success("Found: %s"%(match.group(1)))
        return match.group(1).strip()
    log.fail("Not found keyword: %s"%(regex))
    return ""

@logThis
def parseSimpleKeyword(regex, output, ignore_case=False):
    if ignore_case:
        match = re.search(regex, output, re.IGNORECASE)
    else:
        match = re.search(regex, output)
    if match:
        log.info("Found: %s"%(match.group(0)))
        return match.group(0).strip()
    log.info("Not found keyword: %s"%(regex))
    return ""

@logThis
def parseLineIntoDictionary(regex, output):
    outDict = {}
    for line in output.splitlines():
        line = line.strip()
        match = re.search(regex, line)
        if match:
            key = match.group(1).strip()
            outDict[key] = match.group(2).strip()
    log.info(outDict)
    return outDict

@logThis
def parseSensors(regex, output):
    regex = r'(.+):\s+([+|-]?\d+.\d+)\s+\w+.*min\s*=\s*([+|-]?\d+.\d+).*max\s*=\s*([+|-]?\d+.\d+)'
    outDict = {}
    for line in output.splitlines():
        line = line.strip()
        match = re.search(regex, line)
        if match:
            key = match.group(1).strip()
            outDict[key] = (match.group(2).strip(), match.group(3).strip(), match.group(4).strip())
    log.info(outDict)
    return outDict



def parseGetFanSpeed(output):
    p1 = r'Fan (\d+) RPMs: (\d+), (\d+), \((\d+)\%\)'
    outDict = {}
    for line in output.splitlines():
        line = line.strip()
        match = re.search(p1, line)
        if match:
            fan_name = 'Fan ' + match.group(1)
            outDict[fan_name + ' front'] = match.group(2)
            outDict[fan_name + ' rear'] = match.group(3)
            outDict[fan_name + ' percentage'] = match.group(4)
    # log.info(outDict)
    return outDict

@logThis
def verifyCurrentBootFlash(fw_type, boot_flash, boot_status='OK'):
    err_count = 0
    if fw_type.upper() == "BMC":
        output = device.executeCmd('boot_info.sh', commonVar.openbmc_mode)
        parsed_output = parseOneGroupKeyword(bmc_flash_pattern, output)
    elif fw_type.upper() == "BIOS":
        loadOpenbmcUtils()
        output = device.executeCmd('come_boot_info', commonVar.openbmc_mode)
        parsed_status = parseOneGroupKeyword(come_status_pattern, output)
        if parsed_status == boot_status:
            log.success("COMe boot status match: %s, %s" %(boot_status, parsed_status))
        else:
            log.fail("COMe boot status mismatch: %s, %s"%(boot_status, parsed_status))
            err_count += 1
        parsed_output = parseOneGroupKeyword(bios_flash_pattern, output)
    if parsed_output.lower() == boot_flash.lower():
        log.success("verifyCurrentBootFlash match: %s, %s" %(boot_flash, parsed_output))
    else:
        log.fail("verifyCurrentBootFlash mismatch: %s, %s"%(boot_flash, parsed_output))
        err_count += 1
    if err_count:
        device.raiseException("verifyCurrentBootFlash")

@logThis
def switchBmcFlash(bmc_flash):
    cmd = "boot_from " + bmc_flash.lower()
    loadOpenbmcUtils()
    output = device.executeCmd(cmd, commonVar.openbmc_mode)
    p2 = 'Current boot source is %s, no need to switch.'%(bmc_flash.lower())
    match2 = re.search(p2, output)
    if match2:
        log.info("switch bmc flash to %s" %(bmc_flash.lower()))
        verifyCurrentBootFlash("bmc", bmc_flash)
    else:
        log.info("###### switch bmc flash to %s ######" %(bmc_flash.lower()))
        ### rebooting
        device.receive('Starting kernel ...', timeout=AliConst.BOOT_TIME)
        device.sendline()
        device.getPrompt(commonVar.openbmc_mode, timeout=AliConst.BOOT_TIME)
        sleep(40)
        verifyCurrentBootFlash("bmc", bmc_flash)

@logThis
def switchBiosFlash(bios_flash, timeout=AliConst.BOOT_TIME):
    #### come_reset master
    cmd = "come_reset " + bios_flash.lower() + "\n"
    loadOpenbmcUtils()
    device.executeCmd(cmd, commonVar.openbmc_mode)
    device.trySwitchToCpu()
    device.receive('System Reset', timeout=180)
    output = device.receive('sonic login:', timeout=timeout)
    device.getPrompt(commonVar.diagos_mode, timeout=timeout)
    sleep(10)
    verifyCurrentBootFlash("bios", bios_flash)
    return output

@logThis
def updateBmc(bmc_flash="master", isUpgrade=True, forceUpdate=False):
    imageObj = SwImage.getSwImage(SwImage.BMC)
    version = {}
    version[SwImage.BMC_VER] = imageObj.newVersion if isUpgrade else imageObj.oldVersion

    if (not forceUpdate) and (not verifyFwVersion(SwImage.BMC, version, "need_update")):
        log.info("Already at version " +  version[SwImage.BMC_VER] + ", no need to update.")
        return 0, version[SwImage.BMC_VER]

    log.info("###### need to update bmc to version %s ######" %(version[SwImage.BMC_VER]))
    log.info("###### check MAC address of eth0 ######")
    verifyMacAddress(default_interface)
    log.info("###### online update bmc ######")
    onlineUpdateFw("bmc", bmc_flash, isUpgrade)
    return 1, version[SwImage.BMC_VER]

@logThis
def updateBmcCrash(bmc_flash="master"):
    log.info("###### online update bmc ######")
    imageObj = SwImage.getSwImage("BMC")
    image_path = imageObj.localImageDir + '/' + imageObj.newImage
    flash_path = slave_dev if bmc_flash.lower() == "slave" else master_dev
    cmd = 'flashcp -v ' + image_path + ' /dev/' + flash_path

    ###### start flashing ######
    device.getPrompt(commonVar.openbmc_mode)
    device.sendCmd(cmd)
    device.read_until_regexp(bmc_crash_pattern, 1200)

    ###### send CTRL+C ######
    device.sendCmd(Const.KEY_CTRL_C)
    device.getPrompt(commonVar.openbmc_mode)

    sleep(5)

@logThis
def updateBios(bios_flash="master",isUpgrade=True, forceUpdate=False):
    imageObj = SwImage.getSwImage(SwImage.BIOS)
    version = {}
    parsed = {}
    version[SwImage.BIOS_VER] = imageObj.newVersion if isUpgrade else imageObj.oldVersion

    if (not forceUpdate) and (not verifyFwVersion(SwImage.BIOS, version, "need_update")):
        log.info("Already at version " +  version[SwImage.BIOS_VER] + ", no need to update.")
        return
    log.info("###### need to update bios to version %s ######" %(version[SwImage.BIOS_VER]))
    log.info("###### online update bios ######")
    onlineUpdateFw("bios", bios_flash, isUpgrade)

    if bios_flash.lower() == 'slave':
        log.info("###### switch to slave bios ######")
        output = switchBiosFlash('slave')
    else:
        log.info("###### Power cycle sonic and check version ######")
        output = AliCommonLib.powerCycleSonic(commonVar.diagos_mode)

    verifyLogWithKeywords(bios_boot_pattern, output)
    parsed[SwImage.BIOS_VER] = parseOneGroupKeyword(bios_boot_version_pattern, output)
    err_count = CommonLib.compare_input_dict_to_parsed(parsed, version)
    if err_count:
        log.fail("BIOS version in POST message mismatch, found: %s, expected: %s"%(parsed[SwImage.BIOS_VER], version[SwImage.BIOS_VER]))
    else:
        log.success("BIOS version in POST message match: %s, %s"%(parsed[SwImage.BIOS_VER], version[SwImage.BIOS_VER]))
    sleep(5)
    log.info("###### check version in CPU OS ######")
    verifyFwVersion(SwImage.BIOS, version)

    if bios_flash.lower() == 'slave':
        log.info("###### Power cycle and check version ######")
        AliCommonLib.powerCycleToOpenbmc(timeout=600)
        verifyCurrentBootFlash("BIOS", "master")
        verifyFwVersion(SwImage.BMC, bmc_version_dict)
        verifyFwVersion(SwImage.BIOS, bios_version_dict)

@logThis
def updateBiosCrash():
    log.info("###### update BIOS with USB device ######")
    ### AfuEfix64.efi bios.bin /p /b /n /me /x
    cmd = '%s %s /p /b /n /me /x'%(afu_new_image, bios_image)

    ###### prepare tool ######
    AliCommonLib.bootIntoUefiMode()
    device.sendCmd('cls')
    device.sendCmdRegexp("FS0:", AliConst.PROMPT_UEFI, timeout=30)
    device.sendMsg('\r\n')
    output = device.sendCmdRegexp("dir", r'Dir\(s\)', timeout=30)
    if (afu_new_image in output) and (bios_image in output):
        ###### start flashing ######
        device.flush()
        device.sendCmd('cls')
        device.sendMsg('\r\n')
        sleep(2)
        #### @WORKAROUND send cmd by sending one character at a time to avoid characters missing issue
        for c in cmd:
            device.sendMsg(c)
            sleep(0.5)
        device.sendMsg('\r\n')
        output = device.read_until_regexp(bios_crash_pattern, timeout=600)

        ###### power cycle while flashing ######
        device.powerCycleDevice()
        device.trySwitchToBmc()
        device.getPrompt(Const.BOOT_MODE_OPENBMC, timeout=300)
        sleep(30)
    else:
        log.fail("Not found tool or bios image")
        device.raiseException("Failure while update bios crash")

@logThis
def updateCpld(isUpgrade=True):
    version = {}
    version[BASE_CPLD_KEY] = BASE_CPLD.newVersion if isUpgrade else BASE_CPLD.oldVersion
    version[COME_CPLD_KEY] = COME_CPLD.newVersion if isUpgrade else COME_CPLD.oldVersion
    version[FAN_CPLD_KEY] = FAN_CPLD.newVersion if isUpgrade else FAN_CPLD.oldVersion
    version[SWITCH_CPLD1_KEY] = SWITCH_CPLD.newVersion if isUpgrade else SWITCH_CPLD.oldVersion
    version[SWITCH_CPLD2_KEY] = SWITCH_CPLD.newVersion if isUpgrade else SWITCH_CPLD.oldVersion
    if 'migaloo' in devicename:
        version[TOPLINE_CPLD1_KEY] = SWITCH_CPLD.newVersion if isUpgrade else SWITCH_CPLD.oldVersion
        version[TOPLINE_CPLD2_KEY] = SWITCH_CPLD.newVersion if isUpgrade else SWITCH_CPLD.oldVersion
        version[BOTLINE_CPLD1_KEY] = SWITCH_CPLD.newVersion if isUpgrade else SWITCH_CPLD.oldVersion
        version[BOTLINE_CPLD2_KEY] = SWITCH_CPLD.newVersion if isUpgrade else SWITCH_CPLD.oldVersion

    if not verifyFwVersion(SwImage.CPLD, version, "need_update"):
        for key in version.keys():
            log.info("Already at " + key + " " +  version[key] + ", no need to update.")
        return {}

    AliCommonLib.executePythonCommand("python", commonVar.openbmc_mode, timeout=30)
    AliCommonLib.executePythonCommand("from hal.hal_firmware import *", timeout=30)
    AliCommonLib.executePythonCommand("a=HalFirmware()", timeout=30)
    sleep(3)

    onlineUpdateCpld(isUpgrade)
    sleep(10)

    device.getPrompt(commonVar.openbmc_mode)
    return version


@logThis
def updateFpga(isUpgrade=True):
    imageObj = SwImage.getSwImage("FPGA_MULTBOOT")
    version = {}
    version[FPGA_KEY] = imageObj.newVersion if isUpgrade else imageObj.oldVersion
    package_file = imageObj.newImage if isUpgrade else imageObj.oldImage
    if not verifyFwVersion(SwImage.FPGA, version, "need_update"):
        log.info("Already at version " +  version[FPGA_KEY] + ", no need to update.")
        return

    AliCommonLib.executePythonCommand("python", commonVar.openbmc_mode, timeout=30)
    AliCommonLib.executePythonCommand("from hal.hal_firmware import *", timeout=30)
    AliCommonLib.executePythonCommand("a=HalFirmware()", timeout=30)
    cmd = "a.program_cpld(['FPGA'],['%s/%s'])"%(imageObj.localImageDir, package_file)
    output = AliCommonLib.executePythonCommand(cmd, timeout=600)
    sleep(3)
    device.getPrompt(commonVar.openbmc_mode)

    verifyLogWithKeywords(util_fail_patterns, output, check_fail=True)
    if parseSimpleKeyword(fpga_update_pass_msg, output) != "":
        log.success("Successfully online update fpga")
    else:
        device.raiseException("Online update fpga failed")

    log.info("###### check COM-E status and logs ######")
    verifyPowerStatus("on")
    verifyCommandPatternList(fpga_update_log_cmd, fpga_update_log_patterns, commonVar.openbmc_mode)

    log.info("###### Power cycle and check version ######")
    AliCommonLib.powerCycleToOpenbmc()
    device.getPrompt(commonVar.diagos_mode)
    sleep(30)
    verifyFwVersion("FPGA_MULTBOOT", version)

@logThis
def verifyFwVersion(device_type, device_version, role="verify"):
    err_count = 0
    parsed_output = {}
    if device_type.upper() == "BMC":
        cmd = 'cat /etc/issue'
        output = device.executeCmd(cmd, commonVar.openbmc_mode)
        parsed_output[SwImage.BMC_VER] = parseOneGroupKeyword(openbmc_version_regex, output)
    elif device_type.upper() == "BIOS":
        cmd = "dmidecode -s bios-version"
        device.getPrompt(commonVar.diagos_mode)
        changeToRootUserMode()
        output = device.executeCmd(cmd, commonVar.diagos_mode)
        exitFromRootUserMode()
        parsed_output[SwImage.BIOS_VER] = parseOneGroupKeyword(bios_version_pattern, output)
    elif 'CPLD' in device_type.upper():
        if 'migaloo' in devicename:
            restful_cmd_test = "curl -g %s/%s"%(api_bmc_url, api_bmc_info)
            log.info("##### wait until bmc restful is ready before getting CPLD version #####")
            waitAndVerifyCommand(restful_cmd_test, '"status": "OK"', commonVar.diagos_mode)
        changeToRootUserMode()
        log.info("##### getting %s version #####"%(device_type))
        CommonLib.change_dir(diag_cpu_path, commonVar.diagos_mode)
        output = device.executeCmd(cpld_version_cmd, commonVar.diagos_mode)
        CommonLib.change_dir("", commonVar.diagos_mode)
        exitFromRootUserMode()
        parsed_output = parseLineIntoDictionary(version_test_pattern, output)
        if 'shamu' in devicename:
            output = device.executeCmd('version_dump', commonVar.openbmc_mode)
            parsed_fan_output = parseLineIntoDictionary(version_test_pattern, output)
            if FAN_CPLD_KEY in parsed_fan_output:
                parsed_output[FAN_CPLD_KEY] = "0x%02x" % int(parsed_fan_output[FAN_CPLD_KEY], 16)
            else:
                log.fail('Not found %s in output'%(FAN_CPLD_KEY))
    elif 'FPGA' in device_type.upper():
        changeToRootUserMode()
        log.info("##### getting %s version #####"%(device_type))
        CommonLib.change_dir(diag_cpu_path, commonVar.diagos_mode)
        output = device.executeCmd(fpga_version_cmd, commonVar.diagos_mode)
        CommonLib.change_dir("", commonVar.diagos_mode)
        exitFromRootUserMode()
        parsed_output = parseLineIntoDictionary(version_test_pattern, output)
    if role == "need_update":
        err_count += CommonLib.compare_input_dict_to_parsed(parsed_output, device_version, False)
        # return True if err_count > 0 else False
        #### To force update for draft version, always return True
        return True if err_count > 0 else False
    elif role == "get":
        return parsed_output
    else:
        err_count += CommonLib.compare_input_dict_to_parsed(parsed_output, device_version)
        if err_count:
            device.raiseException("Failure while verifyFwVersion with result FAIL")

@logThis
def onlineUpdateFw(fw_type, boot_flash, isUpgrade, timeout=1200):
    imageObj = SwImage.getSwImage(fw_type.upper())
    package_file = imageObj.newImage if isUpgrade else imageObj.oldImage
    image_path = imageObj.localImageDir + '/' + package_file
    if fw_type.upper() == "BMC":
        flash_path = slave_dev if boot_flash.lower() == "slave" else master_dev
        cmd = 'flashcp -v ' + imageObj.localImageDir + '/' + package_file + ' /dev/' + flash_path
        pass_msg = bmc_update_pass_msg
    elif fw_type.upper() == "BIOS":
        loadOpenbmcUtils()
        cmd = 'bios_upgrade ' + boot_flash.lower() + ' -w ' + image_path
        pass_msg = bios_update_pass_msg
    else:
        log.fail("onlineUpdateFw does not support fw type: %s"%(fw_type))
        device.raiseException("onlineUpdateFw failed")

    output = device.executeCmd(cmd, commonVar.openbmc_mode, timeout)
    match = re.search(pass_msg, output)
    match2 = re.search(no_such_file_msg, output)
    if match:
        log.success("Successfully onlineUpdateFw: %s"%(fw_type))
    elif match2:
        log.fail("%s" %(no_such_file_msg))
        device.raiseException("onlineUpdateFw failed")
    else:
        log.fail("Not found: %s" %(pass_msg))
        device.raiseException("onlineUpdateFw failed")

@logThis
def onlineUpdateCpld(isUpgrade, timeout=cpld_update_timeout):
    cpld_image_list = []
    cpld_list_str =  ", ".join(f"'{w.upper()}'" for w in cpld_type_image_dict.keys())

    for cpld_image in cpld_type_image_dict.values():
        imageObj = SwImage.getSwImage(cpld_image)
        package_file = imageObj.newImage if isUpgrade else imageObj.oldImage
        image_path = imageObj.localImageDir + '/' + package_file
        cpld_image_list.append(image_path)

    cpld_image_list_str = ", ".join(f"'{w}'" for w in cpld_image_list)

    cmd = "a.program_cpld([%s],[%s])"%(cpld_list_str, cpld_image_list_str)
    # log.info(cmd)
    device.readMsg()
    sleep(1)
    output = AliCommonLib.executePythonCommand(cmd, timeout=timeout)
    sleep(3)
    device.getPrompt(commonVar.openbmc_mode)
    match = re.search(cpld_update_pass_msg, output)
    match2 = re.search(no_such_file_msg, output)
    if match:
        log.success("Successfully onlineUpdateCpld")
    elif match2:
        log.fail("%s" %(no_such_file_msg))
        device.raiseException("onlineUpdateCpld failed")
    else:
        log.fail("Not found: %s" %(cpld_update_pass_msg))
        device.raiseException("onlineUpdateCpld failed")


@logThis
def checkEthPorts(interface_list):
    err_count = 0
    out = device.executeCmd('ifconfig', timeout=10)
    for interface in interface_list:
        if interface in out:
            log.info("Found ethernet port: %s"%(interface))
        else:
            log.fail("Not found ethernet port: %s"%(interface))
            err_count += 1
    if err_count:
        log.fail("Verify ethernet ports failed!")
        device.raiseException("Verify ethernet ports failed!")
    log.success("Successfully check all ethernet ports")

@logThis
def verifyMacAddress(interface, expected_result=None):
    err_count = 0
    cmd = 'ifconfig %s'%(interface)
    output = device.executeCmd(cmd)
    parsed_output = parseOneGroupKeyword(mac_addr_pattern, output)
    if expected_result != None:
        if parsed_output.lower() == expected_result.lower():
            log.success("Mac address match: %s, %s" %(expected_result, parsed_output))
        else:
            log.fail("Mac address mismatch: %s, %s"%(expected_result, parsed_output))
            err_count += 1
    else:
        if parsed_output:
            log.info("Successfully get mac address: %s"%(parsed_output))
        else:
            log.fail("Fail to parse mac adrress")
            err_count += 1
    if err_count:
        device.raiseException("verifyMacAddress")

@logThis
def checkCpuAlive(need_cd=False, path='/etc'):
    device.getPrompt(commonVar.diagos_mode)
    if need_cd:
        CommonLib.change_dir(path, commonVar.diagos_mode)
    verifySimpleCommand("pwd", path, commonVar.diagos_mode)
    device.getPrompt(commonVar.openbmc_mode)

@logThis
def verifySimpleCommand(cmd, regex, mode, timeout=60):
    output = device.executeCmd(cmd, mode, timeout)
    parsed = parseSimpleKeyword(regex, output)
    if parsed != "":
        log.success("Successfully verify command: %s"%(cmd))
    else:
        log.fail("verify command '%s' failed"%(cmd))
        device.raiseException("verifySimpleCommand")

@logThis
def verifyCommandPatternList(cmd, regex_list: list, mode, timeout=60):
    err_count = 0
    output = device.executeCmd(cmd, mode, timeout)
    for regex in regex_list:
        if parseSimpleKeyword(regex, output) == "":
            err_count += 1
    if err_count:
        log.fail("verify command '%s' failed"%(cmd))
        device.raiseException("verifyCommandPatternList failed!")
    log.success("Successfully verifyCommandPatternList")

@logThis
def prepareAutotestImages():
    CommonLib.get_dhcp_ip_address(Const.DUT, 'eth0', commonVar.diagos_mode)
    CommonLib.create_dir(auto_test_image_dir, commonVar.diagos_mode)
    CommonLib.download_image(Const.DUT, SwImage.BMC, destinationDir = os.path.join(auto_test_image_dir, 'flash-as58xx-cl'))
    CommonLib.download_image(Const.DUT, SwImage.FPGA , destinationDir = os.path.join(auto_test_image_dir, 'fpga.bin'))
    CommonLib.download_image(Const.DUT, SwImage.BIOS, destinationDir = os.path.join(auto_test_image_dir, 'bios.bin'))
    log.success('prepareAutotestImages successfully.')

@logThis
def prepareAutotestCplds():
    CommonLib.get_dhcp_ip_address(Const.DUT, 'eth0', commonVar.diagos_mode)
    CommonLib.create_dir(auto_test_image_dir, commonVar.diagos_mode)
    for cpld_type, cpld_img in auto_test_cpld_img_dict.items():
        CommonLib.download_image(Const.DUT, cpld_type, destinationDir=os.path.join(auto_test_image_dir, cpld_img))
    if 'migaloo' in devicename:
        CommonLib.change_dir(auto_test_image_dir, commonVar.diagos_mode)
        device.executeCmd('cp %s %s'% (auto_test_cpld_img_dict.get("SWITCH_CPLD"), auto_test_top_cpld_img))
        device.executeCmd('cp %s %s'% (auto_test_cpld_img_dict.get("SWITCH_CPLD"), auto_test_bot_cpld_img))
    log.success('prepareAutotestCplds successfully.')

@logThis
def exeAutotest(option, timeout = 20):
    pattern = "{}.*?...[\s\S]+{}".format(option.split('.')[-1], 'ok')
    device.getPrompt(mode=commonVar.diagos_mode)
    device.sendCmd('cd ' + auto_test_dir)
    device.sendCmdRegexp(auto_test_cmd + option, pattern, timeout)
    log.success(option.split('.')[-1] + ' successfully.')

@logThis
def exeAutotestAndWaitSystemReboot(option, timeout=120):
    err_count = 0
    device.getPrompt(mode=commonVar.diagos_mode)
    device.sendCmd('cd ' + auto_test_dir)
    device.sendCmd(auto_test_cmd + option)
    output = device.read_until_regexp('------------------------------|BIOS Power On Self-Test Start', timeout)
    sleep(3)
    device.getPrompt(commonVar.diagos_mode, AliConst.BOOT_TIME)
    device.getPrompt(commonVar.openbmc_mode, AliConst.BOOT_TIME)
    ### check fail message
    for regex in auto_fail_patterns:
        if parseSimpleKeyword(regex, output):
            err_count += 1
    if err_count:
        log.fail(option.split('.')[-1] + ' failed.')
        device.raiseException("exe autotest and wait system reboot failed!")
    else:
        log.success(option.split('.')[-1] + ' successfully.')
        sleep(40)

@logThis
def setSkipRebootCpu(option=False):
    device.getPrompt(mode=commonVar.diagos_mode)
    CommonLib.change_dir(auto_test_dir, commonVar.diagos_mode)
    if option:
        cmd = "sed -i 's/%s/%s/' %s"%(skip_reboot_cpu_false, skip_reboot_cpu_true, unittest_config_file)
    else:
        cmd = "sed -i 's/%s/%s/' %s"%(skip_reboot_cpu_true, skip_reboot_cpu_false, unittest_config_file)
    device.executeCmd(cmd)
    device.executeCmd('cat %s | grep SKIP_REBOOT_CPU'%(unittest_config_file))
    CommonLib.change_dir()

@logThis
def verifyLogWithKeywords(regex_list: list, target_log, check_fail=False):
    err_count = 0
    for regex in regex_list:
        if check_fail:
            if parseSimpleKeyword(regex, target_log, ignore_case=True):
                err_count += 1
        else:
            if parseSimpleKeyword(regex, target_log) == "":
                err_count += 1
    if err_count:
        log.fail("verify log failed")
        device.raiseException("verifyLogWithKeywords failed!")
    log.success("Successfully verifyLogWithKeywords")


@logThis
def verifyPowerControl(power_mode, verify_log_flag=True):
    loadOpenbmcUtils()
    if power_mode == 'off':
        cmd = 'wedge_power.sh off'
        output = device.executeCmd(cmd, mode=commonVar.openbmc_mode, timeout=300)
        parsed = parseSimpleKeyword(power_ctrl_pattern, output)
        sleep(5)
        if 'Done' in parsed:
            log.success("Successfully power switched off")
            return
        else:
            log.fail("Chassis not switched off")
            device.raiseException("Chassis switch %s failed"%(power_mode))
    elif power_mode == 'on':
        cmd = 'wedge_power.sh on'
        output = device.executeCmd(cmd, mode=commonVar.openbmc_mode, timeout=300)
        parsed = parseSimpleKeyword(power_ctrl_pattern, output)
        if 'Done' in parsed:
            log.success("Successfully power switched %s"%(power_mode))
        elif 'Skip' in parsed:
            device.sendline("")
            log.info("Chassis is already on")
            return
        else:
            log.fail("Chassis not switched %s"%(power_mode))
            device.raiseException("Chassis switch %s failed"%(power_mode))
        device.trySwitchToCpu()
        output = device.receive('sonic login:', timeout=AliConst.BOOT_TIME)
        output += device.getPrompt(commonVar.diagos_mode, AliConst.BOOT_TIME)
        sleep(5)
    elif power_mode == 'cycle':
        output = AliCommonLib.powerCycleSonic(commonVar.diagos_mode)
    elif power_mode == 'reset':
        output = AliCommonLib.powerResetSonic(commonVar.diagos_mode)

    if verify_log_flag:
        verifyLogWithKeywords(bios_boot_pattern, output)

@logThis
def verifyPowerStatus(power_status):
    loadOpenbmcUtils()
    cmd = 'wedge_power.sh status'
    output = device.executeCmd(cmd, mode=commonVar.openbmc_mode)
    parsed = parseSimpleKeyword(power_status_pattern, output)
    if power_status in parsed:
        log.success("Power Status is correct")
    else:
        log.fail("Power Status is incorrect")
        device.raiseException("Verify power status failed")

@logThis
def runEepromTool(option, fan='', expected_result='None', prompt=commonVar.openbmc_mode, pattern=eeprom_pattern):
    err_count = 0
    if fan != '':
        cmd = './eeprom_tool -%s -f %s'%(option, str(fan))
    else:
        cmd = './eeprom_tool -%s'%(option)
    if option == 'tlv':
        cmd = './cel-eeprom-test -t tlv -d 1 -r -C 256'
    output = device.executeCmd(cmd, prompt)
    if option == 'd' or option == 'tlv':
        parsed_dict = parseLineIntoDictionary(pattern, output)
        if expected_result != 'None':
            expected_dict = CommonLib.get_eeprom_cfg_dict(expected_result)
            log.info("##### comparing eeprom info output with eeprom.cfg #####")
            err_count += CommonLib.compare_input_dict_to_parsed(parsed_dict, expected_dict)
        else:
            if parsed_dict:
                log.success("Successfully run eeprom tool")
                return parsed_dict
            else:
                log.fail("No eeprom output returned")
                err_count += 1
    else:
        for regex in util_fail_patterns:
            if parseSimpleKeyword(regex, output, ignore_case=True):
                err_count += 1
    if err_count:
        log.fail(cmd + ' failed.')
        device.raiseException("run eeprom tool failed!")
    log.success("Successfully run eeprom tool")

@logThis
def runUtil(cmd, expected_result='None'):
    err_count = 0
    output = device.executeCmd(cmd, commonVar.openbmc_mode)
    parsed_dict = parseLineIntoDictionary(eeprom_pattern, output)
    if expected_result != 'None':
        err_count += CommonLib.compare_input_dict_to_parsed(parsed_dict, expected_result)
    else:
        if parsed_dict:
            log.success("Successfully run util: %s"%(cmd))
            return parsed_dict
        else:
            log.fail("No util output returned")
            err_count += 1
    if err_count:
        device.raiseException("run %s failed"%(cmd))

@logThis
def compareUtilAndEeprom(util_dict, eeprom_dict, map_key_dict=UTIL_EEPROM_MAP_KEY):
    new_dict = {}
    log.info("##### changing util output to eeprom output format #####")
    for key, val in util_dict.items():
        if key in map_key_dict:
            mapping_key = map_key_dict[key]
            new_dict[mapping_key] = util_dict[key]
            log.info("%s: %s --> %s: %s"%(key, val, mapping_key, new_dict[mapping_key]))
        else:
            new_dict[key] = util_dict[key]

    log.info("##### comparing mapped util output with eeprom output #####")
    err_count = 0
    err_count += CommonLib.compare_input_dict_to_parsed(new_dict, eeprom_dict, highlight_fail=True)
    if err_count:
        device.raiseException("compareUtilAndEeprom failed")

@logThis
def modifyEepromCfg(eeprom_name, fru_type, eeprom_cfg_file):
    eeprom_string = AliCommonLib.ali_generate_eeprom_cfg(eeprom_name, fru_type)
    cmd = "echo -e \"%s\" > %s"%(eeprom_string, eeprom_cfg_file)
    device.executeCmd(cmd, commonVar.openbmc_mode)
    device.executeCmd("cat %s"%(eeprom_cfg_file))

@logThis
def checkRebootLog(iterate=1):
    device.getPrompt(commonVar.diagos_mode)
    device.flush()
    output = ""
    for i in range (1, iterate+1):
        output += "\n" + device.sendCmdRegexp('time reboot', device.loginPromptDiagOS, AliConst.BOOT_TIME)
        device.getPrompt(commonVar.diagos_mode)
        cmds = [
            'ls aaaaaaa',
            'ls bbbbbbb',
            'ls ccccccc',
        ]
        for cmd in cmds:
            output += "\n" + device.executeCmd(cmd)

    device.getPrompt(commonVar.openbmc_mode)
    data = device.sendCmdRegexp("time cat %s"%(uart_log_file), r"sys\s.*\dm.*\ds.*\n%s"%(device.promptBmc), 60*iterate)

    lostLines = []
    for line in output.splitlines():
        if line.strip() == '':
            continue
        if line.strip() not in data:
            if line.strip() in cmds:
                raise RuntimeError('Can not find cmd [{}]!'.format(line))
            lostLines.append(line.strip())

    if lostLines:
        log.info('mismatch lines: \n' + '\n'.join(lostLines))

    if len(lostLines) < 28*iterate:
        log.success('Most of the records are exactly match, judged as success.')
    else:
        raise RuntimeError('Too many mismatch lines found, judged as fail!')


def getLogData():
    ip = CommonLib.get_dhcp_ip_address(Const.DUT, 'eth0', commonVar.openbmc_mode)
    if CommonLib.get_file_by_scp(ip, device.bmcUserName, device.bmcPassword, '/var/log/', 'console.log', './'):
        raise RuntimeError('Can not download file console.log')

    with open('console.log', 'rt', encoding='ISO-8859-1') as f:
        data = f.read()
        # log.cprint('data: ' + data)
    return data


@logThis
def checkMultiRebootLog(rebootCount):
    device.getPrompt(commonVar.diagos_mode)
    device.flush()
    output = ''
    for i in range(int(rebootCount)):
        output += device.sendCmdRegexp('time reboot', device.loginPromptDiagOS, AliConst.BOOT_TIME)
        device.getPrompt(commonVar.diagos_mode)
    data = getLogData()

    lostLines = []
    for line in output.splitlines():
        if line.strip() == '':
            continue
        if line.strip() not in data:
            lostLines.append(line.strip())

    log.info('mismatch lines: \n' + '\n'.join(lostLines))

    if len(lostLines) < 28*3:
        log.success('Most of the records are exactly match, judged as success.')
    else:
        raise RuntimeError('Too many mismatch lines found, judged as fail!')

@logThis
def checkMemory():
    out = device.executeCmd('cat /proc/meminfo')
    CommonKeywords.should_match_ordered_regexp_list(out, meminfo_pattern)
    log.success('checkMemory successfully.')

@logThis
def memoryTest():
    device.sendCmd('cd ' + commonVar.bmc_diag_utility_path)
    out = device.executeCmd('./memtester 10M 1', timeout=1200)
    CommonKeywords.should_match_ordered_regexp_list(out, memtest_pattern)

@logThis
def cpuShouldOff():
    try:
        device.switchToCpu(timeout=20)
        raise RuntimeError('CPU is not powered off as expected!')
    except:
        log.success('CPU is powered off successfully.')
        device.switchToBmc()

@logThis
def restoreCpu():   ## for comm case 45
    try:
        device.switchToCpu(timeout=20)
    except:
        log.warning('CPU is powered off, need powered on.')
        device.switchToBmc()
        try:
            device.execCmd('i2cset -f -y 0 0x0d 0x24 0; sleep 1; i2cset -f -y 0 0x0d 0x24 0x01')
            device.getPrompt(commonVar.diagos_mode, timeout=300)
        except:
            log.error('Power on cpu failed, use workaround power cycle to recover cpu !')
            AliCommonLib.powerCycleToOpenbmc()  # @WORKAROUND workaround for the SW issue: jira BEYON-1236
            raise RuntimeError('Power on cpu failed, restored it by power cycle !')

@logThis
def recoverNetwork():
    CommonLib.get_dhcp_ip_address(Const.DUT, 'eth0', commonVar.openbmc_mode)
    sleep(5)
    try:
        CommonLib.exec_ping(Const.DUT, DeviceMgr.getServerInfo('PC').managementIP, 4, commonVar.diagos_mode)
    except:
        log.error('network is broken down, need recover it !')
        AliCommonLib.powerCycleToOpenbmc()
        raise RuntimeError('network is broken down, after running this case !')

@logThis
def getFanSpeed(fan_speed, fan_speed_max=None, check_rpm=True):
    err_count = 0
    variance = 2
    output = device.executeCmd('get_fan_speed.sh', commonVar.openbmc_mode)
    parsed = parseGetFanSpeed(output)
    for i in range(1, FAN_NUM + 1):
        key = 'Fan %d percentage'%(i)
        if key in parsed:
            speed = int(parsed[key])
            exp_speed = int(fan_speed)
            if fan_speed_max:
                max_speed = int(fan_speed_max)
                if (exp_speed-variance) <= speed <= (max_speed+variance):
                    log.success("get fan %d speed: %d%% (%d%% ~ %d%%)"%(i, speed, exp_speed, max_speed))
                else:
                    log.fail("fan %d speed: %d%% is over the range of expected speed: %d%% ~ %d%%"%(i, speed, exp_speed, max_speed))
                    err_count += 1
            else:
                if (exp_speed-variance) <= speed <= (exp_speed+variance):
                    log.success("get fan %d speed: %d%% (%d%%)"%(i, speed, exp_speed))
                else:
                    log.fail("fan %d speed: %d%% is over the range of expected speed: %d%%"%(i, speed, exp_speed))
                    err_count += 1
        else:
            log.fail("Not found: %s"%(key))
            err_count += 1

        if check_rpm:
            key = 'Fan %d front'%(i)
            if key in parsed:
                parsed_rpm_front = int(parsed[key])
                err_count += verifyFanRpm(i, parsed_rpm_front, MIN_RPM, MAX_RPM)
            else:
                log.fail("Not found: %s"%(key))
                err_count += 1

            key = 'Fan %d rear'%(i)
            if key in parsed:
                parsed_rpm_rear = int(parsed[key])
                err_count += verifyFanRpm(i, parsed_rpm_rear, MIN_RPM, MAX_RPM)
            else:
                log.fail("Not found: %s"%(key))
                err_count += 1
    if err_count:
        raise RuntimeError("Get fan Speed failed")

@logThis
def verifyFanRpm(fan, rpm, min, max):
    err_count = 0
    if min <= rpm <= max:
        log.success("Fan %d RPM: %d is in range %d-%d"%(fan, rpm, min, max))
    else:
        log.fail("Fan %d RPM: %d is out of range %d-%d"%(fan, rpm, min, max))
        err_count += 1
    return err_count

@logThis
def waitAndVerifyCommand(cmd, pattern, mode, delay=30, timeout=60):
    count = 0
    status = ""
    while status == "":
        sleep(delay)
        count += 1
        log.info("trying: #%d"%(count))
        try:
            output = device.executeCmd(cmd, mode, timeout)
            status = parseSimpleKeyword(pattern, output)
            if count >= 20 and status == "":
                device.raiseException("try checking command %d times and always not found %s"%(count, pattern))
        except:
            if count >= 20:
                device.raiseException("try checking command %d times and always not found %s"%(count, pattern))

@logThis
def waitAndVerifyDateSync(delay=30):
    count = 0
    status = 1
    while status == 1:
        sleep(delay)
        count += 1
        log.info("trying: #%d"%(count))
        try:
            status = verifyDateSync()
            if count >= 60 and status == 1:
                device.raiseException("try checking command %d times and always not sync"%(count))
        except:
            if count >= 60:
                device.raiseException("try checking command %d times and always not sync"%(count))

@logThis
def verifyDateSync(tz="UTC"):
    tformat = "%a %b %d %H:%M:%S %Z %Y"
    cmd = "TZ=%s date"%(tz)
    output1 = device.executeCmd(cmd, commonVar.diagos_mode)
    output2 = device.executeCmd(cmd, commonVar.openbmc_mode)
    output1 = parseOneGroupKeyword(date_pattern, output1)
    output2 = parseOneGroupKeyword(date_pattern, output2)
    date_sonic = datetime.strptime(output1, tformat)
    date_bmc = datetime.strptime(output2, tformat)
    diff = abs(date_sonic - date_bmc)
    if diff.seconds < 10:
        log.success('Openbmc has the same date as SONIC')
        return 0
    log.info('Openbmc date does not sync with SONIC')
    return 1

@logThis
def verifySensorValue(output, min:float=None, max:float=None, useThreshold=False):
    err_count = 0
    parsed_sensor = parseSensors(sensors_pattern, output)
    for sensor, value in parsed_sensor.items():
        val = float(value[0])
        if useThreshold:
            min = float(value[1])
            max = float(value[2])
        if min:
            if val >= min:
                log.success("sensor: %s, value: %s is greater than min: %s"%(sensor, value[0], min))
            else:
                err_count += 1
                log.fail("sensor: %s, value: %s is lower than min: %s"%(sensor, value[0], min))
        if max:
            if val <= max:
                log.success("sensor: %s, value: %s is lower than max: %s"%(sensor, value[0], max))
            else:
                err_count += 1
                log.fail("sensor: %s, value: %s is greater than max: %s"%(sensor, value[0], max))
    if err_count:
        device.raiseException("fail to verify sensor value")

@logThis
def close_eeprom_write_protect():
    """
    The new basecpld has eeprom (switch/sys/tlv) write protect function.
    Migaloo basecpld version: 0xf
    Shamu basecpld version: 0x11
    """
    changeToRootUserMode()
    device.executeCmd('echo 0xa131 0x00 > /sys/devices/platform/AS*.cpldb/setreg')
