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
# Script       : openbmc_keywords.robot                                                                               #
# Date         : July 29, 2023                                                                                        #
# Author       : Hui Gong <huigon@celestica.com>                                                                      #
# Description  : This script used as keywords in openbmc.robot                                                        #
#                                                                                                                     #
# Script Revision Details:                                                                                            #
#   Initial Draft for openbmc testing                                                                                 #
#######################################################################################################################

*** Settings ***
Variables         openbmc_variable.py
Library           ./openbmc_lib.py
#Library           bios_menu_lib.py
Library           CommonLib.py
Library           OperatingSystem
Library           openbmc_lib.py
Library           WhiteboxLibAdapter.py
Library           Collections
Library           Process
Resource          CommonResource.robot

*** Variables ***
#${LoopCnt}        1

*** Keywords ***
Keyword Retry
    [Arguments]    ${keyword}    @{args}    &{config}
    ${result}=    Wait Until Keyword Succeeds    ${G Retry Count}    10s    ${keyword}    @{args}    &{config}
    [Return]    ${result}

get all the variables
    ${server_ipv4_ip} =  get_deviceinfo_from_config  PC  managementIP
    ${server_username} =  get_deviceinfo_from_config  PC  rootUserName
    ${server_password} =  get_deviceinfo_from_config  PC  rootPassword
    ${bmc_ipv4_ip_a} =  get_deviceinfo_from_config  ${DeviceName}  bmcIP
    ${bmc_username_a} =  get_deviceinfo_from_config  ${DeviceName}  bmcUserName
    ${bmc_password_a} =  get_deviceinfo_from_config  ${DeviceName}  bmcPassword
    ${DUT_ipv4_ip_a} =  get_ip_address_from_config  ${DeviceName}
    ${DUT_username_a} =  get_username_from_config  ${DeviceName}
    ${DUT_password_a} =  get_password_from_config  ${DeviceName}
    ${bmc_ipv4_ip_b} =  Run Keyword If  ${Peer_Canister}  get_deviceinfo_from_config  ${PeerDeviceName}  bmcIP
    ${bmc_username_b} =  Run Keyword If  ${Peer_Canister}  get_deviceinfo_from_config  ${PeerDeviceName}  bmcUserName
    ${bmc_password_b} =  Run Keyword If  ${Peer_Canister}  get_deviceinfo_from_config  ${PeerDeviceName}  bmcPassword
    ${DUT_ipv4_ip_b} =  Run Keyword If  ${Peer_Canister}  get_ip_address_from_config  ${PeerDeviceName}
    ${DUT_username_b} =  Run Keyword If  ${Peer_Canister}  get_username_from_config  ${PeerDeviceName}
    ${DUT_password_b} =  Run Keyword If  ${Peer_Canister}  get_password_from_config  ${PeerDeviceName}
#    Set Environment Variable  server_ipv4_ip_1  ${server_ipv4_ip}
    Set Environment Variable  server_ipv4_ip_1  ${server_ipv4_ip}
    Set Environment Variable  server_username_1  ${server_username}
    Set Environment Variable  server_password_1  ${server_password}
    Set Environment Variable  bmc_ipv4_ip_1  ${bmc_ipv4_ip_a}
    Set Environment Variable  bmc_username_1  ${bmc_username_a}
    Set Environment Variable  bmc_password_1  ${bmc_password_a}
    Set Environment Variable  DUT_ipv4_ip_1  ${DUT_ipv4_ip_a}
    Set Environment Variable  DUT_username_1  ${DUT_username_a}
    Set Environment Variable  DUT_password_1  ${DUT_password_a}
    Set Environment Variable  bmc_ipv4_ip_2  ${bmc_ipv4_ip_b}
    Set Environment Variable  bmc_username_2  ${bmc_username_b}
    Set Environment Variable  bmc_password_2  ${bmc_password_b}
    Set Environment Variable  DUT_ipv4_ip_2  ${DUT_ipv4_ip_b}
    Set Environment Variable  DUT_username_2  ${DUT_username_b}
    Set Environment Variable  DUT_password_2  ${DUT_password_b}
    Set Global Variable  @{device_info_a}  ${DeviceName}  ${bmc_ipv4_ip_a}  ${bmc_username_a}  ${bmc_password_a}
                                      ...  ${DUT_ipv4_ip_a}  ${DUT_username_a}  ${DUT_password_a}
    Run Keyword If  ${Peer_Canister}  Set Global Variable  @{device_info_b}  ${PeerDeviceName}  ${bmc_ipv4_ip_b}
                ...  ${bmc_username_b}  ${bmc_password_b}  ${DUT_ipv4_ip_b}  ${DUT_username_b}  ${DUT_password_b}


check BMC Version after mc reset
    ${openbmc_info} =  call_openbmc_class  ${device_info_a}
    Step  1  Call Method  ${openbmc_info}  check_openbmc_info  bmc_version  exp_info=${BMC_version}
    Step  2  Call Method  ${openbmc_info}  check_openbmc_info  product_id  exp_info=${BMC_Product_ID}
    Connect Device  ${DeviceName}  bmc
    Step  3  Call Method  ${openbmc_info}  ipmi_dev_global_cmd  cold_reset  rm=True
    Step  4  wait_pattern  ${DeviceName}  ${BOOT_REGEX}
    Disconnect Device  ${DeviceName}  bmc
    Step  5  Call Method  ${openbmc_info}  check_openbmc_info  bmc_version  exp_info=${BMC_version}
    Step  6  Call Method  ${openbmc_info}  check_openbmc_info  product_id  exp_info=${BMC_Product_ID}

check BMC Version after ac cycle
    ${openbmc_info} =  call_openbmc_class  ${device_info_a}
    Step  1  Call Method  ${openbmc_info}  check_openbmc_info  bmc_version  exp_info=${BMC_version}
    Step  2  Call Method  ${openbmc_info}  check_openbmc_info  product_id  exp_info=${BMC_Product_ID}
    Step  3  AC Power Cycle the Device
    Step  4  Call Method  ${openbmc_info}  check_openbmc_info  bmc_version  exp_info=${BMC_version}
    Step  5  Call Method  ${openbmc_info}  check_openbmc_info  product_id  exp_info=${BMC_Product_ID}

check KCS Communicate
    Step  1  ssh_command  %{DUT_username_1}  %{DUT_ipv4_ip_1}  %{DUT_password_1}  modprobe ipmi_si
    Step  2  ssh_command  %{DUT_username_1}  %{DUT_ipv4_ip_1}  %{DUT_password_1}  modprobe ipmi_devintf
    Step  3  check_bmc_kcs_communicate  ${DeviceName}

check KCS Interface
    ${openbmc_info} =  call_openbmc_class  ${DeviceName}
    Step  1  Call Method  ${openbmc_info}  get_mc_info

Power Restore Policy Power Off
    ${openbmc_info} =  call_openbmc_class  ${DeviceName}
    Step  1  Call Method  ${openbmc_info}  check_openbmc_info  policy_status  ${power_restore_policy_on}
    Step  2  Call Method  ${openbmc_info}  check_openbmc_info  power_status  on
    Step  3  Call Method  ${openbmc_info}  ipmi_power_control  ${power_restore_policy_off}
    Step  4  Call Method  ${openbmc_info}  check_openbmc_info  policy_status  ${power_restore_policy_off}
    Step  5  AC Power Cycle the Device
    Step  6  set time delay  60
    Step  7  Call Method  ${openbmc_info}  check_openbmc_info  power_status  off
    Step  8  Call Method  ${openbmc_info}  ipmi_power_control  power on
    Step  9  wait boot prompt  ${DeviceName}  os
    Step  10  Call Method  ${openbmc_info}  check_openbmc_info  policy_status  ${power_restore_policy_off}

Power Restore Policy Power Previous
    ${openbmc_info} =  call_openbmc_class  ${DeviceName}
    Step  1  Call Method  ${openbmc_info}  check_openbmc_info  power_status  on
    Step  2  Call Method  ${openbmc_info}  ipmi_power_control  ${power_restore_policy_per}
    Step  3  Call Method  ${openbmc_info}  check_openbmc_info  policy_status  ${power_restore_policy_per}
    Step  4  Call Method  ${openbmc_info}  ipmi_power_control  power off
    Step  5  set time delay  30
    Step  6  Call Method  ${openbmc_info}  check_openbmc_info  power_status  off
    Step  7  AC Power Cycle the Device
    Step  8  set time delay  60
    Step  9  Call Method  ${openbmc_info}  check_openbmc_info  power_status  off
    Step  10  Call Method  ${openbmc_info}  ipmi_power_control  power on
    Step  11  wait boot prompt  ${DeviceName}  os
    Step  12  Call Method  ${openbmc_info}  check_openbmc_info  policy_status  ${power_restore_policy_per}
    Step  13  AC Power Cycle the Device
    Step  14  Call Method  ${openbmc_info}  check_openbmc_info  power_status  on
    Step  15  wait boot prompt  ${DeviceName}  os

Power Restore Policy Power On
    ${openbmc_info} =  call_openbmc_class  ${DeviceName}
    Step  1  Call Method  ${openbmc_info}  check_openbmc_info  power_status  on
    Step  2  Call Method  ${openbmc_info}  ipmi_power_control  ${power_restore_policy_on}
    Step  3  Call Method  ${openbmc_info}  check_openbmc_info  policy_status  ${power_restore_policy_on}
    Step  4  AC Power Cycle the Device
    Step  5  wait boot prompt  ${DeviceName}  os
    Step  6  Call Method  ${openbmc_info}  check_openbmc_info  power_status  on
    Step  7  Call Method  ${openbmc_info}  check_openbmc_info  policy_status  ${power_restore_policy_on}

Power Status Power Off and Power On
    ${openbmc_info} =  call_openbmc_class  ${DeviceName}
    Step  1  Call Method  ${openbmc_info}  get_mc_info
    Step  2  Call Method  ${openbmc_info}  check_openbmc_info  power_status  on
    Step  3  Call Method  ${openbmc_info}  ipmi_power_control  power off
    set time delay  5
    Step  4  Call Method  ${openbmc_info}  check_openbmc_info  power_status  off
    set time delay  5
    Step  5  Call Method  ${openbmc_info}  ipmi_power_control  power on
    set time delay  2
    Step  6  Call Method  ${openbmc_info}  check_openbmc_info  power_status  on
    Step  7  wait boot prompt  ${DeviceName}  os

Power Status Power Cycle
    ${openbmc_info} =  call_openbmc_class  ${DeviceName}
    Step  1  Call Method  ${openbmc_info}  check_openbmc_info  power_status  on
    Step  2  Call Method  ${openbmc_info}  ipmi_power_control  power cycle
    set time delay  5
    Step  3  Call Method  ${openbmc_info}  check_openbmc_info  power_status  off
    set time delay  25
    Step  4  Call Method  ${openbmc_info}  check_openbmc_info  power_status  on
    Step  5  wait boot prompt  ${DeviceName}  os

Power Control Power Off and Power On
    ${openbmc_info} =  call_openbmc_class  ${DeviceName}
    ${SEL} =  call_sel_class  ${DeviceName}
    Step  1  Call Method  ${SEL}  sel_clear
    Step  2  Call Method  ${openbmc_info}  ipmi_power_control  power off
    set time delay  10
    Step  3  Call Method  ${openbmc_info}  check_openbmc_info  power_status  off
    Step  4  Call Method  ${SEL}  check_sel_list_unexpect_event  ${error_messages_list}
    Step  5  Call Method  ${SEL}  sel_clear
    Step  6  Call Method  ${openbmc_info}  ipmi_power_control  power on
    set time delay  10
    Step  7  Call Method  ${openbmc_info}  check_openbmc_info  power_status  on
    Step  8  wait boot prompt  ${DeviceName}  os
    Step  9  Call Method  ${SEL}  check_sel_list_unexpect_event  ${error_messages_list}

Power Control Power Cycle
# openbmc power cycle step: force power off 7s --> sleep 20s --> power on
    ${openbmc_info} =  call_openbmc_class  ${DeviceName}
    ${SEL} =  call_sel_class  ${DeviceName}
    Step  1  Call Method  ${SEL}  sel_clear
    Step  2  Call Method  ${openbmc_info}  ipmi_power_control  power cycle
    set time delay  5
    Step  3  Call Method  ${openbmc_info}  check_openbmc_info  power_status  off
    set time delay  25
    Step  4  Call Method  ${openbmc_info}  check_openbmc_info  power_status  on
    Step  5  wait boot prompt  ${DeviceName}  os
    Step  6  Call Method  ${SEL}  check_sel_list_unexpect_event  ${error_messages_list}

Power Control Power Reset
    ${openbmc_info} =  call_openbmc_class  ${DeviceName}
    ${SEL} =  call_sel_class  ${DeviceName}
    Step  1  Call Method  ${SEL}  sel_clear
    Step  2  Call Method  ${openbmc_info}  ipmi_power_control  hard reset
    set time delay  5
    Step  3  Call Method  ${openbmc_info}  check_openbmc_info  power_status  on
    set time delay  10
    Step  4  Call Method  ${openbmc_info}  check_openbmc_info  power_status  on
    Step  5  wait boot prompt  ${DeviceName}  os
    Step  6  Call Method  ${SEL}  check_sel_list_unexpect_event  ${error_messages_list}

verify the sensor power off status
    ${openbmc_info} =  call_openbmc_class  ${device_info_a}
    Step  1  Call Method  ${openbmc_info}  ipmi_power_control  power off
    set time delay  5
    Step  2  Call Method  ${openbmc_info}  check_openbmc_info  power_status  off
    Step  3  set time delay  5
    ${sensor} =  call_sensor_class  ${device_info_a}
    Step  4  Call Method  ${sensor}  verify_normal_status
    Step  5  Call Method  ${openbmc_info}  ipmi_power_control  power on
    Step  6  set time delay  2
    Step  7  Call Method  ${openbmc_info}  check_openbmc_info  power_status  on
    Step  8  wait boot prompt  ${DeviceName}  os

verify the sensor power on status
    ${openbmc_info} =  call_openbmc_class  ${device_info_a}
    Step  1  Call Method  ${openbmc_info}  check_openbmc_info  power_status  on
    ${sensor} =  call_sensor_class  ${device_info_a}
    Step  2  Call Method  ${sensor}  verify_normal_status

verify the sensor power reset status
    ${openbmc_info} =  call_openbmc_class  ${device_info_a}
    Connect Device  ${DeviceName}  bmc
    Step  1  Call Method  ${openbmc_info}  ipmi_dev_global_cmd  cold_reset
    Step  2  wait_pattern  ${DeviceName}  ${BOOT_REGEX}
    Disconnect Device  ${DeviceName}  bmc
    ${sensor} =  call_sensor_class  ${DeviceName}
    Step  3  Call Method  ${sensor}  verify_normal_status

Check Sensor Thresholds
    #${sensor} =  call_sensor_class  ${DeviceName}
    #Call Method  ${sensor}  thresholds_cmd  ${sensor}.sensor_list
    check_sensor_threshold_set  ${device_info_a}

Check the Sel DC Cycle
    Power Control Power Cycle

Check the Sel AC Cycle
    ${openbmc_info} =  call_openbmc_class  ${DeviceName}
    ${SEL} =  call_sel_class  ${DeviceName}
    Step  1  Call Method  ${SEL}  sel_clear
    Step  2  AC Power Cycle the Device
    Step  3  wait boot prompt  ${DeviceName}  os
    Step  4  Call Method  ${SEL}  check_sel_list_unexpect_event  ${error_messages_list}

User Name and Password Check
    Step  1  verify_bmc_user  ${DeviceName}  %{bmc_username_1}  %{bmc_ipv4_ip_1}  %{bmc_password_1}  1
    Step  2  verify_add_openbmc_user  ${DeviceName}  test2  qwsd22  2  new_username=tester2
    Step  3  verify_add_openbmc_user  ${DeviceName}  test3  qwsd23  3  new_username=tester3
    Step  4  verify_add_openbmc_user  ${DeviceName}  test4  qwsd24  4  new_username=tester4
    Step  5  verify_add_openbmc_user  ${DeviceName}  test5  qwsd25  5  new_username=tester5
    Step  6  verify_add_openbmc_user  ${DeviceName}  test6  qwsd26  6  new_username=tester6
    Step  7  verify_add_openbmc_user  ${DeviceName}  test7  qwsd27  7  new_username=tester7
    Step  8  verify_add_openbmc_user  ${DeviceName}  test8  qwsd28  8  new_username=tester8
    Step  9  verify_add_openbmc_user  ${DeviceName}  test9  qwsd29  9  new_username=tester9
    Step  10  verify_add_openbmc_user  ${DeviceName}  test10  qwsd210  10  new_username=tester10
    Step  11  verify_add_openbmc_user  ${DeviceName}  test11  qwsd211  11  new_username=tester11
    Step  12  verify_add_openbmc_user  ${DeviceName}  test12  qwsd212  12  new_username=tester12
    Step  13  verify_add_openbmc_user  ${DeviceName}  test13  qwsd213  13  new_username=tester13
    Step  14  verify_add_openbmc_user  ${DeviceName}  test14  qwsd214  14  new_username=tester14
    Step  15  verify_add_openbmc_user  ${DeviceName}  test15  qwsd215  15  new_username=tester15

Watchdog Event Logging Test
    Step  1  watchdog_do_not_log_bit  ${DeviceName}
    Step  2  watchdog_time_use_set  ${DeviceName}
#    Step  3  watchdog_timeout_action_set  ${DeviceName}

Check Fan Status Monitor
    ${sensor} =  call_sensor_class  ${device_info_a}
    Step  1  Call Method  ${sensor}  verify_normal_status
    Step  2  fan_status_monitor  ${device_info_a}

Check multi-node feature
    Step  1  check_default_multi_node_info  ${device_info_a}  ${device_info_b}
    Step  2  check_muli_node_role_change  ${device_info_a}  ${device_info_b}

BMC Online Update
    ${FW_class} =  call_firmware_class  ${DeviceName}
    ${SEL} =  call_sel_class  ${DeviceName}
    Call Method  ${SEL}  sel_clear
    Step  1  Call Method  ${FW_class}  check_fw_version
    Step  2  Call Method  ${FW_class}  firmware_flash  bmc  upgrade=False
    Step  3  Call Method  ${FW_class}  check_fw_version  bmc_version=old
    Step  4  Call Method  ${FW_class}  firmware_flash  bmc  upgrade=True
    Step  5  Call Method  ${FW_class}  check_fw_version
    Step  6  Call Method  ${SEL}  check_sel_list_unexpect_event  ${error_messages_list}

BIOS Online Update
    ${FW_class} =  call_firmware_class  ${DeviceName}
    ${SEL} =  call_sel_class  ${DeviceName}
    Call Method  ${SEL}  sel_clear
    Step  1  Call Method  ${FW_class}  check_fw_version
    Step  2  Call Method  ${FW_class}  firmware_flash  bios  upgrade=False
    Step  3  Call Method  ${FW_class}  check_fw_version  bios_version=old
    Step  4  Call Method  ${FW_class}  firmware_flash  bios  upgrade=True
    Step  5  Call Method  ${FW_class}  check_fw_version
    Step  6  Call Method  ${SEL}  check_sel_list_unexpect_event  ${error_messages_list}

CPLD Update
    ${FW_class} =  call_firmware_class  ${DeviceName}
    ${SEL} =  call_sel_class  ${DeviceName}
    Call Method  ${SEL}  sel_clear
    Step  1  Call Method  ${FW_class}  check_fw_version
    Step  2  Call Method  ${FW_class}  firmware_flash  cpld  upgrade=False
    Step  3  Call Method  ${FW_class}  check_fw_version  cpld_version=old
    Step  4  Call Method  ${FW_class}  firmware_flash  cpld  upgrade=True
    Step  5  Call Method  ${FW_class}  check_fw_version
    Step  6  Call Method  ${SEL}  check_sel_list_unexpect_event  ${error_messages_list}

PSU FW Update
    ${FW_class} =  call_firmware_class  ${DeviceName}
    ${SEL} =  call_sel_class  ${DeviceName}
    Call Method  ${SEL}  sel_clear
    Step  1  Call Method  ${FW_class}  check_fw_version
    Step  2  Call Method  ${FW_class}  firmware_flash  psu  upgrade=False
    Step  3  Call Method  ${FW_class}  check_fw_version  psu_version=old
    Step  4  Call Method  ${FW_class}  firmware_flash  psu  upgrade=True
    Step  5  Call Method  ${FW_class}  check_fw_version
    Step  6  Call Method  ${SEL}  check_sel_list_unexpect_event  ${error_messages_list}

BMC Online Update Stress
    FOR    ${INDEX}    IN RANGE    ${FW_STRESS_CYCLE}
       Print Loop Info  ${INDEX}  ${FW_STRESS_CYCLE}
       BMC Online Update
    END

BIOS Online Update Stress
    FOR    ${INDEX}    IN RANGE    ${FW_STRESS_CYCLE}
       Print Loop Info  ${INDEX}  ${FW_STRESS_CYCLE}
       BIOS Online Update
    END

Print Loop Info
    [Arguments]    ${CUR_INDEX}    ${MaxLoopNum}
    Log  *******************************************
    Log  *** Test Loop \#: ${CUR_INDEX} / ${MaxLoopNum}-1 ***
    Log  *

AC Power Cycle the Device
    Connect Device  ${DeviceName}  bmc
    powercycle_pdu1  ${DeviceName}
    wait_pattern  ${DeviceName}  ${BOOT_REGEX}
    Disconnect Device  ${DeviceName}  bmc

wait boot prompt
    [Arguments]  ${Dev}  ${console_type}
    Connect Device  ${Dev}  ${console_type}
    wait_prompt  ${Dev}  ${console_type}  timeout=300
    Disconnect Device  ${Dev}  ${console_type}

