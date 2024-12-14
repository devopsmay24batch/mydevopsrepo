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
import os
import logging
from SwImage import SwImage
import CommonLib
devicename = os.environ.get("deviceName", "").lower()
logging.info("devicename:{}".format(devicename))

diagos_login_info = [r'Linux sonic 4.19.0-12-2-amd64 #1 SMP Debian 4.19.152-1 (2020-10-18) x86_64', \
                     r'You are on', r'-- Software for Open Networking in the Cloud --', \
                     r'Unauthorized access and/or use are prohibited', 'All access and/or use are subject to monitoring', \
                     r'Help:    http://azure.github.io/SONiC/']

## TC08 show version
show_version_cmd = 'show version'
show_boot_cmd = 'show boot'
uname_cmd = 'uname -v'
uname_value = '#1 SMP Debian 4.19.152-1 (2020-10-18)'
cls_diag_path = 'cd /usr/local/cls_diag/bin/'
sys_info_test_cmd = './cel-sysinfo-test -a'
eeprom_cmd = './cel-eeprom-test -r -d 3 -t tlv'

## TC09 boot info test case
coreboot_release_date = '2022-01-10'

##TC10 dependent sw version
expect_diag_version = CommonLib.get_swinfo_dict("BRIXIA_SONIC")
expect_diag_version = expect_diag_version.get("DIAG").get("newVersion", "")
diag_SW = "R3152-M0025-01_Diag-brixia.v"+expect_diag_version+".deb"

sdk_version = CommonLib.get_swinfo_dict("BRIXIA_SONIC")
sdk_version = sdk_version.get("SDK").get("newVersion", "")
sdk_SW = 'R3152-J0003-01-SDK_brixia.v'+sdk_version+'_sonic202012.deb'

#diag_SW = 'R3152-M0025-01_Diag-brixia.v0.1.4.deb'
#sdk_SW = 'R3152-m0165-01-SDK_brixia.v0.2.0_sonic202012.deb'
bios_cmd = 'dmidecode -t bios'
libyaml = 'libyaml-0-2_0.2.1-1_amd64.deb'
libyaml_output = ["\\/\\.",
        "/usr",
        "/usr/lib",
        "/usr/lib/x86_64-linux-gnu",
        "/usr/lib/x86_64-linux-gnu/libyaml-0.so.2.0.5",
        "/usr/share",
        "/usr/share/doc",
        "/usr/share/doc/libyaml-0-2",
        "/usr/share/doc/libyaml-0-2/changelog.Debian.gz",
        "/usr/share/doc/libyaml-0-2/copyright",
        "/usr/lib/x86_64-linux-gnu/libyaml-0.so.2"]
autoload_output=['mknod: /dev/linux-user-bde: File exists',
        'mknod: /dev/linux-kernel-bde: File exists']
bcm_sdk_version='sdk-6.5.26'
come_cpld_version = ['0x18']
mmc_major_version = ['0x00']
mmc_minor_version = ['0x0e']
mmc_month_version = ['0x01']
mmc_date_version = ['0x12']
fpga_major_version = ['3']
fpga_minor_version = ['10']

##TC12 cpld/fpga register access test
tool_path= 'cd /usr/local/cls_diag/tools/'

##TC14 HW interface check
platform = 'x86_64-cel_brixia-r0'
HwSKU = 'Brixia'
ASIC = 'broadcom'
ASIC_Count = '1'

cpu_info ="Intel(R) Xeon(R) CPU D-1649N @ 2.30GHz"

pcie_log = ['01:00.0 Ethernet controller: Broadcom Limited Device b996.*',
        ' System peripheral: Google, Inc. Device 0065']

th4_pci = '01:00.0 Ethernet controller: Broadcom Limited Device b996'
th4_pci_speed_width = 'Speed 8GT/s, Width x4'

gfpga_pci = ' System peripheral: Google, Inc. Device 0065'
gfpga_pci_speed_width = 'Speed 2.5GT/s, Width x1'

ssd = '/dev/sda'
msd = '/dev/sd'

