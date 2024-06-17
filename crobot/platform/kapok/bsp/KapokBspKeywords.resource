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
Library         Collections

Resource        CommonKeywords.resource
Resource        KapokCommonKeywords.resource
Resource        KapokBspKeywords.resource


*** Keywords ***
show BSP Driver installed version
    [Documentation]  show BSP Driver installed version
    [Arguments]
    ...  ${command}=${bsp_driver_show_version_command}
    ...  ${console}=${diagos_mode}
    ...  ${sec}=60
    ...  ${pattern}=${bsp_driver_version_pattern}

    execute command and verify with a pattern
    ...  path=${EMPTY}
    ...  command=${command}
    ...  console=${console}
    ...  sec=${sec}
    ...  pattern=${pattern}

    set test variable  ${bsp_installed_driver_version}  ${match}[bsp_installed_driver_version]


reinstall BSP Driver
    [Documentation]  Remove & install BSP Driver (if needed for outdated version)
    [Arguments]
    ...  ${path}=${bsp_driver_path_to_install}
    ...  ${console}=${diagos_mode}
    ...  ${sec}=15

    # No update BSP driver if it already up-to-date
    show BSP Driver installed version
    ${is_bsp_driver_up_to_date}=  run keyword and return status
    ...  should be equal as strings  ${bsp_installed_driver_version}  ${bsp_driver_new_version}
    ...  msg=The installed BSP Driver does not match (outdated version), needed to re-install BSP Driver!
    return from keyword if  ${is_bsp_driver_up_to_date}

    # Delete BSP driver folder, create new one and go to the folder
    remove file/folder  console=${console}  file=${path}
    create directory  console=${console}  dir=${path}
    change directory  console=${console}  dir=${path}

    # Download BSP Driver and decompress tar.xz to tar
    BusyBox TFTP get file
    ...  console=${console}
    ...  server=${tftp_server_ipv4}
    ...  file=${bsp_driver_file}
    decompress xz file
    ...  console=${console}
    ...  file=${bsp_driver_file_name_only}.tar.xz

    # Decompress tar to the folder
    decompress tar file
    ...  console=${console}
    ...  file=${bsp_driver_file_name_only}.tar -C .

    force unload/load all kernel driver matched with *.ko file  sec=${sec}


force unload/load all kernel driver matched with *.ko file
    [Documentation]  Pre-condition before run all test-cases
    [Arguments]
    ...  ${path}=${bsp_driver_path_to_install}
    ...  ${console}=${diagos_mode}
    ...  ${sec}=15

    # Unload kernel module by *.ko file(s)
    unload kernel module matched *.ko file  console=${console}  path=${path}

    # Go to the folder, install it and check all the module(s) already installed/loaded
    change directory  console=${console}  dir=${path}
    execute command and set test variable
    ...  command=./install.sh
    ...  console=${console}
    ...  sec=${sec}
    #The install.sh script already contains the insmod operation. There is no need to repeat this operation here
    #FOR  ${key}  ${value}  IN  &{kmod_file_name_list}
    #    insert kernel module
    #    ...  console=${console}
    #    ...  module=${value}
    #    ...  exit_code_pattern=(?m)^(?P<exit_code>\\d)$
    #    Run Keyword If  ${exit_code} != 0  search for a pattern  # Some module is not in the install.sh script!
    #    ...  text=${insmod_text}
    #    ...  pattern=(?m)^(?P<PASS>insmod.*ERROR.*File exists)$
    #END


set logger dump baud rate to 115200 kbps
    [Documentation]  Setting logger dump baud rate to 115200 kbps
    [Arguments]
    ...  ${console}=${diagos_mode}

    execute command and set test variable
    ...  console=${console}
    ...  command=i2cset -y -f 15 0x60 0x40 0x43
    verify exit code

fhv2 set logger dump baud rate to 115200 kbps
    [Documentation]  Setting logger dump baud rate to 115200 kbps
    [Arguments]
    ...  ${console}=${diagos_mode}

    execute command and set test variable
    ...  console=${console}
    ...  command=i2cset -y -f 8 0x60 0x40 0x43
    verify exit code

simple read logger dump
    [Documentation]  Simple read logger dump to see the device is work
    [Arguments]
    ...  ${console}=${diagos_mode}

    execute command and verify with a pattern
    ...  console=${console}
    ...  command=dd if=console_logger_dump bs=128 count=1 2>/dev/null | hexdump -C
    ...  path=${i2c_devices_tree}[LOGGER_DUMP][PATH]
    ...  pattern=(?P<PASS>${EMPTY})
    ...  msg=Can not read LOGGER DUMP!${\n}The device may not load properly driver/or not successful


verify logger dump reset functionality
    [Documentation]  Reset the logger dump and put new message to verify it
    [Arguments]
    ...  ${console}=${diagos_mode}

    execute command and verify with a pattern
    ...  console=${console}
    ...  command=(echo 1 > console_logger_reset && echo "log reset" && dd if=console_logger_dump bs=128 count=1 2>/dev/null | hexdump -C)
    ...  path=${i2c_devices_tree}[LOGGER_DUMP][PATH]
    ...  pattern=(?m)^00000000[ \\w]+\\|(?P<PASS>log reset).*\\|
    ...  msg=Failed to read logger dump to verify reset functionality


