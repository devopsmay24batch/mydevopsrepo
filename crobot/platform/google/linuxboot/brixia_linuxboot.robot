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
Documentation   Brixia common linuxboot suite
Resource        CommonKeywords.resource
#Resource        GoogleCommonKeywords.resource
#Resource        GoogleLinuxBootKeywords.resource
Library         GoogleLinuxBootLib.py
Library         CommonLib.py
Library         ../GoogleCommonLib.py
Library         ../diag/GoogleDiagLib.py
Variables       GoogleLinuxBootVariable.py


Suite Setup     DiagOS Connect Device
Suite Teardown  DiagOS Disconnect Device

*** Test Cases ***
LinuxBoot_TC_001_xxxx
    [Documentation]  This test checks linuxboot info
    [Tags]  LinuxBoot_TC_001_xxxx  brixia
    [Setup]  xxxx
    Step  1  check linuxboot
    Step  2  xxxx
    [Teardown]  xxxx

BRIXIA_LINUXBOOT_TC_03_VERSION_CHECK
   [Documentation]  This test checks the Bios  version
   [Tags]   BRIXIA_LINUXBOOT_TC_03_VERSION_CHECK    brixia
   [Timeout]  15 min 00 seconds
   Step  1   Check Bios version post   new



BRIXIA_LINUXBOOT_TC_07_BUILD_LINUX_KERNEL_CHECK
   [Documentation]  This test checks linux kernel uname command
   [Tags]   BRIXIA_LINUXBOOT_TC_07_BUILD_LINUX_KERNEL_CHECK   brixia  test1
   [Timeout]  5 min 00 seconds
   [Setup]  AC powercycle device
   Step  1  check uname operations


BRIXIA_LINUXBOOT_TC_05_MISC_CHECK
   [Documentation]  This test checks ROM size
   [Tags]   BRIXIA_LINUXBOOT_TC_05_MISC_CHECK   brixia  test2
   [Setup]  AC powercycle device
   [Timeout]  15 min 00 seconds
   Step  1  check flash size



BRIXIA_LINUXBOOT_TC_06_LINUXBOOT_INITIAL_INFORMATION_CHECK
    [Documentation]  This test checks linuxboot boot.
    [Tags]  BRIXIA_LINUXBOOT_TC_06_LINUXBOOT_INITIAL_INFORMATION_CHECK  brixia  test6
    Step  1  boot into linux



BRIXIA_LINUXBOOT_TC_08_CUSTOMIZE_BOOT_SONIC_TEST
    [Documentation]  This test checks sonic boot.
    [Tags]  BRIXIA_LINUXBOOT_TC_08_CUSTOMIZE_BOOT_SONIC_TEST  brixia  test8
    [Timeout]  15mins 00 seconds
    Step  1  boot into sonic
    Step  2  check sonic operation


BRIXIA_LINUXBOOT_TC_34_S0_STATE_TEST
   [Documentation]  This test checks the S0 state of the DUT
   [Tags]   BRIXIA_LINUXBOOT_TC_34_S0_STATE_TEST  brixia
   [Timeout]  20 min 00 seconds
   Step  1  Check sonic operation
   Step  2  AC powercycle device
   Step  3  Check sonic operation

BRIXIA_LINUXBOOT_TC_027_PCIE_Bus_Scan
    [Documentation]  This test checks PCIe bus scan
    [Tags]    BRIXIA_LINUXBOOT_TC_027_PCIE_Bus_Scan  brixia
    Step  1  boot into linuxboots
    Step  2  check PCIe Device Detection  Linuxboot
    Step  3  boot Into Sonic
    Step  4  check PCIe Device Detection  Sonic

BRIXIA_LINUXBOOT_TC_028_PCIE_Configuration_Test
    [Documentation]  This test checks PCIe configuration
    [Tags]    BRIXIA_LINUXBOOT_TC_028_PCIE_Configuration_Test  brixia
    Step  1  boot Into linuxboots
    Step  2  check Linuxboot Pcie Devices
    Step  3  boot into Sonic
    Step  4  check Sonic Pcie Devices
    Step  5  check PCIe Configuration

BRIXIA_LINUXBOOT_TC_029_CPU_I2C/SMBus/SMLink_Interface_Test
    [Documentation]  This test checks CPU I2C Interface Test
    [Tags]    BRIXIA_LINUXBOOT_TC_029_CPU_I2C/SMBus/SMLink_Interface_Test  brixia
    Step  1  boot Into Sonic
    Step  2  scan I2C Buses
    Step  3  check All I2C Device Scan

