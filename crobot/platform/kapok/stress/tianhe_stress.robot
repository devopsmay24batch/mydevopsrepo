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
tianhe_STRESS_TC_00_Diag_Initialize_And_Version_Check
    [Documentation]  This test Initialize and Version Check
    [Tags]  tianhe_STRESS_TC_00_Diag_Initialize_And_Version_Check  tianhe
    [Timeout]  60 min 00 seconds
	[Setup]  KapokCommonLib.boot Into DiagOS Mode
    Step  1  get dhcp ip
    Step  2  update diagos and onie test
    Step  3  check version before the test
    Step  4  check driver version  ${drive_pattern_tianhe}


tianhe_STRESS_DIAG_TC_01_PCIE_Test_With_PowerCycle
   [Documentation]  This test checks diag PCIe bus status after soft reset in all cycles
   [Tags]  common   tianhe_STRESS_DIAG_TC_01_PCIE_Test_With_PowerCycle  tianhe  diag  bsp
   [Setup]    KapokCommonLib.boot Into DiagOS Mode
   ${MaxLoopNum}=  KapokCommonLib.get data from yaml
   ...  name=${TEST NAME}
   ${Current_Loop}  Evaluate  ${MaxLoopNum}-1
   FOR    ${INDEX}    IN RANGE    1    ${MaxLoopNum}
        Print Loop Info  ${INDEX}  ${Current_Loop}
        Step  1  check pcie stress test  ${scratchTool}  ${PCIeTool}
        Step  2  KapokCommonLib.power Cycle To DiagOS
   END

tianhe_STRESS_DIAG_TC_02_Detect_PCIE_Device_Test
   [Documentation]  This test checks diag Detect PCIE Device Test
   [Tags]  common   tianhe_STRESS_DIAG_TC_02_Detect_PCIE_Device_Test  tianhe  diag
   [Setup]    KapokCommonLib.boot Into DiagOS Mode
   Step  1  switch diag path  ${SDK_PATH}
   ${MaxLoopNum}=  KapokCommonLib.get data from yaml
   ...  name=${TEST NAME}
   ${Current_Loop}  Evaluate  ${MaxLoopNum}-1
   FOR    ${INDEX}    IN RANGE    1    ${MaxLoopNum}
        Print Loop Info  ${INDEX}  ${Current_Loop}
        Step  1  check lspci test  ${LSPCI_TOOL}
        Step  2  load user mode tianhe  ${remote_shell_load_sdk}  ${PAM4_400G_32}
        Step  3  show port status test  ${show_port_info}
        Step  4  exit sdk env in diag side
   END

tianhe_STRESS_DIAG_TC_03_Power_Cycle_Test
   [Documentation]  This test checks diag power cycle test
   [Tags]  common   tianhe_STRESS_DIAG_TC_03_Power_Cycle_Test  tianhe  diag
   [Setup]    KapokCommonLib.boot Into DiagOS Mode
   ${MaxLoopNum}=  KapokCommonLib.get data from yaml
   ...  name=${TEST NAME}
   ${Current_Loop}  Evaluate  ${MaxLoopNum}-1
   FOR    ${INDEX}    IN RANGE    1    ${MaxLoopNum}
        Print Loop Info  ${INDEX}  ${Current_Loop}
        Step  1  KapokCommonLib.power Cycle To DiagOS
        Step  2  check and scan some devices info
   END

tianhe_STRESS_DIAG_TC_04_DDR_Stress_Test
    [Documentation]  This test checks DDR function
    [Tags]     common  tianhe_STRESS_DIAG_TC_04_DDR_Stress_Test  tianhe  diag
    [Setup]    KapokCommonLib.boot Into DiagOS Mode
    ${MaxLoopNum}=  KapokCommonLib.get data from yaml
    ...  name=${TEST NAME}
    Step  1  create and switch stress path  ${STRESS_PATH}
    Step  2  download snake file  ${DDR_SSD_TOOL_LST}
    Step  2  unzip ddr ssd tool  ${DDR_SSD_TOOL_LST}
    Step  3  run ddr stress test  ${DDR_TOOL}  ${MaxLoopNum}  ${DDR_LOG}

