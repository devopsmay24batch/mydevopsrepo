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
import CommonLib

from SwImage import SwImage
from Const import BOOT_MODE_UBOOT, BOOT_MODE_DIAGOS, BOOT_MODE_ONIE,ONIE_RESCUE_MODE


pc_info = DeviceMgr.getServerInfo('ERACKSERVER')
dev_info = DeviceMgr.getDevice()

diagos_mode = BOOT_MODE_DIAGOS
uboot_mode = BOOT_MODE_UBOOT
onie_mode = BOOT_MODE_ONIE


scp_ip = pc_info.managementIP
scp_username = pc_info.scpUsername
scp_password = pc_info.scpPassword
dhcp_username = pc_info.username
dhcp_password = pc_info.password
dhcp_prompt = pc_info.prompt
tftp_server_ipv4 = pc_info.managementIP
tftp_interface = dhcp_interface = mgmt_interface = "eth0"

diag = 'sysinfo'

bmc = 'bmc'


#image_path ='/MOONSTONE/'
image_path ='/MOONSTONE/DVT/'
MOONSTONE = SwImage.getSwImage("MOONSTONE_DIAG")
diag_image = MOONSTONE.newImage
diag_version = MOONSTONE.newVersion

old_image = MOONSTONE.oldImage
old_version = MOONSTONE.oldVersion



baseVersion = CommonLib.get_swinfo_dict("MOONSTONE_DIAG")
cpld_image = baseVersion.get('bb_clpd_image')
cpld_upgrade_version = baseVersion.get('bb_cpld_version')
fpga_image = baseVersion.get('fpga_image')
fpga_upgrade_version = baseVersion.get('fpga_version')
bios_image = baseVersion.get('bios_image')
bios_upgrade_version = baseVersion.get('bios_version')

cpld = 'bbcpld'
cpld_version=diag_version
cpld_help=['-h, --help    Display this help text and exit',
   '-V\, --verbose Set verbose\[\'EMERG\'\, \'ALERT\'\, \'CRIT\'\, \'ERROR\'\, \'WARNING\'\, \'NOTICE\'\, \'INFO\', \'DEBUG\'\]',
   '-v\, --version Display the version and exit',
   '-x\, --nolog   Don\'t output to log file',
   '-b\, --bmc     Send command to BMC',
   '--all     Test all configure options',
   '-l\, --list    List the config info',
   '-u\, --dump    Dump all register contents of a CPLD device',
   '-r\, --read    Read option',
   '-w\, --write   Write option',
   '-f\, --file    Config file',
   '-d\, --dev     Device id \[1:baseboard | 2:switch_cpld1 | 3:switch_cpld2 | 4:fpga | 5: come_cpld \]',
   '-R\, --reg     Register id',
   '-D\, --data    Write data with hex value',
   '-A\, --addr    Register address']

bbcpld_help=['--all             Test all configure options',
    '-l, --list            Show device list',
    '-d, --dev             Test device id id',
    '-v, --version         Show diag version',
    '-x, --loop            Loop to test',
    '-h, --help            Display this help text and exit',
    'Example:',
    './cel-cpld-test --all      Test all device id',
    './cel-cpld-test -d 1       Test device id 1',
    './cel-cpld-test -h         Display help message']

bbcpld_list=['cpld_sysfs_path: /sys/devices/platform/sys_cpld',
	' 1 | CPLD_B_Version                           |   0XA100  | N/A    |',
	'51 | Cust_ID                                  |   0XA1A2  | N/A    |']

fpga = 'fpga'
fpga_version = diag_version 
fpga_help = ['--all             Test all configure options',
    '-l, --list            Show device list',
    '-d, --dev             Test device id id',
    '-v, --version         Show diag version',
    '-x, --loop            Loop to test',
    '-h, --help            Display this help text and exit',
    'Example:',
    './cel-fpga-test --all      Test all device id',
    './cel-fpga-test -d 1       Test device id 1',
    './cel-fpga-test -h         Display help message']
fpga_list=['fpga_sysfs_path: /sys/devices/platform/cls_sw_fpga/FPGA/',
	' 1 | FPGA_Version                             |   0X00000000  | N/A    |',
	' 9 | SFP2_Ctrl_Stat_Register                  |   0X00001008  | N/A    |']
bios = 'bios'

moonstone_bmc ='1.02'
devicename = os.environ.get("deviceName", "")
dummymac=DeviceMgr.getDevice(devicename).get('dummyBmcMac')
realmac=DeviceMgr.getDevice(devicename).get('realBmcMac')
come_mgmt=DeviceMgr.getDevice(devicename).get('managementIP2')
realcomemac=DeviceMgr.getDevice(devicename).get('realComeMac')

