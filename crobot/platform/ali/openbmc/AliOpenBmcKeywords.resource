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

*** Settings ***
Resource        CommonKeywords.resource
Resource        sdk/AliSdkKeywords.resource
Library         sdk/AliSdkLib.py

*** Keywords ***

dump software version
    [Documentation]  OpenBMC version dump
    [Arguments]
    ...  ${console}=${openbmc_mode}
    ...  ${command}=version_dump

    execute command and set test variable
    ...  console=${console}
    ...  command=${command}


verify boot source
    [Documentation]  verify current boot source
    [Arguments]
    ...  ${console}=${openbmc_mode}
    ...  ${command}=boot_info.sh
    ...  ${pattern}=(?m)^[ \\t]*Current[ \\t]+Boot[ \\t]+Code[ \\t]+Source:[ \\t]*(?P<boot_source>[ \\w]+)$

    execute command and verify with a pattern
    ...  console=${console}
    ...  command=${command}
    ...  pattern=${pattern}
    ...  msg=Failed to verify the boot source!


update master bmc cross version
    [Arguments]
    ...  ${isUpgrade}
    prepare image  ${bmc_local_image_path}  BMC  upgrade=${isUpgrade}
    ${did_updated}  ${version}=  update bmc  master  ${isUpgrade}
    Return From Keyword If  ${did_updated} == ${0}
    &{version_dict} =	Create Dictionary	BMC Version=${version}
    check cpu alive  path=${cpu_test_path}
    reboot openbmc and check version  ${version_dict}
    check cpu alive  path=${cpu_test_path}


update master bmc
    [Arguments]
    ...  ${isUpgrade}
    check cpu alive  True  ${cpu_test_path}
    prepare image  ${bmc_local_image_path}  BMC  upgrade=${isUpgrade}
    ${did_updated}  ${version}=  update bmc  master  ${isUpgrade}
    Return From Keyword If  ${did_updated} == ${0}
    &{version_dict} =	Create Dictionary	BMC Version=${version}
    check cpu alive  path=${cpu_test_path}
    reboot openbmc and check version  ${version_dict}
    check cpu alive  path=${cpu_test_path}
    power cycle and check version  ${version_dict}


update slave bmc
    [Arguments]
    ...  ${isUpgrade}
    check cpu alive  True  ${cpu_test_path}
    prepare image  ${bmc_local_image_path}  BMC  upgrade=${isUpgrade}
    ${did_updated}  ${version}=  update bmc  slave  ${isUpgrade}  forceUpdate=True
    Return From Keyword If  ${did_updated} == ${0}
    &{version_dict} =	Create Dictionary	BMC Version=${version}
    check cpu alive  path=${cpu_test_path}
    switch bmc flash  slave
    Run Keyword And Ignore Error  change kernel log level  console=${openbmc_mode}  level=3
    verify fw version  BMC  ${version_dict}
    verify current boot flash  BMC  slave
    BuiltIn.Sleep  30
    check eth ports  ${interface_list}
    verify mac address  ${default_interface}
    check cpu alive  path=${cpu_test_path}
    switch bmc flash  master
    Run Keyword And Ignore Error  change kernel log level  console=${openbmc_mode}  level=3
    verify fw version  BMC  ${bmc_version_dict}
    verify current boot flash  BMC  master
    BuiltIn.Sleep  30
    check eth ports  ${interface_list}
    verify mac address  ${default_interface}
    check cpu alive  path=${cpu_test_path}
    power cycle and check version  ${bmc_version_dict}


reboot openbmc and check version
    [Arguments]  ${bmc_version_dict}
    reboot openbmc  timeout=600
    Run Keyword And Ignore Error  change kernel log level  console=${openbmc_mode}  level=3
    verify fw version  BMC  ${bmc_version_dict}
    verify current boot flash  BMC  master
    BuiltIn.sleep  60
    check eth ports  ${interface_list}
    verify mac address  ${default_interface}


power cycle and check version
    [Arguments]  ${bmc_version_dict}
    power cycle to openbmc  timeout=600
    Run Keyword And Ignore Error  change kernel log level  console=${openbmc_mode}  level=3
    verify fw version  BMC  ${bmc_version_dict}
    verify current boot flash  BMC  master
    BuiltIn.Sleep  30
    check eth ports  ${interface_list}
    verify mac address  ${default_interface}


#### @WORKAROUND to recover openbmc network, because OpenBMC cannot get the IP by itself
check and flush eth0 interface
    [Arguments]
    ...  ${console}=${openbmc_mode}
    ${server_ip}=  get ip address from config  PC
    ${status}  ${value}=  Run Keyword And Ignore Error  execute command and verify with a pattern
    ...  console=${console}
    ...  command=ping ${server_ip} -c 5
    ...  pattern=(?i)(?P<ping_result>, 0% packet loss)
    ...  is_check_exit_code=${FALSE}
    Run Keyword If  '${status}' == 'FAIL'
    ...  Run Keywords  flush network interface  console=${console}  interface=eth0
    ...  AND  BuiltIn.Sleep  10

prepare image
    [Arguments]
    ...  ${localImageDir}
    ...  ${image}
    ...  ${console}=${openbmc_mode}
    ...  ${upgrade}=True
    ...  ${bmc_flash}=master
    switch bmc flash  ${bmc_flash}
    BuiltIn.Sleep  50
    create dir  ${localImageDir}  ${console}
    check and flush eth0 interface  ${console}  #### @WORKAROUND to recover openbmc network
    get dhcp ip address  DUT  eth0  ${console}
    BuiltIn.Sleep  10
    download image  DUT  ${image}  upgrade=${upgrade}


prepare CPLD images
    [Arguments]
    ...  ${isUpgrade}
    switch bmc flash  Master
    create dir  ${cpld_local_image_path}  OPENBMC
    check and flush eth0 interface  #### @WORKAROUND to recover openbmc network
    get dhcp ip address  DUT  eth0  OPENBMC
    BuiltIn.Sleep  10
    download image  DUT  BASE_CPLD   upgrade=${isUpgrade}
    download image  DUT  COME_CPLD  upgrade=${isUpgrade}
    download image  DUT  FAN_CPLD  upgrade=${isUpgrade}
    download image  DUT  SWITCH_CPLD  upgrade=${isUpgrade}

