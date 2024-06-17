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
FENGHUANGV2_STRESS_TC_00_Diag_Initialize_And_Version_Check
    [Documentation]  This test Initialize and Version Check
    [Tags]  FENGHUANGV2_STRESS_TC_00_Diag_Initialize_And_Version_Check  fenghuangv2
    [Timeout]  60 min 00 seconds
    [Setup]  KapokCommonLib.boot Into Onie Rescue Mode
    Step  1  Check network connectivity  ${ONIE_RESCUE_MODE}
    Step  2  fhv2 Diag download Images And Recovery DiagOS
    Step  3  Self Update Onie  new
    Step  4  KapokStressLib.power Cycle To DiagOS
    Step  5  check version before the test
    Step  6  check driver version  ${drive_pattern}

FENGHUANGV2_STRESS_TC_03_ONIE_FW_Update_Stress_Test
    [Documentation]  This test checks the ONIE Updater Stress Test
    [Tags]  common  FENGHUANGV2_STRESS_TC_03_ONIE_FW_Update_Stress_Test  fenghuangv2
    [Timeout]  180 min 00 seconds
    ${MaxLoopNum}=  KapokCommonLib.get data from yaml
    ...  name=${TEST NAME}
    ${Current_Loop}  Evaluate  ${MaxLoopNum}-1
    FOR    ${INDEX}    IN RANGE    1    ${MaxLoopNum}
        Print Loop Info  ${INDEX}  ${Current_Loop}
        Step  1  Self Update Onie  old
        Step  2  Self Update Onie  new
    END

FENGHUANGV2_STRESS_TC_04_CPLD/FPGA_Updates_Stress_Test
    [Documentation]  This test checks that CPLD can be updated under ONIE mode
    [Tags]  common  FENGHUANGV2_STRESS_TC_04_CPLD/FPGA_Updates_Stress_Test  fenghuangv2
    [Timeout]  180 min 00 seconds
    ${MaxLoopNum}=  KapokCommonLib.get data from yaml
    ...  name=${TEST NAME}
    ${Current_Loop}  Evaluate  ${MaxLoopNum}-1
    FOR    ${INDEX}    IN RANGE    1    ${MaxLoopNum}
        Print Loop Info  ${INDEX}  ${Current_Loop}
        Step  1  KapokCommonLib.boot Into Onie Rescue Mode
        Step  2  Check network connectivity  ${ONIE_RESCUE_MODE}
        Step  3  fenghuangv2 upgrade cpld
        Step  4  KapokCommonLib.power Cycle To Onie Rescue Mode
        Step  5  check cpld version
    END

FENGHUANGV2_STRESS_TC_05_Warm_Reboot_Stress_Test
    [Documentation]  This test checks each of reboot cycle work normally.
    [Tags]  common  FENGHUANGV2_STRESS_TC_05_Warm_Reboot_Stress_Test  fenghuangv2
    [Timeout]  180 min 00 seconds
    ${MaxLoopNum}=  KapokCommonLib.get data from yaml
    ...  name=${TEST NAME}
    ${Current_Loop}  Evaluate  ${MaxLoopNum}-1
    FOR    ${INDEX}    IN RANGE    1    ${MaxLoopNum}
        Print Loop Info  ${INDEX}  ${Current_Loop}
        Step  1  warm stress reboot
        Step  2  KapokStressLib.verify onie and cpld version  new
        Step  3  scan HW Info
    END

FENGHUANGV2_STRESS_TC_06_Detect_PCIE_Device_Test
    [Documentation]  This test detect PCIE device ensure PCIE device be found every time
    [Tags]     FENGHUANGV2_STRESS_TC_06_Detect_PCIE_Device_Test    fenghuangv2
    [Timeout]  20 min 00 seconds
    [Setup]   KapokCommonLib.Boot into Diag OS MOde
     Step  1  change to sdk path
    ${Current_Loop}  Evaluate  10-1
    FOR    ${INDEX}    IN RANGE    0   10
       Print Loop Info  ${INDEX}  ${Current_Loop}
       Step  2  Detect PCIE device
    END


