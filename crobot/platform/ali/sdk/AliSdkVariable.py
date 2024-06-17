###############################################################################
# LEGALESE:   "Copyright (C) 2019-2021, Celestica Corp. All rights reserved." #
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

from common.sdk.Sdk_variable import fail_pattern
from common.sdk.Sdk_variable import BCM_promptstr
from common.sdk.Sdk_variable import port_mac_cmd
from common.sdk.Sdk_variable import port_phy_cmd
from common.sdk.Sdk_variable import check_bcm_user

devicename = os.environ.get("deviceName", "")
import logging
logging.info("devicename:{}".format(devicename))
if "migaloo" in devicename.lower():
    sdk_parent_path = '/usr/local/migaloo/'
    sdk_path = '/usr/local/migaloo/SDK'
    diag_path = '/usr/local/migaloo/CPU_Diag'
    sdk_version_file = 'version'
    version_pattern = r'(\d+\.\d+\.\d+)'
else:
    sdk_parent_path = '/usr/local/CPU_Diag/utility/'
    sdk_path = '/usr/local/CPU_Diag/utility/Shamu_SDK'
    diag_path = '/usr/local/CPU_Diag/bin'
    sdk_version_file = 'Version'
    version_pattern = r'Version <(\d+\.\d+\.\d+)>'
    prbs_stat_cmd_for_shamu = 'dsh -c "phy diag 1-69 prbsstat ber"'
    set_40x100G_rate = "bcm56780_a0-generic-40x100.config.yml"
    common_ucode_version_for_shamu = 'D005_09'
    test_10gkr_cmd_for_shamu = './cel-10gKR-test -t'
    test_10gkr_pass_pattern_kr_test_for_shamu = r'(\w+?kr_.*?PASS\s])'
    test_remote_SDK_version_test_for_shamu = r'(Release:\s+?sdk-6.5.21)'
    let_CPU_send_package_cmd_for_shamu = "tx 100 pbm=cd0 vlan=100 DM=0x2"
    let_CPU_send_package_100_cmd_for_shamu = "tx 100 pbm=cd0 vlan=100 length=100 DM=0x2"
    let_CPU_send_package_1280_cmd_for_shamu = "tx 100 pbm=cd0 vlan=100 length=1280 DM=0x2"
    stop_traffic_cmd_for_shamu = "port cd0 en=off"
    show_c_cd_cmd = "show c cd"
    port_cd_on_cmd = "port cd0 en=on"
    dsc_check = 'dsh -c "phy diag 1-69 dsc"'
    PORT_BER_TOLERANCE_FOR_SHAMU = 1e-6  ## WORKAROUND is checking this value.
    error_pattern = r'(error|Error|ERROR|failed|FAILED|fail|Fail|FAIL)'

### specific for shamu begin
port_TX_RX_pattern = r"(.*\.cd\d+).*?:.*?(\d[,0-9]+).*?(\d[,0-9]+)"
set_snake_vlan_200G_cmd_for_shamu = "rcload snake_script.soc"
### specific for shamu end

SDKLT_PROMPT = "sdklt.0>"
CINT_PROMPT = "cint>"
PCIE_INFO_CMD = "PCIEphy fwinfo"

BER_PORT_PATTERN = "(\d+\.\d+e\-\d+)"
LOSS_OF_LOCK = "LossOfLock"
PORT_BER_TOLERANCE = 1e-4  ## WORKAROUND is checking this value.
SDK_SCRIPT = "auto_load_user.sh"
BCM_USER = "bcm.user"
BCM_VERSION = "6.5.21"
set_snake_vlan_200G_cmd = "linespeed200G.soc"
prbs_stat_cmd = "phy diag 1-262 prbsstat ber"
pvlan_show_cmd = "pvlan show"
vlan_show_cmd = "vlan show"
show_c_cmd = "show c"
clear_c_cmd = "clear c"
ps_cmd = "ps"
ps_cd_cmd = "ps cd"
ps_ce_cmd = "ps ce"
loopback_mode_mac = ["up", "(?:200G|400G)", "FD", "No", "Forward", "TX RX", "Backplane", "9412", "RS544-2xN", 'MAC']
loopback_mode_phy = ["up", "(?:200G|400G)", "FD", "No", "Forward", "TX RX", "Backplane", "9412", "RS544-2xN", 'PHY']
port_up_status = ["up", "(?:200G|400G)", "FD", "No",  "Forward", "TX RX", "Backplane", "9412", "RS544-2xN"]
port_down_status = ["!ena", "(?:200G|400G)", "FD", "No",  "Forward", "TX RX", "Backplane", "9412", "RS544-2xN"]
port_pattern = r"cd\d+\(\s*\d+\)|P\d+|Port\d+|ce\d+\(\s*\d+\)"

let_CPU_send_package_cmd = "tx 1000 pbm=cd0 vlan=10 length=295 SM=0x1 DM=0x2"
sleep_300s_cmd = "sleep 300"
sleep_pattern = ["Sleeping for"]

stop_traffic_cmd = "pvlan set cd127 1888"
port_XLMIB_RPKT_pattern = r"(XLMIB_RPKT\.cd\d+).*?:.*?(\d[,0-9]+).*?(\d[,0-9]+)"

test_10gkr_cmd = './cel-10KR-test -a'
test_10gkr_pass_pattern = r'10G KR test.*?PASS'

phy_info_pattern = []
for i in range (1, 65):
    mdio_str = '0x%04x'%(0x400 + i)
    port_str = '%02d' % i
    pattern = r'\d+:\s' + mdio_str + r'\s+TSCBHGEN3A0-A0/' + port_str
    phy_info_pattern.append(pattern + '/0-3')
    phy_info_pattern.append(pattern + '/4-7')

common_ucode_version = 'D005_0B'
common_ucode_pattern = r'Common Ucode Version = (\w+)'

cls_shell = "cel_bcmshell"
cls_shell_port_status = "%s ps cd"%(cls_shell)
cls_shell_exit = "%s exit\n"%(cls_shell)

kill_bcm = "killall -9 bcm.user"
cls_shell_sdk_version = "%s version"%(cls_shell)

tx_rx_pkt_patterns = [
    r'(XLMIB_TBYT)\.cd.*?:(.*?)\+([,0-9]+)'
    r'(XLMIB_RBYT)\.cd.*?:(.*?)\+([,0-9]+)'
    r'(XLMIB_TPOK)\.cd.*?:(.*?)\+([,0-9]+)'
    r'(XLMIB_RPOK)\.cd.*?:(.*?)\+([,0-9]+)'
    r'(XLMIB_TUCA)\.cd.*?:(.*?)\+([,0-9]+)'
    r'(XLMIB_RUCA)\.cd.*?:(.*?)\+([,0-9]+)'
    r'(XLMIB_TPKT)\.cd.*?:(.*?)\+([,0-9]+)'
    r'(XLMIB_RPKT)\.cd.*?:(.*?)\+([,0-9]+)'
    r'(XLMIB_T64)\.cd.*?:(.*?)\+([,0-9]+)'
    r'(XLMIB_R64)\.cd.*?:(.*?)\+([,0-9]+)'
    r'(XLMIB_RPRM)\.cd.*?:(.*?)\+([,0-9]+)'
]
