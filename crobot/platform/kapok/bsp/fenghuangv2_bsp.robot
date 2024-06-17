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
    [Tags]  BSP_TC00_Diag_Initialize_And_Version_Check  fenghuangv2
    [Timeout]  60 min 00 seconds
    [Setup]  boot Into Onie Rescue Mode
    Step  1  Diag Check network connectivity  ${ONIE_RESCUE_MODE}
    Step  2  fhv2 Diag download Images And Recovery DiagOS
    Step  3  Self Update Onie  new
    Step  4  power Cycle To DiagOS
    Step  5  check version before the test
    Step  6  check driver version  ${drive_pattern}

BSP_10.1.1.1_INSTALL_DRIVER_TEST
    [Tags]  BSP_10.1.1.1_INSTALL_DRIVER_TEST  fenghuangv2
    Step  1  uboot boot to diagos
    Step  2  dhclient get ip
    Step  3  ping to IP  ${diagos_mode}  ${tftp_server_ipv4}
    Step  4  reinstall BSP Driver


BSP_10.1.2.1.1_CPLD_Version_Test
    [Documentation]  This test is to check CPLD version
    [Tags]     BSP_10.1.2.1.1_CPLD_Version_Test  fenghuangv2
    [Timeout]  2 min 00 seconds
    Step  1  verify cpld versions  filelist=${cpld_file_list}


BSP_10.1.2.1.2_BOARD_VERSION_TEST
    [Tags]  BSP_10.1.2.1.2_BOARD_VERSION_TEST  fenghuangv2

    #[Setup]  force unload/load all kernel driver matched with *.ko file
    Step  1  read board version


BSP_10.1.2.1.3_CPLD_RAW_ACCESS_TEST
    [Tags]  BSP_10.1.2.1.3_CPLD_RAW_ACCESS_TEST  fenghuangv2

    #[Setup]  force unload/load all kernel driver matched with *.ko file

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


BSP_10.1.3_CONSOLE_LOGGER_DUMP_TEST
    [Tags]  BSP_10.1.3_CONSOLE_LOGGER_DUMP_TEST  fenghuangv2

    #[Setup]  force unload/load all kernel driver matched with *.ko file

    Step  1  fhv2 set logger dump baud rate to 115200 kbps
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


BSP_10.1.5.1_Port_Module_Interrupt_Test
    [Documentation]  This test is to check the optical module interrupt status
    [Tags]     common  BSP_10.1.5.1_Port_Module_Interrupt_Test  fenghuangv2
    [Timeout]  5 min 00 seconds
    Step  1  cat loop file info  path=${interrupt_port_file_path}  pre=${file_pre}  suf=${file_suf}  passpattern=${interrupt_port_info_passpattern_list_0}
    Step  2  Page Select And IntL Config  pre=${i2cset_IntL_pre}  suf=${i2cset_IntL_suf}  page_pre=${page_select_pre}  page_suf=${page_selest_suf}
    Step  3  cat loop file info  path=${interrupt_port_file_path}  pre=${file_pre}  suf=${file_suf}  passpattern=${interrupt_port_info_passpattern_list_1}
    Step  4  Page Select And IntL Config  pre=${i2cset_IntL_clear_pre}  suf=${i2cset_IntL_clear_suf}  page_pre=${page_select_pre}  page_suf=${page_selest_suf}
    Step  5  cat loop file info  path=${interrupt_port_file_path}  pre=${file_pre}  suf=${file_suf}  passpattern=${interrupt_port_info_passpattern_list_0}

#BSP_TC12_Port_Module_Interrupt_Mask_Test
    #[Documentation]  This test is to check the optical module interrupt mask status
    #[Tags]     BSP_TC12_Port_Module_Interrupt_Mask_Test  fenghuang
    #[Timeout]  5 min 00 seconds
    #Step  1  cat loop file info  path=${interrupt_port_file_path}  pre=${mask_pre}  suf=${mask_suf}  passpattern=${common_test_pattern1}
    #Step  2  modify reset file value  path=${interrupt_port_file_path}  pre=${mask_pre}  suf=${mask_suf}  value=${modify_file_value1}
    #Step  3  cat loop file info  path=${interrupt_port_file_path}  pre=${mask_pre}  suf=${mask_suf}  passpattern=${common_test_pattern2}
    #Step  4  modify reset file value  path=${interrupt_port_file_path}  pre=${mask_pre}  suf=${mask_suf}  value=${modify_file_value2}
    #Step  5  cat loop file info  path=${interrupt_port_file_path}  pre=${mask_pre}  suf=${mask_suf}  passpattern=${common_test_pattern1}

BSP_10.1.5.2_Port_Module_Present_Test
    [Documentation]  This test is check the optical module predent status
    [Tags]     BSP_10.1.5.2_Port_Module_Present_Test  fenghuangv2
    [Timeout]  5 min 00 seconds
    Step  1  cat loop file info  path=${interrupt_port_file_path}  pre=${present_file_pre}  suf=${present_file_suf}  passpattern=${present_passpattern_list}

BSP_10.1.5.3_Port_Module_Reset_Test
    [Documentation]  This test is check the optical module reset signal
    [Tags]     BSP_10.1.5.3_Port_Module_Reset_Test  fenghuangv2
    [Timeout]  2 min 00 seconds
    Step  1  cat loop file info  path=${interrupt_port_file_path}  pre=${reset_file_pre}  suf=${reset_file_suf}  passpattern=${reset_passpattern_list1}
    Step  2  modify reset file value  path=${interrupt_port_file_path}  pre=${reset_file_pre}  suf=${reset_file_suf}  value=${echo_value}
    Step  3  cat loop file info  path=${interrupt_port_file_path}  pre=${reset_file_pre}  suf=${reset_file_suf}  passpattern=${reset_passpattern_list2}
    [Teardown]  modify reset file value  path=${interrupt_port_file_path}  pre=${reset_file_pre}  suf=${reset_file_suf}  value=${port_module_reset_value}

BSP_10.1.15.2_Uboot_Update_Test_via_SPI_Flash
    [Documentation]  This test is to ensure that onie can install by flashcp on onie
    [Tags]  BSP_10.1.15.2_Uboot_Update_Test_via_SPI_Flash  fenghuangv2
    [Timeout]  60 min 00 seconds
    [Setup]   boot into onie rescue mode
    Step  1  if config and ping address   ${ipaddr}
    Step  2  tftp uboot image  ${server_ip}  ${image}
    Step  3  cat dev mtd and erase mtd0
    Step  4  upgrade onie  ${image}
    Step  5  check onie version

BSP_10.1.15.3_Uboot_Update_Test_via_TFTP
    [Documentation]  This test is to check the U-boot installation
    [Tags]  BSP_10.1.15.3_Uboot_Update_Test_via_TFTP
    [Timeout]  60 min 00 seconds
    [Setup]   boot into Uboot
    Step  1  set ipaddr and server  ${ipaddr}  ${serverip}
    Step  2  run bootupd
    Step  3  check Uboot ver

BSP_10.1.6.5_PSU_Voltage_Fault_Test
    [Documentation]  this test is to check PSU voltage fault status
    [Tags]     BSP_10.1.6.5_PSU_Voltage_Fault_Test  fenghuangv2
    [Timeout]  1 min 00 seconds
    [Setup]   uboot boot to diagos
    Step  1  cat loop file info  path=${psu_voltage_file_path}  pre=${psu_filename}  part=1  passpattern=${voltage_passpattern}

BSP_10.1.6.6_PSU_Voltage_Up_Test
    [Documentation]  check PSU all voltage rails up stat
    [Tags]     BSP_10.1.6.6_PSU_Voltage_Up_Test  fenghuangv2
    [Setup]   uboot boot to diagos
    [Timeout]  1 min 00 seconds
    Step  1  cat loop file info  path=${psu_voltage_up_file_path}  pre=${psu_up_filename}  part=1  passpattern=${voltage_up_passpattern}


BSP_10.1.7.1_FAN_MAX_SPEED_TEST
    [Tags]  BSP_10.1.7.1_FAN_MAX_SPEED_TEST  fenghuangv2

    #[Setup]  force unload/load all kernel driver matched with *.ko file

    Step  1  disable fan watchdog by file system attribute
    Step  2  write pwm value by diagtool  pwd=50
    Step  3  read fan maximum speed from file system attribute  pattern=(?m)^(?P<fan_max_speed>\\\\w+$)  # It should be 0 here, but unit does not work for now
    Step  4  write fan maximum speed to file system attribute  fan_max_speed=1
    Step  5  read fan maximum speed from file system attribute  pattern=(?m)^(?P<fan_max_speed>\\\\w+$)  # It should be 1 here, but unit does not work for now

    Step  6  read all current fans pwm by diagtool
    Step  7  verify current fan pwm value read by diagtool  pwm=255  # More step than doc here to keep like doc intention to check it

    Step  8  write fan maximum speed to file system attribute  fan_max_speed=0
    Step  9  write pwm value by diagtool  pwd=100

    Step  10  read all current fans pwm by diagtool
    Step  11  verify current fan pwm value read by diagtool  pwm=100  # More step than doc here to keep like doc intention to check it


