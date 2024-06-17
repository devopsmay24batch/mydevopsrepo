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



uboot_prompt = dev_info.promptUboot

tftp_server_ipv4 = pc_info.managementIP
tftp_interface = dhcp_interface = mgmt_interface = "eth0"
# mgmt_server_ip = pc_info.managementIP

BRIXIA = SwImage.getSwImage("BRIXIA_DIAG")
brixia_diag_version=BRIXIA.newVersion
brixia_old_diag_version=BRIXIA.oldVersion
brixia_ver= BRIXIA.newImage



####TC 10####

pci_help=['Options are:',
            '--all                   Do test all',
        '-l, --list                  Display the yaml configure file',
        '-f, --file  \[config_file\]   Specify the yaml configure file',
        '-v, --version               Display the version and exit',
        '-h, --help                  Display this help text and exit']


pci_list_mtp =['1.*Intel Xeon Processor.*CPU',
           '2.*X552 10 GbE SFP+.*Eth',
           '3.*X552 10 GbE SFP+.*Eth',
           '4.*X552 10 GbE SFP+.*Eth',
                   '5.*X552 10 GbE SFP+.*Eth',
           '6.*Micron Technology Inc Device.*NVMe',
           '7.*Micron Technology Inc Device.*NVMe',
           '8.*Mellanox Technologies MT27800.*Eth',
           '9.*Mellanox Technologies MT27800.*Eth']

pci_list =['1.*Intel Xeon Processor.*CPU',
           '2.*X552 10 GbE SFP+.*Eth',
           '3.*X552 10 GbE SFP+.*Eth',
           '4.*X552 10 GbE SFP+.*Eth',
                   '5.*X552 10 GbE SFP+.*Eth',
           '6.*I210 Gigabit Network Connection.*Eth',
           '7.*I210 Gigabit Network Connection.*Eth',
           '8.*Broadcom Device b996.*Switch-chip',
           '9.*Google, Inc. Device 0065.*FPGA']

pci_version= brixia_diag_version
pci = "pci"
lspci = ['01:00.0 Ethernet controller: Broadcom Limited Device b996 \(rev .*1\)',
'03:00.0 Co-processor: Intel Corporation Xeon Processor D Family QuickAssist Technology',
'Ethernet controller: Intel Corporation Ethernet Connection X552 10 GbE SFP+',
'Ethernet controller: Intel Corporation Ethernet Connection X552 10 GbE SFP+',
'Ethernet controller: Intel Corporation Ethernet Connection X552 10 GbE SFP+',
'Ethernet controller: Intel Corporation Ethernet Connection X552 10 GbE SFP+',
'System peripheral: Google, Inc. Device 0065',
'Ethernet controller: Intel Corporation I210 Gigabit Network Connection \(rev 03\)',
'Ethernet controller: Intel Corporation I210 Gigabit Network Connection \(rev 03\)']

lspci_mtp=['00:00.0 Host bridge: Intel Corporation Xeon E7 v4/Xeon E5 v4/Xeon E3 v4/Xeon D DMI2',
        '00:01.0 PCI bridge: Intel Corporation Xeon E7 v4/Xeon E5 v4/Xeon E3 v4/Xeon D PCI Express Root Port 1',
        '00:02.0 PCI bridge: Intel Corporation Xeon E7 v4/Xeon E5 v4/Xeon E3 v4/Xeon D PCI Express Root Port 2',
        '00:03.0 PCI bridge: Intel Corporation Xeon E7 v4/Xeon E5 v4/Xeon E3 v4/Xeon D PCI Express Root Port 3',
        '00:04.0 System peripheral: Intel Corporation Xeon E7 v4/Xeon E5 v4/Xeon E3 v4/Xeon D Crystal Beach DMA Channel 0',
        '00:05.0 System peripheral: Intel Corporation Xeon E7 v4/Xeon E5 v4/Xeon E3 v4/Xeon D Map/VTd_Misc/System Management',
        '00:14.0 USB controller: Intel Corporation 8 Series/C220 Series Chipset Family USB xHCI',
        '00:1d.0 USB controller: Intel Corporation 8 Series/C220 Series Chipset Family USB EHCI',
        '00:1f.0 ISA bridge: Intel Corporation C224 Series Chipset Family Server Standard SKU LPC Controller',
        '01:00.0 Serial Attached SCSI controller: LSI Logic / Symbios Logic SAS3008 PCI-Express Fusion-MPT SAS-3',
        '02:00.0 Co-processor: Intel Corporation Xeon Processor D Family QuickAssist Technology',
        '04:00.0 Ethernet controller: Intel Corporation Ethernet Connection X552 10 GbE SFP+',
        '06:00.0 Ethernet controller: Intel Corporation Ethernet Connection X552 10 GbE SFP+',
        '08:00.0 Ethernet controller: Mellanox Technologies MT27800 Family',
        'ff:0b.0 System peripheral: Intel Corporation Xeon E7 v4/Xeon E5 v4/Xeon E3 v4/Xeon D R3 QPI Link',
        'ff:0c.0 System peripheral: Intel Corporation Xeon E7 v4/Xeon E5 v4/Xeon E3 v4/Xeon D Caching Agent',
        'ff:0f.0 System peripheral: Intel Corporation Xeon E7 v4/Xeon E5 v4/Xeon E3 v4/Xeon D Caching Agent',
        'ff:10.0 System peripheral: Intel Corporation Xeon E7 v4/Xeon E5 v4/Xeon E3 v4/Xeon D R2PCIe Agent',
        'ff:12.0 System peripheral: Intel Corporation Xeon E7 v4/Xeon E5 v4/Xeon E3 v4/Xeon D Home Agent 0',
        'ff:13.0 System peripheral: Intel Corporation Xeon E7 v4/Xeon E5 v4/Xeon E3 v4/Xeon D Memory Controller 0',
        'ff:14.0 System peripheral: Intel Corporation Xeon E7 v4/Xeon E5 v4/Xeon E3 v4/Xeon D Memory Controller 0',
        'ff:15.0 System peripheral: Intel Corporation Xeon E7 v4/Xeon E5 v4/Xeon E3 v4/Xeon D Memory Controller 0',
        'ff:1e.0 System peripheral: Intel Corporation Xeon E7 v4/Xeon E5 v4/Xeon E3 v4/Xeon D Power Control Unit',
        'ff:1f.0 System peripheral: Intel Corporation Xeon E7 v4/Xeon E5 v4/Xeon E3 v4/Xeon D Power Control Unit']
############# TCS 12 ##############

adapter_list = [
    "Adapter: i2c-10000-mux (chan_id 1)",
    "Adapter: i2c-10000-mux (chan_id 1)",
    "Adapter: i2c-11-mux (chan_id 2)",
    "Adapter: ISA adapter",
    "Adapter: i2c-10000-mux (chan_id 0)",
    "Adapter: ISA adapter",
    "Adapter: ISA adapter",
    "Adapter: i2c-ocores",
    "Adapter: i2c-10000-mux (chan_id 0)",
    "Adapter: ISA adapter",
    "Adapter: ISA adapter",
    "Adapter: i2c-ocores",
    "Adapter: iMC socket 0 for channel pair 0-1",
    "Adapter: ISA adapter",
    "Adapter: i2c-10000-mux (chan_id 1)",
    "Adapter: i2c-10000-mux (chan_id 0)",
    "Adapter: i2c-10000-mux (chan_id 1)",
    "Adapter: i2c-11-mux (chan_id 0)",
    "Adapter: ISA adapter",
    "Adapter: i2c-10000-mux (chan_id 0)",
    "Adapter: i2c-11-mux (chan_id 1)",
    "Adapter: ISA adapter",
    "Adapter: i2c-ocores",
    "Adapter: iMC socket 0 for channel pair 0-1",
    "Adapter: ISA adapter",
    "Adapter: ISA adapter",
    "Adapter: ISA adapter",
    "Adapter: i2c-10000-mux (chan_id 1)",
    "Adapter: i2c-11-mux (chan_id 3)",
    "Adapter: ISA adapter",
    "Adapter: i2c-10000-mux (chan_id 0)"
]

adapter_list_mtp= [
    "Adapter: i2c-ocores",
    "Adapter: iMC socket 0 for channel pair 0-1",
    "Adapter: ISA adapter",
    "Adapter: i2c-ocores",
    "Adapter: iMC socket 0 for channel pair 0-1"
]

