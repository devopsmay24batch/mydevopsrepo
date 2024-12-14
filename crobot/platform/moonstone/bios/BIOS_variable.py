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
##### Variable file used for bmc.robot #####uefi_shell_command
import DeviceMgr
import os
from SwImage import SwImage
dev_info = DeviceMgr.getDevice()

from Const import BOOT_MODE_UBOOT, BOOT_MODE_DIAGOS, BOOT_MODE_ONIE,ONIE_RESCUE_MODE
dev_info = DeviceMgr.getDevice()
mgmt_ip = dev_info.managementIP

devicename = os.environ.get("deviceName", "")
bmc_mgmp_ip=DeviceMgr.getDevice(devicename).get('bmcManagementIp') 

MOONSTONE = SwImage.getSwImage("MOONSTONE_BIOS")
moonstone_images_path="/home/brixia/gitcap/Moonstone/automation/"

moonstone_bios_new_image=MOONSTONE.newImage
moonstone_bios_new_image_path = moonstone_images_path+moonstone_bios_new_image
moonstone_bios_new_img_version=MOONSTONE.newVersion['biosNewImagVersion']

moonstone_bios_old_image=MOONSTONE.oldImage
moonstone_bios_old_image_path = moonstone_images_path+moonstone_bios_old_image
moonstone_bios_old_img_version=MOONSTONE.oldVersion['biosOldImagVersion']


moonstone_bios_image_version = MOONSTONE.newVersion['bios_image_version']
onie_sysinfo_version = MOONSTONE.newVersion['onie_sysinfo_version']
bios_deb_image = MOONSTONE.newVersion['bios_deb_image']
clpd_image_version = MOONSTONE.newVersion['clpd_image_version']
amid_name=MOONSTONE.newVersion['amid_name']
amid_path=moonstone_images_path+amid_name

moonstone_bmc_ipmi_version = MOONSTONE.newVersion['ipmi_version']
moonstone_bmc_firmware_revision = MOONSTONE.newVersion['firmware_revision']
moonstone_bmc_device_revision = MOONSTONE.newVersion['device_revision']

#moonstone_bmc_image = MOONSTONE.newVersion['bmc_image']
AfuEfix64_file=MOONSTONE.newVersion['Afuefix64_file']
#afulnx_64_image = MOONSTONE.newVersion['afulnx_64_image']

stress_file=MOONSTONE.newVersion['stress_file']
stress_file_path = moonstone_images_path+stress_file

fastboot_image=MOONSTONE.newVersion['fastboot_image']
fastboot_path=moonstone_images_path+fastboot_image
memtest_file = MOONSTONE.newVersion['memtest_image']
memtest_file_path= moonstone_images_path+memtest_file

AfuEfix64_file_path = moonstone_images_path+AfuEfix64_file
pc_info = DeviceMgr.getServerInfo('PC')
scp_ip = pc_info.managementIP
scp_username = pc_info.scpUsername
scp_password = pc_info.scpPassword
dhcp_username = pc_info.username
dhcp_password = pc_info.password
dhcp_prompt = pc_info.prompt

microcode_revision_code = 'revision=(\S+)'

#main_menu_pattern_check_1="American Megatrends"+"||"+moonstone_bios_new_image[:-4]+"||"


bios_setup_memory_speed='2400'
main_menu_test_data_1= 'American Megatrends||32768 MB||English||'+moonstone_bios_image_version[:-4]+'||5.17'

reset_cause_reboot='(0x11)'
reset_cause_power_chasis = '(0x77)'
reset_cause_power_reset='(0x22)'

memory_speed = 'Memory Speed = '

#memtest_file = MOONSTONE.newVersion['memtest_image']
 

memory_speed_general='2400'

password_keys={
    '1':'KEY_1',
    '2':'KEY_2',
    '3':'KEY_3',
    '4':'KEY_4'
}



pattern_ifconfig=["RX errors\s+(\S+)", "TX errors\s+(\S+)"]

uefi_shell_command="AfuEfix64.efi "+moonstone_bios_old_img_version+" /p /b /n /x /me /k"

management_port_command='00   07   00    00 ==> Network Controller - Ethernet controller'

pattern_dmidecode_memory= ["Total Width: 72 bits", "Data Width: 72 bits", "Size: 16384 MB", "Form Factor: SODIMM","Locator: DIMM_A1","Bank Locator: NODE 1","Type: DDR4","Speed: 2133 MT/s",  "Manufacturer: Samsung", "Asset Tag: DIMM_A1_AssetTag", " Minimum Voltage: 1.2 V", "Maximum Voltage: 1.2 V", "Configured Voltage: 1.2 V"]

pattern_pxe_server=["Checking Media Presence","Media Present","Start PXE over IPv4","Station IP address is (\S+\.\S+\.\S+\.\S+)", "Server IP address is (\S+\.\S+\.\S+\.\S+)", "NBP filename is bootx64\.efi","NBP filesize is 9022976 Bytes", "Downloading NBP file", "NBP file downloaded successfully"]
    

#pattern_bmc_information_setup=['BMC Device ID\s+(\S+)', 'BMC Device Revision\s+(\S+)','IPMI Version\s+(\S+)']

#pattern_bmc_information_os=['Device ID\s+:\s+(\S+)','Device Revision\s+:\s+(\S+)','Version\s+:\s+(\S+)']

pattern_check_bios_setup=["BIOS Vendor\s+(\S+\s\S+)","Project Version\s+(.*)\s+x64","Build Date and Time\s+(\S+\s\S+)"]

pattern_check_bios_post_log=['(American Megatrends)',"Ver:\s+(\S+)","BIOS Date:\s+(\S+\s\S+)"]

pattern_check_bios_dmidecode=["Vendor:\s+(\S+\s\S+)","Version:\s+(\S+)"]

pattern_date_and_time=["System Date\s+(\S+\s\S+)","System Time\s+(\S+)"]

