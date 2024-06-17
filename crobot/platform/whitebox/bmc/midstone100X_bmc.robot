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
# Script       : midstone100i_bmc.robot                                                                               #
# Date         : Feb 23, 2021                                                                                         #
# Author       : Yagami <yajiang@celestica.com>                                                                       #
# Description  : This script will validate BMC                                                                        #
#                                                                                                                     #
# Script Revision Details:                                                                                            #
# Initial Draft for midstone100i bmc testing                                                                        #
#######################################################################################################################

*** Settings ***
Documentation       Tests to verify BMC functions described in the BMC function SPEC for the whiteboxproject.

Variables         BMC_variable.py

Library           ../WhiteboxLibAdapter.py
Library           whitebox_lib.py
#Library           common_lib.py
Library           bios_menu_lib.py
Resource          BMC_keywords.robot
Resource          CommonResource.robot

*** Test Cases ***
BMC_Device_Info_Check
    [Documentation]  9.1.3 To check if BMC version/manufacture id/product id can be printed out correctly
    [Tags]     BMC_Device_Info_Check  Midstone100X  AMI_BMC  
    [Setup]     OS Connect Device
    independent_step  1  check_bmc_version  DUT  ${cmd_ipmitool_mc_info}  ${midstone_bmc_version}
    independent_step  2  set_reset_type  DUT  ${cmd_ipmitool_mc_reset_cold}  reset_type=cold
    independent_step  3  check_bmc_version  DUT  ${cmd_ipmitool_mc_info}  ${midstone_bmc_version}
    independent_step  4  set_reset_type  DUT  ${cmd_ipmitool_mc_reset_warm}  reset_type=warm
    independent_step  5  check_bmc_version  DUT  ${cmd_ipmitool_mc_info}  ${midstone_bmc_version}
    [Teardown]  OS Disconnect Device


User_Operation_Test
    [Documentation]  9.2.1 To check if the user information can be added and updated in user list.
    [Tags]     User_Operation_Test  Midstone100X  AMI_BMC
    [Setup]     OS Connect Device
    FOR  ${num}  IN RANGE  3  17
        del_user_info  DUT  ${num}
    END
    independent_step  1  get_bmc_user_list  DUT  ${cmd_ipmitool_user_list_1}
    independent_step  2  check_add_bmc_user  DUT  3  ${cmd_add_user_test}  True  True
    independent_step  3  check_psw_ascii  DUT  3  testtest  20  True  True
    independent_step  4  check_bmc_user_passwd  DUT  3  testtest  16  decide=False
    independent_step  5  check_bmc_user_passwd  DUT  3  testtest  20  decide=True
    independent_step  6  check_bmc_user_passwd  DUT  3  testtest1  20  decide=False
    independent_step  7  check_psw_ascii  DUT  3  testtest  16  True  True
    independent_step  8  check_bmc_user_passwd  DUT  3  testtest  20  decide=False
    independent_step  9  check_bmc_user_passwd  DUT  3  testtest  16  decide=True
    independent_step  10  check_bmc_user_passwd  DUT  3  testtest1  16  decide=False
    independent_step  11  set_user_name  DUT  3  tester
    independent_step  12  check_bmc_reboot_user_list  DUT  True  True
    FOR  ${index}  IN RANGE  4  16
        independent_step  13  check_add_bmc_user  DUT  ${index}  test${index}  True  True
    END
    independent_step  14  check_add_bmc_user  DUT  16  test16  False  True
    independent_step  15  OS Disconnect Device
    [Teardown]  End User Operation Test

User_Privilege_Test
    [Documentation]  9.2.2  To check if the user privilege can be set and modified.
    [Tags]     User_Privilege_Test  Midstone100X  AMI_BMC
    [Setup]     OS Connect Device
    independent_step  1  check_add_bmc_user  DUT  3  ${cmd_add_user_test}  True  True
    independent_step  2  set_user_privilege  DUT  3   Administrator
    independent_step  3  check_session_status  DUT  ADMINISTRATOR  test  testtest
    independent_step  4  check_session_status  DUT  OPERATOR  test  testtest
    independent_step  5  check_session_status  DUT  USER  test  testtest
    independent_step  6  set_user_privilege  DUT  3   Operator
    independent_step  7  check_session_status  DUT  ADMINISTRATOR  test  testtest  decide=False
    independent_step  8  check_session_status  DUT  OPERATOR  test  testtest
    independent_step  9  check_session_status  DUT  USER  test  testtest
    independent_step  10  set_user_privilege  DUT  3   User
    independent_step  11  check_session_status  DUT  ADMINISTRATOR  test  testtest  decide=False
    independent_step  12  check_session_status  DUT  OPERATOR  test  testtest  decide=False
    independent_step  13  check_session_status  DUT  USER  test  testtest
    independent_step  14  OS Disconnect Device
    [Teardown]  End User Privilege Test


KCS_Interface_Test
    [Documentation]  9.4.1  To verify KCS interfaces and communication via KCS from BMC to BIOS.
    [Tags]     KCS_Interface_Test  Midstone100X  AMI_BMC
    [Setup]     OS Connect Device
    independent_step  1.1  send_cmd  DUT  modprobe ipmi_si
    independent_step  1.2  send_cmd  DUT  modprobe ipmi_devintf
    independent_step  2  check_bmc_kcs_communicate  DUT
    independent_step  3  get_mc_info  DUT
    independent_step  4  set_bmc_ip_status  DUT  static
    independent_step  5  set_bmc_ip  DUT  ipaddr=${set_bmc_ipaddr}
    independent_step  6  set_bmc_ip  DUT  netmask=255.255.0.0
    ${Current_Configuration_sta}  get_info_from_lan_print  DUT  IP Address Source  True
    ${Station_IP_address_sta}  get_info_from_lan_print  DUT  IP Address
    ${Subnet_mask_sta}  get_info_from_lan_print  DUT  Subnet Mask
    ${Station_MAC_address_sta}  get_info_from_lan_print  DUT  MAC Address  True
    independent_step  7  set_wait  120
    independent_step  8  get_network_from_bios  DUT  ${Current_Configuration_sta}  ${Station_IP_address_sta}  ${Subnet_mask_sta}
            ...  ${Station_MAC_address_sta}
    independent_step  9  set_bmc_ip_status  DUT  dhcp
    independent_step  10  set_wait  120
    ${Current_Configuration_dhcp}  get_info_from_lan_print  DUT  IP Address Source  True
    ${Station_IP_address_dhcp}  get_info_from_lan_print  DUT  IP Address
    ${Subnet_mask_dhcp}  get_info_from_lan_print  DUT  Subnet Mask
    ${Station_MAC_address_dhcp}  get_info_from_lan_print  DUT  MAC Address  True
    independent_step  11  check_info_equal  ${Station_IP_address_dhcp}  0.0.0.0  False
    independent_step  12  check_info_equal  ${Subnet_mask_dhcp}  0.0.0.0  False
    independent_step  13  get_network_from_bios  DUT  ${Current_Configuration_dhcp}  ${Station_IP_address_dhcp}  ${Subnet_mask_dhcp}
            ...  ${Station_MAC_address_dhcp}
    independent_step  14  OS Disconnect Device
    [Teardown]  Run Keyword If Test Failed
    ...  Run Keywords
    ...  OS Connect Device  AND
    ...  set_pdu_status_connect_os  DUT  reboot  ${pdu_port}  600  100  AND
    ...  connect  DUT  AND
    ...  set_bmc_ip_status  DUT  dhcp  AND
    ...  set_wait  120  AND
    ...  OS Disconnect Device


LAN_Configuration_Test
    [Documentation]  9.4.2.2 To verify if the LAN interface can be configured.
    [Tags]     LAN_Configuration_Test  Midstone100X  AMI_BMC  
    [Setup]     OS Connect Device
    independent_step  1  set_bmc_ip_status  DUT  dhcp
    independent_step  2  set_wait  40
    ${ip}  get_ip_address_from_ipmitool  DUT
    independent_step  3  check_communication_lan_pc  DUT  ${ip}
    independent_step  4  set_reset_type  DUT  ${cmd_ipmitool_mc_reset_cold}  reset_type=cold
    independent_step  5  set_bmc_ip_status  DUT  static
    independent_step  6  set_bmc_ip  DUT  ipaddr=${set_bmc_ipaddr}
    independent_step  7  set_bmc_ip  DUT  netmask=${set_bmc_netmask}
    independent_step  8  check_bmc_ip_info  DUT  ipaddr=${set_bmc_ipaddr}  netmask=${set_bmc_netmask}
    independent_step  9  set_wait  40
    independent_step  10  check_communication_lan_pc  DUT  ${set_bmc_ipaddr}
    independent_step  11  set_reset_type  DUT  ${cmd_ipmitool_mc_reset_cold}  reset_type=cold
    independent_step  12  set_bmc_ip  DUT  ipaddr=${set_bmc_ipaddr_oth}
    independent_step  13  set_bmc_ip  DUT  netmask=${set_bmc_netmask}
    independent_step  14  check_bmc_ip_info  DUT  ipaddr=${set_bmc_ipaddr_oth}  netmask=${set_bmc_netmask}
    independent_step  15  check_communication_lan_pc  DUT  ${set_bmc_ipaddr_oth}
    independent_step  16  set_reset_type  DUT  ${cmd_ipmitool_mc_reset_cold}  reset_type=cold
    independent_step  13  set_bmc_ip_status  DUT  dhcp
    independent_step  17  set_wait  90
    independent_step  18  check_bmc_ip_info  DUT  ipaddr=${ip}
    independent_step  19  OS Disconnect Device
    [Teardown]  Run Keyword If Test Failed  End LAN Configuration Test


Chassis_Power_Status_Test
    [Documentation]  9.5.1 To verify if BMC can get the correct current power state.
	[Tags]     Chassis_Power_Status_Test  Midstone100X  AMI_BMC
    [Setup]     OS Connect Device
    ${ip}  get_ip_address_from_ipmitool  DUT
    independent_step  1  get_chassis_power_status  DUT
    independent_step  2  check_chassis_power_status  DUT  ${ip}  on
    independent_step  3  check_power_status_cycle  DUT  45
    independent_step  4  set_power_status  DUT  off  ${ip}
    independent_step  5  set_wait  10
    independent_step  6  check_chassis_power_status  DUT  ${ip}  off
    independent_step  7  set_power_status  DUT  on  ${ip}
    independent_step  8  set_wait  5
    independent_step  9  check_chassis_power_status  DUT  ${ip}  on
    independent_step  10  connect  DUT  180  100
    independent_step  11  set_power_status  DUT  reset  ${ip}
    independent_step  12  connect  DUT  180  100
    independent_step  13  check_chassis_power_status  DUT  ${ip}  on
    independent_step  14  OS Disconnect Device
    [Teardown]  Run Keyword If Test Failed  End AC Disconnect


