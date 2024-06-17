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
    [Tags]  DIAG_TC00_Diag_Initialize_And_Version_Check  fenghuang
    [Setup]  boot Into Onie Rescue Mode
    Step  1  Diag Check network connectivity  ${ONIE_RESCUE_MODE}
    Step  2  Diag format Disk  ${fail_dict}
    Step  3  Diag mount Disk  ${fail_dict}
    Step  4  Diag download Images And Recovery DiagOS  ${fail_dict}
    Step  5  Self Update Onie  new
    Step  6  power Cycle To DiagOS
    Step  7  check version before the test
    Step  8  check driver version  ${drive_pattern}

DIAG_TC01_POST_Test
    [Tags]  DIAG_TC01_POST_Test  fenghuang
    Step  1  verify hw version  ${export_cmd_list}  ${get_hw_version_path}  ${hw_version_dict}  ${get_hw_versions_tool}  ${get_hw_versions_option}


DIAG_TC02_Boot-up_Image_Updating(Only for NPI stage)
    [Tags]  DIAG_TC02_Boot-up_Image_Updating(Only for NPI stage)  fenghuang
    [Setup]  boot into uboot
    Step  1  set static address
    Step  2  update boot image
    Step  3  to onine and verify boot image  ${get_versions_cmd}


DIAG_TC03_CPLD_Image_Updating(Only for NPI stage)
    [Tags]  DIAG_TC03_CPLD_Image_Updating(Only for NPI stage)  fenghuang
    [Setup]  boot Into DiagOS Mode
    Step  1  upgrade diag cpld  ${vmetool_path}  ${vmetool}
    Step  2  power cycle to DiagOS


DIAG_TC04_Boot-Up_Test
    [Tags]  DIAG_TC04_Boot-Up_Test  fenghuang
    [Setup]  boot into uboot
    Step  1  verify boot to each mode
    Step  2  reset default boot to diag
    Step  3  set default env


DIAG_TC05_UART_MUX_Function_Test
    [Tags]  DIAG_TC05_UART_MUX_Function_Test  fenghuang
    [Setup]  boot Into DiagOS Mode
    Step  1  check Uart Mux Function  ${check_uart_cmd}


DIAG_TC06_Management_Port_MAC_Address_Modify
    [Tags]  DIAG_TC06_Management_Port_MAC_Address_Modify  fenghuang
    [Timeout]  5 min
    [Setup]  boot Into DiagOS Mode
    Step  1  check Mac Address
    Step  2  modify Mac Address

DIAG_TC07_Switch_Board_EEPROM_Burning
    [Tags]  DIAG_TC07_Switch_Board_EEPROM_Burning  fenghuang
    [Timeout]  15 min
    [Setup]  boot Into DiagOS Mode
    Step  1  burning Tlv Data
    Step  2  prepare EEPROM Burning  ${eeprom_burning_cmd}
    Step  3  verify Init Ouput Same As D1  ${eeprom_d1_cmd}  ${eeprom_init_cmd}
    Step  4  burning Tlv Data  ${TLV_Value_Test}
    Step  5  prepare EEPROM Burning  ${eeprom_burning_cmd2}
    [Teardown]  burning Tlv Data

DIAG_TC08_FAN_Control_Board_EEPROM_Burning
    [Tags]  DIAG_TC08_FAN_Control_Board_EEPROM_Burning  fenghuang
    [Timeout]  5 min
    [Setup]  boot Into DiagOS Mode
    Step  1  write Fan Control Value
    Step  2  check Fan Control Value

#duplicated with TC06
#DIAG_TC08_MANAGEMENT_PORT_MAC_ADDRESS_MODIFY
#    [Tags]  DIAG_TC08_MANAGEMENT_PORT_MAC_ADDRESS_MODIFY
#    ...  briggs  fenghuang  shenzhou  tigris
#    ...  npi_stage
#
#    Step  1  verify MGMT port MAC address modification


DIAG_TC10_System_Information_Checking
    [Tags]  DIAG_TC10_System_Information_Checking  fenghuang
    [Timeout]  10 min
    [Setup]  boot Into DiagOS Mode
    Step  1  check HW info
    Step  2  check SDK Version
    Step  3  check ONIE version


DIAG_TC11_CPLD_ACCESS_TEST
    [Tags]  DIAG_TC11_CPLD_ACCESS_TEST
    ...  briggs  fenghuang  shenzhou  tigris

    [Setup]  boot Into DiagOS Mode
    Step  1  export env path  ${export_cmd_list}
    Step  2  verify CPLD versions
    Step  3  verify CPLD dump device register
    Step  4  verify CPLD tool help option


