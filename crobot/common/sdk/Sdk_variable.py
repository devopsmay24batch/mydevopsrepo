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
##### Variable file used for Wedge400_sdk.robot #####
import os
from collections import OrderedDict
import DeviceMgr
from SwImage import SwImage

eth_int_params = {
    'interface' : 'eth0',
    }#####differ
# Get the variable from the DeviceInfo.yaml
pc_info = DeviceMgr.getServerInfo('PC')
scp_username = pc_info.scpUsername
scp_password = pc_info.scpPassword
scp_ip = pc_info.managementIP
scp_ipv6 = pc_info.managementIPV6
# scp_filepath_test = "/home/Prapatsorn/automation/Wedge400C/sdk/IMAGES"
# sdk_package = ['wedge400c_sdk_v0.2.3.zip']
#sdk_soc_dir = '/home/automation/Auto_Test/automation/FB-Wedge400/autotest/SDK'
sdk_soc_dir_w400 = SwImage.getSwImage(SwImage.SDK).hostImageDir
sdk_soc_files = '*.soc'
ETH_TOOL = 'ifconfig eth0'
DHCP_TOOL = 'dhclient -6 eth0'
sdk_working_dir = '/usr/local/cls_diag/SDK'
SDK_PATH = sdk_working_dir
SDK_SCRIPT = 'auto_load_user.py'

DUT_PHASE = 'EVT2'
openbmc_mode="openbmc"
centos_mode="centos"
tmp_output_file_on_dut = '/tmp/dut_output'
check_log_script_file_list = ['check_log.py']
check_log_script_file_dst_path = "/tmp/"
check_log_pass_pattern = {"Checking log PASSED":"Checking log PASSED"}

qsfpDDPortNum = list(range(0, 16))
qsfp56PortNum = list(range(16, 48))
qsfp2x25PortNum = list(range(16, 80))

ALL_PORT_NUM = qsfpDDPortNum + qsfp56PortNum
ALL_PORT_NUM_2X2X25G = qsfpDDPortNum + qsfp2x25PortNum
ALL_PORT_COUNT = len(ALL_PORT_NUM)
ALL_PORT_COUNT_2X2X25G = len(ALL_PORT_NUM_2X2X25G)

ok_keyword = r'-do_reinit_test-.*TEST.*?PASS'
true_keyword = 'PASS'
sdkConsole = '>>>'
fail_pattern = [ "ERROR", "cannot read file", "command not found", "No such file", "Unknown command"]
fail_dict = { #"fail":"fail",
              "ERROR":"ERROR",
              "cannot read file":"cannot read file",
              "command not found":"command not found"
              }
portStatusDD_8X50G_QSFP_4X50G = {}
for i in ALL_PORT_NUM:
    portStatusDD_8X50G_QSFP_4X50G[i] = {}
    if i in qsfpDDPortNum:
        portStatusDD_8X50G_QSFP_4X50G[i]['link_name'] = '8x50G'
    elif i in qsfp56PortNum:
        portStatusDD_8X50G_QSFP_4X50G[i]['link_name'] = '4x50G'
    portStatusDD_8X50G_QSFP_4X50G[i]['link_status'] = 'True'
    portStatusDD_8X50G_QSFP_4X50G[i]['pcs_status'] = 'True'
    if i == 0:
        portStatusDD_8X50G_QSFP_4X50G[i]['link_name'] = '4x50G'
    if i == 16:
        portStatusDD_8X50G_QSFP_4X50G[i]['link_name'] = '8x50G'

portStatusDD_8X50G_QSFP_4X25G = {}
for i in ALL_PORT_NUM:
    portStatusDD_8X50G_QSFP_4X25G[i] = {}
    if i in qsfpDDPortNum:
        portStatusDD_8X50G_QSFP_4X25G[i]['link_name'] = '8x50G'
    elif i in qsfp56PortNum:
        portStatusDD_8X50G_QSFP_4X25G[i]['link_name'] = '4x25G'
    portStatusDD_8X50G_QSFP_4X25G[i]['link_status'] = 'True'
    portStatusDD_8X50G_QSFP_4X25G[i]['pcs_status'] = 'True'
    if i == 0:
        portStatusDD_8X50G_QSFP_4X25G[i]['link_name'] = '4x25G'
    if i == 16:
        portStatusDD_8X50G_QSFP_4X25G[i]['link_name'] = '8x50G'

portStatusDD_4X50G_QSFP_4X25G = {}
for i in ALL_PORT_NUM:
    portStatusDD_4X50G_QSFP_4X25G[i] = {}
    if i in qsfpDDPortNum:
        portStatusDD_4X50G_QSFP_4X25G[i]['link_name'] = '4x50G'
    elif i in qsfp56PortNum:
        portStatusDD_4X50G_QSFP_4X25G[i]['link_name'] = '4x25G'
    portStatusDD_4X50G_QSFP_4X25G[i]['link_status'] = 'True'
    portStatusDD_4X50G_QSFP_4X25G[i]['pcs_status'] = 'True'

portStatusDD_4X25G_QSFP_4X25G = {}
for i in ALL_PORT_NUM:
    portStatusDD_4X25G_QSFP_4X25G[i] = {}
    portStatusDD_4X25G_QSFP_4X25G[i]['link_name'] = '4x25G'
    portStatusDD_4X25G_QSFP_4X25G[i]['link_status'] = 'True'
    portStatusDD_4X25G_QSFP_4X25G[i]['pcs_status'] = 'True'

portStatusDD_4X25G_QSFP_2X2X25G = {}
for i in ALL_PORT_NUM:
    portStatusDD_4X25G_QSFP_2X2X25G[i] = {}
    portStatusDD_4X25G_QSFP_2X2X25G[i]['link_name'] = '2x25G'
    portStatusDD_4X25G_QSFP_2X2X25G[i]['link_status'] = 'True'
    portStatusDD_4X25G_QSFP_2X2X25G[i]['pcs_status'] = 'True'

#when the real value reaches the range edge, it should be considered as unacceptable
ber_threshold = 1e-10
temperature_range_min, temperature_range_max = 15, 100
voltage_range_min, voltage_range_max = 0.7, 1.5

