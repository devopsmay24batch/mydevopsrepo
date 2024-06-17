##############################################################################
# LEGALESE:   "Copyright (C) 2019-2020, Celestica Corp. All rights reserved." #
#                                                                             #
# This source code is confidential, proprietary, and contains trade           #
# secrets that are the sole property of Celestica Corp.                       #
# Copy and/or distribution of this source code or disassembly or reverse      #
# engineering of the resultant object code are strictly forbidden without     #
# the written consent of Celestica Corp.                                      #
#                                                                             #
###############################################################################
#######################################################################################################################
# Script       : minerva_j3_sdk.robot                                                                                 #
# Date         : Feb 15, 2024                                                                                       #
# Author       : Harshit Khanna.                                                                                        #
# Description  : This script will validate SDK package for MiniPack3                                                 #
#                                                                                                                   #
# Script Revision Details:                                                                                            #
#
######################################################################################################################

*** Settings ***
Documentation       This Suite will validate SDK package

Force Tags        SDK
Library           SdkLibAdapter.py
Resource          Resource.robot
#Library           SdkLib.py  DUT
Variables         Sdk_variable.py

Suite Setup       Connect Device
Suite Teardown    Disconnect Device


*** Test Cases ***


Meta_Minerva_J3_SDK_TC_001_Load_and_Initialization_SDK_Test 
    [Documentation]  This test checks SDK initialization
    [Tags]     Meta_Minerva_J3_SDK_TC_001_Load_and_Initialization_SDK_Test  minervaJ3  
    [Timeout]  15 min 00 seconds
    [Setup]    change dir to sdk path
    Step  1  check sdk load and initialization  DUT  ${load_18x1x800}
    Step  2  check sdk load and initialization  DUT  ${load_18x1x400}
    Step  3  check sdk load and initialization  DUT  ${load_18x2x200}
    Step  4  check sdk load and initialization  DUT  ${load_18x2x100}
    Step  5  check sdk load and initialization  DUT  ${load_18x2x400}
    Step  5  check sdk load and initialization  DUT  ${load_18x4x100}
    Step  5  check sdk load and initialization  DUT  ${load_18x4x200}
    [Teardown]  change to centos  DUT
    
Meta_Minerva_J3_SDK_TC_002_Version_Test 
    [Documentation]  This test checks SDK version and release version
    [Tags]     Meta_Minerva_J3_SDK_TC_002_Version_Test  minervaJ3  
    [Timeout]  5 min 00 seconds
    [Setup]    change dir to sdk path
    Step  1  check version sdk  DUT
    [Teardown]  change to centos from BCM Prompt  DUT

Meta_Minerva_J3_SDK_TC_003_Default_Port_Info_Test
    [Documentation]  This test checks port default info with each speed.
    [Tags]     Meta_Minerva_J3_SDK_TC_003_Default_Port_Info_Test  minervaJ3  
    [Timeout]  25 min 00 seconds
    [Setup]    change dir to sdk path
    Step  1  test port default info  DUT  ${load_18x1x800}
    Step  2  test port default info  DUT  ${load_18x1x400}
    Step  3  test port default info  DUT  ${load_18x2x200}
    #Step  4  test port default info  DUT  ${load_18x2x100}
    Step  4  test port default info  DUT  ${load_18x2x400}
    #Step  5  test port default info  DUT  ${load_18x4x100}
    Step  5  test port default info  DUT  ${load_18x4x200}
    [Teardown]  change to centos  DUT

Meta_Minerva_J3_SDK_TC_004_Port_Status_Test_18x1x400G
    [Documentation]  This test checks port default info with each speed.
    [Tags]     Meta_Minerva_J3_SDK_TC_004_Port_Status_Test_18x1x400G  minervaJ3  
    [Timeout]  25 min 00 seconds
    [Setup]    change dir to sdk path
    Step  1  check port status  DUT  ${load_18x1x400}  ${port_disable_cmd}  ${port_enable_cmd}
    [Teardown]  change to centos from BCM Prompt  DUT

Meta_Minerva_J3_SDK_TC_005_Port_Status_Test_18x1x800G
    [Documentation]  This test checks port default info with each speed.
    [Tags]     Meta_Minerva_J3_SDK_TC_005_Port_Status_Test_18x1x800G  minervaJ3  
    [Timeout]  25 min 00 seconds
    [Setup]    change dir to sdk path
    Step  1  check port status  DUT  ${load_18x1x800}  ${port_disable_cmd}  ${port_enable_cmd}
    [Teardown]  change to centos from BCM Prompt  DUT

