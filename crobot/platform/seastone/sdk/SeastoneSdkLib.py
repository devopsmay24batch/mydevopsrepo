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
import Const
import re
from Decorator import *
import time
from functools import partial
import YamlParse
import SEASTONECommonLib

workDir = CRobot.getWorkDir()
sys.path.append(os.path.join(workDir, 'common', 'commonlib'))
sys.path.append(os.path.join(workDir, 'platform/seastone'))

import CommonLib
try:
    from Device import Device
    import DeviceMgr
except Exception as err:
    log.cprint(str(err))
device = DeviceMgr.getDevice()
run_command = partial(CommonLib.run_command, deviceObj=device, prompt=device.promptDiagOS)




def OnieConnect():
    log.debug("Entering OnieTestCase procedure: OnieConnect")
    device.loginOnie()
    return

def OnieDisconnect():
    global libObj
    log.debug("Entering OnieTestCase procedure: OnieDisconnect")
    device.disconnect()
    return

