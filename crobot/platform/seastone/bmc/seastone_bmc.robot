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
# Script       : BMC.robot                                                                                            #
# Date         : July 29, 2020                                                                                        #
# Author       : James Shi <jameshi@celestica.com>                                                                    #
# Description  : This script will validate BMC                                                                        #
#                                                                                                                     #
# Script Revision Details:                                                                                            #
#   Initial Draft for bmc testing                                                                                      #
#######################################################################################################################

*** Settings ***
Documentation       Tests to verify BMC functions described in the BMC function SPEC for the whiteboxproject.

# Force Tags        BMC
Variables         SeastoneBMCVariable.py
Library           ../SEASTONECommonLib.py
Library           SeastoneBMCLib.py
#Library           bios_menu_lib.py
Resource          SeastoneBMCkeywords.robot
Resource          CommonResource.robot

Suite Setup       DIAG OS Connect 
Suite Teardown    DIAG OS Disconnect 
** Variables ***
# It is recommended to use <{ScriptName}|{FeatureName}|{DomainName}_Variable> file for variable declaration with help of
# setting table. This section should keep blank.
#In extreme case if script requires variable then it should be defined in this table with documentaiton tag

*** Test Cases ***
# *** comment ***

SEASTONE2V2_BMC_Device_Info_Check_Test
   [Documentation]  Test to verify BMC device info
   [Tags]  SEASTONE2V2_BMC_Device_Info_Check_Test  Seastone2V2  AMI_BMC
   Step  1  check bmc version info  DUT
   Step  2  bmc reset  DUT  cold
   Step  3  check bmc version info  DUT
   Step  4  bmc reset  DUT  warm
   Step  5  check bmc version info  DUT
   

SEASTONE2V2_BMC_Lan_Communication_Test
    [Documentation]  To verify if the LAN interface can be cSEASTONE2V2_BMConfigured through device.
    [Tags]     SEASTONE2V2_BMC_Lan_Communication_Test  Seastone2V2  AMI_BMC
    Step  1  check_lan_print_info  DUT  exp_ip_addr=${mgmt_ip}  exp_ip_status=${dhcp_add}  exp_subnet_mask=${net_mask}
    Step  2  set_bmc_ip_status  DUT  static
    Step  3  set_bmc_ip_netmask  DUT  ipaddr=${set_bmc_ipaddr}  netmask=${set_bmc_netmask}
    Step  4  check_lan_print_info  DUT  exp_ip_addr=${set_bmc_ipaddr}  exp_subnet_mask=${set_bmc_netmask}  exp_ip_status=${static_add}
    Step  5  set_bmc_ip_status  DUT  dhcp
    Step  6  check_lan_print_info  DUT  exp_ip_addr=${mgmt_ip}  exp_ip_status=${dhcp_add}  exp_subnet_mask=${net_mask}


SEASTONE2V2_BMC_Lan_Configuration_Test
    [Documentation]  To verify if the LAN interface can be configured through server.
    [Tags]     SEASTONE2V2_BMC_Lan_Configuration_Test  Seastone2V2  AMI_BMC
    Step  1  check server seastone  DUT  ${scp_ip}  ${scp_username}  ${scp_password}  ${dhcp_prompt}
    Step  2  check_lan_print_info  DUT  exp_ip_addr=${mgmt_ip}  exp_ip_status=${dhcp_add}  exp_subnet_mask=${net_mask}  lanplus=True
    Step  3  set_bmc_ip_status  DUT  static  lanplus=True
    Step  4  set_bmc_ip_netmask  DUT  ipaddr=${set_bmc_ipaddr}  netmask=${set_bmc_netmask}  lanplus=True
    Step  5  check_lan_print_info  DUT  exp_ip_addr=${set_bmc_ipaddr}  exp_subnet_mask=${set_bmc_netmask}  exp_ip_status=${static_add}  lanplus=True
    Step  6  set_bmc_ip_status  DUT  dhcp  lanplus=True
    Step  7  check_lan_print_info  DUT  exp_ip_addr=${mgmt_ip}  exp_ip_status=${dhcp_add}  exp_subnet_mask=${net_mask}  lanplus=True
    Step  8  exit the server  DUT
    [Teardown]  Run Keyword If Test Failed  exit the server  DUT


Seastone2v2_BMC_Memory_Test
    [Documentation]  To verify memory of bmc
    [Tags]  Seastone2v2_BMC_Memory_Test  AMI_BMC  Seastone2v2
    Step  1  check memory status  ${bmc_memory_disabled}
    Step  2  enable bmc memory
    Step  3  check memory status  ${bmc_memory_enabled}
    Step  4  disable bmc memory
    Step  5  check memory status  ${bmc_memory_disabled}


