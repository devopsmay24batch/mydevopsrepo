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

Variables         KapokSdkVariable.py
Library           KapokSdkLib.py
Library          ../KapokCommonLib.py
Library           CommonLib.py
Resource          KapokSdkKeywords.robot

Suite Setup       Onie Connect Device
Suite Teardown    Onie Disconnect Device

*** Variables ***

*** Test Cases ***
KAPOK_SDK_TC_00_Diag_Initialize_And_Version_Check
    [Tags]  common  KAPOK_SDK_TC_00_Diag_Initialize_And_Version_Check  fenghuang
    [Setup]  boot Into Onie Rescue Mode
    Step  1  Diag Check network connectivity  ${ONIE_RESCUE_MODE}
    Step  2  Diag format Disk  ${fail_dict}
    Step  3  Diag mount Disk  ${fail_dict}
    Step  4  Diag download Images And Recovery DiagOS  ${fail_dict}
    Step  5  Self Update Onie  new
    Step  6  power Cycle To DiagOS
    Step  7  check version before the test
    Step  8  check driver version  ${drive_pattern}

KAPOK_SDK_TC_01_Check_SDK_shell_Version_Test
    [Documentation]  This test checks SDK version and release version
    [Tags]     common  KAPOK_SDK_TC_01_Check_SDK_shell_Version_Test fenghuang
    [Timeout]  5 min 00 seconds
    [Setup]    change dir to sdk path
    Step  1  load user mode  ${remote_shell_load_sdk} ${PAM4_400G_32}
    Step  2  check sdk version
    Step  3  exit user mode

KAPOK_SDK_TC_02_Load_and_Initialization_SDK_Test
    [Documentation]  This test check SDK initialization
    [Tags]     common  KAPOK_SDK_TC_02_Load_and_Initialization_SDK_Test fenghuang
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

KAPOK_SDK_TC_03_Default_Port_info_Test
    [Documentation]  This test check default port information
    [Tags]     common  KAPOK_SDK_TC_03_Default_Port_info_Test fenghuang
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

KAPOK_SDK_TC_04_32x400G_Port_Status_Test
    [Documentation]  This test check 32x400G port up/down and speed
    [Tags]     common  KAPOK_SDK_TC_04_32x400G_Port_Status_Test fenghuang
    [Timeout]  15 min 00 seconds
    [Setup]    change dir to sdk path
    Step  1  load user mode  ${remote_shell_load_sdk} ${PAM4_400G_32}
    Step  2  check port status  ${PAM4_400G_32}  32
    Step  3  source cmd function  ${PAM4_400G_32}  32
    Step  4  clear counters
    Step  5  source config  ${PAM4_400G_32}  32
    Step  6  start traffic  ${PAM4_400G_32}
    Step  7  sleep time  120
    Step  8  check port rate  32  400
    Step  9  stop traffic
    Step  10  check port counter  32
    Step  11  remove config
    Step  12  clear counters
    Step  13  exit user mode

KAPOK_SDK_TC_05_32x100G_Port_Status_Test
    [Documentation]  This test check 32x100G port up/down and speed
    [Tags]     common  KAPOK_SDK_TC_05_32x100G_Port_Status_Test fenghuang
    [Timeout]  15 min 00 seconds
    [Setup]    change dir to sdk path
    Step  1  load user mode  ${remote_shell_load_sdk} ${NRZ_100G_32}
    Step  2  check port status  ${NRZ_100G_32}  32
    Step  3  source cmd function  ${NRZ_100G_32}  32
    Step  4  clear counters
    Step  5  source config  ${NRZ_100G_32}  32
    Step  6  start traffic  ${NRZ_100G_32}
    Step  7  sleep time  120
    Step  8  check port rate  32  100
    Step  9  stop traffic
    Step  10  check port counter  32
    Step  11  remove config
    Step  12  clear counters
    Step  13  exit user mode

