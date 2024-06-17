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
${MAX_LOOP}     3

*** Test Cases ***

# sonic already packed the latest diag and sdk
#ALI_SDK_COMM_TC_000_Install_SDK_Test
#    [Documentation]  This test checks SDK initialization
#    [Tags]     ALI_SDK_COMM_TC_000_Install_SDK_Test  migaloo
#    [Timeout]  15 min 00 seconds
#    [Setup]    prepare images  SDK  ${diagos_mode}
#    Step  1  install sdk
#    Step  2  check sdk version
#    [Teardown]  clean images  DUT  SDK

ALI_SDK_COMM_TC_001_Load_and_Initialization_SDK_Test
    [Tags]     ALI_SDK_COMM_TC_001_Load_and_Initialization_SDK_Test  migaloo
    [Timeout]  30 min 00 seconds
    [Setup]  change dir to sdk path
    Step  1  verify load SDK
    [Teardown]  exit sdk mode

ALI_SDK_COMM_TC_002_Version_Test
    [Tags]     ALI_SDK_COMM_TC_002_Version_Test  migaloo
    [Timeout]  30 min 00 seconds
    [Setup]  change dir to sdk path
    Step  1  verify load SDK
    Step  2  check bcm version
    Step  3  to lt mode
    Step  4  check pcie phy fw info
    [Teardown]  exit sdk mode

ALI_SDK_COMM_TC_004_128x200G_Port_Status_Test
    [Tags]     ALI_SDK_COMM_TC_004_128x200G_Port_Status_Test  migaloo
    [Timeout]  30 min 00 seconds
    [Setup]  Run Keywords
    ...  change dir to sdk path  AND
    ...  Run Keyword And Ignore Error  change kernel log level  console=${diagos_mode}  level=3
    Step  1  verify load SDK
    Step  2  check all port up status
    Step  3  sendline  port cd en=0
    BuiltIn.Sleep  5
    Step  4  check all port down status
    Step  5  sendline  port cd en=1
    BuiltIn.Sleep  5
    Step  6  check all port up status
    [Teardown]  Run Keywords
    ...  exit sdk mode  AND
    ...  Run Keyword And Ignore Error  change kernel log level  console=${diagos_mode}  level=7

ALI_SDK_COMM_TC_006_128x200G_Port_BER_Test
    [Tags]     ALI_SDK_COMM_TC_006_128x200G_Port_BER_Test  migaloo
    [Timeout]  30 min 00 seconds
    [Setup]  change dir to sdk path
    Step  1  verify load SDK
    Step  2  to lt mode
    Step  3  run cmd  phy diag 1-262 prbs clear  ${SDKLT_PROMPT}
    Step  4  run cmd  phy diag 1-262 prbs set p=3  ${SDKLT_PROMPT}
    Step  5  run cmd  phy diag 1-262 prbsstat start interval=30  ${SDKLT_PROMPT}
    BuiltIn.Sleep  10
    Step  6  run cmd  ${prbs_stat_cmd}  ${SDKLT_PROMPT}
    BuiltIn.Sleep  300
    Step  7  verify prbs ber
    [Teardown]  exit sdk mode

ALI_SDK_COMM_TC_007_128x200G_Port_Loopback_Test
    [Tags]     ALI_SDK_COMM_TC_007_128x200G_Port_Loopback_Test  migaloo
    [Timeout]  30 min 00 seconds
    [Setup]  Run Keywords
    ...  change dir to sdk path  AND
    ...  Run Keyword And Ignore Error  change kernel log level  console=${diagos_mode}  level=3
    Step  1  verify load SDK
    Step  2  run cmd  ${port_mac_cmd}  ${BCM_promptstr}
    Step  3  check port loopback mode  ${loopback_mode_mac}
    Step  4  set 200G soc
    Step  5  run cmd  ${clear_c_cmd}  ${BCM_promptstr}
    Step  6  run cmd  ${show_c_cmd}   ${BCM_promptstr}
    Step  7  run cmd  ${let_CPU_send_package_cmd}  ${BCM_promptstr}
    Step  8  run cmd  sleep 30  ${BCM_promptstr}
    Step  9  run cmd  ${stop_traffic_cmd}  ${BCM_promptstr}
    Step  10  check pkt counter
    Step  11  exit sdk mode
    Step  12  verify load SDK  -m 128x200intphy
    Step  13  run cmd  ${port_mac_cmd}  ${BCM_promptstr}
    Step  14  check port loopback mode  ${loopback_mode_mac}
    Step  15  set 200G soc
    Step  16  run cmd  ${clear_c_cmd}  ${BCM_promptstr}
    Step  17  run cmd  ${show_c_cmd}   ${BCM_promptstr}
    Step  18  run cmd  ${let_CPU_send_package_cmd}  ${BCM_promptstr}
    Step  19  run cmd  sleep 30  ${BCM_promptstr}
    Step  20  run cmd  ${stop_traffic_cmd}  ${BCM_promptstr}
    Step  21  check pkt counter
    Step  22  exit sdk mode
    [Teardown]  Run Keywords
    ...  exit sdk mode  AND
    ...  Run Keyword And Ignore Error  change kernel log level  console=${diagos_mode}  level=7

