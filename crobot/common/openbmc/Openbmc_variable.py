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
import logging
import DeviceMgr
from SwImage import SwImage
from Sdk_variable import BCM_promptstr, SDK_PATH, SDK_SCRIPT, sdkConsole
devicename = os.environ.get("deviceName", "")
logging.info("devicename:{}".format(devicename))

PimType = 'PIM'
bmc_bin_path = '/mnt/data1/BMC_Diag/bin'
bmc_version_cmd = './cel-software-test -h'

pc_info = DeviceMgr.getServerInfo('PC')
scp_ip = pc_info.managementIP
scp_username = pc_info.scpUsername
scp_password = pc_info.scpPassword
dhcp_ipv6 = pc_info.managementIPV6
dhcp_username = pc_info.username
dhcp_password = pc_info.password
dhcp_prompt = pc_info.prompt


usb0_int_bmc = {
    'ip_ipv6' : 'fe80::ff:fe00:1',
    'interface' : 'usb0',
}
usb0_int_cpu = {
    'ip_ipv6' : 'fe80::ff:fe00:2',
    'interface' : 'usb0',
}

default_bmc_usb0_mac_addr = '02:00:00:00:00:01'
default_bmc_usb0_ipv6_addr = 'fe80::1'

power_option = '-s'
workspace = '/mnt/data1/'
error_messages_list = 'error,no driver bound,module lm75 not found,module pmbus not found,warning'
### FB_BMC_W400C_TC_006_RackmonTest ####
rackmon_service_messages_list = '/usr/local/bin/rackmond,runsv /etc/sv/rackmond,grep rack'

#### FB_BMC_COMM_TC_008 ####
bic_messages_list = [
    r'Bridge-IC\svers.*\s.*is\s(.+)',
    r'Bridge-IC\s?.*\sis\s?.*\sini\s?.*\s?tialized\s?.*\sSCL\s?.*\sto\s?.*\s1Mhz'
]
bic_auto_set_test_iteration = 3

#### FB_BMC_COMM_TC_014 ####
dhcp_messages_list = [
    r'Setting\svendor\sinformation\sin\s\/etc\/dhcp\/dhclient\.conf'
]

#### FB_BMC_COMM_TC_018, FB_BMC_COMM_TC_014 ####
usb0_test_file = 'test1M'
usb0_test_size_mb = 10

#### FB_BMC_COMM_TC_023 ####
MIN_RPM = 0
MAX_RPM = 15000

#### FB_BMC_COMM_TC_021 ####
test_path_tc_021 = '/etc'

#### FB_BMC_COMM_TC_022, FB_BMC_COMM_TC_053 ####
sdk_path = SDK_PATH
python_tool = 'python3'
sdk_cmd_option = '-c all --run_case 1'
SDK_INIT_CMD = '%s %s %s'%(python_tool, SDK_SCRIPT, sdk_cmd_option)
SDK_PROMPT = sdkConsole
SDK_EXIT_CMD = 'exit()'
sdk_timeout = 600

#### FB_BMC_COMM_TC_032 ####
gpio_test_path = '/tmp/gpionames/BMC_CPLD_BOARD_REV_ID0'
board_rev_direction = 'in'
# board_rev_value = '1'

#### FB_BMC_COMM_TC_033 ####
WDT_test0 = {
    'WDT1': 0,
    'WDT2': 0,
}
WDT_test1 = {
    'WDT1': WDT_test0['WDT1']+1,
    'WDT2': WDT_test0['WDT2']
}
WDT_test2 = {
    'WDT1': WDT_test1['WDT1']+1,
    'WDT2': WDT_test1['WDT2']
}
WDT_test3 = {
    'WDT1': 0,
    'WDT2': 1
}
WDT_test4 = {
    'WDT1': WDT_test3['WDT1']+1,
    'WDT2': WDT_test3['WDT2']
}
WDT_test5 = {
    'WDT1': WDT_test4['WDT1']+1,
    'WDT2': WDT_test4['WDT2']
}
WDT_test6 = {
    'WDT1': 0,
    'WDT2': 1
}

#### FB_BMC_COMM_TC_038 ####
psu1_eeprom_dict_tc_038 = {
    'FRU Information'      : 'PSU1 (Bus:24 Addr:0x50)'
}
psu2_eeprom_dict_tc_038 = {
    'FRU Information'      : 'PSU2 (Bus:25 Addr:0x50)'
}

#### FB_BMC_COMM_TC_034, FB_BMC_COMM_TC_047 ####
all_eeprom_path = '/mnt/data1/BMC_Diag/utility/eeprom'
scm_cpld_bus = '2'
scm_cpld_addr = '0x3e'
system_misc_4_reg = '0x38'
write_enable_scm = '0'
scm_eeprom_path = all_eeprom_path
scm_eeprom_test = 'SCM_EEPROM_TEST'
scm_eeprom_test2 = 'SCM_EEPROM_TEST2'
scm_eeprom_product_name = 'SCM_EEPROM_DEFAULT'

#### FB_BMC_COMM_TC_035, FB_BMC_COMM_TC_045, FB_BMC_COMM_TC_019 ####
smb_cpld_bus = '12'
smb_cpld_addr = '0x3e'
cpld_spi_hold_wp_reg = '0x46'
enable_wp = '0xfd'
disable_wp = '0xff'

#### FB_BMC_COMM_TC_019 ####
cmd_read_mac_from_eeprom = './eeprom_tool -d -e SMB'
mac_eeprom_path = all_eeprom_path
mac_eeprom_type = 'SMB'

smb_eeprom_path = all_eeprom_path
smb_eeprom_test = 'SMB_EEPROM_TEST_AC'
smb_eeprom_test_dc = 'SMB_EEPROM_TEST_DC'

smb_eeprom_test2 = 'SMB_EEPROM_TEST_AC2'
smb_eeprom_test_dc2 = 'SMB_EEPROM_TEST_DC2'

smb_eeprom_product_name = 'SMB_EEPROM_DEFAULT_AC'
smb_eeprom_product_name_dc = 'SMB_EEPROM_DEFAULT_DC'
smb_eeprom_name_dc = 'SMB_EEPROM_DEFAULT_DC'


#### FB_BMC_COMM_TC_036, FB_BMC_COMM_TC_046 ####
fcm_eeprom_path = all_eeprom_path
fcm_eeprom_test = 'FCM_EEPROM_TEST'
fcm_eeprom_test2 = 'FCM_EEPROM_TEST2'
fcm_eeprom_product_name = 'FCM_EEPROM_DEFAULT'

#### FB_BMC_COMM_TC_037, FB_BMC_COMM_TC_046 ####
fan_eeprom_path = all_eeprom_path
fan_eeprom_test = 'FAN_EEPROM_TEST'
fan_eeprom_test2 = 'FAN_EEPROM_TEST2'
fan_eeprom_product_name = 'FAN_EEPROM_DEFAULT'

#### FB_BMC_W400C_TC_003 ####
pem_eeprom_path = '/mnt/data1/BMC_Diag/utility/PEM_eeprom'
pem_eeprom_test = 'PEM_EEPROM_TEST'
pem_eeprom_test2 = 'PEM_EEPROM_TEST2'
pem_eeprom_product_name = 'PEM_EEPROM_DEFAULT'
hotswap_eeprom_name = 'PEM2-HOTSWAP'
hotswap_eeprom_test = 'HOTSWAP_EEPROM_TEST'
hotswap_eeprom_test2 = 'HOTSWAP_EEPROM_TEST2'

#### FB_BMC_COMM_TC_039 ####
emmc_disk_name = 'mmcblk0'
emmc_size_keyword = r'(7|29).?\\d* (GB|GiB|MB)'
emmc_test_file = '/mnt/data1/test'
emmc_path = '/mnt/data1'

#### FB_BMC_COMM_TC_045, FB_BMC_COMM_TC_046, FB_BMC_COMM_TC_047 ####
UTIL_EEPROM_MAP_KEY = {
    'Version' : 'format_version',
    'Product Part Number' : 'top_level_product_part_number',
    'Local MAC' : 'local_mac_address',
    'Extended MAC Base': 'extended_mac_address_base',
    'Location on Fabric' : 'eeprom_location_on_fabric'
}

#### FB_BMC_COMM_TC_051 ####
presence_dict = {
    'scm'  : '1',
    'fan1' : '1',
    'fan2' : '1',
    'fan3' : '1',
    'fan4' : '1',
    'psu1' : '1',
    'psu2' : '1',
    'pem1' : '0',
    'pem2' : '0',
    'debug_card' : '0'
}

presence_dict_dc = {
    'scm'  : '1',
    'fan1' : '1',
    'fan2' : '1',
    'fan3' : '1',
    'fan4' : '1',
    'psu1' : '0',
    'psu2' : '1',
    'pem1' : '0',
    'pem2' : '0',
    'debug_card' : '0'
}

presence_dict_pem = {
    'scm'  : '1',
    'fan1' : '1',
    'fan2' : '1',
    'fan3' : '1',
    'fan4' : '1',
    'psu1' : '0',
    'psu2' : '0',
    'pem1' : '0',
    'pem2' : '1',
    'debug_card' : '0'
}

