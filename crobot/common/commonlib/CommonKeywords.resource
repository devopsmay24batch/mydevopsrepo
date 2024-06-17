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
Library     Collections
Library     DateTime
Library     CommonLib.py        # Pass-through APIs for cross sub-system
Library     CommonKeywords.py   # Common and usable for cross sub-system


*** Variables ***
@{uboot_dhcp_patterns}          (?m)^DHCP client bound to address (?P<new_ip>[\\w\\.]+)


*** Keywords ***
# utility keyword
open prompt
    [Tags]  flatten-keyword
    [Documentation]  Open ${console} prompt and wait for ${sec}
    ...  to execute next command
    [Arguments]
    ...  ${console}
    ...  ${sec}

    ${text}=  prompt
    ...  mode=${console}
    ...  timeout=${sec}

    set test variable  ${text}
    set test variable  ${console}


send a line
    [Tags]  flatten-keyword
    [Documentation]  Send a line with no interaction or wait for it
    [Arguments]
    ...  ${command}
    ...  ${CR}=${TRUE}

    sendline
    ...  cmd=${command}
    ...  CR=${CR}


read until pattern
    [Tags]  flatten-keyword
    [Documentation]  Read the output until expected regular expressions pattern match
    [Arguments]
    ...  ${pattern}
    ...  ${sec}=180

    ${text}=  receive
    ...  rcv_str=${pattern}
    ...  timeout=${sec}

    set test variable  ${text}


verify exit code
    [Tags]  flatten-keyword
    [Documentation]  Fails if exit code is not match pattern
    [Arguments]
    ...  ${sec}=60
    ...  ${pattern}=(?m)^(?P<exit_code>0)$
    ...  ${msg}=An exit code is not return zero/success!

    ${text}=  execute command
    ...  cmd=echo $?
    ...  mode=${console}
    ...  timeout=${sec}
    search for a pattern  ${text}  ${pattern}  ${msg}

    set test variable  ${exit_code}  ${match}[exit_code]


change directory
    [Tags]  flatten-keyword
    [Documentation]  Go to the given directory
    [Arguments]
    ...  ${console}
    ...  ${dir}
    ...  ${msg}=Failed to change directory!

    execute command and set test variable
    ...  console=${console}
    ...  command=cd ${dir}
    verify exit code
    ...  msg=${msg}


search for one of patterns
    [Tags]  flatten-keyword
    [Documentation]  Search for one of patterns and return match group
    [Arguments]
    ...  ${text}
    ...  ${patterns}
    ...  ${msg}="Not found a one of patterns!"

    &{matches}=  should match one of regexp list  ${text}  ${patterns}  ${msg}

    set test variable  &{matches}


search for a regexp for table
    [Tags]  flatten-keyword
    [Documentation]  Search for a pattern on the table and return match
    [Arguments]
    ...  ${text}
    ...  ${pattern}
    ...  ${msg}=Not found a pattern on table of information!

    &{matches}=  should match a regexp for table  ${text}  ${pattern}  ${msg}

    set test variable  &{matches}


could not search for a regexp for table
    [Tags]  flatten-keyword
    [Documentation]  Could not search for a pattern on the table and if not return match
    [Arguments]
    ...  ${text}
    ...  ${pattern}
    ...  ${msg}=found a pattern on table of information!

    &{matches}=  should not match a regexp for table  ${text}  ${pattern}

    set test variable  &{matches}


search for a pattern
    [Tags]  flatten-keyword
    [Documentation]  Search for a pattern and return match
    [Arguments]
    ...  ${text}
    ...  ${pattern}
    ...  ${msg}=${EMPTY}

    &{match}=  should match a regexp  ${text}  ${pattern}  ${msg}

    set test variable  &{match}


search for ordered pattern list
    [Tags]  flatten-keyword
    [Documentation]  Search for ordered pattern list and return match group
    [Arguments]
    ...  ${text}
    ...  ${patterns}
    ...  ${msg}=Not found a pattern list or wrong order to search for!

    &{matches}=  should match ordered regexp list  ${text}  ${patterns}  ${msg}

    set test variable  &{matches}


search for paired pattern list
    [Tags]  flatten-keyword
    [Documentation]  Search for pattern list with ordered and return match group
    [Arguments]
    ...  ${text}
    ...  ${patterns}
    ...  ${msg}=Not found a pattern list or wrong order to search for!

    &{matches}=  should match paired regexp list  ${text}  ${patterns}  ${msg}

    set test variable  &{matches}


execute command and set test variable
    [Tags]  flatten-keyword
    [Documentation]  Execute "${command}" on ${console} prompt
    [Arguments]
    ...  ${console}
    ...  ${command}
    ...  ${sec}=60

    ${text}=  execute command
    ...  cmd=${command}
    ...  mode=${console}
    ...  timeout=${sec}

    set test variable  ${text}
    set test variable  ${console}


