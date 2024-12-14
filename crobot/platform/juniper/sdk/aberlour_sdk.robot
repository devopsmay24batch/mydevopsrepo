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

*** Settings ***
Documentation       This Suite will validate SDK package

Library           JuniperAberlourSdkLib.py
Library           ../JuniperCommonLib.py
Library           SdkCommonLib.py
Library           CommonLib.py
Variables         JuniperCommonVariable.py
Variables         JuniperAberlourSdkVariable.py

Resource          JuniperSdkKeywords.resource

Suite Setup       DiagOS Connect Device
Suite Teardown    DiagOS Disconnect Device


*** Test Cases ***


ABERLOUR_SDK_TC_9.1_Load_and_Initialization_SDK_Test
    [Tags]  ABERLOUR_SDK_TC_9.1_Load_and_Initialization_SDK_Test
    [Setup]  change dir to sdk path
    Step  1  verify load SDK  -a
    [Teardown]  exit sdk mode

ABERLOUR_SDK_TC_9.3_PHY_Info_Test
    [Tags]  ABERLOUR_SDK_TC_9.3_PHY_Info_Test
    [Setup]  change dir to sdk path
    Step  1  verify load SDK  -a
    Step  2  check phy info
    [Teardown]  exit sdk mode

ABERLOUR_SDK_TC_9.4_Mdio_Advisor_Test
    [Tags]  ABERLOUR_SDK_TC_9.4_Mdio_Advisor_Test
    [Setup]  change dir to sdk path
    Step  1  verify loadSDK  -a
    Step  2  check mdio advisor
    [Teardown]  exit sdk mode


ABERLOUR_SDK_TC_9.40_Stacking_Qsfp28_100g_Port_Prbs_Sys_Side_Test
    [Tags]  ABERLOUR_SDK_TC_9.40_Stacking_Qsfp28_100g_Port_Prbs_Sys_Side_Test  
    [Setup]  change dir to sdk path

    Step  1  verify load sdk  -a
    Step  2  run cmd  epdm prbs set ce0-ce1 tx_rx=0 p=5 lane=all inv=0 if=sys  ${BCM_promptstr}
    Step  3  run cmd  phy diag ce0-ce1 prbs set p=3  ${BCM_promptstr}
    Step  4  check prbs ports sys side
    [Teardown]  exit sdk mode

ABERLOUR_SDK_TC_9.41_Stacking_Qsfp28_100g_Port_Prbs_Line_Side_Test
    [Tags]  ABERLOUR_SDK_TC_9.41_Stacking_Qsfp28_100g_Port_Prbs_Line_Side_Test
    [Setup]  change dir to sdk path
    Step  1  verify load sdk  -a
    Step  2  run cmd  epdm link all  ${BCM_promptstr}
    Step  3  run cmd  epdm prbs set ce0 tx_rx=0 p=5 lane=1 inv=0 if=line  ${BCM_promptstr}
    Step  4  run cmd  epdm prbs set ce1 tx_rx=0 p=5 lane=0 inv=0 if=line  ${BCM_promptstr}
    BuiltIn.Sleep  300
    Step  5  check prbs ports line side
    [Teardown]  exit sdk mode

ABERLOUR_SDK_TC_9.54_Sdk_Reboot_Test
    [Tags]  ABERLOUR_SDK_TC_9.54_Sdk_Reboot_Test
    [Setup]  change dir to sdk path
    Step  1  verify load sdk  -a
    Step  2  send a line  command=exit
    Step  3  remove all related modules
    [Teardown]  exit sdk mode

 

ABERLOUR_SDK_TC_9.79_Stacking_QSFP28_100G_Speed_Change_To_40G_Speed_Test
    [Tags]  ABERLOUR_SDK_TC_9.79_Stacking_QSFP28_100G_Speed_Change_To_40G_Speed_Test
    [Setup]  change dir to sdk path
    Step  1  verify load sdk  -a
    Step  2  change qsfp28 100g speed to 40g speed
    Step  3  check port link status changes to 40G from 100G
    [Teardown]  exit sdk mode

