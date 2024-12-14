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
FENGHUANGV2_SDK_TC_00_Diag_Initialize_And_Version_Check
    [Documentation]  This test Initialize and Version Check
    [Tags]  FENGHUANGV2_SDK_TC_00_Diag_Initialize_And_Version_Check  fenghuangv2
    [Timeout]  60 min 00 seconds
    [Setup]  boot Into Onie Rescue Mode
    Step  1  Diag Check network connectivity  ${ONIE_RESCUE_MODE}
    Step  2  fhv2 Diag download Images And Recovery DiagOS
    Step  3  Self Update Onie  new
    Step  4  power Cycle To DiagOS
    Step  5  check version before the test
    Step  6  check driver version  ${drive_pattern}

FENGHUANGV2_SDK_9.1_Check_SDK_shell_Version_Test
    [Documentation]  This test checks SDK version and release version
    [Tags]     common  FENGHUANGV2_SDK_9.1_Check_SDK_shell_Version_Test  fenghuangv2
    [Timeout]  5 min 00 seconds
    [Setup]    change dir to sdk path
    Step  1  load user mode  ${remote_shell_load_sdk} ${PAM4_400G_32}
    Step  2  check sdk version
    Step  3  exit user mode

FENGHUANGV2_SDK_9.2_Load_and_Initialization_SDK_Test
    [Documentation]  This test check SDK initialization
    [Tags]     FENGHUANGV2_SDK_9.2_Load_and_Initialization_SDK_Test  fenghuangv2
    [Timeout]  10 min 00 seconds
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
    Step  19  load user mode  ${remote_shell_load_sdk} ${NRZ_100G_64}
    Step  20  check port infomation  ${NRZ_100G_64}
    Step  21  exit user mode
    Step  22  load user mode  ${remote_shell_load_sdk} ${NRZ_200G_32}
    Step  23  check port infomation  ${NRZ_200G_32}
    Step  24  exit user mode


FENGHUANGV2_SDK_9.3_Default_Port_info_Test
    [Documentation]  This test check default port information
    [Tags]     common  FENGHUANGV2_SDK_93_Default_Port_info_Test  fenghuangv2
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
    Step  19  load user mode  ${remote_shell_load_sdk} ${NRZ_100G_64}
    Step  20  check port infomation  ${NRZ_100G_64}
    Step  21  exit user mode

FENGHUANGV2_SDK_9.4_32x400G_Port_Status_Test
    [Documentation]  This test check 32x400G port up/down and speed
    [Tags]     common  FENGHUANGV2_SDK_9.4_32x400G_Port_Status_Test  fenghuangv2
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

FENGHUANGV2_SDK_9.5_32x100G_Port_Status_Test
    [Documentation]  This test check 32x100G port up/down and speed
    [Tags]     common  FENGHUANGV2_SDK_9.5_32x100G_Port_Status_Test  fenghuangv2
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

FENGHUANGV2_SDK_9.6_128x100G_Port_Status_Test
    [Documentation]  This test check 128x100G port up/down and speed
    [Tags]     common  FENGHUANGV2_SDK_9.6_128x100G_Port_Status_Test  fenghuangv2
    [Timeout]  15 min 00 seconds
    [Setup]    change dir to sdk path
    Step  1  load user mode  ${remote_shell_load_sdk} ${PAM4_100G_128}
    Step  2  check port status  ${PAM4_100G_128}  128
    Step  3  source cmd function  ${PAM4_100G_128}  128
    Step  4  clear counters
    Step  5  source config  ${PAM4_100G_128}  128
    Step  6  start traffic  ${PAM4_100G_128}
    Step  7  sleep time  120
    Step  8  check port rate  128  83
    Step  9  stop traffic
    Step  10  check port counter  128
    Step  11  remove config
    Step  12  clear counters
    Step  13  exit user mode

FENGHUANGV2_SDK_9.7_32x40G_Port_Status_Test
    [Documentation]  This test check 32x40G port up/down and speed
    [Tags]     common  FENGHUANGV2_SDK_9.7_32x40G_Port_Status_Test  fenghuangv2
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

