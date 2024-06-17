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
from collections import OrderedDict
from SwImage import SwImage
try:
    from Device import Device
    import DeviceMgr
except Exception as err:
    log.cprint(str(err))
device = DeviceMgr.getDevice()
SDK = SwImage.getSwImage("SDK")
sdkname = SDK.newImage
BRIXIA=SwImage.getSwImage("BRIXIA_DIAG")
new_onie=BRIXIA.newImage


#### variable define begin ####

#TC_12_ONIE_System_Information

sysinfo="x86\_64-cel\_brixia-r0"
sysinfo_version="2020.08.0.0.2"

fdisk=['Disk /dev/sda.*GB',
        '/dev/sda1.*']
ifconfig=['eth0.*','UP.*BROADCAST MULTICAST.*MTU:1500',
          'eth1.*','UP.*BROADCAST RUNNING MULTICAST.*MTU:1500',
          'lo.*','UP.*LOOPBACK RUNNING.*MTU:65536']


##tcs 02

new_sonic=['Welcome to LinuxBoot\'s Menu',
'Enter a number to boot a kernel:',
'01. '+new_onie,
'02. Reboot',
'03. Enter a LinuxBoot shell']


#tcs01
linux_menu=['01. embed',
'02. rescue',
'03. \"ONIE: Rescue\"',
'04. Reboot',
'05. Enter a LinuxBoot shell']


menu_02=['Welcome to LinuxBoot\'s Menu',
      'Enter a number to boot a kernel:',
      '01. SONiC-OS-202106-brixia.pb.*',
      '02. Reboot',
      '03. Enter a LinuxBoot shell']

DHCP_IP="192.168.*"
onie_stop="Stopping.*done."
OS_Install="100%"











