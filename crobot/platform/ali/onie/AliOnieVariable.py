###############################################################################
# LEGALESE:   "Copyright (C) 2019-2021, Celestica Corp. All rights reserved." #
#                                                                             #
# This source code is confidential, proprietary, and contains trade           #
# secrets that are the sole property of Celestica Corp.                       #
# Copy and/or distribution of this source code or disassembly or reverse      #
# engineering of the resultant object code are strictly forbidden without     #
# the written consent of Celestica Corp.                                      #
#                                                                             #
###############################################################################

diagos_install_msg = 'Installing SONiC in ONIE'
diagos_install_pass = 'Installed SONiC base image SONiC-OS successfully'
sonic_installer = 'onie-installer-x86_64-alibaba_as24-128d-cl-r0.bin'
onie_updater = 'onie-upda-x86_64-alibaba_as24-128d-cl-r0'  ## a name can't be found by onie discovery !
specific_file = '/home/admin/wwwwwwww'
test_mac1 = '00:E0:EC:FE:86:86'
ext4_fs_msg = "EXT4-fs \(sda3\): couldn't mount as ext3 due to feature incompatibilities\r\n"

onie_sysinfo = ['x86_64-alibaba_as24-128d-cl-r0']


TLV_Value_Test1 = { "Product Name"     : ["0x21", "XYZ1234A"],
                    "Part Number"      : ["0x22", "ABC1234567890"],
                    "Serial Number"    : ["0x23", "0123456789"],
                    "Base MAC Address" : ["0x24", "00:11:22:33:44:55"],
                    "Manufacture Date" : ["0x25", "01/31/2017 01:02:03"],
                    "Device Version"   : ["0x26", "03"],
                    "Label Revision"   : ["0x27", "R0C"],
                    "Platform Name"    : ["0x28", "powerpc-xyz1234a-r0"],
                    "MAC Addresses"    : ["0x2A", "4"],
                    "Manufacturer"     : ["0x2B", "Manufacturer"],
                    "Country Code"     : ["0x2C", "TW"],
                    "Vendor Name"      : ["0x2D", "Manufacturer"],
                    "Diag Version"     : ["0x2E", "1.1"],
                    "Vendor Extension" : ["0xFD", "0x01"],
                    "ONIE Version"     : ["0x29", "onie_version_1.0"],
                    "Service Tag"      : ["0x2F", "XYZ1234B"]
        }

TLV_Value_Test2 = { "Product Name"     : ["0x21", "AS24-128D-CL"],
                    "Part Number"      : ["0x22", "R3174-F9001-01"],
                    "Serial Number"    : ["0x23", "CLR3174FCL03090410014"],
                    "Base MAC Address" : ["0x24", "00:E0:EC:C9:B1:B4"],
                    "Manufacture Date" : ["0x25", "12/14/2018 03:01:52"],
                    "Device Version"   : ["0x26", "4"],
                    "Label Revision"   : ["0x27", "Migaloo"],
                    "Platform Name"    : ["0x28", "x86_64-alibaba_as24-128d-cl-r0"],
                    "MAC Addresses"    : ["0x2A", "2"],
                    "Manufacturer"     : ["0x2B", "Celestica"],
                    "Country Code"     : ["0x2C", "US"],
                    "Vendor Name"      : ["0x2D", "Alibaba"],
                    "Diag Version"     : ["0x2E", "0.1.1"],
                    "Vendor Extension" : ["0xFD", "0x0C"],
                    "ONIE Version"     : ["0x29", "2019.02.01.0.0.1"],
                    "Service Tag"      : ["0x2F", "XYZ1234C"]
        }

backup_sonic = 'sonic-broadcom_1.1.9_backup.bin'
backup_sonic_version = '1.1.9'

import os
devicename = os.environ.get("deviceName", "")
import logging
logging.info("devicename:{}".format(devicename))
if "shamu" in devicename.lower():
    sonic_installer = "onie-installer-x86_64-alibaba_as14-40d-cl-r0.bin"
    onie_sysinfo = ['x86_64-alibaba_as14-40d-cl-r0']