clean images CPLD
    clean images  DUT  BASE_CPLD
    clean images  DUT  COME_CPLD
    clean images  DUT  FAN_CPLD
    clean images  DUT  SWITCH_CPLD
    clean images  DUT  FAN_CPLD_REFRESH
    clean images  DUT  BASE_CPLD_REFRESH
    clean images  DUT  CPU_CPLD_REFRESH

update cpld in bmc
    [Arguments]
    ...  ${isUpgrade}
    prepare CPLD images  ${isUpgrade}
    verify current boot flash  BMC  master
    clear log  ${openbmc_mode}  ${syslog_path}
    ${version}=  update cpld  ${isUpgrade}
    ${length} =  Get Length  ${version}
    Return From Keyword If  ${length} == 0
    verify power status  on
    execute command and verify with unordered pattern list
    ...  console=${openbmc_mode}
    ...  command=${fpga_update_log_cmd}
    ...  patterns=${cpld_update_log_patterns}
    ...  msg=Failed to verify ${fpga_update_log_cmd}!
    refresh cpld
    check fpga ctrl bit
    BuiltIn.Sleep  240
    verify fw version  CPLD  ${version}
    execute command and verify with ordered pattern list
    ...  console=${openbmc_mode}
    ...  command=${refresh_cpld_log_cmd}
    ...  patterns=${refresh_fw_log_patterns}
    ...  msg=Failed to verify ${refresh_cpld_log_cmd}!

refresh cpld
    [Arguments]
    ...  ${image_path}=${cpld_local_image_path}
    ...  ${sec}=30
    prepare image  ${image_path}  FAN_CPLD_REFRESH
    prepare image  ${image_path}  BASE_CPLD_REFRESH
    prepare image  ${image_path}  CPU_CPLD_REFRESH
    executePythonCommand
    ...  cmd=python
    ...  mode=${openbmc_mode}
    ...  timeout=${sec}
    executePythonCommand
    ...  cmd=from hal.hal_firmware import *
    ...  timeout=${sec}
    executePythonCommand
    ...  cmd=a=HalFirmware()
    ...  timeout=${sec}
    send cmd regexp
    ...  cmd=${refresh_cpld_cmd}
    ...  promptRegexp=login:
    ...  timeout=900
    open prompt  console=${openbmc_mode}  sec=300
    BuiltIn.Sleep  60

check fpga ctrl bit
    [Arguments]  ${console}=${openbmc_mode}
    execute command and verify with a pattern
    ...  console=${console}
    ...  command=cat /sys/bus/i2c/devices/0-000d/fpga_buf_ctrl
    ...  pattern=(?m)^${fpga_buf_ctrl_default_val}$
    ...  msg=Failed to verify default value (should be ${fpga_buf_ctrl_default_val})
    BuiltIn.Sleep  1

    execute command and verify exit code
    ...  console=${console}
    ...  command=echo 0x1 > /sys/bus/i2c/devices/0-000d/fpga_buf_ctrl
    BuiltIn.Sleep  1
    execute command and verify with a pattern
    ...  console=${console}
    ...  command=cat /sys/bus/i2c/devices/0-000d/fpga_buf_ctrl
    ...  pattern=(?m)^${fpga_buf_ctrl_test_val}$
    ...  msg=Failed to verify value (should be ${fpga_buf_ctrl_test_val})
    BuiltIn.Sleep  1

    Run Keyword If  'migaloo' in '${devicename}'
    ...  Run Keywords
    ...  execute command and verify exit code
         ...  console=${console}
         ...  command=i2cset -y -f 0 0x0d 0x7d 0x03
    ...  AND  BuiltIn.Sleep  1
    ...  AND  execute command and verify with a pattern
              ...  console=${console}
              ...  command=i2cget -y -f 0 0x0d 0x7d
              ...  pattern=(?m)^0x03$
              ...  msg=Failed to verify value (should be 0x03)
    ...  AND  BuiltIn.Sleep  1
    ...  AND  execute command and verify with a pattern
              ...  console=${console}
              ...  command=cat /sys/bus/i2c/devices/0-000d/fpga_buf_ctrl
              ...  pattern=(?m)^0x3$
              ...  msg=Failed to verify value (should be 0x3)
    ...  AND  BuiltIn.Sleep  1

    execute command and verify exit code
    ...  console=${console}
    ...  command=i2cset -y -f 0 0x0d 0x7d ${fpga_buf_ctrl_default_val}
    BuiltIn.Sleep  1
    execute command and verify with a pattern
    ...  console=${console}
    ...  command=i2cget -y -f 0 0x0d 0x7d
    ...  pattern=${fpga_hex_pattern}
    ${fpga_buf_ctrl_hex}=  Convert To Hex  ${match['hex_val']}  base=16
    ${fpga_buf_ctrl_default_hex}=   Convert To Hex  ${fpga_buf_ctrl_default_val}  base=16
    Should Be Equal  ${fpga_buf_ctrl_hex}  ${fpga_buf_ctrl_default_hex}
    BuiltIn.Sleep  1
    execute command and verify with a pattern
    ...  console=${console}
    ...  command=cat /sys/bus/i2c/devices/0-000d/fpga_buf_ctrl
    ...  pattern=(?m)^${fpga_buf_ctrl_default_val}$
    ...  msg=Failed to verify value (should be ${fpga_buf_ctrl_default_val})
    BuiltIn.Sleep  1


update fpga in sonic
    [Arguments]
    ...  ${isUpgrade}
    ...  ${fpga_image}
    ...  ${fpga_ver_patterns}
    ...  ${fpga_image_path}=${fpga_fw_save_to}
    prepare image  ${fpga_image_path}  FPGA  console=${diagos_mode}  upgrade=${isUpgrade}
    verify current boot flash  BMC  master
    program FPGA  where=${fpga_image_path}/${fpga_image}
    OpenBMC wedge power script
    BuiltIn.Sleep  60
    verify installed FPGA firmware  pattern=${fpga_ver_patterns}


program FPGA
    [Documentation]  Update the FPGA firmware
    [Arguments]
    ...  ${console}=${diagos_mode}
    ...  ${command}=fpga_prog
    ...  ${path}=${EMPTY}
    ...  ${where}=${fpga_fw_save_to}/${fpga_new_fw_name}
    ...  ${patterns}=${fpga_prog_patterns}

    execute command and verify with ordered pattern list
    ...  console=${console}
    ...  command=${command} ${where}
    ...  patterns=${patterns}
    ...  path=${path}
    ...  sec=60
    ...  msg=Failed to program FPGA firmware!


