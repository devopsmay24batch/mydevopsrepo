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

import os
import DeviceMgr
from SwImage import SwImage
from Const import BOOT_MODE_UBOOT, BOOT_MODE_DIAGOS, BOOT_MODE_ONIE,ONIE_RESCUE_MODE
dev_info = DeviceMgr.getDevice()

pc_info = DeviceMgr.getServerInfo('PC')
scp_ip = pc_info.managementIP
scp_username = pc_info.scpUsername
scp_password = pc_info.scpPassword
dhcp_username = pc_info.username
dhcp_password = pc_info.password
dhcp_prompt = pc_info.prompt

SEASTONE = SwImage.getSwImage("SEASTONE_BMC")
seastone_bios_new_image=SEASTONE.newImage
seastone_bios_old_image=SEASTONE.oldImage
seastone_clpd_image = SEASTONE.newVersion['clpd_image']


clpd_image_name = SEASTONE.newVersion['clpd_image']
clpd_image_version = SEASTONE.newVersion['clpd_image_version']
seastone_bmc_new_img = SEASTONE.newVersion['bmc_image']
seastone_bmc_old_img = SEASTONE.oldVersion['bmc_image']
seastone_bmc_ipmi_version = SEASTONE.newVersion['ipmi_version']
seastone_bmc_firmware_revision = SEASTONE.newVersion['firmware_revision']
sestone_bmc_device_revision = SEASTONE.newVersion['device_revision']
seastone_bmc_new_img_version = SEASTONE.newVersion['bmc_image_version']
seastone_bmc_old_img_version = SEASTONE.oldVersion['bmc_image_version']


#dummymac=DeviceMgr.getDevice(devicename).get('dummyBmcMac')
#realmac=DeviceMgr.getDevice(devicename).get('realBmcMac')
#realmac=DeviceMgr.getDevice(devicename).get('realBmcMac')
#realcomemac=DeviceMgr.getDevice(devicename).get('realComeMac')

devicename = os.environ.get("deviceName", "")
mgmt_ip = dev_info.managementIP
mgmt_ip1 = DeviceMgr.getDevice(devicename).get('managementIP')
mac_addr = DeviceMgr.getDevice(devicename).get('macAddress')
net_mask = DeviceMgr.getDevice(devicename).get('subnetMask')
bmc_prompt = DeviceMgr.getDevice(devicename).get('promptBmc')
bmc_user = DeviceMgr.getDevice(devicename).get('bmcUserName')
bmc_pass = DeviceMgr.getDevice(devicename).get('bmcPassword')
bmc_sec_ip = DeviceMgr.getDevice(devicename).get('secondryManagementIp')
device_mac_string =  DeviceMgr.getDevice(devicename).get('macAddressString')

DIAGOS = "DIAGOS"
cmd_ipmitool_user_list_1 = 'ipmitool user list 1'
set_bmc_ipaddr = "10.208.80.121"
dhcp_add = 'DHCP Address'
set_bmc_netmask = "255.255.255.0"
static_add = 'Static Address'
write_fru1_mac = r"0093afe5c282"
response_lan1_mac = r"00:93:af:e5:c2:82"

wrong_mac = r"0000000002G2"
response_wrong_mac = r"00:00:00:00:02:G2"

bmc_memory_disabled=r"00 00"
bmc_memory_enabled=r"00 01"


#sel_list_power_on_pattern = [r"System ACPI Power State #0x0a | S5/G2: soft-off | Asserted",
#r"System ACPI Power State #0x0a | S0/G0: working | Asserted"]

sel_list_power_on_pattern = [r"working | Asserted"]


#sel_list_mc_reset_pattern = [r"Power Supply #0x0f | Power Supply AC lost | Asserted",
#r"Power Supply #0x10 | Presence detected | Asserted"]
sel_list_mc_reset_pattern = [r"Power Supply\s+.*| Asserted"]

lanplus_ipmitool_cmd='ipmitool -I lanplus -H '+ mgmt_ip + ' -U admin -P admin {}'
lanplus_ipmitool_tester_cmd='ipmitool -L USER -I lanplus -H '+ mgmt_ip + ' -U tester -P testtest {}'
lanplus_ipmitool_tester1_cmd='ipmitool -L OPERATOR -I lanplus -H '+ mgmt_ip + ' -U tester1 -P testtest1 {}'
lanplus_ipmitool_tester2_cmd='ipmitool -L ADMINISTRATOR -I lanplus -H '+ mgmt_ip + ' -U tester2 -P testtest2 {}'
mc_info = "mc info"
bmc_status = "raw 0x32 0x8f 0x08 0x01"
sel_list = "sel list"
update_primary_bmc_cmd="./CFUFLASH -nw -ip "+ mgmt_ip +" -u admin -p admin -d 1 -mse 1 "+ seastone_bmc_new_img
no_update_required_pattern=r"Existing Image and Current Image are same"
reset_firmware_pattern=r"Resetting the firmware."


