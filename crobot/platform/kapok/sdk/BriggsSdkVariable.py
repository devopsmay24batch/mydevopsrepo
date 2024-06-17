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
from collections import OrderedDict
import DeviceMgr

SDK_PATH = '/root/sdk/R3181-J0001-01_V0.1.0_Briggs_SDK'
fail_pattern = ["fail", "ERROR", "cannot read file", "command not found", "No such file", "Unknown command"]
SDK_SCRIPT = 'auto_load_user.sh'
remote_shell_load_sdk = "./{}".format(SDK_SCRIPT)
daemon_mode = '-d'
credo_init = './c-phy/load_fw_init.sh -m'
credo_init_pattern = "FW load done"
sixteen_port_cmd_pattern = "credo config done"
PAM4_400G_32_sixteen_cmd = './c-phy/auto_load_user.sh -m 1-16:copper_1x400G'
PAM4_400G_32_cmd = './auto_load_user.sh -m 1-32:copper_1x400G'
PAM4_100G_128_sixteen_cmd = './c-phy/auto_load_user.sh -m 1-16:copper_4x100G'
PAM4_100G_128_cmd = './auto_load_user.sh -m 1-32:copper_4x100G'
NRZ_100G_32_sixteen_cmd = './c-phy/auto_load_user.sh -m 1-16:copper_1x100G'
NRZ_100G_32_cmd = './auto_load_user.sh -m 1-32:copper_1x100G'
NRZ_40G_32_sixteen_cmd = './c-phy/auto_load_user.sh -m 1-16:copper_1x40G'
NRZ_40G_32_cmd = './auto_load_user.sh -m 1-32:copper_1x40G'
NRZ_25G_128_sixteen_cmd = './c-phy/auto_load_user.sh -m 1-16:copper_4x25G'
NRZ_25G_128_cmd = './auto_load_user.sh -m 1-32:copper_4x25G'
NRZ_10G_128_sixteen_cmd = './c-phy/auto_load_user.sh -m 1-16:copper_4x10G'
NRZ_10G_128_cmd = './auto_load_user.sh -m 1-32:copper_4x10G'
knet_l2_show_cmd = './knet-l2-show'
knet_l2_show_finish_prompt = '\-\++[\s\S]+Total l2_entry count: 0'
knet_l2_show_pattern = ['.*key_type.*mac_addr.*mac_mask.*source.*group.*l2vni.*entry_dest.*entry_type.*fwd_policy.*ctc_policy.*user_cookie.*hitbit','Total l2_entry count: 0']
qsfp_cmd = 'qsfp'
qsfp_finish_prompt = 'Port 32+[\s\S]+ONIE'
qsfp_pattern = []
for i in range(1,33):
    regexp="Port[ \t]"+str(i)+":[\s]+Vendor:[ \t]LEONI|Port[ \t]"+str(i)+":[\s]+Vendor:[ \t]Molex"
    qsfp_pattern.append(regexp)
init_pass_pattern = {"Innovium Switch PCIe Driver opened successfully":"Innovium Switch PCIe Driver opened successfully"}
init_port_pattern = {"link True, pcs True":"link True,\s+pcs True"}
sdkConsole = 'IVM:0>'
CatReadMe = 'shell cat ReadMe\r\n'
CatReadMe_regexp = '.*SDK'
CatReadMe_pattern = ["R3181-J0001-01_V0.1.0_Briggs_SDK"]
ifcs = 'ifcs show version\r\n'
ifcs_regexp = 'Release.*Date'
ifcs_pattern = ["0.12.41"]
copper_1_8_9_22_23_32 = "-m \"1-8:Copper_4x25;9-22:Copper_2x100;23-32:Copper_4x25\""
copper_1_8_9_22_23_32_pattern = []
for i in range(1,33):
    regexp=".* "+str(i)+" .*ETH.*ISG.*1.*sysport.*[ \t]"+str(i)+"\).*25G.*DISABLED"
    copper_1_8_9_22_23_32_pattern.append(regexp)
for i in range(33,61):
    regexp=".* "+str(i)+" .*ETH.*ISG.*4.*sysport.*[ \t]"+str(i)+"\).*100G.*DISABLED"
    copper_1_8_9_22_23_32_pattern.append(regexp)
for i in range(61,101):
    regexp=".* "+str(i)+" .*ETH.*ISG.*1.*sysport.*[ \t]"+str(i)+"\).*25G.*DISABLED"
    copper_1_8_9_22_23_32_pattern.append(regexp)
