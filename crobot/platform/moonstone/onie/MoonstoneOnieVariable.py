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
from SwImage import SwImage
try:
    from Device import Device
    import DeviceMgr
except Exception as err:
    log.cprint(str(err))
device = DeviceMgr.getDevice()

pc_info = DeviceMgr.getServerInfo('PC')
dev_info = DeviceMgr.getDevice()


"""
Common Setting
"""
tftp_file_path = r"/var/lib/tftpboot/"
http_file_path = r"/usr/local/apache2/htdocs/"

tftp_server_ip = r"10.208.84.251"
http_server_ip = r"10.208.84.251"
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

"""
Case Setting
"""
# Case: Static_IP+TFTP
devicename = os.environ.get("deviceName", "")
static_ip = DeviceMgr.getDevice(devicename).get('managementIP2')
MOONSTONE = SwImage.getSwImage("MOONSTONE_ONIE")
version=MOONSTONE.newVersion
ONIEimage=MOONSTONE.newImage

MOONSTONE_ONL = SwImage.getSwImage("MOONSTONE_ONL")
ONLversion=MOONSTONE_ONL.newVersion
ONLimage=MOONSTONE_ONL.newImage

# Case: ONIE_Rescue_Mode
ONIE_SYSEEPROM_CMD = "onie-syseeprom"
DICT_tlv_value = {
    "Part Number": ["0x22", "R4028-F9001-01"],
    "Serial Number": ["0x23", "SN number"],
    "Base MAC Address": ["0x24", "B4:DB:91:D0:DF:34"],
    "Manufacture Date": ["0x25", "03/24/2021 16:12:05"],
    "Device Version": ["0x26", "6"],
    "Label Revision": ["0x27", "DS5000"],
    "Platform Name": ["0x28", "x86_64-cel_ds3000-r0"],
    "ONIE Version": ["0x29", "1.1.0"],
    "MAC Addresses": ["0x2A", "134"],
    "Manufacturer": ["0x2B", "Celestica"],
    "Country Code": ["0x2C", "THA"],
    "Vendor Name": ["0x2D", "Celestica"],
    "Diag Version": ["0x2E", "1.1.0"],
    "Service Tag": ["0x2F", "LB"],
    "Vendor Extension": ["0xFD", " 0x2F 0xD4 0xBF"],
    "Product Name": ["0x21", "moonstone"],
    "CRC-32": ["0xFE", "0x51BDEBEC"]
    }