ABERLOUR_SDK_TC_9.71_Stacking_100G_Packet_Counter_Test

    [Tags]  ABERLOUR_SDK_TC_9.71_Stacking_100G_Packet_Counter_Test
    [Setup]  change dir to sdk path
    Step  1  verify load sdk  -a
    Step  2  check 100G stacking packet counter
    Step  3  clear 100G stacking packet counter
    Step  4  check 100G stacking packet counter after clear
    [Teardown]  exit sdk mode

ABERLOUR_SDK_TC_9.76_Uplink_QSFP28_100G_Speed_Change_To_40G_Speed_Test
    [Tags]  ABERLOUR_SDK_TC_9.76_Uplink_QSFP28_100G_Speed_Change_To_40G_Speed_Test
    [Setup]  change dir to sdk path
    Step  1  verify load sdk  -a
    Step  2  change qsfp28 100g speed to 40g speed
    Step  3  check port link status changes to 40G from 100G
    [Teardown]  exit sdk mode

  
ABERLOUR_SDK_TC_9.68_Downlink_10G_Packet_Counter_Test
    [Tags]  ABERLOUR_SDK_TC_9.68_Downlink_10G_Packet_Counter_Test
    [Setup]  change dir to sdk path
    Step  1  verify load sdk  -a
    Step  2  check 10G packet counter
    Step  3  clear 10G packet counter
    Step  4  check 10G packet counter after clear
    [Teardown]  exit sdk mode

ABERLOUR_SDK_TC_9.70_Uplink_100G_Packet_Counter_Test

    [Tags]  ABERLOUR_SDK_TC_9.70_Uplink_100G_Packet_Counter_Test
    [Setup]  change dir to sdk path
    Step  1  verify load sdk  -a
    Step  2  check 100G uplink packet counter
    Step  3  clear 100G uplink packet counter
    Step  4  check 100G uplink packet counter after clear
    [Teardown]  exit sdk mode

ABERLOUR_SDK_TC_9.38_Uplink_Qsfp28_100g_Port_Prbs_Sys_Side_Test
    [Tags]  ABERLOUR_SDK_TC_9.38_Uplink_Qsfp28_100g_Port_Prbs_Sys_Side_Test
    [Setup]  change dir to sdk path
    Step  1  verify load sdk  -a
    Step  2  run cmd  epdm prbs set ce2 tx_rx=0 p=5 lane=all inv=0 if=sys  ${BCM_promptstr}
    Step  3  run cmd  phy diag ce2 prbs set p=3  ${BCM_promptstr}
    Step  4  check uplink prbs ports sys side
    [Teardown]  exit sdk mode

ABERLOUR_SDK_TC_9.39_Uplink_Qsfp28_100g_Port_Prbs_Line_Side_Test
    [Tags]  ABERLOUR_SDK_TC_9.39_Uplink_Qsfp28_100g_Port_Prbs_Line_Side_Test
    [Setup]  change dir to sdk path
    Step  1  verify load sdk  -a
    Step  2  run cmd  epdm prbs set ce2 tx_rx=0 p=5 lane=all inv=0 if=line  ${BCM_promptstr}
    BuiltIn.Sleep  300
    Step  3  check uplink prbs ports line side
    [Teardown]  exit sdk mode

ABERLOUR_SDK_TC_9.33_Downlink_SFP_10G_Port_PRBS_Sys_Side_Test
    [Tags]  ABERLOUR_SDK_TC_9.33_Downlink_SFP_10G_Port_PRBS_Sys_Side_Test
    [Setup]  change dir to sdk path
    Step  1  verify load sdk  -a
    Step  2  start prbs sys generator
    BuiltIn.Sleep  300
    Step  3  check all sys prbs
    [Teardown]  exit sdk mode 