portFEC_DD_8X50G_QSFP_4X50G = {}
for i in ALL_PORT_NUM:
    portFEC_DD_8X50G_QSFP_4X50G[i] = {}
    if i in [16, qsfpDDPortNum]:
        portFEC_DD_8X50G_QSFP_4X50G[i]['link_name'] = '8x50G'
    elif i in qsfp56PortNum:
        portFEC_DD_8X50G_QSFP_4X50G[i]['link_name'] = '4x50G'
    portFEC_DD_8X50G_QSFP_4X50G[i]['FEC'] = '3'
    if i == 0:
        portFEC_DD_8X50G_QSFP_4X50G[i]['link_name'] = '4x50G'

portFEC_DD_8X50G_QSFP_4X25G = {}
for i in ALL_PORT_NUM:
    portFEC_DD_8X50G_QSFP_4X25G[i] = {}
    if i in [16, qsfpDDPortNum]:
        portFEC_DD_8X50G_QSFP_4X25G[i]['link_name'] = '8x50G'
        portFEC_DD_8X50G_QSFP_4X25G[i]['FEC'] = '3'
    elif i in qsfp56PortNum:
        portFEC_DD_8X50G_QSFP_4X25G[i]['link_name'] = '4x25G'
        portFEC_DD_8X50G_QSFP_4X25G[i]['FEC'] = '2'
    if i == 0:
        portFEC_DD_8X50G_QSFP_4X25G[i]['link_name'] = '4x25G'
        portFEC_DD_8X50G_QSFP_4X25G[i]['FEC'] = '2'

portFEC_DD_4X50G_QSFP_4X25G = {}
for i in ALL_PORT_NUM:
    portFEC_DD_4X50G_QSFP_4X25G[i] = {}
    if i in [16, qsfpDDPortNum]:
        portFEC_DD_4X50G_QSFP_4X25G[i]['link_name'] = '4x50G'
        portFEC_DD_4X50G_QSFP_4X25G[i]['FEC'] = '3'
    elif i in qsfp56PortNum:
        portFEC_DD_4X50G_QSFP_4X25G[i]['link_name'] = '4x25G'
        portFEC_DD_4X50G_QSFP_4X25G[i]['FEC'] = '2'
    if i == 0:
        portFEC_DD_4X50G_QSFP_4X25G[i]['link_name'] = '4x25G'
        portFEC_DD_4X50G_QSFP_4X25G[i]['FEC'] = '2'

portFEC_DD_4X25G_QSFP_2X2X25G = {}
for i in ALL_PORT_NUM_2X2X25G:
    portFEC_DD_4X25G_QSFP_2X2X25G[i] = {}
    if i in [16, qsfpDDPortNum]:
        portFEC_DD_4X25G_QSFP_2X2X25G[i]['link_name'] = '4x25G'
        portFEC_DD_4X25G_QSFP_2X2X25G[i]['FEC'] = '2'
    elif i in qsfp2x25PortNum:
        portFEC_DD_4X25G_QSFP_2X2X25G[i]['link_name'] = '2x25G'
        portFEC_DD_4X25G_QSFP_2X2X25G[i]['FEC'] = '2'
    if i == 0:
        portFEC_DD_4X25G_QSFP_2X2X25G[i]['link_name'] = '2x25G'
        portFEC_DD_4X25G_QSFP_2X2X25G[i]['FEC'] = '2'

portFEC_DD_4X25G_QSFP_4X25G = {}
for i in ALL_PORT_NUM:
    portFEC_DD_4X25G_QSFP_4X25G[i] = {}
    portFEC_DD_4X25G_QSFP_4X25G[i]['link_name'] = '4x25G'
    portFEC_DD_4X25G_QSFP_4X25G[i]['FEC'] = '2'

portFEC_DD_8X50G = {}
portFEC_DD_4X50G = {}
for i in range(32):
    portFEC_DD_8X50G[i] = {}
    portFEC_DD_8X50G[i]['link_name'] = '8x50G'
    portFEC_DD_8X50G[i]['FEC'] = '3'

    portFEC_DD_4X50G[i] = {}
    portFEC_DD_4X50G[i]['link_name'] = '4x50G'
    portFEC_DD_4X50G[i]['FEC'] = '3'

test_time_24_hr = 86400
cloudripper_port_mode = ("32x1x8x50g", "32x1x4x50g", "32x1x4x25g")

####################### MINIPACK2 #############################
BCM_promptstr = "BCM.0>"
BCMLT_prompt = "sdklt.0>"
speed_100G = '100G'
speed_200G = '200G'
speed_400G = '400G'
BCM_VERSION = "Release: sdk-6.5.22"

xphy_init_modex1 = "for x in $(seq 1 2); do ./xphy parinit mode=1 pim=$x iftype=11 txfir=1 txfirshow=0 dscdump=0 download=1 fecmode=0; done"
xphy_init_modey1 = "for y in $(seq 3 6); do ./xphy parinit mode=2 pim=$y iftype=11 txfir=1 txfirshow=0 dscdump=0 download=1 fecmode=0; done"
xphy_init_modez1 = "for z in $(seq 7 8); do ./xphy parinit mode=1 pim=$z iftype=11 txfir=1 txfirshow=0 dscdump=0 download=1 fecmode=0; done"
xphy_init_modex2 = "for x in $(seq 1 2); do ./xphy parinit mode=1 pim=$x iftype=11 txfir=2 txfirshow=0 dscdump=0 download=1 fecmode=0; done"
xphy_init_modey2 = "for y in $(seq 3 6); do ./xphy parinit mode=2 pim=$y iftype=11 txfir=2 txfirshow=0 dscdump=0 download=1 fecmode=0; done"
xphy_init_modez2 = "for z in $(seq 7 8); do ./xphy parinit mode=1 pim=$z iftype=11 txfir=2 txfirshow=0 dscdump=0 download=1 fecmode=0; done"
xphy_init_modey1_pim5 = "for y in 6; do ./xphy parinit mode=2 pim=$y iftype=11 txfir=1 txfirshow=0 dscdump=0 download=1 fecmode=0; done"
xphy_init_modey2_pim5 = "for y in 6; do ./xphy parinit mode=2 pim=$y iftype=11 txfir=2 txfirshow=0 dscdump=0 download=1 fecmode=0; done"
xphy_init_modey2_pim6 = "./xphy parinit mode=2 pim=6 iftype=11 txfir=2 txfirshow=0 dscdump=0 download=1 fecmode=0"

