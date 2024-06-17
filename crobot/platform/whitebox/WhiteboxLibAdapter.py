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
import os
import sys
import Logger as log
import CRobot

workDir = CRobot.getWorkDir()
sys.path.append(os.path.join(workDir, 'common', 'commonlib'))
sys.path.append(os.path.join(workDir, 'legacy'))

try:
    from WhiteboxLib import WhiteboxLib
except Exception as err:
    log.cprint(str(err))

libObj = None


def OSConnect():
    global libObj
    log.debug("Entering WhiteboxLibAdapter procedure: OSConnect")
    libObj = WhiteboxLib()
    libObj.loginDevice()
    return


def ConnectESMB():
    global libObj
    log.debug("Entering WhiteboxLibAdapter procedure: ConnectESMB")
    libObj = WhiteboxLib()
    libObj.loginDevice1()
    return


def OSDisconnect():
    global libObj
    log.debug("Entering WhiteboxLibAdapter procedure: OSDisconnect")
    libObj.disconnectDevice()
    return


def ConnectDevice(device, console_type='bmc', login=False):
    global libObj
    log.debug("Entering WhiteboxLibAdapter procedure: Connect Device %s" % console_type)
    libObj = WhiteboxLib(device)
    console_list = {'os': [libObj.device.consoleIP, libObj.device.consolePort],
                    'bmc': [libObj.device.bmcConsoleIP, libObj.device.bmcConsolePort]}
    libObj.device.telnetConnect.open_connection(console_list[console_type][0], port=console_list[console_type][1])
    if login:
        libObj.whiteboxlib_tryLogin()
    return libObj


def DisconnectDevice(device, console_type='bmc'):
    global libObj
    log.debug("Entering WhiteboxLibAdapter procedure: Disconnect Device %s" % console_type)
    libObj = WhiteboxLib(device)
    return libObj.device.disconnect()
