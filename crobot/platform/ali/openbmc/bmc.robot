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
Documentation       Tests to verify OpenBMC functions described in the OpenBMC function SPEC for the project migaloo.

Force Tags        openbmc
Library           AliOpenBmcLib.py
Library           AliCommonLib.py
Library           CommonLib.py

Resource          CommonKeywords.resource
Resource          AliCommonKeywords.resource
Resource          AliOpenBmcKeywords.resource

Suite Setup       Bmc Connect Device
Suite Teardown    Bmc Disconnect Device

*** Variables ***
${MAX_LOOP}     4

*** Test Cases ***
# *** comment ***


ALI_BMC_COMM_TC_002_CROSS_VERSION_OPENBMC_UPGRADE_PRIMARY_IN_BMC_OS
    [Tags]
    ...  ALI_BMC_COMM_TC_002_CROSS_VERSION_OPENBMC_UPGRADE_PRIMARY_IN_BMC_OS
    ...  migaloo
    ...  shamu

    Step  1  verify boot info  console=${openbmc_mode}
    Step  2  execute command and verify exit code  console=${openbmc_mode}  command=cat /etc/issue
    Step  3  Setting up flash memory boot  console=${openbmc_mode}   flash=master
    Step  4  set sonic system idle time
    Step  5  check cpu alive  True  ${cpu_test_path}
    Step  6  update master bmc cross version  isUpgrade=True
    Step  7  update master bmc cross version  isUpgrade=False
    Step  8  update master bmc cross version  isUpgrade=True
    [Teardown]  Run Keywords  clean images  DUT  BMC
                ...      AND  Run Keyword And Ignore Error  change kernel log level  console=${openbmc_mode}  level=7


ALI_BMC_COMM_TC_003_ONLINE_UPDATE_BMC_IN_BMC_OS
    [Documentation]  This test checks the BMC FW programming functions by updating the BMC FW in BMC OS
    [Tags]  ALI_BMC_COMM_TC_003_ONLINE_UPDATE_BMC_IN_BMC_OS  migaloo  shamu  long_time
    [Timeout]  150 min 00 seconds
    [Setup]  Run Keywords  Setting up flash memory boot  console=${openbmc_mode}  flash=master
             ...      AND  set sonic system idle time
    Step  1  verify current boot flash  BMC  master
    Step  2  check cpu alive  True  ${cpu_test_path}
    Step  3  update master bmc  isUpgrade=True
    Step  4  update master bmc  isUpgrade=False
    Step  5  update master bmc  isUpgrade=True
    Step  6  update slave bmc  isUpgrade=False
    Step  7  update slave bmc  isUpgrade=True
    [Teardown]  Run Keywords  clean images  DUT  BMC
                ...      AND  Run Keyword And Ignore Error  change kernel log level  console=${openbmc_mode}  level=7


ALI_BMC_COMM_TC_004_OPENBMC_UART_INFORMATION_CHECK
    [Documentation]  This test checks BMC booting log after reboot
    [Tags]  ALI_BMC_COMM_TC_004_OPENBMC_UART_INFORMATION_CHECK  shamu
    ...  migaloo

    Step  1  reboot openbmc and check error log
    Step  2  reboot openbmc and check error log
    Step  3  reboot openbmc and check error log
    Step  4  clear monitor log
    Step  5  power cycle to openbmc  timeout=600
    BuiltIn.Sleep  90
    Step  6  check monitor status
    Step  7  check monitor log
    Step  8  clear monitor log
    Step  9  OpenBMC reboot
    BuiltIn.Sleep  90
    Step  10  check monitor status
    Step  11  check monitor log
    [Teardown]  open prompt  console=${openbmc_mode}  sec=300


ALI_BMC_COMM_TC_005_ONLINE_UPDATE_BIOS_IN_BMC_OS
    [Documentation]  This test checks the BMC FW programming functions by updating the BIOS FW in BMC OS
    [Tags]  ALI_BMC_COMM_TC_005_ONLINE_UPDATE_BIOS_IN_BMC_OS  migaloo  shamu
    [Timeout]  150 min 00 seconds
    [Setup]  prepare image  ${bios_local_image_path}  BIOS  upgrade=True
    Step  1  check and switch bios boot
    Step  2  update bios  bios_flash=master  isUpgrade=True
    Step  3  prepare image  ${bios_local_image_path}  BIOS  upgrade=False
    Step  4  update bios  bios_flash=master  isUpgrade=False
    Step  5  prepare image  ${bios_local_image_path}  BIOS  upgrade=True
    Step  6  update bios  bios_flash=master  isUpgrade=True
    Step  7  check and switch bios boot
    Step  8  prepare image  ${bios_local_image_path}  BIOS  upgrade=False
    Step  9  update bios  bios_flash=slave  isUpgrade=False  forceUpdate=True
    Step  10  prepare image  ${bios_local_image_path}  BIOS  upgrade=True
    Step  11  update bios  bios_flash=slave  isUpgrade=True  forceUpdate=True
    [Teardown]  Run Keywords  switch to openbmc
                ...      AND  check and switch bios boot
                ...      AND  clean images  DUT  BIOS


ALI_BMC_COMM_TC_006_ONLINE_UPDATE_CPLD_IN_BMC_OS_IN_HW_MODE
    [Documentation]  This test checks the BMC FW programming functions by updating the cpld in BMC OS
    [Tags]  ALI_BMC_COMM_TC_006_ONLINE_UPDATE_CPLD_IN_BMC_OS_IN_HW_MODE  migaloo  shamu  long_time
    Step  1  update cpld in bmc  isUpgrade=True
    Step  2  update cpld in bmc  isUpgrade=False
    Step  3  update cpld in bmc  isUpgrade=True
    [Teardown]  Run Keywords  switch to openbmc
                ...      AND  execute command and verify exit code
                              ...  console=${openbmc_mode}
                              ...  command=echo ${fpga_buf_ctrl_default_val} > /sys/bus/i2c/devices/0-000d/fpga_buf_ctrl
                ...      AND  BuiltIn.Sleep  1
                ...      AND  execute command and verify exit code
                              ...  console=${openbmc_mode}
                              ...  command=cat /sys/bus/i2c/devices/0-000d/fpga_buf_ctrl
                ...      AND  BuiltIn.Sleep  1
                ...      AND  clean images CPLD
                ...      AND  recover network  ###@WORKAROUND try recover network before run the auto cases, need find which case break down the network!!!

ALI_BMC_COMM_TC_007_ONLINE_UPDATE_FPGA_IN_SONIC
    [Tags]  ALI_BMC_COMM_TC_007_ONLINE_UPDATE_FPGA_IN_SONIC  shamu
    ...  migaloo
    Step  1  update fpga in sonic  isUpgrade=True
    ...  fpga_image=${fpga_new_fw_name}  fpga_ver_patterns=${fpga_new_version_patterns}
    Step  2  update fpga in sonic  isUpgrade=False
    ...  fpga_image=${fpga_old_fw_name}  fpga_ver_patterns=${fpga_old_version_patterns}
    Step  3  update fpga in sonic  isUpgrade=True
    ...  fpga_image=${fpga_new_fw_name}  fpga_ver_patterns=${fpga_new_version_patterns}
    [Teardown]  Run Keywords  recover cpu
                ...      AND  open prompt  ${diagos_mode}  10
                ...      AND  clean images  DUT  FPGA


ALI_BMC_COMM_TC_008_BACKUP_BMC_MANUAL_BOOTING_TEST
    [Tags]
    ...  ALI_BMC_COMM_TC_008_BACKUP_BMC_MANUAL_BOOTING_TEST
    ...  migaloo
    ...  shamu

    # Get started with slave flash all the time
    [Setup]  Run Keyword And Ignore Error
    ...  Run Keywords
    ...  Setting up flash memory boot  flash=master  AND
    ...  verify boot info  pattern=(?i)(?P<boot_master>Master)
    BuiltIn.sleep  20
    Step  1   switch bmc and check boot source and log
    ...  bmc_flash=slave
    ...  bmc_boot_log_pattern=${bmc_boot_slave_pattern}
    BuiltIn.sleep  20
    Step  2   switch bmc and check boot source and log
    ...  bmc_flash=master
    ...  bmc_boot_log_pattern=${bmc_boot_master_pattern}
    BuiltIn.sleep  20
    Step  3  switch bmc and check boot source and log
    ...  bmc_flash=slave
    ...  bmc_boot_log_pattern=${bmc_boot_slave_pattern}
    Step  4  power cycle to openbmc
    BuiltIn.Sleep  20
    Step  5   verify boot info  pattern=(?i)(?P<boot_master>Master)
    # To make sure next step is boot from Master flash!
    [Teardown]  Run Keyword And Ignore Error
    ...  Run Keywords
    ...  Setting up flash memory boot  flash=master  AND
    ...  verify boot info  pattern=(?i)(?P<boot_master>Master)  AND
    ...  change kernel log level  console=${openbmc_mode}  level=7


ALI_BMC_COMM_TC_009_BACKUP_BIOS_MANUAL_BOOTING_TEST
    [Tags]
    ...  ALI_BMC_COMM_TC_009_BACKUP_BIOS_MANUAL_BOOTING_TEST
    ...  migaloo
    ...  shamu
    [Setup]  check and switch bios boot
    Step  1  verify current boot flash  BIOS  master
    Step  2  switch bios and check boot source and log  slave  ${bios_boot_slave_pattern}
    Step  3  switch bios and check boot source and log  master  ${bios_boot_master_pattern}
    Step  4  switch bios flash  slave
    Step  5  verify current boot flash  BIOS  slave
    Step  6  power cycle to openbmc
    BuiltIn.Sleep  20
    Step  7  verify current boot flash  BIOS  master
    [Teardown]  Run Keyword If Test Failed  check and switch bios boot


ALI_BMC_COMM_TC_010_BMC_NETWORK_CONFIG_TEST
    [Tags]  ALI_BMC_COMM_TC_010_BMC_NETWORK_CONFIG_TEST
    ...  migaloo
    ...  shamu

    [Setup]  Run Keyword And Ignore Error
    ...  Run Keywords
    ...  change kernel log level  console=${diagos_mode}  level=3  AND
    ...  change kernel log level  console=${openbmc_mode}  level=3

    Step  1   flush network interface  console=${openbmc_mode}  interface=eth0
    ${openbmc_ipv6}=   check ip address list
    ...  device=DUT
    ...  interfaceName=eth0
    ...  mode=${openbmc_mode}
    ...  preferred_network=fe80
    ...  ipv6=True
    ...  staticMode=True

    Step  3   flush network interface  console=${diagos_mode}  interface=eth0
    ${diagos_ipv6}=   check ip address list
    ...  device=DUT
    ...  interfaceName=eth0
    ...  mode=${diagos_mode}
    ...  preferred_network=fe80
    ...  ipv6=True
    ...  staticMode=True
    BuiltIn.Sleep  5
    Step  5   ping to IP  console=${diagos_mode}  ip=${openbmc_ipv6} -I eth0  ip_ver=6  time=10
    Step  6   execute command and set test variable  console=${diagos_mode}  command=dd if=/dev/zero of=/home/admin/test bs=1M count=60
    Step  7   copy files through scp
    ...  device=DUT
    ...  username=${openbmc_username}
    ...  password=${openbmc_password}
    ...  server_ip=${openbmc_ipv6}
    ...  filelist=["test"]
    ...  filepath=/home/admin/
    ...  destination_path=/tmp/
    ...  mode=${diagos_mode}
    ...  swap=True
    ...  ipv6=True
    ...  interface=eth0
    ...  retry=3
    Step  8   execute command and verify with a pattern
    ...  console=${openbmc_mode}
    ...  command=ls /tmp/test
    ...  pattern=(?P<found>test)
    Step  9   execute command and set test variable  console=${openbmc_mode}  command=ifconfig -a

    Step  10  flush network interface  console=${openbmc_mode}  interface=eth0
    ${openbmc_ip}=   check ip address list
    ...  device=DUT
    ...  interfaceName=eth0
    ...  mode=${openbmc_mode}
    ...  ipv6=False
    ...  staticMode=True

    Step  12  flush network interface  console=${diagos_mode}  interface=eth0
    ${diagos_ip}=   check ip address list
    ...  device=DUT
    ...  interfaceName=eth0
    ...  mode=${diagos_mode}
    ...  ipv6=False
    ...  staticMode=True
    BuiltIn.Sleep  5

    Step  14  ping to IP  console=${diagos_mode}  ip=${openbmc_ip} -I eth0
    Step  15  ping to IP  console=${openbmc_mode}  ip=${diagos_ip} -I eth0

    Step  16  OpenBMC reboot
    BuiltIn.Sleep  60
    Step  17  Run Keyword And Ignore Error
    ...  change kernel log level  console=${openbmc_mode}  level=3

    Step  18  show network interface IP  console=${openbmc_mode}  interface=eth0

    Step  19  OpenBMC renew IP using DHCP and set variable
    Step  20  show network interface IP  console=${diagos_mode}  interface=eth0
    Step  21  DiagOS renew IP using DHCP and set variable
    BuiltIn.Sleep  5

    Step  22  ping to IP  console=${openbmc_mode}  ip=${diagos_dhcp_info}[dhcp_our_new_ip]
    Step  23  ping to IP  console=${diagos_mode}  ip=${openbmc_dhcp_info}[dhcp_our_new_ip]

    # This one is used to fix AliOpenBmcLib.Prepare Autotest Images failed to get files
    [Teardown]  Run Keyword and Ignore Error
    ...  Run Keywords
    ...  flush network interface  console=${openbmc_mode}  interface=eth0  AND
    ...  renew IP using DHCP  console=${openbmc_mode}  interface=eth0  AND
    ...  flush network interface  console=${diagos_mode}  interface=eth0  AND
    ...  renew IP using DHCP  console=${diagos_mode}  interface=eth0  AND
    ...  change kernel log level  console=${openbmc_mode}  level=7  AND
    ...  change kernel log level  console=${diagos_mode}  level=7  AND
    ...  remove file/folder  console=${diagos_mode}  file=/home/admin/test  AND
    ...  remove file/folder  console=${openbmc_mode}  file=/tmp/test