pattern_management_port_pci=['02   00    00','03   00    00']

pattern_management_port_lspci=['07:00','10:00']

pattern_main_menu=["BIOS Vendor\s+(\S+\s\S+)","Project Version\s+(\S+)"]

main_menu_items=["BIOS Vendor\s+(\S+\s\S+)",'Total Memory\s+(\S+\s+\S+)',"Project Version\s+(.*)\s+x64","Core Version\s+(\S+)","System Date\s+(\S+\s\S+)","System Time\s+(\S+)"]

commands_in_s0_state_test=["fdisk -l", " ls -l", "i2cdetect -l"]

pattern_reset_cause='Reset cause(\S+):'

lanplus_ipmitool_cmd='ipmitool -I lanplus -H '+ mgmt_ip + ' -U root -P 0penBmc -C 17 {}'

sel_list_power_on_pattern = [r"working | Asserted"]

pattern_bmc_information_setup=["BMC Self Test Status.*PASSED",  
"BMC Device ID.*32",
"BMC Device Revision.*"+moonstone_bmc_device_revision,      
"BMC Firmware Revision.*"+moonstone_bmc_firmware_revision,
"IPMI Version.*"+moonstone_bmc_ipmi_version,   
"BMC Interface.*KCS" ]    
                              
pattern_bmc_information_os=["Device ID.*32",
"Device Revision.*"+moonstone_bmc_device_revision,
"Firmware Revision.*"+moonstone_bmc_firmware_revision,
"IPMI Version.*"+moonstone_bmc_ipmi_version,
"Manufacturer ID.*12290"]


pci_result=[ "00   00   00    00 ==> Bridge Device - Host/PCI bridge",
             "Vendor 8086 Device 6F00 Prog Interface 0",
    "00   00   01    00 ==> Bridge Device - PCI/PCI bridge",
             "Vendor 8086 Device 6F02 Prog Interface 0",
    "00   00   01    01 ==> Bridge Device - PCI/PCI bridge",
     "Vendor 8086 Device 6F03 Prog Interface 0",
    "00   00   02    00 ==> Bridge Device - PCI/PCI bridge",
             "Vendor 8086 Device 6F04 Prog Interface 0",
    "00   00   02    02 ==> Bridge Device - PCI/PCI bridge",
             "Vendor 8086 Device 6F06 Prog Interface 0",
    "00   00   02    03 ==> Bridge Device - PCI/PCI bridge",
             "Vendor 8086 Device 6F07 Prog Interface 0",
    "00   00   03    00 ==> Bridge Device - PCI/PCI bridge",
             "Vendor 8086 Device 6F08 Prog Interface 0",
    "00   00   03    01 ==> Bridge Device - PCI/PCI bridge",
             "Vendor 8086 Device 6F09 Prog Interface 0",
    "00   00   03    02 ==> Bridge Device - PCI/PCI bridge",
             "Vendor 8086 Device 6F0A Prog Interface 0",
    "00   00   03    03 ==> Bridge Device - PCI/PCI bridge",
             "Vendor 8086 Device 6F0B Prog Interface 0",
    "00   00   04    00 ==> Base System Peripherals - Other system peripheral",
             "Vendor 8086 Device 6F20 Prog Interface 0",
    "00   00   04    01 ==> Base System Peripherals - Other system peripheral",
             "Vendor 8086 Device 6F21 Prog Interface 0",
    "00   00   04    02 ==> Base System Peripherals - Other system peripheral",
             "Vendor 8086 Device 6F22 Prog Interface 0",
    "00   00   04    03 ==> Base System Peripherals - Other system peripheral",
             "Vendor 8086 Device 6F23 Prog Interface 0",
    "00   00   04    04 ==> Base System Peripherals - Other system peripheral",
             "Vendor 8086 Device 6F24 Prog Interface 0",
    "00   00   04    05 ==> Base System Peripherals - Other system peripheral",
             "Vendor 8086 Device 6F25 Prog Interface 0",
    "00   00   04    06 ==> Base System Peripherals - Other system peripheral",
             "Vendor 8086 Device 6F26 Prog Interface 0",
    "00   00   04    07 ==> Base System Peripherals - Other system peripheral",
             "Vendor 8086 Device 6F27 Prog Interface 0",
    "00   00   05    00 ==> Base System Peripherals - Other system peripheral",
             "Vendor 8086 Device 6F28 Prog Interface 0",
    "00   00   05    01 ==> Base System Peripherals - Other system peripheral",
             "Vendor 8086 Device 6F29 Prog Interface 0",
    "00   00   05    02 ==> Base System Peripherals - Other system peripheral",
             "Vendor 8086 Device 6F2A Prog Interface 0",
    "00   00   05    04 ==> Base System Peripherals - PIC",
             "Vendor 8086 Device 6F2C Prog Interface 20",
    "00   00   05    06 ==> Data Acquisition & Signal Processing Controllers - Performance Counters",
             "Vendor 8086 Device 6F39 Prog Interface 0",
    "00   00   06    00 ==> Base System Peripherals - Other system peripheral",
             "Vendor 8086 Device 6F10 Prog Interface 0",
    "00   00   06    01 ==> Base System Peripherals - Other system peripheral",
             "Vendor 8086 Device 6F11 Prog Interface 0",
    "00   00   06    02 ==> Base System Peripherals - Other system peripheral",
             "Vendor 8086 Device 6F12 Prog Interface 0",
    "00   00   06    03 ==> Base System Peripherals - Other system peripheral",
             "Vendor 8086 Device 6F13 Prog Interface 0",
    "00   00   06    04 ==> Base System Peripherals - Other system peripheral",
             "Vendor 8086 Device 6F14 Prog Interface 0",
    "00   00   06    05 ==> Base System Peripherals - Other system peripheral",
             "Vendor 8086 Device 6F15 Prog Interface 0",
    "00   00   06    06 ==> Base System Peripherals - Other system peripheral",
             "Vendor 8086 Device 6F16 Prog Interface 0",
    "00   00   06    07 ==> Base System Peripherals - Other system peripheral",
             "Vendor 8086 Device 6F17 Prog Interface 0",
    "00   00   07    00 ==> Base System Peripherals - Other system peripheral",
             "Vendor 8086 Device 6F18 Prog Interface 0",
    "00   00   07    01 ==> Base System Peripherals - Other system peripheral",
             "Vendor 8086 Device 6F19 Prog Interface 0",
    "00   00   07    02 ==> Base System Peripherals - Other system peripheral",
             "Vendor 8086 Device 6F1A Prog Interface 0",
    "00   00   07    03 ==> Base System Peripherals - Other system peripheral",
             "Vendor 8086 Device 6F1B Prog Interface 0",
    "00   00   07    04 ==> Base System Peripherals - Other system peripheral",
             "Vendor 8086 Device 6F1C Prog Interface 0",
    "00   00   14    00 ==> Serial Bus Controllers - USB",
             "Vendor 8086 Device 8C31 Prog Interface 30",
    "00   00   1C    00 ==> Bridge Device - PCI/PCI bridge",
             "Vendor 8086 Device 8C10 Prog Interface 0",
    "00   00   1C    01 ==> Bridge Device - PCI/PCI bridge",
             "Vendor 8086 Device 8C12 Prog Interface 0",
    "00   00   1C    02 ==> Bridge Device - PCI/PCI bridge",
             "Vendor 8086 Device 8C14 Prog Interface 0",
    "00   00   1C    03 ==> Bridge Device - PCI/PCI bridge",
             "Vendor 8086 Device 8C16 Prog Interface 0",
    "00   00   1C    04 ==> Bridge Device - PCI/PCI bridge",
             "Vendor 8086 Device 8C18 Prog Interface 0",
    "00   00   1C    05 ==> Bridge Device - PCI/PCI bridge",
             "Vendor 8086 Device 8C1A Prog Interface 0",
    "00   00   1C    06 ==> Bridge Device - PCI/PCI bridge",
             "Vendor 8086 Device 8C1C Prog Interface 0",
    "00   00   1C    07 ==> Bridge Device - PCI/PCI bridge",
             "Vendor 8086 Device 8C1E Prog Interface 0",
    "00   00   1D    00 ==> Serial Bus Controllers - USB",
             "Vendor 8086 Device 8C26 Prog Interface 20",
    "00   00   1F    00 ==> Bridge Device - PCI/ISA bridge",
             "Vendor 8086 Device 8C54 Prog Interface 0",
    "00   00   1F    02 ==> Mass Storage Controller - Serial ATA controller",
             "Vendor 8086 Device 8C02 Prog Interface 1",
    "00   00   1F    03 ==> Serial Bus Controllers - System Management Bus",
             "Vendor 8086 Device 8C22 Prog Interface 0",
    "00   04   00    00 ==> Network Controller - Ethernet controller",
             "Vendor 8086 Device 15AB Prog Interface 0",
    "00    01 ==> Network Controller - Ethernet controller",
    "8086 Device 15AB Prog Interface 0",
    "00   07   00    00 ==> Network Controller - Ethernet controller",
             "Vendor 14E4 Device F900 Prog Interface 0",
    "00   10   00    00 ==> Network Controller - Ethernet controller",
             "Vendor 8086 Device 1533 Prog Interface 0",
    "00   11   00    00 ==> Memory Controller - Other memory controller",
             "Vendor 10EE Device 7021 Prog Interface 0"]




