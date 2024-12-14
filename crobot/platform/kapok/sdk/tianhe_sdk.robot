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
tianhe_SDK_TC_00_Diag_Initialize_And_Version_Check
    [Documentation]  This test Initialize and Version Check
    [Tags]  tianhe_SDK_TC_00_Diag_Initialize_And_Version_Check  tianhe
    [Timeout]  60 min 00 seconds
	[Setup]  boot Into DiagOS Mode
    Step  1  get dhcp ip
    Step  2  update diagos and onie test
    Step  3  check version before the test
    Step  4  check driver version  ${drive_pattern_tianhe}


tianhe_SDK_9.1_Check_SDK_shell_Version_Test
    [Documentation]  This test checks SDK version and release version
    [Tags]     common  tianhe_SDK_9.1_Check_SDK_shell_Version_Test  tianhe
    [Timeout]  5 min 00 seconds
    [Setup]    boot Into Onie Install Mode
    Step  1  switch sdk folder path  ${SDK_PATH}
    Step  2  load user mode tianhe  ${remote_shell_load_sdk}  ${PAM4_400G_32}
    Step  3  check sdk version tianhe  ${CatReadMe}  ${ifcs}
    Step  4  exit user mode


tianhe_SDK_9.2_Load_and_Initialization_SDK_Test
    [Documentation]  This test check SDK initialization
    [Tags]     tianhe_SDK_9.2_Load_and_Initialization_SDK_Test  tianhe
    [Timeout]  60 min 00 seconds
    [Setup]    boot Into Onie Install Mode
    Step  1  switch sdk folder path  ${SDK_PATH}
    Step  2  check sdk diff load user mode  ${remote_shell_load_sdk}  ${show_port_info}
    Step  3  check sdk diff load user mode  ${remote_shell_load_sdk}  ${show_port_info}  ${PAM4_400G_32}
    Step  4  check sdk diff load user mode  ${remote_shell_load_sdk}  ${show_port_info}  ${OPTICS_400G_32}
    Step  5  check sdk diff load user mode  ${remote_shell_load_sdk}  ${show_port_info}  ${PAM4_100G_128}
    Step  6  check sdk diff load user mode  ${remote_shell_load_sdk}  ${show_port_info}  ${OPTICS_100G_128}
    Step  7  check sdk diff load user mode  ${remote_shell_load_sdk}  ${show_port_info}  ${NRZ_200G_32}
    Step  8  check sdk diff load user mode  ${remote_shell_load_sdk}  ${show_port_info}  ${OPTICS_100G_32}
    Step  9  check sdk diff load user mode  ${remote_shell_load_sdk}  ${show_port_info}  ${NRZ_40G_32}
    Step  10  check sdk diff load user mode  ${remote_shell_load_sdk}  ${show_port_info}  ${OPTICS_40G_32}
    Step  11  check sdk diff load user mode  ${remote_shell_load_sdk}  ${show_port_info}  ${NRZ_25G_128}
    Step  12  check sdk diff load user mode  ${remote_shell_load_sdk}  ${show_port_info}  ${OPTICS_25G_128}
    Step  13  check sdk diff load user mode  ${remote_shell_load_sdk}  ${show_port_info}  ${NRZ_10G_128}
    Step  14  check sdk diff load user mode  ${remote_shell_load_sdk}  ${show_port_info}  ${OPTICS_10G_128}
    Step  15  check sdk diff load user mode  ${remote_shell_load_sdk}  ${show_port_info}  ${NRZ_10G_32}
    Step  16  check sdk diff load user mode  ${remote_shell_load_sdk}  ${show_port_info}  ${OPTICS_10G_32}
    Step  17  check sdk diff load user mode  ${remote_shell_load_sdk}  ${show_port_info}  ${NRZ_100G_64}
    Step  18  check sdk diff load user mode  ${remote_shell_load_sdk}  ${show_port_info}  ${OPTICS_100G_64}
    Step  19  check sdk diff load user mode  ${remote_shell_load_sdk}  ${show_port_info}  ${OPTICS_PAM4_100G_64}
    Step  20  check sdk diff load user mode  ${remote_shell_load_sdk}  ${show_port_info}  ${NRZ_100G_64_1}