Restore the user list
    run_ipmi_cmd  %{bmc_username_1}  %{bmc_ipv4_ip_1}  %{bmc_password_1}  raw 0x32 0x66  True
    run_ipmi_cmd  %{bmc_username_1}  %{bmc_ipv4_ip_1}  %{bmc_password_1}  raw 00 02 03  True
    wait boot prompt  ${DeviceName}  bmc

Check System Status
# Check the system status before test
# TODO: check more status
    ${sensor} =  call_sensor_class  ${DeviceName}
    Call Method  ${sensor}  verify_normal_status

Sensor Read Stress Test
    ${sensor} =  call_sensor_class  ${DeviceName}
    ${SEL} =  call_sel_class  ${DeviceName}
    Call Method  ${SEL}  sel_clear
    Call Method  ${sensor}  verify_normal_status
    FOR    ${INDEX}    IN RANGE    ${FRUREAD_CYCLES}
        Print Loop Info  ${INDEX}  ${FRUREAD_CYCLES}
        Call Method  ${sensor}  refresh_sensor
        Call Method  ${sensor}  verify_normal_status
    END
    Call Method  ${SEL}  check_sel_list_unexpect_event  ${error_messages_list}

run ipmi command "Get Device ID"
    ipmi_standard_cmd  ${device_info_a}  ${cmd_get_deviceID}  ${rsp_device_id}
#    Step  1  run ipmi get cmd ar  %{bmc_username_1}  %{bmc_ipv4_ip_1}  %{bmc_password_1}  ${cmd_get_deviceID}  ${rsp_device_id}

run ipmi command "cold reset"
    ${openbmc_info} =  call_openbmc_class  ${device_info_a}
    Connect Device  ${DeviceName}  bmc
    Step  1  Call Method  ${openbmc_info}  ipmi_dev_global_cmd  cold_reset  rm=True
    Step  2  wait_pattern  ${DeviceName}  ${BOOT_REGEX}
    Disconnect Device  ${DeviceName}  bmc
    ipmi_standard_cmd  ${DeviceName}  ${cmd_get_deviceID}  ${rsp_device_id}

run ipmi command "warm reset"
    Step  1  run ipmi cmd  %{bmc_username_1}  %{bmc_ipv4_ip_1}  %{bmc_password_1}  ${cmd_warm_reset}

run ipmi command "Get Self Test Results"
    Step  1  run ipmi get cmd ar  %{bmc_username_1}  %{bmc_ipv4_ip_1}  %{bmc_password_1}  ${cmd_self_test}  ${rsp_cmd_self_test}

run ipmi command "Set ACPI Power State"
    Step  1  run ipmi cmd  %{bmc_username_1}  %{bmc_ipv4_ip_1}  %{bmc_password_1}  ${cmd_Set_ACPI_Power_State}  True

run ipmi command "Get ACPI Power State"
    Step  1  run ipmi cmd  %{bmc_username_1}  %{bmc_ipv4_ip_1}  %{bmc_password_1}  ${cmd_Get_ACPI_Power_State}

run ipmi command "Set Watchdog Timer"
    watchdog_do_not_log_bit  ${device_info_a}  wdg_not_reset=True

run ipmi command "Get Watchdog Timer"
    watchdog_do_not_log_bit  ${device_info_a}  wdg_not_reset=True

run ipmi command "Reset Watchdog Timer"
    watchdog_do_not_log_bit  ${device_info_a}

run ipmi command "Set BMC Global enables"
    Step  1  run ipmi cmd  %{bmc_username_1}  %{bmc_ipv4_ip_1}  %{bmc_password_1}  ${cmd_set_bmc_global_enables}
    Step  2  run ipmi cmd  %{bmc_username_1}  %{bmc_ipv4_ip_1}  %{bmc_password_1}  ${cmd_get_bmc_global_enables}

run ipmi command "Get BMC Global enables"
    Step  1  run ipmi get cmd ar  %{bmc_username_1}  %{bmc_ipv4_ip_1}  %{bmc_password_1}  ${cmd_get_bmc_global_enables}  ${rsp_get_bmc_global_enables}

run ipmi command "Clear Message Flags"
    Step  1  run ipmi cmd  %{bmc_username_1}  %{bmc_ipv4_ip_1}  %{bmc_password_1}  ${cmd_clear_message_flags}

run ipmi command "Get Message Flags"
#    Step  1  run ipmi cmd  %{bmc_username_1}  %{bmc_ipv4_ip_1}  %{bmc_password_1}  ${cmd_clear_message_flags}
    Step  1  run ipmi get cmd ar  %{bmc_username_1}  %{bmc_ipv4_ip_1}  %{bmc_password_1}  ${cmd_get_message_flags}  ${rsp_cmd_Get_message_flags}

run ipmi command "Enable Message Channel Receive"
    Step  1  run ipmi cmd  %{bmc_username_1}  %{bmc_ipv4_ip_1}  %{bmc_password_1}  ${cmd_Enable_Message_Channel_Receive}

run ipmi command "Get System GUID"
    Step  1  run ipmi cmd  %{bmc_username_1}  %{bmc_ipv4_ip_1}  %{bmc_password_1}  ${cmd_get_system_GUID}

run ipmi command "Get Channel Authentication capabilities"
    Step  1  run ipmi cmd  %{bmc_username_1}  %{bmc_ipv4_ip_1}  %{bmc_password_1}  ${cmd_Get_Channel_Authentication_capabilities}

run ipmi command "Get Session Challenge" by remote ipmitool
    Step  1  run ipmi cmd  %{bmc_username_1}  %{bmc_ipv4_ip_1}  %{bmc_password_1}  ${cmd_get_session_challenge}

run ipmi command "Set Session Privilege Level" by remote ipmitool
    Step  1  run ipmi get cmd ar  %{bmc_username_1}  %{bmc_ipv4_ip_1}  %{bmc_password_1}  ${cmd_set_session_privilege_Level}  ${cmd_get_session_privilege_Level}

run ipmi command "Get Session Info"
    Step  1  run ipmi cmd  %{bmc_username_1}  %{bmc_ipv4_ip_1}  %{bmc_password_1}  ${cmd_get_session_info}  True

run ipmi command "Get AuthCode"
    Step  1  run ipmi cmd  %{bmc_username_1}  %{bmc_ipv4_ip_1}  %{bmc_password_1}  ${cmd_Get_AuthCode}

run ipmi command "Set Channel Access"
    Step  1  run ipmi cmd  %{bmc_username_1}  %{bmc_ipv4_ip_1}  %{bmc_password_1}  ${cmd_Set_Channel_Access}

run ipmi command "Get Channel Access"
    Step  1  run ipmi cmd  %{bmc_username_1}  %{bmc_ipv4_ip_1}  %{bmc_password_1}  ${cmd_Get_Channel_Access}

run ipmi command "Get Channel Info"
    Step  1  run ipmi get cmd ar  %{bmc_username_1}  %{bmc_ipv4_ip_1}  %{bmc_password_1}  ${cmd_Get_Channel_Info}  ${rsp_Get_Channel_Info}

run ipmi command "Set User Access"
    Step  1  run ipmi cmd  %{bmc_username_1}  %{bmc_ipv4_ip_1}  %{bmc_password_1}  ${cmd_Set_User_Access}

run ipmi command "Get User Access"
    Step  1  run ipmi cmd  %{bmc_username_1}  %{bmc_ipv4_ip_1}  %{bmc_password_1}  ${cmd_Get_User_Access}

run ipmi command "Set User name"
    Step  1  run ipmi cmd  %{bmc_username_1}  %{bmc_ipv4_ip_1}  %{bmc_password_1}  ${cmd_Set_User_name}

run ipmi command "Get User name"
    Step  1  run ipmi get cmd ar  %{bmc_username_1}  %{bmc_ipv4_ip_1}  %{bmc_password_1}  ${cmd_Get_User_name}

run ipmi command "Set User Password"
    Step  1  run ipmi cmd  %{bmc_username_1}  %{bmc_ipv4_ip_1}  %{bmc_password_1}  ${cmd_Set_User_Password}

run ipmi command "Get Payload Activation Status"
    Step  1  run ipmi cmd  %{bmc_username_1}  %{bmc_ipv4_ip_1}  %{bmc_password_1}  ${cmd_Get_Payload_Activation_Status}  True

run ipmi command "Get Payload Instance Info"
    Step  1  run ipmi cmd  %{bmc_username_1}  %{bmc_ipv4_ip_1}  %{bmc_password_1}  ${cmd_Get_Payload_Instance_Info}  True

run ipmi command "Set user Payload Access"
    Step  1  run ipmi cmd  %{bmc_username_1}  %{bmc_ipv4_ip_1}  %{bmc_password_1}  ${cmd_Set_user_Payload_Access}

run ipmi command "Get user Payload Access"
    Step  1  run ipmi cmd  %{bmc_username_1}  %{bmc_ipv4_ip_1}  %{bmc_password_1}  ${cmd_Get_user_Payload_Access}  True

run ipmi command "Get channel Payload support"
    Step  1  run ipmi cmd  %{bmc_username_1}  %{bmc_ipv4_ip_1}  %{bmc_password_1}  ${cmd_Get_channel_Payload_support}

run ipmi command "Get channel Payload Version"
    Step  1  run ipmi cmd  %{bmc_username_1}  %{bmc_ipv4_ip_1}  %{bmc_password_1}  ${cmd_Get_channel_Payload_Version}

run ipmi command "Get Channel Cipher Suites"
    Step  1  run ipmi cmd  %{bmc_username_1}  %{bmc_ipv4_ip_1}  %{bmc_password_1}  ${cmd_Get_Channel_Cipher_Suites}

run ipmi command "Master Write-Read"
    Step  1  run ipmi cmd  %{bmc_username_1}  %{bmc_ipv4_ip_1}  %{bmc_password_1}  ${cmd_Master_Write_Read}

run ipmi command "Set Channel Security Keys 56h"
    Step  1  run ipmi cmd  %{bmc_username_1}  %{bmc_ipv4_ip_1}  %{bmc_password_1}  ${cmd_Set_Channel_Security_Keys_56h}

run ipmi command "Get Chassis Capabilities"
    Step  1  run ipmi cmd  %{bmc_username_1}  %{bmc_ipv4_ip_1}  %{bmc_password_1}  ${cmd_Get_Chassis_Capabilities}

run ipmi command "Get Chassis Status"
    Step  1  run ipmi get cmd ar  %{bmc_username_1}  %{bmc_ipv4_ip_1}  %{bmc_password_1}  ${cmd_Get_Chassis_Status}  ${rsp_Get_Chassis_Status}

run ipmi command "Chassis power down"
    Step  1  run ipmi cmd  %{bmc_username_1}  %{bmc_ipv4_ip_1}  %{bmc_password_1}  ${cmd_Get_Chassis_Control_Power_Down}
    Step  2  set time delay  30
    Step  3  run ipmi get cmd ar  %{bmc_username_1}  %{bmc_ipv4_ip_1}  %{bmc_password_1}  power status  ${rsp_Get_Chassis_Status_Off}
#    Step  3  Keyword Retry  ssh_command_exec_ping  %{server_username_1}  %{server_ipv4_ip_1}  %{server_password_1}  %{DUT_ipv4_ip_1}  5  loss

run ipmi command "Chassis power up"
    Step  1  run ipmi cmd  %{bmc_username_1}  %{bmc_ipv4_ip_1}  %{bmc_password_1}  ${cmd_Get_Chassis_Control_Power_Up}
    Step  2  set time delay  50
    Step  3  run ipmi get cmd ar  %{bmc_username_1}  %{bmc_ipv4_ip_1}  %{bmc_password_1}  power status  ${rsp_Get_Chassis_Status_On}
    Step  4  set time delay  120

run ipmi command "Chassis power cycle"
    Step  1  run ipmi cmd  %{bmc_username_1}  %{bmc_ipv4_ip_1}  %{bmc_password_1}  ${cmd_Get_Chassis_Control_Power_Cycle}
    Step  2  set time delay  10
    Step  3  Keyword Retry  run ipmi get cmd ar  %{bmc_username_1}  %{bmc_ipv4_ip_1}  %{bmc_password_1}  power status  ${rsp_Get_Chassis_Status_Off}
    Step  4  set time delay  60
    Step  5  Keyword Retry  run ipmi get cmd ar  %{bmc_username_1}  %{bmc_ipv4_ip_1}  %{bmc_password_1}  power status  ${rsp_Get_Chassis_Status_On}
    Step  6  set time delay  100

run ipmi command "Chassis soft shutdown"
    Step  1  run ipmi cmd  %{bmc_username_1}  %{bmc_ipv4_ip_1}  %{bmc_password_1}  ${cmd_Get_Chassis_Control_Soft_Shutdown}
    Step  2  set time delay  100
    Step  3  run ipmi get cmd ar  %{bmc_username_1}  %{bmc_ipv4_ip_1}  %{bmc_password_1}  power status  ${rsp_Get_Chassis_Status_Off}

run ipmi command "Chassis Identify"
    Step  1  run ipmi cmd  %{bmc_username_1}  %{bmc_ipv4_ip_1}  %{bmc_password_1}  ${cmd_Chassis_Identify}

run ipmi command "Always stay power off"
    Step  1  run ipmi cmd  %{bmc_username_1}  %{bmc_ipv4_ip_1}  %{bmc_password_1}  ${cmd_Set_Power_Restore_policy_00}

run ipmi command "Restore prior state"
    Step  1  run ipmi cmd  %{bmc_username_1}  %{bmc_ipv4_ip_1}  %{bmc_password_1}  ${cmd_Set_Power_Restore_policy_01}

run ipmi command "Always stay power up"
    Step  1  run ipmi cmd  %{bmc_username_1}  %{bmc_ipv4_ip_1}  %{bmc_password_1}  ${cmd_Set_Power_Restore_policy_02}

run ipmi command "No change"
    Step  1  run ipmi cmd  %{bmc_username_1}  %{bmc_ipv4_ip_1}  %{bmc_password_1}  ${cmd_Set_Power_Restore_policy_03}

run ipmi command "Get System Restart Cause"
    Step  1  run ipmi get cmd ar  %{bmc_username_1}  %{bmc_ipv4_ip_1}  %{bmc_password_1}  ${cmd_Get_System_Restart_Cause}  ${rsp_Get_System_Restart_Cause}

run ipmi command "Set System Boot Options"
#    Step  1  run ipmi cmd  %{bmc_username_1}  %{bmc_ipv4_ip_1}  %{bmc_password_1}  ${cmd_1_Set_System_Boot_Options}
#    Step  2  run ipmi cmd  %{bmc_username_1}  %{bmc_ipv4_ip_1}  %{bmc_password_1}  ${cmd_2_Set_System_Boot_Options}
    Step  3  run ipmi cmd  %{bmc_username_1}  %{bmc_ipv4_ip_1}  %{bmc_password_1}  ${cmd_3_Set_System_Boot_Options}

run ipmi command "Get System Boot Options"
    Step  1  run ipmi get cmd ar  %{bmc_username_1}  %{bmc_ipv4_ip_1}  %{bmc_password_1}  ${cmd_Get_System_Boot_Options}  ${cmd_rsp_Get_System_Boot_Options}

run ipmi command "Set Front Panel Button Enables"
    Step  1  run ipmi cmd  %{bmc_username_1}  %{bmc_ipv4_ip_1}  %{bmc_password_1}  ${cmd_Set_Front_Panel_Button_Enables}

run ipmi command "Set Power Cycle Interval"
    Step  1  run ipmi cmd  %{bmc_username_1}  %{bmc_ipv4_ip_1}  %{bmc_password_1}  ${cmd_Set_Power_Cycle_Interval}

run ipmi command "Get POH Counter"
    Step  1  run ipmi cmd  %{bmc_username_1}  %{bmc_ipv4_ip_1}  %{bmc_password_1}  ${cmd_Get_POH_Counter}

run ipmi command "Set Event Receiver"
    Step  1  run ipmi cmd  %{bmc_username_1}  %{bmc_ipv4_ip_1}  %{bmc_password_1}  ${cmd_Set_Event_Receiver}

run ipmi command "Get Event Receiver"
    Step  1  run ipmi cmd  %{bmc_username_1}  %{bmc_ipv4_ip_1}  %{bmc_password_1}  ${cmd_Get_Event_Receiver}

run ipmi command "Platform Event Message"
    Step  1  run ipmi cmd  %{bmc_username_1}  %{bmc_ipv4_ip_1}  %{bmc_password_1}  ${cmd_Platform_Event_Message}

run ipmi command "Get PEF Capabilities"
    Step  1  run ipmi cmd  %{bmc_username_1}  %{bmc_ipv4_ip_1}  %{bmc_password_1}  ${cmd_Get_PEF_Capabilities}

run ipmi command "Disable postpone timer"
    Step  1  run ipmi cmd  %{bmc_username_1}  %{bmc_ipv4_ip_1}  %{bmc_password_1}  ${cmd_Disable_postpone_timer}

run ipmi command "arm timer"
    Step  1  run ipmi cmd  %{bmc_username_1}  %{bmc_ipv4_ip_1}  %{bmc_password_1}  ${cmd_arm_timer}

run ipmi command "get present countdown value"
    Step  1  run ipmi cmd  %{bmc_username_1}  %{bmc_ipv4_ip_1}  %{bmc_password_1}  ${cmd_get_present_countdown_value}

run ipmi command "Set PEF Configuration Parameters"
    Step  1  run ipmi cmd  %{bmc_username_1}  %{bmc_ipv4_ip_1}  %{bmc_password_1}  ${cmd_Set_PEF_Capabilities_1}
    Step  2  run ipmi cmd  %{bmc_username_1}  %{bmc_ipv4_ip_1}  %{bmc_password_1}  ${cmd_Set_PEF_Capabilities_2}
    Step  3  run ipmi cmd  %{bmc_username_1}  %{bmc_ipv4_ip_1}  %{bmc_password_1}  ${cmd_Set_PEF_Capabilities_3}
    Step  4  run ipmi cmd  %{bmc_username_1}  %{bmc_ipv4_ip_1}  %{bmc_password_1}  ${cmd_Set_PEF_Capabilities_4}
    Step  5  run ipmi cmd  %{bmc_username_1}  %{bmc_ipv4_ip_1}  %{bmc_password_1}  ${cmd_Set_PEF_Capabilities_5}
    Step  6  run ipmi cmd  %{bmc_username_1}  %{bmc_ipv4_ip_1}  %{bmc_password_1}  ${cmd_Set_PEF_Capabilities_6}

run ipmi command "Get PEF Configuration Parameters"
    Step  1  run ipmi cmd  %{bmc_username_1}  %{bmc_ipv4_ip_1}  %{bmc_password_1}  ${cmd_Get_PEF_Configuration_Parameters_1}
    Step  2  run ipmi cmd  %{bmc_username_1}  %{bmc_ipv4_ip_1}  %{bmc_password_1}  ${cmd_Get_PEF_Configuration_Parameters_2}
    Step  3  run ipmi cmd  %{bmc_username_1}  %{bmc_ipv4_ip_1}  %{bmc_password_1}  ${cmd_Get_PEF_Configuration_Parameters_3}

run ipmi command "Set Last Processed Event ID"
    Step  1  run ipmi cmd  %{bmc_username_1}  %{bmc_ipv4_ip_1}  %{bmc_password_1}  ${cmd_Set_Last_Processed_Event_ID}

run ipmi command "Get Last Processed Event ID"
    Step  1  run ipmi cmd  %{bmc_username_1}  %{bmc_ipv4_ip_1}  %{bmc_password_1}  ${cmd_Get_Last_Processed_Event_ID}

run ipmi command "Alert Immediate"
    Step  1  run ipmi cmd  %{bmc_username_1}  %{bmc_ipv4_ip_1}  %{bmc_password_1}  ${cmd_Alert_Immediate}

run ipmi command "PET Acknowledge"
    Step  1  run ipmi cmd  %{bmc_username_1}  %{bmc_ipv4_ip_1}  %{bmc_password_1}  ${cmd_PET_Acknowledge}

run ipmi command "Set Sensor Hysteresis"
    Step  1  run ipmi cmd  %{bmc_username_1}  %{bmc_ipv4_ip_1}  %{bmc_password_1}  ${cmd_Set_Sensor_Hysteresis}

run ipmi command "Get Sensor Hysteresis"
    Step  1  run ipmi cmd  %{bmc_username_1}  %{bmc_ipv4_ip_1}  %{bmc_password_1}  ${cmd_Get_Sensor_Hysteresis}

run ipmi command "Set Sensor Threshold"
    check_sensor_threshold_set  ${device_info_a}

run ipmi command "Get Sensor Threshold"
    Step  1  run ipmi cmd  %{bmc_username_1}  %{bmc_ipv4_ip_1}  %{bmc_password_1}  ${cmd_Get_Sensor_Threshold}

run ipmi command "Set Sensor Event Enable"
    Step  1  run ipmi cmd  %{bmc_username_1}  %{bmc_ipv4_ip_1}  %{bmc_password_1}  ${cmd_Set_Sensor_Event_Enable}

run ipmi command "Get Sensor Event Enable"
    Step  1  run ipmi cmd  %{bmc_username_1}  %{bmc_ipv4_ip_1}  %{bmc_password_1}  ${cmd_Get_Sensor_Event_Enable}

run ipmi command "Re-arm Sensor Event"
    Step  1  run ipmi cmd  %{bmc_username_1}  %{bmc_ipv4_ip_1}  %{bmc_password_1}  ${cmd_Re_arm_Sensor_Event}

