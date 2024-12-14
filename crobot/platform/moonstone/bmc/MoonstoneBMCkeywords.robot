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
# Script       : BMC_keywords.robot                                                                                   #
# Date         : July 29, 2020                                                                                        #
# Author       : James Shi <jameshi@celestica.com>                                                                    #
# Description  : This script used as keywords in bmc.robot                                                            #
#                                                                                                                     #
# Script Revision Details:                                                                                            #
#   Initial Draft for BMC testing                                                                                     #
#######################################################################################################################

*** Settings ***
#Variables         BMC_variable.py
#Library           whitebox_lib.py
#Library           openbmc_lib.py
Library           bios_menu_lib.py
Library           CommonLib.py
Library           OperatingSystem
#Library           WhiteboxLibAdapter.py
#Library           ../ses/ses_lib.py

Resource          CommonResource.robot

*** Variables ***
${LoopCnt}        1
${MaxLoopNum}     2

*** Keywords ***

Power cycle test
   Step  1  MOONSTONECommonLib.Powercycle Device   DUT

reset_sol_configuration
    Step  1  set_and_check_sol_configuration  DUT  enabled  true
    Step  2  set_and_check_sol_configuration  DUT  non-volatile-bit-rate  115.2
    Step  3  set_and_check_sol_configuration  DUT  volatile-bit-rate  115.2
    Step  4  check_default_sol_configuration  DUT
    Step  5  exit the server  DUT


end online update via lan
    Step  1  check server moonstone  DUT  ${scp_ip}  ${scp_username}  ${scp_password}  ${dhcp_prompt}
    Step  2  update bmc image  DUT  R4039-DS3000-1.02.00.ima
    Step  3  check_bmc_version_through_raw_cmd  DUT  ${version2}  True
    Step  4  exit the server  DUT

copy old bios image from server to bmc console
	Step  1  check server moonstone  DUT  ${scp_ip}  ${scp_username}  ${scp_password}  ${dhcp_prompt}
	Step  2  copy_bios_image_from_server_via_scp  DUT  ${old_bios_image}
	Step  3  exit the server  DUT
	
copy new bios image from server to bmc console
	Step  1  check server moonstone  DUT  ${scp_ip}  ${scp_username}  ${scp_password}  ${dhcp_prompt}
	Step  2  copy_bios_image_from_server_via_scp  DUT  ${new_bios_image}
	Step  3  exit the server  DUT
	
downgrade primary bios image through bmc console
    verify_the_bios_version  DUT  ${new_bios_image}
	copy old bios image from server to bmc console
    switch bmc  DUT
    update_bios_image  DUT  ${old_bios_image}  0  lanplus=True
    switch cpu  DUT
    # # bios_boot  DUT  0
    verify_the_bios_version  DUT  ${old_bios_image}

upgrade primary bios image through bmc console
    verify_the_bios_version  DUT  ${old_bios_image}
	copy new bios image from server to bmc console
    switch bmc  DUT
    update_bios_image  DUT  ${new_bios_image}  0  lanplus=True
    switch cpu  DUT
    # # bios_boot  DUT  0
    verify_the_bios_version  DUT  ${new_bios_image}

downgrade primary bios image through lan
    update_bios_image  DUT  ${old_bios_image}  0  lanplus=True
    bios_boot  DUT  0
    verify_the_bios_version  DUT  ${old_bios_image}

upgrade primary bios image through lan
    update_bios_image  DUT  ${new_bios_image}  0  lanplus=True
    bios_boot  DUT  0
    verify_the_bios_version  DUT  ${new_bios_image}

downgrade backup bios image through lan
    bios_boot  DUT  1
    update_bios_image  DUT  ${old_bios_image}  0  lanplus=True
    bios_boot  DUT  1
    verify_the_bios_version  DUT  ${old_bios_image}

upgrade backup bios image through lan
    bios_boot  DUT  1
    update_bios_image  DUT  ${new_bios_image}  0  lanplus=True
    bios_boot  DUT  1
    verify_the_bios_version  DUT  ${new_bios_image}


prepare BMC images
    ${server_ipv4_ip} =  get_ip_address_from_config  PC
    ${sw_image_hostImageDir} =  get_sw_image_hostImageDir  DUT  swimage_type=BMC
    ${sw_image_localImageDir} =  get_sw_image_localImageDir  DUT  swimage_type=BMC
    ${bmc_ipv4_ip} =  get_ip_address_from_ipmitool  DUT  eth_type=dedicated
    ${DUT_ipv4_ip} =  get_ip_address_from_config  UUT
    ${DUT_username} =  get_username_from_config  UUT
    ${DUT_password} =  get_password_from_config  UUT
    ${server_username} =  get_username_from_config  PC
    ${server_password} =  get_password_from_config  PC
    Set Environment Variable  server_ipv4_ip_1  ${server_ipv4_ip}
    Set Environment Variable  bmc_ipv4_ip_1  ${bmc_ipv4_ip}
    Set Environment Variable  server_username_1  ${server_username}
    Set Environment Variable  server_password_1  ${server_password}
    Set Environment Variable  DUT_ipv4_ip_1  ${DUT_ipv4_ip}
    Set Environment Variable  DUT_username_1  ${DUT_username}
    Set Environment Variable  DUT_password_1  ${DUT_password}
    Step  1  mkdir data path  DUT  ${sw_image_localImageDir}
    Step  2  download images  DUT  BMC
    Step  3  change_directory  DUT  ${sw_image_localImageDir}
    Step  4  copy files from PC to OS  DUT  ${server_username}  ${server_password}
              ...   ${server_ipv4_ip}  filepath=${sw_image_hostImageDir}  filename=${FW_update_tool}
              ...   destination_path=${sw_image_localImageDir}  size_MB=10
    Step  5  chmod file  DUT  filename=${FW_update_tool}

prepare BIOS images
    ${server_ipv4_ip} =  get_ip_address_from_config  PC
    ${sw_image_hostImageDir} =  get_sw_image_hostImageDir  DUT  swimage_type=BIOS
    ${sw_image_localImageDir} =  get_sw_image_localImageDir  DUT  swimage_type=BIOS
    ${bmc_ipv4_ip} =  get_ip_address_from_ipmitool  DUT  eth_type=dedicated
    ${DUT_ipv4_ip} =  get_ip_address_from_config  UUT
    ${DUT_username} =  get_username_from_config  UUT
    ${DUT_password} =  get_password_from_config  UUT
    ${server_username} =  get_username_from_config  PC
    ${server_password} =  get_password_from_config  PC
    Set Environment Variable  server_ipv4_ip_1  ${server_ipv4_ip}
    Set Environment Variable  bmc_ipv4_ip_1  ${bmc_ipv4_ip}
    Set Environment Variable  server_username_1  ${server_username}
    Set Environment Variable  server_password_1  ${server_password}
    Set Environment Variable  DUT_ipv4_ip_1  ${DUT_ipv4_ip}
    Set Environment Variable  DUT_username_1  ${DUT_username}
    Set Environment Variable  DUT_password_1  ${DUT_password}
    Step  1  mkdir data path  DUT  ${sw_image_localImageDir}
    Step  2  download images  DUT  BIOS
    Step  3  change_directory  DUT  ${sw_image_localImageDir}
    Step  4  copy files from PC to OS  DUT  ${server_username}  ${server_password}
              ...   ${server_ipv4_ip}  filepath=${sw_image_hostImageDir}  filename=${FW_update_tool}
              ...   destination_path=${sw_image_localImageDir}  size_MB=10
    Step  5  chmod file  DUT  filename=${FW_update_tool}

restore serial ouput to normal
    ${server_ipv4_ip} =  get_ip_address_from_config  PC
    ${server_username} =  get_username_from_config  PC
    ${server_password} =  get_password_from_config  PC
    Step  1  set time delay  60
    Step  2  Keyword Retry  power_cycle_os_by_ipmitool  DUT  ${server_username}  ${server_ipv4_ip}  ${server_password}
        ...  %{bmc_ipv4_ip_1}  ipmitool_cmd=power cycle  bmcusername=${bmc_username}  bmcpassword=${bmc_password}
    Step  3  set time delay  30
    Step  4  Keyword Retry  power_cycle_os_by_ipmitool  DUT  ${server_username}  ${server_ipv4_ip}  ${server_password}
        ...  %{bmc_ipv4_ip_1}  ipmitool_cmd=power on  bmcusername=${bmc_username}  bmcpassword=${bmc_password}
    Step  5  set time delay  20
    Step  6  wait_prompt  DUT

power cycle OS
    Step  1  Keyword Retry  power_cycle_os_by_ipmitool  DUT  %{server_username_1}  %{server_ipv4_ip_1}
        ...  %{server_password_1}  %{bmc_ipv4_ip_1}  ipmitool_cmd=power cycle  bmcusername=${bmc_username}
        ...  bmcpassword=${bmc_password}
    Step  2  set time delay  30
    Step  3  Keyword Retry  power_cycle_os_by_ipmitool  DUT  %{server_username_1}  %{server_ipv4_ip_1}
        ...  %{server_password_1}  %{bmc_ipv4_ip_1}  ipmitool_cmd=power on  bmcusername=${bmc_username}
        ...  bmcpassword=${bmc_password}
    Step  4  set time delay  20
    Step  5  wait_prompt  DUT

upgrade bmc and dc cycle to check version
    Step  1  run_ipmi_cmd_sel_clear  DUT
    Step  2  update whitebox bmc  DUT  toolname=${FW_update_tool}  device_type=BMC
        ...  bmcip=%{bmc_ipv4_ip_1}  isUpgrade=True  local=True
    Step  3  Keyword Retry  power_cycle_os_by_ipmitool  DUT  %{server_username_1}  %{server_ipv4_ip_1}
        ...  %{server_password_1}  %{bmc_ipv4_ip_1}  ipmitool_cmd=power cycle  bmcusername=${bmc_username}
        ...  bmcpassword=${bmc_password}
    Step  4  set time delay  20
    Step  5  wait_prompt  DUT
    Step  6  whitebox_lib.verify_fw_version  DUT  device_type=BMC  isUpgrade=True

remote upgrade bmc and dc cycle to check version
    Step  1  run_ipmi_cmd_sel_clear  DUT
    Step  2  Keyword Retry  update whitebox bmc  DUT  toolname=${FW_update_tool}  device_type=BMC  username=%{server_username_1}
        ...  hostip=%{server_ipv4_ip_1}  password=%{server_password_1}  bmcip=%{bmc_ipv4_ip_1}  isUpgrade=True
        ...  local=False  bmcusername=${bmc_username}  bmcpassword=${bmc_password}
    Step  3  Keyword Retry  power_cycle_os_by_ipmitool  DUT  %{server_username_1}  %{server_ipv4_ip_1}
        ...  %{server_password_1}  %{bmc_ipv4_ip_1}  ipmitool_cmd=power cycle  bmcusername=${bmc_username}
        ...  bmcpassword=${bmc_password}
    Step  4  set time delay  20
    Step  5  wait_prompt  DUT
    Step  6  whitebox_lib.verify_fw_version  DUT  device_type=BMC  isUpgrade=True

remote upgrade bios and reboot to check version
    Step  1  run_ipmi_cmd_sel_clear  DUT
    Step  2  Keyword Retry  update whitebox bios  DUT  toolname=${FW_update_tool}  device_type=BIOS
        ...  username=%{server_username_1}  hostip=%{server_ipv4_ip_1}  password=%{server_password_1}  bmcip=%{bmc_ipv4_ip_1}
        ...  isUpgrade=True  local=False  bmcusername=${bmc_username}  bmcpassword=${bmc_password}
    Step  3  reboot_os  DUT
    Step  4  set time delay  60
    Step  5  Keyword Retry  power_cycle_os_by_ipmitool  DUT  %{server_username_1}  %{server_ipv4_ip_1}
        ...  %{server_password_1}  %{bmc_ipv4_ip_1}  ipmitool_cmd=power on  bmcusername=${bmc_username}
        ...  bmcpassword=${bmc_password}
    Step  6  set time delay  20
    Step  7  wait_prompt  DUT
    Step  8  whitebox_lib.verify_fw_version  DUT  device_type=BIOS  isUpgrade=True

remote upgrade bios and dc cycle to check version
    Step  1  run_ipmi_cmd_sel_clear  DUT
    Step  2  Keyword Retry  update whitebox bios  DUT  toolname=${FW_update_tool}  device_type=BIOS
        ...  username=%{server_username_1}  hostip=%{server_ipv4_ip_1}  password=%{server_password_1}  bmcip=%{bmc_ipv4_ip_1}
        ...  isUpgrade=True  local=False  bmcusername=${bmc_username}  bmcpassword=${bmc_password}
    Step  3  Keyword Retry  power_cycle_os_by_ipmitool  DUT  %{server_username_1}  %{server_ipv4_ip_1}
        ...  %{server_password_1}  %{bmc_ipv4_ip_1}  ipmitool_cmd=power cycle  bmcusername=${bmc_username}
        ...  bmcpassword=${bmc_password}
    Step  4  set time delay  20
    Step  5  wait_prompt  DUT
    Step  6  whitebox_lib.verify_fw_version  DUT  device_type=BIOS  isUpgrade=True

downgrade bmc and dc cycle to check version
    Step  1  run_ipmi_cmd_sel_clear  DUT
    Step  2  update whitebox bmc  DUT  toolname=${FW_update_tool}  device_type=BMC
        ...  bmcip=%{bmc_ipv4_ip_1}  isUpgrade=False  local=True
    Step  3  Keyword Retry  power_cycle_os_by_ipmitool  DUT  %{server_username_1}  %{server_ipv4_ip_1}
        ...  %{server_password_1}  %{bmc_ipv4_ip_1}  ipmitool_cmd=power cycle  bmcusername=${bmc_username}
        ...  bmcpassword=${bmc_password}
    Step  4  set time delay  20
    Step  5  wait_prompt  DUT
    Step  6  whitebox_lib.verify_fw_version  DUT  device_type=BMC  isUpgrade=False

remote downgrade bmc and dc cycle to check version
    Step  1  run_ipmi_cmd_sel_clear  DUT
    Step  2  Keyword Retry  update whitebox bmc  DUT  toolname=${FW_update_tool}  device_type=BMC
        ...  username=%{server_username_1}  hostip=%{server_ipv4_ip_1}  password=%{server_password_1}  bmcip=%{bmc_ipv4_ip_1}
        ...  isUpgrade=False  local=False  bmcusername=${bmc_username}  bmcpassword=${bmc_password}
    Step  3  Keyword Retry  power_cycle_os_by_ipmitool  DUT  %{server_username_1}  %{server_ipv4_ip_1}
        ...  %{server_password_1}  %{bmc_ipv4_ip_1}  ipmitool_cmd=power cycle  bmcusername=${bmc_username}
        ...  bmcpassword=${bmc_password}
    Step  4  set time delay  20
    Step  5  wait_prompt  DUT
    Step  6  whitebox_lib.verify_fw_version  DUT  device_type=BMC  isUpgrade=False

remote downgrade bios and reboot to check version
    Step  1  run_ipmi_cmd_sel_clear  DUT
    Step  2  Keyword Retry  update whitebox bios  DUT  toolname=${FW_update_tool}  device_type=BIOS
        ...  username=%{server_username_1}  hostip=%{server_ipv4_ip_1}  password=%{server_password_1}  bmcip=%{bmc_ipv4_ip_1}
        ...  isUpgrade=False  local=False  bmcusername=${bmc_username}  bmcpassword=${bmc_password}
    Step  3  reboot_os  DUT
    Step  4  set time delay  60
    Step  5  Keyword Retry  power_cycle_os_by_ipmitool  DUT  %{server_username_1}  %{server_ipv4_ip_1}
        ...  %{server_password_1}  %{bmc_ipv4_ip_1}  ipmitool_cmd=power on  bmcusername=${bmc_username}
        ...  bmcpassword=${bmc_password}
    Step  6  set time delay  20
    Step  7  wait_prompt  DUT
    Step  8  whitebox_lib.verify_fw_version  DUT  device_type=BIOS  isUpgrade=False

remote downgrade bios and dc cycle to check version
    Step  1  run_ipmi_cmd_sel_clear  DUT
    Step  2  Keyword Retry  update whitebox bios  DUT  toolname=${FW_update_tool}  device_type=BIOS
        ...  username=%{server_username_1}  hostip=%{server_ipv4_ip_1}  password=%{server_password_1}  bmcip=%{bmc_ipv4_ip_1}
        ...  isUpgrade=False  local=False  bmcusername=${bmc_username}  bmcpassword=${bmc_password}
    Step  3  Keyword Retry  power_cycle_os_by_ipmitool  DUT  %{server_username_1}  %{server_ipv4_ip_1}
        ...  %{server_password_1}  %{bmc_ipv4_ip_1}  ipmitool_cmd=power cycle  bmcusername=${bmc_username}
        ...  bmcpassword=${bmc_password}
    Step  4  set time delay  20
    Step  5  wait_prompt  DUT
    Step  6  whitebox_lib.verify_fw_version  DUT  device_type=BIOS  isUpgrade=False

upgrade bios and dc cycle to check version
    Step  1  run_ipmi_cmd_sel_clear  DUT
    Step  2  update whitebox bios  DUT  toolname=${FW_update_tool}  device_type=BIOS  bmcip=%{bmc_ipv4_ip_1}
        ...  isUpgrade=True  local=True
    Step  3  Keyword Retry  power_cycle_os_by_ipmitool  DUT  %{server_username_1}  %{server_ipv4_ip_1}
        ...  %{server_password_1}  %{bmc_ipv4_ip_1}  ipmitool_cmd=power cycle  bmcusername=${bmc_username}
        ...  bmcpassword=${bmc_password}
    Step  4  set time delay  20
    Step  5  wait_prompt  DUT
    Step  6  whitebox_lib.verify_fw_version  DUT  device_type=BIOS  isUpgrade=True

upgrade bios and reboot to check version
    Step  1  run_ipmi_cmd_sel_clear  DUT
    Step  2  update whitebox bios  DUT  toolname=${FW_update_tool}  device_type=BIOS  bmcip=%{bmc_ipv4_ip_1}
        ...  isUpgrade=True  local=True
    Step  3  reboot_os  DUT
    Step  4  set time delay  30
    Step  5  Keyword Retry  power_cycle_os_by_ipmitool  DUT  %{server_username_1}  %{server_ipv4_ip_1}
        ...  %{server_password_1}  %{bmc_ipv4_ip_1}  ipmitool_cmd=power on  bmcusername=${bmc_username}
        ...  bmcpassword=${bmc_password}
    Step  6  set time delay  20
    Step  7  wait_prompt  DUT
    Step  8  whitebox_lib.verify_fw_version  DUT  device_type=BIOS  isUpgrade=True

downgrade bios and dc cycle to check version
    Step  1  run_ipmi_cmd_sel_clear  DUT
    Step  2  update whitebox bios  DUT  toolname=${FW_update_tool}  device_type=BIOS  bmcip=%{bmc_ipv4_ip_1}
        ...  isUpgrade=False  local=True
    Step  3  Keyword Retry  power_cycle_os_by_ipmitool  DUT  %{server_username_1}  %{server_ipv4_ip_1}
        ...  %{server_password_1}  %{bmc_ipv4_ip_1}  ipmitool_cmd=power cycle  bmcusername=${bmc_username}
        ...  bmcpassword=${bmc_password}
    Step  4  set time delay  20
    Step  5  wait_prompt  DUT
    Step  6  whitebox_lib.verify_fw_version  DUT  device_type=BIOS  isUpgrade=False

downgrade bios and reboot to check version
    Step  1  run_ipmi_cmd_sel_clear  DUT
    Step  2  update whitebox bios  DUT  toolname=${FW_update_tool}  device_type=BIOS  bmcip=%{bmc_ipv4_ip_1}
        ...  isUpgrade=False  local=True
    Step  3  reboot_os  DUT
    Step  4  set time delay  60
    Step  5  Keyword Retry  power_cycle_os_by_ipmitool  DUT  %{server_username_1}  %{server_ipv4_ip_1}
        ...  %{server_password_1}  %{bmc_ipv4_ip_1}  ipmitool_cmd=power on  bmcusername=${bmc_username}
        ...  bmcpassword=${bmc_password}
    Step  6  set time delay  20
    Step  7  wait_prompt  DUT
    Step  8  whitebox_lib.verify_fw_version  DUT  device_type=BIOS  isUpgrade=False

run ipmi command "Get Device ID"
    Step  1  verify ipmi test  get_device_id  DUT  ${cmd_get_device_id}  ${device_id}

run ipmi command "cold reset"
    ${bmc_ipv4_ip} =  get_ip_address_from_ipmitool  DUT  eth_type=dedicated
    ${DUT_ipv4_ip} =  get_ip_address_from_config  UUT
    ${DUT_username} =  get_username_from_config  UUT
    ${DUT_password} =  get_password_from_config  UUT
    Set Environment Variable  bmc_ipv4_ip_1  ${bmc_ipv4_ip}
    Step  1  run_ipmi_cmd_sel_clear  DUT
    Step  2  Keyword Retry  run_ipmi_cmd_reset  DUT  ${DUT_username}  ${DUT_ipv4_ip}  ${DUT_password}
        ...  ${cmd_cold_reset}
    Step  3  Keyword Retry  ssh_command_run_ipmi_set_cmd  ${DUT_username}  ${DUT_ipv4_ip}  ${DUT_password}  reboot
    Step  4  wait_prompt  DUT

run ipmi command "warm reset"
    ${bmc_ipv4_ip} =  get_ip_address_from_ipmitool  DUT  eth_type=dedicated
    ${DUT_ipv4_ip} =  get_ip_address_from_config  UUT
    ${DUT_username} =  get_username_from_config  UUT
    ${DUT_password} =  get_password_from_config  UUT
    Set Environment Variable  bmc_ipv4_ip_1  ${bmc_ipv4_ip}
    Step  1  run_ipmi_cmd_sel_clear  DUT
    Step  2  Keyword Retry  run_ipmi_cmd_reset  DUT  ${DUT_username}  ${DUT_ipv4_ip}  ${DUT_password}
        ...  ${cmd_warm_reset}
    Step  3  Keyword Retry  ssh_command_run_ipmi_set_cmd  ${DUT_username}  ${DUT_ipv4_ip}  ${DUT_password}  reboot
    Step  4  wait_prompt  DUT

run ipmi command "Get Self Test Results"
    Step  1  run ipmi get cmd  DUT  ${cmd_get_self_test_result}  ${rsp_self_test}

run ipmi command "Reset Watchdog Timer"
    Step  1  run ipmi set cmd  DUT  cmd=${cmd_reset_wdt}

run ipmi command "Set Watchdog Timer"
    Step  1  run ipmi set cmd  DUT  cmd=${cmd_set_wdt_1}

run ipmi command "Get Watchdog Timer"
    Step  1  run ipmi get cmd  DUT  ${cmd_get_wdt}  ${rsp_wdt_1}

run ipmi command "Restore Watchdog Timer to default"
    Step  1  run ipmi set cmd  DUT  cmd=${cmd_set_wdt_2}

Set ACPI Power State back to default
    Step  1  run ipmi set cmd  DUT  cmd=${cmd_default_ACPI_power_state}
    Step  2  run ipmi get cmd  DUT  ${cmd_get_ACPI_power_state}  ${rsp_ACPI_power_state_default}

run ipmi command "Set ACPI Power State:soft off"
    Step  1  run ipmi set cmd  DUT  cmd=${cmd_set_ACPI_power_state_soft_off}

run ipmi command "Get ACPI Power State:soft off"
    Step  1  run ipmi set cmd  DUT  cmd=${cmd_set_ACPI_power_state_soft_off}
    Step  2  run ipmi get cmd  DUT  ${cmd_get_ACPI_power_state}  ${rsp_ACPI_power_state_soft_off}

run ipmi command "Set BMC Global enables"
    Step  1  run ipmi set cmd  DUT  cmd=${cmd_set_bmc_global_enables}

run ipmi command "Get BMC Global enables"
    Step  1  run ipmi set cmd  DUT  cmd=${cmd_set_bmc_global_enables}
    Step  2  run ipmi get cmd  DUT  ${cmd_get_bmc_global_enables}  ${rsp_get_bmc_global_enables}

run ipmi command "Clear Message Flags"
    Step  1  run ipmi set cmd  DUT  cmd=${cmd_Clear_Message_Flags}

run ipmi command "Get Message Flags"
    Step  1  run ipmi get cmd  DUT  ${cmd_Get_Message_Flags}  ${rsp_Get_Message_Flags}

run ipmi command "Enable Message Channel Receive"
    Step  1  run ipmi set cmd  DUT  cmd=${cmd_Enable_Message_Channel_Receive}

run ipmi command "Get System GUID"
    Step  1  verify_system_guid  DUT

run ipmi command "Get Channel Authentication capabilities"
    Step  1  run ipmi get cmd  DUT  ${cmd_Get_Channel_Authentication_capabilities}  ${rsp_Get_Channel_Authentication_capabilities}

run ipmi command "Get Session Challenge" by remote ipmitool
    ${bmc_ipv4_ip} =  get_ip_address_from_ipmitool  DUT  eth_type=dedicated
    Step  1  verify_get_session_challenge  DUT  ${bmc_ipv4_ip}  ${bmc_username}  ${bmc_password}

run ipmi command "Set Session Privilege Level" by remote ipmitool
    ${bmc_ipv4_ip} =  get_ip_address_from_ipmitool  DUT  eth_type=dedicated
    Step  1  Keyword Retry  ssh_command_run_ipmi_set_cmd  %{DUT_username_1}  %{DUT_ipv4_ip_1}  %{DUT_password_1}
          ...  ipmitool -H ${bmc_ipv4_ip} -U ${bmc_username} -P ${bmc_password} ${cmd_Set_Session_Privilege_Level}
          ...  ${rsp_Set_Session_Privilege_Level}

run ipmi command "Get Session Info"
    Step  1  run ipmi get cmd  DUT  ${cmd_Get_Session_Info}  ${rsp_Get_Session_Info}

run ipmi command "Get AuthCode"
    ${DUT_ipv4_ip} =  CommonLib.get_ip_address  DUT  -a  mode=CENTOS_MODE
    ${DUT_username} =  get_username_from_config  UUT
    ${DUT_password} =  get_password_from_config  UUT
    Step  1  Keyword Retry  ssh command run ipmi get cmd  ${DUT_username}  ${DUT_ipv4_ip}  ${DUT_password}  ${cmd_Get_AuthCode}  ${tyr_rsp_Get_AuthCode}

run ipmi command "Set Channel Access"
    Step  1  run ipmi set cmd  DUT  cmd=${cmd_Set_Channel_Access}

run ipmi command "Get Channel Access"
    Step  1  run ipmi get cmd  DUT  ${cmd_Get_Channel_Access}  ${rsp_Get_Channel_Access}

run ipmi command "Get Channel Info"
    Step  1  run ipmi get cmd  DUT  ${cmd_Get_Channel_Info}  ${rsp_Get_Channel_Info}

run ipmi command "Set User Access"
    Step  1  run ipmi set cmd  DUT  cmd=${cmd_Set_User_Access}

run ipmi command "Get User Access"
    Step  1  run ipmi get cmd  DUT  ${cmd_Get_User_Access}  ${rsp_Get_User_Access}

run ipmi command "Set User name"
    Step  1  run ipmi set cmd  DUT  cmd=${cmd_Set_User_name}

run ipmi command "Get User name"
    Step  1  run ipmi get cmd  DUT  ${cmd_Get_User_name}  ${rsp_Get_User_name}

run ipmi command "Set User Password"
    Step  1  run ipmi set cmd  DUT  cmd=${cmd_Set_User_Password}

run ipmi command "Get Payload Activation Status"
    Step  1  run ipmi get cmd  DUT  ${cmd_Get_Payload_Activation_Status}  ${rsp_Get_Payload_Activation_Status}

run ipmi command "Get Payload Instance Info"
    Step  1  run ipmi get cmd  DUT  ${cmd_Get_Payload_Instance_Info}  ${rsp_Get_Payload_Instance_Info}

run ipmi command "Set user Payload Access"
    Step  1  run ipmi set cmd  DUT  cmd=${cmd_Set_user_Payload_Access}

run ipmi command "Get user Payload Access"
    Step  1  run ipmi get cmd  DUT  ${cmd_Get_user_Payload_Access}  ${rsp_Get_user_Payload_Access}

run ipmi command "Get channel Payload support"
    Step  1  run ipmi get cmd  DUT  ${cmd_Get_channel_Payload_support}  ${rsp_Get_channel_Payload_support}

run ipmi command "Get channel Payload Version"
    Step  1  run ipmi get cmd  DUT  ${cmd_Get_channel_Payload_Version}  ${rsp_Get_channel_Payload_Version}

run ipmi command "Master Write-Read"
    Step  1  run ipmi get cmd  DUT  ${cmd_Master_Write_Read}  ${rsp_Master_Write_Read}

run ipmi command "Set Channel Security Keys"
    Step  1  run ipmi get cmd  DUT  ${cmd_Set_Channel_Security_Keys}  ${rsp_Set_Channel_Security_Keys}

run ipmi command "Get Chassis Capabilities"
    Step  1  run ipmi get cmd  DUT  ${cmd_Get_Chassis_Capabilities}  ${rsp_Get_Chassis_Capabilities}

run ipmi command "Get Chassis Status"
    Step  1  run ipmi get cmd  DUT  ${cmd_Get_Chassis_Status}  ${rsp_Get_Chassis_Status}

run ipmi command "Set Event Receiver"
    Step  1  run ipmi set cmd  DUT  cmd=${cmd_Set_Event_Receiver}

run ipmi command "Get Event Receiver"
    Step  1  run ipmi get cmd  DUT  ${cmd_Get_Event_Receiver}  ${rsp_Get_Event_Receiver}

run ipmi command "Platform Event Message"
    Step  1  run ipmi set cmd  DUT  cmd=${cmd_Platform_Event_Message}

run ipmi command "Set PEF Configuration Parameters"
    Step  1  run ipmi set cmd  DUT  cmd=${cmd_Set_PEF_Capabilities_1}
    Step  2  run ipmi set cmd  DUT  cmd=${cmd_Set_PEF_Capabilities_2}
    Step  3  run ipmi set cmd  DUT  cmd=${cmd_Set_PEF_Capabilities_3}
    Step  4  run ipmi set cmd  DUT  cmd=${cmd_Set_PEF_Capabilities_4}
    Step  5  run ipmi set cmd  DUT  cmd=${cmd_Set_PEF_Capabilities_5}
    Step  6  run ipmi set cmd  DUT  cmd=${cmd_Set_PEF_Capabilities_6}

run ipmi command "Get PEF Capabilities"
    Step  1  run ipmi get cmd  DUT  ${cmd_Get_PEF_Capabilities}  ${rsp_Get_PEF_Capabilities}

run ipmi command "Disable postpone timer"
    Step  1  run ipmi get cmd  DUT  ${cmd_Disable_postpone_timer}  ${rsp_Disable_postpone_timer}

run ipmi command "arm timer"
    Step  1  run ipmi get cmd  DUT  ${cmd_arm_timer}  ${rsp_arm_timer}

run ipmi command "get present countdown value"
    Step  1  run ipmi get cmd  DUT  ${cmd_get_present_countdown_value}  ${rsp_get_present_countdown_value}

run ipmi command "Set System Boot Options"
    Step  1  run ipmi set cmd  DUT  cmd=${cmd_4_Set_System_Boot_Options}
    Step  2  run ipmi set cmd  DUT  cmd=${cmd_1_Set_System_Boot_Options}
    Step  3  run ipmi set cmd  DUT  cmd=${cmd_2_Set_System_Boot_Options}
    Step  4  run ipmi set cmd  DUT  cmd=${cmd_3_Set_System_Boot_Options}
    Step  5  run ipmi set cmd  DUT  cmd=${cmd_4_Set_System_Boot_Options}
    Step  6  reboot_os  DUT
    Step  7  set time delay  300
    Step  8  send key  DUT  KEY_ENTER  ${1}
    Step  9  send key  DUT  KEY_LEFT  ${1}
    Step  10  verify_menu_bios_setup  DUT  Save Changes and Exit
    Step  11  whitebox exit bios setup  DUT

