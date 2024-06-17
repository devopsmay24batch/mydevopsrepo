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
Documentation     Kapok common BSP suite

Variables         kapok/KapokBspFhVariablesLatest.py
Variables         KapokBspVariable.py
Library           KapokBspLib.py
Library           CommonLib.py
Library           ../KapokCommonLib.py

# Those three lines are commonly include pattern for all sub-systems
# and hopefully no more or less to include and the variable is pass
# by argument not specified by file name
Resource          CommonKeywords.resource
Resource          KapokCommonKeywords.resource
Resource          KapokBspKeywords.resource

Suite Setup     DiagOS Connect Device
Suite Teardown  DiagOS Disconnect Device


*** Variables ***


*** Test Cases ***
BSP_TC00_Diag_Initialize_And_Version_Check
    [Documentation]  This test Initialize and Version Check
    [Tags]  BSP_TC00_Diag_Initialize_And_Version_Check  tianhe
    [Timeout]  60 min 00 seconds
	[Setup]  boot Into DiagOS Mode
    Step  1  dhclient get ip
    Step  2  update diagos and onie test
    Step  3  check version before the test
    Step  4  check driver version  ${drive_pattern_dict}

BSP_10.1.1.1_INSTALL_DRIVER_TEST
    [Tags]  BSP_10.1.1.1_INSTALL_DRIVER_TEST  tianhe
	Step  1  uboot boot to diagos
    Step  2  dhclient get ip
    Step  3  ping to IP  ${diagos_mode}  ${tftp_server_ipv4}
    Step  4  check or reinstall bsp driver  ${DRIVE_VER}

BSP_10.1.2.1.1_CPLD_Version_Test
    [Documentation]  This test is to check CPLD version
    [Tags]     BSP_10.1.2.1.1_CPLD_Version_Test  tianhe
    [Timeout]  2 min 00 seconds
    Step  1  verify cpld versions  filelist=${t_cpld_file_list}


BSP_10.1.2.1.2_BOARD_VERSION_TEST
    [Tags]  BSP_10.1.2.1.2_BOARD_VERSION_TEST  tianhe
    Step  1  Verify board version


BSP_10.1.2.1.3_CPLD_RAW_ACCESS_TEST
    [Tags]  BSP_10.1.2.1.3_CPLD_RAW_ACCESS_TEST  tianhe
	Step  1  read cpld1 register  ${RAW_ADDR_CMD}  ${RAW_DATA_CMD}  ${RAW_ADDR_RES}  ${SysCpldVer}
    Step  2  write cpld1 raw register  ${write_raw_data}  ${write_raw_addr}
    Step  3  read cpld1 register  ${RAW_ADDR_CMD}  ${RAW_DATA_CMD}  ${RAW_ADDR_TEST}  ${RAW_ADDR_RES}
    Step  4  write cpld1 raw register  ${test_raw_data}  ${test_raw_addr}
    Step  5  read cpld1 register  ${RAW_ADDR_CMD}  ${RAW_DATA_CMD}  ${RAW_ADDR_RES}  ${SysCpldVer}


BSP_10.1.3_CONSOLE_LOGGER_DUMP_TEST
    [Tags]  BSP_10.1.3_CONSOLE_LOGGER_DUMP_TEST  tianhe
    Step  1  switch bsp folder path  ${LOGGER_FOLDER}
    Step  2  check the console logs  ${LOGGER_DUMP_CMD1}
    Step  3  console logger reset or pause or start  ${LOGGER_RESET_CMD}
    Step  4  check the console logs  ${LOGGER_DUMP_CMD1}  ${UNAME_TOOL}
    Step  5  console logger reset or pause or start  ${LOGGER_PAUSE_CMD}
    Step  6  check the console logs  ${LOGGER_DUMP_CMD2}  ${PAUSE_PATTERN}
    Step  7  console logger reset or pause or start  ${LOGGER_START_CMD}
    Step  8  check the console logs  ${LOGGER_DUMP_CMD2}  ${FDISK_TOOL}
    Step  9  console logger reset or pause or start  ${LOGGER_RESET_CMD}

BSP_10.1.4_Fault_Logger_Dump_Test
    [Documentation]  this test is to check fault logger dump test
    [Tags]     BSP_10.1.4_Fault_Logger_Dump_Test  tianhe
    [Timeout]  10 min 00 seconds
    [Setup]  boot into diag os mode
    Step  1  check come fault logger test  ${MB_CPLD_PATH}  ${LOGGER_DUMP_TOOL}  ${RESET_LOGGER}  ${PAUSE_LOGGER}

BSP_10.1.5.1_Port_Module_Interrupt_Test
    [Documentation]  This test is to check the optical module interrupt status
    [Tags]     common  BSP_10.1.5.1_Port_Module_Interrupt_Test  tianhe
    [Timeout]  5 min 00 seconds
    [Setup]  boot into diag os mode
    Step  1  set or clear IntL signal test  ${i2c_tool}  ${i2c_set_option}
    Step  2  check IntL signal status  ${sfp_tool}  ${sfp_all_status_option}  ${interrupt_value1}
    Step  3  check one by one port signal status  ${sfp_status_cmd}  ${sfp_status_option}  ${interrupt_value1}
    Step  4  set or clear IntL signal test  ${i2c_tool}  ${i2c_clear_option}
    Step  5  check IntL signal status  ${sfp_tool}  ${sfp_all_status_option}  ${interrupt_value2}
    Step  6  check one by one port signal status  ${sfp_status_cmd}  ${sfp_status_option}  ${interrupt_value2}

BSP_10.1.5.2_Port_Module_Present_Test
    [Documentation]  This test is check the optical module predent status
    [Tags]     BSP_10.1.5.2_Port_Module_Present_Test  tianhe
    [Timeout]  5 min 00 seconds
    [Setup]  boot into diag os mode
    Step  1  check one by one port signal status  ${sfp_status_cmd}  ${sfp_present_option}  ${interrupt_value1}
	
BSP_10.1.5.3_Port_Module_Reset_Test
    [Documentation]  This test is check the optical module reset signal
    [Tags]     BSP_10.1.5.3_Port_Module_Reset_Test  tianhe
    [Timeout]  2 min 00 seconds
    [Setup]  boot into diag os mode
    Step  1  check one by one port signal status  ${sfp_status_cmd}  ${sfp_reset_option}  ${interrupt_value2}
    Step  2  write register to reset port module  ${sfp_set_cmd}  ${sfp_reset_option}  ${interrupt_value1}
    Step  3  check one by one port signal status  ${sfp_status_cmd}  ${sfp_reset_option}  ${interrupt_value1}
    Step  4  write register to reset port module  ${sfp_set_cmd}  ${sfp_reset_option}  ${interrupt_value2}
    Step  5  check one by one port signal status  ${sfp_status_cmd}  ${sfp_reset_option}  ${interrupt_value2}

BSP_10.1.6.1_PSU_Input_Good_Test
    [Documentation]  this test is to check psu input good test
    [Tags]     BSP_10.1.6.1_PSU_Input_Good_Test  tianhe
    [Timeout]  10 min 00 seconds
    [Setup]  boot into diag os mode
    Step  1  read psu1 input value test  ${PSU1_INPUT_TOOL}  ${interrupt_value1}

BSP_10.1.6.2_PSU_Output_Good_Test
    [Documentation]  this test is to check psu output good test
    [Tags]     BSP_10.1.6.2_PSU_Output_Good_Test  tianhe
    [Timeout]  10 min 00 seconds
    [Setup]  boot into diag os mode
    Step  1  read psu1 output value test  ${PSU1_OUTPUT_TOOL}  ${interrupt_value1}

BSP_10.1.6.3_PSU_Present_Test
    [Documentation]  this test is to check psu present test
    [Tags]     BSP_10.1.6.3_PSU_Present_Test  tianhe
    [Timeout]  10 min 00 seconds
    [Setup]  boot into diag os mode
    Step  1  read psu present value test  ${PSU1_PRESENT_TOOL}  ${interrupt_value1}

BSP_10.1.6.4_PSU_Voltage_Fault_Test
    [Documentation]  this test is to check PSU voltage fault status
    [Tags]     BSP_10.1.6.4_PSU_Voltage_Fault_Test  tianhe
    [Timeout]  1 min 00 seconds
    [Setup]   uboot boot to diagos
    Step  1  check psu voltage status test  ${psu_fault_cmd}  ${interrupt_value2}

BSP_10.1.6.5_PSU_Voltage_Up_Test
    [Documentation]  check PSU all voltage rails up stat
    [Tags]     BSP_10.1.6.5_PSU_Voltage_Up_Test  tianhe
    [Setup]   uboot boot to diagos
    [Timeout]  1 min 00 seconds
    Step  1  check psu voltage status test  ${psu_up_cmd}  ${interrupt_value2}

BSP_10.1.7.1_FAN_MAX_SPEED_TEST
    [Documentation]  check fan max speed
    [Tags]  BSP_10.1.7.1_FAN_MAX_SPEED_TEST  tianhe
    [Setup]   uboot boot to diagos
    Step  1  stop fcs before test  ${FAN_TOOL}
    Step  2  set fan speed  ${FAN_TOOL}  ${fan_50_option}
    Step  3  check fan max speed status  ${FAN_MAX_STATUS}  ${interrupt_value2}
    Step  4  write and read fan max speed  ${FAN_MAX_SPEED}  ${interrupt_value1}
    Step  5  read all fan speed  ${FAN_TOOL}  ${FAN_TOOL_OPTION}  ${FAN_255_VALUE}
    Step  6  write and read fan max speed  ${FAN_MAX_SPEED}  ${interrupt_value2}
    Step  7  set fan speed  ${FAN_TOOL}  ${fan_100_option}
    Step  8  read all fan speed  ${FAN_TOOL}  ${FAN_TOOL_OPTION}  ${FAN_100_VALUE}


BSP_10.1.8.1_SYSTEM_WATCHDOG_ENABLE_TEST
    [Documentation]  check system watchdog enable test
    [Tags]  BSP_10.1.8.1_SYSTEM_WATCHDOG_ENABLE_TEST  tianhe
    [Setup]   uboot boot to diagos
    Step  1  check the system watchdog status  ${WATCHDOG_ENABLE}  ${interrupt_value2}
    Step  2  write poreset value test  ${WATCHDOG_ENABLE}  ${interrupt_value1}
    Step  3  check the system watchdog status  ${WATCHDOG_ENABLE}  ${interrupt_value2}
    Step  4  enable or disable system watchdog  ${WATCHDOG_ENABLE}  ${interrupt_value2}
    Step  5  check the system watchdog status  ${WATCHDOG_ENABLE}  ${interrupt_value2}


