
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


MiniPack3_DIAG_TC_000_Diag_Script_install_reinstall_Test
   [Documentation]  This is to install/reinstall diag .
   [Tags]  MiniPack3_DIAG_TC_000_Diag_Script_install_reinstall_Test  minipack3  test0 
   Step  1  unidiag_version_check  DUT  ${minipack3_unidiag_new_version}
   Step  2  install_reinstall_test  DUT
   Step  3  unidiag_version_check  DUT  ${minipack3_unidiag_new_version}
   Step  4  check_unidiag_system_version_from_submenu  DUT
   Step  5  exit_unidiag_interface  DUT
   [Teardown]  Run Keyword If Test Failed  exit_unidiag_interface  DUT

Minipack3_DIAG_TC_001_Diag_Script_Interactive_UI_Check
   [Documentation]  Check diag interactive UI interface submenus
   [Tags]  Minipack3_DIAG_TC_001_Diag_Script_Interactive_UI_Check  minipack3  test1  diag
   Step  1  check_unidiag_system_versions  DUT
   Step  2  check_diag_script_ui_submenu  DUT
   [Teardown]  exit_unidiag_interface  DUT 

MiniPack3_DIAG_TC_003_System_I2c_Scan_Test
   [Documentation]  This is to I2c scan for system.
   [Tags]  MiniPack3_DIAG_TC_003_System_I2c_Scan_Test  minipack3  test3  diag
   Step  1  check_unidiag_system_versions  DUT
   Step  2  check_system_i2c_scan   DUT
   [Teardown]  exit_unidiag_interface  DUT

MiniPack3_DIAG_TC_004_System_SPI_Scan_Test
   [Documentation]  This is to SPI scan for system.
   [Tags]  MiniPack3_DIAG_TC_004_System_SPI_Scan_Test  minipack3  test4  diag
   Step  1  check_unidiag_system_versions  DUT
   Step  2  check_system_spi_scan   DUT
   [Teardown]  exit_unidiag_interface  DUT

MiniPack3_DIAG_TC_005_PCIE_Scan_Test
   [Documentation]  This is to PCIE scan for system.
   [Tags]  MiniPack3_DIAG_TC_005_PCIE_Scan_Test  minipack3  test5  diag
   Step  1  check_unidiag_system_versions  DUT
   Step  2  check_system_pcie_scan   DUT
   [Teardown]  exit_unidiag_interface  DUT

MiniPack3_DIAG_TC_015_System_USB_Network_Test
   [Documentation]  This is to USB Network test for system.
   [Tags]  MiniPack3_DIAG_TC_015_System_USB_Network_Test  minipack3  test15  diag
   Step  1  check_unidiag_system_versions  DUT
   Step  2  check_system_usb_network_test  DUT
   [Teardown]  exit_unidiag_interface  DUT
   
MiniPack3_DIAG_TC_018_System_OOB_Test
   [Documentation]  This is to OOB test for system.
   [Tags]  MiniPack3_DIAG_TC_018_System_OOB_Test  minipack3  test18  diag
   Step  1  check_unidiag_system_versions  DUT
   Step  2  check_system_oob_test  DUT
   [Teardown]  exit_unidiag_interface  DUT

MiniPack3_DIAG_TC_21_OSFP_I2C_Scan_Test
   [Documentation]  This is to OSFP port disable test .
   [Tags]  MiniPack3_DIAG_TC_21_OSFP_I2C_Scan_Test  minipack3  test21  diag
   Step  1  check_unidiag_system_versions  DUT
   Step  2  get_into_osfp_submenu  DUT
   Step  3  check_osfp_port_enable  DUT
   Step  4  check_osfp_i2c_scan  DUT
   Step  5  check_osfp_port_disable  DUT
   [Teardown]  exit_unidiag_interface  DUT

MiniPack3_DIAG_TC_076_Upgrade_Th5_Switch_Flash
   [Documentation]   This tests upgrades th5 blade
   [Tags]  MiniPack3_DIAG_TC_076_Upgrade_Th5_Switch_Flash  test76 
   Step  1  check file present  DIAG  ${th5_image}  
   Step  2  check sdk path
   Step  3  check th5 version  
   Step  4  check_firmware_flash_upgrade  DUT  ${th5_name}  ${th5_option}  ${minipack_th5_update_pattern}
   Step  5  check power cycle bmc  DUT
   Step  6  check sdk path
   Step  7  check th5 version