ALI_BMC_COMM_TC_012_VLAN4088_TEST
    [Tags]  ALI_BMC_COMM_TC_012_VLAN4088_TEST
    ...  migaloo

    Step  1   open prompt  console=${openbmc_mode}  sec=300
    Step  2   reboot UNIX-like OS  console=${openbmc_mode}
    Step  3   open prompt and login to root user  console=${openbmc_mode}
    Step  4   ssh execute
    ...  console=${diagos_mode}
    ...  command=cat /etc/issue
    ...  username=${openbmc_username}
    ...  password=${openbmc_password}
    ...  server_ip=240.1.1.1
    Step  5   verify exit code  msg=An executed command on the SSH Server,${\n}is not return exit code zero / unsuccessful to execute.
    Step  6   execute command and verify exit code
    ...  console=${openbmc_mode}
    ...  command=vconfig rem eth0.4088
    ...  msg=Failed to remove the VLAN name: eth0.4088!
    Step  7   verify the VLAN was removed
    Step  8   reboot openbmc
    Step  9   execute command and verify with a pattern
    ...  console=${openbmc_mode}
    ...  command=ifconfig -a
    ...  pattern=(?m)^(?P<interface_name>eth0\\\\.4088)
    ...  msg=Failed, not found the VLAN name: eth0.4088!


ALI_BMC_COMM_TC_013_OPENBMC_MAC_ADDRESS_TEST
    [Tags]  ALI_BMC_COMM_TC_013_OPENBMC_MAC_ADDRESS_TEST
    ...  migaloo
    ...  shamu
    [Setup]  Run Keywords
    ...  OpenBMC reboot  AND
    ...  Run Keyword And Ignore Error  change kernel log level  console=${openbmc_mode}  level=3  AND
    ...  Run Keyword And Ignore Error  execute command and verify exit code  console=${openbmc_mode}  command=sleep 10  sec=15  AND
    ...  ifconfig to save original mac address  AND
    ...  Run Keyword And Ignore Error  execute command and verify exit code  console=${openbmc_mode}  command=sleep 60  sec=65
    ...  AND  close eeprom write protect

    Step  1   show file content
    ...  console=${openbmc_mode}
    ...  path=${sys_eeprom_path}
    ...  file=eeprom.cfg
    Step  2   change MAC address file configuration  mac=AA:BB:CC:DD:EE:FE
    Step  3   verify eeprom tool dumpped mac information
    Step  4   verify network interface MAC address
    ...  console=${openbmc_mode}
    ...  interface=eth0
    ...  mac=(?:[a-fA-F0-9]{2}:?){6}
    Step  5   eeprom tool write, update, dump and verify MAC information
    Step  6   verify eeprom tool dumpped mac information
    ...  pattern=Product[ \\\\t]+Extra_\\\\d+[ \\\\t]+:[ \\\\t]*(?P<eepromtool_mac>${written_eepromtool_mac}[written_eepromtool_mac])
    ...  msg=The MAC should not update yet!
    Step  7   OpenBMC reboot
    Step  8   Run Keyword And Ignore Error
    ...  change kernel log level  console=${openbmc_mode}  level=3
    # Wait for ethernet update its MAC, around 1 min (later know 3 mins is more sure)
    Step  9   execute command and verify exit code  console=${openbmc_mode}  command=sleep 180  sec=200
    Step  10  verify eeprom tool dumpped mac information
    ...  pattern=Product[ \\\\t]+Extra_\\\\d+[ \\\\t]+:[ \\\\t]*(?P<eepromtool_mac>${written_eepromtool_mac}[written_eepromtool_mac])
    ...  msg=The MAC address does not treat after reboot the system!
    Step  11   verify network interface MAC address
    ...  console=${openbmc_mode}
    ...  interface=eth0
    ...  mac=(?:[a-fA-F0-9]{2}:?){6}
    Step  12  compare MAC address for eeprom tool and ifconfig

    [Teardown]  Run Keywords
    ...  change MAC address file configuration  mac=${mac_original}[ifconfig_mac]  AND
    ...  eeprom tool write, update, dump and verify MAC information  pattern=Product[ \\t]+Extra_\\d+[ \\t]+:[ \\t]*(?P<mac>${mac_original}[ifconfig_mac])  AND
    ...  Run Keyword And Ignore Error  change kernel log level  console=${openbmc_mode}  level=7


ALI_BMC_COMM_TC_014_POWER_CONTROL
    [Tags]  ALI_BMC_COMM_TC_014_POWER_CONTROL  migaloo  shamu
    [Timeout]  150 min 00 seconds
    [Setup]  Run Keyword And Ignore Error
    ...  change kernel log level  console=${openbmc_mode}  level=3
    Step  1  power cycle to openbmc
    BuiltIn.Sleep  20
    Step  2  Run Keyword And Ignore Error  change kernel log level  console=${openbmc_mode}  level=3
    Step  3  check power status of cpu
    Step  4  test power control  cycle
    Step  5  test power control  reset
    BuiltIn.Sleep  60
    Step  6  verify power control  off
    Step  7  check power status of cpu  off  not OK
    Step  8  test power control  on
    [Teardown]  Run Keywords
    ...  recover cpu  AND
    ...  Run Keyword And Ignore Error  change kernel log level  console=${openbmc_mode}  level=7


ALI_BMC_COMM_TC_015_OPENBMC_RESET_TEST
    [Tags]  ALI_BMC_COMM_TC_015_OPENBMC_RESET_TEST  migaloo  shamu
    [Timeout]  60 min 00 seconds
    [Setup]  set sonic system idle time
    Step  1  verify current boot flash  BMC  master
    Step  2  check cpu alive  need_cd=True  path=${cpu_test_path}
    Step  3  reboot openbmc
    Step  4  check cpu alive  path=${cpu_test_path}
    Step  5  verify current boot flash  BMC  master
    BuiltIn.Sleep  20

    Step  6  switch bmc flash  slave
    Step  7  check cpu alive  path=${cpu_test_path}
    Step  8  verify current boot flash  BMC  slave
    Step  9  reboot openbmc
    Step  10  check cpu alive  path=${cpu_test_path}
    Step  11  verify current boot flash  BMC  slave
    BuiltIn.Sleep  20

    Step  12  switch bmc flash  master
    Step  13  verify current boot flash  BMC  master
    [Teardown]  Run Keyword If Test Failed  Run Keywords
    ...  BuiltIn.Sleep  20  AND
    ...  switch bmc flash  master

ALI_BMC_COMM_TC_016_POWER_COMMAND_TEST_IN_SONIC
    [Tags]  ALI_BMC_COMM_TC_016_POWER_COMMAND_TEST_IN_SONIC  migaloo  shamu
    [Setup]  wait bmc restful
    Step  1  run power command  cpu
    wait bmc restful
    Step  2  run power command  system
    [Teardown]  recover cpu

ALI_BMC_COMM_TC_017_BMC_EXEC_COMMAND_TEST_IN_SONIC
    [Tags]  ALI_BMC_COMM_TC_017_BMC_EXEC_COMMAND_TEST_IN_SONIC  migaloo  shamu
    [Setup]  wait bmc restful
    Step  1  execute command and verify with a pattern
    ...  console=${diagos_mode}
    ...  command=bmc-exec "ls -lh"
    ...  pattern=${ls_lh_pattern}
    ...  msg=Failed to run bmc-exec
    Step  2  execute command and verify with a pattern
    ...  console=${diagos_mode}
    ...  command=bmc-exec "cat /etc/issue"
    ...  pattern=${openbmc_version_regex}
    ...  msg=Failed to run bmc-exec

ALI_BMC_COMM_TC_023_SIMULATE_BMC_HANG_AND_RESTORE
    [Tags]  ALI_BMC_COMM_TC_023_SIMULATE_BMC_HANG_AND_RESTORE  migaloo  shamu
    Step  1  boot into uboot mode
    BuiltIn.Sleep  330
    Step  2  open prompt  ${openbmc_mode}  300
    BuiltIn.Sleep  30
    Step  3  Run Keyword And Ignore Error
    ...  change kernel log level  console=${openbmc_mode}  level=3
    Step  4  get fan speed  100  None  check_rpm=False
    BuiltIn.Sleep  120
    Step  5  get fan speed  30  70  check_rpm=False
    [Teardown]  switch bmc flash  master


ALI_BMC_COMM_TC_025_FAN_SPEED_MANUAL_CONTROL
    [Tags]  ALI_BMC_COMM_TC_025_FAN_SPEED_MANUAL_CONTROL  migaloo  shamu
    [Setup]  Run Keywords
    ...  BuiltIn.Sleep  120  AND
    ...  Run Keyword And Ignore Error  change kernel log level  console=${openbmc_mode}  level=3
    Step  1  get fan speed  30  70
    Step  2  execute command and verify exit code
    ...  console=${openbmc_mode}
    ...  command=systemctl stop fanctrl
    Step  3  set and get fan speed  10
    Step  4  execute command and verify exit code
    ...  console=${openbmc_mode}
    ...  command=systemctl start fanctrl
    BuiltIn.Sleep  120
    Step  5  get fan speed  30  70
    Step  6  execute command and verify exit code
    ...  console=${openbmc_mode}
    ...  command=systemctl stop fanctrl
    Step  7  set and get fan speed  25
    Step  8  set and get fan speed  50
    Step  9  set and get fan speed  70
    Step  10  set and get fan speed  10
    Step  11  set and get fan speed  70
    Step  12  set and get fan speed  10
    Step  13  set and get fan speed  70
    Step  14  set and get fan speed  10
    Step  15  execute command and verify exit code
    ...  console=${openbmc_mode}
    ...  command=systemctl start fanctrl
    BuiltIn.Sleep  40
    [Teardown]  Run Keywords
    ...  Run Keyword If Test Failed  execute command and verify exit code
    ...  console=${openbmc_mode}
    ...  command=systemctl start fanctrl  AND
    ...  Run Keyword And Ignore Error  change kernel log level  console=${openbmc_mode}  level=7


ALI_BMC_COMM_TC_026_WDT1_TEST
    [Tags]  ALI_BMC_COMM_TC_026_WDT1_TEST  migaloo  shamu
    Step  1  power cycle to openbmc
    Step  2  reset bmc via devmem
    Step  3  verify watchdog info  ${wdt_patterns_1}
    Step  4  reboot openbmc
    Step  5  verify watchdog info  ${wdt_patterns_2}
    BuiltIn.Sleep  20
    Step  6  switch bmc flash  slave
    Step  7  verify watchdog info  ${wdt_patterns_3}
    BuiltIn.Sleep  20
    Step  8  reset bmc via devmem
    Step  9  verify watchdog info  ${wdt_patterns_4}
    Step  10  reboot openbmc
    Step  11  verify watchdog info  ${wdt_patterns_5}
    BuiltIn.Sleep  20
    Step  12  switch bmc flash  master
    Step  13  verify watchdog info  ${wdt_patterns_6}
    [Teardown]  Run Keyword If Test Failed  Run Keywords
    ...  BuiltIn.Sleep  20  AND
    ...  switch bmc flash  master


