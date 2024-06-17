#  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #
# LEGALESE:   "Copyright (C) 2019-2020, Celestica Corp. All rights reserved." #
#                                                                             #
# This source code is confidential, proprietary, and contains trade           #
# secrets that are the sole property of Celestica Corp.                       #
# Copy and/or distribution of this source code or disassembly or reverse      #
# engineering of the resultant object code are strictly forbidden without     #
# the written consent of Celestica Corp.                                      #
#                                                                             #
#  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #
#  ## Variable file used for bmc.robot #  ##
G_RETRY_COUNT = '3x'
CENTOS_MODE = 'centos'
# CENTOS_MODE = "DIAGOS"
FW_update_tool = 'CFUFLASH_4.93'
BMC_Product_ID = '509'
BMC_lan_print_1_mac_address = '00:01:ff:6d:08:36'
BMC_lan_print_8_mac_address = '00:01:ff:5d:08:36'
BMC_version = '2.17'
BMC_version_ESMB = '7.17'
BMC_Manufacturer_ID = '6894'
CPLD_version = '10 05'
eth_mac_addr = '00:01:ff:4d:08:36'
BMC_UUID = '6dff0100-3608-03ef-0010-debf00c9146d'
error_messages_list = 'error,fault,fail,warning,critical'
management_interface = 'eno6'
pci_device_number = '156'
BIOS_version = 'TITANRB.2.00.04'
CPU_model_name = 'Intel(R) Xeon(R) Gold 6140 CPU @ 2.30GHz'
memory_size = '16G'
#  ONSR-BMCT-BSFC-0001-0001
remote = 'False'
#  CONSR-BMCT-BSFC-0002-0001
#   Power On(always-on)|Power Off(always-off)|Last State(previous)
modified_power_restore_policy = 'Last State'
#   CONSR-BMCT-BSFC-0003-0001
bios_password = 'c411ie'
COM0_baud_rate = '115200'
#   CONSR-BMCT-BSFC-0004-0001  CONSR-BMCT-BSFC-0005-0001  CONSR-BMCT-BSFC-0004-0001
rsp_device_id = '20 01 01 93 02 bf ee 1a 00 70 04 00 00 00 00'
#   CONSR-BMCT-BSFC-0005-0001
#  0h=reserved  1h=CALLBACK  2h=USER  3h=OPERATOR  4h=ADMINISTRATOR  5h=OEM
expected_level = '04'
user_id = '3'
#   Network_001_IP setting test
lan_id = '8'
ipsrc_mode_1 = 'static'
ipsrc_mode_2 = 'dhcp'
ipaddr = '192.168.10.11'
netmask = '255.255.255.0'
ping_count = '5'
#  CONSR-BMCT-NTWT-0010-0001
support_suite_id = '3,17'
unsupport_suite_id = ''
#  CONSR-BMCT-NTWT-0014-0001
ping_timeout = '300'
#  IPMI command
bmc_username = 'admin'
bmc_password = 'admin'
cmd_get_device_id = 'ipmitool raw 0x06 0x01'
device_id = {
    'Firmware Revision': '',  # will be updated to current version defined by SwImage.yaml or ImageInfo.yaml
    'Manufacturer ID': '6894',
    'Product ID': '1136 (0x470)'
}
cmd_cold_reset = 'ipmitool raw 0x06 0x02'
remote_cmd_cold_reset = 'raw 0x06 0x02'
cmd_warm_reset = 'ipmitool raw 0x06 0x03'
remote_cmd_warm_reset = 'raw 0x06 0x03'
cmd_sel_clear = 'ipmitool sel clear'
cmd_get_self_test_result = 'ipmitool raw 0x06 0x04'
rsp_self_test = '55 00'  #  '55 00'
cmd_set_wdt_1 = 'ipmitool raw 0x06 0x24 0x01 0x03 0x00 0x3e 0x58 0x02'
cmd_set_wdt_2 = 'ipmitool raw 0x06 0x24 0x01 0x00 0x00 0x00 0x00 0x00'
cmd_get_wdt = 'ipmitool raw 0x06 0x25'
cmd_reset_wdt = 'ipmitool raw 0x06 0x22'
rsp_wdt_1 = '01 03 00 00 58 02 58 02'
cmd_default_ACPI_power_state = 'ipmitool raw 0x06 0x06 0x80 0x80'
cmd_set_ACPI_power_state_soft_off = 'ipmitool raw 0x06 0x06 0x85 0x80'
cmd_get_ACPI_power_state = 'ipmitool raw 0x6 0x7'
rsp_ACPI_power_state_soft_off = '05 00'
rsp_ACPI_power_state_default = '00 00'
cmd_set_bmc_global_enables = 'ipmitool raw 0x06 0x2e 0x01'
cmd_get_bmc_global_enables = 'ipmitool raw 0x06 0x2f'
rsp_get_bmc_global_enables = '01'
cmd_Clear_Message_Flags = 'ipmitool raw 0x06 0x30 0x01'
cmd_Get_Message_Flags = 'ipmitool raw 0x06 0x31'
rsp_Get_Message_Flags = '00'
cmd_Enable_Message_Channel_Receive = 'ipmitool raw 0x06 0x32 0x08 0x01'
cmd_Get_Channel_Authentication_capabilities = 'ipmitool raw 0x06 0x38 0x88 0x04'
rsp_Get_Channel_Authentication_capabilities = '08 84 14 03 00 00 00 00'
#  CONSR-BMC-IPMI-0018-0001
cmd_Set_Session_Privilege_Level = 'raw 06 0x3b 04'
rsp_Set_Session_Privilege_Level = '04'
cmd_Get_Session_Info = 'ipmitool raw 0x06 0x3d 0x00'
rsp_Get_Session_Info = '00 24 00'
cmd_Get_AuthCode = 'ipmitool raw 06 0x3f 01 0x08 01 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00'
tyr_rsp_Get_AuthCode = '35 57 36 65 b9 98 5f cd 14 97 1b 11 9c 66 b9 50'
cmd_Set_Channel_Access = 'ipmitool raw 0x06 0x40 0x08 0x30 0x04'
cmd_Get_Channel_Access = 'ipmitool raw 0x06 0x41 0x08 0x40'
rsp_Get_Channel_Access = '12 04'
cmd_Get_Channel_Info = 'ipmitool raw 0x06 0x42 0x08'
rsp_Get_Channel_Info = '08 04 01 80 f2 1b 00 00 00'
cmd_Set_User_Access = 'ipmitool raw 0x06 0x43 0xb8 0x01 0x04'
cmd_Get_User_Access = 'ipmitool raw 0x06 0x44 0x08 0x01'
rsp_Get_User_Access = '0a 81 02 34'
cmd_Set_User_name = 'ipmitool raw 0x06 0x45 0x03 0x61 0x61 0x62 0x63 0x64 00 00 00 00 00 00 00 00 00 00 00'
cmd_Get_User_name = 'ipmitool raw 06 0x46 01'
rsp_Get_User_name = '00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00'
cmd_Set_User_Password = 'ipmitool raw 06 0x47 03 02 61 62 63 64 65 66 00 00 00 00 00 00 00 00 00 00'
cmd_Get_Payload_Activation_Status = 'ipmitool raw 06 0x4a 01'
rsp_Get_Payload_Activation_Status = '01 00 00'
cmd_Get_Payload_Instance_Info = 'ipmitool raw 06 0x4b 01 01'
rsp_Get_Payload_Instance_Info = '00 00 00 00 00 00 00 00 00 00 00 00'
cmd_Set_user_Payload_Access = 'ipmitool raw 06 0x4c 0x08 02 02 00 00 00'
cmd_Get_user_Payload_Access = 'ipmitool raw 06 0x4d 0x08 02'
rsp_Get_user_Payload_Access = '02 00 00 00'
cmd_Get_channel_Payload_support = 'ipmitool raw 06 0x4e 0x08'
rsp_Get_channel_Payload_support = '03 00 00 00 00 00 00 00'
cmd_Get_channel_Payload_Version = 'ipmitool raw 06 0x4f 0x08 00'
rsp_Get_channel_Payload_Version = '10'
cmd_Master_Write_Read = 'ipmitool raw 06 0x54 0x08 00 0x80'
rsp_Master_Write_Read = '08 c0 00 00 40 80 c0 01 01 40 80 c0 02 01 41 80 c0'
cmd_Set_Channel_Security_Keys = 'ipmitool raw 06 0x56 0x08 00 00 01 01 01 01'
rsp_Set_Channel_Security_Keys = '02 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00'
cmd_Get_Chassis_Capabilities = 'ipmitool raw 00 00'
rsp_Get_Chassis_Capabilities = '00 20 20 20 20 20'
cmd_Get_Chassis_Status = 'ipmitool raw 00 01'
rsp_Get_Chassis_Status = '41 10 40 f0'
cmd_Set_Event_Receiver = 'ipmitool raw 04 00 0x20 00'
cmd_Get_Event_Receiver = 'ipmitool raw 04 01'
rsp_Get_Event_Receiver = '20 00'
cmd_Platform_Event_Message = 'ipmitool raw 04 02 0 0 0 0 0 0'
cmd_Get_PEF_Capabilities = 'ipmitool raw 04 0x10'
rsp_Get_PEF_Capabilities = '51 3f 28'
cmd_Disable_postpone_timer = 'ipmitool raw 04 0x11 00'
rsp_Disable_postpone_timer = '00'
cmd_arm_timer = 'ipmitool raw 04 0x11 01'
rsp_arm_timer = '01'
cmd_get_present_countdown_value = 'ipmitool raw 04 0x11 0xff'
rsp_get_present_countdown_value = '00'
cmd_Chassis_power_down = 'ipmitool raw 00 02 00'
cmd_Chassis_power_up = 'ipmitool raw 00 02 01'
cmd_Chassis_power_cycle = 'ipmitool raw 00 02 02'
cmd_Chassis_soft_shutdown = 'ipmitool raw 00 02 05'
cmd_Get_System_Restart_Cause = 'ipmitool raw 00 07'
#  CONSR-BMC-IPMI-0043-0001
rsp_Get_System_Restart_Cause = '01 0f'
cmd_1_Set_System_Boot_Options = 'ipmitool raw 00 0x08 00 01'
cmd_2_Set_System_Boot_Options = 'ipmitool raw 00 0x08 03 0x1f'
cmd_3_Set_System_Boot_Options = 'ipmitool raw 00 0x08 05 0x80 0x18 00 00 00'
cmd_4_Set_System_Boot_Options = 'ipmitool raw 00 0x08 00 00'
cmd_Get_System_Boot_Options = 'ipmitool raw 00 0x09 05 00 00'
rsp_Get_System_Boot_Options = '01 05 80 18 00 00 00'
cmd_default_Set_System_Boot_Options = 'ipmitool raw 00 0x08 05 00 00 00 00 00'
rsp_default_Get_System_Boot_Options = '01 05 00 00 00 00 00'
cmd_Set_Power_Cycle_Interval = 'ipmitool raw 00 0x0b 00'
cmd_Set_bmc_load_default = 'ipmitool raw 0x32 0x66'
#  CONSR-BMC-IPMI-0054-0001
cmd_Set_PEF_Capabilities_1 = 'ipmitool raw 04 0x12 00 01'
cmd_Set_PEF_Capabilities_2 = 'ipmitool raw 04 0x12 01 0x0f'
cmd_Set_PEF_Capabilities_3 = 'ipmitool raw 04 0x12 02 0x3f'
cmd_Set_PEF_Capabilities_4 = 'ipmitool raw 04 0x12 06 0x10 0x80 01 01 01 0xFF 0xFF 0xFF 0x02 0xFF 0xFF 0xFF 00 0xFF 00 ' \
                             '00 0xFF 00 00 0xFF 00'