run ipmi command "Get System Boot Options"
    Step  1  run ipmi set cmd  DUT  cmd=${cmd_4_Set_System_Boot_Options}
    Step  2  run ipmi set cmd  DUT  cmd=${cmd_1_Set_System_Boot_Options}
    Step  3  run ipmi set cmd  DUT  cmd=${cmd_2_Set_System_Boot_Options}
    Step  4  run ipmi set cmd  DUT  cmd=${cmd_3_Set_System_Boot_Options}
    Step  5  run ipmi get cmd  DUT  ${cmd_Get_System_Boot_Options}  ${rsp_Get_System_Boot_Options}
    Step  6  run ipmi set cmd  DUT  cmd=${cmd_default_Set_System_Boot_Options}
    Step  7  run ipmi get cmd  DUT  ${cmd_Get_System_Boot_Options}  ${rsp_default_Get_System_Boot_Options}
    Step  8  run ipmi set cmd  DUT  cmd=${cmd_4_Set_System_Boot_Options}
    Step  9  reboot_os  DUT
    Step  10  set time delay  20
    Step  11  wait_prompt  DUT
    Step  12  whitebox_exec_ping  DUT  %{bmc_ipv4_ip_1}  1  mode=CENTOS_MODE

run ipmi command "Set Power Cycle Interval"
    Step  1  run ipmi set cmd  DUT  cmd=${cmd_Set_Power_Cycle_Interval}
    Step  2  power_cycle_os_by_ipmitool  DUT  ipmitool_cmd=power cycle  mode=local
    Step  3  set time delay  20
    Step  4  wait_prompt  DUT
    Step  5  whitebox_exec_ping  DUT  %{bmc_ipv4_ip_1}  1  mode=CENTOS_MODE
    Step  6  run ipmi set cmd  DUT  cmd=${cmd_Set_bmc_load_default}
    Step  7  set time delay  60
    Step  8  Keyword Retry  power_cycle_os_by_ipmitool  DUT  %{server_username_1}  %{server_ipv4_ip_1}
        ...  %{server_password_1}  %{bmc_ipv4_ip_1}  ipmitool_cmd=power cycle  bmcusername=${bmc_username}
        ...  bmcpassword=${bmc_password}
    Step  9  set time delay  20
    Step  10  wait_prompt  DUT

get all the variables
    ${server_ipv4_ip} =  get_ip_address_from_config  PC
    ${server_username} =  get_username_from_config  PC
    ${server_password} =  get_password_from_config  PC
    ${bmc_ipv4_ip} =  get_ip_address_from_ipmitool  DUT  eth_type=dedicated
    ${DUT_ipv4_ip} =  get_ip_address_from_config  UUT
    ${DUT_username} =  get_username_from_config  UUT
    ${DUT_password} =  get_password_from_config  UUT
    Set Environment Variable  server_ipv4_ip_1  ${server_ipv4_ip}
    Set Environment Variable  bmc_ipv4_ip_1  ${bmc_ipv4_ip}
    Set Environment Variable  server_username_1  ${server_username}
    Set Environment Variable  server_password_1  ${server_password}
    Set Environment Variable  DUT_ipv4_ip_1  ${DUT_ipv4_ip}
    Set Environment Variable  DUT_username_1  ${DUT_username}
    Set Environment Variable  DUT_password_1  ${DUT_password}
    Step  1  whitebox_exec_ping  DUT  %{bmc_ipv4_ip_1}  5  mode=CENTOS_MODE

run ipmi command "Chassis power down"
    Step  1  run ipmi set cmd  DUT  cmd=${cmd_Chassis_power_down}
    Step  2  set time delay  60
    Step  3  Keyword Retry  ssh_command_exec_ping  %{server_username_1}  %{server_ipv4_ip_1}  %{server_password_1}  %{DUT_ipv4_ip_1}  5  loss

run ipmi command "Chassis power up"
    Step  1  Keyword Retry  ssh_command_run_ipmi_set_cmd  %{server_username_1}  %{server_ipv4_ip_1}  %{server_password_1}
            ...  ipmitool -H %{bmc_ipv4_ip_1} -U ${bmc_username} -P ${bmc_password} raw 00 02 01
    Step  2  set time delay  20
    Step  3  wait_prompt  DUT
    Step  4  whitebox_exec_ping  DUT  %{DUT_ipv4_ip_1}  5  mode=CENTOS_MODE
    Step  5  Keyword Retry  ssh_command_exec_ping  %{server_username_1}  %{server_ipv4_ip_1}  %{server_password_1}  %{DUT_ipv4_ip_1}  5

run ipmi command "Chassis power cycle"
    Step  1  Keyword Retry  ssh_command_run_ipmi_set_cmd  %{server_username_1}  %{server_ipv4_ip_1}  %{server_password_1}
            ...  ipmitool -H %{bmc_ipv4_ip_1} -U ${bmc_username} -P ${bmc_password} raw 00 02 02
    Step  2  set time delay  10
    Step  3  Keyword Retry  ssh_command_exec_ping  %{server_username_1}  %{server_ipv4_ip_1}  %{server_password_1}  %{DUT_ipv4_ip_1}  5  loss
    Step  4  set time delay  20
    Step  5  wait_prompt  DUT
    Step  6  whitebox_exec_ping  DUT  %{DUT_ipv4_ip_1}  5  mode=CENTOS_MODE
    Step  7  Keyword Retry  ssh_command_exec_ping  %{server_username_1}  %{server_ipv4_ip_1}  %{server_password_1}  %{DUT_ipv4_ip_1}  5

run ipmi command "Chassis soft shutdown"
    Step  1  Keyword Retry  ssh_command_run_ipmi_set_cmd  %{server_username_1}  %{server_ipv4_ip_1}  %{server_password_1}
            ...  ipmitool -H %{bmc_ipv4_ip_1} -U ${bmc_username} -P ${bmc_password} raw 00 02 05
    Step  2  set time delay  10
    Step  3  Keyword Retry  ssh_command_exec_ping  %{server_username_1}  %{server_ipv4_ip_1}  %{server_password_1}  %{DUT_ipv4_ip_1}  5  loss
    Step  4  Keyword Retry  ssh_command_run_ipmi_set_cmd  %{server_username_1}  %{server_ipv4_ip_1}  %{server_password_1}
            ...  ipmitool -H %{bmc_ipv4_ip_1} -U ${bmc_username} -P ${bmc_password} raw 00 02 01
    Step  5  set time delay  20
    Step  6  wait_prompt  DUT
    Step  7  whitebox_exec_ping  DUT  %{DUT_ipv4_ip_1}  5  mode=CENTOS_MODE
    Step  8  Keyword Retry  ssh_command_exec_ping  %{server_username_1}  %{server_ipv4_ip_1}  %{server_password_1}  %{DUT_ipv4_ip_1}  5

run ipmi command "Get System Restart Cause"
    Step  1  Keyword Retry  power_cycle_os_by_ipmitool  DUT  %{server_username_1}  %{server_ipv4_ip_1}
        ...  %{server_password_1}  %{bmc_ipv4_ip_1}  ipmitool_cmd=power cycle  bmcusername=${bmc_username}
        ...  bmcpassword=${bmc_password}
    Step  2  set time delay  20
    Step  3  wait_prompt  DUT
    Step  4  run ipmi get cmd  DUT  ${cmd_Get_System_Restart_Cause}  ${rsp_Get_System_Restart_Cause}

run ipmi command "Get PEF Configuration Parameters"
    Step  1  run ipmi get cmd  DUT  ${cmd_Get_PEF_Configuration_Parameters_1}  ${rsp_Get_PEF_Configuration_Parameters_1}
    Step  2  run ipmi get cmd  DUT  ${cmd_Get_PEF_Configuration_Parameters_2}  ${rsp_Get_PEF_Configuration_Parameters_2}
    Step  3  run ipmi get cmd  DUT  ${cmd_Get_PEF_Configuration_Parameters_3}  ${rsp_Get_PEF_Configuration_Parameters_3}

run ipmi command "Set Last Processed Event ID"
    Step  1  run ipmi set cmd  DUT  cmd=${cmd_Set_Last_Processed_Event_ID}

run ipmi command "Get Last Processed Event ID"
    Step  1  run ipmi set cmd  DUT  cmd=${cmd_Get_Last_Processed_Event_ID}

run ipmi command "Alert Immediate"
    Step  1  run ipmi set cmd  DUT  cmd=${cmd_Alert_Immediate}

run ipmi command "PET Acknowledge"
    Step  1  run ipmi set cmd  DUT  cmd=${cmd_PET_Acknowledge}

run ipmi command "Set Sensor Hysteresis"
    Step  1  run ipmi set cmd  DUT  cmd=${cmd_Set_Sensor_Hysteresis}

run ipmi command "Get Sensor Hysteresis"
    Step  1  run ipmi get cmd  DUT  ${cmd_Get_Sensor_Hysteresis}  ${rsp_Get_Sensor_Hysteresis}

run ipmi command "Set Sensor Threshold"
    ###lower non-critical|lower critical|lower non-recoverable|upper non-critical|upper critical|upper non-recoverabl
    Step  1  verify_set_sensor_threshold  DUT  ${cmd_Set_Sensor_Threshold_1}
    Step  2  verify_set_sensor_threshold  DUT  ${cmd_Set_Sensor_Threshold_2}

run ipmi command "Get Sensor Threshold"
    ###lower non-critical|lower critical|lower non-recoverable|upper non-critical|upper critical|upper non-recoverabl
    Step  1  verify_get_sensor_threshold  DUT  ${cmd_Get_Sensor_Threshold}  ${rsp_Get_Sensor_Threshold}

run ipmi command "Set Sensor Event Enable"
    Step  1  run ipmi set cmd  DUT  ${cmd_Set_Sensor_Event_Enable}

run ipmi command "Get Sensor Event Enable"
    Step  1  run ipmi get cmd  DUT  ${cmd_Get_Sensor_Event_Enable}  ${rsp_Get_Sensor_Event_Enable}

run ipmi command "Re-arm Sensor Event"
    Step  1  run ipmi set cmd  DUT  ${cmd_Re_arm_Sensor_Event}

run ipmi command "Get Sensor Event Status"
    Step  1  run ipmi get cmd  DUT  ${cmd_Get_Sensor_Event_Status}  ${rsp_Get_Sensor_Event_Status}

run ipmi command "Get Sensor Reading"
    Step  1  verify_get_sensor_reading  DUT  ${cmd_Get_Sensor_Reading}

run ipmi command "Get FRU Inventory Area Info"
    Step  1  run ipmi get cmd  DUT  ${cmd_Get_FRU_Inventory_Area_Info}  ${rsp_Get_FRU_Inventory_Area_Info}

run ipmi command "Read FRU Data"
    Step  1  verify_read_fru_data  DUT

run ipmi command "Write FRU Data"
    Step  1  verify_write_fru_data  DUT  ${cmd_Write_FRU_Inventory_Area_Info}

run ipmi command "Reserve SDR Repository"
    Step  1  run ipmi set cmd  DUT  ${cmd_Reserve_SDR_Repository}

run ipmi command "Get SDR"
    Step  1  run ipmi set cmd  DUT  ${cmd_Get_SDR}

run ipmi command "Partial Add SDR"
    Step  1  verify_partial_add_sdr  DUT  ${cmd_Reserve_SDR_Repository}

run ipmi command "Delete SDR"
    Step  1  run ipmi set cmd  DUT  ${cmd_Delete_SDR}

run ipmi command "Clear SDR Repository"
    Step  1  verify_clear_sdr_repository  DUT  ${cmd_Reserve_SDR_Repository}
    Step  2  update whitebox bmc force  DUT  toolname=${FW_update_tool}  device_type=BMC
        ...  bmcip=%{bmc_ipv4_ip_1}  isUpgrade=True  local=True
    Step  3  Keyword Retry  power_cycle_os_by_ipmitool  DUT  %{server_username_1}  %{server_ipv4_ip_1}
        ...  %{server_password_1}  %{bmc_ipv4_ip_1}  ipmitool_cmd=power cycle  bmcusername=${bmc_username}
        ...  bmcpassword=${bmc_password}
    Step  4  set time delay  20
    Step  5  wait_prompt  DUT
    Step  6  whitebox_lib.verify_fw_version  DUT  device_type=BMC  isUpgrade=True

run ipmi command "Run Initialization Agent"
    Step  1  run ipmi get cmd  DUT  ${cmd_Run_Initialization_Agent}  ${rsp_Run_Initialization_Agent}

run ipmi command "Get SEL Info"
    Step  1  verify_get_sel_info  %{DUT_ipv4_ip_1}  %{DUT_username_1}  %{DUT_password_1}  ${expected_byte1_value}

run ipmi command "Get SEL Allocation Info"
    ### check the return value from byte 1-4
    Step  1  verify_get_sel_allocation_info  DUT  ${cmd_Get_SEL_Allocation_Info}  ${rsp_Get_SEL_Allocation_Info}

run ipmi command "Reserve SEL"
    Step  1  verify_ipmi_set_cmd  DUT  ${cmd_Reserve_SEL}

get DUT variables
    ${DUT_ipv4_ip} =  get_ip_address_from_config  UUT
    ${DUT_username} =  get_username_from_config  UUT
    ${DUT_password} =  get_password_from_config  UUT
    Set Environment Variable  DUT_ipv4_ip_1  ${DUT_ipv4_ip}
    Set Environment Variable  DUT_username_1  ${DUT_username}
    Set Environment Variable  DUT_password_1  ${DUT_password}

run ipmi command "Get SEL Entry"
    Step  1  verify_get_sel_entry  %{DUT_ipv4_ip_1}  %{DUT_username_1}  %{DUT_password_1}

run ipmi command "Add SEL Entry"
    Step  1  run_ipmi_cmd_sel_clear  DUT
    Step  2  verify_add_sel_entry  DUT  %{DUT_ipv4_ip_1}  %{DUT_username_1}  %{DUT_password_1}

run ipmi command "Delete SEL Entry"
    Step  1  verify_add_sel_entry  DUT  %{DUT_ipv4_ip_1}  %{DUT_username_1}  %{DUT_password_1}
    Step  2  verify_delete_sel_entry  DUT  %{DUT_ipv4_ip_1}  %{DUT_username_1}  %{DUT_password_1}

run ipmi command "Clear SEL"
    Step  1  verify_clear_sel  DUT  ${rsp_Clear_SEL}

run ipmi command "Get SEL Time"
    Step  1  verify_get_sel_time  DUT

run ipmi command "Set SEL Time"
    Step  1  verify_set_sel_time  DUT
    Step  2  run_ipmi_cmd_sel_clear  DUT
    Step  3  Keyword Retry  run_ipmi_cmd_reset  DUT  %{DUT_username_1}  %{DUT_ipv4_ip_1}  %{DUT_password_1}
        ...  ${cmd_cold_reset}
    Step  4  Keyword Retry  ssh_command_run_ipmi_set_cmd  %{DUT_username_1}  %{DUT_ipv4_ip_1}  %{DUT_password_1}  reboot
    Step  5  wait_prompt  DUT

run ipmi command "Get SEL Time UTC Offset"
    Step  1  run ipmi get cmd  DUT  ${cmd_Get_SEL_Time_UTC_Offset}  ${rsp_Get_SEL_Time_UTC_Offset}

run ipmi command "Set SEL Time UTC Offset"
    Step  1  verify_set_sel_time_utc_offset  DUT  ${cmd_Set_SEL_Time_UTC_Offset}

run ipmi command "Set LAN Configuration Parameters"
    ${bmc_ipv4_ip} =  get_ip_address_from_ipmitool  DUT  eth_type=dedicated
    Set Environment Variable  bmc_ipv4_ip_1  ${bmc_ipv4_ip}
    Step  1  whitebox_exec_ping  DUT  %{bmc_ipv4_ip_1}  5  mode=CENTOS_MODE
    Step  2  Keyword Retry  delete_arp  DUT  %{bmc_ipv4_ip_1}
    Step  3  verify_set_bmc_lan_arp_respond  DUT  ${cmd_set_bmc_lan_arp_off}  off
    Step  4  whitebox_exec_ping  DUT  %{bmc_ipv4_ip_1}  5  mode=CENTOS_MODE  expected=loss
    Step  5  verify_set_bmc_lan_arp_respond  DUT  ${cmd_set_bmc_lan_arp_on}  on
    Step  6  whitebox_exec_ping  DUT  %{bmc_ipv4_ip_1}  5  mode=CENTOS_MODE

run ipmi command "Get LAN Configuration Parameters"
    Step  1  verify_bmc_lan_info  DUT  ${cmd_ipmitool_lan_print}  ${bmc_lan_1_info}

common upgrade bios check list
    Step  1  verify_bmc_product_id  DUT  ${BMC_Product_ID}
    Step  2  verify_bmc_mac_address  DUT  cmd=ipmitool lan print 1  expected_result=${BMC_lan_print_1_mac_address}
    Step  3  verify_bmc_mac_address  DUT  cmd=ipmitool lan print 8  expected_result=${BMC_lan_print_8_mac_address}
#    Step  4  verify_bmc_voltage_sensor  DUT
#    Step  5  verify_bmc_version  DUT  ${BMC_version}
#    Step  6  verify_bmc_tmp_sensor  DUT
    Step  7  verify_bmc_manufacturer_id  DUT  ${BMC_Manufacturer_ID}
#    Step  8  CPLD version check
    Step  9  check_mac_address  DUT  interface=${management_interface}  expected_result=${eth_mac_addr}
    Step  10  verify_bmc_uuid  DUT  expected_result=${BMC_UUID}
    Step  11  verify_pci_device_number  DUT  expected_result=${pci_device_number}
    Step  12  verify_cmd_output_message  DUT  ipmitool sel list  ${error_messages_list}
    Step  14  verify_processor_model_name  DUT  ${CPU_model_name}
    Step  15  verify_memory_size  DUT  ${memory_size}

common upgrade bmc check list
    Step  1  verify_bmc_product_id  DUT  ${BMC_Product_ID}
    Step  2  verify_bmc_mac_address  DUT  cmd=ipmitool lan print 1  expected_result=${BMC_lan_print_1_mac_address}
    Step  3  verify_bmc_mac_address  DUT  cmd=ipmitool lan print 8  expected_result=${BMC_lan_print_8_mac_address}
#    Step  4  verify_bmc_voltage_sensor  DUT
#    Step  5  verify_bios_version  DUT  bios_version=${BIOS_version}
#    Step  6  verify_bmc_tmp_sensor  DUT
    Step  7  verify_bmc_manufacturer_id  DUT  ${BMC_Manufacturer_ID}
#    Step  8  CPLD version check
    Step  9  check_mac_address  DUT  interface=${management_interface}  expected_result=${eth_mac_addr}
    Step  10  verify_bmc_uuid  DUT  expected_result=${BMC_UUID}
    Step  11  verify_pci_device_number  DUT  expected_result=${pci_device_number}
    Step  12  verify_cmd_output_message  DUT  ipmitool sel list  ${error_messages_list}
    Step  14  verify_processor_model_name  DUT  ${CPU_model_name}
    Step  15  verify_memory_size  DUT  ${memory_size}

CPLD version check
    Step  1  run ipmi get cmd  DUT  ipmitool raw 0x3a 0x4  ${CPLD_version}

Keyword Retry
    [Arguments]    ${keyword}    @{args}    &{config}
    ${result}=    Wait Until Keyword Succeeds    ${G Retry Count}    30s    ${keyword}    @{args}    &{config}
    RETURN    ${result}

check COM0 BIOS settings
    Step  1  run ipmi set cmd  DUT  cmd=${cmd_4_Set_System_Boot_Options}
    Step  2  run ipmi set cmd  DUT  cmd=${cmd_1_Set_System_Boot_Options}
    Step  3  run ipmi set cmd  DUT  cmd=${cmd_2_Set_System_Boot_Options}
    Step  4  run ipmi set cmd  DUT  cmd=${cmd_3_Set_System_Boot_Options}
    Step  5  run ipmi set cmd  DUT  cmd=${cmd_4_Set_System_Boot_Options}
    Step  6  reboot_os  DUT
    Step  7  set time delay  300
    Step  8  whitebox_enter_bios_setup  DUT  ${bios_password}
    Step  9  send key  DUT  KEY_RIGHT  ${1}
    Step  10  send key  DUT  KEY_DOWN  ${1}
    Step  11  verify_com0_bios_setting  DUT  Enabled  ${COM0_baud_rate}
    Step  12  send key  DUT  KEY_ESC  ${2}
    Step  13  whitebox exit bios setup  DUT
    Step  14  set time delay  180

check COM0 baud rate under OS
    Step  1  Keyword Retry  verify_serial_port_baud_rate  %{server_username_1}  %{server_ipv4_ip_1}  %{server_password_1}
        ...  %{bmc_ipv4_ip_1}  ${bmc_username}  ${bmc_password}  ${COM0_baud_rate}

Enter command to active SOL
    Step  1  verify sol function  %{server_ipv4_ip_1}  %{server_username_1}  %{server_password_1}  %{bmc_ipv4_ip_1}
        ...  ${bmc_username}  ${bmc_password}  %{DUT_username_1}  %{DUT_password_1}
    Step  2  Keyword Retry  power_cycle_os_by_ipmitool  DUT  %{server_username_1}  %{server_ipv4_ip_1}
        ...  %{server_password_1}  %{bmc_ipv4_ip_1}  ipmitool_cmd=power cycle  bmcusername=${bmc_username}
        ...  bmcpassword=${bmc_password}
    Step  3  set time delay  20
    Step  4  wait_prompt  DUT
    Step  5  verify sol function  %{server_ipv4_ip_1}  %{server_username_1}  %{server_password_1}  %{bmc_ipv4_ip_1}
        ...  ${bmc_username}  ${bmc_password}  %{DUT_username_1}  %{DUT_password_1}
    Step  6  Keyword Retry  ssh_command_run_ipmi_set_cmd  %{server_username_1}  %{server_ipv4_ip_1}  %{server_password_1}
            ...  ipmitool -H %{bmc_ipv4_ip_1} -U ${bmc_username} -P ${bmc_password} sel clear
    Step  7  Keyword Retry  run_ipmi_cmd_reset  DUT  %{DUT_username_1}  %{DUT_ipv4_ip_1}  %{DUT_password_1}
        ...  ${cmd_cold_reset}
    Step  8  set time delay  90
    Step  9  verify sol function  %{server_ipv4_ip_1}  %{server_username_1}  %{server_password_1}  %{bmc_ipv4_ip_1}
        ...  ${bmc_username}  ${bmc_password}  %{DUT_username_1}  %{DUT_password_1}
    Step  10  Keyword Retry  ssh_command_run_ipmi_set_cmd  %{server_username_1}  %{server_ipv4_ip_1}  %{server_password_1}
        ...  ipmitool -H %{bmc_ipv4_ip_1} -U ${bmc_username} -P ${bmc_password} raw 0x32 0x66
    Step  11  set time delay  90
    Step  12  Keyword Retry  power_cycle_os_by_ipmitool  DUT  %{server_username_1}  %{server_ipv4_ip_1}
        ...  %{server_password_1}  %{bmc_ipv4_ip_1}  ipmitool_cmd=power cycle  bmcusername=${bmc_username}
        ...  bmcpassword=${bmc_password}
    Step  13  set time delay  20
    Step  14  wait_prompt  DUT

fix SOL's activation causing serial port problem
    Step  1  Keyword Retry  ssh_command_run_ipmi_set_cmd  %{server_username_1}  %{server_ipv4_ip_1}  %{server_password_1}
        ...  ipmitool -H %{bmc_ipv4_ip_1} -U ${bmc_username} -P ${bmc_password} raw 0x32 0x66
    Step  2  set time delay  90
    Step  3  Keyword Retry  power_cycle_os_by_ipmitool  DUT  %{server_username_1}  %{server_ipv4_ip_1}
        ...  %{server_password_1}  %{bmc_ipv4_ip_1}  ipmitool_cmd=power cycle  bmcusername=${bmc_username}
        ...  bmcpassword=${bmc_password}
    Step  4  set time delay  20
    Step  5  wait_prompt  DUT
    Step  6  whitebox_exec_ping  DUT  %{bmc_ipv4_ip_1}  5  mode=CENTOS_MODE

User Name and Password Check
    Step  1  Keyword Retry  verify_current_bmc_user  %{DUT_username_1}  %{DUT_ipv4_ip_1}  %{DUT_password_1}  %{bmc_ipv4_ip_1}
        ...  ${rsp_device_id}
    Step  2  Keyword Retry  verify_add_bmc_user  DUT  %{server_username_1}  %{server_ipv4_ip_1}  %{server_password_1}  %{bmc_ipv4_ip_1}
        ...  test3  qwsd23  3  ${rsp_device_id}  new_username=tester3
    Step  3  Keyword Retry  verify_add_bmc_user  DUT  %{server_username_1}  %{server_ipv4_ip_1}  %{server_password_1}  %{bmc_ipv4_ip_1}
        ...  test4  qwsd24  4  ${rsp_device_id}  new_username=tester4
    Step  4  Keyword Retry  verify_add_bmc_user  DUT  %{server_username_1}  %{server_ipv4_ip_1}  %{server_password_1}  %{bmc_ipv4_ip_1}
        ...  test5  qwsd25  5  ${rsp_device_id}  new_username=tester5
    Step  5  Keyword Retry  verify_add_bmc_user  DUT  %{server_username_1}  %{server_ipv4_ip_1}  %{server_password_1}  %{bmc_ipv4_ip_1}
        ...  test6  qwsd26  6  ${rsp_device_id}  new_username=tester6
    Step  6  Keyword Retry  verify_add_bmc_user  DUT  %{server_username_1}  %{server_ipv4_ip_1}  %{server_password_1}  %{bmc_ipv4_ip_1}
        ...  test7  qwsd27  7  ${rsp_device_id}  new_username=tester7
    Step  7  Keyword Retry  verify_add_bmc_user  DUT  %{server_username_1}  %{server_ipv4_ip_1}  %{server_password_1}  %{bmc_ipv4_ip_1}
        ...  test8  qwsd28  8  ${rsp_device_id}  new_username=tester8
    Step  8  Keyword Retry  verify_add_bmc_user  DUT  %{server_username_1}  %{server_ipv4_ip_1}  %{server_password_1}  %{bmc_ipv4_ip_1}
        ...  test9  qwsd29  9  ${rsp_device_id}  new_username=tester9
    Step  9  Keyword Retry  verify_add_bmc_user  DUT  %{server_username_1}  %{server_ipv4_ip_1}  %{server_password_1}  %{bmc_ipv4_ip_1}
        ...  test10  qwsd210  10  ${rsp_device_id}  new_username=tester10
    Step  10  Keyword Retry  modify_bmc_user_name  DUT  %{DUT_username_1}  %{DUT_ipv4_ip_1}  %{DUT_password_1}
    Step  11  Keyword Retry  run_ipmi_cmd_sel_clear  DUT
    Step  12  Keyword Retry  Keyword Retry  run_ipmi_cmd_reset  DUT  %{DUT_username_1}  %{DUT_ipv4_ip_1}  %{DUT_password_1}
        ...  ${cmd_warm_reset}
    Step  13  set time delay  90
    Step  14  Keyword Retry  verify_bmc_user_count  %{DUT_username_1}  %{DUT_ipv4_ip_1}  %{DUT_password_1}
    Step  15  Keyword Retry  ssh_command_run_ipmi_set_cmd  %{server_username_1}  %{server_ipv4_ip_1}  %{server_password_1}
        ...  ipmitool -H %{bmc_ipv4_ip_1} -U ${bmc_username} -P ${bmc_password} raw 0x32 0x66
    Step  16  set time delay  90
    Step  17  Keyword Retry  power_cycle_os_by_ipmitool  DUT  %{server_username_1}  %{server_ipv4_ip_1}
        ...  %{server_password_1}  %{bmc_ipv4_ip_1}  ipmitool_cmd=power cycle  bmcusername=${bmc_username}
        ...  bmcpassword=${bmc_password}
    Step  18  set time delay  20
    Step  19  wait_prompt  DUT
    Step  20  whitebox_exec_ping  DUT  %{bmc_ipv4_ip_1}  5  mode=CENTOS_MODE

SMASH CLP Command Check
    Step  1  Keyword Retry  verify_smash_clp_command_help  ${bmc_username}  %{bmc_ipv4_ip_1}  ${bmc_password}

Power Control Check
    Step  1  run_ipmi_cmd_sel_clear  DUT
    Step  2  verify_whitebox_power_control  %{server_username_1}  %{server_ipv4_ip_1}
        ...  %{server_password_1}  %{bmc_ipv4_ip_1}  ${bmc_username}  ${bmc_password}  power off
    Step  3  verify_whitebox_power_status  %{server_username_1}  %{server_ipv4_ip_1}
        ...  %{server_password_1}  %{bmc_ipv4_ip_1}  ${bmc_username}  ${bmc_password}  off
    Step  4  check_sel_list_unexpect_event  %{server_username_1}  %{server_ipv4_ip_1}  %{server_password_1}
        ...  %{bmc_ipv4_ip_1}  ${bmc_username}  ${bmc_password}  ${error_messages_list}
    Step  5  Keyword Retry  ssh_command_run_ipmi_set_cmd  %{server_username_1}  %{server_ipv4_ip_1}  %{server_password_1}
            ...  ipmitool -H %{bmc_ipv4_ip_1} -U ${bmc_username} -P ${bmc_password} sel clear
    Step  6  verify_whitebox_power_control  %{server_username_1}  %{server_ipv4_ip_1}
        ...  %{server_password_1}  %{bmc_ipv4_ip_1}  ${bmc_username}  ${bmc_password}  power on
    Step  7  verify_whitebox_power_status  %{server_username_1}  %{server_ipv4_ip_1}
        ...  %{server_password_1}  %{bmc_ipv4_ip_1}  ${bmc_username}  ${bmc_password}  on
    Step  8  set time delay  20
    Step  10  wait_prompt  DUT
    Step  11  check_sel_list_unexpect_event  %{server_username_1}  %{server_ipv4_ip_1}  %{server_password_1}
        ...  %{bmc_ipv4_ip_1}  ${bmc_username}  ${bmc_password}  ${error_messages_list}
    Step  12  run_ipmi_cmd_sel_clear  DUT
    Step  13  verify_whitebox_power_control  %{server_username_1}  %{server_ipv4_ip_1}
        ...  %{server_password_1}  %{bmc_ipv4_ip_1}  ${bmc_username}  ${bmc_password}  power cycle
    Step  14  set time delay  20
    Step  15  wait_prompt  DUT
    Step  16  check_sel_list_unexpect_event  %{server_username_1}  %{server_ipv4_ip_1}  %{server_password_1}
        ...  %{bmc_ipv4_ip_1}  ${bmc_username}  ${bmc_password}  ${error_messages_list}
    Step  17  Keyword Retry  ssh_command_run_ipmi_set_cmd  %{server_username_1}  %{server_ipv4_ip_1}  %{server_password_1}
            ...  ipmitool -H %{bmc_ipv4_ip_1} -U ${bmc_username} -P ${bmc_password} sel clear
    Step  18  verify_whitebox_power_control  %{server_username_1}  %{server_ipv4_ip_1}
        ...  %{server_password_1}  %{bmc_ipv4_ip_1}  ${bmc_username}  ${bmc_password}  hard reset
    Step  19  set time delay  20
    Step  20  wait_prompt  DUT
    Step  21  check_sel_list_unexpect_event  %{server_username_1}  %{server_ipv4_ip_1}  %{server_password_1}
        ...  %{bmc_ipv4_ip_1}  ${bmc_username}  ${bmc_password}  ${error_messages_list}
    Step  22  run_ipmi_cmd_sel_clear  DUT
    Step  22  verify_whitebox_power_control  %{server_username_1}  %{server_ipv4_ip_1}
        ...  %{server_password_1}  %{bmc_ipv4_ip_1}  ${bmc_username}  ${bmc_password}  soft shutdown
    Step  23  check_sel_list_unexpect_event  %{server_username_1}  %{server_ipv4_ip_1}  %{server_password_1}
        ...  %{bmc_ipv4_ip_1}  ${bmc_username}  ${bmc_password}  ${error_messages_list}
    Step  24  verify_whitebox_power_control  %{server_username_1}  %{server_ipv4_ip_1}
        ...  %{server_password_1}  %{bmc_ipv4_ip_1}  ${bmc_username}  ${bmc_password}  power on
    Step  25  verify_whitebox_power_status  %{server_username_1}  %{server_ipv4_ip_1}
        ...  %{server_password_1}  %{bmc_ipv4_ip_1}  ${bmc_username}  ${bmc_password}  on
    Step  26  set time delay  20
    Step  27  wait_prompt  DUT

modify bmc lan static&dhcp function
    Step  1  modify_bmc_lan_ipsrc  DUT  ${lan_id}  ${ipsrc_mode_1}
    Step  2  modify_bmc_lan_ipaddr  DUT  ${lan_id}  ${ipaddr}
    Step  3  modify_bmc_lan_netmask  DUT  ${lan_id}  ${netmask}
    Step  4  ssh_command_ping  %{server_username_1}  %{server_ipv4_ip_1}  %{server_password_1}  ${ipaddr}  ${ping_count}
    Step  5  modify_bmc_lan_ipsrc  DUT  ${lan_id}  ${ipsrc_mode_2}
    Step  6  set time delay  60
    ${bmc_ipaddr} =  get_ip_address_from_ipmitool  DUT  eth_type=shared
    Step  7  ssh_command_ping  %{server_username_1}  %{server_ipv4_ip_1}  %{server_password_1}  ${bmc_ipaddr}  5

