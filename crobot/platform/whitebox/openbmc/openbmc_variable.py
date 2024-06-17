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
import os
import YamlParse
import random

#  ## Variable file used for openbmc.robot #  ##

FW_STRESS_CYCLE = 2
G_RETRY_COUNT = '1x'
Peer_Canister = True
BMC_Manufacturer_ID = '12290'
BMC_Product_ID = '4038'
imageInfo = YamlParse.getSwImageInfo()
BMC_version = imageInfo['Artemis_A_BMC']['newVersion']
BIOS_version = imageInfo['Artemis_A_BIOS']['newVersion']
CPLD_version = imageInfo['Artemis_A_CPLD']['newVersion']
BMC_UUID = '6dff0100-3608-03ef-0010-debf00c9146d'
#  IPMI command
remote = 'True'
device_id = {
    'Firmware Revision': '',  # will be updated to current version defined by SwImage.yaml or ImageInfo.yaml
    'Manufacturer ID': '6894',
    'Product ID': '1136 (0x470)'
}
CENTOS_MODE = ''
BMC_lan_print_1_mac_address = ''
BMC_lan_print_2_mac_address = ''
eth_mac_addr = ''
error_messages_list = 'error,fault,fail,warning,critical'
management_interface = ''
pci_device_number = ''
CPU_model_name = ''
memory_size = ''

DeviceName = os.environ.get("deviceName", "")
PeerDeviceName = DeviceName + '_peer' if Peer_Canister else None
deviceInfo = YamlParse.getDeviceInfo()
deviceDict_A = deviceInfo[DeviceName]
deviceDict_B = deviceInfo[PeerDeviceName]
OS_A_LOGIN_PROMPT = deviceDict_A.get('loginPromptDiagOS')
OS_B_LOGIN_PROMPT = deviceDict_B.get('loginPromptDiagOS')
OS_LOGIN_PROMPT = '|'.join([OS_A_LOGIN_PROMPT, OS_B_LOGIN_PROMPT])
RAND_DEV = random.choice([DeviceName, PeerDeviceName])

power_restore_policy_on = "always-on"
power_restore_policy_off = "always-off"
power_restore_policy_per = "previous"

openbmc_info_map = {'bmc_version': ['mc info', r'Firmware Revision\s+:\s+(\S+)'],
                    'product_id': ['mc info', r'Product ID\s+:\s+(\d+)\s+\S+'],
                    'power_status': ['power status', r'Chassis Power is (\w+)'],
                    'policy_status': ['chassis status', r'Power Restore Policy\s:\s(.+)']}
chassis_policy_cmd_list = {power_restore_policy_off: 'raw 00 06 00',
                           power_restore_policy_per: 'raw 00 06 01',
                           power_restore_policy_on: 'raw 00 06 02'}
# 07: Chassis policy supports always on, always off and pervious.
policy_cmd_output = '07'
chassis_cmd_list = {'power off': 'raw 00 02 00',
                    'power on': 'raw 00 02 01',
                    'power cycle': 'raw 00 02 02',
                    'hard reset': 'raw 00 02 03',
                    'trigger NMI interrupt': 'raw 00 02 04',
                    'soft shutdown': 'raw 00 02 05'
                    } | chassis_policy_cmd_list
device_global_cmd_list = {'get_device_id': 'raw 06 01',
                          'cold_reset': 'raw 06 02',
                          'warm_reset': 'raw 06 03',
                          'self_test': 'raw 06 04',
                          'watchdog_get': 'raw 0x06 0x25',
                          'watchdog_reset': 'raw 0x06 0x22'
                          }
oem_cmd_list = {'multi-node_info': 'raw 0x3a 0xb6 0x00',
                'get_fsc_mode': 'raw 0x2e 0x04 0xcf 0xc2 0x00 0x00 0x00',
                'set_fsc_mode': 'raw 0x2e 0x04 0xcf 0xc2 0x00 0x01 0x00 0x00',
                'dis_fsc_mode': 'raw 0x2e 0x04 0xcf 0xc2 0x00 0x01 0x00 0x01',
                'get_post_code': 'raw 0x3a 0x2f',
                'get_bios_boot': 'raw 0x3a 0x2a 0x00',
                'set_bios_pri': 'raw 0x3a 0x2a 0x01 0x00',
                'set_bios_sec': 'raw 0x3a 0x2a 0x01 0x01',
                'set_fan_pwm': 'raw 0x3a 0x26 0x01'  # Add 1 byte System Fan PWM: 0-0x64h
                }
sensor_disc_check_p = r'^\w+\s+[|]\s\S+\s+[|]\s(?P<type>\S+|\S+\s\S)\s+[|]\s'
sdr_elist_p = r'^(?P<sensor_name>\w+)\s+[|]\s(?P<sensor_id>\w\w)h\s+[|]\s(?P<status>\S+)\s+[|].+[|](?P<info>.+)'
sensor_discrete = r'^(?P<sensor_name>\w+)\s+[|]\s(?P<value>\S+)\s+[|]\s(?P<type>\S+)\s+[|]\s' \
                  r'(?P<status>\S+)[|]\s(?P<L_N_rec>\S+)\s+[|]\s(?P<L_crit>\S+)\s+[|]\s(?P<L_warn>\S+)\s+[|]\s' \
                  r'(?P<U_warn>\S+)\s+[|]\s(?P<U_crit>\S+)\s+[|]\s(?P<U_N_rec>\S+)\s+'
sensor_non_disc = r'^(?P<sensor_name>\w+)\s+[|]\s(?P<value>\S+)\s+[|]\s(?P<type>\S+|\S+\s\S)\s+[|]\s' \
                  r'(?P<status>\S+)\s+[|]\s(?P<L_N_rec>\S+)\s+[|]\s(?P<L_crit>\S+)\s+[|]\s(?P<L_warn>\S+)\s+[|]\s' \
                  r'(?P<U_warn>\S+)\s+[|]\s(?P<U_crit>\S+)\s+[|]\s(?P<U_N_rec>\S+)\s+'

temp_sensor = 'temp'
current_sensor = 'current'
fan_sensor = 'fan'
power_sensor = 'power'
voltage_sensor = 'voltage'
sensor_type_info = {temp_sensor: 'degrees C',
                    current_sensor: 'Amps',
                    fan_sensor: 'RPM',
                    power_sensor: 'Watts',
                    voltage_sensor: 'Volts'
                    }
sel_list_pattern = r'^(?P<ID>\w+)\s[|]\s(?P<Date>\w+\S\w+\S\w+)\s[|]\s(?P<Time>\w+\S\w+\S\w+).+[|]' \
                   r'\s(?P<Name>\S+\s\S+)\s[|]\s(?P<Type>.+)\s[|]\s(?P<Event>.+)'
sel_elist_pattern = r'^(?P<ID>\w+)\s[|]\s(?P<Date>\w+\S\w+\S\w+)\s[|]\s(?P<Time>\w+\S\w+\S\w+).+[|]' \
                    r'\s(?P<Name>\S+\s\S+)\s[|]\s(?P<Type>.+)\s[|]\s(?P<Event>.+)\s[|]\s(?P<Detail>.+)'
OPENBMC_FLASH = [r'Erasing block: \w/\w\w\w\w \(0%\)',
                 r'Erasing block: \w\w\w\w/\w\w\w\w \(100%\)',
                 r'Writing kb: \w/65\w\w\w \(0%\)',
                 r'Writing kb: 65\w\w\w/65\w\w\w \(100%\)',
                 # r'Verifying kb: \w/65\w\w\w \(0%\)',
                 r'Verifying kb: 65\w\w\w/65\w\w\w \(100%\)']
OPENBMC_FLASH_REGEX = ['Updating bmc0'] + OPENBMC_FLASH
OPENBMC_FLASH_BACKUP_REGEX = ['Updating bmc1'] + OPENBMC_FLASH
BIOS_SPI_FLASH_REGEX = [r'Erasing block: \w/\w\w\w \(0%\)',
                        r'Erasing block: \w\w\w/\w\w\w \(100%\)',
                        r'Writing kb: \w/16\w\w\w \(0%\)',
                        r'Writing kb: 16\w\w\w/16\w\w\w \(100%\)',
                        # r'Verifying kb: \w/16\w\w\w \(0%\)',
                        r'Verifying kb: 16\w\w\w/16\w\w\w \(100%\)']
CPLD_JTAG_REGEX = ['Erase/Program the Flash',
                   '100%',
                   r'Verify config pages: \w\w\w\w',
                   # TODO: sometimes can not detect PASS, the system has been reset.
                   # 'PASS!'
                   ]
BOOT_REGEX = ['U-Boot', 'Starting kernel', 'artemis login:']
OS_BOOT_REGEX = [BIOS_version, OS_LOGIN_PROMPT]
cmd_get_deviceID = 'raw 06 01'
ver_output = ' '.join(BMC_version.split('.'))
pro_id_output = ' '.join([hex(int(BMC_Product_ID) & 0xff)[2:], hex(int(BMC_Product_ID) >> 8)[2:]])
manu_id_output = ' '.join([hex(int(BMC_Manufacturer_ID) & 0xff)[2:], hex(int(BMC_Manufacturer_ID) >> 8)[2:]])
rsp_device_id = f'20 81 {ver_output} 02 8d {manu_id_output} 00 {pro_id_output} 00 00 00 00'
cmd_cold_reset = 'raw 06 02'
cmd_warm_reset = 'raw 06 03'
cmd_self_test = 'raw 06 04'
rsp_cmd_self_test = "56 00"
cmd_Set_ACPI_Power_State = 'raw 0x06 0x06 0x00 0x00'
cmd_Get_ACPI_Power_State = 'raw 06 07'
cmd_set_bmc_global_enables = 'raw 0x06 0x2e 0x09'
cmd_get_bmc_global_enables = 'raw 0x06 0x2f'
rsp_get_bmc_global_enables = '09'
cmd_clear_message_flags = "raw 06 0x30 01"
cmd_get_message_flags = "raw 06 0x31"
rsp_cmd_Get_message_flags = "00"
cmd_get_system_GUID = "raw 06 0x37"
cmd_Enable_Message_Channel_Receive = 'raw 0x06 0x32 0x08 0x01'
cmd_Get_Channel_Authentication_capabilities = 'raw 0x06 0x38 0x01 0x04'
rsp_Get_Channel_Authentication_capabilities = '01 80 04 02 00 00 00 00'
cmd_get_session_challenge = "raw 06 0x39 02 0x61 0x64 0x6d 0x69 0x6e 00 00 00 00 00 00 00 00 00 00 00"
cmd_set_session_privilege_Level = "-I lanplus -H 10.10.10.37 -U root -P 0penBmc raw 06 0x3b 04"
cmd_get_session_privilege_Level = "04"
cmd_get_session_info = "raw 06 0x3d 00"
# rsp_get_session_info = '41 1e 01 01 04 12 0a 0a 0a 49 00 00 00 00 00 00 '
cmd_Get_AuthCode = 'raw 06 0x3f 01 0x08 01 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00'
rsp_Get_AuthCode = '35 57 36 65 b9 98 5f cd 14 97 1b 11 9c 66 b9 50'
cmd_Set_Channel_Access = 'raw 0x06 0x40 0x01 0x30 0x04'
cmd_Get_Channel_Access = 'raw 0x06 0x41 0x01 0x40'
cmd_Get_Channel_Info = 'raw 0x06 0x42 0x08'
rsp_Get_Channel_Info = '08 60 1c 00 f2 1b 00 00 00'
cmd_Set_User_Access = 'raw 0x06 0x43 0xb1 0x01 0x04'
cmd_Get_User_Access = 'raw 0x06 0x44 0x01 0x01'
cmd_Set_User_name = "raw 0x06 0x45 0x03 0x61 0x62 0x63 0x64 0x65 00 00 00 00 00 00 00 00 00 00 00"
cmd_Get_User_name = "raw 0x06 0x46 0x01"
rsp_cmd_Get_User_name = "72 6f 6f 74 00 00 00 00 00 00 00 00 00 00 00 00"
# Password set: AaBb00000000000
cmd_Set_User_Password = \
    'raw 0x06 0x47 0x03 0x02 0x41 0x61 0x42 0x62 0x30 0x30 0x30 0x30 0x30 0x30 0x30 0x30 0x30 0x30 0x30 0x30'
cmd_Get_Payload_Activation_Status = 'raw 06 0x4a 01'
rsp_Get_Payload_Activation_Status = '01 00 00'
cmd_Get_Payload_Instance_Info = 'raw 06 0x4b 01 01'
rsp_Get_Payload_Instance_Info = '00 00 00 00 00 00 00 00 00 00 00 00'
cmd_Set_user_Payload_Access = 'raw 06 0x4c 0x01 02 02 00 00 00'
cmd_Get_user_Payload_Access = 'raw 06 0x4d 0x01 02'
rsp_Get_user_Payload_Access = '02 00 00 00'
cmd_Get_channel_Payload_support = 'raw 06 0x4e 0x01'
rsp_Get_channel_Payload_support = '03 00 00 00 00 00 00 00'
cmd_Get_channel_Payload_Version = 'raw 06 0x4f 0x01 00'
rsp_Get_channel_Payload_Version = '10'
cmd_Master_Write_Read = 'raw 0x06 0x52 0x03 0xc2 0x01'
rsp_Master_Write_Read = '08 c0 00 00 40 80 c0 01 01 40 80 c0 02 01 41 80 c0'
cmd_Get_Channel_Cipher_Suites = 'raw 0x06 0x54 0x01 0x00 0x80'
cmd_Set_Channel_Security_Keys_56h = 'raw 06 0x56 0x08 00 00 01 01 01 01'
rsp_Set_Channel_Security_Keys = '02 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00'
cmd_Get_Chassis_Capabilities = "raw 00 00"
cmd_Get_Chassis_Status = "raw 00 01"
rsp_Get_Chassis_Status = "41 00 70 00"
cmd_Get_Chassis_Control_Power_Down = "raw 00 02 00"
cmd_Get_Chassis_Control_Power_Up = "raw 00 02 01"
cmd_Get_Chassis_Control_Power_Cycle = "raw 00 02 02"
cmd_Get_Chassis_Control_Soft_Shutdown = "raw 00 02 05"
cmd_Get_Chassis_Chassis_Identify = "raw 00 04 00 01"
cmd_Set_Power_Restore_policy_Power_off = "raw 00 06 00"
cmd_Set_Power_Restore_Prior_State = "raw 00 06 01"
cmd_Set_Power_Restore_policy_Power_Up = "raw 00 06 02"
cmd_Set_Power_Restore_policy_No_Change = "raw 00 06 03"
cmd_Get_System_Restart_Cause = 'raw 00 07'
rsp_Get_System_Restart_Cause = '00 08'
cmd_1_Set_System_Boot_Options = 'raw 00 0x08 00 01'
cmd_2_Set_System_Boot_Options = 'raw 00 0x08 05 0x80 0x18 00 00 00'
cmd_3_Set_System_Boot_Options = 'raw 00 0x08 00 00'
cmd_Get_System_Boot_Options = 'raw 00 0x09 05 00 00'
cmd_rsp_Get_System_Boot_Options = '01 05 00 00 00 00 00'
cmd_Set_Front_Panel_Button_Enables = 'raw 00 0xa 01'
cmd_Set_Power_Cycle_Interval = 'raw 00 0x0b 00'
cmd_default_Set_System_Boot_Options = 'raw 00 0x08 05 00 00 00 00 00'
cmd_rsp_default_Get_System_Boot_Options = '01 05 00 00 00 00 00'
cmd_Get_POH_Counter = 'raw 00 0xf'
cmd_Set_Event_Receiver = 'raw 04 00 0x20 00'
cmd_Get_Event_Receiver = 'raw 04 01'
cmd_Platform_Event_Message = 'raw 04 02 0 0 0 0 0 0'
cmd_Get_PEF_Capabilities = 'raw 04 0x10'
rsp_Get_PEF_Capabilities = '51 3f 28'
cmd_Disable_postpone_timer = 'raw 04 0x11 00'
rsp_Disable_postpone_timer = '00'
cmd_arm_timer = 'raw 04 0x11 01'
rsp_arm_timer = '01'
cmd_get_present_countdown_value = 'raw 04 0x11 0xff'
rsp_get_present_countdown_value = '00'
cmd_Set_PEF_Capabilities_1 = 'raw 04 0x12 00 01'
cmd_Set_PEF_Capabilities_2 = 'raw 04 0x12 01 0x0f'
cmd_Set_PEF_Capabilities_3 = 'raw 04 0x12 02 0x3f'
cmd_Set_PEF_Capabilities_4 = 'raw 04 0x12 06 0x10 0x80 01 01 01 0xFF 0xFF 0xFF 0x02 0xFF 0xFF 0xFF 00 0xFF 00 ' \
                             '00 0xFF 00 00 0xFF 00'
cmd_Set_PEF_Capabilities_5 = 'raw 04 0x12 0x09 01 0x18 0x11 00'
cmd_Set_PEF_Capabilities_6 = 'raw 04 0x12 00 00'
cmd_Get_PEF_Configuration_Parameters_1 = 'raw 04 0x13 00 00 00'
rsp_Get_PEF_Configuration_Parameters_1 = '11 00'
cmd_Get_PEF_Configuration_Parameters_2 = 'raw 04 0x13 01 00 00'
rsp_Get_PEF_Configuration_Parameters_2 = '11 0f'
cmd_Get_PEF_Configuration_Parameters_3 = 'raw 04 0x13 02 00 00'
rsp_Get_PEF_Configuration_Parameters_3 = '11 3f'
cmd_Set_Last_Processed_Event_ID = 'raw 04 0x14 01 1 0'
cmd_Get_Last_Processed_Event_ID = 'raw 04 0x15'
cmd_Alert_Immediate = 'raw 04 0x16 01 0 0x80'
cmd_PET_Acknowledge = 'raw 04 0x17'
cmd_Set_Sensor_Hysteresis = 'raw 04 0x24 01 0xff 00 00'
cmd_Get_Sensor_Hysteresis = 'raw 04 0x25 01 0xff'
rsp_Get_Sensor_Hysteresis = '00 00'
cmd_Set_Sensor_Threshold_1 = 'raw 04 0x26 01 0x10 00 00 00 00 32 00'  # (set senor 01 upper critical threshold value 50)
cmd_Set_Sensor_Threshold_2 = 'raw 04 0x26 01 0x08 00 00 00 28 00 00'  # (set senor 01 upper non-critical threshold value 40))
cmd_Set_Sensor_Threshold_3 = 'raw 04 26 01 02 00 08 00 00 00 00'  # (set senor 01 lower critical threshold value 10)
cmd_Set_Sensor_Threshold_4 = 'raw 04 26 01 01 14 00 00 00 00 00'  # (set senor 01 lower critical threshold value 20)
cmd_Get_Sensor_Threshold = 'raw 0x04 0x27 0x01'
cmd_Set_Sensor_Event_Enable = 'raw 0x04 0x28 0x01 0xc0 0x80 0x02 0x80 0x02'
cmd_Get_Sensor_Event_Enable = 'raw 0x04 0x29 0x01'
cmd_Re_arm_Sensor_Event = 'raw 04 0x2a 01 00'
cmd_Get_Sensor_Event_Status = 'raw 04 0x2b 01'
rsp_Get_Sensor_Event_Status = '80 00 00 00 00'
cmd_Get_Sensor_Reading = 'raw 04 0x2d 01'
cmd_Get_FRU_Inventory_Area_Info = 'raw 0x0a 0x10 00'
rsp_cmd_Get_FRU_Inventory = '00 06 00'
cmd_Write_FRU_Inventory_Area_Info = 'raw 0x0a 0x12 02 00 00 01 02 03 04 05 06 07 0x08 0x09 0x0a 0x0b 0x0c 0x0d 0x0e 0x0f'
rsp_cmd_Write_FRU_Inventory_Area_Info = '0f'
cmd_Get_SDR_Repository_Info = 'raw 0x0a 0x20'
rsp_Get_SDR_Repository_Info = '51 4c 00 ff ff 94 60 32 64 ff ff ff ff 83'
cmd_Get_SDR_Repository_Allocation_Info = 'raw 0x0a 0x21'
rsp_Get_SDR_Repository_Allocation_Info = '00 00 4c 00 00 00 00 00 01'
cmd_Reserve_SDR_Repository = 'raw 0x0a 0x22'
cmd_Get_SDR = 'raw 0x0a 0x23 00 00 00 00 00 0x01'
rsp_cmd_Get_SDR = '01 00 00'
cmd_Partial_Add_SDR = 'raw 0x0a 0x25 00 01 00 00 00 00 01 02 03 04'
cmd_Delete_SDR = 'raw 0x0a 0x26 00 00 00 01'
cmd_Clear_SDR_Repository = 'raw 0x0a 0x27 00 00 0x43 0x4c 0x52 0xaa'
cmd_Enter_SDR_Repository_Update_Mode = 'raw 0x0a 0x2a'
cmd_Exit_SDR_Repository_Update_Mode = 'raw 0x0a 0x2b'
cmd_Run_Initialization_Agent = 'raw 0x0a 0x2c 01'
cmd_Get_SEL_Info = 'raw 0x0a 0x40'
rsp_Get_SEL_Info = '51 /w/w /w/w ff ff /w/w /w/w /w/w /w/w /w/w /w/w /w/w /w/w 02'
cmd_Get_SEL_Allocation_Info = 'raw 0x0a 0x41'
cmd_Reserve_SEL = 'raw 0x0a 0x42'
cmd_Add_SEL_Entry = "raw 0x0a 0x44 00 04 02 f3 02 34 56 01 80 04 12 00 6f 05 00 00"
cmd_Clear_SEL = 'sel clear'
cmd_Get_SEL_Time = "raw 0x0a 0x48"
cmd_Set_SEL_Time = "raw 0x0a 0x49 00 00 00 00"
cmd_Get_SEL_Time_UTC_Offset = 'raw 28 5c'
cmd_Set_SEL_Time_UTC_Offset = 'raw 0x0a 0x5d 0xff 0x07'
cmd_ipmitool_lan_print_1 = 'lan print 1'
cmd_ipmitool_lan_print_2 = 'lan print 2'
bmc_lan_1_info_dhcp = {
    'MAC Address': 'b4:db:91:e1:7c:4c',
    'IP Address': '10.10.10.41',
    'IP Address Source': 'DHCP Address',
    'Subnet Mask': '255.255.255.0',
    # 'Default Gateway IP': '10.204.125.1',
    '802.1q VLAN ID': 'Disabled'
}
bmc_lan_2_info_dhcp = {
    'MAC Address': 'b4:db:91:e1:7c:4d',
    'IP Address': '10.10.10.37',
    'IP Address Source': 'DHCP Address',
    'Subnet Mask': '255.255.255.0',
    # 'Default Gateway IP': '10.204.125.1',
    '802.1q VLAN ID': 'Disabled'
}
bmc_lan_1_info_static = {
    'MAC Address': 'b4:db:91:d0:23:92',
    'IP Address': '192.168.10.10',
    'IP Address Source': 'Static Address',
    'Subnet Mask': '255.255.255.0',
    # 'Default Gateway IP': '10.204.125.1',
    '802.1q VLAN ID': 'Disabled'
}
bmc_lan_2_info_static = {
    'MAC Address': 'b4:db:91:d0:23:93',
    'IP Address': '192.168.10.20',
    'IP Address Source': 'Static Address',
    'Subnet Mask': '255.255.255.0',
    # 'Default Gateway IP': '0.0.0.0',
    '802.1q VLAN ID': 'Disabled'
}
bmc_ipv4_ip_lan1 = '10.10.10.41'
bmc_ipv4_ip_lan2 = '10.10.10.37'

cmd_Get_Message = 'raw 0x06 0x33'
cmd_Send_Message = 'raw 0x06 0x34'
cmd_Read_Event_Message_Buffer = 'raw 0x06 0x35'
rsp_Read_Event_Message_Buffer = '55 55 c0 41 a7 00 00 00 00 00 3a ff 00 ff ff ff'
cmd_Set_bmc_load_default = 'raw 0x32 0x66'
cmd_get_self_test_result = 'raw 0x06 0x04'
rsp_self_test = '55 00'
cmd_Activate_Session = 'raw 0x06 0x3A'
cmd_Close_Session = 'raw 0x06 0x3C'
cmd_Activate_Payload = 'raw 0x06 0x48 0x01 0x01 0xe0 0x00 0x00 0x00'
cmd_Deactivate_Payload = 'raw 0x06 0x49 0x01 0x01 0x00 0x00 0x00 0x00'
cmd_Set_Channel_Security_Keys_55h = 'raw 0x06 0x55'
rsp_Get_Chassis_Status_Off = 'Chassis Power is off'
rsp_Get_Chassis_Status_On = 'Chassis Power is on'
cmd_Chassis_Identify = 'raw 00 04 00 01'
cmd_Set_Power_Restore_policy_00 = 'raw 00 06 00'
cmd_Set_Power_Restore_policy_01 = 'raw 00 06 01'
cmd_Set_Power_Restore_policy_02 = 'raw 00 06 02'
cmd_Set_Power_Restore_policy_03 = 'raw 00 06 03'
# rsp_Set_Power_Restore_policy = '07'
ping_timeout = '180'
BMC_lan_print_1_ip_status = 'Static'
BMC_lan_print_1_ip_address = '192.168.10.10'
chassis_type_output = 'Main Server Chassis'
fru_print = {
    'FRU Device Description': 'Builtin FRU Device (ID 0)',
    'Product Manufacturer': 'CELESTICA-CTH',
    'Product Name': 'Artemis',
    'Product Version': 'DVT',
    'Product Serial': '0987654321098765ABCDEFGHIJKLMNOP',
    # 'FRU Device Description1: 'UNKNOWN (ID 219)',
    # 'Product Serial': 'IIUT2304003242'
    'Product Part Number': 'Product-Part/Model-1'

}
fru_print_id0 = {
    'FRU Device Description': 'Builtin FRU Device (ID 0)',
    'Chassis Type': 'Rack Mount Chassis',
    'Chassis Part Number': 'R4038-F9001-01',
    'Chassis Serial': 'Chassis-Serial-Number-0123456789',
    'Chassis Extra': 'Chassis-Product-Name',
    'Board Mfg': 'CELESTICA-CTH',
    'Board Product': 'Artemis BMC',
    'Board Serial': 'R4038-G0009-02AT0223440054',
    'Board Part Number': 'R4038-G0009-02',
    'Board Extra': '01',
    'Product Manufacturer': 'CELESTICA-CTH',
    'Product Name': 'Artemis',
    'Product Part Number': 'Product-Part/Model-1',
    'Product Version': 'DVT',
    'Product Serial': '0987654321098765ABCDEFGHIJKLMNOP'
}
fru_print_id1 = {
    'FRU Device Description': 'UNKNOWN (ID 1)',
    'Chassis Type': 'Rack Mount Chassis',
    'Chassis Part Number': 'R4038-F9001-01',
    'Chassis Serial': 'Chassis-Serial-Number-0123456789',
    'Chassis Extra': 'Chassis-Product-Name',
    'Board Mfg': 'CELESTICA-CTH',
    'Board Product': 'Artemis FAN Tray',
    'Board Serial': 'R4038-G0005-02AT0123440021',
    'Board Part Number': 'R4038-G0005-02',
    'Board Extra': '01',
    'Product Manufacturer': 'CELESTICA-CTH',
    'Product Name': 'Artemis',
    'Product Part Number': 'Product-Part/Model-1',
    'Product Version': 'DVT',
    'Product Serial': '0987654321098765ABCDEFGHIJKLMNOP'
}
fru_print_id2 = {
    'FRU Device Description': 'UNKNOWN (ID 2)',
    'Chassis Type': 'Rack Mount Chassis',
    'Chassis Part Number': 'R4038-F9001-01',
    'Chassis Serial': 'Chassis-Serial-Number-0123456789',
    'Chassis Extra': 'Chassis-Product-Name',
    'Board Mfg': 'CELESTICA-CTH',
    'Board Product': 'Artemis FAN Tray',
    'Board Serial': 'R4038-G0005-02AT0123440013',
    'Board Part Number': 'R4038-G0005-02',
    'Board Extra': '01',
    'Product Manufacturer': 'CELESTICA-CTH',
    'Product Name': 'Artemis',
    'Product Part Number': 'Product-Part/Model-1',
    'Product Version': 'DVT',
    'Product Serial': '0987654321098765ABCDEFGHIJKLMNOP'
}
fru_print_id3 = {
    'FRU Device Description': 'UNKNOWN (ID 3)',
    'Chassis Type': 'Rack Mount Chassis',
    'Chassis Part Number': 'R4038-F9001-01',
    'Chassis Serial': 'Chassis-Serial-Number-0123456789',
    'Chassis Extra': 'Chassis-Product-Name',
    'Board Mfg': 'CELESTICA-CTH',
    'Board Product': 'Artemis MB',
    'Board Serial': 'G0001CTH302AT3B601E',
    'Board Part Number': 'R4038-G0001-03',
    'Board Extra': '01',
    'Product Manufacturer': 'CELESTICA-CTH',
    'Product Name': 'Artemis',
    'Product Part Number': 'Product-Part/Model-1',
    'Product Version': 'DVT',
    'Product Serial': '0987654321098765ABCDEFGHIJKLMNOP'
}
fru_print_id4 = {
    'FRU Device Description': 'UNKNOWN (ID 4)',
    'Chassis Type': 'Rack Mount Chassis',
    'Chassis Part Number': 'R4038-F9001-01',
    'Chassis Serial': 'Chassis-Serial-Number-0123456789',
    'Chassis Extra': 'Chassis-Product-Name',
    'Board Mfg': 'CELESTICA-CTH',
    'Board Product': 'Artemis Midplane',
    'Board Serial': 'R4038-G0003-02AT0223440014',
    'Board Part Number': 'R4038-G0003-02',
    'Board Extra': '01',
    'Product Manufacturer': 'CELESTICA-CTH',
    'Product Name': 'Artemis',
    'Product Part Number': 'Product-Part/Model-1',
    'Product Version': 'DVT',
    'Product Serial': '0987654321098765ABCDEFGHIJKLMNOP'
}
fru_print_id5 = {
    'FRU Device Description': 'UNKNOWN (ID 5)',
    'Chassis Type': 'Rack Mount Chassis',
    'Chassis Part Number': 'R4038-F9001-01',
    'Chassis Serial': 'Chassis-Serial-Number-0123456789',
    'Chassis Extra': 'Chassis-Product-Name',
    'Board Mfg': 'CELESTICA-CTH',
    'Board Product': 'Artemis Midplane',
    'Board Serial': 'R4038-G0003-02AT0223440014',
    'Board Part Number': 'R4038-G0003-02',
    'Board Extra': '01',
    'Product Manufacturer': 'CELESTICA-CTH',
    'Product Name': 'Artemis',
    'Product Part Number': 'Product-Part/Model-1',
    'Product Version': 'DVT',
    'Product Serial': '0987654321098765ABCDEFGHIJKLMNOP'
}
fru_print_id6 = {
    'FRU Device Description': 'UNKNOWN (ID 89)',
    'Product Manufacturer': 'DELTA',
    'Product Name': 'TDPS2400HB A',
    'Product Part Number': 'TDPS2400HB A',
    'Product Version': '00F',
    'Product Serial': 'IIUT2317003418'
}
fru_print_id7 = {
    'FRU Device Description': 'UNKNOWN (ID 219)',
    'Product Manufacturer': 'DELTA',
    'Product Name': 'TDPS2400HB A',
    'Product Part Number': 'TDPS2400HB A',
    'Product Version': '00F',
    'Product Serial': 'IIUT2317003450'
}
true_value = True
sensor_threshold = '1026.000  | 2052.000  | 25992.000 | 28956.000'
error_messages_sel_list = 'error,fault,fail,warning,Critical,Non-critical'
error_messages_sensor_list = 'cr,nr,nc,lcr,lnr,failed,abnormal,fault'
FRUREAD_CYCLES = 5
Power_Reset_SELF_CYCLES = 2
Power_Reset_CYCLES = 2
Power_CYCLE_CYCLES = 2
CPLD_version_major = '13'
CPLD_version_minor = '20'
cmd_set_led_success = 'Wrote 2 bytes to I2C device C2h'
cmd_system_GUID_to_VPD = 'raw 0x3a 0x47 0x1 0x1 0x2 0x3 0x4 0x5 0x6 0x7 0x1 0x1 0x2 0x3 0x4 0x5 0x6 0x7'
rsp_cmd_system_GUID_to_VPD = 'System GUID   : 01010203040506070101020304050607'
set_boot_device = 'raw 0x00 0x08 0x03 0x1f'
set_boot_device_once = 'raw 0x00 0x08 0x05 0xA0 0x18 0x00 0x00 0x00'
set_boot_device_persistent = 'raw 0x00 0x08 0x05 0xE0 0x18 0x00 0x00 0x00'
Get_the_boot_1 = 'raw 0x00 0x09 0x03 0x00 0x00'
Get_the_boot_2 = 'raw 0x00 0x09 0x05 0x00 0x00'
rsp_the_boot_once_1 = '01 03 1f'
rsp_the_boot_once_2 = '01 05 a0 18 00 00 00'
rsp_the_boot_persistent_1 = '01 03 1f'
rsp_the_boot_persistent_2 = '01 05 e0 18 00 00 00'
set_BIOS_Flash_Switch_Pri = 'raw 0x3a 0x24 0x01 0x38 0x00 0x00'
set_BIOS_Flash_Switch_Sec = 'raw 0x3a 0x24 0x01 0x38 0x01 0x00'
Get_BIOS_Flash_Switch = 'raw 0x3a 0x24 0x00 0x38'  # ((Primay:0x00 Secondary:0x01))
cmd_Get_host_POST_Code = oem_cmd_list['get_post_code']
rsp_Get_host_POST_Code = '15 14 15 14 15 14 15 14 15 14 15 14 15 14 15 14 15 14 15 14 15 14 15 14 15 14 15 14 15 14 15 14\
 15 14 15 14 15 14 15 14 15 14 15 14 15 14 15 14 15 14 15 14 15 14 15 14 15 14 15 14 15 14 15 14\
 15 14 15 14 15 14 14 15 14 15 14 15 14 15 14 15 14 15 14 15 14 15 14 15 14 14 14 15 14 15 14 14\
 15 14 15 14 15 14 15 14 15 14 15 14 15 14 15 14 15 14 15 14 15 14 14 14 14 15 14 15 14 15 14 15\
 14 15 14 15 14 15 14 15 14 15 14 15 14 15 14 15 14 15 14 15 14 15 14 15 14 15 14 15 02 57 56 3a\
 3b 41 73 77 70 5d dd 00 14 78 29 5d dd 00 62 e2 00 06 86 00 2a 94 ad aa aa 00 2a aa 00 2a aa 00\
 2a aa 00 2a aa 00 2a aa 00 2a aa 00 2a aa 00 2a aa 00 2a aa 00 2a aa 00 2a aa 00 2a aa 00 2a aa\
 00 2a aa 00 2a aa 00 2a aa 00 2a aa 00 2a aa 00 2a aa 00 2a aa 00 2a aa 00 2b 2c af b1 b1 aa 00'