BSP_10.1.8.2_System_Watchdog_Seconds_Test
    [Documentation]  check watchdog counter time
    [Tags]     BSP_10.1.8.2_System_Watchdog_Seconds_Test  tianhe
    [Timeout]  10 min 00 seconds
    [Setup]  boot into diag os mode
    Step  1  enable or disable system watchdog  ${WATCHDOG_SECOND}  ${TRIGGER_10_TIME}
    Step  2  check the system watchdog status  ${WATCHDOG_SECOND}  ${TRIGGER_10_TIME}
    Step  3  multi enable system watchdog  ${WATCHDOG_ENABLE}  ${interrupt_value1}  ${TRIGGER_5_TIME}
    Step  4  check the system watchdog status  ${WATCHDOG_SECOND}  ${interrupt_value2}
    Step  5  check the system watchdog status  ${WATCHDOG_ENABLE}  ${interrupt_value2}


BSP_10.1.8.3_FAN_Watchdog_Enable_Test
    [Documentation]  This test is to check that enable of disable Fan watchdog function
    [Tags]     BSP_10.1.8.3_FAN_Watchdog_Enable_Test  tianhe
    [Timeout]  6 min 00 seconds
    [Setup]  boot into diag os mode
    Step  1  stop fcs before test  ${FAN_TOOL}
    Step  2  check current fan watchdog  ${FAN_WATCHDOG_ENABLE_CMD}  ${interrupt_value1}
    Step  3  set fan watchdog enable or disable  ${FAN_WATCHDOG_ENABLE_CMD}  ${interrupt_value2}
    Step  4  check current fan watchdog  ${FAN_WATCHDOG_ENABLE_CMD}  ${interrupt_value2}
    Step  5  switch bsp folder path  ${DIAG_PATH}
    Step  6  set fan speed  ${FAN_TOOL}  ${fan_50_option}
    Step  7  read all fan speed  ${FAN_TOOL}  ${FAN_TOOL_OPTION}  ${FAN_50_VALUE}
    Step  8  set fan watchdog enable or disable  ${FAN_WATCHDOG_ENABLE_CMD}  ${interrupt_value1}
    Step  9  check current fan watchdog  ${FAN_WATCHDOG_ENABLE_CMD}  ${interrupt_value1}
    Step  10  check fan speed value  ${FAN_TOOL}  ${FAN_TOOL_OPTION}  ${FAN_50_VALUE}


BSP_10.1.8.4_FAN_Watchdog_Seconds_Test
    [Documentation]  This test is to check that enable of disable Fan watchdog function
    [Tags]     BSP_10.1.8.4_FAN_Watchdog_Seconds_Test  tianhe
    [Timeout]  6 min 00 seconds
    [Setup]  boot into diag os mode
    Step  1  stop fcs before test  ${FAN_TOOL}
    Step  2  set fan watchdog enable or disable  ${FAN_WATCHDOG_ENABLE_CMD}  ${interrupt_value1}
    Step  3  check the system watchdog status  ${FAN_WATCHDOG_SEC_CMD}  ${FAN_60_VALUE}
    Step  4  enable or disable system watchdog  ${FAN_WATCHDOG_SEC_CMD}  ${TRIGGER_10_TIME}
    Step  5  check the system watchdog status  ${FAN_WATCHDOG_SEC_CMD}  ${TRIGGER_10_TIME}
    Step  6  set and check fan speed  ${FAN_TOOL}  ${fan_50_option}  ${FAN_TOOL_OPTION}  ${FAN_50_VALUE}

BSP_10.1.10.1_WARM_RESET_TEST
    [Documentation]  This test is to check warm reset function
    [Tags]  BSP_10.1.10.1_WARM_RESET_TEST  tianhe
    [Setup]  boot into diag os mode
    Step  1  check warm or cold reset test  ${WARM_REBOOT_CMD}

BSP_10.1.10.2_COLD_RESET_TEST
    [Documentation]  This test is to check cold reset function
    [Tags]  BSP_10.1.10.2_COLD_RESET_TEST  tianhe
    [Setup]  boot into diag os mode
    Step  1  check warm or cold reset test  ${COLD_REBOOT_CMD}

BSP_10.1.10.3_Fan_CPLD_Reset_Test
    [Documentation]  This test is to check fan reset status
    [Tags]     BSP_10.1.10.3_Fan_CPLD_Reset_Test  tianhe
    [Timeout]  3 min 00 seconds
    [Setup]  boot into diag os mode
    Step  1  read fan reset value  ${FAN_RESET_CMD}  ${interrupt_value2}
    Step  2  reset fan cpld test  ${FAN_RESET_CMD}  ${interrupt_value1}
    Step  3  read fan reset value  ${FAN_RESET_CMD}  ${interrupt_value2}

BSP_10.1.10.4_LED_CPLD_CPLD2_3_Reset_Test
    [Documentation]  This test is to check cpld2/3 reset status
    [Tags]     BSP_10.1.10.4_LED_CPLD_CPLD2_3_Reset_Test  tianhe
    [Timeout]  3 min 00 seconds
    [Setup]  boot into diag os mode
    Step  1  check led cpld reset  ${LED_CPLD_RESET_CMD}  ${interrupt_value2}
    Step  2  reset led cpld test  ${LED_CPLD_RESET_CMD}  ${interrupt_value1}
    Step  3  check led cpld reset  ${LED_CPLD_RESET_CMD}  ${interrupt_value2}
    [Teardown]  set to original value  ${LED_CPLD_RESET_CMD}  ${interrupt_value2}

BSP_10.1.11.1_Swith_Board_EEPROM_Test
    [Documentation]  This test is to check board EEPROM
    [Tags]     BSP_10.1.11.1_Swith_Board_EEPROM_Test  tianhe
    [Timeout]  6 min 00 seconds
    [Setup]  boot into diag os mode
    Step  1  check switch board eeprom status  ${SYS_EEPROM_CMD}  ${interrupt_value1}
    Step  2  disable or enable write protect  ${SYS_EEPROM_CMD}  ${interrupt_value2}
    Step  3  read switch board eeprom test  ${HEX_TOOL}  ${HEX_OPTION}  ${HEX_PATTERN1}
    Step  4  write some data into eeprom  ${HEX_OPTION}  ${HEX_PATTERN3}
    Step  5  read back the eeprom data  ${HEX_TOOL}  ${HEX_OPTION}  ${HEX_PATTERN2}
    Step  6  write original data back to eeprom  ${HEX_OPTION}  ${HEX_PATTERN1}
    Step  7  read switch board eeprom test  ${HEX_TOOL}  ${HEX_OPTION}  ${HEX_PATTERN1}
    Step  8  disable or enable write protect  ${SYS_EEPROM_CMD}  ${interrupt_value1}
    Step  9  write some data into eeprom again  ${HEX_OPTION}  ${HEX_PATTERN3}  ${HEX_PATTERN4}

BSP_10.1.12.1_Fan_Direction_Test
    [Documentation]  This test is to check fan direction
    [Tags]     BSP_10.1.12.1_Fan_Direction_Test  tianhe
    [Timeout]  3 min 00 seconds
    [Setup]  boot into diag os mode
    Step  1  check fan direction test  ${FAN_RPM_TOOL}  ${FAN_PRM_OPTION1}  ${interrupt_value2}


BSP_10.1.12.2_FAN_INPUT_TEST
    [Documentation]  This test is to check fan input
    [Tags]  BSP_10.1.12.2_FAN_INPUT_TEST  tianhe
    [Timeout]  10 min 00 seconds
    [Setup]  boot into diag os mode
    Step  1  read FAN input  ${t_system_FAN_input_cmd}
    Step  2  read FAN input  ${diag_FAN_input_cmd}
#    Step  3  compare system and diag FAN input

BSP_10.1.12.3_Fan_Label_Test
    [Documentation]  This test is to check fan label if it is correct
    [Tags]     BSP_10.1.12.3_Fan_Label_Test  tianhe
    [Timeout]  3 min 00 seconds
    [Setup]  boot into diag os mode
    Step  1  verify fan label info  ${device_34_0066_path}  ${fan_label_file_pre}  ${fan_label_file_suf}  ${fan_label_pattern1_pre}  ${fan_label_pattern1_suf}
    Step  2  verify fan label info  ${device_34_0066_path}  ${fan_label_file_pre}  ${fan_label_file_suf}  ${fan_label_pattern2_pre}  ${fan_label_pattern2_suf}  2

BSP_10.1.12.5_Fan_max_Speed_RPM_Test
    [Documentation]  This test is to check each fan max speed setting
    [Tags]     BSP_10.1.12.5_Fan_max_Speed_RPM_Test  tianhe
    [Timeout]  6 min 00 seconds
    [Setup]  boot into diag os mode
    Step  1  check current maximum fan speed  ${FAN_RPM_TOOL}  ${FAN_PRM_OPTION2}  ${FAN_RPM_PATTER1}  ${FAN_RPM_PATTER4}
    Step  2  set maximum fan speed  ${FAN_RPM_TOOL}  ${FAN_PRM_OPTION2}  ${FAN_RPM_PATTER2}
    Step  3  read fan maximum speed  ${FAN_RPM_TOOL}  ${FAN_PRM_OPTION2}  ${FAN_RPM_PATTER2}
	[Teardown]  fan speed set back to default  ${FAN_RPM_TOOL}  ${FAN_PRM_OPTION2}  ${FAN_RPM_PATTER1}  ${FAN_RPM_PATTER4}

BSP_10.1.12.6_Fan_min_Speed_RPM_Test
    [Documentation]  This test is to check each fan min speed setting
    [Tags]     BSP_10.1.12.6_Fan_min_Speed_RPM_Test  tianhe
    [Timeout]  6 min 00 seconds
    [Setup]  boot into diag os mode
    Step  1  read fan maximum speed  ${FAN_RPM_TOOL}  ${FAN_PRM_OPTION3}  ${interrupt_value2}
    Step  2  set maximum fan speed  ${FAN_RPM_TOOL}  ${FAN_PRM_OPTION3}  ${FAN_RPM_PATTER3}
    Step  3  read fan maximum speed  ${FAN_RPM_TOOL}  ${FAN_PRM_OPTION3}  ${FAN_RPM_PATTER3}
	[Teardown]  fan min speed set back to default  ${FAN_RPM_TOOL}  ${FAN_PRM_OPTION3}  ${interrupt_value2}

