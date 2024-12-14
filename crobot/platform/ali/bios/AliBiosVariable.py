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

from SwImage import SwImage

# SwImage shared objects
BIOS = SwImage.getSwImage("BIOS")
AFU_TOOL = SwImage.getSwImage("AFU_TOOL")
ME_FIRMWARE = SwImage.getSwImage("ME_FIRMWARE")
BDX_DE_LINUX = SwImage.getSwImage("BDX_DE_LINUX")
BASE_CPLD = SwImage.getSwImage("BASE_CPLD")
COME_CPLD = SwImage.getSwImage("COME_CPLD")
RU = SwImage.getSwImage("RU")
# End of SwImage shared objects

BIOS_START_KEYWORD = r'BIOS Power On Self-Test Start'
BIOS_HEADER_KEYWORD = r'.*Aptio Setup Utility.*'
ENTER_BIOS_KEYWORD = r'Press <DEL>\/<ESC> to enter setup'
ENTER_BBS_KEYWORD = r'Press <F7> to BBS POPUP Menu'

bios_new_version = BIOS.newVersion
bios_old_version = BIOS.oldVersion
bios_new_image = BIOS.newImage
bios_old_image = BIOS.oldImage
afu_new_image = AFU_TOOL.newImage
bios_local_image_path = BIOS.localImageDir
bdx_local_image_path = BDX_DE_LINUX.localImageDir
bdx_new_image = BDX_DE_LINUX.newImage
cpld_b_new_version = BASE_CPLD.newVersion
cpld_c_new_version = COME_CPLD.newVersion
ru_local_image_path = RU.localImageDir
ru_new_image = RU.newImage
ru_dir_name = ru_new_image.rsplit('.',1)[0]
ru_cmd = 'RU.efi'

bios_pass_pattern = r'Process completed'
bios_vendor = r'(?P<bios_vendor>American Megatrends)'
bios_date_pattern = r'(?P<bios_date>\d{2}/\d{2}/\d{4} \d{2}:\d{2}:\d{2})'
bios_version_pattern = r'D0000\.(?P<bios_version>%s)'%(bios_new_version)
bios_old_version_pattern = r'D0000\.(?P<bios_version>%s)'%(bios_old_version)

bios_info_last_line = r'System Time.*Enter: Select'
bios_info_vendor = r'(?i)BIOS Vendor\s*%s'%(bios_vendor)
bios_info_date = r'(?i)Build Date and Time\s*%s'%(bios_date_pattern)

evaluation_keywords = [r'(?i)EVALUATION COPY']

post_test_list = [
    'POST : Pre-memory SB.*',
    'POST : System.*',
    'POST : Memory.*',
    'POST : CPU.*',
    'POST : DXE.*',
    'POST : PCI HB.*',
    'POST : SB.*',
    'POST : CSM.*',
    'POST : PCI Bus.*',
    'POST : .*Drivers.*',
    'POST : Console.*',
    'POST : IDE.*',
]

eeprom_pattern = r'((?:Board|Product).+): (.+)'
smbios_eeprom_pattern = r'((?:board|product|chassis).+)=(.*)'
tlv_eeprom_pattern = r'(.+)\s+(?:0[xX][0-9a-fA-F]+)\s+(?:\d+)\s+(.*)'

diag_util_bmc_path = '/var/log/BMC_Diag/utility/'
diag_util_cpu_path = '/usr/local/migaloo/utility/'
diag_cpu_path = '/usr/local/migaloo/CPU_Diag/'

bmc_eeprom_path = diag_util_bmc_path + 'BMC_fru_eeprom'
sys_eeprom_path = diag_util_bmc_path + 'system_fru_eeprom'
switch_eeprom_path = diag_util_bmc_path + 'switch_fru_eeprom'
come_eeprom_path = diag_util_bmc_path + 'COMe_fru_eeprom'
smbios_eeprom_path = diag_util_cpu_path + 'SMBIOS_fru_eeprom'
tlv_eeprom_path = diag_cpu_path
tlv_eeprom_cmd = './cel-eeprom-test -t tlv -d 1 -r -C 256'

eeprom_tlv_patterns = [
    r"(?m)^Product Name +\w+ +\d+ +(?P<product_name>.*)",
    r"(?m)^Part Number +\w+ +\d+ +(?P<part_number>.*)",
    r"(?m)^Serial Number +\w+ +\d+ +(?P<serial_number>.*)",
    r"(?m)^Base MAC Address +\w+ +\d+ +(?P<base_mac>.*)",
    r"(?m)^Manufacture Date +\w+ +\d+ +(?P<mfg_date>.*)",
    r"(?m)^Device Version +\w+ +\d+ +(?P<device_version>.*)",
    r"(?m)^Label Revision +\w+ +\d+ +(?P<label_device>.*)",
    r"(?m)^Platform Name +\w+ +\d+ +(?P<platform_name>.*)",
    r"(?m)^ONIE Version +\w+ +\d+ +(?P<onie_version>.*)",
    r"(?m)^MAC Addresses +\w+ +\d+ +(?P<mac_addr>.*)",
    r"(?m)^Manufacturer +\w+ +\d+ +(?P<mfg>.*)",
    r"(?m)^Manufacture Country +\w+ +\d+ +(?P<mfg_country>.*)",
    r"(?m)^Vendor Name +\w+ +\d+ +(?P<vendor_name>.*)",
    r"(?m)^Diag Version +\w+ +\d+ +(?P<diag_version>.*)",
    r"(?m)^Service Tag +\w+ +\d+ +(?P<service_tag>.*)",
    r"(?m)^Vendor Extension +\w+ +\d+ +(?P<vendor_ext>.*)",
    r"(?m)^CRC-32 +\w+ +\d+ +(?P<crc_32>.*)",
]

me_fw_version = ME_FIRMWARE.newVersion
me_config_last_line = r'MCTP Bus Owner\s*\d+'
me_info_patterns = [
    r'Operational Firmware\s*\d+:(?P<ME_version>%s)'%(me_fw_version),
    r'Current State\s*(?P<ME_default_value>Operational)'
]

boot_override_last_line = r'(UEFI:|ONIE:|SONiC).*F10: Save & Exit'
boot_sonic_str = 'SONiC-OS'
boot_onie_str = 'ONIE'
boot_uefi_str = 'UEFI.*Shell'

boot_option_1_selected = r'Boot Option #1\s+\[(.+)\*?\|'
boot_option_last_line = r'Disabled\s+'

proc_name = r'Intel\(R\) Xeon\(R\) CPU D-1533N @ 2\.10GHz'
proc_speed_mhz = '2100'
proc_speed_ghz = '2.100'
proc_type_pattern = r'Processor Type: (?P<processor_name>%s)'%(proc_name)
proc_speed_pattern = r'Processor Speed: (?P<processor_speed>%s) MHz'%(proc_speed_mhz)

proc_freq_pattern = r'Processor Frequency\s+(?P<processor_frequency>%sGHz)'%(proc_speed_ghz)
proc_l1_cache = r'L1 Cache RAM\s*(?P<L1_Cache>384KB)'
proc_l2_cache = r'L2 Cache RAM\s*(?P<L1_Cache>1536KB)'
proc_l3_cache = r'L3 Cache RAM\s*(?P<L1_Cache>9216KB)'
proc_0_ver_1 = r'Processor 0 Version\s*(?P<processor_name_1>%s)\s*\+\|\+\/\-: Change Opt\.\s+\|'%(proc_name[:27])
proc_0_ver_2 = r'(?P<processor_name_2>%s)\s*\+\|F1: General Help'%(proc_name[27:])

proc_patterns = [
    r'(processor\s*:\s*.+)\r',
    r'(vendor_id\s*:\s*.+)\r',
    r'(cpu family\s*:\s*.+)\r',
    r'(model\s*:\s*.+)\r',
    r'(model name\s*:\s*%s)'%(proc_name),
    r'(stepping\s*:\s*.+)\r',
    r'(microcode\s*:\s*.+)\r',
    r'(cpu MHz\s*:\s*.+)\r',
    r'(cache size\s*:\s*9216 KB)',
    r'(physical id\s*:\s*.+)\r',
    r'(siblings\s*:\s*.+)\r',
    r'(core id\s*:\s*.+)\r',
    r'(cpu cores\s*:\s*.+)\r',
    r'(apicid\s*:\s*.+)\r',
    r'(initial apicid\s*:\s*.+)\r',
    r'(fpu\s*:\s*.+)\r',
    r'(fpu_exception\s*:\s*.+)\r',
    r'(cpuid level\s*:\s*.+)\r',
    r'(wp\s*:\s*.+)\r',
]
proc_pattern = "[\r|\n]+".join(proc_patterns)

top_last_line = r'%Cpu\d+.*(\n)+KiB Mem'
top_patterns = [
    r'(%Cpu\d+)\s*:',
    r'(\d+\.\d+ us)',
    r'(\d+\.\d+ sy)',
    r'(\d+\.\d+ ni)',
    r'(\d+\.\d+ id)',
    r'(\d+\.\d+ wa)',
    r'(\d+\.\d+ hi)',
    r'(\d+\.\d+ si)',
    r'(\d+\.\d+ st)',
]
top_pattern = ",?\s*".join(top_patterns)
proc_config_last_line = r'Execute Disable Bit.*\|'
cores_en_patterns = r'Cores Enabled\s+\d+'

microcode_rev_setup_pattern = r'(?i)Microcode Revision\\s*(?P<revision1>\\w+)'
microcode_rev_dmesg_pattern = r'(?i)microcode:.*revision=(?P<revision2>\\w+)'
dmesg_microcode_cmd = 'dmesg | grep microcode'

mem_size_gb = '8'
mem_size_mb = '8192'
mem_type = 'DDR4 2133'
memory_info_pattern = r'(?i)Total Memory Installed:\\s*(?P<memory_size_gb>%s\\s*GB)\\s*\\((?P<memory_type>%s)\\)'%(mem_size_gb, mem_type)
memory_size_pattern = r'(?i)Total Memory\\s*(?P<memory_size_mb>%s\\s*MB)'%(mem_size_mb)
meminfo_patterns = [
    r'MemTotal:\\s*(?P<MemTotal>\\d+) kB',
    r'MemFree:\\s*(?P<MemFree>\\d+) kB',
    r'MemAvailable:\\s*(?P<MemAvailable>\\d+) kB',
    r'Buffers:\\s*(?P<Buffers>\\d+) kB',
    r'Cached:\\s*(?P<Cached>\\d+) kB',
    r'SwapCached:\\s*(?P<SwapCached>\\d+) kB',
    r'Active:\\s*(?P<Active>\\d+) kB',
    r'Inactive:\\s*(?P<Inactive>\\d+) kB',
    r'Active\\(anon\\):\\s*(?P<Active_anon>\\d+) kB',
    r'Inactive\\(anon\\):\\s*(?P<Inactive_anon>\\d+) kB',
    r'Active\\(file\\):\\s*(?P<Active_file>\\d+) kB',
    r'Inactive\\(file\\):\\s*(?P<Inactive_file>\\d+) kB',
    r'Unevictable:\\s*(?P<Unevictable>\\d+) kB',
    r'Mlocked:\\s*(?P<Mlocked>\\d+) kB',
    r'SwapTotal:\\s*(?P<SwapTotal>\\d+) kB',
    r'SwapFree:\\s*(?P<SwapFree>\\d+) kB',
    r'Dirty:\\s*(?P<Dirty>\\d+) kB',
    r'Writeback:\\s*(?P<Writeback>\\d+) kB',
    r'AnonPages:\\s*(?P<AnonPages>\\d+) kB',
    r'Mapped:\\s*(?P<Mapped>\\d+) kB',
    r'Shmem:\\s*(?P<Shmem>\\d+) kB',
    r'Slab:\\s*(?P<Slab>\\d+) kB',
    r'SReclaimable:\\s*(?P<SReclaimable>\\d+) kB',
    r'SUnreclaim:\\s*(?P<SUnreclaim>\\d+) kB',
    r'KernelStack:\\s*(?P<KernelStack>\\d+) kB',
    r'PageTables:\\s*(?P<PageTables>\\d+) kB',
    r'NFS_Unstable:\\s*(?P<NFS_Unstable>\\d+) kB',
    r'Bounce:\\s*(?P<Bounce>\\d+) kB',
    r'WritebackTmp:\\s*(?P<WritebackTmp>\\d+) kB',
    r'CommitLimit:\\s*(?P<CommitLimit>\\d+) kB',
    r'Committed_AS:\\s*(?P<Committed_AS>\\d+) kB',
    r'VmallocTotal:\\s*(?P<VmallocTotal>\\d+) kB',
    r'VmallocUsed:\\s*(?P<VmallocUsed>\\d+) kB',
    r'VmallocChunk:\\s*(?P<VmallocChunk>\\d+) kB',
]