verify installed FPGA firmware
    [Documentation]  verify installed FPGA firmware
    [Arguments]
    ...  ${console}=${diagos_mode}
    ...  ${pattern}=${fpga_new_version_patterns}
    ...  ${path}=${diag_cpu_path}
    ...  ${command}=${fpga_version_cmd}

    show software version
    ...  console=${console}
    ...  command=${command}
    ...  path=${path}
    search for a pattern
    ...  text=${text}
    ...  pattern=${pattern}
    ...  msg=Not found the FPGA version pattern or wrong installed version!


test power control
    [Arguments]
    ...  ${power_option}
    verify power control  ${power_option}
    check power status of cpu  on  OK
    get dhcp ip address  DUT  eth0  ${openbmc_mode}
    ${cpu_ip} =  get dhcp ip address  DUT  eth0  ${diagos_mode}
    BuiltIn.Sleep  5
    exec ping  DUT  ${cpu_ip}  5  ${openbmc_mode}


check power status of cpu
    [Arguments]
    ...  ${expected_power}=on
    ...  ${expected_boot}=OK
    verify power status  ${expected_power}
    verify current boot flash  BIOS  master  ${expected_boot}


verify the VLAN was removed
    [Documentation]  verify the VLAN was removed
    [Arguments]
    ...  ${console}=${openbmc_mode}
    ...  ${command}=ifconfig -a
    ...  ${pattern}=(?m)^eth0\\.4088

    ${status}  ${value}=  Run Keyword And Ignore Error  execute command and verify with a pattern
    ...  console=${console}
    ...  command=${command}
    ...  path=${EMPTY}
    ...  pattern=${pattern}
    ...  msg=Should not found the fail pattern!
    ...  is_check_exit_code=${FALSE}
    Run Keyword If  '${status}' == 'PASS'
    ...  Fail  Failed, the VLAN did not remove.${\n*2}Found it on:${\n}${match}

prepare store eeprom
    [Arguments]
    ...  ${eeprom_path}

    Run Keyword And Ignore Error  change kernel log level  console=${openbmc_mode}  level=3
    change dir
    ...  path=${eeprom_path}
    ...  mode=${openbmc_mode}
    run eeprom tool
    ...  option=d
    execute command and set test variable
    ...  console=${openbmc_mode}
    ...  command=cp eeprom_out.cfg eeprom_store.cfg


prepare store all fan eeprom
    Run Keyword And Ignore Error  change kernel log level  console=${openbmc_mode}  level=3
    change dir
    ...  path=${fan_eeprom_path}
    ...  mode=${openbmc_mode}
    FOR    ${fan}    IN RANGE    ${1}  ${FAN_NUM}+1
        run eeprom tool
        ...  option=d
        ...  fan=${fan}
        execute command and set test variable
        ...  console=${openbmc_mode}
        ...  command=cp eeprom_out.cfg eeprom_store${fan}.cfg
    END


restore eeprom
    [Arguments]
    ...  ${eeprom_path}

    change dir
    ...  path=${eeprom_path}
    ...  mode=${openbmc_mode}
    execute command and set test variable
    ...  console=${openbmc_mode}
    ...  command=cp eeprom_store.cfg eeprom.cfg
    run eeprom tool
    ...  option=w
    run eeprom tool
    ...  option=u
    run eeprom tool
    ...  option=d
    execute command and set test variable
    ...  console=${openbmc_mode}
    ...  command=rm eeprom_store.cfg
    reboot openbmc


restore all fan eeprom
    change dir
    ...  path=${fan_eeprom_path}
    ...  mode=${openbmc_mode}
    FOR    ${fan}    IN RANGE    ${1}  ${FAN_NUM}+1
        execute command and set test variable
        ...  console=${openbmc_mode}
        ...  command=cp eeprom_store${fan}.cfg eeprom.cfg
        run eeprom tool
        ...  option=w
        ...  fan=${fan}
        run eeprom tool
        ...  option=u
        ...  fan=${fan}
        run eeprom tool
        ...  option=d
        ...  fan=${fan}
        execute command and set test variable
        ...  console=${openbmc_mode}
        ...  command=rm eeprom_store${fan}.cfg
    END
    change dir
    Run Keyword And Ignore Error  change kernel log level  console=${openbmc_mode}  level=7


check fru data match with fru-util command
    [Arguments]
    ...  ${fru_name}
    ...  ${fan}=${EMPTY}

    ${eeprom_result} =  run eeprom tool
    ...  option=d
    ...  fan=${fan}
    ${util_result} =  run util
    ...  cmd=fru-util ${fru_name} ${fan}
    compare util and eeprom
    ...  util_dict=${util_result}
    ...  eeprom_dict=${eeprom_result}


write and read eeprom
    [Arguments]
    ...  ${eeprom_test_name}
    ...  ${fru_type}
    ...  ${fru_name}
    ...  ${fan}=${EMPTY}

    modify eeprom cfg
    ...  eeprom_name=${eeprom_test_name}
    ...  fru_type=${fru_type}
    ...  eeprom_cfg_file=eeprom.cfg
    run eeprom tool
    ...  option=w
    ...  fan=${fan}
    run eeprom tool
    ...  option=u
    ...  fan=${fan}
    run eeprom tool
    ...  option=d
    ...  fan=${fan}
    ...  expected_result=${eeprom_test_name}
    check fru data match with fru-util command
    ...  fru_name=${fru_name}
    ...  fan=${fan}


reboot openbmc and read eeprom
    [Arguments]
    ...  ${eeprom_path}
    ...  ${eeprom_test_name}

    reboot openbmc
    Run Keyword And Ignore Error  change kernel log level  console=${openbmc_mode}  level=3
    change dir
    ...  path=${eeprom_path}
    ...  mode=${openbmc_mode}
    run eeprom tool
    ...  option=d
    ...  expected_result=${eeprom_test_name}


check fan fru data match with fru-util command
    FOR    ${fan}    IN RANGE    ${1}  ${FAN_NUM}+1
        check fru data match with fru-util command
        ...  fru_name=${fan_fru}
        ...  fan=${fan}
    END