BSP_10.1.12.8_Fan_board_EEPROM_protect_Test
    [Documentation]  This test is to set the Fan Board eeprom write protect status
    [Tags]     BSP_10.1.12.8_Fan_board_EEPROM_protect_Test  tianhe
    [Timeout]  6 min 00 seconds
    [Setup]  boot into diag os mode
    Step  1  check the fan current protect status  ${FAN_EEPROM_CMD}  ${interrupt_value2}
    Step  2  set and read fan board eeprom protect active or inactive  ${FAN_EEPROM_CMD}  ${interrupt_value1}
    Step  3  write some data into eeprom again  ${FAN_HEX_OPTION}  ${HEX_PATTERN3}  ${HEX_PATTERN4}
    [Teardown]  set and read fan board eeprom protect active or inactive  ${FAN_EEPROM_CMD}  ${interrupt_value2}

BSP_10.1.12.9_Fan_Speed_PWM_test
    [Documentation]  This test is to check that set the fan speed of fan module (0-255)
    [Tags]     BSP_10.1.12.9_Fan_Speed_PWM_test  tianhe
    [Timeout]  6 min 00 seconds
    [Setup]  boot into diag os mode 
    Step  1  stop fcs before test  ${FAN_TOOL}
    Step  2  check fan speed pwm  ${FAN_PWM_TOOL}  ${FAN_255_VALUE}
    Step  3  set fan speed pwm value  ${FAN_PWM_TOOL}  ${FAN_PWM_PATTERN1}
    Step  4  check fan speed pwm  ${FAN_PWM_TOOL}  ${FAN_PWM_PATTERN1}
    Step  5  set fan speed pwm value  ${FAN_PWM_TOOL}  ${FAN_PWM_PATTERN2}
    Step  6  check fan speed pwm  ${FAN_PWM_TOOL}  ${FAN_PWM_PATTERN2}
    Step  7  set fan speed pwm value  ${FAN_PWM_TOOL}  ${FAN_PWM_PATTERN3}
    Step  8  check fan speed pwm  ${FAN_PWM_TOOL}  ${FAN_PWM_PATTERN3}
    Step  9  set fan speed pwm value  ${FAN_PWM_TOOL}  ${FAN_PWM_PATTERN4}
    Step  10  check fan speed pwm  ${FAN_PWM_TOOL}  ${FAN_PWM_PATTERN4}
    Step  11  set fan speed pwm value  ${FAN_PWM_TOOL}  ${FAN_255_VALUE}
    Step  12  check fan speed pwm  ${FAN_PWM_TOOL}  ${FAN_255_VALUE}

BSP_10.1.12.10_FAN_CPLD_RAW_ACCESS_TEST
    [Documentation]  This test is to check fan cpld raw access test
    [Tags]  BSP_10.1.12.10_FAN_CPLD_RAW_ACCESS_TEST  tianhe
    [Timeout]  6 min 00 seconds
    [Setup]  boot into diag os mode
    Step  1  fan cpld read register data  ${FAN_RAW_DATA}  ${FAN_RAW_ADDR}  ${FAN_RAW_PATTERN1}  ${FAN_RAW_PATTERN2}
    Step  2  fan cpld set register data  ${FAN_RAW_ADDR}  ${FAN_RAW_PATTERN3}  ${FAN_RAW_PATTERN2}
    Step  3  fan cpld read register data  ${FAN_RAW_DATA}  ${FAN_RAW_ADDR}  ${FAN_RAW_PATTERN2}  ${FAN_RAW_PATTERN3}
    [Teardown]  restore to original fan raw access value  ${FAN_RAW_DATA}  ${FAN_RAW_ADDR}  ${FAN_RAW_PATTERN1}  ${FAN_RAW_PATTERN2}


BSP_10.1.13_I2C_L-ASC10_DRIVER_TEST
    [Documentation]  This test is to check i2c asc10 driver test
    [Tags]  BSP_10.1.13_I2C_L-ASC10_DRIVER_TEST  tianhe
    [Timeout]  10 min 00 seconds
    [Setup]  boot into diag os mode
    Step  1  read asc10 voltage value  ${LASC10_LST}  ${LASC10_OPTION}  ${LASC10_VALUE_MIN_LST}  ${LASC10_VALUE_MAX_LST}
    Step  2  switch bsp folder path  ${DIAG_PATH}
    Step  3  diagtool check all items  ${DCDC_TOOL}  ${DCDC_ALL_OPTION}


BSP_10.1.14.1_Uboot_boot_log_check
    [Documentation]  This test is to check uboot boot log
    [Tags]     BSP_10.1.14.1_Uboot_boot_log_check  tianhe
    [Timeout]  60 min 00 seconds
    Step  1  check reboot boot log msg  ${check_uboot_log_pattern}


BSP_10.1.14.2_Uboot_Update_Test_via_SPI_Flash
    [Documentation]  This test is to ensure that onie can install by flashcp on onie
    [Tags]  BSP_10.1.14.2_Uboot_Update_Test_via_SPI_Flash  tianhe
    [Timeout]  60 min 00 seconds
    [Setup]   boot into onie rescue mode
    Step  1  if config and ping address   ${ipaddr}
    Step  2  tftp uboot image  ${server_ip}  ${image}
    Step  3  cat dev mtd and erase mtd0
    Step  4  upgrade onie  ${image}
	Step  5  ac power on dut
    Step  6  get onie version


BSP_10.1.14.3_Uboot_Update_Test_via_TFTP
    [Documentation]  This test is to check the U-boot installation
    [Tags]  BSP_10.1.14.3_Uboot_Update_Test_via_TFTP
    [Timeout]  60 min 00 seconds
    [Setup]   boot into Uboot
    Step  1  set ipaddr and server  ${ipaddr}  ${serverip}
    Step  2  run bootupd
    Step  3  check Uboot ver
    Step  4  uboot boot to diagos

BSP_10.1.14.5_UBOOT_MGMT_TFTP_STRESS_TEST
    [Documentation]  This test is to check uboot mgmt tftpp stress test
    [Tags]  BSP_10.1.14.5_UBOOT_MGMT_TFTP_STRESS_TEST  tianhe  stress
    [Timeout]  160 min 00 seconds
    [Setup]  boot into Uboot
    FOR    ${INDEX}    IN RANGE    1    3
        Step  1  mdio read register test  ${MDIO_TOOL}  ${MDIO_OPTION}
        Step  2  download image file in uboot by tftp  ${UBOOT_SERVERIP}  ${UBOOT_STRESS_FILE}  ${UBOOT_ADDRESS}
        Step  3  check_uboot_reset_test  ${UBOOT_RESET_TOOL}
    END
    [Teardown]  power cycle to onie rescue mode

BSP_10.1.14.6_Uboot_environment_Variable_test
    [Documentation]  This test is to check uboot environment variable
    [Tags]     BSP_10.1.14.6_Uboot_environment_Variable_test  tianhe
    [Timeout]  60 min 00 seconds
    [Setup]  boot Into Uboot
    Step  1  set ip address in uboot environment  ${SET_ETH1ADDR_CMD}  ${TEST_ETH1ADDR}  ${SAVE_ENV1}  ${PRINT_ENV}  ${TEST_ETH1DICT}
    Step  2  switch to onie rescue mode  ${ONIE_RESCUE_CMD}  ${ONIE_RESCUE_PATTERN}
    Step  3  check print env test  ${PRINT_ENV2}  ${TEST_ETH1DICT}
    Step  4  add some test para in onie mode  ${FW_SET_ENV}
    Step  5  boot Into Uboot
    Step  6  check test env value  ${PRINT_ENV}  ${TEST_ENV_LST}
    Step  7  reset to default environment  ${ENV_DEF_LST}  ${PRINT_ENV}  ${TEST_PATTERN}
    [Teardown]  boot into onie rescue mode


BSP_10.1.14.7_Uboot_booting_mode_check_test
    [Documentation]  This test is to check Uboot booting mode check test
    [Tags]     BSP_10.1.14.7_Uboot_booting_mode_check_test  tianhe
    [Timeout]  60 min 00 seconds
    Step  1  boot Into Uboot
    Step  2  switch And Check Output  installer
    Step  3  boot Into Uboot
    Step  4  switch And Check Output  update
    Step  5  boot Into Uboot
    Step  6  switch And Check Output  rescue
    Step  7  boot Into Uboot
    Step  8  switch And Check Output  Uninstall
    Step  9  uboot boot to diagos


#BSP_10.1.14.8_Uboot_DHCP_Client_Function_Test
#    [Documentation]  This test is to check Uboot dhcp client function test
#    [Tags]     BSP_10.1.14.8_Uboot_DHCP_Client_Function_Test  tianhe
#    [Timeout]  60 min 00 seconds
#    [Setup]  boot Into Uboot
#    Step  1  uboot set to default  ${ENV_DEF_LST}
#    Step  2  check uboot ip addr  ${PRINT_ENV}  ${PRINT_ENV_OPTION}  ${IPADDR_PATTERN1}
#    Step  3  set dhcp class user by uboot  ${SETENV_TOOL}  ${DHCP_OPTION1}  ${DHCP_OPTION2}
#    Step  4  uboot get ip address from dhcp
#    Step  5  check uboot ip addr  ${PRINT_ENV}  ${PRINT_ENV_OPTION}  ${IPADDR_PATTERN2}
#    Step  6  uboot ping dhcp server  ${server_ipv4}
#    Step  7  download image file in uboot by tftp  ${UBOOT_SERVERIP}  ${UBOOT_STRESS_FILE}
#    [Teardown]  boot into onie rescue mode


BSP_10.2.2.1_ASIC_Reset_Test
    [Documentation]  This test is to check chip reset status
    [Tags]     BSP_10.2.2.1_ASIC_Reset_Test  tianhe
    [Timeout]  3 min 00 seconds
    [Setup]  boot into diag os mode
    Step  1  read asic reset value  ${ASIC_RESET_TOOL}  ${interrupt_value2}
    Step  2  reset and read asic switch chip  ${ASIC_RESET_TOOL}  ${interrupt_value1}

BSP_10.2.2.2_I2C_Reset_Test
    [Documentation]  This test is to check i2c reset
    [Tags]     BSP_10.2.2.2_I2C_Reset_Test  tianhe
    [Timeout]  3 min 00 seconds
    [Setup]  boot into diag os mode
    Step  1  check the current i2c reset status  ${I2C_RESET_TOOL}  ${interrupt_value2}
    Step  2  reset and read i2c test  ${I2C_RESET_TOOL}  ${interrupt_value1}