i2c_l_pattern = ["i2c-3   smbus           i2c-0-mux \\(chan_id 1\\)                   SMBus adapter",
        "i2c-10102       i2c             i2c-10100-mux \\(chan_id 1\\)               I2C adapter",
        "i2c-10130       i2c             i2c-10100-mux \\(chan_id 29\\)              I2C adapter",
        "i2c-20  i2c             i2c-11-mux \\(chan_id 0\\)                  I2C adapter",
        "i2c-10120       i2c             i2c-10100-mux \\(chan_id 19\\)              I2C adapter",
        "i2c-10  i2c             i2c-ocores                              I2C adapter",
        "i2c-10110       i2c             i2c-10100-mux \\(chan_id 9\\)               I2C adapter",
        "i2c-1   i2c             i2c-ocores                              I2C adapter",
        "i2c-10100       i2c             GFPGA adapter                           I2C adapter",
        "i2c-29  smbus           iMC socket 0 for channel pair 2-3       SMBus adapter",
        "i2c-10129       i2c             i2c-10100-mux \\(chan_id 28\\)              I2C adapter",
        "i2c-19  i2c             i2c-10-mux \\(chan_id 7\\)                  I2C adapter",
        "i2c-10119       i2c             i2c-10100-mux \\(chan_id 18\\)              I2C adapter",
        "i2c-10109       i2c             i2c-10100-mux \\(chan_id 8\\)               I2C adapter",
        "i2c-27  i2c             i2c-11-mux \\(chan_id 7\\)                  I2C adapter",
        "i2c-10127       i2c             i2c-10100-mux \\(chan_id 26\\)              I2C adapter",
        "i2c-10004       i2c             i2c-10000-mux \\(chan_id 3\\)               I2C adapter",
        "i2c-17  i2c             i2c-10-mux \\(chan_id 5\\)                  I2C adapter",
        "i2c-10117       i2c             i2c-10100-mux \\(chan_id 16\\)              I2C adapter",
        "i2c-8   smbus           i2c-0-mux \\(chan_id 6\\)                   SMBus adapter",
        "i2c-10107       i2c             i2c-10100-mux \\(chan_id 6\\)               I2C adapter",
        "i2c-25  i2c             i2c-11-mux \\(chan_id 5\\)                  I2C adapter",
        "i2c-10125       i2c             i2c-10100-mux \\(chan_id 24\\)              I2C adapter",
        "i2c-10002       i2c             i2c-10000-mux \\(chan_id 1\\)               I2C adapter",
        "i2c-15  i2c             i2c-10-mux \\(chan_id 3\\)                  I2C adapter",
        "i2c-10115       i2c             i2c-10100-mux \\(chan_id 14\\)              I2C adapter",
        "i2c-6   smbus           i2c-0-mux \\(chan_id 4\\)                   SMBus adapter",
        "i2c-10105       i2c             i2c-10100-mux \\(chan_id 4\\)               I2C adapter",
        "i2c-10133       i2c             i2c-10100-mux \\(chan_id 32\\)              I2C adapter",
        "i2c-23  i2c             i2c-11-mux \\(chan_id 3\\)                  I2C adapter",
        "i2c-10123       i2c             i2c-10100-mux \\(chan_id 22\\)              I2C adapter",
        "i2c-10000       i2c             GFPGA adapter                           I2C adapter",
        "i2c-13  i2c             i2c-10-mux \\(chan_id 1\\)                  I2C adapter",
        "i2c-10113       i2c             i2c-10100-mux \\(chan_id 12\\)              I2C adapter",
        "i2c-4   smbus           i2c-0-mux \\(chan_id 2\\)                   SMBus adapter",
        "i2c-10103       i2c             i2c-10100-mux \\(chan_id 2\\)               I2C adapter",
        "i2c-10131       i2c             i2c-10100-mux \\(chan_id 30\\)              I2C adapter",
        "i2c-21  i2c             i2c-11-mux \\(chan_id 1\\)                  I2C adapter",
        "i2c-10121       i2c             i2c-10100-mux \\(chan_id 20\\)              I2C adapter",
        "i2c-11  i2c             i2c-ocores                              I2C adapter",
        "i2c-10111       i2c             i2c-10100-mux \\(chan_id 10\\)              I2C adapter",
        "i2c-2   smbus           i2c-0-mux \\(chan_id 0\\)                   SMBus adapter",
        "i2c-10101       i2c             i2c-10100-mux \\(chan_id 0\\)               I2C adapter",
        "i2c-0   smbus           SMBus I801 adapter at ffe0              SMBus adapter",
        "i2c-28  smbus           iMC socket 0 for channel pair 0-1       SMBus adapter",
        "i2c-10128       i2c             i2c-10100-mux \\(chan_id 27\\)              I2C adapter",
        "i2c-18  i2c             i2c-10-mux \\(chan_id 6\\)                  I2C adapter",
        "i2c-10118       i2c             i2c-10100-mux \\(chan_id 17\\)              I2C adapter",
        "i2c-9   smbus           i2c-0-mux \\(chan_id 7\\)                   SMBus adapter",
        "i2c-10108       i2c             i2c-10100-mux \\(chan_id 7\\)               I2C adapter",
        "i2c-26  i2c             i2c-11-mux \\(chan_id 6\\)                  I2C adapter",
        "i2c-10126       i2c             i2c-10100-mux \\(chan_id 25\\)              I2C adapter",
        "i2c-10003       i2c             i2c-10000-mux \\(chan_id 2\\)               I2C adapter",
        "i2c-16  i2c             i2c-10-mux \\(chan_id 4\\)                  I2C adapter",
        "i2c-10116       i2c             i2c-10100-mux \\(chan_id 15\\)              I2C adapter",
        "i2c-7   smbus           i2c-0-mux \\(chan_id 5\\)                   SMBus adapter",
        "i2c-10106       i2c             i2c-10100-mux \\(chan_id 5\\)               I2C adapter",
        "i2c-10134       i2c             i2c-10100-mux \\(chan_id 33\\)              I2C adapter",
        "i2c-24  i2c             i2c-11-mux \\(chan_id 4\\)                  I2C adapter",
        "i2c-10124       i2c             i2c-10100-mux \\(chan_id 23\\)              I2C adapter",
        "i2c-10001       i2c             i2c-10000-mux \\(chan_id 0\\)               I2C adapter",
        "i2c-14  i2c             i2c-10-mux \\(chan_id 2\\)                  I2C adapter",
        "i2c-10114       i2c             i2c-10100-mux \\(chan_id 13\\)              I2C adapter",
        "i2c-5   smbus           i2c-0-mux \\(chan_id 3\\)                   SMBus adapter",
        "i2c-10104       i2c             i2c-10100-mux \\(chan_id 3\\)               I2C adapter",
        "i2c-10132       i2c             i2c-10100-mux \\(chan_id 31\\)              I2C adapter",
        "i2c-22  i2c             i2c-11-mux \\(chan_id 2\\)                  I2C adapter",
        "i2c-10122       i2c             i2c-10100-mux \\(chan_id 21\\)              I2C adapter",
        "i2c-12  i2c             i2c-10-mux \\(chan_id 0\\)                  I2C adapter",
        "i2c-10112       i2c             i2c-10100-mux \\(chan_id 11\\)              I2C adapter"]