tianhe_STRESS_DIAG_TC_05_SSD_STRESS_TEST
    [Documentation]  This test checks SSD function
    [Tags]     common  tianhe_STRESS_DIAG_TC_05_SSD_STRESS_TEST  tianhe  diag
    [Setup]    KapokCommonLib.boot Into DiagOS Mode
    ${MaxLoopNum}=  KapokCommonLib.get data from yaml
    ...  name=${TEST NAME}
    Step  1  switch diag path  ${SSD_PATH}
    Step  2  modify ssd loop and run test  ${SSD_CMD}  ${MaxLoopNum}  ${ssdPatternLst}

tianhe_STRESS_DIAG_TC_06_I2C_Bus_Scan_Stress_Test
   [Documentation]  This test checks diag i2c bus scan test
   [Tags]  common   tianhe_STRESS_DIAG_TC_06_I2C_Bus_Scan_Stress_Test  tianhe  diag
   [Setup]    KapokCommonLib.boot Into DiagOS Mode
   ${MaxLoopNum}=  KapokCommonLib.get data from yaml
   ...  name=${TEST NAME}
   ${Current_Loop}  Evaluate  ${MaxLoopNum}-1
   FOR    ${INDEX}    IN RANGE    1    ${MaxLoopNum}
        Print Loop Info  ${INDEX}  ${Current_Loop}
        Step  1  switch diag path  ${diag_tools_path}
        Step  2  run diag tool test  ${I2C_TOOL}  ${I2C_PATTERN}  I2c_Bus_Scan
   END

tianhe_STRESS_DIAG_TC_07_ALL_Test
   [Documentation]  This test checks diag all test
   [Tags]  common   tianhe_STRESS_DIAG_TC_07_ALL_Test  tianhe  diag
   [Setup]    KapokCommonLib.boot Into DiagOS Mode
   Step  1  change phy config file
   ${MaxLoopNum}=  KapokCommonLib.get data from yaml
   ...  name=${TEST NAME}
   ${Current_Loop}  Evaluate  ${MaxLoopNum}-1
   FOR    ${INDEX}    IN RANGE    1    ${MaxLoopNum}
        Print Loop Info  ${INDEX}  ${Current_Loop}
        Step  1  switch diag path  ${diag_tools_path}
        Step  2  run diag all test  ${DIAG_ALL_TOOL}
        Step  3  diag reboot test
   END

tianhe_STRESS_DIAG_TC_08_QDD_Port_I2C_Stress_Test
   [Documentation]  This test checks QDD port i2c stress test
   [Tags]  common   tianhe_STRESS_DIAG_TC_08_QDD_Port_I2C_Stress_Test  tianhe  diag
   [Setup]    KapokCommonLib.boot Into DiagOS Mode
   Step  1  switch diag path  ${diag_tools_path}
   ${MaxLoopNum}=  KapokCommonLib.get data from yaml
   ...  name=${TEST NAME}
   ${Current_Loop}  Evaluate  ${MaxLoopNum}-1
   FOR    ${INDEX}    IN RANGE    1    ${MaxLoopNum}
        Print Loop Info  ${INDEX}  ${Current_Loop}
        Step  1  set i2c bus speed profile  ${D_1_cmd}
        Step  2  run diag tool test  ${run_sfp_cmd}  ${SFP_PATTERN}  QDD_Port_I2c_Stress
        Step  3  set i2c bus speed profile  ${D_2_cmd}
        Step  4  run diag tool test  ${run_sfp_cmd}  ${SFP_PATTERN}  QDD_Port_I2c_Stress
   END

tianhe_STRESS_DIAG_TC_09_ASC10_FW_Update_Stress_Test
   [Documentation]  This test checks QDD port i2c stress test
   [Tags]  common   tianhe_STRESS_DIAG_TC_09_ASC10_FW_Update_Stress_Test  tianhe  diag
   [Setup]    KapokCommonLib.boot Into DiagOS Mode
   ${MaxLoopNum}=  KapokCommonLib.get data from yaml
   ...  name=${TEST NAME}
   ${Current_Loop}  Evaluate  ${MaxLoopNum}-1
   FOR    ${INDEX}    IN RANGE    1    ${MaxLoopNum}
        Print Loop Info  ${INDEX}  ${Current_Loop}
        Step  1  switch diag path  ${FW_PATH}
        Step  2  asc10 fw update test  ${ASC_FW_LST}  ${ASC_PATTERN}
        Step  3  KapokCommonLib.power Cycle To DiagOS
        Step  4  check asc10 fw version test  ${ASC10_VER_LST}
   END