xphyback_dict = {"16nm": "xphyback_16nm", "7nm": "xphyback_7nm"}
xphy_h = "./xphy -h"
xphy_h_pattern = {"xphy driver version:PLP_BARCHETTA2_SW_misc_2_6_0+PLP_EPDM_misc_4_0_6": "xphy\s+driver\s+version:PLP_BARCHETTA2_SW_misc_2_6_0\+PLP_EPDM_misc_4_0_6"}
xphy_init_mode2 = "for pimx in $(seq 1 8); do ./xphy parinit mode=2 pim=$pimx iftype=11 txfir=1 txfirshow=0 dscdump=0 download=1 fecmode=0; done"
xphy_init_mode3 = "for pimx in $(seq 1 8); do ./xphy parinit mode=3 pim=$pimx iftype=11 txfir=1 txfirshow=0 dscdump=0 download=1 fecmode=0; done"
xphy_init_mode3_txfir2 = "for pimx in $(seq 1 8); do ./xphy parinit mode=3 pim=$pimx iftype=11 txfir=2 txfirshow=0 dscdump=0 download=1 fecmode=0; sleep 1; done"
xphy_init_mode3_d2 = "for pimx in $(seq 1 8); do ./xphy parinit mode=3 pim=$pimx iftype=11 txfir=2 txfirshow=0 dscdump=0 download=2 fecmode=0; done"
xphy_init_mode3_pim5 = "for pimx in 1 2 6 7 8; do ./xphy parinit mode=3 pim=$pimx iftype=11 txfir=1 txfirshow=0 dscdump=0 download=1 fecmode=0; done"
xphy_init_mode3_d2_pim5 = "for pimx in 1 2 6 7 8; do ./xphy parinit mode=3 pim=$pimx iftype=11 txfir=2 txfirshow=0 dscdump=0 download=2 fecmode=0; done"
xphy_init_mode3_pim4 = "for pimx in 1 2 7 8; do ./xphy parinit mode=3 pim=$pimx iftype=11 txfir=1 txfirshow=0 dscdump=0 download=1 fecmode=0; done"
xphy_init_mode3_d2_pim4 = "for pimx in 1 2 7 8; do ./xphy parinit mode=3 pim=$pimx iftype=11 txfir=2 txfirshow=0 dscdump=0 download=2 fecmode=0; done"
xphy_init_mode3_d1_d2 = "{}; sleep 1; {}".format(xphy_init_mode3, xphy_init_mode3_d2)
xphy_init_mode3_d1_d2_pim5 = "{}; sleep 1; {}".format(xphy_init_mode3_pim5, xphy_init_mode3_d2_pim5)
xphy_init_mode3_d1_d2_pim4 = "{}; sleep 1; {}".format(xphy_init_mode3_pim4, xphy_init_mode3_d2_pim4)
xphy_init_8pim_txfir2 = "./xphy200GEloopinit_txfirdft.sh"
clean_xphy = "ps -ef | grep xphyback |grep -v grep | awk  '{print \"kill \" $2}' |sh; sleep 2;"
port_up_status = ["up", "(?:200G|400G)", "FD", "No",  "Forward", "TX RX", "Backplane", "9412", "RS544-2xN"]
port_up_status_100G = ["up", "100G", "FD", "No",  "Forward", "TX RX", "Backplane", "9412"]
port_init_status = ["down", "(?:200G|400G|100G)", "FD", "No",  "Forward", "TX RX", "Backplane", "9412"]
port_up_dict = {"up FD No Forward TX RX Backplane 9412":"up\s+.*?(?:200G|400G).*?FD.*?No.*?Forward.*?TX RX.*?Backplane.*?9412.*?RS544-2xN" }
port_mac_status = ["cd", "MAC"]
port_ce_mac_status = ["ce", "MAC"]
port_phy_status = ["cd", "PHY"]
port_disable_status = ["!ena"]
port_pattern = "cd\d+\(\s*\d+\)|P\d+|Port\d+|ce\d+\(\s*\d+\)|xe\d+\(\s*\d+\)\s+.*\s+RS544-1xN"
port_pattern_dc_down = "cd\d+\(\s*\d+\)\s*down|ce\d+\(\s*\d+\)"
port_pattern_dc = "cd\d+\(\s*\d+\)\s*(up|!ena)|P\d+.*400G|Port\d+|ce\d+\(\s*\d+\)"
lb_mac_pimNum5_400G_200G = 'port cd2-cd5,cd8-cd11,cd14-cd17,cd20-cd23,cd26-cd29,cd32-cd35,cd38-cd41,cd44-cd51,cd54-cd57,cd60-cd63,cd66-cd69,cd72-cd75,cd78-cd81,cd84-cd87,cd90-cd93 lb=mac'
lb_mac_pimNum5_200G_200G = 'port cd4-cd7,cd12-cd15,cd20-cd23,cd28-cd31,cd44-cd47,cd52-cd55,cd36-cd39,cd60-cd63,cd66-cd67,cd72-cd73,cd80-cd81,cd88-cd89,cd96-cd97,cd104-cd105,cd112-cd113,cd120-cd121 lb=mac'
lb_mac_pimNum5_200G_100G = 'port ce4-ce7,ce12-ce15,ce20-ce23,ce28-ce31,ce36-ce39,ce44-ce47,ce52-ce55,ce60-ce63,ce66-ce67,ce72-ce73,ce80-ce81,ce88-ce89,ce96-ce97,ce104-ce105,ce112-ce113,ce120-ce121 lb=mac'
lb_mac_pimNum4_400G_200G = 'port cd2-cd5,cd8-cd11,cd14-cd17,cd20-cd23,cd26-cd29,cd32-cd35,cd38-cd41,cd44-cd51,cd54-cd57,cd60-cd63,cd66-cd69,cd72-cd75,cd78-cd81,cd84-cd87,cd90-cd93 lb=mac'
lb_mac_pimNum4_200G_200G = 'port cd12-cd15,cd4-cd7,cd20-cd23,cd28-cd31,cd36-cd37,cd44-cd45,cd62-cd63,cd52-cd53,cd38-cd39,cd46-cd47,cd54-cd55,cd60-cd61,cd64-cd67,cd72-cd75,cd80-cd83,cd88-cd91,cd120-cd123,cd112-cd115,cd104-cd107,cd96-cd99 lb=mac'
lb_mac_pimNum4_200G_100G = 'port ce4-ce7,ce12-ce15,ce20-ce23,ce28-ce31,ce36-ce39,ce44-ce47,ce52-ce55,ce60-ce67,ce72-ce75,ce80-ce83,ce88-ce91,ce96-ce99,ce104-ce107,ce112-ce115,ce120-ce123 lb=mac'
port_total = 96
prompt_dict = {"exit":BCM_promptstr, "exit\nexit": "sdklt.0>",
               "exit()":">>>", "\x03":">"}