eeprom = 'eeprom'
eeprom_help=['Options are:',
             '--all           Test all configure options',
             '--dump          Dump eeprom info',
             '--fru           Fru operate; SMBIOS',
         '-o, --out           Output biniry file with dumped data',
         '-O, --offset        EEPROM data offset',
         '-p, --update        Update the eeprom content with the binary file',
         '-f, --file          \[binary file path\]',
         '-v, --version       Display the version and exit',
         '-h, --help          Display this help text and exit',
         '-l, --list          List yaml info',
         '-r, --read          Read options',
         '-w, --write         Write options',
         '-d, --dev           \[dev num: 1\]',
         '-t, --type          \[eeprom type:tlv\]',
         '-D, --data          \[dev info\]',
         '-A, --addr          \[tlv type code address\]']

eeprom_list=['group:1, type: tlv, format: tlv, dev_num:1',
             'group:2, type: smbios, format: fru, dev_num:1']
eeprom_version = diag_version


sysinfo='sysinfo'
sysinfo_version=diag_version
sysinfo_help=['usage: ./cel-sysinfo-test \[OPTIONS\]',
       'Options are:',
       '--all           Test all configure options',
       '-s, --status        Show sysinfo presence and type',
       '-v, --version       Display the version and exit',
       '-h, --help          Display this help text and exit',
       '-l, --list          List yaml info',
       '-f, --file          Specify the yaml configure file',
       '-d, --dev           device id']

sysinfo_list=['sysinfos_info:dev_num : 8',

 'sysinfo name : BIOS',
 'dev_id : 1',
 'get vesion command : dmidecode -t bios | grep Version',
 'present or absent ; present',
 'need analy : no',
 'processing data : NULL',
 'check failed : FAILED',

 'sysinfo name : COMe CPLD',
 'dev_id : 2',
 'get vesion command : ../tools/lpc_cpld_x86_64 blu r 0xA1E0',
 'present or absent ; present',
 'need analy : no',
 'processing data : NULL',
 'check failed : FAILED',

 'sysinfo name : Baseboard CPLD',
 'dev_id : 3',
 'get vesion command : ../tools/lpc_cpld_x86_64 blu r 0xA100',
 'present or absent ; present',
 'need analy : no',
 'processing data : NULL',
 'check failed : FAILED',

 'sysinfo name : OS',
 'dev_id : 4',
 'get vesion command : cat /proc/version',
 'present or absent ; present',
 'need analy : no',
 'processing data : NULL',
 'check failed : FAILED',

 'sysinfo name : Diag',
 'dev_id : 5',
 "get vesion command : echo -n 'Diag Version: ';cat ../diag_configs/version",
 'present or absent ; present',
 'need analy : no',
 'processing data : NULL',
 'check failed : FAILED',

 'sysinfo name : Switch CPLD 1',
 'dev_id : 6',
 "get vesion command : cat /sys/devices/platform/cls_sw_fpga/CPLD1/version",
 'present or absent ; present',
 'need analy : no',
 'processing data : NULL',
 'check failed : FAILED',

 'sysinfo name : Switch CPLD 2',
 'dev_id : 7',
 'get vesion command : cat /sys/devices/platform/cls_sw_fpga/CPLD2/version',
 'present or absent ; present',
 'need analy : no',
 'processing data : NULL',
 'check failed : FAILED',

 'sysinfo name : FPGA',
 'dev_id : 8',
 'get vesion command : cat /sys/devices/platform/cls_sw_fpga/FPGA/version',
 'present or absent ; present',
 'need analy : no',
 'processing data : NULL',
 'check failed : FAILED',]
"""
 'sysinfo name : FPGA',
 'dev_id : 9',
 'get vesion command : cat /sys/devices/platform/cls_sw_fpga/FPGA/version',
 'present or absent ; present',
 'need analy : no',
 'processing data : NULL',
 'check failed : FAILED']"""


uart='uart'
uart_list = ['ttyS0    115200',
        'ttyS1      9600']
uart_version= diag_version
uart_help=['Options are:',
 '-l, --list   List config info',
 '-r, --read   Read option',
 '-w, --write  Write option',
 '-d, --dev    \[device id:1-2\]',
 '-t, --type   \[cfg\]',
 '-f, --file   Specify the yaml configure file',
 '-D, --data   \[text value\]',
 '-m, --mode   set device and parity etc',
 '--all    Test all config']


