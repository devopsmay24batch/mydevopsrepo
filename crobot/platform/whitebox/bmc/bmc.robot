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
# Script       : BMC.robot                                                                                            #
# Date         : July 29, 2020                                                                                        #
# Author       : James Shi <jameshi@celestica.com>                                                                    #
# Description  : This script will validate BMC                                                                        #
#                                                                                                                     #
# Script Revision Details:                                                                                            #
#   Initial Draft for bmc testing                                                                                      #
#######################################################################################################################

*** Settings ***
Documentation       Tests to verify BMC functions described in the BMC function SPEC for the whiteboxproject.

# Force Tags        BMC
Variables         BMC_variable.py
Library           ../WhiteboxLibAdapter.py
Library           whitebox_lib.py
Library           bios_menu_lib.py
Resource          BMC_keywords.robot
Resource          CommonResource.robot

Suite Setup       OS Connect Device
Suite Teardown    OS Disconnect Device
** Variables ***
# It is recommended to use <{ScriptName}|{FeatureName}|{DomainName}_Variable> file for variable declaration with help of
# setting table. This section should keep blank.
#In extreme case if script requires variable then it should be defined in this table with documentaiton tag

*** Test Cases ***
# *** comment ***
CONSR-BMCT-BSFC-0001-0001
    [Documentation]  This test checks BMC Version
    [Tags]     CONSR-BMCT-BSFC-0001-0001  tyr  tyr-se  Titan-RD  Athena-G2
    [Timeout]  30 min 00 seconds
    [Setup]  get all the variables
    Sub-Case  CONSR-BMCT-BSFC-0001-0001_1  check BMC Version after mc reset warm
    Sub-Case  CONSR-BMCT-BSFC-0001-0001_2  check BMC Version after mc reset cold
#    Sub-Case  CONSR-BMCT-BSFC-0001-0001_3  check BMC Version after ac cycle
    Sub-Case  CONSR-BMCT-BSFC-0001-0001_4  power cycle OS
    [Teardown]  Run Keyword If Test Failed  fix SOL's activation causing serial port problem

CONSR-BMCT-BSFC-0002-0001
    [Documentation]  This test checks KCS Function
    [Tags]     CONSR-BMCT-BSFC-0002-0001  tyr  tyr-se  Titan-RD  Athena-G2
    [Timeout]  30 min 00 seconds
    [Setup]  get all the variables
    Sub-Case  CONSR-BMCT-BSFC-0002-0001_1  check KCS Function
    [Teardown]  Run Keyword If Test Failed  fix SOL's activation causing serial port problem

CONSR-BMCT-BSFC-0003-0001
    [Documentation]  This test checks the Serial over LAN
    [Tags]     CONSR-BMCT-BSFC-0003-0001  tyr  tyr-se  Titan-RD  Athena-G2
    [Timeout]  90 min 00 seconds
    [Setup]  get all the variables
    Sub-Case  CONSR-BMCT-BSFC-0003-0001_1  check COM0 BIOS settings
    Sub-Case  CONSR-BMCT-BSFC-0003-0001_2  check COM0 baud rate under OS
    Sub-Case  CONSR-BMCT-BSFC-0003-0001_3  Enter command to active SOL
    [Teardown]  Run Keyword If Test Failed  fix SOL's activation causing serial port problem

CONSR-BMCT-BSFC-0004-0001
    [Documentation]  This test checks User Name and Password Check
    [Tags]     CONSR-BMCT-BSFC-0004-0001  tyr  tyr-se  Titan-RD  Athena-G2
    [Timeout]  40 min 00 seconds
    [Setup]  get all the variables
    Sub-Case  CONSR-BMCT-BSFC-0004-0001_1  User Name and Password Check
    [Teardown]  Run Keyword If Test Failed  fix SOL's activation causing serial port problem

CONSR-BMCT-BSFC-0005-0001
    [Documentation]  This test checks Function_005_User Privilege Check
    [Tags]     CONSR-BMCT-BSFC-0005-0001  tyr  tyr-se  Titan-RD  Athena-G2
    [Timeout]  40 min 00 seconds
    [Setup]  get all the variables
    Sub-Case  CONSR-BMCT-BSFC-0005-0001_1  User Privilege Check

CONSR-BMCT-BSFC-0006-0001
    [Documentation]  This test checks Function_006_Power Control
    [Tags]     CONSR-BMCT-BSFC-0006-0001  tyr  tyr-se  Titan-RD  Athena-G2
    [Timeout]  40 min 00 seconds
    [Setup]  get all the variables
    Sub-Case  CONSR-BMCT-BSFC-0006-0001_1  Power Control Check
    [Teardown]  Run Keyword If Test Failed  fix SOL's activation causing serial port problem

CONSR-BMCT-BSFC-0024-0001
    [Documentation]  This test checks Function_025_SMASH CLP Command
    [Tags]     CONSR-BMCT-BSFC-0024-0001  tyr  tyr-se  Titan-RD  Athena-G2
    [Timeout]  30 min 00 seconds
    [Setup]  get all the variables
    Sub-Case  CONSR-BMCT-BSFC-0024-0001_1  SMASH CLP Command Check
    [Teardown]  Run Keyword If Test Failed  fix SOL's activation causing serial port problem

CONSR-BMCT-BSFC-0025-0001
    [Documentation]  This test checks BMC POH status after BMC FW refresh
    [Tags]     CONSR-BMCT-BSFC-0025-0001  Titan-RD-DDN  stress
    [Timeout]  720 min 00 seconds
    [Setup]  get all the variables
    Sub-Case  CONSR-BMCT-BSFC-0025-0001_1  check BMC POH status after BMC FW update
    [Teardown]  Run Keyword If Test Failed  fix SOL's activation causing serial port problem

CONSR-BMCT-NTWT-0001-0001
    [Documentation]  This test checks BMC lan static&dhcp function
    [Tags]     CONSR-BMCT-NTWT-0001-0001  tyr  tyr-se  Titan-RD  Athena-G2
    [Timeout]  30 min 00 seconds
    [Setup]  get all the variables
    Sub-Case  CONSR-BMCT-NTWT-0001-0001_1  modify bmc lan static&dhcp function
    [Teardown]  Run Keyword If Test Failed  fix SOL's activation causing serial port problem

CONSR-BMCT-NTWT-0010-0001
    [Documentation]  This test checks BMC Suite ID Test
    [Tags]     CONSR-BMCT-NTWT-0010-0001  special  Athena-G2
    [Timeout]  20 min 00 seconds
    [Setup]  get all the variables
    Sub-Case  CONSR-BMCT-NTWT-0010-0001_1  Check BMC Suite ID Test