run ipmi command "Get Sensor Event Status"
    Step  1  run ipmi cmd  %{bmc_username_1}  %{bmc_ipv4_ip_1}  %{bmc_password_1}  ${cmd_Get_Sensor_Event_Status}

run ipmi command "Get Sensor Reading"
    Step  1  run ipmi cmd  %{bmc_username_1}  %{bmc_ipv4_ip_1}  %{bmc_password_1}  ${cmd_Get_Sensor_Reading}

run ipmi command "Get FRU Inventory Area Info"
    Step  1  run ipmi get cmd ar  %{bmc_username_1}  %{bmc_ipv4_ip_1}  %{bmc_password_1}  ${cmd_Get_FRU_Inventory_Area_Info}  ${rsp_cmd_Get_FRU_Inventory}

run ipmi command "Write FRU Data"
    Step  1  run ipmi get cmd ar  %{bmc_username_1}  %{bmc_ipv4_ip_1}  %{bmc_password_1}  ${cmd_Write_FRU_Inventory_Area_Info}  ${rsp_cmd_Write_FRU_Inventory_Area_Info}

run ipmi command "Get SDR Repository Info"
    Step  1  run ipmi cmd  %{bmc_username_1}  %{bmc_ipv4_ip_1}  %{bmc_password_1}  ${cmd_Get_SDR_Repository_Info}

run ipmi command "Get SDR Repository Allocation Info"
    Step  1  run ipmi get cmd ar  %{bmc_username_1}  %{bmc_ipv4_ip_1}  %{bmc_password_1}  ${cmd_Get_SDR_Repository_Allocation_Info}  ${rsp_Get_SDR_Repository_Allocation_Info}

run ipmi command "Reserve SDR Repository"
    Step  1  run ipmi cmd  %{bmc_username_1}  %{bmc_ipv4_ip_1}  %{bmc_password_1}  ${cmd_Reserve_SDR_Repository}

run ipmi command "Get SDR"
    Step  1  run ipmi get cmd ar  %{bmc_username_1}  %{bmc_ipv4_ip_1}  %{bmc_password_1}  ${cmd_Get_SDR}  ${rsp_cmd_Get_SDR}

run ipmi command "Partial Add SDR"
    Step  1  run ipmi cmd  %{bmc_username_1}  %{bmc_ipv4_ip_1}  %{bmc_password_1}  ${cmd_Partial_Add_SDR}

run ipmi command "Delete SDR"
    Step  1  run ipmi cmd  %{bmc_username_1}  %{bmc_ipv4_ip_1}  %{bmc_password_1}  ${cmd_Delete_SDR}

run ipmi command "Clear SDR Repository"
    Step  1  run ipmi cmd  %{bmc_username_1}  %{bmc_ipv4_ip_1}  %{bmc_password_1}  ${cmd_Clear_SDR_Repository}

run ipmi command "Enter SDR Repository Update Mode"
    Step  1  run ipmi cmd  %{bmc_username_1}  %{bmc_ipv4_ip_1}  %{bmc_password_1}  ${cmd_Enter_SDR_Repository_Update_Mode}

run ipmi command "Exit SDR Repository Update Mode"
    Step  1  run ipmi cmd  %{bmc_username_1}  %{bmc_ipv4_ip_1}  %{bmc_password_1}  ${cmd_Exit_SDR_Repository_Update_Mode}

run ipmi command "Run Initialization Agent"
    Step  1  run ipmi cmd  %{bmc_username_1}  %{bmc_ipv4_ip_1}  %{bmc_password_1}  ${cmd_Run_Initialization_Agent}

run ipmi command "Get SEL Info"
    Step  1  run ipmi cmd  %{bmc_username_1}  %{bmc_ipv4_ip_1}  %{bmc_password_1}  ${cmd_Get_SEL_Info}
    #Step  1  run ipmi get cmd ar  %{bmc_username_1}  %{bmc_ipv4_ip_1}  %{bmc_password_1}  ${cmd_Get_SEL_Info}  ${rsp_Get_SEL_Info}

run ipmi command "Get SEL Allocation Info"
    Step  1  run ipmi cmd  %{bmc_username_1}  %{bmc_ipv4_ip_1}  %{bmc_password_1}  ${cmd_Get_SEL_Allocation_Info}

run ipmi command "Reserve SEL"
    Step  1  run ipmi cmd  %{bmc_username_1}  %{bmc_ipv4_ip_1}  %{bmc_password_1}  ${cmd_Reserve_SEL}

run ipmi command "Get SEL Entry"
    Step  1  verify_get_sel_entry  %{DUT_ipv4_ip_1}  %{DUT_username_1}  %{DUT_password_1}

run ipmi command "Add SEL Entry"
#    Step  1  run_ipmi_cmd_sel_clear  Artemis
   # Step  1  run ipmi cmd  %{bmc_username_1}  %{bmc_ipv4_ip_1}  %{bmc_password_1}  ${cmd_Add_SEL_Entry}
    Step  1  verify add sel entry ar  %{bmc_ipv4_ip_1}  %{bmc_username_1}  %{bmc_password_1}

run ipmi command "Delete SEL Entry"
    Step  1  verify add sel entry ar  %{bmc_ipv4_ip_1}  %{bmc_username_1}  %{bmc_password_1}
    Step  2  verify_delete_sel_entry_ar  Artemis  %{DUT_ipv4_ip_1}  %{DUT_username_1}  %{DUT_password_1}

run ipmi command "Clear SEL"
    Step  1  run ipmi cmd  %{bmc_username_1}  %{bmc_ipv4_ip_1}  %{bmc_password_1}  ${cmd_Clear_SEL}

run ipmi command "Get SEL Time"
    Step  1  run ipmi cmd  %{bmc_username_1}  %{bmc_ipv4_ip_1}  %{bmc_password_1}  ${cmd_Get_SEL_Time}

run ipmi command "Set SEL Time"
    Step  1  run ipmi cmd  %{bmc_username_1}  %{bmc_ipv4_ip_1}  %{bmc_password_1}  ${cmd_Set_SEL_Time}

run ipmi command "Get SEL Time UTC Offset"
    Step  1  run ipmi cmd  %{bmc_username_1}  %{bmc_ipv4_ip_1}  %{bmc_password_1}  ${cmd_Get_SEL_Time_UTC_Offset}

run ipmi command "Set SEL Time UTC Offset"
    Step  1  run ipmi cmd  %{bmc_username_1}  %{bmc_ipv4_ip_1}  %{bmc_password_1}  ${cmd_Set_SEL_Time_UTC_Offset}

#run ipmi command "Set LAN Configuration Parameters"

run ipmi command "Get LAN Configuration Parameters"
    Step  1  verify openbmc lan info  %{bmc_username_1}  %{bmc_ipv4_ip_1}  %{bmc_password_1}  ${cmd_ipmitool_lan_print_1}  ${bmc_lan_1_info_dhcp}
    Step  2  verify openbmc lan info  %{bmc_username_1}  %{bmc_ipv4_ip_1}  %{bmc_password_1}  ${cmd_ipmitool_lan_print_2}  ${bmc_lan_2_info_dhcp}

run ipmi command "Get Message"
    Step  1  run ipmi cmd  %{bmc_username_1}  %{bmc_ipv4_ip_1}  %{bmc_password_1}  ${cmd_Get_Message}

run ipmi command "Send Message"
    Step  1  run ipmi cmd  %{bmc_username_1}  %{bmc_ipv4_ip_1}  %{bmc_password_1}  ${cmd_Send_Message}

run ipmi command "Read Event Message Buffer"
    Step  1  run ipmi get cmd ar  %{bmc_username_1}  %{bmc_ipv4_ip_1}  %{bmc_password_1}  ${cmd_Read_Event_Message_Buffer}  ${rsp_Read_Event_Message_Buffer}

run ipmi command "Activate Session"
    Step  1  run ipmi cmd  %{bmc_username_1}  %{bmc_ipv4_ip_1}  %{bmc_password_1}  ${cmd_Activate_Session}

run ipmi command "Close Session"
    Step  1  run ipmi cmd  %{bmc_username_1}  %{bmc_ipv4_ip_1}  %{bmc_password_1}  ${cmd_Close_Session}

run ipmi command "Activate Payload"
    Step  1  run ipmi cmd  %{bmc_username_1}  %{bmc_ipv4_ip_1}  %{bmc_password_1}  ${cmd_Activate_Payload}  True

run ipmi command "Deactivate Payload"
    Step  1  run ipmi cmd  %{bmc_username_1}  %{bmc_ipv4_ip_1}  %{bmc_password_1}  ${cmd_Deactivate_Payload}  True

run ipmi command "Set Channel Security Keys 55h"
    Step  1  run ipmi cmd  %{bmc_username_1}  %{bmc_ipv4_ip_1}  %{bmc_password_1}  ${cmd_Set_Channel_Security_Keys_55h}

Check IPMIStandcmd Test
    Step  1  execute_commands_ssh  ${DeviceName}  ${ipmitool_get_deviceID}
    Step  2  execute_commands_ssh  ${DeviceName}  ${ipmitool_cold_reset}

IP Setting Test
#    Step  1  verify_openbmc_lan_status  %{bmc_ipv4_ip_1}  %{bmc_username_1}  %{bmc_password_1}  ${BMC_lan_print_1_ip_address}
    Step  1  run ipmi cmd  %{bmc_username_1}  %{bmc_ipv4_ip_1}  %{bmc_password_1}  lan set 1 ipsrc static
    Step  2  run ipmi cmd  %{bmc_username_1}  %{bmc_ipv4_ip_1}  %{bmc_password_1}  lan set 1 ipaddr 192.168.10.10
    Step  3  run ipmi cmd  %{bmc_username_1}  %{bmc_ipv4_ip_1}  %{bmc_password_1}  lan set 1 netmask 255.255.255.0
    Step  4  set time delay  30
    Step  5  verify_openbmc_lan_address  %{bmc_ipv4_ip_1}  %{bmc_username_1}  %{bmc_password_1}  ${BMC_lan_print_1_ip_address}
    Step  6  verify_openbmc_lan_status  %{bmc_ipv4_ip_1}  %{bmc_username_1}  %{bmc_password_1}  ${BMC_lan_print_1_ip_status}
    Step  7  set time delay  3
    Step  8  run ipmi cmd  %{bmc_username_1}  %{bmc_ipv4_ip_1}  %{bmc_password_1}  lan set 1 ipsrc dhcp
    Step  9  set time delay  30

Check BMC dedicate and share port ping stress
    Step  1  verify openbmc lan info  %{bmc_username_1}  %{bmc_ipv4_ip_1}  %{bmc_password_1}  ${cmd_ipmitool_lan_print_1}  ${bmc_lan_1_info_dhcp}
    Step  2  verify openbmc lan info  %{bmc_username_1}  %{bmc_ipv4_ip_1}  %{bmc_password_1}  ${cmd_ipmitool_lan_print_2}  ${bmc_lan_2_info_dhcp}
    Step  3  verify_ssh_ping_function   %{DUT_username_1}  %{DUT_ipv4_ip_1}  %{DUT_password_1}
        ...  ${bmc_ipv4_ip_lan1}  ping_timeout=${ping_timeout}
    Step  4  verify_ssh_ping_function  %{DUT_username_1}  %{DUT_ipv4_ip_1}  %{DUT_password_1}
        ...  ${bmc_ipv4_ip_lan2}  ping_timeout=${ping_timeout}

Setting openBMC SOL configuration Lan_1 Test
    Step  1  run ipmi cmd  %{bmc_username_1}  %{bmc_ipv4_ip_1}  %{bmc_password_1}  sol set enabled true 1  remote=True
    Step  2  run ipmi cmd  %{bmc_username_1}  %{bmc_ipv4_ip_1}  %{bmc_password_1}  sol set non-volatile-bit-rate 115.2  remote=True
    Step  3  run ipmi cmd  %{bmc_username_1}  %{bmc_ipv4_ip_1}  %{bmc_password_1}  sol set volatile-bit-rate 115.2  remote=True

Setting openBMC SOL configuration Lan_2 Test
    Step  1  run ipmi cmd  %{bmc_username_2}  %{bmc_ipv4_ip_2}  %{bmc_password_2}  sol set enabled true 1  remote=True
    Step  2  run ipmi cmd  %{bmc_username_2}  %{bmc_ipv4_ip_2}  %{bmc_password_2}  sol set non-volatile-bit-rate 115.2  remote=True
    Step  3  run ipmi cmd  %{bmc_username_2}  %{bmc_ipv4_ip_2}  %{bmc_password_2}  sol set volatile-bit-rate 115.2  remote=True

Check openBMC SOL Activating Test
    Step  1  verify_sol_function_ar  ${device_info_a}

Set BMC SEL time and Check
    Step  1  ssh_command  %{DUT_username_1}  %{DUT_ipv4_ip_1}  %{DUT_password_1}  ipmitool sel time get  end=True
    Step  2  ssh_command  %{DUT_username_1}  %{DUT_ipv4_ip_1}  %{DUT_password_1}  ipmitool sel time set "2/15/2016 21:26:00"
    Step  3  ssh_command  %{DUT_username_1}  %{DUT_ipv4_ip_1}  %{DUT_password_1}  ipmitool sel time get  end=True

BMC LAN1 Configuration dhcp_1
    Step  1  verify openbmc lan info  %{bmc_username_1}  %{bmc_ipv4_ip_1}  %{bmc_password_1}  ${cmd_ipmitool_lan_print_1}  ${bmc_lan_1_info_dhcp}
    Step  2  run ipmi cmd  %{bmc_username_1}   %{bmc_ipv4_ip_1}  %{bmc_password_1}  mc info   remote=True
BMC LAN1 Configuration dhcp_2
    Step  1  run ipmi cmd  %{bmc_username_1}   %{bmc_ipv4_ip_1}  %{bmc_password_1}  lan print 1  remote=True
BMC LAN2 Configuration dhcp_1
    Step  1  verify openbmc lan info  %{bmc_username_1}  %{bmc_ipv4_ip_1}  %{bmc_password_1}  ${cmd_ipmitool_lan_print_2}  ${bmc_lan_2_info_dhcp}
    Step  2  run ipmi cmd  %{bmc_username_1}  %{bmc_ipv4_ip_1}  %{bmc_password_1}  mc info   remote=True
BMC LAN2 Configuration dhcp_2
    ${bmc_LAN1_ip} =  ssh_command  %{DUT_username_1}  %{DUT_ipv4_ip_1}  %{DUT_password_1}  /usr/local/bin/bmcip1get.sh  end=True
    Step  1  run ipmi cmd  %{bmc_username_1}   ${bmc_LAN1_ip}  %{bmc_password_1}  lan print 2  remote=True
BMC LAN1 Configuration static
    Run Keyword And Continue On Failure  Step  1  verify openbmc lan info  %{bmc_username_1}  %{bmc_ipv4_ip_1}  %{bmc_password_1}  ${cmd_ipmitool_lan_print_1}  ${bmc_lan_1_info_static}
    Step  2  run ipmi cmd  %{bmc_username_1}  %{bmc_ipv4_ip_1}  %{bmc_password_1}  mc info   remote=True
BMC LAN2 Configuration static
    ${bmc_LAN1_ip} =  ssh_command  %{DUT_username_1}  %{DUT_ipv4_ip_1}  %{DUT_password_1}  /usr/local/bin/bmcip1get.sh  end=True
    Run Keyword And Continue On Failure  Step  1  verify openbmc lan info  %{bmc_username_1}  ${bmc_LAN1_ip}  %{bmc_password_1}  ${cmd_ipmitool_lan_print_2}  ${bmc_lan_2_info_static}
    Step  2  run ipmi cmd  %{bmc_username_1}  ${bmc_LAN1_ip}  %{bmc_password_1}  mc info   remote=True

Console Prompt_1
    Console_Prompt_User  Hint:Please unplug the BMC port 1 cable manually !!!
Console Prompt_2
    Console_Prompt_User  Hint:Please Insert the BMC port 1 cable manually !!!
Console Prompt_3
    Console_Prompt_User  Hint:Please unplug the BMC port 2 cable manually !!!
Console Prompt_4
#    ${message}=  Evaluate  "\\033[31mHint:Please Insert the BMC port 2 calbe manually !!!\\033[0m"
    Console_Prompt_User  Please Insert the BMC port 2 cable manually !!!

Ping BMC Port1 dhcp
    ${bmc_LAN1_ip} =  ssh_command  %{DUT_username_1}  %{DUT_ipv4_ip_1}  %{DUT_password_1}  /usr/local/bin/bmcip1get.sh  end=True
#    Step  1  verify_ssh_ping_function   %{DUT_username_1}  %{DUT_ipv4_ip_1}  %{DUT_password_1}
#        ...  ${bmc_LAN1_ip}  ping_timeout=${ping_timeout}
    Step  1  whitebox_exec_ping_openbmc  ${DeviceName}  %{bmc_username_1}  ${bmc_LAN1_ip}   %{bmc_password_1}  10
Ping BMC Port2 dhcp
    ${bmc_LAN2_ip} =  ssh_command  %{DUT_username_1}  %{DUT_ipv4_ip_1}  %{DUT_password_1}  /usr/local/bin/bmcip2get.sh  end=True
    Step  1  whitebox_exec_ping_openbmc  ${DeviceName}  %{bmc_username_1}  ${bmc_LAN2_ip}  %{bmc_password_1}  10
Ping BMC Port1 dhcp loss
    Run Keyword And Continue On Failure  Step  1  whitebox_exec_ping_openbmc  ${DeviceName}  %{bmc_username_1}  ${bmc_ipv4_ip_lan1}  %{bmc_password_1}  10  loss
Ping BMC Port2 dhcp loss
    Run Keyword And Continue On Failure  Step  1  whitebox_exec_ping_openbmc  ${DeviceName}  %{bmc_username_1}  ${bmc_ipv4_ip_lan2}  %{bmc_password_1}  10  loss
Ping BMC Port1 static
    Run Keyword And Continue On Failure  Step  1  whitebox_exec_ping_openbmc  ${DeviceName}  %{bmc_username_1}  192.168.10.10  %{bmc_password_1}  10
Ping BMC Port1 static loss
    Run Keyword And Continue On Failure  Step  1  whitebox_exec_ping_openbmc  ${DeviceName}  %{bmc_username_1}  192.168.10.10  %{bmc_password_1}  10  loss
Ping BMC Port2 static
    Run Keyword And Continue On Failure  Step  1  whitebox_exec_ping_openbmc  ${DeviceName}  %{bmc_username_1}  192.168.10.20  %{bmc_password_1}  10
Ping BMC Port2 static loss
    Run Keyword And Continue On Failure  Step  1  whitebox_exec_ping_openbmc  ${DeviceName}  %{bmc_username_1}  192.168.10.20  %{bmc_password_1}  10  loss

run ipmi command "61"
    ${bmc_LAN1_ip} =  ssh_command  %{DUT_username_1}  %{DUT_ipv4_ip_1}  %{DUT_password_1}  /usr/local/bin/bmcip1get.sh  end=True
    ${bmc_LAN2_ip} =  ssh_command  %{DUT_username_1}  %{DUT_ipv4_ip_1}  %{DUT_password_1}  /usr/local/bin/bmcip2get.sh  end=True
    Step  1  run ipmi get cmd ar  %{bmc_username_1}  ${bmc_LAN1_ip}  %{bmc_password_1}  ${cmd_get_deviceID}  ${rsp_device_id}
    Step  2  run ipmi get cmd ar  %{bmc_username_1}  ${bmc_LAN2_ip}  %{bmc_password_1}  ${cmd_get_deviceID}  ${rsp_device_id}

Ip setting port1_static
    Step  1  run ipmi cmd  %{bmc_username_1}  %{bmc_ipv4_ip_1}  %{bmc_password_1}  lan set 1 ipsrc static
    Step  2  run ipmi cmd  %{bmc_username_1}  %{bmc_ipv4_ip_1}  %{bmc_password_1}  lan set 1 ipaddr 192.168.10.10
    Step  3  run ipmi cmd  %{bmc_username_1}  %{bmc_ipv4_ip_1}  %{bmc_password_1}  lan set 1 netmask 255.255.255.0
Ip setting port2_static
    ${bmc_LAN1_ip} =  ssh_command  %{DUT_username_1}  %{DUT_ipv4_ip_1}  %{DUT_password_1}  /usr/local/bin/bmcip1get.sh  end=True
    ${bmc_LAN2_ip} =  ssh_command  %{DUT_username_1}  %{DUT_ipv4_ip_1}  %{DUT_password_1}  /usr/local/bin/bmcip2get.sh  end=True
    Step  1  run ipmi cmd  %{bmc_username_1}  ${bmc_LAN2_ip}  %{bmc_password_1}  lan set 2 ipsrc static
    Step  2  run ipmi cmd  %{bmc_username_1}  ${bmc_LAN2_ip}  %{bmc_password_1}  lan set 2 ipaddr 192.168.10.20
    Step  3  run ipmi cmd  %{bmc_username_1}  ${bmc_LAN2_ip}  %{bmc_password_1}  lan set 2 netmask 255.255.255.0
Ip setting port1_dhcp
    Step  1  run ipmi cmd  %{bmc_username_1}  ${bmc_ipv4_ip_lan2}   %{bmc_password_1}  lan set 1 ipsrc dhcp
    Sleep  15
#    Step  2  run ipmi cmd  %{bmc_username_1}  ${bmc_ipv4_ip_lan2}  %{bmc_password_1}  raw 6 2  end=True
#    Sleep  180
#    Step  3  run ipmi cmd  %{bmc_username_1}  ${bmc_ipv4_ip_lan2} %{bmc_password_1}  lan set 1 ipsrc dhcp
Ip setting port2_dhcp
    Step  1  ssh_command  %{DUT_username_1}  %{DUT_ipv4_ip_1}  %{DUT_password_1}  ipmitool lan set 2 ipsrc dhcp  end=True
    Sleep  15
