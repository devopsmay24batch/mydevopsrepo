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
# Script       : minipack2_sdk.robot                                                                                 #
# Date         : April 14, 2020                                                                                       #
# Author       : Prapatsorn W.                                                                                        #
# Description  : This script will validate SDK package for MINIPACK2                                                  #
#                                                                                                                   #
# Script Revision Details:                                                                                            #
#
######################################################################################################################

*** Settings ***
Documentation       This Suite will validate SDK package

Force Tags        SDK
Resource          Resource.robot
Library           SdkLibAdapter.py
Variables         Sdk_variable.py

Suite Setup       Connect Device
Suite Teardown    Disconnect Device


*** Test Cases ***
FB_SDK_BCM_COMM_TC_001_Load_and_Initialization_SDK_Test
    [Documentation]  This test checks SDK initialization
    [Tags]  FB_200G_SDK_BCM_COMM_TC_001_Load_and_Initialization_SDK_Test  minipack2  MP2_400G_SDK_BCM_COMM_TC_001_Load_and_Initialization_SDK_Test
    [Timeout]  5 min 00 seconds
    [Setup]  change dir to sdk path
    Step  1  verify load HSDK
    [Teardown]  exit BCM

FB_SDK_BCM_COMM_TC_002_Version_Test
    [Documentation]  This test checks BCM and PCIe version
    [Tags]  FB_200G_SDK_BCM_COMM_TC_002_Version_Test  minipack2  MP2_400G_SDK_BCM_COMM_TC_002_Version_Test
    [Timeout]  5 min 00 seconds
    [Setup]  change dir to sdk path
    Step  1  verify load HSDK
    Step  2  verify BCM version
    Step  3  enter SDKLT mode
    Step  4  verify PCIe version
    Step  5  exit SDKLT mode
    [Teardown]  exit BCM

FB_SDK_BCM_COMM_TC_003_TH4_Default_Port_Info_Test
    [Documentation]  This test checks SDK port info
    [Tags]  FB_200G_SDK_BCM_COMM_TC_003_TH4_Default_Port_Info_Test  minipack2  MP2_400G_SDK_BCM_COMM_TC_003_TH4_Default_Port_Info_Test
    [Timeout]  50 min 00 seconds
    [Setup]  change dir to sdk path
    Step  1  verify load HSDK  ${SDK_SCRIPT} -m 64x200_32x400
    Step  2  check all port status  port_status_pattern=${port_init_status}
    Step  3  exit BCM
    Step  4  verify load HSDK  ${SDK_SCRIPT} -m 128x200
    Step  5  check all port status  port_status_pattern=${port_init_status}
    Step  6  exit BCM
    Step  7  verify load HSDK  ${SDK_SCRIPT} -m 128x100
    Step  8  check all port status  port_status_pattern=${port_init_status}  port_cmd=${ps_ce_cmd}
    [Teardown]  exit BCM

FB_SDK_BCM_COMM_TC_004_Port_Status_Test_32x400G_64x200G
    [Documentation]  This test checks SDK port status
    [Tags]  FB_SDK_BCM_COMM_TC_004_Port_Status_Test_32x400G_64x200G  minipack2  MP2_400G_SDK_BCM_COMM_TC_004_Port_Status_Test
    [Timeout]  40 min 00 seconds
    [Setup]  change dir to sdk path
    ${pim_NA_count} =  check pim number
    Set Test Variable  ${pim_NA_count}  ${pim_NA_count}
    Step  1  verify remote shell  ${clean_xphy}  ${fail_dict}
    Step  2  startup default port group  init_cmd=${xphy_init_modex2}
    Run KeyWord If  ${pim_NA_count}==${3}   startup default port group  use_xphyback=False  init_cmd=${xphy_init_modey2_pim5}
    ...    ELSE IF  ${pim_NA_count}==${4}   No Operation
    ...    ELSE   startup default port group  use_xphyback=False  init_cmd=${xphy_init_modey2}
    Step  4  startup default port group  use_xphyback=False  init_cmd=${xphy_init_modez2}
    Step  5  verify load HSDK2
    Step  6  set port lb mac  ${speed_400G}  ${pim_NA_count}
    Step  7  check all port status
    Step  8  disable all ports
    Step  8  check all ports disabled
    Step  10  enable all ports
    Step  11  check all port status
    [Teardown]  exit BCM

