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
Documentation       Tests to verify BIOS functions described in the BIOS function SPEC for the whiteboxproject.

Variables         BIOS_variable.py

Library           ../../whitebox/WhiteboxLibAdapter.py
Library           ../../whitebox/whitebox_lib.py
#Library           common_lib.py
Library           bios_menu_lib.py
Library           openbmc_lib.py
Library           bios_lib.py
Library           ../EDK2CommonLib.py
#Library           ../diag/GoogleDiagLib.py

Resource          BIOS_keywords.robot
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
CONSR-BIOS-INFO-0004-0001
   [Documentation]   InfoCheck_004_BIOS/OS time sync
   [Tags]   CONSR-BIOS-INFO-0004-0001   Athena-G2

   Step  1   Change System date and time in BIOS
   Step  2   Check date and time is sync with BIOS
   Step  3   Change System date and time in OS
   Step  4   Verify date and time is sync with OS


EDK2_EDKII_Information_Check_TC_03
   [Documentation]   To check if BIOS image has been programmed
   [Tags]     EDK2_EDKII_Information_Check_TC_03   edk2   test3
   [Timeout]  20 min 00 seconds
   [Setup]  AC power device
   #Step  0  enter bios with shell  DUT  ${bios_pass}
   Step  1  check bios basic
   Step  2  exit the shell
   Step  3  check dmidecode bios
   [Teardown]  Run Keyword If Test Failed   chuck it


EDK2_TC_06_ME_Information_Check
   [Documentation]  to check ME image have been programmed successfully.
   [Tags]   EDK2_TC_06_ME_Information_Check  edk2  test6
   [Setup]  AC Power device
   #Step  1  enter bios with shell  DUT  ${bios_pass}
   Step  1  check me config  DUT
   [Teardown]  Run Keyword If Test Failed   chuck it


EDK2_TC_07_RAM_and_UEFI_Volume_SIZE_Check
   [Documentation]  This test checks EDK2 Ram size
   [Tags]   EDK2_TC_07_RAM_and_UEFI_Volume_SIZE_Check   edk2  test7
   [Timeout]  10 mins 
   [Setup]  AC power device
   Step  1  read ram size  DUT
   Step  2  leave bios 
   Step  3  exit the shell


EDK2_TC_08_POST_Information_Test
   [Documentation]  This test checks post information test
   [Tags]  EDK2_TC_08_POST_Information_Test  edk2  test8
   #[Setup]  AC power device
   Step  1  check post info   DUT
   Step  2  exit bios shelll  DUT
   Step  3  exit the shell
   [Teardown]  Run Keyword If Test Failed   chuck it
 

EDK2_TC_09_Build_Linux_Kernel_Check
   [Documentation]   This test checks basic linux version
   [Tags]     EDK2_TC_09_Build_Linux_Kernel_Check    edk2   test9
   Step  1  check uname operations


EDK2_TC_10_Customize_boot_SONiC_test
   [Documentation]   This test checks Customize boot SONiC 
   [Tags]     EDK2_TC_10_Customize_boot_SONiC_test    edk2   test10
   #[Setup]  AC power device
   Step  1  check sonic boot via bios  DUT
   Step  2  check network stats
   [Teardown]  Run Keyword If Test Failed   chuck it

EDK2_TC_21_Boot_Override_Test
    [Documentation]  This test checks boot manager options
    [Tags]  EDK2_TC_21_Boot_Override_Test  edk2  test21
    [Setup]  enter bios now
    Step  1  check boot manager option  DUT
    [Teardown]  Run Keyword If Test Failed   chuck it

EDK2_TEST_TC_23_Fast_boot_test
    [Documentation]  This test checks fast boots
    [Tags]  EDK2_TEST_TC_23_Fast_boot_test   edk2  test23
    Step  1  enter bios now
    Step  2  check fast boot  DUT  Enable  DOWN  2
    Step  3  enter bios now
    Step  3  check fast boot  DUT  Disable  UP  1
    Step  4  enter bios now
    Step  5  check fast boot  DUT  Auto  UP  1
    [Teardown]  Run Keyword If Test Failed   chuck it