cmd_Set_PEF_Capabilities_5 = 'ipmitool raw 04 0x12 0x09 01 0x18 0x11 00'
cmd_Set_PEF_Capabilities_6 = 'ipmitool raw 04 0x12 00 00'
#  CONSR-BMC-IPMI-0055-0001
cmd_Get_PEF_Configuration_Parameters_1 = 'ipmitool raw 04 0x13 00 00 00'
rsp_Get_PEF_Configuration_Parameters_1 = '11 00'
cmd_Get_PEF_Configuration_Parameters_2 = 'ipmitool raw 04 0x13 01 00 00'
rsp_Get_PEF_Configuration_Parameters_2 = '11 0f'
cmd_Get_PEF_Configuration_Parameters_3 = 'ipmitool raw 04 0x13 02 00 00'
rsp_Get_PEF_Configuration_Parameters_3 = '11 3f'
cmd_Get_PEF_Configuration_Parameters_4 = 'ipmitool raw 04 0x13 06 0x10 00'
rsp_Get_PEF_Configuration_Parameters_4 = '11 10 80 01 01 01 ff ff ff 02 ff ff ff 00 ff 00.*00 ff 00 00 ff 00'
cmd_Get_PEF_Configuration_Parameters_5 = 'ipmitool raw 04 0x13 0x09 0x01 00'
rsp_Get_PEF_Configuration_Parameters_5 = '11 01 18 11 00'
cmd_Set_Last_Processed_Event_ID = 'ipmitool raw 04 0x14 01 1 0'
#  CONSR-BMC-IPMI-0059-0001
cmd_Get_Last_Processed_Event_ID = 'ipmitool raw 04 0x15'

cmd_Alert_Immediate = 'ipmitool raw 04 0x16 01 0 0x80'
cmd_PET_Acknowledge = 'ipmitool raw 04 0x17'
cmd_Set_Sensor_Hysteresis = 'ipmitool raw 04 0x24 01 0xff 00 00'
cmd_Get_Sensor_Hysteresis = 'ipmitool raw 04 0x25 01 0xff'
rsp_Get_Sensor_Hysteresis = '00 00'
cmd_Set_Sensor_Event_Enable = 'ipmitool raw 04 0x28 01 0xc0 80 02 80 02'
cmd_Get_Sensor_Event_Enable = 'ipmitool raw 04 0x29 01'
rsp_Get_Sensor_Event_Enable = 'c0 80 0a 80 0a'
cmd_Re_arm_Sensor_Event = 'ipmitool raw 04 0x2a 01 00'
cmd_Get_Sensor_Event_Status = 'ipmitool raw 04 0x2b 01'
rsp_Get_Sensor_Event_Status = 'c0 00 00 00 00'
cmd_Get_FRU_Inventory_Area_Info = 'ipmitool raw 0x0a 0x10 00'
rsp_Get_FRU_Inventory_Area_Info = '00 08 00'
#  CONSR-BMC-IPMI-0062-0001
cmd_Set_Sensor_Threshold_1 = 'ipmitool raw 04 0x26 01 0x10 00 00 00 00 32 00'
cmd_Set_Sensor_Threshold_2 = 'ipmitool raw 04 0x26 01 0x08 00 00 00 28 00 00'
#  CONSR-BMC-IPMI-0063-0001
#  lower non-critical|lower critical|lower non-recoverable|upper non-critical|upper critical|upper non-recoverabl
cmd_Get_Sensor_Threshold = 'ipmitool raw 04 0x27 01'
rsp_Get_Sensor_Threshold = '00 00 00 64 69 6e'
#  CONSR-BMC-IPMI-0068-0001
cmd_Get_Sensor_Reading = 'ipmitool raw 04 0x2d 01'
#  CONSR-BMC-IPMI-0071-0001
cmd_Write_FRU_Inventory_Area_Info = 'ipmitool raw 0x0a 0x12 02 00 00 01 02 03 04 05 06 07 0x08 0x09 0x0a 0x0b 0x0c 0x0d 0x0e 0x0f'
#  CONSR-BMC-IPMI-0074-0001  CONSR-BMC-IPMI-0076-0001  CONSR-BMC-IPMI-0078-0001
cmd_Reserve_SDR_Repository = 'ipmitool raw 0x0a 0x22'
#  CONSR-BMC-IPMI-0075-0001 CONSR-BMC-IPMI-0076-0001
cmd_Get_SDR = 'ipmitool raw 0x0a 0x23 00 00 00 00 00 0xff'
#  CONSR-BMC-IPMI-0077-0001
cmd_Delete_SDR = 'ipmitool raw 0x0a 0x26 00 00 00 01'
#  CONSR-BMC-IPMI-0081-0001
cmd_Run_Initialization_Agent = 'ipmitool raw 0x0a 0x2c 0'
rsp_Run_Initialization_Agent = '01'
#  CONSR-BMC-IPMI-0082-0001
expected_byte1_value = '51'
#  CONSR-BMC-IPMI-0083-0001
#   check the return value from byte 1-4
cmd_Get_SEL_Allocation_Info = 'ipmitool raw 0x0a 0x41'
rsp_Get_SEL_Allocation_Info = '37 0e 12 00'
#  CONSR-BMC-IPMI-0084-0001
cmd_Reserve_SEL = 'ipmitool raw 0x0a 0x42'
#  CONSR-BMC-IPMI-0088-0001
rsp_Clear_SEL = '01'
#  CONSR-BMC-IPMI-0091-0001
cmd_Get_SEL_Time_UTC_Offset = 'ipmitool raw 0xa 0x5c'
rsp_Get_SEL_Time_UTC_Offset = '00 00'
#  CONSR-BMC-IPMI-0092-0001
cmd_Set_SEL_Time_UTC_Offset = 'ipmitool raw 0xa 0x5d 0xe0 0x01'
#  CONSR-BMC-IPMI-0093-0001
cmd_set_bmc_lan_arp_off = 'ipmitool lan set 1 arp respond off'
cmd_set_bmc_lan_arp_on = 'ipmitool lan set 1 arp respond on'
#  CONSR-BMC-IPMI-0095-0001
cmd_ipmitool_lan_print = 'ipmitool lan print 1'
bmc_lan_1_info = {
    'MAC Address': '00:01:ff:6d:08:30',
    'IP Address': '10.204.125.72',
    'IP Address Source': 'DHCP Address',
    'Subnet Mask': '255.255.255.0',
    'Default Gateway IP': '10.204.125.1',
    '802.1q VLAN ID': 'Disabled'
}
workspace = '/mnt/data1'
bmc_version_list = {
    "Device ID": "32",
    "Device Revision": "1",
    "Firmware Revision": "1.00",
    "IPMI Version": "2.0",
    "Manufacturer ID": "12290",
    "Product ID": "3250 (0x0cb2)",
}


