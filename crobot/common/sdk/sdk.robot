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
# Script       : Wedge400C_diag.robot                                                                                 #
# Date         : April 14, 2020                                                                                       #
# Author       : Prapatsorn W.                                                                                        #
# Description  : This script will validate SDK package for Wedge400C                                                  #
#                                                                                                                   #
# Script Revision Details:                                                                                            #
#
######################################################################################################################

*** Settings ***
Documentation       This Suite will validate SDK package

Force Tags        SDK
Resource          Resource.robot
Library           SdkLibAdapter.py

Suite Setup       Connect Device
Suite Teardown    Disconnect Device


*** Test Cases ***
FB_SDK_CS_COM_TC_001_Load and Initialization SDK Test
    [Documentation]  This test checks SDK initialization
    [Tags]     common  wedge400c  FB_SDK_CS_COM_TC_001_Load_and_Initialization_SDK_Test
    [Timeout]  15 min 00 seconds
    [Setup]    change dir to sdk path
    Step  1  Check SDK initialization  dd_8x50g_qsfp_4x50g
    Step  2  Check SDK initialization  dd_8x50g_qsfp_4x25g
    Step  3  Check SDK initialization  dd_4x50g_qsfp_4x25g
    Step  4  Check SDK initialization  dd_4x25g_qsfp_4x25g
    Step  5  Check SDK initialization  dd_4x25g_qsfp_2x2x25g
    [Teardown]  go to centos

FB_SDK_CS_COM_TC_002_Version Test
    [Documentation]  This test checks SDK version and release version
    [Tags]     common  wedge400c  FB_SDK_CS_COM_TC_002_Version_Test
    [Timeout]  5 min 00 seconds
    [Setup]    change dir to sdk path
    Step  1  check sdk version
    [Teardown]  go to centos

FB_SDK_CS_COM_TC_003_Default Port Info Test
    [Documentation]  This test checks port default info with each speed.
    [Tags]     common  wedge400c  FB_SDK_CS_COM_TC_003_Default_Port_Info_Test
    [Timeout]  25 min 00 seconds
    [Setup]    change dir to sdk path
    Step  1  port default info test  dd_8x50g_qsfp_4x50g
    Step  2  port default info test  dd_8x50g_qsfp_4x25g
    Step  3  port default info test  dd_4x50g_qsfp_4x25g
    Step  4  port default info test  dd_4x25g_qsfp_4x25g
    Step  5  port default info test  dd_4x25g_qsfp_2x2x25g
    [Teardown]  go to centos

FB_SDK_CS_COM_TC_004_QSFPDD 1x400G Port Linkup Test
    [Documentation]  This test checks QSFPDD(400G) port linkup
    [Tags]  FB_SDK_CS_COM_TC_004_QSFPDD_1x400G_Port_Linkup_Test  common  wedge400c
    [Timeout]  9 min 00 seconds
    [Setup]    change dir to sdk path
    Step  1  run port linkup test  dd_8x50g_qsfp_4x50g
    Step  2  go to centos
    Step  3  run port linkup test  dd_8x50g_qsfp_4x25g
    [Teardown]  go to centos

FB_SDK_CS_COM_TC_005_QSFPDD 1x200G Port Linkup Test
    [Documentation]  This test checks QSFPDD(200G) port linkup
    [Tags]  FB_SDK_CS_COM_TC_005_QSFPDD_1x200G_Port_Linkup_Test  common  wedge400c
    [Timeout]  5 min 00 seconds
    [Setup]    change dir to sdk path
    Step  1  run port linkup test  dd_4x50g_qsfp_4x25g
    [Teardown]  go to centos

FB_SDK_CS_COM_TC_006_QSFPDD_1x100G_Port_Linkup_Test
    [Documentation]  This test checks QSFPDD(100G) port linkup
    [Tags]  FB_SDK_CS_COM_TC_006_QSFPDD_1x100G_Port_Linkup_Test   common  wedge400c
    [Timeout]  9 min 00 seconds
    [Setup]    change dir to sdk path
    Step  1  run port linkup test  dd_4x25g_qsfp_4x25g
    Step  2  go to centos
    Step  3  run port linkup test  dd_4x25g_qsfp_2x2x25g
    [Teardown]  go to centos

FB_SDK_CS_COM_TC_007_QSFPDD_1x400G_Port_BER_Test
    [Documentation]  This test checks QSFPDD(400G) QSFP56(200G) BER
    [Tags]  FB_SDK_CS_COM_TC_007_QSFPDD_1x400G_Port_BER_Test  common  wedge400c
    [Timeout]  85 min 00 seconds
    [Setup]    change dir to sdk path
    Step  1  run mac port ber test  dd_8x50g_qsfp_4x50g
    Step  2  go to centos
    Step  3  check mac port ber status  dd_8x50g_qsfp_4x50g
    Step  4  run mac port ber test  dd_8x50g_qsfp_4x25g
    Step  5  go to centos
    Step  6  check mac port ber status  dd_8x50g_qsfp_4x25g
    [Teardown]  go to centos

