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

"""
Common Setting
"""
tftp_file_path = r"/var/lib/tftpboot/"
http_file_path = r"/var/www/html/"
auto_server_ip = r"10.10.10.138"
device_type = "DUT"
pdu_port = 3
ONIE_UPDATE_MODE = 'ONIE_UPDATE_MODE'
ONIE_RESCUE_MODE = 'ONIE_RESCUE_MODE'
ONIE_INSTALL_MODE = 'ONIE_INSTALL_MODE'
BOOT_MODE_DIAGOS = 'DIAGOS'
tftp_root_path = "/var/lib/tftpboot"
http_root_path = "/var/www/html"
BOOT_MODE_OPENBMC = 'OPENBMC'
KEY_UP = '\x1b[A'
KEY_DOWN = '\x1b[B'
KEY_CTRL_C = '\x03'
KEY_CTRL_A = '\x01'
PROTOCOL_TFTP = 'tftp'
PROTOCOL_HTTP = 'http'

"""
Case Setting
"""
# Case: TC_005  Install_Sonic_via_Static_IP+TFTP
set_onie_static_ip = r"10.10.10.111"
diagos_install_msg = 'Installing SONiC in ONIE'
diagos_install_pass = 'Installed SONiC base image SONiC-OS successfully'

# Case: Update_MAC_Address_in_ONIE
test_mac1 = '00:E0:EC:FE:86:86'

ext4_fs_msg = "EXT4-fs \(sda3\): couldn't mount as ext3 due to feature incompatibilities\r\n"

# Case: Stress_install_uninstall_sonic
dut_snoic_file_path = r"/"
loop_num = 1

# Case: ONIE_Rescue_Mode
ONIE_SYSEEPROM_CMD = "onie-syseeprom"
error_tlv_value = {
    "Product Name": ["0x21", "Midstone 100x"],
    "Part Number": ["0x22", "R3250-F9003-02"],
    "Serial Number": ["0x23", "0C:48:C6:97:F9:A1"],
    "Base MAC Address": ["0x24", "0C:48:C6:97:F9:A1"],
    "Manufacture Date": ["0x25", "04/21/2021 15:26:11"],
    "Device Version": ["0x26", "6"],
    "Label Revision": ["0x27", "Midstone 100x"],
    "Platform Name": ["0x28", "x86_64-cel_midstone-100x-r1"],
    "MAC Addresses": ["0x2A", "261"],
    "Manufacturer": ["0x2B", "Celesticc"],
    "Country Code": ["0x2C", "THa"],
    "Vendor Name": ["0x2D", "CelesticA"],
    "Diag Version": ["0x2E", "1.0.1"],
    "Service Tag": ["0x2F", "Lb"],
    "Vendor Extension": ["0xFD", "0x2F 0xD4 0xBf"],
    "ONIE Version": ["0x29", "2019.02.01.1.0.1"],
    "CRC-32": ["0xFE", "0x992BA201"],
}
DICT__right_tlv_value = {
    "Product Name": ["0x21", "Midstone 100X"],
    "Part Number": ["0x22", "R3250-F9003-01"],
    "Serial Number": ["0x23", "0C:48:C6:97:F9:A0"],
    "Base MAC Address": ["0x24", "0C:48:C6:97:F9:A0"],
    "Manufacture Date": ["0x25", "04/21/2021 15:26:12"],
    "Device Version": ["0x26", "5"],
    "Label Revision": ["0x27", "Midstone 100X"],
    "Platform Name": ["0x28", "x86_64-cel_midstone-100x-r0"],
    "MAC Addresses": ["0x2A", "262"],
    "Manufacturer": ["0x2B", "Celestica"],
    "Country Code": ["0x2C", "THA"],
    "Vendor Name": ["0x2D", "Celestica"],
    "Diag Version": ["0x2E", "1.0.0"],
    "Service Tag": ["0x2F", "LB"],
    "Vendor Extension": ["0xFD", "0x2F 0xD4 0xBF"],
    "ONIE Version": ["0x29", "2019.02.01.1.0.0"],
    "CRC-32": ["0xFE", "0x992BA209"]

}