FB_SDK_BCM_COMM_TC_007_PRBS_BER_Test_32x400G_64x200G
    [Documentation]  This test checks SDK port status
    [Tags]  FB_SDK_BCM_COMM_TC_007_PRBS_BER_Test_32x400G_64x200G  minipack2  MP2_400G_SDK_BCM_COMM_TC_007_PRBS_BER_Test
    [Timeout]  60 min 00 seconds
    [Setup]  change dir to sdk path
    ${pim_NA_count} =  check pim number
    Set Test Variable  ${pim_NA_count}  ${pim_NA_count}
    Step  1  verify remote shell  ${clean_xphy}  ${fail_dict}
    Step  2  startup default port group  init_cmd=${xphy_init_modex1}
    Run KeyWord If  ${pim_NA_count}==${3}   startup default port group  use_xphyback=False  init_cmd=${xphy_init_modey1_pim5}
    ...    ELSE IF  ${pim_NA_count}==${4}   No Operation
    ...    ELSE   startup default port group  use_xphyback=False  init_cmd=${xphy_init_modey1}
    Step  4  startup default port group  use_xphyback=False  init_cmd=${xphy_init_modez1}
    Step  5  startup default port group  use_xphyback=False  init_cmd=${xphy_init_modex2}
    Run KeyWord If  ${pim_NA_count}==3   startup default port group  use_xphyback=False  init_cmd=${xphy_init_modey2_pim5}
    ...    ELSE IF  ${pim_NA_count}==4   No Operation
    ...    ELSE   startup default port group  use_xphyback=False  init_cmd=${xphy_init_modey2}
    Step  7  startup default port group  use_xphyback=False  init_cmd=${xphy_init_modez2}
    Step  8  verify load HSDK2
    Step  9  set port lb mac  ${speed_400G}  ${pim_NA_count}
    Step  10  check all port status  ${port_up_status}
    Step  11  enter SDKLT mode
    Step  12  set prbs mode and run PRBS test
    Step  13  check BER level
    Step  14  exit SDKLT mode
    [Teardown]  exit BCM

FB_SDK_BCM_COMM_TC_010_L2_CPU_Traffic_Test_32x400G_64x200G
    [Documentation]  This test checks SDK port status
    [Tags]  FB_SDK_BCM_COMM_TC_010_L2_CPU_Traffic_Test_32x400G_64x200G  minipack2  MP2_400G_SDK_BCM_COMM_TC_010_L2_CPU_Traffic_Test
    [Timeout]  40 min 00 seconds
    [Setup]  change dir to sdk path
    ${len_port} =  verify TH4L or TH4
    Set Test Variable  ${len_port}  ${len_port}
    ${pim_NA_count} =  check pim number
    Set Test Variable  ${pim_NA_count}  ${pim_NA_count}
    Step  1  verify remote shell  ${clean_xphy}  ${fail_dict}
    Step  2  startup default port group  init_cmd=${xphy_init_modex2}
    Run KeyWord If  ${pim_NA_count}==3   startup default port group  use_xphyback=False  init_cmd=${xphy_init_modey2_pim5}
    ...    ELSE IF  ${pim_NA_count}==4   No Operation
    ...    ELSE   startup default port group  use_xphyback=False  init_cmd=${xphy_init_modey2}
    Step  4  startup default port group  use_xphyback=False  init_cmd=${xphy_init_modez2}
    Step  5  verify load HSDK2
    Step  4  set port lb mac  ${speed_400G}  ${pim_NA_count}
    Step  6  set snake vlan to all ports  ${set_snake_vlan_400G_cmd}
    Step  7  check all port status  ${portdump_pass_pattern}  ${portdump_status_cmd}
    Step  8  clear all port counter
    Step  9  let CPU send packages  port_cmd=${let_CPU_send_package_cd1_cmd}  port_len=${len_port}
    Step  10  let CPU send packages  port_cmd=${let_CPU_send_package_cd8_cmd}  port_len=${len_port}
    Step  11  sleep 300s
    Step  12  stop traffic  port_cmd=${stop_traffic_cd16_89_cmd}
    Step  13  stop traffic  port_cmd=${stop_traffic_cd17_80_cmd}
    [Teardown]  exit BCM

