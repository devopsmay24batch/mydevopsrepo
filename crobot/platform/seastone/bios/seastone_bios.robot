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
Library           bios_menu_lib.py
#Library           openbmc_lib.py
Library           bios_lib.py
Library           ../SEASTONECommonLib.py

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
SEASTONE2v2_BIOS_Information_Check_TC_01
   [Documentation]   To check if BIOS image has been programmed
   [Tags]     SEASTONE2v2_BIOS_Information_Check_TC_01   seastone   test1
  # [Timeout]  20 min 00 seconds
   Step  1  Enter bios now
   Step  2  check bios basic  DUT
   Step  2  exit bios now  DUT 
 

SEASTONE2v2_1.0.12_boot_sequence_test
   [Documentation]   To verify if the pluuged USB can be detected
   [Tags]     SEASTONE2v2_1.0.12_boot_sequence_test  ready  upto  1-0-12  updating
  # [Timeout]  20 min 00 seconds
   Step  1  enter into bios setup now  DUT
   Step  2  check boot menu spec  DUT
   Step  3  set boot one  DUT  Shell
   Step  4  detect in shell  DUT  1
   Step  5  enter into bios setup now  DUT  2
   #Step  6  disable all boot  DUT
   Step  7  boot cleanup  DUT

SEASTONE2v2_1.0.13_cpu_information_test
   [Documentation]   To check cpu info matches in setup and inside os
   [Tags]     SEASTONE2v2_1.0.13_cpu_information_test  ready  bios
  # [Timeout]  20 min 00 seconds
    Step  1  read os cpu info  DUT
    Step  2  enter into bios setup now  DUT
    Step  3  read setup cpu info  DUT
    Step  4  exit bios now  DUT
    [Teardown]  Run Keyword If Test Failed  bios_boot  DUT  0

SEASTONE2v2_1.0.27_usb_device_detect_test
   [Documentation]   To verify if the pluuged USB can be detected
   [Tags]     SEASTONE2v2_1.0.27_usb_device_detect_test  ready  1-0-27  bios
  # [Timeout]  20 min 00 seconds
   Step  1  detect usb onl  DUT
   Step  2  enter into bios setup now  DUT
   Step  3  detect usb setup  DUT  1
   Step  4  set boot one  DUT  Shell
   Step  5  detect in shell  DUT  2
   Step  6  enter into bios setup now  DUT
   Step  7  set boot one  DUT  ONL
   [Teardown]  Run Keyword If Test Failed  bios_boot  DUT  0
   
SEASTONE2v2_1.0.28_usb_read_write_test
   [Documentation]   To check if BIOS image has been programmed
   [Tags]     SEASTONE2v2_1.0.28_usb_read_write_test  ready  bios
  # [Timeout]  20 min 00 seconds
   Step  1  check usb read write  DUT
   [Teardown]  Run Keyword If Test Failed  bios_boot  DUT  0

SEASTONE2v2_1.0.31_sata_device_detect_test
   [Documentation]  This test checks if SATA devices are detected
   [Tags]    SEASTONE2v2_1.0.31_sata_device_detect_test  ready  bios  noob
   [Timeout]  30 min 00 seconds
   Step  1  enter into bios setup now  DUT
   Step  2  find sata device in setup  DUT
   Step  3  exit bios now  DUT
   Step  4  check sata device size  DUT  2
   [Teardown]  Run Keyword If Test Failed  bios_boot  DUT  0

SEASTONE2v2_1.0.32_sata_device_size_test
   [Documentation]  This test checks if SATA device size is correct
   [Tags]    SEASTONE2v2_1.0.32_sata_device_size_test  ready  bios  noob  1-0-32
   [Timeout]  30 min 00 seconds
   Step  1  check sata device size  DUT 
   [Teardown]  Run Keyword If Test Failed  power_cycle_and_login  DUT

SEASTONE2v2_1.0.33_sata_device_read_write_test
   [Documentation]  This test checks if the SATA device read write functions work properly
   [Tags]   SEASTONE2v2_1.0.33_sata_device_read_write_test  ready  bios  noob
   Step  1  check sata write  DUT
   [Teardown]  Run Keyword If Test Failed  power_cycle_and_login  DUT