copper_1_8_9_22_23_32_link_pattern = []
for i in range(1,33):
    regexp=".* "+str(i)+" .*ETH.*ISG.*1.*sysport.*[ \t]"+str(i)+"\).*25G.*UP"
    copper_1_8_9_22_23_32_link_pattern.append(regexp)
for i in range(33,61):
    regexp=".* "+str(i)+" .*ETH.*ISG.*4.*sysport.*[ \t]"+str(i)+"\).*100G.*UP"
    copper_1_8_9_22_23_32_link_pattern.append(regexp)
for i in range(61,101):
    regexp=".* "+str(i)+" .*ETH.*ISG.*1.*sysport.*[ \t]"+str(i)+"\).*25G.*UP"
    copper_1_8_9_22_23_32_link_pattern.append(regexp)
copper_1_20_21_24_25_32 = "-m \"1-20:Copper_1x100;21-24:Copper_4x10G;25-32:1x100G\""
copper_1_20_21_24_25_32_pattern = []
for i in range(1,21):
    regexp=".* "+str(i)+" .*ETH.*ISG.*4.*sysport.*[ \t]"+str(i)+"\).*100G.*DISABLED"
    copper_1_20_21_24_25_32_pattern.append(regexp)
for i in range(21,37):
    regexp=".* "+str(i)+" .*ETH.*ISG.*1.*sysport.*[ \t]"+str(i)+"\).*10G.*DISABLED"
    copper_1_20_21_24_25_32_pattern.append(regexp)
for i in range(37,45):
    regexp=".* "+str(i)+" .*ETH.*ISG.*4.*sysport.*[ \t]"+str(i)+"\).*100G.*DISABLED"
    copper_1_20_21_24_25_32_pattern.append(regexp)
copper_1_20_21_24_25_32_link_pattern = []
for i in range(1,21):
    regexp=".* "+str(i)+" .*ETH.*ISG.*4.*sysport.*[ \t]"+str(i)+"\).*100G.*UP"
    copper_1_20_21_24_25_32_link_pattern.append(regexp)
for i in range(21,37):
    regexp=".* "+str(i)+" .*ETH.*ISG.*1.*sysport.*[ \t]"+str(i)+"\).*10G.*UP"
    copper_1_20_21_24_25_32_link_pattern.append(regexp)
for i in range(37,45):
    regexp=".* "+str(i)+" .*ETH.*ISG.*4.*sysport.*[ \t]"+str(i)+"\).*100G.*UP"
    copper_1_20_21_24_25_32_link_pattern.append(regexp)
copper_1_20_21_24_25_32_4x100 = "-m \"1-20:Copper_1x100G;21-24:Copper_4x10G;25-32:Copper_4x100G\""
copper_1_20_21_24_25_32_4x100_pattern = []
for i in range(1,21):
    regexp=".* "+str(i)+" .*ETH.*ISG.*4.*sysport.*[ \t]"+str(i)+"\).*100G.*DISABLED"
    copper_1_20_21_24_25_32_4x100_pattern.append(regexp)
for i in range(21,37):
    regexp=".* "+str(i)+" .*ETH.*ISG.*1.*sysport.*[ \t]"+str(i)+"\).*10G.*DISABLED"
    copper_1_20_21_24_25_32_4x100_pattern.append(regexp)
for i in range(37,69):
    regexp=".* "+str(i)+" .*ETH.*ISG.*2.*sysport.*[ \t]"+str(i)+"\).*100G.*DISABLED"
    copper_1_20_21_24_25_32_4x100_pattern.append(regexp)
copper_1_20_21_24_25_32_4x100_link_pattern = []
for i in range(1,21):
    regexp=".* "+str(i)+" .*ETH.*ISG.*4.*sysport.*[ \t]"+str(i)+"\).*100G.*UP"
    copper_1_20_21_24_25_32_4x100_link_pattern.append(regexp)
for i in range(21,37):
    regexp=".* "+str(i)+" .*ETH.*ISG.*1.*sysport.*[ \t]"+str(i)+"\).*10G.*UP"
    copper_1_20_21_24_25_32_4x100_link_pattern.append(regexp)
for i in range(37,69):
    regexp=".* "+str(i)+" .*ETH.*ISG.*2.*sysport.*[ \t]"+str(i)+"\).*100G.*UP"
    copper_1_20_21_24_25_32_4x100_link_pattern.append(regexp)
