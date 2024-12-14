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
Documentation   Kapok common diagnostic suite
Resource        CommonKeywords.resource
Resource        KapokCommonKeywords.resource
Resource        KapokDiagKeywords.resource
Library         KapokDiagLib.py
Library         CommonLib.py
Library         ../KapokCommonLib.py


Suite Setup     DiagOS Connect Device
Suite Teardown  DiagOS Disconnect Device

*** Test Cases ***
DIAG_TC00_Diag_Initialize_And_Version_Check
    [Tags]  DIAG_TC00_Diag_Initialize_And_Version_Check  tianhe
	[Setup]  boot Into DiagOS Mode
    Step  1  get dhcp ip
    Step  2  update diagos and onie test
    Step  3  check version before the test
#Step  4  check driver version  ${drive_pattern_tianhe}

DIAG_10.1_POST_Test
    [Tags]  DIAG_10.1_POST_Test  tianhe
	[Setup]  boot Into DiagOS Mode
    Step  1  check Post Info  ${post_test_pattern_tianhe}


DIAG_10.2_Boot-up_Image_Updating_Only_for_NPI_stage
    [Tags]  DIAG_10.2_Boot-up_Image_Updating_Only_for_NPI_stage  tianhe
    [Setup]  boot into uboot
    Step  1  set static address
    Step  2  update boot image
#Step  3  power Cycle To onie rescue mode  # WORKAROUNDD, if no this step unit will hung
	Step  3  check uboot version in onie mode  ${get_versions_cmd}
    Step  4  power Cycle To DiagOS
    Step  5  get dhcp ip
	Step  6  tftp download image to unit  ${serverip}  ${ubootImgHostPath}  ${ubootImgFile}  ${ubootImgUnitPath}
    Step  7  flash uboot partition  ${flashTool}  ${ubootDevice}  ${ubootImgFile}  ${ubootImgUnitPath}
    Step  8  boot into uboot
    Step  9  reset Uboot Env
    Step  10  boot Into DiagOS Mode
    Step  11  verify boot image  ${get_versions_cmd}


#This case is temporarily not applicable to tianhe
#and the operation may cause other cases to fail.
#It should be fixed to the applicable tianhe and then executed
DIAG_10.3_CPLD_Image_Updating(Only for NPI stage)
    [Tags]  DIAG_10.3_CPLD_Image_Updating(Only for NPI stage)  tianhe
    [Setup]  boot Into DiagOS Mode
    Step  1  upgrade diag cpld  ${vmetool_path}  ${vmetool}
    Step  2  power cycle to DiagOS
    Step  3  check cpld version


DIAG_10.5_SYSCPLD_Backup_Image_Test
    [Tags]  DIAG_10.5_SYSCPLD_Backup_Image_Test  tianhe
    [Setup]  boot into DiagOS Mode
    Step  1  erase sys cpld image 
#Step  2  power cycle to DiagOS
    Step  3  check SYSCPLD version 
    Step  4  restore sys cpld image 
#Step  5  power cycle to DiagOS
    Step  6  verify cpld version


DIAG_10.6_Boot-Up_Test
    [Tags]  DIAG_10.6_Boot-Up_Test  tianhe
    [Setup]  boot into uboot
    Step  1  verify boot to each mode
    #Step  2  reset default boot to diag
    #Step  3  set default env


DIAG_10.7_Management_Port_MAC_Address_Modify
    [Tags]  DIAG_10.7_Management_Port_MAC_Address_Modify   tianhe
    [Timeout]  10 min
#[Setup]  boot Into Uboot
#Step  1  reset Uboot Env
    Step  1  boot Into DiagOS Mode
    ${mac} =  KapokDiagLib.get mac address
    Step  2  check Mac Address
    Step  3  modify Mac Address
    Step  4  boot Into Uboot   ## @WORKAROUND, Step 5, 6 to avoid this issue "ERROR: can't get kernel image"
    Step  5  reset Uboot Env
    Step  6  boot Into DiagOS Mode
    Step  7  check Mac Address
    [Teardown]  modify Mac Address  ${mac}


DIAG_10.8_TLV_EEPROM_Burning
    [Tags]  DIAG_10.8_TLV_EEPROM_Burning   tianhe
    [Timeout]  15 min
    [Setup]  boot Into DiagOS Mode
	Step  1  switch folder path  ${diag_tools_path}
    Step  2  disable or enable protection  ${disableEEValue}  ${COMeEEWP}  ${sysEEWP}
    Step  3  erase eeprom then read eeprom value  True  ${eepromTool}  ${eraseTlvCmd}  ${readTlvCmd}
    Step  4  disable or enable protection  ${enableEEValue}  ${COMeEEWP}  ${sysEEWP}
    Step  5  erase eeprom then read eeprom value  False  ${eepromTool}  ${eraseTlvCmd}  ${readTlvCmd}
    Step  6  write eeprom data  ${eepromTool}  ${writeTlvCmd}  ${storeFile}


