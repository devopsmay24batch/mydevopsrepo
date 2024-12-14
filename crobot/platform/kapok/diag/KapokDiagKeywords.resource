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


*** Keywords ***
write MAC address to MGMT port
    [Documentation]  Write given MAC Address to Management Port
    [Arguments]
    ...  ${console}=${uboot_mode}
    ...  ${path}=${diag_tools_path}
    ...  ${command}=${diag_write_mac_addr_command}
    ...  ${options}=${diag_write_mac_addr_options}
    ...  ${mac}=38:73:EA:DA:89:82
    ...  ${patterns}=${diag_write_mac_addr_patterns}

    execute command and verify with ordered pattern list
    ...  path=${path}
    ...  command=${command} ${options} ${mac}
    ...  console=${console}
    ...  patterns=${patterns}

    set test variable  &{mac_addr_written}  &{matches}


read MAC address from MGMT port
    [Documentation]  Read MAC Address from Management Port
    [Arguments]
    ...  ${console}=${uboot_mode}
    ...  ${path}=${diag_tools_path}
    ...  ${command}=${diag_read_mac_addr_command}
    ...  ${options}=${diag_read_mac_addr_options}
    ...  ${patterns}=${diag_read_mac_addr_patterns}

    execute command and verify with ordered pattern list
    ...  path=${path}
    ...  command=${command} ${options}
    ...  console=${console}
    ...  patterns=${patterns}

    set test variable  &{mac_addr_read}  &{matches}


verify MGMT port MAC address modification
    [Documentation]  Write given MAC Address to Management Port and read it to verify

    write MAC address to MGMT port
    read MAC address from MGMT port
    compare two dictionaries with matched key
    ...  original=${mac_addr_written}
    ...  compare=${mac_addr_read}
    ...  msg=Written MAC Address does not match read MAC Address!


verify CPLD test all
    [Documentation]  Verify CPLD tool with --all
    [Arguments]
    ...  ${console}=${diagos_mode}
    ...  ${path}=${diag_tools_path}
    ...  ${command}=${diag_cel_cpld_test_command}
    ...  ${options}=${diag_cel_cpld_test_all_options}
    ...  ${patterns}=${diag_cel_cpld_test_all_patterns}

    execute command and verify with ordered pattern list
    ...  path=${path}
    ...  command=${command} ${options}
    ...  console=${console}
    ...  patterns=${patterns}

    set test variable  &{cpld_all_versions}  &{matches}


verify CPLD dump device register
    [Documentation]  Verify dumped device register memory
    [Arguments]
    ...  ${console}=${diagos_mode}
    ...  ${path}=${diag_tools_path}
    ...  ${command}=${diag_cel_cpld_test_command}
    ...  ${options}=${diag_cel_cpld_test_dump_d_options}
    ...  ${patterns}=${diag_cel_cpld_test_dump_d_patterns}
    ...  ${dev_id}=1

    execute command and verify with ordered pattern list
    ...  path=${path}
    ...  command=${command} ${options} ${dev_id}
    ...  console=${console}
    ...  patterns=${patterns}


verify CPLD scan device info
    [Documentation]  Verify CPLD scanned device information
    [Arguments]
    ...  ${console}=${diagos_mode}
    ...  ${path}=${diag_tools_path}
    ...  ${command}=${diag_cel_cpld_test_command}
    ...  ${options}=${diag_cel_cpld_test_s_d_options}
    ...  ${patterns}=${diag_cel_cpld_test_s_d_patterns}
    ...  ${dev_id}=1

    execute command and verify with ordered pattern list
    ...  path=${path}
    ...  command=${command} ${options} ${dev_id}
    ...  console=${console}
    ...  patterns=${patterns}

    # set test variable  &{cpld${dev_id}_scanned_versions}  &{matches}
    set to dictionary
    ...  ${cpld_scanned_versions}
    ...  CPLD${dev_id}_VER=${matches}[CPLD_VER]


verify CPLD versions
    [Documentation]  Verify CPLD read versions over difference tools

    verify CPLD test all
    &{cpld_scanned_versions}  create dictionary  CPLD1_VER=""
    set test variable  &{cpld_scanned_versions}
    verify CPLD scan device info  dev_id=1
    verify CPLD scan device info  dev_id=2
    verify CPLD scan device info  dev_id=3
    verify CPLD scan device info  dev_id=4  # fan_cpld
    # set to dictionary
    # ...  ${cpld_scanned_versions}
    # ...  CPLD1_VER  cpld1_scanned_versions[CPLD_VER]
    # ...  CPLD2_VER  cpld2_scanned_versions[CPLD_VER]
    # ...  CPLD3_VER  cpld3_scanned_versions[CPLD_VER]
    # ...  CPLD4_VER  cpld4_scanned_versions[CPLD_VER]
    compare two dictionaries with matched key
    ...  original=${cpld_scanned_versions}
    ...  compare=${cpld_all_versions}
    ...  msg=CPLD version over difference tools does not match!


