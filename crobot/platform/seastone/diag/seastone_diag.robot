###############################################################################
# LEGALESE:   "Copyright (C) 2020-      Celestica Corp. All rights reserved." #
#                                                                             #
# This source code is confidential, proprietary, and contains trade           #
# secrets that are the sole property of Celestica Corp.                       #
# Copy and/or distribution of this source code or disassembly or reverse      #
# engineering of the resultant object code are strictly forbidden without     #
# the written consent of Celestica Corp.                                      #
#                                                                             #
###############################################################################

*** Settings ***
Documentation   SEASTONE common diagnostic suite
Resource        CommonKeywords.resource
Resource        SeastoneDiagKeywords.resource
Library         SeastoneDiagLib.py
Library         CommonLib.py
Library         ../SEASTONECommonLib.py
Variables       SeastoneDiagVariable.py


Suite Setup   DIAG OS Connect Device
Suite Teardown  DIAG OS Disconnect Device

*** Test Cases ***


SEASTONE_V2_TC_POWER
   [Documentation]  This test will check power cycle
   [Tags]  SEASTONE_V2_TC_POWER  seastone  power
   [Setup]  power cycle test
   Step  1  go to diag path




SEASTONE_V2_TC_CHECK_PROMPT
   [Documentation]  This test will checks prompt
   [Tags]  SEASTONE_V2_TC_POWER  seastone  prompt
   #[Setup]  power cycle test
   Step  1  check diag basic  DUT





SEASTONE2_V2_DIAG_TC_17_QSFP_TEMP_TEST
   [Documentation]  This test checks qsfp temp test
   [Tags]  SEASTONE2_V2_DIAG_TC_17_QSFP_TEMP_TEST  seastone  test17  stat
   Step  1  go to diag path
   Step  2  check help  ${qsfp}
   Step  3  check qsfp temp

SEASTONE2_V2_DIAG_TC_18_QSFP_CHANGE_POWER_MODE
   [Documentation]  This test checks qsfp power mode
   [Tags]   SEASTONE2_V2_DIAG_TC_18_QSFP_CHANGE_POWER_MODE  seastone  test18  stat
   Step  1  check qsfp power



SEASTONE2_V2_DIAG_TC_19_SFP_AND_QSFP_SIGNAL_TEST
   [Documentation]  This test checks sfp test
   [Tags]   SEASTONE2_V2_DIAG_TC_19_SFP_AND_QSFP_SIGNAL_TEST  seastone  test19  stat
   Step  1  go to diag path
   Step  2  check test  ${sfp}
   Step  3  check version  ${sfp}  ${sfp_version}
   Step  4  check list  ${sfp}
   Step  5  check help  ${sfp}
 



SEASTONE2_V2_DIAG_TC_21_RTC_TEST
   [Documentation]  This test checks sfp test
   [Tags]   SEASTONE2_V2_DIAG_TC_21_RTC_TEST   seastone  test21
   Step  1  go to diag path
   Step  2  check test  ${rtc}
   Step  3  check version  ${rtc}  ${rtc_version}
   Step  4  check help  ${rtc}
   Step  5  check rtc operation


SEASTONE2_V2_TC_000_CPU_I2C_Bus_Test
   [Documentation]  To check if can detect CPU I2C Bus successfully.
   [Tags]  SEASTONE2_V2_TC_000_CPU_I2C_Bus_Test
   Step  1  go to diag path
   Step  2  check cpu bus  DUT


SEASTONE2_V2_TC_36_COMe_Management_Ether_Port_Connect_Test
   [Documentation]  This tests mgmt ip connectivity test
   [Tags]  SEASTONE2_V2_TC_36_COMe_Management_Ether_Port_Connect_Test  seastone  test36
   Step  1  check mgmt connect
   
SEASTONE2_V2_TC_REBOOT
   [Documentation]  reboot test
   [Tags]  seastone  swit
   Step  1  check the test  DUT 