#### FB_BMC_COMM_TC_054 ####
PRI_FW_VER_KEY = 'PRI_FW_VER         (0xDD)'
SEC_FW_VER_KEY = 'SEC_FW_VER         (0xD7)'
psu1_eeprom_dict_tc_054 = {
    'FRU Information'      : 'PSU1 (Bus:24 Addr:0x50)',
    'Product Manufacturer' : 'DELTA',
    'Product Name'         : 'DDM1500BH12A3F',
    'Product Part Number'  : 'ECD55020006',
    'Product Version'      : '00',
    'Product Serial'       : 'ANY',
    'Product Asset Tag'    : 'N/A',
    'Product FRU ID'       : 'P3C300A00'
}
psu2_eeprom_dict_tc_054 = {
    'FRU Information'      : 'PSU2 (Bus:25 Addr:0x50)',
    'Product Manufacturer' : 'DELTA',
    'Product Name'         : 'DDM1500BH12A3F',
    'Product Part Number'  : 'ECD55020006',
    'Product Version'      : '00',
    'Product Serial'       : 'ANY',
    'Product Asset Tag'    : 'N/A',
    'Product FRU ID'       : 'P3C300A00'
}
psu1_info_dict_tc_054 = {
    'PSU Information'           : 'PSU1 (Bus:24 Addr:0x58)',
    'MFR_ID             (0x99)' : 'Delta',
    'MFR_MODEL          (0x9A)' : 'ECD55020006',
    'MFR_REVISION       (0x9B)' : '00',
    'MFR_DATE           (0x9D)' : 'ANY',
    'MFR_SERIAL         (0x9E)' : 'ANY',
    # 'PRI_FW_VER         (0xDD)' : '4.0',
    # 'SEC_FW_VER         (0xD7)' : '3.2',
    # 'STATUS_WORD        (0x79)' : '0x0',
    # 'STATUS_VOUT        (0x7A)' : '0x0',
    # 'STATUS_IOUT        (0x7B)' : '0x0',
    # 'STATUS_INPUT       (0x7C)' : '0x0',
    # 'STATUS_TEMP        (0x7D)' : '0x0',
    # 'STATUS_CML         (0x7E)' : '0x0',
    # 'STATUS_FAN         (0x81)' : '0x0',
    # 'STATUS_STBY_WORD   (0xD3)' : '0x0',
    # 'STATUS_VSTBY       (0xD4)' : '0x0',
    # 'STATUS_ISTBY       (0xD5)' : '0x0'
    # 'OPTN_TIME_TOTAL    (0xD8)' : '190D:21H:30M:34S',
    # 'OPTN_TIME_PRESENT  (0xD9)' : '0D:0H:41M:17S'
}
psu2_info_dict_tc_054 = {
    'PSU Information'           : 'PSU2 (Bus:25 Addr:0x58)',
    'MFR_ID             (0x99)' : 'Delta',
    'MFR_MODEL          (0x9A)' : 'ECD55020006',
    'MFR_REVISION       (0x9B)' : '00',
    'MFR_DATE           (0x9D)' : 'ANY',
    'MFR_SERIAL         (0x9E)' : 'ANY',
    # 'PRI_FW_VER         (0xDD)' : '4.0',
    # 'SEC_FW_VER         (0xD7)' : '3.2',
    # 'STATUS_WORD        (0x79)' : '0x2848',
    # 'STATUS_VOUT        (0x7A)' : '0x0',
    # 'STATUS_IOUT        (0x7B)' : '0x0',
    # 'STATUS_INPUT       (0x7C)' : '0x8',
    # 'STATUS_TEMP        (0x7D)' : '0x0',
    # 'STATUS_CML         (0x7E)' : '0x0',
    # 'STATUS_FAN         (0x81)' : '0x0',
    # 'STATUS_STBY_WORD   (0xD3)' : '0x840',
    # 'STATUS_VSTBY       (0xD4)' : '0x0',
    # 'STATUS_ISTBY       (0xD5)' : '0x0'
    # 'OPTN_TIME_TOTAL    (0xD8)' : '14D:7H:48M:3S',
    # 'OPTN_TIME_PRESENT  (0xD9)' : '0D:0H:0M:0S'
}
psu2_info_dict_tc_054_Delta_dc = {
    'PSU Information': 'PSU2 (Bus:25 Addr:0x58)',
    'MFR_ID             (0x99)': 'Delta',
    'MFR_MODEL          (0x9A)': 'ECD25010015',
    'MFR_REVISION       (0x9B)': 'P2.1',
    'MFR_DATE           (0x9D)': 'ANY',
    'MFR_SERIAL         (0x9E)': 'ANY',
}
psu2_info_dict_tc_054_Delta_dc_new = {
    'PSU Information': 'PSU2 (Bus:25 Addr:0x58)',
    'MFR_ID             (0x99)': 'Delta',
    'MFR_MODEL          (0x9A)': 'ECD25010015',
    'MFR_REVISION       (0x9B)': '02',
    'MFR_DATE           (0x9D)': 'ANY',
    'MFR_SERIAL         (0x9E)': 'ANY',
}
psu2_info_dict_tc_054_Liteon_dc = {
    'PSU Information': 'PSU2 (Bus:25 Addr:0x58)',
    'MFR_ID             (0x99)': 'Liteon',
    'MFR_MODEL          (0x9A)': 'DD-2152-2L',
    'MFR_REVISION       (0x9B)': 'X5',
    'MFR_DATE           (0x9D)': 'ANY',
    'MFR_SERIAL         (0x9E)': 'ANY',
}
psu2_eeprom_dict_tc_054_Delta_dc = {
    'FRU Information': 'PSU2 (Bus:25 Addr:0x50)',
    'System Manufacturer': 'DELTA',
    'Product Name': 'MINIPACK2-DC-PSU-48V',
    'Product Version': '0',
    'Product Serial Number': 'ANY',
    #'Product Asset Tag': 'xxxxxxxx',
}
psu2_eeprom_dict_tc_054_Delta_dc_rework = {
    'FRU Information': 'PSU2 (Bus:25 Addr:0x50)',
    'System Manufacturer': 'DELTA',
    'Product Name': 'DC-PSU-48V',
    'Product Version': '1',
    'Product Serial Number': 'ANY',
    #'Product Asset Tag': 'xxxxxxxx',
}
psu2_eeprom_dict_tc_054_Delta_dc_rework_new = {
    'FRU Information': 'PSU2 (Bus:25 Addr:0x50)',
    'System Manufacturer': 'DELTA',
    'Product Name': 'DC-PSU-48V',
    'Product Version': '2',
    'Product Serial Number': 'ANY',
    #'Product Asset Tag': 'xxxxxxxx',
}
psu2_eeprom_dict_tc_054_Liteon_dc = {
    'FRU Information': 'PSU2 (Bus:25 Addr:0x50)',
    'System Manufacturer': 'Liteon',
    'Product Name': 'MINIPACK2-DC-PSU-48V',
    'Product Version': '0',
    'Product Serial Number': 'ANY',
    #'Product Asset Tag': 'xxxxxxxx',
}
psu2_eeprom_dict_tc_054_Liteon_dc_rework = {
    'FRU Information': 'PSU2 (Bus:25 Addr:0x50)',
    'System Manufacturer': 'Liteon',
    'Product Name': 'DC-PSU-48V',
    'Product Version': '0',
    'Product Serial Number': 'ANY',
    #'Product Asset Tag': 'xxxxxxxx',
}

#### FB_BMC_COMM_TC_055 ####
tftp_server_path = '/var/lib/tftpboot'
tftp_file_test = 'sensors.txt'
TFTP_SERVER = 'PC'

scm_type = 'scm'
smb_type = 'smb'
psu_type = 'psu'
pem_type = 'pem'
all_type = 'all'
SENSOR_IGNORE_KEY_LIST = ['SYSTEM_AIRFLOW']
SENSOR_OK = 'ok'

################### ipmitool cmd ###################
##### FB_BMC_COMM_TC_060, FB_BMC_COMM_TC_061, FB_BMC_COMM_TC_062 #####
# wdt_countdown_val_0s = '0x00 0x00'
# wdt_countdown_val_02s = '0x02 0x00'
# wdt_countdown_val_1s = '0x0a 0x00'
# wdt_countdown_val_5s = '0x32 0x00'
# wdt_countdown_val_10s = '0x64 0x00'
# wdt_countdown_val_25s = '0xff 0x00'
# wdt_timer_use     = {
#     'BIOS FRB2'   : '0x01',
#     'BIOS/POST'   : '0x02',
#     'OS Load'     : '0x03',
#     'SMS/OS'      : '0x04',
#     'OEM'         : '0x05'
# }
# wdt_timer_use_dont_log     = {
#     'BIOS FRB2'   : '0x81',
#     'BIOS/POST'   : '0x82',
#     'OS Load'     : '0x83',
#     'SMS/OS'      : '0x84',
#     'OEM'         : '0x85'
# }
# wdt_timer_action  = {
#     'no action'   : '0x00',
#     'hard reset'  : '0x01',
#     'power down'  : '0x02',
#     'power cycle' : '0x03'
# }
# wdt_pre_timeout    = '0x00'
# wdt_timer_use_expr = '0x00'
# cmd_set_wdt              = 'ipmitool raw 0x06 0x24'
# cmd_get_wdt              = 'ipmitool raw 0x06 0x25'
# cmd_reset_wdt            = 'ipmitool raw 0x06 0x22'

#### FB_BMC_COMM_TC_041, FB_BMC_COMM_TC_056 ####
cmd_get_device_id        = 'ipmitool raw 0x06 0x01'
cmd_get_device_id_err1   = 'ipmitool raw 0x06 0x01 0x01'
rsp_device_id = {
    'Firmware Revision' : '',  ## will be updated to current version defined by SwImage.yaml or ImageInfo.yaml
    'Manufacturer ID'   : '40981',
    'Product ID'        : '12614 (0x3146)'
}
AUTO_BUILD_FW_VER = '1.3'

#### FB_BMC_COMM_TC_049_SPI_Utility_Test ####
str_1 = 'Usage:||spi_util.sh <op> spi1 <spi1 device> <file>||  <op>          : read, write, erase||  <spi1 device> : SYSTEM_EE, BIOS, BCM5389_EE, GB_PCIE_FLASH, DOM_FPGA_FLASH1, DOM_FPGA_FLASH2||                  (SYSTEM_EE not support for Wedge400-C)||Examples:||  spi_util.sh write spi1 DOM_FPGA_FLASH domfpga.bit'
str_2 = 'Usage:||spi_util.sh <op> spi1 <spi1 device> <file>||  <op>          : read, write, erase||  <spi1 device> : SYSTEM_EE, BIOS, BCM5389_EE, TH3_PCIE_FLASH, DOM_FPGA_FLASH1, DOM_FPGA_FLASH2||                  (SYSTEM_EE not support for Wedge400-C)||Examples:||  spi_util.sh write spi1 DOM_FPGA_FLASH domfpga.bit'

#### FB_BMC_COMM_TC_056, FB_BMC_COMM_TC_057 ####
cmd_cold_reset           = 'ipmitool raw 0x06 0x02'

#### FB_BMC_COMM_TC_058 ####
cmd_get_self_test_result = 'ipmitool raw 0x06 0x04'
rsp_self_test     = '55 00'
bmc_self_result_pass = 'BMC Self Test Status       PASSED'
# bmc_self_test_boundary_line = 'BMC Firmware Revision'

#### FB_BMC_COMM_TC_059 ####
cmd_get_device_guid      = 'ipmitool raw 0x06 0x08'
rsp_device_guid   = ['ff ff ff ff ff ff ff ff ff ff ff ff ff ff ff ff', '00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00']

#### FB_BMC_COMM_TC_064 ####
cmd_get_system_info      = 'ipmitool raw 0x06 0x59 0x00 0x01 0x00 0x00'
cmd_set_system_info      = 'ipmitool raw 0x06 0x58 0x01 0x00 0x00 0x08'

#### FB_BMC_COMM_TC_066 ####
cmd_get_lan_config_1     = 'ipmitool raw 0x0c 0x02 0x01 0x33 0x0 0x00'
cmd_get_lan_config_2     = 'ipmitool raw 0x0c 0x02 0x01 0x3b 0x0 0x00'
rsp_get_lan_1 = '11 02'
rsp_get_lan_2 = {
    'byte1'  : '11',
    'byte2'  : '00',
    'byte3'  : '02',
}
rsp_get_lan_2_fail = '00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00'

