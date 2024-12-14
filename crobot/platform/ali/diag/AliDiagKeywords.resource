###############################################################################
# LEGALESE:   "Copyright (C) 2019-2021, Celestica Corp. All rights reserved." #
#                                                                             #
# This source code is confidential, proprietary, and contains trade           #
# secrets that are the sole property of Celestica Corp.                       #
# Copy and/or distribution of this source code or disassembly or reverse      #
# engineering of the resultant object code are strictly forbidden without     #
# the written consent of Celestica Corp.                                      #
#                                                                             #
###############################################################################

*** Keywords ***
Verify all fan eeproms by eeprom tool
    [Documentation]  Read the all fan EEPROMs content by eeprom tool
    [Arguments]
    ...  ${console}=${openbmc_mode}
    ...  ${path}=${openbmc_fan_fru_eeprom_path}
    ...  ${command}=./eeprom_tool -d -f
    ...  ${patterns}=${regularly_unexpected_patterns}
    ...  ${msg}=Failed to verify for fan FRU eeprom(s)!
    ...  ${start}=1
    ...  ${stop}=5

    FOR  ${eeprom}  IN RANGE  ${start}  ${stop}+1  1
        execute command and verify with unexpected patterns
        ...  console=${console}
        ...  command=${command} ${eeprom}
        ...  patterns=${patterns}
        ...  path=${path}
        ...  msg=${msg}
    END


Verify all fan eeproms by FRU tool
    [Documentation]  Read the all fan EEPROMs content by FRU tool
    [Arguments]
    ...  ${console}=${openbmc_mode}
    ...  ${path}=${EMPTY}
    ...  ${command}=fru-util fan
    ...  ${patterns}=${regularly_unexpected_patterns}
    ...  ${msg}=Failed to verify for fan FRU eeprom(s)!
    ...  ${start}=1
    ...  ${stop}=5

    FOR  ${eeprom}  IN RANGE  ${start}  ${stop}+1  1
        execute command and verify with unexpected patterns
        ...  console=${console}
        ...  command=${command} ${eeprom}
        ...  patterns=${patterns}
        ...  path=${path}
        ...  msg=${msg}
    END


Verify all PSU status
    [Documentation]  Read all PSU status
    [Arguments]
    ...  ${console}=${openbmc_mode}
    ...  ${path}=${openbmc_diag_bin_path}
    ...  ${command}=./cel-psu-test -s -p
    ...  ${start}=1
    ...  ${stop}=4

    FOR  ${psu}  IN RANGE  ${start}  ${stop}+1  1
        execute command and verify with a pattern
        ...  console=${console}
        ...  path=${path}
        ...  command=${command} ${psu}
        ...  pattern=(?m)^PSU_(?P<psu_present_number>${psu}) Present
        ...  msg=Failed the PSU number ${psu} is not present!${\n}or it may return non-zero exit code!
    END


Write CPLD register
    [Tags]  flatten-keyword
    [Arguments]
    ...  ${command}
    ...  ${console}=${diagos_mode}
    ...  ${path}=${diagos_cpu_diag_path}
    ...  ${pattern}=wirte reg: (?P<addr>0x[a-fA-F0-9]+) (?P<data>0x[a-fA-F0-9]+)
    ...  ${msg}=Failed to write or verify it!

    execute command and verify with a pattern
    ...  console=${console}
    ...  path=${path}
    ...  command=${command}
    ...  pattern=${pattern}
    ...  msg=${msg}
    set test variable  &{cpld_written}  &{match}


find I2C device number by i2cdetect
    [Tags]  flatten-keyword
    [Arguments]
    ...  ${console}=${diagos_mode}
    ...  ${command}=i2cdetect -l | wc -l
    ...  ${pattern}=(?m)^(?P<number>\\d+)$
    ...  ${msg}=Failed, can not find the number of I2C devices!

    execute command and verify with a pattern
    ...  console=${console}
    ...  command=${command}
    ...  pattern=${pattern}
    ...  msg=${msg}
    set test variable  ${i2cdetect_dev}  ${match}


find I2C device number by diagtool
    [Tags]  flatten-keyword
    [Arguments]
    ...  ${console}=${diagos_mode}
    ...  ${path}=${diagos_cpu_diag_path}
    ...  ${command}=./cel-i2c-test -l
    ...  ${pattern}=(?P<i2c_path>/sys/bus/i2c/devices/\\d+-\\w+)
    ...  ${msg}=Failed, can not find the number of I2C devices!

    execute command and verify with a pattern for table
    ...  console=${console}
    ...  path=${path}
    ...  command=${command}
    ...  pattern=${pattern}
    ...  msg=${msg}
    ${diagtool_dev_number}=  Get Length  ${matches}
    set test variable  ${diagtool_dev_number}