tianhe_SDK_9.26_32x400G_PRBS_With_Loopback_Test
    [Documentation]  This test check SDK initialization
    [Tags]     tianhe_SDK_9.26_32x400G_PRBS_With_Loopback_Test  tianhe
    [Timeout]  60 min 00 seconds
    [Setup]    boot Into Onie Install Mode
    Step  1  switch sdk folder path  ${SDK_PATH}
    Step  2  check ber level test  ${PRBS_TOOL}  ${PORT_400G_MODE}

tianhe_SDK_9.28_128x100G_PRBS_With_Loopback_Test
    [Documentation]  This test check SDK initialization
    [Tags]     tianhe_SDK_9.28_128x100G_PRBS_With_Loopback_Test  tianhe
    [Timeout]  60 min 00 seconds
    [Setup]    boot Into Onie Install Mode
    Step  1  switch sdk folder path  ${SDK_PATH}
    Step  2  check ber level test  ${PRBS_TOOL}  ${PORT_100G_MODE}

tianhe_SDK_9.29_32x100G_PRBS_With_Loopback_Test
    [Documentation]  This test check SDK initialization
    [Tags]     tianhe_SDK_9.29_32x100G_PRBS_With_Loopback_Test  tianhe
    [Timeout]  60 min 00 seconds
    [Setup]    boot Into Onie Install Mode
    Step  1  switch sdk folder path  ${SDK_PATH}
    Step  2  check ber level test  ${PRBS_TOOL}  ${PORT_100G_32_MODE}  ${FEC_OPTION}

tianhe_SDK_9.30_32x40G_PRBS_With_Loopback_Test
    [Documentation]  This test check SDK initialization
    [Tags]     tianhe_SDK_9.30_32x40G_PRBS_With_Loopback_Test  tianhe
    [Timeout]  60 min 00 seconds
    [Setup]    boot Into Onie Install Mode
    Step  1  switch sdk folder path  ${SDK_PATH}
    Step  2  check ber level test  ${PRBS_TOOL}  ${PORT_40G_MODE}  ${BER_OPTION}

tianhe_SDK_9.31_128x25G_PRBS_With_Loopback_Test
    [Documentation]  This test check SDK initialization
    [Tags]     tianhe_SDK_9.31_128x25G_PRBS_With_Loopback_Test  tianhe
    [Timeout]  60 min 00 seconds
    [Setup]    boot Into Onie Install Mode
    Step  1  switch sdk folder path  ${SDK_PATH}
    Step  2  check ber level test  ${PRBS_TOOL}  ${PORT_25G_MODE}  ${BER_OPTION}

tianhe_SDK_9.32_128x10G_PRBS_With_Loopback_Test
    [Documentation]  This test check SDK initialization
    [Tags]     tianhe_SDK_9.32_128x10G_PRBS_With_Loopback_Test  tianhe
    [Timeout]  60 min 00 seconds
    [Setup]    boot Into Onie Install Mode
    Step  1  switch sdk folder path  ${SDK_PATH}
    Step  2  check ber level test  ${PRBS_TOOL}  ${PORT_10G_MODE}  ${BER_OPTION}

tianhe_SDK_9.33_64x100G_PRBS_With_Loopback_Test
    [Documentation]  This test check SDK initialization
    [Tags]     tianhe_SDK_9.33_64x100G_PRBS_With_Loopback_Test  tianhe
    [Timeout]  60 min 00 seconds
    [Setup]    boot Into Onie Install Mode
    Step  1  switch sdk folder path  ${SDK_PATH}
    Step  2  check ber level test  ${PRBS_TOOL}  ${PORT_100G_64_MODE}  ${FEC_OPTION}