#### FB_BMC_COMM_TC_067 ####
cmd_get_sol_config_1     = 'ipmitool raw 0x0c 0x22 0x81 00 00 00'
cmd_get_sol_config_2     = 'ipmitool raw 0x0c 0x22 0x81 0x01 00 00'
cmd_get_sol_config_3     = 'ipmitool raw 0x0c 0x22 0x81 0x05 00 00'
cmd_get_sol_config_4     = 'ipmitool raw 0x0c 0x22 0x81 0x06 00 00'
rsp_get_sol_config_1 = '01 00'
rsp_get_sol_config_2 = '01 01'
rsp_get_sol_config_3 = '01 09'

#### FB_BMC_COMM_TC_070 ####
cmd_get_board_id         = 'ipmitool raw 0x30 0x37'
rsp_board_id = {
    "Board SKU ID"      : "00",
    "Board Revision ID" : "01",
    "MB Slot ID"        : "01",
    "Slot Config ID"    : "00"
}

#### FB_BMC_COMM_TC_071 ####
cmd_get_port80           = 'ipmitool raw 0x30 0x49 0x00'
cmd_get_port80_err1      = 'ipmitool raw 0x30 0x49 0x00 0x01'
cmd_get_port80_err2      = 'ipmitool raw 0x30 0x49'

#### FB_BMC_COMM_TC_072 ####
cmd_get_pcie_config      = 'ipmitool raw 0x30 0xf4'
rsp_get_pcie_config = '02'

#### FB_BMC_COMM_TC_073 ####
cmd_set_post_start       = 'ipmitool raw 0x30 0x73'

#### FB_BMC_COMM_TC_074 ####
cmd_set_post_end         = 'ipmitool raw 0x30 0x74'

#### FB_BMC_COMM_TC_075 ####
# cmd_set_ppin             = 'ipmitool raw 0x30 0x77 0x64 0x64 0x59 0xd7 0x57 0xB1 0x5B 0xD1'

#### FB_BMC_COMM_TC_068, FB_BMC_COMM_TC_069 ####
# cmd_get_bios_boot_order  = 'ipmitool raw 0x30 0x53'
# cmd_set_bios_boot_order  = 'ipmitool raw 0x30 0x52'
BOOT_ORDER_LIST = ['Network:UEFI: IPv4', 'Hard Disk:CentOS  (', 'USB', 'CD/DVD', 'Other', 'Disabled']
# BOOT_ORDER_IPV6 = 'Network:UEFI: IPv6'
# boot_override_keyword = 'CentOS'

# #### for supporting BIOS version XG1_3A09
# if "minipack2" in devicename.lower() or 'cloudripper' in devicename.lower():
#     BOOT_ORDER_LIST = ['Network:UEFI: IPv4', 'Hard Disk:Linux OS', 'USB', 'CD/DVD', 'Other', 'Disabled']
#     boot_override_keyword = 'Linux OS'

# bios_boot_order_default = {
#     "boot option 1"            : BOOT_ORDER_LIST[0], ### Network:UEFI: IPv4
#     "boot option 2"            : BOOT_ORDER_LIST[1], ### Hard Disk:CentOS  (
#     "boot option 3"            : BOOT_ORDER_LIST[2], ### USB
#     "boot option 4"            : BOOT_ORDER_LIST[3], ### CD/DVD
#     "boot option 5"            : BOOT_ORDER_LIST[4]  ### Other
# }
# bios_boot_order_test_2nd = {
#     "boot option 1"            : BOOT_ORDER_LIST[2], ### USB
#     "boot option 2"            : BOOT_ORDER_LIST[1], ### Hard Disk:CentOS  (
#     "boot option 3"            : BOOT_ORDER_LIST[0], ### Network:UEFI: IPv4
#     "boot option 4"            : BOOT_ORDER_LIST[3], ### CD/DVD
#     "boot option 5"            : BOOT_ORDER_LIST[4]  ### Other
# }
# bios_boot_order_test_3rd = {
#     "boot option 1"            : BOOT_ORDER_LIST[3], ### CD/DVD
#     "boot option 2"            : BOOT_ORDER_LIST[0], ### Network:UEFI: IPv4
#     "boot option 3"            : BOOT_ORDER_LIST[1], ### Hard Disk:CentOS  (
#     "boot option 4"            : BOOT_ORDER_LIST[2], ### USB
#     "boot option 5"            : BOOT_ORDER_LIST[4]  ### Other
# }
# bios_boot_order_test_4th = {
#     "boot option 1"            : BOOT_ORDER_LIST[4], ### Other
#     "boot option 2"            : BOOT_ORDER_LIST[0], ### Network:UEFI: IPv4
#     "boot option 3"            : BOOT_ORDER_LIST[1], ### Hard Disk:CentOS  (
#     "boot option 4"            : BOOT_ORDER_LIST[2], ### USB
#     "boot option 5"            : BOOT_ORDER_LIST[3]  ### CD/DVD
# }
# bios_boot_order_test_5th = {
#     "boot option 1"            : BOOT_ORDER_LIST[1], ### Hard Disk:CentOS  (
#     "boot option 2"            : BOOT_ORDER_LIST[0], ### Network:UEFI: IPv4
#     "boot option 3"            : BOOT_ORDER_LIST[2], ### USB
#     "boot option 4"            : BOOT_ORDER_LIST[3], ### CD/DVD
#     "boot option 5"            : BOOT_ORDER_LIST[4]  ### Other
# }
# bios_boot_order_test_6th = {
#     "boot option 1"            : BOOT_ORDER_IPV6,    ### Network:UEFI: IPv6
#     "boot option 2"            : BOOT_ORDER_LIST[1], ### Hard Disk:CentOS  (
#     "boot option 3"            : BOOT_ORDER_LIST[2], ### USB
#     "boot option 4"            : BOOT_ORDER_LIST[3], ### CD/DVD
#     "boot option 5"            : BOOT_ORDER_LIST[4]  ### Other
# }
# bios_boot_order_test_1st_list = ",".join(list(bios_boot_order_test_5th.values()))
# bios_boot_order_test_2nd_list = ",".join([BOOT_ORDER_LIST[2], BOOT_ORDER_LIST[0], BOOT_ORDER_LIST[1], BOOT_ORDER_LIST[3], BOOT_ORDER_LIST[4]])
# bios_boot_order_test_3rd_list = ",".join(list(bios_boot_order_test_3rd.values()))
# bios_boot_order_test_4th_list = ",".join(list(bios_boot_order_test_4th.values()))
# bios_boot_order_test_5th_list = ",".join(list(bios_boot_order_default.values()))
#######################################################

#### FB_BMC_COMM_TC_076 ####
cmd_get_DIMM_info        = 'ipmitool raw 0x36 0x13 0xAD 0x11 0x00'
cmd_set_DIMM_info        = 'ipmitool raw 0x36 0x12 0xAD 0x11 0x00'
cmd_dimm_dict = {
    "DIMM location"              : "0x01",
    "DIMM type"                  : "0x02",
    "DIMM speed"                 : "0x03",
    "DIMM module part number"    : "0x04",
    "DIMM module serial number"  : "0x05",
    "DIMM module manufacture ID" : "0x06"
}
rsp_DIMM_location_test = {
    "DIMM Present"   : "01",
    "node number"    : "00",
    "channel number" : "00",
    "DIMM number"    : "01"
}
rsp_DIMM_type_test = {
    "DIMM type" : 'c0'
}
rsp_DIMM_speed_test = {
    "DIMM speed" : '55 08',
    "DIMM size"  : '00 00 40 00'
}
rsp_DIMM_module_part_num_test = {
    "module part number" : '31 38 41 53 46 32 47 37 32 48 5a 2d 32 47 36 45 00 00 00 00'
}
rsp_DIMM_module_serial_num_test = {
    "module serial number" : '21 0c 00 00'
}
rsp_DIMM_module_manu_id_test = {
    "module manufacture ID" : '00 20'
}
cmd_DIMM_location_test   = '0x01 0x00 0x00 0x01'
cmd_DIMM_type_test       = '0x' + list(rsp_DIMM_type_test.values())[0]
cmd_DIMM_speed_test      = '0x55 0x08 0x00 0x00 0x40 0x00'
cmd_DIMM_module_part_num_test = ' '.join(['0x'+b for b in list(rsp_DIMM_module_part_num_test.values())[0].split()])
cmd_DIMM_module_serial_num_test = ' '.join(['0x'+b for b in list(rsp_DIMM_module_serial_num_test.values())[0].split()])
cmd_DIMM_module_manu_id_test = ' '.join(['0x'+b for b in list(rsp_DIMM_module_manu_id_test.values())[0].split()])