pci_uefi_patterns = [
    r'(?i)\s*(?P<bdf>00   00   00    00)\s+==>\s+(?P<device_class>Bridge Device - Host/PCI bridge)[\r|\n]+.+Vendor\s*(?P<vendor_id>8086)\s*Device\s*(?P<device_id>6F00)\s*(Prog Interface 0)',
    r'(?i)\s*(?P<bdf>00   00   01    00)\s+==>\s+(?P<device_class>Bridge Device - PCI/PCI bridge)[\r|\n]+.+Vendor\s*(?P<vendor_id>8086)\s*Device\s*(?P<device_id>6F02)\s*(Prog Interface 0)',
    r'(?i)\s*(?P<bdf>00   00   02    00)\s+==>\s+(?P<device_class>Bridge Device - PCI/PCI bridge)[\r|\n]+.+Vendor\s*(?P<vendor_id>8086)\s*Device\s*(?P<device_id>6F04)\s*(Prog Interface 0)',
    r'(?i)\s*(?P<bdf>00   00   02    02)\s+==>\s+(?P<device_class>Bridge Device - PCI/PCI bridge)[\r|\n]+.+Vendor\s*(?P<vendor_id>8086)\s*Device\s*(?P<device_id>6F06)\s*(Prog Interface 0)',
    r'(?i)\s*(?P<bdf>00   00   02    03)\s+==>\s+(?P<device_class>Bridge Device - PCI/PCI bridge)[\r|\n]+.+Vendor\s*(?P<vendor_id>8086)\s*Device\s*(?P<device_id>6F07)\s*(Prog Interface 0)',

    r'(?i)\s*(?P<bdf>00   00   03    00)\s+==>\s+(?P<device_class>Bridge Device - PCI/PCI bridge)[\r|\n]+.+Vendor\s*(?P<vendor_id>8086)\s*Device\s*(?P<device_id>6F08)\s*(Prog Interface 0)',
    r'(?i)\s*(?P<bdf>00   00   03    01)\s+==>\s+(?P<device_class>Bridge Device - PCI/PCI bridge)[\r|\n]+.+Vendor\s*(?P<vendor_id>8086)\s*Device\s*(?P<device_id>6F09)\s*(Prog Interface 0)',
    r'(?i)\s*(?P<bdf>00   00   03    02)\s+==>\s+(?P<device_class>Bridge Device - PCI/PCI bridge)[\r|\n]+.+Vendor\s*(?P<vendor_id>8086)\s*Device\s*(?P<device_id>6F0A)\s*(Prog Interface 0)',

    r'(?i)\s*(?P<bdf>00   00   04    00)\s+==>\s+(?P<device_class>Base System Peripherals - Other system peripheral)[\r|\n]+.+Vendor\s*(?P<vendor_id>8086)\s*Device\s*(?P<device_id>6F20)\s*(Prog Interface 0)',
    r'(?i)\s*(?P<bdf>00   00   04    01)\s+==>\s+(?P<device_class>Base System Peripherals - Other system peripheral)[\r|\n]+.+Vendor\s*(?P<vendor_id>8086)\s*Device\s*(?P<device_id>6F21)\s*(Prog Interface 0)',
    r'(?i)\s*(?P<bdf>00   00   04    02)\s+==>\s+(?P<device_class>Base System Peripherals - Other system peripheral)[\r|\n]+.+Vendor\s*(?P<vendor_id>8086)\s*Device\s*(?P<device_id>6F22)\s*(Prog Interface 0)',
    r'(?i)\s*(?P<bdf>00   00   04    03)\s+==>\s+(?P<device_class>Base System Peripherals - Other system peripheral)[\r|\n]+.+Vendor\s*(?P<vendor_id>8086)\s*Device\s*(?P<device_id>6F23)\s*(Prog Interface 0)',
    r'(?i)\s*(?P<bdf>00   00   04    04)\s+==>\s+(?P<device_class>Base System Peripherals - Other system peripheral)[\r|\n]+.+Vendor\s*(?P<vendor_id>8086)\s*Device\s*(?P<device_id>6F24)\s*(Prog Interface 0)',
    r'(?i)\s*(?P<bdf>00   00   04    05)\s+==>\s+(?P<device_class>Base System Peripherals - Other system peripheral)[\r|\n]+.+Vendor\s*(?P<vendor_id>8086)\s*Device\s*(?P<device_id>6F25)\s*(Prog Interface 0)',
    r'(?i)\s*(?P<bdf>00   00   04    06)\s+==>\s+(?P<device_class>Base System Peripherals - Other system peripheral)[\r|\n]+.+Vendor\s*(?P<vendor_id>8086)\s*Device\s*(?P<device_id>6F26)\s*(Prog Interface 0)',
    r'(?i)\s*(?P<bdf>00   00   04    07)\s+==>\s+(?P<device_class>Base System Peripherals - Other system peripheral)[\r|\n]+.+Vendor\s*(?P<vendor_id>8086)\s*Device\s*(?P<device_id>6F27)\s*(Prog Interface 0)',

    r'(?i)\s*(?P<bdf>00   00   05    00)\s+==>\s+(?P<device_class>Base System Peripherals - Other system peripheral)[\r|\n]+.+Vendor\s*(?P<vendor_id>8086)\s*Device\s*(?P<device_id>6F28)\s*(Prog Interface 0)',
    r'(?i)\s*(?P<bdf>00   00   05    01)\s+==>\s+(?P<device_class>Base System Peripherals - Other system peripheral)[\r|\n]+.+Vendor\s*(?P<vendor_id>8086)\s*Device\s*(?P<device_id>6F29)\s*(Prog Interface 0)',
    r'(?i)\s*(?P<bdf>00   00   05    02)\s+==>\s+(?P<device_class>Base System Peripherals - Other system peripheral)[\r|\n]+.+Vendor\s*(?P<vendor_id>8086)\s*Device\s*(?P<device_id>6F2A)\s*(Prog Interface 0)',
    r'(?i)\s*(?P<bdf>00   00   05    04)\s+==>\s+(?P<device_class>Base System Peripherals - PIC)[\r|\n]+.+Vendor\s*(?P<vendor_id>8086)\s*Device\s*(?P<device_id>6F2C)\s*(Prog Interface 20)',

    r'(?i)\s*(?P<bdf>00   00   14    00)\s+==>\s+(?P<device_class>Serial Bus Controllers - USB)[\r|\n]+.+Vendor\s*(?P<vendor_id>8086)\s*Device\s*(?P<device_id>8C31)\s*(Prog Interface 30)',
    r'(?i)\s*(?P<bdf>00   00   1C    00)\s+==>\s+(?P<device_class>Bridge Device - PCI/PCI bridge)[\r|\n]+.+Vendor\s*(?P<vendor_id>8086)\s*Device\s*(?P<device_id>8C10)\s*(Prog Interface 0)',
    r'(?i)\s*(?P<bdf>00   00   1C    02)\s+==>\s+(?P<device_class>Bridge Device - PCI/PCI bridge)[\r|\n]+.+Vendor\s*(?P<vendor_id>8086)\s*Device\s*(?P<device_id>8C14)\s*(Prog Interface 0)',
    r'(?i)\s*(?P<bdf>00   00   1D    00)\s+==>\s+(?P<device_class>Serial Bus Controllers - USB)[\r|\n]+.+Vendor\s*(?P<vendor_id>8086)\s*Device\s*(?P<device_id>8C26)\s*(Prog Interface 20)',
    r'(?i)\s*(?P<bdf>00   00   1F    00)\s+==>\s+(?P<device_class>Bridge Device - PCI/ISA bridge)[\r|\n]+.+Vendor\s*(?P<vendor_id>8086)\s*Device\s*(?P<device_id>8C54)\s*(Prog Interface 0)',
    r'(?i)\s*(?P<bdf>00   00   1F    02)\s+==>\s+(?P<device_class>Mass Storage Controller - Serial ATA controller)[\r|\n]+.+Vendor\s*(?P<vendor_id>8086)\s*Device\s*(?P<device_id>8C02)\s*(Prog Interface 1)',
    r'(?i)\s*(?P<bdf>00   00   1F    03)\s+==>\s+(?P<device_class>Serial Bus Controllers - System Management Bus)[\r|\n]+.+Vendor\s*(?P<vendor_id>8086)\s*Device\s*(?P<device_id>8C22)\s*(Prog Interface 0)',

    r'(?i)\s*(?P<bdf>00   02   00    00)\s+==>\s+(?P<device_class>Processors - Co-processor)[\r|\n]+.+Vendor\s*(?P<vendor_id>8086)\s*Device\s*(?P<device_id>6F54)\s*(Prog Interface 0)',
    r'(?i)\s*(?P<bdf>00   03   00    00)\s+==>\s+(?P<device_class>Network Controller - Ethernet controller)[\r|\n]+.+Vendor\s*(?P<vendor_id>8086)\s*Device\s*(?P<device_id>15AB)\s*(Prog Interface 0)',
    r'(?i)\s*(?P<bdf>00   03   00    01)\s+==>\s+(?P<device_class>Network Controller - Ethernet controller)[\r|\n]+.+Vendor\s*(?P<vendor_id>8086)\s*Device\s*(?P<device_id>15AB)\s*(Prog Interface 0)',
    r'(?i)\s*(?P<bdf>00   04   00    00)\s+==>\s+(?P<device_class>Network Controller - Ethernet controller)[\r|\n]+.+Vendor\s*(?P<vendor_id>8086)\s*Device\s*(?P<device_id>15AB)\s*(Prog Interface 0)',
    r'(?i)\s*(?P<bdf>00   04   00    01)\s+==>\s+(?P<device_class>Network Controller - Ethernet controller)[\r|\n]+.+Vendor\s*(?P<vendor_id>8086)\s*Device\s*(?P<device_id>15AB)\s*(Prog Interface 0)',
    r'(?i)\s*(?P<bdf>00   05   00    00)\s+==>\s+(?P<device_class>Network Controller - Ethernet controller)[\r|\n]+.+Vendor\s*(?P<vendor_id>14E4)\s*Device\s*(?P<device_id>B990)\s*(Prog Interface 0)',
    r'(?i)\s*(?P<bdf>00   08   00    00)\s+==>\s+(?P<device_class>Memory Controller - Other memory controller)[\r|\n]+.+Vendor\s*(?P<vendor_id>1DED)\s*Device\s*(?P<device_id>4301)\s*(Prog Interface 0)',
    r'(?i)\s*(?P<bdf>00   09   00    00)\s+==>\s+(?P<device_class>Network Controller - Ethernet controller)[\r|\n]+.+Vendor\s*(?P<vendor_id>8086)\s*Device\s*(?P<device_id>1537)\s*(Prog Interface 0)',
]

