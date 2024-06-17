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
    [Tags]  DIAG_TC00_Diag_Initialize_And_Version_Check  fenghuangv2
    [Setup]  boot Into Onie Rescue Mode
    Step  1  Diag Check network connectivity  ${ONIE_RESCUE_MODE}
    Step  2  fhv2 Diag download Images And Recovery DiagOS
    Step  3  Self Update Onie  new
    Step  4  power Cycle To DiagOS
    Step  5  check version before the test
    Step  6  check driver version  ${drive_pattern}


DIAG_10.1_POST_Test
    [Tags]  DIAG_10.1_POST_Test  fenghuangv2
    Step  1  check Post Info  ${post_test_pattern}

DIAG_10.2_Boot-up_Image_Updating_Only_for_NPI_stage
    [Tags]  DIAG_10.2_Boot-up_Image_Updating_Only_for_NPI_stage  fenghuangv2
    [Setup]  boot into uboot
    Step  1  set static address
    Step  2  update boot image
    Step  3  power Cycle To onie rescue mode  # WORKAROUNDD, if no this step unit will hung
    Step  4  verify boot image  ${get_versions_cmd}

#This case is temporarily not applicable to fenghuangv2
#and the operation may cause other cases to fail.
#It should be fixed to the applicable fenghuangv2 and then executed
DIAG_10.3_CPLD_Image_Updating(Only for NPI stage)
    [Tags]  DIAG_10.3_CPLD_Image_Updating(Only for NPI stage)  fenghuangv2
    [Setup]  boot Into DiagOS Mode
    Step  1  upgrade diag cpld  ${vmetool_path}  ${vmetool}
    Step  2  power cycle to DiagOS
    Step  3  check cpld version


DIAG_10.4_SYSCPLD_Backup_Image_Test
    [Tags]  DIAG_10.4_SYSCPLD_Backup_Image_Test  fenghuangv2
    [Setup]  boot into DiagOS Mode
    Step  1  erase sys cpld image 
    Step  2  power cycle to DiagOS
    Step  3  check SYSCPLD version 
    Step  4  restore sys cpld image 
    Step  5  power cycle to DiagOS
    Step  6  verify cpld version

DIAG_10.5_Boot-Up_Test
    [Tags]  DIAG_10.5_Boot-Up_Test  fenghuangv2
    [Setup]  boot into uboot
    Step  1  verify boot to each mode
    #Step  2  reset default boot to diag
    #Step  3  set default env


DIAG_10.6_UART_MUX_Function_Test
    [Tags]  DIAG_10.6_UART_MUX_Function_Test  fenghuangv2
    [Setup]  boot Into DiagOS Mode
    Step  1  check Uart Mux Function  ${check_uart_cmd}


DIAG_10.7_Management_Port_MAC_Address_Modify
    [Tags]  DIAG_10.7_Management_Port_MAC_Address_Modify   fenghuangv2
    [Timeout]  5 min
    [Setup]  boot Into Uboot
    Step  1  reset Uboot Env
    Step  2  boot Into DiagOS Mode
    ${mac} =  KapokDiagLib.get mac address
    Step  3  check Mac Address
    Step  4  modify Mac Address
    Step  5  boot Into Uboot   ## @WORKAROUND, Step 5, 6 to avoid this issue "ERROR: can't get kernel image"
    Step  6  reset Uboot Env
    Step  7  boot Into DiagOS Mode
    Step  8  check Mac Address
    [Teardown]  modify Mac Address  ${mac}

DIAG_10.8_Switch_Board_EEPROM_Burning
    [Tags]  DIAG_10.8_Switch_Board_EEPROM_Burning   fenghuangv2
    [Timeout]  15 min
    [Setup]  boot Into DiagOS Mode
    ${mac} =  KapokDiagLib.get mac address
    Step  1  burning Tlv Data
    Step  2  prepare EEPROM Burning  ${eeprom_burning_cmd}
    Step  3  verify Init Ouput Same As D1  ${eeprom_d1_cmd}  ${eeprom_init_cmd}
    Step  4  burning Tlv Data  ${TLV_Value_Test}
    Step  5  prepare EEPROM Burning  ${eeprom_burning_cmd2}
    [Teardown]  Run Keywords  burning Tlv Data  AND  modify Mac Address  ${mac}

