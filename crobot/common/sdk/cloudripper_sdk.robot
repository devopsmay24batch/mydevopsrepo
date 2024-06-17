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
# Script       : Cloudripper_sdk.robot                                                                                 #
# Date         : Sept. 1st, 2020                                                                                       #
# Author       : Yang, Xuecun <yxcun@celestica.com>                                                                    #
# Description  : This script will validate SDK package for Cloudripper                                                 #
#                                                                                                                      #
# Script Revision Details:                                                                                             #
#                                                                                                                      #
######################################################################################################################

*** Settings ***
Documentation       This Suite will validate SDK package

Force Tags        SDK
Resource          Resource.robot
Library           SdkLibAdapter.py
Variables         Sdk_variable.py

Suite Setup       Connect Device
Suite Teardown    Disconnect Device


*** Test Cases ***
FB_SDK_CS_COM_TC_001_Load and Initialization SDK Test
    [Documentation]  This test checks SDK initialization
    [Tags]  FB_SDK_CS_COM_TC_001_Load_and_Initialization_SDK_Test  common  cloudripper
    [Timeout]  200 min 00 seconds
    [Setup]    change dir to sdk path
    Step  1  verify load user  ${init_load_user_cmd} 32x1x8x50g
    Step  2  exit mode
    Step  3  verify load user  ${init_load_user_cmd} 32x1x4x25g
    [Teardown]  exit mode


FB_SDK_CS_COM_TC_002_Version Test
    [Documentation]  This test checks SDK version and release version
    [Tags]  FB_SDK_CS_COM_TC_002_Version_Test  common  cloudripper
    [Timeout]  2 min 00 seconds
    [Setup]    change dir to sdk path
    Step  1  check sdk version

FB_SDK_CS_COM_TC_003_Default Port Info Test
    [Documentation]  This test checks port default info with each speed.
    [Tags]  FB_SDK_CS_COM_TC_003_Default_Port_Info_Test  common  cloudripper
    [Timeout]  200 min 00 seconds
    [Setup]    change dir to sdk path
    Step  1  port default info test  32x1x8x50g
    Step  2  port default info test  32x1x4x50g
    [Teardown]  exit mode

FB_SDK_CS_COM_TC_004_QSFPDD 1x400G Port Linkup Test
    [Documentation]  This test checks QSFPDD(400G) port linkup
    [Tags]  FB_SDK_CS_COM_TC_004_QSFPDD_1x400G_Port_Linkup_Test  common  cloudripper
    [Timeout]  90 min 00 seconds
    [Setup]    change dir to sdk path
    Step  1  run port linkup test  32x1x8x50g
    [Teardown]  go to centos

FB_SDK_CS_COM_TC_005_QSFPDD 1x200G Port Linkup Test
    [Documentation]  This test checks QSFPDD(200G) port linkup
    [Tags]  FB_SDK_CS_COM_TC_005_QSFPDD_1x200G_Port_Linkup_Test  common  cloudripper
    [Timeout]  90 min 00 seconds
    [Setup]    change dir to sdk path
    Step  1  run port linkup test  32x1x4x50g
    [Teardown]  go to centos

FB_SDK_CS_COM_TC_007_QSFPDD_1x400G_Port_BER_Test
    [Documentation]  This test checks QSFPDD(400G) QSFP56(200G) BER
    [Tags]  FB_SDK_CS_COM_TC_007_QSFPDD_1x400G_Port_BER_Test  common  cloudripper
    [Timeout]  85 min 00 seconds
    [Setup]    change dir to sdk path
    Step  1  run mac port ber test  32x1x8x50g
    [Teardown]  go to centos

FB_SDK_CS_COM_TC_008_QSFPDD_1x200G_Port_BER_Test
    [Documentation]  This test checks QSFPDD(200G) QSFP56(100G) BER
    [Tags]  FB_SDK_CS_COM_TC_008_QSFPDD_1x200G_Port_BER_Test  common  cloudripper
    [Timeout]  45 min 00 seconds
    [Setup]    change dir to sdk path
    Step  1  run mac port ber test  32x1x4x50g
    [Teardown]  go to centos

