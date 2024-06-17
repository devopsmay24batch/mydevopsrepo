
###############################################################################
# LEGALESE:   "Copyright (C) 2019_2020, Celestica Corp. All rights reserved." #
#                                                                             #
# This source code is confidential, proprietary, and contains trade           #
# secrets that are the sole property of Celestica Corp.                       #
# Copy and/or distribution of this source code or disassembly or reverse      #
# engineering of the resultant object code are strictly forbidden without     #
# the written consent of Celestica Corp.                                      #
#                                                                             #
###############################################################################
#######################################################################################################################
# Script       : minipack2_diag.robot                                                                                  #
# Date         : April 22, 2020                                                                                       #
# Author       : TK                                                                                                   #
# Description  : This script will validate all Diag OS EDA tools                                                      #
#                                                                                                                     #
# Script Revision Details:                                                                                            #

#######################################################################################################################

*** Settings ***
Documentation   This Suite will validate all Diag OS

Library           Keyword_Resource.py
Resource          Resource.robot
Library           DiagLib.py  DUT
Library           DiagLibAdapter.py
Variables         Diag_OS_variable.py


Suite Setup       Diag Connect Device
Suite Teardown    Diag Disconnect Device

*** Variables ***
${LoopCnt}        1
${MaxLoopNum}     2

*** Test Cases ***
Meta_Minerva_DIAG_TC_001_Diag_Script_install_reinstall_Test
   [Documentation]  This is to install/reinstall diag .
   [Tags]  Meta_Minerva_DIAG_TC_001_Diag_Script_install_reinstall_Test  minerva  test1  
   Step  1  Prepare_images  DUT  ${DIAG_workspace}  DIAG
   Step  2  minerva_diag_install_reinstall  DUT  ${minerva_diag_new_image}  ${minerva_diag_new_version}
   [Teardown]  cleanup_device_after_update  DUT
    
Meta_Minerva_DIAG_TC_002_Diag_Script_Interactive_UI_Check
   [Documentation]  Check diag interactive UI interface submenus
   [Tags]  Meta_Minerva_DIAG_TC_002_Diag_Script_Interactive_UI_Check  minerva  test2  
   Step  1  check_unidiag_system_versions  DUT  
   Step  2  check_minerva_diag_script_ui_submenu  DUT
   [Teardown]  exit_unidiag_interface  DUT 

Meta_Minerva_DIAG_TC_003_System_Version
   [Documentation]  This is to check system versions.
   [Tags]  Meta_Minerva_DIAG_TC_003_System_Version  minerva  test3  
   Step  1  check_unidiag_system_versions  DUT  
   Step  2  check_minerva_system_versions  DUT
   [Teardown]  exit_unidiag_interface  DUT

Meta_Minerva_DIAG_TC_004_I2C_Devices_Scan_Test
   [Documentation]  This is to verify I2c scan for system.
   [Tags]  Meta_Minerva_DIAG_TC_004_I2C_Devices_Scan_Test  minerva  test4  
   Step  1  check_unidiag_system_versions  DUT  
   Step  2  check_system_i2c_scan   DUT  
   [Teardown]  exit_unidiag_interface  DUT

Meta_Minerva_DIAG_TC_005_SPI_Devices_Scan_Test
   [Documentation]  This is to verify SPI scan for system.
   [Tags]  Meta_Minerva_DIAG_TC_005_SPI_Devices_Scan_Test  minerva  test5  
   Step  1  check_unidiag_system_versions  DUT  
   Step  2  check_system_spi_scan   DUT  
   [Teardown]  exit_unidiag_interface  DUT

Meta_Minerva_DIAG_TC_006_PCIe_Devices_Scan_Test
   [Documentation]  This is for system PCIE scan test.
   [Tags]  Meta_Minerva_DIAG_TC_006_PCIe_Devices_Scan_Test  minerva  test6  
   Step  1  check_unidiag_system_versions  DUT  
   Step  2  check_system_pcie_scan   DUT  
   [Teardown]  exit_unidiag_interface  DUT

Meta_Minerva_DIAG_TC_007_GPIO_Devices_Scan_Test
   [Documentation]  This is for system GPIO Devices scan test.
   [Tags]  Meta_Minerva_DIAG_TC_007_GPIO_Devices_Scan_Test  minerva  test7  
   Step  1  check_unidiag_system_versions  DUT  
   Step  2  check_system_gpio_device_scan   DUT  
   [Teardown]  exit_unidiag_interface  DUT

Meta_Minerva_DIAG_TC_011_USB_Network_Test
   [Documentation]  This is for system USB Network test.
   [Tags]  Meta_Minerva_DIAG_TC_011_USB_Network_Test  minerva  test11  
   Step  1  check_unidiag_system_versions  DUT  
   Step  2  check_minerva_system_usb_network_test  DUT 
   Step  3  exit_unidiag_interface  DUT 
   Step  4  check_ping_from_bmc_come  DUT  10

Meta_Minerva_DIAG_TC_012_COMe_MAC_Addr_check
   [Documentation]  This is for Come mac address check test.
   [Tags]  Meta_Minerva_DIAG_TC_012_COMe_MAC_Addr_check  minerva  test12  
   Step  1  check_unidiag_system_versions  DUT  
   Step  2  check_minerva_system_come_mac_address  DUT 
   [Teardown]  Run Keyword If Test Failed  exit_unidiag_interface  DUT

Meta_Minerva_DIAG_TC_013_BMC_MAC_Addr_check
   [Documentation]  This is for bmc mac address check test.
   [Tags]  Meta_Minerva_DIAG_TC_013_BMC_MAC_Addr_check  minerva  test13  
   Step  1  check_unidiag_system_versions  DUT  
   Step  2  check_minerva_system_bmc_mac_address  DUT 
   [Teardown]  Run Keyword If Test Failed  exit_unidiag_interface  DUT

Meta_Minerva_DIAG_TC_014_MDIO_Test
   [Documentation]  This is for MDIO test.
   [Tags]  Meta_Minerva_DIAG_TC_014_MDIO_Test  minerva  test14  
   Step  1  check_unidiag_system_versions  DUT  
   Step  2  check_system_mdio_test   DUT  
   [Teardown]  exit_unidiag_interface  DUT
 