verify logger dump pause functionality
    [Documentation]  Pause the logger dump and verify it not log
    [Arguments]
    ...  ${console}=${diagos_mode}

    ${status}=  Run Keyword And Return Status  execute command and verify with a pattern
    ...  console=${console}
    # Not pause logger, reset logger, put a new message (log me) to logger and dump to see the message was loagged to logger
    # Pause logger, try to put a new message (log puased) to logger and dump and expected to not see the message
    ...  command=(echo 0 > console_logger_pause && echo 1 > console_logger_reset && echo log me && dd if=console_logger_dump bs=128 count=1 2>/dev/null | hexdump -C && echo 1 > console_logger_pause && echo log paused && dd if=console_logger_dump bs=128 count=1 2>/dev/null | hexdump -C)
    ...  path=${i2c_devices_tree}[LOGGER_DUMP][PATH]
    ...  pattern=(?m)^[\\da-fA-F]+[ \\w]+\\|(?P<FAIL>log paused).*\\|
    # Fail if found above pattern
    Run Keyword If  '${status}' == 'True'
    ...  Fail  Failed to verify logger pause functionality


verify all attributes on the directory
    [Documentation]  verify given all attributes on the directory
    [Arguments]
    ...  ${console}
    ...  ${path}
    ...  ${attrs}
    ...  ${msg}

    run keyword if  '${path}' != '${EMPTY}'
    ...  change directory  console=${console}  dir=${path}

    &{fs_attrs}  Create Dictionary

    FOR  ${attribute name}  ${its expected pattern}  IN  &{attrs}
        execute command and set test variable
        ...  console=${console}
        ...  command=cat ${attribute name}
        verify exit code
        search for a pattern
        ...  text=${text}
        ...  pattern=${its expected pattern}
        ...  msg=${msg}${\n}for its attribute name "${attribute name}"
        Set To Dictionary  ${fs_attrs}  ${attribute name}=${match}[${attribute name}]
    END

    set test variable  &{fs_attrs}


verify all LM75 devices for its all file system attributes
    [Documentation]  Verify given LM75 devices for all its attributes
    [Arguments]
    ...  ${console}=${diagos_mode}

    FOR  ${device name}  ${its attributes}  IN  &{i2c_lm75_devices}
        verify all attributes on the directory
        ...  console=${console}
        ...  path=${its attributes}[PATH]
        ...  attrs=${its attributes}[ATTRS]
        ...  msg=Failed to verify I2C device name "${device name}"${\n}on path "${its attributes}[PATH]"
    END


read FAN input by file system attribute
    [Documentation]  Read all CD8200 FAN input by file system attribute
    [Arguments]
    ...  ${console}=${diagos_mode}
    ...  ${path}=${i2c_devices_tree}[CD8200_FAN_CPLD][PATH]
    ...  ${attrs}=${i2c_cd8200_fan_cpld_input}

    verify all attributes on the directory
    ...  console=${console}
    ...  path=${path}
    ...  attrs=${attrs}
    ...  msg=Failed to verify I2C device name "CD8200_FAN_CPLD"${\n}on path "${path}\[PATH]"
    set test variable  &{fs_attrs_fan_inputs}  &{fs_attrs}


read FAN input by diagtool
    [Documentation]  Read all CD8200 FAN input by diagtool
    [Arguments]
    ...  ${console}=${diagos_mode}
    ...  ${path}=${diag_tools_path}

    &{diagtool_fan_inputs}  Create Dictionary

    FOR  ${index}  ${key}  ${value}  IN ENUMERATE  &{i2c_cd8200_fan_cpld_input}
        ${fan_id} =  Evaluate  ${index} + 1
        execute command and verify with a pattern
        ...  console=${console}
        ...  command=(${diag_export_env}./cel-fan-test -r -t speed -d ${fan_id})
        ...  path=${path}
        ...  pattern=[ \\t]*Reading[ \\t]fan-\\d[ \\t]+\\w+,[ \\t]+speed:[ \\t]+(?P<fan${fan_id}_input>\\d+) .*:[ \\t]\\w+
        ...  msg=Not found the FAN speed/input!
        Set To Dictionary  ${diagtool_fan_inputs}  ${key}=${match}[${key}]
    END

    set test variable  &{diagtool_fan_inputs}


compare FAN input
    [Documentation]  Compare all FAN inputs for ile system attribute and diagtool
    [Arguments]
    ...  ${fs_attrs_inputs}=${fs_attrs_fan_inputs}
    ...  ${diagtool_inputs}=${diagtool_fan_inputs}

    compare two dictionaries with matched key
    ...  original=${fs_attrs_inputs}
    ...  compare=${diagtool_inputs}
    ...  msg=Failed to compare FAN input for file system attribute vs diagtool


simple check access FAN raw data attribute
    [Documentation]  Simple cat to read FAN raw data attribute
    [Arguments]
    ...  ${console}=${diagos_mode}
    ...  ${path}=${i2c_devices_tree}[CD8200_FAN_CPLD][PATH]
    ...  ${pattern}=${i2c_cd8200_fan_cpld_raw}[raw_access_data]

    execute command and verify with a pattern
    ...  console=${console}
    ...  command=cat raw_access_data
    ...  path=${path}
    ...  pattern=${pattern}


write data to raw access address attribute
    [Documentation]  To ensure the file system attribute for address is writable
    [Arguments]
    ...  ${console}=${diagos_mode}
    ...  ${path}=${i2c_devices_tree}[CD8200_FAN_CPLD][PATH]
    ...  ${address}=0x02 0x00

    execute command and verify exit code
    ...  console=${console}
    ...  command=echo ${address} > raw_access_addr
    ...  path=${path}


write data to raw access data attribute
    [Documentation]  To ensure the file system attribute for raw access data is writable
    [Arguments]
    ...  ${console}=${diagos_mode}
    ...  ${path}=
    ...  ${data}=

    execute command and verify exit code
    ...  console=${console}
    ...  command=echo ${data} > raw_access_data
    ...  path=${path}


