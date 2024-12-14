###############################################################################
# LEGALESE:   "Copyright (C) 2021, Celestica Corp. All rights reserved."      #
#                                                                             #
# This source code is confidential, proprietary, and contains trade           #
# secrets that are the sole property of Celestica Corp.                       #
# Copy and/or distribution of this source code or disassembly or reverse      #
# engineering of the resultant object code are strictly forbidden without     #
# the written consent of Celestica Corp.                                      #
#                                                                             #
###############################################################################

*** Keywords ***
FPGA remove, set register, rescan and modprobe
    unload kernel module
    ...  console=${diagos_mode}
    ...  module=int_switchboard_fpga
    execute command and verify exit code
    ...  console=${diagos_mode}
    ...  command=echo 1 > /sys/devices/pci0000:00/0000:00:1c.0/0000:08:00.0/remove
    execute command and verify exit code
    ...  console=${diagos_mode}
    ...  command=echo 0xa10a 0x0 > /sys/devices/platform/AS24128D.cpldb/setreg
    execute command and verify exit code
    ...  console=${diagos_mode}
    ...  command=echo 1 > /sys/devices/pci0000:00/0000:00:1c.0/rescan
    kernel module probe
    ...  module=int_switchboard_fpga
