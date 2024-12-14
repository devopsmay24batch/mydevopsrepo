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
#######################################################################################################################
# Script       : Openbmc_keywords.robot                                                                               #
# Date         : February 24, 2020                                                                                    #
# Author       : Prapatsorn W. <pwisutti@celestica.com>                                                               #
# Description  : This script used as keywords in Openbmc_test.robot                                                   #
#                                                                                                                     #
# Script Revision Details:                                                                                            #
#   Initial Draft for openbmc testing                                                                                 #
#######################################################################################################################

*** Settings ***
Variables         Openbmc_variable.py
Library           openbmc_lib.py
Library           bios_menu_lib.py
Library           CommonLib.py
Library           OperatingSystem

*** Keywords ***

go to openbmc
  switch to openbmc

go to centos
  switch to centos

reboot device
  reboot  mode=openbmc

reboot diag os
  reboot  mode=centos

update TH3
  [Arguments]  ${package_file}  ${th3_version}
  online update th3  DUT  package_file=${package_file}  package_file_path=${workspace}/TH3
  powercycle device
  verify TH3 version  DUT  ${th3_version}

ping PC from BMC
  ${ip} =  get ip address from config  PC
  exec_ping  DUT  ipAddress=${ip}  count=5  mode=${OPENBMC_MODE}

ping PC from CPU
  ${ip} =  get ip address from config  PC
  exec_ping  DUT  ipAddress=${ip}  count=5  mode=${CENTOS_MODE}

ping CPU from BMC
  [Arguments]  ${ip}
  exec_ping  DUT  ipAddress=${ip}  count=5  mode=${OPENBMC_MODE}

ping BMC from CPU
  [Arguments]  ${ip}
  exec_ping  DUT  ipAddress=${ip}  count=5  mode=${CENTOS_MODE}

ping BMC and CPU from PC
  [Arguments]  ${bmc_ip}  ${cpu_ip}
  exec_ping  PC  ipAddress=${bmc_ip}  count=5  mode=None
  exec_ping  PC  ipAddress=${cpu_ip}  count=5  mode=None

copy file from BMC to CPU ipv6
  [Arguments]  ${ip}  ${filepath}  ${filename}  ${destination_path}  ${interface}
  Step  1  go to openbmc
  Step  2  create dir  path=${filepath}  mode=${OPENBMC_MODE}
  Step  3  create test file  DUT  filename=${filepath}/${filename}  size_MB=${usb0_test_size_mb}
  Step  4  copy files from bmc to cpu  DUT  cpu_ip=${ip}  filename=${filename}  filepath=${filepath}
              ...  destination_path=${destination_path}  size_MB=${usb0_test_size_mb}
              ...  swap=True  ipv6=True  interface=${interface}

clean up file on both bmc and cpu
  Step  1  clean up file  DUT  files=/home/${usb0_test_file}  mode=${CENTOS_MODE}
  Step  2  clean up file  DUT  files=${workspace}/${usb0_test_file}  mode=${OPENBMC_MODE}

clean up file on both bmc and cpu and ssh disconnect
  Step  1  clean up file on both bmc and cpu
  Step  2  ssh disconnect  DUT

ping6 PC from BMC
  [Arguments]  ${ip}  ${interface}
  exec_ping6  DUT  interface=${interface}  ipAddress=${ip}  count=5  mode=${OPENBMC_MODE}

ping6 PC from CPU
  [Arguments]  ${ip}  ${interface}
  exec_ping6  DUT  interface=${interface}  ipAddress=${ip}  count=5  mode=${CENTOS_MODE}

ping6 CPU from BMC
  [Arguments]  ${ip}  ${interface}
  exec_ping6  DUT  interface=${interface}  ipAddress=${ip}  count=5  mode=${OPENBMC_MODE}

ping6 BMC from CPU
  [Arguments]  ${ip}  ${interface}
  exec_ping6  DUT  interface=${interface}  ipAddress=${ip}  count=5  mode=${CENTOS_MODE}

ping BMC from PC
  [Arguments]  ${bmc_ip}
#  ping it from cap server directly, do not ssh cap server firstly
  exec local ping  ipAddress=${bmc_ip}  count=5  mode=None

ping6 BMC from PC
  [Arguments]  ${bmc_ip}  ${interface}
  exec_ping6  PC  interface=${interface}  ipAddress=${bmc_ip}  count=5  mode=None

ping6 CPU from PC
  [Arguments]  ${cpu_ip}  ${interface}
  exec_ping6  PC  interface=${interface}  ipAddress=${cpu_ip}  count=5  mode=None

power off dut and check the power status
  Step  1  verify power control  DUT  power_mode=off
  Step  2  verify power control  DUT  power_mode=status  power_status=off

power on dut and check the power status
  Step  1  verify power control  DUT  power_mode=on
  Step  2  verify power control  DUT  power_mode=status  power_status=on

chassis power cycle dut and check power status
  Step  1  reset power chassis  DUT  check_string_flag=True
  Step  2  go to centos
  Step  3  go to openbmc
  Step  4  verify power control  DUT  power_mode=status  power_status=on

check power status and ping test
  Step  1  verify power control  DUT  power_mode=status  power_status=on
  Step  2  ping cpu from bmc test

power off dut and ping test
  Step  1  power off dut and check the power status
  Step  2  exec ping  DUT  ipAddress=${cpu_ipv6}  count=5  mode=${OPENBMC_MODE}  expected=loss

ping cpu from bmc test
  ${bmc_ipv6} =  get dhcp ip address  DUT  interfaceName=eth0  mode=${OPENBMC_MODE}  ipv6=True
  ${cpu_ipv6} =  get dhcp ip address  DUT  interfaceName=eth0  mode=${CENTOS_MODE}  ipv6=True
  Set Suite Variable  ${cpu_ipv6}  ${cpu_ipv6}
  Step  1  ping6 CPU from BMC  ${cpu_ipv6}  eth0

power reset cpu and check only cpu be reset
  Step  1  verify power control  DUT  power_mode=reset
  Step  2  go to openbmc
  Step  3  verify power control  DUT  power_mode=status  power_status=on

run sdk script
  [Arguments]  ${exit_flag}=True
  Step  1  set interface link  interface_name=usb0  status=up  mode=${CENTOS_MODE}
  Step  2  check file exist  path=${sdk_path}  mode=${CENTOS_MODE}  test_flag=True
  Step  3  change dir  path=${sdk_path}  mode=${CENTOS_MODE}
  Step  4  run sdk init  DUT  exe_timeout=${sdk_timeout}  exit_flag=${exit_flag}
  Step  5  set time delay  60

run sdk script and check pem presence device
  Step  1  run sdk script  exit_flag=False
  Run keyword if  ${has_pem}  check pem presence device  ELSE  set false pem device

check all sensor list
  Step  1  wedge400c run sdk script  exit_flag=False
  Step  2  go to openbmc
  Step  3  verify sensor util  DUT  all  force  ${all_type}  info_flag=True

check all sensor list wedge400
  Step  1  go to openbmc
  Step  2  verify sensor util  DUT  all  force  ${all_type}  info_flag=True

wedge400c run sdk script
  [Arguments]  ${exit_flag}=True
  Step  1  set interface link  interface_name=usb0  status=up  mode=${CENTOS_MODE}
  Step  2  ping6 ip test  DUT
  Step  3  check file exist  path=${sdk_path}  mode=${CENTOS_MODE}  test_flag=True
  Step  4  change dir  path=${sdk_path}  mode=${CENTOS_MODE}
#Step  5  download images  DUT  SDK
#Step  6  copy file to other folder  DUT
  Step  7  run sdk init  DUT  exe_timeout=${sdk_timeout}  exit_flag=${exit_flag}
  Step  8  set time delay  10

check all sensor list minipack2
  Step  1  run sdk script if TH4 present
  Step  2  go to openbmc
  Step  3  verify sensor util  DUT  all  force  ${all_type}  info_flag=True

run sdk script if TH4 present
    ${th4_presence} =  check th4 chip  DUT
    Run keyword if  ${th4_presence} == True  run sdk script

change dir to default
  Step  1  change dir  mode=${CENTOS_MODE}
  Step  2  go to openbmc

set and get fan speed
  [Arguments]  ${fan_speed}
  Step  1  set fan speed  DUT  fan_speed=${fan_speed}
  Step  2  set time delay  10
  Step  3  get fan speed  DUT  fan_speed=${fan_speed}

read fan speed and disable fan auto control
  Step  1  get fan speed  DUT  30  70
  Step  2  set fan auto control  DUT  disable
  Step  3  set and get fan speed  10

run command to enable fan auto control and read fan speed
  Step  1  set fan auto control  DUT  enable
  Step  2  set time delay  60
  Step  3  get fan speed  DUT  30  70

run commnad to disable fan auto control and set and get fan speed 25
  Step  1  set fan auto control  DUT  disable
  Step  2  set and get fan speed  25

set and get fan speed 50
  Step  1  set and get fan speed  50

set and get fan speed 70
  Step  1  set and get fan speed  70

set and get fan speed 10
  Step  1  set and get fan speed  10

set and get fan speed 25
  Step  1  set and get fan speed  25

run command to enable fan auto control
  Step  1  set fan auto control  DUT  enable

run command to read scm eeprom
  Step  1  read eeprom  ${scm_eeprom_path}  SCM  ${scm_eeprom_product_name}

run command to write and read scm eeprom
  #### i2cset -f -y 2 0x3e 0x38 0
  Step  1  run i2ctool  DUT  set  bus=${scm_cpld_bus}  addr=${scm_cpld_addr}  reg=${system_misc_4_reg}  val=${write_enable_scm}
  Step  2  write and read eeprom  SCM  ${scm_eeprom_test}

run command to write and read scm eeprom with different data
  #### i2cset -f -y 2 0x3e 0x38 0
  Step  1  run i2ctool  DUT  set  bus=${scm_cpld_bus}  addr=${scm_cpld_addr}  reg=${system_misc_4_reg}  val=${write_enable_scm}
  Step  2  write and read eeprom  SCM  ${scm_eeprom_test2}

run command to write and read scm eeprom minipack2
  Step  1  write and read eeprom  SCM  ${scm_eeprom_test}

run command to write and read scm eeprom with different data minipack2
  Step  1  write and read eeprom  SCM  ${scm_eeprom_test2}

reset bmc and read scm eeprom
  Step  1  reset bmc and read eeprom  SCM  ${scm_eeprom_path}  ${scm_eeprom_test}

reset bmc and read scm eeprom with different data
  Step  1  reset bmc and read eeprom  SCM  ${scm_eeprom_path}  ${scm_eeprom_test2}

chassis power cycle and read scm eeprom
  Step  1  chassis power cycle and read eeprom  SCM  ${scm_eeprom_path}  ${scm_eeprom_test}

run command to read smb eeprom
  ${smb_content}=  Set Variable If	  ${pem1_presence} == True or ${pem2_presence} == True    ${smb_eeprom_name_dc}
  ...  ${smb_eeprom_product_name}
  Step  1  read eeprom  ${smb_eeprom_path}  SMB  ${smb_content}

run command to write and read smb eeprom
  ${smb_content}=  Set Variable If	  ${pem1_presence} == True or ${pem2_presence} == True    ${smb_eeprom_test_dc}
  ...  ${smb_eeprom_test}
  Step  1  write and read eeprom  SMB  ${smb_content}

run command to write and read smb eeprom with different data
  ${smb_content}=  Set Variable If	  ${pem1_presence} == True or ${pem2_presence} == True    ${smb_eeprom_test_dc2}
  ...  ${smb_eeprom_test2}
  Step  1  write and read eeprom  SMB  ${smb_content}

run command to write and read smb eeprom minipack2
  Step  1  run i2ctool  DUT  set  bus=${smb_cpld_bus}  addr=${smb_cpld_addr}  reg=${cpld_spi_hold_wp_reg}  val=${enable_wp}
  Step  2  write and read eeprom  SMB  ${smb_eeprom_test}
  Step  3  run i2ctool  DUT  set  bus=${smb_cpld_bus}  addr=${smb_cpld_addr}  reg=${cpld_spi_hold_wp_reg}  val=${disable_wp}

run command to write and read smb eeprom with different data minipack2
  Step  1  run i2ctool  DUT  set  bus=${smb_cpld_bus}  addr=${smb_cpld_addr}  reg=${cpld_spi_hold_wp_reg}  val=${enable_wp}
  Step  2  write and read eeprom  SMB  ${smb_eeprom_test2}
  Step  3  run i2ctool  DUT  set  bus=${smb_cpld_bus}  addr=${smb_cpld_addr}  reg=${cpld_spi_hold_wp_reg}  val=${disable_wp}

reset bmc and read smb eeprom
  ${smb_content}=  Set Variable If	  ${pem1_presence} == True or ${pem2_presence} == True    ${smb_eeprom_test_dc}
  ...  ${smb_eeprom_test}
  Step  1  reset bmc and read eeprom  SMB  ${smb_eeprom_path}  ${smb_content}

reset bmc and read smb eeprom with different data
  ${smb_content}=  Set Variable If	  ${pem1_presence} == True or ${pem2_presence} == True    ${smb_eeprom_test_dc2}
  ...  ${smb_eeprom_test2}
  Step  1  reset bmc and read eeprom  SMB  ${smb_eeprom_path}  ${smb_content}

chassis power cycle and read smb eeprom
  ${smb_content}=  Set Variable If	  ${pem1_presence} == True or ${pem2_presence} == True    ${smb_eeprom_test_dc}
  ...  ${smb_eeprom_test}
  Step  1  chassis power cycle and read eeprom  SMB  ${smb_eeprom_path}  ${smb_content}

run command to read fcb eeprom minipack2
  Step  1  read eeprom  ${fcm_t_eeprom_path}  FCM_T  ${fcm_eeprom_product_name}
  Step  2  read eeprom  ${fcm_b_eeprom_path}  FCM_B  ${fcm_eeprom_product_name}

run command to read fcb eeprom
  Step  1  read eeprom  ${fcm_eeprom_path}  FCM  ${fcm_eeprom_product_name}

run command to write and read fcb eeprom minipack2
  Step  1  change dir  ${fcm_t_eeprom_path}
  Step  2  write and read eeprom  FCM_T  ${fcm_eeprom_test}
  Step  3  change dir  ${fcm_b_eeprom_path}
  Step  4  write and read eeprom  FCM_B  ${fcm_eeprom_test}

run command to write and read fcb eeprom
  Step  1  write and read eeprom  FCM  ${fcm_eeprom_test}

reset bmc and read fcb eeprom minipack2
  Step  1  reboot device
  Step  2  change dir  ${fcm_t_eeprom_path}
  Step  3  run eeprom tool  DUT  option=d  eeprom_type=FCM_T  expected_result=${fcm_eeprom_test}
  Step  4  change dir  ${fcm_b_eeprom_path}
  Step  5  run eeprom tool  DUT  option=d  eeprom_type=FCM_B  expected_result=${fcm_eeprom_test}

reset bmc and read fcb eeprom
  Step  1  reset bmc and read eeprom  FCM  ${fcm_eeprom_path}  ${fcm_eeprom_test}

chassis power cycle and read fcb eeprom minipack2
  Step  1  reset power chassis  DUT
  Step  2  change dir  ${fcm_t_eeprom_path}
  Step  3  run eeprom tool  DUT  option=d  eeprom_type=FCM_T  expected_result=${fcm_eeprom_test}
  Step  2  change dir    ${fcm_b_eeprom_path}
  Step  3  run eeprom tool  DUT  option=d  eeprom_type=FCM_B  expected_result=${fcm_eeprom_test}

chassis power cycle and read fcb eeprom
  Step  1  chassis power cycle and read eeprom  FCM  ${fcm_eeprom_path}  ${fcm_eeprom_test}

run command to write and read fcb eeprom with different data minipack2
  Step  1  change dir  ${fcm_t_eeprom_path}
  Step  2  write and read eeprom  FCM_T  ${fcm_eeprom_test2}
  Step  3  change dir  ${fcm_b_eeprom_path}
  Step  4  write and read eeprom  FCM_B  ${fcm_eeprom_test2}

run command to write and read fcb eeprom with different data
  Step  1  write and read eeprom  FCM  ${fcm_eeprom_test2}

reset bmc and read fcb eeprom with different data minipack2
  Step  1  reboot device
  Step  2  change dir  ${fcm_t_eeprom_path}
  Step  3  run eeprom tool  DUT  option=d  eeprom_type=FCM_T  expected_result=${fcm_eeprom_test2}
  Step  4  change dir  ${fcm_b_eeprom_path}
  Step  5  run eeprom tool  DUT  option=d  eeprom_type=FCM_B  expected_result=${fcm_eeprom_test2}

reset bmc and read fcb eeprom with different data
  Step  1  reset bmc and read eeprom  FCM  ${fcm_eeprom_path}  ${fcm_eeprom_test2}

run command to read pem eeprom if pem present
  Run keyword if  ${pem1_presence} == True or ${pem2_presence} == True  run command to read pem eeprom

run command to read pem eeprom
  Step  1  read eeprom  ${pem_eeprom_path}  PEM  ${pem_eeprom_product_name}

run command to write and read pem eeprom if pem present
  Run keyword if  ${pem1_presence} == True or ${pem2_presence} == True  run command to write and read pem eeprom

run command to write and read pem eeprom
  Step  1  write and read eeprom  PEM  ${pem_eeprom_test}
  Step  2  write and read hotswap eeprom  ${hotswap_eeprom_test}

run command to write and read pem eeprom with different data if pem present
  Run keyword if  ${pem1_presence} == True or ${pem2_presence} == True  run command to write and read pem eeprom with different data

run command to write and read pem eeprom with different data
  Step  1  write and read eeprom  PEM  ${pem_eeprom_test2}
  Step  2  write and read hotswap eeprom  ${hotswap_eeprom_test2}

chassis power cycle and read pem eeprom with different data if pem present
  Run keyword if  ${pem1_presence} == True or ${pem2_presence} == True  chassis power cycle and read pem eeprom with different data

chassis power cycle and read pem eeprom with different data
  Step  1  chassis power cycle and read eeprom  PEM  ${pem_eeprom_path}  ${pem_eeprom_test2}

write and read hotswap eeprom
  [Arguments]  ${eeprom_test_name}
  Step  1  modify eeprom cfg  DUT  ${eeprom_test_name}  hotswap_eeprom.cfg
  Step  2  run eeprom tool  DUT  option=w  eeprom_type=${hotswap_eeprom_name}
  Step  3  run eeprom tool  DUT  option=d  eeprom_type=${hotswap_eeprom_name}  expected_result=${eeprom_test_name}

check pem presence device and prepare store pem eeprom
  Step  1  check pem presence device
  Run keyword if  ${pem1_presence} == True or ${pem2_presence} == True  prepare store eeprom  ${pem_eeprom_path}  PEM
  Run keyword if  ${pem1_presence} == True or ${pem2_presence} == True  store eeprom  DUT  hotswap_eeprom.cfg  hotswap_eeprom_store.cfg  ${pem_eeprom_path}

restore pem eeprom and hotswap eeprom if pem present
  Run keyword if  ${pem1_presence} == True or ${pem2_presence} == True  restore pem eeprom and hotswap eeprom

restore pem eeprom and hotswap eeprom
  Step  1  change dir  ${pem_eeprom_path}
  Step  2  store eeprom  DUT  eeprom_store.cfg  eeprom.cfg  ${pem_eeprom_path}
  Step  3  run eeprom tool  DUT  option=w  eeprom_type=PEM
  Step  5  run eeprom tool  DUT  option=d  eeprom_type=PEM
  Step  6  clean up file  DUT  eeprom_store.cfg
  Step  7  store eeprom  DUT  hotswap_eeprom_store.cfg  hotswap_eeprom.cfg  ${pem_eeprom_path}
  Step  8  run eeprom tool  DUT  option=w  eeprom_type=${hotswap_eeprom_name}
  Step  9  run eeprom tool  DUT  option=d  eeprom_type=${hotswap_eeprom_name}
  Step  10  clean up file  DUT  hotswap_eeprom_store.cfg
  Step  11  change dir

read eeprom
  [Arguments]  ${eeprom_path}  ${eeprom_type}  ${eeprom_product_name}
  Step  1  change dir  ${eeprom_path}
  Step  2  run eeprom tool  DUT  option=d  eeprom_type=${eeprom_type}  expected_result=${eeprom_product_name}

write and read eeprom
  [Arguments]  ${eeprom_type}  ${eeprom_test_name}
  Step  1  modify eeprom cfg  DUT  ${eeprom_test_name}  eeprom.cfg
  Step  2  run eeprom tool  DUT  option=w  eeprom_type=${eeprom_type}
  Step  4  run eeprom tool  DUT  option=d  eeprom_type=${eeprom_type}  expected_result=${eeprom_test_name}

