###############################################################################
# LEGALESE:   "Copyright (C) 2021, Celestica Corp. All rights reserved."      #
#                                                                             #
# This source code is confidential, proprietary, and contains trade           #
# secrets that are the sole property of Celestica Corp.                       #
# Copy and/or distribution of this source code or disassembly or reverse      #
# engineering of the resultant object code are strictly forbidden without     #
# the written consent of Celestica Corp.                                      #
#                                                                             #
###############################################################################

*** Settings ***
Documentation   Alibaba common stress suite
Resource        CommonKeywords.resource
Resource        AliCommonKeywords.resource
Resource        AliStressKeywords.resource

Library         AliCommonLib.py
Library         CommonLib.py
Library         AliStressLib.py
Library         DateTime


*** Test Cases ***

ALI_STRESS_TC001_CPU_STRESS
    [Timeout]  ${stress_tc001_total_test_time_sec + 900} seconds
    [Tags]  ALI_STRESS_TC001_CPU_STRESS
    ...  migaloo

    [Setup]  Run Keywords
    ...  open prompt and login to root user  console=${diagos_mode}
    ...  AND  DiagOS renew IP using DHCP and set variable

    Step   1  secure copy file
    ...  console=${diagos_mode}
    ...  username=${scp_username}
    ...  password=${scp_password}
    ...  source_ip=${ssh_server_ipv4}
    ...  source_path=${tftp_root_path}/migaloo/image/STRESS
    ...  source_file=${stress_script_tarball_file}
    ...  destination=/tmp/STRESS
    ...  sec=${15 * 60}
    Step   2  decompress tar file
    ...  console=${diagos_mode}
    ...  path=/tmp/STRESS
    ...  file=${stress_script_tarball_file}
    Step   3  execute command and verify with a pattern
    ...  console=${diagos_mode}
    ...  command=grep "processor" /proc/cpuinfo | wc -l
    ...  pattern=(?m)^(?P<number_of_cpu>\\\\d+)$
    ...  msg=Failed, do not know the number of CPU(s)!
    set test variable  ${total_cpus}  ${match}

    set test variable  ${each_cpu_test_time}  ${${stress_tc001_total_test_time_sec}/${total_cpus}[number_of_cpu]}

    FOR  ${number_of_cpu}  IN RANGE  1  ${total_cpus}[number_of_cpu]+1  1
        Log  >>Stress test on ${number_of_cpu} CPU(s) of 12<<
        execute command and verify exit code
        ...  console=${diagos_mode}
        ...  command=killall -9 stress
        ...  exit_code_pattern=(?m)^(?P<exit_code>\\d+)$
        execute command and verify exit code
        ...  console=${diagos_mode}
        ...  path=/tmp/STRESS/STRESS/TS-Migaloo-01
        ...  command=rm -rf cpu_stress.log
        ...  exit_code_pattern=(?m)^(?P<exit_code>\\d+)$
        execute command and verify with a pattern for table
        ...  console=${diagos_mode}
        ...  path=/tmp/STRESS/STRESS/TS-Migaloo-01
        ...  command=(timeout --preserve-status --kill-after=${each_cpu_test_time + 5} ${each_cpu_test_time + 5} stress --cpu ${number_of_cpu} --vm-bytes 256M --timeout ${each_cpu_test_time} >> cpu_stress.log 2>&1 & sleep ${each_cpu_test_time * 0.9} && ps -eo user,pid,%cpu,%mem,command --sort=-pcpu -a | head -n ${number_of_cpu + 2} && wait)
        ...  pattern=(?m)^\\w+[ \\t]+\\d+[ \\t]+(?P<percent>(9[0-9](?:\\.\\d+)?|100))[ \\t]+\\d+\\.?\\d+[ \\t]+stress
        ...  sec=${each_cpu_test_time + 10}
        execute command and verify exit code
        ...  console=${diagos_mode}
        ...  path=/tmp/STRESS/STRESS/TS-Migaloo-01
        ...  command=test -f cpu_stress.log
        ...  msg=The Log file is not created!
        ${number_of_cpu_on_full_load}=  Get Length  ${matches}
        Should Be Equal As Integers
        ...  ${number_of_cpu}  ${number_of_cpu_on_full_load}
        ...  Failed, the CPU does not stress test full load for ${number_of_cpu} core(s) of ${total_cpus} cores!
    END


ALI_STRESS_TC002_SSD_STRESS
    [Timeout]  ${stress_tc002_total_test_time_sec + 900} seconds
    [Tags]  ALI_STRESS_TC002_SSD_STRESS
    ...  migaloo
    [Setup]  Run Keywords
    ...  open prompt and login to root user  console=${diagos_mode}
    ...  AND  DiagOS renew IP using DHCP and set variable

    Step   1  secure copy file
    ...  console=${diagos_mode}
    ...  username=${scp_username}
    ...  password=${scp_password}
    ...  source_ip=${ssh_server_ipv4}
    ...  source_path=${tftp_root_path}/migaloo/image/STRESS/STRESS/TS-Migaloo-02
    ...  source_file=SVT_COME_SATA_SSD_stress_test_v0.3.sh
    ...  destination=/tmp/STRESS
    Step  2  execute command and verify exit code
    ...  console=${diagos_mode}
    ...  path=/tmp/STRESS
    ...  command=./SVT_COME_SATA_SSD_stress_test_v0.3.sh
    ...  exit_code_pattern=(?m)^(?P<exit_code>\\\\d+)$
    ...  sec=${stress_tc002_total_test_time_sec}


ALI_STRESS_TC003_MEMORY_STRESS_TEST
    [Timeout]  ${stress_tc003_total_test_time_sec + 900} seconds
    [Tags]  ALI_STRESS_TC003_MEMORY_STRESS_TEST
    ...  migaloo
    [Setup]  open prompt and login to root user  console=${diagos_mode}
    Step   1  execute command and verify exit code
    ...  console=${diagos_mode}
    ...  command=killall -9 stressapptest
    ...  exit_code_pattern=(?m)^(?P<exit_code>\\\\d+)$
    Step   2  execute command and verify with a pattern
    ...  console=${diagos_mode}
    ...  path=${diagos_tool_path}
    ...  command=./stressapptest -s ${stress_tc003_total_test_time_sec} -M 5000 -m 8 -i 8 -C 8 -l 2
    ...  pattern=(?i)Status\\: (?P<result>PASS)
    ...  msg=The Stress Test result is not pass!${\n}Not found the pass pattern!
    ...  sec=${stress_tc003_total_test_time_sec + 60}


ALI_STRESS_TC004_USB_RW_STRESS
    [Timeout]  ${stress_tc004_total_test_time_sec + 900} seconds
    [Tags]  ALI_STRESS_TC004_USB_RW_STRESS
    ...  migaloo

    [Setup]  open prompt and login to root user  console=${diagos_mode}

    ${date_start}=  Get Time

    execute command and verify with a pattern for table
    ...  console=${diagos_mode}
    ...  command=(echo p | fdisk /dev/sdb)
    ...  pattern=(?P<path>\\/dev\\/sdb\\d+)
    ...  sec=${2 * 60}
    ...  msg=Failed, not found the USB Storage!
    ...  is_check_exit_code=${FALSE}
    ${number_of_usb_drive}=  Get Length  ${matches}
    Run Keyword If  '${number_of_usb_drive}' != '${1}'
    ...  Fail  Found more than one USB Drive, it should be found only one USB Drive!${\n}Or not found any USB Drive!

    execute command and verify exit code
    ...  console=${diagos_mode}
    ...  command=umount /tmp/usb-sdbx-mount-point
    ...  exit_code_pattern=(?m)^(?P<exit_code>\\d+)$
    remove file/folder
    ...  console=${diagos_mode}
    ...  file=/tmp/usb-sdbx-mount-point
    create directory
    ...  console=${diagos_mode}
    ...  dir=/tmp/usb-sdbx-mount-point
    execute command and verify exit code
    ...  console=${diagos_mode}
    ...  command=mount ${matches}[path_1] /tmp/usb-sdbx-mount-point
    ...  msg=Failed to mount the USB Drive!

    FOR  ${loop}  IN RANGE  1  ${times_100000000}+1  1
        Log  >>The loop number #${loop}<<  console=${TRUE}

        execute command and verify exit code
        ...  console=${diagos_mode}
        ...  command=(sync && dd if=/dev/sdb1 of=/tmp/usb-sdbx-mount-point/delete-me bs=1000M count=1 && rm /tmp/usb-sdbx-mount-point/delete-me && sync)
        ...  sec=${2 * 60}

        ${date_stop}=  Get Time
        ${total_test_time}=  Subtract Date From Date
        ...  ${date_stop}  ${date_start}
        ...  result_format=timer
        ...  exclude_millis=${TRUE}
        ${total_test_time_sec}=  Convert Time
        ...  ${total_test_time}
        ...  result_format=number

        ${status}=  Evaluate  ${total_test_time_sec} >= ${stress_tc004_total_test_time_sec}
        Exit For Loop If  '${status}' == '${TRUE}'
    END

    Log  >>Total test time is ${total_test_time} (HH:MM:SS)<<  console=${TRUE}

    [Teardown]  Run Keywords
    ...  remove file/folder
    ...  console=${diagos_mode}
    ...  file=/tmp/usb-sdbx-mount-point/delete-me
    ...  AND  execute command and verify exit code
    ...  console=${diagos_mode}
    ...  command=umount /tmp/usb-sdbx-mount-point
    ...  exit_code_pattern=(?m)^(?P<exit_code>\\d+)$
    ...  AND  remove file/folder
    ...  console=${diagos_mode}
    ...  file=/tmp/usb-sdbx-mount-point