#BSP_TC21_FAN_RESET_TEST
    #[Tags]  BSP_TC21_FAN_RESET_TEST
    #...  briggs  fenghuang  shenzhou  tigris
    #...  pending

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

    #[Setup]  force unload/load all kernel driver matched with *.ko file

    #Step  1  read fan reset by file system attribute
    #Step  2  write fan reset by file system attribute  fan_reset=1
    #Step  3  read fan reset by file system attribute
    #Step  4  read all current fans pwm by diagtool


BSP_10.1.8.1_SYSTEM_WATCHDOG_ENABLE_TEST
    [Tags]  BSP_10.1.8.1_SYSTEM_WATCHDOG_ENABLE_TEST  fenghuangv2

    # Pending to do list
    # 1) Step 3-5 - see its comments
    # 2) Step 7 - update the pattern to detect, now accepted all

    #[Setup]  force unload/load all kernel driver matched with *.ko file

    Step  1  write a time to system watchdog attribute
    Step  2  fhv2 read watchdog timeout by file system attribute  # Additional than the doc!

    # The doc said, re-enable it for 3 times within 5s
    Step  3  enable system watchdog by file system attribute  # Comment due to "echo: write error: Invalid argument" the unit is not normally work, waiting for fix it
    Step  4  enable system watchdog by file system attribute  # Comment due to "echo: write error: Invalid argument" the unit is not normally work, waiting for fix it
    Step  5  enable system watchdog by file system attribute  # Comment due to "echo: write error: Invalid argument" the unit is not normally work, waiting for fix it

    Step  6  sleep time  300  # After 600s the watchdog should reset the system
    Step  7  open prompt  console=${diagos_mode}  sec=300  # System watchdog take reboot
    Step  8  fhv2 read system watchdog enable status by file system attribute


BSP_10.1.8.2_System_Watchdog_Seconds_Test
    [Documentation]  check watchdog counter time
    [Tags]     BSP_10.1.8.2_System_Watchdog_Seconds_Test  fenghuangv2
    [Timeout]  10 min 00 seconds
    Step  1  echo value to file  path=${device_15_0060_path}  file=${watchdog_time_file}  value=${watchdog_time_value}
    Step  2  loop to echo value to file  path=${device_15_0060_path}  file=${watchdog_enable_file}  value=${watchdog_enable_value}
    Step  3  read until to diagos
    Step  4  cat loop file info  path=${device_15_0060_path}  part=1  pre=${watchdog_time_file}  passpattern=${watchdog_time_pass_list}
    Step  5  cat loop file info  path=${device_15_0060_path}  part=1  pre=${watchdog_enable_file}  passpattern=${watchdog_enable_pass_list}

BSP_10.1.8.3_FAN_Watchdog_Enable_Test
    [Documentation]  This test is to check that enable of disable Fan watchdog function
    [Tags]     BSP_10.1.8.3_FAN_Watchdog_Enable_Test  fenghuangv2
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

BSP_10.1.8.4_FAN_Watchdog_Seconds_Test
    [Documentation]  This test is to check that enable of disable Fan watchdog function
    [Tags]     BSP_10.1.8.4_FAN_Watchdog_Seconds_Test  fenghuangv2
    [Timeout]  6 min 00 seconds
    [Setup]  echo value to file  path=${device_5_0066_path}  file=${fan_watchdog_enable}  value=${fan_watchdog_default}
    Step  1  verify exe cmd no output  cmd=${fan_watchdog_export_cmd1}
    Step  2  verify exe cmd no output  cmd=${fan_watchdog_export_cmd2}
    Step  3  cat loop file info  path=${device_5_0066_path}  pre=${fan_watchdog_seconds}  part=1  passpattern=${fan_watchdog_seconds_passpattern1}
    Step  4  echo value to file  path=${device_5_0066_path}  file=${fan_watchdog_seconds}  value=${fan_watchdog_seconds_value}
    Step  5  cat loop file info  path=${device_5_0066_path}  pre=${fan_watchdog_seconds}  part=1  passpattern=${fan_watchdog_seconds_passpattern2}
    Step  6  verify fan speed change  ${fan_watchdog_path}  ${fan_tool_name}  ${fan_test_option1}  ${fan_test_option2}  ${fan_speed_pattern2}  ${fan_speed_pattern1}
    [Teardown]  echo value to file  path=${device_5_0066_path}  file=${fan_watchdog_seconds}  value=${fan_watchdog_seconds_default}

# He Min has reported:
# Run this TC will be crashed the system and folder disappeared, always mark as pending for a moment till fix
BSP_10.1.10.1_WARM_RESET_TEST
    [Tags]  BSP_10.1.10.1_WARM_RESET_TEST  fenghuangv2

    # Pending due to..and wnats you to update..
    # Step 2 has no effect to restart the system
    # Step 3 comments due to above

    #[Setup]  force unload/load all kernel driver matched with *.ko file

    Step  1  fhv2 read warm reset by file system attribute
    Step  2  fhv2 write warm reset by file system attribute  warm_reset=1
    Step  3  sleep time  300  # After 300s it will finish reboot
    Step  4  open prompt  console=${diagos_mode}  sec=300
    Step  5  fhv2 read warm reset by file system attribute

BSP_10.1.10.2_COLD_RESET_TEST
    [Tags]  BSP_10.1.10.2_COLD_RESET_TEST  fenghuangv2

    # Pending due to..and wnats you to update..
    # Step 2 has no effect to restart the system
    # Step 3 comments due to above

    #[Setup]  force unload/load all kernel driver matched with *.ko file

    Step  1  fhv2 read cold reset by file system attribute
    Step  2  fhv2 write cold reset by file system attribute  cold_reset=1
    Step  3  sleep time  300  # After 300s it will finish reboot
    Step  4  open prompt  console=${diagos_mode}  sec=300
    Step  5  fhv2 read cold reset by file system attribute

BSP_10.1.10.3_Fan_CPLD_Reset_Test
    [Documentation]  This test is to check fan reset status
    [Tags]     BSP_10.1.10.3_Fan_CPLD_Reset_Test  fenghuangv2
    [Timeout]  3 min 00 seconds
    Step  1  cat loop file info  path=${device_15_0060_path}  pre=${fan_reset}  part=1  passpattern=${fan_reset_default_value}
    Step  2  echo value to file  path=${device_15_0060_path}  file=${fan_reset}  value=${fan_reset_value}
    Step  3  cat loop file info  path=${device_15_0060_path}  pre=${fan_reset}  part=1  passpattern=${fan_reset_default_value}

BSP_10.1.10.4_LED_CPLD(CPLD2/3)_Reset_Test
    [Documentation]  This test is to check cpld2/3 reset status
    [Tags]     BSP_10.1.10.4_LED_CPLD(CPLD2/3)_Reset_Test  fenghuangv2
    [Timeout]  3 min 00 seconds
    Step  1  cat loop file info  path=${device_15_0060_path}  pre=${led_cpld2_3_reset}  part=1  passpattern=${led_cpld2_3_reset_passpattern}
    Step  2  echo value to file  path=${device_15_0060_path}  file=${led_cpld2_3_reset}  value=${led_cpld2_3_reset_value}
    Step  3  cat loop file info  path=${device_15_0060_path}  pre=${led_cpld2_3_reset}  part=1  passpattern=${led_cpld2_3_reset_passpattern}

#BSP_10.1.10.5_LED_CPLD_Reset_Test
    #[Documentation]  This test is to check led cpld reset
    #[Tags]     BSP_10.1.10.4_LED_CPLD_Reset_Test  fenghuangv2
    #[Timeout]  3 min 00 seconds
    #Step  1  cat loop file info  path=${platform_15_0060_path}  pre=${led_cpld_reset}  part=1  passpattern=${led_reset_passpattern}
    #Step  2  echo value to file  path=${platform_15_0060_path}  file=${led_cpld_reset}  value=${led_reset_value}
    #Step  3  cat loop file info  path=${platform_15_0060_path}  pre=${led_cpld_reset}  part=1  passpattern=${led_reset_passpattern}