write and read fan eeprom
    [Arguments]
    ...  ${eeprom_test_name}

    FOR    ${fan}    IN RANGE    ${1}  ${FAN_NUM}+1
        write and read eeprom
        ...  eeprom_test_name=${eeprom_test_name}
        ...  fru_type=${fan_fru_type}
        ...  fru_name=${fan_fru}
        ...  fan=${fan}
    END

reboot openbmc and read fan eeprom
    [Arguments]
    ...  ${eeprom_test_name}

    reboot openbmc
    Run Keyword And Ignore Error  change kernel log level  console=${openbmc_mode}  level=3
    change dir
    ...  path=${fan_eeprom_path}
    ...  mode=${openbmc_mode}
    FOR    ${fan}    IN RANGE    ${1}  ${FAN_NUM}+1
        run eeprom tool
        ...  option=d
        ...  fan=${fan}
        ...  expected_result=${eeprom_test_name}
    END


restore openbmc master
    open prompt  console=${openbmc_mode}  sec=300
    create dir  ${bmc_local_image_path}  ${openbmc_mode}
    check and flush eth0 interface  #### @WORKAROUND to recover openbmc network
    get dhcp ip address  DUT  eth0  ${openbmc_mode}
    BuiltIn.Sleep  10
    download image  DUT  BMC
    online update fw  BMC  slave  True
    power cycle to openbmc  timeout=600


restore openbmc slave
    open prompt  console=${openbmc_mode}  sec=300
    create dir  ${bmc_local_image_path}  ${openbmc_mode}
    check and flush eth0 interface  #### @WORKAROUND to recover openbmc network
    get dhcp ip address  DUT  eth0  ${openbmc_mode}
    BuiltIn.Sleep  10
    download image  DUT  BMC
    online update fw  BMC  slave  True
    switch bmc flash  slave
    check logs and verify bmc boot from  slave  ${bmc_boot_slave_pattern}
    switch bmc flash  master


check logs and verify bmc boot from
    [Arguments]
    ...  ${bmc_flash}
    ...  ${bmc_boot_log_pattern}
    wait and verify command
    ...  cmd=${boot_cpumon_cmd}
    ...  pattern=${bmc_boot_log_pattern}
    ...  mode=${openbmc_mode}
    wait and verify command
    ...  cmd=${boot_syslog_cmd}
    ...  pattern=${bmc_boot_log_pattern}
    ...  mode=${openbmc_mode}
    verify current boot flash
    ...  fw_type=BMC
    ...  boot_flash=${bmc_flash}


OpenBMC reboot
    [Documentation]  Reboot OpenBMC and login to OpenBMC once again
    [Arguments]
    ...  ${console}=${openbmc_mode}
    ...  ${reboot_time}=300

    open prompt  console=${console}  sec=${reboot_time}
    reboot UNIX-like OS  console=${console}
    open prompt and login to root user  console=${console}
    BuiltIn.Sleep  40


change MAC address file configuration
    [Documentation]  Do change the MAC address to the file configuration
    [Arguments]
    ...  ${console}=${openbmc_mode}
    ...  ${path}=${sys_eeprom_path}
    ...  ${file}=eeprom.cfg
    ...  ${mac}=AA:BB:CC:DD:EE:FF
    ...  ${sed_pattern}=s/product_custom_2.*$/product_custom_2=${mac}/g

    file edit and replace a line
    ...  console=${console}
    ...  path=${path}
    ...  file=${file}
    ...  sed_pattern=${sed_pattern}


verify eeprom tool dumpped mac information
    [Documentation]  verify eeprom tool dumpped mac information
    [Arguments]
    ...  ${console}=${openbmc_mode}
    ...  ${path}=${sys_eeprom_path}
    ...  ${command}=./eeprom_tool -d
    ...  ${pattern}=Product[ \\t]+Extra_\\d+[ \\t]+:[ \\t]*(?P<eepromtool_mac>(?:[a-fA-F0-9]{2}:?){6})
    ...  ${msg}=Not found the MAC address!

    execute command and verify with a pattern
    ...  console=${console}
    ...  path=${path}
    ...  command=${command}
    ...  pattern=${pattern}
    ...  msg=${msg}

    set test variable  &{eepromtool_mac}  &{match}


increases MAC address
    [Documentation]  Do calculate for MAC Address
    [Arguments]
    ...  ${mac}

    ${last_mac}=  Evaluate  hex(eval('0x${mac}[15:]+1')).upper()
    ${new_mac}=  Catenate  ${mac}[:-2]${last_mac}[2:]

    [Return]  ${new_mac}


compare MAC address for eeprom tool and ifconfig
    [Documentation]  Compare two MAC addresses
    [Arguments]
    ...  ${msg}=The eeprom_tool does not matched with ifconfig MAC address

    ${eepromtool_mac_plus}=  increases MAC address  mac=${eepromtool_mac}[eepromtool_mac]

    Should Be Equal  ${eepromtool_mac_plus}  ${ifconfig_mac}[ifconfig_mac]
    ...  msg=${msg}
    ...  ignore_case=${TRUE}


eeprom tool write, update, dump and verify MAC information
    [Documentation]  write, update, dump and verify MAC information to the eeprom
    [Arguments]
    ...  ${console}=${openbmc_mode}
    ...  ${path}=${sys_eeprom_path}
    ...  ${command}=(./eeprom_tool -w && ./eeprom_tool -u && ./eeprom_tool -d)
    ...  ${mac}=AA:BB:CC:DD:EE:FE
    ...  ${pattern}=Product[ \\t]+Extra_\\d+[ \\t]+:[ \\t]*(?P<written_eepromtool_mac>${mac})
    ...  ${msg}=The dummped MAC by eeprom_tool does not matched with configuration file!

    execute command and verify with a pattern
    ...  console=${openbmc_mode}
    ...  path=${sys_eeprom_path}
    ...  command=${command}
    ...  pattern=${pattern}
    ...  msg=${msg}

    set test variable  &{written_eepromtool_mac}  &{match}


send switch slave bios
    load openbmc utils
    execute command
    ...  cmd=come_reset slave
    ...  mode=${openbmc_mode}
    BuiltIn.Sleep  120


check logs and verify bios boot from
    [Arguments]
    ...  ${bios_boot_log_patterns}
    wait and verify command
    ...  cmd=${boot_cpumon_cmd}
    ...  pattern=${bios_boot_log_patterns}
    ...  mode=${openbmc_mode}
    wait and verify command
    ...  cmd=${boot_syslog_cmd}
    ...  pattern=${bios_boot_log_patterns}
    ...  mode=${openbmc_mode}