moonstone_home_path = "8080/MOONSTONE/"

#bmc_file_path = 'BMC/'+moonstone_bmc_image

ic2_info_error_pattern_list = [r"I2C Test All.*|.*FAIL.*|", r"Error performing I2C Test All.", r"Status_Code = 0x01010100000002", r"Status = FAIL"]

#new_bios_image = moonstone_bios_new_image
#old_bios_image = moonstone_bios_old_image
cfuflash_path = "BMC/CFUFLASH"
afulnx_image = "afulnx_64"
afulnx_path = moonstone_images_path+afulnx_image


lscpi_pattern = ["00:00.0 Host bridge: Intel Corporation Xeon E7 v4/Xeon E5 v4/Xeon E3 v4/Xeon D DMI2",
"00:01.0 PCI bridge: Intel Corporation Xeon E7 v4/Xeon E5 v4/Xeon E3 v4/Xeon D PCI Express Root Port 1",
"00:01.1 PCI bridge: Intel Corporation Xeon E7 v4/Xeon E5 v4/Xeon E3 v4/Xeon D PCI Express Root Port 1",
"00:02.0 PCI bridge: Intel Corporation Xeon E7 v4/Xeon E5 v4/Xeon E3 v4/Xeon D PCI Express Root Port 2",
"00:02.2 PCI bridge: Intel Corporation Xeon E7 v4/Xeon E5 v4/Xeon E3 v4/Xeon D PCI Express Root Port 2",
"00:02.3 PCI bridge: Intel Corporation Xeon E7 v4/Xeon E5 v4/Xeon E3 v4/Xeon D PCI Express Root Port 2",
"00:03.0 PCI bridge: Intel Corporation Xeon E7 v4/Xeon E5 v4/Xeon E3 v4/Xeon D PCI Express Root Port 3",
"00:03.1 PCI bridge: Intel Corporation Xeon E7 v4/Xeon E5 v4/Xeon E3 v4/Xeon D PCI Express Root Port 3",
"00:03.2 PCI bridge: Intel Corporation Xeon E7 v4/Xeon E5 v4/Xeon E3 v4/Xeon D PCI Express Root Port 3",
"00:03.3 PCI bridge: Intel Corporation Xeon E7 v4/Xeon E5 v4/Xeon E3 v4/Xeon D PCI Express Root Port 3",
"00:04.0 System peripheral: Intel Corporation Xeon E7 v4/Xeon E5 v4/Xeon E3 v4/Xeon D Crystal Beach DMA Channel 0",
"00:04.1 System peripheral: Intel Corporation Xeon E7 v4/Xeon E5 v4/Xeon E3 v4/Xeon D Crystal Beach DMA Channel 1",
"00:04.2 System peripheral: Intel Corporation Xeon E7 v4/Xeon E5 v4/Xeon E3 v4/Xeon D Crystal Beach DMA Channel 2",
"00:04.3 System peripheral: Intel Corporation Xeon E7 v4/Xeon E5 v4/Xeon E3 v4/Xeon D Crystal Beach DMA Channel 3",
"00:04.4 System peripheral: Intel Corporation Xeon E7 v4/Xeon E5 v4/Xeon E3 v4/Xeon D Crystal Beach DMA Channel 4",
"00:04.5 System peripheral: Intel Corporation Xeon E7 v4/Xeon E5 v4/Xeon E3 v4/Xeon D Crystal Beach DMA Channel 5",
"00:04.6 System peripheral: Intel Corporation Xeon E7 v4/Xeon E5 v4/Xeon E3 v4/Xeon D Crystal Beach DMA Channel 6",
"00:04.7 System peripheral: Intel Corporation Xeon E7 v4/Xeon E5 v4/Xeon E3 v4/Xeon D Crystal Beach DMA Channel 7",
"00:05.0 System peripheral: Intel Corporation Xeon E7 v4/Xeon E5 v4/Xeon E3 v4/Xeon D Map/VTd_Misc/System Management",
"00:05.1 System peripheral: Intel Corporation Xeon E7 v4/Xeon E5 v4/Xeon E3 v4/Xeon D IIO Hot Plug",
"00:05.2 System peripheral: Intel Corporation Xeon E7 v4/Xeon E5 v4/Xeon E3 v4/Xeon D IIO RAS/Control Status/Global Errors",
"00:05.4 PIC: Intel Corporation Xeon E7 v4/Xeon E5 v4/Xeon E3 v4/Xeon D I/O APIC",
"00:05.6 Performance counters: Intel Corporation Xeon E7 v4/Xeon E5 v4/Xeon E3 v4/Xeon D IO Performance Monitoring",
"00:06.0 System peripheral: Intel Corporation Xeon E7 v4/Xeon E5 v4/Xeon E3 v4/Xeon D IIO Debug",
"00:06.1 System peripheral: Intel Corporation Xeon E7 v4/Xeon E5 v4/Xeon E3 v4/Xeon D IIO Debug",
"00:06.2 System peripheral: Intel Corporation Xeon E7 v4/Xeon E5 v4/Xeon E3 v4/Xeon D IIO Debug",
"00:06.3 System peripheral: Intel Corporation Xeon E7 v4/Xeon E5 v4/Xeon E3 v4/Xeon D IIO Debug",
"00:06.4 System peripheral: Intel Corporation Xeon E7 v4/Xeon E5 v4/Xeon E3 v4/Xeon D IIO Debug",
"00:06.5 System peripheral: Intel Corporation Xeon E7 v4/Xeon E5 v4/Xeon E3 v4/Xeon D IIO Debug",
"00:06.6 System peripheral: Intel Corporation Xeon E7 v4/Xeon E5 v4/Xeon E3 v4/Xeon D IIO Debug",
"00:06.7 System peripheral: Intel Corporation Xeon E7 v4/Xeon E5 v4/Xeon E3 v4/Xeon D IIO Debug",
"00:07.0 System peripheral: Intel Corporation Xeon E7 v4/Xeon E5 v4/Xeon E3 v4/Xeon D IIO Debug",
"00:07.1 System peripheral: Intel Corporation Xeon E7 v4/Xeon E5 v4/Xeon E3 v4/Xeon D IIO Debug",
"00:07.2 System peripheral: Intel Corporation Xeon E7 v4/Xeon E5 v4/Xeon E3 v4/Xeon D IIO Debug",
"00:07.3 System peripheral: Intel Corporation Xeon E7 v4/Xeon E5 v4/Xeon E3 v4/Xeon D IIO Debug",
"00:07.4 System peripheral: Intel Corporation Xeon E7 v4/Xeon E5 v4/Xeon E3 v4/Xeon D IIO Debug",
"00:14.0 USB controller: Intel Corporation 8 Series/C220 Series Chipset Family USB xHCI",
"00:1c.0 PCI bridge: Intel Corporation 8 Series/C220 Series Chipset Family PCI Express Root Port #1",
"00:1c.1 PCI bridge: Intel Corporation 8 Series/C220 Series Chipset Family PCI Express Root Port #2",
"00:1c.2 PCI bridge: Intel Corporation 8 Series/C220 Series Chipset Family PCI Express Root Port #3",
"00:1c.3 PCI bridge: Intel Corporation 8 Series/C220 Series Chipset Family PCI Express Root Port #4",
"00:1c.4 PCI bridge: Intel Corporation 8 Series/C220 Series Chipset Family PCI Express Root Port #5",
"00:1c.5 PCI bridge: Intel Corporation 8 Series/C220 Series Chipset Family PCI Express Root Port #6",
"00:1c.6 PCI bridge: Intel Corporation 8 Series/C220 Series Chipset Family PCI Express Root Port #7",
"00:1c.7 PCI bridge: Intel Corporation 8 Series/C220 Series Chipset Family PCI Express Root Port #8",
"00:1d.0 USB controller: Intel Corporation 8 Series/C220 Series Chipset Family USB EHCI #1",
"00:1f.0 ISA bridge: Intel Corporation C224 Series Chipset Family Server Standard SKU LPC Controller",
"00:1f.2 SATA controller: Intel Corporation 8 Series/C220 Series Chipset Family 6-port SATA Controller 1",
"00:1f.3 SMBus: Intel Corporation 8 Series/C220 Series Chipset Family SMBus Controller",
"04:00.0 Ethernet controller: Intel Corporation Ethernet Connection X552 10 GbE Backplane",
"04:00.1 Ethernet controller: Intel Corporation Ethernet Connection X552 10 GbE Backplane",
"07:00.0 Ethernet controller: Broadcom Limited Device f900",
"10:00.0 Ethernet controller: Intel Corporation I210 Gigabit Network Connection",
"11:00.0 Memory controller: Xilinx Corporation Device 7021",
"ff:0b.0 System peripheral: Intel Corporation Xeon E7 v4/Xeon E5 v4/Xeon E3 v4/Xeon D R3 QPI Link 0/1",
"ff:0b.1 Performance counters: Intel Corporation Xeon E7 v4/Xeon E5 v4/Xeon E3 v4/Xeon D R3 QPI Link 0/1",
"ff:0b.2 Performance counters: Intel Corporation Xeon E7 v4/Xeon E5 v4/Xeon E3 v4/Xeon D R3 QPI Link 0/1",
"ff:0b.3 System peripheral: Intel Corporation Xeon E7 v4/Xeon E5 v4/Xeon E3 v4/Xeon D R3 QPI Link Debug",
"ff:0c.0 System peripheral: Intel Corporation Xeon E7 v4/Xeon E5 v4/Xeon E3 v4/Xeon D Caching Agent",
"ff:0c.1 System peripheral: Intel Corporation Xeon E7 v4/Xeon E5 v4/Xeon E3 v4/Xeon D Caching Agent",
"ff:0c.2 System peripheral: Intel Corporation Xeon E7 v4/Xeon E5 v4/Xeon E3 v4/Xeon D Caching Agent",
"ff:0c.3 System peripheral: Intel Corporation Xeon E7 v4/Xeon E5 v4/Xeon E3 v4/Xeon D Caching Agent",
"ff:0f.0 System peripheral: Intel Corporation Xeon E7 v4/Xeon E5 v4/Xeon E3 v4/Xeon D Caching Agent",
"ff:0f.4 System peripheral: Intel Corporation Xeon E7 v4/Xeon E5 v4/Xeon E3 v4/Xeon D Caching Agent",
"ff:0f.5 System peripheral: Intel Corporation Xeon E7 v4/Xeon E5 v4/Xeon E3 v4/Xeon D Caching Agent",
"ff:0f.6 System peripheral: Intel Corporation Xeon E7 v4/Xeon E5 v4/Xeon E3 v4/Xeon D Caching Agent",
"ff:10.0 System peripheral: Intel Corporation Xeon E7 v4/Xeon E5 v4/Xeon E3 v4/Xeon D R2PCIe Agent",
"ff:10.1 Performance counters: Intel Corporation Xeon E7 v4/Xeon E5 v4/Xeon E3 v4/Xeon D R2PCIe Agent",
"ff:10.5 System peripheral: Intel Corporation Xeon E7 v4/Xeon E5 v4/Xeon E3 v4/Xeon D Ubox",
"ff:10.6 Performance counters: Intel Corporation Xeon E7 v4/Xeon E5 v4/Xeon E3 v4/Xeon D Ubox",
"ff:10.7 System peripheral: Intel Corporation Xeon E7 v4/Xeon E5 v4/Xeon E3 v4/Xeon D Ubox",
"ff:12.0 System peripheral: Intel Corporation Xeon E7 v4/Xeon E5 v4/Xeon E3 v4/Xeon D Home Agent 0",
"ff:12.1 Performance counters: Intel Corporation Xeon E7 v4/Xeon E5 v4/Xeon E3 v4/Xeon D Home Agent 0",
"ff:12.2 System peripheral: Intel Corporation Xeon E7 v4/Xeon E5 v4/Xeon E3 v4/Xeon D Home Agent 0 Debug",
"ff:13.0 System peripheral: Intel Corporation Xeon E7 v4/Xeon E5 v4/Xeon E3 v4/Xeon D Memory Controller 0 - Target Address/Thermal/RAS",
"ff:13.1 System peripheral: Intel Corporation Xeon E7 v4/Xeon E5 v4/Xeon E3 v4/Xeon D Memory Controller 0 - Target Address/Thermal/RAS",
"ff:13.2 System peripheral: Intel Corporation Xeon E7 v4/Xeon E5 v4/Xeon E3 v4/Xeon D Memory Controller 0 - Channel Target Address Decoder",
"ff:13.3 System peripheral: Intel Corporation Xeon E7 v4/Xeon E5 v4/Xeon E3 v4/Xeon D Memory Controller 0 - Channel Target Address Decoder",
"ff:13.4 System peripheral: Intel Corporation Xeon E7 v4/Xeon E5 v4/Xeon E3 v4/Xeon D Memory Controller 0 - Channel Target Address Decoder",
"ff:13.5 System peripheral: Intel Corporation Xeon E7 v4/Xeon E5 v4/Xeon E3 v4/Xeon D Memory Controller 0 - Channel Target Address Decoder",
"ff:13.6 System peripheral: Intel Corporation Xeon E7 v4/Xeon E5 v4/Xeon E3 v4/Xeon D DDRIO Channel 0/1 Broadcast",
"ff:13.7 System peripheral: Intel Corporation Xeon E7 v4/Xeon E5 v4/Xeon E3 v4/Xeon D DDRIO Global Broadcast",
"ff:14.0 System peripheral: Intel Corporation Xeon E7 v4/Xeon E5 v4/Xeon E3 v4/Xeon D Memory Controller 0 - Channel 0 Thermal Control",
"ff:14.1 System peripheral: Intel Corporation Xeon E7 v4/Xeon E5 v4/Xeon E3 v4/Xeon D Memory Controller 0 - Channel 1 Thermal Control",
"ff:14.2 System peripheral: Intel Corporation Xeon E7 v4/Xeon E5 v4/Xeon E3 v4/Xeon D Memory Controller 0 - Channel 0 Error",
"ff:14.3 System peripheral: Intel Corporation Xeon E7 v4/Xeon E5 v4/Xeon E3 v4/Xeon D Memory Controller 0 - Channel 1 Error",
"ff:14.4 System peripheral: Intel Corporation Xeon E7 v4/Xeon E5 v4/Xeon E3 v4/Xeon D DDRIO Channel 0/1 Interface",
"ff:14.5 System peripheral: Intel Corporation Xeon E7 v4/Xeon E5 v4/Xeon E3 v4/Xeon D DDRIO Channel 0/1 Interface",
"ff:14.6 System peripheral: Intel Corporation Xeon E7 v4/Xeon E5 v4/Xeon E3 v4/Xeon D DDRIO Channel 0/1 Interface",
"ff:14.7 System peripheral: Intel Corporation Xeon E7 v4/Xeon E5 v4/Xeon E3 v4/Xeon D DDRIO Channel 0/1 Interface",
"ff:15.0 System peripheral: Intel Corporation Xeon E7 v4/Xeon E5 v4/Xeon E3 v4/Xeon D Memory Controller 0 - Channel 2 Thermal Control",
"ff:15.1 System peripheral: Intel Corporation Xeon E7 v4/Xeon E5 v4/Xeon E3 v4/Xeon D Memory Controller 0 - Channel 3 Thermal Control",
"ff:15.2 System peripheral: Intel Corporation Xeon E7 v4/Xeon E5 v4/Xeon E3 v4/Xeon D Memory Controller 0 - Channel 2 Error",
"ff:15.3 System peripheral: Intel Corporation Xeon E7 v4/Xeon E5 v4/Xeon E3 v4/Xeon D Memory Controller 0 - Channel 3 Error",
"ff:1e.0 System peripheral: Intel Corporation Xeon E7 v4/Xeon E5 v4/Xeon E3 v4/Xeon D Power Control Unit",
"ff:1e.1 System peripheral: Intel Corporation Xeon E7 v4/Xeon E5 v4/Xeon E3 v4/Xeon D Power Control Unit",
"ff:1e.2 System peripheral: Intel Corporation Xeon E7 v4/Xeon E5 v4/Xeon E3 v4/Xeon D Power Control Unit",
"ff:1e.3 System peripheral: Intel Corporation Xeon E7 v4/Xeon E5 v4/Xeon E3 v4/Xeon D Power Control Unit",
"ff:1e.4 System peripheral: Intel Corporation Xeon E7 v4/Xeon E5 v4/Xeon E3 v4/Xeon D Power Control Unit",
"ff:1e.7 System peripheral: Intel Corporation Device 6f9f",
"ff:1f.0 System peripheral: Intel Corporation Xeon E7 v4/Xeon E5 v4/Xeon E3 v4/Xeon D Power Control Unit",
"ff:1f.2 System peripheral: Intel Corporation Xeon E7 v4/Xeon E5 v4/Xeon E3 v4/Xeon D Power Control Unit"]



