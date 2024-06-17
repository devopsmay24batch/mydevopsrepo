###############################################################################
# LEGALESE:   "Copyright (C) 2019-2022, Celestica Corp. All rights reserved." #
#                                                                             #
# This source code is confidential, proprietary, and contains trade           #
# secrets that are the sole property of Celestica Corp.                       #
# Copy and/or distribution of this source code or disassembly or reverse      #
# engineering of the resultant object code are strictly forbidden without     #
# the written consent of Celestica Corp.                                      #
#                                                                             #
###############################################################################

import os
import re

from common.sdk.Sdk_variable import BCM_promptstr

show_c_cmd = "show c"
clear_c_cmd = "clear c"
ps_cmd = "ps"

fail_pattern = [ "ERROR", "Failed", "cannot read file", "command not found", "No such file", "Unknown command"]

SDK_SCRIPT = "auto_load_user.sh"

kill_bcm = "killall -9 bcm.user"

sdk_path = '/root/Diag/lagavulin/SDK'

port_status_patterns = []
for i in range(0,36):
    regexp="ge" + str(i) +".*?down.*?10M.*?FD.*?Yes.*?Forward.*?TX RX.*?SGMII 12284"
    port_status_patterns.append(regexp)
for i in range(0,12):
    regexp="xe" + str(i) +".*?up.*?10G.*?FD.*?No.*?Forward.*?TX RX.*?XFI 12284"
    port_status_patterns.append(regexp)
for i in range(0,2):
    regexp="ce" + str(i) +".*?up.*?100G.*?FD.*?No.*?Forward.*?TX RX.*?CAUI4 12284"
    port_status_patterns.append(regexp)
regexp="ce" + str(3) +".*?up.*?10G.*?FD.*?No.*?Forward.*?TX RX.*?CAUI4 12284"
port_status_patterns.append(regexp)

epdm_link_patterns = []
epdm_link_patterns. append("miura.*?xe0.*?0x1.*?0x20.*?10000.*?SFI.*?XFI.*?UP.*?UP")
epdm_link_patterns. append("miura.*?xe1.*?0x2.*?0x20.*?10000.*?SFI.*?XFI.*?UP.*?UP")
epdm_link_patterns. append("miura.*?xe2.*?0x4.*?0x20.*?10000.*?SFI.*?XFI.*?UP.*?UP")
epdm_link_patterns. append("miura.*?xe3.*?0x8.*?0x20.*?10000.*?SFI.*?XFI.*?UP.*?UP")
epdm_link_patterns. append("miura.*?xe4.*?0x1.*?0x24.*?10000.*?SFI.*?XFI.*?UP.*?UP")
epdm_link_patterns. append("miura.*?xe5.*?0x2.*?0x24.*?10000.*?SFI.*?XFI.*?UP.*?UP")
epdm_link_patterns. append("miura.*?xe6.*?0x4.*?0x24.*?10000.*?SFI.*?XFI.*?UP.*?UP")
epdm_link_patterns. append("miura.*?xe7.*?0x8.*?0x24.*?10000.*?SFI.*?XFI.*?UP.*?UP")
epdm_link_patterns. append("miura.*?xe8.*?0x1.*?0x28.*?10000.*?SFI.*?XFI.*?UP.*?UP")
epdm_link_patterns. append("miura.*?xe9.*?0x2.*?0x28.*?10000.*?SFI.*?XFI.*?UP.*?UP")
epdm_link_patterns. append("miura.*?xe10.*?0x4.*?0x28.*?10000.*?SFI.*?XFI.*?UP.*?UP")
epdm_link_patterns. append("miura.*?xe11.*?0x8.*?0x28.*?10000.*?SFI.*?XFI.*?UP.*?UP")
epdm_link_patterns. append("europa.*?ce0.*?0xf.*?0x0.*?100000.*?CR4.*?CAUI4_C2C.*?UP.*?UP")

phy_info_patterns = []
for i in range (0, 12):
    phy_info_patterns.append("miura.*?xe" + str(i) + ".*?0xd006/0x600d.*?MIUR_1\.10")
phy_info_patterns.append("europa.*?ce" + str(0) + ".*?0xd010/0x600d.*?EURO_4\.2")

mdio_advisor_pattern = r'rate_ext_mdio_divisor=0x30'

uplink_prbs_get = "phy diag ce0 prbs get"
uplink_prbs_patterns = [
    "ce0.*?GENERATOR.*?Enable",
    "PRBS CHECKER\(RX\): Enable",
    "PRBS LOCK: 1",
    "PRBS WAS LOCK LOSS: YES",
    "PRBS ERROR COUNT: 0",
    "Phy 0x0 lanes 0x0f: prbs locked",
    "Phy 0x0 lanes 0x0f: PRBS OK!"
]
