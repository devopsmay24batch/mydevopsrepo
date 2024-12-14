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


*** Keywords ***
Detect hardware loopback module
    [Tags]  flatten-keyword
    [Arguments]
    ...  ${console}=${openbmc_mode}
    ...  ${path}=${openbmc_diag_bin_path}
    ...  ${command}=./cel-i2c-test -a
    ...  ${pattern}=(?mi)^[ \\t]*All the I2C devices test.*(?P<result>PASS)
    ...  ${exit_code_pattern}=(?m)^(?P<exit_code>0)$
    ...  ${exit_code_msg}=An exit code is not return zero/success!${\n}The command is fail!
    ...  ${msg}=This machine has no loopback module capability
    ...  ${sec}=${3 * 60}

    ${result}  ${text}=  Run Keyword And Ignore Error
    ...  execute command
    ...  cmd=(cd ${path} && ${command})
    ...  mode=${console}
    ...  timeout=${sec}

    ${exit_code_result}  ${exit_code_text}=  Run Keyword And Ignore Error
    ...  execute command
    ...  cmd=echo $?
    ...  mode=${console}
    ...  timeout=${sec}

    Run Keyword And Ignore Error
    ...  should match a regexp  text=${exit_code_text}  pattern=${exit_code_pattern}  msg=${exit_code_msg}

    ${loopback module?}  ${value}=  Run Keyword And Ignore Error
    ...  should match a regexp  text=${text}  pattern=${pattern}  msg=${msg}
    Set Suite Variable  ${loopback module?}


OpenBMC switch to SONiC console
    [Tags]  flatten-keyword
    [Documentation]  OpenBMC switch to SONiC console
    [Arguments]
    ...  ${sec}=300

    open prompt   console=${openbmc_mode}  sec=${sec}

    FOR  ${key}  IN  @{keys_switch_to_sonic}
        send msg  msg=${key}
        BuiltIn.Sleep  0.5
    END


OpenBMC switch from SONiC console back to OpenBMC console
    [Tags]  flatten-keyword
    [Documentation]  OpenBMC switch from SONiC console back to OpenBMC console
    [Arguments]
    ...  ${sec}=300

    open prompt   console=${openbmc_mode}  sec=${sec}

    FOR  ${key}  IN  @{keys_switch_to_openbmc}
        send msg  msg=${key}
        BuiltIn.Sleep  0.5
    END

sonic switch to openbmc console
    [Tags]  flatten-keyword
    [Documentation]  SONiC switch to OpenBMC console
    [Arguments]
    ...  ${sec}=300

    open prompt   console=${openbmc_mode}  sec=${sec}


open prompt and login to root user
    [Tags]  flatten-keyword
    [Documentation]  Open prompt and login to root user
    [Arguments]
    ...  ${console}=${diagos_mode}
    ...  ${sec}=300

    open prompt
    ...  console=${console}
    ...  sec=${sec}

    send a line
    ...  command=sudo -s


OpenBMC wedge power script
    [Tags]  flatten-keyword
    [Documentation]  Ask OpenBMC to power cycle/reset the SONiC OS
    [Arguments]
    ...  ${action}=cycle
    ...  ${sec}=240

    OpenBMC switch from SONiC console back to OpenBMC console
    execute command and verify exit code
    ...  console=${openbmc_mode}
    ...  command=wedge_power.sh ${action}
    ...  msg=OpenBMC is unsuccessfully to power ${action} the SONiC OS!
    OpenBMC switch to SONiC console
    read until pattern  pattern=\ login:  sec=${sec}


show software version
    [Tags]  flatten-keyword
    [Documentation]  show current software version
    [Arguments]
    ...  ${console}=${diagos_mode}
    ...  ${command}=${diagos_show_diag_version_command}
    ...  ${path}=${diagos_cpu_diag_path}
    ...  ${sec}=${60}

    # For SDK version check
    # Run Keyword And Ignore Error  execute command and verify exit code
    # ...  console=${console}
    # ..  command=pkill bcm.user

    execute command and verify exit code
    ...  console=${console}
    ...  path=${path}
    ...  command=${command}
    ...  msg=Failed to show software version!
    ...  sec=${sec}