BSP_10.1.11.1_Swith_Board_EEPROM_Test
    [Documentation]  This test is to check board EEPROM
    [Tags]     BSP_10.1.11.1_Swith_Board_EEPROM_Test  fenghuangv2
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

BSP_10.1.11.2_PSU_EEPROM_TEST
    [Tags]  BSP_10.1.11.2_PSU_EEPROM_TEST  fenghuangv2

    #[Setup]  force unload/load all kernel driver matched with *.ko file

    Step  1  dump PSU eeprom on file system attribute
    ...  path=${i2c_devices_tree}[PSU1_EEPROM][PATH]
    Step  2  dump PSU eeprom on file system attribute
    ...  path=${i2c_devices_tree}[PSU2_EEPROM][PATH]

BSP_10.1.12.1_Fan_Direction_Test
    [Documentation]  This test is to check fan direction
    [Tags]     BSP_10.1.12.1_Fan_Direction_Test  fenghuangv2
    [Timeout]  3 min 00 seconds
    Step  1  cat loop file info  ${device_5_0066_path}  ${fan_direction_file_pre}  ${fan_direction_file_suf}  12  ${fan_direction_passpattern}  1

BSP_10.1.12.2_FAN_INPUT_TEST
    [Documentation]  This test is to check fan input
    [Tags]  BSP_10.1.12.2_FAN_INPUT_TEST  fenghuangv2
    [Timeout]  10 min 00 seconds
    [Setup]  boot into diag os mode
    Step  1  read FAN input  ${system_FAN_input_cmd}
    Step  2  read FAN input  ${diag_FAN_input_cmd}
    Step  3  compare system and diag FAN input

BSP_10.1.12.3_Fan_Label_Test
    [Documentation]  This test is to check fan label if it is correct
    [Tags]     BSP_10.1.12.3_Fan_Label_Test  fenghuangv2
    [Timeout]  3 min 00 seconds
    Step  1  verify fan label info  ${device_5_0066_path}  ${fan_label_file_pre}  ${fan_label_file_suf}  ${fan_label_pattern1_pre}  ${fan_label_pattern1_suf}
    Step  2  verify fan label info  ${device_5_0066_path}  ${fan_label_file_pre}  ${fan_label_file_suf}  ${fan_label_pattern2_pre}  ${fan_label_pattern2_suf}  2

BSP_10.1.12.5_Fan_max_Speed(RPM)_Test
    [Documentation]  This test is to check each fan max speed setting
    [Tags]     BSP_10.1.12.5_Fan_max_Speed(RPM)_Test  fenghuangv2
    [Timeout]  6 min 00 seconds
    Step  1  cat loop file info  ${device_5_0066_path}  ${fan_max_speed_path_pre}  ${fan_max_speed_path_suf}  12  ${fan_max_speed_passpattern1}
    Step  2  modify reset file value  ${device_5_0066_path}  ${fan_max_speed_path_pre}  ${fan_max_speed_path_suf}  ${echo_max_speed}  12
    Step  3  cat loop file info  ${device_5_0066_path}  ${fan_max_speed_path_pre}  ${fan_max_speed_path_suf}  12  ${fan_max_speed_passpattern2}

BSP_10.1.12.6_Fan_min_Speed(RPM)_Test
    [Documentation]  This test is to check each fan min speed setting
    [Tags]     BSP_10.1.12.6_Fan_min_Speed(RPM)_Test  fenghuangv2
    [Timeout]  6 min 00 seconds
    Step  1  cat loop file info  ${device_5_0066_path}  ${fan_min_speed_path_pre}  ${fan_min_speed_path_suf}  12  ${fan_min_speed_passpattern1}
    Step  2  modify reset file value  ${device_5_0066_path}  ${fan_min_speed_path_pre}  ${fan_min_speed_path_suf}  ${echo_min_speed}  12
    Step  3  cat loop file info  ${device_5_0066_path}  ${fan_min_speed_path_pre}  ${fan_min_speed_path_suf}  12  ${fan_min_speed_passpattern2}
    [Teardown]  modify reset file value  ${device_5_0066_path}  ${fan_min_speed_path_pre}  ${fan_min_speed_path_suf}  ${echo_min_default}  12


BSP_10.1.12.8_Fan_board_EEPROM_protect_Test
    [Documentation]  This test is to set the Fan Board eeprom write protect status
    [Tags]     BSP_10.1.12.8_Fan_board_EEPROM_protect_Test  fenghuangv2
    [Timeout]  6 min 00 seconds
    Step  1  cat loop file info  path=${device_5_0066_path}  pre=${fan_board_eeprom_protect}  part=1  passpattern=${fan_board_eeprom_protect_passpattern1}
    Step  2  echo value to file  path=${device_5_0066_path}  file=${fan_board_eeprom_protect}  value=${fan_board_eeprom_protect_value}
    Step  3  cat loop file info  path=${device_5_0066_path}  pre=${fan_board_eeprom_protect}  part=1  passpattern=${fan_board_eeprom_protect_passpattern2}
    [Teardown]  echo value to file  path=${device_5_0066_path}  file=${fan_board_eeprom_protect}  value=${fan_board_eeprom_protect_default}

BSP_10.1.12.9_Fan_Speed_PWM_test
    [Documentation]  This test is to check that set the fan speed of fan module (0-255)
    [Tags]     BSP_10.1.12.9_Fan_Speed_PWM_test  fenghuangv2
    [Timeout]  6 min 00 seconds
    [Setup]  modify reset file value  path=${device_5_0066_path}  pre=${fan_speed_pwm_pre}  value=${fan_speed_pwd_default}  part=12
    Step  1  cat loop file info  path=${device_5_0066_path}  pre=${fan_speed_pwm_pre}  part=12  passpattern=${fan_speed_pwm_passpattern1}
    Step  2  modify reset file value  path=${device_5_0066_path}  pre=${fan_speed_pwm_pre}  value=${fan_speed_pwm_value}  part=12
    Step  3  set Time To Sleep  10
    Step  4  cat loop file info  path=${device_5_0066_path}  pre=${fan_speed_pwm_pre}  part=12  passpattern=${fan_speed_pwm_passpattern2}
    [Teardown]  modify reset file value  path=${device_5_0066_path}  pre=${fan_speed_pwm_pre}  value=${fan_speed_pwd_default}  part=12

BSP_10.1.12.10_FAN_CPLD_RAW_ACCESS_TEST
    [Tags]  BSP_10.1.12.10_FAN_CPLD_RAW_ACCESS_TEST  fenghuangv2

    #[Setup]  force unload/load all kernel driver matched with *.ko file

    Step  1  read raw access address attribute  pattern=(?m)^(?P<raw_access_addr>0x[0-9a-fA-F]{1,2})$
    Step  2  write data to raw access address attribute  address=0xab
    Step  1  read raw access address attribute  pattern=(?m)^(?P<raw_access_addr>0xab)$

BSP_10.1.12.11_REGISTER_RAW_DATA_TEST
    [Tags]  BSP_10.1.12.11_REGISTER_RAW_DATA_TEST  fenghuangv2

    #[Setup]  force unload/load all kernel driver matched with *.ko file

    Step  1  simple check access FAN raw data attribute
    Step  2  write data to raw access address attribute
    Step  3  read raw access data attribute
    Step  4  read raw access address attribute

BSP_10.1.13_ASC10_DRIVER_TEST
    [Tags]  BSP_10.1.13_ASC10_DRIVER_TEST  fenghuangv2

    #[Setup]  force unload/load all kernel driver matched with *.ko file

    Step  1  read all ASC10-1 values by diagtool
    Step  2  read all ASC10-2 values by diagtool
    Step  3  read all ASC10-3 values by diagtool
    Step  4  fhv2 verify all ASC10-1 values by file system attribute
    Step  5  fhv2 verify all ASC10-2 values by file system attribute
    Step  6  fhv2 verify all ASC10-3 values by file system attribute
    Step  7  compare all ASC10 1 & 2 & 3 values for file system attribute with diagtool table min/max values

BSP_10.1.14.1_MANUFACTURE_INFORMATION_CHECK
    [Tags]  BSP_10.1.14.1_MANUFACTURE_INFORMATION_CHECK  fenghuangv2

    #[Setup]  force unload/load all kernel driver matched with *.ko file

    Step  1  verify all PSU1 file system attributes
    Step  2  verify all PSU2 file system attributes

