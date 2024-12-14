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
Library           ../MOONSTONECommonLib.py

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
1.0.0_BIOS_Information_Check_Test
   [Documentation]   To check if BIOS image has been programmed
   [Tags]     1.0.0_BIOS_Information_Check_Test  1-0-0  
   Step  1  Enter bios now
   Step  2  exit bios now  DUT 

1.0.21_CPU_I2C_Interface_Test  
    [Documentation]  To verify I2C Bios CPU interface
    [Tags]  1.0.21_CPU_I2C_Interface_Test  1-0-21  bios  
    Step  1  download_deb_package  DUT
    Step  2  check i2c test info  DUT
    Step  3  remove_files_from_device  DUT  ${bios_deb_image}
    

1.0.22_CPU_I2C_Interface_Test  
    [Documentation]  To verify LPC tools for read write operations
    [Tags]  1.0.22_CPU_I2C_Interface_Test  1-0-22  bios  
    Step  1  enter into lpc  DUT
    Step  2  check_cpld_version_through_lpc_tools  DUT
    Step  3  test_read_write_cpld_register  DUT  0x11
    Step  4  check add user to bmc  3  test
    [Teardown]  End CPU LPC Interface Test

1.0.20_PCIE_Information_Test
    [Documentation]  To verify PCI information through shell prompt and linux prompt
    [Tags]  1.0.20_PCIE_Information_Test  1-0-20  bios  smoke
    Step  1  check pci information  DUT
    Step  2  boot UEFI shell check

1.0.46_SMBios_table_read
    [Documentation]  To verify SMBIOS information for various codes
    [Tags]  1.0.46_SMBios_table_read  1-0-46  bios
    Step  1  read_smbios  DUT  ${smbios_list}

1.0.13_cpu_information_test
   [Documentation]   To check cpu info matches in setup and inside os
   [Tags]     1.0.13_cpu_information_test  1-0-13  bios  smoke
   Step  1  read os cpu info  DUT
   Step  2  enter into bios setup now  DUT
   Step  3  read setup cpu info  DUT
   Step  4  exit bios now  DUT
   
1.0.28_usb_read_write_test
   [Documentation]   To check if BIOS image has been programmed
   [Tags]     1.0.28_usb_read_write_test  1-0-28  bios
   Step  1  check usb read write  DUT

1.0.33_sata_device_read_write_test
   [Documentation]  This test checks if the SATA device read write functions work properly
   [Tags]   1.0.33_sata_device_read_write_test  1-0-33  bios  
   Step  1  check sata write  DUT

1.0.39_post_information_test
   [Documentation]   To verify if the information displayed during POST is accurate
   [Tags]     1.0.39_post_information_test  1-0-39  bios
   Step  1  check post info  DUT

1.0.41_post_hotkey_test
   [Documentation]   To verify if hotkeys work as expected during POST
   [Tags]     1.0.41_post_hotkey_test  1-0-41  bios 
   Step  1  enter into bios setup now  DUT  2
   Step  2  exit bios now  DUT

1.0.59_memory_stress_test
   [Documentation]   To do memory stress test with memtester tool
   [Tags]     1.0.59_memory_stress_test  1-0-59  bios
   Step  1  run memory stress test  DUT
   Step  2  reboot x times  DUT  1

1.0.53_boot_menu_test
    [Documentation]  This test is for boot menu
    [Tags]     1.0.53_boot_menu_test  1-0-53  bios
    [Timeout]  30 min 00 seconds
    Step  1  boot_menu_check

1.0.14_cpu_microcode_test
    [Documentation]  This test checks cpu microcode
    [Tags]     1.0.14_cpu_microcode_test  1-0-14  bios
    [Timeout]  30 min 00 seconds
    Step  1  check the cpu microcode 
    
1.0.9_boot_onie_test
    [Documentation]  This test boot ONIE
    [Tags]     1.0.9_boot_onie_test  1-0-9  bios 
    [Timeout]  30 min 00 seconds
    Step  1  boot onie test

1.0.51_main_menu_test
    [Documentation]  This test is for main menu
    [Tags]     1.0.51_main_menu_test  1-0-51  bios
    [Timeout]  30 min 00 seconds
    Step  1  main menu test

1.0.48_administrator_password_test
    [Documentation]  This test is for administrator password
    [Tags]     1.0.48_administrator_password_test  bios  
    Step  1  administrator password test

1.0.49_user_password_test
    [Documentation]  This test is for user password
    [Tags]     1.0.49_user_password_test  1-0-49  bios  
    [Timeout]  30 min 00 seconds
    Step  1  user password test

1.0.6_bios_information_test
    [Documentation]  This test checks bios information
    [Tags]     1.0.6_bios_information_test  1-0-6  bios  smoke
    [Timeout]  30 min 00 seconds
    Step  1  bios information check

1.0.16_memory_information_test
    [Documentation]  This test checks memory information
    [Tags]     1.0.16_memory_information_test  1-0-16  bios  
    [Timeout]  30 min 00 seconds
    Step  1  check memory information  DUT

