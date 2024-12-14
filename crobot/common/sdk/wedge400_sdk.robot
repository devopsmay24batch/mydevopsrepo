##############################################################################
# LEGALESE:   "Copyright (C) 2019-2020, Celestica Corp. All rights reserved." #
#                                                                             #
# This source code is confidential, proprietary, and contains trade           #
# secrets that are the sole property of Celestica Corp.                       #
# Copy and/or distribution of this source code or disassembly or reverse      #
# engineering of the resultant object code are strictly forbidden without     #
# the written consent of Celestica Corp.                                      #
#                                                                             #
###############################################################################
#######################################################################################################################
# Script       : wedge400_diag.robot                                                                                 #
# Date         : April 14, 2020                                                                                       #
# Author       : Prapatsorn W.                                                                                        #
# Description  : This script will validate SDK package for wedge400                                                  #
#                                                                                                                   #
# Script Revision Details:                                                                                            #
#
######################################################################################################################

*** Settings ***
Documentation       This Suite will validate SDK package

Force Tags        SDK
Resource          Resource.robot
Library           SdkLibAdapter.py
Variables         Sdk_variable.py

Suite Setup       Connect Device
Suite Teardown    Disconnect Device

*** Variables ***
${LoopCnt}        7
${MaxLoopNum}     7

*** Test Cases ***
FB_SDK_BCM_COM_TC_001_Load and Initialization SDK Test
    [Documentation]  This test checks SDK initialization
    [Tags]     common  wedge400  FB_SDK_BCM_COM_TC_001_Load_and_Initialization_SDK_Test
    [Timeout]  15 min 00 seconds
    [Setup]    change dir to sdk path
    Step  1  copy sdk soc files w400
    Step  2  verify load HSDK
    [Teardown]  exit BCM

FB_SDK_BCM_COM_TC_002_Default Port Info Test
    [Documentation]  This test checks port default info with each speed.
    [Tags]     common  wedge400  FB_SDK_BCM_COM_TC_002_Default_Port_Info_Test
    [Timeout]  30 min 00 seconds
    [Setup]    change dir to sdk path
    Step  1  verify load HSDK  ${SDK_SCRIPT} -m 16x400G_32x200G_PAM4
    Step  2  check all port status
    Step  3  exit BCM
    Step  4  verify load HSDK  ${SDK_SCRIPT} -m 16x200G_PAM4_32x100G_NRZ
    Step  5  check all port status
    Step  6  check all port status  port_cmd=${ps_ce_cmd}
    Step  7  exit BCM
    Step  8  verify load HSDK  ${SDK_SCRIPT} -m 16x100G_32x100G_NRZ
    Step  9  check all port status  port_cmd=${ps_ce_cmd}
    Step  10  exit BCM
    Step  11  verify load HSDK  ${SDK_SCRIPT} -m 16x100G_64x50G
    Step  12  check all port status  port_cmd=${ps_ce_cmd}
    Step  13  check all port status  port_cmd=${ps_xe_cmd}
    Step  14  exit BCM
    Step  15  verify load HSDK  ${SDK_SCRIPT} -m 32x100G_32x100G_NRZ
    Step  16  check all port status  port_cmd=${ps_ce_cmd}
    [Teardown]  exit BCM

FB_SDK_BCM_COM_TC_003_QSFPDD 1x400G Port Status Test
    [Documentation]  This test checks QSFPDD(400G) port status
    [Tags]  FB_SDK_BCM_COM_TC_003_QSFPDD_1x400G_Port_Status_Test  common  wedge400
    [Timeout]  9 min 00 seconds
    [Setup]    change dir to sdk path
    Step  1  verify load HSDK  ${SDK_SCRIPT} -m 16x400G_32x200G_PAM4
    Step  2  check all port status
    Step  3  set snake vlan to all ports w400  ${set_snake_vlan_400G_cmd}
    Step  4  stop traffic
    Step  5  check all port status w400  port_cmd=${portdump_counters_cmd}
    Step  6  exit BCM
    Step  7  verify load HSDK  ${SDK_SCRIPT} -m 16x400G_PAM4_32x100G_NRZ
    Step  8  check all port status
    Step  9  check all port status  port_cmd=${ps_ce_cmd}
    Step  10  set snake vlan to all ports w400  port_cmd=${set_snake_vlan_400G_cmd}  sustain_time=${sleep_time}
    Step  11  stop traffic
    Step  12  check all port status w400  port_cmd=${portdump_counters_cmd}
    [Teardown]  exit BCM