BSP_10.2.3.1_Fan_board_EEPROM_Test
    [Documentation]  This test is to check Fan board EEPROM
    [Tags]     BSP_10.2.3.1_Fan_board_EEPROM_Test  tianhe
    [Timeout]  6 min 00 seconds
    [Setup]  boot into diag os mode
    Step  1  set and read the fan board eeprom proect  ${FAN_EEPROM_CMD}  ${interrupt_value2}
    Step  2  read fan board eeprom  ${FAN_BOARD_CMD}  ${interrupt_value2}
    Step  3  write some data into fan eeprom  ${FAN_HEX_OPTION}  ${HEX_PATTERN3}
    Step  4  read fan board eeprom  ${FAN_BOARD_CMD}  ${interrupt_value1}
    Step  5  restore origianl data eeprom  ${FAN_HEX_OPTION}
    Step  6  read fan board eeprom  ${FAN_BOARD_CMD}  ${interrupt_value2}
    Step  7  set and read the fan board eeprom proect  ${FAN_EEPROM_CMD}  ${interrupt_value1}
    Step  8  write some data into eeprom again  ${FAN_HEX_OPTION}  ${HEX_PATTERN3}  ${HEX_PATTERN4}

BSP_10.2.3.2_Check_FAN_Module_EEPROM
    [Documentation]  This test is to check FAN Module EEPROM
    [Tags]  BSP_10.2.3.2_Check_FAN_Module_EEPROM  tianhe
    [Timeout]  6 min 00 seconds
    [Setup]  boot into diag os mode
    FOR  ${addr}  IN  @{FAN_ADDR_LST}
        Step  1  read fan module eeprom  ${addr}  ${interrupt_value2}
        Step  2  write some data to fan module eeprom  ${addr}  ${HEX_PATTERN3}
        Step  3  read fan module eeprom  ${addr}  ${interrupt_value1}
        Step  4  restore fan module eeprom data  ${addr}
        Step  5  read fan module eeprom  ${addr}  ${interrupt_value2}
    END

BSP_10.2.3.3_Busbar_Board_EEPROM_Test
    [Documentation]  This test is to check busbar board EEPROM
    [Tags]  BSP_10.2.3.3_Busbar_Board_EEPROM_Test  tianhe
    [Timeout]  6 min 00 seconds
    [Setup]  boot into diag os mode
    Step  1  read busbar board eeprom  ${HEX_TOOL}  ${BUSBAR_TOOL}  ${interrupt_value2}
    Step  2  write some data into fan eeprom  ${BUSBAR_TOOL}  ${HEX_PATTERN3}
    Step  3  read busbar board eeprom  ${HEX_TOOL}  ${BUSBAR_TOOL}  ${interrupt_value1}
    Step  5  restore origianl data eeprom  ${BUSBAR_TOOL}
    Step  6  read busbar board eeprom  ${HEX_TOOL}  ${BUSBAR_TOOL}  ${interrupt_value2}


BSP_10.2.3.4_COMe_Card_EEPROM_Test
    [Documentation]  This test is to check come card EEPROM
    [Tags]  BSP_10.2.3.4_COMe_Card_EEPROM_Test  tianhe
    [Timeout]  6 min 00 seconds
    [Setup]  boot into diag os mode
    Step  1  check come write protect  ${COME_EEPROM_TOOL}  ${interrupt_value2}
    Step  2  read come card eeprom  ${HEX_TOOL}  ${COME_BUS_TOOL}  ${HEX_PATTERN1}
    Step  3  write some data into eeprom  ${COME_BUS_TOOL}  ${HEX_PATTERN3}
    Step  4  read back the eeprom data  ${HEX_TOOL}  ${COME_BUS_TOOL}  ${HEX_PATTERN2}
    Step  5  restore come card original data  ${COME_BUS_TOOL}
    Step  6  read come card eeprom  ${HEX_TOOL}  ${COME_BUS_TOOL}  ${HEX_PATTERN1}
    Step  7  enable or disable come card write protect  ${COME_EEPROM_TOOL}  ${interrupt_value1}
    Step  8  write some data into eeprom again  ${COME_BUS_TOOL}  ${HEX_PATTERN3}  ${HEX_PATTERN4}
    Step  9  read come card eeprom  ${HEX_TOOL}  ${COME_BUS_TOOL}  ${HEX_PATTERN1}
    Step  10  enable or disable come card write protect  ${COME_EEPROM_TOOL}  ${interrupt_value2}


BSP_10.2.3.5_Riser_board_eerpom_test
    [Documentation]  This test is to check riser board eerpom test
    [Tags]     BSP_10.2.3.5_Riser_board_eerpom_test  tianhe
    [Timeout]  60 min 00 seconds
    Step  1  read riser board eerpom test  ${HEX_TOOL}  ${RISER_EEPROM_TOOL}  ${interrupt_value2}
    Step  2  write some data to riser board eeprom  ${RISER_EEPROM_TOOL}  ${HEX_PATTERN3}
    Step  3  read riser board eerpom test  ${HEX_TOOL}  ${RISER_EEPROM_TOOL}  ${interrupt_value1}
    Step  4  restore origianl data eeprom  ${RISER_EEPROM_TOOL}
    Step  5  read riser board eerpom test  ${HEX_TOOL}  ${RISER_EEPROM_TOOL}  ${interrupt_value2}


BSP_10.2.4.1_Fan_eeprom_Power_Status_Test
    [Documentation]  This test is to read and set  Fan eeprom power status
    [Tags]  BSP_10.2.4.1_Fan_eeprom_Power_Status_Test  tianhe
    [Timeout]  6 min 00 seconds
    [Setup]  boot into diag os mode
    Step  1  read fan eeprom power status  ${FAN_POWER_TOOL}  ${interrupt_value1}
    Step  2  set the fan eeprom power enable or disable  ${FAN_POWER_TOOL}  ${interrupt_value2}
    Step  3  read fan eeprom power status  ${FAN_POWER_TOOL}  ${interrupt_value2}
    Step  4  set the fan eeprom power enable or disable  ${FAN_POWER_TOOL}  ${interrupt_value1}
    Step  5  read fan eeprom power status  ${FAN_POWER_TOOL}  ${interrupt_value1}


BSP_10.2.4.2_I2C_Fan_MUX_Reset_Test
    [Documentation]  This test is to reset I2C fan mux
    [Tags]  BSP_10.2.4.2_I2C_Fan_MUX_Reset_Test  tianhe
    [Timeout]  6 min 00 seconds
    [Setup]  boot into diag os mode
    Step  1  read fan mux reset value  ${FAN_MUX_TOOL}  ${interrupt_value2}
    Step  2  reset fan mux status  ${FAN_MUX_TOOL}  ${interrupt_value1}
    Step  3  read fan mux reset value  ${FAN_MUX_TOOL}  ${interrupt_value1}
    Step  4  reset fan mux status  ${FAN_MUX_TOOL}  ${interrupt_value2}
    Step  5  read fan mux reset value  ${FAN_MUX_TOOL}  ${interrupt_value2}


BSP_10.2.5.1_CPLD2_3_RAW_ACCESS_TEST
    [Documentation]  This test is to check cpld2_3 raw access test
    [Tags]  BSP_10.2.5.1_CPLD2_3_RAW_ACCESS_TEST  tianhe
    [Timeout]  6 min 00 seconds
    [Setup]  boot into diag os mode
    Step  1  read cpld raw access test  ${CPLD2_RAW_ADDR}  ${CPLD2_RAW_DATA}  ${CPLD2_RAW_PATTERN1}  ${CPLD2_RAW_PATTERN2}
    Step  2  write cpld raw access test  ${CPLD2_RAW_ADDR}  ${CPLD2_RAW_DATA}  ${CPLD_RAW_pattern1}  ${CPLD_RAW_pattern2}
    Step  3  read cpld raw access test  ${CPLD2_RAW_ADDR}  ${CPLD2_RAW_DATA}  ${CPLD_RAW_pattern1}  ${CPLD_RAW_pattern2}
    Step  4  read cpld raw access test  ${CPLD3_RAW_ADDR}  ${CPLD3_RAW_DATA}  ${CPLD2_RAW_PATTERN1}  ${CPLD3_RAW_PATTERN1}
    Step  5  write cpld raw access test  ${CPLD3_RAW_ADDR}  ${CPLD3_RAW_DATA}  ${CPLD_RAW_pattern1}  ${CPLD_RAW_pattern2}
    Step  6  read cpld raw access test  ${CPLD3_RAW_ADDR}  ${CPLD3_RAW_DATA}  ${CPLD_RAW_pattern1}  ${CPLD_RAW_pattern2}
    [Teardown]  restore to default cpld raw value


BSP_10.2.5.2_LED_ENABLE_TEST
    [Documentation]  This test is to check cpld2_3 led enable test
    [Tags]  BSP_10.2.5.2_LED_ENABLE_TEST  tianhe
    [Timeout]  6 min 00 seconds
    [Setup]  boot into diag os mode
    Step  1  check cpld led enable status  ${CPLD2_LED_TOOL}  ${CPLD3_LED_TOOL}  ${interrupt_value2}
    Step  2  set cpld led enable test  ${CPLD2_LED_TOOL}  ${CPLD3_LED_TOOL}  ${interrupt_value1}
    Step  3  check cpld led enable status  ${CPLD2_LED_TOOL}  ${CPLD3_LED_TOOL}  ${interrupt_value1}
    [Teardown]  restore to default cpld led value  ${CPLD2_LED_TOOL}  ${CPLD3_LED_TOOL}  ${interrupt_value2}

	
#BSP_10.2.5.3_LED_COLOR_TEST
#    [Documentation]  This test is to check cpld2_3 led color test
#    [Tags]  BSP_10.2.5.3_LED_COLOR_TEST  tianhe
#    [Timeout]  6 min 00 seconds
#    [Setup]  boot into diag os mode
#    Step  1  check port led status  ${CPLD2_LED_COLOR}  ${CPLD3_LED_COLOR}  ${LED_COLOR_DEFAULT}
#    Step  2  set and read port led color  ${CPLD2_LED_COLOR}  ${CPLD3_LED_COLOR}  ${LED_COLOR_RED}
#    Step  3  set and read port led color  ${CPLD2_LED_COLOR}  ${CPLD3_LED_COLOR}  ${LED_COLOR_GREEN}
#    Step  4  set and read port led color  ${CPLD2_LED_COLOR}  ${CPLD3_LED_COLOR}  ${LED_COLOR_WHITE}
#    Step  5  set and read port led color  ${CPLD2_LED_COLOR}  ${CPLD3_LED_COLOR}  ${LED_COLOR_BLUE}
#    Step  6  set and read port led color  ${CPLD2_LED_COLOR}  ${CPLD3_LED_COLOR}  ${LED_COLOR_DEFAULT}