1.0.23_management_port_information_check
    [Documentation]  This test is for management port information
    [Tags]     1.0.23_management_port_information_check  1-0-23  bios  smoke 
    [Timeout]  30 min 00 seconds
    Step  1  management_port_information_check

1.0.54_save_and_exit_test
    [Documentation]  This test checks save and exit menu
    [Tags]     1.0.54_save_and_exit_test  1-0-54  bios
    [Timeout]  30 min 00 seconds
    Step  1  save and exit check

1.0.50_accesslevel_test
    [Documentation]  This test is for accesslevel
    [Tags]     1.0.50_accesslevel_test  1-0-50  bios
    [Timeout]  30 min 00 seconds
    Step  1  accesslevel test

1.0.8_boot_UEFI_OS_test
    [Documentation]  This test is for boot uefi os 
    [Tags]     1.0.8_boot_UEFI_OS_test  1-0-8  bios  
    [Timeout]  30 min 00 seconds
    Step  1  boot UEFI OS test

1.0.10_boot_UEFI_shell_test
    [Documentation]  This test is for boot uefi shell
    [Tags]     1.0.10_boot_UEFI_shell_test  1-0-10  bios 
    [Timeout]  30 min 00 seconds
    Step  1  boot UEFI shell check

1.0.2_online_programming_under_uefi_shell
   [Documentation]  This test checks online programming under uefi shell
   [Tags]     1.0.2_online_programming_under_uefi_shell  1-0-2  bios  
   Step  1  download_deb_package  DUT
   Step  2  downgrade primary bios image through shell
   Step  3  upgrade primary bios image through shell
   [Teardown]  remove_files_from_device  DUT  ${bios_deb_image}

1.0.3_Online_Programming_under_Linux_OS
    [Documentation]  To update bios via linux OS
    [Tags]  1.0.3_Online_Programming_under_Linux_OS  1.0.3  bios  
    Step  1  Setup for online os programming through linux afulnx
    Step  2  downgrade primary bios image through afulnx
    Step  3  upgrade primary bios image through afulnx
    Step  4  downgrade secondary bios image through afulnx
    Step  5  upgrade secondary bios image through afulnx
    [Teardown]  Cleanup for online os programming through linux afulnx

1.0.36_backup_bios_test
   [Documentation]   To check if DUT can boot from backup BIOS successfully
   [Tags]     1.0.36_backup_bios_test  1-0-36  bios  
   Step  1  download_deb_package  DUT
   Step  2  boot_bios_to_primary_or_backup  DUT  3
   Step  3  check_bmc_version_info  DUT
   Step  4  check_pci_information  DUT
   Step  5  check_i2c_test_info  DUT
   Step  6  boot_bios_to_primary_or_backup  DUT  1
   [Teardown]  remove_files_from_device  DUT  ${bios_deb_image}

1.0.34_RTC_test
    [Documentation]  This test is for RTC 
    [Tags]     1.0.34_RTC_test  1-0-34  bios  
    Step  1  check_for_RTC  DUT 

1.0.12_boot_sequence_test
   [Documentation]   To verify if the pluuged USB can be detected
   [Tags]     1.0.12_boot_sequence_test  1-0-12  bios
   Step  1  enter into bios setup now  DUT
   Step  2  set boot one  DUT  Shell
   Step  3  detect in shell  DUT  1
   Step  4  enter into bios setup now  DUT  2
   Step  5  disable all boot  DUT
   Step  6  boot_menu_onl  DUT

1.0.27_usb_device_detect_test
   [Documentation]   To verify if the pluuged USB can be detected
   [Tags]     1.0.27_usb_device_detect_test  1-0-27  bios
   Step  1  detect usb onl  DUT
   Step  2  enter into bios setup now  DUT
   Step  3  detect usb setup  DUT  1
   Step  4  set boot one  DUT  Shell
   Step  5  detect in shell  DUT  2
   Step  6  enter into bios setup now  DUT
   Step  7  boot_menu_onl  DUT

1.0.31_sata_device_detect_test
   [Documentation]  This test checks if SATA devices are detected
   [Tags]    SATA-DEVICE-DETECT-TEST-1-0-31  1-0-31  bios
   [Timeout]  30 min 00 seconds
   Step  1  enter into bios setup now  DUT
   Step  2  find sata device in setup  DUT
   Step  3  exit bios now  DUT
   Step  4  check sata device size  DUT  2

1.0.32_sata_device_size_test
   [Documentation]  This test checks if SATA device size is correct
   [Tags]    1.0.32_sata_device_size_test  1-0-32  bios 
   [Timeout]  30 min 00 seconds
   Step  1  check sata device size  DUT 

1.0.60_SSD_Read/Write_stress_test
    [Documentation]  This test is for read write stress test
    [Tags]     1.0.60_SSD_Read/Write_stress_test  1-0-60  bios  
    Step  1  read_write_stress_test  DUT  3

1.0.56_warm_reset_stress_test
   [Documentation]   To do warm reset stress for x number of times
   [Tags]     1.0.56_warm_reset_stress_test  1-0-56   bios
   Step   1  warm_reset_stress_test  DUT  3