Meta_Minerva_DIAG_TC_015_LPC_Test
   [Documentation]  This is for system LPC test.
   [Tags]  Meta_Minerva_DIAG_TC_015_LPC_Test  minerva  test15  
   Step  1  check_unidiag_system_versions  DUT  
   Step  2  check_system_lpc_test   DUT  
   Step  3  exit_unidiag_interface  DUT
   Step  4  check_lpc_through_ipmitool  DUT
   [Teardown]  exit_unidiag_interface  DUT

Meta_Minerva_DIAG_TC_016_OOB_Switch_Test
   [Documentation]  This is to OOB test for system.
   [Tags]  Meta_Minerva_DIAG_TC_016_OOB_Switch_Test  minerva  test16  
   Step  1  check_unidiag_system_versions  DUT  
   Step  2  check_minerva_system_oob_test  DUT
   [Teardown]  exit_unidiag_interface  DUT

Meta_Minerva_DIAG_TC_017_OSFP_QSFP_PORTS_I2C_Scan_Test
   [Documentation]  This is for OSFP/QSFP port I2C scan test .
   [Tags]  Meta_Minerva_DIAG_TC_017_OSFP_QSFP_PORTS_I2C_Scan_Test  minerva  test17  
   Step  1  check_unidiag_system_versions  DUT  
   Step  2  get_into_minerva_osfp_submenu  DUT
   Step  3  check_minerva_osfp_i2c_scan  DUT 
   [Teardown]  exit_unidiag_interface  DUT

Meta_Minerva_DIAG_TC_018_OSFP_QSFP_PORTS_Enable
   [Documentation]  This is for OSFP/QSFP port enable test .
   [Tags]  Meta_Minerva_DIAG_TC_018_OSFP_QSFP_PORTS_Enable  minerva  test18  
   Step  1  check_unidiag_system_versions  DUT  
   Step  2  get_into_minerva_osfp_submenu  DUT
   Step  3  check_osfp_port_enable  DUT  
   [Teardown]  exit_unidiag_interface  DUT

Meta_Minerva_DIAG_TC_019_OSFP_QSFP_PORTS_Disable
   [Documentation]  This is to OSFP port disable test .
   [Tags]  Meta_Minerva_DIAG_TC_019_OSFP_QSFP_PORTS_Disable  minerva  test19  
   Step  1  check_unidiag_system_versions  DUT 
   Step  2  get_into_minerva_osfp_submenu    DUT
   Step  3  check_osfp_port_disable  DUT  
   [Teardown]  exit_unidiag_interface  DUT

Meta_Minerva_DIAG_TC_020_OSFP_QSFP_PORTS_Present_Check
   [Documentation]  This is to OSFP ports present check .
   [Tags]  Meta_Minerva_DIAG_TC_020_OSFP_QSFP_PORTS_Present_Check  minerva  test20  
   Step  1  check_unidiag_system_versions  DUT  
   Step  2  get_into_minerva_osfp_submenu  DUT
   Step  3  check_osfp_port_present  DUT  
   [Teardown]  exit_unidiag_interface  DUT

Meta_Minerva_DIAG_TC_021_OSFP_QSFP_PORTS_Reset_Check
   [Documentation]  This is to verify OSFP ports reset check
   [Tags]  Meta_Minerva_DIAG_TC_021_OSFP_QSFP_PORTS_Reset_Check  minerva  test21  
   Step  1  check_unidiag_system_versions  DUT  
   Step  2  get_into_minerva_osfp_submenu  DUT
   Step  3  check_osfp_port_disable  DUT  
   Step  4  check_minerva_osfp_port_reset_check  DUT  
   Step  5  check_osfp_port_enable  DUT  
   Step  6  check_minerva_osfp_port_reset_check  DUT  True
   Step  7  check_minerva_osfp_port_unreset_test  DUT  
   Step  8  check_minerva_osfp_port_reset_check  DUT  
   Step  9  check_minerva_osfp_port_reset_test  DUT  
   Step  10  check_minerva_osfp_port_reset_check  DUT  True
   [Teardown]  exit_unidiag_interface  DUT

Meta_Minerva_DIAG_TC_022_OSFP_QSFP_PORTS_LPMODE_Check
   [Documentation]  This is to OSFP ports lpmode check .
   [Tags]  Meta_Minerva_DIAG_TC_022_OSFP_QSFP_PORTS_LPMODE_Check  minerva  test22  
   Step  1  check_unidiag_system_versions  DUT  
   Step  2  get_into_minerva_osfp_submenu  DUT
   Step  3  check_osfp_port_lpmode_test  DUT  
   Step  4  check_osfp_port_lpmode_check  DUT  True
   [Teardown]  exit_unidiag_interface  DUT

Meta_Minerva_DIAG_TC_023_OSFP_QSFP_PORTS_INT_Check
   [Documentation]  This is to OSFP ports INT check .
   [Tags]  Meta_Minerva_DIAG_TC_023_OSFP_QSFP_PORTS_INT_Check  minerva  test23  
   Step  1  check_unidiag_system_versions  DUT  
   Step  2  get_into_minerva_osfp_submenu  DUT
   Step  3  check_osfp_port_int_check  DUT  
   [Teardown]  exit_unidiag_interface  DUT

Meta_Minerva_DIAG_TC_024_OSFP_QSFP_PORTS_RESET_Test
   [Documentation]  This is to OSFP ports reset test .
   [Tags]  Meta_Minerva_DIAG_TC_024_OSFP_QSFP_PORTS_RESET_Test  minerva  test24  
   Step  1  check_unidiag_system_versions  DUT  
   Step  2  get_into_minerva_osfp_submenu  DUT
   Step  3  check_minerva_osfp_port_reset_test  DUT  5
   [Teardown]  exit_unidiag_interface  DUT

Meta_Minerva_DIAG_TC_025_OSFP_QSFP_PORTS_UNRESET_Test
   [Documentation]  This is to OSFP ports unreset test.
   [Tags]  Meta_Minerva_DIAG_TC_025_OSFP_QSFP_PORTS_UNRESET_Test  minerva  test25  
   Step  1  check_unidiag_system_versions  DUT  
   Step  2  get_into_minerva_osfp_submenu  DUT
   Step  3  check_minerva_osfp_port_unreset_test  DUT  5
   [Teardown]  exit_unidiag_interface  DUT

Meta_Minerva_DIAG_TC_026_OSFP_QSFP_PORTS_LPMODE_Test
   [Documentation]  This is to OSFP ports lpmode test .
   [Tags]  Meta_Minerva_DIAG_TC_026_OSFP_QSFP_PORTS_LPMODE_Test  minerva  test26  
   Step  1  check_unidiag_system_versions  DUT  
   Step  2  get_into_minerva_osfp_submenu  DUT
   Step  3  check_osfp_port_lpmode_test  DUT  
   [Teardown]  exit_unidiag_interface  DUT