ALI_BMC_COMM_TC_028_BMC_FLASH_BACKUP_FUNCTION
    [Tags]  ALI_BMC_COMM_TC_028_BMC_FLASH_BACKUP_FUNCTION  migaloo  shamu  long_time
    [Timeout]  150 min 00 seconds
    Step  1  update bmc crash and check backup bmc can boot
    ...  bmc_flash=master
    ...  backup_flash=slave
    ...  boot_patterns=${bmc_boot_slave_pattern}
    Step  2  restore openbmc master
    Step  3  verify current boot flash  BMC  master
    Step  4  update bmc crash and check backup bmc can boot
    ...  bmc_flash=slave
    ...  backup_flash=master
    ...  boot_patterns=${bmc_boot_master_pattern}
    Step  5  restore openbmc slave
    [Teardown]  Run Keyword If Test Failed  restore openbmc master


ALI_BMC_COMM_TC_029_BIOS_FLASH_BACKUP_FUNCTION
    [Tags]  ALI_BMC_COMM_TC_029_BIOS_FLASH_BACKUP_FUNCTION  migaloo  shamu  long_time
    [Timeout]  150 min 00 seconds
    [Setup]  prepare file on usb device
    #### ALI_BMC_COMM_TC_029_1
    Step  1  check and switch bios boot  master
    Step  2  Run keywords
    ...  clear log  ${openbmc_mode}  ${syslog_path}  AND
    ...  clear log  ${openbmc_mode}  ${cpumon_log}
    Step  3  update bios crash
    Step  4  verify current boot flash  BIOS  master  not OK
    BuiltIn.Sleep  60
    Step  5  check logs and verify bios boot from  ${bios_boot_master_fail_pattern}
    BuiltIn.Sleep  120
    Step  6  verify current boot flash  BIOS  slave
    Step  7  check logs and verify bios boot from  ${bios_boot_master_fail_pattern}
    Step  8  check logs and verify bios boot from  ${bios_boot_slave_pattern}
    Step  9  restore bios master

    #### ALI_BMC_COMM_TC_029_2
    Step  10  check and switch bios boot  slave
    Step  11  Run keywords
    ...  clear log  ${openbmc_mode}  ${syslog_path}  AND
    ...  clear log  ${openbmc_mode}  ${cpumon_log}
    Step  12  update bios crash
    BuiltIn.Sleep  120
    Step  13  verify current boot flash  BIOS  master
    Step  14  send switch slave bios
    Step  15  verify current boot flash  BIOS  slave  not OK
    Step  16  check logs and verify bios boot from  ${bios_boot_slave_fail_pattern}
    Step  17  power cycle to openbmc  timeout=600
    Step  18  verify current boot flash  BIOS  master
    Step  19  restore bios slave
    [Teardown]  Run Keyword If Test Failed
                         ...  Run Keywords  open prompt  console=${diagos_mode}  sec=300
                         ...           AND  switch to openbmc
                         ...           AND  restore bios master
                         ...           AND  restore bios slave
                         ...           AND  recover cpu

ALI_BMC_COMM_TC_030_BMC_EEPROM_R/W_TEST
    [Tags]  ALI_BMC_COMM_TC_030_BMC_EEPROM_R/W_TEST  migaloo  shamu
    [Timeout]  25 min 00 seconds
    [Setup]  prepare store eeprom  ${bmc_eeprom_path}
    Step  1  change dir  ${bmc_eeprom_path}  ${openbmc_mode}
    Step  2  check fru data match with fru-util command  ${bmc_fru}
    Step  3  write and read eeprom  ${bmc_eeprom_test}  ${bmc_fru_type}  ${bmc_fru}
    Step  4  write and read eeprom  ${bmc_eeprom_test2}  ${bmc_fru_type}  ${bmc_fru}
    Step  5  reboot openbmc and read eeprom  ${bmc_eeprom_path}  ${bmc_eeprom_test2}
    [Teardown]  restore eeprom  ${bmc_eeprom_path}

ALI_BMC_COMM_TC_031_SYSTEM_EEPROM_R/W_TEST
    [Tags]  ALI_BMC_COMM_TC_031_SYSTEM_EEPROM_R/W_TEST  migaloo  shamu
    [Timeout]  25 min 00 seconds
    [Setup]  Run Keywords  close eeprom write protect
    ...  AND  prepare store eeprom  ${sys_eeprom_path}
    Step  1  change dir  ${sys_eeprom_path}  ${openbmc_mode}
    Step  2  check fru data match with fru-util command  ${sys_fru}
    Step  3  write and read eeprom  ${sys_eeprom_test}  ${sys_fru_type}  ${sys_fru}
    Step  4  write and read eeprom  ${sys_eeprom_test2}  ${sys_fru_type}  ${sys_fru}
    Step  5  reboot openbmc and read eeprom  ${sys_eeprom_path}  ${sys_eeprom_test2}

    [Teardown]  restore eeprom  ${sys_eeprom_path}

ALI_BMC_COMM_TC_032_FCB_EEPROM_R/W_TEST
    [Tags]  ALI_BMC_COMM_TC_032_FCB_EEPROM_R/W_TEST  migaloo  shamu
    [Timeout]  25 min 00 seconds
    [Setup]  prepare store eeprom  ${fcb_eeprom_path}
    Step  1  change dir  ${fcb_eeprom_path}  ${openbmc_mode}
    Step  2  check fru data match with fru-util command  ${fcb_fru}
    Step  3  write and read eeprom  ${fcb_eeprom_test}  ${fcb_fru_type}  ${fcb_fru}
    Step  4  write and read eeprom  ${fcb_eeprom_test2}  ${fcb_fru_type}  ${fcb_fru}
    Step  5  reboot openbmc and read eeprom  ${fcb_eeprom_path}  ${fcb_eeprom_test2}
    [Teardown]  restore eeprom  ${fcb_eeprom_path}

ALI_BMC_COMM_TC_033_COME_EEPROM_R/W_TEST
    [Tags]  ALI_BMC_COMM_TC_033_COME_EEPROM_R/W_TEST  migaloo  shamu
    [Timeout]  25 min 00 seconds
    [Setup]  prepare store eeprom  ${come_eeprom_path}
    Step  1  change dir  ${come_eeprom_path}  ${openbmc_mode}
    Step  2  check fru data match with fru-util command  ${come_fru}
    Step  3  write and read eeprom  ${come_eeprom_test}  ${come_fru_type}  ${come_fru}
    Step  4  write and read eeprom  ${come_eeprom_test2}  ${come_fru_type}  ${come_fru}
    Step  5  reboot openbmc and read eeprom  ${come_eeprom_path}  ${come_eeprom_test2}
    [Teardown]  restore eeprom  ${come_eeprom_path}

ALI_BMC_COMM_TC_034_SWITCH_EEPROM_R/W_TEST
    [Tags]  ALI_BMC_COMM_TC_034_SWITCH_EEPROM_R/W_TEST  migaloo  shamu
    [Timeout]  25 min 00 seconds
    [Setup]  Run Keywords  close eeprom write protect
    ...  AND  prepare store eeprom  ${switch_eeprom_path}
    Step  1  change dir  ${switch_eeprom_path}  ${openbmc_mode}
    Step  2  check fru data match with fru-util command  ${switch_fru}
    Step  3  write and read eeprom  ${switch_eeprom_test}  ${switch_fru_type}  ${switch_fru}
    Step  4  write and read eeprom  ${switch_eeprom_test2}  ${switch_fru_type}  ${switch_fru}
    Step  5  reboot openbmc and read eeprom  ${switch_eeprom_path}  ${switch_eeprom_test2}
    [Teardown]  restore eeprom  ${switch_eeprom_path}

ALI_BMC_COMM_TC_035_FAN_EEPROM_R/W_TEST
    [Tags]  ALI_BMC_COMM_TC_035_FAN_EEPROM_R/W_TEST  migaloo  shamu
    [Timeout]  25 min 00 seconds
    [Setup]  prepare store all fan eeprom
    Step  1  change dir  ${fan_eeprom_path}  ${openbmc_mode}
    Step  2  check fan fru data match with fru-util command
    Step  3  write and read fan eeprom  ${fan_eeprom_test}
    Step  4  write and read fan eeprom  ${fan_eeprom_test2}
    Step  5  reboot openbmc and read fan eeprom  ${fan_eeprom_test2}
    [Teardown]  restore all fan eeprom

ALI_BMC_COMM_TC_036_PSU_EEPROM_READ_TEST
    [Tags]  ALI_BMC_COMM_TC_036_PSU_EEPROM_READ_TEST  migaloo  shamu
    FOR    ${psu}    IN RANGE    ${1}  ${PSU_NUM}+1
        Step  1  execute command and verify with ordered pattern list
        ...  console=${openbmc_mode}
        ...  command=fru-util psu -p ${psu}
        ...  patterns=${psu_${psu}_fru_patterns}
        ...  msg=Failed to verify fru-util psu -p ${psu}!
    END
    Step  2  execute command and verify with ordered pattern list
    ...  console=${openbmc_mode}
    ...  command=${psu_all_fru_cmd}
    ...  patterns=${psu_all_fru_normal_patterns}
    ...  msg=Failed to verify ${psu_all_fru_cmd}!

ALI_BMC_COMM_TC_037_RESTFUL_OPENBMC_NEXT_BOOT_TEST
    [Tags]  ALI_BMC_COMM_TC_037_RESTFUL_OPENBMC_NEXT_BOOT_TEST  migaloo  shamu
    [Setup]  Run Keywords
    ...      switch bmc flash  master  AND
    ...      wait bmc restful
    Step  1  restful get nextboot and info
    ...  nextboot_url=${api_bmc_nextboot}
    ...  info_url=${api_bmc_info}
    ...  nextboot_patterns=${nextboot_master_patterns}
    ...  info_patterns=${info_master_master_patterns}
    Step  2  restful set nextboot
    ...  nextboot_url=${api_bmc_nextboot}
    ...  nextboot=slave
    Step  3  restful get nextboot and info
    ...  nextboot_url=${api_bmc_nextboot}
    ...  info_url=${api_bmc_info}
    ...  nextboot_patterns=${nextboot_slave_patterns}
    ...  info_patterns=${info_master_slave_patterns}
    Step  4  restful reboot bmc
    ...  current_boot=slave
    wait bmc restful
    Step  5  restful get nextboot and info
    ...  nextboot_url=${api_bmc_nextboot}
    ...  info_url=${api_bmc_info}
    ...  nextboot_patterns=${nextboot_slave_patterns}
    ...  info_patterns=${info_slave_slave_patterns}

    Step  6  restful set nextboot
    ...  nextboot_url=${api_bmc_nextboot}
    ...  nextboot=master
    Step  7  restful get nextboot and info
    ...  nextboot_url=${api_bmc_nextboot}
    ...  info_url=${api_bmc_info}
    ...  nextboot_patterns=${nextboot_master_patterns}
    ...  info_patterns=${info_slave_master_patterns}
    Step  8  restful reboot bmc
    ...  current_boot=master
    wait bmc restful
    Step  9  restful get nextboot and info
    ...  nextboot_url=${api_bmc_nextboot}
    ...  info_url=${api_bmc_info}
    ...  nextboot_patterns=${nextboot_master_patterns}
    ...  info_patterns=${info_master_master_patterns}
    [Teardown]  Run Keyword If Test Failed  Run Keywords
    ...  switch bmc flash  master  AND
    ...  reboot openbmc

ALI_BMC_COMM_TC_038_RESTFUL_BIOS_NEXT_BOOT_TEST
    [Tags]  ALI_BMC_COMM_TC_038_RESTFUL_BIOS_NEXT_BOOT_TEST  migaloo  shamu
    [Setup]  Run Keywords
    ...      check and switch bios boot  AND
    ...      wait bmc restful  60
    Step  1  restful get nextboot and info
    ...  nextboot_url=${api_bios_nextboot}
    ...  info_url=${api_bios_info}
    ...  nextboot_patterns=${nextboot_master_patterns}
    ...  info_patterns=${nextboot_master_patterns}
    Step  2  restful set nextboot
    ...  nextboot_url=${api_bios_nextboot}
    ...  nextboot=slave
    Step  3  restful get nextboot and info
    ...  nextboot_url=${api_bios_nextboot}
    ...  info_url=${api_bios_info}
    ...  nextboot_patterns=${nextboot_slave_patterns}
    ...  info_patterns=${nextboot_master_patterns}
    Step  4  restful reboot cpu
    ...  current_boot_pattern=Backup
    wait bmc restful
    Step  5  restful get nextboot and info
    ...  nextboot_url=${api_bios_nextboot}
    ...  info_url=${api_bios_info}
    ...  nextboot_patterns=${nextboot_slave_patterns}
    ...  info_patterns=${nextboot_slave_patterns}
    Step  6  restful set nextboot
    ...  nextboot_url=${api_bios_nextboot}
    ...  nextboot=master
    Step  7  restful get nextboot and info
    ...  nextboot_url=${api_bios_nextboot}
    ...  info_url=${api_bios_info}
    ...  nextboot_patterns=${nextboot_master_patterns}
    ...  info_patterns=${nextboot_slave_patterns}
    Step  8  restful reboot cpu
    ...  current_boot_pattern=Primary
    wait bmc restful
    Step  9  restful get nextboot and info
    ...  nextboot_url=${api_bios_nextboot}
    ...  info_url=${api_bios_info}
    ...  nextboot_patterns=${nextboot_master_patterns}
    ...  info_patterns=${nextboot_master_patterns}
    [Teardown]  Run Keyword If Test Failed  Run Keywords
    ...  check and switch bios boot  AND
    ...  reboot openbmc