resource_service_root = "/redfish/v1"
####CONSR-OBMC-RDFT-0160-0001
resource_JSONSchema_AccountService = "/redfish/v1/JsonSchemas/AccountService"
odata_type_value_AccountService = "#JsonSchemaFile.v1_0_2.JsonSchemaFile"
Language_AccountService = "['en']"
Location_AccountService = "[{'Language': 'en', 'PublicationUri': 'http://redfish.dmtf.org/schemas/v1/AccountService.json', 'Uri': '/redfish/v1/JsonSchemas/AccountService/AccountService.json'}]"
Description_AccountService = "AccountService Schema File Location"
Id_AccountService = "AccountService"
Languages_odatacount_AccountService = "1"
Location_odatacount_AccountService = "1"
Name_AccountService = "AccountService Schema File"
Schema_AccountService = "#AccountService.AccountService"
####CONSR-OBMC-RDFT-0162-0001
resource_JSONSchema_AggregationService = "/redfish/v1/JsonSchemas/AggregationService"
odata_type_value_AggregationService = "#JsonSchemaFile.v1_0_2.JsonSchemaFile"
Language_AggregationService = "['en']"
Location_AggregationService = "[{'Language': 'en', 'PublicationUri': 'http://redfish.dmtf.org/schemas/v1/AggregationService.json', 'Uri': '/redfish/v1/JsonSchemas/AggregationService/AggregationService.json'}]"
Description_AggregationService = "AggregationService Schema File Location"
Id_AggregationService = "AggregationService"
Languages_odatacount_AggregationService = "1"
Location_odatacount_AggregationService = "1"
Name_AggregationService = "AggregationService Schema File"
Schema_AggregationService = "#AggregationService.AggregationService"
####CONSR-OBMC-RDFT-0164-0001
resource_JSONSchema_AggregationSourceCollection = "/redfish/v1/JsonSchemas/AggregationSourceCollection"
odata_type_value_AggregationSourceCollection = "#JsonSchemaFile.v1_0_2.JsonSchemaFile"
Language_AggregationSourceCollection = "['en']"
Location_AggregationSourceCollection = "[{'Language': 'en', 'PublicationUri': 'http://redfish.dmtf.org/schemas/v1/AggregationSourceCollection.json', 'Uri': '/redfish/v1/JsonSchemas/AggregationSourceCollection/AggregationSourceCollection.json'}]"
Description_AggregationSourceCollection = "AggregationSourceCollection Schema File Location"
Id_AggregationSourceCollection = "AggregationSourceCollection"
Languages_odatacount_AggregationSourceCollection = "1"
Location_odatacount_AggregationSourceCollection = "1"
Name_AggregationSourceCollection = "AggregationSourceCollection Schema File"
Schema_AggregationSourceCollection = "#AggregationSourceCollection.AggregationSourceCollection"
####CONSR-OBMC-RDFT-0166-0001
resource_JSONSchema_AttributeRegistry = "/redfish/v1/JsonSchemas/AttributeRegistry"
odata_type_value_AttributeRegistry = "#JsonSchemaFile.v1_0_2.JsonSchemaFile"
Language_AttributeRegistry = "['en']"
Location_AttributeRegistry = "[{'Language': 'en', 'PublicationUri': 'http://redfish.dmtf.org/schemas/v1/AttributeRegistry.json', 'Uri': '/redfish/v1/JsonSchemas/AttributeRegistry/AttributeRegistry.json'}]"
Description_AttributeRegistry = "AttributeRegistry Schema File Location"
Id_AttributeRegistry = "AttributeRegistry"
Languages_odatacount_AttributeRegistry = "1"
Location_odatacount_AttributeRegistry = "1"
Name_AttributeRegistry = "AttributeRegistry Schema File"
Schema_AttributeRegistry = "#AttributeRegistry.AttributeRegistry"
####CONSR-OBMC-RDFT-0168-0001
resource_JSONSchema_Cable = "/redfish/v1/JsonSchemas/Cable"
odata_type_value_Cable = "#JsonSchemaFile.v1_0_2.JsonSchemaFile"
Language_Cable = "['en']"
Location_Cable = "[{'Language': 'en', 'PublicationUri': 'http://redfish.dmtf.org/schemas/v1/Cable.json', 'Uri': '/redfish/v1/JsonSchemas/Cable/Cable.json'}]"
Description_Cable = "Cable Schema File Location"
Id_Cable = "Cable"
Languages_odatacount_Cable = "1"
Location_odatacount_Cable = "1"
Name_Cable = "Cable Schema File"
Schema_Cable = "#Cable.Cable"
####CONSR-OBMC-RDFT-0170-0001
resource_JSONSchema_Certificate = "/redfish/v1/JsonSchemas/Certificate"
odata_type_value_Certificate = "#JsonSchemaFile.v1_0_2.JsonSchemaFile"
Language_Certificate = "['en']"
Location_Certificate = "[{'Language': 'en', 'PublicationUri': 'http://redfish.dmtf.org/schemas/v1/Certificate.json', 'Uri': '/redfish/v1/JsonSchemas/Certificate/Certificate.json'}]"
Description_Certificate = "Certificate Schema File Location"
Id_Certificate = "Certificate"
Languages_odatacount_Certificate = "1"
Location_odatacount_Certificate = "1"
Name_Certificate = "Certificate Schema File"
Schema_Certificate = "#Certificate.Certificate"
####CONSR-OBMC-RDFT-0172-0001
resource_JSONSchema_CertificateLocations = "/redfish/v1/JsonSchemas/CertificateLocations"
odata_type_value_CertificateLocations = "#JsonSchemaFile.v1_0_2.JsonSchemaFile"
Language_CertificateLocations = "['en']"
Location_CertificateLocations = "[{'Language': 'en', 'PublicationUri': 'http://redfish.dmtf.org/schemas/v1/CertificateLocations.json', 'Uri': '/redfish/v1/JsonSchemas/CertificateLocations/CertificateLocations.json'}]"
Description_CertificateLocations = "CertificateLocations Schema File Location"
Id_CertificateLocations = "CertificateLocations"
Languages_odatacount_CertificateLocations = "1"
Location_odatacount_CertificateLocations = "1"
Name_CertificateLocations = "CertificateLocations Schema File"
Schema_CertificateLocations = "#CertificateLocations.CertificateLocations"
####CONSR-OBMC-RDFT-0174-0001
resource_JSONSchema_Chassis = "/redfish/v1/JsonSchemas/Chassis"
odata_type_value_Chassis = "#JsonSchemaFile.v1_0_2.JsonSchemaFile"
Language_Chassis = "['en']"
Location_Chassis = "[{'Language': 'en', 'PublicationUri': 'http://redfish.dmtf.org/schemas/v1/Chassis.json', 'Uri': '/redfish/v1/JsonSchemas/Chassis/Chassis.json'}]"
Description_Chassis = "Chassis Schema File Location"
Id_Chassis = "Chassis"
Languages_odatacount_Chassis = "1"
Location_odatacount_Chassis = "1"
Name_Chassis = "Chassis Schema File"
Schema_Chassis = "#Chassis.Chassis"
####CONSR-OBMC-RDFT-0176-0001
resource_JSONSchema_ComponentIntegrity = "/redfish/v1/JsonSchemas/ComponentIntegrity"
odata_type_value_ComponentIntegrity = "#JsonSchemaFile.v1_0_2.JsonSchemaFile"
Language_ComponentIntegrity = "['en']"
Location_ComponentIntegrity = "[{'Language': 'en', 'PublicationUri': 'http://redfish.dmtf.org/schemas/v1/ComponentIntegrity.json', 'Uri': '/redfish/v1/JsonSchemas/ComponentIntegrity/ComponentIntegrity.json'}]"
Description_ComponentIntegrity = "ComponentIntegrity Schema File Location"
Id_ComponentIntegrity = "ComponentIntegrity"
Languages_odatacount_ComponentIntegrity = "1"
Location_odatacount_ComponentIntegrity = "1"
Name_ComponentIntegrity = "ComponentIntegrity Schema File"
Schema_ComponentIntegrity = "#ComponentIntegrity.ComponentIntegrity"
####CONSR-OBMC-RDFT-0178-0001
resource_JSONSchema_ComputerSystem = "/redfish/v1/JsonSchemas/ComputerSystem"
odata_type_value_ComputerSystem = "#JsonSchemaFile.v1_0_2.JsonSchemaFile"
Language_ComputerSystem = "['en']"
Location_ComputerSystem = "[{'Language': 'en', 'PublicationUri': 'http://redfish.dmtf.org/schemas/v1/ComputerSystem.json', 'Uri': '/redfish/v1/JsonSchemas/ComputerSystem/ComputerSystem.json'}]"
Description_ComputerSystem = "ComputerSystem Schema File Location"
Id_ComputerSystem = "ComputerSystem"
Languages_odatacount_ComputerSystem = "1"
Location_odatacount_ComputerSystem = "1"
Name_ComputerSystem = "ComputerSystem Schema File"
Schema_ComputerSystem = "#ComputerSystem.ComputerSystem"
####CONSR-OBMC-RDFT-0180-0001
resource_JSONSchema_Drive = "/redfish/v1/JsonSchemas/Drive"
odata_type_value_Drive = "#JsonSchemaFile.v1_0_2.JsonSchemaFile"
Language_Drive = "['en']"
Location_Drive = "[{'Language': 'en', 'PublicationUri': 'http://redfish.dmtf.org/schemas/v1/Drive.json', 'Uri': '/redfish/v1/JsonSchemas/Drive/Drive.json'}]"
Description_Drive = "Drive Schema File Location"
Id_Drive = "Drive"
Languages_odatacount_Drive = "1"
Location_odatacount_Drive = "1"
Name_Drive = "Drive Schema File"
Schema_Drive = "#Drive.Drive"
####CONSR-OBMC-RDFT-0182-0001
resource_JSONSchema_EnvironmentMetrics = "/redfish/v1/JsonSchemas/EnvironmentMetrics"
odata_type_value_EnvironmentMetrics = "#JsonSchemaFile.v1_0_2.JsonSchemaFile"
Language_EnvironmentMetrics = "['en']"
Location_EnvironmentMetrics = "[{'Language': 'en', 'PublicationUri': 'http://redfish.dmtf.org/schemas/v1/EnvironmentMetrics.json', 'Uri': '/redfish/v1/JsonSchemas/EnvironmentMetrics/EnvironmentMetrics.json'}]"
Description_EnvironmentMetrics = "EnvironmentMetrics Schema File Location"
Id_EnvironmentMetrics = "EnvironmentMetrics"
Languages_odatacount_EnvironmentMetrics = "1"
Location_odatacount_EnvironmentMetrics = "1"
Name_EnvironmentMetrics = "EnvironmentMetrics Schema File"
Schema_EnvironmentMetrics = "#EnvironmentMetrics.EnvironmentMetrics"
####CONSR-OBMC-RDFT-0184-0001
resource_JSONSchema_EthernetInterfaceCollection = "/redfish/v1/JsonSchemas/EthernetInterfaceCollection"
odata_type_value_EthernetInterfaceCollection = "#JsonSchemaFile.v1_0_2.JsonSchemaFile"
Language_EthernetInterfaceCollection = "['en']"
Location_EthernetInterfaceCollection = "[{'Language': 'en', 'PublicationUri': 'http://redfish.dmtf.org/schemas/v1/EthernetInterfaceCollection.json', 'Uri': '/redfish/v1/JsonSchemas/EthernetInterfaceCollection/EthernetInterfaceCollection.json'}]"
Description_EthernetInterfaceCollection = "EthernetInterfaceCollection Schema File Location"
Id_EthernetInterfaceCollection = "EthernetInterfaceCollection"
Languages_odatacount_EthernetInterfaceCollection = "1"
Location_odatacount_EthernetInterfaceCollection = "1"
Name_EthernetInterfaceCollection = "EthernetInterfaceCollection Schema File"
Schema_EthernetInterfaceCollection = "#EthernetInterfaceCollection.EthernetInterfaceCollection"
####CONSR-OBMC-RDFT-0186-0001
resource_JSONSchema_EventDestination = "/redfish/v1/JsonSchemas/EventDestination"
odata_type_value_EventDestination = "#JsonSchemaFile.v1_0_2.JsonSchemaFile"
Language_EventDestination = "['en']"
Location_EventDestination = "[{'Language': 'en', 'PublicationUri': 'http://redfish.dmtf.org/schemas/v1/EventDestination.json', 'Uri': '/redfish/v1/JsonSchemas/EventDestination/EventDestination.json'}]"
Description_EventDestination = "EventDestination Schema File Location"
Id_EventDestination = "EventDestination"
Languages_odatacount_EventDestination = "1"
Location_odatacount_EventDestination = "1"
Name_EventDestination = "EventDestination Schema File"
Schema_EventDestination = "#EventDestination.EventDestination"
####CONSR-OBMC-RDFT-0188-0001
resource_JSONSchema_EventService = "/redfish/v1/JsonSchemas/EventService"
odata_type_value_EventService = "#JsonSchemaFile.v1_0_2.JsonSchemaFile"
Language_EventService = "['en']"
Location_EventService = "[{'Language': 'en', 'PublicationUri': 'http://redfish.dmtf.org/schemas/v1/EventService.json', 'Uri': '/redfish/v1/JsonSchemas/EventService/EventService.json'}]"
Description_EventService = "EventService Schema File Location"
Id_EventService = "EventService"
Languages_odatacount_EventService = "1"
Location_odatacount_EventService = "1"
Name_EventService = "EventService Schema File"
Schema_EventService = "#EventService.EventService"
####CONSR-OBMC-RDFT-0190-0001
resource_JSONSchema_FabricAdapterCollection = "/redfish/v1/JsonSchemas/FabricAdapterCollection"
odata_type_value_FabricAdapterCollection = "#JsonSchemaFile.v1_0_2.JsonSchemaFile"
Language_FabricAdapterCollection = "['en']"
Location_FabricAdapterCollection = "[{'Language': 'en', 'PublicationUri': 'http://redfish.dmtf.org/schemas/v1/FabricAdapterCollection.json', 'Uri': '/redfish/v1/JsonSchemas/FabricAdapterCollection/FabricAdapterCollection.json'}]"
Description_FabricAdapterCollection = "FabricAdapterCollection Schema File Location"
Id_FabricAdapterCollection = "FabricAdapterCollection"
Languages_odatacount_FabricAdapterCollection = "1"
Location_odatacount_FabricAdapterCollection = "1"
Name_FabricAdapterCollection = "FabricAdapterCollection Schema File"
Schema_FabricAdapterCollection = "#FabricAdapterCollection.FabricAdapterCollection"
####CONSR-OBMC-RDFT-0192-0001
resource_JSONSchema_FanCollection = "/redfish/v1/JsonSchemas/FanCollection"
odata_type_value_FanCollection = "#JsonSchemaFile.v1_0_2.JsonSchemaFile"
Language_FanCollection = "['en']"
Location_FanCollection = "[{'Language': 'en', 'PublicationUri': 'http://redfish.dmtf.org/schemas/v1/FanCollection.json', 'Uri': '/redfish/v1/JsonSchemas/FanCollection/FanCollection.json'}]"
Description_FanCollection = "FanCollection Schema File Location"
Id_FanCollection = "FanCollection"
Languages_odatacount_FanCollection = "1"
Location_odatacount_FanCollection = "1"
Name_FanCollection = "FanCollection Schema File"
Schema_FanCollection = "#FanCollection.FanCollection"
####CONSR-OBMC-RDFT-0194-0001
resource_JSONSchema_JsonSchemaFile = "/redfish/v1/JsonSchemas/JsonSchemaFile"
odata_type_value_JsonSchemaFile = "#JsonSchemaFile.v1_0_2.JsonSchemaFile"
Language_JsonSchemaFile = "['en']"
Location_JsonSchemaFile = "[{'Language': 'en', 'PublicationUri': 'http://redfish.dmtf.org/schemas/v1/JsonSchemaFile.json', 'Uri': '/redfish/v1/JsonSchemas/JsonSchemaFile/JsonSchemaFile.json'}]"
Description_JsonSchemaFile = "JsonSchemaFile Schema File Location"
Id_JsonSchemaFile = "JsonSchemaFile"
Languages_odatacount_JsonSchemaFile = "1"
Location_odatacount_JsonSchemaFile = "1"
Name_JsonSchemaFile = "JsonSchemaFile Schema File"
Schema_JsonSchemaFile = "#JsonSchemaFile.JsonSchemaFile"
####CONSR-OBMC-RDFT-0196-0001
resource_JSONSchema_LogEntry = "/redfish/v1/JsonSchemas/LogEntry"
odata_type_value_LogEntry = "#JsonSchemaFile.v1_0_2.JsonSchemaFile"
Language_LogEntry = "['en']"
Location_LogEntry = "[{'Language': 'en', 'PublicationUri': 'http://redfish.dmtf.org/schemas/v1/LogEntry.json', 'Uri': '/redfish/v1/JsonSchemas/LogEntry/LogEntry.json'}]"
Description_LogEntry = "LogEntry Schema File Location"
Id_LogEntry = "LogEntry"
Languages_odatacount_LogEntry = "1"
Location_odatacount_LogEntry = "1"
Name_LogEntry = "LogEntry Schema File"
Schema_LogEntry = "#LogEntry.LogEntry"
####CONSR-OBMC-RDFT-0198-0001
resource_JSONSchema_LogService = "/redfish/v1/JsonSchemas/LogService"
odata_type_value_LogService = "#JsonSchemaFile.v1_0_2.JsonSchemaFile"
Language_LogService = "['en']"
Location_LogService = "[{'Language': 'en', 'PublicationUri': 'http://redfish.dmtf.org/schemas/v1/LogService.json', 'Uri': '/redfish/v1/JsonSchemas/LogService/LogService.json'}]"
Description_LogService = "LogService Schema File Location"
Id_LogService = "LogService"
Languages_odatacount_LogService = "1"
Location_odatacount_LogService = "1"
Name_LogService = "LogService Schema File"
Schema_LogService = "#LogService.LogService"
####CONSR-OBMC-RDFT-0200-0001
resource_JSONSchema_Manager = "/redfish/v1/JsonSchemas/Manager"
odata_type_value_Manager = "#JsonSchemaFile.v1_0_2.JsonSchemaFile"
Language_Manager = "['en']"
Location_Manager = "[{'Language': 'en', 'PublicationUri': 'http://redfish.dmtf.org/schemas/v1/Manager.json', 'Uri': '/redfish/v1/JsonSchemas/Manager/Manager.json'}]"
Description_Manager = "Manager Schema File Location"
Id_Manager = "Manager"
Languages_odatacount_Manager = "1"
Location_odatacount_Manager = "1"
Name_Manager = "Manager Schema File"
Schema_Manager = "#Manager.Manager"
####CONSR-OBMC-RDFT-0202-0001
resource_JSONSchema_ManagerAccountCollection = "/redfish/v1/JsonSchemas/ManagerAccountCollection"
odata_type_value_ManagerAccountCollection = "#JsonSchemaFile.v1_0_2.JsonSchemaFile"
Language_ManagerAccountCollection = "['en']"
Location_ManagerAccountCollection = "[{'Language': 'en', 'PublicationUri': 'http://redfish.dmtf.org/schemas/v1/ManagerAccountCollection.json', 'Uri': '/redfish/v1/JsonSchemas/ManagerAccountCollection/ManagerAccountCollection.json'}]"
Description_ManagerAccountCollection = "ManagerAccountCollection Schema File Location"
Id_ManagerAccountCollection = "ManagerAccountCollection"
Languages_odatacount_ManagerAccountCollection = "1"
Location_odatacount_ManagerAccountCollection = "1"
Name_ManagerAccountCollection = "ManagerAccountCollection Schema File"
Schema_ManagerAccountCollection = "#ManagerAccountCollection.ManagerAccountCollection"
####CONSR-OBMC-RDFT-0204-0001
resource_JSONSchema_ManagerDiagnosticData = "/redfish/v1/JsonSchemas/ManagerDiagnosticData"
odata_type_value_ManagerDiagnosticData = "#JsonSchemaFile.v1_0_2.JsonSchemaFile"
Language_ManagerDiagnosticData = "['en']"
Location_ManagerDiagnosticData = "[{'Language': 'en', 'PublicationUri': 'http://redfish.dmtf.org/schemas/v1/ManagerDiagnosticData.json', 'Uri': '/redfish/v1/JsonSchemas/ManagerDiagnosticData/ManagerDiagnosticData.json'}]"
Description_ManagerDiagnosticData = "ManagerDiagnosticData Schema File Location"
Id_ManagerDiagnosticData = "ManagerDiagnosticData"
Languages_odatacount_ManagerDiagnosticData = "1"
Location_odatacount_ManagerDiagnosticData = "1"
Name_ManagerDiagnosticData = "ManagerDiagnosticData Schema File"
Schema_ManagerDiagnosticData = "#ManagerDiagnosticData.ManagerDiagnosticData"
####CONSR-OBMC-RDFT-0206-0001
resource_JSONSchema_Memory = "/redfish/v1/JsonSchemas/Memory"
odata_type_value_Memory = "#JsonSchemaFile.v1_0_2.JsonSchemaFile"
Language_Memory = "['en']"
Location_Memory = "[{'Language': 'en', 'PublicationUri': 'http://redfish.dmtf.org/schemas/v1/Memory.json', 'Uri': '/redfish/v1/JsonSchemas/Memory/Memory.json'}]"
Description_Memory = "Memory Schema File Location"
Id_Memory = "Memory"
Languages_odatacount_Memory = "1"
Location_odatacount_Memory = "1"
Name_Memory = "Memory Schema File"
Schema_Memory = "#Memory.Memory"
####CONSR-OBMC-RDFT-0208-0001
resource_JSONSchema_Message = "/redfish/v1/JsonSchemas/Message"
odata_type_value_Message = "#JsonSchemaFile.v1_0_2.JsonSchemaFile"
Language_Message = "['en']"
Location_Message = "[{'Language': 'en', 'PublicationUri': 'http://redfish.dmtf.org/schemas/v1/Message.json', 'Uri': '/redfish/v1/JsonSchemas/Message/Message.json'}]"
Description_Message = "Message Schema File Location"
Id_Message = "Message"
Languages_odatacount_Message = "1"
Location_odatacount_Message = "1"
Name_Message = "Message Schema File"
Schema_Message = "#Message.Message"
####CONSR-OBMC-RDFT-0210-0001
resource_JSONSchema_MessageRegistryCollection = "/redfish/v1/JsonSchemas/MessageRegistryCollection"
odata_type_value_MessageRegistryCollection = "#JsonSchemaFile.v1_0_2.JsonSchemaFile"
Language_MessageRegistryCollection = "['en']"
Location_MessageRegistryCollection = "[{'Language': 'en', 'PublicationUri': 'http://redfish.dmtf.org/schemas/v1/MessageRegistryCollection.json', 'Uri': '/redfish/v1/JsonSchemas/MessageRegistryCollection/MessageRegistryCollection.json'}]"
Description_MessageRegistryCollection = "MessageRegistryCollection Schema File Location"
Id_MessageRegistryCollection = "MessageRegistryCollection"
Languages_odatacount_MessageRegistryCollection = "1"
Location_odatacount_MessageRegistryCollection = "1"
Name_MessageRegistryCollection = "MessageRegistryCollection Schema File"
Schema_MessageRegistryCollection = "#MessageRegistryCollection.MessageRegistryCollection"
####CONSR-OBMC-RDFT-0212-0001
resource_JSONSchema_MessageRegistryCollection = "/redfish/v1/JsonSchemas/MessageRegistryCollection"
odata_type_value_MessageRegistryCollection = "#JsonSchemaFile.v1_0_2.JsonSchemaFile"
Language_MessageRegistryCollection = "['en']"
Location_MessageRegistryCollection = "[{'Language': 'en', 'PublicationUri': 'http://redfish.dmtf.org/schemas/v1/MessageRegistryCollection.json', 'Uri': '/redfish/v1/JsonSchemas/MessageRegistryCollection/MessageRegistryCollection.json'}]"
Description_MessageRegistryCollection = "MessageRegistryCollection Schema File Location"
Id_MessageRegistryCollection = "MessageRegistryCollection"
Languages_odatacount_MessageRegistryCollection = "1"
Location_odatacount_MessageRegistryCollection = "1"
Name_MessageRegistryCollection = "MessageRegistryCollection Schema File"
Schema_MessageRegistryCollection = "#MessageRegistryCollection.MessageRegistryCollection"
####CONSR-OBMC-RDFT-0214-0001
resource_JSONSchema_MetricDefinitionCollection = "/redfish/v1/JsonSchemas/MetricDefinitionCollection"
odata_type_value_MetricDefinitionCollection = "#JsonSchemaFile.v1_0_2.JsonSchemaFile"
Language_MetricDefinitionCollection = "['en']"
Location_MetricDefinitionCollection = "[{'Language': 'en', 'PublicationUri': 'http://redfish.dmtf.org/schemas/v1/MetricDefinitionCollection.json', 'Uri': '/redfish/v1/JsonSchemas/MetricDefinitionCollection/MetricDefinitionCollection.json'}]"
Description_MetricDefinitionCollection = "MetricDefinitionCollection Schema File Location"
Id_MetricDefinitionCollection = "MetricDefinitionCollection"
Languages_odatacount_MetricDefinitionCollection = "1"
Location_odatacount_MetricDefinitionCollection = "1"
Name_MetricDefinitionCollection = "MetricDefinitionCollection Schema File"
Schema_MetricDefinitionCollection = "#MetricDefinitionCollection.MetricDefinitionCollection"
####CONSR-OBMC-RDFT-0216-0001
resource_JSONSchema_MetricReportCollection = "/redfish/v1/JsonSchemas/MetricReportCollection"
odata_type_value_MetricReportCollection = "#JsonSchemaFile.v1_0_2.JsonSchemaFile"
Language_MetricReportCollection = "['en']"
Location_MetricReportCollection = "[{'Language': 'en', 'PublicationUri': 'http://redfish.dmtf.org/schemas/v1/MetricReportCollection.json', 'Uri': '/redfish/v1/JsonSchemas/MetricReportCollection/MetricReportCollection.json'}]"
Description_MetricReportCollection = "MetricReportCollection Schema File Location"
Id_MetricReportCollection = "MetricReportCollection"
Languages_odatacount_MetricReportCollection = "1"
Location_odatacount_MetricReportCollection = "1"
Name_MetricReportCollection = "MetricReportCollection Schema File"
Schema_MetricReportCollection = "#MetricReportCollection.MetricReportCollection"
####CONSR-OBMC-RDFT-0218-0001
resource_JSONSchema_MetricReportDefinitionCollection = "/redfish/v1/JsonSchemas/MetricReportDefinitionCollection"
odata_type_value_MetricReportDefinitionCollection = "#JsonSchemaFile.v1_0_2.JsonSchemaFile"
Language_MetricReportDefinitionCollection = "['en']"
Location_MetricReportDefinitionCollection = "[{'Language': 'en', 'PublicationUri': 'http://redfish.dmtf.org/schemas/v1/MetricReportDefinitionCollection.json', 'Uri': '/redfish/v1/JsonSchemas/MetricReportDefinitionCollection/MetricReportDefinitionCollection.json'}]"
Description_MetricReportDefinitionCollection = "MetricReportDefinitionCollection Schema File Location"
Id_MetricReportDefinitionCollection = "MetricReportDefinitionCollection"
Languages_odatacount_MetricReportDefinitionCollection = "1"
Location_odatacount_MetricReportDefinitionCollection = "1"
Name_MetricReportDefinitionCollection = "MetricReportDefinitionCollection Schema File"
Schema_MetricReportDefinitionCollection = "#MetricReportDefinitionCollection.MetricReportDefinitionCollection"
####CONSR-OBMC-RDFT-0220-0001
resource_JSONSchema_odata_v4 = "/redfish/v1/JsonSchemas/odata-v4"
odata_type_value_odata_v4 = "#JsonSchemaFile.v1_0_2.JsonSchemaFile"
Language_odata_v4 = "['en']"
Location_odata_v4 = "[{'Language': 'en', 'PublicationUri': 'http://redfish.dmtf.org/schemas/v1/odata-v4.json', 'Uri': '/redfish/v1/JsonSchemas/odata-v4/odata-v4.json'}]"
Description_odata_v4 = "odata-v4 Schema File Location"
Id_odata_v4 = "odata-v4"
Languages_odatacount_odata_v4 = "1"
Location_odatacount_odata_v4 = "1"
Name_odata_v4 = "odata-v4 Schema File"
Schema_odata_v4 = "#odata-v4.odata-v4"
####CONSR-OBMC-RDFT-0222-0001
resource_JSONSchema_OperatingConfigCollection = "/redfish/v1/JsonSchemas/OperatingConfigCollection"
odata_type_value_OperatingConfigCollection = "#JsonSchemaFile.v1_0_2.JsonSchemaFile"
Language_OperatingConfigCollection = "['en']"
Location_OperatingConfigCollection = "[{'Language': 'en', 'PublicationUri': 'http://redfish.dmtf.org/schemas/v1/OperatingConfigCollection.json', 'Uri': '/redfish/v1/JsonSchemas/OperatingConfigCollection/OperatingConfigCollection.json'}]"
Description_OperatingConfigCollection = "OperatingConfigCollection Schema File Location"
Id_OperatingConfigCollection = "OperatingConfigCollection"
Languages_odatacount_OperatingConfigCollection = "1"
Location_odatacount_OperatingConfigCollection = "1"
Name_OperatingConfigCollection = "OperatingConfigCollection Schema File"
Schema_OperatingConfigCollection = "#OperatingConfigCollection.OperatingConfigCollection"
####CONSR-OBMC-RDFT-0224-0001
resource_JSONSchema_PCIeDeviceCollection = "/redfish/v1/JsonSchemas/PCIeDeviceCollection"
odata_type_value_PCIeDeviceCollection = "#JsonSchemaFile.v1_0_2.JsonSchemaFile"
Language_PCIeDeviceCollection = "['en']"
Location_PCIeDeviceCollection = "[{'Language': 'en', 'PublicationUri': 'http://redfish.dmtf.org/schemas/v1/PCIeDeviceCollection.json', 'Uri': '/redfish/v1/JsonSchemas/PCIeDeviceCollection/PCIeDeviceCollection.json'}]"
Description_PCIeDeviceCollection = "PCIeDeviceCollection Schema File Location"
Id_PCIeDeviceCollection = "PCIeDeviceCollection"
Languages_odatacount_PCIeDeviceCollection = "1"
Location_odatacount_PCIeDeviceCollection = "1"
Name_PCIeDeviceCollection = "PCIeDeviceCollection Schema File"
Schema_PCIeDeviceCollection = "#PCIeDeviceCollection.PCIeDeviceCollection"
####CONSR-OBMC-RDFT-0226-0001
resource_JSONSchema_PCIeFunctionCollection = "/redfish/v1/JsonSchemas/PCIeFunctionCollection"
odata_type_value_PCIeFunctionCollection = "#JsonSchemaFile.v1_0_2.JsonSchemaFile"
Language_PCIeFunctionCollection = "['en']"
Location_PCIeFunctionCollection = "[{'Language': 'en', 'PublicationUri': 'http://redfish.dmtf.org/schemas/v1/PCIeFunctionCollection.json', 'Uri': '/redfish/v1/JsonSchemas/PCIeFunctionCollection/PCIeFunctionCollection.json'}]"
Description_PCIeFunctionCollection = "PCIeFunctionCollection Schema File Location"
Id_PCIeFunctionCollection = "PCIeFunctionCollection"
Languages_odatacount_PCIeFunctionCollection = "1"
Location_odatacount_PCIeFunctionCollection = "1"
Name_PCIeFunctionCollection = "PCIeFunctionCollection Schema File"
Schema_PCIeFunctionCollection = "#PCIeFunctionCollection.PCIeFunctionCollection"
####CONSR-OBMC-RDFT-0228-0001
resource_JSONSchema_PhysicalContext = "/redfish/v1/JsonSchemas/PhysicalContext"
odata_type_value_PhysicalContext = "#JsonSchemaFile.v1_0_2.JsonSchemaFile"
Language_PhysicalContext = "['en']"
Location_PhysicalContext = "[{'Language': 'en', 'PublicationUri': 'http://redfish.dmtf.org/schemas/v1/PhysicalContext.json', 'Uri': '/redfish/v1/JsonSchemas/PhysicalContext/PhysicalContext.json'}]"
Description_PhysicalContext = "PhysicalContext Schema File Location"
Id_PhysicalContext = "PhysicalContext"
Languages_odatacount_PhysicalContext = "1"
Location_odatacount_PhysicalContext = "1"
Name_PhysicalContext = "PhysicalContext Schema File"
Schema_PhysicalContext = "#PhysicalContext.PhysicalContext"
####CONSR-OBMC-RDFT-0230-0001
resource_JSONSchema_PortCollection = "/redfish/v1/JsonSchemas/PortCollection"
odata_type_value_PortCollection = "#JsonSchemaFile.v1_0_2.JsonSchemaFile"
Language_PortCollection = "['en']"
Location_PortCollection = "[{'Language': 'en', 'PublicationUri': 'http://redfish.dmtf.org/schemas/v1/PortCollection.json', 'Uri': '/redfish/v1/JsonSchemas/PortCollection/PortCollection.json'}]"
Description_PortCollection = "PortCollection Schema File Location"
Id_PortCollection = "PortCollection"
Languages_odatacount_PortCollection = "1"
Location_odatacount_PortCollection = "1"
Name_PortCollection = "PortCollection Schema File"
Schema_PortCollection = "#PortCollection.PortCollection"
####CONSR-OBMC-RDFT-0232-0001
resource_JSONSchema_PowerSubsystem = "/redfish/v1/JsonSchemas/PowerSubsystem"
odata_type_value_PowerSubsystem = "#JsonSchemaFile.v1_0_2.JsonSchemaFile"
Language_PowerSubsystem = "['en']"
Location_PowerSubsystem = "[{'Language': 'en', 'PublicationUri': 'http://redfish.dmtf.org/schemas/v1/PowerSubsystem.json', 'Uri': '/redfish/v1/JsonSchemas/PowerSubsystem/PowerSubsystem.json'}]"
Description_PowerSubsystem = "PowerSubsystem Schema File Location"
Id_PowerSubsystem = "PowerSubsystem"
Languages_odatacount_PowerSubsystem = "1"
Location_odatacount_PowerSubsystem = "1"
Name_PowerSubsystem = "PowerSubsystem Schema File"
Schema_PowerSubsystem = "#PowerSubsystem.PowerSubsystem"
####CONSR-OBMC-RDFT-0234-0001
resource_JSONSchema_PowerSupplyCollection = "/redfish/v1/JsonSchemas/PowerSupplyCollection"
odata_type_value_PowerSupplyCollection = "#JsonSchemaFile.v1_0_2.JsonSchemaFile"
Language_PowerSupplyCollection = "['en']"
Location_PowerSupplyCollection = "[{'Language': 'en', 'PublicationUri': 'http://redfish.dmtf.org/schemas/v1/PowerSupplyCollection.json', 'Uri': '/redfish/v1/JsonSchemas/PowerSupplyCollection/PowerSupplyCollection.json'}]"
Description_PowerSupplyCollection = "PowerSupplyCollection Schema File Location"
Id_PowerSupplyCollection = "PowerSupplyCollection"
Languages_odatacount_PowerSupplyCollection = "1"
Location_odatacount_PowerSupplyCollection = "1"
Name_PowerSupplyCollection = "PowerSupplyCollection Schema File"
Schema_PowerSupplyCollection = "#PowerSupplyCollection.PowerSupplyCollection"
####CONSR-OBMC-RDFT-0236-0001
resource_JSONSchema_Processor = "/redfish/v1/JsonSchemas/Processor"
odata_type_value_Processor = "#JsonSchemaFile.v1_0_2.JsonSchemaFile"
Language_Processor = "['en']"
Location_Processor = "[{'Language': 'en', 'PublicationUri': 'http://redfish.dmtf.org/schemas/v1/Processor.json', 'Uri': '/redfish/v1/JsonSchemas/Processor/Processor.json'}]"
Description_Processor = "Processor Schema File Location"
Id_Processor = "Processor"
Languages_odatacount_Processor = "1"
Location_odatacount_Processor = "1"
Name_Processor = "Processor Schema File"
Schema_Processor = "#Processor.Processor"
####CONSR-OBMC-RDFT-0238-0001
resource_JSONSchema_redfish_error = "/redfish/v1/JsonSchemas/redfish-error"
odata_type_value_redfish_error = "#JsonSchemaFile.v1_0_2.JsonSchemaFile"
Language_redfish_error = "['en']"
Location_redfish_error = "[{'Language': 'en', 'PublicationUri': 'http://redfish.dmtf.org/schemas/v1/redfish-error.json', 'Uri': '/redfish/v1/JsonSchemas/redfish-error/redfish-error.json'}]"
Description_redfish_error = "redfish-error Schema File Location"
Id_redfish_error = "redfish-error"
Languages_odatacount_redfish_error = "1"
Location_odatacount_redfish_error = "1"
Name_redfish_error = "redfish-error Schema File"
Schema_redfish_error = "#redfish-error.redfish-error"
####CONSR-OBMC-RDFT-0240-0001
resource_JSONSchema_redfish_schema = "/redfish/v1/JsonSchemas/redfish-schema"
odata_type_value_redfish_schema = "#JsonSchemaFile.v1_0_2.JsonSchemaFile"
Language_redfish_schema = "['en']"
Location_redfish_schema = "[{'Language': 'en', 'PublicationUri': 'http://redfish.dmtf.org/schemas/v1/redfish-schema.json', 'Uri': '/redfish/v1/JsonSchemas/redfish-schema/redfish-schema.json'}]"
Description_redfish_schema = "redfish-schema Schema File Location"
Id_redfish_schema = "redfish-schema"
Languages_odatacount_redfish_schema = "1"
Location_odatacount_redfish_schema = "1"
Name_redfish_schema = "redfish-schema Schema File"
Schema_redfish_schema = "#redfish-schema.redfish-schema"
####CONSR-OBMC-RDFT-0242-0001
resource_JSONSchema_Redundancy = "/redfish/v1/JsonSchemas/Redundancy"
odata_type_value_Redundancy = "#JsonSchemaFile.v1_0_2.JsonSchemaFile"
Language_Redundancy = "['en']"
Location_Redundancy = "[{'Language': 'en', 'PublicationUri': 'http://redfish.dmtf.org/schemas/v1/Redundancy.json', 'Uri': '/redfish/v1/JsonSchemas/Redundancy/Redundancy.json'}]"
Description_Redundancy = "Redundancy Schema File Location"
Id_Redundancy = "Redundancy"
Languages_odatacount_Redundancy = "1"
Location_odatacount_Redundancy = "1"
Name_Redundancy = "Redundancy Schema File"
Schema_Redundancy = "#Redundancy.Redundancy"
####CONSR-OBMC-RDFT-0244-0001
resource_JSONSchema_Role = "/redfish/v1/JsonSchemas/Role"
odata_type_value_Role = "#JsonSchemaFile.v1_0_2.JsonSchemaFile"
Language_Role = "['en']"
Location_Role = "[{'Language': 'en', 'PublicationUri': 'http://redfish.dmtf.org/schemas/v1/Role.json', 'Uri': '/redfish/v1/JsonSchemas/Role/Role.json'}]"
Description_Role = "Role Schema File Location"
Id_Role = "Role"
Languages_odatacount_Role = "1"
Location_odatacount_Role = "1"
Name_Role = "Role Schema File"
Schema_Role = "#Role.Role"
####CONSR-OBMC-RDFT-0246-0001
resource_JSONSchema_Sensor = "/redfish/v1/JsonSchemas/Sensor"
odata_type_value_Sensor = "#JsonSchemaFile.v1_0_2.JsonSchemaFile"
Language_Sensor = "['en']"
Location_Sensor = "[{'Language': 'en', 'PublicationUri': 'http://redfish.dmtf.org/schemas/v1/Sensor.json', 'Uri': '/redfish/v1/JsonSchemas/Sensor/Sensor.json'}]"
Description_Sensor = "Sensor Schema File Location"
Id_Sensor = "Sensor"
Languages_odatacount_Sensor = "1"
Location_odatacount_Sensor = "1"
Name_Sensor = "Sensor Schema File"
Schema_Sensor = "#Sensor.Sensor"
####CONSR-OBMC-RDFT-0248-0001
resource_JSONSchema_ServiceRoot = "/redfish/v1/JsonSchemas/ServiceRoot"
odata_type_value_ServiceRoot = "#JsonSchemaFile.v1_0_2.JsonSchemaFile"
Language_ServiceRoot = "['en']"
Location_ServiceRoot = "[{'Language': 'en', 'PublicationUri': 'http://redfish.dmtf.org/schemas/v1/ServiceRoot.json', 'Uri': '/redfish/v1/JsonSchemas/ServiceRoot/ServiceRoot.json'}]"
Description_ServiceRoot = "ServiceRoot Schema File Location"
Id_ServiceRoot = "ServiceRoot"
Languages_odatacount_ServiceRoot = "1"
Location_odatacount_ServiceRoot = "1"
Name_ServiceRoot = "ServiceRoot Schema File"
Schema_ServiceRoot = "#ServiceRoot.ServiceRoot"
####CONSR-OBMC-RDFT-0250-0001
resource_JSONSchema_SessionCollection = "/redfish/v1/JsonSchemas/SessionCollection"
odata_type_value_SessionCollection = "#JsonSchemaFile.v1_0_2.JsonSchemaFile"
Language_SessionCollection = "['en']"
Location_SessionCollection = "[{'Language': 'en', 'PublicationUri': 'http://redfish.dmtf.org/schemas/v1/SessionCollection.json', 'Uri': '/redfish/v1/JsonSchemas/SessionCollection/SessionCollection.json'}]"
Description_SessionCollection = "SessionCollection Schema File Location"
Id_SessionCollection = "SessionCollection"
Languages_odatacount_SessionCollection = "1"
Location_odatacount_SessionCollection = "1"
Name_SessionCollection = "SessionCollection Schema File"
Schema_SessionCollection = "#SessionCollection.SessionCollection"
####CONSR-OBMC-RDFT-0252-0001
resource_JSONSchema_Settings = "/redfish/v1/JsonSchemas/Settings"
odata_type_value_Settings = "#JsonSchemaFile.v1_0_2.JsonSchemaFile"
Language_Settings = "['en']"
Location_Settings = "[{'Language': 'en', 'PublicationUri': 'http://redfish.dmtf.org/schemas/v1/Settings.json', 'Uri': '/redfish/v1/JsonSchemas/Settings/Settings.json'}]"
Description_Settings = "Settings Schema File Location"
Id_Settings = "Settings"
Languages_odatacount_Settings = "1"
Location_odatacount_Settings = "1"
Name_Settings = "Settings Schema File"
Schema_Settings = "#Settings.Settings"
####CONSR-OBMC-RDFT-0254-0001
resource_JSONSchema_SoftwareInventoryCollection = "/redfish/v1/JsonSchemas/SoftwareInventoryCollection"
odata_type_value_SoftwareInventoryCollection = "#JsonSchemaFile.v1_0_2.JsonSchemaFile"
Language_SoftwareInventoryCollection = "['en']"
Location_SoftwareInventoryCollection = "[{'Language': 'en', 'PublicationUri': 'http://redfish.dmtf.org/schemas/v1/SoftwareInventoryCollection.json', 'Uri': '/redfish/v1/JsonSchemas/SoftwareInventoryCollection/SoftwareInventoryCollection.json'}]"
Description_SoftwareInventoryCollection = "SoftwareInventoryCollection Schema File Location"
Id_SoftwareInventoryCollection = "SoftwareInventoryCollection"
Languages_odatacount_SoftwareInventoryCollection = "1"
Location_odatacount_SoftwareInventoryCollection = "1"
Name_SoftwareInventoryCollection = "SoftwareInventoryCollection Schema File"
Schema_SoftwareInventoryCollection = "#SoftwareInventoryCollection.SoftwareInventoryCollection"
####CONSR-OBMC-RDFT-0256-0001
resource_JSONSchema_StorageCollection = "/redfish/v1/JsonSchemas/StorageCollection"
odata_type_value_StorageCollection = "#JsonSchemaFile.v1_0_2.JsonSchemaFile"
Language_StorageCollection = "['en']"
Location_StorageCollection = "[{'Language': 'en', 'PublicationUri': 'http://redfish.dmtf.org/schemas/v1/StorageCollection.json', 'Uri': '/redfish/v1/JsonSchemas/StorageCollection/StorageCollection.json'}]"
Description_StorageCollection = "StorageCollection Schema File Location"
Id_StorageCollection = "StorageCollection"
Languages_odatacount_StorageCollection = "1"
Location_odatacount_StorageCollection = "1"
Name_StorageCollection = "StorageCollection Schema File"
Schema_StorageCollection = "#StorageCollection.StorageCollection"
####CONSR-OBMC-RDFT-0258-0001
resource_JSONSchema_StorageControllerCollection = "/redfish/v1/JsonSchemas/StorageControllerCollection"
odata_type_value_StorageControllerCollection = "#JsonSchemaFile.v1_0_2.JsonSchemaFile"
Language_StorageControllerCollection = "['en']"
Location_StorageControllerCollection = "[{'Language': 'en', 'PublicationUri': 'http://redfish.dmtf.org/schemas/v1/StorageControllerCollection.json', 'Uri': '/redfish/v1/JsonSchemas/StorageControllerCollection/StorageControllerCollection.json'}]"
Description_StorageControllerCollection = "StorageControllerCollection Schema File Location"
Id_StorageControllerCollection = "StorageControllerCollection"
Languages_odatacount_StorageControllerCollection = "1"
Location_odatacount_StorageControllerCollection = "1"
Name_StorageControllerCollection = "StorageControllerCollection Schema File"
Schema_StorageControllerCollection = "#StorageControllerCollection.StorageControllerCollection"
####CONSR-OBMC-RDFT-0260-0001
resource_JSONSchema_TaskCollection = "/redfish/v1/JsonSchemas/TaskCollection"
odata_type_value_TaskCollection = "#JsonSchemaFile.v1_0_2.JsonSchemaFile"
Language_TaskCollection = "['en']"
Location_TaskCollection = "[{'Language': 'en', 'PublicationUri': 'http://redfish.dmtf.org/schemas/v1/TaskCollection.json', 'Uri': '/redfish/v1/JsonSchemas/TaskCollection/TaskCollection.json'}]"
Description_TaskCollection = "TaskCollection Schema File Location"
Id_TaskCollection = "TaskCollection"
Languages_odatacount_TaskCollection = "1"
Location_odatacount_TaskCollection = "1"
Name_TaskCollection = "TaskCollection Schema File"
Schema_TaskCollection = "#TaskCollection.TaskCollection"
####CONSR-OBMC-RDFT-0262-0001
resource_JSONSchema_TelemetryService = "/redfish/v1/JsonSchemas/TelemetryService"
odata_type_value_TelemetryService = "#JsonSchemaFile.v1_0_2.JsonSchemaFile"
Language_TelemetryService = "['en']"
Location_TelemetryService = "[{'Language': 'en', 'PublicationUri': 'http://redfish.dmtf.org/schemas/v1/TelemetryService.json', 'Uri': '/redfish/v1/JsonSchemas/TelemetryService/TelemetryService.json'}]"
Description_TelemetryService = "TelemetryService Schema File Location"
Id_TelemetryService = "TelemetryService"
Languages_odatacount_TelemetryService = "1"
Location_odatacount_TelemetryService = "1"
Name_TelemetryService = "TelemetryService Schema File"
Schema_TelemetryService = "#TelemetryService.TelemetryService"
####CONSR-OBMC-RDFT-0264-0001
resource_JSONSchema_ThermalMetrics = "/redfish/v1/JsonSchemas/ThermalMetrics"
odata_type_value_ThermalMetrics = "#JsonSchemaFile.v1_0_2.JsonSchemaFile"
Language_ThermalMetrics = "['en']"
Location_ThermalMetrics = "[{'Language': 'en', 'PublicationUri': 'http://redfish.dmtf.org/schemas/v1/ThermalMetrics.json', 'Uri': '/redfish/v1/JsonSchemas/ThermalMetrics/ThermalMetrics.json'}]"
Description_ThermalMetrics = "ThermalMetrics Schema File Location"
Id_ThermalMetrics = "ThermalMetrics"
Languages_odatacount_ThermalMetrics = "1"
Location_odatacount_ThermalMetrics = "1"
Name_ThermalMetrics = "ThermalMetrics Schema File"
Schema_ThermalMetrics = "#ThermalMetrics.ThermalMetrics"
####CONSR-OBMC-RDFT-0266-0001
resource_JSONSchema_Triggers = "/redfish/v1/JsonSchemas/Triggers"
odata_type_value_Triggers = "#JsonSchemaFile.v1_0_2.JsonSchemaFile"
Language_Triggers = "['en']"
Location_Triggers = "[{'Language': 'en', 'PublicationUri': 'http://redfish.dmtf.org/schemas/v1/Triggers.json', 'Uri': '/redfish/v1/JsonSchemas/Triggers/Triggers.json'}]"
Description_Triggers = "Triggers Schema File Location"
Id_Triggers = "Triggers"
Languages_odatacount_Triggers = "1"
Location_odatacount_Triggers = "1"
Name_Triggers = "Triggers Schema File"
Schema_Triggers = "#Triggers.Triggers"
####CONSR-OBMC-RDFT-0268-0001
resource_JSONSchema_UpdateService = "/redfish/v1/JsonSchemas/UpdateService"
odata_type_value_UpdateService = "#JsonSchemaFile.v1_0_2.JsonSchemaFile"
Language_UpdateService = "['en']"
Location_UpdateService = "[{'Language': 'en', 'PublicationUri': 'http://redfish.dmtf.org/schemas/v1/UpdateService.json', 'Uri': '/redfish/v1/JsonSchemas/UpdateService/UpdateService.json'}]"
Description_UpdateService = "UpdateService Schema File Location"
Id_UpdateService = "UpdateService"
Languages_odatacount_UpdateService = "1"
Location_odatacount_UpdateService = "1"
Name_UpdateService = "UpdateService Schema File"
Schema_UpdateService = "#UpdateService.UpdateService"
####CONSR-OBMC-RDFT-0270-0001
resource_JSONSchema_VirtualMediaCollection = "/redfish/v1/JsonSchemas/VirtualMediaCollection"
odata_type_value_VirtualMediaCollection = "#JsonSchemaFile.v1_0_2.JsonSchemaFile"
Language_VirtualMediaCollection = "['en']"
Location_VirtualMediaCollection = "[{'Language': 'en', 'PublicationUri': 'http://redfish.dmtf.org/schemas/v1/VirtualMediaCollection.json', 'Uri': '/redfish/v1/JsonSchemas/VirtualMediaCollection/VirtualMediaCollection.json'}]"
Description_VirtualMediaCollection = "VirtualMediaCollection Schema File Location"
Id_VirtualMediaCollection = "VirtualMediaCollection"
Languages_odatacount_VirtualMediaCollection = "1"
Location_odatacount_VirtualMediaCollection = "1"
Name_VirtualMediaCollection = "VirtualMediaCollection Schema File"
Schema_VirtualMediaCollection = "#VirtualMediaCollection.VirtualMediaCollection"
####CONSR-OBMC-RDFT-0159-0001
resource_JSONSchema_FileCollection = "/redfish/v1/JsonSchemas"
data_type_FileCollection = "#JsonSchemaFileCollection.JsonSchemaFileCollection"
Members_odata_count_FileCollection = "111"
Description_FileCollection = "Collection of JsonSchemaFiles"
Name_FileCollection = "JsonSchemaFile Collection"
####CONSR-OBMC-RDFT-0161-0001
resource_JSONSchema_ActionInfo = "/redfish/v1/JsonSchemas/ActionInfo"
odata_type_ActionInfo = "#JsonSchemaFile.v1_0_2.JsonSchemaFile"
Description_ActionInfo = "ActionInfo Schema File Location"
Id_ActionInfo = "ActionInfo"
Languages_ActionInfo = "['en']"
Languages_odata_count_ActionInfo = "1"
Location_odata_count_ActionInfo = "1"
Location_ActionInfo = "[{'Language': 'en', 'PublicationUri': 'http://redfish.dmtf.org/schemas/v1/ActionInfo.json', 'Uri': '/redfish/v1/JsonSchemas/ActionInfo/ActionInfo.json'}]"
Name_ActionInfo = "ActionInfo Schema File"
Schema_ActionInfo = "#ActionInfo.ActionInfo"
####CONSR-OBMC-RDFT-0163-0001
resource_JSONSchema_AggregationSource = "/redfish/v1/JsonSchemas/AggregationSource"
odata_type_AggregationSource = "#JsonSchemaFile.v1_0_2.JsonSchemaFile"
Description_AggregationSource = "AggregationSource Schema File Location"
Id_AggregationSource = "AggregationSource"
Languages_AggregationSource = "['en']"
Languages_odata_count_AggregationSource = "1"
Location_odata_count_AggregationSource = "1"
Location_AggregationSource = "[{'Language': 'en', 'PublicationUri': 'http://redfish.dmtf.org/schemas/v1/AggregationSource.json', 'Uri': '/redfish/v1/JsonSchemas/AggregationSource/AggregationSource.json'}]"
Name_AggregationSource = "AggregationSource Schema File"
Schema_AggregationSource = "#AggregationSource.AggregationSource"
####CONSR-OBMC-RDFT-0165-0001
resource_JSONSchema_Assembly = "/redfish/v1/JsonSchemas/Assembly"
odata_type_Assembly = "#JsonSchemaFile.v1_0_2.JsonSchemaFile"
Description_Assembly = "Assembly Schema File Location"
Id_Assembly = "Assembly"
Languages_Assembly = "['en']"
Languages_odata_count_Assembly = "1"
Location_odata_count_Assembly = "1"
Location_Assembly = "[{'Language': 'en', 'PublicationUri': 'http://redfish.dmtf.org/schemas/v1/Assembly.json', 'Uri': '/redfish/v1/JsonSchemas/Assembly/Assembly.json'}]"
Name_Assembly = "Assembly Schema File"
Schema_Assembly = "#Assembly.Assembly"
####CONSR-OBMC-RDFT-0167-0001
resource_JSONSchema_Bios = "/redfish/v1/JsonSchemas/Bios"
odata_type_Bios = "#JsonSchemaFile.v1_0_2.JsonSchemaFile"
Description_Bios = "Bios Schema File Location"
Id_Bios = "Bios"
Languages_Bios = "['en']"
Languages_odata_count_Bios = "1"
Location_odata_count_Bios = "1"
Location_Bios = "[{'Language': 'en', 'PublicationUri': 'http://redfish.dmtf.org/schemas/v1/Bios.json', 'Uri': '/redfish/v1/JsonSchemas/Bios/Bios.json'}]"
Name_Bios = "Bios Schema File"
Schema_Bios = "#Bios.Bios"
####CONSR-OBMC-RDFT-0169-0001
resource_JSONSchema_CableCollection = "/redfish/v1/JsonSchemas/CableCollection"
odata_type_CableCollection = "#JsonSchemaFile.v1_0_2.JsonSchemaFile"
Description_CableCollection = "CableCollection Schema File Location"
Id_CableCollection = "CableCollection"
Languages_CableCollection = "['en']"
Languages_odata_count_CableCollection = "1"
Location_odata_count_CableCollection = "1"
Location_CableCollection = "[{'Language': 'en', 'PublicationUri': 'http://redfish.dmtf.org/schemas/v1/CableCollection.json', 'Uri': '/redfish/v1/JsonSchemas/CableCollection/CableCollection.json'}]"
Name_CableCollection = "CableCollection Schema File"
Schema_CableCollection = "#CableCollection.CableCollection"
####CONSR-OBMC-RDFT-0171-0001
resource_JSONSchema_CertificateCollection = "/redfish/v1/JsonSchemas/CertificateCollection"
odata_type_CertificateCollection = "#JsonSchemaFile.v1_0_2.JsonSchemaFile"
Description_CertificateCollection = "CertificateCollection Schema File Location"
Id_CertificateCollection = "CertificateCollection"
Languages_CertificateCollection = "['en']"
Languages_odata_count_CertificateCollection = "1"
Location_odata_count_CertificateCollection = "1"
Location_CertificateCollection = "[{'Language': 'en', 'PublicationUri': 'http://redfish.dmtf.org/schemas/v1/CertificateCollection.json', 'Uri': '/redfish/v1/JsonSchemas/CertificateCollection/CertificateCollection.json'}]"
Name_CertificateCollection = "CertificateCollection Schema File"
Schema_CertificateCollection = "#CertificateCollection.CertificateCollection"
####CONSR-OBMC-RDFT-0173-0001
resource_JSONSchema_CertificateService = "/redfish/v1/JsonSchemas/CertificateService"
odata_type_CertificateService = "#JsonSchemaFile.v1_0_2.JsonSchemaFile"
Description_CertificateService = "CertificateService Schema File Location"
Id_CertificateService = "CertificateService"
Languages_CertificateService = "['en']"
Languages_odata_count_CertificateService = "1"
Location_odata_count_CertificateService = "1"
Location_CertificateService = "[{'Language': 'en', 'PublicationUri': 'http://redfish.dmtf.org/schemas/v1/CertificateService.json', 'Uri': '/redfish/v1/JsonSchemas/CertificateService/CertificateService.json'}]"
Name_CertificateService = "CertificateService Schema File"
Schema_CertificateService = "#CertificateService.CertificateService"
####CONSR-OBMC-RDFT-0175-0001
resource_JSONSchema_ChassisCollection = "/redfish/v1/JsonSchemas/ChassisCollection"
odata_type_ChassisCollection = "#JsonSchemaFile.v1_0_2.JsonSchemaFile"
Description_ChassisCollection = "ChassisCollection Schema File Location"
Id_ChassisCollection = "ChassisCollection"
Languages_ChassisCollection = "['en']"
Languages_odata_count_ChassisCollection = "1"
Location_odata_count_ChassisCollection = "1"
Location_ChassisCollection = "[{'Language': 'en', 'PublicationUri': 'http://redfish.dmtf.org/schemas/v1/ChassisCollection.json', 'Uri': '/redfish/v1/JsonSchemas/ChassisCollection/ChassisCollection.json'}]"
Name_ChassisCollection = "ChassisCollection Schema File"
Schema_ChassisCollection = "#ChassisCollection.ChassisCollection"
####CONSR-OBMC-RDFT-0177-0001
resource_JSONSchema_ComponentIntegrityCollection = "/redfish/v1/JsonSchemas/ComponentIntegrityCollection"
odata_type_ComponentIntegrityCollection = "#JsonSchemaFile.v1_0_2.JsonSchemaFile"
Description_ComponentIntegrityCollection = "ComponentIntegrityCollection Schema File Location"
Id_ComponentIntegrityCollection = "ComponentIntegrityCollection"
Languages_ComponentIntegrityCollection = "['en']"
Languages_odata_count_ComponentIntegrityCollection = "1"
Location_odata_count_ComponentIntegrityCollection = "1"
Location_ComponentIntegrityCollection = "[{'Language': 'en', 'PublicationUri': 'http://redfish.dmtf.org/schemas/v1/ComponentIntegrityCollection.json', 'Uri': '/redfish/v1/JsonSchemas/ComponentIntegrityCollection/ComponentIntegrityCollection.json'}]"
Name_ComponentIntegrityCollection = "ComponentIntegrityCollection Schema File"
Schema_ComponentIntegrityCollection = "#ComponentIntegrityCollection.ComponentIntegrityCollection"
####CONSR-OBMC-RDFT-0179-0001
resource_JSONSchema_ComputerSystemCollection = "/redfish/v1/JsonSchemas/ComputerSystemCollection"
odata_type_ComputerSystemCollection = "#JsonSchemaFile.v1_0_2.JsonSchemaFile"
Description_ComputerSystemCollection = "ComputerSystemCollection Schema File Location"
Id_ComputerSystemCollection = "ComputerSystemCollection"
Languages_ComputerSystemCollection = "['en']"
Languages_odata_count_ComputerSystemCollection = "1"
Location_odata_count_ComputerSystemCollection = "1"
Location_ComputerSystemCollection = "[{'Language': 'en', 'PublicationUri': 'http://redfish.dmtf.org/schemas/v1/ComputerSystemCollection.json', 'Uri': '/redfish/v1/JsonSchemas/ComputerSystemCollection/ComputerSystemCollection.json'}]"
Name_ComputerSystemCollection = "ComputerSystemCollection Schema File"
Schema_ComputerSystemCollection = "#ComputerSystemCollection.ComputerSystemCollection"
####CONSR-OBMC-RDFT-0181-0001
resource_JSONSchema_DriveCollection = "/redfish/v1/JsonSchemas/DriveCollection"
odata_type_DriveCollection = "#JsonSchemaFile.v1_0_2.JsonSchemaFile"
Description_DriveCollection = "DriveCollection Schema File Location"
Id_DriveCollection = "DriveCollection"
Languages_DriveCollection = "['en']"
Languages_odata_count_DriveCollection = "1"
Location_odata_count_DriveCollection = "1"
Location_DriveCollection = "[{'Language': 'en', 'PublicationUri': 'http://redfish.dmtf.org/schemas/v1/DriveCollection.json', 'Uri': '/redfish/v1/JsonSchemas/DriveCollection/DriveCollection.json'}]"
Name_DriveCollection = "DriveCollection Schema File"
Schema_DriveCollection = "#DriveCollection.DriveCollection"
####CONSR-OBMC-RDFT-0183-0001
resource_JSONSchema_EthernetInterface = "/redfish/v1/JsonSchemas/EthernetInterface"
odata_type_EthernetInterface = "#JsonSchemaFile.v1_0_2.JsonSchemaFile"
Description_EthernetInterface = "EthernetInterface Schema File Location"
Id_EthernetInterface = "EthernetInterface"
Languages_EthernetInterface = "['en']"
Languages_odata_count_EthernetInterface = "1"
Location_odata_count_EthernetInterface = "1"
Location_EthernetInterface = "[{'Language': 'en', 'PublicationUri': 'http://redfish.dmtf.org/schemas/v1/EthernetInterface.json', 'Uri': '/redfish/v1/JsonSchemas/EthernetInterface/EthernetInterface.json'}]"
Name_EthernetInterface = "EthernetInterface Schema File"
Schema_EthernetInterface = "#EthernetInterface.EthernetInterface"
####CONSR-OBMC-RDFT-0185-0001
resource_JSONSchema_Event = "/redfish/v1/JsonSchemas/Event"
odata_type_Event = "#JsonSchemaFile.v1_0_2.JsonSchemaFile"
Description_Event = "Event Schema File Location"
Id_Event = "Event"
Languages_Event = "['en']"
Languages_odata_count_Event = "1"
Location_odata_count_Event = "1"
Location_Event = "[{'Language': 'en', 'PublicationUri': 'http://redfish.dmtf.org/schemas/v1/Event.json', 'Uri': '/redfish/v1/JsonSchemas/Event/Event.json'}]"
Name_Event = "Event Schema File"
Schema_Event = "#Event.Event"
####CONSR-OBMC-RDFT-0187-0001
resource_JSONSchema_EventDestinationCollection = "/redfish/v1/JsonSchemas/EventDestinationCollection"
odata_type_EventDestinationCollection = "#JsonSchemaFile.v1_0_2.JsonSchemaFile"
Description_EventDestinationCollection = "EventDestinationCollection Schema File Location"
Id_EventDestinationCollection = "EventDestinationCollection"
Languages_EventDestinationCollection = "['en']"
Languages_odata_count_EventDestinationCollection = "1"
Location_odata_count_EventDestinationCollection = "1"
Location_EventDestinationCollection = "[{'Language': 'en', 'PublicationUri': 'http://redfish.dmtf.org/schemas/v1/EventDestinationCollection.json', 'Uri': '/redfish/v1/JsonSchemas/EventDestinationCollection/EventDestinationCollection.json'}]"
Name_EventDestinationCollection = "EventDestinationCollection Schema File"
Schema_EventDestinationCollection = "#EventDestinationCollection.EventDestinationCollection"
####CONSR-OBMC-RDFT-0189-0001
resource_JSONSchema_FabricAdapter = "/redfish/v1/JsonSchemas/FabricAdapter"
odata_type_FabricAdapter = "#JsonSchemaFile.v1_0_2.JsonSchemaFile"
Description_FabricAdapter = "FabricAdapter Schema File Location"
Id_FabricAdapter = "FabricAdapter"
Languages_FabricAdapter = "['en']"
Languages_odata_count_FabricAdapter = "1"
Location_odata_count_FabricAdapter = "1"
Location_FabricAdapter = "[{'Language': 'en', 'PublicationUri': 'http://redfish.dmtf.org/schemas/v1/FabricAdapter.json', 'Uri': '/redfish/v1/JsonSchemas/FabricAdapter/FabricAdapter.json'}]"
Name_FabricAdapter = "FabricAdapter Schema File"
Schema_FabricAdapter = "#FabricAdapter.FabricAdapter"
####CONSR-OBMC-RDFT-0191-0001
resource_JSONSchema_Fan = "/redfish/v1/JsonSchemas/Fan"
odata_type_Fan = "#JsonSchemaFile.v1_0_2.JsonSchemaFile"
Description_Fan = "Fan Schema File Location"
Id_Fan = "Fan"
Languages_Fan = "['en']"
Languages_odata_count_Fan = "1"
Location_odata_count_Fan = "1"
Location_Fan = "[{'Language': 'en', 'PublicationUri': 'http://redfish.dmtf.org/schemas/v1/Fan.json', 'Uri': '/redfish/v1/JsonSchemas/Fan/Fan.json'}]"
Name_Fan = "Fan Schema File"
Schema_Fan = "#Fan.Fan"
####CONSR-OBMC-RDFT-0193-0001
resource_JSONSchema_IPAddresses = "/redfish/v1/JsonSchemas/IPAddresses"
odata_type_IPAddresses = "#JsonSchemaFile.v1_0_2.JsonSchemaFile"
Description_IPAddresses = "IPAddresses Schema File Location"
Id_IPAddresses = "IPAddresses"
Languages_IPAddresses = "['en']"
Languages_odata_count_IPAddresses = "1"
Location_odata_count_IPAddresses = "1"
Location_IPAddresses = "[{'Language': 'en', 'PublicationUri': 'http://redfish.dmtf.org/schemas/v1/IPAddresses.json', 'Uri': '/redfish/v1/JsonSchemas/IPAddresses/IPAddresses.json'}]"
Name_IPAddresses = "IPAddresses Schema File"
Schema_IPAddresses = "#IPAddresses.IPAddresses"
####CONSR-OBMC-RDFT-0195-0001
resource_JSONSchema_JsonSchemaFileCollection = "/redfish/v1/JsonSchemas/JsonSchemaFileCollection"
odata_type_JsonSchemaFileCollection = "#JsonSchemaFile.v1_0_2.JsonSchemaFile"
Description_JsonSchemaFileCollection = "JsonSchemaFileCollection Schema File Location"
Id_JsonSchemaFileCollection = "JsonSchemaFileCollection"
Languages_JsonSchemaFileCollection = "['en']"
Languages_odata_count_JsonSchemaFileCollection = "1"
Location_odata_count_JsonSchemaFileCollection = "1"
Location_JsonSchemaFileCollection = "[{'Language': 'en', 'PublicationUri': 'http://redfish.dmtf.org/schemas/v1/JsonSchemaFileCollection.json', 'Uri': '/redfish/v1/JsonSchemas/JsonSchemaFileCollection/JsonSchemaFileCollection.json'}]"
Name_JsonSchemaFileCollection = "JsonSchemaFileCollection Schema File"
Schema_JsonSchemaFileCollection = "#JsonSchemaFileCollection.JsonSchemaFileCollection"
####CONSR-OBMC-RDFT-0197-0001
resource_JSONSchema_LogEntryCollection = "/redfish/v1/JsonSchemas/LogEntryCollection"
odata_type_LogEntryCollection = "#JsonSchemaFile.v1_0_2.JsonSchemaFile"
Description_LogEntryCollection = "LogEntryCollection Schema File Location"
Id_LogEntryCollection = "LogEntryCollection"
Languages_LogEntryCollection = "['en']"
Languages_odata_count_LogEntryCollection = "1"
Location_odata_count_LogEntryCollection = "1"
Location_LogEntryCollection = "[{'Language': 'en', 'PublicationUri': 'http://redfish.dmtf.org/schemas/v1/LogEntryCollection.json', 'Uri': '/redfish/v1/JsonSchemas/LogEntryCollection/LogEntryCollection.json'}]"
Name_LogEntryCollection = "LogEntryCollection Schema File"
Schema_LogEntryCollection = "#LogEntryCollection.LogEntryCollection"
####CONSR-OBMC-RDFT-0199-0001
resource_JSONSchema_LogServiceCollection = "/redfish/v1/JsonSchemas/LogServiceCollection"
odata_type_LogServiceCollection = "#JsonSchemaFile.v1_0_2.JsonSchemaFile"
Description_LogServiceCollection = "LogServiceCollection Schema File Location"
Id_LogServiceCollection = "LogServiceCollection"
Languages_LogServiceCollection = "['en']"
Languages_odata_count_LogServiceCollection = "1"
Location_odata_count_LogServiceCollection = "1"
Location_LogServiceCollection = "[{'Language': 'en', 'PublicationUri': 'http://redfish.dmtf.org/schemas/v1/LogServiceCollection.json', 'Uri': '/redfish/v1/JsonSchemas/LogServiceCollection/LogServiceCollection.json'}]"
Name_LogServiceCollection = "LogServiceCollection Schema File"
Schema_LogServiceCollection = "#LogServiceCollection.LogServiceCollection"
####CONSR-OBMC-RDFT-0201-0001
resource_JSONSchema_ManagerAccount = "/redfish/v1/JsonSchemas/ManagerAccount"
odata_type_ManagerAccount_201 = "#JsonSchemaFile.v1_0_2.JsonSchemaFile"
Description_ManagerAccount_201 = "ManagerAccount Schema File Location"
Id_ManagerAccount_201 = "ManagerAccount"
Languages_ManagerAccount_201 = "['en']"
Languages_odata_count_ManagerAccount_201 = "1"
Location_odata_count_ManagerAccount_201 = "1"
Location_ManagerAccount_201 = "[{'Language': 'en', 'PublicationUri': 'http://redfish.dmtf.org/schemas/v1/ManagerAccount.json', 'Uri': '/redfish/v1/JsonSchemas/ManagerAccount/ManagerAccount.json'}]"
Name_ManagerAccount_201 = "ManagerAccount Schema File"
Schema_ManagerAccount_201 = "#ManagerAccount.ManagerAccount"
####CONSR-OBMC-RDFT-0203-0001
resource_JSONSchema_ManagerCollection = "/redfish/v1/JsonSchemas/ManagerCollection"
odata_type_ManagerCollection = "#JsonSchemaFile.v1_0_2.JsonSchemaFile"
Description_ManagerCollection = "ManagerCollection Schema File Location"
Id_ManagerCollection = "ManagerCollection"
Languages_ManagerCollection = "['en']"
Languages_odata_count_ManagerCollection = "1"
Location_odata_count_ManagerCollection = "1"
Location_ManagerCollection = "[{'Language': 'en', 'PublicationUri': 'http://redfish.dmtf.org/schemas/v1/ManagerCollection.json', 'Uri': '/redfish/v1/JsonSchemas/ManagerCollection/ManagerCollection.json'}]"
Name_ManagerCollection = "ManagerCollection Schema File"
Schema_ManagerCollection = "#ManagerCollection.ManagerCollection"
####CONSR-OBMC-RDFT-0205-0001
resource_JSONSchema_ManagerNetworkProtocol = "/redfish/v1/JsonSchemas/ManagerNetworkProtocol"
odata_type_ManagerNetworkProtocol = "#JsonSchemaFile.v1_0_2.JsonSchemaFile"
Description_ManagerNetworkProtocol = "ManagerNetworkProtocol Schema File Location"
Id_ManagerNetworkProtocol = "ManagerNetworkProtocol"
Languages_ManagerNetworkProtocol = "['en']"
Languages_odata_count_ManagerNetworkProtocol = "1"
Location_odata_count_ManagerNetworkProtocol = "1"
Location_ManagerNetworkProtocol = "[{'Language': 'en', 'PublicationUri': 'http://redfish.dmtf.org/schemas/v1/ManagerNetworkProtocol.json', 'Uri': '/redfish/v1/JsonSchemas/ManagerNetworkProtocol/ManagerNetworkProtocol.json'}]"
Name_ManagerNetworkProtocol = "ManagerNetworkProtocol Schema File"
Schema_ManagerNetworkProtocol = "#ManagerNetworkProtocol.ManagerNetworkProtocol"
####CONSR-OBMC-RDFT-0207-0001
resource_JSONSchema_MemoryCollection = "/redfish/v1/JsonSchemas/MemoryCollection"
odata_type_MemoryCollection = "#JsonSchemaFile.v1_0_2.JsonSchemaFile"
Description_MemoryCollection = "MemoryCollection Schema File Location"
Id_MemoryCollection = "MemoryCollection"
Languages_MemoryCollection = "['en']"
Languages_odata_count_MemoryCollection = "1"
Location_odata_count_MemoryCollection = "1"
Location_MemoryCollection = "[{'Language': 'en', 'PublicationUri': 'http://redfish.dmtf.org/schemas/v1/MemoryCollection.json', 'Uri': '/redfish/v1/JsonSchemas/MemoryCollection/MemoryCollection.json'}]"
Name_MemoryCollection = "MemoryCollection Schema File"
Schema_MemoryCollection = "#MemoryCollection.MemoryCollection"
####CONSR-OBMC-RDFT-0209-0001
resource_JSONSchema_MessageRegistry = "/redfish/v1/JsonSchemas/MessageRegistry"
odata_type_MessageRegistry = "#JsonSchemaFile.v1_0_2.JsonSchemaFile"
Description_MessageRegistry = "MessageRegistry Schema File Location"
Id_MessageRegistry = "MessageRegistry"
Languages_MessageRegistry = "['en']"
Languages_odata_count_MessageRegistry = "1"
Location_odata_count_MessageRegistry = "1"
Location_MessageRegistry = "[{'Language': 'en', 'PublicationUri': 'http://redfish.dmtf.org/schemas/v1/MessageRegistry.json', 'Uri': '/redfish/v1/JsonSchemas/MessageRegistry/MessageRegistry.json'}]"
Name_MessageRegistry = "MessageRegistry Schema File"
Schema_MessageRegistry = "#MessageRegistry.MessageRegistry"
####CONSR-OBMC-RDFT-0211-0001
resource_JSONSchema_MessageRegistryFile = "/redfish/v1/JsonSchemas/MessageRegistryFile"
odata_type_MessageRegistryFile = "#JsonSchemaFile.v1_0_2.JsonSchemaFile"
Description_MessageRegistryFile = "MessageRegistryFile Schema File Location"
Id_MessageRegistryFile = "MessageRegistryFile"
Languages_MessageRegistryFile = "['en']"
Languages_odata_count_MessageRegistryFile = "1"
Location_odata_count_MessageRegistryFile = "1"
Location_MessageRegistryFile = "[{'Language': 'en', 'PublicationUri': 'http://redfish.dmtf.org/schemas/v1/MessageRegistryFile.json', 'Uri': '/redfish/v1/JsonSchemas/MessageRegistryFile/MessageRegistryFile.json'}]"
Name_MessageRegistryFile = "MessageRegistryFile Schema File"
Schema_MessageRegistryFile = "#MessageRegistryFile.MessageRegistryFile"
####CONSR-OBMC-RDFT-0213-0001
resource_JSONSchema_MetricDefinition = "/redfish/v1/JsonSchemas/MetricDefinition"
odata_type_MetricDefinition = "#JsonSchemaFile.v1_0_2.JsonSchemaFile"
Description_MetricDefinition = "MetricDefinition Schema File Location"
Id_MetricDefinition = "MetricDefinition"
Languages_MetricDefinition = "['en']"
Languages_odata_count_MetricDefinition = "1"
Location_odata_count_MetricDefinition = "1"
Location_MetricDefinition = "[{'Language': 'en', 'PublicationUri': 'http://redfish.dmtf.org/schemas/v1/MetricDefinition.json', 'Uri': '/redfish/v1/JsonSchemas/MetricDefinition/MetricDefinition.json'}]"
Name_MetricDefinition = "MetricDefinition Schema File"
Schema_MetricDefinition = "#MetricDefinition.MetricDefinition"
####CONSR-OBMC-RDFT-0215-0001
resource_JSONSchema_MetricReport = "/redfish/v1/JsonSchemas/MetricReport"
odata_type_MetricReport = "#JsonSchemaFile.v1_0_2.JsonSchemaFile"
Description_MetricReport = "MetricReport Schema File Location"
Id_MetricReport = "MetricReport"
Languages_MetricReport = "['en']"
Languages_odata_count_MetricReport = "1"
Location_odata_count_MetricReport = "1"
Location_MetricReport = "[{'Language': 'en', 'PublicationUri': 'http://redfish.dmtf.org/schemas/v1/MetricReport.json', 'Uri': '/redfish/v1/JsonSchemas/MetricReport/MetricReport.json'}]"
Name_MetricReport = "MetricReport Schema File"
Schema_MetricReport = "#MetricReport.MetricReport"
####CONSR-OBMC-RDFT-0217-0001
resource_JSONSchema_MetricReportDefinition = "/redfish/v1/JsonSchemas/MetricReportDefinition"
odata_type_MetricReportDefinition = "#JsonSchemaFile.v1_0_2.JsonSchemaFile"
Description_MetricReportDefinition = "MetricReportDefinition Schema File Location"
Id_MetricReportDefinition = "MetricReportDefinition"
Languages_MetricReportDefinition = "['en']"
Languages_odata_count_MetricReportDefinition = "1"
Location_odata_count_MetricReportDefinition = "1"
Location_MetricReportDefinition = "[{'Language': 'en', 'PublicationUri': 'http://redfish.dmtf.org/schemas/v1/MetricReportDefinition.json', 'Uri': '/redfish/v1/JsonSchemas/MetricReportDefinition/MetricReportDefinition.json'}]"
Name_MetricReportDefinition = "MetricReportDefinition Schema File"
Schema_MetricReportDefinition = "#MetricReportDefinition.MetricReportDefinition"
####CONSR-OBMC-RDFT-0219-0001
resource_JSONSchema_odata = "/redfish/v1/JsonSchemas/odata"
odata_type_odata = "#JsonSchemaFile.v1_0_2.JsonSchemaFile"
Description_odata = "odata Schema File Location"
Id_odata = "odata"
Languages_odata = "['en']"
Languages_odata_count_odata = "1"
Location_odata_count_odata = "1"
Location_odata = "[{'Language': 'en', 'PublicationUri': 'http://redfish.dmtf.org/schemas/v1/odata.json', 'Uri': '/redfish/v1/JsonSchemas/odata/odata.json'}]"
Name_odata = "odata Schema File"
Schema_odata = "#odata.odata"
####CONSR-OBMC-RDFT-0221-0001
resource_JSONSchema_OperatingConfig = "/redfish/v1/JsonSchemas/OperatingConfig"
OperatingConfig_type_OperatingConfig = "#JsonSchemaFile.v1_0_2.JsonSchemaFile"
Description_OperatingConfig = "OperatingConfig Schema File Location"
Id_OperatingConfig = "OperatingConfig"
Languages_OperatingConfig = "['en']"
Languages_OperatingConfig_count_OperatingConfig = "1"
Location_OperatingConfig_count_OperatingConfig = "1"
Location_OperatingConfig = "[{'Language': 'en', 'PublicationUri': 'http://redfish.dmtf.org/schemas/v1/OperatingConfig.json', 'Uri': '/redfish/v1/JsonSchemas/OperatingConfig/OperatingConfig.json'}]"
Name_OperatingConfig = "OperatingConfig Schema File"
Schema_OperatingConfig = "#OperatingConfig.OperatingConfig"
####CONSR-OBMC-RDFT-0223-0001
resource_JSONSchema_PCIeDevice = "/redfish/v1/JsonSchemas/PCIeDevice"
PCIeDevice_type_PCIeDevice = "#JsonSchemaFile.v1_0_2.JsonSchemaFile"
Description_PCIeDevice = "PCIeDevice Schema File Location"
Id_PCIeDevice = "PCIeDevice"
Languages_PCIeDevice = "['en']"
Languages_PCIeDevice_count_PCIeDevice = "1"
Location_PCIeDevice_count_PCIeDevice = "1"
Location_PCIeDevice = "[{'Language': 'en', 'PublicationUri': 'http://redfish.dmtf.org/schemas/v1/PCIeDevice.json', 'Uri': '/redfish/v1/JsonSchemas/PCIeDevice/PCIeDevice.json'}]"
Name_PCIeDevice = "PCIeDevice Schema File"
Schema_PCIeDevice = "#PCIeDevice.PCIeDevice"
####CONSR-OBMC-RDFT-0225-0001
resource_JSONSchema_PCIeFunction = "/redfish/v1/JsonSchemas/PCIeFunction"
PCIeFunction_type_PCIeFunction = "#JsonSchemaFile.v1_0_2.JsonSchemaFile"
Description_PCIeFunction = "PCIeFunction Schema File Location"
Id_PCIeFunction = "PCIeFunction"
Languages_PCIeFunction = "['en']"
Languages_PCIeFunction_count_PCIeFunction = "1"
Location_PCIeFunction_count_PCIeFunction = "1"
Location_PCIeFunction = "[{'Language': 'en', 'PublicationUri': 'http://redfish.dmtf.org/schemas/v1/PCIeFunction.json', 'Uri': '/redfish/v1/JsonSchemas/PCIeFunction/PCIeFunction.json'}]"
Name_PCIeFunction = "PCIeFunction Schema File"
Schema_PCIeFunction = "#PCIeFunction.PCIeFunction"
####CONSR-OBMC-RDFT-0227-0001
resource_JSONSchema_PCIeSlots = "/redfish/v1/JsonSchemas/PCIeSlots"
PCIeSlots_type_PCIeSlots = "#JsonSchemaFile.v1_0_2.JsonSchemaFile"
Description_PCIeSlots = "PCIeSlots Schema File Location"
Id_PCIeSlots = "PCIeSlots"
Languages_PCIeSlots = "['en']"
Languages_PCIeSlots_count_PCIeSlots = "1"
Location_PCIeSlots_count_PCIeSlots = "1"
Location_PCIeSlots = "[{'Language': 'en', 'PublicationUri': 'http://redfish.dmtf.org/schemas/v1/PCIeSlots.json', 'Uri': '/redfish/v1/JsonSchemas/PCIeSlots/PCIeSlots.json'}]"
Name_PCIeSlots = "PCIeSlots Schema File"
Schema_PCIeSlots = "#PCIeSlots.PCIeSlots"
####CONSR-OBMC-RDFT-0229-0001
resource_JSONSchema_Port = "/redfish/v1/JsonSchemas/Port"
Port_type_Port = "#JsonSchemaFile.v1_0_2.JsonSchemaFile"
Description_Port = "Port Schema File Location"
Id_Port = "Port"
Languages_Port = "['en']"
Languages_Port_count_Port = "1"
Location_Port_count_Port = "1"
Location_Port = "[{'Language': 'en', 'PublicationUri': 'http://redfish.dmtf.org/schemas/v1/Port.json', 'Uri': '/redfish/v1/JsonSchemas/Port/Port.json'}]"
Name_Port = "Port Schema File"
Schema_Port = "#Port.Port"
####CONSR-OBMC-RDFT-0231-0001
resource_JSONSchema_Power = "/redfish/v1/JsonSchemas/Power"
Power_type_Power = "#JsonSchemaFile.v1_0_2.JsonSchemaFile"
Description_Power = "Power Schema File Location"
Id_Power = "Power"
Languages_Power = "['en']"
Languages_Power_count_Power = "1"
Location_Power_count_Power = "1"
Location_Power = "[{'Language': 'en', 'PublicationUri': 'http://redfish.dmtf.org/schemas/v1/Power.json', 'Uri': '/redfish/v1/JsonSchemas/Power/Power.json'}]"
Name_Power = "Power Schema File"
Schema_Power = "#Power.Power"
####CONSR-OBMC-RDFT-0233-0001
resource_JSONSchema_PowerSupply = "/redfish/v1/JsonSchemas/PowerSupply"
PowerSupply_type_PowerSupply = "#JsonSchemaFile.v1_0_2.JsonSchemaFile"
Description_PowerSupply = "PowerSupply Schema File Location"
Id_PowerSupply = "PowerSupply"
Languages_PowerSupply = "['en']"
Languages_PowerSupply_count_PowerSupply = "1"
Location_PowerSupply_count_PowerSupply = "1"
Location_PowerSupply = "[{'Language': 'en', 'PublicationUri': 'http://redfish.dmtf.org/schemas/v1/PowerSupply.json', 'Uri': '/redfish/v1/JsonSchemas/PowerSupply/PowerSupply.json'}]"
Name_PowerSupply = "PowerSupply Schema File"
Schema_PowerSupply = "#PowerSupply.PowerSupply"
####CONSR-OBMC-RDFT-0235-0001
resource_JSONSchema_Privileges = "/redfish/v1/JsonSchemas/Privileges"
Privileges_type_Privileges = "#JsonSchemaFile.v1_0_2.JsonSchemaFile"
Description_Privileges = "Privileges Schema File Location"
Id_Privileges = "Privileges"
Languages_Privileges = "['en']"
Languages_Privileges_count_Privileges = "1"
Location_Privileges_count_Privileges = "1"
Location_Privileges = "[{'Language': 'en', 'PublicationUri': 'http://redfish.dmtf.org/schemas/v1/Privileges.json', 'Uri': '/redfish/v1/JsonSchemas/Privileges/Privileges.json'}]"
Name_Privileges = "Privileges Schema File"
Schema_Privileges = "#Privileges.Privileges"
####CONSR-OBMC-RDFT-0237-0001
resource_JSONSchema_ProcessorCollection = "/redfish/v1/JsonSchemas/ProcessorCollection"
ProcessorCollection_type_ProcessorCollection = "#JsonSchemaFile.v1_0_2.JsonSchemaFile"
Description_ProcessorCollection = "ProcessorCollection Schema File Location"
Id_ProcessorCollection = "ProcessorCollection"
Languages_ProcessorCollection = "['en']"
Languages_ProcessorCollection_count_ProcessorCollection = "1"
Location_ProcessorCollection_count_ProcessorCollection = "1"
Location_ProcessorCollection = "[{'Language': 'en', 'PublicationUri': 'http://redfish.dmtf.org/schemas/v1/ProcessorCollection.json', 'Uri': '/redfish/v1/JsonSchemas/ProcessorCollection/ProcessorCollection.json'}]"
Name_ProcessorCollection = "ProcessorCollection Schema File"
Schema_ProcessorCollection = "#ProcessorCollection.ProcessorCollection"
####CONSR-OBMC-RDFT-0239-0001
resource_JSONSchema_redfish_payload_annotations = "/redfish/v1/JsonSchemas/redfish-payload-annotations"
redfish_payload_annotations_type_redfish_payload_annotations = "#JsonSchemaFile.v1_0_2.JsonSchemaFile"
Description_redfish_payload_annotations = "redfish-payload-annotations Schema File Location"
Id_redfish_payload_annotations = "redfish-payload-annotations"
Languages_redfish_payload_annotations = "['en']"
Languages_redfish_payload_annotations_count_redfish_payload_annotations = "1"
Location_redfish_payload_annotations_count_redfish_payload_annotations = "1"
Location_redfish_payload_annotations = "[{'Language': 'en', 'PublicationUri': 'http://redfish.dmtf.org/schemas/v1/redfish-payload-annotations.json', 'Uri': '/redfish/v1/JsonSchemas/redfish-payload-annotations/redfish-payload-annotations.json'}]"
Name_redfish_payload_annotations = "redfish-payload-annotations Schema File"
Schema_redfish_payload_annotations = "#redfish-payload-annotations.redfish-payload-annotations"
####CONSR-OBMC-RDFT-0241-0001
resource_JSONSchema_redfish_schema_v1 = "/redfish/v1/JsonSchemas/redfish-schema-v1"
redfish_schema_v1_type_redfish_schema_v1 = "#JsonSchemaFile.v1_0_2.JsonSchemaFile"
Description_redfish_schema_v1 = "redfish-schema-v1 Schema File Location"
Id_redfish_schema_v1 = "redfish-schema-v1"
Languages_redfish_schema_v1 = "['en']"
Languages_redfish_schema_v1_count_redfish_schema_v1 = "1"
Location_redfish_schema_v1_count_redfish_schema_v1 = "1"
Location_redfish_schema_v1 = "[{'Language': 'en', 'PublicationUri': 'http://redfish.dmtf.org/schemas/v1/redfish-schema-v1.json', 'Uri': '/redfish/v1/JsonSchemas/redfish-schema-v1/redfish-schema-v1.json'}]"
Name_redfish_schema_v1 = "redfish-schema-v1 Schema File"
Schema_redfish_schema_v1 = "#redfish-schema-v1.redfish-schema-v1"
####CONSR-OBMC-RDFT-0243-0001
resource_JSONSchema_Resource = "/redfish/v1/JsonSchemas/Resource"
Resource_type_Resource = "#JsonSchemaFile.v1_0_2.JsonSchemaFile"
Description_Resource = "Resource Schema File Location"
Id_Resource = "Resource"
Languages_Resource = "['en']"
Languages_Resource_count_Resource = "1"
Location_Resource_count_Resource = "1"
Location_Resource = "[{'Language': 'en', 'PublicationUri': 'http://redfish.dmtf.org/schemas/v1/Resource.json', 'Uri': '/redfish/v1/JsonSchemas/Resource/Resource.json'}]"
Name_Resource = "Resource Schema File"
Schema_Resource = "#Resource.Resource"
####CONSR-OBMC-RDFT-0245-0001
resource_JSONSchema_RoleCollection = "/redfish/v1/JsonSchemas/RoleCollection"
RoleCollection_type_RoleCollection = "#JsonSchemaFile.v1_0_2.JsonSchemaFile"
Description_RoleCollection = "RoleCollection Schema File Location"
Id_RoleCollection = "RoleCollection"
Languages_RoleCollection = "['en']"
Languages_RoleCollection_count_RoleCollection = "1"
Location_RoleCollection_count_RoleCollection = "1"
Location_RoleCollection = "[{'Language': 'en', 'PublicationUri': 'http://redfish.dmtf.org/schemas/v1/RoleCollection.json', 'Uri': '/redfish/v1/JsonSchemas/RoleCollection/RoleCollection.json'}]"
Name_RoleCollection = "RoleCollection Schema File"
Schema_RoleCollection = "#RoleCollection.RoleCollection"
####CONSR-OBMC-RDFT-0247-0001
resource_JSONSchema_SensorCollection = "/redfish/v1/JsonSchemas/SensorCollection"
SensorCollection_type_SensorCollection = "#JsonSchemaFile.v1_0_2.JsonSchemaFile"
Description_SensorCollection = "SensorCollection Schema File Location"
Id_SensorCollection = "SensorCollection"
Languages_SensorCollection = "['en']"
Languages_SensorCollection_count_SensorCollection = "1"
Location_SensorCollection_count_SensorCollection = "1"
Location_SensorCollection = "[{'Language': 'en', 'PublicationUri': 'http://redfish.dmtf.org/schemas/v1/SensorCollection.json', 'Uri': '/redfish/v1/JsonSchemas/SensorCollection/SensorCollection.json'}]"
Name_SensorCollection = "SensorCollection Schema File"
Schema_SensorCollection = "#SensorCollection.SensorCollection"
####CONSR-OBMC-RDFT-0249-0001
resource_JSONSchema_Session = "/redfish/v1/JsonSchemas/Session"
Session_type_Session = "#JsonSchemaFile.v1_0_2.JsonSchemaFile"
Description_Session = "Session Schema File Location"
Id_Session = "Session"
Languages_Session = "['en']"
Languages_Session_count_Session = "1"
Location_Session_count_Session = "1"
Location_Session = "[{'Language': 'en', 'PublicationUri': 'http://redfish.dmtf.org/schemas/v1/Session.json', 'Uri': '/redfish/v1/JsonSchemas/Session/Session.json'}]"
Name_Session = "Session Schema File"
Schema_Session = "#Session.Session"
####CONSR-OBMC-RDFT-0251-0001
resource_JSONSchema_SessionService = "/redfish/v1/JsonSchemas/SessionService"
SessionService_type_SessionService = "#JsonSchemaFile.v1_0_2.JsonSchemaFile"
Description_SessionService = "SessionService Schema File Location"
Id_SessionService = "SessionService"
Languages_SessionService = "['en']"
Languages_SessionService_count_SessionService = "1"
Location_SessionService_count_SessionService = "1"
Location_SessionService = "[{'Language': 'en', 'PublicationUri': 'http://redfish.dmtf.org/schemas/v1/SessionService.json', 'Uri': '/redfish/v1/JsonSchemas/SessionService/SessionService.json'}]"
Name_SessionService = "SessionService Schema File"
Schema_SessionService = "#SessionService.SessionService"
####CONSR-OBMC-RDFT-0253-0001
resource_JSONSchema_SoftwareInventory = "/redfish/v1/JsonSchemas/SoftwareInventory"
SoftwareInventory_type_SoftwareInventory = "#JsonSchemaFile.v1_0_2.JsonSchemaFile"
Description_SoftwareInventory = "SoftwareInventory Schema File Location"
Id_SoftwareInventory = "SoftwareInventory"
Languages_SoftwareInventory = "['en']"
Languages_SoftwareInventory_count_SoftwareInventory = "1"
Location_SoftwareInventory_count_SoftwareInventory = "1"
Location_SoftwareInventory = "[{'Language': 'en', 'PublicationUri': 'http://redfish.dmtf.org/schemas/v1/SoftwareInventory.json', 'Uri': '/redfish/v1/JsonSchemas/SoftwareInventory/SoftwareInventory.json'}]"
Name_SoftwareInventory = "SoftwareInventory Schema File"
Schema_SoftwareInventory = "#SoftwareInventory.SoftwareInventory"
####CONSR-OBMC-RDFT-0255-0001
resource_JSONSchema_Storage = "/redfish/v1/JsonSchemas/Storage"
Storage_type_Storage = "#JsonSchemaFile.v1_0_2.JsonSchemaFile"
Description_Storage = "Storage Schema File Location"
Id_Storage = "Storage"
Languages_Storage = "['en']"
Languages_Storage_count_Storage = "1"
Location_Storage_count_Storage = "1"
Location_Storage = "[{'Language': 'en', 'PublicationUri': 'http://redfish.dmtf.org/schemas/v1/Storage.json', 'Uri': '/redfish/v1/JsonSchemas/Storage/Storage.json'}]"
Name_Storage = "Storage Schema File"
Schema_Storage = "#Storage.Storage"
####CONSR-OBMC-RDFT-0257-0001
resource_JSONSchema_StorageController = "/redfish/v1/JsonSchemas/StorageController"
StorageController_type_StorageController = "#JsonSchemaFile.v1_0_2.JsonSchemaFile"
Description_StorageController = "StorageController Schema File Location"
Id_StorageController = "StorageController"
Languages_StorageController = "['en']"
Languages_StorageController_count_StorageController = "1"
Location_StorageController_count_StorageController = "1"
Location_StorageController = "[{'Language': 'en', 'PublicationUri': 'http://redfish.dmtf.org/schemas/v1/StorageController.json', 'Uri': '/redfish/v1/JsonSchemas/StorageController/StorageController.json'}]"
Name_StorageController = "StorageController Schema File"
Schema_StorageController = "#StorageController.StorageController"
####CONSR-OBMC-RDFT-0259-0001
resource_JSONSchema_Task = "/redfish/v1/JsonSchemas/Task"
Task_type_Task = "#JsonSchemaFile.v1_0_2.JsonSchemaFile"
Description_Task = "Task Schema File Location"
Id_Task = "Task"
Languages_Task = "['en']"
Languages_Task_count_Task = "1"
Location_Task_count_Task = "1"
Location_Task = "[{'Language': 'en', 'PublicationUri': 'http://redfish.dmtf.org/schemas/v1/Task.json', 'Uri': '/redfish/v1/JsonSchemas/Task/Task.json'}]"
Name_Task = "Task Schema File"
Schema_Task = "#Task.Task"
####CONSR-OBMC-RDFT-0261-0001
resource_JSONSchema_TaskService = "/redfish/v1/JsonSchemas/TaskService"
TaskService_type_TaskService = "#JsonSchemaFile.v1_0_2.JsonSchemaFile"
Description_TaskService = "TaskService Schema File Location"
Id_TaskService = "TaskService"
Languages_TaskService = "['en']"
Languages_TaskService_count_TaskService = "1"
Location_TaskService_count_TaskService = "1"
Location_TaskService = "[{'Language': 'en', 'PublicationUri': 'http://redfish.dmtf.org/schemas/v1/TaskService.json', 'Uri': '/redfish/v1/JsonSchemas/TaskService/TaskService.json'}]"
Name_TaskService_1 = "TaskService Schema File"
Schema_TaskService = "#TaskService.TaskService"
####CONSR-OBMC-RDFT-0263-0001
resource_JSONSchema_Thermal = "/redfish/v1/JsonSchemas/Thermal"
Thermal_type_Thermal = "#JsonSchemaFile.v1_0_2.JsonSchemaFile"
Description_Thermal = "Thermal Schema File Location"
Id_Thermal = "Thermal"
Languages_Thermal = "['en']"
Languages_Thermal_count_Thermal = "1"
Location_Thermal_count_Thermal = "1"
Location_Thermal = "[{'Language': 'en', 'PublicationUri': 'http://redfish.dmtf.org/schemas/v1/Thermal.json', 'Uri': '/redfish/v1/JsonSchemas/Thermal/Thermal.json'}]"
Name_Thermal = "Thermal Schema File"
Schema_Thermal = "#Thermal.Thermal"
####CONSR-OBMC-RDFT-0265-0001
resource_JSONSchema_ThermalSubsystem = "/redfish/v1/JsonSchemas/ThermalSubsystem"
ThermalSubsystem_type_ThermalSubsystem = "#JsonSchemaFile.v1_0_2.JsonSchemaFile"
Description_ThermalSubsystem = "ThermalSubsystem Schema File Location"
Id_ThermalSubsystem = "ThermalSubsystem"
Languages_ThermalSubsystem = "['en']"
Languages_ThermalSubsystem_count_ThermalSubsystem = "1"
Location_ThermalSubsystem_count_ThermalSubsystem = "1"
Location_ThermalSubsystem = "[{'Language': 'en', 'PublicationUri': 'http://redfish.dmtf.org/schemas/v1/ThermalSubsystem.json', 'Uri': '/redfish/v1/JsonSchemas/ThermalSubsystem/ThermalSubsystem.json'}]"
Name_ThermalSubsystem = "ThermalSubsystem Schema File"
Schema_ThermalSubsystem = "#ThermalSubsystem.ThermalSubsystem"
####CONSR-OBMC-RDFT-0267-0001
resource_JSONSchema_TriggersCollection = "/redfish/v1/JsonSchemas/TriggersCollection"
TriggersCollection_type_TriggersCollection = "#JsonSchemaFile.v1_0_2.JsonSchemaFile"
Description_TriggersCollection = "TriggersCollection Schema File Location"
Id_TriggersCollection = "TriggersCollection"
Languages_TriggersCollection = "['en']"
Languages_TriggersCollection_count_TriggersCollection = "1"
Location_TriggersCollection_count_TriggersCollection = "1"
Location_TriggersCollection = "[{'Language': 'en', 'PublicationUri': 'http://redfish.dmtf.org/schemas/v1/TriggersCollection.json', 'Uri': '/redfish/v1/JsonSchemas/TriggersCollection/TriggersCollection.json'}]"
Name_TriggersCollection = "TriggersCollection Schema File"
Schema_TriggersCollection = "#TriggersCollection.TriggersCollection"
####CONSR-OBMC-RDFT-0269-0001
resource_JSONSchema_VirtualMedia = "/redfish/v1/JsonSchemas/VirtualMedia"
VirtualMedia_type_VirtualMedia = "#JsonSchemaFile.v1_0_2.JsonSchemaFile"
Description_VirtualMedia = "VirtualMedia Schema File Location"
Id_VirtualMedia = "VirtualMedia"
Languages_VirtualMedia = "['en']"
Languages_VirtualMedia_count_VirtualMedia = "1"
Location_VirtualMedia_count_VirtualMedia = "1"
Location_VirtualMedia = "[{'Language': 'en', 'PublicationUri': 'http://redfish.dmtf.org/schemas/v1/VirtualMedia.json', 'Uri': '/redfish/v1/JsonSchemas/VirtualMedia/VirtualMedia.json'}]"
Name_VirtualMedia = "VirtualMedia Schema File"
Schema_VirtualMedia = "#VirtualMedia.VirtualMedia"
####CONSR-OBMC-RDFT-0038-0001
resource_Chasssis_Collection = "/redfish/v1/Chassis"
data_type_Chasssis_Collection = "#ChassisCollection.ChassisCollection"
Members_odata_count_Chasssis_Collection = "1"
Name_Chasssis_Collection = "Chassis Collection"
# CONSR-OBMC-RDFT-0272-0001
resource_sessionservice_Collection = "/redfish/v1/SessionService/Sessions/"
data_type_sessionservice_Collection = "#SessionCollection.SessionCollection"
Members_odata_count_sessionservice_Collection = "0"
Name_sessionservice_Collection = "Session Collection"
####CONSR-OBMC-RDFT-0274-0001
resource_MessageRegistry_Collection = "/redfish/v1/Registries"
data_type_MessageRegistry_Collection = "#MessageRegistryFileCollection.MessageRegistryFileCollection"
Members_odata_count_MessageRegistry_Collection = "4"
Description_MessageRegistry_Collection_1 = "Collection of MessageRegistryFiles"
Name_MessageRegistry_Collection_1 = "MessageRegistryFile Collection"
####CONSR-OBMC-RDFT-0278-0001
resource_MessageRegistry_4 = "/redfish/v1/Registries/TaskEvent/TaskEvent"
Redfish_Copyright_MessageRegistry_4 = "Copyright 2014-2020 DMTF in cooperation with the Storage Networking Industry Association (SNIA). All rights reserved."
data_type_MessageRegistry_4 = "#MessageRegistry.v1_4_1.MessageRegistry"
Description_MessageRegistry_4 = "This registry defines the messages for task related events."
Id_MessageRegistry_4 = "TaskEvent.1.0.3"
Language_MessageRegistry_4 = "en"
Name_MessageRegistry_4 = "Task Event Message Registry"
OwningEntity_MessageRegistry_4 = "DMTF"
RegistryPrefix_MessageRegistry_4 = "TaskEvent"
RegistryVersion_MessageRegistry_4 = "1.0.3"
Messages_MessageRegistry_4 = """{'TaskAborted': {'Description': 'A task has completed with errors.', 'Message': "The task with Id '%1' has completed with errors.", 'MessageSeverity': 'Critical', 'NumberOfArgs': 1, 'ParamTypes': ['string'], 'Resolution': 'None.', 'Severity': 'Critical'}, 'TaskCancelled': {'Description': 'A task has been cancelled.', 'Message': "Work on the task with Id '%1' has been halted prior to completion due to an explicit request.", 'MessageSeverity': 'Warning', 'NumberOfArgs': 1, 'ParamTypes': ['string'], 'Resolution': 'None.', 'Severity': 'Warning'}, 'TaskCompletedOK': {'Description': 'A task has completed.', 'Message': "The task with Id '%1' has completed.", 'MessageSeverity': 'OK', 'NumberOfArgs': 1, 'ParamTypes': ['string'], 'Resolution': 'None.', 'Severity': 'OK'}, 'TaskCompletedWarning': {'Description': 'A task has completed with warnings.', 'Message': "The task with Id '%1' has completed with warnings.", 'MessageSeverity': 'Warning', 'NumberOfArgs': 1, 'ParamTypes': ['string'], 'Resolution': 'None.', 'Severity': 'Warning'}, 'TaskPaused': {'Description': 'A task has been paused.', 'Message': "The task with Id '%1' has been paused.", 'MessageSeverity': 'Warning', 'NumberOfArgs': 1, 'ParamTypes': ['string'], 'Resolution': 'None.', 'Severity': 'Warning'}, 'TaskProgressChanged': {'Description': 'A task has changed progress.', 'Message': "The task with Id '%1' has changed to progress %2 percent complete.", 'MessageSeverity': 'OK', 'NumberOfArgs': 2, 'ParamTypes': ['string', 'number'], 'Resolution': 'None.', 'Severity': 'OK'}, 'TaskRemoved': {'Description': 'A task has been removed.', 'Message': "The task with Id '%1' has been removed.", 'MessageSeverity': 'Warning', 'NumberOfArgs': 1, 'ParamTypes': ['string'], 'Resolution': 'None.', 'Severity': 'Warning'}, 'TaskResumed': {'Description': 'A task has been resumed.', 'Message': "The task with Id '%1' has been resumed.", 'MessageSeverity': 'OK', 'NumberOfArgs': 1, 'ParamTypes': ['string'], 'Resolution': 'None.', 'Severity': 'OK'}, 'TaskStarted': {'Description': 'A task has started.', 'Message': "The task with Id '%1' has started.", 'MessageSeverity': 'OK', 'NumberOfArgs': 1, 'ParamTypes': ['string'], 'Resolution': 'None.', 'Severity': 'OK'}}"""
####CONSR-OBMC-RDFT-0280-0001
resource_MessageRegistry_6 = "/redfish/v1/Registries/ResourceEvent/ResourceEvent"
Redfish_Copyright_MessageRegistry_6 = "Copyright 2014-2023 DMTF in cooperation with the Storage Networking Industry Association (SNIA). All rights reserved."
data_type_MessageRegistry_6 = "#MessageRegistry.v1_6_0.MessageRegistry"
Description_MessageRegistry_6 = "This registry defines the messages to use for resource events."
Id_MessageRegistry_6 = "ResourceEvent.1.3.0"
Language_MessageRegistry_6 = "en"
Name_MessageRegistry_6 = "Resource Event Message Registry"
OwningEntity_MessageRegistry_6 = "DMTF"
RegistryPrefix_MessageRegistry_6 = "ResourceEvent"
RegistryVersion_MessageRegistry_6 = "1.3.0"
Messages_MessageRegistry_6 = """{'AggregationSourceDiscovered': {'Description': 'Indicates that a new aggregation source has been discovered.', 'Message': 'A aggregation source of connection method `%1` located at `%2` has been discovered.', 'MessageSeverity': 'OK', 'NumberOfArgs': 2, 'ParamTypes': ['string', 'string'], 'Resolution': 'The aggregation source is available to the service and can be identified using the identified connection method.', 'Severity': 'OK'}, 'LicenseAdded': {'Description': 'Indicates that a license has been added.', 'Message': "A license for '%1' has been added.  The following message was returned: '%2'.", 'MessageSeverity': 'OK', 'NumberOfArgs': 2, 'ParamTypes': ['string', 'string'], 'Resolution': 'See vendor specific instructions for specific actions.', 'Severity': 'OK'}, 'LicenseChanged': {'Description': 'Indicates that a license has changed.', 'Message': "A license for '%1' has changed.  The following message was returned: '%2'.", 'MessageSeverity': 'Warning', 'NumberOfArgs': 2, 'ParamTypes': ['string', 'string'], 'Resolution': 'See vendor specific instructions for specific actions.', 'Severity': 'Warning'}, 'LicenseExpired': {'Description': 'Indicates that a license has expired.', 'Message': "A license for '%1' has expired.  The following message was returned: '%2'.", 'MessageSeverity': 'Warning', 'NumberOfArgs': 2, 'ParamTypes': ['string', 'string'], 'Resolution': 'See vendor specific instructions for specific actions.', 'Severity': 'Warning'}, 'ResourceChanged': {'Description': 'Indicates that one or more resource properties have changed.  This is not used whenever there is another event message for that specific change, such as only the state has changed.', 'Message': 'One or more resource properties have changed.', 'MessageSeverity': 'OK', 'NumberOfArgs': 0, 'Resolution': 'None.', 'Severity': 'OK'}, 'ResourceCreated': {'Description': 'Indicates that all conditions of a successful creation operation have been met.', 'Message': 'The resource has been created successfully.', 'MessageSeverity': 'OK', 'NumberOfArgs': 0, 'Resolution': 'None', 'Severity': 'OK'}, 'ResourceErrorThresholdCleared': {'Description': 'Indicates that a specified resource property has cleared its error threshold.  Examples would be drive I/O errors, or network link errors.', 'Message': 'The resource property %1 has cleared the error threshold of value %2.', 'MessageSeverity': 'OK', 'NumberOfArgs': 2, 'ParamTypes': ['string', 'number'], 'Resolution': 'None.', 'Severity': 'OK'}, 'ResourceErrorThresholdExceeded': {'Description': 'Indicates that a specified resource property has exceeded its error threshold.  Examples would be drive I/O errors, or network link errors.', 'Message': 'The resource property %1 has exceeded error threshold of value %2.', 'MessageSeverity': 'Critical', 'NumberOfArgs': 2, 'ParamTypes': ['string', 'number'], 'Resolution': 'None.', 'Severity': 'Critical'}, 'ResourceErrorsCorrected': {'Description': 'Indicates that a specified resource property has corrected errors.  Examples would be drive I/O errors, or network link errors.', 'Message': "The resource property %1 has corrected errors of type '%2'.", 'MessageSeverity': 'OK', 'NumberOfArgs': 2, 'ParamTypes': ['string', 'string'], 'Resolution': 'None.', 'Severity': 'OK'}, 'ResourceErrorsDetected': {'Description': 'Indicates that a specified resource property has detected errors.  Examples would be drive I/O errors, or network link errors.', 'Message': "The resource property %1 has detected errors of type '%2'.", 'MessageSeverity': 'Warning', 'NumberOfArgs': 2, 'ParamTypes': ['string', 'string'], 'Resolution': 'Resolution dependent upon error type.', 'Severity': 'Warning'}, 'ResourcePaused': {'Description': 'Indicates that the power state of a resource has changed to paused.', 'Message': 'The resource `%1` has been paused.', 'MessageSeverity': 'OK', 'NumberOfArgs': 1, 'ParamTypes': ['string'], 'Resolution': 'None.', 'Severity': 'OK'}, 'ResourcePoweredOff': {'Description': 'Indicates that the power state of a resource has changed to powered off.', 'Message': 'The resource `%1` has powered off.', 'MessageSeverity': 'OK', 'NumberOfArgs': 1, 'ParamTypes': ['string'], 'Resolution': 'None.', 'Severity': 'OK'}, 'ResourcePoweredOn': {'Description': 'Indicates that the power state of a resource has changed to powered on.', 'Message': 'The resource `%1` has powered on.', 'MessageSeverity': 'OK', 'NumberOfArgs': 1, 'ParamTypes': ['string'], 'Resolution': 'None.', 'Severity': 'OK'}, 'ResourcePoweringOff': {'Description': 'Indicates that the power state of a resource has changed to powering off.', 'Message': 'The resource `%1` is powering off.', 'MessageSeverity': 'OK', 'NumberOfArgs': 1, 'ParamTypes': ['string'], 'Resolution': 'None.', 'Severity': 'OK'}, 'ResourcePoweringOn': {'Description': 'Indicates that the power state of a resource has changed to powering on.', 'Message': 'The resource `%1` is powering on.', 'MessageSeverity': 'OK', 'NumberOfArgs': 1, 'ParamTypes': ['string'], 'Resolution': 'None.', 'Severity': 'OK'}, 'ResourceRemoved': {'Description': 'Indicates that all conditions of a successful remove operation have been met.', 'Message': 'The resource has been removed successfully.', 'MessageSeverity': 'OK', 'NumberOfArgs': 0, 'Resolution': 'None', 'Severity': 'OK'}, 'ResourceSelfTestCompleted': {'Description': 'Indicates that a self-test has completed.', 'Message': 'A self-test has completed.', 'MessageSeverity': 'OK', 'NumberOfArgs': 0, 'Resolution': 'None.', 'Severity': 'OK'}, 'ResourceSelfTestFailed': {'Description': 'Indicates that a self-test has failed.  Suggested resolution may be provided as OEM data.', 'Message': "A self-test has failed.  The following message was returned: '%1'.", 'MessageSeverity': 'Critical', 'NumberOfArgs': 1, 'ParamTypes': ['string'], 'Resolution': 'See vendor specific instructions for specific actions.', 'Severity': 'Critical'}, 'ResourceStateChanged': {'Description': 'Indicates that the state of a resource has changed.', 'Message': 'The state of resource `%1` has changed to %2.', 'MessageSeverity': 'OK', 'NumberOfArgs': 2, 'ParamTypes': ['string', 'string'], 'Resolution': 'None.', 'Severity': 'OK'}, 'ResourceStatusChangedCritical': {'Description': 'Indicates that the health of a resource has changed to Critical.', 'Message': 'The health of resource `%1` has changed to %2.', 'MessageSeverity': 'Critical', 'NumberOfArgs': 2, 'ParamTypes': ['string', 'string'], 'Resolution': 'None.', 'Severity': 'Critical'}, 'ResourceStatusChangedOK': {'Description': 'Indicates that the health of a resource has changed to OK.', 'Message': "The health of resource '%1' has changed to %2.", 'MessageSeverity': 'OK', 'NumberOfArgs': 2, 'ParamTypes': ['string', 'string'], 'Resolution': 'None.', 'Severity': 'OK'}, 'ResourceStatusChangedWarning': {'Description': 'Indicates that the health of a resource has changed to Warning.', 'Message': 'The health of resource `%1` has changed to %2.', 'MessageSeverity': 'Warning', 'NumberOfArgs': 2, 'ParamTypes': ['string', 'string'], 'Resolution': 'None.', 'Severity': 'Warning'}, 'ResourceVersionIncompatible': {'Description': 'Indicates that an incompatible version of software has been detected.  Examples may be after a component or system level software update.', 'Message': "An incompatible version of software '%1' has been detected.", 'MessageSeverity': 'Warning', 'NumberOfArgs': 1, 'ParamTypes': ['string'], 'Resolution': 'Compare the version of the resource with the compatible version of the software.', 'Severity': 'Warning'}, 'ResourceWarningThresholdCleared': {'Description': 'Indicates that a specified resource property has cleared its warning threshold.  Examples would be drive I/O errors, or network link errors.  Suggested resolution may be provided as OEM data.', 'Message': 'The resource property %1 has cleared the warning threshold of value %2.', 'MessageSeverity': 'OK', 'NumberOfArgs': 2, 'ParamTypes': ['string', 'number'], 'Resolution': 'None.', 'Severity': 'OK'}, 'ResourceWarningThresholdExceeded': {'Description': 'Indicates that a specified resource property has exceeded its warning threshold.  Examples would be drive I/O errors, or network link errors.  Suggested resolution may be provided as OEM data.', 'Message': 'The resource property %1 has exceeded its warning threshold of value %2.', 'MessageSeverity': 'Warning', 'NumberOfArgs': 2, 'ParamTypes': ['string', 'number'], 'Resolution': 'None.', 'Severity': 'Warning'}, 'TestMessage': {'Description': 'A test message used to validate event delivery mechanisms.', 'Message': 'Test message.', 'MessageSeverity': 'OK', 'NumberOfArgs': 0, 'Resolution': 'None.', 'Severity': 'OK'}, 'URIForResourceChanged': {'Description': 'Indicates that the URI for a resource has changed.  Examples for this would be physical component replacement or redistribution.', 'Message': 'The URI for the resource has changed.', 'MessageSeverity': 'OK', 'NumberOfArgs': 0, 'Resolution': 'None.', 'Severity': 'OK'}}"""
####CONSR-OBMC-RDFT-0282-0001
resource_MessageRegistry_8 = "/redfish/v1/Registries/OpenBMC/OpenBMC"
Redfish_Copyright_MessageRegistry_8 = "Copyright 2014-2020 DMTF in cooperation with the Storage Networking Industry Association (SNIA). All rights reserved."
data_type_MessageRegistry_8 = "#MessageRegistry.v1_6_0.MessageRegistry"
Description_MessageRegistry_8 = "This registry defines the messages to use for resource events."
Id_MessageRegistry_8 = "ResourceEvent.1.3.0"
Language_MessageRegistry_8 = "en"
Name_MessageRegistry_8 = "Resource Event Message Registry"
OwningEntity_MessageRegistry_8 = "DMTF"
RegistryPrefix_MessageRegistry_8 = "ResourceEvent"
RegistryVersion_MessageRegistry_8 = "1.3.0"
Messages_MessageRegistry_8 = """{'AggregationSourceDiscovered': {'Description': 'Indicates that a new aggregation source has been discovered.', 'Message': 'A aggregation source of connection method `%1` located at `%2` has been discovered.', 'MessageSeverity': 'OK', 'NumberOfArgs': 2, 'ParamTypes': ['string', 'string'], 'Resolution': 'The aggregation source is available to the service and can be identified using the identified connection method.', 'Severity': 'OK'}, 'LicenseAdded': {'Description': 'Indicates that a license has been added.', 'Message': "A license for '%1' has been added.  The following message was returned: '%2'.", 'MessageSeverity': 'OK', 'NumberOfArgs': 2, 'ParamTypes': ['string', 'string'], 'Resolution': 'See vendor specific instructions for specific actions.', 'Severity': 'OK'}, 'LicenseChanged': {'Description': 'Indicates that a license has changed.', 'Message': "A license for '%1' has changed.  The following message was returned: '%2'.", 'MessageSeverity': 'Warning', 'NumberOfArgs': 2, 'ParamTypes': ['string', 'string'], 'Resolution': 'See vendor specific instructions for specific actions.', 'Severity': 'Warning'}, 'LicenseExpired': {'Description': 'Indicates that a license has expired.', 'Message': "A license for '%1' has expired.  The following message was returned: '%2'.", 'MessageSeverity': 'Warning', 'NumberOfArgs': 2, 'ParamTypes': ['string', 'string'], 'Resolution': 'See vendor specific instructions for specific actions.', 'Severity': 'Warning'}, 'ResourceChanged': {'Description': 'Indicates that one or more resource properties have changed.  This is not used whenever there is another event message for that specific change, such as only the state has changed.', 'Message': 'One or more resource properties have changed.', 'MessageSeverity': 'OK', 'NumberOfArgs': 0, 'Resolution': 'None.', 'Severity': 'OK'}, 'ResourceCreated': {'Description': 'Indicates that all conditions of a successful creation operation have been met.', 'Message': 'The resource has been created successfully.', 'MessageSeverity': 'OK', 'NumberOfArgs': 0, 'Resolution': 'None', 'Severity': 'OK'}, 'ResourceErrorThresholdCleared': {'Description': 'Indicates that a specified resource property has cleared its error threshold.  Examples would be drive I/O errors, or network link errors.', 'Message': 'The resource property %1 has cleared the error threshold of value %2.', 'MessageSeverity': 'OK', 'NumberOfArgs': 2, 'ParamTypes': ['string', 'number'], 'Resolution': 'None.', 'Severity': 'OK'}, 'ResourceErrorThresholdExceeded': {'Description': 'Indicates that a specified resource property has exceeded its error threshold.  Examples would be drive I/O errors, or network link errors.', 'Message': 'The resource property %1 has exceeded error threshold of value %2.', 'MessageSeverity': 'Critical', 'NumberOfArgs': 2, 'ParamTypes': ['string', 'number'], 'Resolution': 'None.', 'Severity': 'Critical'}, 'ResourceErrorsCorrected': {'Description': 'Indicates that a specified resource property has corrected errors.  Examples would be drive I/O errors, or network link errors.', 'Message': "The resource property %1 has corrected errors of type '%2'.", 'MessageSeverity': 'OK', 'NumberOfArgs': 2, 'ParamTypes': ['string', 'string'], 'Resolution': 'None.', 'Severity': 'OK'}, 'ResourceErrorsDetected': {'Description': 'Indicates that a specified resource property has detected errors.  Examples would be drive I/O errors, or network link errors.', 'Message': "The resource property %1 has detected errors of type '%2'.", 'MessageSeverity': 'Warning', 'NumberOfArgs': 2, 'ParamTypes': ['string', 'string'], 'Resolution': 'Resolution dependent upon error type.', 'Severity': 'Warning'}, 'ResourcePaused': {'Description': 'Indicates that the power state of a resource has changed to paused.', 'Message': 'The resource `%1` has been paused.', 'MessageSeverity': 'OK', 'NumberOfArgs': 1, 'ParamTypes': ['string'], 'Resolution': 'None.', 'Severity': 'OK'}, 'ResourcePoweredOff': {'Description': 'Indicates that the power state of a resource has changed to powered off.', 'Message': 'The resource `%1` has powered off.', 'MessageSeverity': 'OK', 'NumberOfArgs': 1, 'ParamTypes': ['string'], 'Resolution': 'None.', 'Severity': 'OK'}, 'ResourcePoweredOn': {'Description': 'Indicates that the power state of a resource has changed to powered on.', 'Message': 'The resource `%1` has powered on.', 'MessageSeverity': 'OK', 'NumberOfArgs': 1, 'ParamTypes': ['string'], 'Resolution': 'None.', 'Severity': 'OK'}, 'ResourcePoweringOff': {'Description': 'Indicates that the power state of a resource has changed to powering off.', 'Message': 'The resource `%1` is powering off.', 'MessageSeverity': 'OK', 'NumberOfArgs': 1, 'ParamTypes': ['string'], 'Resolution': 'None.', 'Severity': 'OK'}, 'ResourcePoweringOn': {'Description': 'Indicates that the power state of a resource has changed to powering on.', 'Message': 'The resource `%1` is powering on.', 'MessageSeverity': 'OK', 'NumberOfArgs': 1, 'ParamTypes': ['string'], 'Resolution': 'None.', 'Severity': 'OK'}, 'ResourceRemoved': {'Description': 'Indicates that all conditions of a successful remove operation have been met.', 'Message': 'The resource has been removed successfully.', 'MessageSeverity': 'OK', 'NumberOfArgs': 0, 'Resolution': 'None', 'Severity': 'OK'}, 'ResourceSelfTestCompleted': {'Description': 'Indicates that a self-test has completed.', 'Message': 'A self-test has completed.', 'MessageSeverity': 'OK', 'NumberOfArgs': 0, 'Resolution': 'None.', 'Severity': 'OK'}, 'ResourceSelfTestFailed': {'Description': 'Indicates that a self-test has failed.  Suggested resolution may be provided as OEM data.', 'Message': "A self-test has failed.  The following message was returned: '%1'.", 'MessageSeverity': 'Critical', 'NumberOfArgs': 1, 'ParamTypes': ['string'], 'Resolution': 'See vendor specific instructions for specific actions.', 'Severity': 'Critical'}, 'ResourceStateChanged': {'Description': 'Indicates that the state of a resource has changed.', 'Message': 'The state of resource `%1` has changed to %2.', 'MessageSeverity': 'OK', 'NumberOfArgs': 2, 'ParamTypes': ['string', 'string'], 'Resolution': 'None.', 'Severity': 'OK'}, 'ResourceStatusChangedCritical': {'Description': 'Indicates that the health of a resource has changed to Critical.', 'Message': 'The health of resource `%1` has changed to %2.', 'MessageSeverity': 'Critical', 'NumberOfArgs': 2, 'ParamTypes': ['string', 'string'], 'Resolution': 'None.', 'Severity': 'Critical'}, 'ResourceStatusChangedOK': {'Description': 'Indicates that the health of a resource has changed to OK.', 'Message': "The health of resource '%1' has changed to %2.", 'MessageSeverity': 'OK', 'NumberOfArgs': 2, 'ParamTypes': ['string', 'string'], 'Resolution': 'None.', 'Severity': 'OK'}, 'ResourceStatusChangedWarning': {'Description': 'Indicates that the health of a resource has changed to Warning.', 'Message': 'The health of resource `%1` has changed to %2.', 'MessageSeverity': 'Warning', 'NumberOfArgs': 2, 'ParamTypes': ['string', 'string'], 'Resolution': 'None.', 'Severity': 'Warning'}, 'ResourceVersionIncompatible': {'Description': 'Indicates that an incompatible version of software has been detected.  Examples may be after a component or system level software update.', 'Message': "An incompatible version of software '%1' has been detected.", 'MessageSeverity': 'Warning', 'NumberOfArgs': 1, 'ParamTypes': ['string'], 'Resolution': 'Compare the version of the resource with the compatible version of the software.', 'Severity': 'Warning'}, 'ResourceWarningThresholdCleared': {'Description': 'Indicates that a specified resource property has cleared its warning threshold.  Examples would be drive I/O errors, or network link errors.  Suggested resolution may be provided as OEM data.', 'Message': 'The resource property %1 has cleared the warning threshold of value %2.', 'MessageSeverity': 'OK', 'NumberOfArgs': 2, 'ParamTypes': ['string', 'number'], 'Resolution': 'None.', 'Severity': 'OK'}, 'ResourceWarningThresholdExceeded': {'Description': 'Indicates that a specified resource property has exceeded its warning threshold.  Examples would be drive I/O errors, or network link errors.  Suggested resolution may be provided as OEM data.', 'Message': 'The resource property %1 has exceeded its warning threshold of value %2.', 'MessageSeverity': 'Warning', 'NumberOfArgs': 2, 'ParamTypes': ['string', 'number'], 'Resolution': 'None.', 'Severity': 'Warning'}, 'TestMessage': {'Description': 'A test message used to validate event delivery mechanisms.', 'Message': 'Test message.', 'MessageSeverity': 'OK', 'NumberOfArgs': 0, 'Resolution': 'None.', 'Severity': 'OK'}, 'URIForResourceChanged': {'Description': 'Indicates that the URI for a resource has changed.  Examples for this would be physical component replacement or redistribution.', 'Message': 'The URI for the resource has changed.', 'MessageSeverity': 'OK', 'NumberOfArgs': 0, 'Resolution': 'None.', 'Severity': 'OK'}}"""
####CONSR-OBMC-RDFT-0276-0001
resource_MessageRegistry_2 = "/redfish/v1/Registries/Base/Base"
Redfish_Copyright_MessageRegistry_2 = "Copyright 2014-2023 DMTF. All rights reserved."
data_type_MessageRegistry_2 = "#MessageRegistry.v1_5_0.MessageRegistry"
Description_MessageRegistry_2 = "This registry defines the base messages for Redfish"
Id_MessageRegistry_2 = "Base.1.16.0"
Language_MessageRegistry_2 = "en"
Name_MessageRegistry_2 = "Base Message Registry"
OwningEntity_MessageRegistry_2 = "DMTF"
RegistryPrefix_MessageRegistry_2 = "Base"
RegistryVersion_MessageRegistry_2 = "1.16.0"
Messages_MessageRegistry_2 = """{'AccessDenied': {'Description': 'Indicates that while attempting to access, connect to, or transfer to or from another resource, the service denied access.', 'Message': "While attempting to establish a connection to '%1', the service denied access.", 'MessageSeverity': 'Critical', 'NumberOfArgs': 1, 'ParamTypes': ['string'], 'Resolution': 'Attempt to ensure that the URI is correct and that the service has the appropriate credentials.', 'Severity': 'Critical'}, 'AccountForSessionNoLongerExists': {'Description': 'Indicates that the account for the session has been removed, thus the session has been removed as well.', 'Message': 'The account for the current session has been removed, thus the current session has been removed as well.', 'MessageSeverity': 'OK', 'NumberOfArgs': 0, 'Resolution': 'Attempt to connect with a valid account.', 'Severity': 'OK'}, 'AccountModified': {'Description': 'Indicates that the account was successfully modified.', 'Message': 'The account was successfully modified.', 'MessageSeverity': 'OK', 'NumberOfArgs': 0, 'Resolution': 'No resolution is required.', 'Severity': 'OK'}, 'AccountNotModified': {'Description': 'Indicates that the modification requested for the account was not successful.', 'Message': 'The account modification request failed.', 'MessageSeverity': 'Warning', 'NumberOfArgs': 0, 'Resolution': 'The modification may have failed due to permission issues or issues with the request body.', 'Severity': 'Warning'}, 'AccountRemoved': {'Description': 'Indicates that the account was successfully removed.', 'Message': 'The account was successfully removed.', 'MessageSeverity': 'OK', 'NumberOfArgs': 0, 'Resolution': 'No resolution is required.', 'Severity': 'OK'}, 'ActionDeprecated': {'Description': 'Indicates the action is deprecated.', 'Message': 'The action %1 is deprecated.', 'MessageSeverity': 'Warning', 'NumberOfArgs': 1, 'ParamTypes': ['string'], 'Resolution': 'Refer to the schema guide for more information.', 'Severity': 'Warning'}, 'ActionNotSupported': {'Description': 'Indicates that the action supplied with the POST operation is not supported by the resource.', 'Message': 'The action %1 is not supported by the resource.', 'MessageSeverity': 'Critical', 'NumberOfArgs': 1, 'ParamTypes': ['string'], 'Resolution': 'The action supplied cannot be resubmitted to the implementation.  Perhaps the action was invalid, the wrong resource was the target or the implementation documentation may be of assistance.', 'Severity': 'Critical'}, 'ActionParameterDuplicate': {'Description': 'Indicates that the action was supplied with a duplicated action parameter in the request body.', 'Message': 'The action %1 was submitted with more than one value for the parameter %2.', 'MessageSeverity': 'Warning', 'NumberOfArgs': 2, 'ParamTypes': ['string', 'string'], 'Resolution': 'Resubmit the action with only one instance of the action parameter in the request body if the operation failed.', 'Severity': 'Warning'}, 'ActionParameterMissing': {'Description': 'Indicates that the action requested was missing an action parameter that is required to process the action.', 'Message': 'The action %1 requires the parameter %2 to be present in the request body.', 'MessageSeverity': 'Critical', 'NumberOfArgs': 2, 'ParamTypes': ['string', 'string'], 'Resolution': 'Supply the action with the required parameter in the request body when the request is resubmitted.', 'Severity': 'Critical'}, 'ActionParameterNotSupported': {'Description': 'Indicates that the parameter supplied for the action is not supported on the resource.', 'Message': 'The parameter %1 for the action %2 is not supported on the target resource.', 'MessageSeverity': 'Warning', 'NumberOfArgs': 2, 'ParamTypes': ['string', 'string'], 'Resolution': 'Remove the parameter supplied and resubmit the request if the operation failed.', 'Severity': 'Warning'}, 'ActionParameterUnknown': {'Description': 'Indicates that an action was submitted but an action parameter supplied did not match any of the known parameters.', 'Message': 'The action %1 was submitted with the invalid parameter %2.', 'MessageSeverity': 'Warning', 'NumberOfArgs': 2, 'ParamTypes': ['string', 'string'], 'Resolution': 'Correct the invalid action parameter and resubmit the request if the operation failed.', 'Severity': 'Warning'}, 'ActionParameterValueConflict': {'Description': 'Indicates that the requested parameter value could not be completed, because of a mismatch with other parameters or properties in the resource.', 'Message': "The parameter '%1' with the requested value of '%2' does not meet the constraints of the implementation.", 'MessageSeverity': 'Warning', 'NumberOfArgs': 2, 'ParamTypes': ['string', 'string'], 'Resolution': 'No resolution is required.', 'Severity': 'Warning'}, 'ActionParameterValueError': {'Description': 'Indicates that a parameter was given an invalid value.', 'Message': 'The value for the parameter %1 in the action %2 is invalid.', 'MessageSeverity': 'Warning', 'NumberOfArgs': 2, 'ParamTypes': ['string', 'string'], 'Resolution': 'Correct the value for the parameter in the request body and resubmit the request if the operation failed.', 'Severity': 'Warning'}, 'ActionParameterValueFormatError': {'Description': 'Indicates that a parameter was given the correct value type but the value of that parameter was not supported.  This includes the value size or length has been exceeded.', 'Message': "The value '%1' for the parameter %2 in the action %3 is of a different format than the parameter can accept.", 'MessageSeverity': 'Warning', 'NumberOfArgs': 3, 'ParamTypes': ['string', 'string', 'string'], 'Resolution': 'Correct the value for the parameter in the request body and resubmit the request if the operation failed.', 'Severity': 'Warning'}, 'ActionParameterValueNotInList': {'Description': 'Indicates that a parameter was given the correct value type but the value of that parameter was not supported.  The value is not in an enumeration.', 'Message': "The value '%1' for the parameter %2 in the action %3 is not in the list of acceptable values.", 'MessageSeverity': 'Warning', 'NumberOfArgs': 3, 'ParamTypes': ['string', 'string', 'string'], 'Resolution': 'Choose a value from the enumeration list that the implementation can support and resubmit the request if the operation failed.', 'Severity': 'Warning'}, 'ActionParameterValueTypeError': {'Description': 'Indicates that a parameter was given the wrong value type, such as when a number is supplied for a parameter that requires a string.', 'Message': "The value '%1' for the parameter %2 in the action %3 is of a different type than the parameter can accept.", 'MessageSeverity': 'Warning', 'NumberOfArgs': 3, 'ParamTypes': ['string', 'string', 'string'], 'Resolution': 'Correct the value for the parameter in the request body and resubmit the request if the operation failed.', 'Severity': 'Warning'}, 'ArraySizeTooLong': {'Description': 'Indicates that the size of the array exceeded the maximum number of elements.', 'Message': 'The array provided for property %1 exceeds the size limit %2.', 'MessageSeverity': 'Warning', 'NumberOfArgs': 2, 'ParamTypes': ['string', 'number'], 'Resolution': 'Resubmit the request with an appropriate array size.', 'Severity': 'Warning'}, 'ArraySizeTooShort': {'Description': 'Indicates that the size of the array is under the minimum number of elements.', 'Message': 'The array provided for property %1 is under the minimum size limit %2.', 'MessageSeverity': 'Warning', 'NumberOfArgs': 2, 'ParamTypes': ['string', 'number'], 'Resolution': 'Resubmit the request with an appropriate array size.', 'Severity': 'Warning'}, 'AuthenticationTokenRequired': {'Description': 'Indicates that the request could not be performed because an authentication token was not provided.', 'Message': 'The request could not be performed because an authentication token was not provided.', 'MessageSeverity': 'Critical', 'NumberOfArgs': 0, 'Resolution': 'Obtain an authentication token and resubmit the request.', 'Severity': 'Critical'}, 'ChassisPowerStateOffRequired': {'Description': 'Indicates that the request requires a specified chassis to be powered off.', 'Message': "The Chassis with Id '%1' requires to be powered off to perform this request.", 'MessageSeverity': 'Warning', 'NumberOfArgs': 1, 'ParamTypes': ['string'], 'Resolution': 'Power off the specified chassis and resubmit the request.', 'Severity': 'Warning'}, 'ChassisPowerStateOnRequired': {'Description': 'Indicates that the request requires a specified chassis to be powered on.', 'Message': "The chassis with Id '%1' requires to be powered on to perform this request.", 'MessageSeverity': 'Warning', 'NumberOfArgs': 1, 'ParamTypes': ['string'], 'Resolution': 'Power on the specified chassis and resubmit the request.', 'Severity': 'Warning'}, 'ConditionInRelatedResource': {'Description': 'Indicates that one or more fault or error conditions exist in a related resource.', 'Message': 'One or more conditions exist in a related resource.  See the OriginOfCondition property.', 'MessageSeverity': 'Warning', 'NumberOfArgs': 0, 'Resolution': 'Check the Conditions array in the resource shown in the OriginOfCondition property to determine the conditions that need attention.', 'Severity': 'Warning'}, 'CouldNotEstablishConnection': {'Description': 'Indicates that the attempt to access the resource, file, or image at the URI was unsuccessful because a session could not be established.', 'Message': "The service failed to establish a connection with the URI '%1'.", 'MessageSeverity': 'Critical', 'NumberOfArgs': 1, 'ParamTypes': ['string'], 'Resolution': 'Ensure that the URI contains a valid and reachable node name, protocol information and other URI components.', 'Severity': 'Critical'}, 'CreateFailedMissingReqProperties': {'Description': 'Indicates that a create was attempted on a resource but that properties that are required for the create operation were missing from the request.', 'Message': 'The create operation failed because the required property %1 was missing from the request.', 'MessageSeverity': 'Critical', 'NumberOfArgs': 1, 'ParamTypes': ['string'], 'Resolution': 'Correct the body to include the required property with a valid value and resubmit the request if the operation failed.', 'Severity': 'Critical'}, 'CreateLimitReachedForResource': {'Description': 'Indicates that no more resources can be created on the resource as it has reached its create limit.', 'Message': 'The create operation failed because the resource has reached the limit of possible resources.', 'MessageSeverity': 'Critical', 'NumberOfArgs': 0, 'Resolution': 'Either delete resources and resubmit the request if the operation failed or do not resubmit the request.', 'Severity': 'Critical'}, 'Created': {'Description': 'Indicates that all conditions of a successful create operation have been met.', 'Message': 'The resource has been created successfully.', 'MessageSeverity': 'OK', 'NumberOfArgs': 0, 'Resolution': 'None.', 'Severity': 'OK'}, 'EmptyJSON': {'Description': 'Indicates that the request body contained an empty JSON object when one or more properties are expected in the body.', 'Message': 'The request body submitted contained an empty JSON object and the service is unable to process it.', 'MessageSeverity': 'Warning', 'NumberOfArgs': 0, 'Resolution': 'Add properties in the JSON object and resubmit the request.', 'Severity': 'Warning'}, 'EventBufferExceeded': {'Description': 'Indicates undelivered events may have been lost due to a lack of buffer space in the service.', 'Message': 'Undelivered events may have been lost due to exceeding the event buffer.', 'MessageSeverity': 'Warning', 'NumberOfArgs': 0, 'Resolution': 'None.', 'Severity': 'Warning'}, 'EventSubscriptionLimitExceeded': {'Description': 'Indicates that a event subscription establishment has been requested but the operation failed due to the number of simultaneous connection exceeding the limit of the implementation.', 'Message': 'The event subscription failed due to the number of simultaneous subscriptions exceeding the limit of the implementation.', 'MessageSeverity': 'Critical', 'NumberOfArgs': 0, 'Resolution': 'Reduce the number of other subscriptions before trying to establish the event subscription or increase the limit of simultaneous subscriptions, if supported.', 'Severity': 'Critical'}, 'GeneralError': {'Description': 'Indicates that a general error has occurred.  Use in `@Message.ExtendedInfo` is discouraged.  When used in `@Message.ExtendedInfo`, implementations are expected to include a `Resolution` property with this message and provide a service-defined resolution to indicate how to resolve the error.', 'Message': 'A general error has occurred.  See Resolution for information on how to resolve the error, or @Message.ExtendedInfo if Resolution is not provided.', 'MessageSeverity': 'Critical', 'NumberOfArgs': 0, 'Resolution': 'None.', 'Severity': 'Critical'}, 'HeaderInvalid': {'Description': 'Indicates that a request header is invalid.', 'Message': "Header '%1' is invalid.", 'MessageSeverity': 'Critical', 'NumberOfArgs': 1, 'ParamTypes': ['string'], 'Resolution': 'Resubmit the request with a valid request header.', 'Severity': 'Critical'}, 'HeaderMissing': {'Description': 'Indicates that a required request header is missing.', 'Message': "Required header '%1' is missing in the request.", 'MessageSeverity': 'Critical', 'NumberOfArgs': 1, 'ParamTypes': ['string'], 'Resolution': 'Resubmit the request with the required request header.', 'Severity': 'Critical'}, 'InsufficientPrivilege': {'Description': 'Indicates that the credentials associated with the established session do not have sufficient privileges for the requested operation.', 'Message': 'There are insufficient privileges for the account or credentials associated with the current session to perform the requested operation.', 'MessageSeverity': 'Critical', 'NumberOfArgs': 0, 'Resolution': 'Either abandon the operation or change the associated access rights and resubmit the request if the operation failed.', 'Severity': 'Critical'}, 'InsufficientStorage': {'Description': 'Indicates that the operation could not be completed due to a lack of storage or memory avaiable to the service.', 'Message': 'Insufficent storage or memory available to complete the request.', 'MessageSeverity': 'Critical', 'NumberOfArgs': 0, 'Resolution': 'Increase the free storage space available to the service and resubmit the request.', 'Severity': 'Critical'}, 'InternalError': {'Description': 'Indicates that the request failed for an unknown internal error but that the service is still operational.', 'Message': 'The request failed due to an internal service error.  The service is still operational.', 'MessageSeverity': 'Critical', 'NumberOfArgs': 0, 'Resolution': 'Resubmit the request.  If the problem persists, consider resetting the service.', 'Severity': 'Critical'}, 'InvalidIndex': {'Description': 'The index is not valid.', 'Message': 'The index %1 is not a valid offset into the array.', 'MessageSeverity': 'Warning', 'NumberOfArgs': 1, 'ParamTypes': ['number'], 'Resolution': 'Verify the index value provided is within the bounds of the array.', 'Severity': 'Warning'}, 'InvalidJSON': {'Description': 'Indicates that the request body contains invalid JSON.', 'Message': 'The request body submitted is invalid JSON starting at line %1 and could not be parsed by the receiving service.', 'MessageSeverity': 'Critical', 'NumberOfArgs': 1, 'ParamTypes': ['number'], 'Resolution': 'Ensure that the request body is valid JSON and resubmit the request.', 'Severity': 'Critical'}, 'InvalidObject': {'Description': 'Indicates that the object in question is invalid according to the implementation.  Examples include a firmware update malformed URI.', 'Message': "The object at '%1' is invalid.", 'MessageSeverity': 'Critical', 'NumberOfArgs': 1, 'ParamTypes': ['string'], 'Resolution': 'Either the object is malformed or the URI is not correct.  Correct the condition and resubmit the request if it failed.', 'Severity': 'Critical'}, 'InvalidURI': {'Description': 'Indicates that the operation encountered a URI that does not correspond to a valid resource.', 'Message': 'The URI %1 was not found.', 'MessageSeverity': 'Critical', 'NumberOfArgs': 1, 'ParamTypes': ['string'], 'Resolution': 'Provide a valid URI and resubmit the request.', 'Severity': 'Critical'}, 'LicenseRequired': {'Description': 'Indicates that a license is required to perform the requested operation.', 'Message': 'A license is required for this operation: %1.', 'MessageSeverity': 'Critical', 'NumberOfArgs': 1, 'ParamTypes': ['string'], 'Resolution': 'Install the requested license and resubmit the request.', 'Severity': 'Critical'}, 'MalformedJSON': {'Description': 'Indicates that the request body was malformed JSON.', 'Message': 'The request body submitted was malformed JSON and could not be parsed by the receiving service.', 'MessageSeverity': 'Critical', 'NumberOfArgs': 0, 'Resolution': 'Ensure that the request body is valid JSON and resubmit the request.', 'Severity': 'Critical'}, 'MaximumErrorsExceeded': {'Description': 'Indicates that sufficient errors have occurred that the reporting service cannot return them all.', 'Message': 'Too many errors have occurred to report them all.', 'MessageSeverity': 'Critical', 'NumberOfArgs': 0, 'Resolution': 'Resolve other reported errors and retry the current operation.', 'Severity': 'Critical'}, 'MissingOrMalformedPart': {'Description': 'Indicates that a multipart request is missing a required part or contains malformed parts.', 'Message': 'The multipart request contains malformed parts or is missing required parts.', 'MessageSeverity': 'Critical', 'NumberOfArgs': 0, 'Resolution': 'Add any missing required parts or correct the malformed parts and resubmit the request.', 'Severity': 'Critical'}, 'NetworkNameResolutionNotConfigured': {'Description': 'Indicates that network-based name resolution has not been configured on the service.', 'Message': 'Network name resolution has not been configured on this service.', 'MessageSeverity': 'Warning', 'NumberOfArgs': 0, 'Resolution': 'Configure the network name resolution protocol support on this service, or update any URI values to include an IP address instead of a network name and resubmit the request.', 'Severity': 'Warning'}, 'NetworkNameResolutionNotSupported': {'Description': 'Indicates the service does not support network-based name resolution.', 'Message': 'Resolution of network-based names is not supported by this service.', 'MessageSeverity': 'Warning', 'NumberOfArgs': 0, 'Resolution': 'Update any URI values to include an IP address instead of a network name and resubmit the request.', 'Severity': 'Warning'}, 'NoOperation': {'Description': 'Indicates that the requested operation will not perform any changes on the service.', 'Message': 'The request body submitted contain no data to act upon and no changes to the resource took place.', 'MessageSeverity': 'Warning', 'NumberOfArgs': 0, 'Resolution': 'Add properties in the JSON object and resubmit the request.', 'Severity': 'Warning'}, 'NoValidSession': {'Description': 'Indicates that the operation failed because a valid session is required in order to access any resources.', 'Message': 'There is no valid session established with the implementation.', 'MessageSeverity': 'Critical', 'NumberOfArgs': 0, 'Resolution': 'Establish a session before attempting any operations.', 'Severity': 'Critical'}, 'OperationFailed': {'Description': 'Indicates that one of the internal operations necessary to complete the request failed.  Examples of this are when an internal service provider is unable to complete the request, such as in aggregation or RDE.', 'Message': 'An error occurred internal to the service as part of the overall request.  Partial results may have been returned.', 'MessageSeverity': 'Warning', 'NumberOfArgs': 0, 'Resolution': 'Resubmit the request.  If the problem persists, consider resetting the service or provider.', 'Severity': 'Warning'}, 'OperationNotAllowed': {'Description': 'Indicates that the HTTP method in the request is not allowed on this resource.', 'Message': 'The HTTP method is not allowed on this resource.', 'MessageSeverity': 'Critical', 'NumberOfArgs': 0, 'Resolution': 'None.', 'Severity': 'Critical'}, 'OperationTimeout': {'Description': 'Indicates that one of the internal operations necessary to complete the request timed out.  Examples of this are when an internal service provider is unable to complete the request, such as in aggregation or RDE.', 'Message': 'A timeout internal to the service occured as part of the request.  Partial results may have been returned.', 'MessageSeverity': 'Warning', 'NumberOfArgs': 0, 'Resolution': 'Resubmit the request.  If the problem persists, consider resetting the service or provider.', 'Severity': 'Warning'}, 'PasswordChangeRequired': {'Description': 'Indicates that the password for the account provided must be changed before accessing the service.  The password can be changed with a PATCH to the `Password` property in the manager account resource instance.  Implementations that provide a default password for an account may require a password change prior to first access to the service.', 'Message': "The password provided for this account must be changed before access is granted.  PATCH the Password property for this account located at the target URI '%1' to complete this process.", 'MessageSeverity': 'Critical', 'NumberOfArgs': 1, 'ParamTypes': ['string'], 'Resolution': 'Change the password for this account using a PATCH to the Password property at the URI provided.', 'Severity': 'Critical'}, 'PayloadTooLarge': {'Description': 'Indicates that the supplied payload is too large to be accepted by the service.', 'Message': 'The supplied payload exceeds the maximum size supported by the service.', 'MessageSeverity': 'Critical', 'NumberOfArgs': 0, 'Resolution': 'Check that the supplied payload is correct and supported by this service.', 'Severity': 'Critical'}, 'PreconditionFailed': {'Description': 'Indicates that the ETag supplied did not match the current ETag of the resource.', 'Message': 'The ETag supplied did not match the ETag required to change this resource.', 'MessageSeverity': 'Critical', 'NumberOfArgs': 0, 'Resolution': 'Try the operation again using the appropriate ETag.', 'Severity': 'Critical'}, 'PreconditionRequired': {'Description': 'Indicates that the request did not provide the required precondition such as an `If-Match` or `If-None-Match` header, or `@odata.etag` annotations.', 'Message': 'A precondition header or annotation is required to change this resource.', 'MessageSeverity': 'Critical', 'NumberOfArgs': 0, 'Resolution': 'Try the operation again using an If-Match or If-None-Match header and appropriate ETag.', 'Severity': 'Critical'}, 'PropertyDeprecated': {'Description': 'Indicates the property is deprecated.', 'Message': 'The deprecated property %1 was included in the request body.', 'MessageSeverity': 'Warning', 'NumberOfArgs': 1, 'ParamTypes': ['string'], 'Resolution': 'Refer to the schema guide for more information.', 'Severity': 'Warning'}, 'PropertyDuplicate': {'Description': 'Indicates that a duplicate property was included in the request body.', 'Message': 'The property %1 was duplicated in the request.', 'MessageSeverity': 'Warning', 'NumberOfArgs': 1, 'ParamTypes': ['string'], 'Resolution': 'Remove the duplicate property from the request body and resubmit the request if the operation failed.', 'Severity': 'Warning'}, 'PropertyMissing': {'Description': 'Indicates that a required property was not supplied as part of the request.', 'Message': 'The property %1 is a required property and must be included in the request.', 'MessageSeverity': 'Warning', 'NumberOfArgs': 1, 'ParamTypes': ['string'], 'Resolution': 'Ensure that the property is in the request body and has a valid value and resubmit the request if the operation failed.', 'Severity': 'Warning'}, 'PropertyNotUpdated': {'Description': 'Indicates that a property was not updated due to an internal service error, but the service is still functional.', 'Message': 'The property %1 was not updated due to an internal service error.  The service is still operational.', 'MessageSeverity': 'Critical', 'NumberOfArgs': 1, 'ParamTypes': ['string'], 'Resolution': 'Resubmit the request.  If the problem persists, check for additional messages and consider resetting the service.', 'Severity': 'Critical'}, 'PropertyNotWritable': {'Description': 'Indicates that a property was given a value in the request body, but the property is a readonly property.', 'Message': 'The property %1 is a read only property and cannot be assigned a value.', 'MessageSeverity': 'Warning', 'NumberOfArgs': 1, 'ParamTypes': ['string'], 'Resolution': 'Remove the property from the request body and resubmit the request if the operation failed.', 'Severity': 'Warning'}, 'PropertyUnknown': {'Description': 'Indicates that an unknown property was included in the request body.', 'Message': 'The property %1 is not in the list of valid properties for the resource.', 'MessageSeverity': 'Warning', 'NumberOfArgs': 1, 'ParamTypes': ['string'], 'Resolution': 'Remove the unknown property from the request body and resubmit the request if the operation failed.', 'Severity': 'Warning'}, 'PropertyValueConflict': {'Description': 'Indicates that the requested write of a property value could not be completed, because of a conflict with another property value.', 'Message': "The property '%1' could not be written because its value would conflict with the value of the '%2' property.", 'MessageSeverity': 'Warning', 'NumberOfArgs': 2, 'ParamTypes': ['string', 'string'], 'Resolution': 'No resolution is required.', 'Severity': 'Warning'}, 'PropertyValueDeprecated': {'Description': 'Indicates that a property was given a deprecated value.', 'Message': "The value '%1' for the property %2 is deprecated.", 'MessageSeverity': 'Warning', 'NumberOfArgs': 2, 'ParamTypes': ['string', 'string'], 'Resolution': 'Refer to the schema guide for more information.', 'Severity': 'Warning'}, 'PropertyValueError': {'Description': 'Indicates that a property was given an invalid value.', 'Message': 'The value provided for the property %1 is not valid.', 'MessageSeverity': 'Warning', 'NumberOfArgs': 1, 'ParamTypes': ['string'], 'Resolution': 'Correct the value for the property in the request body and resubmit the request if the operation failed.', 'Severity': 'Warning'}, 'PropertyValueExternalConflict': {'Description': 'Indicates that the requested write of a property value could not be completed, due to the current state or configuration of the resource.  This can include configuration conflicts with other resources or parameters that are not exposed by this interface.', 'Message': "The property '%1' with the requested value of '%2' could not be written because the value is not available due to a configuration conflict.", 'MessageSeverity': 'Warning', 'NumberOfArgs': 2, 'ParamTypes': ['string', 'string'], 'Resolution': 'No resolution is required.', 'Severity': 'Warning'}, 'PropertyValueFormatError': {'Description': 'Indicates that a property was given the correct value type but the value of that property was not supported.', 'Message': "The value '%1' for the property %2 is of a different format than the property can accept.", 'MessageSeverity': 'Warning', 'NumberOfArgs': 2, 'ParamTypes': ['string', 'string'], 'Resolution': 'Correct the value for the property in the request body and resubmit the request if the operation failed.', 'Severity': 'Warning'}, 'PropertyValueIncorrect': {'Description': 'Indicates that the requested write of a property value could not be completed, because of an incorrect value of the property.  Examples include values that do not match a regular expression requirement or passwords that do not match the implementation constraints.', 'Message': "The property '%1' with the requested value of '%2' could not be written because the value does not meet the constraints of the implementation.", 'MessageSeverity': 'Warning', 'NumberOfArgs': 2, 'ParamTypes': ['string', 'string'], 'Resolution': 'No resolution is required.', 'Severity': 'Warning'}, 'PropertyValueModified': {'Description': 'Indicates that a property was given the correct value type but the value of that property was modified.  Examples are truncated or rounded values.', 'Message': "The property %1 was assigned the value '%2' due to modification by the service.", 'MessageSeverity': 'Warning', 'NumberOfArgs': 2, 'ParamTypes': ['string', 'string'], 'Resolution': 'No resolution is required.', 'Severity': 'Warning'}, 'PropertyValueNotInList': {'Description': 'Indicates that a property was given the correct value type but the value of that property was not supported.  The value is not in an enumeration.', 'Message': "The value '%1' for the property %2 is not in the list of acceptable values.", 'MessageSeverity': 'Warning', 'NumberOfArgs': 2, 'ParamTypes': ['string', 'string'], 'Resolution': 'Choose a value from the enumeration list that the implementation can support and resubmit the request if the operation failed.', 'Severity': 'Warning'}, 'PropertyValueOutOfRange': {'Description': 'Indicates that a property was given the correct value type but the value of that property is outside the supported range.', 'Message': "The value '%1' for the property %2 is not in the supported range of acceptable values.", 'MessageSeverity': 'Warning', 'NumberOfArgs': 2, 'ParamTypes': ['string', 'string'], 'Resolution': 'Correct the value for the property in the request body and resubmit the request if the operation failed.', 'Severity': 'Warning'}, 'PropertyValueResourceConflict': {'Description': 'Indicates that the requested write of a property value could not be completed, due to the current state or configuration of another resource.', 'Message': "The property '%1' with the requested value of '%2' could not be written because the value conflicts with the state or configuration of the resource at '%3'.", 'MessageSeverity': 'Warning', 'NumberOfArgs': 3, 'ParamTypes': ['string', 'string', 'string'], 'Resolution': 'No resolution is required.', 'Severity': 'Warning'}, 'PropertyValueTypeError': {'Description': 'Indicates that a property was given the wrong value type, such as when a number is supplied for a property that requires a string.', 'Message': "The value '%1' for the property %2 is of a different type than the property can accept.", 'MessageSeverity': 'Warning', 'NumberOfArgs': 2, 'ParamTypes': ['string', 'string'], 'Resolution': 'Correct the value for the property in the request body and resubmit the request if the operation failed.', 'Severity': 'Warning'}, 'QueryCombinationInvalid': {'Description': 'Indicates the request contains multiple query parameters, and that two or more of them cannot be used together.', 'Message': 'Two or more query parameters in the request cannot be used together.', 'MessageSeverity': 'Warning', 'NumberOfArgs': 0, 'Resolution': 'Remove one or more of the query parameters and resubmit the request if the operation failed.', 'Severity': 'Warning'}, 'QueryNotSupported': {'Description': 'Indicates that query is not supported on the implementation.', 'Message': 'Querying is not supported by the implementation.', 'MessageSeverity': 'Warning', 'NumberOfArgs': 0, 'Resolution': 'Remove the query parameters and resubmit the request if the operation failed.', 'Severity': 'Warning'}, 'QueryNotSupportedOnOperation': {'Description': 'Indicates that query is not supported with the given operation, such as when the `$expand` query is attempted with a PATCH operation.', 'Message': 'Querying is not supported with the requested operation.', 'MessageSeverity': 'Warning', 'NumberOfArgs': 0, 'Resolution': 'Remove the query parameters and resubmit the request if the operation failed.', 'Severity': 'Warning'}, 'QueryNotSupportedOnResource': {'Description': 'Indicates that query is not supported on the given resource, such as when the `$skip` query is attempted on a resource that is not a collection.', 'Message': 'Querying is not supported on the requested resource.', 'MessageSeverity': 'Warning', 'NumberOfArgs': 0, 'Resolution': 'Remove the query parameters and resubmit the request if the operation failed.', 'Severity': 'Warning'}, 'QueryParameterOutOfRange': {'Description': 'Indicates that a query parameter was provided that is out of range for the given resource.  This can happen with values that are too low or beyond that possible for the supplied resource, such as when a page is requested that is beyond the last page.', 'Message': "The value '%1' for the query parameter %2 is out of range %3.", 'MessageSeverity': 'Warning', 'NumberOfArgs': 3, 'ParamTypes': ['string', 'string', 'string'], 'Resolution': 'Reduce the value for the query parameter to a value that is within range, such as a start or count value that is within bounds of the number of resources in a collection or a page that is within the range of valid pages.', 'Severity': 'Warning'}, 'QueryParameterUnsupported': {'Description': 'Indicates that a query parameter is not supported.', 'Message': "Query parameter '%1' is not supported.", 'MessageSeverity': 'Warning', 'NumberOfArgs': 1, 'ParamTypes': ['string'], 'Resolution': 'Correct or remove the query parameter and resubmit the request.', 'Severity': 'Warning'}, 'QueryParameterValueError': {'Description': 'Indicates that a query parameter was given an invalid value.', 'Message': 'The value for the parameter %1 is invalid.', 'MessageSeverity': 'Warning', 'NumberOfArgs': 1, 'ParamTypes': ['string'], 'Resolution': 'Correct the value for the query parameter in the request and resubmit the request if the operation failed.', 'Severity': 'Warning'}, 'QueryParameterValueFormatError': {'Description': 'Indicates that a query parameter was given the correct value type but the value of that parameter was not supported.  This includes the value size or length has been exceeded.', 'Message': "The value '%1' for the parameter %2 is of a different format than the parameter can accept.", 'MessageSeverity': 'Warning', 'NumberOfArgs': 2, 'ParamTypes': ['string', 'string'], 'Resolution': 'Correct the value for the query parameter in the request and resubmit the request if the operation failed.', 'Severity': 'Warning'}, 'QueryParameterValueTypeError': {'Description': 'Indicates that a query parameter was given the wrong value type, such as when a number is supplied for a query parameter that requires a string.', 'Message': "The value '%1' for the query parameter %2 is of a different type than the parameter can accept.", 'MessageSeverity': 'Warning', 'NumberOfArgs': 2, 'ParamTypes': ['string', 'string'], 'Resolution': 'Correct the value for the query parameter in the request and resubmit the request if the operation failed.', 'Severity': 'Warning'}, 'ResetRecommended': {'Description': 'Indicates that a component reset is recommended for error recovery while unaffected applications can continue running without any effects on accuracy and performance.', 'Message': "In order to recover from errors, a component reset is recommended with the Reset action URI '%1' and ResetType '%2'.", 'MessageSeverity': 'Warning', 'NumberOfArgs': 2, 'ParamTypes': ['string', 'string'], 'Resolution': 'Perform the recommended reset action on the specified component.', 'Severity': 'Warning'}, 'ResetRequired': {'Description': 'Indicates that a component reset is required for changes, error recovery, or operations to complete.', 'Message': "In order to apply changes, recover from errors, or complete the operation, a component reset is required with the Reset action URI '%1' and ResetType '%2'.", 'MessageSeverity': 'Warning', 'NumberOfArgs': 2, 'ParamTypes': ['string', 'string'], 'Resolution': 'Perform the required reset action on the specified component.', 'Severity': 'Warning'}, 'ResourceAlreadyExists': {'Description': 'Indicates that a resource change or creation was attempted but that the operation cannot proceed because the resource already exists.', 'Message': "The requested resource of type %1 with the property %2 with the value '%3' already exists.", 'MessageSeverity': 'Critical', 'NumberOfArgs': 3, 'ParamTypes': ['string', 'string', 'string'], 'Resolution': 'Do not repeat the create operation as the resource has already been created.', 'Severity': 'Critical'}, 'ResourceAtUriInUnknownFormat': {'Description': 'Indicates that the URI was valid but the resource or image at that URI was in a format not supported by the service.', 'Message': "The resource at '%1' is in a format not recognized by the service.", 'MessageSeverity': 'Critical', 'NumberOfArgs': 1, 'ParamTypes': ['string'], 'Resolution': 'Place an image or resource or file that is recognized by the service at the URI.', 'Severity': 'Critical'}, 'ResourceAtUriUnauthorized': {'Description': 'Indicates that the attempt to access the resource, file, or image at the URI was unauthorized.', 'Message': "While accessing the resource at '%1', the service received an authorization error '%2'.", 'MessageSeverity': 'Critical', 'NumberOfArgs': 2, 'ParamTypes': ['string', 'string'], 'Resolution': 'Ensure that the appropriate access is provided for the service in order for it to access the URI.', 'Severity': 'Critical'}, 'ResourceCannotBeDeleted': {'Description': 'Indicates that a delete operation was attempted on a resource that cannot be deleted.', 'Message': 'The delete request failed because the resource requested cannot be deleted.', 'MessageSeverity': 'Critical', 'NumberOfArgs': 0, 'Resolution': 'Do not attempt to delete a non-deletable resource.', 'Severity': 'Critical'}, 'ResourceCreationConflict': {'Description': 'Indicates that the requested resource creation could not be completed because the service has a resource that conflicts with the request.', 'Message': "The resource could not be created.  The service has a resource at URI '%1' that conflicts with the creation request.", 'MessageSeverity': 'Warning', 'NumberOfArgs': 1, 'ParamTypes': ['string'], 'Resolution': 'No resolution is required.', 'Severity': 'Warning'}, 'ResourceDeprecated': {'Description': 'Indicates the resource is deprecated.', 'Message': "The operation was performed on a deprecated resource '%1'.", 'MessageSeverity': 'Warning', 'NumberOfArgs': 1, 'ParamTypes': ['string'], 'Resolution': 'Refer to the schema guide for more information.', 'Severity': 'Warning'}, 'ResourceExhaustion': {'Description': 'Indicates that a resource could not satisfy the request due to some unavailability of resources.  An example is that available capacity has been allocated.', 'Message': "The resource '%1' was unable to satisfy the request due to unavailability of resources.", 'MessageSeverity': 'Critical', 'NumberOfArgs': 1, 'ParamTypes': ['string'], 'Resolution': 'Ensure that the resources are available and resubmit the request.', 'Severity': 'Critical'}, 'ResourceInStandby': {'Description': 'Indicates that the request could not be performed because the resource is in standby.', 'Message': 'The request could not be performed because the resource is in standby.', 'MessageSeverity': 'Critical', 'NumberOfArgs': 0, 'Resolution': 'Ensure that the resource is in the correct power state and resubmit the request.', 'Severity': 'Critical'}, 'ResourceInUse': {'Description': 'Indicates that a change was requested to a resource but the change was rejected due to the resource being in use or transition.', 'Message': 'The change to the requested resource failed because the resource is in use or in transition.', 'MessageSeverity': 'Warning', 'NumberOfArgs': 0, 'Resolution': 'Remove the condition and resubmit the request if the operation failed.', 'Severity': 'Warning'}, 'ResourceMissingAtURI': {'Description': 'Indicates that the operation expected an image or other resource at the provided URI but none was found.  Examples of this are in requests that require URIs like firmware update.', 'Message': "The resource at the URI '%1' was not found.", 'MessageSeverity': 'Critical', 'NumberOfArgs': 1, 'ParamTypes': ['string'], 'Resolution': 'Place a valid resource at the URI or correct the URI and resubmit the request.', 'Severity': 'Critical'}, 'ResourceNotFound': {'Description': 'Indicates that the operation expected a resource identifier that corresponds to an existing resource but one was not found.', 'Message': "The requested resource of type %1 named '%2' was not found.", 'MessageSeverity': 'Critical', 'NumberOfArgs': 2, 'ParamTypes': ['string', 'string'], 'Resolution': 'Provide a valid resource identifier and resubmit the request.', 'Severity': 'Critical'}, 'ResourceTypeIncompatible': {'Description': 'Indicates that the resource type of the operation does not match that for the operation destination.  Examples of when this can happen include during a POST to a resource collection using the wrong resource type, an update where the `@odata.type` properties do not match, or on a major version incompatibility.', 'Message': 'The @odata.type of the request body %1 is incompatible with the @odata.type of the resource, which is %2.', 'MessageSeverity': 'Critical', 'NumberOfArgs': 2, 'ParamTypes': ['string', 'string'], 'Resolution': "Resubmit the request with a payload compatible with the resource's schema.", 'Severity': 'Critical'}, 'RestrictedPrivilege': {'Description': 'Indicates that the operation was not successful because a privilege is restricted.', 'Message': "The operation was not successful because the privilege '%1' is restricted.", 'MessageSeverity': 'Warning', 'NumberOfArgs': 1, 'ParamTypes': ['string'], 'Resolution': 'Remove restricted privileges from the request body and resubmit the request.', 'Severity': 'Warning'}, 'RestrictedRole': {'Description': 'Indicates that the operation was not successful because the role is restricted.', 'Message': "The operation was not successful because the role '%1' is restricted.", 'MessageSeverity': 'Warning', 'NumberOfArgs': 1, 'ParamTypes': ['string'], 'Resolution': 'No resolution is required.  For standard roles, consider using the role specified in the AlternateRoleId property in the Role resource.', 'Severity': 'Warning'}, 'ServiceDisabled': {'Description': 'Indicates that the operation failed because the service, such as the account service, is disabled and cannot accept requests.', 'Message': 'The operation failed because the service at %1 is disabled and cannot accept requests.', 'MessageSeverity': 'Warning', 'NumberOfArgs': 1, 'ParamTypes': ['string'], 'Resolution': 'Enable the service and resubmit the request if the operation failed.', 'Severity': 'Warning'}, 'ServiceInUnknownState': {'Description': 'Indicates that the operation failed because the service is in an unknown state and cannot accept additional requests.', 'Message': 'The operation failed because the service is in an unknown state and can no longer take incoming requests.', 'MessageSeverity': 'Critical', 'NumberOfArgs': 0, 'Resolution': 'Restart the service and resubmit the request if the operation failed.', 'Severity': 'Critical'}, 'ServiceShuttingDown': {'Description': 'Indicates that the operation failed as the service is shutting down, such as when the service reboots.', 'Message': 'The operation failed because the service is shutting down and can no longer take incoming requests.', 'MessageSeverity': 'Critical', 'NumberOfArgs': 0, 'Resolution': 'When the service becomes available, resubmit the request if the operation failed.', 'Severity': 'Critical'}, 'ServiceTemporarilyUnavailable': {'Description': 'Indicates the service is temporarily unavailable.', 'Message': 'The service is temporarily unavailable.  Retry in %1 seconds.', 'MessageSeverity': 'Critical', 'NumberOfArgs': 1, 'ParamTypes': ['string'], 'Resolution': 'Wait for the indicated retry duration and retry the operation.', 'Severity': 'Critical'}, 'SessionLimitExceeded': {'Description': 'Indicates that a session establishment has been requested but the operation failed due to the number of simultaneous sessions exceeding the limit of the implementation.', 'Message': 'The session establishment failed due to the number of simultaneous sessions exceeding the limit of the implementation.', 'MessageSeverity': 'Critical', 'NumberOfArgs': 0, 'Resolution': 'Reduce the number of other sessions before trying to establish the session or increase the limit of simultaneous sessions, if supported.', 'Severity': 'Critical'}, 'SessionTerminated': {'Description': 'Indicates that the DELETE operation on the session resource resulted in the successful termination of the session.', 'Message': 'The session was successfully terminated.', 'MessageSeverity': 'OK', 'NumberOfArgs': 0, 'Resolution': 'No resolution is required.', 'Severity': 'OK'}, 'SourceDoesNotSupportProtocol': {'Description': 'Indicates that while attempting to access, connect to or transfer a resource, file, or image from another location that the other end of the connection did not support the protocol.', 'Message': "The other end of the connection at '%1' does not support the specified protocol %2.", 'MessageSeverity': 'Critical', 'NumberOfArgs': 2, 'ParamTypes': ['string', 'string'], 'Resolution': 'Change protocols or URIs.', 'Severity': 'Critical'}, 'StrictAccountTypes': {'Description': 'Indicates the request failed because a set of `AccountTypes` or `OEMAccountTypes` was not accepted while `StrictAccountTypes` is set to `true`.', 'Message': "The request was not possible to fulfill with the account types included in property '%1' and property StrictAccountTypes set to true.", 'MessageSeverity': 'Warning', 'NumberOfArgs': 1, 'ParamTypes': ['string'], 'Resolution': 'Resubmit the request either with an acceptable set of AccountTypes and OEMAccountTypes or with StrictAccountTypes set to false.', 'Severity': 'Warning'}, 'StringValueTooLong': {'Description': 'Indicates that a string value passed to the given resource exceeded its length limit.  An example is when a shorter limit is imposed by an implementation than that allowed by the specification.', 'Message': "The string '%1' exceeds the length limit %2.", 'MessageSeverity': 'Warning', 'NumberOfArgs': 2, 'ParamTypes': ['string', 'number'], 'Resolution': 'Resubmit the request with an appropriate string length.', 'Severity': 'Warning'}, 'StringValueTooShort': {'Description': 'Indicates that a string value passed to the given resource was under its minimum required length.  An example is when a higher minimum length is imposed by an implementation than that allowed by the specification.', 'Message': "The string '%1' was under the minimum required length %2.", 'MessageSeverity': 'Warning', 'NumberOfArgs': 2, 'ParamTypes': ['string', 'number'], 'Resolution': 'Resubmit the request with an appropriate string length.', 'Severity': 'Warning'}, 'SubscriptionTerminated': {'Description': 'An event subscription has been terminated by the service.  No further events will be delivered.', 'Message': 'The event subscription has been terminated.', 'MessageSeverity': 'OK', 'NumberOfArgs': 0, 'Resolution': 'No resolution is required.', 'Severity': 'OK'}, 'Success': {'Description': 'Indicates that all conditions of a successful operation have been met.', 'Message': 'The request completed successfully.', 'MessageSeverity': 'OK', 'NumberOfArgs': 0, 'Resolution': 'None', 'Severity': 'OK'}, 'UndeterminedFault': {'Description': 'Indicates that a fault or error condition exists but the source of the fault cannot be determined or is unknown to the service.', 'Message': "A undetermined fault condition has been reported by '%1'.", 'MessageSeverity': 'Critical', 'NumberOfArgs': 1, 'ParamTypes': ['string'], 'Resolution': 'None.', 'Severity': 'Critical'}, 'UnrecognizedRequestBody': {'Description': 'Indicates that the service encountered an unrecognizable request body that could not even be interpreted as malformed JSON.', 'Message': 'The service detected a malformed request body that it was unable to interpret.', 'MessageSeverity': 'Warning', 'NumberOfArgs': 0, 'Resolution': 'Correct the request body and resubmit the request if it failed.', 'Severity': 'Warning'}}"""
####CONSR-OBMC-RDFT-0023-0001
LogServiceCollection1 = "/redfish/v1/Systems/system/LogServices"
data_type_LogServiceCollection1 = "#LogServiceCollection.LogServiceCollection"
Members_odata_count_LogServiceCollection1 = "3"
Description_LogServiceCollection1 = "Collection of LogServices for this Computer System"
Name_LogServiceCollection1 = "System Log Services Collection"
####CONSR-OBMC-RDFT-0025-0001
resource_logservice1 = "/redfish/v1/Systems/system/LogServices/EventLog"
data_type_logservice1 = "#LogService.v1_1_0.LogService"
Actions_logservice1 = """{'#LogService.ClearLog': {'target': '/redfish/v1/Systems/system/LogServices/EventLog/Actions/LogService.ClearLog'}}"""
Description_logservice1 = "System Event Log Service"
Entries_logservice1 = """{'@odata.id': '/redfish/v1/Systems/system/LogServices/EventLog/Entries'}"""
Id_logservice1 = "EventLog"
Name_logservice1 = "Event Log Service"
OverWritePolicy_logservice1 = "WrapsWhenFull"
####CONSR-OBMC-RDFT-0027-0001
resource_logservice3 = "/redfish/v1/Systems/system/LogServices/HostLogger"
data_type_logservice3 = "#LogService.v1_1_0.LogService"
Description_logservice3 = "Host Logger Service"
Entries_logservice3 = """{'@odata.id': '/redfish/v1/Systems/system/LogServices/HostLogger/Entries'}"""
Id_logservice3 = "HostLogger"
Name_logservice3 = "Host Logger Service"
####CONSR-OBMC-RDFT-0012-0001
resource_Manager_Collection = "/redfish/v1/Managers"
data_type_Manager_Collection = "#ManagerCollection.ManagerCollection"
Members_odata_count_Manager_Collection = "1"
Name_Manager_Collection_1 = "Manager Collection"
####CONSR-OBMC-RDFT-0014-0001
resource_Manager_2 = "/redfish/v1/Managers/bmc/ManagerDiagnosticData"
odata_type_Manager_2 = "#ManagerDiagnosticData.v1_2_0.ManagerDiagnosticData"
Id_Manager_2 = "ManagerDiagnosticData"
Name_Manager_2 = "Manager Diagnostic Data"
####CONSR-OBMC-RDFT-0021-0001
resource_Networkprotocol1 = "/redfish/v1/Managers/bmc/NetworkProtocol/HTTPS/Certificates"
data_type_Networkprotocol1 = "#CertificateCollection.CertificateCollection"
Members_odata_count_Networkprotocol1 = "1"
Description_Networkprotocol1 = "A Collection of HTTPS certificate instances"
Name_Networkprotocol1 = "HTTPS Certificates Collection"
####CONSR-OBMC-RDFT-0002-0001
resource_cables_Collection = "/redfish/v1/Cables"
data_type_cables_Collection = "#CableCollection.CableCollection"
Description_cables_Collection = "Collection of Cable Entries"
Members_odata_count_cables_Collection = "0"
Name_cables_Collection = "Cable Collection"
####CONSR-OBMC-RDFT-0004-0001
resource_Computer_System_Collection_2 = "/redfish/v1/Systems/system"
data_type_Computer_System_Collection_2 = "#ComputerSystem.v1_16_0.ComputerSystem"
Actions_Computer_System_Collection_2 = """{'#ComputerSystem.Reset': {'@Redfish.ActionInfo': '/redfish/v1/Systems/system/ResetActionInfo', 'target': '/redfish/v1/Systems/system/Actions/ComputerSystem.Reset'}}"""
Bios_Computer_System_Collection_2 = """{'@odata.id': '/redfish/v1/Systems/system/Bios'}"""
Boot_Computer_System_Collection_2 = """{'AutomaticRetryConfig': 'RetryAttempts', 'AutomaticRetryConfig@Redfish.AllowableValues': ['Disabled', 'RetryAttempts'], 'BootSourceOverrideEnabled': 'Disabled', 'BootSourceOverrideMode': 'UEFI', 'BootSourceOverrideMode@Redfish.AllowableValues': ['Legacy', 'UEFI'], 'BootSourceOverrideTarget': 'None', 'BootSourceOverrideTarget@Redfish.AllowableValues': ['None', 'Pxe', 'Hdd', 'Cd', 'Diags', 'BiosSetup', 'Usb'], 'StopBootOnFault': 'Never', 'TrustedModuleRequiredToBoot': 'Disabled'}"""
Description_Computer_System_Collection_2 = "Computer System"
FabricAdapters_Computer_System_Collection_2 = """{'@odata.id': '/redfish/v1/Systems/system/FabricAdapters'}"""
GraphicalConsole_Computer_System_Collection_2 = """{'ConnectTypesSupported': ['KVMIP'], 'MaxConcurrentSessions': 4, 'ServiceEnabled': True}"""
HostWatchdogTimer_Computer_System_Collection_2 = """{'FunctionEnabled': False, 'Status': {'State': 'Enabled'}, 'TimeoutAction': 'None'}"""
Id_Computer_System_Collection_2 = "system"
Links_Computer_System_Collection_2 = """{'Chassis': [{'@odata.id': '/redfish/v1/Chassis/artemis_motherboard'}], 'ManagedBy': [{'@odata.id': '/redfish/v1/Managers/bmc'}]}"""
LogServices_Computer_System_Collection_2 = """{'@odata.id': '/redfish/v1/Systems/system/LogServices'}"""
Memory_Computer_System_Collection_2 = """{'@odata.id': '/redfish/v1/Systems/system/Memory'}"""
MemorySummary_Computer_System_Collection_2 = """{'TotalSystemMemoryGiB': 0.0}"""
Name_Computer_System_Collection_2 = "system"
PCIeDevices_Computer_System_Collection_2 = "[]"
PCIeDevices_odata_count_Computer_System_Collection_2 = "0"
PowerRestorePolicy_Computer_System_Collection_2 = "AlwaysOn"
PowerState_Computer_System_Collection_2 = "On"
ProcessorSummary_Computer_System_Collection_2 = """{'Count': 0}"""
Processors_Computer_System_Collection_2 = """{'@odata.id': '/redfish/v1/Systems/system/Processors'}"""
SerialConsole_Computer_System_Collection_2 = """{'IPMI': {'ServiceEnabled': True}, 'MaxConcurrentSessions': 15, 'SSH': {'HotKeySequenceDisplay': 'Press ~. to exit console', 'Port': 2200, 'ServiceEnabled': True}}"""
Status_Computer_System_Collection_2 = """{'Health': 'OK', 'HealthRollup': 'OK', 'State': 'Enabled'}"""
Storage_Computer_System_Collection_2 = """{'@odata.id': '/redfish/v1/Systems/system/Storage'}"""
SystemType_Computer_System_Collection_2 = "Physical"
####CONSR-OBMC-RDFT-0016-0001
resource_Manager_4 = "/redfish/v1/Managers/bmc/EthernetInterfaces/eth0"
data_type_Manager_4 = "#EthernetInterface.v1_9_0.EthernetInterface"
DHCPv4_Manager_4 = """{'DHCPEnabled': True, 'UseDNSServers': True, 'UseDomainName': True, 'UseNTPServers': True}"""
DHCPv6_Manager_4 = """{'OperatingMode': 'Stateful', 'UseDNSServers': True, 'UseDomainName': True, 'UseNTPServers': True}"""
Description_Manager_4 = "Management Network Interface"
EthernetInterfaceType_Manager_4 = "Physical"
FQDN_Manager_4 = "artemis"
HostName_Manager_4 = "artemis"
Id_Manager_4 = "eth0"
InterfaceEnabled_Manager_4 = "True"
LinkStatus_Manager_4 = "LinkUp"
MTUSize_Manager_4 = "1500"
Name_Manager_4 = "Manager Ethernet Interface"
Status_Manager_4 = """{'State': 'Enabled'}"""
####CONSR-OBMC-RDFT-0018-0001
resource_Manager_6 = "/redfish/v1/Managers/bmc/EthernetInterfaces/usb0"
data_type_Manager_6 = "#EthernetInterface.v1_9_0.EthernetInterface"
DHCPv4_Manager_6 = """{'DHCPEnabled': True, 'UseDNSServers': True, 'UseDomainName': True, 'UseNTPServers': True}"""
DHCPv6_Manager_6 = """{'OperatingMode': 'Stateful', 'UseDNSServers': True, 'UseDomainName': True, 'UseNTPServers': True}"""
Description_Manager_6 = "Management Network Interface"
EthernetInterfaceType_Manager_6 = "Physical"
FQDN_Manager_6 = "artemis"
HostName_Manager_6 = "artemis"
Id_Manager_6 = "usb0"
InterfaceEnabled_Manager_6 = "False"
LinkStatus_Manager_6 = "NoLink"
MTUSize_Manager_6 = "1500"
Name_Manager_6 = "Manager Ethernet Interface"
Status_Manager_6 = """{'State': 'Disabled'}"""
###CONSR-OBMC-RDFT-0030-0001
resource_logservice6 = "/redfish/v1/Systems/system/LogServices/PostCodes/Entries"
data_type_logservice6 = "#LogEntryCollection.LogEntryCollection"
Description_logservice6 = "Collection of POST Code Log Entries"
Name_logservice6 = "BIOS POST Code Log Entries"
###CONSR-OBMC-RDFT-0032-0001
resource_logservice8 = "/redfish/v1/Managers/bmc/LogServices/Journal/Entries"
data_type_logservice8 = "#LogEntryCollection.LogEntryCollection"
Description_logservice8 = "Collection of BMC Journal Entries"
Name_logservice8 = "Open BMC Journal Entries"
Members_odata_nextLink_logservice8 = "/redfish/v1/Managers/bmc/LogServices/Journal/Entries?$skip=1000"
#####CONSR-OBMC-RDFT-0009-0001
resource_computersystem5 = "/redfish/v1/Systems/system/ResetActionInfo"
data_type_computersystem5 = "#ActionInfo.v1_1_2.ActionInfo"
Id_computersystem5 = "ResetActionInfo"
Name_computersystem5 = "Reset Action Info"
Parameters_computersystem5 = """[{'AllowableValues': ['On', 'ForceOff', 'ForceOn', 'ForceRestart', 'GracefulRestart', 'GracefulShutdown', 'PowerCycle', 'Nmi'], 'DataType': 'String', 'Name': 'ResetType', 'Required': True}]"""
######CONSR-OBMC-RDFT-0034-0001
resource_telemetryservice = "/redfish/v1/TelemetryService"
data_type_telemetryservice = "#TelemetryService.v1_2_1.TelemetryService"
Id_telemetryservice = "TelemetryService"
MaxReports_telemetryservice = "10"
MetricReportDefinitions_telemetryservice = """{'@odata.id': '/redfish/v1/TelemetryService/MetricReportDefinitions'}"""
MetricReports_telemetryservice = """{'@odata.id': '/redfish/v1/TelemetryService/MetricReports'}"""
MinCollectionInterval_telemetryservice = "PT1.000S"
Name_telemetryservice1 = "Telemetry Service"
Status_telemetryservice = """{'State': 'Enabled'}"""
SupportedCollectionFunctions_telemetryservice = """['Maximum', 'Minimum', 'Average', 'Summation']"""
Triggers_telemetryservice = """{'@odata.id': '/redfish/v1/TelemetryService/Triggers'}"""
######CONSR-OBMC-RDFT-0039-0001
resource_chassis1 = "/redfish/v1/Chassis/artemis_motherboard"
data_type_chassis1 = "#Chassis.v1_22_0.Chassis"
Actions_chassis1 = """{'#Chassis.Reset': {'@Redfish.ActionInfo': '/redfish/v1/Chassis/artemis_motherboard/ResetActionInfo', 'target': '/redfish/v1/Chassis/artemis_motherboard/Actions/Chassis.Reset'}}"""
ChassisType_chassis1 = "RackMount"
Id_chassis1 = "artemis_motherboard"
Links_chassis1 = """{'ComputerSystems': [{'@odata.id': '/redfish/v1/Systems/system'}], 'ManagedBy': [{'@odata.id': '/redfish/v1/Managers/bmc'}]}"""
Manufacturer_chassis1 = "$PRODUCT_MANUFACTURER"
Name_chassis1 = "artemis_motherboard"
Model_chassis1 = "$PRODUCT_PRODUCT_NAME"
PCIeDevices_chassis1 = """{'@odata.id': '/redfish/v1/Systems/system/PCIeDevices'}"""
PartNumber_chassis1 = "$PRODUCT_PART_NUMBER"
Power_chassis1 = """{'@odata.id': '/redfish/v1/Chassis/artemis_motherboard/Power'}"""
PowerState_chassis1 = "On"
Sensors_chassis1 = """{'@odata.id': '/redfish/v1/Chassis/artemis_motherboard/Sensors'}"""
SerialNumber_chassis1 = "$PRODUCT_SERIAL_NUMBER"
Status_chassis1 = """{'Health': 'OK', 'HealthRollup': 'OK', 'State': 'Enabled'}"""
Thermal_chassis1 = """{'@odata.id': '/redfish/v1/Chassis/artemis_motherboard/Thermal'}"""
#####CONSR-OBMC-RDFT-0042-0001
resource_sensors = "/redfish/v1/Chassis/artemis_motherboard/Sensors"
data_type_sensors = "#SensorCollection.SensorCollection"
Description_sensors = "Collection of Sensors for this Chassis"
Members_sensors = """[{'@odata.id': '/redfish/v1/Chassis/artemis_motherboard/Sensors/current_BBU_Average_Current'}, {'@odata.id': '/redfish/v1/Chassis/artemis_motherboard/Sensors/current_BBU_Charging_Current'}, {'@odata.id': '/redfish/v1/Chassis/artemis_motherboard/Sensors/current_BBU_Current'}, {'@odata.id': '/redfish/v1/Chassis/artemis_motherboard/Sensors/current_BBU_Remain_Capacity'}, {'@odata.id': '/redfish/v1/Chassis/artemis_motherboard/Sensors/current_PSU_A_CurrIn'}, {'@odata.id': '/redfish/v1/Chassis/artemis_motherboard/Sensors/current_PSU_A_CurrOut'}, {'@odata.id': '/redfish/v1/Chassis/artemis_motherboard/Sensors/current_PSU_B_CurrIn'}, {'@odata.id': '/redfish/v1/Chassis/artemis_motherboard/Sensors/current_PSU_B_CurrOut'}, {'@odata.id': '/redfish/v1/Chassis/artemis_motherboard/Sensors/power_PSU_A_PowerIn'}, {'@odata.id': '/redfish/v1/Chassis/artemis_motherboard/Sensors/power_PSU_A_PowerOut'}, {'@odata.id': '/redfish/v1/Chassis/artemis_motherboard/Sensors/power_PSU_B_PowerIn'}, {'@odata.id': '/redfish/v1/Chassis/artemis_motherboard/Sensors/power_PSU_B_PowerOut'}, {'@odata.id': '/redfish/v1/Chassis/artemis_motherboard/Sensors/power_total_power'}]"""
Members_odata_count_sensors = "13"
Name_sensors = "Sensors"
#####CONSR-OBMC-RDFT-0044-0001
resource_sensors_2 = "/redfish/v1/Chassis/artemis_motherboard/Sensors/current_BBU_Charging_Current"
data_type_sensors_2 = "#Sensor.v1_2_0.Sensor"
Id_sensors_2 = "current_BBU_Charging_Current"
Name_sensors_2 = "BBU Charging Current"
ReadingRangeMax_sensors_2 = "150.0"
ReadingRangeMin_sensors_2 = "-10.0"
ReadingType_sensors_2 = "Current"
ReadingUnits_sensors_2 = "A"
Status_sensors_2 = """{'Health': 'OK', 'State': 'Enabled'}"""
#####CONSR-OBMC-RDFT-0046-0001
resource_sensors_4 = "/redfish/v1/Chassis/artemis_motherboard/Sensors/current_BBU_Remain_Capacity"
data_type_sensors_4 = "#Sensor.v1_2_0.Sensor"
Id_sensors_4 = "current_BBU_Remain_Capacity"
Name_sensors_4 = "BBU Remain Capacity"
ReadingRangeMax_sensors_4 = "100.0"
ReadingRangeMin_sensors_4 = "0.0"
ReadingType_sensors_4 = "Current"
ReadingUnits_sensors_4 = "A"
Status_sensors_4 = """{'Health': 'OK', 'State': 'Enabled'}"""
####CONSR-OBMC-RDFT-0048-0001
resource_sensors_6 = "/redfish/v1/Chassis/artemis_motherboard/Sensors/current_PSU_A_CurrOut"
data_type_sensors_6 = "#Sensor.v1_2_0.Sensor"
Id_sensors_6 = "current_PSU_A_CurrOut"
Name_sensors_6 = "PSU A CurrOut"
ReadingRangeMax_sensors_6 = "255.0"
ReadingRangeMin_sensors_6 = "0.0"
ReadingType_sensors_6 = "Current"
ReadingUnits_sensors_6 = "A"
Status_sensors_6 = """{'Health': 'OK', 'State': 'Enabled'}"""
Thresholds_sensors_6 = """{'UpperCaution': {'Reading': 200.0}}"""
#####CONSR-OBMC-RDFT-0050-0001
resource_sensors_8 = "/redfish/v1/Chassis/artemis_motherboard/Sensors/current_PSU_B_CurrOut"
data_type_sensors_8 = "#Sensor.v1_2_0.Sensor"
Id_sensors_8 = "current_PSU_B_CurrOut"
Name_sensors_8 = "PSU B CurrOut"
ReadingRangeMax_sensors_8 = "255.0"
ReadingRangeMin_sensors_8 = "0.0"
ReadingType_sensors_8 = "Current"
ReadingUnits_sensors_8 = "A"
Status_sensors_8 = """{'Health': 'OK', 'State': 'Enabled'}"""
Thresholds_sensors_8 = """{'UpperCaution': {'Reading': 200.0}}"""
#####CONSR-OBMC-RDFT-0052-0001
resource_sensors_10 = "/redfish/v1/Chassis/artemis_motherboard/Sensors/power_PSU_A_PowerOut"
data_type_sensors_10 = "#Sensor.v1_2_0.Sensor"
Id_sensors_10 = "power_PSU_A_PowerOut"
Name_sensors_10 = "PSU A PowerOut"
ReadingRangeMax_sensors_10 = "3000.0"
ReadingRangeMin_sensors_10 = "0.0"
ReadingType_sensors_10 = "Power"
ReadingUnits_sensors_10 = "W"
Status_sensors_10 = """{'Health': 'OK', 'State': 'Enabled'}"""
Thresholds_sensors_10 = """{'UpperCaution': {'Reading': 2312.0}}"""
#####CONSR-OBMC-RDFT-0054-0001
resource_sensors_12 = "/redfish/v1/Chassis/artemis_motherboard/Sensors/power_PSU_B_PowerOut"
data_type_sensors_12 = "#Sensor.v1_2_0.Sensor"
Id_sensors_12 = "power_PSU_B_PowerOut"
Name_sensors_12 = "PSU B PowerOut"
ReadingRangeMax_sensors_12 = "3000.0"
ReadingRangeMin_sensors_12 = "0.0"
ReadingType_sensors_12 = "Power"
ReadingUnits_sensors_12 = "W"
Status_sensors_12 = """{'Health': 'OK', 'State': 'Enabled'}"""
Thresholds_sensors_12 = """{'UpperCaution': {'Reading': 2312.0}}"""
####CONSR-OBMC-RDFT-0150-0001
resource_ManagerAccount_Collection = "/redfish/v1/AccountService/Accounts"
data_type_ManagerAccount_Collection = "#ManagerAccountCollection.ManagerAccountCollection"
Members_odata_count_ManagerAccount_Collection = "1"
Description_ManagerAccount_Collection_1 = "BMC User Accounts"
Name_ManagerAccount_Collection_1 = "Accounts Collection"
Members_ManagerAccount_Collection = """[{'@odata.id': '/redfish/v1/AccountService/Accounts/root'}]"""
####CONSR-OBMC-RDFT-0003-0001
resource_Computer_Collection_1 = "/redfish/v1/Systems"
data_type_Computer_Collection_1 = "#ComputerSystemCollection.ComputerSystemCollection"
Members_Computer_Collection_1 = """[{'@odata.id': '/redfish/v1/Systems/system'}]"""
Members_odata_count_Computer_Collection_1 = "1"
Name_Computer_Collection_1 = "Computer System Collection"
####CONSR-OBMC-RDFT-0006-0001
resource_computer_system2 = "/redfish/v1/Systems/system/Bios"
data_type_computer_system2 = "#Bios.v1_1_0.Bios"
actions_computer_systems2 = """{'#Bios.ResetBios': {'target': '/redfish/v1/Systems/system/Bios/Actions/Bios.ResetBios'}}"""
Description_computer_system2 = "BIOS Configuration Service"
ID_computer_system2 = "BIOS"
Links_computer_system2 = """{'ActiveSoftwareImage': {'@odata.id': '/redfish/v1/UpdateService/FirmwareInventory/bios_active'}, 'SoftwareImages': [{'@odata.id': '/redfish/v1/UpdateService/FirmwareInventory/bios_active'}], 'SoftwareImages@odata.count': 1}"""
Name_computer_system2 = "BIOS Configuration"
####CONSR-OBMC-RDFT-0015-0001
resource_manager_3 = "/redfish/v1/Managers/bmc/EthernetInterfaces"
data_type_manager_3 = "#EthernetInterfaceCollection.EthernetInterfaceCollection"
Description_manager_3 = "Collection of EthernetInterfaces for this Manager"
Member_manager_3 = """[{'@odata.id': '/redfish/v1/Managers/bmc/EthernetInterfaces/eth0'}, {'@odata.id': '/redfish/v1/Managers/bmc/EthernetInterfaces/eth1'}, {'@odata.id': '/redfish/v1/Managers/bmc/EthernetInterfaces/usb0'}]"""
Members_odata_count_manager_3 = "3"
Name_manager_3 = "Ethernet Network Interface Collection"
####CONSR-OBMC-RDFT-0271-0001
resource_session_collection_1 = "/redfish/v1/SessionService/"
data_type_session_collection_1 = "#SessionService.v1_0_2.SessionService"
Description_session_collection_1 = "Session Service"
ID_session_collection_1 = "SessionService"
name_session_collection_1 = "Session Service"
serviceenabled_session_collection_1 = "True"
sessiontimeout_session_collection_1 = "1800"
sessions_session_collection_1 = """{'@odata.id': '/redfish/v1/SessionService/Sessions'}"""
####CONSR-OBMC-RDFT-0275-0001
resource_message_registry_1 = "/redfish/v1/Registries/Base"
data_type_message_registry_1 = "#MessageRegistryFile.v1_1_0.MessageRegistryFile"
Description_message_registry_1 = "DMTF Base Message Registry File Location"
ID_message_registry_1 = "Base"
Languages_message_registry_1 = "['en']"
Languages_odata_count_message_registry_1 = "1"
Location_message_registry_1 = """[{'Language': 'en', 'PublicationUri': 'https://redfish.dmtf.org/registries/Base.1.16.0.json', 'Uri': '/redfish/v1/Registries/Base/Base'}]"""
Location_odata_count_message_registry_1 = "1"
Name_message_registry_1 = "Base Message Registry File"
Registry_message_registry_1 = "Base.1.16.0"
####CONSR-OBMC-RDFT-0277-0001
resource_message_registry_3 = "/redfish/v1/Registries/TaskEvent"
data_type_message_registry_3 = "#MessageRegistryFile.v1_1_0.MessageRegistryFile"
Description_message_registry_3 = "DMTF TaskEvent Message Registry File Location"
ID_message_registry_3 = "TaskEvent"
Languages_message_registry_3 = "['en']"
Languages_odata_count_message_registry_3 = "1"
Location_message_registry_3 = """[{'Language': 'en', 'PublicationUri': 'https://redfish.dmtf.org/registries/TaskEvent.1.0.3.json', 'Uri': '/redfish/v1/Registries/TaskEvent/TaskEvent'}]"""
Location_odata_count_message_registry_3 = "1"
Name_message_registry_3 = "TaskEvent Message Registry File"
Registry_message_registry_3 = "TaskEvent.1.0.3"
####CONSR-OBMC-RDFT-0279-0001
resource_message_registry_5 = "/redfish/v1/Registries/ResourceEvent"
data_type_message_registry_5 = "#MessageRegistryFile.v1_1_0.MessageRegistryFile"
Description_message_registry_5 = "DMTF ResourceEvent Message Registry File Location"
ID_message_registry_5 = "ResourceEvent"
Languages_message_registry_5 = "['en']"
Languages_odata_count_message_registry_5 = "1"
Location_message_registry_5 = """[{'Language': 'en', 'PublicationUri': 'https://redfish.dmtf.org/registries/ResourceEvent.1.3.0.json', 'Uri': '/redfish/v1/Registries/ResourceEvent/ResourceEvent'}]"""
Location_odata_count_message_registry_5 = "1"
Name_message_registry_5 = "ResourceEvent Message Registry File"
Registry_message_registry_5 = "ResourceEvent.1.3.0"
####CONSR-OBMC-RDFT-0281-0001
resource_message_registry_7 = "/redfish/v1/Registries/OpenBMC"
data_type_message_registry_7 = "#MessageRegistryFile.v1_1_0.MessageRegistryFile"
Description_message_registry_7 = "OpenBMC Message Registry File Location"
ID_message_registry_7 = "OpenBMC"
Languages_message_registry_7 = "['en']"
Languages_odata_count_message_registry_7 = "1"
Location_message_registry_7 = """[{'Language': 'en', 'Uri': '/redfish/v1/Registries/OpenBMC/OpenBMC'}]"""
Location_odata_count_message_registry_7 = "1"
Name_message_registry_7 = "OpenBMC Message Registry File"
Registry_message_registry_7 = "OpenBMC.0.4.0"
####CONSR-OBMC-RDFT-0151-0001
resource_ManagerAccount = "/redfish/v1/AccountService/Accounts/root"
data_type_ManagerAccount = "#ManagerAccount.v1_7_0.ManagerAccount"
AccountTypes_ManagerAccount = """['HostConsole', 'IPMI', 'Redfish', 'WebUI', 'ManagerConsole']"""
Description_ManagerAccount = "User Account"
Enabled_ManagerAccount = "True"
ID_MAnagerAccount = "root"
Links_ManagerAccount = """{'Role': {'@odata.id': '/redfish/v1/AccountService/Roles/Administrator'}}"""
Locked_ManagerAccount = "False"
Locked_Redfish_AllowableValues_ManagerAccount = """['false']"""
Name_ManagerAccount = "User Account"
PasswordChangeRequired_ManagerAccount = "False"
RoleID_MAnagerAccount = "Administrator"
StrictAccountTypes_ManagerAccount = "True"
UserName_ManagerAccount = "root"
####CONSR-OBMC-RDFT-0153-0001
resource_role_1 = "/redfish/v1/AccountService/Roles/Administrator"
data_type_role_1 = "#Role.v1_2_2.Role"
AssignedPrivileges_role_1 = """['Login', 'ConfigureManager', 'ConfigureUsers', 'ConfigureSelf', 'ConfigureComponents']"""
Description_role_1 = "Administrator User Role"
Id_role_1 = "Administrator"
IsPredefined_role_1 = "True"
Name_role_1 = "User Role"
OemPrivileges_role_1 = "[]"
RoleId_role_1 = "Administrator"
####CONSR-OBMC-RDFT-0155-0001
resource_role_3 = "/redfish/v1/AccountService/Roles/ReadOnly"
data_type_role_3 = "#Role.v1_2_2.Role"
AssignedPrivileges_role_3 = """['Login', 'ConfigureSelf']"""
Description_role_3 = "ReadOnly User Role"
Id_role_3 = "ReadOnly"
IsPredefined_role_3 = "True"
Name_role_3 = "User Role"
OemPrivileges_role_3 = "[]"
RoleId_role_3 = "ReadOnly"
####CONSR-OBMC-RDFT-0041-0001
resource_chassis_3 = "/redfish/v1/Chassis/artemis_motherboard/ResetActionInfo"
data_type_chassis_3 = "#ActionInfo.v1_1_2.ActionInfo"
ID_chassis_3 = "ResetActionInfo"
name_chassis_3 = "Reset Action Info"
Parameters_chassis_3 = """[{'AllowableValues': ['PowerCycle'], 'DataType': 'String', 'Name': 'ResetType', 'Required': True}]"""
####CONSR-OBMC-RDFT-0053-0001
resource_sensor_11 = "/redfish/v1/Chassis/artemis_motherboard/Sensors/power_PSU_B_PowerIn"
data_type_sensor_11 = "#Sensor.v1_2_0.Sensor"
Id_sensor_11 = "power_PSU_B_PowerIn"
Name_sensor_11 = "PSU B PowerIn"
ReadingRangeMax_sensor_11 = "3000.0"
ReadingRangeMin_sensor_11 = "0.0"
ReadingType_sensor_11 = "Power"
ReadingUnits_sensor_11 = "W"
Status_sensor_11 = """{'Health': 'OK', 'State': 'Enabled'}"""
####CONSR-OBMC-RDFT-0051-0001
resource_sensor_9 = "/redfish/v1/Chassis/artemis_motherboard/Sensors/power_PSU_A_PowerIn"
data_type_sensor_9 = "#Sensor.v1_2_0.Sensor"
Id_sensor_9 = "power_PSU_A_PowerIn"
Name_sensor_9 = "PSU A PowerIn"
ReadingRangeMax_sensor_9 = "3000.0"
ReadingRangeMin_sensor_9 = "0.0"
ReadingType_sensor_9 = "Power"
ReadingUnits_sensor_9 = "W"
Status_sensor_9 = """{'Health': 'OK', 'State': 'Enabled'}"""
####CONSR-OBMC-RDFT-0049-0001
resource_sensor_7 = "/redfish/v1/Chassis/artemis_motherboard/Sensors/current_PSU_B_CurrIn"
data_type_sensor_7 = "#Sensor.v1_2_0.Sensor"
Id_sensor_7 = "current_PSU_B_CurrIn"
Name_sensor_7 = "PSU B CurrIn"
ReadingRangeMax_sensor_7 = "20.0"
ReadingRangeMin_sensor_7 = "0.0"
ReadingType_sensor_7 = "Current"
ReadingUnits_sensor_7 = "A"
Status_sensor_7 = """{'Health': 'OK', 'State': 'Enabled'}"""
####CONSR-OBMC-RDFT-0047-0001
resource_sensor_5 = "/redfish/v1/Chassis/artemis_motherboard/Sensors/current_PSU_A_CurrIn"
data_type_sensor_5 = "#Sensor.v1_2_0.Sensor"
Id_sensor_5 = "current_PSU_A_CurrIn"
Name_sensor_5 = "PSU A CurrIn"
ReadingRangeMax_sensor_5 = "20.0"
ReadingRangeMin_sensor_5 = "0.0"
ReadingType_sensor_5 = "Current"
ReadingUnits_sensor_5 = "A"
Status_sensor_5 = """{'Health': 'OK', 'State': 'Enabled'}"""
####CONSR-OBMC-RDFT-0045-0001
resource_sensor_3 = "/redfish/v1/Chassis/artemis_motherboard/Sensors/current_BBU_Current"
data_type_sensor_3 = "#Sensor.v1_2_0.Sensor"
Id_sensor_3 = "current_BBU_Current"
Name_sensor_3 = "BBU Current"
ReadingRangeMax_sensor_3 = "150.0"
ReadingRangeMin_sensor_3 = "-10.0"
ReadingType_sensor_3 = "Current"
ReadingUnits_sensor_3 = "A"
Status_sensor_3 = """{'Health': 'OK', 'State': 'Enabled'}"""
####CONSR-OBMC-RDFT-0043-0001
resource_sensor_1 = "/redfish/v1/Chassis/artemis_motherboard/Sensors/current_BBU_Average_Current"
data_type_sensor_1 = "#Sensor.v1_2_0.Sensor"
Id_sensor_1 = "current_BBU_Average_Current"
Name_sensor_1 = "BBU Average Current"
ReadingRangeMax_sensor_1 = "150.0"
ReadingRangeMin_sensor_1 = "-10.0"
ReadingType_sensor_1 = "Current"
ReadingUnits_sensor_1 = "A"
Status_sensor_1 = """{'Health': 'OK', 'State': 'Enabled'}"""
####CONSR-OBMC-RDFT-0283-0001
resource_UpdateService_1 = "/redfish/v1/UpdateService"
data_type_UpdateService_1 = "#UpdateService.v1_11_1.UpdateService"
Description_UpdateService_1 = "Service for Software Update"
FirmwareInventory_UpdateService_1 = """{'@odata.id': '/redfish/v1/UpdateService/FirmwareInventory'}"""
HttpPushUri_UpdateService_1 = "/redfish/v1/UpdateService/update"
HttpPushUriOptions_UpdateService_1 = """{'HttpPushUriApplyTime': {'ApplyTime': 'OnReset'}}"""
Id_UpdateService_1 = "UpdateService"
MaxImageSizeBytes_UpdateService_1 = "68157440"
MultipartHttpPushUri_UpdateService_1 = "/redfish/v1/UpdateService/update"
Name_UpdateService_1 = "Update Service"
ServiceEnabled_UpdateService_1 = "True"
####CONSR-OBMC-RDFT-0029-0001
resource_Log_Service_5 = "/redfish/v1/Systems/system/LogServices/PostCodes"
data_type_Log_service_5 = "#LogService.v1_1_0.LogService"
Actions_Log_service_5 = """{'#LogService.ClearLog': {'target': '/redfish/v1/Systems/system/LogServices/PostCodes/Actions/LogService.ClearLog'}}"""
Description_Log_service_5 = "POST Code Log Service"
Entries_Log_service_5 = """{'@odata.id': '/redfish/v1/Systems/system/LogServices/PostCodes/Entries'}"""
Id_Log_service_5 = "PostCodes"
Name_Log_service_5 = "POST Code Log Service"
OverWritePolicy_Log_service_5 = "WrapsWhenFull"
####CONSR-OBMC-RDFT-0031-0001
resource_log_service_7 = "/redfish/v1/Managers/bmc/LogServices/Journal"
data_type_log_service_7 = "#LogService.v1_1_0.LogService"
Description_log_service_7 = "BMC Journal Log Service"
Entries_log_services_7 = """{'@odata.id': '/redfish/v1/Managers/bmc/LogServices/Journal/Entries'}"""
Id_log_services_7 = "Journal"
Name_log_service_7 = "Open BMC Journal Log Service"
OverWritePolicy_log_service_7 = "WrapsWhenFull"
####CONSR-OBMC-RDFT-0013-0001
resource_manager_1 = "/redfish/v1/Managers/bmc"
data_type_manager_1 = "#Manager.v1_14_0.Manager"
Actions_Manager_1 = """{'#Manager.Reset': {'@Redfish.ActionInfo': '/redfish/v1/Managers/bmc/ResetActionInfo', 'target': '/redfish/v1/Managers/bmc/Actions/Manager.Reset'}, '#Manager.ResetToDefaults': {'ResetType@Redfish.AllowableValues': ['ResetAll'], 'target': '/redfish/v1/Managers/bmc/Actions/Manager.ResetToDefaults'}}"""
Description_Manager_1 = "Baseboard Management Controller"
EthernetInterface_Manager_1 = """{'@odata.id': '/redfish/v1/Managers/bmc/EthernetInterfaces'}"""
GraphicalConsole_manager_1 = """{'ConnectTypesSupported': ['KVMIP'], 'MaxConcurrentSessions': 4, 'ServiceEnabled': True}"""
ID_manager_1 = "bmc"
Links_Manager_1 = """{'ActiveSoftwareImage': {'@odata.id': '/redfish/v1/UpdateService/FirmwareInventory/23d89625'}, 'ManagerForChassis': [{'@odata.id': '/redfish/v1/Chassis/artemis_motherboard'}], 'ManagerForChassis@odata.count': 1, 'ManagerForServers': [{'@odata.id': '/redfish/v1/Systems/system'}], 'ManagerForServers@odata.count': 1, 'ManagerInChassis': {'@odata.id': '/redfish/v1/Chassis/artemis_motherboard'}, 'SoftwareImages': [{'@odata.id': '/redfish/v1/UpdateService/FirmwareInventory/23d89625'}], 'SoftwareImages@odata.count': 1}"""
Logservices_manager_1 = """{'@odata.id': '/redfish/v1/Managers/bmc/LogServices'}"""
ManagerDiagnosticData_Manager_1 = """{'@odata.id': '/redfish/v1/Managers/bmc/ManagerDiagnosticData'}"""
ManagerType_manager_1 = "BMC"
Model_manager_1 = "OpenBmc"
Name_manager_1 = "OpenBmc Manager"
NetworkProtocol_manager_1 = """{'@odata.id': '/redfish/v1/Managers/bmc/NetworkProtocol'}"""
oem_manager_1 = """{'@odata.id': '/redfish/v1/Managers/bmc#/Oem', '@odata.type': '#OemManager.Oem', 'OpenBmc': {'@odata.id': '/redfish/v1/Managers/bmc#/Oem/OpenBmc', '@odata.type': '#OemManager.OpenBmc', 'Certificates': {'@odata.id': '/redfish/v1/Managers/bmc/Truststore/Certificates'}}}"""
Powerstate_manager_1 = "On"
SerialConsole_manager_1 = """{'ConnectTypesSupported': ['IPMI', 'SSH'], 'MaxConcurrentSessions': 15, 'ServiceEnabled': True}"""
status_manager_1 = """{'Health': 'OK', 'State': 'Enabled'}"""
####CONSR-OBMC-RDFT-0017-0001
resource_manager_5 = "/redfish/v1/Managers/bmc/EthernetInterfaces/eth1"
data_type_manager_5 = "#EthernetInterface.v1_9_0.EthernetInterface"
dhcpv4_manager_5 = """{'DHCPEnabled': True, 'UseDNSServers': True, 'UseDomainName': True, 'UseNTPServers': True}"""
dhcpv6_manager_5 = """{'OperatingMode': 'Stateful', 'UseDNSServers': True, 'UseDomainName': True, 'UseNTPServers': True}"""
Description_manager_5 = "Management Network Interface"
EthernetInterfaceType_manager_5 = "Physical"
FQDN_manager_5 = "artemis"
HostName_manager_5 = "artemis"
Id_manager_5 = "eth1"
Name_manager_5 = "Manager Ethernet Interface"
Status_manager_5 = """{'State': 'Enabled'}"""
####CONSR-OBMC-RDFT-0020-0001
resource_ManagersNetworkProtocol = "/redfish/v1/Managers/bmc/NetworkProtocol"
data_type_ManagersNetworkProtocol = "#ManagerNetworkProtocol.v1_5_0.ManagerNetworkProtocol"
Description_ManagersNetworkProtocol = "Manager Network Service"
FQDN_ManagersNetworkProtocol = "artemis"
HTTP_ManagersNetworkProtocol = """{'Port': None, 'ProtocolEnabled': False}"""
HTTPS_ManagersNetworkProtocol = """{'Certificates': {'@odata.id': '/redfish/v1/Managers/bmc/NetworkProtocol/HTTPS/Certificates'}, 'Port': 443, 'ProtocolEnabled': True}"""
Hostname_ManagersNetworkProtocol = "artemis"
IPMI_ManagersNetworkProtocol = """{'Port': 623, 'ProtocolEnabled': True}"""
ID_ManagersNetworkProtocol = "NetworkProtocol"
Name_ManagersNetworkProtocol = "Manager Network Protocol"
SSH_ManagersNetworkProtocol = """{'Port': 22, 'ProtocolEnabled': True}"""
Status_ManagersNetworkProtocol = """{'Health': 'OK', 'HealthRollup': 'OK', 'State': 'Enabled'}"""
####CONSR-OBMC-RDFT-0022-0001
resource_NetworkProtocol_2 = "/redfish/v1/Managers/bmc/NetworkProtocol/HTTPS/Certificates/1"
data_type_NetworkProtocol_2 = "#Certificate.v1_0_0.Certificate"
Description_networkprotocol_2 = "HTTPS Certificate"
Id_networkprotocol_2 = "1"
Issuer_networkprotocol_2 = """{'CommonName': 'testhost', 'Country': 'US', 'Organization': 'OpenBMC'}"""
KeyUsage_networkprotocol_2 = """['KeyEncipherment', 'ServerAuthentication']"""
Name_networkprotocol_2 = "HTTPS Certificate"
Subject_networkprotocol_2 = """{'CommonName': 'testhost', 'Country': 'US', 'Organization': 'OpenBMC'}"""
####CONSR-OBMC-RDFT-0287-0001
resource_CertificateService_2 = "/redfish/v1/CertificateService/CertificateLocations"
data_type_CertificateService_2 = "#CertificateLocations.v1_0_0.CertificateLocations"
Description_CertificateService_2 = "Defines a resource that an administrator can use in order to locate all certificates installed on a given service"
ID_CertificateService_2 = "CertificateLocations"
Links_CertificateService_2 = """{'Certificates': [{'@odata.id': '/redfish/v1/Managers/bmc/NetworkProtocol/HTTPS/Certificates/1'}], 'Certificates@odata.count': 1}"""
Name_CertificateService_2 = "Certificate Locations"
####CONSR-OBMC-RDFT-0148-0001
resource_AccountService_1 = "/redfish/v1/AccountService"
data_type_AccountService_1 = "#AccountService.v1_10_0.AccountService"
AccountLockoutDuration_AccountService_1 = "0"
AccountLockoutThreshold_AccountService_1 = "0"
Accounts_AccountService_1 = """{'@odata.id': '/redfish/v1/AccountService/Accounts'}"""
ActiveDirectory_AccountService_1 = """{'Authentication': {'AuthenticationType': 'UsernameAndPassword', 'Password': None, 'Username': ''}, 'LDAPService': {'SearchSettings': {'BaseDistinguishedNames': [''], 'GroupsAttribute': '', 'UsernameAttribute': ''}}, 'RemoteRoleMapping': [], 'ServiceAddresses': [''], 'ServiceEnabled': False}"""
Description_AccountService_1 = "Account Service"
ID_AccountService_1 = "AccountService"
LDAP_AccountService_1 = """{'Authentication': {'AuthenticationType': 'UsernameAndPassword', 'Password': None, 'Username': ''}, 'Certificates': {'@odata.id': '/redfish/v1/AccountService/LDAP/Certificates'}, 'LDAPService': {'SearchSettings': {'BaseDistinguishedNames': [''], 'GroupsAttribute': '', 'UsernameAttribute': ''}}, 'RemoteRoleMapping': [], 'ServiceAddresses': [''], 'ServiceEnabled': False}"""
MaxPasswordLength_AccountService_1 = "20"
MinPasswordLength_AccountService_1 = "8"
Name_AccountService_1 = "Account Service"
Oem_AccountService_1 = """{'OpenBMC': {'@odata.id': '/redfish/v1/AccountService#/Oem/OpenBMC', '@odata.type': '#OpenBMCAccountService.v1_0_0.AccountService', 'AuthMethods': {'BasicAuth': True, 'Cookie': True, 'SessionToken': True, 'TLS': True, 'XToken': True}}}"""
Roles_AccountService_1 = """{'@odata.id': '/redfish/v1/AccountService/Roles'}"""
ServiceEnabled_AccountService_1 = "True"
####CONSR-OBMC-RDFT-0026-0001
resource_Log_service_2 = "/redfish/v1/Systems/system/LogServices/EventLog/Entries"
data_type_log_service_2 = "#LogEntryCollection.LogEntryCollection"
Description_log_service_2 = "Collection of System Event Log Entries"
Members_data_nextLink_Log_service_2 = "/redfish/v1/Systems/system/LogServices/EventLog/Entries?$skip=1000"
Name_Log_service_2 = "System Event Log Entries"
#####CONSR-OBMC-RDFT-0288-0001
resource_TelemetryService_1 = "/redfish/v1/TelemetryService"
data_type_TelemetryService_1 = "#TelemetryService.v1_2_1.TelemetryService"
Id_TelemetryService_1 = "TelemetryService"
MaxReports_TelemetryService_1 = "10"
MetricReportDefinitions_TelemetryService_1 = """{'@odata.id': '/redfish/v1/TelemetryService/MetricReportDefinitions'}"""
MetricReports_TelemetryService_1 = """{'@odata.id': '/redfish/v1/TelemetryService/MetricReports'}"""
MinCollectionInterval_TelemetryService_1 = "PT1.000S"
Name_TelemetryService_1 = "Telemetry Service"
Status_TelemetryService_1 = """{'State': 'Enabled'}"""
SupportedCollectionFunctions_TelemetryService_1 = """['Maximum', 'Minimum', 'Average', 'Summation']"""
Triggers_TelemetryService_1 = """{'@odata.id': '/redfish/v1/TelemetryService/Triggers'}"""
#####CONSR-OBMC-RDFT-0154-0001
resource_role2 = "/redfish/v1/AccountService/Roles/Operator"
data_type_role2 = "#Role.v1_2_2.Role"
AssignedPrivileges_role2 = """['Login', 'ConfigureSelf', 'ConfigureComponents']"""
Description_role2 = "Operator User Role"
Id_role2 = "Operator"
IsPredefined_role2 = "True"
Name_role2 = "User Role"
OemPrivileges_role2 = "[]"
RoleId_role2 = "Operator"
#####CONSR-OBMC-RDFT-0156-0001
resource_TaskService = "/redfish/v1/TaskService"
data_type_TaskService = "#TaskService.v1_1_4.TaskService"
CompletedTaskOverWritePolicy_TaskService = "Oldest"
Id_TaskService = "TaskService"
LifeCycleEventOnTaskStateChange_TaskService = "True"
Name_TaskService = "Task Service"
ServiceEnabled_TaskService = "True"
Status_TaskService = """{'State': 'Enabled'}"""
Tasks_TaskService = """{'@odata.id': 
redfish/v1/TaskService/Tasks'}"""

