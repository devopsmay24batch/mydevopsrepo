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
# Script       : minipack3_sdk.robot                                                                                 #
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


MiniPack3_Test_TC_001_Load_and_Initialization_SDK_Test
    [Documentation]  This test checks SDK initialization
    [Tags]     MiniPack3_Test_TC_001_Load_and_Initialization_SDK_Test  minipack3
    [Timeout]  15 min 00 seconds
    [Setup]    change dir to sdk path
    Step  1  check sdk load and initialization  DUT  ${load_128x400}
    Step  2  check sdk load and initialization  DUT  ${load_128x200}
    Step  3  check sdk load and initialization  DUT  ${load_128x100}
    Step  4  check sdk load and initialization  DUT  ${load_64x400_64x200}
    Step  5  check sdk load and initialization  DUT  ${load_64x200_64x400}
    Step  6  check sdk load and initialization  DUT  ${load_64x800}
    [Teardown]  change to centos  DUT

MiniPack3_Test_SDK_TC_002_Version_Test
    [Documentation]  This test checks SDK version and release version
    [Tags]     MiniPack3_Test_SDK_TC_002_Version_Test  minipack3
    [Timeout]  5 min 00 seconds
    [Setup]    change dir to sdk path
    Step  1  check version sdk  DUT
    [Teardown]  change to centos from BCM Prompt  DUT

Minipack3_Test_SDK_TC_003_Default_Port_Info_Test
    [Documentation]  This test checks port default info with each speed.
    [Tags]     Minipack3_Test_SDK_TC_003_Default_Port_Info_Test  minipack3
    [Timeout]  25 min 00 seconds
    [Setup]    change dir to sdk path
    Step  1  test port default info  DUT  ${load_128x400}
    Step  2  test port default info  DUT  ${load_128x200}
    Step  3  test port default info  DUT  ${load_128x100}
    Step  4  test port default info  DUT  ${load_64x400_64x200}
    Step  5  test port default info  DUT  ${load_64x200_64x400}
    Step  6  test port default info  DUT  ${load_64x800}
    [Teardown]  change to centos  DUT

MiniPack3_Test_SDK_TC_004_Port_Status_Test_64x_2x400G
    [Documentation]  This test checks port default info with each speed.
    [Tags]     MiniPack3_Test_SDK_TC_004_Port_Status_Test_64x_2x400G  minipack3
    [Timeout]  25 min 00 seconds
    [Setup]    change dir to sdk path
    Step  1  check port status  DUT  ${load_128x400}  ${port_disable_cmd}  ${port_enable_cmd}
    [Teardown]  change to centos from BCM Prompt  DUT

MiniPack3_Test_SDK_TC_005_Port_Status_Test_64x_2x200G
    [Documentation]  This test checks port default info with each speed.
    [Tags]     MiniPack3_Test_SDK_TC_005_Port_Status_Test_64x_2x200G  minipack3
    [Timeout]  25 min 00 seconds
    [Setup]    change dir to sdk path
    Step  1  check port status  DUT  ${load_128x200}  ${port_disable_cmd}  ${port_enable_cmd}
    [Teardown]  change to centos from BCM Prompt  DUT

MiniPack3_Test_SDK_TC_006_Port_Status_Test_64x_2x100G
    [Documentation]  This test checks port default info with each speed.
    [Tags]     MiniPack3_Test_SDK_TC_006_Port_Status_Test_64x_2x100G  minipack3
    [Timeout]  25 min 00 seconds
    [Setup]    change dir to sdk path
    Step  1  check port status  DUT  ${load_128x100}  ${port_ce_disable_cmd}  ${port_ce_enable_cmd}
    [Teardown]  change to centos from BCM Prompt  DUT

MiniPack3_Test_SDK_TC_007_Port_Status_Test_64x400G_64x200G
    [Documentation]  This test checks port default info with each speed.
    [Tags]     MiniPack3_Test_SDK_TC_007_Port_Status_Test_64x400G_64x200G  minipack3
    [Timeout]  25 min 00 seconds
    [Setup]    change dir to sdk path
    Step  1  check port status  DUT  ${load_64x400_64x200}  ${port_disable_cmd}  ${port_enable_cmd}
    [Teardown]  change to centos from BCM Prompt  DUT

MiniPack3_Test_SDK_TC_008_Port_Status_Test_64x400G_64x200G
    [Documentation]  This test checks port default info with each speed.
    [Tags]     MiniPack3_Test_SDK_TC_008_Port_Status_Test_64x200G_64x400G  minipack3
    [Timeout]  25 min 00 seconds
    [Setup]    change dir to sdk path
    Step  1  check port status  DUT  ${load_64x200_64x400}  ${port_disable_cmd}  ${port_enable_cmd}
    [Teardown]  change to centos from BCM Prompt  DUT