FB_SDK_BCM_COM_TC_004_QSFPDD 1x200G Port Status Test
    [Documentation]  This test checks QSFPDD(200G) port status
    [Tags]  FB_SDK_BCM_COM_TC_004_QSFPDD_1x200G_Port_Status_Test  common  wedge400
    [Timeout]  5 min 00 seconds
    [Setup]    change dir to sdk path
    Step  1  verify load HSDK  ${SDK_SCRIPT} -m 16x200G_PAM4_32x100G_NRZ
    Step  2  check all port status
    Step  3  check all port status  port_cmd=${ps_ce_cmd}
    Step  4  set snake vlan to all ports w400  ${set_snake_vlan_200G_cmd}  sustain_time=${sleep_time}
    Step  5  stop traffic
    Step  6  check all port status w400  port_cmd=${portdump_counters_cmd}
    [Teardown]  exit BCM

FB_SDK_BCM_COM_TC_005_QSFPDD_1x100G_Port_Status_Test
    [Documentation]  This test checks QSFPDD(100G) port status
    [Tags]  FB_SDK_BCM_COM_TC_005_QSFPDD_1x100G_Port_Status_Test   common  wedge400
    [Timeout]  9 min 00 seconds
    [Setup]    change dir to sdk path
    Step  1  verify load HSDK  ${SDK_SCRIPT} -m 16x100G_32x100G_NRZ
    Step  2  check all port status  port_cmd=${ps_ce_cmd}
    Step  4  set snake vlan to all ports w400  ${set_snake_vlan_100G_cmd}  sustain_time=${sleep_time}
    Step  5  stop traffic  ${stop_traffic_cmd_DD100G}
    Step  6  check all port status w400  port_cmd=${portdump_counters_cmd_100G}
    Step  7  exit BCM
    Step  8  verify load HSDK  ${SDK_SCRIPT} -m 16x100G_64x50G
    Step  9  check all port status  port_cmd=${ps_ce_cmd}
    Step  10  check all port status  port_cmd=${ps_xe_cmd}
    Step  11  set snake vlan to all ports w400  ${set_snake_vlan_100G_cmd}  sustain_time=${sleep_time}
    Step  12  stop traffic  ${stop_traffic_cmd_DD100G}
    Step  13  check all port status w400  port_cmd=${portdump_counters_cmd_100G}
    [Teardown]  exit BCM

FB_SDK_BCM_COM_TC_006_QSFP56_1x200G_Port_Status_Test
    [Documentation]  This test checks QSFP56(200G) port status
    [Tags]  FB_SDK_BCM_COM_TC_006_QSFP56_1x200G_Port_Status_Test  common  wedge400
    [Timeout]  85 min 00 seconds
    [Setup]    change dir to sdk path
    Step  1  verify load HSDK  ${SDK_SCRIPT} -m 16x400G_32x200G_PAM4
    Step  2  check all port status
    Step  4  set snake vlan to all ports w400  ${set_snake_vlan_200G_cmd_56}  sustain_time=${sleep_time}
    Step  5  stop traffic  ${stop_traffic_cmd_56200G}
    Step  6  check all port status w400  port_cmd=${portdump_counters_cmd_200G_56}
    [Teardown]  exit BCM