read raw access data attribute
    [Documentation]  Simple read file system attribute raw access data with no error
    [Arguments]
    ...  ${console}=${diagos_mode}
    ...  ${path}=${i2c_devices_tree}[CD8200_FAN_CPLD][PATH]

    execute command and verify exit code
    ...  console=${console}
    ...  command=cat raw_access_data
    ...  path=${path}


read raw access address attribute
    [Documentation]  Simple read file system attribute raw access address with no error
    [Arguments]
    ...  ${console}=${diagos_mode}
    ...  ${path}=${i2c_devices_tree}[CD8200_FAN_CPLD][PATH]
    ...  ${pattern}=${EMPTY}

    execute command and verify with a pattern
    ...  console=${console}
    ...  command=cat raw_access_addr
    ...  path=${path}
    ...  pattern=${pattern}


verify all PSU1 file system attributes
    [Documentation]  To ensure no error to read any PSU1's attributes
    [Arguments]
    ...  ${console}=${diagos_mode}

    verify all attributes on the directory
    ...  console=${console}
    ...  path=${i2c_devices_tree}[PSU1_DPS_1500][PATH]
    ...  attrs=${i2c_devices_tree}[PSU1_DPS_1500][ATTRS]
    ...  msg=Failed to verify I2C device name "PSU1_DPS_1500"${\n}on path "${i2c_devices_tree}[PSU1_DPS_1500][PATH]"
    set test variable  &{psu1_fs_attrs}  &{fs_attrs}


verify all PSU2 file system attributes
    [Documentation]  To ensure no error to read any PSU2's attributes
    [Arguments]
    ...  ${console}=${diagos_mode}

    verify all attributes on the directory
    ...  console=${console}
    ...  path=${i2c_devices_tree}[PSU2_DPS_1500][PATH]
    ...  attrs=${i2c_devices_tree}[PSU2_DPS_1500][ATTRS]
    ...  msg=Failed to verify I2C device name "PSU2_DPS_1500"${\n}on path "${i2c_devices_tree}[PSU2_DPS_1500][PATH]"
    set test variable  &{psu2_fs_attrs}  &{fs_attrs}


verify all CDCD/IR35215 devices for its all file system attributes
    [Documentation]  Verify given CDCD/IR35215 devices for all its attributes
    [Arguments]
    ...  ${console}=${diagos_mode}

    FOR  ${index}  ${device name}  ${its attributes}  IN ENUMERATE  &{i2c_ir35215_devices}
        ${dev_id} =  Evaluate  ${index} + 1
        verify all attributes on the directory
        ...  console=${console}
        ...  path=${its attributes}[PATH]
        ...  attrs=${its attributes}[ATTRS]
        ...  msg=Failed to verify I2C device name "${device name}"${\n}on path "${its attributes}[PATH]"
        set test variable  &{cdcd${dev_id}_fs_attrs}  &{fs_attrs}
    END


read led enable attribute
    [Documentation]  Read CPLD 2/3's led enable attribute
    [Arguments]
    ...  ${console}=${diagos_mode}
    ...  ${path}=${EMPTY}

    execute command and verify exit code
    ...  console=${console}
    ...  command=cat led_enable
    ...  path=${path}


write to led enable attribute
    [Documentation]  Write to CPLD 2/3's led enable attribute
    [Arguments]
    ...  ${console}=${diagos_mode}
    ...  ${path}=${EMPTY}
    ...  ${enable}=1

    execute command and verify exit code
    ...  console=${console}
    ...  command=echo ${enable} > led_enable
    ...  path=${path}


read led color attribute
    [Documentation]  Read CPLD 2/3's led color attribute
    [Arguments]
    ...  ${console}=${diagos_mode}
    ...  ${path}=${EMPTY}

    execute command and verify exit code
    ...  console=${console}
    ...  command=cat led_color
    ...  path=${path}


write color to led color attribute
    [Documentation]  write CPLD 2/3's color to led color attribute
    [Arguments]
    ...  ${console}=${diagos_mode}
    ...  ${path}=${EMPTY}
    ...  ${color}=off

    execute command and verify exit code
    ...  console=${console}
    ...  command=echo ${color} > led_color
    ...  path=${path}


read board version
    [Documentation]  Simple read board version
    [Arguments]
    ...  ${console}=${diagos_mode}
    ...  ${path}=${i2c_devices_tree}[LOGGER_DUMP][PATH]

    execute command and verify exit code
    ...  console=${console}
    ...  command=cat board_version
    ...  path=${path}


disable fan watchdog by file system attribute
    [Documentation]  Write 0 to fan watchdog enable on file system attribute
    [Arguments]
    ...  ${console}=${diagos_mode}
    ...  ${path}=${i2c_devices_tree}[CD8200_FAN_CPLD][PATH]

    execute command and verify exit code
    ...  console=${console}
    ...  command=echo 0 > fan_watchdog_enable
    ...  path=${path}


write pwm value by diagtool
    [Documentation]  Write given PWM value by diagtool
    [Arguments]
    ...  ${console}=${diagos_mode}
    ...  ${path}=${diag_tools_path}
    ...  ${pwd}=100

    execute command and verify exit code
    ...  console=${console}
    ...  command=(${diag_export_env}./cel-fan-test -w -t pwm -D ${pwd})
    ...  path=${path}


read fan maximum speed from file system attribute
    [Documentation]  Read FAN maxumum spped from file system attribute
    [Arguments]
    ...  ${console}=${diagos_mode}
    ...  ${path}=${i2c_devices_tree}[LOGGER_DUMP][PATH]
    ...  ${pattern}=(?m)^(?P<fan_max_speed>\\d+)

    execute command and verify with a pattern
    ...  console=${console}
    ...  command=cat fan_max_speed
    ...  path=${path}
    ...  pattern=${pattern}