SEASTONE2v2_1.0.36_backup_bios_test
   [Documentation]   To check if DUT can boot from backup BIOS successfully
   [Tags]     SEASTONE2v2_1.0.36_backup_bios_test  ready  bios
  # [Timeout]  20 min 00 seconds 
   Step  1  configure diag dir  DUT  ${cel_diag_image}
   Step  1  toggle bios  DUT  1
   Step  2  check reboot bios boot  DUT
   Step  3  toggle bios  DUT  0
   Step  4  check reboot bios boot  DUT  2
   [Teardown]  Run Keyword If Test Failed  power_cycle_and_login  DUT

SEASTONE2v2_1.0.37_serial_port_configuration_test
   [Documentation]   To check the serial port address to ensure it is consistent with the BIOS SPEC definition
   [Tags]     SEASTONE2v2_1.0.37_serial_port_configuration_test  ready  bios  1-0-37
  # [Timeout]  20 min 00 seconds
   Step  1  check os serial port  DUT
   Step  2  enter into bios setup now  DUT
   Step  3  check setup serial port  DUT
   Step  4  exit bios now  DUT
   [Teardown]  Run Keyword If Test Failed  power_cycle_and_login  DUT

SEASTONE2v2_1.0.39_post_information_test
   [Documentation]   To verify if the information displayed during POST is accurate
   [Tags]     SEASTONE2v2_1.0.39_post_information_test  ready  bios
   Step  1  check post info  DUT
   [Teardown]  Run Keyword If Test Failed  power_cycle_and_login  DUT

SEASTONE2v2_1.0.41_post_hotkey_test
   [Documentation]   To verify if hotkeys work as expected during POST
   [Tags]     SEASTONE2v2_1.0.41_post_hotkey_test  ready  bios
   Step  1  enter into bios setup now  DUT  2
   Step  2  exit bios now  DUT
   [Teardown]  Run Keyword If Test Failed  power_cycle_and_login  DUT

SEASTONE2v2_1.0.42_setup_hotkey_test
   [Documentation]  This test checks hotkeys functioning inside setup
   [Tags]    SEASTONE2v2_1.0.42_setup_hotkeys_test  ready  bios
   [Timeout]  30 min 00 seconds
   Step  1  enter into bios setup now  DUT
   Step  2  check hotkey functions  DUT
   Step  3  exit bios now  DUT
   [Teardown]  Run Keyword If Test Failed  power_cycle_and_login  DUT


SEASTONE2v2_1.0.52_intelRC_setup_menu_test
   [Documentation]   To check if BIOS image has been programmed
   [Tags]     SEASTONE2v2_1.0.52_intelRC_setup_menu_test  ready  bios
  # [Timeout]  20 min 00 seconds
   Step  1  Enter bios now
   Step  2  check IntelRC  DUT
   Step  3  exit bios now  DUT 
   [Teardown]  Run Keyword If Test Failed  power_cycle_and_login  DUT

SEASTONE2v2_1.0.55_ac_power_cycling_stress_test
   [Documentation]   To do ac power cycling stress test and check system stability
   [Tags]     SEASTONE2v2_1.0.55_ac_power_cycling_stress_test 
   #Step  1  import from remote  DUT  1 
   Step  2  powercycle x times  DUT  3
   Step  3  run post stress test scans  DUT
   [Teardown]  Run Keyword If Test Failed  bios_boot  DUT  0

SEASTONE2v2_1.0.56_warm_reset_stress_test
   [Documentation]   To do warm reset stress for x number of times
   [Tags]     SEASTONE2v2_1.0.56_warm_reset_stress_test 
   #Step  1  import from remote  DUT  2
   #Step  2  run cpu warm reset stress test  DUT
   #Step  3  display stress test logs  DUT
   Step   4  reboot x times  DUT  3
   Step   5  run post stress test scans  DUT
   [Teardown]  Run Keyword If Test Failed  bios_boot  DUT  0