chassis power cycle and read eeprom
  [Arguments]  ${eeprom_type}  ${eeprom_path}  ${eeprom_test_name}
  Step  1  reset power chassis  DUT
  Step  2  change dir  ${eeprom_path}
  Step  3  run eeprom tool  DUT  option=d  eeprom_type=${eeprom_type}  expected_result=${eeprom_test_name}

reset bmc and read eeprom
  [Arguments]  ${eeprom_type}  ${eeprom_path}  ${eeprom_test_name}
  Step  1  reboot device
  Step  2  change dir  ${eeprom_path}
  Step  3  run eeprom tool  DUT  option=d  eeprom_type=${eeprom_type}  expected_result=${eeprom_test_name}

run command to read fan eeprom
  Step  1  change dir  ${fan_eeprom_path}
  FOR    ${fan}    IN RANGE    ${1}  ${FAN_NUM}+1
      Step  1  run eeprom tool  DUT  option=d  eeprom_type=FAN${fan}  fan=${fan}  expected_result=${fan_eeprom_product_name}
  END

run command to write and read fan eeprom
  FOR    ${fan}    IN RANGE    ${1}  ${FAN_NUM}+1
      Step  1  write and read fan eeprom  ${fan}  ${fan_eeprom_test}
  END

run command to write and read fan eeprom with different data
  FOR    ${fan}    IN RANGE    ${1}  ${FAN_NUM}+1
      Step  1  write and read fan eeprom  ${fan}  ${fan_eeprom_test2}
  END

reset bmc and read fan eeprom
  Step  1  reboot device
  Step  2  change dir  ${fan_eeprom_path}
  FOR    ${fan}    IN RANGE    ${1}  ${FAN_NUM}+1
      Step  1  run eeprom tool  DUT  option=d  eeprom_type=FAN${fan}  fan=${fan}  expected_result=${fan_eeprom_test}
  END

reset bmc and read fan eeprom with different data
  Step  1  reboot device
  Step  2  change dir  ${fan_eeprom_path}
  FOR    ${fan}    IN RANGE    ${1}  ${FAN_NUM}+1
      Step  1  run eeprom tool  DUT  option=d  eeprom_type=FAN${fan}  fan=${fan}  expected_result=${fan_eeprom_test2}
  END

chassis power cycle and read fan eeprom
  Step  1  reset power chassis  DUT
  Step  2  change dir  ${fan_eeprom_path}
  FOR    ${fan}    IN RANGE    ${1}  ${FAN_NUM}+1
      Step  1  run eeprom tool  DUT  option=d  eeprom_type=FAN${fan}  fan=${fan}  expected_result=${fan_eeprom_test}
  END

write and read fan eeprom
  [Arguments]  ${fan_number}  ${eeprom_test_name}
  Step  1  modify eeprom cfg  DUT  ${eeprom_test_name}  eeprom.cfg
  Step  2  run eeprom tool  DUT  option=w  eeprom_type=FAN${fan_number}  fan=${fan_number}
  Step  3  run eeprom tool  DUT  option=d  eeprom_type=FAN${fan_number}  fan=${fan_number}  expected_result=${eeprom_test_name}

prepare store eeprom
  [Arguments]  ${eeprom_path}  ${eeprom_type}
  Step  1  switch to openbmc
  Step  2  change dir  ${eeprom_path}
  Step  3  run eeprom tool  DUT  option=d  eeprom_type=${eeprom_type}
  Step  4  store eeprom  DUT  eeprom_out.cfg  eeprom_store.cfg  ${eeprom_path}

prepare store eeprom w400
  [Arguments]  ${eeprom_path}  ${eeprom_type}
  Step  1  change dir  ${bmc_bin_path}
  Step  2  init diag config  DUT
  Step  2  change dir  ${eeprom_path}
  Step  3  run eeprom tool  DUT  option=d  eeprom_type=${eeprom_type}
  Step  4  store eeprom  DUT  eeprom_out.cfg  eeprom_store.cfg  ${eeprom_path}

prepare store all fan eeprom
  Step  1  change dir  ${fan_eeprom_path}
  FOR    ${fan}    IN RANGE    ${1}  ${FAN_NUM}+1
      Step  1  run eeprom tool  DUT  option=d  eeprom_type=FAN${fan}  fan=${fan}
      Step  2  store eeprom  DUT  eeprom_out.cfg  eeprom_store${fan}.cfg  ${fan_eeprom_path}
  END

prepare dc unit init diag
  Step  1  change dir  ${bmc_bin_path}
  Step  2  init diag config  DUT

prepare store fcb eeprom minipack2
  Step  1  change dir  ${fcm_t_eeprom_path}
  Step  2  run eeprom tool  DUT  option=d  eeprom_type=FCM_T
  Step  3  store eeprom  DUT  eeprom_out.cfg  eeprom_store.cfg  ${fcm_t_eeprom_path}
  Step  4  change dir  ${fcm_b_eeprom_path}
  Step  5  run eeprom tool  DUT  option=d  eeprom_type=FCM_B
  Step  6  store eeprom  DUT  eeprom_out.cfg  eeprom_store.cfg  ${fcm_b_eeprom_path}

restore eeprom
  [Arguments]  ${eeprom_path}  ${eeprom_type}
  Step  1  change dir  ${eeprom_path}
  Step  2  store eeprom  DUT  eeprom_store.cfg  eeprom.cfg  ${eeprom_path}
  Step  3  run eeprom tool  DUT  option=w  eeprom_type=${eeprom_type}
  Step  5  run eeprom tool  DUT  option=d  eeprom_type=${eeprom_type}
  Step  6  clean up file  DUT  eeprom_store.cfg
  Step  7  reboot device

restore smb eeprom minipack2
  Step  1  change dir  ${smb_eeprom_path}
  Step  2  store eeprom  DUT  eeprom_store.cfg  eeprom.cfg  ${smb_eeprom_path}
  Step  3  run i2ctool  DUT  set  bus=${smb_cpld_bus}  addr=${smb_cpld_addr}  reg=${cpld_spi_hold_wp_reg}  val=${enable_wp}
  Step  4  run eeprom tool  DUT  option=w  eeprom_type=SMB
  Step  6  run eeprom tool  DUT  option=d  eeprom_type=SMB
  Step  7  run i2ctool  DUT  set  bus=${smb_cpld_bus}  addr=${smb_cpld_addr}  reg=${cpld_spi_hold_wp_reg}  val=${disable_wp}
  Step  8  clean up file  DUT  eeprom_store.cfg
  Step  9  reboot device

restore all fan eeprom
  Step  1  change dir  ${fan_eeprom_path}
  FOR    ${fan}    IN RANGE    ${1}  ${FAN_NUM}+1
      Step  1  restore fan eeprom  ${fan}  eeprom_store${fan}.cfg
      Step  2  clean up file  DUT  eeprom_store${fan}.cfg
  END
  Step  2  change dir

restore fan eeprom
  [Arguments]  ${fan_number}  ${store_file}
  Step  1  store eeprom  DUT  ${store_file}  eeprom.cfg
  Step  2  run eeprom tool  DUT  option=w  eeprom_type=FAN${fan_number}  fan=${fan_number}  flag=${PimType}
  Step  4  run eeprom tool  DUT  option=d  eeprom_type=FAN${fan_number}  fan=${fan_number}  flag=${PimType}

restore fcb eeprom minipack2
  Step  1  change dir  ${fcm_t_eeprom_path}
  Step  2  store eeprom  DUT  eeprom_store.cfg  eeprom.cfg  ${fcm_t_eeprom_path}
  Step  3  run eeprom tool  DUT  option=w  eeprom_type=FCM_T
  Step  5  run eeprom tool  DUT  option=d  eeprom_type=FCM_T
  Step  6  clean up file  DUT  eeprom_store.cfg
  Step  7  change dir  ${fcm_b_eeprom_path}
  Step  8  store eeprom  DUT  eeprom_store.cfg  eeprom.cfg  ${fcm_b_eeprom_path}
  Step  9  run eeprom tool  DUT  option=w  eeprom_type=FCM_B
  Step  11  run eeprom tool  DUT  option=d  eeprom_type=FCM_B
  Step  12  clean up file  DUT  eeprom_store.cfg
  Step  13  change dir

prepare FCM eeprom test
  go to openbmc
  prepare i2c device  DUT  bus=31  addr=0x51  delete_flag=True

prepare PEM eeprom test
  go to openbmc
  prepare i2c device  DUT  bus=22  addr=0x50

log util test
  [Arguments]  ${option}
  Step  1  verify log util  DUT  scm  option=${option}
  Step  2  verify log util  DUT  smb  option=${option}
  Step  3  verify log util  DUT  sys  option=${option}
  Step  4  verify log util  DUT  psu1  option=${option}
  Step  5  verify log util  DUT  psu2  option=${option}
  Step  6  verify log util  DUT  all  option=${option}

run all the support parameters of sensor-util threshold
  Step  1  verify sensor util  DUT  scm  threshold  ${scm_type}  info_flag=True
  Step  2  verify sensor util  DUT  smb  threshold  ${smb_type}  info_flag=True
  Run keyword if  ${pem1_presence} == False and ${pem2_presence} == False  verify sensor util  DUT  psu1  threshold  ${psu_type}  info_flag=True
  Run keyword if  ${pem1_presence} == False and ${pem2_presence} == False  verify sensor util  DUT  psu2  threshold  ${psu_type}  info_flag=True
  Run keyword if  ${pem2_presence} == True  verify sensor util  DUT  pem2  threshold  ${pem_type}  info_flag=True
  Step  3  verify sensor util  DUT  all  threshold  ${all_type}  info_flag=True

run all the support parameters of sensor-util history information
  Step  1  verify sensor util  DUT  scm  history 10m  ${scm_type}
  Step  2  verify sensor util  DUT  smb  history 10m  ${smb_type}
  Run keyword if  ${pem1_presence} == False and ${pem2_presence} == False  verify sensor util  DUT  psu1  history 10m  ${psu_type}
  Run keyword if  ${pem1_presence} == False and ${pem2_presence} == False  verify sensor util  DUT  psu2  history 10m  ${psu_type}
  Run keyword if  ${pem2_presence} == True  verify sensor util  DUT  pem2  history 10m  ${pem_type}
  Step  3  verify sensor util  DUT  all  history 10m  ${all_type}

run all the support parameters of sensor-util history clear
  Step  1  verify sensor util  DUT  scm  history-clear
  Step  2  verify sensor util  DUT  smb  history-clear
  Run keyword if  ${pem1_presence} == False and ${pem2_presence} == False  verify sensor util  DUT  psu1  history-clear
  Run keyword if  ${pem1_presence} == False and ${pem2_presence} == False  verify sensor util  DUT  psu2  history-clear
  Run keyword if  ${pem2_presence} == True  verify sensor util  DUT  pem2  history-clear
  Step  3  verify sensor util  DUT  all  history-clear

run all the support parameters of sensor-util firmware information
  Step  1  verify sensor util  DUT  scm  force  ${scm_type}  info_flag=True
  Step  2  verify sensor util  DUT  smb  force  ${smb_type}  info_flag=True
  Run keyword if  ${pem1_presence} == False and ${pem2_presence} == False  verify sensor util  DUT  psu1  force  ${psu_type}  info_flag=True
  Run keyword if  ${pem1_presence} == False and ${pem2_presence} == False  verify sensor util  DUT  psu2  force  ${psu_type}  info_flag=True
  Run keyword if  ${pem2_presence} == True  verify sensor util  DUT  pem2  force  ${pem_type}  info_flag=True
  Step  3  verify sensor util  DUT  all  force  ${all_type}  info_flag=True

run all the support parameters of sensor-util threshold minipack2
  Step  1  verify sensor util  DUT  scm  threshold  ${scm_type}  info_flag=True
  Step  2  verify sensor util  DUT  smb  threshold  ${smb_type}  info_flag=True
  Step  3  verify sensor util  DUT  psu1  threshold  ${psu_type}  info_flag=True
  Step  4  verify sensor util  DUT  psu2  threshold  ${psu_type}  info_flag=True
  Step  5  verify sensor util  DUT  psu3  threshold  ${psu_type}  info_flag=True
  Step  6  verify sensor util  DUT  psu4  threshold  ${psu_type}  info_flag=True
  Step  7  verify sensor util  DUT  all  threshold  ${all_type}  info_flag=True

run all the support parameters of sensor-util history information minipack2
  Step  1  verify sensor util  DUT  scm  history 10m  ${scm_type}
  Step  2  verify sensor util  DUT  smb  history 10m  ${smb_type}
  Step  3  verify sensor util  DUT  psu1  history 10m  ${psu_type}
  Step  4  verify sensor util  DUT  psu2  history 10m  ${psu_type}
  Step  5  verify sensor util  DUT  psu3  history 10m  ${psu_type}
  Step  6  verify sensor util  DUT  psu4  history 10m  ${psu_type}
  Step  7  verify sensor util  DUT  all  history 10m  ${all_type}

run all the support parameters of sensor-util history clear minipack2
  Step  1  verify sensor util  DUT  scm  history-clear
  Step  2  verify sensor util  DUT  smb  history-clear
  Step  3  verify sensor util  DUT  psu1  history-clear
  Step  4  verify sensor util  DUT  psu2  history-clear
  Step  5  verify sensor util  DUT  psu3  history-clear
  Step  6  verify sensor util  DUT  psu4  history-clear
  Step  7  verify sensor util  DUT  all  history-clear

run all the support parameters of sensor-util firmware information minipack2
  Step  1  verify sensor util  DUT  scm  force  ${scm_type}  info_flag=True
  Step  2  verify sensor util  DUT  smb  force  ${smb_type}  info_flag=True
  Step  3  verify sensor util  DUT  psu1  force  ${psu_type}  info_flag=True
  Step  4  verify sensor util  DUT  psu2  force  ${psu_type}  info_flag=True
  Step  5  verify sensor util  DUT  psu3  force  ${psu_type}  info_flag=True
  Step  6  verify sensor util  DUT  psu4  force  ${psu_type}  info_flag=True
  Step  7  verify sensor util  DUT  all  force  ${all_type}  info_flag=True

check file size on tftp server
  ${file_on_server_size} =  check file exist and size  PC  path=${tftp_server_path}/${tftp_file_test}  check_size_flag=True
  Set Suite Variable  ${file_on_server_size}  ${file_on_server_size}

copy the image file from tftp server and check size
  Step  1  get dhcp ip address  DUT  eth0  mode=${OPENBMC_MODE}  ipv6=True
  Step  2  copy files through tftp  DUT  ${TFTP_SERVER}  ${tftp_file_test}
  Step  3  check file exist and size  DUT  ${tftp_file_test}  True  ${file_on_server_size}  ${OPENBMC_MODE}

check openbmc info after openbmc cold reset of itself
  [Arguments]  ${bmc_flash}
  Step  1  run ipmi cmd cold reset  DUT  ${cmd_cold_reset}
  Step  2  verify current boot flash  DUT  ${bmc_flash}
  Step  3  run ipmi get test  get_device_id  DUT  ${cmd_get_device_id}  ${rsp_device_id}

check openbmc info after chassis power cycle
  Step  1  go to openbmc
  Step  2  reset power chassis  DUT  check_string_flag=True
  Step  3  verify current boot flash  DUT  Master
  Step  4  run ipmi get test  get_device_id  DUT  ${cmd_get_device_id}  ${rsp_device_id}

check bic power cycle stress
  Step  1  go to openbmc
  Step  2  reset power chassis  DUT  check_string_flag=True

run ipmi command "get device id" to get openbmc info in master openbmc
  Step  1  run ipmi get test  get_device_id  DUT  ${cmd_get_device_id}  ${rsp_device_id}
  Step  2  check openbmc info after openbmc cold reset of itself  Master
  Step  3  check openbmc info after chassis power cycle

run ipmi command "get device id" to get openbmc info in slave openbmc
  Step  1  switch bmc flash  DUT  Slave
  Step  2  run ipmi get test  get_device_id  DUT  ${cmd_get_device_id}  ${rsp_device_id}
  Step  3  check openbmc info after openbmc cold reset of itself  Slave
  Step  4  check openbmc info after chassis power cycle

run ipmi command "reset bmc from host" in master openbmc
  Step  1  run ipmi cmd cold reset  DUT  ${cmd_cold_reset}
  # Step  3  run ipmi cmd cold reset  DUT  ${cmd_cold_reset}
  # Step  4  run ipmi cmd cold reset  DUT  ${cmd_cold_reset}

verify self test result
  Step  1  go to centos
  Step  2  run ipmi get cmd  DUT  ${cmd_get_self_test_result}  ${rsp_self_test}
  Step  3  enter bios setup  DUT
  Step  4  send key  DUT  KEY_RIGHT  ${3}
  Step  5  verify menu bios setup  DUT  keyword=${bmc_self_result_pass}
  Step  6  exit bios setup  DUT
  Step  7  go to openbmc

get the bmc selftest result via ipmi command "get self results" in master openbmc
  Step  1  verify self test result

# set and get watchdog no action
#   [Arguments]    ${timer_use}  ${countdown_val}
#   Step  1  set watchdog  DUT  cmd=${cmd_set_wdt}
#                 ...  timer_use=${wdt_timer_use["${timer_use}"]}
#                 ...  timer_action=${wdt_timer_action["no action"]}
#                 ...  pre_timer=${wdt_pre_timeout}
#                 ...  timer_use_expr=${wdt_timer_use_expr}
#                 ...  countdown=${countdown_val}
#   Step  2  get watchdog  DUT  cmd=${cmd_get_wdt}
#                 ...  expected_result=${wdt_timer_use["${timer_use}"]} ${wdt_timer_action["no action"]} ${wdt_pre_timeout} ${wdt_timer_use_expr} ${countdown_val} ${countdown_val}
#   Step  3  reset watchdog
#   Step  4  set time delay  1
#   Step  5  get watchdog  DUT  cmd=${cmd_get_wdt}
#                 ...  expected_result=${wdt_timer_use["${timer_use}"]} ${wdt_timer_action["no action"]} ${wdt_pre_timeout} ${wdt_timer_use_expr} ${countdown_val} ${wdt_countdown_val_0s}

# set and get watchdog hard reset
#   [Arguments]    ${timer_use}  ${countdown_val}
#   Step  1  set watchdog  DUT  cmd=${cmd_set_wdt}
#                 ...  timer_use=${wdt_timer_use["${timer_use}"]}
#                 ...  timer_action=${wdt_timer_action["hard reset"]}
#                 ...  pre_timer=${wdt_pre_timeout}
#                 ...  timer_use_expr=${wdt_timer_use_expr}
#                 ...  countdown=${countdown_val}
#   Step  2  get watchdog  DUT  cmd=${cmd_get_wdt}
#                 ...  expected_result=${wdt_timer_use["${timer_use}"]} ${wdt_timer_action["hard reset"]} ${wdt_pre_timeout} ${wdt_timer_use_expr} ${countdown_val} ${countdown_val}
#   Step  3  reset watchdog
#   Step  4  set time delay  1
#   Step  5  verify bios boot  DUT
#   Step  6  get watchdog  DUT  cmd=${cmd_get_wdt}
#                 ...  expected_result=${wdt_timer_use["BIOS FRB2"]} ${wdt_timer_action["no action"]} ${wdt_pre_timeout} ${wdt_timer_use_expr} ${wdt_countdown_val_0s} ${wdt_countdown_val_0s}

# set and get watchdog power down
#   [Arguments]    ${timer_use}  ${countdown_val}
#   Step  1  set watchdog  DUT  cmd=${cmd_set_wdt}
#                 ...  timer_use=${wdt_timer_use["${timer_use}"]}
#                 ...  timer_action=${wdt_timer_action["power down"]}
#                 ...  pre_timer=${wdt_pre_timeout}
#                 ...  timer_use_expr=${wdt_timer_use_expr}
#                 ...  countdown=${countdown_val}
#   Step  2  get watchdog  DUT  cmd=${cmd_get_wdt}
#                 ...  expected_result=${wdt_timer_use["${timer_use}"]} ${wdt_timer_action["power down"]} ${wdt_pre_timeout} ${wdt_timer_use_expr} ${countdown_val} ${countdown_val}
#   Step  3  reset watchdog
#   Step  4  set time delay  1
#   Step  5  go to openbmc
#   Step  6  verify power control  DUT  power_mode=status  power_status=off
#   Step  7  verify power control  DUT  power_mode=on
#   Step  8  get watchdog  DUT  cmd=${cmd_get_wdt}
#                 ...  expected_result=${wdt_timer_use["BIOS FRB2"]} ${wdt_timer_action["no action"]} ${wdt_pre_timeout} ${wdt_timer_use_expr} ${wdt_countdown_val_0s} ${wdt_countdown_val_0s}