CONSR-BMCT-NTWT-0011-0001
    [Documentation]  This test checks Web Session ID
    [Tags]     CONSR-BMCT-NTWT-0011-0001  Athena-G2  Titan-RD
    [Timeout]  20 min 00 seconds
    Sub-Case  CONSR-BMCT-NTWT-0011-0001_1  Check Web Session ID

CONSR-BMCT-NTWT-0013-0001
    [Documentation]  This test checks BMC Network_013_BMC SSL Cipher Version Test
    [Tags]     CONSR-BMCT-NTWT-0013-0001  lenovo  special  Athena-G2
    [Timeout]  10 min 00 seconds
    [Setup]  get all the variables
    Sub-Case  CONSR-BMCT-NTWT-0013-0001_1  Check BMC SSL Cipher Version

CONSR-BMCT-NTWT-0014-0001
    [Documentation]  This test checks BMC dedicate and share port ping stress 12 hours
    [Tags]     CONSR-BMCT-NTWT-0014-0001  stress  Titan-RD
    [Timeout]  720 min 00 seconds
    [Setup]  get all the variables
    Sub-Case  CONSR-BMCT-NTWT-0014-0001_1  Check BMC dedicate and share port ping stress

CONSR-BMCT-NTWT-0015-0001
    [Documentation]  This test checks Invalid BMC API Call Test
    [Tags]     CONSR-BMCT-NTWT-0015-0001  lenovo  special
    [Timeout]  20 min 00 seconds
    Sub-Case  CONSR-BMCT-NTWT-0015-0001_1  Check BMC API Call Test

CONSR-BMCT-FWUP-0015-0001
    [Documentation]  This test checks the local BMC programming functions by dc cycle
    [Tags]     CONSR-BMCT-FWUP-0015-0001  tyr  tyr-se  Titan-RD  Athena-G2
    [Timeout]  60 min 00 seconds
    [Setup]  prepare BMC images
    Sub-Case  CONSR-BMCT-FWUP-0015-0001_1  downgrade bmc and dc cycle to check version
    Sub-Case  CONSR-BMCT-FWUP-0015-0001_2  common upgrade bmc check list
    Sub-Case  CONSR-BMCT-FWUP-0015-0001_3  upgrade bmc and dc cycle to check version
    Sub-Case  CONSR-BMCT-FWUP-0015-0001_4  common upgrade bmc check list
    [Teardown]  Run Keyword If Test Failed  power cycle OS

CONSR-BMCT-FWUP-0016-0001
    [Documentation]  This test checks the remote BMC programming functions by dc cycle
    [Tags]     CONSR-BMCT-FWUP-0016-0001  tyr  tyr-se  Titan-RD  Athena-G2
    [Timeout]  60 min 00 seconds
    [Setup]  prepare BMC images
    Sub-Case  CONSR-BMCT-FWUP-0016-0001_1  remote downgrade bmc and dc cycle to check version
    Sub-Case  CONSR-BMCT-FWUP-0016-0001_2  common upgrade bmc check list
    Sub-Case  CONSR-BMCT-FWUP-0016-0001_3  remote upgrade bmc and dc cycle to check version
    Sub-Case  CONSR-BMCT-FWUP-0016-0001_4  common upgrade bmc check list
    [Teardown]  Run Keyword If Test Failed  power cycle OS

CONSR-BMCT-FWUP-0017-0001
    [Documentation]  This test checks the local BIOS programming functions by reboot
    [Tags]     CONSR-BMCT-FWUP-0017-0001  tyr  tyr-se  Titan-RD  Athena-G2
    [Timeout]  60 min 00 seconds
    [Setup]  prepare BIOS images
    Sub-Case  CONSR-BMCT-FWUP-0017-0001_1  downgrade bios and reboot to check version
    Sub-Case  CONSR-BMCT-FWUP-0017-0001_2  common upgrade bios check list
    Sub-Case  CONSR-BMCT-FWUP-0017-0001_3  upgrade bios and reboot to check version
    Sub-Case  CONSR-BMCT-FWUP-0017-0001_4  common upgrade bios check list
    [Teardown]  Run Keyword If Test Failed  power cycle OS

CONSR-BMCT-FWUP-0018-0001
    [Documentation]  This test checks the local BIOS programming functions by dc cycle
    [Tags]     CONSR-BMCT-FWUP-0018-0001  tyr  tyr-se  Titan-RD  Athena-G2
    [Timeout]  60 min 00 seconds
    [Setup]  prepare BIOS images
    Sub-Case  CONSR-BMCT-FWUP-0018-0001_1  downgrade bios and dc cycle to check version
    Sub-Case  CONSR-BMCT-FWUP-0018-0001_2  common upgrade bios check list
    Sub-Case  CONSR-BMCT-FWUP-0018-0001_3  upgrade bios and dc cycle to check version
    Sub-Case  CONSR-BMCT-FWUP-0018-0001_4  common upgrade bios check list
    [Teardown]  Run Keyword If Test Failed  power cycle OS

CONSR-BMCT-FWUP-0019-0001
    [Documentation]  This test checks the remote BIOS programming functions by reboot
    [Tags]     CONSR-BMCT-FWUP-0019-0001  tyr  tyr-se  Titan-RD  Athena-G2
    [Timeout]  60 min 00 seconds
    [Setup]  prepare BIOS images
    Sub-Case  CONSR-BMCT-FWUP-0019-0001_1  remote downgrade bios and reboot to check version
    Sub-Case  CONSR-BMCT-FWUP-0019-0001_2  common upgrade bios check list
    Sub-Case  CONSR-BMCT-FWUP-0019-0001_3  remote upgrade bios and reboot to check version
    Sub-Case  CONSR-BMCT-FWUP-0019-0001_4  common upgrade bios check list
    [Teardown]  Run Keyword If Test Failed  power cycle OS

CONSR-BMCT-FWUP-0020-0001
    [Documentation]  This test checks the remote BIOS programming functions by dc cyle
    [Tags]     CONSR-BMCT-FWUP-0020-0001  tyr  tyr-se  Titan-RD  Athena-G2
    [Timeout]  60 min 00 seconds
    [Setup]  prepare BIOS images
    Sub-Case  CONSR-BMCT-FWUP-0020-0001_1  remote downgrade bios and dc cycle to check version
    Sub-Case  CONSR-BMCT-FWUP-0020-0001_2  common upgrade bios check list
    Sub-Case  CONSR-BMCT-FWUP-0020-0001_3  remote upgrade bios and dc cycle to check version
    Sub-Case  CONSR-BMCT-FWUP-0020-0001_4  common upgrade bios check list
    [Teardown]  Run Keyword If Test Failed  power cycle OS

