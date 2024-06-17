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
##### Variable file used for bmc.robot #####

import os
from collections import OrderedDict
import DeviceMgr
from Const import BOOT_MODE_UBOOT, BOOT_MODE_DIAGOS, BOOT_MODE_ONIE
from SwImage import SwImage



BRIXIA = SwImage.getSwImage("BRIXIA_BIOS")
bios_version=BRIXIA.newVersion


pc_info = DeviceMgr.getServerInfo('PC')
tftp_server_ipv4 = pc_info.managementIP
bios_copy='EVALUATION COPY'
vendor='Intel'
vendor1='Google'
bios_pass = 'google'
user_pass='user'
new_bios_pass='admin'
new_user_pass='guest'
copy_str='Copyright (c) 2006-2019, Intel Corporation'
ifwi='0.0.1'
eeprom_tlv = [
'Read come EEPROM information:',
'mfg_date: 0x1234',
'hw_revision: 0xFF',
'psu_type: DC',
'Read come EEPROM information:',
'hw_revision: 0xFF',
'Read baseboard EEPROM information:',
'psu_type: DC',
'Read switch EEPROM information:',
'mfg_date: 0x1234',
'hw_revision: 0xFF',
'psu_type: DC',
'Read fan-1 EEPROM information:',
'hw_revision: 0xFF',
'psu_type: DC',
'Read fan-2 EEPROM information:',
'mfg_date: 0x1234',
'hw_revision: 0xFF',
'psu_type: DC',
'Read fan-3 EEPROM information:',
'hw_revision: 0xFF',
'psu_type: DC',
'Read fan-4 EEPROM information:',
'psu_type: DC']

cpu_info='Intel(R) Xeon(R) CPU D-1649N @ 2.30GHz'
bios_list=['EDKII Menu',' Boot Manager Menu','Boot Maintenance Manager','Continue','Reset']

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

ifconfig_list =['eth0:.*UP','lo.*RUNNING']

fdisk_list=['/dev/sda1.*EFI System','/dev/sda2.*ONIE boot','/dev/sda3.*Linux filesystem']


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

cpu_new=[]
for i in range(0,2):
    cpu_new.append('processor.*:.*'+str(i))
    cpu_new.append('vendor_id.*:.*GenuineIntel')
    cpu_new.append('cpu family.*:.*6')
    cpu_new.append('model.*:.*86')
    cpu_new.append('model name.*:.*Intel\(R\) Xeon\(R\) CPU D-1649N @ 2.30GHz')
    cpu_new.append('stepping.*:.*5')
    cpu_new.append('microcode.*:.*0xe000014')
    cpu_new.append('cpu cores.*:.*1')
    cpu_new.append('fpu.*:.*yes')
    cpu_new.append('fpu_exception.*:.*yes')
    cpu_new.append('cpuid level.*:.*20')
    cpu_new.append('wp.*:.*yes')


lscpi = ['Architecture:        x86_6',
        'CPU op-mode\(s\):.*32-bit, 64-bit',
        'Byte Order:          Little Endian',
        'CPU\(s\):              16',
        'Vendor ID:           GenuineIntel',
        'CPU family:          6',
        'Model:               86',
        'Model name:          Intel\(R\) Xeon\(R\) CPU D-1649N @ 2.30GHz',
        'Stepping:            5',
        'Virtualization:      VT-x']



##########tc 08 #########
copy_right='Copyright (c) 2006-2019, Intel Corporation'
eval_string= 'EVALUATION COPY'
ifwi = '0.0.1'

ram='32768 MB RAM'


#tc 64 ####
boot_list=['UEFI SATA0','UEFI USB0','UEFI Internal Shell']

#####tc_27###########
brixia_ip='10.208.140.237'
brixia_comm='MASTER_L2_7'



###################################
#tc68
i2detect_y0= {'00':['-- -- -- -- -- 08 -- -- -- -- -- -- --'], \
'10': ['-- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --'],\
'20': ['-- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --'], \
'30': ['-- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --'], \
'40': ['-- -- -- -- 44 -- -- -- 48 -- -- -- -- -- -- --'], \
'50': ['-- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --'], \
'60': ['-- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --'], \
'70':['-- -- UU -- -- -- -- --']}

i2detect_y1={'00' : ['         -- -- -- -- -- -- -- -- -- -- -- -- --'],\
'10' : ['-- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --'],\
'20' : ['-- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --'],\
'30' : ['-- -- -- -- UU -- -- -- -- -- -- -- -- -- -- --'],\
'40' : ['-- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --'],\
'50' : ['UU UU -- -- -- -- -- -- 58 -- -- -- -- -- -- --'],\
'60' : ['-- -- -- -- UU -- UU -- -- -- -- -- -- -- -- --'],\
'70' : ['-- -- -- -- -- -- -- --']}