# Product: Midstone100 X
"""
Notes:
1.CFU tool need update, and rename 'CFUFLASH'
2.You need to upload the old and new versions of BMC, CPLD, and BIOS separately
3.The added account Have 'ssh' permissions
4.Before testing, plug in the mobile CD-ROM drive and install the centos7 installation CD in it
5.fru 1 3 6 7 8 9 Need to write
6.Before testing, plug in the mobile CD-ROM drive and install the centos7 installation CD in it
"""
"""
Common Setting
"""
pdu_port = 15
python_server_ip = "10.10.10.138"
python_server_user = r"root"
python_server_password = r"123456"
dut_username = "root"  # for ssh
dut_password = "123"    # for ssh
dut_os_ip = r"10.10.10.135"
cmd_ipmitool_mc_info = 'ipmitool mc info'
cmd_ipmitool_mc_reset_cold = "ipmitool mc reset cold"
cmd_ipmitool_mc_reset_warm = "ipmitool mc reset warm"
cmd_ipmitool_user_list_1 = 'ipmitool user list 1'
exp_reset_sel_list = ["Entity Presence", "Power Supply", "System ACPI Power State"]


"""
Case Setting
"""
# Case: 1.1.1 Get_Airflow
cmd_get_fan_air_flow = r"ipmitool raw 0x3a 0x62"
airflow_list = ["0x00", "0x01", "0x02", "0x03", "0x04", "0x05", "0x06"]
fen = "B2F"    # B2F/F2B

# Case: 1.1.8 Switch_BIOS_Flash
cmd_get_bios_start_from_primary_backup = r"ipmitool raw 0x3a 0x64 0 1 0x70"

# Case: 1.1.10 Set_Get_FRU_Write_Protect
cmd_get_and_set_fru_write_protect_status = r"ipmitool raw 0x3a 0x61"
LIST__fru_id_list_get_status = ["0x01 2", "0x03 2", "0x06 2", "0x07 2", "0x08 2", "0x09 2"]
LIST__fru_id_list_enable = ["0x01 1", "0x03 1", "0x06 1", "0x07 1", "0x08 1", "0x09 1"]
LIST__fru_id_list_disable = ["0x01 0", "0x03 0", "0x06 0", "0x07 0", "0x08 0", "0x09 0"]
ipmi_write_fru_info = {"1": "TEST BOARD", "3": "CHANGE BOARD", "6": "FAN BOARD A", "7": "FAN BOARD B",
                       "8": "FAN BOARD C", "9": "FAN BOARD D"}

# Case: 1.1.13 BMC_MAC_Address_Test
cmd_edit_fruo_mac = r"ipmitool fru edit 0 field b 6"
write_fru0_mac = r"0093afe5c282"
cmd_get_lan1_mac = r"ipmitool lan print 1"
response_lan1_mac = r"00:93:af:e5:c2:82"

# Case: 1.1.14 Boot_Option_Flag_Test
cmd_set_boot_flag_valid_bit_clearing_to_00 = r"ipmitool raw 0x00 0x08 0x03 0x00"
cmd_set_boot_to_BIOS_for_next_boot = r"ipmitool raw 0x00 0x08 0x05 0x80 0x18 0 0 0"
cmd_check_set_boot_to_BIOS_for_next_boot = r"ipmitool raw 0 9 5 0 0"
response_check_set_boot_to_BIOS_for_next_boot = r"01 05 80 18 00 00 00"
cmd_reset_os = r"ipmitool raw 0x00 0x02 0x03"

# Case: 9.1.3 BMC_Device_Info_Check
midstone_bmc_version = "2.10"
cmd_add_user_test = "test"
cmd_add_user4 = '-U test4 -P test4 raw 0x06 0x01'
cmd_add_user = '-U admin -P admin raw 0x06 0x01'
set_bmc_ipaddr = "10.10.10.229"
set_bmc_ipaddr_oth = "10.10.10.239"
set_bmc_netmask = "255.255.255.0"
set_non_volatile = "115.2"
set_volatile_bit = "115.2"
channel_6_medium_type = r"IPMB (I2C)"
channel_1_medium_type = r"802.3 LAN"
channel_f_medium_type = r"KCS"

# Case: 9.5.3 Boot_Option_Configuration_Test
cmd_set_into_bios_step = r"ipmitool raw 0x0 0x08 0x3 0x1f"
cmd_set_into_bios_step_next = r"ipmitool raw 0x0 0x08 0x5 0xa0 0x18 0 0 0"
cmd_check_set_boot_into_bios_1 = r"ipmitool raw 0x00 0x09 0x03 0x00 0x00"
response_check_set_boot_into_bios = r"01 03 1f"
cmd_check_set_boot_into_bios_2 = r"ipmitool raw 0x00 0x09 0x05 0x00 0x00"
response_check_set_boot_into_bios_next = r"01 05 a0 18 00 00 00"

cmd_set_into_bios_step_always = r"ipmitool raw 0x0 0x08 0x5 0xe0 0x18 0 0 0"
response_check_set_boot_into_bios_always = r"01 05 e0 18 00 00 00"

cmd_set_boot_from_dvd_next = r"ipmitool raw 0x00 0x08 0x5 0xa0 0x3c 0 0 0"
response_check_set_boot_from_dvd_next = r"01 05 a0 3c 00 00 00"

cmd_set_boot_from_dvd_always = r"ipmitool raw 0x00 0x08 0x5 0xe0 0x3c 0 0 0"
response_check_set_boot_from_dvd_always = r"01 05 e0 3c 00 00 00"
# The first boot item should be a DVD in UEFI mode
keyword_boot_option_1_dvd = "UEFI: SlimtypeeBAU1"

cmd_set_boot_from_pxe_next = r"ipmitool raw 0x0 0x08 0x5 0xa0 0x04 0 0 0"
response_check_set_boot_from_pex_next = r"01 05 a0 04 00 00 00"
cmd_set_boot_from_pxe_always = r"ipmitool raw 0x0 0x08 0x5 0xe0 0x04 0 0 0"
response_set_boot_from_pxe_always = r"01 05 e0 04 00 00 00"
# step to set pxe enable
LIST__step_to_set_pxe_enable = ["LEFT", "LEFT", "LEFT", "LEFT", "DOWN", "DOWN", "DOWN", "ENTER", "ENTER", "DOWN",
                                "ENTER", "DOWN", "ENTER", "DOWN", "ENTER"]
# Keyword to enter the pxe system
keyword_enter_pxe = r"Checking Media Presence"
# The first boot item should be a PXE in UEFI mode
keyword_boot_option_1_pxe = "UEFI: PXE IP4 Intel"
# How many times can I press down to change the UEFI shell mode to the first boot item
step_num_to_uefi_shell_mode = 3
# UEFI shell mode changed to the first boot item
cmd_set_boot_from_hdd_next = r"ipmitool raw 0x0 0x08 0x5 0xa0 0x08 0 0 0"
response_set_boot_from_hdd_next = r"01 05 a0 08 00 00 00"
cmd_set_boot_from_hdd_always = r"ipmitool raw 0x0 0x08 0x5 0xe0 0x08 0 0 0"
response_set_boot_from_hdd_always = r"01 05 e0 08 00 00 00"

# After setting hdd, the bios interface display string when the first startup item is sonic or onie
LIST__keyword_set_hdd_alway_in_bios_boot_option = ["SONIC OS", "ONIE: Open Network"]

# Case: 9.6.1 SDR_Information_Test
# There are Assertion / Deassertion attributes, and there is no Reading Mask attribute
special_sen_name_list = ["Fan1_Status", "Fan2_Status", "Fan3_Status", "Fan4_Status", "PSU1_Status",
                         "PSU2_Status", "PowerStatus", "SEL_Status", "Watchdog2", "BMC_FW_Health"]

# Case: 9.8.1 PEF_Configuration_Test
cmd_get_pef_Capabilities = r"ipmitool raw 0x04 0x10"
ssl_cmd_Set_PEF_Capabilities_1 = cmd_Set_PEF_Capabilities_1
ssl_cmd_Set_PEF_Capabilities_2 = cmd_Set_PEF_Capabilities_2
ssl_cmd_Set_PEF_Capabilities_3 = cmd_Set_PEF_Capabilities_3
ssl_cmd_Set_PEF_Capabilities_4 = cmd_Set_PEF_Capabilities_4
ssl_cmd_Set_PEF_Capabilities_5 = cmd_Set_PEF_Capabilities_5
ssl_cmd_Set_PEF_Capabilities_6 = cmd_Set_PEF_Capabilities_6
ssl_cmd_Get_PEF_Configuration_Parameters_1 = cmd_Get_PEF_Configuration_Parameters_1
ssl_rsp_Get_PEF_Configuration_Parameters_1 = rsp_Get_PEF_Configuration_Parameters_1
ssl_cmd_Get_PEF_Configuration_Parameters_2 = cmd_Get_PEF_Configuration_Parameters_2
ssl_rsp_Get_PEF_Configuration_Parameters_2 = rsp_Get_PEF_Configuration_Parameters_2
ssl_cmd_Get_PEF_Configuration_Parameters_3 = cmd_Get_PEF_Configuration_Parameters_3
ssl_rsp_Get_PEF_Configuration_Parameters_3 = rsp_Get_PEF_Configuration_Parameters_3
ssl_cmd_Get_PEF_Configuration_Parameters_4 = cmd_Get_PEF_Configuration_Parameters_4
ssl_rsp_Get_PEF_Configuration_Parameters_4 = rsp_Get_PEF_Configuration_Parameters_4
ssl_cmd_Get_PEF_Configuration_Parameters_5 = cmd_Get_PEF_Configuration_Parameters_5
ssl_rsp_Get_PEF_Configuration_Parameters_5 = rsp_Get_PEF_Configuration_Parameters_5