#    Step  2  ssh_command  %{DUT_username_1}  %{DUT_ipv4_ip_1}  %{DUT_password_1}  ipmitool raw 6 2  end=True
#    Sleep  180
#    Step  3  ssh_command  %{DUT_username_1}  %{DUT_ipv4_ip_1}  %{DUT_password_1}  ipmitool lan set 2 ipsrc dhcp  end=True


Verify fru_vpd before
    ${fru_output_before1} =  ssh_command  %{DUT_username_1}  %{DUT_ipv4_ip_1}  %{DUT_password_1}  ipmitool fru  end=True

    Set Environment Variable   fru_output_before  ${fru_output_before1}


Verify fru_vpd after
    ${fru_output_after} =  ssh_command  %{DUT_username_1}  %{DUT_ipv4_ip_1}  %{DUT_password_1}  ipmitool fru  end=True

    compare_info_before_and_after_ar   %{fru_output_before}  ${fru_output_after}


Verify fru_vpd_mcinfo before
    ${fru_output_before1} =  ssh_command  %{DUT_username_1}  %{DUT_ipv4_ip_1}  %{DUT_password_1}  ipmitool fru  end=True
    ${mcinfo_output_before1} =  ssh_command  %{DUT_username_1}  %{DUT_ipv4_ip_1}  %{DUT_password_1}  ipmitool mc info  end=True
    Set Environment Variable   fru_output_before  ${fru_output_before1}
    Set Environment Variable   mcinfo_output_before  ${mcinfo_output_before1}

Verify fru_vpd_mcinfo after
    ${fru_output_after} =  ssh_command  %{DUT_username_1}  %{DUT_ipv4_ip_1}  %{DUT_password_1}  ipmitool fru  end=True
    ${mcinfo_output_after} =  ssh_command  %{DUT_username_1}  %{DUT_ipv4_ip_1}  %{DUT_password_1}  ipmitool mc info  end=True
    compare_info_before_and_after_ar  %{fru_output_before}  ${fru_output_after}
    compare_info_before_and_after_ar  %{mcinfo_output_before}  ${mcinfo_output_after}

Verify the SEL and ensure no error
    verify_cmd_output_message_ar  %{bmc_username_1}  %{bmc_ipv4_ip_1}  %{bmc_password_1}  sel list  ${error_messages_sel_list}

Verify the Sensor and ensure no error
    Run Keyword And Continue On Failure  verify_cmd_output_message_ar  %{bmc_username_1}  %{bmc_ipv4_ip_1}  %{bmc_password_1}  sensor list  ${error_messages_sensor_list}

Verify the sensor and check status
    verifythesensorreadingandcheckstatus_ar  %{bmc_username_1}  %{bmc_ipv4_ip_1}  %{bmc_password_1}

Run power control "power reset"
    Step  1  run ipmi cmd  %{bmc_username_1}  %{bmc_ipv4_ip_1}  %{bmc_password_1}  power reset
    Sleep  200
#    ssh_command_exec_ping  %{server_username_1}  %{server_ipv4_ip_1}  %{server_password_1}  %{DUT_ipv4_ip_1}  10

Run power control "power cycle"
    ${openbmc_info} =  call_openbmc_class  ${DeviceName}
    Call Method  ${openbmc_info}  ipmi_power_control  power cycle

run ipmi command "get multi-node info"
    Step  1  check_default_multi_node_info  ${device_info_a}  ${device_info_a}
	
run ipmi command "set_get GPIO State"
# set gpio186 to low no delay
    Step  1  run_ipmi_get_cmd_success_ar  %{bmc_username_1}  %{bmc_ipv4_ip_1}  %{bmc_password_1}  raw 0x3a 0x24 0x01 186 0x0 0x0;ipmitool raw 0x3a 0x24 0x00 186  00   00
# set to high no delay
    Step  2  run_ipmi_get_cmd_success_ar  %{bmc_username_1}  %{bmc_ipv4_ip_1}  %{bmc_password_1}  raw 0x3a 0x24 0x01 186 0x1 0x0;ipmitool raw 0x3a 0x24 0x00 186  01   01
# set to low-high no delay
    Step  3  run_ipmi_get_cmd_success_ar  %{bmc_username_1}  %{bmc_ipv4_ip_1}  %{bmc_password_1}  raw 0x3a 0x24 0x01 186 0x2 0x0;ipmitool raw 0x3a 0x24 0x00 186  00   00
# set to high-low no delay
    Step  4  run_ipmi_get_cmd_success_ar  %{bmc_username_1}  %{bmc_ipv4_ip_1}  %{bmc_password_1}  raw 0x3a 0x24 0x01 186 0x3 0x0;ipmitool raw 0x3a 0x24 0x00 186  01   01

run ipmi command "Set Access CPLD registers"
    Step  1  run_ipmi_get_cmd_success_ar  %{bmc_username_1}  %{bmc_ipv4_ip_1}  %{bmc_password_1}  i2c bus=1 0xC2 0x00 0x30 0x5;ipmitool i2c bus=1 0xC2 0x01  05  05
run ipmi command "Get Access CPLD registers"
    Step  1  run_ipmi_get_cmd_success_ar  %{bmc_username_1}  %{bmc_ipv4_ip_1}  %{bmc_password_1}  i2c bus=1 0xC2 0x00 0x02;ipmitool i2c bus=1 0xC2 0x01  ${CPLD_version_major}  ${CPLD_version_major}
    Step  2  run_ipmi_get_cmd_success_ar  %{bmc_username_1}  %{bmc_ipv4_ip_1}  %{bmc_password_1}  i2c bus=1 0xC2 0x00 0x03;ipmitool i2c bus=1 0xC2 0x01  ${CPLD_version_minor}  ${CPLD_version_minor}

run ipmi command "Set Get LED state offset_30"
    Step  1  verify_led_set_status_ar  %{DUT_username_1}  %{DUT_ipv4_ip_1}  %{DUT_password_1}  0x30
run ipmi command "Set Get LED state offset_31"
    Step  1  verify_led_set_status_ar  %{bmc_username_1}  %{bmc_ipv4_ip_1}  %{bmc_password_1}  0x31
run ipmi command "Set Get LED state offset_32"
    Step  1  verify_led_set_status_ar  %{bmc_username_1}  %{bmc_ipv4_ip_1}  %{bmc_password_1}  0x32
run ipmi command "Set Get LED state offset_33"
    Step  1  verify_led_set_status_ar  %{bmc_username_1}  %{bmc_ipv4_ip_1}  %{bmc_password_1}  0x33
run ipmi command "Set Get LED state offset_34"
    Step  1  verify_led_set_status_ar  %{bmc_username_1}  %{bmc_ipv4_ip_1}  %{bmc_password_1}  0x34
run ipmi command "Set Get LED state offset_35"
    Step  1  verify_led_set_status_ar  %{bmc_username_1}  %{bmc_ipv4_ip_1}  %{bmc_password_1}  0x35
run ipmi command "Set Get LED state offset_36"
    Step  1  verify_led_set_status_ar  %{bmc_username_1}  %{bmc_ipv4_ip_1}  %{bmc_password_1}  0x36
run ipmi command "Set Get LED state offset_37"
    Step  1  verify_led_set_status_ar  %{bmc_username_1}  %{bmc_ipv4_ip_1}  %{bmc_password_1}  0x37

run ipmi command "Set SSD Power State"
    Step  1  verify_ssd_on_off_status_ar  %{bmc_username_1}  %{bmc_ipv4_ip_1}  %{bmc_password_1}  0x17
    Step  2  verify_ssd_on_off_status_ar  %{bmc_username_1}  %{bmc_ipv4_ip_1}  %{bmc_password_1}  0x18
    Step  3  verify_ssd_on_off_status_ar  %{bmc_username_1}  %{bmc_ipv4_ip_1}  %{bmc_password_1}  0x19

run ipmi command "Get-Set BIOS Flash Switch Position to Secondary"
#TODO: issueR4038-384
    Step  1  run ipmi cmd  %{bmc_username_1}  %{bmc_ipv4_ip_1}  %{bmc_password_1}  ${set_BIOS_Flash_Switch_Sec}
    Sleep  1
    Step  1  run ipmi cmd  %{bmc_username_1}  %{bmc_ipv4_ip_1}  %{bmc_password_1}  power off
    Step  2  run ipmi get cmd ar  %{bmc_username_1}  %{bmc_ipv4_ip_1}  %{bmc_password_1}  power status  off
    Step  3  run ipmi cmd  %{bmc_username_1}  %{bmc_ipv4_ip_1}  %{bmc_password_1}  power on
    Sleep   200
    Step  2  run ipmi get cmd ar  %{bmc_username_1}  %{bmc_ipv4_ip_1}  %{bmc_password_1}  power status  on
    Step  3  run ipmi get cmd ar  %{bmc_username_1}  %{bmc_ipv4_ip_1}  %{bmc_password_1}  ${Get_BIOS_Flash_Switch}  01

run ipmi command "Set system GUID to VPD of main board"
    Step  1  run_ipmi_cmd  %{bmc_username_1}  %{bmc_ipv4_ip_1}  %{bmc_password_1}  ${cmd_system_GUID_to_VPD}
    Step  2  run_ipmi_get_cmd_success_ar  %{bmc_username_1}  %{bmc_ipv4_ip_1}  %{bmc_password_1}  mc guid   01010203040506070101020304050607  01010203040506070101020304050607

run ipmi command "Get host POST Code"
    Step  1  run ipmi get cmd ar  %{bmc_username_1}  %{bmc_ipv4_ip_1}  %{bmc_password_1}  ${cmd_Get_host_POST_Code}  ${rsp_Get_host_POST_Code}
	
check ip6 test
    Run Keyword And Continue On Failure  Step  1  verify_ssh_ping6_function_ar   %{bmc_username_1}  %{bmc_ipv4_ip_1}  %{bmc_password_1}
        ...   %{DUT_username_1}  %{DUT_ipv4_ip_1}  %{DUT_password_1}  ip1  40
    Run Keyword And Continue On Failure  Step  2  verify_ssh_ping6_function_ar   %{bmc_username_1}  %{bmc_ipv4_ip_1}  %{bmc_password_1}
        ...   %{DUT_username_1}  %{DUT_ipv4_ip_1}  %{DUT_password_1}  ip2  40
    Run Keyword And Continue On Failure  Step  3  verify_ssh_ping6_function_ar   %{bmc_username_2}  %{bmc_ipv4_ip_2}  %{bmc_password_2}
        ...   %{DUT_username_2}  %{DUT_ipv4_ip_2}  %{DUT_password_2}  ip1  40
    Run Keyword And Continue On Failure  Step  4  verify_ssh_ping6_function_ar   %{bmc_username_2}  %{bmc_ipv4_ip_2}  %{bmc_password_2}
        ...   %{DUT_username_2}  %{DUT_ipv4_ip_2}  %{DUT_password_2}  ip2  40

check Access BMC By USB_Ethernet
    Step  1  ssh_command  %{bmc_username_2}  %{bmc_ipv4_ip_2}  %{bmc_password_2}  ifconfig usb0 10.10.10.56   end=True
    Sleep  3
    Step  2  verify_ssh_ping_function   %{DUT_username_1}  %{DUT_ipv4_ip_1}  %{DUT_password_1}
        ...  10.10.10.56  ping_timeout=${ping_timeout}
    Step  3  ssh_command  %{bmc_username_1}  %{bmc_ipv4_ip_1}  %{bmc_password_1}  ifconfig usb0 10.10.10.55   end=True
    Sleep  3
    Step  4  verify_ssh_ping_function   %{DUT_username_2}  %{DUT_ipv4_ip_2}  %{DUT_password_2}
        ...  10.10.10.55  ping_timeout=${ping_timeout}

set the boot flags apply to next boot
    Step  1  run ipmi cmd  %{DUT_username_1}  %{DUT_ipv4_ip_1}  %{DUT_password_1}  ${set_boot_device}
    Step  2  run ipmi cmd  %{DUT_username_1}  %{DUT_ipv4_ip_1}  %{DUT_password_1}  ${set_boot_device_once}
    Step  3  run ipmi get cmd ar  %{DUT_username_1}  %{DUT_ipv4_ip_1}  %{DUT_password_1}  ${Get_the_boot_1}  ${rsp_the_boot_once_1}
    Step  4  run ipmi get cmd ar  %{DUT_username_1}  %{DUT_ipv4_ip_1}  %{DUT_password_1}  ${Get_the_boot_2}  ${rsp_the_boot_once_2}
    Step  5  enter_and_exit_bios_option_ar  ${DeviceName}  %{DUT_username_1}  %{DUT_ipv4_ip_1}  %{DUT_password_1}
    Step  6  Sleep   200

set the boot flags to be persistent
    Step  1  run ipmi cmd  %{DUT_username_1}  %{DUT_ipv4_ip_1}  %{DUT_password_1}  ${set_boot_device}
    Step  2  run ipmi cmd  %{DUT_username_1}  %{DUT_ipv4_ip_1}  %{DUT_password_1}  ${set_boot_device_persistent}
    Step  3  run ipmi get cmd ar  %{DUT_username_1}  %{DUT_ipv4_ip_1}  %{DUT_password_1}  ${Get_the_boot_1}  ${rsp_the_boot_persistent_1}
    Step  4  run ipmi get cmd ar  %{DUT_username_1}  %{DUT_ipv4_ip_1}  %{DUT_password_1}  ${Get_the_boot_2}  ${rsp_the_boot_persistent_2}
    Step  5  enter_and_exit_bios_option_ar  ${DeviceName}  %{DUT_username_1}  %{DUT_ipv4_ip_1}  %{DUT_password_1}
    Step  6  Sleep   200

set the chassis bootdev bios clear
    Step  1  run ipmi cmd  %{bmc_username_1}  %{bmc_ipv4_ip_1}  %{bmc_password_1}   chassis bootdev bios clear-cmos=yes
    Step  2  enter_and_exit_bios_option_ar  ${DeviceName}  %{DUT_username_1}  %{DUT_ipv4_ip_1}  %{DUT_password_1}
    Step  3  Sleep   240
    Step  4  ssh_command  %{DUT_username_1}  %{DUT_ipv4_ip_1}  %{DUT_password_1}  reboot  end=True
    Step  5  Sleep   300
	
power off_on chassis
    Step  1  run ipmi cmd  %{bmc_username_1}  %{bmc_ipv4_ip_1}  %{bmc_password_1}  power off
    Step  2  Sleep   2
    Step  3  run ipmi cmd  %{bmc_username_1}  %{bmc_ipv4_ip_1}  %{bmc_password_1}  power on
    Step  4  Sleep   200

	
	
Inventory Management
#TODO:Default string need to modified
    Step  1  run ipmi cmd  %{bmc_username_1}  %{bmc_ipv4_ip_1}  %{bmc_password_1}  raw 0x0a 0x10 0x00
    Step  2  verify_openbmc_fru_print_ar  %{bmc_username_1}  %{bmc_ipv4_ip_1}  %{bmc_password_1}  fru print|sed -n '1,21p'  ${fru_print_id0}
    Step  3  verify_openbmc_fru_print_ar  %{bmc_username_1}  %{bmc_ipv4_ip_1}  %{bmc_password_1}  fru print|sed -n '22,43p'  ${fru_print_id1}
    Step  4  verify_openbmc_fru_print_ar  %{bmc_username_1}  %{bmc_ipv4_ip_1}  %{bmc_password_1}  fru print|sed -n '44,65p'  ${fru_print_id2}
    Step  5  verify_openbmc_fru_print_ar  %{bmc_username_1}  %{bmc_ipv4_ip_1}  %{bmc_password_1}  fru print|sed -n '66,87p'  ${fru_print_id3}
    Step  6  verify_openbmc_fru_print_ar  %{bmc_username_1}  %{bmc_ipv4_ip_1}  %{bmc_password_1}  fru print|sed -n '88,109p'  ${fru_print_id4}
    Step  7  verify_openbmc_fru_print_ar  %{bmc_username_1}  %{bmc_ipv4_ip_1}  %{bmc_password_1}  fru print|sed -n '110,131p'  ${fru_print_id5}
    Step  8  verify_openbmc_fru_print_ar  %{bmc_username_1}  %{bmc_ipv4_ip_1}  %{bmc_password_1}  fru print|sed -n '132,139p'  ${fru_print_id6}
    Step  9  verify_openbmc_fru_print_ar  %{bmc_username_1}  %{bmc_ipv4_ip_1}  %{bmc_password_1}  fru print|sed -n '140,147p'  ${fru_print_id7}
    log  Verify the FRU data is match with the data in SMBIOS
    ${chassis_type_outp} =  ssh_command  %{DUT_username_1}  %{DUT_ipv4_ip_1}  %{DUT_password_1}  dmidecode -s chassis-type  end=True
    Should be equal  ${chassis_type_outp}  Main Server Chassis
    ${Product_Manufacturer_outp} =  ssh_command  %{DUT_username_1}  %{DUT_ipv4_ip_1}  %{DUT_password_1}  dmidecode -s system-manufacturer  end=True
    Should be equal  ${Product_Manufacturer_outp}  CELESTICA-CSS
    ${Product_Name_outp} =  ssh_command  %{DUT_username_1}  %{DUT_ipv4_ip_1}  %{DUT_password_1}  dmidecode -s system-product-name  end=True
    Should be equal  ${Product_Name_outp}  Artemis
    ${Product_Serial_Number_outp} =  ssh_command  %{DUT_username_1}  %{DUT_ipv4_ip_1}  %{DUT_password_1}  dmidecode -s system-serial-number  end=True
    Should be equal  ${Product_Serial_Number_outp}  Default string
    ${Product_Asset_Tag_outp} =  ssh_command  %{DUT_username_1}  %{DUT_ipv4_ip_1}  %{DUT_password_1}  dmidecode -s chassis-asset-tag  end=True
    Should be equal  ${Product_Serial_Number_outp}  Default string
    ${Product_Chassis_Version_outp} =  ssh_command  %{DUT_username_1}  %{DUT_ipv4_ip_1}  %{DUT_password_1}  dmidecode -s chassis-version  end=True
    Should be equal  ${Product_Chassis_Version_outp}  Default string
	

check error in curl output
  [Arguments]    ${curl_output}
  ${curl_output_str} =    Convert To String   ${curl_output}
  common_check_patern_2     ${curl_output_str}    ResourceMissingAtURI     Verify the resource is available   expect=False
  common_check_patern_2     ${curl_output_str}    Error     check any error in curl output   expect=False
  common_check_patern_2     ${curl_output_str}    the service was denied access     check the access to the resource   expect=False

Verify JSON Schema
  [Arguments]   ${resource}  ${odata.type_value}  ${Languages}   ${Location}  ${Description}  ${Id}  ${Languages@odata.count}  ${Location@odata.count}  ${Name}  ${Schema}
  ${output_A} =  run_curl_get  ${resource}  %{bmc_ipv4_ip_1}  %{bmc_username_1}  %{bmc_password_1}
  ${output_B} =  run_curl_get  ${resource}  %{bmc_ipv4_ip_2}  %{bmc_username_2}  %{bmc_password_2}
  get_key_value  ${output_A}  @odata.id   ${resource}
  get_key_value  ${output_A}  @odata.type   ${odata.type_value}
  get_key_value  ${output_A}  Description  ${Description}
  get_key_value  ${output_A}  Id   ${Id}
  get_key_value  ${output_A}  Languages  ${Languages}
  get_key_value  ${output_A}  Languages@odata.count   ${Languages@odata.count}
  get_key_value  ${output_A}  Location   ${Location}
  get_key_value  ${output_A}  Location@odata.count   ${Location@odata.count}
  get_key_value  ${output_A}  Name  ${Name}
  get_key_value  ${output_A}  Schema  ${Schema}
  check error in curl output    ${output_A}
  get_key_value  ${output_B}  @odata.id   ${resource}
  get_key_value  ${output_B}  @odata.type   ${odata.type_value}
  get_key_value  ${output_B}  Description  ${Description}
  get_key_value  ${output_B}  Id   ${Id}
  get_key_value  ${output_B}  Languages  ${Languages}
  get_key_value  ${output_B}  Languages@odata.count   ${Languages@odata.count}
  get_key_value  ${output_B}  Location   ${Location}
  get_key_value  ${output_B}  Location@odata.count   ${Location@odata.count}
  get_key_value  ${output_B}  Name  ${Name}
  get_key_value  ${output_B}  Schema  ${Schema}
  check error in curl output    ${output_B}

Check BMC API Call Test
    ${bmc_ipv4_ip} =  get_ip_address_from_ipmitool  DUT  eth_type=dedicated
    Step  1  verify_bmc_api_call_test  DUT  curl -k -d "username=%{bmc_username_1}&password=%{bmc_password_1}" https://${bmc_ipv4_ip}/api/session
    Step  2  verify_bmc_api_call_test  DUT  curl -k -d "username=%{bmc_username_1}&password=%{bmc_password_1}" https://${bmc_ipv4_ip}/api/session123  invalid

