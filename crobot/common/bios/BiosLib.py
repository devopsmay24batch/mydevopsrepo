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
from Device import Device

class BiosLib:
    device = Device()

    def __init__(self):
        pass

############### bios related keywords begin

# here just an example
def displayBmcversion(self):
    version = BiosLib.device.sendCmd("show_ver")
    log.cprint("versin: " + version)
    return version

def sendTest(self):
    return BiosLib.device.sendCmd("echo 'test' > ttt")

############### bios related keywords end

############### wrapper of Device related keyword begin, just transmit the calling to Device Object
def loginDevice(self):
    BiosLib.device.loginBios()
    # pass

def disconnectDevice(self):
    return BiosLib.device.disconnectBios()

############### wrapper of Device related keyword end