restore bios master
    open prompt  console=${openbmc_mode}  sec=300
    create dir  ${bios_local_image_path}  ${openbmc_mode}
    check and flush eth0 interface  #### @WORKAROUND to recover openbmc network
    get dhcp ip address  DUT  eth0  ${openbmc_mode}
    BuiltIn.Sleep  10
    download image  DUT  BIOS
    online update fw  BIOS  master  True
    switch bios flash  master


restore bios slave
    open prompt  console=${openbmc_mode}  sec=300
    create dir  ${bios_local_image_path}  ${openbmc_mode}
    check and flush eth0 interface  #### @WORKAROUND to recover openbmc network
    get dhcp ip address  DUT  eth0  ${openbmc_mode}
    BuiltIn.Sleep  10
    download image  DUT  BIOS
    online update fw  BIOS  slave  True
    switch bios flash  slave
    switch bios flash  master


check and restore bios
    [Arguments]
    ...  ${bios_flash}
    ${status}  ${value}=  Run Keyword And Ignore Error  switch bios flash  ${bios_flash}  180
    Run Keyword If  '${status}' == 'FAIL'
    ...  Run Keywords  switch to openbmc  AND  restore bios ${bios_flash}
    ...  ELSE
    ...  Log  ${bios_flash} bios can boot normally


prepare file on usb device
    create dir  ${bios_local_image_path}  ${diagos_mode}
    check and flush eth0 interface  ${diagos_mode}  #### @WORKAROUND to recover openbmc network
    get dhcp ip address  DUT  eth0  ${diagos_mode}
    BuiltIn.Sleep  10
    download image  DUT  BIOS  destinationDir=${bios_local_image_path}/${bios_image}
    download image  DUT  AFU_TOOL
    execute command and verify with a pattern
    ...  console=${diagos_mode}
    ...  command=fdisk -l
    ...  pattern=\\/dev\\/sdb1
    ...  msg=Not found USB disk
    create dir  /mnt  ${diagos_mode}
    execute command and verify exit code
    ...  console=${diagos_mode}
    ...  command=mount /dev/sdb1 /mnt
    execute command and verify exit code
    ...  console=${diagos_mode}
    ...  command=cp ${bios_local_image_path}/${afu_new_image} /mnt
    execute command and verify exit code
    ...  console=${diagos_mode}
    ...  command=cp ${bios_local_image_path}/${bios_image} /mnt
    execute command and verify exit code
    ...  console=${diagos_mode}
    ...  command=ls /mnt
    execute command and verify exit code
    ...  console=${diagos_mode}
    ...  command=umount /mnt


update bmc crash and check backup bmc can boot
    [Arguments]
    ...  ${bmc_flash}
    ...  ${backup_flash}
    ...  ${boot_patterns}

    prepare image  ${bmc_local_image_path}  BMC  bmc_flash=${bmc_flash}
    Run keywords
    ...  clear log  ${openbmc_mode}  ${syslog_path}  AND
    ...  clear log  ${openbmc_mode}  ${cpumon_log}
    update bmc crash
    ${reboot_log} =  reboot openbmc  timeout=900
    verify log with keywords  ${bmc_init_patterns}  ${reboot_log}
    check logs and verify bmc boot from  ${backup_flash}  ${boot_patterns}
    Run keywords
    ...  clear log  ${openbmc_mode}  ${syslog_path}  AND
    ...  clear log  ${openbmc_mode}  ${cpumon_log}
    power cycle to openbmc  timeout=900
    check logs and verify bmc boot from  ${backup_flash}  ${boot_patterns}


verify boot info
    [Documentation]  Display current boot flash memory
    [Arguments]
    ...  ${console}=${openbmc_mode}
    ...  ${pattern}=(?i)(?P<boot_info>Master|Slave)
    ...  ${is_check_exit_code}=${FALSE}

    execute command and verify with a pattern
    ...  console=${console}
    ...  command=boot_info.sh
    ...  pattern=${pattern}
    ...  is_check_exit_code=${is_check_exit_code}

    set test variable  &{boot_info}  &{match}


Setting up flash memory boot
    [Documentation]  Set the system to boot from the flash memory
    [Arguments]
    ...  ${console}=${openbmc_mode}
    ...  ${flash}=master
    ...  ${sec}=300

    ${status}  ${value}=  Run Keyword And Ignore Error  execute command and verify with a pattern
    ...  console=${console}
    ...  command=(source /usr/local/bin/openbmc-utils.sh && boot_from ${flash})
    ...  sec=30
    ...  pattern=(?i)(?P<boot_switch>no need to switch)
    ...  msg=If found, the system is not going to reboot.
    ...  is_check_exit_code=${FALSE}
    Run Keyword If  '${status}' == 'FAIL'
    ...  Run Keywords
    ...  read until pattern  pattern= login:  sec=${sec}  AND
    ...  open prompt  console=${console}  sec=10  AND
    ...  BuiltIn.sleep  30


ifconfig to save original mac address
    [Documentation]  Save original MAC address
    [Arguments]
    ...  ${console}=${openbmc_mode}
    ...  ${interface}=eth0

    verify network interface MAC address  console=${console}  interface=${interface}
    set test variable  &{mac_original}  &{match}


set sonic system idle time
    [Arguments]
    ...  ${timeout}=7200
    execute command and verify exit code
    ...  console=${diagos_mode}
    ...  command=grep -q "TMOUT=${timeout}" /etc/profile || echo "TMOUT=${timeout}" >> /etc/profile
    execute command and verify exit code
    ...  console=${diagos_mode}
    ...  command=grep -q "export TMOUT" /etc/profile || echo "export TMOUT" >> /etc/profile
    execute command and verify exit code
    ...  console=${diagos_mode}
    ...  command=cat /etc/profile | grep TMOUT
    execute command and verify exit code
    ...  console=${diagos_mode}
    ...  command=source /etc/profile


clear log
    [Arguments]
    ...  ${console}
    ...  ${log}
    execute command and verify exit code
    ...  console=${console}
    ...  command=echo > ${log}


reboot openbmc and check error log
    ${reboot_log} =  reboot openbmc  timeout=600
    verify log with keywords  ${reboot_error_patterns}  ${reboot_log}  True