BMC_Power_Control_Test
    # Step 8，9，10 Have been checked in every Step
    [Documentation]  9.5.2 To verify BMC can correctly control the system power to different
                    ...  states: power on, power off, power cycle, reset.
    [Tags]     BMC_Power_Control_Test  Midstone100X  AMI_BMC
    [Setup]     OS Connect Device
    ${ip}  get_ip_address_from_ipmitool  DUT
    independent_step  1  set_power_status  DUT  off
    independent_step  2  set_wait  10
    ${off}  get_chassis_power_status  DUT  ${ip}
    independent_step  3  check_info_equal  ${off}  off
    independent_step  4  set_power_status  DUT  on  ${ip}
    independent_step  5  set_wait  10
    ${on}  get_chassis_power_status  DUT  ${ip}
    independent_step  6  check_info_equal  ${on}  on
    independent_step  7  connect  DUT
    independent_step  8  set_power_status  DUT  cycle  ${ip}
    independent_step  9  check_power_status_bmc  DUT  ${ip}  45
    independent_step  10  connect  DUT  40
    independent_step  11  set_power_status  DUT  reset  ${ip}
    ${on_1}  get_chassis_power_status  DUT  ${ip}
    independent_step  12  check_info_equal  ${on_1}  on
    independent_step  13  connect  DUT  50
    independent_step  14  OS Disconnect Device
    [Teardown]  Run Keyword If Test Failed  End AC Disconnect


SDR_Information_Test
    [Documentation]  9.6.1 To verify the SDR information can be get correctly.
    [Tags]     SDR_Information_Test  Midstone100X  AMI_BMC
    [Setup]     OS Connect Device
    independent_step  1  check_sensor_info  DUT
    independent_step  2  whitebox_lib.execute  DUT  rm -rf ${dut_shell_path}
    [Teardown]  OS Disconnect Device


SEL
    [Documentation]  9.6.3.2 To verify the behavior of SEL sensor should be correct as definition in BMC SPEC and
    [Tags]     SEL  Midstone100X  AMI_BMC
    [Setup]     OS Connect Device
    independent_step  1  set_sel_clear  DUT
    independent_step  2  check_sel_event_data  DUT  1  02
    [Teardown]  OS Disconnect Device


Power_Status
    [Documentation]  9.6.3.4 To verify the behavior of power status sensor should be correct as definition in BMC SPEC
    [Tags]     Power_Status  Midstone100X  AMI_BMC
    [Setup]     OS Connect Device
    ${ip}  get_ip_address_from_ipmitool  DUT
    independent_step  add-1  set_power_status  DUT  off
    independent_step  add-2  set_wait  10
    independent_step  add-3  set_sel_clear  DUT  ${ip}
    independent_step  1  set_power_status  DUT  on  ${ip}
    independent_step  2  connect  DUT  180
    independent_step  3  check_bmc_sel_list_keyword  DUT  S0/G0: working  ip=${ip}
    independent_step  4  check_bmc_sel_list_keyword  DUT  S5/G2: soft-off  False  ${ip}
    independent_step  5  set_sel_clear  DUT  ${ip}
    independent_step  6  set_power_status  DUT  off  ${ip}
    independent_step  7  set_wait  10
    independent_step  8  check_bmc_sel_list_keyword  DUT  S0/G0: working  False  ip=${ip}
    independent_step  9  check_bmc_sel_list_keyword  DUT  S5/G2: soft-off  ip=${ip}
    independent_step  10  set_power_status  DUT  on  ${ip}
    independent_step  11  connect  DUT
    independent_step  12  set_sel_clear  DUT  ${ip}
    independent_step  13  set_power_status  DUT  cycle  ${ip}
    independent_step  14  connect  DUT
    independent_step  15  check_bmc_sel_list_keyword  DUT  S0/G0: working,S5/G2: soft-off  ip=${ip}
    independent_step  16  set_sel_clear  DUT  ${ip}
    independent_step  17  set_power_status  DUT  reset  ${ip}
    independent_step  18  connect  DUT
    # Note:The two sel messages do not exist in Midstone100X reset --by Yagami 2021/8/26
    # independent_step  19  check_bmc_sel_list_keyword  DUT  S0/G0: working,S5/G2: soft-off  ip=${ip}
    independent_step  20  OS Disconnect Device
    [Teardown]  Run Keyword If Test Failed  End AC Disconnect


Watchdog_Timer_Configuration_Test
    [Documentation]  9.10.1  9.10.2  To verify the standardized ‘Watchdog Timer’ functions implemented
                    ...  by BMC, including configuring Watchdog Timer.
    [Tags]     Watchdog_Timer_Configuration_Test  Midstone100X  AMI_BMC
    [Setup]     OS Connect Device
    ${ip}  get_ip_address_from_ipmitool  DUT
    independent_step  add-1  set_reset_type  DUT  ${cmd_ipmitool_mc_reset_cold}  reset_type=cold
    independent_step  1.1  set_sel_clear  DUT
    independent_step  1.2  set_watchdog_timer  DUT  1  0
    independent_step  1.3  check_watchdog_update  DUT  1  0
    independent_step  1.4  set_watchdog_start  DUT
    independent_step  1.5  check_watchdog_counting_down  DUT  1  60  5
    independent_step  1.6  check_bmc_sel_list_keyword  DUT  Hard reset,Power down,soft-off,working  False
    independent_step  1.7  check_bmc_sel_list_keyword  DUT  Watchdog2
    independent_step  2.1  set_sel_clear  DUT
    independent_step  2.2  set_watchdog_timer  DUT  2  1
    independent_step  2.3  check_watchdog_update  DUT  2  1
    independent_step  2.4  set_watchdog_start  DUT
    independent_step  2.5  check_watchdog_counting_down  DUT  1  30  150  ${ip}
    independent_step  2.6  connect  DUT  60
    independent_step  2.7  check_bmc_sel_list_keyword  DUT  Watchdog,Hard reset
    independent_step  3.1  set_sel_clear  DUT
    independent_step  3.2  set_watchdog_timer  DUT  3  2
    independent_step  3.3  check_watchdog_update  DUT  3  2
    independent_step  3.4  set_watchdog_start  DUT
    independent_step  3.5  OS Disconnect Device
    independent_step  3.6  set_wait  20
    independent_step  3.7  set_power_status  DUT  on  ${ip}
    independent_step  3.8  set_wait  180
    independent_step  3.9  OS Connect Device
    independent_step  3.10  check_bmc_sel_list_keyword  DUT  Power down
    independent_step  4.1  set_sel_clear  DUT
    independent_step  4.2  set_watchdog_timer  DUT  4  3
    independent_step  4.3  check_watchdog_update  DUT  4  3
    independent_step  4.4  set_watchdog_start  DUT
    independent_step  4.5  check_watchdog_counting_down  DUT  1  30  150  ${ip}
    independent_step  4.6  connect  DUT  60
    independent_step  4.7  check_bmc_sel_list_keyword  DUT  soft-off,working
    independent_step  5.1  set_sel_clear  DUT
    independent_step  5.2  set_watchdog_timer  DUT  5  3
    independent_step  5.3  check_watchdog_update  DUT  5  3
    independent_step  5.4  set_watchdog_start  DUT
    independent_step  5.5  check_watchdog_counting_down  DUT  1  30  150  ${ip}
    independent_step  5.6  connect  DUT  60
    independent_step  5.7  check_bmc_sel_list_keyword  DUT  soft-off,working
    [Teardown]  OS Disconnect Device


Watchdog_Event_Logging_Test
    [Documentation]  9.10.3 To verify if BMC can log or ignore the watchdog event successfully
    [Tags]     Watchdog_Event_Logging_Test  Midstone100X  AMI_BMC
    [Setup]     OS Connect Device
    ${ip}  get_ip_address_from_ipmitool  DUT
    independent_step  1.1  set_sel_clear  DUT
    independent_step  1.2  set_watchdog_timer  DUT  81  0
    independent_step  1.3  check_watchdog_update  DUT  81  0
    independent_step  1.4  set_watchdog_start  DUT
    independent_step  1.5  check_watchdog_counting_down  DUT  1  30  5  None
    independent_step  1.6  check_bmc_sel_list_keyword  DUT  keyword=Watchdog2,Hard reset,Power down,soft-off,working  decide=False
    independent_step  2.1  set_sel_clear  DUT
    independent_step  2.2  set_watchdog_timer  DUT  82  1
    independent_step  2.3  check_watchdog_update  DUT  82  1
    independent_step  2.4  set_watchdog_start  DUT
    independent_step  2.5  check_watchdog_counting_down  DUT  1  30  150  ${ip}
    independent_step  2.6  check_bmc_sel_list_keyword  DUT  keyword=Watchdog,Hard reset  decide=False
    independent_step  2.7  set_root_hostname  DUT
    independent_step  3.1  set_sel_clear  DUT
    independent_step  3.2  set_watchdog_timer  DUT  83  2
    independent_step  3.3  check_watchdog_update  DUT  83  2
    independent_step  3.4  set_watchdog_start  DUT
    independent_step  3.5  OS Disconnect Device
    independent_step  3.6  set_wait  20
    independent_step  3.7  set_power_status  DUT  on  ${ip}
    independent_step  3.8  set_wait  180
    independent_step  3.9  OS Connect Device
    independent_step  3.10  check_bmc_sel_list_keyword  DUT  keyword=Watchdog,Power down  decide=False
    independent_step  4.1  set_sel_clear  DUT
    independent_step  4.2  set_watchdog_timer  DUT  84  3
    independent_step  4.3  check_watchdog_update  DUT  84  3
    independent_step  4.4  set_watchdog_start  DUT
    independent_step  4.5  check_watchdog_counting_down  DUT  1  30  150  ${ip}
    independent_step  4.6  connect  DUT  60  300
    independent_step  4.7  check_bmc_sel_list_keyword  DUT  keyword=soft-off,working
    independent_step  4.8  check_bmc_sel_list_keyword  DUT  keyword=Watchdog  decide=False
    independent_step  5.1  set_sel_clear  DUT
    independent_step  5.2  set_watchdog_timer  DUT  85  3
    independent_step  5.3  check_watchdog_update  DUT  85  3
    independent_step  5.4  set_watchdog_start  DUT
    independent_step  5.5  check_watchdog_counting_down  DUT  1  30  150  ${ip}
    independent_step  5.6  connect  DUT  60  300
    independent_step  5.7  check_bmc_sel_list_keyword  DUT  keyword=soft-off,working
    independent_step  5.8  check_bmc_sel_list_keyword  DUT  keyword=Watchdog  decide=False
    independent_step  6.1  set_sel_clear  DUT
    independent_step  6.2  set_watchdog_timer  DUT  1  0
    independent_step  6.3  check_watchdog_update  DUT  1  0
    independent_step  6.4  set_watchdog_start  DUT
    independent_step  6.5  check_watchdog_counting_down  DUT  1  30  5  None
    independent_step  6.6  check_bmc_sel_list_keyword  DUT  keyword=Hard reset,Power down,soft-off,working  decide=False
    independent_step  6.7  check_bmc_sel_list_keyword  DUT  keyword=Watchdog2
    independent_step  7.1  set_sel_clear  DUT
    independent_step  7.2  set_watchdog_timer  DUT  2  1
    independent_step  7.3  check_watchdog_update  DUT  2  1
    independent_step  7.4  set_watchdog_start  DUT
    independent_step  7.5  check_watchdog_counting_down  DUT  1  30  150  ${ip}
    independent_step  7.6  connect  DUT  60  300
    independent_step  7.7  check_bmc_sel_list_keyword  DUT  keyword=Watchdog,Hard reset
    independent_step  8.1  set_sel_clear  DUT
    independent_step  8.2  set_watchdog_timer  DUT  3  2
    independent_step  8.3  check_watchdog_update  DUT  3  2
    independent_step  8.4  set_watchdog_start  DUT
    independent_step  8.6  set_wait  20
    independent_step  8.7  set_power_status  DUT  on  ${ip}
    independent_step  8.8  connect  DUT  100  300
    independent_step  8.9  check_bmc_sel_list_keyword  DUT  keyword=Power down
    independent_step  9.1  set_sel_clear  DUT
    independent_step  9.2  set_watchdog_timer  DUT  4  3
    independent_step  9.3  check_watchdog_update  DUT  4  3
    independent_step  9.4  set_watchdog_start  DUT
    independent_step  9.5  check_watchdog_counting_down  DUT  1  30  150  ${ip}
    independent_step  9.6  connect  DUT  100  300
    independent_step  9.7  check_bmc_sel_list_keyword  DUT  keyword=soft-off,working
    independent_step  10.1  set_sel_clear  DUT
    independent_step  10.2  set_watchdog_timer  DUT  5  3
    independent_step  10.3  check_watchdog_update  DUT  5  3
    independent_step  10.4  set_watchdog_start  DUT
    independent_step  10.5  check_watchdog_counting_down  DUT  1  30  150  ${ip}
    independent_step  10.6  connect  DUT  100  300
    independent_step  10.7  check_bmc_sel_list_keyword  DUT  keyword=soft-off,working
    independent_step  11  OS Disconnect Device
    [Teardown]  Run Keyword If Test Failed  End AC Disconnect