rsp_DIMM0_location = {
    "DIMM Present"   : "01",
    "node number"    : "00",
    "channel number" : "00",
    "DIMM number"    : "00"
}
rsp_DIMM1_location = {
    "DIMM Present"   : "01",
    "node number"    : "00",
    "channel number" : "01",
    "DIMM number"    : "00"
}
rsp_DIMM0_type = {
    "DIMM type" : 'c6'
}
rsp_DIMM0_speed = {
    "DIMM speed" : '55 08',
    "DIMM size"  : '00 40 00 00'
}
rsp_DIMM0_module_part_num = {
    "module part number" : '31 38 41 53 46 32 47 37 32 48 5a 2d 32 47 36 45 31 20 20 20'
}
rsp_DIMM0_module_part_num_rsp = {"module part number" : '48 4d 41 38 32 47 53 37 44 4a 52 38 4e 2d 56 4b 20 20 20 20'}
rsp_DIMM0_module_part_num_rsp_newCOMe = {"module part number" : '48 4d 41 47 37 38 45 58 4e 41 41 30 37 35 4e 20 20 20 20 20'}
rsp_DIMM0_module_part_num_rsp_newCOMe_SKU1 = {"module part number" : '31 38 41 53 46 32 47 37 32 48 5a 2d 33 47 32 52 31 20 20 20'}
rsp_DIMM0_module_manu_id_rsp = {"module manufacture ID" : '00 ad'}
rsp_DIMM0_module_manu_id_sku5 = {"module manufacture ID" : '00 20'}
cmd_DIMM_module_part_num_test_dc = '0x31 0x38 0x41 0x53 0x46 0x32 0x47 0x37 0x32 0x48 0x5a 0x2d 0x32 0x47 0x36 0x45 0x31 0x20 0x20 0x20'
cmd_DIMM_module_part_num_test_rsp = '0x48 0x4d 0x41 0x38 0x32 0x47 0x53 0x37 0x44 0x4a 0x52 0x38 0x4e 0x2d 0x56 0x4b 0x20 0x20 0x20 0x20'
cmd_DIMM_module_part_num_test_rsp_newCOMe = '0x48 0x4d 0x41 0x47 0x37 0x38 0x45 0x58 0x4e 0x41 0x41 0x30 0x37 0x35 0x4e 0x20 0x20 0x20 0x20 0x20'
cmd_DIMM_module_part_num_test_rsp_newCOMe_SKU1 = '0x31 0x38 0x41 0x53 0x46 0x32 0x47 0x37 0x32 0x48 0x5a 0x2d 0x33 0x47 0x32 0x52 0x31 0x20 0x20 0x20'
cmd_DIMM_module_manu_id_test_rsp = '0x00 0xad'
cmd_DIMM_module_manu_id_test_rsp_NewCOMe = '0x00 0x2c'
rsp_DIMM0_module_serial_num = {
    "module serial number" : 'ANY'
}
rsp_DIMM1_module_serial_num = {
    "module serial number" : 'ANY'
}
rsp_DIMM0_module_manu_id = {
    "module manufacture ID" : '00 2c'
}
rsp_DIMM0 = {
    "DIMM location" : rsp_DIMM0_location,
    "DIMM type"     : rsp_DIMM0_type,
    "DIMM speed"    : rsp_DIMM0_speed,
    "DIMM module part num"    : rsp_DIMM0_module_part_num,
    "DIMM module serial num"  : rsp_DIMM0_module_serial_num,
    "DIMM module manufacture ID" : rsp_DIMM0_module_manu_id
}
rsp_DIMM1 = {
    "DIMM location" : rsp_DIMM1_location,
    "DIMM type"     : rsp_DIMM0_type,
    "DIMM speed"    : rsp_DIMM0_speed,
    "DIMM module part num"    : rsp_DIMM0_module_part_num,
    "DIMM module serial num"  : rsp_DIMM1_module_serial_num,
    "DIMM module manufacture ID" : rsp_DIMM0_module_manu_id
}
rsp_DIMM_test = {
    "DIMM location" : rsp_DIMM_location_test,
    "DIMM type"     : rsp_DIMM_type_test,
    "DIMM speed"    : rsp_DIMM_speed_test,
    "DIMM module part num"    : rsp_DIMM_module_part_num_test,
    "DIMM module serial num"  : rsp_DIMM_module_serial_num_test,
    "DIMM module manufacture ID" : rsp_DIMM_module_manu_id_test
}

#### FB_BMC_COMM_TC_077 ####
cmd_get_proc_info        = 'ipmitool raw 0x36 0x11 0x57 0x01 0x00'
cmd_set_proc_info        = 'ipmitool raw 0x36 0x10 0x57 0x01 0x00'
cmd_product_name     = '0x01'
cmd_basic_info       = '0x02'
rsp_proc_name = {
    "Product Name" : "Intel(R) Xeon(R) CPU D-1527 @ 2.20GHz"
}
rsp_proc_basic_info = {
    "Core Number"             : 4,
    "Thread Number"           : 8,
    "Processor frequency MHz" : 2200,
    "Revision"                : "58 58"
}
rsp_proc_name_test = {
    "Product Name" : ""
}
rsp_proc_basic_info_test = {
    "Core Number"             : 0,
    "Thread Number"           : 0,
    "Processor frequency MHz" : 0,
    "Revision"                : "00 00"
}
rsp_proc0 = {
    "processor name"       : rsp_proc_name,
    "processor basic info" : rsp_proc_basic_info
}
rsp_proc_test = {
    "processor name"       : rsp_proc_name_test,
    "processor basic info" : rsp_proc_basic_info_test
}
cmd_proc_name_test = ' '.join(['00'] * 48)
cmd_proc_basic_info_test = ' '.join(['00'] * 7)

#### FB_BMC_COMM_TC_084 ####
cmd_get_mem_info = 'cat /proc/meminfo'
common_path = '/mnt/data1/BMC_Diag/common/'

#### FB_BMC_COMM_TC_085 ####
test_cmd_sol_test = 'uname -a'
expected_kernel = r'Linux \\w+.*\\d+\\.\\d+\\.\\d+'
sol_test_iteration = 3

#### FB_BMC_COMM_TC_086 ####
power_on_val = '0x07'
power_off_val = '0x05'
scm_cpld_addr = '0x3e'
come_pwr_ctrl_reg = '0x14'

#### FB_BMC_COMM_TC_087 ####
tpm_untar_keyword = 'TPM2_Test_Scripts/README.md'
tpm_pass_keyword = 'test_tpm2_dictionarylockout.sh pass'
tpm_result = {
    'Tests passed' : '19',
    'Tests Failed' : '0'
}
CHECK_TPM_PATH_CMD = 'ls /dev/tpm* |grep tpmrm1'
TPMRM1_PATH = '/dev/tpmrm1'
TPMRM0_PATH = '/dev/tpmrm0'

#### FB_BMC_COMM_TC_089 ####
mdio_reg_test = '0xe'
mdio_0xe_default = '0x1140'
mdio_0xe_test1 = '0x00'
mdio_0xe_test2 = '0x1000'
mdio_reg_test_mp2 = '0x0a'
mdio_bus_2 = '2'
mdio_reg_test_cr = '0x0d'
mdio_bus_4 = '4'
mac_second = '2'
mdio_0x0_reg_test = '0x0'
mdio_0x0_default = '0x141'
mdio_reg_test1 = '0x02'
mac_first = '1'
mdio_0x1_reg_test = '0x1'
mdio_reg_test2 = '0x16'
mdio_reg_test3 = '0x10'
eth_tool = 'up'
eth_tool_down = 'down'

#### FB_BMC_COMM_TC_090 ####
cit_tool = 'tests/wedge400/*'
local_tool_path = '/run'
python_path = '/usr/lib/python3.8/'
CIT_PASS = r'OK \(skipped=\d+\)'
CIT_PASS_PSU = r'OK \(skipped=49\)'
CIT_PASS_PSU_RSP = r'OK \(skipped=34\)'
CIT_PASS_PEM = r'OK \(skipped=41\)'
CIT_PASS_PEM_RSP = r'OK \(skipped=31\)'
cit_test_cmd = 'python cit_runner.py --platform wedge400'
log_debug_level = "sed -i -e 's#\"level\": \"INFO\"#\"level\": \"DEBUG\"#g' -e 's#\"maxBytes\": 100000#\"maxBytes\": 1000000#g' utils/cit_logger.py"
cit_log_file = '/tmp/cit.log'

error_code_array = {
    "code" : "0xd5",
    "message" : "Command not supported in present state"
}

completion_code_array = {
    "code" : "0xc7",
    "message" : "Request data length invalid"
}

cpu_uart_log_path = '/var/log/mTerm_wedge.log'

diag_image_file=SwImage.getSwImage(SwImage.DIAG).newImage

OPENBMC_MODE = 'openbmc'
CENTOS_MODE = 'centos'
MASTER_DEV = 'mtd4'
SLAVE_DEV = 'mtd5'
GET = 'get'
POST = 'post'
Other = 'other'
LOCALHOST = '127.0.0.1'
LOCALHOST_SPEC = 'localhost'
WDT_RSP_COUNT = 8
FAN_NUM = 4
OPENBMC_VER = 'BMC Version'
SLAVE = 'Slave'
MASTER = 'Master'
RESET_MESSAGE = 'DRAM Init-V12-DDR4'
CPLD_VER_CMD = 'cpld_ver.sh'
FPGA_VER_CMD = 'fpga_ver.sh'
SCM_VER_CMD = 'fw-util scm --version'
has_pem = True
SPI_UPDATE_PASS_MSG = r'Verifying flash.*VERIFIED'
SPI_ERASE_WRITE_MSG = r'Erase/write done|Verifying flash.*VERIFIED'

#### FB_BMC_COMM_TC_006 ####
FCM_CPLD_UPDATE_CMD = 'fcmcpld_update.sh'
SCM_CPLD_UPDATE_CMD = 'scmcpld_update.sh'
SMB_CPLD_UPDATE_CMD = 'smbcpld_update.sh'
PWR_CPLD_UPDATE_CMD = 'pwrcpld_update.sh'
FCM_T_CPLD_UPDATE_CMD = 'cpld_update.sh -s FCM-T -f'
FCM_B_CPLD_UPDATE_CMD = 'cpld_update.sh -s FCM-B -f'
PWR_L_CPLD_UPDATE_CMD = 'cpld_update.sh -s PWR-L -f'
PWR_R_CPLD_UPDATE_CMD = 'cpld_update.sh -s PWR-R -f'
SMB_CPLD_KEY = 'SMB_SYSCPLD'
PWR_CPLD_KEY = 'SMB_PWRCPLD'

#### FB_BMC_MP2_TC_004, FB_BMC_MP2_TC_008 ####
PIM_NUM = 8
pim_eeprom_path = '/mnt/data1/BMC_Diag/utility/PIM_eeprom'
pim_eeprom_test = 'PIM_EEPROM_TEST'
pim_eeprom_test2 = 'PIM_EEPROM_TEST2'
pim_eeprom_product_name = 'PIM_EEPROM_DEFAULT'

PIM_UPDATE_CMD = 'pim_upgrade.sh all'
PIM_UPDATE_PASS_MSG = 'done'
FPGA_UPDATE_FAIL_MSG = 'fail|error'
PIM_REINIT_CMD = 'reinit_all_pim.sh'

#### FB_BMC_MP2_TC_005 ####
sim_eeprom_path = '/mnt/data1/BMC_Diag/utility/SIM_eeprom'
sim_eeprom_test = 'SIM_EEPROM_TEST'
sim_eeprom_test2 = 'SIM_EEPROM_TEST2'
sim_eeprom_product_name = 'SIM_EEPROM_DEFAULT'
sim_eeprom_product_name_dc = 'SIM_EEPROM_DEFAULT_DC'
sim_eeprom_test_dc = 'SIM_EEPROM_TEST_DC'
sim_eeprom_test2_dc = 'SIM_EEPROM_TEST2_DC'

IOB_FPGA_KEY = 'IOB FPGA'
IOB_FPGA_DIAG_KEY = 'SMB_IOB_FPGA'

#### FB_BMC_W400C_TC_007 ####
bsm_eeprom_path = all_eeprom_path

#### FB_BMC_MP2_TC_009 ####
bmc_eeprom_path = '/mnt/data1/BMC_Diag/utility/BMC_eeprom'

