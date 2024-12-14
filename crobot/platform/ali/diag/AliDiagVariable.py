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
from AliCommonVariable import *

devicename = os.environ.get("deviceName", "").lower()
logging.info("devicename:{}".format(devicename))

# How long to run stress test
diagos_tc066_cpu_test_time = 30*60  # 30 minutes
diagos_tc067_come_ddr_time = 60
diagos_tc067_come_ddr_size = 60
diagos_tc068_come_ssd_time = 100
openbmc_tc069_ddr_stress_time = 30
openbmc_tc069_ddr_stress_size = 50
diagos_tc073_optical_modules_stress_time = 1800  # 30 minutes
# End of How long to run stress test

# SwImage shared objects
BIOS = SwImage.getSwImage("BIOS")
BIOS_FRU_EEPROM_INTERNAL = SwImage.getSwImage("BIOS_FRU_EEPROM_INTERNAL")
BCM5387 = SwImage.getSwImage("BCM5387")
BASE_CPLD = SwImage.getSwImage("BASE_CPLD")
FPGA = SwImage.getSwImage("FPGA")
TH4_PCIE_FLASH = SwImage.getSwImage("TH4_PCIE_FLASH")
TH4 = SwImage.getSwImage("TH4")
FAN_CPLD = SwImage.getSwImage("FAN_CPLD")
SWITCH_CPLD = SwImage.getSwImage("SWITCH_CPLD")
COME_CPLD = SwImage.getSwImage("COME_CPLD")
BASE_CPLD_REFRESH = SwImage.getSwImage("BASE_CPLD_REFRESH")
FAN_CPLD_REFRESH = SwImage.getSwImage("FAN_CPLD_REFRESH")
CPU_CPLD_REFRESH = SwImage.getSwImage("CPU_CPLD_REFRESH")
SWITCH_CPLD_REFRESH = SwImage.getSwImage("SWITCH_CPLD_REFRESH")
FPGA_MULTBOOT = SwImage.getSwImage("FPGA_MULTBOOT")
BMC = SwImage.getSwImage("BMC")
DIAG = SwImage.getSwImage("DIAG")
# End of SwImage shared objects

