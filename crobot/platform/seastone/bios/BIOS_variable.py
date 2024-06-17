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
import DeviceMgr
from SwImage import SwImage
dev_info = DeviceMgr.getDevice()

from Const import BOOT_MODE_UBOOT, BOOT_MODE_DIAGOS, BOOT_MODE_ONIE,ONIE_RESCUE_MODE
dev_info = DeviceMgr.getDevice()
mgmt_ip = dev_info.managementIP

SEASTONE = SwImage.getSwImage("SEASTONE_BIOS")

seastone_bios_new_image=SEASTONE.newImage
seastone_bios_old_image=SEASTONE.oldImage

seastone_bmc_image = SEASTONE.newVersion['bmc_image']
AfuEfix64_file=SEASTONE.newVersion['Afuefix64_file']
afulnx_64_image = SEASTONE.newVersion['afulnx_64_image']
stress_file=SEASTONE.newVersion['stress_file']
memtest_file = SEASTONE.newVersion['memtest_image']
cel_diag_image=SEASTONE.newVersion['cel_diag_image']


pc_info = DeviceMgr.getServerInfo('PC')
scp_ip = pc_info.managementIP
scp_username = pc_info.scpUsername
scp_password = pc_info.scpPassword
dhcp_username = pc_info.username
dhcp_password = pc_info.password
dhcp_prompt = pc_info.prompt

microcode_revision_code = 'revision=(\S+)'

main_menu_pattern_check_1="American Megatrends"+"||"+seastone_bios_new_image[:-4]+"||"


bios_setup_memory_speed='2400'

main_menu_test_data_1= 'American Megatrends||8192 MB (DDR4)||English||'+seastone_bios_new_image[:-4]+'||5.13'

cel_diag_upgrade = './cel-upgrade-test --update  -d 5 -f ../firmware/bmc/'+seastone_bmc_image
reset_cause_reboot='(0x44)'
reset_cause_power_chasis = '(0x33)'
reset_cause_power_reset='(0x22)'

memory_speed = 'Memory Speed = '

memtest_file = SEASTONE.newVersion['memtest_image']
 

memory_speed_general='2400'

password_keys={
    '1':'KEY_1',
    '2':'KEY_2',
    '3':'KEY_3',
    '4':'KEY_4'
}



pattern_ifconfig=["RX errors\s+(\S+)", "TX errors\s+(\S+)"]

uefi_shell_command="AfuEfix64.efi "+seastone_bios_new_image+" /p /b /n /x /me /k"

management_port_command='00   07   00    01 ==> Network Controller - Ethernet controller'

pattern_dmidecode_memory= ["Total Width: 72 bits", "Data Width: 72 bits", "Size: 8192 MB", "Form Factor: DIMM","Locator: DIMM0","Bank Locator: BANK 0","Type: DDR4","Speed: 3200 MT/s",  "Manufacturer: InnoDisk", "Asset Tag: BANK 0 DIMM0 AssetTag", " Minimum Voltage: 1.2 V", "Maximum Voltage: 1.2 V", "Configured Voltage: 1.2 V"]

pattern_pxe_server=["Checking Media Presence", "Media Present","Media Present","Start PXE over IPv4","Station IP address is (\S+\.\S+\.\S+\.\S+)", "Station IP address is (\S+\.\S+\.\S+\.\S+)", "NBP filename is bootx64\.efi","NBP filesize is 9022976 Bytes", "Downloading NBP file", "NBP file downloaded successfully"]

pattern_bmc_information_setup=['BMC Device ID\s+(\S+)', 'BMC Device Revision\s+(\S+)','IPMI Version\s+(\S+)']

pattern_bmc_information_os=['Device ID\s+:\s+(\S+)','Device Revision\s+:\s+(\S+)','Version\s+:\s+(\S+)']

pattern_check_bios_setup=["BIOS Vendor\s+(\S+\s\S+)","Project Version\s+(\S+)","Build Date and Time\s+(\S+\s\S+)"]

pattern_check_bios_post_log=['(American Megatrends)',"Ver:\s+(\S+)","BIOS Date:\s+(\S+\s\S+)"]