EDK2_TC_24_Set_Booting_Time_Out_Test
    [Documentation]  This test checks boot time out
    [Tags]  EDK2_TC_24_Set_Booting_Time_Out_Test  edk2  test24
    [Setup]  power me up
    Step  1  enter bios now
    Step  2  check boottime value  DUT  0
    Step  3  enter bios now
    Step  4  check boottime value  DUT  0  no
    Step  5  enter bios now
    Step  6  check boottime value  DUT  3
    Step  7  enter bios now
    Step  8  check boottime value  DUT  3  no
    Step  9  enter bios now
    Step  10  check boottime value  DUT  27
    Step  11  enter bios now
    Step  12  check boottime value  DUT  27  no
    Step  13  enter bios now
    Step  14  check boottime value  DUT  1
    Step  15  enter bios now
    Step  16  check boottime value  DUT  1  no
    [Teardown]  Run Keyword If Test Failed   chuck it


EDK2_TC_26_CPU_Microcodetest_Test
   [Documentation]   This test checks cpu microcode
   [Tags]   EDK2_TC_26_CPU_Microcodetest_Test  edk2  test26
   Step  1  enter bios now
   Step  2  check the microcode
   [Teardown]  Run Keyword If Test Failed   chuck it


EDK2_TC_27_CPU_P_State_Test
   [Documentation]   This test checks cpu p state
   [Tags]   EDK2_TC_27_CPU_P_State_Test  test27  edk2
   [Setup]  enter bios now
   Step  1  check pstate enable  DUT  KEY_UP
   Step  2  check lscpu
   Step  3  enter bios now
   Step  4  check pstate enable  DUT  KEY_DOWN
   Step  5  check lscpu


EDK2_TC_28_Hyper_Thread_Function_Test
   [Documentation]   This test checks hyper thread function
   [Tags]   EDK2_TC_28_Hyper_Thread_Function_Test edk2  test28
   [Setup]  powercycle to bios  DUT  no  ${bios_pass}
   Step  1  check hyper thread  DUT  KEY_UP 
   Step  2  check cpui info  8
   Step  3  enter bios now
   Step  4  check hyper thread  DUT  KEY_DOWN
   Step  5  check cpui info  16
   [Teardown]  Run Keyword If Test Failed   chuck it 


EDK2_BIOS_TC_39_MicroSD_card_Detect_Test
   [Documentation]   This test will detect microsd
   [Tags]  EDK2_BIOS_TC_39_MicroSD_card_Detect_Test  edk2  test39
   [Setup]  enter bios now
   Step  1  check microsd   DUT
   Step  2  convert sd to onie
   Step  3  enter bios now
   Step  4  check microsd   DUT
   [Teardown]  Run Keyword If Test Failed   chuck it

EDK2_TEST_TC_42_Serial_Port_Address_Check
   [Documentation]  This test checks  serial port address
   [Tags]    edk2  test42  EDK2_TEST_TC_42_Serial_Port_Address_Check
   Step  1  check port address  DUT


EDK2_TC_44_Read_EEPROM_Test
   [Documentation]   This test checks eeprom data
   [Tags]  EDK2_TC_44_Read_EEPROM_Test  edk2  test44
   Step  1  check eeprom tlv  


EDK2_TEST_TC_47_S0_State_Test
   [Documentation]   This test checks  S0 state test
   [Tags]   EDK2_TEST_TC_47_S0_State_Test  edk2  test47
   Step  1  check coverage  58



EDK2_TEST
   [Documentation]  MOCK test
   [Tags]   mock 
   [Setup]  enter bios now 
   #Step  1  remove bios pass  DUT
   #Step  2  enter bios now
   Step  2  create pass  DUT  admin  1



EDK2_TEST
   [Documentation]  MOCK test
   [Tags]   stock
   Step  1  power me up  