sfp = 'sfp'
sfp_version=diag_version
sfp_help=['Options are:',
	   '--all         Test all configure options',
	   '--lpmode      Set OSFP low power mode to all ports',
	   '--hpmode      Set OSFP high power mode to all ports',
	   '-l, --list    List brief information',
	   '-h, --help    Display this help text and exit']


sfp_list=['osfp num:     : 64',
            'sfp\+ num:     : 2',
	    'osfp:name     : osfp_eeprom',
	    'dev_path : /sys/bus/i2c/devices',
	    'present  : ../tools/osfp_control.sh',
	    'sfp\+:name     : sfp1_eeprom',
	    'dev_path : /sys/bus/i2c/devices',
	    'present  : ../tools/pcimem /sys/bus/pci/devices/0000\\\:11\\\:00.0/resource0 0x1004 w',
	    'sfp\+:name     : sfp2_eeprom',
	    'dev_path : /sys/bus/i2c/devices',
	    'present  : ../tools/pcimem /sys/bus/pci/devices/0000\\\:11\\\:00.0/resource0 0x1008 w']

sfp_lpmode_list = ['lpmode',
        'Set OSFP all ports to low power mode',
        'OSFP LED must change to be orange color']

sfp_hpmode_list = ['hpmode',
        'Set OSFP all ports to high power mode',
        'OSFP LED must change to be green color after set high power to ELB']

rtc ='rtc'
rtc_version=diag_version
rtc_help = ["Options are:",
        "-r, --read       Read rtc data",
        "-w, --write      Use the config to test write",
        "-D, --data       \[Input the date and time eg:'20201231 235959'\]",
        "--all        Test all configure options",
        "-v, --version    Display the version and exit",
        "-h, --help       Display this help text and exit"]


new_date='\'20201231 235959\''
current_date='Curr Date info : 2021-01-01'


pci='pci'
pci_version=diag_version
pci_help=['Options are:',
    '-V, --verbose    Verbose',
    '-v, --version    Version',
    '-h, --help       Show this help text',
    '--all        Test all configure options',
    '-l, --list       list config',
    '-s, --scan       Scan the specific pcie device']

pci_list=['Xilinx Corporation Device',
        'Broadcom Limited Device f900',
        'Intel Corporation I210']

cpu='cpu'
cpu_version=diag_version
cpu_help=["Options are:",
    "-h, --help     Display this help text and exit",
    "-V, --verbose  Set verbose\['EMERG', 'ALERT', 'CRIT', 'ERROR', 'WARNING', 'NOTICE', 'INFO', 'DEBUG'\]",
    "-v, --version  Display the version and exit",
    "--all      Test all configure options",
    "-l, --list     List the config info",
    "-f, --file     Use config filename",
    "-i, --info     Show cpu information"]
cpu_list=['cpu_cores: 8',
        'cpu_threads: 16',
        'cpu_freq: 3200',
        'vendor_id: GenuineIntel',
        'model_name: Intel\(R\)Xeon\(R\)CPUD\-1649N@2.30GHz']

fan='fan'
fan_help=['Options are:',
        '--all             Test all configure options',
        '-l, --list            Show device list',
        '-v, --version         Show diag version',
        '-h, --help            Display this help text and exit']

fan_list = ['cpld_sysfs_path: /sys/devices/platform/sys_cpld',
	'read_interface: getreg',
	'write_interface: setreg',
	'max_rear_fan_rpm:',
	'min_rear_fan_rpm:',
	'max_front_fan_rpm:',
	'min_front_fan_rpm:',
	'dev  | Register name                           |   Offset',
	'Fan1 | ctrl_reg                                |   0XA140',
	'     | fan_presence                            |   0xA141',
	'     | rear_fan_reg                            |   0xA142',
	'     | front_fan_reg                           |   0xA143',
	'Fan2 | ctrl_reg                                |   0XA144',
	'     | fan_presence                            |   0xA145',
	'     | rear_fan_reg                            |   0xA146',
	'     | front_fan_reg                           |   0xA147',
	'Fan3 | ctrl_reg                                |   0XA148',
	'     | fan_presence                            |   0xA149',
	'     | rear_fan_reg                            |   0xA14A',
	'     | front_fan_reg                           |   0xA14B']