Meta_Minerva_DIAG_TC_027_OSFP_QSFP_PORTS_HPMODE_Test
   [Documentation]  This is to OSFP ports HPMODE test .
   [Tags]  Meta_Minerva_DIAG_TC_027_OSFP_QSFP_PORTS_HPMODE_Test  minerva  test27  
   Step  1  check_unidiag_system_versions  DUT  
   Step  2  get_into_minerva_osfp_submenu  DUT
   Step  3  check_osfp_port_hpmode_test  DUT  
   [Teardown]  exit_unidiag_interface  DUT

Meta_Minerva_DIAG_TC_028_OSFP_QSFP_PORTS_temperature_Check
   [Documentation]  This is to OSFP ports temperature check.
   [Tags]  Meta_Minerva_DIAG_TC_028_OSFP_QSFP_PORTS_temperature_Check  minerva  test28  
   Step  1  check_unidiag_system_versions  DUT  
   Step  2  get_into_minerva_osfp_submenu  DUT
   Step  3  check_osfp_port_enable  DUT 
   Step  4  check_osfp_port_temperature_check  DUT 
   Step  5  check_osfp_port_disable  DUT  
   [Teardown]  exit_unidiag_interface  DUT

Meta_Minerva_DIAG_TC_029_OSFP_QSFP_PORTS_Voltage_Check
   [Documentation]  This is to OSFP ports voltage check.
   [Tags]  Meta_Minerva_DIAG_TC_029_OSFP_QSFP_PORTS_Voltage_Check  minerva  test29  
   Step  1  check_unidiag_system_versions  DUT  
   Step  2  get_into_minerva_osfp_submenu  DUT
   Step  3  check_osfp_port_enable  DUT  
   Step  4  check_osfp_port_voltage_check  DUT 
   Step  5  check_osfp_port_disable  DUT  
   [Teardown]  exit_unidiag_interface  DUT

Meta_Minerva_DIAG_TC_030_OSFP_QSFP_PORTS_Current_Check
   [Documentation]  This is to OSFP ports current check.
   [Tags]  Meta_Minerva_DIAG_TC_030_OSFP_QSFP_PORTS_Current_Check  minerva  test30  
   Step  1  check_unidiag_system_versions  DUT  
   Step  2  get_into_minerva_osfp_submenu  DUT
   Step  3  check_osfp_port_enable  DUT  
   Step  4  check_osfp_port_current_check  DUT 
   Step  5  check_osfp_port_disable  DUT  
   [Teardown]  exit_unidiag_interface  DUT

Meta_Minerva_DIAG_TC_031_System_Power_Status
   [Documentation]  This is for system power status test .
   [Tags]  Meta_Minerva_DIAG_TC_031_System_Power_Status  minerva  test31  
   Step  1  check_unidiag_system_versions  DUT  
   Step  2  check_unidiag_system_power_status  DUT
   [Teardown]  Run Keyword If Test Failed  exit_unidiag_interface  DUT

Meta_Minerva_DIAG_TC_032_System_Power_cycle_test
   [Documentation]  This is for system power cycle test.
   [Tags]  Meta_Minerva_DIAG_TC_032_System_Power_cycle_test  minerva  test32   
   Step  1  check_unidiag_system_versions  DUT  
   Step  2  check_unidiag_system_power_cycle_test  DUT
   [Teardown]  Run Keyword If Test Failed  exit_unidiag_interface  DUT

Meta_Minerva_DIAG_TC_033_COMe_Power_cycle_test
   [Documentation]  This is for COMe power cycle test .
   [Tags]  Meta_Minerva_DIAG_TC_033_COMe_Power_cycle_test  minerva  test33  
   Step  1  check_unidiag_system_versions  DUT  
   Step  2  check_unidiag_come_power_cycle_test  DUT
   [Teardown]  Run Keyword If Test Failed  exit_unidiag_interface  DUT

Meta_Minerva_DIAG_TC_034_Show_IOB_FPGA_Version
   [Documentation]  This is to show IOB FPGA Version .
   [Tags]  Meta_Minerva_DIAG_TC_034_Show_IOB_FPGA_Version  minerva  test34  
   Step  1  check_unidiag_fpga_iob_version  DUT 
   [Teardown]  exit_unidiag_interface  DUT 

Meta_Minerva_DIAG_TC_035_IOB_Scratch_Test
   [Documentation]  This is for FPGA IOB scratch test.
   [Tags]  Meta_Minerva_DIAG_TC_035_IOB_Scratch_Test  minerva  test35  
   Step  1  check_unidiag_system_versions  DUT  
   Step  2  check_unidiag_fpga_iob_scratch_test  DUT 
   [Teardown]  exit_unidiag_interface  DUT

Meta_Minerva_DIAG_TC_036_Show_DOM_FPGA_Version
   [Documentation]  This is for verifying DOM FPGA version.
   [Tags]  Meta_Minerva_DIAG_TC_036_Show_DOM_FPGA_Version  minerva  test36  
   Step  1  check_unidiag_fpga_dom_version  DUT 
   [Teardown]  exit_unidiag_interface  DUT 

Meta_Minerva_DIAG_TC_037_DOM_Scratch_Test
   [Documentation]  This is for FPGA DOM scratch test.
   [Tags]  Meta_Minerva_DIAG_TC_037_DOM_Scratch_Test  minerva  test37  
   Step  1  check_unidiag_system_versions  DUT  
   Step  2  check_unidiag_fpga_dom_scratch_test  DUT 
   [Teardown]  exit_unidiag_interface  DUT

Meta_Minerva_DIAG_TC_038_Show_SMB_CPLD_1_Version
   [Documentation]  This is to show SMB CPLD1 Version .
   [Tags]  Meta_Minerva_DIAG_TC_038_Show_SMB_CPLD_1_Version  minerva  test38  
   Step  1  check_unidiag_cpld1_smb_version  DUT 
   [Teardown]  exit_unidiag_interface  DUT

Meta_Minerva_DIAG_TC_039_SMB_CPLD_1_Scratch_Test
   [Documentation]  This is for CPLD1 SMB scratch test .
   [Tags]  Meta_Minerva_DIAG_TC_039_SMB_CPLD_1_Scratch_Test  minerva  test39  
   Step  1  check_unidiag_system_versions  DUT  
   Step  2  check_unidiag_cpld1_smb_scratch_test  DUT 
   [Teardown]  exit_unidiag_interface  DUT

