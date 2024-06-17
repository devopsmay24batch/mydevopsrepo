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
    [Tags]  BSP_TC00_Diag_Initialize_And_Version_Check  fenghuang
    [Setup]  boot Into Onie Rescue Mode
    Step  1  Diag Check network connectivity  ${ONIE_RESCUE_MODE}
    Step  2  Diag format Disk  ${fail_dict}
    Step  3  Diag mount Disk  ${fail_dict}
    Step  4  Diag download Images And Recovery DiagOS  ${fail_dict}
    Step  5  Self Update Onie  new
    Step  6  power Cycle To DiagOS
    Step  7  check version before the test
    Step  8  check driver version  ${drive_pattern}

#BSP_TC01_INSTALL_DRIVER_TEST
#    [Tags]  BSP_TC01_INSTALL_DRIVER_TEST
#    ...  briggs  fenghuang  shenzhou  tigris
#
#    Step  1  uboot boot to diagos
#    Step  2  dhclient get ip
#    Step  3  ping to IP  ${diagos_mode}  ${tftp_server_ipv4}
#    Step  4  reinstall BSP Driver


BSP_TC02_CPLD_Version_Test
    [Documentation]  This test is to check CPLD version
    [Tags]     BSP_TC02_CPLD_Version_Test  fenghuang
    [Timeout]  2 min 00 seconds
    Step  1  verify cpld versions  filelist=${cpld_file_list}


BSP_TC03_BOARD_VERSION_TEST
    [Tags]  BSP_TC03_BOARD_VERSION_TEST
    ...  briggs  fenghuang  shenzhou  tigris

    [Setup]  force unload/load all kernel driver matched with *.ko file

    Step  1  read board version


BSP_TC04_CPLD_RAW_ACCESS_TEST
    [Tags]  BSP_TC04_CPLD_RAW_ACCESS_TEST
    ...  briggs  fenghuang  shenzhou  tigris

    [Setup]  force unload/load all kernel driver matched with *.ko file

    Step  1  read raw access data attribute
    ...  path=${i2c_devices_tree}[LOGGER_DUMP][PATH]
    Step  2  read raw access address attribute
    ...  path=${i2c_devices_tree}[LOGGER_DUMP][PATH]
    Step  3  write data to raw access data attribute
    ...  path=${i2c_devices_tree}[LOGGER_DUMP][PATH]
    ...  data=0x14 0x01
    Step  4  write data to raw access address attribute
    ...  path=${i2c_devices_tree}[LOGGER_DUMP][PATH]
    ...  address=0x14
    Step  5  read raw access data attribute
    ...  path=${i2c_devices_tree}[LOGGER_DUMP][PATH]
    Step  6  read raw access address attribute
    ...  path=${i2c_devices_tree}[LOGGER_DUMP][PATH]


BSP_TC05_CONSOLE_LOGGER_DUMP_TEST
    [Tags]  BSP_TC05_CONSOLE_LOGGER_DUMP_TEST
    ...  briggs  fenghuang  shenzhou  tigris

    [Setup]  force unload/load all kernel driver matched with *.ko file

    Step  1  set logger dump baud rate to 115200 kbps
    Step  2  simple read logger dump
    Step  3  verify logger dump reset functionality
    Step  4  verify logger dump pause functionality


# BSP_TC134_ASC10_DRIVER_TEST
#     [Tags]  BSP_TC134_ASC10_DRIVER_TEST
#     ...  briggs  fenghuang  shenzhou  tigris

#     Step  1  read ASC10 all sysfs attribute in*_input  path=
#     Step  2  read ASC10 all sysfs attribute in*_input  path=
#     Step  3  read all ASC10 by diagtool
#     Step  4  compare all ASC10 input value


BSP_TC11_Port_Module_Interrupt_Test
    [Documentation]  This test is to check the optical module interrupt status
    [Tags]     common  BSP_TC11_Port_Module_Interrupt_Test  fenghuang
    [Timeout]  5 min 00 seconds
    Step  1  cat loop file info  path=${interrupt_port_file_path}  pre=${file_pre}  suf=${file_suf}  passpattern=${interrupt_port_info_passpattern_list}

BSP_TC12_Port_Module_Present_Test
    [Documentation]  This test is check the optical module predent status
    [Tags]     BSP_TC12_Port_Module_Present_Test  fenghuang
    [Timeout]  5 min 00 seconds
    Step  1  cat loop file info  path=${interrupt_port_file_path}  pre=${present_file_pre}  suf=${present_file_suf}  passpattern=${present_passpattern_list}