#### FB_BMC_COMM_TC_010 ####
oob_eeprom_name = 'BCM5389_EE'
oob_spi = 'spi1'
re_run_oob_command_list = [
        'spi_util.sh read spi2 BCM5387_EE dump1',
        'hexdump -C dump1',
        'spi_util.sh erase spi2 BCM5387_EE',
        'spi_util.sh read spi2 BCM5387_EE dump2',
        'hexdump -C dump2',
        'spi_util.sh write spi2 BCM5387_EE /mnt/data1/BMC_Diag/firmware/OOB/mp2_swapped.bin',
        'spi_util.sh read spi2 BCM5387_EE dump3',
        'hexdump -C dump3',
    ]

#### FB_BMC_W400C_TC_001 ####
PSU_NUM = 2
PSU_NUM_DC = 1

####################### MINIPACK2 #############################
if "minipack2" in devicename.lower():
    tpm_result = {
    'Tests passed' : '19',
    'Tests Failed' : '0'
}
    img_th4_path = SwImage.getSwImage(SwImage.TH4).hostImageDir
    local_th4_path = SwImage.getSwImage(SwImage.TH4).localImageDir

    img_cpld_path = SwImage.getSwImage(SwImage.CPLD).hostImageDir
    local_cpld_path = SwImage.getSwImage(SwImage.CPLD).localImageDir

    dhcp_messages_list = [
        #r'Setting vendor information in \/e.*\[.*?\] using self ethernet address:.*?'
         r'Setting\svendor\sinformation\sin\s\/etc\/dhcp\/dhclient\.conf'
]
    re_run_oob_command_list = [
        'spi_util.sh read spi2 BCM5387_EE dump1',
        'hexdump -C dump1',
        'spi_util.sh erase spi2 BCM5387_EE',
        'spi_util.sh read spi2 BCM5387_EE dump2',
        'hexdump -C dump2',
        'spi_util.sh write spi2 BCM5387_EE /mnt/data1/BMC_Diag/firmware/OOB/mp2_swapped.bin',
        'spi_util.sh read spi2 BCM5387_EE dump3',
        'hexdump -C dump3',
    ]

    RESET_MESSAGE = 'Starting kernel'
    CPLD_VER_CMD = 'fw-util cpld --version'
    FPGA_VER_CMD = 'fw-util fpga --version'
    has_pem = False
    SPI_UPDATE_PASS_MSG = r'Verifying flash.*VERIFIED'

    #### FB_BMC_COMM_TC_006 ####
    FCM_CPLD_UPDATE_CMD = 'cpld_update.sh -s FCM -f'
    SCM_CPLD_UPDATE_CMD = 'cpld_update.sh -s SCM -f'
    SMB_CPLD_UPDATE_CMD = 'cpld_update.sh -s SMB -f'
    PWR_CPLD_UPDATE_CMD = 'cpld_update.sh -s PDB -f'
    SMB_CPLD_KEY = 'SMBCPLD'

    SDK_INIT_CMD = './%s'%(SDK_SCRIPT)
    SDK_PROMPT = BCM_promptstr
    SDK_EXIT_CMD = 'exit'

    #### FB_BMC_COMM_TC_003 ####
    MASTER_DEV = 'mtd5'

    #### FB_BMC_COMM_TC_019 ####
    cmd_read_mac_from_eeprom = './eeprom_tool -d'
    mac_eeprom_path = sim_eeprom_path
    mac_eeprom_type = 'SIM'

    #### FB_BMC_COMM_TC_036, FB_BMC_COMM_TC_046 ####
    scm_eeprom_path = '/mnt/data1/BMC_Diag/utility/SCM_eeprom'
    smb_eeprom_path = '/mnt/data1/BMC_Diag/utility/SMB_eeprom'
    fan_eeprom_path = '/mnt/data1/BMC_Diag/utility/FAN_eeprom'
    fcm_b_eeprom_path = '/mnt/data1/BMC_Diag/utility/FCM_B_eeprom'
    fcm_t_eeprom_path = '/mnt/data1/BMC_Diag/utility/FCM_T_eeprom'
    smb_eeprom_product_name = 'SMB_EEPROM_DEFAULT'
    smb_eeprom_test = 'SMB_EEPROM_TEST'
    smb_eeprom_test2 = 'SMB_EEPROM_TEST2'

    #### FB_BMC_COMM_TC_037 ####
    FAN_NUM = 8

    #### FB_BMC_COMM_TC_038 ####
    psu1_eeprom_dict_tc_038 = {
        'FRU Information'      : 'PSU1 (Bus:48 Addr:0x50)'
    }
    psu2_eeprom_dict_tc_038 = {
        'FRU Information'      : 'PSU2 (Bus:49 Addr:0x52)'
    }
    psu3_eeprom_dict_tc_038 = {
        'FRU Information'      : 'PSU3 (Bus:56 Addr:0x50)'
    }
    psu4_eeprom_dict_tc_038 = {
        'FRU Information'      : 'PSU4 (Bus:57 Addr:0x52)'
    }

    #### FB_BMC_COMM_TC_049_SPI_Utility_Test ####
    str_1 = 'Usage:||  spi_util.sh <op> <spi1|spi2> <spi device> <file>||    <op>          : read, write, erase||    <spi1 device> : TH4_PCIE_FLASH, IOB_FPGA, PCIE_SW, COME_BIOS, DOM_FPGA_ALL, DOM_FPGA_PIM1 ~ DOM_FPGA_PIM8||    <spi2 device> : BCM5387_EE, SMB_EE||||Examples:||  spi_util.sh write spi1 DOM_FPGA_PIM7 domfpga.bit'

    #### FB_BMC_COMM_TC_051 ####
    presence_dict = {
        'scm'  : '1',
        'pim1' : '1',
        'pim2' : '1',
        'pim3' : '1',
        'pim4' : '1',
        'pim5' : '1',
        'pim6' : '1',
        'pim7' : '1',
        'pim8' : '1',
        'fan1' : '1',
        'fan2' : '1',
        'fan3' : '1',
        'fan4' : '1',
        'fan5' : '1',
        'fan6' : '1',
        'fan7' : '1',
        'fan8' : '1',
        'psu1' : '1',
        'psu2' : '1',
        'psu3' : '1',
        'psu4' : '1'
    }

    presence_dict_dc = {
        'scm'  : '1',
        'pim1' : '1',
        'pim2' : '1',
        'pim3' : '0',
        'pim4' : '0',
        'pim5' : '0',
        'pim6' : '1',
        'pim7' : '1',
        'pim8' : '1',
        'fan1' : '1',
        'fan2' : '1',
        'fan3' : '1',
        'fan4' : '1',
        'fan5' : '1',
        'fan6' : '1',
        'fan7' : '1',
        'fan8' : '1',
        'psu1' : '0',
        'psu2' : '0',
        'psu3' : '1',
        'psu4' : '1'
    }

    #### FB_BMC_COMM_TC_054 ####
    psu1_info_dict_tc_054_Liteon = {
        'PSU Information': 'PSU1 (Bus:48 Addr:0x58)',
        'MFR_ID             (0x99)': 'Liteon',
        'MFR_MODEL          (0x9A)': 'PS-2152-5L',
        'MFR_REVISION       (0x9B)': '01',
        'MFR_DATE           (0x9D)': 'ANY',
        'MFR_SERIAL         (0x9E)': 'ANY',
    }
    psu2_info_dict_tc_054_Liteon = {
        'PSU Information': 'PSU2 (Bus:49 Addr:0x5a)',
        'MFR_ID             (0x99)': 'Liteon',
        'MFR_MODEL          (0x9A)': 'PS-2152-5L',
        'MFR_REVISION       (0x9B)': '01',
        'MFR_DATE           (0x9D)': 'ANY',
        'MFR_SERIAL         (0x9E)': 'ANY',
    }
    psu3_info_dict_tc_054_Liteon = {
        'PSU Information': 'PSU3 (Bus:56 Addr:0x58)',
        'MFR_ID             (0x99)': 'Liteon',
        'MFR_MODEL          (0x9A)': 'PS-2152-5L',
        'MFR_REVISION       (0x9B)': '01',
        'MFR_DATE           (0x9D)': 'ANY',
        'MFR_SERIAL         (0x9E)': 'ANY',
    }
    psu4_info_dict_tc_054_Liteon = {
        'PSU Information': 'PSU4 (Bus:57 Addr:0x5a)',
        'MFR_ID             (0x99)': 'Liteon',
        'MFR_MODEL          (0x9A)': 'PS-2152-5L',
        'MFR_REVISION       (0x9B)': '01',
        'MFR_DATE           (0x9D)': 'ANY',
        'MFR_SERIAL         (0x9E)': 'ANY',
    }
    psu1_eeprom_dict_tc_054_liteon = {
        'FRU Information': 'PSU1 (Bus:48 Addr:0x50)',
        'Product Manufacturer': 'LITE-ON',
        'Product Name': 'LITE-ON POWER SUPPLY',
        'Product Part Number': 'PS-2152-5L',
        #'Product Version': '00',
        'Product Serial': 'ANY',
        'Product Asset Tag': 'N/A',
        'Product FRU ID': 'N/A'
    }
    psu2_eeprom_dict_tc_054_liteon = {
        'FRU Information': 'PSU2 (Bus:49 Addr:0x52)',
        'Product Manufacturer': 'LITE-ON',
        'Product Name': 'LITE-ON POWER SUPPLY',
        'Product Part Number': 'PS-2152-5L',
        # 'Product Version': '00',
        'Product Serial': 'ANY',
        'Product Asset Tag': 'N/A',
        'Product FRU ID': 'N/A'
    }
    psu3_eeprom_dict_tc_054_liteon = {
        'FRU Information': 'PSU3 (Bus:56 Addr:0x50)',
        'Product Manufacturer': 'LITE-ON',
        'Product Name': 'LITE-ON POWER SUPPLY',
        'Product Part Number': 'PS-2152-5L',
        # 'Product Version': '00',
        'Product Serial': 'ANY',
        'Product Asset Tag': 'N/A',
        'Product FRU ID': 'N/A'
    }
    psu4_eeprom_dict_tc_054_liteon = {
        'FRU Information': 'PSU4 (Bus:57 Addr:0x52)',
        'Product Manufacturer': 'LITE-ON',
        'Product Name': 'LITE-ON POWER SUPPLY',
        'Product Part Number': 'PS-2152-5L',
        # 'Product Version': '00',
        'Product Serial': 'ANY',
        'Product Asset Tag': 'N/A',
        'Product FRU ID': 'N/A'
    }
    psu1_eeprom_dict_tc_054 = {
        'FRU Information'      : 'PSU1 (Bus:48 Addr:0x50)',
        'Product Manufacturer' : 'DELTA',
        'Product Name'         : 'DDM1500BH12A3F',
        'Product Part Number'  : 'ECD55020006',
        'Product Version'      : '00',
        'Product Serial'       : 'ANY',
        'Product Asset Tag'    : 'N/A',
        'Product FRU ID'       : 'P3C300A00'
    }
    psu2_eeprom_dict_tc_054 = {
        'FRU Information'      : 'PSU2 (Bus:49 Addr:0x52)',
        'Product Manufacturer' : 'DELTA',
        'Product Name'         : 'DDM1500BH12A3F',
        'Product Part Number'  : 'ECD55020006',
        'Product Version'      : '00',
        'Product Serial'       : 'ANY',
        'Product Asset Tag'    : 'N/A',
        'Product FRU ID'       : 'P3C300A00'
    }
    psu3_eeprom_dict_tc_054 = {
        'FRU Information'      : 'PSU3 (Bus:56 Addr:0x50)',
        'Product Manufacturer' : 'DELTA',
        'Product Name'         : 'DDM1500BH12A3F',
        'Product Part Number'  : 'ECD55020006',
        'Product Version'      : '00',
        'Product Serial'       : 'ANY',
        'Product Asset Tag'    : 'N/A',
        'Product FRU ID'       : 'P3C300A00'
    }
    psu3_eeprom_dict_tc_054_Delta_dc = {
        'FRU Information': 'PSU3 (Bus:56 Addr:0x50)',
        'System Manufacturer': 'DELTA',
        'Product Name': 'MINIPACK2-DC-PSU-48V',
        #'Product Part Number': '',
        'Product Version': '0',
        'Product Serial Number': 'ANY',
        #'Product Asset Tag': '',
        #'Product FRU ID': 'P3C300A00'
    }
    psu3_eeprom_dict_tc_054_Delta_dc_rework = {
        'FRU Information': 'PSU3 (Bus:56 Addr:0x50)',
        'System Manufacturer': 'DELTA',
        'Product Name': 'DC-PSU-48V',
        # 'Product Part Number': '',
        'Product Version': '1',
        'Product Serial Number': 'ANY',
        # 'Product Asset Tag': '',
        # 'Product FRU ID': 'P3C300A00'
    }
    psu3_eeprom_dict_tc_054_Delta_dc_rework_new = {
        'FRU Information': 'PSU3 (Bus:56 Addr:0x50)',
        'System Manufacturer': 'DELTA',
        'Product Name': 'DC-PSU-48V',
        # 'Product Part Number': '',
        'Product Version': '2',
        'Product Serial Number': 'ANY',
        # 'Product Asset Tag': '',
        # 'Product FRU ID': 'P3C300A00'
    }
    psu3_eeprom_dict_tc_054_Delta_dc_rework_new_second = {
        'FRU Information': 'PSU3 (Bus:56 Addr:0x50)',
        'System Manufacturer': 'DELTA',
        'Product Name': 'DC-PSU-48V',
        # 'Product Part Number': '',
        'Product Version': '1',
        'Product Serial Number': 'ANY',
        # 'Product Asset Tag': '',
        # 'Product FRU ID': 'P3C300A00'
    }
    psu3_eeprom_dict_tc_054_Liteon_dc = {
        'FRU Information': 'PSU3 (Bus:56 Addr:0x50)',
        'System Manufacturer': 'Liteon',
        'Product Name': 'MINIPACK2-DC-PSU-48V',
        #'Product Part Number': '',
        'Product Version': '0',
        'Product Serial Number': 'ANY',
        #'Product Asset Tag': '',
        #'Product FRU ID': 'P3C300A00'
    }
    psu3_eeprom_dict_tc_054_Liteon_dc_rework = {
        'FRU Information': 'PSU3 (Bus:56 Addr:0x50)',
        'System Manufacturer': 'Liteon',
        'Product Name': 'DC-PSU-48V',
        'Product Version': '0',
        'Product Serial Number': 'ANY',
    }
    psu4_eeprom_dict_tc_054 = {
        'FRU Information'      : 'PSU4 (Bus:57 Addr:0x52)',
        'Product Manufacturer' : 'DELTA',
        'Product Name'         : 'DDM1500BH12A3F',
        'Product Part Number'  : 'ECD55020006',
        'Product Version'      : '00',
        'Product Serial'       : 'ANY',
        'Product Asset Tag'    : 'N/A',
        'Product FRU ID'       : 'P3C300A00'
    }
    psu4_eeprom_dict_tc_054_Delta_dc = {
        'FRU Information': 'PSU4 (Bus:57 Addr:0x52)',
        'System Manufacturer': 'DELTA',
        'Product Name': 'MINIPACK2-DC-PSU-48V',
        # 'Product Part Number': '',
        'Product Version': '0',
        'Product Serial Number': 'ANY',
        # 'Product Asset Tag': '',
        # 'Product FRU ID': 'P3C300A00'
    }
    psu4_eeprom_dict_tc_054_Delta_dc_rework = {
        'FRU Information': 'PSU4 (Bus:57 Addr:0x52)',
        'System Manufacturer': 'DELTA',
        'Product Name': 'DC-PSU-48V',
        # 'Product Part Number': '',
        'Product Version': '1',
        'Product Serial Number': 'ANY',
        # 'Product Asset Tag': '',
        # 'Product FRU ID': 'P3C300A00'
    }
    psu4_eeprom_dict_tc_054_Delta_dc_rework_new = {
        'FRU Information': 'PSU4 (Bus:57 Addr:0x52)',
        'System Manufacturer': 'DELTA',
        'Product Name': 'DC-PSU-48V',
        # 'Product Part Number': '',
        'Product Version': '2',
        'Product Serial Number': 'ANY',
        # 'Product Asset Tag': '',
        # 'Product FRU ID': 'P3C300A00'
    }

    psu4_eeprom_dict_tc_054_Liteon_dc = {
        'FRU Information': 'PSU4 (Bus:57 Addr:0x52)',
        'System Manufacturer': 'Liteon',
        'Product Name': 'MINIPACK2-DC-PSU-48V',
        # 'Product Part Number': '',
        'Product Version': '0',
        'Product Serial Number': 'ANY',
        # 'Product Asset Tag': '',
        # 'Product FRU ID': 'P3C300A00'
    }
    psu4_eeprom_dict_tc_054_Liteon_dc_rework = {
        'FRU Information': 'PSU4 (Bus:57 Addr:0x52)',
        'System Manufacturer': 'Liteon',
        'Product Name': 'DC-PSU-48V',
        'Product Version': '0',
        'Product Serial Number': 'ANY',
    }
    psu1_info_dict_tc_054 = {
        'PSU Information'           : 'PSU1 (Bus:48 Addr:0x58)',
        'MFR_ID             (0x99)' : 'Delta',
        'MFR_MODEL          (0x9A)' : 'ECD55020006',
        'MFR_REVISION       (0x9B)' : '00',
        'MFR_DATE           (0x9D)' : 'ANY',
        'MFR_SERIAL         (0x9E)' : 'ANY',
        # 'PRI_FW_VER         (0xDD)' : '4.0',
        # 'SEC_FW_VER         (0xD7)' : '3.2',
    }
    psu2_info_dict_tc_054 = {
        'PSU Information'           : 'PSU2 (Bus:49 Addr:0x5a)',
        'MFR_ID             (0x99)' : 'Delta',
        'MFR_MODEL          (0x9A)' : 'ECD55020006',
        'MFR_REVISION       (0x9B)' : '00',
        'MFR_DATE           (0x9D)' : 'ANY',
        'MFR_SERIAL         (0x9E)' : 'ANY',
        # 'PRI_FW_VER         (0xDD)' : '4.0',
        # 'SEC_FW_VER         (0xD7)' : '3.2',
    }
    psu3_info_dict_tc_054 = {
        'PSU Information'           : 'PSU3 (Bus:56 Addr:0x58)',
        'MFR_ID             (0x99)' : 'Delta',
        'MFR_MODEL          (0x9A)' : 'ECD55020006',
        'MFR_REVISION       (0x9B)' : '00',
        'MFR_DATE           (0x9D)' : 'ANY',
        'MFR_SERIAL         (0x9E)' : 'ANY',
        # 'PRI_FW_VER         (0xDD)' : '4.0',
        # 'SEC_FW_VER         (0xD7)' : '3.2',
    }
    psu3_info_dict_tc_054_Delta_dc = {
        'PSU Information': 'PSU3 (Bus:56 Addr:0x58)',
        'MFR_ID             (0x99)': 'Delta',
        'MFR_MODEL          (0x9A)': 'ECD25010015',
        'MFR_REVISION       (0x9B)': 'P2.1',
        'MFR_DATE           (0x9D)': 'ANY',
        'MFR_SERIAL         (0x9E)': 'ANY',
        # 'PRI_FW_VER         (0xDD)' : '4.0',
        # 'SEC_FW_VER         (0xD7)' : '3.2',
    }
    psu3_info_dict_tc_054_Delta_dc_new = {
        'PSU Information': 'PSU3 (Bus:56 Addr:0x58)',
        'MFR_ID             (0x99)': 'Delta',
        'MFR_MODEL          (0x9A)': 'ECD25010015',
        'MFR_REVISION       (0x9B)': '02',
        'MFR_DATE           (0x9D)': 'ANY',
        'MFR_SERIAL         (0x9E)': 'ANY',
        # 'PRI_FW_VER         (0xDD)' : '4.0',
        # 'SEC_FW_VER         (0xD7)' : '3.2',
    }
    psu3_info_dict_tc_054_Liteon_dc = {
        'PSU Information': 'PSU3 (Bus:56 Addr:0x58)',
        'MFR_ID             (0x99)': 'Liteon',
        'MFR_MODEL          (0x9A)': 'DD-2152-2L',
        'MFR_REVISION       (0x9B)': '01',
        'MFR_DATE           (0x9D)': 'ANY',
        'MFR_SERIAL         (0x9E)': 'ANY',
    }
    psu4_info_dict_tc_054 = {
        'PSU Information'           : 'PSU4 (Bus:57 Addr:0x5a)',
        'MFR_ID             (0x99)' : 'Delta',
        'MFR_MODEL          (0x9A)' : 'ECD55020006',
        'MFR_REVISION       (0x9B)' : '00',
        'MFR_DATE           (0x9D)' : 'ANY',
        'MFR_SERIAL         (0x9E)' : 'ANY',
        # 'PRI_FW_VER         (0xDD)' : '4.0',
        # 'SEC_FW_VER         (0xD7)' : '3.2',
    }
    psu4_info_dict_tc_054_Delta_dc = {
        'PSU Information': 'PSU4 (Bus:57 Addr:0x5a)',
        'MFR_ID             (0x99)': 'Delta',
        'MFR_MODEL          (0x9A)': 'ECD25010015',
        'MFR_REVISION       (0x9B)': 'P2.1',
        'MFR_DATE           (0x9D)': 'ANY',
        'MFR_SERIAL         (0x9E)': 'ANY',
        # 'PRI_FW_VER         (0xDD)' : '4.0',
        # 'SEC_FW_VER         (0xD7)' : '3.2',
    }
    psu4_info_dict_tc_054_Delta_dc_new = {
        'PSU Information': 'PSU4 (Bus:57 Addr:0x5a)',
        'MFR_ID             (0x99)': 'Delta',
        'MFR_MODEL          (0x9A)': 'ECD25010015',
        'MFR_REVISION       (0x9B)': '02',
        'MFR_DATE           (0x9D)': 'ANY',
        'MFR_SERIAL         (0x9E)': 'ANY',
        # 'PRI_FW_VER         (0xDD)' : '4.0',
        # 'SEC_FW_VER         (0xD7)' : '3.2',
    }
    psu4_info_dict_tc_054_Liteon_dc = {
        'PSU Information': 'PSU4 (Bus:57 Addr:0x5a)',
        'MFR_ID             (0x99)': 'Liteon',
        'MFR_MODEL          (0x9A)': 'DD-2152-2L',
        'MFR_REVISION       (0x9B)': '01',
        'MFR_DATE           (0x9D)': 'ANY',
        'MFR_SERIAL         (0x9E)': 'ANY',
    }

    #### FB_BMC_COMM_TC_086 ####
    scm_cpld_addr = '0x35'

    #### FB_BMC_COMM_TC_010 ####
    oob_eeprom_name = 'BCM5387_EE'
    oob_spi = 'spi2'

    #### FB_BMC_COMM_TC_070 ####
    rsp_board_id = {
        "Board SKU ID"      : "06",
        "Board Revision ID" : "ANY",
        "MB Slot ID"        : "01",
        "Slot Config ID"    : "00"
    }

    #### FB_BMC_MP2_TC_003 ####
    PSU_NUM = 4
    PSU_NUM_DC = 2

    #### FB_BMC_MP2_TC_090 ####
    cit_tool = 'tests/fuji/*'
    CIT_PASS_PSU = r'OK \(skipped=2\)'
    cit_test_cmd = 'python cit_runner.py --platform fuji'
    cit_test_cmd_dc = 'python platform_config.py -c fuji_dc -p fuji'
    cit_test_cmd_rsp = 'python platform_config.py -c fuji_respin -p fuji'