tianhe_SDK_9.34_64x100G_PRBS_With_Loopback_Test
    [Documentation]  This test check SDK initialization
    [Tags]     tianhe_SDK_9.34_64x100G_PRBS_With_Loopback_Test  tianhe
    [Timeout]  60 min 00 seconds
    [Setup]    boot Into Onie Install Mode
    Step  1  switch sdk folder path  ${SDK_PATH}
    Step  2  load user mode tianhe  ${remote_shell_load_sdk}  ${NRZ_100G_64_1}
    Step  3  check double port status  ${show_port_info}
    Step  4  run odd ber test  ${DIAGTEST_TOOL_LST}  ${PRBS_64_100G}

tianhe_SDK_9.35_PAM4-Active-Copper_2x100G_PRBS_Test
    [Documentation]  This test check SDK initialization
    [Tags]     tianhe_SDK_9.35_PAM4-Active-Copper_2x100G_PRBS_Test  tianhe
    [Timeout]  60 min 00 seconds
    [Setup]    boot Into Onie Install Mode
    Step  1  switch sdk folder path  ${SDK_PATH}
    Step  2  load user mode tianhe  ${remote_shell_load_sdk}  ${OPTICS_PAM4_100G_64}
    Step  3  show port status test  ${show_port_info}
    Step  4  run ber test  ${BER_100G_LST}  ${PRBS_64_100G}

tianhe_SDK_9.37_Active_Copper_2x100G_PRBS_Test
    [Documentation]  This test check SDK initialization
    [Tags]     tianhe_SDK_9.37_Active_Copper_2x100G_PRBS_Test  tianhe
    [Timeout]  60 min 00 seconds
    [Setup]    boot Into Onie Install Mode
    Step  1  switch sdk folder path  ${SDK_PATH}
    Step  2  load user mode tianhe  ${remote_shell_load_sdk}  ${PRBS_2_100G_OPTION}
    Step  3  show port status test  ${show_port_info}
    Step  4  run ber test  ${PRBS_LST}  ${PRBS_32_100G}

tianhe_SDK_9.38_32x400G_PRBS_Test
    [Documentation]  This test check SDK PRBS Via ONIE_PORT_CMD
    [Tags]     tianhe_SDK_9.38_32x400G_PRBS_Test  tianhe
    [Timeout]  60 min 00 seconds
    [Setup]    boot Into Onie Install Mode
    Step  1  switch sdk folder path  ${SDK_PATH}
    Step  2  check load prbs mode  ${SDK_FEC_SCRIPT}  ${integrator_400G_32_copper}
    Step  3  check shell port status  ${ShellPortCmd}
    Step  4  enable or disable prbs test  ${ONIE_PORT}  ${PRBS_OPTION}  ${ENABLE_PATTERN}
    Step  5  check shell ber test  ${BER_READ_LST}  ${PRBS_400G}
    Step  6  enable or disable prbs test  ${ONIE_PORT}  ${PRBS_OPTION}  ${DISABLE_PATTERN}
    Step  7  exit sdk shell mode  ${SDK_SHELL_EXIT}

tianhe_SDK_9.39_32x100G_PRBS_Test
    [Documentation]  This test check SDK PRBS Via ONIE_PORT_CMD
    [Tags]     tianhe_SDK_9.39_32x100G_PRBS_Test  tianhe
    [Timeout]  60 min 00 seconds
    [Setup]    boot Into Onie Install Mode
    Step  1  switch sdk folder path  ${SDK_PATH}
    Step  2  check load prbs mode  ${SDK_FEC_SCRIPT}  ${integrator_100g_32_copper}
    Step  3  check shell port status  ${ShellPortCmd}
    Step  4  enable or disable prbs test  ${ONIE_PORT}  ${PRBS_OPTION}  ${ENABLE_PATTERN}
    Step  5  check shell ber test  ${BER_READ_LST}  ${PRBS_64_100G}
    Step  6  enable or disable prbs test  ${ONIE_PORT}  ${PRBS_OPTION}  ${DISABLE_PATTERN}
    Step  7  exit sdk shell mode  ${SDK_SHELL_EXIT}