BSP_TC13_Port_Module_Reset_Test
    [Documentation]  This test is check the optical module reset signal
    [Tags]     BSP_TC13_Port_Module_Reset_Test  fenghuang
    [Timeout]  2 min 00 seconds
    Step  1  cat loop file info  path=${interrupt_port_file_path}  pre=${reset_file_pre}  suf=${reset_file_suf}  passpattern=${reset_passpattern_list1}
    Step  2  modify reset file value  path=${interrupt_port_file_path}  pre=${reset_file_pre}  suf=${reset_file_suf}  value=${echo_value}
    Step  3  cat loop file info  path=${interrupt_port_file_path}  pre=${reset_file_pre}  suf=${reset_file_suf}  passpattern=${reset_passpattern_list2}
    [Teardown]  modify reset file value  path=${interrupt_port_file_path}  pre=${reset_file_pre}  suf=${reset_file_suf}  value=${port_module_reset_value}

BSP_TC18_PSU_Voltage_Fault_Test
    [Documentation]  this test is to check PSU voltage fault status
    [Tags]     BSP_TC18_PSU_Voltage_Fault_Test  fenghuang
    [Timeout]  1 min 00 seconds
    Step  1  cat loop file info  path=${psu_voltage_file_path}  pre=${psu_filename}  part=1  passpattern=${voltage_passpattern}

BSP_TC19_PSU_Voltage_Up_Test
    [Documentation]  check PSU all voltage rails up stat
    [Tags]     BSP_TC19_PSU_Voltage_Up_Test  fenghuang
    [Timeout]  1 min 00 seconds
    Step  1  cat loop file info  path=${psu_voltage_up_file_path}  pre=${psu_up_filename}  part=1  passpattern=${voltage_up_passpattern}


BSP_TC20_FAN_MAX_SPEED_TEST
    [Tags]  BSP_TC20_FAN_MAX_SPEED_TEST
    ...  briggs  fenghuang  shenzhou  tigris
    ...  pending

    [Setup]  force unload/load all kernel driver matched with *.ko file

    Step  1  disable fan watchdog by file system attribute
    Step  2  write pwm value by diagtool  pwd=50
    Step  3  read fan maximum speed from file system attribute  pattern=(?m)^(?P<fan_max_speed>\\\\w+$)  # It should be 0 here, but unit does not work for now
    Step  4  write fan maximum speed to file system attribute  fan_max_speed=1
    Step  5  read fan maximum speed from file system attribute  pattern=(?m)^(?P<fan_max_speed>\\\\w+$)  # It should be 1 here, but unit does not work for now

    Step  6  read current fan pwm by diagtool
    # Step  7  verify current fan pwm value read by diagtool  pwm=255  # More step than doc here to keep like doc intention to check it

    Step  8  write fan maximum speed to file system attribute  fan_max_speed=0
    Step  9  write pwm value by diagtool  pwd=100

    Step  10  read current fan pwm by diagtool
    # Step  11  verify current fan pwm value read by diagtool  pwm=100  # More step than doc here to keep like doc intention to check it


BSP_TC21_FAN_RESET_TEST
    [Tags]  BSP_TC21_FAN_RESET_TEST
    ...  briggs  fenghuang  shenzhou  tigris
    ...  pending

    # Pending meaning ... I want you to fix it after the unit gets fix/working normally!
    #
    # Masked as pending due to the hardware/software issue not working normally
    # An example:
    #   1) The default should be 0 and no matter it is
    #   2) Just exit code is 0
    #   3) Auto reset to 0 (now accepted all)
    #      Please update pattern to correct this
    #   4) Expected for full speed (RPM or PWM=255??), now accepted all,
    #      Please update patterns to correct this

    [Setup]  force unload/load all kernel driver matched with *.ko file

    Step  1  read fan reset by file system attribute
    Step  2  write fan reset by file system attribute  fan_reset=1
    Step  3  read fan reset by file system attribute
    Step  4  read all current fans pwm by diagtool


BSP_TC22_SYSTEM_WATCHDOG_ENABLE_TEST
    [Tags]  BSP_TC22_SYSTEM_WATCHDOG_ENABLE_TEST
    ...  briggs  fenghuang  shenzhou  tigris
    ...  pending

    # Pending to do list
    # 1) Step 3-5 - see its comments
    # 2) Step 7 - update the pattern to detect, now accepted all

    [Setup]  force unload/load all kernel driver matched with *.ko file

    Step  1  write a time to system watchdog attribute
    # Step  2  read watchdog timeout by file system attribute  # Additional than the doc!

    # The doc said, re-enable it for 3 times within 5s
    # Step  3  enable system watchdog by file system attribute  # Comment due to "echo: write error: Invalid argument" the unit is not normally work, waiting for fix it
    # Step  4  enable system watchdog by file system attribute  # Comment due to "echo: write error: Invalid argument" the unit is not normally work, waiting for fix it
    # Step  5  enable system watchdog by file system attribute  # Comment due to "echo: write error: Invalid argument" the unit is not normally work, waiting for fix it

    Step  6  sleep for second(s)  console=${diagos_mode}  sleep=15  # After 10s the watchdog should reset the system
    Step  7  open prompt  console=${diagos_mode}  sec=300  # System watchdog take reboot
    Step  8  read system watchdog enable status by file system attribute