SEASTONE2V2_BMC_MAC_Address_Test
    [Documentation]  To verify update bmc mac address functionality
    [Tags]     SEASTONE2V2_BMC_MAC_Address_Test  AMI_BMC  Seastone2V2
    Step  1  check_lan_print_info  DUT  exp_mac_addr=${mac_addr}
    Step  2  set_fru1_mac  DUT  ${write_fru1_mac}
    Step  3  check_mac_in_lan_and_fru  DUT  ${write_fru1_mac}  ${response_lan1_mac}
    Step  4  set_fru1_mac  DUT  ${wrong_mac}
    Step  5  check_mac_in_lan_and_fru  DUT  ${wrong_mac}  ${response_lan1_mac}
    Step  6  set_fru1_mac  DUT  ${device_mac_string}
    Step  7  check_mac_in_lan_and_fru  DUT  ${device_mac_string}  ${mac_addr}


SEASTONE2V2_BMC_User_Operation_Test
    [Documentation]  To verify user operation access commands through ipmitool
    [Tags]  SEASTONE2V2_BMC_User_Operation_Test  AMI_BMC  Seastone2V2
    Step  1  check_add_single_user  DUT  3  tester
    Step  2  set_user_password  DUT  3  testtest  16
    Step  3  test_user_password  DUT  3  testtest  testtest123  len16=True
    Step  4  set_user_password  DUT  3  testtest123  20
    Step  5  test_user_password  DUT  3  testtest123  testtest  len20=True
    Step  6  enable_user_and_ipmi_message  DUT  3  tester
    Step  7  check_lanplus_communication_through_user  DUT  3  tester  testtest123
    Step  8  check_add_all_users  DUT  4  15
    Step  9  check_add_single_user  DUT  16  user16  False
    [Teardown]  delete_all_new_user_info  DUT


SEASTONE2V2_BMC_User_Priviledge_Test
    [Documentation]  To verify user priviledge access in ipmitool
    [Tags]  SEASTONE2V2_BMC_User_Priviledge_Test  AMI_BMC  Seastone2V2
    Step  1  check_add_single_user  DUT  3  tester
    Step  2  set_user_password  DUT  3  testtest  16
    Step  3  test_user_password  DUT  3  testtest  testtest123  len16=True
    Step  4  check_set_user_priviledge  DUT  3  tester  testtest
    [Teardown]  delete_all_new_user_info  DUT


SEASTONEV2_BMC_Console_Baurdrate_Setting
    [Documentation]  To verify baurd rate setting through bmc console
    [Tags]  SEASTONEV2_BMC_Console_Baurdrate_Setting  AMI_BMC  Seastone2V2
    Step  1  check_set_baurd_rate  DUT  5  1
    [Teardown]  Run Keyword If Test Failed  check_set_baurd_rate  DUT  1  1


SEASTONEV2_BMC_SOL_Configuration_Test
    [Documentation]  To verify bmc sol configuration commands
    [Tags]  SEASTONEV2_BMC_SOL_Configuration_Test  AMI_BMC  Seastone2V2
    Step  1  check server seastone  DUT  ${scp_ip}  ${scp_username}  ${scp_password}  ${dhcp_prompt}
    Step  2  set_and_check_sol_configuration  DUT  enabled  false
    Step  3  set_and_check_sol_configuration  DUT  non-volatile-bit-rate  57.6
    Step  4  set_and_check_sol_configuration  DUT  volatile-bit-rate  57.6
    Step  5  bmc_reset  DUT  cold  lanplus=True
    Step  6  check_sol_configuration  DUT  enabled  false 
    Step  7  check_sol_configuration  DUT  non-volatile-bit-rate  57.6 
    Step  8  check_sol_configuration  DUT  volatile-bit-rate  57.6
    Step  9  reset_sol_configuration  
    [Teardown]  Run Keyword If Test Failed  reset_sol_configuration   


SEASTONEV2_BMC_KCS_Interface_Test
    [Documentation]  To verify KCS interfaces and communication via KCS from BMC to BIOS.
    [Tags]  SEASTONEV2_BMC_KCS_Interface_Test  AMI_BMC  Seastone2V2
    Step  1  set_modprobe  DUT
    Step  2  initialize_kcs_interface  DUT 
    Step  3  check_bmc_version_info  DUT
    Step  4  check_lan_print_info  DUT  exp_ip_addr=${mgmt_ip}  exp_ip_status=${dhcp_add}  exp_subnet_mask=${net_mask}  exp_mac_addr=${mac_addr}
    Step  5  clear_sel_list  DUT
    Step  6  boot_bios_through_ipmitool_raw  DUT