PAM4_400G_32 = "-m PAM4_400G_32"
PAM4_100G_128 = "-m PAM4_100G_128"
NRZ_100G_32 = "-m NRZ_100G_32"
NRZ_40G_32 = "-m NRZ_40G_32"
NRZ_25G_128 = "-m NRZ_25G_128"
NRZ_10G_128 = "-m NRZ_10G_128"
NRZ_100G_64 = "-m NRZ_100G_64"
show_port_info = "ifcs show devport\r\n"
port_info_finish_prompt = "RECIRC"
shell_sleep_10 = "shell sleep 10\r\n"
PAM4_400G_32_source_preemphasis = 'source cel_cmds/preemphasis_PAM4_400G_32_LB_v4.txt\r\n'
PAM4_400G_32_source_preemphasis_regexp = 'Pre-emphasis setting.*'
PAM4_400G_32_source_preemphasis_pattern = ["Pre-emphasis setting.*"]
PAM4_400G_32_source_rx_gs = 'source cel_cmds/rx_gs_PAM4_400G_32_LB_v4.txt\r\n'
PAM4_400G_32_source_rx_gs_regexp = 'Applied gainshapes.*'
PAM4_400G_32_source_rx_gs_pattern = ["Applied gainshapes.*"]
source_cmd = 'source cel_cmds/misc_config.cmd\r\n'
source_cmd_regexp = 'Trace of source files.*'
source_cmd_pattern = ['Trace of source files.*']
clear_devport = 'ifcs clear counters devport\r\n'
clear_hardware = 'ifcs clear counters hardware\r\n'
start_traffic_500_cmd = 'diagtest snake start_traffic -n 500 -s 1518'
start_traffic_1000_cmd = 'diagtest snake start_traffic -n 1000 -s 1518'
check_rate = 'diagtest snake gen_report\r\n'
check_rate_id1 = 'diagtest snake gen_report -id 1\r\n'
check_rate_id2 = 'diagtest snake gen_report -id 2\r\n'
stop_traffic_cmd = 'diagtest snake stop_traffic'
check_counters = 'ifcs show counters devport filter nz\r\n'
remove_config_cmd = 'diagtest snake unconfig\r\n'
remove_config_regexp = 'Removing L2VNI members'
remove_config_pattern = ['Removing.*']
PAM4_400G_32_pattern = []
for i in range(1,33):
    regexp=".* "+str(i)+" .*ETH.*ISG.*8.*sysport.*[ \t]"+str(i)+"\).*400G.*DISABLED"
    PAM4_400G_32_pattern.append(regexp)
PAM4_100G_128_pattern = []
for i in range(1,129):
    regexp=".* "+str(i)+" .*ETH.*ISG.*2.*sysport.*[ \t]"+str(i)+"\).*100G.*DISABLED"
    PAM4_100G_128_pattern.append(regexp)
NRZ_100G_32_pattern = []
for i in range(1,33):
    regexp=".* "+str(i)+" .*ETH.*ISG.*4.*sysport.*[ \t]"+str(i)+"\).*100G.*DISABLED"
    NRZ_100G_32_pattern.append(regexp)
NRZ_40G_32_pattern = []
for i in range(1,33):
    regexp=".* "+str(i)+" .*ETH.*ISG.*4.*sysport.*[ \t]"+str(i)+"\).*40G.*DISABLED"
    NRZ_40G_32_pattern.append(regexp)
NRZ_25G_128_pattern = []
for i in range(1,129):
    regexp=".* "+str(i)+" .*ETH.*ISG.*1.*sysport.*[ \t]"+str(i)+"\).*25G.*DISABLED"
    NRZ_25G_128_pattern.append(regexp)
NRZ_10G_128_pattern = []
for i in range(1,129):
    regexp=".* "+str(i)+" .*ETH.*ISG.*1.*sysport.*[ \t]"+str(i)+"\).*10G.*DISABLED"
    NRZ_10G_128_pattern.append(regexp)
NRZ_100G_64_pattern = []
for i in range(1,65):
    regexp=".* "+str(i)+" .*ETH.*ISG.*4.*sysport.*[ \t]"+str(i)+"\).*100G.*DISABLED"
    NRZ_100G_64_pattern.append(regexp)
