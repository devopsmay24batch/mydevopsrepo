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
import os
from collections import OrderedDict
import DeviceMgr
import CommonLib
from SwImage import SwImage
deviceM = DeviceMgr.getDevice()
#MOONSTONE_ONL = SwImage.getSwImage("MOONSTONE_ONL")
##### Variable file used for bmc.robot #####

#MOONSTONE = SwImage.getSwImage("MOONSTONE_DIAG")
#moonstone_diag_version=MOONSTONE.newVersion

pc_info = DeviceMgr.getServerInfo('PC')

scp_ip = pc_info.managementIP
scp_username = pc_info.scpUsername
scp_password = pc_info.scpPassword
dhcp_username = pc_info.username
dhcp_password = pc_info.password
dhcp_prompt = pc_info.prompt


MOONSTONE = CommonLib.get_swinfo_dict("MOONSTONE_ONL")

exp_bios_version = MOONSTONE.get("bios_version").get("NEW_IMAGE","")

exp_onie_version = MOONSTONE.get('onieVersionName')
exp_bmc_version = MOONSTONE.get('bmcVersion')
devicename = os.environ.get("deviceName", "")
exp_mac_addr=DeviceMgr.getDevice(devicename).get('realComeMac') 

exp_diag_version = MOONSTONE.get('diagVersion')
#exp_fpga_version = '0x00010004'
exp_fpga_version = MOONSTONE.get('fpgaVersion')
exp_come_cpld_version = MOONSTONE.get('comeCpldVersion')
exp_bb_cpld_version = MOONSTONE.get('bbCpldVersion')
exp_switch_cpld_version = MOONSTONE.get('switchCpldVersion')
exp_onl_version = MOONSTONE.get('onlVersion')
exp_onl_sysinfo = MOONSTONE.get('onlSysinfo')
exp_sys_OID = MOONSTONE.get('sysOID')
device_OID = MOONSTONE.get('deviceOID')
onie_version = MOONSTONE.get('onieVersion')
tlv_onie = {'0x29': onie_version}
exp_product_name = MOONSTONE.get('productName')
bios_deb_image = MOONSTONE.get("bios_version").get("bios_deb_image","")
default_mac='B4:DB:91:99:B7:A4'
old_diag_version='3.1.0'
PlatformEnv = {
    "SysInfo": {
        "ProductName": "DX030",
        "Label": "Moonstone",
     },
    "PSU": {
        "Total": 4,
        "PSU-1": {
          "FAN_Index": [ ],
          "Thermal_Index": [ ],
          },
         "PSU-2": {
          "FAN_Index": [ ],
          "Thermal_Index": [ ],
         },
         },
    "FAN": {
        "Total": 6,
        "FAN_Index": [1, 2, 3, 4, 5, 6],
        "Airflow": "Back-to-Front",
        },
    "LED": {
        "Total": 4,
        "SYSTEM_LED": 1,
        #"Chassis_FAN_LED": [2, 3, 4, 5],
        "ALERT_LED": 2,
        "PSU_LED": [3],
        "FAN_LED": 4,
    },
    "Thermal": {
         "Total": 10,
         "Thermal_Index": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
         "Thermal_Description": [
                                "CPU_Temp", \
                                "TEMP_DIMMA0", "Base_Temp_U5", \
                                "Base_Temp_U56", "Switch_Temp_U17", \
                                "Switch_Temp_U18", "Switch_Temp_U29", \
                                "Switch_Temp_U28", "VDD_CORE_T", \
                                "VDD_ANLG_Temp"],
                },
}
exp_device_info = {'System Information': 
                      {'Product Name': exp_product_name, 'Part Number': 'R4028-F9001-01', 'Serial Number': 'SN number', 
                       'MAC': 'bc:e8:04:03:33:f5|'+exp_mac_addr ,
                       'MAC Range': 2, 'Manufacturer': 'Celestica', 'Manufacture Date': '05/12/2022 00:00:01',
                       'Vendor': 'Celestica', 'Platform Name': 'Broadwell-DE', 'Device Version': '7',
                       'Label Revision': 'Moonstone', 'Country Code': 'THA', 'Diag Version': exp_diag_version, 'Service Tag': 'LB',
                       'ONIE Version': onie_version 
                       }
                       
                      

                  }