execute command and verify with a pattern for table
    [Tags]  flatten-keyword
    [Documentation]  Execute command and verify with a pattern for table
    [Arguments]
    ...  ${console}
    ...  ${command}
    ...  ${path}=${EMPTY}
    ...  ${sec}=60
    ...  ${pattern}=
    ...  ${msg}=${EMPTY}
    ...  ${is_check_exit_code}=${TRUE}
    ...  ${reverse_judgment}=${FALSE}

    run keyword if  '${path}' != '${EMPTY}'
    ...  change directory  console=${console}  dir=${path}

    execute command and set test variable  console=${console}  command=${command}  sec=${sec}
    run keyword if  '${is_check_exit_code}' == '${TRUE}'
    ...  verify exit code
    run keyword if  '${reverse_judgment}' == '${TRUE}'
    ...  could not search for a regexp for table  text=${text}  pattern=${pattern}  msg=${msg}
    ...  ELSE
    ...  search for a regexp for table  text=${text}  pattern=${pattern}  msg=${msg}


execute command and verify with paired pattern list
    [Tags]  flatten-keyword
    [Documentation]  Execute command and verify with paired pattern list
    [Arguments]
    ...  ${console}
    ...  ${command}
    ...  ${path}=${EMPTY}
    ...  ${sec}=60
    ...  ${patterns}=
    ...  ${msg}=${EMPTY}

    run keyword if  '${path}' != '${EMPTY}'
    ...  change directory  console=${console}  dir=${path}

    execute command and set test variable  console=${console}  command=${command}  sec=${sec}
    verify exit code
    search for paired pattern list  text=${text}  patterns=${patterns}  msg=${msg}


execute command and verify with ordered pattern list
    [Tags]  flatten-keyword
    [Documentation]  execute command and verify with ordered pattern list
    [Arguments]
    ...  ${console}
    ...  ${command}
    ...  ${patterns}
    ...  ${path}=${EMPTY}
    ...  ${sec}=60
    ...  ${msg}=${EMPTY}
    ...  ${is_check_exit_code}=${TRUE}

    run keyword if  '${path}' != '${EMPTY}'
    ...  change directory  console=${console}  dir=${path}

    execute command and set test variable  console=${console}  command=${command}  sec=${sec}
    run keyword if  '${is_check_exit_code}' == '${TRUE}'
    ...  verify exit code
    search for ordered pattern list  text=${text}  patterns=${patterns}  msg=${msg}


execute command and verify with a pattern
    [Tags]  flatten-keyword
    [Documentation]  Execute command and verify with a pattern
    [Arguments]
    ...  ${console}
    ...  ${command}
    ...  ${path}=${EMPTY}
    ...  ${sec}=60
    ...  ${pattern}=
    ...  ${msg}=${EMPTY}
    ...  ${is_check_exit_code}=${TRUE}

    run keyword if  '${path}' != '${EMPTY}'
    ...  change directory  console=${console}  dir=${path}

    execute command and set test variable  console=${console}  command=${command}  sec=${sec}
    run keyword if  '${is_check_exit_code}' == '${TRUE}'
    ...  verify exit code
    search for a pattern  text=${text}  pattern=${pattern}  msg=${msg}


execute command and verify with unexpected patterns
    [Tags]  flatten-keyword
    [Documentation]  Execute command and verify, fails if found one of patterns
    [Arguments]
    ...  ${console}
    ...  ${command}
    ...  ${patterns}
    ...  ${path}=${EMPTY}
    ...  ${sec}=60
    ...  ${msg}=Should not found any one of fail patterns!
    ...  ${is_check_exit_code}=${TRUE}

    run keyword if  '${path}' != '${EMPTY}'
    ...  change directory  console=${console}  dir=${path}

    execute command and set test variable  console=${console}  command=${command}  sec=${sec}
    run keyword if  '${is_check_exit_code}' == '${TRUE}'
    ...  verify exit code
    ${status}  ${value}=  Run Keyword And Ignore Error
    ...  search for one of patterns  text=${text}  patterns=${patterns}  msg=${msg}
    Run Keyword If  '${status}' == 'PASS'
    ...  Fail  ${msg}


execute command and verify with unordered pattern list
    [Tags]  flatten-keyword
    [Documentation]  execute command and verify with unordered pattern list
    [Arguments]
    ...  ${console}
    ...  ${command}
    ...  ${patterns}
    ...  ${path}=${EMPTY}
    ...  ${sec}=60
    ...  ${msg}=${EMPTY}
    ...  ${is_check_exit_code}=${TRUE}

    run keyword if  '${path}' != '${EMPTY}'
    ...  change directory  console=${console}  dir=${path}

    execute command and set test variable  console=${console}  command=${command}  sec=${sec}
    run keyword if  '${is_check_exit_code}' == '${TRUE}'
    ...  verify exit code
    search for one of patterns  text=${text}  patterns=${patterns}  msg=${msg}