Verify service root property
  [Arguments]  ${BMC_IP}  ${BMC_Username}  ${BMC_password}
  ${output} =  run_curl_get  ${resource_service_root}  ${BMC_IP}  ${BMC_Username}  ${BMC_password}
  get_key_value  ${output}  @odata.id
  get_key_value  ${output}  @odata.type
  get_key_value  ${output}  AccountService
  get_key_value  ${output}  Cables
  get_key_value  ${output}  CertificateService
  get_key_value  ${output}  Chassis
  get_key_value  ${output}  EventService
  get_key_value  ${output}  Id
  get_key_value  ${output}  JsonSchemas
  get_key_value  ${output}  Links
  get_key_value  ${output}  Managers
  get_key_value  ${output}  Name
  get_key_value  ${output}  ProtocolFeaturesSupported
  get_key_value  ${output}  RedfishVersion
  get_key_value  ${output}  Registries
  get_key_value  ${output}  SessionService
  get_key_value  ${output}  Systems
  get_key_value  ${output}  Tasks
  get_key_value  ${output}  TelemetryService
  get_key_value  ${output}  UUID
  get_key_value  ${output}  UpdateService
  check error in curl output    ${output}

Verify resource details
  [Arguments]   ${resource}  ${odata.type_value}  ${Description}    ${Members_odata_count}  ${Name}
  ${output_A} =  run_curl_get  ${resource}  %{bmc_ipv4_ip_1}  %{bmc_username_1}  %{bmc_password_1}
  ${output_B} =  run_curl_get  ${resource}  %{bmc_ipv4_ip_2}  %{bmc_username_2}  %{bmc_password_2}
  get_key_value  ${output_A}  @odata.id   ${resource}
  get_key_value  ${output_A}  @odata.type   ${odata.type_value}
  get_key_value  ${output_A}  Description  ${Description}
  get_key_value  ${output_A}  Members@odata.count   ${Members_odata_count}
  get_key_value  ${output_A}  Name  ${Name}
  check error in curl output    ${output_A}
  get_key_value  ${output_B}  @odata.id   ${resource}
  get_key_value  ${output_B}  @odata.type   ${odata.type_value}
  get_key_value  ${output_B}  Description  ${Description}
  get_key_value  ${output_B}  Members@odata.count   ${Members_odata_count}
  get_key_value  ${output_B}  Name  ${Name}
  check error in curl output    ${output_B}

Verify resource collection
  [Arguments]   ${resource}  ${odata.type_value}  ${Members_odata_count}  ${Name}
  ${output_A} =  run_curl_get  ${resource}  %{bmc_ipv4_ip_1}  %{bmc_username_1}  %{bmc_password_1}
  ${output_B} =  run_curl_get  ${resource}  %{bmc_ipv4_ip_2}  %{bmc_username_2}  %{bmc_password_2}
  get_key_value  ${output_A}  @odata.id   ${resource}
  get_key_value  ${output_A}  @odata.type   ${odata.type_value}
  get_key_value  ${output_A}  Members@odata.count   ${Members_odata_count}
  get_key_value  ${output_A}  Name  ${Name}
  check error in curl output    ${output_A}
  get_key_value  ${output_B}  @odata.id   ${resource}
  get_key_value  ${output_B}  @odata.type   ${odata.type_value}
  get_key_value  ${output_B}  Members@odata.count   ${Members_odata_count}
  get_key_value  ${output_B}  Name  ${Name}
  check error in curl output    ${output_B}

verify message registry file details
  [Arguments]   ${resource}  ${Copyright}  ${odata.type_value}  ${Description}   ${Id}  ${Language}   ${Name}  ${OwningEntity}  ${RegistryPrefix}  ${RegistryVersion}  ${Messages}
  ${output_A} =  run_curl_get  ${resource}  %{bmc_ipv4_ip_1}  %{bmc_username_1}  %{bmc_password_1}
  ${output_B} =  run_curl_get  ${resource}  %{bmc_ipv4_ip_2}  %{bmc_username_2}  %{bmc_password_2}
  get_key_value  ${output_A}  @Redfish.Copyright   ${Copyright}
  get_key_value  ${output_A}  @odata.type  ${odata.type_value}
  get_key_value  ${output_A}  Description  ${Description}
  get_key_value  ${output_A}  Id  ${Id}
  get_key_value  ${output_A}  Language  ${Language}
  get_key_value  ${output_A}  Name  ${Name}
  get_key_value  ${output_A}  OwningEntity  ${OwningEntity}
  get_key_value  ${output_A}  RegistryPrefix   ${RegistryPrefix}
  get_key_value  ${output_A}  RegistryVersion  ${RegistryVersion}
  get_key_value  ${output_A}  Messages   ${Messages}
  get_key_value  ${output_B}  @Redfish.Copyright   ${Copyright}
  get_key_value  ${output_B}  @odata.type  ${odata.type_value}
  get_key_value  ${output_B}  Description  ${Description}
  get_key_value  ${output_B}  Id  ${Id}
  get_key_value  ${output_B}  Language  ${Language}
  get_key_value  ${output_B}  Name  ${Name}
  get_key_value  ${output_B}  OwningEntity  ${OwningEntity}
  get_key_value  ${output_B}  RegistryPrefix   ${RegistryPrefix}
  get_key_value  ${output_B}  RegistryVersion  ${RegistryVersion}
  get_key_value  ${output_B}  Messages   ${Messages}

Verify Computer_System_Collection_2 details
  [Arguments]   ${resource}  ${data_type}  ${Actions}  ${Bios}  ${Boot}  ${Description}   ${FabricAdapters}   ${GraphicalConsole}  ${HostWatchdogTimer}  ${Id}  ${Links}  ${LogServices}  ${Memory}  ${MemorySummary}  ${Name}  ${PCIeDevices}  ${PCIeDevices@odata.count}  ${PowerRestorePolicy}  ${PowerState}   ${ProcessorSummary}  ${Processors}  ${SerialConsole}   ${Status}  ${Storage}  ${SystemType}
  ${output_A} =  run_curl_get  ${resource}  %{bmc_ipv4_ip_1}  %{bmc_username_1}  %{bmc_password_1}
  ${output_B} =  run_curl_get  ${resource}  %{bmc_ipv4_ip_2}  %{bmc_username_2}  %{bmc_password_2}
  get_key_value  ${output_A}  @odata.id   ${resource}
  get_key_value  ${output_A}  @odata.type  ${data_type}
  get_key_value  ${output_A}  Actions  ${Actions}
  get_key_value  ${output_A}  Bios  ${Bios}
  get_key_value  ${output_A}  Boot  ${Boot}
  get_key_value  ${output_A}  Description  ${Description}
  get_key_value  ${output_A}  FabricAdapters  ${FabricAdapters}
  get_key_value  ${output_A}  GraphicalConsole  ${GraphicalConsole}
  get_key_value  ${output_A}  HostWatchdogTimer  ${HostWatchdogTimer}
  get_key_value  ${output_A}  Id  ${Id}
  get_key_value  ${output_A}  LastResetTime
  get_key_value  ${output_A}  Links  ${Links}
  get_key_value  ${output_A}  LogServices  ${LogServices}
  get_key_value  ${output_A}  Memory  ${Memory}
  get_key_value  ${output_A}  MemorySummary  ${MemorySummary}
  get_key_value  ${output_A}  Name  ${Name}
  get_key_value  ${output_A}  PCIeDevices  ${PCIeDevices}
  get_key_value  ${output_A}  PCIeDevices@odata.count   ${PCIeDevices@odata.count}
  get_key_value  ${output_A}  PowerRestorePolicy   ${PowerRestorePolicy}
  get_key_value  ${output_A}  PowerState   ${PowerState}
  get_key_value  ${output_A}  ProcessorSummary  ${ProcessorSummary}
  get_key_value  ${output_A}  Processors  ${Processors}
  get_key_value  ${output_A}  SerialConsole  ${SerialConsole}
  get_key_value  ${output_A}  Status  ${Status}
  get_key_value  ${output_A}  Storage  ${Storage}
  get_key_value  ${output_A}  SystemType  ${SystemType}
  check error in curl output    ${output_A}
  get_key_value  ${output_B}  @odata.id   ${resource}
  get_key_value  ${output_B}  @odata.type  ${data_type}
  get_key_value  ${output_B}  Actions  ${Actions}
  get_key_value  ${output_B}  Bios  ${Bios}
  get_key_value  ${output_B}  Boot  ${Boot}
  get_key_value  ${output_B}  Description  ${Description}
  get_key_value  ${output_B}  FabricAdapters  ${FabricAdapters}
  get_key_value  ${output_B}  GraphicalConsole  ${GraphicalConsole}
  get_key_value  ${output_B}  HostWatchdogTimer  ${HostWatchdogTimer}
  get_key_value  ${output_B}  Id  ${Id}
  get_key_value  ${output_B}  LastResetTime
  get_key_value  ${output_B}  Links  ${Links}
  get_key_value  ${output_B}  LogServices  ${LogServices}
  get_key_value  ${output_B}  Memory  ${Memory}
  get_key_value  ${output_B}  MemorySummary  ${MemorySummary}
  get_key_value  ${output_B}  Name  ${Name}
  get_key_value  ${output_B}  PCIeDevices  ${PCIeDevices}
  get_key_value  ${output_B}  PCIeDevices@odata.count   ${PCIeDevices@odata.count}
  get_key_value  ${output_B}  PowerRestorePolicy   ${PowerRestorePolicy}
  get_key_value  ${output_B}  PowerState   ${PowerState}
  get_key_value  ${output_B}  ProcessorSummary  ${ProcessorSummary}
  get_key_value  ${output_B}  Processors  ${Processors}
  get_key_value  ${output_B}  SerialConsole  ${SerialConsole}
  get_key_value  ${output_B}  Status  ${Status}
  get_key_value  ${output_B}  Storage  ${Storage}
  get_key_value  ${output_B}  SystemType  ${SystemType}
  check error in curl output    ${output_B}

Verify Manager_2 details
  [Arguments]   ${resource}  ${odata_type}  ${Id}  ${Name}
  ${output_A} =  run_curl_get  ${resource}  %{bmc_ipv4_ip_1}  %{bmc_username_1}  %{bmc_password_1}
  ${output_B} =  run_curl_get  ${resource}  %{bmc_ipv4_ip_2}  %{bmc_username_2}  %{bmc_password_2}
  get_key_value  ${output_A}  @odata.id   ${resource}
  get_key_value  ${output_A}  @odata.type  ${odata_type}
  get_key_value  ${output_A}  Id  ${Id}
  get_key_value  ${output_A}  Name  ${Name}
  get_key_value  ${output_A}  ServiceRootUptimeSeconds
  check error in curl output    ${output_A}
  get_key_value  ${output_B}  @odata.id   ${resource}
  get_key_value  ${output_B}  @odata.type  ${odata_type}
  get_key_value  ${output_B}  Id  ${Id}
  get_key_value  ${output_B}  Name  ${Name}
  get_key_value  ${output_B}  ServiceRootUptimeSeconds
  check error in curl output    ${output_B}

Verify logservice1 details
  [Arguments]   ${resource}  ${data_type}  ${Actions}  ${Description}  ${Entries}  ${Id}  ${Name}  ${OverWritePolicy}
  ${output_A} =  run_curl_get  ${resource}  %{bmc_ipv4_ip_1}  %{bmc_username_1}  %{bmc_password_1}
  ${output_B} =  run_curl_get  ${resource}  %{bmc_ipv4_ip_2}  %{bmc_username_2}  %{bmc_password_2}
  get_key_value  ${output_A}  @odata.id   ${resource}
  get_key_value  ${output_A}  @odata.type  ${data_type}
  get_key_value  ${output_A}  Actions   ${Actions}
  get_key_value  ${output_A}  DateTime
  get_key_value  ${output_A}  DateTimeLocalOffset
  get_key_value  ${output_A}  Description  ${Description}
  get_key_value  ${output_A}  Entries   ${Entries}
  get_key_value  ${output_A}  Id  ${Id}
  get_key_value  ${output_A}  Name  ${Name}
  get_key_value  ${output_A}  OverWritePolicy   ${OverWritePolicy}
  check error in curl output    ${output_A}
  get_key_value  ${output_B}  @odata.id   ${resource}
  get_key_value  ${output_B}  @odata.type  ${data_type}
  get_key_value  ${output_B}  Actions   ${Actions}
  get_key_value  ${output_B}  DateTime
  get_key_value  ${output_B}  DateTimeLocalOffset
  get_key_value  ${output_B}  Description  ${Description}
  get_key_value  ${output_B}  Entries   ${Entries}
  get_key_value  ${output_B}  Id  ${Id}
  get_key_value  ${output_B}  Name  ${Name}
  get_key_value  ${output_B}  OverWritePolicy   ${OverWritePolicy}
  check error in curl output    ${output_B}

Verify logservice3 details
  [Arguments]   ${resource}  ${data_type}  ${Description}  ${Entries}  ${Id}  ${Name}
  ${output_A} =  run_curl_get  ${resource}  %{bmc_ipv4_ip_1}  %{bmc_username_1}  %{bmc_password_1}
  ${output_B} =  run_curl_get  ${resource}  %{bmc_ipv4_ip_2}  %{bmc_username_2}  %{bmc_password_2}
  get_key_value  ${output_A}  @odata.id   ${resource}
  get_key_value  ${output_A}  @odata.type  ${data_type}
  get_key_value  ${output_A}  Description  ${Description}
  get_key_value  ${output_A}  Entries   ${Entries}
  get_key_value  ${output_A}  Id  ${Id}
  get_key_value  ${output_A}  Name  ${Name}
  check error in curl output    ${output_A}
  get_key_value  ${output_B}  @odata.id   ${resource}
  get_key_value  ${output_B}  @odata.type  ${data_type}
  get_key_value  ${output_B}  Description  ${Description}
  get_key_value  ${output_B}  Entries   ${Entries}
  get_key_value  ${output_B}  Id  ${Id}
  get_key_value  ${output_B}  Name  ${Name}
  check error in curl output    ${output_B}

Verify Manager_4_6 details
  [Arguments]   ${resource}  ${data_type}  ${DHCPv4}  ${DHCPv6}  ${Description}  ${EthernetInterfaceType}  ${FQDN}  ${HostName}  ${Id}  ${InterfaceEnabled}  ${LinkStatus}  ${MTUSize}  ${Name}  ${Status}
  ${output_A} =  run_curl_get  ${resource}  %{bmc_ipv4_ip_1}  %{bmc_username_1}  %{bmc_password_1}
  ${output_B} =  run_curl_get  ${resource}  %{bmc_ipv4_ip_2}  %{bmc_username_2}  %{bmc_password_2}
  get_key_value  ${output_A}  @odata.id   ${resource}
  get_key_value  ${output_A}  @odata.type  ${data_type}
  get_key_value  ${output_A}  DHCPv4   ${DHCPv4}
  get_key_value  ${output_A}  DHCPv6   ${DHCPv6}
  get_key_value  ${output_A}  Description  ${Description}
  get_key_value  ${output_A}  EthernetInterfaceType  ${EthernetInterfaceType}
  get_key_value  ${output_A}  FQDN  ${FQDN}
  get_key_value  ${output_A}  HostName   ${HostName}
  get_key_value  ${output_A}  IPv4Addresses
  get_key_value  ${output_A}  IPv4StaticAddresses
  get_key_value  ${output_A}  IPv6AddressPolicyTable
  get_key_value  ${output_A}  IPv6Addresses
  get_key_value  ${output_A}  IPv6DefaultGateway
  get_key_value  ${output_A}  IPv6StaticAddresses
  get_key_value  ${output_A}  Id  ${Id}
  get_key_value  ${output_A}  InterfaceEnabled  ${InterfaceEnabled}
  get_key_value  ${output_A}  LinkStatus   ${LinkStatus}
  get_key_value  ${output_A}  MACAddress
  get_key_value  ${output_A}  MTUSize   ${MTUSize}
  get_key_value  ${output_A}  Name  ${Name}
  get_key_value  ${output_A}  NameServers
  get_key_value  ${output_A}  SpeedMbps
  get_key_value  ${output_A}  StaticNameServers
  get_key_value  ${output_A}  Status   ${Status}
  check error in curl output    ${output_A}
  get_key_value  ${output_B}  @odata.id   ${resource}
  get_key_value  ${output_B}  @odata.type  ${data_type}
  get_key_value  ${output_B}  DHCPv4   ${DHCPv4}
  get_key_value  ${output_B}  DHCPv6   ${DHCPv6}
  get_key_value  ${output_B}  Description  ${Description}
  get_key_value  ${output_B}  EthernetInterfaceType  ${EthernetInterfaceType}
  get_key_value  ${output_B}  FQDN  ${FQDN}
  get_key_value  ${output_B}  HostName   ${HostName}
  get_key_value  ${output_B}  IPv4Addresses
  get_key_value  ${output_B}  IPv4StaticAddresses
  get_key_value  ${output_B}  IPv6AddressPolicyTable
  get_key_value  ${output_B}  IPv6Addresses
  get_key_value  ${output_B}  IPv6DefaultGateway
  get_key_value  ${output_B}  IPv6StaticAddresses
  get_key_value  ${output_B}  Id  ${Id}
  get_key_value  ${output_B}  InterfaceEnabled  ${InterfaceEnabled}
  get_key_value  ${output_B}  LinkStatus   ${LinkStatus}
  get_key_value  ${output_B}  MACAddress
  get_key_value  ${output_B}  MTUSize   ${MTUSize}
  get_key_value  ${output_B}  Name  ${Name}
  get_key_value  ${output_B}  NameServers
  get_key_value  ${output_B}  SpeedMbps
  get_key_value  ${output_B}  StaticNameServers
  get_key_value  ${output_B}  Status   ${Status}
  check error in curl output    ${output_B}

Verify log details
  [Arguments]   ${resource}  ${odata.type_value}  ${Description}  ${Name}
  ${output_A} =  run_curl_get  ${resource}  %{bmc_ipv4_ip_1}  %{bmc_username_1}  %{bmc_password_1}
  ${output_B} =  run_curl_get  ${resource}  %{bmc_ipv4_ip_2}  %{bmc_username_2}  %{bmc_password_2}
  get_key_value  ${output_A}  @odata.id   ${resource}
  get_key_value  ${output_A}  @odata.type   ${odata.type_value}
  get_key_value  ${output_A}  Description  ${Description}
  get_key_value  ${output_A}  Members
  get_key_value  ${output_A}  Members@odata.count
  get_key_value  ${output_A}  Name  ${Name}
  check error in curl output    ${output_A}
  get_key_value  ${output_B}  @odata.id   ${resource}
  get_key_value  ${output_B}  @odata.type   ${odata.type_value}
  get_key_value  ${output_B}  Description  ${Description}
  get_key_value  ${output_B}  Members
  get_key_value  ${output_B}  Members@odata.count
  get_key_value  ${output_B}  Name  ${Name}
  check error in curl output    ${output_B}

Verify logservice8 details
  [Arguments]   ${resource}  ${odata.type_value}  ${Description}  ${nextLink}  ${Name}
  ${output_A} =  run_curl_get  ${resource}  %{bmc_ipv4_ip_1}  %{bmc_username_1}  %{bmc_password_1}
  ${output_B} =  run_curl_get  ${resource}  %{bmc_ipv4_ip_2}  %{bmc_username_2}  %{bmc_password_2}
  get_key_value  ${output_A}  @odata.id   ${resource}
  get_key_value  ${output_A}  @odata.type   ${odata.type_value}
  get_key_value  ${output_A}  Description  ${Description}
  get_key_value  ${output_A}  Members
  get_key_value  ${output_A}  Members@odata.count
  get_key_value  ${output_A}  Members@odata.nextLink    ${nextLink}
  get_key_value  ${output_A}  Name  ${Name}
  get_key_value  ${output_B}  @odata.id   ${resource}
  get_key_value  ${output_B}  @odata.type   ${odata.type_value}
  get_key_value  ${output_B}  Description  ${Description}
  get_key_value  ${output_B}  Members
  get_key_value  ${output_B}  Members@odata.count
  get_key_value  ${output_B}  Members@odata.nextLink    ${nextLink}
  get_key_value  ${output_B}  Name  ${Name}

verify computersystem5 details
  [Arguments]  ${resource}  ${data_type}  ${Id}  ${Name}  ${Parameters}
  ${output_A} =  run_curl_get  ${resource}  %{bmc_ipv4_ip_1}  %{bmc_username_1}  %{bmc_password_1}
  ${output_B} =  run_curl_get  ${resource}  %{bmc_ipv4_ip_2}  %{bmc_username_2}  %{bmc_password_2}
  get_key_value  ${output_A}  @odata.id   ${resource}
  get_key_value  ${output_A}  @odata.type   ${data_type}
  get_key_value  ${output_A}  Name   ${Name}
  get_key_value  ${output_A}  Id   ${Id}
  get_key_value  ${output_A}  Parameters   ${Parameters}
  check error in curl output    ${output_A}
  get_key_value  ${output_B}  @odata.id   ${resource}
  get_key_value  ${output_B}  @odata.type   ${data_type}
  get_key_value  ${output_B}  Name   ${Name}
  get_key_value  ${output_B}  Id   ${Id}
  get_key_value  ${output_B}  Parameters   ${Parameters}
  check error in curl output    ${output_B}

