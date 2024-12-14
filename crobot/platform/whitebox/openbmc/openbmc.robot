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
#######################################################################################################################
# Script       : openbmc.robot                                                                                        #
# Date         : July 29, 2023                                                                                        #
# Author       : Hui Gong <huigon@celestica.com>                                                                      #
# Description  : This script will validate openbmc                                                                    #
#                                                                                                                     #
# Script Revision Details:                                                                                            #
#   Initial Draft for openbmc testing                                                                                 #
#######################################################################################################################

*** Settings ***
Documentation       Tests to verify openbmc functions described in the openbmc function SPEC for the whiteboxproject.

# Force Tags        openbmc
Variables         openbmc_variable.py
Library           ../WhiteboxLibAdapter.py
# Library           bios_menu_lib.py
Resource          openbmc_keywords.robot
Resource          CommonResource.robot

Suite Setup    get all the variables
#Suite Teardown

#Test Setup
#Test Teardown

*** Variables ***
# It is recommended to use <{ScriptName}|{FeatureName}|{DomainName}_Variable> file for variable declaration with help of
# setting table. This section should keep blank.
#In extreme case if script requires variable then it should be defined in this table with documentaiton tag

*** Test Cases ***
# *** comment ***

CONSR-OBMC-BSFC-0001-0001
    [Documentation]  This test checks Function_001_BMC Image MD5 Check (TBD/NOT SUPPORT/MANUAL TEST)
    [Tags]     CONSR-OBMC-BSFC-0001-0001
    [Timeout]  30 min 00 seconds

CONSR-OBMC-BSFC-0002-0001
    [Documentation]  This test checks openbmc Version
    [Tags]     CONSR-OBMC-BSFC-0002-0001  Artemis_U2  robot:skip  # TODO: AC serial console issues
    [Timeout]  30 min 00 seconds
    Sub-Case  CONSR-OBMC-BSFC-0002-0001_1  check BMC Version after mc reset
    Sub-Case  CONSR-OBMC-BSFC-0002-0001_2  check BMC Version after ac cycle

CONSR-OBMC-BSFC-0003-0001
    [Documentation]  This test checks KCS Function
    [Tags]     CONSR-OBMC-BSFC-0003-0001  Artemis_U2
    [Timeout]  30 min 00 seconds
    Sub-Case  CONSR-OBMC-BSFC-0003-0001_1  check KCS Communicate
    Sub-Case  CONSR-OBMC-BSFC-0003-0001_2  check KCS Interface
#    Sub-Case  CONSR-OBMC-BSFC-0003-0001_3  check openbmc in bios via KCS

CONSR-OBMC-BSFC-0004-0001
    [Documentation]  This test checks openBMC SOL Activating Test
    [Tags]     CONSR-OBMC-BSFC-0004-0001  Artemis_U2
    [Timeout]  6 min 00 seconds
    Sub-Case  CONSR-OBMC-BSFC-0004-0001_1  Check openBMC SOL Activating Test

CONSR-OBMC-BSFC-0005-0001
    [Documentation]  This test checks Function_005_SOL Activating Test (TBD/NOT SUPPORT/MANUAL TEST)
    [Tags]     CONSR-OBMC-BSFC-0005-0001
    [Timeout]  6 min 00 seconds

CONSR-OBMC-BSFC-0006-0001
    [Documentation]  This test checks Function_006_SOL Authentication Test (TBD/NOT SUPPORT/MANUAL TEST)
    [Tags]     CONSR-OBMC-BSFC-0006-0001
    [Timeout]  6 min 00 seconds

CONSR-OBMC-BSFC-0007-0001
    [Documentation]  This test checks User Name and Password Check
    [Tags]     CONSR-OBMC-BSFC-0007-0001  Artemis
    [Timeout]  40 min 00 seconds
    #[Setup]  get all the variables
    Sub-Case  CONSR-OBMC-BSFC-0007-0001_1  User Name and Password Check
    [Teardown]  Restore the user list

CONSR-OBMC-BSFC-0008-0001
    [Documentation]  This test checks Function_005_User Privilege Check
    [Tags]     CONSR-OBMC-BSFC-0008-0001  Artemis
    [Timeout]  40 min 00 seconds
    #[Setup]  get all the variables
    Sub-Case  CONSR-OBMC-BSFC-0008-0001_1  User Privilege Check

CONSR-OBMC-BSFC-0009-0001
    [Documentation]  This test checks Function_006_Power Status
    [Tags]     CONSR-OBMC-BSFC-0009-0001  Artemis_U2
    [Timeout]  30 min 00 seconds
    Sub-Case  CONSR-OBMC-BSFC-0009-0001_1  Power Status Power Off and Power On
    Sub-Case  CONSR-OBMC-BSFC-0009-0001_2  Power Status Power Cycle
    [Teardown]  Run Keyword If Test Failed  restore_system_power  ${DeviceName}

CONSR-OBMC-BSFC-0010-0001
    [Documentation]  This test checks Function_007_Power Control
    [Tags]     CONSR-OBMC-BSFC-0010-0001  Artemis_U2
    [Timeout]  30 min 00 seconds
    Sub-Case  CONSR-OBMC-BSFC-0010-0001_1  Power Control Power Off and Power On
    Sub-Case  CONSR-OBMC-BSFC-0010-0001_2  Power Control Power Cycle
    Sub-Case  CONSR-OBMC-BSFC-0010-0001_3  Power Control Power Reset
    [Teardown]  Run Keyword If Test Failed  restore_system_power  ${DeviceName}

CONSR-OBMC-BSFC-0011-0001
    [Documentation]  This test checks the Function_008_Power Restore Policy
    [Tags]  CONSR-OBMC-BSFC-0011-0001  Artemis_U2  robot:skip  # TODO: issues
    [Timeout]  20 min 00 seconds
#    [Setup]
    ${openbmc_info} =  call_openbmc_class  ${DeviceName}
    ${ori_power_restore_policy} =  Call Method  ${openbmc_info}  check_openbmc_info  policy_status  get_status=True
    Sub-Case  CONSR-OBMC-BSFC-0011-0001_1  Power Restore Policy Power Off
    Sub-Case  CONSR-OBMC-BSFC-0011-0001_2  Power Restore Policy Power Previous
    Sub-Case  CONSR-OBMC-BSFC-0011-0001_2  Power Restore Policy Power On
    [Teardown]  Call Method  ${openbmc_info}  ipmi_power_control  ${ori_power_restore_policy}

CONSR-OBMC-BSFC-0012-0001
    [Documentation]  This test checks the Function_009_Sensor Summary Check
    [Tags]     CONSR-OBMC-BSFC-0012-0001  Artemis_U2
#    [Setup]
    Sub-Case  CONSR-OBMC-BSFC-0012-0001_1  Check System Status
    Sub-Case  CONSR-OBMC-BSFC-0012-0001_2  verify the sensor power off status
    Sub-Case  CONSR-OBMC-BSFC-0012-0001_3  verify the sensor power on status
    Sub-Case  CONSR-OBMC-BSFC-0012-0001_4  verify the sensor power reset status
    [Teardown]  Run Keyword If Test Failed  restore_system_power  ${DeviceName}

CONSR-OBMC-BSFC-0013-0001
    [Documentation]  This test checks the Function_013_Threshord Sensor
    [Tags]     CONSR-OBMC-BSFC-0013-0001  Artemis_U2
#    [Setup]
    Sub-Case  CONSR-OBMC-BSFC-0013-0001_1  Check Sensor Thresholds
    #[Teardown]

CONSR-OBMC-BSFC-0014-0001
    [Documentation]  This test checks Function_014_Discrete Sensor (TBD/NOT SUPPORT/MANUAL TEST)
    [Tags]     CONSR-OBMC-BSFC-0014-0001
    [Timeout]  30 min 00 seconds

CONSR-OBMC-BSFC-0015-0001
    [Documentation]  This test checks Function_012_SEL Summary Check
    [Tags]     CONSR-OBMC-BSFC-0015-0001  Artemis_U2  robot:skip  # TODO: AC serial console issues
    Sub-Case  CONSR-OBMC-BSFC-0015-0001_1  Check the Sel DC Cycle
    Sub-Case  CONSR-OBMC-BSFC-0015-0001_2  Check the Sel AC Cycle

CONSR-OBMC-BSFC-0016-0001
    [Documentation]  This test checks Function_016_SEL Management (TBD/NOT SUPPORT/MANUAL TEST)
    [Tags]     CONSR-OBMC-BSFC-0016-0001
    [Timeout]  30 min 00 seconds

CONSR-OBMC-BSFC-0017-0001
    [Documentation]  This test checks Function_017_SEL Time Check (TBD/NOT SUPPORT/MANUAL TEST)
    [Tags]     CONSR-OBMC-BSFC-0017-0001
    [Timeout]  30 min 00 seconds

CONSR-OBMC-BSFC-0018-0001
#TODO:
    [Documentation]  This test checks openBMC Inventory Management
    [Tags]     CONSR-OBMC-BSFC-0018-0001   Artemis
    [Timeout]  6 min 00 seconds
    Sub-Case  CONSR-OBMC-BSFC-0018-0001_1  Inventory Management

CONSR-OBMC-BSFC-0019-0001
    [Documentation]  This test verify watchDog test
    [Tags]     CONSR-OBMC-BSFC-0019-0001  CONSR-OBMC-BSFC-0020-0001  Artemis_U2
    [Timeout]  30 min 00 seconds
    #Sub-Case  CONSR-BMCT-BSFC-0020-0001_1  watchdog_timeout_action_set  ${DeviceName}
    Step  1  watchdog_timeout_action_set  ${DeviceName}

CONSR-OBMC-BSFC-0020-0001
    [Documentation]  This test checks Function_020_Watchdog Timeout Action Test (TBD/NOT SUPPORT/MANUAL TEST)
    [Tags]     CONSR-OBMC-BSFC-0020-0001
    [Timeout]  30 min 00 seconds

CONSR-OBMC-BSFC-0021-0001
    [Documentation]  This test checks Function_021_Watchdog Event Logging Test
    [Tags]     CONSR-OBMC-BSFC-0021-0001  Artemis_U2
    Sub-Case  CONSR-OBMC-BSFC-0021-0001_1  Watchdog Event Logging Test

#CONSR-OBMC-BSFC-0022-0001
#CONSR-OBMC-BSFC-0023-0001
#CONSR-OBMC-BSFC-0024-0001
#CONSR-OBMC-BSFC-0025-0001
#CONSR-OBMC-BSFC-0026-0001
#CONSR-OBMC-BSFC-0027-0001
#CONSR-OBMC-BSFC-0028-0001
#CONSR-OBMC-BSFC-0029-0001
#CONSR-OBMC-BSFC-0030-0001
#CONSR-OBMC-BSFC-0031-0001
#CONSR-OBMC-BSFC-0032-0001

CONSR-OBMC-BSFC-0033-0001
    [Documentation]  This test checks Function_033_Fan Status Monitor
    [Tags]     CONSR-OBMC-BSFC-0033-0001  Artemis_U2
    Sub-Case  CONSR-OBMC-BSFC-0033-0001_1  Check Fan Status Monitor
#    [Teardown]  Run Keyword If Test Failed  restore_system_power  ${DeviceName}

CONSR-OBMC-BSFC-0034-0001
    [Documentation]  This test checks Function_034_Fan Failure Protection (TBD/NOT SUPPORT/MANUAL TEST)
    [Tags]     CONSR-OBMC-BSFC-0034-0001

CONSR-OBMC-BSFC-0035-0001
    [Documentation]  This test checks Function_035_Multi-Node Management Feature set
    [Tags]     CONSR-OBMC-BSFC-0035-0001  Artemis_U2
    Sub-Case  CONSR-OBMC-BSFC-0035-0001_1  Check multi-node feature

CONSR-OBMC-NTWT-0001-0001-1
    [Documentation]  This test checks BMC LAN Configuration with port 1
    [Tags]     CONSR-OBMC-NTWT-0001-0001  CONSR-OBMC-NTWT-0001-0001-1  Artemis
    [Timeout]  30 min 00 seconds
    Sub-Case  CONSR-OBMC-NTWT-0001-0001_1  BMC LAN1 Configuration dhcp_1
#    Sub-Case  CONSR-OBMC-NTWT-0001-0001_2  run ipmi command "cold reset"
    Sub-Case  CONSR-OBMC-NTWT-0001-0001_3  BMC LAN1 Configuration dhcp_1
    Sub-Case  CONSR-OBMC-NTWT-0001-0001_4  Console Prompt_1
    Sub-Case  CONSR-OBMC-NTWT-0001-0001_5  Ping BMC Port1 dhcp loss
    Sub-Case  CONSR-OBMC-NTWT-0001-0001_6  Console Prompt_2
    Sub-Case  CONSR-OBMC-NTWT-0001-0001_7  Ping BMC Port1 dhcp
    Sub-Case  CONSR-BMCT-BSFC-0013-0001_8  Ip setting port1_static
    Sub-Case  CONSR-OBMC-NTWT-0001-0001_9  BMC LAN1 Configuration static
    Sub-Case  CONSR-BMCT-BSFC-0013-0001_10  Ip setting port1_dhcp
    Sub-Case  CONSR-OBMC-NTWT-0001-0001_11  BMC LAN1 Configuration dhcp_2

CONSR-OBMC-NTWT-0001-0001-2
    [Documentation]  This test checks BMC LAN Configuration with port 2
    [Tags]     CONSR-OBMC-NTWT-0001-0001  CONSR-OBMC-NTWT-0001-0001-2  Artemis
    [Timeout]  30 min 00 seconds
    Sub-Case  CONSR-OBMC-NTWT-0001-0001_1  BMC LAN2 Configuration dhcp_1
#    Sub-Case  CONSR-OBMC-NTWT-0001-0001_2  run ipmi command "cold reset"
    Sub-Case  CONSR-OBMC-NTWT-0001-0001_3  BMC LAN2 Configuration dhcp_1
    Sub-Case  CONSR-OBMC-NTWT-0001-0001_4  Console Prompt_3
    Sub-Case  CONSR-OBMC-NTWT-0001-0001_5  Ping BMC Port2 dhcp loss
    Sub-Case  CONSR-OBMC-NTWT-0001-0001_6  Console Prompt_4
    Sub-Case  CONSR-OBMC-NTWT-0001-0001_7  Ping BMC Port2 dhcp
    Sub-Case  CONSR-OBMC-NTWT-0001-0001_8  Ip setting port2_static
    Sub-Case  CONSR-OBMC-NTWT-0001-0001_9  BMC LAN2 Configuration static
    Sub-Case  CONSR-OBMC-NTWT-0001-0001_10  Ip setting port2_dhcp
    Sub-Case  CONSR-OBMC-NTWT-0001-0001_11  BMC LAN2 Configuration dhcp_2

CONSR-OBMC-NTWT-0002-0001-1
    [Documentation]  This test checks BMC LAN Communication with port1
    [Tags]     CONSR-OBMC-NTWT-0002-0001  CONSR-OBMC-NTWT-0002-0001-1  Artemis
    [Timeout]  30 min 00 seconds
    Sub-Case  CONSR-OBMC-NTWT-0002-0001-1_1  BMC LAN1 Configuration dhcp_2
    Sub-Case  CONSR-OBMC-NTWT-0002-0001-1_2  Ping BMC Port1 dhcp
    Sub-Case  CONSR-OBMC-NTWT-0002-0001-1_3  run ipmi command "61"
    Sub-Case  CONSR-OBMC-NTWT-0002-0001-1_4  Console Prompt_1
    Sub-Case  CONSR-OBMC-NTWT-0002-0001-1_5  Ping BMC Port1 dhcp loss
    Sub-Case  CONSR-OBMC-NTWT-0002-0001-1_6  Console Prompt_2
    Sub-Case  CONSR-OBMC-NTWT-0002-0001-1_7  Ping BMC Port1 dhcp
    Sub-Case  CONSR-OBMC-NTWT-0002-0001-1_8  Ip setting port1_static
    Sub-Case  CONSR-OBMC-NTWT-0002-0001-1_9  BMC LAN1 Configuration static
    Sub-Case  CONSR-OBMC-NTWT-0002-0001-1_10  Ping BMC Port1 static
    Sub-Case  CONSR-OBMC-NTWT-0002-0001-1_11  Console Prompt_1
    Sub-Case  CONSR-OBMC-NTWT-0002-0001-1_12  Ping BMC Port1 static loss
    Sub-Case  CONSR-OBMC-NTWT-0002-0001-1_13  Console Prompt_2
    Sub-Case  CONSR-OBMC-NTWT-0002-0001-1_14  Ping BMC Port1 static
    Sub-Case  CONSR-OBMC-NTWT-0002-0001-1_15  Ip setting port1_dhcp
    Sub-Case  CONSR-OBMC-NTWT-0001-0001-1_16  BMC LAN1 Configuration dhcp_2

CONSR-OBMC-NTWT-0002-0001-2
    [Documentation]  This test checks BMC LAN Communication with port2
    [Tags]     CONSR-OBMC-NTWT-0002-0001  CONSR-OBMC-NTWT-0002-0001-2  Artemis
    [Timeout]  30 min 00 seconds
    Sub-Case  CONSR-OBMC-NTWT-0002-0001-1_1  BMC LAN2 Configuration dhcp_2
    Sub-Case  CONSR-OBMC-NTWT-0002-0001-1_2  Ping BMC Port2 dhcp
    Sub-Case  CONSR-OBMC-NTWT-0002-0001-1_3  run ipmi command "61"
    Sub-Case  CONSR-OBMC-NTWT-0002-0001-1_4  Console Prompt_3
    Sub-Case  CONSR-OBMC-NTWT-0002-0001-1_5  Ping BMC Port2 dhcp loss
    Sub-Case  CONSR-OBMC-NTWT-0002-0001-1_6  Console Prompt_4
    Sub-Case  CONSR-OBMC-NTWT-0002-0001-1_7  Ping BMC Port2 dhcp
    Sub-Case  CONSR-OBMC-NTWT-0002-0001-1_8  Ip setting port2_static
    Sub-Case  CONSR-OBMC-NTWT-0002-0001-1_9  BMC LAN2 Configuration static
    Sub-Case  CONSR-OBMC-NTWT-0002-0001-1_10  Ping BMC Port2 static
    Sub-Case  CONSR-OBMC-NTWT-0002-0001-1_11  Console Prompt_3
    Sub-Case  CONSR-OBMC-NTWT-0002-0001-1_12  Ping BMC Port2 static loss
    Sub-Case  CONSR-OBMC-NTWT-0002-0001-1_13  Console Prompt_4
    Sub-Case  CONSR-OBMC-NTWT-0002-0001-1_14  Ping BMC Port2 static
    Sub-Case  CONSR-OBMC-NTWT-0002-0001-1_15  Ip setting port2_dhcp
    Sub-Case  CONSR-OBMC-NTWT-0002-0001-1_16  BMC LAN2 Configuration dhcp_2

CONSR-OBMC-NTWT-0003-0001
    [Documentation]  This test for "IP setting test"
    [Tags]     CONSR-OBMC-NTWT-0003-0001  Artemis
    [Timeout]  30 min 00 seconds
    Sub-Case  CONSR-BMCT-BSFC-0013-0001_1  IP Setting Test

CONSR-OBMC-NTWT-0004-0001
    [Documentation]  This test checks ip6 test
    [Tags]     CONSR-OBMC-NTWT-0004-0001  Artemis
    [Timeout]  30 min 00 seconds
    Sub-Case  CONSR-OBMC-NTWT-0004-0001_1  check ip6 test

CONSR-OBMC-NTWT-0006-0001
    [Documentation]  This test checks BMC dedicate and share port ping stress 12 hours
    [Tags]     CONSR-OBMC-NTWT-0006-0001  Artemis
    [Timeout]  720 min 00 seconds
    Sub-Case  CONSR-OBMC-NTWT-0006-0001_1  Check BMC dedicate and share port ping stress

CONSR-OBMC-NTWT-0007-0001
    [Documentation]  This test checks Network_007_Invalid BMC API Call Test
    [Tags]     CONSR-OBMC-NTWT-0007-0001  Artemis
    [Timeout]  20 min 00 seconds
    Sub-Case  CONSR-OBMC-NTWT-0007-0001_1  Check BMC API Call Test

CONSR-OBMC-NTWT-0008-0001
    [Documentation]  This test checks Access BMC By USB_Ethernet
    [Tags]     CONSR-OBMC-NTWT-0008-0001  Artemis
    [Timeout]  30 min 00 seconds
    Sub-Case  CONSR-OBMC-NTWT-0008-0001_1  check Access BMC By USB_Ethernet

CONSR-OBMC-BHSI-0003-0001
    [Documentation]  This test To verify if openBMC can control the boot options correctly
    [Tags]     CONSR-OBMC-BHSI-0003-0001  Artemis
    [Timeout]  60 min 00 seconds
    Sub-Case  CONSR-OBMC-BHSI-0003-0001_1  set the boot flags to be persistent

CONSR-OBMC-BHSI-0003-0002
    [Documentation]  This test To verify if openBMC can control the boot options correctly
    [Tags]     CONSR-OBMC-BHSI-0003-0002  Artemis
    [Timeout]  60 min 00 seconds
    Sub-Case  CONSR-OBMC-BHSI-0003-0001_2  set the boot flags apply to next boot

CONSR-OBMC-BHSI-0003-0003
    [Documentation]  This test To verify if openBMC can control the boot options correctly
    [Tags]     CONSR-OBMC-BHSI-0003-0003  Artemis
    [Timeout]  60 min 00 seconds
    Sub-Case  CONSR-OBMC-BHSI-0003-0001_3  set the chassis bootdev bios clear

CONSR-OBMC-BHSI-0005-0001
    [Documentation]  This test To verify Interaction_005_Server Mgmt
    [Tags]     CONSR-OBMC-BHSI-0005-0001  Artemis
    [Timeout]  30 min 00 seconds
    Sub-Case  CONSR-OBMC-BHSI-0005-0001_1  Interaction server mgmt


CONSR-OBMC-FWUP-0002-0001
    [Documentation]   This test checks openbmc online Firmware Update
    [Tags]   CONSR-OBMC-FWUP-0002-0001  Artemis_U2
    Sub-Case  CONSR-OBMC-FWUP-0002-0001_1  BMC Online Update
    #Sub-Case  CONSR-OBMC-FWUP-0002-0001_2  BMC Online Update Backup
    [Teardown]

CONSR-OBMC-FWUP-0003-0001
    [Documentation]   This test checks bios online Firmware Update
    [Tags]   CONSR-OBMC-FWUP-0003-0001  Artemis_U2
    Sub-Case  CONSR-OBMC-FWUP-0003-0001_1  BIOS Online Update
    #Sub-Case  CONSR-OBMC-FWUP-0003-0001_2  BIOS Online Update Backup
    [Teardown]

CONSR-OBMC-FWUP-0004-0001
    [Documentation]   This test checks CPLD online Firmware Update
    [Tags]   CONSR-OBMC-FWUP-0004-0001  Artemis_U2
    Sub-Case  CONSR-OBMC-FWUP-0004-0001_1  CPLD Update
    [Teardown]

CONSR-OBMC-FWUP-0005-0001
    [Documentation]   This test checks PSU Firmware Update
    [Tags]   CONSR-OBMC-FWUP-0005-0001  Artemis
    Sub-Case  CONSR-OBMC-FWUP-0005-0001_1  PSU FW Update
    [Teardown]

CONSR-OBMC-SRTS-0001-0001
    [Documentation]  This test checks Stress_002_BMC FW Update Stress Test
    [Tags]  CONSR-OBMC-SRTS-0001-0001   Artemis_stress
    [Timeout]  24 hours
    Sub-Case  CONSR-OBMC-SRTS-0001-0001_1  BMC Online Update Stress

CONSR-OBMC-SRTS-0002-0001
    [Documentation]  This test checks Stress_003_BIOS FW Update Stress Test
    [Tags]  CONSR-OBMC-SRTS-0002-0001   Artemis_stress
    [Timeout]  24 hours
    Sub-Case  CONSR-OBMC-SRTS-0002-0001_1  BIOS Online Update Stress