BSP_10.1.15.1_Uboot_boot_log_check
    [Documentation]  This test is to check uboot boot log
    [Tags]     BSP_10.1.15.1_Uboot_boot_log_check  fenghuangv2
    [Timeout]  60 min 00 seconds
    Step  1  check reboot boot log msg  ${check_boot_log_msg_pattern}
  


BSP_10.1.15.5_UBOOT_MGMT_TFTP_STRESS_TEST
    [Tags]  BSP_10.1.15.5_UBOOT_MGMT_TFTP_STRESS_TEST  fenghuangv2  stress
    [Setup]  boot into Uboot

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

BSP_10.1.15.6_Uboot_environment_Variable_test
    [Documentation]  This test is to check uboot environment variable
    [Tags]     BSP_10.1.15.6_Uboot_environment_Variable_test  fenghuangv2
    [Timeout]  60 min 00 seconds
    Step  1  boot Into Uboot
    Step  2  set And Save Mac Address
    Step  3  boot Into Uboot
    Step  4  verify Can Found Parameter
    Step  5  boot Into Onie Rescue Mode
    Step  6  printenv Onie Uboot address
    Step  7  add Test Parameters  1
    Step  8  add Test Parameters  2
    Step  9  add Test Parameters  3
    Step  10  add Test Parameters  4
    Step  11  boot Into Uboot
    Step  12  printenv On Uboot

BSP_10.1.15.7_Uboot_booting_mode_check_test
    [Documentation]  This test is to check Uboot booting mode check test
    [Tags]     BSP_10.1.15.7_Uboot_booting_mode_check_test  fenghuangv2
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

BSP_10.2.2.1_ASIC(BCM5980)_Reset_Test
    [Documentation]  This test is to check chip (bcm56980) reset status
    [Tags]     BSP_10.2.2.1_ASIC(BCM5980)_Reset_Test  fenghuangv2
    [Timeout]  3 min 00 seconds
    Step  1  cat loop file info  path=${device_15_0060_path}  pre=${asic_reset}  part=1  passpattern=${asic_reset_passpattern_list}
    Step  2  echo value to file  path=${device_15_0060_path}  file=${asic_reset}  value=${asic_reset_reset_value}
    Step  3  cat loop file info  path=${device_15_0060_path}  pre=${asic_reset}  part=1  passpattern=${asic_reset_passpattern_list}

BSP_10.2.2.2_Warm_Reset_on_Reboot_Test
    [Documentation]  This test is to check warm reset on reboot test
    [Tags]     BSP_10.2.2.2_Warm_Reset_on_Reboot_Test  fenghuangv2
    [Timeout]  60 min 00 seconds
    [Setup]  boot into diag os mode
    Step  1  check warm reset on reboot   0
    Step  2  execute command  echo 1 > /sys/bus/i2c/devices/8-0060/warm_reset_on_reboot
    Step  3  check warm reset on reboot   1
    Step  4  Kapok reboot to U-Boot and enter to Diag OS
    Step  5  check warm reset on reboot  0
    [Teardown]  exec cmd  stty columns 1000   ## @WORKAROUND this case will change ttys and make following cases failed

BSP_10.2.2.3_Cold_Reset_on_Reboot_Test
    [Documentation]  This test is to check cold reset on reboot test
    [Tags]     BSP_10.2.2.3_Cold_Reset_on_Reboot_Test  fenghuangv2
    [Timeout]  60 min 00 seconds
    [Setup]  boot into diag os mode
    Step  1   check cold reset on reboot   0
    Step  2   execute command  echo 1 > /sys/bus/i2c/devices/8-0060/cold_reset_on_reboot
    Step  3   check cold reset on reboot   1
    Step  4   Kapok reboot to U-Boot and enter to Diag OS
    Step  5   check cold reset on reboot   0
    [Teardown]  exec cmd  stty columns 1000   ## @WORKAROUND this case will change ttys and make following cases failed

BSP_10.2.2.4_I2C_Reset_Test
    [Documentation]  This test is to check reset SC18IS600
    [Tags]     BSP_10.2.2.4_I2C_Reset_Test  fenghuangv2
    [Timeout]  3 min 00 seconds
    Step  1  cat loop file info  path=${device_15_0060_path}  pre=${i2c_reset_file}  part=1  passpattern=${i2c_reset_passpattern}
    Step  2  echo value to file  path=${device_15_0060_path}  file=${i2c_reset_file}  value=${i2c_reset_value}
    Step  3  cat loop file info  path=${device_15_0060_path}  pre=${i2c_reset_file}  part=1  passpattern=${i2c_reset_passpattern}

#Remove this case, This case not support in FH2
#BSP_TC36_QSFP_MUX[1..4]_Reset_Test
#    [Documentation]  this test is to check i2c mux PCA9548
#    [Tags]     BSP_TC36_QSFP_MUX[1..4]_Reset_Test  fenghuang
#    [Timeout]  6 min 00 seconds
#    Step  1  cat loop file info  path=${device_15_0060_path}  pre=${qsfp_mux_file_pre}  suf=${qsfp_mux_file_suf}  part=4  passpattern=${qsfp_mux_passpattern_list1}
#    Step  2  modify reset file value  path=${device_15_0060_path}  pre=${qsfp_mux_file_pre}  suf=${qsfp_mux_file_suf}  value=${qsfp_mux_reset_value}  part=4
#    Step  3  cat loop file info  path=${device_15_0060_path}  pre=${qsfp_mux_file_pre}  suf=${qsfp_mux_file_suf}  part=4  passpattern=${qsfp_mux_passpattern_list2}
#    Step  4  modify reset file value  path=${device_15_0060_path}  pre=${qsfp_mux_file_pre}  suf=${qsfp_mux_file_suf}  value=${qsfp_mux_default_value}  part=4
#    Step  5  cat loop file info  path=${device_15_0060_path}  pre=${qsfp_mux_file_pre}  suf=${qsfp_mux_file_suf}  part=4  passpattern=${qsfp_mux_passpattern_list1}

BSP_10.2.3.1_Fan_board_EEPROM_Test
    [Documentation]  This test is to check Fan board EEPROM
    [Tags]     BSP_10.2.3.1_Fan_board_EEPROM_Test  fenghuangv2
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

BSP_10.2.3.2_Check_FAN_Tray_EEPROM
    [Documentation]  This test is to check FAN tray EEPROM
    [Tags]  BSP_10.2.3.2_Check_FAN_Tray_EEPROM  fenghuangv2
    [Timeout]  6 min 00 seconds
    [Setup]  boot into diag os mode
    Step  1  cat loop file info  path=${fan_module_eeprom_path}  suf=${fan_module_eeprom_suf}  part=30  passpattern=${fan_module_eeprom_passpattern1}  start_index=25
    Step  2  modify reset file value  path=${fan_module_eeprom_path}  suf=${fan_module_eeprom_file_suf}  value=${fan_module_eeprom_value1}  part=30  start_index=25
    Step  3  cat loop file info  path=${fan_module_eeprom_path}  suf=${fan_module_eeprom_suf}  part=30  passpattern=${fan_module_eeprom_passpattern2}  start_index=25
    Step  4  modify reset file value  path=${fan_module_eeprom_path}  suf=${fan_module_eeprom_file_suf}  value=${fan_module_eeprom_value2}  part=30  start_index=25
    Step  5  cat loop file info  path=${fan_module_eeprom_path}  suf=${fan_module_eeprom_suf}  part=30  passpattern=${fan_module_eeprom_passpattern1}  start_index=25
    Step  6  check for fan7

#BSP_TC39_TOP_Fan_board_EEPROM_Test
    #[Documentation]  This test is to check Fan board EEPROM
    #[Tags]     BSP_TC39_TOP_Fan_board_EEPROM_Test  fenghuang
    #[Timeout]  6 min 00 seconds
    #Step  1  execute check dict  device=DUT  cmd=${read_eeprom_cmd}  patterns_dict=${busbar_board_eeprom_pattern1}
    #Step  2  verify exe cmd no output  cmd=${modify_eeprom_cmd1}
    #Step  3  execute check dict  device=DUT  cmd=${read_eeprom_cmd}  patterns_dict=${busbar_board_eeprom_pattern2}
    #Step  4  verify exe cmd no output  cmd=${modify_eeprom_cmd2}
    #Step  5  execute check dict  device=DUT  cmd=${read_eeprom_cmd}  patterns_dict=${busbar_board_eeprom_pattern1}