smbios_list = [0,2,3,4,7,17]
smbios_bios_res = ["BIOS Information",
        "Vendor: American Megatrends Inc.",
        "Version: "+moonstone_bios_new_img_version,
        "Runtime Size: 64 kB",
        "ROM Size: 8192 kB",
        "BIOS Revision: 5.17"]
        
sbmios_baseboard_res = ["Base Board Information",
        "Manufacturer: Celestica",
        "Product Name: R4028-G0002-01",
        "Version: 01",
        "Serial Number: 00:a0:c9:00:00:00",
        "Asset Tag: R3240-G0013-01",
        "Chassis Handle: 0x0003",
        "Type: Motherboard"]

smbios_chassis_res = ["Chassis Information",
        "Manufacturer: Celestica",
        "Type: Other",
        "Lock: Present|Not Present",
        "Version: 01",
        "Serial Number: SN12345678",
        "Asset Tag: R4028-F0101-01",
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
        "Socket Designation: SOCKET 0",
        "Type: Central Processor",
        "Family: Xeon",
        "Manufacturer: Intel",
        "ID: 65 06 05 00 FF FB EB BF",
        "Signature: Type 0, Family 6, Model 86, Stepping 5",
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
        "Version: Intel.*Xeon.*CPU D-1627 @ 2.90GHz",
        "Voltage: 1.8 V",
        "External Clock: 100 MHz",
        "Max Speed: 4000 MHz",
        "Current Speed: 2900 MHz",
        "Status: Populated, Enabled",
        "Upgrade: Socket LGA2011-3",
        "L1 Cache Handle: 0x0052",
        "L2 Cache Handle: 0x0053",
        "L3 Cache Handle: 0x0054",
        "Serial Number: Not Specified",
        "Asset Tag: Not Specified",
        "Part Number: Not Specified",
        "Core Count: 4",
        "Core Enabled: 4",
        "Thread Count: 8"]