SEASTONE2v2_1.0.57_cold_reset_stress_test
   [Documentation]   To do cold reset stress for x number of times
   [Tags]     SEASTONE2v2_1.0.57_cold_reset_stress_test 
   #Step  1  import from remote  DUT  3
   #Step  2  run cpu cold reset stress test  DUT
   #Step  3  display stress test logs  DUT
   Step  4  powercycle x times  DUT  3
   Step  5  run post stress test scans  DUT
   [Teardown]  Run Keyword If Test Failed  bios_boot  DUT  0

SEASTONE2v2_1.0.58_cpu_stress_test
   [Documentation]   To do cpu stress load upto 99%
   [Tags]     SEASTONE2v2_1.0.58_cpu_stress_test 
   Step  1  import from remote  DUT  4
   Step  2  run cpu stress test  DUT
   [Teardown]  Run Keyword If Test Failed  bios_boot  DUT  0

SEASTONE2v2_1.0.59_memory_stress_test
   [Documentation]   To do memory stress test with memtester tool
   [Tags]     SEASTONE2v2_1.0.59_memory_stress_test 
   Step  1  run memory stress test  DUT
   Step  2  reboot x times  DUT  1
   [Teardown]  Run Keyword If Test Failed  bios_boot  DUT  0

SEASTONE2v2_1.0.63_system_event_log_test
   [Documentation]   To verify if the pluuged USB can be detected
   [Tags]     SEASTONE2v2_1.0.63_system_event_log_test  1-0-63  failing  bios
  # [Timeout]  20 min 00 seconds
   Step  1  check bmc and sel setup
   Step  2  check and clear sel os
   Step  3  check sel clear setup
   Step  4  check sel update setup
   [Teardown]  Run Keyword If Test Failed  power_cycle_and_login  DUT

SEASTONE2v2_1.0.64_bmc_self_log_test
   [Documentation]   To verify if the BIOS can operate the SEL correctly
   [Tags]     SEASTONE2v2_1.0.64_bmc_self_log_test  1-0-64  failing  bios
  # [Timeout]  20 min 00 seconds
   Step  1  enter into bios setup now  DUT
   Step  2  validate bmc log options  DUT  No  Clear
   Step  3  exit bios now  DUT
   Step  4  reboot x times  DUT  3
   Step  5  enter into bios setup now  DUT
   Step  6  validate bmc log options  DUT  No  Clear  False
   Step  7  validate bmc log options  DUT  No  No More
   Step  8  exit bios now  DUT
   Step  9  reboot x times  DUT  3
   Step  10  enter into bios setup now  DUT
   Step  11  validate bmc log options  DUT  No  No More  True
   Step  12  validate bmc log options  DUT  Yes  No More
   Step  13  validate bmc log options  DUT  Yes  Clear
   Step  14  validate bmc log options  DUT  Yes  No More
   Step  15  exit bios now  DUT
   [Teardown]  Run Keyword If Test Failed  power_cycle_and_login  DUT

SEASTONE2v2_1.0.65_bmc_network_configuration_test
   [Documentation]   To verify if the BIOS can set and get the BMC network configuration correctly
   [Tags]     SEASTONE2v2_1.0.65_bmc_network_configuration_test  1-0-65  ready  bios
   Step  1  validate static ip config
   Step  2  validate dhcp ip config
   [Teardown]  Run Keyword If Test Failed  bios_boot  DUT  0

SEASTONE2v2_1.0.66_fast_boot_test
   [Documentation]   Temporary testcase for fastboot experimenting
   [Tags]     SEASTONE2v2_1.0.66_fast_boot_test  1-0-66  bios
   Step  1  config fastboot image
   Step  2  validate fastboot image
   Step  3  cleanup fastboot image

SEASTONEv2_BIOS_CPU_I2C_Interface_Test  
    [Documentation]  To verify I2C Bios CPU interface
    [Tags]  SEASTONEv2_BIOS_CPU_I2C_Interface_Test  ready  bios  upto  bhavya
    Step  1  check i2c test info  DUT
    [Teardown]  Run Keyword If Test Failed  bios_boot  DUT  0