####CONSR-OBMC-RDFT-0284-0001
resource_UpdateService_6 = "/redfish/v1/UpdateService/FirmwareInventory"
data_type_UpdateService_6 = "#SoftwareInventoryCollection.SoftwareInventoryCollection"
Members_odata_count_UpdateService_6 = "3"
Name_UpdateService_6 = "Software Inventory Collection"
Members_UpdateService_6 = """[{'@odata.id': '/redfish/v1/UpdateService/FirmwareInventory/23d89625'}, {'@odata.id': '/redfish/v1/UpdateService/FirmwareInventory/bios_active'}, {'@odata.id': '/redfish/v1/UpdateService/FirmwareInventory/cpld_active'}]"""
####CONSR-OBMC-RDFT-0152-0001
resource_role_152 = "/redfish/v1/AccountService/Roles"
data_type_role_152 = "#RoleCollection.RoleCollection"
Members_odata_count_role_152 = "3"
Description_role_collection_152 = "BMC User Roles"
Name_role_collection_152 = "Roles Collection"
Members_role_152 = """[{'@odata.id': '/redfish/v1/AccountService/Roles/Administrator'}, {'@odata.id': '/redfish/v1/AccountService/Roles/Operator'}, {'@odata.id': '/redfish/v1/AccountService/Roles/ReadOnly'}]"""
####CONSR-OBMC-RDFT-0080-0001
resource_thermal1 = "/redfish/v1/Chassis/artemis_motherboard/Thermal"
data_type_thermal1 = "#Thermal.v1_4_0.Thermal"
Id_thermal1 = "Thermal"
Name_thermal1 = "Thermal"
Redundancy_thermal1 = "[]"
####CONSR-OBMC-RDFT-0055-0001
resource_PowerCollection = "/redfish/v1/Chassis/artemis_motherboard/Power"
data_type_PowerCollection = "#Power.v1_5_2.Power"
ID_PowerCollection = "Power"
Name_PowerCollection = "Power"
Powercontrol_PowerCollection = """[{'@odata.id': '/redfish/v1/Chassis/artemis_motherboard/Power#/PowerControl/0', '@odata.type': '#Power.v1_0_0.PowerControl', 'MemberId': '0', 'Name': 'Chassis Power Control', 'PowerConsumedWatts': 283.75, 'PowerLimit': {'LimitException': 'NoAction'}, 'Status': {'Health': 'OK', 'State': 'Enabled'}}]"""
Voltages_PowerCollection = """[{'@odata.id': '/redfish/v1/Chassis/artemis_motherboard/Power#/Voltages/0','Status': {'Health': 'OK','State': 'Enabled'}]"""
power_status_count_check = "23"
####CONSR-OBMC-RDFT-0285-0001
resource_updateservice_7 = "/redfish/v1/UpdateService/FirmwareInventory/bios_active"
data_type_updateservice_7 = "#SoftwareInventory.v1_1_0.SoftwareInventory"
Description_updateservice_7 = "Host image"
ID_updateservice_7 = "bios_active"
Name_updateservice_7 = "Software Inventory"
RelatedItem_updateservice_7 = """[{'@odata.id': '/redfish/v1/Systems/system/Bios'}]"""
RelatedItem_odata_count_updateservice_7 = "1"
status_updateservice_7 = """{'Health': 'OK', 'HealthRollup': 'OK', 'State': 'Enabled'}"""
Updateable_updateservice_7 = "False"
Version_updateservice_7_before = "ART.2.02.01"
Version_updateservice_7_after = "ART.2.02.01"
cpld_resource_updateservice_7 = "/redfish/v1/UpdateService/FirmwareInventory/cpld_active"
cpld_data_type_updateservice_7 = "#SoftwareInventory.v1_1_0.SoftwareInventory"
cpld_Description_updateservice_7 = "CPLD image"
cpld_ID_updateservice_7 = "cpld_active"
cpld_Name_updateservice_7 = "Software Inventory"
cpld_Status_updateservice_7 = """{'Health': 'OK', 'HealthRollup': 'OK', 'State': 'Enabled'}"""
cpld_Updateable_updateservice_7 = "False"
cpld_Version_updateservice_7_before = "V1.3.20"
cpld_Version_updateservice_7_after = "V1.3.20"
resource_redfish_updateservice_update = "/redfish/v1/UpdateService/update"
filename_redfish_bios_upgrade = "/root/ART.2.02.01/obmc-bios.tar.gz"
filename_redfish_cpld_upgrade = "/root/cpld_1320/obmc-cpld.tar.gz"

