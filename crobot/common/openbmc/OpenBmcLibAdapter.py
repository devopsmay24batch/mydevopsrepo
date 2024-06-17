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
    from OpenBmcLib import OpenBmcLib
except Exception as err:
    log.cprint(str(err))

libObj = None

def BmcConnect():
    global libObj
    log.debug("Entering FacebookBmcLibAdapter procedure: BmcConnect")
    libObj = OpenBmcLib()
    libObj.loginDevice()
    return

def BmcDisconnect():
    global libObj
    log.debug("Entering FacebookBmcLibAdapter procedure: BmcDisconnect")
    libObj.disconnectDevice()
    return

# def switchToOpenBmc():
#     global libObj
#     log.debug("Entering FacebookBmcLibAdapter procedure: switchToOpenBmc")
#     libObj.switchToOpenBmc()
#     return
#
# def switchToCentos():
#     global libObj
#     log.debug("Entering FacebookBmcLibAdapter procedure: switchToCentos")
#     libObj.disconnectDevice()
#     return