write fan maximum speed to file system attribute
    [Documentation]  Write given speed to fan maximum speed on file system attribute
    [Arguments]
    ...  ${console}=${diagos_mode}
    ...  ${path}=${i2c_devices_tree}[LOGGER_DUMP][PATH]
    ...  ${fan_max_speed}=

    execute command and verify exit code
    ...  console=${console}
    ...  command=echo ${fan_max_speed} > fan_max_speed
    ...  path=${path}


read fan pwm and rpm by diagtool
    [Documentation]  Read FAN PWM and RPM depends on given patterns,
    ...  cause it use the same option --show
    [Arguments]
    ...  ${console}=${diagos_mode}
    ...  ${path}=
    ...  ${patterns}=

    execute command and verify with ordered pattern list
    ...  console=${console}
    ...  command=(${diag_export_env}./cel-fan-test --show)
    ...  path=${path}
    ...  patterns=${patterns}


read all current fans pwm by diagtool
    [Documentation]  Use diagtool to read all current FAN PWM
    [Arguments]
    ...  ${console}=${diagos_mode}
    ...  ${path}=${diag_tools_path}
    ...  ${patterns}=${diag_tools_cel_fan_test_show_current_pwm_patterns}

    read fan pwm and rpm by diagtool
    ...  console=${console}
    ...  path=${path}
    ...  patterns=${patterns}
    set test variable  &{diag_tools_current_fans_pwm}  &{matches}


read all current fans rpm by diagtool
    [Documentation]  Use diagtool to read all current FAN RPM
    [Arguments]
    ...  ${console}=${diagos_mode}
    ...  ${path}=${diag_tools_path}
    ...  ${patterns}=${diag_tools_cel_fan_test_show_current_rpm_patterns}

    read fan pwm and rpm by diagtool
    ...  console=${console}
    ...  path=${path}
    ...  patterns=${patterns}
    set test variable  &{diag_tools_current_fans_rpm}  &{matches}


verify current fan pwm value read by diagtool
    [Documentation]  Verify current fan pwm value read by diagtool
    [Arguments]
    ...  ${pwm}=255

    FOR  ${key}  ${value}  IN  &{diag_tools_current_fans_pwm}
        Should Be Equal As Numbers  ${pwm}  ${value}  precision=0  msg=The ${key} must be ${pwm}!${\n}
    END


read fan reset by file system attribute
    [Documentation]  Read fan reset attribute
    [Arguments]
    ...  ${console}=${diagos_mode}
    ...  ${path}=${i2c_devices_tree}[LOGGER_DUMP][PATH]
    ...  ${pattern}=(?m)^\\w+$  # Should be this pattern, now unit is abnormal (?m)^0x[0-9a-fA-F]{2}$

    execute command and verify with a pattern
    ...  console=${console}
    ...  command=cat fan_reset
    ...  path=${path}
    ...  pattern=${pattern}


write fan reset by file system attribute
    [Documentation]  Write given value to fan reset attribute
    [Arguments]
    ...  ${console}=${diagos_mode}
    ...  ${path}=${i2c_devices_tree}[LOGGER_DUMP][PATH]
    ...  ${fan_reset}=0

    execute command and verify exit code
    ...  console=${console}
    ...  command=echo ${fan_reset} > fan_reset
    ...  path=${path}


write a time to system watchdog attribute
    [Documentation]  Write given time to system watchdog attribute
    [Arguments]
    ...  ${console}=${diagos_mode}
    ...  ${path}=${i2c_devices_tree}[LOGGER_DUMP][PATH]
    ...  ${system_watchdog_seconds}=10

    execute command and verify exit code
    ...  console=${console}
    ...  command=echo ${system_watchdog_seconds} > system_watchdog_seconds
    ...  path=${path}


read watchdog timeout by file system attribute
    [Documentation]  read watchdog timeout by file system attribute
    [Arguments]
    ...  ${console}=${diagos_mode}
    ...  ${path}=${i2c_devices_tree}[LOGGER_DUMP][PATH]
    ...  ${pattern}=(?m)^0x[0-9a-fA-F]{2}$

    execute command and verify with a pattern
    ...  console=${console}
    ...  command=cat system_watchdog_seconds
    ...  path=${path}
    ...  pattern=${pattern}

fhv2 read watchdog timeout by file system attribute
    [Documentation]  read watchdog timeout by file system attribute
    [Arguments]
    ...  ${console}=${diagos_mode}
    ...  ${path}=${i2c_devices_tree}[LOGGER_DUMP][PATH]
    ...  ${pattern}=(?m)^10$

    execute command and verify with a pattern
    ...  console=${console}
    ...  command=cat system_watchdog_seconds
    ...  path=${path}
    ...  pattern=${pattern}

write system watchdog enable status by file system attribute
    [Documentation]  Write given value (0x0 = disable and 0x1 = enablee) to file system attribute for system watchdog
    [Arguments]
    ...  ${console}=${diagos_mode}
    ...  ${path}=${i2c_devices_tree}[LOGGER_DUMP][PATH]
    ...  ${system_watchdog_enable}=0x1

    execute command and verify exit code
    ...  console=${console}
    ...  command=echo ${system_watchdog_enable} > system_watchdog_enable
    ...  path=${path}


enable system watchdog by file system attribute
    [Documentation]  enable system watchdog by file system attribute
    [Arguments]
    ...  ${console}=${diagos_mode}
    ...  ${path}=${i2c_devices_tree}[LOGGER_DUMP][PATH]
    ...  ${system_watchdog_enable}=1

    write system watchdog enable status by file system attribute
    ...  console=${console}
    ...  path=${path}
    ...  system_watchdog_enable=${system_watchdog_enable}


