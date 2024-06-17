###############################################################################
# LEGALESE:   "Copyright (C) 2020-      Celestica Corp. All rights reserved." #
#                                                                             #
# This source code is confidential, proprietary, and contains trade           #
# secrets that are the sole property of Celestica Corp.                       #
# Copy and/or distribution of this source code or disassembly or reverse      #
# engineering of the resultant object code are strictly forbidden without     #
# the written consent of Celestica Corp.                                      #
#                                                                             #
###############################################################################

# IMPORTANT NOTE:
#   Keep up-to-date Jenkins's SwImages.yaml every time you update it!

import os
import DeviceMgr
from SwImage import SwImage
from Const import BOOT_MODE_UBOOT, BOOT_MODE_DIAGOS, BOOT_MODE_ONIE,ONIE_RESCUE_MODE
import CommonLib
import CommonKeywords



pc_info = DeviceMgr.getServerInfo('PC')
dev_info = DeviceMgr.getDevice()

# diagos_mode = BOOT_MODE_DIAGOS
# uboot_mode = BOOT_MODE_UBOOT
# onie_mode = BOOT_MODE_ONIE

# SwImage shared objects
# CPLD = SwImage.getSwImage("CPLD")
# UBOOT = SwImage.getSwImage("UBOOT")
# End of SwImage shared objects

# uboot_prompt = dev_info.promptUboot
server_username = pc_info.scpUsername
server_password = pc_info.scpPassword
tftp_server_ipv4 = pc_info.managementIP
tftp_interface = dhcp_interface = mgmt_interface = "eth0"
# mgmt_server_ip = pc_info.managementIP

diag_tools_path = "/root/diag"
diag_ld_lib_path = "/root/diag/output"


TempToolVersion_cmd1 = "./bin/cel-cpu-test -v"
TempToolVersion_cmd2 = "./bin/cel-cpu-test --version"
yamlinfo_cmd1 = "./bin/cel-temp-test -l"
yamlinfo_cmd2 = "./bin/cel-temp-test --list"
TempValue_cmd1 = "./bin/cel-temp-test -r -d "
TempValue_cmd2 = "./bin/cel-temp-test --read --dev "
Sensor_cmdlist = ["./bin/cel-temp-test --all", "./bin/cel-temp-test --all  -m high",
        "./bin/cel-temp-test --all  -m normal", "./bin/cel-temp-test --all  -m low",
        "./bin/cel-temp-test --all  --mode high", "./bin/cel-temp-test --all  --mode normal",
        "./bin/cel-temp-test --all  --mode low"]

bin_file = "Dev_Start_I210_Copper_NOMNG_16Mb_A2_3.25_0.03.bin"

############### 13.1_Diag_Tool_Update  ####################
diag_old_version=SwImage.getSwImage(SwImage.ABERLOUR_DIAG).oldVersion
diag_new_version=SwImage.getSwImage(SwImage.ABERLOUR_DIAG).newVersion
diag_old_image=SwImage.getSwImage(SwImage.ABERLOUR_DIAG).oldImage
diag_new_image=SwImage.getSwImage(SwImage.ABERLOUR_DIAG).newImage
diag_image_copy_list = [diag_old_image, diag_new_image]
diag_image_server_path = SwImage.getSwImage(SwImage.ABERLOUR_DIAG).hostImageDir
diag_image_unit_path = SwImage.getSwImage(SwImage.ABERLOUR_DIAG).localImageDir

###############  13.7 Com-e Card Power Monitor Online Update  ####################
firmware_update= "CPU_UCD90120A_U2046_R03_20210305_1709.txt"
firmware_version= "V03"

module_eeprom_help_cmd = "./bin/cel-cpld-test"
module_eeprom_help_pattern = """
Options are:
        -r, --read          Read the data
        -w, --write         Write the data
        -D, --data          Input data
        -d, --dev           Device id <1 is system cpld,2 is cpu cpld>
        -R, --reg           Register id 1..x
        -A, --addr          Register address
        -l, --list          List yaml config
        -V                  Show cpld version
            --all           Test all configure options
        -v, --version        Display the test tool version and exit
        -h, --help          Display this help text and exit""".splitlines()
load_drivers_cmd = [
    "echo 0x54 > /sys/bus/i2c/devices/i2c-7/delete_device",
    "echo 24c04 0x54 > /sys/bus/i2c/devices/i2c-7/new_device",
    "i2cdetect -y 7"]