ALI_BMC_COMM_TC_039_HAL_UNIT_TEST
    [Tags]  ALI_BMC_COMM_TC_039_HAL_UNIT_TEST  migaloo  shamu
    [Setup]  Run Keywords  execute command and verify exit code
                           ...  path=/tmp
                           ...  console=${openbmc_mode}
                           ...  command=touch cl_image_flag
             ...      AND  Run Keyword And Ignore Error  change kernel log level  console=${openbmc_mode}  level=3
    Step  1  execute command and verify with a pattern
    ...  console=${openbmc_mode}
    ...  command=${hal_unit_test_cmd} test_bmc
    ...  path=${hal_unit_test_path}
    ...  pattern=(?m)^[ \\\\t]*OK[ \\\\t]*
    ...  msg=Failed to run test_bmc
    ...  is_check_exit_code=${FALSE}
    ...  sec=300
    Step  2  execute command and verify with a pattern
    ...  console=${openbmc_mode}
    ...  command=${hal_unit_test_cmd} test_cpu
    ...  path=${hal_unit_test_path}
    ...  pattern=(?m)^[ \\\\t]*OK[ \\\\t]*
    ...  msg=Failed to run test_cpu
    ...  is_check_exit_code=${FALSE}
    ...  sec=300
    Step  3  execute command and verify with a pattern
    ...  console=${openbmc_mode}
    ...  command=${hal_unit_test_cmd} test_misc
    ...  path=${hal_unit_test_path}
    ...  pattern=(?m)^[ \\\\t]*OK[ \\\\t]*
    ...  msg=Failed to run test_misc
    ...  is_check_exit_code=${FALSE}
    ...  sec=800
    Step  4  execute command and verify with a pattern
    ...  console=${openbmc_mode}
    ...  command=${hal_unit_test_cmd} test_sensor
    ...  path=${hal_unit_test_path}
    ...  pattern=(?m)^[ \\\\t]*OK[ \\\\t]*
    ...  msg=Failed to run test_sensor
    ...  is_check_exit_code=${FALSE}
    ...  sec=60
    Step  5  execute command and verify with a pattern
    ...  console=${openbmc_mode}
    ...  command=${hal_unit_test_cmd} test_dcdc
    ...  path=${hal_unit_test_path}
    ...  pattern=(?m)^[ \\\\t]*OK[ \\\\t]*
    ...  msg=Failed to run test_dcdc
    ...  is_check_exit_code=${FALSE}
    ...  sec=60
    Step  6  execute command and verify with a pattern
    ...  console=${openbmc_mode}
    ...  command=${hal_unit_test_cmd} test_psu
    ...  path=${hal_unit_test_path}
    ...  pattern=(?m)^[ \\\\t]*OK[ \\\\t]*
    ...  msg=Failed to run test_psu
    ...  is_check_exit_code=${FALSE}
    ...  sec=60
    Step  7  execute command and verify with a pattern
    ...  console=${openbmc_mode}
    ...  command=${hal_unit_test_cmd} test_temp
    ...  path=${hal_unit_test_path}
    ...  pattern=(?m)^[ \\\\t]*OK[ \\\\t]*
    ...  msg=Failed to run test_temp
    ...  is_check_exit_code=${FALSE}
    ...  sec=60
    Step  8  load openbmc utils
    Step  9  execute command and verify exit code
    ...  console=${openbmc_mode}
    ...  command=set_watchdog_status 0
    Step  10  execute command and verify exit code
    ...  console=${openbmc_mode}
    ...  command=systemctl stop fanctrl
    Step  11  execute command and verify with a pattern
    ...  console=${openbmc_mode}
    ...  command=${hal_unit_test_cmd} test_fan
    ...  path=${hal_unit_test_path}
    ...  pattern=(?m)^[ \\\\t]*OK[ \\\\t]*
    ...  msg=Failed to run test_fan
    ...  is_check_exit_code=${FALSE}
    ...  sec=300
    [Teardown]  Run Keywords  execute command and verify exit code
                              ...  console=${openbmc_mode}
                              ...  command=systemctl start fanctrl
                ...      AND  load openbmc utils
                ...      AND  execute command and verify exit code
                              ...  console=${openbmc_mode}
                              ...  command=set_watchdog_status 1
                ...      AND  recover cpu
                ...      AND  Run Keyword And Ignore Error  change kernel log level  console=${openbmc_mode}  level=7

ALI_BMC_COMM_TC_040_SYSTEM_STATUS_LED_CONTROL
    [Tags]  ALI_BMC_COMM_TC_040_SYSTEM_STATUS_LED_CONTROL  migaloo  shamu
    #### Ali_BMC_COMM_TC_040_1
    Step  1  load openbmc utils
    Step  2  set and get sys led  green on  green on
    Step  3  set and get sys led  yellow on  yellow on
    Step  4  set and get sys led  green slow  green 1HZ blink
    Step  5  set and get sys led  green fast  green 4HZ blink
    Step  6  set and get sys led  green off  green off
    Step  7  set and get sys led  yellow slow  yellow 1HZ blink
    Step  8  set and get sys led  yellow fast  yellow 4HZ blink
    Step  9  set and get sys led  yellow off  yellow off
    Step  10  set and get sys led  mix slow  green and yellow 1HZ blink
    Step  11  set and get sys led  mix fast  green and yellow 4HZ blink

    #### Ali_BMC_COMM_TC_040_2
    Step  12  power cycle to openbmc
    Step  13  get sys led  green on
    Step  14  reboot openbmc
    Step  15  get sys led  green on

    ###### The following functions are not implemented, so remove them.

    #### Ali_BMC_COMM_TC_040_3
    # BuiltIn.Sleep  20
    # Step  16  switch bmc flash  slave
    # Step  17  get sys led  yellow on
    # BuiltIn.Sleep  20
    # Step  16  switch bmc flash  master
    # Step  17  get sys led  green on
    # BuiltIn.Sleep  20
    # Step  18  switch bios flash  slave
    # Step  19  get sys led  yellow on
    # BuiltIn.Sleep  20
    # Step  20  switch bios flash  master
    # Step  21  get sys led  green on
    # BuiltIn.Sleep  20
    # Step  22  Run Keywords  switch bios flash  slave  AND  switch bmc flash  slave
    # Step  23  get sys led  yellow on
    # BuiltIn.Sleep  20
    # Step  22  Run Keywords  switch bios flash  master  AND  switch bmc flash  master
    # Step  24  get sys led  green on

    #### Ali_BMC_COMM_TC_040_4 should be manual test

    #### Ali_BMC_COMM_TC_040_5
    # Step  25  prepare file on usb device
    # Step  26  check and switch bios boot  Master
    # Step  27  update bios crash
    # BuiltIn.Sleep  60
    # Step  28  check and switch bios boot  Slave
    # Step  29  update bios crash
    # BuiltIn.Sleep  120
    # Step  30  cpu should off
    # Step  31  get sys led  yellow 1HZ blink
    # Step  32  restore bios master
    # Step  33  restore bios slave

    [Teardown]  Run Keyword If Test Failed  Run Keywords
    ...  switch to openbmc  AND
    # ...  switch bmc flash  master  AND
    # ...  check and restore bios  master  AND
    # ...  check and restore bios  slave  AND
    # ...  check and switch bios boot  master  AND
    ...  recover cpu



ALI_BMC_COMM_TC_042_ARCHIVE_CPU_UART_LOG_TEST
    [Tags]  ALI_BMC_COMM_TC_042_ARCHIVE_CPU_UART_LOG_TEST  migaloo  shamu
    [Timeout]  30 min 00 seconds
    Step  1  clear log  ${openbmc_mode}  ${uart_log_file}
    Step  2  check reboot log
    Step  3  clear log  ${openbmc_mode}  ${uart_log_file}
    Step  4  check reboot log  3

ALI_BMC_COMM_TC_043_OPENBMC_MEMORY_TEST
    [Tags]  ALI_BMC_COMM_TC_043_OPENBMC_MEMORY_TEST  migaloo  shamu
    [Timeout]  30 min 00 seconds
    Step  1  open prompt  console=${openbmc_mode}  sec=300
    Step  2  check memory
    Step  3  memory test

ALI_BMC_COMM_TC_044_SOL_TEST
    [Tags]  ALI_BMC_COMM_TC_044_SOL_TEST  migaloo  shamu
    Step  1  open prompt  console=${openbmc_mode}  sec=10
    Step  2  sol switch to sonic
    BuiltIn.Sleep  3
    Step  3  execute command and verify with a pattern
    ...  console=${diagos_mode}
    ...  path=/
    ...  command=ls -lh
    ...  pattern=${ls_lh_pattern}
    ...  msg=Failed to verify command ls -lh
    Step  4  reboot  mode=${diagos_mode}
    Step  5  sol switch to openbmc
    [Teardown]  Run Keyword If Test Failed  sol switch to openbmc

ALI_BMC_COMM_TC_045_CPLD_REGISTER_RW_TEST
    [Tags]  ALI_BMC_COMM_TC_045_CPLD_REGISTER_RW_TEST  migaloo  shamu
    [Timeout]  30 min 00 seconds
    [Setup]  Run Keyword And Ignore Error
    ...  change kernel log level  console=${openbmc_mode}  level=3
    Step  1  execute command and verify with a pattern
    ...  console=${openbmc_mode}
    ...  command=wedge_power.sh status
    ...  path=${EMPTY}
    ...  pattern=Microserver power is on
    ...  sec=10
    Step  2   open prompt  console=${diagos_mode}  sec=300
    Step  3  execute command and verify with a pattern
    ...  console=${openbmc_mode}
    ...  command=i2cget -f -y 0 0x0d 0x22
    ...  path=${EMPTY}
    ...  pattern=0x0f
    ...  sec=10
    Step  4  execute command  i2cset -f -y 0 0x0d 0x24 0x00; sleep 5; i2cset -f -y 0 0x0d 0x24 0x01
    Step  5  BuiltIn.Sleep  20
    Step  6  execute command and verify with a pattern
    ...  console=${openbmc_mode}
    ...  command=i2cget -f -y 0 0x0d 0x22
    ...  path=${EMPTY}
    ...  pattern=0x08
    ...  sec=20
    Step  7  execute command and verify with a pattern
    ...  console=${openbmc_mode}
    ...  command=wedge_power.sh status
    ...  path=${EMPTY}
    ...  pattern=Microserver power is off
    ...  sec=20
    Step  8  cpu should off
    Step  9  execute command  i2cset -f -y 0 0x0d 0x24 0; sleep 1; i2cset -f -y 0 0x0d 0x24 0x01  mode=${openbmc_mode}
    Step  10  BuiltIn.Sleep  20
    Step  11  execute command and verify with a pattern
    ...  console=${openbmc_mode}
    ...  command=i2cget -f -y 0 0x0d 0x22
    ...  path=${EMPTY}
    ...  pattern=0x0f
    ...  sec=20
    Step  12  execute command and verify with a pattern
    ...  console=${openbmc_mode}
    ...  command=wedge_power.sh status
    ...  path=${EMPTY}
    ...  pattern=Microserver power is on
    ...  sec=20
    Step  13   open prompt  console=${diagos_mode}  sec=300
    Step  14   open prompt  console=${openbmc_mode}  sec=20
    [Teardown]  Run Keywords
    ...  restore cpu  AND
    ...  Run Keyword And Ignore Error  change kernel log level  console=${openbmc_mode}  level=7

ALI_BMC_COMM_TC_046_NTP_TEST
    [Tags]  ALI_BMC_COMM_TC_046_NTP_TEST  migaloo  shamu
    [Setup]  check ntp server
    Step  1  execute command and verify with ordered pattern list
    ...  console=${diagos_mode}
    ...  command=ntpstat
    ...  patterns=${ntpstat_patterns}
    ...  msg=Failed to verify ntpstat!
    Step  2  wait and verify date sync
    Step  3  execute command and verify exit code
    ...  console=${openbmc_mode}
    ...  command=date -s "2020-05-05 05:05:05"
    BuiltIn.Sleep  300
    Step  4  wait and verify date sync
    Step  5  reboot openbmc
    Step  6  wait and verify date sync
    Step  7  reboot openbmc
    Step  8  wait and verify date sync

