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

class OpenBmcLib():
    def __init__(self):
        log.debug("Entering OpenBmcLib class procedure: __init__")
        import DeviceMgr
        self.device = DeviceMgr.getDevice()

    def loginDevice(self):
        self.device.loginBmc()

    def disconnectDevice(self):
        return self.device.disconnect()
