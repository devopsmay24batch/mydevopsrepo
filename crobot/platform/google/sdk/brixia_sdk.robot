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
Documentation       This Suite will validate all brixia sdk functions:

Variables         GoogleSdkVariable.py
Library           GoogleSdkLib.py
Library          ../GoogleCommonLib.py
Library           CommonLib.py
Resource          GoogleSdkKeywords.robot

Suite Setup       DiagOS Connect Device
Suite Teardown    DiagOS Disconnect Device

*** Variables ***

@{mode_list} =  ${tool_32x8x50}  ${tool_64x4x100}  ${tool_256x1x100}

*** Test Cases ***
SDK_TC_001_xxxx
    [Documentation]  This test check sdk info
    [Tags]  SDK_TC_001_xxxx  brixia
    [Timeout]  60 min 00 seconds
    [Setup]  xxxx
    Step  1  check sdk info
    Step  2  xxxx
    [Teardown]  xxxx

BRIXIA_SDK_TC_01_Load_initialize_SDK_Test
   [Documentation]  This test checks the Loading and initialization of SDK modes
   [Tags]   BRIXIA_SDK_TC_01_Load_initialize_SDK_Test  brixia  
   Step  1  Change dir to sdk path
   Step  2  Load and initialize
   Step  3  exit from sdk

BRIXIA_SDK_TC_02_Version_Test
   [Documentation]  This test checks the BCM and PCIE Version
   [Tags]   BRIXIA_SDK_TC_02_Version_Test  brixia  
   Step  1  change dir to sdk path
   Step  2  enter into sdk   bcm.user  ${tool_32x8x50}
   Step  3  check bcm ver
   Step  4  PCIE ver check
   Step  5  exit from sdk 

BRIXIA_SDK_TC_03_Default_Port_info_Test
   [Documentation]  This test checks the Default Port info
   [Tags]   BRIXIA_SDK_TC_03_Default_Port_info_Test  brixia
   Step  1  Change dir to sdk path
   Step  2  Default port check
   Step  3  exit from sdk

BRIXIA_SDK_TC_04_32_2_400G_Port_Status_Test
   [Documentation]  This test checks 32_2_400G_Status Test
   [Tags]   BRIXIA_SDK_TC_04_32_2_400G_Port_Status_Test  brixia
   Step  1  change dir to sdk path
   Step  2  enter into sdk   bcm.user  ${tool_64x4x100}
   Step  3  check port status  64x4x100
   Step  4  disable port check   64x4x100
   Step  5  enable port check   64x4x100
   Step  6  exit from sdk

BRIXIA_SDK_TC_05_32_1_400G_Port_Status_Test
   [Documentation]  This test checks the 32x1x400G Port status
   [Tags]   BRIXIA_SDK_TC_05_32_1_400G_Port_Status_Test  brixia
   Step  1  change dir to sdk path
   Step  2  enter into sdk   bcm.user  ${tool_32x8x50}
   Step  3  check port status   32x8x50
   Step  4  disable port check   32x8x50
   Step  5  enable port check   32x8x50
   Step  6  exit from sdk

BRIXIA_SDK_TC_06_32_8_100G_Port_Status_Test
   [Documentation]  This test checks the 32x8x100G Port status
   [Tags]   BRIXIA_SDK_TC_06_32_8_100G_Port_Status_Test  brixia
   Step  1  change dir to sdk path
   Step  2  enter into sdk   bcm.user  ${tool_256x1x100}
   Step  3  check port status   256x1x100
   Step  4  disable port check   256x1x100
   Step  5  enable port check    256x1x100
   Step  6  exit from sdk