verify CPLD tool help option
    [Documentation]  Verify CPLD tool help option
    [Arguments]
    ...  ${console}=${diagos_mode}
    ...  ${path}=${diag_tools_path}
    ...  ${command}=${diag_cel_cpld_test_command}
    ...  ${options}=${diag_cel_cpld_test_h_options}
    ...  ${patterns}=${diag_cel_cpld_test_h_patterns}

    execute command and verify with ordered pattern list
    ...  path=${path}
    ...  command=${command} ${options}
    ...  console=${console}
    ...  patterns=${patterns}


cat main board version
    [Documentation]  Show and verify mani board version by cat command
    [Arguments]
    ...  ${console}=${diagos_mode}
    ...  ${path}=${EMPTY}
    ...  ${command}=cat
    ...  ${options}=${diag_cat_board_version_options}
    ...  ${patterns}=${diag_cat_board_version_patterns}

    execute command and verify with ordered pattern list
    ...  path=${path}
    ...  command=${command} ${options}
    ...  console=${console}
    ...  patterns=${patterns}

    set test variable  &{cat_board_version}  &{matches}


show PCIe device
    [Documentation]  Show PCIe device
    [Arguments]
    ...  ${console}=${uboot_mode}
    ...  ${path}=${diag_tools_path}
    ...  ${command}=${diag_cel_pci_test_command}
    ...  ${options}=${diag_cel_pci_test_all_options}
    ...  ${patterns}=${diag_cel_pci_test_all_patterns}

    execute command and verify with a pattern for table
    ...  path=${path}
    ...  command=${command} ${options}
    ...  console=${console}
    ...  patterns=${patterns}

    set test variable  &{pcie_devices}  &{matches}


verify PCIe device list
    [Documentation]  Verify PCIe device list

    show PCIe device


check CPLD's PRSTN2X16N status
    [Documentation]  check CPLD's PRSTN2X16N status
    [Arguments]
    ...  ${console}=${diagos_mode}
    ...  ${path}=${diag_tools_path}
    ...  ${command}=${present_status_cmd}
    ...  ${pattern}=(?m)^0$

    execute command and verify with a pattern
    ...  path=${path}
    ...  command=${command}
    ...  console=${console}
    ...  pattern=${pattern}

access all temperature sensor devices
    [Documentation]  Verify to access all temperature sensor devices
    [Arguments]
    ...  ${console}=${diagos_mode}
    ...  ${path}=${diag_tools_path}
    ...  ${command}=./cel-temp-test --all
    ...  ${pattern}=${temp_test_all_fail_pattern}

    ${status}  ${value}=  Run Keyword And Ignore Error  execute command and verify with a pattern for table
    ...  console=${console}
    ...  command=(${diag_export_env} ${command})
    ...  path=${path}
    ...  pattern=${pattern}
    ...  msg=Should not found the fail pattern!
    ...  is_check_exit_code=${FALSE}
    Run Keyword If  '${status}' == 'PASS'
    ...  Fail  Failed to check temperature:${\n*2}Failed on ID${\n}${matches}


show temperature sensor
    [Documentation]  show temperature sensor
    [Arguments]
    ...  ${console}=${diagos_mode}
    ...  ${path}=${diag_tools_path}
    ...  ${command}=./cel-temp-test --show

    execute command and verify exit code
    ...  path=${path}
    ...  command=(${diag_export_env} ${command})
    ...  console=${console}

show temperature list
    [Documentation]  show temperature sensor
    [Arguments]
    ...  ${console}=${diagos_mode}
    ...  ${path}=${diag_tools_path}
    ...  ${command}=./cel-temp-test --list

    execute command and verify exit code
    ...  path=${path}
    ...  command=(${diag_export_env} ${command})
    ...  console=${console}

verify CPLDs access on I2C bus by "-s -d 4" option
    [Documentation]  verify CPLDs access on I2C bus by "-s -d 4" option
    [Arguments]
    ...  ${console}=${diagos_mode}
    ...  ${path}=${diag_tools_path}
    ...  ${command}=./cel-cpld-test -s -d 4
    ...  ${pattern}=${cpld_fan_d4_fail_pattern}

    ${status}  ${value}=  Run Keyword And Ignore Error  execute command and verify with a pattern for table
    ...  console=${console}
    ...  command=(${diag_export_env} ${command})
    ...  path=${path}
    ...  pattern=${pattern}
    ...  msg=Should not found the fail pattern!
    ...  is_check_exit_code=${FALSE}
    Run Keyword If  '${status}' == 'PASS'
    ...  Fail  Failed to check temperature:${\n*2}Failed on ID${\n}${matches}


