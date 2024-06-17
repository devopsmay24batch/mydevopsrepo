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
Documentation       Tests to verify ONL functions described in the ONL function SPEC for the moonstone project.

Variables         ONL_variable.py

Library           ../../whitebox/WhiteboxLibAdapter.py
Library           ../../whitebox/whitebox_lib.py
Library           bios_menu_lib.py
Library           ONL_lib.py
Library           ../MOONSTONECommonLib.py

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

MOONSTONE_ONL_TC_00
   [Documentation]   To check if BIOS image has been programmed
   [Tags]     MOONSTONE_ONL_TC_00   moonstone   test0  done
   Step  1  Enter bios now
   Step  2  check bios basic  DUT
   Step  2  exit bios now  DUT 

MOONSTONE_ONL_TC_01
   [Documentation]  Verify BIOS Version
   [Tags]     MOONSTONE_ONL_TC_01   moonstone   test1  done
   Step  1   Verify BIOS Version

MOONSTONE_ONL_TC_02
   [Documentation]  Verify BMC Version
   [Tags]     MOONSTONE_ONL_TC_02   moonstone   test2  done
   Step  1   Verify BMC Version

MOONSTONE_ONL_TC_03
   [Documentation]  Verify ONIE Version
   [Tags]     MOONSTONE_ONL_TC_03   moonstone   test3  done
   Step  1   Verify ONIE Version

MOONSTONE_ONL_TC_04
   [Documentation]  Verify FPGA Version
   [Tags]     MOONSTONE_ONL_TC_04   moonstone   test4  done
   Step  1   Verify FPGA Version

MOONSTONE_ONL_TC_05
   [Documentation]  Verify COME CPLD Version
   [Tags]     MOONSTONE_ONL_TC_05   moonstone   test5  done
   Step  1   Verify COME CPLD Version

MOONSTONE_ONL_TC_06
   [Documentation]  Verify Baseboard CPLD Version
   [Tags]     MOONSTONE_ONL_TC_06   moonstone   test6  done
   Step  1   verify_baseboard_cpld_version  DUT

MOONSTONE_ONL_TC_07
   [Documentation]  Verify Switch CPLD Version
   [Tags]     MOONSTONE_ONL_TC_07   moonstone   test7  done
   Step  1   Verify Switch CPLD Version

MOONSTONE_ONL_TC_09
   [Documentation]  Verify ONL booting Check
   [Tags]     MOONSTONE_ONL_TC_09   moonstone   test9  done
   Step  1   Verify ONL booting check

MOONSTONE_ONL_TC_10
   [Documentation]  Verify ONL login check
   [Tags]     MOONSTONE_ONL_TC_10   moonstone   test10  done
   Step  1   Verify ONL Login check

MOONSTONE_ONL_TC_11
   [Documentation]  Verify ONL version 
   [Tags]     MOONSTONE_ONL_TC_11   moonstone   test11  done
   Step  1   verify_onl_version  DUT

MOONSTONE_ONL_TC_12
   [Documentation]  Verify ONL system info check
   [Tags]     MOONSTONE_ONL_TC_12   moonstone   test12  done
   Step  1   verify_onl_system_info_check  DUT

MOONSTONE_ONL_TC_13
   [Documentation]  This test checks the ONL install or update
   [Tags]  MOONSTONE_ONL_TC_13   moonstone   test13  done
   Step  1  Install ONL from ONL and Check

MOONSTONE_ONL_TC_14
   [Documentation]  This test checks the install and uninstall of ONL
   [Tags]  MOONSTONE_ONL_TC_14   moonstone   test14  test8  done 
   Step  1  Uninstall ONL then Install ONL and Check

MOONSTONE_ONL_TC_16
   [Documentation]  Verify device data test
   [Tags]     MOONSTONE_ONL_TC_16   moonstone   test16  done
   Step  1   verify_device_data  DUT

MOONSTONE_ONL_TC_15
   [Documentation]  Verify system info test
   [Tags]     MOONSTONE_ONL_TC_15   moonstone   test15  done
   Step  1   Verify system info test

MOONSTONE_ONL_TC_17
   [Documentation]  Verify data in json format
   [Tags]     MOONSTONE_ONL_TC_17   moonstone   test17  done
   Step  1   Verify data in json format

MOONSTONE_ONL_TC_18
   [Documentation]  Verify platform management daemon function driver
   [Tags]     MOONSTONE_ONL_TC_18   moonstone   test18  done
   Step  1   Verify platform management daemon function driver

MOONSTONE_ONL_TC_19
   [Documentation]  Verify SYSFS Interface
   [Tags]     MOONSTONE_ONL_TC_19   moonstone   test19  done
   Step  1   Verify SYSFS Interface 

MOONSTONE_ONL_TC_20
   [Documentation]  Verify SFP SYSFS
   [Tags]     MOONSTONE_ONL_TC_20   moonstone   test20  done
   Step  1   Verify SFP SYSFS

MOONSTONE_ONL_TC_21
   [Documentation]  Verify OSFP SYSFS
   [Tags]     MOONSTONE_ONL_TC_21   moonstone   test21  done
   Step  1   Verify OSFP SYSFS 

MOONSTONE_ONL_TC_22
   [Documentation]  Verify device OID test
   [Tags]     MOONSTONE_ONL_TC_22   moonstone   test22  done
   Step  1   Verify Device OID test  DUT

MOONSTONE_ONL_TC_23
   [Documentation]  Verify Device SYS OID Test
   [Tags]     MOONSTONE_ONL_TC_23   moonstone   test23  done
   Step  1   Verify Device SYS OID Test  DUT

MOONSTONE_ONL_TC_24
   [Documentation]  Verify device SNMP test
   [Tags]     MOONSTONE_ONL_TC_24   moonstone   test24  done
   Step  1   Verify Device SNMP test

MOONSTONE_ONL_TC_25
   [Documentation]  Verify PSU test
   [Tags]     MOONSTONE_ONL_TC_25   moonstone   test25  done
   Step  1   Verify PSU Test

MOONSTONE_ONL_TC_28
   [Documentation]  Verify FAN test
   [Tags]     MOONSTONE_ONL_TC_28   moonstone   test28  done
   Step  1   Verify FAN Test

MOONSTONE_ONL_TC_31
   [Documentation]  Verify Thermal Sensor Test
   [Tags]     MOONSTONE_ONL_TC_31   moonstone   test31  done
   Step  1   Verify Thermal Sensor Test

MOONSTONE_ONL_TC_33
   [Documentation]  Verify System LED
   [Tags]     MOONSTONE_ONL_TC_33   moonstone   test33  done
   Step  1   Verify System LED

MOONSTONE_ONL_TC_34
   [Documentation]  Verify Alarm LED
   [Tags]     MOONSTONE_ONL_TC_34   moonstone   test34  done
   Step  1   Verify Alarm LED

MOONSTONE_ONL_TC_40
   [Documentation]  Verify TLV eeprom info
   [Tags]     MOONSTONE_ONL_TC_40   moonstone   test40  done
   Step  1   Verify TLV EEPROM info

MOONSTONE_ONL_TC_41
   [Documentation]  Verify device reset test
   [Tags]     MOONSTONE_ONL_TC_41   moonstone   test41  done
   Step  1   Verify device reset test

MOONSTONE_ONL_TC_43
   [Documentation]  Verify ONL Stress test
   [Tags]     MOONSTONE_ONL_TC_43   moonstone   test43  done
   Step  1   Verify ONL Stress test

*** Keywords ***
DiagOS Connect Device
    DiagOSConnect

DiagOS Disconnect Device
    DiagOSDisconnect