ALI_STRESS_TC005_10G_KR_STRESS
    [Timeout]  ${times_500 * 40 + 5 * 60} seconds
    [Tags]  ALI_STRESS_TC005_10G_KR_STRESS
    ...  migaloo
    [Setup]  open prompt and login to root user  console=${diagos_mode}

    Step  1  run cmd  cd ${diagos_cpu_sdk_path}  root@sonic
    Step  2  execute command  killall bcm.user
    step  3  run cmd  ./auto_load_user.sh  ${BCM_promptstr}
    Step  4  run cmd  ps xe  ${BCM_promptstr}
    Step  5  run cmd  vlan clear  ${BCM_promptstr}
    Step  6  run cmd  vlan create 250 pbm=xe0,xe1 ubm=xe0,xe1  ${BCM_promptstr}
    Step  7  run cmd  vlan show  ${BCM_promptstr}
    Step  8  run cmd  clear c  ${BCM_promptstr}
    Step  9  run cmd  sh  root@sonic
    Step  10  run cmd  cd ${diagos_cpu_diag_path}  root@sonic
    Step  11  test_10gkr_stress  ${test_10gkr_cmd}  ${platform}  ${times_500}
    [Teardown]  power reset sonic  mode=${diagos_mode}


ALI_STRESS_TC006_CPU_MANAGEMENT_PORT_PERFORMANCE_TEST
    [Timeout]  ${stress_tc006_total_test_time_sec + 900} seconds
    [Tags]  ALI_STRESS_TC006_CPU_MANAGEMENT_PORT_PERFORMANCE_TEST
    ...  migaloo

    [Setup]  Run Keywords
    ...  open prompt and login to root user  console=${diagos_mode}
    ...  AND  DiagOS renew IP using DHCP and set variable

    Step   1  secure copy file
    ...  console=${diagos_mode}
    ...  username=${scp_username}
    ...  password=${scp_password}
    ...  source_ip=${ssh_server_ipv4}
    ...  source_path=${tftp_root_path}/migaloo/image/STRESS/dpkg
    ...  source_file=iperf_2.0.9+dfsg1-1_amd64.deb
    ...  destination=/tmp/STRESS/dpkg
    ...  sec=${15 * 60}

    Step   2  execute command and verify exit code
    ...  console=${diagos_mode}
    ...  command=dpkg --force-overwrite --force-confnew -i /tmp/STRESS/dpkg/iperf_2.0.9+dfsg1-1_amd64.deb
    ...  sec=${2 * 60}

    ${iperf_port}=  Evaluate  random.randint(40000, 65000)
    Step   3  ssh execute
    ...  console=${diagos_mode}
    ...  username=${scp_username}
    ...  password=${scp_password}
    ...  server_ip=${ssh_server_ipv4}
    ...  command="iperf -s -p ${iperf_port} -i 1 -m -P 2 -D"
    ...  sec=${2 * 60}
    search for a pattern
    ...  text=${text}
    ...  pattern=The Iperf daemon process ID : (?P<pid>\\d+)
    ...  msg=Failed, not found iperf daemon server!
    set test variable  ${iperf_server_pid}  ${match}[pid]

    ${date_start}=  Get Time
    Step   4  execute command and verify with unexpected patterns
    ...  console=${diagos_mode}
    ...  command=(timeout --preserve-status --kill-after=${stress_tc006_total_test_time_sec + 70} ${stress_tc006_total_test_time_sec + 60} iperf -c ${ssh_server_ipv4} -p ${iperf_port} -i 1 -t ${stress_tc006_total_test_time_sec} -P 2 -d)
    ...  patterns=${iperf_unexpected_patterns}
    ...  sec=${stress_tc006_total_test_time_sec + 60}
    ...  msg=Failed for iperf test!${\n}The iperf server is may not running!

    Step   5  ssh execute
    ...  console=${diagos_mode}
    ...  username=${scp_username}
    ...  password=${scp_password}
    ...  server_ip=${ssh_server_ipv4}
    ...  command="kill -9 ${iperf_server_pid}"
    ...  sec=${2 * 60}

    ${date_stop}=  Get Time
    ${total_test_time}=  Subtract Date From Date
    ...  ${date_stop}  ${date_start}
    ...  result_format=timer
    ...  exclude_millis=${TRUE}
    ${total_test_time_sec}=  Convert Time
    ...  ${total_test_time}
    ...  result_format=number

    Log  >>Total test time is ${total_test_time} (HH:MM:SS)<<  console=${TRUE}


# The 'stress_tc007_total_test_time_sec' can also mean the number of ping network times, not just the time(timeout).
ALI_STRESS_TC007_CPU_BMC_PING_STRESS_VIA_VLAN4088
    [Timeout]  ${stress_tc007_total_test_time_sec + 900} seconds
    [Tags]  ALI_STRESS_TC007_CPU_BMC_PING_STRESS_VIA_VLAN4088
    ...  migaloo
    [Setup]  open prompt and login to root user  console=${diagos_mode}

    Step  1  execute command  bmc-exec "rm -f tc_007bmc.log"
    step  2  execute command  rm -f tc_007cpu.log

    # BMC OS ping CPU OS via eth0.4088
    Log  >>BMC OS ping CPU OS via eth0.4088, total times: ${stress_tc007_total_test_time_sec} <<  console=${TRUE}
    Step  3  execute command and verify exit code
        ...  console=${diagos_mode}
        ...  command=bmc-exec "ping -c ${stress_tc007_total_test_time_sec} 240.1.1.2 >> tc_007bmc.log" &
        ...  sec=${stress_tc007_total_test_time_sec + 5 * 60}

    # CPU OS ping BMC OS via eth0.4088
    Log  >>CPU OS ping BMC OS via eth0.4088, total times: ${stress_tc007_total_test_time_sec} <<  console=${TRUE}
    Step  4  execute command and verify with a pattern
        ...  console=${diagos_mode}
        ...  path=/home/admin/
        ...  command=ping -c ${stress_tc007_total_test_time_sec} 240.1.1.1 2>&1 | tee -a tc_007cpu.log
        ...  pattern=min/avg/max
        ...  msg=Can not found the pattern!
        ...  sec=${stress_tc007_total_test_time_sec + 5 * 60}
    BuiltIn.Sleep  5 seconds
    Step  5  check_network_ping_log  ${stress_tc007_total_test_time_sec}  tc_007bmc.log  bmc_side
    Step  6  check_network_ping_log  ${stress_tc007_total_test_time_sec}  tc_007cpu.log  cpu_side