check BMC POH status after BMC FW update
    Step  1  set time delay  1800
    FOR    ${INDEX}    IN RANGE    1    ${MaxLoopNum}
        Print Loop Info  ${INDEX}
        ${time_before} =  get_poh_counter  DUT
        Step  1  whitebox_lib.online_update_bmc  DUT  toolname=${FW_update_tool}  bmcip=%{bmc_ipv4_ip_1}  isUpgrade=True  local=True
        Step  2  set time delay  90
        Step  3  Keyword Retry  power_cycle_os_by_ipmitool  DUT  %{server_username_1}  %{server_ipv4_ip_1}
            ...  %{server_password_1}  %{bmc_ipv4_ip_1}  ipmitool_cmd=power cycle  bmcusername=${bmc_username}
            ...  bmcpassword=${bmc_password}
        Step  4  set time delay  20
        Step  5  wait_prompt  DUT
        ${time_after} =  get_poh_counter  DUT
        Step  6  verify_poh_counter  ${time_before}  ${time_after}
    END

Check BMC SSL Cipher Version
    verify_bmc_ssl_cipher_version  DUT  %{bmc_ipv4_ip_1}

Check BMC Suite ID Test
    Step  1  verify_bmc_suite_id_test  %{server_username_1}  %{server_ipv4_ip_1}  %{server_password_1}  %{bmc_ipv4_ip_1}
        ...  ${bmc_username}  ${bmc_password}  ${rsp_device_id}  ${support_suite_id}  ${unsupport_suite_id}

Check BMC dedicate and share port ping stress
    ${bmc_ipv4_ip_share_port} =  get_ip_address_from_ipmitool  DUT  eth_type=shared
    Set Environment Variable  bmc_ipv4_ip_2  ${bmc_ipv4_ip_share_port}
    Step  1  verify_ssh_ping_function  %{server_username_1}  %{server_ipv4_ip_1}  %{server_password_1}
        ...  %{bmc_ipv4_ip_1}  ping_timeout=${ping_timeout}
    Step  2  verify_ssh_ping_function  %{server_username_1}  %{server_ipv4_ip_1}  %{server_password_1}
        ...  %{bmc_ipv4_ip_2}  ping_timeout=${ping_timeout}

check KCS Function
    ### Power On(always-on)|Power Off(always-off)|Last State(previous)
    ${original_power_restore_policy} =  get_bmc_power_restore_policy  DUT
    Step  1  verify_kcs_function  DUT  ${device_id}  ${BMC_Product_ID}  ${bios_password}
    Step  2  verify_bios_power_restore_policy  DUT  ${original_power_restore_policy}
    Step  3  modify_bios_power_restore_policy  DUT  ${modified_power_restore_policy}
    Step  4  verify_bmc_power_restore_policy  DUT  ${modified_power_restore_policy}
    Step  5  verify_kcs_function  DUT  ${device_id}  ${BMC_Product_ID}  ${bios_password}
    Step  6  verify_bios_power_restore_policy  DUT  ${modified_power_restore_policy}
    Step  7  modify_bios_power_restore_policy  DUT  ${original_power_restore_policy}
    Step  8  verify_bmc_power_restore_policy  DUT  ${original_power_restore_policy}

check BMC Version after mc reset cold
    Step  1  Keyword Retry  ssh_command_verify_bmc_version  %{server_username_1}  %{server_ipv4_ip_1}  %{server_password_1}
            ...  %{bmc_ipv4_ip_1}  ${bmc_username}  ${bmc_password}  ${remote}  ${BMC_version}
    Step  2  Keyword Retry  ssh_command_verify_bmc_product_id  %{server_username_1}  %{server_ipv4_ip_1}  %{server_password_1}
            ...  %{bmc_ipv4_ip_1}  ${bmc_username}  ${bmc_password}  ${remote}  ${BMC_Product_ID}
    Step  3  Keyword Retry  ssh_command_verify_mc_reset  %{server_username_1}  %{server_ipv4_ip_1}  %{server_password_1}
            ...  %{bmc_ipv4_ip_1}  ${bmc_username}  ${bmc_password}  ${remote}  cold
    Step  4  set time delay  180
    Step  5  Keyword Retry  ssh_command_verify_bmc_version  %{server_username_1}  %{server_ipv4_ip_1}  %{server_password_1}
            ...  %{bmc_ipv4_ip_1}  ${bmc_username}  ${bmc_password}  ${remote}  ${BMC_version}
    Step  6  Keyword Retry  ssh_command_verify_bmc_product_id  %{server_username_1}  %{server_ipv4_ip_1}  %{server_password_1}
            ...  %{bmc_ipv4_ip_1}  ${bmc_username}  ${bmc_password}  ${remote}  ${BMC_Product_ID}

check BMC Version after mc reset warm
    Step  1  Keyword Retry  ssh_command_verify_bmc_version  %{server_username_1}  %{server_ipv4_ip_1}  %{server_password_1}
            ...  %{bmc_ipv4_ip_1}  ${bmc_username}  ${bmc_password}  ${remote}  ${BMC_version}
    Step  2  Keyword Retry  ssh_command_verify_bmc_product_id  %{server_username_1}  %{server_ipv4_ip_1}  %{server_password_1}
            ...  %{bmc_ipv4_ip_1}  ${bmc_username}  ${bmc_password}  ${remote}  ${BMC_Product_ID}
    Step  3  Keyword Retry  ssh_command_verify_mc_reset  %{server_username_1}  %{server_ipv4_ip_1}  %{server_password_1}
            ...  %{bmc_ipv4_ip_1}  ${bmc_username}  ${bmc_password}  ${remote}  warm
    Step  4  set time delay  180
    Step  5  Keyword Retry  ssh_command_verify_bmc_version  %{server_username_1}  %{server_ipv4_ip_1}  %{server_password_1}
            ...  %{bmc_ipv4_ip_1}  ${bmc_username}  ${bmc_password}  ${remote}  ${BMC_version}
    Step  6  Keyword Retry  ssh_command_verify_bmc_product_id  %{server_username_1}  %{server_ipv4_ip_1}  %{server_password_1}
            ...  %{bmc_ipv4_ip_1}  ${bmc_username}  ${bmc_password}  ${remote}  ${BMC_Product_ID}

User Privilege Check
    ###0h=reserved  1h=CALLBACK level  2h=USER level  3h=OPERATOR level  4h=ADMINISTRATOR level  5h=OEM Proprietary level
    Step  1  verify_get_privilege  DUT  ${cmd_Get_Channel_Access}  ${expected_level}
    Step  2  verify_user_privilege  DUT  %{bmc_ipv4_ip_1}

Check BMC API Call Test
    ${bmc_ipv4_ip} =  get_ip_address_from_ipmitool  DUT  eth_type=dedicated
    Step  1  verify_bmc_api_call_test  DUT  curl -k -d "username=${bmc_username}&password=${bmc_password}" https://${bmc_ipv4_ip}/api/session
    Step  2  verify_bmc_api_call_test  DUT  curl -k -d "username=${bmc_username}&password=${bmc_password}" https://${bmc_ipv4_ip}/api/session123  invalid

Check Web Session ID
    ${bmc_ipv4_ip} =  get_ip_address_from_ipmitool  DUT  eth_type=dedicated
    ${cmd1_Web_Session_ID}=  get_web_session_id  DUT  curl -k -d "username=${bmc_username}&password=${bmc_password}" -v -X POST https://${bmc_ipv4_ip}/api/session
    ${cmd2_Web_Session_ID}=  get_web_session_id  DUT  curl -k -d "username=${bmc_username}&password=${bmc_password}" -v -X POST https://${bmc_ipv4_ip}/api/session
    Step  1  verify_web_session_ID  ${cmd1_Web_Session_ID}  ${cmd2_Web_Session_ID}

OS Connect Device
    Step  1  OSConnect
    Step  2  set_root_hostname  DUT
    Step  3  check_bmc_ip_normal  DUT

OS Disconnect Device
    OSDisconnect

End User Operation Test
    OS Connect Device
    FOR  ${num}  IN RANGE  3  17
        del_user_info  DUT  ${num}
    END
    OS Disconnect Device

End User Privilege Test
    OS Connect Device
    independent_step  1  del_user_info  DUT  3
    OS Disconnect Device

End LAN Configuration Test
    OS Connect Device
    independent_step  1  set_power_status  DUT  cycle  connection=True
    independent_step  2  set_bmc_ip_status  DUT  dhcp
    independent_step  3  Set_wait  120
    independent_step  4  set_os_ip_by_dhclient  DUT
    OS Disconnect Device

End AC Disconnect
    OS Connect Device
    independent_step  1  set_pdu_status_connect_os  DUT  reboot  ${pdu_port}  400  100
    independent_step  2  connect  DUT
    OS Disconnect Device


End Online Update Test with HPM
    OS Connect Device
    independent_step  1  update_bmc_by_hpm  DUT  now  ${bmc_ip}
    independent_step  2  set_wait  220
    independent_step  3  set_update_bmc_primary_backup  DUT
    independent_step  4  update_bmc_by_hpm  DUT  now  ${bmc_ip}
    independent_step  5  set_wait  220
    independent_step  6  check_communication_lan_pc  DUT
    independent_step  7  set_fw_boot_selector  DUT  1
    independent_step  8  set_reset_type  DUT  ${cmd_ipmitool_mc_reset_cold}  cold  False
    OS Disconnect Device

End BMC Firmware Boot Up
    OS Connect Device
    independent_step  1  set_fw_boot_selector  DUT  1
    independent_step  2  set_reset_type  DUT  ${cmd_ipmitool_mc_reset_cold}  cold  False
    independent_step  3  check_current_active_image  DUT  01
    OS Disconnect Device

End Switch BIOS Chip Selector
    OS Connect Device
    independent_step  1  set_bios_boot_selector  DUT
    independent_step  2  set_power_status  DUT  cycle  connection=True
    OS Disconnect Device

End Bmc Online Update Test
    OS Connect Device
    independent_step  1  set_pdu_status_connect_os  DUT  reboot  ${pdu_port}  600  100
    independent_step  2  set_fw_boot_selector  DUT  2
    independent_step  3  set_reset_type  DUT  ${cmd_ipmitool_mc_reset_cold}  cold  False
    independent_step  4  set_bmc_virtual_usb_device  DUT
    independent_step  5  update_by_cfu  DUT  bmc  False  now
    independent_step  6  set_fw_boot_selector  DUT  1
    independent_step  7  set_reset_type  DUT  ${cmd_ipmitool_mc_reset_cold}  cold  False
    independent_step  8  update_by_cfu  DUT  bmc  True  now
    OS Disconnect Device

End CPLD Update Test
    OS Connect Device
    independent_step  1  set_pdu_status_connect_os  DUT  reboot  ${pdu_port}  600  100
    independent_step  2  set_bmc_virtual_usb_device  DUT
    independent_step  3  update_by_cfu  DUT  cpld  version=now  update_time=1200
    independent_step  4  set_pdu_status_connect_os  DUT  reboot  ${pdu_port}  600  100
    OS Disconnect Device

End BIOS Update Test
    OS Connect Device
    independent_step  1  set_pdu_status_connect_os  DUT  reboot  ${pdu_port}  600  100
    independent_step  2  set_bmc_virtual_usb_device  DUT
    independent_step  3  set_start_bios_primary_backup  DUT  False
    independent_step  4  set_power_status  DUT  cycle  connection=True
    # independent_step  5  set_update_bios_primary_backup  DUT  False
    independent_step  6  update_by_cfu  DUT  bios  version=now  update_time=480
    independent_step  7  set_pdu_status_connect_os  DUT  reboot  ${pdu_port}  600  100
    independent_step  8  set_start_bios_primary_backup  DUT
    independent_step  9  set_power_status  DUT  cycle  connection=True
    # independent_step  10  set_update_bios_primary_backup  DUT
    independent_step  11  update_by_cfu  DUT  bios  version=now  update_time=480
    independent_step  12  set_pdu_status_connect_os  DUT  reboot  ${pdu_port}  600  100
    OS Disconnect Device

End PEF Configuration Test
    OS Connect Device
    independent_step  1  send_cmd  DUT  ${cmd_Set_PEF_Capabilities_1}
    independent_step  2  set_pef_config  DUT  01   ${rsp_Get_PEF_Configuration_Parameters_2}
    independent_step  3  set_pef_config  DUT  02   ${rsp_Get_PEF_Configuration_Parameters_3}
    independent_step  4  set_pef_config  DUT  06   ${rsp_Get_PEF_Configuration_Parameters_4}
    independent_step  5  set_pef_config  DUT  09   ${rsp_Get_PEF_Configuration_Parameters_5}
    independent_step  6  send_cmd  DUT  ${cmd_Set_PEF_Capabilities_6}
    independent_step  7  set_pef_filter_close  DUT  all
    OS Disconnect Device

End Extensional I2C Master Write Read
    OS Connect Device
    independent_step  1  set_fan_scan_status  DUT
    OS Disconnect Device

END KCS Interface Test
    OS Connect Device
    independent_step  1  set_pdu_status_connect_os  DUT  reboot  ${pdu_port}  400  120
    independent_step  2  connect  DUT
    independent_step  3  set_bmc_ip_status  DUT  dhcp
    independent_step  4  set_wait  80
    OS Disconnect Device

# 11.1.2 	Online Update Test via USB
run update bmc by cfu to high primary usb
    ${ip}  get_ip_address_from_ipmitool  DUT
    ${version_pr_old}  get_bmc_version  DUT  mc_info=True
    independent_step  1.1  set_bmc_virtual_usb_device  DUT
    independent_step  1.2  set_sel_clear  DUT
    independent_step  2  update_by_cfu  DUT  bmc
    independent_step  3  set_bmc_virtual_usb_device  DUT  False
    ${version_pr_new}  get_bmc_version  DUT  mc_info=True
    independent_step  4  check_info_equal  ${version_pr_old}  ${version_pr_new}  False
    independent_step  5  check_reset_sel_info  DUT
    ${version_pr_again_1}  get_bmc_version  DUT  mc_info=True
    independent_step  6  check_info_equal  ${version_pr_again_1}  ${version_pr_new}
    independent_step  7  set_reset_type  DUT  ${cmd_ipmitool_mc_reset_cold}  cold  True
    ${version_pr_again_2}  get_bmc_version  DUT  mc_info=True
    independent_step  8  check_info_equal  ${version_pr_again_2}  ${version_pr_again_1}

run update bmc by cfu to lower primary usb
    ${ip}  get_ip_address_from_ipmitool  DUT
    ${version_pr_old}  get_bmc_version  DUT  mc_info=True
    independent_step  1  set_bmc_virtual_usb_device  DUT
    independent_step  2  set_sel_clear  DUT
    independent_step  3  update_by_cfu  DUT  bmc  version=old
    independent_step  4  set_bmc_virtual_usb_device  DUT  False
    ${version_pr_now_old}  get_bmc_version  DUT  mc_info=True
    independent_step  5  check_info_equal  ${version_pr_old}  ${version_pr_now_old}  False
    independent_step  6  check_reset_sel_info  DUT
    ${version_pr_again_3}  get_bmc_version  DUT  mc_info=True
    independent_step  7  check_info_equal  ${version_pr_again_3}  ${version_pr_now_old}
    independent_step  8  set_reset_type  DUT  ${cmd_ipmitool_mc_reset_cold}  cold  True
    ${version_pr_again_4}  get_bmc_version  DUT  mc_info=True
    independent_step  9  check_info_equal  ${version_pr_again_3}  ${version_pr_again_4}

run update bmc by cfu to high backup usb
    ${ip}  get_ip_address_from_ipmitool  DUT
    ${version_bk_old}  get_bmc_version  DUT  mc_info=True
    independent_step  1  set_bmc_virtual_usb_device  DUT
    independent_step  2  set_sel_clear  DUT
    independent_step  3  update_by_cfu  DUT  bmc  False  now
    independent_step  4  set_bmc_virtual_usb_device  DUT  False
    ${version_bk_now_old}  get_bmc_version  DUT  mc_info=True
    independent_step  5  check_info_equal  ${version_bk_old}  ${version_bk_now_old}  False
    independent_step  6  check_reset_sel_info  DUT
    ${version_bk_again_3}  get_bmc_version  DUT  mc_info=True
    independent_step  7  check_info_equal  ${version_bk_again_3}  ${version_bk_now_old}
    independent_step  8  set_reset_type  DUT  ${cmd_ipmitool_mc_reset_cold}  cold  True
    ${version_bk_again_4}  get_bmc_version  DUT  mc_info=True
    independent_step  9  check_info_equal  ${version_bk_again_3}  ${version_bk_again_4}

run update bmc by cfu to lower backup usb
    ${ip}  get_ip_address_from_ipmitool  DUT
    ${version_bk_old}  get_bmc_version  DUT  mc_info=True
    independent_step  1  set_bmc_virtual_usb_device  DUT
    independent_step  2  set_sel_clear  DUT
    independent_step  3  update_by_cfu  DUT  bmc  False  old
    independent_step  4  set_bmc_virtual_usb_device  DUT  False
    ${version_bk_now_old}  get_bmc_version  DUT  mc_info=True
    independent_step  5  check_info_equal  ${version_bk_old}  ${version_bk_now_old}  False
    independent_step  6  check_reset_sel_info  DUT
    ${version_bk_again_3}  get_bmc_version  DUT  mc_info=True
    independent_step  7  check_info_equal  ${version_bk_again_3}  ${version_bk_now_old}
    independent_step  8  set_reset_type  DUT  ${cmd_ipmitool_mc_reset_cold}  cold  True
    ${version_bk_again_4}  get_bmc_version  DUT  mc_info=True
    independent_step  9  check_info_equal  ${version_bk_again_3}  ${version_bk_again_4}

# 11.1.3 	Online Update Test via LAN
run update bmc by cfu to high primary lan
    ${ip}  get_ip_address_from_ipmitool  DUT
    ${version_pr_old}  get_bmc_version  DUT  ip=${ip}  mc_info=True
    independent_step  1.1  set_bmc_virtual_usb_device  DUT  ip=${ip}
    independent_step  1.2  set_sel_clear  DUT  ${ip}
    independent_step  2  update_by_cfu  DUT  bmc  bmc_ip=${ip}
    ${ip}  get_ip_address_from_ipmitool  DUT
    independent_step  3  set_bmc_virtual_usb_device  DUT  False  ${ip}
    ${version_pr_new}  get_bmc_version  DUT  ip=${ip}  mc_info=True
    independent_step  4  check_info_equal  ${version_pr_old}  ${version_pr_new}  False
    independent_step  5  check_reset_sel_info  DUT  ${ip}
    ${version_pr_again_1}  get_bmc_version  DUT  ip=${ip}  mc_info=True
    independent_step  6  check_info_equal  ${version_pr_again_1}  ${version_pr_new}
    independent_step  7  set_reset_type  DUT  ${cmd_ipmitool_mc_reset_cold}  cold  True
    ${version_pr_again_2}  get_bmc_version  DUT  ip=${ip}  mc_info=True
    independent_step  8  check_info_equal  ${version_pr_again_2}  ${version_pr_again_1}

run update bmc by cfu to lower primary lan
    ${ip}  get_ip_address_from_ipmitool  DUT
    ${version_pr_old}  get_bmc_version  DUT  ip=${ip}  mc_info=True
    independent_step  1  set_bmc_virtual_usb_device  DUT  ip=${ip}
    independent_step  2  set_sel_clear  DUT  ${ip}
    independent_step  3  update_by_cfu  DUT  bmc  version=old  bmc_ip=${ip}
    ${ip}  get_ip_address_from_ipmitool  DUT
    independent_step  4  set_bmc_virtual_usb_device  DUT  False  ${ip}
    ${version_pr_now_old}  get_bmc_version  DUT  ip=${ip}  mc_info=True
    independent_step  5  check_info_equal  ${version_pr_old}  ${version_pr_now_old}  False
    independent_step  7  check_reset_sel_info  DUT  ip=${ip}
    ${version_pr_again_3}  get_bmc_version  DUT  ip=${ip}  mc_info=True
    independent_step  7  check_info_equal  ${version_pr_again_3}  ${version_pr_now_old}
    independent_step  8  set_reset_type  DUT  ${cmd_ipmitool_mc_reset_cold}  cold  True
    ${version_pr_again_4}  get_bmc_version  DUT  ip=${ip}  mc_info=True
    independent_step  9  check_info_equal  ${version_pr_again_3}  ${version_pr_again_4}

run update bmc by cfu to high backup lan
    ${ip}  get_ip_address_from_ipmitool  DUT
    ${version_bk_old}  get_bmc_version  DUT  ip=${ip}  mc_info=True
    independent_step  1  set_bmc_virtual_usb_device  DUT  ip=${ip}
    independent_step  2  set_sel_clear  DUT  ${ip}
    independent_step  3  update_by_cfu  DUT  bmc  False  now  bmc_ip=${ip}
    ${ip}  get_ip_address_from_ipmitool  DUT
    independent_step  4  set_bmc_virtual_usb_device  DUT  False  ${ip}
    ${version_bk_now_old}  get_bmc_version  DUT  ip=${ip}  mc_info=True
    independent_step  5  check_info_equal  ${version_bk_old}  ${version_bk_now_old}  False
    independent_step  6  check_reset_sel_info  DUT  ip=${ip}
    ${version_bk_again_3}  get_bmc_version  DUT  ip=${ip}  mc_info=True
    independent_step  7  check_info_equal  ${version_bk_again_3}  ${version_bk_now_old}
    independent_step  8  set_reset_type  DUT  ${cmd_ipmitool_mc_reset_cold}  cold  True
    ${version_bk_again_4}  get_bmc_version  DUT  ip=${ip}  mc_info=True
    independent_step  9  check_info_equal  ${version_bk_again_3}  ${version_bk_again_4}

run update bmc by cfu to lower backup lan
    ${ip}  get_ip_address_from_ipmitool  DUT
    ${version_bk_old}  get_bmc_version  DUT  ip=${ip}  mc_info=True
    independent_step  1  set_bmc_virtual_usb_device  DUT  ip=${ip}
    independent_step  2  set_sel_clear  DUT  ${ip}
    independent_step  3  update_by_cfu  DUT  bmc  False  old  bmc_ip=${ip}
    ${ip}  get_ip_address_from_ipmitool  DUT
    independent_step  4  set_bmc_virtual_usb_device  DUT  False  ${ip}
    ${version_bk_now_old}  get_bmc_version  DUT  ip=${ip}  mc_info=True
    independent_step  5  check_info_equal  ${version_bk_old}  ${version_bk_now_old}  False
    independent_step  6  check_reset_sel_info  DUT  ${ip}  reboot
    ${version_bk_again_3}  get_bmc_version  DUT  ip=${ip}  mc_info=True
    independent_step  7  check_info_equal  ${version_bk_again_3}  ${version_bk_now_old}
    independent_step  8  set_reset_type  DUT  ${cmd_ipmitool_mc_reset_cold}  cold  True
    ${version_bk_again_4}  get_bmc_version  DUT  ip=${ip}  mc_info=True
    independent_step  9  check_info_equal  ${version_bk_again_3}  ${version_bk_again_4}

End BMC Sensor Read Stress Test
    OS Connect Device
    independent_step  1  set_pdu_status_connect_os  DUT  reboot  ${pdu_port}  600  60
    independent_step  2  delete_folder  DUT  ${dut_shell_path}
    OS Disconnect Device

Begin Boot Option Configuration
    OS Connect Device
    independent_step  1  run ipmi set cmd  DUT  cmd=${cmd_4_Set_System_Boot_Options}
    independent_step  2  run ipmi set cmd  DUT  cmd=${cmd_1_Set_System_Boot_Options}
    independent_step  3  run ipmi set cmd  DUT  cmd=${cmd_2_Set_System_Boot_Options}
    independent_step  4  run ipmi set cmd  DUT  cmd=${cmd_3_Set_System_Boot_Options}
    independent_step  5  run ipmi set cmd  DUT  cmd=${cmd_4_Set_System_Boot_Options}
    independent_step  6  reboot_os  DUT
    independent_step  7  set time delay  300
    independent_step  8  send key  DUT  KEY_LEFT  ${1}
    independent_step  9  verify_menu_bios_setup  DUT  Save Changes and Exit
    independent_step  10  whitebox exit bios setup  DUT  False

END Boot Option Configuration
    OS Connect Device
    independent_step  1  Keyword Retry  power_cycle_os_by_ipmitool  DUT  %{server_username_1}  %{server_ipv4_ip_1}
        ...  %{server_password_1}  %{bmc_ipv4_ip_1}  ipmitool_cmd=power cycle  bmcusername=${bmc_username}
        ...  bmcpassword=${bmc_password}
    independent_step  2  set time delay  30
    independent_step  3  Keyword Retry  power_cycle_os_by_ipmitool  DUT  %{server_username_1}  %{server_ipv4_ip_1}
        ...  %{server_password_1}  %{bmc_ipv4_ip_1}  ipmitool_cmd=power on  bmcusername=${bmc_username}
        ...  bmcpassword=${bmc_password}
    independent_step  4  set time delay  20
    independent_step  5  wait_prompt  DUT
    OS Disconnect Device

Set BMC SEL time and Check
    OS Connect Device
    execute_Linux_command   ipmitool sel time set "2/15/2016 21:26:00"
    ${SEL_time_output} =  execute_Linux_command   ipmitool sel time get
    common_check_patern_2    ${SEL_time_output}  2.*15.*2016 21.*26  check in sel time get command   expect=True
    OS Disconnect Device

Set the RTC time to current time and sync to hwclock
    OS Connect Device
    ${os_dt} =  change_date_time_in_os   DUT
    Set Suite Variable  ${os_dt}
    execute_Linux_command    hwclock --systohc
    OS Disconnect Device

Check Time in BIOS
    OS Connect Device
    verify_time_in_BIOS  DUT   ${athena_bios_password}   ${os_dt}
    OS Disconnect Device
    Sleep  150

Check if BMC SEL time is synced
    OS Connect Device
    ${time_output} =  execute_Linux_command   ipmitool sel time get
    verify_bmc_time_is_synced  DUT   ${time_output}  ${os_dt}
    OS Disconnect Device


Trigger and event and check time in log
    Set the RTC time to current time and sync to hwclock
    OS Connect Device
    execute_Linux_command    ipmitool sel clear
    Sleep  10
    ${SEL_time_in_Logs} =  execute_Linux_command   ipmitool sel elist
    verify_bmc_time_is_synced  DUT   ${SEL_time_in_Logs}  ${os_dt}
    OS Disconnect Device

Warm reset BMC and then check BMC time
    Set the RTC time to current time and sync to hwclock
    OS Connect Device
    execute_Linux_command    ipmitool mc reset warm
    execute_Linux_command    ipmitool mc reset cold
    OS Disconnect Device
    Sleep  150
    Check if BMC SEL time is synced

Reset SUT and boot to OS
    Set the RTC time to current time and sync to hwclock
    OS Connect Device
    execute_Linux_command    ipmitool power reset
    OS Disconnect Device
    Sleep  150
    Check if BMC SEL time is synced

AC cycle and then check the BMC time
   Set the RTC time to current time and sync to hwclock
   OS Connect Device
   ses_lib.powercycle_pdu1  DUT
   OS Disconnect Device
   Sleep  300
   Check if BMC SEL time is synced

Check inventory details
    ${fru_area_size_output} =   execute_Linux_command   ipmitool raw 0x0a 0x10 0x00
    common_check_patern_2       ${fru_area_size_output}    ${expected_fru_size}   FRU Area size check   expect=True
    ${fru_0_ouput} =    execute_Linux_command   ipmitool fru print 0
    common_check_patern_2   ${fru_0_ouput}   Chassis Type.*:.*${chassis_type}   check_chassis_type  expect=True
    common_check_patern_2   ${fru_0_ouput}   Board Mfg.*:.*${board_mfg}  check_board_mfg   expect=True
    common_check_patern_2   ${fru_0_ouput}   Board Product.*:.*${board_product}  check_board_product   expect=True
    common_check_patern_2   ${fru_0_ouput}   Product Manufacturer.*:.*${product_mfg}   check_product_mfg   expect=True
    common_check_patern_2   ${fru_0_ouput}   Product Name.*:.*${product_name}   check_product_name    expect=True
    common_check_patern_2   ${fru_0_ouput}   Product Part Number.*:.*${product_part_number}   check_product_part_number    expect=True
    common_check_patern_2   ${fru_0_ouput}   Product Version.*:.*${product_version}  check_product_version     expect=True
    common_check_patern_2   ${fru_0_ouput}   Board Part Number.*:.*${board_part_number}   check_board_part_number   expect=True
    ${fru_2_ouput} =    execute_Linux_command   ipmitool fru print 2
    common_check_patern_2    ${fru_2_ouput}    Product Manufacturer.*:.*${product_mfg_fru2}   check_product_manufacturer  expect=True
    common_check_patern_2    ${fru_2_ouput}    Product Name.*:.*${Product_name_fru2}    check_product_name    expect=True
    common_check_patern_2    ${fru_2_ouput}    Product Part Number.*:.*${product_part_number_fru2}   check_product_part_number    expect=True
    common_check_patern_2    ${fru_2_ouput}    Product Version.*:.*${product_version_fru2}    check_product_version   expect=True
    ${chassis_type_output} =  execute_Linux_command  dmidecode -s chassis-type
    common_check_patern_2   ${chassis_type_output}   ${chassis_type}   check_chassis_type  expect=True
    ${system_manufacturer_output} =  execute_Linux_command   dmidecode -s system-manufacturer
    common_check_patern_2   ${system_manufacturer_output}    ${product_mfg}  check_product_manufacturer  expect=True
    ${system_product_name_output} =  execute_Linux_command   dmidecode -s system-product-name
    common_check_patern_2   ${system_product_name_output}   ${product_name}    check_product_name    expect=True
    ${system_serial_number_output} =  execute_Linux_command  dmidecode -s system-serial-number
    common_check_patern_2   ${system_serial_number_output}  ${serial_number}   check_serial_number    expect=True
    ${chassis_asset_tag_output} =  execute_Linux_command    dmidecode -s chassis-asset-tag
    validate asset tag   ${chassis_asset_tag_output}
    ${chassis_version_output}=  execute_Linux_command  dmidecode -s chassis-version
    common_check_patern_2    ${chassis_version_output}   ${chassis_ver}   check_chassis_version  expect=True

Clear SEL Logs
    execute_Linux_command    ipmitool sel clear
    Sleep  10

Verify Watchdog Timer for Power Cycle timeout action
   OS Connect Device
   Clear SEL Logs
   Set Watchdog Timer for Power Cycle timeout action
   Get Watchdog Timer and Verify it will not count down
   Reset Watchdog Timer
   Get Watchdog Timer and Verify it will count down
   verify system power cycle after count down
   OS Disconnect Device
   Sleep  150

   Verify BMC can detect the watchdog event for Power Cycle

Verify Watchdog Timer for hard reset timeout action
   OS Connect Device
   Clear SEL Logs
   Set Watchdog Timer for hard reset timeout action
   Get Watchdog Timer and Verify it will not count down
   Reset Watchdog Timer
   Get Watchdog Timer and Verify it will count down
   verify system hard reset after count down
   OS Disconnect Device
   Sleep  100

   Verify BMC can detect the watchdog event for hard reset

Verify Watchdog Timer for power down timeout action
   OS Connect Device
   Clear SEL Logs
   Set Watchdog Timer for power down timeout action
   Get Watchdog Timer and Verify it will not count down
   Reset Watchdog Timer
   Get Watchdog Timer and Verify it will count down
   verify system power down after count down
   OS Disconnect Device

   Power on the system

   Verify BMC can detect the watchdog event for power down

Verify Watchdog Timer for no action
   OS Connect Device
   Clear SEL Logs
   Set Watchdog Timer for no action
   Get Watchdog Timer and Verify it will not count down
   Reset Watchdog Timer
   Get Watchdog Timer and Verify it will count down
   Sleep  65
   Verify BMC can detect the watchdog event for no action
   OS Disconnect Device

Set Watchdog Timer for Power Cycle timeout action
    execute_Linux_command    ipmitool raw 06 0x24 01 03 00 0x3e 0x58 02
    Sleep  5

Set Watchdog Timer for hard reset timeout action
    execute_Linux_command    ipmitool raw 06 0x24 01 01 00 0x3e 0x58 02
    Sleep  5