####################### CLOUDRIPPER #############################
elif "cloudripper" in devicename.lower():

    RESET_MESSAGE = 'Power reset.*'
    SPI_UPDATE_PASS_MSG = r'Verifying flash.*VERIFIED'

    bmc_bin_path = '/mnt/data1/BMC_Diag/bin'
    bmc_version_cmd = './cel-software-test -h'
    #### FB_BMC_COMM_TC_003 ####
    MASTER_DEV = 'mtd5'
    SLAVE_DEV = 'mtd6'

    #### FB_BMC_COMM_TC_006 ####
    FCM_CPLD_UPDATE_CMD = 'cpld_update.sh -s FCM -f'
    SCM_CPLD_UPDATE_CMD = 'cpld_update.sh -s SCM -f'
    SMB_CPLD_UPDATE_CMD = 'cpld_update.sh -s SMB -f'
    PWR_CPLD_UPDATE_CMD = 'cpld_update.sh -s PWR -f'

    #### FB_BMC_COMM_TC_010 ####
    oob_eeprom_name = 'BCM5389_EE'
    oob_spi = 'spi2'

    #### FB_BMC_COMM_TC_049_SPI_Utility_Test ####
    str_1 = 'Usage:||  spi_util.sh <op> <spi1> <spi device> <file>||    <op>          : read, write, erase||    <spi1 device> : BIOS, GB_PCIE_FLASH, DOM_FPGA_FLASH1, DOM_FPGA_FLASH2||    <spi2 device> : BCM5389_EE||||Examples:||  spi_util.sh write spi1 BIOS bios.bin'

    has_pem = False

    #### FB_BMC_COMM_TC_038 ####
    psu1_eeprom_dict_tc_038 = {
        'FRU Information'      : 'PSU1 (Bus:40 Addr:0x50)'
    }
    psu2_eeprom_dict_tc_038 = {
        'FRU Information'      : 'PSU2 (Bus:41 Addr:0x50)'
    }

    #### FB_BMC_COMM_TC_054 ####
    psu1_info_dict_tc_054 = {
        'PSU Information'           : 'PSU1 (Bus:40 Addr:0x58)',
        'MFR_ID             (0x99)' : 'Murata-PS',
        'MFR_MODEL          (0x9A)' : 'D1U54T-W-2000-12-HC4TC-FB',
        'MFR_REVISION       (0x9B)' : '0501-0701-0000',
        'MFR_DATE           (0x9D)' : 'ANY',
        'MFR_SERIAL         (0x9E)' : 'ANY',
        # 'PRI_FW_VER         (0xDD)' : '0.5',
        # 'SEC_FW_VER         (0xD7)' : '0.7',
    }
    psu2_info_dict_tc_054 = {
        'PSU Information'           : 'PSU2 (Bus:41 Addr:0x58)',
        'MFR_ID             (0x99)' : 'Murata-PS',
        'MFR_MODEL          (0x9A)' : 'D1U54T-W-2000-12-HC4TC-FB',
        'MFR_REVISION       (0x9B)' : '0501-0701-0000',
        'MFR_DATE           (0x9D)' : 'ANY',
        'MFR_SERIAL         (0x9E)' : 'ANY',
        # 'PRI_FW_VER         (0xDD)' : '0.5',
        # 'SEC_FW_VER         (0xD7)' : '0.7',
    }
    psu1_eeprom_dict_tc_054 = {
        'FRU Information'      : 'PSU1 (Bus:40 Addr:0x50)',
        'Product Manufacturer' : 'Murata-PS',
        'Product Name'         : 'M5819',
        'Product Part Number'  : 'D1U54T-W-2000-12-HC4TC-FB',
        'Product Version'      : 'E02',
        'Product Serial'       : 'ANY',
        'Product Asset Tag'    : 'N/A',
        'Product FRU ID'       : 'N/A'
    }
    psu2_eeprom_dict_tc_054 = {
        'FRU Information'      : 'PSU2 (Bus:41 Addr:0x50)',
        'Product Manufacturer' : 'Murata-PS',
        'Product Name'         : 'M5819',
        'Product Part Number'  : 'D1U54T-W-2000-12-HC4TC-FB',
        'Product Version'      : 'E02',
        'Product Serial'       : 'ANY',
        'Product Asset Tag'    : 'N/A',
        'Product FRU ID'       : 'N/A'
    }

    #### FB_BMC_COMM_TC_022, FB_BMC_COMM_TC_053 ####
    sdk_timeout = 3000

    #### FB_BMC_COMM_TC_070 ####
    rsp_board_id = {
        "Board SKU ID"      : "06",
        "Board Revision ID" : "00",
        "MB Slot ID"        : "01",
        "Slot Config ID"    : "00"
    }

    #### FB_BMC_COMM_TC_090 ####
    cit_tool = 'tests/cloudripper/*'
    CIT_PASS_PSU = r'OK \(skipped=1\)'
    python_path = '/usr/lib/python3.8/'
    cit_test_cmd = 'python cit_runner.py --platform cloudripper'

    smb_eeprom_product_name = 'SMB_EEPROM_DEFAULT'
    smb_eeprom_test = 'SMB_EEPROM_TEST'
    smb_eeprom_test2 = 'SMB_EEPROM_TEST2'

