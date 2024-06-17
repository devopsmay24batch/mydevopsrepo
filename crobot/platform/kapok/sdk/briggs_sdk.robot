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

*** Settings ***
Documentation       This Suite will validate all Sdk functions:

Variables         BriggsSdkVariable.py
Library           KapokSdkLib.py
Library          ../KapokCommonLib.py
Library           CommonLib.py

Suite Setup       Onie Connect Device
Suite Teardown    Onie Disconnect Device

*** Variables ***

*** Test Cases ***
BRIGGS_SDK_TC_02_Check_SDK_shell_Version_Test
    [Documentation]  This test checks SDK version and release version
    [Tags]     common  BRIGGS_SDK_TC_02_Check_SDK_shell_Version_Test briggs
    [Timeout]  5 min 00 seconds
    [Setup]    change dir to sdk path
    Step  1  load user mode  ${remote_shell_load_sdk} ${PAM4_400G_32}
    Step  2  check sdk version
    Step  3  exit user mode

BRIGGS_SDK_TC_03_Load_and_Initialization_SDK_Test
    [Documentation]  This test check SDK initialization
    [Tags]     common  BRIGGS_SDK_TC_03_Load_and_Initialization_SDK_Test briggs
    [Timeout]  10 min 00 seconds
    [Setup]    change dir to sdk path
    Step  1  load user mode  ${remote_shell_load_sdk} ${PAM4_100G_128}
    Step  2  exit user mode
    Step  3  load user mode  ${remote_shell_load_sdk} ${NRZ_100G_32}
    Step  4  exit user mode
    Step  5  load user mode  ${remote_shell_load_sdk} ${NRZ_40G_32}
    Step  6  exit user mode
    Step  7  load user mode  ${remote_shell_load_sdk} ${NRZ_25G_128}
    Step  8  exit user mode
    Step  9  load user mode  ${remote_shell_load_sdk} ${NRZ_10G_128}
    Step  10  exit user mode

BRIGGS_SDK_TC_04_Default_Port_info_Test
    [Documentation]  This test check default port information
    [Tags]     common  BRIGGS_SDK_TC_04_Default_Port_info_Test briggs
    [Timeout]  15 min 00 seconds
    [Setup]    change dir to sdk path
    Step  1  load user mode  ${remote_shell_load_sdk} ${PAM4_400G_32}
    Step  2  check port infomation  ${PAM4_400G_32}
    Step  3  exit user mode
    Step  4  load user mode  ${remote_shell_load_sdk} ${PAM4_100G_128}
    Step  5  check port infomation  ${PAM4_100G_128}
    Step  6  exit user mode
    Step  7  load user mode  ${remote_shell_load_sdk} ${NRZ_100G_32}
    Step  8  check port infomation  ${NRZ_100G_32}
    Step  9  exit user mode
    Step  10  load user mode  ${remote_shell_load_sdk} ${NRZ_40G_32}
    Step  11  check port infomation  ${NRZ_40G_32}
    Step  12  exit user mode
    Step  13  load user mode  ${remote_shell_load_sdk} ${NRZ_25G_128}
    Step  14  check port infomation  ${NRZ_25G_128}
    Step  15  exit user mode
    Step  16  load user mode  ${remote_shell_load_sdk} ${NRZ_10G_128}
    Step  17  check port infomation  ${NRZ_10G_128}
    Step  18  exit user mode

BRIGGS_SDK_TC_05_32x400G_Port_Status_Test
    [Documentation]  This test check 32x400G port up/down and speed
    [Tags]     common  BRIGGS_SDK_TC_05_32x400G_Port_Status_Test briggs
    [Timeout]  15 min 00 seconds
    [Setup]    change dir to sdk path
    Step  1  load user mode  ${remote_shell_load_sdk} ${PAM4_400G_32}
    Step  2  check port status  ${PAM4_400G_32}  32
    Step  3  source cmd function  ${PAM4_400G_32}  32
    Step  4  clear counters
    Step  5  source config  ${PAM4_400G_32}  32
    Step  6  start traffic  ${PAM4_400G_32}
    Step  7  check port rate  32  400
    Step  8  stop traffic
    Step  9  check port counter  32
    Step  10  remove config
    Step  11  clear counters
    Step  12  exit user mode