DIAG_10.9_FRU_EEPROM_Burning
    [Tags]  DIAG_10.9_FRU_EEPROM_Burning   tianhe
    [Timeout]  15 min
    [Setup]  boot Into DiagOS Mode
    Step  1  disable or enable All Protect  ${enableEEValue}  ${fanDevice}
    Step  2  switch folder path  ${configPath}
    Step  3  write sample fan eeprom  ${fruFanEeprom}  ${fruDefEeprom}  ${fanSampleFile}  ${defSampleFile}
    Step  4  switch folder path  ${diag_tools_path}
    Step  5  write and read then store fan eeprom  ${enableEEValue}  ${eepromTool}  ${writeFanCmd}  ${readFanCmd}  ${fanFolder}  ${storeType1}
    Step  6  disable or enable All Protect  ${disableEEValue}  ${fanDevice}
    Step  7  write and read then store fan eeprom  ${disableEEValue}  ${eepromTool}  ${writeFanCmd}  ${readFanCmd}  ${defFolder}  ${storeType2}
    Step  8  compare eeprom data  ${storeType1}  ${storeType2}
    [Teardown]  delete log file  ${diag_tools_path}  ${storeType}


DIAG_10.10_FRU_EEPROM_ACCESS_TEST
    [Tags]  DIAG_10.10_FRU_EEPROM_ACCESS_TEST  tianhe
#Step  1  dump all FRU EEPROM content depents on tianhe model
    Step  1  fru Eeprom Access Test


DIAG_10.11_System_Information_Checking
    [Tags]  DIAG_10.11_System_Information_Checking   tianhe
    [Timeout]  10 min
    [Setup]  boot Into DiagOS Mode
    Step  1  check HW info
    Step  2  check SDK Version
    

DIAG_10.12_CPLD_ACCESS_TEST
    [Tags]  DIAG_10.12_CPLD_ACCESS_TEST  tianhe
    [Setup]  boot Into DiagOS Mode
    Step  1  verify CPLD access


DIAG_10.13_MAIN_BOARD_VERSION_CHECK
    [Tags]  DIAG_10.13_MAIN_BOARD_VERSION_CHECK  tianhe
    [Setup]  boot Into DiagOS Mode
    Step  1  check Main Board Version By CPLD


DIAG_10.14_TPM_Device_Access_Test
    [Documentation]  This test is to check vendor id, device id and the presence of TPM device
    [Tags]  DIAG_10.14_TPM_Device_Access_Test  tianhe
    [Timeout]  5 min 00 seconds
    [Setup]  boot Into DiagOS Mode
    Step  1  TPM Device Access Test
	Step  2  dump tpm test  ${tpm_output_path}  ${dump_tpm_tool}  ${tpm_pattern}


DIAG_10.15_CPU_DDR_Memory_Test
    [Tags]  DIAG_10.15_CPU_DDR_Memory_Test  tianhe
    [Setup]  boot Into DiagOS Mode
    Step  1  export env path  ${export_cmd_list}
    Step  2  verify diag tool test result  ${diag_tools_path}  ${mem_test_tool_name}  ${mem_test_option}  ${mem_test_passPattern}  timeout=${3000}
    Step  3  verify diag tool test result  ${diag_tools_path}  ${mem_test_tool_name}  ${cores_option1}  ${option_cores_pattern}  timeout=${3000}
    Step  4  verify diag tool test result  ${diag_tools_path}  ${mem_test_tool_name}  ${stress_option1}  ${option_stress_pattern}  timeout=${3000}
    Step  5  verify diag tool test result  ${diag_tools_path}  ${mem_test_tool_name}  ${stress_option2}  ${option_stress_pattern}  timeout=${3000}
    Step  6  verify diag tool test result  ${diag_tools_path}  ${mem_test_tool_name}  ${mem_test_option2}  ${mem_test_passPattern}  timeout=${3000}
    Step  7  verify diag tool test result  ${diag_tools_path}  ${mem_test_tool_name}  ${cores_option2}  ${option_cores_pattern}  timeout=${3000}
    Step  8  verify diag tool test result  ${diag_tools_path}  ${mem_test_tool_name}  ${stress_option3}  ${option_stress_pattern}  timeout=${3000}
    Step  9  verify diag tool test result  ${diag_tools_path}  ${mem_test_tool_name}  ${edac_option}  ${option_edac_pattern}  timeout=${3000}


DIAG_10.16_I2C_Bus_Scan_Test
    [Tags]  DIAG_10.16_I2C_Bus_Scan_Test  tianhe
    [Setup]  boot Into DiagOS Mode
    Step  1  export env path  ${export_cmd_list}
    Step  2  verify diag tool test result  ${diag_tools_path}  ${i2c_test_tool_name}  ${i2c_test_option}  ${i2c_test_pattern}


DIAG_10.17_PCIE_SCAN_TEST
    [Tags]  DIAG_10.17_PCIE_SCAN_TEST  tianhe
    Step  1  detect all PCIe devices


DIAG_10.18_Switch_Device_Access_Test
    [Tags]  DIAG_10.18_Switch_Device_Access_Test  tianhe
    Step  1  verify diag tool test result  ${diag_tools_path}  ${device_access_test_cmd}  ${device_access_test_option}  ${device_access_test_pattern}  True




DIAG_10.19_On-board_DC/DC_Controller_Access_Test
    [Tags]  DIAG_10.19_On-board_DC/DC_Controller_Access_Test  tianhe
    [Setup]  export env path  ${export_cmd_list}
    Step  1  verify diag tool test result  ${diag_tools_path}  ${dcdc_test_tool_name}  ${dcdc_access_option1}  ${passpattern_of_option1}
    Step  2  verify diag tool test result  ${diag_tools_path}  ${dcdc_test_tool_name}  ${dcdc_access_option2}  ${passpattern_of_option2}
    Step  3  verify diag tool test result  ${diag_tools_path}  ${dcdc_test_tool_name}  ${dcdc_access_option3}  ${passpattern_of_option3}