############### wedge400 #######################
elif "wedge400_" in devicename.lower():
    #### FB_BMC_COMM_TC_022 sensor check ####
    #python_tool = 'auto_load_user.sh'
    #SDK_INIT_CMD = './%s' % (python_tool)
    #SDK_PROMPT = 'BCM.0>'
    #SDK_EXIT_CMD = 'exit'

    #### FB_BMC_COMM_TC_051 ####
    presence_dict_dc = {
        'scm': '1',
        'fan1': '1',
        'fan2': '1',
        'fan3': '1',
        'fan4': '1',
        'psu1': '0',
        'psu2': '1',
        'pem1': '0',
        'pem2': '0',
        'debug_card': '0'
    }
   
    #### FB_BMC_COMM_TC_054 ####
    psu1_info_dict_tc_054 = {
        'PSU Information': 'PSU1 (Bus:24 Addr:0x58)',
        'MFR_ID             (0x99)': 'Delta',
        'MFR_MODEL          (0x9A)': 'ECD55020006',
        'MFR_REVISION       (0x9B)': 'PR',
        'MFR_DATE           (0x9D)': 'ANY',
        'MFR_SERIAL         (0x9E)': 'ANY',
    }
    psu1_eeprom_dict_tc_054 = {
        'FRU Information': 'PSU1 (Bus:24 Addr:0x50)',
        'Product Manufacturer': 'DELTA',
        'Product Name': 'DDM1500BH12A3F',
        'Product Part Number': 'ECD55020006',
        'Product Version': 'PR',
        'Product Serial': 'ANY',
        'Product Asset Tag': 'N/A',
        'Product FRU ID': 'P3C300A00'
    }
    psu2_info_dict_tc_054 = {
        'PSU Information': 'PSU2 (Bus:25 Addr:0x58)',
        'MFR_ID             (0x99)': 'Delta',
        'MFR_MODEL          (0x9A)': 'ECD55020006',
        'MFR_REVISION       (0x9B)': '00',
        'MFR_DATE           (0x9D)': 'ANY',
        'MFR_SERIAL         (0x9E)': 'ANY',
    }
    psu2_eeprom_dict_tc_054 = {
        'FRU Information': 'PSU2 (Bus:25 Addr:0x50)',
        'Product Manufacturer': 'DELTA',
        'Product Name': 'DDM1500BH12A3F',
        'Product Part Number': 'ECD55020006',
        'Product Version': '00',
        'Product Serial': 'ANY',
        'Product Asset Tag': 'N/A',
        'Product FRU ID': 'P3C300A00'
    }
   # psu2_info_dict_tc_054 = {
   #     'PSU Information': 'PSU2 (Bus:25 Addr:0x58)',
   #     'MFR_ID             (0x99)': 'Liteon',
   #     'MFR_MODEL          (0x9A)': 'DD-2152-2L',
   #     'MFR_REVISION       (0x9B)': 'X3',
   #     'MFR_DATE           (0x9D)': 'ANY',
   #     'MFR_SERIAL         (0x9E)': 'ANY',
   # }
   # psu2_eeprom_dict_tc_054 = {
   #     'FRU Information': 'PSU2 (Bus:25 Addr:0x50)',
   #     'System Manufacturer': 'Liteon',
   #     'Product Name': 'MINIPACK2-DC-PEM-48V',
   #     'Product Version': '0',
   #     'Product Serial Number': 'ANY',
   #     'Product Asset Tag': 'xxxxxxxx',
   # }

    #### FB_BMC_COMM_TC_076 ####
    #rsp_DIMM0 = {
    #    "DIMM location": {"DIMM Present": "01", "node number": "00", "channel number": "00", "DIMM number": "00"},
    #    "DIMM type": {"DIMM type" : 'c6'},
    #    "DIMM speed": {"DIMM speed": '55 08', "DIMM size": '00 40 00 00'},
    #    "DIMM module part num": {"module part number": '48 4d 41 38 32 47 53 37 44 4a 52 38 4e 2d 56 4b 20 20 20 00'},
    #    "DIMM module serial num": {"module serial number" : 'ANY'},
    #    "DIMM module manufacture ID": {"module manufacture ID": '00 ad'}
    #}

    #rsp_DIMM1 = {
    #    "DIMM location": {"DIMM Present": "01", "node number": "00", "channel number": "01", "DIMM number": "00"},
    #    "DIMM type": {"DIMM type" : 'c6'},
    #    "DIMM speed": {"DIMM speed": '55 08', "DIMM size": '00 40 00 00'},
    #    "DIMM module part num": {"module part number": '48 4d 41 38 32 47 53 37 44 4a 52 38 4e 2d 56 4b 20 20 20 00'},
    #    "DIMM module serial num": {"module serial number" : 'ANY'},
    #    "DIMM module manufacture ID": {"module manufacture ID": '00 ad'}
    #}
    #cmd_DIMM_module_part_num_test = '0x48 0x4d 0x41 0x38 0x32 0x47 0x53 0x37 0x44 0x4a 0x52 0x38 0x4e 0x2d 0x56 0x4b 0x20 0x20 0x20 0x00'
    #cmd_DIMM_module_manu_id_test = '0x00 0xad'
    #rsp_DIMM_test = {
    #    "DIMM location": {"DIMM Present": "01", "node number": "00", "channel number": "00", "DIMM number": "01"},
    #    "DIMM type": {"DIMM type" : 'c0'},
    #    "DIMM speed": {"DIMM speed": '55 08', "DIMM size": '00 00 40 00'},
    #    "DIMM module part num": {"module part number": '48 4d 41 38 32 47 53 37 44 4a 52 38 4e 2d 56 4b 20 20 20 00'},
    #    "DIMM module serial num": {"module serial number" : '21 0c 00 00'},
    #    "DIMM module manufacture ID": {"module manufacture ID": '00 ad'}
    #}

    #### FB_BMC_COMM_TC_077 ####
    cmd_proc_name_test = '0x43 0x41 0x50 0x20 0x41 0x75 0x74 0x6F 0x6D 0x61 0x74 0x69 0x6F 0x6E 0x20 0x46 0x6F 0x72 0x20 0x57 0x65 0x64 0x67 0x65 0x34 0x30 0x30 0x20 0x50 0x72 0x6F 0x6A 0x65 0x63 0x74 0x20 0x4F 0x70 0x65 0x6E 0x62 0x6D 0x63 0x20 0x55 0x6E 0x69 0x74'
    cmd_proc_basic_info_test = '0x01 0x02 0x03 0x04 0x05 0x06 0x07'
    rsp_proc_test = {
        "processor name": {"Product Name": 'CAP Automation For Wedge400 Project Openbmc Unit'},
        "processor basic info" : {
            "Core Number"             : 1,
            "Thread Number"           : 770,
            "Processor frequency MHz" : 1284,
            "Revision"                : "06 07"
        }

    }