BRIXIA_SDK_TC_13_32x2x400G_Port_Loopback_Test
    [Documentation]  This test check SDK 32x2x400G Port Loopback Test
    [Tags]  BRIXIA_SDK_TC_13_32x2x400G_Port_Loopback_Test  brixia
    Step  1  change dir to sdk path
    Step  2  enter Into SDK  bcm.user  ${tool_64x4x100}
    Step  3  set Port And Check  ${port_mac_63_status_pattern}  ${cd_lb_cmd}  ${cd_ps_cmd}
    Step  4  run Snake Traffic Test  ${cd_snake_cmd}
    Step  5  check ports     64x4x100
    Step  6  send packet to all ports  ${cd_pckt_gen_cmd}  60
    Step  7  stop traffic and check counter  ${cd_stop_traffic.format(63)}
    Step  8  exit From Sdk

BRIXIA_SDK_TC_16_10G_KR_Port_Loopback_Test
    [Documentation]  This test checks 10G KR Port Loopback Test
    [Tags]  BRIXIA_SDK_TC_16_10G_KR_Port_Loopback_Test   brixia
    Step  1  change dir to sdk path
    Step  2  enter Into SDK  bcm.user  ${tool_64x4x100}
    Step  3  set port loopback   ${xe_mac_patn}  ${xe1_lb_cmd}  ${xe1_ps_cmd}
    Step  4  set snake vlan
    Step  5  check ports     64x4x100
    Step  6  send packet to all ports   ${xe_packt_gen_cmd}  60
    Step  7  stop traffic and check counter  ${xe_stop_traffic}
    Step  8  exit from sdk

BRIXIA_SDK_TC_10_32x2x400G_Port_BER_Test
    [Documentation]  This test check SDK 32x2x400G Port BER Test
    [Tags]  BRIXIA_SDK_TC_10_32x2x400G_Port_BER_Test  brixia
    Step  1  change dir to sdk path
    Step  2  enter Into SDK  bcm.user  ${tool_64x4x100}
    Step  3  run PRBS and BER test
    Step  4  stop PRBS and clear
    Step  5  Exit From Sdk

BRIXIA_SDK_TC_11_32x1x400G_Port_BER_Test
    [Documentation]  This test check SDK 32x1x800G Port BER Test
    [Tags]  BRIXIA_SDK_TC_11_32x1x400G_Port_BER_Test  brixia
    Step  1  change dir to sdk path
    Step  2  enter Into SDK  bcm.user  ${tool_32x8x50}
    Step  3  run PRBS and BER test
    Step  4  stop PRBS and clear
    Step  5  exit From Sdk

BRIXIA_SDK_TC_12_32x8x100G_Port_BER_Test
    [Documentation]  This test check SDK 32x8x100G Port BER Test
    [Tags]  BRIXIA_SDK_TC_12_32x8x100G_Port_BER_Test  brixia
    Step  1  change dir to sdk path
    Step  2  enter Into SDK  bcm.user  ${tool_256x1x100}
    Step  3  run PRBS and BER test
    Step  4  stop PRBS and clear
    Step  5  exit From Sdk

BRIXIA_SDK_TC_17_32_2_400G_Port_L2_CPU_Traffic_Test
   [Documentation]  This test checks the 400G Port L2 CPU Traffic Test
   [Tags]   BRIXIA_SDK_TC_17_32_2_400G_Port_L2_CPU_Traffic_Test  brixia
   Step  1  change dir to sdk path
   Step  2  enter into sdk  bcm.user  ${tool_64x4x100}
   Step  3  set Snake and check vlan   64x4x100   ${cd_snake_cmd}
   Step  4  check ports     64x4x100
   Step  5  send packet to all ports  ${cd_pckt_gen_cmd}  300
   Step  6  stop traffic and check counter  ${cd_stop_traffic.format(63)}
   Step  7  exit from sdk

BRIXIA_SDK_TC_18_32_1_400G_Port_L2_CPU_Traffic_Test
    [Documentation]  This test checks the 32_1 400G Port L2 CPU Traffic Test
    [Tags]   BRIXIA_SDK_TC_18_32_1_400G_Port_L2_CPU_Traffic_Test  brixia
    Step  1  change dir to sdk path
    Step  2  enter into sdk  bcm.user  ${tool_32x8x50}
    Step  3  set Snake and check vlan    32x8x50   ${snake_cmd_1}
    Step  4  check ports   32x8x50
    Step  5  send packet to all ports  ${cd_pckt_gen_cmd}  300
    Step  6  stop traffic and check counter  ${cd_stop_traffic.format(31)}
    Step  7  exit from sdk