BSP_10.2.6_LM75_DRIVER_TEST
    [Documentation]  This test is to check lm75 driver test
    [Tags]  BSP_10.2.6_LM75_DRIVER_TEST  tianhe
    [Timeout]  6 min 00 seconds
    [Setup]  boot into diag os mode
    Step  1  read left side of the switch board tas voltage  ${LM75_TOOL}  ${LM75_SENSOR_ADDR[0]}  ${HWMON_LST[0]}  ${LM75_OPTION_LST}
    Step  2  read left side of the switch board bas voltage  ${LM75_TOOL}  ${LM75_SENSOR_ADDR[1]}  ${HWMON_LST[1]}  ${LM75_OPTION_LST}
    Step  3  read right side of the switch board tas voltage  ${LM75_TOOL}  ${LM75_SENSOR_ADDR[2]}  ${HWMON_LST[2]}  ${LM75_OPTION_LST}
    Step  4  read middle side of the switch board tas voltage  ${LM75_TOOL}  ${LM75_SENSOR_ADDR[3]}  ${HWMON_LST[3]}  ${LM75_OPTION_LST}
    Step  5  read right side of the switch board bas voltage  ${LM75_TOOL}  ${LM75_SENSOR_ADDR[4]}  ${HWMON_LST[4]}  ${LM75_OPTION_LST}
    Step  6  read middle side of fan board voltage  ${LM75_TOOL}  ${LM75_SENSOR_ADDR[5]}  ${HWMON_LST[5]}  ${LM75_OPTION_LST}
    Step  7  read right side of fan board voltage  ${LM75_TOOL}  ${LM75_SENSOR_ADDR[6]}  ${HWMON_LST[6]}  ${LM75_OPTION_LST}
    Step  8  read left side of fan board voltage  ${LM75_TOOL}  ${LM75_SENSOR_ADDR[7]}  ${HWMON_LST[7]}  ${LM75_OPTION_LST}


BSP_10.2.7_I2C_SA5604_DRIVER_TEST
    [Documentation]  This test is to read i2c sa5604 sensor driver test
    [Tags]  BSP_10.2.7_I2C_SA5604_DRIVER_TEST  tianhe
    [Timeout]  60 min 00 seconds
    [Setup]  boot into diag os mode
    Step  1  read sa5604 temperature info  ${LM90_TOOL}  ${LM90_SENSOR_ADDR[0]}  ${HWMON_LST[8]}  ${LM90_OPTION_LST}
    Step  2  read sa5604 temperature info  ${LM90_TOOL}  ${LM90_SENSOR_ADDR[1]}  ${HWMON_LST[9]}  ${LM90_OPTION_LST}


BSP_10.2.8.1_I2C_LTC4282_DRIVER_TEST
    [Documentation]  This test is to read i2c ltc4282 driver test
    [Tags]  BSP_10.2.8.1_I2C_LTC4282_DRIVER_TEST  tianhe
    [Timeout]  60 min 00 seconds
    [Setup]  boot into diag os mode
    Step  1  read ltc4282 voltage test  ${LTC_TOOL}  ${LTC_ADDR}  ${HWMON_LST[10]}  ${LTC_OPTION_LST}


BSP_10.2.9.1_TPS53679_DRIVER_TEST
    [Documentation]  this test is to check tps53679 driver test
    [Tags]     BSP_10.2.9.1_TPS53679_DRIVER_TEST  tianhe
    [Timeout]  10 min 00 seconds
    [Setup]  boot into diag os mode
    Step  1  check tps53679 driver value test  ${TPS_TOOL}  ${TPS_ADDR[0]}  ${HWMON_LST[11]}  ${TPS_OPTION_LST}
    Step  2  check tps53679 driver value test  ${TPS_TOOL}  ${TPS_ADDR[1]}  ${HWMON_LST[12]}  ${IN_LABEL_LST}
    Step  3  check tps53679 driver value test  ${TPS_TOOL}  ${TPS_ADDR[2]}  ${HWMON_LST[13]}  ${IN_MIN_LST}


BSP_10.2.9.2_TPS53679_DCDC_Controller_Driver_Test
    [Documentation]  this test is to check tps53679 dcdc driver test
    [Tags]     BSP_10.2.9.2_TPS53679_DCDC_Controller_Driver_Test  tianhe
    [Timeout]  1 min 00 seconds
    [Setup]  boot into diag os mode
    Step  1  check tps53679 driver value test  ${TPS_TOOL}  ${TPS_ADDR[3]}  ${HWMON_LST[14]}  ${DCDC_OPTION_LST}


BSP_10.2.10.1.1_COMe_CPLD_Version_Test
    [Documentation]  This test is to check come cpld version test.
    [Tags]  BSP_10.2.10.1.1_COMe_CPLD_Version_Test  tianhe
    [Timeout]  60 min 00 seconds
    [Setup]  boot into diag os mode
    Step  1  check come cpld version  ${COMe_CPLD_TOOL}  ${COMe_NEW_VER}


BSP_10.2.10.1.2_COMe_Board_Version_Test
    [Documentation]  This test is to check come board version test.
    [Tags]  BSP_10.2.10.1.2_COMe_Board_Version_Test  tianhe
    [Timeout]  60 min 00 seconds
    [Setup]  boot into diag os mode
    Step  1  check come cpld version  ${Board_VER_TOOL}  ${Board_NEW_VER}


BSP_10.2.10.1.3_COMe_CPLD_Raw_Access_Test
    [Documentation]  This test is to check come cpld raw access test.
    [Tags]  BSP_10.2.10.1.3_COMe_CPLD_Raw_Access_Test  tianhe
    [Timeout]  60 min 00 seconds
    [Setup]  boot into diag os mode
    Step  1  check page select value  ${PAGE_SELECT_TOOL}  ${interrupt_value1}  ${CPLD_RAW_pattern1}
    Step  2  read access sysfs note test  ${PAGE_ADDR}  ${PAGE_DATA}  ${CPLD2_RAW_PATTERN1}
    Step  3  write access sysfs note test  ${PAGE_ADDR}  ${PAGE_DATA}  ${PAGE_OPTION}  ${CPLD_RAW_pattern2}
    Step  4  read access sysfs note test again  ${PAGE_ADDR}  ${PAGE_DATA}  ${PAGE_OPTION}  ${CPLD_RAW_pattern2}
    [Teardown]  restore to default come cpld raw value  ${PAGE_SELECT_TOOL}  ${PAGE_ADDR}  ${PAGE_DATA}  ${CPLD2_RAW_PATTERN1}


BSP_10.2.10.2.1_Hreset_Test
    [Documentation]  This test is to check hreset test.
    [Tags]  BSP_10.2.10.2.1_Hreset_Test  tianhe
    [Timeout]  60 min 00 seconds
    [Setup]  boot into diag os mode
    Step  1  read hreset value  ${HRESET_TOOL}  ${interrupt_value1}
    Step  2  write hreset value test  ${HRESET_TOOL}  ${interrupt_value2}
    Step  3  read hreset value  ${HRESET_TOOL}  ${interrupt_value1}
#    [Teardown]  restore to default hreset value  ${HRESET_TOOL}  ${interrupt_value1}

BSP_10.2.10.2.2_Poreset_Test
    [Documentation]  this test is to check poreset test
    [Tags]     BSP_10.2.10.2.2_Poreset_Test  tianhe
    [Timeout]  10 min 00 seconds
    [Setup]  boot into diag os mode
    Step  1  read poreset value test  ${PORESET_TOOL}  ${interrupt_value1}
    Step  2  write poreset value test  ${PORESET_TOOL}  ${interrupt_value2}
    Step  3  read poreset value test  ${PORESET_TOOL}  ${interrupt_value1}

BSP_10.2.10.3.1_Come_Watchdog_Enable_Test
    [Documentation]  this test is to check come watchdog enable test
    [Tags]     BSP_10.2.10.3.1_Come_Watchdog_Enable_Test  tianhe
    [Timeout]  10 min 00 seconds
    [Setup]  boot into diag os mode
    Step  1  check the come watchdog status  ${COME_WATCHDOG_TOOL}  ${interrupt_value2}
    Step  2  write and read the come watchdog status  ${COME_WATCHDOG_TOOL}  ${interrupt_value1}
    Step  3  write and read the come watchdog status  ${COME_WATCHDOG_TOOL}  ${interrupt_value2}

BSP_10.2.10.3.2_Come_Watchdog_Seconds_Test
    [Documentation]  this test is to check come watchdog seconds test
    [Tags]     BSP_10.2.10.3.2_Come_Watchdog_Seconds_Test  tianhe
    [Timeout]  10 min 00 seconds
    [Setup]  boot into diag os mode
    Step  1  set and read come watchdog trigger time  ${COME_WATCHDOG_SEC_TOOL}  ${TRIGGER_10_TIME}
    Step  2  enable come watchdog test  ${COME_WATCHDOG_ENABLE_TOOL}  ${interrupt_value1}

BSP_10.2.10.4_Come_Fault_Logger_Test
    [Documentation]  this test is to check come fault logger test
    [Tags]     BSP_10.2.10.4_Come_Fault_Logger_Test  tianhe
    [Timeout]  10 min 00 seconds
    [Setup]  boot into diag os mode
    Step  1  check come fault logger test  ${COME_CPLD_PATH}  ${LOGGER_DUMP_TOOL}  ${RESET_LOGGER}  ${PAUSE_LOGGER}

BSP_10.2.11_I2C_MCP3422_ADC_Driver_Test
    [Documentation]  this test is to check i2c mcp3422 adc drive
    [Tags]     BSP_10.2.11_I2C_MCP3422_ADC_Driver_Test  tianhe
    [Timeout]  1 min 00 seconds
    [Setup]  boot into diag os mode
    Step  1  read mcp3422 voltage value  ${VOLTAGE_RAW}
    Step  2  read mcp3422 voltage value  ${VOLTAGE_SCALE}
    Step  3  read mcp3422 voltage value  ${VOLTAGE_FREQ}
    Step  4  read mcp3422 voltage value  ${VOLTAGE_AVAIL}
    Step  5  read mcp3422 voltage value  ${VOLTAGE_FREQ_AVAIL}

BSP_10.2.12.1_I2cfpga_Present_Test
    [Documentation]  this test is to check i2cfpga present
    [Tags]     BSP_10.2.12.1_I2cfpga_Present_Test  tianhe
    [Timeout]  1 min 00 seconds
    [Setup]  boot into diag os mode
    Step  1  check the i2cfpga card present status  ${I2CFPGA_PRE}  ${interrupt_value1}