DIAG_TC12_MAIN_BOARD_VERSION_CHECK
    [Tags]  DIAG_TC12_MAIN_BOARD_VERSION_CHECK
    ...  briggs  fenghuang  shenzhou  tigris

    [Setup]  boot Into DiagOS Mode
    Step  1  cat main board version
    Step  2  check Main Board Version By CPLD


DIAG_TC13_CPU_DDR_Memory_Test
    [Tags]  DIAG_TC13_CPU_DDR_Memory_Test  fenghuang
    [Setup]  boot Into DiagOS Mode
    Step  1  export env path  ${export_cmd_list}
    Step  2  verify diag tool test result  ${diag_tools_path}  ${mem_test_tool_name}  ${mem_test_option}  ${mem_test_passPattern}


DIAG_TC14_I2C_Bus_Scan_Test
    [Tags]  DIAG_TC14_I2C_Bus_Scan_Test  fenghuang
    [Setup]  boot Into DiagOS Mode
    Step  1  export env path  ${export_cmd_list}
    Step  2  verify diag tool test result  ${diag_tools_path}  ${i2c_test_tool_name}  ${i2c_test_option}  ${i2c_test_pattern}


DIAG_TC15_PCIE_SCAN_TEST
    [Tags]  DIAG_TC15_PCIE_SCAN_TEST
    ...  briggs  fenghuang  shenzhou  tigris

    Step  1  Detect all PCIe devices on the BUS


DIAG_TC16_Switch_Device_Access_Test
    [Tags]  DIAG_TC16_Switch_Device_Access_Test  fenghuang
    Step  1  verify diag tool test result  ${diag_tools_path}  ${device_access_test_cmd}  ${device_access_test_option}  ${device_access_test_pattern}  True


DIAG_TC17_Switch_SPI_Flash_Access_Test
    [Tags]  DIAG_TC17_Switch_SPI_Flash_Access_Test  fenghuang
    [Timeout]  10 min
    [Setup]  boot Into DiagOS Mode
    Step  1  check SDK Version


DIAG_TC18_On-board_DC/DC_Controller_Access_Test
    [Tags]  DIAG_TC18_On-board_DC/DC_Controller_Access_Test  fenghuang
    [Setup]  export env path  ${export_cmd_list}
    Step  1  verify diag tool test result  ${diag_tools_path}  ${dcdc_test_tool_name}  ${dcdc_test_option1}  ${pattern_of_option1}
    Step  2  verify diag tool test result  ${diag_tools_path}  ${dcdc_test_tool_name}  ${dcdc_test_option2}  ${pattern_of_option2}
    Step  3  verify diag tool test result  ${diag_tools_path}  ${dcdc_test_tool_name}  ${dcdc_test_option3}  ${pattern_of_option2}
    Step  4  verify diag tool test result  ${diag_tools_path}  ${dcdc_test_tool_name}  ${dcdc_test_option4}  ${pattern_of_option2}


DIAG_TC19_Power_Monitor_Functional_Test
    [Tags]  DIAG_TC19_Power_Monitor_Functional_Test  fenghuang
    [Setup]  export env path  ${export_cmd_list}
    Step  1  verify diag tool test result  ${diag_tools_path}  ${dcdc_test_tool_name}  ${dcdc_test_option5}  ${pattern_of_option3}
    Step  2  verify diag tool test result  ${diag_tools_path}  ${dcdc_test_tool_name}  ${dcdc_test_option6}  ${pattern_of_option3}
    Step  3  verify diag tool test result  ${diag_tools_path}  ${dcdc_test_tool_name}  ${dcdc_test_option7}  ${pattern_of_option3}
    Step  4  verify diag tool test result  ${diag_tools_path}  ${dcdc_test_tool_name}  ${dcdc_test_option8}  ${pattern_of_option3}
    Step  5  verify diag tool test result  ${diag_tools_path}  ${dcdc_test_tool_name}  ${dcdc_test_option9}  ${pattern_of_option3}
    Step  6  verify diag tool test result  ${diag_tools_path}  ${dcdc_test_tool_name}  ${dcdc_test_option1}  ${pattern_of_option1}
    Step  7  verify diag tool test result  ${diag_tools_path}  ${dcdc_test_tool_name}  ${dcdc_test_option10}  ${pattern_of_option1}
    Step  8  verify diag tool test result  ${diag_tools_path}  ${dcdc_test_tool_name}  ${dcdc_test_option11}  ${pattern_of_option1}
    Step  9  verify diag tool test result  ${diag_tools_path}  ${dcdc_test_tool_name}  ${dcdc_test_option12}  ${pattern_of_option1}