CONSR-OBMC-SRTS-0003-0001
    [Documentation]  This test checks Stress Test - BMC FRU Read Stress Test
    [Tags]   CONSR-OBMC-SRTS-0003-0001  Artemis_stress
    [Timeout]  20 min 00 seconds
    Step  1  run ipmi command "Clear SEL"
    Step  2  Verify fru_vpd before
    FOR   ${INDEX}   IN RANGE   ${FRUREAD_CYCLES}
        Log     This is the ${INDEX} Loop
        Step  1  Verify fru_vpd after
        Sleep  5
        Step  2  Verify the SEL and ensure no error
    END

CONSR-OBMC-SRTS-0004-0001
    [Documentation]  This is Stress_004_BMC Sensor Read Stress Test
    [Tags]  CONSR-OBMC-SRTS-0004-0001   Artemis_U2_stress
    [Timeout]  24 hours
    Sub-Case  CONSR-OBMC-SRTS-0004-0001_1  Sensor Read Stress Test

CONSR-OBMC-SRTS-0005-0001
    [Documentation]  This is Stress_005_BMC Reset(Self) Stress Test
    [Tags]  CONSR-OBMC-SRTS-0005-0001   Artemis_stress
    [Timeout]  24 hours
    Step  1  run ipmi command "Clear SEL"
    Step  2  Verify fru_vpd_mcinfo before
    FOR  ${INDEX}  IN RANGE  ${Power_Reset_SELF_CYCLES}
        Log     This is the ${INDEX} Loop
        Step  1  run ipmi command "cold reset"
        Step  2  Verify fru_vpd_mcinfo after
        Step  3  run ipmi command "Get LAN Configuration Parameters"
        Step  4  Verify the Sensor and ensure no error
        Step  5  Verify the SEL and ensure no error
    END

CONSR-OBMC-SRTS-0006-0001
    [Documentation]  This is Stress_006_IPMI power reset stress test
    [Tags]  CONSR-OBMC-SRTS-0006-0001   Artemis_stress
    [Timeout]  24 hours
    Step  1  run ipmi command "Clear SEL"
    Step  2  Verify fru_vpd_mcinfo before
    FOR  ${INDEX}  IN RANGE  ${Power_Reset_CYCLES}
        Log     This is the ${INDEX} Loop
        Step  1  Run power control "power reset"
        Step  2  Verify fru_vpd_mcinfo after
        Step  3  Verify the Sensor and ensure no error
        Step  4  Verify the SEL and ensure no error
    END

CONSR-OBMC-SRTS-0007-0001
    [Documentation]  This is Stress_007_IPMI power cycle stress test
    [Tags]  CONSR-OBMC-SRTS-0007-0001  Artemis_stress
    [Timeout]  24 hours
    Step  1  run ipmi command "Clear SEL"
    Step  2  Verify fru_vpd_mcinfo before
    FOR  ${INDEX}  IN RANGE  ${Power_CYCLE_CYCLES}
        Log     This is the ${INDEX} Loop
        Step  1  Run power control "power cycle"
        Sleep  180
        Step  2  Verify fru_vpd_mcinfo after
        Step  3  Verify the Sensor and ensure no error
        Step  4  Verify the SEL and ensure no error
    END

CONSR-BMC-IPMI-0001-0001
    [Documentation]  This test checks IPMI command: Get Device ID
    [Tags]     CONSR-OBMC-BSFC-0022-0001  CONSR-BMC-IPMI-0001-0001  Artemis_U2
    [Timeout]  15 min 00 seconds
    Sub-Case  CONSR-BMC-IPMI-0001-0001_1  run ipmi command "Get Device ID"

CONSR-BMC-IPMI-0002-0001
    [Documentation]  This test checks IPMI command: "cold reset"
    [Tags]     CONSR-OBMC-BSFC-0022-0001  CONSR-BMC-IPMI-0002-0001  Artemis_U2
    [Timeout]  15 min 00 seconds
    Sub-Case  CONSR-BMC-IPMI-0002-0001_1  run ipmi command "cold reset"

#CONSR-BMC-IPMI-0003-0001
#    [Documentation]  This test checks IPMI command: "warm reset"
#    [Tags]     CONSR-BMC-IPMI-0003-0001  Artemis
#    [Timeout]  1 min 00 seconds
#    Sub-Case  CONSR-BMC-IPMI-0003-0001_1  run ipmi command "warm reset"

CONSR-BMC-IPMI-0004-0001
    [Documentation]  This test checks IPMI command: "Get Self Test Results"
    [Tags]     CONSR-OBMC-BSFC-0022-0001  CONSR-BMC-IPMI-0004-0001  Artemis_U2
    [Timeout]  5 min 00 seconds
    Sub-Case  CONSR-BMC-IPMI-0004-0001_1  run ipmi command "Get Self Test Results"

CONSR-BMC-IPMI-0005-0001
    [Documentation]  This test checks IPMI command: "Set ACPI Power State"
    [Tags]     CONSR-OBMC-BSFC-0022-0001  CONSR-BMC-IPMI-0005-0001  Artemis_U2
    [Timeout]  5 min 00 seconds
    Sub-Case  CONSR-BMC-IPMI-0005-0001_1  run ipmi command "Set ACPI Power State"
    #[Teardown]  Set ACPI Power State back to default

#CONSR-BMC-IPMI-0006-0001
#    [Documentation]  This test checks IPMI command: "Get ACPI Power State"
#    [Tags]     CONSR-OBMC-BSFC-0022-0001  CONSR-BMC-IPMI-0006-0001  Artemis
#    [Timeout]  5 min 00 seconds
#    Sub-Case  CONSR-BMC-IPMI-0006-0001_1  run ipmi command "Get ACPI Power State"

CONSR-BMC-IPMI-0007-0001
    [Documentation]  This test checks IPMI command: "Reset Watchdog Timer"
    [Tags]     CONSR-BMC-IPMI-0007-0001  Artemis_U2
    [Timeout]  5 min 00 seconds
    Sub-Case  CONSR-BMC-IPMI-0007-0001_1  run ipmi command "Reset Watchdog Timer"

CONSR-BMC-IPMI-0008-0001
    [Documentation]  This test checks IPMI command: "Set Watchdog Timer"
    [Tags]     CONSR-BMC-IPMI-0008-0001  Artemis_U2
    [Timeout]  5 min 00 seconds
    Sub-Case  CONSR-BMC-IPMI-0008-0001_1  run ipmi command "Set Watchdog Timer"

CONSR-BMC-IPMI-0009-0001
    [Documentation]  This test checks IPMI command: "Get Watchdog Timer"
    [Tags]     CONSR-BMC-IPMI-0009-0001  Artemis_U2
    [Timeout]  5 min 00 seconds
    Sub-Case  CONSR-BMC-IPMI-0009-0001_1  run ipmi command "Get Watchdog Timer"

#TODO: Not support: Command not supported in present state
#CONSR-BMC-IPMI-0010-0001
#    [Documentation]  This test checks IPMI command: "Set BMC Global enables"
#    [Tags]     CONSR-OBMC-BSFC-0024-0001  CONSR-BMC-IPMI-0010-0001  Artemis
#    [Timeout]  5 min 00 seconds
#    Sub-Case  CONSR-BMC-IPMI-0010-0001_1  run ipmi command "Set BMC Global enables"

CONSR-BMC-IPMI-0011-0001
    [Documentation]  This test checks IPMI command: "Get BMC Global enables"
    [Tags]     CONSR-OBMC-BSFC-0024-0001  CONSR-BMC-IPMI-0011-0001  Artemis_U2
    [Timeout]  5 min 00 seconds
    Sub-Case  CONSR-BMC-IPMI-0011-0001_1  run ipmi command "Get BMC Global enables"

#TODO: NOT SUPPORT
#CONSR-BMC-IPMI-0012-0001
#    [Documentation]  This test checks IPMI command: "Clear Message Flags"
#    [Tags]     CONSR-OBMC-BSFC-0024-0001  CONSR-BMC-IPMI-0012-0001  Artemis
#    [Timeout]  5 min 00 seconds
#    Sub-Case  CONSR-BMC-IPMI-0012-0001_1  run ipmi command "Clear Message Flags"

CONSR-BMC-IPMI-0013-0001
    [Documentation]  This test checks IPMI command: "Get Message Flags"
    [Tags]     CONSR-OBMC-BSFC-0024-0001  CONSR-BMC-IPMI-0013-0001  Artemis_U2
    [Timeout]  5 min 00 seconds
    Sub-Case  CONSR-BMC-IPMI-0013-0001_1  run ipmi command "Get Message Flags"

#TODO: NOT SUPPORT
#CONSR-BMC-IPMI-0014-0001
#    [Documentation]  This test checks IPMI command: "Enable Message Channel Receive"
#    [Tags]     CONSR-OBMC-BSFC-0024-0001  CONSR-BMC-IPMI-0014-0001  Artemis
#    [Timeout]  5 min 00 seconds
#    Sub-Case  CONSR-BMC-IPMI-0014-0001_1  run ipmi command "Enable Message Channel Receive"

CONSR-BMC-IPMI-0015-0001
    [Documentation]  This test checks IPMI command: "Get System GUID"
    [Tags]     CONSR-OBMC-BSFC-0024-0001  CONSR-BMC-IPMI-0 015-0001  Artemis_U2
    [Timeout]  5 min 00 seconds
    Sub-Case  CONSR-BMC-IPMI-0015-0001_1  run ipmi command "Get System GUID"

CONSR-BMC-IPMI-0016-0001
    [Documentation]  This test checks IPMI command: "Get Channel Authentication capabilities"
    [Tags]     CONSR-OBMC-BSFC-0024-0001  CONSR-BMC-IPMI-0016-0001  Artemis_U2
    [Timeout]  5 min 00 seconds
    Sub-Case  CONSR-BMC-IPMI-0016-0001_1  run ipmi command "Get Channel Authentication capabilities"

#CONSR-BMC-IPMI-0017-0001
#    [Documentation]  This test checks IPMI command: "Get Session Challenge"
#    [Tags]     CONSR-OBMC-BSFC-0024-0001  CONSR-BMC-IPMI-0017-0001  Artemis
#    [Timeout]  5 min 00 seconds
#    Sub-Case  CONSR-BMC-IPMI-0017-0001_1  run ipmi command "Get Session Challenge" by remote ipmitool

CONSR-BMC-IPMI-0018-0001
    [Documentation]  This test checks IPMI command: "Set Session Privilege Level"
    [Tags]     CONSR-OBMC-BSFC-0024-0001  CONSR-BMC-IPMI-0018-0001  Artemis_U2
    [Timeout]  5 min 00 seconds
    Sub-Case  CONSR-BMC-IPMI-0018-0001_1  run ipmi command "Set Session Privilege Level" by remote ipmitool

CONSR-BMC-IPMI-0019-0001
    [Documentation]  This test checks IPMI command: "Get Session Info"
    [Tags]     CONSR-OBMC-BSFC-0024-0001  CONSR-BMC-IPMI-0019-0001  Artemis_U2
    [Timeout]  5 min 00 seconds
    Sub-Case  CONSR-BMC-IPMI-0019-0001_1  run ipmi command "Get Session Info"

##not support
#CONSR-BMC-IPMI-0020-0001
#    [Documentation]  This test checks IPMI command: "Get AuthCode"
#    [Tags]     CONSR-OBMC-BSFC-0024-0001  CONSR-BMC-IPMI-0020-0001  Artemis  robot:skip
#    [Timeout]  20 min 00 seconds
#    Sub-Case  CONSR-BMC-IPMI-0020-0001_1  run ipmi command "Get AuthCode"

CONSR-BMC-IPMI-0021-0001
    [Documentation]  This test checks IPMI command: "Set Channel Access"
    [Tags]     CONSR-OBMC-BSFC-0024-0001  CONSR-BMC-IPMI-0021-0001  Artemis_U2
    [Timeout]  5 min 00 seconds
    Sub-Case  CONSR-BMC-IPMI-0021-0001_1  run ipmi command "Set Channel Access"

CONSR-BMC-IPMI-0022-0001
    [Documentation]  This test checks IPMI command: "Get Channel Access"
    [Tags]     CONSR-OBMC-BSFC-0024-0001  CONSR-BMC-IPMI-0022-0001  Artemis_U2
    [Timeout]  5 min 00 seconds
    Sub-Case  CONSR-BMC-IPMI-0022-0001_1  run ipmi command "Get Channel Access"

CONSR-BMC-IPMI-0023-0001
    [Documentation]  This test checks IPMI command: "Get Channel Info"
    [Tags]     CONSR-OBMC-BSFC-0024-0001  CONSR-BMC-IPMI-0023-0001  Artemis_U2
    [Timeout]  5 min 00 seconds
    Sub-Case  CONSR-BMC-IPMI-0023-0001_1  run ipmi command "Get Channel Info"

CONSR-BMC-IPMI-0024-0001
    [Documentation]  This test checks IPMI command: "Set User Access"
    [Tags]     CONSR-OBMC-BSFC-0024-0001  CONSR-BMC-IPMI-0024-0001  Artemis_U2
    [Timeout]  5 min 00 seconds
    Sub-Case  CONSR-BMC-IPMI-0024-0001_1  run ipmi command "Set User Access"

CONSR-BMC-IPMI-0025-0001
    [Documentation]  This test checks IPMI command: "Get User Access"
    [Tags]     CONSR-OBMC-BSFC-0024-0001  CONSR-BMC-IPMI-0025-0001  Artemis_U2
    [Timeout]  5 min 00 seconds
    Sub-Case  CONSR-BMC-IPMI-0025-0001_1  run ipmi command "Get User Access"

CONSR-BMC-IPMI-0026-0001
    [Documentation]  This test checks IPMI command: "Set User name"
    [Tags]     CONSR-OBMC-BSFC-0024-0001  CONSR-BMC-IPMI-0026-0001  Artemis_U2
    [Timeout]  5 min 00 seconds
    Sub-Case  CONSR-BMC-IPMI-0026-0001_1  run ipmi command "Set User name"

CONSR-BMC-IPMI-0027-0001
    [Documentation]  This test checks IPMI command: "Get User name"
    [Tags]     CONSR-OBMC-BSFC-0024-0001  CONSR-BMC-IPMI-0027-0001  Artemis_U2
    [Timeout]  5 min 00 seconds
    Sub-Case  CONSR-BMC-IPMI-0027-0001_1  run ipmi command "Get User name"

CONSR-BMC-IPMI-0028-0001
    [Documentation]  This test checks IPMI command: "Set User Password"
    [Tags]     CONSR-OBMC-BSFC-0024-0001  CONSR-BMC-IPMI-0028-0001  Artemis_U2
    [Timeout]  5 min 00 seconds
    Sub-Case  CONSR-BMC-IPMI-0028-0001_1  run ipmi command "Set User Password"

CONSR-BMC-IPMI-0029-0001
    [Documentation]  This test checks IPMI command: "Get Payload Activation Status"
    [Tags]     CONSR-OBMC-BSFC-0024-0001  CONSR-BMC-IPMI-0029-0001  Artemis_U2
    [Timeout]  5 min 00 seconds
    Sub-Case  CONSR-BMC-IPMI-0029-0001_1  run ipmi command "Get Payload Activation Status"

CONSR-BMC-IPMI-0030-0001
    [Documentation]  This test checks IPMI command: "Get Payload Instance Info"
    [Tags]     CONSR-OBMC-BSFC-0024-0001  CONSR-BMC-IPMI-0030-0001  Artemis_U2
    [Timeout]  5 min 00 seconds
    Sub-Case  CONSR-BMC-IPMI-0030-0001_1  run ipmi command "Get Payload Instance Info"

CONSR-BMC-IPMI-0031-0001
    [Documentation]  This test checks IPMI command: "Set user Payload Access"
    [Tags]     CONSR-OBMC-BSFC-0024-0001  CONSR-BMC-IPMI-0031-0001  Artemis_U2
    [Timeout]  5 min 00 seconds
    Sub-Case  CONSR-BMC-IPMI-0031-0001_1  run ipmi command "Set user Payload Access"

CONSR-BMC-IPMI-0032-0001
    [Documentation]  This test checks IPMI command: "Get user Payload Access"
    [Tags]     CONSR-OBMC-BSFC-0024-0001  CONSR-BMC-IPMI-0032-0001  Artemis_U2
    [Timeout]  5 min 00 seconds
    Sub-Case  CONSR-BMC-IPMI-0032-0001_1  run ipmi command "Get user Payload Access"

CONSR-BMC-IPMI-0033-0001
    [Documentation]  This test checks IPMI command: "Get channel Payload support"
    [Tags]     CONSR-OBMC-BSFC-0024-0001  CONSR-BMC-IPMI-0033-0001  Artemis_U2
    [Timeout]  5 min 00 seconds
    Sub-Case  CONSR-BMC-IPMI-0033-0001_1  run ipmi command "Get channel Payload support"

CONSR-BMC-IPMI-0034-0001
    [Documentation]  This test checks IPMI command: "Get channel Payload Version"
    [Tags]     CONSR-OBMC-BSFC-0024-0001  CONSR-BMC-IPMI-0034-0001  Artemis_U2
    [Timeout]  5 min 00 seconds
    Sub-Case  CONSR-BMC-IPMI-0034-0001_1  run ipmi command "Get channel Payload Version"

CONSR-BMC-IPMI-0035-0001
    [Documentation]  This test checks IPMI command: "Get Channel Cipher"
    [Tags]     CONSR-OBMC-BSFC-0024-0001  CONSR-BMC-IPMI-0035-0001  Artemis_U2
    [Timeout]  5 min 00 seconds
    Sub-Case  CONSR-BMC-IPMI-0035-0001_1  run ipmi command "Get Channel Cipher Suites"

CONSR-BMC-IPMI-0036-0001
    [Documentation]  This test checks IPMI command: "Master Write-Read"
    [Tags]     CONSR-OBMC-BSFC-0024-0001  CONSR-BMC-IPMI-0036-0001  Artemis_U2
    [Timeout]  5 min 00 seconds
    Sub-Case  CONSR-BMC-IPMI-0036-0001_1  run ipmi command "Master Write-Read"

#CONSR-BMC-IPMI-0037-0001
#    [Documentation]  This test checks IPMI command: "Set Channel Security Keys 56h"
#    [Tags]     CONSR-OBMC-BSFC-0024-0001  CONSR-BMC-IPMI-0037-0001  Artemis
#    [Timeout]  5 min 00 seconds
#    Sub-Case  CONSR-BMC-IPMI-0037-0001_1  run ipmi command "Set Channel Security Keys 56h"

#CONSR-BMC-IPMI-0038-0001
#    [Documentation]  This test checks IPMI command: "Get Chassis Capabilities"
#    [Tags]     CONSR-OBMC-BSFC-0025-0001  CONSR-BMC-IPMI-0038-0001  Artemis  robot:skip
#    [Timeout]  5 min 00 seconds
#    Sub-Case  CONSR-BMC-IPMI-0038-0001_1  run ipmi command "Get Chassis Capabilities"

CONSR-BMC-IPMI-0039-0001
    [Documentation]  This test checks IPMI command: "Get Chassis Status"
    [Tags]     CONSR-OBMC-BSFC-0025-0001  CONSR-BMC-IPMI-0039-0001  Artemis_U2
    [Timeout]  5 min 00 seconds
    Sub-Case  CONSR-BMC-IPMI-0039-0001_1  run ipmi command "Get Chassis Status"

#TODO:
#CONSR-BMC-IPMI-0040-0001
#    [Documentation]  This test checks IPMI command: "Chassis power control"
#    [Tags]     CONSR-OBMC-BSFC-0025-0001  CONSR-BMC-IPMI-0040-0001  Artemis
#    [Timeout]  60 min 00 seconds
#    Sub-Case  CONSR-BMC-IPMI-0040-0001_1  run ipmi command "Chassis power down"
#    Sub-Case  CONSR-BMC-IPMI-0040-0001_2  run ipmi command "Chassis power up"
#    Sub-Case  CONSR-BMC-IPMI-0040-0001_3  run ipmi command "Chassis soft shutdown"
#    Sub-Case  CONSR-BMC-IPMI-0040-0001_4  run ipmi command "Chassis power up"
#    Sub-Case  CONSR-BMC-IPMI-0040-0001_5  run ipmi command "Chassis power cycle"

#CONSR-BMC-IPMI-0041-0001
#    [Documentation]  This test checks IPMI command: "Chassis Identify"
#    [Tags]     CONSR-OBMC-BSFC-0025-0001  CONSR-BMC-IPMI-0041-0001  Artemis
#    [Timeout]  60 min 00 seconds
#    Sub-Case  CONSR-BMC-IPMI-0041-0001_1  run ipmi command "Chassis Identify"

#TODO:
#CONSR-BMC-IPMI-0042-0001
#    [Documentation]  This test checks IPMI command: "Set Power Restore Policy"
#    [Tags]     CONSR-OBMC-BSFC-0025-0001  CONSR-BMC-IPMI-0042-0001  Artemis
#    [Timeout]  60 min 00 seconds
#    Sub-Case  CONSR-BMC-IPMI-0042-0001_1  run ipmi command "Always stay power off"
#    Sub-Case  CONSR-BMC-IPMI-0042-0001_2  run ipmi command "Restore prior state"
#    Sub-Case  CONSR-BMC-IPMI-0042-0001_3  run ipmi command "Always stay power up"
#    Sub-Case  CONSR-BMC-IPMI-0042-0001_4  run ipmi command "No change"

CONSR-BMC-IPMI-0043-0001
    [Documentation]  This test checks IPMI command: "Get System Restart Cause"
    [Tags]     CONSR-OBMC-BSFC-0025-0001  CONSR-BMC-IPMI-0043-0001  Artemis_U2
    [Timeout]  30 min 00 seconds
    #[Setup]  get all the variables
    Sub-Case  CONSR-BMC-IPMI-0043-0001_1  run ipmi command "Get System Restart Cause"

CONSR-BMC-IPMI-0044-0001
    [Documentation]  This test checks IPMI command: "Set System Boot Options"
    [Tags]     CONSR-OBMC-BSFC-0025-0001  CONSR-BMC-IPMI-0044-0001  Artemis_U2
    [Timeout]  30 min 00 seconds
    Sub-Case  CONSR-BMC-IPMI-0044-0001_1  run ipmi command "Set System Boot Options"

CONSR-BMC-IPMI-0045-0001
    [Documentation]  This test checks IPMI command: "Get System Boot Options"
    [Tags]     CONSR-OBMC-BSFC-0025-0001  CONSR-BMC-IPMI-0045-0001  Artemis_U2
    [Timeout]  30 min 00 seconds
    Sub-Case  CONSR-BMC-IPMI-0045-0001_1  run ipmi command "Get System Boot Options"

#CONSR-BMC-IPMI-0046-0001
#    [Documentation]  This test checks IPMI command: "Set Front Panel Button Enables"
#    [Tags]     CONSR-OBMC-BSFC-0025-0001  CONSR-BMC-IPMI-0046-0001  Artemis  robot:skip
#    [Timeout]  30 min 00 seconds
#    Sub-Case  CONSR-BMC-IPMI-0046-0001_1  run ipmi command "Set Front Panel Button Enables"
#
#CONSR-BMC-IPMI-0047-0001
#    [Documentation]  This test checks IPMI command: "Set Power Cycle Interval"
#    [Tags]     CONSR-OBMC-BSFC-0025-0001  CONSR-BMC-IPMI-0047-0001  Artemis  robot:skip
#    [Timeout]  30 min 00 seconds
#    Sub-Case  CONSR-BMC-IPMI-0047-0001_1  run ipmi command "Set Power Cycle Interval"
#
#CONSR-BMC-IPMI-0048-0001
#    [Documentation]  This test checks IPMI command: "Get POH Counter"
#    [Tags]     CONSR-OBMC-BSFC-0025-0001  CONSR-BMC-IPMI-0048-0001  Artemis  robot:skip
#    [Timeout]  30 min 00 seconds
#    Sub-Case  CONSR-BMC-IPMI-0048-0001_1  run ipmi command "Get POH Counter"
#
#CONSR-BMC-IPMI-0049-0001
#    [Documentation]  This test checks IPMI command: "Set Event Receiver"
#    [Tags]     CONSR-OBMC-BSFC-0026-0001  CONSR-BMC-IPMI-0049-0001  Artemis  robot:skip
#    [Timeout]  5 min 00 seconds
#    Sub-Case  CONSR-BMC-IPMI-0049-0001_1  run ipmi command "Set Event Receiver"