execute command and verify exit code
    [Tags]  flatten-keyword
    [Documentation]  execute command and verify exit code (no verify the output)
    [Arguments]
    ...  ${console}
    ...  ${command}
    ...  ${exit_code_pattern}=(?m)^(?P<exit_code>0)$
    ...  ${path}=${EMPTY}
    ...  ${sec}=60
    ...  ${msg}=An exit code is not return zero/success!
    ...  ${is_check_exit_code}=${TRUE}

    run keyword if  '${path}' != '${EMPTY}'
    ...  change directory  console=${console}  dir=${path}

    execute command and set test variable  console=${console}  command=${command}  sec=${sec}
    run keyword if  '${is_check_exit_code}' == '${TRUE}'
    ...  verify exit code  msg=${msg}  pattern=${exit_code_pattern}


sleep for second(s)
    [Tags]  flatten-keyword
    [Documentation]  Send sleep command to Linux to sleep some second(s) to wait for something upcoming
    [Arguments]
    ...  ${console}
    ...  ${sleep}=1
    ...  ${sec}=5

    # Offset / wait for this command is more than its sleep time
    ${sec}=  Evaluate  ${sleep} + ${sec}

    execute command and verify exit code
    ...  console=${console}
    ...  command=sleep ${sleep}
    ...  sec=${sec}


reboot UNIX-like OS
    [Tags]  flatten-keyword
    [Documentation]  Issue reboot command and wait for the system boot-up
    [Arguments]
    ...  ${console}
    ...  ${sec}=300

    send a line  reboot

    read until regexp
    ...  patterns=\ login:
    ...  timeout=${sec}


Set terminal auto-logout timeout
    [Tags]  flatten-keyword
    [Documentation]  Set TMOUT (auto-logout) to given UNIX-like terminal
    [Arguments]
    ...  ${console}
    ...  ${timeout}=0  # 0 = disable
    ...  ${sec}=10

    execute command and verify exit code
    ...  console=${console}
    ...  command=(unset TMOUT && export TMOUT=${timeout})


ssh execute
    [Tags]  flatten-keyword
    [Documentation]  Execute command on SSH Server
    [Arguments]
    ...  ${console}
    ...  ${command}
    ...  ${sec}=10
    ...  ${ip_version}=-4
    ...  ${ssh_option}=-o "UserKnownHostsFile=/dev/null" -o "StrictHostKeyChecking=no"
    ...  ${port}=22
    ...  ${username}=
    ...  ${password}=
    ...  ${server_ip}=

    open prompt  console=${console}  sec=300
    send a line  command=ssh ${ip_version} -p ${port} ${ssh_option} ${username}@${server_ip} ${command}
    read until regexp  patterns='s password  timeout=300
    send a line  command=${password}
    ${text}=  read until regexp  patterns=.*?@.*?:  timeout=${sec}
    verify exit code
    ...  msg=Failed to execute command on SSH Server!

    set test variable  ${text}


change kernel log level
    [Tags]  flatten-keyword
    [Arguments]
    ...  ${console}
    ...  ${level}=7

    execute command and verify exit code
    ...  console=${console}
    ...  command=sysctl -w kernel.printk=${level}
# End of utility keyword


# File keyword
is file/folder exists
    [Tags]  flatten-keyword
    [Arguments]
    ...  ${console}
    ...  ${file}
    ...  ${sec}=60

    execute command and set test variable
    ...  command=test -f ${file}
    ...  console=${console}
    verify exit code
    ...  pattern=(?m)^(?P<exit_code>\\d)$


remove file/folder
    [Tags]  flatten-keyword
    [Arguments]
    ...  ${console}
    ...  ${file}
    ...  ${sec}=60

    execute command and set test variable
    ...  command=rm -rf ${file}
    ...  console=${console}
    verify exit code
    ...  pattern=(?m)^(?P<exit_code>\\d)$


create directory
    [Tags]  flatten-keyword
    [Arguments]
    ...  ${console}
    ...  ${dir}
    ...  ${sec}=60

    execute command and set test variable
    ...  command=mkdir -p ${dir}
    ...  console=${console}
    verify exit code
    ...  msg=Failed to create new directory!


decompress xz file
    [Tags]  flatten-keyword
    [Arguments]
    ...  ${console}
    ...  ${file}
    ...  ${path}=${EMPTY}
    ...  ${sec}=180

    run keyword if  '${path}' != '${EMPTY}'
    ...  change directory  console=${console}  dir=${path}

    execute command and set test variable
    ...  console=${console}
    ...  command=xz -f -d ${file}
    ...  sec=${sec}
    verify exit code
    ...  msg=Failed to decompress xz file!


