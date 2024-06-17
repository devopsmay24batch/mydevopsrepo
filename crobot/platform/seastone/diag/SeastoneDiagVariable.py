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


pc_info = DeviceMgr.getServerInfo('PC')
dev_info = DeviceMgr.getDevice()

diagos_mode = BOOT_MODE_DIAGOS
uboot_mode = BOOT_MODE_UBOOT
onie_mode = BOOT_MODE_ONIE


pc_info = DeviceMgr.getServerInfo('PC')
scp_ip = pc_info.managementIP
scp_username = pc_info.scpUsername
scp_password = pc_info.scpPassword
dhcp_username = pc_info.username
dhcp_password = pc_info.password
dhcp_prompt = pc_info.prompt
tftp_server_ipv4 = pc_info.managementIP
tftp_interface = dhcp_interface = mgmt_interface = "eth0"


SEASTONE = SwImage.getSwImage("SEASTONE_DIAG")
SEASTONE1 = SwImage.getSwImage("SEASTONE_BMC")
seastone_diag_version=SEASTONE.newVersion
seastone_bmc=SEASTONE1.newVersion['firmware_revision']
#dummymac=DeviceMgr.getDevice(devicename).get('dummyBmcMac')
#realmac=DeviceMgr.getDevice(devicename).get('realBmcMac')
devicename = os.environ.get("deviceName", "")
dummymac=DeviceMgr.getDevice(devicename).get('dummyBmcMac')
realmac=DeviceMgr.getDevice(devicename).get('realBmcMac')
come_mgmt=DeviceMgr.getDevice(devicename).get('managementIP2')
realcomemac=DeviceMgr.getDevice(devicename).get('realComeMac')
#realmac=SEASTONE.realBmcMac
# mgmt_server_ip = pc_info.managementIP
path= '/root/R1157-J0017-01_V1.4.0-Seastone2_DVT_Diag'

