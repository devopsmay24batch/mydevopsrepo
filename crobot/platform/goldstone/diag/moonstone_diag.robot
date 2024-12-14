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
Documentation   MOONSTONE common diagnostic suite
Resource        CommonKeywords.resource
Resource        MoonstoneDiagKeywords.resource
Library         MoonstoneDiagLib.py
Library         CommonLib.py
Library         ../MOONSTONECommonLib.py
Variables       MoonstoneDiagVariable.py


Suite Setup   DIAG OS Connect Device
Suite Teardown  DIAG OS Disconnect Device

*** Test Cases ***
MOONSTONE_TC_1.0.1_Install_Diag_Package_Test
   [Documentation]  This test check diag installation
   [Tags]  MOONSTONE_DIAG_TC_1.0.1_Install_Diag_Package_Test  moonstone  diag  smoke
   Step  1  diag installation  ${diag_image}
   Step  2  go to diag path
   Step  3  check Version  ${diag}  ${diag_version}


MOONSTONE_TC_1.0.2_Update_Diag_Package_Test
   [Documentation]  Check the diag update
   [Tags]  MOONSTONE_DIAG_TC_1.0.2_Update_Diag_Package_Test  moonstone  diag  smoke
   Step  1  diag installation  ${old_image}
   Step  2  go to diag path
   Step  3  check Version  ${diag}  ${old_version}
   Step  4  diag installation  ${diag_image}
   Step  5  go to diag path
   Step  6  check Version  ${diag}  ${diag_version}

  	
MOONSTONE_DIAG_TC_1.0.3_UPGRADE_TEST
   [Documentation]  This test checks upgrade for fpga.
   [Tags]  MOONSTONE_DIAG_TC_1.0.3_UPGRADE_TEST  moonstone  diag  smoke
   Step  1  check upgrade test  DUT  ${fpga}  ${fpga_image}  ${fpga_upgrade_version}  3


MOONSTONE_DIAG_TC_1.0.4_UPGRADE_TEST
   [Documentation]  This test checks upgrade for bios.
   [Tags]  MOONSTONE_DIAG_TC_1.0.4_UPGRADE_TEST  moonstone  diag  smoke
   Step  1  check upgrade test  DUT  ${bios}  ${bios_image}  ${bios_upgrade_version}  1


MOONSTONE_DIAG_TC_1.0.5_UPGRADE_TEST
   [Documentation]  This test checks upgrade for cpld.
   [Tags]  MOONSTONE_DIAG_TC_1.0.5_UPGRADE_TEST  moonstone  diag  smoke
   Step  1  check upgrade test  DUT  ${cpld}  ${cpld_image}  ${cpld_upgrade_version}  2


MOONSTONE_DIAG_TC_1.0.7_SYSINFO_TEST
   [Documentation]  This test checks sysinfo test
   [Tags]  MOONSTONE_DIAG_TC_1.0.7_SYSINFO_TEST  moonstone  diag   smoke
   Step  1  go to diag path
   Step  2  check sysinfo test
   Step  3  check version  ${sysinfo}  ${sysinfo_version}
   Step  4  check list  ${sysinfo}  ${sysinfo_list}
   Step  5  check help  ${sysinfo}  ${sysinfo_help}


MOONSTONE_DIAG_1.0.8_MAC_TEST
   [Documentation]  MOONSTONE_DIAG_1.0.8_MAC_TEST
   [Tags]  MOONSTONE_DIAG_TC_1.0.8_MAC_TEST  moonstone   diag
   Step  1  check mac test 


MOONSTONE_DIAG_TC_1.0.10_TLV_EEPROM_TEST
   [Documentation]  This test checks tlv eeprom test
   [Tags]   MOONSTONE_DIAG_TC_1.0.10_TLV_EEPROM_TEST  moonstone  diag
   Step  1  go to diag path
   Step  2  check version  ${eeprom}  ${eeprom_version}
   Step  3  check list  ${eeprom}  ${eeprom_list}
   Step  4  check help  ${eeprom}  ${eeprom_help}
   Step  5  check eeprom test