openbmc_diag_bin_path = "/var/log/BMC_Diag/bin"
openbmc_diag_utility_path = "/var/log/BMC_Diag/utility"
openbmc_fan_fru_eeprom_path = openbmc_diag_utility_path + "/fan_fru_eeprom"
openbmc_come_fru_eeprom_path = openbmc_diag_utility_path + "/COMe_fru_eeprom"
openbmc_fcb_fru_eeprom_path = openbmc_diag_utility_path + "/FCB_fru_eeprom"
openbmc_linecard_fru_eeprom_path = openbmc_diag_utility_path + "/linecard_fru_eeprom"
openbmc_system_fru_eeprom_path = openbmc_diag_utility_path + "/system_fru_eeprom"
openbmc_bmc_fru_eeprom_path = openbmc_diag_utility_path + "/BMC_fru_eeprom"
openbmc_switch_fru_eeprom_path = openbmc_diag_utility_path + "/switch_fru_eeprom"
openbmc_diag_utility_stress_path = openbmc_diag_utility_path + "/stress"
base_cpld_refresh_new_image = BASE_CPLD_REFRESH.newImage
# base_cpld_refresh_old_image = BASE_CPLD_REFRESH.oldImage  # There is no old image for refresh version!
base_cpld_refresh_path = BASE_CPLD_REFRESH.hostImageDir
base_cpld_refresh_save_to = BASE_CPLD_REFRESH.localImageDir
fan_cpld_refresh_new_image = FAN_CPLD_REFRESH.newImage
fan_cpld_refresh_path = FAN_CPLD_REFRESH.hostImageDir
fan_cpld_refresh_save_to = FAN_CPLD_REFRESH.localImageDir
cpu_cpld_refresh_new_image = CPU_CPLD_REFRESH.newImage
cpu_cpld_refresh_old_image = CPU_CPLD_REFRESH.oldImage
cpu_cpld_refresh_path = CPU_CPLD_REFRESH.hostImageDir
cpu_cpld_refresh_save_to =CPU_CPLD_REFRESH.localImageDir
switch_cpld_refresh_new_image = SWITCH_CPLD_REFRESH.newImage
switch_cpld_refresh_old_image = SWITCH_CPLD_REFRESH.oldImage
switch_cpld_refresh_path = SWITCH_CPLD_REFRESH.hostImageDir
switch_cpld_refresh_save_to = SWITCH_CPLD_REFRESH.localImageDir
openbmc_th4_new_image = TH4.newImage
openbmc_th4_path = TH4.hostImageDir
openbmc_th4_save_to = TH4.localImageDir
fan_cpld_new_image = FAN_CPLD.newImage
fan_cpld_old_image = FAN_CPLD.oldImage
fan_cpld_path = FAN_CPLD.hostImageDir
fan_cpld_save_to = FAN_CPLD.localImageDir
switch_cpld_new_image = SWITCH_CPLD.newImage
switch_cpld_old_image = SWITCH_CPLD.oldImage
switch_cpld_new_version = SWITCH_CPLD.newVersion
switch_cpld_old_version = SWITCH_CPLD.oldVersion
switch_cpld_path = SWITCH_CPLD.hostImageDir
switch_cpld_save_to = SWITCH_CPLD.localImageDir
come_cpld_new_image = COME_CPLD.newImage
come_cpld_old_image = COME_CPLD.oldImage
come_cple_new_version = COME_CPLD.newVersion
come_cple_old_versoin = COME_CPLD.oldVersion
come_cpld_path = COME_CPLD.hostImageDir
come_cpld_save_to = COME_CPLD.localImageDir
fpga_multboot_new_image = FPGA_MULTBOOT.newImage
fpga_multboot_old_image = FPGA_MULTBOOT.oldImage
fpga_multboot_new_version = FPGA_MULTBOOT.newVersion
fpga_multboot_old_version = FPGA_MULTBOOT.oldVersion
fpga_multboot_path = FPGA_MULTBOOT.hostImageDir
fpga_multboot_save_to = FPGA_MULTBOOT.localImageDir
diagos_diag_utility_path = "/usr/local/migaloo/utility"
diagos_smbios_fru_eeprom_path = diagos_diag_utility_path + "/SMBIOS_fru_eeprom"
diagos_cpu_diag_path = "/usr/local/migaloo/CPU_Diag"
diagos_diag_utility_stress_path = diagos_diag_utility_path + "/stress"
diagos_image_bios_path = BIOS_FRU_EEPROM_INTERNAL.hostImageDir
diagos_bcm5387_path = BCM5387.hostImageDir
diagos_bcm5387_new_image = BCM5387.newImage
diagos_bcm5387_save_to = BCM5387.localImageDir
base_cpld_path = BASE_CPLD.hostImageDir
base_cpld_save_to = BASE_CPLD.localImageDir
base_cpld_new_image = BASE_CPLD.newImage
base_cpld_old_image = BASE_CPLD.oldImage
base_cpld_new_version = BASE_CPLD.newVersion
base_cple_old_versoin = BASE_CPLD.oldVersion
diagos_base_cpld_new_version = BASE_CPLD.newVersion
diagos_fpga_path = FPGA.hostImageDir
diagos_fpga_save_to = FPGA.localImageDir
diagos_fpga_new_image = FPGA.newImage
diagos_fpga_old_image = FPGA.oldImage
diagos_fpga_new_version = FPGA.newVersion
diagos_fpga_old_version = FPGA.oldVersion
diagos_sdk_path = "/usr/local/migaloo/SDK"
diagos_th4_pcie_new_image = TH4_PCIE_FLASH.newImage
diagos_th4_pcie_new_version = TH4_PCIE_FLASH.newVersion["PCIe FW loader version"]
diagos_th4_pcie_old_image = TH4_PCIE_FLASH.oldImage
diagos_th4_pcie_old_version = TH4_PCIE_FLASH.oldVersion["PCIe FW loader version"]
bios_path = BIOS.hostImageDir
bios_save_to = BIOS.localImageDir
bios_new_image = BIOS.newImage
bios_old_image = BIOS.oldImage
bios_new_version = BIOS.newVersion
bios_old_version = BIOS.oldVersion
bmc_path = BMC.hostImageDir
bmc_save_to = BMC.localImageDir
bmc_new_image = BMC.newImage
bmc_old_image = BMC.oldImage
bmc_new_version = BMC.newVersion
bmc_old_version = BMC.oldVersion
diag_path = DIAG.hostImageDir
diag_save_to = DIAG.localImageDir
diag_new_image = DIAG.newImage
diag_old_image = DIAG.oldImage
diag_new_version = DIAG.newVersion
diag_old_version = DIAG.oldVersion

# Commonly to the whole family
openbmc_show_diag_version_command = r"./cel-software-test -a"
diagos_show_diag_version_command = r"./cel-version-test -S"
diagos_show_fpga_version_command = diagos_show_diag_version_command
openbmc_show_temp_sensor_command = r"./cel-temperature-test -a"
openbmc_sol_test_command = r"./cel-sol-test -a"
openbmc_oob_test_command = r"./cel-OOB-test -a"
openbmc_bmc_mac_test_command = r"./cel-MAC-test -a"
openbmc_mem_test_command = r"./cel-memory-test -a"
openbmc_peci_test_command = r"./cel-peci-test -a"
# End of commonly to the whole family