ALI_BMC_COMM_TC_048_LED_LOCATION_TEST
    [Tags]  ALI_BMC_COMM_TC_048_LED_LOCATION_TEST  migaloo  shamu
    [Setup]  Run Keyword And Ignore Error
    ...  change kernel log level  console=${openbmc_mode}  level=3
    Step  1  switch bmc flash  Master
    Step  2  verify power status  on
    Step  3  execute command and verify with a pattern
    ...  console=${openbmc_mode}
    ...  command=led_location status
    ...  pattern=${get_off_pattern}
    ...  msg=Failed to verify led location!
    Step  4  execute command and verify with a pattern
    ...  console=${openbmc_mode}
    ...  command=led_location on
    ...  pattern=${set_pass_pattern}
    ...  msg=Failed to set led location!
    Step  5  execute command and verify with a pattern
    ...  console=${openbmc_mode}
    ...  command=led_location status
    ...  pattern=${get_on_pattern}
    ...  msg=Failed to verify led location!
    Step  6  execute command and verify with a pattern
    ...  console=${openbmc_mode}
    ...  command=led_location off
    ...  pattern=${set_pass_pattern}
    ...  msg=Failed to set led location!
    Step  7  execute command and verify with a pattern
    ...  console=${openbmc_mode}
    ...  command=led_location status
    ...  pattern=${get_off_pattern}
    ...  msg=Failed to verify led location!
    Step  8  verify power control  off
    Step  9  verify power status  off
    Step  10  execute command and verify with a pattern
    ...  console=${openbmc_mode}
    ...  command=led_location on
    ...  pattern=${set_fail_pattern}
    ...  is_check_exit_code=${FALSE}
    Step  11  verify power control  on
    Step  12  verify power status  on
    Step  13  execute command and verify with a pattern
    ...  console=${openbmc_mode}
    ...  command=led_location on
    ...  pattern=${set_pass_pattern}
    ...  msg=Failed to set led location!
    [Teardown]  Run Keywords  recover cpu
    ...  AND  execute command and verify exit code
    ...  console=${openbmc_mode}
    ...  command=led_location off
    ...  AND  Run Keyword And Ignore Error
    ...  change kernel log level  console=${openbmc_mode}  level=7


ALI_BMC_COMM_TC_049_ONLINE_UPDATE_FPGA_IN_BMC_OS_IN_HW_MODE
    [Documentation]  This test checks the BMC FW programming functions by updating the fpga in BMC OS
    [Tags]  ALI_BMC_COMM_TC_049_ONLINE_UPDATE_FPGA_IN_BMC_OS_IN_HW_MODE  migaloo  shamu
    [Timeout]  150 min 00 seconds
    [Setup]  Run Keywords
    ...  prepare image  ${fpga_fw_save_to}  FPGA_MULTBOOT  upgrade=True  AND
    ...  clear log  ${openbmc_mode}  ${syslog_path}
    Step  1  verify current boot flash  BMC  master
    Step  2  update fpga  isUpgrade=True
    Step  3  Run Keywords
    ...  prepare image  ${fpga_fw_save_to}  FPGA_MULTBOOT  upgrade=False  AND
    ...  clear log  ${openbmc_mode}  ${syslog_path}
    Step  4  update fpga  isUpgrade=False
    Step  5  Run Keywords
    ...  prepare image  ${fpga_fw_save_to}  FPGA_MULTBOOT  upgrade=True  AND
    ...  clear log  ${openbmc_mode}  ${syslog_path}
    Step  6  update fpga  isUpgrade=True
    [Teardown]  clean images  DUT  FPGA_MULTBOOT


ALI_BMC_COMM_TC_050_SWITCH_CHIP_POWER_CONTROL
    [Tags]  ALI_BMC_COMM_TC_050_SWITCH_CHIP_POWER_CONTROL  migaloo  shamu
    [Setup]  Run Keyword And Ignore Error
    ...  change kernel log level  console=${openbmc_mode}  level=3
    #### Ali_BMC_COMM_TC_050_1
    Step  1  check all cd ports link up status
    Step  2  load HalMisc
    Step  3  get switch chip  ${get_on_pattern}
    Step  4  set switch chip  off  ${set_pass_pattern}
    BuiltIn.Sleep  3
    Step  5  get switch chip  ${get_off_pattern}
    Step  6  check switch chip sensors  max=1
    Step  7  load HalMisc
    Step  8  set switch chip  on  ${set_pass_pattern}
    Step  9  get switch chip  ${get_on_pattern}
    Step  10  check switch chip sensors  useThreshold=${TRUE}

    #### Ali_BMC_COMM_TC_050_2
    Step  11  power cycle to openbmc
    Run Keyword And Ignore Error
    ...  change kernel log level  console=${openbmc_mode}  level=3
    Step  12  check all cd ports link up status
    Step  13  load HalMisc
    Step  14  set switch chip  off  ${set_pass_pattern}
    BuiltIn.Sleep  3
    Step  15  check switch chip sensors  max=1
    Step  16  power off and on cpu in bmc os
    Step  17  check switch chip sensors  max=1
    Step  18  load HalMisc
    Step  19  set switch chip  on  ${set_pass_pattern}
    Step  20  check switch chip sensors  useThreshold=${TRUE}
    Step  21  power off and on cpu in bmc os
    Step  22  check switch chip sensors  useThreshold=${TRUE}

    #### Ali_BMC_COMM_TC_050_3
    Step  23  load HalMisc
    Step  24  execute HalMisc command  a.get_ssd_power_status()  ${get_on_pattern}
    Step  25  execute HalMisc command  a.set_ssd_power_status("off")  ${set_pass_pattern}
    Step  26  check error messages on sonic idle state  ${ssd_off_err_pattern}
    Step  27  load HalMisc
    Step  28  execute HalMisc command  a.get_ssd_power_status()  ${get_off_pattern}
    Step  29  execute HalMisc command  a.set_ssd_power_status("on")  ${set_pass_pattern}
    Step  30  execute HalMisc command  a.get_ssd_power_status()  ${get_on_pattern}
    Step  31  check error messages on sonic idle state  ${ssd_on_err_pattern}  120
    Step  32  power cycle sonic  ${diagos_mode}

    #### Ali_BMC_COMM_TC_050_4
    Step  33  store sensors config
    Step  34  modify sensors config
    Step  35  load HalMisc
    Step  36  get switch chip  ${get_fail_pattern}
    Step  37  set switch chip  on  ${set_fail_pattern}
    Step  38  execute HalMisc command  a.get_ssd_power_status()  ${get_fail_pattern}
    Step  39  execute HalMisc command  a.set_ssd_power_status("on")  ${set_fail_pattern}
    Step  40  restore sensors config
    Step  41  load HalMisc
    Step  42  get switch chip  ${get_on_pattern}
    Step  43  set switch chip  on  ${set_pass_pattern}
    Step  44  execute HalMisc command  a.get_ssd_power_status()  ${get_on_pattern}
    Step  45  execute HalMisc command  a.set_ssd_power_status("on")  ${set_pass_pattern}

    #### Ali_BMC_COMM_TC_050_5
    Step  46  execute command and verify with unexpected patterns
    ...  console=${diagos_mode}
    ...  command=./cel-port-test -h
    ...  patterns=${regularly_unexpected_patterns}
    ...  path=${diag_cpu_path}
    ...  msg=Failed to verify by run the command!
    Step  47  execute command and verify with unexpected patterns
    ...  console=${diagos_mode}
    ...  command=${cel_port_scan_cmd}
    ...  patterns=${regularly_unexpected_patterns}
    ...  path=${diag_cpu_path}
    ...  msg=Failed to verify by run the command!
    ...  sec=180
    Step  48  execute command and verify with unexpected patterns
    ...  console=${diagos_mode}
    ...  command=${cel_port1_scan_cmd}
    ...  patterns=${regularly_unexpected_patterns}
    ...  path=${diag_cpu_path}
    ...  msg=Failed to verify by run the command!
    Step  49  execute command and verify with unexpected patterns
    ...  console=${diagos_mode}
    ...  command=${cel_port_reset_enable}
    ...  patterns=${regularly_unexpected_patterns}
    ...  path=${diag_cpu_path}
    ...  msg=Failed to verify by run the command!
    ...  sec=180
    BuiltIn.Sleep  3
    Step  50  execute command and verify with unexpected patterns
    ...  console=${diagos_mode}
    ...  command=${cel_port_reset_disable}
    ...  patterns=${regularly_unexpected_patterns}
    ...  path=${diag_cpu_path}
    ...  msg=Failed to verify by run the command!
    ...  sec=180
    BuiltIn.Sleep  3
    Step  51  execute command and verify with unexpected patterns
    ...  console=${diagos_mode}
    ...  command=${cel_port1_reset_enable}
    ...  patterns=${regularly_unexpected_patterns}
    ...  path=${diag_cpu_path}
    ...  msg=Failed to verify by run the command!
    BuiltIn.Sleep  3
    Step  52  execute command and verify with unexpected patterns
    ...  console=${diagos_mode}
    ...  command=${cel_port1_reset_disable}
    ...  patterns=${regularly_unexpected_patterns}
    ...  path=${diag_cpu_path}
    ...  msg=Failed to verify by run the command!
    BuiltIn.Sleep  3
    Run Keyword And Ignore Error
    ...  change kernel log level  console=${openbmc_mode}  level=7

    [Teardown]  Run Keyword If Test Failed  Run Keywords  switch to openbmc
    ...  AND  Run Keyword And Ignore Error  restore sensors config
    ...  AND  load HalMisc
    ...  AND  set switch chip  on  ${set_pass_pattern}
    ...  AND  execute HalMisc command
    ...  command=a.set_ssd_power_status("on")
    ...  pattern=${set_pass_pattern}
    ...  AND  open prompt  ${openbmc_mode}  30
    ...  AND  Run Keyword And Ignore Error  change kernel log level  console=${openbmc_mode}  level=7
    ...  AND  power cycle sonic  ${diagos_mode}
    ...  AND  recover cpu
    ...  AND  recover network  ###@WORKAROUND try recover network before run the auto cases, need find which case break down the network!!!

ALI_BMC_COMM_TC_056_SOL_STRESS_TEST
    [Tags]  ALI_BMC_COMM_TC_056_SOL_STRESS_TEST  migaloo  stress  shamu
    [Setup]  open prompt  console=${openbmc_mode}  sec=10
    FOR    ${INDEX}    IN RANGE    1    ${MAX_LOOP}+1
        Step  1  sol switch to sonic
        BuiltIn.Sleep  2
        Step  2  run cmd
        ...  cmd=date
        ...  prompt=${diagos_prompt}
        BuiltIn.Sleep  2
        Step  3  send a line
        ...  command=exit
        BuiltIn.Sleep  1
        Step  4  sol switch to openbmc
        BuiltIn.Sleep  1
    END
    [Teardown]  Run Keyword If Test Failed  sol switch to openbmc

ALI_BMC_COMM_TC_057_SLAVE_OPENBMC_SWAP_STRESS_TEST
    [Tags]  ALI_BMC_COMM_TC_057_SLAVE_OPENBMC_SWAP_STRESS_TEST  migaloo  stress  shamu
    [Setup]  Run Keywords  switch bmc flash  Master
             ...      AND  set test variable  ${bmcSta}  Master
    FOR    ${INDEX}    IN RANGE    1    ${MAX_LOOP}+1
        Log  ---------------Test Loop:${INDEX}, current bmc:${bmcSta}---------------
        Run Keyword And Ignore Error
        ...  change kernel log level  console=${openbmc_mode}  level=3
        Step  1  execute command and verify exit code
        ...  console=${openbmc_mode}
        ...  command=cat /etc/issue
        Step  2  verify boot info
        Step  3  execute command and verify exit code
        ...  console=${openbmc_mode}
        ...  command=ifconfig -a
        Step  4  check and swap bmc boot
    END
    [Teardown]  Run Keywords  BuiltIn.Sleep  20
                ...      AND  switch bmc flash  Master
                ...      AND  Run Keyword And Ignore Error
                ...           change kernel log level  console=${openbmc_mode}  level=7