#CONSR-BMC-IPMI-0050-0001
#    [Documentation]  This test checks IPMI command: "Get Event Receiver"
#    [Tags]     CONSR-OBMC-BSFC-0026-0001  CONSR-BMC-IPMI-0050-0001  Artemis  robot:skip
#    [Timeout]  5 min 00 seconds
#    Sub-Case  CONSR-BMC-IPMI-0050-0001_1  run ipmi command "Get Event Receiver"

CONSR-BMC-IPMI-0051-0001
    [Documentation]  This test checks IPMI command: "Platform Event Message"
    [Tags]     CONSR-OBMC-BSFC-0026-0001  CONSR-BMC-IPMI-0051-0001  Artemis_U2
    [Timeout]  5 min 00 seconds
    Sub-Case  CONSR-BMC-IPMI-0051-0001_1  run ipmi command "Platform Event Message"

# PEF and Alerting Commands CONSR-OBMC-BSFC-0027-000 "not support "
#CONSR-BMC-IPMI-0052-0001
#    [Documentation]  This test checks IPMI command: "Get PEF Capabilities"
#    [Tags]     CONSR-OBMC-BSFC-0027-0001  CONSR-BMC-IPMI-0052-0001  Artemis  robot:skip
#    [Timeout]  5 min 00 seconds
#    Sub-Case  CONSR-BMC-IPMI-0052-0001_1  run ipmi command "Get PEF Capabilities"
#
#CONSR-BMC-IPMI-0053-0001
#    [Documentation]  This test checks IPMI command: "Arm PEF Postpone Timer"
#    [Tags]     CONSR-OBMC-BSFC-0027-0001  CONSR-BMC-IPMI-0053-0001  Artemis  robot:skip
#    [Timeout]  5 min 00 seconds
#    Sub-Case  CONSR-BMC-IPMI-0053-0001_1  run ipmi command "Disable postpone timer"
#    Sub-Case  CONSR-BMC-IPMI-0053-0001_2  run ipmi command "arm timer"
#    Sub-Case  CONSR-BMC-IPMI-0053-0001_3  run ipmi command "get present countdown value"
#
#CONSR-BMC-IPMI-0054-0001
#    [Documentation]  This test checks IPMI command: "Set PEF Configuration Parameters"
#    [Tags]     CONSR-OBMC-BSFC-0027-0001  CONSR-BMC-IPMI-0054-0001  Artemis  robot:skip
#    [Timeout]  5 min 00 seconds
#    Sub-Case  CONSR-BMC-IPMI-0054-0001_1  run ipmi command "Set PEF Configuration Parameters"
#
#CONSR-BMC-IPMI-0055-0001
#    [Documentation]  This test checks IPMI command: "Get PEF Configuration Parameters"
#    [Tags]     CONSR-OBMC-BSFC-0027-0001  CONSR-BMC-IPMI-0055-0001  Artemis  robot:skip
#    [Timeout]  5 min 00 seconds
#    Sub-Case  CONSR-BMC-IPMI-0055-0001_1  run ipmi command "Get PEF Configuration Parameters"

#CONSR-BMC-IPMI-0056-0001
#    [Documentation]  This test checks IPMI command: "Set Last Processed Event ID"
#    [Tags]     CONSR-OBMC-BSFC-0027-0001  CONSR-BMC-IPMI-0056-0001  Artemis  robot:skip
#    [Timeout]  5 min 00 seconds
#    Sub-Case  CONSR-BMC-IPMI-0056-0001_1  run ipmi command "Set Last Processed Event ID"
#
#CONSR-BMC-IPMI-0057-0001
#    [Documentation]  This test checks IPMI command: "Get Last Processed Event ID"
#    [Tags]     CONSR-OBMC-BSFC-0027-0001  CONSR-BMC-IPMI-0057-0001  Artemis  robot:skip
#    [Timeout]  5 min 00 seconds
#    Sub-Case  CONSR-BMC-IPMI-0057-0001_1  run ipmi command "Get Last Processed Event ID"
#
#CONSR-BMC-IPMI-0058-0001
#    [Documentation]  This test checks IPMI command: "Alert Immediate"
#    [Tags]     CONSR-OBMC-BSFC-0027-0001  CONSR-BMC-IPMI-0058-0001  Artemis  robot:skip
#    [Timeout]  5 min 00 seconds
#    Sub-Case  CONSR-BMC-IPMI-0058-0001_1  run ipmi command "Alert Immediate"
#
#CONSR-BMC-IPMI-0059-0001
#    [Documentation]  This test checks IPMI command: "PET Acknowledge"
#    [Tags]     CONSR-OBMC-BSFC-0027-0001  CONSR-BMC-IPMI-0059-0001  Artemis  robot:skip
#    [Timeout]  5 min 00 seconds
#    Sub-Case  CONSR-BMC-IPMI-0059-0001_1  run ipmi command "PET Acknowledge"

#CONSR-BMC-IPMI-0060-0001
#    [Documentation]  This test checks IPMI command: "Set Sensor Hysteresis"
#    [Tags]     CONSR-OBMC-BSFC-0028-0001  CONSR-BMC-IPMI-0060-0001  Artemis  robot:skip
#    [Timeout]  5 min 00 seconds
#    Sub-Case  CONSR-BMC-IPMI-0060-0001_1  run ipmi command "Set Sensor Hysteresis"
#
#CONSR-BMC-IPMI-0061-0001
#    [Documentation]  This test checks IPMI command: "Get Sensor Hysteresis"
#    [Tags]     CONSR-OBMC-BSFC-0028-0001  CONSR-BMC-IPMI-0061-0001  Artemis  robot:skip
#    [Timeout]  5 min 00 seconds
#    Sub-Case  CONSR-BMC-IPMI-0061-0001_1  run ipmi command "Get Sensor Hysteresis"

CONSR-BMC-IPMI-0062-0001
    [Documentation]  This test checks IPMI command: "Set Sensor Threshold"
    [Tags]     CONSR-OBMC-BSFC-0028-0001  CONSR-BMC-IPMI-0062-0001  Artemis_U2
    [Timeout]  5 min 00 seconds
    Sub-Case  CONSR-BMC-IPMI-0062-0001_1  run ipmi command "Set Sensor Threshold"

CONSR-BMC-IPMI-0063-0001
    [Documentation]  This test checks IPMI command: "Get Sensor Threshold"
    [Tags]     CONSR-OBMC-BSFC-0028-0001  CONSR-BMC-IPMI-0063-0001  Artemis_U2
    [Timeout]  5 min 00 seconds
    Sub-Case  CONSR-BMC-IPMI-0063-0001_1  run ipmi command "Get Sensor Threshold"

#CONSR-BMC-IPMI-0064-0001
#    [Documentation]  This test checks IPMI command: "Set Sensor Event Enables"
#    [Tags]     CONSR-OBMC-BSFC-0028-0001  CONSR-BMC-IPMI-0064-0001  Artemis  robot:skip
#    [Timeout]  5 min 00 seconds
#    Sub-Case  CONSR-BMC-IPMI-0064-0001_1  run ipmi command "Set Sensor Event Enable"

CONSR-BMC-IPMI-0065-0001
    [Documentation]  This test checks IPMI command: "Get Sensor Event Enables"
    [Tags]     CONSR-OBMC-BSFC-0028-0001  CONSR-BMC-IPMI-0065-0001  Artemis_U2
    [Timeout]  5 min 00 seconds
    Sub-Case  CONSR-BMC-IPMI-0065-0001_1  run ipmi command "Get Sensor Event Enable"

#CONSR-BMC-IPMI-0066-0001
#    [Documentation]  This test checks IPMI command: "Re-arm Sensor Event"
#    [Tags]     CONSR-OBMC-BSFC-0028-0001  CONSR-BMC-IPMI-0066-0001  Artemis
#    [Timeout]  5 min 00 seconds
#    Sub-Case  CONSR-BMC-IPMI-0066-0001_1  run ipmi command "Re-arm Sensor Event"

CONSR-BMC-IPMI-0067-0001
    [Documentation]  This test checks IPMI command: "Get Sensor Event Status"
    [Tags]     CONSR-OBMC-BSFC-0028-0001  CONSR-BMC-IPMI-0067-0001  Artemis_U2
    [Timeout]  5 min 00 seconds
    Sub-Case  CONSR-BMC-IPMI-0067-0001_1  run ipmi command "Get Sensor Event Status"

CONSR-BMC-IPMI-0068-0001
    [Documentation]  This test checks IPMI command: "Get Sensor Reading"
    [Tags]     CONSR-OBMC-BSFC-0028-0001  CONSR-BMC-IPMI-0068-0001  Artemis_U2
    [Timeout]  5 min 00 seconds
    Sub-Case  CONSR-BMC-IPMI-0068-0001_1  run ipmi command "Get Sensor Reading"

CONSR-BMC-IPMI-0069-0001
    [Documentation]  This test checks IPMI command: "Get FRU Inventory Area Info"
    [Tags]     CONSR-BMC-IPMI-0069-0001  Artemis_U2
    [Timeout]  5 min 00 seconds
    Sub-Case  CONSR-BMC-IPMI-0069-0001_1  run ipmi command "Get FRU Inventory Area Info"

CONSR-BMC-IPMI-0071-0001
    [Documentation]  This test checks IPMI command: "Write FRU Data"
    [Tags]     CONSR-BMC-IPMI-0071-0001  Artemis_U2
    [Timeout]  5 min 00 seconds
    Sub-Case  CONSR-BMC-IPMI-0071-0001_1  run ipmi command "Write FRU Data"

CONSR-BMC-IPMI-0072-0001
    [Documentation]  This test checks IPMI command: "Get SDR Repository Info"
    [Tags]     CONSR-OBMC-BSFC-0029-0001  CONSR-BMC-IPMI-0072-0001  Artemis_U2
    [Timeout]  5 min 00 seconds
    Sub-Case  CONSR-BMC-IPMI-0072-0001_1  run ipmi command "Get SDR Repository Info"

CONSR-BMC-IPMI-0073-0001
    [Documentation]  This test checks IPMI command: "Get SDR Repository Allocation Info"
    [Tags]     CONSR-OBMC-BSFC-0029-0001  CONSR-BMC-IPMI-0073-0001  Artemis_U2
    [Timeout]  5 min 00 seconds
    Sub-Case  CONSR-BMC-IPMI-0073-0001_1  run ipmi command "Get SDR Repository Allocation Info"

CONSR-BMC-IPMI-0074-0001
    [Documentation]  This test checks IPMI command: "Reserve SDR Repository"
    [Tags]     CONSR-OBMC-BSFC-0029-0001  CONSR-BMC-IPMI-0074-0001  Artemis_U2
    [Timeout]  5 min 00 seconds
    Sub-Case  CONSR-BMC-IPMI-0074-0001_1  run ipmi command "Reserve SDR Repository"

CONSR-BMC-IPMI-0075-0001
    [Documentation]  This test checks IPMI command: "Get SDR"
    [Tags]     CONSR-OBMC-BSFC-0029-0001  CONSR-BMC-IPMI-0075-0001  Artemis_U2
    [Timeout]  5 min 00 seconds
    Sub-Case  CONSR-BMC-IPMI-0075-0001_1  run ipmi command "Get SDR"

#CONSR-BMC-IPMI-0076-0001
#    [Documentation]  This test checks IPMI command: "Partial Add SDR"
#    [Tags]     CONSR-OBMC-BSFC-0029-0001  CONSR-BMC-IPMI-0076-0001  Artemis  robot:skip
#    [Timeout]  5 min 00 seconds
#    Sub-Case  CONSR-BMC-IPMI-0076-0001_1  run ipmi command "Partial Add SDR"
#
#CONSR-BMC-IPMI-0077-0001
#    [Documentation]  This test checks IPMI command: "Delete SDR"
#    [Tags]     CONSR-OBMC-BSFC-0029-0001  CONSR-BMC-IPMI-0077-0001  Artemis  robot:skip
#    [Timeout]  5 min 00 seconds
#    Sub-Case  CONSR-BMC-IPMI-0077-0001_1  run ipmi command "Partial Add SDR"
#    Sub-Case  CONSR-BMC-IPMI-0077-0001_2  run ipmi command "Delete SDR"
#
#CONSR-BMC-IPMI-0078-0001
#    [Documentation]  This test checks IPMI command: "Clear SDR Repository"
#    [Tags]     CONSR-OBMC-BSFC-0029-0001  CONSR-BMC-IPMI-0078-0001  Artemis  robot:skip
#    [Timeout]  20 min 00 seconds
#    Sub-Case  CONSR-BMC-IPMI-0078-0001_1  run ipmi command "Clear SDR Repository"
#
#CONSR-BMC-IPMI-0079-0001
#    [Documentation]  This test checks IPMI command: "Enter SDR Repository Update Mode"
#    [Tags]     CONSR-BMC-IPMI-0079-0001  Artemis  robot:skip
#    [Timeout]  20 min 00 seconds
#    Sub-Case  CONSR-BMC-IPMI-0079-0001_1  run ipmi command "Enter SDR Repository Update Mode"

#CONSR-BMC-IPMI-0080-0001
#    [Documentation]  This test checks IPMI command: "Exit SDR Repository Update Mode"
#    [Tags]     CONSR-BMC-IPMI-0080-0001  Artemis  robot:skip
#    [Timeout]  20 min 00 seconds
#    Sub-Case  CONSR-BMC-IPMI-0080-0001_1  run ipmi command "Exit SDR Repository Update Mode"
#
#CONSR-BMC-IPMI-0081-0001
#    [Documentation]  This test checks IPMI command: "Run Initialization Agent"
#    [Tags]     CONSR-OBMC-BSFC-0029-0001  CONSR-BMC-IPMI-0081-0001  Artemis  robot:skip
#    [Timeout]  5 min 00 seconds
#    Sub-Case  CONSR-BMC-IPMI-0081-0001_1  run ipmi command "Run Initialization Agent"

CONSR-BMC-IPMI-0082-0001
    [Documentation]  This test checks IPMI command: "Get SEL Info"
    [Tags]     CONSR-OBMC-BSFC-0030-0001  CONSR-BMC-IPMI-0082-0001  Artemis_U2
    [Timeout]  5 min 00 seconds
    Sub-Case  CONSR-BMC-IPMI-0082-0001_1  run ipmi command "Get SEL Info"

#CONSR-BMC-IPMI-0083-0001
#    [Documentation]  This test checks IPMI command: "Get SEL Allocation Info"
#    [Tags]     CONSR-OBMC-BSFC-0030-0001  CONSR-BMC-IPMI-0083-0001  Artemis
#    [Timeout]  5 min 00 seconds
#    Sub-Case  CONSR-BMC-IPMI-0083-0001_1  run ipmi command "Get SEL Allocation Info"

CONSR-BMC-IPMI-0084-0001
    [Documentation]  This test checks IPMI command: "Reserve SEL"
    [Tags]     CONSR-OBMC-BSFC-0030-0001  CONSR-BMC-IPMI-0084-0001  Artemis_U2
    [Timeout]  5 min 00 seconds
    Sub-Case  CONSR-BMC-IPMI-0084-0001_1  run ipmi command "Reserve SEL"

CONSR-BMC-IPMI-0085-0001
    [Documentation]  This test checks IPMI command: "Get SEL Entry"
    [Tags]     CONSR-OBMC-BSFC-0030-0001  CONSR-BMC-IPMI-0085-0001  Artemis_U2
    [Timeout]  5 min 00 seconds
    Sub-Case  CONSR-BMC-IPMI-0085-0001_1  run ipmi command "Get SEL Entry"

#CONSR-BMC-IPMI-0086-0001
#    [Documentation]  This test checks IPMI command: "Add SEL Entry"
#    [Tags]     CONSR-OBMC-BSFC-0030-0001  CONSR-BMC-IPMI-0086-0001  Artemis
#    [Timeout]  5 min 00 seconds
#    Sub-Case  CONSR-BMC-IPMI-0086-0001_1  run ipmi command "Add SEL Entry"

#CONSR-BMC-IPMI-0087-0001
##TODO:
#    [Documentation]  This test checks IPMI command: "Delete SEL Entry"
#    [Tags]     CONSR-OBMC-BSFC-0030-0001  CONSR-BMC-IPMI-0087-0001  Artemis
#    [Timeout]  5 min 00 seconds
#    Sub-Case  CONSR-BMC-IPMI-0087-0001_1  run ipmi command "Delete SEL Entry"

CONSR-BMC-IPMI-0088-0001
    [Documentation]  This test checks IPMI command: "Clear SEL"
    [Tags]     CONSR-OBMC-BSFC-0030-0001  CONSR-BMC-IPMI-0088-0001  Artemis_U2
    [Timeout]  5 min 00 seconds
    Sub-Case  CONSR-BMC-IPMI-0088-0001_1  run ipmi command "Clear SEL"

CONSR-BMC-IPMI-0089-0001
    [Documentation]  This test checks IPMI command: "Get SEL Time"
    [Tags]     CONSR-OBMC-BSFC-0030-0001  CONSR-BMC-IPMI-0089-0001  Artemis_U2
    [Timeout]  5 min 00 seconds
    Sub-Case  CONSR-BMC-IPMI-0089-0001_1  run ipmi command "Get SEL Time"

#CONSR-BMC-IPMI-0090-0001
#    [Documentation]  This test checks IPMI command: "Set SEL Time"
#    [Tags]     CONSR-OBMC-BSFC-0030-0001  CONSR-BMC-IPMI-0090-0001  Artemis  robot:skip
#    [Timeout]  5 min 00 seconds
#    Sub-Case  CONSR-BMC-IPMI-0090-0001_1  run ipmi command "Set SEL Time"
#
#CONSR-BMC-IPMI-0091-0001
#    [Documentation]  This test checks IPMI command: "Get SEL Time UTC Offset"
#    [Tags]     CONSR-OBMC-BSFC-0030-0001  CONSR-BMC-IPMI-0091-0001  Artemis  robot:skip
#    [Timeout]  5 min 00 seconds
#    Sub-Case  CONSR-BMC-IPMI-0091-0001_1  run ipmi command "Get SEL Time UTC Offset"
#
#CONSR-BMC-IPMI-0092-0001
#    [Documentation]  This test checks IPMI command: "Set SEL Time UTC Offset"
#    [Tags]     CONSR-OBMC-BSFC-0030-0001  CONSR-BMC-IPMI-0092-0001  Artemis  robot:skip
#    [Timeout]  5 min 00 seconds
#    Sub-Case  CONSR-BMC-IPMI-0092-0001_1  run ipmi command "Set SEL Time UTC Offset"
#
#CONSR-BMC-IPMI-0093-0001
#    [Documentation]  This test checks IPMI command: "Set LAN Configuration Parameters"
#    [Tags]     CONSR-BMC-IPMI-0093-0001  Artemis  robot:skip
#    [Timeout]  10 min 00 seconds
#    Sub-Case  CONSR-BMC-IPMI-0093-0001_1  run ipmi command "Set LAN Configuration Parameters"

CONSR-BMC-IPMI-0095-0001
    [Documentation]  This test checks IPMI command: "Get LAN Configuration Parameters"
    [Tags]     CONSR-OBMC-BSFC-0031-0001  CONSR-BMC-IPMI-0095-0001  Artemis_U2  robot:skip  #TODO: LAN port test
    [Timeout]  10 min 00 seconds
    Sub-Case  CONSR-BMC-IPMI-0095-0001_1  run ipmi command "Get LAN Configuration Parameters"

#CONSR-BMC-IPMI-0096-0001
#    [Documentation]  This test checks IPMI command: "Get Message"
#    [Tags]     CONSR-OBMC-BSFC-0024-0001  CONSR-BMC-IPMI-0096-0001  Artemis  robot:skip
#    [Timeout]  10 min 00 seconds
#    Sub-Case  CONSR-BMC-IPMI-0096-0001_1  run ipmi command "Get Message"
#
#CONSR-BMC-IPMI-0097-0001
#    [Documentation]  This test checks IPMI command: "Send Message"
#    [Tags]     CONSR-OBMC-BSFC-0024-0001  CONSR-BMC-IPMI-0097-0001  Artemis  robot:skip
#    [Timeout]  10 min 00 seconds
#    Sub-Case  CONSR-BMC-IPMI-0097-0001_1  run ipmi command "Send Message"

CONSR-BMC-IPMI-0098-0001
    [Documentation]  This test checks IPMI command: "Read Event Message Buffer"
    [Tags]     CONSR-OBMC-BSFC-0024-0001  CONSR-BMC-IPMI-0098-0001  Artemis_U2
    [Timeout]  10 min 00 seconds
    Sub-Case  CONSR-BMC-IPMI-0098-0001_1  run ipmi command "Read Event Message Buffer"

#CONSR-BMC-IPMI-0099-0001
#    [Documentation]  This test checks IPMI command: "Activate Session"
#    [Tags]     CONSR-OBMC-BSFC-0024-0001  CONSR-BMC-IPMI-0099-0001  Artemis  robot:skip
#    [Timeout]  10 min 00 seconds
#    Sub-Case  CONSR-BMC-IPMI-0099-0001_1  run ipmi command "Activate Session"
#
#CONSR-BMC-IPMI-0100-0001
#    [Documentation]  This test checks IPMI command: "Close Session"
#    [Tags]     CONSR-OBMC-BSFC-0024-0001  CONSR-BMC-IPMI-0100-0001  Artemis  robot:skip
#    [Timeout]  10 min 00 seconds
#    Sub-Case  CONSR-BMC-IPMI-0100-0001_1  run ipmi command "Close Session"

CONSR-BMC-IPMI-0101-0001
    [Documentation]  This test checks IPMI command: "Activate Payload"
    [Tags]     CONSR-OBMC-BSFC-0024-0001  CONSR-BMC-IPMI-0101-0001  Artemis_U2
    [Timeout]  10 min 00 seconds
    Sub-Case  CONSR-BMC-IPMI-0101-0001_1  run ipmi command "Activate Payload"

CONSR-BMC-IPMI-0102-0001
    [Documentation]  This test checks IPMI command: "Deactivate Payload"
    [Tags]     CONSR-OBMC-BSFC-0024-0001  CONSR-BMC-IPMI-0102-0001  Artemis_U2
    [Timeout]  10 min 00 seconds
    Sub-Case  CONSR-BMC-IPMI-0102-0001_1  run ipmi command "Deactivate Payload"

#CONSR-BMC-IPMI-0103-0001
#    [Documentation]  This test checks IPMI command: "Set Channel Security Keys 55h"
#    [Tags]     CONSR-OBMC-BSFC-0024-0001  CONSR-BMC-IPMI-0103-0001  Artemis
#    [Timeout]  10 min 00 seconds
#    Sub-Case  CONSR-BMC-IPMI-0103-0001_1  run ipmi command "Set Channel Security Keys 55h"

CONSR-OBMC-RDFT-0001-0001
    [Documentation]  This test checks Redfish   Service Root
    [Tags]   CONSR-OBMC-RDFT-0001-0001  Artemis_U2
    [Timeout]  5 min 00 seconds
    Step  1   Verify service root property  %{bmc_ipv4_ip_1}  %{bmc_username_1}  %{bmc_password_1}
    Step  2   Verify service root property  %{bmc_ipv4_ip_2}  %{bmc_username_2}  %{bmc_password_2}

CONSR-OBMC-RDFT-0160-0001
    [Documentation]  This test checks Redfish JSON Schema file-1 AccountService
    [Tags]   CONSR-OBMC-RDFT-0160-0001  Artemis_U2
    [Timeout]  5 min 00 seconds
    Step  1   Verify JSON Schema  ${resource_JSONSchema_AccountService}  ${odata_type_value_AccountService}  ${Language_AccountService}  ${Location_AccountService}  ${Description_AccountService}  ${Id_AccountService}  ${Languages_odatacount_AccountService}  ${Location_odatacount_AccountService}  ${Name_AccountService}  ${Schema_AccountService}

CONSR-OBMC-RDFT-0162-0001
    [Documentation]  This test checks Redfish JSON Schema file-3 AggregationService
    [Tags]   CONSR-OBMC-RDFT-0162-0001  Artemis_U2
    [Timeout]  5 min 00 seconds
    Step  1   Verify JSON Schema  ${resource_JSONSchema_AggregationService}  ${odata_type_value_AggregationService}  ${Language_AggregationService}  ${Location_AggregationService}  ${Description_AggregationService}  ${Id_AggregationService}  ${Languages_odatacount_AggregationService}  ${Location_odatacount_AggregationService}  ${Name_AggregationService}  ${Schema_AggregationService}