BSP_TC23_System_Watchdog_Seconds_Test
    [Documentation]  check watchdog counter time
    [Tags]     BSP_TC23_System_Watchdog_Seconds_Test  fenghuang
    [Timeout]  10 min 00 seconds
    Step  1  echo value to file  path=${device_15_0060_path}  file=${watchdog_time_file}  value=${watchdog_time_value}
    Step  2  loop to echo value to file  path=${device_15_0060_path}  file=${watchdog_enable_file}  value=${watchdog_enable_value}
    Step  3  read until to diagos
    Step  4  cat loop file info  path=${device_15_0060_path}  part=1  pre=${watchdog_time_file}  passpattern=${watchdog_time_pass_list}
    Step  5  cat loop file info  path=${device_15_0060_path}  part=1  pre=${watchdog_enable_file}  passpattern=${watchdog_enable_pass_list}

BSP_TC29_LED_CPLD_Reset_Test
    [Documentation]  This test is to check led cpld reset
    [Tags]     BSP_TC29_LED_CPLD_Reset_Test  fenghuang
    [Timeout]  3 min 00 seconds
    Step  1  cat loop file info  path=${platform_15_0060_path}  pre=${led_cpld_reset}  part=1  passpattern=${led_reset_passpattern}
    Step  2  echo value to file  path=${platform_15_0060_path}  file=${led_cpld_reset}  value=${led_reset_value}
    Step  3  cat loop file info  path=${platform_15_0060_path}  pre=${led_cpld_reset}  part=1  passpattern=${led_reset_passpattern}

BSP_TC_30_I2C_Reset_Test
    [Documentation]  This test is to check reset SC18IS600
    [Tags]     BSP_TC_30_I2C_Reset_Test  fenghuang
    [Timeout]  3 min 00 seconds
    Step  1  cat loop file info  path=${device_15_0060_path}  pre=${i2c_reset_file}  part=1  passpattern=${i2c_reset_passpattern}
    Step  2  echo value to file  path=${device_15_0060_path}  file=${i2c_reset_file}  value=${i2c_reset_value}
    Step  3  cat loop file info  path=${device_15_0060_path}  pre=${i2c_reset_file}  part=1  passpattern=${i2c_reset_passpattern}

# He Min has reported:
# Run this TC will be crashed the system and folder disappeared, always mark as pending for a moment till fix
BSP_TC31_WARM_RESET_TEST
    [Tags]  BSP_TC31_WARM_RESET_TEST
    ...  fenghuang
    ...  pending

    # Pending due to..and wnats you to update..
    # Step 2 has no effect to restart the system
    # Step 3 comments due to above

    [Setup]  force unload/load all kernel driver matched with *.ko file

    Step  1  read warm reset by file system attribute
    Step  2  write warm reset by file system attribute  warm_reset=1
    # Step  3  open prompt  console=${diagos_mode}  sec=300
    Step  4  read warm reset by file system attribute


BSP_TC32_COLD_RESET_TEST
    [Tags]  BSP_TC32_COLD_RESET_TEST
    ...  fenghuang
    ...  pending

    # Pending due to..and wnats you to update..
    # Step 2 has no effect to restart the system
    # Step 3 comments due to above

    [Setup]  force unload/load all kernel driver matched with *.ko file

    Step  1  read cold reset by file system attribute
    Step  2  write cold reset by file system attribute  cold_reset=1
    # Step  3  open prompt  console=${diagos_mode}  sec=300
    Step  4  read cold reset by file system attribute


BSP_TC33_Fan_CPLD_Reset_Test
    [Documentation]  This test is to check fan reset status
    [Tags]     BSP_TC33_Fan_CPLD_Reset_Test  fenghuang
    [Timeout]  3 min 00 seconds
    Step  1  cat loop file info  path=${device_15_0060_path}  pre=${fan_reset}  part=1  passpattern=${fan_reset_default_value}
    Step  2  echo value to file  path=${device_15_0060_path}  file=${fan_reset}  value=${fan_reset_value}
    Step  3  cat loop file info  path=${device_15_0060_path}  pre=${fan_reset}  part=1  passpattern=${fan_reset_default_value}

BSP_TC34_ASIC(BCM5980)_Reset_Test
    [Documentation]  This test is to check chip (bcm56980) reset status
    [Tags]     BSP_TC34_ASIC(BCM5980)_Reset_Test  fenghuang
    [Timeout]  3 min 00 seconds
    Step  1  cat loop file info  path=${device_15_0060_path}  pre=${asic_reset}  part=1  passpattern=${asic_reset_passpattern_list}
    Step  2  echo value to file  path=${device_15_0060_path}  file=${asic_reset}  value=${asic_reset_reset_value}
    Step  3  cat loop file info  path=${device_15_0060_path}  pre=${asic_reset}  part=1  passpattern=${asic_reset_passpattern_list}