Set Watchdog Timer for power down timeout action
    execute_Linux_command    ipmitool raw 06 0x24 01 02 00 0x3e 0x58 02
    Sleep  5

Set Watchdog Timer for no action
    execute_Linux_command    ipmitool raw 06 0x24 01 00 00 0x3e 0x58 02
    Sleep  5

Get Watchdog Timer and Verify it will not count down
    ${temp_output_1} =  execute_Linux_command    ipmitool raw 06 0x25
    Sleep  5
    ${temp_output_2} =  execute_Linux_command    ipmitool raw 06 0x25
    Verify_IPMI_Get_Watchdog_Timer_output    ${temp_output_1}   ${temp_output_2}   check if watchdog timer is not running   expect_same=True    

Reset Watchdog Timer
    execute_Linux_command    ipmitool raw 06 0x22
    Sleep  5

Get Watchdog Timer and Verify it will count down
    ${temp_output_1} =  execute_Linux_command    ipmitool raw 06 0x25
    Sleep  5
    ${temp_output_2} =  execute_Linux_command    ipmitool raw 06 0x25
    Verify_IPMI_Get_Watchdog_Timer_output    ${temp_output_1}  ${temp_output_2}  check if watchdog timer is running   expect_same=False

verify system power cycle after count down
    verify_power_cycle_after_watchdog_timer_expiry  DUT
    Sleep  5

verify system hard reset after count down
    verify_hard_reset_after_watchdog_timer_expiry  DUT
    Sleep  5

verify system power down after count down
    verify_power_down_after_watchdog_timer_expiry  DUT
    Sleep  5

Verify BMC can detect the watchdog event for Power Cycle
   OS Connect Device
   ${event_Logs} =  execute_Linux_command   ipmitool sel elist
   common_check_patern_2    ${event_Logs}  Power cycle.*Asserted  check if device power cycled through SEL Logs   expect=True
   OS Disconnect Device


Verify BMC can detect the watchdog event for hard reset
   OS Connect Device
   ${event_Logs} =  execute_Linux_command   ipmitool sel elist
   common_check_patern_2    ${event_Logs}  Hard reset.*Asserted  check if device hard reset through SEL Logs   expect=True
   OS Disconnect Device


Verify BMC can detect the watchdog event for power down
   OS Connect Device
   ${event_Logs} =  execute_Linux_command   ipmitool sel elist
   common_check_patern_2    ${event_Logs}  Power down.*Asserted  check if device power down through SEL Logs   expect=True
   OS Disconnect Device


Verify BMC can detect the watchdog event for no action
   ${event_Logs} =  execute_Linux_command   ipmitool sel elist
   common_check_patern_2    ${event_Logs}  Timer expired.*Asserted  check if no action was taken through SEL Logs   expect=True

Power on the system
   OS Connect Device
   ses_lib.powercycle_pdu1  DUT
   OS Disconnect Device
   Sleep  300

Verify_BMC_fru_information
   ${fru_info} =  get_BMC_fru_info   DUT 
   common_check_patern_2     ${fru_info}   System Manufacturer.*${product_mfg}     check System Manufacturer   expect=True
   common_check_patern_2     ${fru_info}   System Product Name.*${product_name}    check System Product Name   expect=True
   common_check_patern_2     ${fru_info}   System Version.*${product_version}      check System Version    expect=True
   common_check_patern_2     ${fru_info}   System Serial Number.*${serial_number_bios}  check System Serial Number   expect=True
   common_check_patern_2     ${fru_info}   Board Manufacturer.*${board_mfg}        check Board Manufacturer  expect=True
   common_check_patern_2     ${fru_info}   Board Product Name.*${board_product}    check Board Product Name  expect=True
   common_check_patern_2     ${fru_info}   Board Part Number.*${board_part_number}  check Board Part Number   expect=True
   common_check_patern_2     ${fru_info}   Board Serial Number.*${Board_Serial_num}   check Board Serial Number  expect=True
   common_check_patern_2     ${fru_info}   Chassis Manufacturer.*${chassis_mfg}   check Chassis Manufacturer   expect=True

verify_system_event_log
   ${ip}  get_ip_address_from_ipmitool  DUT
   ${clearlog_output} =  execute_local_cmd   ipmitool -I lanplus -H ${ip} -U admin -P admin sel clear
   common_check_patern_2    ${clearlog_output}    Clearing SEL    check system event log clear   expect=True
   Sleep   30
   ${add_system_event} =   execute_local_cmd   ipmitool -I lanplus -H ${ip} -U admin -P admin event 1
   common_check_patern_2   ${add_system_event}    Sending SAMPLE event   check system event insertion    expect=True
   check_system_event_log    DUT

Download Athena BMC FW image
   OS Disconnect Device
   OS Connect Device
   mkdir_data_path    DUT  "/root/athena_gen2_fw/BMC"
   change_directory   DUT  "/root/athena_gen2_fw/BMC"
   downloadAthenaSesFwImage    DUT   Athena_FW_BMC_A
   OS Disconnect Device
   ConnectESMB
   mkdir_data_path    DUT  "/root/athena_gen2_fw/BMC"
   change_directory   DUT  "/root/athena_gen2_fw/BMC"
   downloadAthenaSesFwImage    DUT   Athena_FW_BMC_B
   OS Disconnect Device

Remove Athena BMC FW image
    OS Connect Device
    change_directory   DUT  "/root/athena_gen2_fw/BMC"
    RemoveAthenaBIOSFwImage    DUT   Athena_FW_BMC_A
    OS Disconnect Device
    ConnectESMB
    change_directory   DUT  "/root/athena_gen2_fw/BMC"
    RemoveAthenaBIOSFwImage    DUT   Athena_FW_BMC_B
    OS Disconnect Device

Upgrade bmc FW
    OS Connect Device
    installBMCFWimage  DUT  Athena_FW_BMC_A  upgrade
    Sleep  500
    OS Disconnect Device
    ConnectESMB
    installBMCFWimage  DUT  Athena_FW_BMC_B  upgrade
    Sleep  400
    OS Disconnect Device
    Remove Athena BMC FW image
    ConnectESMB
    ses_lib.powercycle_pdu1  DUT
    Sleep  300
    OS Connect Device
    ses_lib.powercycle_pdu1  DUT
    Sleep  300
    OS Disconnect Device

set boot device into BIOS Setup
    [Arguments]  ${ip}
    send_cmd  DUT  ${cmd_set_into_bios_step}  ${ip}
    send_cmd  DUT  ${cmd_set_into_bios_step_next}  ${ip}

get the boot options
    [Arguments]  ${ip}
    check_cmd_response  DUT  ${cmd_check_set_boot_into_bios_1}  ${response_check_set_boot_into_bios}  ip=${ip}
    check_cmd_response  DUT  ${cmd_check_set_boot_into_bios_2}  ${response_check_set_boot_into_bios_next}  ip=${ip}

power cycle and check status
    [Arguments]  ${ip}  ${action}  ${TC}
    ${clearlog_output} =  execute_local_cmd   ipmitool -I lanplus -H ${ip} -U admin -P admin power cycle
    common_check_patern_2    ${clearlog_output}    Cycle    ${TC}    expect=True

power reset and check status
    [Arguments]  ${ip}  ${TC}
    ${clearlog_output} =  execute_local_cmd   ipmitool -I lanplus -H ${ip} -U admin -P admin power reset
    common_check_patern_2    ${clearlog_output}    Reset    ${TC}    expect=True
    Sleep  150

set Force boot from default HDD single valid
    [Arguments]  ${ip}  ${cmd_single_valid}  ${cmd_single_valid_next}
    execute_local_cmd   ipmitool -I lanplus -H ${ip} -U admin -P admin ${cmd_single_valid}
    execute_local_cmd   ipmitool -I lanplus -H ${ip} -U admin -P admin ${cmd_single_valid_next}

set Force boot from default HDD permanent
    [Arguments]  ${ip}  ${cmd_permanent_valid}  ${cmd_permanent_valid_next}
    execute_local_cmd   ipmitool -I lanplus -H ${ip} -U admin -P admin ${cmd_permanent_valid}
    execute_local_cmd   ipmitool -I lanplus -H ${ip} -U admin -P admin ${cmd_permanent_valid_next}

End test 1
    Step  1  check_bmc_status_by_lan_thread_2
    OS Disconnect Device

Download Athena BMC image
   OS Connect Device
   downloadAthenaSesFwImage    DUT   Athena_FW_BMC
   OS Disconnect Device

Make SEL to contain full logs
   OS Connect Device
   Generate_SEL_Logs      DUT   Athena_FW_BMC
   OS Disconnect Device

Upgrade BMC using CFUFLASH Tool
   OS Connect Device
   upgrade_bmc_FW    DUT   Athena_FW_BMC
   ses_lib.powercycle_pdu1  DUT
   OS Disconnect Device
   Sleep  300

Verify BMC version
   OS Connect Device
   verify_BMC_version_in_BIOS     DUT   Athena_FW_BMC  upgrade  bios_password=${athena_bios_password}
   OS Disconnect Device
   Sleep  200

Remove Athena FW image
    OS Connect Device
    execute_Linux_command    ipmitool sel clear
    Sleep  10
    RemoveAthenaBIOSFwImage    DUT   Athena_FW_BMC
    OS Disconnect Device

verify fru vpd before and after cold reset
   ${fru_output_before_reset} =    execute_Linux_command   ipmitool fru
   ${mc_info_output_before_reset} =  execute_Linux_command  ipmitool mc info
   ${reset_output} =    execute_Linux_command  ipmitool mc reset cold
   common_check_patern_2    ${reset_output}     Sent cold reset command to MC      check cold reset command   expect=True
   Sleep  120
   ${fru_output_after_reset} =    execute_Linux_command   ipmitool fru
   ${mc_info_output_after_reset} =  execute_Linux_command  ipmitool mc info
   compare_fru_info_before_and_after_reset_powercycle   ${fru_output_before_reset}      ${fru_output_after_reset}
   compare_mc_info_before_and_after_reset    ${mc_info_output_before_reset}     ${mc_info_output_after_reset}

Verify BMC Version and ip address from ipmitoolinfo
   [Arguments]  ${ip}
   verify_bmc_version_ip_ipmitool   DUT  ipmitool raw 0x06 0x01  ipmitool raw 6 1
   check_bmc_ip_info  DUT  ${ip}

Verify the SEL and ensure no error
   verify_cmd_output_message  DUT  ipmitool sel list  ${error_messages_sell_list}

Verify the sensor and check status
   [Arguments]  ${ip}
   verifythesensorreadingandcheckstatus  DUT  ${ip}

Run BMC cold reset
   ${reset_output} =    execute_Linux_command  ipmitool mc reset cold
   common_check_patern_2    ${reset_output}     Sent cold reset command to MC      check cold reset command   expect=True
   Print Loop Info  'cold reset command to MC and Sleeping 150 seconds...'
   Sleep  170

verify fru mc info
   [Arguments]   ${bmc_ip}   ${fru_output_before_powercycle}     ${mc_info_output_before_powercycle}
   ${fru_output_after_powercycle} =   execute_local_cmd    ipmitool -I lanplus -H ${bmc_ip} -U admin -P admin fru
   ${mc_info_output_after_powercycle} =   execute_local_cmd    ipmitool -I lanplus -H ${bmc_ip} -U admin -P admin mc info
   compare_fru_info_before_and_after_reset_powercycle   ${fru_output_before_powercycle}      ${fru_output_after_powercycle}
   compare_mc_info_before_and_after_powercycle    ${mc_info_output_before_powercycle}    ${mc_info_output_after_powercycle}

verify IPMI commands
  [Arguments]    ${ip}
  ${version_check} =  execute_local_cmd  ipmitool -I lanplus -H ${ip} -U admin -P admin raw 0x06 0x01
  check ipmitool BMC version  ${version_check}    ${expected_bmc_version}
  ${lan_info_check} =  execute_local_cmd  ipmitool -I lanplus -H ${ip} -U admin -P admin lan print 1
  common_check_patern_2   ${lan_info_check}   ${ip_address_source_pattern}    check ip address source pattern  expect=True
  common_check_patern_2   ${lan_info_check}   IP Address.*:.*${ip}    check ip address pattern  expect=True
  common_check_patern_2   ${lan_info_check}   ${subnet_mask_pattern}    check subnet mask pattern  expect=True
  common_check_patern_2   ${lan_info_check}   ${mac_address_pattern}    check mac address pattern  expect=True
  ${sel_check} =  execute_local_cmd  ipmitool -I lanplus -H ${ip} -U admin -P admin sel list
  common_check_patern_2   ${sel_check}  Abnormal   check sel list  expect=False
  common_check_patern_2   ${sel_check}  fault   check sel list  expect=False
  common_check_patern_2   ${sel_check}  warning   check sel list  expect=False
  common_check_patern_2   ${sel_check}  fail   check sel list  expect=False
  common_check_patern_2   ${sel_check}  Error  check sel list  expect=False
  ${sensor_check} =   execute_local_cmd  ipmitool -I lanplus -H ${ip} -U admin -P admin sensor list  60
  common_check_patern_2   ${sensor_check}  Abnormal   check sensor list  expect=False
  common_check_patern_2   ${sensor_check}  fault   check sensor list  expect=False
  common_check_patern_2   ${sensor_check}  warning  check sensor list  expect=False
  common_check_patern_2   ${sensor_check}  fail   check sensor list  expect=False
  common_check_patern_2   ${sensor_check}  Error  check sensor list  expect=False

Download and verify BMC FW image
    [Arguments]  ${action}
    Download Athena BMC FW image
    OS Connect Device
    Verify the SEL and ensure no error
    ${ip}  get_ip_address_from_ipmitool  DUT
    Verify event log SEL clear  DUT  ${ip}
    ${BMC_MAC_address1a}  get_info_from_lan_print  DUT  MAC Address  True  ${ip}
    OS Disconnect Device
    ConnectESMB
    ${ip}  get_ip_address_from_ipmitool  DUT
    ${BMC_MAC_address1b}  get_info_from_lan_print  DUT  MAC Address  True  ${ip}
    OS Disconnect Device
    Download bmc FW image  ${action}
    OS Connect Device
    ${ip}  get_ip_address_from_ipmitool  DUT
    getBMCFWimageversion  DUT  Athena_FW_BMC_A  ${get_BMC_version}  ${get_BMC_version_next}  ${action}
    checkinstalledBCMFWversion  DUT  Athena_FW_BMC_A  ${ip}  ${action}
    ${BMC_MAC_address2a}  get_info_from_lan_print  DUT  MAC Address  True  ${ip}
    common_check_patern_2    ${BMC_MAC_address1a}     ${BMC_MAC_address2a}      check MAC address not swipe out on ESMA  expect=True
    Verify the SEL and ensure no error
    verifyeventlogSELclear  DUT  ${ip}
    OS Disconnect Device
    ConnectESMB
    ${ip}  get_ip_address_from_ipmitool  DUT
    getBMCFWimageversion  DUT  Athena_FW_BMC_B  ${get_BMC_version}  ${get_BMC_version_next}  ${action}
    checkinstalledBCMFWversion  DUT  Athena_FW_BMC_B  ${ip}  ${action}
    ${BMC_MAC_address2b}  get_info_from_lan_print  DUT  MAC Address  True  ${ip}
    common_check_patern_2    ${BMC_MAC_address1b}     ${BMC_MAC_address2b}      check MAC address not swipe out on ESMB   expect=True
    Verify the SEL and ensure no error
    verifyeventlogSELclear  DUT  ${ip}
    OS Disconnect Device

Download bmc FW image
    [Arguments]  ${action}
    FOR    ${INDEX}    IN RANGE    1    3
        Print Loop Info  ${INDEX}
        OS Connect Device
        installBMCFWimage  DUT  Athena_FW_BMC_A  ${action}  ${INDEX}
        Sleep  400
        OS Disconnect Device
        ConnectESMB
        installBMCFWimage  DUT  Athena_FW_BMC_B  ${action}  ${INDEX}
        Sleep  400
        OS Disconnect Device
    END
    Remove Athena BMC FW image
    ConnectESMB
    ses_lib.powercycle_pdu1  DUT
    OS Disconnect Device
    Sleep  300
    OS Connect Device
    ses_lib.powercycle_pdu1  DUT
    OS Disconnect Device
    Sleep  300

verify SOL Function
  [Arguments]    ${ip}  ${BIOS_info_output_before_SOL_active}
  ${mc_info_output_before_SOL_active} =   execute_local_cmd    ipmitool -I lanplus -H ${ip} -U admin -P admin mc info
  verifyeventlogSELclear  DUT  ${ip}
  execute_local_cmd  ipmitool -I lanplus -H {ip} -U admin -P admin sol activate
  Sleep  20
  ${mc_info_output_after_SOL_active} =   execute_Linux_command  ipmitool mc info
  compare_mc_info    ${mc_info_output_before_SOL_active}    ${mc_info_output_after_SOL_active}
  ${BIOS_info_output_after_SOL_active} =   execute_Linux_command  dmidecode -t 0
  compare_BIOS_info    ${BIOS_info_output_before_SOL_active}    ${BIOS_info_output_after_SOL_active}
  verifythesensorreadingandcheckstatus  DUT  
  Verify the SEL and ensure no error
  Run BMC cold reset

upgrade_downgrade_bios_FW
  [Arguments]    ${module}  ${version}  ${key}
  OS Connect Device
  ${ip}  get_ip_address_from_ipmitool  DUT
  OS Disconnect Device
  Verify event log SEL clear  DUT  ${ip}
  ${image_to_upgrade_downgrade} =  get_image_version_for_upgrade_downgrade   ${module}  ${version}   ${key}
  ${rev_to_check} =  GetRevFromImage  ${image_to_upgrade_downgrade}
  OS Connect Device
  change_directory   DUT  /root/athena_gen2_fw/BIOS
  update_bios_FW   DUT    ./CFUFLASH -cd -d 2  ${image_to_upgrade_downgrade}
  OS Disconnect Device
  whitebox_lib.Powercycle Pdu1  DUT
  Sleep  300
  whitebox_lib.Powercycle Pdu1  DUT
  Sleep  480
  Verify abnormal event log  DUT  ${ip}
  OS Connect Device
  Sleep  60
  ${version_output} =  execute_Linux_command    dmidecode -s bios-version
  common_check_patern_2     ${version_output}     ${rev_to_check}    BIOS_Version_check  expect=True
  ${mac_address_bmc_lan} =  execute_Linux_command   ipmitool lan print 1
  common_check_patern_2     ${mac_address_bmc_lan}   ${mac_address_pattern}   BMC_LAN_MAC_check  expect=True
  ${mac_address_OS} =  execute_Linux_command    ifconfig -a | grep -i ether
  common_check_patern_2    ${mac_address_OS}      ${mac_address_OS_pattern1}    OS_MAC_check   expect=True
  common_check_patern_2    ${mac_address_OS}      ${mac_address_OS_pattern2}    OS_MAC_check   expect=True
  common_check_patern_2    ${mac_address_OS}      ${mac_address_OS_pattern3}    OS_MAC_check   expect=True
  common_check_patern_2    ${mac_address_OS}      ${mac_address_OS_pattern4}    OS_MAC_check   expect=True
  Check version in BIOS
  Sleep  60
  OS Disconnect 

upgrade_downgrade_bios_FW_remoteOS
  [Arguments]    ${module}  ${version}  ${key}
  ConnectESMB
  ${ip}  get_ip_address_from_ipmitool  DUT
  ${BMC_MAC_address1b}  get_info_from_lan_print  DUT  MAC Address  True  ${ip}
  OS Disconnect Device
  Verify event log SEL clear  DUT  ${ip}
  ${image_to_upgrade_downgrade} =  get_image_version_for_upgrade_downgrade   ${module}  ${version}   ${key}
  ${rev_to_check} =  GetRevFromImage  ${image_to_upgrade_downgrade}
  change_local_dir  /root/Athena-G2-FW/BIOS
  ${output} =  execute_local_cmd  ./CFUFLASH -nw -ip ${ip} -u admin -p admin -d 2 ${image_to_upgrade_downgrade} -fb   500
  common_check_patern_2      ${output}    Verifying Firmware Image : 100%... done   upgrade_complete check    expect=True
  common_check_patern_2      ${output}    Resetting the firmware   upgrade_complete check    expect=True
  common_check_patern_2      ${output}    Beginning to Deactive flashMode...end   upgrade_complete check    expect=True
  ses_lib.powercycle_pdu1  DUT
  Sleep  300
  ses_lib.powercycle_pdu1  DUT
  Sleep  360
  ConnectESMB
  Sleep  60
  ${version_output} =  execute_Linux_command    dmidecode -s bios-version
  common_check_patern_2     ${version_output}     ${rev_to_check}    BIOS_Version_check  expect=True
  ${BMC_MAC_address2b}  get_info_from_lan_print  DUT  MAC Address  True  ${ip}
  common_check_patern_2    ${BMC_MAC_address1b}     ${BMC_MAC_address2b}      check MAC address not swipe out on ESMB   expect=True
  ${mac_address_OS} =  execute_Linux_command    ifconfig -a | grep -i ether
  common_check_patern_2    ${mac_address_OS}      ${mac_address_OS_pattern1_B}    OS_MAC_check   expect=True
  common_check_patern_2    ${mac_address_OS}      ${mac_address_OS_pattern2_B}    OS_MAC_check   expect=True
  common_check_patern_2    ${mac_address_OS}      ${mac_address_OS_pattern3_B}    OS_MAC_check   expect=True
  common_check_patern_2    ${mac_address_OS}      ${mac_address_OS_pattern4_B}    OS_MAC_check   expect=True
  common_check_patern_2    ${mac_address_OS}      ${mac_address_OS_pattern5_B}    OS_MAC_check   expect=True
  Verify the SEL and ensure no error
  Verify abnormal event log  DUT  ${ip}
  verifythesensorreadingandcheckstatus  DUT  ${ip}
  Check version in BIOS
  Sleep  60
  OS Disconnect Device

Verify event sevice subscriptions info show up correctly
  OS Connect Device
  ${output} =  run_curl_get  ${resource_1}
  get_key_value  ${output}  @odata.context
  get_key_value  ${output}  @odata.etag
  get_key_value  ${output}  @odata.id
  get_key_value  ${output}  @odata.type
  get_key_value  ${output}  Description
  get_key_value  ${output}  Members
  get_key_value  ${output}  Members@odata.count
  get_key_value  ${output}  Name
  OS Disconnect Device

Verify service root property
  OS Connect Device
  ${output} =  run_curl_get  ${resource_service_root}
  get_key_value  ${output}  @odata.context
  get_key_value  ${output}  @odata.etag
  get_key_value  ${output}  @odata.id
  get_key_value  ${output}  @odata.type
  get_key_value  ${output}  AccountService
  get_key_value  ${output}  CertificateService
  get_key_value  ${output}  Chassis
  get_key_value  ${output}  CompositionService
  get_key_value  ${output}  Description
  get_key_value  ${output}  EventService
  get_key_value  ${output}  Id
  get_key_value  ${output}  JsonSchemas
  get_key_value  ${output}  Links
  get_key_value  ${output}  Managers
  get_key_value  ${output}  Name
  get_key_value  ${output}  Oem
  get_key_value  ${output}  Product
  get_key_value  ${output}  ProtocolFeaturesSupported
  get_key_value  ${output}  RedfishVersion
  get_key_value  ${output}  Registries
  get_key_value  ${output}  SessionService
  get_key_value  ${output}  Systems
  get_key_value  ${output}  Tasks
  get_key_value  ${output}  TelemetryService
  get_key_value  ${output}  UUID
  get_key_value  ${output}  UpdateService
  get_key_value  ${output}  Vendor
  check error in curl output    ${output}
  OS Disconnect Device

Verify service system property
  OS Connect Device
  ${output} =  run_curl_get  ${resource_service_system}
  get_key_value  ${output}  @Redfish.CollectionCapabilities
  get_key_value  ${output}  @odata.context
  get_key_value  ${output}  @odata.etag
  get_key_value  ${output}  @odata.id
  get_key_value  ${output}  @odata.type
  get_key_value  ${output}  Description
  get_key_value  ${output}  Members
  get_key_value  ${output}  Members@odata.count
  get_key_value  ${output}  Name
  check error in curl output    ${output}
  OS Disconnect Device

Verify system instance property
  OS Connect Device
  ${output} =  run_curl_get  ${resource_system_instance}
  get_key_value  ${output}  @odata.etag
  get_key_value  ${output}  @odata.id
  get_key_value  ${output}  @odata.type
  get_key_value  ${output}  Actions
  get_key_value  ${output}  AssetTag
  get_key_value  ${output}  Boot
  get_key_value  ${output}  Description
  get_key_value  ${output}  EthernetInterfaces
  get_key_value  ${output}  HostName
  get_key_value  ${output}  HostingRoles
  get_key_value  ${output}  Id
  get_key_value  ${output}  Links
  get_key_value  ${output}  LogServices
  get_key_value  ${output}  Manufacturer
  get_key_value  ${output}  Memory
  get_key_value  ${output}  MemoryDomains
  get_key_value  ${output}  Model
  get_key_value  ${output}  Name
  get_key_value  ${output}  NetworkInterfaces
  get_key_value  ${output}  PartNumber
  get_key_value  ${output}  PowerRestorePolicy
  get_key_value  ${output}  PowerState
  get_key_value  ${output}  Processors
  get_key_value  ${output}  SKU
  get_key_value  ${output}  SecureBoot
  get_key_value  ${output}  SerialNumber
  get_key_value  ${output}  SimpleStorage
  get_key_value  ${output}  Status
  get_key_value  ${output}  Storage
  get_key_value  ${output}  SystemType
  get_key_value  ${output}  TrustedModules
  get_key_value  ${output}  HostedServices
  check error in curl output    ${output}
  OS Disconnect Device

Verify collections
  [Arguments]    ${resource_options_collections}
  ${output} =  run_curl_get  ${resource_options_collections}
  get_key_value  ${output}  @odata.context
  get_key_value  ${output}  @odata.etag
  get_key_value  ${output}  @odata.id
  get_key_value  ${output}  @odata.type
  get_key_value  ${output}  Description
  get_key_value  ${output}  Members
  get_key_value  ${output}  Members@odata.count
  get_key_value  ${output}  Name
  check error in curl output    ${output}

Set UpdateService ServiceEnabled to True
  run_curl_patch  ${resource_2}  ${data_ServiceEnabled_true}

Check UpdateService ServiceEnabled value as True
  ${output} =  run_curl_get  ${resource_2}
  ${act_value} =  get_key_value  ${output}  ServiceEnabled
  Log  ${act_value}
  check_values_are_equal  ${act_value}  ${true_value}

Set UpdateService ServiceEnabled to False
  run_curl_patch  ${resource_2}  ${data_ServiceEnabled_false}

Check UpdateService ServiceEnabled value as False
  ${output} =  run_curl_get  ${resource_2}
  ${act_value} =  get_key_value  ${output}  ServiceEnabled
  Log  ${act_value}
  check_values_are_equal  ${act_value}  ${false_value}

Verify service enable can be changed to False successfully
  run_curl_patch  ${self_logservices}  ${data_ServiceEnabled_false}
  ${output} =  run_curl_get  ${self_logservices}
  ${act_value} =  get_key_value  ${output}  ServiceEnabled
  Log  ${act_value}
  check_values_are_equal  ${act_value}  ${false_value}

Create a new EventService Subscription and Verify
  ${output_1} =    run_curl_post  ${resource_3}  ${data_EventService_Subscription}
  ${Subs_id} =  get_key_value  ${output_1}  Id
  Log  ${Subs_id}
  ${output_2} =  run_curl_get  ${resource_3}/${Subs_id}
  ${act_value} =  get_key_value  ${output_2}  Context
  check_values_are_equal  ${act_value}  ${context}

Verify time can be changed successfully
  run_curl_patch  ${self_logservices}  ${data_DataTime_set}
  ${output} =  run_curl_get  ${self_logservices}
  ${act_value} =  get_key_value  ${output}  DateTime
  Log  ${act_value}
  check_values_are_equal  ${act_value}  ${data_DataTime}

Verify time offset can be changed successfully
  run_curl_patch  ${self_logservices}  ${data_DataTimeLocalOffset_set}
  ${output} =  run_curl_get  ${self_logservices}
  ${act_value} =  get_key_value  ${output}  DateTimeLocalOffset
  Log  ${act_value}
  check_values_are_equal  ${act_value}  ${data_DataTimeLocalOffset}

Delete the previously created EventService Subscription
  ${output_1} =    run_curl_get  ${resource_3}  
  ${last_id} =  get_key_value  ${output_1}  Members@odata.count
  run_curl_delete  ${resource_3}/${last_id}
  ${exp_count} =   Evaluate  ${last_id} - int(1)   
  ${output_2} =    run_curl_get  ${resource_3}
  ${act_count} =   get_key_value  ${output_2}  Members@odata.count
  check_values_are_equal  ${act_count}  ${exp_count}

Verify storage collections
  OS Connect Device
  ${output} =  run_curl_get  ${simple_storage_collection}
  get_key_value  ${output}  @odata.context
  get_key_value  ${output}  @odata.etag
  get_key_value  ${output}  @odata.id
  get_key_value  ${output}  @odata.type
  get_key_value  ${output}  Description
  get_key_value  ${output}  Members
  get_key_value  ${output}  Members@odata.count
  get_key_value  ${output}  Name
  OS Disconnect Device

Verify simple storage
  OS Connect Device
  ${output} =  run_curl_get  ${simple_storage}
  get_key_value  ${output}  @odata.context
  get_key_value  ${output}  @odata.etag
  get_key_value  ${output}  @odata.id
  get_key_value  ${output}  @odata.type
  get_key_value  ${output}  Description
  get_key_value  ${output}  Devices
  get_key_value  ${output}  Id
  get_key_value  ${output}  Name
  OS Disconnect Device

Verify log service collection
  OS Connect Device
  ${output} =  run_curl_get  ${log_service_collection_1}
  get_key_value  ${output}  @odata.context
  get_key_value  ${output}  @odata.etag
  get_key_value  ${output}  @odata.id
  get_key_value  ${output}  @odata.type
  get_key_value  ${output}  Description
  get_key_value  ${output}  Members
  get_key_value  ${output}  Members@odata.count
  get_key_value  ${output}  Name
  OS Disconnect Device

Verify log service collection_2
  OS Connect Device
  ${output} =  run_curl_get  ${log_service_collection_2}
  get_key_value  ${output}  @odata.context
  get_key_value  ${output}  @odata.etag
  get_key_value  ${output}  @odata.id
  get_key_value  ${output}  @odata.type
  get_key_value  ${output}  Description
  get_key_value  ${output}  Members
  get_key_value  ${output}  Members@odata.count
  get_key_value  ${output}  Name
  OS Disconnect Device

Modify the context of previously created EventService Subscription
  ${output_1} =    run_curl_get  ${resource_3}
  ${last_id} =  get_key_value  ${output_1}  Members@odata.count
  run_curl_patch  ${resource_3}/${last_id}  ${data_context_1}
  ${output_2} =  run_curl_get  ${resource_3}/${last_id}
  ${act_value} =  get_key_value  ${output_2}  Context
  check_values_are_equal  ${act_value}  ${context_1}

Verify BMC Log ID entries successfully
  ${ip}  get_ip_address_from_ipmitool  DUT
  execute_local_cmd  ipmitool -I lanplus -H ${ip} -U ${bmc_username} -P ${bmc_password} sel clear
  ${sel_list_before_output} =  execute_local_cmd  ipmitool -I lanplus -H ${ip} -U ${bmc_username} -P ${bmc_password} sel list
  ${output_before} =  run_curl_BMCIP_get  ${SEL_Log_Entries}  ${ip}
  ${sel_event_output} =  execute_local_cmd  ipmitool -I lanplus -H ${ip} -U ${bmc_username} -P ${bmc_password} event 1  20
  Sleep  20
  ${sel_list_after_output} =  execute_local_cmd  ipmitool -I lanplus -H ${ip} -U ${bmc_username} -P ${bmc_password} sel list
  ${EventTimestamp_value} =  get_EventTimestamp_sel_list  ${sel_list_after_output}
  ${output_after} =  run_curl_BMCIP_get  ${SEL_Log_Entries}  ${ip}
  ${act_value} =  get_key_value  ${output_after}  EventTimestamp
  Verify the curl output and ensure no error    ${output_after}
  check_values_are_equal  ${act_value}  ${EventTimestamp_value}

Verify the curl output and ensure no error
  [Arguments]    ${curl_output}
  check_output_from_curl  ${curl_output}