tianhe_SDK_9.40_32x40G_PRBS_Test
    [Documentation]  This test check SDK PRBS Via ONIE_PORT_CMD
    [Tags]     tianhe_SDK_9.40_32x40G_PRBS_Test  tianhe
    [Timeout]  60 min 00 seconds
    [Setup]    boot Into Onie Install Mode
    Step  1  switch sdk folder path  ${SDK_PATH}
    Step  2  check load prbs mode  ${SDK_FEC_SCRIPT}  ${integrator_40G_32_copper}
    Step  3  check shell port status  ${ShellPortCmd}
    Step  4  enable or disable prbs test  ${ONIE_PORT}  ${PRBS_OPTION}  ${ENABLE_PATTERN}
    Step  5  check shell ber test  ${BER_READ_LST}  ${PRBS_64_100G}
    Step  6  enable or disable prbs test  ${ONIE_PORT}  ${PRBS_OPTION}  ${DISABLE_PATTERN}
    Step  7  exit sdk shell mode  ${SDK_SHELL_EXIT}

tianhe_SDK_9.41_128x100G_PRBS_Test
    [Documentation]  This test check SDK PRBS Via ONIE_PORT_CMD
    [Tags]     tianhe_SDK_9.41_128x100G_PRBS_Test  tianhe
    [Timeout]  60 min 00 seconds
    [Setup]    boot Into Onie Install Mode
    Step  1  switch sdk folder path  ${SDK_PATH}
    Step  2  check load prbs mode  ${SDK_FEC_SCRIPT}  ${integrator_100G_128_copper}
    Step  3  check shell port status  ${ShellPortCmd}
    Step  4  enable or disable prbs test  ${ONIE_PORT}  ${PRBS_OPTION2}  ${ENABLE_PATTERN}
    Step  5  check shell ber test  ${BER_READ_LST2}  ${PRBS_400G}
    Step  6  enable or disable prbs test  ${ONIE_PORT}  ${PRBS_OPTION2}  ${DISABLE_PATTERN}
    Step  7  exit sdk shell mode  ${SDK_SHELL_EXIT}

tianhe_SDK_9.42_128x25G_PRBS_Test
    [Documentation]  This test check SDK PRBS Via ONIE_PORT_CMD
    [Tags]     tianhe_SDK_9.42_128x25G_PRBS_Test  tianhe
    [Timeout]  60 min 00 seconds
    [Setup]    boot Into Onie Install Mode
    Step  1  switch sdk folder path  ${SDK_PATH}
    Step  2  check load prbs mode  ${SDK_FEC_SCRIPT}  ${integrator_25G_128_copper}
    Step  3  check shell port status  ${ShellPortCmd}
	Step  4  enable or disable prbs test  ${ONIE_PORT}  ${PRBS_OPTION2}  ${ENABLE_PATTERN}
    Step  5  check shell ber test  ${BER_READ_LST2}  ${PRBS_64_100G}
    Step  6  enable or disable prbs test  ${ONIE_PORT}  ${PRBS_OPTION2}  ${DISABLE_PATTERN}
    Step  7  exit sdk shell mode  ${SDK_SHELL_EXIT}