SEASTONE2v2_BIOS_CPU_LPC_Interface_Test
    [Documentation]  To verify LPC tools for read write operations
    [Tags]  SEASTONE2v2_BIOS_CPU_LPC_Interface_Test  ready  bios  upto  bhavya
    Step  1  power_cycle_and_login  DUT
    Step  2  enter into lpc  DUT
    Step  3  read baseboard cpld register  DUT  0xa101  de
    Step  4  write baseboard cpld register  0xa101  0xaa
    Step  5  read baseboard cpld register  DUT  0xa101  aa
    Step  6  read baseboard cpld register  DUT  0xa1e1  de
    Step  7  write baseboard cpld register  0xa1e1  0x5e
    Step  8  read baseboard cpld register  DUT  0xa1e1  5e
    Step  9  power_cycle_and_enter_into_lpc  DUT
    Step  10  read baseboard cpld register  DUT  0xa101  de
    Step  11  read baseboard cpld register  DUT  0xa1e1  de
    Step  12  check add user to bmc  3  test
    [Teardown]  Run Keyword If Test Failed  End CPU LPC Interface Test
    
SEASTONE2v2_1.0.5_programming_via_bmc_lan
    [Documentation]   To verify bios image update through LAN
    [Tags]   SEASTONE2v2_1.0.5_programming_via_bmc_lan  ready  bios  upto  bhavya
    Step  1  downgrade primary bios image through lan
    Step  2  upgrade primary bios image through lan
    Step  3  power_cycle_and_login  DUT
    [Teardown]  Run Keyword If Test Failed  bios_boot  DUT  0


SEASTONE2v2_1.0.21_PCIE_Information_Test
    [Documentation]  To verify PCI information through shell prompt and linux prompt
    [Tags]  SEASTONE2v2_1.0.21_PCIE_Information_Test  ready  bios  upto  bhavya
    Step  1  check pci information  DUT
    Step  2  boot UEFI shell check
    [Teardown]  Run Keyword If Test Failed  bios_boot  DUT  0


SEASTONE2v2_1.0.46_SMBios_table_read
    [Documentation]  To verify SMBIOS information for various codes
    [Tags]  SEASTONE2v2_1.0.46_SMBios_table_read  
    Step  1  read_smbios  DUT  ${smbios_list}


SEASTONE2v2_1.0.4_Programming_via_BMC_USB
    [Documentation]  To update bios through bmc usb
    [Tags]  SEASTONE2v2_1.0.4_Programming_via_BMC_USB  ready  bios  upto  1-0-4  bhavya
    Step  1  downgrade primary bios image through usb
    Step  2  upgrade primary bios image through usb
    Step  3  power_cycle_and_login  DUT
    [Teardown]  Run Keyword If Test Failed  umount_disk_from_device  DUT

SEASTONE2v2_1.0.3_Online_Programming_under_Linux_OS
    [Documentation]  To update bios via linux OS
    [Tags]  SEASTONE2v2_1.0.3_Online_Programming_under_Linux_OS  ready  bios  upto  bhavya
    Step  1  downgrade primary bios image through afulnx
    Step  2  upgrade primary bios image through afulnx
    Step  3  power_cycle_and_login  DUT
    [Teardown]  Run Keyword If Test Failed  umount_disk_from_device  DUT

SEASTONE2v2_1.0.62_ipmi_bmc_information_test
    [Documentation]  This test is for bmc information
    [Tags]     SEASTONE2v2_1.0.62_ipmi_bmc_information_test  bios
    [Timeout]  30 min 00 seconds
    Step  1  ipmi bmc test
    [Teardown]  Run Keyword If Test Failed  bios_boot  DUT  0

SEASTONE2v2_1.0.53_boot_menu_test
    [Documentation]  This test is for boot menu
    [Tags]     SEASTONE2v2_1.0.53_boot_menu_test  ready  bios
    [Timeout]  30 min 00 seconds
    Step  1  boot_menu_check
    [Teardown]  Run Keyword If Test Failed  bios_boot  DUT  0