FENGHUANGV2_STRESS_TC_08_Power_Cycle_Test
    [Documentation]  This test checks whether the system will boot up every time after power-cycle
    [Tags]     common  FENGHUANGV2_STRESS_TC_08_Power_Cycle_Test  fenghuangv2
    [Timeout]  240 min 00 seconds
    ${MaxLoopNum}=  KapokCommonLib.get data from yaml
    ...  name=${TEST NAME}
    ${Current_Loop}  Evaluate  ${MaxLoopNum}-1
    FOR    ${INDEX}    IN RANGE    1    ${MaxLoopNum}
        Print Loop Info  ${INDEX}  ${Current_Loop}
        Step  1  KapokCommonLib.power Cycle To DiagOS
    END

FENGHUANGV2_STRESS_TC_09_DDR_Stress_Test
    [Documentation]  This test checks DDR function
    [Tags]     common  FENGHUANGV2_STRESS_TC_09_DDR_Stress_Test  fenghuangv2
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

FENGHUANGV2_STRESS_TC_10_SSD_STRESS_TEST
    [Documentation]  This test checks SSD function
    [Tags]     common  FENGHUANGV2_STRESS_TC_10_SSD_STRESS_TEST  fenghuangv2
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

FENGHUANGV2_STRESS_TC_11_I2C_BUS_SCAN_STRESS_TEST
    [Documentation]  This test checks access all the I2C end-point devices successfully
    [Tags]     common  FENGHUANGV2_STRESS_TC_11_I2C_BUS_SCAN_STRESS_TEST  fenghuangv2
    [Timeout]  360 min 00 seconds
    Step  1  KapokCommonLib.power Cycle To DiagOS
    ${MaxLoopNum}=  KapokCommonLib.get data from yaml
    ...  name=${TEST NAME}
    ${Current_Loop}  Evaluate  ${MaxLoopNum}-1
    FOR    ${INDEX}    IN RANGE    1    ${MaxLoopNum}
        Print Loop Info  ${INDEX}  ${Current_Loop}
        Step  2  I2C bus scan stress test
    END

FENGHUANGV2_STRESS_TC_12_DIAG_ALL_TEST
    [Documentation]  This test is to run all diagnostic test
    [Tags]     common  FENGHUANGV2_STRESS_TC_12_DIAG_ALL_TEST  fenghuangv2
    [Timeout]  180 min 00 seconds
    Step  1  KapokCommonLib.boot Into DiagOS Mode
    ${MaxLoopNum}=  KapokCommonLib.get data from yaml
    ...  name=${TEST NAME}
    ${Current_Loop}  Evaluate  ${MaxLoopNum}-1
    Step  2  change phy config file
    FOR    ${INDEX}    IN RANGE    1    ${MaxLoopNum}
        Print Loop Info  ${INDEX}  ${Current_Loop}
        Step  3  run all diagnostic test
    END

FENGHUANGV2_STRESS_TC_13_QDD_PORT_I2C_TEST
    [Documentation]  This test is to run all diagnostic test
    [Tags]     common  FENGHUANGV2_STRESS_TC_13_QDD_PORT_I2C_TEST  fenghuangv2
    [Timeout]  60 min 00 seconds
    ${MaxLoopNum}=  KapokCommonLib.get data from yaml
    ...  name=${TEST NAME}
    ${Current_Loop}  Evaluate  ${MaxLoopNum}-1
    FOR    ${INDEX}    IN RANGE    1    ${MaxLoopNum}
        Print Loop Info  ${INDEX}  ${Current_Loop}
        Step  1  KapokCommonLib.power Cycle To DiagOS
        Step  2  run sfp all test  ${run_sfp_cmd}  ${D_1_cmd_pattern}
        Step  3  check speed profile  ${D_2_cmd}
        Step  4  run sfp all test  ${run_sfp_cmd}  ${D_2_cmd_pattern}
        Step  5  check speed profile  ${D_1_cmd}
        Step  6  run sfp all test  ${run_sfp_cmd}  ${D_1_cmd_pattern}
    END

FENGHUANGV2_STRESS_TC_14_ASC10_FW_UPDATE_TEST
    [Documentation]  This test is to run all diagnostic test
    [Tags]     common  FENGHUANGV2_STRESS_TC_14_ASC10_FW_UPDATE__TEST  fenghuangv2
    [Timeout]  60 min 00 seconds
    ${MaxLoopNum}=  KapokCommonLib.get data from yaml
    ...  name=${TEST NAME}
    ${Current_Loop}  Evaluate  ${MaxLoopNum}-1
    FOR    ${INDEX}    IN RANGE    1    ${MaxLoopNum}
        Print Loop Info  ${INDEX}  ${Current_Loop}
        Step  1  KapokCommonLib.power Cycle To DiagOS
        Step  2  run asc update test
        Step  3  KapokCommonLib.power Cycle To DiagOS
        Step  4  check asc version
    END