tianhe_SDK_9.43_128x10G_PRBS_Test
    [Documentation]  This test check SDK PRBS Via ONIE_PORT_CMD
    [Tags]     tianhe_SDK_9.43_128x10G_PRBS_Test  tianhe
    [Timeout]  60 min 00 seconds
    [Setup]    boot Into Onie Install Mode
    Step  1  switch sdk folder path  ${SDK_PATH}
    Step  2  check load prbs mode  ${SDK_FEC_SCRIPT}  ${integrator_10G_128_copper}
    Step  3  check shell port status  ${ShellPortCmd}
	Step  4  enable or disable prbs test  ${ONIE_PORT}  ${PRBS_OPTION2}  ${ENABLE_PATTERN}
    Step  5  check shell ber test  ${BER_READ_LST2}  ${PRBS_64_100G}
    Step  6  enable or disable prbs test  ${ONIE_PORT}  ${PRBS_OPTION2}  ${DISABLE_PATTERN}
    Step  7  exit sdk shell mode  ${SDK_SHELL_EXIT}

tianhe_SDK_9.44_64x100G_PRBS_Test
    [Documentation]  This test check SDK PRBS Via ONIE_PORT_CMD
    [Tags]     tianhe_SDK_9.44_64x100G_PRBS_Test  tianhe
    [Timeout]  60 min 00 seconds
    [Setup]    boot Into Onie Install Mode
    Step  1  switch sdk folder path  ${SDK_PATH}
    Step  2  check load prbs mode  ${SDK_FEC_SCRIPT}  ${integrator_100G_64_copper}
    Step  3  check shell port status  ${ShellPortCmd}
	Step  4  enable or disable prbs test  ${ONIE_PORT}  ${PRBS_OPTION1}  ${ENABLE_PATTERN}
    Step  5  check shell ber test  ${BER_READ_LST1}  ${PRBS_400G}
    Step  6  enable or disable prbs test  ${ONIE_PORT}  ${PRBS_OPTION1}  ${DISABLE_PATTERN}
    Step  7  exit sdk shell mode  ${SDK_SHELL_EXIT}

tianhe_SDK_9.45_64x100-1G_PRBS_Test
    [Documentation]  This test check SDK PRBS Via ONIE_PORT_CMD
    [Tags]     tianhe_SDK_9.45_64x100-1G_PRBS_Test  tianhe
    [Timeout]  60 min 00 seconds
    [Setup]    boot Into Onie Install Mode
    Step  1  switch sdk folder path  ${SDK_PATH}
    Step  2  check load prbs mode  ${SDK_FEC_SCRIPT}  ${integrator_OPTICS_100G}
    Step  3  check double port status  ${ShellPortCmd}
    Step  4  enable or disable prbs test  ${ONIE_PORT}  ${PRBS_OPTION1}  ${ENABLE_PATTERN}
	Step  5  check shell ber test  ${BER_READ_LST1}  ${PRBS_64_100G}  ${PORT_64_100G_MODE}
    Step  6  enable or disable prbs test  ${ONIE_PORT}  ${PRBS_OPTION1}  ${DISABLE_PATTERN}
    Step  7  exit sdk shell mode  ${SDK_SHELL_EXIT}

tianhe_SDK_9.46_FEC_Test
    [Documentation]  This test check SDK FEC Test
    [Tags]     tianhe_SDK_9.46_FEC_Test  tianhe
    [Timeout]  60 min 00 seconds
    [Setup]    boot Into Onie Install Mode
    Step  1  switch sdk folder path  ${SDK_PATH}
    Step  2  check the port fec test  ${DIAGTEST_SDK_TOOL}  ${PORT_MODE_OPTION1}
    Step  3  check the port fec test  ${DIAGTEST_SDK_TOOL}  ${PORT_MODE_OPTION2}
    Step  4  check the port fec test  ${DIAGTEST_SDK_TOOL}  ${PORT_MODE_OPTION3}
    Step  5  check the port fec test  ${DIAGTEST_SDK_TOOL}  ${PORT_MODE_OPTION4}
    Step  6  check the port fec test  ${DIAGTEST_SDK_TOOL}  ${PORT_MODE_OPTION5}
    Step  7  check the port fec test  ${DIAGTEST_SDK_TOOL}  ${PORT_MODE_OPTION6}
    Step  8  check the port fec test  ${DIAGTEST_SDK_TOOL}  ${PORT_MODE_OPTION7}
    Step  9  check the port fec test  ${DIAGTEST_SDK_TOOL}  ${PORT_MODE_OPTION8}
    Step  10  check the port fec test  ${DIAGTEST_SDK_TOOL}  ${PORT_MODE_OPTION9}
    Step  11  check the port fec test  ${DIAGTEST_SDK_TOOL}  ${PORT_MODE_OPTION10}
    Step  12  check the port fec test  ${DIAGTEST_SDK_TOOL}  ${PORT_MODE_OPTION11}
    Step  13  check the port fec test  ${DIAGTEST_SDK_TOOL}  ${PORT_MODE_OPTION12}
    Step  14  check the port fec test  ${DIAGTEST_SDK_TOOL}  ${PORT_MODE_OPTION13}
    Step  15  check the port fec test  ${DIAGTEST_SDK_TOOL}  ${PORT_MODE_OPTION14}