pattern_check_bios_dmidecode=["Vendor:\s+(\S+\s\S+)","Version:\s+(\S+)"]

pattern_date_and_time=["System Date\s+(\S+\s\S+)","System Time\s+(\S+)"]

pattern_management_port_pci=['02   00    00','03   00    00']

pattern_management_port_lspci=['02:00','03:00']

pattern_main_menu=["BIOS Vendor\s+(\S+\s\S+)","Project Version\s+(\S+)"]

main_menu_items=["BIOS Vendor\s+(\S+\s\S+)",'Total Memory\s+(\S+\s+\S+\s+\S+)',"Project Version\s+(\S+)","Core Version\s+(\S+)","System Date\s+(\S+\s\S+)","System Time\s+(\S+)"]

commands_in_s0_state_test=["fdisk -l", " ls -l", "lspci", "i2cdetect -l"]

pattern_reset_cause='Reset cause(\S+):'

lanplus_ipmitool_cmd='ipmitool -I lanplus -H '+ mgmt_ip + ' -U admin -P admin {}'

sel_list_power_on_pattern = [r"working | Asserted"]

pattern_bmc_information_advanced_option=["Device Name\s+(\S+\s+\S+\s+\S+)","PCI Device ID\s+(\S+)","PCI Address\s+(\S+)","Chip Type\s+(\S+\s+\S+)","Adapter PBA\s+(\S+)", "UEFI Driver\s+(\S+\s+\S+)" ]



pci_result=['00   00   00    00 ==> Bridge Device - Host/PCI bridge', '             Vendor 8086 Device 1980 Prog Interface 0', '    00   00   04    00 ==> Bridge Device - Host/PCI bridge', '             Vendor 8086 Device 19A1 Prog Interface 0', '    00   00   05    00 ==> Base System Peripherals - Root Complex Event Collector', '             Vendor 8086 Device 19A2 Prog Interface 0', '    00   00   06    00 ==> Bridge Device - PCI/PCI bridge', '             Vendor 8086 Device 19A3 Prog Interface 0', '    00   00   09    00 ==> Bridge Device - PCI/PCI bridge', '             Vendor 8086 Device 19A4 Prog Interface 0', '    00   00   0B    00 ==> Bridge Device - PCI/PCI bridge', '             Vendor 8086 Device 19A6 Prog Interface 0', '    00   00   0C    00 ==> Bridge Device - PCI/PCI bridge', '             Vendor 8086 Device 19A7 Prog Interface 0', '    00   00   0E    00 ==> Bridge Device - PCI/PCI bridge', '             Vendor 8086 Device 19A8 Prog Interface 0', '    00   00   10    00 ==> Bridge Device - PCI/PCI bridge', '             Vendor 8086 Device 19AA Prog Interface 0', '    00   00   12    00 ==> Base System Peripherals - Other system peripheral', '             Vendor 8086 Device 19AC Prog Interface 0', '    00   00   14    00 ==> Mass Storage Controller - Serial ATA controller', '             Vendor 8086 Device 19C2 Prog Interface 1', '    00   00   15    00 ==> Serial Bus Controllers - USB', '             Vendor 8086 Device 19D0 Prog Interface 30', '    00   00   16    00 ==> Bridge Device - PCI/PCI bridge', '             Vendor 8086 Device 19D1 Prog Interface 0', '    00   00   18    00 ==> Simple Communications Controllers - Other communication device', '             Vendor 8086 Device 19D3 Prog Interface 0', '    00   00   1A    00 ==> Simple Communications Controllers - Serial controller', '             Vendor 8086 Device 19D8 Prog Interface 2', '    00   00   1A    01 ==> Simple Communications Controllers - Serial controller', '             Vendor 8086 Device 19D8 Prog Interface 2', '    00   00   1A    02 ==> Simple Communications Controllers - Serial controller', '             Vendor 8086 Device 19D8 Prog Interface 2', '    00   00   1C    00 ==> Base System Peripherals - SD Host controller', '             Vendor 8086 Device 19DB Prog Interface 1', '    00   00   1F    00 ==> Bridge Device - PCI/ISA bridge', '             Vendor 8086 Device 19DC Prog Interface 0', '    00   00   1F    02 ==> Memory Controller - Other memory controller', '             Vendor 8086 Device 19DE Prog Interface 0', '    00   00   1F    04 ==> Serial Bus Controllers - System Management Bus', '             Vendor 8086 Device 19DF Prog Interface 0', '    00   00   1F    05 ==> Serial Bus Controllers - Other bus type', '             Vendor 8086 Device 19E0 Prog Interface 0', '    00   01   00    00 ==> Processors - Co-processor', '             Vendor 8086 Device 19E2 Prog Interface 0', '    00   02   00    00 ==> Network Controller - Ethernet controller', '             Vendor 14E4 Device B870 Prog Interface 0', '00   03   00    00 ==> Network Controller - Ethernet controller', '             Vendor 8086 Device 1533 Prog Interface 0', '    00   06   00    00 ==> Memory Controller - Other memory controller', '             Vendor 10EE Device 7021 Prog Interface 0', '    00   07   00    00 ==> Network Controller - Ethernet controller', '             Vendor 8086 Device 15C2 Prog Interface 0', '    00   07   00    01 ==> Network Controller - Ethernet controller', '             Vendor 8086 Device 15C2 Prog Interface 0']