# Case: 9.12.1 FRU_Access_Test
# The end of the command needs to be filled. eg: ipmitool raw 0x0a 0x10 0x09
cmd_get_fru_inventory_area = 'ipmitool raw 0x0a 0x10 0x0'
rsp_get_fru_inventory_area = '00 10 00'
cmd_get_read_fru_data = r"ipmitool raw 0x0a 0x11 0 0 0 0xff"
cmd_set_fru_protection_disable = r"ipmitool raw 0x3a 0x61 0x06 0x00"
cmd_set_fru_protection_enable = r"ipmitool raw 0x3a 0x61 0x06 0x01"
cmd_write_fru_for_r_w_frus_1 = r"ipmitool raw 0x0a 0x12 0x06 0x00 0x00 0x01 0x02 0x03 0x04"
cmd_write_fru_for_r_w_frus_2 = r"ipmitool raw 0x0a 0x12 0x06 0x00 0x00 0x06 0x03 0x07 0x08"
res_write_fru_for_r_w_frus = "04"
cmd_check_fru_date = r"ipmitool raw 0x0a 0x11 0x06 0x00 0x00 0xff"
res_check_fru_date_1 = r"01 02 03 04"
res_check_fru_date_2 = r"06 03 07 08"
restore_fru6_info = r"ipmitool raw 0x0a 0x12 0x06 0x00 0x00 0x01 0x00 0x00 0x01"
empty_str = ""

# Case: 9.13.1 Extensional_I2C_Master_Write_Read
cmd_get_baseboard_cpld = r"ipmitool raw 0x3a 0x3e 0x00 0x1a 0x01 0x00"
response_baseboard_cpld_version = r"15"  # 当前cpld baseboard的版本
cmd_get_cpld_sw_scratch_default = r"ipmitool raw 0x3a 0x3e 0x00 0x1a 0x01 0x01"
response_cpld_sw_scratch_default = r"de"
cmd_get_right_psu_data = r"ipmitool raw 0x3a 0x3e 0x06 0xa0 0xff 0x00"
cmd_get_lift_psu_data = r"ipmitool raw 0x3a 0x3e 0x06 0xa2 0xff 0x00"
cmd_switch_to_fan_1 = r"ipmitool raw 0x3a 0x3e 0x08 0xEE 0x00 0x08"
cmd_switch_to_fan_2 = r"ipmitool raw 0x3a 0x3e 0x08 0xEE 0x00 0x04"
cmd_switch_to_fan_3 = r"ipmitool raw 0x3a 0x3e 0x08 0xEE 0x00 0x02"
cmd_switch_to_fan_4 = r"ipmitool raw 0x3a 0x3e 0x08 0xEE 0x00 0x01"
cmd_read_fan_fru = r" ipmitool raw 0x3a 0x3e 0x08 0xa0 0xff 0 0"
cmd_switch_to_fan_write = r"ipmitool raw 0x3a 0x3e 0x08 0xEE 0x00 0x08"
cmd_write_fru_info_to_fan1 = r"ipmitool raw 0x3a 0x3e 0x08 0xA0 0x00 0x00 0x00 0x11 0x22 0x33"
check_write_response = "11 22 33"   # 0x11 0x22 0x33

# Case: 9.13.4 Set_Get_GPIO
change_gpio_num_list = [8, 12, 145]

# Case: 9.13.8 Switch_BIOS_Chip_Selector
cmd_check_bios_default_fw = r"ipmitool raw 0x3a 0x10 0"
cmd_check_bios_boot_selector = r"ipmitool raw 0x3a 0x10 0x02"
cmd_get_bios_status = r"ipmitool raw 0x3a 0x10 0x03"
cmd_me_to_recovery = r"ipmitool -b 6 -t 0x2c raw 0x2e 0xdf 0x57 0x01 0x00 0x01"
cmd_me_to_operational = r"ipmitool -b 6 -t 0x2c raw 0x06 0x02"
cmd_get_device_id_me = r"ipmitool -b 6 -t 0x2c raw 0x06 0x01"
cmd_verify_error_1 = r"ipmitool raw 0x3a 0x10 0 0x01"
cmd_verify_error_2 = r"ipmitool raw 0x3a 0x10 0x02 0x01"
cmd_verify_error_3 = r"ipmitool raw 0x3a 0x01 0x01 0x04 0x06"

# Case: 9.13.9 Read_Write_CPLD_Register
cmd_get_cpld_version = r"ipmitool raw 0x3a 0x0c 0x00 0x01 0x00"
cmd_get_cpld_sw_scratch_register_1 = r"ipmitool raw 0x3a 0x0c 0x00 0x01 0x01"
cmd_get_cpld_sw_scratch_register_2 = r"ipmitool raw 0x3a 0x0c 0x00 0x01 0x02"
cmd_get_cpld_sw_scratch_register_3 = r"ipmitool raw 0x3a 0x0c 0x00 0x01 0x03"
cmd_write_baseboarad_cpld_sw_scratch = r"ipmitool raw 0x3a 0x0c 0x00 0x02 0x01 0xff"
cmd_write_baseboarad_cpld_sw_scratch_default = r"ipmitool raw 0x3a 0x0c 0x00 0x02 0x01 0xde"
cmd_cpld_verify_error_1 = r"ipmitool raw 0x3a 0x0c 0x00 0x01 0x00 0x05"
cmd_cpld_verify_error_2 = r"ipmitool raw 0x3a 0x0c 0x00 0x02 0x01 0xff 0x03"

# Case: 9.13.13 Get_Set_NTP_Configuration
cmd_get_ntp_status = r"ipmitool raw 0x32 0xa7"
cmd_set_ntp_disabled = r"ipmitool raw 0x32 0xa8 0x03 0"
cmd_set_ntp_enable = r"ipmitool raw 0x32 0xa8 0x03 0x01"
set_ntp_server = r"192.168.0.1"
cmd_get_bmc_time = r"ipmitool sel time get"

# Case: 9.13.14 Enable_Disable_BMC_Virtual_USB
cmd_get_bmc_virtual_usb_status = "ipmitool raw 0x32 0xab"

# Case: 9.15.1 SEL_Test
cmd_get_sel_policy_status = r"ipmitool raw 0x32 0x7E"

# Case: 10.1.2 BMC_FRU_Read_Stress_Test
set_svt_bmc_fru_loop = 200
cmd_svt_bmc_fru_read_stress = \
    r"/home/test/master/crobot/file_folder/midstone100x/shell/midstone100x_bmc_fru_read_stress.sh"

# Case: 10.1.3 BMC_Sensor_Read_Stress_Test
dut_shell_path = "/home/white_box"
set_svt_bmc_sensor_loop = 200
cmd_svt_bmc_sensor_read_stress = \
    r"/home/test/master/crobot/file_folder/midstone100x/shell/midstone100x_bmc_sensor_read_stress.sh"

# Case: 11.13.3.1 CPLD_Update_Test
# 'COMECPLD Baseboard switchboard1 switchboard2 switchboard3 switchboard4'
cpld_os_version_1_2_lower = r"0x06 11 0.8 0.8 0.8 0.8"  # function:get_cpld_version_in_os
cpld_os_version_1_2_high = r"0x06 15 0.9 0.9 0.9 0.9"
cpld_ac_version_baseboard_come_lower = r"1.1 0.6"  # 'CPLD_BaseBoard+Space+CPLD_COMe'(string)
cpld_ac_version_baseboard_come_high = r"1.5 0.6"

# Case: 11.13.5.2 BIOS_Update_Test_via_USB
bios_version_old = r"1.01.00"
bios_version_now = r"2.00.00"
cmd_set_bios_next_start_primary = r"ipmitool raw 0x3a 0x25 0"
cmd_set_bios_next_start_backup = r"ipmitool raw 0x3a 0x25 1"


# Case: 12.1 BMC_Update_Stress_Test
bmc_update_stress_test_loop = 5

# Case: CONSR-BMCT-BSFC-0008-0001 Function_008_Power Restore Policy
set_power_restore_policy1 = "00"
set_power_restore_policy2 = "01"
set_power_restore_policy3 = "02"
expectedvalue = "07"
exp_restorepolicy_status1 = "always-off"
exp_restorepolicy_status2 = "previous"
exp_restorepolicy_status3 = "always-on"
exp_chassispower_status1 = "on"
exp_chassispower_status2 = "off"
ChassisPower_Status = ""
last_power_state = "1"

# Case: CONSR-BMCT-BSFC-0009-0001: Function_009_Sensor Summary Check
Sensor_pattern = r"(^[a-z\s0-9._]+)\|\s([a-z0-9.\s]+)\|\s[a-z\s0-9]+\|\s([a-z0-9\s]+)\|\s([a-z0-9.\s]+)\|\s([a-z0-9.\s]+)\|\s([a-z0-9.\s]+)\|\s([a-z0-9.\s]+)\|\s([a-z0-9.\s]+)\|\s([a-z0-9.]+)"