SEASTONE2_V2_DIAG_TC_1_UPGRADE_TEST
   [Documentation]  This test checks upgrades.
   [Tags]  SEASTONE2_V2_DIAG_TC_1_UPGRADE_TEST  seastone  test1
   Step  1  go to diag path
   Step  2  check upgrade test  ${fpga}  1  0
   Step  3  check upgrade test  ${bios}  2
   Step  4  power cycle test
   Step  5   go to diag path
   Step  5  check upgrade test  ${bios}  3
   Step  6  power cycle test
   Step  7  go to diag path
   Step  7  check upgrade test  ${cpld}  4
   Step  8  check upgrade test  ${bmc}  5
   Step  9  check upgrade test  ${bmc}  6
   Step  11  check test  upgrade
   Step  12  power cycle test
   [Teardown]  Run Keyword If Test Failed  Power cycle test

SEASTONE2_V2_DIAG_TC_2_CPU_TEST
   [Documentation]  This test checks cpu test
   [Tags]  SEASTONE2_V2_DIAG_TC_2_CPU_TEST  seastone  test2
   Step  1  go to diag path
   Step  2  check test  ${cpu}
   Step  3  check version  ${cpu}  ${cpu_version}
   Step  4  check list  ${cpu}
   Step  5  check help  ${cpu}


SEASTONE2_V2_DIAG_TC_3_FPGA/CPLD_TEST
   [Documentation]  This test checks cpu test
   [Tags]  SEASTONE2_V2_DIAG_TC_3_FPGA/CPU_TEST  seastone  test3
   Step  1  go to diag path
   Step  2  check test  ${cpld}
   Step  3  check version  ${cpld}  ${cpld_version}
   Step  4  check list  ${cpld}
   Step  5  check help  ${cpld}
   Step  6  check cpld dump



SEASTONE2_V2_DIAG_TC_4_CPLD_BMC_TEST
   [Documentation]  This test checks cpld bmc test
   [Tags]   SEASTONE2_V2_DIAG_TC_4_CPLD_BMC_TEST  seastone  test4
   Step  1  check cpld bmc test


SEASTONE2_V2_DIAG_TC_5_TLV_EEPROM_TEST
   [Documentation]  This test checks tlv eeprom test
   [Tags]   SEASTONE2_V2_DIAG_TC_5_TLV_EEPROM_TEST  seastone  test5
   Step  1  go to diag path
   Step  2  check test  ${eeprom}
   Step  3  check version  ${eeprom}  ${eeprom_version}
   Step  4  check list  ${eeprom}
   Step  5  check help  ${eeprom}
   Step  6  check eeprom test

SEASTONE2_V2_DIAG_TC_6_SMBIOS_info_burning
   [Documentation]  This test checks smbios burning.
   [Tags]  SEASTONE2_V2_DIAG_TC_6_SMBIOS_info_burning  seastone  test6
   Step  0  go to diag path
   Step  1  check smbios burn  DUT

SEASTONE2_V2_DIAG_TC_7_BMC_FRU_EEPROM_Test
   [Documentation]  This test checks BMC FRU info test
   [Tags]  SEASTONE2_V2_DIAG_TC_7_BMC_FRU_EEPROM_Test  seastone   test7
   Step  1  go to fru
   Step  2  go to diag path
   Step  3  write bmc fru


SEASTONE2_V2_DIAG_TC_8_Fan_Test
   [Documentation]  This test checks fan test
   [Tags]  SEASTONE2_V2_DIAG_TC_8_Fan_Test  seastone  test8
   Step  1  go to diag path
   Step  2  check fan test
   Step  3  check fan speed  1  20 
   Step  3  check fan speed  2  50
   Step  3  check fan speed  3  70


SEASTONE2_V2_DIAG_TC_9_CPU_I2C_test
   [Documentation]  This tests checks for i2c test
   [Tags]  SEASTONE2_V2_DIAG_TC_9_CPU_I2C_test  seastone  test9
   Step  0  check test  i2c
   Step  1  check i2c read write 


SEASTONE2_V2_DIAG_TC_10_BMC_I2C_Test
   [Documentation]  This test checks i2c devices under BMC access test
   [Tags]   SEASTONE2_V2_DIAG_TC_10_BMC_I2C_Test  seastone  test10
   Step  1  go to diag path
   Step  2  check i2c operation