BRIGGS_SDK_TC_06_32x100G_Port_Status_Test
    [Documentation]  This test check 32x100G port up/down and speed
    [Tags]     common  BRIGGS_SDK_TC_06_32x100G_Port_Status_Test briggs
    [Timeout]  15 min 00 seconds
    [Setup]    change dir to sdk path
    Step  1  load user mode  ${remote_shell_load_sdk} ${NRZ_100G_32}
    Step  2  check port status  ${NRZ_100G_32}  32
    Step  3  source cmd function  ${NRZ_100G_32}  32
    Step  4  clear counters
    Step  5  source config  ${NRZ_100G_32}  32
    Step  6  start traffic  ${NRZ_100G_32}
    Step  7  check port rate  32  100
    Step  8  stop traffic
    Step  9  check port counter  32
    Step  10  remove config
    Step  11  clear counters
    Step  12  exit user mode

BRIGGS_SDK_TC_07_128x100G_Port_Status_Test
    [Documentation]  This test check 128x100G port up/down and speed
    [Tags]     common  BRIGGS_SDK_TC_07_128x100G_Port_Status_Test briggs
    [Timeout]  15 min 00 seconds
    [Setup]    change dir to sdk path
    Step  1  load user mode  ${remote_shell_load_sdk} ${PAM4_100G_128}
    Step  2  check port status  ${PAM4_100G_128}  128
    Step  3  source cmd function  ${PAM4_100G_128}  128
    Step  4  clear counters
    Step  5  source config  ${PAM4_100G_128}  128
    Step  6  start traffic  ${PAM4_100G_128}
    Step  7  check port rate  128  100
    Step  8  stop traffic
    Step  9  check port counter  128
    Step  10  remove config
    Step  11  clear counters
    Step  12  exit user mode

BRIGGS_SDK_TC_08_32x40G_Port_Status_Test
    [Documentation]  This test check 32x40G port up/down and speed
    [Tags]     common  BRIGGS_SDK_TC_08_32x40G_Port_Status_Test briggs
    [Timeout]  15 min 00 seconds
    [Setup]    change dir to sdk path
    Step  1  load user mode  ${remote_shell_load_sdk} ${NRZ_40G_32}
    Step  2  check port status  ${NRZ_40G_32}  32
    Step  3  source cmd function  ${NRZ_40G_32}  32
    Step  4  clear counters
    Step  5  source config  ${NRZ_40G_32}  32
    Step  6  start traffic  ${NRZ_40G_32}
    Step  7  check port rate  32  40
    Step  8  stop traffic
    Step  9  check port counter  32
    Step  10  remove config
    Step  11  clear counters
    Step  12  exit user mode

BRIGGS_SDK_TC_09_128x25G_Port_Status_Test
    [Documentation]  This test check 128x25G port up/down and speed
    [Tags]     common  BRIGGS_SDK_TC_09_128x25G_Port_Status_Test briggs
    [Timeout]  15 min 00 seconds
    [Setup]    change dir to sdk path
    Step  1  load user mode  ${remote_shell_load_sdk} ${NRZ_25G_128}
    Step  2  check port status  ${NRZ_25G_128}  128
    Step  3  source cmd function  ${NRZ_25G_128}  128
    Step  4  clear counters
    Step  5  source config  ${NRZ_25G_128}  128
    Step  6  start traffic  ${NRZ_25G_128}
    Step  7  check port rate  128  25
    Step  8  stop traffic
    Step  9  check port counter  128
    Step  10  remove config
    Step  11  clear counters
    Step  12  exit user mode