FENGHUANGV2_SDK_9.8_128x25G_Port_Status_Test
    [Documentation]  This test check 128x25G port up/down and speed
    [Tags]     common  FENGHUANGV2_SDK_9.8_128x25G_Port_Status_Test  fenghuangv2
    [Timeout]  15 min 00 seconds
    [Setup]    change dir to sdk path
    Step  1  load user mode  ${remote_shell_load_sdk} ${NRZ_25G_128}
    Step  2  source cmd function  ${NRZ_25G_128}  128
    Step  3  clear counters
    Step  4  source config  ${NRZ_25G_128}  128
    Step  5  start traffic  ${NRZ_25G_128}
    Step  6  sleep time  120
    Step  7  stop traffic
    Step  8  remove config
    Step  9  clear counters
    Step  10  exit user mode


FENGHUANGV2_SDK_9.9_128x10G_Port_Status_Test
    [Documentation]  This test check 128x10G port up/down and speed
    [Tags]     common  FENGHUANGV2_SDK_9.9_128x10G_Port_Status_Test  fenghuangv2
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

FENGHUANGV2_SDK_9.10_64x100G_Port_Status_Test
    [Documentation]  This test check 64x100G port up/down and speed
    [Tags]     common  FENGHUANGV2_SDK_9.10_64x100G_Port_Status_Test  fenghuangv2
    [Timeout]  15 min 00 seconds
    [Setup]    change dir to sdk path
    Step  1  load user mode  ${remote_shell_load_sdk} ${NRZ_100G_64}
    Step  2  source cmd function  ${NRZ_100G_64}  64
    Step  3  clear counters
    Step  4  source config  ${NRZ_100G_64}  64
    Step  5  start traffic  ${NRZ_100G_64}
    Step  6  sleep time  120
    Step  7  stop traffic
    Step  8  remove config
    Step  9  clear counters
    Step  10  exit user mode

FENGHUANGV2_SDK_9.11_64x100-1G_Port_Status_Test
    [Documentation]  This test check 64x100-1G port up/down and speed
    [Tags]     common  FENGHUANGV2_SDK_9.11_64x100-1G_Port_Status_Test  fenghuangv2
    [Timeout]  15 min 00 seconds
    [Setup]    change dir to sdk path
    Step  1  load user mode  ${remote_shell_load_sdk_integrator} ${integrator_100G_64_1}
    Step  2  source cmd function  ${integrator_100G_64_1}  64
    Step  3  clear counters
    Step  4  source config  ${integrator_100G_64_1}  64  True
    Step  5  start traffic  ${integrator_100G_64_1}
    Step  6  sleep time  120
    Step  7  stop traffic
    Step  8  remove config
    Step  9  clear counters
    Step  10  exit user mode

FENGHUANGV2_SDK_9.20_32x400G_PRBS_with_Loopback_Test
    [Documentation]  This test check 32x400G PRBS
    [Tags]     common  FENGHUANGV2_SDK_9.20_32x400G_PRBS_with_Loopback_Test  fenghuangv2
    [Timeout]  180 min 00 seconds
    [Setup]    KapokCommonLib.power Cycle To Onie Install Mode
    Step  1  change dir to sdk path
    Step  2  load user mode  ${remote_shell_load_sdk} ${PAM4_400G_32}
    Step  3  check ber level   ${PAM4_400G_32}  32
    Step  4  exit user mode

FENGHUANGV2_SDK_9.21_32x400G_PRBS_with_DAC_Test
    [Documentation]  This test check 32x400G PRBS with DAC
    [Tags]     common  FENGHUANGV2_SDK_9.21_32x400G_PRBS_with_DAC_Test  fenghuangv2
    [Timeout]  15 min 00 seconds
    [Setup]    KapokCommonLib.power Cycle To Onie Install Mode
    Step  1  change dir to sdk path
    Step  2  load user mode  ${remote_shell_load_sdk} ${PAM4_400G_32}
    Step  3  check ber level   ${PAM4_400G_32}  32
    Step  4  exit user mode