BSP_10.2.3.4_I2CFPGA_Board_EEPROMT_Test
    [Documentation]  This test is to check I2CFPGA board EEPROM
    [Tags]     BSP_10.2.3.4_I2CFPGA_Board_EEPROMT_Test  fenghuangv2  i2c
    [Timeout]  6 min 00 seconds
    Step  1  execute check dict  device=DUT  cmd=${read_i2ceeprom_protect}  patterns_dict=${i2ceeprom_protect_pattern}
    Step  2  verify exe cmd no output  cmd=${modify_i2ceeprom_protect_cmd1}
    Step  3  execute check dict  device=DUT  cmd=${read_i2c_eeprom_cmd}  patterns_dict=${busbar_board_eeprom_pattern1}
    Step  4  verify exe cmd no output  cmd=${modify_i2ceeprom_cmd1}
    Step  5  execute check dict  device=DUT  cmd=${read_i2c_eeprom_cmd}  patterns_dict=${busbar_board_eeprom_pattern2}
    Step  6  verify exe cmd no output  cmd=${modify_i2ceeprom_cmd2}
    Step  7  execute check dict  device=DUT  cmd=${read_i2c_eeprom_cmd}  patterns_dict=${busbar_board_eeprom_pattern1}
    [Teardown]  verify exe cmd no output  cmd=${modify_i2ceeprom_protect_cmd2}

BSP_10.2.3.5_Check_1PPS_FPGA_Card_EEPROM
    [Documentation]  This test is to check 1PPS FPGA Card EEPROM
    [Tags]  BSP_10.2.3.5_Check_1PPS_FPGA_Card_EEPROM  fenghuangv2
    [Timeout]  6 min 00 seconds
    [Setup]  boot into diag os mode
    Step  1  execute check dict  device=DUT  cmd=${read_fpgaeeprom_protect}  patterns_dict=${fpgaeeprom_protect_pattern}
    Step  2  verify exe cmd no output  cmd=${modify_fpgaeeprom_protect_cmd1}
    Step  3  execute check dict  device=DUT  cmd=${read_FPGA_card_eeprom_cmd}  patterns_dict=${FPGA_card_eeprom_pattern1}
    Step  4  verify exe cmd no output  cmd=${modify_FPGA_card_eeprom_cmd1}
    Step  5  execute check dict  device=DUT  cmd=${read_FPGA_card_eeprom_cmd}  patterns_dict=${FPGA_card_eeprom_pattern2}
    Step  6  verify exe cmd no output  cmd=${modify_FPGA_card_eeprom_cmd2}
    Step  7  execute check dict  device=DUT  cmd=${read_FPGA_card_eeprom_cmd}  patterns_dict=${FPGA_card_eeprom_pattern1}
    Step  8  verify exe cmd no output  cmd=${modify_fpgaeeprom_protect_cmd2}

BSP_10.2.3.6_Check_1PPS_SFP_Card_EEPROM
    [Documentation]  This test is to check 1PPS SFP-Card EEPROM
    [Tags]  BSP_10.2.3.6_Check_1PPS_SFP_Card_EEPROM  fenghuang
    [Timeout]  6 min 00 seconds
    [Setup]  boot into diag os mode
    Step  1  execute check dict  device=DUT  cmd=${read_fpgaeeprom_protect}  patterns_dict=${fpgaeeprom_protect_pattern}
    Step  2  verify exe cmd no output  cmd=${modify_fpgaeeprom_protect_cmd1}
    Step  3  execute check dict  device=DUT  cmd=${read_SFP_card_eeprom_cmd}  patterns_dict=${SFP_card_eeprom_pattern1}
    Step  4  verify exe cmd no output  cmd=${modify_SFP_card_eeprom_cmd1}
    Step  5  execute check dict  device=DUT  cmd=${read_SFP_card_eeprom_cmd}  patterns_dict=${SFP_card_eeprom_pattern2}
    Step  6  verify exe cmd no output  cmd=${modify_SFP_card_eeprom_cmd2}
    Step  7  execute check dict  device=DUT  cmd=${read_SFP_card_eeprom_cmd}  patterns_dict=${SFP_card_eeprom_pattern1}
    Step  8  verify exe cmd no output  cmd=${modify_fpgaeeprom_protect_cmd2}

BSP_10.2.3.7_Riser_board_eerpom_test
    [Documentation]  This test is to check riser board eerpom test
    [Tags]     BSP_10.2.3.7_Riser_board_eerpom_test  fenghuangv2
    [Timeout]  60 min 00 seconds
    Step  1  riser board eerpom test

BSP_10.2.4.1_Fan_eeprom_Power_Status_Test
    [Documentation]  This test is to read and set  Fan eeprom power status
    [Tags]  BSP_10.2.4.1_Fan_eeprom_Power_Status_Test  fenghuangv2
    [Timeout]  6 min 00 seconds
    [Setup]  boot into diag os mode
    Step  1  cat loop file info  path=${device_23_0066_path}  pre=${fan_eeprom_power}  part=1  passpattern=${fan_eeprom_power_passpattern1}
    Step  2  echo value to file  path=${device_23_0066_path}  file=${fan_eeprom_power}  value=${fan_eeprom_power_value}
    Step  3  cat loop file info  path=${device_23_0066_path}  pre=${fan_eeprom_power}  part=1  passpattern=${fan_eeprom_power_passpattern2}
    Step  4  echo value to file  path=${device_23_0066_path}  file=${fan_eeprom_power}  value=${fan_eeprom_power_default}
    Step  5  cat loop file info  path=${device_23_0066_path}  pre=${fan_eeprom_power}  part=1  passpattern=${fan_eeprom_power_passpattern1}

BSP_10.2.4.2_I2C_Fan_MUX_Reset_Test
    [Documentation]  This test is to reset I2C fan mux
    [Tags]  BSP_10.2.4.2_I2C_Fan_MUX_Reset_Test  fenghuangv2
    [Timeout]  6 min 00 seconds
    Step  1  cat loop file info  path=${device_23_0066_path}  pre=${fan_mux_reset}  part=1  passpattern=${fan_mux_reset_passpattern1}
    Step  2  echo value to file  path=${device_23_0066_path}  file=${fan_mux_reset}  value=${fan_mux_reset_value}
    Step  3  cat loop file info  path=${device_23_0066_path}  pre=${fan_mux_reset}  part=1  passpattern=${fan_mux_reset_passpattern2}
    Step  4  echo value to file  path=${device_23_0066_path}  file=${fan_mux_reset}  value=${fan_mux_reset_default}
    Step  5  cat loop file info  path=${device_23_0066_path}  pre=${fan_mux_reset}  part=1  passpattern=${fan_mux_reset_passpattern1}

BSP_10.2.5.1_CPLD2_3_RAW_ACCESS_TEST
    [Tags]  BSP_10.2.5.1_CPLD2_3_RAW_ACCESS_TEST  fenghuangv2

    #[Setup]  force unload/load all kernel driver matched with *.ko file

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


BSP_10.2.5.2_LED_ENABLE_TEST
    [Tags]  BSP_10.2.5.2_LED_ENABLE_TEST  fenghuangv2

    #[Setup]  force unload/load all kernel driver matched with *.ko file

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
BSP_10.2.5.3_LED_COLOR_TEST
    [Tags]  BSP_10.2.5.3_LED_COLOR_TEST  fenghuangv2

    #[Setup]  force unload/load all kernel driver matched with *.ko file

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

BSP_10.2.6_LM75_DRIVER_TEST
    [Tags]  BSP_10.2.6_LM75_DRIVER_TEST  fenghuangv2

    #[Setup]  force unload/load all kernel driver matched with *.ko file

    Step  1  verify all LM75 devices for its all file system attributes

BSP_10.2.7.1_Read_voltage_current_power_consumption
    [Documentation]  This test is to read voltage current and power consumption
    [Tags]  BSP_10.2.7.1_Read_voltage_current_power_consumption  fenghuangv2
    [Timeout]  60 min 00 seconds
    [Setup]  boot into diag os mode
    Step  1  cat loop file info  path=${device_path}  pre=${voltage}  part=1  passpattern=${pass_pattern}
    Step  2  cat loop file info  path=${device_path}  pre=${current}  part=1  passpattern=${pass_pattern}
    Step  3  cat loop file info  path=${device_path}  pre=${power}  part=1  passpattern=${pass_pattern}

BSP_10.2.8_DCDC_DRIVER_TEST
    [Tags]  BSP_10.2.8_DCDC_DRIVER_TEST  fenghuangv2

    #[Setup]  force unload/load all kernel driver matched with *.ko file

    Step  1  verify all CDCD/IR35215 devices for its all file system attributes

