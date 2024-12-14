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
import Logger as log
from SwImage import SwImage
from Const import BOOT_MODE_UBOOT, BOOT_MODE_DIAGOS, BOOT_MODE_ONIE,ONIE_RESCUE_MODE
try:
    from Device import Device
    import DeviceMgr
except Exception as err:
    log.cprint(str(err))
device = DeviceMgr.getDevice()
pc_info = DeviceMgr.getServerInfo('PC')
server_ip = pc_info.managementIP
SDK = SwImage.getSwImage("SDK")
SDK_SCRIPT = 'auto_load_user.sh'
remote_shell_load_sdk = "./{}".format(SDK_SCRIPT)
sdkname = SDK.newImage
SDK_PATH = '/root/sdk/{}'.format(sdkname)
ifconfig_a_cmd = "ifconfig -a"
fail_dict = { "fail":"fail",
              "ERROR":"ERROR",
              "Failure": "Failure",
              "cannot read file":"cannot read file",
              "command not found":"command not found",
              "No such file": "No such file",
              "not found": "not found",
              "Unknown command":"Unknown command",
              "No space left on device": "No space left on device",
              "Command exited with non-zero status": "Command exited with non-zero status"
              }
drive_pattern = {
        "psu_dps800"     : "psu_dps800.*",
        "sfp_module"     : "sfp_module.*",
        "pktgen"         : "pktgen.*",
        "mcp3422"        : "mcp3422.*",
        "ir35215"        : "ir35215.*",
        "asc10"          : "asc10.*",
        "i2c_sc18is600"  : "i2c_sc18is600.*",
        "fan_cpld"       : "fan_cpld.*",
        "sys_cpld"       : "sys_cpld.*",
        "cls_i2c_client" : "cls_i2c_client.*",
        "pmbus_core"     : "pmbus_core.*"
        }
drive_pattern_tianhe = {
        "sfp_module"     : "sfp_module.*",
        "1pps_fpga"     : "1pps_fpga.*",
        "march_hare_fpga_core"  : "march_hare_fpga_core.*",
        "come_cpld"        : "come_cpld.*",
        "fan_cpld"        : "fan_cpld.*",
        "sys_cpld"          : "sys_cpld.*",
        "cls_i2c_client"  : "cls_i2c_client.*",
        "ltc4282"       : "ltc4282.*",
        "asc10"       : "asc10.*"
}
devicename = os.environ.get("deviceName", "")
import logging
logging.info("devicename:{}".format(devicename))
if "fenghuangv2" in devicename.lower():
    drive_pattern = {
        "cms": "cms50216.*",
        "sfp_module": "sfp_module.*",
#        "i2c_accel_fpga": "i2c_accel_fpga.*",
        "fan_cpld": "fan_cpld.*",
        "sys_cpld": "sys_cpld.*",
        "cls_i2c_client": "cls_i2c_client.*",
        "ltc4282": "ltc4282.*",
        "psu_dps800": "psu_dps800.*",
        "tps53679": "tps53679.*",
        "asc10": "asc10.*"
    }
fail_pattern = ["fail", "ERROR", "cannot read file", "command not found", "No such file", "Unknown command"]
SDK_SCRIPT = 'auto_load_user.sh'
remote_shell_load_sdk = "./{}".format(SDK_SCRIPT)
daemon_mode = '-d'
knet_l2_show_cmd = 'knet-l2-show'
knet_l2_show_finish_prompt = '\-\++[\s\S]+Total l2_entry count: 0'
knet_l2_show_pattern = ['.*key_type.*mac_addr.*mac_mask.*source.*group.*l2vni.*entry_dest.*entry_type.*fwd_policy.*ctc_policy.*user_cookie.*hitbit','Total l2_entry count: 0']
qsfp_cmd = 'qsfp'
qsfp_finish_prompt = 'Port 32+[\s\S]+ONIE'
qsfp_pattern = []
for i in range(1,33):
    regexp="Port[ \t]"+str(i)+":[\s]+Vendor:.{1,20}"
    qsfp_pattern.append(regexp)
