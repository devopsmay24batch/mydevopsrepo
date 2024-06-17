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
import Logger as log
from Device import Device

class DellDevice(Device):

    def __init__(self, deviceDict):
        super().__init__(deviceDict)
        log.debug("Entering DellPlatformDevice class procedure: __init__")

    ############ dell platform specific implementations, overwrite the functions of parent class begin:
    def displayDiagOSVersion(self):
        log.debug("Entering DeviceDellPlatform class procedure: displayDiagOSVersion")
        version = self.sendCmd("sh_ver", self.promptDiagOS)
        LogMsg = "Version:\r\n"
        LogMsg += version
        log.debug(LogMsg)
        time.sleep(1)
        return version


    ############ dell platform specific implementations, overwrite the function of parent class end


    ############ new added funcitons for dell platform  begin:



    ############ new added funcitons for dell platform  end