ABERLOUR_SDK_TC_9.34_Downlink_SFP_10G_Port_PRBS_Line_Side_Test
    [Tags]  ABERLOUR_SDK_TC_9.34_Downlink_SFP_10G_Port_PRBS_Line_Side_Test
    [Setup]  change dir to sdk path
    Step  1  verify load sdk  -a
    Step  2  start prbs line generator
    BuiltIn.Sleep  300
    Step  3  check all line prbs
    [Teardown]  exit sdk mode 


ABERLOUR_SDK_TC_9.58_Downlink_10g_Fec_Test_Phy_Side
    [Tags]  ABERLOUR_SDK_TC_9.58_Downlink_10g_Fec_Test_Phy_Side
    [Setup]  change dir to sdk path
    Step  1  verify load sdk  -a
    Step  2  downlink 10g interface enable disable  1  cl74  sys
    Step  3  downlink 10g interface enable disable  0  cl74  sys
    Step  4  downlink 10g interface enable disable  1  cl91  sys
    Step  5  downlink 10g interface enable disable  0  cl91  sys
    Step  6  downlink 10g interface enable disable  1  cl108  sys
    Step  7  downlink 10g interface enable disable  0  cl108  sys
    Step  8  downlink 10g interface enable disable  1  cl74  line
    Step  9  downlink 10g interface enable disable  0  cl74  line
    Step  10  downlink 10g interface enable disable  1  cl91  line
    Step  11  downlink 10g interface enable disable  0  cl91  line
    Step  12  downlink 10g interface enable disable  1  cl108  line
    Step  13  downlink 10g interface enable disable  0  cl108  line
    [Teardown]  exit sdk mode  

ABERLOUR_SDK_TC_9.63_Uplink_100g_Fec_Test_Phy_Side
    [Tags]  ABERLOUR_SDK_TC_9.63_Uplink_100g_Fec_Test_Phy_Side
    [Setup]  change dir to sdk path
    Step  1  verify load sdk  -a
    Step  2  uplink 100g interface enable disable  1  cl74  sys
    Step  3  uplink 100g interface enable disable  0  cl74  sys
    Step  4  uplink 100g interface enable disable  1  cl91  sys
    Step  5  uplink 100g interface enable disable  0  cl91  sys
    Step  6  uplink 100g interface enable disable  1  cl108  sys
    Step  7  uplink 100g interface enable disable  0  cl108  sys
    Step  8  uplink 100g interface enable disable  1  cl74  line
    Step  9  uplink 100g interface enable disable  0  cl74  line
    Step  10  uplink 100g interface enable disable  1  cl91  line
    Step  11  uplink 100g interface enable disable  0  cl91  line
    Step  12  uplink 100g interface enable disable  1  cl108  line
    Step  13  uplink 100g interface enable disable  0  cl108  line
    [Teardown]  exit sdk mode

ABERLOUR_SDK_TC_9.66_Stacking_100g_Fec_Test_Phy_Side
    [Tags]  ABERLOUR_SDK_TC_9.66_Stacking_100g_Fec_Test_Phy_Side
    [Setup]  change dir to sdk path
    Step  1  verify load sdk  -a
    Step  2  stacking 100g interface enable disable  1  cl74  sys
    Step  3  stacking 100g interface enable disable  0  cl74  sys
    Step  4  stacking 100g interface enable disable  1  cl91  sys
    Step  5  stacking 100g interface enable disable  0  cl91  sys
    Step  6  stacking 100g interface enable disable  1  cl108  sys
    Step  7  stacking 100g interface enable disable  0  cl108  sys
    Step  8  stacking 100g interface enable disable  1  cl74  line
    Step  9  stacking 100g interface enable disable  0  cl74  line
    Step  10  stacking 100g interface enable disable  1  cl91  line
    Step  11  stacking 100g interface enable disable  0  cl91  line
    Step  12  stacking 100g interface enable disable  1  cl108  line
    Step  13  stacking 100g interface enable disable  0  cl108  line
    [Teardown]  exit sdk mode