KAPOK_SDK_TC_06_128x100G_Port_Status_Test
    [Documentation]  This test check 128x100G port up/down and speed
    [Tags]     common  KAPOK_SDK_TC_06_128x100G_Port_Status_Test fenghuang
    [Timeout]  15 min 00 seconds
    [Setup]    change dir to sdk path
    Step  1  load user mode  ${remote_shell_load_sdk} ${PAM4_100G_128}
    Step  2  check port status  ${PAM4_100G_128}  128
    Step  3  source cmd function  ${PAM4_100G_128}  128
    Step  4  clear counters
    Step  5  source config  ${PAM4_100G_128}  128
    Step  6  start traffic  ${PAM4_100G_128}
    Step  7  sleep time  120
    Step  8  check port rate  128  100
    Step  9  stop traffic
    Step  10  check port counter  128
    Step  11  remove config
    Step  12  clear counters
    Step  13  exit user mode

KAPOK_SDK_TC_07_32x40G_Port_Status_Test
    [Documentation]  This test check 32x40G port up/down and speed
    [Tags]     common  KAPOK_SDK_TC_07_32x40G_Port_Status_Test fenghuang
    [Timeout]  15 min 00 seconds
    [Setup]    change dir to sdk path
    Step  1  load user mode  ${remote_shell_load_sdk} ${NRZ_40G_32}
    Step  2  check port status  ${NRZ_40G_32}  32
    Step  3  source cmd function  ${NRZ_40G_32}  32
    Step  4  clear counters
    Step  5  source config  ${NRZ_40G_32}  32
    Step  6  start traffic  ${NRZ_40G_32}
    Step  7  sleep time  120
    Step  8  check port rate  32  40
    Step  9  stop traffic
    Step  10  check port counter  32
    Step  11  remove config
    Step  12  clear counters
    Step  13  exit user mode

KAPOK_SDK_TC_08_128x25G_Port_Status_Test
    [Documentation]  This test check 128x25G port up/down and speed
    [Tags]     common  KAPOK_SDK_TC_08_128x25G_Port_Status_Test fenghuang
    [Timeout]  15 min 00 seconds
    [Setup]    change dir to sdk path
    Step  1  load user mode  ${remote_shell_load_sdk} ${NRZ_25G_128}
    Step  2  check port status  ${NRZ_25G_128}  128
    Step  3  source cmd function  ${NRZ_25G_128}  128
    Step  4  clear counters
    Step  5  source config  ${NRZ_25G_128}  128
    Step  6  start traffic  ${NRZ_25G_128}
    Step  7  sleep time  120
    Step  8  check port rate  128  25
    Step  9  stop traffic
    Step  10  check port counter  128
    Step  11  remove config
    Step  12  clear counters
    Step  13  exit user mode

KAPOK_SDK_TC_09_128x10G_Port_Status_Test
    [Documentation]  This test check 128x10G port up/down and speed
    [Tags]     common  KAPOK_SDK_TC_09_128x10G_Port_Status_Test fenghuang
    [Timeout]  15 min 00 seconds
    [Setup]    change dir to sdk path
    Step  1  load user mode  ${remote_shell_load_sdk} ${NRZ_10G_128}
    Step  2  check port status  ${NRZ_10G_128}  128
    Step  3  source cmd function  ${NRZ_10G_128}  128
    Step  4  clear counters
    Step  5  source config  ${NRZ_10G_128}  128
    Step  6  start traffic  ${NRZ_10G_128}
    Step  7  sleep time  120
    Step  8  check port rate  128  10
    Step  9  stop traffic
    Step  10  check port counter  128
    Step  11  remove config
    Step  12  clear counters
    Step  13  exit user mode