#############TCS 14##############
cpld_help = ['Options are:',
        '--all             Test all configure options',
    '-l, --list            Show device list',
    '-d, --dev             Test device id id',
    '-v, --version         Show diag version',
    '-h, --help            Display this help text and exit'

]

cpld = "cpld"
cpld_list = ['1 | version',
              '2 | scratch']

cpld_version= brixia_diag_version


#####tcs 44 ####
stress_help = [ '-M mbytes        megabytes of ram to test',
 '--reserve-memory If not using hugepages, the amount of memory to  reserve for the system',
 '-H mbytes        minimum megabytes of hugepages to require',
 '-s seconds       number of seconds to run',
 '-m threads       number of memory copy threads to run',
 '-i threads       number of memory invert threads to run',
 '-C threads       number of memory CPU stress threads to run',
 '--findfiles      find locations to do disk IO automatically',
 '-d device        add a direct write disk thread with block device \(or file\) \'device\'',
 '-f filename      add a disk thread with tempfile \'filename\'',
 '-l logfile       log output to file \'logfile\'',
 '--no_timestamps  do not prefix timestamps to log messages',
 '--max_errors n   exit early after finding \'n\' errors',
 '-v level         verbosity \(0-20\), default is 8',
 '--printsec secs  How often to print \'seconds remaining\'',
 '-W               Use more CPU-stressful memory copy',
 '-A               run in degraded mode on incompatible systems',
 '-p pagesize      size in bytes of memory chunks',
 '--filesize size  size of disk IO tempfiles',
 '-n ipaddr        add a network thread connecting to system at \'ipaddr\'',
 '--listen         run a thread to listen for and respond to network threads.',
 '--no_errors      run without checking for ECC or other errors',
 '--force_errors   inject false errors to test error handling',
 '--force_errors_like_crazy   inject a lot of false errors to test error handling',
 '-F               don\'t result check each transaction',
 '--stop_on_errors  Stop after finding the first error.',
 '--read-block-size     size of block for reading \(-d\)',
 '--write-block-size    size of block for writing \(-d\). If not defined, the size of block for writing will be defined as the size of block for reading',
 '--segment-size   size of segments to split disk into \(-d\)',
 '--cache-size     size of disk cache \(-d\)',
 '--blocks-per-segment  number of blocks to read\/write per segment per iteration \(-d\)',
 '--read-threshold      maximum time \(in us\) a block read should take \(-d\)',
 '--write-threshold     maximum time \(in us\) a block write should take \(-d\)',
 '--random-threads      number of random threads for each disk write thread \(-d\)',
 '--destructive    write\/wipe disk partition \(-d\)',
 '--monitor_mode   only do ECC error polling, no stress load.',
 '--cc_test        do the cache coherency testing',
 '--cc_inc_count   number of times to increment the cacheline\'s member',
 '--cc_line_count  number of cache line sized datastructures to allocate for the cache coherency threads to operate',
 '--cc_line_size   override the auto-detected cache line size',
 '--cpu_freq_test  enable the cpu frequency test \(requires the --cpu_freq_threshold argument to be set\)',
 '--cpu_freq_threshold  fail the cpu frequency test if the frequency goes below this value \(specified in MHz\)',
 '--cpu_freq_round round the computed frequency to this value, if set to zero, only round to the nearest MHz',
 '--paddr_base     allocate memory starting from this address',
 '--pause_delay    delay \(in seconds\) between power spikes',
 '--pause_duration duration \(in seconds\) of each pause',
 '--local_numa     choose memory regions associated with each CPU to be tested by that CPU',
 '--remote_numa    choose memory regions not associated with each CPU to be tested by that CPU',
 '--channel_hash   mask of address bits XORed to determine channel. Mask 0x40 interleaves cachelines between channels',
 '--channel_width bits     width in bits of each memory channel']

#########################TCS 34 #######################################
th4_help = ['Options are:',
       '--all             Test all configure options',
    '-f, --file            Defined configuration file',
    '-l, --list            Show device list',
    '-d, --dev             Test device id id',
    '-v, --version         Show diag version',
    '-h, --help            Display this help text and exit']

th4_version = brixia_diag_version
th4_list= ['1.*|.*device_id.*00.*0x14E4.*W',
        '2.*|.*vendor_id.*02.*0xB996.*W',
        '3.*|.*revision_id.*08 .*0x01.*B']
write_mac_pattern="Updating Mac Address to 00A0C9121220...Done."
read_mac_pattern="5: LAN MAC Address is .*"


#####TC 09  #########
fpga = "fpga"
fpga_help= ['usage: ./cel-fpga-test \[OPTIONS\]',
        'Options are:',
        '--all             Test all configure options',
        '--loop            Test with loop counts',
    '-l, --list            Show device list',
    '-d, --dev             Test device id id',
    '-v, --version         Show diag version',
    '-h, --help            Display this help text and exit']
fpga_list =  ['fpga_sysfs_path: /sys/devices/gfpga-platform',
             'id | device name',
             '1 | deviceid',
             '2 | majorrevision',
             '3 | minorrevision',
             '4 | scratch']

fpga_version = brixia_diag_version

i2cdetect_list_mtp=['i2c-3.*smbus.*i2c-0-mux \(chan_id 1\).*SMBus adapter',\
'i2c-10.*smbus.*iMC socket 0 for channel pair 0-1.*SMBus adapter',\
'i2c-1.*i2c.*i2c-ocores.*I2C adapter',\
'i2c-8.*smbus.*i2c-0-mux \(chan_id 6\).*SMBus adapter',\
'i2c-6.*smbus.*i2c-0-mux \(chan_id 4\).*SMBus adapter',\
'i2c-4.*smbus.*i2c-0-mux \(chan_id 2\).*SMBus adapter',\
'i2c-11  smbus           iMC socket 0 for channel pair 2-3.*SMBus adapter',\
'i2c-2.*smbus.*i2c-0-mux \(chan_id 0\).*SMBus adapter',\
'i2c-0.*smbus.*SMBus I801 adapter at 0780.*SMBus adapter',\
'i2c-9.*smbus.*i2c-0-mux \(chan_id 7\).*SMBus adapter',\
'i2c-7.*smbus.*i2c-0-mux \(chan_id 5\).*SMBus adapter',\
'i2c-5.*smbus.*i2c-0-mux \(chan_id 3\).*SMBus adapter']