SEASTONE2_V2_DIAG_TC_12_MEMORY_TEST
   [Documentation]  This test checks memory test
   [Tags]  SEASTONE2_V2_DIAG_TC_12_MEMORY_TEST  test12  seastone
   Step  1  go to diag path
   Step  2  check memory test

SEASTONE2_V2_DIAG_TC_13_PCI_TEST
   [Documentation]  This test checks pci test
   [Tags]  SEASTONE2_V2_DIAG_TC_13_PCI_TEST  seastone  test13
   Step  1  go to diag path 
   Step  2  check pci test
   Step  3  check version  ${pci}  ${pci_version}
   Step  4  check list  ${pci}
   Step  5  check help  ${pci}
  
 
SEASTONE2_V2_DIAG_TC_14_PHY_TEST
   [Documentation]  This test checks phy test
   [Tags]  SEASTONE2_V2_DIAG_TC_14_PHY_TEST  seastone  test14
   Step  1  go to diag path
   Step  2  check phy test



SEASTONE2_V2_DIAG_TC_16_SFP_and_QSFP_EEPROM_test
   [Documentation]  This test checks sfp and qspf tests.
   [Tags]   SEASTONE2_V2_DIAG_TC_16_SFP_and_QSFP_EEPROM_test  seastone  test16
   FOR    ${INDEX}    IN RANGE    1   20
      Step  0  go to diag path
      Step  1  check test  ${qsfp}
      Step  2  check list  ${qsfp}
      Step  3  check version  ${qsfp}  ${qsfp_version}
   END 

SEASTONE2_V2_DIAG_TC_22_STORAGETEST
   [Documentation]  This test checks storage test
   [Tags]  SEASTONE2_V2_DIAG_TC_22_STORAGETEST  seastone  test222
   Step  1  check test  ${storage}
   Step  2  check version  ${storage}  ${storage_version}
   Step  3  check help  ${storage}


SEASTONE2_V2_DIAG_TC_23_USB_TEST
   [Documentation]  This test checks usb test
   [Tags]   SEASTONE2_V2_DIAG_TC_23_USB_TEST  test23  seastone
   Step  1  go to diag path
   Step  2  check usb test
   Step  3  check version  ${usb}  ${usb_version}
   Step  4  check list  ${usb}
   Step  5  check help  ${usb}


SEASTONE2_V2_DIAG_TC_24_SYSINFO_TEST
   [Documentation]  This test checks sysinfo test
   [Tags]   SEASTONE2_V2_DIAG_TC_24_SYSINFO_TEST  test24  seastone
   Step  1  go to diag path
   Step  2  check sysinfo test 
   Step  3  check version  ${sysinfo}  ${sysinfo_version}
   Step  4  check list  ${sysinfo}
   Step  5  check help  ${sysinfo}

SEASTONE2_V2_DIAG_TC_25_TEMPERATURE_TEST
   [Documentation]  This test checks temp test
   [Tags]   SEASTONE2_V2_DIAG_TC_25_TEMPERATURE_TEST  seastone  test25
   step  0  go to diag path
   Step  1  check test  ${temp}

SEASTONE2_V2_DIAG_TC_26_TPM_TEST
   [Documentation]  This test checks tpm test
   [Tags]   SEASTONE2_V2_DIAG_TC_26_TPM_TEST  seastone  test26
   Step  1  check test  ${tpm}


SEASTONE2_V2_DIAG_TC_27_COMe_switch_master/slave_BIOS_Test
   [Documentation]  This test checks for master/slave bios via come
   [Tags]  SEASTONE2_V2_DIAG_TC_27_COMe_switch_master/slave_BIOS_Test  seastone  test27
   Step  1  check come bios  secondary
   Step  2  check come bios  primary

SEASTONE2_V2_DIAG_TC_37_Management_UART_Switch_Test
   [Documentation]  This test checks switch between come and bmc
   [Tags]  SEASTONE2_V2_DIAG_TC_37_Management_UART_Switch_Test  seastone  test37 
   Step  1  check the uart  DUT