disable system watchdog by file system attribute
    [Documentation]  disable system watchdog by file system attribute
    [Arguments]
    ...  ${console}=${diagos_mode}
    ...  ${path}=${i2c_devices_tree}[LOGGER_DUMP][PATH]
    ...  ${system_watchdog_enable}=0

    write system watchdog enable status by file system attribute
    ...  console=${console}
    ...  path=${path}
    ...  system_watchdog_enable=${system_watchdog_enable}


read system watchdog enable status by file system attribute
    [Documentation]  read system watchdog enable status by file system attribute
    [Arguments]
    ...  ${console}=${diagos_mode}
    ...  ${path}=${i2c_devices_tree}[LOGGER_DUMP][PATH]
    ...  ${pattern}=(?m)^0x[0-9a-fA-F]$

    execute command and verify with a pattern
    ...  console=${console}
    ...  command=cat system_watchdog_enable
    ...  path=${path}
    ...  pattern=${pattern}

fhv2 read system watchdog enable status by file system attribute
    [Documentation]  read system watchdog enable status by file system attribute
    [Arguments]
    ...  ${console}=${diagos_mode}
    ...  ${path}=${i2c_devices_tree}[LOGGER_DUMP][PATH]
    ...  ${pattern}=(?m)^0$

    execute command and verify with a pattern
    ...  console=${console}
    ...  command=cat system_watchdog_enable
    ...  path=${path}
    ...  pattern=${pattern}

read warm reset by file system attribute
    [Documentation]  read warm reset status by file system attribute
    [Arguments]
    ...  ${console}=${diagos_mode}
    ...  ${path}=${i2c_devices_tree}[LOGGER_DUMP][PATH]
    ...  ${pattern}=(?m)^0x[0-9a-fA-F]$

    execute command and verify with a pattern
    ...  console=${console}
    ...  command=cat warm_reset
    ...  path=${path}
    ...  pattern=${pattern}

fhv2 read warm reset by file system attribute
    [Documentation]  read warm reset status by file system attribute
    [Arguments]
    ...  ${console}=${diagos_mode}
    ...  ${path}=${i2c_devices_tree}[LOGGER_DUMP][PATH]
    ...  ${pattern}=(?m)^0$

    execute command and verify with a pattern
    ...  console=${console}
    ...  command=cat warm_reset
    ...  path=${path}
    ...  pattern=${pattern}

write warm reset by file system attribute
    [Documentation]  write warm reset by file system attribute
    [Arguments]
    ...  ${console}=${diagos_mode}
    ...  ${path}=${i2c_devices_tree}[LOGGER_DUMP][PATH]
    ...  ${warm_reset}=1

    execute command and verify exit code
    ...  console=${console}
    ...  command=echo ${warm_reset} > warm_reset
    ...  path=${path}

fhv2 write warm reset by file system attribute
    [Documentation]  write warm reset by file system attribute
    [Arguments]
    ...  ${console}=${diagos_mode}
    ...  ${path}=${i2c_devices_tree}[LOGGER_DUMP][PATH]
    ...  ${warm_reset}=1

    fhv2 execute reset command
    ...  console=${console}
    ...  command=echo ${warm_reset} > warm_reset
    ...  path=${path}

read cold reset by file system attribute
    [Documentation]  read cold reset status by file system attribute
    [Arguments]
    ...  ${console}=${diagos_mode}
    ...  ${path}=${i2c_devices_tree}[LOGGER_DUMP][PATH]
    ...  ${pattern}=(?m)^0x[0-9a-fA-F]$

    execute command and verify with a pattern
    ...  console=${console}
    ...  command=cat cold_reset
    ...  path=${path}
    ...  pattern=${pattern}

fhv2 read cold reset by file system attribute
    [Documentation]  read cold reset status by file system attribute
    [Arguments]
    ...  ${console}=${diagos_mode}
    ...  ${path}=${i2c_devices_tree}[LOGGER_DUMP][PATH]
    ...  ${pattern}=(?m)^0$

    execute command and verify with a pattern
    ...  console=${console}
    ...  command=cat cold_reset
    ...  path=${path}
    ...  pattern=${pattern}

write cold reset by file system attribute
    [Documentation]  write cold reset by file system attribute
    [Arguments]
    ...  ${console}=${diagos_mode}
    ...  ${path}=${i2c_devices_tree}[LOGGER_DUMP][PATH]
    ...  ${cold_reset}=1

    execute command and verify exit code
    ...  console=${console}
    ...  command=echo ${cold_reset} > cold_reset
    ...  path=${path}

fhv2 write cold reset by file system attribute
    [Documentation]  write cold reset by file system attribute
    [Arguments]
    ...  ${console}=${diagos_mode}
    ...  ${path}=${i2c_devices_tree}[LOGGER_DUMP][PATH]
    ...  ${cold_reset}=1

    fhv2 execute reset command
    ...  console=${console}
    ...  command=echo ${cold_reset} > cold_reset
    ...  path=${path}

dump PSU eeprom on file system attribute
    [Documentation]  dump given PSU eeprom path on file system attribute
    [Arguments]
    ...  ${console}=${diagos_mode}
    ...  ${path}=

    execute command and verify exit code
    ...  console=${console}
    ...  command=(cat eeprom | hexdump -C)
    ...  path=${path}