MOONSTONE_DIAG_1.0.12_FPGA_CPLD_TEST
   [Documentation]  This test checks fpgs and cpld access and version
   [Tags]  MOONSTONE_DIAG_TC_1.0.12_FPGA_CPLD_TEST  moonstone   diag
   Step  1  go to diag path
   Step  2  check version  ${cpld}  ${cpld_version}
   Step  3  check help  ${cpld}  ${bbcpld_help}
   Step  4  check bbcpld test
   Step  5  check list  ${cpld}  ${bbcpld_list}
   Step  6  write bbcpld scratch reg
   Step  7  check version  ${fpga}  ${fpga_version}
   Step  8  check help  ${fpga}  ${fpga_help}
   Step  9  check fpga test
   Step  10  check list  ${fpga}  ${fpga_list}


MOONSTONE_DIAG_1.0.15_OSFP-SFP-EEPROM_TEST
   [Documentation]  MOONSTONE_DIAG_1.0.15_OSFP-SFP-EEPROM_TEST
   [Tags]  MOONSTONE_DIAG_TC_1.0.15_OSFP-SFP-EEPROM_TEST  moonstone   diag
   Step  1  go to diag path
   Step  2  check help  ${sfp}  ${sfp_help}
   Step  3  check list  ${sfp}  ${sfp_list}
   Step  4  check test  ${sfp}
   Step  5  check sfp hpmode
   Step  6  check sfp lpmode

MOONSTONE_DIAG_1.0.18_RTC_TEST
   [Documentation]  MOONSTONE_DIAG_1.0.18_RTC_TEST
   [Tags]  MOONSTONE_DIAG_TC_1.0.18_RTC_TEST  moonstone   diag
   Step  1  go to diag path
   Step  2  check help  ${rtc}  ${rtc_help}
   Step  3  check version  ${rtc}  ${rtc_version}
   Step  4  check test  ${rtc}
   Step  5  check rtc operation


MOONSTONE_DIAG_1.0.19_PCIE_TEST
   [Documentation]  MOONSTONE_DIAG_1.0.19_PCIE_TEST
   [Tags]  MOONSTONE_DIAG_TC_1.0.19_PCIE_TEST  moonstone   diag
   Step  1  go to diag path
   Step  2  check help  ${pci}  ${pci_help}
   Step  3  check version  ${pci}  ${pci_version}
   Step  4  check list  ${pci}  ${pci_list}
   Step  5  check pci test  


MOONSTONE_DIAG_1.0.20_CPU_INFO_TEST
   [Documentation]  MOONSTONE_DIAG_1.0.20_CPU_INFO_TEST
   [Tags]  MOONSTONE_DIAG_TC_1.0.20_CPU_INFO_TEST  moonstone   diag
   Step  1  go to diag path
   Step  2  check help  ${cpu}  ${cpu_help}
   Step  3  check version  ${cpu}  ${cpu_version}
   Step  4  check list  ${cpu}  ${cpu_list}
   Step  5  check test  ${cpu}


MOONSTONE_DIAG_1.0.21_FAN_TEST
   [Documentation]  MOONSTONE_DIAG_1.0.21_FAN_TEST
   [Tags]  MOONSTONE_DIAG_TC_1.0.21_FAN_TEST  moonstone   diag
   Step  1  go to diag path
   Step  2  check help  ${fan}  ${fan_help}
   Step  3  check list  ${fan}  ${fan_list}
   Step  4  check fan test


MOONSTONE_DIAG_TC_1.0.22_UART_Mux_Test
   [Documentation]  This test checks switch between come and bmc
   [Tags]  MOONSTONE_DIAG_TC_1.0.22_UART_Mux_Test  moonstone  diag   smoke
   Step  1  check the uart  DUT


MOONSTONE_DIAG_TC_1.0.24_UART_Internal_TEST
   [Documentation]  This test checks for UART
   [Tags]   MOONSTONE_DIAG_TC_1.0.24_UART_Internal_TEST   moonstone  diag  smoke
   Step  1  go to diag path
   Step  2  check help  ${uart}  ${uart_help}
   Step  3  check version  ${uart}  ${uart_version}
   Step  4  check the uart test  ${uart}


MOONSTONE_DIAG_1.0.25_STORAGE_TEST
   [Documentation]  MOONSTONE_DIAG_1.0.25_STORAGE_TEST
   [Tags]  MOONSTONE_DIAG_TC_1.0.25_STRAGETEST   moonstone   diag
   Step  1  check version  ${storage}  ${storage_version}
   Step  2  check help  ${storage}  ${storage_help}
   Step  3  check test  ${storage}