smbios_cache_res = ["Cache Information",
        "Socket Designation: ........CPU Internal L1",
        "Configuration: Enabled, Not Socketed, Level 1",
        "Operational Mode: Write Back",
        "Location: Internal",
        "Installed Size: 256 kB",
        "Maximum Size: 256 kB",
        "Installed SRAM Type: Synchronous",
        "Speed: Unknown",
        "Error Correction Type: Parity",
        "System Type: Other",
        "Associativity: 8-way Set-associative",
        "Socket Designation: ........CPU Internal L2",
        "Configuration: Enabled, Not Socketed, Level 2",
        "Operational Mode: Write Back",
        "Location: Internal",
        "Installed Size: 1024 kB",
        "Maximum Size: 1024 kB",
        "Installed SRAM Type: Synchronous",
        "Speed: Unknown",
        "Error Correction Type: Single-bit ECC",
        "System Type: Unified",
        "Associativity: 8-way Set-associative",
        "Socket Designation: ........CPU Internal L3",
        "Configuration: Enabled, Not Socketed, Level 3",
        "Operational Mode: Write Back",
        "Location: Internal",
        "Installed Size: 6144 kB",
        "Maximum Size: 6144 kB",
        "Installed SRAM Type: Synchronous",
        "Speed: Unknown",
        "Error Correction Type: Single-bit ECC",
        "System Type: Unified",
        "Associativity: 12-way Set-associative"]


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
    cpu_proc.append('model name.*:.*Intel\(R\) Xeon\(R\) CPU D-1627 @ 2.90GHz')
    cpu_proc.append('stepping.*:.*[0-9]')
    cpu_proc.append('microcode.*:.*0x.*')
    cpu_proc.append('cpu cores.*:.*4')
    cpu_proc.append('fpu.*:.*yes')
    cpu_proc.append('fpu_exception.*:.*yes')
    cpu_proc.append('cpuid level.*:.*20')
    cpu_proc.append('wp.*:.*yes')