force to switch boot source
    [Arguments]
    ...  ${console}=${openbmc_mode}
    ...  ${switch_to_pattern}=Slave FLash
    ...  ${switch_to_command}=(source /usr/local/bin/openbmc-utils.sh && boot_from slave)
    ...  ${boot_msg}= login:
    ...  ${boot_wait}=360  # 6 mins
    ...  ${msg}=msg=Failed, current boot is not "${switch_to_pattern}"!

    find current boot source
    run keyword if  '${current_boot}[current_boot]' != '${switch_to_pattern}'
    ...  Run Keywords
    ...  send a line  command=${switch_to_command}  AND
    ...  read until pattern  pattern=${boot_msg}  sec=${boot_wait}  AND
    ...  Sleep  45s  AND  # Wait for some terrible I2C bus add messages
    ...  find current boot source
    ...  pattern=Current Boot Code Source:[ \\t]+(?P<current_boot>${switch_to_pattern})
    ...  msg=${msg}


force to switch BIOS boot source
    [Arguments]
    ...  ${console}=${openbmc_mode}
    ...  ${switch_to_pattern}=Master flash
    ...  ${switch_to_command}=(source /usr/local/bin/openbmc-utils.sh && come_reset slave)
    ...  ${boot_msg}= login:
    ...  ${boot_wait}=${30 * 60}
    ...  ${msg}=Failed, can not switch to ${switch_to_pattern}!
    ...  ${force_reboot}=${FALSE}

    find BIOS boot source  console=${console}
    run keyword if  '${bios_current_boot}[bios_boot_source]' != '${switch_to_pattern}' or '${force_reboot}' == '${TRUE}'
    ...  Run Keywords
    ...  send a line  command=${switch_to_command}  AND
    ...  OpenBMC switch to SONiC console  AND
    ...  read until pattern  pattern=${boot_msg}  sec=${boot_wait}  AND
    ...  set test variable  ${bootup_text}  ${text}  AND
    ...  Run Keyword And Ignore Error  open prompt and login to root user  console=${openbmc_mode}  AND
    ...  Run Keyword And Ignore Error  change kernel log level  console=${openbmc_mode}  level=3  AND
    ...  Sleep  45s  AND  # Wait for some terrible I2C bus add messages
    ...  find BIOS boot source  console=${console}
    ...  pattern=(?i)COMe CPU boots from BIOS (?P<bios_boot_source>${switch_to_pattern})
    ...  msg=${msg}


Verify QSFP specific status
    [Tags]  flatten-keyword
    [Arguments]
    ...  ${command}
    ...  ${pattern}
    ...  ${number_of_qsfp}
    ...  ${msg}
    ...  ${console}=${diagos_mode}
    ...  ${path}=${diagos_cpu_diag_path}

    execute command and verify with a pattern for table
    ...  console=${console}
    ...  command=${command}
    ...  path=${path}
    ...  pattern=${pattern}

    Length Should Be  item=${matches}  length=${number_of_qsfp}  msg=${msg}


Verify all QSFP one-by-one port specific status
    [Arguments]
    ...  ${pattern}
    ...  ${msg}
    ...  ${command}
    ...  ${command_to_verify}=./cel-port-test -s
    ...  ${start}=1
    ...  ${stop}=128
    ...  ${console}=${diagos_mode}
    ...  ${path}=${diagos_cpu_diag_path}

    FOR  ${port}  IN RANGE  ${start}  ${stop}+1  1
        execute command and verify exit code
        ...  console=${console}
        ...  command=${command} ${port}
        ...  path=${path}

        execute command and verify with a pattern
        ...  console=${console}
        ...  command=${command_to_verify}
        ...  path=${path}
        ...  pattern=(?mi)^[ \\t]+(?P<number>${port})${pattern}
        ...  msg=${msg}${\n}On the QSFP Port Number ${port}
    END


Verify SDK pass count
    [Tags]  flatten-keyword
    ${text}=  read until regexp  patterns=BCM.0>  timeout=60
    search for a pattern
    ...  text=${text}
    ...  pattern=TOTAL[ \\t\\|]+\\d+[ \\t\\|]+(?P<run_count>\\d+)[ \\t\\|]+(?P<pass_count>\\d+)
    ...  msg=Failed not found run count and/or pass count!
    Should Be Equal As Strings
    ...  first=${match}[run_count]
    ...  second=${match}[pass_count]
    ...  msg=Failed "run count" does not match "pass count"!