DIAG_10.9_FAN_Control_Board_EEPROM_Burning
    [Tags]  DIAG_10.9_FAN_Control_Board_EEPROM_Burning   fenghuangv2
    [Timeout]  15 min
    [Setup]  boot Into DiagOS Mode
    Step  1  disable All Protect
    Step  1  read Fan Control Value
    [Teardown]  boot Into DiagOS Mode

DIAG_10.10_FRU_EEPROM_ACCESS_TEST
    [Tags]  DIAG_10.10_FRU_EEPROM_ACCESS_TEST
    ...  fenghuangv2

    Step  1  dump all FRU EEPROM content depents on fenghuangv2 model

#Step  2  fru Eeprom Access Test
#duplicated with TC06
#DIAG_TC08_MANAGEMENT_PORT_MAC_ADDRESS_MODIFY
#    [Tags]  DIAG_TC08_MANAGEMENT_PORT_MAC_ADDRESS_MODIFY
#    ...  briggs  fenghuangv2  shenzhou  tigris
#    ...  npi_stage
#
#    Step  1  verify MGMT port MAC address modification


DIAG_10.11_System_Information_Checking
    [Tags]  DIAG_10.11_System_Information_Checking   fenghuangv2
    [Timeout]  10 min
    [Setup]  boot Into DiagOS Mode
    Step  1  check HW info
    Step  2  check SDK Version
    Step  3  boot Into Onie Rescue Mode
    Step  4  check ONIE version


DIAG_10.12_CPLD_ACCESS_TEST
    [Tags]  DIAG_10.12_CPLD_ACCESS_TEST
    ...  briggs  fenghuangv2  shenzhou  tigris

    [Setup]  boot Into DiagOS Mode
    Step  1  verify CPLD access


DIAG_10.13_MAIN_BOARD_VERSION_CHECK
    [Tags]  DIAG_10.13_MAIN_BOARD_VERSION_CHECK
    ...  briggs  fenghuangv2  shenzhou  tigris

    [Setup]  boot Into DiagOS Mode
    Step  1  check Main Board Version By CPLD


DIAG_10.14_TPM_Device_Access_Test
    [Documentation]  This test is to check vendor id, device id and the presence of TPM device
    [Tags]  DIAG_10.14_TPM_Device_Access_Test  fenghuangv2
    [Timeout]  5 min 00 seconds
    [Setup]  boot Into DiagOS Mode
    Step  1  TPM Device Access Test

DIAG_10.15_CPU_DDR_Memory_Test
    [Tags]  DIAG_10.15_CPU_DDR_Memory_Test  fenghuangv2
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

DIAG_10.16_CPU_SDR_Access_Test
    [Documentation]  This test is to finish reading SDR data from uC successfully.
    [Tags]  DIAG_10.16_CPU_SDR_Access_Test  fenghuangv2
    [Timeout]  5 min 00 seconds
    [Setup]  boot Into DiagOS Mode
    Step  1  CPU SDR Access Test

DIAG_10.17_I2C_Bus_Scan_Test
    [Tags]  DIAG_10.17_I2C_Bus_Scan_Test  fenghuangv2
    [Setup]  boot Into DiagOS Mode
    Step  1  export env path  ${export_cmd_list}
    Step  2  verify diag tool test result  ${diag_tools_path}  ${i2c_test_tool_name}  ${i2c_test_option}  ${i2c_test_pattern}


DIAG_10.18_PCIE_SCAN_TEST
    [Tags]  DIAG_10.18_PCIE_SCAN_TEST
    ...  briggs  fenghuangv2  shenzhou  tigris

    Step  1  Detect all PCIe devices on the BUS


DIAG_10.19_Switch_Device_Access_Test
    [Tags]  DIAG_10.19_Switch_Device_Access_Test  fenghuangv2
    Step  1  verify diag tool test result  ${diag_tools_path}  ${device_access_test_cmd}  ${device_access_test_option}  ${device_access_test_pattern}  True


