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
Documentation       Tests to verify ONL functions described in the ONL function SPEC for the seastone2v2 project.

Variables         ONL_variable.py

Library           ../../whitebox/WhiteboxLibAdapter.py
Library           ../../whitebox/whitebox_lib.py
Library           bios_menu_lib.py
#Library           openbmc_lib.py
Library           ONL_lib.py
Library           ../SEASTONECommonLib.py

Resource          ONL_keywords.robot
Resource          CommonResource.robot

Suite Setup       DiagOS Connect Device
Suite Teardown    DiagOS Disconnect Device



** Variables ***
# It is recommended to use <{ScriptName}|{FeatureName}|{DomainName}_Variable> file for variable declaration with help of
# setting table. This section should keep blank.
#In extreme case if script requires variable then it should be defined in this table with documentaiton tag

# -- Important --
# It is required to set default BIOS Password if not already set to run the below test-cases
# except for CONSR-BIOS-BSST-0012-0001 

*** Test Cases ***

SEASTONE2v2_ONL_TC_00
   [Documentation]   To check if BIOS image has been programmed
   [Tags]     SEASTONE2v2_ONL_TC_00   seastone_bios   test0
  # [Timeout]  20 min 00 seconds
   Step  1  Enter bios now
   Step  2  check bios basic  DUT
   Step  2  exit bios now  DUT 

SEASTONE2v2_ONL_TC_01
   [Documentation]  Verify BIOS Version
   [Tags]     SEASTONE2v2_ONL_TC_01   seastone   test1
   Step  1   Verify BIOS Version

 
SEASTONE2v2_ONL_TC_02
   [Documentation]  Verify BMC Version
   [Tags]     SEASTONE2v2_ONL_TC_02   seastone   test2
   Step  1   Verify BMC Version

SEASTONE2v2_ONL_TC_03
   [Documentation]  Verify ONIE Version
   [Tags]     SEASTONE2v2_ONL_TC_03   seastone   test3
   Step  1   Verify ONIE Version


SEASTONE2v2_ONL_TC_04
   [Documentation]  Verify FPGA Version
   [Tags]     SEASTONE2v2_ONL_TC_04   seastone   test4
   Step  1   Verify FPGA Version

SEASTONE2v2_ONL_TC_05
   [Documentation]  Verify COME CPLD Version
   [Tags]     SEASTONE2v2_ONL_TC_05   seastone   test5
   Step  1   Verify COME CPLD Version


SEASTONE2v2_ONL_TC_06
   [Documentation]  Verify Baseboard CPLD Version
   [Tags]     SEASTONE2v2_ONL_TC_06   seastone   test6
   Step  1   Verify Baseboard CPLD Version


SEASTONE2v2_ONL_TC_07
   [Documentation]  Verify Switch CPLD Version
   [Tags]     SEASTONE2v2_ONL_TC_07   seastone   test7
   Step  1   Verify Switch CPLD Version

SEASTONE2v2_ONL_TC_09
   [Documentation]  Verify ONL booting Check
   [Tags]     SEASTONE2v2_ONL_TC_09   seastone   test9
   Step  1   Verify ONL booting check

SEASTONE2v2_ONL_TC_10
   [Documentation]  Verify ONL login check
   [Tags]     SEASTONE2v2_ONL_TC_10   seastone   test10
   Step  1   Verify ONL Login check

SEASTONE2v2_ONL_TC_11
   [Documentation]  Verify ONL version 
   [Tags]     SEASTONE2v2_ONL_TC_11   seastone   test11
   Step  1   Verify ONL Version

SEASTONE2v2_ONL_TC_12
   [Documentation]  Verify ONL system info check
   [Tags]     SEASTONE2v2_ONL_TC_12   seastone   test12
   Step  1   Verify ONL system info check

SEASTONE2v2_ONL_TC_13
   [Documentation]  This test checks the ONL install or update
   [Tags]  SEASTONE2v2_ONL_TC_13   seastone_ha   test13
   [Timeout]  20 min 00 seconds
   Step  1  Install ONL from ONL and Check