write_read_by_reg_add_cmd = [
    "./bin/cel-cpld-test -w -d 1 -A 0x30 -D 0x81",
    "./bin/cel-cpld-test -r -d 1 -A 0x30",
    "./bin/cel-cpld-test --write --dev 1 --addr 0x30 --data 0x80",
    "./bin/cel-cpld-test --read --dev 1 --addr 0x30",
]
write_read_by_reg_id_cmd = [
    "./bin/cel-cpld-test -w -d 1 -R 14 -D 0x81",
    "./bin/cel-cpld-test -r -d 1 -R 14",
    "./bin/cel-cpld-test --write --dev 1 --reg 14 --data 0x80",
    "./bin/cel-cpld-test --read --dev 1 --reg 14"
]
eeprom_flash_cmd = [
    "./eeprom -p /sys/bus/i2c/devices/7-0054/eeprom -d 1",
    "./eeprom -c eeprom.cfg -o /sys/bus/i2c/devices/7-0054/eeprom -d 1",
    "./eeprom -p /sys/bus/i2c/devices/7-0054/eeprom -d 1"
]

### PoE_Firmware_Update ###
poe_firmware_help_cmd = "./bin/cel-poe-test"
poe_firmware_help_pattern = """
Usage:=
     -h, --help                    Show the help text
     -v, --version                 Display version
     -R, --reset                   Reset controller
     -r, --restore                 Restore to factory default setting
     -i, --init                    Initilize POE controller
     -p, --port=                   Port number
     -g, --get                     Get operation
     -s, --set                     Set operation
     -S, --swversion               Software version
     -Y, --system-status           PoE system status
     -D, --device-status           PoE device status
     -T, --port-status             PoE port status""".splitlines()
card_type_cmd = "./bin/cel-cards-test -s"
card_type_pattern = "Card type is.*"
tool_ver_cmd = "./bin/cel-cpld-test -v"
tool_ver_ptn = "The ./bin/cel-cpld-test version is :.*"
poe_ver_cmd = "./bin/cel-poe-test -g -S"
poe_ver_ptn = "SW Version:.*"
update_image = "24035492_1092_001.s19"
poe_fw_update_cmd = "./bin/cel-poe-test -U -e ./firmware/" + update_image

### Disk Stress Test  ###
stress_time = "5m"
timeout = '370'
#stress_time = "12h"
#timeout = '43300'


fan_help = ['Options are:',
             '--all           Test all configure options',
         '-s, --status        Show fan present and type',
         '-v, --version        Display the version and exit',
         '-h, --help          Display this help text and exit',
         '-l, --list          List yaml info',
         '-L, --led           Set fan led on or off',
         '-r, --read          Read',
         '-R, --reg           Register ID number',
         '-w, --write         Write',
         '-S, --speed         Set  fan speed',
         '-d, --dev           Fan dev name',
         '-D, --data']

diag_tools_path = "/root/diag"
diag_ld_lib_path = "/root/diag/output"
dcdcmod = "dcdc"
dcdcver = "1.0.0"
volt = "'0x82' || '0x84' || '0x81' || '0x88'"
fanmod = "fan"
fanver = "1.2.0"
dcdc_list = ['dev_1 name: pxe1110_cpu_1']


##  16.2 FCT Test (10G and 25G uplink card) ##

eeprom_cmds = [
        "./bin/cel-cpld-test -w -d 1 -A 0x30 -D 0x80",
        "cd tools",
        "./eeprom -c eeprom.cfg -o /sys/bus/i2c/devices/7-0054/eeprom -d 1",
        "./eeprom -p /sys/bus/i2c/devices/7-0054/eeprom -d 1",
        "cd ..",
        "./bin/cel-cpld-test -w -d 1 -A 0x30 -D 0x81"
    ]

eeprom_test_pattern = [
    "sys_cpld write reg: 0x30 0x80",
    "jedec_code.*=.*",
    "format_version.*=.*",
    "bit_fields.*=.*",
    "assembly_id.*=.*",
    "assembly_major_version.*=.*",
    "assembly_minor_version.*=.*",
    "assembly_revision.*=.*",
    "assembly_pn.*=.*",
    "assembly_sn.*=.*",
    "assembly_flag.*=.*",
    "assembly_manufacture_date.*=.*",
    "reserved.*=.*",
    "customer_identification.*=.*",
    "board_specific_info.*=.*",
    "mac_addr_format_version.*=.*",
    "mac_block_count.*=.*",
    "mac_address.*=.*",
    "unused.*=.*",
    "msi_specific_info.*=.*",
    "clei_code.*=.*",
    "model_number.*=.*",
    "model_major_revision.*=.*",
    "model_minor_revision.*=.*",
    "deviation.*=.*",
    "chassis_sn.*=.*",
    "sys_cpld write reg: 0x30 0x81"
]