SEASTONE2v2_1.0.44_s0_state_test
    [Documentation]  This test is for s0 state check
    [Tags]     SEASTONE2v2_1.0.44_s0_state_test  ready  bios
    [Timeout]  30 min 00 seconds
    Step  1  s0_state_test  DUT
    [Teardown]  Run Keyword If Test Failed  bios_boot  DUT  0

SEASTONE2v2_1.0.60_SSD_Read/Write_stress_test
    [Documentation]  This test is for read write stress test
    [Tags]     SEASTONE2v2_1.0.60_SSD_Read/Write_stress_test
    [Timeout]  30 min 00 seconds
    Step  1  read_write_stress_test  DUT  100
    [Teardown]  Run Keyword If Test Failed  bios_boot  DUT  0

   

SEASTONE2v2_1.0.14_cpu_microcode_test
    [Documentation]  This test checks cpu microcode
    [Tags]     SEASTONE2v2_1.0.14_cpu_microcode_test  ready  bios
    [Timeout]  30 min 00 seconds
    Step  1  check the cpu microcode 
    [Teardown]  Run Keyword If Test Failed  bios_boot  DUT  0
    



SEASTONE2v2_1.0.9_boot_onie_test
    [Documentation]  This test boot ONIE
    [Tags]     SEASTONE2v2_1.0.9_boot_onie_test  bios
    [Timeout]  30 min 00 seconds
    Step  1  boot onie test
   [Teardown]  Run Keyword If Test Failed  power_cycle_and_login  DUT

SEASTONE2v2_1.0.51_main_menu_test
    [Documentation]  This test is for main menu
    [Tags]     SEASTONE2v2_1.0.51_main_menu_test  bios
    [Timeout]  30 min 00 seconds
    Step  1  main menu test
   [Teardown]  Run Keyword If Test Failed  power_cycle_and_login  DUT


SEASTONE2v2_1.0.48_administrator_password_test
    [Documentation]  This test is for administrator password
    [Tags]     SEASTONE2v2_1.0.48_administrator_password_test  bios
    [Timeout]  30 min 00 seconds
    Step  1  administrator password test
   [Teardown]  Run Keyword If Test Failed  power_cycle_and_login  DUT

SEASTONE2v2_1.0.49_user_password_test
    [Documentation]  This test is for user password
    [Tags]     SEASTONE2v2_1.0.49_user_password_test  bios
    [Timeout]  30 min 00 seconds
    Step  1  user password test
   [Teardown]  Run Keyword If Test Failed  power_cycle_and_login  DUT


SEASTONE2v2_1.0.6_bios_information_test
    [Documentation]  This test checks bios information
    [Tags]     SEASTONE2v2_1.0.6_bios_information_test  bios
    [Timeout]  30 min 00 seconds
    Step  1  bios information check
   [Teardown]  Run Keyword If Test Failed  power_cycle_and_login  DUT


SEASTONE2v2_1.0.69_power_reset_cause_test
    [Documentation]  This test is for power reset cause
    [Tags]     SEASTONE2v2_1.0.69_power_reset_cause_test  bios
    [Timeout]  30 min 00 seconds
    Step  1  power_reset_cause_test
   [Teardown]  Run Keyword If Test Failed  power_cycle_and_login  DUT

SEASTONE2v2_1.0.16_memory_information_test
    [Documentation]  This test checks memory information
    [Tags]     SEASTONE2v2_1.0.16_memory_information_test  bios
    [Timeout]  30 min 00 seconds
    Step  1  check memory information  DUT
   [Teardown]  Run Keyword If Test Failed  power_cycle_and_login  DUT



SEASTONE2v2_1.0.23_management_port_information_check
    [Documentation]  This test is for management port information
    [Tags]     SEASTONE2v2_1.0.23_management_port_information_check  bios
    [Timeout]  30 min 00 seconds
    Step  1  management_port_information_check
   [Teardown]  Run Keyword If Test Failed  power_cycle_and_login  DUT