#BSP_10.2.12.2_I2cfpga_Eeprom_Protect_Test
#    [Documentation]  this test is to check i2cfpga eeprom protect
#    [Tags]     BSP_10.2.12.2_I2cfpga_Eeprom_Protect_Test  tianhe
#    [Timeout]  10 min 00 seconds
#    [Setup]  boot into diag os mode
#    Step  1  check i2c fpga card eeprom write protect status  ${I2CFPGA_WRITE_PROTECT}  ${interrupt_value1}
#    Step  2  set the i2c fpga card eeprom write protect  ${I2CFPGA_WRITE_PROTECT}  ${interrupt_value2}
#    Step  3  check i2c fpga card eeprom write protect status  ${I2CFPGA_WRITE_PROTECT}  ${interrupt_value2}
#    Step  4  set the i2c fpga card eeprom write protect  ${I2CFPGA_WRITE_PROTECT}  ${interrupt_value1}
#    Step  5  check i2c fpga card eeprom write protect status  ${I2CFPGA_WRITE_PROTECT}  ${interrupt_value1}
#    Step  6  write data to i2c fpga card eeprom  ${I2CFPGA_EEPROM_TOOL}  ${HEX_PATTERN3}

BSP_10.2.12.3_I2cfpga_LM75_Interrupt_Test
    [Documentation]  this test is to check i2cfpga LM75 interrupt test
    [Tags]     BSP_10.2.12.3_I2cfpga_LM75_Interrupt_Test  tianhe
    [Timeout]  1 min 00 seconds
    [Setup]  boot into diag os mode
    Step  1  check the lm75 interrupt status  ${I2CFPGA_LM75_TOOL}  ${interrupt_value2}

BSP_10.2.14.1.1_1PPS-I2C-FPGA_Version_Test
    [Documentation]  this test is to check 1pps i2c fpga version test
    [Tags]     BSP_10.2.14.1.1_1PPS-I2C-FPGA_Version_Test  tianhe
    [Timeout]  1 min 00 seconds
    [Setup]  boot into diag os mode
    Step  1  check 1pps fpga version  ${PPS_VER_TOOL}  ${fpagImge}

BSP_10.2.14.1.2_1PPS-I2C-FPGA_Board_Version_Test
    [Documentation]  this test is to check 1pps i2c fpga board version test
    [Tags]     BSP_10.2.14.1.2_1PPS-I2C-FPGA_Board_Version_Test  tianhe
    [Timeout]  1 min 00 seconds
    [Setup]  boot into diag os mode
    Step  1  check 1pps fpga version  ${PPS_BORAD_VER_TOOL}  FPGA_Board_Version

BSP_10.2.14.1.3_1PPS-I2C-FPGA_PCB_Version_Test
    [Documentation]  this test is to check 1pps i2c fpga board version test
    [Tags]     BSP_10.2.14.1.3_1PPS-I2C-FPGA_PCB_Version_Test  tianhe
    [Timeout]  1 min 00 seconds
    [Setup]  boot into diag os mode
    Step  1  check 1pps fpga version  ${PCB_VER_TOOL}  PCB_version

BSP_10.2.14.1.4_1PPS-I2C-FPGA_Image_Version_Test
    [Documentation]  this test is to check 1pps i2c fpga image version test
    [Tags]     BSP_10.2.14.1.4_1PPS-I2C-FPGA_Image_Version_Test  tianhe
    [Timeout]  10 min 00 seconds
    [Setup]  boot into diag os mode
    Step  1  check 1pps fpga version  ${I2C_VER_TOOL}  I2C_FPGA

BSP_10.2.14.1.5_1PPS-I2C_Raw_Access_Test
    [Documentation]  this test is to check 1pps i2c raw access test
    [Tags]     BSP_10.2.14.1.5_1PPS-I2C_Raw_Access_Test  tianhe
    [Timeout]  10 min 00 seconds
    [Setup]  boot into diag os mode
    Step  1  read i2c raw access test  ${I2C_RAW_ACCESS_DATA}  ${I2C_RAW_ACCESS_ADDR}  ${I2C_RAW_PATTERN1}  ${I2C_RAW_PATTERN2}
    Step  2  write i2c raw access test  ${I2C_RAW_ACCESS_DATA}  ${I2C_RAW_ACCESS_ADDR}  ${I2C_WRITE_DATA1}  ${I2C_WRITE_DATA2}
    Step  3  read i2c raw access test  ${I2C_RAW_ACCESS_DATA}  ${I2C_RAW_ACCESS_ADDR}  ${I2C_RAW_PATTERN3}  ${I2C_RAW_PATTERN4}
    [Teardown]  restore to default i2c raw value

BSP_10.2.14.1.6_1PPS-I2C_Scratch_Test
    [Documentation]  this test is to check 1pps i2c scratch test
    [Tags]     BSP_10.2.14.1.6_1PPS-I2C_Scratch_Test  tianhe
    [Timeout]  10 min 00 seconds
    [Setup]  boot into diag os mode
    Step  1  read i2c scratch test  ${I2C_SCRATCH_TOOL}  ${I2C_RAW_PATTERN2}
    Step  2  write i2c scratch test  ${I2C_SCRATCH_TOOL}  ${I2C_SCRATCH_PATTERN}
    Step  3  read i2c scratch test  ${I2C_SCRATCH_TOOL}  ${I2C_SCRATCH_PATTERN}
    [Teardown]  restore to default i2c scratch value  ${I2C_SCRATCH_TOOL}  ${I2C_RAW_PATTERN2}

BSP_10.2.14.2.1_Port_I2C_Profile_Select_Test
    [Documentation]  this test is to check port i2c profile select test
    [Tags]     BSP_10.2.14.2.1_Port_I2C_Profile_Select_Test  tianhe
    [Timeout]  10 min 00 seconds
    [Setup]  boot into diag os mode
    Step  1  read the current profile select  ${PORT_PROFILE_TOOL}  ${PORT_PROFILE_OPTION}  ${interrupt_value1}
    Step  2  set the profile select  ${PORT_PROFILE_TOOL}  ${PORT_PROFILE_OPTION}  ${PORT_PROFILE_PATTERN}
    Step  3  read the current profile select  ${PORT_PROFILE_TOOL}  ${PORT_PROFILE_OPTION}  ${PORT_PROFILE_PATTERN}
    [Teardown]  restore to default i2c profile select value  ${PORT_PROFILE_TOOL}  ${PORT_PROFILE_OPTION}  ${interrupt_value1}

BSP_10.2.14.2.2_Port_I2C_Profile_Speed_Test
    [Documentation]  this test is to check port i2c profile speed test
    [Tags]     BSP_10.2.14.2.2_Port_I2C_Profile_Speed_Test  tianhe
    [Timeout]  10 min 00 seconds
    [Setup]  boot into diag os mode
    Step  1  set the profile speed  ${PORT_PROFILE_TOOL}  ${PORT_SPEED_OPTION1}  ${PORT_SPEED_OPTION2}  ${SPEED_PATTERN1}
    Step  2  read the profile speed  ${PORT_PROFILE_TOOL}  ${PORT_SPEED_OPTION1}  ${PORT_SPEED_OPTION2}  ${SPEED_PATTERN1}
    Step  3  set the profile speed  ${PORT_PROFILE_TOOL}  ${PORT_SPEED_OPTION1}  ${PORT_SPEED_OPTION2}  ${SPEED_PATTERN2}
    Step  4  read the profile speed  ${PORT_PROFILE_TOOL}  ${PORT_SPEED_OPTION1}  ${PORT_SPEED_OPTION2}  ${SPEED_PATTERN2}
    Step  5  set the profile speed  ${PORT_PROFILE_TOOL}  ${PORT_SPEED_OPTION1}  ${PORT_SPEED_OPTION2}  ${SPEED_PATTERN3}
    Step  6  read the profile speed  ${PORT_PROFILE_TOOL}  ${PORT_SPEED_OPTION1}  ${PORT_SPEED_OPTION2}  ${SPEED_PATTERN3}

BSP_10.2.14.2.3_Port_I2C_9_clock_Test
    [Documentation]  this test is to check port i2c 9 colck test
    [Tags]     BSP_10.2.14.2.3_Port_I2C_9_clock_Test  tianhe
    [Timeout]  10 min 00 seconds
    [Setup]  boot into diag os mode
    Step  1  set the i2c clock speed  ${PORT_PROFILE_TOOL}  ${I2C_CLOCK_OPTION}  ${interrupt_value1}

BSP_10.2.14.2.4_Port_I2C_Master_Reset_Test
    [Documentation]  this test is to check port i2c master reset test
    [Tags]     BSP_10.2.14.2.4_Port_I2C_Master_Reset_Test  tianhe
    [Timeout]  10 min 00 seconds
    [Setup]  boot into diag os mode
    Step  1  read the i2c master reset test  ${PORT_PROFILE_TOOL}  ${I2C_MASTER_OPTION}  ${interrupt_value2}
    Step  2  set the i2c master reset test  ${PORT_PROFILE_TOOL}  ${I2C_MASTER_OPTION}  ${interrupt_value1}
    Step  3  read the i2c master reset test  ${PORT_PROFILE_TOOL}  ${I2C_MASTER_OPTION}  ${interrupt_value2}

BSP_10.2.14.3.1_Port_Module_Interrupt_Mask_Test
    [Documentation]  this test is to check port module interrupt mask test
    [Tags]     BSP_10.2.14.3.1_Port_Module_Interrupt_Mask_Test  tianhe
    [Timeout]  10 min 00 seconds
    [Setup]  boot into diag os mode
    Step  1  read the port interrupt mask test  ${PORT_PROFILE_TOOL}  ${PORT_MASK_OPTION}  ${interrupt_value2}
    Step  2  set the port interrupt mask test  ${PORT_PROFILE_TOOL}  ${PORT_MASK_OPTION}  ${interrupt_value1}
    Step  3  read the port interrupt mask test  ${PORT_PROFILE_TOOL}  ${PORT_MASK_OPTION}  ${interrupt_value1}
    [Teardown]  restore to default port interrupt mask test  ${PORT_PROFILE_TOOL}  ${PORT_MASK_OPTION}  ${interrupt_value2}