CONSR-BMC-IPMI-0001-0001
    [Documentation]  This test checks IPMI command: Get Device ID
    [Tags]     CONSR-BMC-IPMI-0001-0001  tyr  tyr-se  ipmi  Titan-RD  Athena-G2
    [Timeout]  1 min 00 seconds
    [Setup]  get DUT variables
    Sub-Case  CONSR-BMC-IPMI-0001-0001_1  run ipmi command "Get Device ID"

CONSR-BMC-IPMI-0002-0001
    [Documentation]  This test checks IPMI command: "cold reset"
    [Tags]     CONSR-BMC-IPMI-0002-0001  tyr  tyr-se  ipmi  Titan-RD  Athena-G2
    [Timeout]  20 min 00 seconds
    Sub-Case  CONSR-BMC-IPMI-0002-0001_1  run ipmi command "cold reset"
    [Teardown]  restore serial ouput to normal

CONSR-BMC-IPMI-0003-0001
    [Documentation]  This test checks IPMI command: "warm reset"
    [Tags]     CONSR-BMC-IPMI-0003-0001  tyr  tyr-se  ipmi  Titan-RD  Athena-G2
    [Timeout]  20 min 00 seconds
    Sub-Case  CONSR-BMC-IPMI-0003-0001_1  run ipmi command "warm reset"
    [Teardown]  restore serial ouput to normal

CONSR-BMC-IPMI-0004-0001
    [Documentation]  This test checks IPMI command: "Get Self Test Results"
    [Tags]     CONSR-BMC-IPMI-0004-0001  tyr  tyr-se  ipmi  Titan-RD  Athena-G2
    [Timeout]  5 min 00 seconds
    Sub-Case  CONSR-BMC-IPMI-0004-0001_1  run ipmi command "Get Self Test Results"

CONSR-BMC-IPMI-0005-0001
    [Documentation]  This test checks IPMI command: "Set ACPI Power State:soft off"
    [Tags]     CONSR-BMC-IPMI-0005-0001  tyr  tyr-se  ipmi  Titan-RD  Athena-G2
    [Timeout]  5 min 00 seconds
    Sub-Case  CONSR-BMC-IPMI-0005-0001_1  run ipmi command "Set ACPI Power State:soft off"
    [Teardown]  Set ACPI Power State back to default

CONSR-BMC-IPMI-0006-0001
    [Documentation]  This test checks IPMI command: "Get ACPI Power State:soft off"
    [Tags]     CONSR-BMC-IPMI-0006-0001  tyr  tyr-se  ipmi  Titan-RD  Athena-G2
    [Timeout]  5 min 00 seconds
    Sub-Case  CONSR-BMC-IPMI-0005-0001_1  run ipmi command "Get ACPI Power State:soft off"
    [Teardown]  Set ACPI Power State back to default

CONSR-BMC-IPMI-0007-0001
    [Documentation]  This test checks IPMI command: "Reset Watchdog Timer"
    [Tags]     CONSR-BMC-IPMI-0007-0001  tyr  tyr-se  ipmi  Titan-RD  Athena-G2
    [Timeout]  5 min 00 seconds
    Sub-Case  CONSR-BMC-IPMI-0007-0001_1  run ipmi command "Set Watchdog Timer"
    Sub-Case  CONSR-BMC-IPMI-0007-0002_1  run ipmi command "Reset Watchdog Timer"
    [Teardown]  run ipmi command "Restore Watchdog Timer to default"

CONSR-BMC-IPMI-0008-0001
    [Documentation]  This test checks IPMI command: "Set Watchdog Timer"
    [Tags]     CONSR-BMC-IPMI-0008-0001  tyr  tyr-se  ipmi  Titan-RD  Athena-G2
    [Timeout]  5 min 00 seconds
    Sub-Case  CONSR-BMC-IPMI-0008-0001_1  run ipmi command "Set Watchdog Timer"
    [Teardown]  run ipmi command "Restore Watchdog Timer to default"

CONSR-BMC-IPMI-0009-0001
    [Documentation]  This test checks IPMI command: "Get Watchdog Timer"
    [Tags]     CONSR-BMC-IPMI-0009-0001  tyr  tyr-se  ipmi  Titan-RD  Athena-G2
    [Timeout]  5 min 00 seconds
    Sub-Case  CONSR-BMC-IPMI-0009-0001_1  run ipmi command "Set Watchdog Timer"
    Sub-Case  CONSR-BMC-IPMI-0009-0001_2  run ipmi command "Get Watchdog Timer"
    [Teardown]  run ipmi command "Restore Watchdog Timer to default"

CONSR-BMC-IPMI-0010-0001
    [Documentation]  This test checks IPMI command: "Set BMC Global enables"
    [Tags]     CONSR-BMC-IPMI-0010-0001  tyr  tyr-se  ipmi  Titan-RD  Athena-G2
    [Timeout]  5 min 00 seconds
    Sub-Case  CONSR-BMC-IPMI-0010-0001_1  run ipmi command "Set BMC Global enables"

CONSR-BMC-IPMI-0011-0001
    [Documentation]  This test checks IPMI command: "Get BMC Global enables"
    [Tags]     CONSR-BMC-IPMI-0011-0001  tyr  tyr-se  ipmi  Titan-RD  Athena-G2
    [Timeout]  5 min 00 seconds
    Sub-Case  CONSR-BMC-IPMI-0011-0001_1  run ipmi command "Get BMC Global enables"

CONSR-BMC-IPMI-0012-0001
    [Documentation]  This test checks IPMI command: "Clear Message Flags"
    [Tags]     CONSR-BMC-IPMI-0012-0001  tyr  tyr-se  ipmi  Titan-RD
    [Timeout]  5 min 00 seconds
    Sub-Case  CONSR-BMC-IPMI-0012-0001_1  run ipmi command "Clear Message Flags"

CONSR-BMC-IPMI-0013-0001
    [Documentation]  This test checks IPMI command: "Get Message Flags"
    [Tags]     CONSR-BMC-IPMI-0013-0001  tyr  tyr-se  ipmi  Titan-RD
    [Timeout]  5 min 00 seconds
    Sub-Case  CONSR-BMC-IPMI-0013-0001_1  run ipmi command "Clear Message Flags"
    Sub-Case  CONSR-BMC-IPMI-0013-0001_2  run ipmi command "Get Message Flags"

