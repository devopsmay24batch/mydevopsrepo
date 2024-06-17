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
from JuniperCommonVariable import *

try:
    from Device import Device
    import DeviceMgr
except Exception as err:
    log.cprint(str(err))

device = DeviceMgr.getDevice()

def DiagOSConnect():
    log.debug("Entering JuniperCommonLib procedure: DiagOSConnect")
    device.loginDiagOS()
    return

def DiagOSDisconnect():
    global libObj
    log.debug("Entering JuniperCommonLib procedure: DiagOSDisconnect")
    device.disconnect()
    return

def bootIntoDiagOSMode():
    log.debug("Entering JuniperCommonLib procedure: bootIntoDiagOSMode")
    return device.getPrompt(Const.BOOT_MODE_DIAGOS)

def get_data_from_yaml(name):
    stressInfo = YamlParse.getStressConfig()
    return stressInfo[name]

@logThis
def setTimeToSleep(para):
    import time
    time.sleep(int(para))

@logThis
def get_card_type():
    CommonLib.change_dir(diag_path)
    output = device.executeCmd("./bin/cel-cards-test -s")
    for line in output.splitlines():
        match = re.search(r'Card type is(.*?)$', line)
        if match:
            type = match.group(1)
            log.info("card type: " + type)
            return type.strip()

    raise RuntimeError("can't get card type!")



