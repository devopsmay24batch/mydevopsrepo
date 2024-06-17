###############################################################################
# LEGALESE:   "Copyright (C) 2019-2021, Celestica Corp. All rights reserved." #
#                                                                             #
# This source code is confidential, proprietary, and contains trade           #
# secrets that are the sole property of Celestica Corp.                       #
# Copy and/or distribution of this source code or disassembly or reverse      #
# engineering of the resultant object code are strictly forbidden without     #
# the written consent of Celestica Corp.                                      #
#                                                                             #
###############################################################################

*** Settings ***
Documentation       This Suite will vGoogledate Sonic package

Library           GoogleSonicLib.py
Library           ../EDK2CommonLib.py
Library           CommonLib.py
Library           ../diag/GoogleDiagLib.py
Variables         ../GoogleCommonVariable.py
Variables         GoogleSonicVariable.py

Resource          GoogleSonicKeywords.resource
Resource	  CommonKeywords.resource

Suite Setup       Connect Device
Suite Teardown    Disconnect Device

*** Variables ***


*** Test Cases ***


EDK2_SONIC_TC_test
    [Documentation]  This test checks SONiC Login Test
    [Tags]    EDK2_SONIC_TC_07_SONiC_Login_Check_Test  reboot
    FOR    ${INDEX}    IN RANGE    1   5
        Step  1  diagos login check
    END



EDK2_SONIC_Power_test
    [Documentation]  This test checks powercycles
    [Tags]    cycle   EDK2_SONIC_Power_test
    FOR    ${INDEX}    IN RANGE    1   101
        Step  1  check power mtp
    END
    Step  2  login check


EDK2_SONIC_Power_test_Brixia
    [Documentation]  This test checks powercycles
    [Tags]    cycle1   EDK2_SONIC_Power_test_Brixia
    FOR    ${INDEX}    IN RANGE    1   3
        Step  1  check power brixia 
    END
    Step  2  login check





EDK2_SONIC_TC_07_SONiC_Login_Check_Test
    [Documentation]  This test checks SONiC Login Test
    [Tags]    EDK2_SONIC_TC_07_SONiC_Login_Check_Test  edk2  test7
    [Timeout]  10 min 00 seconds
    Step  1  diagos login check

EDK2_SONIC_TC_08_SONiC_Version_Check
    [Documentation]  This test checks SONiC version
    [Tags]    EDK2_SONIC_TC_08_SONiC_Version_Check  edk2  test8
    [Timeout]  10 min 00 seconds
    Step  1  check sonic version  ${show_version_cmd}  ${show_boot_cmd}  ${uname_cmd}  


EDK2_SONIC_TC_09_SONiC_Booting_info_Check
    [Documentation]  This test checks SONiC booting info
    [Tags]    EDK2_SONIC_TC_09_SONiC_Booting_info_Check  edk2  test9
    [Timeout]  6 min 00 seconds
    Step  1  sonic_booting_info_check  ${coreboot_release_date}


EDK2_SONIC_TC_011_Dependent_Software_Version_Check
    [Documentation]  This test check dependent software version
    [Tags]    EDK2_SONIC_TC_011_Dependent_Software_Version_Check  edk2  test11
    [Timeout]  10 min 00 seconds
    Step  1  check dependent software  ${diag_SW}  ${sdk_SW}
    Step  2  check software version

EDK2_SONIC_TC_012_CPLD_FPGA_Register_Access_Check
     [Documentation]  This test checks CPLD and FPGA register access
     [Tags]    EDK2_SONIC_TC_012_CPLD_FPGA_Register_Access_Check  test12
     [Timeout]  15 min 00 seconds
     step  1  COMe CPLD register access
     step  2  MMc CPLD register access
     step  3  FPGA register access

 EDK2_SONIC_TC_014_Hardware_Interface_Access_Scan_Check
    [Documentation]  This case test hardware details
    [Tags]    EDK2_SONIC_TC_014_Hardware_Interface_Access_Scan_Check  test14  edk2
    [Timeout]  15 min 00 seconds
    step  1  check platform
    step  2  check cpu info
    step  3  check memory info
    step  4  scan i2c device
    step  5  scan pcie device
    step  6  check storage device
    step  7  check mgmt port