Temperature_SensorList=['ESMx_PCH','ESMx_CPU0','ESMx_CPU1','ESMx_CPU0Ch0DM0','ESMx_CPU0Ch0DM1','ESMx_CPU0Ch1DM0','ESMx_CPU0Ch2DM0','ESMx_CPU0Ch3DM0','ESMx_CPU0Ch4DM0','ESMx_CPU0Ch5DM0','ESMx_CPU0Ch6DM0','ESMx_CPU0Ch7DM0','ESMx_CPU1Ch0DM0','ESMx_CPU1Ch0DM1','ESMx_CPU1Ch1DM0','ESMx_CPU1Ch2DM0','ESMx_CPU1Ch3DM0','ESMx_CPU1Ch4DM0','ESMx_CPU1Ch5DM0','ESMx_CPU1Ch6DM0','ESMx_CPU1Ch7DM0','ESMx_CPU0_Tjmax','ESMx_CPU1_Tjmax','ESMx_Inlet','ESMx_Outlet','ESMx_Switch0','ESMx_Switch1','ESMx_PCIeSlot1','ESMx_PCIeSlot2','ESMx_PCIeSlot3','ESMx_PCIeSlot4','PSU0_Ambient','PSU1_Ambient','FrontPanel_1','FrontPanel_2','NVMeSSD01','NVMeSSD02','NVMeSSD03','NVMeSSD04','NVMeSSD05','NVMeSSD06','NVMeSSD07','NVMeSSD08','NVMeSSD09','NVMeSSD10','NVMeSSD11','NVMeSSD12','NVMeSSD13','NVMeSSD14','NVMeSSD15','NVMeSSD16','NVMeSSD17','NVMeSSD18','NVMeSSD19','NVMeSSD20','NVMeSSD21','NVMeSSD22','NVMeSSD23','NVMeSSD24']
Voltage_SensorList=['ESMx_P3VDD_3.3','ESMx_PCH_3.3','ESMx_RTC_3.3','ESMx_CPU0IO_1.0','ESMx_C0_ABCD_1.2','ESMx_C0_EFGH_1.2','ESMx_C1_ABCD_1.2','ESMx_C1_EFGH_1.2','ESMx_CPU0IN_1.8','ESMx_CPU1IN_1.8','ESMx_CPU0SA_0.8','ESMx_CPU0SA_0.8','ESMx_PCH_1.05','ESMx_PCHVNN_0.85','ESMx_PCIE1_0.9','ESMx_CPU1IO_1.0','ESMx_PCIE0_0.9','ESMx_PCHAUX_1.8','ESMx_VCOIN_3.0','ESMx_PVDD_1.8']
PowerSupply_SensorList=['PSU1_Power','PSU2_Power']
Fan_SensorList=['ESMx_FAN1_Front','ESMx_FAN1_Rear','ESMx_FAN2_Front','ESMx_FAN2_Rear','ESMx_FAN3_Front','ESMx_FAN3_Rear','ESMx_FAN4_Front','ESMx_FAN4_Rear','ESMx_FAN5_Front','ESMx_FAN5_Rear','ESMx_FAN6_Front','ESMx_FAN6_Rear','PSU1_FAN1_Front','PSU1_FAN1_Rear','PSU2_FAN1_Front','PSU2_FAN1_Rear']
Discrete_SensorsList=['SEL_STATUS','QPI_STATUS','CORE_STATUS','SYSFW_PROGRESS','CBO_STATUS','DIMM_STATUS','PCIE_STATUS','PEF_Action','Watchdog2','ACPI_PWR_STATE','PSU1_Status','PSU2_Status','CPU_STATUS','BMC FW Health','BMC Reboot']
TotalThreshold_SensorsFunSpec= Temperature_SensorList+Voltage_SensorList+PowerSupply_SensorList+Fan_SensorList+Discrete_SensorsList
off_server ="00"
on_server="01"
#case: CONSR-BMCT-BSFC-0017-0001
expected_fru_size="00 10 00"
chassis_type="Rack Mount Chassis"
board_mfg="CELESTICA-CTH"
board_product="Athena Gen2 MB"
product_mfg="CELESTICA-CTH"
product_name="Athena Gen2"
product_part_number="P2523"
product_version="DVT"
board_part_number="R3139-G0001-02"
product_mfg_fru2="COMPUWARE"
Product_name_fru2="CPR-2021-2M17"
product_part_number_fru2="CPR-2021-2M17"
product_version_fru2="1.0"
serial_number="0987654321098765ABCDEFGHIJKLMNOP"
chassis_ver="To be filled by O.E.M."
BMC_Firmware_version="7.17"
chassis_mfg="CELESTICA-CTH"
serial_number_bios="0987654321098765ABCDEFGH.*IJKLMNOP"
Board_Serial_num="Board-Serial-Number-0123.*45678912"
athena_bios_password = 'c411ie'
number_of_logs = '5000'
MAXINDEX='1' #By default MAXINDEX (Number of iterations) is set to 1. Increase this variable as per stress test requirement
#case: CONSR-BMCT-BHSI-0005-0001 BMC and Host System Interaction Interaction_005_Boot Option
cmd_power_cycle_step = r"power cycle"
TestSteps1 =r"Reboot SUT to check whether the SUT will boot into BIOS setup screen"
TestSteps2 = r"SUT is booted from the first boot device set in the BIOS"
TestSteps10= r"power cycle and check auto boot to UEFI PXE page"
cmd_single_valid = r"raw 0x00 0x08 0x03 0x1f"
cmd_single_valid_next = r"raw 0x00 0x08 0x05 0xa0 0x04 0x00 0x00 0x00"
cmd_permanent_valid = r"raw 0x00 0x08 0x03 0x1f"
cmd_permanent_valid_next = r"raw 0x00 0x08 0x05 0xe0 0x04 0x00 0x00 0x00"
TestSteps10_12 = r"PEX is set to 1st boot option and need to power reset using IPMITool"
validation1=r"Single Valid"
validation2=r"Permanet Valid"
Get_slots_alive="ipmitool -I lanplus -U admin -P admin raw 0x3A 0x97 -H"
Get_cpld_info="ipmitool -I lanplus -U admin -P admin raw 0x3A 0x27 -H"
Set_Drive_power="ipmitool -I lanplus -U admin -P admin raw 0x3A 0xA6 0 -H"
Set_canister_power="ipmitool -I lanplus -U admin -P admin raw 0x3A 0x9E 0 0 -H"
Get_canister_power="ipmitool -I lanplus -U admin -P admin raw 0x3A 0x9F -H"
Set_switch_bios="ipmitool -I lanplus -U admin -P admin raw 0x3A 0x25 0 -H"
Get_current_canister="ipmitool -I lanplus -U admin -P admin raw 0x3A 0xA8 -H"
Get_BMC_memory="ipmitool -I lanplus -U admin -P admin raw 0x3A 0x0A 0 -H"
Set_BMC_memory="ipmitool -I lanplus -U admin -P admin raw 0x3A 0x0A 1 -H"
fan_type="ipmitool -I lanplus -U admin -P admin sdr type fan -H"
set_fan_control="ipmitool -I lanplus -U admin -P admin raw 0x3a 1 0xff 0x30 -H"
Get_fan_status="ipmitool -I lanplus -U admin -P admin raw 0x3a 2 -H"
fan_control_automatic="ipmitool -I lanplus -U admin -P admin raw 0x3a 1 0xff 0xff -H"
all_fan_PWM="ipmitool -I lanplus -U admin -P admin raw 0x3a 1 0xff 0x40 -H"
fail_pattern = "fail|ERROR|Failure|cannot read file|command not found|No such file|not found|Unknown command|No space left on device|Command exited with non-zero status"
#CONSR-BMCT-SRTS-0001-0001 Stress Test Stress_001_BMC Local Stress Test
error_messages_sell_list = 'error,fault,fail,warning'
expected_bmc_version="07 17"
ip_address_source_pattern="IP Address Source.*:.*DHCP Address"
subnet_mask_pattern="Subnet Mask.*:.*255.255.255.0"
mac_address_pattern="MAC Address.*:.*36:ed:26:ab:aa:62"
#CONSR-BMCT-SRTS-0002-0001 Stress_002_BMC FW Update Stress Test (Local)
get_BMC_version="ipmitool raw 0x32 0x8f 9 1 | awk '{print $1}'"
get_BMC_version_next="ipmitool raw 0x32 0x8f 9 2 | awk '{print $1}'"
#CONSR-BMCT-SRTS-0005-0001 Stress_005_SOL Connection Stress Test
testloopcycle='10' #By default testloopcycle (Number of loop cycle) is set to 10. Increase this variable as per stress test requirement
#CONSR-BMCT-FWUP-0002-0001
mac_address_OS_pattern1="00:0a:f7:a7:0c:70"
mac_address_OS_pattern2="00:0a:f7:a7:0c:71"
mac_address_OS_pattern3="52:54:00:16:55:9e"
mac_address_OS_pattern4="52:54:00:16:55:9e"
resource_1 = '/redfish/v1/EventService/Subscriptions'
resource_service_root="/redfish/v1"
resource_service_system="/redfish/v1/Systems"
resource_system_instance="/redfish/v1/Systems/Self"
resource_boot_options_collections="/redfish/v1/Systems/Self/BootOptions"
resource_memory_options_collections="/redfish/v1/Systems/Self/Memory"

