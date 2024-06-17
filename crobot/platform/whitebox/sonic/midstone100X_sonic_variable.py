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
# Variable file used for midstone100X_sonic.robot
"""
NOTES:
    1.When testing, because Case: 9.7   SFP_Mode_Test
                                  9.23  Loopback_module_present_stress
                                  needs to fully plug the loop back
    2.because Case: 9.17 Transceivers_EEPROM_Info_Check need to plug loopback from the same manufacturer
"""

"""
Basic Settings
"""
CENTOS_MODE = 'sonic'
deviceType = "DUT"
PDU_Port = 4
tftp_file_path = r"/var/lib/tftpboot/"
http_file_path = r"/var/www/html/"
auto_server_ip = r"10.10.10.138"
diagos_install_msg = r'Installing SONiC in ONIE'
diagos_install_pass = r'Installed SONiC base image SONiC-OS successfully'
ext4_fs_msg = "EXT4-fs \(sda3\): couldn't mount as ext3 due to feature incompatibilities\r\n"

"""
Case Settings
"""
# Case: 9.4 Switch_board_CPLD_register_access
value_of_sys_bus_i2c_devices_10_0030_0033 = "0.9"
value_of_getreg = r"0x09"

# Case: 9.9 SONIC_Login_Check_Test
# # e.g ERROR: Class:0; Subclass:20000; Operation: 1008
keyword_can_ignore_when_sonic_start_list = ["Starting kdump-tools: no crashkernel= parameter in the kernel cmdline ... failed!"]

# Case: 9.10 SONIC_Version_Check
expected_platform = "midstone-100x"
expected_baud_rate = "115200.0"
keyword_error_in_show_version = ["dirty"]

# Case: 9.15 Hardware_Interface_Acess_Scan_Check
cpu_info_list = [{"cpu_MHz": [750, 2900]},  # Enter in the value range
                 {"cache_size": 6144},
                 {"cpu_cores": 4},
                 {"thread_number": 8},
                 {"model_name": "Intel(R) Xeon(R) CPU D-1627 @ 2.90GHz"}
                 ]
memtotal_G = 8

# Case: 9.16 TLV_EEPROM_Info_Read
tlv_info = {'Product Name': 'Midstone100X',
            'Serial Number': 'R3250B2F081510GD200021',
            'Base MAC Address': '0C:48:C6:97:FD:B8',
            'Manufacture Date': '03/30/2021 16:12:05',
            'Label Revision': 'Midstone100X',
            'Platform Name': 'x86_64-cel_midstone-100x-r0',
            'Manufacturer': 'Celestica',
            'Vendor Name': 'Celestica'}

# Case: 9.17 Transceivers_EEPROM_Info_Check
expected_present_num = 64
loopback_manufacturer_name = r"LEONI"