seastone_home_path = "8080/SEASTONE/"

bmc_file_path = seastone_bmc_image

ic2_info_error_pattern_list = [r"I2C Test All.*|.*FAIL.*|", r"Error performing I2C Test All.", r"Status_Code = 0x01010100000002", r"Status = FAIL"]

new_bios_image = seastone_bios_new_image
old_bios_image = seastone_bios_old_image
cfuflash_path = "BMC/CFUFLASH"
afulnx_path = "afulnx_64"
lscpi_pattern = ["00:00.0 Host bridge: Intel Corporation Device 1980",
"00:04.0 Host bridge: Intel Corporation Device 19a1",
"00:05.0 Generic system peripheral \[0807\]: Intel Corporation Device 19a2",
"00:06.0 PCI bridge: Intel Corporation Device 19a3",
"00:09.0 PCI bridge: Intel Corporation Device 19a4",
"00:0b.0 PCI bridge: Intel Corporation Device 19a6",
"00:0c.0 PCI bridge: Intel Corporation Device 19a7",
"00:0e.0 PCI bridge: Intel Corporation Device 19a8",
"00:10.0 PCI bridge: Intel Corporation Device 19aa",
"00:12.0 System peripheral: Intel Corporation DNV SMBus Contoller - Host",
"00:14.0 SATA controller: Intel Corporation DNV SATA Controller 1",
"00:15.0 USB controller: Intel Corporation Atom Processor C3000 Series USB 3.0 xHCI Controller",
"00:16.0 PCI bridge: Intel Corporation Device 19d1",
"00:18.0 Communication controller: Intel Corporation Device 19d3",
"00:1a.0 Serial controller: Intel Corporation Device 19d8",
"00:1a.1 Serial controller: Intel Corporation Device 19d8",
"00:1a.2 Serial controller: Intel Corporation Device 19d8",
"00:1c.0 SD Host controller: Intel Corporation Device 19db",
"00:1f.0 ISA bridge: Intel Corporation DNV LPC or eSPI",
"00:1f.2 Memory controller: Intel Corporation Device 19de",
"00:1f.4 SMBus: Intel Corporation DNV SMBus controller",
"00:1f.5 Serial bus controller \[0c80\]: Intel Corporation DNV SPI Controller",
"01:00.0 Co-processor: Intel Corporation Atom Processor C3000 Series QuickAssist Technology",
"02:00.0 Ethernet controller: Broadcom Limited Device b870",
"03:00.0 Ethernet controller: Intel Corporation I210 Gigabit Network Connection",
"06:00.0 Memory controller: Xilinx Corporation Device 7021",
"07:00.0 Ethernet controller: Intel Corporation Ethernet Connection X553 Backplane",
"07:00.1 Ethernet controller: Intel Corporation Ethernet Connection X553 Backplane",
]