pci_diag_patterns = [
    r'(?i)(?P<bdf>00:00.0)\s*(?P<device_class>Host bridge):\s*(?P<device_name>Intel Corporation Xeon E7 v4/Xeon E5 v4/Xeon E3 v4/Xeon D DMI2)\s*(\(rev\s*05\))?',
    r'(?i)(?P<bdf>00:01.0)\s*(?P<device_class>PCI bridge):\s*(?P<device_name>Intel Corporation Xeon E7 v4/Xeon E5 v4/Xeon E3 v4/Xeon D PCI Express Root Port 1)\s*(\(rev\s*05\))?',
    r'(?i)(?P<bdf>00:02.0)\s*(?P<device_class>PCI bridge):\s*(?P<device_name>Intel Corporation Xeon E7 v4/Xeon E5 v4/Xeon E3 v4/Xeon D PCI Express Root Port 2)\s*(\(rev\s*05\))?',
    r'(?i)(?P<bdf>00:02.2)\s*(?P<device_class>PCI bridge):\s*(?P<device_name>Intel Corporation Xeon E7 v4/Xeon E5 v4/Xeon E3 v4/Xeon D PCI Express Root Port 2)\s*(\(rev\s*05\))?',
    r'(?i)(?P<bdf>00:02.3)\s*(?P<device_class>PCI bridge):\s*(?P<device_name>Intel Corporation Xeon E7 v4/Xeon E5 v4/Xeon E3 v4/Xeon D PCI Express Root Port 2)\s*(\(rev\s*05\))?',
    r'(?i)(?P<bdf>00:03.0)\s*(?P<device_class>PCI bridge):\s*(?P<device_name>Intel Corporation Xeon E7 v4/Xeon E5 v4/Xeon E3 v4/Xeon D PCI Express Root Port 3)\s*(\(rev\s*05\))?',
    r'(?i)(?P<bdf>00:03.1)\s*(?P<device_class>PCI bridge):\s*(?P<device_name>Intel Corporation Xeon E7 v4/Xeon E5 v4/Xeon E3 v4/Xeon D PCI Express Root Port 3)\s*(\(rev\s*05\))?',
    r'(?i)(?P<bdf>00:03.2)\s*(?P<device_class>PCI bridge):\s*(?P<device_name>Intel Corporation Xeon E7 v4/Xeon E5 v4/Xeon E3 v4/Xeon D PCI Express Root Port 3)\s*(\(rev\s*05\))?',

    r'(?i)(?P<bdf>00:04.0)\s*(?P<device_class>System peripheral):\s*(?P<device_name>Intel Corporation Xeon E7 v4/Xeon E5 v4/Xeon E3 v4/Xeon D Crystal Beach DMA Channel 0)\s*(\(rev\s*05\))?',
    r'(?i)(?P<bdf>00:04.1)\s*(?P<device_class>System peripheral):\s*(?P<device_name>Intel Corporation Xeon E7 v4/Xeon E5 v4/Xeon E3 v4/Xeon D Crystal Beach DMA Channel 1)\s*(\(rev\s*05\))?',
    r'(?i)(?P<bdf>00:04.2)\s*(?P<device_class>System peripheral):\s*(?P<device_name>Intel Corporation Xeon E7 v4/Xeon E5 v4/Xeon E3 v4/Xeon D Crystal Beach DMA Channel 2)\s*(\(rev\s*05\))?',
    r'(?i)(?P<bdf>00:04.3)\s*(?P<device_class>System peripheral):\s*(?P<device_name>Intel Corporation Xeon E7 v4/Xeon E5 v4/Xeon E3 v4/Xeon D Crystal Beach DMA Channel 3)\s*(\(rev\s*05\))?',
    r'(?i)(?P<bdf>00:04.4)\s*(?P<device_class>System peripheral):\s*(?P<device_name>Intel Corporation Xeon E7 v4/Xeon E5 v4/Xeon E3 v4/Xeon D Crystal Beach DMA Channel 4)\s*(\(rev\s*05\))?',
    r'(?i)(?P<bdf>00:04.5)\s*(?P<device_class>System peripheral):\s*(?P<device_name>Intel Corporation Xeon E7 v4/Xeon E5 v4/Xeon E3 v4/Xeon D Crystal Beach DMA Channel 5)\s*(\(rev\s*05\))?',
    r'(?i)(?P<bdf>00:04.6)\s*(?P<device_class>System peripheral):\s*(?P<device_name>Intel Corporation Xeon E7 v4/Xeon E5 v4/Xeon E3 v4/Xeon D Crystal Beach DMA Channel 6)\s*(\(rev\s*05\))?',
    r'(?i)(?P<bdf>00:04.7)\s*(?P<device_class>System peripheral):\s*(?P<device_name>Intel Corporation Xeon E7 v4/Xeon E5 v4/Xeon E3 v4/Xeon D Crystal Beach DMA Channel 7)\s*(\(rev\s*05\))?',

    r'(?i)(?P<bdf>00:05.0)\s*(?P<device_class>System peripheral):\s*(?P<device_name>Intel Corporation Xeon E7 v4/Xeon E5 v4/Xeon E3 v4/Xeon D Map/VTd_Misc/System Management)\s*(\(rev\s*05\))?',
    r'(?i)(?P<bdf>00:05.1)\s*(?P<device_class>System peripheral):\s*(?P<device_name>Intel Corporation Xeon E7 v4/Xeon E5 v4/Xeon E3 v4/Xeon D IIO Hot Plug)\s*(\(rev\s*05\))?',
    r'(?i)(?P<bdf>00:05.2)\s*(?P<device_class>System peripheral):\s*(?P<device_name>Intel Corporation Xeon E7 v4/Xeon E5 v4/Xeon E3 v4/Xeon D IIO RAS/Control Status/Global Errors)\s*(\(rev\s*05\))?',
    r'(?i)(?P<bdf>00:05.4)\s*(?P<device_class>PIC):\s*(?P<device_name>Intel Corporation Xeon E7 v4/Xeon E5 v4/Xeon E3 v4/Xeon D I/O APIC)\s*(\(rev\s*05\))?',

    r'(?i)(?P<bdf>00:14.0)\s*(?P<device_class>USB controller):\s*(?P<device_name>Intel Corporation 8 Series/C220 Series Chipset Family USB xHCI)\s*(\(rev\s*05\))?',
    r'(?i)(?P<bdf>00:1c.0)\s*(?P<device_class>PCI bridge):\s*(?P<device_name>Intel Corporation 8 Series/C220 Series Chipset Family PCI Express Root Port #1)\s*(\(rev\s*05\))?',
    r'(?i)(?P<bdf>00:1c.2)\s*(?P<device_class>PCI bridge):\s*(?P<device_name>Intel Corporation 8 Series/C220 Series Chipset Family PCI Express Root Port #3)\s*(\(rev\s*05\))?',
    r'(?i)(?P<bdf>00:1d.0)\s*(?P<device_class>USB controller):\s*(?P<device_name>Intel Corporation 8 Series/C220 Series Chipset Family USB EHCI #1)\s*(\(rev\s*05\))?',
    r'(?i)(?P<bdf>00:1f.0)\s*(?P<device_class>ISA bridge):\s*(?P<device_name>Intel Corporation C224 Series Chipset Family Server Standard SKU LPC Controller)\s*(\(rev\s*05\))?',
    r'(?i)(?P<bdf>00:1f.2)\s*(?P<device_class>SATA controller):\s*(?P<device_name>Intel Corporation 8 Series/C220 Series Chipset Family 6-port SATA Controller 1 \[AHCI mode\])\s*(\(rev\s*05\))?',
    r'(?i)(?P<bdf>00:1f.3)\s*(?P<device_class>SMBus):\s*(?P<device_name>Intel Corporation 8 Series/C220 Series Chipset Family SMBus Controller)\s*(\(rev\s*05\))?',

    r'(?i)(?P<bdf>02:00.0)\s*(?P<device_class>Co-processor):\s*(?P<device_name>Intel Corporation Device 6f54)\s*(\(rev\s*05\))?',
    r'(?i)(?P<bdf>03:00.0)\s*(?P<device_class>Ethernet controller):\s*(?P<device_name>Intel Corporation Ethernet Connection X552 10 GbE Backplane)\s*(\(rev\s*05\))?',
    r'(?i)(?P<bdf>03:00.1)\s*(?P<device_class>Ethernet controller):\s*(?P<device_name>Intel Corporation Ethernet Connection X552 10 GbE Backplane)\s*(\(rev\s*05\))?',
    r'(?i)(?P<bdf>04:00.0)\s*(?P<device_class>Ethernet controller):\s*(?P<device_name>Intel Corporation Ethernet Connection X552 10 GbE Backplane)\s*(\(rev\s*05\))?',
    r'(?i)(?P<bdf>04:00.1)\s*(?P<device_class>Ethernet controller):\s*(?P<device_name>Intel Corporation Ethernet Connection X552 10 GbE Backplane)\s*(\(rev\s*05\))?',
    r'(?i)(?P<bdf>05:00.0)\s*(?P<device_class>Ethernet controller):\s*(?P<device_name>Broadcom Limited Device b990)\s*(\(rev\s*11\))?',
    r'(?i)(?P<bdf>08:00.0)\s*(?P<device_class>Memory controller):\s*(?P<device_name>Device 1ded:4301)\s*(\(rev\s*11\))?',
    r'(?i)(?P<bdf>09:00.0)\s*(?P<device_class>Ethernet controller):\s*(?P<device_name>Intel Corporation I210 Gigabit Backplane Connection)\s*(\(rev\s*03\))?',

    r'(?i)(?P<bdf>ff:0b.0)\s*(?P<device_class>System peripheral):\s*(?P<device_name>Intel Corporation Xeon E7 v4/Xeon E5 v4/Xeon E3 v4/Xeon D R3 QPI Link 0/1)\s*(\(rev\s*05\))?',
    r'(?i)(?P<bdf>ff:0b.1)\s*(?P<device_class>Performance counters):\s*(?P<device_name>Intel Corporation Xeon E7 v4/Xeon E5 v4/Xeon E3 v4/Xeon D R3 QPI Link 0/1)\s*(\(rev\s*05\))?',
    r'(?i)(?P<bdf>ff:0b.2)\s*(?P<device_class>Performance counters):\s*(?P<device_name>Intel Corporation Xeon E7 v4/Xeon E5 v4/Xeon E3 v4/Xeon D R3 QPI Link 0/1)\s*(\(rev\s*05\))?',
    r'(?i)(?P<bdf>ff:0b.3)\s*(?P<device_class>System peripheral):\s*(?P<device_name>Intel Corporation Xeon E7 v4/Xeon E5 v4/Xeon E3 v4/Xeon D R3 QPI Link Debug)\s*(\(rev\s*05\))?',

    r'(?i)(?P<bdf>ff:0c.0)\s*(?P<device_class>System peripheral):\s*(?P<device_name>Intel Corporation Xeon E7 v4/Xeon E5 v4/Xeon E3 v4/Xeon D Caching Agent)\s*(\(rev\s*05\))?',
    r'(?i)(?P<bdf>ff:0c.1)\s*(?P<device_class>System peripheral):\s*(?P<device_name>Intel Corporation Xeon E7 v4/Xeon E5 v4/Xeon E3 v4/Xeon D Caching Agent)\s*(\(rev\s*05\))?',
    r'(?i)(?P<bdf>ff:0c.2)\s*(?P<device_class>System peripheral):\s*(?P<device_name>Intel Corporation Xeon E7 v4/Xeon E5 v4/Xeon E3 v4/Xeon D Caching Agent)\s*(\(rev\s*05\))?',
    r'(?i)(?P<bdf>ff:0c.3)\s*(?P<device_class>System peripheral):\s*(?P<device_name>Intel Corporation Xeon E7 v4/Xeon E5 v4/Xeon E3 v4/Xeon D Caching Agent)\s*(\(rev\s*05\))?',
    r'(?i)(?P<bdf>ff:0c.4)\s*(?P<device_class>System peripheral):\s*(?P<device_name>Intel Corporation Xeon E7 v4/Xeon E5 v4/Xeon E3 v4/Xeon D Caching Agent)\s*(\(rev\s*05\))?',
    r'(?i)(?P<bdf>ff:0c.5)\s*(?P<device_class>System peripheral):\s*(?P<device_name>Intel Corporation Xeon E7 v4/Xeon E5 v4/Xeon E3 v4/Xeon D Caching Agent)\s*(\(rev\s*05\))?',

    r'(?i)(?P<bdf>ff:0f.0)\s*(?P<device_class>System peripheral):\s*(?P<device_name>Intel Corporation Xeon E7 v4/Xeon E5 v4/Xeon E3 v4/Xeon D Caching Agent)\s*(\(rev\s*05\))?',
    r'(?i)(?P<bdf>ff:0f.4)\s*(?P<device_class>System peripheral):\s*(?P<device_name>Intel Corporation Xeon E7 v4/Xeon E5 v4/Xeon E3 v4/Xeon D Caching Agent)\s*(\(rev\s*05\))?',
    r'(?i)(?P<bdf>ff:0f.5)\s*(?P<device_class>System peripheral):\s*(?P<device_name>Intel Corporation Xeon E7 v4/Xeon E5 v4/Xeon E3 v4/Xeon D Caching Agent)\s*(\(rev\s*05\))?',
    r'(?i)(?P<bdf>ff:0f.6)\s*(?P<device_class>System peripheral):\s*(?P<device_name>Intel Corporation Xeon E7 v4/Xeon E5 v4/Xeon E3 v4/Xeon D Caching Agent)\s*(\(rev\s*05\))?',

    r'(?i)(?P<bdf>ff:10.0)\s*(?P<device_class>System peripheral):\s*(?P<device_name>Intel Corporation Xeon E7 v4/Xeon E5 v4/Xeon E3 v4/Xeon D R2PCIe Agent)\s*(\(rev\s*05\))?',
    r'(?i)(?P<bdf>ff:10.1)\s*(?P<device_class>Performance counters):\s*(?P<device_name>Intel Corporation Xeon E7 v4/Xeon E5 v4/Xeon E3 v4/Xeon D R2PCIe Agent)\s*(\(rev\s*05\))?',
    r'(?i)(?P<bdf>ff:10.5)\s*(?P<device_class>System peripheral):\s*(?P<device_name>Intel Corporation Xeon E7 v4/Xeon E5 v4/Xeon E3 v4/Xeon D Ubox)\s*(\(rev\s*05\))?',
    r'(?i)(?P<bdf>ff:10.6)\s*(?P<device_class>Performance counters):\s*(?P<device_name>Intel Corporation Xeon E7 v4/Xeon E5 v4/Xeon E3 v4/Xeon D Ubox)\s*(\(rev\s*05\))?',
    r'(?i)(?P<bdf>ff:10.7)\s*(?P<device_class>System peripheral):\s*(?P<device_name>Intel Corporation Xeon E7 v4/Xeon E5 v4/Xeon E3 v4/Xeon D Ubox)\s*(\(rev\s*05\))?',

    r'(?i)(?P<bdf>ff:13.0)\s*(?P<device_class>System peripheral):\s*(?P<device_name>Intel Corporation Xeon E7 v4/Xeon E5 v4/Xeon E3 v4/Xeon D Memory Controller 0 - Target Address/Thermal/RAS)\s*(\(rev\s*05\))?',
    r'(?i)(?P<bdf>ff:13.1)\s*(?P<device_class>System peripheral):\s*(?P<device_name>Intel Corporation Xeon E7 v4/Xeon E5 v4/Xeon E3 v4/Xeon D Memory Controller 0 - Target Address/Thermal/RAS)\s*(\(rev\s*05\))?',
    r'(?i)(?P<bdf>ff:13.2)\s*(?P<device_class>System peripheral):\s*(?P<device_name>Intel Corporation Xeon E7 v4/Xeon E5 v4/Xeon E3 v4/Xeon D Memory Controller 0 - Channel Target Address Decoder)\s*(\(rev\s*05\))?',
    r'(?i)(?P<bdf>ff:13.3)\s*(?P<device_class>System peripheral):\s*(?P<device_name>Intel Corporation Xeon E7 v4/Xeon E5 v4/Xeon E3 v4/Xeon D Memory Controller 0 - Channel Target Address Decoder)\s*(\(rev\s*05\))?',
    r'(?i)(?P<bdf>ff:13.4)\s*(?P<device_class>System peripheral):\s*(?P<device_name>Intel Corporation Xeon E7 v4/Xeon E5 v4/Xeon E3 v4/Xeon D Memory Controller 0 - Channel Target Address Decoder)\s*(\(rev\s*05\))?',
    r'(?i)(?P<bdf>ff:13.5)\s*(?P<device_class>System peripheral):\s*(?P<device_name>Intel Corporation Xeon E7 v4/Xeon E5 v4/Xeon E3 v4/Xeon D Memory Controller 0 - Channel Target Address Decoder)\s*(\(rev\s*05\))?',
    r'(?i)(?P<bdf>ff:13.6)\s*(?P<device_class>System peripheral):\s*(?P<device_name>Intel Corporation Xeon E7 v4/Xeon E5 v4/Xeon E3 v4/Xeon D DDRIO Channel 0/1 Broadcast)\s*(\(rev\s*05\))?',
    r'(?i)(?P<bdf>ff:13.7)\s*(?P<device_class>System peripheral):\s*(?P<device_name>Intel Corporation Xeon E7 v4/Xeon E5 v4/Xeon E3 v4/Xeon D DDRIO Global Broadcast)\s*(\(rev\s*05\))?',

    r'(?i)(?P<bdf>ff:14.0)\s*(?P<device_class>System peripheral):\s*(?P<device_name>Intel Corporation Xeon E7 v4/Xeon E5 v4/Xeon E3 v4/Xeon D Memory Controller 0 - Channel 0 Thermal Control)\s*(\(rev\s*05\))?',
    r'(?i)(?P<bdf>ff:14.1)\s*(?P<device_class>System peripheral):\s*(?P<device_name>Intel Corporation Xeon E7 v4/Xeon E5 v4/Xeon E3 v4/Xeon D Memory Controller 0 - Channel 1 Thermal Control)\s*(\(rev\s*05\))?',
    r'(?i)(?P<bdf>ff:14.2)\s*(?P<device_class>System peripheral):\s*(?P<device_name>Intel Corporation Xeon E7 v4/Xeon E5 v4/Xeon E3 v4/Xeon D Memory Controller 0 - Channel 0 Error)\s*(\(rev\s*05\))?',
    r'(?i)(?P<bdf>ff:14.3)\s*(?P<device_class>System peripheral):\s*(?P<device_name>Intel Corporation Xeon E7 v4/Xeon E5 v4/Xeon E3 v4/Xeon D Memory Controller 0 - Channel 1 Error)\s*(\(rev\s*05\))?',
    r'(?i)(?P<bdf>ff:14.4)\s*(?P<device_class>System peripheral):\s*(?P<device_name>Intel Corporation Xeon E7 v4/Xeon E5 v4/Xeon E3 v4/Xeon D DDRIO Channel 0/1 Interface)\s*(\(rev\s*05\))?',
    r'(?i)(?P<bdf>ff:14.5)\s*(?P<device_class>System peripheral):\s*(?P<device_name>Intel Corporation Xeon E7 v4/Xeon E5 v4/Xeon E3 v4/Xeon D DDRIO Channel 0/1 Interface)\s*(\(rev\s*05\))?',
    r'(?i)(?P<bdf>ff:14.6)\s*(?P<device_class>System peripheral):\s*(?P<device_name>Intel Corporation Xeon E7 v4/Xeon E5 v4/Xeon E3 v4/Xeon D DDRIO Channel 0/1 Interface)\s*(\(rev\s*05\))?',
    r'(?i)(?P<bdf>ff:14.7)\s*(?P<device_class>System peripheral):\s*(?P<device_name>Intel Corporation Xeon E7 v4/Xeon E5 v4/Xeon E3 v4/Xeon D DDRIO Channel 0/1 Interface)\s*(\(rev\s*05\))?',

    r'(?i)(?P<bdf>ff:15.0)\s*(?P<device_class>System peripheral):\s*(?P<device_name>Intel Corporation Xeon E7 v4/Xeon E5 v4/Xeon E3 v4/Xeon D Memory Controller 0 - Channel 2 Thermal Control)\s*(\(rev\s*05\))?',
    r'(?i)(?P<bdf>ff:15.1)\s*(?P<device_class>System peripheral):\s*(?P<device_name>Intel Corporation Xeon E7 v4/Xeon E5 v4/Xeon E3 v4/Xeon D Memory Controller 0 - Channel 3 Thermal Control)\s*(\(rev\s*05\))?',
    r'(?i)(?P<bdf>ff:15.2)\s*(?P<device_class>System peripheral):\s*(?P<device_name>Intel Corporation Xeon E7 v4/Xeon E5 v4/Xeon E3 v4/Xeon D Memory Controller 0 - Channel 2 Error)\s*(\(rev\s*05\))?',
    r'(?i)(?P<bdf>ff:15.3)\s*(?P<device_class>System peripheral):\s*(?P<device_name>Intel Corporation Xeon E7 v4/Xeon E5 v4/Xeon E3 v4/Xeon D Memory Controller 0 - Channel 3 Error)\s*(\(rev\s*05\))?',

    r'(?i)(?P<bdf>ff:1e.0)\s*(?P<device_class>System peripheral):\s*(?P<device_name>Intel Corporation Xeon E7 v4/Xeon E5 v4/Xeon E3 v4/Xeon D Power Control Unit)\s*(\(rev\s*05\))?',
    r'(?i)(?P<bdf>ff:1e.1)\s*(?P<device_class>System peripheral):\s*(?P<device_name>Intel Corporation Xeon E7 v4/Xeon E5 v4/Xeon E3 v4/Xeon D Power Control Unit)\s*(\(rev\s*05\))?',
    r'(?i)(?P<bdf>ff:1e.2)\s*(?P<device_class>System peripheral):\s*(?P<device_name>Intel Corporation Xeon E7 v4/Xeon E5 v4/Xeon E3 v4/Xeon D Power Control Unit)\s*(\(rev\s*05\))?',
    r'(?i)(?P<bdf>ff:1e.3)\s*(?P<device_class>System peripheral):\s*(?P<device_name>Intel Corporation Xeon E7 v4/Xeon E5 v4/Xeon E3 v4/Xeon D Power Control Unit)\s*(\(rev\s*05\))?',
    r'(?i)(?P<bdf>ff:1e.4)\s*(?P<device_class>System peripheral):\s*(?P<device_name>Intel Corporation Xeon E7 v4/Xeon E5 v4/Xeon E3 v4/Xeon D Power Control Unit)\s*(\(rev\s*05\))?',
    r'(?i)(?P<bdf>ff:1f.0)\s*(?P<device_class>System peripheral):\s*(?P<device_name>Intel Corporation Xeon E7 v4/Xeon E5 v4/Xeon E3 v4/Xeon D Power Control Unit)\s*(\(rev\s*05\))?',
    r'(?i)(?P<bdf>ff:1f.2)\s*(?P<device_class>System peripheral):\s*(?P<device_name>Intel Corporation Xeon E7 v4/Xeon E5 v4/Xeon E3 v4/Xeon D Power Control Unit)\s*(\(rev\s*05\))?',
]