FB_SDK_BCM_COM_TC_007_QSFP56_1x100G_Port_Status_Test
    [Documentation]  This test checks QSFP56(100G) port status
    [Tags]  FB_SDK_BCM_COM_TC_007_QSFP56_1x100G_Port_Status_Test  common  wedge400
    [Timeout]  45 min 00 seconds
    [Setup]    change dir to sdk path
    Step  1  verify load HSDK  ${SDK_SCRIPT} -m 16x200G_PAM4_32x100G_NRZ
    Step  2  check all port status
    Step  3  check all port status  port_cmd=${ps_ce_cmd}
    Step  4  set snake vlan to all ports w400  ${set_snake_vlan_100G_cmd_56_400200}  sustain_time=${sleep_time}
    Step  5  stop traffic  ${stop_traffic_cmd_56100G}
    Step  6  check all port status w400  port_cmd=${portdump_counters_cmd_100G_56}
    Step  7  exit BCM
    Step  8  verify load HSDK  ${SDK_SCRIPT} -m 16x100G_32x100G_NRZ
    Step  9  check all port status  port_cmd=${ps_ce_cmd}
    Step  10  set snake vlan to all ports w400  ${set_snake_vlan_100G_cmd_56_100}  sustain_time=${sleep_time}
    Step  11  stop traffic  ${stop_traffic_cmd_56100G_1}
    Step  12  check all port status w400  port_cmd=${portdump_counters_cmd_100G_56_100}
    Step  13  exit BCM
    Step  14  verify load HSDK  ${SDK_SCRIPT} -m 16x400G_PAM4_32x100G_NRZ
    Step  15  check all port status
    Step  16  check all port status  port_cmd=${ps_ce_cmd}
    Step  17  set snake vlan to all ports w400  ${set_snake_vlan_100G_cmd_56_400200}  sustain_time=${sleep_time}
    Step  18  stop traffic  ${stop_traffic_cmd_56100G}
    Step  19  check all port status w400  port_cmd=${portdump_counters_cmd_100G_56}
    [Teardown]  exit BCM

FB_SDK_BCM_COM_TC_008_QSFP56_1x50G_Port_Status_Test
    [Documentation]  This test checks QSFP56(50G) port status
    [Tags]  FB_SDK_BCM_COM_TC_008_QSFP56_1x50G_Port_Status_Test   common  wedge400
    [Timeout]  95 min 00 seconds
    [Setup]    change dir to sdk path
    Step  1  verify load HSDK  ${SDK_SCRIPT} -m 16x100G_64x50G
    Step  2  check all port status  port_cmd=${ps_ce_cmd}
    Step  3  check all port status  port_cmd=${ps_xe_cmd}
    Step  4  set snake vlan to all ports w400  ${set_snake_vlan_50G_cmd_56}  sustain_time=${sleep_time}
    Step  5  stop traffic  ${stop_traffic_cmd_5650G}
    Step  6  check all port status w400  port_cmd=${portdump_counters_cmd_50G_56}
    [Teardown]  exit BCM

FB_SDK_BCM_COM_TC_009_QSFPDD_1x400G_Port_Mapping_Test
    [Documentation]  This test checks QSFPDD(400G) port mapping
    [Tags]  FB_SDK_BCM_COM_TC_009_QSFPDD_1x400G_Port_Mapping_Test   common  wedge400
    [Timeout]  20 min 00 seconds
    [Setup]    change dir to sdk path
    Step  1  verify load HSDK  ${SDK_SCRIPT} -m 16x400G_32x200G_PAM4
    Step  2  check all port status  ${port_up_status_400G}  ${ps_cmd}  ${port_pattern_400G}
    Step  3  exit BCM
    Step  4  verify load HSDK  ${SDK_SCRIPT} -m 16x400G_PAM4_32x100G_NRZ
    Step  5  check all port status  ${port_up_status_400G}  ${ps_cmd}  ${port_pattern_400G}
    [Teardown]  exit BCM

FB_SDK_BCM_COM_TC_010_QSFPDD_1x200G_Port_Mapping_Test
    [Documentation]  This test checks QSFPDD(200G) port mapping
    [Tags]  FB_SDK_BCM_COM_TC_010_QSFPDD_1x200G_Port_Mapping_Test   common  wedge400
    [Timeout]  20 min 00 seconds
    [Setup]    change dir to sdk path
    Step  1  verify load HSDK  ${SDK_SCRIPT} -m 16x200G_PAM4_32x100G_NRZ
    Step  2  check all port status  ${port_up_status_200G}  ${ps_cmd}  ${port_pattern_200G}
    [Teardown]  exit BCM