BSP_TC35_LED_CPLD(CPLD2/3)_Reset_Test
    [Documentation]  This test is to check cpld2/3 reset status
    [Tags]     BSP_TC35_LED_CPLD(CPLD2/3)_Reset_Test  fenghuang
    [Timeout]  3 min 00 seconds
    Step  1  cat loop file info  path=${device_15_0060_path}  pre=${led_cpld2_3_reset}  part=1  passpattern=${led_cpld2_3_reset_passpattern}
    Step  2  echo value to file  path=${device_15_0060_path}  file=${led_cpld2_3_reset}  value=${led_cpld2_3_reset_value}
    Step  3  cat loop file info  path=${device_15_0060_path}  pre=${led_cpld2_3_reset}  part=1  passpattern=${led_cpld2_3_reset_passpattern}

BSP_TC36_QSFP_MUX[1..4]_Reset_Test
    [Documentation]  this test is to check i2c mux PCA9548
    [Tags]     BSP_TC36_QSFP_MUX[1..4]_Reset_Test  fenghuang
    [Timeout]  6 min 00 seconds
    Step  1  cat loop file info  path=${device_15_0060_path}  pre=${qsfp_mux_file_pre}  suf=${qsfp_mux_file_suf}  part=4  passpattern=${qsfp_mux_passpattern_list1}
    Step  2  modify reset file value  path=${device_15_0060_path}  pre=${qsfp_mux_file_pre}  suf=${qsfp_mux_file_suf}  value=${qsfp_mux_reset_value}  part=4
    Step  3  cat loop file info  path=${device_15_0060_path}  pre=${qsfp_mux_file_pre}  suf=${qsfp_mux_file_suf}  part=4  passpattern=${qsfp_mux_passpattern_list2}
    Step  4  modify reset file value  path=${device_15_0060_path}  pre=${qsfp_mux_file_pre}  suf=${qsfp_mux_file_suf}  value=${qsfp_mux_default_value}  part=4
    Step  5  cat loop file info  path=${device_15_0060_path}  pre=${qsfp_mux_file_pre}  suf=${qsfp_mux_file_suf}  part=4  passpattern=${qsfp_mux_passpattern_list1}

BSP_TC37_Swith_Board_EEPROM_Test
    [Documentation]  This test is to check board EEPROM
    [Tags]     BSP_TC37_Swith_Board_EEPROM_Test  fenghuang
    [Timeout]  6 min 00 seconds
    Step  1  cat loop file info  path=${device_15_0060_path}  pre=${board_eeprom_wp}  part=1  passpattern=${board_eeprom_default_passpattern}
    Step  2  echo value to file  path=${device_15_0060_path}  file=${board_eeprom_wp}  value=${board_eeprom_wp_reset_value}
    Step  3  cat loop file info  path=${device_15_0060_path}  pre=${board_eeprom_wp}  part=1  passpattern=${board_eeprom_wp_reset_passpattern}
    Step  4  cat loop file info  path=${device_20_0056_path}  pre=${board_eeprom_cmd}  part=1  passpattern=${board_eeprom_passpattern}
    Step  5  echo value to file  path=${device_20_0056_path}  file=${board_eeprom}  value=${board_eeprom_reset_value1}
    Step  6  cat loop file info  path=${device_20_0056_path}  pre=${board_eeprom_cmd}  part=1  passpattern=${board_eeprom_reset_passpattern}
    Step  7  echo value to file  path=${device_20_0056_path}  file=${board_eeprom}  value=${board_eeprom_reset_value2}
    Step  8  cat loop file info  path=${device_20_0056_path}  pre=${board_eeprom_cmd}  part=1  passpattern=${board_eeprom_passpattern}
    [Teardown]  echo value to file  path=${device_15_0060_path}  file=${board_eeprom_wp}  value=${board_eeprom_wp_default_value}