pci_mgmt_patterns = pci_uefi_patterns[28:35]
pci_030_pattern = pci_diag_patterns[28]
pci_031_pattern = pci_diag_patterns[29]
pci_040_pattern = pci_diag_patterns[30]
pci_041_pattern = pci_diag_patterns[31]
pci_050_pattern = pci_diag_patterns[32]
pci_080_pattern = pci_diag_patterns[33]
pci_090_pattern = pci_diag_patterns[34]

advance_last_line = r'(?i)Intel.*F2:'

i210_last_line = r'Virtual MAC Address.*:\w+\s*\|F9: Optimized Defaults'
i210_patterns = [
    r'(?i)Device Name\s*(?P<device_name>Intel\(R\) I210 Gigabit)',
    r'(?i)Chip Type\s*(?P<chip_type>Intel i210)',
    r'(?i)PCI Device ID\s*(?P<device_id>1537)',
    r'(?i)PCI Address\s*(?P<pci_address>09:00:00)'
]

ethernet_last_line = r'Virtual MAC Address.*:\w+\s*\|F10: Save & Exit'
ethernet030_patterns = [
    r'(?i)Device Name\s*(?P<device_name>Intel\(R\) Ethernet)',
    r'(?i)Chip Type\s*(?P<chip_type>Intel X550)',
    r'(?i)PCI Device ID\s*(?P<device_id>15AB)',
    r'(?i)PCI Address\s*(?P<pci_address>03:00:00)'
]
ethernet031_patterns = [
    r'(?i)Device Name\s*(?P<device_name>Intel\(R\) Ethernet)',
    r'(?i)Chip Type\s*(?P<chip_type>Intel X550)',
    r'(?i)PCI Device ID\s*(?P<device_id>15AB)',
    r'(?i)PCI Address\s*(?P<pci_address>03:00:01)'
]
ethernet040_patterns = [
    r'(?i)Device Name\s*(?P<device_name>Intel\(R\) Ethernet)',
    r'(?i)Chip Type\s*(?P<chip_type>Intel X550)',
    r'(?i)PCI Device ID\s*(?P<device_id>15AB)',
    r'(?i)PCI Address\s*(?P<pci_address>04:00:00)'
]
ethernet041_patterns = [
    r'(?i)Device Name\s*(?P<device_name>Intel\(R\) Ethernet)',
    r'(?i)Chip Type\s*(?P<chip_type>Intel X550)',
    r'(?i)PCI Device ID\s*(?P<device_id>15AB)',
    r'(?i)PCI Address\s*(?P<pci_address>04:00:01)'
]

