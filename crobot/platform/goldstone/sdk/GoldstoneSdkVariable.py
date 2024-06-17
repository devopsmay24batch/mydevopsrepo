# LEGALESE:   "Copyright (C) 2019-2020, Celestica Corp. All rights reserved." #
#                                                                             #
# This source code is confidential, proprietary, and contains trade           #
# secrets that are the sole property of Celestica Corp.                       #
# Copy and/or distribution of this source code or disassembly or reverse      #
# engineering of the resultant object code are strictly forbidden without     #
# the written consent of Celestica Corp.                                      #
#                                                                             #
###############################################################################
# It's better not to call functions in variable files(e.g. BSP_DRIVER = SwImage.getSwImage("BSP_DRIVER")).
# Any error during the calling will make all the tests fail. We can use it in functions of lib/keywords files
# We have encountered this type of issue many many times in facebook projects.

import os
import Logger as log
try:
    from Device import Device
    import DeviceMgr
except Exception as err:
    log.cprint(str(err))
device = DeviceMgr.getDevice()

sdk_path = '/root/R4035-J0002-01_V1.4_Goldstone_SDK'

devicename       = os.environ.get("deviceName", "")
hostPrompt       = DeviceMgr.getDevice(devicename).get('promptDiagOS')
sdkBCMPrompt     = 'BCM.0>'
sdkBCMdshPrompt  = 'ssdklt.0>'
native_mode      = '16x1x400'
maxBERepow       = 6
lb_edb           = 'edb'
lb_phy           = 'phy'
lb_mac           = 'mac'
serdes_version   = 'D003_06'

portMap =  {'16x2x400':{'prefix':'cd','numPorts':32},
            '16x1x400':{'prefix':'cd','numPorts':16},
            '16x4x200':{'prefix':'cd','numPorts':64}, 
            '16x8x100':{'prefix':'ce','numPorts':128},
            '16x4x100':{'prefix':'ce','numPorts':64},
            '16x2x100':{'prefix':'ce','numPorts':32},
            '16x8x50':{'prefix':'xe','numPorts':128},
            '16x4x50':{'prefix':'xe','numPorts':64},
            '16x2x40':{'prefix':'xe','numPorts':32},
            '16x8x25':{'prefix':'xe','numPorts':128},
            '16x8x10':{'prefix':'xe','numPorts':128},
            '16x2x200':{'prefix':'cd','numPorts':32}}