FB_SDK_BCM_COMM_TC_005_Port_Status_Test_128x200G
    [Documentation]  This test checks SDK port status
    [Tags]  FB_200G_SDK_BCM_COMM_TC_005_Port_Status_Test_128x200G  minipack2
    [Timeout]  40 min 00 seconds
    [Setup]  change dir to sdk path
    ${pim_NA_count} =  check pim number
    Set Test Variable  ${pim_NA_count}  ${pim_NA_count}
    Step  1  verify remote shell  ${clean_xphy}  ${fail_dict}
    Step  2  startup default port group
    Step  3  verify load HSDK
    Step  4  set port lb mac  ${speed_200G}  ${pim_NA_count}
    Step  5  check all port status
    Step  6  disable all ports
    Step  7  check all ports disabled
    Step  8  enable all ports
    Step  9  check all port status
    [Teardown]  exit BCM

FB_SDK_BCM_COMM_TC_008_PRBS_BER_Test_128x200G
    [Documentation]  This test checks PRBS result and BER level
    [Tags]  FB_200G_SDK_BCM_COMM_TC_008_PRBS_BER_Test_128x200G  minipack2
    [Timeout]  60 min 00 seconds
    [Setup]  change dir to sdk path
    ${pim_NA_count} =  check pim number
    Set Test Variable  ${pim_NA_count}  ${pim_NA_count}
    Step  1  verify remote shell  ${clean_xphy}  ${fail_dict}
    Step  2  startup default port group  init_cmd=${xphy_init_8pim_txfir2}
    Step  3  verify load HSDK
    Step  4  set port lb mac  ${speed_200G}  ${pim_NA_count}
    Step  5  check all port status  ${port_up_status}
    Step  6  enter SDKLT mode
    Step  7  set prbs mode and run PRBS test
    Step  8  check BER level
    Step  9  exit SDKLT mode
    [Teardown]  exit BCM

FB_SDK_BCM_COMM_TC_011_L2_CPU_Traffic_Test_128x200G
    [Documentation]  This test checks SDK CPU Traffic
    [Tags]  FB_200G_SDK_BCM_COMM_TC_011_L2_CPU_Traffic_Test_128x200G  minipack2  CPU_Traffic
    [Timeout]  30 min 00 seconds
    [Setup]  change dir to sdk path
    ${len_port} =  verify TH4L or TH4
    Set Test Variable  ${len_port}  ${len_port}
    ${pim_NA_count} =  check pim number
    Set Test Variable  ${pim_NA_count}  ${pim_NA_count}
    Step  1  startup default port group
    Step  2  verify load HSDK
    Step  3  set port lb mac  ${speed_200G}  ${pim_NA_count}
    Step  4  set snake vlan to all ports
    Step  5  check all port status  ${portdump_pass_pattern}  ${portdump_status_cmd}
    Step  6  clear all port counter
    Step  7  let CPU send packages  port_len=${len_port}
    Step  8  sleep 300s
    Step  9  stop traffic
    Step  10  check all port status  ${portdump_pass_pattern}  ${portdump_counters_cmd}
    [Teardown]  exit BCM

FB_SDK_BCM_COMM_TC_013_Remote_Shell_Test
    [Documentation]  This test checks SDK remote shell
    [Tags]  FB_200G_SDK_BCM_COMM_TC_013_Remote_Shell_Test  minipack2  MP2_400G_SDK_BCM_COMM_TC_013_Remote_Shell_Test
    [Timeout]  10 min 00 seconds
    [Setup]  change dir to sdk path
    Step  1  verify remote shell  ${remote_shell_load_sdk}  ${fail_dict}
    Step  2  verify remote shell port status
    Step  3  verify remote shell  ${cls_shell_exit}  ${fail_dict}
    Step  4  verify remote shell  ${check_bcm_user}  ${bcm_user}
    [Teardown]  check and exit BCM user

