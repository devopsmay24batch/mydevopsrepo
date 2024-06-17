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

MOONSTONE = SwImage.getSwImage("MOONSTONE_BMC")
moonstone_bios_new_image=MOONSTONE.newImage
moonstone_bios_old_image=MOONSTONE.oldImage
# moonstone_bios_new_image=MOONSTONE.newVersion['bios_image']
# moonstone_bios_old_image=MOONSTONE.oldVersion['bios_image']
# moonstone_bios_new_image_version=moonstone_bios_new_image.split('Moonstone_Offline_BIOS_')[1].split('.BIN')[0]
# moonstone_bios_old_image_version=moonstone_bios_old_image.split('Moonstone_Offline_BIOS_')[1].split('.BIN')[0]
# moonstone_cpld_image = MOONSTONE.newVersion['cpld_image']


cpld_image_name = MOONSTONE.newVersion['cpld_image']
cpld_image_version = '0x' + cpld_image_name.split('Moonstone_BB_CPLD_V')[1].split('.vme')[0].lower()
cpld_image_version_lpc = '0x' + cpld_image_name.split('Moonstone_BB_CPLD_V')[1].split('.vme')[0].lower().lstrip('0')
come_cpld_version = MOONSTONE.newVersion['COMe_CPLD_version']
diag_version = MOONSTONE.newVersion['Diag_version']
switch_cpld_1_version = MOONSTONE.newVersion['Switch_CPLD_1_version']
switch_cpld_2_version = MOONSTONE.newVersion['Switch_CPLD_2_version']
fpga_version = MOONSTONE.newVersion['FPGA_version']
onl_version = MOONSTONE.newVersion['ONL_version']
moonstone_bmc_new_img = MOONSTONE.newVersion['bmc_image']
moonstone_bmc_old_img = MOONSTONE.oldVersion['bmc_image']
moonstone_bmc_ipmi_version = MOONSTONE.newVersion['ipmi_version']
moonstone_bmc_firmware_revision = MOONSTONE.newVersion['firmware_revision']
moonstone_bmc_device_revision = MOONSTONE.newVersion['device_revision']

moonstone_bmc_ipmi_version_old = MOONSTONE.oldVersion['ipmi_version']
moonstone_bmc_firmware_revision_old = MOONSTONE.oldVersion['firmware_revision']
moonstone_bmc_device_revision_old = MOONSTONE.oldVersion['device_revision']


# #dummymac=DeviceMgr.getDevice(devicename).get('dummyBmcMac')
# #realmac=DeviceMgr.getDevice(devicename).get('realBmcMac')
# #realmac=DeviceMgr.getDevice(devicename).get('realBmcMac')
# #realcomemac=DeviceMgr.getDevice(devicename).get('realComeMac')

devicename = os.environ.get("deviceName", "")
mgmt_ip = dev_info.managementIP
mgmt_ip_onl = '10.208.84.85'
mac_addr = DeviceMgr.getDevice(devicename).get('macAddress')
net_mask = DeviceMgr.getDevice(devicename).get('subnetMask')
bmc_prompt = DeviceMgr.getDevice(devicename).get('promptBmc')
bmc_user = DeviceMgr.getDevice(devicename).get('bmcUserName')
bmc_pass = DeviceMgr.getDevice(devicename).get('bmcPassword')
# # bmc_sec_ip = DeviceMgr.getDevice(devicename).get('secondryManagementIp')
# # device_mac_string =  DeviceMgr.getDevice(devicename).get('macAddressString')

# DIAGOS = "DIAGOS"
# cmd_ipmitool_user_list_1 = 'ipmitool user list 1'
set_bmc_ipaddr = "10.208.84.86"
dhcp_add = 'DHCP Address'
set_bmc_netmask = "255.255.255.0"
static_add = 'Static Address'
# write_fru1_mac = r"0093afe5c282"
# response_lan1_mac = r"00:93:af:e5:c2:82"

# wrong_mac = r"0000000002G2"
# response_wrong_mac = r"00:00:00:00:02:G2"

# bmc_memory_disabled=r"00 00"
# bmc_memory_enabled=r"00 01"


# #sel_list_power_on_pattern = [r"System ACPI Power State #0x0a | S5/G2: soft-off | Asserted",
# #r"System ACPI Power State #0x0a | S0/G0: working | Asserted"]

# sel_list_power_on_pattern = [r"working | Asserted"]


# #sel_list_mc_reset_pattern = [r"Power Supply #0x0f | Power Supply AC lost | Asserted",
# #r"Power Supply #0x10 | Presence detected | Asserted"]
# sel_list_mc_reset_pattern = [r"Power Supply\s+.*| Asserted"]

lanplus_ipmitool_cmd='ipmitool -I lanplus -H '+ mgmt_ip + ' -U root -P 0penBmc -C 17 {}'
# mc_info = "mc info"
# bmc_status = "raw 0x32 0x8f 0x08 0x01"
# sel_list = "sel list"
# update_primary_bmc_cmd="./CFUFLASH -nw -ip "+ mgmt_ip +" -u admin -p admin -d 1 -mse 1 "+ moonstone_bmc_new_img
# no_update_required_pattern=r"Existing Image and Current Image are same"
# reset_firmware_pattern=r"Resetting the firmware."