sfp_cmds = [
        "cd /root/Diag/aberlour",
        "./bin/cel-cpld-test -w -d 1 -A 0x6a -D 0xb0",
        "cd /root/Diag/aberlour/tools/oom/apps",
        "python inventory.py",
        "python iop.py 0 | grep -a Stacking",
        "python iop.py 0 | grep -a VOLTAGE",
        "python iop.py 1 | grep -a Stacking",
        "python iop.py 1 | grep -a VOLTAGE"

    ]

sfp_test_pattern = [
    "sys_cpld write reg: 0x6A 0xb0",
    "Port Name.*Vendor.*Type.*Part #.*Serial #",
    "Stacking#0 LEONI.*QSFP28.*",
    "Stacking#1 LEONI.*QSFP28.*",
    "Uplink#0.*LEONI.*QSFP28.*",
#    "Uplink#1.*LEONI.*SFP.*",
#    "Uplink#2.*LEONI.*SFP.*",
#    "Uplink#3.*LEONI.*SFP.*",
    "Port: Stacking#0",
    "Port: Stacking#1",
    "SUPPLY_VOLTAGE:",
    "VOLTAGE_HIGH_ALARM:",
    "VOLTAGE_LOW_ALARM:"
]


######11.20 #######


cpu_list = ['\[CPU_EEPROM\]',
  'jedec_code                     = 0x7FB0',
  'format_version                 = 0x02',
  'bit_fields                     = .*',
  'assembly_id                    = 0x0DCC',
  'assembly_major_version         = 0x01',
  'assembly_minor_version         = 0x01',
  'assembly_revision              = REV 08',
  'assembly_pn                    = 611-107142',
  'assembly_sn                    = ZN4322120571',
  'assembly_flag                  = 0x00',
  'assembly_manufacture_date      = 20220412',
  'reserved                       = 0xFFFF',
  'customer_identification        = 0xFF',
  'board_specific_info            = 0xAD',
  'mac_addr_format_version        = 0x01',
  'mac_block_count                = 0x0080',
  'mac_address                    = a2:23:45:45:01:02',
  'unused                         = ff:ff:ff:ff:ff:ff',
  'msi_specific_info              = 0x01',
  'deviation                      = FFFFFFFFFF']



sys_list = ['\[SYS_EEPROM\]',
    'jedec_code                     = 0x7FB0',
    'format_version                 = 0x02',
    'bit_fields                     = 0xFC',
    'assembly_id                    = 0x0DCC',
    'assembly_major_version         = 0x01',
    'assembly_minor_version         = 0x01',
    'assembly_revision              = REV 08',
    'assembly_pn                    = 611-107142',
    'assembly_sn                    = ZN4322120571',
    'assembly_flag                  = 0x00',
    'assembly_manufacture_date      = 20220412',
    'reserved                       = 0xFFFF',
    'customer_identification        = 0xFF',
    'board_specific_info            = 0xAD',
    'mac_addr_format_version        = 0x01',
    'mac_block_count                = 0x0080',
    'mac_address                    = a2:23:45:45:01:02',
    'unused                         = ff:ff:ff:ff:ff:ff',
    'msi_specific_info              = 0x01',
    'clei_code                      = DUMMYCLEI',
#    'model_number                   = EX4400-48P-S',
    'model_major_revision           = 0x31',
    'model_minor_revision           = 0x0000',
    'deviation                      = FFFFFFFFFF',
    'chassis_sn                     = XC0219200001']

sys_list1 = ['\[SYS_EEPROM\]',
    'jedec_code                     = 0x7FB0',
    'format_version                 = 0x02',
    'bit_fields                     = 0xFC',
    'assembly_id                    = 0x0DCC',
    'assembly_major_version         = 0x01',
    'assembly_minor_version         = 0x01',
    'assembly_revision              = REV 08',
    'assembly_pn                    = 611-107142',
    'assembly_sn                    = ZN4322120571',
    'assembly_flag                  = 0x00',
    'assembly_manufacture_date      = 20220412',
    'reserved                       = 0xFFFF',
    'customer_identification        = 0xFF',
    'board_specific_info            = 0xAD',
    'mac_addr_format_version        = 0x01',
    'mac_block_count                = 0x0080',
    'mac_address                    = a2:23:45:45:01:02',
    'unused                         = ff:ff:ff:ff:ff:ff',
    'msi_specific_info              = 0x01',
    'clei_code                      = DUMMYCLEI',
    'model_number                   = EX4400-48F-S',
    'model_major_revision           = 0x31',
    'model_minor_revision           = 0x0000',
    'deviation                      = FFFFFFFFFF',
    'chassis_sn                     = XC0219200001']