decompress tar file
    [Tags]  flatten-keyword
    [Arguments]
    ...  ${console}
    ...  ${file}
    ...  ${path}=${EMPTY}
    ...  ${extract_only}=${EMPTY}  # Default (extract all file/folder)
    ...  ${sec}=180

    run keyword if  '${path}' != '${EMPTY}'
    ...  change directory  console=${console}  dir=${path}

    execute command and set test variable
    ...  console=${console}
    ...  command=tar -xf ${file} ${extract_only}
    ...  sec=${sec}
    verify exit code
    ...  msg=Failed to decompress tar file!


show file content
    [Tags]  flatten-keyword
    [Arguments]
    ...  ${console}
    ...  ${file}
    ...  ${path}=${EMPTY}
    ...  ${sec}=10

    run keyword if  '${path}' != '${EMPTY}'
    ...  change directory  console=${console}  dir=${path}

    execute command and set test variable
    ...  console=${console}
    ...  command=cat ${file}
    ...  sec=${sec}
    verify exit code
    ...  msg=Failed to decompress tar file!


file edit and replace a line
    [Tags]  flatten-keyword
    [Arguments]
    ...  ${console}
    ...  ${file}
    ...  ${sed_pattern}
    ...  ${path}=${EMPTY}
    ...  ${sec}=10

    execute command and verify exit code
    ...  console=${console}
    ...  path=${path}
    ...  command=sed -ir '${sed_pattern}' ${file}
    ...  sec=${sec}


move file/folder
    [Tags]  flatten-keyword
    [Arguments]
    ...  ${console}
    ...  ${source}
    ...  ${destination}
    ...  ${sec}=60

    execute command and verify exit code
    ...  console=${console}
    ...  command=mv -f ${source} ${destination}
    ...  sec=${sec}


copy file/folder
    [Tags]  flatten-keyword
    [Arguments]
    ...  ${console}
    ...  ${source}
    ...  ${destination}
    ...  ${sec}=${3 * 60}

    execute command and verify exit code
    ...  console=${console}
    ...  command=cp -rf ${source} ${destination}
    ...  sec=${sec}
# End of file keyword


# Network keyword
secure copy file
    [Tags]  flatten-keyword
    [Documentation]  copy given file/folder by scp command
    [Arguments]
    ...  ${console}
    ...  ${sec}=60
    ...  ${ip_version}=-4
    ...  ${ssh_option}=-o "UserKnownHostsFile=/dev/null" -o "StrictHostKeyChecking=no"
    ...  ${port}=22
    ...  ${username}=
    ...  ${password}=
    ...  ${source_ip}=
    ...  ${source_path}=
    ...  ${source_file}=
    ...  ${destination}=
    ...  ${always_copy}=${FALSE}
    ...  ${has_md5sum}=${FALSE}
    ...  ${md5sum_sec}=30

    is file/folder exists
    ...  console=${console}
    ...  file=${destination}/${source_file}
    run keyword if  '${exit_code}' == '0' and '${always_copy}' == '${FALSE}'  run keywords
    ...  log  File(s) or folder(s) already exist, no needed to copy  AND
    ...  return from keyword

    create directory  console=${console}  dir=${destination}

    open prompt  console=${console}  sec=300
    send a line  command=time (scp ${ip_version} -P ${port} ${ssh_option} ${username}@${source_ip}:${source_path}/${source_file} ${destination})
    read until pattern  pattern='s password
    send a line  command=${password}
    read until pattern  pattern=100%  sec=${sec}
    Run Keyword And Ignore Error  read until regexp  patterns=sys.*s  timeout=${sec}
    verify exit code
    ...  msg=Failed to copy file/folder by SCP!

    run keyword if  '${has_md5sum}' == '${TRUE}'  run keywords
    ...  send a line  command=scp ${ip_version} -P ${port} ${ssh_option} ${username}@${source_ip}:${source_path}/${source_file}.md5sum ${destination}  AND
    ...  read until pattern  pattern='s password  AND
    ...  send a line  command=${password}  AND
    ...  read until pattern  pattern=100%  sec=${sec}  AND
    ...  verify exit code  msg=Failed to copy file/folder by SCP!  AND
    ...  execute command and verify exit code  console=${console}  path=${destination}  command=md5sum -c ${source_file}.md5sum  sec=${md5sum_sec}  AND
    ...  remove file/folder  console=${console}  file=${source_file}.md5sum


