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
Documentation       This Suite will validate all Helga sdk functions:
Variables         HelgaSdkVariable.py
Library           HelgaSdkLib.py
Library          ../HelgaCommonLib.py
Library           CommonLib.py
Resource          HelgaSdkKeywords.robot

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

HELGA_SDK_TC_01_Load_initialize_SDK_Test
   [Documentation]  This test checks the Loading and initialization of SDK modes
   [Tags]   HELGA_SDK_TC_01_Load_initialize_SDK_Test  Helga_Load_Init  Helga_sdk_sanity 
   Step  1  Change dir to sdk path
   Step  2  Load and initialize
   Step  3  exit from sdk

HELGA_SDK_TC_02_Version_Test
   [Documentation]  This test checks the BCM and PCIE Version
   [Tags]   HELGA_SDK_TC_02_Version_Test  Helga_version  Helga_sdk_sanity
   Step  1  change dir to sdk path
   Step  2  enter into sdk   bcm.user  ${tool_256x1x100}
   Step  3  check bcm ver
   Step  4  PCIE ver check
   Step  5  exit from sdk 

HELGA_SDK_TC_03_Default_Port_info_Test
   [Documentation]  This test checks the Default Port info
   [Tags]   HELGA_SDK_TC_03_Default_Port_info_Test  helga_default  Helga_sdk_sanity
   Step  1  Change dir to sdk path
   Step  2  Default port check
   Step  3  exit from sdk

HELGA_SDK_TC_04_32_4_100G_Port_Status_Test
   [Documentation]  This test checks 32_4_100G_Status Test
   [Tags]   HELGA_SDK_TC_04_32_4_400G_Port_Status_Test  helga_32x4x100  Helga_sdk_sanity 
   Step  1  change dir to sdk path
   Step  2  enter into sdk   bcm.user  ${tool_64x4x100}
   Step  3  check port status  32x4x100
   Step  4  disable port check   32x4x100
   Step  5  enable port check   32x4x100
   Step  6  exit from sdk

HELGA_SDK_TC_05_64_2_100G_Port_Status_Test
   [Documentation]  This test checks 64_2_100G_Status Test
   [Tags]   HELGA_SDK_TC_05_64_2_100G_Port_Status_Test  helga_64x2x100  Helga_sdk_sanity
   Step  1  change dir to sdk path
   Step  2  enter into sdk   bcm.user  ${tool_64x2x100}
   Step  3  check port status  64x2x100
   Step  4  disable port check   64x2x100
   Step  5  enable port check   64x2x100
   Step  6  exit from sdk


HELGA_SDK_TC_06_128_1_100G_Port_Status_Test
   [Documentation]  This test checks the 128x1x100G Port status
   [Tags]   HELGA_SDK_TC_06_128_1_100G_Port_Status_Test  helga_128x1x100  Helga_sdk_sanity
   Step  1  change dir to sdk path
   Step  2  enter into sdk   bcm.user  ${tool_256x1x100}
   Step  3  check port status   128x1x100
   Step  4  disable port check   128x1x100
   Step  5  enable port check    128x1x100
   Step  6  exit from sdk


HELGA_SDK_TC_11_16x2x400G_Port_Loopback_Test
    [Documentation]  This test check SDK 16x2x400G Port Loopback Test with and without loopback
    [Tags]  HELGA_SDK_TC_11_32x2x400G_Port_Loopback_Test  Helga_16_2_400_loop  Helga_sdk_sanity
    Step  1  change dir to sdk path
    Step  2  enter Into SDK  bcm.user  ${tool_64x4x100}
    Step  3  set Port And Check  ${port_mac_63_status_pattern}  ${cd_lb_cmd}  ${cd_ps_cmd}
    Step  4  run Snake Traffic Test  ${cd_snake_cmd}
    Step  5  check ports     32x4x100
    Step  6  send packet to all ports  ${cd_pckt_gen_cmd}  60
    Step  7  stop traffic and check counter  ${cd_stop_traffic.format(31)}
    Step  8  exit from sdk
    Step  9  enter Into SDK  bcm.user  ${tool_64x4x100}
    Step  a  check ports     32x4x100
    Step  b  run Snake Traffic Test  ${cd_snake_cmd}
    Step  c  send packet to all ports  ${cd_pckt_gen_cmd}  120
    Step  d  stop traffic and check counter  ${cd_stop_traffic.format(31)}
    Step  e  exit from sdk