verify TelemetryService
  [Arguments]   ${resource}  ${data_type}  ${Id}  ${MaxReports}  ${MetricReportDefinitions}   ${MetricReports}   ${MinCollectionInterval}   ${Name}  ${Status}    ${SupportedCollectionFunctions}  ${Triggers}
  ${output_A} =  run_curl_get  ${resource}  %{bmc_ipv4_ip_1}  %{bmc_username_1}  %{bmc_password_1}
  ${output_B} =  run_curl_get  ${resource}  %{bmc_ipv4_ip_2}  %{bmc_username_2}  %{bmc_password_2}
  get_key_value  ${output_A}  @odata.id   ${resource}
  get_key_value  ${output_A}  @odata.type   ${data_type}
  get_key_value  ${output_A}  Name   ${Name}
  get_key_value  ${output_A}  Id   ${Id}
  get_key_value  ${output_A}  MaxReports  ${MaxReports}
  get_key_value  ${output_A}  MetricReportDefinitions  ${MetricReportDefinitions}
  get_key_value  ${output_A}  MetricReports   ${MetricReports}
  get_key_value  ${output_A}  MinCollectionInterval   ${MinCollectionInterval}
  get_key_value  ${output_A}  Status    ${Status}
  get_key_value  ${output_A}  SupportedCollectionFunctions   ${SupportedCollectionFunctions}
  get_key_value  ${output_A}  Triggers   ${Triggers}
  check error in curl output    ${output_A}
  get_key_value  ${output_B}  @odata.id   ${resource}
  get_key_value  ${output_B}  @odata.type   ${data_type}
  get_key_value  ${output_B}  Name   ${Name}
  get_key_value  ${output_B}  Id   ${Id}
  get_key_value  ${output_B}  MaxReports  ${MaxReports}
  get_key_value  ${output_B}  MetricReportDefinitions  ${MetricReportDefinitions}
  get_key_value  ${output_B}  MetricReports   ${MetricReports}
  get_key_value  ${output_B}  MinCollectionInterval   ${MinCollectionInterval}
  get_key_value  ${output_B}  Status    ${Status}
  get_key_value  ${output_B}  SupportedCollectionFunctions   ${SupportedCollectionFunctions}
  get_key_value  ${output_B}  Triggers   ${Triggers}
  check error in curl output    ${output_B}


verify Chassis-1 details
  [Arguments]   ${resource}  ${data_type}  ${Actions}  ${ChassisType}  ${Id}   ${Links}   ${Manufacturer}   ${Name}  ${Model}    ${PCIeDevices}  ${PartNumber}  ${Power}  ${PowerState}  ${Sensors}    ${SerialNumber}  ${Status}  ${Thermal}
  ${output_A} =  run_curl_get  ${resource}  %{bmc_ipv4_ip_1}  %{bmc_username_1}  %{bmc_password_1}
  ${output_B} =  run_curl_get  ${resource}  %{bmc_ipv4_ip_2}  %{bmc_username_2}  %{bmc_password_2}
  get_key_value  ${output_A}  @odata.id   ${resource}
  get_key_value  ${output_A}  @odata.type   ${data_type}
  get_key_value  ${output_A}  Name   ${Name}
  get_key_value  ${output_A}  Actions  ${Actions}
  get_key_value  ${output_A}  ChassisType  ${ChassisType}
  get_key_value  ${output_A}  Id  ${Id}
  get_key_value  ${output_A}  Links  ${Links}
  get_key_value  ${output_A}  Manufacturer  ${Manufacturer}
  get_key_value  ${output_A}  Model  ${Model}
  get_key_value  ${output_A}  PCIeDevices  ${PCIeDevices}
  get_key_value  ${output_A}  PartNumber  ${PartNumber}
  get_key_value  ${output_A}  Power  ${Power}
  get_key_value  ${output_A}  PowerState   ${PowerState}
  get_key_value  ${output_A}  Sensors   ${Sensors}
  get_key_value  ${output_A}  SerialNumber  ${SerialNumber}
  get_key_value  ${output_A}  Status   ${Status}
  get_key_value  ${output_A}  Thermal  ${Thermal}
  check error in curl output    ${output_A}
  get_key_value  ${output_A}  @odata.id   ${resource}
  get_key_value  ${output_A}  @odata.type   ${data_type}
  get_key_value  ${output_A}  Name   ${Name}
  get_key_value  ${output_A}  Actions  ${Actions}
  get_key_value  ${output_A}  ChassisType  ${ChassisType}
  get_key_value  ${output_A}  Id  ${Id}
  get_key_value  ${output_A}  Links  ${Links}
  get_key_value  ${output_A}  Manufacturer  ${Manufacturer}
  get_key_value  ${output_A}  Model  ${Model}
  get_key_value  ${output_A}  PCIeDevices  ${PCIeDevices}
  get_key_value  ${output_A}  PartNumber  ${PartNumber}
  get_key_value  ${output_A}  Power  ${Power}
  get_key_value  ${output_A}  PowerState   ${PowerState}
  get_key_value  ${output_A}  Sensors   ${Sensors}
  get_key_value  ${output_A}  SerialNumber  ${SerialNumber}
  get_key_value  ${output_A}  Status   ${Status}
  get_key_value  ${output_B}  Thermal  ${Thermal}
  check error in curl output    ${output_B}

verify sensor_manageraccount collection
  [Arguments]   ${resource}  ${data_type}  ${Description}   ${Members}  ${Members@odata_count}  ${Name}
  ${output_A} =  run_curl_get  ${resource}  %{bmc_ipv4_ip_1}  %{bmc_username_1}  %{bmc_password_1}
  ${output_B} =  run_curl_get  ${resource}  %{bmc_ipv4_ip_2}  %{bmc_username_2}  %{bmc_password_2}
  get_key_value  ${output_A}  @odata.id   ${resource}
  get_key_value  ${output_A}  @odata.type   ${data_type}
  get_key_value  ${output_A}  Description  ${Description}
  get_key_value  ${output_A}  Members   ${Members}
  get_key_value  ${output_A}  Members@odata.count   ${Members@odata_count}
  get_key_value  ${output_A}  Name  ${Name}
  check error in curl output    ${output_A}
  get_key_value  ${output_B}  @odata.id   ${resource}
  get_key_value  ${output_B}  @odata.type   ${data_type}
  get_key_value  ${output_B}  Description  ${Description}
  get_key_value  ${output_B}  Members  ${Members}
  get_key_value  ${output_B}  Members@odata.count   ${Members@odata_count}
  get_key_value  ${output_B}  Name  ${Name}
  check error in curl output    ${output_B}

verify sensor details
  [Arguments]   ${resource}  ${data_type}  ${Id}  ${Name}  ${ReadingRangeMax}   ${ReadingRangeMin}  ${ReadingType}  ${ReadingUnits}   ${Status}
  ${output_A} =  run_curl_get  ${resource}  %{bmc_ipv4_ip_1}  %{bmc_username_1}  %{bmc_password_1}
  ${output_B} =  run_curl_get  ${resource}  %{bmc_ipv4_ip_2}  %{bmc_username_2}  %{bmc_password_2}
  get_key_value  ${output_A}  @odata.id   ${resource}
  get_key_value  ${output_A}  @odata.type   ${data_type}
  get_key_value  ${output_A}  Id  ${Id}
  get_key_value  ${output_A}  Name  ${Name}
  get_key_value  ${output_A}  Reading
  get_key_value  ${output_A}  ReadingRangeMax   ${ReadingRangeMax}
  get_key_value  ${output_A}  ReadingRangeMin   ${ReadingRangeMin}
  get_key_value  ${output_A}  ReadingType   ${ReadingType}
  get_key_value  ${output_A}  ReadingUnits    ${ReadingUnits}
  get_key_value  ${output_A}  Status   ${Status}
  check error in curl output    ${output_A}
  get_key_value  ${output_B}  @odata.id   ${resource}
  get_key_value  ${output_B}  @odata.type   ${data_type}
  get_key_value  ${output_B}  Id  ${Id}
  get_key_value  ${output_B}  Name  ${Name}
  get_key_value  ${output_B}  Reading
  get_key_value  ${output_B}  ReadingRangeMax   ${ReadingRangeMax}
  get_key_value  ${output_B}  ReadingRangeMin   ${ReadingRangeMin}
  get_key_value  ${output_B}  ReadingType   ${ReadingType}
  get_key_value  ${output_B}  ReadingUnits    ${ReadingUnits}
  get_key_value  ${output_B}  Status   ${Status}
  check error in curl output    ${output_B}

verify sensor psu details
  [Arguments]   ${resource}  ${data_type}  ${Id}  ${Name}  ${ReadingRangeMax}   ${ReadingRangeMin}  ${ReadingType}  ${ReadingUnits}   ${Status}  ${threshold}
  ${output_A} =  run_curl_get  ${resource}  %{bmc_ipv4_ip_1}  %{bmc_username_1}  %{bmc_password_1}
  ${output_B} =  run_curl_get  ${resource}  %{bmc_ipv4_ip_2}  %{bmc_username_2}  %{bmc_password_2}
  get_key_value  ${output_A}  @odata.id   ${resource}
  get_key_value  ${output_A}  @odata.type   ${data_type}
  get_key_value  ${output_A}  Id  ${Id}
  get_key_value  ${output_A}  Name  ${Name}
  get_key_value  ${output_A}  Reading
  get_key_value  ${output_A}  ReadingRangeMax   ${ReadingRangeMax}
  get_key_value  ${output_A}  ReadingRangeMin   ${ReadingRangeMin}
  get_key_value  ${output_A}  ReadingType   ${ReadingType}
  get_key_value  ${output_A}  ReadingUnits    ${ReadingUnits}
  get_key_value  ${output_A}  Status   ${Status}
  get_key_value  ${output_A}  Thresholds   ${threshold}
  check error in curl output    ${output_A}
  get_key_value  ${output_B}  @odata.id   ${resource}
  get_key_value  ${output_B}  @odata.type   ${data_type}
  get_key_value  ${output_B}  Id  ${Id}
  get_key_value  ${output_B}  Name  ${Name}
  get_key_value  ${output_B}  Reading
  get_key_value  ${output_B}  ReadingRangeMax   ${ReadingRangeMax}
  get_key_value  ${output_B}  ReadingRangeMin   ${ReadingRangeMin}
  get_key_value  ${output_B}  ReadingType   ${ReadingType}
  get_key_value  ${output_B}  ReadingUnits    ${ReadingUnits}
  get_key_value  ${output_B}  Status   ${Status}
  get_key_value  ${output_B}  Thresholds   ${threshold}
  check error in curl output    ${output_B}

Verify computer collection1
  [Arguments]   ${resource}  ${odata.type_value}  ${Members}    ${Members_odata_count}  ${Name}
  ${output_A} =  run_curl_get  ${resource}  %{bmc_ipv4_ip_1}  %{bmc_username_1}  %{bmc_password_1}
  ${output_B} =  run_curl_get  ${resource}  %{bmc_ipv4_ip_2}  %{bmc_username_2}  %{bmc_password_2}
  get_key_value  ${output_A}  @odata.id   ${resource}
  get_key_value  ${output_A}  @odata.type   ${odata.type_value}
  get_key_value  ${output_A}  Members  ${Members}
  get_key_value  ${output_A}  Members@odata.count   ${Members_odata_count}
  get_key_value  ${output_A}  Name  ${Name}
  check error in curl output    ${output_A}
  get_key_value  ${output_B}  @odata.id   ${resource}
  get_key_value  ${output_B}  @odata.type   ${odata.type_value}
  get_key_value  ${output_B}  Members  ${Members}
  get_key_value  ${output_B}  Members@odata.count   ${Members_odata_count}
  get_key_value  ${output_B}  Name  ${Name}
  check error in curl output    ${output_B}

Verify computer System-2
  [Arguments]   ${resource}  ${odata.type_value}  ${Actions}    ${Description}  ${ID}   ${Links}  ${Name}
  ${output_A} =  run_curl_get  ${resource}  %{bmc_ipv4_ip_1}  %{bmc_username_1}  %{bmc_password_1}
  ${output_B} =  run_curl_get  ${resource}  %{bmc_ipv4_ip_2}  %{bmc_username_2}  %{bmc_password_2}
  get_key_value  ${output_A}  @odata.id   ${resource}
  get_key_value  ${output_A}  @odata.type   ${odata.type_value}
  get_key_value  ${output_A}  Actions  ${Actions}
  get_key_value  ${output_A}  Description   ${Description}
  get_key_value  ${output_A}  Links      ${Links}
  get_key_value  ${output_A}  Name  ${Name}
  check error in curl output    ${output_A}
  get_key_value  ${output_B}  @odata.id   ${resource}
  get_key_value  ${output_B}  @odata.type   ${odata.type_value}
  get_key_value  ${output_B}   Actions  ${Actions}
  get_key_value  ${output_B}  Description   ${Description}
  get_key_value  ${output_A}  Links      ${Links}
  get_key_value  ${output_B}  Name  ${Name}
  check error in curl output    ${output_B}

Verify manager-3
  [Arguments]   ${resource}  ${odata.type_value}  ${Description}    ${Members}  ${Mem_data_count}  ${Name}
  ${output_A} =  run_curl_get  ${resource}  %{bmc_ipv4_ip_1}  %{bmc_username_1}  %{bmc_password_1}
  ${output_B} =  run_curl_get  ${resource}  %{bmc_ipv4_ip_2}  %{bmc_username_2}  %{bmc_password_2}
  get_key_value  ${output_A}  @odata.id   ${resource}
  get_key_value  ${output_A}  @odata.type   ${odata.type_value}
  get_key_value  ${output_A}  Description   ${Description}
  get_key_value  ${output_A}  Members      ${Members}
  get_key_value  ${output_A}  Members@odata.count   ${Mem_data_count}
  get_key_value  ${output_A}  Name  ${Name}
  check error in curl output    ${output_A}
  get_key_value  ${output_B}  @odata.id   ${resource}
  get_key_value  ${output_B}  @odata.type   ${odata.type_value}
  get_key_value  ${output_B}  Description   ${Description}
  get_key_value  ${output_B}  Members      ${Members}
  get_key_value  ${output_B}  Members@odata.count   ${Mem_data_count}
  get_key_value  ${output_B}  Name  ${Name}
  check error in curl output    ${output_B}

Verify Session Collection-1
  [Arguments]   ${resource}  ${odata.type_value}  ${Description}    ${ID}  ${name}  ${serviceenabled}    ${sessiontimeout}   ${sessions}
  ${output_A} =  run_curl_get  ${resource}  %{bmc_ipv4_ip_1}  %{bmc_username_1}  %{bmc_password_1}
  ${output_B} =  run_curl_get  ${resource}  %{bmc_ipv4_ip_2}  %{bmc_username_2}  %{bmc_password_2}
  get_key_value  ${output_A}  @odata.id   ${resource}
  get_key_value  ${output_A}  @odata.type   ${odata.type_value}
  get_key_value  ${output_A}  Description   ${Description}
  get_key_value  ${output_A}  Id          ${ID}
  get_key_value  ${output_A}  Name        ${name}
  get_key_value  ${output_A}  ServiceEnabled    ${serviceenabled}
  get_key_value  ${output_A}  SessionTimeout    ${sessiontimeout}
  get_key_value  ${output_A}  Sessions     ${sessions}
  check error in curl output    ${output_A}
  get_key_value  ${output_B}  @odata.id   ${resource}
  get_key_value  ${output_B}  @odata.type   ${odata.type_value}
  get_key_value  ${output_B}  Description   ${Description}
  get_key_value  ${output_B}  Id          ${ID}
  get_key_value  ${output_B}  Name        ${name}
  get_key_value  ${output_B}  ServiceEnabled    ${serviceenabled}
  get_key_value  ${output_B}  SessionTimeout    ${sessiontimeout}
  get_key_value  ${output_B}  Sessions     ${sessions}
  check error in curl output    ${output_B}

Verify Message Registry File-1
  [Arguments]   ${resource}  ${odata.type_value}  ${Description}    ${ID}  ${Language}  ${Language_count}    ${Location}   ${Location_count}  ${name}  ${Registry}
  ${output_A} =  run_curl_get  ${resource}  %{bmc_ipv4_ip_1}  %{bmc_username_1}  %{bmc_password_1}
  ${output_B} =  run_curl_get  ${resource}  %{bmc_ipv4_ip_2}  %{bmc_username_2}  %{bmc_password_2}
  get_key_value  ${output_A}  @odata.id   ${resource}
  get_key_value  ${output_A}  @odata.type   ${odata.type_value}
  get_key_value  ${output_A}  Description   ${Description}
  get_key_value  ${output_A}  Id          ${ID}
  get_key_value  ${output_A}  Languages    ${Language}
  get_key_value  ${output_A}  Languages@odata.count    ${Language_count}
  get_key_value  ${output_A}  Location     ${Location}
  get_key_value  ${output_A}  Location@odata.count    ${Location_count}
  get_key_value  ${output_A}  Name   ${name}
  get_key_value  ${output_A}  Registry   ${Registry}
  check error in curl output    ${output_A}
  get_key_value  ${output_B}  @odata.id   ${resource}
  get_key_value  ${output_B}  @odata.type   ${odata.type_value}
  get_key_value  ${output_B}  Description   ${Description}
  get_key_value  ${output_B}  Id          ${ID}
  get_key_value  ${output_B}  Languages    ${Language}
  get_key_value  ${output_B}  Languages@odata.count    ${Language_count}
  get_key_value  ${output_B}  Location     ${Location}
  get_key_value  ${output_B}  Location@odata.count    ${Location_count}
  get_key_value  ${output_B}  Name   ${name}
  get_key_value  ${output_B}  Registry   ${Registry}
  check error in curl output    ${output_B}

Verify ManagerAccount
  [Arguments]   ${resource}  ${odata.type_value}  ${AccountTypes}  ${Description}  ${Enabled}  ${ID}  ${Links}   ${Locked}   ${Locked_Redfish_AllowableValues}  ${Name}    ${PasswordChangeRequired}   ${RoleID}   ${StrictAccountTypes}  ${Username}
  ${output_A} =  run_curl_get  ${resource}  %{bmc_ipv4_ip_1}  %{bmc_username_1}  %{bmc_password_1}
  ${output_B} =  run_curl_get  ${resource}  %{bmc_ipv4_ip_2}  %{bmc_username_2}  %{bmc_password_2}
  get_key_value  ${output_A}  @odata.id   ${resource}
  get_key_value  ${output_A}  @odata.type   ${odata.type_value}
  get_key_value  ${output_A}  AccountTypes   ${AccountTypes}
  get_key_value  ${output_A}  Description   ${Description}
  get_key_value  ${output_A}  Enabled    ${Enabled}
  get_key_value  ${output_A}  Id          ${ID}
  get_key_value  ${output_A}  Links     ${Links}
  get_key_value  ${output_A}  Locked    ${Locked}
  get_key_value  ${output_A}  Locked@Redfish.AllowableValues    ${Locked_Redfish_AllowableValues}
  get_key_value  ${output_A}  Name     ${Name}
  get_key_value  ${output_A}  PasswordChangeRequired   ${PasswordChangeRequired}
  get_key_value  ${output_A}  RoleId   ${RoleID}
  get_key_value  ${output_A}  StrictAccountTypes   ${StrictAccountTypes}
  get_key_value  ${output_A}  UserName    ${Username}
  check error in curl output    ${output_A}
  get_key_value  ${output_B}  @odata.id   ${resource}
  get_key_value  ${output_B}  @odata.type   ${odata.type_value}
  get_key_value  ${output_B}  AccountTypes   ${AccountTypes}
  get_key_value  ${output_B}  Description   ${Description}
  get_key_value  ${output_B}  Enabled    ${Enabled}
  get_key_value  ${output_B}  Id          ${ID}
  get_key_value  ${output_B}  Links     ${Links}
  get_key_value  ${output_B}  Locked    ${Locked}
  get_key_value  ${output_B}  Locked@Redfish.AllowableValues    ${Locked_Redfish_AllowableValues}
  get_key_value  ${output_B}  Name     ${Name}
  get_key_value  ${output_B}  PasswordChangeRequired   ${PasswordChangeRequired}
  get_key_value  ${output_B}  RoleId   ${RoleID}
  get_key_value  ${output_B}  StrictAccountTypes   ${StrictAccountTypes}
  get_key_value  ${output_B}  UserName    ${Username}
  check error in curl output    ${output_B}

Verify Role-1
  [Arguments]   ${resource}  ${odata.type_value}   ${AssignedPrivileges}  ${Description}  ${Id}  ${IsPredefined}  ${Name}  ${OemPrivileges}   ${RoleId}
  ${output_A} =  run_curl_get  ${resource}  %{bmc_ipv4_ip_1}  %{bmc_username_1}  %{bmc_password_1}
  ${output_B} =  run_curl_get  ${resource}  %{bmc_ipv4_ip_2}  %{bmc_username_2}  %{bmc_password_2}
  get_key_value  ${output_A}  @odata.id   ${resource}
  get_key_value  ${output_A}  @odata.type   ${odata.type_value}
  get_key_value  ${output_A}  AssignedPrivileges   ${AssignedPrivileges}
  get_key_value  ${output_A}  Description    ${Description}
  get_key_value  ${output_A}  Id   ${Id}
  get_key_value  ${output_A}  IsPredefined   ${IsPredefined}
  get_key_value  ${output_A}  Name    ${Name}
  get_key_value  ${output_A}  OemPrivileges    ${OemPrivileges}
  get_key_value  ${output_A}  RoleId   ${RoleId}
  check error in curl output    ${output_A}
  get_key_value  ${output_B}  @odata.id   ${resource}
  get_key_value  ${output_B}  @odata.type   ${odata.type_value}
  get_key_value  ${output_B}  AssignedPrivileges   ${AssignedPrivileges}
  get_key_value  ${output_B}  Description    ${Description}
  get_key_value  ${output_B}  Id   ${Id}
  get_key_value  ${output_B}  IsPredefined   ${IsPredefined}
  get_key_value  ${output_B}  Name    ${Name}
  get_key_value  ${output_B}  OemPrivileges    ${OemPrivileges}
  get_key_value  ${output_B}  RoleId   ${RoleId}
  check error in curl output    ${output_B}