FB_SDK_CS_COM_TC_008_QSFPDD_1x200G_Port_BER_Test
    [Documentation]  This test checks QSFPDD(200G) QSFP56(100G) BER
    [Tags]  FB_SDK_CS_COM_TC_008_QSFPDD_1x200G_Port_BER_Test  common  wedge400c
    [Timeout]  45 min 00 seconds
    [Setup]    change dir to sdk path
    Step  1  run mac port ber test  dd_4x50g_qsfp_4x25g
    Step  2  go to centos
    Step  3  check mac port ber status  dd_4x50g_qsfp_4x25g
    [Teardown]  go to centos

FB_SDK_CS_COM_TC_009_QSFPDD_1x100G_Port_BER_Test
    [Documentation]  This test checks QSFPDD(100G) QSFP56(100G) BER
    [Tags]  FB_SDK_CS_COM_TC_009_QSFPDD_1x100G_Port_BER_Test   common  wedge400c
    [Timeout]  95 min 00 seconds
    [Setup]    change dir to sdk path
    Step  1  run mac port ber test  dd_4x25g_qsfp_4x25g
    Step  2  go to centos
    Step  3  check mac port ber status  dd_4x25g_qsfp_4x25g
    Step  4  run mac port ber test  dd_4x25g_qsfp_2x2x25g
    Step  5  go to centos
    Step  6  check mac port ber status  dd_4x25g_qsfp_2x2x25g
    [Teardown]  go to centos

FB_SDK_CS_COM_TC_010_QSFPDD_1x400G_Port_Loopback_Test
    [Documentation]  This test makes sure that after each flap event link is able to latch on to correct signal.
    [Tags]  FB_SDK_CS_COM_TC_010_QSFPDD_1x400G_Port_Loopback_Test   common  wedge400c
    [Timeout]  20 min 00 seconds
    [Setup]    change dir to sdk path
    Step  1  check loopback test  dd_8x50g_qsfp_4x50g  none
    Step  2  check loopback test  dd_8x50g_qsfp_4x50g  pma
    Step  3  check loopback test  dd_8x50g_qsfp_4x50g  pma_serdes
    Step  4  check loopback test  dd_8x50g_qsfp_4x25g  none
    Step  5  check loopback test  dd_8x50g_qsfp_4x25g  pma
    Step  6  check loopback test  dd_8x50g_qsfp_4x25g  pma_serdes
    [Teardown]  go to centos

FB_SDK_CS_COM_TC_011_QSFPDD_1x200G_Port_Loopback_Test
    [Documentation]  This test makes sure that after each flap event link is able to latch on to correct signal.
    [Tags]  FB_SDK_CS_COM_TC_011_QSFPDD_1x200G_Port_Loopback_Test   common  wedge400c
    [Timeout]  10 min 00 seconds
    [Setup]    change dir to sdk path
    Step  1  check loopback test  dd_4x50g_qsfp_4x25g  none
    Step  2  check loopback test  dd_4x50g_qsfp_4x25g  pma
    Step  3  check loopback test  dd_4x50g_qsfp_4x25g  pma_serdes
    [Teardown]  go to centos

FB_SDK_CS_COM_TC_012_QSFPDD_1x100G_Port_Loopback_Test
    [Documentation]  This test makes sure that after each flap event link is able to latch on to correct signal.
    [Tags]  FB_SDK_CS_COM_TC_012_QSFPDD_1x100G_Port_Loopback_Test  common  wedge400c
    [Timeout]  20 min 00 seconds
    [Setup]    change dir to sdk path
    Step  1  check loopback test  dd_4x25g_qsfp_4x25g  none
    Step  2  check loopback test  dd_4x25g_qsfp_4x25g  pma
    Step  3  check loopback test  dd_4x25g_qsfp_4x25g  pma_serdes
    [Teardown]  go to centos

FB_SDK_CS_COM_TC_013_QSFPDD_1x400G_L2_CPU_Traffic_Test
    [Documentation]  This test checks QSFPDD(400G) can forward L2 snake traffic with CPU.
    [Tags]  FB_SDK_CS_COM_TC_013_QSFPDD_1x400G_L2_CPU_Traffic_Test  common  wedge400c
    [Timeout]  30 min 00 seconds
    [Setup]    change dir to sdk path
    Step  1  test L2 traffic  dd_8x50g_qsfp_4x50g
    Step  2  test L2 traffic  dd_8x50g_qsfp_4x25g
    [Teardown]  go to centos

FB_SDK_CS_COM_TC_014_QSFPDD_1x200G_L2_CPU_Traffic_Test
    [Documentation]  This test checks QSFPDD(200G) can forward L2 snake traffic with CPU.
    [Tags]  FB_SDK_CS_COM_TC_014_QSFPDD_1x200G_L2_CPU_Traffic_Test  common  wedge400c
    [Timeout]  20 min 00 seconds
    [Setup]    change dir to sdk path
    Step  1  test L2 traffic  dd_4x50g_qsfp_4x25g
    [Teardown]  go to centos