# set and get watchdog power cycle
#   [Arguments]    ${timer_use}  ${countdown_val}
#   Step  1  set watchdog  DUT  cmd=${cmd_set_wdt}
#                 ...  timer_use=${wdt_timer_use["${timer_use}"]}
#                 ...  timer_action=${wdt_timer_action["power cycle"]}
#                 ...  pre_timer=${wdt_pre_timeout}
#                 ...  timer_use_expr=${wdt_timer_use_expr}
#                 ...  countdown=${countdown_val}
#   Step  2  get watchdog  DUT  cmd=${cmd_get_wdt}
#                 ...  expected_result=${wdt_timer_use["${timer_use}"]} ${wdt_timer_action["power cycle"]} ${wdt_pre_timeout} ${wdt_timer_use_expr} ${countdown_val} ${countdown_val}
#   Step  3  reset watchdog
#   Step  4  set time delay  1
#   Step  5  verify bios boot  DUT
#   Step  6  get watchdog  DUT  cmd=${cmd_get_wdt}
#                 ...  expected_result=${wdt_timer_use["BIOS FRB2"]} ${wdt_timer_action["no action"]} ${wdt_pre_timeout} ${wdt_timer_use_expr} ${wdt_countdown_val_0s} ${wdt_countdown_val_0s}

# test watchdog timer with parameters "bios frb2" and "no action"
#   Step  1  set and get watchdog no action  BIOS FRB2  ${wdt_countdown_val_02s}

# test watchdog timer with parameters "bios/post" and "no action"
#   Step  1  set and get watchdog no action  BIOS/POST  ${wdt_countdown_val_02s}

# test watchdog timer with parameters "os load" and "no action"
#   Step  1  set and get watchdog no action  OS Load  ${wdt_countdown_val_02s}

# test watchdog timer with parameters "sms/os" and "no action"
#   Step  1  set and get watchdog no action  SMS/OS  ${wdt_countdown_val_02s}

# test watchdog timer with parameters "oem" and "no action"
#   Step  1  set and get watchdog no action  OEM  ${wdt_countdown_val_02s}

# test watchdog timer with parameters "bios frb2" and "hard reset"
#   Step  1  set and get watchdog hard reset  BIOS FRB2  ${wdt_countdown_val_02s}

# test watchdog timer with parameters "bios/post" and "hard reset"
#   Step  1  set and get watchdog hard reset  BIOS/POST  ${wdt_countdown_val_02s}

# test watchdog timer with parameters "os load" and "hard reset"
#   Step  1  set and get watchdog hard reset  OS Load  ${wdt_countdown_val_02s}

# test watchdog timer with parameters "sms/os" and "hard reset"
#   Step  1  set and get watchdog hard reset  SMS/OS  ${wdt_countdown_val_02s}

# test watchdog timer with parameters "oem" and "hard reset"
#   Step  1  set and get watchdog hard reset  OEM  ${wdt_countdown_val_02s}

# test watchdog timer with parameters "bios frb2" and "power down"
#   Step  1  set and get watchdog power down  BIOS FRB2  ${wdt_countdown_val_02s}

# test watchdog timer with parameters "bios/post" and "power down"
#   Step  1  set and get watchdog power down  BIOS/POST  ${wdt_countdown_val_02s}

# test watchdog timer with parameters "os load" and "power down"
#   Step  1  set and get watchdog power down  OS Load  ${wdt_countdown_val_02s}

# test watchdog timer with parameters "sms/os" and "power down"
#   Step  1  set and get watchdog power down  SMS/OS  ${wdt_countdown_val_02s}

# test watchdog timer with parameters "oem" and "power down"
#   Step  1  set and get watchdog power down  OEM  ${wdt_countdown_val_02s}

# test watchdog timer with parameters "bios frb2" and "power cycle"
#   Step  1  set and get watchdog power cycle  BIOS FRB2  ${wdt_countdown_val_02s}

# test watchdog timer with parameters "bios/post" and "power cycle"
#   Step  1  set and get watchdog power cycle  BIOS/POST  ${wdt_countdown_val_02s}

# test watchdog timer with parameters "os load" and "power cycle"
#   Step  1  set and get watchdog power cycle  OS Load  ${wdt_countdown_val_02s}

# test watchdog timer with parameters "sms/os" and "power cycle"
#   Step  1  set and get watchdog power cycle  SMS/OS  ${wdt_countdown_val_02s}

# test watchdog timer with parameters "oem" and "power cycle"
#   Step  1  set and get watchdog power cycle  OEM  ${wdt_countdown_val_02s}

# reset watchdog
#   Step  1  run ipmi set cmd  DUT  cmd=${cmd_reset_wdt}

# set another watchdog
#   [Arguments]    ${timer_use}  ${timer_action}  ${countdown_val}
#   Step  1  set watchdog  DUT  cmd=${cmd_set_wdt}
#             ...  timer_use=${wdt_timer_use["${timer_use}"]}
#             ...  timer_action=${wdt_timer_action["${timer_action}"]}
#             ...  pre_timer=${wdt_pre_timeout}
#             ...  timer_use_expr=${wdt_timer_use_expr}
#             ...  countdown=${countdown_val}
#   Step  2  reset watchdog
#   Step  3  keep getting watchdog before count down to 0  BIOS FRB2  no action  ${wdt_countdown_val_25s}

# set and start watchdog
#   [Arguments]    ${timer_use}  ${timer_action}  ${countdown_val}
#   Step  1  set watchdog  DUT  cmd=${cmd_set_wdt}
#         ...  timer_use=${wdt_timer_use["${timer_use}"]}
#         ...  timer_action=${wdt_timer_action["${timer_action}"]}
#         ...  pre_timer=${wdt_pre_timeout}
#         ...  timer_use_expr=${wdt_timer_use_expr}
#         ...  countdown=${countdown_val}
#   Step  2  reset watchdog

# keep getting watchdog before count down to 0
#   [Arguments]    ${timer_use}  ${timer_action}  ${countdown_val}
#   ${present_time_1} =  get watchdog  DUT  cmd=${cmd_get_wdt}
#         ...  expected_result=${wdt_timer_use["${timer_use}"]} ${wdt_timer_action["${timer_action}"]} ${wdt_pre_timeout} ${wdt_timer_use_expr} ${countdown_val}
#         ...  start_flag=True
#   ${present_time_2} =  get watchdog  DUT  cmd=${cmd_get_wdt}
#         ...  expected_result=${wdt_timer_use["${timer_use}"]} ${wdt_timer_action["${timer_action}"]} ${wdt_pre_timeout} ${wdt_timer_use_expr} ${countdown_val}
#         ...  start_flag=True  previous_t=${present_time_1}
#   ${present_time_3} =  get watchdog  DUT  cmd=${cmd_get_wdt}
#         ...  expected_result=${wdt_timer_use["${timer_use}"]} ${wdt_timer_action["${timer_action}"]} ${wdt_pre_timeout} ${wdt_timer_use_expr} ${countdown_val}
#         ...  start_flag=True  previous_t=${present_time_2}

# run ipmi command "set watchdog timer" to "no action"
#   Step  1  go to centos
#   Step  2  set and start watchdog  BIOS FRB2  no action  ${wdt_countdown_val_02s}
#   Step  3  set time delay  1
#   Step  4  get watchdog  DUT  cmd=${cmd_get_wdt}
#         ...  expected_result=${wdt_timer_use["BIOS FRB2"]} ${wdt_timer_action["no action"]} ${wdt_pre_timeout} ${wdt_timer_use_expr} ${wdt_countdown_val_02s} ${wdt_countdown_val_0s}
#   Step  5  set another watchdog  BIOS FRB2  no action  ${wdt_countdown_val_25s}
#   Step  6  reset watchdog
#   Step  7  get watchdog  DUT  cmd=${cmd_get_wdt}
#         ...  expected_result=${wdt_timer_use["BIOS FRB2"]} ${wdt_timer_action["no action"]} ${wdt_pre_timeout} ${wdt_timer_use_expr} ${wdt_countdown_val_25s}
#         ...  start_flag=True
#   Step  8  go to openbmc

# run ipmi command "set watchdog timer" to "hard reset"
#   Step  1  go to centos
#   Step  2  set and start watchdog  BIOS FRB2  hard reset  ${wdt_countdown_val_02s}
#   Step  3  set time delay  1
#   Step  4  verify bios boot  DUT
#   Step  5  set another watchdog  BIOS FRB2  no action  ${wdt_countdown_val_25s}
#   Step  6  reset watchdog
#   Step  7  get watchdog  DUT  cmd=${cmd_get_wdt}
#         ...  expected_result=${wdt_timer_use["BIOS FRB2"]} ${wdt_timer_action["no action"]} ${wdt_pre_timeout} ${wdt_timer_use_expr} ${wdt_countdown_val_25s}
#         ...  start_flag=True
#   Step  8  go to openbmc

# run ipmi command "set watchdog timer" to "power down"
#   Step  1  go to centos
#   Step  2  set and start watchdog  BIOS FRB2  power down  ${wdt_countdown_val_02s}
#   Step  3  set time delay  1
#   Step  4  go to openbmc
#   Step  5  verify power control  DUT  power_mode=status  power_status=off
#   Step  6  verify power control  DUT  power_mode=on
#   Step  7  set another watchdog  BIOS FRB2  no action  ${wdt_countdown_val_25s}
#   Step  8  reset watchdog
#   Step  9  get watchdog  DUT  cmd=${cmd_get_wdt}
#         ...  expected_result=${wdt_timer_use["BIOS FRB2"]} ${wdt_timer_action["no action"]} ${wdt_pre_timeout} ${wdt_timer_use_expr} ${wdt_countdown_val_25s}
#         ...  start_flag=True
#   Step  10  go to openbmc

# run ipmi command "set watchdog timer" to "power cycle"
#   Step  1  go to centos
#   Step  2  set and start watchdog  BIOS FRB2  power cycle  ${wdt_countdown_val_02s}
#   Step  3  set time delay  1
#   Step  4  verify bios boot  DUT
#   Step  5  set another watchdog  BIOS FRB2  no action  ${wdt_countdown_val_25s}
#   Step  6  reset watchdog
#   Step  7  get watchdog  DUT  cmd=${cmd_get_wdt}
#         ...  expected_result=${wdt_timer_use["BIOS FRB2"]} ${wdt_timer_action["no action"]} ${wdt_pre_timeout} ${wdt_timer_use_expr} ${wdt_countdown_val_25s}
#         ...  start_flag=True
#   Step  8  go to openbmc

# wait for watchdog timeout and set power on chassis
#   Step  1  set time delay  25
#   Step  2  set power on chassis

# clear log scm
#   Step  1  verify log util  DUT  scm  option=clear

# set "don't log" bit to "1" which means do not log the watchdog event
#   Step  1  go to centos
#   Step  2  verify do not log watchdog event no action  BIOS FRB2  ${wdt_countdown_val_02s}

# set "don't log" bit to "0" which means log the watchdog event
#   Step  1  verify log watchdog event no action  BIOS FRB2  ${wdt_countdown_val_02s}

# verify log watchdog event bios frb2 no action
#   Step  1  clear log scm
#   Step  2  verify log watchdog event no action  BIOS FRB2  ${wdt_countdown_val_02s}

# verify log watchdog event bios/post no action
#   Step  1  clear log scm
#   Step  2  verify log watchdog event no action  BIOS/POST  ${wdt_countdown_val_02s}

# verify log watchdog event os load no action
#   Step  1  clear log scm
#   Step  2  verify log watchdog event no action  OS Load  ${wdt_countdown_val_02s}

# verify log watchdog event sms/os no action
#   Step  1  clear log scm
#   Step  2  verify log watchdog event no action  SMS/OS  ${wdt_countdown_val_02s}

# verify log watchdog event oem no action
#   Step  1  clear log scm
#   Step  2  verify log watchdog event no action  OEM  ${wdt_countdown_val_02s}

# verify log watchdog event bios frb2 hard reset
#   Step  1  clear log scm
#   Step  2  verify log watchdog event hard reset  BIOS FRB2  ${wdt_countdown_val_02s}

# verify log watchdog event bios frb2 power down
#   Step  1  clear log scm
#   Step  2  verify log watchdog event power down  BIOS FRB2  ${wdt_countdown_val_02s}

# verify log watchdog event bios frb2 power cycle
#   Step  1  clear log scm
#   Step  2  verify log watchdog event power cycle  BIOS FRB2  ${wdt_countdown_val_02s}

# verify do not log watchdog event no action
#   [Arguments]    ${timer_use}  ${countdown_val}
#   Step  1  set watchdog  DUT  cmd=${cmd_set_wdt}
#                   ...  timer_use=${wdt_timer_use_dont_log["${timer_use}"]}
#                   ...  timer_action=${wdt_timer_action["no action"]}
#                   ...  pre_timer=${wdt_pre_timeout}
#                   ...  timer_use_expr=${wdt_timer_use_expr}
#                   ...  countdown=${countdown_val}
#   Step  2  reset watchdog
#   Step  3  verify log util watchdog  DUT  timer_use=${timer_use}  timer_action=no action  dont_log_flag=True

# verify log watchdog event no action
#   [Arguments]    ${timer_use}  ${countdown_val}
#   Step  1  set watchdog  DUT  cmd=${cmd_set_wdt}
#                   ...  timer_use=${wdt_timer_use["${timer_use}"]}
#                   ...  timer_action=${wdt_timer_action["no action"]}
#                   ...  pre_timer=${wdt_pre_timeout}
#                   ...  timer_use_expr=${wdt_timer_use_expr}
#                   ...  countdown=${countdown_val}
#   Step  2  reset watchdog
#   Step  3  set time delay  1
#   Step  4  verify log util watchdog  DUT  timer_use=${timer_use}  timer_action=no action

# verify log watchdog event hard reset
#   [Arguments]    ${timer_use}  ${countdown_val}
#   Step  1  set watchdog  DUT  cmd=${cmd_set_wdt}
#                   ...  timer_use=${wdt_timer_use["${timer_use}"]}
#                   ...  timer_action=${wdt_timer_action["hard reset"]}
#                   ...  pre_timer=${wdt_pre_timeout}
#                   ...  timer_use_expr=${wdt_timer_use_expr}
#                   ...  countdown=${countdown_val}
#   Step  2  reset watchdog
#   Step  3  set time delay  1
#   Step  4  verify bios boot  DUT
#   Step  5  verify log util watchdog  DUT  timer_use=${timer_use}  timer_action=hard reset

# verify log watchdog event power down
#   [Arguments]    ${timer_use}  ${countdown_val}
#   Step  1  set watchdog  DUT  cmd=${cmd_set_wdt}
#                   ...  timer_use=${wdt_timer_use["${timer_use}"]}
#                   ...  timer_action=${wdt_timer_action["power down"]}
#                   ...  pre_timer=${wdt_pre_timeout}
#                   ...  timer_use_expr=${wdt_timer_use_expr}
#                   ...  countdown=${countdown_val}
#   Step  3  reset watchdog
#   Step  4  go to openbmc
#   Step  5  set time delay  1
#   Step  6  verify power control  DUT  power_mode=status  power_status=off
#   Step  7  verify power control  DUT  power_mode=on
#   Step  8  verify log util watchdog  DUT  timer_use=${timer_use}  timer_action=power down

# verify log watchdog event power cycle
#   [Arguments]    ${timer_use}  ${countdown_val}
#   Step  1  set watchdog  DUT  cmd=${cmd_set_wdt}
#                   ...  timer_use=${wdt_timer_use["${timer_use}"]}
#                   ...  timer_action=${wdt_timer_action["power cycle"]}
#                   ...  pre_timer=${wdt_pre_timeout}
#                   ...  timer_use_expr=${wdt_timer_use_expr}
#                   ...  countdown=${countdown_val}
#   Step  2  reset watchdog
#   Step  3  set time delay  1
#   Step  4  verify bios boot  DUT
#   Step  5  verify log util watchdog  DUT  timer_use=${timer_use}  timer_action=power cycle

get DIMM information
  [Arguments]  ${DIMM_index}  ${rsp_DIMM}
  Step  1  run ipmi get test  dimm_location  DUT  ${cmd_get_DIMM_info} ${DIMM_index} ${cmd_dimm_dict['DIMM location']}  ${rsp_DIMM["DIMM location"]}
  Step  2  run ipmi get test  dimm_type  DUT  ${cmd_get_DIMM_info} ${DIMM_index} ${cmd_dimm_dict['DIMM type']}  ${rsp_DIMM["DIMM type"]}
  Step  3  run ipmi get test  dimm_speed  DUT  ${cmd_get_DIMM_info} ${DIMM_index} ${cmd_dimm_dict['DIMM speed']}  ${rsp_DIMM["DIMM speed"]}
  Step  4  run ipmi get test  dimm_module_part_num  DUT  ${cmd_get_DIMM_info} ${DIMM_index} ${cmd_dimm_dict['DIMM module part number']}  ${rsp_DIMM["DIMM module part num"]}
  Step  5  run ipmi get test  dimm_module_serial_num  DUT  ${cmd_get_DIMM_info} ${DIMM_index} ${cmd_dimm_dict['DIMM module serial number']}  ${rsp_DIMM["DIMM module serial num"]}
  Step  6  run ipmi get test  dimm_module_manu_id  DUT  ${cmd_get_DIMM_info} ${DIMM_index} ${cmd_dimm_dict['DIMM module manufacture ID']}  ${rsp_DIMM["DIMM module manufacture ID"]}

set DIMM information
  [Arguments]  ${DIMM_index}
  Step  1  run ipmi set cmd  DUT  ${cmd_set_DIMM_info} ${DIMM_index} ${cmd_dimm_dict['DIMM location']} ${cmd_DIMM_location_test}
  Step  2  run ipmi set cmd  DUT  ${cmd_set_DIMM_info} ${DIMM_index} ${cmd_dimm_dict['DIMM type']} ${cmd_DIMM_type_test}
  Step  3  run ipmi set cmd  DUT  ${cmd_set_DIMM_info} ${DIMM_index} ${cmd_dimm_dict['DIMM speed']} ${cmd_DIMM_speed_test}
  Step  4  run ipmi set cmd  DUT  ${cmd_set_DIMM_info} ${DIMM_index} ${cmd_dimm_dict['DIMM module part number']} ${cmd_DIMM_module_part_num_test}
  Step  5  run ipmi set cmd  DUT  ${cmd_set_DIMM_info} ${DIMM_index} ${cmd_dimm_dict['DIMM module serial number']} ${cmd_DIMM_module_serial_num_test}
  Step  6  run ipmi set cmd  DUT  ${cmd_set_DIMM_info} ${DIMM_index} ${cmd_dimm_dict['DIMM module manufacture ID']} ${cmd_DIMM_module_manu_id_test}

get processor information
  [Arguments]  ${processor_index}  ${rsp_proc}
  Step  1  run ipmi get test  proc_name  DUT  ${cmd_get_proc_info} ${processor_index} ${cmd_product_name}  ${rsp_proc['processor name']}
  Step  2  run ipmi get test  proc_basic_info  DUT  ${cmd_get_proc_info} ${processor_index} ${cmd_basic_info}  ${rsp_proc['processor basic info']}

set processor information
  [Arguments]  ${processor_index}
  Step  1  run ipmi set cmd  DUT  ${cmd_set_proc_info} ${processor_index} ${cmd_product_name} ${cmd_proc_name_test}
  Step  2  run ipmi set cmd  DUT  ${cmd_set_proc_info} ${processor_index} ${cmd_basic_info} ${cmd_proc_basic_info_test}

read SCM CPLD REG
  [Arguments]  ${expected_result}
  run_i2ctool  DUT  get  bus=${scm_cpld_bus}  addr=${scm_cpld_addr}  reg=${come_pwr_ctrl_reg}  expected_result=${expected_result}

write SCM CPLD REG
  [Arguments]  ${val}
  run_i2ctool  DUT  set  bus=${scm_cpld_bus}  addr=${scm_cpld_addr}  reg=${come_pwr_ctrl_reg}  val=${val}

read ac psu eeprom
  Step  1  verify psu util  DUT  psu1  get_eeprom_info  ${psu1_eeprom_dict_tc_038}
  Step  2  verify psu util  DUT  psu2  get_eeprom_info  ${psu2_eeprom_dict_tc_038}

read ac psu eeprom minipack2
  Step  1  verify psu util  DUT  psu1  get_eeprom_info  ${psu1_eeprom_dict_tc_038}
  Step  2  verify psu util  DUT  psu2  get_eeprom_info  ${psu2_eeprom_dict_tc_038}
  Step  3  verify psu util  DUT  psu3  get_eeprom_info  ${psu3_eeprom_dict_tc_038}
  Step  4  verify psu util  DUT  psu4  get_eeprom_info  ${psu4_eeprom_dict_tc_038}