FB_SDK_CS_COM_TC_010_QSFPDD_1x400G_Port_Loopback_Test
    [Documentation]  This test makes sure that after each flap event link is able to latch on to correct signal.
    [Tags]  FB_SDK_CS_COM_TC_010_QSFPDD_1x400G_Port_Loopback_Test  common  cloudripper
    [Timeout]  70 min 00 seconds
    [Setup]    change dir to sdk path
    Step  1  verify loopback test  32x1x8x50g  none
    Step  2  verify loopback test  32x1x8x50g  pma
    Step  3  verify loopback test  32x1x8x50g  pma_serdes
    [Teardown]  exit mode

FB_SDK_CS_COM_TC_011_QSFPDD_1x200G_Port_Loopback_Test
    [Documentation]  This test makes sure that after each flap event link is able to latch on to correct signal.
    [Tags]  FB_SDK_CS_COM_TC_011_QSFPDD_1x200G_Port_Loopback_Test  common  cloudripper
    [Timeout]  200 min 00 seconds
    [Setup]    change dir to sdk path
    Step  1  verify load user  ${loopback_cmd} -o none -p 32x1x4x50g  ${loopback_pattern}  port_sum_pattern=None
    Step  2  exit mode
    Step  3  verify load user  ${loopback_cmd} -o pma -p 32x1x4x50g  ${loopback_pattern}  port_sum_pattern=None
    Step  4  exit mode
    Step  5  verify load user  ${loopback_cmd} -o pma_serdes -p 32x1x4x50g  ${loopback_pattern}  port_sum_pattern=None
    [Teardown]  exit mode

FB_SDK_CS_COM_TC_013_QSFPDD_1x400G_L2_CPU_Traffic_Test
    [Documentation]  This test checks QSFPDD(400G) can forward L2 snake traffic with CPU.
    [Tags]  FB_SDK_CS_COM_TC_013_QSFPDD_1x400G_L2_CPU_Traffic_Test  common  cloudripper
    [Timeout]  55 min 00 seconds
    [Setup]    change dir to sdk path
    Step  1  verify load user  ${l2_cpu_cmd} 32x1x8x50g  ${l2_cpu_pattern}  port_sum_pattern=None  timeout=2700
    Step  2  check same port
    [Teardown]  exit mode

FB_SDK_CS_COM_TC_014_QSFPDD_1x200G_L2_CPU_Traffic_Test
    [Documentation]  This test checks QSFPDD(200G) can forward L2 snake traffic with CPU.
    [Tags]  FB_SDK_CS_COM_TC_014_QSFPDD_1x200G_L2_CPU_Traffic_Test  common  cloudripper
    [Timeout]  50 min 00 seconds
    [Setup]    change dir to sdk path
    Step  1  verify load user  ${l2_cpu_cmd} 32x1x4x50g  ${l2_cpu_pattern}  port_sum_pattern=None
    Step  2  check same port
    [Teardown]  exit mode

FB_SDK_CS_COM_TC_016_QSFPDD_1x400G_L3_CPU_Traffic_Test
    [Documentation]  This test checks QSFPDD(400G) can forward L3 snake traffic with CPU.
    [Tags]  FB_SDK_CS_COM_TC_016_QSFPDD_1x400G_L3_CPU_Traffic_Test  common  cloudripper
    [Timeout]  50 min 00 seconds
    [Setup]    change dir to sdk path
    Step  1  verify load user  ${l3_cpu_cmd} 32x1x8x50g  ${l3_cpu_pattern}  port_sum_pattern=None
    Step  2  check same port
    [Teardown]  exit mode

FB_SDK_CS_COM_TC_017_QSFPDD_1x200G_L3_CPU_Traffic_Test
    [Documentation]  This test checks QSFPDD(200G) can forward L3 snake traffic with CPU.
    [Tags]  FB_SDK_CS_COM_TC_017_QSFPDD_1x200G_L3_CPU_Traffic_Test  common  cloudripper
    [Timeout]  50 min 00 seconds
    [Setup]    change dir to sdk path
    Step  1  verify load user  ${l3_cpu_cmd} 32x1x4x50g  ${l3_cpu_pattern}  port_sum_pattern=None
    Step  2  check same port
    [Teardown]  exit mode

FB_SDK_CS_COM_TC_006_QSFPDD_1x100G_Port_Linkup_Test
    [Documentation]  This test checks QSFPDD(100G) port linkup
    [Tags]  FB_SDK_CS_COM_TC_006_QSFPDD_1x100G_Port_Linkup_Test   common  cloudripper
    [Timeout]  90 min 00 seconds
    [Setup]    change dir to sdk path
    Step  1  run port linkup test  32x1x4x25g
    [Teardown]  go to centos