i2c_detect=['i2c-30.*smbus.*SMBus.*I2C Adapter.*PortID: QSFP21.*SMBus adapter',
'i2c-20.*smbus.*SMBus.*I2C Adapter.*PortID: QSFP11.*SMBus adapter',
'i2c-49.*smbus.*SMBus.*I2C Adapter.*PortID: FAN4  .*SMBus adapter',
'i2c-10.*smbus.*SMBus.*I2C Adapter.*PortID: QSFP1 .*SMBus adapter',
'i2c-39.*smbus.*SMBus.*I2C Adapter.*PortID: QSFP30.*SMBus adapter',
'i2c-1	smbus     	SMBus iSMT adapter at df37f000  	SMBus adapter',
'i2c-29.*smbus.*SMBus.*I2C Adapter.*PortID: QSFP20.*SMBus adapter',
'i2c-19.*smbus.*SMBus.*I2C Adapter.*PortID: QSFP10.*SMBus adapter',
'i2c-47.*smbus.*SMBus.*I2C Adapter.*PortID: PSU   .*SMBus adapter',
'i2c-37.*smbus.*SMBus.*I2C Adapter.*PortID: QSFP28.*SMBus adapter',
'i2c-27.*smbus.*SMBus.*I2C Adapter.*PortID: QSFP18.*SMBus adapter',
'i2c-17.*smbus.*SMBus.*I2C Adapter.*PortID: QSFP8 .*SMBus adapter',
'i2c-45.*smbus.*SMBus.*I2C Adapter.*PortID: POWER .*SMBus adapter',
'i2c-35.*smbus.*SMBus.*I2C Adapter.*PortID: QSFP26.*SMBus adapter',
'i2c-25.*smbus.*SMBus.*I2C Adapter.*PortID: QSFP16.*SMBus adapter',
'i2c-53.*smbus.*SMBus.*I2C Adapter.*PortID: LM75  .*SMBus adapter',
'i2c-15.*smbus.*SMBus.*I2C Adapter.*PortID: QSFP6 .*SMBus adapter',
'i2c-43.*smbus.*SMBus.*I2C Adapter.*PortID: SFP2  .*SMBus adapter',
'i2c-33.*smbus.*SMBus.*I2C Adapter.*PortID: QSFP24.*SMBus adapter',
'i2c-23.*smbus.*SMBus.*I2C Adapter.*PortID: QSFP14.*SMBus adapter',
'i2c-51.*smbus.*SMBus.*I2C Adapter.*PortID: FAN1  .*SMBus adapter',
'i2c-13.*smbus.*SMBus.*I2C Adapter.*PortID: QSFP4 .*SMBus adapter',
'i2c-41.*smbus.*SMBus.*I2C Adapter.*PortID: QSFP32.*SMBus adapter',
'i2c-31.*smbus.*SMBus.*I2C Adapter.*PortID: QSFP22.*SMBus adapter',
'i2c-21.*smbus.*SMBus.*I2C Adapter.*PortID: QSFP12.*SMBus adapter',
'i2c-11.*smbus.*SMBus.*I2C Adapter.*PortID: QSFP2 .*SMBus adapter',
'i2c-48.*smbus.*SMBus.*I2C Adapter.*PortID: FAN5  .*SMBus adapter',
'i2c-38.*smbus.*SMBus.*I2C Adapter.*PortID: QSFP29.*SMBus adapter',
'i2c-0	smbus.*SMBus I801 adapter at e000.*SMBus adapter',
'i2c-28.*smbus.*SMBus.*I2C Adapter.*PortID: QSFP19.*SMBus adapter',
'i2c-18.*smbus.*SMBus.*I2C Adapter.*PortID: QSFP9 .*SMBus adapter',
'i2c-46.*smbus.*SMBus.*I2C Adapter.*PortID: CPLD_B.*SMBus adapter',
'i2c-36.*smbus.*SMBus.*I2C Adapter.*PortID: QSFP27.*SMBus adapter',
'i2c-26.*smbus.*SMBus.*I2C Adapter.*PortID: QSFP17.*SMBus adapter',
'i2c-16.*smbus.*SMBus.*I2C Adapter.*PortID: QSFP7 .*SMBus adapter',
'i2c-44.*smbus.*SMBus.*I2C Adapter.*PortID: CPLD  .*SMBus adapter',
'i2c-34.*smbus.*SMBus.*I2C Adapter.*PortID: QSFP25.*SMBus adapter',
'i2c-24.*smbus.*SMBus.*I2C Adapter.*PortID: QSFP15.*SMBus adapter',
'2c-52	smbus.*SMBus I2C Adapter PortID: UCD90120.*SMBus adapter',
'i2c-14.*smbus.*SMBus.*I2C Adapter.*PortID: QSFP5 .*SMBus adapter',
'i2c-42.*smbus.*SMBus.*I2C Adapter.*PortID: SFP1  .*SMBus adapter',
'i2c-32.*smbus.*SMBus.*I2C Adapter.*PortID: QSFP23.*SMBus adapter',
'i2c-22.*smbus.*SMBus.*I2C Adapter.*PortID: QSFP13.*SMBus adapter',
'i2c-50.*smbus.*SMBus.*I2C Adapter.*PortID: FAN2  .*SMBus adapter',
'i2c-12.*smbus.*SMBus.*I2C Adapter.*PortID: QSFP3 .*SMBus adapter',
'i2c-40.*smbus.*SMBus.*I2C Adapter.*PortID: QSFP31.*SMBus adapter']

i2c_detect0=['00:          -- -- -- -- -- 08 -- -- -- -- -- -- --',
'10: -- -- -- -- -- -- -- -- 18 -- -- -- -- -- -- --',
'20: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --', 
'30: 30 31 -- -- 34 35 36 -- -- -- -- -- -- -- -- --', 
'40: -- -- -- -- 44 -- -- -- -- -- -- -- -- -- -- --', 
'50: 50 -- -- -- -- -- -- -- -- -- -- -- -- -- -- --', 
'60: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --', 
'70: -- -- -- -- -- -- -- --']

i2c_detect36=['00:          -- -- -- -- -- -- -- -- -- -- -- -- --',
'10: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --', 
'20: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --', 
'30: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --', 
'40: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --', 
'50: UU -- -- -- -- -- -- -- -- -- -- -- -- -- -- --', 
'60: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --', 
'70: -- -- 72 73 74 75 -- --'] 


#tc2
cpu = 'cpu'
cpu_version=seastone_diag_version


cpu_help=['Options are:',
    '-h, --help     Display this help text and exit',
    '-V, --verbose  Set verbose\[\'EMERG\'\, \'ALERT\'\, \'CRIT\'\, \'ERROR\'\, \'WARNING\'\, \'NOTICE\'\, \'INFO\'\, \'DEBUG\'\]',
    '-v, --version  Display the version and exit',
    '-x\, --nolog    Don\'t output to log file',
    '--all      Test all configure options',
    '-l\, --list     List the config info',
    '-f\, --file     Use config filename',
    '-i\, --info     Show cpu information',
    ]
	