EDK2_SONIC_TC_15_TLV_EEPROM_Info
    [Documentation]  This case verifies eeprom erase read write
    [Tags]    EDK2_SONIC_TC_15_TLV_EEPROM_Info  test15  edk2
    [Timeout]  20 min 00 seconds
   # step  1  tlv eeprom from diag cmd
   # step  2  tlv eeprom from sonic cmd
   # step  3  erase and program tlv eeprom
    step  4  tlv eeprom failover check

EDK2_SONIC_TC_28_Warm-boot_Reset_Stress_Test
    [Documentation]  This test needs to scan all drivers and disks
    [Tags]  EDK2_SONIC_TC_28_Warm-boot_Reset_Stress_Test  testing  test28  edk2
    [Setup]  check sdb
    [Timeout]  30 min 00 seconds
    Step  1  warm boot reset stress test
        
EDK2_SONIC_TC_29_Watchdog_Reset_Stress_Test
    [Documentation]  This test run the WDT Reset in Sonic
    [Tags]  EDK2_SONIC_TC_29_Watchdog_Reset_Stress_Test  test29
    [Timeout]  20 min 00 seconds
    [Setup]  check sdb
    Step  1  WDT reset stress test

EDK2_SONIC_TC_016_OSFP_SFP+_Port_EEPROM_Info_Check
     [Documentation]  This test checks OSFP SFP+ eeprom Info check
     [Tags]    EDK2_SONIC_TC_016_OSFP_SFP+_Port_EEPROM_Info_Check  test16
     [Timeout]  15 min 00 seconds
     step  1  check osfp port eeprom info
     step  2  check sfp plus port eeprom info
     
# two steps are manual steps, skipped in this test case
EDK2_SONIC_TC_017_Temperature_Sensors_check
     [Documentation]  This test check the temp range
	 [Tags]    EDK2_SONIC_TC_017_Temperature_Sensors_check  test17
	 [Timeout]  15 min 00 seconds
	 step  1  temp sensor check 

# two steps are manual steps, skipped in this test case
EDK2_SONIC_TC_018_Voltage_Sensors_check
     [Documentation]  This case checks the voltage sensors
     [Tags]    EDK2_SONIC_TC_018_Voltage_Sensors_check  test18
     [Timeout]  15 min 00 seconds
     step  1  COMe baseboard powerbrick sensor check
     step  2  check ADM1266 sensor via both FPGA and CPLD
     step  3  switch adm1266 to baseboard cpld 
     step  4  switch adm1266 to fpga pmbus
     step  5  check switchboard sensors

EDK2_SONIC_TC_020_Fan_Speed_Control_Test
     [Documentation]  This case check fan speed control
	 [Tags]    EDK2_SONIC_TC_020_Fan_Speed_Control_Test   test20
	 [Timeout]  15 min 00 seconds
     step  1  Fan speed control

EDK2_SONIC_TC_023_WDT_Service_Check
     [Documentation]  This Test checks WDT service
	 [Tags]    EDK2_SONIC_TC_023_WDT_Service_Check  test23
	 [Timeout]  15 min 00 seconds
     step  1  Powercycle and restart wdt service
	 step  2  inspect wdt service
	 step  3  stop wdt service and check system is stable
	 step  4  inspect wdt after service stopped and start service
	 step  5  check status kill the service and check system reset
	 step  6  recheck wdt steps 2 to 4
	 step  7  restart wdt and repeat step 5

EDK2_SONIC_TC_030_EEPROM_stress_test
     [Documentation]  eeprom stress test
     [Tags]    EDK2_SONIC_TC_030_EEPROM_stress_test  edk2  test30
     ${loop_count}  Set Variable  ${200}
	 FOR  ${each}  IN RANGE  ${loop_count}
		  LOG TO CONSOLE  ------------------------ LOOP No. ${each+1} out of ${loop_count} ------------------------
	      step  1  check osfp port eeprom info
		  step  2  check sfp plus port eeprom info
		  step  3  tlv eeprom from diag cmd
                  step  4  tlv eeprom from sonic cmd
	 END
	 step  4  check storage device


EDK2_SONIC_TC_032_I2C_Scan_Stress_Test
    [Documentation]  i2c scan stress test
    [Tags]    EDK2_SONIC_TC_032_I2C_Scan_Stress_Test  edk2  test32
    [Timeout]  40 min 00 seconds
	${loop_count}  Set Variable  ${20}
	FOR  ${i}  IN RANGE  ${loop_count}
		LOG TO CONSOLE  ------------------------ LOOP No. ${i+1} out of ${loop_count} ------------------------
	    step  1  i2cstress test
	END
	step  2  check device stability