########################################################################################
tianhe_STRESS_BSP_TC_01_CPLD_FPGA_Update_Stress_Test
   [Documentation]  This test checks bsp cpld fpga update test
   [Tags]  common   tianhe_STRESS_BSP_TC_01_CPLD_FPGA_Update_Stress_Test  tianhe  bsp
   [Setup]    KapokCommonLib.boot Into DiagOS Mode
   ${MaxLoopNum}=  KapokCommonLib.get data from yaml
   ...  name=${TEST NAME}
   ${Current_Loop}  Evaluate  ${MaxLoopNum}-1
   FOR    ${INDEX}    IN RANGE    1    ${MaxLoopNum}
        Print Loop Info  ${INDEX}  ${Current_Loop}
        Step  1  switch diag path  ${FW_PATH}
        Step  2  cpld and fpga fw update test  ${CPLD_FPGA_LST}
        Step  3  KapokCommonLib.power Cycle To DiagOS
        Step  4  check cpld fw version test  ${get_versions_cmd}
   END

tianhe_STRESS_BSP_TC_02_Uboot_rov_bits_Stress_Test
   [Documentation]  This test checks bsp uboot rov bits stress test
   [Tags]  common   tianhe_STRESS_BSP_TC_02_Uboot_rov_bits_Stress_Test  tianhe  bsp
   [Setup]    KapokCommonLib.bootIntoOnieInstallMode
   ${MaxLoopNum}=  KapokCommonLib.get data from yaml
   ...  name=${TEST NAME}
   ${Current_Loop}  Evaluate  ${MaxLoopNum}-1
   FOR    ${INDEX}    IN RANGE    1    ${MaxLoopNum}
        Print Loop Info  ${INDEX}  ${Current_Loop}
        Step  1  run uboot rov bits test  ${UBOOT_ROV_CMD}
        Step  2  onie reboot to install mode
   END


########################################################################################
tianhe_STRESS_SDK_TC_01_XE_Port_Stress_Test
   [Documentation]  This test checks sdk XE port stress test
   [Tags]  common   tianhe_STRESS_SDK_TC_01_XE_Port_Stress_Test  tianhe  sdk
   [Setup]    KapokCommonLib.bootIntoOnieInstallMode
   Step  1  switch sdk folder path  ${SDK_PATH}
   Step  2  exit sdk shell mode  ${SDK_SHELL_EXIT}
   ${MaxLoopNum}=  KapokCommonLib.get data from yaml
   ...  name=${TEST NAME}
   ${Current_Loop}  Evaluate  ${MaxLoopNum}-1
   FOR    ${INDEX}    IN RANGE    1    ${MaxLoopNum}
        Print Loop Info  ${INDEX}  ${Current_Loop}
        Step  1  run sdk xe port stress test  ${remote_shell_load_sdk}  ${PAM4_400G_32}  ${CONSOLE_LST}  ${SHOW_COUNTER_CMD}
        Step  2  check xfi0 counter result  ${XFI_TOOL1}  ${XFI_TOOL2}
   END


tianhe_STRESS_SDK_TC_02_ReInit_SDK_Stress_Test
    [Documentation]  This test checks every SDK init test
    [Tags]  common  tianhe_STRESS_SDK_TC_02_ReInit_SDK_Stress_Test  tianhe  sdk
    [Setup]    KapokCommonLib.bootIntoOnieInstallMode
    ${MaxLoopNum}=  KapokCommonLib.get data from yaml
    ...  name=${TEST NAME}
    Step  1  switch sdk folder path  ${SDK_PATH}
    Step  2  exit sdk shell mode  ${SDK_SHELL_EXIT}
    Step  3  run sdk reinit stress test  ${SDK_INIT_TOOL}  ${SDK_INIT_OPTION}  ${MaxLoopNum}