temp_sensor_help_patterns = [
    r"(?m)^[ \\t]*-h",
    r"(?m)^[ \\t]*-a",
    r"(?m)^[ \\t]*-H",
]
temp_sensor_pattern = r"(?P<sensor>^\\w+-i2c-\\w+-(?:0x)?\\w+)"
temp_overall_test_pattern = r"(?mi)^[ \\t]*Temperature test[ \\.\\t]+\\[[ \\t]*(?:(?!FAIL).)*$"

sw_help_patterns = [
    r"(?m)^[ \\t]*-h",
    r"(?m)^[ \\t]*-a",
]
sw_a_patterns  = [
    r"^[ \\t]*Diag version:[ \\t]*(?P<diag>.*)",
    r"^[ \\t]*OS information:[ \\t]*(?P<os_info>.*)",
    r"^[ \\t]*COMe board CPLD information:[ \\t]*(?P<come>.*)",
    r"^[ \\t]*FCB CPLD version:[ \\t]*(?P<cpld>.*)",
]

pow_help_patterns = sw_help_patterns

efi_boot_order_pattern = r"BootOrder: (?:(?P<first>\\d+),?)?(?:(?P<second>\\d+),?)?(?:(?P<third>\\d+),?)?(?:(?P<fourth>\\d+),?)?(?:(?P<five>\\d+),?)?"
efi_boot_whereof_patterns = [
    r"Boot(?P<sonic>\\d+)[ \\*]+SONiC-OS",
    r"Boot(?P<onie>\\d+)\\* ]*ONIE",
]

cpu_test_help_patters = [
    r"(?mi)^[ \\t]*-a",
    r"(?mi)^[ \\t]*-v",
    r"(?mi)^[ \\t]*-h",
]
cpu_test_all_patterns = [
    r"\\[Config\\]CPU Model Name: (?P<cpu_model_name>.*)",
    r"(?mi)^[ \\t]*CPU test.*PASS",
]
cpu_test_version_pattern = r"(?mi)^[ \\t]*The (?:\\.\\/)cel-cpu-test version is : (?P<version>.*)"
lscpu_model_name_pattern = r"Model name:\\ +(?P<cpu_model_name>.*)"

sata_test_help_patterns = [
    r"(?mi)^[ \\t]*--all",
    r"(?mi)^[ \\t]*-i",
    r"(?mi)^[ \\t]*-v",
    r"(?mi)^[ \\t]*-h",
    r"(?mi)^[ \\t]*-l",
]
sata_test_version_pattern = r"(?mi)^[ \\t]*The (?:\\.\\/)cel-sata-test version is : (?P<version>.*)"

psu_help_patterns = [
    r"(?m)^[ \\t]+-h",
    r"(?m)^[ \\t]+-p",
    r"(?m)^[ \\t]+-s",
    r"(?m)^[ \\t]+-a",
]

option_h_and_a_patterns = [
    r"(?m)^[ \\t]+-h",
    r"(?m)^[ \\t]+-a",
]

cpld_help_patterns = [
    r"(?m)^[ \\t]*-r",
    r"(?m)^[ \\t]*-w",
    r"(?m)^[ \\t]*-D",
    r"(?m)^[ \\t]*-d",
    r"(?m)^[ \\t]*-A",
    r"(?m)^[ \\t]*-l",
    r"(?m)^[ \\t]*-V",
    r"(?m)^[ \\t]*-a",
    r"(?m)^[ \\t]*-v",
    r"(?m)^[ \\t]*-h",
]

pci_help_patterns = [
    r"(?m)^[ \\t]*-l",
    r"(?m)^[ \\t]*-a",
    r"(?m)^[ \\t]*-v",
    r"(?m)^[ \\t]*-h",
]

emmc_help_patterns = [
    r"(?m)^[ \\t]*-h",
    r"(?m)^[ \\t]*-i",
    r"(?m)^[ \\t]*-s",
    r"(?m)^[ \\t]*-a",
]

memory_help_patterns = [
    r"(?m)[ \\t]*-h",
    r"(?m)[ \\t]*-i",
    r"(?m)[ \\t]*-a",
]
memory_a_pattern = r"(?mi)^[ \\t]*get_mem_info[ \\.]*.*(?P<get_mem_info>PASS)"

openbmc_cpu_help_patterns = [
    r"(?m)^[ \\t]*-h",
    r"(?m)^[ \\t]*-i",
    r"(?m)^[ \\t]*-a",
]
openbmc_cpu_i_patterns = [
    r"(?m)^[ \\t]*get_cpu_info[ \\.]+.*(?P<cpu_info>PASS)",
    r"(?m)^[ \\t]*check_processor_number[ \\.]+.*(?P<proc_number>PASS)",
    r"(?m)^[ \\t]*check_cpu_model[ \\.]+.*(?P<cpu_model>PASS)",
]

