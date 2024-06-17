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
import traceback
import CRobot
from time import sleep

workDir = CRobot.getWorkDir()
sys.path.append(os.path.join(workDir, 'platform', 'ali', 'openbmc'))
from crobot import Logger as log
try:
    from common.commonlib import CommonLib
    from common.openbmc import bios_menu_lib
    from ali.openbmc import AliOpenBmcLib
    from AliBiosVariable import *
    from AliCommonVariable import *
    from AliConst import *
    import AliCommonLib
    import DeviceMgr
    from crobot import Const
    from crobot.SwImage import SwImage
    from crobot.Decorator import logThis
except Exception as err:
    log.cprint(traceback.format_exc())

device = DeviceMgr.getDevice()


@logThis
def biosConnect():
    device.loginBios()
    device.sendCmd('sudo su')
    return

@logThis
def biosDisconnect():
    return device.disconnect()

@logThis
def enterBiosSetup(prompt=diagos_mode, post_list:list=[], enter_keyword=ENTER_BIOS_KEYWORD, \
                   enter_key="KEY_DEL", bios_password="", enter_line=BIOS_HEADER_KEYWORD):
    line1 = BIOS_START_KEYWORD
    line2 = '------'
    line4 = 'Enter Password'

    device.getPrompt(prompt)
    if prompt == uefi_mode:
        device.sendline("reset")
    else:
        device.sendline("reboot")
    sleep(1)
    output = device.readMsg()
    output += device.read_until_regexp(line1, timeout=300)
    for post_str in post_list:
        output += device.read_until_regexp(post_str, timeout=180)

    try:
        output += device.read_until_regexp(enter_keyword, timeout=60)
        sendKey(enter_key)
    except:
        ##### in case of having password both admin and user access
        for c in bios_password:
            device.sendMsg(c)
            sleep(0.5)
        sendKey('KEY_ENTER')
        if enter_line != BIOS_HEADER_KEYWORD:
            output += device.read_until_regexp(enter_line, timeout=10)
            log.success("Found keyword: %s"%(enter_line))
            return
        output += device.read_until_regexp(enter_keyword, timeout=60)
        sendKey(enter_key)

    output += device.read_until_regexp(line2, timeout=60)
    match = re.search(line4, output)
    match1 = re.search(enter_line, output)
    if match:
        log.debug("Found '%s'"%(line4))
        for c in bios_password:
            device.sendMsg(c)
            sleep(0.5)
        sendKey('KEY_ENTER')
        output += device.read_until_regexp(enter_line, timeout=60)
        if enter_line == BIOS_HEADER_KEYWORD:
            log.success("Successfully enter Bios Setup")
        else:
            log.success("Found keyword: %s"%(enter_line))
    elif match1:
        log.debug("Found '%s'"%(enter_line))
        log.success("Successfully enter Bios Setup")
    else:
        log.fail("Failed enter Bios Setup")
        device.raiseException("Failed enter Bios Setup")
    return output

@logThis
def exitBiosSetup(prompt=diagos_mode):
    line_quit = 'Quit without saving?'
    for i in range (1, 11):
        log.debug('exit #%i'%(i))
        sendKey('KEY_ESC')
        try:
            device.read_until_regexp(line_quit, timeout=10)
            break
        except:
            continue
    sendKey('KEY_ENTER')
    device.getPrompt(prompt, timeout=BOOT_TIME)

@logThis
def saveAndExitBiosSetup(prompt=diagos_mode):
    line_quit = 'Save configuration and exit?'
    sendKey('KEY_F10')
    device.read_until_regexp(line_quit, timeout=10)
    sendKey('KEY_ENTER')
    sleep(5)
    device.getPrompt(prompt, timeout=BOOT_TIME)

@logThis
def sendKey(key_name, counts=1, delay=2):
    return bios_menu_lib.send_key(Const.DUT, key_name, counts, delay)

@logThis
def verifyLogWithKeywords(regex_list: list, target_log, check_fail=False):
    return AliOpenBmcLib.verifyLogWithKeywords(regex_list, target_log, check_fail)

@logThis
def runEepromTool(option, fan='', expected_result='None', prompt=openbmc_mode, pattern=eeprom_pattern):
    return AliOpenBmcLib.runEepromTool(option, fan, expected_result, prompt, pattern)