BusyBox TFTP get file
    [Tags]  flatten-keyword
    [Documentation]  BusyBox TFTP get file
    [Arguments]
    ...  ${console}
    ...  ${server}
    ...  ${file}
    ...  ${where_to_download}=${EMPTY}
    ...  ${save_to}=${EMPTY}
    ...  ${sec}=180
    ...  ${has_md5sum}=${FALSE}
    ...  ${md5sum_sec}=30

    run keyword if  '${save_to}' != '${EMPTY}'  run keywords
    ...  create directory  console=${console}  dir=${save_to}  AND
    ...  change directory  console=${console}  dir=${save_to}

    execute command and set test variable
    ...  command=tftp -g ${server} -r ${where_to_download}/${file}
    ...  console=${console}
    ...  sec=${sec}
    verify exit code
    ...  msg=Failed to get a file by BusyBox TFTP!

    run keyword if  '${has_md5sum}' == '${TRUE}'  run keywords
    ...  execute command and set test variable  console=${console}  command=tftp -g ${server} -r ${where_to_download}/${file}.md5sum  sec=60  AND
    ...  verify exit code  msg=Failed to get a file's md5sum by BusyBox TFTP!  AND
    ...  execute command and set test variable  console=${console}  command=md5sum -c ${file}.md5sum  sec=${md5sum_sec}  AND
    ...  verify exit code  msg=MD5SUM does not match!  AND
    ...  remove file/folder  console=${console}  file=${file}.md5sum


assign and verify network interface IP
    [Documentation]  Verify written IP to network interface
    [Arguments]
    ...  ${interface}=${tftp_interface}
    ...  ${network_id}=${diagos_network_id}
    ...  ${console}=${diagos_mode}

    down network interface  console=${console}  interface=${interface}
    flush network interface  console=${console}  interface=${interface}
    assign IP to network interface  console=${console}  network_id=${network_id}  interface=${interface}
    up network interface  console=${console}  interface=${interface}
    show network interface IP  console=${console}  interface=${interface}
    compare two dictionaries by value
    ...  original=${written_ip}
    ...  compare=${assigned_ip}
    ...  msg=Written IP Address does not match read IP Address on the interface!


show network interface IP
    [Tags]  flatten-keyword
    [Documentation]  show network interface IP
    [Arguments]
    ...  ${console}
    ...  ${interface}
    ...  ${sec}=15
    ...  ${pattern}=(?m)^[ \\t]+inet6?[ \\t]+(?P<network_id>[\\w\\.:\\/]+)
    ...  ${path}=${EMPTY}
    ...  ${msg}=Failed to set network interface UP!

    # execute command and verify with a pattern
    execute command and verify with a pattern for table
    ...  path=${path}
    ...  command=ip addr show ${interface}
    ...  console=${console}
    ...  pattern=${pattern}
    ...  msg=${msg}

    set test variable  &{assigned_ip}  &{matches}


ping to IP
    [Tags]  flatten-keyword
    [Documentation]  Ping to given IP and show statistic
    [Arguments]
    ...  ${console}
    ...  ${ip}
    ...  ${msg}=Failed ping check!
    # Leave ip_ver empty for IPv4 and 6 for IPv6
    ...  ${ip_ver}=
    ...  ${time}=3
    ...  ${sec}=30

    execute command and set test variable
    ...  command=ping${ip_ver} -c ${time} ${ip}
    ...  console=${console}
    ...  sec=${sec}
    verify exit code
    ...  msg=${msg}


renew IP using DHCP
    [Tags]  flatten-keyword
    [Documentation]  Release and obtain new IP using DHCP
    [Arguments]
    ...  ${console}
    ...  ${interface}
    ...  ${msg}=Failed to obtain new IP using DHCP!
    # Leave ip_ver empty is auto, -4/-6 to specified IP version
    ...  ${ip_ver}=-4
    ...  ${sec}=120
    ...  ${pattern}=(?m)^DHCPACK (?:of (?P<dhcp_our_new_ip>(?:\\d{1,3}\\.?){4}) )?from (?P<dhcp_server_ip>(?:\\d{1,3}\\.?){4})$

    # Release and obtain a new IP
    execute command and set test variable
    ...  command=dhclient -v -r ${interface}
    ...  console=${console}
    ...  sec=10

    execute command and set test variable
    ...  command=dhclient -v ${ip_ver} ${interface}
    ...  console=${console}
    ...  sec=${sec}
    verify exit code
    ...  msg= ${msg}

    search for a pattern
    ...  text=${text}
    ...  pattern=${pattern}
    ...  msg=Not found the DHCP Server IPv4 and/or failed to bound to new IPv4!

    set test variable  &{dhcp_renew_info}  &{match}


