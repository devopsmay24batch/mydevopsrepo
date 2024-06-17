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

import os
import DeviceMgr
from SwImage import SwImage
import Const
#from DiagLib import * 

deviceObj = DeviceMgr.getDevice()

# Get the variable from the DeviceInfo.yaml
pc_info = DeviceMgr.getServerInfo('PC')

##### Variable file used for DIAG_OS_test.robot #####
DIAG_TOOL_PATH='/usr/local/cls_diag/bin/'
DIAG_TOOL_PATH_CPU='/usr/local/cls_diag/'
DIAG_TOOL_PATH_BKP='/usr/local/cls_diag/bin/'
BMC_DIAG_PATH='/mnt/data1/BMC_Diag'
BMC_DIAG_TOOL_PATH='/mnt/data1/BMC_Diag/bin/'
BMC_DIAG_CONFIG_PATH='/mnt/data1/BMC_Diag/configs/'
BMC_BLK_MOUNT_PATH='/mnt/data1/'
FW_IMG_PATH='/mnt/data1/'
BLK_DEV_PATH='/dev/mmcblk0'
DIAG_UTIL_TOOL_PATH=FPGA_TOOL_PATH='/usr/local/cls_diag/utility/'
EEPROM_TOOL_PATH='/mnt/data1/BMC_Diag/utility/eeprom/'
CPU_POWER_STRESS_TOOL_PATH='/usr/local/cls_diag/utility/stress/'
LPMODE_STRESS_TOOL_PATH='/usr/local/cls_diag/utility/stress/Lpmode/'
PCIE_STRESS_TOOL_PATH='/usr/local/cls_diag/utility/stress/PCIE_stress/FPGA'
SDK_UTIL_PATH='/usr/local/cls_diag/SDK/'
FW_UTIL_PATH='/usr/bin/'
SPI_UTIL_PATH='/usr/local/bin/'
Utility_PATH = '/mnt/data1/BMC_Diag/utility/'
EEPROM_PATH = '/mnt/data1/BMC_Diag/utility/eeprom'
SCM_EEPROM_PATH = '/mnt/data1/BMC_Diag/utility/SCM_eeprom'
FCM_EEPROM_PATH = '/mnt/data1/BMC_Diag/utility/FCM_eeprom'
SMB_EEPROM_PATH = '/mnt/data1/BMC_Diag/utility/SMB_eeprom'
BMC_STRESS_POWER_CYCLE_PATH = '/mnt/data1/BMC_Diag/utility/stress/Power_Cycle'
BMC_STRESS_EMMC_PATH = '/mnt/data1/BMC_Diag/utility/stress/EMMC_stress'
BMC_STRESS_I2C_PATH = '/mnt/data1/BMC_Diag/utility/stress/I2C_stress'
BMC_STRESS_BIC_PATH = '/mnt/data1/BMC_Diag/utility/stress/BIC_stress'
DOWNLOADABLE_DIR_WEDGE400C = '/home/automation/Auto_Test/automation/FB-Wedge400C/autotest/downloadable'
DOWNLOADABLE_DIR_WEDGE400 = '/home/automation/Auto_Test/automation/FB-Wedge400/autotest/downloadable'
DOWNLOADABLE_DIR_WEDGE400_3A10 = '/home/automation/Auto_Test/automation/FB-Wedge400/autotest/downloadable/3A10'
DOWNLOADABLE_DIR_CLOUDRIPPER = '/home/automation/Auto_Test/automation/FB-Cloudripper/autotest/downloadable'
EEPROM_CFG="eeprom.cfg"
EEPROM_OUT_CFG="eeprom_out.cfg"
EEPROM_OUT_BAK_CFG="eeprom_out_store.cfg"
DEFAULT_SCP_TIME = 1200

#toolName="ipmitool"
ipmi_toolName="ipmitool"
CMD_APP_NETFN='raw 0x06'
openbmc_mode='openbmc'
centos_mode='centos'
default_mode=centos_mode
centos_eth_params = {
    'interface' : 'eth0',
    'usb_interface' : 'usb0'
}
openbmc_eth_params = {
    'interface' : 'eth0',
    'usb_interface' : 'usb0'
}
minipack2_openbmc_eth_params = {
    'interface' : 'eth0',
}
scp_username = pc_info.scpUsername
scp_password = pc_info.scpPassword
scp_ip = pc_info.managementIP
scp_ipv6 = pc_info.managementIPV6

test_pass_pattern='[\n\s]+.+PASS.+\|'

##### TC-1001-MANAGEMENT-ETHER-PORT-MAC-TEST #####
cel_mac_help_array = {
    "bin_tool" : "cel-mac-test",
    "all_option" : "Check if MAC belong to Quanta",
    "help_option" : "Display this help text and exit",
    }
mac_test_keyword='MAC test'

##### TC-1002-CPU-INFORMATION-TEST #####
cel_cpu_help_array = {
    "bin_tool" : "cel-cpu-test",
    "all_option" : "Show the CPU information and check if it is correct",
    "help_option" : "Display this help text and exit",
    }
cpu_test_keyword_true=[
    r'\[Config\]CPU Threads.*?8',
    r'\[Actual\]CPU Threads.*?8',
    r'CPU test.*?PASS'
]
cpu_test_keyword_false=[
    r'\[Config\]CPU Threads.*?8',
    r'\[Actual\]CPU Threads.*?4',
    r'CPU test.*?FAIL'
]

#### FB_DIAG_COM_TS_024-SYSTEM-LOG-CHECK-TEST ####
sys_log_help_array = {
    "bin_tool" : "cel_syslog",
    "help_option" : "help information",
    "l_option" : "Save system log to file",
    "clean_option": "Clean system logs in the system"
}

##### TC-1003-ACCESS-FPGA-TEST, TC_068_IOB_FPGA_Update_without_Hot-plug #####
cel_fpga_help_array = {
    "bin_tool" : "cel-fpga-test",
    "all_option" : "Test all configure options",
    "help_option" : "Display this help text and exit",
    }
option_str = ''
fpga_test_keyword = 'FPGA test'
fpga_scm_query_cmd = "./fpga scm r 0x70"
fpga_smb_query_cmd = "./fpga smb r 0x70"
fpga_scm_set_cmd = "./fpga scm w 0x70 0xab"
fpga_smb_set_cmd = "./fpga smb w 0x70 0xcd"
fpga_scm_init_pattern = ["0x"]
fpga_scm_set_pattern = ["ab"]
fpga_smb_set_pattern = ["cd"]


##### FB_DIAG_COMM_TC_003 USB device scan Test(SMB_Card)
cel_usb_device_scan_help_array = {
    "bin_tool" : "cel-usb-test",
    "help_option" : "show help",
    "list_option" : "list all supported USB information",
    "all_option" : "test CPU"
    }
cel_usb_device_scan_help_pattern = ['Usage\:\s+\.\/(cel-[\w\-]+)\s+options\s+.+',
                        '-h\s+(.+)',
                        '-l\s+(.+)',
                        '-a\s+(.+)',
                        ]
cel_usb_device_scan_help_a = ['USB devices detect']
test_pass_pattern_device_scan = '.*?PASS'
cel_usb_device_scan_help_l = ['devices']

##### FB_DIAG_COMM_TC_058_BIOS_CONFIG_CHECK_TEST #####
cel_bios_config_check_help_dict = {
    'bin_tool' : 'bios_check.sh',
    'golden_file' : 'bios_golden_file.cfg',
    'option_tool' : './SCELNX_64',
}
bios_config_file_list = ['bios_golden_file.cfg', 'SCELNX_64']
cel_bios_check_tool_help_pattern = ['Usage: ./bios_check.sh golden_file.*SCE_tool', 'All difference will be saved in bios_diff.txt']
cel_bios_default_check_pass_pattern = ['Check BIOS Config.*PASS', 'Check BIOS Boot Order.*PASS']
cel_bios_default_check_fail_pattern = ['Check BIOS Config.*PASS', 'Check BIOS Boot Order.*FAIL']
i2c_config_file_list = ['i2c_devices.cfg', 'devices.cfg']
##### TC-1004-DIMM-SPD-TEST #####
cel_mem_help_array = {
    "bin_tool" : "cel-mem-test",
    "all_option" : "Test all configure options",
    "check_option" : "Check memory block in one minute",
    "help_option" : "Display this help text and exit",
    }
mem_check_pattern={"MEM memtester":'MEM\s+memtester.*?PASS'}
mem_a_keyword = 'Memory\s+size\s+check'

##### TC-1005-USB-STORAGE-TEST #####
cel_usb_help_array = {
    "bin_tool" : "cel-usb-test",
    "all_option" : "Test all configure options",
    "info_option" : "Show all usb SSDs smart information",
    "help_option" : "Display this help text and exit",
    }
usb_info_array = {
    "Vendor" : "[a-zA-Z0-9_. ]+",
    "Product" : "[a-zA-Z0-9_. ]+",
    "Revision" : "[a-zA-Z0-9_. ]+",
    "Compliance" : "SPC-4",
    "User Capacity" : ".*?GB",
    "Logical block size" : "\d+ bytes",
    "SMART Health Status" : "OK"
    }
usb_smarttool = "smartctl"
usb_test_keyword='usb test'

##### TC-1006-RTC-TEST #####
cel_RTC_help_array = {
    "bin_tool" : "cel-rtc-test",
    "all_option" : "Test all configure options",
    "help_option" : "Display this help text and exit",
    "read_option" : "Read rtc data",
    "write_option" : "Use the config to test write",
    "data_option" : "Input the date and time ",
    }
rtc_test_keyword='[Rtc,RTC] test'
rtc_test_p1 = 'usage:([\w\W]+)time'
rtc_test_p2 = '\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}'
rtc_test_p3 = '(\d{4})\-(\d{2})\-(\d{2}) (\d{2})\:(\d{2})\:(\d{2})'
rtc_test_cmd = './cel-rtc-test -h'
rtc_test_cmd1 = './cel-rtc-test --help'
rtc_test_cmd2 = './cel-rtc-test -r'
rtc_test_cmd3 = 'hwclock'
rtc_test_cmd4 = './cel-rtc-test --read'
rtc_test_keyword_1 = "usage: ./cel-rtc-test [OPTIONS]||Options are: ||    -r, --read       Read rtc data> ||    -w, --write      Use the config to test write> ||    -D, --data       Input the date and time '20181231 235959'>||    -a, --all        Test all configure options>||    -h, --help       Display this help text and exit ||||Example:         ||    --all                   # test all time roll over.||    -w -D  '20181231 235959'# set date time"
rtc_read_pattern='Current Date info : (\d{4})\-(\d{2})\-(\d{2}) (\d{2})\:(\d{2})\:(\d{2})'
rtc_write_patternList = ["Will use the config data to test set.",
							"Write date successfully.+",
							"Curr date info : .+"]
rtc_write_data_patternList = ["Will use the input data to test set \({0}\)",
								"Write date successfully.+",
								"Curr date info : .+"]

##### TC-1007-PCIE-DEVICES-TEST #####
cel_pcie_help_array = {
    "bin_tool" : "cel-pci-test",
    "all_option" : "Test all devices",
    "help_option" : "Display this help text and exit",
    }
pcie_test_keyword='PCIe test'

##### TC-1008-FW-SW-INFO-TEST #####
cel_version_help_array = {
    "bin_tool" : "cel-version-test",
    "show_option" : "Show FW info.",
    "help_option" : "Display this help text and exit",
    }

catch_etc_redhat_release_pattern = r'CentOS[ \t]+Linux[ \t]+release[ \t]+(?P<version>\d{1,2}\.\d{1,2}\.\d{1,4})'

catch_kernel_version_pattern = r'Kernel[ \t]+Version:[ \t]+(?P<version>[^\s]+)'

catch_os_diag_version_pattern = r'(OS[ \t]+Diag:[ \t]+|VERSION=)(?P<version>[^\s]+)'

#catch_centos_version_pattern = r'(OS[ \t]+Version:[ \t]+|CentOS)(?P<version>[^\s]+)'
catch_centos_version_pattern = r'(OS[ \t]+Version:[ \t]+|CentOS\-)(?P<version>[\d\.]+)'

catch_i210_fw_version_pattern = r'(I210[ \t]+FW[ \t]+Version:[ \t]+|NVM[ \t]+Version:[ \t]+)(?P<version>[^\s]+)'

catch_openbmc_version_pattern = r'(BMC[ \t]+Version:[ \t]+|OpenBMC[ \t]+Release[ \t]+[^\s]+v)(?P<version>[^\s]+)'

catch_scm_version_pattern = r'(SCM[ \t]+CPLD[ \t]+Version:[ \t]+|SCMCPLD:[ \t]+)(?P<version>[^\s]+)'

catch_smb_version_pattern = r'(SMB[ \t]+CPLD[ \t]+Version:[ \t]+|SMB_SYSCPLD:[ \t]+)(?P<version>[^\s]+)'

catch_fpga1_version_pattern = r'(FPGA1[ \t]+Version:[ \t]+|DOMFPGA1:[ \t]+)(?P<version>[^\s]+)'

catch_fpga2_version_pattern = r'(FPGA2[ \t]+Version:[ \t]+|DOMFPGA2:[ \t]+)(?P<version>[^\s]+)'

catch_bios_version_pattern = r'BIOS[ \t]+Version:[ \t]+(?P<version>[^\s]+)'

##### TC-CR-002-OOB-TEST #####
cel_eth_test_array = {
    "bin_tool" : "cel-eth-test",
    "help_option" : "Display this help text and exit",
    "show_option" : "Show ethernet info",
    "all_option" : "Test ethernet",
}
cel_eth_test_h_pattern = [
    #'^Usage:\s+\.\/cel-eth-test\s+options\s+\(-h\|-s\|-a\)',
    r'-h[ \t]+print this help',
    r'-s[ \t]+show ethernet info',
    r'-a[ \t]+auto'
]
cel_eth_test_s_pattern = [
    'eth0',
    'lo'
]

cel_eth_test_a_pattern = [
    'get_eth_info.*?PASS',
    'ping_internal_USB.*?PASS'
]

##### TC-1009-PORT-LED-TEST #####
cel_led_help_array = {
    "bin_tool" : "cel-led-test",
    "read_option" : "Get Port LED information",
    "write_option" : "Set Port LED information",
    "port_option" : "[port id] (0, 1 ~ 48)",
    "color_option" : "[white, cyan, blue, pink, red, orange, yellow, green]",
    "off_option" : "Off the LEDs. (Default is on)",
    "flash_option" : "Flash LED(s).",
    "help_option" : "Display this help text and exit",
    }
#led_read_pattern='\d+\s+\|\s+.+\|.+'
led_read_pattern='\d+\|\s+.+\|\s+.+'

##### TC-1011-TPM-TEST #####
cel_tpm_help_array = {
    "bin_tool" : "cel-tpm-test",
    "all_option" : "Test all configure options",
    "help_option" : "Display this help text and exit",
    }
tpm_test_keyword='TPM'
tpm_list_array = {
#TPM Info:
    "chip_type" : "SLB9635",
    "vendor_id" : "0x15d1",
#-- I2C info --
    "bus_id" : "0",
    "dev_addr" : "0x51",
    "dev_path" : "/dev/tpm0",
    }


##### TC-1013-NVME-SSD-TEST #####
cel_nvme_help_array = {
    "bin_tool" : "cel-nvme-test",
    "all_option" : "Test all configure options",
    "help_option" : "Display this help text and exit",
    "info_option" : "Show all NVMe SSDs smart information",
    }
cel_nvme_i_array = [
        "Model Number:\s+(.*?)$",
        "Serial Number:\s+(.*?)$",
        "Firmware Version:\s+(.*?)$",
        "PCI Vendor/Subsystem ID:\s+(.*?)$",
        "IEEE OUI Identifier:\s+(.*?)$",
        "Controller ID:\s+(.*?)$",
        "Number of Namespaces:\s+(.*?)$",
        "Namespace 1 Size/Capacity:\s+(.*?)$",
        "Namespace 1 Formatted LBA Size:\s+(.*?)$",
        # "Namespace 1 IEEE EUI-64:\s+(.*?)$",
        "Firmware Updates .*:\s+(.*?)$",
        "Optional Admin Commands \(0x0017\):\s+(.*?)$",
        "Optional NVM Commands .*:\s+(.*?)$",
        "Maximum Data Transfer Size:\s+(.*?)$",
        "Warning  Comp. Temp. Threshold:\s+(.*?)$",
        "Critical Comp. Temp. Threshold:\s+(.*?)$",
        "SMART\s+overall-health\s+self-assessment\s+test\s+result:\s+(PASSED)$"
        ]
nvme_smart_log_patterns= ["media_errors\s+:\s+0", "num_err_log_entries\s+:\s+0"]
nvme_test_keyword='nvme test'
nvme_test_a=['nvme\s+test.*?PASS']
nvme_info_patternList = ["SMART overall-health self-assessment test result: PASSED",
                            "No Errors Logged",
                            "done."]

##### TC-1014-OOB-TEST#####
cel_oob_help_array = {
    "bin_tool" : "cel-oob-test",
    "all_option" : "Test all configure options",
    "help_option" : "Display this help text and exit",
    }
oob_test_keyword='OOB test'
ping_ip=pc_info.managementIP
oob_config_file='/usr/local/cls_diag/configs/oob.yaml'

#### TC-1015-CPLD-TEST ####
cel_cpld_help_array = {
    "bin_tool" : "cel-cpld-test",
    "all_option" : "Scan scm",
    "help_option" : "Display this help text and exit",
}
cpld_test_keyword='cpld i2c test\s+| PASS |'

##### TC-1016-CPLD-TEST#####
cpld_verify_tool='fpga'
scm_cpld='scm'
smb_cpld='smb'
scm_set_reg='0x5'
scm_get_reg_list=['0x0','0x1','0x2']
scm_set_value='0f'
smb_set_reg='0x3'
smb_get_reg_list=['0x0','0x1','0x2']
smb_set_value='12'

##### TC-1101-INITIALIZE-TEST#####
diag_initialize_bin='cel-diag-init'

##### TC-1102-BMC-UPDATE-TEST#####
diag_bmc_boot_bin='cel-boot-test'
flashtool='flashcp'
flash_fuji = 'flash-fuji'
flash_fuji_path10 = '/dev/mtd10'
flash_fuji_path11 = '/dev/mtd11'
bmc_upgrade_file=SwImage.getSwImage(SwImage.BMC).newImage
bmc_downgrade_file=SwImage.getSwImage(SwImage.BMC).oldImage
bmc_package_copy_list = [bmc_upgrade_file,bmc_downgrade_file]
bmc_upgrade_ver=SwImage.getSwImage(SwImage.BMC).newVersion
bmc_downgrade_ver=SwImage.getSwImage(SwImage.BMC).oldVersion
bmc_img_path='/mnt/data1/'
flash_device_path='/dev/mtd4'
scp_bmc_filepath = SwImage.getSwImage(SwImage.BMC).hostImageDir
bmc_update_stress_log = "BMC-Update-Stress"

##### TC-1103-BIOS-UPDATE-TEST#####
spiUtil_tool='spi_util.sh'
boot_info_util='boot_info.sh'
bios_upgrade_file=SwImage.getSwImage(SwImage.BIOS).newImage
bios_downgrade_file=SwImage.getSwImage(SwImage.BIOS).oldImage
bios_package_copy_list = [bios_upgrade_file,bios_downgrade_file]
bios_upgrade_ver=SwImage.getSwImage(SwImage.BIOS).newVersion
bios_downgrade_ver=SwImage.getSwImage(SwImage.BIOS).oldVersion
bios_img_path='/mnt/data1/'
diag_cpu_bios_ver_bin='cel-version-test'
scp_bios_filepath=SwImage.getSwImage(SwImage.BIOS).hostImageDir
spiUtil_write_pattern = ['Config SPI1 Done.',
                            'Erase/write done.']
spiUtil_read_pattern = ['Config SPI1 Done.',
                            'Reading flash to bios...',
                            'done.']
bios_ver_pattern='BIOS Version: ([\w\d\_]+)'
fw_util_option='scm --update --bios'
fw_util_tool='fw-util'
fwUtil_update_pattern = ['updated bios: 100 %','Upgrade of scm : bios succeeded']

i2c_set_tool = "i2cset"
i2c_get_tool = "i2cget"
i2c_default_options = "-f -y"
bios_smb_cpld_bus = '12'
bios_smb_cpld_chip_address = '0x3e'
bios_smb_set_reg='0x20'
bios_smb_before_update_value='0x99'
bios_smb_after_update_value='0x00'
bios_update_stress_log = "BIOS-Update-Stress"

cel_fw_sw_version_array = {
    "BRIDGE_VER" : SwImage.getSwImage(SwImage.SCM).newVersion["Bridge-IC Version"],
    "BRIDGE_BOOTLOADER_VER" : SwImage.getSwImage(SwImage.SCM).newVersion["Bridge-IC Bootloader Version"],
    "BIOS_VER" : SwImage.getSwImage(SwImage.BIOS).newVersion,
    "CPLD_VER" : SwImage.getSwImage(SwImage.SCM).newVersion["CPLD Version"],
    "ME_VER" : "3.0.3.45",
    "PVCCIN_VER" : "0x54c8, 0xe9d6",
    "DDRAB_VER" : "0xb41b, 0xe66c",
    "P1V05_VER" : "0x54c8, 0xe9d6",
    }

##### TC-1104-TH3-UPDATE-TEST #####
th3_upgrade_file=SwImage.getSwImage(SwImage.TH3).newImage
th3_downgrade_file='pciefw_2.05.bin'  # The SwImage.getSwImage(SwImage.TH3).oldImage is defined to TH3_PCIE_FW_02_05
th3_upgrade_ver=SwImage.getSwImage(SwImage.TH3).newVersion["PCIe FW loader version"]
th3_downgrade_ver=SwImage.getSwImage(SwImage.TH3).oldVersion["PCIe FW loader version"]
th3_package_copy_list = [th3_upgrade_file,th3_downgrade_file]
scp_th3_filepath=SwImage.getSwImage(SwImage.TH3).hostImageDir
th3_img_path='/mnt/data1/'
sdk_file='auto_load_user.sh'
th3_ver_command='pciephy fw version'
th3_ver_pattern='PCIe FW loader version: ([\.\d]+)'


##### TC-1106-BIC-UPDATE-TEST #####
cpu_uart_log = "mTerm_wedge"
openbmc_uart_log = "terminal_uart"
bic_upgrade_file=SwImage.getSwImage(SwImage.BIC).newImage
bic_downgrade_file=SwImage.getSwImage(SwImage.BIC).oldImage
bic_package_copy_list = [bic_upgrade_file,bic_downgrade_file]
scp_bic_filepath=SwImage.getSwImage(SwImage.BIC).hostImageDir
bic_img_path='/mnt/data1/'
bic_software_test='cel-software-test'
bic_ver_pattern='Bridge-IC Version:\s+(v[\d\.]+)'
bic_upgrade_ver=SwImage.getSwImage(SwImage.BIC).newVersion
bic_downgrade_ver=SwImage.getSwImage(SwImage.BIC).oldVersion
bic_update_pattern = ['updated bic: 100 %', 'Upgrade of scm : bic succeeded']
bic_update_stress_log = "BIC-Update-Stress"


##### TC-1115-BMC-CPU-TEST #####
cel_bmc_cpu_help_array = {
    "bin_tool" : "cel-CPU-test",
    "all_option" : "test CPU",
    "info_option" : "show CPU info",
    "help_option" : "show this help",
    }
bmc_cpu_keyword_pattern = ['get_cpu_info.*?PASS',
                            'get_cpu_status.*?PASS',
                            'check_processor_number.*?PASS',
                            'check_cpu_model.*?PASS']

bmc_cpu_help_pattern = [
                        '-a\s+.*?',
                        '-h\s+.*?',
                        '-i\s+.*?',
                        ]

bmc_cpu_info_pattern = ['processor\s*:\s*(.+)',
                        'model name\s*:\s*(.+)',
                        'BogoMIPS\s*:\s*(.+)',
                        'Features\s*:\s*(.+)',
                        'CPU implementer\s*:\s*(.+)',
                        'CPU architecture\s*:\s*(.+)',
                        'CPU variant\s*:\s*(.+)',
                        'CPU part\s*:\s*(.+)',
                        'CPU revision\s*:\s*(.+)',
                        'Hardware\s*:\s*(.+)',
                        'Revision\s*:\s*(.+)',
                        'Serial\s*:\s*(.+)',
                        ]

##### TC-1116-BMC-FPGA-TEST #####
cel_bmc_fpga_help_array = {
    "bin_tool" : "cel-fpga-test",
    "help_option" : "help information",
    "write_option" : "write to FPGA",
    "read_option" : "read from FPGA",
    "select_option" : "FPGA name(SMB_DOM_FPGA_1|SMB_DOM_FPGA_2)",
    "reg_addr_option" : "FPGA register address",
    "data_option" : "data written to FPGA",
    "version_option" : "show FPGA version",
    "test_option" : "auto test configure items",
}
bmc_fpga_help_pattern = ['Usage\:\s+\.\/(cel-[\w\-]+)\s+options\s+.+',
                        '-h\s+(.+)',
                        '-w\s+(.+)',
                        '-r\s+(.+)',
                        '-c\s+(.+)',
                        '-s\s+(.+)',
                        '-d\s+(.+)',
                        '-v\s+(.+)',
                        '-a\s+(.+)',
                        ]

##### TC-1117-BMC-CPLD-TEST #####
cel_bmc_cpld_help_array = {
    "bin_tool" : "cel-cpld-test",
    }

bmc_cpld_help_pattern = [
    #r'cel-cpld-test[ \t]+-h[ \t]*$',
    #r'Usage:[ \t]+(?:\.\/)?cel-cpld-test[ \t]+options[ \t]+\(-h\|-w\|-r\|-a\|-v\)[ \t]+\[-c[ \t]+CPLD[ \t]+-s[ \t]REG[ ]+-d[ \t]DATA\][ \t]*$',
    r'[ \t]*-h',
    r'[ \t]*-w',
    r'[ \t]*-r',
    r'[ \t]*-c',
    r'[ \t]*-s',
    r'[ \t]*-d',
    r'[ \t]*-v',
    r'[ \t]*-a',
]

bmc_cpld_keyword_pattern = ['check_cpld_(version|scratch)',
                            'check_cpld_scratch',
                            ]

bmc_cpld_version_pattern = ['FCM_CPLD\s*:\s*(.+)',
                        'FCM_CPLD\s*:\s*(.+)',
                        'SCM_CPLD\s*:\s*(.+)',
                        'SMB_CPLD\s*:\s*(.+)',
                        'PWR_CPLD\s*:\s*(.+)',
                        ]

##### TC-1118-BMC-I2C-TEST #####
cel_bmc_i2c_help_array = {
    "bin_tool" : "cel-i2c-test",
    "help_option" : "show help",
    "scan_option" : "scan i2c devices",
    "list_option" : "list all supported I2C devices information",
    "test_option" : "test i2c devices",
    }
bmc_i2c_help_pattern = ['Usage\:\s+\.\/(cel-[\w\-]+)\s+options\s+.+',
                        '-h\s+(.+)',
                        '-s\s+(.+)',
                        '-l\s+(.+)',
                        '-a\s+(.+)',
                        ]
bmc_i2c_keyword_pattern = ['scan_i2c_devices'
                            ]
i2c_scan_pattern=['[\w\d\_\-]+\s+\d{1,2}\s+0x[0-9a-fA-F]{1,2}\s+(\w+)']
i2c_scan_pass_keyword='OK'

cel_bmc_i2c_other_help_array = {
    "bin_tool" : "cel-i2c-other-test",
    "help_option" : "show help",
    "scan_option" : "scan i2c other devices",
    "list_option" : "list all supported I2C devices information",
    "test_option" : "test i2c devices",
    }
bmc_i2c_other_help_pattern = ['-h\s+(.+)',
                        '-s\s+(.+)',
                        '-f\s+(.+)',
                        '-m\s+(.+)',
                        '-b\s+(.+)',
                        '-p\s+(.+)',
                        '-a\s+(.+)',
                        ]
bmc_i2c_other_keyword_pattern = ['scm_i2c_check',
                                 'fcm_i2c_check',
                                 'smb_i2c_check',
                                 'smb_i2c_1_check',
                                 'pim_base_i2c_check',
                                 'pim_mezz_i2c_check',
                                 'smb_clock_check',
                            ]

#### FB-DIAG-COM-TS-033-FRU-EEPROM-UPDATE ####
cel_bmc_scm_auto_eeprom = {
    "bin_tool" : "auto_eeprom",
    "scm_eeprom" : "SCM EEPROM",
    "fb" : "[fb]",
    "magic_word" : "magic_word",
    "format_version" : "format_version i2c devices",
    "product_name" : "product_name",
    "top_level_product_part_number" : "top_level_product_part_number",
    "system_assembly_part_number" : "system_assembly_part_number",
    "facebook_pcba_part_number" : "facebook_pcba_part_number",
    "facebook_pcb_part_number" : "facebook_pcb_part_number",
    "odm_pcba_part_number" : "odm_pcba_part_number",
    "odm_pcba_serial_number" : "odm_pcba_serial_number",
    "product_production_state" : "product_production_state",
    "product_version" : "product_version",
    "product_sub_version" : "product_sub_version",
    "product_serial_number" : "product_serial_number",
    "product_asset_tag" : "product_asset_tag",
    "system_manufacturer" : "system_manufacturer",
    "system_manufacturing_date" : "system_manufacturing_date",
    "pcb_manufacturer" : "pcb_manufacturer",
    "assembled_at" : "assembled_at",
    "local_mac_address" : "local_mac_address",
    "extended_mac_address_base" : "extended_mac_address_base",
    "extended_mac_address_size" : "extended_mac_address_size",
    "eeprom_location_on_fabric" : "eeprom_location_on_fabric",
    }

bmc_scm_auto_eeprom_pattern = [
    r'#([ \t]+)?(\.\/)?auto_eeprom',
    r'SCM EEPROM\s+\.+',
    r'\[fb\]',
    r'magic_word([ \t])+=([ \t])+0x[0-9a-fA-F]+',
    r'format_version([ \t])+=([ \t])+0x[0-9a-fA-F]+',
    r'product_name([ \t])+=([ \t])+.+',
    r'top_level_product_part_number([ \t])+=([ \t])+(NA|\d+)',
    r'system_assembly_part_number([ \t])+=([ \t])+(NA|\d+)',
    r'facebook_pcba_part_number([ \t])+=([ \t])+\d+',
    r'facebook_pcb_part_number([ \t])+=([ \t])+\d+',
    r'odm_pcba_part_number([ \t])+=([ \t])+[a-zA-Z0-9]+',
    r'odm_pcba_serial_number([ \t])+=([ \t])+[a-zA-Z0-9]+',
    r'product_production_state([ \t])+=([ \t])+\d+',
    r'product_version([ \t])+=([ \t])+\d+',
    r'product_sub_version([ \t])+=([ \t])+\d+',
    r'product_serial_number([ \t])+=([ \t])+[A-Z0-9]+',
    r'product_asset_tag([ \t])+=([ \t])+(NA|\d+)',
    r'system_manufacturer([ \t])+=([ \t])+\w+',
    r'system_manufacturing_date([ \t])+=([ \t])+\d+',
    r'pcb_manufacturer([ \t])+=([ \t])+\w+',
    r'assembled_at([ \t])+=([ \t])+\w+',
    r'local_mac_address([ \t])+=([ \t])+[0-9A-Fa-f]{12}',
    r'extended_mac_address_base([ \t])+=([ \t])+[0-9A-Fa-f]{12}',
    r'extended_mac_address_size([ \t])+=([ \t])+\d+',
    r'eeprom_location_on_fabric([ \t])+=([ \t])+[A-Z]+',
]

tpm_all_config_yaml_patterns = [
    r'TPM testall.*?PASS',
    r'TPM get PCRs.*?PASS',
    r'TPM chip type check.*?PASS',
    r'TPM pcr0 check.*?PASS'
]

#fw_util_version = [
       # r'^[ \t]*BMC[ \t]+Version:.*?',
       # r'^[ \t]*Fan[ \t]+Speed[ \t]+.*?',
     #   r'^[ \t]*FCMCPLD[ \t]+' + str(SwImage.getSwImage(SwImage.CPLD).newVersion["fcm"]).replace(".", "\."),
    #    r'^[ \t]*PWRCPLD[ \t]+' + str(SwImage.getSwImage(SwImage.CPLD).newVersion["pwr"]).replace(".", "\."),
       # r'^[ \t]*SCMCPLD:[ \t]+' + str(SwImage.getSwImage(SwImage.CPLD).newVersion["scm"]).replace(".", "\."),
      #  r'^[ \t]*SMBCPLD:[ \t]+' + str(SwImage.getSwImage(SwImage.CPLD).newVersion["smb"]).replace(".", "\."),
     #   r'^[ \t]*DOMFPGA1:[ \t]+' + str(SwImage.getSwImage(SwImage.FPGA).newVersion["DOMFPGA1"]).replace(".", "\."),
    #    r'^[ \t]*DOMFPGA2:[ \t]+' + str(SwImage.getSwImage(SwImage.FPGA).newVersion["DOMFPGA2"]).replace(".", "\."),
   # ]

cel_bmc_fcm_auto_eeprom = {
    "bin_tool" : "auto_eeprom",
    "fcm_eeprom" : "FCM EEPROM",
    "fb" : "[fb]",
    "magic_word" : "magic_word",
    "format_version" : "format_version i2c devices",
    "product_name" : "product_name",
    "top_level_product_part_number" : "top_level_product_part_number",
    "system_assembly_part_number" : "system_assembly_part_number",
    "facebook_pcba_part_number" : "facebook_pcba_part_number",
    "facebook_pcb_part_number" : "facebook_pcb_part_number",
    "odm_pcba_part_number" : "odm_pcba_part_number",
    "odm_pcba_serial_number" : "odm_pcba_serial_number",
    "product_production_state" : "product_production_state",
    "product_version" : "product_version",
    "product_sub_version" : "product_sub_version",
    "product_serial_number" : "product_serial_number",
    "product_asset_tag" : "product_asset_tag",
    "system_manufacturer" : "system_manufacturer",
    "system_manufacturing_date" : "system_manufacturing_date",
    "pcb_manufacturer" : "pcb_manufacturer",
    "assembled_at" : "assembled_at",
    "local_mac_address" : "local_mac_address",
    "extended_mac_address_base" : "extended_mac_address_base",
    "extended_mac_address_size" : "extended_mac_address_size",
    "eeprom_location_on_fabric" : "eeprom_location_on_fabric",
    }

bmc_fcm_auto_eeprom_pattern = [
    r'#([ \t]+)?(\.\/)?auto_eeprom',
    r'FCM EEPROM\s+\.+',
    r'\[fb\]',
    r'magic_word([ \t])+=([ \t])+0x[0-9a-fA-F]+',
    r'format_version([ \t])+=([ \t])+0x[0-9a-fA-F]+',
    r'product_name([ \t])+=([ \t])+.+',
    r'top_level_product_part_number([ \t])+=([ \t])+(NA|\d+)',
    r'system_assembly_part_number([ \t])+=([ \t])+(NA|\d+)',
    r'facebook_pcba_part_number([ \t])+=([ \t])+\d+',
    r'facebook_pcb_part_number([ \t])+=([ \t])+\d+',
    r'odm_pcba_part_number([ \t])+=([ \t])+[a-zA-Z0-9]+',
    r'odm_pcba_serial_number([ \t])+=([ \t])+[a-zA-Z0-9]+',
    r'product_production_state([ \t])+=([ \t])+\d+',
    r'product_version([ \t])+=([ \t])+\d+',
    r'product_sub_version([ \t])+=([ \t])+\d+',
    r'product_serial_number([ \t])+=([ \t])+[A-Z0-9]+',
    r'product_asset_tag([ \t])+=([ \t])+(NA|\d+)',
    r'system_manufacturer([ \t])+=([ \t])+\w+',
    r'system_manufacturing_date([ \t])+=([ \t])+\d+',
    r'pcb_manufacturer([ \t])+=([ \t])+\w+',
    r'assembled_at([ \t])+=([ \t])+\w+',
    r'local_mac_address([ \t])+=([ \t])+[0-9A-Fa-f]{12}',
    r'extended_mac_address_base([ \t])+=([ \t])+[0-9A-Fa-f]{12}',
    r'extended_mac_address_size([ \t])+=([ \t])+\d+',
    r'eeprom_location_on_fabric([ \t])+=([ \t])+[A-Z]+',
]

cel_bmc_smb_auto_eeprom = {
    "bin_tool" : "auto_eeprom",
    "smb_eeprom" : "SMB EEPROM",
    "fb" : "[fb]",
    "magic_word" : "magic_word",
    "format_version" : "format_version i2c devices",
    "product_name" : "product_name",
    "top_level_product_part_number" : "top_level_product_part_number",
    "system_assembly_part_number" : "system_assembly_part_number",
    "facebook_pcba_part_number" : "facebook_pcba_part_number",
    "facebook_pcb_part_number" : "facebook_pcb_part_number",
    "odm_pcba_part_number" : "odm_pcba_part_number",
    "odm_pcba_serial_number" : "odm_pcba_serial_number",
    "product_production_state" : "product_production_state",
    "product_version" : "product_version",
    "product_sub_version" : "product_sub_version",
    "product_serial_number" : "product_serial_number",
    "product_asset_tag" : "product_asset_tag",
    "system_manufacturer" : "system_manufacturer",
    "system_manufacturing_date" : "system_manufacturing_date",
    "pcb_manufacturer" : "pcb_manufacturer",
    "assembled_at" : "assembled_at",
    "local_mac_address" : "local_mac_address",
    "extended_mac_address_base" : "extended_mac_address_base",
    "extended_mac_address_size" : "extended_mac_address_size",
    "eeprom_location_on_fabric" : "eeprom_location_on_fabric",
    }

minipack2_sw_option_S_show = [
        r'^Diag[ \t]+Version:[ \t]+.*',
        r'^OS[ \t]+Version:[ \t]+.*',
        r'^Kernel[ \t]+Version:[ \t]+.*',
        r'^I210[ \t]+FW[ \t]+Version:[ \t]+.*',
        r'^BIOS[ \t]+Version:[ \t]+.*',

    ]

bmc_smb_auto_eeprom_pattern = [
    r'#([ \t]+)?(\.\/)?auto_eeprom',
    r'SMB EEPROM\s+\.+',
    r'\[fb\]',
    r'magic_word([ \t])+=([ \t])+0x[0-9a-fA-F]+',
    r'format_version([ \t])+=([ \t])+0x[0-9a-fA-F]+',
    r'product_name([ \t])+=([ \t])+.+',
    r'top_level_product_part_number([ \t])+=([ \t])+(NA|\d+)',
    r'system_assembly_part_number([ \t])+=([ \t])+(NA|\d+)',
    r'facebook_pcba_part_number([ \t])+=([ \t])+\d+',
    r'facebook_pcb_part_number([ \t])+=([ \t])+\d+',
    r'odm_pcba_part_number([ \t])+=([ \t])+[a-zA-Z0-9]+',
    r'odm_pcba_serial_number([ \t])+=([ \t])+[a-zA-Z0-9]+',
    r'product_production_state([ \t])+=([ \t])+\d+',
    r'product_version([ \t])+=([ \t])+\d+',
    r'product_sub_version([ \t])+=([ \t])+\d+',
    r'product_serial_number([ \t])+=([ \t])+[A-Z0-9]+',
    r'product_asset_tag([ \t])+=([ \t])+(NA|\d+)',
    r'system_manufacturer([ \t])+=([ \t])+\w+',
    r'system_manufacturing_date([ \t])+=([ \t])+\d+',
    r'pcb_manufacturer([ \t])+=([ \t])+\w+',
    r'assembled_at([ \t])+=([ \t])+\w+',
    r'local_mac_address([ \t])+=([ \t])+[0-9A-Fa-f]{12}',
    r'extended_mac_address_base([ \t])+=([ \t])+[0-9A-Fa-f]{12}',
    r'extended_mac_address_size([ \t])+=([ \t])+\d+',
    r'eeprom_location_on_fabric([ \t])+=([ \t])+[A-Z]+',
]

cel_bmc_eeprom_tool_d = {
    "bin_tool" : "eeprom_tool",
    "smb_eeprom" : "SMB EEPROM",
    "fb" : "[fb]",
    "magic_word" : "magic_word",
    "format_version" : "format_version i2c devices",
    "product_name" : "product_name",
    "top_level_product_part_number" : "top_level_product_part_number",
    "system_assembly_part_number" : "system_assembly_part_number",
    "facebook_pcba_part_number" : "facebook_pcba_part_number",
    "facebook_pcb_part_number" : "facebook_pcb_part_number",
    "odm_pcba_part_number" : "odm_pcba_part_number",
    "odm_pcba_serial_number" : "odm_pcba_serial_number",
    "product_production_state" : "product_production_state",
    "product_version" : "product_version",
    "product_sub_version" : "product_sub_version",
    "product_serial_number" : "product_serial_number",
    "product_asset_tag" : "product_asset_tag",
    "system_manufacturer" : "system_manufacturer",
    "system_manufacturing_date" : "system_manufacturing_date",
    "pcb_manufacturer" : "pcb_manufacturer",
    "assembled_at" : "assembled_at",
    "local_mac_address" : "local_mac_address",
    "extended_mac_address_base" : "extended_mac_address_base",
    "extended_mac_address_size" : "extended_mac_address_size",
    "eeprom_location_on_fabric" : "eeprom_location_on_fabric",
    }

high_power_sensor_u_pattern = [
    r'GB_TEMP1.*?C',
    r'GB_TEMP2.*?C',
    r'GB_TEMP3.*?C',
    r'GB_TEMP4.*?C',
    r'GB_TEMP5.*?C',
    r'GB_TEMP6.*?C',
    r'GB_TEMP7.*?C',
    r'GB_TEMP8.*?C',
    r'GB_TEMP9.*?C',
    r'GB_TEMP10.*?C',
    r'(get|check)_sensor_util_status.*?PASS'
]
high_power_sensor_s_pattern = [
    r'GB_TEMP1.*?C',
    r'GB_TEMP2.*?C',
    r'GB_TEMP3.*?C',
    r'GB_TEMP4.*?C',
    r'GB_TEMP5.*?C',
    r'GB_TEMP6.*?C',
    r'GB_TEMP7.*?C',
    r'GB_TEMP8.*?C',
    r'GB_TEMP9.*?C',
    r'GB_TEMP10.*?C',
]
high_power_sensor_a_pattern = [
    r'GB_TEMP1.*?C',
    r'GB_TEMP2.*?C',
    r'GB_TEMP3.*?C',
    r'GB_TEMP4.*?C',
    r'GB_TEMP5.*?C',
    r'GB_TEMP6.*?C',
    r'GB_TEMP7.*?C',
    r'GB_TEMP8.*?C',
    r'GB_TEMP9.*?C',
    r'GB_TEMP10.*?C',
    r'(get|check)_sensors?_status.*?PASS',
    r'(get|check)_sensor_util_status.*?PASS'
]
bmc_eeprom_tool_d_pattern = [
    r'eeprom_tool[ \t]+-d',
    r'... EEPROM\s+\.+',
    r'\[fb\]',
    r'magic_word([ \t])+=([ \t])+0x[0-9a-fA-F]+',
    r'format_version([ \t])+=([ \t])+0x[0-9a-fA-F]+',
    r'product_name([ \t])+=([ \t])+.+',
    r'top_level_product_part_number([ \t])+=([ \t])+(NA|\d+)',
    r'system_assembly_part_number([ \t])+=([ \t])+(NA|\d+)',
    r'facebook_pcba_part_number([ \t])+=([ \t])+\d+',
    r'facebook_pcb_part_number([ \t])+=([ \t])+\d+',
    r'odm_pcba_part_number([ \t])+=([ \t])+[a-zA-Z0-9]+',
    r'odm_pcba_serial_number([ \t])+=([ \t])+[a-zA-Z0-9]+',
    r'product_production_state([ \t])+=([ \t])+\d+',
    r'product_version([ \t])+=([ \t])+\d+',
    r'product_sub_version([ \t])+=([ \t])+\d+',
    r'product_serial_number([ \t])+=([ \t])+[A-Z0-9]+',
    r'product_asset_tag([ \t])+=([ \t])+(N.?A|\d+)',
    r'system_manufacturer([ \t])+=([ \t])+\w+',
    r'system_manufacturing_date([ \t])+=([ \t])+\d+',
    r'pcb_manufacturer([ \t])+=([ \t])+\w+',
    r'assembled_at([ \t])+=([ \t])+\w+',
    r'local_mac_address([ \t])+=([ \t])+[0-9A-Fa-f]{12}',
    r'extended_mac_address_base([ \t])+=([ \t])+[0-9A-Fa-f]{12}',
    r'extended_mac_address_size([ \t])+=([ \t])+\d+',
    r'eeprom_location_on_fabric([ \t])+=([ \t])+[A-Z]+',
]

#### FB-DIAG-COM-TS-036-BMC-BIOS-BOOT-TEST ####
bmc_cel_boot_test_h = {
    "bin_tool": "cel-boot-test",
    "usage": "Usage",
    "option_h": "Show this help",
    "option_b": "<bmc|bios>",
    "option_s": "Show boot status",
    "option_r": "Boot from <master|slave>",
    "option_a": "Auto test",
}

bmc_boot_test_h_pattern = [
    r'cel-boot-test[ \t]+-h$',
    r'Usage:[ \t]+\./cel-boot-test[ \t]+options[ \t]+\(-h\|-s\|-a\|\[-b[ \t]+<bmc\|bios>\]\|\[-r[ \t]+<master\|slave>\]\)$',
    r'[ \t]*-h[ \t]+.*?',
    r'[ \t]*-b[ \t]+.*?',
    r'[ \t]*-s[ \t]+.*?',
    r'[ \t]*-r[ \t]+.*?',
    r'[ \t]*-a[ \t]+.*?',
]

cel_boot_test_b_bmc_s = {
    "bin_tool": "cel-boot-test",
    "wdt1": "WDT1 Timeout Count",
    "wdt2": "WDT2 Timeout Count",
    "current_boot": "Current Boot Code Source",
}

boot_test_b_bmc_s_master_pattern = [
    r'WDT1[ \t]+Timeout[ \t]+Count:[ \t]+\d$',
    r'WDT2[ \t]+Timeout[ \t]+Count:[ \t]+\d$',
    r'Current[ \t]+Boot[ \t]+Code[ \t]+Source:[ \t]+Master[ \t]+Flash$',
]

boot_test_b_bmc_s_slave_pattern = [
    r'cel-boot-test[ \t]+-b[ \t]+bmc[ \t]+-s$',
    r'WDT1[ \t]+Timeout[ \t]+Count:[ \t]+\d$',
    r'WDT2[ \t]+Timeout[ \t]+Count:[ \t]+\d$',
    r'Current[ \t]+Boot[ \t]+Code[ \t]+Source:[ \t]+Slave[ \t]+Flash$',
]

boot_info_sh_bios_master_pattern = [
    r'[ \t]*(\./)?boot_info\.sh[ \t]+bios',
    r'master',
]

boot_info_sh_bios_slave_pattern = [
    r'[ \t]*(\./)?boot_info\.sh[ \t]+bios',
    r'slave',
]

cel_boot_test_b_bios_r_slave = [
    #r'uServer[ \t]will[ \t]boot[ \t]from[ \t]slave[ \t]bios[ \t]at[ \t]next[ \t]reboot'
    r'Power[ \t]off[ \t]microserver[ \t]\.\.\.[ \t]Done'
]

cel_boot_test_b_bios_r_master = [
    #r'uServer[ \t]will[ \t]boot[ \t]from[ \t]master[ \t]bios[ \t]at[ \t]next[ \t]reboot'
    r'Power[ \t]off[ \t]microserver[ \t]\.\.\.[ \t]Done'
]

cel_boot_test = {
    "bin_tool": "cel-boot-test",
}

cel_boot_test_b_bmc_r_slave_pattern = [
    r'[ \t]*(\./)?cel-boot-test[ \t]+-b[ \t]+bmc[ \t]+-r[ \t]+slave$',
    r'BMC[ \t]+will[ \t]+switch[ \t]+to[ \t]+slave[ \t]+after[ \t]+\d+[ \t]+seconds...',
]

cel_boot_test_b_bmc_r_master_pattern = [
    r'[ \t]*(\./)?cel-boot-test[ \t]+-b[ \t]+bmc[ \t]+-r[ \t]+master$',
    r'BMC[ \t]+will[ \t]+switch[ \t]+to[ \t]+master[ \t]+after[ \t]+\d+[ \t]+seconds...',
]

cel_boot_test_a_pattern = [
    r'cel-boot-test[ \t]+-a',
    r'check_(bmc|bios)_boot_status_master.*?PASS'
]

cel_boot_test_a_pattern_fail = [
    r'cel-boot-test[ \t]+-a',
    r'check_(bmc|bios)_boot_status_master.*?FAIL'
]

cel_boot_test_a_bios_fail_pattern = [
    r'[ \t]*(\./)?cel-boot-test[ \t]+-a',
    r'^[ \t]*check_bmc_boot_status_master[ \t\n\s]+.*\s*.*PASS',
    r'^[ \t]*check_bios_boot_status_master[ \t\n\s]+.*\s*.*FAIL',
]

cel_boot_test_a_bios_and_bmc_fail_pattern = [
    r'[ \t]*(\./)?cel-boot-test[ \t]+-a',
    r'^[ \t]*check_bmc_boot_status_master[ \t\n\s]+.*\s*.*FAIL',
    r'^[ \t]*check_bios_boot_status_master[ \t\n\s]+.*\s*.*FAIL',
]

#### FB-DIAG-COM-TS-041-FAN-TEST ####
cel_fan_test = {
    "bin_tool": "cel-fan-test",
}

cel_fan_test_h_pattern = [
   # r'^Usage:[ \t]+\./cel-fan-test[ \t]+options[ \t]+\(-h\|-g\|-s\|-e\|-a\|\[-p[ \t]+speed\]\|\[-c[ \t]+fan_type\]\)$',
    r'-h',
    r'-p',
    r'-g',
    r'-s',
    r'-e',
    r'-a',
]

cel_fan_test_g_pattern = [
    r'^[ \t]*Fan[ \t]+1[ \t]+RPMs:[ \t]+\d{1,5},[ \t]+\d{1,5},[ \t]+\(\d{1,3}%\)$',
    r'^[ \t]*Fan[ \t]+2[ \t]+RPMs:[ \t]+\d{1,5},[ \t]+\d{1,5},[ \t]+\(\d{1,3}%\)$',
    r'^[ \t]*Fan[ \t]+3[ \t]+RPMs:[ \t]+\d{1,5},[ \t]+\d{1,5},[ \t]+\(\d{1,3}%\)$',
    r'^[ \t]*Fan[ \t]+4[ \t]+RPMs:[ \t]+\d{1,5},[ \t]+\d{1,5},[ \t]+\(\d{1,3}%\)$',
]

cel_fan_test_s_pattern = [
    r'^[ \t]*Fan1[ \t]+Present[ \t]*:[ \t]*OK$',
    r'^[ \t]*Fan1[ \t]+Alive[ \t]*:[ \t]*OK$',
    r'^[ \t]*RFan1[ \t]+Alive[ \t]*:[ \t]*OK$',
    r'^[ \t]*FFan1[ \t]+Alive[ \t]*:[ \t]*OK$',
    r'^[ \t]*Fan2[ \t]+Present[ \t]*:[ \t]*OK$',
    r'^[ \t]*Fan2[ \t]+Alive[ \t]*:[ \t]*OK$',
    r'^[ \t]*RFan2[ \t]+Alive[ \t]*:[ \t]*OK$',
    r'^[ \t]*FFan2[ \t]+Alive[ \t]*:[ \t]*OK$',
    r'^[ \t]*Fan3[ \t]+Present[ \t]*:[ \t]*OK$',
    r'^[ \t]*Fan3[ \t]+Alive[ \t]*:[ \t]*OK$',
    r'^[ \t]*RFan3[ \t]+Alive[ \t]*:[ \t]*OK$',
    r'^[ \t]*FFan3[ \t]+Alive[ \t]*:[ \t]*OK$',
    r'^[ \t]*Fan4[ \t]+Present[ \t]*:[ \t]*OK$',
    r'^[ \t]*Fan4[ \t]+Alive[ \t]*:[ \t]*OK$',
    r'^[ \t]*RFan4[ \t]+Alive[ \t]*:[ \t]*OK$',
    r'^[ \t]*FFan4[ \t]+Alive[ \t]*:[ \t]*OK$',
]

cal_fan_test_p_10_pattern = [
    r'cel-fan-test[ \t]+-p[ \t]*\d{1,3}$',
    # The error is acceptance +/- 3% and the number does not have a decimal digit,
    # it is approximately 9 - 11 shows here.
    r'^Successfully[ \t]+set[ \t]+fan[ \t]+1[ \t]+speed[ \t]+to[ \t]+(9|1[01])%$',
    r'^Successfully[ \t]+set[ \t]+fan[ \t]+2[ \t]+speed[ \t]+to[ \t]+(9|1[01])%$',
    r'^Successfully[ \t]+set[ \t]+fan[ \t]+3[ \t]+speed[ \t]+to[ \t]+(9|1[01])%$',
    r'^Successfully[ \t]+set[ \t]+fan[ \t]+4[ \t]+speed[ \t]+to[ \t]+(9|1[01])%$',
]

cel_fan_test_g_p_10_pattern = [
    r'cel-fan-test[ \t]+-g$',
    # The error is acceptance +/- 3% and the number does not have a decimal digit,
    # it is approximately 9 - 11 shows here.
    r'^[ \t]*Fan[ \t]+1[ \t]+RPMs:[ \t]+\d{1,5},[ \t]+\d{1,5},[ \t]+\((9|10|11)%\)$',
    r'^[ \t]*Fan[ \t]+2[ \t]+RPMs:[ \t]+\d{1,5},[ \t]+\d{1,5},[ \t]+\((9|10|11)%\)$',
    r'^[ \t]*Fan[ \t]+3[ \t]+RPMs:[ \t]+\d{1,5},[ \t]+\d{1,5},[ \t]+\((9|10|11)%\)$',
    r'^[ \t]*Fan[ \t]+4[ \t]+RPMs:[ \t]+\d{1,5},[ \t]+\d{1,5},[ \t]+\((9|10|11)%\)$',
]

cal_fan_test_p_100_pattern = [
    r'cel-fan-test[ \t]+-p[ \t]*\d{1,3}$',
    # The error is acceptance +/- 3% and the number does not have a decimal digit,
    # it is approximately 97 - 103 shows here.
    r'^Successfully[ \t]+set[ \t]+fan[ \t]+1[ \t]+speed[ \t]+to[ \t]+(9[789]|10[0123])%$',
    r'^Successfully[ \t]+set[ \t]+fan[ \t]+2[ \t]+speed[ \t]+to[ \t]+(9[789]|10[0123])%$',
    r'^Successfully[ \t]+set[ \t]+fan[ \t]+3[ \t]+speed[ \t]+to[ \t]+(9[789]|10[0123])%$',
    r'^Successfully[ \t]+set[ \t]+fan[ \t]+4[ \t]+speed[ \t]+to[ \t]+(9[789]|10[0123])%$',
]

cel_fan_test_g_p_100_pattern = [
    r'cel-fan-test[ \t]+-g$',
    # The error is acceptance +/- 3% and the number does not have a decimal digit,
    # it is approximately 97 - 103 shows here.
    r'^[ \t]*Fan[ \t]+1[ \t]+RPMs:[ \t]+\d{1,5},[ \t]+\d{1,5},[ \t]+\((9[789]|10[0123])%\)$',
    r'^[ \t]*Fan[ \t]+2[ \t]+RPMs:[ \t]+\d{1,5},[ \t]+\d{1,5},[ \t]+\((9[789]|10[0123])%\)$',
    r'^[ \t]*Fan[ \t]+3[ \t]+RPMs:[ \t]+\d{1,5},[ \t]+\d{1,5},[ \t]+\((9[789]|10[0123])%\)$',
    r'^[ \t]*Fan[ \t]+4[ \t]+RPMs:[ \t]+\d{1,5},[ \t]+\d{1,5},[ \t]+\((9[789]|10[0123])%\)$',
]

cal_fan_test_p_50_pattern = [
    r'cel-fan-test[ \t]+-p[ \t]*\d{1,3}$',
    # The error is acceptance +/- 3% and the number does not have a decimal digit,
    # it is approximately 48 - 52 shows here.
    r'^Successfully[ \t]+set[ \t]+fan[ \t]+1[ \t]+speed[ \t]+to[ \t]+(4[89]|5[012])%$',
    r'^Successfully[ \t]+set[ \t]+fan[ \t]+2[ \t]+speed[ \t]+to[ \t]+(4[89]|5[012])%$',
    r'^Successfully[ \t]+set[ \t]+fan[ \t]+3[ \t]+speed[ \t]+to[ \t]+(4[89]|5[012])%$',
    r'^Successfully[ \t]+set[ \t]+fan[ \t]+4[ \t]+speed[ \t]+to[ \t]+(4[89]|5[012])%$',
]

cel_fan_test_g_p_50_pattern = [
    r'cel-fan-test[ \t]+-g$',
    # The error is acceptance +/- 3% and the number does not have a decimal digit,
    # it is approximately 48 - 52 shows here.
    r'^[ \t]*Fan[ \t]+1[ \t]+RPMs:[ \t]+\d{1,5},[ \t]+\d{1,5},[ \t]+\((4[89]|5[012])%\)$',
    r'^[ \t]*Fan[ \t]+2[ \t]+RPMs:[ \t]+\d{1,5},[ \t]+\d{1,5},[ \t]+\((4[89]|5[012])%\)$',
    r'^[ \t]*Fan[ \t]+3[ \t]+RPMs:[ \t]+\d{1,5},[ \t]+\d{1,5},[ \t]+\((4[89]|5[012])%\)$',
    r'^[ \t]*Fan[ \t]+4[ \t]+RPMs:[ \t]+\d{1,5},[ \t]+\d{1,5},[ \t]+\((4[89]|5[012])%\)$',
]

cel_fan_test_a_pattern = [
    r'cel-fan-test[ \t]+-a$',
   # r'[ \t]*Fan[ \t]+1[ \t]+RPMs:[ \t]+\d{1,5},[ \t]+\d{1,5},[ \t]+\(\d{1,3}%\)$',
   # r'^[ \t]*Fan[ \t]+2[ \t]+RPMs:[ \t]+\d{1,5},[ \t]+\d{1,5},[ \t]+\(\d{1,3}%\)$',
   # r'^[ \t]*Fan[ \t]+3[ \t]+RPMs:[ \t]+\d{1,5},[ \t]+\d{1,5},[ \t]+\(\d{1,3}%\)$',
   # r'^[ \t]*Fan[ \t]+4[ \t]+RPMs:[ \t]+\d{1,5},[ \t]+\d{1,5},[ \t]+\(\d{1,3}%\)$',
    r'^[ \t]*(check|get)_fan_speed[ \t]+.+PASS',
   # r'^[ \t]*Fan1[ \t]+Present[ \t]*:[ \t]*OK$',
   # r'^[ \t]*Fan1[ \t]+Alive[ \t]*:[ \t]*OK$',
   # r'^[ \t]*RFan1[ \t]+Alive[ \t]*:[ \t]*OK$',
   # r'^[ \t]*FFan1[ \t]+Alive[ \t]*:[ \t]*OK$',
   # r'^[ \t]*Fan2[ \t]+Present[ \t]*:[ \t]*OK$',
   # r'^[ \t]*Fan2[ \t]+Alive[ \t]*:[ \t]*OK$',
   # r'^[ \t]*RFan2[ \t]+Alive[ \t]*:[ \t]*OK$',
   # r'^[ \t]*FFan2[ \t]+Alive[ \t]*:[ \t]*OK$',
   # r'^[ \t]*Fan3[ \t]+Present[ \t]*:[ \t]*OK$',
   # r'^[ \t]*Fan3[ \t]+Alive[ \t]*:[ \t]*OK$',
   # r'^[ \t]*RFan3[ \t]+Alive[ \t]*:[ \t]*OK$',
   # r'^[ \t]*FFan3[ \t]+Alive[ \t]*:[ \t]*OK$',
   # r'^[ \t]*Fan4[ \t]+Present[ \t]*:[ \t]*OK$',
   # r'^[ \t]*Fan4[ \t]+Alive[ \t]*:[ \t]*OK$',
   # r'^[ \t]*RFan4[ \t]+Alive[ \t]*:[ \t]*OK$',
   # r'^[ \t]*FFan4[ \t]+Alive[ \t]*:[ \t]*OK$',
    r'^[ \t]*(check|get)_fan_status[ \t]+.+PASS',
]

cel_fan_test_c_pattern = [
    r'cel-fan-test[ \t]+-c.*?',
    r'^[ \t]*Fan[ \t]+Speed[ \t]+Verify.+[ \t]+.+PASS',
]

cel_fan_test_e_pattern = [
    r'cel-fan-test[ \t]+-e$',
    r'^Check all FANs enable:[ \t]+OK',
    r'.+PASS'
]

catch_fan1_manufacturer = r'Fan[ \t]+1[\w\W]*System[ \t]+Manufacturer:[ \t]+(?P<maker>\w+)[\w\W]*Fan[ \t]+2'

dmidecode_t_bios = r'Getting[ \t]+SMBIOS[ \t]+data[ \t]+from[ \t]sysfs.*?'

#### FB-DIAG-COM-TS-042-MEMORY-TEST ####
cel_memory_test = {
    "bin_tool": "cel-memory-test",
}

cel_memory_test_h_pattern = [
    r'cel-memory-test[ \t]+-h$',
#    r'^Usage:[ \t]+\./cel-memory-test[ \t]+options[ \t]+\(-h\|-i\|-m\|-a\)$',
    r'^[ \t]*-h[ \t]+.*?',
    r'^[ \t]*-i[ \t]+.*?',
    r'^[ \t]*-m[ \t]+.*?',
    r'^[ \t]*-a[ \t]+.*?',
]

get_mem_i_cmd = "./{} -i".format(cel_memory_test["bin_tool"])
get_meminfo_cmd = "cat /proc/meminfo"
mem_compare_pattern_dict = { "MemTotal":"MemTotal:\s+(\d+)\s+kB",
                             "Bounce":"Bounce:\s+(\d+)\s+kB",
                             "VmallocTotal":"VmallocTotal:\s+(\d+)\s+kB",
                             "Percpu":"Percpu:\s+(\d+)\s+kB",
                             #"CmaTotal":"CmaTotal:\s+(\d+)\s+kB",
                          }

cel_memory_test_i_pattern = [
    r'cel-memory-test[ \t]+-i$',
    r'^[ \t]*MemTotal:[ \t]+\d+[ \t]+.+B$',
    r'^[ \t]*MemFree:[ \t]+\d+[ \t]+.+B$',
    r'^[ \t]*MemAvailable:[ \t]+\d+[ \t]+.+B$',
    r'^[ \t]*Buffers:[ \t]+\d+[ \t]+.+B$',
    r'^[ \t]*Cached:[ \t]+\d+[ \t]+.+B$',
    r'^[ \t]*SwapCached:[ \t]+\d+[ \t]+.+B$',
    r'^[ \t]*Active:[ \t]+\d+[ \t]+.+B$',
    r'^[ \t]*Inactive:[ \t]+\d+[ \t]+.+B$',
    r'^[ \t]*Active\(anon\):[ \t]+\d+[ \t]+.+B$',
    r'^[ \t]*Inactive\(anon\):[ \t]+\d+[ \t]+.+B$',
    r'^[ \t]*Active\(file\):[ \t]+\d+[ \t]+.+B$',
    r'^[ \t]*Inactive\(file\):[ \t]+\d+[ \t]+.+B$',
    r'^[ \t]*Unevictable:[ \t]+\d+[ \t]+.+B$',
    r'^[ \t]*Mlocked:[ \t]+\d+[ \t]+.+B$',
    r'^[ \t]*SwapTotal:[ \t]+\d+[ \t]+.+B$',
    r'^[ \t]*SwapFree:[ \t]+\d+[ \t]+.+B$',
    r'^[ \t]*Dirty:[ \t]+\d+[ \t]+.+B$',
    r'^[ \t]*Writeback:[ \t]+\d+[ \t]+.+B$',
    r'^[ \t]*AnonPages:[ \t]+\d+[ \t]+.+B$',
    r'^[ \t]*Mapped:[ \t]+\d+[ \t]+.+B$',
    r'^[ \t]*Shmem:[ \t]+\d+[ \t]+.+B$',
    r'^[ \t]*KReclaimable:[ \t]+\d+[ \t]+.+B$',
    r'^[ \t]*Slab:[ \t]+\d+[ \t]+.+B$',
    r'^[ \t]*SReclaimable:[ \t]+\d+[ \t]+.+B$',
    r'^[ \t]*SUnreclaim:[ \t]+\d+[ \t]+.+B$',
    r'^[ \t]*KernelStack:[ \t]+\d+[ \t]+.+B$',
    r'^[ \t]*PageTables:[ \t]+\d+[ \t]+.+B$',
    r'^[ \t]*NFS_Unstable:[ \t]+\d+[ \t]+.+B$',
    r'^[ \t]*Bounce:[ \t]+\d+[ \t]+.+B$',
    r'^[ \t]*WritebackTmp:[ \t]+\d+[ \t]+.+B$',
    r'^[ \t]*CommitLimit:[ \t]+\d+[ \t]+.+B$',
    r'^[ \t]*Committed_AS:[ \t]+\d+[ \t]+.+B$',
    r'^[ \t]*VmallocTotal:[ \t]+\d+[ \t]+.+B$',
    r'^[ \t]*VmallocUsed:[ \t]+\d+[ \t]+.+B$',
    r'^[ \t]*VmallocChunk:[ \t]+\d+[ \t]+.+B$',
    r'^[ \t]*Percpu:[ \t]+\d+[ \t]+.+B$',
    #r'^[ \t]*CmaTotal:[ \t]+\d+[ \t]+.+B$',
    #r'^[ \t]*CmaFree:[ \t]+\d+[ \t]+.+B$',
    r'^[ \t]*total[ \t]+used[ \t]+free[ \t]+shared[ \t]+buff/cache[ \t]+available$',
    r'^[ \t]*Mem:[ \t]+\d+[ \t]+\d+[ \t]+\d+[ \t]+\d+[ \t]+\d+[ \t]+\d+$',
]

cel_memory_test_m_pattern = [
    r'cel-memory-test[ \t]+-m$',
    # It is a lot of funny characters begins here, the regular expression has to be more flexible!
    #r'Stuck.+Address.+ok',
    #r'Random.+Value.+ok',
    #r'Compare.+XOR.+ok',
    #r'Compare.+SUB.+ok',
    #r'Compare.+MUL.+ok',
    #r'Compare.+DIV.+ok',
    #r'Compare.+OR.+ok',
    #r'Compare.+AND.+ok',
    #r'Sequential.+Increment.+ok',
    #r'Solid.+Bits.+ok',
    #r'Block.+Sequential.+ok',
    #r'Checkerboard.+ok',
    #r'Bit.+Spread.+ok',
    #r'Bit.+Flip.+ok',
    #r'Walking.+Ones.+ok',
    #r'Walking.+Zeroes.+ok',
    #r'8-bit.+Writes.+ok',
    #r'16-bit.+Writes.+ok',
    r'Done',
]

cel_memory_test_a_pattern = [
    r'cel-memory-test[ \t]+-a$',
    #r'^[ \t]*get_memory_info.+PASS',
    r'PASS',
]

#### FB-DIAG-COM-TS-043-EMMC-TEST ###
cel_emmc_test = {
    "bin_tool": "cel-emmc-test",
}

cel_emmc_test_h_pattern = [
    r'cel-emmc-test[ \t]+-h$',
    r'^Usage:[ \t]+\./cel-emmc-test[ \t]+options.*?',
    r'^[ \t]*-h[ \t]+.*?',
    r'^[ \t]*-i[ \t]+.*?',
    r'^[ \t]*-s[ \t]+.*?',
    r'^[ \t]*-a[ \t]+.*?',
]

cel_emmc_test_i_pattern = [
    r'cel-emmc-test[ \t]+-i$',
    r'^[ \t]*eMMC[ \t]+/dev/mmcblk0[ \t]+CID+[ \t]+Register:',
    r'^[ \t]*eMMC[ \t]+/dev/mmcblk0[ \t]+Device+[ \t]+Summary'

    # Have to define the exactly size!
    #r'^[ \t]*Disk[ \t]+/dev/mmcblk0:[ \t]+[\d,\.]+[ \t]+GiB,[ \t]+\d+[ \t]+bytes,[ \t]+\d+[ \t]+sectors$',
]

cel_emmc_test_s_pattern = [
    r'cel-emmc-test[ \t]+-s$',
    r'^[ \t]*[\d,\.]+[ \t]+(GB|GiB|MB)$',
]

cel_emmc_test_a_pattern = [
    r'cel-emmc-test[ \t]+-a$',
    r'^[ \t]*get_emmc_info[ \t\s]+.+PASS',
   # r'^[ \t]*check_emmc_size[ \t\s]+.+PASS',
    r'^[ \t]*check_emmc_read_write[ \t\s]+.+PASS',
]


cel_emmc_test_a_pattern_wedge = [
    r'cel-emmc-test[ \t]+-a$',
    r'^[ \t]*get_disks_info[ \t\s]+.+PASS',
    r'^[ \t]*get_emmc_info[ \t\s]+.+PASS',
   # r'^[ \t]*check_emmc_size[ \t\s]+.+PASS',
    r'^[ \t]*check_emmc_read_write[ \t\s]+.+PASS',
]

# This regular expression was verified and works on https://regex101.com
# It is not begins used, because of this bug.
# root@bmc-oob:/usr/bin# ./find /mnt/data1/BMC_Diag/bin/ -type f -name "*disk.dump"
# " <= This is a bug!
# root@bmc-oob:/usr/bin#
cel_find_disk_dump_pattern = [
    # Finding an empty console
    r'(?<=dump\")\s*\w+@[\w-]+:[/\w]+#[ \t]*',
]


#### FB-DIAG-COM-TS-044-INTERNAL-UART-TEST ####
check_cpu_os_version = [
    r'.*?(cat.*?VERSION).*?',
    r'.*?VERSION=([0-9.]+).*?',
]

check_the_openbmc_version = [
    r'OpenBMC[ \t]+Release[ \t]+.*?'
]

check_emmc_info_test= [
    r'^Disk[ \t]+.*?',
    r'^Units:[ \t]+.*?',
    r'^Sector[ \t]+size[ \t]+.*?',
    r'^I\\O[ \t]+size[ \t]+.*?'

]

check_the_issue_file = [
    r'# [ \t]*(\./)?cat[ \t]+[\w/]+issue\s+',
    r'^[ \t]*OpenBMC[ \t]+Release[ \t]+\w+-v2\.3$',
]

#### FB-DIAG-COM-TS-045-MDIO-TEST ####
cel_mdio_test = {
    "bin_tool": "cel-mdio-test",
}

cel_mdio_test_h_pattern = [
    r'cel-mdio-test[ \t]+-h$',
    #r'^Usage:[ \t]+\./cel-mdio-test[ \t]+options[ \t]+\(-h\|-a\)$',
    r'^[ \t]*-h[ \t]+.*?',
    r'^[ \t]*-a[ \t]+.*?',
]

cel_mdio_test_a_pattern = [
    r'cel-mdio-test[ \t]+-a$',
    r'^[ \t]*enable_mdio[ \t\s]+.+PASS',
    r'^[ \t]*check_mdio_54616[ \t\s]+.+PASS',
    r'^[ \t]*check_mdio_5387[ \t\s]+.+PASS',
]

#### FB-DIAG-COM-TS-046-HOT-SWAP-CONTROLLER-ACCESS-TEST ####
cel_hotswap_test = {
    "bin_tool": "cel-hotswap-test",
}

cel_hotswap_test_h_pattern = [
    #r'cel-hotswap-test[ \t]+-h$',
    #r'^Usage:[ \t]+\./cel-hotswap-test[ \t]+options[ \t]+\(-h\|-a\)$',
    r'-h',
    r'-a',
]

cel_hotswap_test_a_pattern = [
    r'cel-hotswap-test[ \t]+-a$',
    r'^[ \t]*check_FCM_hotswap_access[ \t\s]+.+PASS',
    r'^[ \t]*check_SCM_hotswap_access[ \t\s]+.+PASS',
]

i2cset_scm_hotswap_pattern = [
    r'^\d+$',
]

i2cset_fcm_hotswap_pattern = [
    r'0x.*',
]

#### FB-DIAG-COM-TS-049-PSU-TEST ####
cel_psu_test = {
    "bin_tool": "cel-psu-test",
}

cel_psu_test_h_pattern = [
    #r'cel-psu-test[ \t]+-h',
    #r'cel-psu-test[ \t]+options[ \t]+.*?',
    r'-h',
    r'-i',
    r'-s',
    r'-a',
]

cel_psu_test_i_pattern = [
    r'cel-psu-test[ \t]+-i',
    r'^[ \t]*PSU[ \t]+Information[ \t]+:[ \t]PSU1',
    r'^[ \t]*FRU[ \t]+Information[ \t]+:[ \t]PSU1',
    r'^[ \t]*PSU[ \t]+Information[ \t]+:[ \t]PSU2',
    r'^[ \t]*FRU[ \t]+Information[ \t]+:[ \t]PSU2',
]

cel_psu_test_i_pattern_dc = [
    r'cel-psu-test[ \t]+-i',
    r'^[ \t]*PSU[ \t]+Information[ \t]+:[ \t]PSU2',
    r'^[ \t]*FRU[ \t]+Information[ \t]+:[ \t]PSU2',
]

cel_psu_test_s_pattern = [
    r'cel-psu-test[ \t]+-s$',
    r'PSU1.*?Present.*?OK$',
    r'PSU1.*?ACOK.*?OK$',
    r'PSU1.*?DCOK.*?OK$',
    r'PSU2.*?Present.*?OK$',
    r'PSU2.*?ACOK.*?OK$',
    r'PSU2.*?DCOK.*?OK$',
]

cel_psu_test_s_pattern_dc = [
    r'cel-psu-test[ \t]+-s$',
    r'PSU2.*?Present.*?OK$',
    r'PSU2.*?ACOK.*?OK$',
    r'PSU2.*?DCOK.*?OK$',
]

cel_psu_test_a_pattern = [
    r'cel-psu-test[ \t]+-a$',
    r'^[ \t]*check_psu_status[ \t\s]+.+PASS',
    r'^[ \t]*get_psu_info[ \t\s]+.+PASS'
]

catch_psu1_info_pattern = [
    r'PSU[ \t]+Information.*PSU1[ \t]+\(Bus:(?P<bus>\d+)[ \t]Addr:(?P<addr>0[xX][0-9a-fA-F]+)',
    r'MFR_ID.*:[ \t]+(?P<mfr_id>\w+)',
    r'MFR_MODEL.*:[ \t]+(?P<mfr_model>\w+)',
    r'MFR_REVISION.*:[ \t]+(?P<mfr_rev>\w+)',
    r'MFR_DATE.*:[ \t]+(?P<mfr_date>\w+)',
    r'MFR_SERIAL.*:[ \t]+(?P<mfr_serial>[a-zA-Z]\w+)',
    r'PRI_FW_VER.*:[ \t]+(?P<pri_version>[\d.]+)',
    r'SEC_FW_VER.*:[ \t]+(?P<sec_fw_ver>[\d.]+)',
    r'STATUS_WORD.*:[ \t]+(?P<status_word>0[xX][0-9a-fA-F]+)',
    r'STATUS_VOUT.*:[ \t]+(?P<vout>0[xX][0-9a-fA-F]+)',
    r'STATUS_IOUT.*:[ \t]+(?P<iout>0[xX][0-9a-fA-F]+)',
    r'STATUS_INPUT.*:[ \t]+(?P<input>0[xX][0-9a-fA-F]+)',
    r'STATUS_TEMP.*:[ \t]+(?P<temp>0[xX][0-9a-fA-F]+)',
    r'STATUS_CML.*:[ \t]+(?P<cml>0[xX][0-9a-fA-F]+)',
    r'STATUS_FAN.*:[ \t]+(?P<fan>0[xX][0-9a-fA-F]+)',
    r'STATUS_STBY_WORD.*:[ \t]+(?P<stby_word>0[xX][0-9a-fA-F]+)',
    r'STATUS_VSTBY.*:[ \t]+(?P<vstby>0[xX][0-9a-fA-F]+)',
    r'STATUS_ISTBY.*:[ \t]+(?P<istby>0[xX][0-9a-fA-F]+)',
    r'OPTN_TIME_TOTAL.*:[ \t]+(?P<optn_time_total>\d+D:\d+H)',      # Don't check for minute and second
    r'OPTN_TIME_PRESENT.*:[ \t]+(?P<optn_time_present>\d+D:\d+H)',  # Don't check for minute and second
]

catch_psu2_info_pattern = [
    r'PSU[ \t]+Information.*PSU2[ \t]+\(Bus:(?P<bus>\d+)[ \t]Addr:(?P<addr>0[xX][0-9a-fA-F]+)',
    r'MFR_ID.*:[ \t]+(?P<mfr_id>\w+)',
    r'MFR_MODEL.*:[ \t]+(?P<mfr_model>\w+)',
    r'MFR_REVISION.*:[ \t]+(?P<mfr_rev>\w+)',
    r'MFR_DATE.*:[ \t]+(?P<mfr_date>\w+)',
    r'MFR_SERIAL.*:[ \t]+(?P<mfr_serial>[a-zA-Z]\w+)',
    r'PRI_FW_VER.*:[ \t]+(?P<pri_version>[\d.]+)',
    r'SEC_FW_VER.*:[ \t]+(?P<sec_fw_ver>[\d.]+)',
    r'STATUS_WORD.*:[ \t]+(?P<status_word>0[xX][0-9a-fA-F]+)',
    r'STATUS_VOUT.*:[ \t]+(?P<vout>0[xX][0-9a-fA-F]+)',
    r'STATUS_IOUT.*:[ \t]+(?P<iout>0[xX][0-9a-fA-F]+)',
    r'STATUS_INPUT.*:[ \t]+(?P<input>0[xX][0-9a-fA-F]+)',
    r'STATUS_TEMP.*:[ \t]+(?P<temp>0[xX][0-9a-fA-F]+)',
    r'STATUS_CML.*:[ \t]+(?P<cml>0[xX][0-9a-fA-F]+)',
    r'STATUS_FAN.*:[ \t]+(?P<fan>0[xX][0-9a-fA-F]+)',
    r'STATUS_STBY_WORD.*:[ \t]+(?P<stby_word>0[xX][0-9a-fA-F]+)',
    r'STATUS_VSTBY.*:[ \t]+(?P<vstby>0[xX][0-9a-fA-F]+)',
    r'STATUS_ISTBY.*:[ \t]+(?P<istby>0[xX][0-9a-fA-F]+)',
    r'OPTN_TIME_TOTAL.*:[ \t]+(?P<optn_time_total>\d+D:\d+H)',      # Don't check for minute and second
    r'OPTN_TIME_PRESENT.*:[ \t]+(?P<optn_time_present>\d+D:\d+H)',  # Don't check for minute and second
]

catch_psu1_fru_info_pattern = [
    r'FRU[ \t]+Information.*PSU1[ \t]+\(Bus:(?P<bus>\d+)[ \t]Addr:(?P<addr>0[xX][0-9a-fA-F]+)',
    r'Product[ \t]+Manufacturer.*:[ \t]+(?P<mfg>\w+)',
    r'Product[ \t]+Name.*:[ \t]+(?P<name>\w+)',
    r'Product[ \t]+Part[ \t]Number.*:[ \t]+(?P<part_name>\w+)',
    r'Product[ \t]+Version.*:[ \t]+(?P<version>\w+)',
    r'Product[ \t]+Serial.*:[ \t]+(?P<serial>\w+)',
    r'Product[ \t]+Asset[ \t]Tag.*:[ \t]+(?P<tag>[\w/]+)',
    r'Product[ \t]+FRU[ \t]ID.*:[ \t]+(?P<id>[\w/]+)',
]

catch_psu2_fru_info_pattern = [
    r'FRU[ \t]+Information.*PSU2[ \t]+\(Bus:(?P<bus>\d+)[ \t]Addr:(?P<addr>0[xX][0-9a-fA-F]+)',
    r'Product[ \t]+Manufacturer.*:[ \t]+(?P<mfg>\w+)',
    r'Product[ \t]+Name.*:[ \t]+(?P<name>\w+)',
    r'Product[ \t]+Part[ \t]Number.*:[ \t]+(?P<part_name>\w+)',
    r'Product[ \t]+Version.*:[ \t]+(?P<version>\w+)',
    r'Product[ \t]+Serial.*:[ \t]+(?P<serial>\w+)',
    r'Product[ \t]+Asset[ \t]Tag.*:[ \t]+(?P<tag>[\w/]+)',
    r'Product[ \t]+FRU[ \t]ID.*:[ \t]+(?P<id>[\w/]+)',
]

catch_psu2_fru_info_pattern_dc = [
    r'FRU[ \t]+Information.*PSU2[ \t]+\(Bus:(?P<bus>\d+)[ \t]Addr:(?P<addr>0[xX][0-9a-fA-F]+)',
    r'System[ \t]+Manufacturer.*:[ \t]+(?P<mfg>\w+)',
    r'Product[ \t]+Name.*:[ \t]+(?P<name>[-\w]+)',
    r'Product[ \t]+Version.*:[ \t]+(?P<version>\w+)',
    r'Product[ \t]+Serial.*:[ \t]+(?P<serial>\w+)',
    #r'Product[ \t]+Asset[ \t]Tag.*:[ \t]+(?P<tag>[\w/]+)',
]
catch_psu_info_pattern = catch_psu1_info_pattern + catch_psu1_fru_info_pattern + catch_psu2_info_pattern + catch_psu2_fru_info_pattern

psu_util_psu1_get_psu_info_pattern = [
    r'psu-util[ \t]+psu1[ \t]+--get_psu_info',
    r'^[ \t]*PSU[ \t]+Information[ \t]+:[ \t]PSU1',
]

psu_util_psu2_get_psu_info_pattern = [
    r'psu-util[ \t]+psu2[ \t]+--get_psu_info',
    r'^[ \t]*PSU[ \t]+Information[ \t]+:[ \t]PSU2',
]
cel_psu_test_a_cmd = "./cel-psu-test -a"
get_psu_info_cmd = ["psu-util psu{} --get_psu_info".format(i) for i in range(1,5)]
get_eeprom_info_cmd = ["psu-util psu{} --get_eeprom_info".format(i) for i in range(1,5)]
get_psu_eeprom_info_cmd = get_psu_info_cmd + get_eeprom_info_cmd
psu_eeprom_exclude_item = ["OPTN_TIME_TOTAL    (0xD8)", "OPTN_TIME_PRESENT  (0xD9)"]
psu_eeprom_remove_pattern = ["\[[0-9\.]+\]\s+"]

#### FB-DIAG-COM-TS-050-SENSOR-TEST ###
cel_sensor_test = {
    "bin_tool": "cel-sensor-test",
}

ipmitool_test = {
    "bin_tool": "ipmitool",
}

ipmitool_mc_info_pattern = [
    r'Device\s+ID\s+:\s+\d+',
    r'Device Revision([ \t])+:([ \t])+\d+',
    r'Firmware Revision([ \t])+:([ \t])+(\d+.\d+)',
    r'IPMI Version([ \t])+:([ \t])+(\d+.\d+)',
    r'Manufacturer ID([ \t])+:([ \t])+\d+',
    r'Manufacturer Name([ \t])+:([ \t])+([\w])+([ \t])+\([\w,\d]+\)',
    r'Product ID([ \t])+:([ \t])+([\d])+([ \t])+\([\w,\d]+\)',
    r'Product Name([ \t])+:([ \t])+([\w])+([ \t])+\([\w,\d]+\)',
    r'Device Available([ \t])+:([ \t])+\w+',
    r'Provides Device SDRs([ \t])+:([ \t])+\w+',
    r'Additional Device Support([ \t])+:',
    r'Sensor Device',
    r'SDR Repository Device',
    r'SEL Device',
    r'FRU Inventory Device',
    r'IPMB Event Receiver',
    r'IPMB Event Generator',
    r'Chassis Device',
    r'Aux Firmware Rev Info([ \t])+:',
    r'0x00',
    r'retcode=0',
]

cel_sensor_test_h_pattern = [
    #r'cel-sensor-test[ \t]+-h$',
    #r'cel-sensor-test[ \t]+options[ \t]+.*?',
    r'-h',
    r'-s',
    r'-u',
    r'-a',

]

cel_sensor_test_s_pattern = [
    r'error',
    r'failed'
]

cel_sensor_test_a_pattern = [
    r'cel-sensor-test[ \t]+-a$',
    r'get_sensor_status[ \t]+.*?PASS',
    r'check_sensor_util_status[ \t]+.*?PASS',
]

cel_sensor_test_u_pattern = [
    r'check_sensor_util_status[ \t]+.*?PASS',
]

### FB-DIAG-COM-TS-052-OCP-DEBUG-CARD ####
cel_ocp_test = {
    "bin_tool": "cel-OCP-test",
}

cel_ocp_test_h_pattern = [
    r'cel-OCP-test[ \t]+-h$',
    r'cel-OCP-test[ \t]+options[ \t]+\(-h\|-s[ \t]+.*?',
    r'^[ \t]*-h[ \t]+[S|s]how[ \t]+this[ \t]+help$',
    r'^[ \t]*-s[ \t]+<come\|bmc>[ \t]+Set[ \t]+OPC[ \t]+UART[ \t]+to[ \t]+COMe[ \t]+or[ \t]+BMC$',
    r'^[ \t]*-g[ \t]+Get[ \t]+OCP[ \t]+UART[ \t]+path[ \t]+to$',
    r'^[ \t]*-a[ \t]+Auto[ \t]+test$',
]

cel_ocp_test_a_come_pattern = [
    r'cel-OCP-test[ \t]+-a[ \t]+come$',
    r'^[ \t]*check_OCP_I2C_path[ \t\s]+.+PASS',
]

cel_ocp_test_s_come_pattern = [
    r'cel-OCP-test[ \t]+-s[ \t]+come$',
    r'^[ \t]*OCP[ \t]+UART[ \t]+connect[ \t]+to[ \t]+:[ \t]+COMe$',
]

cel_ocp_test_g_come_pattern = [
    r'cel-OCP-test[ \t]+-g$',
    r'^[ \t]*OCP[ \t]+UART[ \t]+connect[ \t]+to[ \t]+:[ \t]+COMe$',
]

cel_ocp_test_fdisk_come_pattern = [
    r'fdisk',
    r'^[ \t]*BusyBox[ \t]+v\d\.\d{2}\.\d[ \t]+\(\d{4}-\d{2}-\d{2}[ \t]+\d{2}:\d{2}:\d{2}[ \t]+UTC\)[ \t]+multi-call[ \t]+binary\.?$',
    r'^[ \t]*Usage:[ \t]+fdisk[ \t]+\[-ul\][ \t]+\[-C[ \t]CYLINDERS\][ \t]+\[-H[ \t]+HEADS\][ \t]\[-S[ \t]+SECTORS\][ \t]+\[-b[ \t]+SSZ\][ \t]+DISK$',
]

cel_ocp_test_s_bmc_pattern = [
    r'cel-OCP-test[ \t]+-s[ \t]+bmc$',
    r'^[ \t]*OCP[ \t]+UART[ \t]+connect[ \t]+to[ \t]+:[ \t]+BMC$',
]

cel_ocp_test_g_bmc_pattern = [
    r'cel-OCP-test[ \t]+-g$',
    r'^[ \t]*OCP[ \t]+UART[ \t]+connect[ \t]+to[ \t]+:[ \t]+BMC$',
]

cel_ocp_test_cat_bmc_pattern = [
    r'cat[ \t]+/etc/issue$',
    r'^[ \t]*OpenBMC[ \t]+Release[ \t]+wedge400-v\d\.\d',
]

cel_ocp_test_a_bmc_pattern = [
    r'cel-OCP-test[ \t]+-a[ \t]+bmc$',
    r'^[ \t]*check_OCP_I2C_path[ \t\s]+.+PASS',
]

#### FB-DIAG-COM-TS-053-FIRMWARE-SOFTWARE-TEST ####
#
# All the versions are meet to the release package 10
#
# Name              Version
# BIOS              3A09
# Bridege-IC        1.11
# OpenBMC           3.0
# W400c SDK         1.0.1
# Diag OS           3.0.0
# Diag Script       2.5.0
# CPLD SMB          2.2
# CPLD SCM          4.0
# CPLD FCB          4.1
# CPLD PWR          2.2
# FPGA              0.56

cel_software_test = {
    "bin_tool": "cel-software-test",
}


cel_software_test_v_pattern = [
    #r'#[ \t]*(\./)?cel-software-test[ \t]+-v$',
    r'^[ \t]*DIAG[ \t]+:[ \t]+.*?' + str(SwImage.getSwImage(SwImage.DIAG).newVersion).replace(".", "\."),
    r'^[ \t]*BMC[ \t]+:[ \t]+OpenBMC[ \t]+Release[ \t]+wedge400-.*?',
    r'^[ \t]*SMB_DOM_FPGA_1[ \t]:[ \t]+.*?',
    r'^[ \t]*SMB_DOM_FPGA_2[ \t]:[ \t]+.*?',
    r'^[ \t]*BIOS[ \t]+Version:[ \t]+.*?',
]



cel_software_test_a_pattern = [
    #r'#[ \t]*(\./)?cel-software-test[ \t]+-a',
    r'^[ \t]*get_diag_version[ \t\n\s]*.+PASS',
    r'^[ \t]*(get_BMC_version|check_BMC_version)[ \t\n\s]*.+PASS',
    r'^[ \t]*(get_COMe_version|check_COMe_version)[ \t\n\s]*.+PASS',
]

cat_etc_issue_bmc_pattern = [
    r'cat[ \t]+/etc/issue$',
    r'^[ \t]*OpenBMC[ \t]+Release[ \t]+.*?'
    ]

#### FB-DIAG-COM-TS-054-PLATFORM-TEST ####
cel_platform_test = {
    "bin_tool": "cel-platform-test",
}

cel_platform_test_h_pattern = [
    #r'^Usage:[ \t]+\./cel-platform-test[ \t]+options[ \t]+.*?',
    r'^[ \t]*-h',
    r'^[ \t]*-i',
    r'^[ \t]*-e',
    r'^[ \t]*-a',
]

cel_platform_test_i_pattern = [
    r'cel-platform-test[ \t]+-i$',
    r'^[ \t]*SMB[ \t]+Board[ \t]+Type:[ \t]+.*?',  # Expected to work on both Wedge400, Wedge400C and minipack2
]

cel_platform_test_p_pattern = [
    r'PIM1 Board Version.*?',
    r'PIM2 Board Version.*?',
    r'PIM3 Board Version.*?',
    r'PIM4 Board Version.*?',
    r'PIM5 Board Version.*?',
    r'PIM6 Board Version.*?',
    r'PIM7 Board Version.*?',
    r'PIM8 Board Version.*?',
]

cel_platform_test_p_pattern_dc = [
    r'PIM1 Board Version.*?',
    r'PIM2 Board Version.*?',
    r'PIM7 Board Version.*?',
    r'PIM8 Board Version.*?',
]

cel_platform_test_a_pattern = [
    r'cel-platform-test[ \t]+-a$',
    r'^[ \t]*get_eeprom_fcm[ \t\s]*.+PASS',
    r'^[ \t]*get_eeprom_fan1[ \t\s]*.+PASS',
    r'^[ \t]*get_eeprom_fan2[ \t\s]*.+PASS',
    r'^[ \t]*get_eeprom_fan3[ \t\s]*.+PASS',
    r'^[ \t]*get_eeprom_fan4[ \t\s]*.+PASS',
    r'^[ \t]*get_eeprom_scm[ \t\s]*.+PASS',
    r'^[ \t]*get_eeprom_smb[ \t\s]*.+PASS',
    #r'^[ \t]*get_eeprom_pim[ \t\s]*.+PASS',
    r'^[ \t]*get_platform_info[ \t\s]*.+PASS',
]

cel_platform_test_e_all_pattern = [
    r'cel-platform-test[ \t]+-e[ \t]+all$',
    r'^[ \t]*get_eeprom_fcm[ \t\s]*.+PASS',
    r'^[ \t]*get_eeprom_fan1[ \t\s]*.+PASS',
    r'^[ \t]*get_eeprom_fan2[ \t\s]*.+PASS',
    r'^[ \t]*get_eeprom_fan3[ \t\s]*.+PASS',
    r'^[ \t]*get_eeprom_fan4[ \t\s]*.+PASS',
    r'^[ \t]*get_eeprom_smb[ \t\s]*.+PASS',
    r'^[ \t]*get_eeprom_scm[ \t\s]*.+PASS',
    #r'^[ \t]*get_eeprom_pim[ \t\s]*.+PASS',
]

cel_platform_test_e_fcm_pattern = [
    r'cel-platform-test[ \t]+-e[ \t]+fcm',
    r'Fan[ \t]+FCM.*?eeprom',
    r'Product[ \t]+Name:.*?FCM$',
]

cel_platform_test_e_pattern = [
    r'Product[ \t]+Name:.*?',
    r'Location on Fabric:.*?'
]

cel_platform_test_e_fan1_pattern = [
    r'cel-platform-test[ \t]+-e[ \t]+fan1$',
    r'^[ \t]*Fan[ \t]+1[ \t]+eeprom'
]

cel_platform_test_e_fan2_pattern = [
    r'cel-platform-test[ \t]+-e[ \t]+fan2$',
    r'^[ \t]*Fan[ \t]+2[ \t]+eeprom',
]

cel_platform_test_e_fan3_pattern = [
    r'cel-platform-test[ \t]+-e[ \t]+fan3$',
    r'^[ \t]*Fan[ \t]+3[ \t]+eeprom',
]

cel_platform_test_e_fan4_pattern = [
    r'cel-platform-test[ \t]+-e[ \t]+fan4$',
    r'^[ \t]*Fan[ \t]+4[ \t]+eeprom',
]

cel_platform_test_e_smb_pattern = [
    r'cel-platform-test[ \t]+-e[ \t]+smb$',
    r'Product[ \t]+Name:[ \t]+\S+$',
    r'Location[ \t]+on[ \t]+Fabric:[ \t]+SMB$',
]

cel_platform_test_e_scm_pattern = [
    r'cel-platform-test[ \t]+-e[ \t]+scm$',
    r'Product[ \t]+Name:[ \t]+\S+SCM$',
    r'Location[ \t]+on[ \t]+Fabric:[ \t]+SCM$',
]

cel_platform_test_e_pem_pattern = [
    r'cel-platform-test[ \t]+-e[ \t]+pem$',
    r'^[ \t]*Product[ \t]+Name[ \t]+:[ \t]*WEDGE400C?-PEM',
]

#### FB-DIAG-COM-TS-056-DDR-AND-EMMC-STRESS-TEST ####
disable_watchdog_for_ddr_test_pattern = [
    r'[ \t]*(\./)?devmem',  # There is not thing output, this is a dummy!
]

rm_ddr_log_pattern = [
    r'[ \t]*(\./)?rm',  # There is not thing output, this is a dummy!
]

ddr_test_sh_pattern = [
    r'Status[: \t]+PASS',
]

#### FB-DIAG-COM-TS-061-SYSTEM-LOG-CHECK-TEST ####
sys_log = {
    "bin_tool": "cel_syslog",
}

sys_log_h_pattern = [
    #r'sys_log[ \t]+-h',
    r'syslog[ \t]+options[ \t]+',
    r'-h[ \t]+',
    r'-l[ \t]+',
    r'-c[ \t]+',
]

sys_log_l_pattern = [
    r'syslog[ \t]+',
    r'^[ \t]*.+PASS',
]



#### FB-DIAG-COM-TS-040-I2C-DEVICE-TEST ####
cel_i2c_test_l_pattern = [
    r'#[ \t]*(\./)?cel-i2c-test[ \t]+-l',
    r'^[ \t]*BSM_EEPROM[ \t]+20[ \t]+0x56[ \t]*$',
    r'^[ \t]*COMe_BIC[ \t]+0[ \t]+0x20[ \t]*$',
    r'^[ \t]*DOM_FPGA_1[ \t]+13[ \t]+0x60[ \t]*$',
    r'^[ \t]*DOM_FPGA_2[ \t]+5[ \t]+0x60[ \t]*$',
    r'^[ \t]*FCM_CPLD[ \t]+30[ \t]+0x3(e|E)[ \t]*$',
    r'^[ \t]*FCM_EEPROM[ \t]+31[ \t]+0x51[ \t]*$',
    r'^[ \t]*FCM_Fan_tray_1[ \t]+34[ \t]+0x52[ \t]*$',
    r'^[ \t]*FCM_Fan_tray_2[ \t]+35[ \t]+0x52[ \t]*$',
    r'^[ \t]*FCM_Fan_tray_3[ \t]+36[ \t]+0x52[ \t]*$',
    r'^[ \t]*FCM_Fan_tray_4[ \t]+37[ \t]+0x52[ \t]*$',
    r'^[ \t]*FCM_Hot_Swap[ \t]+33[ \t]+0x10[ \t]*$',
    r'^[ \t]*FCM_LM75_1[ \t]+32[ \t]+0x48[ \t]*$',
    r'^[ \t]*FCM_LM75_2[ \t]+32[ \t]+0x49[ \t]*$',
    r'^[ \t]*GB_Clock[ \t]+9[ \t]+0x74[ \t]*$',
    r'^[ \t]*PCA9555_Io_Expander[ \t]+4[ \t]+0x27[ \t]*$',
    r'^[ \t]*Power_DC-DC_core_base[ \t]+1[ \t]+0x28[ \t]*$',
    r'^[ \t]*Power_DC-DC_core_pmbus[ \t]+1[ \t]+0x40[ \t]*$',
    r'^[ \t]*Power_Hbm[ \t]+1[ \t]+0x0(e|E)[ \t]*$',
    r'^[ \t]*Power_Left_base[ \t]+1[ \t]+0x35[ \t]*$',
    r'^[ \t]*Power_Left_pmbus[ \t]+1[ \t]+0x4(d|D)[ \t]*$',
    r'^[ \t]*Power_Right_base[ \t]+1[ \t]+0x2(f|F)[ \t]*$',
    r'^[ \t]*Power_Right_pmbus[ \t]+1[ \t]+0x47[ \t]*$',
    r'^[ \t]*Power_Sequence[ \t]+1[ \t]+0x3(a|A)[ \t]*$',
    r'^[ \t]*PSU_1[ \t]+22[ \t]+0x58[ \t]*$',
    r'^[ \t]*PSU_1_EEPROM[ \t]+22[ \t]+0x50[ \t]*$',
    r'^[ \t]*PSU_2[ \t]+23[ \t]+0x58[ \t]*$',
    r'^[ \t]*PSU_2_EEPROM[ \t]+23[ \t]+0x50[ \t]*$',
    r'^[ \t]*PWR_CPLD[ \t]+29[ \t]+0x3(e|E)[ \t]*$',
    r'^[ \t]*SCM_54616_EEPROM[ \t]+18[ \t]+0x50[ \t]*$',
    r'^[ \t]*SCM_CPLD[ \t]+2[ \t]+0x3(e|E)[ \t]*$',
    r'^[ \t]*SCM_EEPROM[ \t]+17[ \t]+0x52[ \t]*$',
    r'^[ \t]*SCM_Hot_Swap[ \t]+14[ \t]+0x10[ \t]*$',
    r'^[ \t]*SCM_LM75_1[ \t]+15[ \t]+0x4(c|C)[ \t]*$',
    r'^[ \t]*SCM_LM75_2[ \t]+15[ \t]+0x4(d|D)[ \t]*$',
    r'^[ \t]*SCM_PCIE_CLOCK_BUF[ \t]+21[ \t]+0x6(c|C)[ \t]*$',
    r'^[ \t]*SMB_Board_ID[ \t]+6[ \t]+0x21[ \t]*$',
    r'^[ \t]*SMB_CPLD[ \t]+12[ \t]+0x3(e|E)[ \t]*$',
    r'^[ \t]*SMB_EEPROM[ \t]+6[ \t]+0x51[ \t]*$',
    r'^[ \t]*SMB_LEDs[ \t]+6[ \t]+0x20[ \t]*$',
    r'^[ \t]*Switch_Gibraltar[ \t]+3[ \t]+0x2(a|A)[ \t]*$',
    r'^[ \t]*Temp_LM75B_1[ \t]+3[ \t]+0x48[ \t]*$',
    r'^[ \t]*Temp_LM75B_2[ \t]+3[ \t]+0x49[ \t]*$',
    r'^[ \t]*Temp_LM75B_3[ \t]+3[ \t]+0x4(a|A)[ \t]*$',
    r'^[ \t]*Temp_LM75B_4[ \t]+3[ \t]+0x4(b|B)[ \t]*$',
    r'^[ \t]*Temp_TPM421_1[ \t]+3[ \t]+0x4(c|C)[ \t]*$',
    r'^[ \t]*Temp_TPM421_2[ \t]+3[ \t]+0x4(e|E)[ \t]*$',
]

#### FB-DIAG-COM-TS-038-BMC-FPGA-TEST ####
fpga_test_a_pattern = [
    r'#[ \t]*(\./)?cel-fpga-test[ \t]+-a',
    r'^[ \t]*SMB_DOM_FPGA_1[ \t]+:.+OK',
    r'^[ \t]*SMB_DOM_FPGA_2[ \t]+:.+OK',
    r'^[ \t]*check_fpga_scratch[ \t\n\s]+.+PASS',
    r'^[ \t]*show_FPGA_version[ \t\n\s]+.+PASS',
]


#### FB-DIAG-COMM-TS-055-TEST-ALL ####
test_all_sh_pattern = [
    r'#[ \t]*(\./)?test_all\.sh',
    r'^[ \t]*get_cpu_info[ \t]+.*PASS',
    r'^[ \t]*get_cpu_status[ \t]+.*PASS',
    r'^[ \t]*check_processor_number[ \t]+.*PASS',
    r'^[ \t]*check_cpu_model[ \t]+.*PASS',
    r'^[ \t]*check_OCP_I2C_path[ \t]+.*PASS',
    r'^[ \t]*check_TPM_SPI_VID[ \t]+.*PASS',
    r'^[ \t]*check_TPM_SPI_DID[ \t]+.*PASS',
    r'^[ \t]*check_bmc_boot_status_master[ \t]+.*PASS',
    r'^[ \t]*check_bios_boot_status_master[ \t]+.*PASS',
    r'^[ \t]*check_cpld_scratch[ \t]+.*PASS',
    r'^[ \t]*show_CPLD_version[ \t]+.*PASS',
    r'^[ \t]*check_cpld_jtag[ \t]+.*PASS',
    r'^[ \t]*get_emmc_info[ \t]+.*PASS',
    r'^[ \t]*check_emmc_size[ \t]+.*PASS',
    r'^[ \t]*check_emmc_read_write[ \t]+.*PASS',
    r'^[ \t]*get_eth_info[ \t]+.*PASS',
    r'^[ \t]*ping_internal_USB[ \t]+.*PASS',
    r'^[ \t]*get_fan_speed[ \t]+.*PASS',
    r'^[ \t]*check_fan_status[ \t]+.*PASS',
    r'^[ \t]*check_fpga_scratch[ \t]+.*PASS',
    r'^[ \t]*show_FPGA_version[ \t]+.*PASS',
    r'^[ \t]*check_FCM_hotswap_access[ \t]+.*PASS',
    r'^[ \t]*check_SCM_hotswap_access[ \t]+.*PASS',
    r'^[ \t]*scan_i2c_devices[ \t]+.*PASS',
    r'^[ \t]*enable_mdio[ \t]+.*PASS',
    r'^[ \t]*check_mdio_54616[ \t]+.*PASS',
    r'^[ \t]*check_mdio_5389[ \t]+.*PASS',
    r'^[ \t]*get_memory_info[ \t]+.*PASS',
    r'^[ \t]*get_eeprom_fcm[ \t]+.*PASS',
    r'^[ \t]*get_eeprom_fan1[ \t]+.*PASS',
    r'^[ \t]*get_eeprom_fan2[ \t]+.*PASS',
    r'^[ \t]*get_eeprom_fan3[ \t]+.*PASS',
    r'^[ \t]*get_eeprom_fan4[ \t]+.*PASS',
    r'^[ \t]*get_eeprom_scm[ \t]+.*PASS',
    r'^[ \t]*get_eeprom_smb[ \t]+.*PASS',
    r'^[ \t]*get_platform_info[ \t]+.*PASS',
    r'^[ \t]*check_psu_status[ \t]+.*PASS',
    r'^[ \t]*get_psu_info[ \t]+.*PASS',
    r'^[ \t]*check_RACKMON_CPLD_GPIO[ \t]+.*PASS',
    r'^[ \t]*check_RACKMON_CPLD_RF_PF_GPIO[ \t]+.*PASS',
    r'^[ \t]*check_RACKMON_BMC_RF_PF_input[ \t]+.*PASS',
    r'^[ \t]*show_RACKMON_GPIO_input[ \t]+.*PASS',
    r'^[ \t]*get_sensor_status[ \t]+.*PASS',
    r'^[ \t]*check_sensor_util_status[ \t]+.*PASS',
    r'^[ \t]*get_diag_version[ \t]+.*PASS',
    r'^[ \t]*get_BMC_version[ \t]+.*PASS',
    r'^[ \t]*get_COMe_version[ \t]+.*PASS',
]

#### FB-DIAG-COM-TS-019-CPU-POWER-STRESS-TEST ####
cel_cpu_power_stress_test_mcelog_array = {
    "bin_cmd" : "mcelog",
    "daemon_option" : "switch mcelog to daemon mode",
}

cel_cpu_power_stress_array = {
    "bin_tool" : "cpupower_test.sh",
    "cpu_stress_tool" : "stress/CPU_test.sh",
    "log_message_1" : "(CPU intel_pstate: performance): pass",
    "log_message_2" : "(CPU intel_pstate: powersave): pass",
}

#### FB-DIAG-COMM-TC-047-TPM-DEVICE-ACCESS-TEST ####
cel_tpm_test = {
    "bin_tool": "cel-TPM-test",
}

cel_tpm_test_device_c_pattern = [
        r'Get /dev/tpmrm.*chip id: .*'
    ]

cel_tpm_test_h_pattern = [
    #r'#[ \t]*(\./)?cel-TPM-test[ \t]+-h',
    #r'^Usage:[ \t]+\./cel-TPM-test[ \t]+options[ \t]+\(-h\|-i(\|-c)?\|-a\)',
    r'^[ \t]*-h',
    #r'^[ \t]*-i',
    r'^[ \t]*-c',
    r'^[ \t]*-a',
]

#cel_tpm_test_device_c_pattern = [
 #       r'Get /dev/tpmrm.*chip id: .*'
  #  ]

cel_tpm_test_device_i_pattern = [
    r'cel-TPM-test[ \t]+-i',
    r'/dev/tpmrm0 Info:',
    r'TPM2_PT_FAMILY_INDICATOR',
    r'TPM2_PT_REVISION',
    r'TPM2_PT_MANUFACTURER',
    r'TPM2_PT_VENDOR_STRING_1',
    r'TPM2_PT_VENDOR_STRING_2',
    r'TPM2_PT_VENDOR_COMMANDS',
    r'TPM2_PT_MODES'
    #r'TPM_PT_FAMILY_INDICATOR:'
    # Comment due to new version of Diag Version: 1.2.0
    # is printed twice information with only difference TPM_PT_VENDOR_STRING 1
    # and did not found the smart solution to fix this.
    # r'TPM_PT_VENDOR_TPM_TYPE:\s+(.*?)$',
    # r'TPM_PT_FIRMWARE_VERSION_1:\s+(.*?)$',
    # r'TPM_PT_FIRMWARE_VERSION_2:\s+(.*?)$',
    # r'TPM_PT_INPUT_BUFFER:\s+(.*?)$'
]

cel_tpm_test_i_pattern = [
    #r'#[ \t]*(\./)?cel-TPM-test[ \t]+-i',
    #r'^[ \t]*TPM[ \t]+SPI[ \t]+VID:',
    r'TPM2_PT',
]

##### FB-DIAG-COMM-TC-035-BCM5389-EEPROM-UPDATE #####
oob_upgrade_file=SwImage.getSwImage(SwImage.OOB).newImage
oob_package_copy_list = [oob_upgrade_file]
scp_oob_filepath=SwImage.getSwImage(SwImage.OOB).hostImageDir
oob_img_path='/mnt/data1/'

spi_util_sh = {
    "bin_tool": "spi_util.sh",
}

spi_util_write_pattern = [
    #r'#[ \t]*(\./)?spi_util\.sh[ \t]+write[ \t]+spi1[ \t]+BCM5389_EE[ \t]+image\.bin',
    r'^[ \t]*Config[ \t]+SPI1[ \t]+Done\.',
    r'^[ \t]*Writing[ \t]+image\.bin[ \t]+to[ \t]+eeprom\.{3}',
]

spi_util_read_pattern = [
    #r'#[ \t]*(\./)?spi_util\.sh[ \t]+read[ \t]+spi1[ \t]+BCM5389_EE[ \t]+image',
    r'^[ \t]*Config[ \t]+SPI1[ \t]+Done\.',
    r'^[ \t]*Reading[ \t]+eeprom[ \t]+to[ \t]+image\.{3}',
]

#### FB-DIAG-COM-TS-020-DDR-STRESS-TEST ####
cel_DDR_stress_test_array = {
    "bin_tool" : "DDR_test.sh",
    "run_time" : "300",
    "percent" : "5",
    "log_file" : "DDR_Stress.log",
    "Status" : "PASS - please verify no corrected errors",
}

#### FB_DIAG_COM_TC_089_DDR_STRESS_TEST ####
minipack2_cel_DDR_stress_test_array = {
    "bin_tool" : "DDR_test.sh",
    "run_time" : "60",
    "percent" : "5",
    "log_file" : "ddr.log",
    "Status" : "PASS - please verify no corrected errors",
}

#### FB-DIAG-COM-TS-021-SSD-STRESS-TEST ####
cel_ssd_stress_test_array = {
    "bin_tool" : "SSD_test.sh",
    "run_time" : "300",
    "log_file" : "SSD_Stress.log"
}

#### FB-DIAG-COM-TS-023-LPMODE-STRESS-TEST ####
cel_lpmode_stress_test_array = {
    "bin_tool" : "Lpmode_test.sh",
    "option" : "-n",
    "run_time" : "10",
    "log_message" : "Lpmode Check PASSED"
}

#### FB-DIAG-COMM-TC-014-QSFP-TEST ####
cel_qsfp_test = {
    "bin_tool": "cel-qsfp-test",
}

cel_qsfp_test_h_or_help_pattern = [
    #r'(\./)?cel-qsfp-test[ \t]+(-h|--help)',
    r'cel-qsfp-test[ \t]+\[OPTIONS\]',
    r'^[ \t]*Options[ \t]+are:',
    r'^[ \t]*-h,[ \t]+--help[ \t]+Display[ \t]+this[ \t]+help[ \t]+text[ \t]+and[ \t]+exit',
    r'^[ \t]*-p,[ \t]+--port[ \t]+\[port id\] \(0, 1, ...\)',
    r'^[ \t]*0 means all ports',
    r'^[ \t]*1 means port 1',
    r'^[ \t]*-i[ \t]+--info[ \t]+Show QSFP eeprom information',
    r'^[ \t]*-s[ \t]+--status[ \t]+Show QSFP status',
    r'^[ \t]*-r[ \t]+--reset[ \t]+\[on/off\] Set QSFP reset on/off',
    r'^[ \t]*-l,[ \t]+--lpmode[ \t]+\[on/off] Set QSFP lpmode on/off',
    r"^[ \t]*-K,[ \t]+--check[ \t]+Auto check all ports' pin test\.",
    r'^[ \t]*-a,[ \t]+--all[ \t]+Test all configure options\.',
    r'^Example:',
    r'^[ \t]*--port=0 -s[ \t]+# Get the status of all ports',
    r'^[ \t]*--port=1 -s[ \t]+# Get the status of port 1',
    r'^[ \t]*--port=0 --reset=on[ \t]+# Set all ports to reset status on',
    r'^[ \t]*--port=2 --reset=on[ \t]+# Set port #2 to reset status on',
    r'^[ \t]*--port=5 --lpmode=on[ \t]+# Set port #5 to lpmode',
    r'^[ \t]*--check',
    r'^[ \t]*--all',
]

cel_qsfp_test_p_0_s_or_port_0_status_pattern = [
    #r'#[ \t]*(\./)?cel-qsfp-test[ \t]+(-p=0 -s|--port=0 --status)',
    r'^1[ \t\|]+(NO|YES)[ \t\|]+(ON|OFF)[ \t\|]+(ON|OFF)[ \t\|]+(ON|OFF)',
    r'^2[ \t\|]+(NO|YES)[ \t\|]+(ON|OFF)[ \t\|]+(ON|OFF)[ \t\|]+(ON|OFF)',
    r'^3[ \t\|]+(NO|YES)[ \t\|]+(ON|OFF)[ \t\|]+(ON|OFF)[ \t\|]+(ON|OFF)',
    r'^4[ \t\|]+(NO|YES)[ \t\|]+(ON|OFF)[ \t\|]+(ON|OFF)[ \t\|]+(ON|OFF)',
    r'^5[ \t\|]+(NO|YES)[ \t\|]+(ON|OFF)[ \t\|]+(ON|OFF)[ \t\|]+(ON|OFF)',
    r'^6[ \t\|]+(NO|YES)[ \t\|]+(ON|OFF)[ \t\|]+(ON|OFF)[ \t\|]+(ON|OFF)',
    r'^7[ \t\|]+(NO|YES)[ \t\|]+(ON|OFF)[ \t\|]+(ON|OFF)[ \t\|]+(ON|OFF)',
    r'^8[ \t\|]+(NO|YES)[ \t\|]+(ON|OFF)[ \t\|]+(ON|OFF)[ \t\|]+(ON|OFF)',
    r'^9[ \t\|]+(NO|YES)[ \t\|]+(ON|OFF)[ \t\|]+(ON|OFF)[ \t\|]+(ON|OFF)',
    r'^10[ \t\|]+(NO|YES)[ \t\|]+(ON|OFF)[ \t\|]+(ON|OFF)[ \t\|]+(ON|OFF)',
    r'^11[ \t\|]+(NO|YES)[ \t\|]+(ON|OFF)[ \t\|]+(ON|OFF)[ \t\|]+(ON|OFF)',
    r'^12[ \t\|]+(NO|YES)[ \t\|]+(ON|OFF)[ \t\|]+(ON|OFF)[ \t\|]+(ON|OFF)',
    r'^13[ \t\|]+(NO|YES)[ \t\|]+(ON|OFF)[ \t\|]+(ON|OFF)[ \t\|]+(ON|OFF)',
    r'^14[ \t\|]+(NO|YES)[ \t\|]+(ON|OFF)[ \t\|]+(ON|OFF)[ \t\|]+(ON|OFF)',
    r'^15[ \t\|]+(NO|YES)[ \t\|]+(ON|OFF)[ \t\|]+(ON|OFF)[ \t\|]+(ON|OFF)',
    r'^16[ \t\|]+(NO|YES)[ \t\|]+(ON|OFF)[ \t\|]+(ON|OFF)[ \t\|]+(ON|OFF)',
    r'^17[ \t\|]+(NO|YES)[ \t\|]+(ON|OFF)[ \t\|]+(ON|OFF)[ \t\|]+(ON|OFF)',
    r'^18[ \t\|]+(NO|YES)[ \t\|]+(ON|OFF)[ \t\|]+(ON|OFF)[ \t\|]+(ON|OFF)',
    r'^19[ \t\|]+(NO|YES)[ \t\|]+(ON|OFF)[ \t\|]+(ON|OFF)[ \t\|]+(ON|OFF)',
    r'^20[ \t\|]+(NO|YES)[ \t\|]+(ON|OFF)[ \t\|]+(ON|OFF)[ \t\|]+(ON|OFF)',
    r'^21[ \t\|]+(NO|YES)[ \t\|]+(ON|OFF)[ \t\|]+(ON|OFF)[ \t\|]+(ON|OFF)',
    r'^22[ \t\|]+(NO|YES)[ \t\|]+(ON|OFF)[ \t\|]+(ON|OFF)[ \t\|]+(ON|OFF)',
    r'^23[ \t\|]+(NO|YES)[ \t\|]+(ON|OFF)[ \t\|]+(ON|OFF)[ \t\|]+(ON|OFF)',
    r'^24[ \t\|]+(NO|YES)[ \t\|]+(ON|OFF)[ \t\|]+(ON|OFF)[ \t\|]+(ON|OFF)',
    r'^25[ \t\|]+(NO|YES)[ \t\|]+(ON|OFF)[ \t\|]+(ON|OFF)[ \t\|]+(ON|OFF)',
    r'^26[ \t\|]+(NO|YES)[ \t\|]+(ON|OFF)[ \t\|]+(ON|OFF)[ \t\|]+(ON|OFF)',
    r'^27[ \t\|]+(NO|YES)[ \t\|]+(ON|OFF)[ \t\|]+(ON|OFF)[ \t\|]+(ON|OFF)',
    r'^28[ \t\|]+(NO|YES)[ \t\|]+(ON|OFF)[ \t\|]+(ON|OFF)[ \t\|]+(ON|OFF)',
    r'^29[ \t\|]+(NO|YES)[ \t\|]+(ON|OFF)[ \t\|]+(ON|OFF)[ \t\|]+(ON|OFF)',
    r'^30[ \t\|]+(NO|YES)[ \t\|]+(ON|OFF)[ \t\|]+(ON|OFF)[ \t\|]+(ON|OFF)',
    r'^31[ \t\|]+(NO|YES)[ \t\|]+(ON|OFF)[ \t\|]+(ON|OFF)[ \t\|]+(ON|OFF)',
    r'^32[ \t\|]+(NO|YES)[ \t\|]+(ON|OFF)[ \t\|]+(ON|OFF)[ \t\|]+(ON|OFF)',
    r'^33[ \t\|]+(NO|YES)[ \t\|]+(ON|OFF)[ \t\|]+(ON|OFF)[ \t\|]+(ON|OFF)',
    r'^34[ \t\|]+(NO|YES)[ \t\|]+(ON|OFF)[ \t\|]+(ON|OFF)[ \t\|]+(ON|OFF)',
    r'^35[ \t\|]+(NO|YES)[ \t\|]+(ON|OFF)[ \t\|]+(ON|OFF)[ \t\|]+(ON|OFF)',
    r'^36[ \t\|]+(NO|YES)[ \t\|]+(ON|OFF)[ \t\|]+(ON|OFF)[ \t\|]+(ON|OFF)',
    r'^37[ \t\|]+(NO|YES)[ \t\|]+(ON|OFF)[ \t\|]+(ON|OFF)[ \t\|]+(ON|OFF)',
    r'^38[ \t\|]+(NO|YES)[ \t\|]+(ON|OFF)[ \t\|]+(ON|OFF)[ \t\|]+(ON|OFF)',
    r'^39[ \t\|]+(NO|YES)[ \t\|]+(ON|OFF)[ \t\|]+(ON|OFF)[ \t\|]+(ON|OFF)',
    r'^40[ \t\|]+(NO|YES)[ \t\|]+(ON|OFF)[ \t\|]+(ON|OFF)[ \t\|]+(ON|OFF)',
    r'^41[ \t\|]+(NO|YES)[ \t\|]+(ON|OFF)[ \t\|]+(ON|OFF)[ \t\|]+(ON|OFF)',
    r'^42[ \t\|]+(NO|YES)[ \t\|]+(ON|OFF)[ \t\|]+(ON|OFF)[ \t\|]+(ON|OFF)',
    r'^43[ \t\|]+(NO|YES)[ \t\|]+(ON|OFF)[ \t\|]+(ON|OFF)[ \t\|]+(ON|OFF)',
    r'^44[ \t\|]+(NO|YES)[ \t\|]+(ON|OFF)[ \t\|]+(ON|OFF)[ \t\|]+(ON|OFF)',
    r'^45[ \t\|]+(NO|YES)[ \t\|]+(ON|OFF)[ \t\|]+(ON|OFF)[ \t\|]+(ON|OFF)',
    r'^46[ \t\|]+(NO|YES)[ \t\|]+(ON|OFF)[ \t\|]+(ON|OFF)[ \t\|]+(ON|OFF)',
    r'^47[ \t\|]+(NO|YES)[ \t\|]+(ON|OFF)[ \t\|]+(ON|OFF)[ \t\|]+(ON|OFF)',
    r'^48[ \t\|]+(NO|YES)[ \t\|]+(ON|OFF)[ \t\|]+(ON|OFF)[ \t\|]+(ON|OFF)',
]

# cel_qsfp_test_eeprom_pattern = [r'Revision Compliance.*: 4.0']
cel_qsfp_test_eeprom_pattern = [r'Vendor.*: CELESTICA|MAXIN']
cel_qsfp_test_all_pattern = [
    # r'QSFP TYPE test.*PASS',
    r'QSFP PRESENT test.*PASS']
cel_qsfp_test_K_pattern = [
    r"QSFP ModselL test.*PASS",
    r"QSFP VCC test.*PASS",
    r"QSFP RESETL pin test.*PASS",
    r"QSFP INTL pin test.*PASS",
    r"QSFP LPMODE pin test.*PASS",
]

#### FB-DIAG-COMM-TC-000-DIAG-INSTALL-UNINSTALL ####
diag_upgrade_version=SwImage.getSwImage(SwImage.DIAG).newVersion
diag_upgrade_file=SwImage.getSwImage(SwImage.DIAG).newImage
diag_package_copy_list = [diag_upgrade_file]
scp_diag_filepath = SwImage.getSwImage(SwImage.DIAG).hostImageDir
diag_img_path = SwImage.getSwImage(SwImage.DIAG).localImageDir

extract_daig_installer_pattern = [
    r'Wedge400_400C_Diag_' + diag_upgrade_version + r'.zip: OK',
]

cel_diag_list = ['bin', 'common', 'configs', 'utility']

#### FB-DIAG-COM-TS-022-PCIE-STRESS-TEST ####
cel_pcie_stress_test_array = {
    "bin_tool" : "fpga_stress.sh",
    "run_time" : "10",
    "log_message" : "Logged to /var/log/messages",
}

cel_sys_log_check_array = {
    "bin_tool" : "cel_syslog",
    "log_path" : "log/syslog"
}

##### FB-DIAG-COM-TS-011-BIC-TEST #####
cel_version_test = {
    "bin_tool": "cel-version-test",
}

cel_version_S = [
    #r'.*cel-version-test.*',
    r'^Diag[ \t]+Version:[ \t]+' + SwImage.getSwImage(SwImage.DIAG).newVersion + r'$',
]


cel_diag_version = [
    r'.*cel-version-test.*',
    r'^Diag[ \t]+Version:.*',
]


cel_pem_tools = {
    "bin_tool" : "cel-pem-test",
}

verify_pem_tool_option_h_pattern = [
    r'cel-pem-test[ \t]+-h',
   # r'^Usage:[ \t]+\./cel-pem-test[ \t]+options[ \t]+\(-h\|-w\|-r\|-i\|-s\|-a\)[ \t]\[-o[ \t]REG[ \t]-d[ \t]DATA\]',
    r'^[ \t]*-h',
    r'^[ \t]*-w',
    r'^[ \t]*-r',
    r'^[ \t]*-d',
    r'^[ \t]*-o',
    r'^[ \t]*-i',
    r'^[ \t]*-s',
    r'^[ \t]*-a',
]

verify_pem_tool_option_i_pattern = [
    r'cel-pem-test[ \t]+-i',
    r'^[ \t]*PEM[ \t]+Information[ \t]+:[ \t]PEM\w+[ \t]\(Bus:\w+[ \t]Addr:0x\w+\)',
]

verify_pem_tool_option_s_pattern = [
    r'cel-pem-test[ \t]+-s',
    r'^[ \t]*PEM\w[ \t]+Present[ \t]+:[ \t]+OK',
    r'^[ \t]*PEM\w[ \t]+ACOK[ \t]+:[ \t]+OK',
    r'^[ \t]*PEM\w[ \t]+PWROK[ \t]+:[ \t]+OK',
]

verify_pem_tool_option_a_pattern = [
    r'cel-pem-test[ \t]+-a',
    r'^check_pem_status[ \t]+.*PASS',
    r'^check_pem_hotswap_access[ \t]+.*PASS',
    r'^get_pem_info[ \t]+.*PASS',
]

verify_pem_tool_option_main_information_pattern = [
    r'cel-pem-test[ \t]+-r[ \t]+-o[ \t]+0x4c',
    r'^0x\w+',
]

modify_pem_tool_option_main_information_pattern = [
    r'cel-pem-test[ \t]+-r[ \t]+-o[ \t]+0x4c',
    r'^0x55',
]

cel_bmc_version_str = "-dirty"

##### FB-DIAG-COM-TC-084-PCIE-SWITCH-FIRMWARE-UPDATE #####
pcie_update_cmd_str = 'spi_util.sh write spi1 PCIE_SW'
pcie_switch_image='MINIPACK2SMB_B036_PM40028B_v1_image.data'
pcie_pass_pattern_list=['Reading old flash chip contents', 'Erase/write', 'Verifying flash']
BMC_PCIE_SWITCH_PATH='/mnt/data1/BMC_Diag/firmware/PCIe_Switch'


ce_hotswap_test_h = "./cel-hotswap-test -h "
ce_hotswap_test_a = "./cel-hotswap-test -a "
ce_hotswap_h_pattern = {"Usage: ./cel-hotswap-test options (-h|-a)":"Usage:\s+./cel-hotswap-test\s+options\s+\(-h\|-a\)",
                        "-h show this help":"-h\s+show\s+this\s+help", "-a test":"-a\s+test"}
ce_hotswap_a_pattern = {"check_FCM_hotswap_access":"check_FCM_hotswap_access.*?PASS.*?check_SCM",
                        "check_SCM_hotswap_access":"check_SCM_hotswap_access.*?PASS" }
fail_message = {"fail":"fail", "error":"error"}

##### FB-DIAG-COM-TC-083-OOB-SWITCH-FIRMWARE-UPDATE ######
oob_update_cmd_str = 'spi_util.sh write spi2 BCM5387_EE'
oob_switch_image = 'bcm5387_Minipack2_04281212'
oob_pass_pattern_list = ['[Setup] BCM5387_EE', 'Config SPI2 Done', 'Writing bcm5387_Minipack2_04281212']
oob_image_read_cmd = ' spi_util.sh read spi2 BCM5387_EE'
image_read_path = '/tmp/BCM5387'
oob_read_image_pass_pattern=['[Setup] BCM5387_EE', 'Config SPI2 Done', 'Reading BCM5387_EE']
oob_switch_image_path = '/mnt/data1/BMC_Diag/firmware/OOB'

##### FB_DIAG_COM_TC_092_FPGA_UPGRADE_STRESS_TEST #####
FPGA_upgrade_stress_cmd = "./FPGA_Update_test.sh -n 2"
FPGA_upgrade_stress_pattern = {"FPGA Version Check PASSED":"FPGA Version.*?Check.*?PASSED"}
FPGA_upgrade_stress_path = "/mnt/data1/BMC_Diag/utility/stress/FPGA_Update/"
verify_log_cmd = 'grep "Version Check" log/log.txt'

##### FB_DIAG_COM_TC_095_BIC_UPGRADE_STRESS_TEST #####
BIC_upgrade_stress_cmd = "./BIC_Update_test.sh -n 1"
BIC_upgrade_stress_pattern = {"Version Check PASSED":"Version.*?Check.*?PASSED"}
BIC_upgrade_stress_path = "/mnt/data1/BMC_Diag/utility/stress/BIC_Update"

#### FB_DIAG_COMM_TC_035_MANAGEMENT_ETHER_PORT_CONNECT_TEST_COME_MODULE ####
remote_ipv4 = pc_info.deviceDict['managementIP']
remote_ipv4_netmask = "24"
remote_ipv6 = pc_info.deviceDict['managementIPV6']
remote_ipv6_netmask = "64"

diag_install_pattern = [
    r'success[ \t]+install[ \t]+BMC_Diag',
]

##### TC_053_FIRMWARE_SOFTWARE_TEST #####
cel_software_test_i_or_v_pattern = [
    #r'cel-software-test[ \t]+-(i|v)$',
    r'^[ \t]*DIAG[ \t]+:[ \t]+.*?' + str(SwImage.getSwImage(SwImage.DIAG).newVersion).replace(".", "\."),
    r'^[ \t]*BMC[ \t]+:[ \t]+OpenBMC[ \n\t]+Release[ \t]+\w+-.*?',
    r'FPGA_1[ \t]+:[ \t]+' + str(SwImage.getSwImage(SwImage.FPGA).newVersion.get("DOMFPGA1", "")).replace(
        ".", "\."),
    r'FPGA_2[ \t]+:[ \t]+' + str(SwImage.getSwImage(SwImage.FPGA).newVersion.get("DOMFPGA2", "")).replace(
        ".", "\."),
    r'FCM_CPLD[ \t]+:[ \t]+' + str(SwImage.getSwImage(SwImage.CPLD).newVersion.get("fcm", "")).replace(".", "\."),
    r'SCM_CPLD[ \t]+:[ \t]+' + str(SwImage.getSwImage(SwImage.CPLD).newVersion.get("scm", "")).replace(".", "\."),
    r'SMB_CPLD[ \t]+:[ \t]+' + str(SwImage.getSwImage(SwImage.CPLD).newVersion.get("smb", "")).replace(".", "\."),
    r'^[ \\t]*(SMB_)?PWR_CPLD[ \t]+:[ \t]+' + str(SwImage.getSwImage(SwImage.CPLD).newVersion.get("pwr", "")).replace(".",
                                                                                                                "\."),
    r'^[ \t]*Bridge-IC[ \t]+Version:[ \n\t]+' + str(
        SwImage.getSwImage(SwImage.SCM).newVersion["Bridge-IC Version"]).replace(".", "\."),
    r'^[ \t]*BIOS[ \t]+Version:[ \n\t]+.*' + str(SwImage.getSwImage(SwImage.BIOS).newVersion).replace(".", "\."),
]
cel_software_test_i_or_v_pattern_dc = [
    #r'cel-software-test[ \t]+-(i|v)$',
    r'^[ \t]*DIAG[ \t]+:[ \t]+.*?' + str(SwImage.getSwImage(SwImage.DIAG).newVersion).replace(".", "\."),
    r'^[ \t]*BMC[ \t]+:[ \t]+OpenBMC[ \n\t]+Release[ \t]+\w+-.*?',
    r'FPGA_1[ \t]+:[ \t]+' + str(SwImage.getSwImage(SwImage.FPGA).newVersion.get("DOMFPGA1", "")).replace(
        ".", "\."),
    r'FPGA_2[ \t]+:[ \t]+' + str(SwImage.getSwImage(SwImage.FPGA).newVersion.get("DOMFPGA2", "")).replace(
        ".", "\."),
    r'FCM_CPLD[ \t]+:[ \t]+' + str(SwImage.getSwImage(SwImage.CPLD).newVersion.get("fcm", "")).replace(".", "\."),
    r'SCM_CPLD[ \t]+:[ \t]+' + str(SwImage.getSwImage(SwImage.CPLD).newVersion.get("scm", "")).replace(".", "\."),
    r'SMB_CPLD[ \t]+:[ \t]+' + str(SwImage.getSwImage(SwImage.CPLD).newVersion.get("smb", "")).replace(".", "\."),
    r'^[ \\t]*(PSB_)?PWR_CPLD[ \t]+:[ \t]+' + str(SwImage.getSwImage(SwImage.CPLD).newVersion.get("pwr", "")).replace(".",
                                                                                                                "\."),
    r'^[ \t]*Bridge-IC[ \t]+Version:[ \n\t]+' + str(
        SwImage.getSwImage(SwImage.SCM).newVersion["Bridge-IC Version"]).replace(".", "\."),
    r'^[ \t]*BIOS[ \t]+Version:[ \n\t]+.*' + str(SwImage.getSwImage(SwImage.BIOS).newVersion).replace(".", "\."),
]
cel_software_test_h_pattern = [
    r'cel-software-test[ \t]+-h$',
    #r'^Usage:[ \t]+\./cel-software-test options[ \t]+\(.*\)$',
    r'^[ \t]*-h',
    r'^[ \t]*-i',
    r'^[ \t]*-v',
    r'^[ \t]*-a',
]
cat_etc_product_version_pattern = [
    # r'cat[ \t]+/etc/product/VERSION$',
    r'^[ \t]*VERSION=' + SwImage.getSwImage(SwImage.DIAG_OS).newVersion,
]

##### TC_008_Firmware/Software_Information_Test #####
cat_etc_redhat_release_pattern = [
    r'CentOS[ \t]+Linux[ \t]+release',
]
cat_proc_version_pattern = [
    r'Linux[ \t]+version[ \t]+(?P<version>\d{1,2}\.\d{1,2}\.\d{1,3})',
]

##### TC-1107-FCM-UPDATE-TEST #####
fcm_upgrade_file = SwImage.getSwImage(SwImage.CPLD).newImage["fcm"]
fcm_downgrade_file = SwImage.getSwImage(SwImage.CPLD).oldImage["fcm"]
fcm_package_copy_list = [fcm_upgrade_file, fcm_downgrade_file]
scp_fcm_filepath = SwImage.getSwImage(SwImage.CPLD).hostImageDir
fcm_img_path = '/mnt/data1/'
fcm_software_test = 'cel-software-test'
fcm_ver_pattern = 'FCM_CPLD\s+:\s+([\d\.]+)'
fcm_update_pattern = ['Upgrade successful.']
fcm_cpld_tool = 'fcmcpld_update.sh'

##### TC-1108-SCM-UPDATE-TEST #####
scm_upgrade_file = SwImage.getSwImage(SwImage.CPLD).newImage["scm"]
scm_downgrade_file = SwImage.getSwImage(SwImage.CPLD).oldImage["scm"]
scm_package_copy_list = [scm_upgrade_file, scm_downgrade_file]
scp_scm_filepath = SwImage.getSwImage(SwImage.CPLD).hostImageDir
scm_img_path = '/mnt/data1/'
scm_software_test = 'cel-software-test'
scm_ver_pattern = 'SCM_CPLD\s+:\s+([\d\.]+)'
scm_update_pattern = ['Upgrade successful.']
scm_cpld_tool = 'scmcpld_update.sh'

##### TC-1109-SYSTEM-UPDATE-TEST #####
smb_upgrade_file = SwImage.getSwImage(SwImage.CPLD).newImage["smb"]
smb_downgrade_file = SwImage.getSwImage(SwImage.CPLD).oldImage["smb"]
smb_package_copy_list = [smb_upgrade_file, smb_downgrade_file]
scp_smb_filepath = SwImage.getSwImage(SwImage.CPLD).hostImageDir
smb_img_path = '/mnt/data1/'
smb_software_test = 'cel-software-test'
smb_ver_pattern = 'SMB_CPLD\s+:\s+([\d\.]+)'
smb_update_pattern = ['Upgrade successful.']
smb_cpld_tool = 'smbcpld_update.sh'

##### TC-1110-POWER-UPDATE-TEST #####
pwr_upgrade_file = SwImage.getSwImage(SwImage.CPLD).newImage["pwr"]
pwr_downgrade_file = SwImage.getSwImage(SwImage.CPLD).oldImage["pwr"]
pwr_package_copy_list = [pwr_upgrade_file, pwr_downgrade_file]
scp_pwr_filepath = SwImage.getSwImage(SwImage.CPLD).hostImageDir
pwr_img_path = '/mnt/data1/'
pwr_software_test = 'cel-software-test'
pwr_ver_pattern = 'PWR_CPLD\s+:\s+([\d\.]+)'
pwr_update_pattern = ['Upgrade successful.']
pwr_cpld_tool = 'pwrcpld_update.sh'

##### TC-1105-FPGA-UPDATE-TEST #####
scp_fpga_filepath = SwImage.getSwImage(SwImage.FPGA).hostImageDir
fpga_img_path = '/mnt/data1/'
fpga_software_test = 'cel-software-test'
fpga1_ver_pattern = 'DOM_FPGA_1\s+:\s+([\d\.]+)'
fpga2_ver_pattern = 'DOM_FPGA_2\s+:\s+([\d\.]+)'
fpga_update_stress_log = 'FPGA-Update-Stress'

version_test_S_or_show_pattern = [
    #r'(\./)?cel-version-test[ \t]+(-S|--show)',
    r'^Diag[ \t]+Version:[ \t]+' + SwImage.getSwImage(SwImage.DIAG).newVersion + r'$',
    r'^OS[ \t]+Diag:[ \t]+' + SwImage.getSwImage(SwImage.DIAG_OS).newVersion + r'$',
    r'^OS[ \t]+Version:[ \t]+' + SwImage.getSwImage(SwImage.OS).newVersion + r'$',
    r'^Kernel[ \t]+Version:[ \t]+' + SwImage.getSwImage(SwImage.KERNEL).newVersion + r'$',
    #r'^BMC[ \t]+Version:[ \t]+' + str(SwImage.getSwImage(SwImage.BMC).newVersion).replace(".", ".0") + r'$',
    r'^BIOS[ \t]+Version:[ \t]+' + SwImage.getSwImage(SwImage.BIOS).newVersion + r'$',
    #r'^BIOS[ \t]+boot:[ \t]+(master|slave)$',
    r'^FPGA1[ \t]+Version:[ \t]+' + SwImage.getSwImage(SwImage.FPGA).newVersion.get("DOMFPGA1", "") + r'$',
    r'^FPGA2[ \t]+Version:[ \t]+' + SwImage.getSwImage(SwImage.FPGA).newVersion.get("DOMFPGA2", "") + r'$',
    r'^SCM[ \t]+CPLD[ \t]+Version:[ \t]+' + SwImage.getSwImage(SwImage.CPLD).newVersion.get("scm", "") + r'$',
    r'^SMB[ \t]+CPLD[ \t]+Version:[ \t]+' + SwImage.getSwImage(SwImage.CPLD).newVersion.get("smb", "") + r'$',
    r'^I210[ \t]+FW[ \t]+Version:[ \t]+' + SwImage.getSwImage(SwImage.I210).newVersion + r'$',
]
##### FB_DIAG_COM_TC_038_BMC_FPGA_TEST #####
fpga_test_v_pattern = [
    r'cel-fpga-test[ \t]+-v',
    r'^[ \t]*SMB_DOM_FPGA_1[ \t]+:[ \t]+' + str(SwImage.getSwImage(SwImage.FPGA).newVersion.get("DOMFPGA1", "")).replace(
        ".", "\.") + r'$',
    r'^[ \t]*SMB_DOM_FPGA_2[ \t]+:[ \t]+' + str(SwImage.getSwImage(SwImage.FPGA).newVersion.get("DOMFPGA2", "")).replace(
        ".", "\.") + r'$',
]
fpga_test_k_pattern = [
    r'cel-fpga-test[ \t]+-k',
    r'^[ \t]*SMB_DOM_FPGA_1[ \t]+:[ \t]+' + str(SwImage.getSwImage(SwImage.FPGA).newVersion.get("DOMFPGA1", "")).replace(
        ".", "\.") + r'[ \t]+OK',
    r'^[ \t]*SMB_DOM_FPGA_2[ \t]+:[ \t]+' + str(SwImage.getSwImage(SwImage.FPGA).newVersion.get("DOMFPGA2", "")).replace(
        ".", "\.") + r'[ \t]+OK',
]

fpga_ver_sh_pattern = [
    r'fpga_ver\.sh',
    r'^[ \t]*DOMFPGA1:[ \t]+' + str(SwImage.getSwImage(SwImage.FPGA).newVersion.get("DOMFPGA1", "")).replace(".", "\."),
    r'^[ \t]*DOMFPGA2:[ \t]+' + str(SwImage.getSwImage(SwImage.FPGA).newVersion.get("DOMFPGA2", "")).replace(".", "\."),
]

cpld_ver_sh_pattern = [
    r'cpld_ver\.sh',
    r'^[ \t]*SMB_SYSCPLD:[ \t]+' + str(SwImage.getSwImage(SwImage.CPLD).newVersion.get("smb")).replace(".", "\."),
    r'^[ \t]*SMB_PWRCPLD:[ \t]+' + str(SwImage.getSwImage(SwImage.CPLD).newVersion.get("pwr")).replace(".", "\."),
    r'^[ \t]*SCMCPLD:[ \t]+' + str(SwImage.getSwImage(SwImage.CPLD).newVersion.get("scm")).replace(".", "\."),
    r'^[ \t]*FCMCPLD:[ \t]+' + str(SwImage.getSwImage(SwImage.CPLD).newVersion.get("fcm")).replace(".", "\."),
]

##### FB_DIAG_COM_TC_039_BMC_CPLD_TEST #####
cel_bmc_cpld_version_array = {
    "FCM_CPLD": SwImage.getSwImage(SwImage.CPLD).newVersion.get("fcm", ""),
    "SCM_CPLD": SwImage.getSwImage(SwImage.CPLD).newVersion.get("scm", ""),
    "SMB_CPLD": SwImage.getSwImage(SwImage.CPLD).newVersion.get("smb", ""),
    "PWR_CPLD": SwImage.getSwImage(SwImage.CPLD).newVersion.get("pwr", ""),
}

cel_qsfp_test_port_status_default = [r'[ \t\|]+(NO|YES)[ \t\|]+(ON|OFF)[ \t\|]+(ON|OFF)[ \t\|]+(ON|OFF)']
cel_qsfp_test_port_status_pattern_reset_off = [r'[ \t\|]+(NO|YES)[ \t\|]+(ON|OFF)[ \t\|]+(OFF)[ \t\|]+(ON|OFF)']
cel_qsfp_test_port_status_pattern_reset_on = [r'[ \t\|]+(NO|YES)[ \t\|]+(ON|OFF)[ \t\|]+(ON)[ \t\|]+(ON|OFF)']
cel_qsfp_test_port_status_pattern_lpmode_off = [r'[ \t\|]+(NO|YES)[ \t\|]+(ON|OFF)[ \t\|]+(ON|OFF)[ \t\|]+(OFF)']
cel_qsfp_test_port_status_pattern_lpmode_on = [r'[ \t\|]+(NO|YES)[ \t\|]+(ON|OFF)[ \t\|]+(ON|OFF)[ \t\|]+(ON)']
nvme_test_a = ['nvme\s+test.*?PASS']

cel_eeprom_test_array = {
    'read_tool' : 'eeprom_tool',
    'write_tool' : 'auto_eeprom',
    'option_d' : '-d',
    'option_e' : '-e',
    'part_SCM' : 'SCM',
    'part_FCM' : 'FCM',
    'part_SMB' : 'SMB',
    'part_FAN' : 'FAN',
    'part_BSM' : 'BSM',
    'pass_pattern' : 'EEPROM Update.*PASS]',
    'line_string' : 'WUX',
}
cel_eeprom_tool_opion_h_pass_pattern = ['-h.*help', '-w.*create local data file eeprom.bin',
                                    '-u.*update EEPROM by local data file eeprom.bin',
                                    '-d.*dump EEPROM data to eeprom_out.bin and parse',
                                    '-r.*dump EEPROM data to eeprom_out.bin', '-e.*EEPROM name']
cel_eeprom_tool_BSM_pass_pattern = [r'eeprom_location_on_fabric.*BSM']

####################### MINIPACK2 #############################
devicename = os.environ.get("deviceName", "")
import logging
logging.info("devicename:{}".format(devicename))
if "minipack2" in devicename.lower():
    cel_sensor_test_a_pattern = [
    r'cel-sensor-test[ \t]+-a$',
    r'check_sensor_util_status[ \t]+.*?PASS',
]
    pim_fpga_pattern = [
    r'IOB FPGA:[ \t]+' + str(SwImage.getSwImage(SwImage.FPGA).newVersion.get("SMB_IOB_FPGA", "")).replace(".", "\."),
    r'PIM1 DOMFPGA:[ \t]+' + str(SwImage.getSwImage(SwImage.FPGA).newVersion.get("PIM1 DOMFPGA", "")).replace(".", "\."),
    r'PIM2 DOMFPGA:[ \t]+' + str(SwImage.getSwImage(SwImage.FPGA).newVersion.get("PIM2 DOMFPGA", "")).replace(".", "\."),
    r'PIM3 DOMFPGA:[ \t]+' + str(SwImage.getSwImage(SwImage.FPGA).newVersion.get("PIM3 DOMFPGA", "")).replace(".", "\."),
    r'PIM4 DOMFPGA:[ \t]+' + str(SwImage.getSwImage(SwImage.FPGA).newVersion.get("PIM4 DOMFPGA", "")).replace(".", "\."),
    r'PIM5 DOMFPGA:[ \t]+' + str(SwImage.getSwImage(SwImage.FPGA).newVersion.get("PIM5 DOMFPGA", "")).replace(".", "\."),
    r'PIM6 DOMFPGA:[ \t]+' + str(SwImage.getSwImage(SwImage.FPGA).newVersion.get("PIM6 DOMFPGA", "")).replace(".", "\."),
    r'PIM7 DOMFPGA:[ \t]+' + str(SwImage.getSwImage(SwImage.FPGA).newVersion.get("PIM7 DOMFPGA", "")).replace(".", "\."),
    r'PIM8 DOMFPGA:[ \t]+' + str(SwImage.getSwImage(SwImage.FPGA).newVersion.get("PIM8 DOMFPGA", "")).replace(".", "\."),
]
    sensor_port_status_pattern = [
        r'check_sensor_util_status.*PASS'
    ]
    set_pim_ucd90160_level_pattern = [
        r'Set PIM1.*?OK',
        r'Set PIM2.*?OK',
        r'Set PIM3.*?OK',
        r'Set PIM4.*?OK',
        r'Set PIM5.*?OK',
        r'Set PIM6.*?OK',
        r'Set PIM7.*?OK',
        r'Set PIM8.*?OK'
    ]
    check_bios_boot_info_pattern = [
        r'boot_info\.sh[ \t]+bmc',
    ]
    bmc_boot_test_h_pattern = [
        r'cel-boot-test[ \t]+-h$',
        r'Usage:[ \t]+\./cel-boot-test[ \t]+options[ \t]+\(-h\|-s\|-a\|\[-b[ \t]+<bmc>\]\|\[-r[ \t]+<master\|slave>\]\)$',
        r'[ \t]*-h[ \t]+Show[ \t]+this[ \t]+help$',
        r'[ \t]*-b[ \t]+<bmc>$',
        r'[ \t]*-s[ \t]+Show[ \t]+boot[ \t]+status$',
        r'[ \t]*-r[ \t]+Boot[ \t]+from[ \t]<master\|slave>$',
        r'[ \t]*-a[ \t]+Auto[ \t]+test$',
    ]
    flashScan_h_pattern = [
        r'Usage:[ \t]+(\./)cel-flashScan-test[ \t]+options.*?',
        r'-h[ \t]+show this help',
        r'-a[ \t]+test'
    ]
    flashScan_a_pattern = [
        r'IOB_FPGA Flash ID Scan test.*PASS',
        #r'PCIE_SW:[ \t]+Flash ID Scan test.*PASS',
        #r'DOM_FPGA_ALL:[ \t]+Flash ID Scan test.*PASS'
        r'DOM_FPGA_PIM1:[ \t]+Flash ID Scan test.*PASS',
        r'DOM_FPGA_PIM2:[ \t]+Flash ID Scan test.*PASS',
        r'DOM_FPGA_PIM3:[ \t]+Flash ID Scan test.*PASS',
        r'DOM_FPGA_PIM4:[ \t]+Flash ID Scan test.*PASS',
        r'DOM_FPGA_PIM5:[ \t]+Flash ID Scan test.*PASS',
        r'DOM_FPGA_PIM6:[ \t]+Flash ID Scan test.*PASS',
        r'DOM_FPGA_PIM7:[ \t]+Flash ID Scan test.*PASS',
        r'DOM_FPGA_PIM8:[ \t]+Flash ID Scan test.*PASS',
    ]
    avs_h_pattern = [
        r'Usage:[ \t]+(\./)cel-avs-test[ \t]+options.*?',
        r'-h[ \t]+help information',
        r'-a[ \t]+test AVS'
    ]
    avs_a_pattern = [
        r'check_AVS.*PASS',
    ]
    #cel_fan_test_e_pattern = [
    #    r'cel-fan-test[ \t]+-e$',
    #    r'^[ \t]*CHECK[ \t]+FAN[ \t]+1[ \t]+Power[ \t]+Disable[ \t]+Status[ \t]+OK',
    #    r'^[ \t]*CHECK[ \t]+FAN[ \t]+3[ \t]+Power[ \t]+Disable[ \t]+Status[ \t]+OK',
    #    r'^[ \t]*CHECK[ \t]+FAN[ \t]+5[ \t]+Power[ \t]+Disable[ \t]+Status[ \t]+OK',
    #    r'^[ \t]*CHECK[ \t]+FAN[ \t]+7[ \t]+Power[ \t]+Disable[ \t]+Status[ \t]+OK',
    #    r'^[ \t]*CHECK[ \t]+FAN[ \t]+2[ \t]+Power[ \t]+Disable[ \t]+Status[ \t]+OK',
    #    r'^[ \t]*CHECK[ \t]+FAN[ \t]+4[ \t]+Power[ \t]+Disable[ \t]+Status[ \t]+OK',
    #    r'^[ \t]*CHECK[ \t]+FAN[ \t]+6[ \t]+Power[ \t]+Disable[ \t]+Status[ \t]+OK',
    #    r'^[ \t]*CHECK[ \t]+FAN[ \t]+8[ \t]+Power[ \t]+Disable[ \t]+Status[ \t]+OK',
    #]
    cel_fan_test_e_pattern = [
        r'cel-fan-test[ \t]+-e$',
        r'^[ \t]*Set ALL FAN Power disable[ \t]+OK',
        r'^[ \t]*CHECK[ \t]+ALL[ \t]+FAN[ \t]+Power[ \t]+Disable[ \t]+Status[ \t]+OK',
        r'^Set ALL FAN Power enable[ \t]+OK',
        r'^[ \t]*CHECK[ \t]+ALL[ \t]+FAN[ \t]+Power[ \t]+Enable[ \t]+Status[ \t]+OK',
        r'.+PASS'
    ]
    scm_cpld_accessed = [
        #r'fpga\s+scm+\s+r.*?',
        r'^\d+:\s+\d+'
    ]
    cel_ucd_security_help_array = {
        "bin_tool": "cel-pwmon-upgrade",
        "help_option": "show help",
        "scan_option": "read image version",
        "list_option": "online upgrade image",
        "board_option": "set the pwmon to security mode",
    }
    ucd_security_help_pattern = [
        '-r\s+(.+)',
        '-w\s+(.+)',
        '-s\s+(.+)',
    ]
    ucd_security_pattern = [
        'get\s+security\s+success\s+[A-Z_]+\d?\s+i2c\s+security_mode\s+=\s+0x\d{2}\s+bus=\d{1,3}\s+i2c_addr=0x\d{2}',
        '^[A_Z_]+\d\s+already\s+in\s+security\s+mode',
    ]
    cel_bmc_i2c_help_array = {
        "bin_tool": "cel-i2c-test",
        "help_option": "show help",
        "scan_option": "scan i2c devices",
        "list_option": "list all supported I2C devices information",
        "board_option": "specify the testing board. If not specified, all board will test.",
        "auto_option" : "auto test i2c devices"
    }
    bmc_i2c_help_pattern = [
                            '-h\s+(.+)',
                            '-s\s+(.+)',
                            '-l\s+(.+)',
                            '-b\s+(.+)',
                            '-a\s+(.+)',
                            ]
    bmc_i2c_keyword_pattern = ['scan_i2c_devices'
                               ]
    i2c_scan_pattern = ['[\w\d\_\-]+\*?\s+\d{1,2}\s+0x[0-9a-fA-F]{1,2}\s+(\w+)']
    i2c_scan_pass_keyword = 'OK'

    diag_install_pattern = [
        r'Verifying...',
        r'success[ \t]+install[ \t]+BMC_Diag',
        ]

    ##### FB_DIAG_COM_TC_052_FRU_EEPROM_UPDATE #####
    cel_fru_eeprom_update_array = {
        'read_tool' : 'eeprom_tool',
        'read_option' : '-d',
        'write_tool' : 'auto_eeprom',
        'verify_tool' : 'eeprom_verify',
        'scm_eeprom_path' : '/mnt/data1/BMC_Diag/utility/SCM_eeprom',
        'smb_eeprom_path' : '/mnt/data1/BMC_Diag/utility/SMB_eeprom',
        'sim_eeprom_path' : '/mnt/data1/BMC_Diag/utility/SIM_eeprom',
        'bmc_eeprom_path' : '/mnt/data1/BMC_Diag/utility/BMC_eeprom',
        'fcm-t_eeprom_path' : '/mnt/data1/BMC_Diag/utility/FCM_T_eeprom',
        'fcm-b_eeprom_path' : '/mnt/data1/BMC_Diag/utility/FCM_B_eeprom',
        'pim_eeprom_path' : '/mnt/data1/BMC_Diag/utility/PIM_eeprom',
        'fan_eeprom_path' : '/mnt/data1/BMC_Diag/utility/FAN_eeprom',
        'pass_pattern' : 'EEPROM Update Successfully.*PASS'
    }

    ##### FB_DIAG_COM_TS_054_MDIO_ERROR_STATUS_TEST #####
    cel_mdio_test_array = {
        'bin_tool' : 'fpga',
        'option_h' : '-h',
        'store_1' : 'mdio',
        'store_2' : 'pim',
        'option_r' : 'r',
        'option_pim' : 'pim=',
        'option_type' : 'type=1f',
        'option_phy' : 'phy=1',
        'ele1' : '0x9c',
        'ele2' : '0xb2e9',
        'ele3' : '0x210',
        'ele4' : '0x5201d000',
        'ele5' : '0x5201d001'
    }
    cel_mdio_option_h_pass_pattern = ['-h Help, show this help information', '-v Verbose, dump IO offset', '-s.*time', '-r.*num',
                                      'ver.*show driver and FPGA versions', 'reg.*data_to_write ...', 'pim.*data_to_write ...',
                                      'mdio.*data_to_write ...', 'scm.*data_to_write', 'smb.*data_to_write', 'pca.*data_to_write']
    cel_mdio_option_0x9c_pass_pattern = ['\d{5}c:  \w{8}']
    cel_mdio_option_0xb2e9_pass_pattern = ['00b2e9:  \w{4}']
    cel_mdio_option_0x210_pass_pattern = ['\d{6}:  \w{8}']
    cel_mdio_option_0x5201d000_pass_pattern = ['5201d000:  \w{8}']
    cel_mdio_option_0x5201d001_pass_pattern = ['5201d001:  \w{8}']

    ##### FB_DIAG_COM_TS_055_MDIO_ERROR_INTERRUPT_TEST #####
    cel_mdio_interrupt_test_array = {
        'bin_tool' : 'fpga',
        'store_1' : 'mdio',
        'store_2' : 'pim',
        'option_w' : 'w',
        'option_r' : 'r',
        'option_pim' : 'pim=',
        'option_type' : 'type=1f',
        'option_phy' : 'phy=1',
        'ele1' : '0x214',
        'ele2' : '0x5201d000',
        'ele3' : '0x2c ',
    }
    cel_mdio_option_0x214_pass_pattern = ['root.*#']
    cel_mdio_option_0x5200cb20_pass_pattern = ['5201d000.*\d{8}']
    cel_mdio_option_0x2c_pass_pattern = ['\d{5}c.*\w{8}']

    ##### FB_DIAG_COMM_TC_057_IOB_FPGA_ACCESS_SMB_CPLD_TEST #####
    cel_bmc_fpga_tool_test_array = {
        'bin_tool' : 'fpga',
        'option_smb' : 'smb',
        'read_option' : 'r',
        'option_0' : '0',
        'option_1': '1',
        'option_2': '2',
        'option_3': '3',
    }
    bmc_smb_cpld_0_pass_pattern = ['000000:  \d{2}']
    bmc_smb_cpld_1_pass_pattern = ['000001:  \d{2}']
    bmc_smb_cpld_2_pass_pattern_DVT = ['000002:  \d{2}']
    cel_bmc_smb_cpld_2_pass_pattern_EVT = ['000002:  \d{2}']
    cel_bmc_smb_cpld_3_pass_pattern = ['000003:  \d{2}']

    #### FB-DIAG-COM-TC-000-DIAG-INSTALL-UNINSTALL ####
    cel_diag_list = ["bin", "common", "configs", "firmware", "log", "utility"]

    cel_bmc_version_str = ''

    minipack2_check_fpga_h = [
        r'Minipack2 FPGA IO access tool',
        r'Version:.*?',
        r'-v',
        r'-s',
        r'-t',
        r'-r'
    ]
    cel_fan_test_g_p_70_pattern = [
    r'cel-fan-test[ \t]+-g$',
    # The error is acceptance +/- 3% and the number does not have a decimal digit,
    # it is approximately 48 - 52 shows here.
    r'^[ \t]*Fan[ \t]+1[ \t]+RPMs:[ \t]+\d{1,5},[ \t]+\d{1,5},[ \t]+\((6[89]|7[012])%\)$',
    r'^[ \t]*Fan[ \t]+2[ \t]+RPMs:[ \t]+\d{1,5},[ \t]+\d{1,5},[ \t]+\((6[89]|7[012])%\)$',
    r'^[ \t]*Fan[ \t]+3[ \t]+RPMs:[ \t]+\d{1,5},[ \t]+\d{1,5},[ \t]+\((6[89]|7[012])%\)$',
    r'^[ \t]*Fan[ \t]+4[ \t]+RPMs:[ \t]+\d{1,5},[ \t]+\d{1,5},[ \t]+\((6[89]|7[012])%\)$',
]

    cal_fan_test_p_70_pattern = [
    r'cel-fan-test[ \t]+-p[ \t]*\d{1,3}$',
    # The error is acceptance +/- 3% and the number does not have a decimal digit,
    # it is approximately 48 - 52 shows here.
    r'^Successfully[ \t]+set[ \t]+fan[ \t]+1[ \t]+speed[ \t]+to[ \t]+(6[89]|7[012])%$',
    r'^Successfully[ \t]+set[ \t]+fan[ \t]+2[ \t]+speed[ \t]+to[ \t]+(6[89]|7[012])%$',
    r'^Successfully[ \t]+set[ \t]+fan[ \t]+3[ \t]+speed[ \t]+to[ \t]+(6[89]|7[012])%$',
    r'^Successfully[ \t]+set[ \t]+fan[ \t]+4[ \t]+speed[ \t]+to[ \t]+(6[89]|7[012])%$',
]

    ##### FB_DIAG_COM_TC_061_PARSE_EEPROM_TEST #####
    cel_eeprom_qsfp_array = {
        'bin_tool' : 'cel-qsfp-test',
        'option_h' : '-h',
        'option_help' : '--help',
        'pim' : '-m',
        'port' :'-p',
        'option_i' : '-i',
    }
    cel_qsfp_h_pass_pattern = ['-m, --pim.*', '-p, --port.*', '-i  --info.*', '-s  --status.*', '-r  --reset.*',
                               '-l, --lpmode.*', '-a, --all.*', '--pim=0 -s.*', '--pim=1 -s.*', '--pim=2 --reset=on.*',
                               '--pim=1 --port=2 --reset=on.*', '--pim=1 --port=5 --lpmode=on.*', ' --all.*']
    cel_qsfp_pass_pattern = ['Identifier description.*' , 'Temperature.*', #'Extended Identifier.*', #'Device Technology.*'
            ]

    ##### FB_DIAG_COM_TC_074_FCM_CPLD_UPDATE_VIA_I2C #####
    cel_bmc_cpld_fcm_b_i2c_array = {
        'bin_tool' : 'cel-i2c_upgrade_cpld',
        'option1' : '-s',
        'dev' : 'FCM-B',
        'dev1' : 'FCM-T',
        'option2' : '-f',
        'option3' : '-h',
        'newimage' : SwImage.getSwImage(SwImage.CPLD).newImage["fcm"],
        'oldimage' : SwImage.getSwImage(SwImage.CPLD).oldImage["fcm"],
        'check_tool': 'cel-cpld-test',
        'check_option': '-v',
        'check_option1': '-k',
    }
    cpld_option_h_array = [
        r'cel-i2c_upgrade_cpld[ \t]+-h',
        r'cel-i2c_upgrade_cpld,*',
        r'^[ \t]*-h[ \t]+show help',
        r'^[ \t]*-s[ \t]+select tpye CPLD',
        r'^[ \t]*-f[ \t]+update image file',
        ]
    fcm_hw_upgrade_file = SwImage.getSwImage(SwImage.CPLD).newImage["fcm"]
    fcm_hw_downgrade_file = SwImage.getSwImage(SwImage.CPLD).oldImage["fcm"]
    fcm_hw_package_copy_list = [fcm_hw_upgrade_file, fcm_hw_downgrade_file]
    cel_bmc_cpld_i2c_pass_pattern = ['FCM-B Upgrade:.*100%', 'Complete program FCM-B CPLD!']
    cel_bmc_cpld_t_i2c_pass_pattern = ['FCM-T Upgrade.*100%', 'Complete program FCM-T CPLD!']
    cel_fcm_b_oldversion_pass_pattern = 'FCM_B_CPLD[ \t]+:[ \t]' + SwImage.getSwImage(SwImage.CPLD).oldVersion["FCMCPLD B"]
    cel_fcm_t_oldversion_pass_pattern = 'FCM_T_CPLD[ \t]+:[ \t]' + SwImage.getSwImage(SwImage.CPLD).oldVersion["FCMCPLD T"]
    cel_fcm_oldversion_pass_pattern = [cel_fcm_b_oldversion_pass_pattern, cel_fcm_t_oldversion_pass_pattern]
    cel_fcm_b_newversion_pass_pattern = 'FCM_B_CPLD[ \t]+:[ \t]' + SwImage.getSwImage(SwImage.CPLD).newVersion["FCMCPLD B"]
    cel_fcm_T_newversion_pass_pattern = 'FCM_T_CPLD[ \t]+:[ \t]' + SwImage.getSwImage(SwImage.CPLD).newVersion["FCMCPLD T"]
    cel_fcm_newversion_pass_pattern = [cel_fcm_b_newversion_pass_pattern, cel_fcm_T_newversion_pass_pattern]

    ##### FB_DIAG_COM_TC_075_FCM_CPLD_UPDATE_VIA_JTAG #####
    cel_bmc_fcm_cpld_jtag_array = {
        'bin_tool': 'cpld_update.sh',
        'option1': '-s',
        'dev': 'FCM-B',
        'dev1': 'FCM-T',
        'option2': '-f',
        'option3': '-h',
        'option4': 'sw',
        'newimage': SwImage.getSwImage(SwImage.CPLD).newImage["fcm"],
        'oldimage': SwImage.getSwImage(SwImage.CPLD).oldImage["fcm"],
        'check_tool': 'cel-cpld-test',
        'check_option': '-k',
    }
    cel_bmc_cpld_fcm_b_pass_pattern = ['100%', ' PASS', 'Upgrade successful']
    cel_cpld_update_option_h_array = [
        r'VME file for software mode',
        r'JED file for hardware mode',
        r'hw: Program the CPLD using JTAG hardware mode',
        r'sw: Program the CPLD using JTAG software mode',
    ]

    ##### FB_DIAG_COM_TC_076_SCM_CPLD_UPDATE_I2C #####
    cel_bmc_cpld_scm_i2c_array = {
        'bin_tool': 'cel-i2c_upgrade_cpld',
        'option1': '-s',
        'dev': 'SCM',
        'option2': '-f',
        'option3': '-h',
        'newimage': SwImage.getSwImage(SwImage.CPLD).newImage["scm"],
        'oldimage': SwImage.getSwImage(SwImage.CPLD).oldImage["scm"],
        'check_tool': 'cel-cpld-test',
        'check_option': '-v',
        'check_option1': '-k',
    }
    scm_upgrade_file = SwImage.getSwImage(SwImage.CPLD).newImage["scm"]
    scm_downgrade_file = SwImage.getSwImage(SwImage.CPLD).oldImage["scm"]
    scm_hw_package_copy_list = [scm_upgrade_file, scm_downgrade_file]
    cel_bmc_cpld_scm_pass_pattern = ['SCM Upgrade:.*100%', 'Complete program SCM CPLD!']
    cel_scm_oldversion_pass_pattern = 'SCM_CPLD[ \t]+:[ \t]' + SwImage.getSwImage(SwImage.CPLD).oldVersion["SCMCPLD"]
    cel_scm_oldversion_pass_pattern = [cel_scm_oldversion_pass_pattern]
    cel_scm_newversion_pass_pattern = 'SCM_CPLD[ \t]+:[ \t]' + SwImage.getSwImage(SwImage.CPLD).newVersion["SCMCPLD"]
    cel_scm_newversion_pass_pattern = [cel_scm_newversion_pass_pattern]

    #####FB_DIAG_COM_TC_077_SCM_CPLD_UPDATE_JTAG #####
    cel_bmc_cpld_scm_jtag_array = {
        'bin_tool': 'cpld_update.sh',
        'option1': '-s',
        'dev': 'SCM',
        'option2': '-f',
        'option3': '-h',
        'option4': 'sw',
        'newimage': SwImage.getSwImage(SwImage.CPLD).newImage["scm"],
        'oldimage': SwImage.getSwImage(SwImage.CPLD).oldImage["scm"],
        'check_tool': 'cel-cpld-test',
        'check_option': '-v',
        'check_option1': '-k',
    }
    cel_bmc_cpld_scm_jtag_pass_pattern = ['100%', ' PASS', 'Upgrade successful']

    ##### FB_DIAG_COM_TC_080_PDB_CPLD_UPDATE_VIA_I2C #####
    cel_bmc_cpld_pdb_array = {
        'bin_tool': 'cel-i2c_upgrade_cpld',
        'option1': '-s',
        'dev': 'PDB-L',
        'dev1': 'PDB-R',
        'option2': '-f',
        'option3': '-h',
        'newimage': SwImage.getSwImage(SwImage.CPLD).newImage["pwr"],
        'oldimage': SwImage.getSwImage(SwImage.CPLD).oldImage["pwr"],
        'check_tool': 'cel-cpld-test',
        'check_option': '-v',
        'check_option1': '-k',
    }
    cel_bmc_cpld_pwr_l_pass_pattern = ['PDB-L Upgrade:.*100%', 'Complete program PDB-L CPLD!']
    cel_bmc_cpld_pwr_r_pass_pattern = ['PDB-R Upgrade:.*100%', 'Complete program PDB-R CPLD!']
    cel_pwr_l_oldversion_pass_pattern = 'PDB_L_CPLD[ \t]+:[ \t]' + SwImage.getSwImage(SwImage.CPLD).oldVersion["PWRCPLD L"]
    cel_pwr_l_newversion_pass_pattern = 'PDB_L_CPLD[ \t]+:[ \t]' + SwImage.getSwImage(SwImage.CPLD).newVersion["PWRCPLD L"]
    cel_pwr_r_oldversion_pass_pattern = 'PDB_R_CPLD[ \t]+:[ \t]' + SwImage.getSwImage(SwImage.CPLD).oldVersion["PWRCPLD R"]
    cel_pwr_r_newversion_pass_pattern = 'PDB_R_CPLD[ \t]+:[ \t]' + SwImage.getSwImage(SwImage.CPLD).newVersion["PWRCPLD R"] + '.*OK'
    cel_pwr_hw_oldversion_pass_pattern = [cel_pwr_l_oldversion_pass_pattern, cel_pwr_r_oldversion_pass_pattern]
    cel_pwr_hw_newversion_pass_pattern = [cel_pwr_l_newversion_pass_pattern, cel_pwr_r_newversion_pass_pattern]
    pwr_hw_upgrade_file = SwImage.getSwImage(SwImage.CPLD).newImage["pwr"]
    pwr_hw_downgrade_file = SwImage.getSwImage(SwImage.CPLD).oldImage["pwr"]
    pwr_hw_package_copy_list = [pwr_hw_upgrade_file, pwr_hw_downgrade_file]

    ##### TC-031-TPM-DEVICE-TEST #####
    tpm_test_keyword='TPM test all'
    cel_tpm_test_l_pattern = [
        r'name.*tpm',
        r'get restart command: systemctl restart tpm2-abrmd.service',
        r'get command: tpm2_getcap -c properties-fixed',
        r'chip type: SLB9670'
        ]

    #### FB-DIAG-COM-TS-034-MANAGEMENT-ETHER-PORT-MAC-CHECK-TEST ####
    cel_mac_test_pattern = [
        r'[a-z]{3}\d',
        r'[A-Fa-f0-9]{1,2}\:[A-Fa-f0-9]{1,2}\:[A-Fa-f0-9]{1,2}\:[A-Fa-f0-9]{1,2}\:[A-Fa-f0-9]{1,2}\:[A-Fa-f0-9]{1,2}'
    ]

    #### FB-DIAG-COM-TS-039-REVISION-AND-DEVICE/BOARD ID/SCRATCH-PAD-TEST ####
    option_str = ' --config=../configs/IOB.yaml'
    fpga_version = '[ \t]*FPGA[ \t]+driver[ \t]+version:[ \t]+' + str(SwImage.getSwImage(SwImage.FPGA_DRIVER).newVersion).replace('.', r'.') + r'[ \t]*$'

    show_version_array = {
        "diag_version": SwImage.getSwImage(SwImage.DIAG).newVersion,
        "os_version": SwImage.getSwImage(SwImage.OS).newVersion,
        "kernel_version": SwImage.getSwImage(SwImage.KERNEL).newVersion,
        "bmc_version": str(SwImage.getSwImage(SwImage.BMC).newVersion).replace(".", ".0"),
        # OpenBMC shows m.n and DIAG shows m.0n
        "bios_version": SwImage.getSwImage(SwImage.BIOS).newVersion,
        "fpga1_version": SwImage.getSwImage(SwImage.FPGA).newVersion["PIM1 DOMFPGA"],
        "fpga2_version": SwImage.getSwImage(SwImage.FPGA).newVersion["PIM2 DOMFPGA"],
        "scm_cpld_version": str(SwImage.getSwImage(SwImage.CPLD).newVersion["SCMCPLD"]),
        "smb_cpld_version": SwImage.getSwImage(SwImage.CPLD).newVersion["SMBCPLD"],
        "i2c_fw_version": SwImage.getSwImage(SwImage.I210).newVersion,

    }

    Minipack2_show_version_array = {
        "diag_version": SwImage.getSwImage(SwImage.DIAG).newVersion,
        "os_version": SwImage.getSwImage(SwImage.OS).newVersion,
        "kernel_version": SwImage.getSwImage(SwImage.KERNEL).newVersion,
        "bmc_version": '1.03',
        # OpenBMC shows m.n and DIAG shows m.0n
        "bios_version": SwImage.getSwImage(SwImage.BIOS).newVersion,
        "i2c_fw_version": SwImage.getSwImage(SwImage.I210).newVersion,
    }

    fpga_pim_upgrade_file = SwImage.getSwImage(SwImage.FPGA).newImage.get("pim","no_such_key")
    fpga_pim_downgrade_file = SwImage.getSwImage(SwImage.FPGA).oldImage.get("pim","no_such_key")
    fpga_package_copy_list = [fpga_pim_upgrade_file, fpga_pim_downgrade_file]
    fpga_iob_upgrade_file = SwImage.getSwImage(SwImage.FPGA).newImage.get("iob","no_such_key")
    fpga_iob_downgrade_file = SwImage.getSwImage(SwImage.FPGA).oldImage.get("iob","no_such_key")
    fpga_iob_package_copy_list = [fpga_iob_upgrade_file, fpga_iob_downgrade_file]
    fpga_upgrade_ver = SwImage.getSwImage(SwImage.FPGA).newVersion["PIM1 DOMFPGA"]
    fpga_downgrade_ver = SwImage.getSwImage(SwImage.FPGA).oldVersion["PIM1 DOMFPGA"]
    fpga_ver_cmd = "./fpga ver"
    cel_fpga_test_k_cmd = "./{} -k".format(cel_fpga_help_array["bin_tool"])
    spi_util_write_low_cmd = "{} write spi1 IOB_FPGA {}".format(spiUtil_tool, fpga_iob_package_copy_list[1])
    spi_util_write_high_cmd = "{} write spi1 IOB_FPGA {}".format(spiUtil_tool, fpga_iob_package_copy_list[0])
    fpga_IOB_upgrade_ver = SwImage.getSwImage(SwImage.FPGA).newVersion["SMB_IOB_FPGA"]
    fpga_IOB_downgrade_ver = SwImage.getSwImage(SwImage.FPGA).oldVersion["SMB_IOB_FPGA"]
    fpga_ver_IOB_pattern = { "FPGA IOB": "FPGA IOB\s+([\d.]+)" }
    fpga_ver_IOB_low_pattern = { "FPGA IOB  {}".format(fpga_IOB_downgrade_ver): "FPGA IOB\s+{}".format(fpga_IOB_downgrade_ver) }
    fpga_ver_IOB_high_pattern = { "FPGA IOB {}".format(fpga_IOB_upgrade_ver): "FPGA IOB\s+{}".format(fpga_IOB_upgrade_ver) }
    cel_fpga_test_k_IOB_pattern = { "SMB_IOB_FPGA : [version]": "SMB_IOB_FPGA\s+:\s+([\d.]+)\s+" }
    cel_fpga_test_k_IOB_low_pattern = { "SMB_IOB_FPGA : {}".format(fpga_IOB_downgrade_ver): "SMB_IOB_FPGA\s+:\s+{}\s+".format(fpga_IOB_downgrade_ver) }
    cel_fpga_test_k_IOB_high_pattern = { "SMB_IOB_FPGA : {}".format(fpga_IOB_upgrade_ver): "SMB_IOB_FPGA\s+:\s+{}\s+".format(fpga_IOB_upgrade_ver) }
    spi_util_write_pattern = {"Verifying flash... VERIFIED": "Verifying flash[\s\S]+"}
    remove_fpga_IOB_files_cmd = "rm -f {} {}".format(fpga_iob_package_copy_list[0], fpga_iob_package_copy_list[1])

    version_test_S_or_show_pattern = [
        r'(\./)?cel-version-test[ \t]+(-S|--show)',
        r'^Diag[ \t]+Version:[ \t]+' + SwImage.getSwImage(SwImage.DIAG).newVersion + r'$',
        r'^OS[ \t]+Diag:[ \t]+' + SwImage.getSwImage(SwImage.DIAG_OS).newVersion + r'$',
        r'^OS[ \t]+Version:[ \t]+' + SwImage.getSwImage(SwImage.OS).newVersion + r'$',
        r'^Kernel[ \t]+Version:[ \t]+' + SwImage.getSwImage(SwImage.KERNEL).newVersion + r'$',
        r'^BMC[ \t]+Version:[ \t]+' + str(SwImage.getSwImage(SwImage.BMC).newVersion).replace(".", ".0") + r'$',
        r'^BIOS[ \t]+Version:[ \t]+' + SwImage.getSwImage(SwImage.BIOS).newVersion + r'$',
        #r'^BIOS[ \t]+boot:[ \t]+(master|slave)$',
        r'^FPGA1[ \t]+Version:[ \t]+' + SwImage.getSwImage(SwImage.FPGA).newVersion["PIM1 DOMFPGA"] + r'$',
        r'^FPGA2[ \t]+Version:[ \t]+' + SwImage.getSwImage(SwImage.FPGA).newVersion["PIM2 DOMFPGA"] + r'$',
        r'^SCM[ \t]+CPLD[ \t]+Version:[ \t]+' + SwImage.getSwImage(SwImage.CPLD).newVersion["SCMCPLD"] + r'$',
        r'^SMB[ \t]+CPLD[ \t]+Version:[ \t]+' + SwImage.getSwImage(SwImage.CPLD).newVersion["SMBCPLD"] + r'$',
        r'^I210[ \t]+FW[ \t]+Version:[ \t]+' + SwImage.getSwImage(SwImage.I210).newVersion + r'$',
    ]

    fpga_test_v_pattern = [
        r'cel-fpga-test[ \t]+-v',
        r'^[ \t]*SMB_DOM_FPGA_1[ \t]+:[ \t]+' + str(SwImage.getSwImage(SwImage.FPGA).newVersion["PIM1 DOMFPGA"]).replace(
            ".", "\.") + r'$',
        r'^[ \t]*SMB_DOM_FPGA_2[ \t]+:[ \t]+' + str(SwImage.getSwImage(SwImage.FPGA).newVersion["PIM2 DOMFPGA"]).replace(
            ".", "\.") + r'$',
    ]

    power_status_off = r'Microserver[ \t]+power[ \t]+is[ \t]+off'
    power_status_on = r'Microserver[ \t]+power[ \t]+is[ \t]+on'

    #### FB-DIAG-COM-TS-057-FPGA-UPGRADE-STRESS-TEST ####
    verify_fpga_ver_sh_downgrade_pattern = [
        r'fpga_ver\.sh',
        r'^[ \t]*PIM1 DOMFPGA:[ \t]+' + str(SwImage.getSwImage(SwImage.FPGA).oldVersion["PIM1 DOMFPGA"]).replace(".", "\."),
        r'^[ \t]*PIM2 DOMFPGA:[ \t]+' + str(SwImage.getSwImage(SwImage.FPGA).oldVersion["PIM2 DOMFPGA"]).replace(".", "\."),
    ]

    verify_fpga_ver_sh_upgrade_pattern = [
        r'fpga_ver\.sh',
        r'^[ \t]*PIM1 DOMFPGA:[ \t]+' + str(SwImage.getSwImage(SwImage.FPGA).newVersion["PIM1 DOMFPGA"]).replace(".", "\."),
        r'^[ \t]*PIM2 DOMFPGA:[ \t]+' + str(SwImage.getSwImage(SwImage.FPGA).newVersion["PIM2 DOMFPGA"]).replace(".", "\."),
    ]

    fpga_ver_sh_pattern = [
        r'^[ \t]*PIM[ \t]*1 DOM(\s|FPGA)*:[ \t]+' + str(SwImage.getSwImage(SwImage.FPGA).newVersion["PIM1 DOMFPGA"]).replace(".", "\."),
        r'^[ \t]*PIM[ \t]*2 DOM(\s|FPGA)*:[ \t]+' + str(SwImage.getSwImage(SwImage.FPGA).newVersion["PIM2 DOMFPGA"]).replace(".", "\."),
    ]

    cpld_ver_sh_pattern = [
        r'cpld_ver\.sh',
        r'^[ \t]*SMB_SYSCPLD:[ \t]+' + str(SwImage.getSwImage(SwImage.CPLD).newVersion["SMBCPLD"]).replace(".", "\."),
        r'^[ \t]*SMB_PWRCPLD:[ \t]+' + str(SwImage.getSwImage(SwImage.CPLD).newVersion["PWRCPLD L"]).replace(".", "\."),
        r'^[ \t]*SCMCPLD:[ \t]+' + str(SwImage.getSwImage(SwImage.CPLD).newVersion["SCMCPLD"]).replace(".", "\."),
        r'^[ \t]*FCMCPLD:[ \t]+' + str(SwImage.getSwImage(SwImage.CPLD).newVersion["FCMCPLD B"]).replace(".", "\."),
    ]

    cel_bmc_cpld_version_array = {
        "FCM_CPLD": SwImage.getSwImage(SwImage.CPLD).newVersion["FCMCPLD B"],
        "SCM_CPLD": SwImage.getSwImage(SwImage.CPLD).newVersion["SCMCPLD"],
        "SMB_CPLD": SwImage.getSwImage(SwImage.CPLD).newVersion["SMBCPLD"],
        # smb - the old one is 4.0 and now it is 2.4
        "PWR_CPLD": SwImage.getSwImage(SwImage.CPLD).newVersion["PWRCPLD L"],
    }

    ##### TC-1107-FCM-UPDATE-TEST #####
    fcm_upgrade_ver = SwImage.getSwImage(SwImage.CPLD).newVersion["FCMCPLD B"]
    fcm_downgrade_ver = SwImage.getSwImage(SwImage.CPLD).oldVersion["FCMCPLD B"]

    ##### TC-1108-SCM-UPDATE-TEST #####
    scm_upgrade_ver = SwImage.getSwImage(SwImage.CPLD).newVersion["SCMCPLD"]
    scm_downgrade_ver = str(SwImage.getSwImage(SwImage.CPLD).oldVersion["SCMCPLD"]).replace("f", "15")

    ##### TC-1109-SYSTEM-UPDATE-TEST #####
    smb_upgrade_ver = SwImage.getSwImage(SwImage.CPLD).newVersion["SMBCPLD"]
    smb_downgrade_ver = SwImage.getSwImage(SwImage.CPLD).oldVersion["SMBCPLD"]

    ##### TC-1110-POWER-UPDATE-TEST #####
    pwr_upgrade_ver = SwImage.getSwImage(SwImage.CPLD).newVersion["PWRCPLD L"]
    pwr_downgrade_ver = SwImage.getSwImage(SwImage.CPLD).oldVersion["PWRCPLD L"]

    cel_software_v_pattern = [
        r'cel-software-test[ \t]+-v$',
        r'Diag[ \t]+version:' + str(SwImage.getSwImage(SwImage.DIAG).newVersion).replace(".", "\."),
        r'^[ \t]*OpenBMC[ \t]+Release[ \t]+.*?',
        #r'^[ \t]*Show[ \t]+all[ \t]+CPLD.*?',
        r'^[ \t]*FCM_B_CPLD[ \t]+:[ \t]+' + str(SwImage.getSwImage(SwImage.CPLD).newVersion["FCMCPLD B"]).replace(".", "\."),
        r'^[ \t]*FCM_T_CPLD[ \t]+:[ \t]+' + str(SwImage.getSwImage(SwImage.CPLD).newVersion["FCMCPLD T"]).replace(".", "\."),
        r'^[ \t]*SCM_CPLD[ \t]+:[ \t]+' + str(SwImage.getSwImage(SwImage.CPLD).newVersion["SCMCPLD"]).replace(".", "\."),
        r'^[ \t]*SMB_CPLD[ \t]+:[ \t]+' + str(SwImage.getSwImage(SwImage.CPLD).newVersion["SMBCPLD"]).replace(".", "\."),
        r'^[ \\t]*PDB_L_CPLD[ \t]+:[ \t]+' + str(SwImage.getSwImage(SwImage.CPLD).newVersion["PWRCPLD L"]).replace(".", "\."),
        r'^[ \\t]*PDB_R_CPLD[ \t]+:[ \t]+' + str(SwImage.getSwImage(SwImage.CPLD).newVersion["PWRCPLD R"]).replace(".", "\."),
    ]

    fw_util_version = [
        r'^[ \t]*BMC[ \t]+Version:.*?',
        r'^[ \t]*Fan[ \t]+Speed[ \t]+.*?',
        r'^[ \t]*FCMCPLD[ \t]+B:[ \t]+' + str(SwImage.getSwImage(SwImage.CPLD).newVersion["FCMCPLD B"]).replace(".", "\."),
        r'^[ \t]*FCMCPLD[ \t]+T:[ \t]+' + str(SwImage.getSwImage(SwImage.CPLD).newVersion["FCMCPLD T"]).replace(".", "\."),
        r'^[ \t]*PWRCPLD[ \t]+L:[ \t]+' + str(SwImage.getSwImage(SwImage.CPLD).newVersion["PWRCPLD L"]).replace(".", "\."),
        r'^[ \t]*PWRCPLD[ \t]+R:[ \t]+' + str(SwImage.getSwImage(SwImage.CPLD).newVersion["PWRCPLD R"]).replace(".", "\."),
        r'^[ \t]*SCMCPLD:[ \t]+' + str(SwImage.getSwImage(SwImage.CPLD).newVersion["SCMCPLD"]).replace(".", "\."),
        r'^[ \t]*SMBCPLD:[ \t]+' + str(SwImage.getSwImage(SwImage.CPLD).newVersion["SMBCPLD"]).replace(".", "\."),
    ]

    cpld_option_h = [
        #r'#[ \t]*(\./)?cel-cpld-test[ \t]+-h',
        #r'^Usage:[ \t]+\./cel-cpld-test[ \t]+options.*?',
        r'^[ \t]*-h[ \t]+print[ \t]+this[ \t]+help[ \t]+message[ \t]+and[ \t]+exit',
        r'^[ \t]*-w[ \t]+write[ \t]+to[ \t]+CPLD',
        r'^[ \t]*-r[ \t]+read[ \t]+from[ \t]+CPLD',
        r'^[ \t]*-c[ \t]+CPLD[ \t]+name.*?',
        r'^[ \t]*-s[ \t]+CPLD[ \t]+register[ \t]+address',
        r'^[ \t]*-i[ \t]+check[ \t]+CPLD[ \t]+JTAG[ \t]+chain',
        r'^[ \t]*-d[ \t]+data[ \t]+written[ \t]+to[ \t]+CPLD',
        r'^[ \t]*-v[ \t]+show[ \t]+CPLD[ \t]+version',
        #r'^[ \t]*-k[ \t]+check[ \t]CPLD[ \t]+version',
        r'^[ \t]*-a[ \t]+auto[ \t]+test[ \t]+configure[ \t]+items',
    ]
    cpld_option_h_dc = [
        # r'#[ \t]*(\./)?cel-cpld-test[ \t]+-h',
        # r'^Usage:[ \t]+\./cel-cpld-test[ \t]+options.*?',
        r'^[ \t]*-h[ \t]+print[ \t]+this[ \t]+help[ \t]+message[ \t]+and[ \t]+exit',
        r'^[ \t]*-w[ \t]+write[ \t]+to[ \t]+CPLD',
        r'^[ \t]*-r[ \t]+read[ \t]+from[ \t]+CPLD',
        r'^[ \t]*-c[ \t]+CPLD[ \t]+name.*?',
        r'^[ \t]*-s[ \t]+CPLD[ \t]+register[ \t]+address',
        r'^[ \t]*-i[ \t]+check[ \t]+CPLD[ \t]+JTAG[ \t]+chain',
        r'^[ \t]*-d[ \t]+data[ \t]+written[ \t]+to[ \t]+CPLD',
        r'^[ \t]*-v[ \t]+show[ \t]+CPLD[ \t]+version',
        #r'^[ \t]*-k[ \t]+check[ \t]CPLD[ \t]+version',
        r'^[ \t]*-a[ \t]+auto[ \t]+test[ \t]+configure[ \t]+items',
    ]
    cpld_option_v = [
        #r'#[ \t]*(\./)?cel-cpld-test[ \t]+-v',
        #r'^[ \t]*Show[ \t]+all[ \t]+CPLD[ \t]+version:',
        r'^[ \t]*FCM_B_CPLD[ \t]+:[ \t]+' + str(SwImage.getSwImage(SwImage.CPLD).newVersion["FCMCPLD B"]).replace(".", "\."),
        #r'^[ \t]*FCM_T_CPLD[ \t]+:[ \t]+' + str(SwImage.getSwImage(SwImage.CPLD).newVersion["FCMCPLD T"]).replace(".", "\."),
        #r'^[ \t]*SCM_CPLD[ \t]+:[ \t]+' + str(SwImage.getSwImage(SwImage.CPLD).newVersion["SCMCPLD"]).replace(".", "\."),
        r'^[ \t]*SMB_CPLD[ \t]+:[ \t]+' + str(SwImage.getSwImage(SwImage.CPLD).newVersion["SMBCPLD"]).replace(".", "\."),
        r'^[ \\t]*PDB_L_CPLD[ \t]+:[ \t]+' + str(SwImage.getSwImage(SwImage.CPLD).newVersion["PWRCPLD L"]).replace(".", "\."),
        r'^[ \\t]*PDB_R_CPLD[ \t]+:[ \t]+' + str(SwImage.getSwImage(SwImage.CPLD).newVersion["PWRCPLD R"]).replace(".", "\."),
    ]

    cpld_option_a = [
        #r'#[ \t]*(\./)?cel-cpld-test[ \t]+-a',
        r'^check_cpld_scratch[ \t]+.*PASS',
        r'^show_CPLD_version[ \t]+.*PASS',
    ]

    ##### FB-DIAG-COMM-TC-038-INTERNAL-USB-TEST-COME #####
    openbmc_ping_to_come_pattern = [
        r'([0-9a-fA-F]{1,4}:){1,3}(:[0-9a-fA-F]{1,4}){1,4}.*seq=0',
        r'([0-9a-fA-F]{1,4}:){1,3}(:[0-9a-fA-F]{1,4}){1,4}.*seq=1',
        r'([0-9a-fA-F]{1,4}:){1,3}(:[0-9a-fA-F]{1,4}){1,4}.*seq=2',
        r'([0-9a-fA-F]{1,4}:){1,3}(:[0-9a-fA-F]{1,4}){1,4}.*seq=3',
        r'([0-9a-fA-F]{1,4}:){1,3}(:[0-9a-fA-F]{1,4}){1,4}.*seq=4',
        r'([0-9a-fA-F]{1,4}:){1,3}(:[0-9a-fA-F]{1,4}){1,4}.*seq=5',
    ]

    come_ping_to_openbmc_pattern = [
        r'([0-9a-fA-F]{1,4}:){1,3}(:[0-9a-fA-F]{1,4}){1,4}.*seq=1',
        r'([0-9a-fA-F]{1,4}:){1,3}(:[0-9a-fA-F]{1,4}){1,4}.*seq=2',
        r'([0-9a-fA-F]{1,4}:){1,3}(:[0-9a-fA-F]{1,4}){1,4}.*seq=3',
        r'([0-9a-fA-F]{1,4}:){1,3}(:[0-9a-fA-F]{1,4}){1,4}.*seq=4',
        r'([0-9a-fA-F]{1,4}:){1,3}(:[0-9a-fA-F]{1,4}){1,4}.*seq=5',
        r'([0-9a-fA-F]{1,4}:){1,3}(:[0-9a-fA-F]{1,4}){1,4}.*seq=6',
    ]

    openbmc_default_ipv6 = r'fe80::ff:fe00:1'
    centos_default_ipv6 = r'fe80::ff:fe00:2'
    internal_interface = "usb0"

    check_i2c_upgrade_cpld_h = [
        #r'#[ \t]*(\./)?cel-i2c_upgrade_cpld[ \t]+-h',
        r'^Usage:[ \t]+\./cel-i2c_upgrade_cpld[ \t]+options[ \t]+\(-h\|-s\|-f\).*?',
        r'^[ \t]*-h[ \t]+show[ \t]+help',
        r'^[ \t]*-s[ \t]+select[ \t]+tpye[ \t]+CPLD',
        r'^[ \t]*-f[ \t]+update[ \t]+image[ \t]+file'
    ]
    Update_CPLD_SMB_Image_PATH = '../../Images/CPLD/SMB/'
    CPLD_MiniPack2_SMB_CPLD_TOP_PATH = '../firmware/CPLD/'
    check_i2c_upgrade_cpld_SMB_f = [
        r'Complete program SMB CPLD!'
    ]

    pci_option_a_pattern = r'PCIe[ \t]+test.*?PASS'
    each_pice_lspci = [
        r'^[ /t]*00:[ \t]+.*?',
        r'^[ /t]*10:[ \t]+.*?',
        r'^[ /t]*20:[ \t]+.*?',
        r'^[ /t]*30:[ \t]+.*?',
        r'^[ /t]*40:[ \t]+.*?',
        r'^[ /t]*50:[ \t]+.*?',
        r'^[ /t]*60:[ \t]+.*?',
        r'^[ /t]*70:[ \t]+.*?',
        r'^[ /t]*80:[ \t]+.*?',
        r'^[ /t]*90:[ \t]+.*?',
    ]

    power_cycle_stress_option_h = [
        # r'#[ \t]*(\./)?power_cycle_stress.sh[ \t]+-h',
        r'^usage:[ \t]+power_cycle_stress.sh[ \t]+\[-h\][ \t]+\[-n <loop times>\]',
        r'^[ \t]*-h[ \t]+show this help message and exit',
        r'^[ \t]*-n[ \t]+set loop times'
    ]
    emmc_stress_option_h = [
        r'^usage:[ \t]+emmc_stress_test.sh[ \t]+\[-h\][ \t]+\[-n <loop times>\]',
        r'^[ \t]*-n[ \t]+set loop times'
    ]
    emmc_stress_pattern = [
        r'EMMC read_write stress:.*PASS'
    ]
    check_update_CPLD_SMB_image = [
        r'Upgrade successful.'
    ]
    check_update_cpld_h = [
        #r'#[ \t]*(\./)?cel-cpld_update[ \t]+-h',
        r'^Usage:[ \t]+\./cel-cpld_update[ \t]+-s.*?',
        r'CPLD_TYPE:.*?',
        r'img_file:[ \t]+Image\s+file\s+for\s+lattice\s+CPLD',
        r'options:',
        r'^[ \t]*hw:[ \t]+Program\s+the\s+CPLD\s+using\s+JTAG\s+hardware\s+mode',
        r'^[ \t]*sw:[ \t]+Program\s+the\s+CPLD\s+using\s+JTAG\s+software\s+mode'
    ]
    cel_sensor_test_h_pattern = [
        #r'#[ \t]*(\./)?cel-sensor-test[ \t]+-h$',
        r'^Usage:[ \t]+\./cel-sensor-test[ \t]+options.*?',
        r'^[ \t]*-h[ \t]+[S|s]how[ \t]+this[ \t]+help$',
        r'^[ \t]*-d[ \t]+show[ \t]+sensors[ \t]+data$',
        r'^[ \t]*-s[ \t]+get[ \t]+sensors[ \t]+status$',
        r'^[ \t]*-b[ \t]+specify[ \t]+the testing board',
        r'^[ \t]*-c[ \t]+check[ \t]+sensors[ \t]+status$',
        r'^[ \t]*-a[ \t]+Auto[ \t]+test$',
    ]
    cel_sensor_test_bc_pattern = [
        r'(get|check)_sensor_util_status[ \t]+.*?PASS'
    ]
    i2c_stress_option_h = [
        #r'#[ \t]*(\./)?i2c_stress.sh[ \t]+-h',
        r'^usage:[ \t]+i2c_stress.sh[ \t]+\[-h\][ \t]+\[-n <loop times>\]',
        r'^[ \t]*-h[ \t]+show this help message and exit',
        r'^[ \t]*-n[ \t]+set loop times'
    ]
    PSU_EEPROM_dict_h = [
        #r'#[ \t]*(\./)?cel-psu-test[ \t]+-h',
        r'^Usage:[ \t]+\./cel-psu-test[ \t]+options.*?',
        r'^[ \t]*-h[ \t]+.*?',
        r'^[ \t]*-i[ \t]+.*?',
        r'^[ \t]*-s[ \t]+.*?',
        r'^[ \t]*-a[ \t]+.*?',
    ]
    PSU_EEPROM_dict_a = [
        r'check_psu_status.*?PASS',
        r'check_psu_info.*?PASS'
    ]
    PSU_EEPROM_dict_i = 'FRU[ \t]+Information.*?'

    mp2_cel_software_test_v_pattern = [
        #r'#[ \t]*(\./)?cel-software-test[ \t]+-v[ \t]*$',
        r'^[ \t]*Diag[ \t]+version:' + SwImage.getSwImage(SwImage.DIAG).newVersion + r'[ \t]*$',
        # r'^[ \t]*' + str(SwImage.getSwImage(SwImage.BMC).newVersion).replace('.', r'.') + r'[ \t]*$',  # Now, this SwImage is not working now, skip first
        r'^BMC[ \t]+Version:[ \t]+' + str(SwImage.getSwImage(SwImage.BMC).newVersion).replace(".", ".0") + r'$',
        r'^[ \t]*FCM_B_CPLD[ \t]+:[ \t]+' + str(SwImage.getSwImage(SwImage.CPLD).newVersion["FCMCPLD B"]).replace('.', r'.') + r'[ \t]*$',
        r'^[ \t]*FCM_T_CPLD[ \t]+:[ \t]+' + str(SwImage.getSwImage(SwImage.CPLD).newVersion["FCMCPLD T"]).replace('.', r'.') + r'[ \t]*$',
        r'^[ \t]*SCM_CPLD[ \t]+:[ \t]+' + str(SwImage.getSwImage(SwImage.CPLD).newVersion["SCMCPLD"]).replace('.', r'.') + r'[ \t]*$',
        r'^[ \t]*SMB_CPLD[ \t]+:[ \t]+' + str(SwImage.getSwImage(SwImage.CPLD).newVersion["SMBCPLD"]).replace('.', r'.') + r'[ \t]*$',
        r'^[ \t]*PDB_L_CPLD[ \t]+:[ \t]+' + str(SwImage.getSwImage(SwImage.CPLD).newVersion["PWRCPLD L"]).replace('.', r'.') + r'[ \t]*$',
        r'^[ \t]*PDB_R_CPLD[ \t]+:[ \t]+' + str(SwImage.getSwImage(SwImage.CPLD).newVersion["PWRCPLD R"]).replace('.', r'.') + r'[ \t]*$',
        r'^[ \t]*SMB_IOB_FPGA[ \t]+:[ \t]+' + str(SwImage.getSwImage(SwImage.FPGA).newVersion["SMB_IOB_FPGA"]).replace('.', r'.') + r'[ \t]*$',
        r'^[ \t]*PIM1_DOM_FPGA[ \t]+:[ \t]+' + str(SwImage.getSwImage(SwImage.FPGA).newVersion["PIM1 DOMFPGA"]).replace('.', r'.') + r'[ \t]*$',
        r'^[ \t]*PIM2_DOM_FPGA[ \t]+:[ \t]+' + str(SwImage.getSwImage(SwImage.FPGA).newVersion["PIM2 DOMFPGA"]).replace('.', r'.') + r'[ \t]*$',
        r'^[ \t]*PIM3_DOM_FPGA[ \t]+:[ \t]+' + str(SwImage.getSwImage(SwImage.FPGA).newVersion["PIM3 DOMFPGA"]).replace('.', r'.') + r'[ \t]*$',
        r'^[ \t]*PIM4_DOM_FPGA[ \t]+:[ \t]+' + str(SwImage.getSwImage(SwImage.FPGA).newVersion["PIM4 DOMFPGA"]).replace('.', r'.') + r'[ \t]*$',
        r'^[ \t]*PIM5_DOM_FPGA[ \t]+:[ \t]+' + str(SwImage.getSwImage(SwImage.FPGA).newVersion["PIM5 DOMFPGA"]).replace('.', r'.') + r'[ \t]*$',
        r'^[ \t]*PIM6_DOM_FPGA[ \t]+:[ \t]+' + str(SwImage.getSwImage(SwImage.FPGA).newVersion["PIM6 DOMFPGA"]).replace('.', r'.') + r'[ \t]*$',
        r'^[ \t]*PIM7_DOM_FPGA[ \t]+:[ \t]+' + str(SwImage.getSwImage(SwImage.FPGA).newVersion["PIM7 DOMFPGA"]).replace('.', r'.') + r'[ \t]*$',
        r'^[ \t]*PIM8_DOM_FPGA[ \t]+:[ \t]+' + str(SwImage.getSwImage(SwImage.FPGA).newVersion["PIM8 DOMFPGA"]).replace('.', r'.') + r'[ \t]*$',
        r'^[ \t]*BIOS[ \t]+Version:[ \t]+' + SwImage.getSwImage(SwImage.SCM).newVersion["BIOS Version"] + r'[ \t]*$',
        r'^[ \t]*CPLD[ \t]+Version:[ \t]+' + SwImage.getSwImage(SwImage.SCM).newVersion["CPLD Version"] + r'[ \t]*$',
        r'^[ \t]*ME[ \t]+Version:[ \t]+' + str(SwImage.getSwImage(SwImage.SCM).newVersion["ME Version"]).replace('.', r'.') + r'[ \t]*$',
        r'^[ \t]*PVCCIN[ \t]+VR[ \t]+Version:[ \t]+' + str(SwImage.getSwImage(SwImage.SCM).newVersion["PVCCIN VR Version"]).replace('.', r'.') + r'[ \t]*$',
        r'^[ \t]*DDRAB[ \t]+VR[ \t]+Version:[ \t]+' + str(SwImage.getSwImage(SwImage.SCM).newVersion["DDRAB VR Version"]).replace('.', r'.') + r'[ \t]*$',
        r'^[ \t]*P1V05[ \t]+VR[ \t]+Version:[ \t]+' + str(SwImage.getSwImage(SwImage.SCM).newVersion["P1V05 VR Version"]).replace('.', r'.') + r'[ \t]*$',
    ]

    bios_version_pattern = r"[ \t]*BIOS[ \t]+Version:[ \t]+"

    cel_cmd_list = [
        'modprobe uio_pci_generic',
        'echo 1d9b 0011 > /sys/bus/pci/drivers/uio_pci_generic/new_id',
        './fpga reg w 0x18 0xffff0101'
    ]
    fpga_pass_pattern = 'pci_generic'

    pwmon_option_h_pattern = [
        #r'#[ \t]*(\./)?cel-pwmon-upgrade[ \t]+-h',
        r'Usage:',
        r'^[ \t]*cel-pwmon-upgrade[ \t]+\<op\>[ \t]+\<device\>[ \t]+\<\file\>',
        r'^[ \t]*\<op\>[ \t]+\:[ \t]+-r,[ \t]+-w',
        r'^[ \t]*\<ucd\s+device\>[ \t]+\:[ \t]+SMB_1,SMB_2,PIM_1\s+\~\s+PIM_8',
    ]
    check_fpga_h = [
        #r'#[ \t]*(\./)?fpga[ \t]+-h',
        r'^[ \t]*Minipack2 FPGA IO access tool',
        r'^[ \t]*Version:[ \t]+' + str(SwImage.getSwImage(SwImage.FPGA_DRIVER).newVersion) + r'[ \t]*$',
        r'Usage:[ \t]+fpga[ \t]+\[reg\|i2c\|spi\|scm\|smb\|pca\|qsfp\|obo\].*?'
    ]
    cel_fpga_sLPC = {
        'bin_tool' : './fpga'
    }
    cel_sLPC_test = [
        r'failed',
        r'error'
    ]
    bic_stress_option_h = [
        #r'#[ \t]*(\./)?BIC_stress.sh[ \t]+-h',
        r'^usage:[ \t]+BIC_stress.sh[ \t]+\[-h\][ \t]+\[-n <loop times>\]',
        r'^[ \t]*-h[ \t]+show this help message and exit',
        r'^[ \t]*-n[ \t]+set loop times'
    ]

    #### FB_DIAG_COMM_TC_042_IOB_FPGA_RESET_HOT_PLUG_TEST ####
    mp2_lspci_device_lists = [
        ('8086', '6f81'),
        ('8086', '6f36'),
        ('8086', '6f37'),
        ('8086', '6f76'),
        ('8086', '6fe0'),
        ('8086', '6fe1'),
        ('8086', '6fe2'),
        ('8086', '6fe3'),
        ('8086', '6ff8'),
        ('8086', '6ffc'),
        ('8086', '6ffd'),
        ('8086', '6ffe'),
        ('8086', '6f1d'),
        ('8086', '6f34'),
        ('8086', '6f1e'),
        ('8086', '6f7d'),
        ('8086', '6f1f'),
        ('8086', '6fa0'),
        ('8086', '6f30'),
        ('8086', '6fa8'),
        ('8086', '6f71'),
        ('8086', '6faa'),
        ('8086', '6fab'),
        ('8086', '6fac'),
        ('8086', '6fad'),
        ('8086', '6fae'),
        ('8086', '6faf'),
        ('8086', '6fb0'),
        ('8086', '6fb1'),
        ('8086', '6fb2'),
        ('8086', '6fb3'),
        ('8086', '6fbc'),
        ('8086', '6fbd'),
        ('8086', '6fbe'),
        ('8086', '6fbf'),
        ('8086', '6fb4'),
        ('8086', '6fb5'),
        ('8086', '6fb6'),
        ('8086', '6fb7'),
        ('8086', '6f98'),
        ('8086', '6f99'),
        ('8086', '6f9a'),
        ('8086', '6fc0'),
        ('8086', '6f9c'),
        ('8086', '6f88'),
        ('8086', '6f8a'),
        ('8086', '6f00'),
        ('8086', '6f50'),
        ('8086', '6f51'),
        ('8086', '6f52'),
        ('8086', '6f53'),
        ('8086', '15ab'),
        ('14e4', 'b990'),
        ('1344', '5410'),
        ('1d9b', '0011'),
        #('8086', '6f28'),
        #('8086', '6f29'),
        #('8086', '6f2a'),
        #('8086', '6f2c'),
        #('8086', '8c31'),
        #('8086', '8c3a'),
        #('8086', '8c3b'),
        #('8086', '1533'),
        #('8086', '8c26'),
        #('8086', '8c54'),
        #('8086', '8c22'),
        #('8086', '8c24'),
    ]

    # A list of where is the address are allowed to change
    mp2_tc042_i2cdump_changes = [
        "0x16", "0x17", "0xfe"
    ]

    mp2_fpga_ver_pattern = [
        #r"[ \t]*(\./)?fpga[ \t]+ver[ \t]*$",
        r"[ \t]*FPGA[ \t]+driver[ \t]+version:[ \t]+" + str(SwImage.getSwImage(SwImage.FPGA_DRIVER).newVersion).replace('.', r'.') + r"[ \t]*$",
        r"[ \t]*FPGA[ \t]+IOB[ \t]+" + str(SwImage.getSwImage(SwImage.FPGA).newVersion["SMB_IOB_FPGA"]).replace('.', r'.') + r"[ \t]*$",
        r"[ \t]*PIM[ \t]+1[ \t]+DOM:[ \t]+" + str(SwImage.getSwImage(SwImage.FPGA).newVersion["PIM1 DOMFPGA"]).replace('.', r'.') +r'.*?',
        r"[ \t]*PIM[ \t]+2[ \t]+DOM:[ \t]+" + str(SwImage.getSwImage(SwImage.FPGA).newVersion["PIM2 DOMFPGA"]).replace('.', r'.') + r'.*?',
        r"[ \t]*PIM[ \t]+3[ \t]+DOM:[ \t]+" + str(SwImage.getSwImage(SwImage.FPGA).newVersion["PIM3 DOMFPGA"]).replace('.', r'.') + r'.*?',
        r"[ \t]*PIM[ \t]+4[ \t]+DOM:[ \t]+" + str(SwImage.getSwImage(SwImage.FPGA).newVersion["PIM4 DOMFPGA"]).replace('.', r'.') + r'.*?',
        r"[ \t]*PIM[ \t]+5[ \t]+DOM:[ \t]+" + str(SwImage.getSwImage(SwImage.FPGA).newVersion["PIM5 DOMFPGA"]).replace('.', r'.') + r'.*?',
        r"[ \t]*PIM[ \t]+6[ \t]+DOM:[ \t]+" + str(SwImage.getSwImage(SwImage.FPGA).newVersion["PIM6 DOMFPGA"]).replace('.', r'.') + r'.*?',
        r"[ \t]*PIM[ \t]+7[ \t]+DOM:[ \t]+" + str(SwImage.getSwImage(SwImage.FPGA).newVersion["PIM7 DOMFPGA"]).replace('.', r'.') + r'.*?',
        r"[ \t]*PIM[ \t]+8[ \t]+DOM:[ \t]+" + str(SwImage.getSwImage(SwImage.FPGA).newVersion["PIM8 DOMFPGA"]).replace('.', r'.') + r'.*?',
    ]
    mp2_fpga_ver_pattern_dc = [
        # r"[ \t]*(\./)?fpga[ \t]+ver[ \t]*$",
        r"[ \t]*FPGA[ \t]+driver[ \t]+version:[ \t]+" + str(SwImage.getSwImage(SwImage.FPGA_DRIVER).newVersion).replace('.', r'.') + r"[ \t]*$",
        r"[ \t]*FPGA[ \t]+IOB[ \t]+" + str(SwImage.getSwImage(SwImage.FPGA).newVersion["SMB_IOB_FPGA"]).replace('.',r'.') + r"[ \t]*$",
        r"[ \t]*PIM[ \t]+1[ \t]+DOM:[ \t]+" + str(SwImage.getSwImage(SwImage.FPGA).newVersion["PIM1 DOMFPGA"]).replace('.', r'.') + r'.*?',
        r"[ \t]*PIM[ \t]+2[ \t]+DOM:[ \t]+" + str(SwImage.getSwImage(SwImage.FPGA).newVersion["PIM2 DOMFPGA"]).replace('.', r'.') + r'.*?',
        r"[ \t]*PIM[ \t]+7[ \t]+DOM:[ \t]+" + str(SwImage.getSwImage(SwImage.FPGA).newVersion["PIM7 DOMFPGA"]).replace('.', r'.') + r'.*?',
        r"[ \t]*PIM[ \t]+8[ \t]+DOM:[ \t]+" + str(SwImage.getSwImage(SwImage.FPGA).newVersion["PIM8 DOMFPGA"]).replace('.', r'.') + r'.*?',
    ]
    cel_tpm_test_device_a_pattern = [
        r'^[ \t]*show_TPM_Info.*PASS',
        r'^[ \t]*check_TPM_Info.*PASS',
    ]
    #cel_tpm_test_device_c_pattern = [
    #    r'TPM device path:',
    #    r'Get.*?SPI.*?TPM_PT_MANUFACTURER:',
    #    r'Expect.*?SPI.*?TPM_PT_MANUFACTURER:'
    #]
    cel_tpm_test_device_c_pattern = [
        r'Get /dev/tpmrm.*chip id: .*'
    ]
    cel_software_test_h_pattern = [
        #r'#[ \t]*(\./)?cel-software-test[ \t]+-h$',
        #r'^Usage:[ \t]+\./cel-software-test options[ \t]+\(-h\|-v\|-a\)$',
        r'^[ \t]*-h',
        r'^[ \t]*-v',
        r'^[ \t]*-a',
    ]

    mp2_fpga_h =[
        #r"(?m)[ \t]*(\./)?fpga[ \t]+-h[ \t]*$",
        r"(?m)^\s*$",
        r"(?m)^[ \t]*Minipack2[ \t]FPGA[ \t]+IO[ \t]+access[ \t]+tool[ \t]*$",
        r"(?m)^[ \t]*Version:[ \t]+" + str(SwImage.getSwImage(SwImage.FPGA_DRIVER).newVersion).replace('.', r'.') + r"[ \t]*$",
        r"(?m)^\s*$",
        r"(?m)^[ \t]*Usage:[ \t]+fpga[ \t]+\[reg\|i2c\|spi\|scm\|smb\|pca\|qsfp\|obo\][ \t]+<...>[ \t]*$",
        r"(?m)^[ \t]*\(Ranges:[ \t]+port[ \t]+\[1,8\]\)[ \t]*$",
        r"(?m)^[ \t]*-h[ \t]+Help,[ \t]+show[ \t]+this[ \t]help[ \t]+information[ \t]*$",
        r"(?m)^[ \t]*-v[ \t]+Verbose,[ \t]+dump[ \t]+IO[ \t]+offset[ \t]*$",
        r"(?m)^[ \t]*-s[ \t]+<time>[ \t]*$",
        r"(?m)^[ \t]*--[ \t]+sleep[ \t]+time[ \t]+in[ \t]+microseconds[ \t]*$",
        r"(?m)^[ \t]*-t[ \t]+<time>[ \t]*$",
        r"(?m)^[ \t]*--[ \t]+timeout[ \t]+in[ \t]+microseconds[ \t]*$",
        r"(?m)^[ \t]*-r[ \t]+<num>[ \t]*$",
        r"(?m)^[ \t]*--[ \t]+repeat[ \t]+num[ \t]+times,[ \t]+for[ \t]+load[ \t]testing[ \t]*$",
        r"(?m)^[ \t]*ver\[sion\][ \t]+--[ \t]+show[ \t]+driver[ \t]+and[ \t]+FPGA[ \t]+versions[ \t]*$",
        r"(?m)^[ \t]*reg[ \t]+<r\|w>\[width\*len\][ \t]+offset[ \t]+\[data_to_write[ \t]+\.\.\.\][ \t]*$",
        r"(?m)^[ \t]*--[ \t]+direct[ \t]+full[ \t]+FPGA[ \t]+scope[ \t]+register[ \t]+access[ \t]*$",
        r"(?m)^[ \t]*repeat[ \t]+in[ \t]+loops[ \t]+for[ \t]+PCIe[ \t]+load[ \t]+tests[ \t]*$",
        r"(?m)^[ \t]*iob[ \t]+\[r\|w>\[width\*len\][ \t]+offset[ \t]+\[data_to_write[ \t]+\.\.\.\][ \t]*$",
        r"(?m)^[ \t]*--[ \t]+iob[ \t]+register[ \t]+block[ \t]*$",
        r"(?m)^[ \t]*pim[ \t]+<r\|w>\[width\*len\][ \t]+pim=<#>[ \t]+offset[ \t]+\[data_to_write[ \t]+\.\.\.\][ \t]*$",
        r"(?m)^[ \t]*--[ \t]+per-PIM[ \t]+register[ \t]+block[ \t]*$",
        r"(?m)^[ \t]*c\[config\][ \t]+pim=<#>[ \t]+dom_collect[ \t]+<on\|off>[ \t]*$",
        r"(?m)^[ \t]*s\[tatus\][ \t]+pim=<#>[ \t]*$",
        r"(?m)^[ \t]*mdio[ \t]+<r\|w>[ \t]+pim=<#>[ \t]+\[type=0x[0-9a-f]{2}\][ \t]+phy=<#>[ \t]+<start>[ \t]+<len>[ \t]+\[data_to_write[ \t]+\.\.\.\][ \t]*$",
        r"(?m)^[ \t]*--[ \t]+mdio[ \t]+access[ \t]*$",
        r"(?m)^[ \t]*--[ \t]+if[ \t]+type=0x[0-9a-f]{2},[ \t]+the[ \t]+access[ \t]+mode[ \t]+is[ \t]+32-bit[ \t]+indirect[ \t]+\(\d*\)[ \t]*$",
        r"(?m)^[ \t]*i2c[ \t]+<r\|w>[ \t]+pim=<#>[ \t]+rtc=<#>[ \t]+desc=<#>[ \t]+chan=<#>[ \t]+bank=<#>[ \t]+page=<#>[ \t]+<start>[ \t]+<byte_len>[ \t]+\[byte_to_write[ \t]+\.\.\.\][ \t]*$",
        r"(?m)^[ \t]*--[ \t]+qsfp[ \t]+i2c[ \t]+bus[ \t]+access,[ \t]+byte_len[ \t]+in[ \t]+\[\d*,\d*\][ \t]*$",
        r"(?m)^[ \t]*spi[ \t]+<r\|w>[ \t]+pim=<#>[ \t]+rtc=<#>[ \t]+desc=<#>[ \t]+chan=<#>[ \t]+bank=<#>[ \t]+page=<#>[ \t]+<start>[ \t]+<byte_len>[ \t]+\[byte_to_write[ \t]+\.\.\.\][ \t]*$",
        r"(?m)^[ \t]*--[ \t]+obo[ \t]+spi[ \t]+bus[ \t]+access,[ \t]+byte_len[ \t]+in[ \t]+\[\d*,\d*\][ \t]*$",
        r"(?m)^[ \t]*scm[ \t]+<r\|w>[ \t]+offset[ \t]+\[data_to_write\][ \t]*$",
        r"(?m)^[ \t]*smb[ \t]+<r\|w>[ \t]+offset[ \t]+\[data_to_write\][ \t]*$",
        r"(?m)^[ \t]*pca[ \t]+<r\|w>[ \t]+offset[ \t]+\[data_to_write\][ \t]*$",
        r"(?m)^[ \t]*qsfp[ \t]+<s\[tatus\]\|c\[onfig\]\|d\[ata\]>[ \t]+\[port=<#>\][ \t]*$",
        r"(?m)^[ \t]*s\[tatus\][ \t]+--[ \t]+show[ \t]+qsfp[ \t]+status[ \t]*$",
        r"(?m)^[ \t]*c\[onfig\][ \t]+reset[ \t]+<on\|off>[ \t]*$",
        r"(?m)^[ \t]*lpmode[ \t]+<on\|off>[ \t]*$",
        r"(?m)^[ \t]*d\[data\][ \t]+--[ \t]+dump[ \t]+qsfp[ \t]+data[ \t]+block[ \t]*$",
        r"(?m)^[ \t]*--[ \t]+if[ \t]+port[ \t]+is[ \t]+not[ \t]+specified,[ \t]+select[ \t]+all[ \t]+ports[ \t]*$",
    ]

    mp2_fpga_scm_r_0_to_4 = [
        r"(?m)^[ \t]*0{5}0:[ \t]+\d{2}[ \t]*$",
        r"(?m)^[ \t]*0{5}1:[ \t]+\d{2}[ \t]*$",
        r"(?m)^[ \t]*0{5}2:[ \t]+\d{2}[ \t]*$",
        r"(?m)^[ \t]*0{5}3:[ \t]+\d{2}[ \t]*$",
    ]
    #### FB_DIAG_091_Lpmode_test ####
    lpmode_script_file = ['Lpmode_test.sh']
    UNIT_LPMODE_TOOL_PATH = '/usr/local/cls_diag/utility/stress/Lpmode'
    #### FB_DIAG_COMM_TC_096_BIC_stress_test ####
    bic_script_file = ['BIC_stress.sh']
    bic_script_file_dc = ['BIC_stress_dc.sh']
    BIC_SCRIPT_PATH = '/home/automation/Auto_Test/automation/FB-Minipack2/autotest/tools'
    UNIT_BIC_TOOL_PATH = '/mnt/data1/BMC_Diag/utility/stress/BIC_stress'
    UNIT_BIC_TOOL_PATH_DC = '/mnt/data1/BMC_Diag/utility/stress/BIC_stress/BIC_stress.sh'
    #### FB_DIAG_COMM_TC_097_I2C_stress_test ####
    I2C_SLEEP_CMD = "sed -i '/cel-i2c-test -b BMC -s/isleep 3' i2c_stress.sh ; sed -i '/cel-i2c-test -b BMC -s/asleep 3' i2c_stress.sh ; sed -i '/cel-i2c-test -b PIM6/isleep 3' i2c_stress.sh ; sed -i '/cel-i2c-test -b PIM6/asleep 3' i2c_stress.sh"
elif "wedge400c_dc" in devicename.lower():
    #### TC_047 ####
    cel_tpm_test_device_a_pattern = [
        r'^[ \t]*show_TPM_Info.*PASS',
        r'^[ \t]*check_TPM_Info.*PASS',
    ]
    fw_util_version = [
        r'^[ \t]*BMC[ \t]+Version:.*?',
        r'^[ \t]*Fan[ \t]+Speed[ \t]+.*?',
        r'^[ \t]*FCMCPLD:[ \t]+' + str(SwImage.getSwImage(SwImage.CPLD).newVersion["fcm"]).replace(".", "\."),
        r'^[ \t]*PWRCPLD:[ \t]+' + str(SwImage.getSwImage(SwImage.CPLD).newVersion["pwr"]).replace(".", "\."),
        r'^[ \t]*SCMCPLD:[ \t]+' + str(SwImage.getSwImage(SwImage.CPLD).newVersion["scm"]).replace(".", "\."),
        r'^[ \t]*SMBCPLD:[ \t]+' + str(SwImage.getSwImage(SwImage.CPLD).newVersion["smb"]).replace(".", "\."),
        r'^[ \t]*DOMFPGA1:[ \t]+' + str(SwImage.getSwImage(SwImage.FPGA).newVersion["DOMFPGA1"]).replace(".", "\."),
        r'^[ \t]*DOMFPGA2:[ \t]+' + str(SwImage.getSwImage(SwImage.FPGA).newVersion["DOMFPGA2"]).replace(".", "\."),
    ]
elif "wedge400c" in devicename.lower():

    fw_util_version = [
        r'^[ \t]*BMC[ \t]+Version:.*?',
        r'^[ \t]*Fan[ \t]+Speed[ \t]+.*?',
        r'^[ \t]*FCMCPLD:[ \t]+' + str(SwImage.getSwImage(SwImage.CPLD).newVersion["fcm"]).replace(".", "\."),
        r'^[ \t]*PWRCPLD:[ \t]+' + str(SwImage.getSwImage(SwImage.CPLD).newVersion["pwr"]).replace(".", "\."),
        r'^[ \t]*SCMCPLD:[ \t]+' + str(SwImage.getSwImage(SwImage.CPLD).newVersion["scm"]).replace(".", "\."),
        r'^[ \t]*SMBCPLD:[ \t]+' + str(SwImage.getSwImage(SwImage.CPLD).newVersion["smb"]).replace(".", "\."),
        r'^[ \t]*DOMFPGA1:[ \t]+' + str(SwImage.getSwImage(SwImage.FPGA).newVersion["DOMFPGA1"]).replace(".", "\."),
        r'^[ \t]*DOMFPGA2:[ \t]+' + str(SwImage.getSwImage(SwImage.FPGA).newVersion["DOMFPGA2"]).replace(".", "\."),
    ]

    cpld_option_a = [
        #r'#[ \t]*(\./)?cel-cpld-test[ \t]+-a',
        r'^check_cpld_scratch[ \t]+.*PASS',
        r'^show_CPLD_version[ \t]+.*PASS',
        r'^check_cpld_jtag[ \t]+.*PASS'
    ]
    diag_install_pattern = [
        r'Updating(.*?)+installing',
        # r'success[ \t]+install[ \t]+CPU Diag',
        r'success[ \t]+install[ \t]+BMC_Diag',
    ]
    cel_tpm_test_device_a_pattern = [
        r'^[ \t]*check_TPM2_I2C_VID_DID.*PASS',
        r'^[ \t]*show_TPM_Info.*PASS',
        r'^[ \t]*check_TPM_Info.*PASS',
    ]
    show_version_array = {
        "diag_version": SwImage.getSwImage(SwImage.DIAG).newVersion,
        "os_version": SwImage.getSwImage(SwImage.OS).newVersion,
        "kernel_version": SwImage.getSwImage(SwImage.KERNEL).newVersion,
        "bmc_version": str(SwImage.getSwImage(SwImage.BMC).newVersion).replace(".", ".0"),
        # OpenBMC shows m.n and DIAG shows m.0n
        "bios_version": SwImage.getSwImage(SwImage.BIOS).newVersion,
        "fpga1_version": SwImage.getSwImage(SwImage.FPGA).newVersion["DOMFPGA1"],
        "fpga2_version": SwImage.getSwImage(SwImage.FPGA).newVersion["DOMFPGA2"],
        "scm_cpld_version": str(SwImage.getSwImage(SwImage.CPLD).newVersion["scm"]),
        "smb_cpld_version": SwImage.getSwImage(SwImage.CPLD).newVersion["smb"],
        "i2c_fw_version": SwImage.getSwImage(SwImage.I210).newVersion,
    }

    ##### TC-1105-FPGA-UPDATE-TEST #####
    fpga_upgrade_file = SwImage.getSwImage(SwImage.FPGA).newImage
    fpga_downgrade_file = SwImage.getSwImage(SwImage.FPGA).oldImage
    fpga_package_copy_list = [fpga_upgrade_file, fpga_downgrade_file]
    fpga_upgrade_ver = SwImage.getSwImage(SwImage.FPGA).newVersion["DOMFPGA1"]
    fpga_downgrade_ver = SwImage.getSwImage(SwImage.FPGA).oldVersion["DOMFPGA1"]

    #### FB-DIAG-COM-TS-057-FPGA-UPGRADE-STRESS-TEST ####
    verify_fpga_ver_sh_downgrade_pattern = [
        r'fpga_ver\.sh',
        r'^[ \t]*DOMFPGA1:[ \t]+' + str(SwImage.getSwImage(SwImage.FPGA).oldVersion["DOMFPGA1"]).replace(".", "\."),
        r'^[ \t]*DOMFPGA2:[ \t]+' + str(SwImage.getSwImage(SwImage.FPGA).oldVersion["DOMFPGA1"]).replace(".", "\."),
    ]

    verify_fpga_ver_sh_upgrade_pattern = [
        r'fpga_ver\.sh',
        r'^[ \t]*DOMFPGA1:[ \t]+' + str(SwImage.getSwImage(SwImage.FPGA).newVersion["DOMFPGA1"]).replace(".", "\."),
        r'^[ \t]*DOMFPGA2:[ \t]+' + str(SwImage.getSwImage(SwImage.FPGA).newVersion["DOMFPGA2"]).replace(".", "\."),
    ]

    ##### TC-1107-FCM-UPDATE-TEST #####
    fcm_upgrade_ver = SwImage.getSwImage(SwImage.CPLD).newVersion["fcm"]
    fcm_downgrade_ver = SwImage.getSwImage(SwImage.CPLD).oldVersion["fcm"]

    ##### TC-1108-SCM-UPDATE-TEST #####
    scm_upgrade_ver = SwImage.getSwImage(SwImage.CPLD).newVersion["scm"]
    scm_downgrade_ver = str(SwImage.getSwImage(SwImage.CPLD).oldVersion["scm"]).replace("f", "15")

    ##### TC-1109-SYSTEM-UPDATE-TEST #####
    smb_upgrade_ver = SwImage.getSwImage(SwImage.CPLD).newVersion["smb"]
    smb_downgrade_ver = SwImage.getSwImage(SwImage.CPLD).oldVersion["smb"]

    ##### TC-1110-POWER-UPDATE-TEST #####
    pwr_upgrade_ver = SwImage.getSwImage(SwImage.CPLD).newVersion["pwr"]
    pwr_downgrade_ver = SwImage.getSwImage(SwImage.CPLD).oldVersion["pwr"]

elif "wedge400_" in devicename.lower():
    cel_tpm_test_device_a_pattern = [
        r'^[ \t]*show_TPM_Info.*PASS',
        r'^[ \t]*check_TPM_Info.*PASS',
    ]

    #### TC_005 ####
    usb_info_array = {
        "Vendor": "[a-zA-Z0-9_. ]+",
        "Product": "[a-zA-Z0-9_. ]+",
        "Revision": "[a-zA-Z0-9_. ]+",
        "User Capacity": ".*?GB",
        "Logical block size": "\d+ bytes",
        "SMART Health Status": "OK"
    }

    #### TC_006 ####
    rtc_test_p2 = '\w{3}\s(\w+)\s+(\d)\s([\d:]+)\s(\d{4})'

    #### TC_008 ####
    fw_util_version = [
        r'^[ \t]*BMC[ \t]+Version:.*?',
        r'^[ \t]*Fan[ \t]+Speed[ \t]+.*?',
        r'^[ \t]*FCMCPLD:[ \t]+' + str(SwImage.getSwImage(SwImage.CPLD).newVersion["fcm"]).replace(".", "\."),
        r'^[ \t]*PWRCPLD:[ \t]+' + str(SwImage.getSwImage(SwImage.CPLD).newVersion["pwr"]).replace(".", "\."),
        r'^[ \t]*SCMCPLD:[ \t]+' + str(SwImage.getSwImage(SwImage.CPLD).newVersion["scm"]).replace(".", "\."),
        r'^[ \t]*SMBCPLD:[ \t]+' + str(SwImage.getSwImage(SwImage.CPLD).newVersion["smb"]).replace(".", "\."),
        r'^[ \t]*DOMFPGA1:[ \t]+' + str(SwImage.getSwImage(SwImage.FPGA).newVersion["DOMFPGA1"]).replace(".", "\."),
        r'^[ \t]*DOMFPGA2:[ \t]+' + str(SwImage.getSwImage(SwImage.FPGA).newVersion["DOMFPGA2"]).replace(".", "\."),
    ]

    #### TC_050 ####
    high_power_sensor_a_pattern = [
        r'(get|check)_sensor_status.*?PASS',
        r'(get|check)_sensor_util_status.*?PASS'
    ]
    high_power_sensor_u_pattern = [
        r'(get|check)_sensor_util_status.*?PASS'
    ]
    
    #### TC_053 ####
    cel_software_test_i_or_v_pattern = [
        # r'cel-software-test[ \t]+-(i|v)$',
        r'^[ \t]*DIAG[ \t]+:[ \t]+.*?' + str(SwImage.getSwImage(SwImage.DIAG).newVersion).replace(".", "\."),
        r'^[ \t]*BMC[ \t]+:[ \t]+OpenBMC[ \n\t]+Release[ \t]+\w+-.*?',
        r'FPGA_1[ \t]+:[ \t]+' + str(SwImage.getSwImage(SwImage.FPGA).newVersion.get("DOMFPGA1", "")).replace(
            ".", "\."),
        r'FPGA_2[ \t]+:[ \t]+' + str(SwImage.getSwImage(SwImage.FPGA).newVersion.get("DOMFPGA2", "")).replace(
            ".", "\."),
        r'FCM_CPLD[ \t]+:[ \t]+' + str(SwImage.getSwImage(SwImage.CPLD).newVersion.get("fcm", "")).replace(".", "\."),
        r'SCM_CPLD[ \t]+:[ \t]+' + str(SwImage.getSwImage(SwImage.CPLD).newVersion.get("scm", "")).replace(".", "\."),
        r'SMB_CPLD[ \t]+:[ \t]+' + str(SwImage.getSwImage(SwImage.CPLD).newVersion.get("smb", "")).replace(".", "\."),
        r'^[ \\t]*(SMB_)?PWR_CPLD[ \t]+:[ \t]+' + str(
            SwImage.getSwImage(SwImage.CPLD).newVersion.get("pwr", "")).replace(".",
                                                                                "\."),
        r'^[ \t]*Bridge-IC[ \t]+Version:[ \n\t]+' + str(
            SwImage.getSwImage(SwImage.SCM).newVersion["Bridge-IC Version"]).replace(".", "\."),
        r'^[ \t]*BIOS[ \t]+Version:[ \n\t]+.*' + str(SwImage.getSwImage(SwImage.BIOS).newVersion).replace(".", "\."),
    ]

####################### CLOUDRIPPER #############################
devicename = os.environ.get("deviceName", "")
import logging
logging.info("devicename:{}".format(devicename))
if "cloudripper" in devicename.lower():
    high_power_sensor_u_pattern = [
        r'SMB_GB_HIGH_TEMP.*?C',
        r'SMB_GB_TEMP1.*?C',
        r'SMB_GB_TEMP2.*?C',
        r'SMB_GB_TEMP3.*?C',
        r'SMB_GB_TEMP4.*?C',
        r'SMB_GB_TEMP5.*?C',
        r'SMB_GB_TEMP6.*?C',
        r'SMB_GB_TEMP7.*?C',
        r'SMB_GB_TEMP8.*?C',
        r'SMB_GB_TEMP9.*?C',
        r'SMB_GB_TEMP10.*?C',
        r'(get|check)_sensor_util_status.*?PASS'
]
    high_power_sensor_a_pattern = [
        r'SMB_GB_HIGH_TEMP.*?C',
        r'SMB_GB_TEMP1.*?C',
        r'SMB_GB_TEMP2.*?C',
        r'SMB_GB_TEMP3.*?C',
        r'SMB_GB_TEMP4.*?C',
        r'SMB_GB_TEMP5.*?C',
        r'SMB_GB_TEMP6.*?C',
        r'SMB_GB_TEMP7.*?C',
        r'SMB_GB_TEMP8.*?C',
        r'SMB_GB_TEMP9.*?C',
        r'SMB_GB_TEMP10.*?C',
        r'SMB_GB_HBM_TEMP1.*?C',
        r'SMB_GB_HBM_TEMP2.*?C',
        r'(get|check)_sensors_status.*?PASS',
        r'(get|check)_sensor_util_status.*?PASS'
]
    high_power_sensor_s_pattern = [
        r'SMB_GB_TEMP1.*?C',
        r'SMB_GB_TEMP2.*?C',
        r'SMB_GB_TEMP3.*?C',
        r'SMB_GB_TEMP4.*?C',
        r'SMB_GB_TEMP5.*?C',
        r'SMB_GB_TEMP6.*?C',
        r'SMB_GB_TEMP7.*?C',
        r'SMB_GB_TEMP8.*?C',
        r'SMB_GB_TEMP9.*?C',
        r'SMB_GB_TEMP10.*?C',
        r'SMB_GB_HBM_TEMP1.*?C',
        r'SMB_GB_HBM_TEMP2.*?C',
        r'SMB_GB_HIGH_TEMP.*?C'
]

    cloudripper_cel_psu_test_s_pattern = [
        r'[ \t]*PSU1\s+Present\s+:[ \t]+OK$',
        r'[ \t]*PSU1\s+ACOK\s+:[ \t]+OK$',
        r'[ \t]*PSU1\s+DCOK\s+:[ \t]+OK$',
        r'[ \t]*PSU2\s+Present\s+:[ \t]+OK$',
        r'[ \t]*PSU2\s+ACOK\s+:[ \t]+OK$',
        r'[ \t]*PSU2\s+DCOK\s+:[ \t]+OK$'
    ]

    cel_tpm_test_device_i_pattern = [
        #r'#[ \t]*(\./)?cel-TPM-test[ \t]+-i',
        r'^[ \t]+TPM[ \t]+SPI[ \t]+VID\:.*?',
        r'^[ \t]+TPM[ \t]+SPI[ \t]+DID\:.*?',
        r'^[ \t]+TPM[ \t]+I2C[ \t]+VID\:.*?',
    ]
    cel_tpm_test_device_a_pattern = [
        r'^[ \t]*check_TPM_Info.*PASS',
        r'^[ \t]*show_TPM_Info.*PASS',
        r'^[ \t]*check_TPM2_I2C_VID_DID.*PASS'
    ]
    bmc_eeprom_option_h_pattern = [
        #r'#[ \t]*(\./)?eeprom_tool[ \t]+-h$',
        r'No EEPROM name',
        #r'^Usage:\s+\./eeprom_tool\s+options.*?',
        r'^[ \t]*-h',
        r'^[ \t]*-w',
        r'^[ \t]*-u',
        r'^[ \t]*-d',
        r'^[ \t]*-r',
        r'^[ \t]*-e',
    ]
    bmc_i2c_help_option_pattern = [
        r'cel-i2c-test\s+options.*?',
        r'-h[ \t]+print this help',
        r'-s',
        r'-l',
        r'-b',
        r'-a'
    ]

    ##### FB_DIAG_COMM_TC_016_E_Loopback_High_power_mode #####
    cel_e_loopback_help_arry = {
        'bin_tool' : 'hpmode',
        'option' : '200 0xA0 93 0x0C',
    }
    list_pass_pattern = ['Port #' + str(x) + ' set 0xA0 to offset 200 passed' for x in range(1, 33)]

    cel_version_test_h_or_help_pattern = [
        #r'^usage:\s+\./cel-version-test\s+\[OPTIONS\]',
        r'Options\s+are:',
        r'-S,[ \t]+--show[ \t]+Show[ \t]+FW[ \t]+info.',
        r'-h,[ \t]+--help[ \t]+Display[ \t]+this[ \t]+help[ \t]+text[ \t]+and[ \t]+exit'
        ]

    fw_util_version = [
        r'^[ \t]*BMC[ \t]+Version:.*?',
        r'^[ \t]*Fan[ \t]+Speed[ \t]+.*?',
     #   r'^[ \t]*FCMCPLD[ \t]+' + str(SwImage.getSwImage(SwImage.CPLD).newVersion["fcm"]).replace(".", "\."),
    #    r'^[ \t]*PWRCPLD[ \t]+' + str(SwImage.getSwImage(SwImage.CPLD).newVersion["pwr"]).replace(".", "\."),
        r'^[ \t]*SCMCPLD:[ \t]+' + str(SwImage.getSwImage(SwImage.CPLD).newVersion["scm"]).replace(".", "\."),
        r'^[ \t]*SMBCPLD:[ \t]+' + str(SwImage.getSwImage(SwImage.CPLD).newVersion["smb"]).replace(".", "\."),
        r'^[ \t]*DOMFPGA1:[ \t]+' + str(SwImage.getSwImage(SwImage.FPGA).newVersion["DOMFPGA1"]).replace(".", "\."),
        r'^[ \t]*DOMFPGA2:[ \t]+' + str(SwImage.getSwImage(SwImage.FPGA).newVersion["DOMFPGA2"]).replace(".", "\."),
    ]



####################### MINIPACK3 #############################

scp_ip = pc_info.managementIP
scp_username = pc_info.scpUsername
scp_password = pc_info.scpPassword
dhcp_username = pc_info.username
dhcp_password = pc_info.password
dhcp_prompt = pc_info.prompt

device_mgmt_ip = deviceObj.managementIP
device_user_name = deviceObj.rootUserName
#device_password = deviceObj.rootUserName
#device_prompt = deviceObj.loginPromptDiagOS


i2c_system_scan_pattern=[
 "TMP1075 Thermal sensor.*IOB CH12.*14.*0x4e.*PASS",
 "MCB EEPROM\s+IOB CH12\s+14\s+0x53.*PASS",
 "MCB CPLD FAN Control\s+IOB CH13\s+15\s+0x33.*PASS",
 "MCB CPLD MCB Control\s+IOB CH13\s+15\s+0x60.*PASS",
 "Fan1_HSC PTPS25990\s+IOB CH18\s+20\s+0x4c.*PASS",
 "Fan2_HSC PTPS25990\s+IOB CH19\s+21\s+0x4c.*PASS",
 "Fan3_HSC PTPS25990\s+IOB CH20\s+22\s+0x4c.*PASS",
 "Fan4_HSC PTPS25990\s+IOB CH21\s+23\s+0x4c.*PASS",
 "Fan5_HSC PTPS25990\s+IOB CH22\s+24\s+0x4c.*PASS",
 "Fan6_HSC PTPS25990\s+IOB CH23\s+25\s+0x4c.*PASS",
 "Fan7_HSC PTPS25990\s+IOB CH24\s+26\s+0x4c.*PASS",
 "Fan8_HSC PTPS25990\s+IOB CH25\s+27\s+0x4c.*PASS",
 "MCB ADC ADC128D818\s+IOB CH26\s+28\s+0x37.*PASS",
"\(y\) detect_mcb_i2c_device: Scanned 13 i2c devices, 0 failed.",

 "XDPE1A2G5B VDD_CORE\s+IOB CH3\s+5\s+0x76.*PASS",
 "SMB ADC1 ADC128D818\s+IOB CH6\s+8\s+0x1d.*PASS",
 "SMB ADC2 ADC128D818\s+IOB CH6\s+8\s+0x1f.*PASS",
 "TH5 SW ASIC\s+IOB CH7\s+9\s+0x44.*PASS",
 "SMB ADC3 ADC128D818\s+IOB CH8\s+10\s+0x35\s+PASS",
 "SMB CPLD\s+IOB CH9\s+11\s+0x33\s+PASS",
 "SMB CPLD OSFP\s+IOB CH9\s+11\s+0x3e\s+PASS",
 "SMB EEPROM\s+IOB CH9\s+11\s+0x50\s+PASS",
 "TRVDD_1 MP2975\s+IOB CH10\s+12\s+0x7d\s+PASS",
 "TRVDD_0 MP2975\s+IOB CH11\s+13\s+0x7b\s+PASS",
 "TMP1075 Thermal Sensor#1\s+DOM1 CH33\s+62\s+0x48\s+PASS",
 "TMP1075 Thermal Sensor#2\s+DOM1 CH33\s+62\s+0x49\s+PASS",
 "TMP1075 Thermal Sensor#3\s+DOM2 CH33\s+96\s+0x4a\s+PASS",
 "TMP1075 Thermal Sensor#4\s+DOM2 CH33\s+96\s+0x4b\s+PASS",
 "\(y\) detect_smb_i2c_device: Scanned 14 i2c devices, 0 failed",

 "PCA9548\s+IOB CH0\s+2\s+0x70\s+PASS",
 "PCA9546\s+IOB CH1\s+3\s+0x70\s+PASS",
 "SCM CPLD\s+IOB CH2\s+4\s+0x35\s+PASS",
 "ADM1278 Hot Swap\s+PCA9548 CH0\s+97\s+0x10\s+PASS",
 "LM75_#1 Thermal sensor\s+PCA9548 CH1\s+98\s+0x4c\s+PASS",
 "LM75_#2 Thermal sensor\s+PCA9548 CH1\s+98\s+0x4d\s+PASS",
 "SCM_ADC ADC128D818\s+PCA9548 CH2\s+99\s+0x37\s+PASS",
 "SCM FRU E2PROM#1\s+PCA9548 CH3\s+100\s+0x54\s+PASS",
 "88E6321 E2PROM\s+PCA9548 CH4\s+101\s+0x50\s+PASS",
 "PCIe Clk buffer #1 RC19004\s+PCA9548 CH6\s+103\s+0x6c\s+PASS",
 "PCIe Clk buffer #2 RC19004\s+PCA9548 CH6\s+103\s+0x6f\s+PASS",
"\(y\) detect_scm_i2c_device: Scanned 11 i2c devices, 0 failed.",

 "FCB_T EEPROM\s+IOB CH14\s+16\s+0x53\s+PASS",
 "FCB_T TMP1075#1\s+IOB CH15\s+17\s+0x49\s+PASS",
 "FCB_T TMP1075#2\s+IOB CH15\s+17\s+0x4b\s+PASS",
 "FCB_B TMP1075#1\s+IOB CH16\s+18\s+0x49\s+PASS",
 "FCB_B TMP1075#2\s+IOB CH16\s+18\s+0x4b\s+PASS",
"\(y\) detect_fcb_i2c_device: Scanned 5 i2c devices, 0 failed.",

"TMP1075 Thermal Sensor \s+IOB CH4\s+6\s+0x48\s+PASS",
 "PSU 1 FRU\s+IOB CH4\s+6\s+0x51\s+PASS", 
 "PSU 1 MCU\s+IOB CH4\s+6\s+0x59\s+PASS",
 "TMP1075 Thermal Sensor\s+IOB CH5\s+7\s+0x48\s+PASS",
 "PSU 2 FRU\s+IOB CH5\s+7\s+0x51\s+PASS",  
 "PSU 2 MCU\s+IOB CH5\s+7\s+0x59\s+PASS",  
"\(y\) detect_pdb_i2c_device: Scanned 6 i2c devices, 0 failed.",                                      

 "XP3R3V_LEFT MPS - MP2891 \s+DOM1 CH32\s+61\s+0x23\s+PASS",
 "TMP1075 Thermal Sensor   \s+DOM1 CH32\s+61\s+0x48\s+PASS",  
 "XP3R3V_RIGHT MPS - MP2891\s+DOM2 CH32\s+95\s+0x23\s+PASS", 
 "TMP1075 Thermal Sensor   \s+DOM2 CH32\s+95\s+0x48\s+PASS",  
"\(y\) detect_3v3_card_i2c_device: Scanned 4 i2c devices, 0 failed.",                                      

 "VNN_PCH\s+PCA9546 CH1\s+106\s+0x11\s+PASS",  
 "1V05_STBY\s+PCA9546 CH1\s+106\s+0x22\s+PASS",  
 "1V8_STBY\s+PCA9546 CH1\s+106\s+0x76\s+PASS",  
 "VDDQ\s+PCA9546 CH1\s+106\s+0x45\s+PASS",  
 "VCCANA_CPU\s+PCA9546 CH1\s+106\s+0x66\s+PASS",  
 "FRU\s+PCA9546 CH2\s+107\s+0x56\s+PASS",  
 "OUTLET Sensor\s+PCA9546 CH2\s+107\s+0x4a\s+PASS",  
 "INLET Sensor\s+PCA9546 CH2\s+107\s+0x48\s+PASS",  
"\(y\) detect_come_i2c_device: Scanned 8 i2c devices, 0 failed.",                                      

 "SCM FRU EEPROM#2\s+BMC CH4\s+3\s+0x56\s+PASS",  
 "PCA9555\s+BMC CH5\s+4\s+0x27\s+PASS",  
 "COMe CPU\s+BMC CH6\s+5\s+0x16\s+PASS",  
 "FCB_B EEPROM\s+BMC CH7\s+6\s+0x53\s+PASS",  
 "BMC EEPROM\s+BMC CH9\s+8\s+0x51\s+PASS",  
 "LM75 Thermal Sensor \s+BMC CH9\s+8\s+0x51\s+PASS",  
 "MCB CPLD MCB Control\s+BMC CH13\s+12\s+ 0x60\s+PASS",  
 "IOB FPGA\s+BMC CH14\s+13\s+ 0x35\s+PASS",  

]

system_spi_scan_test_pattern=[
    "IOB Flash\s+0\s+NA\s+ Micron\s+MT25QL128\s+16384 KB\s+PASS",
    "SCM Flash\s+6\s+1\s+Winbond\s+W25X20\s+256 KB\s+PASS",
   "I210 Flash\s+6\s+2\s+Winbond\s+W25Q32JV\s+4096 KB\s+PASS",
    "MCB Flash\s+3\s+3\s+Winbond\s+W25X20\s+256 KB\s+PASS",
    "SMB Flash\s+4\s+7\s+Winbond\s+W25X20\s+256 KB\s+PASS",
    "TH5 Flash\s+5\s+8\s+Micron/Numonyx/ST\s+N25Q256..1E\s+32768 KB\s+PASS ",
  "DOM_1 Flash\s+1\s+9\s+ Micron\s+MT25QL128\s+16384 KB\s+PASS",
  "DOM_2 Flash\s+2\s+10\s+ Micron\s+MT25QL128\s+16384 KB\s+PASS",
]
system_usb_network_test_pattern = [
"PING fe80::ff:fe00:1%usb0\(fe80::ff:fe00:1%usb0\) 56 data bytes",
"64 bytes from fe80::ff:fe00:1%usb0: icmp_seq=1 ttl=64 time=.*ms",
"64 bytes from fe80::ff:fe00:1%usb0: icmp_seq=2 ttl=64 time=.*ms",
"64 bytes from fe80::ff:fe00:1%usb0: icmp_seq=3 ttl=64 time=.*ms",
"--- fe80::ff:fe00:1%usb0 ping statistics ---",
"3 packets transmitted, 3 received, 0% packet loss, time .*ms",
"rtt min/avg/max/mdev = .*ms",
"\(y\) check_ping_usb0 : Ping command executing succeeded.",

]

system_pcie_scan_test_pattern = [
"Scanning I210 NIC:",
"TOTAL RESULT PASS",
"Scanning TH5 ASIC:",
"TOTAL RESULT PASS",
"Scanning NVMe SSD:",
"TOTAL RESULT PASS",
"Scanning IOB FPGA:",
"TOTAL RESULT PASS",
"\(y\) test_scan_pcie"

]

system_oob_test_pattern = [
"PING .*%eth0.4088.* 56 data bytes",
"64 bytes from .*%eth0.4088: icmp_seq=1 ttl=64 time=.* ms",
"64 bytes from .*%eth0.4088: icmp_seq=2 ttl=64 time=.* ms",
"64 bytes from .*%eth0.4088: icmp_seq=3 ttl=64 time=.* ms",

"--- .*%eth0.4088 ping statistics ---",
"3 packets transmitted, 3 received, 0% packet loss, time.*",
"\(y\) check_ping_network: OOB ping test passed.",
]



osfp_i2c_scan_pattern = [
"E1\s+YES\s+29\s+PASS\s+OSFP\s+ColorChip\s+T-100-O-ELB-300C", 
 "E2\s+YES\s+30\s+PASS\s+OSFP\s+ColorChip\s+T-100-O-ELB-300C", 
 "E3\s+YES\s+31\s+PASS\s+OSFP\s+ColorChip\s+T-100-O-ELB-300C", 
 "E4\s+YES\s+32\s+PASS\s+OSFP\s+ColorChip\s+T-100-O-ELB-300C", 
 "E5\s+YES\s+33\s+PASS\s+OSFP\s+ColorChip\s+T-100-O-ELB-300C", 
 "E6\s+YES\s+34\s+PASS\s+OSFP\s+ColorChip\s+T-100-O-ELB-300C", 
 "E7\s+YES\s+35\s+PASS\s+OSFP\s+ColorChip\s+T-100-O-ELB-300C", 
 "E8\s+YES\s+36\s+PASS\s+OSFP\s+ColorChip\s+T-100-O-ELB-300C", 
 "E9\s+YES\s+37\s+PASS\s+OSFP\s+ColorChip\s+T-100-O-ELB-300C", 
 "E10\s+YES\s+38\s+PASS\s+OSFP\s+ColorChip\s+T-100-O-ELB-300C", 
 "E11\s+YES\s+39\s+PASS\s+OSFP\s+ColorChip\s+T-100-O-ELB-300C", 
 "E12\s+YES\s+40\s+PASS\s+OSFP\s+ColorChip\s+T-100-O-ELB-300C", 
 "E13\s+YES\s+41\s+PASS\s+OSFP\s+ColorChip\s+T-100-O-ELB-300C", 
 "E14\s+YES\s+42\s+PASS\s+OSFP\s+ColorChip\s+T-100-O-ELB-300C", 
 "E15\s+YES\s+43\s+PASS\s+OSFP\s+ColorChip\s+T-100-O-ELB-300C", 
 "E16\s+YES\s+44\s+PASS\s+OSFP\s+ColorChip\s+T-100-O-ELB-300C", 
 "E17\s+YES\s+45\s+PASS\s+OSFP\s+ColorChip\s+T-100-O-ELB-300C", 
 "E18\s+YES\s+46\s+PASS\s+OSFP\s+ColorChip\s+T-100-O-ELB-300C", 
 "E19\s+YES\s+47\s+PASS\s+OSFP\s+ColorChip\s+T-100-O-ELB-300C", 
 "E20\s+YES\s+48\s+PASS\s+OSFP\s+ColorChip\s+T-100-O-ELB-300C", 
 "E21\s+YES\s+49\s+PASS\s+OSFP\s+ColorChip\s+T-100-O-ELB-300C", 
 "E22\s+YES\s+50\s+PASS\s+OSFP\s+ColorChip\s+T-100-O-ELB-300C", 
 "E23\s+YES\s+51\s+PASS\s+OSFP\s+ColorChip\s+T-100-O-ELB-300C", 
 "E24\s+YES\s+52\s+PASS\s+OSFP\s+ColorChip\s+T-100-O-ELB-300C", 
 "E25\s+YES\s+53\s+PASS\s+OSFP\s+ColorChip\s+T-100-O-ELB-300C", 
 "E26\s+YES\s+54\s+PASS\s+OSFP\s+ColorChip\s+T-100-O-ELB-300C", 
 "E27\s+YES\s+55\s+PASS\s+OSFP\s+ColorChip\s+T-100-O-ELB-300C", 
 "E28\s+YES\s+56\s+PASS\s+OSFP\s+ColorChip\s+T-100-O-ELB-300C", 
 "E29\s+YES\s+57\s+PASS\s+OSFP\s+ColorChip\s+T-100-O-ELB-300C", 
 "E30\s+YES\s+58\s+PASS\s+OSFP\s+ColorChip\s+T-100-O-ELB-300C", 
 "E31\s+YES\s+59\s+PASS\s+OSFP\s+ColorChip\s+T-100-O-ELB-300C", 
 "E32\s+YES\s+60\s+PASS\s+OSFP\s+ColorChip\s+T-100-O-ELB-300C", 
 "E33\s+YES\s+63\s+PASS\s+OSFP\s+ColorChip\s+T-100-O-ELB-300C", 
 "E34\s+YES\s+64\s+PASS\s+OSFP\s+ColorChip\s+T-100-O-ELB-300C", 
 "E35\s+YES\s+65\s+PASS\s+OSFP\s+ColorChip\s+T-100-O-ELB-300C", 
 "E36\s+YES\s+66\s+PASS\s+OSFP\s+ColorChip\s+T-100-O-ELB-300C", 
 "E37\s+YES\s+67\s+PASS\s+OSFP\s+ColorChip\s+T-100-O-ELB-300C", 
 "E38\s+YES\s+68\s+PASS\s+OSFP\s+ColorChip\s+T-100-O-ELB-300C", 
 "E39\s+YES\s+69\s+PASS\s+OSFP\s+ColorChip\s+T-100-O-ELB-300C", 
 "E40\s+YES\s+70\s+PASS\s+OSFP\s+ColorChip\s+T-100-O-ELB-300C", 
 "E41\s+YES\s+71\s+PASS\s+OSFP\s+ColorChip\s+T-100-O-ELB-300C", 
 "E42\s+YES\s+72\s+PASS\s+OSFP\s+ColorChip\s+T-100-O-ELB-300C", 
 "E43\s+YES\s+73\s+PASS\s+OSFP\s+ColorChip\s+T-100-O-ELB-300C", 
 "E44\s+YES\s+74\s+PASS\s+OSFP\s+ColorChip\s+T-100-O-ELB-300C", 
 "E45\s+YES\s+75\s+PASS\s+OSFP\s+ColorChip\s+T-100-O-ELB-300C", 
 "E46\s+YES\s+76\s+PASS\s+OSFP\s+ColorChip\s+T-100-O-ELB-300C", 
 "E47\s+YES\s+77\s+PASS\s+OSFP\s+ColorChip\s+T-100-O-ELB-300C", 
 "E48\s+YES\s+78\s+PASS\s+OSFP\s+ColorChip\s+T-100-O-ELB-300C", 
 "E49\s+YES\s+79\s+PASS\s+OSFP\s+ColorChip\s+T-100-O-ELB-300C", 
 "E50\s+YES\s+80\s+PASS\s+OSFP\s+ColorChip\s+T-100-O-ELB-300C", 
 "E51\s+YES\s+81\s+PASS\s+OSFP\s+ColorChip\s+T-100-O-ELB-300C", 
 "E52\s+YES\s+82\s+PASS\s+OSFP\s+ColorChip\s+T-100-O-ELB-300C", 
 "E53\s+YES\s+83\s+PASS\s+OSFP\s+ColorChip\s+T-100-O-ELB-300C", 
 "E54\s+YES\s+84\s+PASS\s+OSFP\s+ColorChip\s+T-100-O-ELB-300C", 
 "E55\s+YES\s+85\s+PASS\s+OSFP\s+ColorChip\s+T-100-O-ELB-300C", 
 "E56\s+YES\s+86\s+PASS\s+OSFP\s+ColorChip\s+T-100-O-ELB-300C", 
 "E57\s+YES\s+87\s+PASS\s+OSFP\s+ColorChip\s+T-100-O-ELB-300C", 
 "E58\s+YES\s+88\s+PASS\s+OSFP\s+ColorChip\s+T-100-O-ELB-300C", 
 "E59\s+YES\s+89\s+PASS\s+OSFP\s+ColorChip\s+T-100-O-ELB-300C", 
 "E60\s+YES\s+90\s+PASS\s+OSFP\s+ColorChip\s+T-100-O-ELB-300C", 
 "E61\s+YES\s+91\s+PASS\s+OSFP\s+ColorChip\s+T-100-O-ELB-300C", 
 "E62\s+YES\s+92\s+PASS\s+OSFP\s+ColorChip\s+T-100-O-ELB-300C", 
 "E63\s+YES\s+93\s+PASS\s+OSFP\s+ColorChip\s+T-100-O-ELB-300C", 
 "E64\s+YES\s+94\s+PASS\s+OSFP\s+ColorChip\s+T-100-O-ELB-300C", 
"\(y\) detect_osfp_i2c_device: OSFP/QSFP scan succeeded.",           

]

usb_ping_patetrn = "5 packets transmitted, 5 received, 0% packet loss"


ospf_ports_check_pattern = [
  "E1\s+YES",
  "E2\s+YES",
  "E3\s+YES",
  "E4\s+YES",
  "E5\s+YES",
  "E6\s+YES",
  "E7\s+YES",
  "E8\s+YES",
  "E9\s+YES",
  "E10\s+YES",
  "E11\s+YES",
  "E12\s+YES",
  "E13\s+YES",
  "E14\s+YES",
  "E15\s+YES",
  "E16\s+YES",
  "E17\s+YES",
  "E18\s+YES",
  "E19\s+YES",
  "E20\s+YES",
  "E21\s+YES",
  "E22\s+YES",
  "E23\s+YES",
  "E24\s+YES",
  "E25\s+YES",
  "E26\s+YES",
  "E27\s+YES",
  "E28\s+YES",
  "E29\s+YES",
  "E30\s+YES",
  "E31\s+YES",
  "E32\s+YES",
  "E33\s+YES",
  "E34\s+YES",
  "E35\s+YES",
  "E36\s+YES",
  "E37\s+YES",
  "E38\s+YES",
  "E39\s+YES",
  "E40\s+YES",
  "E41\s+YES",
  "E42\s+YES",
  "E43\s+YES",
  "E44\s+YES",
  "E45\s+YES",
  "E46\s+YES",
  "E47\s+YES",
  "E48\s+YES",
  "E49\s+YES",
  "E50\s+YES",
  "E51\s+YES",
  "E52\s+YES",
  "E53\s+YES",
  "E54\s+YES",
  "E55\s+YES",
  "E56\s+YES",
  "E57\s+YES",
  "E58\s+YES",
  "E59\s+YES",
  "E60\s+YES",
  "E61\s+YES",
  "E62\s+YES",
  "E63\s+YES",
  "E64\s+YES",
"\(y\) get_all_port_present_status: All OSFP ports are present\."
]


ospf_ports_reset_check_pattern=[
  "E1\s+Hold\s+0x1",
  "E2\s+Hold\s+0x1",
  "E3\s+Hold\s+0x1",
  "E4\s+Hold\s+0x1",
  "E5\s+Hold\s+0x1",
  "E6\s+Hold\s+0x1",
  "E7\s+Hold\s+0x1",
  "E8\s+Hold\s+0x1",
  "E9\s+Hold\s+0x1",
  "E10\s+Hold\s+0x1",
  "E11\s+Hold\s+0x1",
  "E12\s+Hold\s+0x1",
  "E13\s+Hold\s+0x1",
  "E14\s+Hold\s+0x1",
  "E15\s+Hold\s+0x1",
  "E16\s+Hold\s+0x1",
  "E17\s+Hold\s+0x1",
  "E18\s+Hold\s+0x1",
  "E19\s+Hold\s+0x1",
  "E20\s+Hold\s+0x1",
  "E21\s+Hold\s+0x1",
  "E22\s+Hold\s+0x1",
  "E23\s+Hold\s+0x1",
  "E24\s+Hold\s+0x1",
  "E25\s+Hold\s+0x1",
  "E26\s+Hold\s+0x1",
  "E27\s+Hold\s+0x1",
  "E28\s+Hold\s+0x1",
  "E29\s+Hold\s+0x1",
  "E30\s+Hold\s+0x1",
  "E31\s+Hold\s+0x1",
  "E32\s+Hold\s+0x1",
  "E33\s+Hold\s+0x1",
  "E34\s+Hold\s+0x1",
  "E35\s+Hold\s+0x1",
  "E36\s+Hold\s+0x1",
  "E37\s+Hold\s+0x1",
  "E38\s+Hold\s+0x1",
  "E39\s+Hold\s+0x1",
  "E40\s+Hold\s+0x1",
  "E41\s+Hold\s+0x1",
  "E42\s+Hold\s+0x1",
  "E43\s+Hold\s+0x1",
  "E44\s+Hold\s+0x1",
  "E45\s+Hold\s+0x1",
  "E46\s+Hold\s+0x1",
  "E47\s+Hold\s+0x1",
  "E48\s+Hold\s+0x1",
  "E49\s+Hold\s+0x1",
  "E50\s+Hold\s+0x1",
  "E51\s+Hold\s+0x1",
  "E52\s+Hold\s+0x1",
  "E53\s+Hold\s+0x1",
  "E54\s+Hold\s+0x1",
  "E55\s+Hold\s+0x1",
  "E56\s+Hold\s+0x1",
  "E57\s+Hold\s+0x1",
  "E58\s+Hold\s+0x1",
  "E59\s+Hold\s+0x1",
  "E60\s+Hold\s+0x1",
  "E61\s+Hold\s+0x1",
  "E62\s+Hold\s+0x1",
  "E63\s+Hold\s+0x1",
  "E64\s+Hold\s+0x1",
"\(y\) get_all_port_reset_status: All port reset status checked\."
]


ospf_ports_lpmode_check_lpmode_pattern = [
  "E1\s+NO\s+0x1",
  "E2\s+NO\s+0x1",
  "E3\s+NO\s+0x1",
  "E4\s+NO\s+0x1",
  "E5\s+NO\s+0x1",
  "E6\s+NO\s+0x1",
  "E7\s+NO\s+0x1",
  "E8\s+NO\s+0x1",
  "E9\s+NO\s+0x1",
  "E10\s+NO\s+0x1",
  "E11\s+NO\s+0x1",
  "E12\s+NO\s+0x1",
  "E13\s+NO\s+0x1",
  "E14\s+NO\s+0x1",
  "E15\s+NO\s+0x1",
  "E16\s+NO\s+0x1",
  "E17\s+NO\s+0x1",
  "E18\s+NO\s+0x1",
  "E19\s+NO\s+0x1",
  "E20\s+NO\s+0x1",
  "E21\s+NO\s+0x1",
  "E22\s+NO\s+0x1",
  "E23\s+NO\s+0x1",
  "E24\s+NO\s+0x1",
  "E25\s+NO\s+0x1",
  "E26\s+NO\s+0x1",
  "E27\s+NO\s+0x1",
  "E28\s+NO\s+0x1",
  "E29\s+NO\s+0x1",
  "E30\s+NO\s+0x1",
  "E31\s+NO\s+0x1",
  "E32\s+NO\s+0x1",
  "E33\s+NO\s+0x1",
  "E34\s+NO\s+0x1",
  "E35\s+NO\s+0x1",
  "E36\s+NO\s+0x1",
  "E37\s+NO\s+0x1",
  "E38\s+NO\s+0x1",
  "E39\s+NO\s+0x1",
  "E40\s+NO\s+0x1",
  "E41\s+NO\s+0x1",
  "E42\s+NO\s+0x1",
  "E43\s+NO\s+0x1",
  "E44\s+NO\s+0x1",
  "E45\s+NO\s+0x1",
  "E46\s+NO\s+0x1",
  "E47\s+NO\s+0x1",
  "E48\s+NO\s+0x1",
  "E49\s+NO\s+0x1",
  "E50\s+NO\s+0x1",
  "E51\s+NO\s+0x1",
  "E52\s+NO\s+0x1",
  "E53\s+NO\s+0x1",
  "E54\s+NO\s+0x1",
  "E55\s+NO\s+0x1",
  "E56\s+NO\s+0x1",
  "E57\s+NO\s+0x1",
  "E58\s+NO\s+0x1",
  "E59\s+NO\s+0x1",
  "E60\s+NO\s+0x1",
  "E61\s+NO\s+0x1",
  "E62\s+NO\s+0x1",
  "E63\s+NO\s+0x1",
  "E64\s+NO\s+0x1",
"\(y\) get_all_port_lpmod_status: All port lpmode status checked\."]

ospf_ports_lpmode_check_hpmode_pattern = ["E1\s+YES\s+0x0",
  "E2\s+YES\s+0x0",
  "E3\s+YES\s+0x0",
  "E4\s+YES\s+0x0",
  "E5\s+YES\s+0x0",
  "E6\s+YES\s+0x0",
  "E7\s+YES\s+0x0",
  "E8\s+YES\s+0x0",
  "E9\s+YES\s+0x0",
  "E10\s+YES\s+0x0",
  "E11\s+YES\s+0x0",
  "E12\s+YES\s+0x0",
  "E13\s+YES\s+0x0",
  "E14\s+YES\s+0x0",
  "E15\s+YES\s+0x0",
  "E16\s+YES\s+0x0",
  "E17\s+YES\s+0x0",
  "E18\s+YES\s+0x0",
  "E19\s+YES\s+0x0",
  "E20\s+YES\s+0x0",
  "E21\s+YES\s+0x0",
  "E22\s+YES\s+0x0",
  "E23\s+YES\s+0x0",
  "E24\s+YES\s+0x0",
  "E25\s+YES\s+0x0",
  "E26\s+YES\s+0x0",
  "E27\s+YES\s+0x0",
  "E28\s+YES\s+0x0",
  "E29\s+YES\s+0x0",
  "E30\s+YES\s+0x0",
  "E31\s+YES\s+0x0",
  "E32\s+YES\s+0x0",
  "E33\s+YES\s+0x0",
  "E34\s+YES\s+0x0",
  "E35\s+YES\s+0x0",
  "E36\s+YES\s+0x0",
  "E37\s+YES\s+0x0",
  "E38\s+YES\s+0x0",
  "E39\s+YES\s+0x0",
  "E40\s+YES\s+0x0",
  "E41\s+YES\s+0x0",
  "E42\s+YES\s+0x0",
  "E43\s+YES\s+0x0",
  "E44\s+YES\s+0x0",
  "E45\s+YES\s+0x0",
  "E46\s+YES\s+0x0",
  "E47\s+YES\s+0x0",
  "E48\s+YES\s+0x0",
  "E49\s+YES\s+0x0",
  "E50\s+YES\s+0x0",
  "E51\s+YES\s+0x0",
  "E52\s+YES\s+0x0",
  "E53\s+YES\s+0x0",
  "E54\s+YES\s+0x0",
  "E55\s+YES\s+0x0",
  "E56\s+YES\s+0x0",
  "E57\s+YES\s+0x0",
  "E58\s+YES\s+0x0",
  "E59\s+YES\s+0x0",
  "E60\s+YES\s+0x0",
  "E61\s+YES\s+0x0",
  "E62\s+YES\s+0x0",
  "E63\s+YES\s+0x0",
  "E64\s+YES\s+0x0",
"\(y\) get_all_port_lpmod_status: All port lpmode status checked\."]



minipack3_packages_file_name='packages-minipack3'

ospf_ports_lpmode_test_pattern= ["\(y\) set_all_port_low_lpmode_status: All ports have activated LPmode\."]
ospf_ports_hpmode_test_pattern= ["\(y\) set_all_port_high_lpmode_status: All ports have cancelled LPmode\."]

osfp_port_enable_pattern = ["\(y\) enable_all_ports: All ports\' reset signals are released."]
osfp_port_disable_pattern = ["\(y\) disable_all_ports: All ports\' reset signals are held."]
unidiag_case_pass = "\[total_funcs:.*pass:.*skip:.*fail: 0 \].* - - \[PASS\]"


th5_image = 'th5_image'
smb_image='smb_image'
mcb_image='mcb_image'
scm_image='scm_image'
iob_image='iob_image'
dom_image='dom_image'
i210_image= 'i210_image'
bios_from_bmc_image="bios_from_bmc_image"
iob_from_bmc_image="iob_from_bmc_image"

smb_cpld_name="smb_cpld flash" 
smb_cpld="smb_cpld"
smb_cpld_option="g"
minipack_smb_cpld_update_pattern=["\(y\) smb_cpld\s+: SPI device smb upgrade succeeded."]
 
mcb_cpld_name="mcb_cpld flash" 
mcb_cpld="mcb_cpld"
mcb_cpld_option="h" 
minipack_mcb_cpld_update_pattern=["\(y\) mcb_cpld\s+: SPI device mcb upgrade succeeded."]

scm_cpld_name="scm_cpld flash" 
scm_cpld_option="i" 
scm_cpld="scm_cpld"
minipack_scm_cpld_update_pattern=["\(y\) scm_cpld\s+: SPI device scm upgrade succeeded."]

th5_name="th5 switch flash"
th5_option="f"
minipack_th5_update_pattern=["\(y\) th5\s+: SPI device th5 upgrade succeeded."]



MINIPACK3 = SwImage.getSwImage("DIAG")
minipack3_unidiag_old_version = MINIPACK3.oldVersion
minipack3_unidiag_new_version = MINIPACK3.newVersion

packages_file_name='packages-minipack3'
latest_images_dir='automation/Package6'
iob_fpga_unidiag_option='b'
dom_fpga_unidiag_option='c'
#install_reinstall_image_present_list = ['minipack3_montblanc_unidiag_evt_x86_1.2.9', 'minipack3_montblanc_unidiag_evt_x86_1.2.9.tar.gz']
install_reinstall_packages_present_list = ['packages.*',  'packages.*.tar.gz']
unidiag_install_success_regex='install unidiag success!'

system_test_pattern=[ "\[ a \]\s+auto \(44\)\s+53",
  "\[ b \].*System Test \(13\)\s+12",
  "\[ c \].*Board Test \(7\)\s+32",
  "\[ d \].*FPGA Test \(3\)\s+ 0",
  "\[ e \].*CPLD Test \(3\)\s+ 0",
  "\[ f \].*Firmware Upgrade \(11\)\s+ 0",
  "\[ g \].*Stress Test \(6\)\s+ 0",
  "\[ h \].*Sanity Test \(54\)\s+ 0",
  "\[ i \].*Snapshot \(1\)\s+ 0",]
  
  
system_led_test_pattern=["\[ a \].*auto \(0\)\s+0",
  "\[ b \].*SCM LED Test \(1\)\s+0",
  "\[ c \].*SMB LED Test \(1\)\s+0",
  "\[ d \].*PSU LED Test \(1\)\s+0",
  "\[ e \].*FAN LED Test \(1\)\s+0",
  "\[ f \].*SYS LED Test \(1\)\s+0",
  "\[ g \].*PORTs LED Test \(1\)\s+0",]
  
  
  
system_fan_test_pattern=["\[ a \].*auto \(0\)\s+0",
  "\[ b \].*FAN Speed Get Test \(1\)\s+0",
  "\[ c \].*FAN Speed Set Test \(1\)\s+0",
  "\[ q \].*Back to upper menu"]
  
  
system_usb_test_pattern=["\[ a \].*auto \(1\)\s+1",
  "\[ b \].*USB Storage Test \(1\)\s+0",
  "\[ c \].*USB Network Test \(1\)\s+1",]
  
system_mac_test_pattern=["\[ a \].*auto \(2\)\s+2",
  "\[ b \].*COMe MAC Addr Check \(1\)\s+1",
  "\[ c \].*BMC MAC Addr Check \(1\)\s+1",]
  
system_osfp_test_pattern=[
 "\[ a \].*auto \(8\)\s+8",
  "\[ b \].*I2C SCAN Test \(1\)\s+0",
  "\[ c \].*OSFP/QSFP PORTS Enable \(1\)\s+0",
  "\[ d \].*OSFP/QSFP PORTS Disable \(1\)\s+0",
  "\[ e \].*OSFP PORTS Present Check \(1\)\s+1",
  "\[ f \].*OSFP PORTS Reset Check \(1\)\s+1",
  "\[ g \].*OSFP PORTS LPMODE Check \(1\)\s+1",
  "\[ h \].*OSFP PORTS INT Check \(1\)\s+1",
  "\[ i \].*OSFP PORTS RESET Test \(1\)\s+1",
  "\[ j \].*OSFP PORTS UNRESET Test \(1\)\s+1",
  "\[ k \].*OSFP PORTS LPMODE Test \(1\)\s+1",
  "\[ l \].*OSFP PORTS HPMODE Test \(1\)\s+1",
  "\[ m \].*Get OSFP PORTs Voltage \(1\)\s+0",
  "\[ n \].*Get OSFP PORTs Temperature \(1\)\s+0",
  "\[ o \].*Get OSFP PORTs Current \(1\)\s+0",
  "\[ p \].*Set all ELB Power Consumption to 16W \(1\)\s+0",
  "\[ r \].*Set all ELB Power Consumption to 0W \(1\)\s+0",
  "\[ s \].*OSFP PORTS INT Test \(1\)\s+0",
  
]

board_test_pattern=["\[ a \].*auto \(32\)\s+41",
  "\[ b \].*MCB  Board Test \(2\)\s+2",
  "\[ c \].*SMB  Board Test \(2\)\s+2",
  "\[ d \].*SCM  Board Test \(2\)\s+2",
  "\[ e \].*PDB  Board Test \(2\)\s+2",
  "\[ f \].*FCB  Board Test \(1\)\s+1",
  "\[ g \].*COMe Board Test \(8\)\s+14",
  "\[ h \].*BMC  Board Test \(9\)\s+9",]
  
mcb_board_test_pattern=["\[ a \].*auto \(2\)\s+2",
  "\[ b \].*I2C SCAN Test \(1\)\s+1",
  "\[ c \].*PCIe SCAN Test \(1\)\s+1",]
  
smb_board_test_pattern=["\[ a \].*auto \(2\)\s+2",
  "\[ b \].*I2C SCAN Test \(1\)\s+1",
  "\[ c \].*PCIe SCAN Test \(1\)\s+1",]
		  
scm_board_test_pattern=["\[ a \].*auto \(2\)\s+2",
  "\[ b \].*I2C SCAN Test \(1\)\s+1",
  "\[ c \].*NVMe Test \(2\)\s+1",]
  
  

pdb_board_test_pattern=["\[ a \].*auto \(2\)\s+2",
  "\[ b \].*I2C SCAN Test \(1\)\s+1",
  "\[ c \].*I2C SCAN Test 3V3 Card \(1\)\s+1",]
  
fcb_board_test_pattern=["\[ a \].*auto \(1\)\s+1",
  "\[ b \].*I2C SCAN Test \(1\)\s+1",]
  
come_board_test_pattern=["\[ a \].*auto \(14\)\s+22",
  "\[ b \].*I2C SCAN Test \(1\)\s+1",
  "\[ c \].*PCIe SCAN Test \(1\)\s+1",
  "\[ d \].*BIOS Test \(2\)\s+2",
  "\[ e \].*CPU Test \(2\)\s+2",
  "\[ f \].*MEM Test \(2\)\s+2",
  "\[ g \].*TPM Test \(1\)\s+1",
  "\[ h \].*RTC Test \(3\)\s+3",
  "\[ i \].*USB Test \(2\)\s+2",]
  
bmc_board_test_pattern=["\[ a \].*auto \(9\)\s+10",
  "\[ b \].*OS Access \(1\)\s+1",
  "\[ c \].*I2C SCAN Test \(1\)\s+1",
  "\[ d \].*CPU Test \(1\)\s+1",
  "\[ e \].*MEM Test \(1\)\s+1",
  "\[ f \].*RTC Test \(1\)\s+1",
  "\[ g \].*TPM Test \(1\)\s+1",
  "\[ h \].*USB Test \(1\)\s+1",
  "\[ i \].*PECI Test \(1\)\s+1",                       
  "\[ v \].*show bmc version \(1\)\s+1",
  
  ]

fpga_test_pattern=["\[ a \].*auto \(0\)\s+0",
  "\[ b \].*IOB FPGA \(2\)\s+0",
  "\[ c \].*DOM1 FPGA \(2\)\s+0",
  "\[ d \].*DOM2 FPGA \(2\)\s+0",]
  
  
iob_fpga_test_pattern=[
"\[ a \]\s+auto \(0\)\s+0", 
  "\[ b \]\s+Show IOB Version \(1\)\s+0", 
  "\[ c \]\s+IOB Scratch Test \(1\)\s+0", 
]
dom1_fpga_test_pattern=[
"\[ a \]\s+auto \(0\)\s+0", 
  "\[ b \]\s+Show DOM1 Version \(1\)\s+0", 
  "\[ c \]\s+DOM1 Scratch Test \(1\)\s+0", 
  
]

dom2_fpga_test_pattern=[
"\[ a \]\s+auto \(0\)\s+0", 
  "\[ b \]\s+Show DOM2 Version \(1\)\s+0", 
  "\[ c \]\s+DOM2 Scratch Test \(1\)\s+0", 
  
]

cpld_test_pattern=[
"\[ a \].*auto \(0\)\s+0",
  "\[ b \].*MCB CPLD Test \(2\)\s+0",
  "\[ c \].*SMB CPLD Test \(2\)\s+0",
  "\[ d \].*SCM CPLD Test \(2\)\s+0",

]
mcb_cpld_test_pattern=[
"\[ a \]\s+auto \(0\)\s+0",
  "\[ b \]\s+Show MCB Version \(1\)\s+0",
  "\[ c \]\s+MCB Scratch Test \(1\)\s+0",
]
smb_cpld_test_pattern=[
"\[ a \]\s+auto \(0\)\s+0",
  "\[ b \]\s+Show SMB Version \(1\)\s+0",
  "\[ c \]\s+SMB Scratch Test \(1\)\s+0",
]
scm_cpld_test_pattern=[
"\[ a \]\s+auto \(0\)\s+0",
  "\[ b \]\s+Show SCM Version \(1\)\s+0",
  "\[ c \]\s+SCM Scratch Test \(1\)\s+0",
]

firmware_submenu_pattern=[
  "\[ a \].*auto \(0\)\s+0",
  "\[ b \].*Upgrade IOB FPGA Firmware Flash \(1\)\s+0",
  "\[ c \].*Upgrade DOM FPGA Firmware Flash \(1\)\s+0",
  "\[ d \].*Upgrade TH5 Switch ASIC Firmware Flash \(1\)\s+0",
  "\[ e \].*Upgrade MCB CPLD Firmware Flash \(1\)\s+0",
  "\[ f \].*Upgrade SCM CPLD Firmware Flash \(1\)\s+0",
  "\[ g \].*Upgrade SMB CPLD Firmware Flash \(1\)\s+0",
  "\[ h \].*Upgrade I210 NIC Firmware \(1\)\s+0",
  "\[ i \].*Upgrade I210 NIC MAC Address \(1\)\s+0",
  "\[ j \].*Upgrade 88E6321 Firmware EEPROM \(1\)\s+0",
  "\[ k \].*FRU EEPROM Upgrade \(9\)\s+0",
  "\[ l \].*ID EEPROM Upgrade \(6\)\s+0",
]
stress_submenu_pattern=[
"\[ a \]\s+auto \(0\)\s+\s+0",
  "\[ b \]\s+CPU Stress \(1\)\s+\s+0",
  "\[ c \]\s+MEM Stress \(1\)\s+\s+0",
  "\[ d \]\s+I2C Stress \(1\)\s+\s+0",
  "\[ e \]\s+SPI Stress \(1\)\s+\s+0",
  "\[ f \]\s+PCIe Stress \(1\)\s+\s+0",
  "\[ g \]\s+Firmware Upgrade Stress \(1\)\s+0",
]
unidiag_test_run_string = "press \[ a b c d e f g h i \] to run a test"

####################### MINERVA #############################
user_cancelled_unidiag_case = ["User cancelled"]
minerva="minerva"
minerva_janga="minerva_janga"
minerva_tahan="minerva_tahan"
mp3="minipack3"
true=True
false=False
devicename = os.environ.get("deviceName", "")
import logging
logging.info("devicename:{}".format(devicename))
if "minerva" in devicename.lower():
    minerva_version_dict=SwImage.getSwImage(SwImage.DIAG).imageDict.get('minerva_version')
    Diag_workspace=SwImage.getSwImage(SwImage.DIAG).localImageDir
    I210_workspace=SwImage.getSwImage(SwImage.I210).localImageDir
    CPLD_workspace=SwImage.getSwImage(SwImage.CPLD).localImageDir
    BIOS_workspace=SwImage.getSwImage(SwImage.BIOS).localImageDir
    FPGA_workspace=SwImage.getSwImage(SwImage.FPGA).localImageDir
    bios_update_timeout=2400
    
    workspace="~/automation"
    minerva_diag_new_image=SwImage.getSwImage(SwImage.DIAG).newImage
    minerva_diag_old_image=SwImage.getSwImage(SwImage.DIAG).oldImage
    minerva_diag_new_version=SwImage.getSwImage(SwImage.DIAG).newVersion
    minerva_diag_old_version=SwImage.getSwImage(SwImage.DIAG).newVersion
    
    minerva_i210_new_image=SwImage.getSwImage(SwImage.I210).newImage
    minerva_i210_old_image=SwImage.getSwImage(SwImage.I210).oldImage
    minerva_i210_new_version=SwImage.getSwImage(SwImage.I210).newVersion
    minerva_i210_old_version=SwImage.getSwImage(SwImage.I210).newVersion
    
    minerva_pwr_cpld_new_image=SwImage.getSwImage(SwImage.CPLD).newImage["pwr"]
    minerva_pwr_cpld_old_image=SwImage.getSwImage(SwImage.CPLD).oldImage["pwr"]
    minerva_pwr_cpld_new_version=SwImage.getSwImage(SwImage.CPLD).newVersion["pwr"]
    minerva_pwr_cpld_old_version=SwImage.getSwImage(SwImage.CPLD).oldVersion["pwr"]
    
    minerva_smb1_cpld_new_image=SwImage.getSwImage(SwImage.CPLD).newImage["smb1"]
    minerva_smb1_cpld_old_image=SwImage.getSwImage(SwImage.CPLD).oldImage["smb1"]
    minerva_smb1_cpld_new_version=SwImage.getSwImage(SwImage.CPLD).newVersion["smb1"]
    minerva_smb1_cpld_old_version=SwImage.getSwImage(SwImage.CPLD).oldVersion["smb1"]
    
    minerva_smb2_cpld_new_image=SwImage.getSwImage(SwImage.CPLD).newImage["smb2"]
    minerva_smb2_cpld_old_image=SwImage.getSwImage(SwImage.CPLD).oldImage["smb2"]
    minerva_smb2_cpld_new_version=SwImage.getSwImage(SwImage.CPLD).newVersion["smb2"]
    minerva_smb2_cpld_old_version=SwImage.getSwImage(SwImage.CPLD).oldVersion["smb2"]
    
    minerva_bios_new_image=SwImage.getSwImage(SwImage.BIOS).newImage
    minerva_bios_old_image=SwImage.getSwImage(SwImage.BIOS).oldImage
    minerva_bios_new_version=SwImage.getSwImage(SwImage.BIOS).newVersion
    minerva_bios_old_version=SwImage.getSwImage(SwImage.BIOS).oldVersion
    
    minerva_dom_fpga_new_image=SwImage.getSwImage(SwImage.FPGA).newImage["dom"]
    minerva_dom_fpga_old_image=SwImage.getSwImage(SwImage.FPGA).oldImage["dom"]
    minerva_dom_fpga_new_version=SwImage.getSwImage(SwImage.FPGA).newVersion["DOMFPGA"]
    minerva_dom_fpga_old_version=SwImage.getSwImage(SwImage.FPGA).oldVersion["DOMFPGA"]
    
    minerva_iob_fpga_new_image=SwImage.getSwImage(SwImage.FPGA).newImage["iob"]
    minerva_iob_fpga_old_image=SwImage.getSwImage(SwImage.FPGA).oldImage["iob"]
    minerva_iob_fpga_new_version=SwImage.getSwImage(SwImage.FPGA).newVersion["IOBFPGA"]
    minerva_iob_fpga_old_version=SwImage.getSwImage(SwImage.FPGA).oldVersion["IOBFPGA"]
    
    DIAGOS_MODE=Const.BOOT_MODE_DIAGOS
    OPENBMC_MODE=Const.BOOT_MODE_OPENBMC
    DIAG="DIAG"
    
    minerva_smb_cpld1_name="smb_cpld1 flash" 
    minerva_smb_cpld1_option="e" 
    minerva_smb_cpld1_upgrade_format="fw_smb_cpld1_"
    minerva_smb_cpld1_pattern=["\(y\) smb_cpld1\s+: SPI device smb_1 upgrade succeeded."]
    
    minerva_smb_cpld2_name="smb_cpld2 flash" 
    minerva_smb_cpld2_option="f" 
    minerva_smb_cpld2_upgrade_format="fw_smb_cpld2_"
    minerva_smb_cpld2_pattern=["\(y\) smb_cpld2\s+: SPI device smb_2 upgrade succeeded."]
    
    minerva_power_cpld_name="power_cpld flash" 
    minerva_power_cpld_option="g"
    minerva_power_cpld_upgrade_format="fw_pwr_cpld_"
    minerva_power_cpld_pattern=["\(y\) pwr_cpld\s+: SPI device pwr upgrade succeeded."]
    
    minerva_iob_fpga_name="iob_fpga flash" 
    minerva_iob_fpga_option="b"
    minerva_iob_fpga_upgrade_format="fw_iob_"
    minerva_iob_fpga_pattern=["\(y\) iob_fpga\s+: SPI device iob upgrade succeeded."]
    
    minerva_dom_fpga_name="dom flash" 
    minerva_dom_fpga_option="d"
    minerva_dom_fpga_upgrade_format="fw_dom_"
    minerva_dom_fpga_pattern=["\(y\) dom\s+: SPI device dom upgrade succeeded."]
    
    minerva_i210_flash_name="i210 flash" 
    minerva_i210_flash_option="h"
    minerva_i210_flash_upgrade_format="fw_i210_eeupdate.bin"
    minerva_i210_flash_upgrade_pattern = [
    "\(y\) i210\s+:\s+I210 Firmware upgrade succeeded."]
    
    minerva_bios_via_come_option='j'
    minerva_bios_via_come_name="bios flash"
    minerva_bios_via_come_upgrade_format="fw_bios_"
    minerva_bios_via_come_pattern = [
    "\(y\) bios\s+: BIOS upgrade succeeded."]
    
    minerva_i2c_system_scan_pattern = [
     "J3 BRD EEPROM\s+I801 CH1\s+ 1\s+0x53\s+PASS",
     "SMB_CPLD_1\s+IOB CH2\s+ 4\s+0x35\s+PASS",
     "VRM_OSFP_3R3V_LEFT\s+IOB CH3\s+ 5\s+0x7a\s+PASS",
     "VRM_0R75V_0R9_1_L\s+IOB CH3\s+ 5\s+0x7d\s+PASS",
     "LM75B #LEFTT Inner\s+IOB CH3\s+ 5\s+0x48\s+PASS",
     "LM75B #RIGHT_BOT\s+IOB CH4\s+ 6\s+0x49\s+PASS",
     "LM75B #RIGHT_TOP\s+IOB CH4\s+ 6\s+0x4a\s+PASS",
     "EEPROM\(OOB Switch\)\s+IOB CH5\s+ 7\s+0x50\s+PASS",
     "Netlake CPLD\s+IOB CH6\s+ 8\s+0x40\s+PASS",
     "J3 \(Left\)\s+IOB CH7\s+ 9\s+0x44\s+PASS",
     "EEPROM\(SMB FRU#1\)\s+IOB CH8\s+10\s+0x56\s+PASS",
     "SMB_CPLD_2\s+IOB CH9\s+11\s+0x33\s+PASS",
     "SMB_CPLD_2 \(OSFP\)\s+IOB CH9\s+11\s+0x3e\s+PASS",
     "VRM_OSFP_3R3V_R\s+IOB CH10\s+12\s+0x7e\s+PASS",
     "VRM_1R2_0R9_1_R\s+IOB CH10\s+12\s+0x7a\s+PASS",
     "VRM_0R75_0R9_0_R\s+IOB CH10\s+12\s+0x7b\s+PASS",
     "VRM_1R2_0R9_L\s+IOB CH10\s+12\s+0x76\s+PASS",
     "VRM_VDD_CORE_R\s+IOB CH11\s+13\s+0x60\s+PASS",
     "VRM_0R75V_1R2V_0_L\s+IOB CH11\s+13\s+0x7b\s+PASS",
     "VRM_VDD_CORE_L\s+IOB CH11\s+13\s+0x76\s+PASS",
     "VRM_1R2_0R75_R\s+IOB CH11\s+13\s+0x7d\s+PASS",
     "LM75B #Pwr\(TLVR inner\)\s+IOB CH12\s+14\s+0x48\s+PASS",
     "LM75B #OSFP\(outer\)\s+IOB CH12\s+14\s+0x49\s+PASS",
     "XP12V_COME  PTPS25990\s+IOB CH13\s+15\s+0x4c\s+PASS",
     "PCIe_CLK_buffer_Gen4 RC19004\s+IOB CH13\s+15\s+0x6f\s+PASS",
     "PWR CPLD\s+IOB CH15\s+17\s+0x60\s+PASS",
     "J3 \(Right\)\s+IOB CH16\s+18\s+0x44\s+PASS",
     "BMC EEPROM\s+IOB CH19\s+21\s+0x51\s+PASS",
     "BMC Thermal sensor\s+IOB CH19\s+21\s+0x4a\s+PASS",
     "HBM clock buffer_J3_R\s+IOB CH20\s+22\s+0x6f\s+PASS",
     "LM75B outer\s+IOB CH21\s+23\s+0x4a\s+PASS",
     "48V MAIN HOTSWAP\s+IOB CH21\s+23\s+0x10\s+PASS",
     "ADC128D8 #4\s+IOB CH22\s+24\s+0x37\s+PASS",
     "HBM clock buffer_J3_L\s+IOB CH22\s+24\s+0x6c\s+PASS",
     "ADC128D8 #5\s+IOB CH24\s+26\s+0x1d\s+PASS",
     "ADC128D8 #6\s+IOB CH24\s+26\s+0x37\s+PASS",
     "ADC128D8 #7\s+IOB CH25\s+27\s+0x1d\s+PASS",
     "ADC128D8 #8\s+IOB CH25\s+27\s+0x37\s+PASS",
     "SMB ADC #1\s+IOB CH26\s+28\s+0x1d\s+PASS",
     "SMB ADC #2\s+IOB CH26\s+28\s+0x1f\s+PASS",
     "SMB ADC #3\s+IOB CH26\s+28\s+0x37\s+PASS",
     "\(y\) test_scan_i2c_smb: Scanned 41 i2c devices, 0 failed",
     
     "LM75B PDB Thermal sensor\s+IOB\s+CH21\s+23\s+0x48\s+PASS",
     "Power brick #1\s+IOB\s+CH21\s+23\s+0x60\s+PASS",
     "Power brick #2\s+IOB\s+CH21\s+23\s+0x61\s+PASS",
     "\(y\) test_scan_i2c_pdb: Scanned 3 i2c devices, 0 failed.",
    
     "COMe FRU eeprom\s+IOB\s+CH14\s+16\s+0x56\s+PASS",
     "COMe OUTLET Sensor\s+IOB\s+CH14\s+16\s+0x4a\s+PASS",
     "COMe INLET Sensor\s+IOB\s+CH14\s+16\s+0x48\s+PASS",
     "COMe CPLD ADC\s+IOB\s+CH14\s+16\s+0x0f\s+PASS",
     "COMe CPLD MISC control\s+IOB\s+CH14\s+16\s+0x1f\s+PASS",
     "VNN_PCH\s+IOB\s+CH23\s+25\s+0x11\s+PASS",
     "1V05_STBY\s+IOB\s+CH23\s+25\s+0x22\s+PASS",
     "PVCCIN_CPU & P1V8 _STBY\s+IOB\s+CH23\s+25\s+0x76\s+PASS",
     "PVDDQ_ABC_CPU\s+IOB\s+CH23\s+25\s+0x45\s+PASS",
     "PVCCANA_CPU\s+IOB\s+CH23\s+25\s+0x66\s+PASS",
     "\(y\) test_scan_i2c_come: Scanned 10 i2c devices, 0 failed",
    
     "COMe FRU EEPROM\s+BMC\s+CH0\s+0\s+0x56\s+PASS",
     "COMe Inlet Temp\s+BMC\s+CH0\s+0\s+0x48\s+PASS",
     "COMe Outlet Temp\s+BMC\s+CH0\s+0\s+0x4a\s+PASS",
     "COMe CPLD ADC\s+BMC\s+CH0\s+0\s+0x0f\s+PASS",
     "COMe CPLD Misc Control\s+BMC\s+CH0\s+0\s+0x1f\s+PASS",
     "SMB_CPLD_1\s+BMC\s+CH1\s+1\s+0x35\s+PASS",
     "SMB_FRU#2\s+BMC\s+CH3\s+3\s+0x56\s+PASS",
     "PCA9555\s+BMC\s+CH4\s+4\s+0x27\s+PASS",
     "COMe SML0\s+BMC\s+CH5\s+5\s+0x16\s+PASS",
     "BMC Thermal sensor\s+BMC\s+CH8\s+8\s+0x4a\s+PASS",
     "BMC EEPROM\s+BMC\s+CH8\s+8\s+0x51\s+PASS",
     "PWR_CPLD\s+BMC\s+CH12\s+12\s+0x60\s+PASS",
     "IOBFPGA\s+BMC\s+CH13\s+13\s+0x35\s+PASS",
     "\(y\) test_scan_i2c_bmc: Scanned 13 i2c devices, 0 failed.",
    ]
    minerva_system_spi_scan_test_pattern=[
      "IOB Flash\s+0\s+NA\s+Micron/Numonyx/ST\s+N25Q128..3E\s+16384 KB\s+PASS",
      "DOM Flash\s+1\s+9\s+Micron/Numonyx/ST\s+N25Q128..3E\s+16384 KB\s+PASS",
      "SMB_1 Flash\s+6\s+1\s+Winbond\s+W25X20\s+256 KB\s+PASS",
      "SMB_2 Flash\s+4\s+7\s+Winbond\s+W25X20\s+256 KB\s+PASS",
      "PWR Flash\s+3\s+3\s+Winbond\s+W25X20\s+256 KB\s+PASS",
      "J3_1 Flash\s+5\s+8\s+Micron/Numonyx/ST\s+N25Q256..1E\s+32768 KB\s+PASS",
      "J3_2 Flash\s+2\s+10\s+Micron/Numonyx/ST\s+N25Q256..1E\s+32768 KB\s+PASS",
      "\(y\) test_scan_spi_smb: Scanned 7 spi devices, 0 failed.",
    ]
    minerva_system_pcie_scan_test_pattern = [
       "I210 NIC\s+01:00.0\s+PASS",
       "J3 ASIC#0\s+15:00.0\s+PASS",
       "J3 ASIC#1\s+18:00.0\s+PASS",
       "IOB FPGA\s+17:00.0\s+PASS",
    
    ]
    minerva_osfp_port_enable_pattern = ["\(y\) enable_all_ports"]
    minerva_osfp_port_disable_pattern = ["\(y\) disable_all_ports"]
    
    minerva_ospf_ports_check_pattern=[
        "E1\s+PRESENT",
        "E2\s+PRESENT",
        "F3\s+PRESENT",
        "F4\s+PRESENT",
        "F5\s+PRESENT",
        "F6\s+PRESENT",
        "F7\s+PRESENT",
        "F8\s+PRESENT",
        "F9\s+PRESENT",
        "F10\s+PRESENT",
        "F11\s+PRESENT",
        "F12\s+PRESENT",
        "F13\s+PRESENT",
        "F14\s+PRESENT",
        "F15\s+PRESENT",
        "F16\s+PRESENT",
        "F17\s+PRESENT",
        "F18\s+PRESENT",
        "F19\s+PRESENT",
        "F20\s+PRESENT",
        "F21\s+PRESENT",
        "F22\s+PRESENT",
        "F23\s+PRESENT",
        "F24\s+PRESENT",
        "F25\s+PRESENT",
        "F26\s+PRESENT",
        "F27\s+PRESENT",
        "F28\s+PRESENT",
        "F29\s+PRESENT",
        "F30\s+PRESENT",
        "F31\s+PRESENT",
        "F32\s+PRESENT",
        "F33\s+PRESENT",
        "F34\s+PRESENT",
        "F35\s+PRESENT",
        "F36\s+PRESENT",
        "F37\s+PRESENT",
        "F38\s+PRESENT",
        "F39\s+PRESENT",
        "F40\s+PRESENT",
        "E41\s+PRESENT",
        "F42\s+PRESENT",
        "F43\s+PRESENT",
        "E44\s+PRESENT",
        "E45\s+PRESENT",
        "E46\s+PRESENT",
        "\(y\) check_OSFP_QSFP_ports_present: OSFP/QSFP port present check finished.",]
    
    minerva_ospf_ports_reset_check_pattern = ["E1\s+0x0\s+RESET",
    "E2\s+0x0\s+RESET",
    "F3\s+0x0\s+RESET",
    "F4\s+0x0\s+RESET",
    "F5\s+0x0\s+RESET",
    "F6\s+0x0\s+RESET",
    "F7\s+0x0\s+RESET",
    "F8\s+0x0\s+RESET",
    "F9\s+0x0\s+RESET",
    "F10\s+0x0\s+RESET",
    "F11\s+0x0\s+RESET",
    "F12\s+0x0\s+RESET",
    "F13\s+0x0\s+RESET",
    "F14\s+0x0\s+RESET",
    "F15\s+0x0\s+RESET",
    "F16\s+0x0\s+RESET",
    "F17\s+0x0\s+RESET",
    "F18\s+0x0\s+RESET",
    "F19\s+0x0\s+RESET",
    "F20\s+0x0\s+RESET",
    "F21\s+0x0\s+RESET",
    "F22\s+0x0\s+RESET",
    "F23\s+0x0\s+RESET",
    "F24\s+0x0\s+RESET",
    "F25\s+0x0\s+RESET",
    "F26\s+0x0\s+RESET",
    "F27\s+0x0\s+RESET",
    "F28\s+0x0\s+RESET",
    "F29\s+0x0\s+RESET",
    "F30\s+0x0\s+RESET",
    "F31\s+0x0\s+RESET",
    "F32\s+0x0\s+RESET",
    "F33\s+0x0\s+RESET",
    "F34\s+0x0\s+RESET",
    "F35\s+0x0\s+RESET",
    "F36\s+0x0\s+RESET",
    "F37\s+0x0\s+RESET",
    "F38\s+0x0\s+RESET",
    "F39\s+0x0\s+RESET",
    "F40\s+0x0\s+RESET",
    "E41\s+0x0\s+RESET",
    "F42\s+0x0\s+RESET",
    "F43\s+0x0\s+RESET",
    "E44\s+0x0\s+RESET",
    "E45\s+0x0\s+RESET",
    "E46\s+0x0\s+RESET",
    "\(y\) get_all_port_reset_status: All ports reset signal check finished.",

    ]

    minerva_ospf_ports_unreset_check_pattern =["E1\s+0x1\s+UNRESET",
    "E2\s+0x1\s+UNRESET",
    "E3\s+0x1\s+UNRESET",
    "E4\s+0x1\s+UNRESET",
    "E5\s+0x1\s+UNRESET",
    "E6\s+0x1\s+UNRESET",
    "F1\s+0x1\s+UNRESET",
    "F2\s+0x1\s+UNRESET",
    "F3\s+0x1\s+UNRESET",
    "F4\s+0x1\s+UNRESET",
    "F5\s+0x1\s+UNRESET",
    "F6\s+0x1\s+UNRESET",
    "F7\s+0x1\s+UNRESET",
    "F8\s+0x1\s+UNRESET",
    "F9\s+0x1\s+UNRESET",
    "F10\s+0x1\s+UNRESET",
    "F11\s+0x1\s+UNRESET",
    "F12\s+0x1\s+UNRESET",
    "F13\s+0x1\s+UNRESET",
    "F14\s+0x1\s+UNRESET",
    "F15\s+0x1\s+UNRESET",
    "F16\s+0x1\s+UNRESET",
    "F17\s+0x1\s+UNRESET",
    "F18\s+0x1\s+UNRESET",
    "F19\s+0x1\s+UNRESET",
    "F20\s+0x1\s+UNRESET",
    "F21\s+0x1\s+UNRESET",
    "F22\s+0x1\s+UNRESET",
    "F23\s+0x1\s+UNRESET",
    "F24\s+0x1\s+UNRESET",
    "F25\s+0x1\s+UNRESET",
    "F26\s+0x1\s+UNRESET",
    "F27\s+0x1\s+UNRESET",
    "F28\s+0x1\s+UNRESET",
    "F29\s+0x1\s+UNRESET",
    "F30\s+0x1\s+UNRESET",
    "F31\s+0x1\s+UNRESET",
    "F32\s+0x1\s+UNRESET",
    "F33\s+0x1\s+UNRESET",
    "F34\s+0x1\s+UNRESET",
    "F35\s+0x1\s+UNRESET",
    "F36\s+0x1\s+UNRESET",
    "F37\s+0x1\s+UNRESET",
    "F38\s+0x1\s+UNRESET",
    "F39\s+0x1\s+UNRESET",
    "F40\s+0x1\s+UNRESET",
    "\(y\) get_all_port_reset_status: All ports reset signal check finished.",]
    
    minerva_osfp_set_reset_pattern=[
    "E1\s+RESET:\s+PASS",
    "E2\s+RESET:\s+PASS",
    "F3\s+RESET:\s+PASS",
    "F4\s+RESET:\s+PASS",
    "F5\s+RESET:\s+PASS",
    "F6\s+RESET:\s+PASS",
    "F7\s+RESET:\s+PASS",
    "F8\s+RESET:\s+PASS",
    "F9\s+RESET:\s+PASS",
    "F10\s+RESET:\s+PASS",
    "F11\s+RESET:\s+PASS",
    "F12\s+RESET:\s+PASS",
    "F13\s+RESET:\s+PASS",
    "F14\s+RESET:\s+PASS",
    "F15\s+RESET:\s+PASS",
    "F16\s+RESET:\s+PASS",
    "F17\s+RESET:\s+PASS",
    "F18\s+RESET:\s+PASS",
    "F19\s+RESET:\s+PASS",
    "F20\s+RESET:\s+PASS",
    "F21\s+RESET:\s+PASS",
    "F22\s+RESET:\s+PASS",
    "F23\s+RESET:\s+PASS",
    "F24\s+RESET:\s+PASS",
    "F25\s+RESET:\s+PASS",
    "F26\s+RESET:\s+PASS",
    "F27\s+RESET:\s+PASS",
    "F28\s+RESET:\s+PASS",
    "F29\s+RESET:\s+PASS",
    "F30\s+RESET:\s+PASS",
    "F31\s+RESET:\s+PASS",
    "F32\s+RESET:\s+PASS",
    "F33\s+RESET:\s+PASS",
    "F34\s+RESET:\s+PASS",
    "F35\s+RESET:\s+PASS",
    "F36\s+RESET:\s+PASS",
    "F37\s+RESET:\s+PASS",
    "F38\s+RESET:\s+PASS",
    "F39\s+RESET:\s+PASS",
    "F40\s+RESET:\s+PASS",
    "E41\s+RESET:\s+PASS",
    "F42\s+RESET:\s+PASS",
    "F43\s+RESET:\s+PASS",
    "E44\s+RESET:\s+PASS",
    "E45\s+RESET:\s+PASS",
    "E46\s+RESET:\s+PASS",
    "\(y\) set_all_port_reset_status: OSFP/QSFP port reset test succeeded.",
    ]
   
    minerva_osfp_set_unreset_pattern = [
    "E1\s+UNRESET:\s+PASS",
    "E2\s+UNRESET:\s+PASS",
    "F3\s+UNRESET:\s+PASS",
    "F4\s+UNRESET:\s+PASS",
    "F5\s+UNRESET:\s+PASS",
    "F6\s+UNRESET:\s+PASS",
    "F7\s+UNRESET:\s+PASS",
    "F8\s+UNRESET:\s+PASS",
    "F9\s+UNRESET:\s+PASS",
    "F10\s+UNRESET:\s+PASS",
    "F11\s+UNRESET:\s+PASS",
    "F12\s+UNRESET:\s+PASS",
    "F13\s+UNRESET:\s+PASS",
    "F14\s+UNRESET:\s+PASS",
    "F15\s+UNRESET:\s+PASS",
    "F16\s+UNRESET:\s+PASS",
    "F17\s+UNRESET:\s+PASS",
    "F18\s+UNRESET:\s+PASS",
    "F19\s+UNRESET:\s+PASS",
    "F20\s+UNRESET:\s+PASS",
    "F21\s+UNRESET:\s+PASS",
    "F22\s+UNRESET:\s+PASS",
    "F23\s+UNRESET:\s+PASS",
    "F24\s+UNRESET:\s+PASS",
    "F25\s+UNRESET:\s+PASS",
    "F26\s+UNRESET:\s+PASS",
    "F27\s+UNRESET:\s+PASS",
    "F28\s+UNRESET:\s+PASS",
    "F29\s+UNRESET:\s+PASS",
    "F30\s+UNRESET:\s+PASS",
    "F31\s+UNRESET:\s+PASS",
    "F32\s+UNRESET:\s+PASS",
    "F33\s+UNRESET:\s+PASS",
    "F34\s+UNRESET:\s+PASS",
    "F35\s+UNRESET:\s+PASS",
    "F36\s+UNRESET:\s+PASS",
    "F37\s+UNRESET:\s+PASS",
    "F38\s+UNRESET:\s+PASS",
    "F39\s+UNRESET:\s+PASS",
    "F40\s+UNRESET:\s+PASS",
    "E41\s+UNRESET:\s+PASS",
    "F42\s+UNRESET:\s+PASS",
    "F43\s+UNRESET:\s+PASS",
    "E44\s+UNRESET:\s+PASS",
    "E45\s+UNRESET:\s+PASS",
    "E46\s+UNRESET:\s+PASS",
    "\(y\) set_all_port_not_reset_status",
    ]

    minerva_ospf_ports_lpmode_check_pattern = [
    "E1\s+In:\s+Lpmode",
    "E2\s+In:\s+Lpmode",
    "F3\s+In:\s+Lpmode",
    "F4\s+In:\s+Lpmode",
    "F5\s+In:\s+Lpmode",
    "F6\s+In:\s+Lpmode",
    "F7\s+In:\s+Lpmode",
    "F8\s+In:\s+Lpmode",
    "F9\s+In:\s+Lpmode",
    "F10\s+In:\s+Lpmode",
    "F11\s+In:\s+Lpmode",
    "F12\s+In:\s+Lpmode",
    "F13\s+In:\s+Lpmode",
    "F14\s+In:\s+Lpmode",
    "F15\s+In:\s+Lpmode",
    "F16\s+In:\s+Lpmode",
    "F17\s+In:\s+Lpmode",
    "F18\s+In:\s+Lpmode",
    "F19\s+In:\s+Lpmode",
    "F20\s+In:\s+Lpmode",
    "F21\s+In:\s+Lpmode",
    "F22\s+In:\s+Lpmode",
    "F23\s+In:\s+Lpmode",
    "F24\s+In:\s+Lpmode",
    "F25\s+In:\s+Lpmode",
    "F26\s+In:\s+Lpmode",
    "F27\s+In:\s+Lpmode",
    "F28\s+In:\s+Lpmode",
    "F29\s+In:\s+Lpmode",
    "F30\s+In:\s+Lpmode",
    "F31\s+In:\s+Lpmode",
    "F32\s+In:\s+Lpmode",
    "F33\s+In:\s+Lpmode",
    "F34\s+In:\s+Lpmode",
    "F35\s+In:\s+Lpmode",
    "F36\s+In:\s+Lpmode",
    "F37\s+In:\s+Lpmode",
    "F38\s+In:\s+Lpmode",
    "F39\s+In:\s+Lpmode",
    "F40\s+In:\s+Lpmode",
    "E41\s+In:\s+Lpmode",
    "F42\s+In:\s+Lpmode",
    "F43\s+In:\s+Lpmode",
    "E44\s+In:\s+Lpmode",
    "E45\s+In:\s+Lpmode",
    "E46\s+In:\s+Lpmode",
    "\(y\) get_all_port_lpmod_status: OSFP/QSFP port lpmod check succeeded.",

    ]
    
    minerva_ospf_ports_lpmode_test_pattern=[
    "E1\s+LPMODE SET:\s+PASS",
    "E2\s+LPMODE SET:\s+PASS",
    "F3\s+LPMODE SET:\s+PASS",
    "F4\s+LPMODE SET:\s+PASS",
    "F5\s+LPMODE SET:\s+PASS",
    "F6\s+LPMODE SET:\s+PASS",
    "F7\s+LPMODE SET:\s+PASS",
    "F8\s+LPMODE SET:\s+PASS",
    "F9\s+LPMODE SET:\s+PASS",
    "F10\s+LPMODE\s+SET:\s+PASS",
    "F11\s+LPMODE\s+SET:\s+PASS",
    "F12\s+LPMODE\s+SET:\s+PASS",
    "F13\s+LPMODE\s+SET:\s+PASS",
    "F14\s+LPMODE\s+SET:\s+PASS",
    "F15\s+LPMODE\s+SET:\s+PASS",
    "F16\s+LPMODE\s+SET:\s+PASS",
    "F17\s+LPMODE\s+SET:\s+PASS",
    "F18\s+LPMODE\s+SET:\s+PASS",
    "F19\s+LPMODE\s+SET:\s+PASS",
    "F20\s+LPMODE\s+SET:\s+PASS",
    "F21\s+LPMODE\s+SET:\s+PASS",
    "F22\s+LPMODE\s+SET:\s+PASS",
    "F23\s+LPMODE\s+SET:\s+PASS",
    "F24\s+LPMODE\s+SET:\s+PASS",
    "F25\s+LPMODE\s+SET:\s+PASS",
    "F26\s+LPMODE\s+SET:\s+PASS",
    "F27\s+LPMODE\s+SET:\s+PASS",
    "F28\s+LPMODE\s+SET:\s+PASS",
    "F29\s+LPMODE\s+SET:\s+PASS",
    "F30\s+LPMODE\s+SET:\s+PASS",
    "F31\s+LPMODE\s+SET:\s+PASS",
    "F32\s+LPMODE\s+SET:\s+PASS",
    "F33\s+LPMODE\s+SET:\s+PASS",
    "F34\s+LPMODE\s+SET:\s+PASS",
    "F35\s+LPMODE\s+SET:\s+PASS",
    "F36\s+LPMODE\s+SET:\s+PASS",
    "F37\s+LPMODE\s+SET:\s+PASS",
    "F38\s+LPMODE\s+SET:\s+PASS",
    "F39\s+LPMODE\s+SET:\s+PASS",
    "F40\s+LPMODE\s+SET:\s+PASS",
    "E41\s+LPMODE\s+SET:\s+PASS",
    "F42\s+LPMODE\s+SET:\s+PASS",
    "F43\s+LPMODE\s+SET:\s+PASS",
    "E44\s+LPMODE\s+SET:\s+PASS",
    "E45\s+LPMODE\s+SET:\s+PASS",
    "E46\s+LPMODE\s+SET:\s+PASS",
    "\(y\) set_all_port_low_lpmod_status: OSFP/QSFP port lpmode test succeeded.",
    ]
    
    minerva_ospf_ports_hpmode_test_pattern = [
    "E1\s+LPMODE UNSET: PASS",
    "E2\s+LPMODE UNSET: PASS",
    "F3\s+LPMODE UNSET: PASS",
    "F4\s+LPMODE UNSET: PASS",
    "F5\s+LPMODE UNSET: PASS",
    "F6\s+LPMODE UNSET: PASS",
    "F7\s+LPMODE UNSET: PASS",
    "F8\s+LPMODE UNSET: PASS",
    "F9\s+LPMODE UNSET: PASS",
    "F10\s+LPMODE UNSET: PASS",
    "F11\s+LPMODE UNSET: PASS",
    "F12\s+LPMODE UNSET: PASS",
    "F13\s+LPMODE UNSET: PASS",
    "F14\s+LPMODE UNSET: PASS",
    "F15\s+LPMODE UNSET: PASS",
    "F16\s+LPMODE UNSET: PASS",
    "F17\s+LPMODE UNSET: PASS",
    "F18\s+LPMODE UNSET: PASS",
    "F19\s+LPMODE UNSET: PASS",
    "F20\s+LPMODE UNSET: PASS",
    "F21\s+LPMODE UNSET: PASS",
    "F22\s+LPMODE UNSET: PASS",
    "F23\s+LPMODE UNSET: PASS",
    "F24\s+LPMODE UNSET: PASS",
    "F25\s+LPMODE UNSET: PASS",
    "F26\s+LPMODE UNSET: PASS",
    "F27\s+LPMODE UNSET: PASS",
    "F28\s+LPMODE UNSET: PASS",
    "F29\s+LPMODE UNSET: PASS",
    "F30\s+LPMODE UNSET: PASS",
    "F31\s+LPMODE UNSET: PASS",
    "F32\s+LPMODE UNSET: PASS",
    "F33\s+LPMODE UNSET: PASS",
    "F34\s+LPMODE UNSET: PASS",
    "F35\s+LPMODE UNSET: PASS",
    "F36\s+LPMODE UNSET: PASS",
    "F37\s+LPMODE UNSET: PASS",
    "F38\s+LPMODE UNSET: PASS",
    "F39\s+LPMODE UNSET: PASS",
    "F40\s+LPMODE UNSET: PASS",
    "E41\s+LPMODE UNSET: PASS",
    "F42\s+LPMODE UNSET: PASS",
    "F43\s+LPMODE UNSET: PASS",
    "E44\s+LPMODE UNSET: PASS",
    "E45\s+LPMODE UNSET: PASS",
    "E46\s+LPMODE UNSET: PASS",
    "\(y\) set_all_port_high_lpmod_status: OSFP/QSFP port lpmode unset test succeeded."
    ]
        
    minerva_system_oob_test_pattern = ["\(y\) check_ping_network: PING fe80::b6db:91ff:feff:1%eth0.4088\(fe80::b6db:91ff:feff:1%eth0.4088\) 56 data bytes",
    "64 bytes from fe80::b6db:91ff:feff:1%eth0.4088: icmp_seq=1 ttl=64 time=.*ms",
    "64 bytes from fe80::b6db:91ff:feff:1%eth0.4088: icmp_seq=2 ttl=64 time=.*ms",
    "64 bytes from fe80::b6db:91ff:feff:1%eth0.4088: icmp_seq=3 ttl=64 time=.*ms",
    "3 packets transmitted, 3 received, 0% packet loss, time.*ms",]
    
    minerva_osfp_i2c_scan_disable_port_pattern = ["\(x\) detect_OSFP_QSFP_i2c_device:"]
    minerva_osfp_i2c_scan_enable_port_pattern = [ 
       "E1\s+YES\s+29\s+PASS\s+OSFP\s+TE Connectivity",   
       "E2\s+YES\s+30\s+PASS\s+OSFP\s+LUXSHARE-TECH",
       "F3\s+YES\s+31\s+PASS\s+OSFP\s+ColorChip",
       "F4\s+YES\s+32\s+PASS\s+OSFP\s+ColorChip",
       "F5\s+YES\s+33\s+PASS\s+OSFP\s+ColorChip",
       "F6\s+YES\s+34\s+PASS\s+OSFP\s+ColorChip",
       "F7\s+YES\s+35\s+PASS\s+OSFP\s+ColorChip",
       "F8\s+YES\s+36\s+PASS\s+OSFP\s+ColorChip",
       "F9\s+YES\s+37\s+PASS\s+OSFP\s+ColorChip",
       "F10\s+YES\s+38\s+PASS\s+OSFP\s+ColorChip",         
       "F11\s+YES\s+39\s+PASS\s+OSFP\s+ColorChip",         
       "F12\s+YES\s+40\s+PASS\s+OSFP\s+ColorChip",         
       "F13\s+YES\s+41\s+PASS\s+OSFP\s+ColorChip",         
       "F14\s+YES\s+42\s+PASS\s+OSFP\s+ColorChip",         
       "F15\s+YES\s+43\s+PASS\s+OSFP\s+ColorChip",         
       "F16\s+YES\s+44\s+PASS\s+OSFP\s+ColorChip",         
       "F17\s+YES\s+45\s+PASS\s+OSFP\s+ColorChip",         
       "F18\s+YES\s+46\s+PASS\s+OSFP\s+ColorChip",         
       "F19\s+YES\s+47\s+PASS\s+OSFP\s+ColorChip",         
       "F20\s+YES\s+48\s+PASS\s+OSFP\s+ColorChip",         
       "F21\s+YES\s+49\s+PASS\s+OSFP\s+ColorChip",         
       "F22\s+YES\s+50\s+PASS\s+OSFP\s+ColorChip",         
       "F23\s+YES\s+51\s+PASS\s+OSFP\s+ColorChip",         
       "F24\s+YES\s+52\s+PASS\s+OSFP\s+ColorChip",         
       "F25\s+YES\s+53\s+PASS\s+OSFP\s+ColorChip",         
       "F26\s+YES\s+54\s+PASS\s+OSFP\s+ColorChip",         
       "F27\s+YES\s+55\s+PASS\s+OSFP\s+ColorChip",         
       "F28\s+YES\s+56\s+PASS\s+OSFP\s+ColorChip",         
       "F29\s+YES\s+57\s+PASS\s+OSFP\s+ColorChip",         
       "F30\s+YES\s+58\s+PASS\s+OSFP\s+ColorChip",         
       "F31\s+YES\s+59\s+PASS\s+OSFP\s+ColorChip",         
       "F32\s+YES\s+60\s+PASS\s+OSFP\s+ColorChip",         
       "F33\s+YES\s+61\s+PASS\s+OSFP\s+ColorChip",         
       "F34\s+YES\s+62\s+PASS\s+OSFP\s+ColorChip",         
       "F35\s+YES\s+63\s+PASS\s+OSFP\s+ColorChip",         
       "F36\s+YES\s+64\s+PASS\s+OSFP\s+ColorChip",         
       "F37\s+YES\s+65\s+PASS\s+OSFP\s+ColorChip",         
       "F38\s+YES\s+66\s+PASS\s+OSFP\s+ColorChip",         
       "F39\s+YES\s+67\s+PASS\s+OSFP\s+ColorChip",         
       "F40\s+YES\s+68\s+PASS\s+OSFP\s+ColorChip",         
       "E41\s+YES\s+73\s+PASS\s+QSFP\s+CELESTICA",         
       "F42\s+YES\s+69\s+PASS\s+OSFP\s+ColorChip",         
       "F43\s+YES\s+70\s+PASS\s+OSFP\s+ColorChip",         
       "E44\s+YES\s+74\s+PASS\s+QSFP\s+CELESTICA",         
       "E45\s+YES\s+71\s+PASS\s+OSFP\s+ColorChip",         
       "E46\s+YES\s+72\s+PASS\s+OSFP\s+TE Connectivity",
        "\(y\) detect_OSFP_QSFP_i2c_device: OSFP/QSFP scan succeeded.",]
    
    minerva_system_gpio_scan_pattern=["gpiochip0 - 256 lines:",
            "line\s+0:\s+unnamed\s+unused\s+(output|input)\s+active-high",
            "line\s+1:\s+unnamed\s+unused\s+(output|input)\s+active-high",
            "line\s+2:\s+unnamed\s+unused\s+(output|input)\s+active-high",
            "line\s+3:\s+unnamed\s+unused\s+(output|input)\s+active-high",
            "line\s+4:\s+unnamed\s+unused\s+(output|input)\s+active-high",
            "line\s+5:\s+unnamed\s+unused\s+(output|input)\s+active-high",
            "line\s+6:\s+unnamed\s+unused\s+(output|input)\s+active-high",
            "line\s+7:\s+unnamed\s+unused\s+(output|input)\s+active-high",
            "line\s+8:\s+unnamed\s+unused\s+(output|input)\s+active-high",
            "line\s+9:\s+unnamed\s+unused\s+(output|input)\s+active-high",
            "line\s+10:\s+unnamed\s+unused\s+(output|input)\s+active-high",
            "line\s+11:\s+unnamed\s+unused\s+(output|input)\s+active-high",
            "line\s+12:\s+unnamed\s+unused\s+(output|input)\s+active-high",
            "line\s+13:\s+unnamed\s+unused\s+(output|input)\s+active-high",
            "line\s+14:\s+unnamed\s+unused\s+(output|input)\s+active-high",
            "line\s+15:\s+unnamed\s+unused\s+(output|input)\s+active-high",
            "line\s+16:\s+unnamed\s+unused\s+(output|input)\s+active-high",
            "line\s+17:\s+unnamed\s+unused\s+(output|input)\s+active-high",
            "line\s+18:\s+unnamed\s+unused\s+(output|input)\s+active-high",
            "line\s+19:\s+unnamed\s+unused\s+(output|input)\s+active-high",
            "line\s+20:\s+unnamed\s+unused\s+(output|input)\s+active-high",
            "line\s+21:\s+unnamed\s+unused\s+(output|input)\s+active-high",
            "line\s+22:\s+unnamed\s+unused\s+(output|input)\s+active-high",
            "line\s+23:\s+unnamed\s+unused\s+(output|input)\s+active-high",
            "line\s+24:\s+unnamed\s+unused\s+(output|input)\s+active-high",
            "line\s+25:\s+unnamed\s+unused\s+(output|input)\s+active-high",
            "line\s+26:\s+unnamed\s+unused\s+(output|input)\s+active-high",
            "line\s+27:\s+unnamed\s+unused\s+(output|input)\s+active-high",
            "line\s+28:\s+unnamed\s+unused\s+(output|input)\s+active-high",
            "line\s+29:\s+unnamed\s+unused\s+(output|input)\s+active-high",
            "line\s+30:\s+unnamed\s+unused\s+(output|input)\s+active-high",
            "line\s+31:\s+unnamed\s+unused\s+(output|input)\s+active-high",
            "line\s+32:\s+unnamed\s+unused\s+(output|input)\s+active-high",
            "line\s+33:\s+unnamed\s+unused\s+(output|input)\s+active-high",
            "line\s+34:\s+unnamed\s+unused\s+(output|input)\s+active-high",
            "line\s+35:\s+unnamed\s+unused\s+(output|input)\s+active-high",
            "line\s+36:\s+unnamed\s+unused\s+(output|input)\s+active-high",
            "line\s+37:\s+unnamed\s+unused\s+(output|input)\s+active-high",
            "line\s+38:\s+unnamed\s+unused\s+(output|input)\s+active-high",
            "line\s+39:\s+unnamed\s+unused\s+(output|input)\s+active-high",
            "line\s+40:\s+unnamed\s+unused\s+(output|input)\s+active-high",
            "line\s+41:\s+unnamed\s+unused\s+(output|input)\s+active-high",
            "line\s+42:\s+unnamed\s+unused\s+(output|input)\s+active-high",
            "line\s+43:\s+unnamed\s+unused\s+(output|input)\s+active-high",
            "line\s+44:\s+unnamed\s+unused\s+(output|input)\s+active-high",
            "line\s+45:\s+unnamed\s+unused\s+(output|input)\s+active-high",
            "line\s+46:\s+unnamed\s+unused\s+(output|input)\s+active-high",
            "line\s+47:\s+unnamed\s+unused\s+(output|input)\s+active-high",
            "line\s+48:\s+unnamed\s+unused\s+(output|input)\s+active-high",
            "line\s+49:\s+unnamed\s+unused\s+(output|input)\s+active-high",
            "line\s+50:\s+unnamed\s+unused\s+(output|input)\s+active-high",
            "line\s+51:\s+unnamed\s+unused\s+(output|input)\s+active-high",
            "line\s+52:\s+unnamed\s+unused\s+(output|input)\s+active-high",
            "line\s+53:\s+unnamed\s+unused\s+(output|input)\s+active-high",
            "line\s+54:\s+unnamed\s+unused\s+(output|input)\s+active-high",
            "line\s+55:\s+unnamed\s+unused\s+(output|input)\s+active-high",
            "line\s+56:\s+unnamed\s+unused\s+(output|input)\s+active-high",
            "line\s+57:\s+unnamed\s+unused\s+(output|input)\s+active-high",
            "line\s+58:\s+unnamed\s+unused\s+(output|input)\s+active-high",
            "line\s+59:\s+unnamed\s+unused\s+(output|input)\s+active-high",
            "line\s+60:\s+unnamed\s+unused\s+(output|input)\s+active-high",
            "line\s+61:\s+unnamed\s+unused\s+(output|input)\s+active-high",
            "line\s+62:\s+unnamed\s+unused\s+(output|input)\s+active-high",
            "line\s+63:\s+unnamed\s+unused\s+(output|input)\s+active-high",
            "line\s+64:\s+unnamed\s+unused\s+(output|input)\s+active-high",
            "line\s+65:\s+unnamed\s+unused\s+(output|input)\s+active-high",
            "line\s+66:\s+unnamed\s+unused\s+(output|input)\s+active-high",
            "line\s+67:\s+unnamed\s+unused\s+(output|input)\s+active-high",
            "line\s+68:\s+unnamed\s+unused\s+(output|input)\s+active-high",
            "ine\s+69:\s+unnamed\s+unused\s+(output|input)\s+active-high",
            "line\s+70:\s+unnamed\s+unused\s+(output|input)\s+active-high",
            "line\s+71:\s+unnamed\s+unused\s+(output|input)\s+active-high",
            "line\s+72:\s+unnamed\s+unused\s+(output|input)\s+active-high",
            "line\s+73:\s+unnamed\s+unused\s+(output|input)\s+active-high",
            "line\s+74:\s+unnamed\s+unused\s+(output|input)\s+active-high",
            "line\s+75:\s+unnamed\s+unused\s+(output|input)\s+active-high",
            "line\s+76:\s+unnamed\s+unused\s+(output|input)\s+active-high",
            "line\s+77:\s+unnamed\s+unused\s+(output|input)\s+active-high",
            "line\s+78:\s+unnamed\s+unused\s+(output|input)\s+active-high",
            "line\s+79:\s+unnamed\s+unused\s+(output|input)\s+active-high",
            "line\s+80:\s+unnamed\s+unused\s+(output|input)\s+active-high",
            "line\s+81:\s+unnamed\s+unused\s+(output|input)\s+active-high",
            "line\s+82:\s+unnamed\s+unused\s+(output|input)\s+active-high",
            "line\s+83:\s+unnamed\s+unused\s+(output|input)\s+active-high",
            "line\s+84:\s+unnamed\s+unused\s+(output|input)\s+active-high",
            "line\s+85:\s+unnamed\s+unused\s+(output|input)\s+active-high",
            "line\s+86:\s+unnamed\s+unused\s+(output|input)\s+active-high",
            "line\s+87:\s+unnamed\s+unused\s+(output|input)\s+active-high",
            "line\s+88:\s+unnamed\s+unused\s+(output|input)\s+active-high",
            "line\s+89:\s+unnamed\s+unused\s+(output|input)\s+active-high",
            "line\s+90:\s+unnamed\s+unused\s+(output|input)\s+active-high",
            "line\s+91:\s+unnamed\s+unused\s+(output|input)\s+active-high",
            "line\s+92:\s+unnamed\s+unused\s+(output|input)\s+active-high",
            "line\s+93:\s+unnamed\s+unused\s+(output|input)\s+active-high",
            "line\s+94:\s+unnamed\s+unused\s+(output|input)\s+active-high",
            "line\s+95:\s+unnamed\s+unused\s+(output|input)\s+active-high",
            "line\s+96:\s+unnamed\s+unused\s+(output|input)\s+active-high",
            "line\s+97:\s+unnamed\s+unused\s+(output|input)\s+active-high",
            "line\s+98:\s+unnamed\s+unused\s+(output|input)\s+active-high",
            "line\s+99:\s+unnamed\s+unused\s+(output|input)\s+active-high",
            "line\s+100:\s+unnamed\s+unused\s+(output|input)\s+active-high",
            "line\s+101:\s+unnamed\s+unused\s+(output|input)\s+active-high",
            "line\s+102:\s+unnamed\s+unused\s+(output|input)\s+active-high",
            "line\s+103:\s+unnamed\s+unused\s+(output|input)\s+active-high",
            "line\s+104:\s+unnamed\s+unused\s+(output|input)\s+active-high",
            "line\s+105:\s+unnamed\s+unused\s+(output|input)\s+active-high",
            "line\s+106:\s+unnamed\s+unused\s+(output|input)\s+active-high",
            "line\s+107:\s+unnamed\s+unused\s+(output|input)\s+active-high",
            "line\s+108:\s+unnamed\s+unused\s+(output|input)\s+active-high",
            "line\s+109:\s+unnamed\s+unused\s+(output|input)\s+active-high",
            "line\s+110:\s+unnamed\s+unused\s+(output|input)\s+active-high",
            "line\s+111:\s+unnamed\s+unused\s+(output|input)\s+active-high",
            "line\s+112:\s+unnamed\s+unused\s+(output|input)\s+active-high",
            "line\s+113:\s+unnamed\s+unused\s+(output|input)\s+active-high",
            "line\s+114:\s+unnamed\s+unused\s+(output|input)\s+active-high",
            "line\s+115:\s+unnamed\s+unused\s+(output|input)\s+active-high",
            "line\s+116:\s+unnamed\s+unused\s+(output|input)\s+active-high",
            "line\s+117:\s+unnamed\s+unused\s+(output|input)\s+active-high",
            "line\s+118:\s+unnamed\s+unused\s+(output|input)\s+active-high",
            "line\s+119:\s+unnamed\s+unused\s+(output|input)\s+active-high",
            "line\s+120:\s+unnamed\s+unused\s+(output|input)\s+active-high",
            "line\s+121:\s+unnamed\s+unused\s+(output|input)\s+active-high",
            "line\s+122:\s+unnamed\s+unused\s+(output|input)\s+active-high",
            "line\s+123:\s+unnamed\s+unused\s+(output|input)\s+active-high",
            "line\s+124:\s+unnamed\s+unused\s+(output|input)\s+active-high",
            "line\s+125:\s+unnamed\s+unused\s+(output|input)\s+active-high",
            "line\s+126:\s+unnamed\s+unused\s+(output|input)\s+active-high",
            "line\s+127:\s+unnamed\s+unused\s+(output|input)\s+active-high",
            "line\s+128:\s+unnamed\s+unused\s+(output|input)\s+active-high",
            "line\s+129:\s+unnamed\s+unused\s+(output|input)\s+active-high",
            "line\s+130:\s+unnamed\s+unused\s+(output|input)\s+active-high",
            "line\s+131:\s+unnamed\s+unused\s+(output|input)\s+active-high",
            "line\s+132:\s+unnamed\s+unused\s+(output|input)\s+active-high",
            "line\s+133:\s+unnamed\s+unused\s+(output|input)\s+active-high",
            "line\s+134:\s+unnamed\s+unused\s+(output|input)\s+active-high",
            "line\s+135:\s+unnamed\s+unused\s+(output|input)\s+active-high",
            "line\s+136:\s+unnamed\s+unused\s+(output|input)\s+active-high",
            "line\s+137:\s+unnamed\s+unused\s+(output|input)\s+active-high",
            "line\s+138:\s+unnamed\s+unused\s+(output|input)\s+active-high",
            "line\s+139:\s+unnamed\s+unused\s+(output|input)\s+active-high",
            "line\s+140:\s+unnamed\s+unused\s+(output|input)\s+active-high",
            "line\s+141:\s+unnamed\s+unused\s+(output|input)\s+active-high",
            "line\s+142:\s+unnamed\s+unused\s+(output|input)\s+active-high",
            "line\s+143:\s+unnamed\s+unused\s+(output|input)\s+active-high",
            "line\s+144:\s+unnamed\s+unused\s+(output|input)\s+active-high",
            "line\s+145:\s+unnamed\s+unused\s+(output|input)\s+active-high",
            "line\s+146:\s+unnamed\s+unused\s+(output|input)\s+active-high",
            "line\s+147:\s+unnamed\s+unused\s+(output|input)\s+active-high",
            "line\s+148:\s+unnamed\s+unused\s+(output|input)\s+active-high",
            "line\s+149:\s+unnamed\s+unused\s+(output|input)\s+active-high",
            "line\s+150:\s+unnamed\s+unused\s+(output|input)\s+active-high",
            "line\s+151:\s+unnamed\s+unused\s+(output|input)\s+active-high",
            "line\s+152:\s+unnamed\s+unused\s+(output|input)\s+active-high",
            "line\s+153:\s+unnamed\s+unused\s+(output|input)\s+active-high",
            "line\s+154:\s+unnamed\s+unused\s+(output|input)\s+active-high",
            "line\s+155:\s+unnamed\s+unused\s+(output|input)\s+active-high",
            "line\s+156:\s+unnamed\s+unused\s+(output|input)\s+active-high",
            "line\s+157:\s+unnamed\s+unused\s+(output|input)\s+active-high",
            "line\s+158:\s+unnamed\s+unused\s+(output|input)\s+active-high",
            "line\s+159:\s+unnamed\s+unused\s+(output|input)\s+active-high",
            "line\s+160:\s+unnamed\s+unused\s+(output|input)\s+active-high",
            "line\s+161:\s+unnamed\s+unused\s+(output|input)\s+active-high",
            "line\s+162:\s+unnamed\s+unused\s+(output|input)\s+active-high",
            "line\s+163:\s+unnamed\s+unused\s+(output|input)\s+active-high",
            "line\s+164:\s+unnamed\s+unused\s+(output|input)\s+active-high",
            "line\s+165:\s+unnamed\s+unused\s+(output|input)\s+active-high",
            "line\s+166:\s+unnamed\s+unused\s+(output|input)\s+active-high",
            "line\s+167:\s+unnamed\s+unused\s+(output|input)\s+active-high",
            "line\s+168:\s+unnamed\s+unused\s+(output|input)\s+active-high",
            "line\s+169:\s+unnamed\s+unused\s+(output|input)\s+active-high",
            "line\s+170:\s+unnamed\s+unused\s+(output|input)\s+active-high",
            "line\s+171:\s+unnamed\s+unused\s+(output|input)\s+active-high",
            "line\s+172:\s+unnamed\s+unused\s+(output|input)\s+active-high",
            "line\s+173:\s+unnamed\s+unused\s+(output|input)\s+active-high",
            "line\s+174:\s+unnamed\s+unused\s+(output|input)\s+active-high",
            "line\s+175:\s+unnamed\s+unused\s+(output|input)\s+active-high",
            "line\s+176:\s+unnamed\s+unused\s+(output|input)\s+active-high",
            "line\s+177:\s+unnamed\s+unused\s+(output|input)\s+active-high",
            "line\s+178:\s+unnamed\s+unused\s+(output|input)\s+active-high",
            "line\s+179:\s+unnamed\s+unused\s+(output|input)\s+active-high",
            "line\s+180:\s+unnamed\s+unused\s+(output|input)\s+active-high",
            "line\s+181:\s+unnamed\s+unused\s+(output|input)\s+active-high",
            "line\s+182:\s+unnamed\s+unused\s+(output|input)\s+active-high",
            "line\s+183:\s+unnamed\s+unused\s+(output|input)\s+active-high",
            "line\s+184:\s+unnamed\s+unused\s+(output|input)\s+active-high",
            "line\s+185:\s+unnamed\s+unused\s+(output|input)\s+active-high",
            "line\s+186:\s+unnamed\s+unused\s+(output|input)\s+active-high",
            "line\s+187:\s+unnamed\s+unused\s+(output|input)\s+active-high",
            "line\s+188:\s+unnamed\s+unused\s+(output|input)\s+active-high",
            "line\s+189:\s+unnamed\s+unused\s+(output|input)\s+active-high",
            "line\s+190:\s+unnamed\s+unused\s+(output|input)\s+active-high",
            "line\s+191:\s+unnamed\s+unused\s+(output|input)\s+active-high",
            "line\s+192:\s+unnamed\s+unused\s+(output|input)\s+active-high",
            "line\s+193:\s+unnamed\s+unused\s+(output|input)\s+active-high",
            "line\s+194:\s+unnamed\s+unused\s+(output|input)\s+active-high",
            "line\s+195:\s+unnamed\s+unused\s+(output|input)\s+active-high",
            "line\s+196:\s+unnamed\s+unused\s+(output|input)\s+active-high",
            "line\s+197:\s+unnamed\s+unused\s+(output|input)\s+active-high",
            "line\s+198:\s+unnamed\s+unused\s+(output|input)\s+active-high",
            "line\s+199:\s+unnamed\s+unused\s+(output|input)\s+active-high",
            "line\s+200:\s+unnamed\s+unused\s+(output|input)\s+active-high",
            "line\s+201:\s+unnamed\s+unused\s+(output|input)\s+active-high",
            "line\s+202:\s+unnamed\s+unused\s+(output|input)\s+active-high",
            "line\s+203:\s+unnamed\s+unused\s+(output|input)\s+active-high",
            "line\s+204:\s+unnamed\s+unused\s+(output|input)\s+active-high",
            "line\s+205:\s+unnamed\s+unused\s+(output|input)\s+active-high",
            "line\s+206:\s+unnamed\s+unused\s+(output|input)\s+active-high",
            "line\s+207:\s+unnamed\s+unused\s+(output|input)\s+active-high",
            "line\s+208:\s+unnamed\s+unused\s+(output|input)\s+active-high",
            "line\s+209:\s+unnamed\s+unused\s+(output|input)\s+active-high",
            "line\s+210:\s+unnamed\s+unused\s+(output|input)\s+active-high",
            "line\s+211:\s+unnamed\s+unused\s+(output|input)\s+active-high",
            "line\s+212:\s+unnamed\s+unused\s+(output|input)\s+active-high",
            "line\s+213:\s+unnamed\s+unused\s+(output|input)\s+active-high",
            "line\s+214:\s+unnamed\s+unused\s+(output|input)\s+active-high",
            "line\s+215:\s+unnamed\s+unused\s+(output|input)\s+active-high",
            "line\s+216:\s+unnamed\s+unused\s+(output|input)\s+active-high",
            "line\s+217:\s+unnamed\s+unused\s+(output|input)\s+active-high",
            "line\s+218:\s+unnamed\s+unused\s+(output|input)\s+active-high",
            "line\s+219:\s+unnamed\s+unused\s+(output|input)\s+active-high",
            "line\s+220:\s+unnamed\s+unused\s+(output|input)\s+active-high",
            "line\s+221:\s+unnamed\s+unused\s+(output|input)\s+active-high",
            "line\s+222:\s+unnamed\s+unused\s+(output|input)\s+active-high",
            "line\s+223:\s+unnamed\s+unused\s+(output|input)\s+active-high",
            "line\s+224:\s+unnamed\s+unused\s+(output|input)\s+active-high",
            "line\s+225:\s+unnamed\s+unused\s+(output|input)\s+active-high",
            "line\s+226:\s+unnamed\s+unused\s+(output|input)\s+active-high",
            "line\s+227:\s+unnamed\s+unused\s+(output|input)\s+active-high",
            "line\s+228:\s+unnamed\s+unused\s+(output|input)\s+active-high",
            "line\s+229:\s+unnamed\s+unused\s+(output|input)\s+active-high",
            "line\s+230:\s+unnamed\s+unused\s+(output|input)\s+active-high",
            "line\s+231:\s+unnamed\s+unused\s+(output|input)\s+active-high",
            "line\s+232:\s+unnamed\s+unused\s+(output|input)\s+active-high",
            "line\s+233:\s+unnamed\s+unused\s+(output|input)\s+active-high",
            "line\s+234:\s+unnamed\s+unused\s+(output|input)\s+active-high",
            "line\s+235:\s+unnamed\s+unused\s+(output|input)\s+active-high",
            "line\s+236:\s+unnamed\s+unused\s+(output|input)\s+active-high",
            "line\s+237:\s+unnamed\s+unused\s+(output|input)\s+active-high",
            "line\s+238:\s+unnamed\s+unused\s+(output|input)\s+active-high",
            "line\s+239:\s+unnamed\s+unused\s+(output|input)\s+active-high",
            "line\s+240:\s+unnamed\s+unused\s+(output|input)\s+active-high",
            "line\s+241:\s+unnamed\s+unused\s+(output|input)\s+active-high",
            "line\s+242:\s+unnamed\s+unused\s+(output|input)\s+active-high",
            "line\s+243:\s+unnamed\s+unused\s+(output|input)\s+active-high",
            "line\s+244:\s+unnamed\s+unused\s+(output|input)\s+active-high",
            "line\s+245:\s+unnamed\s+unused\s+(output|input)\s+active-high",
            "line\s+246:\s+unnamed\s+unused\s+(output|input)\s+active-high",
            "line\s+247:\s+unnamed\s+unused\s+(output|input)\s+active-high",
            "line\s+248:\s+unnamed\s+unused\s+(output|input)\s+active-high",
            "line\s+249:\s+unnamed\s+unused\s+(output|input)\s+active-high",
            "line\s+250:\s+unnamed\s+unused\s+(output|input)\s+active-high",
            "line\s+251:\s+unnamed\s+unused\s+(output|input)\s+active-high",
            "line\s+252:\s+unnamed\s+unused\s+(output|input)\s+active-high",
            "line\s+253:\s+unnamed\s+unused\s+(output|input)\s+active-high",
            "line\s+254:\s+unnamed\s+unused\s+(output|input)\s+active-high",
            "line\s+255:\s+unnamed\s+unused\s+(output|input)\s+active-high",
    "\(y\) gpio.*: GPIO scan test succeeded.",]
    
    
    minerva_mdio_pattern = [
    "Write to PHY 0x12.0x0, value is 0x9a03",
    "Read from PHY 0x12.0x1, value is 0x3102",
    "\(y\) check_mdio_access"
    ]
    
    IOB_FPGA_Path="/run/devmap/fpgas/SMB_IOB_INFO_ROM"
    DOM_FPGA_Path="/run/devmap/fpgas/SMB_DOM_INFO_ROM_0"
    
    minerva_fpga_iob_scratch_test_pattern = [
    "Writing randomly generated bytes .* to scratch pad registers...",
    "Reading the scratch pad registers: .*",
    "\(y\) iob_scratch_test: IOB FPGA scratch pad test succeeded."
    ]
    
    minerva_fpga_dom_scratch_test_pattern = [
    "Writing randomly generated bytes .* to scratch pad registers...",
    "Reading the scratch pad registers: .*",
    "\(y\) dom_scratch_test: DOM FPGA scratch pad test succeeded."
    
    ]
    
    CPLD_SMB1_Path="/run/devmap/cplds/SMB_CPLD_1"
    minerva_cpld1_smb_scratch_test_pattern = [
    "Writing randomly generated byte .* to scratch pad register...",
    "Reading the scratch pad register: .*",
    "\(y\) smb_1_scratch_test: CPLD scratch pad test succeeded."
    ]
    
    CPLD_SMB2_Path="/run/devmap/cplds/SMB_CPLD_2"
    minerva_cpld2_smb_scratch_test_pattern = [
    "Writing randomly generated byte .* to scratch pad register...",
    "Reading the scratch pad register: .*",
    "\(y\) smb_2_scratch_test: CPLD scratch pad test succeeded."
    ]
    
    CPLD_PWR_Path="/run/devmap/cplds/PWR_CPLD"
    minerva_cpld_pwr_scratch_test_pattern = [
    "Writing randomly generated byte .* to scratch pad register...",
    "Reading the scratch pad register: .*",
    "\(y\) pwr_scratch_test: CPLD scratch pad test succeeded."
    ]
    minerva_smb_board_i2c_scan_pattern = ["J3 BRD EEPROM\s+I801 CH1\s+1\s+0x53\s+PASS",
     "SMB_CPLD_1\s+IOB CH2\s+4\s+0x35\s+PASS",
     "VRM_OSFP_3R3V_LEFT\s+IOB CH3\s+5\s+0x7a\s+PASS",
     "VRM_0R75V_0R9_1_L\s+IOB CH3\s+5\s+0x7d\s+PASS",
     "LM75B #LEFTT Inner\s+IOB CH3\s+5\s+0x48\s+PASS",
     "LM75B #RIGHT_BOT\s+IOB CH4\s+6\s+0x49\s+PASS",
     "LM75B #RIGHT_TOP\s+IOB CH4\s+6\s+0x4a\s+PASS",
     "EEPROM\(OOB Switch\)\s+IOB CH5\s+7\s+0x50\s+PASS",
     "Netlake CPLD\s+IOB CH6\s+8\s+0x40\s+PASS",
     "J3 \(Left\)\s+IOB CH7\s+9\s+0x44\s+PASS",
     "EEPROM\(SMB FRU#1\)\s+IOB CH8\s+10\s+0x56\s+PASS",
     "SMB_CPLD_2\s+IOB CH9\s+11\s+0x33\s+PASS",
     "SMB_CPLD_2 \(OSFP\)\s+IOB CH9\s+11\s+0x3e\s+PASS",
     "VRM_OSFP_3R3V_R\s+IOB\s+CH10\s+12\s+0x7e\s+PASS",
     "VRM_1R2_0R9_1_R\s+IOB\s+CH10\s+12\s+0x7a\s+PASS",
     "VRM_0R75_0R9_0_R\s+IOB\s+CH10\s+12\s+0x7b\s+PASS",
     "VRM_1R2_0R9_L\s+IOB\s+CH10\s+12\s+0x76\s+PASS",
     "VRM_VDD_CORE_R\s+IOB\s+CH11\s+13\s+0x60\s+PASS",
     "VRM_0R75V_1R2V_0_L \s+IOB\s+CH11\s+13\s+0x7b\s+PASS",
     "VRM_VDD_CORE_L\s+IOB\s+CH11\s+13\s+0x76\s+PASS",
     "VRM_1R2_0R75_R\s+IOB\s+CH11\s+13\s+0x7d\s+PASS",
     "LM75B #Pwr\(TLVR inner\)\s+IOB\s+CH12\s+14\s+0x48\s+PASS",
     "LM75B #OSFP\(outer\)\s+IOB\s+CH12\s+14\s+0x49\s+PASS",
     "XP12V_COME  PTPS25990\s+IOB\s+CH13\s+15\s+0x4c\s+PASS",
     "PCIe_CLK_buffer_Gen4 RC19004\s+IOB\s+CH13\s+15\s+0x6f\s+PASS",
     "PWR CPLD\s+IOB\s+CH15\s+17\s+0x60\s+PASS",
     "J3 \(Right\)\s+IOB\s+CH16\s+18\s+0x44\s+PASS",
     "BMC EEPROM\s+IOB\s+CH19\s+21\s+0x51\s+PASS",
     "BMC Thermal sensor\s+IOB\s+CH19\s+21\s+0x4a\s+PASS",
     "HBM clock buffer_J3_R\s+IOB\s+CH20\s+22\s+0x6f\s+PASS",
     "LM75B outer\s+IOB\s+CH21\s+23\s+0x4a\s+PASS",
     "48V MAIN HOTSWAP\s+IOB\s+CH21\s+23\s+0x10\s+PASS",
     "ADC128D8 #4\s+IOB\s+CH22\s+24\s+0x37\s+PASS",
     "HBM clock buffer_J3_L\s+IOB\s+CH22\s+24\s+0x6c\s+PASS",
     "ADC128D8 #5\s+IOB\s+CH24\s+26\s+0x1d\s+PASS",
     "ADC128D8 #6\s+IOB\s+CH24\s+26\s+0x37\s+PASS",
     "ADC128D8 #7\s+IOB\s+CH25\s+27\s+0x1d\s+PASS",
     "ADC128D8 #8\s+IOB\s+CH25\s+27\s+0x37\s+PASS",
     "SMB ADC #1\s+IOB\s+CH26\s+28\s+0x1d\s+PASS",
     "SMB ADC #2\s+IOB\s+CH26\s+28\s+0x1f\s+PASS",
     "SMB ADC #3\s+IOB\s+CH26\s+28\s+0x37\s+PASS",
     "\(y\) test_scan_i2c_smb: Scanned 41 i2c devices, 0 failed."
    ]
    minerva_smb_board_spi_scan_pattern = [
    
    ]
    minerva_smb_board_pcie_scan_pattern = [
     "I210 NIC\s+01:00.0\s+PASS",
     "J3 ASIC#0\s+15:00.0\s+PASS",
     "J3 ASIC#1\s+18:00.0\s+PASS",
     "IOB FPGA\s+17:00.0\s+PASS",
    "\(y\) pcie_scan\s+: Scanned 4 devices, 0 missing.",
    
    ]
    minerva_smb_board_nvme_info_pattern = [
    "\(y\) nvme\s+: smartctl 7.2 2020-12-30 r5155 \[x86_64-linux-5.19.0\] \(local build\)",
    "Copyright \(C\) 2002-20, Bruce Allen, Christian Franke, www.smartmontools.org",
    "Error Information \(NVMe Log 0x01, 16 of 64 entries\)",
    "No Errors Logged",
    ]
    minerva_smb_board_nvme_storate_pattern = [
    "\(y\) nvme\s+: .* records in",
    ".* records out",
    ]
    
    minerva_pdb_board_i2c_scan_pattern = [
     "LM75B PDB Thermal sensor\s+IOB CH21\s+23\s+0x48\s+PASS",
     "Power brick #1\s+IOB CH21\s+23\s+0x60\s+PASS",
     "Power brick #2\s+IOB CH21\s+23\s+0x61\s+PASS",
    "\(y\) test_scan_i2c_pdb: Scanned 3 i2c devices, 0 failed.",
    ]
    
    minerva_bmc_board_os_access_pattern = [
    "\(y\) access\s+: bmc-oob.",
    ]
    
    minerva_bmc_board_i2c_scan_pattern = [
    "COMe FRU EEPROM\s+BMC CH0\s+0\s+0x56\s+PASS",
     "COMe Inlet Temp\s+BMC CH0\s+0\s+0x48\s+PASS",
     "COMe Outlet Temp\s+BMC CH0\s+0\s+0x4a\s+PASS",
     "COMe CPLD ADC\s+BMC CH0\s+0\s+0x0f\s+PASS",
     "COMe CPLD Misc Control\s+BMC CH0\s+0\s+0x1f\s+PASS",
     "SMB_CPLD_1\s+BMC CH1\s+1\s+0x35\s+PASS",
     "SMB_FRU#2\s+BMC CH3\s+3\s+0x56\s+PASS",
     "PCA9555\s+BMC CH4\s+4\s+0x27\s+PASS",
     "COMe SML0\s+BMC CH5\s+5\s+0x16\s+PASS",
     "BMC Thermal sensor\s+BMC CH8\s+8\s+0x4a\s+PASS",
     "BMC EEPROM\s+BMC CH8\s+8\s+0x51\s+PASS",
     "PWR_CPLD\s+BMC CH12\s+12\s+0x60\s+PASS",
     "IOBFPGA\s+BMC CH13\s+13\s+0x35\s+PASS",
     "\(y\) test_scan_i2c_bmc: Scanned 13 i2c devices, 0 failed."
    ]
    minerva_bmc_board_spi_scan_pattern = [
    "BIOS Flash.*PASS",
    "IOB Flash.*PASS",
    "\(y\) test_scan_spi_bmc: Scanned 2 spi devices, 0 failed.",
    ]
    minerva_bmc_board_cpu_info_pattern = [
    "\(y\) logic\s+: 2",
    "\(y\) model\s+: ARMv7 Processor rev 5 \(v7l\)",
    
    ]
    minerva_bmc_board_memory_info_pattern = ["\(y\) meminfo\s+:",
    "MemTotal:.*kB",
    "MemFree:.*kB",
    "MemAvailable:.*kB",
    "Buffers:.*kB",
    "Cached:.*kB",
    "SwapCached:.*kB",
    "Active:.*kB",
    "Inactive:.*kB",
    "Active\(anon\):.*kB",
    "Inactive\(anon\):.*kB",
    "Active\(file\):.*kB",
    "Inactive\(file\):.*kB",
    "Unevictable:.*kB",
    "Mlocked:.*kB",
    "HighTotal:.*kB",
    "HighFree:.*kB",
    "LowTotal:.*kB",
    "LowFree:.*kB",
    "SwapTotal:.*kB",
    "SwapFree:.*kB",
    "Dirty:.*kB",
    "Writeback:.*kB",
    "AnonPages:.*kB",
    "Mapped:.*kB",
    "Shmem:.*kB",
    "KReclaimable:.*kB",
    "Slab:.*kB",
    "SReclaimable:.*kB",
    "SUnreclaim:.*kB",
    "KernelStack:.*kB",
    "PageTables:.*kB",
    "SecPageTables:.*kB",
    "NFS_Unstable:.*kB",
    "Bounce:.*kB",
    "WritebackTmp:.*kB",
    "CommitLimit:.*kB",
    "Committed_AS:.*kB",
    "VmallocTotal:.*kB",
    "VmallocUsed:.*kB",
    "VmallocChunk:.*kB",
    "Percpu:.*kB",]
    
    minerva_bmc_board_usb_pattern = [
    "PING fe80::ff:fe00:2%usb0 \(fe80::ff:fe00:2%usb0\): 56 data bytes",
    "--- fe80::ff:fe00:2%usb0 ping statistics ---",
    "3 packets transmitted, 3 packets received, 0% packet loss",
    "round-trip min/avg/max =.*ms",
    "\(y\) check_bmc_ping_usb0: BMC Ping usb0 network succeeded.",
    ]
    
    minerva_bmc_board_bmc_version_pattern = [
    "\(y\) version\s+: ID=poky",
    "NAME=\"Facebook OpenBMC\"",
    "VERSION=\"janga-v0.20 \(master\)\"",
    "VERSION_ID=janga-v0.20",
    "VERSION_CODENAME=\"master\"",
    "PRETTY_NAME=\"Facebook OpenBMC janga-v0.20 \(master\)\"",
    "CPE_NAME=\"cpe:/o:openembedded:poky:janga-v0.20\"",
    ]
    
    minerva_bmc_board_vender_pattern = ["\(y\) vendor",]
    minerva_come_board_i2c_scan_pattern = [
    "COMe FRU eeprom\s+IOB CH14\s+16\s+0x56\s+PASS",
     "COMe OUTLET Sensor\s+IOB CH14\s+16\s+0x4a\s+PASS",
     "COMe INLET Sensor\s+IOB CH14\s+16\s+0x48\s+PASS",
     "COMe CPLD ADC\s+IOB CH14\s+16\s+0x0f\s+PASS",
     "COMe CPLD MISC control\s+IOB CH14\s+16\s+0x1f\s+PASS",
     "VNN_PCH\s+IOB CH23\s+25\s+0x11\s+PASS",
     "1V05_STBY\s+IOB CH23\s+25\s+0x22\s+PASS",
     "PVCCIN_CPU & P1V8 _STBY\s+IOB CH23\s+25\s+0x76\s+PASS",
     "PVDDQ_ABC_CPU\s+IOB CH23\s+25\s+0x45\s+PASS",
     "PVCCANA_CPU\s+IOB CH23\s+25\s+0x66\s+PASS",
     "\(y\) test_scan_i2c_come: Scanned 10 i2c devices, 0 failed.",]
    
    minerva_come_board_bios_version_pattern = [
    "\(y\) get_bios_version: "+minerva_bios_new_version,
    
    ]
    
    minerva_come_board_bios_vendor_pattern = [
    "\(y\) get_bios_vendor : American Megatrends International, LLC.",
    ]
    
    minerva_come_board_cpu_info_pattern = [
    "\(y\) count\s+: 1",
    "\(y\) vendor\s+: GenuineIntel",
    "\(y\) model\s+: Intel\(R\) Xeon\(R\) D-1736  CPU @ 2.30GHz",
    "\(y\) family\s+: 6",
    "\(y\) cores\s+: 8",
    "\(y\) logic\s+: 16",
    ]
    minerva_come_board_cpu_status_pattern = [
    "\(y\) .*",
    "%Cpu\(s\):",
    
    ]
    minerva_come_board_tpm_vendor_pattern = ["\(y\) vendor"]
    
    minerva_come_board_rtc_epoch_pattern = ["\(y\) epoch\s+: .*"]
    minerva_come_board_rtc_timestamp_pattern = ["\(y\) timestamp\s+: .*"]
    minerva_come_board_rtc_hwclock_pattern = ["\(y\) hwclock\s+: hwclock from util-linux 2.37.4",
    "Trying to open: /dev/rtc0",
    "Using the rtc interface to the clock.",
    "Hardware clock is on local time",
    "Assuming hardware clock is kept in local time.",
    "Waiting for clock tick...",
    "...got clock tick",
    "Time since last adjustment is .* seconds",
    "Test mode: nothing was changed.",
    ]
    minerva_bcb_i2c_scan_via_come_pattern = [
    #"i2c i2c-2: Added multiplexed i2c bus 75",
    #"i2c i2c-2: Added multiplexed i2c bus 76",
    #"i2c i2c-2: Added multiplexed i2c bus 77",
    #"i2c i2c-2: Added multiplexed i2c bus 78",
    #"pca954x 2-0070: registered 4 multiplexed busses for I2C switch pca9546",
    #"i2c i2c-2: new_device: Instantiated device pca9546 at 0x70",
    
     "BCB_CPLD 2\s+IOB CH18\s+20\s+0x3c\s+PASS",
     "BCB_CPLD_FAN 2\s+IOB CH18\s+20\s+0x4a\s+PASS",
     "BCB_CPLD\s+ IOB CH0\s+2\s+0x3c\s+PASS",
     "BCB_CPLD_FAN\s+ IOB CH0\s+2\s+0x4a\s+PASS",
     "BCB_CPLD_PROG\s+ IOB CH0\s+2\s+0x40\s+PASS",
     "BCB_PCA9546\s+ IOB CH0\s+2\s+0x70\s+PASS",
     "BCB_XP12R0V_OUT\s+MUX CH1\s+76\s+0x61\s+PASS",
     "BCB_ADC #1\s+MUX CH2\s+77\s+0x1d\s+PASS",
     "BCB_SMB_LM75B\s+MUX CH3\s+78\s+0x48\s+PASS",
     "BCB_SMB_eeprom\s+MUX CH3\s+78\s+0x50\s+PASS",
     "\(y\) detect_smb_i2c_device_bcb: Scanned 10 i2c devices, 0 failed.",
    ]
    
    minerva_bcb_i2c_scan_via_bmc_pattern = [
    #"i2c i2c-6: Ad multiplexed  bus 16",
    #"i2c i2c-6: Ad multiplexed  bus 17",
    #"i2c i2c-6: Ad multiplexed  bus 18",
    #"i2c i2c-6: Ad multiplexed  bus 19",
    #"pca954x 6-007registered 4 tiplexed bussfor I2C switcca9546",
    #"i2c i2c-6: neevice: Instanted device pc46 at 0x70",
    
     "BCB_CPLD 2\s+BMC CH2\s+2\s+0x3c\s+PASS",
     "BCB_CPLD_FAN 2\s+BMC CH2\s+2\s+0x4a\s+PASS",
     "BCB_CPLD 1\s+BMC CH6\s+6\s+0x3c\s+PASS",
     "BCB_CPLD_FAN 1\s+BMC CH6\s+6\s+0x4a\s+PASS",
     "BCB_CPLD_PROG\s+BMC CH6\s+6\s+0x40\s+PASS",
     "BCB_PCA9546\s+BMC CH6\s+6\s+0x70\s+PASS",
     "BCB_PSU\s+BMC CH16\s+16\s+0x58\s+PASS",
     "BCB_XP12R0V_OUT\s+BMC CH17\s+17\s+0x61\s+PASS",
     "BCB_ADC #1\s+BMC CH18\s+18\s+0x1d\s+PASS",
     "BCB_SMB_LM75B\s+BMC CH19\s+19\s+0x48\s+PASS",
     "BCB_SMB_eeprom\s+BMC CH19\s+19\s+0x50\s+PASS",
     "\(y\) detect_bmc_i2c_device_bcb: Scanned 11 i2c devices, 0 failed.",
    
    ]
    minerva_bcb_network_blade_slot_id_pattern = [
    "\(y\) slot_id_show\s+: Slot ID: 0x0e."
    
    ]
    
    minerva_bcb_cmm_present_signal_check_pattern = [
    "\(y\) cmm_prsn_signal_check: CMM present signal detected."
    ]
    
    minerva_bcb_network_blade_power_enable_signal_pattern = [
    "\(y\) nw_pwren_signal_check: Network Blade power enable signal detected.",
    ]
    minerva_system_eeprom_board_fru_pattern=["\(y\) show_brd_fru\s+:"]
    
    minerva_system_eeprom_smb_fru1_pattern=[
    "\(y\) show_smb1_fru\s+:"
    ]
    
    minerva_system_eeprom_smb_fru2_pattern = [
    "\(y\) show_smb2_fru\s+:"]
    
    minerva_j3_system_test_pattern=["\[ a \].*auto \(43\)\s+52",
      "\[ b \].*System Test \(17\)\s+7",
      "\[ c \].*Board Test \(4\)\s+26",
      "\[ d \].*FPGA Test \(2\)\s+4",
      "\[ e \].*CPLD Test \(3\)\s+6",
      "\[ f \].*Firmware Upgrade \(12\)\s+0",
      "\[ g \].*BCB Interface Test \(8\)\s+0",
      "\[ h \].*Stress Test \(12\)\s+0",
      "\[ i \].*Sanity Test \(23\)\s+0",
      "\[ j \].*Snapshot \(1\)\s+0",
      "\[ k \].*MFG Test \(22\)\s+0",]
      
      
    minerva_j3_system_led_test_pattern=[
      "\[ a \]\s+auto \(0\)\s+0",
      "\[ b \]\s+Leakage LED Test \(1\)\s+0",
      "\[ c \]\s+System LED Test \(1\)\s+0",
      "\[ d \]\s+Status LED Test \(1\)\s+0",
      "\[ e \]\s+PORTs LED Blue Test \(1\)\s+0",
      "\[ f \]\s+PORTs LED Green Test \(1\)\s+0",
      "\[ g \]\s+PORTs LED Yellow Test \(1\)\s+0",
      "\[ h \]\s+PORTs LED Off Test \(1\)\s+0",]
      
      
      
    minerva_j3_system_fan_test_pattern=["\[ a \].*auto \(0\)\s+0",
      "\[ b \].*FAN Speed Get Test \(1\)\s+0",
      "\[ c \].*FAN Speed Set Test \(1\)\s+0",
      "\[ q \].*Back to upper menu"]
      
      
    minerva_j3_system_usb_test_pattern=["\[ a \].*auto \(1\)\s+1",
      "\[ b \].*USB Storage Test \(1\)\s+0",
      "\[ c \].*USB Network Test \(1\)\s+1",]
      
    minerva_j3_system_mac_test_pattern=["\[ a \].*auto \(2\)\s+2",
      "\[ b \].*COMe MAC Addr Check \(1\)\s+1",
      "\[ c \].*BMC MAC Addr Check \(1\)\s+1",]
      
    minerva_j3_system_osfp_test_pattern=[
      "\[ a \]\s+auto \(0\)\s+0",
      "\[ b \]\s+I2C SCAN Test \(1\)\s+0",
      "\[ c \]\s+OSFP/QSFP PORTS Enable \(1\)\s+0",
      "\[ d \]\s+OSFP/QSFP PORTS Disable \(1\)\s+0",
      "\[ e \]\s+OSFP/QSFP PORTS Present Check \(1\)\s+0",
      "\[ f \]\s+OSFP/QSFP PORTS Reset Check \(1\)\s+0",
      "\[ g \]\s+OSFP/QSFP PORTS LPMODE Check \(1\)\s+0",
      "\[ h \]\s+OSFP/QSFP PORTS INT Check \(1\)\s+0",
      "\[ i \]\s+OSFP/QSFP PORTS RESET Test \(1\)\s+0",
      "\[ j \]\s+OSFP/QSFP PORTS UNRESET Test \(1\)\s+0",
      "\[ k \]\s+OSFP/QSFP PORTS LPMODE Test \(1\)\s+0",
      "\[ l \]\s+OSFP/QSFP PORTS HPMODE Test \(1\)\s+0",
      "\[ m \]\s+OSFP/QSFP SET LOOPBACK to 16 Watt \(1\)\s+0",
      "\[ n \]\s+OSFP/QSFP SET LOOPBACK to 0 Watt \(1\)\s+0",
      "\[ o \]\s+OSFP/QSFP PORTS TEMPERATURE \(1\)\s+0",
      "\[ p \]\s+OSFP/QSFP PORTS VOLTAGE \(1\)\s+0",
      "\[ r \]\s+OSFP/QSFP PORTS CURRENT \(1\)\s+0",
      "\[ s \]\s+OSFP/QSFP PORTS INT Test \(1\)\s+0",
    ]
    minerva_j3_system_power_cycle_pattern=[ "\[ a \]\s+auto \(0\)\s+0",
      "\[ b \]\s+Power Status \(1\)\s+0",
      "\[ c \]\s+Power Cycle Test \(1\)\s+0",
      "\[ d \]\s+Come Power Cycle Test \(1\)\s+0",]
      
    minerva_j3_system_eeprom_test_pattern = [
      "\[ a \]\s+auto \(0\)\s+0",
      "\[ b \]\s+Show Board FRU \(1\)\s+0",
      "\[ c \]\s+Show SMB FRU 1 \(1\)\s+0",
      "\[ d \]\s+Show SMB FRU 2 \(1\)\s+0"
    ]
    minerva_j3_system_sensor_test_pattern = [
      "\[ a \].*auto \(2\)\s+2",
      "\[ b \].*MP2975 Sensor Check \(1\)\s+1",
      "\[ c \].*E1.S SSD Temperature \(1\)\s+1",
    ]
    
    minerva_j3_board_test_pattern=["\[ a \].*auto \(26\)\s+35",
      "\[ b \].*SMB  Board Test \(4\)\s+4",
      "\[ c \].*PDB  Board Test \(1\)\s+1",
      "\[ d \].*COMe Board Test \(8\)\s+13",
      "\[ e \].*BMC  Board Test \(9\)\s+8",]
      
      
    minerva_j3_smb_board_test_pattern=["\[ a \]\s+auto \(4\)\s+4",
      "\[ b \].*I2C SCAN Test \(1\)\s+1",
      "\[ c \].*SPI SCAN Test \(1\)\s+1",
      "\[ d \].*PCIe SCAN Test \(1\)\s+1",
      "\[ e \].*NVMe Test \(2\)\s+1",
    ]
    		  
    
    minerva_j3_pdb_board_test_pattern=["\[ a \].*auto \(1\)\s+1",
      "\[ b \].*I2C SCAN Test \(1\)\s+1",
     ]
      
      
    minerva_j3_come_board_test_pattern=["\[ a \]\s+auto \(13\)\s+21",
      "\[ b \].*I2C SCAN Test \(1\)\s+1",
      "\[ c \].*BIOS Test \(2\)\s+2",
      "\[ d \].*CPU Test \(2\)\s+2",
      "\[ e \].*MEM Test \(2\)\s+2",
      "\[ f \].*TPM Test \(1\)\s+1",
      "\[ g \].*RTC Test \(3\)\s+3",
      "\[ h \].*USB Test \(2\)\s+2",
      "\[ i \].*Management Ethernet Port Connection Test \(1\)\s+0",]
      
    minerva_j3_bmc_board_test_pattern=["\[ a \].*auto \(8\)\s+9",
      "\[ b \].*OS Access \(1\)\s+1",
      "\[ c \].*I2C SCAN Test \(1\)\s+1",
      "\[ d \].*SPI SCAN Test \(1\)\s+1",                                         
    
      "\[ e \].*CPU Test \(1\)\s+1",
      "\[ f \].*MEM Test \(1\)\s+1",
      
      "\[ g \].*TPM Test \(1\)\s+0",
      "\[ h \].*USB Test \(1\)\s+1",    
      "\[ i \].*PECI Test \(1\)\s+1",
      "\[ v \].*show bmc version \(1\)\s+1",
      
      ]
    
    minerva_j3_fpga_test_pattern=[
      "\[ a \].*auto \(4\)\s+4",
      "\[ b \].*IOB FPGA \(2\)\s+2",
      "\[ c \].*DOM FPGA \(2\)\s+2",]
      
      
    minerva_j3_iob_fpga_test_pattern=[
      "\[ a \]\s+auto \(2\)\s+2", 
      "\[ b \].*Show IOB Version \(1\)\s+1", 
      "\[ c \].*IOB Scratch Test \(1\)\s+1", 
    ]
    minerva_j3_dom_fpga_test_pattern=[
      "\[ a \]\s+auto \(2\)\s+2", 
      "\[ b \].*Show DOM Version \(1\)\s+1", 
      "\[ c \].*DOM Scratch Test \(1\)\s+1", ]
    minerva_j3_cpld_test_pattern=[
      "\[ a \].*auto \(6\)\s+6",
      "\[ b \].*SMB CPLD 1 Test \(2\)\s+2",
      "\[ c \].*SMB CPLD 2 Test \(2\)\s+2",
      "\[ d \].*PWR CPLD Test \(2\)\s+2",  
    ]
    minerva_j3_smb_cpld1_test_pattern=[
      "\[ a \]\s+auto \(2\)\s+2",
      "\[ b \].*Show SMB CPLD 1 Version \(1\)\s+1",
      "\[ c \].*SMB CPLD 1 Scratch Test \(1\)\s+1",
    ]
    minerva_j3_smb_cpld2_test_pattern=[
      "\[ a \]\s+auto \(2\)\s+2",
      "\[ b \].*Show SMB CPLD 2 Version \(1\)\s+1",
      "\[ c \].*SMB CPLD 2 Scratch Test \(1\)\s+1",
    ]
    minerva_j3_pwr_cpld_test_pattern=[
      "\[ a \]\s+auto \(2\)\s+2",
      "\[ b \].*Show PWR CPLD Version \(1\)\s+1",
      "\[ c \].*PWR CPLD Scratch Test \(1\)\s+1",
    ]
    
    minerva_j3_firmware_submenu_pattern=[
      "\[ a \]\s+auto \(0\)\s+0",
      "\[ b \]\s+upgrade iob_fpga flash \(1\)\s+0",
      "\[ c \]\s+upgrade switch ASIC flash \(1\)\s+0",
      "\[ d \]\s+upgrade dom flash \(1\)\s+0",
      "\[ e \]\s+upgrade smb_cpld1 flash \(1\)\s+0",
      "\[ f \]\s+upgrade smb_cpld2 flash \(1\)\s+0",
      "\[ g \]\s+upgrade power_cpld flash \(1\)\s+0",
      "\[ h \]\s+upgrade i210 flash \(1\)\s+0",
      "\[ i \]\s+upgrade i210 MAC addr \(1\)\s+0",
      "\[ j \]\s+upgrade bios flash \(1\)\s+0",
      "\[ k \]\s+upgrade 88e6321 via iob \(1\)\s+0",
      "\[ l \]\s+upgrade smb fru 1 via iob \(1\)\s+0",
      "\[ m \]\s+upgrade brd fru via iob \(1\)\s+0",
    ]
    minerva_j3_stress_submenu_pattern=[
      "\[ a \]\s+auto \(0\)\s+0",
      "\[ b \]\s+CPU Stress \(1\)\s+0",
      "\[ c \]\s+MEM Stress \(1\)\s+0",
      "\[ d \]\s+PTU Stress \(1\)\s+0",
      "\[ e \]\s+NIC Server Stress \(1\)\s+0",
      "\[ f \]\s+NIC Client Stress \(1\)\s+0",
      "\[ g \]\s+I2C Scan Stress \(1\)\s+0",
      "\[ h \]\s+I2C OSFP/QSFP Scan Stress \(1\)\s+0",
      "\[ i \]\s+SPI Scan Stress \(1\)\s+0",
      "\[ j \]\s+PCIe Scan Stress \(1\)\s+0",
      "\[ k \]\s+FPGA Stress \(1\)\s+0",
      "\[ l \]\s+IO Stress \(1\)\s+0",
      "\[ m \]\s+MP2975 Monitoring Stress Test \(1\)\s+0",
    ]
    system_come_mac_addr_pattern = ["\(y\) mac_come_check  :.*"]
    system_bmc_mac_addr_pattern = ["\(y\) mac_bmc_check  :.*"]
    minerva_osfp_port_temp_pattern = ["E1.*YES.*'C",
    "E2.*YES.*'C",
    "E3.*YES.*'C",
    "E4.*YES.*'C",
    "E5.*YES.*'C",
    "E6.*YES.*'C",
    "F1.*YES.*'C",
    "F2.*YES.*'C",
    "F3.*YES.*'C",
    "F4.*YES.*'C",
    "F5.*YES.*'C",
    "F6.*YES.*'C",
    "F7.*YES.*'C",
    "F8.*YES.*'C",
    "F9.*YES.*'C",
    "F10\s+YES\s+\S+\s+'C",
    "F11\s+YES\s+\S+\s+'C",
    "F12\s+YES\s+\S+\s+'C",
    "F13\s+YES\s+\S+\s+'C",
    "F14\s+YES\s+\S+\s+'C",
    "F15\s+YES\s+\S+\s+'C",
    "F16\s+YES\s+\S+\s+'C",
    "F17\s+YES\s+\S+\s+'C",
    "F18\s+YES\s+\S+\s+'C",
    "F19\s+YES\s+\S+\s+'C",
    "F20\s+YES\s+\S+\s+'C",
    "F21\s+YES\s+\S+\s+'C",
    "F22\s+YES\s+\S+\s+'C",
    "F23\s+YES\s+\S+\s+'C",
    "F24\s+YES\s+\S+\s+'C",
    "F25\s+YES\s+\S+\s+'C",
    "F26\s+YES\s+\S+\s+'C",
    "F27\s+YES\s+\S+\s+'C",
    "F28\s+YES\s+\S+\s+'C",
    "F29\s+YES\s+\S+\s+'C",
    "F30\s+YES\s+\S+\s+'C",
    "F31\s+YES\s+\S+\s+'C",
    "F32\s+YES\s+\S+\s+'C",
    "F33\s+YES\s+\S+\s+'C",
    "F34\s+YES\s+\S+\s+'C",
    "F35\s+YES\s+\S+\s+'C",
    "F36\s+YES\s+\S+\s+'C",
    "F37\s+YES\s+\S+\s+'C",
    "F38\s+YES\s+\S+\s+'C",
    "F39\s+YES\s+\S+\s+'C",
    "F40\s+YES\s+\S+\s+'C",
    ]
    
    minerva_osfp_port_voltage_pattern = ["E1\s+YES\s+\S+\s+V",
    "E2\s+YES\s+\S+\s+V",
    "E3\s+YES\s+\S+\s+V",
    "E4\s+YES\s+\S+\s+V",
    "E5\s+YES\s+\S+\s+V",
    "E6\s+YES\s+\S+\s+V",
    "F1\s+YES\s+\S+\s+V",
    "F2\s+YES\s+\S+\s+V",
    "F3\s+YES\s+\S+\s+V",
    "F4\s+YES\s+\S+\s+V",
    "F5\s+YES\s+\S+\s+V",
    "F6\s+YES\s+\S+\s+V",
    "F7\s+YES\s+\S+\s+V",
    "F8\s+YES\s+\S+\s+V",
    "F9\s+YES\s+\S+\s+V",
    "F10\s+YES\s+\S+\s+V",
    "F11\s+YES\s+\S+\s+V",
    "F12\s+YES\s+\S+\s+V",
    "F13\s+YES\s+\S+\s+V",
    "F14\s+YES\s+\S+\s+V",
    "F15\s+YES\s+\S+\s+V",
    "F16\s+YES\s+\S+\s+V",
    "F17\s+YES\s+\S+\s+V",
    "F18\s+YES\s+\S+\s+V",
    "F19\s+YES\s+\S+\s+V",
    "F20\s+YES\s+\S+\s+V",
    "F21\s+YES\s+\S+\s+V",
    "F22\s+YES\s+\S+\s+V",
    "F23\s+YES\s+\S+\s+V",
    "F24\s+YES\s+\S+\s+V",
    "F25\s+YES\s+\S+\s+V",
    "F26\s+YES\s+\S+\s+V",
    "F27\s+YES\s+\S+\s+V",
    "F28\s+YES\s+\S+\s+V",
    "F29\s+YES\s+\S+\s+V",
    "F30\s+YES\s+\S+\s+V",
    "F31\s+YES\s+\S+\s+V",
    "F32\s+YES\s+\S+\s+V",
    "F33\s+YES\s+\S+\s+V",
    "F34\s+YES\s+\S+\s+V",
    "F35\s+YES\s+\S+\s+V",
    "F36\s+YES\s+\S+\s+V",
    "F37\s+YES\s+\S+\s+V",
    "F38\s+YES\s+\S+\s+V",
    "F39\s+YES\s+\S+\s+V",
    "F40\s+YES\s+\S+\s+V",
    "\(y\) show_OSFP_QSFP_voltage: OSFP/QSFP port get voltage succeeded."
    ]
    minerva_osfp_port_current_pattern = ["E1\s+YES\s+\S+\s+A",
    "E2\s+YES\s+\S+\s+A",
    "E3\s+YES\s+\S+\s+A",
    "E4\s+YES\s+\S+\s+A",
    "E5\s+YES\s+\S+\s+A",
    "E6\s+YES\s+\S+\s+A",
    "F1\s+YES\s+\S+\s+A",
    "F2\s+YES\s+\S+\s+A",
    "F3\s+YES\s+\S+\s+A",
    "F4\s+YES\s+\S+\s+A",
    "F5\s+YES\s+\S+\s+A",
    "F6\s+YES\s+\S+\s+A",
    "F7\s+YES\s+\S+\s+A",
    "F8\s+YES\s+\S+\s+A",
    "F9\s+YES\s+\S+\s+A",
    "F10\s+YES\s+\S+\s+A",
    "F11\s+YES\s+\S+\s+A",
    "F12\s+YES\s+\S+\s+A",
    "F13\s+YES\s+\S+\s+A",
    "F14\s+YES\s+\S+\s+A",
    "F15\s+YES\s+\S+\s+A",
    "F16\s+YES\s+\S+\s+A",
    "F17\s+YES\s+\S+\s+A",
    "F18\s+YES\s+\S+\s+A",
    "F19\s+YES\s+\S+\s+A",
    "F20\s+YES\s+\S+\s+A",
    "F21\s+YES\s+\S+\s+A",
    "F22\s+YES\s+\S+\s+A",
    "F23\s+YES\s+\S+\s+A",
    "F24\s+YES\s+\S+\s+A",
    "F25\s+YES\s+\S+\s+A",
    "F26\s+YES\s+\S+\s+A",
    "F27\s+YES\s+\S+\s+A",
    "F28\s+YES\s+\S+\s+A",
    "F29\s+YES\s+\S+\s+A",
    "F30\s+YES\s+\S+\s+A",
    "F31\s+YES\s+\S+\s+A",
    "F32\s+YES\s+\S+\s+A",
    "F33\s+YES\s+\S+\s+A",
    "F34\s+YES\s+\S+\s+A",
    "F35\s+YES\s+\S+\s+A",
    "F36\s+YES\s+\S+\s+A",
    "F37\s+YES\s+\S+\s+A",
    "F38\s+YES\s+\S+\s+A",
    "F39\s+YES\s+\S+\s+A",
    "F40\s+YES\s+\S+\s+A",
    "\(y\) show_OSFP_QSFP_current: OSFP/QSFP port get current succeeded"
    ]
    
    minerva_ospf_ports_high_power_set_pattern = [
    
    "E1\s+YES\s+True",
    "E2\s+YES\s+True",
    "E3\s+YES\s+True",
    "E4\s+YES\s+True",
    "E5\s+YES\s+True",
    "E6\s+YES\s+True",
    "F1\s+YES\s+True",
    "F2\s+YES\s+True",
    "F3\s+YES\s+True",
    "F4\s+YES\s+True",
    "F5\s+YES\s+True",
    "F6\s+YES\s+True",
    "F7\s+YES\s+True",
    "F8\s+YES\s+True",
    "F9\s+YES\s+True",
    "F10\s+YES\s+True",
    "F11\s+YES\s+True",
    "F12\s+YES\s+True",
    "F13\s+YES\s+True",
    "F14\s+YES\s+True",
    "F15\s+YES\s+True",
    "F16\s+YES\s+True",
    "F17\s+YES\s+True",
    "F18\s+YES\s+True",
    "F19\s+YES\s+True",
    "F20\s+YES\s+True",
    "F21\s+YES\s+True",
    "F22\s+YES\s+True",
    "F23\s+YES\s+True",
    "F24\s+YES\s+True",
    "F25\s+YES\s+True",
    "F26\s+YES\s+True",
    "F27\s+YES\s+True",
    "F28\s+YES\s+True",
    "F29\s+YES\s+True",
    "F30\s+YES\s+True",
    "F31\s+YES\s+True",
    "F32\s+YES\s+True",
    "F33\s+YES\s+True",
    "F34\s+YES\s+True",
    "F35\s+YES\s+True",
    "F36\s+YES\s+True",
    "F37\s+YES\s+True",
    "F38\s+YES\s+True",
    "F39\s+YES\s+True",
    "F40\s+YES\s+True",
    "\(y\) test_set_high_power",
    ]
    
    minerva_power_status_pattern = ["\(y\) test_power_status: COMe power is on."]
    wedge_power_status_pattern = "Microserver power is on"
    minerva_osfp_int_pattern = ["\(y\) get_all_port_interrupt_status: All ports interrupt status checked."]
    power_cycle_cancel_pattern=["\(y\) test_power_cycle","User cancelled the power cycle action."]
    minerva_sanity_pattern = [
    "\(y\) test_scan_i2c_smb",
    "\(y\) test_scan_i2c_pdb",
    "\(y\) test_scan_i2c_come",
    "\(y\) test_scan_i2c_bmc",
    "\(y\) detect_osfp_i2c_device",
    "\(y\) test_scan_spi_smb",
    "\(y\) pcie_scan",
    "\(y\) gpio",
    "\(y\) check_usb_access",
    "\(y\) check_ping_usb0",
    "\(y\) check_ping_network",
    "\(y\) check_lpc_access",
    "\(y\) iob_ver_show",
    "\(y\) iob_scratch_test",
    "\(y\) dom_ver_show",
    "\(y\) dom_scratch_test",
    "\(y\) smb_1_ver_show",
    "\(y\) smb_1_scratch_test",
    "\(y\) smb_2_ver_show",
    "\(y\) smb_2_scratch_test",
    "\(y\) pwr_scratch_test",
    "\(y\) version",]
    
    
    minerva_snapshot_pattern = [
    "\[BMC CPU/Memory Usage\]",
    "Status:.*Succeeded",
    "\[BMC Storage Usage\]",
    "Status:.*Succeeded",
    "\[Microserver OS Version\]",
    "Status:.*Succeeded",
    "\[Microserver CPU Usage\]",
    "Status:.*Succeeded",
    "\[Microserver Memory Usage\]",
    "Status:.*Succeeded",
    "\[Microserver Storage Status\]",
    "Status:.*Succeeded",
    "\[BMC FRU EEPROM Info\]",
    "Status:.*Succeeded",
    "\[Sensors Status\]",
    "Status:.*Succeeded",
    "\[Microserver Network Adapter Info\]",
    "Status:.*Succeeded",
    "\[Systemd Status\]",
    "Status:.*Succeeded",
    "\[PCI-E Devices Info\]",
    "Status:.*Succeeded",
    "\[IOB FPGA PCIe Status\]",
    "Status:.*Succeeded",
    "\[I210 Adapter PCIe Status\]",
    "Status:.*Succeeded",
    "\[GPIO Status\]",
    "Status:.*Succeeded",]
    
    minerva_fpga_auto_test_pattern = [
    "\(y\) iob_ver_show",
    "\(y\) iob_scratch_test",
    "\(y\) dom_ver_show",
    "\(y\) dom_scratch_test",
    ]
    
    minerva_dom_fpga_auto_test_pattern = [
    "\(y\) dom_ver_show",
    "\(y\) dom_scratch_test",
    ]
    
    minerva_iob_fpga_auto_test_pattern = [
    "\(y\) iob_ver_show",
    "\(y\) iob_scratch_test",
    ]
    
    minerva_cpld_auto_test_pattern = [
    "\(y\) smb_1_ver_show",
    "\(y\) smb_1_scratch_test",
    "\(y\) smb_2_ver_show",
    "\(y\) smb_2_scratch_test",
    "\(y\) pwr_ver_show",
    "\(y\) pwr_scratch_test",
    ]
    
    minerva_smb_cpld1_auto_test_pattern = [
    "\(y\) smb_1_ver_show",
    "\(y\) smb_1_scratch_test",]
    
    minerva_smb_cpld2_auto_test_pattern = [
    "\(y\) smb_2_ver_show",
    "\(y\) smb_2_scratch_test"]
    
    cpu_stress_pattern=[
    "\(y\) test_CPU_stress\s+:\s+CPU stress has started running."
    ]
    cpu_stress_cancel_pattern=["\(y\) test_CPU_stress : User cancelled starting the function. "]
    mem_stress_cancel_pattern=["\(y\) test_DDR_stress : User cancelled starting the function."]
    mem_stress_pattern=["\(y\) test_DDR_stress : DDR stress has started running."]
    mfg_pattern=["\(y\) test_scan_i2c_smb:",
    "\(y\) test_scan_i2c_pdb:",
    "\(y\) test_scan_i2c_come:",
    "\(y\) test_scan_i2c_bmc:",
    "\(y\) detect_osfp_i2c_device:",
    "\(y\) test_scan_spi_smb:",
    ]
    minerva_test_main_auto_test_pattern=[
    "\(y\) gpio",
    "\(y\) mac_come_check",
    "\(y\) mac_bmc_check",
    "\(y\) check_mdio_access",
    "\(y\) test_scan_i2c_smb",
    "\(y\) test_scan_spi_smb",
    "\(y\) pcie_scan",
    "\(y\) nvme",
    "\(y\) test_scan_i2c_pdb",
    "\(y\) test_scan_i2c_come",
    "\(y\) get_bios_version",
    "\(y\) get_bios_vendor",
    "\(y\) spd",
    "\(y\) vendor",
    "\(y\) epoch",
    "\(y\) timestamp",
    "\(y\) hwclock",
    "\(y\) check_usb_access",
    "\(y\) check_ping_usb0",
    "\(y\) version",
    "\(y\) access",
    "\(y\) test_scan_i2c_bmc",
    ]
    minerva_system_auto_test_pattern=[
    "\(y\) gpio",
    "\(y\) check_ping_usb0",
    "\(y\) mac_come_check",
    "\(y\) mac_bmc_check",
    "\(y\) check_mdio_access",
    ]
    minerva_system_mac_auto_test_pattern=[
    "\(y\) mac_come_check",
    "\(y\) mac_bmc_check",
    ]
    minerva_lpc_pattern=[
    "Device ID\s+: 32",
  	"Device Revision\s+:\s+"+str(minerva_version_dict.get('Device_Revision',"")),
  	"Firmware Revision\s+:\s+"+str(minerva_version_dict.get('Firmware_Revision',"")),
  	"IPMI Version\s+:\s+"+str(minerva_version_dict.get('Ipmi_version',"")),
  	"Manufacturer ID\s+: 40981",
  	"Manufacturer Name\s+:.*",
  	"Product ID\s+: 12614",
  	"Product Name\s+:.*",
  	"Device Available\s+: yes",
  	"Provides Device SDRs\s+: yes",
  	"Additional Device Support :",
  		"Sensor Device",
  		"SDR Repository Device",
  		"SEL Device",
  		"FRU Inventory Device",
  		"IPMB Event Receiver",
  		"IPMB Event Generator",
  		"Chassis Device",
  	"Aux Firmware Rev Info\s+:",
  		"0x00",
  		"0x00",
  		"0x00",
  		"0x00"]
     
    
    minerva_iob_fpga_via_bmc_pattern=[
    "\(y\) iob_bmc"
    ]
    LOOP_COUNT="3"
    TIME_SECONDS="5"
    stress_time_loop_pattern=["\(y\).*Stress test is ceased.Total trials: .*, fails: 0, errors: 0.Please check the log under"]
    minerva_i2c_scan_option="g"
    minerva_i2c_scan_name="I2C Scan Stress"
    
    minerva_i2c_osfp_option="h"
    minerva_i2c_osfp_name="I2C OSFP Scan Stress"
    
    minerva_spi_scan_option="i"
    minerva_spi_scan_name="SPI Scan Stress"
    
    minerva_pcie_scan_option="j"
    minerva_pcie_scan_name="PCIe Scan Stress"
    minerva_come_board_usb_internal_network_pattern=["3 packets transmitted, 3 received, 0% packet loss, time ",
    "\(y\) check_ping_usb0 : Ping command executing succeeded.",]
    
    minerva_conme_board_ethernet_port_pattern=["\(y\) check_ping_external_network: PING " + deviceObj.managementIP,"3 packets transmitted, 3 received, 0% packet loss, time ", ]
    
    minerva_th5_switch_asic_pattern=["\(y\) asic\s+: SPI device j3_2 upgrade succeeded"]
    
    
    
    
    
    
    
    
    
    
    