DIAG_10.20_Power_Monitor_Functional_Test
    [Tags]  DIAG_10.20_Power_Monitor_Functional_Test  tianhe
    [Setup]  export env path  ${export_cmd_list}
    Step  1  verify diag tool test result  ${diag_tools_path}  ${dcdc_test_tool_name}  ${dcdc_test_option5}  ${pattern_of_option4}
    Step  2  verify diag tool test result  ${diag_tools_path}  ${dcdc_test_tool_name}  --mode low --show  ${pattern_of_option4}
    Step  3  verify diag tool test result  ${diag_tools_path}  ${dcdc_test_tool_name}  --mode normal --show  ${pattern_of_option4}
    Step  4  verify diag tool test result  ${diag_tools_path}  ${dcdc_test_tool_name}  --mode high --show  ${pattern_of_option4}
    Step  5  verify diag tool test result  ${diag_tools_path}  ${dcdc_test_tool_name}  ${dcdc_test_option1}  ${pattern_of_option1}
    Step  6  verify diag tool test result  ${diag_ld_lib_path}  ${margin_cmd_list_low}  ${margin_option}  ${margin_pattern}
    Step  7  verify diag tool test result  ${diag_tools_path}  ${dcdc_test_tool_name}  --mode low --all  ${pattern_of_option1}
    Step  8  verify diag tool test result  ${diag_tools_path}  ${dcdc_test_tool_name}  --mode normal --all  ${pattern_of_option1}
    Step  9  verify diag tool test result  ${diag_ld_lib_path}  ${margin_cmd_list_high}  ${margin_option}  ${margin_pattern}
    Step  10  verify diag tool test result  ${diag_tools_path}  ${dcdc_test_tool_name}  --mode high --all  ${pattern_of_option1}


DIAG_10.21_ROV_Functional_Test
    [Documentation]  This test is to check the actual VDD core output against the target ROV
    [Tags]  DIAG_10.21_ROV_Functional_Test  tianhe
    [Timeout]  5 min 00 seconds
    [Setup]  boot Into DiagOS Mode
    Step  1  ROV Functional Test


DIAG_10.22_SATA_Device_Access_Test
    [Tags]  DIAG_10.22_SATA_Device_Access_Test  tianhe
    [Setup]  export env path  ${export_cmd_list}
    Step  1  disk l
    Step  2  verify diag tool test result  ${diag_tools_path}  ${sata_device_test_tool_name}  ${sata_device_test_option}  ${sata_device_test_pattern}
	Step  3  verify diag tool test result  ${diag_tools_path}  ${sata_device_test_tool_name}  ${sata_multi_test_option}  ${sata_multi_test_pattern}


DIAG_10.23_SSD_Device_Health_Status_Test
    [Tags]  DIAG_10.23_SSD_Device_Health_Status_Test  tianhe
    Step  1  verify diag tool test result  ${ssd_test_path}  ${ssd_test_tool_name}  ${ssd_test_option}  ${ssd_test_pattern}  $(is_ssd_cmd)
    Step  2  wait for execute  ${ssd_test_time_stamp}
    Step  3  verify diag tool test result  ${ssd_test_path}  ${ssd_test_tool_name}  ${ssd_status_check_option}  ${ssd_test_verify_pattern}  $(is_ssd_cmd)


#DIAG_TC22_SPI_to_I2C&I/O_Device(SC18IS600)_Access_Test
#    [Tags]  DIAG_TC22_SPI_to_I2C&I/O_Device(SC18IS600)_Access_Test  tianhe
#    [Setup]  export env path  ${export_cmd_list}
#    Step  1  verify i2cdetect with l  ${spi_i2c_test_cmd}  ${spi_i2c_test_option}
#    Step  2  verify diag tool test result  ${diag_tools_path}  ${spi_i2c_test_cmd}  ${spi_i2c_test_option1}  ${spi_i2c_test_pattern}  True


DIAG_10.24_System_Watchdog_Test
    [Tags]  DIAG_10.24_System_Watchdog_Test  tianhe
    Step  1  check cmd no output  ${system_watchdog_test_cmd}
    Step  2  verify system watchdog  ${system_watchdog_reset_cmd}


DIAG_10.25_System_Reboot_Test
    [Tags]  DIAG_10.25_System_Reboot_Test  tianhe
    Step  1  system reset to diag  ${cold_reboot_cmd}
    Step  2  system reset to diag  ${warm_reboot_cmd}
	Step  3  system reset to diag  ${hotswap_reboot_cmd}
    Step  4  system reset to diag  ${pwrcycle_reboot_cmd}


DIAG_10.26_COMECPLD SRAM Access Test
    [Tags]  DIAG_10.26_COMECPLD SRAM Access Test  tianhe
    [Setup]  boot Into DiagOS Mode
    Step  1  export env path  ${export_cmd_list}
    Step  2  fhv2 Fault Log Sram  ${COME_fault_log_cmd}  ${fault_log_pattern1}  ${fault_log_pattern2}


DIAG_10.27_SYSCPLD_SRAM_Access_Test
    [Tags]  DIAG_10.27_SYSCPLD_SRAM_Access_Test  tianhe
    [Setup]  boot Into DiagOS Mode
    Step  1  export env path  ${export_cmd_list}
    Step  2  fhv2 Fault Log Sram  ${fault_log_cmd}  ${fault_log_pattern1}  ${fault_log_pattern2}
	Step  3  fhv2 Console Log Sram  ${console_log_cmd1}  ${console_log_cmd2}  ${console_log_pattern1}  ${console_log_pattern2}