serial_port=[]
serial_port.append('Console Redirection.*\[.*\]')
serial_port.append('Console Redirection Settings')
serial_port.append('Legacy Console Redirection')
serial_port.append('Legacy Console Redirection Settings')

console_settings=[]
console_settings.append('Terminal Type.*\[ANSI\]')
console_settings.append('Bits per second.*\[115200|9600\]')
console_settings.append('Data.*\[8\]')
console_settings.append('Parity.*\[None\]')
console_settings.append('Stop Bits.*\[1\]')

legacy_settings=[]
legacy_settings.append('Redirection COM Port')
legacy_settings.append('Resolution.*\[80x24|5\]')
legacy_settings.append('Redirect After POST.*\[(Always Enable)|(BootLoader)\]')


mainmenu_RC=[]
mainmenu_RC.append("Processor Configuration ")
mainmenu_RC.append("Advanced Power Management Configuration")
mainmenu_RC.append("Common RefCode Configuration")
mainmenu_RC.append("QPI Configuration")
mainmenu_RC.append("Memory Configuration")
mainmenu_RC.append("IIO Configuration")
mainmenu_RC.append("PCH Configuration")
mainmenu_RC.append("Miscellaneous Configuration")
mainmenu_RC.append("Server ME Debug Configuration")
mainmenu_RC.append("Server ME Configuration")
mainmenu_RC.append("Runtime Error Logging")
  