port_enable_cmd = "port cd en=1"
port_disable_cmd = "port cd en=0"
port_ce_enable_cmd = "port ce en=1"
port_ce_disable_cmd = "port ce en=0"
startup_phy_cmd = "auto_load_user_intphy.sh"
port_phy_cmd = "port cd lb=phy"
port_mac_cmd = "port cd lb=mac"
port_ce_mac_cmd = "port ce lb=mac"
set_prbs_run_PRBS_cmd = "phy diag 1-262 prbs clear\n phy diag 1-262 prbs set p=3\nphy diag 1-262 prbsstat start interval=30\n"
get_port_PRBS_status_cmd = "phy diag 1-262 prbs get"
get_port_BER_level_cmd = "phy diag 1-262 prbsstat ber"
get_port_BER_level_cmd_second = get_port_BER_level_cmd
ps_cmd = "ps"
ps_cd_cmd = "ps cd"
ps_ce_cmd = "ps ce"
ps_xe_cmd = "ps xe"
portdump_status_cmd = "portdump status all"
portdump_counters_cmd = "portdump counters all"
portdump_counters_32_cmd = "portdump counters 1-16,81-96"
portdump_counters_64_cmd = "portdump counters 17-80"
portdump_pass_pattern = ["(Port|P)\d+", "passed"]
PRBS_port_pattern = "(\d+) : PRBS (\S+)"
PRBS_ok = "OK!"
BER_port_pattern = "(\d+\[\d+\]) : ([e\-.0-9]+)"
port_BER_tolerance = 1e-6
port_exclude = ["50", "152"]
set_snake_vlan_400G_cmd = "linespeed64x200_32x400_2TG.soc"
set_snake_vlan_200G_cmd = "linespeed200G.soc"
set_snake_vlan_100G_cmd = "linespeed100G.soc"
SOC_400G_file_list = [set_snake_vlan_400G_cmd]
SOC_400G_file_path = "/home/automation/Auto_Test/automation/FB-Minipack2/autotest/SDK"
pvlan_show_cmd = "pvlan show"
vlan_show_cmd = "vlan show"
show_c_cmd = "show c"
clear_c_cmd = "clear c\n" + show_c_cmd
let_CPU_send_package_cmd = "tx 10000 pbm=cd0 vlan=10 length=600 SM=0x1 DM=0x2"
let_CPU_send_package_100G_cmd = "tx 1000 pbm=ce0 vlan=10 length=600 SM=0x1 DM=0x2"
let_CPU_send_package_cd1_cmd = "tx 10000 pbm=cd1 vlan=100 length=600 SM=0x1 DM=0x2"
let_CPU_send_package_cd8_cmd = "tx 10000 pbm=cd8 vlan=200 length=600 SM=0x1 DM=0x2"
let_CPU_send_package_cd1_cmd = "tx 10000 pbm=cd1 vlan=100 length=600 SM=0x1 DM=0x2"
let_CPU_send_package_cd8_cmd = "tx 10000 pbm=cd8 vlan=200 length=600 SM=0x1 DM=0x2"
sleep_300s_cmd = "sleep 300"
stop_traffic_cmd = "pvlan set cd127 1888"
stop_traffic_cd16_89_cmd = "portdump counters 1-16,81-96"
stop_traffic_cd17_80_cmd = "portdump counters 17-80"
stop_traffic_ce127_cmd = "pvlan set ce127 1888"
stop_traffic_cd53_cd57_cmd = "pvlan set cd53,cd57 1888"
get_lane_serdes_version_cmd = "phy diag 1-262 dsc"
get_hmon_temperature_cmd = "hmon temperature"
lane_serdes_version_pattern = ["Core.*?LANE\s+=\s+(\d+)", "Common Ucode Version\s+=\s+(\S+)"]
sleep_pattern = ["Sleeping for"]
error_placeholder_pattern = ["replaceholder_error"]
port_XLMIB_RPKT_pattern = "XLMIB_RPKT.cd(\d+)\s+:\s+([0-9,]+)\s+(\+[0-9,]+)"
max_temperature = 130
hmon_temperature_pattern = "\d+\s+([0-9.]+)"
cls_shell = "cls_shell"
cls_shell_port_status = "./%s ps cd; sleep 25\n"%(cls_shell)
cls_shell_exit = "./%s exit\n"%(cls_shell)
check_bcm_user = "ps -ef | grep bcm.user |grep -v grep"
check_exit_bcm_user = 'p_exits=`ps -ef | grep bcm.user |grep -v grep`; [ -n "$p_exits" ] && {}'.format(cls_shell_exit)
bcm_user = {"./bcm.user -y":"\./bcm\.user\s+-y"}
KR_10G_TEST = "./10GKR_test.sh; sleep 1"
KR_pass_pattern = {"Passed": "result:.*?Passed" }