CONSR-OBMC-RDFT-0164-0001
    [Documentation]  This test checks Redfish JSON Schema file-5 AggregationSourceCollection
    [Tags]   CONSR-OBMC-RDFT-0164-0001  Artemis_U2
    [Timeout]  5 min 00 seconds
    Step  1   Verify JSON Schema  ${resource_JSONSchema_AggregationSourceCollection}  ${odata_type_value_AggregationSourceCollection}  ${Language_AggregationSourceCollection}  ${Location_AggregationSourceCollection}  ${Description_AggregationSourceCollection}  ${Id_AggregationSourceCollection}  ${Languages_odatacount_AggregationSourceCollection}  ${Location_odatacount_AggregationSourceCollection}  ${Name_AggregationSourceCollection}  ${Schema_AggregationSourceCollection}

CONSR-OBMC-RDFT-0166-0001
    [Documentation]  This test checks Redfish JSON Schema file-7 AttributeRegistry
    [Tags]   CONSR-OBMC-RDFT-0166-0001  Artemis_U2
    [Timeout]  5 min 00 seconds
    Step  1   Verify JSON Schema  ${resource_JSONSchema_AttributeRegistry}  ${odata_type_value_AttributeRegistry}  ${Language_AttributeRegistry}  ${Location_AttributeRegistry}  ${Description_AttributeRegistry}  ${Id_AttributeRegistry}  ${Languages_odatacount_AttributeRegistry}  ${Location_odatacount_AttributeRegistry}  ${Name_AttributeRegistry}  ${Schema_AttributeRegistry}

CONSR-OBMC-RDFT-0168-0001
    [Documentation]  This test checks Redfish JSON Schema file-9 Cable
    [Tags]   CONSR-OBMC-RDFT-0168-0001  Artemis_U2
    [Timeout]  5 min 00 seconds
    Step  1   Verify JSON Schema  ${resource_JSONSchema_Cable}  ${odata_type_value_Cable}  ${Language_Cable}  ${Location_Cable}  ${Description_Cable}  ${Id_Cable}  ${Languages_odatacount_Cable}  ${Location_odatacount_Cable}  ${Name_Cable}  ${Schema_Cable}

CONSR-OBMC-RDFT-0170-0001
    [Documentation]  This test checks Redfish JSON Schema file-11 Certificate
    [Tags]   CONSR-OBMC-RDFT-0170-0001  Artemis_U2
    [Timeout]  5 min 00 seconds
    Step  1   Verify JSON Schema  ${resource_JSONSchema_Certificate}  ${odata_type_value_Certificate}  ${Language_Certificate}  ${Location_Certificate}  ${Description_Certificate}  ${Id_Certificate}  ${Languages_odatacount_Certificate}  ${Location_odatacount_Certificate}  ${Name_Certificate}  ${Schema_Certificate}

CONSR-OBMC-RDFT-0172-0001
    [Documentation]  This test checks Redfish JSON Schema file-13 CertificateLocations
    [Tags]   CONSR-OBMC-RDFT-0172-0001  Artemis_U2
    [Timeout]  5 min 00 seconds
    Step  1   Verify JSON Schema  ${resource_JSONSchema_CertificateLocations}  ${odata_type_value_CertificateLocations}  ${Language_CertificateLocations}  ${Location_CertificateLocations}  ${Description_CertificateLocations}  ${Id_CertificateLocations}  ${Languages_odatacount_CertificateLocations}  ${Location_odatacount_CertificateLocations}  ${Name_CertificateLocations}  ${Schema_CertificateLocations}

CONSR-OBMC-RDFT-0174-0001
    [Documentation]  This test checks Redfish JSON Schema file-15 Chassis
    [Tags]   CONSR-OBMC-RDFT-0174-0001  Artemis_U2
    [Timeout]  5 min 00 seconds
    Step  1   Verify JSON Schema  ${resource_JSONSchema_Chassis}  ${odata_type_value_Chassis}  ${Language_Chassis}  ${Location_Chassis}  ${Description_Chassis}  ${Id_Chassis}  ${Languages_odatacount_Chassis}  ${Location_odatacount_Chassis}  ${Name_Chassis}  ${Schema_Chassis}

CONSR-OBMC-RDFT-0176-0001
    [Documentation]  This test checks Redfish JSON Schema file-17 ComponentIntegrity
    [Tags]   CONSR-OBMC-RDFT-0176-0001  Artemis_U2
    [Timeout]  5 min 00 seconds
    Step  1   Verify JSON Schema  ${resource_JSONSchema_ComponentIntegrity}  ${odata_type_value_ComponentIntegrity}  ${Language_ComponentIntegrity}  ${Location_ComponentIntegrity}  ${Description_ComponentIntegrity}  ${Id_ComponentIntegrity}  ${Languages_odatacount_ComponentIntegrity}  ${Location_odatacount_ComponentIntegrity}  ${Name_ComponentIntegrity}  ${Schema_ComponentIntegrity}

CONSR-OBMC-RDFT-0178-0001
    [Documentation]  This test checks Redfish JSON Schema file-19 ComputerSystem
    [Tags]   CONSR-OBMC-RDFT-0178-0001  Artemis_U2
    [Timeout]  5 min 00 seconds
    Step  1   Verify JSON Schema  ${resource_JSONSchema_ComputerSystem}  ${odata_type_value_ComputerSystem}  ${Language_ComputerSystem}  ${Location_ComputerSystem}  ${Description_ComputerSystem}  ${Id_ComputerSystem}  ${Languages_odatacount_ComputerSystem}  ${Location_odatacount_ComputerSystem}  ${Name_ComputerSystem}  ${Schema_ComputerSystem}

CONSR-OBMC-RDFT-0180-0001
    [Documentation]  This test checks Redfish JSON Schema file-21 Drive
    [Tags]   CONSR-OBMC-RDFT-0180-0001  Artemis_U2
    [Timeout]  5 min 00 seconds
    Step  1   Verify JSON Schema  ${resource_JSONSchema_Drive}  ${odata_type_value_Drive}  ${Language_Drive}  ${Location_Drive}  ${Description_Drive}  ${Id_Drive}  ${Languages_odatacount_Drive}  ${Location_odatacount_Drive}  ${Name_Drive}  ${Schema_Drive}

CONSR-OBMC-RDFT-0182-0001
    [Documentation]  This test checks Redfish JSON Schema file-23 EnvironmentMetrics
    [Tags]   CONSR-OBMC-RDFT-0182-0001  Artemis_U2
    [Timeout]  5 min 00 seconds
    Step  1   Verify JSON Schema  ${resource_JSONSchema_EnvironmentMetrics}  ${odata_type_value_EnvironmentMetrics}  ${Language_EnvironmentMetrics}  ${Location_EnvironmentMetrics}  ${Description_EnvironmentMetrics}  ${Id_EnvironmentMetrics}  ${Languages_odatacount_EnvironmentMetrics}  ${Location_odatacount_EnvironmentMetrics}  ${Name_EnvironmentMetrics}  ${Schema_EnvironmentMetrics}

CONSR-OBMC-RDFT-0184-0001
    [Documentation]  This test checks Redfish JSON Schema file-25 EthernetInterfaceCollection
    [Tags]   CONSR-OBMC-RDFT-0184-0001  Artemis_U2
    [Timeout]  5 min 00 seconds
    Step  1   Verify JSON Schema  ${resource_JSONSchema_EthernetInterfaceCollection}  ${odata_type_value_EthernetInterfaceCollection}  ${Language_EthernetInterfaceCollection}  ${Location_EthernetInterfaceCollection}  ${Description_EthernetInterfaceCollection}  ${Id_EthernetInterfaceCollection}  ${Languages_odatacount_EthernetInterfaceCollection}  ${Location_odatacount_EthernetInterfaceCollection}  ${Name_EthernetInterfaceCollection}  ${Schema_EthernetInterfaceCollection}

CONSR-OBMC-RDFT-0186-0001
    [Documentation]  This test checks Redfish JSON Schema file-27 EventDestination
    [Tags]   CONSR-OBMC-RDFT-0186-0001  Artemis_U2
    [Timeout]  5 min 00 seconds
    Step  1   Verify JSON Schema  ${resource_JSONSchema_EventDestination}  ${odata_type_value_EventDestination}  ${Language_EventDestination}  ${Location_EventDestination}  ${Description_EventDestination}  ${Id_EventDestination}  ${Languages_odatacount_EventDestination}  ${Location_odatacount_EventDestination}  ${Name_EventDestination}  ${Schema_EventDestination}

CONSR-OBMC-RDFT-0188-0001
    [Documentation]  This test checks Redfish JSON Schema file-29 EventService
    [Tags]   CONSR-OBMC-RDFT-0188-0001  Artemis_U2
    [Timeout]  5 min 00 seconds
    Step  1   Verify JSON Schema  ${resource_JSONSchema_EventService}  ${odata_type_value_EventService}  ${Language_EventService}  ${Location_EventService}  ${Description_EventService}  ${Id_EventService}  ${Languages_odatacount_EventService}  ${Location_odatacount_EventService}  ${Name_EventService}  ${Schema_EventService}

CONSR-OBMC-RDFT-0190-0001
    [Documentation]  This test checks Redfish JSON Schema file-31 FabricAdapterCollection
    [Tags]   CONSR-OBMC-RDFT-0190-0001  Artemis_U2
    [Timeout]  5 min 00 seconds
    Step  1   Verify JSON Schema  ${resource_JSONSchema_FabricAdapterCollection}  ${odata_type_value_FabricAdapterCollection}  ${Language_FabricAdapterCollection}  ${Location_FabricAdapterCollection}  ${Description_FabricAdapterCollection}  ${Id_FabricAdapterCollection}  ${Languages_odatacount_FabricAdapterCollection}  ${Location_odatacount_FabricAdapterCollection}  ${Name_FabricAdapterCollection}  ${Schema_FabricAdapterCollection}

CONSR-OBMC-RDFT-0192-0001
    [Documentation]  This test checks Redfish JSON Schema file-33 FanCollection
    [Tags]   CONSR-OBMC-RDFT-0192-0001  Artemis_U2
    [Timeout]  5 min 00 seconds
    Step  1   Verify JSON Schema  ${resource_JSONSchema_FanCollection}  ${odata_type_value_FanCollection}  ${Language_FanCollection}  ${Location_FanCollection}  ${Description_FanCollection}  ${Id_FanCollection}  ${Languages_odatacount_FanCollection}  ${Location_odatacount_FanCollection}  ${Name_FanCollection}  ${Schema_FanCollection}

CONSR-OBMC-RDFT-0194-0001
    [Documentation]  This test checks Redfish JSON Schema file-35 JsonSchemaFile
    [Tags]   CONSR-OBMC-RDFT-0194-0001  Artemis_U2
    [Timeout]  5 min 00 seconds
    Step  1   Verify JSON Schema  ${resource_JSONSchema_JsonSchemaFile}  ${odata_type_value_JsonSchemaFile}  ${Language_JsonSchemaFile}  ${Location_JsonSchemaFile}  ${Description_JsonSchemaFile}  ${Id_JsonSchemaFile}  ${Languages_odatacount_JsonSchemaFile}  ${Location_odatacount_JsonSchemaFile}  ${Name_JsonSchemaFile}  ${Schema_JsonSchemaFile}

CONSR-OBMC-RDFT-0196-0001
    [Documentation]  This test checks Redfish JSON Schema file-37 LogEntry
    [Tags]   CONSR-OBMC-RDFT-0196-0001  Artemis_U2
    [Timeout]  5 min 00 seconds
    Step  1   Verify JSON Schema  ${resource_JSONSchema_LogEntry}  ${odata_type_value_LogEntry}  ${Language_LogEntry}  ${Location_LogEntry}  ${Description_LogEntry}  ${Id_LogEntry}  ${Languages_odatacount_LogEntry}  ${Location_odatacount_LogEntry}  ${Name_LogEntry}  ${Schema_LogEntry}

CONSR-OBMC-RDFT-0198-0001
    [Documentation]  This test checks Redfish JSON Schema file-39 LogService
    [Tags]   CONSR-OBMC-RDFT-0198-0001  Artemis_U2
    [Timeout]  5 min 00 seconds
    Step  1   Verify JSON Schema  ${resource_JSONSchema_LogService}  ${odata_type_value_LogService}  ${Language_LogService}  ${Location_LogService}  ${Description_LogService}  ${Id_LogService}  ${Languages_odatacount_LogService}  ${Location_odatacount_LogService}  ${Name_LogService}  ${Schema_LogService}

CONSR-OBMC-RDFT-0200-0001
    [Documentation]  This test checks Redfish JSON Schema file-41 Manager
    [Tags]   CONSR-OBMC-RDFT-0200-0001  Artemis_U2
    [Timeout]  5 min 00 seconds
    Step  1   Verify JSON Schema  ${resource_JSONSchema_Manager}  ${odata_type_value_Manager}  ${Language_Manager}  ${Location_Manager}  ${Description_Manager}  ${Id_Manager}  ${Languages_odatacount_Manager}  ${Location_odatacount_Manager}  ${Name_Manager}  ${Schema_Manager}

CONSR-OBMC-RDFT-0202-0001
    [Documentation]  This test checks Redfish JSON Schema file-43 ManagerAccountCollection
    [Tags]   CONSR-OBMC-RDFT-0202-0001  Artemis_U2
    [Timeout]  5 min 00 seconds
    Step  1   Verify JSON Schema  ${resource_JSONSchema_ManagerAccountCollection}  ${odata_type_value_ManagerAccountCollection}  ${Language_ManagerAccountCollection}  ${Location_ManagerAccountCollection}  ${Description_ManagerAccountCollection}  ${Id_ManagerAccountCollection}  ${Languages_odatacount_ManagerAccountCollection}  ${Location_odatacount_ManagerAccountCollection}  ${Name_ManagerAccountCollection}  ${Schema_ManagerAccountCollection}

CONSR-OBMC-RDFT-0204-0001
    [Documentation]  This test checks Redfish JSON Schema file-45 ManagerDiagnosticData
    [Tags]   CONSR-OBMC-RDFT-0204-0001  Artemis_U2
    [Timeout]  5 min 00 seconds
    Step  1   Verify JSON Schema  ${resource_JSONSchema_ManagerDiagnosticData}  ${odata_type_value_ManagerDiagnosticData}  ${Language_ManagerDiagnosticData}  ${Location_ManagerDiagnosticData}  ${Description_ManagerDiagnosticData}  ${Id_ManagerDiagnosticData}  ${Languages_odatacount_ManagerDiagnosticData}  ${Location_odatacount_ManagerDiagnosticData}  ${Name_ManagerDiagnosticData}  ${Schema_ManagerDiagnosticData}

CONSR-OBMC-RDFT-0206-0001
    [Documentation]  This test checks Redfish JSON Schema file-47 Memory
    [Tags]   CONSR-OBMC-RDFT-0206-0001  Artemis_U2
    [Timeout]  5 min 00 seconds
    Step  1   Verify JSON Schema  ${resource_JSONSchema_Memory}  ${odata_type_value_Memory}  ${Language_Memory}  ${Location_Memory}  ${Description_Memory}  ${Id_Memory}  ${Languages_odatacount_Memory}  ${Location_odatacount_Memory}  ${Name_Memory}  ${Schema_Memory}

CONSR-OBMC-RDFT-0208-0001
    [Documentation]  This test checks Redfish JSON Schema file-49 Message
    [Tags]   CONSR-OBMC-RDFT-0208-0001  Artemis_U2
    [Timeout]  5 min 00 seconds
    Step  1   Verify JSON Schema  ${resource_JSONSchema_Message}  ${odata_type_value_Message}  ${Language_Message}  ${Location_Message}  ${Description_Message}  ${Id_Message}  ${Languages_odatacount_Message}  ${Location_odatacount_Message}  ${Name_Message}  ${Schema_Message}

CONSR-OBMC-RDFT-0210-0001
    [Documentation]  This test checks Redfish JSON Schema file-51 MessageRegistryCollection
    [Tags]   CONSR-OBMC-RDFT-0210-0001  Artemis_U2
    [Timeout]  5 min 00 seconds
    Step  1   Verify JSON Schema  ${resource_JSONSchema_MessageRegistryCollection}  ${odata_type_value_MessageRegistryCollection}  ${Language_MessageRegistryCollection}  ${Location_MessageRegistryCollection}  ${Description_MessageRegistryCollection}  ${Id_MessageRegistryCollection}  ${Languages_odatacount_MessageRegistryCollection}  ${Location_odatacount_MessageRegistryCollection}  ${Name_MessageRegistryCollection}  ${Schema_MessageRegistryCollection}

CONSR-OBMC-RDFT-0212-0001
    [Documentation]  This test checks Redfish JSON Schema file-53 MessageRegistryCollection
    [Tags]   CONSR-OBMC-RDFT-0212-0001  Artemis_U2
    [Timeout]  5 min 00 seconds
    Step  1   Verify JSON Schema  ${resource_JSONSchema_MessageRegistryCollection}  ${odata_type_value_MessageRegistryCollection}  ${Language_MessageRegistryCollection}  ${Location_MessageRegistryCollection}  ${Description_MessageRegistryCollection}  ${Id_MessageRegistryCollection}  ${Languages_odatacount_MessageRegistryCollection}  ${Location_odatacount_MessageRegistryCollection}  ${Name_MessageRegistryCollection}  ${Schema_MessageRegistryCollection}

CONSR-OBMC-RDFT-0214-0001
    [Documentation]  This test checks Redfish JSON Schema file-55 MetricDefinitionCollection
    [Tags]   CONSR-OBMC-RDFT-0214-0001  Artemis_U2
    [Timeout]  5 min 00 seconds
    Step  1   Verify JSON Schema  ${resource_JSONSchema_MetricDefinitionCollection}  ${odata_type_value_MetricDefinitionCollection}  ${Language_MetricDefinitionCollection}  ${Location_MetricDefinitionCollection}  ${Description_MetricDefinitionCollection}  ${Id_MetricDefinitionCollection}  ${Languages_odatacount_MetricDefinitionCollection}  ${Location_odatacount_MetricDefinitionCollection}  ${Name_MetricDefinitionCollection}  ${Schema_MetricDefinitionCollection}

CONSR-OBMC-RDFT-0216-0001
    [Documentation]  This test checks Redfish JSON Schema file-57 MetricReportCollection
    [Tags]   CONSR-OBMC-RDFT-0216-0001  Artemis_U2
    [Timeout]  5 min 00 seconds
    Step  1   Verify JSON Schema  ${resource_JSONSchema_MetricReportCollection}  ${odata_type_value_MetricReportCollection}  ${Language_MetricReportCollection}  ${Location_MetricReportCollection}  ${Description_MetricReportCollection}  ${Id_MetricReportCollection}  ${Languages_odatacount_MetricReportCollection}  ${Location_odatacount_MetricReportCollection}  ${Name_MetricReportCollection}  ${Schema_MetricReportCollection}

CONSR-OBMC-RDFT-0218-0001
    [Documentation]  This test checks Redfish JSON Schema file-59 MetricReportDefinitionCollection
    [Tags]   CONSR-OBMC-RDFT-0218-0001  Artemis_U2
    [Timeout]  5 min 00 seconds
    Step  1   Verify JSON Schema  ${resource_JSONSchema_MetricReportDefinitionCollection}  ${odata_type_value_MetricReportDefinitionCollection}  ${Language_MetricReportDefinitionCollection}  ${Location_MetricReportDefinitionCollection}  ${Description_MetricReportDefinitionCollection}  ${Id_MetricReportDefinitionCollection}  ${Languages_odatacount_MetricReportDefinitionCollection}  ${Location_odatacount_MetricReportDefinitionCollection}  ${Name_MetricReportDefinitionCollection}  ${Schema_MetricReportDefinitionCollection}

CONSR-OBMC-RDFT-0220-0001
    [Documentation]  This test checks Redfish JSON Schema file-61 odata-v4
    [Tags]   CONSR-OBMC-RDFT-0220-0001  Artemis_U2
    [Timeout]  5 min 00 seconds
    Step  1   Verify JSON Schema  ${resource_JSONSchema_odata_v4}  ${odata_type_value_odata_v4}  ${Language_odata_v4}  ${Location_odata_v4}  ${Description_odata_v4}  ${Id_odata_v4}  ${Languages_odatacount_odata_v4}  ${Location_odatacount_odata_v4}  ${Name_odata_v4}  ${Schema_odata_v4}

CONSR-OBMC-RDFT-0222-0001
    [Documentation]  This test checks Redfish JSON Schema file-63 OperatingConfigCollection
    [Tags]   CONSR-OBMC-RDFT-0222-0001  Artemis_U2
    [Timeout]  5 min 00 seconds
    Step  1   Verify JSON Schema  ${resource_JSONSchema_OperatingConfigCollection}  ${odata_type_value_OperatingConfigCollection}  ${Language_OperatingConfigCollection}  ${Location_OperatingConfigCollection}  ${Description_OperatingConfigCollection}  ${Id_OperatingConfigCollection}  ${Languages_odatacount_OperatingConfigCollection}  ${Location_odatacount_OperatingConfigCollection}  ${Name_OperatingConfigCollection}  ${Schema_OperatingConfigCollection}

CONSR-OBMC-RDFT-0224-0001
    [Documentation]  This test checks Redfish JSON Schema file-65 PCIeDeviceCollection
    [Tags]   CONSR-OBMC-RDFT-0224-0001  Artemis_U2
    [Timeout]  5 min 00 seconds
    Step  1   Verify JSON Schema  ${resource_JSONSchema_PCIeDeviceCollection}  ${odata_type_value_PCIeDeviceCollection}  ${Language_PCIeDeviceCollection}  ${Location_PCIeDeviceCollection}  ${Description_PCIeDeviceCollection}  ${Id_PCIeDeviceCollection}  ${Languages_odatacount_PCIeDeviceCollection}  ${Location_odatacount_PCIeDeviceCollection}  ${Name_PCIeDeviceCollection}  ${Schema_PCIeDeviceCollection}

CONSR-OBMC-RDFT-0226-0001
    [Documentation]  This test checks Redfish JSON Schema file-67 PCIeFunctionCollection
    [Tags]   CONSR-OBMC-RDFT-0226-0001  Artemis_U2
    [Timeout]  5 min 00 seconds
    Step  1   Verify JSON Schema  ${resource_JSONSchema_PCIeFunctionCollection}  ${odata_type_value_PCIeFunctionCollection}  ${Language_PCIeFunctionCollection}  ${Location_PCIeFunctionCollection}  ${Description_PCIeFunctionCollection}  ${Id_PCIeFunctionCollection}  ${Languages_odatacount_PCIeFunctionCollection}  ${Location_odatacount_PCIeFunctionCollection}  ${Name_PCIeFunctionCollection}  ${Schema_PCIeFunctionCollection}

CONSR-OBMC-RDFT-0228-0001
    [Documentation]  This test checks Redfish JSON Schema file-69 PhysicalContext
    [Tags]   CONSR-OBMC-RDFT-0228-0001  Artemis_U2
    [Timeout]  5 min 00 seconds
    Step  1   Verify JSON Schema  ${resource_JSONSchema_PhysicalContext}  ${odata_type_value_PhysicalContext}  ${Language_PhysicalContext}  ${Location_PhysicalContext}  ${Description_PhysicalContext}  ${Id_PhysicalContext}  ${Languages_odatacount_PhysicalContext}  ${Location_odatacount_PhysicalContext}  ${Name_PhysicalContext}  ${Schema_PhysicalContext}

CONSR-OBMC-RDFT-0230-0001
    [Documentation]  This test checks Redfish JSON Schema file-71 PortCollection
    [Tags]   CONSR-OBMC-RDFT-0230-0001  Artemis_U2
    [Timeout]  5 min 00 seconds
    Step  1   Verify JSON Schema  ${resource_JSONSchema_PortCollection}  ${odata_type_value_PortCollection}  ${Language_PortCollection}  ${Location_PortCollection}  ${Description_PortCollection}  ${Id_PortCollection}  ${Languages_odatacount_PortCollection}  ${Location_odatacount_PortCollection}  ${Name_PortCollection}  ${Schema_PortCollection}

