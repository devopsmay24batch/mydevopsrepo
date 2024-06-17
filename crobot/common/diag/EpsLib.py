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
import YamlParse
from Device import Device

import PoeTester

def getEpsList(epsList):
    testers = []
    epsDict = YamlParse.getEpsInfo()
    for p in epsList:
        tester = PoeTester(epsDict[p])
        testers.append(tester)
    return testers

class EpsLib:
    device = Device()
    epsList = getEpsList(device.epsList)

    def __init__(self):
        pass