clear monitor log
    [Arguments]
    ...  ${console}=${openbmc_mode}
    clear log  ${console}  ${fand_log}
    clear log  ${console}  ${dcdcmon_log}
    clear log  ${console}  ${cpumon_log}
    clear log  ${console}  ${powermon_log}


check monitor status
    [Documentation]  verify monitor status
    [Arguments]
    ...  ${console}=${openbmc_mode}
    ...  ${pattern}=active \\(running\\)
    ...  ${option}=--no-pager

    execute command and verify with a pattern
    ...  console=${console}
    ...  command=systemctl status fanctrl ${option}
    ...  pattern=${pattern}
    ...  msg=Failed to verify status fanctrl!
    execute command and verify with a pattern
    ...  console=${console}
    ...  command=systemctl status dcdcmon ${option}
    ...  pattern=${pattern}
    ...  msg=Failed to verify status dcdcmon!
    execute command and verify with a pattern
    ...  console=${console}
    ...  command=systemctl status cpumon ${option}
    ...  pattern=${pattern}
    ...  msg=Failed to verify status cpumon!
    execute command and verify with a pattern
    ...  console=${console}
    ...  command=systemctl status powermon ${option}
    ...  pattern=${pattern}
    ...  msg=Failed to verify status powermon!

check monitor log
    [Arguments]
    ...  ${console}=${openbmc_mode}
    ...  ${error_pattern}=${monlog_error_patterns}
    ...  ${check_fail}=True
    ...  ${msg}=SEL was not recorded!
    ...  ${sec}=300
    execute command and set test variable
    ...  console=${console}
    ...  command=cat ${fand_log}
    ...  sec=${sec}
    verify log with keywords
    ...  regex_list=${error_pattern}
    ...  target_log=${text}
    ...  check_fail=True
    search for a pattern
    ...  pattern=(FAND) - (\\w+): .+
    ...  text=${text}
    ...  msg=${msg}

    execute command and set test variable
    ...  console=${console}
    ...  command=cat ${dcdcmon_log}
    ...  sec=${sec}
    verify log with keywords
    ...  regex_list=${error_pattern}
    ...  target_log=${text}
    ...  check_fail=True
    search for a pattern
    ...  pattern=(DCDCMON) - (\\w+): .+
    ...  text=${text}
    ...  msg=${msg}

    execute command and set test variable
    ...  console=${console}
    ...  command=cat ${cpumon_log}
    ...  sec=${sec}
    verify log with keywords
    ...  regex_list=${error_pattern}
    ...  target_log=${text}
    ...  check_fail=True
    search for a pattern
    ...  pattern=(CPUMON) - (\\w+): .+
    ...  text=${text}
    ...  msg=${msg}

    execute command and set test variable
    ...  console=${console}
    ...  command=cat ${powermon_log}
    ...  sec=${sec}
    verify log with keywords
    ...  regex_list=${error_pattern}
    ...  target_log=${text}
    ...  check_fail=True
    search for a pattern
    ...  pattern=(POWERMON) - (\\w+): .+
    ...  text=${text}
    ...  msg=${msg}

switch bmc and check boot source and log
    [Arguments]
    ...  ${bmc_flash}
    ...  ${bmc_boot_log_pattern}
    Run keywords
    ...  clear log  ${openbmc_mode}  ${syslog_path}  AND
    ...  clear log  ${openbmc_mode}  ${cpumon_log}
    Setting up flash memory boot  flash=${bmc_flash}
    Run Keyword And Ignore Error
    ...  change kernel log level  console=${openbmc_mode}  level=3
    verify current boot flash  BMC  ${bmc_flash}
    execute command and verify exit code  console=${openbmc_mode}  command=cat /etc/issue
    wait and verify command
    ...  cmd=${boot_cpumon_cmd}
    ...  pattern=${bmc_boot_log_pattern}
    ...  mode=${openbmc_mode}
    wait and verify command
    ...  cmd=${boot_syslog_cmd}
    ...  pattern=${bmc_boot_log_pattern}
    ...  mode=${openbmc_mode}

switch bios and check boot source and log
    [Arguments]
    ...  ${bios_flash}
    ...  ${bios_boot_log_pattern}
    Run keywords
    ...  clear log  ${openbmc_mode}  ${syslog_path}  AND
    ...  clear log  ${openbmc_mode}  ${cpumon_log}
    switch bios flash  ${bios_flash}
    verify fw version  BIOS  ${bios_version_dict}
    verify current boot flash  BIOS  ${bios_flash}
    wait and verify command
    ...  cmd=${boot_cpumon_cmd}
    ...  pattern=${bios_boot_log_pattern}
    ...  mode=${openbmc_mode}
    wait and verify command
    ...  cmd=${boot_syslog_cmd}
    ...  pattern=${bios_boot_log_pattern}
    ...  mode=${openbmc_mode}


set and get fan speed
    [Arguments]  ${fan_speed}
    execute command and verify exit code
    ...  console=${openbmc_mode}
    ...  command=set_fan_speed.sh ${fan_speed}
    BuiltIn.Sleep  10
    get fan speed  ${fan_speed}


reset bmc via devmem
    execute command and verify exit code
    ...  console=${openbmc_mode}
    ...  command=devmem 0x1e785004 32 0x00989680
    execute command and verify exit code
    ...  console=${openbmc_mode}
    ...  command=devmem 0x1e785008 32 0x4755
    send a line
    ...  command=devmem 0x1e78500c 32 0x00000033
    read until pattern  pattern= login:  sec=300
    open prompt  ${openbmc_mode}  sec=10
    BuiltIn.Sleep  40

verify watchdog info
    [Arguments]
    ...  ${patterns}
    execute command and verify with ordered pattern list
    ...  console=${openbmc_mode}
    ...  command=boot_info.sh
    ...  patterns=${patterns}
    ...  msg=Failed to verify watchdog info!

sol switch to sonic
    FOR  ${key}  IN  @{keys_sol_to_sonic}
        send msg  msg=${key}
        BuiltIn.Sleep  0.5
    END
    BuiltIn.Sleep  3
    open prompt  console=${diagos_mode}  sec=10

sol switch to openbmc
    FOR  ${key}  IN  @{keys_sol_to_openbmc}
        send msg  msg=${key}
        BuiltIn.Sleep  0.5
    END
    open prompt  console=${openbmc_mode}  sec=10

