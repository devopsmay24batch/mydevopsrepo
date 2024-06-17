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
Documentation       This Suite will validate all Stress functions:

Variables         KapokStressVariable.py
Variables         Const.py
Variables         ../sdk/KapokSdkVariable.py
Library           ../sdk/KapokSdkLib.py
Library           KapokStressLib.py
Library          ../KapokCommonLib.py
Library           CommonLib.py

Resource        CommonKeywords.resource
Resource        KapokCommonKeywords.resource
Resource        KapokStressKeywords.resource

Suite Setup       Stress Onie Connect Device
Suite Teardown    Stress Onie Disconnect Device

*** Variables ***


*** Test Cases ***
KAPOK_STRESS_TC_00_Diag_Initialize_And_Version_Check
    [Tags]  common  KAPOK_STRESS_TC_00_Diag_Initialize_And_Version_Check  fenghuang
    [Setup]  KapokCommonLib.boot Into Onie Rescue Mode
    Step  1  Check network connectivity  ${ONIE_RESCUE_MODE}
    Step  2  Diag format Disk  ${fail_dict}
    Step  3  Diag mount Disk  ${fail_dict}
    Step  4  Diag download Images And Recovery DiagOS  ${fail_dict}
    Step  5  Self Update Onie  new
    Step  6  KapokStressLib.power Cycle To DiagOS
    Step  7  check version before the test
    Step  8  check driver version  ${drive_pattern}

KAPOK_STRESS_TC_05_Power_Cycle_Test
    [Documentation]  This test checks whether the system will boot up every time after power-cycle
    [Tags]     common  KAPOK_STRESS_TC_05_Power_Cycle_Test fenghuang
    [Timeout]  240 min 00 seconds
    ${MaxLoopNum}=  KapokCommonLib.get data from yaml
    ...  name=${TEST NAME}
    ${Current_Loop}  Evaluate  ${MaxLoopNum}-1
    FOR    ${INDEX}    IN RANGE    1    ${MaxLoopNum}
        Print Loop Info  ${INDEX}  ${Current_Loop}
        Step  1  KapokCommonLib.power Cycle To DiagOS
    END

KAPOK_STRESS_TC_06_Ddr_Stress_Test
    [Documentation]  This test checks DDR function
    [Tags]     common  KAPOK_STRESS_TC_06_Ddr_Stress_Test fenghuang
    [Timeout]  180 min 00 seconds
    ${MaxLoopNum}=  KapokCommonLib.get data from yaml
    ...  name=${TEST NAME}
    ${Current_Loop}  Evaluate  ${MaxLoopNum}-1
    FOR    ${INDEX}    IN RANGE    1    ${MaxLoopNum}
        Print Loop Info  ${INDEX}  ${Current_Loop}
        Step  1  KapokCommonLib.power Cycle To DiagOS
        Step  2  fhv2 get Dhcp IP
        Step  3  Check network connectivity  ${BOOT_MODE_DIAGOS}
        Step  4  fhv2 download stress And Recovery DiagOS
        Step  5  execute command and verify with a pattern
        ...  console=${diagos_mode}
        ...  command=(bash ddr_test.sh)
        ...  path=${tools_script_stress_path}
        ...  sec=9000  # 2.5 hours and typically 2 hours
        ...  pattern=DDR stress testing
        ...  msg=Failed, not found the start message!
        ...  is_check_exit_code=${TRUE}
        Step  6  verify ddr stress test
    END

KAPOK_STRESS_TC_07_SSD_STRESS_TEST
    [Documentation]  This test checks SSD function
    [Tags]     common  KAPOK_STRESS_TC_07_SSD_STRESS_TEST fenghuang
    [Timeout]  180 min 00 seconds
    ${MaxLoopNum}=  KapokCommonLib.get data from yaml
    ...  name=${TEST NAME}
    ${Current_Loop}  Evaluate  ${MaxLoopNum}-1
    FOR    ${INDEX}    IN RANGE    1    ${MaxLoopNum}
        Print Loop Info  ${INDEX}  ${Current_Loop}
        Step  1  KapokCommonLib.power Cycle To DiagOS
        Step  2  fhv2 get Dhcp IP
        Step  3  Check network connectivity  ${BOOT_MODE_DIAGOS}
        Step  4  fhv2 download stress And Recovery DiagOS
        Step  5  execute command and verify with a pattern
        ...  console=${diagos_mode}
        ...  command=(bash ssd_test.sh)
        ...  path=${tools_script_stress_path}
        ...  sec=21600  # Did not know how long, assumed not more than 6 hours
        ...  pattern=${ssd_stress_patterns}
        ...  msg=Failed, not found the pass patterns!
        ...  is_check_exit_code=${TRUE}
    END