KAPOK_SDK_TC_10_64x100G_Port_Status_Test
    [Documentation]  This test check 64x100G port up/down and speed
    [Tags]     common  KAPOK_SDK_TC_10_64x100G_Port_Status_Test fenghuang
    [Timeout]  15 min 00 seconds
    [Setup]    change dir to sdk path
    Step  1  load user mode  ${remote_shell_load_sdk} ${NRZ_100G_64}
    Step  2  check port status  ${NRZ_100G_64}  64
    Step  3  source cmd function  ${NRZ_100G_64}  64
    Step  4  clear counters
    Step  5  source config  ${NRZ_100G_64}  64
    Step  6  start traffic  ${NRZ_100G_64}
    Step  7  sleep time  120
    Step  8  check port rate  64  100
    Step  9  stop traffic
    Step  10  check port counter  64
    Step  11  remove config
    Step  12  clear counters
    Step  13  exit user mode

KAPOK_SDK_TC_16_32x400G_PRBS_with_Loopback_Test
    [Documentation]  This test check 32x400G PRBS
    [Tags]     common  KAPOK_SDK_TC_16_32x400G_PRBS_with_Loopback_Test fenghuang
    [Timeout]  180 min 00 seconds
    [Setup]    KapokCommonLib.power Cycle To Onie Install Mode
    Step  1  change dir to sdk path
    Step  2  load user mode  ${remote_shell_load_sdk} ${PAM4_400G_32}
    Step  3  source cmd function  ${PAM4_400G_32}  32
    Step  4  check port status  ${PAM4_400G_32}  32
    Step  5  enable prbs tx
    Step  6  enable prbs rx and check counter
    Step  7  check prbs ber
    Step  8  exit user mode

KAPOK_SDK_TC_17_32x400G_PRBS_with_DAC_Test
    [Documentation]  This test check 32x400G PRBS with DAC
    [Tags]     common  KAPOK_SDK_TC_17_32x400G_PRBS_with_DAC_Test fenghuang
    [Timeout]  15 min 00 seconds
    [Setup]    KapokCommonLib.power Cycle To Onie Install Mode
    Step  1  change dir to sdk path
    Step  2  load user mode  ${remote_shell_load_sdk} ${PAM4_400G_32}
    Step  3  source dac cmd function
    Step  4  check port status  ${PAM4_400G_32}  32
    Step  5  prbs tx 31 53g
    Step  6  prbs rx 31 53g 30 1
    Step  7  sleep 5S
    Step  8  prbs rx 31 53g 30 1
    Step  9  exit user mode

KAPOK_SDK_TC_18_128x100G_PRBS_with_Loopback_Test
    [Documentation]  This test check 128x100G PRBS
    [Tags]     common  KAPOK_SDK_TC_18_128x100G_PRBS_with_Loopback_Test fenghuang
    [Timeout]  15 min 00 seconds
    [Setup]    KapokCommonLib.power Cycle To Onie Install Mode
    Step  1  change dir to sdk path
    Step  2  load user mode  ${remote_shell_load_sdk} ${PAM4_100G_128}
    Step  3  ber check
    Step  4  exit user mode

KAPOK_SDK_TC_19_32x100G_PRBS_with_Loopback_Test
    [Documentation]  This test check 32x100G PRBS
    [Tags]     common  KAPOK_SDK_TC_19_32x100G_PRBS_with_Loopback_Test fenghuang
    [Timeout]  120 min 00 seconds
    [Setup]    KapokCommonLib.power Cycle To Onie Install Mode
    Step  1  change dir to sdk path
    Step  2  load user mode  ${remote_shell_load_sdk} ${NRZ_100G_32}
    Step  3  check port status  ${NRZ_100G_32}  32
    Step  4  prbs tx 31 25g
    Step  5  prbs rx 31 25g 5  32
    Step  6  sleep 5S
    Step  7  prbs rx 31 25g 2160  32
    Step  8  exit user mode

KAPOK_SDK_TC_20_32x40G_PRBS_with_Loopback_Test
    [Documentation]  This test check 32x40G PRBS
    [Tags]     common  KAPOK_SDK_TC_20_32x40G_PRBS_with_Loopback_Test fenghuang
    [Timeout]  120 min 00 seconds
    [Setup]    KapokCommonLib.power Cycle To Onie Install Mode
    Step  1  change dir to sdk path
    Step  2  load user mode  ${remote_shell_load_sdk} ${NRZ_40G_32}
    Step  3  check port status  ${NRZ_40G_32}  32
    Step  4  prbs tx 31 10g
    Step  5  prbs rx 31 10g 5  32
    Step  6  sleep 5S
    Step  7  prbs rx 31 10g 2160  32
    Step  8  exit user mode