Meta_Minerva_J3_SDK_TC_006_Port_Status_Test_18x2x100G
    [Documentation]  This test checks port default info with each speed.
    [Tags]     Meta_Minerva_J3_SDK_TC_006_Port_Status_Test_18x2x100G  minervaJ3  
    [Timeout]  25 min 00 seconds
    [Setup]    change dir to sdk path
    Step  1  check port status  DUT  ${load_18x2x100}  ${port_disable_cmd}  ${port_enable_cmd}
    [Teardown]  change to centos from BCM Prompt  DUT

Meta_Minerva_J3_SDK_TC_007_Port_Status_Test_18x2x200G
    [Documentation]  This test checks port default info with each speed.
    [Tags]     Meta_Minerva_J3_SDK_TC_007_Port_Status_Test_18x2x200G  minervaJ3  
    [Timeout]  25 min 00 seconds
    [Setup]    change dir to sdk path
    Step  1  check port status  DUT  ${load_18x2x200}  ${port_disable_cmd}  ${port_enable_cmd}
    [Teardown]  change to centos from BCM Prompt  DUT

Meta_Minerva_J3_SDK_TC_008_Port_Status_Test_18x2x400G
    [Documentation]  This test checks port default info with each speed.
    [Tags]     Meta_Minerva_J3_SDK_TC_008_Port_Status_Test_18x2x400G  minervaJ3  
    [Timeout]  25 min 00 seconds
    [Setup]    change dir to sdk path
    Step  1  check port status  DUT  ${load_18x2x400}  ${port_disable_cmd}  ${port_enable_cmd}
    [Teardown]  change to centos from BCM Prompt  DUT


Meta_Minerva_J3_SDK_TC_009_Port_Status_Test_18x4x100G
    [Documentation]  This test checks port default info with each speed.
    [Tags]     Meta_Minerva_J3_SDK_TC_009_Port_Status_Test_18x4x100G  minervaJ3  
    [Timeout]  25 min 00 seconds
    [Setup]    change dir to sdk path
    Step  1  check port status  DUT  ${load_18x4x100}  ${port_disable_cmd}  ${port_enable_cmd}
    [Teardown]  change to centos from BCM Prompt  DUT

Meta_Minerva_J3_SDK_TC_010_Port_Status_Test_18x4x200G
    [Documentation]  This test checks port default info with each speed.
    [Tags]     Meta_Minerva_J3_SDK_TC_010_Port_Status_Test_18x4x200G  minervaJ3  
    [Timeout]  25 min 00 seconds
    [Setup]    change dir to sdk path
    Step  1  check port status  DUT  ${load_18x4x200}  ${port_disable_cmd}  ${port_enable_cmd}
    [Teardown]  change to centos from BCM Prompt  DUT


Meta_Minerva_J3_SDK_TC_011_PRBS_BER_Test_18x1x400G
    [Documentation]  This test checks port PRBS/BER test.
    [Tags]     Meta_Minerva_J3_SDK_TC_011_PRBS_BER_Test_18x1x400G  minervaJ3 
    [Timeout]  25 min 00 seconds
    [Setup]    change dir to sdk path
    Step  1  check_port_PRBS_BER  DUT  ${load_18x1x400}
    [Teardown]  change to centos from BCM Prompt  DUT

Meta_Minerva_J3_SDK_TC_012_PRBS_BER_Test_18x1x800G
    [Documentation]  This test checks port PRBS/BER test.
    [Tags]     Meta_Minerva_J3_SDK_TC_012_PRBS_BER_Test_18x1x800G  minervaJ3  
    [Timeout]  25 min 00 seconds
    [Setup]    change dir to sdk path
    Step  1  check_port_PRBS_BER  DUT  ${load_18x1x800}
    [Teardown]  change to centos from BCM Prompt  DUT

Meta_Minerva_J3_SDK_TC_013_PRBS_BER_Test_18x2x100G
    [Documentation]  This test checks port PRBS/BER test.
    [Tags]     Meta_Minerva_J3_SDK_TC_013_PRBS_BER_Test_18x2x100G  minervaJ3 
    [Timeout]  25 min 00 seconds
    [Setup]    change dir to sdk path
    Step  1  check_port_PRBS_BER  DUT  ${load_18x2x100}
    [Teardown]  change to centos from BCM Prompt  DUT


