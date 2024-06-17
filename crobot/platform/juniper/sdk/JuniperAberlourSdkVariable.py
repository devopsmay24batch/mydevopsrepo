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
sdk_path = '/root/Diag/aberlour/SDK'


fail_pattern =['ERROR', 'Failed', 'cannot read file', 'command not found','No such file', 'Unknown command',"not found",
"Command exited with non-zero status","fail"]

SDK_SCRIPT="auto_load_user.sh "
port_status_patterns=[]

phy_info_patterns = []
for i in range (0, 24):
    phy_info_patterns.append("miura.*?xe" + str(i) + ".*?0xd008/0x600d.*?MIUR_2\.3")
phy_info_patterns.append("europa.*?ce" + str(0) + ".*?0xd010/0x600d.*?EURO_4\.2")
phy_info_patterns.append("europa.*?ce" + str(1) + ".*?0xd010/0x600d.*?EURO_4\.2")
phy_info_patterns.append("europa.*?ce" + str(2) + ".*?0xd010/0x600d.*?EURO_4\.2")

mdio_advisor_pattern = "rate_ext_mdio_divisor.*=0x30"


prbs_get_pattern="ce.*?PRBS OK!"

prbs_ce_pattern=["ce.*?PRBS GENERATOR.*?Enable",
"PRBS CHECKER.*?Enable",
"PRBS LOCK: 1",
"PRBS WAS LOCK LOSS: YES",
"PRBS ERROR COUNT: 0",
"Phy.*?prbs locked",
"Phy.*?PRBS OK!"]

prbs_sys_ce_pattern=[]
prbs_sys_ce_pattern.extend(prbs_ce_pattern)
prbs_sys_ce_pattern.extend(prbs_ce_pattern)

ps_40G_pattern=[]
for i in range(24):
    ps_40G_pattern.append("xe.*?up.*?10G.*?")
ps_40G_pattern.append("xe.*?up.*?40G.*?")
ps_40G_pattern.append("xe.*?up.*?40G.*?")
ps_40G_pattern.append("xe.*?up.*?40G.*?")


epdm_40G_pattern=[]
for i in range(24):
    epdm_40G_pattern.append("miura.*?10000.*?UP.*?")
epdm_40G_pattern.append("europa.*?40000.*?UP.*?")
epdm_40G_pattern.append("europa.*?40000.*?UP.*?")
epdm_40G_pattern.append("europa.*?40000.*?UP.*?")

A_100G_uplink_packet_pattern="MIB.*?26.*?0.*"

epdm_pattern=[]
for i in range(24):
    epdm_pattern.append("miura.*?10000.*?UP.*?")
epdm_pattern.append("europa.*?100000.*?UP.*?")
epdm_pattern.append("europa.*?100000.*?UP.*?")
epdm_pattern.append("europa.*?100000.*?UP.*?")

prbs_xe_pattern=["xe.*?PRBS GENERATOR.*?Enable",
"PRBS CHECKER.*?Enable",
"PRBS LOCK: 1",
"PRBS WAS LOCK LOSS: YES",
"PRBS ERROR COUNT: 0",
"Phy.*?prbs locked",
"Phy.*?PRBS OK!"]

all_prbs_get_pattern=["xe.*?PRBS OK!.*"]*24


ps_100G_pattern=[]
for i in range(24):
    ps_100G_pattern.append("xe"+str(i)+".*?"+str(i+1)+".*?up.*?10G.*?")
ps_100G_pattern.append("ce0.*?up.*?100G.*?")
ps_100G_pattern.append("ce1.*?up.*?100G.*?")
ps_100G_pattern.append("ce2.*?up.*?100G.*?")

uplink_100g_led_pattern1="Port27 100G Linespeed test.*?PASS"
linespeed_test_pattern="Linespeed Test PASS"

uplink_40g_led_pattern1="Port27 40G Linespeed test.*?PASS"

stacking_100g_led_pattern1="Port25 100G Linespeed test.*?PASS"
stacking_100g_led_pattern2="Port26 100G Linespeed test.*?PASS"

stacking_40g_led_pattern1="Port25 40G Linespeed test.*?PASS"
stacking_40g_led_pattern2="Port26 40G Linespeed test.*?PASS"

ps_10g_link_pattern=[]
for port in range(24):
    value="xe"+str(port)+".*?"+str(port+1)+".*?up.*?10G.*?"
    ps_10g_link_pattern.append(value)

epdm_10g_link_pattern=[]
for port in range(24):
    value="miura.*?xe"+str(port)+".*?"+str(port+1)+".*?10000.*?"
    epdm_10g_link_pattern.append(value)

ps_1g_link_pattern=[]
for port in range(24):
    value="ge"+str(port)+".*?"+str(port+1)+".*?up.*?1G.*?"
    ps_1g_link_pattern.append(value)

epdm_1g_link_pattern=[]
for port in range(24):
    value="miura.*?ge"+str(port)+".*?"+str(port+1)+".*?1000.*?"
    epdm_1g_link_pattern.append(value)

speed_10g_to_1g_pattern=[]
for i in range(24):
    value1="Configured speed:10000 speed:1000 interface:19 side:1"
    value2="Configured speed:1000 speed:1000 interface:19 side:2"
    speed_10g_to_1g_pattern.append(value1)
    speed_10g_to_1g_pattern.append(value2)