BSP_10.2.9_I2C_MCP3425_ADC_Driver_Test
    [Documentation]  this test is to check i2c mcp3425 adc driver
    [Tags]     BSP_10.2.9_I2C_MCP3425_ADC_Driver_Test  fenghuangv2
    [Timeout]  1 min 00 seconds
    [Setup]  boot into diag os mode
    Step  1  cat loop file info  path=${In_voltage0_path}  pre=${In_voltage0_raw}  part=1  passpattern=${In_voltage0_raw_pattern}
    Step  2  cat loop file info  path=${In_voltage0_path}  pre=${In_voltage0_scale}  part=1  passpattern=${In_voltage0_scale_pattern}
    Step  3  cat loop file info  path=${In_voltage0_path}  pre=${In_voltage_sampling_frequency}  part=1  passpattern=${In_voltage_sampling_frequency_pattern}
    Step  4  cat loop file info  path=${In_voltage0_path}  pre=${In_voltage_scale_available}  part=1  passpattern=${In_voltage_scale_available_pattern}
    Step  5  cat loop file info  path=${In_voltage0_path}  pre=${sampling_frequency_available}  part=1  passpattern=${sampling_frequency_available_pattern}

BSP_10.2.10.1_check_i2cfpga_Card_Present_Status
    [Documentation]  This test is to check i2cfpga card present status.
    [Tags]  BSP_10.2.10.1_check_i2cfpga_Card_Present_Status  fenghuang
    [Timeout]  60 min 00 seconds
    [Setup]  boot into diag os mode
    Step  1   check i2cfpga card present status

BSP_10.2.10.2_I2C_FPGA_EEPROM_Protect_Test
    [Documentation]  This test is to read and set  i2c fpga card eeprom write protect status.
    [Tags]  BSP_10.2.10.2_I2C_FPGA_EEPROM_Protect_Test  fenghuangv2
    [Timeout]  6 min 00 seconds
    [Setup]  boot into diag os mode
    Step  1  cat loop file info  path=${device_8_0060_path}  pre=${i2cfpga_eeprom_write_protect}  part=1  passpattern=${i2cfpga_eeprom_write_protect_passpattern1}
    Step  2  echo value to file  path=${device_8_0060_path}  file=${i2cfpga_eeprom_write_protect}  value=${i2cfpga_eeprom_write_protect_value}
    Step  3  cat loop file info  path=${device_8_0060_path}  pre=${i2cfpga_eeprom_write_protect}  part=1  passpattern=${i2cfpga_eeprom_write_protect_passpattern2}
    Step  4  echo value to file  path=${device_8_0060_path}  file=${i2cfpga_eeprom_write_protect}  value=${i2cfpga_eeprom_write_protect_default}
    Step  5  cat loop file info  path=${device_8_0060_path}  pre=${i2cfpga_eeprom_write_protect}  part=1  passpattern=${i2cfpga_eeprom_write_protect_passpattern1}

BSP_10.2.10.3_check_i2cfpga_lm75_Interrupt_Status
    [Documentation]  This test is to check i2cfpga lm75 interrupt status.
    [Tags]  BSP_10.2.10.3_check_i2cfpga_lm75_Interrupt_Status  fenghuangv2
    [Timeout]  60 min 00 seconds
    [Setup]  boot into diag os mode
    Step  1   check i2cfpga lm75 interrupt status

#BSP_TC123_In_voltage0_raw_Test
#    [Documentation]  this test is to check i2c in_voltage0_raw
#    [Tags]     BSP_TC123_In_voltage0_raw_Test  fenghuangv2
#    [Timeout]  1 min 00 seconds
#    [Setup]  boot into diag os mode
#    Step  1  cat loop file info  path=${In_voltage0_path}  pre=${In_voltage0_raw}  part=1  passpattern=${In_voltage0_raw_pattern}
#
#BSP_TC124_In_voltage0_scale_Test
#    [Documentation]  this test is to check i2c in_voltage0_scale
#    [Tags]     BSP_TC124_In_voltage0_scale_Test  fenghuangv2
#    [Timeout]  1 min 00 seconds
#    [Setup]  boot into diag os mode
#    Step  1  cat loop file info  path=${In_voltage0_path}  pre=${In_voltage0_scale}  part=1  passpattern=${In_voltage0_scale_pattern}
#
#BSP_TC125_In_voltage_sampling_frequency_Test
#    [Documentation]  this test is to check i2c in_voltage_sampling_frequency
#    [Tags]     BSP_TC125_In_voltage_sampling_frequency_Test  fenghuangv2
#    [Timeout]  1 min 00 seconds
#    [Setup]  boot into diag os mode
#    Step  1  cat loop file info  path=${In_voltage0_path}  pre=${In_voltage_sampling_frequency}  part=1  passpattern=${In_voltage_sampling_frequency_pattern}
#
#BSP_TC126_In_voltage_scale_available_Test
#    [Documentation]  this test is to check i2c in_voltage_scale_available
#    [Tags]     BSP_TC126_In_voltage_scale_available_Test  fenghuangv2
#    [Timeout]  1 min 00 seconds
#    [Setup]  boot into diag os mode
#    Step  1  cat loop file info  path=${In_voltage0_path}  pre=${In_voltage_scale_available}  part=1  passpattern=${In_voltage_scale_available_pattern}
#
#BSP_TC127_Sampling_frequency_available_Test
#    [Documentation]  this test is to check i2c sampling_frequency_available
#    [Tags]     BSP_TC127_Sampling_frequency_available_Test  fenghuangv2
#    [Timeout]  1 min 00 seconds
#    [Setup]  boot into diag os mode
#    Step  1  cat loop file info  path=${In_voltage0_path}  pre=${sampling_frequency_available}  part=1  passpattern=${sampling_frequency_available_pattern}

BSP_10.2.11.1.1_Accel_I2C_FPGA_Version_Test
    [Documentation]  this test is to the current firmware version of Accel-I2C-FPGA
    [Tags]     BSP_10.2.11.1.1_Accel_I2C_FPGA_Version_Test  fenghuangv2
    [Timeout]  1 min 00 seconds
    [Setup]  boot into diag os mode
    Step  1  cat loop file info  path=${accel_i2c_path}  pre=${accel_i2c_fpga}  part=1  passpattern=${i2c_fpga_version_pattern}


BSP_10.2.11.1.2_Accel_I2C_FPGA_Board_Version_Test
    [Documentation]  this test is to check the board version of Accel-I2C-FPGA
    [Tags]     BSP_10.2.11.1.2_Accel_I2C_FPGA_Board_Version_Test  fenghuangv2
    [Timeout]  1 min 00 seconds
    [Setup]  boot into diag os mode
    Step  1  cat loop file info  path=${accel_i2c_path}  pre=${accel_i2c_board_version}  part=1  passpattern=${i2c_board_version_pattern}


BSP_10.2.11.1.5_Accel_I2C_raw_access_Test
    [Documentation]  this test is to check access Accel-I2C register Ensure
    [Tags]     BSP_10.2.11.1.5_Accel_I2C_raw_access_Test  fenghuangv2
    [Timeout]  1 min 00 seconds
    [Setup]  boot into diag os mode
    Step  1  cat loop file info  path=${accel_i2c_path}  pre=${accel_i2c_raw_access_data}  part=1  passpattern=${raw_access_data_pattern1}
    Step  2  cat loop file info  path=${accel_i2c_path}  pre=${accel_i2c_raw_access_addr}  part=1  passpattern=${raw_access_addr_pattern1}
    Step  3  echo value to file  path=${accel_i2c_path}  file=${accel_i2c_raw_access_data}  value=${raw_access_data_value1}
    Step  4  echo value to file  path=${accel_i2c_path}  file=${accel_i2c_raw_access_addr}  value=${raw_access_addr_value1}
    Step  5  cat loop file info  path=${accel_i2c_path}  pre=${accel_i2c_raw_access_data}  part=1  passpattern=${raw_access_data_pattern2}
    Step  6  cat loop file info  path=${accel_i2c_path}  pre=${accel_i2c_raw_access_addr}  part=1  passpattern=${raw_access_addr_pattern2}
    Step  7  echo value to file  path=${accel_i2c_path}  file=${accel_i2c_raw_access_data}  value=${raw_access_data_value2}
    Step  8  echo value to file  path=${accel_i2c_path}  file=${accel_i2c_raw_access_addr}  value=${raw_access_addr_value2}
    Step  9  cat loop file info  path=${accel_i2c_path}  pre=${accel_i2c_raw_access_data}  part=1  passpattern=${raw_access_data_pattern1}
    Step  10  cat loop file info  path=${accel_i2c_path}  pre=${accel_i2c_raw_access_addr}  part=1  passpattern=${raw_access_addr_pattern1}