SOL_Configuration_Test
    [Documentation]  9.11.1 To verify the SOL configuration data can be set and modified.
    [Tags]     SOL_Configuration_Test  Midstone100X  AMI_BMC
    [Setup]     OS Connect Device
    ${ip}  get_ip_address_from_ipmitool  DUT
    ${Volatile Bit Rate (kbps)_old}  get_sol_config  DUT  Volatile Bit Rate (kbps)  ${ip}
    ${Non-Volatile Bit Rate (kbps)_old}  get_sol_config  DUT  Volatile Bit Rate (kbps)  ${ip}
    log  Volatile Bit Rate (kbps) Default information is ${Volatile Bit Rate (kbps)_old}
    log  Non-Volatile Bit Rate (kbps) Default information is ${Non-Volatile Bit Rate (kbps)_old}
    independent_step  1  set_sol_config_by_ip  DUT  true  ${set_non_volatile}  ${set_volatile_bit}
    ${Volatile Bit Rate (kbps)_new}  get_sol_config  DUT  Volatile Bit Rate (kbps)  ${ip}
    ${Non-Volatile Bit Rate (kbps)_new}  get_sol_config  DUT  Volatile Bit Rate (kbps)  ${ip}
    independent_step  2.1  check_info_equal  ${set_non_volatile}  ${Volatile Bit Rate (kbps)_new}
    independent_step  2.2  check_info_equal  ${set_volatile_bit}  ${Non-Volatile Bit Rate (kbps)_new}
    independent_step  3.1  set_reset_type  DUT  ${cmd_ipmitool_mc_reset_cold}  reset_type=cold
    ${Volatile Bit Rate (kbps)_new_}  get_sol_config  DUT  Volatile Bit Rate (kbps)  ${ip}
    ${Non-Volatile Bit Rate (kbps)_new_}  get_sol_config  DUT  Volatile Bit Rate (kbps)  ${ip}
    independent_step  3.2  check_info_equal  ${set_non_volatile}  ${Volatile Bit Rate (kbps)_new_}
    independent_step  3.3  check_info_equal  ${set_volatile_bit}  ${Non-Volatile Bit Rate (kbps)_new_}
    [Teardown]  OS Disconnect Device


#Online_Update_Test_with_HPM  # Not applicable Midstone 100X
#    [Documentation]  9.1.2  To check the BMC FW programming functions by updating the BMC FW with hpm file.
#    [Tags]     Online_Update_Test_with_HPM  AMI_BMC
#    [Setup]     OS Connect Device
#    ${ip}  get_ip_address_from_ipmitool  DUT
#    independent_step  add_1  set_fw_boot_selector  DUT  1
#    independent_step  add-2  set_reset_type  DUT  ${cmd_ipmitool_mc_reset_cold}  cold  True
#    independent_step  add_3  set_update_bmc_primary_backup  DUT  False  ip=${ip}
#    independent_step  add_4  update_bmc_by_hpm  DUT  now  ip=${ip}
#    independent_step  add_5  set_wait  180
#    independent_step  add_6  set_update_bmc_primary_backup  DUT  ip=${ip}
#    independent_step  add_7  update_bmc_by_hpm  DUT  now  ip=${ip}
#    independent_step  add_8  set_wait  180
#    independent_step  1  set_sel_disabled  DUT  ${ip}
#    ${info_old}  get_mc_info  DUT  ${ip}
#    ${version_pr_old}  get_bmc_version  DUT  ip=${ip}
#    ${version_bk_old}  get_bmc_version  DUT  False  ip=${ip}
#    independent_step  2  set_sel_clear  DUT  ${ip}
#    independent_step  3  set_update_bmc_primary_backup  DUT  ip=${ip}
#    independent_step  4  update_bmc_by_hpm  DUT  old  ip=${ip}
#    independent_step  5  set_wait  180
#    ${version_pr_new}  get_bmc_version  DUT  ip=${ip}
#    independent_step  6.1  check_info_equal  ${version_pr_old}  ${version_pr_new}  False
#    ${version_bk}  get_bmc_version  DUT  False  ip=${ip}
#    independent_step  6.2  check_info_equal  ${version_bk_old}  ${version_bk}
#    independent_step  6.3  check_bmc_sel_list_keyword  DUT  S0/G0: working  decide=True  ip=${ip}
#    independent_step  6.4  check_bmc_sel_list_keyword  DUT  Log area reset/cleared  False  ip=${ip}
#    independent_step  6.5  set_sel_clear  DUT  ${ip}
#    independent_step  7  set_update_bmc_primary_backup  DUT  False  ip=${ip}
#    independent_step  8  update_bmc_by_hpm  DUT  old  ip=${ip}
#    independent_step  9  set_wait  180
#    ${version_bk_new}  get_bmc_version  DUT  ip=${ip}
#    independent_step  10.1  check_info_equal  ${version_bk_new}  ${version_bk_old}  False
#    independent_step  10.2  check_bmc_sel_list_keyword  DUT  S0/G0: working  decide=True  ip=${ip}
#    independent_step  10.3  check_bmc_sel_list_keyword  DUT  Log area reset/cleared  decide=True  ip=${ip}
#    independent_step  11  OS Disconnect Device
#    [Teardown]  Run Keyword If Test Failed  End Online Update Test with HPM


BMC_Channel_Check
    [Documentation]  9.3  To verify the BMC channel info is correct and can work normally.
    [Tags]     BMC_Channel_Check  Midstone100X  AMI_BMC
    [Setup]     OS Connect Device
    ${ip}  get_ip_address_from_ipmitool  DUT
    independent_step  1.1  check_bmc_channel_medium_type  DUT  6  medium=${channel_6_medium_type}
    independent_step  1.2  check_ipmb_device  DUT
    independent_step  2.1  check_bmc_channel_medium_type  DUT  1  medium=${channel_1_medium_type}
    # Midstone 100X No 'channel 8'
    # independent_step  2.2  check_bmc_channel_medium_type  DUT  8  medium=${channel_8_medium_type}
    independent_step  3  check_communication_lan_pc  DUT  ${ip}
    independent_step  4  check_bmc_channel_medium_type  DUT  15  protocol=${channel_f_medium_type}
    [Teardown]  OS Disconnect Device


BMC_Firmware_Boot_Up
    [Documentation]  9.6.3.5  To verify the behavior of BMC firmware boot up sensor should be
                    ...  correct as definition in BMC SPEC
    [Tags]     BMC_Firmware_Boot_Up  Midstone100X  AMI_BMC
    [Setup]     OS Connect Device
    ${ip}  get_ip_address_from_ipmitool  DUT
    independent_step  add-1  set_fw_boot_selector  DUT  1  ${ip}
    independent_step  add-2  set_reset_type  DUT  ${cmd_ipmitool_mc_reset_cold}  cold  True
    independent_step  add-3  check_current_active_image  DUT  01  ${ip}
    independent_step  1  set_reset_type  DUT  ${cmd_ipmitool_mc_reset_warm}  warm  True
    independent_step  2  check_sel_info_only_clear  DUT  True  ${ip}
    independent_step  3.1  check_fw_boot_selector  DUT  01  ${ip}
    independent_step  3.2  check_current_active_image  DUT  01  ${ip}
    independent_step  4.1  set_reset_type  DUT  ${cmd_ipmitool_mc_reset_cold}  cold  True
    independent_step  4.2  check_sel_event_data  DUT  2  00  True  ${ip}
    independent_step  5.1  set_fw_boot_selector  DUT  2  ${ip}
    independent_step  5.2  set_reset_type  DUT  ${cmd_ipmitool_mc_reset_cold}  cold  True
    independent_step  6  check_sel_event_data  DUT  2  00  True  ${ip}
    independent_step  6  check_current_active_image  DUT  02  ${ip}
    independent_step  7.1  set_fw_boot_selector  DUT  1  ${ip}
    independent_step  7.2  set_reset_type  DUT  ${cmd_ipmitool_mc_reset_cold}  cold  True
    independent_step  7.3  check_sel_event_data  DUT  2  00  True  ${ip}
    independent_step  8  check_current_active_image  DUT  01  ${ip}
    independent_step  9  OS Disconnect Device
    [Teardown]  Run Keyword If Test Failed  End BMC Firmware Boot Up


Set_Get_GPIO
    [Documentation]  9.13.4  To verify if the OEM command can set/get GPIO dir/value successfully.
    [Tags]     Set_Get_GPIO  Midstone100X  AMI_BMC
    [Setup]     OS Connect Device
    independent_step  1  set_get_gpio  DUT
    [Teardown]  OS Disconnect Device


#Switch_BIOS_Chip_Selector  # Note: Midstone100X Mismatch
#    [Documentation]  9.13.8  This command is used to get/set BIOS firmware boot selector
#    [Tags]     Switch_BIOS_Chip_Selector  AMI_BMC
#    [Setup]     OS Connect Device
    # Because the default value will be changed to unexpected due to the setting,
    # discussing with Auggie Chen, cancel the default value check of the biso firmware
#    independent_step  3  check_cmd_response  DUT  ${cmd_check_bios_boot_selector}  00
#    independent_step  4  check_cmd_response  DUT  ${cmd_get_bios_status}  01
#    independent_step  5  check_cmd_response  DUT  ${cmd_me_to_recovery}  57 01 00
#    independent_step  6  check_cmd_response  DUT  ${cmd_get_device_id_me}  .*00
#    independent_step  7.1  set_start_bios_primary_backup  DUT  False
#    independent_step  7.2  set_power_status  DUT  cycle  connection=True
#    independent_step  8.1  check_cmd_response  DUT  ${cmd_check_bios_default_fw}  04
#    independent_step  8.2  check_cmd_response  DUT  ${cmd_check_bios_boot_selector}  01
#    independent_step  8.3  check_cmd_response  DUT  ${cmd_get_bios_status}  01
#    independent_step  9  whitebox_lib.execute  DUT  ${cmd_me_to_operational}
#    independent_step  10.1  set_power_status  DUT  cycle
#    independent_step  10.2  set_wait  240
#    independent_step  11.1  check_cmd_response  DUT  ${cmd_verify_error_1}  Request data length invalid
#    independent_step  11.2  check_cmd_response  DUT  ${cmd_verify_error_2}  Request data length invalid
#    independent_step  11.3  check_cmd_response  DUT  ${cmd_verify_error_3}  Unable to send RAW command
#    independent_step  12  OS Disconnect Device
#    [Teardown]  Run Keyword If Test Failed  End Switch BIOS Chip Selector


