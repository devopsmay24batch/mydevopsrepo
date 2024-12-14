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
import time
from DiagLib import DiagLib
import Logger as log
import Const

class FacebookDiagLib(DiagLib):
    def __init__(self):
        super().__init__()

    def powerCycleDeviceToDiagOS(self):
        log.debug("Entering FacebookDiagLib class procedure: powerCycleDeviceToDiagOS")
        return self.device.powerCycleDeviceToDiagOS()