tianhe_SDK_9.47_Remote_Shell_Test
    [Documentation]  This test check SDK remote shell Test
    [Tags]     tianhe_SDK_9.47_Remote_Shell_Test  tianhe
    [Timeout]  60 min 00 seconds
    [Setup]    boot Into Onie Install Mode
    Step  1  switch sdk folder path  ${SDK_PATH}
    Step  2  remote shell load test  ${Remote_Shell_CMD}
    Step  3  check shell port status  ${ShellPortCmd}
    Step  4  exit sdk shell mode  ${SDK_SHELL_EXIT}

tianhe_SDK_9.48_Pre-emphasis_Check
    [Documentation]  This test check SDK pre-emphasis test
    [Tags]     tianhe_SDK_9.48_Pre-emphasis_Check  tianhe
    [Timeout]  60 min 00 seconds
    [Setup]    boot Into Onie Install Mode
    Step  1  switch sdk folder path  ${SDK_PATH}
    Step  2  check the port fec test  ${DIAGTEST_SDK_TOOL}  ${EMPHASSIS_OPTION1}
    Step  3  check the port fec test  ${DIAGTEST_SDK_TOOL}  ${EMPHASSIS_OPTION2}
    Step  4  check the port fec test  ${DIAGTEST_SDK_TOOL}  ${EMPHASSIS_OPTION3}
    Step  5  check the port fec test  ${DIAGTEST_SDK_TOOL}  ${EMPHASSIS_OPTION4}
    Step  6  check the port fec test  ${DIAGTEST_SDK_TOOL}  ${EMPHASSIS_OPTION5}
    Step  7  check the port fec test  ${DIAGTEST_SDK_TOOL}  ${EMPHASSIS_OPTION6}
    Step  8  check the port fec test  ${DIAGTEST_SDK_TOOL}  ${EMPHASSIS_OPTION7}
    Step  9  check the port fec test  ${DIAGTEST_SDK_TOOL}  ${EMPHASSIS_OPTION8}

tianhe_SDK_9.49_Ess_Script_Test
    [Documentation]  This test check SDK ess script test
    [Tags]     tianhe_SDK_9.49_Ess_Script_Test  tianhe
    [Timeout]  60 min 00 seconds
    [Setup]    boot Into Onie Install Mode
    Step  1  switch sdk folder path  ${SDK_PATH}
    Step  2  check the port fec test  ${DIAGTEST_SDK_TOOL}  ${TRAFFIC_OPTION1}
    Step  3  check the port fec test  ${DIAGTEST_SDK_TOOL}  ${TRAFFIC_OPTION2}
    Step  4  check the port fec test  ${DIAGTEST_SDK_TOOL}  ${TRAFFIC_OPTION3}