ALI_BMC_COMM_TC_058_PSU_POWER_CONTROL
    [Tags]  ALI_BMC_COMM_TC_058_PSU_POWER_CONTROL  migaloo  shamu
    [Setup]  check and switch bios boot
    Step  1  verify power status  on
    Step  2  verify current boot flash  BIOS  master
    Step  3  execute command and verify with ordered pattern list
    ...  console=${openbmc_mode}
    ...  command=${psu_all_sensors_cmd}
    ...  patterns=${psu_all_sensors_normal_patterns}
    ...  msg=Failed to verify psu sensors!
    Step  4  execute command and verify with ordered pattern list
    ...  console=${openbmc_mode}
    ...  command=${psu_all_fru_cmd}
    ...  patterns=${psu_all_fru_normal_patterns}
    ...  msg=Failed to verify ${psu_all_fru_cmd}!
    Step  5  execute command and verify with a pattern
    ...  console=${openbmc_mode}
    ...  command=cat /tmp/powerled
    ...  pattern=green
    ...  msg=Failed to verify power led!

    Step  6  send a line
    ...  command=psu_off_on.sh -a
    Step  7  read until pattern  pattern= login:  sec=420
    Step  8  open prompt  ${openbmc_mode}  sec=10
    BuiltIn.Sleep  40
    Step  9  verify current boot flash  BMC  master
    Step  10  verify current boot flash  BIOS  master
    Step  11  execute command and verify with ordered pattern list
    ...  console=${openbmc_mode}
    ...  command=${psu_all_sensors_cmd}
    ...  patterns=${psu_all_sensors_normal_patterns}
    ...  msg=Failed to verify psu sensors!
    Step  12  execute command and verify with ordered pattern list
    ...  console=${openbmc_mode}
    ...  command=${psu_all_fru_cmd}
    ...  patterns=${psu_all_fru_normal_patterns}
    ...  msg=Failed to verify ${psu_all_fru_cmd}!
    FOR    ${psu}    IN RANGE    ${1}  ${PSU_NUM}+1
        Step  13  power off on a single psu
        ...  psu=${psu}
        ...  psu_sensor_err_patterns=${psu_${psu}_sensors_error_patterns}
    END
    [Teardown]  recover cpu

ALI_BMC_COMM_TC_059_UPDATE_POWER_IMAGE
    [Tags]  ALI_BMC_COMM_TC_059_UPDATE_POWER_IMAGE  migaloo
    [Setup]  Run Keywords  prepare image  ${loadline_path}  POWER_IMAGE_LOADLINE
             ...      AND  prepare image  ${no_loadline_path}  POWER_IMAGE_NO_LOADLINE
    #### Update loadline power image
    Step  1  execute command and verify exit code
    ...  console=${openbmc_mode}
    ...  command=systemctl stop setup_avs
    Step  2  execute command and verify with a pattern
    ...  path=${loadline_path}
    ...  console=${openbmc_mode}
    ...  command=program_xdpe132g5c.sh ${loadline_file}
    ...  pattern=Verify the power image.*OK
    ...  sec=480
    Step  3  execute command and verify exit code
    ...  console=${openbmc_mode}
    ...  command=systemctl start setup_avs
    Step  4  execute command and verify exit code
    ...  console=${openbmc_mode}
    ...  command=i2cset -f -y 17 0x40 0x00 0
    BuiltIn.Sleep  1
    Step  5  execute command and verify with a pattern
    ...  console=${openbmc_mode}
    ...  command=i2cget -f -y 17 0x40 0x28 w
    ...  pattern=(?m)^0x0008$
    ...  msg=Failed to verify value (should be 0x0008)

    #### Update no loadline power image
    Step  6  execute command and verify exit code
    ...  console=${openbmc_mode}
    ...  command=systemctl stop setup_avs
    Step  7  execute command and verify with a pattern
    ...  path=${no_loadline_path}
    ...  console=${openbmc_mode}
    ...  command=program_xdpe132g5c.sh ${no_loadline_file}
    ...  pattern=Verify the power image.*OK
    ...  sec=480
    Step  8  execute command and verify exit code
    ...  console=${openbmc_mode}
    ...  command=systemctl start setup_avs
    Step  9  execute command and verify exit code
    ...  console=${openbmc_mode}
    ...  command=i2cset -f -y 17 0x40 0x00 0
    BuiltIn.Sleep  1
    Step  10  execute command and verify with a pattern
    ...  console=${openbmc_mode}
    ...  command=i2cget -f -y 17 0x40 0x28 w
    ...  pattern=(?m)^0x0000$
    ...  msg=Failed to verify value (should be 0x0000)
    [Teardown]  Run Keywords  change dir  ${EMPTY}  ${openbmc_mode}
                ...      AND  clean images  DUT  POWER_IMAGE_LOADLINE
                ...      AND  clean images  DUT  POWER_IMAGE_NO_LOADLINE
                ...      AND  Run Keyword If Test Failed  execute command and verify exit code
                              ...  console=${openbmc_mode}
                              ...  command=systemctl start setup_avs
                ...      AND  recover cpu

ALI_BMC_COMM_TC_060_CHECK_SENSORS_PXE_1311_WHEN_DIFFERENT_PROCESSES_ACCESS
    [Tags]  ALI_BMC_COMM_TC_060_CHECK_SENSORS_PXE_1311_WHEN_DIFFERENT_PROCESSES_ACCESS  migaloo
    Step  1  execute command and verify exit code
    ...  path=/home/root/
    ...  console=${openbmc_mode}
    ...  command=echo '${test1_script}' > test1.sh
    Step  2  execute command and verify exit code
    ...  path=/home/root/
    ...  console=${openbmc_mode}
    ...  command=echo '${test2_script}' > test2.sh
    Step  3  execute command and verify exit code
    ...  console=${openbmc_mode}
    ...  command=cat test1.sh test2.sh
    Step  4  execute command and verify exit code
    ...  console=${openbmc_mode}
    ...  command=chmod +x test1.sh test2.sh
    Step  5  send cmd regexp
    ...  cmd=./test1.sh &
    ...  promptRegexp=(?mi)^\\\\[\\\\d+\\\\]\\\\s*(?P<ps_id>\\\\d+)
    ...  timeout=10
    Step  6  send cmd regexp
    ...  cmd=./test2.sh &
    ...  promptRegexp=(?mi)^\\\\[\\\\d+\\\\]\\\\s*(?P<ps_id>\\\\d+)
    ...  timeout=10
    Step  7  keep reading sensors
    ...  sensor_name=pxe1311-i2c-16-0e
    ...  timeout=180

    [Teardown]  Run Keywords  kill script  test1
                ...      AND  kill script  test2
                ...      AND  remove file/folder
                              ...  console=${openbmc_mode}
                              ...  file=test1.sh test2.sh

ALI_BMC_COMM_TC_061_TRIGGER_THE_POWER_RETRY_FUNCTION
    [Tags]  ALI_BMC_COMM_TC_061_TRIGGER_THE_POWER_RETRY_FUNCTION  migaloo  shamu
    [Setup]  Run Keywords  clear log  ${openbmc_mode}  ${syslog_path}
             ...      AND  execute command and set test variable
                           ...  console=${openbmc_mode}
                           ...  command=cp ${board_util_script} board-util-store.sh
    Step  1  open prompt  console=${openbmc_mode}  sec=300
    Step  2  file edit and replace a line
        ...  console=${openbmc_mode}
        ...  file=${board_util_script}
        ...  sed_pattern=s/${board_util_old_str}/${board_util_new_str}/
    Step  3  execute command and verify exit code
    ...  console=${openbmc_mode}
    ...  command=cat ${board_util_script} | grep '${board_util_new_str}'
    Step  4  execute command and verify with a pattern
    ...  console=${openbmc_mode}
    ...  command=wedge_power.sh off
    ...  pattern=(?mi)Power off microserver.*[\\\\d+s]?(.|\\\\\n)*(?P<power_off_result>Failed)
    ...  msg=power off should be failed
    ...  sec=300
    ...  is_check_exit_code=${FALSE}
    Step  5  execute command and verify with ordered pattern list
    ...  console=${openbmc_mode}
    ...  command=cat ${syslog_path} | grep -i "power off micro-server"
    ...  patterns=${power_off_fail_log_patterns}
    ...  msg=Failed to verify ${syslog_path}!
    Step  6  BuiltIn.Sleep  90
    Step  7  verify power status  off
    Step  8  cpu should off
    Step  9  verify power control  on
    [Teardown]  Run Keywords  switch to openbmc
                ...      AND  execute command and set test variable
                              ...  console=${openbmc_mode}
                              ...  command=cp board-util-store.sh ${board_util_script}
                ...      AND  recover cpu


ALI_BMC_AUTO_TC_001_OPENBMC_REBOOT
    [Tags]  ALI_BMC_AUTO_TC_001_OPENBMC_REBOOT  migaloo  shamu
    [Setup]  wait bmc restful

    Step  1  execute command and verify with a pattern
    ...  console=${diagos_mode}
    ...  command=${auto_test_cmd} test_bmcutil.TestBMCUtil.test_reboot_bmc
    ...  path=${auto_test_dir}
    ...  pattern=(?m)^[ \\\\t]*OK[ \\\\t]*$
    ...  msg=Failed to run test_reboot_bmc
    ...  sec=600
    [Teardown]  recover network   ###@WORKAROUND try recover network before run the auto cases, need find which case break down the network!!!

ALI_BMC_AUTO_TC_002_OPENBMC_INFO
    [Tags]  ALI_BMC_AUTO_TC_002_OPENBMC_INFO  migaloo  shamu
    [Setup]  wait bmc restful

    Step  1  execute command and verify with a pattern
    ...  console=${diagos_mode}
    ...  command=${auto_test_cmd} test_fwmgrutil.TestFirmwareUtil.test_get_bmc_version
    ...  path=${auto_test_dir}
    ...  pattern=(?m)^[ \\\\t]*OK[ \\\\t]*$
    ...  msg=Failed to run test_get_bmc_version
    ...  sec=30

ALI_BMC_AUTO_TC_003_OPENBMC_CURRENT_BOOT_SOURCE
    [Tags]  ALI_BMC_AUTO_TC_003_OPENBMC_CURRENT_BOOT_SOURCE  migaloo  shamu
    [Setup]  wait bmc restful

    Step  1  execute command and verify with a pattern
    ...  console=${diagos_mode}
    ...  command=${auto_test_cmd} test_fwmgrutil.TestFirmwareUtil.test_get_running_bmc
    ...  path=${auto_test_dir}
    ...  pattern=(?m)^[ \\\\t]*OK[ \\\\t]*$
    ...  msg=Failed to run test_get_running_bmc
    ...  sec=30

ALI_BMC_AUTO_TC_005_SET_OPENBMC_NEXT_BOOT
    [Documentation]  This test cover case ALI_BMC_AUTO_TC_004_GET_OPENBMC_NEXT_BOOT
    [Tags]  ALI_BMC_AUTO_TC_005_SET_OPENBMC_NEXT_BOOT  migaloo  shamu
    [Setup]  wait bmc restful

    Step  1  execute command and verify with a pattern
    ...  console=${diagos_mode}
    ...  command=${auto_test_cmd} test_fwmgrutil.TestFirmwareUtil.test_set_bmc_boot_flash
    ...  path=${auto_test_dir}
    ...  pattern=(?m)^[ \\\\t]*OK[ \\\\t]*$
    ...  msg=Failed to run test_set_bmc_boot_flash
    ...  sec=800

ALI_BMC_AUTO_TC_006_GET_CPLD_VERSION
    [Tags]  ALI_BMC_AUTO_TC_006_GET_CPLD_VERSION
    ...  migaloo
    ...  shamu
    [Setup]  wait bmc restful

    Step  1  execute command and verify with a pattern
    ...  console=${diagos_mode}
    ...  command=${auto_test_cmd} test_fwmgrutil.TestFirmwareUtil.test_get_cpld_version
    ...  path=${auto_test_dir}
    ...  pattern=(?m)^[ \\\\t]*OK[ \\\\t]*$
    ...  msg=Failed to run test_get_cpld_version
    ...  sec=30


ALI_BMC_AUTO_TC_007_GET_BIOS_VERSION
    [Tags]  ALI_BMC_AUTO_TC_007_GET_BIOS_VERSION
    ...  migaloo
    ...  shamu
    [Setup]  wait bmc restful

    Step  1  execute command and verify with a pattern
    ...  console=${diagos_mode}
    ...  command=${auto_test_cmd} test_fwmgrutil.TestFirmwareUtil.test_get_bios_version
    ...  path=${auto_test_dir}
    ...  pattern=(?m)^[ \\\\t]*OK[ \\\\t]*$
    ...  msg=Failed to run test_get_bios_version
    ...  sec=30