openbmc_i2c_help_patterns = [
    r"(?m)^[ \\t]*-h",
    r"(?m)^[ \\t]*-s",
    r"(?m)^[ \\t]*-l",
    r"(?m)^[ \\t]*-a",
]

diagos_sata_help_patterns = [
    r"(?m)^[ \\t]*--all",
    r"(?m)^[ \\t]*-i",
    r"(?m)^[ \\t]*-v",
    r"(?m)^[ \\t]*-h",
    r"(?m)^[ \\t]*-l",
]
diagos_sata_info_patterns = [
    r"(?m)^[ \\t]*Model Family:[ \\t]*(?P<family>.*)",
    r"(?m)^[ \\t]*Device Model:[ \\t]*(?P<model>.*)",
    r"(?m)^[ \\t]*User Capacity:[ \\t]*(?P<capacity>.*) bytes",
]
diagos_sata_list_patterns = [
    r"(?m)^[ \\t]*Id.*(?P<id>\\d+)",
    r"(?m)^[ \\t]*Dev Path.*?(?P<path>\\/.*)",
    r"(?m)^[ \\t]*Device Model.*?(?P<model>\\w.*)",
]

diagos_10kg_help_patterns = [
    r"(?m)^[ \\t]*-a",
    r"(?m)^[ \\t]*-v",
    r"(?m)^[ \\t]*-h",
]

diagos_i2c_device_patterns = [
    r"(?m)^[ \\t]*-r",
    r"(?m)^[ \\t]*-A",
    r"(?m)^[ \\t]*-R",
    r"(?m)^[ \\t]*-C",
    r"(?m)^[ \\t]*-s",
    r"(?m)^[ \\t]*-l",
    r"(?m)^[ \\t]*--bus",
    r"(?m)^[ \\t]*--detect",
    r"(?m)^[ \\t]*-a",
    r"(?m)^[ \\t]*--dump",
    r"(?m)^[ \\t]*-S",
    r"(?m)^[ \\t]*-i",
    r"(?m)^[ \\t]*-v",
    r"(?m)^[ \\t]*-h",
]

diagos_usb_help_patterns = [
    r"(?m)^[ \\t]*-a",
    r"(?m)^[ \\t]*-i",
    r"(?m)^[ \\t]*-h",
]

diagos_int_usb_help_patterns = [
    r"(?m)^[ \\t]*-a",
    r"(?m)^[ \\t]*-v",
    r"(?m)^[ \\t]*-h",
]

diagos_version_help_patterns = [
    r"(?m)^[ \\t]*-S",
    r"(?m)^[ \\t]*-v",
    r"(?m)^[ \\t]*-h",
]
diagos_version_show_patterns = [
    r"(?mi)^[ \\t]*Diag Version[ \\t]+:[ \\t]*(?P<diag>.*)",
    r"(?mi)^[ \\t]*SONiC SW Version[ \\t]+:[ \\t]*(?P<sonic>.*)",
    r"(?mi)^[ \\t]*Onie Version[ \\t]+:[ \\t]*(?P<onie>.*)",
    r"(?mi)^[ \\t]*Kernel Version[ \\t]+:[ \\t]*(?P<kernel>.*)",
    r"(?mi)^[ \\t]*SDK Diag[ \\t]+:[ \\t]*(?P<sdk>.*)",
    r"(?mi)^[ \\t]*Switch Chip Version[ \\t]+:[ \\t]*(?P<switch>.*)",
    r"(?mi)^[ \\t]*BMC Master Version[ \\t]+:[ \\t]*(?P<bmc_master>.*)",
    r"(?mi)^[ \\t]*BMC Slave Version[ \\t]+:[ \\t]*(?P<bmc_slave>.*)",
    r"(?mi)^[ \\t]*BIOS Version[ \\t]+:[ \\t]*(?P<bios>.*)",
    r"(?mi)^[ \\t]*FPGA Version[ \\t]+:[ \\t]*(?P<fpga>.*)",
    r"(?mi)^[ \\t]*BaseBoard CPLD Version[ \\t]+:[ \\t]*(?P<baseboard_cpld>.*)",
    r"(?mi)^[ \\t]*COMe CPLD Version[ \\t]+:[ \\t]*(?P<come_cpld>.*)",
    r"(?mi)^[ \\t]*FAN CPLD Version[ \\t]+:[ \\t]*(?P<fan_cpld>.*)",
    r"(?mi)^[ \\t]*SW CPLD1 Version[ \\t]+:[ \\t]*(?P<cpld1>.*)",
    r"(?mi)^[ \\t]*SW CPLD2 Version[ \\t]+:[ \\t]*(?P<cpld2>.*)",
    r"(?mi)^[ \\t]*Top Line CPLD1 Version[ \\t]+:[ \\t]*(?P<top_line_cpld1>.*)",
    r"(?mi)^[ \\t]*Top Line CPLD2 Version[ \\t]+:[ \\t]*(?P<top_line_cpld2>.*)",
    r"(?mi)^[ \\t]*BOT Line CPLD1 Version[ \\t]+:[ \\t]*(?P<bottom_line_cpld1>.*)",
    r"(?mi)^[ \\t]*BOT Line CPLD2 Version[ \\t]+:[ \\t]*(?P<bottom_line_cpld2>.*)",
    r"(?mi)^[ \\t]*I210 FW Version[ \\t]+:[ \\t]*(?P<i210>.*)",
]