BSP_TC38_Fan_board_EEPROM_Test
    [Documentation]  This test is to check Fan board EEPROM
    [Tags]     BSP_TC38_Fan_board_EEPROM_Test  fenghuang
    [Timeout]  6 min 00 seconds
    Step  1  verify exe cmd no output  cmd=${cmd_close_eeprom_protect}
    Step  2  verify exe cmd no output  cmd=${cmd_val}
    Step  3  verify exe cmd no output  cmd=${cmd_i2cset}
    Step  4  cat loop file info  path=${device_5_0056_path}  pre=${fan_board_eeprom_str}  part=1  passpattern=${fan_board_eeprom_passpattern1}
    Step  5  echo value to file  path=${device_5_0056_path}  file=${fan_board_eeprom}  value=${echo_fan_board_eeprom_value1}
    Step  6  cat loop file info  path=${device_5_0056_path}  pre=${fan_board_eeprom_str}  part=1  passpattern=${fan_board_eeprom_passpattern2}
    Step  7  echo value to file  path=${device_5_0056_path}  file=${fan_board_eeprom}  value=${echo_fan_board_eeprom_value2}
    Step  8  cat loop file info  path=${device_5_0056_path}  pre=${fan_board_eeprom_str}  part=1  passpattern=${fan_board_eeprom_passpattern1}
    Step  9  verify exe cmd no output  cmd=${cmd_open_eeprom_protect}
    Step  10  verify exe cmd no output  cmd=${cmd_i2cset_val}


BSP_TC39_PSU_EEPROM_TEST
    [Tags]  BSP_TC39_PSU_EEPROM_TEST
    ...  briggs  fenghuang  shenzhou  tigris

    [Setup]  force unload/load all kernel driver matched with *.ko file

    Step  1  dump PSU eeprom on file system attribute
    ...  path=${i2c_devices_tree}[PSU1_EEPROM][PATH]
    Step  2  dump PSU eeprom on file system attribute
    ...  path=${i2c_devices_tree}[PSU2_EEPROM][PATH]


BSP_TC40_FAN_Module_EEPROM_Test
    [Documentation]  test is to check FAN tray EEPROM
    [Tags]     BSP_TC40_FAN_Module_EEPROM_Test  fenghuang
    [Timeout]  6 min 00 seconds
    Step  1  verify exe cmd no output  cmd=${cmd_close_eeprom_protect}
    Step  2  verify exe cmd no output  cmd=${cmd_val}
    Step  3  verify exe cmd no output  cmd=${cmd_i2cset}
    Step  4  cat loop file info  path=${fan_module_eeprom_path}  suf=${fan_module_eeprom_suf}  part=13  passpattern=${fan_module_eeprom_passpattern1}  start_index=7
    Step  5  modify reset file value  path=${fan_module_eeprom_path}  suf=${fan_module_eeprom_file_suf}  value=${fan_module_eeprom_value1}  part=13  start_index=7
    Step  6  cat loop file info  path=${fan_module_eeprom_path}  suf=${fan_module_eeprom_suf}  part=13  passpattern=${fan_module_eeprom_passpattern2}  start_index=7
    Step  7  modify reset file value  path=${fan_module_eeprom_path}  suf=${fan_module_eeprom_file_suf}  value=${fan_module_eeprom_value2}  part=13  start_index=7
    Step  8  cat loop file info  path=${fan_module_eeprom_path}  suf=${fan_module_eeprom_suf}  part=13  passpattern=${fan_module_eeprom_passpattern1}  start_index=7
    Step  10  verify exe cmd no output  cmd=${cmd_open_eeprom_protect}
    Step  11  verify exe cmd no output  cmd=${cmd_i2cset_val}


BSP_TC41_ASC10_DRIVER_TEST
    [Tags]  BSP_TC41_ASC10_DRIVER_TEST
    ...  briggs  fenghuang  shenzhou  tigris

    [Setup]  force unload/load all kernel driver matched with *.ko file

    Step  1  read all ASC10-1 values by diagtool
    Step  2  read all ASC10-2 values by diagtool
    Step  3  verify all ASC10-1 values by file system attribute
    Step  4  verify all ASC10-2 values by file system attribute
    Step  5  compare all ASC10 1 & 2 values for file system attribute with diagtool table min/max values


BSP_TC42_LM75_DRIVER_TEST
    [Tags]  BSP_TC42_LM75_DRIVER_TEST
    # Not sure for briggs and tigris
    ...  fenghuang  shenzhou

    [Setup]  force unload/load all kernel driver matched with *.ko file

    Step  1  verify all LM75 devices for its all file system attributes

BSP_TC43_Fan_Direction_Test
    [Documentation]  This test is to check fan direction
    [Tags]     BSP_TC43_Fan_Direction_Test  fenghuang
    [Timeout]  3 min 00 seconds
    Step  1  cat loop file info  ${device_5_0066_path}  ${fan_direction_file_pre}  ${fan_direction_file_suf}  14  ${fan_direction_passpattern}  1

BSP_TC44_FAN_INPUT_TEST
    [Documentation]  This test is to check fan input
    [Tags]  BSP_TC44_FAN_INPUT_TEST  fenghuang
    [Timeout]  10 min 00 seconds
    [Setup]  boot into diag os mode
    Step  1  read FAN input  ${system_FAN_input_cmd}
    Step  2  read FAN input  ${diag_FAN_input_cmd}
    Step  3  compare system and diag FAN input