i2cdetect_list = ['i2c-3.*smbus.*i2c-0-mux.*SMBus adapter',
'i2c-10102.*i2c.*i2c-10100-mux.*I2C adapter',
'i2c-10130.*i2c.*i2c-10100-mux.*I2C adapter',
'i2c-20.*i2c.*i2c-11-mux.*I2C adapter',
'i2c-10120.*i2c.*i2c-10100-mux.*I2C adapter',
'i2c-10  i2c.*i2c-ocores.*.*I2C adapter',
'i2c-10110.*i2c.*i2c-10100-mux.*I2C adapter',
'i2c-1   i2c.*i2c-ocores.*.*I2C adapter',
'i2c-10100.*i2c.*GFPGA adapter.*I2C adapter',
'i2c-29  smbus.*iMC socket.*SMBus adapter',
'i2c-10129.*i2c.*i2c-10100-mux.*I2C adapter',
'i2c-19  i2c.*i2c-10-mux.*I2C adapter',
'i2c-10119.*i2c.*i2c-10100-mux.*I2C adapter',
'i2c-10109.*i2c.*i2c-10100-mux.*I2C adapter',
'i2c-27  i2c.*i2c-11-mux.*I2C adapter',
'i2c-10127.*i2c.*i2c-10100-mux.*I2C adapter',
'i2c-10004.*i2c.*i2c-10000-mux.*I2C adapter',
'i2c-17  i2c.*i2c-10-mux.*I2C adapter',
'i2c-10117.*i2c.*i2c-10100-mux.*I2C adapter',
'i2c-8   smbus.*i2c-0-mux.* SMBus adapter',
'i2c-10107.*i2c.*i2c-10100-mux.*I2C adapter',
'i2c-25  i2c.*i2c-11-mux.*I2C adapter',
'i2c-10125.*i2c.*i2c-10100-mux.*I2C adapter',
'i2c-10002.*i2c.*i2c-10000-mux.*I2C adapter',
'i2c-15  i2c.*i2c-10-mux .*I2C adapter',
'i2c-10115.*i2c.*i2c-10100-mux.*I2C adapter',
'i2c-6   smbus.*i2c-0-mux.*SMBus adapter',
'i2c-10105.*i2c.*i2c-10100-mux.*I2C adapter',
'i2c-10133.*i2c.*i2c-10100-mux.*I2C adapter',
'i2c-23  i2c.*i2c-11-mux.*I2C adapter',
'i2c-10123.*i2c.*i2c-10100-mux.*I2C adapter',
'i2c-10000.*i2c.*GFPGA adapter.*I2C adapter',
'i2c-13  i2c.*i2c-10-mux.*I2C adapter',
'i2c-10113.*i2c.*i2c-10100-mux.*I2C adapter',
'i2c-4   smbus.*i2c-0-mux.* SMBus adapter',
'i2c-10103.*i2c.*i2c-10100-mux.*I2C adapter',
'i2c-10131.*i2c.*i2c-10100-mux.*I2C adapter',
'i2c-21  i2c.*i2c-11-mux.*I2C adapter',
'i2c-10121.*i2c.*i2c-10100-mux.*I2C adapter',
'i2c-11  i2c.*i2c-ocores.*I2C adapter',
'i2c-10111.*i2c.*i2c-10100-mux.*I2C adapter',
'i2c-2   smbus.*i2c-0-mux.* SMBus adapter',
'i2c-10101.*i2c.*i2c-10100-mux.*I2C adapter',
'i2c-0   smbus.*SMBus I801 adapter at 0780.*SMBus adapter',
'i2c-28  smbus.*iMC socket 0 for channel pair 0-1.*SMBus adapter',
'i2c-10128.*i2c.*i2c-10100-mux.*I2C adapter',
'i2c-18  i2c.*i2c-10-mux.*I2C adapter',
'i2c-10118.*i2c.*i2c-10100-mux.*I2C adapter',
'i2c-9   smbus.*i2c-0-mux.* SMBus adapter',
'i2c-10108.*i2c.*i2c-10100-mux.*I2C adapter',
'i2c-26  i2c.*i2c-11-mux.*I2C adapter',
'i2c-10126.*i2c.*i2c-10100-mux.*I2C adapter',
'i2c-10003.*i2c.*i2c-10000-mux.*I2C adapter',
'i2c-16  i2c.*i2c-10-mux.*I2C adapter',
'i2c-10116.*i2c.*i2c-10100-mux.*I2C adapter',
'i2c-7   smbus.*i2c-0-mux.*SMBus adapter',
'i2c-10106.*i2c.*i2c-10100-mux.*I2C adapter',
'i2c-10134.*i2c.*i2c-10100-mux.*I2C adapter',
'i2c-24  i2c.*i2c-11-mux.*I2C adapter',
'i2c-10124.*i2c.*i2c-10100-mux.*I2C adapter',
'i2c-10001.*i2c.*i2c-10000-mux.*I2C adapter',
'i2c-14  i2c.*i2c-10-mux.*I2C adapter',
'i2c-10114.*i2c.*i2c-10100-mux.*I2C adapter',
'i2c-5   smbus.*i2c-0-mux.*SMBus adapter',
'i2c-10104.*i2c.*i2c-10100-mux.*I2C adapter',
'i2c-10132.*i2c.*i2c-10100-mux.*I2C adapter',
'i2c-22  i2c.*i2c-11-mux.*I2C adapter',
'i2c-10122.*i2c.*i2c-10100-mux.*I2C adapter',
'i2c-12  i2c.*i2c-10-mux.*I2C adapter',
'i2c-10112.*i2c.*i2c-10100-mux.*I2C adapter']
major= "3"
minor= "10"
scratch = "0"
fpga_sdk= ['Broadcom Command Monitor',
           'Release: sdk-6.5.26',
           'Platform: X86',
           'OS: Unix']
temp_version=brixia_diag_version
temp="temp"
temp_list = []
for i in range(1,27):
    temp_list.append("dev id:.*"+str(i))


temp_list_mtp=[]
for i in range(1,5):
    temp_list_mtp.append("dev id:.*"+str(i))

temp_help=['Options are:',
     '--all           Test all configure options', 
 '-f, --file          Defined configuration file', 
 '-r, --read          Read option',
 '-v, --version       Display the version and exit', 
 '-h, --help          Display this help text and exit',
 '-l, --list          List yaml info',
 '-d, --dev           dev id: run ./cel-temp-test -l .*id']


psu_version=brixia_diag_version
psu="psu"

psu_list = []
for i in range(1,17):
    psu_list.append("dev:.*"+str(i))

psu_list_mtp = []
for i in range(1,4):
    psu_list_mtp.append("dev:.*"+str(i))



psu_help=['Options are:', 
     '--all           Test all configure options', 
 '-f, --file          Defined configuration file', 
 '-r, --read          Read option', 
 '-v, --version       Display the version and exit', 
 '-h, --help          Display this help text and exit',
 '-l, --list          List yaml info',
 '-d, --dev           See device id by ./cel-psu-test -l command']

memory_spd_list=["# dmidecode 3.2",
"Getting SMBIOS data from sysfs.",
"SMBIOS 3.0 present.",
"Handle 0x0004, DMI type 16, 23 bytes",
"Physical Memory Array",
"Location: System Board Or Motherboard",
"Use: System Memory",
"Error Correction Type: Single-bit ECC",
"Maximum Capacity: 64 GB",
"Error Information Handle: Not Provided",
"Number Of Devices: 2",
"Manufacturer: Hynix Semiconductor",
'Type: DDR4',
'Form Factor: SODIMM',
'Maximum Voltage: 1.2 V']

qsfp_help=['Options are:', 
     '-a  --all.* Test all configure options', 
     '--lpmode.* Set OSFP low power mode to all ports',
     '--hpmode.* Set OSFP high power mode to all ports',
     '-l, --list.* List brief information',
     '-h, --help.* Display this help text and exit']

qsfp_list=["osfp num:.*","sfp+ num:.*","osfp:name.*","sfp+:name","sfp+:name"]

lp_mode_pattern=["Set OSFP all ports to low power mode",
"OSFP LED must change to be green color"]

hp_mode_pattern=["Set OSFP all ports to high power mode",
"OSFP LED must change to be red color"]

qsfp_all_pattern="OSFP.* 32.*Present.*Amphenol.*NLMAME-G104.*"




sysinfo_help=['Options are:',
        '--all.* Test all configure options',
        '-l, --list.* Show device list',
        '-d, --dev.* Device id',
        '-h, --help.* Display this help text and exit']

sysinfo_list_mtp=["id | device name",
 "1 | BIOS",
 "2 | COME CPLD",
 "3 | OS",
 "4 | Diag",
 "5 | SONiC",
 "6 | UCD9090 COMe"]

sysinfo_list=["id | device name",
 "1 | BIOS",
 "2 | Baseboard CPLD",
 "3 | COME CPLD",
 "4 | OS",
 "5 | Diag",
 "6 | SONiC",
 "7 | FPGA",
 "8 | UCD9090 COMe",
 "9 | UCD9090 Baseboard"]

eeprom_tool=['come','baseboard','fan-1','fan-2','fan-3','fan-4']
eeprom="eeprom"

eeprom_write_pattern="Enable write protect: Done"
eeprom_read_pattern=["product_name: Celestica_test","psu_type: DC","00000800"]
eeprom_list=["group:1"]
eeprom_help=['Options are:',
'--all.* Test all configure options',
'--dump.* Dump eeprom info',
 '-v, --version.* Display the version and exit',
 '-h, --help.* Display this help text and exit',
 '-f, --file.* Defined configuration file',
 '-l, --list.* List yaml information',
 '-d, --dev.* run -l for see all device id',
 '-t, --type.*',
 '-D, --data.*',
 '-A, --addr.* run -l to see support address']

eeprom_version= brixia_diag_version
bb_cpld_version= brixia_diag_version
bb_cpld="bb-cpld"

bb_cpld_list=['cpld_sysfs_path: /sys/devices/platform/mmcpld/mmc_reg.3.auto',
'id | device name',
' 1 | version_major',
' 2 | version_minor',
' 3 | xp48r0v_swap_pgd',
' 4 | xp12r0v_bb_pgd',
' 5 | xp12r0v_fan1_pgd',
' 6 | xp12r0v_fan2_pgd',
' 7 | xp12r0v_fan3_pgd',
' 8 | xp12r0v_fan4_pgd',
' 9 | xp3r3v_pgd',
'10 | xp3r3v_ssd_pgd',
'11 | xp3r3v_stby_pgd',
'12 | sw_power_good',
'13 | i210_1_pwr_good',
'14 | i210_2_pwr_good',
'15 | xp12r0v_bb_alt',
'16 | xp12r0v_sw_alt',
'17 | xp48r0v_swap_alt',
'18 | xp48r0v_swap_alt2',
'19 | i210_1_alrt_l',
'20 | i210_2_alrt_l',
'21 | batlow_l',
'22 | brd_version',
'23 | switch_brd_type',
'24 | ucd_pmb_alt_l',
'25 | ucd_pwr_ok',
'26 | scratch']