MiniPack3_Test_SDK_TC_009_Port_Status_Test_64x800G
    [Documentation]  This test checks port default info with each speed.
    [Tags]     MiniPack3_Test_SDK_TC_009_Port_Status_Test_64x800G  minipack3
    [Timeout]  25 min 00 seconds
    [Setup]    change dir to sdk path
    Step  1  check port status  DUT  ${load_64x800}  ${port_d3c_disable_cmd}  ${port_d3c_enable_cmd}
    [Teardown]  change to centos from BCM Prompt  DUT
    

MiniPack3_Test_SDK_TC_010_PRBS_BER_Test_128x400G
    [Documentation]  This test checks port PRBS/BER test.
    [Tags]     MiniPack3_Test_SDK_TC_010_PRBS_BER_Test_128x400G  minipack3
    [Timeout]  25 min 00 seconds
    [Setup]    change dir to sdk path
    Step  1  check_port_PRBS_BER  DUT  ${load_128x400}
    [Teardown]  change to centos from BCM Prompt  DUT

MiniPack3_Test_SDK_TC_011_PRBS_BER_Test_128x200G
    [Documentation]  This test checks port PRBS/BER test.
    [Tags]     MiniPack3_Test_SDK_TC_011_PRBS_BER_Test_128x200G  minipack3
    [Timeout]  25 min 00 seconds
    [Setup]    change dir to sdk path
    Step  1  check_port_PRBS_BER  DUT  ${load_128x200}
    [Teardown]  change to centos from BCM Prompt  DUT

MiniPack3_Test_SDK_TC_012_PRBS_BER_Test_128x100G
    [Documentation]  This test checks port PRBS/BER test.
    [Tags]     MiniPack3_Test_SDK_TC_012_PRBS_BER_Test_128x100G  minipack3
    [Timeout]  25 min 00 seconds
    [Setup]    change dir to sdk path
    Step  1  check_port_PRBS_BER  DUT  ${load_128x100}
    [Teardown]  change to centos from BCM Prompt  DUT
    


MiniPack3_Test_SDK_TC_013_PRBS_BER_Test_64x400G_64x200G
    [Documentation]  This test checks port PRBS/BER test.
    [Tags]     MiniPack3_Test_SDK_TC_013_PRBS_BER_Test_64x400G_64x200G  minipack3
    [Timeout]  25 min 00 seconds
    [Setup]    change dir to sdk path
    Step  1  check_port_PRBS_BER  DUT  ${load_64x400_64x200}
    [Teardown]  change to centos from BCM Prompt  DUT
   

MiniPack3_Test_SDK_TC_014_PRBS_BER_Test_64x200G_64x400G
    [Documentation]  This test checks port PRBS/BER test.
    [Tags]     MiniPack3_Test_SDK_TC_014_PRBS_BER_Test_64x200G_64x400G  minipack3
    [Timeout]  25 min 00 seconds
    [Setup]    change dir to sdk path
    Step  1  check_port_PRBS_BER  DUT  ${load_64x200_64x400}
    [Teardown]  change to centos from BCM Prompt  DUT
   
MiniPack3_Test_SDK_TC_015_PRBS_BER_Test_64x800G
    [Documentation]  This test checks port PRBS/BER test.
    [Tags]     MiniPack3_Test_SDK_TC_015_PRBS_BER_Test_64x800G  minipack3
    [Timeout]  25 min 00 seconds
    [Setup]    change dir to sdk path
    Step  1  check_port_PRBS_BER  DUT  ${load_64x800}
    [Teardown]  change to centos from BCM Prompt  DUT
  
MiniPack3_Test_SDK_TC_016_L2_CPU_Traffic_Test_64x800G
    [Documentation]  This test checks CPU traffic test.
    [Tags]     MiniPack3_Test_SDK_TC_016_L2_CPU_Traffic_Test_64x800G  minipack3
    [Timeout]  25 min 00 seconds
    [Setup]    change dir to sdk path
    Step  1  check_l2_cpu_traffic  DUT  ${load_64x800}
    [Teardown]  change to centos from BCM Prompt  DUT