i2c_all_bus_patterns = [r'/dev/(?P<i2c_bus>i2c-0)\s*:[\r\n\s\w:\-]+40: -- -- -- -- 44 -- -- -- 48[\r\n\s\w:\-]+50: -- -- -- -- -- -- UU']
for i in range (17, 151):
    if i in [39, 40, 63, 64, 84, 127, 128]:
        continue
    elif i in [89, 90, 91, 92, 93, 94, 95, 96, 97, 98, 99, 100, 101, 102, 103, 104]:
        i2c_all_bus_patterns.append(r'/dev/(?P<i2c_bus>i2c-%d)\s*:[\r\n\s\w:\-]+50: UU[\r\n\s\w:\-]+70: UU UU --'%i)
    else:
        i2c_all_bus_patterns.append(r'/dev/(?P<i2c_bus>i2c-%d)\s*:[\r\n\s\w:\-]+50: UU[\r\n\s\w:\-]+70: UU UU UU'%i)

cpld_c_hex_ver = hex(int(cpld_c_new_version, 16))
cpld_b_hex_ver = hex(int(cpld_b_new_version, 16))

pch_sata_last_line = r'SATA Device Type.*F9: Optimized Defaults'
sata_config_patterns = [
    r'(?i)SATA Controller.*(?P<SATA_ctrl>Enabled)',
    r'(?i)Configure SATA as.*(?P<SATA_mode>AHCI)',
]

boot_usb_pattern = r'(?i)(?P<USB_device>UEFI:\\s*\\w+.*,\\s*Partition\\s*\\d+)'
dir_last_line = r'Dir\\(s\\)'
usb_uefi_path = r'FS0:'
usb_diag_path = r'(?P<USB_device>\\/dev\\/sdb1)'

bios_post_info_patterns = [
    r'(?i)(?P<BIOS_date>BIOS Date: %s)'%(bios_date_pattern),
    r'(?i)(?P<BIOS_ver>Ver: %s)'%(bios_version_pattern),
    proc_type_pattern,
    proc_speed_pattern,
    r'(?i)Total Memory Installed:\s*(?P<memory_size_gb>%s\s*GB)\s*\((?P<memory_type>%s)\)'%(mem_size_gb, mem_type),
    r'(?i)(?P<CPLD_C_ver>CPLD_C  Ver: %d\.%d)'%(int(cpld_c_new_version[-2], 16), int(cpld_c_new_version[-1], 16)),
    r'(?i)(?P<CPLD_B_ver>CPLD_B  Ver: %d\.%d)'%(int(cpld_b_new_version[-2], 16), int(cpld_b_new_version[-1], 16)),
    r'(?i)(?P<USB_devices>USB Devices total: \d+ KBDs, \d+ MICE, \d+ MASS, \d+ HUBs)',
    r'(?i)(?P<BIOS_copyrights>Version [\d\.]+ Copyright \(C\) \d{4} American Megatrends, Inc\.)',
]

bbs_last_line = r'ESC to boot using defaults.*\|'

intel_setup_last_line = r'Reserve Memory.*-'
security_last_line = r'User Password.*F2: Previous Values'
pch_config_last_line = r'PCH SATA Configuration.*'
help_last_line = r'(?i)Ok.*\\|'
load_previous_line = r'Load Previous Values\\?'
load_optimized_line = r'Load Optimized Defaults\\?'
cores_en_3_pattern = r'Cores Enabled\\s+3'
cores_en_1_pattern = r'Cores Enabled\\s+1'
cores_en_0_pattern = r'Cores Enabled\\s+0'

system_date_pattern = r'System Date.*\\w{3} (?P<system_date>\\d{2}/\\d{2}/\\d{4})'
system_time_pattern = r'System Time.*(?P<system_time>\\d{2}:\\d{2}:\\d{2})'
mm_test = '09'
dd_test = '14'
yy_test = '2021'
hr_test = '16'
min_test = '00'
sec_test = '01'

diagos_dmidecode_t1_patterns = [
    r"(?m)^[ \\t]*Product Name: (?P<dmi_name>.*)",
    r"(?m)^[ \\t]*Version: (?P<dmi_version>.*)",
    r"(?m)^[ \\t]*SKU Number: (?P<dmi_sku>.*)",
    r"(?m)^[ \\t]*Family: (?P<dmi_family>.*)",
]
diagos_dmidecode_t2_patterns = [
    r"(?m)^[ \\t]*Manufacturer: (?P<dmi_mfg>.*)",
    r"(?m)^[ \\t]*Version: (?P<dmi_version>.*)",
    r"(?m)^[ \\t]*Serial Number: (?P<dmi_serial>.*)",
    r"(?m)^[ \\t]*Asset Tag: (?P<dmi_asset_tag>.*)",
]

create_pass_pattern = r'--Create New Password--'
current_pass_pattern = r'--Enter Current Password--'
confirm_pass_pattern = r'--Confirm New Password--'
invalid_pass_pattern = r'(?i)Invalid password'
clear_pass_pattern = r'Clear Old Password\. Continue\?'

level_admin_pattern = r'(?i)Access Level.*(?P<access_level>Administrator)'
level_user_pattern = r'(?i)Access Level.*(?P<access_level>User)'

advance_power_mgmt_last_line = r'(?i)DRAM RAPL Configuration.*>'
cpu_cstate_last_line = r'(?i)OS ACPI Cx.*-'

cpu_cstate_patterns = [
    r'(?i)CPU C State.*(?P<cpu_cstate>Disable)',
    r'(?i)CPU C6 report.*(?P<cpu_c6_report>Disable)',
    r'(?i)Enhanced Halt State.*(?P<enh_halt_state>Disable)',
    r'(?i)Package C State limit.*(?P<pkg_cstate_limit>C0\/C1 state)'
]

cpu_hwpm_last_line = r'(?i)Enable CPU HWP.*performance'
cpu_hwpm_patterns = r'(?i)Enable CPU HWP.*(?P<cpu_hwpm>Disable)'

eist_patterns = r'(?i)EIST \\(P-states\\).*(?P<eist_pstate>Disable)'

cstate_sonic_patterns = [
    r'(?P<proc_cstate>processor\.max_cstate=0)',
    r'(?P<intel_idle>intel_idle\.max_cstate=0)'
]

cpu_pstate_last_line = r'(?i)Turbo Mode.*MSR'
cpu_pstate_patterns = r'(?i)Turbo Mode.*(?P<turbo_mode>Disable)'

cpu_tstate_last_line = r'(?i)ACPI T-States.*Throttling'
cpu_tstate_patterns = r'(?i)ACPI T-States.*(?P<acpi_tstate>Disable)'

pcie_aspm_last_line = r'(?i)PCI Express.*-'
pcie_aspm_patterns = r'(?i)PCI-E ASPM Support.*(?P<pcie_aspm>Disable)\\]'

sub_2a_last_line = r'(?i)Found.*Device. TCG EFI'
sub_2b_last_line = r'(?i)Console Redirection Settings.*Enter: Select'
sub_2b_1_last_line = r'(?i)Putty keyPad.*-'
sub_2b_2_last_line = r'(?i)Stop Bits EMS.*above,'
sub_2c_last_line = r'(?i)SR-IOV Support.*Disables'
sub_2d_last_line = r'(?i)USB hardware delays.*F1:'
sub_2e_last_line = r'(?i)Network Stack.*Enable\/Disable UEFI'
sub_2f_last_line = r'(?i)Other PCI devices.*-'

sub_3a_last_line = proc_config_last_line
sub_3a_1_last_line = cores_en_patterns
sub_3b_last_line = advance_power_mgmt_last_line
sub_3b_2_last_line = cpu_hwpm_last_line
sub_3b_3_last_line = cpu_cstate_last_line
sub_3b_4_last_line = cpu_tstate_last_line
sub_3b_5_last_line = r'(?i)Program PowerCTL_MSR.*\|'
sub_3b_5_1_last_line = r'(?i)Averaging Time Window.*\|'
sub_3b_5_2_last_line = r'(?i)Energy Efficient Turbo.*\|'
sub_3b_6_last_line = r'(?i)DRAM RAPL Extended.*\|'
sub_3c_last_line = r'(?i)Numa.*\|'
sub_3d_last_line = r'(?i)Memory RAS Configuration.*\|'
sub_3d_1_last_line = r'(?i)SODIMM.*\|'
sub_3d_2_last_line = r'(?i)Set Throttling Mode.*\|'
sub_3d_3_last_line = r'(?i)Reservation.*\|'
sub_3d_4_last_line = r'(?i)Management.*\|'
sub_3e_last_line = r'(?i)PCI-E ASPM Support.*\|'

sub_3e_1_last_line = r'(?i)IOU2 Non-Posted.*\|'
sub_3e_1_1_last_line = r'(?i)PCI-E ASPM Support.*\|'
sub_3e_2_last_line = r'(?i)I\/O.*the I\/O device'

sub_3f_last_line = pch_config_last_line
sub_3f_1_last_line = r'(?i)PCH state after G3.*\|'
sub_3f_2_last_line = r'(?i)PCI Express Root Port.*-'
sub_3f_2_1_last_line = r'(?i)MSI.*\|'
sub_3f_3_last_line = pch_sata_last_line

sub_3g_last_line = r'(?i)TargetVGA.*\|'
sub_3h_last_line = me_config_last_line
sub_3i_last_line = r'(?i)PCI Error Enabling.*\|'
sub_3i_1_last_line = r'(?i)WHEA Support.*\|'
sub_3i_2_last_line = r'(?i)Spare Interrupt.*\|'
sub_3i_3_last_line = r'(?i)DMA Errors.*\|'
sub_3i_4_last_line = r'(?i)Pcie Extended errors.*\|'
sub_3j_last_line = r'(?i)Reserve TAGEC Memory.*\|'

sub_4a_last_line = r'(?i)HDD Master Pwd Status.*F9:'
sub_4b_last_line = r'(?i)Key Management.*\|'
sub_4b_1_last_line = r'(?i)Authorized TimeStamps.*F10:'

boot_last_line = r'(?i)Boot Option #\\d+\\s+\\[(.+)\\*?\\|'

ru_last_line = r'Press any key to continue'
ru_32_bit_last_line2 = r'F0 (\w{8}\s){4}.*(ROM:)*'
select_space_pattern = r'UEFI variable.*<ALT'
io_space_pattern = r'Type:IO Space.*Start 0500'
window_pattern = r'([01]{8}\s){4}.*(\n.*)+(31\s+28\s+24\s+20\s+16\s+12\s+8\s+4.*)'
index_pattern = r'(31\s+28\s+24\s+20\s+16\s+12\s+8\s+4.*)'

gpio_0_31_list = ['8', '9', '10', '14', '15', '18', '19']
gpio_32_63_list = ['32', '50', '51', '54']
gpio_65_95_list = ['70']
gpio_0_31_target_dict = {'GPIO'+k : '1' for k in gpio_0_31_list}
gpio_32_63_target_dict = {'GPIO'+k : '1' for k in gpio_32_63_list}
gpio_65_95_target_dict = {'GPIO'+k : '1' for k in gpio_65_95_list}
gpio_0_31_io_dict = {
    'GPIO8' : '0',
    'GPIO9' : '0',
    'GPIO10' : '1',
    'GPIO14' : '0',
    'GPIO15' : '0',
    'GPIO18' : '0',
    'GPIO19' : '1',
}
gpio_32_63_io_dict = {
    'GPIO32' : '0',
    'GPIO50' : '1',
    'GPIO51' : '1',
    'GPIO54' : '1',
}
gpio_65_95_io_dict = {
    'GPIO70' : '1',
}

gpio_0_31_val_dict = {
    'GPIO8' : '1',
    'GPIO9' : '1',
    'GPIO10' : '0',
    'GPIO14' : '0',
    'GPIO15' : '0',
    'GPIO18' : '1',
    'GPIO19' : '1',
}
gpio_32_63_val_dict = {
    'GPIO32' : '1',
    'GPIO50' : '1',
    'GPIO51' : '1',
    'GPIO54' : '0',
}
gpio_65_95_val_dict = {
    'GPIO70' : '0',
}

ali_version_test_command = './cel-version-test -S'
ali_mem_test_command = './cel-mem-test -l'