bb_cpld_help=['--all.* Test all configure options',
    '-l, --list.* Show device list',
    '-d, --dev.* Test device id id',
    '-v, --version.* Show diag version',
    '-h, --help.* Display this help text and exit']

bb_cpld_all_pattern=[]

bb_cpld_dev_pattern=["dev_id: 1","register name: version_major",
"Test access cpld version_major register:",
"Read value: 0x00","cpld test : Passed"]




###TCS 38 ####


mem164 = 600
mem28= 57600
mem ='./memtester 164 1'
memory28='./memtester 28G 4'


######################tcs05#############
upgrade='upgrade'
upgrade_version=brixia_diag_version
upgrade_help=['Options are:',
         '--update     Update single firmware',
        '-v, --version    Display the version and exit',
        '-l, --list       Show configuration list',
        '-d, --dev\[1-5\]   \[1:BIOS\|2:COMe CPLD\|3:FPGA\|4:Baseboard CPLD\|5:Coreboot\]',
        '-f, --file       Update  the firmware file image',
        '-h, --help       Display this help text and exit']
upgrade_list=['*** 01 |device name : BIOS',
               '*** 02 |device name : COMe_CPLD',
               '*** 03 |device name : FPGA',
               '*** 04 |device name : Baseboard_CPLD',
               '*** 05 |device name : COREBOOT']


######################################################
#########################TCS 33 #######################################
th4_help = ['Options are:',
       '--all             Test all configure options',
    '-f, --file            Defined configuration file',
    '-l, --list            Show device list',
    '-d, --dev             Test device id id',
    '-v, --version         Show diag version',
    '-h, --help            Display this help text and exit']

th4_version = brixia_diag_version
th4_list= ['1.*|.*device_id.*00.*0x14E4.*W',
        '2.*|.*vendor_id.*02.*0xB996.*W',
        '3.*|.*revision_id.*08 .*0x01.*B']


#########################tcs 34################
all='all'
all_help= ['Options are:',
       ' --all               Run all test',
    '-l, --list          List config',
    '-h, --help          Display this help text and exit']

all_list=['./cel-sysinfo-test.*|.*--all.*|.*all test',
 './cel-cpld-test      |.*   -a |.*all test |',
 './cel-bb-cpld-test.*|.*--all |.*all test |',
 './cel-cpu-test.*|.*--all |.*all test |',
 './cel-fpga-test.* |.*--all |.*all test |',
 './cel-fan-test.*|.*--all |.*all test |',
 './cel-eeprom-test.*|.*--all |  write TLV eeprom |',
 './cel-i2c-test.*|.*--all |.*all test |',
 './cel-led-test.*|.*--all |.*all test |',
 './cel-mem-test.*|.*--all |.*all test |',
 './cel-storage-test   |.*--all |.*all test |',
 './cel-pci-test.*|.*--all |.*all test |',
 './cel-psu-test.*|.*--all |.*all test |',
 './cel-phy-test.*|.*--all |.*all test |',
 './cel-qsfp-test.*|.*--all |   all test  |',
 './cel-rtc-test.*|.*--all |.*all test |',
 './cel-temp-test.*|.*--all |.*all test |',
 './cel-uart-test.*|.*--all |.*all test |']

all_list_mtp=['./cel-sysinfo-test.*|.*--all.*|.*all test',
 './cel-cpld-test      |.*   -a |.*all test |',
 './cel-cpu-test.*|.*--all |.*all test |',
 './cel-eeprom-test.*|.*--all |  write TLV eeprom |',
 './cel-i2c-test.*|.*--all |.*all test |',
 './cel-mem-test.*|.*--all |.*all test |',
 './cel-storage-test   |.*--all |.*all test |',
 './cel-psu-test.*|.*--all |.*all test |',
 './cel-rtc-test.*|.*--all |.*all test |',
 './cel-temp-test.*|.*--all |.*all test |']

########TCS35
struct_mtp=[ '|configs',
 '| |mem.yaml',
 '| |psu.yaml',
 '| |macs.yam',
 '| |cplds.yaml',
 '| |storage.yaml',
 '| |i2cs.yaml',
 '| |version',
 '| |sysinfo.yaml',
 '| |all.yaml',
 '| |pcis_edk2.yaml',
 '| |gpio.yaml',
 '| |upgrade.yaml',
 '| |uart.yaml',
 '| |eeprom.yaml',
 '| |cpu.yaml',
 '| |temp.yaml',
 '| |rtc.yaml',
 '| |pcis.yaml',
 '| |pcis_coreboot.yaml',
 '|log',
 '|tools',
 '| |mcelog_147+dfsg-1_amd64.deb',
 '| |mprime',
 '| |smartctl',
 '| |set_hpmode.sh',
 '| |libcel_yaml.so',
 '| |eeupdate64e',
 '| |baseboard_voltage_margin.sh',
 '| |afulnx_64',
 '| |mcelog',
 '| |set_all_led_blue.sh',
 '| |io_rd_wr.py',
 '| |come_voltage_margin.sh',
 '| |pktgen',
 '| |pmbus_margin.py',
 '| |bin_file_tool',
 '| |inteltool',
 '| |ispvm',
 '| |BDXNS_SFP_PLUS_NO_MNG_LED_LO_LAN0_2p00_800008D9.bin',
 '| |set_all_led_default.sh',
 '| |prime.txt',
 '| |optictemputil.py',
 '| |dmidecode',
 '| |stress',
 '| | |SSD_test.sh',
 '| | |CPU_test.sh',
 '| | |CPU_DDR_SSD_I2C',
 '| | | |stress.cfg',
 '| | | |stress',
 '| | | |README',
 '| | |DDR_test.sh',
 '| | |PCIE_stress',
 '| | | |fpga_io',
 '| | | |FPGA',
 '| | | | |PCIE_CFG_R_stress',
 '| | | | |PCIE_BAR0_R_stress',
 '| | | | |fpga_stress.sh',
 '| | | | |PCIE_scratch_RW_stress',
 '| | | |pcimem',
 '| | | |README',
 '| | |test_SSD.log',
 '| | |diag_test.sh',
 '| | |CPU_test.log',
 '| | |README',
 '| | |NVME_test.sh',
 '| | |cpupower_test.sh',
 '| | |Lpmode',
 '| | | |Lpmode_test.sh',
 '| | | |README.txt',
 '| |fusion_config_updater.py',
 '| |BDXNS_SFP_PLUS_NO_MNG_LED_LO_LAN1_2p00_800008DA.bin',
 '| |fio',
 '| |lpc_cpld_x64_64',
 '| |local.txt',
 '| |iperf3_loopback_COME_EVT.sh',
 '| |CFUFLASH',
 '| |eltt2',
 '| |come_cpld_upgrade',
 '| |ipmi-fru-it',
 '| |mb_cpld_upgrade',
 '| |stressapptest',
 '| |decode-dimms',
 '| |iperf3_loopback.sh',
 '| |pcimem',
 '| |firmware',
 '| | |ELM.0.01.05.bin',
 '| | |capitaine-11-02-2021-4310-vendor.bios',
 '| | |BRIXIA_CPLD_V0b_20211217.vme',
 '| | |capitaine_ucd_rev04.csv',
 '| | |onie-recovery-x86_64-cel_brixia-r0.iso',
 '| | |doubledouble_03_0a.bin',
 '| | |COMe_CPLD_V16_20210901.vme',
 '| | |ELM.0.01.00.T12.bin',
 '| | |COMe_CPLD_V17_20211228.vme',
 '| | |capitaine-01-10-2022-vendor-6002.bios',
 '| |set_all_led_red.sh',
 '| |set_lpmode.sh',
 '| |hpmode',
 '| |timetobinary.sh',
 '| |memtester',
 '| |hpmode_celestic_eloopmode',
 '| |fpga_prog',
 '| |amifldrv_mod.o',
 '| |memtool',
 '|bin',
 '| |cel-cpu-test',
 '| |cel-mem-test',
 '| |cel-temp-test',
 '| |cel-rtc-test',
 '| |cel-all-test',
 '| |cel-amplitude-test',
 '| |cel-eeprom-test',
 '| |cel-sysinfo-test',
 '| |cel-storage-test',
 '| |cel-gpio-test',
 '| |cel-psu-test',
 '| |cel-i2c-test',
 '| |cel-upgrade-test',
 '| |cel-uart-test',
 '| |cel-pci-test',
 '| |cel-cpld-test',
 '|libs',
 '| |libcel_yaml.so',
 '| |libsctp1_1.0.18+dfsg-1_amd64.deb',
 '| |libyaml.so',
 '| |iperf3_3.6-2_amd64.deb',
 '| |libcel_yaml.a',
 '| |libiperf0_3.6-2_amd64.deb']