verify CPLDs firmware version
    [Documentation]  verify CPLDs firmware version
    [Arguments]
    ...  ${console}=${diagos_mode}
    ...  ${command}=./cel-cpld-test --all
    ...  ${patterns}=${diag_cel_cpld_test_all_patterns}
    ...  ${path}=${diag_tools_path}

    execute command and verify with ordered pattern list
    ...  console=${console}
    ...  command=(${diag_export_env} ${command})
    ...  patterns=${patterns}
    ...  path=${path}
    ...  msg=Failed to verify CPLD FAN version(s)!



Verify current FAN PWM/RPM is not excess maximum
    [Documentation]  Verify current FAN PWM/RPM is not excess maximum

    FOR  ${x}  IN RANGE  1  8  1
        Run Keyword If  ${fans_pwm_rpm}[fan${x}_front_pwm_max] < ${fans_pwm_rpm}[fan${x}_front_pwm_value]
        ...  Fail  Failed due to FAN${x} FRONT current PWM value is exceeded the maximum
        Run Keyword If  ${fans_pwm_rpm}[fan${x}_front_rpm_max] < ${fans_pwm_rpm}[fan${x}_front_rpm_value]
        ...  Fail  Failed due to FAN${x} FRONT current RPM value is exceeded the maximum

        Run Keyword If  ${fans_pwm_rpm}[fan${x}_panel_pwm_max] < ${fans_pwm_rpm}[fan${x}_panel_pwm_value]
        ...  Fail  Failed due to FAN${x} PANEL current PWM value is exceeded the maximum
        Run Keyword If  ${fans_pwm_rpm}[fan${x}_panel_rpm_max] < ${fans_pwm_rpm}[fan${x}_panel_rpm_value]
        ...  Fail  Failed due to FAN${x} PANEL current RPM value is exceeded the maximum
    END


set PWM to specified FAN device
    [Documentation]  Write given PWM duty cycle to specified FAN device
    [Arguments]
    ...  ${console}=${diagos_mode}
    ...  ${command}=./cel-fan-test -w -t pwm
    ...  ${duty_cycle}=50
    ...  ${fan_number}=1
    ...  ${path}=${diag_tools_path}
    ...  ${pattern}=(?mi)^Writing\\s*(?P<fan_name>fan.*),\\s*pwm:\\s*(?P<pwm_duty_cycle>\\d+).*:\\s*(?P<result>Passed)\\s*$
    ...  ${msg}=Failed to write PWM duty cycle (${duty_cycle}) to FAN number ${fan_number}!

    execute command and verify with a pattern
    ...  console=${console}
    ...  command=(${diag_export_env} ${command} -D ${duty_cycle} -d ${fan_number})
    ...  path=${path}
    ...  pattern=${pattern}
    ...  msg=${msg}


FAN control test
    [Documentation]  Run FAN control test for given test time
    [Arguments]
    ...  ${console}=${diagos_mode}
    ...  ${path}=${diag_tools_path}
    ...  ${command}=./cel-fan-test --test -t fan_ctrl
    ...  ${test_time}=2 minutes 0 seconds
    ...  ${patterns}=${diagos_prompt}

    open prompt
    ...  console=${console}
    ...  sec=300

    send a line
    ...  command=cd ${path} && (${diag_export_env} ${command})

    read until regexp
    ...  patterns=Passed
    ...  timeout=30

    Sleep  ${test_time}

    read until regexp
    ...  patterns=Passed
    ...  timeout=30

    send a line
    ...  command=\x03  # Ctrl-C

    read until regexp
    ...  patterns=${patterns}
    ...  timeout=5

    [Teardown]  send a line  command=\x03  # Ctrl-C


set FAN watchdog trigger time
    [Documentation]  Write given watchdog trigger time
    [Arguments]
    ...  ${console}=${diagos_mode}
    ...  ${time}=10
    ...  ${path}=${i2c_devices_tree}[CD8200_FAN_CPLD][PATH]

    execute command and verify exit code
    ...  console=${console}
    ...  command=echo ${time} > ${path}/fan_watchdog_seconds