DIAG_10.20_Switch_SBus_Flash_Access_Test
    [Tags]  DIAG_10.20_Switch_SBus_Flash_Access_Test  fenghuangv2
    [Timeout]  10 min
    [Setup]  boot Into DiagOS Mode
    Step  1  check PCIE Firmware Version


DIAG_10.21_On-board_DC/DC_Controller_Access_Test
    [Tags]  DIAG_10.21_On-board_DC/DC_Controller_Access_Test  fenghuangv2
    [Setup]  export env path  ${export_cmd_list}
    Step  1  verify diag tool test result  ${diag_tools_path}  ${dcdc_test_tool_name}  ${dcdc_access_option1}  ${passpattern_of_option1}
    Step  2  verify diag tool test result  ${diag_tools_path}  ${dcdc_test_tool_name}  ${dcdc_access_option2}  ${passpattern_of_option2}
    Step  3  verify diag tool test result  ${diag_tools_path}  ${dcdc_test_tool_name}  ${dcdc_access_option3}  ${passpattern_of_option2}


DIAG_10.22_Power_Monitor_Functional_Test
    [Tags]  DIAG_10.22_Power_Monitor_Functional_Test  fenghuangv2
    [Setup]  export env path  ${export_cmd_list}
    Step  1  verify diag tool test result  ${diag_tools_path}  ${dcdc_test_tool_name}  ${dcdc_test_option1}  ${pattern_of_option1}
    Step  2  verify diag tool test result  ${diag_tools_path}  ${dcdc_test_tool_name}  --mode low --show  ${pattern_of_option1}
    Step  3  verify diag tool test result  ${diag_tools_path}  ${dcdc_test_tool_name}  --mode normal --show  ${pattern_of_option1}
    Step  4  verify diag tool test result  ${diag_tools_path}  ${dcdc_test_tool_name}  --mode high --show  ${pattern_of_option1}
    Step  5  verify diag tool test result  ${diag_tools_path}  ${dcdc_test_tool_name}  ${dcdc_test_option2}  ${pattern_of_option2}
    Step  6  verify diag tool test result  ${diag_tools_path}  ${dcdc_test_tool_name}  --mode low --all  ${pattern_of_option2}
    Step  7  verify diag tool test result  ${diag_tools_path}  ${dcdc_test_tool_name}  --mode normal --all  ${pattern_of_option2}
    Step  8  verify diag tool test result  ${diag_tools_path}  ${dcdc_test_tool_name}  --mode high --all  ${pattern_of_option2}

DIAG_10.23_ROV_Functional_Test
    [Documentation]  This test is to check the actual VDD core output against the target ROV
    [Tags]  DIAG_10.23_ROV_Functional_Test  fenghuangv2
    [Timeout]  5 min 00 seconds
    [Setup]  boot Into DiagOS Mode
    Step  1  ROV Functional Test


DIAG_10.24_SATA_Device_Access_Test
    [Tags]  DIAG_10.24_SATA_Device_Access_Test  fenghuangv2
    [Setup]  export env path  ${export_cmd_list}
    Step  1  disk l
    Step  2  verify diag tool test result  ${diag_tools_path}  ${sata_device_test_tool_name}  ${sata_device_test_option}  ${sata_device_test_pattern}


DIAG_10.25_SSD_Device_Health_Status_Test
    [Tags]  DIAG_10.25_SSD_Device_Health_Status_Test  fenghuangv2
    Step  1  verify diag tool test result  ${ssd_test_path}  ${ssd_test_tool_name}  ${ssd_test_option}  ${ssd_test_pattern}  $(is_ssd_cmd)
    Step  2  wait for execute  ${ssd_test_time_stamp}
    Step  3  verify diag tool test result  ${ssd_test_path}  ${ssd_test_tool_name}  ${ssd_status_check_option}  ${ssd_test_verify_pattern}  $(is_ssd_cmd)