init_pass_pattern = {"Innovium Switch PCIe Driver opened successfully":"Innovium Switch PCIe Driver opened successfully"}
init_port_pattern = {"link True, pcs True":"link True,\s+pcs True"}
sdkConsole = 'IVM:0>'
CatReadMe = 'shell cat ReadMe\r\n'
CatReadMe_regexp = '.*SDK'
CatReadMe_pattern = [sdkname]
ifcs = 'ifcs show version\r\n'
ifcs_regexp = 'Release.*Date'
ifcs_pattern = ["0.12.58"]
copper_1_8_9_22_23_32 = "-m \"1-8:Copper_4x25;9-22:Copper_2x100;23-32:Copper_4x25\""
copper_1_8_9_22_23_32_pattern = []
for i in range(1,33):
    regexp=".* "+str(i)+" .*ETH.*ISG.*1.*sysport.*[ \t]"+str(i)+"\).*25G.*LINK_UP"
    copper_1_8_9_22_23_32_pattern.append(regexp)
for i in range(33,61):
    regexp=".* "+str(i)+" .*ETH.*ISG.*4.*sysport.*[ \t]"+str(i)+"\).*100G.*LINK_UP"
    copper_1_8_9_22_23_32_pattern.append(regexp)
for i in range(61,101):
    regexp=".* "+str(i)+" .*ETH.*ISG.*1.*sysport.*[ \t]"+str(i)+"\).*25G.*LINK_UP"
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
    regexp=".* "+str(i)+" .*ETH.*ISG.*4.*sysport.*[ \t]"+str(i)+"\).*100G"
    copper_1_20_21_24_25_32_pattern.append(regexp)
for i in range(21,37):
    regexp=".* "+str(i)+" .*ETH.*ISG.*1.*sysport.*[ \t]"+str(i)+"\).*10G"
    copper_1_20_21_24_25_32_pattern.append(regexp)
for i in range(37,45):
    regexp=".* "+str(i)+" .*ETH.*ISG.*4.*sysport.*[ \t]"+str(i)+"\).*100G"
    copper_1_20_21_24_25_32_pattern.append(regexp)
copper_1_20_21_24_25_32_link_pattern = []
for i in range(1,21):
    regexp=".* "+str(i)+" .*ETH.*ISG.*4.*sysport.*[ \t]"+str(i)+"\).*100G"
    copper_1_20_21_24_25_32_link_pattern.append(regexp)
for i in range(21,37):
    regexp=".* "+str(i)+" .*ETH.*ISG.*1.*sysport.*[ \t]"+str(i)+"\).*10G"
    copper_1_20_21_24_25_32_link_pattern.append(regexp)
for i in range(37,45):
    regexp=".* "+str(i)+" .*ETH.*ISG.*4.*sysport.*[ \t]"+str(i)+"\).*100G"
    copper_1_20_21_24_25_32_link_pattern.append(regexp)
copper_1_20_21_24_25_32_4x100 = "-m \"1-20:Copper_1x100G;21-24:Copper_4x10G;25-32:Copper_4x100G\""
copper_1_20_21_24_25_32_4x100_pattern = []
for i in range(1,21):
    regexp=".* "+str(i)+" .*ETH.*ISG.*4.*sysport.*[ \t]"+str(i)+"\).*100G"
    copper_1_20_21_24_25_32_4x100_pattern.append(regexp)
for i in range(21,37):
    regexp=".* "+str(i)+" .*ETH.*ISG.*1.*sysport.*[ \t]"+str(i)+"\).*10G"
    copper_1_20_21_24_25_32_4x100_pattern.append(regexp)
for i in range(37,69):
    regexp=".* "+str(i)+" .*ETH.*ISG.*2.*sysport.*[ \t]"+str(i)+"\).*100G"
    copper_1_20_21_24_25_32_4x100_pattern.append(regexp)
copper_1_20_21_24_25_32_4x100_link_pattern = []
for i in range(1,21):
    regexp=".* "+str(i)+" .*ETH.*ISG.*4.*sysport.*[ \t]"+str(i)+"\).*100G"
    copper_1_20_21_24_25_32_4x100_link_pattern.append(regexp)
for i in range(21,37):
    regexp=".* "+str(i)+" .*ETH.*ISG.*1.*sysport.*[ \t]"+str(i)+"\).*10G"
    copper_1_20_21_24_25_32_4x100_link_pattern.append(regexp)