FENGHUANGV2_SDK_9.22_128x100G_PRBS_with_Loopback_Test
    [Documentation]  This test check 128x100G PRBS
    [Tags]     common  FENGHUANGV2_SDK_9.22_128x100G_PRBS_with_Loopback_Test  fenghuangv2
    [Timeout]  15 min 00 seconds
    [Setup]    KapokCommonLib.power Cycle To Onie Install Mode
    Step  1  change dir to sdk path
    Step  2  load user mode  ${remote_shell_load_sdk} ${PAM4_100G_128}
    Step  3  check ber level   ${PAM4_100G_128}  128
    Step  4  exit user mode

FENGHUANGV2_SDK_9.23_32x100G_PRBS_with_Loopback_Test
    [Documentation]  This test check 32x100G PRBS
    [Tags]     common  FENGHUANGV2_SDK_9.23_32x100G_PRBS_with_Loopback_Test  fenghuangv2
    [Timeout]  120 min 00 seconds
    [Setup]    KapokCommonLib.power Cycle To Onie Install Mode
    Step  1  change dir to sdk path
    Step  2  load user mode  ${remote_shell_load_sdk} ${NRZ_100G_32}
    Step  3  check ber level   ${NRZ_100G_32}  32
    Step  4  exit user mode

FENGHUANGV2_SDK_9.24_32x40G_PRBS_with_Loopback_Test
    [Documentation]  This test check 32x40G PRBS
    [Tags]     common  FENGHUANGV2_SDK_9.24_32x40G_PRBS_with_Loopback_Test  fenghuangv2
    [Timeout]  120 min 00 seconds
    [Setup]    KapokCommonLib.power Cycle To Onie Install Mode
    Step  1  change dir to sdk path
    Step  2  load user mode  ${remote_shell_load_sdk} ${NRZ_40G_32}
    Step  3  check ber level  ${NRZ_40G_32}  32
    Step  4  exit user mode


FENGHUANGV2_SDK_9.25_128x25G_PRBS_with_Loopback_Test
    [Documentation]  This test check 128x25G PRBS
    [Tags]     common  FENGHUANGV2_SDK_9.25_128x25G_PRBS_with_Loopback_Test  fenghuangv2
    [Timeout]  120 min 00 seconds
    [Setup]    KapokCommonLib.power Cycle To Onie Install Mode
    Step  1  change dir to sdk path
    Step  2  load user mode  ${remote_shell_load_sdk} ${NRZ_25G_128}
    Step  3  check ber level  ${NRZ_25G_128}  128
    Step  4  exit user mode


FENGHUANGV2_SDK_9.26_128x10G_PRBS_with_Loopback_Test
    [Documentation]  This test check 128x10G PRBS
    [Tags]     common  FENGHUANGV2_SDK_9.26_128x10G_PRBS_with_Loopback_Test  fenghuangv2
    [Timeout]  120 min 00 seconds
    [Setup]    KapokCommonLib.power Cycle To Onie Install Mode
    Step  1  change dir to sdk path
    Step  2  load user mode  ${remote_shell_load_sdk} ${NRZ_10G_128}
    Step  3  check ber level  ${NRZ_10G_128}  128
    Step  4  exit user mode


FENGHUANGV2_SDK_9.27_64x100G_PRBS_with_Loopback_Test
    [Documentation]  This test check 64x100G PRBS
    [Tags]     common  FENGHUANGV2_SDK_9.27_64x100G_PRBS_with_Loopback_Test  fenghuangv2
    [Timeout]  120 min 00 seconds
    [Setup]    KapokCommonLib.power Cycle To Onie Install Mode
    Step  1  change dir to sdk path
    Step  2  load user mode  ${remote_shell_load_sdk} ${NRZ_100G_64}
    Step  3  check ber level  ${NRZ_100G_64}  64
    Step  4  exit user mode