Meta_Minerva_J3_SDK_TC_014_PRBS_BER_Test_18x2x200G
    [Documentation]  This test checks port PRBS/BER test.
    [Tags]     Meta_Minerva_J3_SDK_TC_014_PRBS_BER_Test_18x2x200G  minervaJ3  
    [Timeout]  25 min 00 seconds
    [Setup]    change dir to sdk path
    Step  1  check_port_PRBS_BER  DUT  ${load_18x2x200}
    [Teardown]  change to centos from BCM Prompt  DUT

Meta_Minerva_J3_SDK_TC_015_PRBS_BER_Test_18x2x400G
    [Documentation]  This test checks port PRBS/BER test.
    [Tags]     Meta_Minerva_J3_SDK_TC_015_PRBS_BER_Test_18x2x400G  minervaJ3  
    [Timeout]  25 min 00 seconds
    [Setup]    change dir to sdk path
    Step  1  check_port_PRBS_BER  DUT  ${load_18x2x400}
    [Teardown]  change to centos from BCM Prompt  DUT


Meta_Minerva_J3_SDK_TC_016_PRBS_BER_Test_18x4x100G
    [Documentation]  This test checks port PRBS/BER test.
    [Tags]     Meta_Minerva_J3_SDK_TC_016_PRBS_BER_Test_18x4x100G  minervaJ3 
    [Timeout]  25 min 00 seconds
    [Setup]    change dir to sdk path
    Step  1  check_port_PRBS_BER  DUT  ${load_18x4x100}
    [Teardown]  change to centos from BCM Prompt  DUT

Meta_Minerva_J3_SDK_TC_017_PRBS_BER_Test_18x4x200G
    [Documentation]  This test checks port PRBS/BER test.
    [Tags]     Meta_Minerva_J3_SDK_TC_017_PRBS_BER_Test_18x4x200G  minervaJ3  
    [Timeout]  25 min 00 seconds
    [Setup]    change dir to sdk path
    Step  1  check_port_PRBS_BER  DUT  ${load_18x4x200}
    [Teardown]  change to centos from BCM Prompt  DUT

Meta_Minerva_J3_SDK_TC_018_L2_CPU_Traffic_Test_18x1x400G
    [Documentation]  This test checks CPU traffic test.
    [Tags]     Meta_Minerva_J3_SDK_TC_018_L2_CPU_Traffic_Test_18x1x400G  minervaJ3  
    [Timeout]  25 min 00 seconds
    [Setup]    change dir to sdk path
    Step  1  check_l2_cpu_traffic  DUT  ${load_18x1x400}
    [Teardown]  change to centos from BCM Prompt  DUT


Meta_Minerva_J3_SDK_TC_019_L2_CPU_Traffic_Test_18x1x800G
    [Documentation]  This test checks CPU traffic test.
    [Tags]     Meta_Minerva_J3_SDK_TC_019_L2_CPU_Traffic_Test_18x1x800G  minervaJ3  
    [Timeout]  25 min 00 seconds
    [Setup]    change dir to sdk path
    Step  1  check_l2_cpu_traffic  DUT  ${load_18x1x800}
    [Teardown]  change to centos from BCM Prompt  DUT

Meta_Minerva_J3_SDK_TC_020_L2_CPU_Traffic_Test_18x2x100G
    [Documentation]  This test checks CPU traffic test.
    [Tags]     Meta_Minerva_J3_SDK_TC_020_L2_CPU_Traffic_Test_18x2x100G  minervaJ3  
    [Timeout]  25 min 00 seconds
    [Setup]    change dir to sdk path
    Step  1  check_l2_cpu_traffic  DUT  ${load_18x2x100}
    [Teardown]  change to centos from BCM Prompt  DUT

Meta_Minerva_J3_SDK_TC_021_L2_CPU_Traffic_Test_18x2x200G
    [Documentation]  This test checks CPU traffic test.
    [Tags]     Meta_Minerva_J3_SDK_TC_021_L2_CPU_Traffic_Test_18x2x200G  minervaJ3 
    [Timeout]  25 min 00 seconds
    [Setup]    change dir to sdk path
    Step  1  check_l2_cpu_traffic  DUT  ${load_18x2x200}
    [Teardown]  change to centos from BCM Prompt  DUT