verify software version
    [Tags]  flatten-keyword
    [Documentation]  verify software version
    [Arguments]
    ...  ${console}=${diagos_mode}
    ...  ${command}=${diagos_show_diag_version_command}
    ...  ${path}=${diagos_cpu_diag_path}
    ...  ${patterns}=${diagos_version_show_patterns}
    ...  ${msg}=Failed not found some of version pattern(s)!

    show software version
    ...  console=${console}
    ...  command=${command}
    ...  path=${path}
    search for ordered pattern list  text=${text}  patterns=${patterns}  msg=${msg}


install diagtool debian package
    [Tags]  flatten-keyword
    [Documentation]  install diagtool debian package
    [Arguments]
    ...  ${console}=${diagos_mode}
    ...  ${package}=${diag_deb_new_package}
    ...  ${path}=${diag_deb_save_to}

    execute command and verify exit code
    ...  console=${console}
    ...  command=dpkg -i ${package}
    ...  path=${path}
    ...  sec=300
    ...  msg=Failed to install the new deb diagtool package!


verify installed DIAG package
    [Tags]  flatten-keyword
    [Documentation]  verify installed DIAG package
    [Arguments]
    ...  ${patterns}=${diagos_version_show_patterns}
    ...  ${console}=${diagos_mode}
    ...  ${version}=${diag_new_version}
    ...  ${command}=${diagos_show_diag_version_command}
    ...  ${path}=${diagos_cpu_diag_path}

    verify software version
    ...  console=${console}
    ...  command=${command}
    ...  path=${path}
    ...  patterns=${patterns}
    Should Be Equal As Strings
    ...  first=${matches}[diag]
    ...  second=${version}
    ...  msg=The installed DIAG package is not up-to-date!


find current boot source
    [Tags]  flatten-keyword
    [Arguments]
    ...  ${console}=${openbmc_mode}
    ...  ${command}=(source /usr/local/bin/openbmc-utils.sh && boot_info.sh)
    ...  ${pattern}=Current Boot Code Source:[ \\t]+(?P<current_boot>.*)
    ...  ${msg}=Failed, can not find the current boot source!

    execute command and verify with a pattern
    ...  console=${console}
    ...  command=${command}
    ...  pattern=${pattern}
    ...  msg=Failed to get the current boot source!
    set test variable  ${current_boot}  ${match}


find BIOS boot source
    [Tags]  flatten-keyword
    [Arguments]
    ...  ${console}=${openbmc_mode}
    ...  ${command}=(source /usr/local/bin/openbmc-utils.sh && come_boot_info)
    ...  ${pattern}=(?i)COMe CPU boots from BIOS (?P<bios_boot_source>.*)
    ...  ${msg}=Failed to get the BIOS current boot source!

    execute command and verify with a pattern
    ...  console=${console}
    ...  command=${command}
    ...  pattern=${pattern}
    ...  msg=${msg}
    set test variable  ${bios_current_boot}  ${match}


ISPVM/CPLD download and update
    [Arguments]
    ...  ${file}
    ...  ${save_to}
    ...  ${ispvm_number}
    ...  ${source_path}=${switch_cpld_path}
    ...  ${download_time}=${10 * 60}

    # DiagOS renew IP using DHCP and set variable
    secure copy file
    ...  console=${diagos_mode}
    ...  username=${scp_username}
    ...  password=${scp_password}
    ...  source_ip=${ssh_server_ipv4}
    ...  source_path=${source_path}
    ...  source_file=${file}
    ...  destination=${save_to}
    ...  sec=${6 * 60}
    ...  always_copy=${TRUE}
    execute command and verify with a pattern
    ...  path=${save_to}
    ...  command=ispvm ${ispvm_number} ${save_to}/${file}
    ...  console=${diagos_mode}
    ...  sec=${3 * 60}
    ...  pattern=PASS
    ...  msg=Failed not found the pass pattern!


Read CPLD register
    [Tags]  flatten-keyword
    [Arguments]
    ...  ${command}
    ...  ${console}=${diagos_mode}
    ...  ${path}=${diagos_cpu_diag_path}
    ...  ${pattern}=data: (?P<data>0x[a-fA-F0-9]+)
    ...  ${msg}=Failed to read or verify it!

    execute command and verify with a pattern
    ...  console=${console}
    ...  path=${path}
    ...  command=${command}
    ...  pattern=${pattern}
    ...  msg=${msg}
    set test variable  &{cpld_read}  &{match}