BSP_10.2.14.3.2_Port_Module_Lpmod_Test
    [Documentation]  this test is to check port module lpmod test
    [Tags]     BSP_10.2.14.3.2_Port_Module_Lpmod_Test  tianhe
    [Timeout]  10 min 00 seconds
    [Setup]  boot into diag os mode
    Step  1  read the port lpmod test  ${PORT_PROFILE_TOOL}  ${PORT_LPMOD_OPTION}  ${interrupt_value2}
    Step  2  set the port lpmod test  ${PORT_PROFILE_TOOL}  ${PORT_LPMOD_OPTION}  ${interrupt_value1}
    Step  3  read the port lpmod test  ${PORT_PROFILE_TOOL}  ${PORT_LPMOD_OPTION}  ${interrupt_value1}
    [Teardown]  restore to default port lpmod test  ${PORT_PROFILE_TOOL}  ${PORT_LPMOD_OPTION}  ${interrupt_value2}

BSP_10.2.15_Rsense_Config_From_Device_Tree_Test
    [Documentation]  this test is to check Rsense config from device tree test
    [Tags]     BSP_10.2.15_Rsense_Config_From_Device_Tree_Test  tianhe
    [Timeout]  10 min 00 seconds
    [Setup]  boot into diag os mode
    Step  1  check the rsense value test  ${RSENSE_TREE_TOOL}  ${RSENSE_TREE_PATTERN}

BSP_10.2.16_ASC10_EEPROM_And_CRC_Sysfs_Node_Test
    [Documentation]  this test is to check asc10 eeprom and crc sysfs node test
    [Tags]     BSP_10.2.16_ASC10_EEPROM_And_CRC_Sysfs_Node_Test  tianhe
    [Timeout]  10 min 00 seconds
    [Setup]  boot into diag os mode
    Step  1  check asc10 eeprom and crc test  ${ASC10_TOOL_LST}  ${ASC10_EEPROM_LST}  ${ASC10_CRC_LST}


BSP_10.2.17.1_Conn_Type_Test
    [Documentation]  this test is to check conn type test
    [Tags]     BSP_10.2.17.1_Conn_Type_Test  tianhe
    [Timeout]  10 min 00 seconds
    [Setup]  boot into diag os mode
    Step  1  check the type of connector  ${CONN_TOOL}  ${CONN_OPTION}  ${CONN_PATTERN}  Conn_Type

BSP_10.2.17.2_EEPROM_Lower_Check_Test
    [Documentation]  this test is to check eeprom lower test
    [Tags]     BSP_10.2.17.2_EEPROM_Lower_Check_Test  tianhe
    [Timeout]  10 min 00 seconds
    [Setup]  boot into diag os mode
    Step  1  check raw eeprom on the lower 128 bytes  ${CONN_TOOL}  ${EEPROM_LOWER_OPTION}  ${EEPROM_LOWER_PATTERN}  EEPROM_Lower


BSP_10.2.17.3_EEPROM_Upper_Check_Test
    [Documentation]  this test is to check eeprom Upper test
    [Tags]     BSP_10.2.17.3_EEPROM_Upper_Check_Test  tianhe
    [Timeout]  10 min 00 seconds
    [Setup]  boot into diag os mode
    Step  1  check raw eeprom on the upper 128 bytes  ${CONN_TOOL}  ${EEPROM_UPPER_OPTION}  ${EEPROM_UPPER_PATTERN}  EEPROM_Upper

BSP_10.2.17.4_EEPROM_Upper_Page_Select_Check
    [Documentation]  this test is to check eeprom Upper page select test
    [Tags]     BSP_10.2.17.4_EEPROM_Upper_Page_Select_Check  tianhe
    [Timeout]  10 min 00 seconds
    [Setup]  boot into diag os mode
    Step  1  read visible page number  ${CONN_TOOL}  ${EEPROM_UP_PAGE_OPTION}  ${interrupt_value2}  Visible_Page
    Step  2  set visible page number  ${CONN_TOOL}  ${EEPROM_UP_PAGE_OPTION}  ${PORT_PROFILE_PATTERN}
    Step  3  read visible page number  ${CONN_TOOL}  ${EEPROM_UP_PAGE_OPTION}  ${PORT_PROFILE_PATTERN}  Visible_Page
    [Teardown]  restore to default visible page number test  ${CONN_TOOL}  ${EEPROM_UP_PAGE_OPTION}  ${interrupt_value2}  Visible_Page


BSP_10.2.17.5_EEPROM_Valid_Check
    [Documentation]  this test is to check eeprom valid test
    [Tags]     BSP_10.2.17.5_EEPROM_Valid_Check  tianhe
    [Timeout]  10 min 00 seconds
    [Setup]  boot into diag os mode
    Step  1  read eeprom valid test  ${CONN_TOOL}  ${EEPROM_VALID_OPTION}  ${interrupt_value1}  EEPROM_Valid

BSP_10.2.17.6_High_Power_Class_Enable_Check
    [Documentation]  this test is to check high power class enable test
    [Tags]     BSP_10.2.17.6_High_Power_Class_Enable_Check  tianhe
    [Timeout]  10 min 00 seconds
    [Setup]  boot into diag os mode
    Step  1  read high power class enable  ${CONN_TOOL}  ${HIGH_POWER_OPTION}  ${interrupt_value2}  High_Power
    Step  2  set high power class enable  ${CONN_TOOL}  ${HIGH_POWER_OPTION}  ${interrupt_value1}
    Step  3  read high power class enable  ${CONN_TOOL}  ${HIGH_POWER_OPTION}  ${interrupt_value2}  High_Power

BSP_10.2.17.7_In1_Highest_Check
    [Documentation]  this test is to check In1 Highest check
    [Tags]     BSP_10.2.17.7_In1_Highest_Check  tianhe
    [Timeout]  10 min 00 seconds
    [Setup]  boot into diag os mode
    Step  1  read in1 highest test  ${CONN_TOOL}  ${IN1_OPTION}  ${INI_PATTERN}  In1_Highest

BSP_10.2.17.8_In1_Input_Check
    [Documentation]  this test is to check In1 input check
    [Tags]     BSP_10.2.17.8_In1_Input_Check  tianhe
    [Timeout]  10 min 00 seconds
    [Setup]  boot into diag os mode
    Step  1  read in1 input test  ${CONN_TOOL}  ${IN1_INPUT_OPTION}  ${INI_PATTERN}  In1_Input


BSP_10.2.17.9_In1_Lowest_Check
    [Documentation]  this test is to check In1 lowest check
    [Tags]     BSP_10.2.17.9_In1_Lowest_Check  tianhe
    [Timeout]  10 min 00 seconds
    [Setup]  boot into diag os mode
    Step  1  read in1 lowest test  ${CONN_TOOL}  ${IN1_LOWEST_OPTION}  ${INI_PATTERN}  In1_Lowest

BSP_10.2.17.10_In1_Max_Check
    [Documentation]  this test is to check In1 Max check
    [Tags]     BSP_10.2.17.10_In1_Max_Check  tianhe
    [Timeout]  10 min 00 seconds
    [Setup]  boot into diag os mode
    Step  1  read in1 max test  ${CONN_TOOL}  ${IN1_MAX_OPTION}  ${IN1_MAX_PATTERN}  In1_Max


BSP_10.2.17.11_In1_Min_Check
    [Documentation]  this test is to check In1 Min check
    [Tags]     BSP_10.2.17.11_In1_Min_Check  tianhe
    [Timeout]  10 min 00 seconds
    [Setup]  boot into diag os mode
    Step  1  read in1 min test  ${CONN_TOOL}  ${IN1_MIN_OPTION}  ${IN1_MIN_PATTERN}  In1_Min

BSP_10.2.17.12_In1_Reset_History_Check
    [Documentation]  this test is to check In1 reset history check
    [Tags]     BSP_10.2.17.12_In1_Reset_History_Check  tianhe
    [Timeout]  10 min 00 seconds
    [Setup]  boot into diag os mode
    Step  1  set in1 reset history test  ${CONN_TOOL}  ${IN1_HISTORY_OPTION}  ${interrupt_value1}

BSP_10.2.17.13_Lane_Ctle_Check
    [Documentation]  this test is to check lane ctle test
    [Tags]     BSP_10.2.17.13_Lane_Ctle_Check  tianhe
    [Timeout]  10 min 00 seconds
    [Setup]  boot into diag os mode
    Step  1  read lane ctle test  ${CONN_TOOL}  ${LANE_CTLE_OPTION}  ${interrupt_value2}  ${LANE_CTLE_PATTERN}  Lane_Ctle

BSP_10.2.17.14_Lane_rx-or-tx_Los_Check
    [Documentation]  this test is to check lane rx or tx los
    [Tags]     BSP_10.2.17.14_Lane_rx-or-tx_Los_Check  tianhe
    [Timeout]  10 min 00 seconds
    [Setup]  boot into diag os mode
    Step  1  read lane rx and tx los test  ${CONN_TOOL}  ${RX_LOS_OPTION}  rx-or-tx_Los
    Step  2  read lane rx and tx los test  ${CONN_TOOL}  ${TX_LOS_OPTION}  rx-or-tx_Los

BSP_10.2.17.15_Lane_rx-or-tx_power_highest_Check
    [Documentation]  this test is to check lane rx or tx power highest test
    [Tags]     BSP_10.2.17.15_Lane_rx-or-tx_power_highest_Check  tianhe
    [Timeout]  10 min 00 seconds
    [Setup]  boot into diag os mode
    Step  1  read lane rx and tx power highest test  ${CONN_TOOL}  ${TX_POWER_OPTION}  Highest
    Step  2  read lane rx and tx power highest test  ${CONN_TOOL}  ${RX_POWER_OPTION}  Highest

BSP_10.2.17.16_Lane_rx-or-tx_power_input_Check
    [Documentation]  this test is to check lane rx or tx power input test
    [Tags]     BSP_10.2.17.16_Lane_rx-or-tx_power_input_Check  tianhe
    [Timeout]  10 min 00 seconds
    [Setup]  boot into diag os mode
    Step  1  read lane rx and tx power input test  ${CONN_TOOL}  ${TX_INPUT_OPTION}  Input
    Step  2  read lane rx and tx power input test  ${CONN_TOOL}  ${RX_INPUT_OPTION}  Input

BSP_10.2.17.17_Lane_rx-or-tx_power_lowest_Check
    [Documentation]  this test is to check lane rx or tx power lowest test
    [Tags]     BSP_10.2.17.17_Lane_rx-or-tx_power_lowest_Check  tianhe
    [Timeout]  10 min 00 seconds
    [Setup]  boot into diag os mode
    Step  1  read lane rx and tx power lowest test  ${CONN_TOOL}  ${TX_LOWEST_OPTION}  Lowest
    Step  2  read lane rx and tx power lowest test  ${CONN_TOOL}  ${RX_LOWEST_OPTION}  Lowest