SEASTONE2_V2_DIAG_TC_40_BMC_switch_master/slave_BMC_Test
   [Documentation]  This test checks BMC switch master/slave BMC Test
   [Tags]   SEASTONE2_V2_DIAG_TC_40_BMC_switch_master/slave_BMC_Test   test40  seastone  star
   Step  1  change partition  0x02
   Step  2  check partition  01
   Step  3  check active partition  02
   Step  3  check bmc reboot  DUT
   Step  4  check partition  02
   Step  5  change partition  0x01
   Step  6  check partition  02
   Step  8  check active partition  01
   Step  7  check bmc reboot  DUT
   Step  8  check partition  01



SEASTONE2_V2_DIAG_TC_28_UART_TEST
   [Documentation]  This test checks for UART
   [Tags]   SEASTONE2_V2_DIAG_TC_28_UART_TEST   test28  seastone
   [Setup]  go to diag path
   Step  1  check help  ${uart}
   Step  2  check version  ${uart}  ${uart_version}
   Step  3  check the uart test  ${uart}
   
SEASTONE2_V2_DIAG_TC_29_BMC_Devices_LPC_Bus_Access_Test
   [Documentation]  this test checks bmc mc info
   [Tags]  SEASTONE2_V2_DIAG_TC_29_BMC_Devices_LPC_Bus_Access_Test  seastone  test29
   Step  1  check mc info


SEASTONE2_V2_DIAG_TC_30_BMC_CPU_test
   [Documentation]  This test checks bmc cpu test
   [Tags]  SEASTONE2_V2_DIAG_TC_30_BMC_CPU_test   seastone  test30  star
   Step  1  check bmc cpu  DUT  
   [Teardown]  Run Keyword If Test Failed  Switch to come

SEASTONE2_V2_DIAG_TC_42_CPU_STRESS_TEST
    [Documentation]  This test checks cpu stress
    [Tags]  SEASTONE2_V2_DIAG_TC_43_CPU_STRESS_TEST  seastone  test42  stress
    Step  1  check cpu stress


SEASTONE2_V2_DIAG_TC_43_DDR_STRESS_TEST
    [Documentation]  This test checks ddr stress
    [Tags]  SEASTONE2_V2_DIAG_TC_44_DDR_STRESS_TEST  seastone  test43  stress
    Step  1  check ddr stress



SEASTONE2_V2_DIAG_TC_44_SSD_STRESS_TEST
    [Documentation]  This test checks storage stress
    [Tags]  SEASTONE2_V2_DIAG_TC_44_SSD_STRESS_TEST  seastone  test44  stress
    Step  1  check storage stress


SEASTONE2_V2_DIAG_TC_45_SOL_TEST
   [Documentation]  This test checks  sol activation
   [Tags]  SEASTONE2_V2_DIAG_TC_45_SOL_TEST  seastone  test45
   Step  1  check sol activate  DUT


SEASTONE2_V2_DIAG_TC_46_INTERNAL_USB_TEST
   [Documentation]  This test checks internal usb settings
   [Tags]   SEASTONE2_V2_DIAG_TC_46_INTERNAL_USB_TEST  seastone  test46
   Step  1  check internal usb  DUT

SEASTONE2_V2_DIAG_TC_47_EXTERNAL_USB_TEST
   [Documentation]  This test checks external usb settings
   [Tags]   SEASTONE2_V2_DIAG_TC_47_EXTERNAL_USB_TEST   seastone  test47
   Step  1  check external usb  DUT


SEASTONE2_V2_DIAG_TC_CONTROL_COME_REBOOT_Test
   [Documentation]  This test checks for come reboot.
   [Tags]   SEASTONE2_V2_DIAG_CONTROL_COME_REBOOT_Test  seastone
   Step  1  check chassis  DUT


SEASTONE2_V2_DIAG_TC_38_BMC_control_COMe_reboot_Test
   [Documentation]  This test checks for chassis power cycle
   [Tags]   SEASTONE2_V2_DIAG_TC_38_BMC_control_COMe_reboot_Test   seastone  test38  net
   Step  1   check come reboot



SEASTONEV2_BMC_SERVER_TEST
   [Documentation]  Random test
   [Tags]  SEASTONE_SERVER_TEST  seastone_bmc  test1sgsegse
   Step  1  check server seastone  DUT  ${scp_ip}  ${scp_username}  ${scp_password}  ${dhcp_prompt}
   Step  2  get mc info  DUT 
   Step  3  exit the server  DUT
   [Teardown]  Run Keyword If Test Failed  exit the server  DUT