####################### Shamu #############################
import os
devicename = os.environ.get("deviceName", "").lower()
import logging
logging.info("devicename:{}".format(devicename))
if "shamu" in devicename:
    diag_util_cpu_path = '/usr/local/CPU_Diag/utility/'
    smbios_eeprom_path = diag_util_cpu_path + 'SMBIOS_fru_eeprom'
    tlv_eeprom_path = diag_util_cpu_path + 'CPU_tlv_eeprom'
    tlv_eeprom_cmd = 'show platform syseeprom'

    diag_cpu_path = '/usr/local/CPU_Diag/bin/'
    i2c_all_bus_patterns = [
        'QSFP_\d.*?61\s*0x50\s*OK'
    ]
    for i in range(62,101):
        i2c_all_bus_patterns.append('QSFP_\d.*?%d\s*0x50\s*OK'%i)
    ali_version_test_command = './cel-software-test -i'
    ali_mem_test_command = './cel-memory-test -t'
    pci_mgmt_patterns = [
        r'(?i)\s*(?P<bdf>00   02   00    00)\s+==>\s+(?P<device_class>Processors - Co-processor)[\r|\n]+.+Vendor\s*(?P<vendor_id>8086)\s*Device\s*(?P<device_id>6F54)\s*(Prog Interface 0)',
        r'(?i)\s*(?P<bdf>00   03   00    00)\s+==>\s+(?P<device_class>Network Controller - Ethernet controller)[\r|\n]+.+Vendor\s*(?P<vendor_id>8086)\s*Device\s*(?P<device_id>15AB)\s*(Prog Interface 0)',
        r'(?i)\s*(?P<bdf>00   03   00    01)\s+==>\s+(?P<device_class>Network Controller - Ethernet controller)[\r|\n]+.+Vendor\s*(?P<vendor_id>8086)\s*Device\s*(?P<device_id>15AB)\s*(Prog Interface 0)',
        r'(?i)\s*(?P<bdf>00   04   00    00)\s+==>\s+(?P<device_class>Network Controller - Ethernet controller)[\r|\n]+.+Vendor\s*(?P<vendor_id>8086)\s*Device\s*(?P<device_id>15AB)\s*(Prog Interface 0)',
        r'(?i)\s*(?P<bdf>00   04   00    01)\s+==>\s+(?P<device_class>Network Controller - Ethernet controller)[\r|\n]+.+Vendor\s*(?P<vendor_id>8086)\s*Device\s*(?P<device_id>15AB)\s*(Prog Interface 0)',
        r'(?i)\s*(?P<bdf>00   09   00    00)\s+==>\s+(?P<device_class>Network Controller - Ethernet controller)[\r|\n]+.+Vendor\s*(?P<vendor_id>8086)\s*Device\s*(?P<device_id>1537)\s*(Prog Interface 0)',
    ]
    pci_050_pattern = r'(?i)(?P<bdf>05:00.0)\s*(?P<device_class>Ethernet controller):\s*(?P<device_name>Broadcom Limited Device b780).*?'
    pci_080_pattern = r'(?i)(?P<bdf>08:00.0)\s*(?P<device_class>Memory controller):\s*(?P<device_name>Device 1ded:4303).*?'
    pci_uefi_patterns = [
        r'(?i)\s*(?P<bdf>00   00   00    00)\s+==>\s+(?P<device_class>Bridge Device - Host/PCI bridge)[\r|\n]+.+Vendor\s*(?P<vendor_id>8086)\s*Device\s*(?P<device_id>6F00)\s*(Prog Interface 0)',
        r'(?i)\s*(?P<bdf>00   00   01    00)\s+==>\s+(?P<device_class>Bridge Device - PCI/PCI bridge)[\r|\n]+.+Vendor\s*(?P<vendor_id>8086)\s*Device\s*(?P<device_id>6F02)\s*(Prog Interface 0)',
        r'(?i)\s*(?P<bdf>00   00   02    00)\s+==>\s+(?P<device_class>Bridge Device - PCI/PCI bridge)[\r|\n]+.+Vendor\s*(?P<vendor_id>8086)\s*Device\s*(?P<device_id>6F04)\s*(Prog Interface 0)',
        r'(?i)\s*(?P<bdf>00   00   02    02)\s+==>\s+(?P<device_class>Bridge Device - PCI/PCI bridge)[\r|\n]+.+Vendor\s*(?P<vendor_id>8086)\s*Device\s*(?P<device_id>6F06)\s*(Prog Interface 0)',
        r'(?i)\s*(?P<bdf>00   00   02    03)\s+==>\s+(?P<device_class>Bridge Device - PCI/PCI bridge)[\r|\n]+.+Vendor\s*(?P<vendor_id>8086)\s*Device\s*(?P<device_id>6F07)\s*(Prog Interface 0)',

        r'(?i)\s*(?P<bdf>00   00   03    00)\s+==>\s+(?P<device_class>Bridge Device - PCI/PCI bridge)[\r|\n]+.+Vendor\s*(?P<vendor_id>8086)\s*Device\s*(?P<device_id>6F08)\s*(Prog Interface 0)',
        r'(?i)\s*(?P<bdf>00   00   03    01)\s+==>\s+(?P<device_class>Bridge Device - PCI/PCI bridge)[\r|\n]+.+Vendor\s*(?P<vendor_id>8086)\s*Device\s*(?P<device_id>6F09)\s*(Prog Interface 0)',
        r'(?i)\s*(?P<bdf>00   00   03    02)\s+==>\s+(?P<device_class>Bridge Device - PCI/PCI bridge)[\r|\n]+.+Vendor\s*(?P<vendor_id>8086)\s*Device\s*(?P<device_id>6F0A)\s*(Prog Interface 0)',

        r'(?i)\s*(?P<bdf>00   00   04    00)\s+==>\s+(?P<device_class>Base System Peripherals - Other system peripheral)[\r|\n]+.+Vendor\s*(?P<vendor_id>8086)\s*Device\s*(?P<device_id>6F20)\s*(Prog Interface 0)',
        r'(?i)\s*(?P<bdf>00   00   04    01)\s+==>\s+(?P<device_class>Base System Peripherals - Other system peripheral)[\r|\n]+.+Vendor\s*(?P<vendor_id>8086)\s*Device\s*(?P<device_id>6F21)\s*(Prog Interface 0)',
        r'(?i)\s*(?P<bdf>00   00   04    02)\s+==>\s+(?P<device_class>Base System Peripherals - Other system peripheral)[\r|\n]+.+Vendor\s*(?P<vendor_id>8086)\s*Device\s*(?P<device_id>6F22)\s*(Prog Interface 0)',
        r'(?i)\s*(?P<bdf>00   00   04    03)\s+==>\s+(?P<device_class>Base System Peripherals - Other system peripheral)[\r|\n]+.+Vendor\s*(?P<vendor_id>8086)\s*Device\s*(?P<device_id>6F23)\s*(Prog Interface 0)',
        r'(?i)\s*(?P<bdf>00   00   04    04)\s+==>\s+(?P<device_class>Base System Peripherals - Other system peripheral)[\r|\n]+.+Vendor\s*(?P<vendor_id>8086)\s*Device\s*(?P<device_id>6F24)\s*(Prog Interface 0)',
        r'(?i)\s*(?P<bdf>00   00   04    05)\s+==>\s+(?P<device_class>Base System Peripherals - Other system peripheral)[\r|\n]+.+Vendor\s*(?P<vendor_id>8086)\s*Device\s*(?P<device_id>6F25)\s*(Prog Interface 0)',
        r'(?i)\s*(?P<bdf>00   00   04    06)\s+==>\s+(?P<device_class>Base System Peripherals - Other system peripheral)[\r|\n]+.+Vendor\s*(?P<vendor_id>8086)\s*Device\s*(?P<device_id>6F26)\s*(Prog Interface 0)',
        r'(?i)\s*(?P<bdf>00   00   04    07)\s+==>\s+(?P<device_class>Base System Peripherals - Other system peripheral)[\r|\n]+.+Vendor\s*(?P<vendor_id>8086)\s*Device\s*(?P<device_id>6F27)\s*(Prog Interface 0)',

        r'(?i)\s*(?P<bdf>00   00   05    00)\s+==>\s+(?P<device_class>Base System Peripherals - Other system peripheral)[\r|\n]+.+Vendor\s*(?P<vendor_id>8086)\s*Device\s*(?P<device_id>6F28)\s*(Prog Interface 0)',
        r'(?i)\s*(?P<bdf>00   00   05    01)\s+==>\s+(?P<device_class>Base System Peripherals - Other system peripheral)[\r|\n]+.+Vendor\s*(?P<vendor_id>8086)\s*Device\s*(?P<device_id>6F29)\s*(Prog Interface 0)',
        r'(?i)\s*(?P<bdf>00   00   05    02)\s+==>\s+(?P<device_class>Base System Peripherals - Other system peripheral)[\r|\n]+.+Vendor\s*(?P<vendor_id>8086)\s*Device\s*(?P<device_id>6F2A)\s*(Prog Interface 0)',
        r'(?i)\s*(?P<bdf>00   00   05    04)\s+==>\s+(?P<device_class>Base System Peripherals - PIC)[\r|\n]+.+Vendor\s*(?P<vendor_id>8086)\s*Device\s*(?P<device_id>6F2C)\s*(Prog Interface 20)',

        r'(?i)\s*(?P<bdf>00   00   14    00)\s+==>\s+(?P<device_class>Serial Bus Controllers - USB)[\r|\n]+.+Vendor\s*(?P<vendor_id>8086)\s*Device\s*(?P<device_id>8C31)\s*(Prog Interface 30)',
        r'(?i)\s*(?P<bdf>00   00   1C    00)\s+==>\s+(?P<device_class>Bridge Device - PCI/PCI bridge)[\r|\n]+.+Vendor\s*(?P<vendor_id>8086)\s*Device\s*(?P<device_id>8C10)\s*(Prog Interface 0)',
        r'(?i)\s*(?P<bdf>00   00   1C    02)\s+==>\s+(?P<device_class>Bridge Device - PCI/PCI bridge)[\r|\n]+.+Vendor\s*(?P<vendor_id>8086)\s*Device\s*(?P<device_id>8C14)\s*(Prog Interface 0)',
        r'(?i)\s*(?P<bdf>00   00   1D    00)\s+==>\s+(?P<device_class>Serial Bus Controllers - USB)[\r|\n]+.+Vendor\s*(?P<vendor_id>8086)\s*Device\s*(?P<device_id>8C26)\s*(Prog Interface 20)',
        r'(?i)\s*(?P<bdf>00   00   1F    00)\s+==>\s+(?P<device_class>Bridge Device - PCI/ISA bridge)[\r|\n]+.+Vendor\s*(?P<vendor_id>8086)\s*Device\s*(?P<device_id>8C54)\s*(Prog Interface 0)',
        r'(?i)\s*(?P<bdf>00   00   1F    02)\s+==>\s+(?P<device_class>Mass Storage Controller - Serial ATA controller)[\r|\n]+.+Vendor\s*(?P<vendor_id>8086)\s*Device\s*(?P<device_id>8C02)\s*(Prog Interface 1)',
        r'(?i)\s*(?P<bdf>00   00   1F    03)\s+==>\s+(?P<device_class>Serial Bus Controllers - System Management Bus)[\r|\n]+.+Vendor\s*(?P<vendor_id>8086)\s*Device\s*(?P<device_id>8C22)\s*(Prog Interface 0)',

        r'(?i)\s*(?P<bdf>00   02   00    00)\s+==>\s+(?P<device_class>Processors - Co-processor)[\r|\n]+.+Vendor\s*(?P<vendor_id>8086)\s*Device\s*(?P<device_id>6F54)\s*(Prog Interface 0)',
        r'(?i)\s*(?P<bdf>00   03   00    00)\s+==>\s+(?P<device_class>Network Controller - Ethernet controller)[\r|\n]+.+Vendor\s*(?P<vendor_id>8086)\s*Device\s*(?P<device_id>15AB)\s*(Prog Interface 0)',
        r'(?i)\s*(?P<bdf>00   03   00    01)\s+==>\s+(?P<device_class>Network Controller - Ethernet controller)[\r|\n]+.+Vendor\s*(?P<vendor_id>8086)\s*Device\s*(?P<device_id>15AB)\s*(Prog Interface 0)',
        r'(?i)\s*(?P<bdf>00   04   00    00)\s+==>\s+(?P<device_class>Network Controller - Ethernet controller)[\r|\n]+.+Vendor\s*(?P<vendor_id>8086)\s*Device\s*(?P<device_id>15AB)\s*(Prog Interface 0)',
        r'(?i)\s*(?P<bdf>00   04   00    01)\s+==>\s+(?P<device_class>Network Controller - Ethernet controller)[\r|\n]+.+Vendor\s*(?P<vendor_id>8086)\s*Device\s*(?P<device_id>15AB)\s*(Prog Interface 0)',
        r'(?i)\s*(?P<bdf>00   05   00    00)\s+==>\s+(?P<device_class>Network Controller - Ethernet controller)[\r|\n]+.+Vendor\s*(?P<vendor_id>14E4)\s*Device\s*(?P<device_id>B780)\s*(Prog Interface 0)',
        r'(?i)\s*(?P<bdf>00   08   00    00)\s+==>\s+(?P<device_class>Memory Controller - Other memory controller)[\r|\n]+.+Vendor\s*(?P<vendor_id>1DED)\s*Device\s*(?P<device_id>4303)\s*(Prog Interface 0)',
        r'(?i)\s*(?P<bdf>00   09   00    00)\s+==>\s+(?P<device_class>Network Controller - Ethernet controller)[\r|\n]+.+Vendor\s*(?P<vendor_id>8086)\s*Device\s*(?P<device_id>1537)\s*(Prog Interface 0)',
    ]
    pci_diag_patterns = [
        r'(?i)(?P<bdf>00:00.0)\s*(?P<device_class>Host bridge):\s*(?P<device_name>Intel Corporation Xeon E7 v4/Xeon E5 v4/Xeon E3 v4/Xeon D DMI2)\s*(\(rev\s*05\))?',
        r'(?i)(?P<bdf>00:01.0)\s*(?P<device_class>PCI bridge):\s*(?P<device_name>Intel Corporation Xeon E7 v4/Xeon E5 v4/Xeon E3 v4/Xeon D PCI Express Root Port 1)\s*(\(rev\s*05\))?',
        r'(?i)(?P<bdf>00:02.0)\s*(?P<device_class>PCI bridge):\s*(?P<device_name>Intel Corporation Xeon E7 v4/Xeon E5 v4/Xeon E3 v4/Xeon D PCI Express Root Port 2)\s*(\(rev\s*05\))?',
        r'(?i)(?P<bdf>00:02.2)\s*(?P<device_class>PCI bridge):\s*(?P<device_name>Intel Corporation Xeon E7 v4/Xeon E5 v4/Xeon E3 v4/Xeon D PCI Express Root Port 2)\s*(\(rev\s*05\))?',
        r'(?i)(?P<bdf>00:02.3)\s*(?P<device_class>PCI bridge):\s*(?P<device_name>Intel Corporation Xeon E7 v4/Xeon E5 v4/Xeon E3 v4/Xeon D PCI Express Root Port 2)\s*(\(rev\s*05\))?',
        r'(?i)(?P<bdf>00:03.0)\s*(?P<device_class>PCI bridge):\s*(?P<device_name>Intel Corporation Xeon E7 v4/Xeon E5 v4/Xeon E3 v4/Xeon D PCI Express Root Port 3)\s*(\(rev\s*05\))?',
        r'(?i)(?P<bdf>00:03.1)\s*(?P<device_class>PCI bridge):\s*(?P<device_name>Intel Corporation Xeon E7 v4/Xeon E5 v4/Xeon E3 v4/Xeon D PCI Express Root Port 3)\s*(\(rev\s*05\))?',
        r'(?i)(?P<bdf>00:03.2)\s*(?P<device_class>PCI bridge):\s*(?P<device_name>Intel Corporation Xeon E7 v4/Xeon E5 v4/Xeon E3 v4/Xeon D PCI Express Root Port 3)\s*(\(rev\s*05\))?',

        r'(?i)(?P<bdf>00:04.0)\s*(?P<device_class>System peripheral):\s*(?P<device_name>Intel Corporation Xeon E7 v4/Xeon E5 v4/Xeon E3 v4/Xeon D Crystal Beach DMA Channel 0)\s*(\(rev\s*05\))?',
        r'(?i)(?P<bdf>00:04.1)\s*(?P<device_class>System peripheral):\s*(?P<device_name>Intel Corporation Xeon E7 v4/Xeon E5 v4/Xeon E3 v4/Xeon D Crystal Beach DMA Channel 1)\s*(\(rev\s*05\))?',
        r'(?i)(?P<bdf>00:04.2)\s*(?P<device_class>System peripheral):\s*(?P<device_name>Intel Corporation Xeon E7 v4/Xeon E5 v4/Xeon E3 v4/Xeon D Crystal Beach DMA Channel 2)\s*(\(rev\s*05\))?',
        r'(?i)(?P<bdf>00:04.3)\s*(?P<device_class>System peripheral):\s*(?P<device_name>Intel Corporation Xeon E7 v4/Xeon E5 v4/Xeon E3 v4/Xeon D Crystal Beach DMA Channel 3)\s*(\(rev\s*05\))?',
        r'(?i)(?P<bdf>00:04.4)\s*(?P<device_class>System peripheral):\s*(?P<device_name>Intel Corporation Xeon E7 v4/Xeon E5 v4/Xeon E3 v4/Xeon D Crystal Beach DMA Channel 4)\s*(\(rev\s*05\))?',
        r'(?i)(?P<bdf>00:04.5)\s*(?P<device_class>System peripheral):\s*(?P<device_name>Intel Corporation Xeon E7 v4/Xeon E5 v4/Xeon E3 v4/Xeon D Crystal Beach DMA Channel 5)\s*(\(rev\s*05\))?',
        r'(?i)(?P<bdf>00:04.6)\s*(?P<device_class>System peripheral):\s*(?P<device_name>Intel Corporation Xeon E7 v4/Xeon E5 v4/Xeon E3 v4/Xeon D Crystal Beach DMA Channel 6)\s*(\(rev\s*05\))?',
        r'(?i)(?P<bdf>00:04.7)\s*(?P<device_class>System peripheral):\s*(?P<device_name>Intel Corporation Xeon E7 v4/Xeon E5 v4/Xeon E3 v4/Xeon D Crystal Beach DMA Channel 7)\s*(\(rev\s*05\))?',

        r'(?i)(?P<bdf>00:05.0)\s*(?P<device_class>System peripheral):\s*(?P<device_name>Intel Corporation Xeon E7 v4/Xeon E5 v4/Xeon E3 v4/Xeon D Map/VTd_Misc/System Management)\s*(\(rev\s*05\))?',
        r'(?i)(?P<bdf>00:05.1)\s*(?P<device_class>System peripheral):\s*(?P<device_name>Intel Corporation Xeon E7 v4/Xeon E5 v4/Xeon E3 v4/Xeon D IIO Hot Plug)\s*(\(rev\s*05\))?',
        r'(?i)(?P<bdf>00:05.2)\s*(?P<device_class>System peripheral):\s*(?P<device_name>Intel Corporation Xeon E7 v4/Xeon E5 v4/Xeon E3 v4/Xeon D IIO RAS/Control Status/Global Errors)\s*(\(rev\s*05\))?',
        r'(?i)(?P<bdf>00:05.4)\s*(?P<device_class>PIC):\s*(?P<device_name>Intel Corporation Xeon E7 v4/Xeon E5 v4/Xeon E3 v4/Xeon D I/O APIC)\s*(\(rev\s*05\))?',

        r'(?i)(?P<bdf>00:14.0)\s*(?P<device_class>USB controller):\s*(?P<device_name>Intel Corporation 8 Series/C220 Series Chipset Family USB xHCI)\s*(\(rev\s*05\))?',
        r'(?i)(?P<bdf>00:1c.0)\s*(?P<device_class>PCI bridge):\s*(?P<device_name>Intel Corporation 8 Series/C220 Series Chipset Family PCI Express Root Port #1)\s*(\(rev\s*05\))?',
        r'(?i)(?P<bdf>00:1c.2)\s*(?P<device_class>PCI bridge):\s*(?P<device_name>Intel Corporation 8 Series/C220 Series Chipset Family PCI Express Root Port #3)\s*(\(rev\s*05\))?',
        r'(?i)(?P<bdf>00:1d.0)\s*(?P<device_class>USB controller):\s*(?P<device_name>Intel Corporation 8 Series/C220 Series Chipset Family USB EHCI #1)\s*(\(rev\s*05\))?',
        r'(?i)(?P<bdf>00:1f.0)\s*(?P<device_class>ISA bridge):\s*(?P<device_name>Intel Corporation C224 Series Chipset Family Server Standard SKU LPC Controller)\s*(\(rev\s*05\))?',
        r'(?i)(?P<bdf>00:1f.2)\s*(?P<device_class>SATA controller):\s*(?P<device_name>Intel Corporation 8 Series/C220 Series Chipset Family 6-port SATA Controller 1 \[AHCI mode\])\s*(\(rev\s*05\))?',
        r'(?i)(?P<bdf>00:1f.3)\s*(?P<device_class>SMBus):\s*(?P<device_name>Intel Corporation 8 Series/C220 Series Chipset Family SMBus Controller)\s*(\(rev\s*05\))?',

        r'(?i)(?P<bdf>02:00.0)\s*(?P<device_class>Co-processor):\s*(?P<device_name>Intel Corporation Device 6f54)\s*(\(rev\s*05\))?',
        r'(?i)(?P<bdf>03:00.0)\s*(?P<device_class>Ethernet controller):\s*(?P<device_name>Intel Corporation Ethernet Connection X552 10 GbE Backplane)\s*(\(rev\s*05\))?',
        r'(?i)(?P<bdf>03:00.1)\s*(?P<device_class>Ethernet controller):\s*(?P<device_name>Intel Corporation Ethernet Connection X552 10 GbE Backplane)\s*(\(rev\s*05\))?',
        r'(?i)(?P<bdf>04:00.0)\s*(?P<device_class>Ethernet controller):\s*(?P<device_name>Intel Corporation Ethernet Connection X552 10 GbE Backplane)\s*(\(rev\s*05\))?',
        r'(?i)(?P<bdf>04:00.1)\s*(?P<device_class>Ethernet controller):\s*(?P<device_name>Intel Corporation Ethernet Connection X552 10 GbE Backplane)\s*(\(rev\s*05\))?',
        r'(?i)(?P<bdf>05:00.0)\s*(?P<device_class>Ethernet controller):\s*(?P<device_name>Broadcom Limited Device b780).*?',
        r'(?i)(?P<bdf>08:00.0)\s*(?P<device_class>Memory controller):\s*(?P<device_name>Device 1ded:4303).*?',
        r'(?i)(?P<bdf>09:00.0)\s*(?P<device_class>Ethernet controller):\s*(?P<device_name>Intel Corporation I210 Gigabit Backplane Connection)\s*(\(rev\s*03\))?',

        r'(?i)(?P<bdf>ff:0b.0)\s*(?P<device_class>System peripheral):\s*(?P<device_name>Intel Corporation Xeon E7 v4/Xeon E5 v4/Xeon E3 v4/Xeon D R3 QPI Link 0/1)\s*(\(rev\s*05\))?',
        r'(?i)(?P<bdf>ff:0b.1)\s*(?P<device_class>Performance counters):\s*(?P<device_name>Intel Corporation Xeon E7 v4/Xeon E5 v4/Xeon E3 v4/Xeon D R3 QPI Link 0/1)\s*(\(rev\s*05\))?',
        r'(?i)(?P<bdf>ff:0b.2)\s*(?P<device_class>Performance counters):\s*(?P<device_name>Intel Corporation Xeon E7 v4/Xeon E5 v4/Xeon E3 v4/Xeon D R3 QPI Link 0/1)\s*(\(rev\s*05\))?',
        r'(?i)(?P<bdf>ff:0b.3)\s*(?P<device_class>System peripheral):\s*(?P<device_name>Intel Corporation Xeon E7 v4/Xeon E5 v4/Xeon E3 v4/Xeon D R3 QPI Link Debug)\s*(\(rev\s*05\))?',

        r'(?i)(?P<bdf>ff:0c.0)\s*(?P<device_class>System peripheral):\s*(?P<device_name>Intel Corporation Xeon E7 v4/Xeon E5 v4/Xeon E3 v4/Xeon D Caching Agent)\s*(\(rev\s*05\))?',
        r'(?i)(?P<bdf>ff:0c.1)\s*(?P<device_class>System peripheral):\s*(?P<device_name>Intel Corporation Xeon E7 v4/Xeon E5 v4/Xeon E3 v4/Xeon D Caching Agent)\s*(\(rev\s*05\))?',
        r'(?i)(?P<bdf>ff:0c.2)\s*(?P<device_class>System peripheral):\s*(?P<device_name>Intel Corporation Xeon E7 v4/Xeon E5 v4/Xeon E3 v4/Xeon D Caching Agent)\s*(\(rev\s*05\))?',
        r'(?i)(?P<bdf>ff:0c.3)\s*(?P<device_class>System peripheral):\s*(?P<device_name>Intel Corporation Xeon E7 v4/Xeon E5 v4/Xeon E3 v4/Xeon D Caching Agent)\s*(\(rev\s*05\))?',
        r'(?i)(?P<bdf>ff:0c.4)\s*(?P<device_class>System peripheral):\s*(?P<device_name>Intel Corporation Xeon E7 v4/Xeon E5 v4/Xeon E3 v4/Xeon D Caching Agent)\s*(\(rev\s*05\))?',
        r'(?i)(?P<bdf>ff:0c.5)\s*(?P<device_class>System peripheral):\s*(?P<device_name>Intel Corporation Xeon E7 v4/Xeon E5 v4/Xeon E3 v4/Xeon D Caching Agent)\s*(\(rev\s*05\))?',

        r'(?i)(?P<bdf>ff:0f.0)\s*(?P<device_class>System peripheral):\s*(?P<device_name>Intel Corporation Xeon E7 v4/Xeon E5 v4/Xeon E3 v4/Xeon D Caching Agent)\s*(\(rev\s*05\))?',
        r'(?i)(?P<bdf>ff:0f.4)\s*(?P<device_class>System peripheral):\s*(?P<device_name>Intel Corporation Xeon E7 v4/Xeon E5 v4/Xeon E3 v4/Xeon D Caching Agent)\s*(\(rev\s*05\))?',
        r'(?i)(?P<bdf>ff:0f.5)\s*(?P<device_class>System peripheral):\s*(?P<device_name>Intel Corporation Xeon E7 v4/Xeon E5 v4/Xeon E3 v4/Xeon D Caching Agent)\s*(\(rev\s*05\))?',
        r'(?i)(?P<bdf>ff:0f.6)\s*(?P<device_class>System peripheral):\s*(?P<device_name>Intel Corporation Xeon E7 v4/Xeon E5 v4/Xeon E3 v4/Xeon D Caching Agent)\s*(\(rev\s*05\))?',

        r'(?i)(?P<bdf>ff:10.0)\s*(?P<device_class>System peripheral):\s*(?P<device_name>Intel Corporation Xeon E7 v4/Xeon E5 v4/Xeon E3 v4/Xeon D R2PCIe Agent)\s*(\(rev\s*05\))?',
        r'(?i)(?P<bdf>ff:10.1)\s*(?P<device_class>Performance counters):\s*(?P<device_name>Intel Corporation Xeon E7 v4/Xeon E5 v4/Xeon E3 v4/Xeon D R2PCIe Agent)\s*(\(rev\s*05\))?',
        r'(?i)(?P<bdf>ff:10.5)\s*(?P<device_class>System peripheral):\s*(?P<device_name>Intel Corporation Xeon E7 v4/Xeon E5 v4/Xeon E3 v4/Xeon D Ubox)\s*(\(rev\s*05\))?',
        r'(?i)(?P<bdf>ff:10.6)\s*(?P<device_class>Performance counters):\s*(?P<device_name>Intel Corporation Xeon E7 v4/Xeon E5 v4/Xeon E3 v4/Xeon D Ubox)\s*(\(rev\s*05\))?',
        r'(?i)(?P<bdf>ff:10.7)\s*(?P<device_class>System peripheral):\s*(?P<device_name>Intel Corporation Xeon E7 v4/Xeon E5 v4/Xeon E3 v4/Xeon D Ubox)\s*(\(rev\s*05\))?',

        r'(?i)(?P<bdf>ff:13.0)\s*(?P<device_class>System peripheral):\s*(?P<device_name>Intel Corporation Xeon E7 v4/Xeon E5 v4/Xeon E3 v4/Xeon D Memory Controller 0 - Target Address/Thermal/RAS)\s*(\(rev\s*05\))?',
        r'(?i)(?P<bdf>ff:13.1)\s*(?P<device_class>System peripheral):\s*(?P<device_name>Intel Corporation Xeon E7 v4/Xeon E5 v4/Xeon E3 v4/Xeon D Memory Controller 0 - Target Address/Thermal/RAS)\s*(\(rev\s*05\))?',
        r'(?i)(?P<bdf>ff:13.2)\s*(?P<device_class>System peripheral):\s*(?P<device_name>Intel Corporation Xeon E7 v4/Xeon E5 v4/Xeon E3 v4/Xeon D Memory Controller 0 - Channel Target Address Decoder)\s*(\(rev\s*05\))?',
        r'(?i)(?P<bdf>ff:13.3)\s*(?P<device_class>System peripheral):\s*(?P<device_name>Intel Corporation Xeon E7 v4/Xeon E5 v4/Xeon E3 v4/Xeon D Memory Controller 0 - Channel Target Address Decoder)\s*(\(rev\s*05\))?',
        r'(?i)(?P<bdf>ff:13.4)\s*(?P<device_class>System peripheral):\s*(?P<device_name>Intel Corporation Xeon E7 v4/Xeon E5 v4/Xeon E3 v4/Xeon D Memory Controller 0 - Channel Target Address Decoder)\s*(\(rev\s*05\))?',
        r'(?i)(?P<bdf>ff:13.5)\s*(?P<device_class>System peripheral):\s*(?P<device_name>Intel Corporation Xeon E7 v4/Xeon E5 v4/Xeon E3 v4/Xeon D Memory Controller 0 - Channel Target Address Decoder)\s*(\(rev\s*05\))?',
        r'(?i)(?P<bdf>ff:13.6)\s*(?P<device_class>System peripheral):\s*(?P<device_name>Intel Corporation Xeon E7 v4/Xeon E5 v4/Xeon E3 v4/Xeon D DDRIO Channel 0/1 Broadcast)\s*(\(rev\s*05\))?',
        r'(?i)(?P<bdf>ff:13.7)\s*(?P<device_class>System peripheral):\s*(?P<device_name>Intel Corporation Xeon E7 v4/Xeon E5 v4/Xeon E3 v4/Xeon D DDRIO Global Broadcast)\s*(\(rev\s*05\))?',

        r'(?i)(?P<bdf>ff:14.0)\s*(?P<device_class>System peripheral):\s*(?P<device_name>Intel Corporation Xeon E7 v4/Xeon E5 v4/Xeon E3 v4/Xeon D Memory Controller 0 - Channel 0 Thermal Control)\s*(\(rev\s*05\))?',
        r'(?i)(?P<bdf>ff:14.1)\s*(?P<device_class>System peripheral):\s*(?P<device_name>Intel Corporation Xeon E7 v4/Xeon E5 v4/Xeon E3 v4/Xeon D Memory Controller 0 - Channel 1 Thermal Control)\s*(\(rev\s*05\))?',
        r'(?i)(?P<bdf>ff:14.2)\s*(?P<device_class>System peripheral):\s*(?P<device_name>Intel Corporation Xeon E7 v4/Xeon E5 v4/Xeon E3 v4/Xeon D Memory Controller 0 - Channel 0 Error)\s*(\(rev\s*05\))?',
        r'(?i)(?P<bdf>ff:14.3)\s*(?P<device_class>System peripheral):\s*(?P<device_name>Intel Corporation Xeon E7 v4/Xeon E5 v4/Xeon E3 v4/Xeon D Memory Controller 0 - Channel 1 Error)\s*(\(rev\s*05\))?',
        r'(?i)(?P<bdf>ff:14.4)\s*(?P<device_class>System peripheral):\s*(?P<device_name>Intel Corporation Xeon E7 v4/Xeon E5 v4/Xeon E3 v4/Xeon D DDRIO Channel 0/1 Interface)\s*(\(rev\s*05\))?',
        r'(?i)(?P<bdf>ff:14.5)\s*(?P<device_class>System peripheral):\s*(?P<device_name>Intel Corporation Xeon E7 v4/Xeon E5 v4/Xeon E3 v4/Xeon D DDRIO Channel 0/1 Interface)\s*(\(rev\s*05\))?',
        r'(?i)(?P<bdf>ff:14.6)\s*(?P<device_class>System peripheral):\s*(?P<device_name>Intel Corporation Xeon E7 v4/Xeon E5 v4/Xeon E3 v4/Xeon D DDRIO Channel 0/1 Interface)\s*(\(rev\s*05\))?',
        r'(?i)(?P<bdf>ff:14.7)\s*(?P<device_class>System peripheral):\s*(?P<device_name>Intel Corporation Xeon E7 v4/Xeon E5 v4/Xeon E3 v4/Xeon D DDRIO Channel 0/1 Interface)\s*(\(rev\s*05\))?',

        r'(?i)(?P<bdf>ff:15.0)\s*(?P<device_class>System peripheral):\s*(?P<device_name>Intel Corporation Xeon E7 v4/Xeon E5 v4/Xeon E3 v4/Xeon D Memory Controller 0 - Channel 2 Thermal Control)\s*(\(rev\s*05\))?',
        r'(?i)(?P<bdf>ff:15.1)\s*(?P<device_class>System peripheral):\s*(?P<device_name>Intel Corporation Xeon E7 v4/Xeon E5 v4/Xeon E3 v4/Xeon D Memory Controller 0 - Channel 3 Thermal Control)\s*(\(rev\s*05\))?',
        r'(?i)(?P<bdf>ff:15.2)\s*(?P<device_class>System peripheral):\s*(?P<device_name>Intel Corporation Xeon E7 v4/Xeon E5 v4/Xeon E3 v4/Xeon D Memory Controller 0 - Channel 2 Error)\s*(\(rev\s*05\))?',
        r'(?i)(?P<bdf>ff:15.3)\s*(?P<device_class>System peripheral):\s*(?P<device_name>Intel Corporation Xeon E7 v4/Xeon E5 v4/Xeon E3 v4/Xeon D Memory Controller 0 - Channel 3 Error)\s*(\(rev\s*05\))?',

        r'(?i)(?P<bdf>ff:1e.0)\s*(?P<device_class>System peripheral):\s*(?P<device_name>Intel Corporation Xeon E7 v4/Xeon E5 v4/Xeon E3 v4/Xeon D Power Control Unit)\s*(\(rev\s*05\))?',
        r'(?i)(?P<bdf>ff:1e.1)\s*(?P<device_class>System peripheral):\s*(?P<device_name>Intel Corporation Xeon E7 v4/Xeon E5 v4/Xeon E3 v4/Xeon D Power Control Unit)\s*(\(rev\s*05\))?',
        r'(?i)(?P<bdf>ff:1e.2)\s*(?P<device_class>System peripheral):\s*(?P<device_name>Intel Corporation Xeon E7 v4/Xeon E5 v4/Xeon E3 v4/Xeon D Power Control Unit)\s*(\(rev\s*05\))?',
        r'(?i)(?P<bdf>ff:1e.3)\s*(?P<device_class>System peripheral):\s*(?P<device_name>Intel Corporation Xeon E7 v4/Xeon E5 v4/Xeon E3 v4/Xeon D Power Control Unit)\s*(\(rev\s*05\))?',
        r'(?i)(?P<bdf>ff:1e.4)\s*(?P<device_class>System peripheral):\s*(?P<device_name>Intel Corporation Xeon E7 v4/Xeon E5 v4/Xeon E3 v4/Xeon D Power Control Unit)\s*(\(rev\s*05\))?',
        r'(?i)(?P<bdf>ff:1f.0)\s*(?P<device_class>System peripheral):\s*(?P<device_name>Intel Corporation Xeon E7 v4/Xeon E5 v4/Xeon E3 v4/Xeon D Power Control Unit)\s*(\(rev\s*05\))?',
        r'(?i)(?P<bdf>ff:1f.2)\s*(?P<device_class>System peripheral):\s*(?P<device_name>Intel Corporation Xeon E7 v4/Xeon E5 v4/Xeon E3 v4/Xeon D Power Control Unit)\s*(\(rev\s*05\))?',
    ]