CONSR-OBMC-RDFT-0232-0001
    [Documentation]  This test checks Redfish JSON Schema file-73 PowerSubsystem
    [Tags]   CONSR-OBMC-RDFT-0232-0001  Artemis_U2
    [Timeout]  5 min 00 seconds
    Step  1   Verify JSON Schema  ${resource_JSONSchema_PowerSubsystem}  ${odata_type_value_PowerSubsystem}  ${Language_PowerSubsystem}  ${Location_PowerSubsystem}  ${Description_PowerSubsystem}  ${Id_PowerSubsystem}  ${Languages_odatacount_PowerSubsystem}  ${Location_odatacount_PowerSubsystem}  ${Name_PowerSubsystem}  ${Schema_PowerSubsystem}

CONSR-OBMC-RDFT-0234-0001
    [Documentation]  This test checks Redfish JSON Schema file-75 PowerSupplyCollection
    [Tags]   CONSR-OBMC-RDFT-0234-0001  Artemis_U2
    [Timeout]  5 min 00 seconds
    Step  1   Verify JSON Schema  ${resource_JSONSchema_PowerSupplyCollection}  ${odata_type_value_PowerSupplyCollection}  ${Language_PowerSupplyCollection}  ${Location_PowerSupplyCollection}  ${Description_PowerSupplyCollection}  ${Id_PowerSupplyCollection}  ${Languages_odatacount_PowerSupplyCollection}  ${Location_odatacount_PowerSupplyCollection}  ${Name_PowerSupplyCollection}  ${Schema_PowerSupplyCollection}

CONSR-OBMC-RDFT-0236-0001
    [Documentation]  This test checks Redfish JSON Schema file-77 Processor
    [Tags]   CONSR-OBMC-RDFT-0236-0001  Artemis_U2
    [Timeout]  5 min 00 seconds
    Step  1   Verify JSON Schema  ${resource_JSONSchema_Processor}  ${odata_type_value_Processor}  ${Language_Processor}  ${Location_Processor}  ${Description_Processor}  ${Id_Processor}  ${Languages_odatacount_Processor}  ${Location_odatacount_Processor}  ${Name_Processor}  ${Schema_Processor}

CONSR-OBMC-RDFT-0238-0001
    [Documentation]  This test checks Redfish JSON Schema file-79 redfish-error
    [Tags]   CONSR-OBMC-RDFT-0238-0001  Artemis_U2
    [Timeout]  5 min 00 seconds
    Step  1   Verify JSON Schema  ${resource_JSONSchema_redfish_error}  ${odata_type_value_redfish_error}  ${Language_redfish_error}  ${Location_redfish_error}  ${Description_redfish_error}  ${Id_redfish_error}  ${Languages_odatacount_redfish_error}  ${Location_odatacount_redfish_error}  ${Name_redfish_error}  ${Schema_redfish_error}

CONSR-OBMC-RDFT-0240-0001
    [Documentation]  This test checks Redfish JSON Schema file-81 redfish-schema
    [Tags]   CONSR-OBMC-RDFT-0240-0001  Artemis_U2
    [Timeout]  5 min 00 seconds
    Step  1   Verify JSON Schema  ${resource_JSONSchema_redfish_schema}  ${odata_type_value_redfish_schema}  ${Language_redfish_schema}  ${Location_redfish_schema}  ${Description_redfish_schema}  ${Id_redfish_schema}  ${Languages_odatacount_redfish_schema}  ${Location_odatacount_redfish_schema}  ${Name_redfish_schema}  ${Schema_redfish_schema}

CONSR-OBMC-RDFT-0242-0001
    [Documentation]  This test checks Redfish JSON Schema file-83 Redundancy
    [Tags]   CONSR-OBMC-RDFT-0242-0001  Artemis_U2
    [Timeout]  5 min 00 seconds
    Step  1   Verify JSON Schema  ${resource_JSONSchema_Redundancy}  ${odata_type_value_Redundancy}  ${Language_Redundancy}  ${Location_Redundancy}  ${Description_Redundancy}  ${Id_Redundancy}  ${Languages_odatacount_Redundancy}  ${Location_odatacount_Redundancy}  ${Name_Redundancy}  ${Schema_Redundancy}

CONSR-OBMC-RDFT-0244-0001
    [Documentation]  This test checks Redfish JSON Schema file-85 Role
    [Tags]   CONSR-OBMC-RDFT-0244-0001  Artemis_U2
    [Timeout]  5 min 00 seconds
    Step  1   Verify JSON Schema  ${resource_JSONSchema_Role}  ${odata_type_value_Role}  ${Language_Role}  ${Location_Role}  ${Description_Role}  ${Id_Role}  ${Languages_odatacount_Role}  ${Location_odatacount_Role}  ${Name_Role}  ${Schema_Role}

CONSR-OBMC-RDFT-0246-0001
    [Documentation]  This test checks Redfish JSON Schema file-87 Sensor
    [Tags]   CONSR-OBMC-RDFT-0246-0001  Artemis_U2
    [Timeout]  5 min 00 seconds
    Step  1   Verify JSON Schema  ${resource_JSONSchema_Sensor}  ${odata_type_value_Sensor}  ${Language_Sensor}  ${Location_Sensor}  ${Description_Sensor}  ${Id_Sensor}  ${Languages_odatacount_Sensor}  ${Location_odatacount_Sensor}  ${Name_Sensor}  ${Schema_Sensor}

CONSR-OBMC-RDFT-0248-0001
    [Documentation]  This test checks Redfish JSON Schema file-89 ServiceRoot
    [Tags]   CONSR-OBMC-RDFT-0248-0001  Artemis_U2
    [Timeout]  5 min 00 seconds
    Step  1   Verify JSON Schema  ${resource_JSONSchema_ServiceRoot}  ${odata_type_value_ServiceRoot}  ${Language_ServiceRoot}  ${Location_ServiceRoot}  ${Description_ServiceRoot}  ${Id_ServiceRoot}  ${Languages_odatacount_ServiceRoot}  ${Location_odatacount_ServiceRoot}  ${Name_ServiceRoot}  ${Schema_ServiceRoot}

CONSR-OBMC-RDFT-0250-0001
    [Documentation]  This test checks Redfish JSON Schema file-91 SessionCollection
    [Tags]   CONSR-OBMC-RDFT-0250-0001  Artemis_U2
    [Timeout]  5 min 00 seconds
    Step  1   Verify JSON Schema  ${resource_JSONSchema_SessionCollection}  ${odata_type_value_SessionCollection}  ${Language_SessionCollection}  ${Location_SessionCollection}  ${Description_SessionCollection}  ${Id_SessionCollection}  ${Languages_odatacount_SessionCollection}  ${Location_odatacount_SessionCollection}  ${Name_SessionCollection}  ${Schema_SessionCollection}

CONSR-OBMC-RDFT-0252-0001
    [Documentation]  This test checks Redfish JSON Schema file-93 Settings
    [Tags]   CONSR-OBMC-RDFT-0252-0001  Artemis_U2
    [Timeout]  5 min 00 seconds
    Step  1   Verify JSON Schema  ${resource_JSONSchema_Settings}  ${odata_type_value_Settings}  ${Language_Settings}  ${Location_Settings}  ${Description_Settings}  ${Id_Settings}  ${Languages_odatacount_Settings}  ${Location_odatacount_Settings}  ${Name_Settings}  ${Schema_Settings}

CONSR-OBMC-RDFT-0254-0001
    [Documentation]  This test checks Redfish JSON Schema file-95 SoftwareInventoryCollection
    [Tags]   CONSR-OBMC-RDFT-0254-0001  Artemis_U2
    [Timeout]  5 min 00 seconds
    Step  1   Verify JSON Schema  ${resource_JSONSchema_SoftwareInventoryCollection}  ${odata_type_value_SoftwareInventoryCollection}  ${Language_SoftwareInventoryCollection}  ${Location_SoftwareInventoryCollection}  ${Description_SoftwareInventoryCollection}  ${Id_SoftwareInventoryCollection}  ${Languages_odatacount_SoftwareInventoryCollection}  ${Location_odatacount_SoftwareInventoryCollection}  ${Name_SoftwareInventoryCollection}  ${Schema_SoftwareInventoryCollection}

CONSR-OBMC-RDFT-0256-0001
    [Documentation]  This test checks Redfish JSON Schema file-97 StorageCollection
    [Tags]   CONSR-OBMC-RDFT-0256-0001  Artemis_U2
    [Timeout]  5 min 00 seconds
    Step  1   Verify JSON Schema  ${resource_JSONSchema_StorageCollection}  ${odata_type_value_StorageCollection}  ${Language_StorageCollection}  ${Location_StorageCollection}  ${Description_StorageCollection}  ${Id_StorageCollection}  ${Languages_odatacount_StorageCollection}  ${Location_odatacount_StorageCollection}  ${Name_StorageCollection}  ${Schema_StorageCollection}

CONSR-OBMC-RDFT-0258-0001
    [Documentation]  This test checks Redfish JSON Schema file-99 StorageControllerCollection
    [Tags]   CONSR-OBMC-RDFT-0258-0001  Artemis_U2
    [Timeout]  5 min 00 seconds
    Step  1   Verify JSON Schema  ${resource_JSONSchema_StorageControllerCollection}  ${odata_type_value_StorageControllerCollection}  ${Language_StorageControllerCollection}  ${Location_StorageControllerCollection}  ${Description_StorageControllerCollection}  ${Id_StorageControllerCollection}  ${Languages_odatacount_StorageControllerCollection}  ${Location_odatacount_StorageControllerCollection}  ${Name_StorageControllerCollection}  ${Schema_StorageControllerCollection}

CONSR-OBMC-RDFT-0260-0001
    [Documentation]  This test checks Redfish JSON Schema file-101 TaskCollection
    [Tags]   CONSR-OBMC-RDFT-0260-0001  Artemis_U2
    [Timeout]  5 min 00 seconds
    Step  1   Verify JSON Schema  ${resource_JSONSchema_TaskCollection}  ${odata_type_value_TaskCollection}  ${Language_TaskCollection}  ${Location_TaskCollection}  ${Description_TaskCollection}  ${Id_TaskCollection}  ${Languages_odatacount_TaskCollection}  ${Location_odatacount_TaskCollection}  ${Name_TaskCollection}  ${Schema_TaskCollection}

CONSR-OBMC-RDFT-0262-0001
    [Documentation]  This test checks Redfish JSON Schema file-103 TelemetryService
    [Tags]   CONSR-OBMC-RDFT-0262-0001  Artemis_U2
    [Timeout]  5 min 00 seconds
    Step  1   Verify JSON Schema  ${resource_JSONSchema_TelemetryService}  ${odata_type_value_TelemetryService}  ${Language_TelemetryService}  ${Location_TelemetryService}  ${Description_TelemetryService}  ${Id_TelemetryService}  ${Languages_odatacount_TelemetryService}  ${Location_odatacount_TelemetryService}  ${Name_TelemetryService}  ${Schema_TelemetryService}

CONSR-OBMC-RDFT-0264-0001
    [Documentation]  This test checks Redfish JSON Schema file-105 ThermalMetrics
    [Tags]   CONSR-OBMC-RDFT-0264-0001  Artemis_U2
    [Timeout]  5 min 00 seconds
    Step  1   Verify JSON Schema  ${resource_JSONSchema_ThermalMetrics}  ${odata_type_value_ThermalMetrics}  ${Language_ThermalMetrics}  ${Location_ThermalMetrics}  ${Description_ThermalMetrics}  ${Id_ThermalMetrics}  ${Languages_odatacount_ThermalMetrics}  ${Location_odatacount_ThermalMetrics}  ${Name_ThermalMetrics}  ${Schema_ThermalMetrics}

CONSR-OBMC-RDFT-0266-0001
    [Documentation]  This test checks Redfish JSON Schema file-107 Triggers
    [Tags]   CONSR-OBMC-RDFT-0266-0001  Artemis_U2
    [Timeout]  5 min 00 seconds
    Step  1   Verify JSON Schema  ${resource_JSONSchema_Triggers}  ${odata_type_value_Triggers}  ${Language_Triggers}  ${Location_Triggers}  ${Description_Triggers}  ${Id_Triggers}  ${Languages_odatacount_Triggers}  ${Location_odatacount_Triggers}  ${Name_Triggers}  ${Schema_Triggers}

CONSR-OBMC-RDFT-0268-0001
    [Documentation]  This test checks Redfish JSON Schema file-109 UpdateService
    [Tags]   CONSR-OBMC-RDFT-0268-0001  Artemis_U2
    [Timeout]  5 min 00 seconds
    Step  1   Verify JSON Schema  ${resource_JSONSchema_UpdateService}  ${odata_type_value_UpdateService}  ${Language_UpdateService}  ${Location_UpdateService}  ${Description_UpdateService}  ${Id_UpdateService}  ${Languages_odatacount_UpdateService}  ${Location_odatacount_UpdateService}  ${Name_UpdateService}  ${Schema_UpdateService}

CONSR-OBMC-RDFT-0270-0001
    [Documentation]  This test checks Redfish JSON Schema file-111 VirtualMediaCollection
    [Tags]   CONSR-OBMC-RDFT-0270-0001  Artemis_U2
    [Timeout]  5 min 00 seconds
    Step  1   Verify JSON Schema  ${resource_JSONSchema_VirtualMediaCollection}  ${odata_type_value_VirtualMediaCollection}  ${Language_VirtualMediaCollection}  ${Location_VirtualMediaCollection}  ${Description_VirtualMediaCollection}  ${Id_VirtualMediaCollection}  ${Languages_odatacount_VirtualMediaCollection}  ${Location_odatacount_VirtualMediaCollection}  ${Name_VirtualMediaCollection}  ${Schema_VirtualMediaCollection}

CONSR-OBMC-RDFT-0159-0001
    [Documentation]  This test checks JSON Schema file collection
    [Tags]   CONSR-OBMC-RDFT-0159-0001  Artemis_U2
    [Timeout]  5 min 00 seconds
    Step  1   Verify resource details   ${resource_JSONSchema_FileCollection}  ${data_type_FileCollection}   ${Description_FileCollection}  ${Members_odata_count_FileCollection}  ${Name_FileCollection}

CONSR-OBMC-RDFT-0161-0001
    [Documentation]  This test checks Redfish JSON Schema file-2 ActionInfo
    [Tags]   CONSR-OBMC-RDFT-0161-0001  Artemis_U2
    [Timeout]  5 min 00 seconds
    Step  1   Verify JSON Schema  ${resource_JSONSchema_ActionInfo}  ${odata_type_ActionInfo}  ${Languages_ActionInfo}  ${Location_ActionInfo}  ${Description_ActionInfo}  ${Id_ActionInfo}  ${Languages_odata_count_ActionInfo}  ${Location_odata_count_ActionInfo}  ${Name_ActionInfo}  ${Schema_ActionInfo}

CONSR-OBMC-RDFT-0163-0001
    [Documentation]  This test checks Redfish JSON Schema file-4 AggregationSource
    [Tags]   CONSR-OBMC-RDFT-0163-0001  Artemis_U2
    [Timeout]  5 min 00 seconds
    Step  1   Verify JSON Schema  ${resource_JSONSchema_AggregationSource}  ${odata_type_AggregationSource}  ${Languages_AggregationSource}  ${Location_AggregationSource}  ${Description_AggregationSource}  ${Id_AggregationSource}  ${Languages_odata_count_AggregationSource}  ${Location_odata_count_AggregationSource}  ${Name_AggregationSource}  ${Schema_AggregationSource}

CONSR-OBMC-RDFT-0165-0001
    [Documentation]  This test checks Redfish JSON Schema file-6 Assembly
    [Tags]   CONSR-OBMC-RDFT-0165-0001  Artemis_U2
    [Timeout]  5 min 00 seconds
    Step  1   Verify JSON Schema  ${resource_JSONSchema_Assembly}  ${odata_type_Assembly}  ${Languages_Assembly}  ${Location_Assembly}  ${Description_Assembly}  ${Id_Assembly}  ${Languages_odata_count_Assembly}  ${Location_odata_count_Assembly}  ${Name_Assembly}  ${Schema_Assembly}

CONSR-OBMC-RDFT-0167-0001
    [Documentation]  This test checks Redfish JSON Schema file-8 Bios
    [Tags]   CONSR-OBMC-RDFT-0167-0001  Artemis_U2
    [Timeout]  5 min 00 seconds
    Step  1   Verify JSON Schema  ${resource_JSONSchema_Bios}  ${odata_type_Bios}  ${Languages_Bios}  ${Location_Bios}  ${Description_Bios}  ${Id_Bios}  ${Languages_odata_count_Bios}  ${Location_odata_count_Bios}  ${Name_Bios}  ${Schema_Bios}

CONSR-OBMC-RDFT-0169-0001
    [Documentation]  This test checks Redfish JSON Schema file-10 CableCollection
    [Tags]   CONSR-OBMC-RDFT-0169-0001  Artemis_U2
    [Timeout]  5 min 00 seconds
    Step  1   Verify JSON Schema  ${resource_JSONSchema_CableCollection}  ${odata_type_CableCollection}  ${Languages_CableCollection}  ${Location_CableCollection}  ${Description_CableCollection}  ${Id_CableCollection}  ${Languages_odata_count_CableCollection}  ${Location_odata_count_CableCollection}  ${Name_CableCollection}  ${Schema_CableCollection}

CONSR-OBMC-RDFT-0171-0001
    [Documentation]  This test checks Redfish JSON Schema file-12 CertificateCollection
    [Tags]   CONSR-OBMC-RDFT-0171-0001  Artemis_U2
    [Timeout]  5 min 00 seconds
    Step  1   Verify JSON Schema  ${resource_JSONSchema_CertificateCollection}  ${odata_type_CertificateCollection}  ${Languages_CertificateCollection}  ${Location_CertificateCollection}  ${Description_CertificateCollection}  ${Id_CertificateCollection}  ${Languages_odata_count_CertificateCollection}  ${Location_odata_count_CertificateCollection}  ${Name_CertificateCollection}  ${Schema_CertificateCollection}

CONSR-OBMC-RDFT-0173-0001
    [Documentation]  This test checks Redfish JSON Schema file-14 CertificateService
    [Tags]   CONSR-OBMC-RDFT-0173-0001  Artemis_U2
    [Timeout]  5 min 00 seconds
    Step  1   Verify JSON Schema  ${resource_JSONSchema_CertificateService}  ${odata_type_CertificateService}  ${Languages_CertificateService}  ${Location_CertificateService}  ${Description_CertificateService}  ${Id_CertificateService}  ${Languages_odata_count_CertificateService}  ${Location_odata_count_CertificateService}  ${Name_CertificateService}  ${Schema_CertificateService}

CONSR-OBMC-RDFT-0175-0001
    [Documentation]  This test checks Redfish JSON Schema file-16 ChassisCollection
    [Tags]   CONSR-OBMC-RDFT-0175-0001  Artemis_U2
    [Timeout]  5 min 00 seconds
    Step  1   Verify JSON Schema  ${resource_JSONSchema_ChassisCollection}  ${odata_type_ChassisCollection}  ${Languages_ChassisCollection}  ${Location_ChassisCollection}  ${Description_ChassisCollection}  ${Id_ChassisCollection}  ${Languages_odata_count_ChassisCollection}  ${Location_odata_count_ChassisCollection}  ${Name_ChassisCollection}  ${Schema_ChassisCollection}

CONSR-OBMC-RDFT-0177-0001
    [Documentation]  This test checks Redfish JSON Schema file-18 ComponentIntegrityCollection
    [Tags]   CONSR-OBMC-RDFT-0177-0001  Artemis_U2
    [Timeout]  5 min 00 seconds
    Step  1   Verify JSON Schema  ${resource_JSONSchema_ComponentIntegrityCollection}  ${odata_type_ComponentIntegrityCollection}  ${Languages_ComponentIntegrityCollection}  ${Location_ComponentIntegrityCollection}  ${Description_ComponentIntegrityCollection}  ${Id_ComponentIntegrityCollection}  ${Languages_odata_count_ComponentIntegrityCollection}  ${Location_odata_count_ComponentIntegrityCollection}  ${Name_ComponentIntegrityCollection}  ${Schema_ComponentIntegrityCollection}

CONSR-OBMC-RDFT-0179-0001
    [Documentation]  This test checks Redfish JSON Schema file-20 ComputerSystemCollection
    [Tags]   CONSR-OBMC-RDFT-0179-0001  Artemis_U2
    [Timeout]  5 min 00 seconds
    Step  1   Verify JSON Schema  ${resource_JSONSchema_ComputerSystemCollection}  ${odata_type_ComputerSystemCollection}  ${Languages_ComputerSystemCollection}  ${Location_ComputerSystemCollection}  ${Description_ComputerSystemCollection}  ${Id_ComputerSystemCollection}  ${Languages_odata_count_ComputerSystemCollection}  ${Location_odata_count_ComputerSystemCollection}  ${Name_ComputerSystemCollection}  ${Schema_ComputerSystemCollection}

CONSR-OBMC-RDFT-0181-0001
    [Documentation]  This test checks Redfish JSON Schema file-22 DriveCollection
    [Tags]   CONSR-OBMC-RDFT-0181-0001  Artemis_U2
    [Timeout]  5 min 00 seconds
    Step  1   Verify JSON Schema  ${resource_JSONSchema_DriveCollection}  ${odata_type_DriveCollection}  ${Languages_DriveCollection}  ${Location_DriveCollection}  ${Description_DriveCollection}  ${Id_DriveCollection}  ${Languages_odata_count_DriveCollection}  ${Location_odata_count_DriveCollection}  ${Name_DriveCollection}  ${Schema_DriveCollection}

CONSR-OBMC-RDFT-0183-0001
    [Documentation]  This test checks Redfish JSON Schema file-24 EthernetInterface
    [Tags]   CONSR-OBMC-RDFT-0183-0001  Artemis_U2
    [Timeout]  5 min 00 seconds
    Step  1   Verify JSON Schema  ${resource_JSONSchema_EthernetInterface}  ${odata_type_EthernetInterface}  ${Languages_EthernetInterface}  ${Location_EthernetInterface}  ${Description_EthernetInterface}  ${Id_EthernetInterface}  ${Languages_odata_count_EthernetInterface}  ${Location_odata_count_EthernetInterface}  ${Name_EthernetInterface}  ${Schema_EthernetInterface}

CONSR-OBMC-RDFT-0185-0001
    [Documentation]  This test checks Redfish JSON Schema file-26 Event
    [Tags]   CONSR-OBMC-RDFT-0185-0001  Artemis_U2
    [Timeout]  5 min 00 seconds
    Step  1   Verify JSON Schema  ${resource_JSONSchema_Event}  ${odata_type_Event}  ${Languages_Event}  ${Location_Event}  ${Description_Event}  ${Id_Event}  ${Languages_odata_count_Event}  ${Location_odata_count_Event}  ${Name_Event}  ${Schema_Event}

CONSR-OBMC-RDFT-0187-0001
    [Documentation]  This test checks Redfish JSON Schema file-28 EventDestinationCollection
    [Tags]   CONSR-OBMC-RDFT-0187-0001  Artemis_U2
    [Timeout]  5 min 00 seconds
    Step  1   Verify JSON Schema  ${resource_JSONSchema_EventDestinationCollection}  ${odata_type_EventDestinationCollection}  ${Languages_EventDestinationCollection}  ${Location_EventDestinationCollection}  ${Description_EventDestinationCollection}  ${Id_EventDestinationCollection}  ${Languages_odata_count_EventDestinationCollection}  ${Location_odata_count_EventDestinationCollection}  ${Name_EventDestinationCollection}  ${Schema_EventDestinationCollection}

CONSR-OBMC-RDFT-0189-0001
    [Documentation]  This test checks Redfish JSON Schema file-30 FabricAdapter
    [Tags]   CONSR-OBMC-RDFT-0189-0001  Artemis_U2
    [Timeout]  5 min 00 seconds
    Step  1   Verify JSON Schema  ${resource_JSONSchema_FabricAdapter}  ${odata_type_FabricAdapter}  ${Languages_FabricAdapter}  ${Location_FabricAdapter}  ${Description_FabricAdapter}  ${Id_FabricAdapter}  ${Languages_odata_count_FabricAdapter}  ${Location_odata_count_FabricAdapter}  ${Name_FabricAdapter}  ${Schema_FabricAdapter}