BSP_10.2.11.1.6_Accel_I2C_Scratch_Test
    [Documentation]  this test is to check that read/set the Accel-I2C Scratch
    [Tags]     BSP_10.2.11.1.6_Accel_I2C_Scratch_Test  fenghuangv2
    [Timeout]  1 min 00 seconds
    [Setup]  boot into diag os mode
    Step  1  cat loop file info  path=${accel_i2c_path}  pre=${accel_i2c_scratch}  part=1  passpattern=${i2c_scratch_pattern1}
    Step  2  echo value to file  path=${accel_i2c_path}  file=${accel_i2c_scratch}  value=${i2c_scratch_value1}
    Step  3  cat loop file info  path=${accel_i2c_path}  pre=${accel_i2c_scratch}  part=1  passpattern=${i2c_scratch_pattern2}
    Step  4  echo value to file  path=${accel_i2c_path}  file=${accel_i2c_scratch}  value=${i2c_scratch_value2}
    Step  5  cat loop file info  path=${accel_i2c_path}  pre=${accel_i2c_scratch}  part=1  passpattern=${i2c_scratch_pattern1}


BSP_10.2.11.2.1_Port_I2C_Profile_Select_Test
    [Documentation]  this test is to check that read/set the speed profiles
    [Tags]     BSP_10.2.11.2.1_Port_I2C_Profile_Select_Test  fenghuangv2
    [Timeout]  5 min 00 seconds
    [Setup]  boot into diag os mode
    Step  1  cat loop file info  path=${port_file_path}  pre=${i2c_profile_select_pre}  suf=${i2c_profile_select_suf}  passpattern=${i2c_profile_select_pattern1}
    Step  2  modify reset file value  path=${port_file_path}  pre=${i2c_profile_select_pre}  suf=${i2c_profile_select_suf}  value=${i2c_profile_select_value1}
    Step  3  cat loop file info  path=${port_file_path}  pre=${i2c_profile_select_pre}  suf=${i2c_profile_select_suf}  passpattern=${i2c_profile_select_pattern2}
    Step  4  modify reset file value  path=${port_file_path}  pre=${i2c_profile_select_pre}  suf=${i2c_profile_select_suf}  value=${i2c_profile_select_value2}
    Step  5  cat loop file info  path=${port_file_path}  pre=${i2c_profile_select_pre}  suf=${i2c_profile_select_suf}  passpattern=${i2c_profile_select_pattern1}


BSP_10.2.11.2.2_Port_I2C_Profile_Speed_Test
    [Documentation]  this test is to check that read/set the i2c profile speed
    [Tags]     BSP_10.2.11.2.2_Port_I2C_Profile_Speed_Test  fenghuangv2  
    [Timeout]  60 min 00 seconds
    [Setup]  boot into DiagOS mode
    Step  1  profile speed test new


BSP_10.2.11.2.3_Port_I2C_9_clock_Test
    [Documentation]  this test is to check that writing 1 initiates a 9 clk I2C reset sequence
    [Tags]     BSP_10.2.11.2.3_Port_I2C_9_clock_Test  fenghuangv2
    [Timeout]  1 min 00 seconds
    [Setup]  boot into diag os mode
    Step  1  modify reset file value  path=${port_file_path}  pre=${i2c_9_clock_pre}  suf=${i2c_9_clock_suf}  value=${i2c_9_clock_value}  part=32


BSP_10.2.11.2.4_Port_I2C_master_Reset_Test
    [Documentation]  this test is to check that reset i2c master controller
    [Tags]     BSP_10.2.11.2.4_Port_I2C_master_Reset_Test  fenghuangv2
    [Timeout]  5 min 00 seconds
    [Setup]  boot into diag os mode
    Step  1  cat loop file info  path=${port_file_path}  pre=${i2c_master_pre}  suf=${i2c_master_suf}  part=32  passpattern=${i2c_master_pattern1}
    Step  2  modify reset file value  path=${port_file_path}  pre=${i2c_master_pre}  suf=${i2c_master_suf}  value=${i2c_master_value1}  part=32
    Step  3  cat loop file info  path=${port_file_path}  pre=${i2c_master_pre}  suf=${i2c_master_suf}  part=32  passpattern=${i2c_master_pattern1}
    Step  4  modify reset file value  path=${port_file_path}  pre=${i2c_master_pre}  suf=${i2c_master_suf}  value=${i2c_master_value2}  part=32
    Step  5  cat loop file info  path=${port_file_path}  pre=${i2c_master_pre}  suf=${i2c_master_suf}  part=32  passpattern=${i2c_master_pattern1}

BSP_10.2.11.3.2_Port_Module_Lpmod_Test
    [Documentation]  This test is to check the optical module interrupt mask status
    [Tags]     BSP_10.2.11.3.2_Port_Module_Lpmod_Test  fenghuangv2
    [Timeout]  5 min 00 seconds
    Step  1  cat loop file info  path=${interrupt_port_file_path}  pre=${lpmode_pre}  suf=${lpmode_suf}  passpattern=${common_test_pattern2}
    Step  2  modify reset file value  path=${interrupt_port_file_path}  pre=${lpmode_pre}  suf=${lpmode_suf}  value=${modify_file_value2}
    Step  3  cat loop file info  path=${interrupt_port_file_path}  pre=${lpmode_pre}  suf=${lpmode_suf}  passpattern=${common_test_pattern1}
    Step  4  modify reset file value  path=${interrupt_port_file_path}  pre=${lpmode_pre}  suf=${lpmode_suf}  value=${modify_file_value1}
    Step  5  cat loop file info  path=${interrupt_port_file_path}  pre=${lpmode_pre}  suf=${lpmode_suf}  passpattern=${common_test_pattern2}

BSP_10.2.12.1.6_check_Read_Write_Scratchpad_Register
    [Documentation]  This test is to check Read write scratch pad register
    [Tags]  BSP_10.2.12.1.6_check_Read_Write_Scratchpad_Register  fenghuangv2
    [Timeout]  60 min 00 seconds
    [Setup]  boot into diag os mode
    Step  1   check read write scratchpad register


BSP_10.2.12.2.1_Port_I2C_Profile_Select_Test
    [Documentation]  this test is to check that read/set the speed profiles
    [Tags]     BSP_10.2.12.2.1_Port_I2C_Profile_Select_Test  fenghuangv2  1PPS
    [Timeout]  5 min 00 seconds
    [Setup]  boot into Onie Rescue Mode
    Step  1  cat loop file info  path=${port_file_path}  pre=${i2c_profile_select_pre}  suf=${i2c_profile_select_suf}  passpattern=${i2c_profile_select_pattern1}
    Step  2  modify reset file value  path=${port_file_path}  pre=${i2c_profile_select_pre}  suf=${i2c_profile_select_suf}  value=${i2c_profile_select_value1}
    Step  3  cat loop file info  path=${port_file_path}  pre=${i2c_profile_select_pre}  suf=${i2c_profile_select_suf}  passpattern=${i2c_profile_select_pattern2}
    Step  4  modify reset file value  path=${port_file_path}  pre=${i2c_profile_select_pre}  suf=${i2c_profile_select_suf}  value=${i2c_profile_select_value2}
    Step  5  cat loop file info  path=${port_file_path}  pre=${i2c_profile_select_pre}  suf=${i2c_profile_select_suf}  passpattern=${i2c_profile_select_pattern1}



BSP_10.2.13_check_RsenseValue
    [Documentation]  This test is to check Rsense value
    [Tags]  BSP_10.2.13_check_RsenseValue  fenghuangv2
    [Timeout]  60 min 00 seconds
    [Setup]  boot into diag os mode
    Step  1  execute check dict  device=DUT  cmd=${rsense_cmd}  patterns_dict=${rsense_pattern}



BSP_10.2.12.1.1_1PPS-I2C-FPGA_Version_Test
    [Documentation]  The purpose of this test is to the current firmware version of 1PPS-I2C-FPGA. Ensure that the version is correct.
    [Tags]  BSP_10.2.12.1.1_1PPS-I2C-FPGA_Version_Test   fenghuangv2  test
    [Timeout]  5 min 00 seconds
    [Setup]  boot Into Onie Install Mode
     Step  1  check current version


BSP_10.2.12.1.2_1PPS-I2C-FPGA_Board_Version_Test
    [Documentation]  The purpose of this test is to check the board version of 1PPS -I2C-FPGA. Ensure that the board version is correct.
    [Tags]  BSP_10.2.12.1.2_1PPS-I2C-FPGA_Board_Version_Test   fenghuangv2  test
    [Timeout]  5 min 00 seconds
    [Setup]  boot Into Onie Install Mode
     Step  1  check current board version