smbios_list = [0,2,3,4,7,17]
smbios_bios_res = ["BIOS Information",
        "Vendor: American Megatrends Inc.",
        "Version: "+seastone_bios_new_image[:-4],
        "Runtime Size: 64 kB",
        "ROM Size: 8192 kB",
        "BIOS Revision: 5.13"]
sbmios_baseboard_res = ["Base Board Information",
        "Manufacturer: Celestica",
        "Product Name: R4039-G0002-01",
        "Version: 04",
        "Serial Number: b4:db:91:d0:df:34",
        "Asset Tag: R4041-G0007-01",
        "Chassis Handle: 0x0003",
        "Type: Motherboard"]

smbios_chassis_res = ["Chassis Information",
        "Manufacturer: Celestica",
        "Type: <OUT OF SPEC>",
        "Lock: Present|Not Present",
        "Version: 01",
        "Serial Number: SN12345678",
        "Asset Tag: R4039-F9001-01",
        "Boot-up State: Safe",
        "Power Supply State: Safe",
        "Thermal State: Safe",
        "Security Status: None",
        "OEM Information: 0x00000000",
        "Height: Unspecified",
        "Number Of Power Cords: 1",
        "Contained Elements: 0",
        "SKU Number: Default string"]

symbios_processor_res = ["Processor Information",
        "Socket Designation: CPU0",
        "Type: Central Processor",
        "Family: Pentium 4",
        "Manufacturer: Intel.*Corporation",
        "ID: F1 06 05 00 FF FB EB BF",
        "Signature: Type 0, Family 6, Model 95, Stepping 1",
        "Flags:",
                "FPU.*Floating-point unit on-chip",
                "VME.*Virtual mode extension",
                "DE.*Debugging extension",
                "PSE.*Page size extension",
                "TSC.*Time stamp counter",
                "MSR.*Model specific registers",
                "PAE.*Physical address extension",
                "MCE.*Machine check exception",
                "CX8.*CMPXCHG8 instruction supported",
                "APIC.*On-chip APIC hardware supported",
                "SEP.*Fast system call",
                "MTRR.*Memory type range registers",
                "PGE.*Page global enable",
                "MCA.*Machine check architecture",
                "CMOV.*Conditional move instruction supported",
                "PAT.*Page attribute table",
                "PSE-36.*36-bit page size extension",
                "CLFSH.*CLFLUSH instruction supported",
                "DS.*Debug store",
                "ACPI.*ACPI supported",
                "MMX.*MMX technology supported",
                "FXSR.*FXSAVE and FXSTOR instructions supported",
                "SSE.*Streaming SIMD extensions",
                "SSE2.*Streaming SIMD extensions 2",
                "SS.*Self-snoop",
                "HTT.*Multi-threading",
                "TM.*Thermal monitor supported",
                "PBE.*Pending break enabled",
        "Version: Intel.*Atom.*CPU C3558R @ 2.40GHz",
        "Voltage: 1.6 V",
        "External Clock: 100 MHz",
        "Max Speed: 2400 MHz",
        "Current Speed: 2400 MHz",
        "Status: Populated, Enabled",
        "Upgrade: Socket LGA775",
        "L1 Cache Handle: 0x001E",
        "L2 Cache Handle: 0x001F",
        "L3 Cache Handle: Not Provided",
        "Serial Number: Not Specified",
        "Asset Tag: UNKNOWN",
        "Part Number: Not Specified",
        "Core Count: 4",
        "Core Enabled: 4",
        "Thread Count: 4"]

smbios_cache_res = ["Cache Information",
        "Socket Designation: L1-Cache",
        "Configuration: Enabled, Not Socketed, Level 1",
        "Operational Mode: Write Back",
        "Location: Internal",
        "Installed Size: ",
        "Maximum Size: ",
        "Supported SRAM Types:",
                "Synchronous",
        "Installed SRAM Type: Synchronous",
        "Speed: Unknown",
        "Error Correction Type: Single-bit ECC",
        "System Type: Instruction",
        "Associativity: 8-way Set-associative",
"Handle 0x001F, DMI type 7, .*bytes",
"Cache Information",
        "Socket Designation: L2-Cache",
        "Configuration: Enabled, Not Socketed, Level 2",
        "Operational Mode: Write Back",
        "Location: Internal",
        "Installed Size: ",
        "Maximum Size: ",
        "Supported SRAM Types:",
                "Synchronous",
        "Installed SRAM Type: Synchronous",

        "Error Correction Type: Single-bit ECC",
        "System Type: Unified",
        "Associativity: 16-way Set-associative"]