BRIXIA_LINUXBOOT_TC_030_CPU_LPC_Interface_Test
    [Documentation]  This test checks CPU LPC Interface.
    [Tags]    BRIXIA_LINUXBOOT_TC_030_CPU_LPC_Interface_Test  brixia
    Step  1  boot Into Sonic
    Step  2  check ComE MMC CPLD Version
    FOR  ${i}  IN RANGE  3
        Step  3  read Write CPLD Scratch Register
    END

BRIXIA_LINUXBOOT_TC_031_Management_Port_Information_Check
    [Documentation]  This test checks Management Port Information.
    [Tags]    BRIXIA_LINUXBOOT_TC_031_Management_Port_Information_Check  brixia
    Step  1  boot Into Linuxboots
    Step  2  check VendorId DeviceId  Linuxboot
    Step  3  boot Into Sonic
    Step  4  check VendorId DeviceId

BRIXIA_LINUXBOOT_TC_021_Read_EEPROM_test
    [Documentation]  This test checks EEPROM Test
    [Tags]    BRIXIA_LINUXBOOT_TC_021_Read_EEPROM_test  brixia
    Step  1  boot Into Sonic
    Step  2  check EEPROM Option
    Step  3  dump And Read EEPROM Via Diag And Hexdump
    Step  4  write TLV Information  ${write_tlf_commands1}
    Step  5  dump And Read EEPROM Via Diag And Hexdump
    Step  6  AC Powercycle Device
    Step  7  dump And Read EEPROM Via Diag And Hexdump
    Step  8  write TLV Information  ${write_tlf_commands2}
    Step  9  dump And Read EEPROM Via Diag And Hexdump
    Step  10  AC Powercycle Device
    Step  11  dump And Read EEPROM Via Diag And Hexdump
    Step  12  check EEPROM All Option

BRIXIA_LINUXBOOT_TC_016_Kexe_runtime_kernel_check
    [Documentation]  This test checks Kexe's runtime kernel check.
    [Tags]    BRIXIA_LINUXBOOT_TC_016_Kexe_runtime_kernel_check  brixia
    Step  1  boot Into Sonic
    Step  2  check Kexe Runtime Kernel
    Step  3  AC Powercycle Device Into Linuxboot
    Step  4  boot Into Sonic
    Step  5  check Kexe Runtime Kernel

BRIXIA_LINUXBOOT_TC_24_CPU_Microcode_Test
   [Documentation]  This test checks the CPU Microcode version
   [Tags]   BRIXIA_LINUXBOOT_TC_24_CPU_Microcode_Test  brixia
   [Timeout]  15 min 00 seconds
   Step  1  boot Into Sonic
   Step  2  CPU Microcode ver check

BRIXIA_LINUXBOOT_TC_14_LinuxBoot_cpu_memory_check
   [Documentation]  This test checks the CPU Microcode version
   [Tags]   BRIXIA_LINUXBOOT_TC_14_LinuxBoot_cpu_memory_check  brixia
   [Timeout]  15 min 00 seconds
   Step  1  check cpu and memory info  LinuxBoot
   Step  2  check cpu and memory info  Sonic

BRIXIA_LINUXBOOT_TC_04_Post_information_check
   [Documentation]  This test checks the Post information
   [Tags]   BRIXIA_LINUXBOOT_TC_04_Post_information_check  brixia
   [Timeout]  15 min 00 seconds
   Step  1   Check Post info

BRIXIA_LINUXBOOT_TC_19_LinuxBoot_booting_message_check
   [Documentation]  This test checks the LinuxBoot Version while booting
   [Tags]   BRIXIA_LINUXBOOT_TC_19_LinuxBoot_booting_message_check  brixia
   [Timeout]  15 min 00 seconds
   Step  1  Check LinuxBoot ver   new

BRIXIA_LINUXBOOT_TC_23_CPU_Information_Test
   [Documentation]  This test checks the CPU Information
   [Tags]   BRIXIA_LINUXBOOT_TC_23_CPU_Information_Test  brixia
   [Timeout]  15 min 00 seconds
   Step  1  Cpu information check

BRIXIA_LINUXBOOT_TC_025_CPU_Frequency_Check_Under_Full_Loading
    [Documentation]  This test checks CPU Frequency Check Under Full Loading.
    [Tags]    BRIXIA_LINUXBOOT_TC_025_CPU_Frequency_Check_Under_Full_Loading  brixia
    [Timeout]  730 minute
#    ${time_in_minute}  Set Variable  ${720}
    ${time_in_minute}  Set Variable  ${5}
    Step  1  boot Into Sonic
    Step  2  Change Intel Power Saving  powersave  ${power_saving_dict["powersave"]}
    Step  3  Check List Cpu
    Step  4  Change Intel Power Saving  performance  ${power_saving_dict["performance"]}
    Step  5  Check List Cpu
    Step  6  Monitor Cpu Frequency  ${time_in_minute}