i2c_y0_pattern = ["0  1  2  3  4  5  6  7  8  9  a  b  c  d  e  f",
        "00:          -- -- -- -- -- 08 -- -- -- -- -- -- --",
        "10: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --",
        "20: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --",
        "30: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --",
        "40: -- -- -- -- 44 -- -- -- 48 -- -- -- -- -- -- --",
        "50: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --",
        "60: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --",
        "70: -- -- UU -- -- -- -- --"]

i2c_y1_pattern = ["0  1  2  3  4  5  6  7  8  9  a  b  c  d  e  f",
        "00:          -- -- -- -- -- -- -- -- -- -- -- -- --",
        "10: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --",
        "20: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --",
        "30: -- -- -- -- UU -- -- -- -- -- -- -- -- -- -- --",
        "40: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --",
        "50: UU UU -- -- -- -- -- -- 58 -- -- -- -- -- -- --",
        "60: -- -- -- -- UU -- UU -- -- -- -- -- -- -- -- --",
        "70: -- -- -- -- -- -- -- --"]

##TC_15 tlv eeprom info
file1 = 'eeprom_test_01.sh'
file2 = 'eeprom_test_02.sh'
file3 = 'eeprom_test_03.sh'

f1_come1_pattern = ['Read COMe EEPROM info:',
        'subassy_pn: ABC1234567-01',
        'mac_count: 2',
        'mfg_date: 0x2103',
        'card_type: 0x00000054',
        'psu_type: DC',
        'mac_address: 00:E0:EC:00:00:00',
        'subassy_sn: 1618123478901',
        'pn: 1075455-01',
        'sn: TMBCTH194201433',
        'hw_revision: 0x01']

f1_come2_pattern = ['Read COMe:0x51 EEPROM info:',
        'subassy_pn: DUMMY123456',
        'mac_count: 65535',
        'mfg_date: 0x1234',
        'card_type: 0x11223344',
        'psu_type: DC',
        'mac_address: AA:BB:CC:DD:EE:FF',
        'subassy_sn: DUMMY123456789X',
        'pn: DUMMY123456',
        'sn: DUMMY123456789X',
        'hw_revision: 0xFF']

f1_baseboard_pattern = ['Read Baseboard EEPROM info:',
        'board_sn: ABCDEFG123456789',
        'mac_count: 262',
        'mfg_date: 0x2103',
        'card_type: 0x00000060',
        'psu_type: DC',
        'margin_low:  0x00 0x1F 0x7F 0x7F 0x7F 0x7F 0x7F 0x00',
        'mac_address: 00:E0:EC:00:00:02',
        'margin_off:  0x00 0x1F 0x7F 0x7F 0x7F 0x7F 0x7F 0x00',
        'pn: 1075455-02',
        'product_name: BX',
        'margin_high:  0x00 0x1F 0x7F 0x7F 0x7F 0x7F 0x7F 0x00',
        'sn: TMBCTH194201434',
        'board_pn: 1098633-01',
        'hw_revision: 0x01']