Verify Chassis-3
  [Arguments]   ${resource}  ${odata.type_value}   ${Id}   ${Name}   ${Parameters}
  ${output_A} =  run_curl_get  ${resource}  %{bmc_ipv4_ip_1}  %{bmc_username_1}  %{bmc_password_1}
  ${output_B} =  run_curl_get  ${resource}  %{bmc_ipv4_ip_2}  %{bmc_username_2}  %{bmc_password_2}
  get_key_value  ${output_A}  @odata.id   ${resource}
  get_key_value  ${output_A}  @odata.type   ${odata.type_value}
  get_key_value  ${output_A}  Id   ${Id}
  get_key_value  ${output_A}  Name    ${Name}
  get_key_value  ${output_A}  Parameters   ${Parameters}
  check error in curl output    ${output_A}
  get_key_value  ${output_B}  @odata.id   ${resource}
  get_key_value  ${output_B}  @odata.type   ${odata.type_value}
  get_key_value  ${output_B}  Id   ${Id}
  get_key_value  ${output_B}  Name    ${Name}
  get_key_value  ${output_B}  Parameters   ${Parameters}
  check error in curl output    ${output_B}

Verify Sensor-11
  [Arguments]   ${resource}  ${odata.type_value}  ${Id}  ${Name}   ${ReadingRangeMax}   ${ReadingRangeMin}   ${ReadingType}  ${ReadingUnits}  ${Status}
  ${output_A} =  run_curl_get  ${resource}  %{bmc_ipv4_ip_1}  %{bmc_username_1}  %{bmc_password_1}
  ${output_B} =  run_curl_get  ${resource}  %{bmc_ipv4_ip_2}  %{bmc_username_2}  %{bmc_password_2}
  get_key_value  ${output_A}  @odata.id   ${resource}
  get_key_value  ${output_A}  @odata.type   ${odata.type_value}
  get_key_value  ${output_A}  Id   ${Id}
  get_key_value  ${output_A}  Name    ${Name}
  get_key_value  ${output_A}  Reading
  get_key_value  ${output_A}  ReadingRangeMax  ${ReadingRangeMax}
  get_key_value  ${output_A}  ReadingRangeMin  ${ReadingRangeMin}
  get_key_value  ${output_A}  ReadingType   ${ReadingType}
  get_key_value  ${output_A}  ReadingUnits   ${ReadingUnits}
  get_key_value  ${output_A}  Status  ${Status}
  get_key_value  ${output_A}  Thresholds
  check error in curl output    ${output_A}
  get_key_value  ${output_B}  @odata.id   ${resource}
  get_key_value  ${output_B}  @odata.type   ${odata.type_value}
  get_key_value  ${output_B}  Id   ${Id}
  get_key_value  ${output_B}  Name    ${Name}
  get_key_value  ${output_B}  Reading
  get_key_value  ${output_B}  ReadingRangeMax  ${ReadingRangeMax}
  get_key_value  ${output_B}  ReadingRangeMin  ${ReadingRangeMin}
  get_key_value  ${output_B}  ReadingType   ${ReadingType}
  get_key_value  ${output_B}  ReadingUnits   ${ReadingUnits}
  get_key_value  ${output_B}  Status  ${Status}
  get_key_value  ${output_B}  Thresholds
  check error in curl output    ${output_B}

Verify Sensor-3
  [Arguments]   ${resource}  ${odata.type_value}  ${Id}  ${Name}   ${ReadingRangeMax}   ${ReadingRangeMin}   ${ReadingType}  ${ReadingUnits}  ${Status}
  ${output_A} =  run_curl_get  ${resource}  %{bmc_ipv4_ip_1}  %{bmc_username_1}  %{bmc_password_1}
  ${output_B} =  run_curl_get  ${resource}  %{bmc_ipv4_ip_2}  %{bmc_username_2}  %{bmc_password_2}
  get_key_value  ${output_A}  @odata.id   ${resource}
  get_key_value  ${output_A}  @odata.type   ${odata.type_value}
  get_key_value  ${output_A}  Id   ${Id}
  get_key_value  ${output_A}  Name    ${Name}
  get_key_value  ${output_A}  ReadingRangeMax  ${ReadingRangeMax}
  get_key_value  ${output_A}  ReadingRangeMin  ${ReadingRangeMin}
  get_key_value  ${output_A}  ReadingType   ${ReadingType}
  get_key_value  ${output_A}  ReadingUnits   ${ReadingUnits}
  get_key_value  ${output_A}  Status  ${Status}
  check error in curl output    ${output_A}
  get_key_value  ${output_B}  @odata.id   ${resource}
  get_key_value  ${output_B}  @odata.type   ${odata.type_value}
  get_key_value  ${output_B}  Id   ${Id}
  get_key_value  ${output_B}  Name    ${Name}
  get_key_value  ${output_B}  ReadingRangeMax  ${ReadingRangeMax}
  get_key_value  ${output_B}  ReadingRangeMin  ${ReadingRangeMin}
  get_key_value  ${output_B}  ReadingType   ${ReadingType}
  get_key_value  ${output_B}  ReadingUnits   ${ReadingUnits}
  get_key_value  ${output_B}  Status  ${Status}
  check error in curl output    ${output_B}

Verify UpdateService-1
  [Arguments]   ${resource}  ${odata.type_value}  ${Description}  ${FirmwareInventory}   ${HttpPushUri}   ${HttpPushUriOptions}  ${Id}  ${MaxImageSizeBytes}   ${MultipartHttpPushUri}   ${Name}   ${ServiceEnabled}
  ${output_A} =  run_curl_get  ${resource}  %{bmc_ipv4_ip_1}  %{bmc_username_1}  %{bmc_password_1}
  ${output_B} =  run_curl_get  ${resource}  %{bmc_ipv4_ip_2}  %{bmc_username_2}  %{bmc_password_2}
  get_key_value  ${output_A}  @odata.id   ${resource}
  get_key_value  ${output_A}  @odata.type   ${odata.type_value}
  get_key_value  ${output_A}  Description   ${Description}
  get_key_value  ${output_A}  FirmwareInventory    ${FirmwareInventory}
  get_key_value  ${output_A}  HttpPushUri    ${HttpPushUri}
  get_key_value  ${output_A}  HttpPushUriOptions    ${HttpPushUriOptions}
  get_key_value  ${output_A}  Id   ${Id}
  get_key_value  ${output_A}  MaxImageSizeBytes   ${MaxImageSizeBytes}
  get_key_value  ${output_A}  MultipartHttpPushUri   ${MultipartHttpPushUri}
  get_key_value  ${output_A}  Name    ${Name}
  get_key_value  ${output_A}  ServiceEnabled    ${ServiceEnabled}
  check error in curl output    ${output_A}
  get_key_value  ${output_B}  @odata.id   ${resource}
  get_key_value  ${output_B}  @odata.type   ${odata.type_value}
  get_key_value  ${output_B}  Description   ${Description}
  get_key_value  ${output_B}  FirmwareInventory    ${FirmwareInventory}
  get_key_value  ${output_B}  HttpPushUri    ${HttpPushUri}
  get_key_value  ${output_B}  HttpPushUriOptions    ${HttpPushUriOptions}
  get_key_value  ${output_B}  Id   ${Id}
  get_key_value  ${output_B}  MaxImageSizeBytes   ${MaxImageSizeBytes}
  get_key_value  ${output_B}  MultipartHttpPushUri   ${MultipartHttpPushUri}
  get_key_value  ${output_B}  Name    ${Name}
  get_key_value  ${output_B}  ServiceEnabled    ${ServiceEnabled}
  check error in curl output    ${output_B}

Verify Log Service-5
  [Arguments]   ${resource}  ${odata.type_value}  ${Actions}  ${Description}   ${Entries}   ${Id}  ${Name}  ${OverWritePolicy}
  ${output_A} =  run_curl_get  ${resource}  %{bmc_ipv4_ip_1}  %{bmc_username_1}  %{bmc_password_1}
  ${output_B} =  run_curl_get  ${resource}  %{bmc_ipv4_ip_2}  %{bmc_username_2}  %{bmc_password_2}
  get_key_value  ${output_A}  @odata.id   ${resource}
  get_key_value  ${output_A}  @odata.type   ${odata.type_value}
  get_key_value  ${output_A}  Actions    ${Actions}
  get_key_value  ${output_A}  DateTime
  get_key_value  ${output_A}  DateTimeLocalOffset
  get_key_value  ${output_A}  Description   ${Description}
  get_key_value  ${output_A}  Entries    ${Entries}
  get_key_value  ${output_A}  Id   ${Id}
  get_key_value  ${output_A}  Name    ${Name}
  get_key_value  ${output_A}  OverWritePolicy    ${OverWritePolicy}
  check error in curl output    ${output_A}
  get_key_value  ${output_B}  @odata.id   ${resource}
  get_key_value  ${output_B}  @odata.type   ${odata.type_value}
  get_key_value  ${output_B}  Actions    ${Actions}
  get_key_value  ${output_B}  DateTime
  get_key_value  ${output_B}  DateTimeLocalOffset
  get_key_value  ${output_B}  Description   ${Description}
  get_key_value  ${output_B}  Entries    ${Entries}
  get_key_value  ${output_B}  Id   ${Id}
  get_key_value  ${output_B}  Name    ${Name}
  get_key_value  ${output_B}  OverWritePolicy    ${OverWritePolicy}
  check error in curl output    ${output_B}

Verify Log Service-7
  [Arguments]   ${resource}  ${odata.type_value}  ${Description}   ${Entries}   ${Id}  ${Name}  ${OverWritePolicy}
  ${output_A} =  run_curl_get  ${resource}  %{bmc_ipv4_ip_1}  %{bmc_username_1}  %{bmc_password_1}
  ${output_B} =  run_curl_get  ${resource}  %{bmc_ipv4_ip_2}  %{bmc_username_2}  %{bmc_password_2}
  get_key_value  ${output_A}  @odata.id   ${resource}
  get_key_value  ${output_A}  @odata.type   ${odata.type_value}
  get_key_value  ${output_A}  DateTime
  get_key_value  ${output_A}  DateTimeLocalOffset
  get_key_value  ${output_A}  Description   ${Description}
  get_key_value  ${output_A}  Entries    ${Entries}
  get_key_value  ${output_A}  Id   ${Id}
  get_key_value  ${output_A}  Name    ${Name}
  get_key_value  ${output_A}  OverWritePolicy    ${OverWritePolicy}
  check error in curl output    ${output_A}
  get_key_value  ${output_B}  @odata.id   ${resource}
  get_key_value  ${output_B}  @odata.type   ${odata.type_value}
  get_key_value  ${output_B}  DateTime
  get_key_value  ${output_B}  DateTimeLocalOffset
  get_key_value  ${output_B}  Description   ${Description}
  get_key_value  ${output_B}  Entries    ${Entries}
  get_key_value  ${output_B}  Id   ${Id}
  get_key_value  ${output_B}  Name    ${Name}
  get_key_value  ${output_B}  OverWritePolicy    ${OverWritePolicy}
  check error in curl output    ${output_B}

Verify Manager-1
  [Arguments]   ${resource}  ${odata.type_value}  ${Actions}  ${Description}  ${EthernetInterface}   ${GraphicalConsole}   ${ID}  ${Links}  ${Logservices}  ${ManagerDiagnosticData}   ${ManagerType}   ${Model}   ${Name}   ${NetworkProtocol}  ${oem}  ${Powerstate}   ${SerialConsole}   ${status}
  ${output_A} =  run_curl_get  ${resource}  %{bmc_ipv4_ip_1}  %{bmc_username_1}  %{bmc_password_1}
  ${output_B} =  run_curl_get  ${resource}  %{bmc_ipv4_ip_2}  %{bmc_username_2}  %{bmc_password_2}
  get_key_value  ${output_A}  @odata.id   ${resource}
  get_key_value  ${output_A}  @odata.type   ${odata.type_value}
  get_key_value  ${output_A}  Actions  ${Actions}
  get_key_value  ${output_A}  DateTime
  get_key_value  ${output_A}  DateTimeLocalOffset
  get_key_value  ${output_A}  Description  ${Description}
  get_key_value  ${output_A}  EthernetInterfaces  ${EthernetInterface}
  get_key_value  ${output_A}  FirmwareVersion
  get_key_value  ${output_A}  GraphicalConsole  ${GraphicalConsole}
  get_key_value  ${output_A}  Id  ${ID}
  get_key_value  ${output_A}  LastResetTime
  get_key_value  ${output_A}  Links   ${Links}
  get_key_value  ${output_A}  LogServices   ${Logservices}
  get_key_value  ${output_A}  ManagerType  ${ManagerType}
  get_key_value  ${output_A}  Model  ${Model}
  get_key_value  ${output_A}  Name  ${Name}
  get_key_value  ${output_A}  NetworkProtocol  ${NetworkProtocol}
  get_key_value  ${output_A}  Oem   ${oem}
  get_key_value  ${output_A}  PowerState   ${Powerstate}
  get_key_value  ${output_A}  SerialConsole  ${SerialConsole}
  get_key_value  ${output_A}  ServiceEntryPointUUID
  get_key_value  ${output_A}  Status   ${status}
  get_key_value  ${output_A}  UUID
  check error in curl output    ${output_A}
  get_key_value  ${output_B}  @odata.id   ${resource}
  get_key_value  ${output_B}  @odata.type   ${odata.type_value}
  get_key_value  ${output_B}  Actions  ${Actions}
  get_key_value  ${output_B}  DateTime
  get_key_value  ${output_B}  DateTimeLocalOffset
  get_key_value  ${output_B}  Description  ${Description}
  get_key_value  ${output_B}  EthernetInterfaces  ${EthernetInterface}
  get_key_value  ${output_B}  FirmwareVersion
  get_key_value  ${output_B}  GraphicalConsole  ${GraphicalConsole}
  get_key_value  ${output_B}  Id  ${ID}
  get_key_value  ${output_B}  LastResetTime
  get_key_value  ${output_B}  Links   ${Links}
  get_key_value  ${output_B}  LogServices   ${Logservices}
  get_key_value  ${output_B}  ManagerType  ${ManagerType}
  get_key_value  ${output_B}  Model  ${Model}
  get_key_value  ${output_B}  Name  ${Name}
  get_key_value  ${output_B}  NetworkProtocol  ${NetworkProtocol}
  get_key_value  ${output_B}  Oem   ${oem}
  get_key_value  ${output_B}  PowerState   ${Powerstate}
  get_key_value  ${output_B}  SerialConsole  ${SerialConsole}
  get_key_value  ${output_B}  ServiceEntryPointUUID
  get_key_value  ${output_B}  Status   ${status}
  get_key_value  ${output_B}  UUID
  check error in curl output    ${output_B}

Verify Manager-5
  [Arguments]   ${resource}  ${odata.type_value}  ${dhcpv4}   ${dhcpv6}  ${Description}   ${EthernetInterfaceType}  ${FQDN}  ${HostName}  ${Id}  ${Name}  ${Status}
  ${output_A} =  run_curl_get  ${resource}  %{bmc_ipv4_ip_1}  %{bmc_username_1}  %{bmc_password_1}
  ${output_B} =  run_curl_get  ${resource}  %{bmc_ipv4_ip_2}  %{bmc_username_2}  %{bmc_password_2}
  get_key_value  ${output_A}  @odata.id   ${resource}
  get_key_value  ${output_A}  @odata.type   ${odata.type_value}
  get_key_value  ${output_A}  DHCPv4    ${dhcpv4}
  get_key_value  ${output_A}  DHCPv6   ${dhcpv6}
  get_key_value  ${output_A}  Description   ${Description}
  get_key_value  ${output_A}  EthernetInterfaceType   ${EthernetInterfaceType}
  get_key_value  ${output_A}  FQDN   ${FQDN}
  get_key_value  ${output_A}  HostName   ${HostName}
  get_key_value  ${output_A}  IPv4Addresses
  get_key_value  ${output_A}  IPv4StaticAddresses
  get_key_value  ${output_A}  IPv6AddressPolicyTable
  get_key_value  ${output_A}  IPv6Addresses
  get_key_value  ${output_A}  IPv6DefaultGateway
  get_key_value  ${output_A}  IPv6StaticAddresses
  get_key_value  ${output_A}  Id  ${Id}
  get_key_value  ${output_A}  InterfaceEnabled
  get_key_value  ${output_A}  LinkStatus
  get_key_value  ${output_A}  MACAddress
  get_key_value  ${output_A}  MTUSize
  get_key_value  ${output_A}  Name   ${Name}
  get_key_value  ${output_A}  NameServers
  get_key_value  ${output_A}  SpeedMbps
  get_key_value  ${output_A}  StaticNameServers
  get_key_value  ${output_A}  Status   ${Status}
  check error in curl output    ${output_A}
  get_key_value  ${output_B}  @odata.id   ${resource}
  get_key_value  ${output_B}  @odata.type   ${odata.type_value}
  get_key_value  ${output_B}  DHCPv4    ${dhcpv4}
  get_key_value  ${output_B}  DHCPv6   ${dhcpv6}
  get_key_value  ${output_B}  Description   ${Description}
  get_key_value  ${output_B}  EthernetInterfaceType   ${EthernetInterfaceType}
  get_key_value  ${output_B}  FQDN   ${FQDN}
  get_key_value  ${output_B}  HostName   ${HostName}
  get_key_value  ${output_B}  IPv4Addresses
  get_key_value  ${output_B}  IPv4StaticAddresses
  get_key_value  ${output_B}  IPv6AddressPolicyTable
  get_key_value  ${output_B}  IPv6Addresses
  get_key_value  ${output_B}  IPv6DefaultGateway
  get_key_value  ${output_B}  IPv6StaticAddresses
  get_key_value  ${output_B}  Id  ${Id}
  get_key_value  ${output_B}  InterfaceEnabled
  get_key_value  ${output_B}  LinkStatus
  get_key_value  ${output_B}  MACAddress
  get_key_value  ${output_B}  MTUSize
  get_key_value  ${output_B}  Name   ${Name}
  get_key_value  ${output_B}  NameServers
  get_key_value  ${output_B}  SpeedMbps
  get_key_value  ${output_B}  StaticNameServers
  get_key_value  ${output_B}  Status   ${Status}
  check error in curl output    ${output_B}

Verify ManagersNetworkProtocol
  [Arguments]   ${resource}  ${odata.type_value}  ${Description}   ${FQDN}  ${HTTP}   ${HTTPS}  ${HostName}  ${IPMI}  ${ID}   ${Name}  ${SSH}  ${Status}
  ${output_A} =  run_curl_get  ${resource}  %{bmc_ipv4_ip_1}  %{bmc_username_1}  %{bmc_password_1}
  ${output_B} =  run_curl_get  ${resource}  %{bmc_ipv4_ip_2}  %{bmc_username_2}  %{bmc_password_2}
  get_key_value  ${output_A}  @odata.id   ${resource}
  get_key_value  ${output_A}  @odata.type   ${odata.type_value}
  get_key_value  ${output_A}  Description  ${Description}
  get_key_value  ${output_A}  FQDN  ${FQDN}
  get_key_value  ${output_A}  HTTP  ${HTTP}
  get_key_value  ${output_A}  HTTPS  ${HTTPS}
  get_key_value  ${output_A}  HostName   ${HostName}
  get_key_value  ${output_A}  IPMI   ${IPMI}
  get_key_value  ${output_A}  Id   ${ID}
  get_key_value  ${output_A}  NTP
  get_key_value  ${output_A}  Name   ${Name}
  get_key_value  ${output_A}  SSH   ${SSH}
  get_key_value  ${output_A}  Status  ${Status}
  check error in curl output    ${output_A}
  get_key_value  ${output_B}  @odata.id   ${resource}
  get_key_value  ${output_B}  @odata.type   ${odata.type_value}
  get_key_value  ${output_B}  Description  ${Description}
  get_key_value  ${output_B}  FQDN  ${FQDN}
  get_key_value  ${output_B}  HTTP  ${HTTP}
  get_key_value  ${output_B}  HTTPS  ${HTTPS}
  get_key_value  ${output_B}  HostName   ${HostName}
  get_key_value  ${output_B}  IPMI   ${IPMI}
  get_key_value  ${output_B}  Id   ${ID}
  get_key_value  ${output_B}  NTP
  get_key_value  ${output_B}  Name   ${Name}
  get_key_value  ${output_B}  SSH   ${SSH}
  get_key_value  ${output_B}  Status  ${Status}
  check error in curl output    ${output_B}

Verify NetworkProtocol-2
  [Arguments]   ${resource}  ${odata.type_value}  ${Description}   ${ID}  ${Issuer}   ${keyusage}  ${Name}  ${subject}
  ${output_A} =  run_curl_get  ${resource}  %{bmc_ipv4_ip_1}  %{bmc_username_1}  %{bmc_password_1}
  ${output_B} =  run_curl_get  ${resource}  %{bmc_ipv4_ip_2}  %{bmc_username_2}  %{bmc_password_2}
  get_key_value  ${output_A}  @odata.id   ${resource}
  get_key_value  ${output_A}  @odata.type   ${odata.type_value}
  get_key_value  ${output_A}  CertificateString
  get_key_value  ${output_A}  Description  ${Description}
  get_key_value  ${output_A}  Id   ${ID}
  get_key_value  ${output_A}  Issuer    ${Issuer}
  get_key_value  ${output_A}  KeyUsage   ${keyusage}
  get_key_value  ${output_A}  Name   ${Name}
  get_key_value  ${output_A}  Subject   ${subject}
  get_key_value  ${output_A}  ValidNotAfter
  get_key_value  ${output_A}  ValidNotBefore
  check error in curl output    ${output_A}
  get_key_value  ${output_B}  @odata.id   ${resource}
  get_key_value  ${output_B}  @odata.type   ${odata.type_value}
  get_key_value  ${output_B}  CertificateString
  get_key_value  ${output_B}  Description  ${Description}
  get_key_value  ${output_B}  Id   ${ID}
  get_key_value  ${output_B}  Issuer    ${Issuer}
  get_key_value  ${output_B}  KeyUsage   ${keyusage}
  get_key_value  ${output_B}  Name   ${Name}
  get_key_value  ${output_B}  Subject   ${subject}
  get_key_value  ${output_B}  ValidNotAfter
  get_key_value  ${output_B}  ValidNotBefore
  check error in curl output    ${output_B}