verify all ASC10-1 values by file system attribute
    [Documentation]  verify all ASC10-1 values by file system attribute
    [Arguments]
    ...  ${console}=${diagos_mode}
    ...  ${path}=${i2c_devices_tree}[ASC10-1][PATH]
    ...  ${attrs}=${i2c_asc10_comm_attrs}

    verify all attributes on the directory
    ...  console=${console}
    ...  path=${path}
    ...  attrs=${attrs}
    ...  msg=Failed to verify I2C device name "ASC10-1"${\n}on path "${path}\[PATH]"
    set test variable  &{fs_attrs_asc10_1}  &{fs_attrs}

fhv2 verify all ASC10-1 values by file system attribute
    [Documentation]  verify all ASC10-1 values by file system attribute
    [Arguments]
    ...  ${console}=${diagos_mode}
    ...  ${path}=${i2c_devices_tree}[ASC10-1][PATH]
    ...  ${attrs}=${i2c_asc10_comm_attrs_1}

    verify all attributes on the directory
    ...  console=${console}
    ...  path=${path}
    ...  attrs=${attrs}
    ...  msg=Failed to verify I2C device name "ASC10-1"${\n}on path "${path}\[PATH]"
    set test variable  &{fs_attrs_asc10_1}  &{fs_attrs}

verify all ASC10-2 values by file system attribute
    [Documentation]  verify all ASC10-2 values by file system attribute
    [Arguments]
    ...  ${console}=${diagos_mode}
    ...  ${path}=${i2c_devices_tree}[ASC10-1][PATH]
    ...  ${attrs}=${i2c_asc10_comm_attrs}

    verify all attributes on the directory
    ...  console=${console}
    ...  path=${path}
    ...  attrs=${attrs}
    ...  msg=Failed to verify I2C device name "ASC10-2"${\n}on path "${path}\[PATH]"
    set test variable  &{fs_attrs_asc10_2}  &{fs_attrs}

fhv2 verify all ASC10-2 values by file system attribute
    [Documentation]  verify all ASC10-2 values by file system attribute
    [Arguments]
    ...  ${console}=${diagos_mode}
    ...  ${path}=${i2c_devices_tree}[ASC10-2][PATH]
    ...  ${attrs}=${i2c_asc10_comm_attrs_2}

    verify all attributes on the directory
    ...  console=${console}
    ...  path=${path}
    ...  attrs=${attrs}
    ...  msg=Failed to verify I2C device name "ASC10-2"${\n}on path "${path}\[PATH]"
    set test variable  &{fs_attrs_asc10_2}  &{fs_attrs}

fhv2 verify all ASC10-3 values by file system attribute
    [Documentation]  verify all ASC10-3 values by file system attribute
    [Arguments]
    ...  ${console}=${diagos_mode}
    ...  ${path}=${i2c_devices_tree}[ASC10-3][PATH]
    ...  ${attrs}=${i2c_asc10_comm_attrs_3}

    verify all attributes on the directory
    ...  console=${console}
    ...  path=${path}
    ...  attrs=${attrs}
    ...  msg=Failed to verify I2C device name "ASC10-3"${\n}on path "${path}\[PATH]"
    set test variable  &{fs_attrs_asc10_3}  &{fs_attrs}

read all ASC10 values by diagtool
    [Documentation]  Read all ASC10 values by diagtool
    [Arguments]
    ...  ${console}=${diagos_mode}
    ...  ${path}=${diag_tools_path}
    ...  ${patterns}=
    ...  ${msg}=

    execute command and verify with ordered pattern list
    ...  console=${console}
    ...  command=(${diag_export_env}./cel-dcdc-test --all)
    ...  patterns=${patterns}
    ...  path=${path}
    ...  msg=${msg}
    ...  is_check_exit_code=${TRUE}


read all ASC10-1 values by diagtool
    [Documentation]  Read all ASC10-1 values by diagtool

    read all ASC10 values by diagtool
    ...  patterns=${diag_tools_asc10_1_patterns}
    ...  msg=Failed to search for ASC10-1 pattern!
    set test variable  &{diagtools_asc10_1}  &{matches}


read all ASC10-2 values by diagtool
    [Documentation]  Read all ASC10-2 values by diagtool

    read all ASC10 values by diagtool
    ...  patterns=${diag_tools_asc10_2_patterns}
    ...  msg=Failed to search for ASC10-2 pattern!
    set test variable  &{diagtools_asc10_2}  &{matches}

read all ASC10-3 values by diagtool
    [Documentation]  Read all ASC10-3 values by diagtool

    read all ASC10 values by diagtool
    ...  patterns=${diag_tools_asc10_3_patterns}
    ...  msg=Failed to search for ASC10-3 pattern!
    set test variable  &{diagtools_asc10_3}  &{matches}