exp_ipmi_info = {'Builtin FRU Device (ID 0)':
                 {'Board Mfg Date': 'Wed Jul 24 00:00:00 2019', 'Board Mfg': 'Celestica', 'Board Product': 'Base Board', 'Board Serial': 'R4039-G0002-01xxxxxxxxxxxx',
                  'Board Part Number': 'R4039-G0002-01', 'Board Extra': 'DS3000-baseboard', 'Product Manufacturer': 'Celestica', 'Product Name': 'DS3000',
                  'Product Part Number': 'R4039-F9001-01', 'Product Serial': 'R4039B2F072815PS200003', 'Product Extra': '134'}}
port = '01'
reboot_count = 2
moonstone_home_path = "80/MOONSTONE/DVT/"
dpkg_install_pattern = ["Being postinst processed!"]
#########################################
"""
Common Setting
"""
tftp_file_path = r"/var/lib/tftpboot/"
http_file_path = r"/usr/local/apache2/htdocs/"

#tftp_server_ip = r"10.208.80.203"
tftp_server_ip = r"10.208.84.203"
http_server_ip = r"10.208.84.203/MOONSTONE/DVT"
device_type = "DUT"
pdu_port = 3
ONIE_UPDATE_MODE = 'update'
ONIE_RESCUE_MODE = 'rescue'
ONIE_INSTALL_MODE = 'installer'
ONIE_UNINSTALL_MODE = 'uninstall'

tftp_root_path = "/srv/tftp"
http_root_path = "/var/www/html"
PROTOCOL_TFTP = 'tftp'
PROTOCOL_HTTP = 'http'

netmask='255.255.255.0'


"""
Case Setting
"""
# Case: Static_IP+TFTP
static_ip = deviceM.managementIP
#bmcManagementIp-deviceM.bmcManagementIp
default_gateway="10.208.84.1"
MOONSTONE_ONIE = SwImage.getSwImage("MOONSTONE_ONIE")
version=MOONSTONE_ONIE.newVersion
ONIEimage=MOONSTONE_ONIE.newImage

MOONSTONE_ONL = SwImage.getSwImage("MOONSTONE_ONL")
ONLversion=MOONSTONE_ONL.newVersion
ONLimage=MOONSTONE_ONL.newImage
moonstone_onl_image_path = "/home/brixia/gitcap/Moonstone/automation/"


RUN_TIME='900'

# Case: TC_005  Install_Sonic_via_Static_IP+TFTP
set_onie_static_ip = deviceM.managementIP  
diagos_install_msg = 'Installing SONiC in ONIE'
diagos_install_pass = 'Installed SONiC base image SONiC-OS successfully'