DIAG_TC20_SATA_Device_Access_Test
    [Tags]  DIAG_TC20_SATA_Device_Access_Test  fenghuang
    [Setup]  export env path  ${export_cmd_list}
    Step  1  verify diag tool test result  ${diag_tools_path}  ${sata_device_test_tool_name}  ${sata_device_test_option}  ${sata_device_test_pattern}


DIAG_TC21_SSD_Device_Health_Status_Test
    [Tags]  DIAG_TC21_SSD_Device_Health_Status_Test  fenghuang
    Step  1  verify diag tool test result  ${ssd_test_path}  ${ssd_test_tool_name}  ${ssd_test_option}  ${ssd_test_pattern}  $(is_ssd_cmd)
    Step  2  wait for execute  ${ssd_test_time_stamp}
    Step  3  verify diag tool test result  ${ssd_test_path}  ${ssd_test_tool_name}  ${ssd_status_check_option}  ${ssd_test_verify_pattern}  $(is_ssd_cmd)


DIAG_TC22_SPI_to_I2C&I/O_Device(SC18IS600)_Access_Test
    [Tags]  DIAG_TC22_SPI_to_I2C&I/O_Device(SC18IS600)_Access_Test  fenghuang
    [Setup]  export env path  ${export_cmd_list}
    Step  1  verify diag tool test result  ${diag_tools_path}  ${spi_test_tool}  ${spi_test_option}  ${spi_test_pattern}
    Step  2  verify i2cdetect with l  ${spi_i2c_test_cmd}  ${spi_i2c_test_option}
    Step  3  verify diag tool test result  ${diag_tools_path}  ${spi_i2c_test_cmd}  ${spi_i2c_test_option1}  ${spi_i2c_test_pattern}  True


DIAG_TC23_System_Watchdog_Test
    [Tags]  DIAG_TC23_System_Watchdog_Test  fenghuang
    Step  1  check cmd no output  ${system_watchdog_test_cmd}
    Step  2  verify system watchdog


DIAG_TC24_System_Reset_Test
    [Tags]  DIAG_TC24_System_Reset_Test  fenghuang
    Step  1  system reset to diag  ${warm_reset_cmd}
    Step  2  system reset to diag  ${cold_reset_cmd}


DIAG_TC26_SRAM_Access_Test
    [Tags]  DIAG_TC26_SRAM_Access_Test  fenghuang
    [Setup]  boot Into DiagOS Mode
    Step  1  export env path  ${export_cmd_list}
    Step  2  fault Log Sram WR  ${fault_log_cmd}  ${log_pattern}
    Step  3  console Log Sram WR  ${log_pattern}


DIAG_TC27_PRESENT_STATUS_TEST
    [Tags]  DIAG_TC27_PRESENT_STATUS_TEST
    ...  briggs  fenghuang  shenzhou  tigris

    Step  1  check CPLD's PRSTN2X16N status


DIAG_TC28_PSU_TEST
    [Tags]  DIAG_TC28_PSU_TEST
    ...  fenghuang

    Step  1  check all PSU status
    Step  2  show all PSU values
    Step  3  show PSU1 values
    Step  4  show PSU2 values


DIAG_TC29_TEMPERATURE_SENSOR_ACCESS_TEST
    [Tags]  DIAG_TC29_TEMPERATURE_SENSOR_ACCESS_TEST
    ...  fenghuang
    ...  uncompleted

    Step  1  access all temperature sensor devices
    # Step  2  check temperature in specific mode  # ./cel-temp-test: unrecognized option '--mode'
    Step  3  show temperature sensor


DIAG_TC30_FAN_BOARD_CPLD_ACCESS_TEST
    [Tags]  DIAG_TC30_FAN_BOARD_CPLD_ACCESS_TEST
    ...  fenghuang

    Step  1  verify CPLDs access on I2C bus by "-s -d 4" option
    Step  2  verify CPLDs firmware version


DIAG_TC31_FAN_Present_Test
    [Tags]  DIAG_TC31_FAN_Present_Test
    ...  fenghuang
    [Setup]  export env path  ${export_cmd_list}
    Step  1  verify diag tool test result  ${diag_tools_path}  ${fan_test_tool_name}  ${fan_test_option1}  ${fan_test_pattern}
    Step  2  verify diag tool test result  ${diag_tools_path}  ${fan_test_tool_name}  ${fan_test_option2}  ${fan_test_pattern}