Verify CertificateService-2
  [Arguments]   ${resource}  ${odata.type_value}  ${Description}   ${ID}   ${links}  ${Name}
  ${output_A} =  run_curl_get  ${resource}  %{bmc_ipv4_ip_1}  %{bmc_username_1}  %{bmc_password_1}
  ${output_B} =  run_curl_get  ${resource}  %{bmc_ipv4_ip_2}  %{bmc_username_2}  %{bmc_password_2}
  get_key_value  ${output_A}  @odata.id   ${resource}
  get_key_value  ${output_A}  @odata.type   ${odata.type_value}
  get_key_value  ${output_A}  Description  ${Description}
  get_key_value  ${output_A}  Id   ${ID}
  get_key_value  ${output_A}  Links   ${links}
  get_key_value  ${output_A}  Name   ${Name}
  check error in curl output    ${output_A}
  get_key_value  ${output_B}  @odata.id   ${resource}
  get_key_value  ${output_B}  @odata.type   ${odata.type_value}
  get_key_value  ${output_B}  Description  ${Description}
  get_key_value  ${output_B}  Id   ${ID}
  get_key_value  ${output_B}  Links   ${links}
  get_key_value  ${output_B}  Name   ${Name}
  check error in curl output    ${output_B}

Verify AccountService-1
  [Arguments]   ${resource}  ${odata.type_value}  ${AccountLockoutDuration}   ${AccountLockoutThreshold}  ${Accounts}   ${ActiveDirectory}   ${Description}   ${ID}  ${LDAP}  ${MaxPasswordLength}    ${MinPasswordLength}    ${Name}   ${Oem}   ${Roles}  ${ServiceEnabled}
  ${output_A} =  run_curl_get  ${resource}  %{bmc_ipv4_ip_1}  %{bmc_username_1}  %{bmc_password_1}
  ${output_B} =  run_curl_get  ${resource}  %{bmc_ipv4_ip_2}  %{bmc_username_2}  %{bmc_password_2}
  get_key_value  ${output_A}  @odata.id   ${resource}
  get_key_value  ${output_A}  @odata.type   ${odata.type_value}
  get_key_value  ${output_A}  AccountLockoutDuration    ${AccountLockoutDuration}
  get_key_value  ${output_A}  AccountLockoutThreshold   ${AccountLockoutThreshold}
  get_key_value  ${output_A}  Accounts    ${Accounts}
  get_key_value  ${output_A}  ActiveDirectory   ${ActiveDirectory}
  get_key_value  ${output_A}  Description  ${Description}
  get_key_value  ${output_A}  Id    ${ID}
  get_key_value  ${output_A}  LDAP    ${LDAP}
  get_key_value  ${output_A}  MaxPasswordLength    ${MaxPasswordLength}
  get_key_value  ${output_A}  MinPasswordLength    ${MinPasswordLength}
  get_key_value  ${output_A}  Name     ${Name}
  get_key_value  ${output_A}  Oem  ${Oem}
  get_key_value  ${output_A}  Roles   ${Roles}
  get_key_value  ${output_A}  ServiceEnabled   ${ServiceEnabled}
  check error in curl output    ${output_A}
  get_key_value  ${output_B}  @odata.id   ${resource}
  get_key_value  ${output_B}  @odata.type   ${odata.type_value}
  get_key_value  ${output_B}  AccountLockoutDuration    ${AccountLockoutDuration}
  get_key_value  ${output_B}  AccountLockoutThreshold   ${AccountLockoutThreshold}
  get_key_value  ${output_B}  Accounts    ${Accounts}
  get_key_value  ${output_B}  ActiveDirectory   ${ActiveDirectory}
  get_key_value  ${output_B}  Description  ${Description}
  get_key_value  ${output_B}  Id    ${ID}
  get_key_value  ${output_B}  LDAP    ${LDAP}
  get_key_value  ${output_B}  MaxPasswordLength    ${MaxPasswordLength}
  get_key_value  ${output_B}  MinPasswordLength    ${MinPasswordLength}
  get_key_value  ${output_B}  Name     ${Name}
  get_key_value  ${output_B}  Oem  ${Oem}
  get_key_value  ${output_B}  Roles   ${Roles}
  get_key_value  ${output_B}  ServiceEnabled   ${ServiceEnabled}
  check error in curl output    ${output_B}

Verify Log Service-2
  [Arguments]   ${resource}  ${odata.type_value}  ${Description}  ${Members_data_nextLink}  ${Name}
  ${output_A} =  run_curl_get  ${resource}  %{bmc_ipv4_ip_1}  %{bmc_username_1}  %{bmc_password_1}
  ${output_B} =  run_curl_get  ${resource}  %{bmc_ipv4_ip_2}  %{bmc_username_2}  %{bmc_password_2}
  get_key_value  ${output_A}  @odata.id   ${resource}
  get_key_value  ${output_A}  @odata.type   ${odata.type_value}
  get_key_value  ${output_A}  Description   ${Description}
  get_key_value  ${output_A}  Members
  get_key_value  ${output_A}  Members@odata.count
  #get_key_value  ${output_A}  Members@odata.nextLink   ${Members_data_nextLink}
  get_key_value  ${output_A}  Name   ${Name}
  check error in curl output    ${output_A}
  get_key_value  ${output_B}  @odata.id   ${resource}
  get_key_value  ${output_B}  @odata.type   ${odata.type_value}
  get_key_value  ${output_B}  Description   ${Description}
  get_key_value  ${output_B}  Members
  get_key_value  ${output_B}  Members@odata.count
  #get_key_value  ${output_B}  Members@odata.nextLink   ${Members_data_nextLink}
  get_key_value  ${output_B}  Name   ${Name}
  check error in curl output    ${output_B}

Verify UpdateService_6
  [Arguments]   ${resource}  ${data_type}  ${Members}  ${Members_odata_count}  ${Name}
  ${output_A} =  run_curl_get  ${resource}  %{bmc_ipv4_ip_1}  %{bmc_username_1}  %{bmc_password_1}
  ${output_B} =  run_curl_get  ${resource}  %{bmc_ipv4_ip_2}  %{bmc_username_2}  %{bmc_password_2}
  get_key_value  ${output_A}  @odata.id   ${resource}
  get_key_value  ${output_A}  @odata.type   ${data_type}
  get_key_value  ${output_A}  Members   ${Members}
  get_key_value  ${output_A}  Members@odata.count   ${Members_odata_count}
  get_key_value  ${output_A}  Name  ${Name}
  check error in curl output    ${output_A}
  get_key_value  ${output_B}  @odata.id   ${resource}
  get_key_value  ${output_B}  @odata.type   ${data_type}
  get_key_value  ${output_B}  Members   ${Members}
  get_key_value  ${output_B}  Members@odata.count   ${Members_odata_count}
  get_key_value  ${output_B}  Name  ${Name}
  check error in curl output    ${output_B}

verify telemetry service 1 details
  [Arguments]     ${resource}   ${data_type}   ${Id}   ${MaxReports}   ${MetricReportDefinitions}   ${MetricReports}   ${MinCollectionInterval}   ${Name}   ${Status}   ${SupportedCollectionFunctions}   ${Triggers}
  ${output_A} =  run_curl_get  ${resource}  %{bmc_ipv4_ip_1}  %{bmc_username_1}  %{bmc_password_1}
  ${output_B} =  run_curl_get  ${resource}  %{bmc_ipv4_ip_2}  %{bmc_username_2}  %{bmc_password_2}
  get_key_value  ${output_A}  @odata.id   ${resource}
  get_key_value  ${output_A}  @odata.type   ${data_type}
  get_key_value  ${output_A}  Id   ${Id}
  get_key_value  ${output_A}  MaxReports   ${MaxReports}
  get_key_value  ${output_A}  MetricReportDefinitions   ${MetricReportDefinitions}
  get_key_value  ${output_A}  MetricReports  ${MetricReports}
  get_key_value  ${output_A}  MinCollectionInterval   ${MinCollectionInterval}
  get_key_value  ${output_A}  Name  ${Name}
  get_key_value  ${output_A}  Status   ${Status}
  get_key_value  ${output_A}  SupportedCollectionFunctions  ${SupportedCollectionFunctions}
  get_key_value  ${output_A}  Triggers   ${Triggers}
  check error in curl output    ${output_A}
  get_key_value  ${output_B}  @odata.id   ${resource}
  get_key_value  ${output_B}  @odata.type   ${data_type}
  get_key_value  ${output_B}  Id   ${Id}
  get_key_value  ${output_B}  MaxReports   ${MaxReports}
  get_key_value  ${output_B}  MetricReportDefinitions   ${MetricReportDefinitions}
  get_key_value  ${output_B}  MetricReports  ${MetricReports}
  get_key_value  ${output_B}  MinCollectionInterval   ${MinCollectionInterval}
  get_key_value  ${output_B}  Name  ${Name}
  get_key_value  ${output_B}  Status   ${Status}
  get_key_value  ${output_B}  SupportedCollectionFunctions  ${SupportedCollectionFunctions}
  get_key_value  ${output_B}  Triggers   ${Triggers}
  check error in curl output    ${output_B}

verify role 2 details
  [Arguments]    ${resource}   ${data_type}   ${AssignedPrivileges}  ${Description}  ${Id}  ${IsPredefined}   ${Name}  ${OemPrivileges}  ${RoleId}
  ${output_A} =  run_curl_get  ${resource}  %{bmc_ipv4_ip_1}  %{bmc_username_1}  %{bmc_password_1}
  ${output_B} =  run_curl_get  ${resource}  %{bmc_ipv4_ip_2}  %{bmc_username_2}  %{bmc_password_2}
  get_key_value  ${output_A}  @odata.id   ${resource}
  get_key_value  ${output_A}  @odata.type   ${data_type}
  get_key_value  ${output_A}  AssignedPrivileges  ${AssignedPrivileges}
  get_key_value  ${output_A}  Description  ${Description}
  get_key_value  ${output_A}  Id   ${Id}
  get_key_value  ${output_A}  IsPredefined     ${IsPredefined}
  get_key_value  ${output_A}  Name  ${Name}
  get_key_value  ${output_A}  OemPrivileges   ${OemPrivileges}
  get_key_value  ${output_A}  RoleId  ${RoleId}
  check error in curl output    ${output_A}
  get_key_value  ${output_B}  @odata.id   ${resource}
  get_key_value  ${output_B}  @odata.type   ${data_type}
  get_key_value  ${output_B}  AssignedPrivileges  ${AssignedPrivileges}
  get_key_value  ${output_B}  Description  ${Description}
  get_key_value  ${output_B}  Id   ${Id}
  get_key_value  ${output_B}  IsPredefined     ${IsPredefined}
  get_key_value  ${output_B}  Name  ${Name}
  get_key_value  ${output_B}  OemPrivileges   ${OemPrivileges}
  get_key_value  ${output_B}  RoleId  ${RoleId}
  check error in curl output    ${output_B}

verify TaskService details
  [Arguments]    ${resource}   ${data_type}   ${CompletedTaskOverWritePolicy}   ${Id}   ${LifeCycleEventOnTaskStateChange}   ${Name}   ${ServiceEnabled}   ${Status}   ${Tasks}
  ${output_A} =  run_curl_get  ${resource}  %{bmc_ipv4_ip_1}  %{bmc_username_1}  %{bmc_password_1}
  ${output_B} =  run_curl_get  ${resource}  %{bmc_ipv4_ip_2}  %{bmc_username_2}  %{bmc_password_2}
  get_key_value  ${output_A}  @odata.id   ${resource}
  get_key_value  ${output_A}  @odata.type   ${data_type}
  get_key_value  ${output_A}  CompletedTaskOverWritePolicy   ${CompletedTaskOverWritePolicy}
  get_key_value  ${output_A}  Id   ${Id}
  get_key_value  ${output_A}  LifeCycleEventOnTaskStateChange   ${LifeCycleEventOnTaskStateChange}
  get_key_value  ${output_A}  Name  ${Name}
  get_key_value  ${output_A}  ServiceEnabled   ${ServiceEnabled}
  get_key_value  ${output_A}  Status    ${Status}
  get_key_value  ${output_A}  Tasks   ${Tasks}
  get_key_value  ${output_A}  DateTime
  check error in curl output    ${output_A}
  get_key_value  ${output_B}  @odata.id   ${resource}
  get_key_value  ${output_B}  @odata.type   ${data_type}
  get_key_value  ${output_B}  CompletedTaskOverWritePolicy   ${CompletedTaskOverWritePolicy}
  get_key_value  ${output_B}  Id   ${Id}
  get_key_value  ${output_B}  LifeCycleEventOnTaskStateChange   ${LifeCycleEventOnTaskStateChange}
  get_key_value  ${output_B}  Name  ${Name}
  get_key_value  ${output_B}  ServiceEnabled   ${ServiceEnabled}
  get_key_value  ${output_B}  Status    ${Status}
  get_key_value  ${output_B}  Tasks   ${Tasks}
  get_key_value  ${output_B}  DateTime
  check error in curl output    ${output_B}

verify thermal_1 details
  [Arguments]    ${resource}   ${data_type}  ${Id}  ${Name}   ${Redundancy}
  ${output_A} =  run_curl_get  ${resource}  %{bmc_ipv4_ip_1}  %{bmc_username_1}  %{bmc_password_1}
  ${output_B} =  run_curl_get  ${resource}  %{bmc_ipv4_ip_2}  %{bmc_username_2}  %{bmc_password_2}
  get_key_value  ${output_A}  @odata.id   ${resource}
  get_key_value  ${output_A}  @odata.type   ${data_type}
  get_key_value  ${output_A}  Id   ${Id}
  get_key_value  ${output_A}  Name  ${Name}
  get_key_value  ${output_A}  Redundancy   ${Redundancy}
  get_key_value  ${output_A}  Fans
  get_key_value  ${output_A}  Temperatures
  verify all fans   ${output_A}  35
  verify_all_temperatures  ${output_A}   59
  verify_count_State   ${output_A}  94
  verify_count_Health  ${output_A}  94
  check error in curl output    ${output_A}
  get_key_value  ${output_B}  @odata.id   ${resource}
  get_key_value  ${output_B}  @odata.type   ${data_type}
  get_key_value  ${output_B}  Id   ${Id}
  get_key_value  ${output_B}  Name  ${Name}
  get_key_value  ${output_B}  Redundancy   ${Redundancy}
  get_key_value  ${output_B}  Fans
  get_key_value  ${output_B}  Temperatures
  verify all fans   ${output_B}  35
  verify_all_temperatures  ${output_B}   59
  verify all fans   ${output_B}  35
  verify_all_temperatures  ${output_B}   59
  verify_count_State   ${output_B}  94
  verify_count_Health  ${output_B}  94
  check error in curl output    ${output_B}

Verify PowerCollection
  [Arguments]   ${resource}  ${odata.type_value}  ${ID}  ${Name}
  ${output_A} =  run_curl_get  ${resource}  %{bmc_ipv4_ip_1}  %{bmc_username_1}  %{bmc_password_1}
  ${output_B} =  run_curl_get  ${resource}  %{bmc_ipv4_ip_2}  %{bmc_username_2}  %{bmc_password_2}
  get_key_value  ${output_A}  @odata.id   ${resource}
  get_key_value  ${output_A}  @odata.type   ${odata.type_value}
  get_key_value  ${output_A}  Id    ${ID}
  get_key_value  ${output_A}  Name     ${Name}
  verify_count_State   ${output_A}  23
  verify_count_Health  ${output_A}  23
  check error in curl output    ${output_A}
  get_key_value  ${output_B}  @odata.id   ${resource}
  get_key_value  ${output_B}  @odata.type   ${odata.type_value}
  get_key_value  ${output_B}  Id    ${ID}
  get_key_value  ${output_B}  Name     ${Name}
  verify_count_State   ${output_A}  23
  verify_count_Health  ${output_A}  23
  check error in curl output    ${output_B}

Verify openbmc system bios
  [Arguments]   ${resource}  ${odata.type_value}  ${Description}  ${ID}  ${Name}   ${RelatedItem}   ${RelatedItem_count}  ${Status}  ${Updatable}  ${Version}
  ${output_A} =  run_curl_get  ${resource}  %{bmc_ipv4_ip_1}  %{bmc_username_1}  %{bmc_password_1}
  ${output_B} =  run_curl_get  ${resource}  %{bmc_ipv4_ip_2}  %{bmc_username_2}  %{bmc_password_2}
  get_key_value  ${output_A}  @odata.id   ${resource}
  get_key_value  ${output_A}  @odata.type   ${odata.type_value}
  get_key_value  ${output_A}  Description   ${Description}
  get_key_value  ${output_A}  Id    ${ID}
  get_key_value  ${output_A}  Name    ${Name}
  get_key_value  ${output_A}  RelatedItem   ${RelatedItem}
  get_key_value  ${output_A}  RelatedItem@odata.count   ${RelatedItem_count}
  get_key_value  ${output_A}  Status  ${Status}
  get_key_value  ${output_A}  Updateable    ${Updatable}
  get_key_value  ${output_A}  Version   ${Version}
  check error in curl output    ${output_A}
  get_key_value  ${output_B}  @odata.id   ${resource}
  get_key_value  ${output_B}  @odata.type   ${odata.type_value}
  get_key_value  ${output_B}  Description   ${Description}
  get_key_value  ${output_B}  Id    ${ID}
  get_key_value  ${output_B}  Name    ${Name}
  get_key_value  ${output_B}  RelatedItem   ${RelatedItem}
  get_key_value  ${output_B}  RelatedItem@odata.count   ${RelatedItem_count}
  get_key_value  ${output_B}  Status  ${Status}
  get_key_value  ${output_B}  Updateable    ${Updatable}
  get_key_value  ${output_B}  Version   ${Version}
  check error in curl output    ${output_B}

Verify openbmc upgrade bios
  [Arguments]   ${resource}   ${filename}
  ${output_A} =  run_curl_post  ${resource}   ${filename}   %{bmc_ipv4_ip_1}  %{bmc_username_1}  %{bmc_password_1}
  get_key_value  ${output_A}   TaskState   Running
  get_key_value  ${output_A}   TaskStatus   OK
  check error in curl output    ${output_A}
  Sleep  900
  dc_cycle_server_1  %{bmc_ipv4_ip_1}  %{bmc_username_1}  %{bmc_password_1}
  Sleep  400
  ${output_B} =  run_curl_post  ${resource}   ${filename}   %{bmc_ipv4_ip_2}  %{bmc_username_2}  %{bmc_password_2}
  get_key_value  ${output_B}   TaskState   Running
  get_key_value  ${output_B}   TaskStatus   OK
  check error in curl output    ${output_B}
  Sleep  900
  dc_cycle_server_1  %{bmc_ipv4_ip_2}  %{bmc_username_2}  %{bmc_password_2}
  Sleep  400

Verify openbmc upgrade cpld
  [Arguments]   ${resource}   ${filename}
  ${output_A} =  run_curl_post  ${resource}   ${filename}   %{bmc_ipv4_ip_1}  %{bmc_username_1}  %{bmc_password_1}
  get_key_value  ${output_A}   TaskState   Running
  get_key_value  ${output_A}   TaskStatus   OK
  check error in curl output    ${output_A}
  Sleep  900
  dc_cycle_server_1  %{bmc_ipv4_ip_1}  %{bmc_username_1}  %{bmc_password_1}
  Sleep  400
  ${output_B} =  run_curl_post  ${resource}   ${filename}   %{bmc_ipv4_ip_2}  %{bmc_username_2}  %{bmc_password_2}
  get_key_value  ${output_B}   TaskState   Running
  get_key_value  ${output_B}   TaskStatus   OK
  check error in curl output    ${output_B}
  Sleep  900
  dc_cycle_server_1  %{bmc_ipv4_ip_2}  %{bmc_username_2}  %{bmc_password_2}
  Sleep  400

Verify openbmc system cpld
  [Arguments]   ${resource}  ${odata.type_value}  ${Description}  ${ID}  ${Name}   ${Status}  ${Updatable}  ${Version}
  ${output_A} =  run_curl_get  ${resource}  %{bmc_ipv4_ip_1}  %{bmc_username_1}  %{bmc_password_1}
  ${output_B} =  run_curl_get  ${resource}  %{bmc_ipv4_ip_2}  %{bmc_username_2}  %{bmc_password_2}
  get_key_value  ${output_A}  @odata.id   ${resource}
  get_key_value  ${output_A}  @odata.type   ${odata.type_value}
  get_key_value  ${output_A}  Description   ${Description}
  get_key_value  ${output_A}  Id    ${ID}
  get_key_value  ${output_A}  Name    ${Name}
  get_key_value  ${output_A}  Status  ${Status}
  get_key_value  ${output_A}  Updateable    ${Updatable}
  get_key_value  ${output_A}  Version   ${Version}
  check error in curl output    ${output_A}
  get_key_value  ${output_B}  @odata.id   ${resource}
  get_key_value  ${output_B}  @odata.type   ${odata.type_value}
  get_key_value  ${output_B}  Description   ${Description}
  get_key_value  ${output_B}  Id    ${ID}
  get_key_value  ${output_B}  Name    ${Name}
  get_key_value  ${output_B}  Status  ${Status}
  get_key_value  ${output_B}  Updateable    ${Updatable}
  get_key_value  ${output_B}  Version   ${Version}
  check error in curl output    ${output_B}