SEASTONEV2_BMC_Online_Update_Test_via_LAN
    [Documentation]  9.4.1  To verify online update of image through LAN
    [Tags]     SEASTONE_BMC_Online_Update_Test_via_LAN  AMI_BMC  Seastone2V2
    Step  1  check_server_seastone  DUT  ${scp_ip}  ${scp_username}  ${scp_password}  ${dhcp_prompt}
    Step  2  update_primary_bmc  DUT  ${seastone_bmc_old_img}
    Step  3  check_bmc_version_through_raw_cmd  DUT  ${version1}  True
    Step  4  update_primary_bmc  DUT  ${seastone_bmc_new_img}
    Step  5  check_bmc_version_through_raw_cmd  DUT  ${version2}  True
    Step  6  exit_the_server  DUT
    [Teardown]  Run Keyword If Test Failed  end online update via lan


SEASTONEV2_BMC_Clear_CMOS_By IPMI
    [Documentation]  To verify cmos clear functionality through ipmi command
    [Tags]  SEASTONEV2_BMC_Clear_CMOS_By  AMI_BMC  Seastone2V2
    Step  1  set_power_chasis  DUT  off
    Step  2  clear_cmos_by_ipmi_lanplus  DUT
    Step  3  set_power_chasis  DUT  on


SEASTONEV2_BMC_CHASSIS_POWER_TEST
   [Documentation]  To verify power chassis test using ipmitool
   [Tags]  SEASTONEV2_BMC_CHASSIS_POWER_TEST  AMI_BMC  Seastone2V2
   Step  1  check power chasis status  DUT  on
   Step  2  set power chasis  DUT  off
   Step  3  check power chasis status  DUT  off
   Step  4  set power chasis  DUT  on
   Step  5  check power chasis status  DUT  on
   [Teardown]  Run Keyword If Test Failed  set power chasis  DUT  on


SEASTONEV2_BMC_Extensional_I2C_Master_Write_Read
    [Documentation]  To verify extensional I2C master read and write operations
    [Tags]  SEASTONEV2_BMC_Extensional_I2C_Master_Write_Read  AMI_BMC  Seastone2V2
    Step  1  write_data_to_bus  DUT  
    Step  2  read_data_from_bus  DUT
    Step  3  read_data_with_invalid_length  DUT
    [Teardown]   power_cycle_and_login  DUT


SEASTONEV2_BMC_FRU_Access_Test
    [Documentation]  To verify fru access commands
    [Tags]  SEASTONEV2_BMC_FRU_Access_Test  AMI_BMC  Seastone2V2
    Step  1  check_fru_list  DUT
    Step  2  execute_fru_eeprom_bin_sh  DUT
    Step  3  check_fru_size  DUT
    Step  4  update_fru_data  DUT  7
    Step  5  update_date_and_mfg_name  DUT  0
    [Teardown]  reset_fru_device_to_default  DUT  0  7


SEASTONEV2_BMC_Bios_Update_Test_Via_Lan
    [Documentation]   To verify bios image update through LAN
    [Tags]   SEASTONEV2_BMC_Bios_Update_Test_Via_Lan  Seastone2v2  AMI_BMC
    Step  1  downgrade primary bios image through lan
    Step  2  upgrade primary bios image through lan
    [Teardown]  Run Keyword If Test Failed  bios_boot  DUT  0


SEASTONEV2_BMC_SSH_Login_Test
    [Documentation]  To verify ssh login of device
    [Tags]  SEASTONEV2_BMC_SSH_Login_Test  AMI_BMC  Seastone2V2
    Step  1  ssh_into_seastonev2_device  DUT  ${mgmt_ip}  ${bmc_user}  ${bmc_pass}  ${bmc_prompt}
    [Teardown]  Run Keyword If Test Failed  exit_from_seastonev2_device  DUT


SEASTONEV2_BMC_Baseboard_CLPD_Update_Test
    [Documentation]  To verify update baseboard clpd version
    [Tags]  SEASTONEV2_BMC_Baseboard_CLPD_Update_Test  AMI_BMC  Seastone2V2
    Step  1  update_baseboard_clpd_image  DUT  ${clpd_image_name}
    Step  2  bios_boot  DUT  0
    Step  3  check_baseboard_clpd_version  DUT  ${clpd_image_name}
    [Teardown]  Run Keyword If Test Failed  exit_the_server  DUT
 

SEASTONEV2_BMC_Get_Set_Fan_Settings_test
    [Documentation]  To verify FCS and PWM settings of fans and PSUs
    [Tags]  SEASTONEV2_BMC_Get_Set_Fan_Settings_test  AMI_BMC  Seastone2V2
    Step  1  check_fcs_status  DUT  ${enable_fcs} 
    Step  2  check_all_fan_psu_status  DUT  
    Step  3  check_set_fcs_status  DUT  ${disable_fcs}
    Step  4  check_set_fcs_status  DUT  ${enable_fcs}
    [Teardown]   Run Keyword If Test Failed  check_set_fcs_status  DUT  ${enable_fcs}
  