Meta_Minerva_DIAG_TC_040_Show_SMB_CPLD_2_Version
   [Documentation]  This is to show SMB CPLD2 Version .
   [Tags]  Meta_Minerva_DIAG_TC_040_Show_SMB_CPLD_2_Version  minerva  test40  
   Step  1  check_unidiag_cpld2_smb_version  DUT 
   [Teardown]  exit_unidiag_interface  DUT

Meta_Minerva_DIAG_TC_041_SMB_CPLD_2_Scratch_Test
   [Documentation]  This is for CPLD2 SMB scratch test .
   [Tags]  Meta_Minerva_DIAG_TC_041_SMB_CPLD_2_Scratch_Test  minerva  test41  
   Step  1  check_unidiag_system_versions  DUT  
   Step  2  check_unidiag_cpld2_smb_scratch_test  DUT 
   [Teardown]  exit_unidiag_interface  DUT

Meta_Minerva_DIAG_TC_042_Show_PWR_CPLD_Version
   [Documentation]  This is to show PWR CPLD Version .
   [Tags]  Meta_Minerva_DIAG_TC_042_Show_PWR_CPLD_Version  minerva  test42  
   Step  1  check_unidiag_cpld_pwr_version  DUT 
   [Teardown]  exit_unidiag_interface  DUT

Meta_Minerva_DIAG_TC_043_PWR_CPLD_Scratch_Test
   [Documentation]  This is for CPLD PWR scratch test .
   [Tags]  Meta_Minerva_DIAG_TC_043_PWR_CPLD_Scratch_Test  minerva  test43  
   Step  1  check_unidiag_system_versions  DUT  
   Step  2  check_unidiag_cpld_pwr_scratch_test  DUT 
   [Teardown]  exit_unidiag_interface  DUT

Meta_Minerva_DIAG_TC_044_SMB_Board_I2C_Devices_Scan_Test
   [Documentation]  This is for Board SMB I2C scan test .
   [Tags]  Meta_Minerva_DIAG_TC_044_SMB_Board_I2C_Devices_Scan_Test  minerva  test44  
   Step  1  check_unidiag_system_versions  DUT  
   Step  2  check_unidiag_smb_board_i2c_scan_test  DUT 
   [Teardown]  exit_unidiag_interface  DUT

Meta_Minerva_DIAG_TC_045_SMB_Board_SPI_Devices_Scan_Test
   [Documentation]  This is for Board SMB SPI scan test .
   [Tags]  Meta_Minerva_DIAG_TC_045_SMB_Board_SPI_Devices_Scan_Test  minerva  test45  
   Step  1  check_unidiag_system_versions  DUT  
   Step  2  check_unidiag_smb_board_spi_scan_test  DUT 
   [Teardown]  exit_unidiag_interface  DUT

Meta_Minerva_DIAG_TC_046_SMB_Board_PCIe_Devices_Scan_Test
   [Documentation]  This is for Board SMB PCIe scan test .
   [Tags]  Meta_Minerva_DIAG_TC_046_SMB_Board_PCIe_Devices_Scan_Test  minerva  test46  
   Step  1  check_unidiag_system_versions  DUT  
   Step  2  check_unidiag_smb_board_pcie_scan_test  DUT 
   [Teardown]  exit_unidiag_interface  DUT

Meta_Minerva_DIAG_TC_047_SMB_Board_NVMe_Test
   [Documentation]  This is for Board SMB NVMe test .
   [Tags]  Meta_Minerva_DIAG_TC_047_SMB_Board_NVMe_Test  minerva  test47  
   Step  1  check_unidiag_system_versions  DUT  
   Step  2  check_unidiag_smb_board_nvme_test  DUT 
   [Teardown]  exit_unidiag_interface  DUT

Meta_Minerva_DIAG_TC_048_PDB_Board_I2C_Devices_Scan_Test
   [Documentation]  This is for PDB Board I2Cscan test .
   [Tags]  Meta_Minerva_DIAG_TC_048_PDB_Board_I2C_Devices_Scan_Test  minerva  test48  
   Step  1  check_unidiag_system_versions  DUT  
   Step  2  check_unidiag_pdb_board_i2c_scan_test  DUT 
   [Teardown]  exit_unidiag_interface  DUT

Meta_Minerva_DIAG_TC_049_BMC_Board_OS_Access_Test
   [Documentation]  This is for BMC Board OS Access test .
   [Tags]  Meta_Minerva_DIAG_TC_049_BMC_Board_OS_Access_Test  minerva  test49  
   Step  1  check_unidiag_system_versions  DUT  
   Step  2  check_unidiag_bmc_board_os_access_test  DUT 
   Step  3  exit_unidiag_interface  DUT
   Step  4  switchToBmcThenToComeAgain  DUT

Meta_Minerva_DIAG_TC_050_BMC_Board_I2C_Devices_Scan_Test
   [Documentation]  This is for BMC Board I2Cscan test .
   [Tags]  Meta_Minerva_DIAG_TC_050_BMC_Board_I2C_Devices_Scan_Test  minerva  test50  
   Step  1  check_unidiag_system_versions  DUT  
   Step  2  check_unidiag_bmc_board_i2c_scan_test  DUT 
   [Teardown]  exit_unidiag_interface  DUT

Meta_Minerva_DIAG_TC_051_BMC_Board_SPI_Devices_Scan_Test
   [Documentation]  This is for BMC Board SPI scan test .
   [Tags]  Meta_Minerva_DIAG_TC_051_BMC_Board_SPI_Devices_Scan_Test  minerva  test51  
   Step  1  check_unidiag_system_versions  DUT 
   Step  2  check_unidiag_bmc_board_spi_scan_test  DUT 
   [Teardown]  exit_unidiag_interface  DUT

Meta_Minerva_DIAG_TC_052_BMC_Board_TPM_Test
   [Documentation]  This is for BMC Board TPM test .
   [Tags]  Meta_Minerva_DIAG_TC_052_BMC_Board_TPM_Test  minerva  test52  
   Step  1  check_unidiag_system_versions  DUT  
   Step  2  check_unidiag_bmc_board_tpm_vendor_test  DUT 
   [Teardown]  exit_unidiag_interface  DUT