#DIAG_TC22_SPI_to_I2C&I/O_Device(SC18IS600)_Access_Test
#    [Tags]  DIAG_TC22_SPI_to_I2C&I/O_Device(SC18IS600)_Access_Test  fenghuangv2
#    [Setup]  export env path  ${export_cmd_list}
#    Step  1  verify i2cdetect with l  ${spi_i2c_test_cmd}  ${spi_i2c_test_option}
#    Step  2  verify diag tool test result  ${diag_tools_path}  ${spi_i2c_test_cmd}  ${spi_i2c_test_option1}  ${spi_i2c_test_pattern}  True


DIAG_10.26_System_Watchdog_Test
    [Tags]  DIAG_10.26_System_Watchdog_Test  fenghuangv2
    Step  1  check cmd no output  ${system_watchdog_test_cmd}
    Step  2  verify system watchdog  ${system_watchdog_reset_cmd}


DIAG_10.27_System_Reset_Test
    [Tags]  DIAG_10.27_System_Reset_Test  fenghuangv2
    Step  1  system reset to diag  ${warm_reset_cmd}
    Step  2  system reset to diag  ${cold_reset_cmd}

DIAG_10.28_SRAM_Access_Test
    [Tags]  DIAG_10.28_SRAM_Access_Test  fenghuangv2
    [Setup]  boot Into DiagOS Mode
    Step  1  export env path  ${export_cmd_list}
    Step  2  fhv2 Fault Log Sram  ${fault_log_cmd}  ${fault_log_pattern1}  ${fault_log_pattern2}
	Step  3  fhv2 Console Log Sram  ${console_log_cmd1}  ${console_log_cmd2}  ${console_log_pattern1}  ${console_log_pattern2}

DIAG_10.29_PRESENT_STATUS_TEST
    [Tags]  DIAG_10.29_PRESENT_STATUS_TEST
    ...  briggs  fenghuangv2  shenzhou  tigris

    Step  1  check CPLD's PRSTN2X16N status


DIAG_10.30_PSU_TEST
    [Tags]  DIAG_10.30_PSU_TEST
    ...  fenghuangv2

    Step  1  check all PSU status
    Step  2  show all PSU values
    Step  3  show PSU1 values
    #Step  4  show PSU2 values  #Testplan has no such step in the log


DIAG_10.31_TEMPERATURE_SENSOR_ACCESS_TEST
    [Tags]  DIAG_10.31_TEMPERATURE_SENSOR_ACCESS_TEST
    ...  fenghuangv2

    Step  1  verify diag tool test result  ${diag_tools_path}  ${temp_test_tool_name}  ${temp_test_option1}  ${temp_test_pattern1}
    Step  2  verify diag tool test result  ${diag_tools_path}  ${temp_test_tool_name}  ${temp_test_option2}  ${temp_test_pattern2}
    Step  3  verify diag tool test result  ${diag_tools_path}  ${temp_test_tool_name}  ${temp_test_option3}  ${temp_test_pattern1}
    Step  4  verify diag tool test result  ${diag_tools_path}  ${temp_test_tool_name}  ${temp_test_option4}  ${temp_test_pattern1}
    Step  5  verify diag tool test result  ${diag_tools_path}  ${temp_test_tool_name}  ${temp_test_option5}  ${temp_test_pattern1}

DIAG_10.32_FAN_BOARD_CPLD_ACCESS_TEST
    [Tags]  DIAG_10.32_FAN_BOARD_CPLD_ACCESS_TEST
    ...  fenghuangv2

    Step  1  verify CPLDs access on I2C bus by "-s -d 4" option
    Step  2  verify CPLDs firmware version


DIAG_10.33_FAN_Present_Test
    [Tags]  DIAG_10.33_FAN_Present_Test
    ...  fenghuangv2
    [Setup]  export env path  ${export_cmd_list}
    Step  1  verify diag tool test result  ${diag_tools_path}  ${fan_test_tool_name}  ${fan_test_option1}  ${fan_test_pattern}
    Step  2  verify diag tool test result  ${diag_tools_path}  ${fan_test_tool_name}  ${fan_test_option2}  ${fan_test_pattern}