ALI_BMC_AUTO_TC_008_GET_BIOS_NEXT_BOOT
    [Tags]  ALI_BMC_AUTO_TC_008_GET_BIOS_NEXT_BOOT  migaloo  shamu
    [Setup]  wait bmc restful

    Step  1  execute command and verify with a pattern
    ...  console=${diagos_mode}
    ...  command=${auto_test_cmd} test_fwmgrutil.TestFirmwareUtil.test_get_bios_next_boot
    ...  path=${auto_test_dir}
    ...  pattern=(?m)^[ \\\\t]*OK[ \\\\t]*$
    ...  msg=Failed to run test_get_bios_next_boot
    ...  sec=30

ALI_BMC_AUTO_TC_009_SET_BIOS_NEXT_BOOT
    [Tags]  ALI_BMC_AUTO_TC_008_SET_BIOS_NEXT_BOOT  migaloo  shamu
    [Setup]  wait bmc restful

    Step  1  execute command and verify with a pattern
    ...  console=${diagos_mode}
    ...  command=${auto_test_cmd} test_fwmgrutil.TestFirmwareUtil.test_set_bios_next_boot
    ...  path=${auto_test_dir}
    ...  pattern=(?m)^[ \\\\t]*OK[ \\\\t]*$
    ...  msg=Failed to run test_set_bios_next_boot
    ...  sec=30

ALI_BMC_AUTO_TC_012_BIOS_UPDATE_CURRENT_MASTER_UPDATE_BOTH
    [Tags]  ALI_BMC_AUTO_TC_012_BIOS_UPDATE_CURRENT_MASTER_UPDATE_BOTH
    ...  migaloo
    ...  shamu
    [Setup]  wait bmc restful

    Step  1  execute command and verify with a pattern
    ...  console=${diagos_mode}
    ...  command=${auto_test_cmd} test_fwmgrutil.TestFirmwareUtil.test_program_bios_master
    ...  path=${auto_test_dir}
    ...  pattern=(?m)^[ \\\\t]*OK[ \\\\t]*$
    ...  msg=Failed to run test_program_bios_master
    ...  sec=900

ALI_BMC_AUTO_TC_015_BIOS_UPDATE_CURRENT_SLAVE_UPDATE_BOTH
    [Tags]  ALI_BMC_AUTO_TC_015_BIOS_UPDATE_CURRENT_SLAVE_UPDATE_BOTH
    ...  migaloo
    ...  shamu
    [Setup]  wait bmc restful

    Step  1  execute command and verify with a pattern
    ...  console=${diagos_mode}
    ...  command=${auto_test_cmd} test_fwmgrutil.TestFirmwareUtil.test_program_bios_slave
    ...  path=${auto_test_dir}
    ...  pattern=(?m)^[ \\\\t]*OK[ \\\\t]*$
    ...  msg=Failed to run test_program_bios_slave
    ...  sec=900

ALI_BMC_AUTO_TC_016_OPENBMC_UPDATE_CURRENT_MASTER
    [Tags]  ALI_BMC_AUTO_TC_016_OPENBMC_UPDATE_CURRENT_MASTER
    ...  migaloo  long_time  shamu
    [Setup]  wait bmc restful

    Step  1  execute command and verify with a pattern
    ...  console=${diagos_mode}
    ...  command=${auto_test_cmd} test_fwmgrutil.TestFirmwareUtil.test_program_bmc_master
    ...  path=${auto_test_dir}
    ...  pattern=(?m)^[ \\\\t]*OK[ \\\\t]*$
    ...  msg=Failed to run test_program_bmc_master
    ...  sec=6000

ALI_BMC_AUTO_TC_020_OPENBMC_UPDATE_CURRENT_SLAVE
    [Tags]  ALI_BMC_AUTO_TC_020_OPENBMC_UPDATE_CURRENT_SLAVE
    ...  migaloo  long_time  shamu
    [Setup]  wait bmc restful

    Step  1  execute command and verify with a pattern
    ...  console=${diagos_mode}
    ...  command=${auto_test_cmd} test_fwmgrutil.TestFirmwareUtil.test_program_bmc_slave
    ...  path=${auto_test_dir}
    ...  pattern=(?m)^[ \\\\t]*OK[ \\\\t]*$
    ...  msg=Failed to run test_program_bmc_slave
    ...  sec=6000

ALI_BMC_AUTO_TC_024_GET_FAN_INFO
    [Tags]  ALI_BMC_AUTO_TC_024_GET_FAN_INFO
    ...  migaloo  shamu
    [Setup]  wait bmc restful

    Step  1  execute command and verify with a pattern
    ...  console=${diagos_mode}
    ...  command=${auto_test_cmd} test_platformutil.TestPlatformUtil.test_fan_info
    ...  path=${auto_test_dir}
    ...  pattern=(?m)^[ \\\\t]*OK[ \\\\t]*$
    ...  msg=Failed to run test_fan_info
    ...  sec=30


ALI_BMC_AUTO_TC_025_GET_PSU_INFO
    [Tags]  ALI_BMC_AUTO_TC_025_GET_PSU_INFO
    ...  migaloo  shamu
    [Setup]  wait bmc restful

    Step  1  execute command and verify with a pattern
    ...  console=${diagos_mode}
    ...  command=${auto_test_cmd} test_platformutil.TestPlatformUtil.test_psu_info
    ...  path=${auto_test_dir}
    ...  pattern=(?m)^[ \\\\t]*OK[ \\\\t]*$
    ...  msg=Failed to run test_psu_info
    ...  sec=30


ALI_BMC_AUTO_TC_026_GET_SENSOR_INFO
    [Tags]  ALI_BMC_AUTO_TC_026_GET_SENSOR_INFO
    ...  migaloo  shamu
    [Setup]  wait bmc restful

    Step  1  execute command and verify with a pattern
    ...  console=${diagos_mode}
    ...  command=${auto_test_cmd} test_platformutil.TestPlatformUtil.test_sensor_info
    ...  path=${auto_test_dir}
    ...  pattern=(?m)^[ \\\\t]*OK[ \\\\t]*$
    ...  msg=Failed to run test_sensor_info
    ...  sec=30


ALI_BMC_AUTO_TC_027_GET_LOCATION_LED_STATUS
    [Tags]  ALI_BMC_AUTO_TC_027_GET_LOCATION_LED_STATUS
    ...  migaloo  shamu
    [Setup]  wait bmc restful

    Step  1  execute command and verify with a pattern
    ...  console=${diagos_mode}
    ...  command=${auto_test_cmd} test_bmcutil.TestBMCUtil.test_get_location_led
    ...  path=${auto_test_dir}
    ...  pattern=(?m)^[ \\\\t]*OK[ \\\\t]*$
    ...  msg=Failed to run test_get_location_led
    ...  sec=30


ALI_BMC_AUTO_TC_028_SET_LOCATION_LED_STATUS
    [Tags]  ALI_BMC_AUTO_TC_028_SET_LOCATION_LED_STATUS
    ...  migaloo  shamu
    [Setup]  wait bmc restful

    Step  1  execute command and verify with a pattern
    ...  console=${diagos_mode}
    ...  command=${auto_test_cmd} test_bmcutil.TestBMCUtil.test_set_location_led
    ...  path=${auto_test_dir}
    ...  pattern=(?m)^[ \\\\t]*OK[ \\\\t]*$
    ...  msg=Failed to run test_set_location_led
    ...  sec=40


ALI_BMC_AUTO_TC_029_ARBITRARY_COMMANDS
    [Tags]  ALI_BMC_AUTO_TC_029_ARBITRARY_COMMANDS
    ...  migaloo  shamu
    [Setup]  wait bmc restful

    Step  1  execute command and verify with a pattern
    ...  console=${diagos_mode}
    ...  command=${auto_test_cmd} test_bmcutil.TestBMCUtil.test_arbitrary_commands
    ...  path=${auto_test_dir}
    ...  pattern=(?m)^[ \\\\t]*OK[ \\\\t]*$
    ...  msg=Failed to run test_arbitrary_commands
    ...  sec=30


ALI_BMC_AUTO_TC_030_POWER_CYCLE_COME
    [Tags]  ALI_BMC_AUTO_TC_030_POWER_CYCLE_COME
    ...  migaloo  shamu
    [Setup]  Run Keywords
    ...  set skip reboot cpu  False  AND
    ...  wait bmc restful

    Step  1  execute command and verify exit code
    ...  console=${diagos_mode}
    ...  command=${auto_test_export_cmd}
    Step  2  exe autotest and wait system reboot
    ...  option=test_bmcutil.TestBMCUtil.test_power_cycle_cpu
    [Teardown]  Run Keywords  recover cpu  AND  BuiltIn.Sleep  30


ALI_BMC_AUTO_TC_031_POWER_CYCLE_COME_AND_REBOOT_OPENBMC
    [Tags]  ALI_BMC_AUTO_TC_031_POWER_CYCLE_COME_AND_REBOOT_OPENBMC
    ...  migaloo  shamu
    [Setup]  Run Keywords
    ...  set skip reboot cpu  False  AND
    ...  wait bmc restful

    Step  1  execute command and verify exit code
    ...  console=${diagos_mode}
    ...  command=${auto_test_export_cmd}
    Step  2  exe autotest and wait system reboot
    ...  option=test_bmcutil.TestBMCUtil.test_power_cycle_system
    [Teardown]  Run Keywords  recover cpu  AND  BuiltIn.Sleep  ${auto_test_delay}


ALI_BMC_AUTO_TC_032_REFRESH_BIOS
    [Tags]  ALI_BMC_AUTO_TC_032_REFRESH_BIOS
    ...  migaloo  shamu
    [Setup]  Run Keywords
    ...  set skip reboot cpu  False  AND
    ...  clear log  ${openbmc_mode}  ${syslog_path}  AND
    ...  wait bmc restful

    Step  1  execute command and verify exit code
    ...  console=${diagos_mode}
    ...  command=${auto_test_export_cmd}
    Step  2  exe autotest and wait system reboot
    ...  option=test_fwmgrutil_refresh.TestFirmwareRefreshUtil.test_firmware_refresh_bios
    ...  timeout=300
    Step  3  execute command and verify with ordered pattern list
    ...  console=${openbmc_mode}
    ...  command=${refresh_fw_log_cmd}
    ...  patterns=${refresh_fw_log_patterns}
    ...  msg=Failed to verify ${refresh_fw_log_cmd}!
    [Teardown]  Run Keywords  recover cpu  AND  BuiltIn.Sleep  ${auto_test_delay}
    ...  AND  Run Keyword If Test Failed  execute command  ${refresh_fw_log_cmd}  ${openbmc_mode}


ALI_BMC_AUTO_TC_033_REFRESH_FPGA
    [Tags]  ALI_BMC_AUTO_TC_033_REFRESH_FPGA
    ...  migaloo  shamu
    [Setup]  Run Keywords
    ...  set skip reboot cpu  False  AND
    ...  clear log  ${diagos_mode}  ${fwlog_path}  AND
    ...  clear log  ${openbmc_mode}  ${syslog_path}  AND
    ...  wait bmc restful

    Step  1  execute command and verify exit code
    ...  console=${diagos_mode}
    ...  command=${auto_test_export_cmd}
    Step  2  exe autotest and wait system reboot
    ...  option=test_fwmgrutil_refresh.TestFirmwareRefreshUtil.test_firmware_refresh_fpga
    ...  timeout=300
    Step  3  execute command and verify with ordered pattern list
    ...  console=${diagos_mode}
    ...  command=${upgrade_fw_log_cmd}
    ...  patterns=${upgrade_fpga_log_patterns}
    ...  msg=Failed to verify ${upgrade_fw_log_cmd}!
    Step  4  execute command and verify with ordered pattern list
    ...  console=${openbmc_mode}
    ...  command=${refresh_fw_log_cmd}
    ...  patterns=${refresh_fw_log_patterns}
    ...  msg=Failed to verify ${refresh_fw_log_cmd}!
    [Teardown]  Run Keywords  recover cpu  AND  BuiltIn.Sleep  ${auto_test_delay}
    ...  AND  Run Keyword If Test Failed  execute command  ${refresh_fw_log_cmd}  ${openbmc_mode}