BRIGGS_SDK_TC_10_128x10G_Port_Status_Test
    [Documentation]  This test check 128x10G port up/down and speed
    [Tags]     common  BRIGGS_SDK_TC_10_128x10G_Port_Status_Test briggs
    [Timeout]  15 min 00 seconds
    [Setup]    change dir to sdk path
    Step  1  load user mode  ${remote_shell_load_sdk} ${NRZ_10G_128}
    Step  2  check port status  ${NRZ_10G_128}  128
    Step  3  source cmd function  ${NRZ_10G_128}  128
    Step  4  clear counters
    Step  5  source config  ${NRZ_10G_128}  128
    Step  6  start traffic  ${NRZ_10G_128}
    Step  7  check port rate  128  10
    Step  8  stop traffic
    Step  9  check port counter  128
    Step  10  remove config
    Step  11  clear counters
    Step  12  exit user mode

BRIGGS_SDK_TC_21_32x400G_PRBS_with_Loopback_Test
    [Documentation]  This test check 32x400G PRBS
    [Tags]     common  BRIGGS_SDK_TC_21_32x400G_PRBS_with_Loopback_Test briggs
    [Timeout]  180 min 00 seconds
    [Setup]    change dir to sdk path
    Step  1  load user mode  ${remote_shell_load_sdk} ${PAM4_400G_32}
    Step  2  source cmd function  ${PAM4_400G_32}  32
    Step  3  check port status  ${PAM4_400G_32}  32
    Step  4  enable prbs tx
    Step  5  enable prbs rx and check counter
    Step  6  check prbs ber
    Step  7  exit user mode

BRIGGS_SDK_TC_22_32x400G_PRBS_with_DAC_Test
    [Documentation]  This test check 32x400G PRBS with DAC
    [Tags]     common  BRIGGS_SDK_TC_22_32x400G_PRBS_with_DAC_Test briggs
    [Timeout]  15 min 00 seconds
    [Setup]    change dir to sdk path
    Step  1  load user mode  ${remote_shell_load_sdk} ${PAM4_400G_32}
    Step  2  source dac cmd function
    Step  3  check port status  ${PAM4_400G_32}  32
    Step  4  prbs tx 31 53g
    Step  5  prbs rx 31 53g 30 1
    Step  6  sleep 5S
    Step  7  prbs rx 31 53g 30 1
    Step  8  exit user mode

BRIGGS_SDK_TC_23_128x100G_PRBS_with_Loopback_Test
    [Documentation]  This test check 128x100G PRBS
    [Tags]     common  BRIGGS_SDK_TC_23_128x100G_PRBS_with_Loopback_Test briggs
    [Timeout]  15 min 00 seconds
    [Setup]    change dir to sdk path
    Step  1  load user mode  ${remote_shell_load_sdk} ${PAM4_100G_128}
    Step  2  ber check
    Step  3  exit user mode

BRIGGS_SDK_TC_24_32x100G_PRBS_with_Loopback_Test
    [Documentation]  This test check 32x100G PRBS
    [Tags]     common  BRIGGS_SDK_TC_24_32x100G_PRBS_with_Loopback_Test briggs
    [Timeout]  120 min 00 seconds
    [Setup]    change dir to sdk path
    Step  1  load user mode  ${remote_shell_load_sdk} ${NRZ_100G_32}
    Step  2  check port status  ${NRZ_100G_32}  32
    Step  3  prbs tx 31 25g
    Step  4  prbs rx 31 25g 5  32
    Step  5  sleep 5S
    Step  6  prbs rx 31 25g 2160  32
    Step  7  exit user mode

BRIGGS_SDK_TC_25_32x40G_PRBS_with_Loopback_Test
    [Documentation]  This test check 32x40G PRBS
    [Tags]     common  BRIGGS_SDK_TC_25_32x40G_PRBS_with_Loopback_Test briggs
    [Timeout]  120 min 00 seconds
    [Setup]    change dir to sdk path
    Step  1  load user mode  ${remote_shell_load_sdk} ${NRZ_40G_32}
    Step  2  check port status  ${NRZ_40G_32}  32
    Step  3  prbs tx 31 10g
    Step  4  prbs rx 31 10g 5  32
    Step  5  sleep 5S
    Step  6  prbs rx 31 10g 2160  32
    Step  7  exit user mode