dcdcmod = "dcdc"
dcdcver = "1.0.0"
#volt = '0x82'
fanmod = "fan"
fanver = "1.2.0"
dcdc_list = ['dev_1 name: pxe1110_cpu_1',
'dev_1 path: /dev/',
'dev_1 type: DCDC',
'dev_1 margin: 0',
'dev_1 chl: 3',
'dev_1 chl_1 type: voltage',
'dev_1 chl_1 name: 12V',
'dev_1 chl_1 max: 12.6',
'dev_1 chl_1 min: 11.4',
'dev_1 chl_1 value: 12.0',
'dev_1 chl_2 type: voltage',
'dev_1 chl_2 name: VCCP',
'dev_1 chl_2 max: 1.3',
'dev_1 chl_2 min: 0.5',
'dev_1 chl_2 value: 1.0',
'dev_1 chl_3 type: voltage',
'dev_1 chl_3 name: VNNP',
'dev_1 chl_3 max: 1.3',
'dev_1 chl_3 min: 0.6',
'dev_1 chl_3 value: 1.0',
'dev_2 name: pxe1110_cpu_1',
'dev_2 path: /dev/',
'dev_2 type: DCDC',
'dev_2 margin: 0',
'dev_2 chl: 3',
'dev_2 chl_1 type: current',
'dev_2 chl_1 name: 12V',
'dev_2 chl_1 max: 0',
'dev_2 chl_1 min: 0',
'dev_2 chl_1 value: 0',
'dev_2 chl_2 type: current',
'dev_2 chl_2 name: VCCP',
'dev_2 chl_2 max: 45',
'dev_2 chl_2 min: 0',
'dev_2 chl_2 value: 0',
'dev_2 chl_3 type: current',
'dev_2 chl_3 name: VNNP',
'dev_2 chl_3 max: 12',
'dev_2 chl_3 min: 0',
'dev_2 chl_3 value: 0',
'dev_3 name: pxe1110_cpu_2',
'dev_3 path: /dev/',
'dev_3 type: DCDC',
'dev_3 margin: 0',
'dev_3 chl: 3',
'dev_3 chl_1 type: voltage',
'dev_3 chl_1 name: 12V',
'dev_3 chl_1 max: 12.6',
'dev_3 chl_1 min: 11.4',
'dev_3 chl_1 value: 12.0',
'dev_3 chl_2 type: voltage',
'dev_3 chl_2 name: VDDQ',
'dev_3 chl_2 max: 1.26',
'dev_3 chl_2 min: 1.14',
'dev_3 chl_2 value: 1.2',
'dev_3 chl_3 type: voltage',
'dev_3 chl_3 name: VCCRAMP',
'dev_3 chl_3 max: 1.3',
'dev_3 chl_3 min: 0.7',
'dev_3 chl_3 value: 1.0',
'dev_4 name: pxe1110_cpu_2',
'dev_4 path: /dev/',
'dev_4 type: DCDC',
'dev_4 margin: 0',
'dev_4 chl: 3',
'dev_4 chl_1 type: current',
'dev_4 chl_1 name: 12V',
'dev_4 chl_1 max: 0',
'dev_4 chl_1 min: 0',
'dev_4 chl_1 value: 0',
'dev_4 chl_2 type: current',
'dev_4 chl_2 name: VDDQ',
'dev_4 chl_2 max: 21',
'dev_4 chl_2 min: 0',
'dev_4 chl_2 value: 0',
'dev_4 chl_3 type: current',
'dev_4 chl_3 name: VCCRAMP',
'dev_4 chl_3 max: 8',
'dev_4 chl_3 min: 0',
'dev_4 chl_3 value: 0',
'dev_5 name: pxe1331',
'dev_5 path: /dev/',
'dev_5 type: DCDC',
'dev_5 margin: 1',
'dev_5 chl: 4',
'dev_5 chl_1 type: voltage',
'dev_5 chl_1 name: 12V',
'dev_5 chl_1 max: 12.6',
'dev_5 chl_1 min: 11.4',
'dev_5 chl_1 value: 12.0',
'dev_5 chl_2 type: voltage',
'dev_5 chl_2 name: VDD_CORE',
'dev_5 chl_2 max: 0.945',
'dev_5 chl_2 min: 0.855',
'dev_5 chl_2 value: 0.9',
'dev_5 chl_3 type: voltage',
'dev_5 chl_3 name: VDD_3V3',
'dev_5 chl_3 max: 3.399',
'dev_5 chl_3 min: 3.201',
'dev_5 chl_3 value: 3.3',
'dev_5 chl_4 type: voltage',
'dev_5 chl_4 name: VDD_1V0',
'dev_5 chl_4 max: 1.05',
'dev_5 chl_4 min: 0.95',
'dev_5 chl_4 value: 1.0',
'dev_6 name: pxe1331',
'dev_6 path: /dev/',
'dev_6 type: DCDC',
'dev_6 margin: 1',
'dev_6 chl: 4',
'dev_6 chl_1 type: current',
'dev_6 chl_1 name: 12V',
'dev_6 chl_1 max: 0',
'dev_6 chl_1 min: 0',
'dev_6 chl_1 value: 0',
'dev_6 chl_2 type: current',
'dev_6 chl_2 name: VDD_CORE',
'dev_6 chl_2 max: 59',
'dev_6 chl_2 min: 0',
'dev_6 chl_2 value: 0',
'dev_6 chl_3 type: current',
'dev_6 chl_3 name: VDD_3V3',
'dev_6 chl_3 max: 23.765',
'dev_6 chl_3 min: 0',
'dev_6 chl_3 value: 0',
'dev_6 chl_4 type: current',
'dev_6 chl_4 name: VDD_1V0',
'dev_6 chl_4 max: 21.1',
'dev_6 chl_4 min: 0',
'dev_6 chl_4 value: 0']