DIAG_10.28_CPU_Risercard_PRESENT_STATUS_TEST
    [Tags]  DIAG_10.28_CPU_Risercard_PRESENT_STATUS_TEST  tianhe
    Step  1  check CPU Riser Card


DIAG_10.29_PSU_TEST
    [Tags]  DIAG_10.29_PSU_TEST  tianhe
    Step  1  check all PSU status
    Step  2  show all PSU values
    Step  3  show PSU1 values
    #Step  4  show PSU2 values  #Testplan has no such step in the log


DIAG_10.30_TEMPERATURE_SENSOR_ACCESS_TEST
    [Tags]  DIAG_10.30_TEMPERATURE_SENSOR_ACCESS_TEST  tianhe
    Step  1  verify diag tool test result  ${diag_tools_path}  ${temp_test_tool_name}  ${temp_test_option1}  ${temp_test_pattern1}
    Step  2  verify diag tool test result  ${diag_tools_path}  ${temp_test_tool_name}  ${temp_test_option2}  ${temp_test_pattern2}
    Step  3  verify diag tool test result  ${diag_tools_path}  ${temp_test_tool_name}  ${temp_test_option3}  ${temp_test_pattern1}
    Step  4  verify diag tool test result  ${diag_tools_path}  ${temp_test_tool_name}  ${temp_test_option4}  ${temp_test_pattern1}
    Step  5  verify diag tool test result  ${diag_tools_path}  ${temp_test_tool_name}  ${temp_test_option5}  ${temp_test_fail_pattern}


DIAG_10.31_FAN_BOARD_CPLD_ACCESS_TEST
    [Tags]  DIAG_10.31_FAN_BOARD_CPLD_ACCESS_TEST  tianhe
	Step  1  verify FAN board CPLD access

DIAG_10.32_FAN_Present_Test
    [Tags]  DIAG_10.32_FAN_Present_Test  tianhe
    [Setup]  export env path  ${export_cmd_list}
    Step  1  verify diag tool test result  ${diag_tools_path}  ${fan_test_tool_name}  ${fan_test_option1}  ${fan_test_pattern}
    Step  2  verify diag tool test result  ${diag_tools_path}  ${fan_test_tool_name}  ${fan_test_option2}  ${fan_test_pattern}


DIAG_10.35_FAN_TRAY_SPEED_TEST
    [Tags]  DIAG_10.35_FAN_TRAY_SPEED_TEST  tianhe
    Step  1  show All Fan PWM RPM
    Step  2  show Fan PWM RPM  ${fan_pwm_rpm_show_patterns}
    Step  3  set All FAN PWM  pwm -D 255
    Step  4  verify diag tool test result  ${diag_tools_path}  ${fan_speed_tool_name}  ${fan_speed_option}  ${fan_speed_pattern1}
    Step  5  set all FAN PWM  pwm -D 229
    Step  6  verify diag tool test result  ${diag_tools_path}  ${fan_speed_tool_name}  ${fan_speed_option}  ${fan_speed_pattern2}
	Step  7  set all FAN PWM  pwm -D 204
	Step  8  verify diag tool test result  ${diag_tools_path}  ${fan_speed_tool_name}  ${fan_speed_option}  ${fan_speed_pattern3}
	Step  9  set all FAN PWM  pwm -D 178
	Step  10  verify diag tool test result  ${diag_tools_path}  ${fan_speed_tool_name}  ${fan_speed_option}  ${fan_speed_pattern4}
	Step  11  set all FAN PWM  pwm -D 140
	Step  12  verify diag tool test result  ${diag_tools_path}  ${fan_speed_tool_name}  ${fan_speed_option}  ${fan_speed_pattern5}


DIAG_10.36_FAN_CTRL_TEST
    [Tags]  DIAG_10.36_FAN_CTRL_TEST  tianhe
    Step  1  verify fan ctrl test  ${diag_tools_path}  ${fan_ctrl_tool}  ${fan_ctrl_option}  ${fan_ctrl_test_pattern}


DIAG_10.37_FAN_WDT_FUNCTION_TEST
    [Tags]  DIAG_10.37_FAN_WDT_FUNCTION_TEST  tianhe
    Step  1  set all FAN PWM  wd_en -D 0
    Step  2  set all FAN PWM  pwm -D 127
    Step  3  verify diag tool test result  ${diag_tools_path}  ${fan_test_tool_name}  ${fan_test_option1}  ${fan_wdt_pwm_pattern1}
    Step  4  set all FAN PWM  wd_sec -D 10
    Step  5  set all FAN PWM  wd_en -D 1
    Step  6  set Time To Sleep  20
    Step  7  verify diag tool test result  ${diag_tools_path}  ${fan_test_tool_name}  ${fan_test_option1}  ${fan_wdt_pwm_pattern2}  
    [Teardown]  set all FAN PWM  duty_cycle=50