FENGHUANGV2_STRESS_TC_15_Soft_Reset_Stress_Test
    [Documentation]  This test checks PCIe bus status after soft reset in all cycles
    [Tags]  common  FENGHUANGV2_STRESS_TC_15_Soft_Reset_Stress_Test  fenghuangv2
    [Timeout]  180 min 00 seconds
    ${MaxLoopNum}=  KapokCommonLib.get data from yaml
    ...  name=${TEST NAME}
    ${Current_Loop}  Evaluate  ${MaxLoopNum}-1
    FOR    ${INDEX}    IN RANGE    1    ${MaxLoopNum}
        Print Loop Info  ${INDEX}  ${Current_Loop}
        Step  1  soft reset   ${soft_reset_cmd}
        Step  2  run pci all test
    END

FENGHUANGV2_STRESS_TC_16_1-16byte_burst_mode_with_I2C_speed_400K/1M
    [Documentation]  This test is to run qsfp test
    [Tags]     common  FENGHUANGV2_STRESS_TC_16_1-16byte_burst_mode_with_I2C_speed_400K/1M  fenghuangv2
    [Timeout]  180 min 00 seconds
    [Setup]    KapokCommonLib.boot Into Onie Install Mode
    Step  1  sfp Stress Test  ${sfp_stress_test_cmd_ist}  ${sfp_stress_test_patterns_dict}
    Step  2  check cmd no output  ${change_profile_cmd2}
    Step  3  sfp Stress Test  ${sfp_stress_test_cmd_ist}  ${sfp_stress_test_patterns_dict}
    Step  4  check cmd no output  ${change_profile_cmd1}

FENGHUANGV2_STRESS_TC_17_128-byte_burst_mode_with_I2C_speed_400K/1M
    [Documentation]  This test is to run qsfp test
    [Tags]     common  FENGHUANGV2_STRESS_TC_17_128-byte_burst_mode_with_I2C_speed_400K/1M  fenghuangv2
    [Timeout]  20 min 00 seconds
    [Setup]    KapokCommonLib.boot Into Onie Install Mode
    Step  1  sfp Stress Test  ${sfp_burst_mode_test_cmd_list}  ${sfp_stress_test_patterns_dict}
    Step  2  check cmd no output  ${change_profile_cmd2}
    Step  3  sfp Stress Test  ${sfp_burst_mode_test_cmd_list}  ${sfp_stress_test_patterns_dict}
    Step  4  check cmd no output  ${change_profile_cmd1}

FENGHUANGV2_STRESS_TC_18_128-byte_32_Multi_threads_I2C_buses_with_speed_400K/1M
    [Documentation]  This test is to run qsfp test
    [Tags]     common  FENGHUANGV2_STRESS_TC_18_128-byte_32_Multi_threads_I2C_buses_with_speed_400K/1M  fenghuangv2
    [Timeout]  20 min 00 seconds
    [Setup]    KapokCommonLib.boot Into Onie Install Mode
    Step  1  sfp Stress Test  ${sfp_multi_threads_test_cmd_list}  ${sfp_stress_test_patterns_dict}
    Step  2  check cmd no output  ${change_profile_cmd2}
    Step  3  sfp Stress Test  ${sfp_multi_threads_test_cmd_list}  ${sfp_stress_test_patterns_dict}
    Step  4  check cmd no output  ${change_profile_cmd1}

FENGHUANGV2_STRESS_TC_19_UBOOT_MGMT_TFTP_STRESS_TEST
    [Documentation]  This test is to check U-boot MGMT port tftp download stress test
    [Tags]     common  FENGHUANGV2_STRESS_TC_19_UBOOT_MGMT_TFTP_STRESS_TEST  fenghuangv2
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