ALI_SDK_COMM_TC_009_128x200G_L2_CPU_Traffic_Test
    [Documentation]  This test checks SDK CPU Traffic
    [Tags]     ALI_SDK_COMM_TC_009_128x200G_L2_CPU_Traffic_Test  migaloo
    [Timeout]  30 min 00 seconds
    [Setup]    change dir to sdk path
    Step  1  verify load SDK
    Step  2  set snake vlan to all ports
    Step  3  check all port up status
    Step  4  clear all port counter
    Step  5  let CPU send packages
    Step  6  sleep 300s
    Step  7  stop traffic
    Step  8  verify all port data
    [Teardown]  exit sdk mode

ALI_SDK_COMM_TC_012_Switch_PCIE_FW_upgrade_Test
    [Tags]     ALI_SDK_COMM_TC_012_Switch_PCIE_FW_upgrade_Test  migaloo
    [Timeout]  30 min 00 seconds
    [Setup]    change dir to sdk path
    Step  1  verify load SDK
    Step  2  to lt mode
    Step  3  update pcie fw
    Step  4  exit sdk mode
    Step  5  reboot to diagos
    Step  6  change dir to sdk path
    Step  7  verify load SDK
    Step  8  to lt mode
    Step  9  check pcie phy fw info
    [Teardown]  exit sdk mode

ALI_SDK_COMM_TC_014_PHY_Info_Test
    [Tags]     ALI_SDK_COMM_TC_014_PHY_Info_Test  migaloo
    [Timeout]  30 min 00 seconds
    [Setup]    change dir to sdk path
    Step  1  verify load SDK
    Step  2  to lt mode
    Step  3  check phy info
    [Teardown]  exit sdk mode

ALI_SDK_COMM_TC_015_Serdes_FW_Test
    [Tags]     ALI_SDK_COMM_TC_015_Serdes_FW_Test  migaloo
    [Timeout]  30 min 00 seconds
    [Setup]    change dir to sdk path
    Step  1  verify load SDK
    Step  2  to lt mode
    Step  3  check common ucode version
    [Teardown]  exit sdk mode

ALI_SDK_COMM_TC_016_10G_KR_Access_Test
    [Tags]     ALI_SDK_COMM_TC_016_10G_KR_Access_Test  migaloo
    [Timeout]  30 min 00 seconds
    [Setup]    change dir to sdk path
    Step  1  verify load SDK
    Step  2  to shell mode
    Step  3  change dir  ${diag_path}
    Step  4  test 10G KR
    [Teardown]  exit sdk mode


ALI_SDK_COMM_TC_017_Remote_Shell_Test
    [Tags]     ALI_SDK_COMM_TC_017_Remote_Shell_Test  migaloo
    [Timeout]  30 min 00 seconds
    [Setup]    change dir to sdk path
    Step  1  verify load SDK  -d
## @ISSUE find this issue on 10008:   cel_bcmshell ps cd
###bash: /usr/local/bin/cel_bcmshell: Permission denied
    Step  2  verify remote port status
    [Teardown]  exit sdk remote