struct = ['|-tools',
'| |-stress',
'| | |-DDR_test.sh',
'| |-stressapptest',
'| | |-cpupower_test.sh',
'| | |-CPU_test.sh',
'| | |-SSD_test.sh',
'| | |-Lpmode',
'| | | |-README.txt',
'| | | |-Lpmode_test.sh',
'| | |-CPU_DDR_SSD_I2C',
'| | | |-stress',
'| | | |-stress.cfg',
'| | | |-README',
'| | |-README',
'| | |-NVME_test.sh',
'| | |-diag_test.sh',
'| | |-PCIE_stress',
'| | | |-fpga_io',
'| | | |-FPGA',
'| | | | |-PCIE_scratch_RW_stress',
'| | | | |-fpga_stress.sh',
'| | | | |-PCIE_BAR0_R_stress',
'| | | | |-PCIE_CFG_R_stress',
'| | | |-pcimem',
'| | | |-README',
'| |-io_rd_wr.py',
'| |-timetobinary.sh',
'| |-ispvm',
'| |-mprime',
'| |-optictemputil.py',
'| |-fusion_config_updater.py',
'| |-ipmi-fru-it',
'| |-iperf3_loopback_COME_EVT.sh',
'| |-bin_file_tool',
'| |-mcelog',
'| |-mb_cpld_upgrade',
'| |-set_lpmode.sh',
'| |-memtester',
'| |-set_hpmode.sh',
'| |-set_all_led_red.sh',
'| |-set_all_led_blue.sh',
'| |-decode-dimms',
'| |-set_all_led_default.sh',
'| |-come_cpld_upgrade',
'| |-CFUFLASH',
'| |-fpga_prog',
'| |-hpmode',
'| |-eeupdate64e',
#'| |-BDXNS_SFP_PLUS_NO_MNG_LED_LO_LAN1_2p00_800008DA.bin',
'| |-fio',
'| |-hpmode_celestic_eloopmode',
'| |-come_voltage_margin.sh',
'| |-amifldrv_mod.o',
'| |-memtool',
'| |-pktgen',
'| |-eltt2',
'| |-iperf3_loopback.sh',
'| |-lpc_cpld_x64_64',
'| |-pcimem',
'| |-mcelog_147+dfsg-1_amd64.deb',
'| |-baseboard_voltage_margin.sh',
'| |-BDXNS_SFP_PLUS_NO_MNG_LED_LO_LAN0_2p00_800008D9.bin',
'| |-smartctl',
'| |-pmbus_margin.py',
'| |.*libcel_yaml.so',
'| |-firmware',
#'| | |-ELM.0.01.00.T12.bin',
#'| | |-capitaine-11-02-2021-4310-vendor.bios',
#'| | |-doubledouble_03_0a.bin',
#'| | |-COMe_CPLD_V16_20210901.vme',
#'| | |-COMe_CPLD_V17_20211228.vme',
#'| | |-Brixia_baseboard_ucd_rev1.2.csv',
#'| | |-capitaine_ucd_rev04.csv',
#'| | |-BRIXIA_CPLD_V0b_20211217.vme',
#'| | |-ELM.0.01.05.bin',
#'| | |-capitaine-01-10-2022-vendor-6002.bios',
#'| | |-doubledouble_03_09.bin',
#'| | |-onie-recovery-x86_64-cel_brixia-r0.iso',
'| |-dmidecode',
'| |-afulnx_64',
'|-log',
'|-configs',
'| |-cplds.yaml',
'| |-qsfp.yaml',
'| |-pcis.yaml',
'| |-macs.yaml',
'| |-eeprom.yaml',
'| |-temp.yaml',
'| |-psu.yaml',
'| |-leds.yaml',
'| |-fpga.yaml',
'| |-pcis_linuxboot.yaml',
'| |-rtc.yaml',
'| |-psu_B0.yaml',
'| |-sysinfo.yaml',
'| |-all.yaml',
'| |-pcis_coreboot.yaml',
'| |-cpu.yaml',
'| |-upgrade.yaml',
'| |-bb_cplds.yaml',
'| |-phys.yaml',
'| |-mem.yaml',
'| |-storage_sonicSD.yaml',
'| |-storage.yaml',
'| |-i2cs.yaml',
'| |-uart.yaml',
'| |-detect_th4.yaml',
'| |-detect_th4_b0.yaml',
'| |-fans.yaml',
'| |-second_source',
'| | |-temp_astersyn.yaml',
'| | |-psu_B0_astersyn.yaml',
'| | |-psu_B0_flex.yaml',
'| | |-psu_astersyn.yaml',
'| | |-psu_flex.yaml',
'| | |-temp_flex.yaml',
'| |-version',
'|-bin',
'| |-cel-led-test',
'| |-cel-pci-test',
'| |-cel-psu-test',
'| |-cel-eeprom-test',
'| |-cel-temp-test',
'| |-cel-fpga-test',
'| |-cel-sysinfo-test',
'| |-log',
#'| | |-all_2022-01-10-03-40-27.log
#'| | |-all_2022-01-10-14-10-18.log
#'| | |-all_2022-01-10-04-41-48.log
#'| | |-all_2022-01-10-03-49-21.log
'| |-cel-upgrade-test',
'| |-cel-rtc-test',
'| |-cel-fan-test',
'| |-cel-qsfp-test',
'| |-cel-storage-test',
'| |-cel-all-test',
'| |-cel-cpu-test',
'| |-cel-mem-test',
'| |-cel-cpld-test',
'| |-cel-detect-th4-test',
'| |-cel-bb-cpld-test',
'| |-cel-uart-test',
'| |-cel-phy-test',
'| |-cel-i2c-test',
'|-libs',
'| |-libiperf0_3.6-2_amd64.deb',
'| |-libsctp1_1.0.18+dfsg-1_amd64.deb',
'| |-libyaml.so',
'| |-libcel_yaml.so',
'| |-iperf3_3.6-2_amd64.deb',
'| |-libcel_yaml.a']

power_margin=['baseboard_voltage_margin.sh','come_voltage_margin.sh','pmbus_margin.py']
fusion = 'fusion_config_updater.py'
scr_pat= 'SCRIPT_VERSION = 2.10'
config_var=['manufacturer: Celestica',
'product_name: UNIT_TEST',
'version: \'0.1.6\'',
'platform: Brixia']

config_var_mtp=['manufacturer: Celestica',
'product_name: UNIT_TEST',
'version: \'0.1.6\'',
'platform: Capitaine']


#####TC 11 #####
rtc = "rtc"
rtc_version = brixia_diag_version

rtc_help=['Options are:',
       '--all                   Do test all',
   '-r, --read                  Read operation',
   '-w, --write                 Write operation',
   '-D, --data <date>           Input the data of date & time \'YYYYMMDD HHMMSS\'',
   '-l, --list                  Display the yaml configure file',
   '-f, --file \[config_file\]    Specify the yaml configure file',
   '-v, --version               Display the version and exit',
   '-h, --help                  Display this help text and exit']

rtc_list=['.*1.*0.*0.*0.*0.*0.*0']

cpu_help = ['Options are:',
            '--all                       Do auto test.',
        '-l, --list                      Display the yaml configure file.',
        '-f, --file  \[config_file\]       Specify the yaml configure file.',
        '-v, --version                   Display the version and exit.',
        '-h, --help                      Display this help text and exit.']

cpu_list = ['CPU cores number:.*16',
'CPU max frequency value:.*3000',
'CPU Vendor ID:.*GenuineIntel',
'CPU Model name:.*Intel\(R\)Xeon\(R\)CPUD-1649N@2.30GHz']

cpu_version = brixia_diag_version
cpu = "cpu"

