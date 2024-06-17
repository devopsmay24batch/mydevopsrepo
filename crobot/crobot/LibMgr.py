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

curDir = os.path.dirname(os.path.abspath(__file__))
parentDir = os.path.dirname(curDir)
sys.path.append(parentDir)
sys.path.append(os.path.join(parentDir, 'common'))
sys.path.append(os.path.join(parentDir, 'common', 'diag'))
sys.path.append(os.path.join(parentDir, 'common', 'bmc'))
sys.path.append(os.path.join(parentDir, 'common', 'onie'))

import Const
import YamlParse
import Logger as log

try:
    from DiagLib import DiagLib
    from BmcLib import BmcLib
    from OnieLib import OnieLib
    from DellDiagLib import DellDiagLib
    # from FacebookDiagLib import FacebookDiagLib
except Exception as err:
    log.cprint(str(err))

def getDiagLib():
    deviceName = os.environ['deviceName']
    currentDevice = YamlParse.getDeviceInfo()
    deviceDict = currentDevice[deviceName]
    platform = deviceDict['platform']
    log.cprint(platform)
    if platform == Const.PLATFORM_DELL:
        return DellDiagLib()
    elif platform == Const.PLATFORM_FACEBOOK:
        return FacebookDiagLib()
    else:
        return DiagLib()

def getBmcLib():
    return BmcLib()

def getOnieLib():
    return OnieLib()