enable FAN watchdog function
    [Documentation]  Enable FAN watchdog function
    [Arguments]
    ...  ${console}=${diagos_mode}
    ...  ${enable}=1
    ...  ${path}=${i2c_devices_tree}[CD8200_FAN_CPLD][PATH]

    execute command and verify exit code
    ...  console=${console}
    ...  command=echo ${enable} > ${path}/fan_watchdog_enable


verify all FAN PWM should be auto-changed to maximum after the watchdog is timeout
    [Documentation]  verify all FAN PWM should be auto-changed to maximum after the watchdog is timeout
    [Arguments]
    ...  ${console}=${diagos_mode}
    ...  ${command}=./cel-fan-test -r --show
    ...  ${patterns}=${diag_tools_cel_fan_test_show_current_pwm_patterns}
    ...  ${path}=${diag_tools_path}

    execute command and verify with ordered pattern list
    ...  console=${console}
    ...  command=(${diag_export_env} ${command})
    ...  patterns=${patterns}
    ...  path=${path}
    ...  msg=Some of FAN PWM does not auto-changed to maximum

    FOR  ${x}  IN RANGE  1  8  1
        Should Be Equal As Integers  255  ${matches}[fan${x}_front_current_rpm]
        ...  msg=FAN${x} FRONT VALUE RPM does not auto-changed to maximum
        Should Be Equal As Integers  255  ${matches}[fan${x}_panel_current_rpm]
        ...  msg=FAN${x} PANEL VALUE RPM does not auto-changed to maximum
    END


verify all FAN PWM already changed to assigned value
    [Documentation]  verify all FAN PWM already changed to assigned value
    [Arguments]
    ...  ${duty_cycle}

    FOR  ${x}  IN RANGE  1  8  1
        Run Keyword If  '${fans_pwm_rpm}[fan${x}_front_pwm_value]' != '${duty_cycle}'
        ...  Fail  FAN${x} FRONT PWM value does not set to ${duty_cycle}
        Run Keyword If  '${fans_pwm_rpm}[fan${x}_panel_pwm_value]' != '${duty_cycle}'
        ...  Fail  FAN${x} PANEL PWM value does not set to ${duty_cycle}
    END


Is Fenghuang 21 inch model
    [Documentation]  Determine what fenghuang model is, 19" or 21"
    [Arguments]
    ...  ${console}=${diagos_mode}

    execute command and verify with a pattern
        ...  console=${console}
        ...  command=i2cget -y -f 5 0x66 0x08
        ...  path=${EMPTY}
        ...  pattern=(?m)^(?P<fan_hw_rev>0x[0-9a-fA-F]{2})$
        ...  msg=Failed to detect Fenghuang model!

    ${model}=  Evaluate  hex(${match}[fan_hw_rev] & 0x08)
    Return From Keyword If  ${model} == 0x08  ${TRUE}
    Return From Keyword  ${FALSE}


dump all FRU EEPROM content depents on fenghuang model
    [Documentation]  Detect Fenghuang model and dump all FRU EEPROM content
    [Arguments]
    ...  ${console}=${diagos_mode}
    ...  ${command}=./cel-eeprom-test -r -t fru -d
    ...  ${path}=${diag_tools_path}

    # Default is FH 21 inch model first
    ${fru_eeprom_number}=  Create List  1  2  3  4  5  6  7

    # If Fenghuang model 19 inch then one more eeprom number 8
    ${fh_model}=  Is Fenghuang 21 inch model
    Run Keyword If  '${fh_model}' == '${FALSE}'  Append To List  ${fru_eeprom_number}  8

    FOR  ${eeprom}  IN  @{fru_eeprom_number}
        execute command and verify exit code
        ...  console=${console}
        ...  command=(${diag_export_env}${command} ${eeprom})
        ...  path=${path}
    END


dump all FRU EEPROM content depents on fenghuangv2 model
    [Documentation]  Detect Fenghuang model and dump all FRU EEPROM content
    [Arguments]
    ...  ${console}=${diagos_mode}
    ...  ${command}=./cel-eeprom-test -r -t fru -d
    ...  ${path}=${diag_tools_path}

    # Default is FH 21 inch model first
    ${fru_eeprom_number}=  Create List  1  2  3  4  5  6  7  8  9  11

    FOR  ${eeprom}  IN  @{fru_eeprom_number}
        execute command and verify exit code
        ...  console=${console}
        ...  command=(${diag_export_env}${command} ${eeprom})
        ...  path=${path}
    END