assign IP to network interface
    [Tags]  flatten-keyword
    [Documentation]  Assign given IP to network interface
    [Arguments]
    ...  ${console}
    ...  ${network_id}
    ...  ${interface}
    ...  ${sec}=15
    ...  ${pattern}=(?m)ip[ \\t]+addr[ \\t]+add[ \\t]+(?P<network_id>[\\w\\.:\\/]+)
    ...  ${path}=${EMPTY}
    ...  ${msg}=Failed to assign new IP to network interface!

    execute command and verify with a pattern
    ...  path=${path}
    ...  command=ip addr add ${network_id} dev ${interface}
    ...  console=${console}
    ...  sec=${sec}
    ...  pattern=${pattern}
    ...  msg=${msg}

    set test variable  &{written_ip}  &{match}


flush network interface
    [Tags]  flatten-keyword
    [Documentation]  Flush the network interface
    [Arguments]
    ...  ${console}
    ...  ${interface}
    ...  ${sec}=15
    ...  ${msg}=Failed to flush network IP!

    execute command and set test variable
    ...  command=ip addr flush dev ${interface}
    ...  console=${console}
    ...  sec=${sec}
    verify exit code
    ...  msg= ${msg}


up network interface
    [Tags]  flatten-keyword
    [Documentation]  Set the network interface up
    [Arguments]
    ...  ${console}
    ...  ${interface}
    ...  ${sec}=15
    ...  ${msg}=Failed to set network interface UP!

    execute command and set test variable
    ...  command=ip link set ${interface} up
    ...  console=${console}
    ...  sec=${sec}
    verify exit code
    ...  msg=${msg}


down network interface
    [Tags]  flatten-keyword
    [Documentation]  Set the network interface down
    [Arguments]
    ...  ${console}
    ...  ${interface}
    ...  ${sec}=15
    ...  ${msg}=Failed to set network interface DOWN!

    execute command and set test variable
    ...  command=ip link set ${interface} down
    ...  console=${console}
    ...  sec=${sec}
    verify exit code
    ...  msg=${msg}


verify network interface MAC address
    [Tags]  flatten-keyword
    [Arguments]
    ...  ${console}
    ...  ${interface}
    ...  ${mac}=(?:[a-fA-F0-9]{2}:?){6}
    ...  ${path}=${EMPTY}
    ...  ${pattern}=HWaddr[ \\\\t]+(?P<ifconfig_mac>${mac})
    ...  ${sec}=15
    ...  ${msg}=Not found the MAC address / ${mac} on the interface ${interface}!

    execute command and verify with a pattern
    ...  console=${console}
    ...  path=${path}
    ...  command=ifconfig ${interface}
    ...  pattern=${pattern}
    ...  msg=${msg}
    ...  sec=${sec}

    set test variable  &{ifconfig_mac}  &{match}


add and verify IP to network interface
    [Tags]  flatten-keyword
    [Arguments]
    ...  ${console}
    ...  ${interface}
    ...  ${ip}
    ...  ${pattern}=(?m)^[ \\t]*inet6?.*?\\ (?P<ip>[\\w\\.\\:\\/]+)
    ...  ${path}=${EMPTY}
    ...  ${sec}=3
    ...  ${msg}=Failed to add new IP to network interface name ${interface}!

    execute command and verify with a pattern for table
    ...  console=${console}
    ...  command=(ip addr add ${ip} dev ${interface} && ip addr show dev ${interface})
    ...  pattern=${pattern}
    ...  path=${path}
    ...  sec=${sec}
    ...  msg=${msg}

    set test variable  &{ifconfig_add_ip}  &{matches}


BusyBox ifconfig add and verify IP to network interface
    [Tags]  flatten-keyword
    [Arguments]
    ...  ${console}
    ...  ${interface}
    ...  ${ip}
    ...  ${pattern}=(?m)^[ \\t]*inet6?.*?:\\ (?P<ip>[\\w\\.\\:\\/]+)
    ...  ${path}=${EMPTY}
    ...  ${sec}=5
    ...  ${msg}=Failed to add new IP to network interface name ${interface}!

    execute command and verify with a pattern for table
    ...  console=${console}
    ...  command=(ifconfig ${interface} "${ip}" && ifconfig ${interface})
    ...  pattern=${pattern}
    ...  path=${path}
    ...  sec=${sec}
    ...  msg=${msg}

    set test variable  &{ifconfig_add_ip}  &{matches}


OpenBMC renew IP using DHCP and set variable
    [Arguments]
    ...  ${console}=${openbmc_mode}
    ...  ${interface}=eth0
    ...  ${pattern}=(?m)^bound to (?P<dhcp_our_new_ip>(?:\\d{1,3}\\.?){4})

    renew IP using DHCP
    ...  console=${console}
    ...  interface=${interface}
    ...  pattern=${pattern}
    set test variable  &{openbmc_dhcp_info}  &{dhcp_renew_info}