i2detect_y10={'00' :['          -- -- -- -- -- -- -- -- -- -- -- -- --'],\
'10' :[' -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --'],\
'20' :[' -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --'],\
'30' :[' -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --'],\
'40' :[' -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --'],\
'50' :[' UU UU -- -- -- -- -- -- -- -- -- -- -- -- -- --'],\
'60' :[' -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --'],\
'70' :[' -- -- -- -- -- UU -- --']}

i2detect_y11={'00' :['          -- -- -- -- -- -- -- -- -- -- -- -- --'],\
'10' :[' UU -- -- -- -- -- -- -- -- -- -- -- -- -- -- --'],\
'20' :[' -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --'],\
'30' :[' -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --'],\
'40' :[' -- UU -- -- -- -- -- -- -- -- -- -- -- -- -- --'],\
'50' :[' -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --'],\
'60' :[' UU UU -- -- -- -- -- -- -- -- -- -- -- -- -- --'],\
'70' :[' -- -- -- -- -- -- UU --']}

#tc42
com='0x3f8'

##tc35
lpca0='0xe'
lpca1='0xde'
lpce0='0x18'
lpce1='0x55'

##tc34
i2cdetect_new= {'30':['             UU']}
imc=['i2c-29  smbus           iMC socket 0 for channel pair 2-3       SMBus adapter',\
     'i2c-28  smbus           iMC socket 0 for channel pair 0-1       SMBus adapter']

i2cdetect_28=['I2C                              no',\
'SMBus Quick Command              no',\
'SMBus Send Byte                  no',\
'SMBus Receive Byte               no',\
'SMBus Write Byte                 yes',\
'SMBus Read Byte                  yes',\
'SMBus Write Word                 yes',\
'SMBus Read Word                  yes',\
'SMBus Process Call               no',\
'SMBus Block Write                no',\
'SMBus Block Read                 no',\
'SMBus Block Process Call         no',\
'SMBus PEC                        no',\
'I2C Block Write                  no',\
'I2C Block Read                   no']

##tc36
lspci_i20=['0c:00.0 Ethernet controller: Intel Corporation I210 Gigabit Network',\
          '0d:00.0 Ethernet controller: Intel Corporation I210 Gigabit Network']
shell_i20=['00   0C   00    00 ==> Network Controller - Ethernet controller',\
           '00   0D   00    00 ==> Network Controller - Ethernet controller']

#tc31
lspci=['00:00.0 Host bridge: Intel Corporation Xeon E7 v4/Xeon E5 v4/Xeon E3 v4/Xeon D DMI2',\
  '00:02.0 PCI bridge: Intel Corporation Xeon E7 v4/Xeon E5 v4/Xeon E3 v4/Xeon D PCI Express Root Port 2',\
  '00:03.0 PCI bridge: Intel Corporation Xeon E7 v4/Xeon E5 v4/Xeon E3 v4/Xeon D PCI Express Root Port 3',\
  '00:04.0 System peripheral: Intel Corporation Xeon E7 v4/Xeon E5 v4/Xeon E3 v4/Xeon D Crystal Beach DMA',\
  '00:05.0 System peripheral: Intel Corporation Xeon E7 v4/Xeon E5 v4/Xeon E3 v4/Xeon D Map/VTd_Misc/System Management',\
  '00:14.0 USB controller: Intel Corporation 8 Series/C220 Series Chipset Family USB xHCI',\
  '01:00.0 Ethernet controller: Broadcom Limited Device b996',\
  '03:00.0 Co-processor: Intel Corporation Xeon Processor D Family',\
  '05:00.0 Ethernet controller: Intel Corporation Ethernet Connection X552 10 GbE SFP+',\
  '07:00.0 Ethernet controller: Intel Corporation Ethernet Connection X552 10 GbE SFP+',\
  '0b:00.0 System peripheral: Google, Inc. Device 0065',\
  '0c:00.0 Ethernet controller: Intel Corporation I210 Gigabit Network',\
  '0d:00.0 Ethernet controller: Intel Corporation I210 Gigabit Network Connection']
bcm=['xe0.*up','xe1.*up']

###############################
#tc25
core0=['Core0']
core8=['Core0','Core1','Core2','Core3','Core4','Core5','Core6','Core7']

##################################################################################
#tc32
lspci_bridge=['Host bridge: Intel Corporation Xeon E7 v4','PCI bridge: Intel Corporation Xeon E7 v4']
lspci_device=['Broadcom Limited Device b996','Google, Inc. Device 0065']
lspci_mgmt=['Ethernet controller: Intel Corporation I210 Gigabit Network Connection','Latency: 0, Cache Line Size: 128 bytes']
lspci_sfp=['Ethernet controller: Intel Corporation Ethernet Connection X552 10 GbE SFP+','Latency: 0, Cache Line Size: 32 bytes']
lspci_broad=['Broadcom Limited Device b996','Latency: 0, Cache Line Size: 32 bytes']
lspci_intel=['Co-processor: Intel Corporation Xeon Processor D Family QuickAssist Technology','Latency: 0, Cache Line Size: 32 bytes']

##################
mgmt_info=['Ethernet controller: Intel Corporation I210 Gigabit Network Connection']