old_cpld_version_patterns = [
    r"(?mi)^[ \\t]*BaseBoard CPLD Version[ \\t]+:[ \\t]*(?P<baseboard_cpld>.*%s)" % BASE_CPLD.oldVersion,
    r"(?mi)^[ \\t]*COMe CPLD Version[ \\t]+:[ \\t]*(?P<come_cpld>.*%s)" % COME_CPLD.oldVersion,
    r"(?mi)^[ \\t]*FAN CPLD Version[ \\t]+:[ \\t]*(?P<fan_cpld>.*%s)" % FAN_CPLD.oldVersion,
    r"(?mi)^[ \\t]*SW CPLD1 Version[ \\t]+:[ \\t]*(?P<cpld1>.*%s)" % SWITCH_CPLD.oldVersion,
    r"(?mi)^[ \\t]*SW CPLD2 Version[ \\t]+:[ \\t]*(?P<cpld2>.*%s)" % SWITCH_CPLD.oldVersion,
    r"(?mi)^[ \\t]*Top Line CPLD1 Version[ \\t]+:[ \\t]*(?P<top_line_cpld1>.*%s)" % SWITCH_CPLD.oldVersion,
    r"(?mi)^[ \\t]*Top Line CPLD2 Version[ \\t]+:[ \\t]*(?P<top_line_cpld2>.*%s)" % SWITCH_CPLD.oldVersion,
    r"(?mi)^[ \\t]*BOT Line CPLD1 Version[ \\t]+:[ \\t]*(?P<bottom_line_cpld1>.*%s)" % SWITCH_CPLD.oldVersion,
    r"(?mi)^[ \\t]*BOT Line CPLD2 Version[ \\t]+:[ \\t]*(?P<bottom_line_cpld2>.*%s)" % SWITCH_CPLD.oldVersion
]

new_cpld_version_patterns = [
    r"(?mi)^[ \\t]*BaseBoard CPLD Version[ \\t]+:[ \\t]*(?P<baseboard_cpld>.*%s)" % BASE_CPLD.newVersion,
    r"(?mi)^[ \\t]*COMe CPLD Version[ \\t]+:[ \\t]*(?P<come_cpld>.*%s)" % COME_CPLD.newVersion,
    r"(?mi)^[ \\t]*FAN CPLD Version[ \\t]+:[ \\t]*(?P<fan_cpld>.*%s)" % FAN_CPLD.newVersion,
    r"(?mi)^[ \\t]*SW CPLD1 Version[ \\t]+:[ \\t]*(?P<cpld1>.*%s)" % SWITCH_CPLD.newVersion,
    r"(?mi)^[ \\t]*SW CPLD2 Version[ \\t]+:[ \\t]*(?P<cpld2>.*%s)" % SWITCH_CPLD.newVersion,
    r"(?mi)^[ \\t]*Top Line CPLD1 Version[ \\t]+:[ \\t]*(?P<top_line_cpld1>.*%s)" % SWITCH_CPLD.newVersion,
    r"(?mi)^[ \\t]*Top Line CPLD2 Version[ \\t]+:[ \\t]*(?P<top_line_cpld2>.*%s)" % SWITCH_CPLD.newVersion,
    r"(?mi)^[ \\t]*BOT Line CPLD1 Version[ \\t]+:[ \\t]*(?P<bottom_line_cpld1>.*%s)" % SWITCH_CPLD.newVersion,
    r"(?mi)^[ \\t]*BOT Line CPLD2 Version[ \\t]+:[ \\t]*(?P<bottom_line_cpld2>.*%s)" % SWITCH_CPLD.newVersion
]

