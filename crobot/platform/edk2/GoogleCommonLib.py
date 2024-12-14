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
import GoogleConst

try:
    from Device import Device
    import DeviceMgr
except Exception as err:
    log.cprint(str(err))

device = DeviceMgr.getDevice()

import Logger as log

class WhiteboxLib():
    def __init__(self):
        log.debug("Entering Whitebox class procedure: __init__")
        import DeviceMgr
        self.device = DeviceMgr.getDevice()

    def loginDevice(self):
        log.debug("Entering Whitebox class procedure: login")
        self.device.telnetConnect.open_connection(self.device.consoleIP, port=self.device.consolePort)
        self.device.tryLogin()
        log.cprint(self.device.currentBootMode)

    def loginDevice1(self):
        log.debug("Entering Whitebox class procedure: login")
        self.device.telnetConnect.open_connection(self.device.esmbConsoleIP, port=self.device.esmbConsolePort)
        self.device.tryLogin()
        log.cprint(self.device.currentBootMode)

    def disconnectDevice(self):
        try:
            self.device.trySwitchToCpu()
        except Exception:
            pass
        finally:
            return self.device.disconnect()




def DiagOSConnect():
    log.debug("Entering GoogleCommonLib procedure: DiagOSConnect")
    device.loginDiagOS()
    return

def DiagOSDisconnect():
    global libObj
    log.debug("Entering GoogleCommonLib procedure: DiagOSDisconnect")
    device.disconnect()
    return

libObj = None

def OSConnect():
    global libObj
    log.debug("Entering GoogleLibAdapter procedure: OSConnect")
    libObj = WhiteboxLib()
    libObj.loginDevice()
    return

def ConnectESMB():
    global libObj
    log.debug("Entering GoogleLibAdapter procedure: ConnectESMB")
    libObj = WhiteboxLib()
    libObj.loginDevice1()
    return

def OSDisconnect():
    global libObj
    log.debug("Entering GoogleLibAdapter procedure: OSDisconnect")
    libObj.disconnectDevice()
    return
                                                  

def powerCycleToDiagOS():
    log.debug("Entering GoogleCommonLib procedure: powerCycleToDiagOS")
    return device.powerCycleToMode(Const.BOOT_MODE_DIAGOS)

def powerCycleToUboot():
    log.debug("Entering GoogleCommonLib procedure: powerCycleToUboot")
    return device.powerCycleToMode(Const.BOOT_MODE_UBOOT)

def powerCycleToOnieRescueMode():
    log.debug("Entering GoogleCommonLib procedure: powerCycleToOnieRescueMode")
    return device.powerCycleToMode(Const.ONIE_RESCUE_MODE)

def powerCycleToOnieInstallMode():
    log.debug("Entering GoogleCommonLib procedure: powerCycleToOnieInstallMode")
    return device.powerCycleToMode(Const.ONIE_INSTALL_MODE)

def powerCycleToOnieUpdateMode():
    log.debug("Entering GoogleCommonLib procedure: powerCycleToOnieUpdateMode")
    return device.powerCycleToMode(Const.ONIE_UPDATE_MODE)

def bootIntoDiagOSMode():
    log.debug("Entering GoogleCommonLib procedure: bootIntoDiagOSMode")
    return device.getPrompt(Const.BOOT_MODE_DIAGOS)

def bootIntoUboot():
    log.debug("Entering GoogleCommonLib procedure: bootIntoUboot")
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

@logThis
def get_data_from_yaml(name):
    stressInfo = YamlParse.getStressConfig()
    return stressInfo[name]

@logThis
def setTimeToSleep(para):
    import time
    time.sleep(int(para))