#Read_Write_CPLD_Register  # Note: Midstone100X Mismatch
#    [Documentation]  9.13.9  To verify if the OEM command read/write CPLD register
#    [Tags]     Read_Write_CPLD_Register  AMI_BMC
#    [Setup]     OS Connect Device
#    ${ip}  get_ip_address_from_ipmitool  DUT
#    independent_step  1  check_cmd_response  DUT  ${cmd_get_cpld_version}  01
#    independent_step  2.1  check_cmd_response  DUT  ${cmd_get_cpld_sw_scratch_register_1}  de
#    independent_step  2.2  check_cmd_response  DUT  ${cmd_get_cpld_sw_scratch_register_2}  12
#    independent_step  2.3  check_cmd_response  DUT  ${cmd_get_cpld_sw_scratch_register_3}  25
#    independent_step  3.1  whitebox_lib.execute  DUT  ${cmd_write_baseboarad_cpld_sw_scratch}
#    independent_step  3.2  check_cmd_response  DUT  ${cmd_get_cpld_sw_scratch_register_1}  ff
#    independent_step  5.1  check_cmd_response  DUT  ${cmd_cpld_verify_error_1}  Request data length
#    independent_step  5.2  check_cmd_response  DUT  ${cmd_cpld_verify_error_2}  Request data length
#    independent_step  4.1  set_power_status  DUT  off
#    independent_step  4.2  set_wait  30
#    independent_step  4.3  check_chassis_power_status  DUT  ${ip}  off
#    independent_step  4.4  check_cmd_response  DUT  ${cmd_get_cpld_version}  01  ip=${ip}
#    independent_step  4.5  check_cmd_response  DUT  ${cmd_get_cpld_sw_scratch_register_1}  ff  ip=${ip}
#    independent_step  4.6  check_cmd_response  DUT  ${cmd_get_cpld_sw_scratch_register_2}  12  ip=${ip}
#    independent_step  4.7  check_cmd_response  DUT  ${cmd_get_cpld_sw_scratch_register_3}  25  ip=${ip}
#    independent_step  4.8  send_cmd  DUT  ${cmd_write_baseboarad_cpld_sw_scratch_default}  ${ip}
#    independent_step  4.9  check_cmd_response  DUT  ${cmd_get_cpld_sw_scratch_register_1}  de  ip=${ip}
#    independent_step  4.10  check_cmd_response  DUT  ${cmd_cpld_verify_error_1}  Request data length  ip=${ip}
#    independent_step  4.11  check_cmd_response  DUT  ${cmd_cpld_verify_error_2}  Request data length  ip=${ip}
#    independent_step  5  OS Disconnect Device
#    [Teardown]  Run Keyword If Test Failed  End AC Disconnect


Online_Update_Test_via_USB
    [Documentation]  11.1.2  To check the BMC FW programming functions by updating the BMC FW with CFUflash in Linux OS.
    [Tags]     Online_Update_Test_via_USB  AMI_B
    [Setup]     OS Connect Device
    ${ip}  get_ip_address_from_ipmitool  DUT
    independent_step  add_1  set_fw_boot_selector  DUT  2
    independent_step  add-2  set_reset_type  DUT  ${cmd_ipmitool_mc_reset_cold}  cold  True
    independent_step  add-3  set_bmc_virtual_usb_device  DUT
    independent_step  add-4  update_by_cfu  DUT  bmc  False  now
    independent_step  add_5  set_fw_boot_selector  DUT  1
    independent_step  add_6  set_reset_type  DUT  ${cmd_ipmitool_mc_reset_cold}  cold  True
    independent_step  add_7  update_by_cfu  DUT  bmc  True  now
    independent_step  1  run update bmc by cfu to lower primary usb
    independent_step  2  run update bmc by cfu to high primary usb
    independent_step  3  set_fw_boot_selector  DUT  2
    independent_step  4  set_reset_type  DUT  ${cmd_ipmitool_mc_reset_cold}  cold  True
    ${ip}  get_ip_address_from_ipmitool  DUT
    independent_step  5  set_update_bmc_primary_backup  DUT  False  ip=${ip}
    independent_step  6  run update bmc by cfu to lower backup usb
    independent_step  7  run update bmc by cfu to high backup usb
    independent_step  8  OS Disconnect Device
    [Teardown]  Run Keyword If Test Failed  End Bmc Online Update Test


Online_Update_Test_via_LAN
    [Documentation]  11.1.3  To check the BMC FW programming functions by updating the BMC FW with CFUflash
                    ...  in via LAN in both Windows and Linux OS.
    [Tags]     Online_Update_Test_via_LAN  Midstone100X  AMI_BMC
    [Setup]     OS Connect Device
    ${ip}  get_ip_address_from_ipmitool  DUT
    independent_step  add_1  set_fw_boot_selector  DUT  2  ${ip}
    independent_step  add-2  set_reset_type  DUT  ${cmd_ipmitool_mc_reset_cold}  cold  True
    ${ip}  get_ip_address_from_ipmitool  DUT
    independent_step  add-3  set_bmc_virtual_usb_device  DUT  ip=${ip}
    independent_step  add_4  update_by_cfu  DUT  bmc  False  now  bmc_ip=${ip}
    independent_step  PDU_Reboot_1  set_pdu_status_connect_os  DUT  reboot  ${pdu_port}  600  10
    ${ip}  get_ip_address_from_ipmitool  DUT
    independent_step  add_6  set_fw_boot_selector  DUT  1  ${ip}
    independent_step  add_7  set_reset_type  DUT  ${cmd_ipmitool_mc_reset_cold}  cold  True
    ${ip}  get_ip_address_from_ipmitool  DUT
    independent_step  add_8  update_by_cfu  DUT  bmc  True  now  bmc_ip=${ip}
    independent_step  PDU_Reboot_2  set_pdu_status_connect_os  DUT  reboot  ${pdu_port}  600  10
    independent_step  1  run update bmc by cfu to lower primary lan
    ${ip}  get_ip_address_from_ipmitool  DUT
    independent_step  2  run update bmc by cfu to high primary lan
    ${ip}  get_ip_address_from_ipmitool  DUT
    independent_step  3  set_fw_boot_selector  DUT  2  ${ip}
    independent_step  4  set_reset_type  DUT  ${cmd_ipmitool_mc_reset_cold}  cold  True
    independent_step  5  set_update_bmc_primary_backup  DUT  False  ip=${ip}
    independent_step  6  run update bmc by cfu to lower backup lan
    independent_step  7  run update bmc by cfu to high backup lan
    independent_step  8  set_fw_boot_selector  DUT  1  ${ip}
    independent_step  9  set_reset_type  DUT  ${cmd_ipmitool_mc_reset_cold}  cold  True
    independent_step  10  OS Disconnect Device
    [Teardown]  Run Keyword If Test Failed  End Bmc Online Update Test


CPLD_Update_Test
    [Documentation]  11.13.3.1  To verify if BMC can online update baseboard CPLD successfully.
    [Tags]     CPLD_Update_Test  AMI_BMC  Midstone100X
    [Setup]     OS Connect Device
    independent_step  add-1  set_pdu_status_connect_os  DUT  reboot  ${pdu_port}  600  60
    independent_step  add-2  get_mc_info  DUT
    ${ip}  get_ip_address_from_ipmitool  DUT
    independent_step  1  set_bmc_virtual_usb_device  DUT
    independent_step  2  update_by_cfu  DUT  cpld  version=old  update_time=1200
    independent_step  3  set_wait  60
    ${cpld_version_ac_lower}  get_cpld_version_power_ac  DUT  ${pdu_port}
    independent_step  4  set_root_hostname  DUT
    ${all_cpld_version_lower}  get_cpld_version_in_os  DUT
    independent_step  5  check_info_equal  ${all_cpld_version_lower}  ${cpld_os_version_1_2_lower}
    independent_step  6  check_info_equal  ${cpld_version_ac_lower}  ${cpld_ac_version_baseboard_come_lower}
    independent_step  7  set_bmc_virtual_usb_device  DUT  False
    independent_step  8  set_bmc_virtual_usb_device  DUT
    independent_step  9  update_by_cfu  DUT  cpld  version=now  update_time=1200
    independent_step  10  set_wait  60
    ${cpld_version_ac_high}  get_cpld_version_power_ac  DUT  ${pdu_port}
    independent_step  11  set_root_hostname  DUT
    ${all_cpld_version_high}  get_cpld_version_in_os  DUT
    independent_step  12  check_info_equal  ${all_cpld_version_high}  ${cpld_os_version_1_2_high}
    independent_step  13  check_info_equal  ${cpld_version_ac_high}  ${cpld_ac_version_baseboard_come_high}
    independent_step  14  set_bmc_virtual_usb_device  DUT  False
    independent_step  15  set_bmc_virtual_usb_device  DUT  ip=${ip}
    independent_step  16  update_by_cfu  DUT  cpld  version=old  update_time=1200  bmc_ip=${ip}
    independent_step  17  set_wait  60
    ${cpld_version_ac_lower_lan}  get_cpld_version_power_ac  DUT  ${pdu_port}
    independent_step  18  set_root_hostname  DUT
    ${all_cpld_version_lower_lan}  get_cpld_version_in_os  DUT
    independent_step  19  check_info_equal  ${all_cpld_version_lower_lan}  ${cpld_os_version_1_2_lower}
    independent_step  20  check_info_equal  ${cpld_version_ac_lower_lan}  ${cpld_ac_version_baseboard_come_lower}
    independent_step  21  set_bmc_virtual_usb_device  DUT  ip=${ip}
    independent_step  22  update_by_cfu  DUT  cpld  version=now  update_time=1200  bmc_ip=${ip}
    independent_step  21  set_wait  60
    ${cpld_version_ac_high_lan}  get_cpld_version_power_ac  DUT  ${pdu_port}
    independent_step  22  set_root_hostname  DUT
    ${all_cpld_version_high_lan}  get_cpld_version_in_os  DUT
    independent_step  23  check_info_equal  ${all_cpld_version_high_lan}  ${cpld_os_version_1_2_high}
    independent_step  24  check_info_equal  ${cpld_version_ac_high_lan}  ${cpld_ac_version_baseboard_come_high}
    independent_step  25  OS Disconnect Device
    [Teardown]  Run Keyword If Test Failed  End CPLD Update Test


