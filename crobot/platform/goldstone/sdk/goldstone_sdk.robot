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

Variables         GoldstoneSdkVariable.py
Library           GoldstoneSdkLib.py
Library           ../diag/GoldstoneDiagLib.py
Library          ../GOLDSTONECommonLib.py
Library           CommonLib.py
Resource          GoldstoneSdkKeywords.robot

Suite Setup       DiagOS Connect Device
Suite Teardown    DiagOS Disconnect Device

*** Variables ***



*** Test Cases ***

Goldstone_sdk_port_status
    [Documentation]  This test checks the sdk port status for all modes
    ...              ELB's should be plugged to all OSFP ports before starting the test.
    [Tags]  Goldstone_SDK_1.0.3_Port_Status_Test  sdk  all_elb
    [Timeout]  120 min 00 seconds
    Step  1  go to diag path
    Step  2  check sysinfo test 
    Step  3  open sdk path  ${sdk_path}
    FOR   ${mode}   IN   @{portMap.keys()}
	Step  4  auto load user  ${mode}  backplane
	Step  5  check all port status  mode=${mode}
	Step  6  disable port  ${mode}  
	Step  7  check all port status  mode=${mode}  status=!ena
	Step  8  enable port  ${mode}
	Step  9  check all port status  mode=${mode}
	Step  10  exit auto load user
    END

Goldstone_sdk_all_port_en_disable_stress_test
    [Documentation]  Test case 1.0.35 This test checks the sdk port status for all modes
    ...              ELB's should be plugged to all OSFP ports before starting the test.
    [Tags]  Goldstone_sdk_all_port_en_disable_stress_test  1.0.37  sdk  all_elb
    [Timeout]  120 min 00 seconds
    Step  1  go to diag path
    Step  2  check sysinfo test 
    Step  3  open sdk path  ${sdk_path}
    FOR  ${i}  IN RANGE  10
	Step  4  auto load user  ${native_mode}  backplane
	Step  5  check all port status  mode=${native_mode}
	Step  6  disable port  ${native_mode}  
	Step  7  check all port status  mode=${native_mode}  status=!ena
	Step  8  enable port  ${native_mode}
	Step  9  check all port status  mode=${native_mode}
	Step  10  loopback_traffic_start  ${native_mode} 
	Step  11  loopback_traffic_stop_verify  mode=${native_mode}
	Step  12  exit auto load user
    END

Goldstone_sdk_each_port_en_disable_stress_test
    [Documentation]  Test case 1.0.36 This test checks the sdk port status for all modes
    ...              ELB's should be plugged to all OSFP ports before starting the test.
    [Tags]  Goldstone_sdk_each_port_en_disable_stress_test  1.0.38  sdk  all_elb
    [Timeout]  120 min 00 seconds
    Step  1  go to diag path
    Step  2  check sysinfo test 
    Step  3  open sdk path  ${sdk_path}
    FOR  ${i}  IN RANGE  10
	Step  4  auto load user  ${native_mode}  backplane
	Step  5  check all port status  mode=${native_mode}
	${portRange} =  Evaluate  $portMap['${native_mode}']['numPorts']
	FOR   ${i}   IN RANGE   ${portRange}
	    Step  6  disable port  ${native_mode}  ${i} 
        END
	Step  7  check all port status  mode=${native_mode}  status=!ena
	FOR   ${i}   IN RANGE   ${portRange}
	    Step  8  enable port  ${native_mode}  ${i}
        END
	Step  9  check all port status  mode=${native_mode}
	Step  10  loopback_traffic_start  ${native_mode} 
	Step  11  loopback_traffic_stop_verify  mode=${native_mode}
	Step  12  exit auto load user
    END

Goldstone_sdk_prbs_test
    [Documentation]  This test checks the sdk port status for all modes
    ...              ELB's should be plugged to all OSFP ports before starting the test.
    [Tags]  Goldstone_sdk_prbs_Test  sdk  all_elb
    [Timeout]  120 min 00 seconds
    Step  1  go to diag path
    Step  2  check sysinfo test 
    Step  3  open sdk path  ${sdk_path}
    FOR   ${mode}   IN   @{portMap.keys()}
	Step  4  auto load user  ${mode}  backplane
	Step  5  check all port status  mode=${mode}
	Step  6  run prbs test  ${mode}  maxBERepow=${maxBERepow} 
	Step  7  check all port status  mode=${mode}
	Step  8  exit auto load user
    END

Goldstone_sdk_serdes_version_test
    [Documentation]  This test checks the sdk serdes version status for all port modes
    ...              ELB's should be plugged to all OSFP ports before starting the test.
    [Tags]  Goldstone_sdk_serdes_version_test  sdk  1.0.22  all_elb
    [Timeout]  120 min 00 seconds
    Step  1  go to diag path
    Step  2  check sysinfo test 
    Step  3  open sdk path  ${sdk_path}
    FOR   ${mode}   IN   @{portMap.keys()}
	Step  4  auto load user  ${mode}  backplane
        Step  5  verify serdes version  mode=${mode}  serdesVersion=${serdes_version}
	Step  6  exit auto load user
    END