# 13.3 CPU CPLD Update
cpu_cpld_old_bin = "lre_p_r0006.bin"
cpu_cpld_new_bin = "lre_g_r0100.bin"

cpld_update_pattern = [
    "read_device_id",
    "Enable Program - Transparent Mode",
    "Erase Flash NVCM0/CFG NVCM1/UFM",
    "- Program CFG Page -",
    "...Done!",
    "- Verify CFG Page -",
    "...Done!",
    "Program Done"
]

# 13.6 Switch Card Power Monitor Online Update
switch_card_help_pattern = [
    "argument is so few",
    "Usage: ./cel-pwmon-upgrade options \\(-h\\|-s\\|-f\\) \\(SYS\\|CPU\\)",
    "-h show help",
    "-s select type PWMON",
    "-f update image file"
]

switch_update_pattern = [
    "Start to Program the SYS PWMON IC!",
    "Maybe need waitting for 90 seconds!",
    "Warning, don't power off!!!",
    "have program done the pwmon",
    "If you want to refresh the SYS PWMON IC image",
    "Need to write the system cpld 0x61 register to 0xf3 to power cycle system"
]

# 11.33 Fly back cable Voltage drop Test
fly_back_pass_pattern = [
    "Cable Voltage Port1#:.*V",
    "Cable Voltage Port2#:.*V",
    "pass"
]

# 13.2 System CPLD Update
sys_cpld_vme_image_old = "systemcpld_v000e_20210205.vme"
sys_cpld_vme_image_new = "systemcpld_v000f_20210302.vme"
scan_pattern=["Scan /dev/i2c-0 :",".*0  1  2  3  4  5  6  7  8  9  a  b  c  d  e  f",
"00:          -- -- -- -- -- -- -- -- -- -- -- UU --",
"10: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --",
"20: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --",
"30: -- -- -- -- UU -- UU -- -- -- UU -- -- -- -- --",
"40: -- -- -- -- -- -- -- -- -- UU UU.* UU UU UU --",
"50: UU UU -- -- UU UU UU UU -- -- -- -- -- -- -- --",
"60: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --",
"70: UU -- UU UU -- -- -- --"]

single_scan_bus_pattern=["Scan /dev/i2c-1 :",".*0  1  2  3  4  5  6  7  8  9  a  b  c  d  e  f", ".* --.*",
".*-- UU.*", ".* --.*", ".*30 31 -- -- 34 35 36 -- .* --"]

dump_test_pattern=["00: .*REV 01..",
"10:.*640-107.*..","20:.*","30.*?...??.*"]   

i2c_detect_pattern=[".* I2c Detect all.*"]

## Mgmt Eth port stress test
mgmtVersion = 'iperf'
server_pwd = 'intel@1234'
server_path = 'cd ../home/automation/Auto_Test/automation/Juniper/autotest/tool/'
server_cmd = './iperf -s'
stress_count = '10'
cmd_timeout = '30'

#dc controller test for 48mp
volt_1= '0x84'

emmc_ffu_firmware_version = "R96-103164TL29L07"
emmc_fw_revision_pattern = "'R96-84810SI05Q05' || 'R96-103164TL29L07' || 'R92-97969TH12P55'"

