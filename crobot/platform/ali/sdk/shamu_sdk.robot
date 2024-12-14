###############################################################################
# LEGALESE:   "Copyright (C) 2019-2021, Celestica Corp. All rights reserved." #
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

Library           AliSdkLib.py
Library           AliCommonLib.py
Library           SdkCommonLib.py
Library           CommonLib.py
Variables         AliCommonVariable.py
Variables         AliSdkVariable.py

Resource          AliSdkKeywords.resource

Suite Setup       Connect Device
Suite Teardown    Disconnect Device

*** Variables ***
${LoopCnt}      1
${MAX_LOOP}     5
# ${MAX_LOOP}     501

*** Test Cases ***
# sonic already packed the latest diag and sdk
#ALI_SDK_COMM_TC_000_Install_SDK_Test
#    [Documentation]  This test checks SDK initialization
#    [Tags]  ALI_SDK_COMM_TC_000_Install_SDK_Test  shamu
#    [Timeout]  15 min 00 seconds
#    [Setup]  prepare images  SDK  ${diagos_mode}
#    Step  1  install sdk
#    Step  2  check sdk version
#    [Teardown]  exit sdk mode

ALI_SDK_COMM_TC_001_Load_And_Initialization_SDK_Test
    [Tags]  ALI_SDK_COMM_TC_001_Load_And_Initialization_SDK_Test  shamu
    [Timeout]  30 min 00 seconds
    [Setup]  power cycle sonic  ${diagos_mode}
    BuiltIn.Sleep  120
    Step  1  change dir to sdk path
    Step  2  verify load SDK
    Step  3  exit sdk mode
    step  4  change dir to sdk path
    Step  5  verify load SDK  bcm56780_a0-generic-16x100_48x50.config.yml
    Step  6  exit sdk mode
    Step  7  change dir to sdk path
    Step  8  verify load SDK  bcm56780_a0-generic-16x200_48x50.config.yml
    Step  9  exit sdk mode
    Step  10  change dir to sdk path
    Step  11  verify load SDK  bcm56780_a0-generic-16x200_24x100.config.yml
    Step  12  exit sdk mode
    Step  13  change dir to sdk path
    Step  14  verify load SDK  bcm56780_a0-generic-16x200_48x100.config.yml
    Step  15  exit sdk mode
    Step  16  change dir to sdk path
    Step  17  verify load SDK  bcm56780_a0-generic-8x200_64x25.config.yml
    Step  18  exit sdk mode
    Step  19  change dir to sdk path
    Step  20  verify load SDK  bcm56780_a0-generic-40x200.config_eloop.yml
    Step  21  exit sdk mode
    Step  22  change dir to sdk path
    Step  23  verify load SDK  bcm56780_a0-generic-40x100.config.yml
    Step  24  exit sdk mode
    Step  25  change dir to sdk path
    Step  26  verify load SDK  bcm56780_a0-generic-40x200.config.yml
    [Teardown]  exit sdk mode

ALI_SDK_COMM_TC_007_QSFP_56_1x200G_Port_PRBS_And_BER_Test
    [Tags]  ALI_SDK_COMM_TC_007_QSFP_56_1x200G_Port_PRBS_And_BER_Test  shamu
    [Timeout]  30 min 00 seconds
    [Setup]  power cycle sonic  ${diagos_mode}
    BuiltIn.Sleep  120
    Step  1  change dir to sdk path
    Step  2  verify load SDK
    Step  3  run cmd  ${ps_cd_cmd}  ${BCM_promptstr}
    Step  4  run cmd  dsh -c "phy diag 1-69 prbs set p=3"  ${BCM_promptstr}
    Step  5  run cmd  dsh -c "phy diag 1-69 prbs get"  ${BCM_promptstr}
    Step  6  run cmd  dsh -c "phy diag 1-69 prbsstat start interval=120"  ${BCM_promptstr}
    BuiltIn.Sleep  5
    Step  7  run cmd  dsh -c "phy diag 1-69 prbsstat ber"  ${BCM_promptstr}
    BuiltIn.Sleep  120
    Step  8  run cmd  dsh -c "phy diag 1-69 prbsstat ber"  ${BCM_promptstr}
    Step  9  verify prbs ber for shamu
    Step  10  run cmd  dsh -c "phy diag 1-69 prbsstat stop"  ${BCM_promptstr}
    Step  11  run cmd  dsh -c "phy diag 1-69 prbs clear"  ${BCM_promptstr}
    [Teardown]  exit sdk mode