Edit EEPROM configulation file
    [Arguments]
    ...  ${path}
    ...  ${console}=${openbmc_mode}
    ...  ${file}=eeprom.cfg
    ...  &{items}=${EMPTY}

    FOR  ${key}  ${value}  IN  &{items}
        # Update/edit configuration file and verify it
        file edit and replace a line
        ...  console=${console}
        ...  file=${file}
        ...  sed_pattern=s/${key}.*$/${key}=${value}/g
        ...  path=${path}
        execute command and verify with a pattern
        ...  console=${console}
        ...  path=${path}
        ...  command=cat ${file}
        ...  pattern=${key}=(?P<${key}>${value})
        ...  msg=Failed to edit ${file}/parameter name "${key}" and value "${value}"
    END


fru-util dump and verify
    [Tags]  flatten-keyword
    [Arguments]
    ...  ${console}
    ...  ${path}
    ...  ${command}
    ...  ${patterns}
    ...  ${original}

    execute command and verify with unordered pattern list
    ...  console=${console}
    ...  command=${command}
    ...  patterns=${patterns}
    set test variable  &{fru_util_info}  &{matches}
    compare two dictionaries with matched key
    ...  original=&{original}
    ...  compare=&{fru_util_info}
    ...  msg=Failed, the eeprom.cfg does not match with fru-util dump info!


Edit eeprom.cfg, write, update and dump to verify
    [Arguments]
    ...  ${log_msg_header}
    ...  ${path}
    ...  ${eeprom_tool_dump}
    ...  ${eeprom_tool_write}
    ...  ${eeprom_tool_update}
    ...  ${fru_util_dump}=${EMPTY}
    ...  ${console}=${openbmc_mode}
    ...  ${eeprom_tool_dump_patterns}=${openbmc_fru_info_patterns}
    ...  ${fru_util_dump_patterns}=${openbmc_fru_info_patterns}

    Log  ${log_msg_header}  console=${TRUE}
    execute command and verify with unordered pattern list
    ...  console=${console}
    ...  path=${path}
    ...  command=${eeprom_tool_dump}
    ...  patterns=${eeprom_tool_dump_patterns}
    set test variable  &{eeprom_tool_info_original}  &{matches}

    Run Keyword If  '${fru_util_dump}' != '${EMPTY}'
    ...  fru-util dump and verify
    ...  console=${console}
    ...  path=${path}
    ...  command=${fru_util_dump}
    ...  patterns=${fru_util_dump_patterns}
    ...  original=&{eeprom_tool_info_original}
    set test variable  &{fru_util_info_original}  &{matches}

    # Edit eeprom.cfg
    ${eeprom_cfg_edited}=  Copy Dictionary  ${eeprom_tool_info_original}  deepcopy=${TRUE}

    Set To Dictionary  ${eeprom_cfg_edited}
    ...  manufacturer  Celestica Limitless Company

    Edit EEPROM configulation file
    ...  path=${path}
    ...  items=&{eeprom_cfg_edited}

    # Write & update eeprom.cfg
    execute command and verify exit code
    ...  console=${console}
    ...  path=${path}
    ...  command=${eeprom_tool_write}
    ...  msg=Failed to write eeprom.cfg
    execute command and verify exit code
    ...  console=${openbmc_mode}
    ...  path=${path}
    ...  command=${eeprom_tool_update}
    ...  msg=Failed to update eeprom.cfg

    # eepromtool: dump to compare it
    execute command and verify with unordered pattern list
    ...  console=${console}
    ...  path=${path}
    ...  command=${eeprom_tool_dump}
    ...  patterns=${eeprom_tool_dump_patterns}
    set test variable  &{eeprom_tool_info_edited}  &{matches}
    compare two dictionaries with matched key
    ...  original=&{eeprom_cfg_edited}
    ...  compare=&{eeprom_tool_info_edited}
    ...  msg=Failed, the edited eeprom.cfg does not match with eepromtool dump info!

    # fru-util: show info to compare it
    Run Keyword If  '${fru_util_dump}' != '${EMPTY}'
    ...  fru-util dump and verify
    ...  console=${console}
    ...  path=${path}
    ...  command=${fru_util_dump}
    ...  patterns=${fru_util_dump_patterns}
    ...  original=&{eeprom_cfg_edited}

    # Hard reboot
    power cycle to mode  mode=${console}

    # eepromtool: dump to compare it
    execute command and verify with unordered pattern list
    ...  console=${openbmc_mode}
    ...  path=${path}
    ...  command=${eeprom_tool_dump}
    ...  patterns=${eeprom_tool_dump_patterns}
    set test variable  &{eeprom_tool_info_edited_reboot}  &{matches}
    compare two dictionaries with matched key
    ...  original=&{eeprom_cfg_edited}
    ...  compare=&{eeprom_tool_info_edited_reboot}
    ...  msg=Failed, the eeprom.cfg does not match with eepromtool dump info after reboot!

    # fru-util: show info to compare it
    Run Keyword If  '${fru_util_dump}' != '${EMPTY}'
    ...  fru-util dump and verify
    ...  console=${console}
    ...  path=${path}
    ...  command=${fru_util_dump}
    ...  patterns=${fru_util_dump_patterns}
    ...  original=&{eeprom_cfg_edited}

    [Teardown]  Run Keywords
    # Also needed to restore original info here
    ...  Edit EEPROM configulation file  path=${path}  items=&{eeprom_tool_info_original}  AND
    ...  execute command and verify exit code  console=${console}  path=${path}  command=${eeprom_tool_write}  msg=Failed to write eeprom.cfg  AND
    ...  execute command and verify exit code  console=${console}  path=${path}  command=${eeprom_tool_update}  msg=Failed to update eeprom.cfg  AND
    # eepromtool: dump to compare it
    ...  execute command and verify with unordered pattern list  console=${console}  path=${path}  command=${eeprom_tool_dump}  patterns=${eeprom_tool_dump_patterns}  AND
    ...  set test variable  &{eeprom_tool_info_teardown}  &{matches}  AND
    ...  compare two dictionaries with matched key  original=&{eeprom_tool_info_original}  compare=&{eeprom_tool_info_teardown}  msg=Failed, the eeprom.cfg does not match with eepromtool dump info!  AND
    # fru-util: show info to compare it
    ...  Run Keyword If  '${fru_util_dump}' != '${EMPTY}'  fru-util dump and verify  console=${console}  path=${path}  command=${fru_util_dump}  patterns=${fru_util_dump_patterns}  original=&{fru_util_info_original}