FENGHUANGV2_SDK_9.29_32x400G_PRBS_Test_(Via ONIE_PORT_CMD)
    [Documentation]  This test to check 32x400G PRBS via ONIE_PORT_CMD
    [Tags]     common  FENGHUANGV2_SDK_9.29_32x400G_PRBS_Test_(Via ONIE_PORT_CMD)  fenghuangv2
    [Timeout]  120 min 00 seconds
    [Setup]    KapokCommonLib.power Cycle To Onie Install Mode
    Step  1  change dir to sdk path
    Step  2  load prbs mode  ${remote_shell_load_sdk_integrator} ${integrator_400G_32_copper}
    Step  3  check PRBS  ${option_32_400G}

FENGHUANGV2_SDK_9.30_32x100G_PRBS_Test_(Via ONIE_PORT_CMD)
    [Documentation]  This test to check 32x100G PRBS via ONIE_PORT_CMD
    [Tags]     common  FENGHUANGV2_SDK_9.30_32x100G_PRBS_Test_(Via ONIE_PORT_CMD)  fenghuangv2
    [Timeout]  120 min 00 seconds
    [Setup]    KapokCommonLib.power Cycle To Onie Install Mode
    Step  1  change dir to sdk path
    Step  2  load prbs mode  ${remote_shell_load_sdk_integrator} ${integrator_100g_32_copper}
    Step  3  check PRBS  ${option_32_100G}

FENGHUANGV2_SDK_9.31_32x40G_PRBS_Test_(Via ONIE_PORT_CMD)
    [Documentation]  This test to check 32x40G PRBS via ONIE_PORT_CMD
    [Tags]     common  FENGHUANGV2_SDK_9.31_32x40G_PRBS_Test_(Via ONIE_PORT_CMD)  fenghuangv2
    [Timeout]  120 min 00 seconds
    [Setup]    KapokCommonLib.power Cycle To Onie Install Mode
    Step  1  change dir to sdk path
    Step  2  load prbs mode  ${remote_shell_load_sdk_integrator} ${integrator_40G_32_copper}
    Step  3  check PRBS  ${option_32_40G}

FENGHUANGV2_SDK_9.32_128x100G_PRBS_Test_(Via ONIE_PORT_CMD)
    [Documentation]  This test to check 128x100G PRBS via ONIE_PORT_CMD
    [Tags]     common  FENGHUANGV2_SDK_9.32_128x100G_PRBS_Test_(Via ONIE_PORT_CMD)  fenghuangv2
    [Timeout]  120 min 00 seconds
    [Setup]    KapokCommonLib.power Cycle To Onie Install Mode
    Step  1  change dir to sdk path
    Step  2  load prbs mode  ${remote_shell_load_sdk_integrator} ${integrator_100G_128_copper}
    Step  3  check PRBS  ${option_128_100G}

FENGHUANGV2_SDK_9.28_64x100-1G_PRBS_with_Loopback_Test
    [Documentation]  This test check 64x100-1G PRBS
    [Tags]     common  FENGHUANGV2_SDK_9.28_64x100-1G_PRBS_with_Loopback_Test  fenghuangv2
    [Timeout]  120 min 00 seconds
    [Setup]    KapokCommonLib.power Cycle To Onie Install Mode
    Step  1  change dir to sdk path
    Step  2  load user mode  ${remote_shell_load_sdk} ${NRZ_100G_64_1}
    Step  3  check ber level   ${NRZ_100G_64_1}  64
    Step  4  exit user mode

FENGHUANGV2_SDK_9.37_FEC_Test
    [Documentation]  This test check FEC switch with DUT
    [Tags]     common  FENGHUANGV2_SDK_9.37_FEC_Test  fenghuangv2
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
    Step  25  load user mode  ${remote_shell_load_sdk_integrator} ${integrator_100G_64_1}
    Step  26  check fec port status  ${integrator_100G_64_1}  64
    Step  27  exit user mode