PAM4_400G_32_link_pattern = []
for i in range(1,33):
    regexp=".* "+str(i)+" .*ETH.*ISG.*8.*sysport.*[ \t]"+str(i)+"\).*400G.*UP"
    PAM4_400G_32_link_pattern.append(regexp)
PAM4_100G_128_link_pattern = []
for i in range(1,129):
    regexp=".* "+str(i)+" .*ETH.*ISG.*2.*sysport.*[ \t]"+str(i)+"\).*100G.*UP"
    PAM4_100G_128_link_pattern.append(regexp)
NRZ_100G_32_link_pattern = []
for i in range(1,33):
    regexp=".* "+str(i)+" .*ETH.*ISG.*4.*sysport.*[ \t]"+str(i)+"\).*100G.*UP"
    NRZ_100G_32_link_pattern.append(regexp)
NRZ_40G_32_link_pattern = []
for i in range(1,33):
    regexp=".* "+str(i)+" .*ETH.*ISG.*4.*sysport.*[ \t]"+str(i)+"\).*40G.*UP"
    NRZ_40G_32_link_pattern.append(regexp)
NRZ_25G_128_link_pattern = []
for i in range(1,129):
    regexp=".* "+str(i)+" .*ETH.*ISG.*1.*sysport.*[ \t]"+str(i)+"\).*25G.*UP"
    NRZ_25G_128_link_pattern.append(regexp)
NRZ_10G_128_link_pattern = []
for i in range(1,129):
    regexp=".* "+str(i)+" .*ETH.*ISG.*1.*sysport.*[ \t]"+str(i)+"\).*10G.*UP"
    NRZ_10G_128_link_pattern.append(regexp)
NRZ_100G_64_link_pattern = []
for i in range(1,65):
    regexp=".* "+str(i)+" .*ETH.*ISG.*4.*sysport.*[ \t]"+str(i)+"\).*100G.*UP"
    NRZ_100G_64_link_pattern.append(regexp)
prbs_tx_enable_cmd = 'source cel_cmds/prbs_tx_enable.cmd'
prbs_finish_pattern = 'Overscript.'
prbs_rx_enable_cmd = 'source cel_cmds/prbs_rx_enable.cmd'
prbs_ber_check_cmd = 'source cel_cmds/prbs_ber_check.cmd'
port_BER_tolerance= 1e-6
BER_port_pattern = "(\d+\.\d+e\-\d+)"
lt_enable_cmd = 'source cel_cmds/lt_enable.cmd'
rx_ctle_set_DAC_cmd = 'source cel_cmds/rx_ctle_set_DAC.cmd'
prbs_tx_31_53g_cmd = 'diagtest serdes prbs tx all all prbs31 53g'
prbs_rx_31_53g_30_1_cmd = 'diagtest serdes prbs rx all all prbs31 53g 30 1'
prbs_rx_31_53g_30_1_pattern = '\|[ \t]+32[ \t]+:[ \t]+7.*\d+\.\d+e\-\d+'
rack_ber_check_cmd = 'source ./cel_cmds/rack_ber_check.cmd'
rack_ber_check_pattern = '\|[ \t]+128[ \t]+:[ \t]+1.*\d+\.\d+e\-\d+[\s\S]+IVM:0>'
prbs_tx_31_25g_cmd = 'diagtest serdes prbs tx all all prbs31 25g'
prbs_rx_31_25g_5_cmd = 'diagtest serdes prbs rx all all prbs31 25g 5'
prbs_rx_31_25g_2160_cmd = 'diagtest serdes prbs rx all all prbs31 25g 2160'
prbs_rx_31_25g_5_pattern = '\|[ \t]+32[ \t]+:[ \t]+3.*\d+\.\d+e\-\d+[\s\S]+IVM:0>'
prbs_rx_31_25g_5_pattern_port128 = '\|[ \t]+128[ \t]+:[ \t]+0.*\d+\.\d+e\-\d+[\s\S]+IVM:0>'
prbs_rx_31_25g_2160_pattern = '\|[ \t]+32[ \t]+:[ \t]+3.*\d+\.\d+e\-\d+[\s\S]+IVM:0>'
prbs_rx_31_25g_2160_pattern_port128 = '\|[ \t]+128[ \t]+:[ \t]+0.*\d+\.\d+e\-\d+[\s\S]+IVM:0>'
prbs_tx_31_10g_cmd = 'diagtest serdes prbs tx all all prbs31 10g'
prbs_rx_31_10g_5_cmd = 'diagtest serdes prbs rx all all prbs31 10g 5'
prbs_rx_31_10g_2160_cmd = 'diagtest serdes prbs rx all all prbs31 10g 2160'
prbs_rx_31_10g_5_pattern = '\|[ \t]+32[ \t]+:[ \t]+3.*\d+\.\d+e\-\d+[\s\S]+IVM:0>'
prbs_rx_31_10g_5_pattern_port64 = '\|[ \t]+64[ \t]+:[ \t]+3.*\d+\.\d+e\-\d+[\s\S]+IVM:0>'
prbs_rx_31_10g_5_pattern_port128 = '\|[ \t]+128[ \t]+:[ \t]+0.*\d+\.\d+e\-\d+[\s\S]+IVM:0>'
prbs_rx_31_10g_2160_pattern = '\|[ \t]+32[ \t]+:[ \t]+3.*\d+\.\d+e\-\d+[\s\S]+IVM:0>'
prbs_rx_31_10g_2160_pattern_port64 = '\|[ \t]+64[ \t]+:[ \t]+3.*\d+\.\d+e\-\d+[\s\S]+IVM:0>'
prbs_rx_31_10g_2160_pattern_port128 = '\|[ \t]+128[ \t]+:[ \t]+0.*\d+\.\d+e\-\d+[\s\S]+IVM:0>'
SDK_FEC_SCRIPT = 'integrator_mode'
remote_shell_load_sdk_integrator = "./{}".format(SDK_FEC_SCRIPT)
integrator_400G_32 = "-m 32x400"
integrator_200G_32 = "-m 32x200"
integrator_100G_32 = "-m 32x100"
integrator_40G_32 = "-m 32x40"
integrator_100G_128 = "-m 128x100"
integrator_25G_128 = "-m 128x25"
integrator_10G_128 = "-m 128x10"
integrator_100G_64 = "-m 64x100"
integrator_400G_32_pattern = []
for i in range(1,33):
    regexp=".* "+str(i)+" .*ETH.*ISG.*8.*sysport.*[ \t]"+str(i)+"\).*400G.*UP.*KP"
    integrator_400G_32_pattern.append(regexp)