CONSR-BMC-IPMI-0014-0001
    [Documentation]  This test checks IPMI command: "Enable Message Channel Receive"
    [Tags]     CONSR-BMC-IPMI-0014-0001  tyr  tyr-se  ipmi  Athena-G2
    [Timeout]  5 min 00 seconds
    Sub-Case  CONSR-BMC-IPMI-0014-0001_1  run ipmi command "Enable Message Channel Receive"

CONSR-BMC-IPMI-0015-0001
    [Documentation]  This test checks IPMI command: "Get System GUID"
    [Tags]     CONSR-BMC-IPMI-0015-0001  tyr  tyr-se  ipmi  Titan-RD  Athena-G2
    [Timeout]  5 min 00 seconds
    Sub-Case  CONSR-BMC-IPMI-0015-0001_1  run ipmi command "Get System GUID"

CONSR-BMC-IPMI-0016-0001
    [Documentation]  This test checks IPMI command: "Get Channel Authentication capabilities"
    [Tags]     CONSR-BMC-IPMI-0016-0001  tyr  tyr-se  ipmi  Titan-RD  Athena-G2
    [Timeout]  5 min 00 seconds
    Sub-Case  CONSR-BMC-IPMI-0016-0001_1  run ipmi command "Get Channel Authentication capabilities"

CONSR-BMC-IPMI-0017-0001
    [Documentation]  This test checks IPMI command: "Get Session Challenge"
    [Tags]     CONSR-BMC-IPMI-0017-0001  tyr  tyr-se  ipmi  Titan-RD  Athena-G2
    [Timeout]  5 min 00 seconds
    Sub-Case  CONSR-BMC-IPMI-0017-0001_1  run ipmi command "Get Session Challenge" by remote ipmitool

CONSR-BMC-IPMI-0018-0001
    [Documentation]  This test checks IPMI command: "Set Session Privilege Level"
    [Tags]     CONSR-BMC-IPMI-0018-0001  tyr  tyr-se  ipmi  Titan-RD  Athena-G2
    [Timeout]  5 min 00 seconds
    [Setup]  get DUT variables
    Sub-Case  CONSR-BMC-IPMI-0018-0001_1  run ipmi command "Set Session Privilege Level" by remote ipmitool

CONSR-BMC-IPMI-0019-0001
    [Documentation]  This test checks IPMI command: "Get Session Info"
    [Tags]     CONSR-BMC-IPMI-0019-0001  tyr  tyr-se  ipmi  Titan-RD  Athena-G2
    [Timeout]  5 min 00 seconds
    Sub-Case  CONSR-BMC-IPMI-0019-0001_1  run ipmi command "Get Session Info"

CONSR-BMC-IPMI-0020-0001
    [Documentation]  This test checks IPMI command: "Get AuthCode"
    [Tags]     CONSR-BMC-IPMI-0020-0001  tyr  tyr-se  ipmi  Titan-RD  Athena-G2
    [Timeout]  20 min 00 seconds
    Sub-Case  CONSR-BMC-IPMI-0020-0001_1  run ipmi command "Get AuthCode"

CONSR-BMC-IPMI-0021-0001
    [Documentation]  This test checks IPMI command: "Set Channel Access"
    [Tags]     CONSR-BMC-IPMI-0021-0001  tyr  tyr-se  ipmi  Titan-RD  Athena-G2
    [Timeout]  5 min 00 seconds
    Sub-Case  CONSR-BMC-IPMI-0021-0001_1  run ipmi command "Set Channel Access"

CONSR-BMC-IPMI-0022-0001
    [Documentation]  This test checks IPMI command: "Get Channel Access"
    [Tags]     CONSR-BMC-IPMI-0022-0001  tyr  tyr-se  ipmi  Titan-RD  Athena-G2
    [Timeout]  5 min 00 seconds
    Sub-Case  CONSR-BMC-IPMI-0022-0001_1  run ipmi command "Get Channel Access"

CONSR-BMC-IPMI-0023-0001
    [Documentation]  This test checks IPMI command: "Get Channel Info"
    [Tags]     CONSR-BMC-IPMI-0023-0001  tyr  tyr-se  ipmi  Titan-RD  Athena-G2
    [Timeout]  5 min 00 seconds
    Sub-Case  CONSR-BMC-IPMI-0023-0001_1  run ipmi command "Get Channel Info"

CONSR-BMC-IPMI-0024-0001
    [Documentation]  This test checks IPMI command: "Set User Access"
    [Tags]     CONSR-BMC-IPMI-0024-0001  tyr  tyr-se  ipmi  Titan-RD  Athena-G2
    [Timeout]  5 min 00 seconds
    Sub-Case  CONSR-BMC-IPMI-0024-0001_1  run ipmi command "Set User Access"

CONSR-BMC-IPMI-0025-0001
    [Documentation]  This test checks IPMI command: "Get User Access"
    [Tags]     CONSR-BMC-IPMI-0025-0001  tyr  tyr-se  ipmi  Titan-RD  Athena-G2
    [Timeout]  5 min 00 seconds
    Sub-Case  CONSR-BMC-IPMI-0025-0001_1  run ipmi command "Get User Access"

CONSR-BMC-IPMI-0026-0001
    [Documentation]  This test checks IPMI command: "Set User name"
    [Tags]     CONSR-BMC-IPMI-0026-0001  tyr  tyr-se  ipmi  Titan-RD  Athena-G2
    [Timeout]  5 min 00 seconds
    Sub-Case  CONSR-BMC-IPMI-0026-0001_1  run ipmi command "Set User name"

CONSR-BMC-IPMI-0027-0001
    [Documentation]  This test checks IPMI command: "Get User name"
    [Tags]     CONSR-BMC-IPMI-0027-0001  tyr  tyr-se  ipmi  Titan-RD  Athena-G2
    [Timeout]  5 min 00 seconds
    Sub-Case  CONSR-BMC-IPMI-0027-0001_1  run ipmi command "Get User name"

CONSR-BMC-IPMI-0028-0001
    [Documentation]  This test checks IPMI command: "Set User Password"
    [Tags]     CONSR-BMC-IPMI-0028-0001  tyr  tyr-se  ipmi  Titan-RD  Athena-G2
    [Timeout]  5 min 00 seconds
    Sub-Case  CONSR-BMC-IPMI-0028-0001_1  run ipmi command "Set User Password"

