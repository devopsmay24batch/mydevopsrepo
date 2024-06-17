# LEGALESE:   "Copyright (C) 2019-2020, Celestica Corp. All rights reserved." #
#                                                                             #
# This source code is confidential, proprietary, and contains trade           #
# secrets that are the sole property of Celestica Corp.                       #
# Copy and/or distribution of this source code or disassembly or reverse      #
# engineering of the resultant object code are strictly forbidden without     #
# the written consent of Celestica Corp.                                      #
#                                                                             #
###############################################################################
import os
import Const
import Logger as log
import YamlParse
from Decorator import *
import CommonLib
import re
import KapokConst

try:
    from Device import Device
    import DeviceMgr
except Exception as err:
    log.cprint(str(err))

device = DeviceMgr.getDevice()

def DiagOSConnect():
    log.debug("Entering KapokCommonLib procedure: DiagOSConnect")
    device.loginDiagOS()
    return

def DiagOSDisconnect():
    global libObj
    log.debug("Entering KapokCommonLib procedure: DiagOSDisconnect")
    device.disconnect()
    return

def powerCycleToDiagOS():
    log.debug("Entering KapokCommonLib procedure: powerCycleToDiagOS")
    return device.powerCycleToMode(Const.BOOT_MODE_DIAGOS)

def powerCycleToUboot():
    log.debug("Entering KapokCommonLib procedure: powerCycleToUboot")
    return device.powerCycleToMode(Const.BOOT_MODE_UBOOT)

def powerCycleToOnieRescueMode():
    log.debug("Entering KapokCommonLib procedure: powerCycleToOnieRescueMode")
    return device.powerCycleToMode(Const.ONIE_RESCUE_MODE)

def powerCycleToOnieInstallMode():
    log.debug("Entering KapokCommonLib procedure: powerCycleToOnieInstallMode")
    return device.powerCycleToMode(Const.ONIE_INSTALL_MODE)

def powerCycleToOnieUpdateMode():
    log.debug("Entering KapokCommonLib procedure: powerCycleToOnieUpdateMode")
    return device.powerCycleToMode(Const.ONIE_UPDATE_MODE)

def bootIntoDiagOSMode():
    log.debug("Entering KapokCommonLib procedure: bootIntoDiagOSMode")
    return device.getPrompt(Const.BOOT_MODE_DIAGOS)

def bootIntoUboot():
    log.debug("Entering KapokCommonLib procedure: bootIntoUboot")
    return device.getPrompt(Const.BOOT_MODE_UBOOT)

def bootIntoOnieInstallMode():
    log.debug("Entering OnieLib class procedure: bootIntoOnieInstallMode")
    return device.getPrompt(Const.ONIE_INSTALL_MODE)

def bootIntoOnieUpdateMode():
    log.debug("Entering OnieLib class procedure: bootIntoOnieUpdateMode")
    return device.getPrompt(Const.ONIE_UPDATE_MODE)

def bootIntoOnieRescueMode():
    log.debug("Entering OnieLib class procedure: bootIntoOnieRescueMode")
    device.getPrompt(Const.ONIE_RESCUE_MODE)

def get_data_from_yaml(name):
    stressInfo = YamlParse.getStressConfig()
    return stressInfo[name]

@logThis
def getUbootImageNamePrefix():
    if 'briggs' in device.name:
        return 'celestica_cs8210-'
    elif 'fenghuangv2' in device.name:
        return 'celestica_cs8260-'
    elif 'tianhe' in device.name:
        return 'celestica_cs8264-'
    else:
        return 'celestica_cs8200-'

@logThis
def setTimeToSleep(para):
    import time
    time.sleep(int(para))

@logThis
def decompressSdk():
    device.getPrompt(Const.BOOT_MODE_DIAGOS)
    cmd = 'cd /root/sdk'
   # device.executeCmd(cmd)
    if 'tianhe' in device.name:
        device.sendCmd(cmd)
    else:
        device.executeCmd(cmd)

    sdk_dict = CommonLib.get_swinfo_dict('SDK')
    sdk_version = sdk_dict.get('newVersion')
    sdk_dir_name = '*' + sdk_version + '*FenghuangV2_SDK/'
    exist_status = False
    tar_package = False
    xz_package = True
    while True:
        if exist_status:
            log.success("sdk dir is exited")
            break
        elif not exist_status and tar_package:
            cmd = 'tar -xvf ' + '*' + sdk_version + "*SDK.tar"
            device.executeCmd(cmd)
            output = device.executeCmd('echo $?')
            p_pass = 0
            for line in output.splitlines():
                if re.search('^0$', line):
                    p_pass += 1
                    log.debug('sdk tar package is decompressed')
            if p_pass:
                exist_status = True
            else:
                tar_package = False
                log.debug('sdk tar package is not exist')
            continue
        elif not exist_status and xz_package:
            cmd = 'xz -d ' + '*' + sdk_version + '*SDK.tar.xz'
            device.executeCmd(cmd)
            output = device.executeCmd('echo $?')
            for line in output.splitlines():
                if re.search('^0$', line):
                    log.debug('sdk xz package is decompressed')
            tar_package = True
            xz_package = False
            continue
        elif not exist_status and not tar_package and not xz_package:
            log.fail("sdk dir and sdk packet is not exited")
            device.raiseException("Failure while decompress the sdk")

@logThis
def resetUbootEnv():
    env_default = 'env default -a'
    save_cmd = 'savee'
    device.sendMsg(env_default + '\n')
    device.read_until_regexp('Resetting to default environment', timeout=60)
    device.sendMsg(save_cmd+'\n')
    device.read_until_regexp('OK', timeout=60)
    device.sendMsg('reset\n')
    device.read_until_regexp(KapokConst.STOP_AUTOBOOT_PROMPT, 100)
    device.sendMsg(KapokConst.STOP_AUTOBOOT_KEY)
    device.read_until_regexp(device.promptUboot)


@logThis
def is1ppsCard():
    cardType = device.get('cardType')
    if cardType == "1PPS":
        return True
    return False

@logThis
def is19Inch():
    devicename = os.environ.get("deviceName", "")
    size = DeviceMgr.getDevice(devicename).get('size')
    if size == '19':
        return True
    return False

@logThis
def isFpgaCard():
    devicename = os.environ.get("deviceName", "")
    if "fenghuangv2" in devicename.lower():
        dev_type = DeviceMgr.getDevice(devicename).get('cardType')
        if dev_type == 'FPGA':
            return True
        return False