SEASTONEV2_BMC_Discrete_Sensor_Monitor_SEL
    [Documentation]  To verify assertion and deassertion of sensor monitors through a script
    [Tags]  SEASTONEV2_BMC_Discrete_Sensor_Monitor_SEL  AMI_BMC  Seastone2V2  check
    Step  1  run_script_through_lan  DUT
    Step  2  run_script_through_kcs  DUT
    [Teardown]  Run Keyword If Test Failed  exit_the_server  DUT

SEASTONE_V2_BMC_Disable_Enable_Scan
    [Documentation]  Test to verify BMC disable/enable scan
    [Tags]  SEASTONE_V2_BMC_Device_Disable_Enable_Scan  seastonev2_fan_scan  3.15.2  AMI_BMC  check
    [Setup]  DIAG OS Connect
    Step  1  check bmc version info  DUT
    Step  2  disable enable fan sensor  c0
    [Teardown]  DIAG OS Disconnect


SEASTONE_V2_BMC_Disable_Enable_Virtual_Usb
    [Documentation]  Test to verify BMC disable/enable virtual usb
    [Tags]  SEASTONE_V2_BMC_Device_Disable_Enable_USB_Scan  seastonev2_usb_scan  3.16.5  AMI_BMC  check
    [Setup]  DIAG OS Connect
    Step  1  check bmc version info  DUT
    Step  2  disable enable virtual usb  00  01
    [Teardown]  DIAG OS Disconnect


BMC_Power_Control_Test
    [Documentation]  9.5.2 To verify BMC can correctly control the system power to different
                    ...  states: power on, power off, power cycle, reset.
    [Tags]     BMC_Power_Control_Test  seastone2_power_control  3.7.2  AMI_BMC
    [Setup]  DIAG OS Connect
    ${ip}  get_ip_address_from_ipmitool  DUT
    #independent_step  1  power_cycle_os  DUT
    Step  1  power cycle onl  DUT  ${ip}
    Step  2  Sleep  30s
    Step  3  DIAG OS Connect
    #Step  4  power off onl  DUT
    Step  4  set power status  DUT  off  ${ip}
    Step  5  Sleep  30s
    #Step  5  switch bmc  DUT
    #Step  6  ${off}  get chassis power status  DUT  127.0.0.1
    #Step  7  check info equal  ${off}  off
    Step  7  poweruptheunit  DUT  ${ip}  on
    #Step  8  set power status  DUT  on  ${ip}
    Step  8  Sleep  30s
    #${on}  get chassis power status  DUT  ${ip}
    #Step  11  check info equal  ${on}  on
    Step  9  DIAG OS Disconnect
    Step  10  DIAG OS Connect
    Step  11  power reset onl  DUT  ${ip}
    Step  12  Sleep  30s
    Step  13  DIAG OS Disconnect
    Step  14  DIAG OS Connect
    Step  15  check chassis power status  DUT  ${ip}  on
    [Teardown]  DIAG OS Disconnect

SEASTONE_V2_BMC_Disable_SDR_Test
    [Documentation]  Test to run BMC SDR Test
    [Tags]  SEASTONE_V2_BMC_Device_SDR_Test  seastonev2_sdr  3.8.1  AMI_BMC
    [Setup]  DIAG OS Connect
    Step  1  check bmc version info  DUT
    Step  2  sdr test  DUT
    [Teardown]  DIAG OS Disconnect


System_ACPI_Control_Test
    [Documentation]  9.5.2 To verify System ACPI State
                    ...  states: power on, power off, power cycle, reset.
    [Tags]     BMC_Power_Control_Test  seastone2_acpi_control  3.7.2  AMI_BMC
    [Setup]  DIAG OS Connect
    ${ip}  get_ip_address_from_ipmitool  DUT
    #independent_step  1  power_cycle_os  DUT
    Step  0  verifyeventlogSELclear  DUT  ${ip}
    Step  1  power cycle onl  DUT  ${ip}
    Step  2  Sleep  50s
    Step  4  DIAG OS Connect
    Step  5  verify sel list power cycle
    Step  7  set power status  DUT  off  ${ip}
    Step  8  Sleep  50s
    Step  9  poweruptheunit  DUT  ${ip}  on
    Step  10  Sleep  50s
    Step  11  DIAG OS Disconnect
    Step  12  DIAG OS Connect
    Step  13  power reset onl  DUT  ${ip}
    Step  14  Sleep  50s
    Step  15  DIAG OS Disconnect
    Step  16  DIAG OS Connect
    Step  17  check chassis power status  DUT  ${ip}  on
    [Teardown]  DIAG OS Disconnect