lscpu = ['Architecture:        x86_6',
        'CPU op-mode\(s\):.*32-bit, 64-bit',
        'Byte Order:          Little Endian',
        'CPU\(s\):              16',
        'Vendor ID:           GenuineIntel',
        'CPU family:          6',
        'Model:               86',
        'Model name:          Intel\(R\) Xeon\(R\) CPU D-1649N @ 2.30GHz',
        'Stepping:            5',
        'Virtualization:      VT-x']

cpu_proc=[]
for i in range(0,16):
    cpu_proc.append('processor.*:.*'+str(i))
    cpu_proc.append('vendor_id.*:.*GenuineIntel')
    cpu_proc.append('cpu family.*:.*6')
    cpu_proc.append('model.*:.*86')
    cpu_proc.append('model name.*:.*Intel\(R\) Xeon\(R\) CPU D-1649N @ 2.30GHz')
    cpu_proc.append('stepping.*:.*5')
    cpu_proc.append('microcode.*:.*0xe000014')
    cpu_proc.append('cpu cores.*:.*8')
    cpu_proc.append('fpu.*:.*yes')
    cpu_proc.append('fpu_exception.*:.*yes')
    cpu_proc.append('cpuid level.*:.*20')
    cpu_proc.append('wp.*:.*yes')


##TCS08

i2c_help = ['Options are:',
        '--all          Test all configure options',
        '--bus          \[i2c bus number. Run -l to see available bus\]',
        '--reg16        \[reg\] of 16bits address',
    '-R, --reg          \[reg\] of I2C device for 8bits address',
    '-r, --read         Read option',
    '-w, --write        Write option',
    '-D, --data         Data to write',
    '-A, --addr         \[addr\] device address',
    '-s, --scan         Scan the device under /dev/i2c-x',
    '-l, --list         List config yaml file',
    '-v, --version      Display the version and exit',
    '-h, --help         Display this help text and exit']

i2c_version = brixia_diag_version
i2c = "i2c"
i2c_list_mtp=['group:.*1,.*bus:.*3,.*type: pmbus',
'1.*0x56.*tlv_eeprom.*|.*      eeprom | /sys/bus/i2c/devices/3-0056 |',
'2.*0x70.*   PCA9543.*|.* i2c-bus-switch | /sys/bus/i2c/devices/3-0070 |',
'3.*0x44.*     PMBus.*|.*       pmbus | /sys/bus/i2c/devices/3-0044 |',
'group:  2,.*bus:.*1,.*type: i2c',
'1 |.*0x50.*|.*COME_EEPROM |.*eeprom | /sys/bus/i2c/devices/1-0050 |',
'2 |.*0x51.*|.*COME_EEPROM |.*eeprom | /sys/bus/i2c/devices/1-0051 |',
'3 |.*0x64.*|.*   VR_1.82V |.* power | /sys/bus/i2c/devices/1-0064 |',
'4 |.*0x66.*|.*   VR_1.05V |.* power | /sys/bus/i2c/devices/1-0066 |',
'5 |.*0x34.*|.*    UCD9090 |.* power | /sys/bus/i2c/devices/1-0034 |',
'group:  3,.*bus:.*0,.*type: cpu',
'1.*| 0x48 |.*  PMBus |.*pmbus | /sys/bus/i2c/devices/0-0048 |',
'2.*| 0x44 |.*  PMBus |.*pmbus | /sys/bus/i2c/devices/0-0044 |',
'3.*| 0x72 |.*PCA9548 |.*  I2C | /sys/bus/i2c/devices/0-0072 |']


i2c_list = ['group:  1,.*bus:.*0,.*type: cpu',
'1.*0x48.*/sys/bus/i2c/devices/0-0048',
'2.*0x44.*/sys/bus/i2c/devices/0-0044',
'3.*0x72.*/sys/bus/i2c/devices/0-0072',
'group:  2,.*bus:.*1,.*type: i2c',
'1.*|.*0x16.*|.*/sys/bus/i2c/devices/1-0016 |',
'2.*|.*0x17.*|.*/sys/bus/i2c/devices/1-0017 |',
'3.*|.*0x50.*|.*/sys/bus/i2c/devices/1-0050 |',
'4.*|.*0x51.*|.*/sys/bus/i2c/devices/1-0051 |',
'5.*|.*0x64.*|.*/sys/bus/i2c/devices/1-0064 |',
'6.*|.*0x66.*|.*/sys/bus/i2c/devices/1-0066 |',
'7.*|.*0x34.*|.*/sys/bus/i2c/devices/1-0034 |',
'group:  3,.*bus:.*10,.*type: cpu',
'1.*|.*0x75.*|.*/sys/bus/i2c/devices/10-0075',
'group:  4,   bus:     11,  type: cpu',
'1.*0x76.*/sys/bus/i2c/devices/11-0076',
'group:  5,   bus:     12,  type: sw-pca9548',
'1.*0x50.*fan1-eeprom.*/sys/bus/i2c/devices/12-0050',
'group:  6,   bus:     13,  type: sw-pca9548',
'1.*0x50.*/sys/bus/i2c/devices/13-0050',
'group:  7,   bus:     14,  type: sw-pca9548',
'1.*0x50.*/sys/bus/i2c/devices/14-0050',
'group:  8,   bus:     15,  type: sw-pca9548',
'1.*0x50.*/sys/bus/i2c/devices/15-0050',
'group:  9,   bus:     19,  type: sw-pca9548',
'1.*0x51.*/sys/bus/i2c/devices/19-0051',
'group: 10,   bus:     20,  type: sw-pca9548',
'1.*0x10.*/sys/bus/i2c/devices/20-0010',
'group: 11,   bus:     21,  type: sw-pca9548',
'1.*0x61.*/sys/bus/i2c/devices/21-0061',
'group: 12,   bus:     22,  type: sw-pca9548',
'1.*0x60.*/sys/bus/i2c/devices/22-0060',
'group: 13,   bus:     23,  type: sw-pca9548',
'1.*0x41.*/sys/bus/i2c/devices/23-0041',
'group: 14,   bus:  10001,  type: sw-pca9548',
'1.*0x44.*/sys/bus/i2c/devices/10001-0044',
'2.*0x60.*/sys/bus/i2c/devices/10001-0060',
'3.*0x53.*/sys/bus/i2c/devices/10001-0053',
'4.*0x54.*/sys/bus/i2c/devices/10001-0054',
'5.*0x55.*/sys/bus/i2c/devices/10001-0055',
'6.*0x50.*/sys/bus/i2c/devices/10001-0050',
'group: 15,   bus:  10002,  type: sw-pca9548',
'1.*0x51.*/sys/bus/i2c/devices/10002-0051',
'2.*0x52.*/sys/bus/i2c/devices/10002-0052',
'3.*0x62.*/sys/bus/i2c/devices/10002-0062',
'4.*0x63.*/sys/bus/i2c/devices/10002-0063',
'5.*0x5c.*/sys/bus/i2c/devices/10002-005c',
'group: 16,   bus:  10003,  type: sw-clkgen',
'1.*0x5b.*/sys/bus/i2c/devices/10003-005b',
'group: 17,   bus:  10004,  type: sw-clkgen',
'1.*0x5b.*/sys/bus/i2c/devices/10004-005b']