fec_enable_pattern="FEC enable=1"
fec_disable_pattern="FEC enable=0"

phy_diag_ce_dict = {"FEC ENA:": "(.*?)$",}
phy_diag_xe0_pattern={"PCS SYNC":"(.*?)$", "PCS LINK":"(.*?)$", }

portmin_pattern=[]
for i in range(24):
    value1="Configured speed:10000 speed:1000 interface:.*? side:1"
    value2="Configured speed:1000 speed:1000 interface:.*? side:2"
    portmin_pattern.append(value1)
    portmin_pattern.append(value2)

portmax_pattern=[]
for i in range(24):
    value1="Configured speed:10000 speed:1000 interface:.*? side:1"
    value2="Configured speed:1000 speed:1000 interface:.*? side:2"
    portmax_pattern.append(value1)
    portmax_pattern.append(value2)


downlink_serde_port="D102_09"
uplink_serde_port="D103_18"


enable_macsec_pattern=[]
value1="CLPORT_CLMAC_CTRL.*?If_side=\[1\].*?PHY-ID.*?Reg_Address.*?Data.*?"
value2="CLPORT_CLMAC_CTRL.*?If_side=\[0\].*?PHY-ID.*?Reg_Address.*?Data.*?"

enable_macsec_pattern.append(value1)
enable_macsec_pattern.append(value1)
enable_macsec_pattern.append(value2)
enable_macsec_pattern.append(value2)


linespeed_24h_traffic_pattern_start=[]
for port in range(1,25):
    value="Start port"+str(port)+" linespeed test with speed 10G"
    linespeed_24h_traffic_pattern_start.append(value)

for port in range(25,28):
    value="Start port"+str(port)+" linespeed test with speed 100G"
    linespeed_24h_traffic_pattern_start.append(value)

for port in range(1,28):
    value="Port"+str(port)+" Link UP..."
    linespeed_24h_traffic_pattern_start.append(value)


linespeed_24h_traffic_pattern_end=[]
for port in range(1,25):
    value="Port"+str(port)+" 10G Linespeed test.*?PASS"
    linespeed_24h_traffic_pattern_end.append(value)

for port in range(25,28):
    value="Port"+str(port)+" 100G Linespeed test.*?PASS"
    linespeed_24h_traffic_pattern_end.append(value)

linespeed_24h_traffic_pattern_end.append("Linespeed Test PASS")

enable_macsec_counters_pattern_dict={"secy stats:":2, "sa stats:":2, "ifc stats:":2, "rxcam stats:":1}

disable_macsec_pattern=[]
value1="CLPORT_CLMAC_CTRL.*?If_side=\[0\].*?PHY-ID.*?Reg_Address.*?Data.*?"
value2="CLPORT_CLMAC_CTRL.*?If_side=\[1\].*?PHY-ID.*?Reg_Address.*?Data.*?"

disable_macsec_pattern.append(value1)
disable_macsec_pattern.append(value1)
disable_macsec_pattern.append(value2)
disable_macsec_pattern.append(value2)

filename1="All_Ports_EnableDisable_Stress_Test_24X.sh"
enale_disable_1000_times_done_pattern="1000 times all port down-up-traffic test end"

filename2="SDK_Re-Init_Stress_Test_100G_24X.sh"
sdk_reinit_stress_1000_times_done_pattern="SDK Re-Init Stress Test 1000 times test end"

# TC_9.68
linespeed_10G_traffic_pattern_start=[]
for port in range(1,25):
    value="Start port"+str(port)+" linespeed test with speed 10G"
    linespeed_10G_traffic_pattern_start.append(value)


for port in range(1,25):
    value="Port"+str(port)+" Link UP..."
    linespeed_10G_traffic_pattern_start.append(value)


linespeed_10G_traffic_pattern_end=[]
for port in range(1,25):
    value="Port"+str(port)+" 10G Linespeed test.*?PASS"
    linespeed_10G_traffic_pattern_end.append(value)


linespeed_10G_traffic_pattern_end.append("Linespeed Test PASS")

linespeed_10G_dict_pattern ={}
for port in range(1,25):
    key="Port"+str(port)+" 10G Linespeed test"
    linespeed_10G_dict_pattern[key]="(.*?)$"


tpok_rpok_dict_pattern={"TPOK":"(.*?)$", "RPOK":"(.*?)$","EPKT":"(.*?)$"}


#TC_9.70

linespeed_100G_uplink_traffic_pattern_start=["Start port27 linespeed test with speed 100G","Port27 Link UP..."]
linespeed_100G_uplink_traffic_pattern_end=["Port27 100G Linespeed test.*?PASS", "Linespeed Test PASS"]
linespeed_100G_uplink_dict_pattern={"Port27 100G Linespeed test":"(.*?)$"}

#TC_9.71
linespeed_100G_stacking_traffic_pattern_start=["Start port25 linespeed test with speed 100G",
        "Start port26 linespeed test with speed 100G", "Port25 Link UP...", "Port26 Link UP..."]
linespeed_100G_stacking_traffic_pattern_end=["Port25 100G Linespeed test.*?PASS","Port26 100G Linespeed test.*?PASS", "Linespeed Test PASS"]

linespeed_100G_stacking_dict_pattern={"Port25 100G Linespeed test":"(.*?)$","Port26 100G Linespeed test":"(.*?)$"}