MINIPACK3_DIAG_TC_077_UPGRADE_SMB_CPLD_FLASH
   [Documentation]   This tests upgrades smb cpld
   [Tags]  MINIPACK3_DIAG_TC_077_UPGRADE_SMB_CPLD_FLASH  minipack3  test77  
   Step  1  copy_file_to_firmware  DUT  DIAG  ${smb_image} 
   Step  2  check_firmware_flash_upgrade  DUT  ${smb_cpld_name}  ${smb_cpld_option}  ${minipack_smb_cpld_update_pattern}
   Step  3  check power cycle bmc  DUT
   Step  4  exit_unidiag_interface  DUT
   Step  5  check_unidiag_system_versions  DUT
   [Teardown]  exit_unidiag_interface  DUT

MINIPACK3_DIAG_TC_078_UPGRADE_MCB_CPLD_FLASH
   [Documentation]   This tests upgrades mcb cpld
   [Tags]  MINIPACK3_DIAG_TC_078_UPGRADE_MCB_CPLD_FLASH  minipack3  test78
   Step  1  copy_file_to_firmware  DUT  DIAG  ${mcb_image} 
   Step  2  check_firmware_flash_upgrade  DUT  ${mcb_cpld_name}  ${mcb_cpld_option}  ${minipack_mcb_cpld_update_pattern}
   Step  3  check power cycle bmc  DUT
   Step  4  exit_unidiag_interface  DUT
   Step  5  check_unidiag_system_versions  DUT
   [Teardown]  exit_unidiag_interface  DUT

MINIPACK3_DIAG_TC_079_UPGRADE_SCM_CPLD_FLASH
   [Documentation]   This tests upgrades scm cpld
   [Tags]  MINIPACK3_DIAG_TC_079_UPGRADE_SCM_CPLD_FLASH  minipack3  test79
   Step  1  copy_file_to_firmware  DUT  DIAG  ${scm_image}  
   Step  2  check_firmware_flash_upgrade  DUT  ${scm_cpld_name}  ${scm_cpld_option}  ${minipack_scm_cpld_update_pattern}
   Step  3  check power cycle bmc  DUT
   Step  4  exit_unidiag_interface  DUT
   Step  5  check_unidiag_system_versions  DUT
   [Teardown]  exit_unidiag_interface  DUT

MiniPack3_DIAG_TC_081_upgrade_dom_flash
   [Documentation]  This is to upgrade dom flash .
   [Tags]  MiniPack3_DIAG_TC_081_upgrade_dom_flash  minipack3  test81
   Step  1  copy_file_to_firmware  DUT  DIAG  ${dom_image} 
   Step  2  upgrade_dom_flash  DUT
   Step  3  exit_unidiag_interface  DUT
   Step  4  check_unidiag_system_versions  DUT
   Step  5  check_unidiag_powercycle  DUT
   Step  6  check_unidiag_system_versions  DUT
   Step  7  verify_fpga_unidiag_version  DUT  ${dom_fpga_unidiag_option}
   [Teardown]  exit_unidiag_interface  DUT

MiniPack3_DIAG_TC_082_upgrade_iob_fpga_flash_Test
   [Documentation]  This is to upgrade iob fpga flash .
   [Tags]  MiniPack3_DIAG_TC_082_upgrade_iob_fpga_flash_Test  minipack3  test82 
   Step  1  copy_file_to_firmware  DUT  DIAG  ${iob_image}
   Step  2  upgrade_iob_fpga_flash  DUT
   Step  3  exit_unidiag_interface  DUT
   Step  4  check_unidiag_system_versions  DUT
   Step  5  check_unidiag_powercycle  DUT
   Step  6  check_unidiag_system_versions  DUT
   Step  7  verify_fpga_unidiag_version  DUT  ${iob_fpga_unidiag_option}
   [Teardown]  exit_unidiag_interface  DUT  

MiniPack3_DIAG_TC_101_OSFP_Port_Enable_Test
   [Documentation]  This is to OSFP port enable test .
   [Tags]  MiniPack3_DIAG_TC_101_OSFP_Port_Enable_Test  minipack3  test101  diag
   Step  1  check_unidiag_system_versions  DUT
   Step  2  get_into_osfp_submenu  DUT
   Step  3  check_osfp_port_enable  DUT
   [Teardown]  exit_unidiag_interface  DUT