# The 'stress_tc008_total_test_time_sec' can also mean the number of ping network times, not just the time(timeout).
ALI_STRESS_TC008_CPU_PING_BMC_AND_BMC_PING_CPU_STRESS
    [Timeout]  ${stress_tc008_total_test_time_sec + 900} seconds
    [Tags]  ALI_STRESS_TC008_CPU_PING_BMC_AND_BMC_PING_CPU_STRESS
    ...  migaloo
    [Setup]  Run Keywords  open prompt and login to root user  console=${diagos_mode}
    ...  AND  OpenBMC renew IP using DHCP and set variable
    ...  AND  DiagOS renew IP using DHCP and set variable
    ${cpu_ip}  get_ip_addr  ip addr show eth0 |grep -E "inet.*scope global eth0" |awk -F "[ /]+" '{print $3}'
    ${bmc_ip}  get_ip_addr  bmc-exec ip addr show eth0 |grep -E "inet.*scope global eth0" |awk -F "[ /]+" '{print $3}'
    Step  1  execute command  bmc-exec "rm -f tc_008bmc.log"
    step  2  execute command  rm -f tc_008cpu.log

    # BMC OS ping CPU OS via eth0
    Log  >>BMC OS ping CPU OS via eth0, total times: ${stress_tc008_total_test_time_sec} <<  console=${TRUE}
    Step  3  execute command and verify exit code
        ...  console=${diagos_mode}
        ...  command=bmc-exec "ping -c ${stress_tc008_total_test_time_sec} ${cpu_ip} >> tc_008bmc.log" &
        ...  sec=${stress_tc008_total_test_time_sec + 5 * 60}

    # CPU OS ping BMC OS via eth0
    Log  >>CPU OS ping BMC OS via eth0, total times: ${stress_tc008_total_test_time_sec} <<  console=${TRUE}
    Step  4  execute command and verify with a pattern
        ...  console=${diagos_mode}
        ...  path=/home/admin/
        ...  command=ping -c ${stress_tc008_total_test_time_sec} ${bmc_ip} 2>&1 | tee -a tc_008cpu.log
        ...  pattern=min/avg/max
        ...  msg=Can not found the pattern!
        ...  sec=${stress_tc008_total_test_time_sec + 5 * 60}
    BuiltIn.Sleep  5 seconds
    Step  5  check_network_ping_log  ${stress_tc008_total_test_time_sec}  tc_008bmc.log  bmc_side
    Step  6  check_network_ping_log  ${stress_tc008_total_test_time_sec}  tc_008cpu.log  cpu_side


# The 'stress_tc009_total_test_time_sec' can also mean the number of ping network times, not just the time(timeout).
ALI_STRESS_TC009_CPU_PING_REMOTE_PC_STRESS
    [Timeout]  ${stress_tc009_total_test_time_sec + 900} seconds
    [Tags]  ALI_STRESS_TC009_CPU_PING_REMOTE_PC_STRESS
    ...  migaloo
    [Setup]  DiagOS renew IP using DHCP and set variable
    Step  1  execute command  rm -f /home/admin/tc_009cpu.log
    Step  2  execute command and verify with a pattern
        ...  console=${diagos_mode}
        ...  path=/home/admin/
        ...  command=ping -c ${stress_tc009_total_test_time_sec} ${ssh_server_ipv4} 2>&1 | tee -a tc_009cpu.log
        ...  pattern=min/avg/max
        ...  msg=Can not found the pattern!
        ...  sec=${stress_tc009_total_test_time_sec + 5 * 60}
    Step  3  check_network_ping_log  ${stress_tc009_total_test_time_sec}  tc_009cpu.log  cpu_side