compare all ASC10 1 & 2 values for file system attribute with diagtool table min/max values
    [Documentation]  Compare all FAN inputs for ile system attribute and diagtool

    # Convert to x.yz Voltage
    FOR  ${x}  IN RANGE  1  11  1
        ${new_asc10_1_max} =  Evaluate  float(${fs_attrs_asc10_1}[in${x}_max] / 1000)
        ${new_asc10_1_min} =  Evaluate  float(${fs_attrs_asc10_1}[in${x}_min] / 1000)
        ${new_asc10_1_input} =  Evaluate  float(${fs_attrs_asc10_1}[in${x}_input] / 1000)

        Set To Dictionary  ${fs_attrs_asc10_1}  in${x}_max=${new_asc10_1_max}
        Set To Dictionary  ${fs_attrs_asc10_1}  in${x}_min=${new_asc10_1_min}
        Set To Dictionary  ${fs_attrs_asc10_1}  in${x}_input=${new_asc10_1_input}

        Run Keyword If  ${fs_attrs_asc10_1}[in${x}_input] > ${diagtools_asc10_1}[in${x}_max]
        ...  Fail  Failed, due to ASC10-1 in${x}_input (${fs_attrs_asc10_1}[in${x}_input]V) is greater than its upper value in${x}_max (${diagtools_asc10_1}[in${x}_max]V)
        Run Keyword If  ${fs_attrs_asc10_1}[in${x}_input] < ${diagtools_asc10_1}[in${x}_min]
        ...  Fail  Failed, due to ASC10-1 in${x}_input (${fs_attrs_asc10_1}[in${x}_input]V) is less than its lower value in${x}_min (${diagtools_asc10_1}[in${x}_min]V)

        ${new_asc10_2_max} =  Evaluate  float(${fs_attrs_asc10_2}[in${x}_max] / 1000)
        ${new_asc10_2_min} =  Evaluate  float(${fs_attrs_asc10_2}[in${x}_min] / 1000)
        ${new_asc10_2_input} =  Evaluate  float(${fs_attrs_asc10_2}[in${x}_input] / 1000)

        Set To Dictionary  ${fs_attrs_asc10_2}  in${x}_max=${new_asc10_2_max}
        Set To Dictionary  ${fs_attrs_asc10_2}  in${x}_min=${new_asc10_2_min}
        Set To Dictionary  ${fs_attrs_asc10_2}  in${x}_input=${new_asc10_2_input}

        Run Keyword If  ${fs_attrs_asc10_2}[in${x}_input] > ${diagtools_asc10_2}[in${x}_max]
        ...  Fail  Failed, due to ASC10-2 in${x}_input (${fs_attrs_asc10_2}[in${x}_input]V) is greater than its upper value in${x}_max (${diagtools_asc10_2}[in${x}_max]V)
        Run Keyword If  ${fs_attrs_asc10_2}[in${x}_input] < ${diagtools_asc10_2}[in${x}_min]
        ...  Fail  Failed, due to ASC10-2 in${x}_input (${fs_attrs_asc10_2}[in${x}_input]V) is less than its lower value in${x}_min (${diagtools_asc10_2}[in${x}_min]V)
    END

compare all ASC10 1 & 2 & 3 values for file system attribute with diagtool table min/max values
    [Documentation]  Compare all FAN inputs for ile system attribute and diagtool

    # Convert to x.yz Voltage
    FOR  ${x}  IN RANGE  1  11  1
        ${new_asc10_1_max} =  Evaluate  float(${fs_attrs_asc10_1}[in${x}_max] / 1000)
        ${new_asc10_1_min} =  Evaluate  float(${fs_attrs_asc10_1}[in${x}_min] / 1000)
        ${new_asc10_1_input} =  Evaluate  float(${fs_attrs_asc10_1}[in${x}_input] / 1000)

        Set To Dictionary  ${fs_attrs_asc10_1}  in${x}_max=${new_asc10_1_max}
        Set To Dictionary  ${fs_attrs_asc10_1}  in${x}_min=${new_asc10_1_min}
        Set To Dictionary  ${fs_attrs_asc10_1}  in${x}_input=${new_asc10_1_input}

        Run Keyword If  ${fs_attrs_asc10_1}[in${x}_input] > ${diagtools_asc10_1}[in${x}_max]
        ...  Fail  Failed, due to ASC10-1 in${x}_input (${fs_attrs_asc10_1}[in${x}_input]V) is greater than its upper value in${x}_max (${diagtools_asc10_1}[in${x}_max]V)
        Run Keyword If  ${fs_attrs_asc10_1}[in${x}_input] < ${diagtools_asc10_1}[in${x}_min]
        ...  Fail  Failed, due to ASC10-1 in${x}_input (${fs_attrs_asc10_1}[in${x}_input]V) is less than its lower value in${x}_min (${diagtools_asc10_1}[in${x}_min]V)

        ${new_asc10_2_max} =  Evaluate  float(${fs_attrs_asc10_2}[in${x}_max] / 1000)
        ${new_asc10_2_min} =  Evaluate  float(${fs_attrs_asc10_2}[in${x}_min] / 1000)
        ${new_asc10_2_input} =  Evaluate  float(${fs_attrs_asc10_2}[in${x}_input] / 1000)

        Set To Dictionary  ${fs_attrs_asc10_2}  in${x}_max=${new_asc10_2_max}
        Set To Dictionary  ${fs_attrs_asc10_2}  in${x}_min=${new_asc10_2_min}
        Set To Dictionary  ${fs_attrs_asc10_2}  in${x}_input=${new_asc10_2_input}

        Run Keyword If  ${fs_attrs_asc10_2}[in${x}_input] > ${diagtools_asc10_2}[in${x}_max]
        ...  Fail  Failed, due to ASC10-2 in${x}_input (${fs_attrs_asc10_2}[in${x}_input]V) is greater than its upper value in${x}_max (${diagtools_asc10_2}[in${x}_max]V)
        Run Keyword If  ${fs_attrs_asc10_2}[in${x}_input] < ${diagtools_asc10_2}[in${x}_min]
        ...  Fail  Failed, due to ASC10-2 in${x}_input (${fs_attrs_asc10_2}[in${x}_input]V) is less than its lower value in${x}_min (${diagtools_asc10_2}[in${x}_min]V)

        ${new_asc10_3_max} =  Evaluate  float(${fs_attrs_asc10_3}[in${x}_max] / 1000)
        ${new_asc10_3_min} =  Evaluate  float(${fs_attrs_asc10_3}[in${x}_min] / 1000)
        ${new_asc10_3_input} =  Evaluate  float(${fs_attrs_asc10_3}[in${x}_input] / 1000)

        Set To Dictionary  ${fs_attrs_asc10_3}  in${x}_max=${new_asc10_3_max}
        Set To Dictionary  ${fs_attrs_asc10_3}  in${x}_min=${new_asc10_3_min}
        Set To Dictionary  ${fs_attrs_asc10_3}  in${x}_input=${new_asc10_3_input}

        Run Keyword If  ${fs_attrs_asc10_3}[in${x}_input] > ${diagtools_asc10_3}[in${x}_max]
        ...  Fail  Failed, due to ASC10-3 in${x}_input (${fs_attrs_asc10_3}[in${x}_input]V) is greater than its upper value in${x}_max (${diagtools_asc10_3}[in${x}_max]V)
        Run Keyword If  ${fs_attrs_asc10_3}[in${x}_input] < ${diagtools_asc10_3}[in${x}_min]
        ...  Fail  Failed, due to ASC10-3 in${x}_input (${fs_attrs_asc10_3}[in${x}_input]V) is less than its lower value in${x}_min (${diagtools_asc10_3}[in${x}_min]V)
    END