edit/update server IP and our IP on configs/phys.yaml file
    [Documentation]  Update server IP and our IP to the configuration file
    [Arguments]
    ...  ${console}=${diagos_mode}
    ...  ${interface}=${mgmt_interface}
    ...  ${server_ip}=${dhcp_renew_info}[dhcp_server_ip]
    ...  ${our_ip}=${dhcp_renew_info}[dhcp_our_new_ip]
    ...  ${path}=${diag_tools_path}

    execute command and verify exit code
    ...  console=${console}
    ...  command=sed -ir 's/server_ip.*$/server_ip: "${server_ip}"/g' configs/phys.yaml
    ...  path=${path}

    execute command and verify exit code
    ...  console=${console}
    ...  command=sed -ir 's/ip_addr.*$/ip_addr: "${our_ip}"/g' configs/phys.yaml
    ...  path=${path}


diagnose MGMT port ping test
    [Documentation]  Run diagnostic to verify ping over management port
    [Arguments]
    ...  ${console}=${diagos_mode}
    ...  ${command}=./cel-phy-test --all

    execute command and verify with a pattern
    ...  console=${console}
    ...  command=${command}
    ...  path=${EMPTY}
    ...  pattern=(?mi)^[ \\t]*Phy[ \\t]*test[ \\t]*:[ \\t]*(?P<PASS>Passed)[ \\t]*$
    ...  msg=Failed for diagnostic management port ping test!


set new date/time to RTC chip
    [Documentation]  Write given new date/time to the RTC chip
    [Arguments]
    ...  ${console}=${diagos_mode}
    ...  ${new_date_time}=20181231 235959
    ...  ${path}=${diag_tools_path}

    execute command and verify exit code
    ...  console=${console}
    ...  command=(${diag_export_env}./cel-rtc-test -w -D '${new_date_time}')
    ...  path=${path}


verify the RTC chip is continue counting correctly
    [Documentation]  Verify the RTC chip is continue counting correctly
    [Arguments]
    ...  ${console}=${diagos_mode}
    ...  ${pattern}=(?mi)^Curr date info : 2019-01-01 \\d{2}:\\d{2}:\\d{2}  # It was written to 20181231 235959
    ...  ${path}=${diag_tools_path}

    execute command and verify with a pattern
    ...  console=${console}
    ...  command=(${diag_export_env}./cel-rtc-test -r)
    ...  path=${path}
    ...  pattern=${pattern}


diagnose I2C/loopback
    [Documentation]  diagnose I2C/loopback
    [Arguments]
    ...  ${console}=${diagos_mode}
    ...  ${command}=./cel-i2c-test --all
    ...  ${path}=${diag_tools_path}
    ...  ${pattern}=${i2c_diagnose_loopback_fail_pattern}

    ${status}  ${value}=  Run Keyword And Ignore Error  execute command and verify with a pattern for table
    ...  console=${console}
    ...  command=(${diag_export_env} ${command})
    ...  path=${path}
    ...  pattern=${pattern}
    ...  msg=Should not found the fail pattern!
    ...  is_check_exit_code=${FALSE}
    Run Keyword If  '${status}' == 'PASS'
    ...  Fail  Failed to verify diagnose I2C/loopback:${\n*2}Failed on number:bus${\n}${matches}


read and expected to see the mtd partition for U-Boot
    [Documentation]  read and expected to see the mtd partition for U-Boot
    [Arguments]
    ...  ${console}=${diagos_mode}
    ...  ${command}=cat /proc/mtd
    ...  ${path}=${diag_tools_path}
    ...  ${pattern}=${mtd_uboot_partition_pattern}

    execute command and verify with a pattern
    ...  console=${console}
    ...  command=${command}
    ...  path=${path}
    ...  pattern=${pattern}
    ...  msg=Failed, not found the mtd partition for uboot partition name

    set test variable  &{mtd_uboot_info}  &{match}

download new U-Boot's boot.img file used to flash to the mtd uboot partition
    [Documentation]  download U-Boot's boot.img by TFTP
    [Arguments]
    ...  ${console}=${diagos_mode}

    BusyBox TFTP get file
    ...  console=${console}
    ...  server=${tftp_server_ipv4}
    ...  where_to_download=${mtd_uboot_boot_img_download_location}
    ...  file=${mtd_uboot_boot_img_file}
    ...  save_to=${mtd_uboot_boot_img_save_location}


flash U-Boot's boot.img to the mtd uboot partition
    [Documentation]  flash U-Boot's boot.img to the mtd uboot partition
    [Arguments]
    ...  ${console}=${diagos_mode}
    ...  ${file}=${mtd_uboot_boot_img_file}
    ...  ${path}=${mtd_uboot_boot_img_save_location}
    ...  ${sec}=180

    execute command and verify exit code
    ...  console=${console}
    ...  command=(flashcp -v ${file} /dev/${mtd_uboot_info}[mtd_number])
    ...  path=${path}
    ...  sec=${sec}


