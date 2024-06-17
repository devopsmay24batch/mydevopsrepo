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
#SEASTONE_ONL = SwImage.getSwImage("SEASTONE_ONL")
##### Variable file used for bmc.robot #####

SEASTONE = SwImage.getSwImage("SEASTONE_DIAG")
seastone_diag_version=SEASTONE.newVersion

SEASTONE = CommonLib.get_swinfo_dict("SEASTONE_ONL")

exp_bios_version = SEASTONE.get("bios_version").get("NEW_IMAGE","")

exp_onie_version = SEASTONE.get('onieVersionName')
exp_bmc_version = SEASTONE.get('bmcVersion')

exp_diag_version = SEASTONE.get('diagVersion')
#exp_fpga_version = '0x00010004'
exp_fpga_version = SEASTONE.get('fpgaVersion')
exp_come_cpld_version = SEASTONE.get('comeCpldVersion')
exp_bb_cpld_version = SEASTONE.get('bbCpldVersion')
exp_switch_cpld_version = SEASTONE.get('switchCpldVersion')
exp_onl_version = SEASTONE.get('onlVersion')
exp_onl_sysinfo = SEASTONE.get('onlSysinfo')
exp_sys_OID = SEASTONE.get('sysOID')
device_OID = SEASTONE.get('deviceOID')
onie_version = SEASTONE.get('onieVersion')
tlv_onie = {'0x29': onie_version}
exp_product_name = SEASTONE.get('productName')
PlatformEnv = {
    "SysInfo": {
        "ProductName": "DX030",
        "Label": "Seatone-II",
     },
    "PSU": {
        "Total": 2,
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
        "Total": 4,
        "FAN_Index": [1, 2, 3, 4],
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
                      {'Product Name': 'DS3000', 'Part Number': 'R4039-F9001-01', 'Serial Number': 'SN number', 'MAC': 'b4:db:91:d0:df:34',
                       'MAC Range': 134, 'Manufacturer': 'Celestica', 'Manufacture Date': '03/24/2021 16:12:05',
                       'Vendor': 'Celestica', 'Platform Name': 'x86_64-cel_ds3000-r0', 'Device Version': '6',
                       'Label Revision': 'DS3000', 'Country Code': 'THA', 'Diag Version': '2.0.0', 'Service Tag': 'LB',
                       'ONIE Version': '1.1.0' 
                       }
                  }
exp_ipmi_info = {'Builtin FRU Device (ID 0)':
                 {'Board Mfg Date': 'Wed Jul 24 00:00:00 2019', 'Board Mfg': 'Celestica', 'Board Product': 'Base Board', 'Board Serial': 'R4039-G0002-01xxxxxxxxxxxx',
                  'Board Part Number': 'R4039-G0002-01', 'Board Extra': 'DS3000-baseboard', 'Product Manufacturer': 'Celestica', 'Product Name': 'DS3000',
                  'Product Part Number': 'R4039-F9001-01', 'Product Serial': 'R4039B2F072815PS200003', 'Product Extra': '134'}}
portlist = ['01','22','31']
reboot_count = 2
#########################################
"""
Common Setting
"""
tftp_file_path = r"/var/lib/tftpboot/"
http_file_path = r"/usr/local/apache2/htdocs/"

tftp_server_ip = r"10.208.80.203"
http_server_ip = r"10.208.29.3:8080/SEASTONE"
device_type = "DUT"
pdu_port = 3
ONIE_UPDATE_MODE = 'update'
ONIE_RESCUE_MODE = 'rescue'
ONIE_INSTALL_MODE = 'installer'
ONIE_UNINSTALL_MODE = 'uninstall'

tftp_root_path = "/var/lib/tftpboot"
http_root_path = "/usr/local/apache2/htdocs/"
PROTOCOL_TFTP = 'tftp'
PROTOCOL_HTTP = 'http'

"""
Case Setting
"""
# Case: Static_IP+TFTP
static_ip = deviceM.managementIP
SEASTONE_ONIE = SwImage.getSwImage("SEASTONE_ONIE")
version=SEASTONE_ONIE.newVersion
ONIEimage=SEASTONE_ONIE.newImage

SEASTONE_ONL = SwImage.getSwImage("SEASTONE_ONL")
ONLversion=SEASTONE_ONL.newVersion
ONLimage=SEASTONE_ONL.newImage
RUN_TIME='900'

# Case: TC_005  Install_Sonic_via_Static_IP+TFTP
set_onie_static_ip = deviceM.managementIP  
diagos_install_msg = 'Installing SONiC in ONIE'
diagos_install_pass = 'Installed SONiC base image SONiC-OS successfully'
install_wait_time = 900