f1_switchboard_pattern = ['Read Switchboard EEPROM info:',
        'subassy_pn: ABC1234567-01',
        'mfg_date: 0x2103',
        'card_type: 0x00000061',
        'psu_type: DC',
        'subassy_sn: 1618123478901',
        'pn: 109661-01',
        'sn: TMBCTH194201436',
        'hw_revision: 0x01']

f1_fan1_pattern = ['Read fan-1 EEPROM info:',
        'fan_maxspeed: 65555',
        'mfg_date: 0x2103',
        'card_type: 0x00000064',
        'psu_type: DC',
        'fan_pn: R80H54BS2PC-07A25',
        'pn: 1098638-01',
        'sn: TMBCTH194201438',
        'hw_revision: 0x01']

f1_fan2_pattern = ['Read fan-2 EEPROM info:',
        'fan_maxspeed: 65555',
        'mfg_date: 0x2103',
        'card_type: 0x00000064',
        'psu_type: DC',
        'fan_pn: R80H54BS2PC-07A25',
        'pn: 1098638-01',
        'sn: TMBCTH194201439',
        'hw_revision: 0x01']

f1_fan3_pattern = ['Read fan-3 EEPROM info:',
        'fan_maxspeed: 65555',
        'mfg_date: 0x2103',
        'card_type: 0x00000064',
        'psu_type: DC',
        'fan_pn: R80H54BS2PC-07A25',
        'pn: 1098638-01',
        'sn: TMBCTH194201440',
        'hw_revision: 0x01']




f2_come1_pattern = ['Read COMe EEPROM info:',
        'subassy_pn: subassy_pn',
        'mac_count: 3',
        'mfg_date: 0x1122',
        'card_type: 0x00000054',
        'psu_type: DC',
        'mac_address: 00:E0:EC:11:11:11',
        'subassy_sn: subassy_sn',
        'pn: pn',
        'sn: sn',
        'hw_revision: 0x05']

f2_come2_pattern = ['Read COMe:0x51 EEPROM info:',
        'subassy_pn: subassy_pn2',
        'mac_count: 22',
        'mfg_date: 0x4321',
        'card_type: 0x00000054',
        'psu_type: DC',
        'mac_address: 00:E0:EC:22:22:22',
        'subassy_sn: subassy_sn2',
        'pn: pn2',
        'sn: sn2',
        'hw_revision: 0x22']

f2_baseboard_pattern = ['Read Baseboard EEPROM info:',
        'board_sn: board_sn',
        'mac_count: 2',
        'mfg_date: 0x0101',
        'card_type: 0x00000060',
        'psu_type: DC',
        'margin_low:  0x00 0x1F 0x7F 0x7F 0x7F 0x7F 0x7F 0x00',
        'mac_address: 00:E0:EC:BB:BB:BB',
        'margin_off:  0x00 0x1F 0x7F 0x7F 0x7F 0x7F 0x7F 0x00',
        'pn: pn',
        'product_name: BX',
        'margin_high:  0x00 0x1F 0x7F 0x7F 0x7F 0x7F 0x7F 0x00',
        'sn: sn',
        'board_pn: board_pn',
        'hw_revision: 0x06']

f2_switchboard_pattern = ['Read Switchboard EEPROM info:',
        'subassy_pn: subassy_pn',
        'mfg_date: 0x1234',
        'card_type: 0x00000061',
        'psu_type: DC',
        'subassy_sn: subassy_sn',
        'pn: pn',
        'sn: sn',
        'hw_revision: 0x07']

f2_fan1_pattern = ['Read fan-1 EEPROM info:',
        'fan_maxspeed: 99999',
        'mfg_date: 0x1122',
        'card_type: 0x00000064',
        'psu_type: DC',
        'fan_pn: fan_pn',
        'pn: pn',
        'sn: sn',
        'hw_revision: 0x09']

f2_fan2_pattern = ['Read fan-2 EEPROM info:',
        'fan_maxspeed: 99999',
        'mfg_date: 0x1122',
        'card_type: 0x00000064',
        'psu_type: DC',
        'fan_pn: fan_pn',
        'pn: pn',
        'sn: sn',
        'hw_revision: 0x09']

f2_fan3_pattern = ['Read fan-3 EEPROM info:',
        'fan_maxspeed: 99999',
        'mfg_date: 0x1122',
        'card_type: 0x00000064',
        'psu_type: DC',
        'fan_pn: fan_pn',
        'pn: pn',
        'sn: sn',
        'hw_revision: 0x09']