BRIXIA_SDK_TC_19_32_8_100G_Port_L2_CPU_Traffic_Test
     [Documentation]  This test checks the 32_8 100G Port L2 CPU Traffic Test
     [Tags]   BRIXIA_SDK_TC_19_32_8_100G_Port_L2_CPU_Traffic_Test  brixia
     Step  1  change dir to sdk path
     Step  2  enter into sdk  bcm.user  ${tool_256x1x100}
     Step  3  set Snake and check vlan    256x1x100   ${snake_cmd_2}
     Step  4  check ports   256x1x100
     Step  5  send packet to all ports  ${ce_pckt_gen_cmd}  300
     Step  6  stop traffic and check counter  ${ce_stop_traffic.format(255)}
     Step  7  exit from sdk

BRIXIA_SDK_TC_25_10G_KR_PRBS_TEST
   [Documentation]  This test checks the PRBS Test
   [Tags]   BRIXIA_SDK_TC_25_10G_KR_PRBS_TEST  brixia
   [Setup]  change dir to sdk path
   Step  1  enter into sdk   bcm.user   ${tool_64x4x100}
   Step  2  set prbs and stop
   Step  3  exit from sdk

BRIXIA_SDK_TC_14_32x1x400G_Port_Loopback_Test
    [Documentation]  This test check SDK 32x1x400G Port Loopback Test
    [Tags]  BRIXIA_SDK_TC_14_32x1x400G_Port_Loopback_Test  brixia
    Step  1  change dir to sdk path
    Step  2  enter Into SDK  bcm.user  ${tool_32x8x50}
    Step  3  set Port And Check  ${port_mac_31_status_pattern}  ${cd_lb_cmd}  ${cd_ps_cmd}
    Step  4  run Snake Traffic Test  ${snake_cmd_1}
    Step  5  check ports     32x8x50
    Step  6  send packet to all ports  ${cd_pckt_gen_cmd}  60
    Step  7  stop traffic and check counter  ${cd_stop_traffic.format(31)}
    Step  8  exit From Sdk

BRIXIA_SDK_TC_15_32x8x100G_Port_Loopback_Test
    [Documentation]  This test check SDK 32x8x100G Port Loopback Test
    [Tags]  BRIXIA_SDK_TC_15_32x8x100G_Port_Loopback_Test  brixia
    Step  1  change dir to sdk path
    Step  2  enter Into SDK  bcm.user  ${tool_256x1x100}
    Step  3  set Port And Check  ${port_mac_255_status_pattern}  ${xe_lb_cmd}  ${xe_ps_cmd}
    Step  4  run Snake Traffic Test  ${xe_snake_cmd}
    Step  5  check ports     256x1x100
    Step  6  send packet to all ports  ${ce_pckt_gen_cmd}  60
    Step  7  stop traffic and check counter  ${ce_stop_traffic}
    Step  8  exit From Sdk

BRIXIA_SDK_TC_20_10G_KR_L2_CPU_Traffic_Test
    [Documentation]  This test check SDK 10G KR L2 CPU Traffic Test
    [Tags]  BRIXIA_SDK_TC_20_10G_KR_L2_CPU_Traffic_Test  brixia
    Step  1  change dir to sdk path
    Step  2  enter Into SDK  bcm.user  ${tool_64x4x100}
    Step  3  set and check vlan port
    Step  4  check ports     64x4x100
    Step  5  send packet to all ports  ${xe_packt_gen_cmd}  300
    Step  6  stop traffic and check counter  ${xe_stop_traffic}
    Step  7  exit From Sdk

