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
import Logger as log

try:
    import LibMgr
except Exception as err:
    log.cprint(str(err))

libObj = None

def BmcConnect():
    global libObj
    log.debug("Entering BmcTestCase procedure: BmcConnect")
    libObj = LibMgr.getBmcLib()
    libObj.loginDevice()
    return

def BmcDisconnect():
    global libObj
    log.debug("Entering BmcTestCase procedure: BmcDisconnect")
    libObj.disconnectDevice()
    return

def sendTest():
    libObj.sendTest()