ABERLOUR_SDK_9.25_Uplink_QSFP28_100G_Port_Status_Test
    [Tags]  ABERLOUR_SDK_9.25_Uplink_QSFP28_100G_Port_Status_Test
    [Setup]  change dir to sdk path
    Step  1  verify load sdk  -a
    Step  2  check port link and status
    Step  3  start led status
    Step  4  check uplink 100g port led status
    [Teardown]  exit sdk mode


ABERLOUR_SDK_9.26_Uplink_QSFP28_40G_Port_Status_Test
    [Tags]  ABERLOUR_SDK_9.26_Uplink_QSFP28_40G_Port_Status_Test
    [Setup]  change dir to sdk path
    Step  1  verify load sdk  -a
    Step  2  change qsfp28 100g speed to 40g speed
    Step  3  check port link status changes to 40G from 100G
    Step  4  start led status
    Step  5  check uplink 40g port led status
    [Teardown]  exit sdk mode

ABERLOUR_SDK_9.29_Stacking_QSFP28_100G_Port_Status_Test
    [Tags]  ABERLOUR_SDK_9.29_Stacking_QSFP28_100G_Port_Status_Test
    [Setup]  change dir to sdk path
    Step  1  verify load sdk  -a
    Step  2  check port link and status
    Step  3  start led status
    Step  4  check stacking 100g port led status
    [Teardown]  exit sdk mode

ABERLOUR_SDK_9.30_Stacking_QSFP28_40G_Port_Status_Test
    [Tags]  ABERLOUR_SDK_9.30_Stacking_QSFP28_40G_Port_Status_Test
    [Setup]  change dir to sdk path
    Step  1  verify load sdk  -a
    Step  2  change qsfp28 100g speed to 40g speed
    Step  3  check port link status changes to 40G from 100G
    Step  4  start led status
    Step  5  check stacking 40g port led status
    [Teardown]  exit sdk mode

ABERLOUR_SDK_9.18_Downlink_Sfp_10G_Port_Status_Test
    [Tags]  ABERLOUR_SDK_9.18_Downlink_Sfp_10G_Port_Status_Test
    [Setup]  change dir to sdk path
    Step  1  verify load sdk  -a
    Step  2  check 10g port link and status 
    Step  3  start led status
    Step  4  check downlink 10g port status
    [Teardown]  exit sdk mode

ABERLOUR_SDK_9.19_Downlink_Sfp_10G_Port_Status_Test
    [Tags]  ABERLOUR_SDK_9.19_Downlink_Sfp_10G_Port_Status_Test
    [Setup]  change dir to sdk path
    Step  1  verify load sdk  -a
    Step  2  change port speed to 1g
    Step  3  check 1g port link and status
    Step  4  start led status
    Step  5  check downlink 1g port status
    [Teardown]  exit sdk mode

ABERLOUR_SDK_9.57_Downlink_10G_FEC_Mac_Side_Test
    [Tags]  ABERLOUR_SDK_9.57_Downlink_10G_FEC_Mac_Side_Test
    [Setup]  change dir to sdk path
    Step  1  verify load sdk  -a
    Step  2  check downlink 10G port MAC side FEC and check port status
    Step  3  enable downlink 10G port MAC side FEC and check port status 
    Step  4  disable downlink 10G port MAC side FEC and check port status
    [Teardown]  exit sdk mode

ABERLOUR_SDK_9.62_Uplink_100G_FEC_Mac_Side_Test
    [Tags]  ABERLOUR_SDK_9.62_Uplink_100G_FEC_Mac_Side_Test
    [Setup]  change dir to sdk path
    Step  1  verify load sdk  -a
    Step  2  check uplink 100G port MAC side FEC status and check port status
    Step  3  enable uplink 100G port MAC side FEC and check port status
    Step  4  disable uplink 100G port MAC side FEC and check port status
    [Teardown]  exit sdk mode