# Case : FPGA check
default_fpga_scratch_value = "0x00000000"
write_fpga_scratch1 = "0x01"
write_fpga_scratch2 = '0xa5'
test_register_value = '0xfa'
test_register = '0x0004'
fpga_scratch_dict = {default_fpga_scratch_value:default_fpga_scratch_value, write_fpga_scratch1:"0x00000001", write_fpga_scratch2:"0x000000a5", test_register_value:"0x000000fa"}
baseboard_scratch_write_1="0x01"
baseboard_scratch_write_2="0xa5"
baseboard_getreg_write_1="0xbc"
sys_led=["on", "off", "1hz", "4hz"]
sys_led_color=["off", "yellow", "green", "both"]
default_scratch_value="0xde"
incorrect_login="Login incorrect"
all_device_oid_test = ["psu,PSU 1,1"]
"""all_device_oid_test=["psu,PSU 1,1",
"psu,PSU 2,2",
"psu,PSU 3,3",
"psu,PSU 4,4",
"thermal,Thermal 1,1",
"thermal,Thermal 2,2",
"thermal,Thermal 3,3",
"thermal,Thermal 4,4",
"thermal,Thermal 5,5",
"thermal,Thermal 6,6",
"fan,Fan 1,1",
"fan,Fan 2,2",
"fan,Fan 3,3",
"fan,Fan 4,4",
"fan,Fan 5,5",
"fan,Fan 6,6",
]"""
onlpdump_pattern = [
"System Information:",
       "Product Name: moonstone|Moonstone",
       "Part Number: R4028-F9001-02",
       "Serial Number: SN number",
       "MAC: b4:db:91:99:bd:a4",
       "MAC Range: 384",
       "Manufacturer: Celestica",
       "Vendor: Celestica",
       "Platform Name: x86-64-cel-moonstone-r0",
       "Label Revision: Moonstone",
       "Country Code: THA",
       "Diag Version: 1.0.0|"+exp_diag_version,
       "Service Tag: LB",
       "ONIE Version: "+onie_version,
   
   "psu @ 1",
       "Description: PSU-Top-Right",
       "Model:  TDPS2000LB A",
       "Status: 0x00000001 \[ PRESENT \]",
       "Caps:   0x00000001 \[ AC \]",
       "Vin:    0",
       "Vout:   0",
       "Iin:    0",
       "Iout:   0",
       "Pin:    0",
       "Pout:   0",


   
   "psu @ 2",
       "Description: PSU-Bottom_Right",
       "Model:  TDPS2000LB A",
       "Status: 0x00000001 \[ PRESENT \]",
       "Caps:   0x00000001 \[ AC \]",
       "Vin:    0",
       "Vout:   0",
       "Iin:    0",
       "Iout:   0",
       "Pin:    0",
       "Pout:   0",
       

   "psu @ 3",
       "Description: PSU-Top-Left",
       "Model:  TDPS2000LB A",
       "Status: 0x00000005 \[ PRESENT,UNPLUGGED \]",
       "Caps:   0x00000001 \[ AC \]",
       "Vin:    0",
       "Vout:   0",
       "Iin:    0",
       "Iout:   0",
       "Pin:    0",
       "Pout:   0",

   "psu @ 4",
       "Description: PSU-Bottom_Left",
       "Model:  TDPS2000LB A",
       "Status: 0x00000005 \[ PRESENT,UNPLUGGED \]",
       "Caps:   0x00000001 \[ AC \]",
       "Vin:    0",
       "Vout:   0",
       "Iin:    0",
       "Iout:   0",
       "Pin:    0",
       "Pout:   0",
       
   "led @ 1",
       "Description: System LED \(Front\)",
       "Status: 0x00000005 \[ PRESENT,ON \]",
       "Caps.*\[ ON_OFF,YELLOW,YELLOW_BLINKING,GREEN,GREEN_BLINKING,AUTO \]",
       "Mode: [AUTO_BLINKING|GREEN|AUTO]",
  
   "led @ 2",
       "Description: Alert LED \(Front\)",
       "Status: 0x00000005 \[ PRESENT,ON \]",
       "Caps.*\[ ON_OFF,YELLOW,YELLOW_BLINKING,GREEN,GREEN_BLINKING \]",
       "Mode: [AUTO_BLINKING|GREEN|AUTO]",
       
   
   "led @ 3",
       "Description: PSU LED \(Front\)",
       "Status: 0x00000005 \[ PRESENT,ON \]",
       "Caps.*\[ ON_OFF,GREEN,AUTO,AMBER \]",
       "Mode: [AUTO_BLINKING|GREEN|AUTO]",
       
   "led @ 4",
       "Description: FAN LED \(Front\)",
       "Status: 0x00000005 \[ PRESENT,ON \]",
       "Caps.*\[ ON_OFF,GREEN,AUTO,AMBER \]",
       "Mode: [AUTO_BLINKING|GREEN|AUTO]",
       
   "led @ 5",
       "Description: FAN1 LED \(Back\)",
       "Status: 0x00000005 \[ PRESENT,ON \]",
       "Caps.*\[ ON_OFF,GREEN,AMBER \]",
       "Mode: [AUTO_BLINKING|GREEN|AUTO]",
   
   "led @ 6",
       "Description: FAN2 LED \(Back|BACK\)",
       "Status: 0x00000005 \[ PRESENT,ON \]",
       "Caps.*\[ ON_OFF,GREEN,AMBER \]",
       "Mode: [AUTO_BLINKING|GREEN|AUTO]",
   
   "led @ 7",
       "Description: FAN3 LED \(Back|BACK\)",
       "Status: 0x00000005 \[ PRESENT,ON \]",
       "Caps.*\[ ON_OFF,GREEN,AMBER \]",
       "Mode: [AUTO_BLINKING|GREEN|AUTO]",
   
   "thermal @ 1",
       "Description: 12V_ENTRY_LEFT",
       "Status: 0x00000001 \[ PRESENT \]",
       "Caps:   0x0000000f \[ GET_TEMPERATURE,GET_WARNING_THRESHOLD,GET_ERROR_THRESHOLD,GET_SHUTDOWN_THRESHOLD \]",
       
   
   "thermal @ 2",
       "Description: 12V_ENTRY_RIGHT",
       "Status: 0x00000001 \[ PRESENT ]",
       "Caps:   0x0000000f \[ GET_TEMPERATURE,GET_WARNING_THRESHOLD,GET_ERROR_THRESHOLD,GET_SHUTDOWN_THRESHOLD \]",
       
   
   "thermal @ 3",
       "Description: BB_BUSBAR_TEMP",
       "Status: 0x00000001 \[ PRESENT \]",
       "Caps:   0x0000000f \[ GET_TEMPERATURE,GET_WARNING_THRESHOLD,GET_ERROR_THRESHOLD,GET_SHUTDOWN_THRESHOLD \]",
      
   
   "thermal @ 4",
       "Description: BB_OUTLET_TEMP",
       "Status: 0x00000001 \[ PRESENT \]",
       "Caps:   0x0000000f \[ GET_TEMPERATURE,GET_WARNING_THRESHOLD,GET_ERROR_THRESHOLD,GET_SHUTDOWN_THRESHOLD \]",
       
   
   "thermal @ 5",
       "Description: TH5_REAR_LEFT",
       "Status: 0x00000001 \[ PRESENT \]",
       "Caps:   0x0000000f \[ GET_TEMPERATURE,GET_WARNING_THRESHOLD,GET_ERROR_THRESHOLD,GET_SHUTDOWN_THRESHOLD \]",
       
   
   "thermal @ 6",
       "Description: TH5_REAR_RIGHT",
       "Status: 0x00000001 \[ PRESENT \]",
       "Caps:   0x0000000f \[ GET_TEMPERATURE,GET_WARNING_THRESHOLD,GET_ERROR_THRESHOLD,GET_SHUTDOWN_THRESHOLD \]",
       
   
   "fan @ 1",
       "Description: Chassis Fan 1 Front",
       "Status: 0x00000001 \[ PRESENT \]",
       "Caps:   0x00000033 \[ B2F,F2B,GET_RPM,GET_PERCENTAGE \]",
       "Model:  R4028-G0005-02",
       
   
   "fan @ 2",
       "Description: Chassis Fan 1 Rear",
       "Status: 0x00000001 \[ PRESENT \]",
       "Caps:   0x00000033 \[ B2F,F2B,GET_RPM,GET_PERCENTAGE \]",
       "Model:  R4028-G0005-02",
       
   
   "fan @ 3",
       "Description: Chassis Fan 2 Front",
       "Status: 0x00000001 \[ PRESENT \]",
       "Caps:   0x00000033 \[ B2F,F2B,GET_RPM,GET_PERCENTAGE \]",
       "Model:  R4028-G0005-02",
       
   
   "fan @ 4",
       "Description: Chassis Fan 2 Rear",
       "Status: 0x00000001 \[ PRESENT \]",
       "Caps:   0x00000033 \[ B2F,F2B,GET_RPM,GET_PERCENTAGE \]",
       "Model:  R4028-G0005-02",
       
   
   "fan @ 5",
       "Description: Chassis Fan 3 Front",
       "Status: 0x00000001 \[ PRESENT \]",
       "Caps:   0x00000033 \[ B2F,F2B,GET_RPM,GET_PERCENTAGE \]",
       "Model:  R4028-G0005-02",
       
   
   "fan @ 6",
       "Description: Chassis Fan 3 Rear",
       "Status: 0x00000001 \[ PRESENT \]",
       "Caps:   0x00000033 \[ B2F,F2B,GET_RPM,GET_PERCENTAGE \]",
       "Model:  R4028-G0005-02",
   "SFPs:",
  "Presence Bitmap:",
  "RX_LOS Bitmap:",

]