MOONSTONE_DIAG_1.0.27_PHY_TEST
   [Documentation]  MOONSTONE_DIAG_1.0.27_PHY_TEST
   [Tags]  MOONSTONE_DIAG_TC_1.0.27_PHY_TEST  moonstone   diag
   Step  1  go to diag path
   Step  2  check phy test
   Step  3  validate phy  ${phy_speed}  ${phy_mode}


MOONSTONE_DIAG_1.0.30_CPU-I2C-BUS_TEST
   [Documentation]  MOONSTONE_DIAG_1.0.30_CPU-I2C-BUS_TEST
   [Tags]  MOONSTONE_DIAG_TC_1.0.30_CPU-I2C-BUS_TEST  moonstone   diag
   Step  1  go to diag path
   Step  3  check help  ${i2c}  ${i2c_help}
   Step  2  check version  ${i2c}  ${i2c_version}
   Step  4  check test  ${i2c}
   Step  5  check list  ${i2c}  ${i2c_list}
   Step  6  check i2c operation


MOONSTONE_DIAG_1.0.31_FPGA_TEST
   [Documentation]  MOONSTONE_DIAG_1.0.31_FPGA_TEST
   [Tags]  MOONSTONE_DIAG_TC_1.0.31_FPGA_TEST  moonstone   diag
   Step  1  go to diag path
   Step  2  check version  ${fpga}  ${fpga_version}
   Step  3  check help  ${fpga}  ${fpga_help}
   Step  4  check fpga test
   Step  5  check list  ${fpga}  ${fpga_list}


MOONSTONE_DIAG_1.0.33_SPD_TEST
   [Documentation]  MOONSTONE_DIAG_1.0.33_SPD_TEST
   [Tags]  MOONSTONE_DIAG_TC_1.0.33_SPD_TEST  moonstone   diag
   Step  1  go to diag path
   Step  2  check memory test
   Step  3  check list  ${mem}  ${mem_list}


MOONSTONE_DIAG_1.0.35_TPM_TEST
   [Documentation]  MOONSTONE_DIAG_1.0.35_TPM_TEST
   [Tags]  MOONSTONE_DIAG_TC_1.0.35_TPM_TEST  moonstone   diag
   Step  1  check test  ${tpm}


#MOONSTONE_DIAG_1.0.37_EEPROM-FRU_TEST
#   [Documentation]  MOONSTONE_DIAG_1.0.37_EEPROM-FRU_TEST 
#   [Tags]  MOONSTONE_DIAG_1.0.37_EEPROM-FRU_TEST  moonstone   diag
#   Step  1  go to diag path
#   Step  2  check help  ${eeprom_fru}  ${eeprom_fru_help}
#   Step  3  check list  ${eeprom_fru}  ${eeprom_fru_list}

MOONSTONE_DIAG_1.0.37_EEPROM-FRU_TEST
   [Documentation]  MOONSTONE_DIAG_1.0.37_EEPROM-FRU_TEST 
   [Tags]  MOONSTONE_DIAG_TC_1.0.37_EEPROM-FRU_TEST  moonstone   diag
   Step  1  go to diag path
   Step  2  check fru  ${eeprom_bmc}  ${eeprom_bmc_dump}  
   Step  3  check help  ${eeprom_bmc}  ${eeprom_bmc_help}
   Step  4  check list  ${eeprom_bmc}  ${eeprom_bmc_list}


MOONSTONE_DIAG_1.0.38_CPU-DDR-SSD-STRESS_TEST
   [Documentation]  MOONSTONE_DIAG_1.0.38_CPU-DDR-SSD-STRESS_TEST
   [Tags]  MOONSTONE_DIAG_TC_1.0.38_CPU-DDR-SSD-STRESS_TEST  moonstone   diag
   Step  1  go to diag path   tools
   Step  2  check stress  sda1
   Step  3  check stress  sdb1



*** Keywords ***
DiagOS Connect Device
    DiagOSConnect

DiagOS Disconnect Device
    DiagOSDisconnect

ServerOS Connect Device
    ServerOsConnect

ServerOS Disconnect Device
    ServerOsDisConnect
                    
 