ALI_SDK_COMM_TC_008_QSFP_56_1x100G_Port_PRBS_And_BER_Test
    [Tags]  ALI_SDK_COMM_TC_008_QSFP_56_1x100G_Port_PRBS_And_BER_Test  shamu
    [Timeout]  30 min 00 seconds
    [Setup]  power cycle sonic  ${diagos_mode}
    BuiltIn.Sleep  120
    Step  1  change dir to sdk path
    Step  2  verify load SDK  ${set_40x100G_rate}
    Step  3  run cmd  ${ps_ce_cmd}  ${BCM_promptstr}
    Step  4  run cmd  dsh -c "phy diag 1-69 prbs set p=3"  ${BCM_promptstr}
    Step  5  run cmd  dsh -c "phy diag 1-69 prbs get"  ${BCM_promptstr}
    Step  6  run cmd  dsh -c "phy diag 1-69 prbsstat start interval=120"  ${BCM_promptstr}
    BuiltIn.Sleep  5
    Step  7  run cmd  dsh -c "phy diag 1-69 prbsstat ber"  ${BCM_promptstr}
    BuiltIn.Sleep  120
    Step  8  run cmd  dsh -c "phy diag 1-69 prbsstat ber"  ${BCM_promptstr}
    Step  9  verify prbs ber for shamu
    Step  10  run cmd  dsh -c "phy diag 1-69 prbsstat stop"  ${BCM_promptstr}
    Step  11  run cmd  dsh -c "phy diag 1-69 prbs clear"  ${BCM_promptstr}
    [Teardown]  exit sdk mode

ALI_SDK_COMM_TC_011_Switch_PCIE_FW_Upgrade_Test
    [Tags]  ALI_SDK_COMM_TC_011_Switch_PCIE_FW_Upgrade_Test  shamu
    [Timeout]  30 min 00 seconds
    [Setup]  power cycle sonic  ${diagos_mode}
    BuiltIn.Sleep  120
    Step  1  change dir to sdk path
    Step  2  prepare_images_for_shamu_pcie  PCIE_FLASH_SHAMU  ${diagos_mode}
    Step  3  verify load SDK
    Step  4  to lt mode
    step  5  check pcie phy fw info for shamu
    Step  6  update pcie fw for shamu
    Step  7  exit sdk mode
    Step  8  reboot to diagos
    BuiltIn.Sleep  60
    Step  9  change dir to sdk path
    Step  10  verify load SDK
    Step  11  to lt mode
    Step  12  check pcie phy fw info for shamu
    [Teardown]  exit sdk mode

ALI_SDK_COMM_TC_013_Serdes_FW_Test
    [Tags]  ALI_SDK_COMM_TC_013_Serdes_FW_Test  shamu
    [Timeout]  30 min 00 seconds
    [Setup]  power cycle sonic  ${diagos_mode}
    BuiltIn.Sleep  120
    Step  1  change dir to sdk path
    Step  2  verify load SDK
    Step  3  check common ucode version for shamu
    Step  4  check lane config information for shamu
    [Teardown]  exit sdk mode

ALI_SDK_COMM_TC_014_10G_KR_Access_Test
    [Tags]  ALI_SDK_COMM_TC_014_10G_KR_Access_Test  shamu
    [Timeout]  240 min 00 seconds
    [Setup]  power cycle sonic  ${diagos_mode}
    BuiltIn.Sleep  120
    Step  1  change dir to sdk path
    Step  2  verify load SDK
    Step  3  run cmd  vlan clear  ${BCM_promptstr}
    Step  4  run cmd  vlan create 250 pbm=xe0,xe1 ubm=xe0,xe1  ${BCM_promptstr}
    Step  5  to shell mode
    Step  6  change dir  ${diag_path}
    Step  7  test 10g KR for shamu
    Step  8  change dir  ${diag_path}
    FOR  ${index}  IN RANGE  1  ${1001}
         Step  1  test 10g KR for shamu
    END
    [Teardown]  exit sdk mode

ALI_SDK_COMM_TC_015_Remote_Shell_Test
    [Tags]  ALI_SDK_COMM_TC_015_Remote_Shell_Test  shamu
    [Timeout]  30 min 00 seconds
    [Setup]  power cycle sonic  ${diagos_mode}
    BuiltIn.Sleep  120
    Step  1  change dir to sdk path
    Step  2  verify remote SDK version for shamu
    Step  3  exit SDK remote for shamu
    [Teardown]  exit sdk mode

ALI_SDK_COMM_TC_018_Loopback_Module_40x200G_Internal_Traffic_Test
    [Documentation]  This test checks SDK CPU Traffic
    [Tags]  ALI_SDK_COMM_TC_018_Loopback_Module_40x200G_Internal_Traffic_Test  shamu
    [Timeout]  30 min 00 seconds
    [Setup]  power cycle sonic  ${diagos_mode}
    BuiltIn.Sleep  120
    Step  1  change dir to sdk path
    Step  2  verify load SDK
    BuiltIn.Sleep  10
    Step  3  run cmd  ${ps_cd_cmd}  ${BCM_promptstr}
    Step  4  check all port up status 
    Step  5  set 200G soc for shamu
    Step  6  run cmd  ${clear_c_cmd}  ${BCM_promptstr}
    Step  7  run cmd  ${show_c_cd_cmd}  ${BCM_promptstr}
    Step  8  run cmd  ${let_CPU_send_package_cmd_for_shamu}  ${BCM_promptstr}
    Step  9  sleep 300s
    Step  10  run cmd  ${stop_traffic_cmd_for_shamu}  ${BCM_promptstr}
    Step  11  verify all port data for shamu
    Step  12  run cmd  ${port_cd_on_cmd}  ${BCM_promptstr}
    [Teardown]  exit sdk mode