cpu_list=['cpu_cores: 4',
         'cpu_freq: 2400',
    	 'vendor_id: GenuineIntel',
	 'model_name: Intel\(R\)Atom\(TM\)CPUC3558R\@2\.40GHz']


#tc2:
bmc='bmc'
bios='bios'
upgrade='upgrade'
fpga='fpga'
#tc3:
cpld='cpld'
cpld_version=seastone_diag_version
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

cpld_list=['Device 01 | Baseboard_CPLD, Base_addr: 0xA100, Reg_num: 87, Dev_path: /sys/devices/platform/mfd_cpld/baseboard_reg_fields.2.auto',
           'Device 02 | MISC_CPLD1, Base_addr: 0x0000, Reg_num: 12, Dev_path: /sys/bus/i2c/devices/10-0030/CPLD1',
	   'Device 03 | MISC_CPLD2, Base_addr: 0x0000, Reg_num: 12, Dev_path: /sys/bus/i2c/devices/11-0031/CPLD2',
	   'Device 04 | FPGA, Base_addr: 0x0000, Reg_num: 6, Dev_path: /sys/devices/pci0000:00/0000:00:1c.0/0000:09:00.0/FPGA4SW',
	   'Device 05 | COME_CPLD, Base_addr: 0xA1E0, Reg_num: 10, Dev_path: /sys/devices/platform/come_cpld']

internal_usb=['Manufacturer: American Megatrends Inc', 
'New USB device found',
        'Product: Virtual Hub']

lsusb = ['Linux Foundation 3.0',
        'Linux Foundation 2.0',
        'American Megatrends',
        'American Megatrends',
        'American Megatrends']

qsfp='qsfp'
qsfp_help=['Options are:',
        '--all.*Test status of all transceiver',
        '-l, --list           List brief information',
        '-T, --temperature    QSFP,QSFPDD temperature test',
        '-z, --retry          retry to read tranciver eeprom \[default 1\]',
        '-h, --help           Display this help text and exit']


qsfp_list=['group:  1, type: qsfp',
 'pld_info:',
  'name: fpga',
  'path: /sys/bus/pci/devices/0000:06:00.0/fpga-sysfs',
  'read_port: getreg',
  'size: 0',
  'eeprom_info:',
  'name: qsfpdd_eeprom',
  'path: /sys/bus/i2c/devices',
  'offset: 0',
  'size: 1024',
  'group:  2, type: sfp',
   'pld_info:',
   'name: fpga',
   'path: /sys/bus/pci/devices/0000:06:00.0/fpga-sysfs',
   'read_port: getreg',
   'size: 0',
   'eeprom_info:',
   'name:.*sfp\+\_eerpom',
   'path: /sys/bus/i2c/devices',
   'offset: 0',
   'size: 1024']
qsfp_version=seastone_diag_version


sfp = 'sfp'
sfp_version=seastone_diag_version
sfp_help=['Options are:',
               '-r, --read          Read option',
               '    --all           Test all configure options',
               '-w, --write         Write option',
               '-d, --dev       \[device id:qsfp:1-8,sfp:1-48\]',
               '-t, --type      \[eg:QSFP or SFP\]',
               '-D, --data          \[port attribute value:hex 1 or 0\]',
               '-l, --list          List yaml info',
               '-p, --port          \[io port:eg:qsfp_lpmode|qsfp_modirq|qsfp_modprs|qsfp_reset',
               'sfp_modabs|sfp_rxlos|sfp_txdisable|sfp_txfault\]',
               '-v, --version       Display the version info',
               '-h, --help          Display the help info']


sfp_list=['qsfp_modprsL',
        'attr.*rd',
        'qsfp_lpmode',
        'attr.*rdwr',
        'qsfp_resetL',
        'attr.*rdwr',
        'sfp_modabs',
        'attr.*rd',
        'sfp_rxlos',
        'attr.*rd',
        'sfp_txdisable',
        'attr.*rdwr']

rtc='rtc'
rtc_version=seastone_diag_version
rtc_help=['Options are:',
        '-r, --read       Read rtc data',
        '-w, --write      Use the config to test write',
        '-D, --data       \[Input the date and time eg:\'20201231 235959\'\]',
        '    --all        Test all configure options',
        '-v, --version    Display the version and exit',
        '-h, --help       Display this help text and exit']