FB_SDK_CS_COM_TC_009_QSFPDD_1x100G_Port_BER_Test
    [Documentation]  This test checks QSFPDD(100G) QSFP56(100G) BER
    [Tags]  FB_SDK_CS_COM_TC_009_QSFPDD_1x100G_Port_BER_Test   common  cloudripper
    [Timeout]  95 min 00 seconds
    [Setup]    change dir to sdk path
    Step  1  run mac port ber test  32x1x4x25g
    [Teardown]  go to centos

FB_SDK_CS_COM_TC_012_QSFPDD_1x100G_Port_Loopback_Test
    [Documentation]  This test makes sure that after each flap event link is able to latch on to correct signal.
    [Tags]  FB_SDK_CS_COM_TC_012_QSFPDD_1x100G_Port_Loopback_Test   common  cloudripper
    [Timeout]  200 min 00 seconds
    [Setup]    change dir to sdk path
    Step  1  verify load user  ${loopback_cmd} -o none -p 32x1x4x25g  ${loopback_pattern}  port_sum_pattern=None
    Step  2  exit mode
    Step  3  verify load user  ${loopback_cmd} -o pma -p 32x1x4x25g  ${loopback_pattern}  port_sum_pattern=None
    Step  4  exit mode
    Step  5  verify load user  ${loopback_cmd} -o pma_serdes -p 32x1x4x25g  ${loopback_pattern}  port_sum_pattern=None
    [Teardown]  exit mode

FB_SDK_CS_COM_TC_015_QSFPDD_1x100G_L2_CPU_Traffic_Test
    [Documentation]  This test checks QSFPDD(100G) can forward L2 snake traffic with CPU.
    [Tags]  FB_SDK_CS_COM_TC_015_QSFPDD_1x100G_L2_CPU_Traffic_Test  common  cloudripper
    [Timeout]  50 min 00 seconds
    [Setup]    change dir to sdk path
    Step  1  verify load user  ${l2_cpu_cmd} 32x1x4x25g  ${l2_cpu_pattern}  port_sum_pattern=None
    Step  2  check same port
    [Teardown]  exit mode

FB_SDK_CS_COM_TC_018_QSFPDD_1x100G_L3_CPU_Traffic_Test
    [Documentation]  This test checks QSFPDD(100G) can forward L3 snake traffic with CPU.
    [Tags]  FB_SDK_CS_COM_TC_018_QSFPDD_1x100G_L3_CPU_Traffic_Test  common  cloudripper
    [Timeout]  50 min 00 seconds
    [Setup]    change dir to sdk path
    Step  1  verify load user  ${l3_cpu_cmd} 32x1x4x25g  ${l3_cpu_pattern}  port_sum_pattern=None
    Step  2  check same port
    [Teardown]  exit mode

FB_SDK_CS_COM_TC_019_Temperature_and_Voltage_Test
    [Documentation]  This test checks switch temperature and voltage with DUT.
    [Tags]  FB_SDK_CS_COM_TC_019_Temperature_and_Voltage_Test  common  cloudripper
    [Timeout]  50 min 00 seconds
    [Setup]    change dir to sdk path
    Step  1  check temperature

FB_SDK_CS_COM_TC_020_Memory_BIST_Test
    [Documentation]  This test checks switch Memory BIST.
    [Tags]  FB_SDK_CS_COM_TC_020_Memory_BIST_Test  common  cloudripper
    [Timeout]  5 min 00 seconds
    [Setup]    change dir to sdk path
    Step  1  check Memory BIST

FB_SDK_CS_COM_TC_021_Manufacturing_Test
    [Documentation]  This test checks Manufacture overall check
    [Tags]  FB_SDK_CS_COM_TC_021_Manufacturing_Test  common  cloudripper
    [Timeout]  55 min 00 seconds
    [Setup]    change dir to sdk path
    Step  1  verify load user  ${manufacturing_cmd}  ${manufacturing_pattern}  port_sum_pattern=None  timeout=2700
    [Teardown]  exit mode
#    [Teardown]  ssh disconnect

FB_SDK_CS_COM_TC_030_SDK_Re_Init_Test
    [Documentation]  This test checks loop 10 times SDK initialization test.
    [Tags]  FB_SDK_CS_COM_TC_030_SDK_Re_Init_Test  common  cloudripper
    [Timeout]  50 min 00 seconds
    [Setup]    change dir to sdk path
    Step  1  verify load user  ${re_init_cmd}  ${re_init_pattern}  port_sum_pattern=None  timeout=2400
    [Teardown]  exit mode