f2_fan4_pattern = ['Read fan-4 EEPROM info:',
        'fan_maxspeed: 99999',
        'mfg_date: 0x1122',
        'card_type: 0x00000064',
        'psu_type: DC',
        'fan_pn: fan_pn',
        'pn: pn',
        'sn: sn',
        'hw_revision: 0x09']
		
		

f3_come1_pattern = ['Read COMe EEPROM info:',
        'subassy_pn: COMe_Board',
        'mac_count: 2',
        'mfg_date: 0x1526',
        'card_type: 0x00000054',
        'psu_type: DC',
        'mac_address: 00:1A:11:16:76:3E',
        'subassy_sn: MSHCTH220100404',
        'pn: 1075455-04-04',
        'sn: MSHCTH220100404',
        'hw_revision: 0x01']

f3_come2_pattern = ['Read COMe:0x51 EEPROM info:',
        'subassy_pn: COMe2_Board',
        'mac_count: 4',
        'mfg_date: 0x1234',
        'card_type: 0x00000054',
        'psu_type: DC',
        'mac_address: 00:1A:11:16:76:41',
        'subassy_sn: COMe2_SN',
        'pn: COMe_PN_2',
        'sn: COMe_SN_2',
        'hw_revision: 0x02']

f3_baseboard_pattern = ['Read Baseboard EEPROM info:',
        'board_sn: BBBCTH215200015',
        'mac_count: 262',
        'mfg_date: 0x1529',
        'card_type: 0x00000060',
        'psu_type: DC',
        'margin_low:  0x00 0x1F 0x7F 0x7F 0x7F 0x7F 0x7F 0x0',
        'mac_address: E4:5E:1B:69:77:BA',
        'margin_off:  0x00 0x1F 0x7F 0x7F 0x7F 0x7F 0x7F 0x00',
        'pn: 1098800-02-08',
        'product_name: BX',
        'margin_high:  0x00 0x1F 0x7F 0x7F 0x7F 0x7F 0x7F 0x00',
        'sn: BBBCTH215200015',
        'board_pn: 1098800-02',
        'hw_revision: 0x05']

f3_switchboard_pattern = ['Read Switchboard EEPROM info:',
        'subassy_pn: ISK1096610-06',
        'mfg_date: 0x1527',
        'card_type: 0x00000061',
        'psu_type: DC',
        'subassy_sn: 3321025200702',
        'pn: 1096610-07',
        'sn: BTBCTH220100008',
        'hw_revision: 0x02']

f3_fan1_pattern = ['Read fan-1 EEPROM info:',
         'fan_maxspeed: 14800',
        'mfg_date: 0x1527',
        'card_type: 0x00000064',
        'psu_type: DC',
        'fan_pn: R80H54BS2PC-07A25',
        'pn: 1098828-02',
        'sn: BFFCTH220200152',
        'hw_revision: 0x01']

f3_fan2_pattern = ['Read fan-2 EEPROM info:',
        'fan_maxspeed: 14800',
        'mfg_date: 0x1527',
        'card_type: 0x00000064',
        'psu_type: DC',
        'fan_pn: R80H54BS2PC-07A25',
        'pn: 1098828-02',
        'sn: BFFCTH220200182',
        'hw_revision: 0x01']

f3_fan3_pattern = ['Read fan-3 EEPROM info:',
        'fan_maxspeed: 14800',
        'mfg_date: 0x1527',
        'card_type: 0x00000064',
        'psu_type: DC',
        'fan_pn: R80H54BS2PC-07A25',
        'pn: 1098828-02',
        'sn: BFFCTH220200181',
        'hw_revision: 0x01']


f3_fan4_pattern = ['Read fan-4 EEPROM info:',
        'fan_maxspeed: 14800',
        'mfg_date: 0x1527',
        'card_type: 0x00000064',
        'psu_type: DC',
        'fan_pn: R80H54BS2PC-07A25',
        'pn: 1098828-02',
        'sn: BFFCTH220200184',
        'hw_revision: 0x01']

		


#TC16_OSFP SFP + epprom check
osfp_info =[
        'Vendor:Amphenol',
        'PN:NLMAME-G101',
        'SN:.*',
        'Temp:.* C',]


#TC_17 temp sensor check
coretemp = 83
tmp05_max = 60
i2cool_max = 60

