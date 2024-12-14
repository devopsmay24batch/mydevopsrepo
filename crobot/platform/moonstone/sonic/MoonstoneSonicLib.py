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
import sys
import os
import re
import traceback
import CRobot
import time
import pexpect
from time import sleep
workDir = CRobot.getWorkDir()
sys.path.append(workDir)
sys.path.append(os.path.join(workDir, 'common', 'commonlib'))
sys.path.append(os.path.join(workDir, 'platform', 'moonstone'))
sys.path.append(os.path.join(workDir, 'platform', 'moonstone','diag'))
sys.path.append(os.path.join(workDir, 'platform', 'moonstone','bios'))
from crobot import Logger as log
from  MoonstoneDiagLib import rebootToSonic
try:
    from common.commonlib import CommonLib
    from common.commonlib import CommonKeywords
    from MoonstoneSonicVariable import *
    from MoonstoneCommonVariable import *
    import DeviceMgr
    from Device import Device
    from crobot.SwImage import SwImage
    from crobot.Decorator import logThis
    import MOONSTONECommonLib
    import WhiteboxPowerCycler
except Exception as err:
    log.cprint(traceback.format_exc())

device = DeviceMgr.getDevice()
from SwImage import SwImage
from functools import partial
run_command = partial(CommonLib.run_command, deviceObj=device, prompt=device.promptDiagOS)

@logThis
def loginDevice():
    device.loginDiagOS()
    device.sendCmd('sudo su')


@logThis
def sonicDisconnect():
    return device.disconnect()