DIAG_10.36_FAN_TRAY_SPEED_TEST
    [Tags]  DIAG_10.36_FAN_TRAY_SPEED_TEST
    ...  fenghuangv2

    Step  1  show all FAN PWM RPM
    Step  2  show FAN PWM RPM  ${fan_pwm_rpm_show_patterns}
    Step  3  set all FAN PWM  pwm -D 255
    Step  4  verify diag tool test result  ${diag_tools_path}  ${fan_speed_tool_name}  ${fan_speed_option}  ${fan_speed_pattern1}
    Step  5  set all FAN PWM  pwm -D 191
    Step  6  verify diag tool test result  ${diag_tools_path}  ${fan_speed_tool_name}  ${fan_speed_option}  ${fan_speed_pattern2}
    Step  7  set all FAN PWM  pwm -D 127
    Step  8  verify diag tool test result  ${diag_tools_path}  ${fan_speed_tool_name}  ${fan_speed_option}  ${fan_speed_pattern3}

DIAG_10.37_FAN_CTRL_TEST
    [Tags]  DIAG_10.37_FAN_CTRL_TEST
    ...  fenghuangv2

    Step  1  verify fan ctrl test  ${diag_tools_path}  ${fan_ctrl_tool}  ${fan_ctrl_option}  ${fan_ctrl_test_pattern}


DIAG_10.38_FAN_WDT_FUNCTION_TEST
    [Tags]  DIAG_10.38_FAN_WDT_FUNCTION_TEST
    ...  fenghuangv2
    
    Step  1  set all FAN PWM  wd_en -D 0
    Step  2  set all FAN PWM  pwm -D 127
    Step  3  verify diag tool test result  ${diag_tools_path}  ${fan_test_tool_name}  ${fan_test_option1}  ${fan_wdt_pwm_pattern1}
    Step  4  set all FAN PWM  wd_sec -D 10
    Step  5  set all FAN PWM  wd_en -D 1
    Step  6  set Time To Sleep  20
    Step  7  verify diag tool test result  ${diag_tools_path}  ${fan_test_tool_name}  ${fan_test_option1}  ${fan_wdt_pwm_pattern2}

    [Teardown]  set all FAN PWM  duty_cycle=50




DIAG_10.41_RJ45_MANAGEMENT_PORT_PING_TEST
    [Tags]  DIAG_10.41_RJ45_MANAGEMENT_PORT_PING_TEST
    ...  fenghuangv2

    Step  1  renew IP using DHCP  console=${diagos_mode}  interface=${mgmt_interface}
    Step  2  edit/update server IP and our IP on configs/phys.yaml file
    Step  3  diagnose MGMT port ping test


DIAG_10.43_RTC_ACCESS_TEST
    [Tags]  DIAG_10.43_RTC_ACCESS_TEST
    ...  fenghuangv2

    Step  1  verify diag tool test result  ${diag_tools_path}  ${rtc_access_tool}  ${rtc_access_option1}  ${rtc_access_pattern1}
    Step  2  set new date/time to RTC chip
    Step  3  verify the RTC chip is continue counting correctly
    Step  4  power Cycle To DiagOS
    Step  5  verify the RTC chip is continue counting correctly


DIAG_10.45_QSFP_DD_PORTS_I2C_ACCESS_TEST
    [Tags]  DIAG_10.45_QSFP_DD_PORTS_I2C_ACCESS_TEST
    ...  fenghuangv2

    Step  1  verify diag tool test result  ${diag_tools_path}  ${sfp_cmd}  ${sfp_option_all}  ${sfp_profile1_pattern}
    Step  2  verify diag tool test result  ${diag_tools_path}  ${sfp_cmd}  ${sfp_option_show}  ${sfp_show_pattern}
    Step  3  check cmd no output  ${sfp_profile2_cmd}
    Step  4  verify diag tool test result  ${diag_tools_path}  ${sfp_cmd}  ${sfp_option_all}  ${sfp_profile2_pattern}
    Step  5  check cmd no output  ${sfp_profile1_cmd}
    Step  6  verify diag tool test result  ${diag_tools_path}  ${sfp_cmd}  ${sfp_option_all}  ${sfp_profile1_pattern}

    [Teardown]  check cmd no output  ${sfp_profile1_cmd}