#TC_18 voltage sensor check
COMe = 'ucd9090-i2c-1-34'
COMe_U51 = 'sn1701022-i2c-1-64'
COMe_U59 = 'sn1701022-i2c-1-66'
Baseboard = 'adm1272-i2c-.*-10'
PowerBrick_U33 = 'Q50SN12072-i2c-.*-61'
PowerBrick_U32 = 'Q50SN12072-i2c-.*-60'
UCD9090 = 'ucd9090-i2c-.*-41'
#COMe
XP3R3V =  3.63
XP1R5V =  1.65
XP1R3V =  1.43
XP12R0V = 13.20
XP1R2V =  1.32
XP1R7V =  1.87
XP1R05V =  1.16
XP2R5V =  2.75
XP1R82V =  2.00
XP1R05V_VCCSCSUS =  1.16
#COMe U51
u51_XP12R0V = 13.20
u51_XP1R82V = 2.00
u51_XP1R2V = 1.32
u51_Power_XP1R82V = 25.50
u51_Power_XP1R2V = 26.80
u51_Current_XP1R82V = 16.00
u51_Current_XP1R2V =14.00
#Come U59
u59_XP12R0V = 13.20
u59_XP1R05V_VCCSCSUS = 1.15
u59_XP1R05V = 1.15
u59_Power_XP1R05V_VCCSCSUS = 16.80
u59_Power_XP1R05V = 14.70
u59_Current_XP1R05V_VCCSCSUS = 16.00
u59_Current_XP1R05V = 14.00
#baseboard
amd_XP48R0V_IN = 60.00
amd_XP48R0V_SWAP = 60.00
amd_Power_XP48R0V_SWAP = 2280
amd_Current_XP48R0V_SWAP = 55
#powerbrick u33
pbU33_XP48R0V_EMC_SW = 60.00
pbU33_XP12R0V_SW = 13.20
pbU33_Current_XP12R0V_SW = 72.00
#powerbrick u32
u32_XP48R0V_EMC_BB = 60.00
u32_XP12R0V_BB = 13.20
u32_Current_XP12R0V_BB = 72.00
#ucd9090 baseboard
ucd_XP12R0V_SW = 13.20
ucd_XP12R0V_BB = 13.20
ucd_XP12R0V_COME = 13.20
ucd_XP5R0V_COME = 5.50
ucd_XP3R3V = 3.63
ucd_XP3R3V_STBY = 3.63
ucd_XP3R3V_SSD = 3.63

#amd1266-i2c-10001-44
VDD_12R0 = 13.20
VDD_12R0_OSFP = 13.20
VDD_5R0 = 5.50
VDD_3R3_AUX = 3.63
VDD_3R3_A = 3.63
VDD_3R3_B = 3.63
ADD_AVS = 0.99
AVDD_1R8 = 1.98
VDD_1R8 = 1.98
VDD_1R2 = 1.32
AVDD_0R9_A = 0.99
AVDD_0R9_B = 0.99
AVDD_0R75_A = 0.825
VDD_1R8_OSC1 = 1.98
VDD_1R8_OSC2 = 1.98
AVDD_0R75_B = 0.825

sensor_state = 'Specified sensor\\(s\\) not found!'

#switchboard sensors
raa_VDD_12R0_TH_FILT = 13.20
raa_VDD_AVS = 0.99
raa_Power_VDD_AVS = 500.00
raa_Current_VDD_AVS = 560.0

isl1_VDD_12R0_OSFP_A_FILT = 13.20
isl1_VDD_12R0_TH_FILT = 13.20
isl1_VDD_3R3_A = 3.63
isl1_AVDD_0R9_A = 0.99
isl1_Power_VDD_3R3_A = 400.00
isl1_Power_AVDD_0R9_A = 90.00
isl1_Current_VDD_3R3_A = 120.00
isl1_Current_AVDD_0R9_A = 95.00

isl2_VDD_12R0_OSFP_B_FILT = 13.20
isl2_VDD_12R0_TH_FILT = 13.20
isl2_VDD_3R3_B = 3.63
isl2_AVDD_0R9_B = 0.99
isl2_Power_VDD_3R3_B = 400.00
isl2_Power_AVDD_0R9_B = 90.00
isl2_Current_VDD_3R3_B = 120.00
isl2_Current_AVDD_0R9_B = 120.00

u51_VDD_12R0 = 13.20
u51_AVDD_0R75_A = 0.90
u51_Current_AVDD_0R75_A = 12.00

u199_VDD_12R0 = 13.20
u199_AVDD_0R75_B = 0.90
u199_Current_AVDD_0R75_B = 12.00

u53_VDD_12R0 = 13.20
u53_VDD_1R2 = 1.32
u53_Current_VDD_1R2 = 5.00

u54_VDD_12R0 = 13.20
u54_VDD_1R8 = 1.98
u54_Current_VDD_1R8 = 5.00

u55_VDD_12R0 = 13.20
u55_AVDD_1R8 = 1.98
u55_Current_AVDD_1R8 = 5.00