FB_SDK_BCM_COMM_TC_014_Serdes_FW_Test
    [Documentation]  This test checks SDK Serdes FW
    [Tags]  FB_200G_SDK_BCM_COMM_TC_014_Serdes_FW_Test  minipack2  MP2_400G_SDK_BCM_COMM_TC_014_Serdes_FW_Test
    [Timeout]  30 min 00 seconds
    [Setup]  change dir to sdk path
    Step  1  verify load HSDK
    Step  2  enter SDKLT mode
    Step  3  check lane common ucode version
    Step  4  exit SDKLT mode
    Step  5  exit BCM
    Step  6  verify load HSDK  ${load_128x100}
    Step  7  enter SDKLT mode
    Step  8  check lane common ucode version
    Step  9  exit SDKLT mode
    [Teardown]  exit BCM

FB_SDK_BCM_COMM_TC_015_Switch_Temperature_Test
    [Documentation]  This test checks SDK switch temperature
    [Tags]  FB_200G_SDK_BCM_COMM_TC_015_Switch_Temperature_Test  minipack2  CPU_Traffic
    [Timeout]  10 min 00 seconds
    [Setup]  change dir to sdk path
    ${len_port} =  verify TH4L or TH4
    Set Test Variable  ${len_port}  ${len_port}
    Step  1  verify load HSDK
    Step  2  enter SDKLT mode
    Step  3  check hmon temperature
    Step  4  exit SDKLT mode
    Step  5  set snake vlan to all ports
    Step  6  let CPU send packages  port_len=${len_port}
    Step  7  port sleep  60
    Step  8  enter SDKLT mode
    Step  9  check hmon temperature
    Step  10  exit SDKLT mode
    Step  11  stop traffic
    [Teardown]  exit BCM

FB_SDK_BCM_COMM_TC_016_10G_KR_Access_Test
    [Documentation]  This test checks SDK 10G KR traffice test with remote shell
    [Tags]  FB_200G_SDK_BCM_COMM_TC_016_10G_KR_Access_Test  minipack2  MP2_400G_SDK_BCM_COMM_TC_016_10G_KR_Access_Test
    [Timeout]  10 min 00 seconds
    [Setup]  change dir to sdk path
    Step  1  verify remote shell  ${remote_shell_load_sdk}  ${fail_dict}
    Step  2  verify remote shell  ${KR_10G_TEST}  ${KR_pass_pattern}  False
    Step  3  verify remote shell  ${cls_shell_exit}  ${fail_dict}
    [Teardown]  check and exit BCM user

FB_SDK_BCM_COMM_TC_006_Port_Status_Test_128x100G
    [Documentation]  This test checks SDK port status
    [Tags]  FB_200G_SDK_BCM_COMM_TC_006_Port_Status_Test_128x100G  minipack2
    [Timeout]  40 min 00 seconds
    [Setup]  change dir to sdk path
    ${pim_NA_count} =  check pim number
    Set Test Variable  ${pim_NA_count}  ${pim_NA_count}
    Step  1  verify remote shell  ${clean_xphy}  ${fail_dict}
    Step  2  startup default port group  init_cmd=${xphy_init_mode3_txfir2}
    Step  3  verify load HSDK  ${load_128x100}
    Step  4  set port lb mac  ${speed_100G}  ${pim_NA_count}
    Step  5  check all port status  ${port_up_status_100G}  ${ps_ce_cmd}
    Step  6  disable all ports  ${port_ce_disable_cmd}
    Step  7  check all ports disabled  ${ps_ce_cmd}
    Step  8  enable all ports  ${port_ce_enable_cmd}
    Step  9  check all port status  ${port_up_status_100G}  ${ps_ce_cmd}
    [Teardown]  exit BCM