Goldstone_port_mapping_test
    [Documentation]  VISUAL INSPECTION REQUIRED WHILE RUNNING TEST FOR LED STATUS.
    ...              REST OF THE STEPS ARE COVERED IN AUTOMATION
    ...              Test case 1.0.4 This test checks the sdk port mapping for all modes.
    [Tags]  Goldstone_port_mapping_test  1.0.4  sdk  visual
    [Timeout]  120 min 00 seconds
    Step  1  go to diag path
    Step  2  check sysinfo test 
    Step  3  open sdk path  ${sdk_path}
    FOR   ${mode}   IN   @{portMap1.keys()}
	Step  4  auto load user  ${mode}  backplane
	Step  5  check all port status  mode=${mode}  verify=0
	${portRange} =  Evaluate  $portMap['${mode}']['numPorts']
	FOR   ${i}   IN RANGE   ${portRange}
	    Step  6  disable port  ${mode}  ${i} 
        END
	Step  7  check all port status  mode=${mode}  status=!ena
	FOR   ${i}   IN RANGE   ${portRange}
	    Step  8  enable port  ${mode}  ${i}
        END
	Step  9  check all port status  mode=${mode}  verify=0
	Step  12  exit auto load user
    END

Goldstone_P2P_snake_test
    [Documentation]  1.0.23-32 This test checks the DAC snake internal traffic.
    ...              All ports connect DAC as per the P2P Snake Internal traffic topology before starting the test. 
    [Tags]  Goldstone_P2P_snake_test  sdk  p2p_snake_internal 
    [Timeout]  120 min 00 seconds
    Step  1  go to diag path
    Step  2  check sysinfo test 
    Step  3  open sdk path  ${sdk_path}
    FOR   ${mode}   IN   @{portMap.keys()}
	Step  4  auto load user  ${mode}  copper
	Step  5  check all port status  mode=${mode}
	Step  6  p2p_internal_traffic_start  ${mode} 
	Step  7  p2p_internal_traffic_stop_verify  ${mode} 
	Step  8  check all port status  mode=${mode}
	Step  9  exit auto load user
    END

Goldstone_sdk_reinit_stress_test
    [Documentation]  Goldstone_sdk_reinit_stress_test  1.0.35
    ...              ELB's should be plugged to all OSFP ports before starting the test.
    [Tags]  Goldstone_sdk_reinit_stress_test  sdk  1.0.35  all_elb
    [Timeout]  120 min 00 seconds
    Step  1  go to diag path
    Step  2  check sysinfo test 
    Step  3  open sdk path  ${sdk_path}
    FOR  ${i}  IN RANGE  10
	Step  4  auto load user  ${native_mode}  backplane
	Step  5  check all port status  mode=${native_mode}
	Step  6  loopback_traffic_start  ${native_mode} 
	Step  7  loopback_traffic_stop_verify  ${native_mode}
	Step  8  check all port status  mode=${native_mode}
	Step  9  exit auto load user
    END
	
Goldstone_Internal_loopback_MAC_Mode_Traffic
    [Documentation]  This test checks the internal loopback traffic lb=MAC  1.0.51-62
    [Tags]   Goldstone_Internal_loopback_MAC_Mode_Traffic   sdk  common
    [Timeout]  120 min 00 seconds
    [Teardown]   exit auto load user 
    Step  1  go to diag path
    Step  2  check sysinfo test 
    Step  3  open sdk path  ${sdk_path}
    FOR   ${mode}   IN   @{portMap.keys()}
	Step  4  auto load user  ${mode}  backplane
	Step  5  check all port status  mode=${mode}
	Step  6  loopback_traffic_start  ${mode}  lb=${lb_mac}  
	Step  7  loopback_traffic_stop_verify  ${mode}
	Step  8  check all port status  mode=${mode}
	Step  9  exit auto load user
    END
	
Goldstone_ELB_CPU_Snake_Traffic
    [Documentation]  VISUAL INSPECTION REQUIRED WHILE RUNNING TEST FOR LED STATUS.
    ...              REST OF THE STEPS ARE COVERED IN AUTOMATION
    ...              This test checks all ports ELB CPU snake traffic   1.0.63-74
    ...              ELB's should be plugged to all OSFP ports before starting the test.
    [Tags]   Goldstone_ELB_CPU_Snake_Traffic   sdk  all_elb  visual
    [Timeout]  120 min 00 seconds
    [Teardown]   exit auto load user 
    Step  1  go to diag path
    Step  2  check sysinfo test 
    Step  3  open sdk path  ${sdk_path}
    FOR   ${mode}   IN   @{portMap.keys()}
	Step  4  auto load user  ${mode}  backplane
	Step  5  check all port status  mode=${mode}
	Step  6  loopback_traffic_start  ${mode}
	Step  7  loopback_traffic_stop_verify  ${mode}
	Step  8  check all port status  mode=${mode}
	Step  9  exit auto load user
    END

Goldstone_sdk_pcie_dma_stress_test
    [Documentation]  This tests the pcie dma stress 1.0.36
    [Tags]  Goldstone_sdk_pcie_dma_stress_test  sdk  1.0.36  common
    [Timeout]  120 min 00 seconds
    Step  1  go to diag path
    Step  2  check sysinfo test 
    Step  3  open sdk path  ${sdk_path}
    Step  4  auto load user  ${native_mode}  backplane
    FOR  ${i}  IN RANGE  10
	Step  5  run pcie dma test
    END

*** Keywords ***
DiagOS Connect Device
    DiagOSConnect

DiagOS Disconnect Device
    DiagOSDisconnect