#TC_20 Fan speed control test
half_speed = 7000
full_speed = 14000
quat_speed = 3000

#TC_23 EDT service Check
#start
wdt_enabled = '1'
wdt_period = '24000'
wdt_expired = '0'
wdt_sw_en = '1'
wdt_sw = '1'
#stop
enabled = '0'
period = '600000'
expired = '0'
sw_en = '1'
sw = '0'

#TC_31 I2c stress test
cmd1 = ".* /sys/bus/i2c/devices/i2c-0 -> ../../../devices/pci0000:00/0000:00:1f.3/i2c-0"
cmd2 = i2c_y0_pattern
cmd3 = ['.* channel-0 -> ../i2c-2',
        '.* channel-1 -> ../i2c-3',
        '.* channel-2 -> ../i2c-4',
        '.* channel-3 -> ../i2c-5',
        '.* channel-4 -> ../i2c-6',
        '.* channel-5 -> ../i2c-7',
        '.* channel-6 -> ../i2c-8',
        '.* channel-7 -> ../i2c-9',
        '.* driver -> ../../../../../bus/i2c/drivers/pca954x',
        '.* idle_state',
        '.* modalias',
        '.* name',
        '.* power',
        '.* subsystem -> ../../../../../bus/i2c',
        '.* uevent']
cmd4 = '.* /sys/bus/i2c/devices/i2c-1 -> ../../../devices/platform/ocores-i2c.2.auto/i2c-1'
cmd5 = i2c_y1_pattern
cmd6 = ['/sys/devices/platform/mmcpld/ocores-i2c.4.auto',
        '/sys/devices/platform/mmcpld/ocores-i2c.5.auto']
cmd7 = ['/sys/devices/platform/mmcpld/mmc_reg.3.auto']
cmd8 = ['/sys/devices/platform/mmcpld/tmp05.10.auto',
        '/sys/devices/platform/mmcpld/tmp05.11.auto',
        '/sys/devices/platform/mmcpld/tmp05.12.auto',
        '/sys/devices/platform/mmcpld/tmp05.13.auto',
        '/sys/devices/platform/mmcpld/tmp05.7.auto',
        '/sys/devices/platform/mmcpld/tmp05.8.auto',
        '/sys/devices/platform/mmcpld/tmp05.9.auto']
cmd9 = ['/sys/devices/platform/mmcpld/fantray.6.auto/hwmon/hwmon10',
        '/sys/devices/platform/mmcpld/fantray.6.auto/hwmon/hwmon11',
        '/sys/devices/platform/mmcpld/fantray.6.auto/hwmon/hwmon8',
        '/sys/devices/platform/mmcpld/fantray.6.auto/hwmon/hwmon9']
cmd10 =['fan3',
        'fan4',
        'fan1',
        'fan2']
cmd11 = ['channel-0',
        'channel-1',
        'channel-2',
        'channel-3',
        'i2c-10000',
        'power',
        'subsystem',
        'uevent']
cmd12 = ['channel-0',
        'channel-1',
        'channel-10',
        'channel-11',
        'channel-12',
        'channel-13',
        'channel-14',
        'channel-15',
        'channel-16',
        'channel-17',
        'channel-18',
        'channel-19',
        'channel-2',
        'channel-20',
        'channel-21',
        'channel-22',
        'channel-23',
        'channel-24',
        'channel-25',
        'channel-26',
        'channel-27',
        'channel-28',
        'channel-29',
        'channel-3',
        'channel-30',
        'channel-31',
        'channel-32',
        'channel-33',
        'channel-4',
        'channel-5',
        'channel-6',
        'channel-7',
        'channel-8',
        'channel-9',
        'i2c-10100',
        'power',
        'subsystem',
        'uevent']
cmd13 = ['.*0x48 .* Passed',
        '.*0x44 .* Passed',
        '.*0x72 .* Passed',
        '.*0x50 .*Passed',
        '.*0x51 .* Passed',
        '.*0x64.* Passed',
        '.*0x66 .* Passed',
        '.*0x34 .* Passed',
        '.*0x75 .* Passed',
        '.*0x76 .* Passed',
        '.*0x50 .* Passed',
        '.*0x50 .* Passed',
        '.*0x50 .* Passed',
        '.*0x50 .* Passed',
        '.*0x51 .* Passed',
        '.*0x10 .* Passed',
        '.*0x61 .*Passed',
        '.*0x60 .* Passed',
        '.*0x41 .* Passed',
        '.*0x44 .* Passed',
        '.*0x60 .* Passed',
        '.*0x53 .* Passed',
        '.*0x54 .* Passed',
        '.*0x55 .* Passed',
        '.*0x50 .* Passed',
        '.*0x51 .* Passed',
        '.*0x52 .* Passed',
        '.*0x62 .* Passed',
        '.*0x63 .* Passed',
        '.*0x5c .* Passed',
        '.*0x5b .* Passed',
        '.*0x5b .* Passed']