FB_SDK_BCM_COMM_TC_009_PRBS_BER_Test_128x100G
    [Documentation]  This test checks PRBS result and BER level
    [Tags]  FB_200G_SDK_BCM_COMM_TC_009_PRBS_BER_Test_128x100G  minipack2
    [Timeout]  30 min 00 seconds
    [Setup]  change dir to sdk path
    ${pim_NA_count} =  check pim number
    Set Test Variable  ${pim_NA_count}  ${pim_NA_count}
    Run KeyWord If  ${pim_NA_count}==${3}   startup default port group  init_cmd=${xphy_init_mode3_d1_d2_pim5}
    ...    ELSE IF  ${pim_NA_count}==${4}   startup default port group  init_cmd=${xphy_init_mode3_d1_d2_pim4}
    ...    ELSE   startup default port group  init_cmd=${xphy_init_mode3_d1_d2}
    Step  2  verify load HSDK  ${load_128x100}
    Step  3  set port lb mac  ${speed_100G}  ${pim_NA_count}
    Step  4  check all port status  ${port_up_status_100G}  ${ps_ce_cmd}
    Step  5  enter SDKLT mode
    Step  6  set prbs mode and run PRBS test
    Step  7  check BER level
    Step  8  exit SDKLT mode
    [Teardown]  exit BCM

FB_SDK_BCM_COMM_TC_012_L2_CPU_Traffic_Test_128x100G
    [Documentation]  This test checks SDK CPU Traffic
    [Tags]  FB_200G_SDK_BCM_COMM_TC_012_L2_CPU_Traffic_Test_128x100G  minipack2  CPU_Traffic
    [Timeout]  30 min 00 seconds
    [Setup]  change dir to sdk path
    ${len_port} =  verify TH4L or TH4
    Set Test Variable  ${len_port}  ${len_port}
    ${pim_NA_count} =  check pim number
    Set Test Variable  ${pim_NA_count}  ${pim_NA_count}
    Step  1  startup default port group  init_cmd=${xphy_init_mode3}
    Step  2  verify load HSDK  ${load_128x100}
    Step  3  set snake vlan to all ports  ${set_snake_vlan_100G_cmd}
    Step  4  set port lb mac  ${speed_100G}  ${pim_NA_count}
    Step  5  check all port status  ${portdump_pass_pattern}  ${portdump_status_cmd}
    Step  6  clear all port counter
    Step  7  let CPU send packages  ${let_CPU_send_package_100G_cmd}  port_len=${len_port} 
    Step  8  sleep 300s
    Step  9  stop traffic  ${stop_traffic_ce127_cmd}
    Step  10  check all port status  ${portdump_pass_pattern}  ${portdump_counters_cmd}
    [Teardown]  exit BCM

FB_SDK_BCM_COMM_TC_017_TH4_Port_Loopback_Test(32x400G+64x200G)
    [Documentation]  This test checks SDK port loopback
    [Tags]  FB_200G_SDK_BCM_COMM_TC_017_TH4_Port_Loopback_Test_32x400G  minipack2  CPU_Traffic  MP2_400G_SDK_BCM_COMM_TC_017_TH4_Port_Loopback_Test
    [Timeout]  15 min 00 seconds
    [Setup]  change dir to sdk path
    ${len_port} =  verify TH4L or TH4
    Set Test Variable  ${len_port}  ${len_port}
    Step  1  scp file from PC  file_list=SOC_400G_file_list
    Step  2  verify load HSDK  ${load_64x200_32x400}
    Step  3  change port mode  ${port_mac_cmd}
    Step  4  check port mode setting  ${port_mac_status}
    Step  5  set snake vlan to all ports  ${set_snake_vlan_400G_cmd}
    Step  6  clear all port counter
    Step  7  let CPU send packages  ${let_CPU_send_package_cd1_cmd}  port_len=${len_port}
    Step  8  let CPU send packages  ${let_CPU_send_package_cd8_cmd}  port_len=${len_port}
    Step  9  port sleep  30
    Step  10  stop traffic  ${stop_traffic_cd53_cd57_cmd}
    Step  11  check all port status  ${portdump_pass_pattern}  ${portdump_counters_32_cmd}
    Step  12  check all port status  ${portdump_pass_pattern}  ${portdump_counters_64_cmd}
    [Teardown]  exit BCM