HELGA_SDK_TC_12_16x8x50G_Port_Loopback_Test
    [Documentation]  This test check SDK 16x8x50G Port Loopback Test with and without loopback
    [Tags]  HELGA_SDK_TC_11_16x8x400G_Port_Loopback_Test  Helga_16_8_50_loop  Helga_sdk_sanity
    Step  1  change dir to sdk path
    Step  2  enter Into SDK  bcm.user  ${tool_32x8x50}
    Step  3  set Port And Check  ${port_mac_63_status_pattern}  ${cd_lb_cmd}  ${cd_ps_cmd}
    Step  4  run Snake Traffic Test  ${cd_snake_cmd_16_8_50}
    Step  5  check ports     16x8x50
    Step  6  send packet to all ports  ${cd_pckt_gen_cmd}  60
    Step  7  stop traffic and check counter  ${cd_stop_traffic.format(15)}
    Step  8  exit from sdk
    Step  9  enter Into SDK  bcm.user  ${tool_32x8x50}
    Step  a  check ports     16x8x50
    Step  b  run Snake Traffic Test  ${cd_snake_cmd_16_8_50}
    Step  c  send packet to all ports  ${cd_pckt_gen_cmd}  120
    Step  d  stop traffic and check counter  ${cd_stop_traffic.format(15)}
    Step  e  exit from sdk

HELGA_SDK_TC_13_128x1x100G_Port_Loopback_Test
    [Documentation]  This test check SDK 128x1x100G Port Loopback Test with and without loopback
    [Tags]  HELGA_SDK_TC_13_128x1x100G_Port_Loopback_Test  Helga_128_1_100_loop  Helga_sdk_sanity
    Step  1  change dir to sdk path
    Step  2  enter Into SDK  bcm.user  ${tool_256x1x100}
    Step  3  set Port And Check  ${port_mac_63_status_pattern}  ${ce_lb_cmd}  ${ce_ps_cmd}
    Step  4  run Snake Traffic Test  ${cd_snake_cmd_128_nondac}
    Step  5  check ports     128x1x100
    Step  6  send packet to all ports  ${ce_pckt_gen_cmd}  120
    Step  7  stop traffic and check counter  ${cd_stop_traffic_128.format(127)}
    Step  8  exit from sdk
    Step  9  enter Into SDK  bcm.user  ${tool_256x1x100}
    Step  a  check ports     128x1x100
    Step  b  check_prbs_and_exit     128x1x100
    Step  c  run Snake Traffic Test  ${cd_snake_cmd_128_nondac}
    Step  d  send packet to all ports  ${ce_pckt_gen_cmd}  180
    Step  e  stop traffic and check counter  ${cd_stop_traffic_128.format(127)}
    Step  f  exit from sdk

HELGA_SDK_TC_14_10G_KR_Port_Loopback_Test
    [Documentation]  This test checks 10G KR Port Loopback Test
    [Tags]  HELGA_SDK_TC_14_10G_KR_Port_Loopback_Test   helga_10kr  Helga_sdk_sanity
    Step  1  change dir to sdk path
    Step  2  enter Into SDK  bcm.user  ${tool_64x4x100}
    Step  3  set port loopback   ${xe_mac_patn}  ${xe1_lb_cmd}  ${xe1_ps_cmd}
    #Step  4  set snake vlan
    Step  4  check ports     32x4x100
    Step  5  run Snake Traffic Test  ${cd_snake_cmd}
    Step  6  send packet to all ports   ${xe_packt_gen_cmd}  60
    Step  7  stop traffic and check counter  ${xe_stop_traffic}
    Step  8  exit from sdk