storage='storage'
storage_version = diag_version 
storage_help=['--all                   Do auto test.',
	   '-f, --file                  Defined configuration file',
	   '-l, --list                  Display the yaml configure file.',
	   '-d, --dev  \[ID\]             Test device id.',
	   '-i, --info                  Show all storage information.',
	   '-v, --version               Display the version and exit.',
	   '-h, --help                  Display this help text and exit.']

phy_speed = '1000'
phy_mode = 'full'

mem='mem'
mem_list=['Memory Info',
        'capacity : 64GB',
        'total_mem : 32768',
        'number of Devices : 2']

tpm='tpm'

i2c='i2c'
i2c_version = diag_version 
i2c_help = ['Options are:',
    "-V, --verbose      Set verbose\['EMERG', 'ALERT', 'CRIT', 'ERROR', 'WARNING', 'NOTICE', 'INFO', 'DEBUG'\]",
    '-v, --version      Display the version and exit',
    '-h, --help         Display this help text and exit',
    '-l, --list         List config yaml file data',
    '-u, --dump         Read and dump i2c data from specified i2c bus and address',
    '--all          Test all configure options',
    '--detect       Detect i2c buses',
    '-s, --scan         Scan the device under /dev/i2c-x',
    '-r, --read         Read option',
    '-w, --write        Write option',
    '-f, --file         Config file name',
    '-A, --addr         \[addr\] device address',
    '-D, --data         I2c data',
    '-R, --reg          \[reg\] of i2c device for 8bits address',
    '--bus          \[i2c bus num:0-5,10-41\]']
i2c_list = ['group:  1,  bus:      0,  type: cpu ',
            'group:  2,  bus:      1,  type: cpu',
            'group:  3,  bus:      2,  type: cpu',
            'group:  4,  bus:      3,  type: cpu',
            'group:  5,  bus:      4,  type: cpu']

eeprom_fru = 'eeprom_fru'
eeprom_fru_version = diag_version
eeprom_fru_help = ['Options are:',
         '-v, --version       Display the version and exit',
         '-h, --help          Display this help text and exit',
         '-l, --list          List yaml info',
         '-r, --read          Read FRU information',
         '-t, --type          \[type val\]  base/bmc/come/sw/fan1/fan2/fan3/psu1/psu2/psu3/psu4']
eeprom_fru_list = ['group:1,\s+type:\s+BMC',
      'bmc\s+\|\s+10', 
      'group:2,\s+type:\s+Baseboard',
      'base\s+\|\s+152', 
      'group:3,\s+type:\s+COMe',
      'come\s+\|\s+210',  
      'group:4,\s+type:\s+psu',
      'psu1\s+\|\s+215',  
      'psu2\s+\|\s+26',
      'psu3\s+\|\s+128', 
      'psu4\s+\|\s+154',
      'group:5,\s+type:\s+switch',
      'sw\s+\|\s+163',  
      'group:6,\s+type:\s+Fan',
      'fan1\s+\|\s+239', 
      'fan2\s+\|\s+142', 
      'fan3\s+\|\s+30'] 

eeprom_bmc = 'eeprom-bmc'
eeprom_bmc_help = ['Options are:',
                '-r  --read       Read options',
                '--dump       Dump all FRU information',
                '-w  --write      Write options',
                '-l, --list       List yaml info', 
                '-t, --type       \[Type value:come,bmc,switch,system,fan1-3,psu1-4\]',
                '-v, --version    Display the version and exit',
                '-h, --help       Display this help text and exit'] 
eeprom_bmc_list = ['0           come         0x50         come-0-50',
    '8           bmc          0x51          bmc-8-51',
    '8           system       0x57       system-8-57',
    '8           switch       0x50       switch-8-50',
    '5           fan1         0x51         fan-16-51',
 'addr: 0x77, reg: 0x00, mask: 0xff, val: 0x01',
    '5           fan2         0x51         fan-17-51',
 'addr: 0x77, reg: 0x00, mask: 0xff, val: 0x02',
    '5           fan3         0x51         fan-18-51',
 'addr: 0x77, reg: 0x00, mask: 0xff, val: 0x04',
    '5           psu1         0x50         psu-19-50',
 'addr: 0x77, reg: 0x00, mask: 0xff, val: 0x08',
   '5           psu2         0x50         psu-20-50',
 'addr: 0x77, reg: 0x00, mask: 0xff, val: 0x10',
    '5           psu3         0x50         psu-21-50',
 'addr: 0x77, reg: 0x00, mask: 0xff, val: 0x20',
    '5           psu4         0x50         psu-22-50',
 'addr: 0x77, reg: 0x00, mask: 0xff, val: 0x40']