switch_cpld_register_value={"0x01":"0xde", "0x21":"0x21", "0xa5":"0xa5", '0x13':'0x13'}
commands_in_reset_test=['fdisk -l', 'i2cdetect -l', 'ifconfig']
fdisk_op_re=[]
iterations=5
fdisk_op_re.append('Device.*Size.*Type')
fdisk_op_re.append('\/dev\/sda1.*[0-9]+(M|G).*EFI System')
fdisk_op_re.append('\/dev\/sda2.*[0-9]+(M|G).*ONIE boot')
fdisk_op_re.append('\/dev\/sda3.*[0-9]+(M|G).*Microsoft basic data')
fdisk_op_re.append('\/dev\/sda4.*[0-9]+(M|G).*Microsoft basic data')
fdisk_op_re.append('\/dev\/sda5.*[0-9]+(M|G).*Microsoft basic data')
fdisk_op_re.append('\/dev\/sda6.*[0-9]+(M|G).*Microsoft basic data')
onl_stress_test_pattern = ["Log: 1 nodes, 8 cpus.", "Stats: Starting SAT, 28800M, 60 seconds", "Stats: Found 0 hardware incidents", "Status: PASS - please verify no corrected errors"]

onlpd_m_pattern=["\[onlp\] Fan 1 has been inserted",
"\[onlp\] Fan 2 has been inserted",
"\[onlp\] Fan 3 has been inserted",
"\[onlp\] Fan 4 has been inserted",
"\[onlp\] Fan 5 has been inserted",
"\[onlp\] Fan 6 has been inserted",
"\[onlp\] PSU 1 has been inserted",
"\[onlp\] PSU 2 has been inserted",
"\[onlp\] PSU 3 has been inserted",
"\[onlp\] PSU 4 has been inserted"]