tianhe_SDK_10.1_Copper_4x25_Copper_2x100_Copper_4x25_Mode
    [Documentation]  This test check SDK 1-8:Copper_4x25;9-22:Copper_2x100;23-32:Copper_4x25 Mode
    [Tags]     tianhe_SDK_10.1_Copper_4x25_Copper_2x100_Copper_4x25_Mode  tianhe
    [Timeout]  60 min 00 seconds
    [Setup]    boot Into Onie Install Mode
    Step  1  switch sdk folder path  ${SDK_PATH}
    Step  2  load user mode tianhe  ${remote_shell_load_sdk}  ${COPPER_PORT_OPTION}
	Step  3  show port status test  ${show_port_info}  ${SpeedType1}
    Step  4  port enable all test  ${PORT_ENABLE_ALL}
    Step  5  show port status test  ${show_port_info}  ${SpeedType1}

tianhe_SDK_10.2_Copper_1x100_Copper_4x10_Copper_1x100_Mode
    [Documentation]  This test check SDK 1-20:Copper_1x100G;21-24:Copper_4x10G;25-32:1x100G Mode
    [Tags]     tianhe_SDK_10.2_Copper_1x100_Copper_4x10_Copper_1x100_Mode  tianhe
    [Timeout]  60 min 00 seconds
    [Setup]    boot Into Onie Install Mode
    Step  1  switch sdk folder path  ${SDK_PATH}
    Step  2  load user mode tianhe  ${remote_shell_load_sdk}  ${COPPER_PORT_OPTION1}
	Step  3  show port status test  ${show_port_info}  ${SpeedType2}
    Step  4  port enable all test  ${PORT_ENABLE_ALL}
    Step  3  show port status test  ${show_port_info}  ${SpeedType2}

tianhe_SDK_10.3_Copper_1x100G_Copper_4x10G_4x100G_Mode
    [Documentation]  This test check SDK 1-20:Copper_1x100G;21-24:Copper_4x10G;25-32:4x100G Mode
    [Tags]     tianhe_SDK_10.3_Copper_1x100G_Copper_4x10G_4x100G_Mode  tianhe
    [Timeout]  60 min 00 seconds
    [Setup]    boot Into Onie Install Mode
    Step  1  switch sdk folder path  ${SDK_PATH}
    Step  2  load user mode tianhe  ${remote_shell_load_sdk}  ${COPPER_PORT_OPTION2}
    Step  3  show port status test  ${show_port_info}  ${SpeedType3}
    Step  4  port enable all test  ${PORT_ENABLE_ALL}
    Step  5  show port status test  ${show_port_info}  ${SpeedType3}

tianhe_SDK_11.3_Default_Onie_fppPort_Mode
    [Documentation]  This test check SDK Default onie_fppPort Mode
    [Tags]     tianhe_SDK_11.3_Default_Onie_fppPort_Mode  tianhe
    [Timeout]  60 min 00 seconds
    [Setup]    boot Into Uboot
    Step  1  set uboot parameters then enter onie bootcmd mode  ${ONIE_FPP}
    Step  2  switch sdk folder path  ${SDK_PATH}
    Step  3  check shell port status  ${ShellPortCmd}

tianhe_SDK_11.4_Integrator_Vlan_Setting_Check
    [Documentation]  This test check Integrator Vlan Setting Check
    [Tags]     tianhe_SDK_11.4_Integrator_Vlan_Setting_Check  tianhe
    [Timeout]  60 min 00 seconds
    [Setup]    boot Into Onie Install Mode
    Step  1  switch sdk folder path  ${SDK_PATH}
    Step  2  check load prbs mode  ${SDK_FEC_SCRIPT}  ${SFP_DETECT_OPTION1}
    Step  3  check shell port status  ${ShellPortCmd}
    Step  4  check default vlan  ${VLAN_TOOL}  ${ENABLE_PATTERN}
    Step  5  exit sdk shell mode  ${SDK_SHELL_EXIT}
    Step  6  check load prbs mode  ${SDK_FEC_SCRIPT}  ${SFP_DETECT_OPTION2}
    Step  7  check shell port status  ${ShellPortCmd}
    Step  8  check default vlan  ${VLAN_TOOL}  ${PRBS_64_100G}
    Step  9  exit sdk shell mode  ${SDK_SHELL_EXIT}