Fan_Led_Test
    [Documentation]  9.5.2 To verify Fan led status
                    ...  states: verify,automatic, manual mode
    [Tags]     Fan_led_test  seastone2_fan_led  AMI_BMC
    [Setup]  DIAG OS Connect
    ${ip}  get_ip_address_from_ipmitool  DUT
    #independent_step  1  power_cycle_os  DUT
    Step  0  verifyeventlogSELclear  DUT  ${ip}
    Step  1  verify fan led policy
    [Teardown]  DIAG OS Disconnect

Alarm_Led_Test
    [Documentation]  9.5.2 To verify Alarm led status
                    ...  states: verify,automatic, manual mode
    [Tags]     Alarm_led_test  seastone2_alarm_led  AMI_BMC
    [Setup]  DIAG OS Connect
    ${ip}  get_ip_address_from_ipmitool  DUT
    #independent_step  1  power_cycle_os  DUT
    Step  0  verifyeventlogSELclear  DUT  ${ip}
    Step  1  verify alarm led policy
    [Teardown]  DIAG OS Disconnect

Event_Generation_Test
    [Documentation]  9.5.2 To verify event generation test
                    ...  Discreete sensor
    [Tags]     event_generation_test  seastone2_event_generation  AMI_BMC
    [Setup]  DIAG OS Connect
    ${ip}  get_ip_address_from_ipmitool  DUT
    #independent_step  1  power_cycle_os  DUT
    Step  0  verifyeventlogSELclear  DUT  ${ip}
    #Checking for Fan_Front sensor
    FOR    ${INDEX}    IN RANGE    11    16
         Step  1  verifyeventlogSELclear  DUT  ${ip}
         Step  2  event generation test  DUT  ${INDEX}
         Step  3  verify sel list Fan assert deassert
    END
    [Teardown]  DIAG OS Disconnect


SEL_Operation_Test
    [Documentation]  9.5.2 To verify Sel operation Test
                    ...  Discreete sensor
    [Tags]     SEL_Operation_test  seastone2_operation_test  AMI_BMC
    [Setup]  DIAG OS Connect
    ${ip}  get_ip_address_from_ipmitool  DUT
    Step  0  verifyeventlogSELclear  DUT  ${ip}
    #Checking for linear and circular log
    Step  1  verify sel operation test
    Step  2  sel policy test  DUT
    [Teardown]  DIAG OS Disconnect


SOL_Authentication_Test
    [Documentation]  9.5.2 To verify Sol operation for all authentication
                    ...  user levels
    [Tags]     SOL_auth_test  seastone2_operation_test
    [Setup]  DIAG OS Connect
    ${ip}  get_ip_address_from_ipmitool  DUT
    #Checking and adding user tester with privilege level USER,user tester1 with privilege lever OPERATOR and tester2 with ADMIN
    Step  0  verifyeventlogSELclear  DUT  ${ip}
    Step  0  delete_all_new_user_info  DUT
    Step  1  check_add_single_user  DUT  3  tester
    Step  2  set_user_password  DUT  3  testtest  16
    Step  4  enable_user_and_ipmi_message  DUT  3  tester
    Step  5  check_lanplus_communication_through_user  DUT  3  tester  testtest
    #Setting user tester to USER
    Step  6  set_user_privilege  DUT  3  2
    Step  7  check_add_single_user  DUT  4  tester1
    Step  8  set_user_password  DUT  4  testtest1  16
    Step  9  enable_user_and_ipmi_message  DUT  4  tester1
    Step  10  check_lanplus_communication_through_user  DUT  4  tester1  testtest1
    #Setting user tester1 to OPERATOR
    Step  11  set_user_privilege  DUT  4  3
    #Create user tester2
    Step  12  check_add_single_user  DUT  5  tester2
    Step  13  set_user_password  DUT  5  testtest2  16
    Step  14  enable_user_and_ipmi_message  DUT  5  tester2
    Step  15  check_lanplus_communication_through_user  DUT  5  tester2  testtest2
    #Setting user tester2 to ADMIN
    Step  16  set_user_privilege  DUT  5  4
    Step  17  set_and_check_sol_config  DUT  enabled  true
    Step  18  set_and_check_sol_auth  DUT  privilege-level  operator
    Step  19  set_sol_payload  DUT  1  3
    Step  20  set_sol_payload  DUT  1  4
    Step  21  set_sol_payload  DUT  1  5
    Step  22  check_sol_activate  DUT
    #Sol activate fails for USER user and works fine for operator level alone
    Step  22  delete_all_new_user_info  DUT
    #Step  20  reset_sol_configuration
    #[Teardown]  Run Keyword If Test Failed  reset_sol_configuration
    [Teardown]  DIAG OS Disconnect