lsmod_pattern=[
"Module.*Size.*Used by",
"tpm_crb.*0",
"jc42.*0",
"x86_pkg_temp_thermal.*0",
"gpio_ich.*0",
"ipmi_si.*0",
"tpm_tis.*0",
"ipmi_devintf.*0",
"tpm_tis_core.*1 tpm_tis",
"ipmi_msghandler.*2\s+ipmi_devintf,ipmi_si",
"tpm.*3\s+tpm_tis,tpm_crb,tpm_tis_core",
"i2c_imc.*0",
"optoe.*0",
"at24.*0",
"cpld_b.*0",
"cls_sw_fpga.*0",
"i2c_xiic_fpga.*0"]

snmp_message_stop_pattern="\[snmp_subagent\] snmp subagent unregister for module onlp_snmp succeeded."
snmp_message_oid_pattern=["collect: PSU:1",
"collect: PSU:2",
"collect: PSU:3",
"collect: PSU:4",
"collect: LED:1",
"collect: LED:2",
"collect: LED:3",
"collect: LED:4",
"collect: LED:5",
"collect: LED:6",
"collect: LED:7",
"collect: THERMAL:1",
"collect: THERMAL:2",
"collect: THERMAL:3",
"collect: THERMAL:4",
"collect: THERMAL:5",
"collect: THERMAL:6",
"collect: FAN:1",
"collect: FAN:2",
"collect: FAN:3",
"collect: FAN:4",
"collect: FAN:5",
"collect: FAN:6",
"update sensor 1 - 12V_ENTRY_LEFT",
"update sensor 2 - 12V_ENTRY_RIGHT",
"update sensor 3 - BB_BUSBAR_TEMP",
"update sensor 4 - BB_OUTLET_TEMP",
"update sensor 5 - TH5_REAR_LEFT",
"update sensor 6 - TH5_REAR_RIGHT",
"update sensor 1 - Chassis Fan 1 Front",
"update sensor 2 - Chassis Fan 1 Rear",
"update sensor 3 - Chassis Fan 2 Front",
"update sensor 4 - Chassis Fan 2 Rear",
"update sensor 5 - Chassis Fan 3 Front",
"update sensor 6 - Chassis Fan 3 Rear",
"update sensor 1 - PSU-Top-Right",
"update sensor 2 - PSU-Bottom_Right",
"update sensor 3 - PSU-Top-Left",
"update sensor 4 - PSU-Bottom_Left",
"restructuring tables",
"restructuring complete"]