ALI_SDK_COMM_TC_023_SDK_Re_Init_Stress_Test
    [Tags]  ALI_SDK_COMM_TC_023_SDK_Re_Init_Stress_Test  shamu
    [Timeout]  60 min 00 seconds
    [Setup]  change dir to sdk path
    FOR  ${INDEX}  IN RANGE  1  ${MAX_LOOP}
         Step  1  power cycle sonic  ${diagos_mode}
         BuiltIn.Sleep  120
         Step  2  change dir to sdk path
         Step  3  verify load SDK
         BuiltIn.Sleep  10
         Step  4  run cmd  ${ps_cd_cmd}  ${BCM_promptstr}
         Step  5  check all port up status
         Step  6  set 200G soc for shamu
         Step  7  run cmd  ${clear_c_cmd}  ${BCM_promptstr}
         Step  8  run cmd  ${show_c_cd_cmd}  ${BCM_promptstr}
         Step  9  run cmd  ${let_CPU_send_package_100_cmd_for_shamu}  ${BCM_promptstr}
         Step  10  run cmd  sleep 60  ${BCM_promptstr}  timeout=100
         Step  11  run cmd  ${stop_traffic_cmd_for_shamu}  ${BCM_promptstr}
         Step  12  check pkt counter for shamu
         Step  13  run cmd  ${port_cd_on_cmd}  ${BCM_promptstr}
         Step  14  exit sdk mode
    END
    [Teardown]  exit sdk mode

ALI_SDK_COMM_TC_025_All_Ports_Disable_And_Enable_Stress_Test
    [Tags]  ALI_SDK_COMM_TC_025_All_Ports_Disable_And_Enable_Stress_Test  shamu
    [Timeout]  60 min 00 seconds
    [Setup]  change dir to sdk path
    FOR  ${INDEX}  IN RANGE  1  ${MAX_LOOP}
         Step  1  power cycle sonic  ${diagos_mode}
         BuiltIn.Sleep  120
         Step  2  change dir to sdk path
         Step  3  verify load SDK
         BuiltIn.Sleep  10
         Step  4  run cmd  ${ps_cd_cmd}  ${BCM_promptstr}
         Step  5  check all port up status
         Step  6  sendline  port cd en=0
         BuiltIn.Sleep  10
         Step  7  check all port down status
         Step  8  sendline  port cd en=1
         BuiltIn.Sleep  10
         Step  9  check all port up status
         Step  10  set 200G soc for shamu
         Step  11  run cmd  ${clear_c_cmd}  ${BCM_promptstr}
         Step  12  run cmd  ${show_c_cd_cmd}  ${BCM_promptstr}
         Step  13  run cmd  ${let_CPU_send_package_1280_cmd_for_shamu}  ${BCM_promptstr}
         Step  14  run cmd  sleep 60  ${BCM_promptstr}  timeout=100
         Step  15  run cmd  ${stop_traffic_cmd_for_shamu}  ${BCM_promptstr}
         Step  16  check pkt counter for shamu
         Step  17  run cmd  ${port_cd_on_cmd}  ${BCM_promptstr}
         Step  18  exit sdk mode
    END
    [Teardown]  exit sdk mode

ALI_SDK_COMM_TC_026_Power_Cycle_Stress_Test
    [Tags]  ALI_SDK_COMM_TC_026_Power_Cycle_Stress_Test  shamu
    [Timeout]  60 min 00 seconds
    [Setup]  power cycle sonic  ${diagos_mode}
    BuiltIn.Sleep  120
    FOR  ${INDEX}  IN RANGE  1  ${MAX_LOOP}
         Step  1  change dir to sdk path
         Step  2  verify load SDK
         BuiltIn.Sleep  10
         Step  3  run cmd  ${ps_cd_cmd}  ${BCM_promptstr}
         Step  4  check all port up status
         Step  5  set 200G soc for shamu
         Step  6  run cmd  ${clear_c_cmd}  ${BCM_promptstr}
         Step  7  run cmd  ${show_c_cd_cmd}  ${BCM_promptstr}
         Step  8  run cmd  ${let_CPU_send_package_1280_cmd_for_shamu}  ${BCM_promptstr}
         Step  9  run cmd  sleep 60  ${BCM_promptstr}  timeout=100
         Step  10  run cmd  ${stop_traffic_cmd_for_shamu}  ${BCM_promptstr}
         Step  11  check pkt counter for shamu
         Step  12  run cmd  ${port_cd_on_cmd}  ${BCM_promptstr}
         Step  13  exit sdk mode
         BuiltIn.Sleep  15
         Step  14  power cycle sonic  ${diagos_mode}
         BuiltIn.Sleep  120
    END
    [Teardown]  exit sdk mode

*** Keywords ***
Connect Device
    Login Device

Disconnect Device
    Sdk Disconnect