FB_SDK_BCM_COM_TC_011_QSFPDD_1x100G_Port_Mapping_Test
    [Documentation]  This test checks QSFPDD(100G) port mapping
    [Tags]  FB_SDK_BCM_COM_TC_011_QSFPDD_1x100G_Port_Mapping_Test   common  wedge400
    [Timeout]  20 min 00 seconds
    [Setup]    change dir to sdk path
    Step  1  verify load HSDK  ${SDK_SCRIPT} -m 16x100G_32x100G_NRZ
    Step  2  check all port status  ${port_up_status_100G}  ${ps_cmd}  ${port_pattern_100G}
    Step  3  exit BCM
    Step  4  verify load HSDK  ${SDK_SCRIPT} -m 16x100G_64x50G
    Step  5  check all port status  ${port_up_status_100G_1}  ${ps_cmd}  ${port_pattern_100G}
    [Teardown]  exit BCM

FB_SDK_BCM_COM_TC_012_QSFP56_1x200G_Port_Mapping_Test
    [Documentation]  This test checks QSFP56(200G) port mapping
    [Tags]  FB_SDK_BCM_COM_TC_012_QSFP56_1x200G_Port_Mapping_Test   common  wedge400
    [Timeout]  20 min 00 seconds
    [Setup]    change dir to sdk path
    Step  1  verify load HSDK
    Step  2  check all port status  ${port_up_status_200G}  ${ps_cmd}  ${port_pattern_200G}
    [Teardown]  exit BCM

FB_SDK_BCM_COM_TC_013_QSFP56_1x100G_Port_Mapping_Test
    [Documentation]  This test checks QSFP56(100G) port mapping
    [Tags]  FB_SDK_BCM_COM_TC_013_QSFP56_1x100G_Port_Mapping_Test   common  wedge400
    [Timeout]  20 min 00 seconds
    [Setup]    change dir to sdk path
    Step  1  verify load HSDK  ${SDK_SCRIPT} -m 16x200G_PAM4_32x100G_NRZ
    Step  2  check all port status  ${port_up_status_100G}  ${ps_cmd}  ${port_pattern_100G}
    Step  3  exit BCM
    Step  4  verify load HSDK  ${SDK_SCRIPT} -m 16x100G_32x100G_NRZ
    Step  5  check all port status  ${port_up_status_100G}  ${ps_cmd}  ${port_pattern_100G}
    Step  6  exit BCM
    Step  7  verify load HSDK  ${SDK_SCRIPT} -m 16x400G_PAM4_32x100G_NRZ
    Step  8  check all port status  ${port_up_status_100G}  ${ps_cmd}  ${port_pattern_100G}
    [Teardown]  exit BCM

FB_SDK_BCM_COM_TC_014_QSFP56_2x50G_Port_Mapping_Test
    [Documentation]  This test checks QSFP56(50G) port mapping
    [Tags]  FB_SDK_BCM_COM_TC_014_QSFP56_2x50G_Port_Mapping_Test   common  wedge400
    [Timeout]  20 min 00 seconds
    [Setup]    change dir to sdk path
    Step  1  verify load HSDK  ${SDK_SCRIPT} -m 16x100G_64x50G
    Step  2  check all port status  ${port_up_status_50G}  ${ps_cmd}  ${port_pattern_50G}
    [Teardown]  exit BCM

FB_SDK_BCM_COM_TC_018_TH3_Temperature_Test
    [Documentation]  This test checks TH3 Temperature
    [Tags]  FB_SDK_BCM_COM_TC_018_TH3_Temperature_Test   common  wedge400
    [Timeout]  20 min 00 seconds
    [Setup]    change dir to sdk path
    Step  1  verify load HSDK
    Step  2  check all port status  port_cmd=${ps_cmd}
    Step  3  show temp
    [Teardown]  exit BCM

FB_SDK_BCM_COM_TC_020_Remote_Shell_Test
    [Documentation]  This test checks Remote Shell Test
    [Tags]  FB_SDK_BCM_COM_TC_020_Remote_Shell_Test  common  wedge400
    [Timeout]  5 min 00 seconds
    [Setup]    change dir to sdk path
    Step  1  verify remote shell  ${remote_shell_load_sdk}  ${fail_dict}
    Step  2  verify remote shell port status
    Step  3  verify remote shell  ${cls_shell_exit}  ${fail_dict}
    Step  4  check remote shell port  sp=${True}
    [Teardown]  go to centos

