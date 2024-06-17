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
import Const
import Logger as log

class BmcLib:

    def __init__(self):
        import DeviceMgr
        self.device = DeviceMgr.getDevice()

    ############### bmc related keywords begin

    # here just an example
    def displayBmcversion(self):
        log.debug("Entering Device class procedure: displayBmcversion")
        version = self.device.sendCmd("uname -a", Const.BOOT_MODE_BMC)  # need replace it with minipack2's
        LogMsg = "Version:\r\n"
        LogMsg += version
        log.debug(LogMsg)
        time.sleep(1)
        return version

    def sendTest(self):
        return self.device.sendMsg("echo 'in bmc' > ttt \n")

    ############### bmc related keywords end

    ############### wrapper of Device related keyword begin, just transmit the calling to Device Object
    def loginDevice(self):
        self.device.loginBmc()

    def disconnectDevice(self):
        return self.device.disconnectBmc()

    ############### wrapper of Device related keyword end