#DIAG_TC45_QSFP_OPTICAL_MODULE_MODSELL_SIGNAL_TEST
#    [Tags]  DIAG_TC45_QSFP_OPTICAL_MODULE_MODSELL_SIGNAL_TEST
#    ...  fenghuangv2
#
#    Step  1  QSFP-DD page select for all modules
#    Step  2  QSFP-DD set power mode for all modules  ${qsfp_dd_cmd1}
#    Step  2  QSFP-DD set power mode for all modules  ${qsfp_dd_cmd2}

DIAG_10.46_QSFP_OPTICAL_MODULE_MODSELL_SIGNAL_TEST
    [Tags]  DIAG_10.46_QSFP_OPTICAL_MODULE_MODSELL_SIGNAL_TEST fenghuangv2
    [Setup]  boot Into DiagOS Mode
    Step  1  qsfp Page Select And Read

#DIAG_TC47_QSFP_OPTICAL_MODULE_INTL_SIGNAL_TEST
#    [Tags]  DIAG_TC47_QSFP_OPTICAL_MODULE_INTL_SIGNAL_TEST
#    ...  fenghuangv2
#
#    Step  1  QSFP-DD page select for all modules
#    Step  2  QSFP-DD set IntL for all modules
#    Step  3  QSFP-DD verify IntL signal status for all modules  pattern=(?m)^(?P<intl>1)$
#    Step  4  QSFP-DD clear IntL for all modules
#    Step  5  QSFP-DD verify IntL signal status for all modules  pattern=(?m)^(?P<intl>0)$

DIAG_10.48_QSFP_OPTICAL_MODULE_INTL_SIGNAL_TEST
    [Tags]  DIAG_10.48_QSFP_OPTICAL_MODULE_INTL_SIGNAL_TEST fenghuangv2
    [Setup]  boot Into DiagOS Mode
    Step  1  qsfp Optical Module Set IntL
    Step  2  check IntL Signal Status  ^1$
    Step  3  qsfp I2c Page Select And Clear
    Step  4  check IntL Signal Status  ^0$

#DIAG_TC48_QSFP_OPTICAL_MODULE_RESETL_SIGNAL_TEST
#    [Tags]  DIAG_TC48_QSFP_OPTICAL_MODULE_RESETL_SIGNAL_TEST
#    ...  fenghuangv2
#
#    Step  1  QSFP-DD page select for all modules  command=0x50 0x7f 0x00
#    Step  2  QSFP-DD set high power mode for all modules
#    Step  3  QSFP optical module resetl signal  command1=${qsfp_reset_module_cmd1}  command2=${check_qsfp_reset_module_cmd}  pattern=${qsfp_reset_module_pattern1}
#    Step  4  QSFP optical module resetl signal  command1=${qsfp_reset_module_cmd2}  command2=${check_qsfp_reset_module_cmd}  pattern=${qsfp_reset_module_pattern2}
DIAG_10.49_QSFP_OPTICAL_MODULE_RESETL_SIGNAL_TEST
    [Tags]  DIAG_10.49_QSFP_OPTICAL_MODULE_RESETL_SIGNAL_TEST
    ...  fenghuangv2
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

DIAG_10.50_QSFP_Optical_Module_LPMode_Signal_Test
    [Tags]  DIAG_10.50_QSFP_Optical_Module_LPMode_Signal_Test
    ...  fenghuangv2
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

DIAG_10.52_INSTALL_UBOOT_BY_FLASHCP_TEST
    [Tags]  DIAG_10.52_INSTALL_UBOOT_BY_FLASHCP_TEST
    ...  fenghuangv2

    Step  1  read and expected to see the mtd partition for U-Boot
    Step  2  renew IP using DHCP  console=${diagos_mode}  interface=${tftp_interface}
    Step  3  download new U-Boot's boot.img file used to flash to the mtd uboot partition
    Step  4  flash U-Boot's boot.img to the mtd uboot partition
    Step  5  reboot to verify the mtd uboot partition is bootable