check error in curl output
  [Arguments]    ${curl_output}
  ${curl_output_str} =    Convert To String   ${curl_output}
  common_check_patern_2     ${curl_output_str}    ResourceMissingAtURI     Verify the resource is available   expect=False
  common_check_patern_2     ${curl_output_str}    error     check any error in curl output   expect=False
  common_check_patern_2     ${curl_output_str}    the service was denied access     check the access to the resource   expect=False

verify BootOption_1
  [Arguments]   ${resource_bootoption}
  OS Connect Device
  ${output} =  run_curl_get  ${resource_bootoption}
  get_key_value  ${output}  @Redfish.Settings
  get_key_value  ${output}  @odata.type
  get_key_value  ${output}  SettingsObject
  get_key_value  ${output}  @odata.id
  get_key_value  ${output}  @odata.context
  get_key_value  ${output}  @odata.etag
  get_key_value  ${output}  @odata.id
  get_key_value  ${output}  @odata.type
  get_key_value  ${output}  Alias
  get_key_value  ${output}  BootOptionEnabled
  get_key_value  ${output}  BootOptionReference
  get_key_value  ${output}  Description
  get_key_value  ${output}  DisplayName
  get_key_value  ${output}  Id
  get_key_value  ${output}  Name
  get_key_value  ${output}  RelatedItem@odata.count
  get_key_value  ${output}  UefiDevicePath
  check error in curl output    ${output}
  OS Disconnect Device

Verify LogEntry Collection_7
  ${ip}  get_ip_address_from_ipmitool  DUT
  execute_local_cmd  ipmitool -I lanplus -H ${ip} -U ${bmc_username} -P ${bmc_password} sel clear
  ${sel_list_before_output} =  execute_local_cmd  ipmitool -I lanplus -H ${ip} -U ${bmc_username} -P ${bmc_password} sel list
  ${curl_output_before} =  run_curl_BMCIP_get  ${LogEntry_Collection_7}  ${ip}
  ${sel_event_output} =  execute_local_cmd  ipmitool -I lanplus -H ${ip} -U ${bmc_username} -P ${bmc_password} event 1  20
  Sleep  20
  ${sel_list_after_output} =  execute_local_cmd  ipmitool -I lanplus -H ${ip} -U ${bmc_username} -P ${bmc_password} sel list
  ${EventTimestamp_value} =  get_EventTimestamp_sel_list  ${sel_list_after_output}
  ${curl_output_after} =  run_curl_BMCIP_get  ${LogEntry_Collection_7}  ${ip}
  ${event_output} =  get_members_message_curl_output  ${curl_output_after}  Event_Type
  check_values_are_equal  ${event_output}  ${Event_Type_message}
  ${sensor_output} =  get_members_message_curl_output  ${curl_output_after}  Sensor_Type
  check_values_are_equal  ${sensor_output}  ${Sensor_Type_details}
  Verify the curl output and ensure no error    ${curl_output_after}
  ${act_value} =  get_key_value  ${curl_output_after}  EventTimestamp
  check_values_are_equal  ${act_value}  ${EventTimestamp_value}

Verify composition service resource block info show up correctly
  ${ip}  get_ip_address_from_ipmitool  DUT
  ${curl_output} =  run_curl_BMCIP_get  ${ResourceBlocksCollection_log}  ${ip}
  Verify the curl output and ensure no error    ${curl_output}
  Verify event collections info show up correctly    ${curl_output}

Verify event collections info show up correctly
  [Arguments]    ${output}  
  get_key_value  ${output}  @odata.context
  get_key_value  ${output}  @odata.etag
  get_key_value  ${output}  @odata.id
  get_key_value  ${output}  @odata.type
  get_key_value  ${output}  Description
  get_key_value  ${output}  Members
  get_key_value  ${output}  Members@odata.count
  get_key_value  ${output}  Name

Verify computeBlock resource block info show up correctly
  ${ip}  get_ip_address_from_ipmitool  DUT
  ${curl_output} =  run_curl_BMCIP_get  ${resourceblocks_instance_1}  ${ip}
  Verify the curl output and ensure no error    ${curl_output}
  Verify computeBlock info under resourceBlock show up correctly    ${curl_output}

Verify computeBlock info under resourceBlock show up correctly 
  [Arguments]    ${output}
  get_key_value  ${output}  @odata.context
  get_key_value  ${output}  @odata.etag
  get_key_value  ${output}  @odata.id
  get_key_value  ${output}  @odata.type
  get_key_value  ${output}  CompositionStatus
  get_key_value  ${output}  Description
  get_key_value  ${output}  Id
  get_key_value  ${output}  Links
  get_key_value  ${output}  Memory
  get_key_value  ${output}  Memory@odata.count
  get_key_value  ${output}  Name
  get_key_value  ${output}  Processors
  get_key_value  ${output}  Processors@odata.count
  get_key_value  ${output}  Status

Verify drivesblock resource block info show up correctly
  ${ip}  get_ip_address_from_ipmitool  DUT
  ${curl_output} =  run_curl_BMCIP_get  ${resourceblocks_instance_2}  ${ip}
  Verify the curl output and ensure no error    ${curl_output}
  Verify drivesblock info under resourceBlock show up correctly    ${curl_output}

Verify drivesblock info under resourceBlock show up correctly
  [Arguments]    ${output}
  get_key_value  ${output}  @odata.context
  get_key_value  ${output}  @odata.etag
  get_key_value  ${output}  @odata.id
  get_key_value  ${output}  @odata.type
  get_key_value  ${output}  CompositionStatus
  get_key_value  ${output}  Description
  get_key_value  ${output}  Drives
  get_key_value  ${output}  Drives@odata.count
  get_key_value  ${output}  Id
  get_key_value  ${output}  Links
  get_key_value  ${output}  Name
  get_key_value  ${output}  ResourceBlockType
  get_key_value  ${output}  SimpleStorage
  get_key_value  ${output}  SimpleStorage@odata.count
  get_key_value  ${output}  Status
  get_key_value  ${output}  Storage
  get_key_value  ${output}  Storage@odata.count

Verify networkBlock resource block info show up correctly
  ${ip}  get_ip_address_from_ipmitool  DUT
  ${curl_output} =  run_curl_BMCIP_get  ${resourceblocks_instance_3}  ${ip}
  Verify the curl output and ensure no error    ${curl_output}
  Verify networkBlock info under resourceBlock show up correctly    ${curl_output}

Verify networkBlock info under resourceBlock show up correctly
  [Arguments]    ${output} 
  get_key_value  ${output}  @odata.context
  get_key_value  ${output}  @odata.etag
  get_key_value  ${output}  @odata.id
  get_key_value  ${output}  @odata.type
  get_key_value  ${output}  CompositionStatus
  get_key_value  ${output}  Description
  get_key_value  ${output}  EthernetInterfaces  
  get_key_value  ${output}  EthernetInterfaces@odata.count
  get_key_value  ${output}  Id
  get_key_value  ${output}  Links 
  get_key_value  ${output}  Name
  get_key_value  ${output}  ResourceBlockType
  get_key_value  ${output}  Status

Verify GET operation on the previously created EventService Subscription doesnt work after DELETE
  ${output_1} =    run_curl_get  ${resource_3}
  ${last_id} =  get_key_value  ${output_1}  Members@odata.count
  run_curl_delete  ${resource_3}/${last_id}
  ${exp_count} =   Evaluate  ${last_id} - int(1)
  ${output_2} =    run_curl_get  ${resource_3}
  ${act_count} =   get_key_value  ${output_2}  Members@odata.count
  check_values_are_equal  ${act_count}  ${exp_count}
  ${output_3} =  run_curl_get  ${resource_3}/${last_id}
  get_key_value  ${output_3}  error

Set ComputeBlock CompositionStatus Reserved to False  
  run_curl_patch  ${resourceblocks_instance_1}  ${computeblock_compositionstatus_false}

Verify ComputeBlock CompositionStatus Reserved value as False
  ${output} =  run_curl_get  ${resourceblocks_instance_1}
  ${act_value} =  get_key_value  ${output}  Reserved
  Log  ${act_value}
  check_values_are_equal  ${act_value}  ${false_value}

Set DrivesBlock CompositionStatus Reserved to False
  run_curl_patch  ${resourceblocks_instance_2}  ${drivesblock_compositionstatus_false}

Verify DrivesBlock CompositionStatus Reserved value as False
  ${output} =  run_curl_get  ${resourceblocks_instance_2}
  ${act_value} =  get_key_value  ${output}  Reserved
  Log  ${act_value}
  check_values_are_equal  ${act_value}  ${false_value}

Set NetworkBlock CompositionStatus Reserved to False
  run_curl_patch  ${resourceblocks_instance_3}  ${networkblock_compositionstatus_false}

Verify NetworkBlock CompositionStatus Reserved value as False
  ${output} =  run_curl_get  ${resourceblocks_instance_3}
  ${act_value} =  get_key_value  ${output}  Reserved
  Log  ${act_value}
  check_values_are_equal  ${act_value}  ${false_value}

Verify composition service info show up correctly
  ${ip}  get_ip_address_from_ipmitool  DUT
  ${curl_output} =  run_curl_BMCIP_get  ${CompositionService_resorce}  ${ip}
  Verify the curl output and ensure no error    ${curl_output}
  Verify compositionservice collections info show up correctly    ${curl_output}

Verify compositionservice collections info show up correctly
  [Arguments]    ${output}
  get_key_value  ${output}  @odata.context
  get_key_value  ${output}  @odata.etag
  get_key_value  ${output}  @odata.id
  get_key_value  ${output}  @odata.type
  get_key_value  ${output}  Id
  get_key_value  ${output}  Name
  get_key_value  ${output}  ResourceBlocks
  get_key_value  ${output}  ResourceZones
  get_key_value  ${output}  ServiceEnabled
  get_key_value  ${output}  Status

Set CompositionService ServiceEnabled to False
  run_curl_patch  ${CompositionService_resorce}  ${data_ServiceEnabled_false}

Verify CompositionService ServiceEnabled value as False
  ${output} =  run_curl_get  ${CompositionService_resorce}
  ${act_value} =  get_key_value  ${output}  ServiceEnabled
  Log  ${act_value}
  check_values_are_equal  ${act_value}  ${false_value}
  Verify the curl output and ensure no error    ${output}
  
Set CompositionService ServiceEnabled to True
  run_curl_patch  ${CompositionService_resorce}  ${data_ServiceEnabled_true}  

Verify CompositionService ServiceEnabled value as True
  ${output} =  run_curl_get  ${CompositionService_resorce}
  ${act_value} =  get_key_value  ${output}  ServiceEnabled
  Log  ${act_value}
  check_values_are_equal  ${act_value}  ${true_value}  
  Verify the curl output and ensure no error    ${output}

Verify telemetry service log service entries info show up correctly
  ${ip}  get_ip_address_from_ipmitool  DUT
  ${curl_output} =  run_curl_BMCIP_get  ${resource_telemetry_logentry}  ${ip}
  Verify the curl output and ensure no error    ${curl_output}
  Verify event collections info show up correctly    ${curl_output}

Verify telemetry service log service info show up correctly
  ${ip}  get_ip_address_from_ipmitool  DUT
  ${curl_output} =  run_curl_BMCIP_get  ${resource_telemetry_logservice}  ${ip}
  Verify the curl output and ensure no error    ${curl_output}
  get_key_value  ${curl_output}  @odata.context
  get_key_value  ${curl_output}  @odata.etag
  get_key_value  ${curl_output}  @odata.id
  get_key_value  ${curl_output}  @odata.type
  get_key_value  ${curl_output}  Actions
  get_key_value  ${curl_output}  DateTime
  get_key_value  ${curl_output}  DateTimeLocalOffset
  get_key_value  ${curl_output}  Description
  get_key_value  ${curl_output}  Entries
  get_key_value  ${curl_output}  Id
  get_key_value  ${curl_output}  LogEntryType
  get_key_value  ${curl_output}  MaxNumberOfRecords
  get_key_value  ${curl_output}  Name
  get_key_value  ${curl_output}  OverWritePolicy
  get_key_value  ${curl_output}  ServiceEnabled
  get_key_value  ${curl_output}  Status

Verify telemetry service triggers info show up correctly
  ${ip}  get_ip_address_from_ipmitool  DUT
  ${curl_output} =  run_curl_BMCIP_get  ${resource_telemetryservice_triggers}  ${ip}
  Verify the curl output and ensure no error    ${curl_output}
  Verify event TelemetryService info show up correctly    ${curl_output}

Verify telemetry service metric reports info show up correctly
  ${ip}  get_ip_address_from_ipmitool  DUT
  ${curl_output} =  run_curl_BMCIP_get  ${resource_telemetryservice_metricreports}  ${ip}
  Verify the curl output and ensure no error    ${curl_output}
  Verify event TelemetryService info show up correctly    ${curl_output}

Verify telemetry service metric report definition info show up correctly
  ${ip}  get_ip_address_from_ipmitool  DUT
  ${curl_output} =  run_curl_BMCIP_get  ${resource_metricreportdefinitions}  ${ip}
  Verify the curl output and ensure no error    ${curl_output}
  Verify event TelemetryService info show up correctly    ${curl_output}

Verify telemetry service metric definition instance info show up correctly
  ${ip}  get_ip_address_from_ipmitool  DUT
  ${curl_output} =  run_curl_BMCIP_get  ${resource_voltage_reading}  ${ip}
  Verify the curl output and ensure no error    ${curl_output}
  Verify event metricDefinition collections info show up correctly  ${curl_output}
  ${curl_output} =  run_curl_BMCIP_get  ${resource_temperature_reading}  ${ip}  
  Verify the curl output and ensure no error    ${curl_output}
  Verify event metricDefinition collections info show up correctly  ${curl_output}
  ${curl_output} =  run_curl_BMCIP_get  ${resource_fan_reading}  ${ip}
  Verify the curl output and ensure no error    ${curl_output}
  Verify event metricDefinition collections info show up correctly  ${curl_output}

Verify event metricDefinition collections info show up correctly
  [Arguments]    ${output}
  get_key_value  ${output}  @odata.context
  get_key_value  ${output}  @odata.etag
  get_key_value  ${output}  @odata.id
  get_key_value  ${output}  @odata.type
  get_key_value  ${output}  Accuracy
  get_key_value  ${output}  Id
  get_key_value  ${output}  Implementation
  get_key_value  ${output}  IsLinear
  get_key_value  ${output}  MetricDataType
  get_key_value  ${output}  MetricProperties
  get_key_value  ${output}  MetricType
  get_key_value  ${output}  Name
  get_key_value  ${output}  Precision
  get_key_value  ${output}  Units

Verify event TelemetryService info show up correctly
  [Arguments]    ${output}
  get_key_value  ${output}  @odata.context
  get_key_value  ${output}  @odata.etag
  get_key_value  ${output}  @odata.id
  get_key_value  ${output}  @odata.type
  get_key_value  ${output}  Members
  get_key_value  ${output}  Members@odata.count
  get_key_value  ${output}  Name

Verify telemetry service metric definition info show up correctly
  ${ip}  get_ip_address_from_ipmitool  DUT
  ${curl_output} =  run_curl_BMCIP_get  ${resource_metricdefinitions}  ${ip}
  Verify the curl output and ensure no error    ${curl_output}
  Verify event TelemetryService info show up correctly    ${curl_output}

verify memory instance
  [Arguments]   ${resource_memory_instance}
  ${output} =  run_curl_get  ${resource_memory_instance}
  get_key_value  ${output}   @odata.context
  get_key_value  ${output}   @odata.etag
  get_key_value  ${output}   @odata.id
  get_key_value  ${output}   @odata.type
  get_key_value  ${output}   Actions
  get_key_value  ${output}   Oem
  get_key_value  ${output}   \#AmiBios.ChangeState
  get_key_value  ${output}   @Redfish.ActionInfo
  get_key_value  ${output}   target
  get_key_value  ${output}   AllowedSpeedsMHz
  get_key_value  ${output}   BaseModuleType
  get_key_value  ${output}   BusWidthBits
  get_key_value  ${output}   CacheSizeMiB
  get_key_value  ${output}   CapacityMiB
  get_key_value  ${output}   DataWidthBits
  get_key_value  ${output}   DeviceLocator
  get_key_value  ${output}   FirmwareRevision
  get_key_value  ${output}   Id
  get_key_value  ${output}   Links
  get_key_value  ${output}   Chassis 
  get_key_value  ${output}   LogicalSizeMiB
  get_key_value  ${output}   Manufacturer
  get_key_value  ${output}   MemoryDeviceType
  get_key_value  ${output}   MemoryLocation
  get_key_value  ${output}   Channel
  get_key_value  ${output}   Slot
  get_key_value  ${output}   Socket
  get_key_value  ${output}   MemorySubsystemControllerManufacturerID
  get_key_value  ${output}   MemorySubsystemControllerProductID
  get_key_value  ${output}   MemoryType
  get_key_value  ${output}   ModuleManufacturerID
  get_key_value  ${output}   ModuleProductID
  get_key_value  ${output}   Name
  get_key_value  ${output}   NonVolatileSizeMiB
  get_key_value  ${output}   OperatingMemoryModes
  get_key_value  ${output}   OperatingSpeedMhz
  get_key_value  ${output}   PartNumber
  get_key_value  ${output}   RankCount
  get_key_value  ${output}   SecurityCapabilities
  get_key_value  ${output}   ConfigurationLockCapable
  get_key_value  ${output}   DataLockCapable
  get_key_value  ${output}   PassphraseCapable
  get_key_value  ${output}   SerialNumber
  get_key_value  ${output}   Status
  get_key_value  ${output}   State
  get_key_value  ${output}   VolatileSizeMiB
  check error in curl output    ${output}

verify sub processor collection
  [Arguments]     ${resource_subprocessor_collection}
  OS Connect Device
  ${output} =  run_curl_get  ${resource_subprocessor_collection}
  get_key_value  ${output}  @odata.context
  get_key_value  ${output}  @odata.etag
  get_key_value  ${output}  @odata.id
  get_key_value  ${output}  @odata.type
  get_key_value  ${output}  Description
  get_key_value  ${output}  Members
  get_key_value  ${output}  Members@odata.count
  get_key_value  ${output}  Members@odata.nextLink
  get_key_value  ${output}  Name
  check error in curl output    ${output}
  OS Disconnect Device

Verify processor instance property
  [Arguments]     ${resource_processor_instance_property}
  OS Connect Device
  ${output} =  run_curl_get  ${resource_processor_instance_property}
  get_key_value  ${output}  @odata.context
  get_key_value  ${output}  @odata.etag
  get_key_value  ${output}  @odata.id
  get_key_value  ${output}  @odata.type
  get_key_value  ${output}  Id
  get_key_value  ${output}  Links
  get_key_value  ${output}  Chassis
  get_key_value  ${output}  ConnectedProcessors 
  get_key_value  ${output}  ConnectedProcessors@odata.count
  get_key_value  ${output}  Manufacturer
  get_key_value  ${output}  MaxSpeedMHz 
  get_key_value  ${output}  Name
  get_key_value  ${output}  ProcessorArchitecture
  get_key_value  ${output}  ProcessorId
  get_key_value  ${output}  EffectiveFamily
  get_key_value  ${output}  ProcessorType
  get_key_value  ${output}  Socket
  get_key_value  ${output}  Status
  get_key_value  ${output}  Health
  get_key_value  ${output}  State
  get_key_value  ${output}  SubProcessors
  get_key_value  ${output}  TotalCores
  get_key_value  ${output}  TotalEnabledCores
  get_key_value  ${output}  TotalThreads
  check error in curl output    ${output}
  OS Disconnect Device

Verify all network interfaces instance 
  [Arguments]    ${resource_network_interface_instance}
  OS Connect Device
  ${output} =  run_curl_get  ${resource_network_interface_instance}
  get_key_value  ${output}   @odata.context
  get_key_value  ${output}   @odata.etag
  get_key_value  ${output}   @odata.id
  get_key_value  ${output}   @odata.type
  get_key_value  ${output}   AutoNeg
  get_key_value  ${output}   DHCPv4
  get_key_value  ${output}   DHCPv6
  get_key_value  ${output}   Description
  get_key_value  ${output}   FQDN
  get_key_value  ${output}   FullDuplex
  get_key_value  ${output}   HostName
  get_key_value  ${output}   IPv4Addresses
  get_key_value  ${output}   IPv6Addresses
  get_key_value  ${output}   IPv6DefaultGateway
  get_key_value  ${output}   Id
  get_key_value  ${output}   InterfaceEnabled
  get_key_value  ${output}   LinkStatus
  get_key_value  ${output}   MACAddress
  get_key_value  ${output}   MTUSize
  get_key_value  ${output}   MaxIPv6StaticAddresses
  get_key_value  ${output}   Name
  get_key_value  ${output}   NameServers
  get_key_value  ${output}   PermanentMACAddress
  get_key_value  ${output}   SpeedMbps
  get_key_value  ${output}   StatelessAddressAutoConfig
  get_key_value  ${output}   Status
  get_key_value  ${output}   VLAN
  check error in curl output    ${output}
  OS Disconnect Device

Verify all network interfaces instance without error
  [Arguments]    ${resource_network_interface_instance}
  OS Connect Device
  ${output} =  run_curl_get  ${resource_network_interface_instance}
  check error in curl output    ${output}
  OS Disconnect Device

verify memory instance without error 
  [Arguments]    ${resource_memory_instance}
  ${output} =  run_curl_get   ${resource_memory_instance}
  check error in curl output    ${output}

Verify GET on EventService
  ${output_1} =    run_curl_get  ${resource_4}
  get_key_value  ${output_1}  Actions
  get_key_value  ${output_1}  DeliveryRetryAttempts
  get_key_value  ${output_1}  DeliveryRetryIntervalSeconds
  get_key_value  ${output_1}  Description
  get_key_value  ${output_1}  EventFormatTypes
  get_key_value  ${output_1}  Id
  get_key_value  ${output_1}  Name
  get_key_value  ${output_1}  RegistryPrefixes
  get_key_value  ${output_1}  ResourceTypes
  get_key_value  ${output_1}  SSEFilterPropertiesSupported
  get_key_value  ${output_1}  ServerSentEventUri
  get_key_value  ${output_1}  ServiceEnabled
  get_key_value  ${output_1}  Status
  get_key_value  ${output_1}  SubordinateResourcesSupported
  get_key_value  ${output_1}  Subscriptions

Create a new EventService SubmitTestEvent and Verify
  ${output_1} =    run_curl_post  ${resource_5}  ${data_EventService_SubmitTestEvent}
  ${Task_id} =  get_key_value  ${output_1}  Id
  Log  ${Task_id}
  ${output_2} =  run_curl_get  ${resource_6}/${Task_id}
  ${act_value} =  get_key_value  ${output_2}  Name
  check_values_are_equal  ${act_value}  EventService SubmitTestEvent Action

Verify GET on TasksService
  ${output_1} =    run_curl_get  ${resource_7}
  get_key_value  ${output_1}  CompletedTaskOverWritePolicy
  get_key_value  ${output_1}  DateTime
  get_key_value  ${output_1}  Description
  get_key_value  ${output_1}  Id
  get_key_value  ${output_1}  LifeCycleEventOnTaskStateChange
  get_key_value  ${output_1}  Name
  get_key_value  ${output_1}  ServiceEnabled
  get_key_value  ${output_1}  Status
  get_key_value  ${output_1}  Tasks
  get_key_value  ${output_1}  @odata.context
  get_key_value  ${output_1}  @odata.etag
  get_key_value  ${output_1}  @odata.id
  get_key_value  ${output_1}  @odata.type

Verify GET on Task Collections
  ${output_1} =    run_curl_get  ${resource_6}
  get_key_value  ${output_1}  @odata.context
  get_key_value  ${output_1}  @odata.etag
  get_key_value  ${output_1}  @odata.id
  get_key_value  ${output_1}  @odata.type
  get_key_value  ${output_1}  Description
  get_key_value  ${output_1}  Members

Verify manager date time can be changed successfully
  run_curl_patch  ${resource_Manager_2}  ${data_datatime_setup}
  ${output} =  run_curl_get  ${resource_Manager_2}
  ${act_value} =  get_key_value  ${output}  DateTime
  Log  ${act_value}
  check_values_are_equal  ${act_value}  ${data_datatime_output}
  run_curl_patch  ${resource_Manager_2}  ${data_DataTimeLocalOffset_set}
  ${output} =  run_curl_get  ${resource_Manager_2}
  ${act_value} =  get_key_value  ${output}  DateTimeLocalOffset
  Log  ${act_value}
  check_values_are_equal  ${act_value}  ${data_DataTimeLocalOffset}

Verify telemetry test metric report can be sent successfully
  ${output} =    run_curl_post  ${resource_SubmitTestMetricReport}  ${data_SubmitTestMetricReport}
  get_key_value  ${output}  @odata.context
  get_key_value  ${output}  @odata.id
  get_key_value  ${output}  @odata.type
  get_key_value  ${output}  Description
  get_key_value  ${output}  Id
  get_key_value  ${output}  Name
  get_key_value  ${output}  TaskState

Verify manager instance info show up correctly
  ${output} =  run_curl_get  ${resource_Manager_1}
  Verify the curl output and ensure no error    ${output}
  get_key_value  ${output}  @odata.context
  get_key_value  ${output}  @odata.etag
  get_key_value  ${output}  @odata.id
  get_key_value  ${output}  @odata.type
  get_key_value  ${output}  Actions
  get_key_value  ${output}  CommandShell
  get_key_value  ${output}  DateTime
  get_key_value  ${output}  DateTimeLocalOffset
  get_key_value  ${output}  Description
  get_key_value  ${output}  EthernetInterfaces
  get_key_value  ${output}  FirmwareVersion
  get_key_value  ${output}  GraphicalConsole
  get_key_value  ${output}  HostInterfaces
  get_key_value  ${output}  Id
  get_key_value  ${output}  Links
  get_key_value  ${output}  LogServices
  get_key_value  ${output}  ManagerType
  get_key_value  ${output}  Model
  get_key_value  ${output}  Name
  get_key_value  ${output}  NetworkProtocol
  get_key_value  ${output}  Oem
  get_key_value  ${output}  PowerState
  get_key_value  ${output}  Redundancy@odata.count
  get_key_value  ${output}  SerialConsole
  get_key_value  ${output}  SerialInterfaces
  get_key_value  ${output}  ServiceEntryPointUUID
  get_key_value  ${output}  Status
  get_key_value  ${output}  UUID
  get_key_value  ${output}  VirtualMedia

Verify chassis instance property show up correctly
  ${output} =  run_curl_get  ${resource_Chassis_1}
  Verify the curl output and ensure no error    ${output}
  get_key_value  ${output}  @odata.context
  get_key_value  ${output}  @odata.etag
  get_key_value  ${output}  @odata.id
  get_key_value  ${output}  @odata.type
  get_key_value  ${output}  Actions
  get_key_value  ${output}  AssetTag
  get_key_value  ${output}  ChassisType
  get_key_value  ${output}  Description
  get_key_value  ${output}  Id
  get_key_value  ${output}  IndicatorLED
  get_key_value  ${output}  IndicatorLED@Redfish.AllowableValues
  get_key_value  ${output}  Links
  get_key_value  ${output}  LogServices
  get_key_value  ${output}  Manufacturer
  get_key_value  ${output}  Model
  get_key_value  ${output}  Name
  get_key_value  ${output}  NetworkAdapters
  get_key_value  ${output}  PCIeDevices
  get_key_value  ${output}  PCIeSlots
  get_key_value  ${output}  PartNumber
  get_key_value  ${output}  PhysicalSecurity
  get_key_value  ${output}  Power
  get_key_value  ${output}  PowerState
  get_key_value  ${output}  SKU
  get_key_value  ${output}  Sensors
  get_key_value  ${output}  SerialNumber
  get_key_value  ${output}  Status
  get_key_value  ${output}  Thermal

Verify power control info show up correctly
  [Arguments]    ${output}
  get_key_value  ${output}  @odata.context
  get_key_value  ${output}  @odata.etag
  get_key_value  ${output}  @odata.id
  get_key_value  ${output}  @odata.type
  get_key_value  ${output}  Description
  get_key_value  ${output}  Id
  get_key_value  ${output}  Name
  
Verify power supply info show up correctly
  [Arguments]    ${output}
  get_key_value  ${output}  PowerControl
  get_key_value  ${output}  PowerControl@odata.count
  get_key_value  ${output}  PowerSupplies
  get_key_value  ${output}  PowerSupplies@odata.count
  
Verify voltage info show up correctly
  [Arguments]    ${output}
  get_key_value  ${output}  Voltages
  get_key_value  ${output}  Voltages@odata.count

Verify fan and temperature sensor info show up correctly
  [Arguments]    ${output}
  get_key_value  ${output}  @odata.context
  get_key_value  ${output}  @odata.etag
  get_key_value  ${output}  @odata.id
  get_key_value  ${output}  @odata.type
  get_key_value  ${output}  Description
  get_key_value  ${output}  Fans
  get_key_value  ${output}  Id
  get_key_value  ${output}  Name
  get_key_value  ${output}  Temperatures

Verify Resource Zone Collection
  OS Connect Device
  ${output} =  run_curl_get  ${Resource_Zone_Collection}
  get_key_value  ${output}  @odata.context
  get_key_value  ${output}  @odata.etag
  get_key_value  ${output}  @odata.id
  get_key_value  ${output}  @odata.type
  get_key_value  ${output}  Description
  get_key_value  ${output}  Members
  get_key_value  ${output}  Members@odata.count
  get_key_value  ${output}  Name
  OS Disconnect Device

Verify Resource Zone Collection instance
  OS Connect Device
  ${output} =  run_curl_get  ${Resource_Zone_Collection_instance}
  get_key_value  ${output}  @Redfish.CollectionCapabilities
  get_key_value  ${output}  @odata.type
  get_key_value  ${output}  Capabilities
  get_key_value  ${output}  CapabilitiesObject
  get_key_value  ${output}  @odata.id
  get_key_value  ${output}  Links
  get_key_value  ${output}  TargetCollection
  get_key_value  ${output}  @odata.id
  get_key_value  ${output}  UseCase
  get_key_value  ${output}  MaxMembers
  get_key_value  ${output}  @odata.context
  get_key_value  ${output}  @odata.etag
  get_key_value  ${output}  @odata.id
  get_key_value  ${output}  @odata.type
  get_key_value  ${output}  Description
  get_key_value  ${output}  Id
  get_key_value  ${output}  Links
  get_key_value  ${output}  ResourceBlocks
  get_key_value  ${output}  @odata.id
  get_key_value  ${output}  @odata.id
  get_key_value  ${output}  @odata.id
  get_key_value  ${output}  Name
  get_key_value  ${output}  Status
  get_key_value  ${output}  Health
  get_key_value  ${output}  HealthRollup
  get_key_value  ${output}  State
  OS Disconnect Device

Verify capabilites
  OS Connect Device
  ${output} =  run_curl_get  ${Capabilities}
  get_key_value  ${output}  @odata.context
  get_key_value  ${output}  @odata.etag
  get_key_value  ${output}  @odata.id
  get_key_value  ${output}  @odata.type
  get_key_value  ${output}  Boot
  get_key_value  ${output}  BootSourceOverrideEnabled@Redfish.AllowableValues
  get_key_value  ${output}  BootSourceOverrideEnabled@Redfish.OptionalOnCreate
  get_key_value  ${output}  BootSourceOverrideEnabled@Redfish.UpdatableAfterCreate
  get_key_value  ${output}  BootSourceOverrideTarget@Redfish.AllowableValues
  get_key_value  ${output}  BootSourceOverrideTarget@Redfish.OptionalOnCreate
  get_key_value  ${output}  BootSourceOverrideTarget@Redfish.UpdatableAfterCreate
  get_key_value  ${output}  Boot@Redfish.OptionalOnCreate
  get_key_value  ${output}  Description
  get_key_value  ${output}  Description@Redfish.OptionalOnCreate
  get_key_value  ${output}  Description@Redfish.SetOnlyOnCreate
  get_key_value  ${output}  HostName@Redfish.OptionalOnCreate
  get_key_value  ${output}  HostName@Redfish.UpdatableAfterCreate
  get_key_value  ${output}  Id
  get_key_value  ${output}  Links
  get_key_value  ${output}  ResourceBlocks@Redfish.RequiredOnCreate
  get_key_value  ${output}  ResourceBlocks@Redfish.UpdatableAfterCreate
  get_key_value  ${output}  Links@Redfish.RequiredOnCreate
  get_key_value  ${output}  Name
  get_key_value  ${output}  Name@Redfish.RequiredOnCreate
  get_key_value  ${output}  Name@Redfish.SetOnlyOnCreate
  OS Disconnect Device