check ipv4 address for bmc and cpu
  ${bmc_ipv4} =  get dhcp ip address  DUT  eth0  mode=${OPENBMC_MODE}
  ${cpu_ipv4} =  get dhcp ip address  DUT  eth0  mode=${CENTOS_MODE}
  Set Suite Variable  ${bmc_ipv4}  ${bmc_ipv4}

check ipv6 address for bmc and cpu
  ${bmc_ipv6} =  get dhcp ip address  DUT  eth0  mode=${OPENBMC_MODE}  ipv6=True
  ${cpu_ipv6} =  get dhcp ip address  DUT  eth0  mode=${CENTOS_MODE}  ipv6=True
  Set Suite Variable  ${bmc_ipv6}  ${bmc_ipv6}

read restful fruid via ipv4
  Step  1  verify restful  DUT  restful_url=mb/fruid  ip=${bmc_ipv4}  interface=eth0
  Step  2  verify restful  DUT  restful_url=seutil  ip=${bmc_ipv4}  interface=eth0
  Step  3  verify restful  DUT  restful_url=feutil/all  ip=${bmc_ipv4}  interface=eth0

read restful fruid via ipv6
  Step  1  verify restful  DUT  restful_url=mb/fruid  ip=${bmc_ipv6}  interface=eth0  ipv6=True
  Step  2  verify restful  DUT  restful_url=seutil  ip=${bmc_ipv6}  interface=eth0  ipv6=True
  Step  3  verify restful  DUT  restful_url=feutil/all  ip=${bmc_ipv6}  interface=eth0  ipv6=True

compare restful fruid with fru data dumped in bmc os
  Step  1  verify restful  DUT  restful_url=mb/fruid  ip=${LOCALHOST}  interface=eth0  compare=True
  Step  2  verify restful  DUT  restful_url=feutil/all  ip=${LOCALHOST}  interface=eth0  compare=True
  Step  3  verify restful  DUT  restful_url=seutil  ip=${LOCALHOST}  interface=eth0  compare=True

read restful bmc info via ipv6
  Step  1  verify restful bmc  DUT  ip=${bmc_ipv6}  interface=eth0  ipv6=True

compare bmc info dumped in cpu os
  Step  1  verify restful bmc  DUT  ip=${LOCALHOST}  cmd_get_device_id=${cmd_get_device_id}  compare=True

read restful sensor via ipv6
  Step  1  verify restful sensors  DUT  ip=${bmc_ipv6}  interface=eth0  ipv6=True

compare restful sensor with sensor info dumped in bmc os
  Step  1  verify restful sensors  DUT  ip=${LOCALHOST}  compare=True
  Step  2  sensor read performance test  DUT  ip=${LOCALHOST_SPEC}  compare=True

read restful status via ipv6
  Step  1  verify restful fw  DUT  restful_url=firmware_info/cpld  ip=${bmc_ipv6}  interface=eth0  ipv6=True
  Step  2  verify restful fw  DUT  restful_url=firmware_info/fpga  ip=${bmc_ipv6}  interface=eth0  ipv6=True
  Step  3  verify restful fw  DUT  restful_url=firmware_info/scm  ip=${bmc_ipv6}  interface=eth0  ipv6=True
  Step  4  verify restful presence  DUT  ip=${bmc_ipv6}  interface=eth0  ipv6=True
  #Step  5  verify restful mTerm  DUT  ip=${bmc_ipv6}  interface=eth0  ipv6=True

compare restful status with status dumped in bmc os
  Step  1  verify restful fw  DUT  restful_url=firmware_info/cpld  ip=${LOCALHOST}  compare=True
  Step  2  verify restful fw  DUT  restful_url=firmware_info/fpga  ip=${LOCALHOST}  compare=True
  Step  3  verify restful fw  DUT  restful_url=firmware_info/scm  ip=${LOCALHOST}  compare=True
  Step  4  verify restful presence  DUT  ip=${LOCALHOST}  compare=True
  #Step  5  verify restful mTerm  DUT  ip=${LOCALHOST}  mode=${OPENBMC_MODE}

# check ipv6 address for bmc and cpu and get com-e status
#   Step  1  check ipv6 address for bmc and cpu
#   Step  2  verify restful server  DUT  ip=${bmc_ipv6}  interface=eth0  ipv6=True  status=on

# power off com-e via remote pc and check status
#   Step  1  verify restful server  PC  ip=${bmc_ipv6}  interface=eno2  ipv6=True  action=off  mode=None
#   Step  2  verify restful server  PC  ip=${bmc_ipv6}  interface=eno2  ipv6=True  status=off  mode=None
#   Step  3  go to openbmc
#   Step  4  verify power control  DUT  power_mode=status  power_status=off
#   Step  5  verify no cpu prompt return  DUT
#   Step  6  go to openbmc
#   Step  7  set time delay  10

# power on com-e via remote pc and check status
#   Step  1  verify restful server  PC  ip=${bmc_ipv6}  interface=eno2  ipv6=True  action=on  mode=None  device2=DUT
#   Step  2  verify restful server  PC  ip=${bmc_ipv6}  interface=eno2  ipv6=True  status=on  mode=None
#   Step  3  go to openbmc
#   Step  4  verify power control  DUT  power_mode=status  power_status=on

# power reset com-e via remote pc and check status
#   Step  1  verify restful server  PC  ip=${bmc_ipv6}  interface=eno2  ipv6=True  action=reset  mode=None  device2=DUT
#   Step  2  verify restful server  PC  ip=${bmc_ipv6}  interface=eno2  ipv6=True  status=on  mode=None
#   Step  3  go to openbmc
#   Step  4  verify power control  DUT  power_mode=status  power_status=on

set power reset chassis
  Step  1  go to openbmc
  Step  2  verify power control  DUT  reset  ${power_option}
  Step  3  set time delay  5

set power on chassis
  Step  1  go to openbmc
  Step  2  verify power control  DUT  on
  Step  3  set time delay  5

run all the parameters of bic-util dev_id information
  Step  1  verify bic util  DUT  option=get_dev_id

run all the parameters of bic-util gpio information
  Step  1  verify bic util  DUT  option=get_gpio
  Step  2  verify bic util  DUT  option=get_gpio_config

run all the parameters of bic-util config information
  Step  1  verify bic util  DUT  option=get_config

run all the parameters of bic-util post_code information
  Step  1  verify bic util  DUT  option=get_post_code

run all the parameters of bic-util sdr information
  Step  1  verify bic util  DUT  option=get_sdr

run all the parameters of bic-util sensor information
  Step  1  verify bic util  DUT  option=read_sensor

run all the parameters of bic-util fruid information
  Step  1  verify bic util  DUT  option=read_fruid

run all the parameters of bic-util mac information
  Step  1  verify bic util  DUT  option=read_mac

run all the parameters of version utility
  Step  1  verify fw version  DUT  BMC
  Step  2  verify fw version  DUT  SCM
  Step  3  verify fw version  DUT  CPLD
  Step  4  verify fw version  DUT  FPGA

run command to get fan/psu/debug card/scm status
  Step  1  verify presence util  DUT  ${presence_dict}  ${pem1_presence}  ${pem2_presence}

run command to get fan/psu/pim/scm status
  Step  1  verify presence util  DUT  ${presence_dict}

run all the parameters of psu-util
  Step  1  verify psu util  DUT  psu1  get_psu_info  ${psu1_info_dict_tc_054}
  Step  2  verify psu util  DUT  psu1  get_eeprom_info  ${psu1_eeprom_dict_tc_054}
  Step  3  verify blackbox psu util  DUT  psu1  get_blackbox_info --print
  Step  4  verify psu util  DUT  psu2  get_psu_info  ${psu2_info_dict_tc_054}
  Step  5  verify psu util  DUT  psu2  get_eeprom_info  ${psu2_eeprom_dict_tc_054}
  Step  6  verify blackbox psu util  DUT  psu2  get_blackbox_info --print

run all the parameters of psu-util minipack2
  Step  1  verify psu util  DUT  psu1  get_psu_info  ${psu1_info_dict_tc_054}
  Step  2  verify psu util  DUT  psu1  get_eeprom_info  ${psu1_eeprom_dict_tc_054}
  Step  3  verify blackbox psu util  DUT  psu1  get_blackbox_info --print
  Step  4  verify psu util  DUT  psu2  get_psu_info  ${psu2_info_dict_tc_054}
  Step  5  verify psu util  DUT  psu2  get_eeprom_info  ${psu2_eeprom_dict_tc_054}
  Step  6  verify blackbox psu util  DUT  psu2  get_blackbox_info --print
  Step  7  verify psu util  DUT  psu3  get_psu_info  ${psu3_info_dict_tc_054}
  Step  8  verify psu util  DUT  psu3  get_eeprom_info  ${psu3_eeprom_dict_tc_054}
  Step  9  verify blackbox psu util  DUT  psu3  get_blackbox_info --print
  Step  10  verify psu util  DUT  psu4  get_psu_info  ${psu4_info_dict_tc_054}
  Step  11  verify psu util  DUT  psu4  get_eeprom_info  ${psu4_eeprom_dict_tc_054}
  Step  12  verify blackbox psu util  DUT  psu4  get_blackbox_info --print

#### cloudripper does not support get_blackbox_info option
run all the parameters of psu-util cloudripper
  Step  1  verify psu util  DUT  psu1  get_psu_info
  Step  2  verify psu util  DUT  psu1  get_eeprom_info
  # Step  3  verify psu util  DUT  psu1  get_blackbox_info --print
  Step  4  verify psu util  DUT  psu2  get_psu_info
  Step  5  verify psu util  DUT  psu2  get_eeprom_info
  # Step  6  verify psu util  DUT  psu2  get_blackbox_info --print

run command to get device guid
  Step  1  run ipmi get device guid  DUT  ${cmd_get_device_guid}  ${rsp_device_guid}

run ipmi command "get system info parameters" to get actual bios version
  Step  1  run ipmi get sys info  DUT  ${cmd_get_system_info}  isActualBios=True

run ipmi command "set system info parameters" to set virtual bios version
  Step  1  run ipmi set sys info  DUT  ${cmd_set_system_info}  isActualBios=False

run ipmi command "get system info parameters" to check virtual bios version
  Step  1  run ipmi get sys info  DUT  ${cmd_get_system_info}  isActualBios=False

reboot unit and then get the bios version again
  Step  1  reboot diag os
  Step  2  run ipmi get sys info  DUT  ${cmd_get_system_info}  isActualBios=True

run ipmi command "get lan config"
  Step  1  go to openbmc
  Step  2  get ip address list  DUT  eth0  mode=${OPENBMC_MODE}  ipv6=True
  Step  3  go to centos
  Step  4  run ipmi get cmd  DUT  ${cmd_get_lan_config_1}  ${rsp_get_lan_1}
  Step  5  run ipmi get lan config  DUT  ${cmd_get_lan_config_2}  ${rsp_get_lan_2}  ${rsp_get_lan_2_fail}
  Step  6  go to openbmc

run ipmi command to get sol info
  Step  1  go to centos
  Step  2  run ipmi get cmd  DUT  ${cmd_get_sol_config_1}  ${rsp_get_sol_config_1}
  Step  3  run ipmi get cmd  DUT  ${cmd_get_sol_config_2}  ${rsp_get_sol_config_2}
  Step  4  run ipmi get cmd  DUT  ${cmd_get_sol_config_3}  ${rsp_get_sol_config_3}
  Step  5  run ipmi get cmd  DUT  ${cmd_get_sol_config_4}  ${rsp_get_sol_config_3}
  Step  6  go to openbmc

get board id via command "get board id"
  Step  1  go to centos
  Step  1  run ipmi get test  board_id  DUT  ${cmd_get_board_id}  ${rsp_board_id}
  Step  2  go to openbmc

read port80 record via command "get port80 record"
  Step  1  go to centos
  Step  1  run ipmi get cmd  DUT  ${cmd_get_port80}

get pcie configuration via "get pcie configuration" command
  Step  1  run ipmi get cmd  DUT  ${cmd_get_pcie_config}  ${rsp_get_pcie_config}

issue "set post start" command
  Step  1  run ipmi set cmd  DUT  ${cmd_set_post_start}

issue "set post end" command
  Step  1  run ipmi set cmd  DUT  ${cmd_set_post_end}

# run the command "set ppin"
#   Step  1  run ipmi set cmd  DUT  ${cmd_set_ppin}

get default dimm 0 information via "get dimm information" command
  Step  1  get DIMM information  0  ${rsp_DIMM0}

set dimm 0 info with "set dimm Information" command
  Step  1  set DIMM information  0

get dimm 0 information via "get dimm information" command
  Step  1  get DIMM information  0  ${rsp_DIMM_test}

get default dimm 1 information via "get dimm Information" command
  Step  1  get DIMM information  1  ${rsp_DIMM1}

set dimm 1 info with "set dimm information" command
  Step  1  set DIMM information  1

get dimm 1 information via "get dimm Information" command
  Step  1  get DIMM information  1  ${rsp_DIMM_test}

reboot diag os and check the dimm info should restore to default value
  Step  1  reboot diag os
  Step  2  get DIMM information  0  ${rsp_DIMM0}
  Step  3  get DIMM information  1  ${rsp_DIMM1}
  Step  4  go to openbmc

get default processor 0 information via "get processor 0 information" command
  Step  1  get processor information  0  ${rsp_proc0}

set processor 0 info with "set processor 0 information" command
  Step  1  set processor information  0

get processor 0 information via "get processor 0 information" command
  Step  1  get processor information  0  ${rsp_proc_test}

reboot dut and check the processor info 0 should restore to default value
  Step  1  reboot diag os
  Step  2  get processor information  0  ${rsp_proc0}

get memory information
  Step  1  go to openbmc
  Step  2  test execute command  DUT  test_cmd=${cmd_get_mem_info}  mode=${OPENBMC_MODE}
  Step  3  change dir  path=${bmc_bin_path}
  Step  4  version option h  DUT  test_cmd=${bmc_version_cmd}  mode=${OPENBMC_MODE}
  Step  5  change dir  path=${common_path}

assign memory size to run memory rw test with tool memtester
  Step  1  run memtester  DUT  mem_size=10M  iteration=1

run command to verify sol test
  FOR    ${loop}    IN RANGE    ${sol_test_iteration}
      Step  1  go to centos
      Step  2  test execute command  DUT  ${test_cmd_sol_test}  ${CENTOS_MODE}  ${expected_kernel}
      Step  3  go to openbmc
  END

run command "wedge_power.sh status"
  Step  1  verify power control  DUT  power_mode=status  power_status=on
  Step  2  go to centos

run command to read/write scm cpld reg to power off com-e
  Step  1  go to openbmc
  Step  2  read SCM CPLD REG  expected_result=${power_on_val}
  Step  3  write SCM CPLD REG  val=${power_off_val}
  Step  4  read SCM CPLD REG  expected_result=${power_off_val}
  Step  5  verify power control  DUT  power_mode=status  power_status=off
  Step  6  verify no cpu prompt return  DUT

run command to read/write scm cpld reg to power on com-e
  Step  1  go to openbmc
  Step  2  write SCM CPLD REG  val=${power_on_val}
  Step  3  read SCM CPLD REG  expected_result=${power_on_val}
  Step  4  verify power control  DUT  power_mode=status  power_status=on
  Step  5  verify bios boot  DUT  switch_console_flag=True
  Step  6  go to openbmc

chassis power cycle dut and reset bmc os and check watchdog info
  Step  1  reset power chassis  DUT
  Step  2  reset bmc os  DUT
  Step  3  verify watchdog info  DUT  WDT=${WDT_test1}

run command reboot to reset master bmc and check watchdog info
  Step  1  reboot device
  Step  2  verify watchdog info  DUT  WDT=${WDT_test2}

run command to boot from slave bmc and check watchdog info
  Step  1  switch bmc flash  DUT  Slave
  Step  2  verify watchdog info  DUT  WDT=${WDT_test3}

run command to reset bmc os and check watchdog info
  Step  1  reset bmc os  DUT
  Step  2  verify watchdog info  DUT  WDT=${WDT_test4}

run command reboot to reset slave bmc and check watchdog info
  Step  1  reboot device
  Step  2  verify watchdog info  DUT  WDT=${WDT_test5}

run command to boot from master bmc and check watchdog info
  Step  1  switch bmc flash  DUT  Master
  Step  2  verify watchdog info  DUT  WDT=${WDT_test6}

get board type
  ${gpio_brd_rev0} =  get gpio brd rev0 by board type  DUT
  Set Suite Variable  ${gpio_brd_rev0}  ${gpio_brd_rev0}

chassis power cycle dut and run command to config gpio
  Step  1  reset power chassis  DUT
  Step  2  change dir  ${gpio_test_path}  ${OPENBMC_MODE}
  Step  2  get gpio data  DUT  direction  ${board_rev_direction}
  Step  3  get gpio data  DUT  value  ${gpio_brd_rev0}

run command to config gpio direction to out
  Step  1  set gpio data  DUT  direction  out
  Step  2  get gpio data  DUT  direction  out
  Step  3  get gpio data  DUT  value  0

run command to config value to 1
  Step  1  set gpio data  DUT  value  1
  Step  2  get gpio data  DUT  direction  out
  Step  3  get gpio data  DUT  value  1

run command to config direction to in
  Step  1  set gpio data  DUT  direction  in
  Step  2  get gpio data  DUT  direction  in
  Step  3  get gpio data  DUT  value  ${gpio_brd_rev0}

go to path and check current path
  Step  1  change dir  ${test_path_tc_021}  ${CENTOS_MODE}
  Step  2  verify working dir  DUT  ${test_path_tc_021}  ${CENTOS_MODE}

check master openbmc and check com-e side
  Step  1  verify current boot flash  DUT  Master
  Step  2  go to centos
  Step  3  go to path and check current path
  Step  4  go to openbmc
  Step  5  reboot device
  Step  6  verify working dir  DUT  ${test_path_tc_021}  ${CENTOS_MODE}
  Step  7  go to openbmc

reboot and check dhcp setting info and check ipv6 address
  Step  1  check reboot message  DUT  openbmc  ${dhcp_messages_list}
  Step  2  verify dhcp address  DUT  interface=eth0  ipv6=True
  Step  3  verify ipv6 address  DUT  interface=usb0  expected_result=${usb0_int_bmc['ip_ipv6']}

reboot and check dhcp setting info and check ipv6 address mp2
  Step  1  reboot device
  Step  2  verify dhcp address  DUT  interface=eth0  ipv6=True
  Step  3  verify ipv6 address  DUT  interface=usb0  expected_result=${usb0_int_bmc['ip_ipv6']}

ping dhcp server with eth0
  ${pc_ipv6} =  get ip address from config  PC  ipv6=True
  Step  1  ping6 PC from BMC  ${pc_ipv6}  eth0

using scp command to copy file from BMC to CPU by eth0 ipv6
  Step  1  go to centos
  ${cpu_ipv6} =  get dhcp ip address  DUT  interfaceName=eth0  mode=${CENTOS_MODE}  ipv6=True
  Step  2  copy file from BMC to CPU ipv6  ${cpu_ipv6}  filepath=${workspace}  filename=${usb0_test_file}
              ...   destination_path=/home/  interface=eth0

Check usb0 ipv6 address&mac&ping function
  Step  1  login to centos
  Step  2  switch to openbmc
  Step  3  verify ipv6 address  DUT  interface=usb0  expected_result=${default_bmc_usb0_ipv6_addr}
  Step  4  verify ipv6 address  DUT  interface=usb0  expected_result=${usb0_int_bmc['ip_ipv6']}
  Step  5  verify mac address  DUT  interface=usb0  expected_result=${default_bmc_usb0_mac_addr}
  Step  6  set interface link  interface_name=usb0  status=up  mode=${CENTOS_MODE}
  Step  7  verify ipv6 address  DUT  interface=usb0  expected_result=${usb0_int_cpu['ip_ipv6']}  mode=${CENTOS_MODE}
  Step  8  ping6 BMC from CPU  ${usb0_int_bmc['ip_ipv6']}  ${usb0_int_bmc['interface']}
  Step  9  ping6 CPU from BMC  ${usb0_int_cpu['ip_ipv6']}  ${usb0_int_cpu['interface']}

Using scp command to copy file from BMC to CPU by usb0 ipv6
  Step  1  copy file from BMC to CPU ipv6  ${usb0_int_cpu['ip_ipv6']}  filepath=${workspace}  filename=${usb0_test_file}
              ...   destination_path=/home/  interface=usb0

run command to check size of emmc
  Step  1  check disk exist  DUT  ${emmc_disk_name}  ${emmc_size_keyword}

run command to read and write emmc
  Step  1  create test file  DUT  ${emmc_test_file}  1
  Step  2  test execute command  DUT  test_cmd=echo $?  mode=${OPENBMC_MODE}  expected_result=0
  Step  3  read test emmc  DUT  ${emmc_test_file}
  Step  4  clean up file  DUT  files=${emmc_test_file}