path1='cd /home/admin/'
path2='cd /usr/local/cls_diag/bin'

#TC_28 Warm Boot Rest Stress Test
filename = 'Warm_Reset_Stress_Test.sh'
bus_pattern = ['-- Journal begins at .*--',
        '.* sonic systemd\\[1\\]: Starting Brixia platform modules...',
        '.* sonic platform-modules-brixia.* Setting up board...',
        '.* sonic platform-modules-brixia.* Brixia',
        '.* sonic platform-modules-brixia.* fan2: .*',
        '.* sonic platform-modules-brixia.* fan3: .*',
        '.* sonic platform-modules-brixia.* fan4: .*',
        '.* sonic platform-modules-brixia.* fan1: .*',
        '.* sonic platform-modules-brixia.* Waiting COMe I2C to be ready:',
        '.* sonic platform-modules-brixia.* continue_found: 1',
        '.* sonic platform-modules-brixia.* continue_found: 2',
        '.* sonic platform-modules-brixia.* continue_found: 3',
        '.* sonic platform-modules-brixia.* continue_found: 4',
        '.* sonic platform-modules-brixia.* continue_found: 5',
        '.* sonic platform-modules-brixia.* continue_found: 6',
        '.* sonic platform-modules-brixia.* continue_found: 7',
        '.* sonic platform-modules-brixia.* continue_found: 8',
        '.* sonic platform-modules-brixia.* continue_found: 9',
        '.* sonic platform-modules-brixia.* continue_found: 10',
        '.* sonic platform-modules-brixia.* Done',
        '.* sonic platform-modules-brixia.* Platform init done.',
        '.* sonic systemd\\[1\\]: Finished Brixia platform modules.']
i2c_l = '.*i2cdetect -l'
Temp = 'Temp test all --> Passed'
osfp = 'All OSFP module is presence: PASS'
sfpplus = 'All SFP\\+ module is presence: PASS'
eth0 = 'eth0:.*UP'
eth_speed = 'Speed: 10.*Mb/s'
ping = '0% packet loss'

#TC_29 WDT stress test
wdt_service = ['Check WDT service',
        'gfpga-watchdog.service - DD3 GFPGA WDT Service',
        'Loaded: loaded \\(/lib/systemd/system/gfpga-watchdog.service; enabled; vendor preset: enabled\\)',
        'Active: active \\(running\\) since .*',
        'Main PID: .* \\(dd3_wdt.sh\\)',
        'Tasks: .*',
        'Memory: .*',
        'CGroup: .*']


#TC03 install uninstall second os
os_format = 'sonic-broadcom-pb'
extension = '.bin'
old_os = SwImage.getSwImage(SwImage.BRIXIA_SONIC).oldVersion
new_os = SwImage.getSwImage(SwImage.BRIXIA_SONIC).newVersion

##
coreboot_version='Version: 999999999.20220110.181349.1'
erase_mailbox='100 % complete'
cryptId="CryptaId:.*"

onie_stop="Stopping.*done."
OS_Install="100%"

sonic_new_image="onie-installer.bin"
sonic_old_image = "onie-installer-x86_64.bin"
fetch_old_sonic = "curl -O http://192.168.0.1/" + sonic_old_image
fetch_new_sonic = "curl -O http://192.168.0.1/" + sonic_new_image


sonic_list=["Current.*SONiC-OS-202106-brixia.pb20","Next.*SONiC-OS-202106-brixia.pb19",
 "Available:", "SONiC-OS-202106-brixia.pb19", "SONiC-OS-202106-brixia.pb20"]

menu=["Welcome to LinuxBoot's Menu","Enter a number to boot a kernel:",
"01. SONiC-OS-202106-brixia.pb20",
"02. SONiC-OS-202106-brixia.pb19"]

menu2=["Welcome to LinuxBoot's Menu","Enter a number to boot a kernel:",".*SONiC-OS-202106-brixia.pb.*"]

filename1='sonic-broadcom-pb18.bin'
filename2='sonic-broadcom-pb20.bin'
filename3='sonic-broadcom-pb19.bin'

filename4='libparted2_3.2-25_amd64.deb'
filename5='parted_3.2-25_amd64.deb'
filename6='sonic-broadcom-pb20_4G.sd.img.zip'
filename7='R3152-M0025-01_Diag-brixia.v0.1.3.deb'

brixia_ip='10.208.140.237'
brixia_comm='Master_L2_7'
mtp_ip='10.208.140.241'
mtp_comm='Master_L2_5'