load_user_tool = "python3 auto_load_user.py "
init_load_user_cmd = load_user_tool + "-c init -d 5 -p "
init_pass_pattern = {"GB Initialization Test": ok_keyword}
init_port_pattern = {"link True, pcs True":"link True,\s+pcs True"}
loopback_cmd = load_user_tool + "-c loopback "
loopback_pattern = {"GB Mac Ports [none|pma_serdes|pma] Loopback Test ---------- PASS":"GB\s+Mac\s+Ports\s+(none|pma_serdes|pma)\s+Loopback\s+Test.*?PASS"}
l2_cpu_cmd = load_user_tool + "-c l2_cpu -d 300 -p"
l2_cpu_pattern = {"L2 snake traffic with cpu injection ---------- PASS":"L2 snake traffic with cpu injection.*?PASS"}
l3_cpu_cmd = load_user_tool + "-c l3_cpu -d 300 -p"
l3_cpu_pattern = {"L3 snake traffic with cpu injection ---------- PASS":"L3 snake traffic with cpu injection.*?PASS"}
mac_port_counter_cmd = "tc.mph.print_mac_stats()"
mac_port_counter_pattern= "Link \[(\d+)\] name.*?Rx ([0-9 ]+), Rx CRC 0, Tx ([0-9 ]+)"
manufacturing_cmd = load_user_tool + "-c all -l 1 -t 15~110"
manufacturing_pattern = {"GB Run Test All PASS": 'GB Run Test All.*?PASS'}
re_init_cmd = load_user_tool + "-c init -l 10"
re_init_pattern = {"GB Initialization Test ---------- PASS":"GB .*?Initialization Test.*?PASS", "TEST STATUS REPORT":"GB Init Test.*?10.*?10.*?10.*?0.*?none"}
link_up_cmd = load_user_tool + "-c linkup -l 1"
link_up_pattern = {"GB Mac Ports LinkUp Validation Test PASS":"GB Mac Ports LinkUp Validation Test.*?PASS",
                    "TEST STATUS REPORT":"Mac Port LinkUp Test.*?1.*?1.*?1.*?0.*?none"}
l2_cpu_snake_traffic_cmd = load_user_tool + '-c l2_cpu -p 32x1x8x50g -d 600 -y macsec_256bit_sci  -s 44'
l2_cpu_snake_traffic_cmd_200G = load_user_tool + '-c l2_cpu -p 32x1x4x50g -d 600 -y macsec_256bit_sci  -s 44'
l2_cpu_snake_traffic_cmd_100G = load_user_tool + '-c l2_cpu -p 32x1x4x25g -d 600 -y macsec_256bit_sci  -s 44'
l3_cpu_snake_traffic_cmd = load_user_tool + '-c l3_cpu -p 32x1x8x50g -d 600 -y macsec_256bit_sci  -s 44'
l3_cpu_snake_traffic_cmd_200G = load_user_tool + '-c l3_cpu -p 32x1x4x50g -d 600 -y macsec_256bit_sci  -s 44'
l3_cpu_snake_traffic_cmd_100G = load_user_tool + '-c l3_cpu -p 32x1x4x25g -d 600 -y macsec_256bit_sci  -s 44'

#For common variable
devicename = os.environ.get("deviceName", "")
if "minipack2" in devicename.lower():
    let_CPU_send_package_cmd = "tx 10000 pbm=cd0 vlan=10 "
    let_CPU_send_package_100G_cmd = "tx 1000 pbm=ce0 vlan=10 "
    let_CPU_send_package_cd1_cmd = "tx 10000 pbm=cd1 vlan=100 "
    let_CPU_send_package_cd8_cmd = "tx 10000 pbm=cd8 vlan=200 "
    let_CPU_send_package_cd1_cmd = "tx 10000 pbm=cd1 vlan=100 "
    let_CPU_send_package_cd8_cmd = "tx 10000 pbm=cd8 vlan=200 "
    len_295 = "length=600 SM=0x1 DM=0x2"
    len_600 = "length=600 SM=0x1 DM=0x2"
    SDK_PATH = '/usr/local/cls_diag/SDK/v*'
    SDK_SCRIPT = 'auto_load_user.sh'
    remote_shell_load_sdk = "./{} -d".format(SDK_SCRIPT)
    load_128x100 = "{} -m 128x100".format(SDK_SCRIPT)
    load_64x200_32x400 = "{} -m 64x200_32x400".format(SDK_SCRIPT)
    SDKLT_array = {"SDKLT_tool"  : "dsh",
                 "SDKLT_prompt"  : "sdklt.0>",
                 "PCIE_INFO_CMD" : "PCIEphy fwinfo",
                 "PCIe_version"  : "PCIe FW version: " + SwImage.getSwImage("TH4_PCIE_FLASH").imageDict.get("newVersion", {}).get('PCIe FW version', "NOTFOUND")
                 }
elif "cloudripper" in devicename.lower() or "wedge400c" in devicename.lower():
    sdk_release_version = SwImage.getSwImage(SwImage.SDK).newVersion
    sdk_release_date = SwImage.getSwImage("SDK").imageDict.get("newVersion_MISC", {}).get('releaseDate', "not found")
    cisco_sdk_version = SwImage.getSwImage("SDK").imageDict.get("newVersion_MISC", {}).get('ciscoSDKVersion', "not found")
    GB_Serdes_version = SwImage.getSwImage("SDK").imageDict.get("newVersion_MISC", {}).get('GBSerdesVersion', "not found")
    sdk_version_dict = (sdk_release_version, sdk_release_date, cisco_sdk_version, GB_Serdes_version)