eeprom_bmc_dump = ['FRU Device Description : BASE_BOARD_FRU \(ID 24\)',
 'Board Mfg Date        : Tue May 28 13:00:00 2019',
 'Board Mfg             : Celestica',
 'Board Product         : DS5000_Baseboard',
 'Board Serial          : R4028-G0002-01XXXXXXXXX',
 'Board Part Number     : R4028-G0002-01',
 'Board Extra           : DS5000_Baseboard',
 'Board Extra           : 01',
 'Product Manufacturer  : Celestica',
 'Product Name          : DS5000',
 'Product Part Number   : R4028-F9001-02',
 'Product Version       : 07',
 'Product Serial        : DV123456789123',
 'Product Extra         : F2B',
 'Product Extra         : B4DB9199BDA4',
 'Product Extra         : 384',

'FRU Device Description : PSU2_FRU \(ID 26\)',
 'Product Manufacturer  : DELTA',
 'Product Name          : TDPS2000LB A',  
 'Product Part Number   : TDPS2000LB A',  
 'Product Version       : S2F',  
 'Product Serial        : JJLT2311000204', 

'FRU Device Description : FAN2_FRU \(ID 77\)',
 'Board Mfg Date        : Tue May 28 13:00:00 2019',
 'Board Mfg             : Celestica',
 'Board Product         : DS5000_Fan Module Board',
 'Board Serial          : R4028-G0022-01222222222',
 'Board Part Number     : R4028-G0005-02',
 'Board Extra           : Fan Control Board',
 'Board Extra           : 05',

'FRU Device Description : MEZZ_BOARD_FRU \(ID 107\)',
 'Board Mfg Date        : Tue May 28 13:00:00 2019',
 'Board Mfg             : Celestica',
 'Board Product         : DS5000_Fan Module Board',
 'Board Serial          : R4028-G0001-01XXXXXXXXXX',
 'Board Part Number     : R4028-G0001-02',
 'Board Extra           : 06',

'FRU Device Description : FAN1_FRU \(ID 112\)',
 'Board Mfg Date        : Thu Apr 18 12:00:00 2024',
 'Board Mfg             : Celestica India',
 'Board Product         : DS5000_Fan Module Board',
 'Board Serial          : R4028-G0022-01111111111',
 'Board Part Number     : R4028-G0005-02',
 'Board Extra           : Fan Control Board',
 'Board Extra           : 05',

'FRU Device Description : BMC_FRU \(ID 124\)',
 'Board Mfg Date        : Tue May 28 13:00:00 2019',
 'Board Mfg             : Celestica',
 'Board Serial          : R4028-G0007-01XXXXXXXXXXXX',
 'Board Part Number     : R4028-G0007-01',
 'Board Extra           : 02',
 'Board Extra           : 98EAEC809E09',
 'Board Extra           : 1ee45469749834aab7d003ba1d7fe296',
 'Board Extra           : NA',
 'Product Manufacturer  : Celestica',
 'Product Name          : DS5000_BMC',
 'Product Part Number   : R4028-F9001-02',
 'Product Version       : 07',

'FRU Device Description : PSU3_FRU \(ID 128\)',
 'Product Manufacturer  : DELTA',
 'Product Name          : TDPS2000LB A',  
 'Product Part Number   : TDPS2000LB A',  
 'Product Version       : S2F',  
 'Product Serial        : JJLT2311000206', 

'FRU Device Description : PSU4_FRU \(ID 154\)',
 'Product Manufacturer  : DELTA',
 'Product Name          : TDPS2000LB A',  
 'Product Part Number   : TDPS2000LB A',  
 'Product Version       : S2F',  
 'Product Serial        : JJLT2311000201', 

'FRU Device Description : FAN3_FRU \(ID 159\)',
 'Board Mfg Date        : Tue May 28 13:00:00 2019',
 'Board Mfg             : Celestica',
 'Board Product         : DS5000_Fan Module Board',
 'Board Serial          : R4028-G0022-01333333333',
 'Board Part Number     : R4028-G0005-02',
 'Board Extra           : Fan Control Board',
 'Board Extra           : 05',

'FRU Device Description : PSU1_FRU \(ID 215\)',
 'Product Manufacturer  : DELTA',
 'Product Name          : TDPS2000LB A',  
 'Product Part Number   : TDPS2000LB A',  
 'Product Version       : S2F',  
 'Product Serial        : JJLT2311000203',]

mgmt_intf = 'ma1'
dummy_mgmt_intf_mac = '00a0c9020828'