BSP_TC45_Fan_Label_Test
    [Documentation]  This test is to check fan label if it is correct
    [Tags]     BSP_TC45_Fan_Label_Test  fenghuang
    [Timeout]  3 min 00 seconds
    Step  1  verify fan label info  ${device_5_0066_path}  ${fan_label_file_pre}  ${fan_label_file_suf}  ${fan_label_pattern1_pre}  ${fan_label_pattern1_suf}
    Step  2  verify fan label info  ${device_5_0066_path}  ${fan_label_file_pre}  ${fan_label_file_suf}  ${fan_label_pattern2_pre}  ${fan_label_pattern2_suf}  2

BSP_TC47_Fan_max_Speed(RPM)_Test
    [Documentation]  This test is to check each fan max speed setting
    [Tags]     BSP_TC47_Fan_max_Speed(RPM)_Test  fenghuang
    [Timeout]  6 min 00 seconds
    Step  1  cat loop file info  ${device_5_0066_path}  ${fan_max_speed_path_pre}  ${fan_max_speed_path_suf}  14  ${fan_max_speed_passpattern1}
    Step  2  modify reset file value  ${device_5_0066_path}  ${fan_max_speed_path_pre}  ${fan_max_speed_path_suf}  ${echo_max_speed}  14
    Step  3  cat loop file info  ${device_5_0066_path}  ${fan_max_speed_path_pre}  ${fan_max_speed_path_suf}  14  ${fan_max_speed_passpattern2}

BSP_TC48_Fan_min_Speed(RPM)_Test
    [Documentation]  This test is to check each fan min speed setting
    [Tags]     BSP_TC48_Fan_min_Speed(RPM)_Test  fenghuang
    [Timeout]  6 min 00 seconds
    Step  1  cat loop file info  ${device_5_0066_path}  ${fan_min_speed_path_pre}  ${fan_min_speed_path_suf}  14  ${fan_min_speed_passpattern1}
    Step  2  modify reset file value  ${device_5_0066_path}  ${fan_min_speed_path_pre}  ${fan_min_speed_path_suf}  ${echo_min_speed}  14
    Step  3  cat loop file info  ${device_5_0066_path}  ${fan_min_speed_path_pre}  ${fan_min_speed_path_suf}  14  ${fan_min_speed_passpattern2}
    [Teardown]  modify reset file value  ${device_5_0066_path}  ${fan_min_speed_path_pre}  ${fan_min_speed_path_suf}  ${echo_min_default}  14

BSP_TC50_Fan_board_EEPROM_protect_Test
    [Documentation]  This test is to set the Fan Board eeprom write protect status
    [Tags]     BSP_TC50_Fan_board_EEPROM_protect_Test  fenghuang
    [Timeout]  6 min 00 seconds
    Step  1  cat loop file info  path=${device_5_0066_path}  pre=${fan_board_eeprom_protect}  part=1  passpattern=${fan_board_eeprom_protect_passpattern1}
    Step  2  echo value to file  path=${device_5_0066_path}  file=${fan_board_eeprom_protect}  value=${fan_board_eeprom_protect_value}
    Step  3  cat loop file info  path=${device_5_0066_path}  pre=${fan_board_eeprom_protect}  part=1  passpattern=${fan_board_eeprom_protect_passpattern2}
    [Teardown]  echo value to file  path=${device_5_0066_path}  file=${fan_board_eeprom_protect}  value=${fan_board_eeprom_protect_default}

BSP_TC51_FAN_Watchdog_Enable_Test
    [Documentation]  This test is to check that enable of disable Fan watchdog function
    [Tags]     BSP_TC51_FAN_Watchdog_Enable_Test  fenghuang
    [Timeout]  6 min 00 seconds
    [Setup]  verify exe cmd no output  cmd=${cd_fan_watchdog_path}
    Step  1  verify exe cmd no output  cmd=${fan_watchdog_export_cmd1}
    Step  2  verify exe cmd no output  cmd=${fan_watchdog_export_cmd2}
    Step  3  cat loop file info  path=${device_5_0066_path}  pre=${fan_watchdog_enable}  part=1  passpattern=${fan_watchdog_passpattern1}
    Step  4  echo value to file  path=${device_5_0066_path}  file=${fan_watchdog_enable}  value=${fan_watchdog_value}
    Step  5  cat loop file info  path=${device_5_0066_path}  pre=${fan_watchdog_enable}  part=1  passpattern=${fan_watchdog_passpattern2}
    Step  6  verify exe cmd no output  cmd=${fan_watchdog_test_cmd}
    Step  7  echo value to file  path=${device_5_0066_path}  file=${fan_watchdog_enable}  value=${fan_watchdog_default}
    Step  8  cat loop file info  path=${device_5_0066_path}  pre=${fan_watchdog_enable}  part=1  passpattern=${fan_watchdog_passpattern1}