BIOS_Update_Test_via_USB
    [Documentation]  11.13.5.2  To verify BIOS can be online updated successfully via BMC USB method.
    [Tags]     BIOS_Update_Test_via_USB  AMI_BMC  Midstone100X
    [Setup]     OS Connect Device
    independent_step  add-1  set_bmc_virtual_usb_device  DUT
    independent_step  1.1  set_start_bios_primary_backup  DUT
    independent_step  1.2  set_power_status  DUT  cycle  connection=True
    independent_step  2.2  set_sel_clear  DUT
    ${dmi_info_1}  get_dmidecode_info  DUT
    independent_step  3.1  update_by_cfu  DUT  bios  version=old  update_time=600
    independent_step  3.2  check_sel_info_only_clear  DUT
    independent_step  3.3  check_bios_info_power_cycle  DUT  ${bios_version_old}  primary
    independent_step  3.4  whitebox_exit_bios_setup  DUT  False
    ${dmi_info_2}  get_dmidecode_info  DUT
    independent_step  3.5  check_dmidecode_info_equal  ${dmi_info_1}  ${dmi_info_2}
    independent_step  3.6  check_reset_sel_info  DUT  restart_method=reboot
    independent_step  4.1  set_start_bios_primary_backup  DUT
    independent_step  4.2  set_power_status  DUT  cycle  connection=True
    independent_step  5  set_sel_clear  DUT
    ${dmi_info_3}  get_dmidecode_info  DUT
    independent_step  6.1  update_by_cfu  DUT  bios  version=now  update_time=600
    independent_step  6.2  check_sel_info_only_clear  DUT
    independent_step  6.3  check_bios_info_power_cycle  DUT  ${bios_version_now}  primary
    independent_step  6.4  whitebox_exit_bios_setup  DUT  False
    ${dmi_info_4}  get_dmidecode_info  DUT
    independent_step  6.5  check_dmidecode_info_equal  ${dmi_info_3}  ${dmi_info_4}
    independent_step  6.6  check_reset_sel_info  DUT  restart_method=reboot
    independent_step  7.1  set_start_bios_primary_backup  DUT  False
    independent_step  7.2  set_boot_option_1  DUT
    independent_step  8  set_sel_clear  DUT
    ${dmi_info_1_1}  get_dmidecode_info  DUT
    independent_step  9.1  update_by_cfu  DUT  bios  version=old  update_time=600
    independent_step  9.2  check_sel_info_only_clear  DUT
    independent_step  9.3  set_start_bios_primary_backup  DUT  False
    independent_step  9.4  check_bios_info_power_cycle  DUT  ${bios_version_old}  backup
    independent_step  9.5  whitebox_exit_bios_setup  DUT  False
    ${dmi_info_2_1}  get_dmidecode_info  DUT
    independent_step  9.6  check_dmidecode_info_equal  ${dmi_info_1_1}  ${dmi_info_2_1}
    independent_step  9.7  check_reset_sel_info  DUT  restart_method=reboot
    independent_step  10.1  set_start_bios_primary_backup  DUT  False
    independent_step  10.2  set_boot_option_1  DUT
    independent_step  11  set_sel_clear  DUT
    ${dmi_info_3_1}  get_dmidecode_info  DUT
    independent_step  12.1  update_by_cfu  DUT  bios  version=now  update_time=600
    independent_step  12.2  check_sel_info_only_clear  DUT
    independent_step  12.3  set_start_bios_primary_backup  DUT  False
    independent_step  12.4  check_bios_info_power_cycle  DUT  ${bios_version_now}  backup
    independent_step  12.5  whitebox_exit_bios_setup  DUT  False
    ${dmi_info_4_1}  get_dmidecode_info  DUT
    independent_step  12.6  check_dmidecode_info_equal  ${dmi_info_3_1}  ${dmi_info_4_1}
    independent_step  12.7  check_reset_sel_info  DUT  restart_method=reboot
    independent_step  13  set_start_bios_primary_backup  DUT
    independent_step  14  set_power_status  DUT  cycle  connection=True
    independent_step  15  OS Disconnect Device
    [Teardown]  Run Keyword If Test Failed  End BIOS Update Test


BIOS_Update_Test_via_LAN
    [Documentation]  11.13.5.1  To verify BIOS can be online updated successfully via BMC LAN method.
    [Tags]     BIOS_Update_Test_via_LAN  AMI_BMC
    [Setup]     OS Connect Device
    ${ip}  get_ip_address_from_ipmitool  DUT
    independent_step  1  set_start_bios_primary_backup  DUT  False  ${ip}
    independent_step  2  set_wait  5
    independent_step  3  set_power_status  DUT  cycle  ${ip}  True
    independent_step  4  check_cmd_response  DUT  ${cmd_get_bios_start_from_primary_backup}  03
    independent_step  5  update_by_cfu  DUT  bios  False  now  1200  ${ip}
    ${eth0_1_old}  get_ether_from_ifconfig  DUT  eth0
    ${dmi_1_old}  get_dmidecode_info  DUT
    independent_step  6  set_sel_clear  DUT  ${ip}
    ${backup_old_name}  update_by_cfu  DUT  bios  False  old  1200  ${ip}  True
    independent_step  7  set_start_bios_primary_backup  DUT  False  ${ip}
    independent_step  8  set_wait  5
    independent_step  9  check_bios_info_power_cycle  DUT  ${backup_old_name}  backup  ${ip}
    independent_step  10  whitebox_exit_bios_setup  DUT  False
    independent_step  10.1  set_root_hostname  DUT
    independent_step  10.2  check_reset_sel_info  DUT  ${ip}  reboot
    independent_step  11  check_cmd_response  DUT  ${cmd_get_bios_start_from_primary_backup}  03
    independent_step  12  check_cmd_response  DUT  dmidecode -t0  ${backup_old_name}
    ${sel_list_1}  get_sel_list  DUT  ${ip}  True
    ${eth0_2_old}  get_ether_from_ifconfig  DUT  eth0
    ${dmi_2_old}  get_dmidecode_info  DUT
    independent_step  13  check_dmidecode_info_equal  ${dmi_2_old}  ${dmi_1_old}
    independent_step  14  check_dmidecode_info_equal  ${eth0_2_old}  ${eth0_1_old}

    independent_step  15  set_sel_clear  DUT  ${ip}
    ${backup_new_name}  update_by_cfu  DUT  bios  False  now  1200  ${ip}  True
    independent_step  16  set_start_bios_primary_backup  DUT  False  ${ip}
    independent_step  17  set_wait  5
    independent_step  18  check_bios_info_power_cycle  DUT  ${backup_new_name}  backup  ${ip}
    independent_step  19  whitebox_exit_bios_setup  DUT  False
    independent_step  19.1  set_root_hostname  DUT
    independent_step  19.2  check_reset_sel_info  DUT  ${ip}  reboot
    independent_step  20  check_cmd_response  DUT  ${cmd_get_bios_start_from_primary_backup}  03
    independent_step  21  check_cmd_response  DUT  dmidecode -t0  ${backup_new_name}
    ${sel_list_2}  get_sel_list  DUT  ${ip}  True
    ${eth0_3_new}  get_ether_from_ifconfig  DUT  eth0
    ${dmi_3_new}  get_dmidecode_info  DUT
    independent_step  22  check_dmidecode_info_equal  ${dmi_3_new}  ${dmi_2_old}
    independent_step  23  check_dmidecode_info_equal  ${eth0_3_new}  ${eth0_2_old}

    independent_step  24  set_sel_clear  DUT  ${ip}
    ${primary_old_name}  update_by_cfu  DUT  bios  True  old  1200  ${ip}  True
    independent_step  25  set_start_bios_primary_backup  DUT  True  ${ip}
    independent_step  26  set_wait  5
    independent_step  27  check_bios_info_power_cycle  DUT  ${primary_old_name}  primary  ${ip}
    independent_step  28  whitebox_exit_bios_setup  DUT  False
    independent_step  28.1  set_root_hostname  DUT
    independent_step  28.2  check_reset_sel_info  DUT  ${ip}  reboot
    independent_step  29  check_cmd_response  DUT  ${cmd_get_bios_start_from_primary_backup}  01
    independent_step  30  check_cmd_response  DUT  dmidecode -t0  ${primary_old_name}
    ${sel_list_3}  get_sel_list  DUT  ${ip}  True
    ${eth0_4_old}  get_ether_from_ifconfig  DUT  eth0
    ${dmi_4_old}  get_dmidecode_info  DUT
    independent_step  31  check_dmidecode_info_equal  ${dmi_4_old}  ${dmi_3_new}
    independent_step  32  check_dmidecode_info_equal  ${eth0_4_old}  ${eth0_3_new}

    independent_step  33  set_sel_clear  DUT  ${ip}
    ${primary_new_name}  update_by_cfu  DUT  bios  True  now  1200  ${ip}  True
    independent_step  34  set_start_bios_primary_backup  DUT  True  ${ip}
    independent_step  35  set_wait  5
    independent_step  36  check_bios_info_power_cycle  DUT  ${primary_new_name}  primary  ${ip}
    independent_step  37  whitebox_exit_bios_setup  DUT  False
    independent_step  37.1  set_root_hostname  DUT
    independent_step  37.2  check_reset_sel_info  DUT  ${ip}  reboot
    independent_step  38  check_cmd_response  DUT  ${cmd_get_bios_start_from_primary_backup}  01
    independent_step  39  check_cmd_response  DUT  dmidecode -t0  ${primary_new_name}
    ${sel_list_4}  get_sel_list  DUT  ${ip}  True
    ${eth0_5_new}  get_ether_from_ifconfig  DUT  eth0
    ${dmi_5_new}  get_dmidecode_info  DUT
    independent_step  40  check_dmidecode_info_equal  ${dmi_5_new}  ${dmi_4_old}
    independent_step  41  check_dmidecode_info_equal  ${eth0_5_new}  ${eth0_4_old}
    independent_step  42  OS Disconnect Device
    [Teardown]  Run Keyword If Test Failed
    ...  Run Keywords
    ...  OS Connect Device  AND
    ...  set_pdu_status_connect_os  DUT  reboot  ${pdu_port}  600  100  AND
    ...  connect  DUT  AND
    ...  ${ip}  get_ip_address_from_ipmitool  DUT  AND
    ...  update_by_cfu  DUT  bios  True  now  1200  ${ip}  AND
    ...  update_by_cfu  DUT  bios  False  now  1200  ${ip}  AND
    ...  set_start_bios_primary_backup  DUT  True  ${ip}  AND
    ...  set_pdu_status_connect_os  DUT  reboot  ${pdu_port}  600  100  AND
    ...  OS Disconnect Device