for i in range(37,69):
    regexp=".* "+str(i)+" .*ETH.*ISG.*2.*sysport.*[ \t]"+str(i)+"\).*100G"
    copper_1_20_21_24_25_32_4x100_link_pattern.append(regexp)
PAM4_400G_32 = "-m 1-32:Copper_1x400G"
PAM4_100G_128 = "-m 1-32:Copper_4x100G"
NRZ_100G_32 = "-m 1-32:Copper_1x100G"
NRZ_40G_32 = "-m 1-32:Copper_1x40G"
NRZ_25G_128 = "-m 1-32:Copper_4x25G"
NRZ_10G_128 = "-m 1-32:Copper_4x10G"
NRZ_100G_64 = "-m 1-32:Copper_2x100G"
NRZ_200G_32 = "-m 1-32:Copper_1x100G"
show_port_info = "ifcs show devport"
port_info_finish_prompt = "RECIRC"
shell_sleep_10 = "shell sleep 10\r\n"
shell_sleep_30 = "shell sleep 30\r\n"
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
NRZ_200G_32_pattern = []
for i in range(1, 33):
    regexp = ".* " + str(i) + " .*ETH.*ISG.*8.*sysport.*[ \t]" + str(i) + "\).*200G.*KP.*"
    NRZ_200G_32_pattern.append(regexp)
PAM4_400G_32_pattern = []
for i in range(1,33):
    regexp=".* "+str(i)+" .*ETH.*ISG.*8.*sysport.*[ \t]"+str(i)+"\).*400G.*"
    PAM4_400G_32_pattern.append(regexp)
PAM4_100G_128_pattern = []
for i in range(1,129):
    regexp=".* "+str(i)+" .*ETH.*ISG.*2.*sysport.*[ \t]"+str(i)+"\).*100G.*"
    PAM4_100G_128_pattern.append(regexp)
NRZ_100G_32_pattern = []
for i in range(1,33):
    regexp=".* "+str(i)+" .*ETH.*ISG.*4.*sysport.*[ \t]"+str(i)+"\).*100G.*"
    NRZ_100G_32_pattern.append(regexp)
NRZ_40G_32_pattern = []
for i in range(1,33):
    regexp=".* "+str(i)+" .*ETH.*ISG.*4.*sysport.*[ \t]"+str(i)+"\).*40G.*"
    NRZ_40G_32_pattern.append(regexp)
NRZ_25G_128_pattern = []
for i in range(1,129):
    regexp=".* "+str(i)+" .*ETH.*ISG.*1.*sysport.*[ \t]"+str(i)+"\).*25G.*"
    NRZ_25G_128_pattern.append(regexp)
NRZ_10G_128_pattern = []
for i in range(1,129):
    regexp=".* "+str(i)+" .*ETH.*ISG.*1.*sysport.*[ \t]"+str(i)+"\).*10G.*"
    NRZ_10G_128_pattern.append(regexp)
NRZ_100G_64_pattern = []
for i in range(1,65):
    regexp=".* "+str(i)+" .*ETH.*ISG.*4.*sysport.*[ \t]"+str(i)+"\).*100G.*"
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
    regexp=".* "+str(i)+" .*ETH.*ISG.*4.*sysport.*[ \t]"+str(i)+"\).*100G.*[UP,DOWN]"
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
prbs_rx_31_10g_300_cmd = 'diagtest serdes prbs rx all all prbs31 10g 300'
prbs_rx_31_10g_300_pattern = '\|[ \t]+32[ \t]+:[ \t]+3.*\d+\.\d+e\-\d+[\s\S]+IVM:0>'
prbs_rx_31_10g_300_pattern_port64 = '\|[ \t]+64[ \t]+:[ \t]+3.*\d+\.\d+e\-\d+[\s\S]+IVM:0>'
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
integrator_100G_64_1 = "-m 64x100-1"
integrator_100g_32_copper = "-m 1-32:copper_1x100G -d -k"
integrator_400G_32_copper= "-m 1-32:copper_1x400G -d -k"
integrator_40G_32_copper= "-m 1-32:copper_1x40G -d -k"
integrator_100G_128_copper = "-m 1-32:copper_4x100G -d -k"
integrator_25G_128_copper = "-m 1-32:copper_4x25G -d -k"
integrator_10G_128_copper = "-m 1-32:copper_4x10G -d -k"
integrator_100G_64_copper = "-m 1-32:copper_2x100G -d -k"
integrator_100G_64_1_copper = "-m 1-32:optics_2x100G -d -k"
integrator_400G_32_pattern = []
for i in range(1,33):
    regexp=".* "+str(i)+" .*ETH.*ISG.*8.*sysport.*[ \t]"+str(i)+"\).*400G.*KP"
    integrator_400G_32_pattern.append(regexp)