MiniPack3_Test_SDK_TC_017_L2_CPU_Traffic_Test_128x400G
    [Documentation]  This test checks CPU traffic test.
    [Tags]     MiniPack3_Test_SDK_TC_017_L2_CPU_Traffic_Test_128x400G  minipack3
    [Timeout]  25 min 00 seconds
    [Setup]    change dir to sdk path
    Step  1  check_l2_cpu_traffic  DUT  ${load_128x400}
    [Teardown]  change to centos from BCM Prompt  DUT

MiniPack3_Test_SDK_TC_018_L2_CPU_Traffic_Test_128x200G
    [Documentation]  This test checks CPU traffic test.
    [Tags]     MiniPack3_Test_SDK_TC_018_L2_CPU_Traffic_Test_128x200G  minipack3
    [Timeout]  25 min 00 seconds
    [Setup]    change dir to sdk path
    Step  1  check_l2_cpu_traffic  DUT  ${load_128x200}
    [Teardown]  change to centos from BCM Prompt  DUT

MiniPack3_Test_SDK_TC_019_L2_CPU_Traffic_Test_128x100G
    [Documentation]  This test checks CPU traffic test.
    [Tags]     MiniPack3_Test_SDK_TC_019_L2_CPU_Traffic_Test_128x100G  minipack3
    [Timeout]  25 min 00 seconds
    [Setup]    change dir to sdk path
    Step  1  check_l2_cpu_traffic  DUT  ${load_128x100}
    [Teardown]  change to centos from BCM Prompt  DUT

MiniPack3_Test_SDK_TC_020_L2_CPU_Traffic_Test_64x400G_64x200G
    [Documentation]  This test checks CPU traffic test.
    [Tags]     MiniPack3_Test_SDK_TC_020_L2_CPU_Traffic_Test_64x400G_64x200G  minipack3
    [Timeout]  25 min 00 seconds
    [Setup]    change dir to sdk path
    Step  1  check_l2_cpu_traffic  DUT  ${load_64x400_64x200}
    [Teardown]  change to centos from BCM Prompt  DUT

MiniPack3_Test_SDK_TC_021_L2_CPU_Traffic_Test_64x200G_64x400G
    [Documentation]  This test checks CPU traffic test.
    [Tags]     MiniPack3_Test_SDK_TC_021_L2_CPU_Traffic_Test_64x200G_64x400G  minipack3
    [Timeout]  25 min 00 seconds
    [Setup]    change dir to sdk path
    Step  1  check_l2_cpu_traffic  DUT  ${load_64x200_64x400}
    [Teardown]  change to centos from BCM Prompt  DUT

MiniPack3_Test_SDK_TC_022_Remote_Shell_Test
    [Documentation]  This test checks remote shell.
    [Tags]     MiniPack3_Test_SDK_TC_022_Remote_Shell_Test  minipack3
    [Timeout]  25 min 00 seconds
    [Setup]    change dir to sdk path
    Step  1  check_remote_shell  DUT 


MiniPack3_Test_SDK_TC_023_Serdes_FW_Test
    [Documentation]  This test checks serdes fw version.
    [Tags]     MiniPack3_Test_SDK_TC_023_Serdes_FW_Test  minipack3
    [Timeout]  25 min 00 seconds
    [Setup]    change dir to sdk path
    Step  1  check_serdes_fw  DUT  ${load_64x400_64x200}
    Step  2  check_serdes_fw  DUT  ${load_64x200_64x400}
    Step  3  check_serdes_fw  DUT  ${load_128x400}
    Step  4  check_serdes_fw  DUT  ${load_128x200}
    Step  5  check_serdes_fw  DUT  ${load_128x100}
    Step  6  check_serdes_fw  DUT  ${load_64x800}
    [Teardown]  change to centos  DUT

MiniPack3_Test_SDK_TC_024_Temperature_Test
    [Documentation]  This test checks temperature.
    [Tags]     MiniPack3_Test_SDK_TC_024_Temperature_Test  minipack3
    [Timeout]  25 min 00 seconds
    [Setup]    change dir to sdk path
    Step  1  check_temperature_sensors  DUT  ${load_64x800}  
    [Teardown]  change to centos from BCM Prompt  DUT


MiniPack3_Test_SDK_TC_025_Port_Loopback_Test
    [Documentation]  This test checks Port Loopback.
    [Tags]     MiniPack3_Test_SDK_TC_025_Port_Loopback_Test  minipack3
    [Timeout]  25 min 00 seconds
    [Setup]    change dir to sdk path
    Step  1  load_into_bcm_prompt  DUT  ${load_64x800} 
    Step  2  port_loopback_test  DUT  NONE 
    Step  3  port_loopback_test  DUT  PHY
    Step  4  port_loopback_test  DUT  EDB 
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