Out_Of_record_Sel_List
    # Step 8，9，10 Have been checked in every Step
    [Documentation]  3.16.1 To verify out of record sel list
                    ...  Discreete sensor
    [Tags]     SEL_Record_test  seastone2_operation_test
    [Setup]  DIAG OS Connect
    ${ip}  get_ip_address_from_ipmitool  DUT
    Step  0  verifyeventlogSELclear  DUT  ${ip}
    #Checking for linear and circular log
    Step  1  verify sel operation test
    Step  2  out_of_record_sel  DUT
    [Teardown]  DIAG OS Disconnect


Dual_BMC_Test
    # Step 8，9，10 Have been checked in every Step
    [Documentation]  9.5.2 To verify Dual BMC Image test
                    ...  BMC Dual image test
    [Tags]     dual_bmc_test  seastone2_operation_test  AMI_BMC
    [Setup]  DIAG OS Connect
    ${ip}  get_ip_address_from_ipmitool  DUT
    Step  0  verifyeventlogSELclear  DUT  ${ip}
    #Switch for primary version
    Step  1  dual bmc test  01 
    Step  2  reset bmc  cold
    Step  3  check switched bmc  01
    #Switch for secondary version
    Step  4  dual bmc test  02 
    Step  5  reset bmc  cold
    Step  6  check switched bmc  02
    #Switch for primary version
    Step  7  dual bmc test  01 
    Step  8  reset bmc  cold
    Step  9  check switched bmc  01


PEF_Configuration_Test
    [Documentation]  9.8.1  To verify the PEF related information can be set can get correctly.
    [Tags]     PEF_Configuration_Test  seastonev2_config_test  AMI_BMC
    ${ip}  get_ip_address_from_ipmitool  DUT
    independent_step  1  send_cmd  DUT  ${cmd_Get_PEF_Capabilities}
    independent_step  2.1  send_cmd  DUT  ${ssl_cmd_Set_PEF_Capabilities_1}
    independent_step  2.2  send_cmd  DUT  ${ssl_cmd_Set_PEF_Capabilities_2}
    independent_step  2.3  send_cmd  DUT  ${ssl_cmd_Set_PEF_Capabilities_3}
    independent_step  2.4  send_cmd  DUT  ${ssl_cmd_Set_PEF_Capabilities_4}
    independent_step  2.5  send_cmd  DUT  ${ssl_cmd_Set_PEF_Capabilities_5}
    independent_step  3.1  send_cmd  DUT  ${ssl_cmd_Set_PEF_Capabilities_6}
    independent_step  3.2  send_cmd  DUT  ${ssl_cmd_Set_PEF_Capabilities_6}
    independent_step  3.3  send_cmd  DUT  ${show_pef}
    FOR  ${index}  IN RANGE  1  3
         independent_step  3.2  check_cmd_response  DUT  ${ssl_cmd_Get_PEF_Configuration_Parameters_1}
                 ...  ${ssl_rsp_Get_PEF_Configuration_Parameters_1}
         independent_step  3.3  check_cmd_response  DUT  ${ssl_cmd_Get_PEF_Configuration_Parameters_2}
                 ...  ${ssl_rsp_Get_PEF_Configuration_Parameters_2}
         independent_step  3.4  check_cmd_response  DUT  ${ssl_cmd_Get_PEF_Configuration_Parameters_3}
                 ...  ${ssl_rsp_Get_PEF_Configuration_Parameters_3}
         independent_step  3.5  check_cmd_response  DUT  ${ssl_cmd_Get_PEF_Configuration_Parameters_4}
                 ...  ${ssl_rsp_Get_PEF_Configuration_Parameters_4}  re_S=True
         independent_step  3.6  check_cmd_response  DUT  ${ssl_cmd_Get_PEF_Configuration_Parameters_5}
                 ...  ${ssl_rsp_Get_PEF_Configuration_Parameters_5}
    END
    [Teardown]  End PEF Configuration Test