Meta_Minerva_J3_SDK_TC_022_L2_CPU_Traffic_Test_18x2x400G
    [Documentation]  This test checks CPU traffic test.
    [Tags]     Meta_Minerva_J3_SDK_TC_022_L2_CPU_Traffic_Test_18x2x400G  minervaJ3  
    [Timeout]  25 min 00 seconds
    [Setup]    change dir to sdk path
    Step  1  check_l2_cpu_traffic  DUT  ${load_18x2x400}
    [Teardown]  change to centos from BCM Prompt  DUT

Meta_Minerva_J3_SDK_TC_023_L2_CPU_Traffic_Test_18x4x100G
    [Documentation]  This test checks CPU traffic test.
    [Tags]     Meta_Minerva_J3_SDK_TC_023_L2_CPU_Traffic_Test_18x4x100G  minervaJ3  
    [Timeout]  25 min 00 seconds
    [Setup]    change dir to sdk path
    Step  1  check_l2_cpu_traffic  DUT  ${load_18x4x100}
    [Teardown]  change to centos from BCM Prompt  DUT

Meta_Minerva_J3_SDK_TC_024_L2_CPU_Traffic_Test_18x4x200G
    [Documentation]  This test checks CPU traffic test.
    [Tags]     Meta_Minerva_J3_SDK_TC_024_L2_CPU_Traffic_Test_18x4x200G  minervaJ3  
    [Timeout]  25 min 00 seconds
    [Setup]    change dir to sdk path
    Step  1  check_l2_cpu_traffic  DUT  ${load_18x4x200}
    [Teardown]  change to centos from BCM Prompt  DUT


Meta_Minerva_J3_SDK_TC_025_Serdes_FW_Test
    [Documentation]  This test checks serdes fw version.
    [Tags]     Meta_Minerva_J3_SDK_TC_025_Serdes_FW_Test  minervaJ3  
    [Timeout]  25 min 00 seconds
    [Setup]    change dir to sdk path
    Step  1  check_serdes_fw  DUT  ${load_18x1x800}
    Step  2  check_serdes_fw  DUT  ${load_18x1x400}
    Step  3  check_serdes_fw  DUT  ${load_18x2x200}
    Step  4  check_serdes_fw  DUT  ${load_18x2x100}
    Step  5  check_serdes_fw  DUT  ${load_18x2x400}
    Step  6  check_serdes_fw  DUT  ${load_18x4x100}
    Step  7  check_serdes_fw  DUT  ${load_18x4x200}
    [Teardown]  change to centos  DUT

Meta_Minerva_J3_SDK_TC_026_Temperature_Test
    [Documentation]  This test checks temperature.
    [Tags]     Meta_Minerva_J3_SDK_TC_026_Temperature_Test  minervaJ3 
    [Timeout]  25 min 00 seconds
    [Setup]    change dir to sdk path
    Step  1  check_temperature_sensors  DUT  ${load_18x1x800}
    [Teardown]  change to centos from BCM Prompt  DUT


Meta_Minerva_J3_SDK_TC_027_Port_Loopback_Test
    [Documentation]  This test checks Port Loopback.
    [Tags]     Meta_Minerva_J3_SDK_TC_027_Port_Loopback_Test  minervaJ3  
    [Timeout]  25 min 00 seconds
    [Setup]    change dir to sdk path
    Step  1  port_loopback_test  DUT  
    [Teardown]  change to centos  DUT


Meta_Minerva_J3_SDK_TC_043_ManuFacturing_Test
    [Documentation]  This is for manufacturing test.
    [Tags]     Meta_Minerva_J3_SDK_TC_043_ManuFacturing_Test  minervaJ3 
    [Setup]    change dir to sdk path
    Step  1  check_manufacturing_test  DUT  ${load_18x1x800}
    [Teardown]  change to centos from BCM Prompt  DUT





*** Keywords ***
Connect Device
    Set Library Order
    Sdk Device Connect
    Init Test Library
    SdkLibAdapter.ssh login bmc


Disconnect Device
    SdkLibAdapter.ssh disconnect
    SdkLibAdapter.Sdk Device Disconnect