BSP_10.2.12.1.3_1PPS-I2C-FPGA_PCB_Version_Test
    [Documentation]  The purpose of this test is to check the pcb version of 1PPS-I2C-FPGA. Ensure that the pcb version is correct.
    [Tags]  BSP_10.2.12.1.3_1PPS-I2C-FPGA_PCB_Version_Test   fenghuangv2  test
    [Timeout]  5 min 00 seconds
    [Setup]  boot Into Onie Install Mode
     Step  1  check pcb version


BSP_10.2.12.1.4_PPS-I2C-FPGA_Image_Version_Test
    [Documentation]  The purpose of this test is to check the image version of 1PPS-I2C-FPGA. Ensure that the imame version is correct.
    [Tags]  BSP_10.2.12.1.4_PPS-I2C-FPGA_Image_Version_Test   fenghuangv2  test
    [Timeout]  5 min 00 seconds
    [Setup]  boot Into Onie Install Mode
     Step  1  check current image version



BSP_10.2.12.1.5_1PPS-I2C_raw_access_Test
    [Documentation]  The purpose of this test is to check access 1PPS-I2C register and ensure that access 1PPS-I2C is success.
    [Tags]  BSP_10.2.12.1.5_1PPS-I2C_raw_access_Test   fenghuangv2  test
    [Timeout]  5 min 00 seconds
    [Setup]  boot Into Onie Install Mode
     Step  1  check raw access info  ${raw_access_data}  ${raw_access_addr}
     Step  2  modify sysfs note  ${addr_path}  ${value2}
     Step  3  modify sysfs note  ${data_path}  ${new_value1}
     Step  4  check raw access info  ${value1}  ${new_value2}
     Step  5  modify sysfs note  ${addr_path}  ${new_raw_access_addr}
     Step  6  modify sysfs note  ${data_path}  ${new_raw_access_data}
     Step  7  check raw access info  ${raw_access_data}  ${raw_access_addr}




BSP_10.2.11.1.3_Accel-I2C-FPGA_PCB_Version_Test
   [Documentation]  The purpose of this test is to check the board version of Accel-I2C-FPGA. Ensure that the board version is correct.
   [Tags]   BSP_10.2.11.1.3_Accel-I2C-FPGA_PCB_Version_Test  fenghuangv2  test1
   [Timeout]  5 min 00 seconds
   [Setup]  boot Into Onie Install Mode
   Step  1  check accel pcb version



BSP_10.2.11.1.4_Accel-I2C-FPGA_Image_Version_Test
   [Documentation]  The purpose of this test is to check the board version of Accel-I2C-FPGA. Ensure that the board version is correct.
   [Tags]   BSP_10.2.11.1.3_Accel-I2C-FPGA_Image_Version_Test  fenghuangv2  tes
   [Timeout]  5 min 00 seconds
    Step  1  check accel image version




BSP_10.2.11.1.5_Accel-I2C_raw_access_Test
    [Documentation]  The purpose of this test is to check access 1PPS-I2C register and ensure that access 1PPS-I2C is success.
    [Tags]  BSP_10.2.11.1.5_Accel-I2C_raw_access_Test   fenghuangv2  test1
    [Timeout]  5 min 00 seconds
    [Setup]  boot Into Onie Install Mode
     Step  1  check accel raw access info  ${accel_raw_data}  ${raw_access_addr}
     Step  2  modify sysfs note  ${addr_path1}  ${value2}
     Step  3  modify sysfs note  ${data_path1}  ${new_value1}
     Step  4  check accel raw access info  ${value1}  ${new_value2}
     Step  5  modify sysfs note  ${addr_path1}  ${new_raw_access_addr}
     Step  6  modify sysfs note  ${data_path1}  ${accel_new_data}
     Step  7  check accel raw access info  ${accel_raw_data}  ${raw_access_addr}



BSP_10.2.12.2.3_Port_I2C_9_Clock_Test
    [Documentation]  The purpose of this test is to check that writing 1 initiates a 9 clk I2C reset sequence. .
    [Tags]  BSP_10.2.12.2.3_Port_I2C_9_Clock_Test  fenghuangv2  test1
    [Timeout]  5 min 00 seconds
    [Setup]   boot Into Onie Install Mode
    Step  1   set i2c profile speed



BSP_10.2.12.2.4_Port_I2C_Master_Reset_Test
    [Documentation]  The purpose of this test is to check that reset i2c master controller.
    [Tags]  BSP_10.2.12.2.4_Port_I2C_Master_Reset_Test  fenghuangv2  test2
    [Setup]   boot Into Onie Install Mode
    [Timeout]  5 min 00 seconds
    Step  1   master reset test



#BSP_TC237_Uboot_Update_Test_via_Flash_On_Onie
    #[Documentation]  This test is to check uboot update test via flash on onie
    #[Tags]     BSP_TC237_Uboot_Update_Test_via_Flash_On_Onie  fenghuang
    #[Timeout]  60 min 00 seconds
    #[Setup]  boot Into Onie Rescue Mode
    #Step  1  ifconfig and ping address  ${tc238_ipaddr}
    #Step  2  tftp uboot image  ${tc238_serverip}  ${uboot_new_image}
    #Step  3  cat dev mtd and erase mtd0
    #Step  4  upgrade onie  ${uboot_new_image}
    #Step  5  power Cycle To Onie Rescue Mode
    #Step  6  get versions to check onie  ${get_versions_cmd}

#BSP_TC238_Uboot_Installation_Test
    #[Documentation]  This test is to check uboot installation test
    #[Tags]     BSP_TC238_Uboot_Installation_Test  fenghuang
    #[Timeout]  60 min 00 seconds
    #[Setup]  boot Into Uboot
    #Step  1  set ipaddr and server  ${tc238_ipaddr}  ${tc238_serverip}
    #Step  2  run bootupd
    #Step  3  boot Into Uboot
    #Step  4  boot Into Onie Rescue Mode

#BSP_TC249_check_Read_Write_Scratchpad_Register
#    [Documentation]  This test is to check Read write scratch pad register
#    [Tags]  BSP_TC249_check_Read_Write_Scratchpad_Register  fenghuang
#    [Timeout]  60 min 00 seconds
#    [Setup]  boot into diag os mode
#    Step  1   check read write scratchpad register

BSP_10.1.4_Fault_Logger_Test_Dump/Pause/Reset
    [Documentation]  This test is to ensure that log function is correct.
    [Tags]  BSP_10.1.4_Fault_Logger_Test_Dump/Pause/Reset  fenghuang
    [Setup]  boot Into Onie Rescue Mode
    Step  1   check Fault Logger Function  ${fault_logger_path}  ${fault_logger_cmd}

BSP_10.2.3.3_Busbar_Board_EEPROM_Test
    [Documentation]  This test is to ensure that busbar EEPROM is correct.
    [Tags]  BSP_10.2.3.3_Busbar_Board_EEPROM_Test  fenghuang
    [Setup]  boot into diag os mode
    Step  1   busbar Board Eeprom Test

BSP_10.2.3.4_I2CFPGA_Board_EEPROM_Test
    [Documentation]  This test is to ensure that I2CFPGA EEPROM is correct.
    [Tags]  BSP_10.2.3.4_I2CFPGA_Board_EEPROM_Test  fenghuang
    [Setup]  boot into diag os mode
    Step  1   I2cfpga Board Eeprom Test

BSP_10.2.11.3.1_Port_Module_Interrupt_Mask_Test
    [Documentation]  This test is to ensure that the optical module present status can be shown correctly.
    [Tags]  BSP_10.2.11.3.1_Port_Module_Interrupt_Mask_Test  fenghuang
    [Setup]  boot into diag os mode
    Step  1   Port Module Interrupt Mask Test

BSP_10.2.14_ASC10_EEPROM_and_CRC_sysfs_node_Test
    [Documentation]  This test is to check asc10 eeprom and crc sysfs node is correct.
    [Tags]  BSP_10.2.14_ASC10_EEPROM_and_CRC_sysfs_node_Test  fenghuang
    [Setup]  boot Into Onie Rescue Mode
    Step  1   Check Asc10 Eeprom And Crc  ${fw_cmd}  ${eeprom_cmd}  ${cat_crc_cmd}

*** Keywords ***
DiagOS Connect Device
    DiagOSConnect

DiagOS Disconnect Device
    DiagOSDisconnect



