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

Library           JuniperSdkLib.py
Library           JuniperCommonLib.py
Library           SdkCommonLib.py
Library           CommonLib.py
Variables         JuniperCommonVariable.py
Variables         JuniperSdkVariable.py

Resource          JuniperSdkKeywords.resource

Suite Setup       Connect Device
Suite Teardown    Disconnect Device

*** Variables ***
${LoopCnt}      1
${MAX_LOOP}     3

*** Test Cases ***

TYRCONNELL_SDK_TC_9.1_Load_and_Initialization_SDK_Test
    [Tags]  TYRCONNELL_SDK_TC_9.1_Load_and_Initialization_SDK_Test  tyrconnell
    [Timeout]  5 min 00 seconds
    [Setup]  change dir to sdk path
    Step  1  verify load SDK  -a
    [Teardown]  exit sdk mode

TYRCONNELL_SDK_TC_9.2_Default_Port_Info_Test
    [Tags]     TYRCONNELL_SDK_TC_9.2_Default_Port_Info_Test  tyrconnell
    [Timeout]  5 min 00 seconds
    [Setup]    change dir to sdk path
    Step  1  verify load SDK  -a
    Step  2  check port status
    Step  3  check epdm link status
    [Teardown]  exit sdk mode

TYRCONNELL_SDK_TC_9.3_PHY_Info_Test
    [Tags]     TYRCONNELL_SDK_TC_9.3_PHY_Info_Test  tyrconnell
    [Timeout]  5 min 00 seconds
    [Setup]    change dir to sdk path
    Step  1  verify load SDK  -a
    Step  2  check phy info
    [Teardown]  exit sdk mode

TYRCONNELL_SDK_TC_9.4_MDIO_advisor_Test
    [Tags]     TYRCONNELL_SDK_TC_9.4_MDIO_advisor_Test  lagavulin
    [Timeout]  5 min 00 seconds
    [Setup]    change dir to sdk path
    Step  1  verify load SDK  -a
    Step  2  check mdio advisor
    [Teardown]  exit sdk mode

TYRCONNELL_SDK_TC_9.9_Uplink_QSFP28_100G_Port_PRBS_Test_Sys_side
    [Tags]     TYRCONNELL_SDK_TC_9.9_Uplink_QSFP28_100G_Port_PRBS_Test_Sys_side  tyrconnell
    [Timeout]  5 min 00 seconds
    [Setup]    change dir to sdk path
    Step  1  verify load SDK  -a
    Step  2  run cmd  epdm prbs set ce0 tx_rx=0 p=5 lane=all inv=0 if=sys  ${BCM_promptstr}
    Step  3  run cmd  phy diag ce0 prbs set p=3  ${BCM_promptstr}
    BuiltIn.Sleep  1
    Step  4  check uplink prbs sys side
    Step  5  run cmd  phy diag ce0 prbs clear  ${BCM_promptstr}
    [Teardown]  exit sdk mode

TYRCONNELL_SDK_TC_9.10_Uplink_QSFP28_100G_Port_PRBS_Test_Line_side
    [Tags]     TYRCONNELL_SDK_TC_9.10_Uplink_QSFP28_100G_Port_PRBS_Test_Line_side  tyrconnell
    [Timeout]  5 min 00 seconds
    [Setup]    change dir to sdk path
    Step  1  verify load SDK  -a
    Step  2  run cmd  epdm prbs set ce0 tx_rx=0 p=5 lane=all inv=0 if=line  ${BCM_promptstr}
    BuiltIn.Sleep  300
    Step  3  check uplink prbs line side
    Step  4  run cmd  phy diag ce0 prbs clear  ${BCM_promptstr}
    [Teardown]  exit sdk mode

TYRCONNELL_SDK_TC_9.11_BCM82399_PHY_PRBS_Test
    [Tags]     TYRCONNELL_SDK_TC_9.11_BCM82399_PHY_PRBS_Test  tyrconnell
    [Timeout]  10 min 00 seconds
    [Setup]    change dir to sdk path
    Step  1  phy prbs test
    [Teardown]  exit sdk mode

TYRCONNELL_SDK_TC_9.30_All_port_maximum_and_minimum_speed_set_Test
   [Tags]    TYRCONNELL_SDK_TC_9.30_All_port_maximum_and_minimum_speed_set_Test  tryconnell
   [Timeout]  5 min 00 seconds
   [Setup]    change dir to sdk path
   Step  1  verify load SDK  -a
   Step  2  Change all port speed to  minimum
   step  3  Check port link status and link speed  minimum
   step  4  Change all port speed to  maximum
   step  5  Check port link status and link speed  maximum
   [Teardown]  exit sdk mode

*** Keywords ***
Connect Device
    Login Device

Disconnect Device
    Sdk Disconnect