if "wedge400_" in devicename.lower():
    SDK_PATH = '/usr/local/cls_diag/SDK'
    SDK_SCRIPT = 'auto_load_user.sh'
    remote_shell_load_sdk = "./{} -d".format(SDK_SCRIPT)
    SDKLT_array = {"SDKLT_tool": "dsh",
                   "SDKLT_prompt": "BCM.0>",
                   }
    port_up_status = ["up", "(?:200G|400G|100G|50G)", "FD", "No", "Forward", "TX RX", "(KR8|KR4|SR4|KR1)", "9412", "(RS544-2xN|RS528|RS544-1xN)"]
    set_snake_vlan_400G_cmd = "snake_script_loopback_DD_400G_16port.soc"
    set_snake_vlan_200G_cmd = "snake_script_loopback_DD_200G_16port.soc"
    set_snake_vlan_100G_cmd = "snake_script_loopback_DD_100G_16port.soc"
    set_snake_vlan_200G_cmd_56 = "snake_script_loopback_56_200G_32port.soc"
    set_snake_vlan_100G_cmd_56_400200 = "snake_script_loopback_56_100G_32port_for_400_200_mode.soc"
    set_snake_vlan_100G_cmd_56_100 = "snake_script_loopback_56_100G_32port_for_100_mode.soc"
    set_snake_vlan_50G_cmd_56 = "snake_script_loopback_56_50G_64port.soc"
    set_snake_vlan_all = "snake_script_loopback.soc"
    clear_c = "clear c"
    sleep_time = "sleep 10"
    sleep_time_sensor = "sleep 60"
    stop_traffic_cmd = "pvlan set cd15 1888"
    stop_traffic_cmd_DD100G = "pvlan set ce15 1888"
    stop_traffic_cmd_56200G = "pvlan set cd47 1888"
    stop_traffic_cmd_56100G = "pvlan set ce31 1888"
    stop_traffic_cmd_56100G_1 = "pvlan set ce47 1888"
    stop_traffic_cmd_5650G = "pvlan set xe63 1888"
    stop_traffic_cmd_th3 = "pvlan set cd15 1888\npvlan set cd47 1888"
    portdump_counters_cmd_th3 = "show c CDMIB_TPKT.cd;show c CDMIB_RPKT.cd;show c CDMIB_RFCS"
    portdump_counters_cmd = "show c CDMIB_RPKT.cd0-cd15; show c CDMIB_TPKT.cd0-cd15; show c CDMIB_RFCS"
    portdump_counters_cmd_100G = "show c CDMIB_RPKT.ce0-ce15; show c CDMIB_TPKT.ce0-ce15; show c CDMIB_RFCS"
    portdump_counters_cmd_200G_56 = "show c CDMIB_RPKT.cd16-cd47; show c CDMIB_TPKT.cd16-cd47; show c CDMIB_RFCS"
    portdump_counters_cmd_100G_56 = "show c CDMIB_RPKT.ce0-ce31; show c CDMIB_TPKT.ce0-ce31; show c CDMIB_RFCS"
    portdump_counters_cmd_100G_56_100 = "show c CDMIB_RPKT.ce16-ce47; show c CDMIB_TPKT.ce16-ce47; show c CDMIB_RFCS"
    portdump_counters_cmd_50G_56 = "show c CDMIB_RPKT.xe0-xe63; show c CDMIB_TPKT.xe0-xe63; show c CDMIB_RFCS"
    portdump_RPKT_pattern = r"CDMIB_RPKT\.\w+.*?([\d,]+)\s+.(\S+)"
    portdump_TPKT_pattern = r"CDMIB_TPKT\.\w+.*?([\d,]+)\s+.(\S+)"
    port_up_status_400G = ["up", "8", "400G", "FD", "SW", "No", "Forward", "TX RX", "KR8", "9412", "RS544-2xN"]
    port_up_status_200G = ["up", "4", "200G", "FD", "SW", "No", "Forward", "TX RX", "KR4", "9412", "RS544-2xN"]
    port_up_status_100G = ["up", "4", "100G", "FD", "SW", "No", "Forward", "TX RX", "KR4", "9412", "RS528"]
    port_up_status_100G_1 = ["up", "4", "100G", "FD", "SW", "No", "Forward", "TX RX", "SR4", "9412", "RS528"]
    port_up_status_50G = ["up", "1", "50G", "FD", "SW", "No", "Forward", "TX RX", "KR1", "9412", "RS544-1xN"]
    port_pattern_400G = "up.*400G"
    port_pattern_200G = "up.*200G"
    port_pattern_100G = "up.*100G"
    port_pattern_50G = "up.*50G"
    show_temp_cmd = "show temp"
    average_temp = "average current temperature is\s+(\d+.\d)"
    maxi_temp = "maximum peak temperature is\s+(\d+.\d)"
    cls_shell = "cls_shell"
    cls_shell_port_status = "./%s ps" % (cls_shell)
    port_up_dict = {"up FD No Forward TX RX 9412": "up\s+.*?(?:200G|400G).*?FD.*?No.*?Forward.*?TX RX.*?9412.*?RS544-2xN"}
    get_lane_serdes_version_cmd = "phy diag cd dsc"
    get_lane_serdes_version_cmd_200G = "phy diag cd0-cd15 dsc"
    get_lane_serdes_version_cmd_100G = "phy diag ce0-ce31 dsc"
    get_lane_serdes_version_cmd_ce = "phy diag ce dsc"
    get_lane_serdes_version_cmd_ce_100G = "phy diag ce0-ce15 dsc"
    get_lane_serdes_version_cmd_xe = "phy diag xe0-xe63 dsc"
    set_prbs_run_PRBS_cmd_400G = "phy diag cd prbs set p=3\nphy diag cd prbsstat\nphy diag cd prbsstat start i=30"
    get_port_BER_level_cmd_400G = "phy diag cd prbsstat ber\nphy diag cd prbsstat clear"
    get_port_BER_level_cmd_second_400G = "phy diag cd prbsstat ber"
    set_prbs_run_PRBS_cmd_200G = "phy diag cd,ce prbs set p=3\nphy diag cd,ce prbsstat\nphy diag cd,ce prbsstat start i=30"
    get_port_BER_level_cmd_200G = "phy diag cd,ce prbsstat ber\nphy diag cd,ce prbsstat clear"
    get_port_BER_level_cmd_second_200G = "phy diag cd,ce prbsstat ber"
    set_prbs_run_PRBS_cmd_100G = "phy diag ce prbs set p=3\nphy diag ce prbsstat\nphy diag ce prbsstat start i=30"
    get_port_BER_level_cmd_100G = "phy diag ce prbsstat ber\nphy diag ce prbsstat clear"
    get_port_BER_level_cmd_second_100G = "phy diag ce prbsstat ber"
    set_prbs_run_PRBS_cmd_50G = "phy diag ce,xe prbs set p=3\nphy diag ce,xe prbsstat\nphy diag ce,xe prbsstat start i=30"
    get_port_BER_level_cmd_50G = "phy diag ce,xe prbsstat ber\nphy diag ce,xe prbsstat clear"
    get_port_BER_level_cmd_second_50G = "phy diag ce,xe prbsstat ber"
    check_power_cmd = "sensors ir35215-i2c-*-*\nsensors isl68137-i2c-*-*"



prompt_dict = OrderedDict(prompt_dict)

tx_rx_pkt_patterns = [
    r'(XLMIB_TBYT)\.cd.*?:(.*?)\+([,0-9]+)'
    r'(XLMIB_RBYT)\.cd.*?:(.*?)\+([,0-9]+)'
    r'(XLMIB_TPOK)\.cd.*?:(.*?)\+([,0-9]+)'
    r'(XLMIB_RPOK)\.cd.*?:(.*?)\+([,0-9]+)'
    r'(XLMIB_TUCA)\.cd.*?:(.*?)\+([,0-9]+)'
    r'(XLMIB_RUCA)\.cd.*?:(.*?)\+([,0-9]+)'
    r'(XLMIB_TPKT)\.cd.*?:(.*?)\+([,0-9]+)'
    r'(XLMIB_RPKT)\.cd.*?:(.*?)\+([,0-9]+)'
    r'(XLMIB_T511)\.cd.*?:(.*?)\+([,0-9]+)'
    r'(XLMIB_R511)\.cd.*?:(.*?)\+([,0-9]+)'
    r'(XLMIB_RPRM)\.cd.*?:(.*?)\+([,0-9]+)'
]

