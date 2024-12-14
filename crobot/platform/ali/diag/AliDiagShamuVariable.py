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

from AliDiagVariable import *

# How long to run stress test

# End of How long to run stress test

# SwImage shared objects
DIAG = SwImage.getSwImage("DIAG")
PCIE_FLASH_SHAMU = SwImage.getSwImage("PCIE_FLASH_SHAMU")
SDK = SwImage.getSwImage("SDK")
# End of SwImage shared objects

openbmc_tmp = '/tmp/'
openbmc_exe_path = '/var/log/BMC_Diag/bin'
diagos_cpu_diag_path = "/usr/local/CPU_Diag/bin"
diagos_sdk_path = "/usr/local/CPU_Diag/utility/Shamu_SDK"
diagos_auto_tool = "/usr/local/CPU_Diag/auto_test_tool"
diag_deb_path = DIAG.hostImageDir
diag_deb_new_package = DIAG.newImage
diag_deb_new_version = DIAG.newVersion
diag_deb_save_to = DIAG.localImageDir
diag_pcie_flash_path = PCIE_FLASH_SHAMU.hostImageDir
diag_pcie_flash_save_to = PCIE_FLASH_SHAMU.localImageDir
diag_pcie_flash_old_image = PCIE_FLASH_SHAMU.oldImage
diag_pcie_flash_new_image = PCIE_FLASH_SHAMU.newImage
diag_pcie_flash_old_version = PCIE_FLASH_SHAMU.oldVersion["PCIe FW loader version"]
diag_pcie_flash_new_version = PCIE_FLASH_SHAMU.newVersion["PCIe FW loader version"]
diag_sdk_path = SDK.hostImageDir
diag_sdk_save_to = SDK.localImageDir
diag_sdk_old_image = SDK.oldImage
diag_sdk_new_image = SDK.newImage
diag_sdk_old_version = SDK.oldVersion
diag_sdk_new_version = SDK.newVersion