FB_SDK_CS_SP_TC_007_L2_CPU_Snake_Traffic_Test_With_MACSec
    [Documentation]  This test checks system status with L2 cpu snake traffic.
    [Tags]  FB_SDK_CS_SP_TC_007_L2_CPU_Snake_MACSec  cloudripper
    [Timeout]  60 min 00 seconds
    [Setup]    change dir to sdk path
    Step  1  verify load user  ${l2_cpu_snake_traffic_cmd}  ${l2_cpu_pattern}  port_sum_pattern=None  timeout=2400
    [Teardown]  exit mode

FB_SDK_CS_SP_TC_008_L2_CPU_Snake_Traffic_Test_With_MACSec_32x200G
    [Documentation]  This test checks system status with L2 cpu snake traffic 32x200G.
    [Tags]  FB_SDK_CS_SP_TC_008_L2_CPU_Snake_MACSec_200G  cloudripper
    [Timeout]  60 min 00 seconds
    [Setup]    change dir to sdk path
    Step  1  verify load user  ${l2_cpu_snake_traffic_cmd_200G}  ${l2_cpu_pattern}  port_sum_pattern=None  timeout=2400
    [Teardown]  exit mode

FB_SDK_CS_SP_TC_009_L2_CPU_Snake_Traffic_Test_With_MACSec_32x100G
    [Documentation]  This test checks system status with L2 cpu snake traffic 32x100G.
    [Tags]  FB_SDK_CS_SP_TC_009_L2_CPU_Snake_MACSec_100G  cloudripper
    [Timeout]  60 min 00 seconds
    [Setup]    change dir to sdk path
    Step  1  verify load user  ${l2_cpu_snake_traffic_cmd_100G}  ${l2_cpu_pattern}  port_sum_pattern=None  timeout=2400
    [Teardown]  exit mode

FB_SDK_CS_SP_TC_010_L3_CPU_Snake_Traffic_Test_With_MACSec
    [Documentation]  This test checks system status with L3 cpu snake traffic.
    [Tags]  FB_SDK_CS_SP_TC_010_L3_CPU_Snake_MACSec  cloudripper
    [Timeout]  60 min 00 seconds
    [Setup]    change dir to sdk path
    Step  1  verify load user  ${l3_cpu_snake_traffic_cmd}  ${l3_cpu_pattern}  port_sum_pattern=None  timeout=2400
    [Teardown]  exit mode

FB_SDK_CS_SP_TC_011_L3_CPU_Snake_Traffic_Test_With_MACSec_32x200G
    [Documentation]  This test checks system status with L3 cpu snake traffic 32x200G.
    [Tags]  FB_SDK_CS_SP_TC_011_L3_CPU_Snake_MACSec_200G  cloudripper
    [Timeout]  60 min 00 seconds
    [Setup]    change dir to sdk path
    Step  1  verify load user  ${l3_cpu_snake_traffic_cmd_200G}  ${l3_cpu_pattern}  port_sum_pattern=None  timeout=2400
    [Teardown]  exit mode

FB_SDK_CS_SP_TC_012_L3_CPU_Snake_Traffic_Test_With_MACSec_32x100G
    [Documentation]  This test checks system status with L3 cpu snake traffic 32x100G.
    [Tags]  FB_SDK_CS_SP_TC_012_L3_CPU_Snake_MACSec_100G  cloudripper
    [Timeout]  60 min 00 seconds
    [Setup]    change dir to sdk path
    Step  1  verify load user  ${l3_cpu_snake_traffic_cmd_100G}  ${l3_cpu_pattern}  port_sum_pattern=None  timeout=2400
    [Teardown]  exit mode

FB_SDK_CS_COM_TC_031_Each_Port_Disable_Enable_Test
    [Documentation]  This test checks loop 10 times port linkup test.
    [Tags]  FB_SDK_CS_COM_TC_031_Each_Port_Disable_Enable_Test  common  cloudripper
    [Timeout]  60 min 00 seconds
    [Setup]    change dir to sdk path
    Step  1  test load user  ${link_up_cmd}  ${link_up_pattern}

*** Keywords ***
Connect Device
    Set Library Order
    Sdk Device Connect
    Init Test Library
    prepare check log script
    ssh login bmc

Disconnect Device
    ssh disconnect
    Sdk Device Disconnect