tianhe_SDK_14.2_knet_L2_Show_Tool_Test
    [Documentation]  This test check knet l2 show tool
    [Tags]     tianhe_SDK_14.2_knet_L2_Show_Tool_Test  tianhe
    [Timeout]  60 min 00 seconds
    [Setup]    boot Into Onie Install Mode
    Step  1  bootup into onie bootcmd mode
    Step  2  check knet l2 information  ${knet_l2_show_cmd}  ${KNET_PATTERN}

tianhe_SDK_14.3_Integrator_mode_Config
    [Documentation]  This test check Integrator_mode Config
    [Tags]     tianhe_SDK_14.3_Integrator_mode_Config  tianhe
    [Timeout]  60 min 00 seconds
    [Setup]    boot Into Onie Install Mode
    Step  1  switch sdk folder path  ${SDK_PATH}
    Step  2  integrator mode config test  ${SDK_FEC_SCRIPT}  ${integrator_400G_32}  ${show_port_info}  ${PORT_ENABLE_ALL1}
    Step  3  integrator mode config test  ${SDK_FEC_SCRIPT}  ${integrator_100G_32}  ${show_port_info}  ${PORT_ENABLE_ALL1}
    Step  4  integrator mode config test  ${SDK_FEC_SCRIPT}  ${integrator_40G_32}  ${show_port_info}  ${PORT_ENABLE_ALL1}
    Step  5  integrator mode config test  ${SDK_FEC_SCRIPT}  ${integrator_100G_128}  ${show_port_info}  ${PORT_ENABLE_ALL1}
    Step  6  integrator mode config test  ${SDK_FEC_SCRIPT}  ${integrator_25G_128}  ${show_port_info}  ${PORT_ENABLE_ALL1}
    Step  7  integrator mode config test  ${SDK_FEC_SCRIPT}  ${integrator_10G_128}  ${show_port_info}  ${PORT_ENABLE_ALL1}
    Step  8  integrator mode config test  ${SDK_FEC_SCRIPT}  ${integrator_100G_64}  ${show_port_info}  ${PORT_ENABLE_ALL1}
    Step  9  integrator mode config test  ${SDK_FEC_SCRIPT}  ${integrator_100G_64_1}  ${show_port_info}  ${PORT_ENABLE_ALL1}

tianhe_SDK_14.4_QSFP_Tool_Test
    [Documentation]  This test check QSFP tool test
    [Tags]     tianhe_SDK_14.4_QSFP_Tool_Test  tianhe
    [Timeout]  60 min 00 seconds
    [Setup]    boot Into Onie Install Mode
    Step  1  switch sdk folder path  ${SDK_PATH}
    Step  2  check qsfp tool test  ${qsfp_cmd}

tianhe_SDK_9.51_Snake_Test
    [Documentation]  This test check SDK snake test
    [Tags]     tianhe_SDK_9.51_Snake_Test  tianhe
    [Timeout]  60 min 00 seconds
    [Setup]  boot Into DiagOS Mode
    Step  1  run memory test in background  ${MEM_LST}
    Step  2  verify the mem test is running  ${PS_TOOL}
    Step  3  switch sdk folder in diag mode  ${SDK_PATH}
    Step  4  download snake file  ${Snake_FILE_LST}
    Step  5  run snake test suite  ${Snake_FILE_LST}
    Step  6  verify the mem test is running  ${PS_TOOL}
    Step  7  monitor mem test complete  ${TAIL_TOOL}
    Step  8  check mem result  ${MEM_RESULT}
    Step  9  check the mem usage log  ${MEM_FREE_RESULT}




*** Keywords ***
Onie Connect Device
    OnieConnect

Onie Disconnect Device
    OnieDisconnect