new_date='\'20201231 235959\''
current_date='Curr Date info : 2021-01-01'


sysinfo='sysinfo'
sysinfo_version=seastone_diag_version
sysinfo_help=['usage: ./cel-sysinfo-test \[OPTIONS\]',
       'Options are:',
       '--all           Test all configure options',
       '-s, --status        Show sysinfo presence and type',
       '-v, --verion        Display the version and exit',
       '-h, --help          Display this help text and exit',
       '-l, --list          List yaml info',
       '-b, --bmc           bmc data',
       '-f, --file          Specify the yaml configure file',
       '-d, --dev           device id']

sysinfo_list=['  1 | BIOS',
  '2 | FPGA',
  '3 | Baseboard CPLD',
  '4 | Switch_CPLD1',
  '5 | Switch_CPLD2',
  '6 | COME CPLD',
  '7 | Fan CPLD',
  '8 | OS',
  '9 | Diag',
 '10 | ONIE']


usb='usb'
usb_version=seastone_diag_version
usb_help=['Options are:',
         '-l, --list          List yaml info',
         '-t, --type          Type to distinguish ssd and usb test',
         '-d, --dev           ',
         '-C, --count         \[count num: MB unit\]',
         '-w, --write         Write random data to dev path',
         '-f, --file          Specify the yaml configure file',
         '-b, --bmc           bmc mode',
         '-v, --version       Display the version and exit',
         '-h, --help          Display this help text and exit',
         '    --all           Test all configure options']

usb_list=[' dev1_name : usb1',
 'type : nand',
 'size : 16',
 'dev_path : /dev/sdb1',
 'dev_id : 1',
 'source_file: /dev/urandom',
 'save_path: /root/']




bios_primary='ipmitool raw 0x3a 0x25 0x00'
bios_secondary='ipmitool raw 0x3a 0x25 0x01'


#tc5
eeprom='eeprom'
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
eeprom_version=seastone_diag_version


#tc13
pci='pci'
pci_version=seastone_diag_version
pci_help=['Options are:',
    '-V, --verbose    Verbose',
    '-v, --version    Version',
    '-h, --help       Show this help text',
    '-l, --list       list config',
    '-s, --scan       Scan the specific pcie device',
    '-a, --all        Test all configure options',
    '-r, --read       Read the PCIe Configuration Register',
    '-w, --write      Write the PCIe Configuration Register',
    '-d, --dev        the BDF of the device',
    '-R, --reg        Register address',
    '-W, --width      The width of data, use \(\'b\', \'w\' or \'l\'\) to indicate \(1, 2, or 4 bytes width\)',
    '-D, --data       The value of data',
    '-P, --pipe       PCIe pipe name']

pci_list=['Intel Corporation Device.*Co-processor',
        'Broadcom Corporation Device                      .*Eth',
        'Xilinx Corporation Device                        .*Memory controller',
        'Intel Corporation I210 Gigabit Network Connection.*Eth',
        'Intel Corporation Device                         .*Eth']


storage='storage'
storage_version=seastone_diag_version
storage_help=['Options are:',
         '-l, --list          List yaml info',
         '-t, --type          Type to distinguish ssd and usb test',
         '-d, --dev           \[dev id 1..n: 1:ssd, 2:u disk\]',
         '-C\, --count         \[count num: MB unit\]',
         '-w\, --write         Write random data to dev path',
         '-f\, --file          Specify the yaml configure file',
         '-b\, --bmc           bmc mode',
         '-v\, --version       Display the version and exit',
         '-h\, --help          Display this help text and exit',
         '    --all           Test all configure options']

mcinfo =['Firmware Revision         : '+seastone_bmc,
         'Manufacturer ID           : 12290',
         'Product ID                : 4039']

uart='uart'
uart_list = ['ttyS0    115200',
        'ttyS1      9600']
uart_version=seastone_diag_version
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

temp='temp'


tpm='tpm'

cpu_proc_info=['processor       : 0',
        'model name      : ARMv6-compatible processor rev 7 \(v6l\)',
        'CPU implementer : 0x41',
        'CPU architecture: 7',
        'CPU variant     : 0x0',
        'CPU part        : 0xb76',
        'CPU revision    : 7',
        'Hardware        : Generic DT based system']

fan='fan'
psu='psu'

url = 'http://10.208.29.3:8080/SEASTONE/download.sh'