EDK2_TEST
   [Documentation]  MOCK test
   [Tags]   hello
   Step  1  check us  DUT
   [Teardown]  danger sign


EDK2_TEST_TC_58_Administrator_Password_Test
   [Documentation]  This test checks for password settings
   [Tags]   EDK2_TEST_TC_58_Administrator_Password_Test   edk2  test58
   [Timeout]  30 mins 00 seconds
   [Setup]  enter bios now
   Step  1  remove bios pass  DUT  ${bios_pass} 
   Step  2  enter bios now
   Step  3  create pass  DUT  admin  1
   Step  4  enter bios now
   Step  5  change bios password  DUT  admin  1
   Step  6  check system halt  DUT
   Step  7  remove bios pass  DUT  ${new_bios_pass}
   Step  8  enter bios now
   Step  9  create pass  DUT  admin  1  
   [Teardown]  Run Keyword If Test Failed   chuck it


EDK2_TEST_TC_59_User_Password_Test
   [Documentation]  This test checks for password settings
   [Tags]   EDK2_TEST_TC_59_User_Password_Test   edk2  test59
   [Timeout]  30 mins 00 seconds
   [Setup]  enter bios now
   Step  1  create pass  DUT  user  3
   Step  4  enter bios as user
   Step  5  change bios password  DUT  user  3
   Step  6  check system halt user   DUT
   Step  7  exit bios shelll  DUT
   Step  8  exit the shell
   [Teardown]  Run Keyword If Test Failed   chuck it


EDK2_TC_60_Access_Level_Test
   [Documentation]    This test checks bios access level
   [Tags]   EDK2_TC_60_Access_Level_Test  edk2  test60
   [Setup]  enter bios now
   Step  1  create pass  DUT  user  3
   Step  2  enter bios as user
   Step  3  check access level  DUT  User
   Step  4  enter bios now
   Step  5  check access level  DUT  Administrator
   [Teardown]  Run Keyword If Test Failed   chuck it


EDK2_TEST_TC_61_Power_Control_Check
    [Documentation]  This test checks power control
    [Tags]  edk2  test61  EDK2_TEST_TC_61_Power_Control_Check
    Step  1  reboot to sonic
    Step  2  check power off 
    Step  3  check watch dog  DUT
    Step  4  check diff reboot  DUT


EDK2_TC_62_Setup_Menu_Check
   [Documentation]   This test checks bios and cpu inf
   [Tags]  EDK2_TC_62_Setup_Menu_Check  edk2  test62
   [Setup]  powercycle to bios  DUT  no  ${bios_pass}
   Step  1  check cpu info  DUT


EDK2_TEST_TC_63_EDKII_Menu_Check
   [Documentation]  This test checks EDK2 menu
   [Tags]  edk2  test63   EDK2_TEST_TC_63_EDKII_Menu_Check
   Step  1  check coverage  58


EDK2_TC_64_Boot_Manager_Menu_Check
   [Documentation]   This test checks bios boot manager options
   [Tags]   EDK2_TC_64_Boot_Manager_Menu_Check   edk2  test64
   [Setup]  powercycle to bios  DUT  no  ${bios_pass}
   Step  1  check boot manager  DUT
   [Teardown]  Run Keyword If Test Failed   chuck it


EDK2_TEST_TC_65_Boot_Maintenance_Manager_Menu_Check
   [Documentation]  This test checks boot maintenance menu options
   [Tags]  EDK2_TEST_TC_65_Boot_Maintenance_Manager_Menu_Check  edk2  test65
   [Setup]  enter bios now
   Step  1  check boottime value  DUT  20
   Step  2  enter bios now
   Step  3  check boottime value  DUT  20  no 
   Step  4  power me up
   [Teardown]  Run Keyword If Test Failed   chuck it