@logThis
def switchBmcFlash(bmc_flash):
    return AliOpenBmcLib.switchBmcFlash(bmc_flash)

@logThis
def switchBiosFlash(bios_flash, timeout=BOOT_TIME):
    return AliOpenBmcLib.switchBiosFlash(bios_flash, timeout)

@logThis
def onlineUpdateFw(fw_type, boot_flash, isUpgrade=True, timeout=1200):
    return AliOpenBmcLib.onlineUpdateFw(fw_type, boot_flash, isUpgrade, timeout)

@logThis
def verifyCurrentBootFlash(fw_type, boot_flash, boot_status='OK'):
    return AliOpenBmcLib.verifyCurrentBootFlash(fw_type, boot_flash, boot_status)

@logThis
def verifyPowerStatus(power_status):
    return AliOpenBmcLib.verifyPowerStatus(power_status)

@logThis
def verifyPowerControl(power_mode, verify_log_flag=False):
    return AliOpenBmcLib.verifyPowerControl(power_mode, verify_log_flag)

@logThis
def updateBiosCrash():
    return AliOpenBmcLib.updateBiosCrash()

@logThis
def updateBiosUefiMode(isUpgrade=True):
    package_file = bios_new_image if isUpgrade else bios_old_image

    ### AfuEfix64.efi bios.bin /p /b /n /me /x
    cmd = '%s %s /p /b /n /me /x'%(afu_new_image, package_file)
    device.getPrompt(uefi_mode)
    device.sendCmd('cls')
    device.sendCmdRegexp("FS0:", PROMPT_UEFI, timeout=30)
    device.sendMsg('\r\n')
    output = device.sendCmdRegexp("dir", r'Dir\(s\)', timeout=30)
    if (afu_new_image in output) and (package_file in output):
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
        output = device.read_until_regexp(bios_pass_pattern, timeout=1200)
    else:
        log.fail("Not found tool or bios image")
        device.raiseException("Failure while update bios")

    device.getPrompt(uefi_mode)

@logThis
def recoverSonic():
    try:
        sendKey('KEY_RIGHT')
        sleep(3)
        device.read_until_regexp('American Megatrends, Inc', timeout=10)
        log.info('CPU stuck in BIOS Setup, need to exit!')
        exitBiosSetup()
    except:
        try:
            device.getPrompt(Const.BOOT_MODE_DIAGOS, timeout=180)
        except:
            try:
                log.error('CPU hung, need recover it!')
                device.switchToBmc()
                AliCommonLib.powerCycleSonic(diagos_mode)
            except:
                log.error('Failed to run wedge_power.sh cycle, need to power cycle the whole system!')
                AliCommonLib.powerCycleToOpenbmc()
            return device.getPrompt(Const.BOOT_MODE_DIAGOS)

@logThis
def selectBootOverride(menu_text, target_boot):
    boot_override_start = r'Boot Override(.|\n)*'
    boot_pattern = r'((?:UEFI:|ONIE:|SONiC).*)\s{2,}[\*|v]\|'
    boot_ordered_list = []
    found = 0
    move_count = 0
    target_str = re.search(boot_override_start, menu_text).group(0)
    boot_list = re.findall(boot_pattern, target_str)
    for boot in boot_list:
        boot_ordered_list.append(boot.strip())
    length = len(boot_ordered_list)
    for boot in boot_ordered_list:
        match = re.search(target_boot, boot)
        if match:
            match_boot = boot
            move_count = length - boot_ordered_list.index(boot) - 1
            found = 1
            break

    if found == 0:
        log.fail("Not found '%s' in Boot Override list"%(target_boot))
        device.raiseException("Failure while selecting boot override")

    if move_count:
        log.info('Move KEY_UP %d time(s) to %s'%(move_count, target_boot))
        sendKey('KEY_UP', move_count)

    log.info("Selecting %s"%(match_boot))
    sendKey('KEY_ENTER')
    sleep(3)