FENGHUANGV2_STRESS_TC_20_PCIE_Test_With_PowerCycle
   [Documentation]  This test checks PCIe bus status after soft reset in all cycles
   [Tags]  common   FENGHUANGV2_STRESS_TC_20_PCIE_Test_With_PowerCycle  fenghuangv2
   [Timeout]  180 min 00 seconds
   [Setup]    KapokCommonLib.boot Into Onie Install Mode
   ${MaxLoopNum}=  KapokCommonLib.get data from yaml
   ...  name=${TEST NAME}
   ${Current_Loop}  Evaluate  ${MaxLoopNum}-1
   FOR    ${INDEX}    IN RANGE    1    ${MaxLoopNum}
        Print Loop Info  ${INDEX}  ${Current_Loop}
        Step  1  Read Write Scratch Pad Register
        Step  2  KapokCommonLib.power Cycle To DiagOS
   END

FENGHUANGV2_STRESS_TC_21_ReInit_SDK_Stress_Test
    [Documentation]  This test checks every SDK init, port link status can be displayed correctly and traffic no loss package for 1000 times
    [Tags]  common  FENGHUANGV2_STRESS_TC_21_ReInit_SDK_Stress_Test  fenghuangv2
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

FENGHUANGV2_STRESS_TC_22_PRBS_SDK_Stress_Test
    [Documentation]  This test checks all kinds of PRBS for 24 hrs
    [Tags]  common  FENGHUANGV2_STRESS_TC_22_PRBS_SDK_Stress_Test  fenghuangv2
    [Timeout]  180 min 00 seconds
    [Setup]    change dir to sdk path
    ${MaxLoopNum}=  KapokCommonLib.get data from yaml
    ...  name=${TEST NAME}
    ${Current_Loop}  Evaluate  ${MaxLoopNum}-1
    FOR    ${INDEX}    IN RANGE    1    ${MaxLoopNum}
        Print Loop Info  ${INDEX}  ${Current_Loop}
        Step  1   load user mode  ${remote_shell_load_sdk} ${PAM4_400G_32}
        Step  2   check ber levels  ${PAM4_400G_32}  32
        Step  3   exit user mode
        Step  4   load user mode  ${remote_shell_load_sdk} ${PAM4_100G_128}
        Step  5   check ber levels  ${PAM4_100G_128}  128
        Step  6   exit user mode
        Step  7   load user mode  ${remote_shell_load_sdk} ${NRZ_100G_32}
        Step  8   check ber levels  ${NRZ_100G_32}  32
        Step  9   exit user mode
        Step  10  load user mode  ${remote_shell_load_sdk} ${NRZ_40G_32}
        Step  11  check ber levels  ${NRZ_40G_32}  32
        Step  12  exit user mode
        Step  13  load user mode  ${remote_shell_load_sdk} ${NRZ_25G_128}
        Step  14  check ber levels  ${NRZ_25G_128}  128
        Step  15  exit user mode
        Step  16  load user mode  ${remote_shell_load_sdk} ${NRZ_10G_128}
        Step  17  check ber levels  ${NRZ_10G_128}  128
        Step  18  exit user mode
    END




BSP_10.2.15.2_Uboot rov_bits_Stress_Test
    [Documentation]  The purpose of this test is to check U-boot rov_bits stress test
    [Tags]   BSP_10.2.15.2_Uboot rov_bits_Stress_Test  fenghuangv2   
    [Timeout]  50 min 00 seconds
    Step  1  uboot rov bits test  a=5


ONIE_11.6_Bootcmd_Stress_Test
    [Documentation]   To verify the system can run bootcmd successfully under stress.
    [Tags]   ONIE_11.6_Bootcmd_Stress_Test   fenghuangv2  
    [Timeout]  50 min 00 seconds
    Step  1  uboot rov bits test  a=10 




ONIE_11.5_Reboot_Stress_Test
    [Documentation]   To test Reboot Stress Test
    [Tags]   ONIE_11.5_Reboot_Stress_Test   fenghuangv2
    [Timeout]  25 min 00 seconds
     Step  1  verify device tests


FENGHUANGV2_STRESS_TC_23_XE_Port_Test
    [Documentation]  This test to check XE Port Loopack Snake Stress Test
    [Tags]  common  FENGHUANGV2_STRESS_TC_23_XE_Port_Test  fenghuangv2
    ${Current_Loop}  Evaluate  10-1
    FOR    ${INDEX}    IN RANGE    0   10
       Print Loop Info  ${INDEX}  ${Current_Loop}
       Step  1  KapokCommonLib.power Cycle To DiagOS
       Step  2  change to sdk path
       Step  3  auto load user
       Step  4  clear counters
       Step  5  console check
       Step  6  show port counter
    END