delete test file and change dir
  Step  1  clean up file  DUT  files=${emmc_test_file}
  Step  2  change dir

switch bios flash to Master
    Step  1  go to openbmc
    Step  2  switch bios flash  DUT  Master

power cycle unit and check bios master mode
    Step  1  go to openbmc
    Step  2  reset power chassis  DUT
    Step  3  switch bios flash  DUT  Master 

power cycle unit
    Step  1  go to openbmc
    Step  2  reset power chassis  DUT

switch bios flash to Slave and check version in cpu
    Step  1  verify current bios flash  DUT  Master
    Step  3  verify power control  DUT  power_mode=off
    Step  2  switch bios flash  DUT  Slave
    Step  4  verify power control  DUT  power_mode=on
    Step  5  verify dmidecode bios version  DUT
    Step  6  run ipmi command "get system info parameters" to get actual bios version

check slave bios version and switch bios flash to Master again
    Step  1  go to openbmc
    Step  2  verify current bios flash  DUT  Slave
    Step  3  verify fw version  DUT  BIOS
    Step  5  verify power control  DUT  power_mode=off
    Step  4  switch bios flash  DUT  Master
    Step  6  verify power control  DUT  power_mode=on
    Step  7  verify current bios flash  DUT  Master

# power cycle chassis and boot source should be Master
#     Step  1  reset power chassis  DUT  check_string_flag=True
#     Step  2  verify current bios flash  DUT  Master
#     Step  3  verify fw version  DUT  BIOS

run smbutil command
    ${smbutil_result} =  run util  DUT  smbutil
    Set Suite Variable  ${smbutil_result}  ${smbutil_result}

check smb data match with smbutil command
    Step  1  change dir  ${smb_eeprom_path}
    ${smb_eeprom_result} =  run eeprom tool  DUT  option=d  eeprom_type=SMB
    Step  2  compare util and eeprom  DUT  ${smbutil_result}  ${smb_eeprom_result}

check sim fru data match with weutil command
    Step  1  change dir  ${sim_eeprom_path}
    ${sim_eeprom_result} =  run eeprom tool  DUT  option=d  eeprom_type=SIM
    Step  2  compare util and eeprom  DUT  ${weutil_result}  ${sim_eeprom_result}

run weutil command
  ${weutil_result} =  run util  DUT  weutil
  Set Suite Variable  ${weutil_result}  ${weutil_result}

check smb fru data match with weutil command
  Step  1  change dir  ${smb_eeprom_path}
  ${smb_eeprom_result} =  run eeprom tool  DUT  option=d  eeprom_type=SMB
  Step  2  compare util and eeprom  DUT  ${weutil_result}  ${smb_eeprom_result}

run feutil command
  Step  1  run util  DUT  feutil all
  ${feutil_fcm_result} =  run util  DUT  feutil fcm
  ${feutil_1_result} =  run util  DUT  feutil 1
  ${feutil_2_result} =  run util  DUT  feutil 2
  ${feutil_3_result} =  run util  DUT  feutil 3
  ${feutil_4_result} =  run util  DUT  feutil 4
  Set Suite Variable  ${feutil_fcm}  ${feutil_fcm_result}
  Set Suite Variable  ${feutil_1}  ${feutil_1_result}
  Set Suite Variable  ${feutil_2}  ${feutil_2_result}
  Set Suite Variable  ${feutil_3}  ${feutil_3_result}
  Set Suite Variable  ${feutil_4}  ${feutil_4_result}

run feutil command minipack2
  Step  1  run util  DUT  feutil all
  ${feutil_fcm-t_result} =  run util  DUT  feutil fcm-t
  ${feutil_fcm-b_result} =  run util  DUT  feutil fcm-b
  ${feutil_1_result} =  run util  DUT  feutil 1
  ${feutil_2_result} =  run util  DUT  feutil 2
  ${feutil_3_result} =  run util  DUT  feutil 3
  ${feutil_4_result} =  run util  DUT  feutil 4
  ${feutil_5_result} =  run util  DUT  feutil 5
  ${feutil_6_result} =  run util  DUT  feutil 6
  ${feutil_7_result} =  run util  DUT  feutil 7
  ${feutil_8_result} =  run util  DUT  feutil 8
  Set Suite Variable  ${feutil_fcm-t}  ${feutil_fcm-t_result}
  Set Suite Variable  ${feutil_fcm-b}  ${feutil_fcm-b_result}
  Set Suite Variable  ${feutil_1}  ${feutil_1_result}
  Set Suite Variable  ${feutil_2}  ${feutil_2_result}
  Set Suite Variable  ${feutil_3}  ${feutil_3_result}
  Set Suite Variable  ${feutil_4}  ${feutil_4_result}
  Set Suite Variable  ${feutil_5}  ${feutil_5_result}
  Set Suite Variable  ${feutil_6}  ${feutil_6_result}
  Set Suite Variable  ${feutil_7}  ${feutil_7_result}
  Set Suite Variable  ${feutil_8}  ${feutil_8_result}

check fan and fcm fru data match with feutil command
  Step  1  change dir  ${fan_eeprom_path}
  ${fan1_eeprom} =  run eeprom tool  DUT  option=d  eeprom_type=FAN1  fan=1
  Step  2  compare util and eeprom  DUT   ${feutil_1}  ${fan1_eeprom}
  ${fan2_eeprom} =  run eeprom tool  DUT  option=d  eeprom_type=FAN2  fan=2
  Step  3  compare util and eeprom  DUT  ${feutil_2}  ${fan2_eeprom}
  ${fan3_eeprom} =  run eeprom tool  DUT  option=d  eeprom_type=FAN3  fan=3
  Step  4  compare util and eeprom  DUT  ${feutil_3}  ${fan3_eeprom}
  ${fan4_eeprom} =  run eeprom tool  DUT  option=d  eeprom_type=FAN4  fan=4
  Step  5  compare util and eeprom  DUT  ${feutil_4}  ${fan4_eeprom}
  Step  6  change dir  ${fcm_eeprom_path}
  ${fcm_eeprom} =  run eeprom tool  DUT  option=d  eeprom_type=FCM
  Step  7  compare util and eeprom  DUT  ${feutil_fcm}  ${fcm_eeprom}

check fan and fcm fru data match with feutil command minipack2
  Step  1  change dir  ${fan_eeprom_path}
  ${fan1_eeprom} =  run eeprom tool  DUT  option=d  eeprom_type=FAN1  fan=1
  Step  2  compare util and eeprom  DUT  ${feutil_1}  ${fan1_eeprom}
  ${fan2_eeprom} =  run eeprom tool  DUT  option=d  eeprom_type=FAN2  fan=2
  Step  3  compare util and eeprom  DUT  ${feutil_2}  ${fan2_eeprom}
  ${fan3_eeprom} =  run eeprom tool  DUT  option=d  eeprom_type=FAN3  fan=3
  Step  4  compare util and eeprom  DUT  ${feutil_3}  ${fan3_eeprom}
  ${fan4_eeprom} =  run eeprom tool  DUT  option=d  eeprom_type=FAN4  fan=4
  Step  5  compare util and eeprom  DUT  ${feutil_4}  ${fan4_eeprom}
  ${fan5_eeprom} =  run eeprom tool  DUT  option=d  eeprom_type=FAN5  fan=5
  Step  6  compare util and eeprom  DUT  ${feutil_5}  ${fan5_eeprom}
  ${fan6_eeprom} =  run eeprom tool  DUT  option=d  eeprom_type=FAN6  fan=6
  Step  7  compare util and eeprom  DUT  ${feutil_6}  ${fan6_eeprom}
  ${fan7_eeprom} =  run eeprom tool  DUT  option=d  eeprom_type=FAN7  fan=7
  Step  8  compare util and eeprom  DUT  ${feutil_7}  ${fan7_eeprom}
  ${fan8_eeprom} =  run eeprom tool  DUT  option=d  eeprom_type=FAN8  fan=8
  Step  9  compare util and eeprom  DUT  ${feutil_8}  ${fan8_eeprom}
  Step  10  change dir  ${fcm_b_eeprom_path}
  ${fcm-b_eeprom} =  run eeprom tool  DUT  option=d  eeprom_type=FCM_B
  Step  11  compare util and eeprom  DUT  ${feutil_fcm-b}  ${fcm-b_eeprom}
  Step  12  change dir  ${fcm_t_eeprom_path}
  ${fcm-t_eeprom} =  run eeprom tool  DUT  option=d  eeprom_type=FCM_T
  Step  13  compare util and eeprom  DUT  ${feutil_fcm-t}  ${fcm-t_eeprom}

run seutil command
  ${seutil_result} =  run util  DUT  seutil
  Set Suite Variable  ${seutil_result}  ${seutil_result}

check scm fru data match with seutil command
  Step  1  change dir  ${scm_eeprom_path}
  ${scm_eeprom_result} =  run eeprom tool  DUT  option=d  eeprom_type=SCM
  Step  2  compare util and eeprom  DUT  ${seutil_result}  ${scm_eeprom_result}

run bsm-eutil command
  ${bsmeutil_result} =  run util  DUT  bsm-eutil
  Set Suite Variable  ${bsmeutil_result}  ${bsmeutil_result}

check bsm fru data match with bsm-eutil command
  Step  1  change dir  ${bmc_bin_path}
  Step  2  init diag config  DUT
  Step  3  change dir  ${bsm_eeprom_path}
  ${bsm_eeprom_result} =  run eeprom tool  DUT  option=d  eeprom_type=BSM
  Step  4  compare util and eeprom  DUT  ${bsmeutil_result}  ${bsm_eeprom_result}

run beutil command
    ${beutil_result} =  run util  DUT  beutil
    Set Suite Variable  ${beutil_result}  ${beutil_result}

check bmc data match with beutil command
    Step  1  change dir  ${bmc_eeprom_path}
    ${bmc_eeprom_result} =  run eeprom tool  DUT  option=d  eeprom_type=BMC
    Step  2  compare util and eeprom  DUT  ${beutil_result}  ${bmc_eeprom_result}

run simutil command
    ${simutil_result} =  run util  DUT  simutil
    Set Suite Variable  ${simutil_result}  ${simutil_result}

check sim data match with simutil command
    Step  1  change dir  ${sim_eeprom_path}
    ${sim_eeprom_result} =  run eeprom tool  DUT  option=d  eeprom_type=SIM
    Step  2  compare util and eeprom  ${simutil_result}  ${sim_eeprom_result}

switch bmc flash to Master
    Step  1  switch bmc flash  DUT  Master

check current openbmc is booted from master
    Step  1  verify current boot flash  DUT  Master

switch bmc flash to Master and change dir to default
  Step  1  switch bmc flash  DUT  Master
  Step  2  change dir  mode=${CENTOS_MODE}
  Step  3  go to openbmc

switch bmc flash to Slave then to Master
    Step  1  switch bmc flash  DUT  Slave
    # Step  2  verify fw version  DUT  BMC  ### no need to check slave bmc's version now.
    Step  3  switch bmc flash  DUT  Master

switch bmc flash to Slave then power cycle chassis
    Step  1  switch bmc flash  DUT  Slave
    Step  2  verify fw version  DUT  BMC
    Step  3  reset power chassis  DUT  check_string_flag=True
    Step  4  verify current boot flash  device=DUT  bmc_flash=Master

Reboot OpenBMC three times and Check booting log
    Step  1  check_reboot_error_message  device=DUT  prompt=openbmc  error_messages=${error_messages_list}
    Step  2  check_reboot_error_message  device=DUT  prompt=openbmc  error_messages=${error_messages_list}
    Step  3  check_reboot_error_message  device=DUT  prompt=openbmc  error_messages=${error_messages_list}

power cycle openbmc and check bic log
  FOR    ${loop}    IN RANGE    ${bic_auto_set_test_iteration}
      Step  1  check power cycle message  DUT  ${bic_messages_list}
      Step  2  verify fw version  DUT  BIC
  END

upgrade master bios and check version
    Step  1  switch bios flash  DUT  Master
    Step  2  update bios  DUT  bios_flash=Master  isUpgrade=True

#downgrade master bios and check version
#     Step  1  update bios  DUT  bios_flash=Master  isUpgrade=False

upgrade slave bios and check version
    Step  1  update bios  DUT  bios_flash=Slave  isUpgrade=True

# downgrade slave bios and check version
#     Step  1  update bios  DUT  bios_flash=Slave  isUpgrade=False

switch to master bios
    Step  1  switch bios flash  DUT  Master

prepare BMC images
    Step  1  switch bmc flash  DUT  Master
    Step  2  mount data  dev=/dev/mmcblk0  path=${workspace}  mode=OPENBMC_MODE
    Step  3  create dir  ${workspace}/BMC  ${OPENBMC_MODE}
    Step  4  get dhcp ip address  DUT  eth0  ${OPENBMC_MODE}
    Step  5  download images  DUT  BMC

prepare BMC and diag images
    Step  1  switch bmc flash  DUT  Master
    Step  2  mount data  dev=/dev/mmcblk0  path=${workspace}  mode=OPENBMC_MODE
    Step  3  create dir  ${workspace}/BMC  ${OPENBMC_MODE}
    Step  4  get dhcp ip address  DUT  eth0  ${OPENBMC_MODE}
    Step  5  download images  DUT  BMC
    Step  6  switch to centos
    Step  7  download images  DUT  DIAG
    Step  8  switch to openbmc

install diag package and init diag
    Step  1  switch to centos
    Step  2  clean diag rpm package  DUT
    Step  3  install diag image  DUT  ${diag_image_file}
    Step  4  switch to openbmc
    Step  5  change dir  ${bmc_bin_path}
    Step  6  init diag config  DUT

upgrade master bmc and check version
    Step  1  update bmc  DUT  bmc_flash=Master  isUpgrade=True

downgrade master bmc and check version
    Step  1  update bmc  DUT  bmc_flash=Master  isUpgrade=False

upgrade slave bmc and check version
    Step  1  update bmc  DUT  bmc_flash=Slave  isUpgrade=True

# downgrade slave bmc and check version
#     Step  1  update bmc  DUT  bmc_flash=Slave  isUpgrade=False

FPGA upgrade and check FPGA version
    Step  1  update fpga  DUT  isUpgrade=True

# FPGA downgrade and check FPGA version
#     Step  1  update fpga  DUT  isUpgrade=False

FPGA upgrade and check FPGA version cloudripper
    Step  1  update fpga cloudripper  DUT  isUpgrade=True

# FPGA downgrade and check FPGA version cloudripper
#     Step  1  update fpga cloudripper  DUT  isUpgrade=False

FPGA upgrade and check FPGA version minipack2
    Step  1  update fpga minipack2  DUT  isUpgrade=True

FPGA downgrade and check FPGA version minipack2
    Step  1  update fpga minipack2  DUT  isUpgrade=False

prepare openbmc mac global variable
    Step  1  prepare store eeprom  ${mac_eeprom_path}  ${mac_eeprom_type}
    ${local_mac_address_without_separator}=  get_eeprom_value  DUT  cmd=${cmd_read_mac_from_eeprom}  key=local_mac_address
    ${local_mac_address_with_separator}=  change_mac_fomat  DUT  original=${local_mac_address_without_separator}
    Set Environment Variable  local_mac_address_without_separator_1  ${local_mac_address_without_separator}
    Set Environment Variable  local_mac_address_with_separator_1  ${local_mac_address_with_separator}

Check OpenBMC MAC address in SMB eeprom by Diag command
    Step  1  verify_mac_address  DUT  interface=eth0  expected_result=%{local_mac_address_with_separator_1}

Use Diag tool eeprom to Update OpenBMC MAC address
    ${random_mac_without_separator}=  create_random_mac_address  DUT  prompt=format_without_separator
    ${random_mac_with_separator}=  change_mac_fomat  DUT  original=${random_mac_without_separator}
    ${local_mac_address_read_by_eeprom.cfg}=  get_eeprom_value  DUT  cmd=cat eeprom.cfg  key=local_mac_address
    Set Environment Variable  random_mac_without_separator_1  ${random_mac_without_separator}
    Set Environment Variable  random_mac_with_separator_1  ${random_mac_with_separator}
    Step  1  modify_eeprom_cfg_string  DUT  original=${local_mac_address_read_by_eeprom.cfg}  modified=%{random_mac_without_separator_1}
    Step  2  run eeprom tool  DUT  option=w  eeprom_type=${mac_eeprom_type}
    ${local_mac_address_after_modify}=  get_eeprom_value  DUT  cmd=${cmd_read_mac_from_eeprom}  key=local_mac_address
    Step  3  Should Be Equal  ${local_mac_address_after_modify}  %{random_mac_without_separator_1}  expect != real
    ${ifconfig_get_mac_address}=  openbmc_lib.get_mac_address  DUT  prompt=openbmc  interface=eth0
    Step  4  Should Not Be Equal  ${ifconfig_get_mac_address}  %{random_mac_with_separator_1}

Reset openbmc os to check mac address
    Step  1  reboot device
    Step  2  change dir  ${mac_eeprom_path}
    ${local_mac_address_after_modify_reset}=  get_eeprom_value  DUT  cmd=${cmd_read_mac_from_eeprom}  key=local_mac_address
    ${ifconfig_get_mac_address_reset}=  openbmc_lib.get_mac_address  DUT  prompt=openbmc  interface=eth0
    Step  3  Should Be Equal  ${local_mac_address_after_modify_reset}  %{random_mac_without_separator_1}
    Step  4  Should Be Equal  ${ifconfig_get_mac_address_reset}  %{random_mac_with_separator_1}
    Step  5  verify_mac_address  DUT  interface=usb0  expected_result=${default_bmc_usb0_mac_addr}

Power cycle chassis to check mac address
    Step  1  reset_power_chassis  DUT
    Step  2  change dir  ${mac_eeprom_path}
    ${local_mac_address_after_modify_powercycle}=  get_eeprom_value  DUT  cmd=${cmd_read_mac_from_eeprom}  key=local_mac_address
    ${ifconfig_get_mac_address_powercycle}=  openbmc_lib.get_mac_address  DUT  prompt=openbmc  interface=eth0
    Step  3  Should Be Equal  ${local_mac_address_after_modify_powercycle}  %{random_mac_without_separator_1}
    Step  4  Should Be Equal  ${ifconfig_get_mac_address_powercycle}  %{random_mac_with_separator_1}
    Step  5  verify_mac_address  DUT  interface=usb0  expected_result=${default_bmc_usb0_mac_addr}

Use Diag tool eeprom to Update OpenBMC MAC address back to previous value
    Step  1  change dir  ${mac_eeprom_path}
    ${local_mac_address_without_separator}=  get_eeprom_value  DUT  cmd=${cmd_read_mac_from_eeprom}  key=local_mac_address
    ${local_mac_address_with_separator}=  change_mac_fomat  DUT  original=${local_mac_address_without_separator}
    ${local_mac_address_read_by_eeprom.cfg}=  get_eeprom_value  DUT  cmd=cat eeprom.cfg  key=local_mac_address
    Step  2  modify_eeprom_cfg_string  DUT  original=${local_mac_address_read_by_eeprom.cfg}  modified=%{local_mac_address_without_separator_1}
    Step  3  run eeprom tool  DUT  option=w  eeprom_type=${mac_eeprom_type}
    ${local_mac_address_after_modify}=  get_eeprom_value  DUT  cmd=${cmd_read_mac_from_eeprom}  key=local_mac_address
    Step  4  Should Be Equal  ${local_mac_address_after_modify}  %{local_mac_address_without_separator_1}  expect != real
    ${ifconfig_get_mac_address}=  openbmc_lib.get_mac_address  DUT  prompt=openbmc  interface=eth0
    Step  5  Should Not Be Equal  ${ifconfig_get_mac_address}  %{local_mac_address_with_separator_1}

Reset openbmc os to check mac address again
    Step  1  reboot device
    Step  2  change dir  ${mac_eeprom_path}
    ${local_mac_address_after_modify_reset}=  get_eeprom_value  DUT  cmd=${cmd_read_mac_from_eeprom}  key=local_mac_address
    ${ifconfig_get_mac_address_reset}=  openbmc_lib.get_mac_address  DUT  prompt=openbmc  interface=eth0
    Step  3  Should Be Equal  ${local_mac_address_after_modify_reset}  %{local_mac_address_without_separator_1}
    Step  4  Should Be Equal  ${ifconfig_get_mac_address_reset}  %{local_mac_address_with_separator_1}
    Step  5  verify_mac_address  DUT  interface=usb0  expected_result=${default_bmc_usb0_mac_addr}