Meta_Minerva_DIAG_TC_053_BMC_Board_CPU_Test
   [Documentation]  This is for BMC Board CPU test .
   [Tags]  Meta_Minerva_DIAG_TC_053_BMC_Board_CPU_Test  minerva  test53  
   Step  1  check_unidiag_system_versions  DUT  
   Step  2  check_unidiag_bmc_board_cpu_test  DUT 
   [Teardown]  exit_unidiag_interface  DUT

Meta_Minerva_DIAG_TC_054_BMC_Board_Memory_Test
   [Documentation]  This is for BMC Board Memory test .
   [Tags]  Meta_Minerva_DIAG_TC_054_BMC_Board_Memory_Test  minerva  test54  
   Step  1  check_unidiag_system_versions  DUT  
   Step  2  check_unidiag_bmc_board_memory_test  DUT 
   [Teardown]  exit_unidiag_interface  DUT

Meta_Minerva_DIAG_TC_055_BMC_Board_USB_Network_Test
   [Documentation]  This is for BMC Board USB Network test .
   [Tags]  Meta_Minerva_DIAG_TC_055_BMC_Board_USB_Network_Test  minerva  test55  
   Step  1  check_unidiag_system_versions  DUT  
   Step  2  check_unidiag_bmc_board_usb_network_test  DUT 
   [Teardown]  exit_unidiag_interface  DUT

Meta_Minerva_DIAG_TC_056_BMC_Board_bmc_version_Test
   [Documentation]  This is for BMC Board BMC Version test.
   [Tags]  Meta_Minerva_DIAG_TC_056_BMC_Board_bmc_version_Test  minerva  test56  
   Step  1  check_unidiag_system_versions  DUT  
   Step  2  check_unidiag_bmc_board_bmc_version_test  DUT 
   [Teardown]  exit_unidiag_interface  DUT

Meta_Minerva_DIAG_TC_057_Come_Board_i2c_device_scan_Test
   [Documentation]  This is for COMe Board I2Cscan test .
   [Tags]  Meta_Minerva_DIAG_TC_057_Come_Board_i2c_device_scan_Test  minerva  test57  
   Step  1  check_unidiag_system_versions  DUT  
   Step  2  check_unidiag_come_board_i2c_device_scan_test  DUT 
   [Teardown]  exit_unidiag_interface  DUT

Meta_Minerva_DIAG_TC_058_Come_Board_Bios_version_and_vendor_Test
   [Documentation]  This is for COMe Board Bios version and vendor test .
   [Tags]  Meta_Minerva_DIAG_TC_058_Come_Board_Bios_version_and_vendor_Test  minerva  test58  
   Step  1  check_unidiag_system_versions  DUT  
   Step  2  check_unidiag_come_board_bios_version_and_vendor_test  DUT 
   [Teardown]  exit_unidiag_interface  DUT

Meta_Minerva_DIAG_TC_059_Come_Board_CPU_info_and_status_Test
   [Documentation]  This is for COMe Board cpu info and status test .
   [Tags]  Meta_Minerva_DIAG_TC_059_Come_Board_CPU_info_and_status_Test  minerva  test59  
   Step  1  check_unidiag_system_versions  DUT  
   Step  2  check_unidiag_come_board_cpu_info_and_status_test  DUT 
   [Teardown]  exit_unidiag_interface  DUT

Meta_Minerva_DIAG_TC_062_Come_Board_TPM_vendor_Test
   [Documentation]  This is for COMe Board tpm vendor test .
   [Tags]  Meta_Minerva_DIAG_TC_062_Come_Board_TPM_vendor_Test  minerva  test62  
   Step  1  check_unidiag_system_versions  DUT  
   Step  2  check_unidiag_come_board_tpm_vendor_test  DUT 
   [Teardown]  exit_unidiag_interface  DUT

Meta_Minerva_DIAG_TC_063_Come_Board_Management_Ethernet_Port Connection_Test
   [Documentation]  This is for COMe Board tpm vendor test .
   [Tags]  Meta_Minerva_DIAG_TC_063_Come_Board_Management_Ethernet_Port  minerva  test63  
   Step  1  check_unidiag_system_versions  DUT  
   Step  2  check_unidiag_come_board_management_ethernet_test  DUT 
   [Teardown]  exit_unidiag_interface  DUT

Meta_Minerva_DIAG_TC_064_Come_Board_USB_Internal_Network_Test
   [Documentation]  This is for COMe Board tpm vendor test .
   [Tags]  Meta_Minerva_DIAG_TC_064_Come_Board_USB_Internal_Network_Test  minerva  test64  
   Step  1  check_unidiag_system_versions  DUT  
   Step  2  check_unidiag_come_board_usb_internal_network_test  DUT 
   [Teardown]  exit_unidiag_interface  DUT

Meta_Minerva_DIAG_TC_066_Come_Board_RTC_Test
   [Documentation]  This is for COMe Board RTC test .
   [Tags]  Meta_Minerva_DIAG_TC_066_Come_Board_RTC_Test  minerva  test66  
   Step  1  check_unidiag_system_versions  DUT  
   Step  2  check_unidiag_come_board_rtc_test  DUT 
   [Teardown]  exit_unidiag_interface  DUT

Meta_Minerva_DIAG_TC_067_BCB_I2C_SCAN_Via_COMe_Test
   [Documentation]  This is for BCB I2C Scan via COMe test .
   [Tags]  Meta_Minerva_DIAG_TC_067_BCB_I2C_SCAN_Via_COMe_Test  minerva  test67  
   Step  1  check_unidiag_system_versions  DUT  
   Step  2  check_unidiag_bcb_i2c_scan_via_come_test  DUT 
   [Teardown]  exit_unidiag_interface  DUT

Meta_Minerva_DIAG_TC_068_BCB_I2C_SCAN_Via_BMC_Test
   [Documentation]  This is for BCB I2C Scan via bmc test  .
   [Tags]  Meta_Minerva_DIAG_TC_068_BCB_I2C_SCAN_Via_BMC_Test  minerva  test68  
   Step  1  check_unidiag_system_versions  DUT 
   Step  2  check_unidiag_bcb_i2c_scan_via_bmc_test  DUT 
   [Teardown]  exit_unidiag_interface  DUT

Meta_Minerva_DIAG_TC_069_BCB_Interface_Network_Blade_Slot_ID_Check
   [Documentation]  This is for interface network blade slot id check.
   [Tags]  Meta_Minerva_DIAG_TC_069_BCB_Interface_Network_Blade_Slot_ID_Check  minerva  test69  
   Step  1  check_unidiag_system_versions  DUT  
   Step  2  check_unidiag_bcb_interface_network_blade_slot_id_check_test  DUT 
   [Teardown]  exit_unidiag_interface  DUT