smbios_memory_res = ["Memory Device",
        "Array Handle: 0x0019",
        "Total Width: 72 bits",
        "Data Width: 72 bits",
        "Size: 8192 MB",
        "Form Factor: DIMM",

        "Locator: DIMM0",
        "Bank Locator: BANK 0",
        "Type: DDR4",
        "Type Detail: Synchronous Unbuffered",
        "Speed: 3200 MT/s",
        "Manufacturer: InnoDisk",
        "Serial Number: 1B810006",
        "Asset Tag: BANK 0 DIMM0 AssetTag",
        "Part Number: M4D0-8GS1PCEM",
        "Rank: 1",
        "Configured Memory Speed: 2400 MT/s",
        "Minimums Voltage: 1.2 V",
        "Maximum Voltage: 1.2 V",
        "Configured Voltage: 1.2 V",
"Handle 0x001D, DMI type 17, 40 bytes",
"Memory Device",
        "Array Handle: 0x0019",
        "Error Information Handle: Not Provided",
        "Total Width: Unknown",
        "Data Width: Unknown",
        "Size: No Module Installed",
        "Form Factor: DIMM",
        "Locator: DIMM1",
        "Bank Locator: BANK 0",
        "Type: Unknown",
        "Type Detail: Unknown",
        "Speed: Unknown",
        "Manufacturer: NO DIMM",
        "Serial Number: NO DIMM",
        "Asset Tag: NO DIMM",
        "Part Number: NO DIMM",
        "Rank: Unknown",
        "Configured Memory Speed: Unknown",
        "Minimum Voltage: Unknown",
        "Maximum Voltage: Unknown",
        "Configured Voltage: Unknown"]

unmount_disk_pattern = ["umount:.*not mounted"]
brixia_pass = "brixia@cls"


#############################
cpu_proc=[]
for i in range(0,4):
    cpu_proc.append('processor\s*:\s*'+str(i))
    cpu_proc.append('vendor_id.*:.*GenuineIntel')
    cpu_proc.append('cpu family.*:.*6')
    cpu_proc.append('model.*:.*')
    cpu_proc.append('model name.*:.*Intel\(R\) Atom\(TM\) CPU C3558R @ 2.40GHz')
    cpu_proc.append('stepping.*:.*[0-9]')
    cpu_proc.append('microcode.*:.*0x.*')
    cpu_proc.append('cpu cores.*:.*4')
    cpu_proc.append('fpu.*:.*yes')
    cpu_proc.append('fpu_exception.*:.*yes')
    cpu_proc.append('cpuid level.*:.*21')
    cpu_proc.append('wp.*:.*yes')

serial_port=[]
serial_port.append('Console Redirection.*\[.*\]')
serial_port.append('Console Redirection Settings')
serial_port.append('Legacy Console Redirection')
serial_port.append('Legacy Console Redirection Settings')

console_settings=[]
console_settings.append('Terminal Type.*\[VT100\+\]')
console_settings.append('Bits per second.*\[115200|9600\]')
console_settings.append('Data.*\[8\]')
console_settings.append('Parity.*\[None\]')
console_settings.append('Stop Bits.*\[1\]')

legacy_settings=[]
legacy_settings.append('Redirection COM Port')
legacy_settings.append('Resolution.*\[80x24|5\]')
legacy_settings.append('Redirect After POST.*\[(Always Enable)|(BootLoader)\]')