CONSR-OBMC-RDFT-0191-0001
    [Documentation]  This test checks Redfish JSON Schema file-32 Fan
    [Tags]   CONSR-OBMC-RDFT-0191-0001  Artemis_U2
    [Timeout]  5 min 00 seconds
    Step  1   Verify JSON Schema  ${resource_JSONSchema_Fan}  ${odata_type_Fan}  ${Languages_Fan}  ${Location_Fan}  ${Description_Fan}  ${Id_Fan}  ${Languages_odata_count_Fan}  ${Location_odata_count_Fan}  ${Name_Fan}  ${Schema_Fan}

CONSR-OBMC-RDFT-0193-0001
    [Documentation]  This test checks Redfish JSON Schema file-34 IPAddresses
    [Tags]   CONSR-OBMC-RDFT-0193-0001  Artemis_U2
    [Timeout]  5 min 00 seconds
    Step  1   Verify JSON Schema  ${resource_JSONSchema_IPAddresses}  ${odata_type_IPAddresses}  ${Languages_IPAddresses}  ${Location_IPAddresses}  ${Description_IPAddresses}  ${Id_IPAddresses}  ${Languages_odata_count_IPAddresses}  ${Location_odata_count_IPAddresses}  ${Name_IPAddresses}  ${Schema_IPAddresses}

CONSR-OBMC-RDFT-0195-0001
    [Documentation]  This test checks Redfish JSON Schema file-36 JsonSchemaFileCollection
    [Tags]   CONSR-OBMC-RDFT-0195-0001  Artemis_U2
    [Timeout]  5 min 00 seconds
    Step  1   Verify JSON Schema  ${resource_JSONSchema_JsonSchemaFileCollection}  ${odata_type_JsonSchemaFileCollection}  ${Languages_JsonSchemaFileCollection}  ${Location_JsonSchemaFileCollection}  ${Description_JsonSchemaFileCollection}  ${Id_JsonSchemaFileCollection}  ${Languages_odata_count_JsonSchemaFileCollection}  ${Location_odata_count_JsonSchemaFileCollection}  ${Name_JsonSchemaFileCollection}  ${Schema_JsonSchemaFileCollection}

CONSR-OBMC-RDFT-0197-0001
    [Documentation]  This test checks Redfish JSON Schema file-38 LogEntryCollection
    [Tags]   CONSR-OBMC-RDFT-0197-0001  Artemis_U2
    [Timeout]  5 min 00 seconds
    Step  1   Verify JSON Schema  ${resource_JSONSchema_LogEntryCollection}  ${odata_type_LogEntryCollection}  ${Languages_LogEntryCollection}  ${Location_LogEntryCollection}  ${Description_LogEntryCollection}  ${Id_LogEntryCollection}  ${Languages_odata_count_LogEntryCollection}  ${Location_odata_count_LogEntryCollection}  ${Name_LogEntryCollection}  ${Schema_LogEntryCollection}

CONSR-OBMC-RDFT-0199-0001
    [Documentation]  This test checks Redfish JSON Schema file-40 LogServiceCollection
    [Tags]   CONSR-OBMC-RDFT-0199-0001  Artemis_U2
    [Timeout]  5 min 00 seconds
    Step  1   Verify JSON Schema  ${resource_JSONSchema_LogServiceCollection}  ${odata_type_LogServiceCollection}  ${Languages_LogServiceCollection}  ${Location_LogServiceCollection}  ${Description_LogServiceCollection}  ${Id_LogServiceCollection}  ${Languages_odata_count_LogServiceCollection}  ${Location_odata_count_LogServiceCollection}  ${Name_LogServiceCollection}  ${Schema_LogServiceCollection}

CONSR-OBMC-RDFT-0201-0001
    [Documentation]  This test checks Redfish JSON Schema file-42 ManagerAccount
    [Tags]   CONSR-OBMC-RDFT-0201-0001  Artemis_U2
    [Timeout]  5 min 00 seconds
    Step  1   Verify JSON Schema  ${resource_JSONSchema_ManagerAccount}  ${odata_type_ManagerAccount_201}  ${Languages_ManagerAccount_201}  ${Location_ManagerAccount_201}   ${Description_ManagerAccount_201}  ${Id_ManagerAccount_201}  ${Languages_odata_count_ManagerAccount_201}  ${Location_odata_count_ManagerAccount_201}  ${Name_ManagerAccount_201}  ${Schema_ManagerAccount_201}

CONSR-OBMC-RDFT-0203-0001
    [Documentation]  This test checks Redfish JSON Schema file-44 ManagerCollection
    [Tags]   CONSR-OBMC-RDFT-0203-0001  Artemis_U2
    [Timeout]  5 min 00 seconds
    Step  1   Verify JSON Schema  ${resource_JSONSchema_ManagerCollection}  ${odata_type_ManagerCollection}  ${Languages_ManagerCollection}  ${Location_ManagerCollection}  ${Description_ManagerCollection}  ${Id_ManagerCollection}  ${Languages_odata_count_ManagerCollection}  ${Location_odata_count_ManagerCollection}  ${Name_ManagerCollection}  ${Schema_ManagerCollection}

CONSR-OBMC-RDFT-0205-0001
    [Documentation]  This test checks Redfish JSON Schema file-46 ManagerNetworkProtocol
    [Tags]   CONSR-OBMC-RDFT-0205-0001  Artemis_U2
    [Timeout]  5 min 00 seconds
    Step  1   Verify JSON Schema  ${resource_JSONSchema_ManagerNetworkProtocol}  ${odata_type_ManagerNetworkProtocol}  ${Languages_ManagerNetworkProtocol}  ${Location_ManagerNetworkProtocol}  ${Description_ManagerNetworkProtocol}  ${Id_ManagerNetworkProtocol}  ${Languages_odata_count_ManagerNetworkProtocol}  ${Location_odata_count_ManagerNetworkProtocol}  ${Name_ManagerNetworkProtocol}  ${Schema_ManagerNetworkProtocol}

CONSR-OBMC-RDFT-0207-0001
    [Documentation]  This test checks Redfish JSON Schema file-48 MemoryCollection
    [Tags]   CONSR-OBMC-RDFT-0207-0001  Artemis_U2
    [Timeout]  5 min 00 seconds
    Step  1   Verify JSON Schema  ${resource_JSONSchema_MemoryCollection}  ${odata_type_MemoryCollection}  ${Languages_MemoryCollection}  ${Location_MemoryCollection}  ${Description_MemoryCollection}  ${Id_MemoryCollection}  ${Languages_odata_count_MemoryCollection}  ${Location_odata_count_MemoryCollection}  ${Name_MemoryCollection}  ${Schema_MemoryCollection}

CONSR-OBMC-RDFT-0209-0001
    [Documentation]  This test checks Redfish JSON Schema file-50 MessageRegistry
    [Tags]   CONSR-OBMC-RDFT-0209-0001  Artemis_U2
    [Timeout]  5 min 00 seconds
    Step  1   Verify JSON Schema  ${resource_JSONSchema_MessageRegistry}  ${odata_type_MessageRegistry}  ${Languages_MessageRegistry}  ${Location_MessageRegistry}  ${Description_MessageRegistry}  ${Id_MessageRegistry}  ${Languages_odata_count_MessageRegistry}  ${Location_odata_count_MessageRegistry}  ${Name_MessageRegistry}  ${Schema_MessageRegistry}

CONSR-OBMC-RDFT-0211-0001
    [Documentation]  This test checks Redfish JSON Schema file-52 MessageRegistryFile
    [Tags]   CONSR-OBMC-RDFT-0211-0001  Artemis_U2
    [Timeout]  5 min 00 seconds
    Step  1   Verify JSON Schema  ${resource_JSONSchema_MessageRegistryFile}  ${odata_type_MessageRegistryFile}  ${Languages_MessageRegistryFile}  ${Location_MessageRegistryFile}  ${Description_MessageRegistryFile}  ${Id_MessageRegistryFile}  ${Languages_odata_count_MessageRegistryFile}  ${Location_odata_count_MessageRegistryFile}  ${Name_MessageRegistryFile}  ${Schema_MessageRegistryFile}

CONSR-OBMC-RDFT-0213-0001
    [Documentation]  This test checks Redfish JSON Schema file-54 MetricDefinition
    [Tags]   CONSR-OBMC-RDFT-0213-0001  Artemis_U2
    [Timeout]  5 min 00 seconds
    Step  1   Verify JSON Schema  ${resource_JSONSchema_MetricDefinition}  ${odata_type_MetricDefinition}  ${Languages_MetricDefinition}  ${Location_MetricDefinition}  ${Description_MetricDefinition}  ${Id_MetricDefinition}  ${Languages_odata_count_MetricDefinition}  ${Location_odata_count_MetricDefinition}  ${Name_MetricDefinition}  ${Schema_MetricDefinition}

CONSR-OBMC-RDFT-0215-0001
    [Documentation]  This test checks Redfish JSON Schema file-56 MetricReport
    [Tags]   CONSR-OBMC-RDFT-0215-0001  Artemis_U2
    [Timeout]  5 min 00 seconds
    Step  1   Verify JSON Schema  ${resource_JSONSchema_MetricReport}  ${odata_type_MetricReport}  ${Languages_MetricReport}  ${Location_MetricReport}  ${Description_MetricReport}  ${Id_MetricReport}  ${Languages_odata_count_MetricReport}  ${Location_odata_count_MetricReport}  ${Name_MetricReport}  ${Schema_MetricReport}

CONSR-OBMC-RDFT-0217-0001
    [Documentation]  This test checks Redfish JSON Schema file-58 MetricReportDefinition
    [Tags]   CONSR-OBMC-RDFT-0217-0001  Artemis_U2
    [Timeout]  5 min 00 seconds
    Step  1   Verify JSON Schema  ${resource_JSONSchema_MetricReportDefinition}  ${odata_type_MetricReportDefinition}  ${Languages_MetricReportDefinition}  ${Location_MetricReportDefinition}  ${Description_MetricReportDefinition}  ${Id_MetricReportDefinition}  ${Languages_odata_count_MetricReportDefinition}  ${Location_odata_count_MetricReportDefinition}  ${Name_MetricReportDefinition}  ${Schema_MetricReportDefinition}

CONSR-OBMC-RDFT-0219-0001
    [Documentation]  This test checks Redfish JSON Schema file-60 odata
    [Tags]   CONSR-OBMC-RDFT-0219-0001  Artemis_U2
    [Timeout]  5 min 00 seconds
    Step  1   Verify JSON Schema  ${resource_JSONSchema_odata}  ${odata_type_odata}  ${Languages_odata}  ${Location_odata}  ${Description_odata}  ${Id_odata}  ${Languages_odata_count_odata}  ${Location_odata_count_odata}  ${Name_odata}  ${Schema_odata}

CONSR-OBMC-RDFT-0221-0001
    [Documentation]  This test checks Redfish JSON Schema file-62 OperatingConfig
    [Tags]   CONSR-OBMC-RDFT-0221-0001  Artemis_U2
    [Timeout]  5 min 00 seconds
    Step  1   Verify JSON Schema  ${resource_JSONSchema_OperatingConfig}  ${OperatingConfig_type_OperatingConfig}  ${Languages_OperatingConfig}  ${Location_OperatingConfig}  ${Description_OperatingConfig}  ${Id_OperatingConfig}  ${Languages_OperatingConfig_count_OperatingConfig}  ${Location_OperatingConfig_count_OperatingConfig}  ${Name_OperatingConfig}  ${Schema_OperatingConfig}

CONSR-OBMC-RDFT-0223-0001
    [Documentation]  This test checks Redfish JSON Schema file-64 PCIeDevice
    [Tags]   CONSR-OBMC-RDFT-0223-0001  Artemis_U2
    [Timeout]  5 min 00 seconds
    Step  1   Verify JSON Schema  ${resource_JSONSchema_PCIeDevice}  ${PCIeDevice_type_PCIeDevice}  ${Languages_PCIeDevice}  ${Location_PCIeDevice}  ${Description_PCIeDevice}  ${Id_PCIeDevice}  ${Languages_PCIeDevice_count_PCIeDevice}  ${Location_PCIeDevice_count_PCIeDevice}  ${Name_PCIeDevice}  ${Schema_PCIeDevice}

CONSR-OBMC-RDFT-0225-0001
    [Documentation]  This test checks Redfish JSON Schema file-66 PCIeFunction
    [Tags]   CONSR-OBMC-RDFT-0225-0001  Artemis_U2
    [Timeout]  5 min 00 seconds
    Step  1   Verify JSON Schema  ${resource_JSONSchema_PCIeFunction}  ${PCIeFunction_type_PCIeFunction}  ${Languages_PCIeFunction}  ${Location_PCIeFunction}  ${Description_PCIeFunction}  ${Id_PCIeFunction}  ${Languages_PCIeFunction_count_PCIeFunction}  ${Location_PCIeFunction_count_PCIeFunction}  ${Name_PCIeFunction}  ${Schema_PCIeFunction}

CONSR-OBMC-RDFT-0227-0001
    [Documentation]  This test checks Redfish JSON Schema file-68 PCIeSlots
    [Tags]   CONSR-OBMC-RDFT-0227-0001  Artemis_U2
    [Timeout]  5 min 00 seconds
    Step  1   Verify JSON Schema  ${resource_JSONSchema_PCIeSlots}  ${PCIeSlots_type_PCIeSlots}  ${Languages_PCIeSlots}  ${Location_PCIeSlots}  ${Description_PCIeSlots}  ${Id_PCIeSlots}  ${Languages_PCIeSlots_count_PCIeSlots}  ${Location_PCIeSlots_count_PCIeSlots}  ${Name_PCIeSlots}  ${Schema_PCIeSlots}

CONSR-OBMC-RDFT-0229-0001
    [Documentation]  This test checks Redfish JSON Schema file-70 Port
    [Tags]   CONSR-OBMC-RDFT-0229-0001  Artemis_U2
    [Timeout]  5 min 00 seconds
    Step  1   Verify JSON Schema  ${resource_JSONSchema_Port}  ${Port_type_Port}  ${Languages_Port}  ${Location_Port}  ${Description_Port}  ${Id_Port}  ${Languages_Port_count_Port}  ${Location_Port_count_Port}  ${Name_Port}  ${Schema_Port}

CONSR-OBMC-RDFT-0231-0001
    [Documentation]  This test checks Redfish JSON Schema file-72 Power
    [Tags]   CONSR-OBMC-RDFT-0231-0001  Artemis_U2
    [Timeout]  5 min 00 seconds
    Step  1   Verify JSON Schema  ${resource_JSONSchema_Power}  ${Power_type_Power}  ${Languages_Power}  ${Location_Power}  ${Description_Power}  ${Id_Power}  ${Languages_Power_count_Power}  ${Location_Power_count_Power}  ${Name_Power}  ${Schema_Power}

CONSR-OBMC-RDFT-0233-0001
    [Documentation]  This test checks Redfish JSON Schema file-74 PowerSupply
    [Tags]   CONSR-OBMC-RDFT-0233-0001  Artemis_U2
    [Timeout]  5 min 00 seconds
    Step  1   Verify JSON Schema  ${resource_JSONSchema_PowerSupply}  ${PowerSupply_type_PowerSupply}  ${Languages_PowerSupply}  ${Location_PowerSupply}  ${Description_PowerSupply}  ${Id_PowerSupply}  ${Languages_PowerSupply_count_PowerSupply}  ${Location_PowerSupply_count_PowerSupply}  ${Name_PowerSupply}  ${Schema_PowerSupply}

CONSR-OBMC-RDFT-0235-0001
    [Documentation]  This test checks Redfish JSON Schema file-76 Privileges
    [Tags]   CONSR-OBMC-RDFT-0235-0001  Artemis_U2
    [Timeout]  5 min 00 seconds
    Step  1   Verify JSON Schema  ${resource_JSONSchema_Privileges}  ${Privileges_type_Privileges}  ${Languages_Privileges}  ${Location_Privileges}  ${Description_Privileges}  ${Id_Privileges}  ${Languages_Privileges_count_Privileges}  ${Location_Privileges_count_Privileges}  ${Name_Privileges}  ${Schema_Privileges}

CONSR-OBMC-RDFT-0237-0001
    [Documentation]  This test checks Redfish JSON Schema file-78 ProcessorCollection
    [Tags]   CONSR-OBMC-RDFT-0237-0001  Artemis_U2
    [Timeout]  5 min 00 seconds
    Step  1   Verify JSON Schema  ${resource_JSONSchema_ProcessorCollection}  ${ProcessorCollection_type_ProcessorCollection}  ${Languages_ProcessorCollection}  ${Location_ProcessorCollection}  ${Description_ProcessorCollection}  ${Id_ProcessorCollection}  ${Languages_ProcessorCollection_count_ProcessorCollection}  ${Location_ProcessorCollection_count_ProcessorCollection}  ${Name_ProcessorCollection}  ${Schema_ProcessorCollection}

CONSR-OBMC-RDFT-0239-0001
    [Documentation]  This test checks Redfish JSON Schema file-80 redfish-payload-annotations
    [Tags]   CONSR-OBMC-RDFT-0239-0001  Artemis_U2
    [Timeout]  5 min 00 seconds
    Step  1   Verify JSON Schema  ${resource_JSONSchema_redfish_payload_annotations}  ${redfish_payload_annotations_type_redfish_payload_annotations}  ${Languages_redfish_payload_annotations}  ${Location_redfish_payload_annotations}  ${Description_redfish_payload_annotations}  ${Id_redfish_payload_annotations}  ${Languages_redfish_payload_annotations_count_redfish_payload_annotations}  ${Location_redfish_payload_annotations_count_redfish_payload_annotations}  ${Name_redfish_payload_annotations}  ${Schema_redfish_payload_annotations}

CONSR-OBMC-RDFT-0241-0001
    [Documentation]  This test checks Redfish JSON Schema file-82 redfish-schema-v1
    [Tags]   CONSR-OBMC-RDFT-0241-0001  Artemis_U2
    [Timeout]  5 min 00 seconds
    Step  1   Verify JSON Schema  ${resource_JSONSchema_redfish_schema_v1}  ${redfish_schema_v1_type_redfish_schema_v1}  ${Languages_redfish_schema_v1}  ${Location_redfish_schema_v1}  ${Description_redfish_schema_v1}  ${Id_redfish_schema_v1}  ${Languages_redfish_schema_v1_count_redfish_schema_v1}  ${Location_redfish_schema_v1_count_redfish_schema_v1}  ${Name_redfish_schema_v1}  ${Schema_redfish_schema_v1}

CONSR-OBMC-RDFT-0243-0001
    [Documentation]  This test checks Redfish JSON Schema file-84 Resource
    [Tags]   CONSR-OBMC-RDFT-0243-0001  Artemis_U2
    [Timeout]  5 min 00 seconds
    Step  1   Verify JSON Schema  ${resource_JSONSchema_Resource}  ${Resource_type_Resource}  ${Languages_Resource}  ${Location_Resource}  ${Description_Resource}  ${Id_Resource}  ${Languages_Resource_count_Resource}  ${Location_Resource_count_Resource}  ${Name_Resource}  ${Schema_Resource}

CONSR-OBMC-RDFT-0245-0001
    [Documentation]  This test checks Redfish JSON Schema file-86 RoleCollection
    [Tags]   CONSR-OBMC-RDFT-0245-0001  Artemis_U2
    [Timeout]  5 min 00 seconds
    Step  1   Verify JSON Schema  ${resource_JSONSchema_RoleCollection}  ${RoleCollection_type_RoleCollection}  ${Languages_RoleCollection}  ${Location_RoleCollection}  ${Description_RoleCollection}  ${Id_RoleCollection}  ${Languages_RoleCollection_count_RoleCollection}  ${Location_RoleCollection_count_RoleCollection}  ${Name_RoleCollection}  ${Schema_RoleCollection}

CONSR-OBMC-RDFT-0247-0001
    [Documentation]  This test checks Redfish JSON Schema file-88 SensorCollection
    [Tags]   CONSR-OBMC-RDFT-0247-0001  Artemis_U2
    [Timeout]  5 min 00 seconds
    Step  1   Verify JSON Schema  ${resource_JSONSchema_SensorCollection}  ${SensorCollection_type_SensorCollection}  ${Languages_SensorCollection}  ${Location_SensorCollection}  ${Description_SensorCollection}  ${Id_SensorCollection}  ${Languages_SensorCollection_count_SensorCollection}  ${Location_SensorCollection_count_SensorCollection}  ${Name_SensorCollection}  ${Schema_SensorCollection}

CONSR-OBMC-RDFT-0249-0001
    [Documentation]  This test checks Redfish JSON Schema file-90 Session
    [Tags]   CONSR-OBMC-RDFT-0249-0001  Artemis_U2
    [Timeout]  5 min 00 seconds
    Step  1   Verify JSON Schema  ${resource_JSONSchema_Session}  ${Session_type_Session}  ${Languages_Session}  ${Location_Session}  ${Description_Session}  ${Id_Session}  ${Languages_Session_count_Session}  ${Location_Session_count_Session}  ${Name_Session}  ${Schema_Session}

CONSR-OBMC-RDFT-0251-0001
    [Documentation]  This test checks Redfish JSON Schema file-92 SessionService
    [Tags]   CONSR-OBMC-RDFT-0251-0001  Artemis_U2
    [Timeout]  5 min 00 seconds
    Step  1   Verify JSON Schema  ${resource_JSONSchema_SessionService}  ${SessionService_type_SessionService}  ${Languages_SessionService}  ${Location_SessionService}  ${Description_SessionService}  ${Id_SessionService}  ${Languages_SessionService_count_SessionService}  ${Location_SessionService_count_SessionService}  ${Name_SessionService}  ${Schema_SessionService}

CONSR-OBMC-RDFT-0253-0001
    [Documentation]  This test checks Redfish JSON Schema file-94 SoftwareInventory
    [Tags]   CONSR-OBMC-RDFT-0253-0001  Artemis_U2
    [Timeout]  5 min 00 seconds
    Step  1   Verify JSON Schema  ${resource_JSONSchema_SoftwareInventory}  ${SoftwareInventory_type_SoftwareInventory}  ${Languages_SoftwareInventory}  ${Location_SoftwareInventory}  ${Description_SoftwareInventory}  ${Id_SoftwareInventory}  ${Languages_SoftwareInventory_count_SoftwareInventory}  ${Location_SoftwareInventory_count_SoftwareInventory}  ${Name_SoftwareInventory}  ${Schema_SoftwareInventory}

CONSR-OBMC-RDFT-0255-0001
    [Documentation]  This test checks Redfish JSON Schema file-96 Storage
    [Tags]   CONSR-OBMC-RDFT-0255-0001  Artemis_U2
    [Timeout]  5 min 00 seconds
    Step  1   Verify JSON Schema  ${resource_JSONSchema_Storage}  ${Storage_type_Storage}  ${Languages_Storage}  ${Location_Storage}  ${Description_Storage}  ${Id_Storage}  ${Languages_Storage_count_Storage}  ${Location_Storage_count_Storage}  ${Name_Storage}  ${Schema_Storage}

CONSR-OBMC-RDFT-0257-0001
    [Documentation]  This test checks Redfish JSON Schema file-98 StorageController
    [Tags]   CONSR-OBMC-RDFT-0257-0001  Artemis_U2
    [Timeout]  5 min 00 seconds
    Step  1   Verify JSON Schema  ${resource_JSONSchema_StorageController}  ${StorageController_type_StorageController}  ${Languages_StorageController}  ${Location_StorageController}  ${Description_StorageController}  ${Id_StorageController}  ${Languages_StorageController_count_StorageController}  ${Location_StorageController_count_StorageController}  ${Name_StorageController}  ${Schema_StorageController}

CONSR-OBMC-RDFT-0259-0001
    [Documentation]  This test checks Redfish JSON Schema file-100 Task
    [Tags]   CONSR-OBMC-RDFT-0259-0001  Artemis_U2
    [Timeout]  5 min 00 seconds
    Step  1   Verify JSON Schema  ${resource_JSONSchema_Task}  ${Task_type_Task}  ${Languages_Task}  ${Location_Task}  ${Description_Task}  ${Id_Task}  ${Languages_Task_count_Task}  ${Location_Task_count_Task}  ${Name_Task}  ${Schema_Task}