FENGHUANGV2_SDK_9.33_128x25G_PRBS_Test_(Via ONIE_PORT_CMD)
    [Documentation]  This test to check 128x25G PRBS via ONIE_PORT_CMD
    [Tags]     common  FENGHUANGV2_SDK_9.33_128x25G_PRBS_Test_(Via ONIE_PORT_CMD)  fenghuangv2
    [Timeout]  15 min 00 seconds
    Step  1  change dir to sdk path
    Step  2  load prbs mode  ${remote_shell_load_sdk_integrator} ${integrator_25G_128_copper}
    Step  3  check PRBS  ${option_128x10}

FENGHUANGV2_SDK_9.34_128x10G_PRBS_Test_(Via ONIE_PORT_CMD)
    [Documentation]  This test to check 128x10G PRBS via ONIE_PORT_CMD
    [Tags]     common  FENGHUANGV2_SDK_9.34_128x10G_PRBS_Test_(Via ONIE_PORT_CMD)  fenghuangv2
    [Timeout]  15 min 00 seconds
    Step  1  change dir to sdk path
    Step  2  load prbs mode  ${remote_shell_load_sdk_integrator} ${integrator_10G_128_copper}
    Step  3  check PRBS  ${option_128x10}

FENGHUANGV2_SDK_9.35_64x100_PRBS_Test_(Via ONIE_PORT_CMD)
    [Documentation]  This test to check 64x100 PRBS via ONIE_PORT_CMD
    [Tags]     common  FENGHUANGV2_SDK_9.35_64x100_PRBS_Test_(Via ONIE_PORT_CMD)  fenghuangv2
    [Timeout]  15 min 00 seconds
    Step  1  change dir to sdk path
    Step  2  load prbs mode  ${remote_shell_load_sdk_integrator} ${integrator_100G_64_copper}
    Step  3  check PRBS  ${option_64x100}

FENGHUANGV2_SDK_9.36_64x100-1G_PRBS_Test_(Via ONIE_PORT_CMD)
    [Documentation]  This test to check 64x100-1G PRBS via ONIE_PORT_CMD
    [Tags]     common  FENGHUANGV2_SDK_9.36_64x100-1G_PRBS_Test_(Via ONIE_PORT_CMD)  fenghuangv2
    [Timeout]  15 min 00 seconds
    Step  1  change dir to sdk path
    Step  2  load prbs mode  ${remote_shell_load_sdk_integrator} ${integrator_100G_64_1_copper}
    Step  3  check PRBS  ${option_64x100}

FENGHUANGV2_SDK_9.38_FEC_ENABLE_Test
    [Documentation]  This test to check EFC enable test
    [Tags]     common  FENGHUANGV2_SDK_9.38_FEC_ENABLE_Test  fenghuangv2
    [Timeout]  45 min 00 seconds
    [Setup]    change dir to sdk path
    Step  1  run each speed  ${fenghuangv2_32_FEC_cmd}  32
    Step  2  run each speed  ${fenghuangv2_64_FEC_cmd}  64
    Step  3  run each speed  ${fenghuangv2_128_FEC_cmd}  128

FENGHUANGV2_SDK_9.39_Remote_Shell_Test
    [Documentation]  This test to check SDK can load successful by remote
    [Tags]     common  FENGHUANGV2_SDK_9.39_Remote_Shell_Test fenghuangv2
    [Timeout]  18 min 00 seconds
    [Setup]    KapokCommonLib.power Cycle To Onie Install Mode
    Step  1  remote Shell Check Port Info
    Step  2  remote Shell Save Log To File

FENGHUANGV2_SDK_9.42_multiple_snake_traffic
    [Documentation]  This test check multiple snake traffic at the same time.
    [Tags]     common  FENGHUANGV2_SDK_9.42_multiple_snake_traffic fenghuangv2
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

FENGHUANGV2_SDK_11_auto_load_sdk_mode
    [Documentation]  This test check port speed.
    [Tags]     common  FENGHUANGV2_SDK_11_auto_load_sdk_mode fenghuangv2
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