reboot to verify the mtd uboot partition is bootable
    [Documentation]  reboot to verify the mtd uboot partition is bootable

    Kapok reboot to U-Boot and enter to Diag OS


#U-Boot TFTP download new boot.img and flash directly to NOR flash memory
#    [Documentation]  U-Boot download boot.img and flash to NOR flash chip (/dev/mtd0)
#    [Arguments]
#    ...  ${console}=${uboot_mode}
#    ...  ${command}=run bootupd
#    ...  ${sec}=120
#
#    execute command and verify exit code
#    ...  console=${console}
#    ...  command=${command}
#    ...  sec=${sec}


I2C bus scan stress test
    [Documentation]  I2C bus scan stress test
    [Arguments]
    ...  ${console}=${diagos_mode}
    ...  ${command}=./cel-i2c-test --all
    ...  ${path}=${diag_tools_path}
    ...  ${pattern}=${i2c_bus_scan_stress_pass_pattern}

    execute command and verify with a pattern
    ...  console=${console}
    ...  command=(${diag_export_env} ${command})
    ...  path=${path}
    ...  pattern=${pattern}
    ...  msg=Fail!I2C test Failed!
    ...  is_check_exit_code=${FALSE}


run all diagnostic test
    [Documentation]  run all diagnostic test
    [Arguments]
    ...  ${console}=${diagos_mode}
    ...  ${command}=./cel-all-test --all
    ...  ${path}=${diag_tools_path}
    ...  ${pattern}=${diagnose_test_all_fail_pattern}
    ...  ${sec}=900

    ${status}  ${value}=  Run Keyword And Ignore Error  execute command and verify with a pattern for table
    ...  console=${console}
    ...  command=(${diag_export_env} ${command})
    ...  path=${path}
    ...  pattern=${pattern}
    ...  msg=Should not found the fail pattern!
    ...  is_check_exit_code=${FALSE}
    ...  sec=${sec}
    Run Keyword If  '${status}' == 'PASS'
    ...  Fail  Failed for some command(s):${\n*2}Number:command name${\n}${matches}


QSFP-DD page select
    [Documentation]  QSFP-DD page select
    [Arguments]
    ...  ${console}=${diagos_mode}
    ...  ${bus}=1
    ...  ${command}=0x50 0x7f 0xff
    ...  ${msg}=Failed on bus number ${bus} while selecting page

    execute command and verify exit code
    ...  console=${console}
    ...  command=i2cset -y -f ${bus} ${command}
    ...  msg=${msg}


QSFP-DD page select for all modules
    [Documentation]  QSFP-DD page select for all modules
    [Arguments]
    ...  ${console}=${diagos_mode}
    ...  ${command}=0x50 0x7f 0xff

    FOR  ${module}  ${bus}  IN  &{qsfp_dd_port_bus_32_modules}
        QSFP-DD page select
        ...  console=${console}
        ...  bus=${bus}
        ...  command=${command}
        ...  msg=Failed on module number ${module} on bus number ${bus} while selecting page
    END


QSFP-DD read ModSelL pin status
    [Documentation]  QSFP-DD read ModSelL pin status
    [Arguments]
    ...  ${console}=${diagos_mode}
    ...  ${bus}=1
    ...  ${pattern}=(?m)^(?P<modsell>0x[0-9a-fA-F]{2})$
    ...  ${msg}=Failed on bus number ${bus} while reading QSFP-DD ModSelL

    execute command and verify with a pattern
    ...  console=${console}
    ...  command=i2cget -y -f ${bus} 0x50 0xe1
    ...  pattern=${pattern}
    ...  msg=${msg}
    ${modsell}=  Evaluate  hex(${match}[modsell] & 0x04)
    Run Keyword If  ${modsell} == 0x04
    ...  Fail  The bit number 2 is not zero!


QSFP-DD read ModSelL pin status for all modules
    [Documentation]  QSFP-DD read ModSelL pin status for all modules
    [Arguments]
    ...  ${console}=${diagos_mode}

    FOR  ${module}  ${bus}  IN  &{qsfp_dd_port_bus_32_modules}
        QSFP-DD read ModSelL pin status
        ...  console=${console}
        ...  bus=${bus}
        ...  msg=Failed on module number ${module} on bus number ${bus} while reading QSFP-DD ModSelL
    END


QSFP-DD set IntL
    [Documentation]  QSFP-DD set IntL
    [Arguments]
    ...  ${console}=${diagos_mode}
    ...  ${bus}=1
    ...  ${msg}=Failed on bus number ${bus} while setting IntL

    execute command and verify exit code
    ...  console=${console}
    ...  command=i2cset -y -f ${bus} 0x50 0xfe 0x20
    ...  msg=${msg}