Meta_Minerva_DIAG_TC_070_CMM_Present_Signal_Check
   [Documentation]  This is for bcb cmm present signal check .
   [Tags]  Meta_Minerva_DIAG_TC_070_CMM_Present_Signal_Check  minerva  test70  
   Step  1  check_unidiag_system_versions  DUT  
   Step  2  check_unidiag_bcb_cmm_present_signal_test  DUT 
   [Teardown]  exit_unidiag_interface  DUT

Meta_Minerva_DIAG_TC_071_Network_Blade_Power_Enable_Signal_Check
   [Documentation]  This is for Network Blade Power Enable Signal Check .
   [Tags]  Meta_Minerva_DIAG_TC_071_Network_Blade_Power_Enable_Signal_Check  minerva  test71  
   Step  1  check_unidiag_system_versions  DUT 
   Step  2  check_unidiag_bcb_network_blade_power_enable_signal_test  DUT 
   [Teardown]  exit_unidiag_interface  DUT

Meta_Minerva_DIAG_TC_072_UPGRADE_Bios_from_COMe
   [Documentation]   This tests upgrades smb cpld
   [Tags]  Meta_Minerva_DIAG_TC_072_UPGRADE_Bios_from_COMe  minerva  test72  
   Step  1  Prepare_images  DUT  ${BIOS_workspace}  BIOS
   Step  2  copy_to_device_firmware  DUT  BIOS  ${minerva_bios_new_image}
   Step  3  rename_file  DUT  ${minerva_bios_new_image}  ${minerva_bios_via_come_upgrade_format}
   Step  4  check_firmware_flash_upgrade  DUT  ${minerva_bios_via_come_name}  ${minerva_bios_via_come_option}  ${minerva_bios_via_come_pattern}  ${bios_update_timeout}
   Step  5  check power cycle bmc  DUT
   Step  6  check_upgraded_component_version  DUT  BIOS  ${minerva_bios_new_version}
   [Teardown]  cleanup_device_after_update  DUT

Meta_Minerva_DIAG_TC_075_UPGRADE_IOB_FPGA_from_COMe
   [Documentation]   This tests upgrades smb cpld
   [Tags]  Meta_Minerva_DIAG_TC_075_UPGRADE_IOB_FPGA_from_COMe  minerva  test75  
   Step  1  Prepare_images  DUT  ${FPGA_workspace}  FPGA
   Step  2  copy_to_device_firmware  DUT  FPGA  ${minerva_iob_fpga_new_image}
   Step  3  rename_file  DUT  ${minerva_iob_fpga_new_image}  ${minerva_iob_fpga_upgrade_format}
   Step  4  check_firmware_flash_upgrade  DUT  ${minerva_iob_fpga_name}  ${minerva_iob_fpga_option}  ${minerva_iob_fpga_pattern}
   Step  5  check power cycle bmc  DUT
   Step  6  check_upgraded_component_version  DUT  IOB FPGA  ${minerva_iob_fpga_new_version}
   [Teardown]  cleanup_device_after_update  DUT

Meta_Minerva_DIAG_TC_077_Upgrade_Th5_Switch_ASIC_Flash
   [Documentation]   This tests upgrades th5 blade
   [Tags]  Meta_Minerva_DIAG_TC_077_Upgrade_Th5_Switch_ASIC_Flash  test77  
   Step  1  check minerva file present  DIAG  ${th5_image}  
   Step  2  check sdk path
   Step  3  check th5 version
   Step  4  upgrade_th5_and_switch_asic  DUT  ${minerva_th5_switch_asic_pattern}
   Step  5  check power cycle bmc  DUT
   Step  6  check sdk path
   Step  7  check th5 version
   [Teardown]  cleanup_device_after_update  DUT

Meta_Minerva_DIAG_TC_078_UPGRADE_DOM_FPGA
   [Documentation]   This tests upgrades smb cpld
   [Tags]  Meta_Minerva_DIAG_TC_075_UPGRADE_IOB_FPGA_from_COMe  minerva  test78  
   Step  1  Prepare_images  DUT  ${FPGA_workspace}  FPGA
   Step  2  copy_to_device_firmware  DUT  FPGA  ${minerva_dom_fpga_new_image}
   Step  3  rename_file  DUT  ${minerva_dom_fpga_new_image}  ${minerva_dom_fpga_upgrade_format}
   Step  4  check_firmware_flash_upgrade  DUT  ${minerva_dom_fpga_name}  ${minerva_dom_fpga_option}  ${minerva_dom_fpga_pattern}
   Step  5  check power cycle bmc  DUT
   Step  6  check_upgraded_component_version  DUT  DOM FPGA  ${minerva_dom_fpga_new_version}
   [Teardown]  cleanup_device_after_update  DUT

Meta_Minerva_DIAG_TC_079_UPGRADE_SMB_CPLD1_FLASH
   [Documentation]   This tests upgrades smb cpld
   [Tags]  Meta_Minerva_DIAG_TC_079_UPGRADE_SMB_CPLD1_FLASH  minerva  test79  
   Step  1  Prepare_images  DUT  ${CPLD_workspace}  CPLD
   Step  2  copy_to_device_firmware  DUT  CPLD  ${minerva_smb1_cpld_new_image}
   Step  3  rename_file  DUT  ${minerva_smb1_cpld_new_image}  ${minerva_smb_cpld1_upgrade_format}
   Step  4  check_firmware_flash_upgrade  DUT  ${minerva_smb_cpld1_name}  ${minerva_smb_cpld1_option}  ${minerva_smb_cpld1_pattern}
   Step  5  check power cycle bmc  DUT
   Step  6  check_upgraded_component_version  DUT  SMB CPLD 1  ${minerva_smb1_cpld_new_version}
   [Teardown]  cleanup_device_after_update  DUT

Meta_Minerva_DIAG_TC_080_UPGRADE_SMB_CPLD2_FLASH
   [Documentation]   This tests upgrades smb2 cpld
   [Tags]  Meta_Minerva_DIAG_TC_078_UPGRADE_SMB_CPLD2_FLASH  minerva  test80  
   Step  1  Prepare_images  DUT  ${CPLD_workspace}  CPLD
   Step  2  copy_to_device_firmware  DUT  CPLD  ${minerva_smb2_cpld_new_image}
   Step  3  rename_file  DUT  ${minerva_smb2_cpld_new_image}  ${minerva_smb_cpld2_upgrade_format}
   Step  4  check_firmware_flash_upgrade  DUT  ${minerva_smb_cpld2_name}  ${minerva_smb_cpld2_option}  ${minerva_smb_cpld2_pattern}
   Step  5  check power cycle bmc  DUT
   Step  6  check_upgraded_component_version  DUT  SMB CPLD 2  ${minerva_smb2_cpld_new_version}
   [Teardown]  cleanup_device_after_update  DUT