HELGA_SDK_TC_10_128x8x100G_Port_BER_Test
    [Documentation]  This test check SDK 128x8x100G Port BER Test
    [Tags]  HELGA_SDK_TC_10_128x8x100G_Port_BER_Test  helga_128_ber  Helga_sdk_sanity
    Step  1  change dir to sdk path
    Step  2  enter Into SDK  bcm.user  ${tool_256x1x100}
    Step  3  run PRBS and BER test
    Step  4  stop PRBS and clear
    Step  5  exit From Sdk

HELGA_SDK_TC_21_32_2_400G_Port_L2_CPU_Traffic_Test
   [Documentation]  This test checks the 400G Port L2 CPU Traffic Test
   [Tags]   HELGA_SDK_TC_21_32_2_400G_Port_L2_CPU_Traffic_Test  brixia   helga_soak  Helga_sdk_sanity
   Step  1  change dir to sdk path
   Step  2  enter into sdk  bcm.user  ${tool_64x4x100}
   Step  3  set Snake and check vlan   32x4x100   ${cd_snake_cmd}
   Step  4  check ports     32x4x100
   Step  5  send packet to all ports  ${cd_pckt_gen_cmd}  60
   Step  6  stop traffic and check counter  ${cd_stop_traffic.format(31)}
   Step  7  exit from sdk

HELGA_SDK_TC_21_32_8_100G_Port_L2_CPU_Traffic_Test_DAC
   [Documentation]  This test checks the 400G Port L2 CPU Traffic Test
   [Tags]   HELGA_SDK_TC_21_32_8_100G_Port_L2_CPU_Traffic_Test  brixia   helga_soak_dac
   #[Timeout]  1200 mins 00 seconds
   [Timeout]  None
   #[Timeout]
   #[Timeout]  72000 seconds 
   Step  1  change dir to sdk path
   Step  2  enter into sdk  bcm.user  ${tool_256x1x100}
   Step  3  check ports     128x1x100
   Step  4  set Snake and check vlan dac   128x1x100   ${cd_snake_cmd_128}
   Step  5  check ports     128x1x100
   #Step  6  send packet to all ports  ${cd_pckt_gen_cmd}  60
   #Step  7  stop traffic and check counter  ${cd_stop_traffic_128.format(127)}
   Step  8  exit from sdk


HELGA_SDK_TC_18_10G_KR_PRBS_TEST
   [Documentation]  This test checks the PRBS Test on 10G port
   [Tags]   HELGA_SDK_TC_18_10G_KR_PRBS_TEST  helga_10g_prbs  Helga_sdk_sanity
   [Setup]  change dir to sdk path
   Step  1  enter into sdk   bcm.user   ${tool_64x4x100}
   Step  2  set prbs and stop
   Step  3  exit from sdk

Helga_SDK_TC_029_SDK_Reinit_Stress_Test
    [Documentation]  This test check SDK Re-init Stress Test
    [Tags]  BRIXIA_SDK_TC_029_SDK_Reinit_Stress_Test   brixia	helga  helga_sdk_stress
    Step  1  sdk_reinit
    FOR  ${i}  IN RANGE  1  10
    	Step  2  run reinit stress test modify  2
    END


HELGA_SDK_TC_30_2x400G_All_Ports_Enable/Disable_Stress_Test
    [Documentation]  This test check 2x400G All Ports Enable/Disable Stress Test
    [Tags]  BRIXIA_SDK_TC_30_2x400G_All_Ports_Enable/Disable_Stress_Test   brixia  helga_port_disable  helga_sdk_stress
    ${loop_count}  Set Variable  ${10}
    Step  1  change dir to sdk path
    Step  2  enter Into SDK  bcm.user  ${tool_64x4x100}
    FOR  ${each}  IN RANGE  ${loop_count}
        LOG TO CONSOLE  ------------------------ LOOP No. ${each+1} out of ${loop_count} ------------------------
        Step  3  check enabling disabling port
        Step  4  run Snake Traffic Test  ${cd_snake_cmd}
        Step  5  send packet to all ports  ${cd_pckt_gen_cmd}  60
        Step  6  stop traffic and check counter  ${cd_stop_traffic.format(31)}
    END
    Step  7  exit From Sdk