QSFP-DD set IntL for all modules
    [Documentation]  QSFP-DD set IntL for all modules
    [Arguments]
    ...  ${console}=${diagos_mode}

    FOR  ${module}  ${bus}  IN  &{qsfp_dd_port_bus_32_modules}
        QSFP-DD set IntL
        ...  console=${console}
        ...  bus=${bus}
        ...  msg=Failed on module number ${module} on bus number ${bus} while setting IntL
    END


QSFP-DD verify IntL signal status
    [Documentation]  QSFP-DD verify IntL signal status
    [Arguments]
    ...  ${console}=${diagos_mode}
    ...  ${pattern}=(?m)^(?P<intl>\\d)$  # Accepted for all (0 or 1)
    ...  ${module}=1
    ...  ${command}=${cat_intl_signal_cmd_start}${module}${cat_intl_signal_cmd_end}
    ...  ${msg}=Failed, it does not expected signal status for module number ${module}

    execute command and verify with a pattern
        ...  console=${console}
        ...  command=${command}
        ...  pattern=${pattern}
        ...  msg=${msg}


QSFP-DD verify IntL signal status for all modules
    [Documentation]  QSFP-DD verify IntL signal status for all modules
    [Arguments]
    ...  ${console}=${diagos_mode}
    ...  ${pattern}=(?m)^(?P<intl>\\d)$  # Accepted for all (0 or 1)

    FOR  ${module}  ${bus}  IN  &{qsfp_dd_port_bus_32_modules}
        QSFP-DD verify IntL signal status
        ...  console=${console}
        ...  pattern=${pattern}
        ...  msg=Failed on module number ${module} on bus number ${bus} while verifying IntL signal
    END


QSFP-DD clear IntL
    [Documentation]  QSFP-DD clear IntL
    [Arguments]
    ...  ${console}=${diagos_mode}
    ...  ${bus}=1
    ...  ${msg}=Failed on bus number ${bus} while clear IntL

    execute command and verify exit code
    ...  console=${console}
    ...  command=i2cset -y -f ${bus} 0x50 0xfe 0x30
    ...  msg=${msg}


QSFP-DD clear IntL for all modules
    [Documentation]  QSFP-DD clear IntL for all modules
    [Arguments]
    ...  ${console}=${diagos_mode}

    FOR  ${module}  ${bus}  IN  &{qsfp_dd_port_bus_32_modules}
        QSFP-DD clear IntL
        ...  console=${console}
        ...  bus=${bus}
        ...  msg=Failed on module number ${module} on bus number ${bus} while clear IntL
    END


QSFP-DD set high power mode
    [Documentation]  QSFP-DD set high power mode
    [Arguments]
    ...  ${console}=${diagos_mode}
    ...  ${bus}=1
    ...  ${command}=0x50 0xc8 0x80
    ...  ${msg}=Failed on bus number ${bus} while setting high power mode

    execute command and verify exit code
    ...  console=${console}
    ...  command=i2cget -y -f ${bus} ${command}
    ...  msg=${msg}

QSFP-DD set high power mode for all modules
    [Documentation]  QSFP-DD set high power mode for all modules
    [Arguments]
    ...  ${console}=${diagos_mode}
    ...  ${command}=0x50 0xc8 0x80

    FOR  ${module}  ${bus}  IN  &{qsfp_dd_port_bus_32_modules}
        QSFP-DD set high power mode
        ...  console=${console}
        ...  bus=${bus}
        ...  command=${command}
        ...  msg=Failed on module number ${module} on bus number ${bus} while setting high power mode
    END


QSFP-DD set power mode for all modules
    [Documentation]  QSFP-DD set power mode for all modules
    [Arguments]
    ...  ${command}
    ...  ${console}=${diagos_mode}

    FOR  ${module}  ${bus}  IN  &{qsfp_dd_port_bus_32_modules}
        QSFP-DD set high power mode
        ...  console=${console}
        ...  bus=${bus}
        ...  command=${command}
        ...  msg=Failed on module number ${module} on bus number ${bus} while setting high power mode
    END


QSFP-DD reset modules
    [Documentation]  QSFP-DD reset modules
    [Arguments]
    ...  ${console}=${diagos_mode}
    ...  ${module}=1
    ...  ${command}=echo 1 > /sys/bus/i2c/devices/15-0060/port${module}_module_reset && echo 0 > /sys/bus/i2c/devices/15-0060/port${module}_module_reset
    ...  ${msg}=Failed, it does not low power mode for module number ${module}!

    execute command and verify exit code
        ...  console=${console}
        ...  command=(${command})
        ...  msg=${msg}