DIAG_10.38_Interrupt_Checking_Test
    [Tags]  DIAG_10.38_Interrupt_Checking_Test  tianhe
	[Setup]  boot Into DiagOS Mode
    Step  1  verify Interrupt Checking
	Step  2  hotswap interrupt test  ${HotSwap_Alter_TOOL1}  ${low_power_mode}
    Step  3  set ltc4287 alert test    ${I2CSET_TOOL1}
    Step  4  hotswap interrupt test  ${HotSwap_Alter_TOOL1}  ${high_power_mode}
    Step  5  set ltc4287 alert test    ${I2CSET_TOOL2}
    Step  6  hotswap interrupt test  ${HotSwap_Alter_TOOL1}  ${low_power_mode}
    Step  7  hotswap interrupt test  ${HotSwap_Alter_TOOL2}  ${low_power_mode}
    Step  8  set ltc4287 alert test    ${I2CSET_TOOL3}
    Step  9  hotswap interrupt test  ${HotSwap_Alter_TOOL2}  ${high_power_mode}
    Step  10  set ltc4287 alert test    ${I2CSET_TOOL4}
    Step  11  hotswap interrupt test  ${HotSwap_Alter_TOOL2}  ${low_power_mode}


DIAG_10.40_RJ45_MANAGEMENT_PORT_PING_TEST
    [Tags]  DIAG_10.40_RJ45_MANAGEMENT_PORT_PING_TEST  tianhe
    [Setup]  boot Into DiagOS Mode
    Step  1  switch folder path  ${diag_tools_path}
    Step  2  modify phy config file  ${dhcpTool}  ${mgmt_interface}  ${tftp_server_ipv4}  ${phyFile}
    Step  3  write speed and ping test  ${phyTool}  ${writeSpeedTool}  ${ethSpeedTool}  ${mgmt_interface}


DIAG_10.42_RTC_ACCESS_TEST
    [Tags]  DIAG_10.42_RTC_ACCESS_TEST  tianhe
    [Setup]  boot Into DiagOS Mode
    Step  1  switch folder path  ${diag_tools_path}
    Step  2  rtc time rollover or write or read check  ${rtcTool}  ${allOption}  ${rtcPattern1}
    Step  3  rtc time rollover or write or read check  ${rtcTool}  ${setRtcOption}  ${rtcPattern2}
    Step  4  rtc time rollover or write or read check  ${rtcTool}  ${readRtcOption}  ${rtcPattern3}
    Step  5  power Cycle To DiagOS
    Step  6  switch folder path  ${diag_tools_path}
    Step  7  rtc time rollover or write or read check  ${rtcTool}  ${readRtcOption}  ${rtcPattern3}


DIAG_10.44_QSFP_DD_PORTS_I2C_ACCESS_TEST
    [Tags]  DIAG_10.44_QSFP_DD_PORTS_I2C_ACCESS_TEST  tianhe
	Step  1  verify diag tool test result  ${diag_tools_path}  ${sfp_cmd}  ${sfp_option_all}  ${sfp_profile1_pattern}
    Step  2  verify diag tool test result  ${diag_tools_path}  ${sfp_cmd}  ${sfp_option_show}  ${sfp_show_pattern}
    Step  3  check cmd no output  ${sfp_profile1_cmd}
    Step  4  verify diag tool test result  ${diag_tools_path}  ${sfp_cmd}  ${sfp_option_all}  ${sfp_profile1_pattern}
    Step  5  check cmd no output  ${sfp_profile2_cmd}
    Step  6  verify diag tool test result  ${diag_tools_path}  ${sfp_cmd}  ${sfp_option_all}  ${sfp_profile2_pattern}
    Step  7  check cmd no output  ${sfp_profile3_cmd}
    Step  8  verify diag tool test result  ${diag_tools_path}  ${sfp_cmd}  ${sfp_option_all}  ${sfp_profile3_pattern}
    [Teardown]  check cmd no output  ${sfp_profile1_cmd}


#DIAG_TC45_QSFP_OPTICAL_MODULE_MODSELL_SIGNAL_TEST
#    [Tags]  DIAG_TC45_QSFP_OPTICAL_MODULE_MODSELL_SIGNAL_TEST
#    ...  tianhe
#
#    Step  1  QSFP-DD page select for all modules
#    Step  2  QSFP-DD set power mode for all modules  ${qsfp_dd_cmd1}
#    Step  2  QSFP-DD set power mode for all modules  ${qsfp_dd_cmd2}

DIAG_10.45_QSFP_OPTICAL_MODULE_MODSELL_SIGNAL_TEST
    [Tags]  DIAG_10.45_QSFP_OPTICAL_MODULE_MODSELL_SIGNAL_TEST tianhe
    [Setup]  boot Into DiagOS Mode
    Step  1  qsfp Page Select And Read

#DIAG_TC47_QSFP_OPTICAL_MODULE_INTL_SIGNAL_TEST
#    [Tags]  DIAG_TC47_QSFP_OPTICAL_MODULE_INTL_SIGNAL_TEST
#    ...  tianhe
#
#    Step  1  QSFP-DD page select for all modules
#    Step  2  QSFP-DD set IntL for all modules
#    Step  3  QSFP-DD verify IntL signal status for all modules  pattern=(?m)^(?P<intl>1)$
#    Step  4  QSFP-DD clear IntL for all modules
#    Step  5  QSFP-DD verify IntL signal status for all modules  pattern=(?m)^(?P<intl>0)$

DIAG_10.47_QSFP_OPTICAL_MODULE_INTL_SIGNAL_TEST
    [Tags]  DIAG_10.47_QSFP_OPTICAL_MODULE_INTL_SIGNAL_TEST tianhe
    [Setup]  boot Into DiagOS Mode
    Step  1  qsfp Optical Module Set IntL
    Step  2  check IntL Signal Status  ^1$
    Step  3  qsfp I2c Page Select And Clear
    Step  4  check IntL Signal Status  ^0$