FB_SDK_CS_COM_TC_015_QSFPDD_1x100G_L2_CPU_Traffic_Test
    [Documentation]  This test checks QSFPDD(100G) can forward L2 snake traffic with CPU.
    [Tags]  FB_SDK_CS_COM_TC_015_QSFPDD_1x100G_L2_CPU_Traffic_Test  common  wedge400c
    [Timeout]  30 min 00 seconds
    [Setup]    change dir to sdk path
    Step  1  test L2 traffic  dd_4x25g_qsfp_4x25g
    Step  2  test L2 traffic  dd_4x25g_qsfp_2x2x25g
    [Teardown]  go to centos

FB_SDK_CS_COM_TC_016_QSFPDD_1x400G_L3_CPU_Traffic_Test
    [Documentation]  This test checks QSFPDD(400G) can forward L3 snake traffic with CPU.
    [Tags]  FB_SDK_CS_COM_TC_016_QSFPDD_1x400G_L3_CPU_Traffic_Test  common  wedge400c
    [Timeout]  30 min 00 seconds
    [Setup]    change dir to sdk path
    Step  1  test L3 traffic  dd_8x50g_qsfp_4x50g
    Step  2  test L3 traffic  dd_8x50g_qsfp_4x25g
    [Teardown]  go to centos

FB_SDK_CS_COM_TC_017_QSFPDD_1x200G_L3_CPU_Traffic_Test
    [Documentation]  This test checks QSFPDD(200G) can forward L3 snake traffic with CPU.
    [Tags]  FB_SDK_CS_COM_TC_017_QSFPDD_1x200G_L3_CPU_Traffic_Test  common  wedge400c
    [Timeout]  20 min 00 seconds
    [Setup]    change dir to sdk path
    Step  1  test L3 traffic  dd_4x50g_qsfp_4x25g
    [Teardown]  go to centos

FB_SDK_CS_COM_TC_018_QSFPDD_1x100G_L3_CPU_Traffic_Test
    [Documentation]  This test checks QSFPDD(100G) can forward L3 snake traffic with CPU.
    [Tags]  FB_SDK_CS_COM_TC_018_QSFPDD_1x100G_L3_CPU_Traffic_Test  common  wedge400c
    [Timeout]  30 min 00 seconds
    [Setup]    change dir to sdk path
    Step  1  test L3 traffic  dd_4x25g_qsfp_4x25g
    Step  2  test L3 traffic  dd_4x25g_qsfp_2x2x25g
    [Teardown]  go to centos

FB_SDK_CS_COM_TC_019_Temperature_and_Voltage_Test
    [Documentation]  This test checks switch temperature and voltage with DUT.
    [Tags]  FB_SDK_CS_COM_TC_019_Temperature_and_Voltage_Test  common  wedge400c
    [Timeout]  5 min 00 seconds
    [Setup]    change dir to sdk path
    Step  1  check temperature
    [Teardown]  go to centos

#FB_SDK_CS_COM_TC_020_Memory_BIST_Test
#    [Documentation]  This test checks switch Memory BIST.
#    [Tags]  FB_SDK_CS_COM_TC_020_Memory_BIST_Test  common  wedge400c
#    [Timeout]  5 min 00 seconds
#    [Setup]    change dir to sdk path
#    Step  1  check Memory BIST
#    [Teardown]  go to centos

FB_SDK_CS_COM_TC_021_Manufacturing_Test
    [Documentation]  This test checks Manufacture overall check
    [Tags]  FB_SDK_CS_COM_TC_021_Manufacturing_Test  common  wedge400c
    [Timeout]  50 min 00 seconds
    [Setup]    change dir to sdk path
    Step  1  test manufacture
    [Teardown]  go to centos

FB_SDK_CS_COM_TC_030_SDK_Re_Init_Test
    [Documentation]  This test checks Manufacture overall check
    [Tags]  FB_SDK_CS_COM_TC_030_SDK_Re_Init_Test  common  wedge400c
    [Timeout]  35 min 00 seconds
    [Setup]    change dir to sdk path
    Step  1  reinit test
    step  2  go to centos
    step  3  check reinit port status
    [Teardown]  go to centos

FB_SDK_CS_COM_TC_031_Each Port Disable_Enable Test
    [Documentation]  This test checks Manufacture overall check
    [Tags]  FB_SDK_CS_COM_TC_031_Each_Port_Disable_Enable_Test  common  wedge400c
    [Timeout]  15 min 00 seconds
    [Setup]    change dir to sdk path
    Step  1  run port enable disable
    step  2  go to centos
    step  3  check port enable disable status
    [Teardown]  go to centos

*** Keywords ***
Connect Device
    Set Library Order
    Sdk Device Connect
    Init Test Library
    ssh login bmc


Disconnect Device
    ssh disconnect
    Sdk Device Disconnect