Meta_Minerva_DIAG_TC_081_UPGRADE_Power_CPLD_FLASH
   [Documentation]   This tests upgrades smb cpld
   [Tags]  Meta_Minerva_DIAG_TC_081_UPGRADE_Power_CPLD_FLASH  minerva  test81  
   Step  1  Prepare_images  DUT  ${CPLD_workspace}  CPLD
   Step  2  copy_to_device_firmware  DUT  CPLD  ${minerva_pwr_cpld_new_image}
   Step  3  rename_file  DUT  ${minerva_pwr_cpld_new_image}  ${minerva_power_cpld_upgrade_format}
   Step  4  check_firmware_flash_upgrade  DUT  ${minerva_power_cpld_name}  ${minerva_power_cpld_option}  ${minerva_power_cpld_pattern}
   Step  5  check power cycle bmc  DUT
   Step  6  check_upgraded_component_version  DUT  PWR CPLD  ${minerva_pwr_cpld_new_version}
   [Teardown]  cleanup_device_after_update  DUT

Meta_Minerva_DIAG_TC_082_UPGRADE_I210_Flash
   [Documentation]   This tests upgrades smb cpld
   [Tags]  Meta_Minerva_DIAG_TC_082_UPGRADE_I210_Flash  minerva  test82  
   Step  1  Prepare_images  DUT  ${I210_workspace}  I210
   Step  2  copy_to_device_firmware  DUT  I210  ${minerva_i210_new_image}
   Step  3  rename_i210_flash_file  DUT  ${minerva_i210_new_image}  ${minerva_i210_flash_upgrade_format}
   Step  4  check_firmware_flash_upgrade  DUT  ${minerva_i210_flash_name}  ${minerva_i210_flash_option}  ${minerva_i210_flash_upgrade_pattern}
   Step  5  check power cycle bmc  DUT
   Step  6  check_upgraded_component_version  DUT  I210  ${minerva_i210_new_version}
   [Teardown]  cleanup_device_after_update  DUT

Meta_Minerva_DIAG_TC_083_UPGRADE_I210_Mac_Address_Flash
   [Documentation]   This tests upgrades smb cpld
   [Tags]  Meta_Minerva_DIAG_TC_083_UPGRADE_I210_Mac_Address_Flash  minerva  test83  
   Step  1  update_i210_mac_address_firmware  DUT  
   [Teardown]  cleanup_device_after_update  DUT

Meta_Minerva_DIAG_TC_088_System_EEPROM_Show_Board_FRU
   [Documentation]  This is for System EEPROM Show Board FRU .
   [Tags]  Meta_Minerva_DIAG_TC_088_Ststem_EEPROM_Show_Board_FRU  minerva  test88  
   Step  1  check_unidiag_system_versions  DUT  
   Step  2  check_unidiag_system_eeprom_show_board_fru_test  DUT 
   [Teardown]  exit_unidiag_interface  DUT

Meta_Minerva_DIAG_TC_089_System_EEPROM_Show_SMB_FRU1
   [Documentation]  This is for System EEPROM Show SMB FRU1.
   [Tags]  Meta_Minerva_DIAG_TC_089_System_EEPROM_Show_SMB_FRU1  minerva  test89  
   Step  1  check_unidiag_system_versions  DUT  
   Step  2  check_unidiag_system_eeprom_show_smb_fru1_test  DUT 
   [Teardown]  exit_unidiag_interface  DUT

Meta_Minerva_DIAG_TC_090_System_EEPROM_Show_SMB_FRU2
   [Documentation]  This is for System EEPROM Show SMB FRU2.
   [Tags]  Meta_Minerva_DIAG_TC_090_System_EEPROM_Show_SMB_FRU2  minerva  test90  
   Step  1  check_unidiag_system_versions  DUT  
   Step  2  check_unidiag_system_eeprom_show_smb_fru2_test  DUT 
   [Teardown]  exit_unidiag_interface  DUT

Meta_Minerva_DIAG_TC_091_Sanity_Test
   [Documentation]  This is for sanity test .
   [Tags]  Meta_Minerva_DIAG_TC_091_Sanity_Test  minerva  test91  
   Step  1  check_unidiag_system_versions  DUT 
   Step  2  check_unidiag_sanity_test  DUT 
   [Teardown]  exit_unidiag_interface  DUT

Meta_Minerva_DIAG_TC_092_Snapshot_Test
   [Documentation]  This is for snapshot test .
   [Tags]  Meta_Minerva_DIAG_TC_092_Snapshot_Test  minerva  test92  
   Step  1  check_unidiag_system_versions  DUT 
   Step  2  check_unidiag_snapshot_test  DUT 
   [Teardown]  exit_unidiag_interface  DUT

Meta_Minerva_DIAG_TC_093_MFG_Test
   [Documentation]  This is for mfg test .
   [Tags]  Meta_Minerva_DIAG_TC_093_MFG_Test  minerva  test93  
   Step  1  check_unidiag_system_versions  DUT 
   Step  2  check_unidiag_mfg_test  DUT 
   [Teardown]  exit_unidiag_interface  DUT

Meta_Minerva_DIAG_TC_094_test_main_auto_Test
   [Documentation]  This is for test main auto test .
   [Tags]  Meta_Minerva_DIAG_TC_094_test_main_auto_Test  minerva  test94  
   Step  1  check_unidiag_system_versions  DUT 
   Step  2  check_unidiag_main_auto_test  DUT 
   [Teardown]  exit_unidiag_interface  DUT

Meta_Minerva_DIAG_TC_095_system_auto_Test
   [Documentation]  This is for system auto test .
   [Tags]  Meta_Minerva_DIAG_TC_095_system_auto_Test  minerva  test95  
   Step  1  check_unidiag_system_versions  DUT 
   Step  2  check_unidiag_system_auto_test  DUT 
   [Teardown]  exit_unidiag_interface  DUT