Verify Configurations_1
  OS Connect Device
  ${output} =  run_curl_get  ${Configurations_1}
  get_key_value  ${output}  @odata.context
  get_key_value  ${output}  @odata.etag
  get_key_value  ${output}  @odata.id
  get_key_value  ${output}  @odata.type
  get_key_value  ${output}  CertificateAuthorityUrl
  get_key_value  ${output}  Id
  get_key_value  ${output}  Name
  OS Disconnect Device

Verify AccountService Configurations_1
  OS Connect Device
  ${output} =  run_curl_get  ${AccountService_Configurations_1}
  get_key_value  ${output}  @odata.context
  get_key_value  ${output}  @odata.etag
  get_key_value  ${output}  @odata.id
  get_key_value  ${output}  @odata.type
  get_key_value  ${output}  Id
  get_key_value  ${output}  Name
  get_key_value  ${output}  PAMEnabled
  get_key_value  ${output}  PAMOrder
  OS Disconnect Device

Verify CertificateService_1
  OS Connect Device
  ${output} =  run_curl_get  ${CertificateService_1}
  get_key_value  ${output}  @odata.context
  get_key_value  ${output}  @odata.etag
  get_key_value  ${output}  @odata.id
  get_key_value  ${output}  @odata.type
  get_key_value  ${output}  Actions
  get_key_value  ${output}  \#CertificateService.GenerateCSR
  get_key_value  ${output}  @Redfish.ActionInfo
  get_key_value  ${output}  target
  get_key_value  ${output}  \#CertificateService.ReplaceCertificate
  get_key_value  ${output}  @Redfish.ActionInfo
  get_key_value  ${output}  target
  get_key_value  ${output}  CertificateLocations
  get_key_value  ${output}  @odata.id
  get_key_value  ${output}  Description
  get_key_value  ${output}  Id
  get_key_value  ${output}  Name
  OS Disconnect Device

Delete the previously created EventService Task
  ${output_1} =    run_curl_post  ${resource_5}  ${data_EventService_SubmitTestEvent}
  ${Task_id} =  get_key_value  ${output_1}  Id
  Log  ${Task_id}
  ${output_2} =  run_curl_get  ${resource_6}/${Task_id}
  ${act_value} =  get_key_value  ${output_2}  Name
  check_values_are_equal  ${act_value}  EventService SubmitTestEvent Action
  ${output_2} =  run_curl_get  ${resource_6}
  ${members} =  get_key_value  ${output_2}  Members
  Log    ${members}

  run_curl_delete  ${resource_6}/${Task_id}
  ${output_2} =  run_curl_get  ${resource_6}
  ${members} =  get_key_value  ${output_2}  Members
  Log    ${members}
  ${output_3} =  run_curl_get  ${resource_3}/${Task_id}
  get_key_value  ${output_3}  error

Verify all network interfaces properties
  [Arguments]    ${resource_ethernet_interface}
  ${output} =  run_curl_get  ${resource_ethernet_interface}
  check error in curl output    ${output}
  get_key_value  ${output}   @odata.context
  get_key_value  ${output}   @odata.etag
  get_key_value  ${output}   @odata.id
  get_key_value  ${output}   @odata.type
  get_key_value  ${output}   DHCPv4
  get_key_value  ${output}   IPv4Addresses
  get_key_value  ${output}   Address
  get_key_value  ${output}   AddressOrigin
  get_key_value  ${output}   SubnetMask
  get_key_value  ${output}   IPv6Addresses
  get_key_value  ${output}   PrefixLength
  get_key_value  ${output}   IPv6DefaultGateway
  get_key_value  ${output}   Id
  get_key_value  ${output}   InterfaceEnabled
  get_key_value  ${output}   LinkStatus
  get_key_value  ${output}   Links
  get_key_value  ${output}   Chassis
  get_key_value  ${output}   Endpoints@odata.count
  get_key_value  ${output}   MACAddress
  get_key_value  ${output}   MTUSize
  get_key_value  ${output}   Name
  get_key_value  ${output}   PermanentMACAddress
  get_key_value  ${output}   Status
  get_key_value  ${output}   Health
  get_key_value  ${output}   State
  get_key_value  ${output}   UefiDevicePath
  get_key_value  ${output}   VLANs

Verify bios attribution
  ${output} =  run_curl_get  ${resource_bios}
  check error in curl output    ${output}
  get_key_value  ${output}   @Redfish.Settings
  get_key_value  ${output}   @odata.type
  get_key_value  ${output}   SettingsObject
  get_key_value  ${output}   @odata.id
  get_key_value  ${output}   @odata.context
  get_key_value  ${output}   @odata.etag
  get_key_value  ${output}   @odata.id
  get_key_value  ${output}   @odata.type
  get_key_value  ${output}   Actions
  get_key_value  ${output}   \#Bios.ChangePassword
  get_key_value  ${output}   @Redfish.ActionInfo
  get_key_value  ${output}   target
  get_key_value  ${output}   \#Bios.ResetBios
  get_key_value  ${output}   AttributeRegistry
  get_key_value  ${output}   Attributes
  get_key_value  ${output}   Description
  get_key_value  ${output}   Id
  get_key_value  ${output}   Name

verify bios property
  ${output} =  run_curl_get  ${resource_bios_property}
  check error in curl output    ${output}
  get_key_value  ${output}   @odata.context
  get_key_value  ${output}   @odata.etag
  get_key_value  ${output}   @odata.id
  get_key_value  ${output}   @odata.type
  get_key_value  ${output}   AttributeRegistry
  get_key_value  ${output}   Attributes
  get_key_value  ${output}   Description
  get_key_value  ${output}   Id
  get_key_value  ${output}   Name

verify log properties
  [Arguments]   ${resource_log_property}
  ${output} =  run_curl_get  ${resource_log_property}
  check error in curl output    ${output}
  get_key_value  ${output}   @odata.context
  get_key_value  ${output}   @odata.etag
  get_key_value  ${output}   @odata.id
  get_key_value  ${output}   @odata.type
  get_key_value  ${output}   Actions
  get_key_value  ${output}   \#LogService.ClearLog
  get_key_value  ${output}   @Redfish.ActionInfo
  get_key_value  ${output}   @Redfish.OperationApplyTimeSupport
  get_key_value  ${output}   MaintenanceWindowDurationInSeconds
  get_key_value  ${output}   MaintenanceWindowResource
  get_key_value  ${output}   SupportedValues
  get_key_value  ${output}   target
  get_key_value  ${output}   DateTime
  get_key_value  ${output}   DateTimeLocalOffset
  get_key_value  ${output}   Description
  get_key_value  ${output}   Entries
  get_key_value  ${output}   Id
  get_key_value  ${output}   LogEntryType
  get_key_value  ${output}   MaxNumberOfRecords
  get_key_value  ${output}   Name
  get_key_value  ${output}   OverWritePolicy
  get_key_value  ${output}   ServiceEnabled
  get_key_value  ${output}   Status
  get_key_value  ${output}   Health
  get_key_value  ${output}   State

Verify sub processor instance property
  [Arguments]   ${resource_subprocess_instance}
  ${output} =  run_curl_get  ${resource_subprocess_instance}
  check error in curl output    ${output}
  get_key_value  ${output}   @odata.context
  get_key_value  ${output}   @odata.etag
  get_key_value  ${output}   @odata.id
  get_key_value  ${output}   @odata.type
  get_key_value  ${output}   Id
  get_key_value  ${output}   Links
  get_key_value  ${output}   Chassis
  get_key_value  ${output}   ConnectedProcessors
  get_key_value  ${output}   MaxSpeedMHz
  get_key_value  ${output}   Name
  get_key_value  ${output}   ProcessorType
  get_key_value  ${output}   ConnectedProcessors@odata.count
  get_key_value  ${output}   TotalThreads

Verify manager network protocal info show up correctly
  ${ip}  get_ip_address_from_ipmitool  DUT
  ${curl_output} =  run_curl_BMCIP_get  ${resource_NetworkProtocol}  ${ip}
  Verify the curl output and ensure no error    ${curl_output}
  Verify networkprotocol info under manager show up correctly    ${curl_output}

Verify networkprotocol info under manager show up correctly
  [Arguments]    ${output}
  get_key_value  ${output}  @odata.context
  get_key_value  ${output}  @odata.etag
  get_key_value  ${output}  @odata.id
  get_key_value  ${output}  @odata.type
  get_key_value  ${output}  Description
  get_key_value  ${output}  FQDN
  get_key_value  ${output}  HTTPS
  get_key_value  ${output}  HostName
  get_key_value  ${output}  IPMI
  get_key_value  ${output}  Id
  get_key_value  ${output}  KVMIP
  get_key_value  ${output}  NTP
  get_key_value  ${output}  Name
  get_key_value  ${output}  SNMP 
  get_key_value  ${output}  SSDP
  get_key_value  ${output}  Status
  get_key_value  ${output}  VirtualMedia

Verify manager serial interfaces info show up correctly
  ${ip}  get_ip_address_from_ipmitool  DUT
  ${curl_output} =  run_curl_BMCIP_get  ${resource_SerialInterfaces}  ${ip}
  Verify the curl output and ensure no error    ${curl_output}
  Verify event collections info show up correctly    ${curl_output}

Verify manager sol info can be changed successfully
  run_curl_patch  ${source_IPMI_SOL}  ${data_BitRate_set1}
  ${curl_output} =  run_curl_get  ${source_IPMI_SOL}
  ${act_value} =  get_key_value  ${curl_output}  BitRate
  Log  ${act_value}
  check_values_are_equal  ${act_value}  ${data_BitRate_output1}
  Verify the curl output and ensure no error    ${curl_output}
  run_curl_patch  ${source_IPMI_SOL}  ${data_BitRate_set2}
  ${curl_output} =  run_curl_get  ${source_IPMI_SOL}
  ${act_value} =  get_key_value  ${curl_output}  BitRate
  Log  ${act_value}
  check_values_are_equal  ${act_value}  ${data_BitRate_output2}
  Verify the curl output and ensure no error    ${curl_output}
  Verify IPMI-SOL info under SerialInterface show up correctly    ${curl_output}

Verify IPMI-SOL info under SerialInterface show up correctly
  [Arguments]    ${output}
  get_key_value  ${output}  @odata.context
  get_key_value  ${output}  @odata.etag
  get_key_value  ${output}  @odata.id
  get_key_value  ${output}  @odata.type
  get_key_value  ${output}  BitRate
  get_key_value  ${output}  DataBits
  get_key_value  ${output}  Description
  get_key_value  ${output}  FlowControl
  get_key_value  ${output}  Id
  get_key_value  ${output}  InterfaceEnabled
  get_key_value  ${output}  Name
  get_key_value  ${output}  Parity
  get_key_value  ${output}  StopBits

Verfiy manager sol can be disable successfully
  Set UpdateService InterfaceEnabled to False
  Check UpdateService InterfaceEnabled value as False	
  
Set UpdateService InterfaceEnabled to False
  run_curl_patch  ${source_IPMI_SOL}  ${data_InterfaceEnabled_false}

Check UpdateService InterfaceEnabled value as False
  ${curl_output} =  run_curl_get  ${source_IPMI_SOL}
  ${act_value} =  get_key_value  ${curl_output}  InterfaceEnabled
  Log  ${act_value}
  check_values_are_equal  ${act_value}  ${false_value}
  Verify the curl output and ensure no error    ${curl_output}

Verfiy manager sol can be enable successfully
  Set UpdateService InterfaceEnabled to True
  Check UpdateService InterfaceEnabled value as True
  
Set UpdateService InterfaceEnabled to True
  run_curl_patch  ${source_IPMI_SOL}  ${data_InterfaceEnabled_true}

Check UpdateService InterfaceEnabled value as True
  ${curl_output} =  run_curl_get  ${source_IPMI_SOL}
  ${act_value} =  get_key_value  ${curl_output}  InterfaceEnabled
  Log  ${act_value}
  check_values_are_equal  ${act_value}  ${true_value}
  Verify the curl output and ensure no error    ${curl_output}

Verify chassis assettag can be modified successfully
  run_curl_patch  ${resource_Chassis_1}  ${data_AssetTag_set1}
  ${output} =  run_curl_get  ${resource_Chassis_1}
  ${act_value} =  get_key_value  ${output}  AssetTag
  Log  ${act_value}
  check_values_are_equal  ${act_value}  ${data_AssetTag_output1}
  run_curl_patch  ${resource_Chassis_1}  ${data_AssetTag_set2}
  ${output} =  run_curl_get  ${resource_Chassis_1}
  ${act_value} =  get_key_value  ${output}  AssetTag
  Log  ${act_value}
  check_values_are_equal  ${act_value}  ${data_AssetTag_output2}

Verify account service info show up correctly
  [Arguments]    ${output}
  get_key_value  ${output}  @odata.context
  get_key_value  ${output}  @odata.etag
  get_key_value  ${output}  @odata.id
  get_key_value  ${output}  @odata.type
  get_key_value  ${output}  AccountLockoutCounterResetAfter
  get_key_value  ${output}  AccountLockoutCounterResetEnabled
  get_key_value  ${output}  AccountLockoutDuration
  get_key_value  ${output}  AccountLockoutThreshold
  get_key_value  ${output}  Accounts
  get_key_value  ${output}  ActiveDirectory
  get_key_value  ${output}  AdditionalExternalAccountProviders
  get_key_value  ${output}  AuthFailureLoggingThreshold
  get_key_value  ${output}  AuthFailureLoggingThreshold
  get_key_value  ${output}  Description
  get_key_value  ${output}  Id
  get_key_value  ${output}  LDAP
  get_key_value  ${output}  LocalAccountAuth
  get_key_value  ${output}  MaxPasswordLength
  get_key_value  ${output}  MinPasswordLength
  get_key_value  ${output}  Name
  get_key_value  ${output}  Oem
  get_key_value  ${output}  PrivilegeMap
  get_key_value  ${output}  Roles
  get_key_value  ${output}  ServiceEnabled
  get_key_value  ${output}  Status

Set ServiceEnabled to True
  [Arguments]   ${resource}
  run_curl_patch  ${resource}  ${data_ServiceEnabled_true}

Set ServiceEnabled to False
  [Arguments]   ${resource}
  run_curl_patch  ${resource}  ${data_ServiceEnabled_false}

Check ServiceEnabled value as True
  [Arguments]   ${resource}
  ${output} =  run_curl_get  ${resource}
  ${act_value} =  get_key_value  ${output}  ServiceEnabled
  Log  ${act_value}
  check_values_are_equal  ${act_value}  ${true_value}

Check ServiceEnabled value as False
  [Arguments]   ${resource}
  ${output} =  run_curl_get  ${resource}
  ${act_value} =  get_key_value  ${output}  ServiceEnabled
  Log  ${act_value}
  check_values_are_equal  ${act_value}  ${false_value}

Verify GET on JsonSchemas
  ${output_1} =    run_curl_get  ${resource_8}
  get_key_value  ${output_1}  @odata.context
  get_key_value  ${output_1}  @odata.etag
  ${act_value} =  get_key_value  ${output_1}  @odata.id
  check_values_are_equal  ${act_value}  ${resource_8}
  get_key_value  ${output_1}  @odata.type
  get_key_value  ${output_1}  Description
  get_key_value  ${output_1}  Members
  get_key_value  ${output_1}  Members@odata.count
  ${act_value} =  get_key_value  ${output_1}  Name
  check_values_are_equal  ${act_value}  Schema Repository

Verify GET on JsonSchemas Members
  ${output_1} =    run_curl_get  ${resource_8}
  ${members} =  get_key_value  ${output_1}  Members
  FOR    ${INDEX}    IN  @{members}
    ${output} =    run_curl_get  ${INDEX}[@odata.id]
    get_key_value  ${output}  @odata.context
    get_key_value  ${output}  @odata.etag
    get_key_value  ${output}  @odata.type
    get_key_value  ${output}  Description
    get_key_value  ${output}  Id
    get_key_value  ${output}  Languages
    get_key_value  ${output}  Location
    get_key_value  ${output}  Name
    get_key_value  ${output}  Schema
  END

verify time and timeoffset
  [Arguments]   ${resource}    ${DateTime_offset}    ${expect_datetime}  ${expect_offset}
  run_curl_patch  ${resource}  ${DateTime_offset}
  ${output} =  run_curl_get  ${resource}
  ${act_value_DateTime} =  get_key_value  ${output}  DateTime
  ${act_value_DateTimeLocalOffset} =  get_key_value  ${output}  DateTimeLocalOffset
  Log  ${act_value_DateTime}
  Log  ${act_value_DateTimeLocalOffset}
  common_check_patern_2     ${act_value_DateTime}    ${expect_datetime}     Verify DateTime value    expect=True
  check_values_are_equal  ${act_value_DateTimeLocalOffset}   ${expect_offset}

Verify log entries show up correctly
  ${ip}  get_ip_address_from_ipmitool  DUT
  ${curl_output} =  run_curl_BMCIP_get  ${resource_LogEntry_Collection_1}  ${ip}
  Verify the curl output and ensure no error    ${curl_output}
  Verify event collections info show up correctly    ${curl_output}

Verify account instance info show up correctly
  ${ip}  get_ip_address_from_ipmitool  DUT
  ${curl_output} =  run_curl_BMCIP_get  ${resource_Accountinstance}  ${ip}
  Verify the curl output and ensure no error    ${curl_output}
  Verify event collections info show up correctly    ${curl_output}
  ${members} =  get_key_value  ${curl_output}  Members
  FOR    ${INDEX}    IN  @{members}
    ${curl_output} =    run_curl_BMCIP_get  ${INDEX}[@odata.id]  ${ip}
    Verify each account info show up correctly    ${curl_output}
    Verify the curl output and ensure no error    ${curl_output}
  END

Verify each account info show up correctly
  [Arguments]    ${output}
  get_key_value  ${output}  @odata.context
  get_key_value  ${output}  @odata.etag
  get_key_value  ${output}  @odata.id
  get_key_value  ${output}  @odata.type
  get_key_value  ${output}  Certificates
  get_key_value  ${output}  Description
  get_key_value  ${output}  Enabled
  get_key_value  ${output}  Id
  get_key_value  ${output}  Links
  get_key_value  ${output}  Locked
  get_key_value  ${output}  Name

Verify account roles info show up correctly
  ${ip}  get_ip_address_from_ipmitool  DUT
  ${curl_output} =  run_curl_BMCIP_get  ${resource_AccountRoles}  ${ip}
  Verify the curl output and ensure no error    ${curl_output}
  Verify event collections info show up correctly    ${curl_output}

Verify account role info show up correctly
  ${ip}  get_ip_address_from_ipmitool  DUT
  ${curl_output} =  run_curl_BMCIP_get  ${resource_Role_Collection_3}  ${ip}
  Verify the curl output and ensure no error    ${curl_output}
  Verify event collections info show up correctly    ${curl_output}
  ${members} =  get_key_value  ${curl_output}  Members
  FOR    ${INDEX}    IN  @{members}
    Log  ${INDEX}
    ${curl_output} =    run_curl_BMCIP_get  ${INDEX}[@odata.id]  ${ip}
    Verify event role info show up correctly    ${curl_output}
    Verify the curl output and ensure no error    ${curl_output}
  END

Verify event role info show up correctly
  [Arguments]    ${output}
  get_key_value  ${output}  @odata.context
  get_key_value  ${output}  @odata.etag
  get_key_value  ${output}  @odata.id
  get_key_value  ${output}  @odata.type
  get_key_value  ${output}  AssignedPrivileges
  get_key_value  ${output}  Description
  get_key_value  ${output}  Id
  get_key_value  ${output}  IsPredefined
  get_key_value  ${output}  Name
  get_key_value  ${output}  RoleId

verify firmware inventory instance
  ${output_1} =    run_curl_get  ${resource_FirmwareInventory_collections}
  ${members} =  get_key_value  ${output_1}  Members
  FOR    ${INDEX}    IN  @{members}
    ${output} =    run_curl_get  ${INDEX}[@odata.id]
    get_key_value  ${output}  @odata.context
    get_key_value  ${output}  @odata.etag
    get_key_value  ${output}  @odata.type
    get_key_value  ${output}  @odata.id
    get_key_value  ${output}  Id
    get_key_value  ${output}  Name
    get_key_value  ${output}  Updateable
  END

Verify secure boot info
  ${output} =  run_curl_get  ${resource_secureboot}
  get_key_value  ${output}  @odata.context
  get_key_value  ${output}  @odata.etag
  get_key_value  ${output}  @odata.type
  get_key_value  ${output}  @odata.id
  get_key_value  ${output}  Actions
  get_key_value  ${output}  \#SecureBoot.ResetKeys
  get_key_value  ${output}  @Redfish.ActionInfo
  get_key_value  ${output}  target
  get_key_value  ${output}  Description
  get_key_value  ${output}  Id
  get_key_value  ${output}  Name
  get_key_value  ${output}  SecureBootCurrentBoot
  get_key_value  ${output}  SecureBootEnable
  get_key_value  ${output}  SecureBootMode

Verify GET on SessionService's Sessions
  ${output_1} =    run_curl_get  ${resource_9}
  get_key_value  ${output_1}  @odata.context
  get_key_value  ${output_1}  @odata.etag
  get_key_value  ${output_1}  @odata.id
  get_key_value  ${output_1}  @odata.type
  get_key_value  ${output_1}  Description
  get_key_value  ${output_1}  Members
  ${act_value} =  get_key_value  ${output_1}  Name
  check_values_are_equal  ${act_value}  Session Collection

Verify TelemetryService_1
  OS Connect Device
  ${output} =  run_curl_get  ${TelemetryService_1}
  get_key_value  ${output}  @odata.context
  get_key_value  ${output}  @odata.etag
  get_key_value  ${output}  @odata.id
  get_key_value  ${output}  @odata.type
  get_key_value  ${output}  Actions
  get_key_value  ${output}  \#TelemetryService.SubmitTestMetricReport
  get_key_value  ${output}  @Redfish.ActionInfo
  get_key_value  ${output}  target
  get_key_value  ${output}  Description
  get_key_value  ${output}  Id
  get_key_value  ${output}  LogService
  get_key_value  ${output}  @odata.id
  get_key_value  ${output}  MaxReports
  get_key_value  ${output}  MetricDefinitions
  get_key_value  ${output}  @odata.id
  get_key_value  ${output}  MetricReportDefinitions
  get_key_value  ${output}  @odata.id
  get_key_value  ${output}  MetricReports
  get_key_value  ${output}  @odata.id
  get_key_value  ${output}  MinCollectionInterval
  get_key_value  ${output}  Name
  get_key_value  ${output}  ServiceEnabled
  get_key_value  ${output}  Status
  get_key_value  ${output}  Health
  get_key_value  ${output}  State
  get_key_value  ${output}  SupportedCollectionFunctions
  get_key_value  ${output}  SupportedCollectionFunctions@Redfish.AllowableValues
  get_key_value  ${output}  Triggers
  get_key_value  ${output}  @odata.id
  OS Disconnect Device

Verify AccountService_4
  OS Connect Device
  ${output} =  run_curl_get  ${AccountService_4}
  get_key_value  ${output}  @odata.context
  get_key_value  ${output}  @odata.etag
  get_key_value  ${output}  @odata.id
  get_key_value  ${output}  @odata.type
  get_key_value  ${output}  Description
  get_key_value  ${output}  Members
  get_key_value  ${output}  @odata.id
  get_key_value  ${output}  @odata.id
  get_key_value  ${output}  Members@odata.count
  get_key_value  ${output}  Name
  OS Disconnect Device

Verify Manager_Account_Collection_1
  OS Connect Device
  ${output} =  run_curl_get  ${Manager_Account_Collection_1}
  get_key_value  ${output}  @odata.context
  get_key_value  ${output}  @odata.etag
  get_key_value  ${output}  @odata.id
  get_key_value  ${output}  @odata.type
  get_key_value  ${output}  Description
  get_key_value  ${output}  Members
  get_key_value  ${output}  @odata.id
  get_key_value  ${output}  @odata.id
  get_key_value  ${output}  Members@odata.count
  get_key_value  ${output}  Name
  OS Disconnect Device

Verify ManagerCollection
  OS Connect Device
  ${output} =  run_curl_get  ${ManagerCollection}
  get_key_value  ${output}  @odata.context
  get_key_value  ${output}  @odata.etag
  get_key_value  ${output}  @odata.id
  get_key_value  ${output}  @odata.type
  get_key_value  ${output}  Description
  get_key_value  ${output}  Members
  get_key_value  ${output}  @odata.id
  get_key_value  ${output}  Members@odata.count
  get_key_value  ${output}  Name
  OS Disconnect Device

Verify HostInterface_Collection
  OS Connect Device
  ${output} =  run_curl_get  ${HostInterface_Collection}
  get_key_value  ${output}  @odata.context
  get_key_value  ${output}  @odata.etag
  get_key_value  ${output}  @odata.id
  get_key_value  ${output}  @odata.type
  get_key_value  ${output}  Description
  get_key_value  ${output}  Members
  get_key_value  ${output}  @odata.id
  get_key_value  ${output}  Members@odata.count
  get_key_value  ${output}  Name
  OS Disconnect Device

Verify HostInterface
  OS Connect Device
  ${output} =  run_curl_get  ${HostInterface}
  get_key_value  ${output}  @odata.context
  get_key_value  ${output}  @odata.etag
  get_key_value  ${output}  @odata.id
  get_key_value  ${output}  @odata.type
  get_key_value  ${output}  AuthNoneRoleId
  get_key_value  ${output}  AuthenticationModes
  get_key_value  ${output}  Description
  get_key_value  ${output}  ExternallyAccessible
  get_key_value  ${output}  FirmwareAuthEnabled
  get_key_value  ${output}  FirmwareAuthRoleId
  get_key_value  ${output}  HostEthernetInterfaces
  get_key_value  ${output}  @odata.id
  get_key_value  ${output}  HostInterfaceType
  get_key_value  ${output}  Id
  get_key_value  ${output}  InterfaceEnabled
  get_key_value  ${output}  KernelAuthEnabled
  get_key_value  ${output}  KernelAuthRoleId
  get_key_value  ${output}  Links
  get_key_value  ${output}  ComputerSystems
  get_key_value  ${output}  @odata.id
  get_key_value  ${output}  ComputerSystems@odata.count
  get_key_value  ${output}  FirmwareAuthRole
  get_key_value  ${output}  @odata.id
  get_key_value  ${output}  KernelAuthRole
  get_key_value  ${output}  @odata.id
  get_key_value  ${output}  ManagerEthernetInterface
  get_key_value  ${output}  @odata.id
  get_key_value  ${output}  Name
  get_key_value  ${output}  NetworkProtocol
  get_key_value  ${output}  @odata.id
  get_key_value  ${output}  Status
  get_key_value  ${output}  Health
  get_key_value  ${output}  State
  OS Disconnect Device

Verify HostEthernetInterfaceCollection
  OS Connect Device
  ${output} =  run_curl_get  ${HostEthernetInterfaceCollection}
  get_key_value  ${output}  @odata.context
  get_key_value  ${output}  @odata.etag
  get_key_value  ${output}  @odata.id
  get_key_value  ${output}  @odata.type
  get_key_value  ${output}  Description
  get_key_value  ${output}  Members
  get_key_value  ${output}  @odata.id
  get_key_value  ${output}  Members@odata.count
  get_key_value  ${output}  Name
  OS Disconnect Device

Verify ManagerEthernetInterface_Instance
  OS Connect Device
  ${output} =  run_curl_get  ${ManagerEthernetInterface_Instance}
  get_key_value  ${output}  @odata.context
  get_key_value  ${output}  @odata.etag
  get_key_value  ${output}  @odata.id
  get_key_value  ${output}  @odata.type
  get_key_value  ${output}  IPv4Addresses
  get_key_value  ${output}  Address
  get_key_value  ${output}  SubnetMask
  get_key_value  ${output}  Id
  get_key_value  ${output}  InterfaceEnabled
  get_key_value  ${output}  MACAddress
  get_key_value  ${output}  Name
  get_key_value  ${output}  StatelessAddressAutoConfig
  get_key_value  ${output}  IPv4AutoConfigEnabled
  get_key_value  ${output}  IPv6AutoConfigEnabled
  get_key_value  ${output}  Status
  get_key_value  ${output}  Health
  get_key_value  ${output}  State
  OS Disconnect Device

Verify account instance can be deleted successfully
  Create a new account creation and Verify
  ${curl_output1} =  run_curl_get  ${resource_Accountinstance}
  Verify the curl output and ensure no error    ${curl_output1}
  Verify event collections info show up correctly    ${curl_output1}
  ${members} =  get_key_value  ${curl_output1}  Members
  ${first_id} =    set variable  ${members}[0]
  ${first_id_value} =    set variable  ${first_id}[@odata.id]
  ${curl_output2} =  run_curl_get  ${first_id_value}
  Verify accountservice instance role info show up correctly  ${curl_output2}
  run_curl_delete  ${first_id_value}
  ${curl_output} =  run_curl_get  ${resource_Accountinstance}
  ${curl_output} =  run_curl_get  ${first_id_value}
  check_output_from_curl  ${curl_output}  error

Verify accountservice instance role info show up correctly
  [Arguments]    ${output}
  get_key_value  ${output}  @odata.context
  get_key_value  ${output}  @odata.etag
  get_key_value  ${output}  @odata.id
  get_key_value  ${output}  @odata.type
  get_key_value  ${output}  Certificates
  get_key_value  ${output}  Description
  get_key_value  ${output}  Enabled
  get_key_value  ${output}  Id
  get_key_value  ${output}  Links
  get_key_value  ${output}  Locked
  get_key_value  ${output}  Name
  get_key_value  ${output}  Password
  get_key_value  ${output}  RoleId
  get_key_value  ${output}  UserName

Create a new account creation and Verify
  ${output_1} =    run_curl_post  ${resource_Accountinstance}  ${data_NewAccount}
  ${Subs_id} =  get_key_value  ${output_1}  Id
  Log  ${Subs_id}
  ${output_2} =  run_curl_get  ${resource_Accountinstance}/${Subs_id}
  ${act_value} =  get_key_value  ${output_2}  Name
  check_values_are_equal  ${act_value}  TestUserAccount

Verify new system can be created successfully
  ${curl_output1} =  run_curl_get  ${resource_service_system}
  Verify the curl output and ensure no error    ${curl_output1}
  ${members} =  get_key_value  ${curl_output1}  Members
  Log  ${members}
  ${first_id} =    set variable  ${members}[0]
  Log  ${first_id}
  ${first_id_value} =    set variable  ${first_id}[@odata.id]
  Log  ${first_id_value}
  run_curl_delete  ${first_id_value}
  Create a new systems and verify collections
  run_curl_delete  ${first_id_value}
  Create a new systems and verify collections
  ${curl_output2} =  run_curl_get  ${resource_service_system}
  Verify the curl output and ensure no error    ${curl_output2}

Create a new systems and verify collections
  ${output_1} =    run_curl_post  ${resource_service_system}  ${data_NewSystem}
  Verify new event system  ${output_1}
  ${Subs_id} =  get_key_value  ${output_1}  Id
  Log  ${Subs_id}
  ${output_2} =  run_curl_get  ${resource_service_system}/${Subs_id}
  ${act_value} =  get_key_value  ${output_2}  Name
  check_values_are_equal  ${act_value}  NewSystem

Verify new event system
  [Arguments]    ${output}
  get_key_value  ${output}  @odata.context
  get_key_value  ${output}  @odata.etag
  get_key_value  ${output}  @odata.id
  get_key_value  ${output}  @odata.type
  get_key_value  ${output}  Actions
  get_key_value  ${output}  Boot
  get_key_value  ${output}  Description
  get_key_value  ${output}  HostName
  get_key_value  ${output}  Id
  get_key_value  ${output}  Links
  get_key_value  ${output}  Memory
  get_key_value  ${output}  Name
  get_key_value  ${output}  PowerState
  get_key_value  ${output}  Processors
  get_key_value  ${output}  SimpleStorage
  get_key_value  ${output}  Storage
  get_key_value  ${output}  SystemType
  get_key_value  ${output}  UUID

Verify new account can be created
  ${curl_output1} =  run_curl_get  ${resource_Accountinstance}
  Verify the curl output and ensure no error    ${curl_output1}
  Verify event collections info show up correctly  ${curl_output1}
  ${output_1} =    run_curl_post  ${resource_Accountinstance}  ${data_NewAccount}
  ${Subs_id} =  get_key_value  ${output_1}  Id
  ${output_2} =  run_curl_get  ${resource_Accountinstance}/${Subs_id}
  ${act_value} =  get_key_value  ${output_2}  Name
  check_values_are_equal  ${act_value}  TestUserAccount
  Verify the curl output and ensure no error    ${output_1}
  Verify accountservice instance role info show up correctly  ${output_1}
  run_curl_delete  ${resource_Accountinstance}/${Subs_id}
  ${curl_output} =  run_curl_get  ${resource_Accountinstance}/${Subs_id}
  check_output_from_curl  ${curl_output}  error
  ${curl_output1} =  run_curl_get  ${resource_Accountinstance}