integrator_200G_32_pattern = []
for i in range(1,33):
    regexp=".* "+str(i)+" .*ETH.*ISG.*8.*sysport.*[ \t]"+str(i)+"\).*200G.*KP"
    integrator_200G_32_pattern.append(regexp)
integrator_100G_32_pattern = []
for i in range(1,33):
    regexp=".* "+str(i)+" .*ETH.*ISG.*4.*sysport.*[ \t]"+str(i)+"\).*100G.*KR"
    integrator_100G_32_pattern.append(regexp)
integrator_40G_32_pattern = []
for i in range(1,33):
    regexp=".* "+str(i)+" .*ETH.*ISG.*4.*sysport.*[ \t]"+str(i)+"\).*40G.*NONE"
    integrator_40G_32_pattern.append(regexp)
integrator_100G_128_pattern = []
for i in range(1,129):
    regexp=".* "+str(i)+" .*ETH.*ISG.*2.*sysport.*[ \t]"+str(i)+"\).*100G.*KP"
    integrator_100G_128_pattern.append(regexp)
integrator_25G_128_pattern = []
for i in range(1,129):
    regexp=".* "+str(i)+" .*ETH.*ISG.*1.*sysport.*[ \t]"+str(i)+"\).*25G.*FC"
    integrator_25G_128_pattern.append(regexp)
integrator_10G_128_pattern = []
for i in range(1,129):
    regexp=".* "+str(i)+" .*ETH.*ISG.*1.*sysport.*[ \t]"+str(i)+"\).*10G.*NONE"
    integrator_10G_128_pattern.append(regexp)
integrator_100G_64_pattern = []
for i in range(1,65):
    regexp=".* "+str(i)+" .*ETH.*ISG.*4.*sysport.*[ \t]"+str(i)+"\).*100G.*KR"
    integrator_100G_64_pattern.append(regexp)
integrator_100G_64_1_pattern = []
for i in range(1,65):
    regexp=".* "+str(i)+" .*ETH.*ISG.*4.*sysport.*[ \t]"+str(i)+"\).*100G.*"
    integrator_100G_64_1_pattern.append(regexp)
sfp_detect_tool_cmd = 'sfp_detect_tool'
sfp_detect_tool_finish_prompt = 'P32:[ \t]+.*4x100G'
sfp_detect_tool_pattern = []
for i in range(1,33):
    regexp="P"+str(i)+":[ \t]Copper_4x100G"
    sfp_detect_tool_pattern.append(regexp)

fenghuangv2_32_FEC_cmd = {
            './integrator_mode -m 32x400 -o 400G',#32
            './integrator_mode -m 1-32:copper_1x400G -o 400G',#32
            './integrator_mode -m 1-32:copper_1x100G -o 100G',#32
            './integrator_mode -m 32x100 -o 100G',#32
            './integrator_mode -m 32x40 -o 40G',#32
            './integrator_mode -m 1-32:copper_1x40G -o 40G', #32
            './integrator_mode -m 1-32:optics_1x10G -o 10G',#32
            './integrator_mode -m 1-32:copper_1x10G -o 10G'#32
        }
fenghuangv2_64_FEC_cmd = {
            './integrator_mode -m 64x100 -o 100G',
            './integrator_mode -m 64x100-1 -o 100G',
            './integrator_mode -m 1-32:2x100-pam4 -o 100G',#64
            './integrator_mode -m 1-32:optics_2x100G -o 100G'#64

        }
fenghuangv2_128_FEC_cmd = {
            './integrator_mode -m 128x100 -o 100G',
            './integrator_mode -m 128x25 -o 25G',
            './integrator_mode -m 128x10 -o  10G',
            './integrator_mode -m 1-32:copper_4x10 100G',#128
            './integrator_mode -m 1-32:copper_4x100G -o 100G',#128
             './integrator_mode -m 1-32:copper_4x25G -o 25G',#128
            './integrator_mode -m 1-32:4x100 -o 100G'#128

        }