PEF_Configuration_Test
    [Documentation]  9.8.1  To verify the PEF related information can be set can get correctly.
    [Tags]     PEF_Configuration_Test  Midstone100X  AMI_BMC
    [Setup]     OS Connect Device
    ${ip}  get_ip_address_from_ipmitool  DUT
    independent_step  1  send_cmd  DUT  ${cmd_Get_PEF_Capabilities}
    independent_step  2.1  send_cmd  DUT  ${ssl_cmd_Set_PEF_Capabilities_1}
    independent_step  2.2  send_cmd  DUT  ${ssl_cmd_Set_PEF_Capabilities_2}
    independent_step  2.3  send_cmd  DUT  ${ssl_cmd_Set_PEF_Capabilities_3}
    independent_step  2.4  send_cmd  DUT  ${ssl_cmd_Set_PEF_Capabilities_4}
    independent_step  2.5  send_cmd  DUT  ${ssl_cmd_Set_PEF_Capabilities_5}
    independent_step  3.1  send_cmd  DUT  ${ssl_cmd_Set_PEF_Capabilities_6}
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
        Run Keyword If  '${index}' == '1'  set_reset_type  DUT  ${cmd_ipmitool_mc_reset_cold}  cold  True
    END
    log  PEF by lan
    independent_step  lan1  send_cmd  DUT  ${cmd_Get_PEF_Capabilities}  ip=${ip}
    independent_step  2.1  send_cmd  DUT  ${ssl_cmd_Set_PEF_Capabilities_1}  ip=${ip}
    independent_step  2.2  send_cmd  DUT  ${ssl_cmd_Set_PEF_Capabilities_2}  ip=${ip}
    independent_step  2.3  send_cmd  DUT  ${ssl_cmd_Set_PEF_Capabilities_3}  ip=${ip}
    independent_step  2.4  send_cmd  DUT  ${ssl_cmd_Set_PEF_Capabilities_4}  ip=${ip}
    independent_step  2.5  send_cmd  DUT  ${ssl_cmd_Set_PEF_Capabilities_5}  ip=${ip}
    independent_step  3.1  send_cmd  DUT  ${ssl_cmd_Set_PEF_Capabilities_6}  ip=${ip}
    FOR  ${index}  IN RANGE  1  3
        independent_step  3.2  check_cmd_response  DUT  ${ssl_cmd_Get_PEF_Configuration_Parameters_1}
                ...  ${ssl_rsp_Get_PEF_Configuration_Parameters_1}  ip=${ip}
        independent_step  3.3  check_cmd_response  DUT  ${ssl_cmd_Get_PEF_Configuration_Parameters_2}
                ...  ${ssl_rsp_Get_PEF_Configuration_Parameters_2}  ip=${ip}
        independent_step  3.4  check_cmd_response  DUT  ${ssl_cmd_Get_PEF_Configuration_Parameters_3}
                ...  ${ssl_rsp_Get_PEF_Configuration_Parameters_3}  ip=${ip}
        independent_step  3.5  check_cmd_response  DUT  ${ssl_cmd_Get_PEF_Configuration_Parameters_4}
                ...  ${ssl_rsp_Get_PEF_Configuration_Parameters_4}  ip=${ip}  re_S=True
        independent_step  3.6  check_cmd_response  DUT  ${ssl_cmd_Get_PEF_Configuration_Parameters_5}
                ...  ${ssl_rsp_Get_PEF_Configuration_Parameters_5}  ip=${ip}
        Run Keyword If  '${index}' == '1'  set_reset_type  DUT  ${cmd_ipmitool_mc_reset_cold}  cold  True
    END
    independent_step  4  OS Disconnect Device
    [Teardown]  End PEF Configuration Test


FRU_Access_Test
    [Documentation]  9.12.1  To verify if the FRU information can be accessed successfully via IPMI command.
    [Tags]     FRU_Access_Test  Midstone100X  AMI_BMC
    [Setup]     OS Connect Device
    ${serial_old}  get_fru_info  DUT  6  Board Serial
    FOR  ${index}  IN RANGE  0  10
        independent_step  1  check_cmd_response  DUT  ${cmd_get_fru_inventory_area}${index}  ${rsp_get_fru_inventory_area}
    END
    independent_step  2  check_read_fru_data  DUT
    independent_step  3  send_cmd_without_return_rule  DUT  ${cmd_set_fru_protection_disable}
    independent_step  4  check_cmd_response  DUT  ${cmd_write_fru_for_r_w_frus_1}  ${res_write_fru_for_r_w_frus}
    independent_step  5  check_cmd_response  DUT  ${cmd_check_fru_date}  ${res_check_fru_date_1}
    independent_step  6  check_cmd_response  DUT  ${cmd_write_fru_for_r_w_frus_2}  ${res_write_fru_for_r_w_frus}
    independent_step  7  check_cmd_response  DUT  ${cmd_check_fru_date}  ${res_check_fru_date_2}
    independent_step  8  check_cmd_response  DUT  ${restore_fru6_info}  ${res_write_fru_for_r_w_frus}
    ${serial_new}  get_fru_info  DUT  6  Board Serial
    ${all_fru_old}  get_fru_info  DUT  ${empty_str}
    independent_step  8  set_pdu_status_connect_os  DUT  reboot  ${pdu_port}  600  70
    ${all_fru_new}  get_fru_info  DUT  ${empty_str}
    independent_step  9  check_info_equal  ${all_fru_old}  ${all_fru_new}
    independent_step  10  send_cmd_without_return_rule  DUT  ${cmd_set_fru_protection_enable}
    [Teardown]     OS Disconnect Device


Extensional_I2C_Master_Write_Read
    [Documentation]  9.13.1  To verify the OEM command can read/write I2C devices with any bus id.
    [Tags]     Extensional_I2C_Master_Write_Read  AMI_BMC  Midstone100X
    [Setup]     OS Connect Device
    ${ip}  get_ip_address_from_ipmitool  DUT
    independent_step  1  send_cmd_without_return_rule  DUT  ${cmd_get_and_set_fru_write_protect_status} 6 0
    independent_step  2  check_cmd_response  DUT  ${cmd_get_baseboard_cpld}  ${response_baseboard_cpld_version}
    independent_step  3  check_cmd_response  DUT  ${cmd_get_cpld_sw_scratch_default}  ${response_cpld_sw_scratch_default}
    independent_step  4  check_psu_data  DUT  ${cmd_get_right_psu_data}  ff
    independent_step  5  check_psu_data  DUT  ${cmd_get_lift_psu_data}  ff
    ${fru_1}  read_fan_fru  DUT  ${cmd_switch_to_fan_1}
    ${fru_2}  read_fan_fru  DUT  ${cmd_switch_to_fan_2}
    ${fru_3}  read_fan_fru  DUT  ${cmd_switch_to_fan_3}
    ${fru_4}  read_fan_fru  DUT  ${cmd_switch_to_fan_4}
    independent_step  6  send_cmd_without_return_rule  DUT  ${cmd_switch_to_fan_write}
    independent_step  7  send_cmd_without_return_rule  DUT  ${cmd_write_fru_info_to_fan1}
    ${fru_1_now}  read_fan_fru  DUT  ${cmd_switch_to_fan_1}  return_str=True
    independent_step  8  check_keyword_in_info  ${fru_1_now}  ${check_write_response}
    independent_step  9  send_cmd_without_return_rule  DUT  ${cmd_switch_to_fan_write}
    independent_step  10  send_cmd_without_return_rule  DUT  ipmitool raw 0x3a 0x3e 0x08 0xA0 0x00 0x00 0x00 ${fru_1}
    independent_step  11  set_wait  10
    independent_step  12  set_power_status  DUT  off
    independent_step  13  set_wait  20
    ${fru_1_bmc}  read_fan_fru  DUT  ${cmd_switch_to_fan_1}  bmc=Ture
    ${fru_2_bmc}  read_fan_fru  DUT  ${cmd_switch_to_fan_2}  bmc=Ture
    ${fru_3_bmc}  read_fan_fru  DUT  ${cmd_switch_to_fan_3}  bmc=Ture
    ${fru_4_bmc}  read_fan_fru  DUT  ${cmd_switch_to_fan_4}  bmc=Ture
    independent_step  14  check_info_equal  ${fru_1_bmc}  ${fru_1}
    independent_step  15  check_info_equal  ${fru_1_bmc}  ${fru_2}
    independent_step  16  check_info_equal  ${fru_1_bmc}  ${fru_3}
    independent_step  17  check_info_equal  ${fru_1_bmc}  ${fru_4}
    independent_step  18  set_power_status  DUT  on  ${ip}  True
    independent_step  19  send_cmd_without_return_rule  DUT  ${cmd_get_and_set_fru_write_protect_status} 6 0
    independent_step  20  OS Disconnect Device
    [Teardown]  Run Keyword If Test Failed
    ...  Run Keywords
    ...  OS Connect Device  AND
    ...  set_pdu_status_connect_os  DUT  reboot  ${pdu_port}  600  100  AND
    ...  independent_step  add  send_cmd_without_return_rule  DUT  ${cmd_get_and_set_fru_write_protect_status} 6 0  AND
    ...  send_cmd_without_return_rule  DUT  ${cmd_switch_to_fan_write}  AND
    ...  send_cmd_without_return_rule  DUT  ipmitool raw 0x3a 0x3e 0x08 0xA0 0x00 0x00 0x00 ${fru_1}  AND
    ...  independent_step  add  send_cmd_without_return_rule  DUT  ${cmd_get_and_set_fru_write_protect_status} 6 1  AND
    ...  OS Disconnect Device


BMC_FRU_Read_Stress_Test
    [Documentation]  10.1.2  Keep reading the BMC FRU via “ipmitool fru print” command via KCS interface to
                    ...  check the FRU info can be read out correctly each time.
    [Tags]     BMC_FRU_Read_Stress_Test  Midstone100X  AMI_BMC  stress
    [Setup]     OS Connect Device
    independent_step  1  set_sel_clear  DUT
    independent_step  2  transfer_shell_for_stress  DUT  ${cmd_svt_bmc_fru_read_stress}  ${set_svt_bmc_fru_loop}  FRU Test PASSED  FRU Test FAILED  100
    independent_step  3  check_sel_info_only_clear  DUT
    independent_step  4  OS Disconnect Device
    [Teardown]  Run Keyword If Test Failed  End AC Disconnect


BMC_Sensor_Read_Stress_Test
    [Documentation]  10.1.3  Keep reading the bmc sensor via “ipmitool sensor” command via KCS interface to
                    ...  check the sensor reading should be normal and correct always under normal temperature.
    [Tags]     BMC_Sensor_Read_Stress_Test  Midstone100X  AMI_BMC  stress
    [Setup]     OS Connect Device
    independent_step  1  unzip_sdk_zip_and_run  DUT
    independent_step  2  set_sel_clear  DUT
    independent_step  3  set_reset_type  DUT  ${cmd_ipmitool_mc_reset_cold}  cold
    independent_step  4  set_sel_clear  DUT
    independent_step  5  transfer_shell_for_stress  DUT  ${cmd_svt_bmc_sensor_read_stress}  ${set_svt_bmc_sensor_loop}  Sensor Scan PASSED  Sensor Scan FAILED  100
    independent_step  6  check_sel_info_only_clear  DUT
    independent_step  7  delete_folder  DUT  ${dut_shell_path}
    independent_step  8  OS Disconnect Device
    [Teardown]  Run Keyword If Test Failed  End AC Disconnect


Enable_Disable_BMC_Virtual_USB
    [Documentation]  1.1.4  check virtual USB status
    [Tags]     Enable_Disable_BMC_Virtual_USB  AMI_BMC  Midstone100X
    [Setup]     OS Connect Device
    independent_step  1  check_bmc_virtual_usb_status  DUT  ${cmd_get_bmc_virtual_usb_status}
    independent_step  2  set_bmc_virtual_usb_device  DUT  False
    independent_step  3  set_reset_type  DUT  ${cmd_ipmitool_mc_reset_cold}  cold
    independent_step  4  check_bmc_virtual_usb_status  DUT  ${cmd_get_bmc_virtual_usb_status}
    independent_step  5  set_bmc_virtual_usb_device  DUT  False
    independent_step  6  set_bmc_virtual_usb_device  DUT
    [Teardown]  OS Disconnect Device