FB_SDK_BCM_COM_TC_023_Serdes_FW_Test
    [Documentation]  This test checks Serdes FW Test
    [Tags]  FB_SDK_BCM_COM_TC_023_Serdes_FW_Test  common  wedge400
    [Timeout]  50 min 00 seconds
    [Setup]    change dir to sdk path
    Step  1  verify load HSDK  ${SDK_SCRIPT} -m 16x400G_32x200G_PAM4
    Step  2  check lane common ucode version
    Step  3  exit BCM
    Step  4  verify load HSDK  ${SDK_SCRIPT} -m 16x200G_PAM4_32x100G_NRZ
    Step  5  check lane common ucode version  ${get_lane_serdes_version_cmd_200G}
    Step  6  check lane common ucode version  ${get_lane_serdes_version_cmd_100G}
    Step  7  exit BCM
    Step  8  verify load HSDK  ${SDK_SCRIPT} -m 16x100G_32x100G_NRZ
    Step  9  check lane common ucode version  ${get_lane_serdes_version_cmd_ce}
    Step  10  exit BCM
    Step  11  verify load HSDK  ${SDK_SCRIPT} -m 16x400G_PAM4_32x100G_NRZ
    Step  12  check lane common ucode version  ${get_lane_serdes_version_cmd_200G}
    Step  13  check lane common ucode version  ${get_lane_serdes_version_cmd_100G}
    Step  14  exit BCM
    Step  15  verify load HSDK  ${SDK_SCRIPT} -m 16x100G_64x50G
    Step  16  check lane common ucode version  ${get_lane_serdes_version_cmd_ce_100G}
    Step  17  check lane common ucode version  ${get_lane_serdes_version_cmd_xe}
    [Teardown]  exit BCM

FB_SDK_BCM_COM_TC_025_TH3_High_Power_Test
    [Documentation]  This test checks TH3 High Power Test
    [Tags]  FB_SDK_BCM_COM_TC_025_TH3_High_Power_Test  common  wedge400
    [Timeout]  50 min 00 seconds
    [Setup]    change dir to sdk path
    Step  1  verify load HSDK
    Step  2  check all port status  ${port_up_status}
    Step  3  switch to openbmc
    Step  4  check power sensor value
    Step  5  stop traffic  ${stop_traffic_cmd_th3}
    Step  6  check all port status w400  port_cmd=${portdump_counters_cmd_th3}
    [Teardown]  exit BCM

FB_SDK_BCM_COM_TC_050_QSFPDD(400G)_QSFP56(200G)_PRBS_Test
    [Documentation]  This test checks QSFPDD(400G) QSFP56(200G) PRBS Test
    [Tags]  FB_SDK_BCM_COM_TC_050_QSFPDD(400G)_QSFP56(200G)_PRBS_Test  common  wedge400
    [Timeout]  35 min 00 seconds
    [Setup]    change dir to sdk path
    Step  1  verify load HSDK
    Step  2  check all port status  ${port_up_status}
    Step  3  set prbs mode and run PRBS test  ${set_prbs_run_PRBS_cmd_400G}
    Step  4  check BER level  ber_cmd=${get_port_BER_level_cmd_400G}  ber_cmd_second=${get_port_BER_level_cmd_second_400G}
    [Teardown]  exit BCM

FB_SDK_BCM_COM_TC_051_QSFPDD(200G)_QSFP56(100G)_PRBS_Test
    [Documentation]  This test checks QSFPDD(200G) QSFP56(100G) PRBS Test
    [Tags]  FB_SDK_BCM_COM_TC_051_QSFPDD(200G)_QSFP56(100G)_PRBS_Test  common  wedge400
    [Timeout]  35 min 00 seconds
    [Setup]    change dir to sdk path
    Step  1  verify load HSDK  ${SDK_SCRIPT} -m 16x200G_PAM4_32x100G_NRZ
    Step  2  check all port status  ${port_up_status}
    Step  3  set prbs mode and run PRBS test  ${set_prbs_run_PRBS_cmd_200G}
    Step  4  check BER level  ber_cmd=${get_port_BER_level_cmd_200G}  ber_cmd_second=${get_port_BER_level_cmd_second_200G}
    [Teardown]  exit BCM