processor_config=["Processor Socket.*Socket 0",
"Processor ID.*00050665",
"Processor Frequency.*2.900GHz",             
"Processor Max Ratio.*1DH",                   
"Processor Min Ratio.*08H",                     
"Microcode Revision.*0E000014",              
"L1 Cache RAM.*256KB",               
"L2 Cache RAM.*1024KB",              
"L3 Cache RAM.*6144KB",              
"Processor 0 Version.*Intel\(R\) Xeon\(R\) CPU D",
"1627 @ 2.90GHz"]


power_management_config=["UFS", "CPU PM Tuning", "EIST \(P-states\)", "Config TDP", "IOTG Setting", "Uncore CLR Freq OVRD", "CPU P State Control", 
"CPU HWPM State Control", "CPU C State Control", "CPU T State Control", "CPU Thermal Management", "CPU Advanced PM Turning", "DRAM RAPL Configuration" ]

common_refcode_config=["MMCFG Base.*2G", "MMIOHBase.*56T", "MMIO High Size.*256G", "Isoc Mode", "MeSeg Mode", "Numa"]

qpi_general_config=["Degrade Precedence.*Topology Precedence", "Link Speed Mode.*Fast", "Link Frequency Select.*Auto", 
"Link L0p Enable.*Enable", "Link L1 Enable.*Enable", "MMIO P2P Disable.*no", "E2E Parity Enable.*Disable", "COD Enable.*Auto", 
"Early Snoop.*Auto", "Home Dir Snoop with.*Auto", "IVT- Style OSB Enable", "QPI Debug Print Level.*All"]

integrated_memory_controller=["Enforce POR.*Auto", "PPR Type.*[PPR Disabled]", "PPR Error Injection.*[Disabled]",
  "Memory Frequency.*[Auto]", "MRC Promote Warnings.*[Enabled]", "Promote Warnings.*[Enable]",
  "Halt on mem Training.*[Enabled]", "Multi-Threaded MRC.*[Auto]", "ECC Support.*[Auto]", "Enforce Timeout.*[Auto]"]

iio_configuration=["", "", "", "", "", "", "",  "", ""]
iio_configuration=["PCIe Train by BIOS.*[yes]", "PCIe Hot Plug.*[Disable]", "PCIe ACPI Hot Plug.*[Disable]", "EV DFX Features.*[Disable]", "IIO0 Configuration", "IOAT Configuration", "IIO General Configuration",  "Intel VT for Directed I/O", "IIO South Complex Configuration"]


                 
me_config=[]
me_config.append("Operational Firmware.*06:3.0.3.214")
me_config.append("ME Firmware Type.*SPS")
me_config.append("Recovery Firmware.*06:3.0.3.214")
me_config.append("ME Firmware Features.*SiEn\+NM\+PECIProxy\+ICC")
me_config.append("ME Firmware Status #1.*0x000F0345")
me_config.append("ME Firmware Status #2.*0x3800.*00")
me_config.append("Current State.*Operational")
me_config.append("Error Code.*No Error")
me_config.append("Altitude.*80000000")




sata_config_south_bridge=[]
sata_config_south_bridge.append("Enable controller")
sata_config_south_bridge.append("Speed limit")

setup_cpu_info=[]
setup_cpu_info.append('Processor ID\s+00050665')
setup_cpu_info.append('Processor Frequency\s+2.900GHz')
#setup_cpu_info.append('CPU BCLK Frequency\s+100MHz')
setup_cpu_info.append('L1 Cache RAM\s+256KB')
setup_cpu_info.append('L2 Cache RAM\s+1024KB')
setup_cpu_info.append('Processor 0 Version\s+Intel\(R\)\s+Xeon\(R\)\s+CPU')    
sel_entry_count_setup=-1
log_entry_count_os=-1
updated_sel_entry_count=-1