Verify account locked after enough unsuccessfu login
  ${ip}  get_ip_address_from_ipmitool  DUT
  ${curl_output} =  run_curl_BMCIP_get  ${resource_accountservice}  ${ip}
  Verify account service info show up correctly  ${curl_output}
  Verify the curl output and ensure no error    ${curl_output}
  FOR    ${INDEX}    IN RANGE    1    6
      Print Loop Info  ${INDEX}
      ${curl_output} =  run_curl_BMCIP_get  ${resource_accountservice}  ${ip}  False
      check_output_from_curl  ${curl_output}  error
  END
  
Verify log entry show up correctly
  ${ip}  get_ip_address_from_ipmitool  DUT
  ${curl_output1} =  run_curl_BMCIP_get  ${LogEntry_Collection_7}  ${ip}
  verify LogEntry sub processor collection  ${curl_output1}
  Verify the curl output and ensure no error    ${curl_output1}
  ${curl_output2} =  run_curl_BMCIP_get  ${LogEntry_Collection_7}/1  ${ip}
  Verify log entry instance info show up correctly    ${curl_output2}
  Verify the curl output and ensure no error    ${curl_output2}

verify LogEntry sub processor collection
  [Arguments]    ${output}
  get_key_value  ${output}  @odata.context
  get_key_value  ${output}  @odata.etag
  get_key_value  ${output}  @odata.id
  get_key_value  ${output}  @odata.type
  get_key_value  ${output}  Description
  get_key_value  ${output}  Members
  get_key_value  ${output}  Members@odata.nextLink
  get_key_value  ${output}  Name

Verify log entry instance info show up correctly
  [Arguments]    ${output}
  get_key_value  ${output}  @odata.context
  get_key_value  ${output}  @odata.etag
  get_key_value  ${output}  @odata.id
  get_key_value  ${output}  @odata.type
  get_key_value  ${output}  Description
  get_key_value  ${output}  EntryCode
  get_key_value  ${output}  EntryType
  get_key_value  ${output}  EventTimestamp
  get_key_value  ${output}  Id
  get_key_value  ${output}  Message
  get_key_value  ${output}  MessageId
  get_key_value  ${output}  Name
  get_key_value  ${output}  SensorNumber
  get_key_value  ${output}  SensorType
  get_key_value  ${output}  Severity

Verify system network info show up correctly
  ${ip}  get_ip_address_from_ipmitool  DUT
  ${curl_output1} =  run_curl_BMCIP_get  ${resource_InterfaceCollection_1}  ${ip}
  Verify the curl output and ensure no error    ${curl_output1}
  Verify event collections info show up correctly    ${curl_output1}
  ${curl_output2} =  run_curl_BMCIP_get  ${resource_VLANNetwork InterfaceCollection_1}  ${ip}
  Verify the curl output and ensure no error    ${curl_output2}
  Verify event collections info show up correctly    ${curl_output2}
  get_key_value  ${curl_output2}  @Message.ExtendedInfo

Verify system network vlan can be created successfully
  ${ip}  get_ip_address_from_ipmitool  DUT
  ${curl_output1} =  run_curl_BMCIP_get  ${resource_InterfaceCollection_1}  ${ip}
  Verify the curl output and ensure no error    ${curl_output1}
  Verify event collections info show up correctly    ${curl_output1}
  ${curl_output2} =  run_curl_BMCIP_get  ${resource_VLANNetwork_InterfaceCollection_1}  ${ip}
  Verify the curl output and ensure no error    ${curl_output2}
  Verify event collections info show up correctly    ${curl_output2}
  get_key_value  ${curl_output2}  @Message.ExtendedInfo
  ${output_1} =    run_curl_post_BCMIP  ${resource_VLANNetwork_InterfaceCollection_1}  ${data_NewAccount_VLANID}  ${ip}  output_required=False
  ${curl_output3} =  run_curl_BMCIP_get  ${resource_VLANNetwork InterfaceCollection_1}  ${ip}
  Verify the curl output and ensure no error    ${curl_output3}
  ${Members} =  get_key_value  ${curl_output3}  Members
  ${first_id} =    set variable  ${members}[0]
  ${first_id_value} =    set variable  ${first_id}[@odata.id]
  common_check_patern_2      ${first_id_value}      ${data_Members_VLANID_100}      check new network vlan can be created successfully
  run_curl_delete  ${data_Members_VLANID_100}

Verify pcie slots info
  ${output} =  run_curl_get  ${resource_pcieslots}
  get_key_value  ${output}  @odata.context
  get_key_value  ${output}  @odata.etag
  get_key_value  ${output}  @odata.type
  get_key_value  ${output}  @odata.id
  get_key_value  ${output}  Description
  get_key_value  ${output}  Id
  get_key_value  ${output}  Name
  get_key_value  ${output}  Slots
  get_key_value  ${output}  Links
  get_key_value  ${output}  PCIeDevice
  get_key_value  ${output}  PCIeDevice@odata.count
  get_key_value  ${output}  Status
  get_key_value  ${output}  State
  get_key_value  ${output}  Health

Verify chassis sensor instance info
  ${output_1} =    run_curl_get  ${resource_sensor_collections}
  ${members} =  get_key_value  ${output_1}  Members
  FOR    ${INDEX}    IN  @{members}
    ${output} =    run_curl_get  ${INDEX}[@odata.id]
    get_key_value  ${output}  @odata.context
    get_key_value  ${output}  @odata.etag
    get_key_value  ${output}  @odata.type
    get_key_value  ${output}  @odata.id
    get_key_value  ${output}  Id
    get_key_value  ${output}  Name
    get_key_value  ${output}  LoadPercent
    get_key_value  ${output}  Accuracy 
    get_key_value  ${output}  AdjustedMaxAllowableOperatingValue
    get_key_value  ${output}  AdjustedMinAllowableOperatingValue
    get_key_value  ${output}  ApparentVA
    get_key_value  ${output}  Description
    get_key_value  ${output}  ElectricalContext
    get_key_value  ${output}  Location
    get_key_value  ${output}  AltitudeMeters
    get_key_value  ${output}  Contacts
    get_key_value  ${output}  Latitude
    get_key_value  ${output}  Longitude
    get_key_value  ${output}  PartLocation
    get_key_value  ${output}  LocationOrdinalValue
    get_key_value  ${output}  LocationType
    get_key_value  ${output}  Orientation
    get_key_value  ${output}  Reference
    get_key_value  ${output}  ServiceLabel
    get_key_value  ${output}  Placement
    get_key_value  ${output}  Rack
    get_key_value  ${output}  AdditionalInfo
    get_key_value  ${output}  RackOffset
    get_key_value  ${output}  RackOffsetUnits
    get_key_value  ${output}  Row
    get_key_value  ${output}  PostalAddress
    get_key_value  ${output}  AdditionalCode
    get_key_value  ${output}  AdditionalInfo
    get_key_value  ${output}  Building
    get_key_value  ${output}  City 
    get_key_value  ${output}  Community
    get_key_value  ${output}  Country
    get_key_value  ${output}  District
    get_key_value  ${output}  Division
    get_key_value  ${output}  Floor
    get_key_value  ${output}  HouseNumber
    get_key_value  ${output}  HouseNumberSuffix
    get_key_value  ${output}  Landmark
    get_key_value  ${output}  LeadingStreetDirection
    get_key_value  ${output}  Neighborhood
    get_key_value  ${output}  POBox
    get_key_value  ${output}  PlaceType
    get_key_value  ${output}  PostalCode
    get_key_value  ${output}  Road
    get_key_value  ${output}  RoadBranch
    get_key_value  ${output}  RoadPostModifier
    get_key_value  ${output}  RoadPreModifier
    get_key_value  ${output}  RoadSection
    get_key_value  ${output}  RoadSubBranch
    get_key_value  ${output}  Room 
    get_key_value  ${output}  Seat
    get_key_value  ${output}  Street
    get_key_value  ${output}  StreetSuffix 
    get_key_value  ${output}  Territory 
    get_key_value  ${output}  TrailingStreetSuffix
    get_key_value  ${output}  Unit
    get_key_value  ${output}  MaxAllowableOperatingValue
    get_key_value  ${output}  MinAllowableOperatingValue
    get_key_value  ${output}  PeakReading
    get_key_value  ${output}  PeakReadingTime
    get_key_value  ${output}  PhysicalContext
    get_key_value  ${output}  PhysicalSubContext
    get_key_value  ${output}  PowerFactor 
    get_key_value  ${output}  Precision
    get_key_value  ${output}  ReactiveVAR 
    get_key_value  ${output}  Reading
    get_key_value  ${output}  ReadingRangeMax
    get_key_value  ${output}  ReadingRangeMin
    get_key_value  ${output}  ReadingType
    get_key_value  ${output}  ReadingUnits
    get_key_value  ${output}  SensingFrequency
    get_key_value  ${output}  SensorResetTime
    get_key_value  ${output}  Status 
    get_key_value  ${output}  Health
    get_key_value  ${output}  HealthRollup
    get_key_value  ${output}  State
    get_key_value  ${output}  Thresholds
    get_key_value  ${output}  LowerCaution
    get_key_value  ${output}  Activation
    get_key_value  ${output}  DwellTime
    get_key_value  ${output}  Reading
    get_key_value  ${output}  LowerCritical
    get_key_value  ${output}  LowerFatal
    get_key_value  ${output}  UpperCaution
    get_key_value  ${output}  UpperCritical 
    get_key_value  ${output}  UpperFatal
    get_key_value  ${output}  VoltageType
  END

Verify drive instance info NVMe
  [Arguments]    ${resource_storage}
  ${output} =    run_curl_get  ${resource_storage}
  get_key_value  ${output}  @odata.context
  get_key_value  ${output}  @odata.etag
  get_key_value  ${output}  @odata.type
  get_key_value  ${output}  @odata.id
  get_key_value  ${output}  AssetTag
  get_key_value  ${output}  BlockSizeBytes
  get_key_value  ${output}  CapableSpeedGbs
  get_key_value  ${output}  CapacityBytes
  get_key_value  ${output}  EncryptionAbility
  get_key_value  ${output}  EncryptionStatus
  get_key_value  ${output}  FailurePredicted 
  get_key_value  ${output}  Id 
  get_key_value  ${output}  IndicatorLED 
  get_key_value  ${output}  Links 
  get_key_value  ${output}  Chassis
  get_key_value  ${output}  Endpoints@odata.count 
  get_key_value  ${output}  Volumes@odata.count
  get_key_value  ${output}  Manufacturer
  get_key_value  ${output}  MediaType
  get_key_value  ${output}  Model
  get_key_value  ${output}  Name
  get_key_value  ${output}  NegotiatedSpeedGbs
  get_key_value  ${output}  Protocol
  get_key_value  ${output}  Revision
  get_key_value  ${output}  RotationSpeedRPM 
  get_key_value  ${output}  SerialNumber
  get_key_value  ${output}  Status 
  get_key_value  ${output}  Health
  get_key_value  ${output}  State


Verify drive instance info SATA
  [Arguments]    ${resource_storage}
  ${output} =    run_curl_get  ${resource_storage}
  get_key_value  ${output}  @odata.context
  get_key_value  ${output}  @odata.etag
  get_key_value  ${output}  @odata.type
  get_key_value  ${output}  @odata.id
  get_key_value  ${output}  AssetTag
  get_key_value  ${output}  BlockSizeBytes
  get_key_value  ${output}  CapableSpeedGbs
  get_key_value  ${output}  CapacityBytes
  get_key_value  ${output}  FailurePredicted
  get_key_value  ${output}  Id
  get_key_value  ${output}  IndicatorLED
  get_key_value  ${output}  Links
  get_key_value  ${output}  Chassis
  get_key_value  ${output}  Endpoints@odata.count
  get_key_value  ${output}  Volumes@odata.count
  get_key_value  ${output}  Manufacturer
  get_key_value  ${output}  MediaType
  get_key_value  ${output}  Model
  get_key_value  ${output}  Name
  get_key_value  ${output}  NegotiatedSpeedGbs
  get_key_value  ${output}  Protocol
  get_key_value  ${output}  SerialNumber
  get_key_value  ${output}  Status
  get_key_value  ${output}  Health
  get_key_value  ${output}  State
  get_key_value  ${output}  Volumes
  get_key_value  ${output}  StatusIndicator

Verify drive instance info USB
  [Arguments]    ${resource_storage}
  ${output} =    run_curl_get  ${resource_storage}
  get_key_value  ${output}  @odata.context
  get_key_value  ${output}  @odata.etag
  get_key_value  ${output}  @odata.type
  get_key_value  ${output}  @odata.id
  get_key_value  ${output}  AssetTag
  get_key_value  ${output}  BlockSizeBytes
  get_key_value  ${output}  CapacityBytes
  get_key_value  ${output}  FailurePredicted
  get_key_value  ${output}  Id
  get_key_value  ${output}  IndicatorLED
  get_key_value  ${output}  Links
  get_key_value  ${output}  Chassis
  get_key_value  ${output}  Endpoints@odata.count
  get_key_value  ${output}  Volumes@odata.count
  get_key_value  ${output}  Manufacturer
  get_key_value  ${output}  MediaType
  get_key_value  ${output}  Model
  get_key_value  ${output}  Name
  get_key_value  ${output}  Protocol
  get_key_value  ${output}  SerialNumber
  get_key_value  ${output}  Status
  get_key_value  ${output}  Health
  get_key_value  ${output}  State
  get_key_value  ${output}  Revision
  get_key_value  ${output}  EncryptionAbility
  get_key_value  ${output}  EncryptionStatus

Verify network port info
  ${output_1} =    run_curl_get  ${resource_networkportinfo}
  ${members} =  get_key_value  ${output_1}  Members
  FOR    ${INDEX}    IN  @{members}
       ${output} =   run_curl_get  ${INDEX}[@odata.id]/NetworkPorts
       get_key_value  ${output}  @odata.context
       get_key_value  ${output}  @odata.etag
       get_key_value  ${output}  @odata.type
       get_key_value  ${output}  @odata.id
       get_key_value  ${output}  Description
       get_key_value  ${output}  Members
       get_key_value  ${output}  Members@odata.count
       get_key_value  ${output}  Name
  END

Verify GET on SessionService
  ${output_1} =    run_curl_get  ${resource_10}
  get_key_value  ${output_1}  @odata.context
  get_key_value  ${output_1}  @odata.etag
  get_key_value  ${output_1}  @odata.id
  get_key_value  ${output_1}  @odata.type
  get_key_value  ${output_1}  Description
  ${act_value} =  get_key_value  ${output_1}  Name
  check_values_are_equal  ${act_value}  Session Service
  get_key_value  ${output_1}  Sessions
  get_key_value  ${output_1}  Status
  get_key_value  ${output_1}  ServiceEnabled

Verify GET on Registries Members JSON
  ${output_1} =    run_curl_get  ${resource_11}
  ${members} =  get_key_value  ${output_1}  Members
  FOR    ${INDEX}    IN  @{members}
    ${output} =    run_curl_get  ${INDEX}[@odata.id].json
  END

Verify GET on Registries
  ${output_1} =    run_curl_get  ${resource_11}
  get_key_value  ${output_1}  @odata.context
  get_key_value  ${output_1}  @odata.etag
  get_key_value  ${output_1}  @odata.id
  get_key_value  ${output_1}  @odata.type
  get_key_value  ${output_1}  Description
  get_key_value  ${output_1}  Members
  ${act_value} =  get_key_value  ${output_1}  Name
  check_values_are_equal  ${act_value}  Registry Repository
  get_key_value  ${output_1}  Members@odata.count

Verify GET on Registries Members File
  ${output_1} =    run_curl_get  ${resource_11}
  ${members} =  get_key_value  ${output_1}  Members
  FOR    ${INDEX}    IN  @{members}
    ${output} =    run_curl_get  ${INDEX}[@odata.id]
    get_key_value  ${output}  @odata.context
    get_key_value  ${output}  @odata.etag
    get_key_value  ${output}  @odata.type
    get_key_value  ${output}  Description
    get_key_value  ${output}  Id
    get_key_value  ${output}  Languages
    get_key_value  ${output}  Location
    get_key_value  ${output}  Name
    get_key_value  ${output}  Registry
  END

Verify chassis network info show up correctly
  ${ip}  get_ip_address_from_ipmitool  DUT
  ${curl_output1} =  run_curl_BMCIP_get  ${resource_networkadapters}  ${ip}
  Verify the curl output and ensure no error    ${curl_output1}
  Verify event collections info show up correctly    ${curl_output1}
  ${curl_output2} =  run_curl_BMCIP_get  ${resource_networkadapters_vlans}  ${ip}
  Verify the curl output and ensure no error    ${curl_output2}
  Verify event collections info show up correctly    ${curl_output2}

Verify system network vlan info show up correctly
  ${ip}  get_ip_address_from_ipmitool  DUT
  ${curl_output1} =  run_curl_BMCIP_get  ${resource_VLAN_Network_Interface_1}  ${ip}
  Verify the curl output and ensure no error    ${curl_output1}
  Verify event collections info show up correctly    ${curl_output1}
  ${curl_output2} =  run_curl_BMCIP_get  ${resource_VLAN_Network_Interface_ID}  ${ip}
  Verify the curl output and ensure no error    ${curl_output2}
  Verify network VLANs ID info show up correctly    ${curl_output2}

Verify network VLANs ID info show up correctly
  [Arguments]    ${output}
  get_key_value  ${output}  @Redfish.Settings
  get_key_value  ${output}  @odata.context
  get_key_value  ${output}  @odata.etag
  get_key_value  ${output}  @odata.id
  get_key_value  ${output}  @odata.type
  get_key_value  ${output}  Description
  get_key_value  ${output}  Id
  get_key_value  ${output}  Name

Verify system network vlan can be deleted successfully
  ${ip}  get_ip_address_from_ipmitool  DUT
  ${curl_output1} =  run_curl_BMCIP_get  ${resource_VLAN_Network_Interface_1}  ${ip}
  Verify the curl output and ensure no error    ${curl_output1}
  Verify event collections info show up correctly    ${curl_output1}
  ${curl_output2} =  run_curl_BMCIP_get  ${resource_VLANNetwork_InterfaceCollection_1}  ${ip}
  Verify the curl output and ensure no error    ${curl_output2}
  Verify event collections info show up correctly    ${curl_output2}
  get_key_value  ${curl_output2}  @Message.ExtendedInfo
  run_curl_delete_BCMIP  ${resource_VLAN_Network_Interface_ID}  ${ip}
  ${curl_output3} =  run_curl_BMCIP_get  ${resource_VLANNetwork_InterfaceCollection_1}  ${ip}
  Verify the curl output and ensure no error    ${curl_output3}
  Verify event collections info show up correctly    ${curl_output3}
  get_key_value  ${curl_output3}  @Message.ExtendedInfo
  ${output_1} =    run_curl_post_BCMIP  ${resource_VLANNetwork_InterfaceCollection_1}  ${data_NewAccount_VLANID}  ${ip}  output_required=False
  ${curl_output3} =  run_curl_BMCIP_get  ${resource_VLANNetwork_InterfaceCollection_1}  ${ip}
  Verify the curl output and ensure no error    ${curl_output3}
  ${Members} =  get_key_value  ${curl_output3}  Members
  ${first_id} =    set variable  ${members}[0]
  ${first_id_value} =    set variable  ${first_id}[@odata.id]
  common_check_patern_2      ${first_id_value}      ${data_Members_VLANID_100}      check new network vlan can be created successfully

Verify VLAN Network Interface_4 info show up correctly
  ${ip}  get_ip_address_from_ipmitool  DUT
  ${curl_output1} =  run_curl_BMCIP_get  ${resource_networkadapters}  ${ip}
  Verify the curl output and ensure no error    ${curl_output1}
  Verify event collections info show up correctly    ${curl_output1}
  ${curl_output2} =  run_curl_BMCIP_get  ${resource_networkadapters_vlans}  ${ip}
  Verify the curl output and ensure no error    ${curl_output2}
  Verify event collections info show up correctly    ${curl_output2}
  get_key_value  ${curl_output2}  @Message.ExtendedInfo
  ${output_1} =    run_curl_post_BCMIP  ${resource_networkadapters_vlans}  ${data_NewAccount_VLANID}  ${ip}  output_required=False
  ${curl_output3} =  run_curl_BMCIP_get  ${resource_networkadapters_vlans}/${resource_VLANsNetworkingID}  ${ip}
  Log  ${curl_output3}
  Verify the curl output and ensure no error    ${curl_output3}
  Verify network VLANs ID info show up correctly    ${curl_output3}
  run_curl_delete_BCMIP  ${resource_networkadapters_vlans}/${resource_VLANsNetworkingID}  ${ip}

verify manager_logentry_instance showup
  ${output_1} =    run_curl_get  ${resource_auditlog_entries}
  ${members} =  get_key_value  ${output_1}  Members
  FOR    ${INDEX}    IN  @{members}
       ${output} =   run_curl_get  ${INDEX}[@odata.id]
       get_key_value  ${output}  @odata.context
       get_key_value  ${output}  @odata.etag
       get_key_value  ${output}  @odata.type
       get_key_value  ${output}  @odata.id
       get_key_value  ${output}  Created
       get_key_value  ${output}  Description
       get_key_value  ${output}  EntryType
       get_key_value  ${output}  EventTimestamp 
       get_key_value  ${output}  Id
       get_key_value  ${output}  Links
       get_key_value  ${output}  OriginOfCondition
       get_key_value  ${output}  Message
       get_key_value  ${output}  MessageId
       get_key_value  ${output}  MessageArgs
       get_key_value  ${output}  Name 
       get_key_value  ${output}  Severity
  END

Verify chassis property
  ${output} =    run_curl_get  ${resource_chassis}
  get_key_value  ${output}  @odata.context
  get_key_value  ${output}  @odata.etag
  get_key_value  ${output}  @odata.type
  get_key_value  ${output}  @odata.id
  get_key_value  ${output}  Description
  get_key_value  ${output}  Members
  get_key_value  ${output}  Name
  get_key_value  ${output}  Members@odata.count

Verify GET on NetworkInterface Collection
  ${output_1} =    run_curl_get  ${resource_12}
  get_key_value  ${output_1}  @odata.context
  get_key_value  ${output_1}  @odata.etag
  get_key_value  ${output_1}  @odata.id
  get_key_value  ${output_1}  @odata.type
  get_key_value  ${output_1}  Description
  get_key_value  ${output_1}  Members
  get_key_value  ${output_1}  Members@odata.count
  ${act_value} =  get_key_value  ${output_1}  Name
  check_values_are_equal  ${act_value}  NetworkInterface Collection

Verify GET on NetworkInterface Ethernet Members
  ${output_1} =    run_curl_get  ${resource_13}
  ${members} =  get_key_value  ${output_1}  Members
  FOR    ${INDEX}    IN  @{members}
    ${output} =    run_curl_get  ${INDEX}[@odata.id]
    get_key_value  ${output}  @odata.context
    get_key_value  ${output}  @odata.etag
    get_key_value  ${output}  @odata.type
    get_key_value  ${output}  DHCPv4
    get_key_value  ${output}  IPv4Addresses
    get_key_value  ${output}  IPv6Addresses
    get_key_value  ${output}  IPv6DefaultGateway
    get_key_value  ${output}  Id
    get_key_value  ${output}  InterfaceEnabled
    get_key_value  ${output}  LinkStatus
    get_key_value  ${output}  Links
    get_key_value  ${output}  MACAddress
    get_key_value  ${output}  MTUSize
    get_key_value  ${output}  Name
    get_key_value  ${output}  PermanentMACAddress
    get_key_value  ${output}  Status
    get_key_value  ${output}  UefiDevicePath
    get_key_value  ${output}  VLANs
  END

Verify GET on NetworkDeviceFunction Collection
  ${output_1} =    run_curl_get  ${resource_14}
  ${members} =  get_key_value  ${output_1}  Members
  FOR    ${INDEX}    IN  @{members}
    ${output} =    run_curl_get  ${INDEX}[@odata.id]/NetworkDeviceFunctions
    get_key_value  ${output}  @odata.context
    get_key_value  ${output}  @odata.etag
    get_key_value  ${output}  @odata.id
    get_key_value  ${output}  @odata.type
    get_key_value  ${output}  Description
    get_key_value  ${output}  Members
    get_key_value  ${output}  Members@odata.count
    ${act_value} =      get_key_value  ${output}  Name
    check_values_are_equal  ${act_value}  NetworkDeviceFunction Collection
  END

Verify GET on NetworkDeviceFunction Members
  ${output_1} =    run_curl_get  ${resource_14}
  ${members_1} =  get_key_value  ${output_1}  Members
  FOR    ${INDEX_1}    IN  @{members_1}
    ${output_2} =    run_curl_get  ${INDEX_1}[@odata.id]/NetworkDeviceFunctions
    ${members_2} =  get_key_value  ${output_2}  Members
    Inner loop for NetworkDeviceFunction Members  ${members_2}
  END

Inner loop for NetworkDeviceFunction Members
  [Arguments]    ${members}
  FOR    ${INDEX}    IN  @{members}
    ${output} =    run_curl_get  ${INDEX}[@odata.id]
    get_key_value  ${output}  @Redfish.Settings
    get_key_value  ${output}  @odata.type
    get_key_value  ${output}  SettingsObject
    get_key_value  ${output}  @odata.context
    get_key_value  ${output}  @odata.etag
    get_key_value  ${output}  @odata.id
    get_key_value  ${output}  @odata.type
    get_key_value  ${output}  Name
    get_key_value  ${output}  Id
  END

Verify GET on NetworkAdapter Collection
  ${output_1} =    run_curl_get  ${resource_14}
  get_key_value  ${output_1}  @odata.context
  get_key_value  ${output_1}  @odata.etag
  get_key_value  ${output_1}  @odata.id
  get_key_value  ${output_1}  @odata.type
  get_key_value  ${output_1}  Description
  get_key_value  ${output_1}  Members
  get_key_value  ${output_1}  Members@odata.count
  ${act_value} =  get_key_value  ${output_1}  Name
  check_values_are_equal  ${act_value}  NetworkAdapter Collection

Verify GET on NetworkAdapter Members
  ${output_1} =    run_curl_get  ${resource_14}
  ${members_1} =  get_key_value  ${output_1}  Members
  FOR    ${INDEX}    IN  @{members_1}
    ${output} =    run_curl_get  ${INDEX}[@odata.id]
    get_key_value  ${output}  @odata.context
    get_key_value  ${output}  @odata.etag
    get_key_value  ${output}  @odata.id
    get_key_value  ${output}  @odata.type
    get_key_value  ${output}  Controllers
    get_key_value  ${output}  NetworkDeviceFunctions@odata.count
    get_key_value  ${output}  NetworkPorts@odata.count
    get_key_value  ${output}  NetworkPorts
    get_key_value  ${output}  Id
    get_key_value  ${output}  Status
    get_key_value  ${output}  Name
    get_key_value  ${output}  NetworkDeviceFunctions
  END

Verify GET on Storage Collection
  ${output_1} =    run_curl_get  ${resource_15}
  get_key_value  ${output_1}  @odata.context
  get_key_value  ${output_1}  @odata.etag
  get_key_value  ${output_1}  @odata.id
  get_key_value  ${output_1}  @odata.type
  get_key_value  ${output_1}  Description
  get_key_value  ${output_1}  Members
  get_key_value  ${output_1}  Members@odata.count
  ${act_value} =  get_key_value  ${output_1}  Name
  check_values_are_equal  ${act_value}  Storage Collection

Verify GET on Storage Members
  ${output_1} =    run_curl_get  ${resource_15}
  ${members_1} =  get_key_value  ${output_1}  Members
  FOR    ${INDEX}    IN  @{members_1}
    ${output} =    run_curl_get  ${INDEX}[@odata.id]
    get_key_value  ${output}  @odata.context
    get_key_value  ${output}  @odata.etag
    get_key_value  ${output}  @odata.id
    get_key_value  ${output}  @odata.type
    get_key_value  ${output}  Id
    get_key_value  ${output}  Status
    get_key_value  ${output}  Name
    get_key_value  ${output}  Drives
    get_key_value  ${output}  Drives@odata.count
    get_key_value  ${output}  Links
    get_key_value  ${output}  Redundancy@odata.count
    get_key_value  ${output}  StorageControllers
    get_key_value  ${output}  StorageControllers@odata.count
    get_key_value  ${output}  Volumes
  END

Verify GET on Volume Collection
  ${output} =    run_curl_get  ${resource_15}
  ${members_1} =  get_key_value  ${output}  Members
  FOR    ${INDEX}    IN  @{members_1}
    ${output_1} =    run_curl_get  ${INDEX}[@odata.id]/Volumes
    get_key_value  ${output_1}  @odata.context
    get_key_value  ${output_1}  @odata.etag
    get_key_value  ${output_1}  @odata.id
    get_key_value  ${output_1}  @odata.type
    get_key_value  ${output_1}  Description
    get_key_value  ${output_1}  Members
    get_key_value  ${output_1}  Members@odata.count
    ${act_value} =  get_key_value  ${output_1}  Name
    check_values_are_equal  ${act_value}  Volume Collection
  END

Verify GET on Volume Members
  ${output} =    run_curl_get  ${resource_15}
  ${members_1} =  get_key_value  ${output}  Members
  FOR    ${INDEX}    IN  @{members_1}
    ${output_1} =    run_curl_get  ${INDEX}[@odata.id]/Volumes
    ${members_2} =  get_key_value  ${output_1}  Members
    Inner loop for Volume Members  ${members_2}
  END

Inner loop for Volume Members
  [Arguments]    ${members}
  FOR    ${INDEX}    IN  @{members}
    ${output} =    run_curl_get  ${INDEX}[@odata.id]
    get_key_value  ${output}  @odata.type
    get_key_value  ${output}  @odata.context
    get_key_value  ${output}  @odata.etag
    get_key_value  ${output}  @odata.id
    get_key_value  ${output}  @odata.type
    get_key_value  ${output}  Name
    get_key_value  ${output}  Id
    get_key_value  ${output}  BlockSizeBytes
    get_key_value  ${output}  CapacityBytes
    get_key_value  ${output}  Encrypted
    get_key_value  ${output}  Links
    get_key_value  ${output}  Drives@odata.count
    get_key_value  ${output}  Status
  END

Verify GET on PCIeDevice Collection
  ${output_1} =    run_curl_get  ${resource_16}
  get_key_value  ${output_1}  @odata.context
  get_key_value  ${output_1}  @odata.etag
  get_key_value  ${output_1}  @odata.id
  get_key_value  ${output_1}  @odata.type
  get_key_value  ${output_1}  Description
  get_key_value  ${output_1}  Members
  get_key_value  ${output_1}  Members@odata.count
  get_key_value  ${output_1}  Members@odata.nextLink
  ${act_value} =  get_key_value  ${output_1}  Name
  check_values_are_equal  ${act_value}  PCIeDevice Collection

Verify GET on PCIeDevice Members
  ${output_1} =    run_curl_get  ${resource_16}
  ${members_1} =  get_key_value  ${output_1}  Members
  FOR    ${INDEX}    IN  @{members_1}
    ${output} =    run_curl_get  ${INDEX}[@odata.id]
    get_key_value  ${output}  @odata.context
    get_key_value  ${output}  @odata.etag
    get_key_value  ${output}  @odata.id
    get_key_value  ${output}  @odata.type
    get_key_value  ${output}  DeviceType
    get_key_value  ${output}  PCIeFunctions
    get_key_value  ${output}  Id
    get_key_value  ${output}  Status
    get_key_value  ${output}  Name
  END

Verify GET on PCIeFunction Members
  ${output_1} =    run_curl_get  ${resource_16}
  ${members_1} =  get_key_value  ${output_1}  Members
  FOR    ${INDEX}    IN  @{members_1}
    ${output_2} =    run_curl_get  ${INDEX}[@odata.id]
    ${members_2} =  get_key_value  ${output_2}  PCIeFunctions
    ${output_3} =    run_curl_get  ${members_2}[@odata.id]
    ${members_3} =  get_key_value  ${output_3}  Members
    Inner loop for PCIeFunction Members  ${members_3}
  END

Inner loop for PCIeFunction Members
  [Arguments]    ${members}
  FOR    ${INDEX}    IN  @{members}
    ${output} =    run_curl_get  ${INDEX}[@odata.id]
    get_key_value  ${output}  @odata.type
    get_key_value  ${output}  @odata.context
    get_key_value  ${output}  @odata.etag
    get_key_value  ${output}  @odata.id
    get_key_value  ${output}  @odata.type
    get_key_value  ${output}  Id
    get_key_value  ${output}  Links
    get_key_value  ${output}  Name
    get_key_value  ${output}  Status
  END