########################## MINIPACK3 #############################
if "minipack3" in devicename.lower():
    CENTOS_SDK_prompt='[root@localhost SDK]#'
    BCM_VERSION_MiniPack3 = "Release: "
    SDK_SHELL = 'auto_load_user.sh'
    load_128x400 =  "./{} -m 128x400".format(SDK_SHELL)
    load_128x200 =  "./{} -m 128x200".format(SDK_SHELL)
    load_128x100 =  "./{} -m 128x100".format(SDK_SHELL)
    load_64x400_64x200 =  "./{} -m 64x400_64x200".format(SDK_SHELL)
    load_64x800 =  "./{} -m 64x800".format(SDK_SHELL)
    load_256x100 =  "./{} -m 256x100".format(SDK_SHELL)
    load_64x200_64x400 =  "./{} -m 64x200_64x400".format(SDK_SHELL)
    portdump_status_pass_regex= 'port status check test PASSED'
    PCIe_version_regex = 'PCIe FW loader version: '
    port_detail_passed_pattern = ["(P\d+)", "(UP)", "(FULL)","passed"]
    port_detail_failed_pattern = ["(P\d+)", "(DOWN)", "(N/A)","(N/A)", "failed"]
    portdump_pass_pattern_regex = "((Port|P)\d+)([\s+\S+]+)passed"
    portdump_failed_pattern = ["(Port|P)\d+", "failed"]
    portdump_failed_pattern_regex = "((Port|P)\d+)([\s+\S+]+)failed"
    port_d3c_enable_cmd = 'port d3c en=1'
    port_d3c_disable_cmd = 'port d3c en=0'
    bertest_cmd='bertest'
    clear_c_command = 'clear c'
    traffic_test_cmd='traffictest all'
    traffic_test_end_regex = 'str=tx([\s+\S+\n]+)\BCM\.0>'
    sdk_prompt='root@localhost SDK'
    cls_shell_d3c = './cls_shell ps d3c'
    cls_shell_d3c_check=['d3c\d+','up', '800G', 'FD','No', 'Forward', 'TX', 'RX', 'Backplane', '9412']
    cls_shell_exit = './cls_shell exit'
    lane_serdes_version_cmd = "phy diag 1-344 dsc"
    serdes_api_version_regex = 'SERDES API Version   = '
    ucode_version_regex = 'Common Ucode Version = '
    port_d3c_lb_cmd = 'port d3c lb='
    phy_diag_d3c_dsc_64 = 'phy diag d3c dsc (x=0~63)'
    phy_diag_d3c_dsc_128 = 'phy diag d3c dsc (x=0~127)'
    cls_shell_exit_output_regex = 'Disconnecting IRQ 0 blocked by kernel ISR'
    cls_shell_d3c_output_regex='RS544-2xN[\s+\n+\S+]+root@localhost SDK'
    bertest_threshold_value='1e-9'
    bertest_regex='\d+\[\d+\]\s+:\s+(([\d+.]+)(e[+-]\d+))'
    portdump_counters_all_cmd = 'portdump counters all'
    BCM_prompt = 'BCM.0>'
    exit_BCM_Prompt='exit'
    port_enable_status='passed'
    port_disable_status='failed'
######################################################
elif "minerva_janga" in devicename.lower():
    SDK_SHELL= "python3 -i diagtest_sdk.py"
    mgmt_port_regex='E\d+\/0'
    load_18x1x800= "{} --port_mode 18x1x800G".format(SDK_SHELL)
    load_18x1x400= "{} --port_mode 18x1x400G".format(SDK_SHELL)
    load_18x2x200= "{} --port_mode 18x2x200G".format(SDK_SHELL)
    load_18x2x100= "{} --port_mode 18x2x100G".format(SDK_SHELL)
    load_18x2x400= "{} --port_mode 18x2x400G".format(SDK_SHELL)
    load_18x4x100= "{} --port_mode 18x4x100G".format(SDK_SHELL)
    load_18x4x200= "{} --port_mode 18x4x200G".format(SDK_SHELL)
    port_enable_tag= "--enable_lt"
    CENTOS_SDK_prompt='[root@localhost SDK]#'
    BCM_SDK_version_cmd='sdk.do_show_version_test()'
    PCIe_version_cmd='sdk.dapi.pciephy_fw_show(unit=None)'
    PCIe_version_check='PCIe FW loader version: '
    show_version_test_passed_regex='do_show_version_test- TEST PASS'
    get_sdk_version = '([a-z0-9\.]+)\s+\S+\s+([a-z0-9\.-]+)'
    portdump_status_cmd = 'sdk.dapi.dump_ports()'
    port_name_regex='\S+\d+\/\d+'
    BCM_prompt='>>>'
    port_disable_cmd='sdk.dapi.port_enable(unit=None, port=None, enable=False)'
    port_enable_cmd='sdk.dapi.port_enable(unit=None, port=None, enable=True)'
    PSBR_passed_pattern= 'do_port_serdes_prbs_ber_test- TEST PASS'
    bertest_cmd=' --run_case 4 --prbs_running_sec 180'
    L2_cpu_traffic_cmd=' --run_case 7 --duration_sec 300'
    L2_cpu_traffic_passed_pattern= 'do_cpu_full_l2snake_test- TEST PASS'
    bertest_regex='\|\s*\d+\s*\|\s*\d+\s*\|\s*\d+\s*\|\s*PRBSlocked\s*\|\s*([\d+\.]+)\s*\|'
    bertest_threshold_value='1e-8'
    lane_serdes_version_cmd='sdk.dapi.phy_dsc(unit={}, port={})'
    ucode_version_regex= 'Common Ucode Version = '
    serdes_api_version_regex= 'SERDES API Version   = '
    manufacturing_test_command='--duration_sec 10 --max_temp 100 --min_temp 25 --prbs_running_sec 10 --auto_run_all'
    manufacturing_test_pattern_lst=['do_dram_bist_test- TEST PASS','do_sdk_reload_test- TEST PASS', 'do_sensor_test- TEST PASS', 'do_port_serdes_prbs_ber_test- TEST PASS', 'do_port_linkup_validation_test- TEST PASS', 'do_port_loopback_test- TEST PASS', 'do_cpu_full_l2snake_test- TEST PASS', 'do_show_version_test- TEST PASS']
    exit_BCM_Prompt='exit()'
    port_enable_status='up'
    port_disable_status='!ena'
    show_temperature_cmd='sdk.dapi.show_temperature(unit=None, main=False, max=False,is_print=True)'
    snake_config_cmd='sdk.dapi.snake_config(unit=0, vehicle=True, ports=None,loopback=True, force_fabric=True, clear=True, use_sat=False)'
    snake_test_start_cmd='sdk.dapi.snake_start_traffic(unit=0, inject=500,psrc=1,data=0x0000002222220000001111118100006408004500,length=360,random=True,use_sat=True,speed=400)'
    snake_test_stop_cmd='sdk.dapi.snake_stop_traffic(unit=0, psrc=1, use_sat=True)'
    port_detail_passed_pattern = ["(eth\d+)", "up", "No", "RS-544-2xN", "NONE"]
    port_loopback_test_pass_regex ='do_port_loopback_test- TEST PASS'
    port_loopback_test_tag= '--run_case 6  --duration_sec 300'
    L2_traffic_test_item_check_regex='(\|\s+[\d,]+\s+){14}'
    l2_traffic_total_tx_rx_packets_regex='-check_mib_counters-:\s+\S+\s+(\d+),\s+rx_gold_bytes:\s+(\d+),\s+tx_gold_frames:\s+(\d+),\s+tx_gold_bytes:\s+(\d+)'