BSP_TC52_FAN_Watchdog_Seconds_Test
    [Documentation]  This test is to check that enable of disable Fan watchdog function
    [Tags]     BSP_TC52_FAN_Watchdog_Seconds_Test  fenghuang
    [Timeout]  6 min 00 seconds
    Step  1  verify exe cmd no output  cmd=${fan_watchdog_export_cmd1}
    Step  2  verify exe cmd no output  cmd=${fan_watchdog_export_cmd2}
    Step  3  cat loop file info  path=${device_5_0066_path}  pre=${fan_watchdog_seconds}  part=1  passpattern=${fan_watchdog_seconds_passpattern1}
    Step  4  echo value to file  path=${device_5_0066_path}  file=${fan_watchdog_seconds}  value=${fan_watchdog_seconds_value}
    Step  5  cat loop file info  path=${device_5_0066_path}  pre=${fan_watchdog_seconds}  part=1  passpattern=${fan_watchdog_seconds_passpattern2}
    Step  6  verify fan speed change  ${fan_watchdog_path}  ${fan_tool_name}  ${fan_test_option1}  ${fan_test_option2}  ${fan_speed_pattern2}  ${fan_speed_pattern1}
    [Teardown]  echo value to file  path=${device_5_0066_path}  file=${fan_watchdog_seconds}  value=${fan_watchdog_seconds_default}

BSP_TC53_Fan_Speed_PWM_test
    [Documentation]  This test is to check that set the fan speed of fan module (0-255)
    [Tags]     BSP_TC53_Fan_Speed_PWM_test  fenghuang
    [Timeout]  6 min 00 seconds
    Step  1  cat loop file info  path=${device_5_0066_path}  pre=${fan_speed_pwm_pre}  part=14  passpattern=${fan_speed_pwm_passpattern1}
    Step  2  modify reset file value  path=${device_5_0066_path}  pre=${fan_speed_pwm_pre}  value=${fan_speed_pwm_value}  part=14
    Step  3  cat loop file info  path=${device_5_0066_path}  pre=${fan_speed_pwm_pre}  part=14  passpattern=${fan_speed_pwm_passpattern2}
    [Teardown]  modify reset file value  path=${device_5_0066_path}  pre=${fan_speed_pwm_pre}  value=${fan_speed_pwd_default}  part=14


BSP_TC54_REGISTER_RAW_ACCESS_TEST
    [Tags]  BSP_TC54_REGISTER_RAW_ACCESS_TEST
    ...  briggs  fenghuang  shenzhou  tigris

    [Setup]  force unload/load all kernel driver matched with *.ko file

    Step  1  read raw access address attribute  pattern=(?m)^(?P<raw_access_addr>0x[0-9a-fA-F]{1,2})$
    Step  2  write data to raw access address attribute  address=0xab
    Step  1  read raw access address attribute  pattern=(?m)^(?P<raw_access_addr>0xab)$


BSP_TC55_REGISTER_RAW_DATA_TEST
    [Tags]  BSP_TC55_REGISTER_RAW_DATA_TEST
    ...  briggs  fenghuang  shenzhou  tigris

    [Setup]  force unload/load all kernel driver matched with *.ko file

    Step  1  simple check access FAN raw data attribute
    Step  2  write data to raw access address attribute
    Step  3  read raw access data attribute
    Step  4  read raw access address attribute


BSP_TC56_MANUFACTURE_INFORMATION_CHECK
    [Tags]  BSP_TC56_MANUFACTURE_INFORMATION_CHECK
    ...  briggs  fenghuang  shenzhou  tigris

    [Setup]  force unload/load all kernel driver matched with *.ko file

    Step  1  verify all PSU1 file system attributes
    Step  2  verify all PSU2 file system attributes


BSP_TC58_DCDC_DRIVER_TEST
    [Tags]  BSP_TC58_DCDC_DRIVER_TEST
    ...  briggs  fenghuang  shenzhou  tigris

    [Setup]  force unload/load all kernel driver matched with *.ko file

    Step  1  verify all CDCD/IR35215 devices for its all file system attributes


BSP_TC59_CPLD2_3_RAW_ACCESS_TEST
    [Tags]  BSP_TC59_CPLD2_3_RAW_ACCESS_TEST
    ...  briggs  fenghuang  shenzhou

    [Setup]  force unload/load all kernel driver matched with *.ko file

    # CPLD2
    Step  1  write data to raw access data attribute
    ...  path=${i2c_devices_tree}[CPLD2][PATH]
    ...  data=0x01 0xab
    Step  2  write data to raw access address attribute
    ...  path=${i2c_devices_tree}[CPLD2][PATH]
    ...  address=0x01
    Step  3  read raw access data attribute
    ...  path=${i2c_devices_tree}[CPLD2][PATH]
    Step  4  read raw access address attribute
    ...  path=${i2c_devices_tree}[CPLD2][PATH]

    # CPLD3
    Step  5  write data to raw access data attribute
    ...  path=${i2c_devices_tree}[CPLD3][PATH]
    ...  data=0x01 0xab
    Step  6  write data to raw access address attribute
    ...  path=${i2c_devices_tree}[CPLD3][PATH]
    ...  address=0x01
    Step  7  read raw access data attribute
    ...  path=${i2c_devices_tree}[CPLD3][PATH]
    Step  8  read raw access address attribute
    ...  path=${i2c_devices_tree}[CPLD3][PATH]