BRIXIA_LINUXBOOT_TC_13_Onie_install_pxeboot_test
   [Documentation]  This test checks the Online install of LinuxBoot
   [Tags]   BRIXIA_LINUXBOOT_TC_13_Onie_install_pxeboot_test  brixia
   Step  1   Onie Install By Pxeboot

BRIXIA_LINUXBOOT_TC_11_Sonic_update_pxeboot_test
   [Documentation]  This test checks the Online install of LinuxBoot
   [Tags]   BRIXIA_LINUXBOOT_TC_11_Sonic_update_pxeboot_test  brixia
   Step  1   Sonic Update By Pxeboot    downgrade
   Step  2   Sonic Update By Pxeboot    upgrade

BRIXIA_LINUXBOOT_TC_02_Online_install_LinuxBoot_BIOS_test
   [Documentation]  This test checks the Online install of LinuxBoot
   [Tags]   BRIXIA_LINUXBOOT_TC_02_Online_install_LinuxBoot_BIOS_test  brixia
   Step  1  Online LinuxBoot Install   old
   Step  2  Check LinuxBoot ver   old
   Step  3  Online LinuxBoot Install   new
   Step  4  Check LinuxBoot ver   new

BRIXIA_LINUXBOOT_TC_41_CPU_WARM_RESET
   [Documentation]  This test checks the CPU Warm Reset
   [Tags]   BRIXIA_LINUXBOOT_TC_41_CPU_WARM_RESET  brixia
   Step  1  CPU Warm Stress Test

BRIXIA_LINUXBOOT_TC_09_SONiC_install_by_pxeboot_test
    [Documentation]  This test checks SONiC install by pxeboot test.
    [Tags]    BRIXIA_LINUXBOOT_TC_09_SONiC_install_by_pxeboot_test  brixia
    Step  1  boot Into Linuxboots
    Step  2  install Sonic with rescue in Pxeboot
    Step  3  check Sonic Basic Functions
    Step  4  auto reboot Into Sonic
    Step  5  check Sonic List  1

BRIXIA_LINUXBOOT_TC_40_AC_Power_Cycle_FPGA
   [Documentation]  This test checks the AC Power cycle stress
   [Tags]   BRIXIA_LINUXBOOT_TC_40_AC_Power_Cycle  brixia
   Step  1  check AC power cycle stress

BRIXIA_LINUXBOOT_TC_44_SATA_interface_R_W_Stress_Test
   [Documentation]  This test checks the SATA interface R/W
   [Tags]   BRIXIA_LINUXBOOT_TC_44_SATA_interface_R_W_Stress_Test   brixia
   Step  1  SATA Interface R W stress

#TC_43 will run for more than 12 hrs
BRIXIA_LINUXBOOT_TC_43_Memory_Stress_Test
   [Documentation]  This test checks the Memory Stress
   [Tags]   BRIXIA_LINUXBOOT_TC_43_Memory_Stress_Test  brixia
   [Timeout]  730 minute
   Step  1  Check Memory stress

BRIXIA_LINUXBOOT_TC_042_CPU_Stress_Test
    [Documentation]  This test checks CPU Stress.
    [Tags]    BRIXIA_LINUXBOOT_TC_042_CPU_Stress_Test  brixia
#    ${time_in_minute}  Set Variable  ${12*60}
    ${time_in_minute}  Set Variable  ${5}
    Step  1  boot Into Sonic
    Step  2  run CPU Stress Test  ${time_in_minute}

BRIXIA_LINUXBOOT_TC_12_SONiC_uninstall_test
    [Documentation]  This test checks SONiC uninstall test.
    [Tags]    BRIXIA_LINUXBOOT_TC_12_SONiC_uninstall_test  brixia
    Step  1  boot Into Sonic
    Step  2  install Previous Sonic OS
    Step  3  boot Into Linuxboots
    Step  4  boot Into Sonic With Args  old
    Step  5  check Sonic Version  old
    Step  6  boot Into Linuxboots
    Step  7  boot Into Sonic With Args
    Step  8  check Sonic Version
    Step  9  uninstall Old Sonic
    Step  10  boot Into Linuxboots
    Step  11  check Linuxboot Menu And Boot Into Sonic
    Step  12  check Sonic Version  new  final

BRIXIA_LINUXBOOT_TC_15_Boot_kernel_initialize_devices_check
   [Documentation]  This test checks the device  list
   [Tags]   BRIXIA_LINUXBOOT_TC_15_Boot_kernel_initialize_devices_check   brixia
   Step  1  Device info check


*** Keywords ***
DiagOS Connect Device
    DiagOSConnect

DiagOS Disconnect Device
    DiagOSDisconnect