HELGA_SDK_TC_024_Power_Cycle_Stress_Test
    [Documentation]  This test check power cycle stress
    [Tags]  Helga_SDK_TC_031_Power_Cycle_Stress_Test  Helga_power_cycle  helga_sdk_stress
    FOR  ${i}  IN RANGE  ${100}
        Step  1  change dir to sdk path
        Step  2  enter Into SDK  bcm.user  ${tool_64x4x100}
        Step  3  check port up status
        Step  4  run Snake Traffic Test  ${cd_snake_cmd}
        Step  5  send packet to all ports 180  ${cd_pckt_gen_cmd_180}  10
        #Step  6  stop traffic and check counter 180  ${cd_stop_traffic.format(31)}
        Step  7  exit From Sdk
        LOG TO CONSOLE  ------------------------ Sleeping for 20 seconds ------------------------
        BuiltIn.Sleep  20
        Step  8  power cycle the helga
    END

HELGA_SDK_TC_024_Power_Cycle_Stress_Test_off_on
    [Documentation]  This test check power cycle stress
    [Tags]  Helga_SDK_TC_031_Power_Cycle_Stress_Test  Helga_power_cycle1  helga_sdk_stress
    FOR  ${i}  IN RANGE  ${50}
        Step  1  change dir to sdk path
        Step  2  enter Into SDK  bcm.user  ${tool_64x4x100}
        Step  3  check port up status
        Step  4  check enabling disabling port
        Step  5  run Snake Traffic Test  ${cd_snake_cmd}
        Step  6  send packet to all ports 180  ${cd_pckt_gen_cmd_180}  10
        #Step  6  stop traffic and check counter 180  ${cd_stop_traffic.format(31)}
        Step  7  exit From Sdk
        #LOG TO CONSOLE  ------------------------ Sleeping for 20 seconds ------------------------
        BuiltIn.Sleep  20
        Step  8  powercycle helga  10.208.84.38   16
    END

HELGA_SDK_TC_025_Warm_Reboot_Stress_Test
    [Documentation]  This test check warm reboot case
    [Tags]  brixia  Helga_warm  helga_sdk_stress 
    [Timeout]  None
    FOR  ${i}  IN RANGE  ${25}
        LOG TO CONSOLE  ------------------------ LOOP No. ${i+1} ------------------------
        Step  1  change dir to sdk path
        #Step  2  enter Into SDK  bcm.user  ${tool_64x4x100}
        #Step  3  check port up status
        #Step  4  check enabling disabling port
        #Step  5  run Snake Traffic Test  ${cd_snake_cmd}
        #Step  6  send packet to all ports  ${cd_pckt_gen_cmd}  60
        #Step  7  stop traffic and check counter  ${cd_stop_traffic.format(31)}
        #Step  8  exit From Sdk
        Step  9  reboot the device
    END

HELGA_SDK_TC_026_Cold_Reboot_Stress_Test
    [Documentation]  This test check cold reboot case
    [Tags]  brixia  Helga_reboot  helga_sdk_stress 
    [Timeout]  None
    FOR  ${i}  IN RANGE  ${100}
        LOG TO CONSOLE  ------------------------ LOOP No. ${i+1} ------------------------
        Step  1  change dir to sdk path
        Step  2  enter Into SDK  bcm.user  ${tool_64x4x100}
        Step  3  check port up status
        Step  4  check enabling disabling port
        Step  5  run Snake Traffic Test  ${cd_snake_cmd}
        Step  6  send packet to all ports  ${cd_pckt_gen_cmd}  60
        Step  7  stop traffic and check counter  ${cd_stop_traffic.format(31)}
        Step  8  exit From Sdk
        Step  9  reboot the device
    END


*** Keywords ***
DiagOS Connect Device
    DiagOSConnect

DiagOS Disconnect Device
    DiagOSDisconnect