Switch_BIOS_Flash
    [Documentation]  1.1.8 	Switch BIOS Flash
    [Tags]     Switch_BIOS_Flash  AMI_BMC  Midstone100X
    [Setup]     OS Connect Device
    independent_step  1  check_cmd_response  DUT  ${cmd_get_bios_start_from_primary_backup}  01
    independent_step  2  set_start_bios_primary_backup  DUT  False
    independent_step  3  set_power_status  DUT  cycle  ${empty}  True
    independent_step  4  check_cmd_response  DUT  ${cmd_get_bios_start_from_primary_backup}  03
    independent_step  5  set_start_bios_primary_backup  DUT
    independent_step  6  set_power_status  DUT  cycle  ${empty}  True
    independent_step  7  check_cmd_response  DUT  ${cmd_get_bios_start_from_primary_backup}  01
    independent_step  8  OS Disconnect Device
    [Teardown]  Run Keyword If Test Failed
    ...  Run Keywords
    ...  OS Connect Device  AND
    ...  set_start_bios_primary_backup  DUT  AND
    ...  set_power_status  DUT  cycle  ${empty}  True  AND
    ...  OS Disconnect Device


Get_Airflow
    [Documentation]  1.1.1  Get Airflow
    [Tags]     Get_Airflow  AMI_BMC  Midstone100X
    [Setup]     OS Connect Device
    independent_step  1  check_fan_air_flow  DUT
    [Teardown]  OS Disconnect Device


Set_Get_FRU_Write_Protect
    [Documentation]  1.1.10 Set/Get FRU Write Protect
    [Tags]     Set_Get_FRU_Write_Protect  AMI_BMC  Midstone100X
    [Setup]     OS Connect Device
    ${fru_1}  get_fru_info  DUT  1
    ${fru_3}  get_fru_info  DUT  3
    ${fru_6}  get_fru_info  DUT  6
    ${fru_7}  get_fru_info  DUT  7
    ${fru_8}  get_fru_info  DUT  8
    ${fru_9}  get_fru_info  DUT  9
    ${board_product_info_1}  get_fru_info  DUT  1  Board Product
    ${board_product_info_3}  get_fru_info  DUT  3  Board Product
    ${board_product_info_6}  get_fru_info  DUT  6  Board Product
    ${board_product_info_7}  get_fru_info  DUT  7  Board Product
    ${board_product_info_8}  get_fru_info  DUT  8  Board Product
    ${board_product_info_9}  get_fru_info  DUT  9  Board Product
    &{dict_board_product}  Create Dictionary  1=${board_product_info_1}  3=${board_product_info_3}
      ...  6=${board_product_info_6}  7=${board_product_info_7}  8=${board_product_info_8}  9=${board_product_info_9}
    Log  dict_board_product items:${dict_board_product}
    FOR  ${status}  IN  @{fru_id_list_get_status}
        check_cmd_response  DUT  ${cmd_get_and_set_fru_write_protect_status} ${status}  01
    END
    FOR  ${enable}  IN  @{fru_id_list_enable}
        send_cmd_without_return_rule  DUT  ${cmd_get_and_set_fru_write_protect_status} ${enable}
    END
    independent_step  1  set_fru_write_by_ipmi  DUT
    ${fru_1_disable}  get_fru_info  DUT  1
    ${fru_3_disable}  get_fru_info  DUT  3
    ${fru_6_disable}  get_fru_info  DUT  6
    ${fru_7_disable}  get_fru_info  DUT  7
    ${fru_8_disable}  get_fru_info  DUT  8
    ${fru_9_disable}  get_fru_info  DUT  9
    independent_step  2  check_info_equal  ${fru_1}  ${fru_1_disable}
    independent_step  3  check_info_equal  ${fru_3}  ${fru_3_disable}
    independent_step  4  check_info_equal  ${fru_6}  ${fru_6_disable}
    independent_step  5  check_info_equal  ${fru_7}  ${fru_7_disable}
    independent_step  6  check_info_equal  ${fru_8}  ${fru_8_disable}
    independent_step  7  check_info_equal  ${fru_9}  ${fru_9_disable}
    FOR  ${disable}  IN  @{fru_id_list_disable}
        send_cmd_without_return_rule  DUT  ${cmd_get_and_set_fru_write_protect_status} ${disable}
    END
    independent_step  8  set_fru_write_by_ipmi  DUT
    ${fru_1_enable}  get_fru_info  DUT  1
    ${fru_3_enable}  get_fru_info  DUT  3
    ${fru_6_enable}  get_fru_info  DUT  6
    ${fru_7_enable}  get_fru_info  DUT  7
    ${fru_8_enable}  get_fru_info  DUT  8
    ${fru_9_enable}  get_fru_info  DUT  9
    independent_step  9  check_info_equal  ${fru_1}  ${fru_1_enable}  False
    independent_step  10  check_info_equal  ${fru_3}  ${fru_3_enable}  False
    independent_step  11  check_info_equal  ${fru_6}  ${fru_6_enable}  False
    independent_step  12  check_info_equal  ${fru_7}  ${fru_7_enable}  False
    independent_step  13  check_info_equal  ${fru_8}  ${fru_8_enable}  False
    independent_step  14  check_info_equal  ${fru_9}  ${fru_9_enable}  False
    independent_step  15  set_fru_write_by_ipmi  DUT  ${dict_board_product}
    FOR  ${enable}  IN  @{fru_id_list_enable}
        send_cmd_without_return_rule  DUT  ${cmd_get_and_set_fru_write_protect_status} ${enable}
    END
    independent_step  17  OS Disconnect Device
    [Teardown]  Run Keyword If Test Failed
    ...  Run Keywords
    ...  OS Connect Device  AND
    ...  set_fru_write_by_ipmi  DUT  ${dict_board_product}  AND
    ...  OS Disconnect Device


BMC_MAC_Address_Test
    [Documentation]  1.1.13 BMC MAC Address Test
    [Tags]     BMC_MAC_Address_Test  AMI_BMC  Midstone100X
    [Setup]     OS Connect Device
    ${mac}  get_fru0_mac  DUT
    independent_step  1  send_cmd_without_return_rule  DUT  ${cmd_edit_fruo_mac} ${write_fru0_mac}
    independent_step  2  set_wait  5
    independent_step  3  set_reset_type  DUT  ${cmd_ipmitool_mc_reset_cold}  cold
    independent_step  4  verify_bmc_mac_address  DUT  ${cmd_get_lan1_mac}  ${response_lan1_mac}
    independent_step  5  send_cmd_without_return_rule  DUT  ${cmd_edit_fruo_mac} 0000000002G2
    independent_step  6  set_wait  5
    ${mac_change}  get_fru0_mac  DUT
    independent_step  7  check_info_equal  ${mac_change}  0000000002G2
    independent_step  8  set_reset_type  DUT  ${cmd_ipmitool_mc_reset_cold}  cold
    independent_step  9  verify_bmc_mac_address  DUT  ${cmd_get_lan1_mac}  ${response_lan1_mac}
    independent_step  10  send_cmd_without_return_rule  DUT  ${cmd_edit_fruo_mac} ${mac}
    independent_step  11  set_wait  5
    independent_step  12  set_reset_type  DUT  ${cmd_ipmitool_mc_reset_cold}  cold
    independent_step  13  OS Disconnect Device
    [Teardown]  Run Keyword If Test Failed
    ...  Run Keywords
    ...  OS Connect Device  AND
    ...  send_cmd_without_return_rule  DUT  ${cmd_edit_fruo_mac} ${mac}  AND
    ...  set_reset_type  DUT  ${cmd_ipmitool_mc_reset_cold}  cold  False  AND
    ...  OS Disconnect Device


Boot_Option_Flag_Test
    [Documentation]  1.1.14 Boot Option Flag Test
    [Tags]     Boot_Option_Flag_Test  AMI_BMC  Midstone100X
    [Setup]     OS Connect Device
    independent_step  1  send_cmd_without_return_rule  DUT  ${cmd_set_boot_flag_valid_bit_clearing_to_00}
    independent_step  2  set_wait  5
    independent_step  3  send_cmd_without_return_rule  DUT  ${cmd_set_boot_to_BIOS_for_next_boot}
    independent_step  4  set_wait  2
    independent_step  5  check_cmd_response  DUT  ${cmd_check_set_boot_to_BIOS_for_next_boot}  ${response_check_set_boot_to_BIOS_for_next_boot}
    independent_step  6  send_cmd_without_return_rule  DUT  ${cmd_reset_os}  True  Core Version  180
    independent_step  7  whitebox_exit_bios_setup  DUT  False
    independent_step  8  set_root_hostname  DUT
    independent_step  9  send_cmd_without_return_rule  DUT  ${cmd_set_boot_flag_valid_bit_clearing_to_00}
    independent_step  10  send_cmd_without_return_rule  DUT  ${cmd_set_boot_to_BIOS_for_next_boot}
    independent_step  11  set_wait  61
    independent_step  12  send_cmd_without_return_rule  DUT  ${cmd_reset_os}
    independent_step  13  connect  DUT
    independent_step  14  OS Disconnect Device
    [Teardown]  Run Keyword If Test Failed  End AC Disconnect


BMC_Update_Stress_Test
    [Documentation]  12.1  To check the BMC FW programming functions by updating the BMC FW with CFUflash in Linux OS.
    [Tags]     BMC_Update_Stress_Test  AMI_BMC  Midstone100X  stress
    [Setup]     OS Connect Device
    FOR  ${index}  IN RANGE  1  ${bmc_update_stress_test_loop}
        Log  Loop ${index}
        ${ip}  get_ip_address_from_ipmitool  DUT
        independent_step  add_1  set_fw_boot_selector  DUT  2
        independent_step  add-2  set_reset_type  DUT  ${cmd_ipmitool_mc_reset_cold}  cold  True
        independent_step  add-3  set_bmc_virtual_usb_device  DUT
        independent_step  add-4  update_by_cfu  DUT  bmc  False  now
        independent_step  add_5  set_fw_boot_selector  DUT  1
        independent_step  add_6  set_reset_type  DUT  ${cmd_ipmitool_mc_reset_cold}  cold  True
        independent_step  add_7  update_by_cfu  DUT  bmc  True  now
        independent_step  1  run update bmc by cfu to lower primary usb
        independent_step  2  run update bmc by cfu to high primary usb
        independent_step  3  set_fw_boot_selector  DUT  2
        independent_step  4  set_reset_type  DUT  ${cmd_ipmitool_mc_reset_cold}  cold  True
        ${ip}  get_ip_address_from_ipmitool  DUT
        independent_step  5  set_update_bmc_primary_backup  DUT  False  ip=${ip}
        independent_step  6  run update bmc by cfu to lower backup usb
        independent_step  7  run update bmc by cfu to high backup usb
    END
    independent_step  8  OS Disconnect Device
    [Teardown]  Run Keyword If Test Failed  End Bmc Online Update Test