FENGHUANGV2_SDK_11.2_auto_load_sdk_mode
    [Documentation]  This test check port speed.
    [Tags]     FENGHUANGV2_SDK_11.2_auto_load_sdk_mode  fenghuangv2
    [Timeout]  20 min 00 seconds
    [Setup]    change dir to sdk path
    Step  1  load user mode  ${remote_shell_load_sdk} ${copper_1_20_21_24_25_32}
    Step  2  sleep time  30
    Step  3  check port info
    Step  4  check port enable  ${copper_1_20_21_24_25_32}  all
    Step  5  exit user mode

FENGHUANGV2_SDK_11.3_auto_load_sdk_mode
    [Documentation]  This test check port speed.
    [Tags]     FENGHUANGV2_SDK_11.3_auto_load_sdk_mode  fenghuangv2
    [Timeout]  20 min 00 seconds
    [Setup]    change dir to sdk path
    Step  1  load user mode  ${remote_shell_load_sdk} ${copper_1_20_21_24_25_32_4x100}
    Step  2  sleep time  30
    Step  3  check port info
    Step  4  check port enable  ${copper_1_20_21_24_25_32_4x100}  all
    Step  5  exit user mode


FENGHUANGV2_SDK_12_integrator_sdk_mode_test
    [Documentation]  This test check port speed.
    [Tags]     common  FENGHUANGV2_SDK_12_integrator_sdk_mode_test fenghuangv2
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

FENGHUANGV2_SDK_12.3_default_onie_fpp_port_mode
    [Documentation]  This test to check default “onie_fpp” port mode should be PAM4_100G_128.
    [Tags]     FENGHUANGV2_SDK_12.3_default_onie_fpp_port_mode   fenghuangv2
    [Timeout]  10 min 00 seconds
    [Setup]    change dir to sdk path
    Step  1  boot into Uboot
    Step  2  set Default Onie Fpp

FENGHUANGV2_SDK_12.4_Integrator_Vlan_Setting_Check
    [Documentation]  This test to to check vlan setting under integrator mode.
    [Tags]     common  FENGHUANGV2_SDK_12.4_Integrator_Vlan_Setting_Check  fenghuangv2
    [Timeout]  10 min 00 seconds
    [Setup]    change dir to sdk path
    Step  1  port Enabled
    Step  2  show Devport  ${PAM4_100G_128_pattern}
    Step  3  diagtest Knet Show
    Step  4  exit Vlan Setting  ${True}
    Step  5  show Devport  ${PAM4_100G_128_pattern}
    Step  6  diagtest Knet Show  ${vlan_check_pattern}
    Step  7  exit Vlan Setting

FENGHUANGV2_SDK_15.1_sfp_detect_tool
    [Documentation]  This test check sfp_detect_tool.
    [Tags]     common  FENGHUANGV2_SDK_15.1_sfp_detect_tool fenghuangv2
    [Timeout]  10 min 00 seconds
    [Setup]    boot Into Onie Rescue Mode
    Step  1  rescue mode change dir to sdk path
    Step  2  sfp detect tool test

FENGHUANGV2_SDK_15.2_knet_l2_show
    [Documentation]  This test check knet l2 information.
    [Tags]     common  FENGHUANGV2_SDK_15.2_knet_l2_show fenghuangv2
    [Timeout]  10 min 00 seconds
    [Setup]    change dir to sdk path
    Step  1  load daemon mode  ${remote_shell_load_sdk} ${daemon_mode}
    Step  2  knet l2 show