diagos_rtc_help_patterns = [
    r"(?m)^[ \\t]*-r",
    r"(?m)^[ \\t]*-w",
    r"(?m)^[ \\t]*-D",
    r"(?m)^[ \\t]*-a",
    r"(?m)^[ \\t]*-v",
    r"(?m)^[ \\t]*-h",
]

diagos_oob_help_patterns = [
    r"(?m)^[ \\t]*-a",
    r"(?m)^[ \\t]*-v",
    r"(?m)^[ \\t]*-h",
]

diagos_mac_help_patterns = [
    r"(?m)^[ \\t]*-a",
    r"(?m)^[ \\t]*-v",
    r"(?m)^[ \\t]*-h",
]

diagos_mem_help_patterns = [
    r"(?m)^[ \\t]*-h",
    r"(?m)^[ \\t]*-l",
    r"(?m)^[ \\t]*-v",
    r"(?m)^[ \\t]*-K",
    r"(?m)^[ \\t]*-a",
]

diagos_eeprom_help_patterns = [
    r"(?m)^[ \\t]*-l",
    r"(?m)^[ \\t]*-r",
    r"(?m)^[ \\t]*-w",
    r"(?m)^[ \\t]*-d",
    r"(?m)^[ \\t]*--dump",
    r"(?m)^[ \\t]*-t",
    r"(?m)^[ \\t]*-C",
    r"(?m)^[ \\t]*-D",
    r"(?m)^[ \\t]*-A",
    r"(?m)^[ \\t]*-v",
    r"(?m)^[ \\t]*-h",
]

diagos_eeprom_tool_d_patterns = [
    # For restore to default value only
    r"(?m)^[ \\t]*chassis_type = (?P<cs_type>.*)",

    # dmidecode -t 3
    r"(?m)^[ \\t]*chassis_serial_number = (?P<cs_serial>.*)",
    r"(?m)^[ \\t]*chassis_manufacture = (?P<cs_mfg>.*)",
    r"(?m)^[ \\t]*chassis_version = (?P<cs_version>.*)",
    r"(?m)^[ \\t]*chassis_asset_tag = (?P<cs_asset_tag>.*)",

    # dmidecode -t 2
    r"(?m)^[ \\t]*board_manufacture = (?P<brd_mfg>.*)",
    r"(?m)^[ \\t]*board_product_name = (?P<brd_product_name>.*)",
    r"(?m)^[ \\t]*board_serial_number = (?P<brd_serial>.*)",
    r"(?m)^[ \\t]*board_revision = (?P<brd_revision>.*)",
    r"(?m)^[ \\t]*board_asset_tag = (?P<brd_asset_tag>.*)",

    # For restore to default value only
    r"(?m)^[ \\t]*board_location = (?P<brd_location>.*)",
    r"(?m)^[ \\t]*product_manufecture = (?P<pd_mfg>.*)",

    # dmidecode -t 1
    r"(?m)^[ \\t]*product_name = (?P<pd_name>.*)",
    r"(?m)^[ \\t]*product_version = (?P<pd_version>.*)",

    # For restore to default value only
    r"(?m)^[ \\t]*product_serial_number = (?P<pd_serial>.*)",
    r"(?m)^[ \\t]*product_system_UUID = (?P<pd_system_uuid>.*)",

    # dmidecode -t 1 (continue)
    r"(?m)^[ \\t]*product_SKU_number = (?P<pd_sku>.*)",
    r"(?m)^[ \\t]*product_family_name = (?P<pd_family>.*)",
]
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
diagos_dmidecode_t3_patterns = [
    r"(?m)^[ \\t]*Manufacturer: (?P<dmi_mfg>.*)",
    r"(?m)^[ \\t]*Version: (?P<dmi_version>.*)",
    r"(?m)^[ \\t]*Serial Number: (?P<dmi_serial>.*)",
    r"(?m)^[ \\t]*Asset Tag: (?P<dmi_asset_tag>.*)",
]

diagos_bios_fru_eeprom_internal_new_image = BIOS_FRU_EEPROM_INTERNAL.newImage
diagos_bios_fru_eeprom_internal_save_to = BIOS_FRU_EEPROM_INTERNAL.localImageDir

diagos_i2c_test_help_patterns = [
    r"(?m)^[ \\t]*-r",
    r"(?m)^[ \\t]*-A",
    r"(?m)^[ \\t]*-R",
    r"(?m)^[ \\t]*-C",
    r"(?m)^[ \\t]*-s",
    r"(?m)^[ \\t]*-l",
    r"(?m)^[ \\t]*--bus",
    r"(?m)^[ \\t]*--detect",
    r"(?m)^[ \\t]*-a",
    r"(?m)^[ \\t]*--dump",
    r"(?m)^[ \\t]*-S",
    r"(?m)^[ \\t]*-i",
    r"(?m)^[ \\t]*-v",
    r"(?m)^[ \\t]*-h",
]
openbmc_i2c_test_help_patterns = [
    r"(?m)^[ \\t]*-h",
    r"(?m)^[ \\t]*-s",
    r"(?m)^[ \\t]*-l",
    r"(?m)^[ \\t]*-a",
]