ALI_BMC_AUTO_TC_034_UPDATE_AND_REFRESH_BASE_CPLD
    [Tags]  ALI_BMC_AUTO_TC_034_UPDATE_AND_REFRESH_BASE_CPLD
    ...  migaloo  shamu
    [Setup]  Run Keywords
    ...  set skip reboot cpu  False  AND
    ...  clear log  ${diagos_mode}  ${fwlog_path}  AND
    ...  clear log  ${openbmc_mode}  ${syslog_path}  AND
    ...  wait bmc restful
    Step  1  prepare autotest cplds
    Step  2  execute command and verify exit code
    ...  console=${diagos_mode}
    ...  command=${auto_test_export_cmd}
    Step  3  exe autotest and wait system reboot
    ...  option=test_fwmgrutil_refresh.TestFirmwareRefreshUtil.test_firmware_refresh_base_cpld
    ...  timeout=600
    Step  4  execute command and verify with ordered pattern list
    ...  console=${diagos_mode}
    ...  command=${upgrade_fw_log_cmd}
    ...  patterns=${upgrade_base_log_patterns}
    ...  msg=Failed to verify ${upgrade_fw_log_cmd}!
    Step  5  execute command and verify with ordered pattern list
    ...  console=${openbmc_mode}
    ...  command=${refresh_cpld_log_cmd}
    ...  patterns=${refresh_base_log_patterns}
    ...  msg=Failed to verify ${refresh_cpld_log_cmd}!
    [Teardown]  Run Keywords  recover cpu  AND  BuiltIn.Sleep  ${auto_test_delay}
    ...  AND  Run Keyword If Test Failed  execute command  ${upgrade_fw_log_cmd}  ${diagos_mode}
    ...  AND  Run Keyword If Test Failed  execute command  ${refresh_cpld_log_cmd}  ${openbmc_mode}

ALI_BMC_AUTO_TC_035_UPDATE_AND_REFRESH_FAN_CPLD
    [Tags]  ALI_BMC_AUTO_TC_035_UPDATE_AND_REFRESH_FAN_CPLD
    ...  migaloo  shamu
    [Setup]  Run Keywords
    ...  set skip reboot cpu  False  AND
    ...  clear log  ${diagos_mode}  ${fwlog_path}  AND
    ...  clear log  ${openbmc_mode}  ${syslog_path}  AND
    ...  wait bmc restful
    Step  1  prepare autotest cplds
    Step  2  execute command and verify exit code
    ...  console=${diagos_mode}
    ...  command=${auto_test_export_cmd}
    Step  3  exe autotest and wait system reboot
    ...  option=test_fwmgrutil_refresh.TestFirmwareRefreshUtil.test_firmware_refresh_fan_cpld
    ...  timeout=600
    Step  4  execute command and verify with ordered pattern list
    ...  console=${diagos_mode}
    ...  command=${upgrade_fw_log_cmd}
    ...  patterns=${upgrade_fan_log_patterns}
    ...  msg=Failed to verify ${upgrade_fw_log_cmd}!
    Step  5  execute command and verify with ordered pattern list
    ...  console=${openbmc_mode}
    ...  command=${refresh_cpld_log_cmd}
    ...  patterns=${refresh_fan_log_patterns}
    ...  msg=Failed to verify ${refresh_cpld_log_cmd}!
    [Teardown]  Run Keywords  recover cpu  AND  BuiltIn.Sleep  ${auto_test_delay}
    ...  AND  Run Keyword If Test Failed  execute command  ${upgrade_fw_log_cmd}  ${diagos_mode}
    ...  AND  Run Keyword If Test Failed  execute command  ${refresh_cpld_log_cmd}  ${openbmc_mode}

ALI_BMC_AUTO_TC_036_UPDATE_COME_CPLD
    [Tags]  ALI_BMC_AUTO_TC_036_UPDATE_COME_CPLD
    ...  migaloo  shamu
    [Setup]  Run Keywords
    ...  set skip reboot cpu  False  AND
    ...  clear log  ${diagos_mode}  ${fwlog_path}  AND
    ...  clear log  ${openbmc_mode}  ${syslog_path}  AND
    ...  wait bmc restful
    Step  1  prepare autotest cplds
    Step  2  execute command and verify exit code
    ...  console=${diagos_mode}
    ...  command=${auto_test_export_cmd}
    Step  3  exe autotest and wait system reboot
    ...  option=test_fwmgrutil_refresh.TestFirmwareRefreshUtil.test_firmware_refresh_cpu_cpld
    ...  timeout=600
    Step  4  execute command and verify with ordered pattern list
    ...  console=${diagos_mode}
    ...  command=${upgrade_fw_log_cmd}
    ...  patterns=${upgrade_cpu_log_patterns}
    ...  msg=Failed to verify ${upgrade_fw_log_cmd}!
    Step  5  execute command and verify with ordered pattern list
    ...  console=${openbmc_mode}
    ...  command=${refresh_cpld_log_cmd}
    ...  patterns=${refresh_cpu_log_patterns}
    ...  msg=Failed to verify ${refresh_cpld_log_cmd}!
    [Teardown]  Run Keywords  recover cpu  AND  BuiltIn.Sleep  ${auto_test_delay}
    ...  AND  Run Keyword If Test Failed  execute command  ${upgrade_fw_log_cmd}  ${diagos_mode}
    ...  AND  Run Keyword If Test Failed  execute command  ${refresh_cpld_log_cmd}  ${openbmc_mode}

ALI_BMC_AUTO_TC_037_UPDATE_SWITCH_1_AND_2_CPLD
    [Tags]  ALI_BMC_AUTO_TC_037_UPDATE_SWITCH_1_AND_2_CPLD
    ...  migaloo  shamu
    [Setup]  Run Keywords
    ...  set skip reboot cpu  False  AND
    ...  clear log  ${diagos_mode}  ${fwlog_path}  AND
    ...  clear log  ${openbmc_mode}  ${syslog_path}  AND
    ...  wait bmc restful
    Step  1  prepare autotest cplds
    Step  2  execute command and verify exit code
    ...  console=${diagos_mode}
    ...  command=${auto_test_export_cmd}
    Step  3  exe autotest and wait system reboot
    ...  option=test_fwmgrutil_refresh.TestFirmwareRefreshUtil.test_firmware_refresh_cpld1
    ...  timeout=600
    Step  4  execute command and verify with ordered pattern list
    ...  console=${diagos_mode}
    ...  command=${upgrade_fw_log_cmd}
    ...  patterns=${upgrade_sw1_log_patterns}
    ...  msg=Failed to verify ${upgrade_fw_log_cmd}!
    Step  5  execute command and verify with ordered pattern list
    ...  console=${openbmc_mode}
    ...  command=${refresh_cpld_log_cmd}
    ...  patterns=${refresh_fw_log_patterns}
    ...  msg=Failed to verify ${refresh_cpld_log_cmd}!
    [Teardown]  Run Keywords  recover cpu  AND  BuiltIn.Sleep  ${auto_test_delay}
    ...  AND  Run Keyword If Test Failed  execute command  ${upgrade_fw_log_cmd}  ${diagos_mode}
    ...  AND  Run Keyword If Test Failed  execute command  ${refresh_cpld_log_cmd}  ${openbmc_mode}

ALI_BMC_AUTO_TC_038_UPDATE_BUTTOM_LINECARD_1_AND_2_CPLD
    [Tags]  ALI_BMC_AUTO_TC_038_UPDATE_BUTTOM_LINECARD_1_AND_2_CPLD
    ...  migaloo
    [Setup]  Run Keywords
    ...  set skip reboot cpu  False  AND
    ...  clear log  ${diagos_mode}  ${fwlog_path}  AND
    ...  clear log  ${openbmc_mode}  ${syslog_path}  AND
    ...  wait bmc restful
    Step  1  prepare autotest cplds
    Step  2  execute command and verify exit code
    ...  console=${diagos_mode}
    ...  command=${auto_test_export_cmd}
    Step  3  exe autotest and wait system reboot
    ...  option=test_fwmgrutil_refresh.TestFirmwareRefreshUtil.test_firmware_refresh_cpld2
    ...  timeout=600
    Step  4  execute command and verify with ordered pattern list
    ...  console=${diagos_mode}
    ...  command=${upgrade_fw_log_cmd}
    ...  patterns=${upgrade_sw2_log_patterns}
    ...  msg=Failed to verify ${upgrade_fw_log_cmd}!
    Step  5  execute command and verify with ordered pattern list
    ...  console=${openbmc_mode}
    ...  command=${refresh_cpld_log_cmd}
    ...  patterns=${refresh_fw_log_patterns}
    ...  msg=Failed to verify ${refresh_cpld_log_cmd}!
    [Teardown]  Run Keywords  recover cpu  AND  BuiltIn.Sleep  ${auto_test_delay}
    ...  AND  Run Keyword If Test Failed  execute command  ${upgrade_fw_log_cmd}  ${diagos_mode}
    ...  AND  Run Keyword If Test Failed  execute command  ${refresh_cpld_log_cmd}  ${openbmc_mode}

ALI_BMC_AUTO_TC_039_UPDATE_TOP_LINECARD_1_AND_2_CPLD
    [Tags]  ALI_BMC_AUTO_TC_039_UPDATE_TOP_LINECARD_1_AND_2_CPLD
    ...  migaloo
    [Setup]  Run Keywords
    ...  set skip reboot cpu  False  AND
    ...  clear log  ${diagos_mode}  ${fwlog_path}  AND
    ...  clear log  ${openbmc_mode}  ${syslog_path}  AND
    ...  wait bmc restful
    Step  1  prepare autotest cplds
    Step  2  execute command and verify exit code
    ...  console=${diagos_mode}
    ...  command=${auto_test_export_cmd}
    Step  3  exe autotest and wait system reboot
    ...  option=test_fwmgrutil_refresh.TestFirmwareRefreshUtil.test_firmware_refresh_cpld_tplc
    ...  timeout=600
    Step  4  execute command and verify with ordered pattern list
    ...  console=${diagos_mode}
    ...  command=${upgrade_fw_log_cmd}
    ...  patterns=${upgrade_tplc_log_patterns}
    ...  msg=Failed to verify ${upgrade_fw_log_cmd}!
    Step  5  execute command and verify with ordered pattern list
    ...  console=${openbmc_mode}
    ...  command=${refresh_cpld_log_cmd}
    ...  patterns=${refresh_fw_log_patterns}
    ...  msg=Failed to verify ${refresh_cpld_log_cmd}!
    [Teardown]  Run Keywords  recover cpu  AND  BuiltIn.Sleep  ${auto_test_delay}
    ...  AND  Run Keyword If Test Failed  execute command  ${upgrade_fw_log_cmd}  ${diagos_mode}
    ...  AND  Run Keyword If Test Failed  execute command  ${refresh_cpld_log_cmd}  ${openbmc_mode}

ALI_BMC_AUTO_TC_040_UPDATE_ALL_CPLD_AND_REFRESH_BASE_AND_FAN_CPLD
    [Tags]  ALI_BMC_AUTO_TC_040_UPDATE_ALL_CPLD_AND_REFRESH_BASE_AND_FAN_CPLD
    ...  migaloo  shamu

    # This test-case is pending to....
    # Maxwill Ma said:
    # It known issue, while refresh CPLD on OpenBMC.

    # Turn SKIP_REBOOT_CPU to False to perform test/reboot action
    [Setup]  run keywords
    ...  execute command and verify exit code
    ...  console=${diagos_mode}
    ...  path=${auto_test_dir}
    ...  command=sed -ir 's/SKIP_REBOOT_CPU.*$/SKIP_REBOOT_CPU = False/g' unittest_config.py  AND
    ...  clear log  ${diagos_mode}  ${fwlog_path}  AND
    ...  clear log  ${openbmc_mode}  ${syslog_path}  AND
    ...  wait bmc restful

    Step  1  prepare autotest cplds
    Step  2  execute command and verify exit code
    ...  console=${diagos_mode}
    ...  command=${auto_test_export_cmd}
    Step  3  exe autotest and wait system reboot
    ...  option=test_fwmgrutil_refresh.TestFirmwareRefreshUtil.test_firmware_refresh_cpld
    ...  timeout=1800
    Step  4  execute command and verify with unordered pattern list
    ...  console=${diagos_mode}
    ...  command=${upgrade_fw_log_cmd}
    ...  patterns=${auto_fw_refresh_cpld_patterns}
    ...  msg=Failed to verify ${upgrade_fw_log_cmd}!
    Step  5  execute command and verify with unordered pattern list
    ...  console=${openbmc_mode}
    ...  command=${refresh_cpld_log_cmd}
    ...  patterns=${auto_fw_refresh_cpld_openbmc_patterns}
    ...  msg=Failed to verify ${refresh_cpld_log_cmd}!
    [Teardown]  Run keywords  recover cpu
    ...  AND  recover network   ## @WORKAROUND @NEED_CHECK_FURTHER, this case will break down the network, only power cycle can recover it.
    ...  AND  Run Keyword If Test Failed  execute command  ${upgrade_fw_log_cmd}  ${diagos_mode}
    ...  AND  Run Keyword If Test Failed  execute command  ${refresh_cpld_log_cmd}  ${openbmc_mode}

*** Keywords ***
Bmc Connect Device
    BmcConnect
    prepare autotest images

Bmc Disconnect Device
    BmcDisconnect