SEASTONE2_V2_DIAG_TC_31_BMC_MAC_Address_Modify
   [Documentation]  This test checks for mac address modification
   [Tags]    SEASTONE2_V2_DIAG_TC_31_BMC_MAC_Address_Modify  seastone  test31
   Step  1  go to diag path
   Step  1  modify bmc address  DUT  ${dummymac}
   Step  2  check bmc mac address  DUT  ${dummymac}
   Step  3  modify bmc address  DUT  ${realmac}
   Step  4  check bmc mac address  DUT  ${realmac}
   [Teardown]  Run Keyword If Test Failed  Switch to come

 
SEASTONE2_V2_DIAG_TC_32_BMC_Management_Ether_Port_MAC_Check_Test 
   [Documentation]  This test checks for mac address.
   [Tags]  SEASTONE2_V2_DIAG_TC_32_BMC_Management_Ether_Port_MAC_Check_Test   seastone  test32
   Step  1  go to diag path
   Step  2  check bmc mac  DUT  ${realmac}


SEASTONE2_V2_DIAG_TC_33_PECI_BUS_TEST
   [Documentation]  This test checks for peci bus.
   [Tags]  SEASTONE2_V2_DIAG_TC_33_PECI_BUS_TEST  seastone  test33
   Step  1  check peci bus


SEASTONE2_V2_DIAG_TC_34_COMe_MAC_address_program
   [Documentation]  This test checks for come mac address.
   [Tags]  SEASTONE2_V2_DIAG_TC_34_COMe_MAC_address_program  seastone  test34
   Step  1  go to diag path
   Step  2  modify come mac  DUT  ${dummymac}
   Step  3  check come mac  DUT  ${dummymac} 
   Step  4  modify come mac  DUT  ${realcomemac}
   Step  5  check come mac  DUT  ${realcomemac}


SEASTONE2_V2_DIAG_TC_35_COME_Management_Ether_Port_MAC_Check_Test
   [Documentation]  This test checks for mac address.
   [Tags]  SEASTONE2_V2_DIAG_TC_35_COME_Management_Ether_Port_MAC_Check_Test   seastone  test35
   Step  1  go to diag path
   Step  2  check come mac  DUT  ${realcomemac}


SEASTONE2_V2_DIAG_TEST
   [Documentation]  This test checks for
   [Tags]  seastone  mole
   Step  1  check mole

SEASTONEv2_POWER_CHASSIS_TEST
   [Documentation]  This test checks chassis power off/on
   [Tags]  SEASTONEv2_POWER_CHASSIS_TEST   chassis
   #[Setup]  Server Os connect
   Step  1  check server seastone  DUT  ${scp_ip}  ${scp_username}  ${scp_password}  ${dhcp_prompt}
   Step  2  get mc info  DUT
   Step  3  diag os connect
   Step  4  check server seastone  DUT  ${scp_ip}  ${scp_username}  ${scp_password}  ${dhcp_prompt}
   Step  3  exit the server  DUT
   [Teardown]  Run Keyword If Test Failed  exit the server  DUT


SEASTONE2_V2_DIAG_TC_39_BMC_switch_master/slave_BIOS_Test
   [Documentation]  This test checks for come reboot.
   [Tags]     SEASTONE2_V2_DIAG_TC_39_BMC_switch_master/slave_BIOS_Test  test39  seastone  net
   Step  1  check bios reboot  DUT  ${bios_secondary}  'Back up'
   Step  2  check bios reboot  DUT  ${bios_primary}  'Primary'


SEASTONE2_V2_DIAG_TC_15_PSU_IPMI_TEST
   [Documentation]  This test checks for psu
   [Tags]   SEASTONE2_V2_DIAG_TC_15_PSU_IPMI_TEST  seastone  test15
   Step  1  check psu ipmi  DUT


*** Keywords ***
DiagOS Connect Device
    DiagOSConnect

DiagOS Disconnect Device
    DiagOSDisconnect

ServerOS Connect Device
    ServerOsConnect

ServerOS Disconnect Device
    ServerOsDisConnect
                    
 