BRIGGS_SDK_TC_26_128x25G_PRBS_with_Loopback_Test
    [Documentation]  This test check 128x25G PRBS
    [Tags]     common  BRIGGS_SDK_TC_26_128x25G_PRBS_with_Loopback_Test briggs
    [Timeout]  120 min 00 seconds
    [Setup]    change dir to sdk path
    Step  1  load user mode  ${remote_shell_load_sdk} ${NRZ_25G_128}
    Step  2  check port status  ${NRZ_25G_128}  128
    Step  3  prbs tx 31 25g
    Step  4  prbs rx 31 25g 5  128
    Step  5  sleep 5S
    Step  6  prbs rx 31 25g 2160  128
    Step  7  exit user mode

BRIGGS_SDK_TC_27_128x10G_PRBS_with_Loopback_Test
    [Documentation]  This test check 128x10G PRBS
    [Tags]     common  BRIGGS_SDK_TC_27_128x10G_PRBS_with_Loopback_Test briggs
    [Timeout]  120 min 00 seconds
    [Setup]    change dir to sdk path
    Step  1  load user mode  ${remote_shell_load_sdk} ${NRZ_10G_128}
    Step  2  check port status  ${NRZ_10G_128}  128
    Step  3  prbs tx 31 10g
    Step  4  prbs rx 31 10g 5  128
    Step  5  sleep 5S
    Step  6  prbs rx 31 10g 2160  128
    Step  7  exit user mode

BRIGGS_SDK_TC_31_Check_LT_Status_Test
    [Documentation]  This test checks LT status on all copper ports under PAM4_400G_32_b mode.
    [Tags]     common  BRIGGS_SDK_TC_31_Check_LT_Status_Test briggs
    [Timeout]  5 min 00 seconds
    [Setup]    change dir to sdk path
    Step  1  load user mode  ${remote_shell_load_sdk} ${PAM4_400G_32}
    Step  2  exit user mode

BRIGGS_SDK_TC_34_FEC_Test
    [Documentation]  This test check FEC switch with DUT
    [Tags]     common  BRIGGS_SDK_TC_34_FEC_Test briggs
    [Timeout]  30 min 00 seconds
    [Setup]    change dir to sdk path
    Step  1  load user mode  ${remote_shell_load_sdk_integrator} ${integrator_400G_32}
    Step  2  check fec port status  ${integrator_400G_32}  32
    Step  3  exit user mode
    Step  4  load user mode  ${remote_shell_load_sdk_integrator} ${integrator_200G_32}
    Step  5  check fec port status  ${integrator_200G_32}  32
    Step  6  exit user mode
    Step  7  load user mode  ${remote_shell_load_sdk_integrator} ${integrator_100G_32}
    Step  8  check fec port status  ${integrator_100G_32}  32
    Step  9  exit user mode
    Step  10  load user mode  ${remote_shell_load_sdk_integrator} ${integrator_40G_32}
    Step  11  check fec port status  ${integrator_40G_32}  32
    Step  12  exit user mode
    Step  13  load user mode  ${remote_shell_load_sdk_integrator} ${integrator_100G_128}
    Step  14  check fec port status  ${integrator_100G_128}  128
    Step  15  exit user mode
    Step  16  load user mode  ${remote_shell_load_sdk_integrator} ${integrator_25G_128}
    Step  17  check fec port status  ${integrator_25G_128}  128
    Step  18  exit user mode
    Step  19  load user mode  ${remote_shell_load_sdk_integrator} ${integrator_10G_128}
    Step  20  check fec port status  ${integrator_10G_128}  128
    Step  21  exit user mode
    Step  22  load user mode  ${remote_shell_load_sdk_integrator} ${integrator_100G_64}
    Step  23  check fec port status  ${integrator_100G_64}  64
    Step  24  exit user mode

BRIGGS_SDK_TC_41_multiple_snake_traffic
    [Documentation]  This test check multiple snake traffic at the same time.
    [Tags]     common  BRIGGS_SDK_TC_41_multiple_snake_traffic briggs
    [Timeout]  15 min 00 seconds
    [Setup]    change dir to sdk path
    Step  1  load user mode  ${remote_shell_load_sdk} ${PAM4_400G_32}
    Step  2  check port status  ${PAM4_400G_32}  32
    Step  3  source cmd function  ${PAM4_400G_32}  32
    Step  4  clear counters
    Step  5  multiple source config  1-20  21-32
    Step  6  multiple start traffic
    Step  7  multiple check port rate  ${check_rate_id1}  20  400  1
    Step  8  multiple check port rate  ${check_rate_id2}  32  400  21
    Step  9  multiple stop traffic
    Step  10  multiple check port counter  32
    Step  11  exit user mode