KAPOK_STRESS_TC_08_I2C_BUS_SCAN_STRESS_TEST
    [Documentation]  This test checks access all the I2C end-point devices successfully
    [Tags]     common  KAPOK_STRESS_TC_08_I2C_BUS_SCAN_STRESS_TEST fenghuang
    [Timeout]  360 min 00 seconds
    Step  1  KapokCommonLib.power Cycle To DiagOS
    ${MaxLoopNum}=  KapokCommonLib.get data from yaml
    ...  name=${TEST NAME}
    ${Current_Loop}  Evaluate  ${MaxLoopNum}-1
    FOR    ${INDEX}    IN RANGE    1    ${MaxLoopNum}
        Print Loop Info  ${INDEX}  ${Current_Loop}
        Step  2  I2C bus scan stress test
    END

KAPOK_STRESS_TC_09_DIAG_ALL_TEST
    [Documentation]  This test is to run all diagnostic test
    [Tags]     common  KAPOK_STRESS_TC_09_DIAG_ALL_TEST fenghuang
    [Timeout]  180 min 00 seconds
    Step  1  KapokCommonLib.power Cycle To DiagOS
    ${MaxLoopNum}=  KapokCommonLib.get data from yaml
    ...  name=${TEST NAME}
    ${Current_Loop}  Evaluate  ${MaxLoopNum}-1
    FOR    ${INDEX}    IN RANGE    1    ${MaxLoopNum}
        Print Loop Info  ${INDEX}  ${Current_Loop}
        Step  2  run all diagnostic test
    END

KAPOK_STRESS_TC_10_UBOOT_MGMT_TFTP_STRESS_TEST
    [Documentation]  This test is to check U-boot MGMT port tftp download stress test
    [Tags]     common  KAPOK_STRESS_TC_10_UBOOT_MGMT_TFTP_STRESS_TEST fenghuang
    [Timeout]  180 min 00 seconds
    ${MaxLoopNum}=  KapokCommonLib.get data from yaml
    ...  name=${TEST NAME}
    ${Current_Loop}  Evaluate  ${MaxLoopNum}-1
    FOR    ${INDEX}    IN RANGE    1    ${MaxLoopNum}
        Print Loop Info  ${INDEX}  ${Current_Loop}
        Step  1   U-Boot mdio read
        Step  2   U-Boot sleep
        Step  3   U-Boot mdio read
        Step  4   U-Boot sleep
        Step  5   U-Boot mdio read
        Step  6   U-Boot sleep
        Step  7   U-Boot setenv  env=serverip ${tftp_server_ipv4}
        Step  8   U-Boot setenv  env=ipaddr ${tftp_client_ipv4}
        Step  9   U-Boot tftpboot
        Step  10   U-Boot reset
    END

KAPOK_STRESS_TC_11_ONIE_Updater_Stress_Test
    [Documentation]  This test checks the ONIE Updater Stress Test
    [Tags]  common  KAPOK_STRESS_TC_11_ONIE_Updater_Stress_Test  fenghuang
    [Timeout]  180 min 00 seconds
    ${MaxLoopNum}=  KapokCommonLib.get data from yaml
    ...  name=${TEST NAME}
    ${Current_Loop}  Evaluate  ${MaxLoopNum}-1
    FOR    ${INDEX}    IN RANGE    1    ${MaxLoopNum}
        Print Loop Info  ${INDEX}  ${Current_Loop}
        Step  1  Self Update Onie  old
        Step  2  Self Update Onie  new
    END

KAPOK_STRESS_TC_12_CPLD/FPGA_Updates_Stress_Test
    [Documentation]  This test checks that CPLD can be updated under ONIE mode
    [Tags]  common  KAPOK_STRESS_TC_12_CPLD/FPGA_Updates_Stress_Test  fenghuang
    [Timeout]  180 min 00 seconds
    ${MaxLoopNum}=  KapokCommonLib.get data from yaml
    ...  name=${TEST NAME}
    ${Current_Loop}  Evaluate  ${MaxLoopNum}-1
    FOR    ${INDEX}    IN RANGE    1    ${MaxLoopNum}
        Print Loop Info  ${INDEX}  ${Current_Loop}
        Step  1  KapokCommonLib.boot Into Onie Rescue Mode
        Step  2  Check network connectivity  ${ONIE_RESCUE_MODE}
        Step  3  upgrade cpld
        Step  4  KapokCommonLib.power Cycle To Onie Rescue Mode
        Step  5  check cpld version
    END