Boot_Option_Configuration_Test
    [Documentation]  9.5.3 To verify if BMC can control the boot options correctly
    [Tags]     Boot_Option_Configuration_Test  AMI_BMC
    [Setup]     OS Connect Device
    ${ip}  get_ip_address_from_ipmitool  DUT
    independent_step  1  send_cmd  DUT  ${cmd_set_into_bios_step}  ${ip}
    independent_step  2  send_cmd  DUT  ${cmd_set_into_bios_step_next}  ${ip}
    independent_step  3  check_cmd_response  DUT  ${cmd_check_set_boot_into_bios_1}
                    ...  ${response_check_set_boot_into_bios}  ip=${ip}
    independent_step  4  check_cmd_response  DUT  ${cmd_check_set_boot_into_bios_2}
                    ...  ${response_check_set_boot_into_bios_next}  ip=${ip}
    independent_step  5  set_power_status  DUT  cycle  ${ip}
    independent_step  6  read_until  DUT  System Date  300
    independent_step  7  whitebox_exit_bios_setup  DUT  False
    independent_step  8  set_power_status  DUT  cycle  ${ip}
    independent_step  9  connect  DUT
    FOR  ${index}  IN RANGE  1  3
        ${ip}  get_ip_address_from_ipmitool  DUT
        independent_step  10  send_cmd  DUT  ${cmd_set_into_bios_step}  ${ip}
        independent_step  11  send_cmd  DUT  ${cmd_set_into_bios_step_always}  ${ip}
        independent_step  12  check_cmd_response  DUT  ${cmd_check_set_boot_into_bios_1}
                        ...  ${response_check_set_boot_into_bios}  ip=${ip}
        independent_step  13  check_cmd_response  DUT  ${cmd_check_set_boot_into_bios_2}
                        ...  ${response_check_set_boot_into_bios_always}  ip=${ip}
        independent_step  14  set_power_status  DUT  cycle  ${ip}
        independent_step  15  read_until  DUT  System Date  300
        independent_step  15  whitebox_exit_bios_setup  DUT  False
        independent_step  16  set_root_hostname  DUT
    END
    independent_step  17  send_cmd  DUT  ${cmd_set_into_bios_step}  ${ip}
    independent_step  18  send_cmd  DUT  ${cmd_set_boot_from_dvd_next}  ${ip}
    independent_step  19  check_cmd_response  DUT  ${cmd_check_set_boot_into_bios_1}
                        ...  ${response_check_set_boot_into_bios}  ip=${ip}
    independent_step  20  check_cmd_response  DUT  ${cmd_check_set_boot_into_bios_2}
                        ...  ${response_check_set_boot_from_dvd_next}  ip=${ip}
    independent_step  21  set_power_status  DUT  cycle  ${ip}
    independent_step  22  read_until  DUT  Troubleshooting  360
    independent_step  23  set_power_status  DUT  cycle  ${ip}
    independent_step  24  connect  DUT
    independent_step  25  send_cmd  DUT  ${cmd_set_into_bios_step}  ${ip}
    independent_step  26  send_cmd  DUT  ${cmd_set_boot_from_dvd_always}  ${ip}
    independent_step  27  check_cmd_response  DUT  ${cmd_check_set_boot_into_bios_1}
                        ...  ${response_check_set_boot_into_bios}  ip=${ip}
    independent_step  28  check_cmd_response  DUT  ${cmd_check_set_boot_into_bios_2}
                        ...  ${response_check_set_boot_from_dvd_always}  ip=${ip}
    independent_step  29  set_power_status  DUT  cycle  ${ip}
    independent_step  30  read_until  DUT  Troubleshooting  360
    independent_step  31  set_power_status  DUT  cycle  ${ip}
    independent_step  32  whitebox_lib.enter_bios_setup  DUT
    independent_step  33  send_key  DUT  KEY_RIGHT  5
    ${read_info}  read_until  DUT  Boot Option #2  15
    independent_step  34  check_keyword_in_info  ${read_info}  ${keyword_boot_option_1_dvd}
    independent_step  35  set_ipv4_pxe_support_status  DUT
    independent_step  36  save_bios_and_exit  DUT  False
    independent_step  37  send_cmd  DUT  ipmitool chassis bootdev bios  ${ip}
    independent_step  38  send_cmd  DUT  ipmitool raw 0 2 3  ${ip}
    independent_step  39  whitebox_lib.enter_bios_setup  DUT
    independent_step  40  send_cmd  DUT  ${cmd_set_into_bios_step}  ${ip}
    independent_step  41  send_cmd  DUT  ${cmd_set_boot_from_pxe_next}  ${ip}
    independent_step  42  check_cmd_response  DUT  ${cmd_check_set_boot_into_bios_1}
                        ...  ${response_check_set_boot_into_bios}  ip=${ip}
    independent_step  42  check_cmd_response  DUT  ${cmd_check_set_boot_into_bios_2}
                        ...  ${response_check_set_boot_from_pex_next}  ip=${ip}
    independent_step  43  set_power_status  DUT  cycle  ${ip}
    independent_step  44  read_until  DUT  ${keyword_enter_pxe}  300
    independent_step  45  set_power_status  DUT  cycle  ${ip}
    independent_step  46  connect  DUT
    independent_step  47  send_cmd  DUT  ${cmd_set_into_bios_step}  ${ip}
    independent_step  48  send_cmd  DUT  ${cmd_set_boot_from_pxe_always}  ${ip}
    independent_step  49  set_wait  10
    independent_step  50  check_cmd_response  DUT  ${cmd_check_set_boot_into_bios_1}
                        ...  ${response_check_set_boot_into_bios}  ip=${ip}
    independent_step  51  check_cmd_response  DUT  ${cmd_check_set_boot_into_bios_2}
                        ...  ${response_set_boot_from_pxe_always}  ip=${ip}
    independent_step  52  set_power_status  DUT  cycle  ${ip}
    independent_step  53  read_until  DUT  ${keyword_enter_pxe}  300
    independent_step  54  set_power_status  DUT  cycle  ${ip}
    independent_step  55  whitebox_lib.enter_bios_setup  DUT
    independent_step  56  send_key  DUT  KEY_RIGHT  5
    ${read_pxe_info}  read_until  DUT  Boot Option #2  10
    independent_step  57  check_keyword_in_info  ${read_pxe_info}  ${keyword_boot_option_1_pxe}
    independent_step  58  send_cmd  DUT  ipmitool chassis bootdev bios  ${ip}
    independent_step  59  send_cmd  DUT  ipmitool raw 0 2 3  ${ip}
    independent_step  60  read_until  DUT  System Date  300
    independent_step  61  set_ipv4_pxe_support_status  DUT disabled
    independent_step  62  save_bios_and_exit  DUT
    ${ip}  get_ip_address_from_ipmitool  DUT
    independent_step  63  send_cmd  DUT  ipmitool chassis bootdev bios  ${ip}
    independent_step  64  send_cmd  DUT  ipmitool raw 0 2 2  ${ip}
    independent_step  65  whitebox_lib.enter_bios_setup  DUT
    independent_step  66  send_key  DUT  KEY_RIGHT  5
    independent_step  67  send_key  DUT  KEY_DOWN  3
    independent_step  68  send_key  DUT  KEY_ENTER
    independent_step  69  send_key  DUT  KEY_DOWN  ${step_num_to_uefi_shell_mode}
    independent_step  70  send_key  DUT  KEY_ENTER
    independent_step  71  save_bios_and_exit  DUT  False
    independent_step  72  read_until  DUT  UEFI Interactive Shell  60
    independent_step  73  send_cmd  DUT  ${cmd_set_into_bios_step}  ${ip}
    independent_step  74  send_cmd  DUT  ${cmd_set_boot_from_hdd_next}  ${ip}
    independent_step  75  check_cmd_response  DUT  ${cmd_check_set_boot_into_bios_1}
                        ...  ${response_check_set_boot_into_bios}  ip=${ip}
    independent_step  76  check_cmd_response  DUT  ${cmd_check_set_boot_into_bios_2}
                        ...  ${response_set_boot_from_hdd_next}  ip=${ip}
    independent_step  77  set_power_status  DUT  cycle  ${ip}
    independent_step  78  check_hdd_startup_items  DUT
    independent_step  79  set_power_status  DUT  cycle  ${ip}
    independent_step  80  read_until  DUT  UEFI Interactive Shell  300
    independent_step  81  send_cmd  DUT  ${cmd_set_into_bios_step}  ${ip}
    independent_step  82  send_cmd  DUT  ${cmd_set_boot_from_hdd_always}  ${ip}
    independent_step  83  check_cmd_response  DUT  ${cmd_check_set_boot_into_bios_1}
                        ...  ${response_check_set_boot_into_bios}  ip=${ip}
    independent_step  84  check_cmd_response  DUT  ${cmd_check_set_boot_into_bios_2}
                        ...  ${response_set_boot_from_hdd_always}  ip=${ip}
    independent_step  85  set_power_status  DUT  cycle  ${ip}
    independent_step  86  check_hdd_startup_items  DUT
    independent_step  87  set_power_status  DUT  cycle  ${ip}
    independent_step  88  whitebox_lib.enter_bios_setup  DUT
    independent_step  89  send_key  DUT  KEY_RIGHT  5
    ${read_hdd_info}  read_until  DUT  Boot Option #2  10
    independent_step  90  check_keyword_in_info  ${read_hdd_info}  ${keyword_set_hdd_alway_in_bios_boot_option}
    independent_step  91  set_default_boot_option  DUT  ${ip}
    independent_step  92  OS Disconnect Device
    [Teardown]  Run Keyword If Test Failed
    ...  Run Keywords
    ...  OS Connect Device  AND
    ...  set_default_boot_option  DUT  ${ip}  AND
    ...  OS Disconnect Device


SEL_Operation_Test
    [Documentation]  9.7.2  9.15.1  To verify KCS interfaces and communication via KCS from BMC to BIOS.
    [Tags]     SEL_Operation_Test  Midstone100X  AMI_BMC
    [Timeout]  720 min 00 seconds
    [Setup]     OS Connect Device
    ${ip}  get_ip_address_from_ipmitool  DUT
    independent_step  1  check_cmd_response  DUT  ${cmd_get_sel_policy_status}  01
    independent_step  2  set_sel_clear  DUT  ${ip}
    independent_step  3  check_sel_shell_info_linear  DUT  3639
    independent_step  4  set_power_status  DUT  cycle  ${ip}  True
    independent_step  5  check_bmc_sel_list_keyword  DUT  soft-off,working  False  ${ip}
    independent_step  6  set_sel_clear  DUT  ${ip}
    independent_step  7  check_sel_shell_info_circular  DUT  40000
    independent_step  8  set_power_status  DUT  cycle  ${ip}  True
    independent_step  9  check_bmc_sel_list_keyword  DUT  soft-off,working  True  ${ip}
    independent_step  10  set_sel_clear  DUT  ${ip}  120
    independent_step  11  OS Disconnect Device
    [Teardown]  Run Keyword If Test Failed  End AC Disconnect


test_1
    [Documentation]
    [Tags]     test_1
    [Setup]     OS Connect Device
    independent_step  3.3  check_bios_info_power_cycle  DUT  ${bios_version_old}  primary
    independent_step  3.4  whitebox_exit_bios_setup  DUT  False
    [Teardown]  OS Disconnect Device

test_2
    [Documentation]
    [Tags]     test_2
    [Setup]     OS Connect Device
    independent_step  2  AA
    [Teardown]  OS Disconnect Device