DiagOS renew IP using DHCP and set variable
    [Arguments]
    ...  ${console}=${diagos_mode}
    ...  ${interface}=eth0
    ...  ${pattern}=(?m)^bound to (?P<dhcp_our_new_ip>(?:\\d{1,3}\\.?){4})

    renew IP using DHCP
    ...  console=${console}
    ...  interface=${interface}
    ...  pattern=${pattern}
    set test variable  &{diagos_dhcp_info}  &{dhcp_renew_info}
# End of network keyword

# Kernel utils
kernel module info
    [Tags]  flatten-keyword
    [Documentation]  Show kernel module informaion
    [Arguments]
    ...  ${console}
    ...  ${module}
    ...  ${command}=modinfo
    ...  ${sec}=15
    ...  ${exit_code_pattern}=(?m)^(?P<exit_code>0)$
    ...  ${msg}=Failed to show kernel module information!

    execute command and set test variable
    ...  command=${command} ${module}
    ...  console=${console}
    ...  sec=${sec}
    set test variable  ${modinfo_text}  ${text}
    verify exit code
    ...  pattern=${exit_code_pattern}
    ...  msg=${msg}


insert kernel module
    [Tags]  flatten-keyword
    [Documentation]  Insert given kernel module
    [Arguments]
    ...  ${console}
    ...  ${module}
    ...  ${command}=insmod
    ...  ${sec}=15
    ...  ${exit_code_pattern}=(?m)^(?P<exit_code>0)$
    ...  ${msg}=Failed to insert/load kernel module!

    execute command and set test variable
    ...  command=${command} ${module}
    ...  console=${console}
    ...  sec=${sec}
    set test variable  ${insmod_text}  ${text}
    verify exit code
    ...  pattern=${exit_code_pattern}
    ...  msg=${msg}


unload kernel module
    [Tags]  flatten-keyword
    [Documentation]  Unload given kernel module
    [Arguments]
    ...  ${console}
    ...  ${module}
    ...  ${command}=rmmod  # Do not recommend for -f option! If needed can place it here
    ...  ${sec}=15
    ...  ${exit_code_pattern}=(?m)^(?P<exit_code>0)$
    ...  ${msg}=Failed to remove/unload kernel module!

    execute command and set test variable
    ...  command=${command} ${module}
    ...  console=${console}
    ...  sec=${sec}
    set test variable  ${rmmod_text}  ${text}
    verify exit code
    ...  pattern=${exit_code_pattern}
    ...  msg=${msg}


unload kernel module matched *.ko file
    [Tags]  flatten-keyword
    [Documentation]  Unload given kernel module matched *.ko file
    [Arguments]
    ...  ${console}
    ...  ${path}=${EMPTY}

    run keyword if  '${path}' != '${EMPTY}'
    ...  change directory  console=${console}  dir=${path}

    Run Keyword And Ignore Error  unload kernel module
    ...  console=${console}
    ...  module=*\\.ko

    Run Keyword And Ignore Error  unload kernel module
    ...  console=${console}
    ...  module=*\\.ko

    list kernel module file  ${console}
    FOR  ${key}  ${value}  IN  &{kmod_file_name_list}
        unload kernel module  console=${console}  module=${value}  exit_code_pattern=(?m)^(?P<exit_code>\\d)$
        search for a pattern
        ...  text=${rmmod_text}
        ...  pattern=(?m)^(?P<PASS>rmmod.*ERROR.*is not currently loaded)$
    END


list loaded kernel module
    [Tags]  flatten-keyword
    [Documentation]  List loaded kernel module
    [Arguments]
    ...  ${console}
    ...  ${pattern}=(?m)^(?P<kmod_name>\\w+)[ \\t]+\\d+[ \\t]+\\d+[ \\t]*$
    ...  ${sec}=10
    ...  ${msg}=Failed to list loaded kernel module!

    execute command and verify with a pattern for table
    ...  path=${EMPTY}
    ...  command=lsmod
    ...  console=${console}
    ...  sec=${sec}
    ...  pattern=${pattern}
    ...  msg=${msg}

    set test variable  &{kmod_loaded}  &{matches}


list kernel module file
    [Tags]  flatten-keyword
    [Documentation]  List kernel module file
    [Arguments]
    ...  ${console}
    ...  ${command}=ls -1 --color=never *\\.ko
    ...  ${path}=${EMPTY}
    ...  ${pattern}=(?m)^(?P<kmod_file_name>[\\w\\-_]+\\.ko)$

    execute command and verify with a pattern for table
    ...  console=${console}
    ...  command=${command}
    ...  path=${path}
    ...  pattern=${pattern}

    set test variable  &{kmod_file_name_list}  &{matches}
# End of Kernel utils