SEASTONE2v2_ONL_TC_14
   [Documentation]  This test checks the install and uninstall of ONL
   [Tags]  SEASTONE2v2_ONL_TC_14   seastone_ha   test14  test8
   [Timeout]  20 min 00 seconds
   Step  1  Uninstall ONL then Install ONL and Check


SEASTONE2v2_ONL_TC_15
   [Documentation]  Verify system info test
   [Tags]     SEASTONE2v2_ONL_TC_15   seastone   test15
   Step  1   Verify system info test

SEASTONE2v2_ONL_TC_16
   [Documentation]  Verify device data test
   [Tags]     SEASTONE2v2_ONL_TC_16   seastone   test16
   Step  1   Verify Device data test

SEASTONE2v2_ONL_TC_17
   [Documentation]  Verify data in json format
   [Tags]     SEASTONE2v2_ONL_TC_17   seastone   test17
   Step  1   Verify data in json format

SEASTONE2v2_ONL_TC_22
   [Documentation]  Verify device OID test
   [Tags]     SEASTONE2v2_ONL_TC_22   seastone   test22
   Step  1   Verify Device OID test 

SEASTONE2v2_ONL_TC_24
   [Documentation]  Verify device SNMP test
   [Tags]     SEASTONE2v2_ONL_TC_24   seastone   test24
   Step  1   Verify Device SNMP test

SEASTONE2v2_ONL_TC_25
   [Documentation]  Verify PSU status
   [Tags]     SEASTONE2v2_ONL_TC_25   seastone   test25
   Step  1   Verify PSU Status

SEASTONE2v2_ONL_TC_26
   [Documentation]  Verify PSU state
   [Tags]     SEASTONE2v2_ONL_TC_26   seastone   test26
   Step  1   Verify PSU State

SEASTONE2v2_ONL_TC_28
   [Documentation]  Verify FAN test
   [Tags]     SEASTONE2v2_ONL_TC_28   seastone   test28
   Step  1   Verify FAN Test

SEASTONE2v2_ONL_TC_29
   [Documentation]  Verify FAN state
   [Tags]     SEASTONE2v2_ONL_TC_29   seastone   test29
   Step  1   Verify FAN State

SEASTONE2v2_ONL_TC_31
   [Documentation]  Verify Thermal Sensor Test
   [Tags]     SEASTONE2v2_ONL_TC_31   seastone   test31
   Step  1   Verify Thermal Sensor Test

SEASTONE2v2_ONL_TC_32
   [Documentation]  Verify Thermal Sensor state
   [Tags]     SEASTONE2v2_ONL_TC_32   seastone   test32
   Step  1   Verify Thermal Sensor State

SEASTONE2v2_ONL_TC_33
   [Documentation]  Verify System LED
   [Tags]     SEASTONE2v2_ONL_TC_33   seastone   test33
   Step  1   Verify System LED

SEASTONE2v2_ONL_TC_34
   [Documentation]  Verify Alarm LED
   [Tags]     SEASTONE2v2_ONL_TC_34   seastone   test34
   Step  1   Verify Alarm LED

SEASTONE2v2_ONL_TC_35
   [Documentation]  Verify PSU LED
   [Tags]     SEASTONE2v2_ONL_TC_35   seastone   test35
   Step  1   Verify PSU LED

SEASTONE2v2_ONL_TC_39
   [Documentation]  Verify Optics present status
   [Tags]     SEASTONE2v2_ONL_TC_39   seastone   test39
   Step  1   Verify Optics present status

SEASTONE2v2_ONL_TC_40
   [Documentation]  Verify TLV eeprom info
   [Tags]     SEASTONE2v2_ONL_TC_40   seastone   test40
   Step  1   Verify TLV EEPROM info

SEASTONE2v2_ONL_TC_41
   [Documentation]  Verify device reset test
   [Tags]     SEASTONE2v2_ONL_TC_41   seastone   test41
   Step  1   Verify device reset test

SEASTONE2v2_ONL_TC_43
   [Documentation]  Verify ONL Stress test
   [Tags]     SEASTONE2v2_ONL_TC_43   seastone   test43
   Step  1   Verify ONL Stress test

*** Keywords ***
DiagOS Connect Device
    DiagOSConnect

DiagOS Disconnect Device
    DiagOSDisconnect