# bmc_status_disabled="00 00"
# bmc_status_enabled="00 01"
bmc_version_info_list = [
    "Device ID.*32",
    "Device Revision.*" + moonstone_bmc_device_revision,
    "Firmware Revision.*" + moonstone_bmc_firmware_revision,
    "IPMI Version.*" + moonstone_bmc_ipmi_version,
    "Manufacturer ID.*12290",
]
bmc_version_info_list_old = [
    "Device ID.*32",
    "Device Revision.*" + moonstone_bmc_device_revision_old,
    "Firmware Revision.*" + moonstone_bmc_firmware_revision_old,
    "IPMI Version.*" + moonstone_bmc_ipmi_version_old,
    "Manufacturer ID.*12290",
]

# bmc_default_user_list=["ID\s+Name\s+Callin\s+Link Auth\s+IPMI Msg\s+Channel Priv Limit",
# "1\s+false\s+false\s+true\s+ADMINISTRATOR",
# "2\s+admin\s+false\s+false\s+true\s+ADMINISTRATOR",
# "3\s+true\s+false\s+false\s+NO ACCESS",
# "4\s+true\s+false\s+false\s+NO ACCESS",
# "5\s+true\s+false\s+false\s+NO ACCESS",
# "6\s+true\s+false\s+false\s+NO ACCESS",
# "7\s+true\s+false\s+false\s+NO ACCESS",
# "8\s+true\s+false\s+false\s+NO ACCESS",
# "9\s+true\s+false\s+false\s+NO ACCESS",
# "10\s+true\s+false\s+false\s+NO ACCESS",
# "11\s+true\s+false\s+false\s+NO ACCESS",
# "12\s+true\s+false\s+false\s+NO ACCESS",
# "13\s+true\s+false\s+false\s+NO ACCESS",
# "14\s+true\s+false\s+false\s+NO ACCESS",
# "15\s+true\s+false\s+false\s+NO ACCESS",
# ]

# bmc_status_enabled=r"01 02"
# error_pass_size = "Failure: wrong password size"
# error_pass_incorrect = "Failure: password incorrect"
# success_pass = "Success"

# user_priv_error_pattern="IPMI command failed: Insufficient privilege level"
# chassis_status_pattern = r"Chassis Power is on|off"

# sol_info_dict = {"enabled":"Enabled", "force-encryption":"Force Encryption", "force-authentication":"Force Authentication", "non-volatile-bit-rate":"Non-Volatile Bit Rate", "volatile-bit-rate":"Volatile Bit Rate"} 


# sol_default_pattern = ["Set in progress\s+:\s+set-complete",
# "Enabled\s+:\s+true",
# "Force Encryption\s+:\s+false",
# "Force Authentication\s+:\s+false",
# "Privilege Level\s+:\s+USER",
# "Character Accumulate Level.*:\s+60",
# "Character Send Threshold\s+:\s+96",
# "Retry Count\s+:\s+7",
# "Retry Interval.*500",
# "Volatile Bit Rate.*115.2",
# "Non-Volatile Bit Rate.*115.2",
# "Payload Channel.*(0x01)",
# "Payload Port\s+:\s+623"]

# sel_clear_pattern="Clearing SEL.  Please allow a few seconds to erase."
# sel_list_after_clear_pattern= "Event Logging Disabled #0x55 | Log area reset/cleared | Asserted"
# self_test_pattern = r"55 00"

# version2 = MOONSTONE.newVersion['bmc_image_version']
# version1 = MOONSTONE.oldVersion['bmc_image_version']

# sel_list_after_updating_image=["Power Supply.*| Presence detected | Asserted"]
# fru_device_name = ["system", "bmc", "come", "psu1", "psu2", "fan1", "fan2", "fan3", "fan4", "sw"]
# bios_image = moonstone_bios_old_image
# cpld_image_to_version_mapping = { cpld_image_name:cpld_image_version }
# fru_list_pattern = ["Builtin FRU Device.*ID 0.*", "FRU_BMC.*ID 1", "FRU_COME.*ID 2", "FRU_PSU1.*ID 3", "FRU_PSU2.*ID 4", "FRU_FAN1.*ID 5", 
    # "FRU_FAN2.*ID 6", "FRU_FAN3.*ID 7", "FRU_FAN4.*ID 8", "FRU_SW.*ID 9"]
# sensor_device = ["Fan 1", "Fan 2", "Fan 3", "Fan 4", "PSU 1", "PSU 2"]
# enable_fcs = "01"
# disable_fcs = "00"
new_bios_image = moonstone_bios_new_image
old_bios_image = moonstone_bios_old_image
# cfuflash_path = "BMC/CFUFLASH"
# sensor_name_list = {"11":"Fan1_Rear", "12":"Fan1_Front", "13":"Fan2_Rear", "14":"Fan2_Front","15":"Fan3_Rear", "16":"Fan3_Front","17":"Fan4_Rear", "18":"Fan4_Front"}
# event_generation_script="event_generation_test.sh"
# moonstone_home_path="8080/MOONSTONE/"
image_path_in_bmc="/run/initramfs/"
image_path_in_server="moonstone_images/"
lan_stress_script='lan_stress_test.sh'
kcs_stress_script='kcs_stress_test.sh'
kcs_stress_script_log='kcs_stress.log'