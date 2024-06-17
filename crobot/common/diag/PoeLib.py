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

def getPoeTesters(poeTesters):
    testers = []
    testerDict = YamlParse.getPoeTesterInfo()
    for p in poeTesters:
        tester = PoeTester(testerDict[p])
        testers.append(tester)
    return testers

class PoeLib:
    device = Device()
    poeTesters = getPoeTesters(device.poeTesters)

    def __init__(self):
        pass

    def setUp(self):
        for tester in PoeLib.poeTesters:
            tester.login()

        PoeLib.device.login()

    def tearDown(self):
        for tester in PoeLib.poeTesters:
            tester.disconnoct()
        PoeLib.device.disconnoct()

    ############### poeTesters  related keywords begin


    ############### poeTesters related keywords end





    ############### host related keywords begin
    def sendTest(self):
        return PoeLib.device.sendCmd("echo 'test' > ttt")

    ############### host related keywords end



    ############### wrapper of Device related keyword begin, just transmit the calling to Device Object


    ############### wrapper of Device related keyword end