CONSR-BMC-IPMI-0029-0001
    [Documentation]  This test checks IPMI command: "Get Payload Activation Status"
    [Tags]     CONSR-BMC-IPMI-0029-0001  tyr  tyr-se  ipmi  Titan-RD  Athena-G2
    [Timeout]  5 min 00 seconds
    Sub-Case  CONSR-BMC-IPMI-0029-0001_1  run ipmi command "Get Payload Activation Status"

CONSR-BMC-IPMI-0030-0001
    [Documentation]  This test checks IPMI command: "Get Payload Instance Info"
    [Tags]     CONSR-BMC-IPMI-0030-0001  tyr  tyr-se  ipmi  Titan-RD  Athena-G2
    [Timeout]  5 min 00 seconds
    Sub-Case  CONSR-BMC-IPMI-0030-0001_1  run ipmi command "Get Payload Instance Info"

CONSR-BMC-IPMI-0031-0001
    [Documentation]  This test checks IPMI command: "Set user Payload Access"
    [Tags]     CONSR-BMC-IPMI-0031-0001  tyr  tyr-se  ipmi  Titan-RD  Athena-G2
    [Timeout]  5 min 00 seconds
    Sub-Case  CONSR-BMC-IPMI-0031-0001_1  run ipmi command "Set user Payload Access"

CONSR-BMC-IPMI-0032-0001
    [Documentation]  This test checks IPMI command: "Get user Payload Access"
    [Tags]     CONSR-BMC-IPMI-0032-0001  tyr  tyr-se  ipmi  Titan-RD  Athena-G2
    [Timeout]  5 min 00 seconds
    Sub-Case  CONSR-BMC-IPMI-0032-0001_1  run ipmi command "Get user Payload Access"

CONSR-BMC-IPMI-0033-0001
    [Documentation]  This test checks IPMI command: "Get channel Payload support"
    [Tags]     CONSR-BMC-IPMI-0033-0001  tyr  tyr-se  ipmi  Titan-RD  Athena-G2
    [Timeout]  5 min 00 seconds
    Sub-Case  CONSR-BMC-IPMI-0033-0001_1  run ipmi command "Get channel Payload support"

CONSR-BMC-IPMI-0034-0001
    [Documentation]  This test checks IPMI command: "Get channel Payload Version"
    [Tags]     CONSR-BMC-IPMI-0034-0001  tyr  tyr-se  ipmi  Titan-RD  Athena-G2
    [Timeout]  5 min 00 seconds
    Sub-Case  CONSR-BMC-IPMI-0034-0001_1  run ipmi command "Get channel Payload Version"

CONSR-BMC-IPMI-0036-0001
    [Documentation]  This test checks IPMI command: "Master Write-Read"
    [Tags]     CONSR-BMC-IPMI-0036-0001  tyr  tyr-se  ipmi  Titan-RD  Athena-G2
    [Timeout]  5 min 00 seconds
    Sub-Case  CONSR-BMC-IPMI-0036-0001_1  run ipmi command "Master Write-Read"

CONSR-BMC-IPMI-0037-0001
    [Documentation]  This test checks IPMI command: "Set Channel Security Keys"
    [Tags]     CONSR-BMC-IPMI-0037-0001  tyr  tyr-se  ipmi  Titan-RD  Athena-G2
    [Timeout]  5 min 00 seconds
    Sub-Case  CONSR-BMC-IPMI-0037-0001_1  run ipmi command "Set Channel Security Keys"

CONSR-BMC-IPMI-0038-0001
    [Documentation]  This test checks IPMI command: "Get Chassis Capabilities"
    [Tags]     CONSR-BMC-IPMI-0038-0001  tyr  tyr-se  ipmi  Titan-RD  Athena-G2
    [Timeout]  5 min 00 seconds
    Sub-Case  CONSR-BMC-IPMI-0038-0001_1  run ipmi command "Get Chassis Capabilities"

CONSR-BMC-IPMI-0039-0001
    [Documentation]  This test checks IPMI command: "Get Chassis Status"
    [Tags]     CONSR-BMC-IPMI-0039-0001  tyr  tyr-se  ipmi  Titan-RD  Athena-G2
    [Timeout]  5 min 00 seconds
    Sub-Case  CONSR-BMC-IPMI-0039-0001_1  run ipmi command "Get Chassis Status"

CONSR-BMC-IPMI-0040-0001
    [Documentation]  This test checks IPMI command: "Chassis power control"
    [Tags]     CONSR-BMC-IPMI-0040-0001  tyr  tyr-se  ipmi  Titan-RD  Athena-G2
    [Timeout]  60 min 00 seconds
    [Setup]  get all the variables
    Sub-Case  CONSR-BMC-IPMI-0040-0001_1  run ipmi command "Chassis power down"
    Sub-Case  CONSR-BMC-IPMI-0040-0001_2  run ipmi command "Chassis power up"
    Sub-Case  CONSR-BMC-IPMI-0040-0001_3  run ipmi command "Chassis power cycle"
    Sub-Case  CONSR-BMC-IPMI-0040-0001_4  run ipmi command "Chassis soft shutdown"
    [Teardown]  Run Keyword If Test Failed  power cycle OS

CONSR-BMC-IPMI-0043-0001
    [Documentation]  This test checks IPMI command: "Get System Restart Cause"
    [Tags]     CONSR-BMC-IPMI-0043-0001  tyr  tyr-se  ipmi  Titan-RD  Athena-G2
    [Timeout]  30 min 00 seconds
    [Setup]  get all the variables
    Sub-Case  CONSR-BMC-IPMI-0043-0001_1  run ipmi command "Get System Restart Cause"

CONSR-BMC-IPMI-0044-0001
    [Documentation]  This test checks IPMI command: "Set System Boot Options"
    [Tags]     CONSR-BMC-IPMI-0044-0001  tyr  tyr-se  ipmi  Titan-RD  Athena-G2
    [Timeout]  30 min 00 seconds
    [Setup]  get all the variables
    Sub-Case  CONSR-BMC-IPMI-0044-0001_1  run ipmi command "Set System Boot Options"
    [Teardown]  Run Keyword If Test Failed  power cycle OS

CONSR-BMC-IPMI-0045-0001
    [Documentation]  This test checks IPMI command: "Get System Boot Options"
    [Tags]     CONSR-BMC-IPMI-0045-0001  tyr  tyr-se  ipmi  Titan-RD  Athena-G2
    [Timeout]  30 min 00 seconds
    [Setup]  get all the variables
    Sub-Case  CONSR-BMC-IPMI-0045-0001_1  run ipmi command "Get System Boot Options"
    [Teardown]  Run Keyword If Test Failed  power cycle OS