DIAG_TC34_FAN_TRAY_SPEED_TEST
    [Tags]  DIAG_TC34_FAN_TRAY_SPEED_TEST
    ...  fenghuang

    Step  1   show all FAN PWM/RPM
    Step  2   show FAN PWM/RPM
    Step  3   Verify current FAN PWM/RPM is not excess maximum

    Step  4   set all FAN PWM  duty_cycle=100
    Step  5   set all FAN PWM  duty_cycle=75
    Step  6   set all FAN PWM  duty_cycle=50

    Step  7   set PWM to specified FAN device  duty_cycle=100  fan_number=1
    Step  8   set PWM to specified FAN device  duty_cycle=100  fan_number=2
    Step  9   set PWM to specified FAN device  duty_cycle=100  fan_number=3
    Step  10  set PWM to specified FAN device  duty_cycle=100  fan_number=4
    Step  11  set PWM to specified FAN device  duty_cycle=100  fan_number=5
    Step  12  set PWM to specified FAN device  duty_cycle=100  fan_number=6
    Step  13  set PWM to specified FAN device  duty_cycle=100  fan_number=7

    Step  14  set PWM to specified FAN device  duty_cycle=75  fan_number=1
    Step  15  set PWM to specified FAN device  duty_cycle=75  fan_number=2
    Step  16  set PWM to specified FAN device  duty_cycle=75  fan_number=3
    Step  17  set PWM to specified FAN device  duty_cycle=75  fan_number=4
    Step  18  set PWM to specified FAN device  duty_cycle=75  fan_number=5
    Step  19  set PWM to specified FAN device  duty_cycle=75  fan_number=6
    Step  20  set PWM to specified FAN device  duty_cycle=75  fan_number=7

    Step  21  set PWM to specified FAN device  duty_cycle=50  fan_number=1
    Step  22  set PWM to specified FAN device  duty_cycle=50  fan_number=2
    Step  23  set PWM to specified FAN device  duty_cycle=50  fan_number=3
    Step  24  set PWM to specified FAN device  duty_cycle=50  fan_number=4
    Step  25  set PWM to specified FAN device  duty_cycle=50  fan_number=5
    Step  26  set PWM to specified FAN device  duty_cycle=50  fan_number=6
    Step  27  set PWM to specified FAN device  duty_cycle=50  fan_number=7


DIAG_TC35_FAN_CTRL_TEST
    [Tags]  DIAG_TC35_FAN_CTRL_TEST
    ...  fenghuang

    Step  1  FAN control test


DIAG_TC36_FAN_WDT_FUNCTION_TEST
    [Tags]  DIAG_TC36_FAN_WDT_FUNCTION_TEST
    ...  fenghuang

    Step  1  set all FAN PWM  duty_cycle=50
    Step  2  show FAN PWM/RPM
    Step  3  verify all FAN PWM already changed to assigned value  duty_cycle=50
    Step  4  set FAN watchdog trigger time  time=10
    Step  5  enable FAN watchdog function
    Step  6  Sleep  15 seconds
    Step  7  verify all FAN PWM should be auto-changed to maximum after the watchdog is timeout

    [Teardown]  set all FAN PWM  duty_cycle=50


DIAG_TC37_FRU_EEPROM_ACCESS_TEST
    [Tags]  DIAG_TC37_FRU_EEPROM_ACCESS_TEST
    ...  fenghuang

    Step  1  dump all FRU EEPROM content depents on fenghuang model


DIAG_TC40_RJ45_MANAGEMENT_PORT_PING_TEST
    [Tags]  DIAG_TC40_RJ45_MANAGEMENT_PORT_PING_TEST
    ...  fenghuang

    Step  1  renew IP using DHCP  console=${diagos_mode}  interface=${mgmt_interface}
    Step  2  edit/update server IP and our IP on configs/phys.yaml file
    Step  3  diagnose MGMT port ping test


DIAG_TC42_RTC_ACCESS_TEST
    [Tags]  DIAG_TC42_RTC_ACCESS_TEST
    ...  fenghuang

    Step  1  set new date/time to RTC chip
    Step  2  Kapok reboot to U-Boot and enter to Diag OS
    Step  3  verify the RTC chip is continue counting correctly