write OpenBMC MAC address back to original value
    Step  1  change dir  ${mac_eeprom_path}
    ${local_mac_address_read_by_eeprom.cfg}=  get_eeprom_value  DUT  cmd=cat eeprom.cfg  key=local_mac_address
    Step  2  modify_eeprom_cfg_string  DUT  original=${local_mac_address_read_by_eeprom.cfg}  modified=%{local_mac_address_without_separator_1}
    Step  3  run eeprom tool  DUT  option=w  eeprom_type=${mac_eeprom_type}
    Step  4  reset_power_chassis  DUT

upgrade bic and check version
    Step  1  update bic  DUT  bmc_flash=Master  isUpgrade=True

downgrade bic and check version
    Step  1  update bic  DUT  bmc_flash=Master  isUpgrade=False

power cycle chassis from Master OpenBMC and boot source should be Master
    Step  1  reset power chassis  DUT  check_string_flag=True
    Step  2  switch bmc flash  DUT  Master

CPLD upgrade and check CPLD version
    Step  1  update CPLD  DUT  update_mode=hw  isUpgrade=True

CPLD upgrade and check CPLD version minipack2
    Step  1  update CPLD minipack2  DUT  isUpgrade=True
    #Step  2  reset power chassis  DUT

CPLD downgrade and check CPLD version minipack2
    Step  1  update CPLD minipack2  DUT  isUpgrade=False
    #Step  2  reset power chassis  DUT

CPLD upgrade and check CPLD version cloudripper
    Step  1  update CPLD  DUT  update_mode=sw  isUpgrade=True

CPLD downgrade and check CPLD version
    Step  1  update CPLD  DUT  update_mode=hw  isUpgrade=False

run command to enable mdio and read reg
    Step  1  go to openbmc
    Step  2  run enable mdio  DUT
    Step  3  read mdio  DUT  ${mdio_reg_test}  ${mdio_0xe_default}
    Step  4  read mdio rsp  DUT  ${mac_second}  ${mdio_0x0_reg_test}  ${mac_second}  ${mdio_0x0_default}

run command to write and read mdio reg
    Step  1  write mdio  DUT  ${mdio_reg_test}  ${mdio_0xe_test1}
    Step  2  read mdio  DUT  ${mdio_reg_test}  ${mdio_0xe_test1}
    Step  3  write mdio rsp  DUT  ${mac_second}  ${mdio_0x0_reg_test}  ${mdio_reg_test1}  ${mdio_0xe_test1}  ${mdio_0x0_reg_test}
    Step  4  read mdio rsp  DUT  ${mac_second}  ${mdio_0x0_reg_test}  ${mac_second}  ${mdio_0x0_default}
    Step  5  read mdio rsp  DUT  ${mac_first}  ${mdio_0x1_reg_test}  ${mac_second}  ${mdio_0x0_default}

run command to write and read mdio reg again
    Step  1  write mdio  DUT  ${mdio_reg_test}  ${mdio_0xe_test2}
    Step  2  read mdio  DUT  ${mdio_reg_test}  ${mdio_0xe_test2}
    Step  3  write mdio rsp  DUT  ${mac_first}  ${mdio_0x1_reg_test}  ${mdio_reg_test1}  ${mdio_0xe_test1}  ${mdio_0x0_reg_test}
    Step  4  read mdio rsp  DUT  ${mac_first}  ${mdio_0x1_reg_test}  ${mac_second}  ${mdio_0x0_default}
    Step  5  read mdio rsp  DUT  ${mac_first}  ${mdio_0x1_reg_test}  ${mdio_reg_test2}  ${mdio_0x0_reg_test}
    Step  6  write mdio rsp  DUT  ${mac_first}  ${mdio_0x1_reg_test}  ${mdio_reg_test2}  ${mdio_reg_test3}  ${mdio_reg_test3}
    Step  7  read mdio rsp  DUT  ${mac_first}  ${mdio_0x1_reg_test}  ${mdio_reg_test2}  ${mdio_reg_test3}
    Step  8  read mdio rsp  DUT  ${mac_first}  ${mdio_0x1_reg_test}  ${mac_second}  ${mdio_0x0_reg_test}
    Step  9  write mdio rsp  DUT  ${mac_first}  ${mdio_0x1_reg_test}  ${mdio_reg_test2}  ${mdio_0xe_test1}  ${mdio_0x0_reg_test}
    Step  10  read mdio rsp  DUT  ${mac_first}  ${mdio_0x1_reg_test}  ${mdio_reg_test2}  ${mdio_0x0_reg_test}
    Step  11  read mdio rsp  DUT  ${mac_first}  ${mdio_0x1_reg_test}  ${mac_second}  ${mdio_0x0_default}

run command to write mdio to default value
    Step  1  write mdio  DUT  ${mdio_reg_test}  ${mdio_0xe_default}
    Step  2  set eth0 status  DUT  ${eth_tool}

run command to read mdio reg minipack2
    Step  1  go to openbmc
    Step  2  set eth0 status  DUT  ${eth_tool_down}
    Step  3  run mdio util  DUT  ${mdio_bus_2}  ${mdio_reg_test_mp2}  r  ${mdio_0xe_default}

run command to write and read mdio reg minipack2
    Step  1  run mdio util  DUT  ${mdio_bus_2}  ${mdio_reg_test_mp2}  w  ${mdio_0xe_test1}
    Step  2  run mdio util  DUT  ${mdio_bus_2}  ${mdio_reg_test_mp2}  r  ${mdio_0xe_test1}

run command to write and read mdio reg again minipack2
    Step  1  run mdio util  DUT  ${mdio_bus_2}  ${mdio_reg_test_mp2}  w  ${mdio_0xe_test2}
    Step  2  run mdio util  DUT  ${mdio_bus_2}  ${mdio_reg_test_mp2}  r  ${mdio_0xe_test2}

run command to write mdio to default value minipack2
    Step  1  run mdio util  DUT  ${mdio_bus_2}  ${mdio_reg_test_mp2}  w  ${mdio_0xe_default}
    Step  2  set eth0 status  DUT  ${eth_tool}

run command to read mdio reg cloudripper
    Step  1  go to openbmc
    Step  2  run mdio util  DUT  ${mdio_bus_2}  ${mdio_reg_test_mp2}  r  ${mdio_0xe_default}
    Step  3  run mdio util  DUT  ${mdio_bus_4}  ${mdio_reg_test_cr}  r  ${mdio_0xe_default}

run command to write and read mdio reg cloudripper
    Step  1  run mdio util  DUT  ${mdio_bus_2}  ${mdio_reg_test_mp2}  w  ${mdio_0xe_test1}
    Step  2  run mdio util  DUT  ${mdio_bus_2}  ${mdio_reg_test_mp2}  r  ${mdio_0xe_test1}
    Step  3  run mdio util  DUT  ${mdio_bus_4}  ${mdio_reg_test_cr}  w  ${mdio_0xe_test1}
    Step  4  run mdio util  DUT  ${mdio_bus_4}  ${mdio_reg_test_cr}  r  ${mdio_0xe_test1}

run command to write and read mdio reg again cloudripper
    Step  1  run mdio util  DUT  ${mdio_bus_2}  ${mdio_reg_test_mp2}  w  ${mdio_0xe_test2}
    Step  2  run mdio util  DUT  ${mdio_bus_2}  ${mdio_reg_test_mp2}  r  ${mdio_0xe_test2}
    Step  3  run mdio util  DUT  ${mdio_bus_4}  ${mdio_reg_test_cr}  w  ${mdio_0xe_test2}
    Step  4  run mdio util  DUT  ${mdio_bus_4}  ${mdio_reg_test_cr}  r  ${mdio_0xe_test2}

run command to write mdio to default value cloudripper
    Step  1  run mdio util  DUT  ${mdio_bus_2}  ${mdio_reg_test_mp2}  w  ${mdio_0xe_default}
    Step  2  run mdio util  DUT  ${mdio_bus_4}  ${mdio_reg_test_cr}  w  ${mdio_0xe_default}

run tpm script
    Step  1  change dir  ${workspace}/TPM
    ${TPM_directory} =  untar file  DUT  TPM  ${tpm_untar_keyword}
    Set Suite Variable  ${TPM_directory}  ${TPM_directory}
    Step  2  prepare tpm test  DUT
    Step  3  run tpm test all  DUT  ${TPM_directory}  ${tpm_pass_keyword}  ${tpm_result}

clean tmp script and change dir
    Step  1  clean up file  DUT  ${workspace}/TPM/${TPM_directory}  isDir=True
    Step  2  clean images  DUT  TPM
    Step  3  change dir

# verify bios get set bootorder 1st
#     Step  1  run ipmi get cmd  DUT  ${cmd_get_bios_boot_order}  expected_result=01 01 02 00 03 04
#     Step  2  run ipmi set cmd  DUT  ipmitool raw 0x30 0x52 0x01 0x02 0x01 0x00 0x03 0x04
#     Step  3  run ipmi get cmd  DUT  ${cmd_get_bios_boot_order}  expected_result=01 02 01 00 03 04

# reboot and verify bios setup bootorder 1st
#     Step  1  enter bios setup  DUT
#     Step  2  send key  DUT  KEY_LEFT  ${2}
#     Step  3  verify menu bios bootorder  DUT  boundary_line=<match all>  bootorder=${bios_boot_order_default}
#     Step  4  exit bios setup  DUT

# verify bios get set bootorder 2nd
#     Step  1  enter bios setup  DUT
#     Step  2  send key  DUT  KEY_LEFT  ${1}
#     Step  3  enter menu bios boot override  DUT  boundary_line=<match all>  p1=${boot_override_keyword}
#     Step  4  run ipmi get cmd  DUT  ${cmd_get_bios_boot_order}  expected_result=01 01 02 00 03 04  ##01 02 01 00 03 04
#     Step  2  run ipmi set cmd  DUT  ipmitool raw 0x30 0x52 0x01 0x00 0x01 0x02 0x03 0x04
#     Step  3  run ipmi get cmd  DUT  ${cmd_get_bios_boot_order}  expected_result=01 00 01 02 03 04

# reboot and verify bios setup bootorder 2nd
#     Step  1  enter bios setup  DUT
#     Step  2  send key  DUT  KEY_LEFT  ${2}
#     Step  3  verify menu bios bootorder  DUT  boundary_line=<match all>  bootorder=${bios_boot_order_default}  ##${bios_boot_order_test_2nd}
#     Step  4  exit bios setup  DUT

# verify bios get set bootorder 3rd
#     Step  1  enter bios setup  DUT
#     Step  2  send key  DUT  KEY_LEFT  ${1}
#     Step  3  enter menu bios boot override  DUT  boundary_line=<match all>  p1=${boot_override_keyword}
#     Step  4  run ipmi get cmd  DUT  ${cmd_get_bios_boot_order}  expected_result=01 01 02 00 03 04  ##01 00 01 02 03 04
#     Step  2  run ipmi set cmd  DUT  ipmitool raw 0x30 0x52 0x01 0x03 0x01 0x02 0x00 0x04
#     Step  3  run ipmi get cmd  DUT  ${cmd_get_bios_boot_order}  expected_result=01 03 01 02 00 04

# reboot and verify bios setup bootorder 3rd
#     Step  1  enter bios setup  DUT
#     Step  2  send key  DUT  KEY_LEFT  ${2}
#     Step  3  verify menu bios bootorder  DUT  boundary_line=<match all>  bootorder=${bios_boot_order_default}  ##${bios_boot_order_test_3rd}
#     Step  4  exit bios setup  DUT

# verify bios get set bootorder 4th
#     Step  1  enter bios setup  DUT
#     Step  2  send key  DUT  KEY_LEFT  ${1}
#     Step  3  enter menu bios boot override  DUT  boundary_line=<match all>  p1=${boot_override_keyword}
#     Step  4  run ipmi get cmd  DUT  ${cmd_get_bios_boot_order}  expected_result=01 01 02 00 03 04  ##01 03 01 02 00 04
#     Step  2  run ipmi set cmd  DUT  ipmitool raw 0x30 0x52 0x01 0x04 0x01 0x02 0x00 0x03
#     Step  3  run ipmi get cmd  DUT  ${cmd_get_bios_boot_order}  expected_result=01 04 01 02 00 03

# reboot and verify bios setup bootorder 4th
#     Step  1  enter bios setup  DUT
#     Step  2  send key  DUT  KEY_LEFT  ${2}
#     Step  3  verify menu bios bootorder  DUT  boundary_line=<match all>  bootorder=${bios_boot_order_default}  ##${bios_boot_order_test_4th}
#     Step  4  exit bios setup  DUT

# verify bios get set bootorder 5th
#     Step  1  enter bios setup  DUT
#     Step  2  send key  DUT  KEY_LEFT  ${1}
#     Step  3  enter menu bios boot override  DUT  boundary_line=<match all>  p1=${boot_override_keyword}
#     Step  4  run ipmi get cmd  DUT  ${cmd_get_bios_boot_order}  expected_result=01 01 02 00 03 04  ##01 04 01 02 00 03
#     Step  2  run ipmi set cmd  DUT  ipmitool raw 0x30 0x52 0x01 0x02 0x01 0x00 0x03 0x04
#     Step  3  run ipmi get cmd  DUT  ${cmd_get_bios_boot_order}  expected_result=01 02 01 00 03 04

# reboot and verify bios setup bootorder 5th
#     Step  1  enter bios setup  DUT
#     Step  2  send key  DUT  KEY_LEFT  ${2}
#     Step  3  verify menu bios bootorder  DUT  boundary_line=<match all>  bootorder=${bios_boot_order_default}  ##${bios_boot_order_test_5th}
#     Step  4  exit bios setup  DUT

# verify bios get set bootorder 6th
#     Step  1  enter bios setup  DUT
#     Step  2  send key  DUT  KEY_LEFT  ${1}
#     Step  3  enter menu bios boot override  DUT  boundary_line=<match all>  p1=${boot_override_keyword}
#     Step  4  run ipmi get cmd  DUT  ${cmd_get_bios_boot_order}  expected_result=01 01 02 00 03 04  ##01 02 01 00 03 04
#     Step  2  run ipmi set cmd  DUT  ipmitool raw 0x30 0x52 0x01 0x09 0x02 0x00 0x03 0x04
#     Step  3  run ipmi get cmd  DUT  ${cmd_get_bios_boot_order}  expected_result=01 09 02 00 03 04

# reboot and verify bios setup bootorder 6th
#     Step  1  enter bios setup  DUT
#     Step  2  send key  DUT  KEY_LEFT  ${2}
#     Step  3  verify menu bios bootorder  DUT  boundary_line=<match all>  bootorder=${bios_boot_order_default}  ##${bios_boot_order_test_6th}
#     Step  4  exit bios setup  DUT

# change bios boot order to default
#     Step  1  go to openbmc
#     Step  2  verify power control  DUT  power_mode=reset
#     Step  1  run ipmi set cmd  DUT  ipmitool raw 0x30 0x52 0x01 0x01 0x02 0x00 0x03 0x04

Reboot OpenBMC and Check the rackmon service
    Step  1  reboot device
    Step  2  check cmd output message  DUT  cmd=ps | grep rack    messages_list=${rackmon_service_messages_list}

Check /tty/USB0 can be found
    Step   1  check cmd output message  DUT  cmd=ls /dev/tty*    messages_list=ttyUSB0

prepare PSU images
    Step  1  prepare images  PSU
    ${psu_power_on} =  check psu power on  DUT
    Set Suite Variable  ${psu_power_on}  ${psu_power_on}

prepare dc PSU images
    Step  1  prepare images  PSU
    ${psu_power_on} =  check dc psu power on  DUT
    Set Suite Variable  ${psu_power_on}  ${psu_power_on}

upgrade psu1 fw
    Step  1  update psu fw  DUT  psu1  ${psu_type}  isUpgrade=True

downgrade psu1 fw
    Step  1  update psu fw  DUT  psu1  ${psu_type}  isUpgrade=False

upgrade psu2 fw
    Step  1  update psu fw  DUT  psu2  ${psu_type}  isUpgrade=True

downgrade psu2 fw
    Step  1  update psu fw  DUT  psu2  ${psu_type}  isUpgrade=False

upgrade psu3 fw
    Step  1  update psu fw  DUT  psu3  ${psu_type}  isUpgrade=True

downgrade psu3 fw
    Step  1  update psu fw  DUT  psu3  ${psu_type}  isUpgrade=False

upgrade psu4 fw
    Step  1  update psu fw  DUT  psu4  ${psu_type}  isUpgrade=True

downgrade psu4 fw
    Step  1  update psu fw  DUT  psu4  ${psu_type}  isUpgrade=False

chassis power cycle and check psu info and status if psu power on
    Run keyword if  ${psu_power_on} == True  chassis power cycle and check psu info and status

chassis power cycle and check psu info and status
    Step  1  reset power chassis  DUT  check_string_flag=True
    FOR    ${psu}    IN RANGE    ${1}  ${PSU_NUM}+1
        Step  1  verify psu util  DUT  psu${psu}  get_psu_info  ${psu${psu}_info_dict_tc_054}  ###${psu1_info_dict_tc_054}
        Step  2  verify sensor util  DUT  psu${psu}  force  ${psu_type}  True
    END

upgrade dc psu1 fw
    Step  1  update dc psu fw  DUT  psu1  ${psu_type}  isUpgrade=True

downgrade dc psu1 fw
    Step  1  update dc psu fw  DUT  psu1  ${psu_type}  isUpgrade=False

upgrade dc psu2 fw
    Step  1  update dc psu fw  DUT  psu2  ${psu_type}  isUpgrade=True

downgrade dc psu2 fw
    Step  1  update dc psu fw  DUT  psu2  ${psu_type}  isUpgrade=False

upgrade dc psu3 fw
    Step  1  update dc psu fw  DUT  psu3  ${psu_type}  isUpgrade=True

downgrade dc psu3 fw
    Step  1  update dc psu fw  DUT  psu3  ${psu_type}  isUpgrade=False

upgrade dc psu4 fw
    Step  1  update dc psu fw  DUT  psu4  ${psu_type}  isUpgrade=True

downgrade dc psu4 fw
    Step  1  update dc psu fw  DUT  psu4  ${psu_type}  isUpgrade=False

check pem presence device
    ${pem1_presence} =  check pem presence  DUT  pem1
    ${pem2_presence} =  check pem presence  DUT  pem2
    Set Suite Variable  ${pem1_presence}  ${pem1_presence}
    Set Suite Variable  ${pem2_presence}  ${pem2_presence}

set false pem device
    Set Suite Variable  ${pem1_presence}  ${FALSE}
    Set Suite Variable  ${pem2_presence}  ${FALSE}

prepare CIT scripts and check pem presence
	Step  1  prepare cit package  DUT  CIT  ${scp_ip}  ${scp_username}  ${scp_password}  ${dhcp_prompt}
    Step  2  prepare images  CIT
    Run keyword if  ${has_pem}  check pem presence device  ELSE  set false pem device

install and run cit test
    #Step  1  wedge400c run sdk script  exit_flag=False
    Step  1  go to openbmc
    Step  2  change dir  ${workspace}/CIT
    ${CIT_directory} =  untar file  DUT  CIT
    Set Suite Variable  ${CIT_directory}  ${CIT_directory}
    Step  3  copy file on device  DUT  ${CIT_directory}  ${local_tool_path}
    Step  4  copy file on device  DUT  ${CIT_directory}/${cit_tool}  ${python_path}
    Step  5  check power type and store  DUT
    Step  6  change dir  ${local_tool_path}/${CIT_directory}
	Step  7  set the log level to debug  DUT  ${log_debug_level}
    Step  8  run cit test  DUT  ${cit_test_cmd}  ${pem1_presence}  ${pem2_presence}

install and run cit test w400
    Step  1  go to openbmc
    Step  2  change dir  ${workspace}/CIT
    ${CIT_directory} =  untar file  DUT  CIT
    Set Suite Variable  ${CIT_directory}  ${CIT_directory}
    Step  3  copy file on device  DUT  ${CIT_directory}  ${local_tool_path}
    Step  4  copy file on device  DUT  ${CIT_directory}/${cit_tool}  ${python_path}
    Step  5  check power type and store  DUT
    Step  6  change dir  ${local_tool_path}/${CIT_directory}
	Step  7  set the log level to debug  DUT  ${log_debug_level}
    Step  8  run cit test  DUT  ${cit_test_cmd}  ${pem1_presence}  ${pem2_presence}

install and run cit test mp2
    Step  1  go to openbmc
    Step  2  change dir  ${workspace}/CIT
    ${CIT_directory} =  untar file  DUT  CIT
    Set Suite Variable  ${CIT_directory}  ${CIT_directory}
    Step  3  copy file on device  DUT  ${CIT_directory}  ${local_tool_path}
    Step  4  copy file on device  DUT  ${CIT_directory}/${cit_tool}  ${python_path}
    Step  5  check power type and store  DUT
    Step  6  change dir  ${local_tool_path}/${CIT_directory}
	Step  7  set the log level to debug  DUT  ${log_debug_level}
    Step  8  run cit test  DUT  ${cit_test_cmd}  ${pem1_presence}  ${pem2_presence}