EDK2_SONIC_TC_03_Installation_uninstallation_Second_Sonic_os
    [Documentation]   Install and uninstall the second sonic os
       [Tags]    EDK2_SONIC_TC_03_Installation_uninstallation_Second_Sonic_os  brixia
       [Timeout]  35 min 00 seconds
       step  1  install second os  ${old_os} 
       step  2  uninstall unused os version  ${new_os}
       step  3  install second os  ${new_os}
       step  4  uninstall unused os version  ${old_os}

EDK2_SONIC_TC_04_Update_SONiC_Image_When_Have_Two_SONiC_OS_Test
    [Documentation]  This test is used to prepare three images and update them
    [Tags]  EDK2_SONIC_TC_04_Update_SONiC_Image_When_Have_Two_SONiC_OS_Test
    [Timeout]  80 min 00 seconds
    Step  1  Downgrade SONiC Via Current Version
    Step  2  Upgrade SONiC Via Current Version
    Step  3  Upgrade SONiC Via Current Version2
    Step  4  Downgrade Current to Older Version
    Step  5  Upgrade Older to Current Version
   
 
#step 8 is not working so skipped the that step
EDK2_SONIC_TC_06_Boot_SONiC_From_uSD_Card
    [Documentation]  This test installs various parted commands and resize sd card
    [Tags]  EDK2_SONIC_TC_06_Boot_SONiC_From_uSD_Card
    [Timeout]  30 min 00 seconds
    Step  1  boot Sonic from Usd
    Step  2  Expand SD Card

EDK2_SONIC_TC_27_Update_And_Identify_Coreboot_By_H1_Tool
    [Documentation]  This test is used to update and identify Coreboot
    [Tags]  EDK2_SONIC_TC_27_Update_And_Identify_Coreboot_By_H1_Tool  test27
    [Timeout]  50 min 00 seconds
    Step  1  DiagOS Login Check
    Step  2  Identify Coreboot Image
    Step  3  Update Coreboot Image
    Step  4  Check Crypt Id


EDK2_SONIC_TC_02_Update_SONiC_Image_When_have_1_SONiC_OS_Test
    [Documentation]  This test needs to install and uninstall 1 Sonic OS
    [Tags]  EDK2_SONIC_TC_02_Update_SONiC_Image_When_have_1_SONiC_OS_Test   
    [Timeout]  30 min 00 seconds
    Step  1  DiagOS Login Check
    Step  2  Check Sonic Version  ${show_version_cmd}  ${show_boot_cmd}
    Step  3  Downgrade Upgrade Sonic Image
    Step  4  Check Update Driver Status

EDK2_SONIC_TC_01_Installation/Uninstallation_First_SONIC_OS
    [Documentation]  This test used to install and uninstall Sonic Image
    [Tags]  EDK2_SONIC_TC_01_Installation/Uninstallation_First_SONIC_OS
    [Timeout]  50 min 00 seconds
    Step  1  DiagOS Login Check
    Step  2  Upgrade Sonic Image
    Step  3  Check Update Driver Status
    Step  4  Uninstall First Sonic  
    Step  5  Lower Sonic Image
    Step  6  Check Update Driver Status

#AC power off step is manual 
EDK2_SONIC_TC_05_Uninstallation_All_SONIC_OS
    [Documentation]  This device will uninstall Sonic OS Label
    [Tags]  EDK2_SONIC_TC_05_Uninstallation_All_SONIC_OS
    [Timeout]  30 min 00 seconds
    Step  1  DiagOS Login Check
    Step  2  show two Sonic
    Step  3  check Sonic Version  ${show_version_cmd}  ${show_boot_cmd}
    Step  4  Uninstall Lower Sonic
    Step  5  check block Device
    Step  6  Uninstall All Sonic
    Step  7  check block Device

EDK2_SONIC_TC_90
    [Documentation]  This device will uninstall Sonic OS Label
    [Tags]  EDK2_SONIC_TC_05_Uninstallation_All_SONIC_OS  newtest
    [Timeout]  30 min 00 seconds
    Step  1  check sdb




EDK2_SONIC_POWER
   [Documentation]   This test checks power cycle
    [Tags]   brixia123
    FOR    ${INDEX}    IN RANGE    1   501
       Step  1  AC power device
    END
    Step  2  login check

*** Keywords ***
Connect Device
    Login Device

Disconnect Device
    Sonic Disconnect