find OpenBMC version
    [Tags]  flatten-keyword
    [Arguments]
    ...  ${pattern}=^OpenBMC Release.*?v(?P<openbmc_version>.*)$

    execute command and verify with a pattern
    ...  console=${openbmc_mode}
    ...  command=version_dump
    ...  pattern=${pattern}
    ...  msg=Failed, not found OpenBMC version!
    set test variable  ${openbmc_version}  ${match}


Update OpenBMC on COMe
    [Arguments]
    ...  ${where_to_download}=${bmc_path}
    ...  ${image_name}=${bmc_old_image}
    ...  ${save_to}=${bmc_save_to}
    ...  ${image_version}=0.0.0
    ...  ${switch_pattern}=Slave Flash
    ...  ${boot_from}=slave
    ...  ${flash_cs}=0

    force to switch boot source
    ...  switch_to_pattern=${switch_pattern}
    ...  switch_to_command=(source /usr/local/bin/openbmc-utils.sh && boot_from ${boot_from})
    DiagOS renew IP using DHCP and set variable
    secure copy file
    ...  console=${diagos_mode}
    ...  username=${scp_username}
    ...  password=${scp_password}
    ...  source_ip=${ssh_server_ipv4}
    ...  source_path=${where_to_download}
    ...  source_file=${image_name}
    ...  destination=${save_to}
    ...  sec=${6 * 60}
    ...  always_copy=${TRUE}
    execute command and verify exit code
    ...  console=${diagos_mode}
    ...  command=(printf "y\n" | ./socflash_x64 -s if="${save_to}/${image_name}" option=l lpcport=0x2e cs=${flash_cs})
    ...  path=/usr/local/migaloo/utility
    ...  msg=Failed to write OpenBMC image!
    ...  sec=${20 * 60}
    open prompt  console=${openbmc_mode}  sec=${8 * 60}
    Sleep  120s  # Wait for some terrible I2C bus add messages
    force to switch boot source
    ...  switch_to_pattern=${switch_pattern}
    ...  switch_to_command=(source /usr/local/bin/openbmc-utils.sh && boot_from ${boot_from})
    execute command and verify exit code
    ...  path=${diagos_sdk_path}
    ...  console=${diagos_mode}
    ...  command=pkill bcm.user
    ...  exit_code_pattern=(?m)^(?P<exit_code>\\d+)$
    find OpenBMC version
    ...  pattern=^OpenBMC Release.*?v(?P<openbmc_version>${image_version})$
    find current boot source
    ...  pattern=Current Boot Code Source:[ \\t]+(?P<current_boot>${switch_pattern})
    ...  msg=Failed, OpenBMC does not boot-up from ${boot_from}!