####################### MINIPACK3 #############################
elif "minipack3_" in devicename.lower():
    workspace = '/tmp'
    workspace_p = '/mnt/data'
    RESET_MESSAGE = 'Starting kernel'
    default_cpu_usb0_ipv6_addr = 'fe80::2'

#### FB_BMC_COMM_TC_005, FB_BMC_COMM_TC_006, FB_BMC_COMM_TC_007 ########
    iob_fpga_version_cmd = 'cat /sys/bus/auxiliary/devices/fbiob_pci.fpga_info_iob.0/fpga_ver'
    SPI_UPDATE_PASS_MSG = r'successfully|Restore environment..'
    COMe_UPDATE_PASS_MSG = r'Upgrade successful'
    BIOS_UPDATE_PASS_MSG = r'Verifying flash...(\s.*)*VERIFIED'
    CPLD_UPDATE_CMD = '/mnt/data/cpld_update.sh'
    IOB_UPDATE_CMD = 'spi_util.sh write spi1 IOB_FPGA'
    COME_CPLD_VERSION_VERIFY = 'jbi -aVERIFY -ddo_real_time_isp=1 -W'

#### FB_BMC_COMM_TC_017, FB_BMC_COMM_TC_18 ####
    disable_write_protection_scm = 'None'
    enable_write_protection_scm = 'None'
    disable_write_protection_fcb = 'i2cset -f -y 15 0x60 0x05 0x03'
    enable_write_protection_fcb = 'i2cset -f -y 15 0x60 0x05 0x0f'
    fcb_eeprom_product_name = 'FCB_EEPROM_DEFAULT'
    fcb_eeprom_test = 'FCB_EEPROM_TEST'
    fcb_eeprom_test_check = 'FCB_EEPROM_TEST_CHECK'
    fcb_eeprom_test2 = 'FCB_EEPROM_TEST2'
    fcb_eeprom_test2_check = 'FCB_EEPROM_TEST2_CHECK'
    fcb_eeprom_path = '/sys/bus/i2c/devices/i2c-6/6-0053/eeprom'
    fcb_bin_name = 'fru_fcb_b_eeprom_from_bmc.bin'

    scm_eeprom_test = 'SCM_EEPROM_TEST'
    scm_eeprom_test_check = 'SCM_EEPROM_TEST_CHECK'
    scm_eeprom_test2 = 'SCM_EEPROM_TEST2'
    scm_eeprom_test2_check = 'SCM_EEPROM_TEST2_CHECK'
    scm_eeprom_product_name = 'SCM_EEPROM_DEFAULT'
    scm_eeprom_path = '/sys/bus/i2c/devices/i2c-3/3-0056/eeprom'
    scm_bin_name = 'fru_scm2_eeprom_from_bmc.bin'

#### FB_BMC_COMM_TC_022 ####
    cmd_read_mac_from_eeprom = 'weutil'
    UTIL_EEPROM_MAP_KEY = {
        'Product Part Number' : 'top_level_product_part_number',
        'Meta PCBA Part Number' : 'facebook_pcba_part_number',
        'Meta PCB Part Number' : 'facebook_pcb_part_number',
        'ODM/JDM PCBA Part Number' : 'odm_pcba_part_number',
        'ODM/JDM PCBA Serial Number' : 'odm_pcba_serial_number',
        'Local MAC' : 'local_mac_address',
        'Extended MAC Base': 'extended_mac_address_base',
        'Location on Fabric' : 'eeprom_location_on_fabric'
    }

#### FB_BMC_COMM_TC_026 ####
    board_type         = 'MONTBLANC'

#### FB_BMC_COMM_TC_030 ####
    power_on_val = '0x0f'
    power_off_val = '0x0d'
    mcb_cpld_bus = '12'
    mcb_cpld_addr = '0x60'
    come_pwr_ctrl_reg = '0x14'

#### FB_BMC_MP3_TC_032 ####
    has_pem = False
    cit_tool = 'tests/montblanc/*'
    CIT_PASS = r'OK.*'
    cit_test_cmd = 'python cit_runner.py --platform montblanc'

####################### MINERVA #############################
elif "minerva_th5" in devicename.lower():
    workspace = '/tmp'
    workspace_p = '/mnt/data'
    RESET_MESSAGE = 'Starting kernel'
    default_cpu_usb0_ipv6_addr = 'fe80::2'

#### FB_BMC_COMM_TC_005, FB_BMC_COMM_TC_006, FB_BMC_COMM_TC_007 ########
    iob_fpga_version_cmd = 'cat /sys/bus/auxiliary/devices/fbiob_pci.fpga_info_iob.0/fpga_ver'
    SPI_UPDATE_PASS_MSG = r'Erase/write done|Verifying flash.*VERIFIED'
    BIOS_UPDATE_PASS_MSG = r'Verifying flash...(\s.*)*VERIFIED'
    COMe_UPDATE_PASS_MSG = r'Upgrade successful'
    CPLD_UPDATE_CMD = '/mnt/data/cpld_update.sh' 
    IOB_UPDATE_CMD = '/mnt/data/iob_update.sh'
    COME_CPLD_VERSION_VERIFY = 'jbi -aVERIFY -ddo_real_time_isp=1 -W'

#### FB_BMC_COMM_TC_017 ########
    disable_write_protection = 'i2cset -f -y 1 0x35 0x42 0x0'
    enable_write_protection = 'i2cset -f -y 1 0x35 0x42 0x1'
    SMB_eeprom_product_name = 'SMB_EEPROM_DEFAULT'
    smb_eeprom_test = 'SMB_EEPROM_TEST'
    smb_eeprom_test_check = 'SMB_EEPROM_TEST_CHECK'
    smb_eeprom_test2 = 'SMB_EEPROM_TEST2'
    smb_eeprom_test2_check = 'SMB_EEPROM_TEST2_CHECK'
    smb_eeprom_path = '/sys/bus/i2c/devices/i2c-3/3-0056/eeprom'
    smb_bin_name = 'fru_smb_eeprom_from_bmc.bin'

#### FB_BMC_COMM_TC_021 ####
    cmd_read_mac_from_eeprom = 'weutil'
    UTIL_EEPROM_MAP_KEY = {
        'Product Part Number' : 'top_level_product_part_number',
        'Meta PCBA Part Number' : 'facebook_pcba_part_number',
        'Meta PCB Part Number' : 'facebook_pcb_part_number',
        'ODM/JDM PCBA Part Number' : 'odm_pcba_part_number',
        'ODM/JDM PCBA Serial Number' : 'odm_pcba_serial_number',
        'Local MAC' : 'local_mac_address',
        'Extended MAC Base': 'extended_mac_address_base',
        'Location on Fabric' : 'eeprom_location_on_fabric'
    }

#### FB_BMC_COMM_TC_025 ####
    board_type         = 'tahan'

#### FB_BMC_COMM_TC_029 ####
    power_on_val = '0x07'
    power_off_val = '0x05'
    smb_cpld_bus = '1'
    smb_cpld_addr = '0x35'
    ome_pwr_ctrl_reg = '0x14'

#### FB_BMC_MP3_TC_031 ####
    has_pem = False
    cit_tool = 'tests/tahan/*'
    CIT_PASS = r'OK.*'
    cit_test_cmd = 'python cit_runner.py --platform tahan'