resource_2 = '/redfish/v1/UpdateService'
data_ServiceEnabled_true = """'{"ServiceEnabled": true}'"""
data_ServiceEnabled_false = """'{"ServiceEnabled": false}'"""

true_value = True
false_value = False
#CONSR-BMCT-RDFT-0056-0001
self_logservices=r'/redfish/v1/Chassis/Self/LogServices/Logs'

context = "ABCDEFGH"
context_1 = "IJKLMNOP"
resource_3 = '/redfish/v1/EventService/Subscriptions'
data_EventService_Subscription = '{"Context":"ABCDEFGH","Destination":"http://10.204.125.47:5000/event","EventFormatType":"Event","RegistryPrefixes":["SyncAgent","EventLog","Base"],"ResourceTypes":["EventService","AccountService","Chassis","Systems"],"Protocol":"Redfish"}'
data_context_1 = """'{"Context":"IJKLMNOP"}'"""

#CONSR-BMCT-RDFT-0057-0001
data_DataTime_set = """'{"DateTime": "2012-01-01T06:00:00-00:00"}'"""
data_DataTimeLocalOffset_set = """'{"DateTimeLocalOffset": "-00:00"}'"""
data_DataTime = r'2012-01-01T06:00:06+00:00'
data_DataTimeLocalOffset = r'+00:00'
simple_storage_collection="/redfish/v1/Systems/Self/SimpleStorage"
simple_storage="/redfish/v1/Systems/Self/SimpleStorage/1"
log_service_collection_1="/redfish/v1/Systems/Self/LogServices"
log_service_collection_2="/redfish/v1/Managers/Self/LogServices"

#CONSR-BMCT-RDFT-0060-0001
SEL_Log_Entries = r'/redfish/v1/Managers/Self/LogServices/SEL/Entries'

resource_processor_collections="/redfish/v1/Systems/Self/Processors"
resource_Ethernet_interface_collections="/redfish/v1/Managers/Self/EthernetInterfaces"
resource_LogService_chassis="/redfish/v1/Chassis/Self/LogServices"
resource_bootoption1_1="/redfish/v1/Systems/Self/BootOptions/0001"
resource_bootoption1_2="/redfish/v1/Systems/Self/BootOptions/0002"
resource_bootoption1_3="/redfish/v1/Systems/Self/BootOptions/0003"
resource_bootoption1_4="/redfish/v1/Systems/Self/BootOptions/0004"
resource_Ethernet_Interface_Collection_12="/redfish/v1/Systems/Self/EthernetInterfaces"
#CONSR-BMCT-RDFT-0064-0001
LogEntry_Collection_7 = r"/redfish/v1/Chassis/Self/LogServices/Logs/Entries"
Event_Type_message = r"Upper Critical - going high"
Sensor_Type_details = r"Temperature"
#CONSR-BMCT-RDFT-0216-0001
ResourceBlocksCollection_log = r"/redfish/v1/CompositionService/ResourceBlocks"
#CONSR-BMCT-RDFT-0217-0001
resourceblocks_instance_1 = r"/redfish/v1/CompositionService/ResourceBlocks/ComputeBlock"
resourceblocks_instance_2 = r"/redfish/v1/CompositionService/ResourceBlocks/DrivesBlock"
resourceblocks_instance_3 = r"/redfish/v1/CompositionService/ResourceBlocks/NetworkBlock"
#CONSR-BMCT-RDFT-0218-0001
computeblock_compositionstatus_false = """'{"CompositionStatus":{"Reserved":false}}'"""
drivesblock_compositionstatus_false = """'{"CompositionStatus":{"Reserved":false}}'"""
networkblock_compositionstatus_false = """'{"CompositionStatus":{"Reserved":false}}'"""
#CONSR-BMCT-RDFT-0214-0001
CompositionService_resorce = r"/redfish/v1/CompositionService"
#CONSR-BMCT-RDFT-0212-0001
resource_telemetry_logentry = r"/redfish/v1/TelemetryService/LogService/Entries"
#CONSR-BMCT-RDFT-0210-0001
resource_telemetry_logservice = r"/redfish/v1/TelemetryService/LogService"
#CONSR-BMCT-RDFT-0206-0001
resource_telemetryservice_triggers = r"/redfish/v1/TelemetryService/Triggers"
#CONSR-BMCT-RDFT-0204-0001
resource_telemetryservice_metricreports = r"/redfish/v1/TelemetryService/MetricReports"
#CONSR-BMCT-RDFT-0200-0001
resource_metricreportdefinitions = r"/redfish/v1/TelemetryService/MetricReportDefinitions"
#CONSR-BMCT-RDFT-0199-0001
resource_voltage_reading = r"/redfish/v1/TelemetryService/MetricDefinitions/Voltage_Reading"
resource_temperature_reading = r"/redfish/v1/TelemetryService/MetricDefinitions/Temperature_Reading"
resource_fan_reading = r"/redfish/v1/TelemetryService/MetricDefinitions/Fan_Reading"
#CONSR-BMCT-RDFT-0198-0001
resource_metricdefinitions = r"/redfish/v1/TelemetryService/MetricDefinitions"
resource_memory_instance_1="/redfish/v1/Systems/Self/Memory/DevType2_DIMM0"
resource_memory_instance_2="/redfish/v1/Systems/Self/Memory/DevType2_DIMM1"
resource_memory_instance_3="/redfish/v1/Systems/Self/Memory/DevType2_DIMM2"
resource_memory_instance_4="/redfish/v1/Systems/Self/Memory/DevType2_DIMM3"
resource_memory_instance_5="/redfish/v1/Systems/Self/Memory/DevType2_DIMM4"
resource_memory_instance_6="/redfish/v1/Systems/Self/Memory/DevType2_DIMM5"
resource_memory_instance_7="/redfish/v1/Systems/Self/Memory/DevType2_DIMM6"
resource_memory_instance_8="/redfish/v1/Systems/Self/Memory/DevType2_DIMM7"
resource_memory_instance_9="/redfish/v1/Systems/Self/Memory/DevType2_DIMM8"
resource_memory_instance_10="/redfish/v1/Systems/Self/Memory/DevType2_DIMM9"
resource_memory_instance_11="/redfish/v1/Systems/Self/Memory/DevType2_DIMM10"
resource_memory_instance_12="/redfish/v1/Systems/Self/Memory/DevType2_DIMM11"
resource_memory_instance_13="/redfish/v1/Systems/Self/Memory/DevType2_DIMM12"
resource_memory_instance_14="/redfish/v1/Systems/Self/Memory/DevType2_DIMM13"
resource_memory_instance_15="/redfish/v1/Systems/Self/Memory/DevType2_DIMM14"
resource_memory_instance_16="/redfish/v1/Systems/Self/Memory/DevType2_DIMM15"
resource_memory_instance_17="/redfish/v1/Systems/Self/Memory/DevType2_DIMM16"
resource_memory_instance_18="/redfish/v1/Systems/Self/Memory/DevType2_DIMM17"
resource_subprocessor_collection_1="/redfish/v1/Systems/Self/Processors/DevType1_CPU0/SubProcessors"
resource_subprocessor_collection_2="/redfish/v1/Systems/Self/Processors/DevType1_CPU1/SubProcessors"
resource_processor_instance_property_1="/redfish/v1/Systems/Self/Processors/DevType1_CPU0"
resource_processor_instance_property_2="/redfish/v1/Systems/Self/Processors/DevType1_CPU1"
resource_network_interface_instance_1="/redfish/v1/Managers/Self/EthernetInterfaces/bond0"
resource_network_interface_instance_2="/redfish/v1/Managers/Self/EthernetInterfaces/eth0"
resource_network_interface_instance_3="/redfish/v1/Managers/Self/EthernetInterfaces/eth1"
resource_network_interface_instance_4="/redfish/v1/Managers/Self/EthernetInterfaces/usb0"

resource_4 = '/redfish/v1/EventService'
resource_5 = '/redfish/v1/EventService/Actions/EventService.SubmitTestEvent'
resource_6 = '/redfish/v1/TaskService/Tasks'
resource_7 = '/redfish/v1/TaskService'
resource_8 = '/redfish/v1/JsonSchemas'
resource_9 = '/redfish/v1/SessionService/Sessions'
resource_10 = '/redfish/v1/SessionService'
resource_11 = '/redfish/v1/Registries'
resource_12 = '/redfish/v1/Systems/Self/NetworkInterfaces'
resource_13 = '/redfish/v1/Systems/Self/EthernetInterfaces'
resource_14 = '/redfish/v1/Chassis/Self/NetworkAdapters'
resource_15 = '/redfish/v1/Systems/Self/Storage'
resource_16 = '/redfish/v1/Chassis/Self/PCIeDevices'
resource_17 = '/redfish/v1/UpdateService'