Execute command on SDK Prompt (sdklt.0>)
    [Tags]  flatten-keyword
    [Arguments]
    ...  ${command}
    ...  ${pattern}
    ...  ${console}=${diagos_mode}
    ...  ${path}=${diagos_sdk_path}
    ...  ${msg}=${EMPTY}

    open prompt and login to root user  console=${console}
    execute command and verify exit code
    ...  path=${path}
    ...  console=${console}
    ...  command=pkill bcm.user
    ...  exit_code_pattern=(?m)^(?P<exit_code>\\d+)$

    # Enter to BCM.0>
    send a line  command=./auto_load_user.sh
    # Start of BMC.0> prompt
    read until pattern  pattern=BCM.0>

    # Start of sdklt.0> prompt
    send a line  command=dsh
    read until pattern  pattern=sdklt.0>

    # Exectue command on sdklt.0> prompt
    send a line  command=${command}
    read until pattern  pattern=sdklt.0>
    read until pattern  pattern=sdklt.0>

    search for a pattern  text=${text}  pattern=${pattern}  msg=${msg}

    send a line  command=exit
    read until pattern  pattern=BCM.0>
    # End of sdklt.0>

    send a line  command=quit
    read until pattern  pattern=root@
    # End of BMC.0> prompt


Execute command on BCM Prompt (BCM.0>)
    [Tags]  flatten-keyword
    [Arguments]
    ...  ${command}
    ...  ${pattern}
    ...  ${console}=${diagos_mode}
    ...  ${path}=${diagos_sdk_path}
    ...  ${msg}=${EMPTY}
    ...  ${is_no_kill}=${FALSE}
    ...  ${is_no_reload}=${FALSE}
    ...  ${is_no_exit}=${FALSE}
    ...  ${is_no_login_to_root_user}=${FALSE}

    Run Keyword If  '${is_no_login_to_root_user}' == '${FALSE}'  open prompt and login to root user  console=${console}

    Run Keyword If  '${is_no_kill}' == '${FALSE}'  execute command and verify exit code
    ...  path=${path}
    ...  console=${console}
    ...  command=pkill bcm.user
    ...  exit_code_pattern=(?m)^(?P<exit_code>\\d+)$

    # Enter to BCM.0>
    Run Keyword If  '${is_no_reload}' == '${FALSE}'
    ...  Run Keywords
    ...  send a line  command=./auto_load_user.sh
    # Start of BMC.0> prompt
    ...  AND  read until pattern  pattern=BCM.0>

    # Exectue command on BCM.0> prompt
    send a line  command=${command}
    read until pattern  pattern=BCM.0>
    read until pattern  pattern=BCM.0>

    search for a pattern  text=${text}  pattern=${pattern}  msg=${msg}

    Run Keyword If  '${is_no_exit}' == '${FALSE}'
    ...  Run Keywords
    ...  send a line  command=quit
    ...  AND  read until pattern  pattern=root@
    # End of BMC.0> prompt


Update BMC on BMC OS
    [Arguments]
    ...  ${where_to_download}=${bmc_path}
    ...  ${image_name}=${bmc_old_image}
    ...  ${save_to}=${bmc_save_to}
    ...  ${image_version}=0.0.0
    ...  ${where_to_write}=/dev/mtdN

    OpenBMC renew IP using DHCP and set variable
    secure copy file
    ...  console=${openbmc_mode}
    ...  username=${scp_username}
    ...  password=${scp_password}
    ...  source_ip=${ssh_server_ipv4}
    ...  source_path=${where_to_download}
    ...  source_file=${image_name}
    ...  destination=${save_to}
    ...  sec=${6 * 60}
    ...  always_copy=${TRUE}
    execute command and verify exit code
    ...  console=${openbmc_mode}
    ...  command=flashcp -v "${save_to}/${image_name}" ${where_to_write}
    ...  msg=Failed to write OpenBMC image!
    ...  sec=${20 * 60}


Wait for OpenBMC Info
    [Arguments]  ${max_wait_number}=1000

    FOR  ${try}  IN RANGE  1  ${max_wait_number}+1  1
        ${status}  ${value}=  Run Keyword And Ignore Error  execute command and verify exit code
        ...  console=${diagos_mode}
        ...  command=(curl -g http://240.1.1.1:8080/api/bmc/info | python -m json.tool)
        ...  msg=Failed to get the OpenBMC Info!
        Exit For Loop If  '${status}' == 'PASS'
    END
    Run Keyword If  '${status}' == 'FAIL'
    ...  Fail  Failed to get OpenBMC Info!