Watchdog_Timer_Configuration_Test
    [Documentation]  9.10.1  9.10.2  To verify the standardized ‘Watchdog Timer’ functions implemented
                    ...  by BMC, including configuring Watchdog Timer.
    [Tags]     Watchdog_Timer_Configuration_Test  AMI_BMC
    ${ip}  get_ip_address_from_ipmitool  DUT
    independent_step  1.1  verifyeventlogSELclear  DUT  ${ip}
    independent_step  1.2  set_watchdog_timer  DUT  1  0
    independent_step  1.3  check_watchdog_update  DUT  1  0
    independent_step  1.4  set_watchdog_start  DUT
    independent_step  1.5  check_watchdog_counting_down  DUT  1  60  5
    independent_step  1.6  check_bmc_sel_list_keyword  DUT  Hard reset,Power down,soft-off,working  False
    independent_step  1.7  check_bmc_sel_list_keyword  DUT  Watchdog2
    independent_step  2.1  verifyeventlogSELclear  DUT  ${ip}
    independent_step  2.2  set_watchdog_timer  DUT  2  1
    independent_step  2.3  check_watchdog_update  DUT  2  1
    independent_step  2.4  set_watchdog_start  DUT
    independent_step  2.5  set_wait  60
    independent_step  2.6  DIAG OS Connect
    independent_step  2.7  check_bmc_sel_list_keyword  DUT  Watchdog,Hard reset
    independent_step  3.1  verifyeventlogSELclear  DUT  ${ip}
    independent_step  3.2  set_watchdog_timer  DUT  3  2
    independent_step  3.3  check_watchdog_update  DUT  3  2
    independent_step  3.4  set_watchdog_start  DUT
    independent_step  3.5  DIAG OS Disconnect
    independent_step  3.6  set_wait  20
    independent_step  3.7  set power status  DUT  on  ${ip}
    independent_step  3.8  set_wait  150
    independent_step  3.9  DIAG OS Connect
    independent_step  3.10  check_bmc_sel_list_keyword  DUT  Power down
    independent_step  4.1  verifyeventlogSELclear  DUT  ${ip}
    independent_step  4.2  set_watchdog_timer  DUT  4  3
    independent_step  4.3  check_watchdog_update  DUT  4  3
    independent_step  4.4  set_watchdog_start  DUT
    independent_step  4.5  DIAG OS Disconnect
    independent_step  4.6  set_wait  150
    independent_step  4.7  DIAG OS Connect
    independent_step  4.8  check_bmc_sel_list_keyword  DUT  soft-off,working
    [Teardown]  DIAG OS Disconnect