prbs_32_400G = '32x400'
prbs_32_100G = '32x100'
prbs_32_40G = '32x40'
prbs_128_100G = '128x100'
prbs_128x25 = '128x25'
prbs_128x10 = '128x10'
prbs_64x100 = '64x100'
prbs_64x100_1G = '64x100-1'
option_32_400G = '--port fpp1:fpp32'
option_32_100G = '--port fpp1:fpp32'
option_32_40G = '--port fpp1:fpp32'
option_128_100G = '--port fpp1-1:fpp32-4'
option_64x100 = '--port fpp1-1:fpp32-2'
option_128x10 = '--port fpp1-1:fpp32-4'

vlan_check_pattern = []
for i in range(2, 130):
    regexp = '\(l2vni\:\s+' +str(i) + '\).*ADD.*TRUE.*'
    vlan_check_pattern.append(regexp)
for j in range(2, 130):
    regexp = 'L2vni.*l2vni\:\s+' + str(j) + '.*'
    vlan_check_pattern.append(regexp)

#TC 20-26
prbs_en_cmd= 'diagtest serdes prbs mode-en 1-{} 1'
prbs_set_cmd='diagtest serdes prbs set 1-{} 1 prbs31 1593750 30000'
prbs_sync_cmd='diagtest serdes prbs sync 1-{}'
prbs_get_cmd='diagtest serdes prbs get 1-{}'
prbs_clear_cmd='diagtest serdes prbs clear 1-{}'
prbs_mode_en_cmd='diagtest serdes prbs mode-en 1-{} 0'

NRZ_100G_64_1= "-m 1-32:optics_2x100G:down-p2:fec-dis"