FB_SDK_BCM_COMM_TC_018_TH4_Port_Loopback_Test(128x200G)
    [Documentation]  This test checks SDK port loopback
    [Tags]  FB_200G_SDK_BCM_COMM_TC_018_TH4_Port_Loopback_Test_128x200G  minipack2  CPU_Traffic  MP2_400G_SDK_BCM_COMM_TC_018_TH4_Port_Loopback_Test
    [Timeout]  15 min 00 seconds
    [Setup]  change dir to sdk path
    ${len_port} =  verify TH4L or TH4
    Set Test Variable  ${len_port}  ${len_port}
    Step  1  verify load HSDK
    Step  2  change port mode  ${port_mac_cmd}
    Step  3  check port mode setting  ${port_mac_status}
    Step  4  set snake vlan to all ports
    Step  5  clear all port counter
    Step  6  let CPU send packages  port_len=${len_port}
    Step  7  port sleep  30
    Step  8  stop traffic
    Step  9  check all port status  ${portdump_pass_pattern}  ${portdump_counters_cmd}
    Step  10  exit BCM
    Step  11  verify load HSDK  ${startup_phy_cmd}
    Step  12  change port mode  ${port_phy_cmd}
    Step  13  check port mode setting  ${port_phy_status}
    Step  14  set snake vlan to all ports
    Step  15  clear all port counter
    Step  16  let CPU send packages  port_len=${len_port}
    Step  17  port sleep  30
    Step  18  stop traffic
    Step  19  check all port status  ${portdump_pass_pattern}  ${portdump_counters_cmd}
    [Teardown]  exit BCM

FB_SDK_BCM_COMM_TC_019_TH4_Port_Loopback_Test(128x100G)
    [Documentation]  This test checks SDK port loopback
    [Tags]  FB_200G_SDK_BCM_COMM_TC_019_TH4_Port_Loopback_Test_128x100G  minipack2  CPU_Traffic  MP2_400G_SDK_BCM_COMM_TC_019_TH4_Port_Loopback_Test
    [Timeout]  15 min 00 seconds
    [Setup]  change dir to sdk path
    ${len_port} =  verify TH4L or TH4
    Set Test Variable  ${len_port}  ${len_port}
    Step  1  verify load HSDK  ${load_128x100}
    Step  2  change port mode  ${port_ce_mac_cmd}
    Step  3  check port mode setting  ${port_ce_mac_status}  ${ps_ce_cmd}
    Step  4  set snake vlan to all ports  ${set_snake_vlan_100G_cmd}
    Step  5  clear all port counter
    Step  6  let CPU send packages  ${let_CPU_send_package_100G_cmd}  port_len=${len_port}
    Step  7  port sleep  30
    Step  8  stop traffic  ${stop_traffic_ce127_cmd}
    Step  9  check all port status  ${portdump_pass_pattern}  ${portdump_counters_cmd}
    [Teardown]  exit BCM

FB_SDK_MP2_TC_001_PHY_Initialization_Test
    [Documentation]  This test checks Retimer Initialization.
    [Tags]  FB_200G_SDK_MP2_TC_001_PHY_Initialization_Test  minipack2
    [Timeout]  30 min 00 seconds
    [Setup]  change dir to sdk path
    ${pim_NA_count} =  check pim number
    Set Test Variable  ${pim_NA_count}  ${pim_NA_count}
    Step  1  verify remote shell  ${clean_xphy}  ${fail_dict}
    Step  2  startup default port group
    Step  3  verify load HSDK
    Step  4  set port lb mac  ${speed_200G}  ${pim_NA_count}
    Step  5  check all port status  ${port_up_status}
    [Teardown]  exit BCM

FB_SDK_MP2_TC_002_PHY_Version_Test
    [Documentation]  This test checks PHY version information.
    [Tags]  FB_200G_SDK_MP2_TC_002_PHY_Version_Test  minipack2
    [Timeout]  30 min 00 seconds
    [Setup]  change dir to sdk path
    Step  1  verify remote shell  ${xphy_h}  ${fail_dict}
    Step  2  verify remote shell  ${xphy_h}  ${xphy_h_pattern}  False

*** Keywords ***
Connect Device
    Set Library Order
    Sdk Device Connect
    Init Test Library
    ssh login bmc

Disconnect Device
    ssh disconnect
    Sdk Device Disconnect