elif "minerva_th5" in devicename.lower():
    CENTOS_SDK_prompt='[root@localhost SDK]#'
    BCM_VERSION_MiniPack3 = "Release: "
    SDK_SHELL = 'auto_load_user.sh'
    load_128x400 =  "./{} -m 128x400".format(SDK_SHELL)
    load_128x200 =  "./{} -m 128x200".format(SDK_SHELL)
    load_128x100 =  "./{} -m 128x100".format(SDK_SHELL)
    load_64x400_64x200 =  "./{} -m 64x400_64x200".format(SDK_SHELL)
    load_64x800 =  "./{} -m 64x800".format(SDK_SHELL)
    load_64x200_64x400 =  "./{} -m 64x200_64x400".format(SDK_SHELL)
    PCIe_version_regex = 'PCIe FW loader version: '
    port_detail_passed_pattern = ["(P\d+)", "(UP)", "(FULL)","passed"]
    port_detail_failed_pattern = ["(P\d+)", "(DOWN)", "(N/A)","(N/A)", "failed"]
    portdump_pass_pattern_regex = "((Port|P)\d+)([\s+\S+]+)passed"
    portdump_failed_pattern = ["(Port|P)\d+", "failed"]
    portdump_failed_pattern_regex = "((Port|P)\d+)([\s+\S+]+)failed"
    port_d3c_enable_cmd = 'port d3c en=1'
    port_d3c_disable_cmd = 'port d3c en=0'
    bertest_cmd='bertest'
    clear_c_command = 'clear c'
    traffic_test_cmd='snaketest'
    traffic_test_end_regex = 'port counters check test([\s+\S+\n]+)BCM\.0>'
    sdk_prompt='root@localhost SDK'
    cls_shell_d3c = './cls_shell ps d3c'
    cls_shell_d3c_check=['d3c\d+','up', '800G', 'FD','No', 'Forward', 'TX', 'RX', 'Backplane', '9412']
    cls_shell_exit = './cls_shell exit'
    lane_serdes_version_cmd = " dsh -c 'phydiag 1-342 dsc'"
    serdes_api_version_regex = 'SERDES API Version   = '
    ucode_version_regex = 'Common Ucode Version = '
    port_d3c_lb_cmd = 'port d3c lb='
    phy_diag_d3c_dsc_64 = 'phy diag d3c dsc (x=0~63)'
    phy_diag_d3c_dsc_128 = 'phy diag d3c dsc (x=0~127)'
    cls_shell_exit_output_regex = 'Disconnecting IRQ 0 blocked by kernel ISR'
    cls_shell_d3c_output_regex='RS544-2xN[\s+\n+\S+]+root@localhost SDK'
    bertest_threshold_value='1e-9'
    bertest_regex='\d+\[\d+\]\s+:\s+(([\d+.]+)(e[+-]\d+))'
    portdump_counters_all_cmd = 'portdump counters all'
    BCM_prompt = 'BCM.0>'
    exit_BCM_Prompt='exit'
    port_enable_status='passed'
    port_disable_status='failed'
    get_hmon_temperature_cmd= 'hmon temp'
    temperature_test_cmd='snake800G.soc'
    traffic_temp_traffic_cmd_1='tx 10000 pbm=ce0 vlan=998 l=295 SM=0x1 DM=0x2 '
    traffic_temp_traffic_cmd_2=' tx 80000 pbm=d3c16 vlan=199 length=295 SM=0x1 DM=0x2 data=0x000000000002000000000001810000c717fe49d06ee7bb6421afc028af8a7abd8a5a198232538823cbabd57da2f5e13e39c71fa249d7d6e65a112793cbabd57d9d7d6e65a145a313e382df27b277a3f907b9b37a3f907b9a145b3e11f9f85d8de7df1c12793cbabd57da2f593f88fd9d2e9c71fa249d7d6e65a145a313e382df27b277a3f907b9b3e11f9f85d8de7d886239a84a1942126200bc442e6983c6b3f6219a6425adc1202bca4aa5063c0b837af7d84819a2965be0ba4fefe7642617c1c9dff1e4439ad86183a8a3ed79bc849c582e2ebbd7f38253079067eb3935183f2c3fb557923f4babac7dbc4794696a328858c706804fad13741efbef830c3fc5178ecfccae6cb2c7f5d4729eb44225b5357dcd5ac2545bbd30e69c91b916db96573b6bcfba34'
    show_c_rate_cmd='show c rate'
    