CONSR-BMC-IPMI-0047-0001
    [Documentation]  This test checks IPMI command: "Set Power Cycle Interval"
    [Tags]     CONSR-BMC-IPMI-0047-0001  tyr  tyr-se  ipmi  Titan-RD  Athena-G2
    [Timeout]  30 min 00 seconds
    [Setup]  get all the variables
    Sub-Case  CONSR-BMC-IPMI-0047-0001_1  run ipmi command "Set Power Cycle Interval"
    [Teardown]  Run Keyword If Test Failed  power cycle OS

CONSR-BMC-IPMI-0049-0001
    [Documentation]  This test checks IPMI command: "Set Event Receiver"
    [Tags]     CONSR-BMC-IPMI-0049-0001  tyr  tyr-se  ipmi  Titan-RD  Athena-G2
    [Timeout]  5 min 00 seconds
    Sub-Case  CONSR-BMC-IPMI-0049-0001_1  run ipmi command "Set Event Receiver"

CONSR-BMC-IPMI-0050-0001
    [Documentation]  This test checks IPMI command: "Get Event Receiver"
    [Tags]     CONSR-BMC-IPMI-0050-0001  tyr  tyr-se  ipmi  Titan-RD  Athena-G2
    [Timeout]  5 min 00 seconds
    Sub-Case  CONSR-BMC-IPMI-0050-0001_1  run ipmi command "Get Event Receiver"

CONSR-BMCT-IPMI-0051-0001
    [Documentation]  This test checks IPMI command: "Platform Event Message"
    [Tags]     CONSR-BMC-IPMI-0051-0001  tyr  tyr-se  ipmi  Titan-RD  Athena-G2
    [Timeout]  5 min 00 seconds
    Sub-Case  CONSR-BMC-IPMI-0051-0001_1  run ipmi command "Platform Event Message"

CONSR-BMC-IPMI-0052-0001
    [Documentation]  This test checks IPMI command: "Get PEF Capabilities"
    [Tags]     CONSR-BMC-IPMI-0052-0001  tyr  tyr-se  ipmi  Titan-RD  Athena-G2
    [Timeout]  5 min 00 seconds
    Sub-Case  CONSR-BMC-IPMI-0052-0001_1  run ipmi command "Get PEF Capabilities"

CONSR-BMC-IPMI-0053-0001
    [Documentation]  This test checks IPMI command: "Arm PEF Postpone Timer"
    [Tags]     CONSR-BMC-IPMI-0053-0001  tyr  tyr-se  ipmi  Titan-RD  Athena-G2
    [Timeout]  5 min 00 seconds
    Sub-Case  CONSR-BMC-IPMI-0053-0001_1  run ipmi command "Disable postpone timer"
    Sub-Case  CONSR-BMC-IPMI-0053-0001_2  run ipmi command "arm timer"
    Sub-Case  CONSR-BMC-IPMI-0053-0001_3  run ipmi command "get present countdown value"

CONSR-BMC-IPMI-0054-0001
    [Documentation]  This test checks IPMI command: "Set PEF Configuration Parameters"
    [Tags]     CONSR-BMC-IPMI-0054-0001  tyr  tyr-se  ipmi  Titan-RD  Athena-G2
    [Timeout]  5 min 00 seconds
    Sub-Case  CONSR-BMC-IPMI-0054-0001_1  run ipmi command "Set PEF Configuration Parameters"

CONSR-BMC-IPMI-0055-0001
    [Documentation]  This test checks IPMI command: "Get PEF Configuration Parameters"
    [Tags]     CONSR-BMC-IPMI-0055-0001  tyr  tyr-se  ipmi  Titan-RD  Athena-G2
    [Timeout]  5 min 00 seconds
    Sub-Case  CONSR-BMC-IPMI-0055-0001_1  run ipmi command "Get PEF Configuration Parameters"

CONSR-BMC-IPMI-0056-0001
    [Documentation]  This test checks IPMI command: "Set Last Processed Event ID"
    [Tags]     CONSR-BMC-IPMI-0056-0001  tyr  tyr-se  ipmi  Titan-RD  Athena-G2
    [Timeout]  5 min 00 seconds
    Sub-Case  CONSR-BMC-IPMI-0056-0001_1  run ipmi command "Set Last Processed Event ID"

CONSR-BMC-IPMI-0057-0001
    [Documentation]  This test checks IPMI command: "Get Last Processed Event ID"
    [Tags]     CONSR-BMC-IPMI-0057-0001  tyr  tyr-se  ipmi  Titan-RD  Athena-G2
    [Timeout]  5 min 00 seconds
    Sub-Case  CONSR-BMC-IPMI-0057-0001_1  run ipmi command "Get Last Processed Event ID"

CONSR-BMC-IPMI-0058-0001
    [Documentation]  This test checks IPMI command: "Alert Immediate"
    [Tags]     CONSR-BMC-IPMI-0058-0001  tyr  tyr-se  ipmi  Titan-RD  Athena-G2
    [Timeout]  5 min 00 seconds
    Sub-Case  CONSR-BMC-IPMI-0058-0001_1  run ipmi command "Alert Immediate"

CONSR-BMC-IPMI-0059-0001
    [Documentation]  This test checks IPMI command: "PET Acknowledge"
    [Tags]     CONSR-BMC-IPMI-0059-0001  tyr  tyr-se  ipmi  Titan-RD  Athena-G2
    [Timeout]  5 min 00 seconds
    Sub-Case  CONSR-BMC-IPMI-0059-0001_1  run ipmi command "PET Acknowledge"

CONSR-BMC-IPMI-0060-0001
    [Documentation]  This test checks IPMI command: "Set Sensor Hysteresis"
    [Tags]     CONSR-BMC-IPMI-0060-0001  tyr  tyr-se  ipmi  Titan-RD  Athena-G2
    [Timeout]  5 min 00 seconds
    Sub-Case  CONSR-BMC-IPMI-0060-0001_1  run ipmi command "Set Sensor Hysteresis"

CONSR-BMC-IPMI-0061-0001
    [Documentation]  This test checks IPMI command: "Set Sensor Hysteresis"
    [Tags]     CONSR-BMC-IPMI-0061-0001  tyr  tyr-se  ipmi  Titan-RD  Athena-G2
    [Timeout]  5 min 00 seconds
    Sub-Case  CONSR-BMC-IPMI-0061-0001_1  run ipmi command "Get Sensor Hysteresis"