U-Boot run uploadonie
    [Documentation]  U-Boot run uploadonie command
    [Arguments]
    ...  ${console}=${uboot_mode}
    ...  ${cmd}=uploadonie
    ...  ${patterns}=${uboot_run_uploadonie_patterns}
    ...  ${sec}=300

    execute command and verify with ordered pattern list
    ...  console=${console}
    ...  command=run ${cmd}
    ...  patterns=${patterns}
    ...  msg=Failed to run "${cmd}" on U-Boot!
    ...  sec=${sec}


update SYS CPLD firmware
    [Documentation]  Write given firmware to SYS CPLD
    [Arguments]
    ...  ${console}=${diagos_mode}
    ...  ${firmware}=${vmetool_sys_cpld_new_image_file}
    ...  ${path}=${vmetool_path}
    ...  ${pattern}=(?m)^\\| (?P<PASS>PASS)! \\|$
    ...  ${sec}=420  # Typically it is 5min 30sec + 2min

    execute command and verify with a pattern
    ...  console=${console}
    ...  command=./vmetool_arm ${firmware}  # No -f option!
    ...  path=${path}
    ...  pattern=${pattern}
    ...  sec=${sec}


read SYS CPLD version
    [Documentation]  Read SYS CPLD version and verify with pattern
    [Arguments]
    ...  ${console}=${diagos_mode}
    ...  ${command}=i2cget -f -y 10 0x66 0x00
    ...  ${path}=${EMPTY}
    ...  ${pattern}=(?m)^(?P<sys_cpld_version>${vmetool_sys_cpld_new_image_version})$

    execute command and verify with a pattern
    ...  console=${console}
    ...  command=${command}
    ...  path=${path}
    ...  pattern=${pattern}


update FAN CPLD firmware
    [Documentation]  Write given firmware to FAN CPLD
    [Arguments]
    ...  ${console}=${diagos_mode}
    ...  ${firmware}=${vmetool_fan_cpld_new_image_file}
    ...  ${path}=${vmetool_path}
    ...  ${pattern}=(?m)^\\| (?P<PASS>PASS)! \\|$
    ...  ${sec}=420  # Typically it is 5min 0sec + 2min

    execute command and verify with a pattern
    ...  console=${console}
    ...  command=./vmetool_arm -f ${firmware}
    ...  path=${path}
    ...  pattern=${pattern}
    ...  sec=${sec}


read FAN CPLD version
    [Documentation]  Read FAN CPLD version and verify with pattern
    [Arguments]
    ...  ${console}=${diagos_mode}
    ...  ${command}=i2cget -f -y 15 0x60 0x00
    ...  ${path}=${EMPTY}
    ...  ${pattern}=(?m)^(?P<fan_cpld_version>${vmetool_fan_cpld_new_image_version})$

    execute command and verify with a pattern
    ...  console=${console}
    ...  command=${command}
    ...  path=${path}
    ...  pattern=${pattern}


U-Boot mdio read
    [Documentation]  U-Boot execute mdio read
    [Arguments]
    ...  ${console}=${uboot_mode}
    ...  ${args}=0 0.21

    execute command and verify exit code
    ...  console=${console}
    ...  command=mdio read ${args}


U-Boot sleep
    [Documentation]  U-Boot execute sleep
    [Arguments]
    ...  ${console}=${uboot_mode}
    ...  ${sleep}=1

    execute command and verify exit code
    ...  console=${console}
    ...  command=sleep ${sleep}


U-Boot tftpboot
    [Documentation]  U-Boot execute tftpboot
    [Arguments]
    ...  ${console}=${uboot_mode}
    ...  ${args}=0x08000000 uboot_stress.tar
    ...  ${patterns}=${uboot_tftpboot_patterns}
    ...  ${sec}=60

    execute command and verify with ordered pattern list
    ...  console=${console}
    ...  command=tftpboot ${args}
    ...  patterns=${patterns}
    ...  msg=Failed to run tftpboot "${args}" on U-Boot!
    ...  sec=${sec}

Diag Check network connectivity
    [Arguments]  ${MODE}
    execute_check_dict  DUT  ${ifconfig_a_cmd}  mode=${MODE}
    ...  patterns_dict=${fail_dict}  timeout=5  is_negative_test=True
    ${ip} =  get ip address from config  PC
    exec_ping  DUT  ipAddress=${ip}  count=5  mode=${MODE}

Self Update Onie
    [Arguments]  ${version}
    Step  1  boot Into Onie Rescue Mode
    Step  2  config Static IP
    Step  3  onie Self Update  update=${version}
    Step  4  verify Onie And CPLD Version  version=${version}