install and run cit test mp3
    Step  1  go to openbmc
    Step  2  change dir  ${workspace}/CIT
    ${CIT_directory} =  untar file  DUT  CIT
    Set Suite Variable  ${CIT_directory}  ${CIT_directory}
    Step  3  copy file on device  DUT  ${CIT_directory}  ${local_tool_path}
    Step  4  copy file on device  DUT  ${CIT_directory}/${cit_tool}  ${python_path}
    Step  5  check power type and store  DUT
    Step  6  change dir  ${local_tool_path}/${CIT_directory}
    Step  7  set the log level to debug  DUT  ${log_debug_level}
    Step  8  run cit test  DUT  ${cit_test_cmd}  ${pem1_presence}  ${pem2_presence}

install and run cit test minerva
    Step  1  go to openbmc
    Step  2  change dir  ${workspace}/CIT
    ${CIT_directory} =  untar file  DUT  CIT
    Set Suite Variable  ${CIT_directory}  ${CIT_directory}
    Step  3  copy file on device  DUT  ${CIT_directory}  ${local_tool_path}
    Step  4  copy file on device  DUT  ${CIT_directory}/${cit_tool}  ${python_path}
    Step  5  check power type and store  DUT
    Step  6  change dir  ${local_tool_path}/${CIT_directory}
    Step  7  set the log level to debug  DUT  ${log_debug_level}
    Step  8  run cit test  DUT  ${cit_test_cmd}  ${pem1_presence}  ${pem2_presence}