bmc_status_disabled="00 00"
bmc_status_enabled="00 01"
bmc_version_info_list = [
    "Device ID.*32",
    "Device Revision.*" + sestone_bmc_device_revision,
    "Firmware Revision.*" + seastone_bmc_firmware_revision,
    "IPMI Version.*" + seastone_bmc_ipmi_version,
    "Manufacturer ID.*12290",
]

bmc_default_user_list=["ID\s+Name\s+Callin\s+Link Auth\s+IPMI Msg\s+Channel Priv Limit",
"1\s+false\s+false\s+true\s+ADMINISTRATOR",
"2\s+admin\s+false\s+false\s+true\s+ADMINISTRATOR",
"3\s+true\s+false\s+false\s+NO ACCESS",
"4\s+true\s+false\s+false\s+NO ACCESS",
"5\s+true\s+false\s+false\s+NO ACCESS",
"6\s+true\s+false\s+false\s+NO ACCESS",
"7\s+true\s+false\s+false\s+NO ACCESS",
"8\s+true\s+false\s+false\s+NO ACCESS",
"9\s+true\s+false\s+false\s+NO ACCESS",
"10\s+true\s+false\s+false\s+NO ACCESS",
"11\s+true\s+false\s+false\s+NO ACCESS",
"12\s+true\s+false\s+false\s+NO ACCESS",
"13\s+true\s+false\s+false\s+NO ACCESS",
"14\s+true\s+false\s+false\s+NO ACCESS",
"15\s+true\s+false\s+false\s+NO ACCESS",
]

bmc_status_enabled=r"01 02"
error_pass_size = "Failure: wrong password size"
error_pass_incorrect = "Failure: password incorrect"
success_pass = "Success"

user_priv_error_pattern="IPMI command failed: Insufficient privilege level"
chassis_status_pattern = r"Chassis Power is on|off"

sol_info_dict = {"enabled":"Enabled", "force-encryption":"Force Encryption", "force-authentication":"Force Authentication", "non-volatile-bit-rate":"Non-Volatile Bit Rate", "volatile-bit-rate":"Volatile Bit Rate"} 


sol_default_pattern = ["Set in progress\s+:\s+set-complete",
"Enabled\s+:\s+true",
"Force Encryption\s+:\s+false",
"Force Authentication\s+:\s+false",
"Privilege Level\s+:\s+USER",
"Character Accumulate Level.*:\s+60",
"Character Send Threshold\s+:\s+96",
"Retry Count\s+:\s+7",
"Retry Interval.*500",
"Volatile Bit Rate.*115.2",
"Non-Volatile Bit Rate.*115.2",
"Payload Channel.*(0x01)",
"Payload Port\s+:\s+623"]

sel_clear_pattern="Clearing SEL.  Please allow a few seconds to erase."
sel_list_after_clear_pattern= "Event Logging Disabled #0x55 | Log area reset/cleared | Asserted"
self_test_pattern = r"55 00"

version2 = seastone_bmc_new_img_version
version1 = seastone_bmc_old_img_version

sel_list_after_updating_image=["Power Supply.*| Presence detected | Asserted"]
fru_device_name = ["system", "bmc", "come", "psu1", "psu2", "fan1", "fan2", "fan3", "fan4", "sw"]
bios_image = seastone_bios_old_image
clpd_image_to_version_mapping = { clpd_image_name:clpd_image_version }
fru_list_pattern = ["Builtin FRU Device.*ID 0.*", "FRU_BMC.*ID 1", "FRU_COME.*ID 2", "FRU_PSU1.*ID 3", "FRU_PSU2.*ID 4", "FRU_FAN1.*ID 5", 
    "FRU_FAN2.*ID 6", "FRU_FAN3.*ID 7", "FRU_FAN4.*ID 8", "FRU_SW.*ID 9"]
sensor_device = ["Fan 1", "Fan 2", "Fan 3", "Fan 4", "PSU 1", "PSU 2"]
enable_fcs = "01"
disable_fcs = "00"
new_bios_image = seastone_bios_new_image
old_bios_image = seastone_bios_old_image
cfuflash_path = "BMC/CFUFLASH"
sensor_name_list = {"11":"Fan1_Rear", "12":"Fan1_Front", "13":"Fan2_Rear", "14":"Fan2_Front","15":"Fan3_Rear", "16":"Fan3_Front","17":"Fan4_Rear", "18":"Fan4_Front"}
event_generation_script="event_generation_test.sh"
sdr_variable_file="SDR_except.csv"
sdr_generation_script="sdr_info_get.sh"
seastone_home_path="8080/SEASTONE/"

bmc_version_info_list = [
    "Device ID.*32",
    "Device Revision.*1",
    "Firmware Revision.*2.0",
    "IPMI Version.*2.0",
    "Manufacturer ID.*12290",
]

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

cmd_Get_PEF_Capabilities = 'ipmitool raw 04 0x10'
rsp_Get_PEF_Capabilities = '51 3f 28'


# Case: 9.8.1 PEF_Configuration_Test
cmd_get_pef_Capabilities = r"ipmitool raw 0x04 0x10"
show_pef = r"ipmitool pef filter list"
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