FB_SDK_BCM_COM_TC_052_QSFPDD(100G)_QSFP56(100G)_PRBS_Test
    [Documentation]  This test checks QSFPDD(100G) QSFP56(100G) PRBS Test
    [Tags]  FB_SDK_BCM_COM_TC_052_QSFPDD(100G)_QSFP56(100G)_PRBS_Test  common  wedge400
    [Timeout]  35 min 00 seconds
    [Setup]    change dir to sdk path
    Step  1  verify load HSDK  ${SDK_SCRIPT} -m 16x100G_32x100G_NRZ
    Step  2  check all port status  port_cmd=${ps_ce_cmd}
    Step  3  set prbs mode and run PRBS test  ${set_prbs_run_PRBS_cmd_100G}
    Step  4  check BER level  ber_cmd=${get_port_BER_level_cmd_100G}  ber_cmd_second=${get_port_BER_level_cmd_second_100G}
    [Teardown]  exit BCM

FB_SDK_BCM_COM_TC_053_QSFPDD(400G)_QSFP56(100G)_PRBS_Test
    [Documentation]  This test checks QSFPDD(400G) QSFP56(100G) PRBS Test
    [Tags]  FB_SDK_BCM_COM_TC_053_QSFPDD(400G)_QSFP56(100G)_PRBS_Test  common  wedge400
    [Timeout]  35 min 00 seconds
    [Setup]    change dir to sdk path
    Step  1  verify load HSDK  ${SDK_SCRIPT} -m 16x400G_PAM4_32x100G_NRZ
    Step  2  check all port status  ${port_up_status}
    Step  3  check all port status  port_cmd=${ps_ce_cmd}
    Step  4  set prbs mode and run PRBS test  ${set_prbs_run_PRBS_cmd_200G}
    Step  5  check BER level  ber_cmd=${get_port_BER_level_cmd_200G}  ber_cmd_second=${get_port_BER_level_cmd_second_200G}
    [Teardown]  exit BCM

FB_SDK_BCM_COM_TC_054_QSFPDD(100G)_QSFP56(50G)_PRBS_Test
    [Documentation]  This test checks QSFPDD(100G) QSFP56(50G) PRBS Test
    [Tags]  FB_SDK_BCM_COM_TC_054_QSFPDD(100G)_QSFP56(50G)_PRBS_Test  common  wedge400
    [Timeout]  35 min 00 seconds
    [Setup]    change dir to sdk path
    Step  1  verify load HSDK  ${SDK_SCRIPT} -m 16x100G_64x50G
    Step  2  check all port status  port_cmd=${ps_ce_cmd}
    Step  3  check all port status  port_cmd=${ps_xe_cmd}
    Step  4  set prbs mode and run PRBS test  ${set_prbs_run_PRBS_cmd_200G}
    Step  5  check BER level  ber_cmd=${get_port_BER_level_cmd_200G}  ber_cmd_second=${get_port_BER_level_cmd_second_200G}
    [Teardown]  exit BCM

BMC_SDK_BCM_COM_TC_055_Verify_PCIe_HW_Test
    [Documentation]  This test checks PCIe hw Test
    [Tags]  BMC_SDK_BCM_COM_TC_055_Verify_PCIe_HW_Test  common  wedge400
    [Timeout]  35 min 00 seconds
    [Setup]    change dir to sdk path
    FOR    ${INDEX}    IN RANGE    1    ${MaxLoopNum}
        Print Loop Info  ${INDEX}
        #Set Testcase Timeout  300
        Step  1  verify load HSDK w400
        Step  2  exit BCM
        Step  3  pcie lsmod check
    END
	Step  4  ssh disconnect
    Step  5  do power cycle
    Step  6  ssh login bmc

*** Keywords ***
Connect Device
    Set Library Order
    Sdk Device Connect
    Init Test Library
    ssh login bmc


Disconnect Device
    ssh disconnect
    Sdk Device Disconnect

Print Loop Info
    [Arguments]    ${CUR_INDEX}
    Log Info  *******************************************
    Log Info  *** Test Loop \#: ${CUR_INDEX} / ${LoopCnt} ***
    Log Info  *******************************************