i2cbus_port = {'0': ['40: -- -- -- -- 44 -- -- -- 48 -- -- -- -- -- -- --','70: -- -- UU -- -- -- -- --'],
            '1': ['10: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --','30: -- -- -- -- UU -- -- -- -- -- -- -- -- -- -- --',
                  '50: UU UU -- -- -- -- -- -- 58 -- -- -- -- -- -- --','60: -- -- -- -- UU -- UU -- -- -- -- -- -- -- -- --'],
            '10': ['50: UU UU -- -- -- -- -- -- -- -- -- -- -- -- -- --','70: -- -- -- -- -- UU -- --'],
            '11': ['10: UU -- -- -- -- -- -- -- -- -- -- -- -- -- -- --','40: -- UU -- -- -- -- -- -- -- -- -- -- -- -- -- --',
                   '60: UU UU -- -- -- -- -- -- -- -- -- -- -- -- -- --','70: -- -- -- -- -- -- UU --'],
            '12': ['50: UU -- -- -- -- -- -- -- -- -- -- -- -- -- -- --','70: -- -- -- -- -- UU -- --'],
            '13': ['50: UU -- -- -- -- -- -- -- -- -- -- -- -- -- -- --','70: -- -- -- -- -- UU -- --'],
            '14': ['50: UU -- -- -- -- -- -- -- -- -- -- -- -- -- -- --','70: -- -- -- -- -- UU -- --'],
            '15': ['50: UU -- -- -- -- -- -- -- -- -- -- -- -- -- -- --','70: -- -- -- -- -- UU -- --'],
            '19': ['50: -- UU -- -- -- -- -- -- -- -- -- -- -- -- -- --','70: -- -- -- -- -- UU -- --'],
            '20': ['10: UU -- -- -- -- -- -- -- -- -- -- -- -- -- -- --','70: -- -- -- -- -- -- UU --'],
            '21': ['60: -- UU -- -- -- -- -- -- -- -- -- -- -- -- -- --','70: -- -- -- -- -- -- UU --'],
            '22': ['60: UU -- -- -- -- -- -- -- -- -- -- -- -- -- -- --','70: -- -- -- -- -- -- UU --'],
            '23': ['40: -- UU -- -- -- -- -- -- -- -- -- -- -- -- -- --','70: -- -- -- -- -- -- UU --'],
            '10001': ['30: -- -- -- -- -- -- -- 37 -- -- -- -- -- -- -- --','40: -- -- -- -- UU -- -- -- -- -- -- -- -- -- -- --',
                      '50: UU -- -- UU UU UU -- -- -- -- -- -- -- -- -- --','60: UU -- -- -- -- -- -- -- -- -- -- -- -- -- -- --'],
            '10002': ['20: -- -- -- -- -- -- -- -- 28 -- -- -- -- -- -- --','30: -- -- -- -- -- -- -- 37 -- -- -- -- -- -- -- --',
                      '50: -- UU UU -- -- -- -- -- -- -- -- -- UU -- -- --','60: -- -- UU UU -- -- -- -- -- -- -- -- -- -- -- --'],
            '10003': ['50: -- -- -- -- -- -- -- -- -- -- -- 5b -- -- -- --'],'10004': ['50: -- -- -- -- -- -- -- -- -- -- -- 5b -- -- -- --']}
i2cdetectdevicelstdddddd = {'0': ['00:          -- -- -- -- -- 08 -- -- -- -- -- -- --','40: -- -- -- -- 44 -- -- -- 48 -- -- -- -- -- -- --','70: -- -- UU -- -- -- -- --'],
                  '1': ['10: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --','30: -- -- -- -- UU -- -- -- -- -- -- -- -- -- -- --',
                        '50: UU UU -- -- -- -- -- -- 58 -- -- -- -- -- -- --','60: -- -- -- -- UU -- UU -- -- -- -- -- -- -- -- --']}

i2cdetectdevicelst = {'0': ['00:          -- -- -- -- -- 08 -- -- -- -- -- -- --','40: -- -- -- -- 44 -- -- -- 48 -- -- -- -- -- -- --','70: -- -- UU -- -- -- -- --'],
                  '1': ['10: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --','30: -- -- -- -- UU -- -- -- -- -- -- -- -- -- -- --',
                        '50: UU UU -- -- -- -- -- -- 58 -- -- -- -- -- -- --','60: -- -- -- -- UU -- UU -- -- -- -- -- -- -- -- --'],
                  '10': ['50: UU UU -- -- -- -- -- -- -- -- -- -- -- -- -- --','70: -- -- -- -- -- UU -- --'],
                  '11': ['10: UU -- -- -- -- -- -- -- -- -- -- -- -- -- -- --','40: -- UU -- -- -- -- -- -- -- -- -- -- -- -- -- --',
                         '60: UU UU -- -- -- -- -- -- -- -- -- -- -- -- -- --','70: -- -- -- -- -- -- UU --'],
                  '12': ['50: UU -- -- -- -- -- -- -- -- -- -- -- -- -- -- --','70: -- -- -- -- -- UU -- --'],
                  '13': ['50: UU -- -- -- -- -- -- -- -- -- -- -- -- -- -- --','70: -- -- -- -- -- UU -- --'],
                  '14': ['50: UU -- -- -- -- -- -- -- -- -- -- -- -- -- -- --','70: -- -- -- -- -- UU -- --'],
                  '15': ['50: UU -- -- -- -- -- -- -- -- -- -- -- -- -- -- --','70: -- -- -- -- -- UU -- --'],
                  '19': ['50: -- UU -- -- -- -- -- -- -- -- -- -- -- -- -- --','70: -- -- -- -- -- UU -- --'],
                  '20': ['10: UU -- -- -- -- -- -- -- -- -- -- -- -- -- -- --','70: -- -- -- -- -- -- UU --'],
                  '21': ['60: -- UU -- -- -- -- -- -- -- -- -- -- -- -- -- --','70: -- -- -- -- -- -- UU --'],
                  '22': ['60: UU -- -- -- -- -- -- -- -- -- -- -- -- -- -- --','70: -- -- -- -- -- -- UU --'],
                  '23': ['40: -- UU -- -- -- -- -- -- -- -- -- -- -- -- -- --','70: -- -- -- -- -- -- UU --'],
                  '10001': ['20: -- -- -- -- -- -- -- -- -- -- -- -- 2c -- -- --','30: -- -- -- -- -- -- -- 37 -- -- -- -- -- -- -- --',
                            '40: -- -- -- -- UU -- -- -- -- -- -- -- -- -- -- --','50: UU -- -- UU UU UU -- -- -- -- -- -- -- -- -- --',
                            '60: UU -- -- -- -- -- -- -- -- -- -- -- -- -- -- --'],
                  '10002': ['30: -- -- -- -- -- -- -- 37 -- -- -- -- -- -- -- --','50: -- UU UU -- -- -- -- -- -- -- -- -- UU -- -- --',
                            '60: -- -- UU UU -- -- -- -- -- -- -- -- -- -- -- --'],
                  '10003': ['50: -- -- -- -- -- -- -- -- -- -- -- 5b -- -- -- --'],
                  '10004': ['50: -- -- -- -- -- -- -- -- -- -- -- 5b -- -- -- --']}


i2cdetectdevicelst_mtp = {'0': ['00:          -- -- -- -- -- 08 -- -- -- -- -- -- --','40: -- -- -- -- 44 -- -- -- 48 -- -- -- -- -- -- --','70: -- -- UU -- -- -- -- --'],
                  '1': ['10: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --','30: -- -- -- -- UU -- -- -- -- -- -- -- -- -- -- --',
                        '50: UU UU -- -- -- -- -- -- 58 -- -- -- -- -- -- --','60: -- -- -- -- UU -- UU -- -- -- -- -- -- -- -- --']}

i2cdevice_data = [["20","0x10","0x01","0x80"],["10001","0x53","0x01","0x00"],["10001","0x54","0x01","0x00"],["10001","0x55","0x01","0x00"],["10002","0x51","0x01","0x00"],
                  ["10002","0x52","0x01","0x00"],["0","0x44","0x00","0x00"],["0","0x72","0x00","0x01"],["1","0x50","0x00","0xff"],["1","0x51","0x00","0xff"],["1","0x64","0x00","0x01"],
                  ["1","0x66","0x00","0x01"],["1","0x34","0x00","0x09"],["10","0x75","0x00","0x00"],["11","0x76","0x00","0x00"],["12","0x50","0x00","0xff"],["13","0x50","0x00","0xff"],
                  ["14","0x50","0x00","0xff"],["15","0x50","0x00","0xff"],["19","0x51","0x00","0xff"],["21","0x61","0x00","0x00"],["22","0x60","0x00","0x00"],["23","0x41","0x00","0x06"],
                  ["10001","0x44","0x00","0x10"],["10001","0x60","0x00","0x01"],["10001","0x50","0x00","0xff"],["10002","0x62","0x00","0x01"],["10002","0x63","0x00","0x01"],
                  ["10002","0x5c","0x00","0x1b"],["10003","0x5b","0x00","0x33"],["10004","0x5b","0x00","0x33"],["0","0x48","0x00","0xff"]]
i2cbus_device_data = {'10001': ['20: -- -- -- -- -- -- -- -- 28 -- -- -- 2c -- -- --','30: -- -- -- -- -- -- -- 37 -- -- -- -- -- -- -- --',
                                '40: -- -- -- -- UU -- -- -- -- -- -- -- -- -- -- --','50: UU -- -- UU UU UU -- -- -- -- -- -- -- -- -- --',
                                '60: UU -- -- -- -- -- -- -- -- -- -- -- -- -- -- --'],
                      '10002': ['20: -- -- -- -- -- -- -- -- 28 -- -- -- -- -- -- --','30: -- -- -- -- -- -- -- 37 -- -- -- -- -- -- -- --',
                                '50: -- UU UU -- -- -- -- -- -- -- -- -- UU -- -- --','60: -- -- UU UU -- -- -- -- -- -- -- -- -- -- -- --']}