#boot_menu_content=''

re_boot_menu_content=[]
re_boot_menu_content.append('Setup Prompt Timeout(.*)')
re_boot_menu_content.append('Bootup NumLock State(.*)')
re_boot_menu_content.append('Quiet Boot(.*)')
re_boot_menu_content.append('Boot Option Priorities(.*)')
re_boot_menu_content.append('Boot Option #[0-9](.*)')
re_boot_menu_content.append('New Boot Option(.*)')
re_boot_menu_content.append('Hard Drive BBS Priorities(.*)')



#boot1_name=''
shell_scroll_count=-1
lap1_bmc_log_count=-1
lap2_bmc_log_count=-1

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
post_re.append('Version.*2\.20\.1276.*Copyright.*\(C\).*2023.*American.*Megatrends,.*Inc\.')
#Version 2.20.1276. Copyright (C) 2023 American Megatrends, Inc.
#line2='BIOS.*Date:.*Ver:.*'+bios_version_re
#post_re.append(line2)
#post_re.append('.*Ver:.*')

sata_write_re=[]
sata_write_re.append('[0-9]\+[0-9]\s+records in')
sata_write_re.append('[0-9]\+[0-9]\s+records out')
sata_write_re.append('[0-9]+ bytes copied,.*')

boot_option_dict={'ONL':'ONL OS', 'ONIE':'ONIE OS', 'USB':'USB.*Partition','AMI Virtual CDROM0':'', 'P4 M2':'\(S80\).*3IE7', 'Shell':'UEFI: Built-in EFI','Disabled':'Disabled'}
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

temp_mgmt_ip1 = "10.208.84.90"
temp_mgmt_ip2 = "10.208.84.91"
re_static_ip_setup=[]
re_static_ip_setup.append('StaticAddress')
re_static_ip_setup.append('Station IP Address.*' + temp_mgmt_ip1 + '|' + temp_mgmt_ip2)
re_static_ip_setup.append('Subnet mask.*255.255.255.0')

re_dhcp_ip_setup=[]#work
re_dhcp_ip_setup.append('DynamicAddressBmcDhcp')
re_dhcp_ip_setup.append('Station IP Address.*'+bmc_mgmp_ip)
re_dhcp_ip_setup.append('Subnet mask.*255.255.255.0')

re_static_ip_os=[]
re_static_ip_os.append('IP Address Source.*Static Address')
re_static_ip_os.append('IP Address.*:.*' + temp_mgmt_ip1 + '|' + temp_mgmt_ip2)
re_static_ip_os.append('Subnet Mask.*:.*255.255.255.0')

re_dhcp_ip_os=[]
re_dhcp_ip_os.append('IP Address Source.*DHCP Address')
re_dhcp_ip_os.append('IP Address.*:.*'+bmc_mgmp_ip)
re_dhcp_ip_os.append('Subnet Mask.*:.*255.255.255.0')

image_version_re={'1':'Version:.*3.0.2','2':'Version:.*'+moonstone_bios_new_img_version}

importDict={'1':'BIOS_stress_scripts/AC_powerCycle_StressTest.sh',
'2':'BIOS_stress_scripts/cpuColdResetStressTest.sh',
'3':'BIOS_stress_scripts/cpuWarmResetStressTest.sh',
'4':'stress',
'5':'Seastone2V2.1.1.2.bin',
'6':'Seastone2V2.2.0.0.bin',
'7':'AMIPRD.efi'
}

boot_time_enabled=-1
boot_time_disabled=-1

bmc_version_info_list = [
    "Device ID.*32",
    "Device Revision.*" + moonstone_bmc_device_revision,
    "Firmware Revision.*" + moonstone_bmc_firmware_revision,
    "IPMI Version.*" + moonstone_bmc_ipmi_version,
    "Manufacturer ID.*12290",
]
dpkg_install_pattern = ["Being postinst processed!"]

ssd_read_write_stress_test_pattern = ["Log: 1 nodes, 8 cpus.", "Stats: Starting SAT, 28800M, 60 seconds", "Stats: Found 0 hardware incidents", "Status: PASS - please verify no corrected errors"]

os_serial_port_pattern=["ttyS0 at I/O 0x3f8.*is a 16550A","ttyS1 at I/O 0x2f8.*is a 16550A"]

save_and_exit_screen_pattern = ["Save Changes And Exit", "Discard Changes And Exit", "Save Changes And Reset", "Discard Changes And Reset", "Discard Changes", "Restore Defaults", "Save As User Defaults", "Restore User Defaults", "Boot Override" ]

advance_menu_check=["Redfish Host Interface Settings", "Serial Port Console Redirection", "PCI Subsystem Settings", "USB Configuration", "Network Stack Configuration", "CSM Configuration"]     

pattern_reset_cause='Reset cause(\S+):'
reset_cause_reboot='(0x11)'
reset_cause_power_chasis = '(0x77)'
reset_cause_power_reset='(0x77)'

lanplus_ipmitool_cmd='ipmitool -I lanplus -H '+ bmc_mgmp_ip + ' -U root -P 0penBmc -C 17 {}'
sel_list_pattern="SEL has no entries"
df_output_pattern = ["devtmpfs.*1024.*0.*1024.*0% /dev"]
'''
"/dev/sda6        3030800 1620800   1236332  57% /",
"/dev/sda5         999320  218160    712348  24% /mnt/onl/images",
"/dev/sda1         261868     252    261616   1% /boot/efi",
"/dev/sda3         122835   36253     77408  32% /mnt/onl/boot",
"/dev/sda4         122835    1556    112105   2% /mnt/onl/config",
"tmpfs            3283740     788   3282952   1% /run",
"tmpfs               5120       0      5120   0% /run/lock",
"tmpfs            6567460       0   6567460   0% /dev/shm"]
'''