CONSR-BMC-IPMI-0062-0001
    [Documentation]  This test checks IPMI command: "Set Sensor Threshold"
    [Tags]     CONSR-BMC-IPMI-0062-0001  tyr  tyr-se  ipmi  Titan-RD  Athena-G2
    [Timeout]  5 min 00 seconds
    Sub-Case  CONSR-BMC-IPMI-0062-0001_1  run ipmi command "Set Sensor Threshold"

CONSR-BMC-IPMI-0063-0001
    [Documentation]  This test checks IPMI command: "Get Sensor Threshold"
    [Tags]     CONSR-BMC-IPMI-0063-0001  tyr  tyr-se  ipmi  Titan-RD  Athena-G2
    [Timeout]  5 min 00 seconds
    Sub-Case  CONSR-BMC-IPMI-0063-0001_1  run ipmi command "Get Sensor Threshold"

CONSR-BMC-IPMI-0064-0001
    [Documentation]  This test checks IPMI command: "Set Sensor Event Enables"
    [Tags]     CONSR-BMC-IPMI-0064-0001  tyr  tyr-se  ipmi  Titan-RD  Athena-G2
    [Timeout]  5 min 00 seconds
    Sub-Case  CONSR-BMC-IPMI-0064-0001_1  run ipmi command "Set Sensor Event Enable"

CONSR-BMC-IPMI-0065-0001
    [Documentation]  This test checks IPMI command: "Get Sensor Event Enables"
    [Tags]     CONSR-BMC-IPMI-0065-0001  tyr  tyr-se  ipmi  Titan-RD  Athena-G2
    [Timeout]  5 min 00 seconds
    Sub-Case  CONSR-BMC-IPMI-0065-0001_1  run ipmi command "Get Sensor Event Enable"

CONSR-BMC-IPMI-0066-0001
    [Documentation]  This test checks IPMI command: "Re-arm Sensor Event"
    [Tags]     CONSR-BMC-IPMI-0066-0001  tyr  tyr-se  ipmi  Titan-RD  Athena-G2
    [Timeout]  5 min 00 seconds
    Sub-Case  CONSR-BMC-IPMI-0066-0001_1  run ipmi command "Re-arm Sensor Event"

CONSR-BMC-IPMI-0067-0001
    [Documentation]  This test checks IPMI command: "Get Sensor Event Status"
    [Tags]     CONSR-BMC-IPMI-0067-0001  tyr  tyr-se  ipmi  Titan-RD  Athena-G2
    [Timeout]  5 min 00 seconds
    Sub-Case  CONSR-BMC-IPMI-0067-0001_1  run ipmi command "Get Sensor Event Status"

CONSR-BMC-IPMI-0068-0001
    [Documentation]  This test checks IPMI command: "Get Sensor Reading"
    [Tags]     CONSR-BMC-IPMI-0068-0001  tyr  tyr-se  ipmi  Titan-RD  Athena-G2
    [Timeout]  5 min 00 seconds
    Sub-Case  CONSR-BMC-IPMI-0068-0001_1  run ipmi command "Get Sensor Reading"

CONSR-BMC-IPMI-0069-0001
    [Documentation]  This test checks IPMI command: "Get FRU Inventory Area Info"
    [Tags]     CONSR-BMC-IPMI-0069-0001  tyr  tyr-se  ipmi  Titan-RD  Athena-G2
    [Timeout]  5 min 00 seconds
    Sub-Case  CONSR-BMC-IPMI-0069-0001_1  run ipmi command "Get FRU Inventory Area Info"

CONSR-BMC-IPMI-0070-0001
    [Documentation]  This test checks IPMI command: "Read FRU Data"
    [Tags]     CONSR-BMC-IPMI-0070-0001  tyr  tyr-se  ipmi  Titan-RD  Athena-G2
    [Timeout]  5 min 00 seconds
    Sub-Case  CONSR-BMC-IPMI-0070-0001_1  run ipmi command "Read FRU Data"

CONSR-BMC-IPMI-0071-0001
    [Documentation]  This test checks IPMI command: "Write FRU Data"
    [Tags]     CONSR-BMC-IPMI-0071-0001  tyr  tyr-se  ipmi  Titan-RD  Athena-G2
    [Timeout]  5 min 00 seconds
    Sub-Case  CONSR-BMC-IPMI-0071-0001_1  run ipmi command "Write FRU Data"

CONSR-BMC-IPMI-0074-0001
    [Documentation]  This test checks IPMI command: "Reserve SDR Repository"
    [Tags]     CONSR-BMC-IPMI-0074-0001  tyr  tyr-se  ipmi  Titan-RD  Athena-G2
    [Timeout]  5 min 00 seconds
    Sub-Case  CONSR-BMC-IPMI-0074-0001_1  run ipmi command "Reserve SDR Repository"

CONSR-BMC-IPMI-0075-0001
    [Documentation]  This test checks IPMI command: "Get SDR"
    [Tags]     CONSR-BMC-IPMI-0075-0001  tyr  tyr-se  ipmi  Titan-RD  Athena-G2
    [Timeout]  5 min 00 seconds
    Sub-Case  CONSR-BMC-IPMI-0075-0001_1  run ipmi command "Get SDR"

CONSR-BMC-IPMI-0076-0001
    [Documentation]  This test checks IPMI command: "Partial Add SDR"
    [Tags]     CONSR-BMC-IPMI-0076-0001  tyr  tyr-se  ipmi  Titan-RD  Athena-G2
    [Timeout]  5 min 00 seconds
    Sub-Case  CONSR-BMC-IPMI-0076-0001_1  run ipmi command "Partial Add SDR"

CONSR-BMC-IPMI-0077-0001
    [Documentation]  This test checks IPMI command: "Delete SDR"
    [Tags]     CONSR-BMC-IPMI-0077-0001  tyr  tyr-se  ipmi  Titan-RD  Athena-G2
    [Timeout]  5 min 00 seconds
    Sub-Case  CONSR-BMC-IPMI-0077-0001_1  run ipmi command "Partial Add SDR"
    Sub-Case  CONSR-BMC-IPMI-0077-0001_2  run ipmi command "Delete SDR"

CONSR-BMC-IPMI-0078-0001
    [Documentation]  This test checks IPMI command: "Clear SDR Repository"
    [Tags]     CONSR-BMC-IPMI-0078-0001  tyr  tyr-se  ipmi  Titan-RD  Athena-G2
    [Timeout]  20 min 00 seconds
    [Setup]  prepare BMC images
    Sub-Case  CONSR-BMC-IPMI-0078-0001_1  run ipmi command "Clear SDR Repository"
    [Teardown]  Run Keyword If Test Failed  power cycle OS