1.0.42_setup_hotkey_test
   [Documentation]  This test checks hotkeys functioning inside setup
   [Tags]    1.0.42_setup_hotkeys_test  1-0-42    bios
   [Timeout]  30 min 00 seconds
   Step  1  enter into bios setup now  DUT
   Step  2  check hotkey functions  DUT
   Step  3  exit bios now  DUT

1.0.61_ipmi_bmc_information_test
    [Documentation]  This test is for bmc information
    [Tags]     1.0.62_ipmi_bmc_information_test  1-0-61  bios  
    [Timeout]  30 min 00 seconds
    Step  1  ipmi bmc test

1.0.17_memory_frequency_test
    [Documentation]  This test checks memory frequency
    [Tags]     1.0.17_memory_frequency_test  1-0-17  bios
    Step  1  check memory frequency

1.0.44_s0_state_test
    [Documentation]  This test is for s0 state check
    [Tags]     1.0.44_s0_state_test  1-0-44  bios  
    [Timeout]  30 min 00 seconds
    Step  1  s0_state_test  DUT

1.0.37_serial_port_address_test
   [Documentation]   To check the serial port address to ensure it is consistent with the BIOS SPEC definition
   [Tags]     1.0.37_serial_port_address_test  1-0-37  bios 
   Step  1  check os serial port  DUT
   Step  2  enter into bios setup now  DUT
   Step  3  check setup serial port  DUT
   Step  4  exit bios now  DUT

1.0.58_cpu_stress_test
   [Documentation]   To do cpu stress load upto 99%
   [Tags]     1.0.58_cpu_stress_test  1-0-58  bios
   Step  1  run cpu stress test  DUT

1.0.52_intelRC_setup_menu_test
   [Documentation]   To check if BIOS image has been programmed
   [Tags]     1.0.52_intelRC_setup_menu_test  1-0-52  bios
   Step  1  Enter bios now
   Step  2  check IntelRC  DUT
   Step  3  exit bios now  DUT

1.0.43_Bios_utility_undefined_hotkeys_and_boundry_check_test
    [Documentation]  To verify bios utility undefined hot keys and boundry keys
    [Tags]  1.0.43_Bios_utility_undefined_hotkeys_and_boundry_check_test  1-0-43  bios
    Step  1  Enter bios now
    Step  2  check_pressing_undefined_keys  DUT
    Step  3  check_left_right_keys_for_main_menu_and_exit_screen  DUT
    Step  4  exit bios now  DUT

1.0.67_TCO_feature_Test
    [Documentation]  To verify bios utility undefined hot keys and boundry keys
    [Tags]  1.0.67_TCO_feature_Test  1-0-67  bios
    Step  1  check tco feature  DUT

1.0.25_uefi_pxe_functional_test
    [Documentation]  This test is for uefi pxe functional
    [Tags]     1.0.25_uefi_pxe_functional_test  1-0-25  bios
    [Timeout]  30 min 00 seconds
    Step  1  uefi_pxe_functional_test 

1.0.40_non_bios_boot_messages
    [Documentation]  This test is for non bios messages
    [Tags]     1.0.40_non_bios_boot_messages  1-0-40    bios
    [Timeout]  30 min 00 seconds
    Step  1  non_bios_boot_messages_test 

1.0.69_bios_upgrade_via_bmc
    [Documentation]  To verify bios update via bmc
    [Tags]  1.0.69_bios_upgrade_via_bmc  1-0-69  bios
    Step  1  Setup for bios update via bmc
    Step  2  downgrade primary bios through bmc
    Step  3  downgrade secondary bios through bmc
    Step  4  upgrade primary bios through bmc
    Step  5  upgrade secondary bios through bmc
    Step  6  Cleanup for bios update via bmc

1.0.55_ac_power_cycling_stress_test
   [Documentation]   To do ac power cycling stress test and check system stability
   [Tags]     1.0.55_ac_power_cycling_stress_test  1-0-55  bios  
   Step  1  run post stress test scans  DUT  3

1.0.68_power_reset_cause_test
    [Documentation]  To verify power reset cause
    [Tags]  1.0.68_power_reset_cause_test  1-0-68   bios
    Step  1  check_power_reset_cause  DUT  

1.0.64_bmc_network_configuration_test
   [Documentation]   To verify if the BIOS can set and get the BMC network configuration correctly
   [Tags]     1.0.64_bmc_network_configuration_test  1-0-64  bios
   Step  1  validate static ip config
   Step  2  validate dhcp ip config
   [Teardown]  bios_lib.powerCycle_device  DUT

1.0.65_fast_boot_test
   [Documentation]   Temporary testcase for fastboot experimenting
   [Tags]     1.0.65_fast_boot_test  1-0-65  
   Step  1  config fastboot image
   #Step  2  validate fastboot image
   Step  3  cleanup fastboot image

1.0.18_memtest86_diagnostic_test
    [Documentation]  This test is for memtest86 
    [Tags]     1.0.18_memtest86_diagnostic_test  1-0-18
    Step  1  memtest86_test_check  
    #[Teardown]  bios_lib.powerCycle_device  DUT



*** Keywords ***
DiagOS Connect Device
    DiagOSConnect

DiagOS Disconnect Device
    DiagOSDisconnect