CONSR-OBMC-RDFT-0261-0001
    [Documentation]  This test checks Redfish JSON Schema file-102 TaskService
    [Tags]   CONSR-OBMC-RDFT-0261-0001  Artemis_U2
    [Timeout]  5 min 00 seconds
    Step  1   Verify JSON Schema  ${resource_JSONSchema_TaskService}  ${TaskService_type_TaskService}  ${Languages_TaskService}  ${Location_TaskService}  ${Description_TaskService}  ${Id_TaskService}  ${Languages_TaskService_count_TaskService}  ${Location_TaskService_count_TaskService}  ${Name_TaskService_1}  ${Schema_TaskService}

CONSR-OBMC-RDFT-0263-0001
    [Documentation]  This test checks Redfish JSON Schema file-104 Thermal
    [Tags]   CONSR-OBMC-RDFT-0263-0001  Artemis_U2
    [Timeout]  5 min 00 seconds
    Step  1   Verify JSON Schema  ${resource_JSONSchema_Thermal}  ${Thermal_type_Thermal}  ${Languages_Thermal}  ${Location_Thermal}  ${Description_Thermal}  ${Id_Thermal}  ${Languages_Thermal_count_Thermal}  ${Location_Thermal_count_Thermal}  ${Name_Thermal}  ${Schema_Thermal}

CONSR-OBMC-RDFT-0265-0001
    [Documentation]  This test checks Redfish JSON Schema file-106 ThermalSubsystem
    [Tags]   CONSR-OBMC-RDFT-0265-0001  Artemis_U2
    [Timeout]  5 min 00 seconds
    Step  1   Verify JSON Schema  ${resource_JSONSchema_ThermalSubsystem}  ${ThermalSubsystem_type_ThermalSubsystem}  ${Languages_ThermalSubsystem}  ${Location_ThermalSubsystem}  ${Description_ThermalSubsystem}  ${Id_ThermalSubsystem}  ${Languages_ThermalSubsystem_count_ThermalSubsystem}  ${Location_ThermalSubsystem_count_ThermalSubsystem}  ${Name_ThermalSubsystem}  ${Schema_ThermalSubsystem}

CONSR-OBMC-RDFT-0267-0001
    [Documentation]  This test checks Redfish JSON Schema file-108 TriggersCollection
    [Tags]   CONSR-OBMC-RDFT-0267-0001  Artemis_U2
    [Timeout]  5 min 00 seconds
    Step  1   Verify JSON Schema  ${resource_JSONSchema_TriggersCollection}  ${TriggersCollection_type_TriggersCollection}  ${Languages_TriggersCollection}  ${Location_TriggersCollection}  ${Description_TriggersCollection}  ${Id_TriggersCollection}  ${Languages_TriggersCollection_count_TriggersCollection}  ${Location_TriggersCollection_count_TriggersCollection}  ${Name_TriggersCollection}  ${Schema_TriggersCollection}

CONSR-OBMC-RDFT-0269-0001
    [Documentation]  This test checks Redfish JSON Schema file-110 VirtualMedia
    [Tags]   CONSR-OBMC-RDFT-0269-0001  Artemis_U2
    [Timeout]  5 min 00 seconds
    Step  1   Verify JSON Schema  ${resource_JSONSchema_VirtualMedia}  ${VirtualMedia_type_VirtualMedia}  ${Languages_VirtualMedia}  ${Location_VirtualMedia}  ${Description_VirtualMedia}  ${Id_VirtualMedia}  ${Languages_VirtualMedia_count_VirtualMedia}  ${Location_VirtualMedia_count_VirtualMedia}  ${Name_VirtualMedia}  ${Schema_VirtualMedia}

CONSR-OBMC-RDFT-0038-0001
    [Documentation]  This test checks Chassis Collection
    [Tags]   CONSR-OBMC-RDFT-0038-0001  Artemis_U2
    [Timeout]  5 min 00 seconds
    Step  1   Verify resource collection  ${resource_Chasssis_Collection}  ${data_type_Chasssis_Collection}  ${Members_odata_count_Chasssis_Collection}  ${Name_Chasssis_Collection}

CONSR-OBMC-RDFT-0272-0001
    [Documentation]  This test checks Session Collection-1 (sessionservices/sessions)
    [Tags]   CONSR-OBMC-RDFT-0272-0001  Artemis_U2
    [Timeout]  5 min 00 seconds
    Step  1   Verify resource collection  ${resource_sessionservice_Collection}  ${data_type_sessionservice_Collection}  ${Members_odata_count_sessionservice_Collection}  ${Name_sessionservice_Collection}

CONSR-OBMC-RDFT-0274-0001
    [Documentation]  This test checks MessageRegistryFileCollection
    [Tags]   CONSR-OBMC-RDFT-0274-0001  Artemis_U2
    [Timeout]  5 min 00 seconds
    Step  1   Verify resource details  ${resource_MessageRegistry_Collection}  ${data_type_MessageRegistry_Collection}   ${Description_MessageRegistry_Collection_1}  ${Members_odata_count_MessageRegistry_Collection}  ${Name_MessageRegistry_Collection_1}

CONSR-OBMC-RDFT-0276-0001
    [Documentation]  This test checks Message Registry File-2
    [Tags]   CONSR-OBMC-RDFT-0276-0001  Artemis_U2
    [Timeout]  5 min 00 seconds
    Step  1   verify message registry file details   ${resource_MessageRegistry_2}  ${Redfish_Copyright_MessageRegistry_2}  ${data_type_MessageRegistry_2}  ${Description_MessageRegistry_2}  ${Id_MessageRegistry_2}  ${Language_MessageRegistry_2}  ${Name_MessageRegistry_2}  ${OwningEntity_MessageRegistry_2}  ${RegistryPrefix_MessageRegistry_2}   ${RegistryVersion_MessageRegistry_2}  ${Messages_MessageRegistry_2}

CONSR-OBMC-RDFT-0278-0001
    [Documentation]  This test checks Message Registry File-4
    [Tags]   CONSR-OBMC-RDFT-0278-0001  Artemis_U2
    [Timeout]  5 min 00 seconds
    Step  1   verify message registry file details   ${resource_MessageRegistry_4}  ${Redfish_Copyright_MessageRegistry_4}  ${data_type_MessageRegistry_4}  ${Description_MessageRegistry_4}  ${Id_MessageRegistry_4}  ${Language_MessageRegistry_4}  ${Name_MessageRegistry_4}  ${OwningEntity_MessageRegistry_4}  ${RegistryPrefix_MessageRegistry_4}   ${RegistryVersion_MessageRegistry_4}  ${Messages_MessageRegistry_4}

CONSR-OBMC-RDFT-0280-0001
    [Documentation]  This test checks Message Registry File-6
    [Tags]   CONSR-OBMC-RDFT-0280-0001  Artemis_U2
    [Timeout]  5 min 00 seconds
    Step  1   verify message registry file details   ${resource_MessageRegistry_6}  ${Redfish_Copyright_MessageRegistry_6}  ${data_type_MessageRegistry_6}  ${Description_MessageRegistry_6}  ${Id_MessageRegistry_6}  ${Language_MessageRegistry_6}  ${Name_MessageRegistry_6}  ${OwningEntity_MessageRegistry_6}  ${RegistryPrefix_MessageRegistry_6}   ${RegistryVersion_MessageRegistry_6}  ${Messages_MessageRegistry_6}

CONSR-OBMC-RDFT-0282-0001
    [Documentation]  This test checks Message Registry File-8
    [Tags]   CONSR-OBMC-RDFT-0282-0001  Artemis_U2
    [Timeout]  5 min 00 seconds
    Step  1   verify message registry file details   ${resource_MessageRegistry_6}  ${Redfish_Copyright_MessageRegistry_6}  ${data_type_MessageRegistry_8}  ${Description_MessageRegistry_8}  ${Id_MessageRegistry_8}  ${Language_MessageRegistry_8}  ${Name_MessageRegistry_8}  ${OwningEntity_MessageRegistry_8}  ${RegistryPrefix_MessageRegistry_8}   ${RegistryVersion_MessageRegistry_8}  ${Messages_MessageRegistry_8}

CONSR-OBMC-RDFT-0002-0001
    [Documentation]  This test checks Cables
    [Tags]   CONSR-OBMC-RDFT-0002-0001  Artemis_U2
    [Timeout]  5 min 00 seconds
    Step  1   Verify resource details  ${resource_cables_Collection}  ${data_type_cables_Collection}   ${Description_cables_Collection}  ${Members_odata_count_cables_Collection}  ${Name_cables_Collection}

CONSR-OBMC-RDFT-0023-0001
    [Documentation]  This test checks LogServiceCollection-1
    [Tags]   CONSR-OBMC-RDFT-0023-0001  Artemis_U2
    [Timeout]  5 min 00 seconds
    Step  1   Verify resource details  ${LogServiceCollection1}  ${data_type_LogServiceCollection1}   ${Description_LogServiceCollection1}  ${Members_odata_count_LogServiceCollection1}  ${Name_LogServiceCollection1}

CONSR-OBMC-RDFT-0025-0001
    [Documentation]  This test checks Log Service-1
    [Tags]   CONSR-OBMC-RDFT-0025-0001  Artemis_U2
    [Timeout]  5 min 00 seconds
    Step  1   Verify logservice1 details  ${resource_logservice1}  ${data_type_logservice1}  ${Actions_logservice1}  ${Description_logservice1}  ${Entries_logservice1}  ${Id_logservice1}  ${Name_logservice1}  ${OverWritePolicy_logservice1}

CONSR-OBMC-RDFT-0027-0001
    [Documentation]  This test checks Log Service-3
    [Tags]   CONSR-OBMC-RDFT-0027-0001  Artemis_U2
    [Timeout]  5 min 00 seconds
    Step  1   Verify logservice3 details  ${resource_logservice3}  ${data_type_logservice3}  ${Description_logservice3}  ${Entries_logservice3}  ${Id_logservice3}  ${Name_logservice3}

CONSR-OBMC-RDFT-0004-0001
    [Documentation]  This test checks Computer System Collection-2
    [Tags]   CONSR-OBMC-RDFT-0004-0001  Artemis_U2
    [Timeout]  5 min 00 seconds
    Step  1   Verify Computer_System_Collection_2 details  ${resource_Computer_System_Collection_2}  ${data_type_Computer_System_Collection_2}   ${Actions_Computer_System_Collection_2}   ${Bios_Computer_System_Collection_2}   ${Boot_Computer_System_Collection_2}   ${Description_Computer_System_Collection_2}   ${FabricAdapters_Computer_System_Collection_2}   ${GraphicalConsole_Computer_System_Collection_2}   ${HostWatchdogTimer_Computer_System_Collection_2}   ${Id_Computer_System_Collection_2}  ${Links_Computer_System_Collection_2}   ${LogServices_Computer_System_Collection_2}   ${Memory_Computer_System_Collection_2}  ${MemorySummary_Computer_System_Collection_2}  ${Name_Computer_System_Collection_2}  ${PCIeDevices_Computer_System_Collection_2}  ${PCIeDevices_odata_count_Computer_System_Collection_2}  ${PowerRestorePolicy_Computer_System_Collection_2}  ${PowerState_Computer_System_Collection_2}   ${ProcessorSummary_Computer_System_Collection_2}  ${Processors_Computer_System_Collection_2}  ${SerialConsole_Computer_System_Collection_2}   ${Status_Computer_System_Collection_2}  ${Storage_Computer_System_Collection_2}  ${SystemType_Computer_System_Collection_2}

CONSR-OBMC-RDFT-0012-0001
    [Documentation]  This test checks Manager Collection
    [Tags]   CONSR-OBMC-RDFT-0012-0001  Artemis_U2
    [Timeout]  5 min 00 seconds
    Step  1   Verify resource collection  ${resource_Manager_Collection}  ${data_type_Manager_Collection}  ${Members_odata_count_Manager_Collection}  ${Name_Manager_Collection_1}

CONSR-OBMC-RDFT-0014-0001
    [Documentation]  This test checks Manager-2
    [Tags]   CONSR-OBMC-RDFT-0014-0001  Artemis_U2
    [Timeout]  5 min 00 seconds
    Step  1   Verify Manager_2 details  ${resource_Manager_2}  ${odata_type_Manager_2}  ${Id_Manager_2}  ${Name_Manager_2}

CONSR-OBMC-RDFT-0021-0001
    [Documentation]  This test checks NetworkProtocol-1
    [Tags]   CONSR-OBMC-RDFT-0021-0001  Artemis_U2
    [Timeout]  5 min 00 seconds
    Step  1   Verify resource details  ${resource_Networkprotocol1}  ${data_type_Networkprotocol1}   ${Description_Networkprotocol1}  ${Members_odata_count_Networkprotocol1}  ${Name_Networkprotocol1}

CONSR-OBMC-RDFT-0016-0001
    [Documentation]  This test checks Manager-4
    [Tags]   CONSR-OBMC-RDFT-0016-0001  Artemis_U2
    [Timeout]  5 min 00 seconds
    Step  1   Verify Manager_4_6 details  ${resource_Manager_4}  ${data_type_Manager_4}  ${DHCPv4_Manager_4}  ${DHCPv6_Manager_4}  ${Description_Manager_4}  ${EthernetInterfaceType_Manager_4}  ${FQDN_Manager_4}  ${HostName_Manager_4}  ${Id_Manager_4}  ${InterfaceEnabled_Manager_4}  ${LinkStatus_Manager_4}  ${MTUSize_Manager_4}  ${Name_Manager_4}  ${Status_Manager_4}

CONSR-OBMC-RDFT-0018-0001
    [Documentation]  This test checks Manager-6
    [Tags]   CONSR-OBMC-RDFT-0018-0001  Artemis_U2
    [Timeout]  5 min 00 seconds
    Step  1   Verify Manager_4_6 details  ${resource_Manager_6}  ${data_type_Manager_6}  ${DHCPv4_Manager_6}  ${DHCPv6_Manager_6}  ${Description_Manager_6}  ${EthernetInterfaceType_Manager_6}  ${FQDN_Manager_6}  ${HostName_Manager_6}  ${Id_Manager_6}  ${InterfaceEnabled_Manager_6}  ${LinkStatus_Manager_6}  ${MTUSize_Manager_6}  ${Name_Manager_6}  ${Status_Manager_6}

CONSR-OBMC-RDFT-0030-0001
    [Documentation]  This test checks Log Service-6
    [Tags]   CONSR-OBMC-RDFT-0030-0001  Artemis_U2
    [Timeout]  5 min 00 seconds
    Step  1   Verify log details   ${resource_logservice6}  ${data_type_logservice6}  ${Description_logservice6}  ${Name_logservice6}

CONSR-OBMC-RDFT-0032-0001
    [Documentation]  This test checks Log Service-8
    [Tags]   CONSR-OBMC-RDFT-0032-0001  Artemis_U2
    [Timeout]  5 min 00 seconds
    Step  1   Verify logservice8 details  ${resource_logservice8}  ${data_type_logservice8}  ${Description_logservice8}   ${Members_odata_nextLink_logservice8}  ${Name_logservice8}

CONSR-OBMC-RDFT-0009-0001
    [Documentation]  This test checks Computer System-5
    [Tags]   CONSR-OBMC-RDFT-0009-0001  Artemis_U2
    [Timeout]  5 min 00 seconds
    Step  1   verify computersystem5 details  ${resource_computersystem5}  ${data_type_computersystem5}  ${Id_computersystem5}  ${Name_computersystem5}  ${Parameters_computersystem5}

CONSR-OBMC-RDFT-0034-0001
    [Documentation]  This test checks TelemetryService
    [Tags]   CONSR-OBMC-RDFT-0034-0001  Artemis_U2
    [Timeout]  5 min 00 seconds
    Step  1   verify TelemetryService   ${resource_telemetryservice}  ${data_type_telemetryservice}  ${Id_telemetryservice}  ${MaxReports_telemetryservice}  ${MetricReportDefinitions_telemetryservice}   ${MetricReports_telemetryservice}   ${MinCollectionInterval_telemetryservice}   ${Name_telemetryservice1}  ${Status_telemetryservice}    ${SupportedCollectionFunctions_telemetryservice}  ${Triggers_telemetryservice}

CONSR-OBMC-RDFT-0039-0001
    [Documentation]  This test checks Chassis-1
    [Tags]   CONSR-OBMC-RDFT-0039-0001  Artemis_U2
    [Timeout]  5 min 00 seconds
    Step  1   verify Chassis-1 details   ${resource_chassis1}  ${data_type_chassis1}  ${Actions_chassis1}  ${ChassisType_chassis1}  ${Id_chassis1}   ${Links_chassis1}   ${Manufacturer_chassis1}   ${Name_chassis1}  ${Model_chassis1}    ${PCIeDevices_chassis1}  ${PartNumber_chassis1}   ${Power_chassis1}  ${PowerState_chassis1}  ${Sensors_chassis1}    ${SerialNumber_chassis1}  ${Status_chassis1}  ${Thermal_chassis1}

CONSR-OBMC-RDFT-0042-0001
    [Documentation]  This test checks SensorCollection
    [Tags]   CONSR-OBMC-RDFT-0042-0001  Artemis_U2
    [Timeout]  5 min 00 seconds
    Step  1   verify sensor_manageraccount collection   ${resource_sensors}  ${data_type_sensors}  ${Description_sensors}   ${Members_sensors}  ${Members_odata_count_sensors}  ${Name_sensors}

CONSR-OBMC-RDFT-0044-0001
    [Documentation]  This test checks Sensor-2
    [Tags]   CONSR-OBMC-RDFT-0044-0001  Artemis_U2
    [Timeout]  5 min 00 seconds
    Step  1   verify sensor details   ${resource_sensors_2}  ${data_type_sensors_2}  ${Id_sensors_2}  ${Name_sensors_2}  ${ReadingRangeMax_sensors_2}   ${ReadingRangeMin_sensors_2}  ${ReadingType_sensors_2}  ${ReadingUnits_sensors_2}   ${Status_sensors_2}

CONSR-OBMC-RDFT-0046-0001
    [Documentation]  This test checks Sensor-4
    [Tags]   CONSR-OBMC-RDFT-0046-0001  Artemis_U2
    [Timeout]  5 min 00 seconds
    Step  1   verify sensor details   ${resource_sensors_4}  ${data_type_sensors_4}  ${Id_sensors_4}  ${Name_sensors_4}  ${ReadingRangeMax_sensors_4}   ${ReadingRangeMin_sensors_4}  ${ReadingType_sensors_4}  ${ReadingUnits_sensors_4}   ${Status_sensors_4}

CONSR-OBMC-RDFT-0048-0001
    [Documentation]  This test checks Sensor-6
    [Tags]   CONSR-OBMC-RDFT-0048-0001  Artemis_U2
    [Timeout]  5 min 00 seconds
    Step  1   verify sensor psu details  ${resource_sensors_6}  ${data_type_sensors_6}   ${Id_sensors_6}   ${Name_sensors_6}  ${ReadingRangeMax_sensors_6}   ${ReadingRangeMin_sensors_6}   ${ReadingType_sensors_6}   ${ReadingUnits_sensors_6}   ${Status_sensors_6}  ${Thresholds_sensors_6}

CONSR-OBMC-RDFT-0050-0001
    [Documentation]  This test checks Sensor-8
    [Tags]   CONSR-OBMC-RDFT-0050-0001  Artemis_U2
    [Timeout]  5 min 00 seconds
    Step  1   verify sensor psu details  ${resource_sensors_8}  ${data_type_sensors_8}   ${Id_sensors_8}   ${Name_sensors_8}  ${ReadingRangeMax_sensors_8}   ${ReadingRangeMin_sensors_8}   ${ReadingType_sensors_8}   ${ReadingUnits_sensors_8}   ${Status_sensors_8}  ${Thresholds_sensors_8}

CONSR-OBMC-RDFT-0052-0001
    [Documentation]  This test checks Sensor-10
    [Tags]   CONSR-OBMC-RDFT-0052-0001  Artemis_U2
    [Timeout]  5 min 00 seconds
    Step  1   verify sensor psu details  ${resource_sensors_10}  ${data_type_sensors_10}   ${Id_sensors_10}   ${Name_sensors_10}  ${ReadingRangeMax_sensors_10}   ${ReadingRangeMin_sensors_10}   ${ReadingType_sensors_10}   ${ReadingUnits_sensors_10}   ${Status_sensors_10}  ${Thresholds_sensors_10}

CONSR-OBMC-RDFT-0054-0001
    [Documentation]  This test checks Sensor-12
    [Tags]   CONSR-OBMC-RDFT-0054-0001  Artemis_U2
    [Timeout]  5 min 00 seconds
    Step  1   verify sensor psu details  ${resource_sensors_12}  ${data_type_sensors_12}   ${Id_sensors_12}   ${Name_sensors_12}  ${ReadingRangeMax_sensors_12}   ${ReadingRangeMin_sensors_12}   ${ReadingType_sensors_12}   ${ReadingUnits_sensors_12}   ${Status_sensors_12}  ${Thresholds_sensors_12}

CONSR-OBMC-RDFT-0150-0001
    [Documentation]  This test checks ManagerAccount Collection-1
    [Tags]   CONSR-OBMC-RDFT-0150-0001  Artemis_U2
    [Timeout]  5 min 00 seconds
    Step  1   verify sensor_manageraccount collection   ${resource_ManagerAccount_Collection}  ${data_type_ManagerAccount_Collection}   ${Description_ManagerAccount_Collection_1}   ${Members_ManagerAccount_Collection}  ${Members_odata_count_ManagerAccount_Collection}  ${Name_ManagerAccount_Collection_1}

CONSR-OBMC-RDFT-0003-0001
    [Documentation]  This test checks Redfish Computer System Collection-1
    [Tags]   CONSR-OBMC-RDFT-0003-0001  Artemis_U2
    [Timeout]  5 min 00 seconds
    Step  1   Verify computer collection1  ${resource_Computer_Collection_1}  ${data_type_Computer_Collection_1}
              ...  ${Members_Computer_Collection_1}  ${Members_odata_count_Computer_Collection_1}  ${Name_Computer_Collection_1}

CONSR-OBMC-RDFT-0006-0001
    [Documentation]  This test checks Redfish Computer System-2
    [Tags]   CONSR-OBMC-RDFT-0006-0001  Artemis_U2
    [Timeout]  5 min 00 seconds
    Step  1   Verify computer System-2   ${resource_computer_system2}   ${data_type_computer_system2}   ${actions_computer_systems2}  ${Description_computer_system2}  ${ID_computer_system2}  ${Links_computer_system2}   ${Name_computer_system2}

CONSR-OBMC-RDFT-0015-0001
    [Documentation]  This test checks Redfish Manager-3
    [Tags]   CONSR-OBMC-RDFT-0015-0001   Artemis_U2
    [Timeout]  5 min 00 seconds
    Step  1   Verify Manager-3   ${resource_manager_3}   ${data_type_manager_3}   ${Description_manager_3}   ${Member_manager_3}   ${Members_odata_count_manager_3}    ${Name_manager_3}

CONSR-OBMC-RDFT-0271-0001
    [Documentation]  This test checks Redfish Session Collection-1
    [Tags]   CONSR-OBMC-RDFT-0271-0001   Artemis_U2
    [Timeout]  5 min 00 seconds
    Step  1   Verify Session Collection-1  ${resource_session_collection_1}   ${data_type_session_collection_1}  ${Description_session_collection_1}   ${ID_session_collection_1}   ${name_session_collection_1}    ${serviceenabled_session_collection_1}   ${sessiontimeout_session_collection_1}    ${sessions_session_collection_1}

CONSR-OBMC-RDFT-0275-0001
    [Documentation]  This test checks Redfish Message Registry File-1
    [Tags]   CONSR-OBMC-RDFT-0275-0001    Artemis_U2
    [Timeout]  5 min 00 seconds
    Step  1   Verify Message Registry File-1   ${resource_message_registry_1}    ${data_type_message_registry_1}  ${Description_message_registry_1}   ${ID_message_registry_1}  ${Languages_message_registry_1}   ${Languages_odata_count_message_registry_1}   ${Location_message_registry_1}   ${Location_odata_count_message_registry_1}  ${Name_message_registry_1}   ${Registry_message_registry_1}

CONSR-OBMC-RDFT-0277-0001
    [Documentation]  This test checks Redfish Message Registry File-3
    [Tags]   CONSR-OBMC-RDFT-0277-0001   Artemis_U2
    [Timeout]  5 min 00 seconds
    Step  1   Verify Message Registry File-1   ${resource_message_registry_3}    ${data_type_message_registry_3}  ${Description_message_registry_3}   ${ID_message_registry_3}  ${Languages_message_registry_3}   ${Languages_odata_count_message_registry_3}   ${Location_message_registry_3}   ${Location_odata_count_message_registry_3}  ${Name_message_registry_3}   ${Registry_message_registry_3}