FENGHUANGV2_SDK_15.3_Integrator_mode_config
    [Documentation]  This test check Integrator mode config.
    [Tags]     common  FENGHUANGV2_SDK_15.3_Integrator_mode_config  fenghuangv2
    [Timeout]  150 min 00 seconds
    [Setup]    change dir to sdk path
    Step  1  load user mode  ${remote_shell_load_sdk_integrator} ${integrator_400G_32}
    Step  2  sleep time  30
    Step  3  check fec port status  ${integrator_400G_32}  32
    Step  4  exit user mode
    Step  5  load user mode  ${remote_shell_load_sdk_integrator} ${integrator_200G_32}
    Step  6  sleep time  30
    Step  7  check fec port status  ${integrator_200G_32}  32
    Step  8  exit user mode
    Step  9  load user mode  ${remote_shell_load_sdk_integrator} ${integrator_100G_32}
    Step  10  sleep time  30
    Step  11  check fec port status  ${integrator_100G_32}  32
    Step  12  exit user mode
    Step  13  load user mode  ${remote_shell_load_sdk_integrator} ${integrator_40G_32}
    Step  14  sleep time  30
    Step  15  check fec port status  ${integrator_40G_32}  32
    Step  16  exit user mode
    Step  17  load user mode  ${remote_shell_load_sdk_integrator} ${integrator_100G_128}
    Step  18  sleep time  30
    Step  19  check fec port status  ${integrator_100G_128}  128
    Step  20  exit user mode
    Step  21  load user mode  ${remote_shell_load_sdk_integrator} ${integrator_25G_128}
    Step  22  sleep time  30
    Step  23  check fec port status  ${integrator_25G_128}  128
    Step  24  exit user mode
    Step  25  load user mode  ${remote_shell_load_sdk_integrator} ${integrator_10G_128}
    Step  26  sleep time  30
    Step  27  check fec port status  ${integrator_10G_128}  128
    Step  28  exit user mode
    Step  29  load user mode  ${remote_shell_load_sdk_integrator} ${integrator_100G_64}
    Step  30  sleep time  30
    Step  31  check fec port status  ${integrator_100G_64}  64
    Step  32  exit user mode
    Step  33  load user mode  ${remote_shell_load_sdk_integrator} ${integrator_100G_64_1}
    Step  34  sleep time  30
    Step  35  check fec port status  ${integrator_100G_64_1}  64
    Step  36  exit user mode

FENGHUANGV2_SDK_15.4_qsfp
    [Documentation]  This test check provides Vendor.
    [Tags]     common  FENGHUANGV2_SDK_15.4_qsfp fenghuangv2
    [Timeout]  10 min 00 seconds
    [Setup]    change dir to sdk path
    Step  1  qsfp test

FENGHUANGV2_SDK_9.50_Ess_Script_Test
    [Documentation]  The purpose of this test is to check ess test is passed.
    [Tags]  common  FENGHUANGV2_SDK_9.50_Ess_Script_Test  fenghuangv2
    [Setup]  change dir to sdk path
    step  1  run Ess Script 






SDK_17.4_1x400G All_Ports_Enable_Disable_Stress_Test
    [Documentation]   After port enable/disable, port link status can be displayed correctly and traffic no loss package for 1000 times
    [Tags]   SDK_17.4_1x400G All_Ports_Enable_Disable_Stress_Test   fenghuangv2  total
    [Setup]  change dir to sdk path
    [Timeout]  120 min 00 seconds
    Step  1  load user mode  ${remote_shell_load_sdk} ${PAM4_400G_32}
    ${Current_Loop}  Evaluate  10-1
    FOR    ${INDEX}    IN RANGE    1  10
         Print Loop Info  ${INDEX}  ${Current_Loop}
         Step  2  check port status  ${PAM4_400G_32}  32
         Step  3  port disable and check status  32
         Step  4  sleep time  10
         Step  4  port enable and check status  32
         Step  5  sleep time   10
         #Step  5  check port status  ${PAM4_400G_32}  32
         Step  6  source config  ${PAM4_400G_32}  32
         Step  7  clear port counters
         #Step  6  source config  ${PAM4_400G_32}  32
         Step  7  clear port counters
         Step  9  start traffic  ${PAM4_400G_32}
         Step  10  sleep time  120
         Step  10  check port rate  32  400
         Step  11  stop traffic
         Step  12  check port counter  32
         Step  13  remove config
    END
    Step  13  exit user mode





*** Keywords ***
Onie Connect Device
    OnieConnect

Onie Disconnect Device
    OnieDisconnect