# U-Boot
U-Boot save current environment to flash memory
    [Tags]  flatten-keyword
    [Documentation]  U-Boot save current environment to flash memory
    [Arguments]
    ...  ${console}=${uboot_mode}
    ...  ${command}=save

    execute command and verify exit code
    ...  console=${console}
    ...  command=${command}


U-Boot reset environment to default
    [Tags]  flatten-keyword
    [Documentation]  U-Boot resetting to default environment
    [Arguments]
    ...  ${console}=${uboot_mode}
    ...  ${command}=env default -a

    execute command and verify exit code
    ...  console=${console}
    ...  command=${command}


U-Boot setenv
    [Tags]  flatten-keyword
    [Documentation]  Set given U-Boot ENV variable
    [Arguments]
    ...  ${console}=${uboot_mode}
    ...  ${env}=

    execute command and verify exit code
    ...  console=${console}
    ...  command=setenv ${env}


U-Boot renew DHCP/IP
    [Tags]  flatten-keyword
    [Documentation]  Get new IP by DHCP client on U-Boot
    [Arguments]
    ...  ${console}=${uboot_mode}
    ...  ${command}=dhcprelease && dhcp
    ...  ${patterns}=${uboot_dhcp_patterns}

    execute command and verify with ordered pattern list
    ...  console=${console}
    ...  command=${command}
    ...  patterns=${patterns}
    ...  msg=Failed to release and renew IP by DHCP on U-Boot!


U-Boot reset
    [Tags]  flatten-keyword
    [Documentation]  U-Boot execute reset
    [Arguments]
    ...  ${sec}=300

    open prompt
    ...  console=${uboot_mode}
    ...  sec=${sec}

    send a line
    ...  command=reset

    read until regexp
    ...  patterns=${STOP_AUTOBOOT_PROMPT}
    ...  timeout=${sec}

    send a line
    ...  command=${STOP_AUTOBOOT_KEY}

    read until regexp
    ...  patterns=${uboot_prompt}
    ...  timeout=10
# End of U-Boot utils

# EFI boot
EFI show boot information
    [Tags]  flatten-keyword
    [Arguments]
    ...  ${console}
    ...  ${command}=efibootmgr

    execute command and verify exit code
    ...  console=${console}
    ...  command=${command}

    set test variable  ${efi_boot_text}  ${text}


EFI find boot order
    [Tags]  flatten-keyword
    [Arguments]
    ...  ${console}
    ...  ${pattern}
    ...  ${msg}=Failed to find for the boot order!

    EFI show boot information  console=${console}
    search for a pattern
    ...  text=${efi_boot_text}
    ...  pattern=${pattern}
    ...  msg=${msg}

    set test variable  &{efi_boot_order}  &{match}


EFI whereof boot priority
    [Tags]  flatten-keyword
    [Arguments]
    ...  ${console}
    ...  ${patterns}
    ...  ${msg}=Failed not found for some boot priority!

    EFI show boot information  console=${console}
    search for one of patterns
    ...  text=${efi_boot_text}
    ...  patterns=${patterns}
    ...  msg=${msg}

    set test variable  &{efi_whereof}  &{matches}


EFI compare boot order
    [Tags]  flatten-keyword
    [Arguments]
    ...  ${boot_priority_higher}
    ...  ${boot_priority_lower}
    ...  ${msg}=Failed, the boot order A priority is less than boot order B priority!

    ${efi_boot_order_value_list}=  Get Dictionary Values  ${efi_boot_order}
    ${efi_boot_priority_higher}=  Get Index From List  ${efi_boot_order_value_list}  ${boot_priority_higher}
    ${efi_boot_priority_lower}=  Get Index From List  ${efi_boot_order_value_list}  ${boot_priority_lower}
    run keyword if  '${efi_boot_priority_higher}' > '${efi_boot_priority_lower}'
    ...  Fail  ${msg}


EFI verify current boot
    [Tags]  flatten-keyword
    [Arguments]
    ...  ${console}
    ...  ${pattern}=BootCurrent: (?P<efi_current_boot>\\d+)
    ...  ${msg}=Failed, can not find EFI current boot information!

    EFI show boot information  console=${console}
    search for a pattern
    ...  text=${efi_boot_text}
    ...  pattern=${pattern}
    ...  msg=${msg}

    set test variable  &{efi_current_boot}  &{match}
# End of EFI boot

# date/time
date/time difference
    [Tags]  flatten-keyword
    [Arguments]
    ...  ${date1}
    ...  ${date2}
    ...  ${diff}
    ...  ${msg}=Failed, the date differential is more than expected!
    ...  ${exclude_millis}=${TRUE}

    ${date_diff}=  Subtract Date From Date
    ...  ${date1}  ${date2}
    ...  exclude_millis=${exclude_millis}
    run keyword if  '${date_diff}' > '${diff}'
    ...  Fail  ${msg}
# End of date/time