mainmenu_RC=[]
mainmenu_RC.append("Platform\s+Harcuvar")
mainmenu_RC.append("RC Revision")
mainmenu_RC.append("Processor BSP\s+506F1")
mainmenu_RC.append("Microcode Revision")
mainmenu_RC.append("Relax Security\s+\[(En|Dis)abled\]")
mainmenu_RC.append("Processor Configuration")
mainmenu_RC.append("Server ME Configuration")
mainmenu_RC.append("North Bridge Chipset Configuration")
mainmenu_RC.append("South Bridge Chipset Configuration")

processor_config=[]
processor_config.append("Processor ID")
processor_config.append("Processor Frequency")
processor_config.append("CPU BCLK Frequency")
processor_config.append("L1 Cache RAM")
processor_config.append("L2 Cache RAM")
processor_config.append("Processor Version")
processor_config.append("EIST \(.*GV3.*\)")
processor_config.append("TM1")
processor_config.append("TM2 Mode")
processor_config.append("CPU C State")

me_config=[]
me_config.append("Operational Firmware")
me_config.append("ME Firmware Type")
me_config.append("Backup Firmware")
me_config.append("Recovery Firmware")
me_config.append("ME Firmware Features")
me_config.append("ME Firmware Status #1")
me_config.append("ME Firmware Status #2")
me_config.append("Current State")
me_config.append("Error Code")

north_bridge_config=[]
north_bridge_config.append("Memory Information")
north_bridge_config.append("MRC Version")
north_bridge_config.append("Total Memory")
north_bridge_config.append("Memory Frequency")
#north_bridge_config.append("Fast Boot")
north_bridge_config.append("Memory Frequency")
north_bridge_config.append("ECC Support")

south_bridge_config=[]
south_bridge_config.append("SATA Configuration")
south_bridge_config.append("Disable S5 support")
south_bridge_config.append("State After G3")
south_bridge_config.append("SMBUS Controller")
south_bridge_config.append("SMBus Host Speed")
south_bridge_config.append("GPIO Status")

sata_config_south_bridge=[]
sata_config_south_bridge.append("Enable controller")
sata_config_south_bridge.append("Speed limit")

setup_cpu_info=[]
setup_cpu_info.append('Processor ID\s+000506F1')
setup_cpu_info.append('Processor Frequency\s+2.400GHz')
setup_cpu_info.append('CPU BCLK Frequency\s+100MHz')
setup_cpu_info.append('L1 Cache RAM\s+56KB')
setup_cpu_info.append('L2 Cache RAM\s+2048KB')
setup_cpu_info.append('Processor Version\s+Intel\(R\)\s+Atom\(TM\)\s+CPU')

sel_entry_count_setup=0
log_entry_count_os=0
updated_sel_entry_count=0

#boot_menu_content=''

re_boot_menu_content=[]
re_boot_menu_content.append('Setup Prompt Timeout(.*)')
re_boot_menu_content.append('Bootup NumLock State(.*)')
re_boot_menu_content.append('Quiet Boot(.*)')
#re_boot_menu_content.append('Boot Option Priorities(.*)')
re_boot_menu_content.append('Boot Option #[0-9](.*)')
re_boot_menu_content.append('New Boot Option(.*)')
re_boot_menu_content.append('Hard Drive BBS Priorities(.*)')



#boot1_name=''
shell_scroll_count=0
lap1_bmc_log_count=0
lap2_bmc_log_count=0

memtester_re=[]
for i in range(1):
    memtester_re.append('Loop {}\/1'.format(i+1))
    memtester_re.append('Stuck Address.*:.*ok')
    memtester_re.append('Random Value.*:.*ok')
    memtester_re.append('Compare XOR.*:.*ok')
    memtester_re.append('Compare SUB.*.*ok')
    memtester_re.append('Compare MUL.*:.*ok')
    memtester_re.append('Compare DIV.*:.*ok')
    memtester_re.append('Compare OR.*:.*ok')
    memtester_re.append('Compare AND.*:.*ok')
    memtester_re.append('Sequential Increment.*:.*ok')
    memtester_re.append('Solid Bits.*:.*ok')
    memtester_re.append('Block Sequential.*:.*ok')
    memtester_re.append('Checkerboard.*:.*ok')
    memtester_re.append('Bit Spread.*:.*ok')
    memtester_re.append('Bit Flip.*:.*ok')
    memtester_re.append('Walking Ones.*:.*ok')
    memtester_re.append('Walking Zeroes.*:.*ok')
    memtester_re.append('8-bit Writes.*:.*ok')
    memtester_re.append('16-bit Writes.*:.*ok')