Verify GET on PCIeFunction Collection
  ${output_1} =    run_curl_get  ${resource_16}
  ${members_1} =  get_key_value  ${output_1}  Members
  FOR    ${INDEX}    IN  @{members_1}
    ${output_2} =    run_curl_get  ${INDEX}[@odata.id]
    ${members_2} =  get_key_value  ${output_2}  PCIeFunctions
    ${output_3} =    run_curl_get  ${members_2}[@odata.id]
    get_key_value  ${output_3}  @odata.context
    get_key_value  ${output_3}  @odata.etag
    get_key_value  ${output_3}  @odata.id
    get_key_value  ${output_3}  @odata.type
    get_key_value  ${output_3}  Description
    get_key_value  ${output_3}  Members
    get_key_value  ${output_3}  Members@odata.count
    ${act_value} =      get_key_value  ${output_3}  Name
    check_values_are_equal  ${act_value}  PCIeFunction Collection
  END

Verify GET on UpdateService
  ${output_1} =    run_curl_get  ${resource_17}
  get_key_value  ${output_1}  @odata.context
  get_key_value  ${output_1}  @odata.etag
  get_key_value  ${output_1}  @odata.id
  get_key_value  ${output_1}  @odata.type
  get_key_value  ${output_1}  Actions
  get_key_value  ${output_1}  Description
  get_key_value  ${output_1}  FirmwareInventory
  get_key_value  ${output_1}  Id
  get_key_value  ${output_1}  MaxImageSizeBytes
  get_key_value  ${output_1}  MultipartHttpPushUri
  get_key_value  ${output_1}  Oem
  get_key_value  ${output_1}  ServiceEnabled
  get_key_value  ${output_1}  Status
  ${act_value} =  get_key_value  ${output_1}  Name
  check_values_are_equal  ${act_value}  Update Service

Verify NetworkPort
  OS Connect Device
  ${output} =  run_curl_get    ${NetworkPort}
  get_key_value  ${output}  @odata.context
  get_key_value  ${output}  @odata.etag
  get_key_value  ${output}  @odata.id
  get_key_value  ${output}  @odata.type
  get_key_value  ${output}  ActiveLinkTechnology@Redfish.AllowableValues
  get_key_value  ${output}  FlowControlConfiguration@Redfish.AllowableValues
  get_key_value  ${output}  Id
  get_key_value  ${output}  Name
  get_key_value  ${output}  PhysicalPortNumber
  OS Disconnect Device

Verify get command TelemetryService_3
  OS Connect Device
  ${output} =  run_curl_get   ${TelemetryService_3}
  get_key_value  ${output}  @odata.context
  get_key_value  ${output}  @odata.etag
  get_key_value  ${output}  @odata.id
  get_key_value  ${output}  @odata.type
  get_key_value  ${output}  Actions
  get_key_value  ${output}  \#TelemetryService.SubmitTestMetricReport
  get_key_value  ${output}  @Redfish.ActionInfo
  get_key_value  ${output}  target
  get_key_value  ${output}  Description
  get_key_value  ${output}  Id
  get_key_value  ${output}  LogService
  get_key_value  ${output}  @odata.id
  get_key_value  ${output}  MaxReports
  get_key_value  ${output}  MetricDefinitions
  get_key_value  ${output}  @odata.id
  get_key_value  ${output}  MetricReportDefinitions
  get_key_value  ${output}  @odata.id
  get_key_value  ${output}  MetricReports
  get_key_value  ${output}  @odata.id
  get_key_value  ${output}  MinCollectionInterval
  get_key_value  ${output}  Name
  get_key_value  ${output}  ServiceEnabled
  get_key_value  ${output}  Status
  get_key_value  ${output}  Health
  get_key_value  ${output}  State
  get_key_value  ${output}  SupportedCollectionFunctions
  get_key_value  ${output}  SupportedCollectionFunctions@Redfish.AllowableValues
  get_key_value  ${output}  Triggers
  get_key_value  ${output}  @odata.id
  OS Disconnect Device


Verify patch command on TelemetryService_3
  run_curl_patch    ${TelemetryService_3}   ${SupportedCollectionFunctions}

Verify set value on TelemetryService_3
  ${output} =  run_curl_get   ${TelemetryService_3}
  ${act_value} =  get_key_value  ${output}  SupportedCollectionFunctions
  Log  ${act_value}
  Log  ${Check_value}
  check_values_are_equal  ${act_value}  ${Check_value}

Set SecureBootEnable to False
  [Arguments]   ${resource}
  run_curl_patch  ${resource}  ${data_SecureBootEnable_false}

Check SecureBootEnable value as False
  [Arguments]   ${resource}
  ${output} =  run_curl_get  ${resource}
  ${act_value} =  get_key_value  ${output}  SecureBootEnable
  Log  ${act_value}
  check_values_are_equal  ${act_value}  ${false_value}

Set SecureBootEnable to True
  [Arguments]   ${resource}
  run_curl_patch  ${resource}  ${data_SecureBootEnable_true}

Check SecureBootEnable value as True
  [Arguments]   ${resource}
  ${output} =  run_curl_get  ${resource}
  ${act_value} =  get_key_value  ${output}  SecureBootEnable
  Log  ${act_value}
  check_values_are_equal  ${act_value}  ${true_value}

update BMC with BIOS image
  [Arguments]    ${module}  ${version}  ${key}
  ${image_to_upgrade_downgrade} =  get_image_version_for_upgrade_downgrade  ${module}  ${version}  ${key}
  Log  ${image_to_upgrade_downgrade}
  OS Connect Device
  change_directory   DUT  /root/athena_gen2_fw/BIOS
  upgrade bmc with bios image   DUT  ./CFUFLASH -cd -mse 1   ${image_to_upgrade_downgrade}  
  OS Disconnect Device
  ConnectESMB
  change_directory   DUT  /root/athena_gen2_fw/BIOS
  upgrade bmc with bios image   DUT  ./CFUFLASH -cd -mse 1   ${image_to_upgrade_downgrade}
  OS Disconnect Device

Update BIOS with BMC image
  OS Connect Device
  upgrade BIOS with BMC image  DUT  Athena_FW_BMC_A  upgrade
  OS Disconnect Device
  ConnectESMB
  upgrade BIOS with BMC image  DUT  Athena_FW_BMC_B  upgrade
  OS Disconnect Device
  Remove Athena BMC FW image
  OS Disconnect Device

Update BMC with Local OS and CFUFLASH ESM A
   [Arguments]    ${module}  ${version}  ${key}  ${action}
   OS Connect Device
   mkdir_data_path    DUT  "/root/athena_gen2_fw/BMC"
   change_directory   DUT  "/root/athena_gen2_fw/BMC"
   downloadAthenaSesFwImage    DUT   ${module}
   OS Disconnect Device
   ${image_to_upgrade_downgrade} =  get_image_version_for_upgrade_downgrade  ${module}  ${version}  ${key}
   Log  ${image_to_upgrade_downgrade}
   OS Connect Device
   ${ip}  get_ip_address_from_ipmitool  DUT
   Verify event log SEL clear  DUT  ${ip}
   ${BMC_MAC_address1a}  get_info_from_lan_print  DUT  MAC Address  True  ${ip}
   change_directory   DUT  /root/athena_gen2_fw/BMC
   Upgrade BMC with Local OS  DUT  ./CFUFLASH -cd ${image_to_upgrade_downgrade} -mse 1 -fb
   OS Disconnect Device
   ses_lib.powercycle_pdu1  DUT
   Sleep  360
   OS Connect Device
   change_directory   DUT  /root/athena_gen2_fw/BMC
   Upgrade BMC with Local OS  DUT  ./CFUFLASH -cd ${image_to_upgrade_downgrade} -mse 2 -fb
   OS Disconnect Device
   ses_lib.powercycle_pdu1  DUT
   Sleep  360
   OS Connect Device
   getBMCFWimageversion  DUT  ${module}  ${get_BMC_version}  ${get_BMC_version_next}  ${action}
   verify_BMC_version_in_BIOS     DUT   ${module}   ${action}   bios_password=${athena_bios_password}
   ${BMC_MAC_address2a}  get_info_from_lan_print  DUT  MAC Address  True  ${ip}
   common_check_patern_2    ${BMC_MAC_address1a}     ${BMC_MAC_address2a}      check MAC address not swipe out on ESMA   expect=True
   Verify the SEL and ensure no error
   Verify abnormal event log  DUT  ${ip}
   verifythesensorreadingandcheckstatus  DUT  ${ip}
   OS Disconnect Device

Update BMC with Local OS and CFUFLASH ESM B
   [Arguments]    ${module}  ${version}  ${key}  ${action}
   ConnectESMB
   mkdir_data_path    DUT  "/root/athena_gen2_fw/BMC"
   change_directory   DUT  "/root/athena_gen2_fw/BMC"
   downloadAthenaSesFwImage    DUT   ${module}
   OS Disconnect Device
   ${image_to_upgrade_downgrade} =  get_image_version_for_upgrade_downgrade  ${module}  ${version}  ${key}
   Log  ${image_to_upgrade_downgrade}
   ConnectESMB
   ${ip}  get_ip_address_from_ipmitool  DUT
   Verify event log SEL clear  DUT  ${ip}
   ${BMC_MAC_address1b}  get_info_from_lan_print  DUT  MAC Address  True  ${ip}
   change_directory   DUT  /root/athena_gen2_fw/BMC
   Upgrade BMC with Local OS  DUT  ./CFUFLASH -cd ${image_to_upgrade_downgrade} -mse 1 -fb
   OS Disconnect Device
   ses_lib.powercycle_pdu1  DUT
   Sleep  360
   ConnectESMB
   change_directory   DUT  /root/athena_gen2_fw/BMC
   Upgrade BMC with Local OS  DUT  ./CFUFLASH -cd ${image_to_upgrade_downgrade} -mse 2 -fb
   OS Disconnect Device
   ses_lib.powercycle_pdu1  DUT
   Sleep  360
   ConnectESMB
   getBMCFWimageversion  DUT  ${module}   ${get_BMC_version}  ${get_BMC_version_next}  ${action}
   verify_BMC_version_in_BIOS     DUT   ${module}   ${action}   bios_password=${athena_bios_password}
   ${BMC_MAC_address2b}  get_info_from_lan_print  DUT  MAC Address  True  ${ip}
   common_check_patern_2    ${BMC_MAC_address1b}     ${BMC_MAC_address2b}      check MAC address not swipe out on ESMB   expect=True
   Verify the SEL and ensure no error
   Verify abnormal event log  DUT  ${ip}
   verifythesensorreadingandcheckstatus  DUT  ${ip}
   change_directory   DUT  "/root/athena_gen2_fw/BMC"
   RemoveAthenaBIOSFwImage    DUT   Athena_FW_BMC_B
   OS Disconnect Device

verifysystemafterFWupdate
  [Arguments]    ${module}  ${action}  ${ip}  ${BMC_MAC_address1a}
  getBMCFWimageversion  DUT  ${module}  ${get_BMC_version}  ${get_BMC_version_next}  ${action}
  ${BMC_MAC_address2a}  get_info_from_lan_print  DUT  MAC Address  True  ${ip}
  common_check_patern_2    ${BMC_MAC_address1a}     ${BMC_MAC_address2a}      check MAC address not swipe out on ESMA   expect=True
  Verify the SEL and ensure no error
  Verify abnormal event log  DUT  ${ip}
  verifythesensorreadingandcheckstatus  DUT  ${ip}
  verify_BMC_version_in_BIOS     DUT   ${module}   ${action}   bios_password=${athena_bios_password}

Remote OS with CFUFLASH Update
  [Arguments]  ${updateinfo}
  OS Connect Device
  ${ip}  get_ip_address_from_ipmitool  DUT
  Verify event log SEL clear  DUT  ${ip}
  ${mc_info_before_update} =  get_bmc_version_ipmitool   DUT  ${ip}
  ${BMC_MAC_address1a}  get_info_from_lan_print  DUT  MAC Address  True  ${ip}
  OS Disconnect Device
  updateBMCfirmwarefromremoteclient  DUT  ${ip}  Athena_FW_BMC_A  ${updateinfo}  1
  Sleep  500
  OS Connect Device
  ${ip}  get_ip_address_from_ipmitool  DUT
  OS Disconnect Device
  updateBMCfirmwarefromremoteclient  DUT  ${ip}  Athena_FW_BMC_A  ${updateinfo}  2
  Sleep  500
  OS Connect Device
  verifysystemafterFWupdate  Athena_FW_BMC_A  ${updateinfo}  ${ip}  ${BMC_MAC_address1a}
  OS Disconnect Device
  ConnectESMB
  ${ip}  get_ip_address_from_ipmitool  DUT
  Verify event log SEL clear  DUT  ${ip}
  ${mc_info_before_update} =  get_bmc_version_ipmitool   DUT  ${ip}
  ${BMC_MAC_address1a}  get_info_from_lan_print  DUT  MAC Address  True  ${ip}
  OS Disconnect Device
  updateBMCfirmwarefromremoteclient  DUT  ${ip}  Athena_FW_BMC_B  ${updateinfo}  1
  Sleep  500
  ConnectESMB
  ${ip}  get_ip_address_from_ipmitool  DUT
  OS Disconnect Device
  updateBMCfirmwarefromremoteclient  DUT  ${ip}  Athena_FW_BMC_B  ${updateinfo}  2
  ses_lib.powercycle_pdu1  DUT
  Sleep  360
  ConnectESMB
  ${ip}  get_ip_address_from_ipmitool  DUT
  verifysystemafterFWupdate  Athena_FW_BMC_B  ${updateinfo}  ${ip}  ${BMC_MAC_address1a}
  OS Disconnect Device

BIOS Firmware Update with pc
  [Arguments]    ${module}  ${version}  ${key}  ${ME_version_BIOS}   ${ME_ver_OS}
  ${image_to_upgrade_downgrade} =  get_image_version_for_upgrade_downgrade   ${module}  ${version}   ${key}
  ${rev_to_check} =  GetRevFromImage  ${image_to_upgrade_downgrade}
  OS Connect Device
  change_directory   DUT  /root/athena_gen2_fw/BIOS
  ${ip}  get_ip_address_from_ipmitool  DUT
  Verify event log SEL clear  DUT  ${ip}
  ${BMC_MAC_address1a}  get_info_from_lan_print  DUT  MAC Address  True  ${ip}
  update_bios_version   DUT    ./CFUFLASH -cd -pc -d 2      ${image_to_upgrade_downgrade}
  OS Disconnect Device
  ConnectESMB
  change_directory   DUT  /root/athena_gen2_fw/BIOS
  ${ip}  get_ip_address_from_ipmitool  DUT
  Verify event log SEL clear  DUT  ${ip}
  ${BMC_MAC_address1b}  get_info_from_lan_print  DUT  MAC Address  True  ${ip}
  update_bios_version   DUT    ./CFUFLASH -cd -pc -d 2      ${image_to_upgrade_downgrade}
  OS Disconnect Device
  whitebox_lib.Powercycle Pdu1  DUT
  Sleep  300
  whitebox_lib.Powercycle Pdu1  DUT
  Sleep  360
  OS Connect Device
  Sleep  30
  ${ip}  get_ip_address_from_ipmitool  DUT
  ${version_output} =  execute_Linux_command    dmidecode -s bios-version
  common_check_patern_2     ${version_output}     ${rev_to_check}    BIOS_Version_check  expect=True
  ${ME_output} =     execute_Linux_command     ipmitool -b 0x6 -t 0x2c raw 6 1
  verify_me_version_in_os      ${ME_output}    ${ME_ver_OS}
  verify_bios_memory  DUT  ${mem_size}  ${mem_speed}  ${cfg_speed}  ${Manufacturer}
  ${BMC_MAC_address2a}  get_info_from_lan_print  DUT  MAC Address  True  ${ip}
  common_check_patern_2    ${BMC_MAC_address1a}     ${BMC_MAC_address2a}      check MAC address not swipe out on ESMA   expect=True
  verify_bios_ip_address  DUT  cmd=ipmitool lan print 1  expected_result=${ip}
  Verify the SEL and ensure no error
  Check version in BIOS
  Sleep  60
  OS Disconnect Device
  ConnectESMB
  ${ip}  get_ip_address_from_ipmitool  DUT
  ${version_output} =  execute_Linux_command    dmidecode -s bios-version
  common_check_patern_2     ${version_output}     ${rev_to_check}    BIOS_Version_check  expect=True
  ${ME_output} =     execute_Linux_command     ipmitool -b 0x6 -t 0x2c raw 6 1
  verify_me_version_in_os      ${ME_output}    ${ME_ver_OS}
  verify_bios_memory  DUT  ${mem_size}  ${mem_speed}  ${cfg_speed}  ${Manufacturer}
  ${BMC_MAC_address2b}  get_info_from_lan_print  DUT  MAC Address  True  ${ip}
  common_check_patern_2    ${BMC_MAC_address1b}     ${BMC_MAC_address2b}      check MAC address not swipe out on ESMA   expect=True
  verify_bios_ip_address  DUT  cmd=ipmitool lan print 1  expected_result=${ip}
  Verify the SEL and ensure no error
  Check version in BIOS
  Sleep  60
  OS Disconnect Device

BMC Firmware Update with pc and verify
  [Arguments]  ${updateinfo}
  Download Athena BMC FW image
  OS Connect Device
  ${ip}  get_ip_address_from_ipmitool  DUT
  Verify event log SEL clear  DUT  ${ip}
  ${BMC_MAC_address1a}  get_info_from_lan_print  DUT  MAC Address  True  ${ip}
  OS Disconnect Device
  ConnectESMB
  {ip2}  get_ip_address_from_ipmitool  DUT
  Verify event log SEL clear  DUT  ${ip2}
  ${BMC_MAC_address1b}  get_info_from_lan_print  DUT  MAC Address  True  ${ip2}
  OS Disconnect Device
  BMC Firmware Update with pc  ${updateinfo}
  OS Connect Device
  getBMCFWimageversion  DUT  Athena_FW_BMC_A  ${get_BMC_version}  ${get_BMC_version_next}  ${updateinfo}
  checkinstalledBCMFWversion  DUT  Athena_FW_BMC_A  ${ip}  ${updateinfo}
  ${BMC_MAC_address2a}  get_info_from_lan_print  DUT  MAC Address  True  ${ip}
  common_check_patern_2    ${BMC_MAC_address1a}     ${BMC_MAC_address2a}      check MAC address not swipe out on ESMA  expect=True
  Verify the SEL and ensure no error
  verifyeventlogSELclear  DUT  ${ip}
  OS Disconnect Device
  ConnectESMB
  ${ip2}  get_ip_address_from_ipmitool  DUT
  getBMCFWimageversion  DUT  Athena_FW_BMC_B  ${get_BMC_version}  ${get_BMC_version_next}  ${updateinfo}
  checkinstalledBCMFWversion  DUT  Athena_FW_BMC_B  ${ip2}  ${updateinfo}
  ${BMC_MAC_address2b}  get_info_from_lan_print  DUT  MAC Address  True  ${ip2}
  common_check_patern_2    ${BMC_MAC_address1b}     ${BMC_MAC_address2b}      check MAC address not swipe out on ESMA  expect=True
  Verify the SEL and ensure no error
  verifyeventlogSELclear  DUT  ${ip2}
  OS Disconnect Device

BMC Firmware Update with pc
  [Arguments]    ${updateinfo}
  OS Connect Device
  installBMCFWimage  DUT  Athena_FW_BMC_A  ${updateinfo}  "1/2/3"  "pc"
  Sleep  500
  OS Disconnect Device
  ConnectESMB
  installBMCFWimage  DUT  Athena_FW_BMC_B  ${updateinfo}  "1/2/3"  "pc"
  Sleep  400
  OS Disconnect Device
  Remove Athena BMC FW image
  ConnectESMB
  ses_lib.powercycle_pdu1  DUT
  Sleep  500
  OS Connect Device
  ses_lib.powercycle_pdu1  DUT
  Sleep  400
  OS Disconnect Device

Download Athena_G2 CPLD image
  OS Connect Device
  mkdir_data_path    DUT  "/root/athena_gen2_fw/CPLD"
  change_directory   DUT  "/root/athena_gen2_fw/CPLD"
  downloadAthenaSesFwImage    DUT   Athena_G2_FW_CPLD_A
  OS Disconnect Device
  ConnectESMB
  mkdir_data_path    DUT  "/root/athena_gen2_fw/CPLD"
  change_directory   DUT  "/root/athena_gen2_fw/CPLD"
  downloadAthenaSesFwImage    DUT   Athena_G2_FW_CPLD_B
  OS Disconnect Device

Remove Athena_G2 CPLD image
  OS Connect Device
  change_directory   DUT  "/root/athena_gen2_fw/CPLD"
  RemoveAthenaSesFwImage    DUT   Athena_G2_FW_CPLD_A
  OS Disconnect Device
  ConnectESMB
  change_directory   DUT  "/root/athena_gen2_fw/CPLD"
  RemoveAthenaSesFwImage    DUT   Athena_G2_FW_CPLD_B
  OS Disconnect Device

CPLD Firware Update with Local OS
  [Arguments]    ${updateinfo}
  Download Athena_G2 CPLD image
  OS Connect Device
  ${ipa}  get_ip_address_from_ipmitool  DUT
  Verify event log SEL clear  DUT  ${ipa}
  ${CPLD_value1a} =  execute_Linux_command   ipmitool raw 0x3a 0x27
  ${BMC_MAC_address1a}  get_info_from_lan_print  DUT  MAC Address  True  ${ipa}
  OS Disconnect Device
  ConnectESMB
  ${ipb}  get_ip_address_from_ipmitool  DUT
  Verify event log SEL clear  DUT  ${ipb}
  ${CPLD_value1b} =  execute_Linux_command   ipmitool raw 0x3a 0x27
  ${BMC_MAC_address1b}  get_info_from_lan_print  DUT  MAC Address  True  ${ipb}
  OS Disconnect Device
  CPLD Firmware Update LocalOS  ${updateinfo}
  OS Connect Device
  ${CPLD_value2a} =  execute_Linux_command   ipmitool raw 0x3a 0x27
  Check Installed CPLD FW Version  DUT  Athena_G2_FW_CPLD_A  ${ipa}  ${updateinfo}
  ${BMC_MAC_address2a}  get_info_from_lan_print  DUT  MAC Address  True  ${ipa}
  common_check_patern_2    ${BMC_MAC_address1a}     ${BMC_MAC_address2a}      check MAC address not swipe out on ESMA  expect=True
  Verify the SEL and ensure no error
  verifyeventlogSELclear  DUT  ${ipa}
  OS Disconnect Device
  ConnectESMB
  ${ipb}  get_ip_address_from_ipmitool  DUT
  ${CPLD_value2b} =  execute_Linux_command   ipmitool raw 0x3a 0x27
  Check Installed CPLD FW Version  DUT  Athena_G2_FW_CPLD_B  ${ipb}  ${updateinfo}
  ${BMC_MAC_address2b}  get_info_from_lan_print  DUT  MAC Address  True  ${ipb}
  common_check_patern_2    ${BMC_MAC_address1b}     ${BMC_MAC_address2b}      check MAC address not swipe out on ESMB  expect=True
  Verify the SEL and ensure no error
  verifyeventlogSELclear  DUT  ${ipb}
  OS Disconnect Device

CPLD Firmware Update LocalOS
  [Arguments]    ${updateinfo}
  OS Connect Device
  installCPLDFWimage  DUT  Athena_G2_FW_CPLD_A  ${updateinfo}
  Sleep  200
  OS Disconnect Device
  ConnectESMB
  installCPLDFWimage  DUT  Athena_G2_FW_CPLD_B  ${updateinfo}
  Sleep  300
  OS Disconnect Device
  Remove Athena_G2 CPLD image
  ConnectESMB
  ses_lib.powercycle_pdu1  DUT
  Sleep  300
  OS Disconnect Device
  OS Connect Device
  ses_lib.powercycle_pdu1  DUT
  Sleep  400
  OS Disconnect Device

CPLD Firware Update with Remote OS
  [Arguments]    ${updateinfo}
  OS Connect Device
  ${ipa}  get_ip_address_from_ipmitool  DUT
  Verify event log SEL clear  DUT  ${ipa}
  ${CPLD_value1a} =  execute_Linux_command   ipmitool raw 0x3a 0x27
  ${BMC_MAC_address1a}  get_info_from_lan_print  DUT  MAC Address  True  ${ipa}
  OS Disconnect Device
  ConnectESMB
  ${ipb}  get_ip_address_from_ipmitool  DUT
  Verify event log SEL clear  DUT  ${ipb}
  ${CPLD_value1b} =  execute_Linux_command   ipmitool raw 0x3a 0x27
  ${BMC_MAC_address1b}  get_info_from_lan_print  DUT  MAC Address  True  ${ipb}
  OS Disconnect Device
  updateCPLDfirmwarefromremoteclient  DUT  ${ipa}  Athena_G2_FW_CPLD_A  ${updateinfo}
  Sleep  200
  updateCPLDfirmwarefromremoteclient  DUT  ${ipb}  Athena_G2_FW_CPLD_B  ${updateinfo
  ses_lib.powercycle_pdu1  DUT
  Sleep  360
  OS Connect Device
  Check Installed CPLD FW Version  DUT  Athena_G2_FW_CPLD_A  ${ipa}  ${updateinfo}
  ${BMC_MAC_address2a}  get_info_from_lan_print  DUT  MAC Address  True  ${ipa}
  common_check_patern_2    ${BMC_MAC_address1a}     ${BMC_MAC_address2a}      check MAC address not swipe out on ESMA  expect=True
  Verify the SEL and ensure no error
  verifyeventlogSELclear  DUT  ${ipa}
  OS Disconnect Device
  ConnectESMB
  Check Installed CPLD FW Version  DUT  Athena_G2_FW_CPLD_B  ${ipb}  ${updateinfo}
  ${BMC_MAC_address2b}  get_info_from_lan_print  DUT  MAC Address  True  ${ipb}
  common_check_patern_2    ${BMC_MAC_address1b}     ${BMC_MAC_address2b}      check MAC address not swipe out on ESMB  expect=True
  Verify the SEL and ensure no error
  verifyeventlogSELclear  DUT  ${ipb}
  OS Disconnect Device

BMC FWFlash Update with socflash
  [Arguments]    ${updateinfo}
  Download Athena BMC FW image
  OS Connect Device
  ${ipa}  get_ip_address_from_ipmitool  DUT
  Verify event log SEL clear  DUT  ${ipa}
  ${BMC_MAC_address1a}  get_info_from_lan_print  DUT  MAC Address  True  ${ipa}
  ${mc_info_before_update} =  get_bmc_version_ipmitool   DUT  ${ipa}
  BMCFWFlashUpdate  DUT  Athena_FW_BMC_A  ${updateinfo}
  Sleep  60
  reboot_os  DUT
  OS Disconnect Device
  Sleep  250
  OS Connect Device
  change_directory   DUT  "/root/athena_gen2_fw/BMC"
  whitebox_lib.execute  DUT  rm -rf test.ima
  ${output} =  execute_Linux_command   dd if=/dev/null of=./test.ima count=32768 bs=1024
  common_check_patern_2    ${output}     records in      Check 00 Records in  expect=True
  common_check_patern_2    ${output}     records out      Check 00 Records out  expect=True
  ${output} =  execute_Linux_command   ./socflash_x64 -s test.ima
  common_check_patern_2    ${output}     Update Flash Chip O.K      Check BMC Firmware Update  expect=True
  Sleep  60
  reboot_os  DUT
  OS Disconnect Device
  Sleep  250
  OS Connect Device
  ${BMC_MAC_address2a}  get_info_from_lan_print  DUT  MAC Address  True  ${ipa}
  common_check_patern_2    ${BMC_MAC_address1a}     ${BMC_MAC_address2a}      check MAC address not swipe out on ESMA  expect=True
  ${mc_info_after_update} =  get_bmc_version_ipmitool   DUT  ${ipa}
  common_check_patern_2    ${mc_info_before_update}     ${mc_info_after_update}      Verify BMC Version  expect=True
  Verify the SEL and ensure no error
  Verify abnormal event log  DUT  ${ipa}
  verifythesensorreadingandcheckstatus  DUT  ${ipa}
  OS Disconnect Device
  Remove Athena BMC FW image

BMC firmware upgrade with socflash
   [Arguments]   ${module}  ${version}  ${key}  ${action}
   server Connect ESMB
   mkdir_data_path    DUT  "/root/athena_gen2_fw/BMC"
   change_directory   DUT  "/root/athena_gen2_fw/BMC"
   downloadAthenaSesFwImage    DUT   Athena_FW_BMC_B
   ${image_to_upgrade_downgrade} =  get_image_version_for_upgrade_downgrade  ${module}  ${version}  ${key}
   Log  ${image_to_upgrade_downgrade}
   ${ip}  get_ip_address_from_ipmitool  DUT
   Verify event log SEL clear  DUT  ${ip}
   ${BMC_MAC_address1b}  get_info_from_lan_print  DUT  MAC Address  True
   change_directory   DUT  /root/athena_gen2_fw/BMC
   upgrade with socflash  DUT   ./socflash_x64 if=${image_to_upgrade_downgrade} cs=0
   Sleep  30
   upgrade with socflash  DUT   ./socflash_x64 if=${image_to_upgrade_downgrade} cs=1
   Sleep  60
   getBMCFWimageversion  DUT  ${module}   ${get_BMC_version}  ${get_BMC_version_next}  ${action}
   ${BMC_MAC_address2b}  get_info_from_lan_print  DUT  MAC Address  True
   common_check_patern_2    ${BMC_MAC_address1b}     ${BMC_MAC_address2b}      check MAC address not swipe out on ESMB   expect=True
   Verify the SEL and ensure no error
   change_directory   DUT  "/root/athena_gen2_fw/BMC"
   RemoveAthenaBIOSFwImage    DUT   Athena_FW_BMC_B
   Server Disconnect

Flash bmc and Terminate the flash process during bmc load driver
   [Arguments]    ${updateinfo}
   Download Athena BMC FW image
   OS Connect Device
   ${ipa}  get_ip_address_from_ipmitool  DUT
   Verify event log SEL clear  DUT  ${ipa}
   ${BMC_MAC_address1a}  get_info_from_lan_print  DUT  MAC Address  True  ${ipa}
   ${mc_info_before_update} =  get_bmc_version_ipmitool   DUT  ${ipa}
   CheckBMCFWFlash  DUT  Athena_FW_BMC_A  ${updateinfo}
   ${BMC_MAC_address2a}  get_info_from_lan_print  DUT  MAC Address  True  ${ipa}
   common_check_patern_2    ${BMC_MAC_address1a}     ${BMC_MAC_address2a}      check MAC address not swipe out on ESMA  expect=True
   ${mc_info_after_update} =  get_bmc_version_ipmitool   DUT  ${ipa}
   common_check_patern_2    ${mc_info_before_update}     ${mc_info_after_update}      Verify BMC Version on ESMA  expect=True
   Verify the SEL and ensure no error
   Verify abnormal event log  DUT  ${ipa}
   verifythesensorreadingandcheckstatus  DUT  ${ipa}
   OS Disconnect Device
   ConnectESMB
   ${ipb}  get_ip_address_from_ipmitool  DUT
   Verify event log SEL clear  DUT  ${ipb}
   ${BMC_MAC_address1b}  get_info_from_lan_print  DUT  MAC Address  True  ${ipb}
   ${mc_info_before_update} =  get_bmc_version_ipmitool   DUT  ${ipb}
   CheckBMCFWFlash  DUT  Athena_FW_BMC_B  ${updateinfo}
   ${BMC_MAC_address2b}  get_info_from_lan_print  DUT  MAC Address  True  ${ipb}
   common_check_patern_2    ${BMC_MAC_address1b}     ${BMC_MAC_address2b}      check MAC address not swipe out on ESMB  expect=True
   ${mc_info_after_update} =  get_bmc_version_ipmitool   DUT  ${ipb}
   common_check_patern_2    ${mc_info_before_update}     ${mc_info_after_update}      Verify BMC Version on ESMB  expect=True
   Verify the SEL and ensure no error
   Verify abnormal event log  DUT  ${ipb}
   verifythesensorreadingandcheckstatus  DUT  ${ipb}
   OS Disconnect Device
   Remove Athena BMC FW image

*** Keywords ***
Print Loop Info
    [Arguments]    ${CUR_INDEX}
    Log   *******************************************
    Log   *** Test Loop \#: ${CUR_INDEX} / ${LoopCnt} ***
    Log   *