ALI_STRESS_TC010_SYSTEM_IDLE_STRESS_TEST
    [Timeout]  ${stress_tc010_total_test_time_sec + 5 * 60} seconds
    [Tags]  ALI_STRESS_TC010_SYSTEM_IDLE_STRESS_TEST
    ...  migaloo

    [Setup]  open prompt and login to root user  console=${diagos_mode}

    ${date_start}=  Get Time
    FOR  ${loop}  IN RANGE  1  ${times_10000000}+1  1
        # Not read the first prompt
        Run Keyword And Ignore Error
        ...  read until regexp
        ...  patterns=.*@.*\\:.*(?:\\$|#)
        ...  timeout=10

        ${status}  ${text}=  Run Keyword And Ignore Error
        ...  read until regexp
        ...  patterns=.*@.*\\:.*(?:\\$|#)
        ...  timeout=${stress_tc010_total_test_time_sec}
        Log  ${text}

        ${status}  ${value}=  Run Keyword And Ignore Error
        ...  search for one of patterns
        ...  text=${text}
        ...  patterns=${idle_system_log_unexpected_patterns}
        ...  msg=Failed, should not found unexpected_patterns!
        Run Keyword If  '${status}' == 'PASS'
        ...  Fail  Failed, should not found unexpected_patterns!${\n * 2}${idle_system_log_unexpected_patterns}

        ${date_stop}=  Get Time
        ${total_test_time}=  Subtract Date From Date
        ...  ${date_stop}  ${date_start}
        ...  result_format=timer
        ...  exclude_millis=${TRUE}
        ${total_test_time_sec}=  Convert Time
        ...  ${total_test_time}
        ...  result_format=number

        ${status}=  Evaluate  ${total_test_time_sec} >= ${stress_tc010_total_test_time_sec}
        Run Keyword If  '${status}' == '${TRUE}'  Exit For Loop
    END

    Log  >>Total test time is ${total_test_time} (HH:MM:SS)<<  console=${TRUE}


ALI_STRESS_TC011_CPU_I2C_SCAN_STRESS_TEST
    [Timeout]  ${times_1000 * 120 + 900} seconds
    [Tags]  ALI_STRESS_TC011_CPU_I2C_SCAN_STRESS_TEST
    ...  migaloo

    ${date_start}=  Get Time
    FOR  ${loop}  IN RANGE  1  ${times_1000}  1
        Log  >>Loop number #${loop}<<  console=${TRUE}

        execute command and verify with a pattern
        ...  console=${diagos_mode}
        ...  path=${diagos_cpu_diag_path}
        ...  command=${diag_i2c_test_cmd}
        ...  pattern=${diag_i2c_test_pattern}
        ...  msg=Failed, not found the pass message!
        ...  sec=${90}
    END


ALI_STRESS_TC012_CPU_LPC_RW_STRESS_TEST
    [Timeout]  ${times_500 * 60 + 5 * 60} seconds
    [Tags]  ALI_STRESS_TC012_CPU_LPC_RW_STRESS_TEST
    ...  migaloo

    [Setup]  open prompt and login to root user  console=${diagos_mode}
    Step  1  cpu_lpc_stress  ${platform}  ${diag_utility_path}  ${times_500}


ALI_STRESS_TC013_OPENBMC_I2C_STRESS_TEST
    [Timeout]  ${times_500 * 90 + 5 * 60} seconds
    [Tags]  ALI_STRESS_TC013_OPENBMC_I2C_STRESS_TEST
    ...  migaloo

    FOR  ${loop}  IN RANGE  1  ${times_500}  1
        Log  >>Loop number #${loop}<<  console=${TRUE}

        execute command and verify with a pattern
        ...  console=${openbmc_mode}
        ...  path=${openbmc_diag_path}
        ...  command=./cel-i2c-test -s
        ...  pattern=All the I2C devices test.*?\[ PASS \]
        ...  msg=Failed, not found the pass message!
        ...  sec=${90}
    END


ALI_STRESS_TC014_OPTICAL_LOOPBACK_EEPROM_ACCESS_STRESS
    [Timeout]  ${stress_tc014_total_test_time_sec + 5 * 60} seconds
    [Tags]  ALI_STRESS_TC014_OPTICAL_LOOPBACK_EEPROM_ACCESS_STRESS
    ...  migaloo
    [Setup]  Run Keywords
    ...  open prompt and login to root user  console=${diagos_mode}
    ...  AND  DiagOS renew IP using DHCP and set variable

    Step   1  secure copy file
    ...  console=${diagos_mode}
    ...  username=${scp_username}
    ...  password=${scp_password}
    ...  source_ip=${ssh_server_ipv4}
    ...  source_path=${tftp_root_path}/migaloo/image/STRESS/STRESS/TS-Migaloo-14
    ...  source_file=*
    ...  destination=/tmp/STRESS
    ...  sec=${2 * 60}
    Step  2  execute command and verify exit code
        ...  console=${diagos_mode}
        ...  path=/tmp/STRESS/
        ...  command=./run_10_processes.sh
        ...  sec=${3 * 60}
    BuiltIn.Sleep  ${stress_tc014_total_test_time_sec}
    Step  3  execute command and verify exit code
        ...  console=${diagos_mode}
        ...  path=/tmp/STRESS/
        ...  command=killall -9 Port_device_present_stress*
        ...  sec=${3 * 60}
    Step  4  execute command and verify exit code
        ...  console=${diagos_mode}
        ...  command=cat EEPROM_access_log_* |grep -iE "ff ff|not detected"
        ...  sec=${6 * 60}
        ...  is_check_exit_code=${FALSE}
    Step  5  execute command  rm -f /tmp/STRESS/*


ALI_STRESS_TC015_EMMC_RW_STRESS_TEST
    [Timeout]  ${stress_tc015_total_test_time_sec + 5 * 60} seconds
    [Tags]  ALI_STRESS_TC015_EMMC_RW_STRESS_TEST
    ...  migaloo

    ${date_start}=  Get Time
    FOR  ${loop}  IN RANGE  1  ${times_10000000}  1
        Log  >>Loop number #${loop}<<  console=${TRUE}

        execute command and verify exit code
        ...  console=${openbmc_mode}
        ...  command=dd if=/dev/zero of=/mnt/data/test bs=50M count=1 && sync && rm -f /mnt/data/test
        ...  sec=${3 * 60}

        ${date_stop}=  Get Time
        ${total_test_time}=  Subtract Date From Date
        ...  ${date_stop}  ${date_start}
        ...  result_format=timer
        ...  exclude_millis=${TRUE}
        ${total_test_time_sec}=  Convert Time
        ...  ${total_test_time}
        ...  result_format=number

        ${status}=  Evaluate  ${total_test_time_sec} >= ${stress_tc015_total_test_time_sec}
        Exit For Loop If  '${status}' == '${TRUE}'
    END

    Log  >>Total test time is ${total_test_time} (HH:MM:SS)<<  console=${TRUE}

    [Teardown]  execute command and verify exit code
        ...  console=${openbmc_mode}
        ...  command=rm -f /mnt/data/test && sync
        ...  sec=${3 * 60}
        ...  is_check_exit_code=${FALSE}


ALI_STRESS_TC016_BMC_DDR_RW_STRESS_TEST
    [Timeout]  ${times_20 * 180 * 60 + 300} seconds
    [Tags]  ALI_STRESS_TC016_BMC_DDR_RW_STRESS_TEST
    ...  migaloo
    [Setup]  open prompt and login to root user  console=${openbmc_mode}
    Step  1  bmc_ddr_stress_test  ${bmc_ddr_result_pattern}  2


ALI_STRESS_TC017_MDIO_STRESS_TEST
    [Timeout]  ${times_500 * 10 + 3 * 60} seconds
    [Tags]  ALI_STRESS_TC017_MDIO_STRESS_TEST
    ...  migaloo

    [Setup]  open prompt and login to root user  console=${openbmc_mode}

    ${date_start}=  Get Time
    FOR  ${loop}  IN RANGE  1  ${times_500}+1  1
        Log  >>Loop number #${loop}<<  console=${TRUE}

        execute command and verify with ordered pattern list
        ...  console=${openbmc_mode}
        ...  path=${openbmc_diag_bin_path}
        ...  command=${openbmc_mido_test}
        ...  patterns=${openbmc_mdio_test_patterns}
        ...  sec=${3 * 60}
    END


ALI_STRESS_TC018_WARM_REBOOT_STRESS
    [Timeout]  ${times_500 * 5 * 60 + 600} seconds
    [Tags]  ALI_STRESS_TC018_WARM_REBOOT_STRESS
    ...  migaloo
    [Setup]  open prompt and login to root user  console=${diagos_mode}
    FOR  ${loop}  IN RANGE  1  ${times_500}+1  1
        Step  1  cpu_reset_check_info  ${platform}  ${diag_i2c_test_pattern}  ${cpld_test_pattern}  ${lspci_list_count}
        Step  2  reboot to diag os
    END


ALI_STRESS_TC019_AC_POWER_CYCLING_STRESS
    [Timeout]  ${times_500 * 900 + 600} seconds
    [Tags]  ALI_STRESS_TC019_AC_POWER_CYCLING_STRESS
    ...  migaloo
    [Setup]  open prompt and login to root user  console=${diagos_mode}
    FOR  ${loop}  IN RANGE  1  ${times_500}+1  1
        Step  1  check_bmc_restful
        Step  2  cpu_reset_check_info  ${platform}  ${diag_i2c_test_pattern}  ${cpld_test_pattern}  ${lspci_list_count}
        Step  3  power cycle to mode  mode=${diagos_mode}
    END


ALI_STRESS_TC020_OPENBMC_RESET_COME_STRESS_TEST
    [Timeout]  ${times_500 * 420 + 300} seconds
    [Tags]  ALI_STRESS_TC020_OPENBMC_RESET_COME_STRESS_TEST
    ...  migaloo
    [Setup]  open prompt and login to root user  console=${diagos_mode}
    FOR  ${loop}  IN RANGE  1  ${times_500}+1  1
        Step  1  cpu_reset_check_info  ${platform}  ${diag_i2c_test_pattern}  ${cpld_test_pattern}  ${lspci_list_count}
        Step  2  power cycle sonic  mode=${diagos_mode}
    END


ALI_STRESS_TC021_COME_POWER_ON_OFF_STRESS_TEST
    [Timeout]  ${times_500 * 420 + 300} seconds
    [Tags]  ALI_STRESS_TC021_COME_POWER_ON_OFF_STRESS_TEST
    ...  migaloo
    [Setup]  open prompt and login to root user  console=${diagos_mode}
    FOR  ${loop}  IN RANGE  1  ${times_500}+1  1
        Step  1  cpu_reset_check_info  ${platform}  ${diag_i2c_test_pattern}  ${cpld_test_pattern}  ${lspci_list_count}
        Step  2  power off on sonic  mode=${diagos_mode}
    END


# ALI_STRESS_TC022_POWER_CYCLE_STRESS_TEST  ## Covered by ALI_STRESS_TC020_OPENBMC_RESET_COME_STRESS_TEST


ALI_STRESS_TC023_OPENBMC_RESET_STRESS_TEST
    [Timeout]  ${times_500 * 10 * 60 + 15 * 60} seconds
    [Tags]  ALI_STRESS_TC023_OPENBMC_RESET_STRESS_TEST
    ...  migaloo

    FOR  ${loop}  IN RANGE  1  ${times_500}  1
        Step  1  open prompt and login to root user  console=${openbmc_mode}
        Step  2  bmc_reset_check_info  ${platform}
        Step  3  reboot UNIX-like OS  console=${openbmc_mode}
        BuiltIn.Sleep  ${2 * 60} seconds  # For terrible I2C messages
    END


ALI_STRESS_TC024_PRIMARY_BIOS_UPGRADE_DOWNGRADE_TEST
    [Timeout]  ${times_200 * 1200 + 15 * 60} seconds
    [Tags]  ALI_STRESS_TC024_PRIMARY_BIOS_UPGRADE_DOWNGRADE_TEST
    ...  migaloo

    [Setup]  Run Keywords
    ...  open prompt and login to root user  console=${openbmc_mode}
    ...  AND  OpenBMC renew IP using DHCP and set variable
    ...  AND  secure copy file
    ...  console=${openbmc_mode}
    ...  username=${scp_username}
    ...  password=${scp_password}
    ...  source_ip=${ssh_server_ipv4}
    ...  source_path=${bios_path}
    ...  source_file=${bios_old_image}
    ...  destination=${bios_save_to}
    ...  sec=${5 * 60}
    ...  AND  secure copy file
    ...  console=${openbmc_mode}
    ...  username=${scp_username}
    ...  password=${scp_password}
    ...  source_ip=${ssh_server_ipv4}
    ...  source_path=${bios_path}
    ...  source_file=${bios_new_image}
    ...  destination=${bios_save_to}
    ...  sec=${5 * 60}

    Wait for OpenBMC Info  max_wait_number=10

    FOR  ${loop}  IN RANGE  1  ${times_200}  1
        Step  1  open prompt and login to root user  console=${diagos_mode}
        Step  2  cpu_reset_check_info  ${platform}  ${diag_i2c_test_pattern}  ${cpld_test_pattern}  ${lspci_list_count}
        Step  3  bios_update_test  master  ${bios_save_to}/${bios_old_image}  is_bios_ver_new=True  upgrade=False
        power cycle sonic  mode=${diagos_mode}
        Step  4  open prompt and login to root user  console=${diagos_mode}
        Step  5  cpu_reset_check_info  ${platform}  ${diag_i2c_test_pattern}  ${cpld_test_pattern}  ${lspci_list_count}
        Step  6  bios_update_test  master  ${bios_save_to}/${bios_new_image}  is_bios_ver_new=False  upgrade=True
        power cycle sonic  mode=${diagos_mode}
    END


ALI_STRESS_TC025_BACKUP_BIOS_UPGRADE_DOWNGRADE_TEST
    [Timeout]  ${times_200 * 1200 + 15 * 60} seconds
    [Tags]  ALI_STRESS_TC025_BACKUP_BIOS_UPGRADE_DOWNGRADE_TEST
    ...  migaloo
    [Setup]  Run Keywords
    ...  open prompt and login to root user  console=${openbmc_mode}
    ...  AND  OpenBMC renew IP using DHCP and set variable
    ...  AND  secure copy file
    ...  console=${openbmc_mode}
    ...  username=${scp_username}
    ...  password=${scp_password}
    ...  source_ip=${ssh_server_ipv4}
    ...  source_path=${bios_path}
    ...  source_file=${bios_old_image}
    ...  destination=${bios_save_to}
    ...  sec=${15 * 60}
    ...  AND  secure copy file
    ...  console=${openbmc_mode}
    ...  username=${scp_username}
    ...  password=${scp_password}
    ...  source_ip=${ssh_server_ipv4}
    ...  source_path=${bios_path}
    ...  source_file=${bios_new_image}
    ...  destination=${bios_save_to}
    ...  sec=${15 * 60}

    execute command  source /usr/local/bin/openbmc-utils.sh
    execute command  come_reset slave
    BuiltIn.Sleep  180
    Wait for OpenBMC Info  max_wait_number=10

    FOR  ${loop}  IN RANGE  1  ${times_200}  1
        Step  1  open prompt and login to root user  console=${diagos_mode}
        Step  2  cpu_reset_check_info  ${platform}  ${diag_i2c_test_pattern}  ${cpld_test_pattern}  ${lspci_list_count}
        Step  3  bios_update_test  slave  ${bios_save_to}/${bios_old_image}  is_bios_ver_new=True  upgrade=False
        power cycle sonic  mode=${diagos_mode}
        execute command  curl -d '{"Flash": "slave"}' http://240.1.1.1:8080/api/firmware/biosnextboot | python -m json.tool
        execute command  curl -d '{"Entity":"cpu"}' http://240.1.1.1:8080/api/hw/powercycle| python -m json.tool
        BuiltIn.Sleep  180
        Step  4  open prompt and login to root user  console=${diagos_mode}
        Step  5  cpu_reset_check_info  ${platform}  ${diag_i2c_test_pattern}  ${cpld_test_pattern}  ${lspci_list_count}
        Step  6  bios_update_test  slave  ${bios_save_to}/${bios_new_image}  is_bios_ver_new=False  upgrade=True
        power cycle sonic  mode=${diagos_mode}
        execute command  curl -d '{"Flash": "slave"}' http://240.1.1.1:8080/api/firmware/biosnextboot | python -m json.tool
        execute command  curl -d '{"Entity":"cpu"}' http://240.1.1.1:8080/api/hw/powercycle| python -m json.tool
        BuiltIn.Sleep  180
    END


ALI_STRESS_TC026_PRIMARY_OPENBMC_UPGRADE_DOWNGRADE_TEST
    [Timeout]  ${times_200 * 40 * 60 + 15 * 60} seconds
    [Tags]  ALI_STRESS_TC026_PRIMARY_OPENBMC_UPGRADE_DOWNGRADE_TEST
    ...  migaloo
    [Setup]  Run Keywords
    ...  open prompt and login to root user  console=${openbmc_mode}
    ...  AND  OpenBMC renew IP using DHCP and set variable
    ...  AND  secure copy file
    ...  console=${openbmc_mode}
    ...  username=${scp_username}
    ...  password=${scp_password}
    ...  source_ip=${ssh_server_ipv4}
    ...  source_path=${bmc_path}
    ...  source_file=${bmc_old_image}
    ...  destination=/var/log/bmcImage/
    ...  sec=${15 * 60}
    ...  AND  secure copy file
    ...  console=${openbmc_mode}
    ...  username=${scp_username}
    ...  password=${scp_password}
    ...  source_ip=${ssh_server_ipv4}
    ...  source_path=${bmc_path}
    ...  source_file=${bmc_new_image}
    ...  destination=/var/log/bmcImage/
    ...  sec=${15 * 60}

    switch bmc flash  master

    FOR  ${loop}  IN RANGE  1  ${times_200}+1  1
        Step  1  update_bmc  /var/log/bmcImage/${bmc_old_image}  /dev/mtd5
        reboot openbmc
        Step  2  check_bmc_info  master  ${old_bmc_version}
        Step  3  update_bmc  /var/log/bmcImage/${bmc_new_image}  /dev/mtd5
        reboot openbmc
        Step  4  check_bmc_info  master  ${new_bmc_version}
    END


ALI_STRESS_TC027_BACKUP_OPENBMC_UPGRADE_DOWNGRADE_TEST
    [Timeout]  ${times_200 * 40 * 60 + 15 * 60} seconds
    [Tags]  ALI_STRESS_TC027_BACKUP_OPENBMC_UPGRADE_DOWNGRADE_TEST
    ...  migaloo

    [Setup]  Run Keywords
    ...  open prompt and login to root user  console=${openbmc_mode}
    ...  AND  OpenBMC renew IP using DHCP and set variable
    ...  AND  secure copy file
    ...  console=${openbmc_mode}
    ...  username=${scp_username}
    ...  password=${scp_password}
    ...  source_ip=${ssh_server_ipv4}
    ...  source_path=${bmc_path}
    ...  source_file=${bmc_old_image}
    ...  destination=/var/log/bmcImage/
    ...  sec=${15 * 60}
    ...  AND  secure copy file
    ...  console=${openbmc_mode}
    ...  username=${scp_username}
    ...  password=${scp_password}
    ...  source_ip=${ssh_server_ipv4}
    ...  source_path=${bmc_path}
    ...  source_file=${bmc_new_image}
    ...  destination=/var/log/bmcImage/
    ...  sec=${15 * 60}

    switch bmc flash  slave

    FOR  ${loop}  IN RANGE  1  ${times_200}+1  1
        Step  1  update_bmc  /var/log/bmcImage/${bmc_old_image}  /dev/mtd5
        reboot openbmc
        Step  2  check_bmc_info  slave  ${old_bmc_version}
        Step  3  update_bmc  /var/log/bmcImage/${bmc_new_image}  /dev/mtd5
        reboot openbmc
        Step  4  check_bmc_info  slave  ${new_bmc_version}
    END
    [Teardown]  openbmc cmd off on psu  mode=${diagos_mode}


ALI_STRESS_TC028_OPENBMC_SENSOR_READING_STRESS_TEST_UNDER_HIGH_LOADING
    [Timeout]  ${time_sec_24_60_60 + 5 * 60} seconds
    [Tags]  ALI_STRESS_TC028_OPENBMC_READING_STRESS_TEST_UNDER_HIGH_LOADING
    ...  migaloo
    [Setup]  Run Keywords
    ...  open prompt and login to root user  console=${diagos_mode}
    ...  AND  run cmd  stress --cpu 8 --vm 8 --vm-bytes 512M --vm-hang 1 --timeout 1440m &  root@sonic
    ...  AND  open prompt and login to root user  console=${openbmc_mode}
    Step  1  sensor_reading_stress  ${sensor_lines}  ${time_sec_24_60_60}
    [Teardown]  power reset sonic  mode=${diagos_mode}


ALI_STRESS_TC029_OPENBMC_SENSOR_READING_STRESS_TEST_CPU_IDLE
    [Timeout]  ${time_sec_24_60_60 + 5 * 60} seconds
    [Tags]  ALI_STRESS_TC029_OPENBMC_READING_STRESS_TEST_CPU_IDLE
    ...  migaloo
    [Setup]  open prompt and login to root user  console=${openbmc_mode}
    Step  1  sensor_reading_stress  ${sensor_lines}  ${time_sec_24_60_60}
    [Teardown]  power reset sonic  mode=${diagos_mode}

#
# This TC is not fully tested yet, may have to clarify it again!
# At this moment, there is a kernel panic on remove the kernel module.
#
# Remove ALI_STRESS_TC030_FPGA_DRIVER_UPGRADE_DOWNGRADE_STRESS_TEST


ALI_STRESS_TC031_FPGA_IAMGE_UPGRADE_DOWNGRADE_VIA_CPU
    [Timeout]  ${times_200 * 900 + 5 * 60} seconds
    [Tags]  ALI_STRESS_TC031_FPGA_IAMGE_UPGRADE_DOWNGRADE_VIA_CPU
    ...  migaloo
    [Setup]  Run Keywords
    ...  open prompt and login to root user  console=${diagos_mode}
    ...  AND  DiagOS renew IP using DHCP and set variable
    ...  AND  secure copy file
    ...  console=${diagos_mode}
    ...  username=${scp_username}
    ...  password=${scp_password}
    ...  source_ip=${ssh_server_ipv4}
    ...  source_path=${fpga_fw_path}
    ...  source_file=${fpga_old_fw_name}
    ...  destination=/home/STRESS
    ...  sec=${15 * 60}
    ...  AND  secure copy file
    ...  console=${diagos_mode}
    ...  username=${scp_username}
    ...  password=${scp_password}
    ...  source_ip=${ssh_server_ipv4}
    ...  source_path=${fpga_fw_path}
    ...  source_file=${fpga_new_fw_name}
    ...  destination=/home/STRESS
    ...  sec=${15 * 60}

    FOR  ${loop}  IN RANGE  1  ${times_200}+1  1
        Log  >>Downgrade<<  console=${TRUE}
        Step  1  fpga_update  /home/STRESS/${fpga_old_fw_name}
        Step  2  power cycle sonic  mode=${diagos_mode}
        Step  3  check fpga version  ${diagos_cpu_diag_path}  ${read_fpga_version_cmd}  ${fpga_old_fw_version}
        Log  >>Upgrade<<  console=${TRUE}
        Step  4  fpga_update  /home/STRESS/${fpga_new_fw_name}
        Step  5  power cycle sonic  mode=${diagos_mode}
        Step  6  check fpga version  ${diagos_cpu_diag_path}  ${read_fpga_version_cmd}  ${fpga_new_fw_version}
    END
    [Teardown]  execute command  rm -rf /home/STRESS

ALI_STRESS_TC032_BASE_CPLD_UPGRADE_DOWNGRADE
    [Timeout]  ${times_200 * 25 * 60 + 5 * 60} seconds
    [Tags]  ALI_STRESS_TC032_BASE_CPLD_UPGRADE_DOWNGRADE
    ...  migaloo

    [Setup]  Run Keywords
    ...  open prompt and login to root user  console=${diagos_mode}
    ...  AND  DiagOS renew IP using DHCP and set variable
    ...  AND  secure copy file
    ...  console=${diagos_mode}
    ...  username=${scp_username}
    ...  password=${scp_password}
    ...  source_ip=${ssh_server_ipv4}
    ...  source_path=${cpld_fw_path}
    ...  source_file=${basecpld_old_fw_name}
    ...  destination=/home/STRESS
    ...  sec=${15 * 60}
    ...  AND  secure copy file
    ...  console=${diagos_mode}
    ...  username=${scp_username}
    ...  password=${scp_password}
    ...  source_ip=${ssh_server_ipv4}
    ...  source_path=${cpld_fw_path}
    ...  source_file=${basecpld_new_fw_name}
    ...  destination=/home/STRESS
    ...  sec=${15 * 60}

    FOR  ${loop}  IN RANGE  1  ${times_200}+1  1
        Log  >>Downgrade<<  console=${TRUE}
        execute command and verify with a pattern
        ...  console=${diagos_mode}
        ...  command=ispvm -i 0 /home/STRESS/${basecpld_old_fw_name}
        ...  pattern=PASS!
        ...  msg=Failed to update BASE CPLD!
        ...  sec=300
        openbmc cmd off on psu  mode=${diagos_mode}
        check basecpld version  ${diagos_cpu_diag_path}  ${read_cpld_version_cmd}  version_new_or_old=old
        Log  >>Upgrade<<  console=${TRUE}
        execute command and verify with a pattern
        ...  console=${diagos_mode}
        ...  command=ispvm -i 0 /home/STRESS/${basecpld_new_fw_name}
        ...  pattern=PASS!
        ...  msg=Failed to update BASE CPLD!
        ...  sec=300
        openbmc cmd off on psu  mode=${diagos_mode}
        check basecpld version  ${diagos_cpu_diag_path}  ${read_cpld_version_cmd}  version_new_or_old=new
    END
    [Teardown]  execute command  rm -rf /home/STRESS


ALI_STRESS_TC033_CPLD_UPGRADE_DOWNLOAD_VIA_CPU
    [Timeout]  ${times_200 * 30 * 60 + 5 * 60} seconds
    [Tags]  ALI_STRESS_TC033_CPLD_UPGRADE_DOWNLOAD_VIA_CPU
    ...  migaloo

    [Setup]  Run Keywords
    ...  open prompt and login to root user  console=${diagos_mode}
    ...  AND  DiagOS renew IP using DHCP and set variable
    ...  AND  secure copy file
    ...  console=${diagos_mode}
    ...  username=${scp_username}
    ...  password=${scp_password}
    ...  source_ip=${ssh_server_ipv4}
    ...  source_path=${cpld_fw_path}
    ...  source_file=*
    ...  destination=/home/STRESS
    ...  sec=${15 * 60}

    FOR  ${loop}  IN RANGE  1  ${times_200}+1  1
        Log  >>Downgrade<<  console=${TRUE}
        execute command and verify with a pattern
        ...  console=${diagos_mode}
        ...  command=ispvm -i 0 /home/STRESS/${basecpld_old_fw_name}
        ...  pattern=PASS!
        ...  msg=Failed to update BASE CPLD!
        ...  sec=300
        execute command and verify with a pattern
        ...  console=${diagos_mode}
        ...  command=ispvm -i 1 /home/STRESS/${cpu_cpld_old_fw_name}
        ...  pattern=PASS!
        ...  msg=Failed to update CPU CPLD!
        ...  sec=300
        execute command and verify with a pattern
        ...  console=${diagos_mode}
        ...  command=ispvm -i 2 /home/STRESS/${fan_cpld_old_fw_name}
        ...  pattern=PASS!
        ...  msg=Failed to update FAN CPLD!
        ...  sec=300
        execute command and verify with a pattern
        ...  console=${diagos_mode}
        ...  command=ispvm -i 3 /home/STRESS/${switch_cpld_old_fw_name}
        ...  pattern=PASS!
        ...  msg=Failed to update SWITCH CPLD!
        ...  sec=300
        Run Keyword If  '${platform}' == 'migaloo'
        ...  Run Keywords
        ...  execute command and verify with a pattern
        ...  console=${diagos_mode}
        ...  command=ispvm -i 4 /home/STRESS/${switch_cpld_old_fw_name}
        ...  pattern=PASS!
        ...  msg=Failed to update TOP Line Card CPLD!
        ...  sec=300
        ...  AND  execute command and verify with a pattern
        ...  console=${diagos_mode}
        ...  command=ispvm -i 5 /home/STRESS/${switch_cpld_old_fw_name}
        ...  pattern=PASS!
        ...  msg=Failed to update BOT Line Card CPLD!
        ...  sec=300
        openbmc cmd off on psu  mode=${diagos_mode}
        check_bmc_restful
        check all cpld version  ${platform}  version_new_or_old=old

        Log  >>Downgrade<<  console=${TRUE}
        execute command and verify with a pattern
        ...  console=${diagos_mode}
        ...  command=ispvm -i 0 /home/STRESS/${basecpld_new_fw_name}
        ...  pattern=PASS!
        ...  msg=Failed to update BASE CPLD!
        ...  sec=300
        execute command and verify with a pattern
        ...  console=${diagos_mode}
        ...  command=ispvm -i 1 /home/STRESS/${cpu_cpld_new_fw_name}
        ...  pattern=PASS!
        ...  msg=Failed to update CPU CPLD!
        ...  sec=300
        execute command and verify with a pattern
        ...  console=${diagos_mode}
        ...  command=ispvm -i 2 /home/STRESS/${fan_cpld_new_fw_name}
        ...  pattern=PASS!
        ...  msg=Failed to update FAN CPLD!
        ...  sec=300
        execute command and verify with a pattern
        ...  console=${diagos_mode}
        ...  command=ispvm -i 3 /home/STRESS/${switch_cpld_new_fw_name}
        ...  pattern=PASS!
        ...  msg=Failed to update SWITCH CPLD!
        ...  sec=300
        Run Keyword If  '${platform}' == 'migaloo'
        ...  Run Keywords
        ...  execute command and verify with a pattern
        ...  console=${diagos_mode}
        ...  command=ispvm -i 4 /home/STRESS/${switch_cpld_new_fw_name}
        ...  pattern=PASS!
        ...  msg=Failed to update TOP Line Card CPLD!
        ...  sec=300
        ...  AND  execute command and verify with a pattern
        ...  console=${diagos_mode}
        ...  command=ispvm -i 5 /home/STRESS/${switch_cpld_new_fw_name}
        ...  pattern=PASS!
        ...  msg=Failed to update BOT Line Card CPLD!
        ...  sec=300
        openbmc cmd off on psu  mode=${diagos_mode}
        check_bmc_restful
        check all cpld version  ${platform}  version_new_or_old=new
    END
    [Teardown]  execute command  rm -rf /home/STRESS

#
# Remove ALI_STRESS_TC034_FPGA_IMAGE_BASE_CPLD


ALI_STRESS_TC035_CHECK_CPU_FREQUENCY_UNDER_FULL_LOADING
    [Timeout]  ${stress_tc035_total_test_time_sec + 15 * 60} seconds
    [Tags]  ALI_STRESS_TC035_CHECK_CPU_FREQUENCY_UNDER_FULL_LOADING
    ...  migaloo

    [Setup]  open prompt and login to root user  console=${diagos_mode}

    Step   1  remove file/folder
    ...  console=${diagos_mode}
    ...  file=/tmp/STRESS
    Step   2  secure copy file
    ...  console=${diagos_mode}
    ...  username=${scp_username}
    ...  password=${scp_password}
    ...  source_ip=${ssh_server_ipv4}
    ...  source_path=${tftp_root_path}/migaloo/image/STRESS
    ...  source_file=${stress_script_tarball_file}
    ...  destination=/tmp/STRESS
    ...  sec=${15 * 60}
    Step   3  decompress tar file
    ...  console=${diagos_mode}
    ...  path=/tmp/STRESS
    ...  file=${stress_script_tarball_file}
    ...  extract_only=STRESS/TS-Migaloo-35
    Step   4  execute command and verify exit code
    ...  console=${diagos_mode}
    ...  command=cd "$(dirname "$(find /tmp/STRESS/STRESS/TS-Migaloo-35 -type f -name "*BroadwellPTU*" )")"
    ...  msg=Failed, not enter to the folder!
    Step   5  execute command and verify exit code
    ...  console=${diagos_mode}
    ...  command=(chmod +x `ls -1 | grep -E "[^README]"`)
    ...  msg=Failed to apply execute permission!
    Step   6  send a line
    ...  command=timeout --preserve-status --kill-after=${stress_tc035_total_test_time_sec + 60} ${stress_tc035_total_test_time_sec} bash -c "(echo y | ./BroadwellPTU_Rev2.0 -P100)" &

    ${date_start}=  Get Time
    FOR  ${loop}  IN RANGE  1  ${times_10000000}+1  1
        Log  >>Run into loop #${loop}<<  console=${TRUE}
        execute command and verify with a pattern
        ...  console=${diagos_mode}
        ...  command=echo y |./BroadwellPwrMon
        ...  pattern=[ \\t]*CPU Brand String.*(?P<cpu_freq>\\d+\\.\\d+[ \\t]*GHz)$
        ...  msg=Failed to monitor CPU Frequency string!
        ...  is_check_exit_code=${FALSE}

        ${date_stop}=  Get Time
        ${total_test_time}=  Subtract Date From Date
        ...  ${date_stop}  ${date_start}
        ...  result_format=timer
        ...  exclude_millis=${TRUE}
        ${total_test_time_sec}=  Convert Time
        ...  ${total_test_time}
        ...  result_format=number

        ${status}=  Evaluate  ${total_test_time_sec} >= ${stress_tc035_total_test_time_sec}
        Run Keyword If  '${status}' == '${TRUE}'  Exit For Loop
    END

    Log  >>Total test time is ${total_test_time} (HH:MM:SS)<<  console=${TRUE}

#    [Teardown]  Run Keywords
#    ...  execute command and verify exit code
#    ...  console=${diagos_mode}
#    ...  command=killall -9 BroadwellPTU_Rev2.0
#    ...  exit_code_pattern=(?m)^(?P<exit_code>\\d+)$
#    ...  AND  remove file/folder
#    ...  console=${diagos_mode}
#    ...  file=/tmp/STRESS


ALI_STRESS_TC036_PSU_REDUNDANT_STRESS_TEST
    [Timeout]  ${stress_tc036_total_test_time_sec + 10 * 60} seconds
    [Tags]  ALI_STRESS_TC036_PSU_REDUNDANT_STRESS_TEST
    ...  migaloo

    ${date_start}=  Get Time
    FOR  ${loop}  IN RANGE  1  ${times_100000000}+1  1
        Run Keyword And Ignore Error
        ...  change kernel log level  console=${openbmc_mode}  level=3
        Sleep  45s  # Wait for some terrible I2C bus add messages

        open prompt and login to root user  console=${openbmc_mode}

        execute command and verify exit code
        ...  console=${openbmc_mode}
        ...  command=i2cget -y -f 0 0x0d 0x60
        ...  sec=${5 * 60}

        execute command and verify exit code
        ...  console=${openbmc_mode}
        ...  command=i2cget -y -f 0 0x0d 0x7f
        ...  sec=${5 * 60}

        execute command and verify exit code
        ...  console=${openbmc_mode}
        ...  command=sensors dps1100-i2c-24-5b dps1100-i2c-25-5b dps1100-i2c-26-5b dps1100-i2c-27-5b
        ...  sec=${15 * 60}

        execute command and verify exit code
        ...  console=${openbmc_mode}
        ...  command=./cel-psu-test -s
        ...  path=${openbmc_diag_bin_path}
        ...  sec=${15 * 60}

        powerCycleToOpenbmc

        ${date_stop}=  Get Time
        ${total_test_time}=  Subtract Date From Date
        ...  ${date_stop}  ${date_start}
        ...  result_format=timer
        ...  exclude_millis=${TRUE}
        ${total_test_time_sec}=  Convert Time
        ...  ${total_test_time}
        ...  result_format=number

        ${status}=  Evaluate  ${total_test_time_sec} >= ${stress_tc036_total_test_time_sec}
        Run Keyword If  '${status}' == '${TRUE}'  Exit For Loop
    END

    Log  >>Total test time is ${total_test_time} (HH:MM:SS)<<  console=${TRUE}


ALI_STRESS_TC038_SWITCH_CPU_BMC_TEST
    [Timeout]  ${stress_tc038_total_test_times * 30 + 5 * 60} seconds
    [Tags]  ALI_STRESS_TC038_SWITCH_CPU_BMC_TEST
    ...  migaloo

    ${date_start}=  Get Time
    FOR  ${loop}  IN RANGE  1  ${stress_tc038_total_test_times + 1}  1
        Log  >>Run into the loop #${loop}<<

        OpenBMC switch to SONiC console
        execute command and verify exit code
        ...  console=${diagos_mode}
        ...  command=cat /etc/issue
        ...  msg=Failed, is not on the DiagOS or terminal is not readly!

        OpenBMC switch from SONiC console back to OpenBMC console
        execute command and verify exit code
        ...  console=${openbmc_mode}
        ...  command=cat /etc/issue
        ...  msg=Failed, is not on the OpenBMC or terminal is not readly!
    END

    ${date_stop}=  Get Time
    ${total_test_time}=  Subtract Date From Date
    ...  ${date_stop}  ${date_start}
    ...  result_format=timer
    ...  exclude_millis=${TRUE}

    Log  >>Total test time is ${total_test_time} (HH:MM:SS)<<  console=${TRUE}


ALI_STRESS_TC039_BMC_PING_REMOTE_PC_STRESS
    [Timeout]  ${stress_tc039_total_test_time_sec + 5 * 60} seconds
    [Tags]  ALI_STRESS_TC039_BMC_PING_REMOTE_PC_STRESS
    ...  migaloo

    [Setup]  Run Keywords
    ...  open prompt and login to root user  console=${openbmc_mode}
    ...  AND  OpenBMC renew IP using DHCP and set variable

    Step  1  execute command and verify with a pattern
        ...  console=${openbmc_mode}
        ...  path=/
        ...  command=ping -c ${stress_tc039_total_test_time_sec} ${ssh_server_ipv4} 2>&1 | tee -a tc_039bmc.log
        ...  pattern=min/avg/max
        ...  msg=Can not found the pattern!
        ...  sec=${stress_tc039_total_test_time_sec + 5 * 60}
    Step  2  check_network_ping_log  ${stress_tc039_total_test_time_sec}  tc_039bmc.log


ALI_STRESS_TC040_COME_REBOOT_BMC_STRESS_TEST
    [Timeout]  ${stress_tc040_total_test_time_sec + 30 * 60} seconds
    [Tags]  ALI_STRESS_TC040_COME_REBOOT_BMC_STRESS_TEST
    ...  migaloo

    execute command and verify exit code
        ...  console=${diagos_mode}
        ...  command=bmc-exec "echo > /var/log/powermon.log" |grep -i failed
        ...  sec=${60}
        ...  is_check_exit_code=${FALSE}
    ${date_start}=  Get Time
    FOR  ${loop}  IN RANGE  1  ${stress_tc040_total_test_times + 1}  1
        open prompt and login to root user  console=${diagos_mode}
        Run Keyword And Ignore Error  change kernel log level  console=${diagos_mode}  level=3
        Sleep  45s  # Wait for some terrible I2C bus add messages
        Wait for OpenBMC Info

        execute command and verify with a pattern
        ...  console=${diagos_mode}
        ...  command=(curl -g http://240.1.1.1:8080/api/misc/biosbootstatus | python -m json.tool)
        ...  pattern=status.*(?P<status>OK)
        ...  sec=${3 * 60}

        execute command and verify with a pattern
        ...  console=${diagos_mode}
        ...  command=(curl -g http://240.1.1.1:8080/api/psu/info | python -m json.tool)
        ...  pattern=status.*(?P<status>OK)
        ...  sec=${3 * 60}

        execute command and verify with a pattern
        ...  console=${diagos_mode}
        ...  command=(curl -g http://240.1.1.1:8080/api/fan/info | python -m json.tool)
        ...  pattern=status.*(?P<status>OK)
        ...  sec=${3 * 60}

        execute command and verify with a pattern
        ...  console=${diagos_mode}
        ...  command=(curl -g http://240.1.1.1:8080/api/sensor/info | python -m json.tool)
        ...  pattern=status.*(?P<status>OK)
        ...  sec=${3 * 60}

        execute command and verify with a pattern
        ...  console=${diagos_mode}
        ...  command=(curl -d '{"Command": "cd /var/log/BMC_Diag/bin/;./cel-i2c-test -s"}' http://240.1.1.1:8080/api/hw/rawcmd | python -m json.tool)
        ...  pattern=\[\s*PASS\s*\]
        ...  sec=${3 * 60}

        execute command and verify exit code
        ...  console=${diagos_mode}
        ...  command=bmc-exec "cat /var/log/powermon.log" | grep -i "yellow"
        ...  sec=${60}
        ...  is_check_exit_code=${FALSE}

        Run Keyword And Ignore Error
        ...  execute command and verify exit code
        ...  console=${diagos_mode}
        ...  command=(curl -d '{}' http://240.1.1.1:8080/api/bmc/reboot | python -m json.tool)
        ...  sec=${3 * 60}
        OpenBMC switch from SONiC console back to OpenBMC console
        Run Keyword And Ignore Error
        ...  change kernel log level  console=${openbmc_mode}  level=3
        Sleep  45s  # Wait for some terrible I2C bus add messages
    END

    ${date_stop}=  Get Time
    ${total_test_time}=  Subtract Date From Date
    ...  ${date_stop}  ${date_start}
    ...  result_format=timer
    ...  exclude_millis=${TRUE}

    Log  >>Total test time is ${total_test_time} (HH:MM:SS)<<  console=${TRUE}


#
# The time of writing for each item was took from ALI_DIAG_TC007_CPLD_UPDATE_VIA_COME,
# multiply by 2 to make sure for the REST API.
#
ALI_STRESS_TC041_CPLD_UPGRADE_DOWNGRADE_VIA_BMC
    [Timeout]  ${times_100 * 150 * 60 + 30 * 60} seconds
    [Tags]  ALI_STRESS_TC041_CPLD_UPGRADE_DOWNGRADE_VIA_BMC
    ...  migaloo

    [Setup]  Run Keywords
    ...  open prompt and login to root user  console=${openbmc_mode}
    ...  AND  OpenBMC renew IP using DHCP and set variable
    ...  AND  secure copy file
    ...  console=${openbmc_mode}
    ...  username=${scp_username}
    ...  password=${scp_password}
    ...  source_ip=${ssh_server_ipv4}
    ...  source_path=${cpld_fw_path}
    ...  source_file=*
    ...  destination=/var/log/STRESS
    ...  sec=${15 * 60}
    FOR  ${loop}  IN RANGE  1  ${times_100}  1
        Step  1  update_cpld_in_openbmc  ${program_old_cpld}  ${refresh_cpld_cmd}
        BuiltIn.Sleep  60 seconds
        open prompt and login to root user  console=${diagos_mode}
        Step  2  check_bmc_restful
        Step  3  check all cpld version  ${platform}  version_new_or_old=old
        open prompt and login to root user  console=${openbmc_mode}
        Step  4  update_cpld_in_openbmc  ${program_new_cpld}  ${refresh_cpld_cmd}
        BuiltIn.Sleep  60 seconds
        open prompt and login to root user  console=${diagos_mode}
        Step  5  check_bmc_restful
        Step  6  check all cpld version  ${platform}  version_new_or_old=new
        open prompt and login to root user  console=${openbmc_mode}
    END
    [TearDown]  execute command  rm -rf /var/log/STRESS

ALI_STRESS_TC042_FPGA_IMAGE_UPGRADE_DOWNGRADE_VIA_BMC
    [Timeout]  ${times_100 * 20 * 60 + 15 * 60} seconds
    [Tags]  ALI_STRESS_TC042_FPGA_IMAGE_UPGRADE_DOWNGRADE_VIA_BMC
    ...  migaloo
    [Setup]  Run Keywords
    ...  open prompt and login to root user  console=${openbmc_mode}
    ...  AND  OpenBMC renew IP using DHCP and set variable
    ...  AND  secure copy file
    ...  console=${openbmc_mode}
    ...  username=${scp_username}
    ...  password=${scp_password}
    ...  source_ip=${ssh_server_ipv4}
    ...  source_path=${fpga_fw_path}
    ...  source_file=*
    ...  destination=/var/log/STRESS
    ...  sec=${15 * 60}

    FOR  ${loop}  IN RANGE  1  ${times_100}  1
        Step  1  update_fpga_in_openbmc  ${program_old_fpga}
        Step  2  openbmc cmd off on psu  mode=${diagos_mode}
        Step  3  check fpga version  ${diagos_cpu_diag_path}  ${read_fpga_version_cmd}  ${fpga_old_fw_version}
        open prompt and login to root user  console=${openbmc_mode}
        Step  4  update_fpga_in_openbmc  ${program_new_fpga}
        Step  5  openbmc cmd off on psu  mode=${diagos_mode}
        Step  6  check fpga version  ${diagos_cpu_diag_path}  ${read_fpga_version_cmd}  ${fpga_new_fw_version}
        open prompt and login to root user  console=${openbmc_mode}
    END
    [TearDown]  execute command  rm -rf /var/log/STRESS

ALI_STRESS_TC043_FRU_EEPROM_READ_STRESS
    [Timeout]  ${times_500 * 60 + 5 * 60} seconds
    [Tags]  ALI_STRESS_TC043_FRU_EEPROM_READ_STRESS
    ...  migaloo
    open prompt and login to root user  console=${openbmc_mode}
    Step  1  fru_info_reading_stress  ${platform}  ${times_500}