DIAG_10.53_DiagOS (NOS) update with installer Test
    [Tags]  DIAG_10.53_DiagOS_(NOS)_update_with_installer_Test
    [Setup]  boot Into Onie Rescue Mode
    Step  1  Diag Check network connectivity  ${ONIE_RESCUE_MODE}
    Step  2  fhv2 Diag download Images And Recovery DiagOS
    Step  3  power Cycle To DiagOS
    Step  4  check version before the test

DIAG_11.1_PCIE_to_SPI_Field_upgrade
    [Documentation]  This test is to on-line update FPGA images to 1pps
    [Tags]    DIAG_11.1_PCIE_to_SPI_Field_upgrade  fenghuangv2
    [Timeout]  5 min 00 seconds
    [Setup]  boot Into DiagOS Mode
    Step  1  Check fpga include in dev
    Step  2  renew IP using DHCP  console=${diagos_mode}  interface=${tftp_interface}
    Step  2  Flash FPGA image
    Step  3  Power Cycle To DiagOS
    Step  4  Check FPGA Version

DIAG_11.2_FPGA_Reset_Check
    [Documentation]  This test is to check FPGA function after reset
    [Tags]  DIAG_11.2_FPGA_Reset_Check  fenghuangv2  1pps
    [Timeout]  5 min 00 seconds
    [Setup]  boot Into DiagOS Mode
    Step  1  Reload FPGA
    Step  2  Check FPGA Function after reset

DIAG_11.3_FPGA_BRAM_Read/Write_Test
    [Documentation]  This test is to test FPGA_BRAM_Read/Write
    [Tags]  DIAG_11.3_FPGA_BRAM_Read/Write_Test  fenghuangv2  1pps
    [Timeout]  5 min 00 seconds
    [Setup]  boot Into DiagOS Mode
    Step  1  check fpga bram access

DIAG_11.4_Read_all_FPGA_registers
    [Documentation]  This test is to read all FPGA registers word by word to check FPGA memory hole
    [Tags]   DIAG_11.4_Read_all_FPGA_registers  fenghuangv2  1PPS
    [Timeout]  5 min 00 seconds
    [Setup]  boot Into DiagOS Mode
    Step  1  read all fpga registers

DIAG_11.5.1_QSFP_Present_INTERRUPT_Test
    [Documentation]  This test is to test QSFP Present INTERRUPT/Present interrupt Mask REGISTER/PCIe MSI status/MSI IRQ Status
    [Tags]   DIAG_11.5.1_QSFP_Present_INTERRUPT_Test  fenghuangv2  1PPS
    [Timeout]  5 min 00 seconds
    [Setup]  boot Into DiagOS Mode
    Step  1  check qsfp present interrupt status

DIAG_11.5.2_QSFP_Interrupt_Test
    [Documentation]  This test is to test QSFP Interrupt/Interrupt Mask register/PCIe MSI status/MSI IRQ status
    [Tags]    DIAG_11.5.2_QSFP_Interrupt_Test  fenghuangv2  1PPS
    [Timeout]  5 min 00 seconds
    [Setup]  boot Into DiagOS Mode
    Step  1  check qsfp irq status

DIAG_11.5.3_I2C_RTC_IRQ_Status_Test
    [Documentation]  This test is to test I2C RTC Status/RTC Interrupt Mask/PCIe MSI status/MSI IRQ status
    [Tags]   DIAG_11.5.3_I2C_RTC_IRQ_Status_Test  fenghuangv2  1PPS
    [Timeout]  5 min 00 seconds
    [Setup]  boot Into DiagOS Mode
    Step  1  check i2c rtc irq status

DIAG_11.7.1_PCIE_BUS_FUNCTION
    [Tags]  DIAG_11.7.1_PCIE_BUS_FUNCTION  fenghuangv2  1pps
    [Timeout]  5 min 00 seconds
    [Setup]  change dir  ${diag_tools_path}
    Step  1  pcie bus test