tianhe_STRESS_SDK_TC_03_All_Ports_Enable_Disable_Stress_Test
   [Documentation]  This test checks sdk port enable or disable test
   [Tags]  common   tianhe_STRESS_SDK_TC_03_All_Ports_Enable_Disable_Stress_Test  tianhe  sdk
   [Setup]    KapokCommonLib.bootIntoOnieInstallMode
   Step  1  switch sdk folder path  ${SDK_PATH}
   Step  2  load user mode tianhe  ${remote_shell_load_sdk}  ${PAM4_400G_32}
   Step  3  show port status test  ${show_port_info}
   Step  4  ifcs clear port counter  ${CLEAR_COUNTER_LST}
   Step  5  show port status test  ${show_port_info}
   ${MaxLoopNum}=  KapokCommonLib.get data from yaml
   ...  name=${TEST NAME}
   ${Current_Loop}  Evaluate  ${MaxLoopNum}-1
   FOR    ${INDEX}    IN RANGE    1    ${MaxLoopNum}
        Print Loop Info  ${INDEX}  ${Current_Loop}
        Step  6  sdk snake traffic test  ${TRAFFIC_LST}
        Step  7  disable or enable port test  ${PORT_DISABLE_TOOL}
        Step  8  check snake port status test  ${show_port_info}  DOWN
        Step  9  disable or enable port test  ${PORT_ENABLE_TOOL}
        Step  10  check snake port status test  ${show_port_info}  UP
        Step  11  ifcs clear port counter  ${CLEAR_CMD_LST}
        Step  12  show port status test  ${show_port_info}
   END
   [Teardown]  exit sdk env in onie side

tianhe_STRESS_SDK_TC_04_Power_Cycle_Stress_Test
   [Documentation]  This test checks sdk power cycle test
   [Tags]  common   tianhe_STRESS_SDK_TC_04_Power_Cycle_Stress_Test  tianhe  sdk
   [Setup]    KapokCommonLib.bootIntoOnieInstallMode
   ${MaxLoopNum}=  KapokCommonLib.get data from yaml
   ...  name=${TEST NAME}
   ${Current_Loop}  Evaluate  ${MaxLoopNum}-1
   FOR    ${INDEX}    IN RANGE    1    ${MaxLoopNum}
        Print Loop Info  ${INDEX}  ${Current_Loop}
        Step  1  switch sdk folder path  ${SDK_PATH}
        Step  2  load user mode tianhe  ${remote_shell_load_sdk}  ${PAM4_400G_32}
        Step  3  shell sleep test  ${SHELL_SLEEP_TOOL}  ${SLEEP10_OPTION}
        Step  4  show port status test  ${show_port_info}
        Step  5  ifcs clear port counter  ${CLEAR_COUNTER_LST}
        Step  6  show port status test  ${show_port_info}
        Step  7  sdk snake traffic test  ${TRAFFIC_LST2}
        Step  8  check devport counter  ${IFCS_SHOW_TOOL}  ${SNAKE_UNCONFIG}
        Step  9  exit sdk env in onie side
        Step  10  KapokCommonLib.power Cycle To Onie Install Mode
   END

##################################################################################################
tianhe_STRESS_ONIE_TC_01_ONIE_Idle_Test
   [Documentation]  This test checks onie idle test
   [Tags]  common   tianhe_STRESS_ONIE_TC_01_ONIE_Idle_Test  tianhe  onie
   [Setup]    KapokCommonLib.bootIntoOnieInstallMode
   ${MaxLoopNum}=  KapokCommonLib.get data from yaml
   ...  name=${TEST NAME}
   Step  1  switch sdk folder path  ${diag_tools_path}
   Step  2  onie idle stress test  ${RTC_TOOL}  ${MaxLoopNum}