#DIAG_TC48_QSFP_OPTICAL_MODULE_RESETL_SIGNAL_TEST
#    [Tags]  DIAG_TC48_QSFP_OPTICAL_MODULE_RESETL_SIGNAL_TEST
#    ...  tianhe
#
#    Step  1  QSFP-DD page select for all modules  command=0x50 0x7f 0x00
#    Step  2  QSFP-DD set high power mode for all modules
#    Step  3  QSFP optical module resetl signal  command1=${qsfp_reset_module_cmd1}  command2=${check_qsfp_reset_module_cmd}  pattern=${qsfp_reset_module_pattern1}
#    Step  4  QSFP optical module resetl signal  command1=${qsfp_reset_module_cmd2}  command2=${check_qsfp_reset_module_cmd}  pattern=${qsfp_reset_module_pattern2}

DIAG_10.48_QSFP_OPTICAL_MODULE_RESETL_SIGNAL_TEST
    [Tags]  DIAG_10.48_QSFP_OPTICAL_MODULE_RESETL_SIGNAL_TEST  tianhe
    ${type} =  judge The Type Of Loopback
    Run Keyword If  "${type}"=="AWS"  Run Keywords
    ...  Step  1  set All And Set One By One  reset  AND
    ...  Step  2  read Aws ResetL Status  0x1  AND
    ...  Step  3  unset All And Unset One By One  reset  AND
    ...  Step  4  read Aws ResetL Status  0x0  AND
    ...  Step  5  optical Module auto Test  ${diag_ld_lib_path}  ${qsfp_optical_cmd_1}  ${qsfp_optical_pattern_1}
    Run Keyword IF  "${type}"=="LEONI"  Run Keywords
    ...  Step  1  page Select And Set High mode  AND
    ...  Step  2  set All And Set One By One  reset  AND
    ...  Step  3  unset All And Unset One By One  reset

DIAG_10.49_QSFP_Optical_Module_LPMode_Signal_Test
    [Tags]  DIAG_10.49_QSFP_Optical_Module_LPMode_Signal_Test  tianhe
	${type} =  judge The Type Of Loopback
    Run Keyword If  "${type}"=="AWS"  Run Keywords
    ...  Step  1  set All And Set One By One  lpmod  AND
    ...  Step  2  read Aws LPMode Status  0x1  AND
    ...  Step  3  unset All And Unset One By One  lpmod  AND
    ...  Step  4  read Aws LPMode Status  0x0  AND
    ...  Step  5  optical Module auto Test  ${diag_ld_lib_path}  ${qsfp_optical_cmd}  ${qsfp_optical_pattern}
    Run Keyword IF  "${type}"=="LEONI"  Run Keywords
    ...  Step  1  page Select And Set High mode New  AND
    ...  Step  2  set All And Set One By One  lpmod  AND
    ...  Step  3  read Leoni LPMode Status  0x1  AND
    ...  Step  4  unset All And Unset One By One  lpmod  AND
    ...  Step  5  read Leoni LPMode Status  0x0

DIAG_10.50_INSTALL_UBOOT_BY_FLASHCP_TEST
    [Tags]  DIAG_10.50_INSTALL_UBOOT_BY_FLASHCP_TEST  tianhe
    [Setup]  boot Into DiagOS Mode
    Step  1  verify diag tool test result  ${diag_tools_path}  ${cat_tool}  ${mtd_cat_option}  ${mtd_cat_pattern}  $(is_ssd_cmd)
    Step  2  get dhcp ip
    Step  3  tftp download image to unit  ${serverip}  ${ubootImgHostPath}  ${ubootImgFile}  ${ubootImgUnitPath}
    Step  4  flash uboot partition  ${flashTool}  ${ubootDevice}  ${ubootImgFile}  ${ubootImgUnitPath}
    Step  5  boot into uboot
    Step  6  reset Uboot Env
    Step  7  boot Into DiagOS Mode
    Step  8  verify boot image  ${get_versions_cmd}	

DIAG_10.51_DiagOS (NOS) update with installer Test
    [Tags]  DIAG_10.51_DiagOS_(NOS)_update_with_installer_Test
    [Setup]  boot Into Onie Rescue Mode
    Step  1  Diag Check network connectivity  ${ONIE_RESCUE_MODE}
    Step  2  fhv2 Diag download Images And Recovery DiagOS
    Step  3  power Cycle To DiagOS
    Step  4  check version before the test

#DIAG_TC51_INSTALL_UBOOT_NOR_FLASH_BY_TFTP_TEST
#    [Tags]  DIAG_TC51_INSTALL_UBOOT_NOR_FLASH_BY_TFTP_TEST
#    ...  tianhe
#
#    [Setup]  boot Into Onie Rescue Mode
#    Step  1  Diag Check network connectivity  ${ONIE_RESCUE_MODE}
#    Step  2  fhv2 Diag download Images And Recovery DiagOS
#    Step  3  power Cycle To DiagOS
#    Step  4  get Dhcp IP
#    Step  5  Diag Check network connectivity  ${BOOT_MODE_DIAGOS}
#    Step  6  fhv2 Diag download stress And Recovery DiagOS
#    [Teardown]  decompress sdk