#DIAG_TC51_INSTALL_UBOOT_NOR_FLASH_BY_TFTP_TEST
#    [Tags]  DIAG_TC51_INSTALL_UBOOT_NOR_FLASH_BY_TFTP_TEST
#    ...  fenghuangv2
#
#    [Setup]  boot Into Onie Rescue Mode
#    Step  1  Diag Check network connectivity  ${ONIE_RESCUE_MODE}
#    Step  2  fhv2 Diag download Images And Recovery DiagOS
#    Step  3  power Cycle To DiagOS
#    Step  4  get Dhcp IP
#    Step  5  Diag Check network connectivity  ${BOOT_MODE_DIAGOS}
#    Step  6  fhv2 Diag download stress And Recovery DiagOS
#    [Teardown]  decompress sdk


DIAG_12.3_POWER_CYCLE_TEST
    [Tags]  DIAG_12.3_POWER_CYCLE_TEST
    ...  fenghuangv2

    Step  1  power cycle to mode  mode=${diagos_mode}


DIAG_12.4_DDR_STRESS_TEST
    [Tags]  DIAG_12.4_DDR_STRESS_TEST
    ...  fenghuangv2

    [Setup]  boot Into DiagOS Mode
    Step  1  fhv2 Diag download stress And Recovery DiagOS
    Step  2  execute command and verify with a pattern
    ...  console=${diagos_mode}
    ...  command=(bash ddr_test.sh)
    ...  path=${tools_script_stress_path}
    ...  sec=9000  # 2.5 hours and typically 2 hours
    ...  pattern=DDR stress testing
    ...  msg=Failed, not found the pass message!
    ...  is_check_exit_code=${TRUE}
    Step  3  verify ddr stress test  ${cat_ddr_log}  ${cat_ddr_log_regexp}  ${cat_ddr_log_pattern}


DIAG_12.5_SSD_STRESS_TEST
    [Tags]  DIAG_12.5_SSD_STRESS_TEST
    ...  fenghuangv2

    [Setup]  boot Into DiagOS Mode
    Step  1  fhv2 Diag download stress And Recovery DiagOS
    Step  2  execute command and verify with a pattern
    ...  console=${diagos_mode}
    ...  command=(bash ssd_test.sh)
    ...  path=${tools_script_stress_path}
    ...  sec=21600  # Did not know how long, assumed not more than 6 hours
    ...  pattern=${ssd_stress_pass_patterns}
    ...  msg=Failed, not found the pass patterns!
    ...  is_check_exit_code=${TRUE}


DIAG_12.6_I2C_BUS_SCAN_STRESS_TEST
    [Tags]  DIAG_12.6_I2C_BUS_SCAN_STRESS_TEST
    ...  fenghuangv2

    Step  1  I2C bus scan stress test


DIAG_12.7_DIAG_ALL_TEST
    [Tags]  DIAG_12.7_DIAG_ALL_TEST
    ...  fenghuangv2

    Step  1  run all diagnostic test

#DIAG_10.50_QSFP_OPTICAL_MODULE_LPMODESIGNAL_TEST
#    [Tags]  DIAG_10.50_QSFP_OPTICAL_MODULE_LPMODESIGNAL_TEST
#    ...  fenghuangv2
#
#    Step  1  QSFP-DD page select for all modules
#    Step  2  QSFP optical module lpmode signal  command1=${qsfp_lpmode_module_cmd1}  command2=${check_qsfp_lpmode_module_cmd}  pattern=${qsfp_lpmode_module_pattern1}
#    Step  3  QSFP optical module lpmode signal  command1=${qsfp_lpmode_module_cmd2}  command2=${check_qsfp_lpmode_module_cmd}  pattern=${qsfp_lpmode_module_pattern2}

DIAG_12.9_ASC_UPDATE_TEST
    [Documentation]  This test is to update asc
    [Tags]     common  DIAG_12.9_ASC_UPDATE_TEST fenghuangv2
    [Timeout]  60 min 00 seconds
    Step  1  KapokCommonLib.power Cycle To DiagOS
    Step  2  run asc update test
    Step  3  KapokCommonLib.power Cycle To DiagOS
    Step  4  check asc version




*** Keywords ***
DiagOS Connect Device
    DiagOSConnect

DiagOS Disconnect Device
    DiagOSDisconnect