#bios_version_re='Seastone2V2.1.00.02'

post_re=[]
post_re.append('Version.*2\.19\.1266.*Copyright.*\(C\).*2023.*American.*Megatrends,.*Inc\.')
#line2='BIOS.*Date:.*Ver:.*'+bios_version_re
#post_re.append(line2)
#post_re.append('.*Ver:.*')

sata_write_re=[]
sata_write_re.append('[0-9]\+[0-9]\s+records in')
sata_write_re.append('[0-9]\+[0-9]\s+records out')
sata_write_re.append('[0-9]+ bytes copied,.*')

boot_option_dict={'ONL':'(Open Network Linux)|(ONL OS)', 'ONIE':'ONIE OS', 'USB':'USB.*Partition','AMI Virtual CDROM0':'', 'P4 M2':'\(S80\).*3IE7', 'Shell':'UEFI: Built-in EFI','Disabled':'Disabled'}
#option_list=['ONL','ONIE','USB', 'AMI Virtual CDROM0', 'P4','Shell', 'Disabled']








fdisk_op_re=[]
fdisk_op_re.append('Device.*Size.*Type')
fdisk_op_re.append('\/dev\/sda1.*[0-9]+(M|G).*EFI System')
fdisk_op_re.append('\/dev\/sda2.*[0-9]+(M|G).*ONIE boot')
fdisk_op_re.append('\/dev\/sda3.*[0-9]+(M|G).*Microsoft basic data')
fdisk_op_re.append('\/dev\/sda4.*[0-9]+(M|G).*Microsoft basic data')
fdisk_op_re.append('\/dev\/sda5.*[0-9]+(M|G).*Microsoft basic data')
fdisk_op_re.append('\/dev\/sda6.*[0-9]+(M|G).*Microsoft basic data')


lspci_op_re=[]
lspci_op_re.append('.+')
#lspci_op_re.append('00\:00\.0 Host bridge\: Intel Corporation Device 1980 \(rev 11\) 00\:04\.0 Host bridge\: Intel Corporation Device 19a1 \(rev 11\) 00\:05\.0 Generic system peripheral \[0807\]\: Intel Corporation Device 19a2 \(rev 11\) 00\:06\.0 PCI bridge\: Intel Corporation Device 19a3 \(rev 11\) 00\:09\.0 PCI bridge\: Intel Corporation Device 19a4 \(rev 11\) 00\:0b\.0 PCI bridge\: Intel Corporation Device 19a6 \(rev 11\) 00\:0c\.0 PCI bridge\: Intel Corporation Device 19a7 \(rev 11\) 00\:0e\.0 PCI bridge\: Intel Corporation Device 19a8 \(rev 11\) 00\:10\.0 PCI bridge\: Intel Corporation Device 19aa \(rev 11\) 00\:12\.0 System peripheral\: Intel Corporation DNV SMBus Contoller \- Host \(rev 11\) 00\:14\.0 SATA controller\: Intel Corporation DNV SATA Controller 1 \(rev 11\) 00\:15\.0 USB controller\: Intel Corporation Atom Processor C3000 Series USB 3\.0 xHCI Controller \(rev 11\) 00\:16\.0 PCI bridge\: Intel Corporation Device 19d1 \(rev 11\) 00\:18\.0 Communication controller\: Intel Corporation Device 19d3 \(rev 11\) 00\:1a\.0 Serial controller\: Intel Corporation Device 19d8 \(rev 11\) 00\:1a\.1 Serial controller\: Intel Corporation Device 19d8 \(rev 11\) 00\:1a\.2 Serial controller\: Intel Corporation Device 19d8 \(rev 11\) 00\:1c\.0 SD Host controller\: Intel Corporation Device 19db \(rev 11\) 00\:1f\.0 ISA bridge\: Intel Corporation DNV LPC or eSPI \(rev 11\) 00\:1f\.2 Memory controller\: Intel Corporation Device 19de \(rev 11\) 00\:1f\.4 SMBus\: Intel Corporation DNV SMBus controller \(rev 11\) 00\:1f\.5 Serial bus controller \[0c80\]\: Intel Corporation DNV SPI Controller \(rev 11\) 01\:00\.0 Co\-processor\: Intel Corporation Atom Processor C3000 Series QuickAssist Technology \(rev 11\) 02\:00\.0 Ethernet controller\: Broadcom Limited Device b870 \(rev 01\) 03\:00\.0 Ethernet controller\: Intel Corporation I210 Gigabit Network Connection \(rev 03\) 06\:00\.0 Memory controller\: Xilinx Corporation Device 7021 07\:00\.0 Ethernet controller\: Intel Corporation Ethernet Connection X553 Backplane \(rev 11\) 07\:00\.1 Ethernet controller\: Intel Corporation Ethernet Connection X553 Backplane \(rev 11\)')