psu_info_pattern=[
 "PSU 1",
   "Description: PSU-Top-Right",
   "State: Present",
   "Status: Running",
   "Model: TDPS2000LB A",
   "SN: JJLT2344000.*",
   "Type: (AC)|(DC)",
 "PSU 2",
   "Description: PSU-Bottom_Right",
   "State: Present",
   "Status: Running",
   "Model: TDPS2000LB A",
   "SN: JJLT2344000.*",
   "Type: (AC)|(DC)",
 "PSU 3",
   "Description: PSU-Top-Left",
   "State: Present",
   "Status: [Running|Unplugged]",
   
 "PSU 4",
   "Description: PSU-Bottom_Left",
   "State: Present",
   "Status: [Running|Unplugged]",
   ]

onie_eeprom_pattern=[
"Part Number          0x22  14 R4028-F9001-02",
"Serial Number        0x23   9 SN number",
"Manufacture Date     0x25  19 05/12/2022 00:00:01",
"Device Version       0x26   1 7",
"Label Revision       0x27   9 Moonstone",
"Platform Name        0x28  23 x86-64-cel-moonstone-r0",
"ONIE Version         0x29   5 "+onie_version,
"MAC Addresses        0x2A   2 384",
"Manufacturer         0x2B   9 Celestica",
"Country Code         0x2C   3 THA",
"Vendor Name          0x2D   9 Celestica",
"Service Tag          0x2F   2 LB",
"Vendor Extension     0xFD   3  0x2F 0xD4 0xFB",
"Product Name         0x21   9 "+exp_product_name,
"CRC-32               0xFE   4"]
 
thermal_info_pattern=["Thermal 1",
   "Description: 12V_ENTRY_LEFT",
   "Status: Functional",
   "Temperature: .*C",
 "Thermal 2",
   "Description: 12V_ENTRY_RIGHT",
   "Status: Functional",
   "Temperature: .*C",
 "Thermal 3",
   "Description: BB_BUSBAR_TEMP",
   "Status: Functional",
   "Temperature: .*C",
 "Thermal 4",
   "Description: BB_OUTLET_TEMP",
   "Status: Functional",
   "Temperature: .*C",
 "Thermal 5",
   "Description: TH5_REAR_LEFT",
   "Status: Functional",
   "Temperature: .*C",
 "Thermal 6",
   "Description: TH5_REAR_RIGHT",
   "Status: Functional",
   "Temperature: .*C",


]