BRIXIA_SDK_TC_029_SDK_Reinit_Stress_Test
    [Documentation]  This test check SDK Re-init Stress Test
    [Tags]  BRIXIA_SDK_TC_029_SDK_Reinit_Stress_Test   brixia
    ${loop_count}  Set Variable  ${2}
    Step  1  change dir to sdk path
    Step  2  run reinit stress test  ${loop_count}

BRIXIA_SDK_TC_30_2x400G_All_Ports_Enable/Disable_Stress_Test
    [Documentation]  This test check 2x400G All Ports Enable/Disable Stress Test
    [Tags]  BRIXIA_SDK_TC_30_2x400G_All_Ports_Enable/Disable_Stress_Test   brixia
    ${loop_count}  Set Variable  ${2}
    Step  1  change dir to sdk path
    Step  2  enter Into SDK  bcm.user  ${tool_64x4x100}
    FOR  ${each}  IN RANGE  ${loop_count}
        LOG TO CONSOLE  ------------------------ LOOP No. ${each+1} out of ${loop_count} ------------------------
        Step  3  check enabling disabling port
        Step  4  send packet to all ports  ${cd_pckt_gen_cmd}  60
        Step  5  stop traffic and check counter  ${cd_stop_traffic.format(63)}
    END
    Step  6  exit From Sdk

BRIXIA_SDK_TC_021_Switch_PCIE_FW_upgrade_Test
    [Documentation]  This test check SDK Switch PCIe firmware upgrade
    [Tags]  BRIXIA_SDK_TC_021_Switch_PCIE_FW_upgrade_Test  brixia
    Step  1  change dir to sdk path
    Step  2  enter Into SDK  bcm.user  ${tool_32x8x50}
    Step  3  check Current PCIe firmware
    Step  4  upgrade PCIe firmware and reboot
    Step  5  change dir to sdk path
    Step  6  enter Into SDK  bcm.user  ${tool_32x8x50}
    Step  7  check Current PCIe firmware  1
    Step  8  exit From Sdk

BRIXIA_SDK_TC_031_Power_Cycle_Stress_Test
    [Documentation]  This test check power cycle stress
    [Tags]  BRIXIA_SDK_TC_031_Power_Cycle_Stress_Test  brixia
    FOR  ${i}  IN RANGE  ${2}
        Step  1  change dir to sdk path
        Step  2  enter Into SDK  bcm.user  ${tool_64x4x100}
        Step  3  check port up status
        Step  4  send packet to all ports  ${cd_pckt_gen_cmd}  60
        Step  5  stop traffic and check counter  ${cd_stop_traffic.format(63)}
        Step  6  exit From Sdk
        Step  7  power cycle the device
    END

BRIXIA_SDK_TC_024_Serdes_FW_Test
    [Documentation]  This test check Serdes FW Test
    [Tags]  BRIXIA_SDK_TC_024_Serdes_FW_Test  brixia
    Step  1  change dir to sdk path
    FOR  ${each}  IN  @{mode_list}
        Step  2  enter Into SDK  bcm.user  ${each}
        Step  3  check serdes version
        Step  4  exit From Sdk
    END

BRIXIA_SDK_TC_26_Temperature_Test
   [Documentation]  This test checks the Temperature
   [Tags]   BRIXIA_SDK_TC_26_Temperature_Test  brixia
   Step  1  change dir to sdk path
   Step  2  enter Into SDK   bcm.user  ${tool_64x4x100}
   Step  3  set snake check Temp    ${cd_snake_cmd}
   Step  4  exit from sdk

BRIXIA_SDK_TC_27_Update_Positive_Voltage_Droop
   [Documentation]  This test updates the positive voltage droop
   [Tags]   BRIXIA_SDK_TC_27_Update_Positive_Voltage_Droop   brixia
   Step  1  change dir to sdk path
   Step  2  enter into sdk  bcm.user  ${tool_256x1x100}
   Step  3  Update Positive voltage droop
   Step  4  exit from sdk


*** Keywords ***
DiagOS Connect Device
    DiagOSConnect

DiagOS Disconnect Device
    DiagOSDisconnect