@logThis
def selectBootOption(menu_text, popup_text, target_boot, option=1, is_bbs=False):
    found = 0
    move_count = 0
    if is_bbs:
        boot_option_start = r'Please select boot device(.|\n)*'
        boot_option_selected = r'((?:SONiC).*)\|'  ### default is SONiC
        boot_pattern = r'((?:UEFI:|ONIE:|SONiC).*)\|'
    else:
        boot_option_start = r'Boot Option #%d(.|\n)*'%(option)
        boot_option_selected = r'Boot Option #%d\s+\[(.+)\*?\|'%(option)
        boot_pattern = r'((?:UEFI:|ONIE:|SONiC).*) \|.*\|'

    old_selected = re.search(boot_option_selected, menu_text).group(1).strip()
    old_selected = old_selected[:17]
    log.info('Target boot: %s'%(target_boot))
    log.info('Old selected boot: %s'%(old_selected))
    boot_ordered_list = []
    target_str = re.search(boot_option_start, popup_text).group(0)
    boot_list = re.findall(boot_pattern, target_str)
    for boot in boot_list:
        boot_ordered_list.append(boot.strip())

    for boot in boot_ordered_list:
        match2 = re.search(re.escape(old_selected), boot)
        if match2:
            current_cursor = boot_ordered_list.index(boot)
            break

    for boot in boot_ordered_list:
            match = re.search(target_boot, boot)
            if match:
                match_boot = boot
                target_cursor = boot_ordered_list.index(boot)
                found = 1
                break

    if found == 0:
        log.fail("Not found '%s' in Boot Option list"%(target_boot))
        device.raiseException("Failure while selecting boot option")

    log.debug('current cur: %d'%current_cursor)
    log.debug('target_cur: %d'%(target_cursor))
    move_count = target_cursor - current_cursor
    if move_count > 0:
        log.info('Move KEY_DOWN %d time(s) to %s'%(move_count, target_boot))
        sendKey('KEY_DOWN', move_count)
    elif move_count < 0:
        log.info('Move KEY_UP %d time(s) to %s'%(abs(move_count), target_boot))
        sendKey('KEY_UP', abs(move_count))

    log.info("Selecting %s"%(match_boot))
    sendKey('KEY_ENTER')
    sleep(3)

@logThis
def verifyFindallKeywords(patterns, target_log, expected_count: int):
    pattern = re.compile(patterns)
    log.debug('Finding pattern: %s'%(str(pattern)))
    found_list = re.findall(pattern, target_log)
    for found in found_list:
        log.info(str(found))
    count = len(found_list)
    if expected_count == count:
        log.success('verify number of found keywords: %d\n'%(expected_count))
    else:
        log.fail("Cannot found pattern %s"%(str(pattern)))
        device.raiseException("Expected counts:{}, total counts:{} \n".format(expected_count, count))

@logThis
def verifyPciCommandUefiMode(expected_list:list, cmd='pci', timeout=10):
    device.getPrompt(uefi_mode)
    device.sendCmd('cls')
    device.sendCmd(cmd)
    sleep(timeout)
    output = device.readMsg()
    verifyLogWithKeywords(expected_list, output)

@logThis
def writeEepromToolDiag(eeprom, store_dict=None):
    eeprom_content = CommonLib.get_eeprom_cfg_dict(eeprom)
    if store_dict:
        for key, value in store_dict.items():
            if key in eeprom_content:
                eeprom_content[key] = store_dict[key]

    for key, value in eeprom_content.items():
        if key and value:
            cmd = './eeprom_tool -w "%s" -v "%s"'%(key, value)
            device.executeCmd(cmd, diagos_mode)
            CommonLib.check_exit_code(device.promptDiagOS)
            sleep(1)

@logThis
def cleanBuffer():
    device.readMsg()
    device.output = ''
    device.telnetConnect.before = ''
    device.telnetConnect.after = ''
    device.telnetConnect.buffer= ''
    return

@logThis
def parseGpio(ru_text, target_list: list, mult=0):
    normalized = int(mult) * 32
    window_size = 35
    found = 0
    gpio_dict = {}
    lines = ru_text.splitlines()
    for lno, line in enumerate(lines):
        match = re.search(index_pattern, line)
        if match:
            window_start = match.start()
            window_end = match.start() + window_size
            found = 1
            break
    if found and lno > 1:
        gpio_str = lines[lno-2][window_start:window_end]
        gpio_str = gpio_str.replace(" ", "")
        gpio_str_inv = gpio_str[::-1]
        log.debug("found gpio_str: %s"%(gpio_str))
        for gpio in target_list:
            idx = int(gpio) - normalized
            if idx < len(gpio_str_inv):
                gpio_dict["GPIO"+gpio] = gpio_str_inv[idx]
    else:
        log.fail('Cannot found GPIO target data or data is invalid')
    return gpio_dict