Meta_Minerva_DIAG_TC_096_system_mac_auto_Test
   [Documentation]  This is for system mac auto test .
   [Tags]  Meta_Minerva_DIAG_TC_096_system_mac_auto_Test  minerva  test96  
   Step  1  check_unidiag_system_versions  DUT 
   Step  2  check_unidiag_system_mac_auto_test  DUT 
   [Teardown]  exit_unidiag_interface  DUT

Meta_Minerva_DIAG_TC_097_FPGA_Auto_Test
   [Documentation]  This is for FPGA auto test.
   [Tags]  Meta_Minerva_DIAG_TC_097_FPGA_Auto_Test  minerva  test97  
   Step  1  check_unidiag_system_versions  DUT  
   Step  2  check_unidiag_fpga_auto_test  DUT 
   [Teardown]  exit_unidiag_interface  DUT

Meta_Minerva_DIAG_TC_098_IOB_FPGA_Auto_Test
   [Documentation]  This is for IOB FPGA auto test.
   [Tags]  Meta_Minerva_DIAG_TC_098_IOB_FPGA_Auto_Test  minerva  test98  
   Step  1  check_unidiag_system_versions  DUT  
   Step  2  check_unidiag_iob_fpga_auto_test  DUT 
   [Teardown]  exit_unidiag_interface  DUT

Meta_Minerva_DIAG_TC_099_DOM_FPGA_Auto_Test
   [Documentation]  This is for DOM FPGA auto test.
   [Tags]  Meta_Minerva_DIAG_TC_099_DOM_FPGA_Auto_Test  minerva  test99  
   Step  1  check_unidiag_system_versions  DUT  
   Step  2  check_unidiag_dom_fpga_auto_test  DUT 
   [Teardown]  exit_unidiag_interface  DUT

Meta_Minerva_DIAG_TC_100_CPLD_Auto_Test
   [Documentation]  This is for CPLD auto test.
   [Tags]  Meta_Minerva_DIAG_TC_100_CPLD_Auto_Test  minerva  test100  
   Step  1  check_unidiag_system_versions  DUT  
   Step  2  check_unidiag_cpld_auto_test  DUT 
   [Teardown]  exit_unidiag_interface  DUT

Meta_Minerva_DIAG_TC_101_SMB_CPLD1_Auto_Test
   [Documentation]  This is for SMB CPLD1 auto test.
   [Tags]  Meta_Minerva_DIAG_TC_101_SMB_CPLD1_Auto_Test  minerva  test101 
   Step  1  check_unidiag_system_versions  DUT  
   Step  2  check_unidiag_smb_cpld1_auto_test  DUT 
   [Teardown]  exit_unidiag_interface  DUT

Meta_Minerva_DIAG_TC_102_SMB_CPLD2_Auto_Test
   [Documentation]  This is for SMB CPLD2 auto test.
   [Tags]  Meta_Minerva_DIAG_TC_102_SMB_CPLD2_Auto_Test  minerva  test102  
   Step  1  check_unidiag_system_versions  DUT  
   Step  2  check_unidiag_smb_cpld2_auto_test  DUT 
   [Teardown]  exit_unidiag_interface  DUT

Meta_Minerva_DIAG_TC_103_Come_CPU_Stress_Test
   [Documentation]  This is for COMe CPU stress test .
   [Tags]  Meta_Minerva_DIAG_TC_103_Come_CPU_Stress_Test  minerva  test103  
   Step  1  check_unidiag_system_versions  DUT  
   Step  2  check_come_cpu_stress_test  DUT 
   [Teardown]  exit_unidiag_interface  DUT

Meta_Minerva_DIAG_TC_104_MEM_Stress_Test
   [Documentation]  This is for memory stress test .
   [Tags]  Meta_Minerva_DIAG_TC_104_MEM_Stress_Test  minerva  test104  
   Step  1  check_unidiag_system_versions  DUT  
   Step  2  check_mem_stress_test  DUT 
   [Teardown]  exit_unidiag_interface  DUT

Meta_Minerva_DIAG_TC_107_I2C_Scan_Stress_Test
   [Documentation]  This is for memory stress test .
   [Tags]  Meta_Minerva_DIAG_TC_107_I2C_Scan_Stress_Test  minerva  test107  
   Step  1  check_unidiag_system_versions  DUT  
   Step  2  minerva_stress_test  DUT  ${minerva_i2c_scan_option}  ${minerva_i2c_scan_name}
   [Teardown]  exit_unidiag_interface  DUT

Meta_Minerva_DIAG_TC_108_OSFP_Stress_Test
   [Documentation]  This is for memory stress test .
   [Tags]  Meta_Minerva_DIAG_TC_108_OSFP_Stress_Test  minerva  test108  
   Step  1  check_unidiag_system_versions  DUT  
   Step  2  minerva_stress_test  DUT  ${minerva_i2c_osfp_option}  ${minerva_i2c_osfp_name}
   [Teardown]  exit_unidiag_interface  DUT

Meta_Minerva_DIAG_TC_109_SPI_Access_Stress_Test
   [Documentation]  This is for memory stress test .
   [Tags]  Meta_Minerva_DIAG_TC_109_SPI_Access_Stress_Test  minerva  test109  
   Step  1  check_unidiag_system_versions  DUT  
   Step  2  minerva_stress_test  DUT  ${minerva_spi_scan_option}  ${minerva_spi_scan_name}
   [Teardown]  exit_unidiag_interface  DUT

Meta_Minerva_DIAG_TC_110_PCIe_Scan_Stress_Test
   [Documentation]  This is for memory stress test .
   [Tags]  Meta_Minerva_DIAG_TC_110_PCIe_Scan_Stress_Test  minerva  test110  
   Step  1  check_unidiag_system_versions  DUT  
   Step  2  minerva_stress_test  DUT  ${minerva_pcie_scan_option}  ${minerva_pcie_scan_name}
   [Teardown]  exit_unidiag_interface  DUT


*** Keywords ***

Diag Connect Device
    WPL Set Library Order
    WPL Diag Device Connect
    WPL Init Test Library

Diag Disconnect Device
    WPL Diag Device Disconnect

Set Testcase Timeout
    [Arguments]    ${TIMEOUT}
    [Timeout]      ${TIMEOUT} seconds
    Log Debug      *** Set Testcase Timeout: ${TIMEOUT} Seconds ***
    sleep          1s

Print Loop Info
    [Arguments]    ${CUR_INDEX}
    Log Info  *******************************************
    Log Info  *** Test Loop \#: ${CUR_INDEX} / ${LoopCnt} ***
    Log Info  *******************************************

                                                                                             