BRIGGS_SDK_TC_44_auto_load_sdk_mode
    [Documentation]  This test check port speed.
    [Tags]     common  BRIGGS_SDK_TC_44_auto_load_sdk_mode briggs
    [Timeout]  20 min 00 seconds
    [Setup]    change dir to sdk path
    Step  1  load user mode  ${remote_shell_load_sdk} ${copper_1_8_9_22_23_32}
    Step  2  check port infomation  ${copper_1_8_9_22_23_32}
    Step  3  check port status  ${copper_1_8_9_22_23_32}  all
    Step  4  exit user mode
    Step  5  load user mode  ${remote_shell_load_sdk} ${copper_1_20_21_24_25_32}
    Step  6  check port infomation  ${copper_1_20_21_24_25_32}
    Step  7  check port status  ${copper_1_20_21_24_25_32}  all
    Step  8  exit user mode
    Step  9  load user mode  ${remote_shell_load_sdk} ${copper_1_20_21_24_25_32_4x100}
    Step  10  check port infomation  ${copper_1_20_21_24_25_32_4x100}
    Step  11  check port status  ${copper_1_20_21_24_25_32_4x100}  all
    Step  12  exit user mode

BRIGGS_SDK_TC_48_integrator_sdk_mode_test
    [Documentation]  This test check port speed.
    [Tags]     common  BRIGGS_SDK_TC_48_integrator_sdk_mode_test briggs
    [Timeout]  20 min 00 seconds
    [Setup]    change dir to sdk path
    Step  1  load user mode  ${remote_shell_load_sdk_integrator} ${copper_1_8_9_22_23_32}
    Step  2  check port infomation  ${copper_1_8_9_22_23_32}
    Step  3  check port status  ${copper_1_8_9_22_23_32}  all
    Step  4  exit user mode
    Step  5  load user mode  ${remote_shell_load_sdk_integrator} ${copper_1_20_21_24_25_32}
    Step  6  check port infomation  ${copper_1_20_21_24_25_32}
    Step  7  check port status  ${copper_1_20_21_24_25_32}  all
    Step  8  exit user mode
    Step  9  load user mode  ${remote_shell_load_sdk_integrator} ${copper_1_20_21_24_25_32_4x100}
    Step  10  check port infomation  ${copper_1_20_21_24_25_32_4x100}
    Step  11  check port status  ${copper_1_20_21_24_25_32_4x100}  all
    Step  12  exit user mode

BRIGGS_SDK_TC_73_sfp_detect_tool
    [Documentation]  This test check sfp_detect_tool.
    [Tags]     common  BRIGGS_SDK_TC_73_sfp_detect_tool briggs
    [Timeout]  10 min 00 seconds
    [Setup]    boot Into Onie Rescue Mode
    Step  1  rescue mode change dir to sdk path
    Step  2  sfp detect tool test

BRIGGS_SDK_TC_74_knet_l2_show
    [Documentation]  This test check knet l2 information.
    [Tags]     common  BRIGGS_SDK_TC_74_knet_l2_show briggs
    [Timeout]  10 min 00 seconds
    [Setup]    change dir to sdk path
    Step  1  load daemon mode  ${remote_shell_load_sdk} ${daemon_mode}
    Step  2  knet l2 show

BRIGGS_SDK_TC_77_qsfp
    [Documentation]  This test check provides Vendor.
    [Tags]     common  BRIGGS_SDK_TC_77_qsfp briggs
    [Timeout]  10 min 00 seconds
    [Setup]    change dir to sdk path
    Step  1  qsfp test

*** Keywords ***
Onie Connect Device
    OnieConnect

Onie Disconnect Device
    OnieDisconnect