bmc_option_dict={'Yes':'Erase.*Yes','No':'Erase.*No','Clear':'When.*Clear', 'No More':'When.*Do'}

cpu_use_percent_re='%Cpu\(s\):\s+([0-9]+\.[0-9])\s+us,\s+([0-9]+\.[0-9])\s+sy,\s+([0-9]+\.[0-9])\s+ni,\s+([0-9]+\.[0-9])\s+id,\s+([0-9]+\.[0-9])\s+wa,\s+([0-9]+\.[0-9])\s+hi,\s+([0-9]+\.[0-9])\s+si,\s+([0-9]+\.[0-9])\s+st'
##############################POSSIBLE?#################################
bios_values={
    '1': 'KEY_1',
    '2': 'KEY_2',
    '3': 'KEY_3',
    '4': 'KEY_4',
    '5': 'KEY_5',
    '6': 'KEY_6',
    '7': 'KEY_7',
    '8': 'KEY_8',
    '9': 'KEY_9',
    '0': 'KEY_0',
    '.': 'KEY_DOT'
    }


re_static_ip_setup=[]
#re_static_ip_setup.append('\[Static\]')
re_static_ip_setup.append('Station IP address.*192\.168\.0\.(10)|(12)')
re_static_ip_setup.append('Subnet mask.*255\.255\.255\.0')

re_dhcp_ip_setup=[]#work
#re_dhcp_ip_setup.append('\[DynamicAddressBmcDhcp\]')
re_dhcp_ip_setup.append('Station IP address.*10\.208\.80\.1[0-9][0-9]')
re_dhcp_ip_setup.append('Subnet mask.*255\.255\.255\.0')

re_static_ip_os=[]
re_static_ip_os.append('IP Address.*:.*192\.168\.0\.10')
re_static_ip_os.append('Subnet Mask.*:.*255\.255\.255\.0')

re_dhcp_ip_os=[]
#re_dhcp_ip_os.append('IP Address.*:.*10\.208\.80\.113')
re_dhcp_ip_os.append('IP Address.*:.*10\.208\.80\.1[0-9][0-9]')
re_dhcp_ip_os.append('Subnet Mask.*:.*255\.255\.255\.0')

image_version_re={'1':'Version:.*Seastone2V2\.1\.1\.2','2':'Version:.*Seastone2V2\.2\.0\.0'}

importDict={'1':'BIOS_stress_scripts/AC_powerCycle_StressTest.sh',
'2':'BIOS_stress_scripts/cpuColdResetStressTest.sh',
'3':'BIOS_stress_scripts/cpuWarmResetStressTest.sh',
'4':'stress',
'5':'Seastone2V2.1.1.2.bin',
'6':'Seastone2V2.2.0.0.bin',
'7':'AMIPRD.efi',
'8':'afulnx_64',
'9':cel_diag_image
}

boot_time_enabled=-1
boot_time_disabled=-1

#seastone_home_path = "8080/SEASTONE/"

#pc_info = DeviceMgr.getServerInfo('PC')
#scp_ip = pc_info.managementIP
#cel_diag_image='dpkg-deb -xv cel_diag-seastone2v2.v1.1.0.deb diag'