#TC 15
cpld_version1='0xe'
cpld_version3='0x6'


#tcs30
ver_1 = ['4.19']
sys_version =  brixia_diag_version




# TC_01

new_diag_image = "R3152-J0001-01_Diag-brixia.v0.1.7.deb"
old_diag_image = "R3152-J0001-01_Diag-brixia.v0.1.6.deb"
structure_ptn_mtp=['cel-all-test',
'cel-amplitude-test',
'cel-cpld-test',
'cel-cpu-test',
'cel-eeprom-test',
'cel-gpio-test',
'cel-i2c-test',
'cel-mem-test',
'cel-pci-test',
'cel-psu-test',
'cel-rtc-test',
'cel-storage-test',
'cel-sysinfo-test',
'cel-temp-test',
'cel-uart-test',
'cel-upgrade-test']
structure_ptn = [
    "cel-all-test",
    "cel-bb-cpld-test",
    "cel-cpld-test",
    "cel-cpu-test",
    "cel-detect-th4-test",
    "cel-eeprom-test",
    "cel-fan-test",
    "cel-fpga-test",
    "cel-i2c-test",
    "cel-led-test",
    "cel-mem-test",
    "cel-pci-test",
    "cel-phy-test",
    "cel-psu-test",
    "cel-qsfp-test",
    "cel-rtc-test",
    "cel-storage-test",
    "cel-sysinfo-test",
    "cel-temp-test",
    "cel-uart-test",
    "cel-upgrade-test",
]

# TC_02
remove_diag_cmds = [
    "cd /home",
    "dpkg --list | grep cel-diag",
    "dpkg -r cel-diag",
    "dpkg --purge cel-diag",
    "cd /usr/local/cls_diag/ ",
    "dpkg --list | grep cel-diag"
]

remove_diag_ptn = [
    "Suite of tools and libraries for Celestica diagnostics.",
    "Removing cel-diag",
    "Purging configuration files for cel-diag",
    "No such file or directory"
    ]
#TC 19
eeprom_data1='''
00000000  ff 01 e0 02 0b 44 55 4d  4d 59 31 32 33 34 35 36  |.....DUMMY123456|
00000010  03 0f 44 55 4d 4d 59 31  32 33 34 35 36 37 38 39  |..DUMMY123456789|
00000020  58 05 02 12 34 06 04 11  22 33 44 07 01 ff 08 0b  |X...4..."3D.....|
00000030  44 55 4d 4d 59 31 32 33  34 35 36 09 0f 44 55 4d  |DUMMY123456..DUM|
00000040  4d 59 31 32 33 34 35 36  37 38 39 58 0b 01 dc 11  |MY123456789X....|
00000050  04 00 00 30 39 12 14 44  55 4d 4d 59 31 32 33 34  |...09..DUMMY1234|
00000060  35 36 2d 37 38 39 58 58  5f 58 58 00 02 5e 0f ff  |56-789XX_XX..^..|
00000070  ff ff ff ff ff ff ff ff  ff ff ff ff ff ff ff ff  |................|
*
00000100
'''
eeprom_data2='''
00000000  ff 01 e0 05 02 12 34 06  04 11 22 33 44 07 01 ff  |......4..."3D...|
00000010  08 0b 44 55 4d 4d 59 31  32 33 34 35 36 09 0f 44  |..DUMMY123456..D|
00000020  55 4d 4d 59 31 32 33 34  35 36 37 38 39 58 0b 01  |UMMY123456789X..|
00000030  dc 0f 0d 44 55 4d 4d 59  31 32 33 34 35 2d 36 37  |...DUMMY12345-67|
00000040  10 0d 44 55 4d 4d 59 31  32 33 34 35 36 37 38 00  |..DUMMY12345678.|
00000050  02 f7 40 ff ff ff ff ff  ff ff ff ff ff ff ff ff  |..@.............|
00000060  ff ff ff ff ff ff ff ff  ff ff ff ff ff ff ff ff  |................|
*
00000100
'''
eeprom_data3='''
00000000  ff 01 e0 02 0b 44 55 4d  4d 59 31 32 33 34 35 36  |.....DUMMY123456|
00000010  03 0f 44 55 4d 4d 59 31  32 33 34 35 36 37 38 39  |..DUMMY123456789|
00000020  58 04 06 aa bb cc dd ee  ff 05 02 12 34 06 04 11  |X...........4...|
00000030  22 33 44 07 01 ff 08 0b  44 55 4d 4d 59 31 32 33  |"3D.....DUMMY123|
00000040  34 35 36 09 0f 44 55 4d  4d 59 31 32 33 34 35 36  |456..DUMMY123456|
00000050  37 38 39 58 0a 02 ff ff  0b 01 dc 00 02 79 0a ff  |789X.........y..|
00000060  ff ff ff ff ff ff ff ff  ff ff ff ff ff ff ff ff  |................|
*
00000800
'''
eeprom_mod1="Dump come EEPROM data:\n"
eeprom_mod2="Dump baseboard EEPROM data:\n"
eeprom_mod3="Dump switch EEPROM data:\n"
for i in range(1,5):
    eeprom_mod4="Dump fan-{} EEPROM data:\n".format(i)
eeprom_rdata1='''
00000000  ff 01 e0 00 02 52 c3 ff  ff ff ff ff ff ff ff ff  |.....R..........|
00000010  ff ff ff ff ff ff ff ff  ff ff ff ff ff ff ff ff  |................|
*
00000800
'''
eeprom_rdata2='''
00000000  ff 01 e0 00 02 52 c3 ff  ff ff ff ff ff ff ff ff  |.....R..........|
00000010  ff ff ff ff ff ff ff ff  ff ff ff ff ff ff ff ff  |................|
*
00000100
'''

# TC_03
BRIXIA_BIOS = SwImage.getSwImage("BRIXIA_BIOS")

bios_old_image=BRIXIA_BIOS.oldImage
bios_new_image=BRIXIA_BIOS.newImage
bios_old_version=BRIXIA_BIOS.oldVersion
bios_new_version=BRIXIA_BIOS.newVersion

upgrade_bios_old_cmd = "./cel-upgrade-test --update -d 5 --file ../tools/firmware/" + bios_old_image
upgrade_bios_new_cmd = "./cel-upgrade-test --update --dev 5 -f ../tools/firmware/" + bios_new_image

option_help_ptn = [
    "usage: ./cel-upgrade-test [OPTIONS]",
    "Options are:",
    "--update     Update single firmware",
    "-v, --version    Display the version and exit",
    "-l, --list       Show configuration list",
    "-d, --dev[1-5]   [1:BIOS|2:COMe CPLD|3:FPGA|4:Baseboard CPLD|5:Coreboot]",
    "-f, --file       Update  the firmware file image",
    "-h, --help       Display this help text and exit",
    "Example:",
    "--update -d 1 -f ../firmware/fpga/ELM.0.01.05.bin",
]

option_list_ptn = [
    "*** 01 |device name : BIOS",
    "*** 02 |device name : COMe_CPLD",
    "*** 03 |device name : FPGA",
    "*** 04 |device name : Baseboard_CPLD",
    "*** 05 |device name : COREBOOT"
]

# TC_04
BRIXIA_BASEBOARD_CPLD = SwImage.getSwImage("BRIXIA_BASEBOARD_CPLD")
BRIXIA_COME_CPLD = SwImage.getSwImage("BRIXIA_COME_CPLD")

cpld_baseboard_old_ver = BRIXIA_BASEBOARD_CPLD.oldVersion
cpld_baseboard_new_ver = BRIXIA_BASEBOARD_CPLD.newVersion
cpld_baseboard_old_image = BRIXIA_BASEBOARD_CPLD.oldImage
cpld_baseboard_new_image = BRIXIA_BASEBOARD_CPLD.newImage

cpld_come_old_ver = BRIXIA_COME_CPLD.oldVersion
cpld_come_new_ver = BRIXIA_COME_CPLD.newVersion
cpld_come_old_image = BRIXIA_COME_CPLD.oldImage
cpld_come_new_image = BRIXIA_COME_CPLD.newImage

change_cpld_cmd = "./cel-upgrade-test --update --dev {} -f ../tools/firmware/{}"
mgmtip='10.208.140.189'