BSP_TC60_LED_ENABLE_TEST
    [Tags]  BSP_TC60_LED_ENABLE_TEST
    ...  briggs  fenghuang  shenzhou

    [Setup]  force unload/load all kernel driver matched with *.ko file

    Step  1  read led enable attribute
    ...  path=${i2c_devices_tree}[CPLD2][PATH]
    Step  2  read led enable attribute
    ...  path=${i2c_devices_tree}[CPLD3][PATH]
    Step  3  write to led enable attribute
    ...  path=${i2c_devices_tree}[CPLD2][PATH]
    ...  enable=1
    Step  4  write to led enable attribute
    ...  path=${i2c_devices_tree}[CPLD3][PATH]
    ...  enable=1


# This TC can check only the ability of the file system attribute "led_color"
# and not confirm the color on the front of the machine!
BSP_TC61_LED_COLOR_TEST
    [Tags]  BSP_TC61_LED_COLOR_TEST
    ...  briggs  fenghuang  shenzhou

    [Setup]  force unload/load all kernel driver matched with *.ko file

    Step  1   read led color attribute
    ...  path=${i2c_devices_tree}[CPLD2][PATH]
    Step  2   read led color attribute
    ...  path=${i2c_devices_tree}[CPLD3][PATH]
    Step  3   write color to led color attribute
    ...  path=${i2c_devices_tree}[CPLD2][PATH]
    ...  color=green
    Step  4   write color to led color attribute
    ...  path=${i2c_devices_tree}[CPLD3][PATH]
    ...  color=green
    Step  5   write color to led color attribute
    ...  path=${i2c_devices_tree}[CPLD2][PATH]
    ...  color=white
    Step  6   write color to led color attribute
    ...  path=${i2c_devices_tree}[CPLD3][PATH]
    ...  color=white
    Step  7   write color to led color attribute
    ...  path=${i2c_devices_tree}[CPLD2][PATH]
    ...  color=blue
    Step  8   write color to led color attribute
    ...  path=${i2c_devices_tree}[CPLD3][PATH]
    ...  color=blue
    Step  9   write color to led color attribute
    ...  path=${i2c_devices_tree}[CPLD2][PATH]
    ...  color=off
    Step  10  write color to led color attribute
    ...  path=${i2c_devices_tree}[CPLD3][PATH]
    ...  color=off


BSP_TC62_INSTALLATOIN_TEST
    [Tags]  BSP_TC62_INSTALLATOIN_TEST
    ...  briggs  fenghuang  shenzhou  tigris

    Step  1  U-Boot renew DHCP/IP
    Step  2  U-Boot setenv  env=serverip ${tftp_server_ipv4}
    Step  3  U-Boot run uploadonie
    Step  4  open prompt  console=${onie_mode}  sec=300


BSP_TC63_CPLD_UPDATER_TEST
    [Tags]  BSP_TC63_CPLD_UPDATER_TEST
    ...  briggs  fenghuang  shenzhou  tigris

    Step  1  update SYS CPLD firmware
    Step  2  read SYS CPLD version
    Step  3  update FAN CPLD firmware
    Step  4  read FAN CPLD version
    Step  5  open prompt  console=${uboot_mode}  sec=300
    Step  6  read SYS CPLD version
    Step  7  read FAN CPLD version


BSP_TC65_UBOOT_MGMT_TFTP_STRESS_TEST
    [Tags]  BSP_TC65_UBOOT_MGMT_TFTP_STRESS_TEST
    ...  briggs  fenghuang  tigris
    ...  stress

    Step  1   U-Boot mdio read
    Step  2   U-Boot sleep
    Step  3   U-Boot mdio read
    Step  4   U-Boot sleep
    Step  5   U-Boot mdio read
    Step  6   U-Boot sleep
    Step  7   U-Boot setenv  env=serverip ${tftp_server_ipv4}
    Step  8   U-Boot setenv  env=ipaddr ${tftp_client_ipv4}
    Step  9   U-Boot tftpboot
    Step  10  U-Boot reset


*** Keywords ***
DiagOS Connect Device
    DiagOSConnect

DiagOS Disconnect Device
    DiagOSDisconnect