restful set nextboot
    [Arguments]
    ...  ${nextboot_url}
    ...  ${nextboot}
    ...  ${bmc_url}=${api_bmc_url}
    execute command and verify with unordered pattern list
    ...  console=${diagos_mode}
    ...  command=curl -d '{"Flash":"${nextboot}"}' ${bmc_url}/${nextboot_url} | python -m json.tool
    ...  patterns=${status_ok_patterns}
    ...  msg=Failed to set restful nextboot!
    ...  sec=300

restful get nextboot and info
    [Arguments]
    ...  ${nextboot_url}
    ...  ${info_url}
    ...  ${nextboot_patterns}
    ...  ${info_patterns}
    ...  ${bmc_url}=${api_bmc_url}
    execute command and verify with unordered pattern list
    ...  console=${diagos_mode}
    ...  command=curl -g ${bmc_url}/${nextboot_url} | python -m json.tool
    ...  patterns=${nextboot_patterns}
    ...  msg=Failed to get restful nextboot!
    ...  sec=300
    execute command and verify with unordered pattern list
    ...  console=${diagos_mode}
    ...  command=curl -g ${bmc_url}/${info_url} | python -m json.tool
    ...  patterns=${info_patterns}
    ...  msg=Failed to get restful info!
    ...  sec=300

restful reboot bmc
    [Arguments]
    ...  ${current_boot}
    ...  ${bmc_url}=${api_bmc_url}
    execute command and verify with unordered pattern list
    ...  console=${diagos_mode}
    ...  command=curl -d '{}' ${bmc_url}/bmc/reboot | python -m json.tool
    ...  patterns=${status_ok_patterns}
    ...  msg=Failed to reboot bmc!
    ...  sec=300
    BuiltIn.Sleep  10
    sonic switch to openbmc console
    BuiltIn.Sleep  40
    verify current boot flash  BMC  ${current_boot}

restful reboot cpu
    [Arguments]
    ...  ${current_boot_pattern}
    ...  ${bmc_url}=${api_bmc_url}
    execute command and verify with unordered pattern list
    ...  console=${diagos_mode}
    ...  command=curl -d '{"Entity":"cpu"}' ${bmc_url}/hw/powercycle | python -m json.tool
    ...  patterns=${status_ok_patterns}
    ...  msg=Failed to reboot cpu!
    ...  sec=300
    ...  is_check_exit_code=${FALSE}
    read until pattern  pattern=${current_boot_pattern}  sec=300
    open prompt  console=${diagos_mode}  sec=300
    BuiltIn.Sleep  30

wait bmc restful
    [Arguments]
    ...  ${delay}=30
    ${status}  ${value}=  Run Keyword And Ignore Error  wait and verify command
    ...  cmd=curl -g ${api_bmc_url}/${api_bmc_info}
    ...  pattern="status": "OK"
    ...  mode=${diagos_mode}
    ...  delay=${delay}
    ...  timeout=30
    ### @WORKAROUND bmc restful cannot work, try power cycle to recover it.
    Run Keyword If  '${status}' == 'FAIL'
    ...  Run Keywords
    ...  power cycle to openbmc
    ...  AND  Log  network is broken down, need recover it !  level=ERROR
    ...  AND  Fail  failed to wait bmc restful

run power command
    [Arguments]
    ...  ${cmd}
    ...  ${boot_time}=300
    open prompt  ${diagos_mode}  sec=10
    send a line
    ...  command=power cycle ${cmd}
    read until pattern  pattern=[y/n]:  sec=30
    send a line
    ...  command=y
    read until pattern  pattern=Power cycling  sec=30
    BuiltIn.Sleep  10
    read until pattern  pattern= login:  sec=${boot_time}
    open prompt  ${openbmc_mode}  sec=${boot_time}
    open prompt  ${diagos_mode}  sec=10
    BuiltIn.Sleep  30

check ntp server
    FOR    ${config}    IN    @{ntp_config_list}
        execute command and verify exit code
        ...  console=${diagos_mode}
        ...  command=grep -q "${config}" ${ntp_conf_file} || echo "${config}" >> ${ntp_conf_file}
        BuiltIn.Sleep  0.5
    END
    execute command and verify exit code
    ...  console=${diagos_mode}
    ...  command=cat ${ntp_conf_file}
    execute command and verify exit code
    ...  console=${diagos_mode}
    ...  command=service ntp restart
    BuiltIn.Sleep  300
    wait and verify command
    ...  cmd=ntpstat
    ...  pattern=synchronised to
    ...  mode=${diagos_mode}

check and switch bios boot
    [Arguments]
    ...  ${bios_flash}=Master
    ...  ${console}=${openbmc_mode}
    load openbmc utils
    ${status}  ${value}=  Run Keyword And Ignore Error  execute command and verify with a pattern
    ...  console=${console}
    ...  command=come_boot_info
    ...  sec=30
    ...  pattern=(?i)(?P<boot_switch>${bios_flash})
    ...  msg=If found, no need to switch bios.
    ...  is_check_exit_code=${FALSE}
    Run Keyword If  '${status}' == 'FAIL'
    ...  switch bios flash  ${bios_flash}

check all cd ports link up status
    change dir
    ...  path=${sdk_path}
    ...  mode=${diagos_mode}
    execute command
    ...  cmd=pkill ${BCM_USER}
    ...  mode=${diagos_mode}
    load sdk mode
    check all port up status
    [Teardown]  exit sdk mode

load HalMisc
    [Arguments]
    ...  ${sec}=30
    executePythonCommand
    ...  cmd=python
    ...  mode=${openbmc_mode}
    ...  timeout=${sec}
    executePythonCommand
    ...  cmd=from hal.hal_firmware import *
    ...  timeout=${sec}
    executePythonCommand
    ...  cmd=a=HalMisc()
    ...  timeout=${sec}
    BuiltIn.Sleep  1

execute HalMisc command
    [Arguments]
    ...  ${command}
    ...  ${pattern}
    ...  ${msg}=${EMPTY}
    ...  ${sec}=30
    ${text}=  executePythonCommand
    ...  cmd=${command}
    ...  timeout=${sec}
    search for a pattern  ${text}  ${pattern}  ${msg}