KAPOK_SDK_TC_21_128x25G_PRBS_with_Loopback_Test
    [Documentation]  This test check 128x25G PRBS
    [Tags]     common  KAPOK_SDK_TC_21_128x25G_PRBS_with_Loopback_Test fenghuang
    [Timeout]  120 min 00 seconds
    [Setup]    KapokCommonLib.power Cycle To Onie Install Mode
    Step  1  change dir to sdk path
    Step  2  load user mode  ${remote_shell_load_sdk} ${NRZ_25G_128}
    Step  3  check port status  ${NRZ_25G_128}  128
    Step  4  prbs tx 31 25g
    Step  5  prbs rx 31 25g 5  128
    Step  6  sleep 5S
    Step  7  prbs rx 31 25g 2160  128
    Step  8  exit user mode

KAPOK_SDK_TC_22_128x10G_PRBS_with_Loopback_Test
    [Documentation]  This test check 128x10G PRBS
    [Tags]     common  KAPOK_SDK_TC_22_128x10G_PRBS_with_Loopback_Test fenghuang
    [Timeout]  120 min 00 seconds
    [Setup]    KapokCommonLib.power Cycle To Onie Install Mode
    Step  1  change dir to sdk path
    Step  2  load user mode  ${remote_shell_load_sdk} ${NRZ_10G_128}
    Step  3  check port status  ${NRZ_10G_128}  128
    Step  4  prbs tx 31 10g
    Step  5  prbs rx 31 10g 5  128
    Step  6  sleep 5S
    Step  7  prbs rx 31 10g 2160  128
    Step  8  exit user mode

KAPOK_SDK_TC_23_64x100G_PRBS_with_Loopback_Test
    [Documentation]  This test check 64x100G PRBS
    [Tags]     common  KAPOK_SDK_TC_23_64x100G_PRBS_with_Loopback_Test fenghuang
    [Timeout]  120 min 00 seconds
    [Setup]    KapokCommonLib.power Cycle To Onie Install Mode
    Step  1  change dir to sdk path
    Step  2  load user mode  ${remote_shell_load_sdk} ${NRZ_100G_64}
    Step  3  check port status  ${NRZ_100G_64}  64
    Step  4  prbs tx 31 10g
    Step  5  prbs rx 31 10g 5  64
    Step  6  sleep 5S
    Step  7  prbs rx 31 10g 2160  64
    Step  8  exit user mode

KAPOK_SDK_TC_25_FEC_Test
    [Documentation]  This test check FEC switch with DUT
    [Tags]     common  KAPOK_SDK_TC_25_FEC_Test fenghuang
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

KAPOK_SDK_TC_26_multiple_snake_traffic
    [Documentation]  This test check multiple snake traffic at the same time.
    [Tags]     common  KAPOK_SDK_TC_26_multiple_snake_traffic fenghuang
    [Timeout]  15 min 00 seconds
    [Setup]    change dir to sdk path
    Step  1  load user mode  ${remote_shell_load_sdk} ${PAM4_400G_32}
    Step  2  check port status  ${PAM4_400G_32}  32
    Step  3  source cmd function  ${PAM4_400G_32}  32
    Step  4  clear counters
    Step  5  multiple source config  1-20  21-32
    Step  6  multiple start traffic
    Step  7  sleep time  120
    Step  8  multiple check port rate  ${check_rate_id1}  20  400  1
    Step  9  multiple check port rate  ${check_rate_id2}  32  400  21
    Step  10  multiple stop traffic
    Step  11  multiple check port counter  32
    Step  12  exit user mode