EDK2_TEST_TC_66_Continue_and_Reset_Menu_Check
   [Documentation]  This test checks boot maintenance menu options
   [Tags]  EDK2_TEST_TC_66_Continue_and_Reset_Menu_Check  edk2  test66
   [Setup]  enter bios now
   Step  1  check boottime value  DUT  8 
   Step  2  enter bios now
   Step  3  check boottime value  DUT  8  no
   [Teardown]  Run Keyword If Test Failed   chuck it



EDK2_TEST_TC_67_AC_Power_Cycling_Stress
   [Documentation]  This test checks basic scans
   [Tags]  EDK2_TEST_TC_67_AC_Power_Cycling_Stress  edk2  test67
   FOR    ${INDEX}    IN RANGE    1   10
      Step  1  check scans  DUT
      Step  2  EDK2CommonLib.Powercycle Device   DUT  yes
   END


EDK2_TEST_TC_68_CPU_Warm_Reset_Stress_Test
   [Documentation]  This test checks basic scans
   [Tags]   EDK2_TEST_TC_68_CPU_Warm_Reset_Stress_Test  edk2  test68
   FOR    ${INDEX}    IN RANGE    1   20
      Step  1  check scans  DUT
      Step  2  reboot to sonic
   END

EDK2_TEST_TC_69_CPU_I2C_Scan_Stress_Test
   [Documentation]  This test checks basic i2c scans over night
   [Tags]   EDK2_TEST_TC_69_CPU_I2C_Scan_Stress_Test  edk2  test69
   FOR    ${INDEX}    IN RANGE    1   50
      Step  1  scan i2c
   END


EDK2_TEST_TC_70_Memory_Stressapp_Test
   [Documentation]  This test checks  Memory/CPU/SATA Stressapp Test
   [Tags]   EDK2_TEST_TC_70_Memory_Stressapp_Test  edk2  test70
   [Timeout]  700 mins 00 seconds
   Step  1  verify home path
   Step  2  check memory
   Step  3  check stress help
   Step  4  check memory



EDK2_TEST_TC_74_System_Stress_Test
   [Documentation]  This test checks  system stress test
   [Tags]  EDK2_TEST_TC_74_System_Stress_Test  edk2  test74
   FOR    ${INDEX}    IN RANGE    1   50
      Step  0   enter bios now
      Step  1   check system stress  DUT
   END
   [Teardown]  Run Keyword If Test Failed   chuck it 




EDK2_TEST_TC_48_S5_State_Test
   [Documentation]   This test checks  S0 state test
   [Setup]  power me up
   [Tags]   EDK2_TEST_TC_48_S5_State_Test  edk2   test48
   Step  1  check ospf


EDK2_TEST_TC_AC_Power_Cycling_Stress
   [Documentation]  This test checks basic scans
   [Tags]  EDK2_TEST_TC_67_AC_Power_Cycling_Stress  edk2  mtp
   FOR    ${INDEX}    IN RANGE    1   2
     # Step  2  EDK2CommonLib.Powercycle Device   DUT  yes
      Run Keyword And Continue On Failure  check scans  DUT
   END


EDK2_TEST_TC_53_SMBIOS_Table_Read
   [Documentation]   This test checks SMBIOS Table
   [Tags]   EDK2_TEST_TC_53_SMBIOS_Table_Read  edk2   test53
   Step  1  check cli bios

EDK2_TEST_TC_40_MicroSD_card_RW_Test
   [Documentation]   This test checks microsd  RW
   [Tags]    EDK2_TEST_TC_40_MicroSD_card_RW_Test  edk2  test40
   Step  1   check micro operations  DUT


EDK2_TEST_TC_34_CPU_I2C_SMBus_SMLink_Interface_Test
   [Documentation]   This test checks CPU I2C/SMBus/SMLink Interface Test
   [Tags]    EDK2_TEST_TC_34_CPU_I2C_SMBus_SMLink_Interface_Test  edk2  test34
   Step  1  check cpu bus  DUT