KAPOK_STRESS_TC_13_Warm_Reboot_Stress_Test
    [Documentation]  This test checks each of reboot cycle work normally.
    [Tags]  common  KAPOK_STRESS_TC_13_Warm_Reboot_Stress_Test  fenghuang
    [Timeout]  180 min 00 seconds
    ${MaxLoopNum}=  KapokCommonLib.get data from yaml
    ...  name=${TEST NAME}
    ${Current_Loop}  Evaluate  ${MaxLoopNum}-1
    FOR    ${INDEX}    IN RANGE    1    ${MaxLoopNum}
        Print Loop Info  ${INDEX}  ${Current_Loop}
        Step  1  warm stress reboot
        Step  2  verify onie and cpld version  new
    END

KAPOK_STRESS_TC_14_ReInit_SDK_Stress_Test
    [Documentation]  This test checks every SDK init, port link status can be displayed correctly and traffic no loss package for 1000 times
    [Tags]  common  KAPOK_STRESS_TC_14_ReInit_SDK_Stress_Test  fenghuang
    [Timeout]  180 min 00 seconds
    [Setup]    change dir to sdk path
    ${MaxLoopNum}=  KapokCommonLib.get data from yaml
    ...  name=${TEST NAME}
    ${Current_Loop}  Evaluate  ${MaxLoopNum}-1
    FOR    ${INDEX}    IN RANGE    1    ${MaxLoopNum}
        Print Loop Info  ${INDEX}  ${Current_Loop}
        Step  1  load user mode  ${remote_shell_load_sdk}
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
    END

KAPOK_STRESS_TC_15_PRBS_SDK_Stress_Test
    [Documentation]  This test checks all kinds of PRBS for 24 hrs
    [Tags]  common  KAPOK_STRESS_TC_15_PRBS_SDK_Stress_Test  fenghuang
    [Timeout]  180 min 00 seconds
    [Setup]    change dir to sdk path
    ${MaxLoopNum}=  KapokCommonLib.get data from yaml
    ...  name=${TEST NAME}
    ${Current_Loop}  Evaluate  ${MaxLoopNum}-1
    FOR    ${INDEX}    IN RANGE    1    ${MaxLoopNum}
        Print Loop Info  ${INDEX}  ${Current_Loop}
        Step  1  load user mode  ${remote_shell_load_sdk}
        Step  2  source cmd function  ${PAM4_400G_32}  32
        Step  3  check port status  ${PAM4_400G_32}  32
        Step  4  enable prbs tx
        Step  5  enable prbs rx and check counter
        Step  6  check prbs ber
        Step  7  exit user mode
        Step  8  load user mode  ${remote_shell_load_sdk} ${PAM4_100G_128}
        Step  9  ber check
        Step  10  exit user mode
        Step  11  load user mode  ${remote_shell_load_sdk} ${NRZ_100G_32}
        Step  12  check port status  ${NRZ_100G_32}  32
        Step  13  prbs tx 31 25g
        Step  14  prbs rx 31 25g 5  32
        Step  15  sleep 5S
        Step  16  stress prbs rx  ${prbs_rx_31_25g_43200_cmd}  32
        Step  17  exit user mode
        Step  18  load user mode  ${remote_shell_load_sdk} ${NRZ_40G_32}
        Step  19  check port status  ${NRZ_40G_32}  32
        Step  20  prbs tx 31 10g
        Step  21  prbs rx 31 10g 5  32
        Step  22  sleep 5S
        Step  23  stress prbs rx  ${prbs_rx_31_10g_43200_cmd}  32
        Step  24  exit user mode
        Step  25  load user mode  ${remote_shell_load_sdk} ${NRZ_25G_128}
        Step  26  check port status  ${NRZ_25G_128}  128
        Step  27  prbs tx 31 25g
        Step  28  prbs rx 31 25g 5  128
        Step  29  sleep 5S
        Step  30  stress prbs rx  ${prbs_rx_31_25g_43200_cmd}  128
        Step  31  exit user mode
        Step  32  load user mode  ${remote_shell_load_sdk} ${NRZ_10G_128}
        Step  33  check port status  ${NRZ_10G_128}  128
        Step  34  prbs tx 31 10g
        Step  35  prbs rx 31 10g 5  128
        Step  36  sleep 5S
        Step  37  stress prbs rx  ${prbs_rx_31_10g_43200_cmd}  128
        Step  38  exit user mode
    END