KAPOK_SDK_TC_27_auto_load_sdk_mode
    [Documentation]  This test check port speed.
    [Tags]     common  KAPOK_SDK_TC_27_auto_load_sdk_mode fenghuang
    [Timeout]  20 min 00 seconds
    [Setup]    change dir to sdk path
    Step  1  load user mode  ${remote_shell_load_sdk} ${copper_1_8_9_22_23_32}
    Step  2  sleep time  30
    Step  3  check port infomation  ${copper_1_8_9_22_23_32}
    Step  4  check port status  ${copper_1_8_9_22_23_32}  all
    Step  5  exit user mode
    Step  6  load user mode  ${remote_shell_load_sdk} ${copper_1_20_21_24_25_32}
    Step  7  sleep time  30
    Step  8  check port infomation  ${copper_1_20_21_24_25_32}
    Step  9  check port status  ${copper_1_20_21_24_25_32}  all
    Step  10  exit user mode
    Step  11  load user mode  ${remote_shell_load_sdk} ${copper_1_20_21_24_25_32_4x100}
    Step  12  sleep time  30
    Step  13  check port infomation  ${copper_1_20_21_24_25_32_4x100}
    Step  14  check port status  ${copper_1_20_21_24_25_32_4x100}  all
    Step  15  exit user mode

KAPOK_SDK_TC_31_integrator_sdk_mode_test
    [Documentation]  This test check port speed.
    [Tags]     common  KAPOK_SDK_TC_31_integrator_sdk_mode_test fenghuang
    [Timeout]  20 min 00 seconds
    [Setup]    change dir to sdk path
    Step  1  load user mode  ${remote_shell_load_sdk_integrator} ${copper_1_8_9_22_23_32}
    Step  2  sleep time  30
    Step  3  check port infomation  ${copper_1_8_9_22_23_32}
    Step  4  check port status  ${copper_1_8_9_22_23_32}  all
    Step  5  exit user mode
    Step  6  load user mode  ${remote_shell_load_sdk_integrator} ${copper_1_20_21_24_25_32}
    Step  7  sleep time  30
    Step  8  check port infomation  ${copper_1_20_21_24_25_32}
    Step  9  check port status  ${copper_1_20_21_24_25_32}  all
    Step  10  exit user mode
    Step  11  load user mode  ${remote_shell_load_sdk_integrator} ${copper_1_20_21_24_25_32_4x100}
    Step  12  sleep time  30
    Step  13  check port infomation  ${copper_1_20_21_24_25_32_4x100}
    Step  14  check port status  ${copper_1_20_21_24_25_32_4x100}  all
    Step  15  exit user mode

KAPOK_SDK_TC_56_sfp_detect_tool
    [Documentation]  This test check sfp_detect_tool.
    [Tags]     common  KAPOK_SDK_TC_56_sfp_detect_tool fenghuang
    [Timeout]  10 min 00 seconds
    [Setup]    boot Into Onie Rescue Mode
    Step  1  rescue mode change dir to sdk path
    Step  2  sfp detect tool test

KAPOK_SDK_TC_57_knet_l2_show
    [Documentation]  This test check knet l2 information.
    [Tags]     common  KAPOK_SDK_TC_57_knet_l2_show fenghuang
    [Timeout]  10 min 00 seconds
    [Setup]    change dir to sdk path
    Step  1  load daemon mode  ${remote_shell_load_sdk} ${daemon_mode}
    Step  2  knet l2 show

KAPOK_SDK_TC_60_qsfp
    [Documentation]  This test check provides Vendor.
    [Tags]     common  KAPOK_SDK_TC_60_qsfp fenghuang
    [Timeout]  10 min 00 seconds
    [Setup]    change dir to sdk path
    Step  1  qsfp test

TEST_SDK_TC_00_ESS
    [Documentation]  This test check provides Vendor.
    [Tags]     TEST_SDK_TC_00_ESS
    [Timeout]  6000 min 00 seconds
    Step  1  ess test

*** Keywords ***
Onie Connect Device
    OnieConnect

Onie Disconnect Device
    OnieDisconnect