ABERLOUR_SDK_9.65_Stacking_100G_FEC_Mac_Side_Test
    [Tags]  ABERLOUR_SDK_9.65_Stacking_100G_FEC_Mac_Side_Test
    [Setup]  change dir to sdk path
    Step  1  verify load sdk  -a
    Step  2  check stacking 100G port MAC side FEC status and check port status
    Step  3  enable stacking 100G port MAC side FEC and check port status
    Step  4  disable stacking 100G port MAC side FEC and check port status
    [Teardown]  exit sdk mode

ABERLOUR_SDK_9.82_All_port_maximum_and_minimum_speed_set_Test
    [Tags]  ABERLOUR_SDK_9.82_All_port_maximum_and_minimum_speed_set_Test
    [Setup]  change dir to sdk path
    Step  1  verify load sdk  -a
    Step  2  change all port speed to minimum
    Step  3  check ps and epdm port link status and speed
    Step  4  change all port speed to maximum
    Step  5  check ps and epdm port link status and speed
    [Teardown]  exit sdk mode

ABERLOUR_SDK_9.83_EEPROM_verification_for_stacking_ports_Test
    [Tags]  ABERLOUR_SDK_9.83_EEPROM_verification_for_stacking_ports_Test
    [Setup]  change dir to sdk path
    Step  1  verify eeprom 
    [Teardown]  exit localhost mode

ABERLOUR_SDK_9.55_Sdk_Remote_Shell_Test
    [Tags]  ABERLOUR_SDK_9.55_Sdk_Remote_Shell_Test
    [Setup]  change dir to sdk path
    Step  1  verify detached load sdk
    Step  2  check port status by remote shell command
    Step  3  remote shell command to exit sdk and check bcm process
    [Teardown]  exit remote shell mode

ABERLOUR_SDK_9.51_Serdes_FW_Test
    [Tags]  ABERLOUR_SDK_9.51_Serdes_FW_Test
    [Setup]  change dir to sdk path
    Step  1  verify load sdk  -a
    Step  2  check downlink port link serde version
    Step  3  check uplink port link serde version
    Step  4  check each port serde version phy side
    [Teardown]  exit sdk mode

ABERLOUR_SDK_9.80_MACsec_Test
    [Tags]  ABERLOUR_SDK_9.80_MACsec_Test
    [Setup]  change dir to sdk path
    Step  1  verify load sdk  -a
    Step  2  enable macsec function
    Step  3  check macsec enable counters
    Step  4  send snake traffic and check macsec counters
    Step  5  disable macsec and check macsec counters
    [Teardown]  exit sdk mode

ABERLOUR_SDK_10.4_Port_Loopback_Traffic_Test_24x10G+1x100G+2x100G
    [Tags]  ABERLOUR_SDK_10.4_Port_Loopback_Traffic_Test_24x10G+1x100G+2x100G
    [Setup]  change dir to sdk path
    Step  1  verify load sdk  -a
    Step  2  run command to test 24h traffic
    Step  3  check port counter and system status
    [Teardown]  exit sdk mode

ABERLOUR_SDK_11.2_All_Ports_Enable_Disable_Stress_Test
    [Tags]  ABERLOUR_SDK_11.2_All_Ports_Enable_Disable_Stress_Test
    [Setup]  change dir to sdk path
    Step  1  all_port_enable_disable_stress_test
    [Teardown]  exit sdk mode

ABERLOUR_SDK_11.1_SDK_Re_Init_Stress_Test
    [Tags]  ABERLOUR_SDK_11.1_SDK_Re_Init_Stress_Test
    [Setup]  change dir to sdk path
    Step  1  sdk_re_init_stress_test
    [Teardown]  exit sdk mode



*** Keywords ***
DiagOS Connect Device
    DiagOSConnect

DiagOS Disconnect Device
    DiagOSDisconnect