clean cit script and change dir
	Step  1  copy cit log to data1  DUT  ${cit_log_file}
    Step  2  change dir
    Step  3  clean up file  DUT  ${workspace}/CIT/*  isDir=True
    Step  4  clean images  DUT  CIT

run command and check output info
    Step  1  check spi util output  DUT  ${str_1}  ${str_2}

# set boot order and reboot to check 1st
#     Step  1  run ipmi get cmd  DUT  ${cmd_get_bios_boot_order}  expected_result=01 01 02 00 03 04
#     Step  2  enter bios setup  DUT
#     Step  3  send key  DUT  KEY_LEFT  ${2}
#     Step  4  enter menu bios boot order  DUT  boundary_line=<match all>  target_list=${bios_boot_order_test_1st_list}  ##Hard Disk:CentOS  (,Network:UEFI: IPv4,USB,CD/DVD,Other
#     Step  5  send key  DUT  KEY_RIGHT  ${1}
#     Step  6  save bios setup  DUT

# set boot order and reboot to check 2nd
#     Step  1  run ipmi get cmd  DUT  ${cmd_get_bios_boot_order}  expected_result=01 02 01 00 03 04
#     Step  2  enter bios setup  DUT
#     Step  3  send key  DUT  KEY_LEFT  ${2}
#     Step  4  enter menu bios boot order  DUT  boundary_line=<match all>  target_list=${bios_boot_order_test_2nd_list}  ##USB,Network:UEFI: IPv4,Hard Disk:CentOS  (,CD/DVD,Other
#     Step  5  send key  DUT  KEY_RIGHT  ${1}
#     Step  6  save bios setup  DUT

# set boot order and reboot to check 3rd
#     Step  1  run ipmi get cmd  DUT  ${cmd_get_bios_boot_order}  expected_result=01 00 01 02 03 04
#     Step  2  enter bios setup  DUT
#     Step  3  send key  DUT  KEY_LEFT  ${2}
#     Step  4  enter menu bios boot order  DUT  boundary_line=<match all>  target_list=${bios_boot_order_test_3rd_list}  ##CD/DVD,Network:UEFI: IPv4,Hard Disk:CentOS  (,USB,Other
#     Step  5  send key  DUT  KEY_RIGHT  ${1}
#     Step  6  save bios setup  DUT

# set boot order and reboot to check 4th
#     Step  1  run ipmi get cmd  DUT  ${cmd_get_bios_boot_order}  expected_result=01 03 01 02 00 04
#     Step  2  enter bios setup  DUT
#     Step  3  send key  DUT  KEY_LEFT  ${2}
#     Step  4  enter menu bios boot order  DUT  boundary_line=<match all>  target_list=${bios_boot_order_test_4th_list}  ##Other,Network:UEFI: IPv4,Hard Disk:CentOS  (,USB,CD/DVD
#     Step  5  send key  DUT  KEY_RIGHT  ${1}
#     Step  6  save bios setup  DUT

# set boot order and reboot to check 5th
#     Step  1  run ipmi get cmd  DUT  ${cmd_get_bios_boot_order}  expected_result=01 04 01 02 00 03
#     Step  2  enter bios setup  DUT
#     Step  3  send key  DUT  KEY_LEFT  ${2}
#     Step  4  enter menu bios boot order  DUT  boundary_line=<match all>  target_list=${bios_boot_order_test_5th_list}  ipv6=True  ##Network:UEFI: IPv4,Hard Disk:CentOS  (,USB,CD/DVD,Other
#     Step  5  send key  DUT  KEY_RIGHT  ${1}
#     Step  6  save bios setup  DUT

# set boot order and reboot to check 6th
#     Step  1  run ipmi get cmd  DUT  ${cmd_get_bios_boot_order}  expected_result=01 09 02 00 03 04

# BIOS load default
#     Step  1  go to openbmc
#     Step  2  power reset enter into bios  DUT
#     Step  3  send key  DUT  KEY_LEFT  ${1}
#     Step  4  send key  DUT  KEY_DOWN  ${3}
#     Step  5  restore bios defaults  DUT
#     Step  6  send key  DUT  KEY_LEFT  ${1}
#     Step  7  send key  DUT  KEY_UP  ${2}
#     Step  8  restore bios network drive bbs priorities defaults  DUT  boundary_line=<match all>
#     Step  9  send key  DUT  KEY_RIGHT  ${1}
#     Step  10  send key  DUT  KEY_UP  ${3}
#     Step  11  save bios setup  DUT
#     Step  12  go to openbmc

#run peutil command dc
#Set Suite Variable  ${peutil}  peutil
#FOR    ${pim}    IN   ${2}  ${3}  ${8}  ${9}
#${peutil_result} =  run util  DUT  peutil ${pim}
#Set Suite Variable  ${${peutil}${pim}}  ${peutil_result}
#END

run peutil command
    Set Suite Variable  ${peutil}  peutil
    FOR    ${pim}    IN RANGE    ${2}  ${PIM_NUM}+2
        ${peutil_result} =  run util  DUT  peutil ${pim}
        Set Suite Variable  ${${peutil}${${pim}-1}}  ${peutil_result}
    END

#run peutil command
#${pim_info} =  check mp2 dc pim  DUT
#Run KeyWord If   ${pim_info} == True   run peutil command dc
#...    ELSE   run peutil command normal

check pim data match with peutil command
    Step  1  change dir  ${pim_eeprom_path}
    FOR    ${pim}    IN RANGE    ${1}  ${PIM_NUM}+1
        ${pim_result} =  run eeprom tool  DUT  option=d  eeprom_type=PIM${pim}  fan=${pim}
        Step  1  compare util and eeprom  DUT  ${${peutil}${pim}}  ${pim_result}  flag=pim${pim}
    END

run command to read pim eeprom
  ${pim_info} =  check mp2 dc pim  DUT
  Step  1  change dir  ${pim_eeprom_path}
  FOR    ${pim}    IN RANGE    ${1}  ${PIM_NUM}+1
#Continue For Loop IF  ${pim} == 3 and ${pim_info} == True
#Continue For Loop IF  ${pim} == 4 and ${pim_info} == True
#Continue For Loop IF  ${pim} == 5 and ${pim_info} == True
#Continue For Loop IF  ${pim} == 6 and ${pim_info} == True
      Step  1  run eeprom tool  DUT  option=d  eeprom_type=PIM${pim}  fan=${pim}  expected_result=${pim_eeprom_product_name}
  END

run command to write and read pim eeprom
  ${pim_info} =  check mp2 dc pim  DUT
  FOR    ${pim}    IN RANGE    ${1}  ${PIM_NUM}+1
#Continue For Loop IF  ${pim} == 3 and ${pim_info} == True
#Continue For Loop IF  ${pim} == 4 and ${pim_info} == True
#Continue For Loop IF  ${pim} == 5 and ${pim_info} == True
#Continue For Loop IF  ${pim} == 6 and ${pim_info} == True
      Wait Until Keyword Succeeds  30s  10s  Step  1  write and read pim eeprom  ${pim}  ${pim_eeprom_test}
  END

run command to write and read pim eeprom with different data
  ${pim_info} =  check mp2 dc pim  DUT
  FOR    ${pim}    IN RANGE    ${1}  ${PIM_NUM}+1
#Continue For Loop IF  ${pim} == 3 and ${pim_info} == True
#Continue For Loop IF  ${pim} == 4 and ${pim_info} == True
#Continue For Loop IF  ${pim} == 5 and ${pim_info} == True
#Continue For Loop IF  ${pim} == 6 and ${pim_info} == True
      Step  1  write and read pim eeprom  ${pim}  ${pim_eeprom_test2}
  END

reset bmc and read pim eeprom
  ${pim_info} =  check mp2 dc pim  DUT
  Step  1  reboot device
  Step  2  change dir  ${pim_eeprom_path}
  FOR    ${pim}    IN RANGE    ${1}  ${PIM_NUM}+1
#Continue For Loop IF  ${pim} == 3 and ${pim_info} == True
#Continue For Loop IF  ${pim} == 4 and ${pim_info} == True
#Continue For Loop IF  ${pim} == 5 and ${pim_info} == True
#Continue For Loop IF  ${pim} == 6 and ${pim_info} == True
      Step  1  run eeprom tool  DUT  option=d  eeprom_type=PIM${pim}  fan=${pim}  expected_result=${pim_eeprom_test}
  END

reset bmc and read pim eeprom with different data
  ${pim_info} =  check mp2 dc pim  DUT
  Step  1  reboot device
  Step  2  change dir  ${pim_eeprom_path}
  FOR    ${pim}    IN RANGE    ${1}  ${PIM_NUM}+1
#Continue For Loop IF  ${pim} == 3 and ${pim_info} == True
#Continue For Loop IF  ${pim} == 4 and ${pim_info} == True
#Continue For Loop IF  ${pim} == 5 and ${pim_info} == True
#Continue For Loop IF  ${pim} == 6 and ${pim_info} == True
      Step  1  run eeprom tool  DUT  option=d  eeprom_type=PIM${pim}  fan=${pim}  expected_result=${pim_eeprom_test2}
  END

chassis power cycle and read pim eeprom
  ${pim_info} =  check mp2 dc pim  DUT
  Step  1  reset power chassis  DUT
  Step  2  change dir  ${pim_eeprom_path}
  FOR    ${pim}    IN RANGE    ${1}  ${PIM_NUM}+1
#Continue For Loop IF  ${pim} == 3 and ${pim_info} == True
#Continue For Loop IF  ${pim} == 4 and ${pim_info} == True
#Continue For Loop IF  ${pim} == 5 and ${pim_info} == True
#Continue For Loop IF  ${pim} == 6 and ${pim_info} == True
      Step  1  run eeprom tool  DUT  option=d  eeprom_type=PIM${pim}  fan=${pim}  expected_result=${pim_eeprom_test}
  END

write and read pim eeprom
  [Arguments]  ${pim_number}  ${eeprom_test_name}
  Step  1  modify eeprom cfg  DUT  ${eeprom_test_name}  eeprom.cfg
  Step  2  run eeprom tool  DUT  option=w  eeprom_type=PIM${pim_number}  fan=${pim_number}
  Step  3  run eeprom tool  DUT  option=d  eeprom_type=PIM${pim_number}  fan=${pim_number}  expected_result=${eeprom_test_name}

prepare store all pim eeprom
  ${pim_info} =  check mp2 dc pim  DUT
  Step  1  change dir  ${pim_eeprom_path}
  FOR    ${pim}    IN RANGE    ${1}  ${PIM_NUM}+1
#Continue For Loop IF  ${pim} == 3 and ${pim_info} == True
#Continue For Loop IF  ${pim} == 4 and ${pim_info} == True
#Continue For Loop IF  ${pim} == 5 and ${pim_info} == True
#Continue For Loop IF  ${pim} == 6 and ${pim_info} == True
      Step  1  run eeprom tool  DUT  option=d  eeprom_type=PIM${pim}  fan=${pim}
      Step  2  store eeprom  DUT  eeprom_out.cfg  eeprom_store${pim}.cfg  ${pim_eeprom_path}
  END

restore all pim eeprom
  ${pim_info} =  check mp2 dc pim  DUT
  Step  1  change dir  ${pim_eeprom_path}
  FOR    ${pim}    IN RANGE    ${1}  ${PIM_NUM}+1
#Continue For Loop IF  ${pim} == 3 and ${pim_info} == True
#Continue For Loop IF  ${pim} == 4 and ${pim_info} == True
#Continue For Loop IF  ${pim} == 5 and ${pim_info} == True
#Continue For Loop IF  ${pim} == 6 and ${pim_info} == True
      Step  1  restore fan eeprom  ${pim}  eeprom_store${pim}.cfg
      Step  2  clean up file  DUT  eeprom_store${pim}.cfg
  END
  Step  2  change dir

run command to read sim eeprom
  Step  1  read eeprom  ${sim_eeprom_path}  SIM  ${sim_eeprom_product_name}

run command to write and read sim eeprom
  Step  1  write and read eeprom  SIM  ${sim_eeprom_test}

run command to write and read sim eeprom with different data
  Step  1  write and read eeprom  SIM  ${sim_eeprom_test2}

reset bmc and read sim eeprom
  Step  1  reset bmc and read eeprom  SIM  ${sim_eeprom_path}  ${sim_eeprom_test}

reset bmc and read sim eeprom with different data
  Step  1  reset bmc and read eeprom  SIM  ${sim_eeprom_path}  ${sim_eeprom_test2}

chassis power cycle and read sim eeprom
  Step  1  chassis power cycle and read eeprom  SIM  ${sim_eeprom_path}  ${sim_eeprom_test}

check TH4 chip presence
    prepare minipack2 images  DUT  ${scp_ip}  ${scp_username}  ${scp_password}  ${img_th4_path}  ${local_th4_path}
    ${th4_presence} =  check th4 chip  DUT
    Set Suite Variable  ${th4_presence}  ${th4_presence}

prepare CPLD images
    go to openbmc
    prepare minipack2 images  DUT  ${scp_ip}  ${scp_username}  ${scp_password}  ${img_cpld_path}  ${workspace}
    switch bmc flash  DUT  Master

# pcie sw eeprom update test if TH4 present
#     Run keyword if  ${th4_presence} == True  pcie sw eeprom update test

# ping dhcp server with eth0 if TH4 present
#     Run keyword if  ${th4_presence} == True  ping dhcp server with eth0

# clean up files if TH4 present
#     Run keyword if  ${th4_presence} == True  clean up file  DUT  files=dump1 dump2 dump3

# pcie sw eeprom update test
#     Step  1  read spi eeprom  DUT  spi1  PCIE_SW  dump1
#     Step  2  write spi eeprom  DUT  spi1  PCIE_SW  erase_flag=True
#     Step  3  read spi eeprom  DUT  spi1  PCIE_SW  dump2
#     Step  4  run hexdump  DUT  dump2  erase_flag=True
#     Step  5  write spi eeprom  DUT  spi1  PCIE_SW
#     Step  6  read spi eeprom  DUT  spi1  PCIE_SW  dump3
#     Step  7  compare dump data and image bin  DUT  PCIE_SW  dump3

upgrade th4 fw if TH4 present
    Run keyword if  ${th4_presence} == True  update th4  DUT  isUpgrade=True

downgrade th4 fw if TH4 present
    Run keyword if  ${th4_presence} == True  update th4  DUT  isUpgrade=False

run command to read and write OOB Switch eeprom
    Step  1  read spi eeprom  DUT  ${oob_spi}  ${oob_eeprom_name}  dump1
    Step  2  run hexdump  DUT  dump1
    Step  3  write spi eeprom  DUT  ${oob_spi}  ${oob_eeprom_name}  erase_flag=True
    Step  4  read spi eeprom  DUT  ${oob_spi}  ${oob_eeprom_name}  dump2
    Step  5  run hexdump  DUT  dump2  erase_flag=True
    Step  6  write spi eeprom  DUT  ${oob_spi}  ${oob_eeprom_name}
    Step  7  read spi eeprom  DUT  ${oob_spi}  ${oob_eeprom_name}  dump3
    Step  8  run hexdump  DUT  dump3
    Step  9  compare dump data and image bin  DUT  OOB  dump3

clean OOB images and dump files
    Step  1  clean images  DUT  OOB
    Step  2  clean up file  DUT  files=dump1 dump2 dump3

set time delay 90 and ssh login bmc
    Step  1  set time delay  90
    Step  2  ssh login bmc  DUT

prepare images
   [Arguments]  ${image}
    Step  1  switch bmc flash  DUT  Master
    Step  2  create dir  ${workspace}/${image}  ${OPENBMC_MODE}
    Step  3  get dhcp ip address  DUT  eth0  ${OPENBMC_MODE}
    Step  4  download images  DUT  ${image}

prepare BIOS images
    Step  1  switch bmc flash  DUT  Master
    Step  2  switch bios flash  DUT  Master
    Step  3  create dir  ${workspace}/BIOS  ${OPENBMC_MODE}
    Step  4  get dhcp ip address  DUT  eth0  ${OPENBMC_MODE}
    Step  5  download images  DUT  BIOS

check come side mac address
    Step  1  come side mac address test  DUT
    Step  2  go to openbmc

verify bmc ipv6 address
  get dhcp ip address  DUT  eth0  mode=${OPENBMC_MODE}  ipv6=True

ping openbmc from dhcp server
  ${bmc_ipv6} =  get dhcp ip address  DUT  eth0  mode=${OPENBMC_MODE}  ipv6=True
  ping6 bmc from dhcp  PC  ${bmc_ipv6}

ssh dhcp server from openbmc
  ssh dhcp server from bmc  ${dhcp_ipv6}  ${dhcp_username}  ${dhcp_password}  ${dhcp_prompt}

ssh openbmc from dhcp server
  ${bmc_ipv6} =  get dhcp ip address  DUT  eth0  mode=${OPENBMC_MODE}  ipv6=True
  ssh bmc from dhcp server  PC  DUT  ${bmc_ipv6}

check bmc auto boot test
    bmc autoboot test  DUT

Print Loop Info
    [Arguments]    ${CUR_INDEX}
    print log info  *******************************************
    print log info  *** Test Loop \#: ${CUR_INDEX} / 2000 ***
    print log info  *******************************************

Using scp command to copy file from BMC to CPU by usb0 ipv6 new
  Step  1  copy file from BMC to CPU ipv6 new  ${usb0_int_cpu['ip_ipv6']}  filepath=${workspace}  filename=${usb0_test_file}
              ...   destination_path=/home/  interface=usb0

copy file from BMC to CPU ipv6 new
  [Arguments]  ${ip}  ${filepath}  ${filename}  ${destination_path}  ${interface}
  Step  1  go to openbmc
  Step  2  create dir  path=${filepath}  mode=${OPENBMC_MODE}
  Step  3  create test file  DUT  filename=${filepath}/${filename}  size_MB=${usb0_test_size_mb}
  Step  4  copy files from bmc to cpu new  DUT  cpu_ip=${ip}  filename=${filename}  filepath=${filepath}
              ...  destination_path=${destination_path}  size_MB=${usb0_test_size_mb}
              ...  swap=True  ipv6=True  interface=${interface}

run all the parameters of version utility lite
  Step  1  verify fw version  DUT  BMC

read restful fruid via ipv4 lite
  Step  1  verify restful  DUT  restful_url=mb/fruid  ip=${bmc_ipv4}  interface=eth0

read restful fruid via ipv6 lite
  Step  1  verify restful  DUT  restful_url=mb/fruid  ip=${bmc_ipv6}  interface=eth0  ipv6=True

compare restful fruid with fru data dumped in bmc os lite
  Step  1  verify restful  DUT  restful_url=mb/fruid  ip=${LOCALHOST}  interface=eth0  compare=True

read redfish chassis info
  Step  1  run redfish  DUT  redfish_url=redfish/v1/Chassis/1  ip=localhost  mode=${OPENBMC_MODE}

read redfish system info
  Step  1  run redfish  DUT  redfish_url=redfish/v1/Systems  ip=localhost  mode=${OPENBMC_MODE}

prepare store eeprom lite
  [Arguments]  ${eeprom_path}
  #Step  1  switch to centos
  #Step  1  copy files from cpu to bmc  DUT  cpu_ip=${default_bmc_usb0_ipv6_addr}  filename=fb_eeprom  filepath=/usr/local/bin
  #            ...  destination_path=${workspace_p}
  #            ...  swap=True  ipv6=True  interface=usb0
  Step  2  store eeprom lite  DUT  eeprom.cfg  ${workspace_p}/eeprom_store.cfg  ${eeprom_path}

read eeprom lite
  [Arguments]  ${eeprom_type}  ${eeprom_product_name}
  Step  1  run eeprom tool lite  DUT  eeprom_type=${eeprom_type}  expected_result=${eeprom_product_name}

write and read eeprom lite
  [Arguments]  ${eeprom_type}  ${eeprom_test_name}  ${eeprom_path}  ${bin_name}  ${eeprom_test_check}  ${disable_write_protection}  ${enable_write_protection}
  Step  1  create dir  path=/var/unidiag/firmware  mode=${OPENBMC_MODE}
  Step  2  change dir  /var/unidiag/firmware
  Step  3  modify eeprom cfg lite  DUT  ${eeprom_test_name}  eeprom.cfg  ${bin_name}
  Step  4  update modified eeprom  DUT   ${bin_name}  ${eeprom_path}  ${disable_write_protection}  ${enable_write_protection}
  Step  5  run eeprom tool lite  DUT  eeprom_type=${eeprom_type}  expected_result=${eeprom_test_check}

reset bmc and read eeprom lite
  [Arguments]  ${eeprom_type}  ${eeprom_test_name}
  Step  1  reboot device
  Step  2  run eeprom tool lite  DUT  eeprom_type=${eeprom_type}  expected_result=${eeprom_test_name}

chassis power cycle and read eeprom lite
  [Arguments]  ${eeprom_type}  ${eeprom_test_name}
  Step  1  reset power chassis  DUT
  Step  2  run eeprom tool lite  DUT  eeprom_type=${eeprom_type}  expected_result=${eeprom_test_name}

restore eeprom lite and clean up files
  [Arguments]  ${eeprom_type}  ${bin_name}  ${eeprom_path}  ${eeprom_test_name}  ${disable_write_protection}  ${enable_write_protection}
  Step  1  create dir  path=/var/unidiag/firmware  mode=${OPENBMC_MODE}
  Step  2  restore eeprom lite  DUT  eeprom_store.cfg  ${bin_name}
  Step  3  update modified eeprom  DUT  ${bin_name}  ${eeprom_path}  ${disable_write_protection}  ${enable_write_protection}
  Step  4  read eeprom lite  ${eeprom_type}  ${eeprom_test_name}
  Step  5  clean up file  DUT  /var/unidiag  isDir=true
  Step  6  change dir  ${workspace_p}
  Step  7  clean up file  DUT  eeprom_store.cfg
  #Step  8  clean up file  DUT  fb_eeprom
  Step  9  clean up file  DUT  eeprom.cfg
  Step  10  clean up file  DUT  eeprom_out.cfg

run command to read scm eeprom minipack3
  Step  1  read eeprom lite  scm_eeprom  ${scm_eeprom_product_name}

run command to write and read scm eeprom minipack3
  Step  1  write and read eeprom lite  scm_eeprom  ${scm_eeprom_test}  ${scm_eeprom_path}  ${scm_bin_name}  ${scm_eeprom_test_check}  ${disable_write_protection_scm}  ${enable_write_protection_scm}

reset bmc and read scm eeprom minipack3
  Step  1  reset bmc and read eeprom lite  scm_eeprom  ${scm_eeprom_test_check}

chassis power cycle and read scm eeprom minipack3
  Step  1  chassis power cycle and read eeprom lite  scm_eeprom  ${scm_eeprom_test_check}

run command to write and read scm eeprom with different data minipack3
    Step  1  write and read eeprom lite  scm_eeprom  ${scm_eeprom_test2}  ${scm_eeprom_path}  ${scm_bin_name}  ${scm_eeprom_test2_check}  ${disable_write_protection_scm}  ${enable_write_protection_scm}

reset bmc and read scm eeprom with different data minipack3
  Step  1  reset bmc and read eeprom lite  scm_eeprom  ${scm_eeprom_test2_check}

run command to read fcb eeprom minipack3
  Step  1  read eeprom lite  chassis_eeprom  ${fcb_eeprom_product_name}

run command to write and read fcb eeprom minipack3
  Step  1  write and read eeprom lite  chassis_eeprom  ${fcb_eeprom_test}  ${fcb_eeprom_path}  ${fcb_bin_name}  ${fcb_eeprom_test_check}  ${disable_write_protection_fcb}  ${enable_write_protection_fcb}

reset bmc and read fcb eeprom minipack3
  Step  1  reset bmc and read eeprom lite  chassis_eeprom  ${fcb_eeprom_test_check}

chassis power cycle and read fcb eeprom minipack3
  Step  1  chassis power cycle and read eeprom lite  chassis_eeprom  ${fcb_eeprom_test_check}

run command to write and read fcb eeprom with different data minipack3
    Step  1  write and read eeprom lite  chassis_eeprom  ${fcb_eeprom_test2}  ${fcb_eeprom_path}  ${fcb_bin_name}  ${fcb_eeprom_test2_check}  ${disable_write_protection_fcb}  ${enable_write_protection_fcb}

reset bmc and read fcb eeprom with different data minipack3
  Step  1  reset bmc and read eeprom lite  chassis_eeprom  ${fcb_eeprom_test2_check}

reboot and check dhcp setting info and check ipv6 address lite
  Step  1  reboot device
  Step  2  verify dhcp address  DUT  interface=eth0  ipv6=True
  Step  3  verify ipv6 address  DUT  interface=usb0  expected_result=${usb0_int_bmc['ip_ipv6']}

get board name via command "wedge_board_type"
    get board name  DUT  expected_result=${board_type}

prepare MEM_TEST images
    Step  1  create dir  ${workspace_p}/MEM_TEST  ${OPENBMC_MODE}
    Step  2  get dhcp ip address  DUT  eth0  ${OPENBMC_MODE}
    Step  3  download images  DUT  MEM_TEST

get memory information lite
  Step  1  go to openbmc
  Step  2  test execute command  DUT  test_cmd=${cmd_get_mem_info}  mode=${OPENBMC_MODE}
  Step  3  change dir  ${workspace_p}/MEM_TEST

clean memtest script and change dir
    Step  1  clean up file  DUT  ${workspace_p}/MEM_TEST  isDir=True
    Step  2  change dir

run command to read/write mcb cpld reg to power off com-e
  Step  1  go to openbmc
  Step  2  read MCB CPLD REG  expected_result=${power_on_val}
  Step  3  write MCB CPLD REG  val=${power_off_val}
  Step  4  read MCB CPLD REG  expected_result=${power_off_val}
  Step  5  verify power control  DUT  power_mode=status  power_status=off
  Step  6  verify no cpu prompt return  DUT

run command to read/write mcb cpld reg to power on com-e
  Step  1  go to openbmc
  Step  2  write MCB CPLD REG  val=${power_on_val}
  Step  3  read MCB CPLD REG  expected_result=${power_on_val}
  Step  4  verify power control  DUT  power_mode=status  power_status=on
  Step  5  verify bios boot  DUT  switch_console_flag=True
  Step  6  go to openbmc

read MCB CPLD REG
  [Arguments]  ${expected_result}
  run_i2ctool  DUT  get  bus=${mcb_cpld_bus}  addr=${mcb_cpld_addr}  reg=${come_pwr_ctrl_reg}  expected_result=${expected_result}

write MCB CPLD REG
  [Arguments]  ${val}
  run_i2ctool  DUT  set  bus=${mcb_cpld_bus}  addr=${mcb_cpld_addr}  reg=${come_pwr_ctrl_reg}  val=${val}

prepare openbmc lite mac global variable
    [Arguments]  ${eeprom_path}
    Step  1  prepare store eeprom lite  ${eeprom_path}
    ${local_mac_address_with_separator}=  get_eeprom_value2  DUT  cmd=${cmd_read_mac_from_eeprom}  key=Local MAC
    Set Environment Variable  local_mac_address_with_separator_1  ${local_mac_address_with_separator}

Check OpenBMC MAC address
    Step  1  verify_mac_address  DUT  interface=eth0  expected_result=%{local_mac_address_with_separator_1}

Use unidiag tool to Update OpenBMC MAC address mp3
    ${random_mac_without_separator}=  create_random_mac_address  DUT  prompt=format_without_separator
    ${random_mac_with_separator}=  change_mac_fomat  DUT  original=${random_mac_without_separator}
    ${local_mac_address_read_by_weutil}=  get_eeprom_value2  DUT  cmd=weutil  key=Local MAC
    Set Environment Variable  random_mac_with_separator_1  ${random_mac_with_separator}
    Step  1  modify_eeprom_cfg_string  DUT  original=${local_mac_address_read_by_weutil}  modified=%{random_mac_with_separator_1}
    Step  2  update modified mac  ${fcb_eeprom_path}  ${fcb_bin_name}  ${disable_write_protection_fcb}  ${enable_write_protection_fcb}
    ${local_mac_address_after_modify}=  get_eeprom_value2  DUT  cmd=${cmd_read_mac_from_eeprom}  key=Local MAC
    Step  3  Should Be Equal  ${local_mac_address_after_modify}  %{random_mac_with_separator_1}  expect != real
    ${ifconfig_get_mac_address}=  openbmc_lib.get_mac_address  DUT  prompt=openbmc  interface=eth0
    Step  4  Should Not Be Equal  ${ifconfig_get_mac_address}  %{random_mac_with_separator_1}

update modified mac
  [Arguments]  ${eeprom_path}  ${bin_name}  ${disable_write_protection}  ${enable_write_protection}
  Step  1  create dir  path=/var/unidiag/firmware  mode=${OPENBMC_MODE}
  Step  2  create bin file  DUT  eeprom.cfg  ${bin_name}
  Step  3  update modified eeprom  DUT  ${bin_name}  ${eeprom_path}  ${disable_write_protection}  ${enable_write_protection}

Reset openbmc lite os to check mac address
    Step  1  reboot device
    ${local_mac_address_after_modify_reset}=  get_eeprom_value2  DUT  cmd=${cmd_read_mac_from_eeprom}  key=Local MAC
    ${ifconfig_get_mac_address_reset}=  openbmc_lib.get_mac_address  DUT  prompt=openbmc  interface=eth0
    Step  2  Should Be Equal  ${ifconfig_get_mac_address_reset}  %{random_mac_with_separator_1}
    Step  3  verify_mac_address  DUT  interface=usb0  expected_result=${default_bmc_usb0_mac_addr}

Power cycle chassis lite to check mac address
    Step  1  reset_power_chassis  DUT
    ${local_mac_address_after_modify_powercycle}=  get_eeprom_value2  DUT  cmd=${cmd_read_mac_from_eeprom}  key=Local MAC
    ${ifconfig_get_mac_address_powercycle}=  openbmc_lib.get_mac_address  DUT  prompt=openbmc  interface=eth0
    Step  2  Should Be Equal  ${ifconfig_get_mac_address_powercycle}  %{random_mac_with_separator_1}
    Step  3  verify_mac_address  DUT  interface=usb0  expected_result=${default_bmc_usb0_mac_addr}

Use unidiag tool to Update OpenBMC MAC address back to previous value mp3
    Step  1  change dir  ${workspace_p}
    ${local_mac_address_read_by_weutil}=  get_eeprom_value2  DUT  cmd=weutil  key=Local MAC
    Set Environment Variable  local_mac_with_separator_1  ${local_mac_address_read_by_weutil}
    ${local_mac_address_read_by_eeprom.cfg}=  get_eeprom_value  DUT  cmd=cat eeprom_store.cfg  key=local_mac_address
    Set Environment Variable  original_mac_with_separator_1  ${local_mac_address_read_by_eeprom.cfg}
    Step  3  modify_eeprom_cfg_string  DUT  original=%{local_mac_with_separator_1}  modified=%{original_mac_with_separator_1}
    Step  4  update modified mac  ${fcb_eeprom_path}  ${fcb_bin_name}  ${disable_write_protection_fcb}  ${enable_write_protection_fcb} 
    ${local_mac_address_after_modify}=  get_eeprom_value2  DUT  cmd=${cmd_read_mac_from_eeprom}  key=Local MAC
    Step  5  Should Be Equal  ${local_mac_address_after_modify}  %{original_mac_with_separator_1}  expect != real
    ${ifconfig_get_mac_address}=  openbmc_lib.get_mac_address  DUT  prompt=openbmc  interface=eth0
    Step  6  Should Not Be Equal  ${ifconfig_get_mac_address}  %{original_mac_with_separator_1}

Reset openbmc lite os to check mac address again
    Step  1  reboot device
    ${local_mac_address_after_modify_reset}=  get_eeprom_value2  DUT  cmd=${cmd_read_mac_from_eeprom}  key=Local MAC
    ${ifconfig_get_mac_address_reset}=  openbmc_lib.get_mac_address  DUT  prompt=openbmc  interface=eth0
    Step  2  Should Be Equal  ${ifconfig_get_mac_address_reset}  %{original_mac_with_separator_1}
    Step  3  verify_mac_address  DUT  interface=usb0  expected_result=${default_bmc_usb0_mac_addr}

upgrade master bios lite and check version
    Step  1  update bios lite  DUT  bios_flash=Master  isUpgrade=True

downgrade master bios lite and check version
     Step  1  update bios lite  DUT  bios_flash=Master  isUpgrade=False

prepare FPGA images
    Step  1  create dir  ${workspace}/FPGA  ${OPENBMC_MODE}
    Step  2  get dhcp ip address  DUT  eth0  ${OPENBMC_MODE}
    Step  3  download images  DUT  FPGA

FPGA upgrade lite and check FPGA version
    Step  1  update fpga lite  DUT  isUpgrade=True

FPGA downgrade lite and check FPGA version
    Step  1  update fpga lite  DUT  isUpgrade=False

prepare COME_CPLD images
    Step  1  create dir  ${workspace_p}/COME_CPLD  ${OPENBMC_MODE}
    Step  2  get dhcp ip address  DUT  eth0  ${OPENBMC_MODE}
    Step  3  download images  DUT  COME_CPLD
    Step  4  download images  DUT  CPLD_UPDATE.SH

COMe CPLD upgrade and check CPLD version
    Step  1  update come cpld  DUT  isUpgrade=True

COMe CPLD downgrade and check CPLD version
    Step  1  update come cpld  DUT  isUpgrade=False

using scp command to copy file from BMC to CPU by eth0 ipv6 lite
  Step  1  go to centos
  ${cpu_ipv6} =  get dhcp ip address  DUT  interfaceName=eth0  mode=${CENTOS_MODE}  ipv6=True
  Step  2  copy file from BMC to CPU ipv6 new  ${cpu_ipv6}  filepath=${workspace}  filename=${usb0_test_file}
              ...   destination_path=/home/  interface=eth0

Use unidiag tool to Update OpenBMC MAC address minerva
    ${random_mac_without_separator}=  create_random_mac_address  DUT  prompt=format_without_separator
    ${random_mac_with_separator}=  change_mac_fomat  DUT  original=${random_mac_without_separator}
    ${local_mac_address_read_by_weutil}=  get_eeprom_value2  DUT  cmd=weutil  key=Local MAC
    Set Environment Variable  random_mac_with_separator_1  ${random_mac_with_separator}
    Step  1  modify_eeprom_cfg_string  DUT  original=${local_mac_address_read_by_weutil}  modified=%{random_mac_with_separator_1}
    Step  2  update modified mac  ${smb_eeprom_path}  ${smb_bin_name}  ${disable_write_protection}  ${enable_write_protection}
    ${local_mac_address_after_modify}=  get_eeprom_value2  DUT  cmd=${cmd_read_mac_from_eeprom}  key=Local MAC
    Step  3  Should Be Equal  ${local_mac_address_after_modify}  %{random_mac_with_separator_1}  expect != real
    ${ifconfig_get_mac_address}=  openbmc_lib.get_mac_address  DUT  prompt=openbmc  interface=eth0
    Step  4  Should Not Be Equal  ${ifconfig_get_mac_address}  %{random_mac_with_separator_1}

Use unidiag tool to Update OpenBMC MAC address back to previous value minerva
    Step  1  change dir  ${workspace_p}
    ${local_mac_address_read_by_weutil}=  get_eeprom_value2  DUT  cmd=weutil  key=Local MAC
    Set Environment Variable  local_mac_with_separator_1  ${local_mac_address_read_by_weutil}
    ${local_mac_address_read_by_eeprom.cfg}=  get_eeprom_value  DUT  cmd=cat eeprom_store.cfg  key=local_mac_address
    Set Environment Variable  original_mac_with_separator_1  ${local_mac_address_read_by_eeprom.cfg}
    Step  3  modify_eeprom_cfg_string  DUT  original=%{local_mac_with_separator_1}  modified=%{original_mac_with_separator_1}
    Step  4  update modified mac  ${smb_eeprom_path}  ${smb_bin_name}  ${disable_write_protection}  ${enable_write_protection}
    ${local_mac_address_after_modify}=  get_eeprom_value2  DUT  cmd=${cmd_read_mac_from_eeprom}  key=Local MAC
    Step  5  Should Be Equal  ${local_mac_address_after_modify}  %{original_mac_with_separator_1}  expect != real
    ${ifconfig_get_mac_address}=  openbmc_lib.get_mac_address  DUT  prompt=openbmc  interface=eth0
    Step  6  Should Not Be Equal  ${ifconfig_get_mac_address}  %{original_mac_with_separator_1}

run command to read/write smb cpld reg to power off com-e
  Step  1  go to openbmc
  Step  2  read SMB CPLD REG  expected_result=${power_on_val}
  Step  3  write SMB CPLD REG  val=${power_off_val}
  Step  4  read SMB CPLD REG  expected_result=${power_off_val}
  Step  5  verify power control  DUT  power_mode=status  power_status=off
  Step  6  verify no cpu prompt return  DUT

run command to read/write smb cpld reg to power on com-e
  Step  1  go to openbmc
  Step  2  write SMB CPLD REG  val=${power_on_val}
  Step  3  read SMB CPLD REG  expected_result=${power_on_val}
  Step  4  verify power control  DUT  power_mode=status  power_status=on
  Step  5  verify bios boot  DUT  switch_console_flag=True
  Step  6  go to openbmc

read SMB CPLD REG
  [Arguments]  ${expected_result}
  run_i2ctool  DUT  get  bus=${smb_cpld_bus}  addr=${smb_cpld_addr}  reg=${come_pwr_ctrl_reg}  expected_result=${expected_result}

write SMB CPLD REG
  [Arguments]  ${val}
  run_i2ctool  DUT  set  bus=${smb_cpld_bus}  addr=${smb_cpld_addr}  reg=${come_pwr_ctrl_reg}  val=${val}

check smb fru data match with eeprom tool minerva
    ${eeprom_result} =  run eeprom  ${smb_eeprom_path}  DUT
    Step  1  compare util and eeprom lite  DUT  ${weutil_result}  ${eeprom_result}

check fcb fru data match with eeprom tool minipack3
    ${eeprom_result} =  run eeprom  ${fcb_eeprom_path}  DUT
    Step  1  compare util and eeprom lite  DUT  ${weutil_result}  ${eeprom_result}

run command to read smb eeprom minerva
  Step  1  read eeprom lite  chassis_eeprom  ${smb_eeprom_product_name}

run command to write and read smb eeprom minerva
  Step  1  write and read eeprom lite  chassis_eeprom  ${smb_eeprom_test}  ${smb_eeprom_path}  ${smb_bin_name}  ${smb_eeprom_test_check}  ${disable_write_protection}  ${enable_write_protection}

reset bmc and read smb eeprom minerva
  Step  1  reset bmc and read eeprom lite  chassis_eeprom  ${smb_eeprom_test_check}

chassis power cycle and read smb eeprom minerva
  Step  1  chassis power cycle and read eeprom lite  chassis_eeprom  ${smb_eeprom_test_check}

run command to write and read smb eeprom with different data minerva
    Step  1  write and read eeprom lite  chassis_eeprom  ${smb_eeprom_test2}  ${smb_eeprom_path}  ${smb_bin_name}  ${smb_eeprom_test2_check}  ${disable_write_protection}  ${enable_write_protection}

reset bmc and read smb eeprom with different data minerva
  Step  1  reset bmc and read eeprom lite  chassis_eeprom  ${smb_eeprom_test2_check}

clean come images and script
    Step  1  clean images  DUT  COME_CPLD
    Step  2  clean up file  DUT  files=${CPLD_UPDATE_CMD}  mode=${OPENBMC_MODE}

prepare iob_update.sh script
    Step  1  download images  DUT  IOB_UPDATE.SH

clean iob_update.sh script
    Step  1  clean up file  DUT  files=${IOB_UPDATE_CMD}  mode=${OPENBMC_MODE}