QSFP-DD lpmode modules
    [Documentation]  QSFP-DD lpmode modules
    [Arguments]
    ...  ${console}=${diagos_mode}
    ...  ${command}=${command1}
    ...  ${msg}=Failed, it does not low power or high power mode for all modules!

    execute command and verify exit code
        ...  console=${console}
        ...  command=(${command})
        ...  msg=${msg}

QSFP optical module resetl signal
    [Documentation]  QSFP optical module resetl signal
    [Arguments]
    ...  ${command1}
    ...  ${command2}
    ...  ${pattern}
    ...  ${console}=${diagos_mode}

    change directory  console=${console}  dir=${diag_tools_path}
    FOR  ${module}  ${bus}  IN  &{qsfp_dd_port_bus_32_modules}
        QSFP-DD reset modules
        ...  console=${console}
        ...  module=${module}
        ...  command=${command1}
        ...  msg=Failed on module number ${module} on bus number ${bus} while setting to low power mode!

        execute command and verify with a pattern
        ...  console=${console}
        ...  command=${command2}
        ...  path=${diag_tools_path}
        ...  pattern=${pattern}
        ...  msg=Failed, can't reset qsfp reset module
    END

QSFP optical module lpmode signal
    [Documentation]  QSFP optical module lpmode signal
    [Arguments]
    ...  ${command1}
    ...  ${command2}
    ...  ${pattern}
    ...  ${console}=${diagos_mode}

    change directory  console=${console}  dir=${diag_tools_path}

    QSFP-DD lpmode modules
        ...  console=${console}
        ...  command=${command1}
        ...  msg=Failed, can't set qsfp lpmode/hpmode module

    FOR  ${module}  ${bus}  IN  &{qsfp_dd_port_bus_32_modules}
        execute command and verify with a pattern
        ...  console=${console}
        ...  command=i2cget -y -f ${bus} ${command2}
        ...  path=${diag_tools_path}
        ...  pattern=${pattern}
        ...  msg=Failed on module number ${module} on bus number ${bus} while setting to low power mode!
    END

QSFP-DD reset for all modules
    [Documentation]  QSFP-DD reset for all modules
    [Arguments]
    ...  ${console}=${diagos_mode}

    FOR  ${module}  ${bus}  IN  &{qsfp_dd_port_bus_32_modules}
        QSFP-DD reset modules
        ...  console=${console}
        ...  module=${module}
        ...  msg=Failed on module number ${module} on bus number ${bus} while setting to low power mode!
    END


QSFP-DD verify low power mode
    [Documentation]  QSFP-DD verify low power mode
    [Arguments]
    ...  ${console}=${diagos_mode}
    ...  ${pattern}=(?m)^(?P<low_power>0x[0-9a-fA-F]{2})$
    ...  ${module}=1
    ...  ${command}=cat /sys/bus/i2c/devices/15-0060/port${module}_module_reset
    ...  ${msg}=Failed, it does not low power mode on module number ${module}

    execute command and verify with a pattern
        ...  console=${console}
        ...  command=${command}
        ...  pattern=${pattern}
        ...  msg=${msg}


QSFP-DD verify low power mode for all modules
    [Documentation]  QSFP-DD verify low power mode for all modules
    [Arguments]
    ...  ${console}=${diagos_mode}
    ...  ${pattern}=(?m)^(?P<low_power>0)$

    FOR  ${module}  ${bus}  IN  &{qsfp_dd_port_bus_32_modules}
        QSFP-DD verify low power mode
        ...  console=${console}
        ...  pattern=${pattern}
        ...  msg=Failed on module number ${module} on bus number ${bus} while waiting for low power mode reset!
    END

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

Detect all PCIe devices on the BUS
    [Documentation]  Detect all PCIe devices on the BUS
    [Arguments]
    ...  ${console}=${diagos_mode}
    ...  ${command}=./cel-pci-test --all
    ...  ${path}=${diag_tools_path}
    ...  ${pattern}=${diagnose_pci_detect_fail_pattern}
    ...  ${sec}=30

    ${status}  ${value}=  Run Keyword And Ignore Error  execute command and verify with a pattern for table
    ...  console=${console}
    ...  command=(${diag_export_env} ${command})
    ...  path=${path}
    ...  pattern=${pattern}
    ...  msg=Should not found the fail pattern!
    ...  is_check_exit_code=${FALSE}
    ...  sec=${sec}
    Run Keyword If  '${status}' != 'PASS'
    ...  Fail  Didn't find pass info