DIAG_10.54.1_1-16byte_burst_mode_with_I2C_speed_400K_1M
    [Documentation]  This test is to check 1-16byte burst mode with I2C speed 400K/1M
    [Tags]  DIAG_10.54.1_1-16byte_burst_mode_with_I2C_speed_400K_1M  tianhe  1pps
    [Timeout]  50 min 00 seconds
    [Setup]  boot Into DiagOS Mode
	Step  1  switch folder path  ${diag_tools_path}
    Step  2  check byte burst test  ${SFP_TOOL_OPTION1}  ${SFP_TOOL_OPTION2}  ${SINGLE_lst1}
    Step  3  change i2c bus speed  ${SFP_PROFILE_TOOL1}
    Step  4  check byte burst test  ${SFP_TOOL_OPTION1}  ${SFP_TOOL_OPTION2}  ${SINGLE_lst1}
    Step  5  change i2c bus speed  ${SFP_PROFILE_TOOL2}
    Step  6  check byte burst test  ${SFP_TOOL_OPTION1}  ${SFP_TOOL_OPTION2}  ${SINGLE_lst1}
    Step  7  change i2c bus speed  ${SFP_PROFILE_TOOL3}
    Step  8  check byte burst test  ${SFP_TOOL_OPTION1}  ${SFP_TOOL_OPTION2}  ${SINGLE_lst1}

DIAG_10.54.2_128-byte_burst_mode_with_I2C_speed_400K_1M
    [Documentation]  This test is to check 128-byte burst mode with I2C speed 400K/1M
    [Tags]  DIAG_10.54.2_128-byte_burst_mode_with_I2C_speed_400K_1M  tianhe  1pps
    [Timeout]  50 min 00 seconds
    [Setup]  boot Into DiagOS Mode
	Step  1  switch folder path  ${diag_tools_path}
    Step  2  check byte burst test  ${SFP_TOOL_OPTION1}  ${SFP_TOOL_OPTION2}  ${SINGLE_lst2}
    Step  3  change i2c bus speed  ${SFP_PROFILE_TOOL1}
    Step  4  check byte burst test  ${SFP_TOOL_OPTION1}  ${SFP_TOOL_OPTION2}  ${SINGLE_lst2}
    Step  5  change i2c bus speed  ${SFP_PROFILE_TOOL2}
    Step  6  check byte burst test  ${SFP_TOOL_OPTION1}  ${SFP_TOOL_OPTION2}  ${SINGLE_lst2}
    Step  7  change i2c bus speed  ${SFP_PROFILE_TOOL3}
    Step  8  check byte burst test  ${SFP_TOOL_OPTION1}  ${SFP_TOOL_OPTION2}  ${SINGLE_lst2}

DIAG_10.54.3_128-byte_32_Multi-threads_I2C_buses_with_speed_400K_1M
    [Documentation]  This test is to check 128-byte Multi-threads with I2C speed 400K/1M
    [Tags]  DIAG_10.54.3_128-byte_32_Multi-threads_I2C_buses_with_speed_400K_1M  tianhe  1pps
    [Timeout]  50 min 00 seconds
    [Setup]  boot Into DiagOS Mode
	Step  1  switch folder path  ${diag_tools_path}
    Step  2  check qsfp real time access test  ${SFP_MULTI_TOOL}
    Step  3  change i2c bus speed  ${SFP_PROFILE_TOOL1}
    Step  4  check qsfp real time access test  ${SFP_MULTI_TOOL}
    Step  5  change i2c bus speed  ${SFP_PROFILE_TOOL2}
    Step  6  check qsfp real time access test  ${SFP_MULTI_TOOL}
    Step  7  change i2c bus speed  ${SFP_PROFILE_TOOL3}
    Step  8  check qsfp real time access test  ${SFP_MULTI_TOOL}


DIAG_11.1_Check_FPGA_version_and_board_version
    [Documentation]  This test is to check FPGA function after reset
    [Tags]  DIAG_11.1_Check_FPGA_version_and_board_version  tianhe  1pps
    [Timeout]  5 min 00 seconds
    [Setup]  boot Into DiagOS Mode
    Step  1  check fpga and board version  ${fpga1ppsTool}  ${boardTool}

DIAG_11.2_FPGA_Reset_Check
    [Documentation]  This test is to check FPGA function after reset
    [Tags]  DIAG_11.2_FPGA_Reset_Check  tianhe  1pps
    [Timeout]  5 min 00 seconds
    [Setup]  boot Into DiagOS Mode
    Step  1  Reload FPGA
    Step  2  Check FPGA Function after reset


DIAG_11.3_FPGA_BRAM_Read/Write_Test
    [Documentation]  This test is to test FPGA_BRAM_Read/Write
    [Tags]  DIAG_11.3_FPGA_BRAM_Read/Write_Test  tianhe  1pps
    [Timeout]  5 min 00 seconds
    [Setup]  boot Into DiagOS Mode
    Step  1  check fpga bram access


DIAG_11.4_Read_all_FPGA_registers
    [Documentation]  This test is to read all FPGA registers word by word to check FPGA memory hole
    [Tags]   DIAG_11.4_Read_all_FPGA_registers  tianhe  1PPS
    [Timeout]  5 min 00 seconds
    [Setup]  boot Into DiagOS Mode
    Step  1  read all fpga registers

DIAG_11.5.1_QSFP_Present_register_check
    [Documentation]  This test is to check QSFP
    [Tags]   DIAG_11.5.1_QSFP_Present_register_check  tianhe  1PPS
    [Timeout]  5 min 00 seconds
    [Setup]  boot Into DiagOS Mode
    Step  1  switch folder path  ${diag_tools_path}
    Step  2  qsfp all present check  ${spi_test_tool}  ${qsfpPresentOption}