SEASTONE2v2_1.0.25_uefi_pxe_functional_test
    [Documentation]  This test is for uefi pxe functional
    [Tags]     SEASTONE2v2_1.0.25_uefi_pxe_functional_test  bios
    [Timeout]  30 min 00 seconds
    Step  1  uefi_pxe_functional_test 
   [Teardown]  Run Keyword If Test Failed  power_cycle_and_login  DUT

SEASTONE2v2_1.0.40_non_bios_boot_messages
    [Documentation]  This test is for non bios messages
    [Tags]     SEASTONE2v2_1.0.40_non_bios_boot_messages  bios
    [Timeout]  30 min 00 seconds
    Step  1  non_bios_boot_messages_test 
   [Teardown]  Run Keyword If Test Failed  power_cycle_and_login  DUT


SEASTONE2v2_1.0.54_save_and_exit_test
    [Documentation]  This test checks save and exit menu
    [Tags]     SEASTONE2v2_1.0.54_save_and_exit_test  bios 
    [Timeout]  30 min 00 seconds
    Step  1  save and exit check
   [Teardown]  Run Keyword If Test Failed  power_cycle_and_login  DUT

SEASTONE2v2_1.0.50_accesslevel_test
    [Documentation]  This test is for accesslevel
    [Tags]     SEASTONE2v2_1.0.50_accesslevel_test  bios
    [Timeout]  30 min 00 seconds
    Step  1  accesslevel test
   [Teardown]  Run Keyword If Test Failed  power_cycle_and_login  DUT

SEASTONE2v2_1.0.8_boot_UEFI_OS_test
    [Documentation]  This test is for boot uefi os 
    [Tags]     SEASTONE2v2_1.0.8_boot_UEFI_OS_test  bios
    [Timeout]  30 min 00 seconds
    Step  1  boot UEFI OS test
   [Teardown]  Run Keyword If Test Failed  power_cycle_and_login  DUT

SEASTONE2v2_1.0.10_boot_UEFI_shell_test
    [Documentation]  This test is for boot uefi shell
    [Tags]     SEASTONE2v2_1.0.10_boot_UEFI_shell_test  bios
    [Timeout]  30 min 00 seconds
    Step  1  boot UEFI shell check
   [Teardown]  Run Keyword If Test Failed  power_cycle_and_login  DUT
  





SEASTONE2v2_1.0.18_memtest86_diagnostic_test
    [Documentation]  This test is for memtest86 
    [Tags]     SEASTONE2v2_1.0.18_memtest86_diagnostic_test
    Step  1  memtest86_test_check  
   [Teardown]  Run Keyword If Test Failed  power_cycle_and_login  DUT 
   

SEASTONE2v2_1.0.34_RTC_test
    [Documentation]  This test is for RTC 
    [Tags]     SEASTONE2v2_1.0.34_RTC_test  bios
    Step  1  check_for_RTC  DUT
   [Teardown]  Run Keyword If Test Failed  power_cycle_and_login  DUT

SEASTONE2v2_1.0.17_memory_frequency_test
    [Documentation]  This test checks memory frequency
    [Tags]     SEASTONE2v2_1.0.17_memory_frequency_test  notready  bios
    [Timeout]  30 min 00 seconds
    Step  1  check memory frequency
    [Teardown]  Run Keyword If Test Failed  bios_boot  DUT  0

SEASTONE2v2_1.0.2_online_programming_under_uefi_shell
    [Documentation]  This test checks online programming under uefi shell
    [Tags]     SEASTONE2v2_1.0.2_online_programming_under_uefi_shell  bios
    [Timeout]  30 min 00 seconds
    Step  1  online_programming_under_uefi_shell_check 
   [Teardown]  Run Keyword If Test Failed  power_cycle_and_login  DUT

dummy_test
    [Tags]     dummy
    Step  1  cleanup fastboot image




















*** Keywords ***
DiagOS Connect Device
    DiagOSConnect

DiagOS Disconnect Device
    DiagOSDisconnect