OOB menu/help verify
    [Tags]  flatten-keyword
    [Arguments]
    ...  ${oob_console}=${openbmc_mode}
    ...  ${oob_command}=./cel-OOB-test -h
    ...  ${oob_patterns}=${option_h_and_a_patterns}
    ...  ${oob_path}=${openbmc_diag_bin_path}

    execute command and verify with ordered pattern list
    ...  console=${oob_console}
    ...  command=${oob_command}
    ...  patterns=${oob_patterns}
    ...  path=${oob_path}
    ...  msg=Failed to verify help option!


OOB menu/auto-test
    [Tags]  flatten-keyword
    [Arguments]
    ...  ${oob_console}=${openbmc_mode}
    ...  ${oob_command}=${openbmc_oob_test_command}
    ...  ${oob_patterns}=(?mi)^[ \\\\t]*OOB Test[ \\\\.]+.*(?P<result>PASS)
    ...  ${oob_path}=${openbmc_diag_bin_path}

    execute command and verify with a pattern
    ...  console=${oob_console}
    ...  command=${oob_command}
    ...  pattern=${oob_patterns}
    ...  msg=Failed to test OOB!


If network does not work take a reboot
    OpenBMC renew IP using DHCP and set variable
    ${status}  ${value}=  Run Keyword And Ignore Error
    ...  ping to IP  console=${openbmc_mode}  ip=${tftp_server_ipv4}
    Run Keyword If  '${status}' == 'FAIL'
    ...  powerCycleToOpenbmc


Verify PCIe list of device is all exist by lspci tool
    [Arguments]  &{devices}=${EMPTY}

    FOR  ${key}  ${value}  IN  &{devices}
        execute command and verify exit code
        ...  console=${diagos_mode}
        ...  command=lspci -s ${value} -vvvxxx
        ...  path=${diagos_cpu_diag_path}
        ...  msg=Failed, not found the PCIe device "${value}"!
        ...  sec=${2 * 60}
    END


Total memory byte by dmidecode
    [Tags]  flatten-keyword
    [Arguments]
    ...  ${console}=${diagos_mode}

    ${dmimem_k_bytes}=  set variable  ${0}
    ${matched_n}=  set variable  ${1}

    execute command and verify with a pattern for table
    ...  console=${diagos_mode}
    ...  command=(dmidecode -t memory | grep -i Size)
    ...  pattern=(?P<MB>\\d+) MB
    ...  msg=Failed, not found the dmidecode memory size!
    FOR  ${mem}  IN  ${matches}
        set test variable  ${dmimem_k_bytes}  ${${${mem}[MB_${matched_n}] * 1024} + ${dmimem_k_bytes}}
        ${matched_n}=  set variable  ${matched_n + 1}
    END


set high power according to port number
    [Tags]  flatten-keyword
    [Arguments]
    ...  ${console}=${diagos_mode}

    execute command and verify with a pattern for table
    ...  console=${console}
    ...  command=./luxshare_power_config.sh -p
    ...  pattern=set (port|i2cbus)_\\d+ power: (?P<pwr>[\\d\\.]+)W
    ...  path=${diagos_diag_utility_path}
    ...  msg=Failed to set all or some port according to its max power!
    ...  sec=${5 * 60}

    FOR  ${index}  ${key}  ${pwr}  IN ENUMERATE  &{matches}
        # ${index + 1} = port number
        RUN KEYWORD IF  ${index + 1} <= ${8}
        ...  Should Be Equal As Numbers
        ...  first=5
        ...  second=${pwr}
        ...  msg=Port 1 - 8 are not all 5W!
        ...  precision=${1}
        ...  ELSE IF  ${index + 1} <= ${32}
        ...  Should Be Equal As Numbers
        ...  first=2.5
        ...  second=${pwr}
        ...  msg=Port 9 - 32 are not all 2.5W!
        ...  precision=${1}
        ...  ELSE IF  ${index + 1} <= ${40}
        ...  Should Be Equal As Numbers
        ...  first=5
        ...  second=${pwr}
        ...  msg=Port 33 - 40 are not all 5W!
        ...  precision=${1}
        ...  ELSE
        ...  Fail  Failed, the port number is out-of-range!
    END