BSP_10.2.17.18_Lane_tx_bias_highest_Check
    [Documentation]  this test is to check lane tx bias higheset test
    [Tags]     BSP_10.2.17.18_Lane_tx_bias_highest_Check  tianhe
    [Timeout]  10 min 00 seconds
    [Setup]  boot into diag os mode
    Step  1  check lane measured tx bias current  ${CONN_TOOL}  ${BIAS_HIGHEST_OPTION}  BiasHighest

BSP_10.2.17.19_Lane_tx_bias_input_Check
    [Documentation]  this test is to check lane tx bias input test
    [Tags]     BSP_10.2.17.19_Lane_tx_bias_input_Check  tianhe
    [Timeout]  10 min 00 seconds
    [Setup]  boot into diag os mode
    Step  1  check lane tx bias input  ${CONN_TOOL}  ${BIAS_INPUT_OPTION}  BiasInput

BSP_10.2.17.20_Lane_tx_bias_lowest_Check
    [Documentation]  this test is to check lane tx bias lowest test
    [Tags]     BSP_10.2.17.20_Lane_tx_bias_lowest_Check  tianhe
    [Timeout]  10 min 00 seconds
    [Setup]  boot into diag os mode
    Step  1  check lane tx bias lowest  ${CONN_TOOL}  ${BIAS_LOWEST_OPTION}  BiasLowest

BSP_10.2.17.21_Lane_tx_disable_Check
    [Documentation]  this test is to check lane tx disable
    [Tags]     BSP_10.2.17.21_Lane_tx_disable_Check  tianhe
    [Timeout]  10 min 00 seconds
    [Setup]  boot into diag os mode
    Step  1  read lane tx fault test  ${CONN_TOOL}  ${TX_DISABLE_OPTION}  TX_Disable
    Step  2  enable or disable lane tx output  ${CONN_TOOL}  ${TX_DISABLE_OPTION}  ${interrupt_value1}
    Step  3  read lane tx fault test  ${CONN_TOOL}  ${TX_DISABLE_OPTION}  TX_Disable
    Step  4  enable or disable lane tx output  ${CONN_TOOL}  ${TX_DISABLE_OPTION}  ${interrupt_value2}
    Step  5  read lane tx fault test  ${CONN_TOOL}  ${TX_DISABLE_OPTION}  TX_Disable

BSP_10.2.17.22_Lane_tx_fault_Check
    [Documentation]  this test is to check lane tx fault
    [Tags]     BSP_10.2.17.22_Lane_tx_fault_Check  tianhe
    [Timeout]  10 min 00 seconds
    [Setup]  boot into diag os mode
    Step  1  read lane tx fault test  ${CONN_TOOL}  ${TX_FAULT_OPTION}  TxFault

BSP_10.2.17.23_Cable_Length_Check
    [Documentation]  this test is to check cable length test
    [Tags]     BSP_10.2.17.23_Cable_Length_Check  tianhe
    [Timeout]  10 min 00 seconds
    [Setup]  boot into diag os mode
    Step  1  check the cable assembly length  ${CONN_TOOL}  ${CABLE_LENGTH_OPTION}  ${interrupt_value2}  Cable_Length

BSP_10.2.17.24_Medium_type_Check
    [Documentation]  this test is to check medium type test
    [Tags]     BSP_10.2.17.24_Medium_type_Check  tianhe
    [Timeout]  10 min 00 seconds
    [Setup]  boot into diag os mode
    Step  1  check the port medium type  ${CONN_TOOL}  ${CABLE_TYPE_OPTION}  ${CABLE_TYPE_PATTERN}  Medium_Type

BSP_10.2.17.25_Module_type_Check
    [Documentation]  this test is to check module type test
    [Tags]     BSP_10.2.17.25_Module_type_Check  tianhe
    [Timeout]  10 min 00 seconds
    [Setup]  boot into diag os mode
    Step  1  check the port module type  ${CONN_TOOL}  ${MODULE_TYPE_OPTION}  ${MODULE_TYPE_PATTERN}  Module_Type

BSP_10.2.17.26_Nominal_Wavelength_Check
    [Documentation]  this test is to check nominal wavelength test
    [Tags]     BSP_10.2.17.26_Nominal_Wavelength_Check  tianhe
    [Timeout]  10 min 00 seconds
    [Setup]  boot into diag os mode
    Step  1  check the wavelength  ${CONN_TOOL}  ${WAVELENGTH_OPTION}  ${interrupt_value2}  ${WAVELENGTH_PATTERN}  Wavelength

BSP_10.2.17.27_Port_num_Check
    [Documentation]  this test is to check port num test
    [Tags]     BSP_10.2.17.27_Port_num_Check  tianhe
    [Timeout]  10 min 00 seconds
    [Setup]  boot into diag os mode
    Step  1  check the port num test  ${CONN_TOOL}  ${PORT_NUM_OPTION}


BSP_10.2.17.28_Power_override_Check
    [Documentation]  this test is to check power override
    [Tags]     BSP_10.2.17.28_Power_override_Check  tianhe
    [Timeout]  10 min 00 seconds
    [Setup]  boot into diag os mode
    Step  1  check power override test  ${CONN_TOOL}  ${OVERRIDE_OPTION}  ${interrupt_value2}  Power_Override
    Step  2  set power override test  ${CONN_TOOL}  ${OVERRIDE_OPTION}  ${interrupt_value1}
    Step  3  check power override test  ${CONN_TOOL}  ${OVERRIDE_OPTION}  ${interrupt_value2}  Power_Override

BSP_10.2.17.29_Power_set_Check
    [Documentation]  this test is to check power set
    [Tags]     BSP_10.2.17.29_Power_set_Check  tianhe
    [Timeout]  10 min 00 seconds
    [Setup]  boot into diag os mode
    Step  1  check power set test  ${CONN_TOOL}  ${POWER_SET_OPTION}  ${interrupt_value1}  Power_Set
    Step  2  set power set test  ${CONN_TOOL}  ${POWER_SET_OPTION}  ${interrupt_value1}
    Step  3  check power set test  ${CONN_TOOL}  ${POWER_SET_OPTION}  ${interrupt_value1}  Power_Set

BSP_10.2.17.30_Power_Class_Check
    [Documentation]  this test is to check power class test
    [Tags]     BSP_10.2.17.30_Power_Class_Check  tianhe
    [Timeout]  10 min 00 seconds
    [Setup]  boot into diag os mode
    Step  1  check the power class  ${CONN_TOOL}  ${POWERCLASS_OPTION}  ${POWERCLASS_PATTERN1}  ${POWERCLASS_PATTERN2}  Powerclass

BSP_10.2.17.31_Temp1_higest_Check
    [Documentation]  this test is to check temp1 higest test
    [Tags]     BSP_10.2.17.31_Temp1_higest_Check  tianhe
    [Timeout]  10 min 00 seconds
    [Setup]  boot into diag os mode
    Step  1  check the temp1 higest test  ${CONN_TOOL}  ${TEMP1_OPTION}  ${interrupt_value2}  Temp1_Higest

BSP_10.2.17.32_Temp1_input_Check
    [Documentation]  this test is to check temp1 input test
    [Tags]     BSP_10.2.17.32_Temp1_input_Check  tianhe
    [Timeout]  10 min 00 seconds
    [Setup]  boot into diag os mode
    Step  1  check the temp1 input test  ${CONN_TOOL}  ${TEMP1_INPUT_OPTION}  ${interrupt_value2}  Temp1_Input

BSP_10.2.17.33_Temp1_label_Check
    [Documentation]  this test is to check temp1 label test
    [Tags]     BSP_10.2.17.33_Temp1_label_Check  tianhe
    [Timeout]  10 min 00 seconds
    [Setup]  boot into diag os mode
    Step  1  check the temp1 label test  ${CONN_TOOL}  ${TEMP1_LABEL_OPTION}

BSP_10.2.17.34_Temp1_lowest_Check
    [Documentation]  this test is to check temp1 lowest test
    [Tags]     BSP_10.2.17.34_Temp1_lowest_Check  tianhe
    [Timeout]  10 min 00 seconds
    [Setup]  boot into diag os mode
    Step  1  check the temp1 lowest test  ${CONN_TOOL}  ${TEMP1_LOWEST_OPTION}  ${interrupt_value2}  Temp1_Lowest


BSP_10.2.17.37_Temp1_reset_history_Check
    [Documentation]  this test is to check temp1 reset history test
    [Tags]     BSP_10.2.17.37_Temp1_reset_history_Check  tianhe
    [Timeout]  10 min 00 seconds
    [Setup]  boot into diag os mode
    Step  1  set the temp1 reset history test  ${CONN_TOOL}  ${TEMP1_RESET_OPTION}  ${interrupt_value1}

BSP_10.2.17.38_Vendor_name_Check
    [Documentation]  this test is to check vendor name test
    [Tags]     BSP_10.2.17.38_Vendor_name_Check  tianhe
    [Timeout]  10 min 00 seconds
    [Setup]  boot into diag os mode
    Step  1  read vendor name test  ${CONN_TOOL}  ${VENDOR_NAME_TOOL}  ${VENDOR_NAME_PATTERN}  Vendor_Name

BSP_10.2.17.39_Vendor_part_num_Check
    [Documentation]  this test is to check vendor part num test
    [Tags]     BSP_10.2.17.39_Vendor_part_num_Check  tianhe
    [Timeout]  10 min 00 seconds
    [Setup]  boot into diag os mode
    Step  1  read vendor part num test  ${CONN_TOOL}  ${VENDOR_PARTNUM_TOOL}  ${VENDOR_PARTNUM_PATTERN}  Vendor_PartNum

BSP_10.2.17.40_Vendor_revision_num_Check
    [Documentation]  this test is to check vendor revision num test
    [Tags]     BSP_10.2.17.40_Vendor_revision_num_Check  tianhe
    [Timeout]  10 min 00 seconds
    [Setup]  boot into diag os mode
    Step  1  read vendor revision num test  ${CONN_TOOL}  ${VENDOR_REVISION_OPTION}  ${VENDOR_REVISION_PATTERN}  Vendor_RevisionNum

BSP_10.2.17.41_Vendor_serial_num_Check
    [Documentation]  this test is to check vendor serial num test
    [Tags]     BSP_10.2.17.41_Vendor_serial_num_Check  tianhe
    [Timeout]  10 min 00 seconds
    [Setup]  boot into diag os mode
    Step  1  read vendor serial num test  ${CONN_TOOL}  ${VENDOR_SERIAL_OPTION}





*** Keywords ***
DiagOS Connect Device
    DiagOSConnect

DiagOS Disconnect Device
    DiagOSDisconnect