# Commonly to the whole family
openbmc_show_diag_version_command = r"./cel-software-test -i"
diagos_show_diag_version_command = r"./cel-software-test -i"
diagos_show_fpga_version_command = r"./cel-fpga-test -v"
openbmc_show_temp_sensor_command = r"./cel-temperature-test -t"
temp_sensor_help_patterns = [
    r"(?m)^[ \\t]*-h",
    r"(?m)^[ \\t]*-t",
    r"(?m)^[ \\t]*-H",
]
openbmc_sol_test_command = r"./cel-sol-test -t"
option_h_and_a_patterns = [
    r"(?m)^[ \\t]+-h",
    r"(?m)^[ \\t]+-t",
]
openbmc_oob_test_command = r"./cel-OOB-test -t"
openbmc_bmc_mac_test_command = r"./cel-MAC-test -t"
openbmc_mem_test_command = r"./cel-memory-test -t"
memory_help_patterns = [
    r"(?m)[ \\t]*-h",
    r"(?m)[ \\t]*-i",
    r"(?m)[ \\t]*-t",
]
openbmc_peci_test_command = r"./cel-peci-test -t"
openbmc_mdio_help_patterns = [
    r"(?m)^[ \\t]*-h",
    r"(?m)^[ \\t]*-t",
]
openbmc_mdio_util_help_patterns = [
    r"(?m)[ \\t]*-p: phy",
    r"(?m)^[ \\t]*-s: switch",
]
diagos_diag_utility_path = r"/usr/local/CPU_Diag/utility"
diagos_smbios_fru_eeprom_path = diagos_diag_utility_path + "/SMBIOS_fru_eeprom"
diagos_diag_utility_stress_path = diagos_diag_utility_path + "/stress"
diagos_eeprom_tool_d_patterns = [
    # For restore to default value only
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
diagos_i2c_test_help_patterns = [
    r"(?m)^[ \\t]*-h",
    r"(?m)^[ \\t]*-s",
    r"(?m)^[ \\t]*-o",
    r"(?m)^[ \\t]*-c",
    r"(?m)^[ \\t]*-l",
    r"(?m)^[ \\t]*-t",
]
diagos_rtc_help_patterns = [
    r"(?m)^[ \\t]*-h",
    r"(?m)^[ \\t]*-i",
    r"(?m)^[ \\t]*-g",
    r"(?m)^[ \\t]*-s",
    r"(?m)^[ \\t]*-d",
]
cpld_help_patterns = [
    r"(?m)^[ \\t]*-h",
    r"(?m)^[ \\t]*-w",
    r"(?m)^[ \\t]*-r",
    r"(?m)^[ \\t]*-a",
    r"(?m)^[ \\t]*-d",
    r"(?m)^[ \\t]*-v",
    r"(?m)^[ \\t]*-t",
]
diagos_mem_help_patterns = [
    r"(?m)^[ \\t]*-h",
    r"(?m)^[ \\t]*-i",
    r"(?m)^[ \\t]*-s",
    r"(?m)^[ \\t]*-t",
]
diagos_fpga_help_patterns = [
    r"(?m)^[ \\t]*-h",
    r"(?m)^[ \\t]*-w",
    r"(?m)^[ \\t]*-r",
    r"(?m)^[ \\t]*-d",
    r"(?m)^[ \\t]*-v",
    r"(?m)^[ \\t]*-t",
]
# End of commonly to the whole family

diagos_cpu_tlv_eeprom_path = diagos_diag_utility_path + "/CPU_tlv_eeprom"
diagos_tlv_eeprom_tool_d_patterns = [
    r"(?m)^[ \\t]*0x21=(?P<addr_0x21>.*)$",
    r"(?m)^[ \\t]*0x22=(?P<addr_0x22>.*)$",
    r"(?m)^[ \\t]*0x23=(?P<addr_0x23>.*)$",
    r"(?m)^[ \\t]*0x24=(?P<addr_0x24>.*)$",
    r"(?m)^[ \\t]*0x25=(?P<addr_0x25>.*)$",
    r"(?m)^[ \\t]*0x26=(?P<addr_0x26>.*)$",
    r"(?m)^[ \\t]*0x27=(?P<addr_0x27>.*)$",
    r"(?m)^[ \\t]*0x28=(?P<addr_0x28>.*)$",
    r"(?m)^[ \\t]*0x29=(?P<addr_0x29>.*)$",
    r"(?m)^[ \\t]*0x2a=(?P<addr_0x2a>.*)$",
    r"(?m)^[ \\t]*0x2b=(?P<addr_0x2b>.*)$",
    r"(?m)^[ \\t]*0x2c=(?P<addr_0x2c>.*)$",
    r"(?m)^[ \\t]*0x2d=(?P<addr_0x2d>.*)$",
    r"(?m)^[ \\t]*0x2e=(?P<addr_0x2e>.*)$",
    r"(?m)^[ \\t]*0x2f=(?P<addr_0x2f>.*)$",
    # r"(?m)^[ \\t]*0xfd=(?P<addr_0xfd>.*)$",  # "0x01" != ""
]
diagos_tlv_sonic_syseeprom_patterns = [
    r"0x2F\ +\\d+\ +(?P<addr_0x2f>.*)$",
    r"0x21\ +\\d+\ +(?P<addr_0x21>.*)$",
    r"0x22\ +\\d+\ +(?P<addr_0x22>.*)$",
    r"0x23\ +\\d+\ +(?P<addr_0x23>.*)$",
    r"0x24\ +\\d+\ +(?P<addr_0x24>.*)$",
    r"0x25\ +\\d+\ +(?P<addr_0x25>.*)$",
    r"0x26\ +\\d+\ +(?P<addr_0x26>.*)$",
    r"0x27\ +\\d+\ +(?P<addr_0x27>.*)$",
    r"0x28\ +\\d+\ +(?P<addr_0x28>.*)$",
    r"0x2A\ +\\d+\ +(?P<addr_0x2a>.*)$",
    r"0x2B\ +\\d+\ +(?P<addr_0x2b>.*)$",
    r"0x2C\ +\\d+\ +(?P<addr_0x2c>.*)$",
    r"0x2D\ +\\d+\ +(?P<addr_0x2d>.*)$",
    r"0x2E\ +\\d+\ +(?P<addr_0x2e>.*)$",
    # r"0xFD\ +\\d+\ +(?P<addr_0xfd>.*)$",  # "0x01" != ""
    r"0x29\ +\\d+\ +(?P<addr_0x29>.*)$",
]
cpld_version_patterns = [
    r"(?i)Base board CPLD version:\ +(?P<base>0x[0-9a-fA-F]{2})",
    r"(?i)COMe board CPLD version:\ +(?P<come>0x[0-9a-fA-F]{2})",
    r"(?i)Switch CPLD-1 version:\ +(?P<switch_1>0x[0-9a-fA-F]{2})",
    r"(?i)Switch CPLD-2 version:\ +(?P<switch_2>0x[0-9a-fA-F]{2})",
]
cpld_test_all_patterns = [
    r"(?i)Switch CPLD-1 test.*(?P<switch_cpld1_result>PASS)",
    r"(?i)Switch CPLD-2 test.*(?P<switch_cpld2_result>PASS)",
    r"(?i)Base board CPLD test.*(?P<base_cpld_result>PASS)",
    r"(?i)COMe board CPLD test.*(?P<come_cpld_result>PASS)",
]
usb_storage_help_patterns = [
    r"(?m)^[ \\t]*-h",
    r"(?m)^[ \\t]*-t",
]
usb_storage_t_patterns = [
    r"(?mi)^[ \\t]*(?P<drive>\\/dev\\/\\w+) is USB disk",
    r"(?i)USB disk test.*(?P<result>PASS)",
]
pcie_help_patterns = [
    r"(?m)^[ \\t]*-h",
    r"(?m)^[ \\t]*-i",
    r"(?m)^[ \\t]*-t",
]
software_help_patterns = [
    r"(?m)^[ \\t]*-h",
    r"(?m)^[ \\t]*-i",
]
software_i_patterns = [
    r"Platform\\: (?P<platform_board_type>.*)",
    r".*Version\\: D0000.(?P<bios_version>.*)",
    r"onie_version=(?P<onie_version>.*)",
    r"SONiC Software Version\\: .*V(?P<sonic_software_version>.*\\d{8}\\.\\d*)",
    r"Distribution\\: (?P<dist_version>.*)",
    r"Diag version\\: (?P<diag_version>.*)",
]
sonic_show_version_patterns = [
    r"SONiC Software Version\\: .*V(?P<sonic_software_version>.*\\d{8}\\.\\d*)",
    r"Distribution\\: (?P<dist_version>.*)",
]
cpld_v_patterns = [
    r"(?i)Base board CPLD version:[ \\t]*(?P<baseboard_cpld>0x[0-9a-fA-F]{2})",
    r"(?i)COMe board CPLD version:[ \\t]*(?P<come_cpld>0x[0-9a-fA-F]{2})",
    r"(?i)Switch CPLD-1 version:[ \\t]*(?P<switch_cpld_1>0x[0-9a-fA-F]{2})",
    r"(?i)Switch CPLD-2 version:[ \\t]*(?P<switch_cpld_2>0x[0-9a-fA-F]{2})",
]
luxshare_power_config_help_patterns = [
    r"(?m)^[ \\t]*-h",
    r"(?m)^[ \\t]*-b",
    r"(?m)^[ \\t]*-n",
    r"(?m)^[ \\t]*-s",
    r"(?m)^[ \\t]*-p",
]

test40_pattern = [
    r'Port_1 module:   Present',  r'Port_2 module:   Present',
    r'Port_3 module:   Present',  r'Port_4 module:   Present',
    r'Port_5 module:   Present',  r'Port_6 module:   Present',
    r'Port_7 module:   Present',  r'Port_8 module:   Present',
    r'Port_9 module:   Present',  r'Port_10 module:   Present',
    r'Port_11 module:   Present',  r'Port_12 module:   Present',
    r'Port_13 module:   Present',  r'Port_14 module:   Present',
    r'Port_15 module:   Present',  r'Port_16 module:   Present',
    r'Port_17 module:   Present',  r'Port_18 module:   Present',
    r'Port_19 module:   Present',  r'Port_20 module:   Present',
    r'Port_21 module:   Present',  r'Port_22 module:   Present',
    r'Port_23 module:   Present',  r'Port_24 module:   Present',
    r'Port_25 module:   Present',  r'Port_26 module:   Present',
    r'Port_27 module:   Present',  r'Port_28 module:   Present',
    r'Port_29 module:   Present',  r'Port_30 module:   Present',
    r'Port_31 module:   Present',  r'Port_32 module:   Present',
    r'Port_33 module:   Present',  r'Port_34 module:   Present',
    r'Port_35 module:   Present',  r'Port_36 module:   Present',
    r'Port_37 module:   Present',  r'Port_38 module:   Present',
    r'Port_39 module:   Present',  r'Port_40 module:   Present',
]

port_present_pattern = [ r"Port_{} module:   Present".format(port) for port in range(1, 41)]
port_reset_enable_pattern = [ r"Port_{} module reset signal is enable".format(port) for port in range(1, 41)]
port_reset_disable_pattern = [ r"Port_{} module reset signal is disable".format(port) for port in range(1, 41)]
port_modsel_enable_pattern = [ r"Port_{} module MODSEL signal is enable".format(port) for port in range(1, 41)]
port_modsel_disable_pattern = [ r"Port_{} module MODSEL signal is disable".format(port) for port in range(1, 41)]
port_lpmod_enable_pattern = [ r"Port_{} module LPMOD signal is enable".format(port) for port in range(1, 41)]
port_lpmod_disable_pattern = [ r"Port_{} module LPMOD signal is disable".format(port) for port in range(1, 41)]
port_interrupt_high_pattern = [ r"Port_{} module interrupt signal is high".format(port) for port in range(1, 41)]
port_interrupt_low_pattern = [ r"Port_{} module interrupt signal is low".format(port) for port in range(1, 41)]
qsfp_not_scanned_pattern = [ r"QSFP_{} .*? NO".format(port) for port in range(1, 41)]
qsfp_scanned_pattern = [ r"QSFP_{} .*? OK".format(port) for port in range(1, 41)]
sfp_eeprom_detected = [ r"Ethernet{}: SFP EEPROM detected".format(port) for port in range(1, 41)]
optical_modules_test_fail_file = 'Optical_modules_Stress_Test_result_failed.txt'