ALI_SDK_COMM_TC_018_Temperature_Test
    [Tags]     ALI_SDK_COMM_TC_018_Temperature_Test  migaloo
    [Timeout]  30 min 00 seconds
    [Setup]    change dir to sdk path
    Step  1  verify load SDK
    Step  2  to lt mode
    Step  3  check hmon temperature
    Step  4  send command  exit
    Step  5  set 200g Soc
    Step  6  run cmd  ${let_CPU_send_package_cmd}  ${BCM_promptstr}
    Step  7  run cmd  sleep 60  ${BCM_promptstr}  timeout=100
    Step  8  to lt mode
    Step  9  check hmon temperature
    Step  10  send command  exit
    Step  11  run cmd  ${stop_traffic_cmd}  ${BCM_promptstr}
    [Teardown]  exit sdk mode

ALI_SDK_COMM_TC_023_SDK_Re-Init_Stress_Test
    [Tags]     ALI_SDK_COMM_TC_023_SDK_Re-Init_Stress_Test  migaloo
    [Timeout]  60 min 00 seconds
    [Setup]    change dir to sdk path
    FOR    ${INDEX}    IN RANGE    1    ${MAX_LOOP}
#        Print Loop Info  ${INDEX}  ${MAX_LOOP}
        Step  1  verify load SDK
        Step  2  check all port up status
        Step  3  set 200G soc
        Step  4  run cmd  ${clear_c_cmd}  ${BCM_promptstr}
        Step  5  run cmd  ${show_c_cmd}   ${BCM_promptstr}
        Step  6  run cmd  ${let_CPU_send_package_cmd}  ${BCM_promptstr}
        Step  7  run cmd  sleep 60  ${BCM_promptstr}  timeout=100
        Step  8  run cmd  ${stop_traffic_cmd}  ${BCM_promptstr}
        Step  9  check pkt counter
        Step  10  exit sdk mode
    END
    [Teardown]  exit sdk mode

ALI_SDK_COMM_TC_025_All_Ports_Disable/Enable_Stress_Test
    [Tags]     ALI_SDK_COMM_TC_025_All_Ports_Disable/Enable_Stress_Test  migaloo
    [Timeout]  60 min 00 seconds
    [Setup]    change dir to sdk path
    FOR    ${INDEX}    IN RANGE    1    ${MAX_LOOP}
        Step  1  verify load SDK
        Step  2  check all port up status
        Step  3  sendline  port cd en=0
        BuiltIn.Sleep  10
        Step  4  check all port down status
        Step  5  sendline  port cd en=1
        BuiltIn.Sleep  10
        Step  6  check all port up status
        Step  7  set 200G soc
        Step  8  run cmd  ${clear_c_cmd}  ${BCM_promptstr}
        Step  9  run cmd  ${show_c_cmd}   ${BCM_promptstr}
        Step  10  run cmd  ${let_CPU_send_package_cmd}  ${BCM_promptstr}
        Step  11  run cmd  sleep 60  ${BCM_promptstr}  timeout=100
        Step  12  run cmd  ${stop_traffic_cmd}  ${BCM_promptstr}
        Step  13  check pkt counter
        Step  14  exit sdk mode
    END
    [Teardown]  exit sdk mode

ALI_SDK_COMM_TC_026_Power_Cycle_Stress_Test
    [Tags]     ALI_SDK_COMM_TC_026_Power_Cycle_Stress_Test  migaloo
    [Timeout]  60 min 00 seconds
    [Setup]    change dir to sdk path
    FOR    ${INDEX}    IN RANGE    1    ${MAX_LOOP}
        Step  1  verify load SDK
        Step  2  check all port up status
        Step  3  to lt mode
        Step  4  check pcie phy fw info
        Step  5  send command  quit
        Step  6  set 200G soc
        Step  7  run cmd  ${clear_c_cmd}  ${BCM_promptstr}
        Step  8  run cmd  ${show_c_cmd}   ${BCM_promptstr}
        Step  9  run cmd  tx 1000 pbm=cd0 vlan=10 length=1280 SM=0x1 DM=0x2  ${BCM_promptstr}
        Step  10  run cmd  sleep 60  ${BCM_promptstr}  timeout=100
        Step  11  run cmd  ${stop_traffic_cmd}  ${BCM_promptstr}
        Step  12  check pkt counter
        Step  13  exit sdk mode
        BuiltIn.Sleep  15
        Step  14  power cycle sonic  ${diagos_mode}
        BuiltIn.Sleep  120
        change dir to sdk path
    END
    [Teardown]  Run Keywords
    ...  exit sdk mode  AND
    ...  recover cpu

*** Keywords ***
Connect Device
    Login Device

Disconnect Device
    Sdk Disconnect