EDK2_TEST_TC_35_CPU_LPC_Interface_Test
   [Documentation]   This test checks lpu interface
   [Tags]  EDK2_TEST_TC_35_CPU_LPC_Interface_Test  edk2  test35
   [Setup]  power me up
   Step  1  check lpc interface  DUT



EDK2_TEST_TC_36_Management_Port_Information_Check
   [Documentation]   This test checks  Management Port Information Check
   [Tags]  edk2  test36   EDK2_TEST_TC_36_Management_Port_Information_Check
   Step  1  check mgmt info  DUT
   



EDK2_TEST_TC_30_Memory_Frequency_Check
   [Documentation]   This test checks Memory Frequency Check
   [Tags]  edk2   EDK2_TEST_TC_30_Memory_Frequency_Check  test30
   [Setup]   AC power device
   Step  1  check freq   DUT



EDK2_TEST_TC_31_PCIE_Bus_Scan
   [Documentation]  This test checks PCIE Bus Scan
   [Tags]  EDK2_TEST_TC_31_PCIE_Bus_Scan  edk2  test31
   Step  1  check pcie  DUT

EDK2_TEST_TC_25_CPU_information_test
   [Documentation]  This test checks  CPU information test
   [Tags]     [Tags]  EDK2_TEST_TC_25_CPU_information_test  edk2  test25
   [Setup]  enter bios now
   Step  1  check info cpu  DUT  0
   Step  2  enter bios now
   Step  3  check info cpu  DUT  3FFE  yes
   Step  4  enter bios now
   Step  5  check info cpu  DUT  0  yes
   [Teardown]  Run Keyword If Test Failed   chuck it

EDK2_TEST_TC_32_PCIE_Configuration_Test
   [Documentation]  This test checks  PCIE Configuration Test
   [Tags]  EDK2_TEST_TC_32_PCIE_Configuration_Test  edk2  test32
   Step  1  enter bios now
   Step  2  check iio config  DUT
   Step  3  try pch  DUT
   Step  4  check pcie conf  DUT
   [Teardown]  Run Keyword If Test Failed   chuck it


EDK2_TEST_TC_49_ACPI_Setting_Test
   [Documentation]  This test checks ACPI Setting Test
   [Tags]  EDK2_TEST_TC_49_ACPI_Setting_Test  edk2  test49
   Step  1   check acpi test  DUT




EDK2_TEST_TC_52_10GbE_SFP+_Interface_Test
    [Documentation]   This test checks 10GbE: SFP+ Interface Test
    [Tags]  EDK2_TEST_TC_52_10GbE_SFP+_Interface_Test  edk2  test52
    Step  1   check sfp interface  DUT



EDK2_TEST_TC_68_CPU_Warm_Reset_Stress_Test
   [Documentation]  This test checks basic scans
   [Tags]   EDK2_TEST_TC_68_CPU_Warm_Reset_Stress_Test  edk2  test68os
   FOR    ${INDEX}    IN RANGE    1   3
      Step  1  check scans  DUT
      Step  2  reboot without shell
   END


EDK2_TEST_TC_69_CPU_I2C_Scan_Stress_Test
   [Documentation]  This test checks basic i2c scans over night
   [Tags]   EDK2_TEST_TC_69_CPU_I2C_Scan_Stress_Test  edk2  test69os
   FOR    ${INDEX}    IN RANGE    1   500
      Step  1  scan i2c
      Step  2  check cpu bus  DUT  
   END



EDK2_TEST_CHOPPER_System_Stress_Test
   [Documentation]  This test checks  system stress test
   [Tags]  EDK2_TEST_CHOPPER_System_Stress_Test  edk2  chopper
   FOR    ${INDEX}    IN RANGE    1   200
      Step  0   enter bios now
      Step  1   check chopper stress  DUT
   END
   #[Teardown]  Run Keyword If Test Failed   chuck it




*** Keywords ***
DiagOS Connect Device
    DiagOSConnect

DiagOS Disconnect Device
    DiagOSDisconnect