tianhe_STRESS_ONIE_TC_02_ONIE_FW_Update_Stress_Test
    [Documentation]  This test checks the ONIE Updater Stress Test
    [Tags]  common  tianhe_STRESS_ONIE_TC_02_ONIE_FW_Update_Stress_Test  tianhe  onie
    ${MaxLoopNum}=  KapokCommonLib.get data from yaml
    ...  name=${TEST NAME}
    ${Current_Loop}  Evaluate  ${MaxLoopNum}-1
    FOR    ${INDEX}    IN RANGE    1    ${MaxLoopNum}
        Print Loop Info  ${INDEX}  ${Current_Loop}
        Step  1  KapokCommonLib.bootIntoOnieRescueMode
        Step  2  check dhcp ip in onie
        Step  3  check onie version test  ${get_versions_cmd}  new
        Step  4  KapokStressLib.onie self update  old
        Step  5  check onie all fw version  ${get_versions_cmd}  old
        Step  6  KapokCommonLib.boot into Onie Rescue mode
        Step  7  check dhcp ip in onie
        Step  8  check onie version test  ${get_versions_cmd}  old
        Step  9  KapokStressLib.onie self update  new
        Step  10  check onie all fw version  ${get_versions_cmd}  new
    END

tianhe_STRESS_ONIE_TC_03_Warm_Action_Stress_Test
    [Documentation]  This test checks the ONIE warm action Stress Test
    [Tags]  common  tianhe_STRESS_ONIE_TC_03_Warm_Action_Stress_Test  tianhe  onie
    [Setup]    KapokCommonLib.bootIntoOnieInstallMode
    ${MaxLoopNum}=  KapokCommonLib.get data from yaml
    ...  name=${TEST NAME}
    ${Current_Loop}  Evaluate  ${MaxLoopNum}-1
    FOR    ${INDEX}    IN RANGE    1    ${MaxLoopNum}
        Print Loop Info  ${INDEX}  ${Current_Loop}
        Step  1  switch sdk folder path  ${diag_tools_path}
        Step  2  check diag tool test  ${DIAG_TOOL_LST}  ${DIAG_PATTERN_LST}
        Step  3  onie reboot to install mode  warm-reboot
    END

tianhe_STRESS_ONIE_TC_04_Cold_Action_Stress_Test
    [Documentation]  This test checks the ONIE cold action Stress Test
    [Tags]  common  tianhe_STRESS_ONIE_TC_04_Cold_Action_Stress_Test  tianhe  onie
    [Setup]    KapokCommonLib.bootIntoOnieInstallMode
    ${MaxLoopNum}=  KapokCommonLib.get data from yaml
    ...  name=${TEST NAME}
    ${Current_Loop}  Evaluate  ${MaxLoopNum}-1
    FOR    ${INDEX}    IN RANGE    1    ${MaxLoopNum}
        Print Loop Info  ${INDEX}  ${Current_Loop}
        Step  1  switch sdk folder path  ${diag_tools_path}
        Step  2  check diag tool test  ${DIAG_TOOL_LST}  ${DIAG_PATTERN_LST}
        Step  3  onie reboot to install mode
    END

tianhe_STRESS_ONIE_TC_05_Bootcmd_Stress_Test
    [Documentation]  This test checks the ONIE bootcmd Stress Test
    [Tags]  common  tianhe_STRESS_ONIE_TC_05_Bootcmd_Stress_Test  tianhe  onie
    [Setup]    KapokCommonLib.bootIntoOnieInstallMode
    ${MaxLoopNum}=  KapokCommonLib.get data from yaml
    ...  name=${TEST NAME}
    ${Current_Loop}  Evaluate  ${MaxLoopNum}-1
    FOR    ${INDEX}    IN RANGE    1    ${MaxLoopNum}
        Print Loop Info  ${INDEX}  ${Current_Loop}
        Step  1  check fw setenv test  ${FW_SETENV_TOOL}
        Step  2  onie reboot to install mode
    END

tianhe_STRESS_ONIE_TC_06_Power_Cycle_Stress_Test
    [Documentation]  This test checks the ONIE power cycle Stress Test
    [Tags]  common  tianhe_STRESS_ONIE_TC_06_Power_Cycle_Stress_Test  tianhe  onie
    ${MaxLoopNum}=  KapokCommonLib.get data from yaml
    ...  name=${TEST NAME}
    ${Current_Loop}  Evaluate  ${MaxLoopNum}-1
    FOR    ${INDEX}    IN RANGE    1    ${MaxLoopNum}
        Print Loop Info  ${INDEX}  ${Current_Loop}
        Step  1  KapokCommonLib.powerCycleToOnieRescueMode
        Step  2  check ssd smartctl test  ${SMARTCTL_TOOL}  ${SSD_SPEED_PATTERN}
    END