integrator_200G_32_pattern = []
for i in range(1,33):
    regexp=".* "+str(i)+" .*ETH.*ISG.*8.*sysport.*[ \t]"+str(i)+"\).*200G.*UP.*KP"
    integrator_200G_32_pattern.append(regexp)
integrator_100G_32_pattern = []
for i in range(1,33):
    regexp=".* "+str(i)+" .*ETH.*ISG.*4.*sysport.*[ \t]"+str(i)+"\).*100G.*UP.*KR"
    integrator_100G_32_pattern.append(regexp)
integrator_40G_32_pattern = []
for i in range(1,33):
    regexp=".* "+str(i)+" .*ETH.*ISG.*4.*sysport.*[ \t]"+str(i)+"\).*40G.*UP.*NONE"
    integrator_40G_32_pattern.append(regexp)
integrator_100G_128_pattern = []
for i in range(1,129):
    regexp=".* "+str(i)+" .*ETH.*ISG.*2.*sysport.*[ \t]"+str(i)+"\).*100G.*UP.*KP"
    integrator_100G_128_pattern.append(regexp)
integrator_25G_128_pattern = []
for i in range(1,129):
    regexp=".* "+str(i)+" .*ETH.*ISG.*1.*sysport.*[ \t]"+str(i)+"\).*25G.*UP.*FC"
    integrator_25G_128_pattern.append(regexp)
integrator_10G_128_pattern = []
for i in range(1,129):
    regexp=".* "+str(i)+" .*ETH.*ISG.*1.*sysport.*[ \t]"+str(i)+"\).*10G.*UP.*NONE"
    integrator_10G_128_pattern.append(regexp)
integrator_100G_64_pattern = []
for i in range(1,65):
    regexp=".* "+str(i)+" .*ETH.*ISG.*4.*sysport.*[ \t]"+str(i)+"\).*100G.*UP.*KR"
    integrator_100G_64_pattern.append(regexp)
sfp_detect_tool_cmd = 'sfp_detect_tool'
sfp_detect_tool_finish_prompt = 'P32:[ \t]+.*'
sfp_detect_tool_pattern = []
for i in range(1,33):
    regexp="P"+str(i)+":[ \t]Copper_400G"
    sfp_detect_tool_pattern.append(regexp)