data_EventService_SubmitTestEvent = '{"EventId":"1531584914","OriginOfCondition":"/redfish/v1/Chassis/Self","MessageId":"Base.1.5.PropertyValueNotInList","MessageArgs":["Lit","IndicatorLED"],"Severity":"Warning"}'
#CONSR-BMCT-RDFT-0086-0001
resource_Manager_2 = r"/redfish/v1/Managers/Self"
data_datatime_setup = """'{"DateTime": "2000-02-22T06:00:00-00:00"}'"""
data_datatime_output = r"2000-02-22T06:00:06+00:00"
#CONSR-BMCT-RDFT-0196-0001
resource_SubmitTestMetricReport = r"/redfish/v1/TelemetryService/Actions/TelemetryService.SubmitTestMetricReport"
data_SubmitTestMetricReport = '{"MetricReportName":"Average2","GeneratedMetricReportValues":[{"MetricId": "Temp_average_reading_Average","MetricProperty": "/redfish/v1/Chassis/Self/Thermal#/Temperatures/39/ReadingCelsius","MetricValue": "23","Timestamp": "2019-07-01T06:05:52Z"}]}'
#CONSR-BMCT-RDFT-0085-0001
resource_Manager_1 = r'/redfish/v1/Managers/Self'
#CONSR-BMCT-RDFT-0078-0001
resource_Chassis_1 = r'/redfish/v1/Chassis/Self'
#CONSR-BMCT-RDFT-0081-0001
resource_ChassisSelfPower = r'/redfish/v1/Chassis/Self/Power'
#CONSR-BMCT-RDFT-0083-0001
resource_ChassisSelfThermal = r'/redfish/v1/Chassis/Self/Thermal'
Resource_Zone_Collection="/redfish/v1/CompositionService/ResourceZones"
Resource_Zone_Collection_instance="/redfish/v1/CompositionService/ResourceZones/1"
Capabilities="/redfish/v1/Systems/Capabilities"
Configurations_1="/redfish/v1/configurations"
AccountService_Configurations_1="/redfish/v1/AccountService/Configurations"
CertificateService_1="/redfish/v1/CertificateService"
resource_ethernet_interface_instance_1="/redfish/v1/Systems/Self/EthernetInterfaces/EthernetInterface1"
resource_ethernet_interface_instance_2="/redfish/v1/Systems/Self/EthernetInterfaces/EthernetInterface2"
resource_ethernet_interface_instance_3="/redfish/v1/Systems/Self/EthernetInterfaces/VirtualEthernetInterface3"
resource_bios="/redfish/v1/Systems/Self/Bios"
resource_bios_property="/redfish/v1/Systems/Self/Bios/SD"
resource_chassis_log_property="/redfish/v1/Chassis/Self/LogServices/Logs"
resource_telemetry_log_property="/redfish/v1/TelemetryService/LogService"
resource_managers_logservices="/redfish/v1/Managers/Self/LogServices"
resource_managerslog_property_1="/redfish/v1/Managers/Self/LogServices/SEL"
resource_managerslog_property_2="/redfish/v1/Managers/Self/LogServices/EventLog"
resource_managerslog_property_3="/redfish/v1/Managers/Self/LogServices/AuditLog"
resource_bios_logentries="/redfish/v1/Systems/Self/LogServices/BIOS/Entries"
resource_log_bios_properties="/redfish/v1/Systems/Self/LogServices/BIOS"
resource_proc1_subproc1="/redfish/v1/Systems/Self/Processors/DevType1_CPU0/SubProcessors/DevType1_CPU0_Core0"
resource_proc1_subproc2="/redfish/v1/Systems/Self/Processors/DevType1_CPU0/SubProcessors/DevType1_CPU0_Core1"
resource_proc1_subproc3="/redfish/v1/Systems/Self/Processors/DevType1_CPU0/SubProcessors/DevType1_CPU0_Core2"
resource_proc1_subproc4="/redfish/v1/Systems/Self/Processors/DevType1_CPU0/SubProcessors/DevType1_CPU0_Core3"
resource_proc1_subproc5="/redfish/v1/Systems/Self/Processors/DevType1_CPU0/SubProcessors/DevType1_CPU0_Core4"
resource_proc1_subproc6="/redfish/v1/Systems/Self/Processors/DevType1_CPU0/SubProcessors/DevType1_CPU0_Core5"
resource_proc1_subproc7="/redfish/v1/Systems/Self/Processors/DevType1_CPU0/SubProcessors/DevType1_CPU0_Core6"
resource_proc1_subproc8="/redfish/v1/Systems/Self/Processors/DevType1_CPU0/SubProcessors/DevType1_CPU0_Core7"
resource_proc1_subproc9="/redfish/v1/Systems/Self/Processors/DevType1_CPU0/SubProcessors/DevType1_CPU0_Core8"
resource_proc1_subproc10="/redfish/v1/Systems/Self/Processors/DevType1_CPU0/SubProcessors/DevType1_CPU0_Core9"
resource_proc1_subproc11="/redfish/v1/Systems/Self/Processors/DevType1_CPU0/SubProcessors/DevType1_CPU0_Core10"
resource_proc1_subproc12="/redfish/v1/Systems/Self/Processors/DevType1_CPU0/SubProcessors/DevType1_CPU0_Core11"
resource_proc1_subproc13="/redfish/v1/Systems/Self/Processors/DevType1_CPU0/SubProcessors/DevType1_CPU0_Core12"
resource_proc1_subproc14="/redfish/v1/Systems/Self/Processors/DevType1_CPU0/SubProcessors/DevType1_CPU0_Core13"
resource_proc1_subproc15="/redfish/v1/Systems/Self/Processors/DevType1_CPU0/SubProcessors/DevType1_CPU0_Core14"
resource_proc1_subproc16="/redfish/v1/Systems/Self/Processors/DevType1_CPU0/SubProcessors/DevType1_CPU0_Core15"
resource_proc1_subproc17="/redfish/v1/Systems/Self/Processors/DevType1_CPU0/SubProcessors/DevType1_CPU0_Core16"
resource_proc1_subproc18="/redfish/v1/Systems/Self/Processors/DevType1_CPU0/SubProcessors/DevType1_CPU0_Core17"
resource_proc1_subproc19="/redfish/v1/Systems/Self/Processors/DevType1_CPU0/SubProcessors/DevType1_CPU0_Core18"
resource_proc1_subproc20="/redfish/v1/Systems/Self/Processors/DevType1_CPU0/SubProcessors/DevType1_CPU0_Core19"
resource_proc1_subproc21="/redfish/v1/Systems/Self/Processors/DevType1_CPU0/SubProcessors/DevType1_CPU0_Core20"
resource_proc1_subproc22="/redfish/v1/Systems/Self/Processors/DevType1_CPU0/SubProcessors/DevType1_CPU0_Core21"
resource_proc1_subproc23="/redfish/v1/Systems/Self/Processors/DevType1_CPU0/SubProcessors/DevType1_CPU0_Core22"
resource_proc1_subproc24="/redfish/v1/Systems/Self/Processors/DevType1_CPU0/SubProcessors/DevType1_CPU0_Core23"
resource_proc2_subproc1="/redfish/v1/Systems/Self/Processors/DevType1_CPU1/SubProcessors/DevType1_CPU1_Core0"
resource_proc2_subproc2="/redfish/v1/Systems/Self/Processors/DevType1_CPU1/SubProcessors/DevType1_CPU1_Core1"
resource_proc2_subproc3="/redfish/v1/Systems/Self/Processors/DevType1_CPU1/SubProcessors/DevType1_CPU1_Core2"
resource_proc2_subproc4="/redfish/v1/Systems/Self/Processors/DevType1_CPU1/SubProcessors/DevType1_CPU1_Core3"
resource_proc2_subproc5="/redfish/v1/Systems/Self/Processors/DevType1_CPU1/SubProcessors/DevType1_CPU1_Core4"
resource_proc2_subproc6="/redfish/v1/Systems/Self/Processors/DevType1_CPU1/SubProcessors/DevType1_CPU1_Core5"
resource_proc2_subproc7="/redfish/v1/Systems/Self/Processors/DevType1_CPU1/SubProcessors/DevType1_CPU1_Core6"
resource_proc2_subproc8="/redfish/v1/Systems/Self/Processors/DevType1_CPU1/SubProcessors/DevType1_CPU1_Core7"
resource_proc2_subproc9="/redfish/v1/Systems/Self/Processors/DevType1_CPU1/SubProcessors/DevType1_CPU1_Core8"
resource_proc2_subproc10="/redfish/v1/Systems/Self/Processors/DevType1_CPU1/SubProcessors/DevType1_CPU1_Core9"
resource_proc2_subproc11="/redfish/v1/Systems/Self/Processors/DevType1_CPU1/SubProcessors/DevType1_CPU1_Core10"
resource_proc2_subproc12="/redfish/v1/Systems/Self/Processors/DevType1_CPU1/SubProcessors/DevType1_CPU1_Core11"
resource_proc2_subproc13="/redfish/v1/Systems/Self/Processors/DevType1_CPU1/SubProcessors/DevType1_CPU1_Core12"
resource_proc2_subproc14="/redfish/v1/Systems/Self/Processors/DevType1_CPU1/SubProcessors/DevType1_CPU1_Core13"
resource_proc2_subproc15="/redfish/v1/Systems/Self/Processors/DevType1_CPU1/SubProcessors/DevType1_CPU1_Core14"
resource_proc2_subproc16="/redfish/v1/Systems/Self/Processors/DevType1_CPU1/SubProcessors/DevType1_CPU1_Core15"
resource_proc2_subproc17="/redfish/v1/Systems/Self/Processors/DevType1_CPU1/SubProcessors/DevType1_CPU1_Core16"
resource_proc2_subproc18="/redfish/v1/Systems/Self/Processors/DevType1_CPU1/SubProcessors/DevType1_CPU1_Core17"
resource_proc2_subproc19="/redfish/v1/Systems/Self/Processors/DevType1_CPU1/SubProcessors/DevType1_CPU1_Core18"
resource_proc2_subproc20="/redfish/v1/Systems/Self/Processors/DevType1_CPU1/SubProcessors/DevType1_CPU1_Core19"
resource_proc2_subproc21="/redfish/v1/Systems/Self/Processors/DevType1_CPU1/SubProcessors/DevType1_CPU1_Core20"
resource_proc2_subproc22="/redfish/v1/Systems/Self/Processors/DevType1_CPU1/SubProcessors/DevType1_CPU1_Core21"
resource_proc2_subproc23="/redfish/v1/Systems/Self/Processors/DevType1_CPU1/SubProcessors/DevType1_CPU1_Core22"
resource_proc2_subproc24="/redfish/v1/Systems/Self/Processors/DevType1_CPU1/SubProcessors/DevType1_CPU1_Core23"
#CONSR-BMCT-RDFT-0088-0001
resource_NetworkProtocol = r'/redfish/v1/Managers/Self/NetworkProtocol'
#CONSR-BMCT-RDFT-0090-0001
resource_SerialInterfaces = r'/redfish/v1/Managers/Self/SerialInterfaces'
#CONSR-BMCT-RDFT-0091-0001
source_IPMI_SOL = r'/redfish/v1/Managers/Self/SerialInterfaces/IPMI-SOL'	
data_BitRate_set1 = """'{"BitRate": "9600"}'"""
data_BitRate_output1 = "9600"
data_BitRate_set2 = """'{"BitRate": "115200"}'"""
data_BitRate_output2 = "115200"
#CONSR-BMCT-RDFT-0092-0001
data_InterfaceEnabled_true = """'{"InterfaceEnabled": true}'"""
data_InterfaceEnabled_false = """'{"InterfaceEnabled": false}'"""
#CONSR-BMCT-RDFT-0079-0001
data_AssetTag_set1 = """'{"AssetTag":"customer setting"}'"""
data_AssetTag_set2 = """'{"AssetTag":"Free for asset tag"}'"""
data_AssetTag_output1 = "customer setting"
data_AssetTag_output2 = "Free for asset tag"
#CONSR-BMCT-RDFT-0097-0001
resource_accountservice = r'/redfish/v1/AccountService'
expected_DateTime="2012-01-01T06:00:.*00:00"
expected_DateTime_1="2012-01-01T06:01:.*00:00"
data_DateTime= """'{"DateTime":"2012-01-01T06:00:00+00:00","DateTimeLocalOffset": "+00:00"}'"""
data_DateTime_1= """'{"DateTime":"2012-01-01T06:01:00+00:00","DateTimeLocalOffset": "+00:00"}'"""
expected_DateTimeOffset=r'+00:00'
set_DateTime="""'{"DateTime":"2012-01-01T06:00:00+08:00","DateTimeLocalOffset": "+08:00"}'"""
expected_DateTime_2="2012-01-01T06:00:.*08:00"
expected_DateTimeOffset_1=r'+08:00'
set_DateTime_1="""'{"DateTime":"2022-01-01T06:00:00+08:00","DateTimeLocalOffset": "+08:00"}'"""
expected_DateTime_3="2022-01-01T06:00:.*08:00"
#CONSR-BMCT-RDFT-0058-0001
resource_LogEntry_Collection_1 = r'/redfish/v1/Systems/Self/LogServices/BIOS/Entries'
#CONSR-BMCT-RDFT-0105-0001
resource_Accountinstance = r'/redfish/v1/AccountService/Accounts'
#CONSR-BMCT-RDFT-0108-0001
resource_AccountRoles = r'/redfish/v1/AccountService/Roles'
#CONSR-BMCT-RDFT-0110-0001
resource_Role_Collection_3 = r"/redfish/v1/AccountService/Roles"
resource_FirmwareInventory_collections="/redfish/v1/UpdateService/FirmwareInventory"
resource_secureboot="/redfish/v1/Systems/Self/SecureBoot"
TelemetryService_1="/redfish/v1/TelemetryService"
AccountService_4="/redfish/v1/AccountService/Accounts"
Manager_Account_Collection_1="/redfish/v1/AccountService/Accounts"
ManagerCollection="/redfish/v1/Managers"
HostInterface_Collection="/redfish/v1/Managers/Self/HostInterfaces"
HostInterface="/redfish/v1/Managers/Self/HostInterfaces/Self"
HostEthernetInterfaceCollection="/redfish/v1/Managers/Self/HostInterfaces/Self/HostEthernetInterfaces"
ManagerEthernetInterface_Instance="/redfish/v1/Managers/Self/EthernetInterfaces/usb0"
#CONSR-BMCT-RDFT-0107-0001
data_NewAccount = '{"Name": "Test User Account",  "Description": "Test User Account", "Enabled": true, "Password": "superuser", "UserName": "Operator", "RoleId": "Operator", "Locked": false}'
#CONSR-BMCT-RDFT-0003-0001
resource_NewSystem = "/redfish/v1/Systems/NewSystem"
data_NewSystem = '{"Name":"NewSystem","Links":{"ResourceBlocks":[{"@odata.id": "/redfish/v1/CompositionService/ResourceBlocks/ComputeBlock"},{"@odata.id": "/redfish/v1/CompositionService/ResourceBlocks/DrivesBlock"}]},"HostName":"intel"}'
#CONSR-BMCT-RDFT-0070-0001
resource_InterfaceCollection_1 = "/redfish/v1/Systems/Self/EthernetInterfaces"
resource_VLANNetwork_InterfaceCollection_1 = "/redfish/v1/Systems/Self/EthernetInterfaces/EthernetInterface1/VLANs"
#CONSR-BMCT-RDFT-0071-0001
data_NewAccount_VLANID = '{"VLANId": 100,"VLANEnable":true}'
data_Members_VLANID_100 = '/redfish/v1/Systems/Self/EthernetInterfaces/EthernetInterface1/VLANs/oob_EthernetInterface1_100'
resource_pcieslots="/redfish/v1/Chassis/Self/PCIeSlots"
resource_sensor_collections="/redfish/v1/Chassis/Self/Sensors"
resource_storage_drive1="/redfish/v1/Systems/Self/Storage/StorageUnit_0/Drives/NVMe_Device3_NSID1"
resource_storage_drive2="/redfish/v1/Systems/Self/Storage/StorageUnit_0/Drives/NVMe_Device4_NSID1"
resource_storage_drive3="/redfish/v1/Systems/Self/Storage/StorageUnit_0/Drives/NVMe_Device5_NSID1"
resource_storage_drive4="/redfish/v1/Systems/Self/Storage/StorageUnit_0/Drives/NVMe_Device6_NSID1"
resource_storage_drive5="/redfish/v1/Systems/Self/Storage/StorageUnit_0/Drives/NVMe_Device7_NSID1"
resource_storage_drive6="/redfish/v1/Systems/Self/Storage/StorageUnit_0/Drives/SATA_Device0_Port2"
resource_storage_drive7="/redfish/v1/Systems/Self/Storage/StorageUnit_0/Drives/USB_Device1_Port7"
resource_storage_drive8="/redfish/v1/Systems/Self/Storage/StorageUnit_0/Drives/USB_Device2_Port7"
resource_networkportinfo="/redfish/v1/Chassis/Self/NetworkAdapters"
#CONSR-BMCT-RDFT-0072-0001
resource_networkadapters = "/redfish/v1/Chassis/Self/NetworkAdapters"
resource_networkadapters_vlans = "/redfish/v1/Chassis/Self/NetworkAdapters/DevType7_NIC0/NetworkDeviceFunctions/NetworkDeviceFunction0/Ethernet/VLANs"
#CONSR-BMCT-RDFT-0073-0001
resource_VLAN_Network_Interface_1 = "/redfish/v1/Systems/Self/EthernetInterfaces"
resource_VLAN_Network_Interface_ID = "/redfish/v1/Systems/Self/EthernetInterfaces/EthernetInterface1/VLANs/oob_EthernetInterface1_100"
#CONSR-BMCT-RDFT-0076-0001
resource_VLANsNetworkingID = "oob_NetworkDeviceFunction0_100"
resource_auditlog_entries="/redfish/v1/Managers/Self/LogServices/AuditLog/Entries"
resource_chassis="/redfish/v1/Chassis"
NetworkPort="/redfish/v1/Chassis/Self/NetworkAdapters/DevType7_NIC0/NetworkPorts/DevType7_Slot0_Instance0_PORT0"
TelemetryService_3="/redfish/v1/TelemetryService"
SupportedCollectionFunctions="""'{"SupportedCollectionFunctions":[ "Maximum", "Minimum", "Summation"]}'"""
Check_value= ['Maximum', 'Minimum', 'Summation']
Secure_Boot="/redfish/v1/Systems/Self/SecureBoot"
data_SecureBootEnable_true = """'{"SecureBootEnable": true}'"""
data_SecureBootEnable_false = """'{"SecureBootEnable": false}'"""
mac_address_OS_pattern1_b="00:0a:f7:a7:0c:70"
mac_address_OS_pattern2_b="00:0a:f7:a7:0c:71"
mac_address_OS_pattern3_b="52:54:00:1d:d5:85"
mac_address_OS_pattern4_b="52:54:00:1d:d5:85"
mac_address_OS_pattern5_b="00:a0:c9:00:00:00"
mode = 'local'