#### tianhe_SDK_9.2_Load_and_Initialization_SDK_Test ####
OPTICS_400G_32 = '-m 1-32:optics_1x400G'
OPTICS_100G_128 = '-m 1-32:optics_4x100G'
OPTICS_100G_32 = '-m 1-32:optics_1x100G'
OPTICS_40G_32 = '-m 1-32:optics_1x40G'
OPTICS_25G_128 = '-m 1-32:optics_4x25G'
OPTICS_10G_128 = '-m 1-32:optics_4x10G'
NRZ_10G_32 = '-m 1-32:copper_1x10G'
OPTICS_10G_32 = '-m 1-32:optics_1x10G'
OPTICS_100G_64 = '-m 1-32:optics_2x100G'
OPTICS_PAM4_100G_64 = '-m 1-32:optics_2x100G-pam4'
#### tianhe_SDK_9.26_32x400G_PRBS_With_Loopback_Test ####
PRBS_TOOL = 'python diagtest_sdk.py --case ber --port_mode '
PORT_400G_MODE = '1x400'
PORT_100G_MODE = '4x100'
PORT_100G_32_MODE = '1x100'
FEC_OPTION = '--fec --ber_threshold 1e-12'
PORT_40G_MODE = '1x40'
PORT_25G_MODE = '4x25'
PORT_10G_MODE = '4x10'
PORT_100G_64_MODE = '2x100'
BER_OPTION = '--ber_threshold 1e-12'
#### tianhe_SDK_9.34_64x100G_PRBS_With_Loopback_Test ####
DIAGTEST_TOOL1 = 'diagtest serdes prbs mode-en 1-64 1'
DIAGTEST_TOOL2 = 'diagtest serdes prbs set 1-64 1 prbs31 6 120000'
DIAGTEST_TOOL3 = 'diagtest serdes prbs sync 1-64'
DIAGTEST_TOOL4 = 'shell sleep 130'
DIAGTEST_TOOL5 = 'diagtest serdes prbs get 1-64'
DIAGTEST_TOOL6 = 'diagtest serdes prbs clear 1-64'
DIAGTEST_TOOL7 = 'diagtest serdes prbs mode-en 1-64 0'
DIAGTEST_TOOL_LST = [DIAGTEST_TOOL1, DIAGTEST_TOOL2, DIAGTEST_TOOL3, DIAGTEST_TOOL4, DIAGTEST_TOOL5, DIAGTEST_TOOL6, DIAGTEST_TOOL7, 'exit']
PRBS_64_100G = '128'
PRBS_32_100G = '32'
PRBS_400G = '256'
DIAGTEST_TOOL8 = 'diagtest serdes prbs set 1-64 1 prbs31 1593750 30000'
BER_100G_LST = [DIAGTEST_TOOL1, DIAGTEST_TOOL8, DIAGTEST_TOOL3, DIAGTEST_TOOL4, DIAGTEST_TOOL5, DIAGTEST_TOOL6, DIAGTEST_TOOL7, 'exit']
PRBS_2_100G_OPTION = '-m "1-1:copper_2x100:fec-def;2-2:optics_2x100:fec-def;3-3:copper_2x100:fec-def;4-4:optics_2x100:fec-def"'
PRBS_TOOL1 = 'diagtest serdes prbs mode-en 1-8 1'
PRBS_TOOL2 = 'diagtest serdes prbs set 1-8 1 prbs31 6 120000'
PRBS_TOOL3 = 'diagtest serdes prbs sync 1-8'
PRBS_TOOL4 = 'diagtest serdes prbs get 1-8'
PRBS_TOOL5 = 'diagtest serdes prbs clear 1-8'
PRBS_TOOL6 = 'diagtest serdes prbs mode-en 1-8 0'
PRBS_LST = [PRBS_TOOL1, PRBS_TOOL2, PRBS_TOOL3, DIAGTEST_TOOL4, PRBS_TOOL4, PRBS_TOOL5, PRBS_TOOL6, 'exit']
#### tianhe_SDK_9.38_32x400G_PRBS_Test_Via_ONIE_PORT_CMD ####
ShellPortCmd = './cls_shell ifcs show devport'
ONIE_PORT = 'onie_port_cmd'
PRBS_OPTION = '--port fpp1-fpp32 prbs --enable='
PRBS_OPTION1 = '--port fpp1-1-fpp32-2 prbs --enable='
PRBS_OPTION2 = '--port fpp1-1-fpp32-4 prbs --enable='
ENABLE_PATTERN = '1'
DISABLE_PATTERN = '0'
BER_SET_TIME1 = 'onie_port_cmd --port fpp1-fpp32 prbs --run --time=300'
BER_SET_TIME1_1 = 'onie_port_cmd --port fpp1-1-fpp32-2 prbs --run --time=300'
BER_SET_TIME1_2 = 'onie_port_cmd --port fpp1-1-fpp32-4 prbs --run --time=300'
BER_SET_TIME2 = 'onie_port_cmd --port fpp1-fpp32 prbs --sync'
BER_SET_TIME3 = './cls_shell shell sleep 300'
BER_READ_CMD = 'onie_port_cmd --port fpp1-fpp32 prbs --read'
BER_READ_CMD1 = 'onie_port_cmd --port fpp1-1-fpp32-2 prbs --read'
BER_READ_CMD2 = 'onie_port_cmd --port fpp1-1-fpp32-4 prbs --read'
BER_READ_LST = [BER_SET_TIME1, BER_READ_CMD]
BER_READ_LST1 = [BER_SET_TIME1_1, BER_READ_CMD1]
BER_READ_LST2 = [BER_SET_TIME1_2, BER_READ_CMD2]
SDK_SHELL_EXIT = './cls_shell exit'
integrator_OPTICS_100G = '-m "1-32:optics_2x100G:down-p2:fec-dis" -d -k'
#### tianhe_SDK_9.46_FEC_Test ####
DIAGTEST_SDK_TOOL = 'python diagtest_sdk.py --case '
PORT_MODE_OPTION1 = 'fec --port_mode 1x400'
PORT_MODE_OPTION2 = 'fec --port_mode 1x400 --module_type optics'
PORT_MODE_OPTION3 = 'fec --port_mode 4x100'
PORT_MODE_OPTION4 = 'fec --port_mode 4x100 --module_type optics'
PORT_MODE_OPTION5 = 'fec --port_mode 2x100'
PORT_MODE_OPTION6 = 'fec --port_mode 2x100 --module_type optics'
PORT_MODE_OPTION7 = 'fec --port_mode 1x100'
PORT_MODE_OPTION8 = 'fec --port_mode 1x100 --module_type optics'
PORT_MODE_OPTION9 = 'fec --port_mode 4x25'
PORT_MODE_OPTION10 = 'fec --port_mode 4x25 --module_type optics'
PORT_MODE_OPTION11 = 'fec --port_mode 1x40'
PORT_MODE_OPTION12 = 'fec --port_mode 1x40 --module_type optics'
PORT_MODE_OPTION13 = 'fec --port_mode 4x10'
PORT_MODE_OPTION14 = 'fec --port_mode 4x10 --module_type optics'
Remote_Shell_CMD = './auto_load_user.sh -d'
EMPHASSIS_OPTION1 = 'pre_emphassis --port_mode 1x400 --module_type copper --snake_topology p2p'
EMPHASSIS_OPTION2 = 'pre_emphassis --port_mode 4x100 --module_type copper --snake_topology p2p'
EMPHASSIS_OPTION3 = 'pre_emphassis --port_mode 2x100 --module_type copper'
EMPHASSIS_OPTION4 = 'pre_emphassis --port_mode 1x400 --module_type optics'
EMPHASSIS_OPTION5 = 'pre_emphassis --port_mode 4x100 --module_type optics'
EMPHASSIS_OPTION6 = 'pre_emphassis --port_mode 2x100 --module_type optics'
EMPHASSIS_OPTION7 = 'pre_emphassis --port_mode 1x40 --module_type optics'
EMPHASSIS_OPTION8 = 'pre_emphassis --port_mode 4x10 --module_type optics'
TRAFFIC_OPTION1 = 'traffic --duration_seconds 300 --port_mode 4x100 --packet_size 322 --inject_num 4000 --split_flows --run_ber --ber_threshold 5e-6 --max_Tj 108 --max_master 105'
TRAFFIC_OPTION2 = 'traffic --duration_seconds 300 --port_mode 2x100 --packet_size 322 --inject_num 4000 --split_flows --max_Tj 108 --max_master 105 --fec'
TRAFFIC_OPTION3 = 'traffic --duration_seconds 300 --packet_size 330 --max_Tj 108 --max_master 105'
#### tianhe_SDK_9.51_Snake_Test ####
RM_MEM_LOG = 'rm -rf /root/diag/output/mem.log'
FREE_TOOL = 'while true; do free -m >> /root/diag/output/mem.log; sleep 1; done &'
MEM_TEST_TOOL = '/root/diag/cel-mem-test --all -C 6000M > /root/diag/output/cel-mem-test.log &'
MEM_LST = [RM_MEM_LOG, FREE_TOOL, MEM_TEST_TOOL]
PS_TOOL = 'ps | grep "cel-mem-test" |grep -v "grep"'
Snake_TAR_FILE = 'innovium_snake_tests_utils.0.v9.1.0.tar.gz'
Snake_Test_V9 = 'cls_snake_testsuite_v9.sh'
Snake_TestSuite = 'cls_snake_testsuite.py'
Snake_FILE_LST = [Snake_TAR_FILE, Snake_Test_V9, Snake_TestSuite]
TAIL_TOOL = 'tail -f /root/diag/output/cel-mem-test.log'
MEM_RESULT = 'cat /root/diag/output/cel-mem-test.log'
MEM_FREE_RESULT = 'cat /root/diag/output/mem.log'
PORT_64_100G_MODE = '64x100-1G'
COPPER_PORT_OPTION = '-m "1-8:Copper_4x25;9-22:Copper_2x100;23-32:Copper_4x25"'
PORT_ENABLE_ALL = 'port enable all'
PORT_ENABLE_ALL1 = 'port enable 1-32'
COPPER_PORT_OPTION1 = '-m "1-20:Copper_1x100;21-24:Copper_4x10G;25-32:1x100G"'
COPPER_PORT_OPTION2 = '-m "1-20:Copper_1x100G;21-24:Copper_4x10G;25-32:Copper_4x100G"'
SpeedType1 = '10_1'
SpeedType2 = '10_2'
SpeedType3 = '10_3'
#### tianhe_SDK_11.3_Default_Onie_fppPort_Mode ####
ONIE_FPP = 'setenv onie_fpp ""'
SFP_DETECT_OPTION1 = '-m "sfp_detect" -d'
SFP_DETECT_OPTION2 = '-m "sfp_detect" -k -d'
VLAN_TOOL = './cls_shell diagtest knet show'
KNET_PATTERN = '64'