MiniPack3_DIAG_TC_102_OSFP_Port_Disable_Test
   [Documentation]  This is to OSFP port disable test .
   [Tags]  MiniPack3_DIAG_TC_102_OSFP_Port_Disable_Test  minipack3  test102  diag
   Step  1  check_unidiag_system_versions  DUT
   Step  2  get_into_osfp_submenu  DUT
   Step  3  check_osfp_port_disable  DUT
   [Teardown]  exit_unidiag_interface  DUT

MiniPack3_DIAG_TC_103_OSFP_PORTS_Present_Test
   [Documentation]  This is to OSFP ports present .
   [Tags]  MiniPack3_DIAG_TC_103_OSFP_PORTS_Present_Test  minipack3  test103  diag
   Step  1  check_unidiag_system_versions  DUT
   Step  2  get_into_osfp_submenu  DUT
   Step  3  check_osfp_port_present  DUT
   [Teardown]  exit_unidiag_interface  DUT

MiniPack3_DIAG_TC_104_OSFP_PORTS_Reset_check
   [Documentation]  This is to OSFP ports reset  .
   [Tags]  MiniPack3_DIAG_TC_104_OSFP_PORTS_Reset_check  minipack3  test104  diag
   Step  1  check_unidiag_system_versions  DUT
   Step  2  get_into_osfp_submenu  DUT
   Step  3  check_osfp_port_reset  DUT
   [Teardown]  exit_unidiag_interface  DUT

MiniPack3_DIAG_TC_105_OSFP_PORTS_LPMODE_check
   [Documentation]  This is to OSFP ports lpmode check .
   [Tags]  MiniPack3_DIAG_TC_105_OSFP_PORTS_LPMODE_check  minipack3  test105  diag
   Step  1  check_unidiag_system_versions  DUT
   Step  2  get_into_osfp_submenu  DUT
   Step  3  check_osfp_port_lpmode_test  DUT
   Step  4  check_osfp_port_lpmode_check  DUT  lpmode=${true}
   Step  5  check_osfp_port_hpmode_test  DUT
   Step  6  check_osfp_port_lpmode_check  DUT  
   [Teardown]  exit_unidiag_interface  DUT

MiniPack3_DIAG_TC_109_OSFP_PORTS_LPMODE_Test
   [Documentation]  This is to OSFP ports lpmode test .
   [Tags]  MiniPack3_DIAG_TC_109_OSFP_PORTS_LPMODE_Test  minipack3  test109  diag
   Step  1  check_unidiag_system_versions  DUT
   Step  2  get_into_osfp_submenu  DUT
   Step  3  check_osfp_port_lpmode_test  DUT
   [Teardown]  exit_unidiag_interface  DUT

MiniPack3_DIAG_TC_110_OSFP_PORTS_HPMODE_Test
   [Documentation]  This is to OSFP ports HPMODE .
   [Tags]  MiniPack3_DIAG_TC_110_OSFP_PORTS_HPMODE_Test  minipack3  test110  diag
   Step  1  check_unidiag_system_versions  DUT
   Step  2  get_into_osfp_submenu  DUT
   Step  3  check_osfp_port_hpmode_test  DUT
   [Teardown]  exit_unidiag_interface  DUT

MINIPACK3_DIAG_TC_111_Power_Cycle_Test
   [Documentation]   This test tests powercycler
   [Tags]  MINIPACK3_DIAG_TC_111_Power_Cycle_Test  minipack3  test111  diag
   Step  1  check_unidiag_system_versions  DUT
   Step  2  check unidiag powercycle  DUT

MiniPack3_DIAG_TC_120_upgrade_i210_flash
   [Documentation]  This is to upgrade i210 flash .
   [Tags]  MiniPack3_DIAG_TC_120_upgrade_i210_flash  minipack3  test120
   Step  1  check file present  DIAG  ${i210_image} 
   Step  2  upgrade_i210_flash  DUT
   Step  3  exit_unidiag_interface  DUT
   Step  4  check_unidiag_system_versions  DUT
   Step  5  check_unidiag_powercycle  DUT
   Step  6  check_unidiag_system_versions  DUT 
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

                                                                                             