CONSR-BMC-IPMI-0081-0001
    [Documentation]  This test checks IPMI command: "Run Initialization Agent"
    [Tags]     CONSR-BMC-IPMI-0081-0001  tyr  tyr-se  ipmi  Titan-RD  Athena-G2
    [Timeout]  5 min 00 seconds
    Sub-Case  CONSR-BMC-IPMI-0081-0001_1  run ipmi command "Run Initialization Agent"

CONSR-BMC-IPMI-0082-0001
    [Documentation]  This test checks IPMI command: "Get SEL Info"
    [Tags]     CONSR-BMC-IPMI-0082-0001  tyr  tyr-se  ipmi  Titan-RD  Athena-G2
    [Timeout]  5 min 00 seconds
    [Setup]  get DUT variables
    Sub-Case  CONSR-BMC-IPMI-0082-0001_1  run ipmi command "Get SEL Info"

CONSR-BMC-IPMI-0083-0001
    [Documentation]  This test checks IPMI command: "Get SEL Allocation Info"
    [Tags]     CONSR-BMC-IPMI-0083-0001  tyr  tyr-se  ipmi  Titan-RD  Athena-G2
    [Timeout]  5 min 00 seconds
    Sub-Case  CONSR-BMC-IPMI-0083-0001_1  run ipmi command "Get SEL Allocation Info"

CONSR-BMC-IPMI-0084-0001
    [Documentation]  This test checks IPMI command: "Reserve SEL"
    [Tags]     CONSR-BMC-IPMI-0084-0001  tyr  tyr-se  ipmi  Titan-RD  Athena-G2
    [Timeout]  5 min 00 seconds
    Sub-Case  CONSR-BMC-IPMI-0084-0001_1  run ipmi command "Reserve SEL"

CONSR-BMC-IPMI-0085-0001
    [Documentation]  This test checks IPMI command: "Get SEL Entry"
    [Tags]     CONSR-BMC-IPMI-0085-0001  tyr  tyr-se  ipmi  Titan-RD  Athena-G2
    [Timeout]  5 min 00 seconds
    [Setup]  get DUT variables
    Sub-Case  CONSR-BMC-IPMI-0085-0001_1  run ipmi command "Get SEL Entry"

CONSR-BMC-IPMI-0086-0001
    [Documentation]  This test checks IPMI command: "Add SEL Entry"
    [Tags]     CONSR-BMC-IPMI-0086-0001  tyr  tyr-se  ipmi  Titan-RD  Athena-G2
    [Timeout]  5 min 00 seconds
    [Setup]  get DUT variables
    Sub-Case  CONSR-BMC-IPMI-0086-0001_1  run ipmi command "Add SEL Entry"

CONSR-BMC-IPMI-0087-0001
    [Documentation]  This test checks IPMI command: "Delete SEL Entry"
    [Tags]     CONSR-BMC-IPMI-0087-0001  tyr  tyr-se  ipmi  Titan-RD  Athena-G2
    [Timeout]  5 min 00 seconds
    [Setup]  get DUT variables
    Sub-Case  CONSR-BMC-IPMI-0087-0001_1  run ipmi command "Delete SEL Entry"

CONSR-BMC-IPMI-0088-0001
    [Documentation]  This test checks IPMI command: "Clear SEL"
    [Tags]     CONSR-BMC-IPMI-0088-0001  tyr  tyr-se  ipmi  Titan-RD  Athena-G2
    [Timeout]  5 min 00 seconds
    Sub-Case  CONSR-BMC-IPMI-0088-0001_1  run ipmi command "Clear SEL"

CONSR-BMC-IPMI-0089-0001
    [Documentation]  This test checks IPMI command: "Get SEL Time"
    [Tags]     CONSR-BMC-IPMI-0089-0001  tyr  tyr-se  ipmi  Titan-RD  Athena-G2
    [Timeout]  5 min 00 seconds
    Sub-Case  CONSR-BMC-IPMI-0089-0001_1  run ipmi command "Get SEL Time"

CONSR-BMC-IPMI-0090-0001
    [Documentation]  This test checks IPMI command: "Set SEL Time"
    [Tags]     CONSR-BMC-IPMI-0090-0001  tyr  tyr-se  ipmi  Titan-RD  Athena-G2
    [Timeout]  5 min 00 seconds
    [Setup]  get DUT variables
    Sub-Case  CONSR-BMC-IPMI-0090-0001_1  run ipmi command "Set SEL Time"

CONSR-BMC-IPMI-0091-0001
    [Documentation]  This test checks IPMI command: "Get SEL Time UTC Offset"
    [Tags]     CONSR-BMC-IPMI-0091-0001  tyr  tyr-se  ipmi  Titan-RD  Athena-G2
    [Timeout]  5 min 00 seconds
    Sub-Case  CONSR-BMC-IPMI-0091-0001_1  run ipmi command "Get SEL Time UTC Offset"

CONSR-BMC-IPMI-0092-0001
    [Documentation]  This test checks IPMI command: "Set SEL Time UTC Offset"
    [Tags]     CONSR-BMC-IPMI-0092-0001  tyr  tyr-se  ipmi  Titan-RD  Athena-G2
    [Timeout]  5 min 00 seconds
    Sub-Case  CONSR-BMC-IPMI-0092-0001_1  run ipmi command "Set SEL Time UTC Offset"

CONSR-BMC-IPMI-0093-0001
    [Documentation]  This test checks IPMI command: "Set LAN Configuration Parameters"
    [Tags]     CONSR-BMC-IPMI-0093-0001  tyr  tyr-se  ipmi  Titan-RD  Athena-G2
    [Timeout]  10 min 00 seconds
    Sub-Case  CONSR-BMC-IPMI-0093-0001_1  run ipmi command "Set LAN Configuration Parameters"

CONSR-BMC-IPMI-0095-0001
    [Documentation]  This test checks IPMI command: "Get LAN Configuration Parameters"
    [Tags]     CONSR-BMC-IPMI-0095-0001  tyr  tyr-se  ipmi  Titan-RD  Athena-G2
    [Timeout]  10 min 00 seconds
    Sub-Case  CONSR-BMC-IPMI-0095-0001_1  run ipmi command "Get LAN Configuration Parameters"
*** Keywords ***
OS Connect Device
    OSConnect

OS Disconnect Device
    OSDisconnect