DIAG_TC44_QSFP_DD_PORTS_I2C_ACCESS_TEST
    [Tags]  DIAG_TC44_QSFP_DD_PORTS_I2C_ACCESS_TEST
    ...  fenghuang

    Step  1  diagnose I2C/loopback


DIAG_TC45_QSFP_OPTICAL_MODULE_MODSELL_SIGNAL_TEST
    [Tags]  DIAG_TC45_QSFP_OPTICAL_MODULE_MODSELL_SIGNAL_TEST
    ...  fenghuang

    Step  1  QSFP-DD page select for all modules
    Step  2  QSFP-DD read ModSelL pin status for all modules


DIAG_TC47_QSFP_OPTICAL_MODULE_INTL_SIGNAL_TEST
    [Tags]  DIAG_TC47_QSFP_OPTICAL_MODULE_INTL_SIGNAL_TEST
    ...  fenghuang

    Step  1  QSFP-DD page select for all modules
    Step  2  QSFP-DD set IntL for all modules
    Step  3  QSFP-DD verify IntL signal status for all modules  pattern=(?m)^(?P<intl>1)$
    Step  4  QSFP-DD clear IntL for all modules
    Step  5  QSFP-DD verify IntL signal status for all modules  pattern=(?m)^(?P<intl>0)$


DIAG_TC48_QSFP_OPTICAL_MODULE_RESETL_SIGNAL_TEST
    [Tags]  DIAG_TC48_QSFP_OPTICAL_MODULE_RESETL_SIGNAL_TEST
    ...  fenghuang

    Step  1  QSFP-DD page select for all modules  command=0x50 0x7f 0x00
    Step  2  QSFP-DD set high power mode for all modules
    Step  3  QSFP-DD reset for all modules
    Step  4  QSFP-DD verify low power mode for all modules


DIAG_TC50_INSTALL_UBOOT_BY_FLASHCP_TEST
    [Tags]  DIAG_TC50_INSTALL_UBOOT_BY_FLASHCP_TEST
    ...  fenghuang

    Step  1  read and expected to see the mtd partition for U-Boot
    Step  2  renew IP using DHCP  console=${diagos_mode}  interface=${tftp_interface}
    Step  3  download new U-Boot's boot.img file used to flash to the mtd uboot partition
    Step  4  flash U-Boot's boot.img to the mtd uboot partition
    Step  5  reboot to verify the mtd uboot partition is bootable


DIAG_TC51_INSTALL_UBOOT_NOR_FLASH_BY_TFTP_TEST
    [Tags]  DIAG_TC51_INSTALL_UBOOT_NOR_FLASH_BY_TFTP_TEST
    ...  fenghuang

    [Setup]  boot into uboot
    Step  1  set Uboot IP
    Step  2  U-Boot setenv  env=serverip ${tftp_server_ipv4}
    Step  3  update boot image
#    Step  4  U-Boot reset
#    Step  5  U-Boot reset environment to default
#    Step  6  U-Boot save current environment to flash memory


DIAG_TC54_POWER_CYCLE_TEST
    [Tags]  DIAG_TC54_POWER_CYCLE_TEST
    ...  fenghuang

    Step  1  power cycle to mode  mode=${diagos_mode}


DIAG_TC55_DDR_STRESS_TEST
    [Tags]  DIAG_TC55_DDR_STRESS_TEST
    ...  fenghuang

    Step  1  execute command and verify with a pattern
    ...  console=${diagos_mode}
    ...  command=(bash ddr_test.sh)
    ...  path=${tools_script_stress_path}
    ...  sec=9000  # 2.5 hours and typically 2 hours
    ...  pattern=Status:[ \\t]*PASS
    ...  msg=Failed, not found the pass message!
    ...  is_check_exit_code=${TRUE}


DIAG_TC56_SSD_STRESS_TEST
    [Tags]  DIAG_TC56_SSD_STRESS_TEST
    ...  fenghuang

    [Setup]  boot Into DiagOS Mode
    Step  1  run Ssd Stress Test


DIAG_TC57_I2C_BUS_SCAN_STRESS_TEST
    [Tags]  DIAG_TC57_I2C_BUS_SCAN_STRESS_TEST
    ...  fenghuang

    Step  1  I2C bus scan stress test


DIAG_TC58_DIAG_ALL_TEST
    [Tags]  DIAG_TC58_DIAG_ALL_TEST
    ...  fenghuang

    Step  1  run all diagnostic test


*** Keywords ***
DiagOS Connect Device
    DiagOSConnect

DiagOS Disconnect Device
    DiagOSDisconnect