Watchdog_Event_Logging_Test
    [Documentation]  9.10.3 To verify if BMC can log or ignore the watchdog event successfully
    [Tags]     Watchdog_Event_Logging_Test  AMI_BMC
    ${ip}  get_ip_address_from_ipmitool  DUT
    independent_step  0  DIAG OS Disconnect
    independent_step  0  DIAG OS Connect
    independent_step  1.1  verifyeventlogSELclear  DUT  ${ip}
    independent_step  1.2  set_watchdog_timer  DUT  81  0
    independent_step  1.3  check_watchdog_update  DUT  81  0
    independent_step  1.4  set_watchdog_start  DUT
    independent_step  1.5  check_watchdog_counting_down  DUT  1  30  5  None
    independent_step  1.6  check_bmc_sel_list_keyword  DUT  keyword=Watchdog2,Hard reset,Power down,soft-off,working  decide=False
    independent_step  2.1  verifyeventlogSELclear  DUT  ${ip}
    independent_step  2.2  set_watchdog_timer  DUT  82  1
    independent_step  2.3  check_watchdog_update  DUT  82  1
    independent_step  2.4  set_watchdog_start  DUT
    independent_step  2.4  DIAG OS Disconnect
    independent_step  2.5  check_watchdog_counting_down  DUT  1  20  150  ${ip}
    independent_step  2.6  set_wait  20
    independent_step  2.6  DIAG OS Connect
    independent_step  2.6  check_bmc_sel_list_keyword  DUT  keyword=Watchdog,Hard reset  decide=False
    independent_step  3.1  verifyeventlogSELclear  DUT  ${ip}
    independent_step  3.2  set_watchdog_timer  DUT  83  2
    independent_step  3.3  check_watchdog_update  DUT  83  2
    independent_step  3.4  set_watchdog_start  DUT
    independent_step  3.5  DIAG OS Disconnect
    independent_step  3.6  set_wait  20
    independent_step  3.7  set_power_status  DUT  on  ${ip}
    independent_step  3.8  set_wait  180
    independent_step  3.9  DIAG OS Connect
    independent_step  3.10  check_bmc_sel_list_keyword  DUT  keyword=Watchdog,Power down  decide=False
    independent_step  4.1  verifyeventlogSELclear  DUT  ${ip}
    independent_step  4.2  set_watchdog_timer  DUT  84  3
    independent_step  4.3  check_watchdog_update  DUT  84  3
    independent_step  4.4  set_watchdog_start  DUT
    independent_step  4.4  DIAG OS Disconnect
    independent_step  4.5  check_watchdog_counting_down  DUT  1  20  150  ${ip}
    independent_step  4.6  DIAG OS Connect
    independent_step  4.7  check_bmc_sel_list_keyword  DUT  keyword=soft-off,working
    independent_step  4.8  check_bmc_sel_list_keyword  DUT  keyword=Watchdog  decide=False
    independent_step  5.1  verifyeventlogSELclear  DUT  ${ip}
    independent_step  5.2  set_watchdog_timer  DUT  85  3
    independent_step  5.3  check_watchdog_update  DUT  85  3
    independent_step  5.4  set_watchdog_start  DUT
    independent_step  5.4  DIAG OS Disconnect
    independent_step  5.5  check_watchdog_counting_down  DUT  1  20  150  ${ip}
    independent_step  5.6  DIAG OS Connect
    independent_step  5.7  check_bmc_sel_list_keyword  DUT  keyword=soft-off,working
    independent_step  5.8  check_bmc_sel_list_keyword  DUT  keyword=Watchdog  decide=False
    independent_step  6.1  verifyeventlogSELclear  DUT  ${ip}
    independent_step  6.2  set_watchdog_timer  DUT  1  0
    independent_step  6.3  check_watchdog_update  DUT  1  0
    independent_step  6.4  set_watchdog_start  DUT
    independent_step  6.5  check_watchdog_counting_down  DUT  1  20  5  None
    independent_step  6.6  check_bmc_sel_list_keyword  DUT  keyword=Hard reset,Power down,soft-off,working  decide=False
    independent_step  6.7  check_bmc_sel_list_keyword  DUT  keyword=Watchdog2
    independent_step  7.1  verifyeventlogSELclear  DUT  ${ip}
    independent_step  7.2  set_watchdog_timer  DUT  2  1
    independent_step  7.3  check_watchdog_update  DUT  2  1
    independent_step  7.4  set_watchdog_start  DUT
    independent_step  7.4  DIAG OS Disconnect
    independent_step  7.5  check_watchdog_counting_down  DUT  1  20  150  ${ip}
    independent_step  7.6  DIAG OS Connect
    independent_step  7.7  check_bmc_sel_list_keyword  DUT  keyword=Watchdog,Hard reset
    independent_step  8.1  verifyeventlogSELclear  DUT  ${ip}
    independent_step  8.2  set_watchdog_timer  DUT  3  2
    independent_step  8.3  check_watchdog_update  DUT  3  2
    independent_step  8.4  set_watchdog_start  DUT
    independent_step  8.5  DIAG OS Disconnect
    independent_step  8.6  set_wait  20
    independent_step  8.7  set_power_status  DUT  on  ${ip}
    independent_step  8.7  set_wait  100
    independent_step  8.8  DIAG OS Connect
    independent_step  8.9  check_bmc_sel_list_keyword  DUT  keyword=Power down
    independent_step  9.1  verifyeventlogSELclear  DUT  ${ip}
    independent_step  9.2  set_watchdog_timer  DUT  4  3
    independent_step  9.3  check_watchdog_update  DUT  4  3
    independent_step  9.4  set_watchdog_start  DUT
    independent_step  8.4  DIAG OS Disconnect
    independent_step  9.5  check_watchdog_counting_down  DUT  1  20  150  ${ip}
    independent_step  9.6  DIAG OS Connect
    independent_step  9.7  check_bmc_sel_list_keyword  DUT  keyword=soft-off,working
    independent_step  10.1  verifyeventlogSELclear  DUT  ${ip}
    independent_step  10.2  set_watchdog_timer  DUT  5  3
    independent_step  10.3  check_watchdog_update  DUT  5  3
    independent_step  10.4  set_watchdog_start  DUT
    independent_step  10.4  DIAG OS Disconnect
    independent_step  10.5  check_watchdog_counting_down  DUT  1  20  150  ${ip}
    independent_step  10.6  DIAG OS Connect
    independent_step  10.7  check_bmc_sel_list_keyword  DUT  keyword=soft-off,working
    independent_step  11  DIAG OS Disconnect
    [Teardown]  DIAG OS Disconnect


SEASTONE_V2_BMC_Reset_Stress_Test
    [Documentation]  Test to Stress BMC Reset
    [Tags]  BMC_Reset_Stress_Test
    FOR    ${INDEX}    IN RANGE    1    3
          Step  1  check bmc version info  DUT
          Step  2  reset bmc  cold
          Step  3  check bmc version info  DUT
    END


Read_Write_CPLD_Register
    # Step 8，9，10 Have been checked in every Step
    [Documentation]  9.5.2 To Read/Write CPLD Register
                    ...  states: verify,automatic, manual mode
    [Tags]     cpld_test  seastone2_cpld  AMI_BMC
    [Setup]  DIAG OS Connect
    ${ip}  get_ip_address_from_ipmitool  DUT
    Step  0  verifyeventlogSELclear  DUT  ${ip}
    Step  1  verify read write cpld
    [Teardown]  DIAG OS Disconnect

*** Keywords ***
DiagOS Connect Device
    DiagOSConnect

DiagOS Disconnect Device
    DiagOSDisconnect

OS Connect Device
    OSConnect

#OS Disconnect Device
#    OSDisconnect

#OS Connect Device
#    ConnectESMB

#OS Disconnect Device
#    OSDisconnect