diagos_eeprom_test_patterns = [
    r"(?m)^[ \\t]*-l",
    r"(?m)^[ \\t]*-r",
    r"(?m)^[ \\t]*-w",
    r"(?m)^[ \\t]*-d",
    r"(?m)^[ \\t]*--dump",
    r"(?m)^[ \\t]*-t",
    r"(?m)^[ \\t]*-C",
    r"(?m)^[ \\t]*-D",
    r"(?m)^[ \\t]*-A",
    r"(?m)^[ \\t]*-v",
    r"(?m)^[ \\t]*-h",
]
eeprom_tlv_patterns = [
    r"(?m)^Product Name +\\w+ +\\d+ +(?P<product_name>.*)",
    r"(?m)^Part Number +\\w+ +\\d+ +(?P<part_number>.*)",
    r"(?m)^Serial Number +\\w+ +\\d+ +(?P<serial_number>.*)",
    r"(?m)^Base MAC Address +\\w+ +\\d+ +(?P<base_mac>.*)",
    r"(?m)^Manufacture Date +\\w+ +\\d+ +(?P<mfg_date>.*)",
    r"(?m)^Device Version +\\w+ +\\d+ +(?P<device_version>.*)",
    r"(?m)^Label Revision +\\w+ +\\d+ +(?P<label_device>.*)",
    r"(?m)^Platform Name +\\w+ +\\d+ +(?P<platform_name>.*)",
    r"(?m)^ONIE Version +\\w+ +\\d+ +(?P<onie_version>.*)",
    r"(?m)^MAC Addresses +\\w+ +\\d+ +(?P<mac_addr>.*)",
    r"(?m)^Manufacturer +\\w+ +\\d+ +(?P<mfg>.*)",
    r"(?m)^Manufacture Country +\\w+ +\\d+ +(?P<mfg_country>.*)",
    r"(?m)^Vendor Name +\\w+ +\\d+ +(?P<vendor_name>.*)",
    r"(?m)^Diag Version +\\w+ +\\d+ +(?P<diag_version>.*)",
    r"(?m)^Service Tag +\\w+ +\\d+ +(?P<service_tag>.*)",
    # r"(?m)^Vendor Extension +\\w+ +\\d+ +(?P<vendor_ext>.*)",  # No match for "0x00" and ""
    r"(?m)^CRC-32 +\\w+ +\\d+ +(?P<crc_32>.*)",
]
eeprom_tlv_dummy = {
    "product_name":"AS24-128D-CL",
    "part_number":"R3174-F9001-02",
    "serial_number":"CLMFCL020C180001",
    "base_mac":"0C:48:C6:87:03:1A",
    "mfg_date":"12/25/2020 16:54:03",
    "device_version":"6",
    "label_revision":"Migaloo",
    "platform_name":"x86_64-alibaba_as24-128d-cl-r0",
    "onie_version":"0.0.1",
    "mac_addr":"4",
    "mfg":"Celestica",
    "mfg_country":"CHN",
    "vendor_name":"Alibaba",
    "diag_version":"2.0.3",
    "service_tag":"AS24-128D",
    "vendor_ext":"0x00",
}

diagos_eeupdate64e_mac = {
    "base":"0C48C68702D2",
    "base_plus_2":"0C48C68702D4",
    "base_plus_3":"0C48C68702D5",
}

diagos_wedge_power_patterns = [
    r"[ \\t]*status:",
    r"[ \\t]*on:",
    r"[ \\t]*-f:",
    r"[ \\t]*off:",
    r"[ \\t]*reset:",
    r"[ \\t]*cycle:",
]

diagos_cpu_freq_help_patterns = [
    r"(?m)^[ \\t]*-h",
    r"(?m)^[ \\t]*-a",
]

openbmc_mdio_help_patterns = [
    r"(?m)^[ \\t]*-h",
    r"(?m)^[ \\t]*-a",
]
openbmc_mdio_write_unexpected_patterns = [
    r"(?i)Write failed",
]

# openbmc_tmp_help_patterns = [
#     r"(?m)^[ \\t]*-a",
#     r"(?m)^[ \\t]*-h",
# ]

diagos_port_help_patterns = [
    r"(?m)^[ \\t]*-d",
    r"(?m)^[ \\t]*-c",
    r"(?m)^[ \\t]*-s",
    r"(?m)^[ \\t]*-D",
    r"(?m)^[ \\t]*-t",
    r"(?m)^[ \\t]*-v",
    r"(?m)^[ \\t]*-h",
]