DIAG_11.5.2_QSFP_LPmode_register_(0x0170)_check
    [Tags]  DIAG_11.5.2_QSFP_LPmode_register_(0x0170)_check  tianhe
    ${type} =  judge The Type Of Loopback
    Run Keyword If  "${type}"=="AWS"  Run Keywords
    ...  Step  1  switch folder path  ${diag_tools_path}  AND
    ...  Step  2  set All lpmode power mode  ${low_power_mode}  ${lpmode_all_option}  AND
    ...  Step  3  read lpmode pin status  3  ${low_power_mode}  ${i2cget_tool}  ${i2cget_option}  AND
    ...  Step  4  set All lpmode power mode  ${high_power_mode}  ${lpmode_all_option}  AND
    ...  Step  5  read lpmode pin status  3  ${high_power_mode}  ${i2cget_tool}  ${i2cget_option}  AND
    ...  Step  6  set lpmode power one by one  ${low_power_mode}  ${pps_i2c_tool}  ${pps_i2c_option}  AND
    ...  Step  7  read lpmode pin status  3  ${low_power_mode}  ${i2cget_tool}  ${i2cget_option}  AND
    ...  Step  8  set lpmode power one by one  ${high_power_mode}  ${pps_i2c_tool}  ${pps_i2c_option}  AND
    ...  Step  9  read lpmode pin status  3  ${high_power_mode}  ${i2cget_tool}  ${i2cget_option}  AND
    ...  Step  10  eric lpmode auto test  ${qsfp_optical_cmd}  ${lpmode_register_pattern}
    Run Keyword IF  "${type}"=="LEONI"  Run Keywords
    ...  Step  1  page Select And Set High mode  AND
    ...  Step  2  set All And Set One By One  reset  AND
    ...  Step  3  unset All And Unset One By One  reset

DIAG_11.5.3_QSFP_Reset_register_(0x0178)_check
    [Tags]  DIAG_11.5.3_QSFP_Reset_register_(0x0178)_check  tianhe
    ${type} =  judge The Type Of Loopback
    Run Keyword If  "${type}"=="AWS"  Run Keywords
    ...  Step  1  switch folder path  ${diag_tools_path}  AND
    ...  Step  2  set All lpmode power mode  ${low_power_mode}  ${resetL_all_option}  AND
    ...  Step  3  read lpmode pin status  2  ${high_power_mode}  ${i2cget_tool}  ${i2cget_option}  AND
    ...  Step  4  set All lpmode power mode  ${high_power_mode}  ${resetL_all_option}  AND
    ...  Step  5  read lpmode pin status  2  ${low_power_mode}  ${i2cget_tool}  ${i2cget_option}  AND
    ...  Step  6  set lpmode power one by one  ${low_power_mode}  ${pps_i2c_tool}  ${reset_register_option}  AND
    ...  Step  7  read lpmode pin status  2  ${high_power_mode}  ${i2cget_tool}  ${i2cget_option}  AND
    ...  Step  8  set lpmode power one by one  ${high_power_mode}  ${pps_i2c_tool}  ${reset_register_option}  AND
    ...  Step  9  read lpmode pin status  2  ${low_power_mode}  ${i2cget_tool}  ${i2cget_option}  AND
    ...  Step  10  eric lpmode auto test  ${qsfp_optical_cmd_1}  ${reset_register_pattern}
    Run Keyword IF  "${type}"=="LEONI"  Run Keywords
    ...  Step  1  page Select And Set High mode  AND
    ...  Step  2  set All And Set One By One  reset  AND
    ...  Step  3  unset All And Unset One By One  reset

DIAG_11.6.1_QSFP_Present_INTERRUPT_Test
    [Documentation]  This test is to test QSFP Present INTERRUPT/Present interrupt Mask REGISTER/PCIe MSI status/MSI IRQ Status
    [Tags]   DIAG_11.6.1_QSFP_Present_INTERRUPT_Test  tianhe  1PPS
    [Timeout]  5 min 00 seconds
    [Setup]  boot Into DiagOS Mode
    Step  1  check qsfp present interrupt status

DIAG_11.6.2_QSFP_Interrupt_Test
    [Documentation]  This test is to test QSFP Interrupt/Interrupt Mask register/PCIe MSI status/MSI IRQ status
    [Tags]    DIAG_11.6.2_QSFP_Interrupt_Test  tianhe  1PPS
    [Timeout]  5 min 00 seconds
    [Setup]  boot Into DiagOS Mode
    Step  1  check qsfp irq status

DIAG_11.6.3_I2C_RTC_IRQ_Status_Test
    [Documentation]  This test is to test I2C RTC Status/RTC Interrupt Mask/PCIe MSI status/MSI IRQ status
    [Tags]   DIAG_11.6.3_I2C_RTC_IRQ_Status_Test  tianhe  1PPS
    [Timeout]  5 min 00 seconds
    [Setup]  boot Into DiagOS Mode
    Step  1  check i2c rtc irq status

DIAG_11.9.1_PCIE_BUS_FUNCTION
    [Tags]  DIAG_11.9.1_PCIE_BUS_FUNCTION  tianhe  1pps
    [Timeout]  5 min 00 seconds
#[Setup]  change dir  ${diag_tools_path}
    Step  1  pcie bus test




*** Keywords ***
DiagOS Connect Device
    DiagOSConnect

DiagOS Disconnect Device
    DiagOSDisconnect