get switch chip
    [Arguments]
    ...  ${pattern}
    execute HalMisc command
    ...  command=a.get_switch_port_power_status()
    ...  pattern=${pattern}
    BuiltIn.Sleep  1
    execute HalMisc command
    ...  command=a.get_switch_chip_power_status()
    ...  pattern=${pattern}

set switch chip
    [Arguments]
    ...  ${status}
    ...  ${pattern}
    execute HalMisc command
    ...  command=a.set_switch_port_power_status("${status}")
    ...  pattern=${pattern}
    BuiltIn.Sleep  1
    execute HalMisc command
    ...  command=a.set_switch_chip_power_status("${status}")
    ...  pattern=${pattern}

check switch chip sensors
    [Arguments]
    ...  ${command}=${switch_chip_sensors_cmd}
    ...  ${min}=None
    ...  ${max}=None
    ...  ${useThreshold}=${FALSE}
    execute command and set test variable
    ...  console=${openbmc_mode}
    ...  command=${command}
    verify sensor value  ${text}  ${min}  ${max}  ${useThreshold}

check error messages on sonic idle state
    [Arguments]
    ...  ${patterns}
    ...  ${sec}=60
    open prompt  ${openbmc_mode}  10
    open prompt  ${diagos_mode}  10
    ${text}=  read until regexp  patterns=${patterns}  timeout=${sec}

store sensors config
    execute command and verify exit code
    ...  path=${switch_chip_dev_path}
    ...  console=${openbmc_mode}
    ...  command=cp ${sensors_conf_file} sensors_config_store.json
    change dir
    ...  mode=${openbmc_mode}

restore sensors config
    execute command and verify exit code
    ...  path=${switch_chip_dev_path}
    ...  console=${openbmc_mode}
    ...  command=cp sensors_config_store.json ${sensors_conf_file}
    execute command and verify exit code
    ...  console=${openbmc_mode}
    ...  command=cat ${switch_chip_dev_path}/${sensors_conf_file} | grep -i "power_"
    change dir
    ...  mode=${openbmc_mode}

modify sensors config
    FOR    ${config}    IN    @{power_ctrl_config_list}
        file edit and replace a line
        ...  path=${switch_chip_dev_path}
        ...  console=${openbmc_mode}
        ...  file=${sensors_conf_file}
        ...  sed_pattern=s|${config}|${config}11|g
        BuiltIn.Sleep  0.5
    END
    execute command and verify exit code
    ...  console=${openbmc_mode}
    ...  command=cat ${switch_chip_dev_path}/${sensors_conf_file} | grep -i "power_"

set and get sys led
    [Arguments]
    ...  ${color_option}
    ...  ${color_pattern}
    ...  ${console}=${openbmc_mode}
    execute command and verify exit code
    ...  console=${console}
    ...  command=sys_led ${color_option}
    BuiltIn.Sleep  2
    execute command and verify with a pattern
    ...  console=${console}
    ...  command=sys_led
    ...  pattern=${color_pattern}
    ...  msg=Failed to verify sys led!

get sys led
    [Arguments]
    ...  ${color_pattern}
    ...  ${console}=${openbmc_mode}
    load openbmc utils
    execute command and verify with a pattern
    ...  console=${console}
    ...  command=sys_led
    ...  pattern=${color_pattern}
    ...  msg=Failed to verify sys led!


check and swap bmc boot
    BuiltIn.Sleep  20
    Run Keyword If  '${boot_info['boot_info']}' == 'Master'
    ...  Run Keywords  switch bmc flash  Slave  AND  set test variable  ${bmcSta}  Slave
    ...  ELSE IF  '${boot_info['boot_info']}' == 'Slave'
    ...  Run Keywords  switch bmc flash  Master  AND  set test variable  ${bmcSta}  Master
    ...  ELSE
    ...  Fail  Failed, Error OpenBMC boot info


power off on a single psu
    [Arguments]
    ...  ${psu}
    ...  ${psu_sensor_err_patterns}
    ...  ${console}=${openbmc_mode}
    execute command and verify with a pattern
    ...  console=${console}
    ...  command=psu_off_on.sh -p ${psu}
    ...  pattern=Set PSU${psu} auto turn on
    ...  msg=Failed to power off-on psu!
    execute command and verify with ordered pattern list
    ...  console=${console}
    ...  command=${psu_all_sensors_cmd}
    ...  patterns=${psu_sensor_err_patterns}
    ...  msg=Failed to verify psu sensors, it should not be read!
    BuiltIn.Sleep  10
    execute command and verify with ordered pattern list
    ...  console=${console}
    ...  command=${psu_all_sensors_cmd}
    ...  patterns=${psu_all_sensors_normal_patterns}
    ...  msg=Failed to verify psu sensors, it should be read normally!
    execute command and verify with ordered pattern list
    ...  console=${console}
    ...  command=${psu_all_fru_cmd}
    ...  patterns=${psu_all_fru_normal_patterns}
    ...  msg=Failed to verify ${psu_all_fru_cmd}!


kill script
    [Arguments]
    ...  ${script_name}
    ...  ${console}=${openbmc_mode}
    execute command and verify with a pattern
    ...  console=${console}
    ...  command=ps | grep ${script_name}
    ...  pattern=(?mi)(?P<ps_id>\\d+).*${script_name}.sh
    execute command and verify exit code
    ...  console=${console}
    ...  command=kill -9 ${match['ps_id']}


keep reading sensors
    [Arguments]
    ...  ${sensor_name}=${EMPTY}
    ...  ${timeout}=${180}
    ...  ${console}=${openbmc_mode}

    ${date_start}=  Get Time
    FOR  ${loop}  IN RANGE  1  100  1
        execute command and set test variable
        ...  console=${console}
        ...  command=sensors ${sensor_name}
        verify sensor value  ${text}  min=None  max=None  useThreshold=${TRUE}

        BuiltIn.Sleep  5

        ${date_stop}=  Get Time
        ${total_test_time}=  Subtract Date From Date
        ...  ${date_stop}  ${date_start}
        ...  result_format=timer
        ...  exclude_millis=${TRUE}
        ${total_test_time_sec}=  Convert Time
        ...  ${total_test_time}
        ...  result_format=number

        ${status}=  Evaluate  ${total_test_time_sec} >= ${timeout}
        Exit For Loop If  '${status}' == '${TRUE}'
    END


power off and on cpu in bmc os
    verify power control  off
    BuiltIn.Sleep  10
    verify power control  on
    BuiltIn.Sleep  60