diagos_cpu_stress_unexpected_patterns = [
    r"- (?P<found_error>[^0]\\d*) errors",
    r", (?P<found_warning>[^0]\\d*) warnings",
    r"(?i)(?P<found_no_such_file_or_directory>No such file or directory)",
]

diagos_come_ddr_stress_patterns = openbmc_ddr_stress = [
    r"Stats: Found (?P<found_hw_incident>[^0]\\d*) hardware incidents",
    r"Stats: Completed.*?, with (?P<completed_hw_incident>[^0]\\d*) hardware incidents",
    r"Stats: Completed.*, (?P<error>[^0]\\d*) errors",
]

diagos_i2c_stress_unexpected_patterns = [
    r"(?i)(?P<found_write_failed>Error: Write failed)",
    r"(?i)(?P<found_no_such_file_or_directory>No such file or directory)",
    r"(?i)(?P<found_error>error)",
    r"(?i)(?P<found_fail>fail)",
]

diagos_sfputil_show_presence_unexpected_patterns = [
    r"(?i)\\w+(?P<found_ethernet_number>\\d+) +not present",
    r"(?i)(?P<found_not_present>not present)",
    r"(?i)(?P<found_not_detect>not detect)",
]

diagos_sfputil_show_eeprom_raw_unexpected_patterns = [
    r"(?i)\\w*?(?P<eth_number>\\d+): SFP EEPROM not detected",
    r"(?i)(?P<found_not_found>not present)",
    r"(?i)(?P<found_not_detect>not detect)",
]

diagos_fpga_help_patterns = [
    r"(?m)^[ \\t]*-r",
    r"(?m)^[ \\t]*-w",
    r"(?m)^[ \\t]*-D",
    r"(?m)^[ \\t]*-d",
    r"(?m)^[ \\t]*-A",
    r"(?m)^[ \\t]*-l",
    r"(?m)^[ \\t]*-V",
    r"(?m)^[ \\t]*-a",
    r"(?m)^[ \\t]*-v",
    r"(?m)^[ \\t]*-h",
]

diagos_lpc_help_patterns = [
    r"(?m)^[ \\t]*-h",
    r"(?m)^[ \\t]*-a",
]

openbmc_fru_info_patterns = [
    r"(?mi)[ \\t]*(?:Product Manufacturer|Board Mfg)[ \\t]+:[ \\t]*(?P<manufacturer>.*?)[ \\t]*$",
    r"(?mi)[ \\t]*(?:Product Name|Board Product)[ \\t]+:[ \\t]*(?P<product_name>.*?)[ \\t]*$",
    r"(?mi)[ \\t]*(?:Product Serial|Board Serial)[ \\t]+:[ \\t]*(?P<serial_number>.*?)[ \\t]*$",
    r"(?mi)[ \\t]*(?:Product Part Number|Board Part Number)[ \\t]+:[ \\t]*(?P<part_number>.*?)[ \\t]*$",
]

bios_upgrade_patterns = [
    r"Reading old flash chip contents... (?P<old_flash_read>done)",
    r"Erasing and writing flash chip... Erase/write (?P<erase_write>done)",
    r"Verifying flash... (?P<verify_flash>VERIFIED)",
]

diagos_nic_list_patterns = [
    r"[ \\t]*(?P<eth1_nic1>1)[ \\t]+\\d+[ \\t]+\\d+[ \\t]+\\d+[ \\t]+.*?[ \\t]+.*",
    r"[ \\t]*(?P<eth2_nic2>2)[ \\t]+\\d+[ \\t]+\\d+[ \\t]+\\d+[ \\t]+.*?[ \\t]+.*",
    r"[ \\t]*(?P<eth0_nic5>5)[ \\t]+\\d+[ \\t]+\\d+[ \\t]+\\d+[ \\t]+.*?[ \\t]+.*",
]

eeupdate64e_nic_update_unexpected_patterns = [
    r"(?i)Incorrect LAN MAC address length",
    r"(?i)Unable to create a valid LAN MAC address",
]

openbmc_mdio_test_patterns = [
    r"(?mi)^[ \\\\t]*management phy BCM54616 mdio Test[ \\\\t]+.*(?P<management_result>PASS)",
    r"(?mi)^[ \\\\t]*opemBMC phy BCM54616 mdio Test[ \\\\t]+.*(?P<opemBMC_result>PASS)",
]

if 'shamu' in devicename:
    diagos_cpu_diag_path = '/usr/local/CPU_Diag/bin'
    diagos_show_fpga_version_command = r"./cel-fpga-test -v"
    diagos_diag_utility_path = "/usr/local/CPU_Diag/utility"