CONSR-OBMC-RDFT-0279-0001
    [Documentation]  This test checks Redfish Message Registry File-5
    [Tags]   CONSR-OBMC-RDFT-0279-0001   Artemis_U2
    [Timeout]  5 min 00 seconds
    Step  1   Verify Message Registry File-1   ${resource_message_registry_5}    ${data_type_message_registry_5}  ${Description_message_registry_5}   ${ID_message_registry_5}  ${Languages_message_registry_5}   ${Languages_odata_count_message_registry_5}   ${Location_message_registry_5}   ${Location_odata_count_message_registry_5}  ${Name_message_registry_5}   ${Registry_message_registry_5}

CONSR-OBMC-RDFT-0281-0001
    [Documentation]  This test checks Redfish Message Registry File-7
    [Tags]   CONSR-OBMC-RDFT-0281-0001   Artemis_U2
    [Timeout]  5 min 00 seconds
    Step  1   Verify Message Registry File-1   ${resource_message_registry_7}    ${data_type_message_registry_7}  ${Description_message_registry_7}   ${ID_message_registry_7}  ${Languages_message_registry_7}   ${Languages_odata_count_message_registry_7}   ${Location_message_registry_7}   ${Location_odata_count_message_registry_7}  ${Name_message_registry_7}   ${Registry_message_registry_7}

CONSR-OBMC-RDFT-0151-0001
    [Documentation]  This test checks Redfish ManagerAccount
    [Tags]   CONSR-OBMC-RDFT-0151-0001    Artemis_U2
    [Timeout]  5 min 00 seconds
    Step  1   Verify ManagerAccount   ${resource_ManagerAccount}   ${data_type_ManagerAccount}   ${AccountTypes_ManagerAccount}  ${Description_ManagerAccount}  ${Enabled_ManagerAccount}  ${ID_MAnagerAccount}   ${Links_ManagerAccount}   ${Locked_ManagerAccount}  ${Locked_Redfish_AllowableValues_ManagerAccount}   ${Name_ManagerAccount}    ${PasswordChangeRequired_ManagerAccount}    ${RoleID_MAnagerAccount}   ${StrictAccountTypes_ManagerAccount}   ${UserName_ManagerAccount}

CONSR-OBMC-RDFT-0153-0001
    [Documentation]  This test checks Redfish Role-1
    [Tags]   CONSR-OBMC-RDFT-0153-0001   Artemis_U2
    [Timeout]  5 min 00 seconds
    Step  1   Verify Role-1  ${resource_role_1}   ${data_type_role_1}  ${AssignedPrivileges_role_1}   ${Description_role_1}  ${Id_role_1}  ${IsPredefined_role_1}   ${Name_role_1}  ${OemPrivileges_role_1}   ${RoleId_role_1}

CONSR-OBMC-RDFT-0155-0001
    [Documentation]  This test checks Redfish Role-3
    [Tags]   CONSR-OBMC-RDFT-0155-0001   Artemis_U2
    [Timeout]  5 min 00 seconds
    Step  1   Verify Role-1  ${resource_role_3}   ${data_type_role_3}  ${AssignedPrivileges_role_3}   ${Description_role_3}  ${Id_role_3}  ${IsPredefined_role_3}   ${Name_role_3}  ${OemPrivileges_role_3}   ${RoleId_role_3}

CONSR-OBMC-RDFT-0041-0001
    [Documentation]  This test checks Redfish Chassis-3
    [Tags]   CONSR-OBMC-RDFT-0041-0001   Artemis_U2
    [Timeout]  5 min 00 seconds
    Step  1   Verify Chassis-3  ${resource_chassis_3}   ${data_type_chassis_3}  ${ID_chassis_3}  ${name_chassis_3}  ${Parameters_chassis_3}

CONSR-OBMC-RDFT-0053-0001
    [Documentation]  This test checks Redfish Sensor-11
    [Tags]   CONSR-OBMC-RDFT-0053-0001   Artemis_U2
    [Timeout]  5 min 00 seconds
    Step  1   Verify Sensor-11  ${resource_sensor_11}  ${data_type_sensor_11}   ${Id_sensor_11}   ${Name_sensor_11}  ${ReadingRangeMax_sensor_11}  ${ReadingRangeMin_sensor_11}  ${ReadingType_sensor_11}   ${ReadingUnits_sensor_11}   ${Status_sensor_11}

CONSR-OBMC-RDFT-0051-0001
    [Documentation]  This test checks Redfish Sensor-9
    [Tags]   CONSR-OBMC-RDFT-0051-0001   Artemis_U2
    [Timeout]  5 min 00 seconds
    Step  1   Verify Sensor-11  ${resource_sensor_9}  ${data_type_sensor_9}   ${Id_sensor_9}   ${Name_sensor_9}  ${ReadingRangeMax_sensor_9}  ${ReadingRangeMin_sensor_9}  ${ReadingType_sensor_9}   ${ReadingUnits_sensor_9}   ${Status_sensor_9}

CONSR-OBMC-RDFT-0049-0001
    [Documentation]  This test checks Redfish Sensor-7
    [Tags]   CONSR-OBMC-RDFT-0049-0001   Artemis_U2
    [Timeout]  5 min 00 seconds
    Step  1   Verify Sensor-11  ${resource_sensor_7}  ${data_type_sensor_7}   ${Id_sensor_7}   ${Name_sensor_7}  ${ReadingRangeMax_sensor_7}  ${ReadingRangeMin_sensor_7}  ${ReadingType_sensor_7}   ${ReadingUnits_sensor_7}   ${Status_sensor_7}

CONSR-OBMC-RDFT-0047-0001
    [Documentation]  This test checks Redfish Sensor-5
    [Tags]   CONSR-OBMC-RDFT-0047-0001   Artemis_U2
    [Timeout]  5 min 00 seconds
    Step  1   Verify Sensor-11  ${resource_sensor_5}  ${data_type_sensor_5}   ${Id_sensor_5}   ${Name_sensor_5}  ${ReadingRangeMax_sensor_5}  ${ReadingRangeMin_sensor_5}  ${ReadingType_sensor_5}   ${ReadingUnits_sensor_5}   ${Status_sensor_5}

CONSR-OBMC-RDFT-0045-0001
    [Documentation]  This test checks Redfish Sensor-3
    [Tags]   CONSR-OBMC-RDFT-0045-0001   Artemis_U2
    [Timeout]  5 min 00 seconds
    Step  1   Verify Sensor-3  ${resource_sensor_3}  ${data_type_sensor_3}   ${Id_sensor_3}   ${Name_sensor_3}  ${ReadingRangeMax_sensor_3}  ${ReadingRangeMin_sensor_3}  ${ReadingType_sensor_3}   ${ReadingUnits_sensor_3}   ${Status_sensor_3}

CONSR-OBMC-RDFT-0043-0001
    [Documentation]  This test checks Redfish Sensor-1
    [Tags]   CONSR-OBMC-RDFT-0043-0001   Artemis_U2
    [Timeout]  5 min 00 seconds
    Step  1   Verify Sensor-3  ${resource_sensor_1}  ${data_type_sensor_1}   ${Id_sensor_1}   ${Name_sensor_1}  ${ReadingRangeMax_sensor_1}  ${ReadingRangeMin_sensor_1}  ${ReadingType_sensor_1}   ${ReadingUnits_sensor_1}   ${Status_sensor_1}

CONSR-OBMC-RDFT-0283-0001
    [Documentation]  This test checks Redfish UpdateService-1
    [Tags]   CONSR-OBMC-RDFT-0283-0001    Artemis_U2
    [Timeout]  5 min 00 seconds
    Step  1   Verify UpdateService-1  ${resource_UpdateService_1}   ${data_type_UpdateService_1}   ${Description_UpdateService_1}   ${FirmwareInventory_UpdateService_1}   ${HttpPushUri_UpdateService_1}  ${HttpPushUriOptions_UpdateService_1}  ${Id_UpdateService_1}  ${MaxImageSizeBytes_UpdateService_1}  ${MultipartHttpPushUri_UpdateService_1}  ${Name_UpdateService_1}  ${ServiceEnabled_UpdateService_1}

CONSR-OBMC-RDFT-0029-0001
    [Documentation]  This test checks Redfish Log Service-5
    [Tags]   CONSR-OBMC-RDFT-0029-0001    Artemis_U2
    [Timeout]  5 min 00 seconds
    Step  1   Verify Log Service-5   ${resource_Log_Service_5}  ${data_type_Log_service_5}  ${Actions_Log_service_5}  ${Description_Log_service_5}   ${Entries_Log_service_5}  ${Id_Log_service_5}   ${Name_Log_service_5}  ${OverWritePolicy_Log_service_5}

CONSR-OBMC-RDFT-0031-0001
    [Documentation]  This test checks Redfish Log Service-7
    [Tags]   CONSR-OBMC-RDFT-0031-0001   Artemis_U2
    [Timeout]  5 min 00 seconds
    Step  1   Verify Log Service-7    ${resource_log_service_7}   ${data_type_log_service_7}  ${Description_log_service_7}   ${Entries_log_services_7}   ${Id_log_services_7}   ${Name_log_service_7}  ${OverWritePolicy_log_service_7}

CONSR-OBMC-RDFT-0013-0001
    [Documentation]  This test checks Redfish Manager-1
    [Tags]   CONSR-OBMC-RDFT-0013-0001   Artemis_U2
    [Timeout]  5 min 00 seconds
    Step  1   Verify Manager-1   ${resource_manager_1}  ${data_type_manager_1}   ${Actions_Manager_1}  ${Description_Manager_1}   ${EthernetInterface_Manager_1}   ${GraphicalConsole_manager_1}   ${ID_manager_1}   ${Links_Manager_1}   ${Logservices_manager_1}   ${ManagerDiagnosticData_Manager_1}   ${ManagerType_manager_1}   ${Model_manager_1}  ${Name_manager_1}    ${NetworkProtocol_manager_1}   ${oem_manager_1}   ${Powerstate_manager_1}   ${SerialConsole_manager_1}    ${status_manager_1}

CONSR-OBMC-RDFT-0017-0001
    [Documentation]  This test checks Redfish Manager-5
    [Tags]   CONSR-OBMC-RDFT-0017-0001   Artemis_U2
    [Timeout]  5 min 00 seconds
    Step  1   Verify Manager-5  ${resource_manager_5}   ${data_type_manager_5}  ${dhcpv4_manager_5}   ${dhcpv6_manager_5}  ${Description_manager_5}   ${EthernetInterfaceType_manager_5}   ${FQDN_manager_5}  ${HostName_manager_5}   ${Id_manager_5}   ${Name_manager_5}   ${Status_manager_5}

CONSR-OBMC-RDFT-0020-0001
    [Documentation]  This test checks Redfish ManagersNetworkProtocol
    [Tags]   CONSR-OBMC-RDFT-0020-0001   Artemis_U2
    [Timeout]  5 min 00 seconds
    Step  1   Verify ManagersNetworkProtocol   ${resource_ManagersNetworkProtocol}   ${data_type_ManagersNetworkProtocol}   ${Description_ManagersNetworkProtocol}   ${FQDN_ManagersNetworkProtocol}   ${HTTP_ManagersNetworkProtocol}   ${HTTPS_ManagersNetworkProtocol}   ${Hostname_ManagersNetworkProtocol}   ${IPMI_ManagersNetworkProtocol}   ${ID_ManagersNetworkProtocol}   ${Name_ManagersNetworkProtocol}   ${SSH_ManagersNetworkProtocol}   ${Status_ManagersNetworkProtocol}

CONSR-OBMC-RDFT-0022-0001
    [Documentation]  This test checks Redfish NetworkProtocol-2
    [Tags]   CONSR-OBMC-RDFT-0022-0001   Artemis_U2
    [Timeout]  5 min 00 seconds
    Step  1   Verify NetworkProtocol-2  ${resource_NetworkProtocol_2}  ${data_type_NetworkProtocol_2}  ${Description_networkprotocol_2}  ${Id_networkprotocol_2}   ${Issuer_networkprotocol_2}   ${KeyUsage_networkprotocol_2}  ${Name_networkprotocol_2}  ${Subject_networkprotocol_2}

CONSR-OBMC-RDFT-0287-0001
    [Documentation]  This test checks Redfish CertificateService-2
    [Tags]   CONSR-OBMC-RDFT-0287-0001  Artemis_U2
    [Timeout]  5 min 00 seconds
    Step  1   Verify CertificateService-2  ${resource_CertificateService_2}   ${data_type_CertificateService_2}   ${Description_CertificateService_2}   ${ID_CertificateService_2}   ${Links_CertificateService_2}   ${Name_CertificateService_2}

CONSR-OBMC-RDFT-0148-0001
    [Documentation]  This test checks Redfish AccountService-1
    [Tags]   CONSR-OBMC-RDFT-0148-0001   Artemis_U2
    [Timeout]  5 min 00 seconds
    Step  1   Verify AccountService-1   ${resource_AccountService_1}   ${data_type_AccountService_1}   ${AccountLockoutDuration_AccountService_1}   ${AccountLockoutThreshold_AccountService_1}   ${Accounts_AccountService_1}  ${ActiveDirectory_AccountService_1}  ${Description_AccountService_1}   ${ID_AccountService_1}   ${LDAP_AccountService_1}  ${MaxPasswordLength_AccountService_1}  ${MinPasswordLength_AccountService_1}  ${Name_AccountService_1}  ${Oem_AccountService_1}  ${Roles_AccountService_1}  ${ServiceEnabled_AccountService_1}

CONSR-OBMC-RDFT-0026-0001
    [Documentation]  This test checks Redfish Log Service-2
    [Tags]   CONSR-OBMC-RDFT-0026-0001   Artemis_U2
    [Timeout]  5 min 00 seconds
    Step  1   Verify Log Service-2  ${resource_Log_service_2}   ${data_type_log_service_2}   ${Description_log_service_2}   ${Members_data_nextLink_Log_service_2}   ${Name_Log_service_2}

CONSR-OBMC-RDFT-0284-0001
    [Documentation]  This test checks UpdateService-6
    [Tags]   CONSR-OBMC-RDFT-0284-0001  Artemis_U2
    [Timeout]  5 min 00 seconds
    Step  1   Verify UpdateService_6  ${resource_UpdateService_6}  ${data_type_UpdateService_6}   ${Members_UpdateService_6}   ${Members_odata_count_UpdateService_6}  ${Name_UpdateService_6}

CONSR-OBMC-RDFT-0152-0001
    [Documentation]  This test checks Role Collection
    [Tags]   CONSR-OBMC-RDFT-0152-0001  Artemis_U2
    [Timeout]  5 min 00 seconds
    Step  1   verify sensor_manageraccount collection   ${resource_role_152}  ${data_type_role_152}  ${Description_role_collection_152}   ${Members_role_152}  ${Members_odata_count_role_152}  ${Name_role_collection_152}

CONSR-OBMC-RDFT-0288-0001
    [Documentation]  This test checks TelemetryService-1
    [Tags]   CONSR-OBMC-RDFT-0288-0001   Artemis_U2
    [Timeout]  5 min 00 seconds
    Step  1   verify telemetry service 1 details   ${resource_TelemetryService_1}   ${data_type_TelemetryService_1}   ${Id_TelemetryService_1}   ${MaxReports_TelemetryService_1}   ${MetricReportDefinitions_TelemetryService_1}   ${MetricReports_TelemetryService_1}   ${MinCollectionInterval_TelemetryService_1}   ${Name_TelemetryService_1}   ${Status_TelemetryService_1}   ${SupportedCollectionFunctions_TelemetryService_1}   ${Triggers_TelemetryService_1}

CONSR-OBMC-RDFT-0154-0001
    [Documentation]  This test checks Role-2
    [Tags]   CONSR-OBMC-RDFT-0154-0001   Artemis_U2
    [Timeout]  5 min 00 seconds
    Step  1   verify role 2 details   ${resource_role2}   ${data_type_role2}   ${AssignedPrivileges_role2}  ${Description_role2}  ${Id_role2}  ${IsPredefined_role2}   ${Name_role2}  ${OemPrivileges_role2}  ${RoleId_role2}

CONSR-OBMC-RDFT-0156-0001
    [Documentation]  This test checks TaskService
    [Tags]   CONSR-OBMC-RDFT-0156-0001   Artemis_U2
    [Timeout]  5 min 00 seconds
    Step  1   verify TaskService details   ${resource_TaskService}   ${data_type_TaskService}   ${CompletedTaskOverWritePolicy_TaskService}  ${Id_TaskService}   ${LifeCycleEventOnTaskStateChange_TaskService}   ${Name_TaskService}   ${ServiceEnabled_TaskService}   ${Status_TaskService}  ${Tasks_TaskService}

CONSR-OBMC-RDFT-0080-0001
    [Documentation]  This test checks Thermal-1
    [Tags]   CONSR-OBMC-RDFT-0080-0001   Artemis_U2
    Step  1   verify thermal_1 details  ${resource_thermal1}   ${data_type_thermal1}   ${Id_thermal1}  ${Name_thermal1}   ${Redundancy_thermal1}

CONSR-OBMC-RDFT-0055-0001
    [Documentation]  This test checks Redfish PowerCollection
    [Tags]   CONSR-OBMC-RDFT-0055-0001   Artemis_U2
    [Timeout]  5 min 00 seconds
    Step  1   Verify PowerCollection   ${resource_PowerCollection}  ${data_type_PowerCollection}   ${ID_PowerCollection}   ${Name_PowerCollection}

CONSR-OBMC-RDFT-0285-0001
    [Documentation]  This test checks Redfish UpdateService-7
    [Tags]   CONSR-OBMC-RDFT-0285-0001   Artemis_U2
    [Timeout]  100 min 00 seconds
    Step  1   Verify openbmc system bios   ${resource_updateservice_7}   ${data_type_updateservice_7}   ${Description_updateservice_7}   ${ID_updateservice_7}   ${Name_updateservice_7}   ${RelatedItem_updateservice_7}    ${RelatedItem_odata_count_updateservice_7}  ${status_updateservice_7}  ${Updateable_updateservice_7}   ${Version_updateservice_7_before}
    Step  2   Verify openbmc system cpld   ${cpld_resource_updateservice_7}   ${cpld_data_type_updateservice_7}   ${cpld_Description_updateservice_7}   ${cpld_ID_updateservice_7}  ${cpld_Name_updateservice_7}   ${cpld_Status_updateservice_7}   ${cpld_Updateable_updateservice_7}   ${cpld_Version_updateservice_7_before}
    Step  3   Verify openbmc upgrade bios  ${resource_redfish_updateservice_update}   ${filename_redfish_bios_upgrade}
    Step  4   Verify openbmc upgrade cpld  ${resource_redfish_updateservice_update}   ${filename_redfish_cpld_upgrade}
    Step  5   Verify openbmc system bios   ${resource_updateservice_7}   ${data_type_updateservice_7}   ${Description_updateservice_7}   ${ID_updateservice_7}   ${Name_updateservice_7}   ${RelatedItem_updateservice_7}    ${RelatedItem_odata_count_updateservice_7}  ${status_updateservice_7}  ${Updateable_updateservice_7}   ${Version_updateservice_7_after}
    Step  6   Verify openbmc system cpld   ${cpld_resource_updateservice_7}   ${cpld_data_type_updateservice_7}   ${cpld_Description_updateservice_7}   ${cpld_ID_updateservice_7}  ${cpld_Name_updateservice_7}   ${cpld_Status_updateservice_7}   ${cpld_Updateable_updateservice_7}   ${cpld_Version_updateservice_7_after}

CONSR-BMC-OEMCMD-0001-0001
    [Documentation]  This test checks IPMI OEM command: "get multi-node info"
    [Tags]     CONSR-OBMC-BSFC-0032-0001  CONSR-BMC-OEMCMD-0001-0001  Artemis
    [Timeout]  10 min 00 seconds
    Sub-Case  CONSR-BMC-OEMCMD-0001-0001_1  run ipmi command "get multi-node info"

CONSR-BMC-OEMCMD-0002-0001
    [Documentation]  This test checks IPMI OEM command: "get and set GPIO State "
    [Tags]     CONSR-OBMC-BSFC-0032-0001  CONSR-BMC-OEMCMD-0002-0001  Artemis
    [Timeout]  10 min 00 seconds
    Sub-Case  CONSR-BMC-OEMCMD-0002-0001_1  run ipmi command "set_get GPIO State"

CONSR-BMC-OEMCMD-0003-0001
    [Documentation]  This test checks IPMI OEM command: "Set-Get Access CPLD registers"
    [Tags]     CONSR-OBMC-BSFC-0032-0001  CONSR-BMC-OEMCMD-0003-0001  Artemis
    [Timeout]  10 min 00 seconds
    Sub-Case  CONSR-BMC-OEMCMD-0003-0001_1  run ipmi command "Set Access CPLD registers"
    Sub-Case  CONSR-BMC-OEMCMD-0003-0001_2  run ipmi command "Get Access CPLD registers"

CONSR-BMC-OEMCMD-0004-0001
    [Documentation]  This test checks IPMI OEM command: "Set LED state "
    [Tags]     CONSR-OBMC-BSFC-0032-0001  CONSR-BMC-OEMCMD-0004-0001  Artemis
    [Timeout]  10 min 00 seconds
    Sub-Case  CONSR-BMC-OEMCMD-0004-0001_1  run ipmi command "Set Get LED state offset_30"
    Sub-Case  CONSR-BMC-OEMCMD-0004-0001_2  run ipmi command "Set Get LED state offset_31"
    Sub-Case  CONSR-BMC-OEMCMD-0004-0001_3  run ipmi command "Set Get LED state offset_32"
    Sub-Case  CONSR-BMC-OEMCMD-0004-0001_4  run ipmi command "Set Get LED state offset_33"
    Sub-Case  CONSR-BMC-OEMCMD-0004-0001_5  run ipmi command "Set Get LED state offset_34"
    Sub-Case  CONSR-BMC-OEMCMD-0004-0001_6  run ipmi command "Set Get LED state offset_35"
    Sub-Case  CONSR-BMC-OEMCMD-0004-0001_7  run ipmi command "Set Get LED state offset_36"
    Sub-Case  CONSR-BMC-OEMCMD-0004-0001_8  run ipmi command "Set Get LED state offset_37"

CONSR-BMC-OEMCMD-0005-0001
    [Documentation]  This test checks IPMI OEM command: "Set SSD Power State"
    [Tags]     CONSR-OBMC-BSFC-0032-0001  CONSR-BMC-OEMCMD-0005-0001  Artemis
    [Timeout]  10 min 00 seconds
    Sub-Case  CONSR-BMC-OEMCMD-0005-0001_1  run ipmi command "Set SSD Power State"

CONSR-BMC-OEMCMD-0006-0001
#TODO:
    [Documentation]  This test checks IPMI OEM command: "Get-Set BIOS Flash Switch Position"
    [Tags]     CONSR-OBMC-BSFC-0032-0001  CONSR-BMC-OEMCMD-0006-0001  Artemis
    [Timeout]  10 min 00 seconds
    Sub-Case  CONSR-BMC-OEMCMD-0006-0001_1  run ipmi command "Get-Set BIOS Flash Switch Position to Secondary"
    Sub-Case  CONSR-BMC-OEMCMD-0006-0001_2  run ipmi command "Get-Set BIOS Flash Switch Position to Primary"

CONSR-BMC-OEMCMD-0007-0001
    [Documentation]  This test checks IPMI OEM command: "Set system GUID to VPD of main board"
    [Tags]     CONSR-OBMC-BSFC-0032-0001  CONSR-BMC-OEMCMD-0007-0001  Artemis
    [Timeout]  10 min 00 seconds
    Sub-Case  CONSR-BMC-OEMCMD-0007-0001_1  run ipmi command "Set system GUID to VPD of main board"

CONSR-BMC-OEMCMD-0008-0001
    [Documentation]  This test checks IPMI OEM command: "Get host POST Code"
    [Tags]     CONSR-OBMC-BSFC-0032-0001  CONSR-BMC-OEMCMD-0008-0001  Artemis
    [Timeout]  10 min 00 seconds
    Sub-Case  CONSR-BMC-OEMCMD-0008-0001_1  run ipmi command "Get host POST Code"
