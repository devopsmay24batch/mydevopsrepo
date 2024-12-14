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
##### Variable file used for DIAG_OS_test.robot #####
import DeviceMgr
import os
from SwImage import SwImage

deviceObj = DeviceMgr.getDevice()
# Get the variable from the DeviceInfo.yaml
jenkins_info = DeviceMgr.getServerInfo('JENKINS')
server_ipv6 = jenkins_info.managementIPV6
SDK_TOOL = 'auto_load_user.py'
#SDK_PATH = '/usr/local/cls_diag/SDK/gibraltar-sdk/gibraltar-sdk-1.30.1b-src/driver/gibraltar/'
MINIPACK2_SDK_TOOL = 'auto_load_user.sh'
SYSTEM_SDK_PATH = '/usr/local/cls_diag/SDK/'
DIAG_TOOL_PATH='/usr/local/cls_diag/bin/'
BMC_DIAG_TOOL_PATH='/mnt/data1/BMC_Diag/bin/'
BMC_DIAG_UTILITY_PATH='/mnt/data1/BMC_Diag/utility/'
BMC_DIAG_CONFIG_PATH='/mnt/data1/BMC_Diag/configs/'
BMC_DIAG_AC_CONFIG_PATH='/mnt/data1/BMC_Diag/configs/AC_configs/'
BMC_DIAG_DC_CONFIG_PATH='/mnt/data1/BMC_Diag/configs/DC_configs/'
BMC_BLK_MOUNT_PATH='/mnt/data1/'
FW_IMG_PATH='/mnt/data1/'
BLK_DEV_PATH='/dev/mmcblk0'
UTILITY_TOOL_PATH='/usr/local/cls_diag/utility/'
FPGA_STRESS_TOOL_PATH='/usr/local/cls_diag/utility/stress/PCIE_stress/FPGA/'
IPMI_STRESS_TOOL_PATH='/usr/bin/'
SDK_UTIL_PATH='/usr/local/cls_diag/SDK/'
FW_UTIL_PATH='/usr/bin/'
SPI_UTIL_PATH='/usr/local/bin/'
LOG_PATH = 'output/system/'
VAR_LOG_PATH = '/var/log/'
AUTOMATION_ROOT_LOG_PATH = '/mnt/data1/automation/'
SYSTEM_CONSOLE_LOG_PATH = '/mnt/data1/automation/system_log/'
JENKINS_WORKING_DIRECTORY = '/var/lib/jenkins/workspace/wedge400c-system-stress-crobot-test-unit4/'
CPLD_TOOL_PATH = '/usr/local/packages/utils/'
SCM_EEPROM_PATH = '/mnt/data1/BMC_Diag/utility/SCM_eeprom'
FCM_EEPROM_PATH = '/mnt/data1/BMC_Diag/utility/FCM_eeprom'
SMB_EEPROM_PATH = '/mnt/data1/BMC_Diag/utility/SMB_eeprom'
BMC_COMMON_TOOL_PATH = '/mnt/data1/BMC_Diag/common/'
BMC_TEST_DIR_AUTOMATION = "/mnt/data1/automation"
BMC_TEST_DIR_AUTOMATION_SYS_LOG = "/mnt/data1/automation/system_log"
BMC_TEST_DIR_AUTOMATION_LOGFILE = "/mnt/data1/logfile"
BMC_TEST_DIR_AUTOMATION_BIC = "/mnt/data1/BIC"
BMC_TEST_DIR_AUTOMATION_BIOS = "/mnt/data1/BIOS"
BMC_TEST_DIR_AUTOMATION_BMC = "/mnt/data1/BMC"
BMC_TEST_DIR_AUTOMATION_DIAG = "/mnt/data1/BMC_Diag"
BMC_TEST_DIR_AUTOMATION_CPLD = "/mnt/data1/CPLD"
BMC_TEST_DIR_AUTOMATION_FPGA = "/mnt/data1/FPGA"
BMC_TEST_DIR_AUTOMATION_OOB = "/mnt/data1/OOB"
SDK_PORT_STATUS_COMMAND = 'ps'
SDK_SET_PORT_COMMAND = 'port cd'
SDK_PORT_ENABLE_OPTION = 'en=1'
SDK_PORT_DISABLE_OPTION = 'en=0'
SDK_BCM_PROMPT = "BCM.0>"
port_up_status = r'cd\d+.*up'
port_down_status = r'cd\d+.*\!ena'

WEDGE400_POWER_RESET = 'wedge_power.sh'
MP2_POWER_RESET = 'wedge_power.sh reset'
FDISK_UTIL = 'fdisk'
DEFAULT_SCP_TIME = 1200
DISK_INFO_UTIL = 'df'
DEV_USB0_INFO_UTIL = "/dev/ttyUSB0"
EMMC_DISK_INFO_PATTERN =  r'\/dev\/mmcblk(\d+)[ \t]+(\d+)[ \t]+(\d+)[ \t]+(\d+)[ \t]+(\d+)\% \/mnt\/data(\d+)'
PEM_TEST_UTIL = 'cel-pem-test'
PSU_TEST_UTIL = 'cel-psu-test'
PSU_UTIL = 'psu-util'

#################### TCG2-02:
DRIVE_LOAD = 'raw 0x06 0x01 |sed -n 1p |cut -b 2,3'
BMC_DEVICE_ID = '20'
DIAG_Ver = SwImage.getSwImage(SwImage.DIAG).newVersion
DIAG_OS = SwImage.getSwImage(SwImage.DIAG_OS).newVersion
BIOS_Ver = SwImage.getSwImage(SwImage.BIOS).newVersion
BIC_Ver = SwImage.getSwImage(SwImage.BIC).newVersion
BIOS_boot_type = 'master'
BMC_boot_type = 'Master'
FPGA_Ver = SwImage.getSwImage(SwImage.FPGA).newVersion
CPLD_Ver = SwImage.getSwImage(SwImage.CPLD).newVersion  #get the dic type
I210_Ver = SwImage.getSwImage(SwImage.I210).newVersion
SDK_Ver = SwImage.getSwImage(SwImage.SDK).newVersion
sdk_host_soc_dir_w400 = SwImage.getSwImage(SwImage.SDK).hostImageDir
cel_wedge_version_show_pattern = [
    r'(Diag Version):[ \t]+([\d.]+)',
    r'(OS Diag):[ \t]+([\d.]+)',
    r'(BIOS Version):[ \t]+(\w+)',
    r'(FPGA1 Version):[ \t]([\d.]+)',
    r'(FPGA2 Version):[ \t]([\d.]+)',
    r'(SCM CPLD Version):[ \t]([\d.]+)',
    r'(SMB CPLD Version):[ \t]([\d.]+)',
    r'(I210 FW Version):[ \t]([\d.]+)'
]
cel_mp2_version_show_pattern = [
    r'(Diag Version):[ \t]+([\d.]+)',
    r'(OS Diag):[ \t]+([\d.]+)',
    r'(SDK Diag):[ \t]+v([\d.]+)',
    r'(BIOS Version):[ \t]+(\w+)',
    r'(BIOS boot):[ \t]+(\w+)',
    r'(FPGA driver version):[ \t]+([\d.]+)',
    r'(FPGA IOB)[ \t]+([\d.]+)',
    r'(PIM 1 DOM):[ \t]+([\d.]+)[ \t]+16Q',
    r'(PIM 2 DOM):[ \t]+([\d.]+)[ \t]+16Q',
    r'(PIM 3 DOM):[ \t]+([\d.]+)[ \t]+16Q',
    r'(PIM 4 DOM):[ \t]+([\d.]+)[ \t]+16Q',
    r'(PIM 5 DOM):[ \t]+([\d.]+)[ \t]+16Q',
    r'(PIM 6 DOM):[ \t]+([\d.]+)[ \t]+16Q',
    r'(PIM 7 DOM):[ \t]+([\d.]+)[ \t]+16Q',
    r'(PIM 8 DOM):[ \t]+([\d.]+)[ \t]+16Q',
    r'(I210 FW Version):[ \t]+([\d.]+)'
]
PCIE_TOOL = 'lspci'
PCIE_NUM = 'lspci | wc -l'
wedge_pcie_num = '77'
mp2_pcie_num = '87'
SCAN_BUS_05 = 'lspci -s 05:00.0 -vvv'
SCAN_BUS_06 = 'lspci -s 06:00.0 -vvv'
SCAN_BUS_07 = 'lspci -s 07:00.0 -vvv'
SCAN_BUS_08 = 'lspci -s 08:00.0 -vvv'
wedge_bus_05 = [
    r'^(0\d:00.0) Communication controller:.*',
    r'LnkSta:[ \t]+Speed[ \t]+(\d\.?\d?G)T/s,[ \t]+Width[ \t]+(x\d)'
]
w400c_bus_06 = [
    r'^(0\d:00.0)[ \t]+Non-VGA unclassified device:.*',
    r'LnkSta:[ \t]+Speed[ \t]+(\d\.?\d?G)T/s,[ \t]+Width[ \t]+(x\d)'
]
wedge_bus_06 = [
    r'^(0\d:00.0)[ \t]+Ethernet controller:.*',
    r'LnkSta:[ \t]+Speed[ \t]+(\d\.?\d?G)T/s,[ \t]+Width[ \t]+(x\d)'
]
wedge_bus_07 = [
    r'^(0\d:00.0)[ \t]+Non-Volatile memory controller:.*',
    r'LnkSta:[ \t]+Speed[ \t]+(\d\.?\d?G)T/s,[ \t]+Width[ \t]+(x\d)'
]
wedge_bus_08 = [
    r'^(0\d:00.0)[ \t]+Communication controller:.*',
    r'LnkSta:[ \t]+Speed[ \t]+(\d\.?\d?G)T/s,[ \t]+Width[ \t]+(x\d)'
]

mp2_bus_06 = [
    r'^(0\d:00.0)[ \t]+Ethernet controller:.*',
    r'LnkSta:[ \t]+Speed[ \t]+(\d\.?\d?G)T/s,[ \t]+Width[ \t]+(x\d)'
]
mp2_bus_07 = [
    r'^(0\d:00.0)[ \t]+Non-Volatile memory controller:.*',
    r'LnkSta:[ \t]+Speed[ \t]+(\d\.?\d?G)T/s,[ \t]+Width[ \t]+(x\d)'
]
mp2_bus_08 = [
    r'^(0\d:00.0)[ \t]+PCI bridge:.*',
    r'LnkSta:[ \t]+Speed[ \t]+(\d\.?\d?G)T/s,[ \t]+Width[ \t]+(x\d)'
]
fdisk_tool = 'fdisk -l'
usbdev_tool = 'fdisk -l |grep /dev/ |grep -v nvme |wc -l'
ssddev_tool = 'fdisk -l |grep /dev/nvme |wc -l'
usbdev_num = '2'
ssddev_num = '4'
ETH_TOOL = 'ifconfig -a'
SENSOR_UTIL = 'sensor-util'
SENSOR_PATTERN = r'^([A-Z]\w+)[ \t]+\(0x\w{1,2}\)[ \t]+:[ \t]+(.*)[ \t]+\| \((ok)\)'
WEUTIL_TOOL = 'weutil'
FEUTIL_TOOL = 'feutil'
SEUTIL_TOOL = 'seutil'
PEUTIL_TOOL = 'peutil'
SIM_EEPROM_PATH = '/mnt/data1/BMC_Diag/utility/SIM_eeprom'
FAN_EEPROM_PATH = '/mnt/data1/BMC_Diag/utility/FAN_eeprom'
EEPROM_PATH = '/mnt/data1/BMC_Diag/utility/eeprom'
FCMT_EEPROM_PATH = '/mnt/data1/BMC_Diag/utility/FCM_T_eeprom'
FCMB_EEPROM_PATH = '/mnt/data1/BMC_Diag/utility/FCM_B_eeprom'
PIM_EEPROM_PATH = '/mnt/data1/BMC_Diag/utility/PIM_eeprom'
EEPROM_TOOL = 'eeprom_tool -d'
FAN_EEPROM_TOOL = 'eeprom_tool -d -f'
map_key_dict = {
    'Version' : 'format_version',
    'Product Part Number' : 'top_level_product_part_number',
    'Local MAC' : 'local_mac_address',
    'Extended MAC Base': 'extended_mac_address_base',
    'Location on Fabric' : 'eeprom_location_on_fabric'
}

#################### TCG2-03:
BCMTOOL = 'bcm.user'
CLSTOOL = 'cls_shell'
truncateTool = 'truncate -s 0 temp.txt'
PortUPStatus = "tail -n +3 temp.txt|grep -a cd |grep up|awk -F'[(]' '{print $1}'|wc |awk '{print $1}'"
mp2_traffic_script = 'minipack2_auto_stress_test.sh'
mp2_traffic_counter = 'portdump counters all'
TRAFFIC_PATTERN = '^Port\d{1,3}[ \t]+couters[ \t]+\(tx=\d+, rx=\d+\)[ \t]+passed'
#################### TCG2-06:
FlashHigh = 'high'
FlashLow = 'low'
BMCImage = 'BMC'
BIOSImage = 'BIOS'
CPLDImage = 'CPLD'
BICImage = 'BIC'
FPGAImage = 'FPGA'
bmcModePattern = r'Current Boot Code Source:[ \t]+(\w+)[ \t]+Flash'
scm_version_pattern = [
    r'(Bridge-IC Version):[ \t]+(v.*)',
    r'(Bridge-IC Bootloader Version):[ \t]+(v.*)',
    r'(BIOS Version):[ \t]+(.*)',
    r'(CPLD Version):[ \t]+(.*)',
    r'(ME Version):[ \t]+(.*)',
    r'(PVCCIN VR Version):[ \t]+(.*)',
    r'(DDRAB VR Version):[ \t]+(.*)',
    r'(P1V05 VR Version):[ \t]+(.*)'
]

#################### TCG2-07:
wedge_all_version_pattern = [
    r'(BMC Version):[ \t]+wedge400-v(.*)',
    r'(FCMCPLD):[ \t]+(.*)',
    r'(PWRCPLD):[ \t]+(.*)',
    r'(SCMCPLD):[ \t]+(.*)',
    r'(SMBCPLD):[ \t]+(.*)',
    r'(DOMFPGA1):[ \t]+(.*)',
    r'(DOMFPGA2):[ \t]+(.*)',
]
mp2_all_version_pattern = [
    r'(BMC Version):[ \t]+fuji-v(.*)',
    r'(FCMCPLD B):[ \t]+(.*)',
    r'(FCMCPLD T):[ \t]+(.*)',
    r'(PWRCPLD L):[ \t]+(.*)',
    r'(PWRCPLD R):[ \t]+(.*)',
    r'(SCMCPLD):[ \t]+(.*)',
    r'(SMBCPLD):[ \t]+(.*)',
    r'(IOB FPGA):[ \t]+(.*)',
    r'(PIM1 DOMFPGA):[ \t]+(.*)',
    r'(PIM2 DOMFPGA):[ \t]+(.*)',
    r'(PIM3 DOMFPGA):[ \t]+(.*)',
    r'(PIM4 DOMFPGA):[ \t]+(.*)',
    r'(PIM5 DOMFPGA):[ \t]+(.*)',
    r'(PIM6 DOMFPGA):[ \t]+(.*)',
    r'(PIM7 DOMFPGA):[ \t]+(.*)',
    r'(PIM8 DOMFPGA):[ \t]+(.*)',
]

#################### TCG2-08:
fpga_ver_tool = 'fpga_ver.sh'
fpga_update_tool_lst = ["spi_util.sh write spi1 DOM_FPGA_FLASH1"]
mp2_fpga_update_tool_lst = ['pim_upgrade.sh all', 'reinit_all_pim.sh', 'spi_util.sh write spi1 IOB_FPGA']
fpga_update_pattern = ['Erase/write done.']

#################### TCG2-09:
STRESSAPP_TOOL = 'stressapptest'
w400_DD_stop_traffic = './cls_shell pvlan set cd15 1888'
w400_56_stop_traffic = './cls_shell pvlan set cd47 1889'
w400_traffic_counter = './cls_shell show c CDMIB_RPKT.cd0-cd47; ./cls_shell show c CDMIB_TPKT.cd0-cd47; ./cls_shell show c CDMIB_RFCS'
w400_exit_traffic_cmd = './cls_shell exit'

#################### TCG2-10:
MP2TOOLPATH = '/home/automation/Auto_Test/automation/FB-Minipack2/autotest/tools'
W400TOOLPATH = '/home/automation/Auto_Test/automation/FB-Wedge400C/autotest/downloadable'

#################### TCG2-19:
RESET_PMD = "dsh -c 'phy 1-262 0x7001d069 1'"
RESET_PMD_W400 = "phy cd DSC_SM_CTL9r RX_RESTART_PMD=1"

#################### TCG2-20:
LPMODE_OFF_TOOL = '-p0 --lpmode=off'
LPMODE_ON_TOOL = '-p0 --lpmode=on'
RESET_ON_TOOL = '-p0 --reset=on'
RESET_OFF_TOOL = '-p0 --reset=off'
PS_CE_TOOL = 'ps ce'
TAIL_TOOL = 'tail -n +2 temp.txt'
ECHO_TOOL = 'echo'
init_remote_shell = '-m 16x100G_32x100G_NRZ_optics -df temp.txt'
upPort_lpmode = " |grep -a ce |grep up|awk -F'[(]' '{print $1}'|wc |awk '{print $1}'"
downPort_lpmode = " |grep -a ce |grep 'down'|awk -F'[(]' '{print $1}'|wc |awk '{print $1}'"
optical_snake_vlan = 'snake_script_optical_100G'
traffic_snake = 'tx 10000 pbm=ce0,ce47 ubm=ce L=1500'

######################################################################################################
ipmi_toolName="ipmitool"
cel_ipmitool_pattern = [
    r'Device ID([ \t])+:([ \t])+(\d+)',
    r'Device Revision([ \t])+:([ \t])+(\d+)',
    r'Firmware Revision([ \t])+:([ \t])+((\d+).(\d+))',
    r'IPMI Version([ \t])+:([ \t])+((\d+).(\d+))',
    r'Manufacturer ID([ \t])+:([ \t])+(\d+)',
    r'Manufacturer Name([ \t])+:([ \t])+(\w+)([ \t])+\(([\w,\d]+)\)',
    r'Product ID([ \t])+:([ \t])+(\d+)([ \t])+\(([\w,\d]+)\)',
    r'Product Name([ \t])+:([ \t])+(\w+)([ \t])+\(([\w,\d]+)\)',
    r'Device Available([ \t])+:([ \t])+yes',
    r'Provides Device SDRs([ \t])+:([ \t])+yes',
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
]

CMD_APP_NETFN='raw 0x06'
openbmc_mode='openbmc'
centos_mode='centos'
default_mode=centos_mode
centos_eth_params = {
    'interface' : 'eth0',
    'usb_interface' : 'usb0',
    }
openbmc_eth_params = {
    'interface' : 'eth0',
    'usb_interface' : 'usb0',
    }

scp_username = jenkins_info.scpUsername
scp_password = jenkins_info.scpPassword
scp_ip = jenkins_info.managementIP
scp_ipv6 = jenkins_info.managementIPV6
scp_static_ipv6 = jenkins_info.staticIPV6
host_prompt = jenkins_info.prompt

test_pass_pattern='\s+\|.+PASS.+\|'

##### TC-1001-MANAGEMENT-ETHER-PORT-MAC-TEST #####
cel_mac_help_array = {
    "bin_tool" : "cel-mac-test",
    "all_option" : "Check if MAC belong to Quanta",
    "help_option" : "Display this help text and exit",
    }
mac_test_keyword='MAC test'

#### TCG1_01-Sensor_Reading_Stress-High_Loading ####
W400_SDK_TOOL = 'auto_load_user.sh'
w400_start_cpu_traffic_cmd = "cls_shell snake_script_loopback_16x400G_32x200G_PAM4.soc"
w400_stop_cpu_traffic_cmd = "cls_shell pvlan set cd15,cd47 1666"
w400_exit_cpu_traffic_cmd = "cls_shell exit"

##### TC-1002-CPU-INFORMATION-TEST #####
cel_cpu_help_array = {
    "bin_tool" : "cel-cpu-test",
    "all_option" : "Show the CPU information and check if it is correct",
    "help_option" : "Display this help text and exit",
    }
cpu_test_keyword='CPU test'

##### TC-1003-ACCESS-FPGA-TEST #####
cel_fpga_help_array = {
    "bin_tool" : "cel-fpga-test",
    "all_option" : "Test all configure options",
    "help_option" : "Display this help text and exit",
    }
fpga_test_keyword='FPGA test'

##### TC-1004-DIMM-SPD-TEST #####
cel_mem_help_array = {
    "bin_tool" : "cel-memory-test",
    "all_option" : "Test all configure options",
    "check_option" : "Check memory block in one minute",
    "help_option" : "Display this help text and exit",
    }
mem_test_keyword='Memory list check'
mem_check_pattern='[\d\-\w\s]+\s*\:.+ok'

##### TC-1005-USB-STORAGE-TEST #####
cel_usb_help_array = {
    "bin_tool" : "cel-usb-test",
    "all_option" : "Test all configure options",
    "info_option" : "Show all usb SSDs smart information",
    "help_option" : "Display this help text and exit",
    }
usb_info_array = {
    "Vendor" : "SanDisk",
    "Product" : "Ultra USB 3.0",
    "Revision" : "1.00",
    "Compliance" : "SPC-4",
    "User Capacity" : "15,376,318,464 bytes [15.3 GB]",
    "Logical block size" : "512 bytes",
    }
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
rtc_test_keyword='Rtc test'
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
    "check_option" : "Check chip_type and PCR0 data",
    }
tpm_test_keyword='TPM testall'
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
nvme_test_keyword='nvme test'
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
oob_config_file='/usr/local/cls_diag/CPU_Diag/configs/oob.yaml'

##### TC-1016-CPLD-TEST#####
cpld_version_tool='cpld_ver.sh'
mp2_cpld_version_tool = 'fw-util cpld --version'
mp2_cpld_update_tool = ['cpld_update.sh -s']
mp2_fpga_version_tool = 'fw-util fpga --version'
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
flash_device_path='/dev/mtd5'
bmc_update_stress_log = "BMC-Update-Stress"

##### TC-1103-BIOS-UPDATE-TEST#####
spiUtil_tool='spi_util.sh'
boot_info_util='boot_info.sh'
diag_cpu_bios_ver_bin='cel-version-test'
spiUtil_write_pattern = ['Config SPI1 Done.',
                            'Erase/write done.']
spiUtil_read_pattern = ['Config SPI1 Done.',
                            'Reading flash... done.']
bios_ver_pattern='BIOS Version: ([\w\d\_]+)'
fw_util_option='scm --update --bios'
fw_util_tool='fw-util'
fw_util_optionStr = 'all --version'
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
    "BRIDGE_VER" : "v1.11",
    "BRIDGE_BOOTLOADER_VER" : "v1.10",
    "BIOS_VER" : "XG1_3A09",
    "CPLD_VER" : "0x00010032",
    "ME_VER" : "3.0.3.45",
    "PVCCIN_VER" : "0x54c8, 0xe9d6",
    "DDRAB_VER" : "0xb41b, 0xe66c",
    "P1V05_VER" : "0x54c8, 0xe9d6",
    }

bic_util_tool = 'bic-util'
bic_util_optionStr = 'scm --get_dev_id'
#bic_util_optionList = ['scm --get_dev_id',
#                       'scm --get_gpio',
#                       'scm --get_gpio_config',
#                       'scm --get_config',
#                       'scm --get_post_code',
#                       'scm --get_sdr',
#                       'scm --read_sensor',
#                       'scm --read_fruid',
#                       'scm --read_mac',
#                      ]

##### TC-1104-TH3-UPDATE-TEST #####
th3_upgrade_file='pciefw_2.06.bin'
th3_downgrade_file='pciefw_2.05.bin'
th3_upgrade_ver='2.6'
th3_downgrade_ver='2.5'
th3_package_copy_list = [th3_upgrade_file,th3_downgrade_file]
th3_img_path='/mnt/data1/'
sdk_file='auto_load_user.sh'
th3_ver_command='pciephy fw version'
th3_ver_pattern='PCIe FW loader version: ([\.\d]+)'

##### TC-1105-FPGA-UPDATE-TEST #####
fpga_software_test='cel-software-test'
fpga1_ver_pattern='DOM_FPGA_1\s+:\s+([\d\.]+)'
fpga2_ver_pattern='DOM_FPGA_2\s+:\s+([\d\.]+)'
fpga_update_stress_log = 'FPGA-Update-Stress'

cel_cpld_fpga_bic_version_array = {
    "FCMCPLD" : "4.2",
    "PWRCPLD" : "2.3",
    "SCMCPLD" : "4.0",
    "SMBCPLD" : "4.0",
    "DOMFPGA1" : "0.56",
    "DOMFPGA2" : "0.56",
    "BRIDGE_VER" : "v1.11",
    "BRIDGE_BOOTLOADER_VER" : "v1.10",
    "CPLD_VER" : "0x00010032",
    }

fpga1_list_cmd = 'lspci -s 05:00.0 -vvv'
fpga2_list_cmd = 'lspci -s 08:00.0 -vvv'
fpga1_pcie_device_id_string = '05:00.0 Communication controller: Facebook, Inc. Device 7012'
fpga2_pcie_device_id_string = '08:00.0 Communication controller: Facebook, Inc. Device 7012'

##### TCG1-07-FPGA-PCIE-BUS-STRESS-TEST #####
fpga_stress_tool = 'fpga_stress.sh'


##### TC-1106-BIC-UPDATE-TEST #####
cpu_uart_log = "mTerm_wedge"
openbmc_uart_log = "terminal_uart"
bic_software_test='cel-software-test'
bic_ver_pattern='Bridge-IC Version:\s+(v[\d\.]+)'
bic_update_pattern = ['updated bic: 100 %', 'Upgrade of scm : bic succeeded']
bic_update_stress_log = "BIC-Update-Stress"

##### TC-1107-FCM-UPDATE-TEST #####
fcm_software_test='cel-software-test'
fcm_ver_pattern='FCM_CPLD\s+:\s+([\d\.]+)'
fcm_update_pattern = ['Upgrade successful.']
fcm_cpld_tool='fcmcpld_update.sh'

##### TC-1108-SCM-UPDATE-TEST #####
scm_software_test='cel-software-test'
scm_ver_pattern='SCM_CPLD\s+:\s+([\d\.]+)'
scm_update_pattern = ['Upgrade successful.']
scm_cpld_tool='scmcpld_update.sh'

##### TC-1109-SYSTEM-UPDATE-TEST #####
cpld_update_stress_log = "CPLD-Update-Stress"
cpld_update_pattern = ['100%','Upgrade successful.']

smb_software_test='cel-software-test'
smb_ver_pattern='SMB_CPLD\s+:\s+([\d\.]+)'
smb_update_pattern = ['Upgrade successful.']
smb_cpld_tool='smbcpld_update.sh'

##### TC-1110-POWER-UPDATE-TEST #####
pwr_software_test='cel-software-test'
pwr_ver_pattern='PWR_CPLD\s+:\s+([\d\.]+)'
pwr_update_pattern = ['Upgrade successful.']
pwr_cpld_tool='pwrcpld_update.sh'

##### TC-1115-BMC-CPU-TEST #####
cel_bmc_cpu_help_array = {
    "bin_tool" : "cel-CPU-test",
    "all_option" : "test CPU",
    "info_option" : "show CPU info",
    "help_option" : "show this help",
    }
bmc_cpu_keyword_pattern = ['get_cpu_info',
                            'get_cpu_status',
                            'check_processor_number',
                            'check_cpu_model']

cel_bmc_cpu_info_array = {
    "processor" : "0",
    "model_name" : "ARMv6-compatible processor rev 7 (v6l)",
    "BogoMIPS" : "49.50",
    "Features" : "half thumb fastmult edsp java tls",
    "CPU_implementer" : "0x41",
    "CPU_architecture" : "7",
    "CPU_variant" : "0x0",
    "CPU_part" : "0xb76",
    "CPU_revision" : "7",
    "Hardware" : "Generic DT based system",
    "Revision" : "0000",
    "Serial" : "0000000000000000",
    }

bmc_cpu_help_pattern = ['Usage\:\s+\.\/(cel-[\w\-]+)\s+options\s+\([\-\w\|]+\)',
                        '-a\s+([\w\s]+)',
                        '-h\s+([\w\s]+)',
                        '-i\s+([\w\s]+)',
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
    "select_option" : "FPGA name(DOM_FPGA_1 DOM_FPGA_2)",
    "reg_addr_option" : "FPGA register address",
    "data_option" : "data written to FPGA",
    "version_option" : "FPGA version",
    "test_option" : "test FPGA",
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
bmc_fpga_keyword_pattern = ['check_fpga_scratch',
                            'show_FPGA_version',]

##### TC-1117-BMC-CPLD-TEST #####
cel_bmc_cpld_help_array = {
    "bin_tool" : "cel-cpld-test",
    "help_option" : "help information",
    "write_option" : "write to CPLD",
    "read_option" : "read from CPLD",
    "select_option" : "CPLD name(FCM_CPLD SCM_CPLD SMB_CPLD PWR_CPLD)",
    "reg_addr_option" : "CPLD register address",
    "data_option" : "data written to CPLD",
    "version_option" : "CPLD version",
    "test_option" : "test CPLD",
    }
bmc_cpld_help_pattern = ['Usage\:\s+\.\/(cel-[\w\-]+)\s+options\s+.+',
                        '-h\s+(.+)',
                        '-w\s+(.+)',
                        '-r\s+(.+)',
                        '-c\s+(.+)',
                        '-s\s+(.+)',
                        '-d\s+(.+)',
                        '-v\s+(.+)',
                        '-a\s+(.+)',
                        ]
bmc_cpld_keyword_pattern = ['check_cpld_scratch',
                            'show_CPLD_version',
                            'check_cpld_jtag',
                            ]
cel_bmc_cpld_version_array = {
    "FCM_CPLD" : "4.2",
    "SCM_CPLD" : "4.0",
    "SMB_CPLD" : "4.0",
    "PWR_CPLD" : "2.3",
    }
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

cel_bmc_scm_auto_eeprom_pattern = [
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

cel_bmc_fcm_auto_eeprom_pattern = [
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

cel_bmc_smb_auto_eeprom_pattern = [
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

cel_bmc_eeprom_tool_d_pattern = [
    r'#([ \t]+)?(\.\/)?eeprom_tool[ \t]+-d',
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

bmc_cel_boot_test_h_pattern = [
    r'#[ \t]*(\./)?cel-boot-test[ \t]+-h$',
    r'Usage:[ \t]+\./cel-boot-test[ \t]+options[ \t]+\(-h\|-s\|-a\|\[-b[ \t]+<bmc\|bios>\]\|\[-r[ \t]+<master\|slave>\]\)$',
    r'[ \t]*-h[ \t]+Show[ \t]+this[ \t]+help$',
    r'[ \t]*-b[ \t]+<bmc\|bios>$',
    r'[ \t]*-s[ \t]+Show[ \t]+boot[ \t]+status$',
    r'[ \t]*-r[ \t]+Boot[ \t]+from[ \t]<master\|slave>$',
    r'[ \t]*-a[ \t]+Auto[ \t]+test$',
]

cel_boot_test_b_bmc_s = {
    "bin_tool": "cel-boot-test",
    "wdt1": "WDT1 Timeout Count",
    "wdt2": "WDT2 Timeout Count",
    "current_boot": "Current Boot Code Source",
}

cel_boot_test_b_bmc_s_pattern = [
    r'#[ \t]*(\./)?cel-boot-test[ \t]+-b[ \t]+bmc[ \t]+-s$',
    r'WDT1[ \t]+Timeout[ \t]+Count:[ \t]+\d$',
    r'WDT2[ \t]+Timeout[ \t]+Count:[ \t]+\d$',
    r'Current[ \t]+Boot[ \t]+Code[ \t]+Source:[ \t]+(Slave|Master)[ \t]+Flash$',
]

cel_boot_test_b_bmc_r_slave = {
    "bin_tool": "cel-boot-test",
}

cel_boot_test_b_bmc_r_slave_pattern = [
    r'#[ \t]*(\./)?cel-boot-test[ \t]+-b[ \t]+bmc[ \t]+-r[ \t]+slave$',
    r'Current[ \t]+boot[ \t]+source[ \t]+is[ \t]+slave,[ \t]+no[ \t]+need[ \t]+to[ \t]+switch\.$',
]

#### FB-DIAG-COM-TS-041-FAN-TEST ####
cel_fan_test = {
    "bin_tool": "cel-fan-test",
}

cel_fan_test_h_pattern = [
    r'#[ \t]*(\./)?cel-fan-test[ \t]+-h$',
    r'^Usage:[ \t]+\./cel-fan-test[ \t]+options[ \t]+\(-h\|-g\|-s\|-e\|-a\|\[-p[ \t]+speed\]\|\[-c[ \t]+fan_type\]\)$',
    r'^[ \t]*-h[ \t]+help[ \t]+information$',
    r'^[ \t]*-p[ \t]+set[ \t]+fan[ \t]+speed\(%\):[ \t]+Eg,[ \t]+-p[ \t]+\d{1,3}[ \t]+\(means[ \t]+set[ \t]+\d{1,3}%[ \t]+speed[ \t]+of[ \t]+fans\)$',
    r'^[ \t]*-g[ \t]+get[ \t]+fan[ \t]+speed$',
    r'^[ \t]*-s[ \t]+get[ \t]+fan[ \t]+status$',
    r'^[ \t]*-e[ \t]+test[ \t]+fan[ \t]+enable[ \t]+disable[ \t]+functions$',
    r'^[ \t]*-a[ \t]+test[ \t]+fan$',
    r'^[ \t]*-c[ \t]+check[ \t]+setting[ \t]+fan[ \t]+value:[ \t]+Eg,[ \t]+-c[ \t]+(SANYO|AVC)[ \t]+\(indicate[ \t]+fans[ \t]+are[ \t]+SANYO[ \t]+or[ \t]+AVC\)$',
]

cel_fan_test_g_pattern = [
    r'# [ \t]*(\./)?cel-fan-test[ \t]+-g$',
    r'^[ \t]*Fan[ \t]+1[ \t]+RPMs:[ \t]+\d{1,5},[ \t]+\d{1,5},[ \t]+\(\d{1,3}%\)$',
    r'^[ \t]*Fan[ \t]+2[ \t]+RPMs:[ \t]+\d{1,5},[ \t]+\d{1,5},[ \t]+\(\d{1,3}%\)$',
    r'^[ \t]*Fan[ \t]+3[ \t]+RPMs:[ \t]+\d{1,5},[ \t]+\d{1,5},[ \t]+\(\d{1,3}%\)$',
    r'^[ \t]*Fan[ \t]+4[ \t]+RPMs:[ \t]+\d{1,5},[ \t]+\d{1,5},[ \t]+\(\d{1,3}%\)$',
]

cel_fan_test_s_pattern = [
    r'#[ \t]*(\./)?cel-fan-test[ \t]+-s$',
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
    r'#[ \t]*(\./)?cel-fan-test[ \t]+-p[ \t]*\d{1,3}$',
    # The error is acceptance +/- 3% and the number does not have a decimal digit,
    # it is approximately 9 - 11 shows here.
    r'^Successfully[ \t]+set[ \t]+fan[ \t]+1[ \t]+speed[ \t]+to[ \t]+(9|1[01])%$',
    r'^Successfully[ \t]+set[ \t]+fan[ \t]+2[ \t]+speed[ \t]+to[ \t]+(9|1[01])%$',
    r'^Successfully[ \t]+set[ \t]+fan[ \t]+3[ \t]+speed[ \t]+to[ \t]+(9|1[01])%$',
    r'^Successfully[ \t]+set[ \t]+fan[ \t]+4[ \t]+speed[ \t]+to[ \t]+(9|1[01])%$',
]

cel_fan_test_g_p_10_pattern = [
    r'# [ \t]*(\./)?cel-fan-test[ \t]+-g$',
    # The error is acceptance +/- 3% and the number does not have a decimal digit,
    # it is approximately 9 - 11 shows here.
    r'^[ \t]*Fan[ \t]+1[ \t]+RPMs:[ \t]+\d{1,5},[ \t]+\d{1,5},[ \t]+\((9|10|11)%\)$',
    r'^[ \t]*Fan[ \t]+2[ \t]+RPMs:[ \t]+\d{1,5},[ \t]+\d{1,5},[ \t]+\((9|10|11)%\)$',
    r'^[ \t]*Fan[ \t]+3[ \t]+RPMs:[ \t]+\d{1,5},[ \t]+\d{1,5},[ \t]+\((9|10|11)%\)$',
    r'^[ \t]*Fan[ \t]+4[ \t]+RPMs:[ \t]+\d{1,5},[ \t]+\d{1,5},[ \t]+\((9|10|11)%\)$',
]

cal_fan_test_p_100_pattern = [
    r'#[ \t]*(\./)?cel-fan-test[ \t]+-p[ \t]*\d{1,3}$',
    # The error is acceptance +/- 3% and the number does not have a decimal digit,
    # it is approximately 97 - 103 shows here.
    r'^Successfully[ \t]+set[ \t]+fan[ \t]+1[ \t]+speed[ \t]+to[ \t]+(9[789]|10[0123])%$',
    r'^Successfully[ \t]+set[ \t]+fan[ \t]+2[ \t]+speed[ \t]+to[ \t]+(9[789]|10[0123])%$',
    r'^Successfully[ \t]+set[ \t]+fan[ \t]+3[ \t]+speed[ \t]+to[ \t]+(9[789]|10[0123])%$',
    r'^Successfully[ \t]+set[ \t]+fan[ \t]+4[ \t]+speed[ \t]+to[ \t]+(9[789]|10[0123])%$',
]

cel_fan_test_g_p_100_pattern = [
    r'#[ \t]*(\./)?cel-fan-test[ \t]+-g$',
    # The error is acceptance +/- 3% and the number does not have a decimal digit,
    # it is approximately 97 - 103 shows here.
    r'^[ \t]*Fan[ \t]+1[ \t]+RPMs:[ \t]+\d{1,5},[ \t]+\d{1,5},[ \t]+\((9[789]|10[0123])%\)$',
    r'^[ \t]*Fan[ \t]+2[ \t]+RPMs:[ \t]+\d{1,5},[ \t]+\d{1,5},[ \t]+\((9[789]|10[0123])%\)$',
    r'^[ \t]*Fan[ \t]+3[ \t]+RPMs:[ \t]+\d{1,5},[ \t]+\d{1,5},[ \t]+\((9[789]|10[0123])%\)$',
    r'^[ \t]*Fan[ \t]+4[ \t]+RPMs:[ \t]+\d{1,5},[ \t]+\d{1,5},[ \t]+\((9[789]|10[0123])%\)$',
]

cal_fan_test_p_50_pattern = [
    r'#[ \t]*(\./)?cel-fan-test[ \t]+-p[ \t]*\d{1,3}$',
    # The error is acceptance +/- 3% and the number does not have a decimal digit,
    # it is approximately 48 - 52 shows here.
    r'^Successfully[ \t]+set[ \t]+fan[ \t]+1[ \t]+speed[ \t]+to[ \t]+(4[89]|5[012])%$',
    r'^Successfully[ \t]+set[ \t]+fan[ \t]+2[ \t]+speed[ \t]+to[ \t]+(4[89]|5[012])%$',
    r'^Successfully[ \t]+set[ \t]+fan[ \t]+3[ \t]+speed[ \t]+to[ \t]+(4[89]|5[012])%$',
    r'^Successfully[ \t]+set[ \t]+fan[ \t]+4[ \t]+speed[ \t]+to[ \t]+(4[89]|5[012])%$',
]

cel_fan_test_g_p_50_pattern = [
    r'#[ \t]*(\./)?cel-fan-test[ \t]+-g$',
    # The error is acceptance +/- 3% and the number does not have a decimal digit,
    # it is approximately 48 - 52 shows here.
    r'^[ \t]*Fan[ \t]+1[ \t]+RPMs:[ \t]+\d{1,5},[ \t]+\d{1,5},[ \t]+\((4[89]|5[012])%\)$',
    r'^[ \t]*Fan[ \t]+2[ \t]+RPMs:[ \t]+\d{1,5},[ \t]+\d{1,5},[ \t]+\((4[89]|5[012])%\)$',
    r'^[ \t]*Fan[ \t]+3[ \t]+RPMs:[ \t]+\d{1,5},[ \t]+\d{1,5},[ \t]+\((4[89]|5[012])%\)$',
    r'^[ \t]*Fan[ \t]+4[ \t]+RPMs:[ \t]+\d{1,5},[ \t]+\d{1,5},[ \t]+\((4[89]|5[012])%\)$',
]

cel_fan_test_a_pattern = [
    r'#[ \t]*(\./)?cel-fan-test[ \t]+-a$',
    r'[ \t]*Fan[ \t]+1[ \t]+RPMs:[ \t]+\d{1,5},[ \t]+\d{1,5},[ \t]+\(\d{1,3}%\)$',
    r'^[ \t]*Fan[ \t]+2[ \t]+RPMs:[ \t]+\d{1,5},[ \t]+\d{1,5},[ \t]+\(\d{1,3}%\)$',
    r'^[ \t]*Fan[ \t]+3[ \t]+RPMs:[ \t]+\d{1,5},[ \t]+\d{1,5},[ \t]+\(\d{1,3}%\)$',
    r'^[ \t]*Fan[ \t]+4[ \t]+RPMs:[ \t]+\d{1,5},[ \t]+\d{1,5},[ \t]+\(\d{1,3}%\)$',
    r'^[ \t]*get_fan_speed[ \t]+.+PASS',
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
    r'^[ \t]*check_fan_status[ \t]+.+PASS',
]

cel_fan_test_c_sanyo_pattern = [
    r'#[ \t]*(\./)?cel-fan-test[ \t]+-c SANYO$',
    r'^[ \t]*Fan[ \t]+Speed[ \t]+Verify.+[ \t]+.+PASS',
]

cel_fan_test_e_pattern = [
    r'#[ \t]*(\./)?cel-fan-test[ \t]+-e$',
    r'^[ \t]*Check[ \t]+FAN1[ \t]+disable,[ \t]+others[ \t]+enable:[ \t]+OK$',
    r'^[ \t]*Check[ \t]+FAN2[ \t]+disable,[ \t]+others[ \t]+enable:[ \t]+OK$',
    r'^[ \t]*Check[ \t]+FAN3[ \t]+disable,[ \t]+others[ \t]+enable:[ \t]+OK$',
    r'^[ \t]*Check[ \t]+FAN4[ \t]+disable,[ \t]+others[ \t]+enable:[ \t]+OK$',
    r'^[ \t]*Check[ \t]+all[ \t]+FANs[ \t]+enable:[ \t]+OK$',
    r'.+PASS',
]

#### FB-DIAG-COM-TS-042-MEMORY-TEST ####
cel_memory_test = {
    "bin_tool": "cel-memory-test",
}

cel_memory_test_h_pattern = [
    r'#[ \t]*(\./)?cel-memory-test[ \t]+-h$',
    r'^Usage:[ \t]+\./cel-memory-test[ \t]+options[ \t]+\(-h\|-i\|-m\|-a\)$',
    r'^[ \t]*-h[ \t]+show[ \t]+this[ \t]+help$',
    r'^[ \t]*-i[ \t]+show[ \t]+memory[ \t]+info$',
    r'^[ \t]*-m[ \t]+memory[ \t]+read[ \t]+write[ \t]+test$',
    r'^[ \t]*-a[ \t]+test[ \t]+memory$',
]

cel_memory_test_i_pattern = [
    r'#[ \t]*(\./)?cel-memory-test[ \t]+-i$',
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
    r'^[ \t]*CmaTotal:[ \t]+\d+[ \t]+.+B$',
    r'^[ \t]*CmaFree:[ \t]+\d+[ \t]+.+B$',
    r'^[ \t]*total[ \t]+used[ \t]+free[ \t]+shared[ \t]+buffers[ \t]+cached$',
    r'^[ \t]*Mem:[ \t]+\d+[ \t]+\d+[ \t]+\d+[ \t]+\d+[ \t]+\d+[ \t]+\d+$',
]

cel_memory_test_m_pattern = [
    r'#[ \t]*(\./)?cel-memory-test[ \t]+-m$',
    # It is a lot of funny characters begins here, the regular expression has to be more flexible!
    r'Stuck.+Address.+ok',
    r'Random.+Value.+ok',
    r'Compare.+XOR.+ok',
    r'Compare.+SUB.+ok',
    r'Compare.+MUL.+ok',
    r'Compare.+DIV.+ok',
    r'Compare.+OR.+ok',
    r'Compare.+AND.+ok',
    r'Sequential.+Increment.+ok',
    r'Solid.+Bits.+ok',
    r'Block.+Sequential.+ok',
    r'Checkerboard.+ok',
    r'Bit.+Spread.+ok',
    r'Bit.+Flip.+ok',
    r'Walking.+Ones.+ok',
    r'Walking.+Zeroes.+ok',
    r'8-bit.+Writes.+ok',
    r'16-bit.+Writes.+ok',
    r'Done',
]

cel_memory_test_a_pattern = [
    r'#[ \t]*(\./)?cel-memory-test[ \t]+-a$',
    r'^[ \t]*get_memory_info.+PASS',
]

#### FB-DIAG-COM-TS-043-EMMC-TEST ###
cel_emmc_test = {
    "bin_tool": "cel-emmc-test",
}

cel_emmc_test_h_pattern = [
    r'#[ \t]*(\./)?cel-emmc-test[ \t]+-h$',
    r'^Usage:[ \t]+\./cel-emmc-test[ \t]+options[ \t]+\(-h\|-i\|-s\|-a\)$',
    r'^[ \t]*-h[ \t]+show[ \t]+this[ \t]+help$',
    r'^[ \t]*-i[ \t]+show[ \t]+emmc[ \t]+info$',
    r'^[ \t]*-s[ \t]+show[ \t]+emmc[ \t]+size$',
    r'^[ \t]*-a[ \t]+test[ \t]+emmc$',
]

cel_emmc_test_i_pattern = [
    r'#[ \t]*(\./)?cel-emmc-test[ \t]+-i$',
    # Have to define the exactly size!
    r'^[ \t]*Disk[ \t]+/dev/mmcblk0:[ \t]+\d+[ \t]+MB,[ \t]+\d+[ \t]+bytes$',
]

cel_emmc_test_s_pattern = [
    r'# [ \t]*(\./)?cel-emmc-test[ \t]+-s$',
    r'^[ \t]*\d+[ \t]+MB$',
]

cel_emmc_test_a_pattern = [
    r'# [ \t]*(\./)?cel-emmc-test[ \t]+-a$',
    r'^[ \t]*get_emmc_info[ \t\s]+.*PASS',
    r'^[ \t]*check_emmc_size[ \t\s]+.*PASS',
    r'^[ \t]*check_emmc_read_write[ \t\s]+.*PASS',
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
    r'# [ \t]*(\./)?cat[ \t]+[\w/]+VERSION\s+',
    r'^[ \t]*VERSION=\d\.\d.\d$',
]

check_the_issue_file = [
    r'# [ \t]*(\./)?cat[ \t]+[\w/]+issue\s+',
    r'^[ \t]*OpenBMC[ \t]+Release[ \t]+\w+-v3\.2$',
]

#### FB-DIAG-COM-TS-045-MDIO-TEST ####
cel_mdio_test = {
    "bin_tool": "cel-mdio-test",
}

cel_mdio_test_h_pattern = [
    r'#[ \t]*(\./)?cel-mdio-test[ \t]+-h$',
    r'^Usage:[ \t]+\./cel-mdio-test[ \t]+options[ \t]+\(-h\|-a\)$',
    r'^[ \t]*-h[ \t]+show[ \t]+this[ \t]+help$',
    r'^[ \t]*-a[ \t]+test$',
]

cel_mdio_test_a_pattern = [
    r'#[ \t]*(\./)?cel-mdio-test[ \t]+-a$',
    r'^[ \t]*enable_mdio[ \t\s]+.+PASS',
    r'^[ \t]*check_mdio_54616[ \t\s]+.+PASS',
    r'^[ \t]*check_mdio_5389[ \t\s]+.+PASS',
]

#### FB-DIAG-COM-TS-046-HOT-SWAP-CONTROLLER-ACCESS-TEST ####
cel_hotswap_test = {
    "bin_tool": "cel-hotswap-test",
}

cel_hotswap_test_h_pattern = [
    r'#[ \t]*(\./)?cel-hotswap-test[ \t]+-h$',
    r'^Usage:[ \t]+\./cel-hotswap-test[ \t]+options[ \t]+\(-h\|-a\)$',
    r'^[ \t]*-h[ \t]+show[ \t]+this[ \t]+help$',
    r'^[ \t]*-a[ \t]+test$',
]

cel_hotswap_test_a_pattern = [
    r'#[ \t]*(\./)?cel-hotswap-test[ \t]+-a$',
    r'^[ \t]*check_FCM_hotswap_access[ \t\s]+.+PASS',
    r'^[ \t]*check_SCM_hotswap_access[ \t\s]+.+PASS',
]

i2cset_scm_and_fcm_hotswap_pattern = [
    r'^[ \t]*0xb0$',
]

#### FB-DIAG-COM-TS-049-PSU-TEST ####
cel_psu_test = {
    "bin_tool": "cel-psu-test",
}

cel_psu_test_h_pattern = [
    r'#[ \t]*(\./)?cel-psu-test[ \t]+-h$',
    r'^Usage:[ \t]+\./cel-psu-test[ \t]+options[ \t]+\(-h\|-i\|-s\|-a\)$',
    r'^[ \t]*-h[ \t]+help[ \t]+information$',
    r'^[ \t]*-i[ \t]+show[ \t]+information$',
    r'^[ \t]*-s[ \t]+show[ \t]+status$',
    r'^[ \t]*-a[ \t]+test$',
]

cel_psu_test_s_pattern = [
    r'#[ \t]*(\./)?cel-psu-test[ \t]+-s$',
    r'^[ \t]*PSU1[ \t]+Present[ \t]+:[ \t]+OK$',
    r'^[ \t]*PSU1[ \t]+ACOK[ \t]+:[ \t]+OK$',
    r'^[ \t]*PSU1[ \t]+PWROK[ \t]+:[ \t]+OK$',
    r'^[ \t]*PSU2[ \t]+Present[ \t]+:[ \t]+OK$',
    r'^[ \t]*PSU2[ \t]+ACOK[ \t]+:[ \t]+OK$',
    r'^[ \t]*PSU2[ \t]+PWROK[ \t]+:[ \t]+OK$',
]

cel_psu_test_a_pattern = [
    r'#[ \t]*(\./)?cel-psu-test[ \t]+-a$',
    r'^[ \t]*check_psu_status[ \t\s]+.+PASS',
    r'^[ \t]*get_psu_info[ \t\s]+.+PASS',
]

#### FB-DIAG-COM-TS-050-SENSOR-TEST ###
cel_sensor_test = {
    "bin_tool": "cel-sensor-test",
}

cel_sensor_test_h_pattern = [
    r'#[ \t]*(\./)?cel-sensor-test[ \t]+-h$',
    r'^Usage:[ \t]+\./cel-sensor-test[ \t]+options[ \t]+\(-h\|-s\|-u\|-a\)$',
    r'^[ \t]*-h[ \t]+[S|s]how[ \t]+this[ \t]+help$',
    r'^[ \t]*-s[ \t]+show[ \t]+sensors[ \t]+data$',
    r'^[ \t]*-u[ \t]+check[ \t]+sensor-util$',
    r'^[ \t]*-a[ \t]+[A|a]uto[ \t]+test$',
]

cel_sensor_test_a_pattern = [
    r'#[ \t]*(\./)?cel-sensor-test[ \t]+-a$',
    r'^[ \t]*get_sensors_status[ \t\s]+.+PASS',
    r'^[ \t]*check_sensor_util_status[ \t\s]+.+PASS',
]

cel_sensor_test_u_pattern = [
    r'#[ \t]*(\./)?cel-sensor-test[ \t]+-u$',
    r'^[ \t]*check_sensor_util_status[ \t\s]+.+PASS',
]


####FB_SYS_COMM_TCG1-08_OpenBMC Utility Stability Test####
cel_openbmc_util_dev_id_pattern = [
    r'^[ \t]*Device[ \t]+ID:[ \t]+0x25',
    r'^[ \t]*Device[ \t]+Revision:[ \t]+0x80',
    r'^[ \t]*Firmware[ \t]+Revision:[ \t]+0x1:0x(12|15)',
    r'^[ \t]*IPMI[ \t]+Version:[ \t]+0x2',
    r'^[ \t]*Device[ \t]+Support:[ \t]+0xBF',
    r'^[ \t]*Manufacturer[ \t]+ID:[ \t]+0x0:0x1C:0x4C',
    r'^[ \t]*Product[ \t]+ID:[ \t]+0x46:0x20',
    r'^[ \t]*Aux.[ \t]+FW[ \t]+Rev:[ \t]+0x0:0x0:0x0:0x0',
]

cel_openbmc_util_gpio_status_pattern = [
    r'^[ \t]*XDP_CPU_SYSPWROK:[ \t]+1$',
    r'^[ \t]*PWRGD_PCH_PWROK:[ \t]+1$',
    r'^[ \t]*PVDDR_VRHOT_N:[ \t]+1$',
    r'^[ \t]*PVCCIN_VRHOT_N:[ \t]+1$',
    r'^[ \t]*FM_FAST_PROCHOT_N:[ \t]+1$',
    r'^[ \t]*PCHHOT_CPU_N:[ \t]+1$',
    r'^[ \t]*FM_CPLD_CPU_DIMM_EVENT_CO_N:[ \t]+1$',
    r'^[ \t]*FM_CPLD_BDXDE_THERMTRIP_N:[ \t]+1$',
    r'^[ \t]*THERMTRIP_PCH_N+:[ \t]+0$',
    r'^[ \t]*FM_CPLD_FIVR_FAULT:[ \t]+0$',
    r'^[ \t]*FM_BDXDE_CATERR_LVT3_N:[ \t]+1$',
    r'^[ \t]*FM_BDXDE_ERR_LVT3_N:[ \t]+7$',
    r'^[ \t]*SLP_S4_N:[ \t]+1$',
    r'^[ \t]*FM_NMI_EVENT_BMC_N:[ \t]+1$',
    r'^[ \t]*FM_SMI_BMC_N:[ \t]+1$',
    r'^[ \t]*RST_PLTRST_BMC_N:[ \t]+1$',
    r'^[ \t]*FP_RST_BTN_BUF_N:[ \t]+1$',
    r'^[ \t]*BMC_RST_BTN_OUT_N:[ \t]+1$',
    r'^[ \t]*FM_BDE_POST_CMPLT_N:[ \t]+0$',
    r'^[ \t]*FM_BDXDE_SLP3_N:[ \t]+1$',
    r'^[ \t]*FM_PWR_LED_N:[ \t]+1$',
    r'^[ \t]*PWRGD_PVCCIN:[ \t]+1$',
    r'^[ \t]*SVR_ID:[ \t]+15$',
    r'^[ \t]*BMC_READY_N:[ \t]+0$',
    r'^[ \t]*BMC_COM_SW_N:[ \t]+1$',
    r'^[ \t]*rsvd:[ \t]+0$',
    ]

cel_openbmc_util_gpio_config_pattern = [
    r'^[ \t]*gpio_config[ \t]+for[ \t]+pin\#0[ \t]+\(XDP_CPU_SYSPWROK\):$',
    r'^[ \t]*Direction:[ \t]+Input,[ \t]+Interrupt:[ \t]+Enabled,[ \t]+Trigger:[ \t]+Edge[ \t]+Trigger,[ \t]+Edge:[ \t]+Both[ \t]+Edges$',
    r'^[ \t]*gpio_config[ \t]for[ \t]pin\#1[ \t]\(PWRGD_PCH_PWROK\):$',
    r'^[ \t]*Direction:[ \t]+Input,[ \t]+Interrupt:[ \t]+Enabled,[ \t]+Trigger:[ \t]+Edge[ \t]+Trigger,[ \t]+Edge:[ \t]+Falling[ \t]+Edge$',
    r'^[ \t]*gpio_config[ \t]+for[ \t]+pin\#2[ \t]+\(PVDDR_VRHOT_N\):$',
    r'^[ \t]*Direction:[ \t]+Input,[ \t]+Interrupt:[ \t]+Disabled,[ \t]+Trigger:[ \t]+Edge[ \t]+Trigger,[ \t]+Edge:[ \t]+Falling[ \t]+Edge$',
    r'^[ \t]*gpio_config[ \t]+for[ \t]+pin\#3[ \t]+\(PVCCIN_VRHOT_N\):$',
    r'^[ \t]*Direction:[ \t]+Input,[ \t]+Interrupt:[ \t]+Disabled,[ \t]+Trigger:[ \t]+Edge[ \t]+Trigger,[ \t]+Edge:[ \t]+Falling[ \t]+Edge$',
    r'^[ \t]*gpio_config[ \t]+for[ \t]+pin\#4[ \t]+\(FM_FAST_PROCHOT_N\):$',
    r'^[ \t]*Direction:[ \t]+Input,[ \t]+Interrupt:[ \t]+Enabled,[ \t]+Trigger:[ \t]+Edge[ \t]+Trigger,[ \t]+Edge:[ \t]+Falling[ \t]+Edge$',
    r'^[ \t]*gpio_config[ \t]+for[ \t]+pin\#5[ \t]+\(PCHHOT_CPU_N\):$',
    r'^[ \t]*Direction:[ \t]+Input,[ \t]+Interrupt:[ \t]+Enabled,[ \t]+Trigger:[ \t]+Edge[ \t]+Trigger,[ \t]+Edge:[ \t]+Both[ \t]+Edges$',
    r'^[ \t]*gpio_config[ \t]for[ \t]pin\#6[ \t]\(FM_CPLD_CPU_DIMM_EVENT_CO_N\):$',
    r'^[ \t]*Direction:[ \t]+Input,[ \t]+Interrupt:[ \t]+Enabled,[ \t]+Trigger:[ \t]+Edge[ \t]+Trigger,[ \t]+Edge:[ \t]+Falling[ \t]+Edge$',
    r'^[ \t]*gpio_config[ \t]for[ \t]pin\#7[ \t]\(FM_CPLD_BDXDE_THERMTRIP_N\):$',
    r'^[ \t]*Direction:[ \t]+Input,[ \t]+Interrupt:[ \t]+Disabled,[ \t]+Trigger:[ \t]+Edge[ \t]+Trigger,[ \t]+Edge:[ \t]+Falling[ \t]+Edge$',
    r'^[ \t]*gpio_config[ \t]+for[ \t]+pin\#8[ \t]+\(THERMTRIP_PCH_N\):$',
    r'^[ \t]*Direction:[ \t]+Input,[ \t]+Interrupt:[ \t]+Enabled,[ \t]+Trigger:[ \t]+Edge[ \t]+Trigger,[ \t]+Edge:[ \t]+Rising[ \t]+Edge$',
    r'^[ \t]*gpio_config[ \t]+for[ \t]+pin\#9[ \t]+\(FM_CPLD_FIVR_FAULT\):$',
    r'^[ \t]*Direction:[ \t]+Input,[ \t]+Interrupt:[ \t]+Disabled,[ \t]+Trigger:[ \t]+Edge[ \t]+Trigger,[ \t]+Edge:[ \t]+Falling[ \t]+Edge$',
    r'^[ \t]*gpio_config[ \t]+for[ \t]+pin\#10[ \t]+\(FM_BDXDE_CATERR_LVT3_N\):$',
    r'^[ \t]*Direction:[ \t]+Input,[ \t]+Interrupt:[ \t]+Enabled,[ \t]+Trigger:[ \t]+Edge[ \t]+Trigger,[ \t]+Edge:[ \t]+Falling[ \t]+Edge$',
    r'^[ \t]*gpio_config[ \t]+for[ \t]+pin\#11[ \t]+\(FM_BDXDE_ERR2_LVT3_N\):$',
    r'^[ \t]*Direction:[ \t]+Input,[ \t]+Interrupt:[ \t]+Disabled,[ \t]+Trigger:[ \t]+Edge[ \t]+Trigger,[ \t]+Edge:[ \t]+Falling[ \t]+Edge$',
    r'^[ \t]*gpio_config[ \t]+for[ \t]+pin\#12[ \t]+\(FM_BDXDE_ERR1_LVT3_N\):$',
    r'^[ \t]*Direction:[ \t]+Input,[ \t]+Interrupt:[ \t]+Disabled,[ \t]+Trigger:[ \t]+Edge[ \t]+Trigger,[ \t]+Edge:[ \t]+Falling[ \t]+Edge$',
    r'^[ \t]*gpio_config[ \t]+for[ \t]+pin\#13[ \t]+\(FM_BDXDE_ERR0_LVT3_N\):$',
    r'^[ \t]*Direction:[ \t]+Input,[ \t]+Interrupt:[ \t]+Disabled,[ \t]+Trigger:[ \t]+Edge[ \t]+Trigger,[ \t]+Edge:[ \t]+Falling[ \t]+Edge$',
    r'^[ \t]*gpio_config[ \t]+for[ \t]+pin\#14[ \t]+\(SLP_S4_N\):$',
    r'^[ \t]*Direction:[ \t]+Input,[ \t]+Interrupt:[ \t]+Disabled,[ \t]+Trigger:[ \t]+Edge[ \t]+Trigger,[ \t]+Edge:[ \t]+Falling[ \t]+Edge$',
    r'^[ \t]*gpio_config[ \t]+for[ \t]+pin\#15[ \t]+\(FM_NMI_EVENT_BMC_N\):$',
    r'^[ \t]*Direction:[ \t]+Input,[ \t]+Interrupt:[ \t]+Disabled,[ \t]+Trigger:[ \t]+Edge[ \t]+Trigger,[ \t]+Edge:[ \t]+Falling[ \t]+Edge$',
    r'^[ \t]*gpio_config[ \t]+for[ \t]+pin\#16[ \t]+\(FM_SMI_BMC_N\):$',
    r'^[ \t]*Direction:[ \t]+Input,[ \t]+Interrupt:[ \t]+Disabled,[ \t]+Trigger:[ \t]+Edge[ \t]+Trigger,[ \t]+Edge:[ \t]+Falling[ \t]+Edge$',
    r'^[ \t]*gpio_config[ \t]+for[ \t]+pin\#17[ \t]+\(RST_PLTRST_BMC_N\):$',
    r'^[ \t]*Direction:[ \t]+Input,[ \t]+Interrupt:[ \t]+Enabled,[ \t]+Trigger:[ \t]+Edge[ \t]+Trigger,[ \t]+Edge:[ \t]+Rising[ \t]+Edge$',
    r'^[ \t]*gpio_config[ \t]+for[ \t]+pin\#18[ \t]+\(FP_RST_BTN_BUF_N\):$',
    r'^[ \t]*Direction:[ \t]+Input,[ \t]+Interrupt:[ \t]+Enabled,[ \t]+Trigger:[ \t]+Edge[ \t]+Trigger,[ \t]+Edge:[ \t]+Both[ \t]+Edges$',
    r'^[ \t]*gpio_config[ \t]+for[ \t]+pin\#19[ \t]+\(BMC_RST_BTN_OUT_N\):$',
    r'^[ \t]*Direction:[ \t]+Output,[ \t]+Interrupt:[ \t]+Disabled,[ \t]+Trigger:[ \t]+Edge[ \t]+Trigger,[ \t]+Edge:[ \t]+Falling[ \t]+Edge$',
    r'^[ \t]*gpio_config[ \t]+for[ \t]+pin\#20[ \t]+\(FM_BDE_POST_CMPLT_N\):$',
    r'^[ \t]*Direction:[ \t]+Input,[ \t]+Interrupt:[ \t]+Enabled,[ \t]+Trigger:[ \t]+Edge[ \t]+Trigger,[ \t]+Edge:[ \t]+Falling[ \t]+Edge$',
    r'^[ \t]*gpio_config[ \t]+for[ \t]+pin\#21[ \t]+\(FM_BDXDE_SLP3_N\):$',
    r'^[ \t]*Direction:[ \t]+Input,[ \t]+Interrupt:[ \t]+Enabled,[ \t]+Trigger:[ \t]+Edge[ \t]+Trigger,[ \t]+Edge:[ \t]+Falling[ \t]+Edge$',
    r'^[ \t]*gpio_config[ \t]+for[ \t]+pin\#22[ \t]+\(FM_PWR_LED_N\):$',
    r'^[ \t]*Direction:[ \t]+Output,[ \t]+Interrupt:[ \t]+Disabled,[ \t]+Trigger:[ \t]+Edge[ \t]+Trigger,[ \t]+Edge:[ \t]+Falling[ \t]+Edge$',
    r'^[ \t]*gpio_config[ \t]+for[ \t]+pin\#23[ \t]+\(PWRGD_PVCCIN\):$',
    r'^[ \t]*Direction:[ \t]+Input,[ \t]+Interrupt:[ \t]+Disabled,[ \t]+Trigger:[ \t]+Edge[ \t]+Trigger,[ \t]+Edge:[ \t]+Falling[ \t]+Edge$',
    r'^[ \t]*gpio_config[ \t]+for[ \t]+pin\#24[ \t]+\(SVR_ID0\):$',
    r'^[ \t]*Direction:[ \t]+Input,[ \t]+Interrupt:[ \t]+Disabled,[ \t]+Trigger:[ \t]+Edge[ \t]+Trigger,[ \t]+Edge:[ \t]+Falling[ \t]+Edge$',
    r'^[ \t]*gpio_config[ \t]+for[ \t]+pin\#25[ \t]+\(SVR_ID1\):$',
    r'^[ \t]*Direction:[ \t]+Input,[ \t]+Interrupt:[ \t]+Disabled,[ \t]+Trigger:[ \t]+Edge[ \t]+Trigger,[ \t]+Edge:[ \t]+Falling[ \t]+Edge$',
    r'^[ \t]*gpio_config[ \t]+for[ \t]+pin\#26[ \t]+\(SVR_ID2\):$',
    r'^[ \t]*Direction:[ \t]+Input,[ \t]+Interrupt:[ \t]+Disabled,[ \t]+Trigger:[ \t]+Edge[ \t]+Trigger,[ \t]+Edge:[ \t]+Falling[ \t]+Edge$',
    r'^[ \t]*gpio_config[ \t]+for[ \t]+pin\#27[ \t]+\(SVR_ID3\):$',
    r'^[ \t]*Direction:[ \t]+Input,[ \t]+Interrupt:[ \t]+Disabled,[ \t]+Trigger:[ \t]+Edge[ \t]+Trigger,[ \t]+Edge:[ \t]+Falling[ \t]+Edge$',
    r'^[ \t]*gpio_config[ \t]+for[ \t]+pin\#28[ \t]+\(BMC_READY_N\):$',
    r'^[ \t]*Direction:[ \t]+Output,[ \t]+Interrupt:[ \t]+Disabled,[ \t]+Trigger:[ \t]+Edge[ \t]+Trigger,[ \t]+Edge:[ \t]+Falling[ \t]+Edge$',
    r'^[ \t]*gpio_config[ \t]+for[ \t]+pin\#29[ \t]+\(BMC_COM_SW_N\):$',
    r'^[ \t]*Direction:[ \t]+Output,[ \t]+Interrupt:[ \t]+Disabled,[ \t]+Trigger:[ \t]+Edge[ \t]+Trigger,[ \t]+Edge:[ \t]+Falling[ \t]+Edge$',
]

cel_openbmc_util_config_pattern = [
    r'^[ \t]*SoL[ \t]+Enabled:[ \t]+Enabled$',
    r'^[ \t]*POST[ \t]+Enabled:[ \t]+Enabled$',
]

cel_openbmc_util_post_code_pattern = [
    r'^[ \t]*util_get_post_buf:[ \t]+returns[ \t]+([\d]+)[ \t]+bytes$',
    r'^[ \t]*([\w,\d]+)[ \t]+([\w,\d]+)[ \t]+([\w,\d]+)[ \t]+([\w,\d]+)[ \t]+([\w,\d]+)[ \t]+([\w,\d]+)[ \t]+([\w,\d]+)[ \t]+([\w,\d]+)[ \t]+([\w,\d]+)[ \t]+([\w,\d]+)[ \t]+([\w,\d]+)[ \t]+([\w,\d]+)[ \t]+([\w,\d]+)[ \t]+([\w,\d]+)[ \t]+([\w,\d]+)[ \t]+([\w,\d]+)',
    r'^[ \t]*([\w,\d]+)[ \t]+([\w,\d]+)[ \t]+([\w,\d]+)[ \t]+([\w,\d]+)[ \t]+([\w,\d]+)[ \t]+([\w,\d]+)[ \t]+([\w,\d]+)[ \t]+([\w,\d]+)[ \t]+([\w,\d]+)[ \t]+([\w,\d]+)[ \t]+([\w,\d]+)[ \t]+([\w,\d]+)[ \t]+([\w,\d]+)[ \t]+([\w,\d]+)[ \t]+([\w,\d]+)[ \t]+([\w,\d]+)',
    r'^[ \t]*([\w,\d]+)[ \t]+([\w,\d]+)[ \t]+([\w,\d]+)[ \t]+([\w,\d]+)[ \t]+([\w,\d]+)[ \t]+([\w,\d]+)[ \t]+([\w,\d]+)[ \t]+([\w,\d]+)[ \t]+([\w,\d]+)[ \t]+([\w,\d]+)[ \t]+([\w,\d]+)[ \t]+([\w,\d]+)[ \t]+([\w,\d]+)[ \t]+([\w,\d]+)[ \t]+([\w,\d]+)[ \t]+([\w,\d]+)',
    r'^[ \t]*([\w,\d]+)[ \t]+([\w,\d]+)[ \t]+([\w,\d]+)[ \t]+([\w,\d]+)[ \t]+([\w,\d]+)[ \t]+([\w,\d]+)[ \t]+([\w,\d]+)[ \t]+([\w,\d]+)[ \t]+([\w,\d]+)[ \t]+([\w,\d]+)[ \t]+([\w,\d]+)[ \t]+([\w,\d]+)[ \t]+([\w,\d]+)[ \t]+([\w,\d]+)[ \t]+([\w,\d]+)[ \t]+([\w,\d]+)',
    r'^[ \t]*([\w,\d]+)[ \t]+([\w,\d]+)[ \t]+([\w,\d]+)[ \t]+([\w,\d]+)[ \t]+([\w,\d]+)[ \t]+([\w,\d]+)[ \t]+([\w,\d]+)[ \t]+([\w,\d]+)[ \t]+([\w,\d]+)[ \t]+([\w,\d]+)[ \t]+([\w,\d]+)[ \t]+([\w,\d]+)[ \t]+([\w,\d]+)[ \t]+([\w,\d]+)[ \t]+([\w,\d]+)[ \t]+([\w,\d]+)',
    r'^[ \t]*([\w,\d]+)[ \t]+([\w,\d]+)[ \t]+([\w,\d]+)[ \t]+([\w,\d]+)[ \t]+([\w,\d]+)[ \t]+([\w,\d]+)[ \t]+([\w,\d]+)[ \t]+([\w,\d]+)[ \t]+([\w,\d]+)[ \t]+([\w,\d]+)[ \t]+([\w,\d]+)[ \t]+([\w,\d]+)[ \t]+([\w,\d]+)[ \t]+([\w,\d]+)[ \t]+([\w,\d]+)[ \t]+([\w,\d]+)',
]

cel_openbmc_util_sdr_pattern = [
    r'^[ \t]*type:[ \t]+1,[ \t]+sensor_num:[ \t]+1,[ \t]+sensor_type:[ \t]+1,[ \t]+evt_read_type:[ \t]+1,[ \t]+m_val:[ \t]+1,[ \t]+m_tolerance:[ \t]+0,[ \t]+b_val:[ \t]+0,[ \t]+b_accuracy:[ \t]+0,[ \t]+accuracy_dir:[ \t]+0,[ \t]+rb_exp:[ \t]+0,',
    r'^[ \t]*type:[ \t]+1,[ \t]+sensor_num:[ \t]+7,[ \t]+sensor_type:[ \t]+1,[ \t]+evt_read_type:[ \t]+1,[ \t]+m_val:[ \t]+1,[ \t]+m_tolerance:[ \t]+0,[ \t]+b_val:[ \t]+0,[ \t]+b_accuracy:[ \t]+0,[ \t]+accuracy_dir:[ \t]+0,[ \t]+rb_exp:[ \t]+0,',
    r'^[ \t]*type:[ \t]+1,[ \t]+sensor_num:[ \t]+8,[ \t]+sensor_type:[ \t]+1,[ \t]+evt_read_type:[ \t]+1,[ \t]+m_val:[ \t]+1,[ \t]+m_tolerance:[ \t]+0,[ \t]+b_val:[ \t]+0,[ \t]+b_accuracy:[ \t]+0,[ \t]+accuracy_dir:[ \t]+0,[ \t]+rb_exp:[ \t]+0,',
    r'^[ \t]*type:[ \t]+1,[ \t]+sensor_num:[ \t]+5,[ \t]+sensor_type:[ \t]+1,[ \t]+evt_read_type:[ \t]+1,[ \t]+m_val:[ \t]+1,[ \t]+m_tolerance:[ \t]+0,[ \t]+b_val:[ \t]+0,[ \t]+b_accuracy:[ \t]+0,[ \t]+accuracy_dir:[ \t]+0,[ \t]+rb_exp:[ \t]+0,',
    r'^[ \t]*type:[ \t]+1,[ \t]+sensor_num:[ \t]+9,[ \t]+sensor_type:[ \t]+1,[ \t]+evt_read_type:[ \t]+1,[ \t]+m_val:[ \t]+1,[ \t]+m_tolerance:[ \t]+0,[ \t]+b_val:[ \t]+0,[ \t]+b_accuracy:[ \t]+0,[ \t]+accuracy_dir:[ \t]+0,[ \t]+rb_exp:[ \t]+0,',
    r'^[ \t]*type:[ \t]+1,[ \t]+sensor_num:[ \t]+48,[ \t]+sensor_type:[ \t]+1,[ \t]+evt_read_type:[ \t]+1,[ \t]+m_val:[ \t]+1,[ \t]+m_tolerance:[ \t]+0,[ \t]+b_val:[ \t]+0,[ \t]+b_accuracy:[ \t]+0,[ \t]+accuracy_dir:[ \t]+0,[ \t]+rb_exp:[ \t]+0,',
    r'^[ \t]*type:[ \t]+1,[ \t]+sensor_num:[ \t]+180,[ \t]+sensor_type:[ \t]+1,[ \t]+evt_read_type:[ \t]+1,[ \t]+m_val:[ \t]+1,[ \t]+m_tolerance:[ \t]+0,[ \t]+b_val:[ \t]+0,[ \t]+b_accuracy:[ \t]+0,[ \t]+accuracy_dir:[ \t]+0,[ \t]+rb_exp:[ \t]+0,',
    r'^[ \t]*type:[ \t]+1,[ \t]+sensor_num:[ \t]+182,[ \t]+sensor_type:[ \t]+1,[ \t]+evt_read_type:[ \t]+1,[ \t]+m_val:[ \t]+1,[ \t]+m_tolerance:[ \t]+0,[ \t]+b_val:[ \t]+0,[ \t]+b_accuracy:[ \t]+0,[ \t]+accuracy_dir:[ \t]+0,[ \t]+rb_exp:[ \t]+0,',
    r'^[ \t]*type:[ \t]+1,[ \t]+sensor_num:[ \t]+129,[ \t]+sensor_type:[ \t]+1,[ \t]+evt_read_type:[ \t]+1,[ \t]+m_val:[ \t]+1,[ \t]+m_tolerance:[ \t]+0,[ \t]+b_val:[ \t]+0,[ \t]+b_accuracy:[ \t]+0,[ \t]+accuracy_dir:[ \t]+0,[ \t]+rb_exp:[ \t]+0,',
    r'^[ \t]*type:[ \t]+1,[ \t]+sensor_num:[ \t]+130,[ \t]+sensor_type:[ \t]+1,[ \t]+evt_read_type:[ \t]+1,[ \t]+m_val:[ \t]+1,[ \t]+m_tolerance:[ \t]+0,[ \t]+b_val:[ \t]+0,[ \t]+b_accuracy:[ \t]+0,[ \t]+accuracy_dir:[ \t]+0,[ \t]+rb_exp:[ \t]+0,',
    r'^[ \t]*type:[ \t]+1,[ \t]+sensor_num:[ \t]+128,[ \t]+sensor_type:[ \t]+1,[ \t]+evt_read_type:[ \t]+1,[ \t]+m_val:[ \t]+1,[ \t]+m_tolerance:[ \t]+0,[ \t]+b_val:[ \t]+0,[ \t]+b_accuracy:[ \t]+0,[ \t]+accuracy_dir:[ \t]+0,[ \t]+rb_exp:[ \t]+0,',
    r'^[ \t]*type:[ \t]+1,[ \t]+sensor_num:[ \t]+132,[ \t]+sensor_type:[ \t]+3,[ \t]+evt_read_type:[ \t]+1,[ \t]+m_val:[ \t]+125,[ \t]+m_tolerance:[ \t]+0,[ \t]+b_val:[ \t]+0,[ \t]+b_accuracy:[ \t]+0,[ \t]+accuracy_dir:[ \t]+0,[ \t]+rb_exp:[ \t]+208,',
    r'^[ \t]*type:[ \t]+1,[ \t]+sensor_num:[ \t]+133,[ \t]+sensor_type:[ \t]+3,[ \t]+evt_read_type:[ \t]+1,[ \t]+m_val:[ \t]+125,[ \t]+m_tolerance:[ \t]+0,[ \t]+b_val:[ \t]+0,[ \t]+b_accuracy:[ \t]+0,[ \t]+accuracy_dir:[ \t]+0,[ \t]+rb_exp:[ \t]+208,',
    r'^[ \t]*type:[ \t]+1,[ \t]+sensor_num:[ \t]+131,[ \t]+sensor_type:[ \t]+3,[ \t]+evt_read_type:[ \t]+1,[ \t]+m_val:[ \t]+5,[ \t]+m_tolerance:[ \t]+0,[ \t]+b_val:[ \t]+0,[ \t]+b_accuracy:[ \t]+0,[ \t]+accuracy_dir:[ \t]+0,[ \t]+rb_exp:[ \t]+240,',
    r'^[ \t]*type:[ \t]+1,[ \t]+sensor_num:[ \t]+137,[ \t]+sensor_type:[ \t]+2,[ \t]+evt_read_type:[ \t]+1,[ \t]+m_val:[ \t]+1,[ \t]+m_tolerance:[ \t]+0,[ \t]+b_val:[ \t]+0,[ \t]+b_accuracy:[ \t]+0,[ \t]+accuracy_dir:[ \t]+0,[ \t]+rb_exp:[ \t]+224,',
    r'^[ \t]*type:[ \t]+1,[ \t]+sensor_num:[ \t]+138,[ \t]+sensor_type:[ \t]+2,[ \t]+evt_read_type:[ \t]+1,[ \t]+m_val:[ \t]+1,[ \t]+m_tolerance:[ \t]+0,[ \t]+b_val:[ \t]+0,[ \t]+b_accuracy:[ \t]+0,[ \t]+accuracy_dir:[ \t]+0,[ \t]+rb_exp:[ \t]+224,',
    r'^[ \t]*type:[ \t]+1,[ \t]+sensor_num:[ \t]+136,[ \t]+sensor_type:[ \t]+2,[ \t]+evt_read_type:[ \t]+1,[ \t]+m_val:[ \t]+1,[ \t]+m_tolerance:[ \t]+0,[ \t]+b_val:[ \t]+0,[ \t]+b_accuracy:[ \t]+0,[ \t]+accuracy_dir:[ \t]+0,[ \t]+rb_exp:[ \t]+224,',
    r'^[ \t]*type:[ \t]+1,[ \t]+sensor_num:[ \t]+140,[ \t]+sensor_type:[ \t]+11,[ \t]+evt_read_type:[ \t]+1,[ \t]+m_val:[ \t]+125,[ \t]+m_tolerance:[ \t]+0,[ \t]+b_val:[ \t]+0,[ \t]+b_accuracy:[ \t]+0,[ \t]+accuracy_dir:[ \t]+0,[ \t]+rb_exp:[ \t]+208,',
    r'^[ \t]*type:[ \t]+1,[ \t]+sensor_num:[ \t]+141,[ \t]+sensor_type:[ \t]+11,[ \t]+evt_read_type:[ \t]+1,[ \t]+m_val:[ \t]+25,[ \t]+m_tolerance:[ \t]+0,[ \t]+b_val:[ \t]+0,[ \t]+b_accuracy:[ \t]+0,[ \t]+accuracy_dir:[ \t]+0,[ \t]+rb_exp:[ \t]+224,',
    r'^[ \t]*type:[ \t]+1,[ \t]+sensor_num:[ \t]+139,[ \t]+sensor_type:[ \t]+11,[ \t]+evt_read_type:[ \t]+1,[ \t]+m_val:[ \t]+1,[ \t]+m_tolerance:[ \t]+0,[ \t]+b_val:[ \t]+0,[ \t]+b_accuracy:[ \t]+0,[ \t]+accuracy_dir:[ \t]+0,[ \t]+rb_exp:[ \t]+0,',
    r'^[ \t]*type:[ \t]+1,[ \t]+sensor_num:[ \t]+208,[ \t]+sensor_type:[ \t]+2,[ \t]+evt_read_type:[ \t]+1,[ \t]+m_val:[ \t]+209,[ \t]+m_tolerance:[ \t]+0,[ \t]+b_val:[ \t]+0,[ \t]+b_accuracy:[ \t]+0,[ \t]+accuracy_dir:[ \t]+0,[ \t]+rb_exp: 192,',
    r'^[ \t]*type:[ \t]+1,[ \t]+sensor_num:[ \t]+213,[ \t]+sensor_type:[ \t]+2,[ \t]+evt_read_type:[ \t]+1,[ \t]+m_val:[ \t]+209,[ \t]+m_tolerance:[ \t]+0,[ \t]+b_val:[ \t]+0,[ \t]+b_accuracy:[ \t]+0,[ \t]+accuracy_dir:[ \t]+0,[ \t]+rb_exp:[ \t]+192,',
    r'^[ \t]*type:[ \t]+1,[ \t]+sensor_num:[ \t]+215,[ \t]+sensor_type:[ \t]+2,[ \t]+evt_read_type:[ \t]+1,[ \t]+m_val:[ \t]+39,[ \t]+m_tolerance:[ \t]+0,[ \t]+b_val:[ \t]+0,[ \t]+b_accuracy:[ \t]+0,[ \t]+accuracy_dir:[ \t]+0,[ \t]+rb_exp:[ \t]+208,',
    r'^[ \t]*type:[ \t]+1,[ \t]+sensor_num:[ \t]+142,[ \t]+sensor_type:[ \t]+2,[ \t]+evt_read_type:[ \t]+1,[ \t]+m_val:[ \t]+130,[ \t]+m_tolerance:[ \t]+0,[ \t]+b_val:[ \t]+0,[ \t]+b_accuracy:[ \t]+0,[ \t]+accuracy_dir:[ \t]+0,[ \t]+rb_exp:[ \t]+192,',
    r'^[ \t]*type:[ \t]+1,[ \t]+sensor_num:[ \t]+211,[ \t]+sensor_type:[ \t]+2,[ \t]+evt_read_type:[ \t]+1,[ \t]+m_val:[ \t]+130,[ \t]+m_tolerance:[ \t]+0,[ \t]+b_val:[ \t]+0,[ \t]+b_accuracy:[ \t]+0,[ \t]+accuracy_dir:[ \t]+0,[ \t]+rb_exp:[ \t]+192,',
    r'^[ \t]*type:[ \t]+1,[ \t]+sensor_num:[ \t]+210,[ \t]+sensor_type:[ \t]+2,[ \t]+evt_read_type:[ \t]+1,[ \t]+m_val:[ \t]+78,[ \t]+m_tolerance:[ \t]+0,[ \t]+b_val:[ \t]+0,[ \t]+b_accuracy: 0,[ \t]+accuracy_dir:[ \t]+0,[ \t]+rb_exp:[ \t]+208,',
    r'^[ \t]*type:[ \t]+1,[ \t]+sensor_num:[ \t]+214,[ \t]+sensor_type:[ \t]+2,[ \t]+evt_read_type:[ \t]+1,[ \t]+m_val:[ \t]+32,[ \t]+m_tolerance:[ \t]+0,[ \t]+b_val:[ \t]+0,[ \t]+b_accuracy: 0,[ \t]+accuracy_dir:[ \t]+0,[ \t]+rb_exp:[ \t]+208,',
    r'^[ \t]*type:[ \t]+1,[ \t]+sensor_num:[ \t]+216,[ \t]+sensor_type:[ \t]+2,[ \t]+evt_read_type:[ \t]+1,[ \t]+m_val:[ \t]+131,[ \t]+m_tolerance:[ \t]+0,[ \t]+b_val:[ \t]+0,[ \t]+b_accuracy:[ \t]+0,[ \t]+accuracy_dir:[ \t]+0,[ \t]+rb_exp:[ \t]+192,',
    r'^[ \t]*type:[ \t]+1,[ \t]+sensor_num:[ \t]+217,[ \t]+sensor_type:[ \t]+2,[ \t]+evt_read_type:[ \t]+1,[ \t]+m_val:[ \t]+129,[ \t]+m_tolerance:[ \t]+0,[ \t]+b_val:[ \t]+0,[ \t]+b_accuracy:[ \t]+0,[ \t]+accuracy_dir:[ \t]+0,[ \t]+rb_exp:[ \t]+192,',
    r'^[ \t]*type:[ \t]+1,[ \t]+sensor_num:[ \t]+44,[ \t]+sensor_type:[ \t]+11,[ \t]+evt_read_type:[ \t]+1,[ \t]+m_val:[ \t]+1,[ \t]+m_tolerance:[ \t]+0,[ \t]+b_val:[ \t]+0,[ \t]+b_accuracy:[ \t]+0,[ \t]+accuracy_dir:[ \t]+0,[ \t]+rb_exp:[ \t]+0,',
    r'^[ \t]*type:[ \t]+1,[ \t]+sensor_num:[ \t]+41,[ \t]+sensor_type:[ \t]+11,[ \t]+evt_read_type:[ \t]+1,[ \t]+m_val:[ \t]+1,[ \t]+m_tolerance:[ \t]+0,[ \t]+b_val:[ \t]+0,[ \t]+b_accuracy:[ \t]+0,[ \t]+accuracy_dir:[ \t]+0,[ \t]+rb_exp:[ \t]+0,',
    r'^[ \t]*type:[ \t]+1,[ \t]+sensor_num:[ \t]+42,[ \t]+sensor_type:[ \t]+2,[ \t]+evt_read_type:[ \t]+1,[ \t]+m_val:[ \t]+79,[ \t]+m_tolerance:[ \t]+0,[ \t]+b_val:[ \t]+0,[ \t]+b_accuracy:[ \t]+0,[ \t]+accuracy_dir:[ \t]+0,[ \t]+rb_exp:[ \t]+208,',
    r'^[ \t]*type:[ \t]+2,[ \t]+sensor_num:[ \t]+16,[ \t]+sensor_type:[ \t]+201,[ \t]+evt_read_type:[ \t]+111,[ \t]+m_val:[ \t]+0,[ \t]+m_tolerance:[ \t]+0,[ \t]+b_val:[ \t]+0,[ \t]+b_accuracy:[ \t]+0,[ \t]+accuracy_dir:[ \t]+0,[ \t]+rb_exp:[ \t]+0,',
    r'^[ \t]*type:[ \t]+2,[ \t]+sensor_num:[ \t]+101,[ \t]+sensor_type:[ \t]+7,[ \t]+evt_read_type:[ \t]+111,[ \t]+m_val:[ \t]+0,[ \t]+m_tolerance:[ \t]+0,[ \t]+b_val:[ \t]+0,[ \t]+b_accuracy:[ \t]+0,[ \t]+accuracy_dir:[ \t]+0,[ \t]+rb_exp:[ \t]+0,',
    r'^[ \t]*type:[ \t]+2,[ \t]+sensor_num:[ \t]+179,[ \t]+sensor_type:[ \t]+199,[ \t]+evt_read_type:[ \t]+111,[ \t]+m_val:[ \t]+0,[ \t]+m_tolerance:[ \t]+0,[ \t]+b_val:[ \t]+0,[ \t]+b_accuracy:[ \t]+0,[ \t]+accuracy_dir:[ \t]+0,[ \t]+rb_exp:[ \t]+0,',
    r'^[ \t]*type:[ \t]+2,[ \t]+sensor_num:[ \t]+178,[ \t]+sensor_type:[ \t]+198,[ \t]+evt_read_type:[ \t]+111,[ \t]+m_val:[ \t]+0,[ \t]+m_tolerance:[ \t]+0,[ \t]+b_val:[ \t]+0,[ \t]+b_accuracy:[ \t]+0,[ \t]+accuracy_dir:[ \t]+0,[ \t]+rb_exp:[ \t]+0,',
    r'^[ \t]*type:[ \t]+2,[ \t]+sensor_num:[ \t]+126,[ \t]+sensor_type:[ \t]+202,[ \t]+evt_read_type:[ \t]+111,[ \t]+m_val:[ \t]+0,[ \t]+m_tolerance:[ \t]+0,[ \t]+b_val:[ \t]+0,[ \t]+b_accuracy:[ \t]+0,[ \t]+accuracy_dir:[ \t]+0,[ \t]+rb_exp:[ \t]+0,',
    r'^[ \t]*type:[ \t]+3,[ \t]+sensor_num:[ \t]+235,[ \t]+sensor_type:[ \t]+1,[ \t]+evt_read_type:[ \t]+0,[ \t]+m_val:[ \t]+0,[ \t]+m_tolerance:[ \t]+0,[ \t]+b_val:[ \t]+0,[ \t]+b_accuracy:[ \t]+0,[ \t]+accuracy_dir:[ \t]+0,[ \t]+rb_exp:[ \t]+0,',
    r'^[ \t]*type:[ \t]+3,[ \t]+sensor_num:[ \t]+59,[ \t]+sensor_type:[ \t]+1,[ \t]+evt_read_type:[ \t]+0,[ \t]+m_val:[ \t]+101,[ \t]+m_tolerance:[ \t]+115,[ \t]+b_val:[ \t]+104,[ \t]+b_accuracy:[ \t]+32,[ \t]+accuracy_dir:[ \t]+69,[ \t]+rb_exp:[ \t]+118,',
    r'^[ \t]*type:[ \t]+3,[ \t]+sensor_num:[ \t]+43,[ \t]+sensor_type:[ \t]+1,[ \t]+evt_read_type:[ \t]+0,[ \t]+m_val:[ \t]+114,[ \t]+m_tolerance:[ \t]+115,[ \t]+b_val:[ \t]+104,[ \t]+b_accuracy:[ \t]+32,[ \t]+accuracy_dir:[ \t]+69,[ \t]+rb_exp:[ \t]+118,',
    r'^[ \t]*type:[ \t]+3,[ \t]+sensor_num:[ \t]+86,[ \t]+sensor_type:[ \t]+1,[ \t]+evt_read_type:[ \t]+0,[ \t]+m_val:[ \t]+114,[ \t]+m_tolerance:[ \t]+114,[ \t]+b_val:[ \t]+111,[ \t]+b_accuracy:[ \t]+114,[ \t]+accuracy_dir:[ \t]+69,[ \t]+rb_exp: 118,',
    r'^[ \t]*type:[ \t]+3,[ \t]+sensor_num:[ \t]+81,[ \t]+sensor_type:[ \t]+1,[ \t]+evt_read_type:[ \t]+0,[ \t]+m_val:[ \t]+32,[ \t]+m_tolerance:[ \t]+69,[ \t]+b_val:[ \t]+120,[ \t]+b_accuracy:[ \t]+116,[ \t]+accuracy_dir:[ \t]+69,[ \t]+rb_exp:[ \t]+118,',
    r'^[ \t]*type:[ \t]+3,[ \t]+sensor_num:[ \t]+64,[ \t]+sensor_type:[ \t]+1,[ \t]+evt_read_type:[ \t]+0,[ \t]+m_val:[ \t]+32,[ \t]+m_tolerance:[ \t]+67,[ \t]+b_val:[ \t]+104,[ \t]+b_accuracy:[ \t]+107,[ \t]+accuracy_dir:[ \t]+32,[ \t]+rb_exp:[ \t]+69,',
    r'^[ \t]*type:[ \t]+3,[ \t]+sensor_num:[ \t]+65,[ \t]+sensor_type:[ \t]+1,[ \t]+evt_read_type:[ \t]+0,[ \t]+m_val:[ \t]+114,[ \t]+m_tolerance:[ \t]+67,[ \t]+b_val:[ \t]+104,[ \t]+b_accuracy:[ \t]+107,[ \t]+accuracy_dir:[ \t]+32,[ \t]+rb_exp:[ \t]+69,',
    r'^[ \t]*type:[ \t]+3,[ \t]+sensor_num:[ \t]+67,[ \t]+sensor_type:[ \t]+1,[ \t]+evt_read_type:[ \t]+0,[ \t]+m_val:[ \t]+73,[ \t]+m_tolerance:[ \t]+79,[ \t]+b_val:[ \t]+32,[ \t]+b_accuracy:[ \t]+69,[ \t]+accuracy_dir:[ \t]+114,[ \t]+rb_exp:[ \t]+114,',
    r'^[ \t]*type:[ \t]+3,[ \t]+sensor_num:[ \t]+99,[ \t]+sensor_type:[ \t]+1,[ \t]+evt_read_type:[ \t]+0,[ \t]+m_val:[ \t]+69,[ \t]+m_tolerance:[ \t]+67,[ \t]+b_val:[ \t]+67,[ \t]+b_accuracy:[ \t]+32,[ \t]+accuracy_dir:[ \t]+69,[ \t]+rb_exp:[ \t]+114,',
    r'^[ \t]*type:[ \t]+3,[ \t]+sensor_num:[ \t]+23,[ \t]+sensor_type:[ \t]+1,[ \t]+evt_read_type:[ \t]+0,[ \t]+m_val:[ \t]+72,[ \t]+m_tolerance:[ \t]+101,[ \t]+b_val:[ \t]+97,[ \t]+b_accuracy:[ \t]+108,[ \t]+accuracy_dir:[ \t]+116,[ \t]+rb_exp:[ \t]+104,',
    r'^[ \t]*This[ \t]+record[ \t]+is[ \t]+LAST[ \t]+record'
]

cel_openbmc_util_sensor_pattern = [
    r'^[ \t]*sensor#1:[ \t]+value:[ \t]+(.+),[ \t]+flags:[ \t]+(.+),[ \t]+status:[ \t]+(.+),[ \t]+ext_status:[ \t]+(.+)$',
    r'^[ \t]*sensor#5:[ \t]+value:[ \t]+(.+),[ \t]+flags:[ \t]+(.+),[ \t]+status:[ \t]+(.+),[ \t]+ext_status:[ \t]+(.+)$',
    r'^[ \t]*sensor#7:[ \t]+value:[ \t]+(.+),[ \t]+flags:[ \t]+(.+),[ \t]+status:[ \t]+(.+),[ \t]+ext_status:[ \t]+(.+)$',
    r'^[ \t]*sensor#8:[ \t]+value:[ \t]+(.+),[ \t]+flags:[ \t]+(.+),[ \t]+status:[ \t]+(.+),[ \t]+ext_status:[ \t]+(.+)$',
    r'^[ \t]*sensor#9:[ \t]+value:[ \t]+(.+),[ \t]+flags:[ \t]+(.+),[ \t]+status:[ \t]+(.+),[ \t]+ext_status:[ \t]+(.+)$',
    r'^[ \t]*sensor#16:[ \t]+value:[ \t]+(.+),[ \t]+flags:[ \t]+(.+),[ \t]+status:[ \t]+(.+),[ \t]+ext_status:[ \t]+(.+)$',
    r'^[ \t]*sensor#23:[ \t]+value:[ \t]+(.+),[ \t]+flags:[ \t]+(.+),[ \t]+status:[ \t]+(.+),[ \t]+ext_status:[ \t]+(.+)$',
    r'^[ \t]*sensor#41:[ \t]+value:[ \t]+(.+),[ \t]+flags:[ \t]+(.+),[ \t]+status:[ \t]+(.+),[ \t]+ext_status:[ \t]+(.+)$',
    r'^[ \t]*sensor#42:[ \t]+value:[ \t]+(.+),[ \t]+flags:[ \t]+(.+),[ \t]+status:[ \t]+(.+),[ \t]+ext_status:[ \t]+(.+)$',
    r'^[ \t]*sensor#43:[ \t]+value:[ \t]+(.+),[ \t]+flags:[ \t]+(.+),[ \t]+status:[ \t]+(.+),[ \t]+ext_status:[ \t]+(.+)$',
    r'^[ \t]*sensor#44:[ \t]+value:[ \t]+(.+),[ \t]+flags:[ \t]+(.+),[ \t]+status:[ \t]+(.+),[ \t]+ext_status:[ \t]+(.+)$',
    r'^[ \t]*sensor#48:[ \t]+value:[ \t]+(.+),[ \t]+flags:[ \t]+(.+),[ \t]+status:[ \t]+(.+),[ \t]+ext_status:[ \t]+(.+)$',
    r'^[ \t]*sensor#59:[ \t]+value:[ \t]+(.+),[ \t]+flags:[ \t]+(.+),[ \t]+status:[ \t]+(.+),[ \t]+ext_status:[ \t]+(.+)$',
    r'^[ \t]*sensor#64:[ \t]+value:[ \t]+(.+),[ \t]+flags:[ \t]+(.+),[ \t]+status:[ \t]+(.+),[ \t]+ext_status:[ \t]+(.+)$',
    r'^[ \t]*sensor#65:[ \t]+value:[ \t]+(.+),[ \t]+flags:[ \t]+(.+),[ \t]+status:[ \t]+(.+),[ \t]+ext_status:[ \t]+(.+)$',
    r'^[ \t]*sensor#67:[ \t]+value:[ \t]+(.+),[ \t]+flags:[ \t]+(.+),[ \t]+status:[ \t]+(.+),[ \t]+ext_status:[ \t]+(.+)$',
    r'^[ \t]*sensor#81:[ \t]+value:[ \t]+(.+),[ \t]+flags:[ \t]+(.+),[ \t]+status:[ \t]+(.+),[ \t]+ext_status:[ \t]+(.+)$',
    r'^[ \t]*sensor#86:[ \t]+value:[ \t]+(.+),[ \t]+flags:[ \t]+(.+),[ \t]+status:[ \t]+(.+),[ \t]+ext_status:[ \t]+(.+)$',
    r'^[ \t]*sensor#99:[ \t]+value:[ \t]+(.+),[ \t]+flags:[ \t]+(.+),[ \t]+status:[ \t]+(.+),[ \t]+ext_status:[ \t]+(.+)$',
    r'^[ \t]*sensor#101:[ \t]+value:[ \t]+(.+),[ \t]+flags:[ \t]+(.+),[ \t]+status:[ \t]+(.+),[ \t]+ext_status:[ \t]+(.+)$',
    r'^[ \t]*sensor#126:[ \t]+value:[ \t]+(.+),[ \t]+flags:[ \t]+(.+),[ \t]+status:[ \t]+(.+),[ \t]+ext_status:[ \t]+(.+)$',
    r'^[ \t]*sensor#128:[ \t]+value:[ \t]+(.+),[ \t]+flags:[ \t]+(.+),[ \t]+status:[ \t]+(.+),[ \t]+ext_status:[ \t]+(.+)$',
    r'^[ \t]*sensor#129:[ \t]+value:[ \t]+(.+),[ \t]+flags:[ \t]+(.+),[ \t]+status:[ \t]+(.+),[ \t]+ext_status:[ \t]+(.+)$',
    r'^[ \t]*sensor#130:[ \t]+value:[ \t]+(.+),[ \t]+flags:[ \t]+(.+),[ \t]+status:[ \t]+(.+),[ \t]+ext_status:[ \t]+(.+)$',
    r'^[ \t]*sensor#131:[ \t]+value:[ \t]+(.+),[ \t]+flags:[ \t]+(.+),[ \t]+status:[ \t]+(.+),[ \t]+ext_status:[ \t]+(.+)$',
    r'^[ \t]*sensor#132:[ \t]+value:[ \t]+(.+),[ \t]+flags:[ \t]+(.+),[ \t]+status:[ \t]+(.+),[ \t]+ext_status:[ \t]+(.+)$',
    r'^[ \t]*sensor#133:[ \t]+value:[ \t]+(.+),[ \t]+flags:[ \t]+(.+),[ \t]+status:[ \t]+(.+),[ \t]+ext_status:[ \t]+(.+)$',
    r'^[ \t]*sensor#136:[ \t]+value:[ \t]+(.+),[ \t]+flags:[ \t]+(.+),[ \t]+status:[ \t]+(.+),[ \t]+ext_status:[ \t]+(.+)$',
    r'^[ \t]*sensor#137:[ \t]+value:[ \t]+(.+),[ \t]+flags:[ \t]+(.+),[ \t]+status:[ \t]+(.+),[ \t]+ext_status:[ \t]+(.+)$',
    r'^[ \t]*sensor#138:[ \t]+value:[ \t]+(.+),[ \t]+flags:[ \t]+(.+),[ \t]+status:[ \t]+(.+),[ \t]+ext_status:[ \t]+(.+)$',
    r'^[ \t]*sensor#139:[ \t]+value:[ \t]+(.+),[ \t]+flags:[ \t]+(.+),[ \t]+status:[ \t]+(.+),[ \t]+ext_status:[ \t]+(.+)$',
    r'^[ \t]*sensor#140:[ \t]+value:[ \t]+(.+),[ \t]+flags:[ \t]+(.+),[ \t]+status:[ \t]+(.+),[ \t]+ext_status:[ \t]+(.+)$',
    r'^[ \t]*sensor#141:[ \t]+value:[ \t]+(.+),[ \t]+flags:[ \t]+(.+),[ \t]+status:[ \t]+(.+),[ \t]+ext_status:[ \t]+(.+)$',
    r'^[ \t]*sensor#142:[ \t]+value:[ \t]+(.+),[ \t]+flags:[ \t]+(.+),[ \t]+status:[ \t]+(.+),[ \t]+ext_status:[ \t]+(.+)$',
    r'^[ \t]*sensor#178:[ \t]+value:[ \t]+(.+),[ \t]+flags:[ \t]+(.+),[ \t]+status:[ \t]+(.+),[ \t]+ext_status:[ \t]+(.+)$',
    r'^[ \t]*sensor#179:[ \t]+value:[ \t]+(.+),[ \t]+flags:[ \t]+(.+),[ \t]+status:[ \t]+(.+),[ \t]+ext_status:[ \t]+(.+)$',
    r'^[ \t]*sensor#180:[ \t]+value:[ \t]+(.+),[ \t]+flags:[ \t]+(.+),[ \t]+status:[ \t]+(.+),[ \t]+ext_status:[ \t]+(.+)$',
    r'^[ \t]*sensor#182:[ \t]+value:[ \t]+(.+),[ \t]+flags:[ \t]+(.+),[ \t]+status:[ \t]+(.+),[ \t]+ext_status:[ \t]+(.+)$',
    r'^[ \t]*sensor#208:[ \t]+value:[ \t]+(.+),[ \t]+flags:[ \t]+(.+),[ \t]+status:[ \t]+(.+),[ \t]+ext_status:[ \t]+(.+)$',
    r'^[ \t]*sensor#210:[ \t]+value:[ \t]+(.+),[ \t]+flags:[ \t]+(.+),[ \t]+status:[ \t]+(.+),[ \t]+ext_status:[ \t]+(.+)$',
    r'^[ \t]*sensor#211:[ \t]+value:[ \t]+(.+),[ \t]+flags:[ \t]+(.+),[ \t]+status:[ \t]+(.+),[ \t]+ext_status:[ \t]+(.+)$',
    r'^[ \t]*sensor#213:[ \t]+value:[ \t]+(.+),[ \t]+flags:[ \t]+(.+),[ \t]+status:[ \t]+(.+),[ \t]+ext_status:[ \t]+(.+)$',
    r'^[ \t]*sensor#214:[ \t]+value:[ \t]+(.+),[ \t]+flags:[ \t]+(.+),[ \t]+status:[ \t]+(.+),[ \t]+ext_status:[ \t]+(.+)$',
    r'^[ \t]*sensor#215:[ \t]+value:[ \t]+(.+),[ \t]+flags:[ \t]+(.+),[ \t]+status:[ \t]+(.+),[ \t]+ext_status:[ \t]+(.+)$',
    r'^[ \t]*sensor#216:[ \t]+value:[ \t]+(.+),[ \t]+flags:[ \t]+(.+),[ \t]+status:[ \t]+(.+),[ \t]+ext_status:[ \t]+(.+)$',
    r'^[ \t]*sensor#217:[ \t]+value:[ \t]+(.+),[ \t]+flags:[ \t]+(.+),[ \t]+status:[ \t]+(.+),[ \t]+ext_status:[ \t]+(.+)$',
    r'^[ \t]*sensor#235:[ \t]+value:[ \t]+(.+),[ \t]+flags:[ \t]+(.+),[ \t]+status:[ \t]+(.+),[ \t]+ext_status:[ \t]+(.+)$',
]

cel_openbmc_util_fruid_pattern = [
    r'^[ \t]*FRU[ \t]+Information[ \t]+:[ \t]+MINILAKE',
    r'^[ \t]*---------------[ \t]+:[ \t]+------------------',
    r'^[ \t]*Chassis[ \t]+Type[ \t]+:[ \t]+Rack[ \t]+Mount[ \t]+Chassis',
    r'^[ \t]*Chassis[ \t]+Part[ \t]+Number[ \t]+:',
    r'^[ \t]*Chassis[ \t]+Serial[ \t]+Number[ \t]+:',
    r'^[ \t]*Board[ \t]+Mfg[ \t]+Date[ \t]+:',
    r'^[ \t]*Board[ \t]+Mfg[ \t]+:[ \t]+Quanta',
    r'^[ \t]*Board[ \t]+Product[ \t]+:[ \t]+Minilake',
    r'^[ \t]*Board[ \t]+Serial[ \t]+:[ \t]+([\w,\d]+)',
    r'^[ \t]*Board[ \t]+Part[ \t]+Number[ \t]+:[ \t]+([\w,\d]+)',
    r'^[ \t]*Board[ \t]+FRU[ \t]+ID[ \t]+:[ \t]+FRU[ \t]+Ver[ \t]+([\d]+.[\d]+)',
    r'^[ \t]*Board[ \t]+Custom[ \t]+Data[ \t]+1[ \t]+:[ \t]+([\d]+\-[\d]+)',
    r'^[ \t]*Product[ \t]+Manufacturer[ \t]+:[ \t]+Quanta',
    r'^[ \t]*Product[ \t]+Name[ \t]+:[ \t]+Minilake',
    r'^[ \t]*Product[ \t]+Part[ \t]+Number[ \t]+:[ \t]+([\w,\d]+)',
    r'^[ \t]*Product[ \t]+Version[ \t]+:[ \t]+Wedge400',
    r'^[ \t]*Product[ \t]+Serial[ \t]+:',
    r'^[ \t]*Product[ \t]+Asset[ \t]+Tag[ \t]+:',
    r'^[ \t]*Product[ \t]+FRU[ \t]+ID[ \t]+:',
    r'^[ \t]*Product[ \t]+Custom[ \t]+Data[ \t]+1[ \t]+:[ \t]+([\d]+\-[\d]+)',
    r'^[ \t]*Product[ \t]+Custom[ \t]+Data[ \t]+2[ \t]+:[ \t]+([\w]+)',
]

cel_openbmc_util_mac_pattern = [
    r'^[ \t]*MAC[ \t]+address:[ \t]+([\w,\d]+):([\w,\d]+):([\w,\d]+):([\w,\d]+):([\w,\d]+):([\w,\d]+)$',
]

cel_openbmc_util_all_version_pattern = [
    r'^[ \t]*ALTBMC[ \t]+Version:[ \t]+.*$',
    r'^[ \t]*BMC[ \t]+Version:[ \t]+.*$',
    r'^[ \t]*Fan[ \t]+Speed[ \t]+Controller[ \t]+Version:[ \t]+.*$',
    r'^[ \t]*ROM[ \t]+Version:[ \t]+.*$',
    r'^[ \t]*TPM[ \t]+Version:[ \t]+.*$',
    r'^[ \t]*FCMCPLD:[ \t]+.*$',
    r'^[ \t]*PWRCPLD:[ \t]+.*$',
    r'^[ \t]*SCMCPLD:[ \t]+.*$',
    r'^[ \t]*SMBCPLD:[ \t]+.*$',
    r'^[ \t]*DOMFPGA1:[ \t]+.*$',
    r'^[ \t]*DOMFPGA2:[ \t]+.*$',
    r'^[ \t]*Bridge-IC[ \t]+Version:[ \t]+.*$',
    r'^[ \t]*Bridge-IC[ \t]+Bootloader[ \t]+Version:[ \t]+.*$',
    r'^[ \t]*BIOS[ \t]+Version:[ \t]+.*$',
    r'^[ \t]*CPLD[ \t]+Version:[ \t]+.*$',
    r'^[ \t]*ME[ \t]+Version:[ \t]+.*$',
    r'^[ \t]*PVCCIN[ \t]+VR[ \t]+Version:[ \t]+.*$',
    r'^[ \t]*DDRAB[ \t]+VR[ \t]+Version:[ \t]+.*$',
    r'^[ \t]*P1V05[ \t]+VR[ \t]+Version:[ \t]+.*$',
]

fwUtilPatternList = [cel_openbmc_util_all_version_pattern]

bicUtilPatternList = [
    cel_openbmc_util_dev_id_pattern,
#    cel_openbmc_util_gpio_status_pattern,
#    cel_openbmc_util_gpio_config_pattern,
#    cel_openbmc_util_config_pattern,
#    cel_openbmc_util_post_code_pattern,
#    cel_openbmc_util_sdr_pattern,
#    cel_openbmc_util_sensor_pattern,
#    cel_openbmc_util_fruid_pattern,
#    cel_openbmc_util_mac_pattern,
]

####FB_SYS_COMM_TCG1-10_COMe NVMe SSD R/W Stress Test####
cel_nvme_stress_tool = 'fio'
cel_nvme_smart_cmd = 'nvme'

cel_nvme_pattern = [
    r'fio-((\d+).(\d+))',
    r'Starting([ \t])+(\d+)([ \t])+threads',
    r'Jobs:([ \t])+(\d+)([ \t])+\(f=(\d+)\):([ \t])+\[m\((\d+)\)\]([ \t])+\[100.0\%([ \t])+done\]',
    r'\(groupid=(\d+),([ \t])+jobs=(\d+)\):([ \t])+err=([ \t])+0:([ \t])+pid=(\d+):',
    r'Run([ \t])+status([ \t])+group([ \t])+0([ \t])+\(all([ \t])+jobs\):',
    r'READ:([ \t])+io=(\d+)(\.*)(\d*)MB\,([ \t])+aggrb=(\d+)(\.*)(\d*)KB/s\,([ \t])+minb=(\d+)(\.*)(\d*)KB/s\,([ \t])+maxb=(\d+)(\.*)(\d*)KB/s\,([ \t])+mint=(\d+)(\.*)(\d*)msec\,([ \t])+maxt=(\d+)(\.*)(\d*)msec',
    r'WRITE:([ \t])+io=(\d+)(\.*)(\d*)MB\,([ \t])+aggrb=(\d+)(\.*)(\d*)KB/s\,([ \t])+minb=(\d+)(\.*)(\d*)KB/s\,([ \t])+maxb=(\d+)(\.*)(\d*)KB/s\,([ \t])+mint=(\d+)(\.*)(\d*)msec\,([ \t])+maxt=(\d+)(\.*)(\d*)msec',
    r'Disk([ \t])+stats([ \t])+\(read\/write\):',
    r'nvme(\d+)n(\d+):([ \t])+ios=(\d+)\/(\d+)\,([ \t])+merge=(\d+)\/(\d+)\,([ \t])+ticks=(\d+)\/(\d+)\,([ \t])+in_queue=(\d+)\,([ \t])+util=((\d+).(\d+))\%',
]

cel_nvme_smart_pattern = [
    r'Smart([ \t])+Log([ \t])+for([ \t])+NVME([ \t])+device:nvme((\d+)[ \t])+namespace-id:([\w,\d]+)',
    r'critical_warning([ \t])+:([ \t])+0',
    r'temperature([ \t])+:([ \t])+(\d+)([ \t])+C',
    r'available_spare([ \t])+:([ \t])+(\d+)\%',
    r'available_spare_threshold([ \t])+:([ \t])+(\d+)\%',
    r'percentage_used([ \t])+:([ \t])+(\d+)\%',
    r'data_units_read([ \t])+:([ \t])+(\d+)',
    r'data_units_written([ \t])+:([ \t])+(\d+)',
    r'host_read_commands([ \t])+:([ \t])+(\d+)',
    r'host_write_commands([ \t])+:([ \t])+(\d+)',
    r'controller_busy_time([ \t])+:([ \t])+(\d+)',
    r'power_cycles([ \t])+:([ \t])+(\d+)',
    r'power_on_hours([ \t])+:([ \t])+(\d+)',
    r'unsafe_shutdowns([ \t])+:([ \t])+(\d+)',
    r'media_errors([ \t])+:([ \t])+0',
    r'num_err_log_entries([ \t])+:([ \t])+0',
    r'Warning([ \t])+Temperature([ \t])+Time([ \t])+:([ \t])+(\d+)',
    r'Critical([ \t])+Composite([ \t])+Temperature([ \t])+Time([ \t])+:([ \t])+(\d+)',
    r'Temperature([ \t])+Sensor([ \t])+(\d+)([ \t])+:([ \t])+(\d+)([ \t])+C',
    r'Temperature([ \t])+Sensor([ \t])+(\d+)([ \t])+:([ \t])+(\d+)([ \t])+C',
    r'Thermal([ \t])+Management([ \t])+T(\d+)([ \t])+Trans([ \t])+Count([ \t])+:([ \t])+(\d+)',
    r'Thermal([ \t])+Management([ \t])+T(\d+)([ \t])+Total([ \t])+Time([ \t])+:([ \t])+(\d+)',
]

####FB_SYS_COMM_TCG1-11_Loopback EEPROM Access Stress Test####
cel_qsfp_tool = 'cel-qsfp-test'
cel_eeprom_stress_tool = 'temp_volt_limit'
#minipack2_cel_eeprom_stress_tool = 'temp_volt_limit'

cel_temp_volt_limit_pattern1 = [
    r'Min_temperature_limit:([ \t])+(\d+)C\';',
    r'Max_temperature_limit:([ \t])+(\d+)C\';',
    r'Low_Voltage_limit:([ \t])+(\d+)mV;',
    r'Max_Voltage_limit:([ \t])+(\d+)mV;',
    r'Number of cycles:([ \t])+(\d+)',
    r'------------cycle([ \t])+count:(\d+)([ \t])+',
    r'p(\d+)#:([ \t])+((\d+).(\d+))V([ \t])pass',
    r'p(\d+)#:([ \t])+((\d+).(\d+))C\'([ \t])pass',
    r'Port([ \t])+#(\d+)([ \t])+eeprom([ \t])+information:',
]

minipack2_cel_temp_volt_limit_pattern1 = [
    r'Min_temperature_limit:([ \t])+(\d+)C\';',
    r'Max_temperature_limit:([ \t])+(\d+)C\';',
    r'Low_Voltage_limit:([ \t])+(\d+)mV;',
    r'Max_Voltage_limit:([ \t])+(\d+)mV;',
    r'Number of cycles:([ \t])+(\d+)',
    r'------------cycle([ \t])+count:(\d+)([ \t])+',
    r'm(\d+) p(\d+)#:([ \t])+((\d+).(\d+))V([ \t])pass',
    r'm(\d+) p(\d+)#:([ \t])+((\d+).(\d+))C\'([ \t])pass',
    r'Pim([ \t])+#(\d+)([ \t])+Port([ \t])+#(\d+)([ \t])+eeprom([ \t])+information:',
]

# QSFP-DD type output
cel_temp_volt_limit_pattern2 = [
    r'Identifier\(([\d]+)\)([ \t])+:([ \t])+([\w,\d]+)',
    r'Identifier([ \t])+description([ \t])+:([ \t])+([\w,\d,\-]+)',
    r'Revision([ \t])+Compliance\(1\)([ \t])+:([ \t])+([\d]+.[\d]+)',
    r'Status\(([\d]+-[\d]+)\)([ \t])+:([ \t])+([\w,\d]+)([ \t])+([\w,\d]+)',
    r'Status([ \t])+description([ \t])+:([ \t])+(\w+)',
    r'Status([ \t])+description([ \t])+:([ \t])+([\w,\d]+)',
    r'Status([ \t])+description([ \t])+:([ \t])+([\w,\d]+)',
    r'Status([ \t])+description([ \t])+:([ \t])+([\w,\d]+)',
    r'Lane([ \t])+Flag([ \t])+Summary\(([\d]+-[\d]+)\)([ \t])+:([ \t])+([\w,\d]+)([ \t])+([\w,\d]+)([ \t])+([\w,\d]+)([ \t])+([\w,\d]+)',
    r'Module-Level([ \t])+Flags\(([\d]+-[\d]+)\)([ \t])+:([ \t])+([\w,\d]+)([ \t])+([\w,\d]+)([ \t])+([\w,\d]+)([ \t])+([\w,\d]+)([ \t])+([\w,\d]+)([ \t])+([\w,\d]+)',
    r'Temperature\(([\d]+-[\d]+)\)([ \t])+:([ \t])+([\d]+.[\d]+)([ \t])+degrees([ \t])+C',
    r'Supply([ \t])+voltage\(([\d]+-[\d]+)\)([ \t])+:([ \t])+([\d]+.[\d]+)([ \t])+V',
    r'AUX1\(([\d]+-[\d]+)\)([ \t])+:([ \t])+([\w,\d]+)([ \t])+([\w,\d]+)',
    r'AUX2\(([\d]+-[\d]+)\)([ \t])+:([ \t])+([\w,\d]+)([ \t])+([\w,\d]+)',
    r'AUX3\(([\d]+-[\d]+)\)([ \t])+:([ \t])+([\w,\d]+)([ \t])+([\w,\d]+)',
    r'Celestica([ \t])+VccTx([ \t])+:([ \t])+([\d]+.[\d]+)([ \t])+V',
    r'Custom([ \t])+monitor\(([\d]+-[\d]+)\)([ \t])+:([ \t])+([\w,\d]+)([ \t])+([\w,\d]+)',
    r'Celestica([ \t])+VccRx([ \t])+:([ \t])+([\w,\d]+)([ \t])+V',
    r'Module([ \t])+Global([ \t])+Controls\(([\d]+-[\d]+)\)([ \t])+:([ \t])+([\w,\d]+)([ \t])+([\w,\d]+)([ \t])+([\w,\d]+)([ \t])+([\w,\d]+)([ \t])+([\w,\d]+)',
    r'Module([ \t])+Active([ \t])+Firmware([ \t])+Version\(([\d]+-[\d]+)\)([ \t])+:([ \t])+([\w,\d]+)',
    r'Module([ \t])+Media([ \t])+Type([ \t])+Encodings\(([\d]+)\)([ \t])+:([ \t])+([\w,\d]+)',
    r'Module([ \t])+Media([ \t])+Type([ \t])+Encodings([ \t])+description([ \t])+:([ \t])+(\w+)',
    r'Vendor([ \t])+Name\(([\d]+-[\d]+)\)([ \t])+:([ \t])+CELESTICA',
    r'Vendor([ \t])+OUI\(([\d]+-[\d]+)\)([ \t])+:([ \t])+(\d+):(\d+):(\d+)',
    r'Vendor([ \t])+PN\(([\d]+-[\d]+)\)([ \t])+:([ \t])+([\w,\d,\-]+)',
    r'Vendor([ \t])+Revsion([ \t])+Number\(([\d]+-[\d]+)\)([ \t])+:([ \t])+(\d+)',
    r'Vendor([ \t])+SN\(([\d]+-[\d]+)\)([ \t])+:([ \t])+([\w,\d]+)',
    r'Date([ \t])+Code\(([\d]+-[\d]+)\)([ \t])+:([ \t])+(\d+)',
    r'CLEI\(([\d]+-[\d]+)\)([ \t])+:',
    r'Module([ \t])+Power([ \t])+Characteristics\(([\d]+-[\d]+)\)([ \t])+:([ \t])+([\w,\d]+)([ \t])+([\w,\d]+)',
    r'Cable([ \t])+Assembly([ \t])+Length\((\d+)\)([ \t])+:([ \t])+([\w,\d]+)',
    r'Cable([ \t])+Assembly([ \t])+Length([ \t])+description([ \t])+:([ \t])+([\d]+.[\d]+)([ \t])+m',
    r'Media([ \t])+Connector([ \t])+Type\((\d+)\)([ \t])+:([ \t])+([\w,\d]+)',
    r'Connector([ \t])+type([ \t])+description([ \t])+:([ \t])+(\w+)',
    r'Copper([ \t])+Cable([ \t])+Attenuation([ \t])+\(([\d]+-[\d]+)\)([ \t])+:([ \t])+([\w,\d]+)([ \t])+([\w,\d]+)([ \t])+([\w,\d]+)([ \t])+([\w,\d]+)([ \t])+([\w,\d]+)([ \t])+([\w,\d]+)',
    r'Cable([ \t])+Assembly([ \t])+Lane([ \t])+Information([ \t])+\(([\d]+-[\d]+)\)([ \t])+:([ \t])+([\w,\d]+)([ \t])+([\w,\d]+)',
    r'Media([ \t])+Interface([ \t])+Technology([ \t])+\((\d+)\)([ \t])+:([ \t])+([\w,\d]+)',
    r'Media([ \t])+Interface([ \t])+Technology([ \t])+description([ \t])+:([ \t])+(\w+)',
    r'Inactive([ \t])+Module([ \t])+firmware([ \t])+\(([\d]+-[\d]+)p(\d)\)([ \t])+:([ \t])+([\d]+.[\d]+)',
    r'Module([ \t])+hardware([ \t])+\(([\d]+-[\d]+)p(\d)\)([ \t])+:([ \t])+([\d]+.[\d]+)',
    r'Temp([ \t])+High([ \t])+Alarm\(([\d]+-[\d]+)p(\d)\)([ \t])+:([ \t])+([\d]+.[\d]+)([ \t])+degrees([ \t])+C',
    r'Temp([ \t])+Low([ \t])+Alarm\(([\d]+-[\d]+)p(\d)\)([ \t])+:([ \t])+([\d]+.[\d]+)([ \t])+degrees([ \t])+C',
    r'Temp([ \t])+High([ \t])+Warning\(([\d]+-[\d]+)p(\d)\)([ \t])+:([ \t])+([\d]+.[\d]+)([ \t])+degrees([ \t])+C',
    r'Temp([ \t])+Low([ \t])+Warning\(([\d]+-[\d]+)p(\d)\)([ \t])+:([ \t])+([\d]+.[\d]+)([ \t])+degrees([ \t])+C',
    r'Supply([ \t])+3.3-volt High Alarm\(([\d]+-[\d]+)p(\d)\)([ \t])+:([ \t])+([\d]+.[\d]+)([ \t])+V',
    r'Supply([ \t])+3.3-volt Low Alarm\(([\d]+-[\d]+)p(\d)\)([ \t])+:([ \t])+([\d]+.[\d]+)([ \t])+V',
    r'Supply([ \t])+3.3-volt High Warning\(([\d]+-[\d]+)p(\d)\)([ \t])+:([ \t])+([\d]+.[\d]+)([ \t])+V',
    r'Supply([ \t])+3.3-volt Low Warning\(([\d]+-[\d]+)p(\d)\)([ \t])+:([ \t])+([\d]+.[\d]+)([ \t])+V',
    r'Aux([ \t])+1([ \t])+monitor([ \t])+High([ \t])+Alarm\(([\d]+-[\d]+)p(\d)\)([ \t])+:([ \t])+([\d]+.[\d]+)([ \t])+mA',
    r'Aux([ \t])+1([ \t])+monitor([ \t])+Low([ \t])+Alarm\(([\d]+-[\d]+)p(\d)\)([ \t])+:([ \t])+([\d]+.[\d]+)([ \t])+mA',
    r'Aux([ \t])+1([ \t])+monitor([ \t])+High([ \t])+Warning\(([\d]+-[\d]+)p(\d)\)([ \t])+:([ \t])+([\d]+.[\d]+)([ \t])+mA',
    r'Aux([ \t])+1([ \t])+monitor([ \t])+Low([ \t])+Warning\(([\d]+-[\d]+)p(\d)\)([ \t])+:([ \t])+([\d]+.[\d]+)([ \t])+mA',
    r'Aux([ \t])+2([ \t])+monitor([ \t])+High([ \t])+Alarm\(([\d]+-[\d]+)p(\d)\)([ \t])+:([ \t])+([\d]+.[\d]+)([ \t])+mA',
    r'Aux([ \t])+2([ \t])+monitor([ \t])+Low([ \t])+Alarm\(([\d]+-[\d]+)p(\d)\)([ \t])+:([ \t])+([\d]+.[\d]+)([ \t])+mA',
    r'Aux([ \t])+2([ \t])+monitor([ \t])+High([ \t])+Warning\(([\d]+-[\d]+)p(\d)\)([ \t])+:([ \t])+([\d]+.[\d]+)([ \t])+mA',
    r'Aux([ \t])+2([ \t])+monitor([ \t])+Low([ \t])+Warning\(([\d]+-[\d]+)p(\d)\)([ \t])+:([ \t])+([\d]+.[\d]+)([ \t])+mA',
    r'Aux([ \t])+3([ \t])+monitor([ \t])+High([ \t])+Alarm\(([\d]+-[\d]+)p(\d)\)([ \t])+:([ \t])+([\d]+.[\d]+)([ \t])+mA',
    r'Aux([ \t])+3([ \t])+monitor([ \t])+Low([ \t])+Alarm\(([\d]+-[\d]+)p(\d)\)([ \t])+:([ \t])+([\d]+.[\d]+)([ \t])+mA',
    r'Aux([ \t])+3([ \t])+monitor([ \t])+High([ \t])+Warning\(([\d]+-[\d]+)p(\d)\)([ \t])+:([ \t])+([\d]+.[\d]+)([ \t])+mA',
    r'Aux([ \t])+3([ \t])+monitor([ \t])+Low([ \t])+Warning\(([\d]+-[\d]+)p(\d)\)([ \t])+:([ \t])+([\d]+.[\d]+)([ \t])+mA',
    r'Custom([ \t])+monitor\(([\d]+-[\d]+)p(\d)\)([ \t])+:([ \t])+([\w,\d]+)([ \t])+([\w,\d]+)([ \t])+([\w,\d]+)([ \t])+([\w,\d]+)([ \t])+([\w,\d]+)([ \t])+([\w,\d]+)([ \t])+([\w,\d]+)([ \t])+([\w,\d]+)',
    r'TX([ \t])+Power([ \t])+High([ \t])+Alarm\(([\d]+-[\d]+)p(\d)\)([ \t])+:([ \t])+([\d]+.[\d]+)([ \t])+mW',
    r'TX([ \t])+Power([ \t])+Low([ \t])+Alarm\(([\d]+-[\d]+)p(\d)\)([ \t])+:([ \t])+([\d]+.[\d]+)([ \t])+mW',
    r'TX([ \t])+Power([ \t])+High([ \t])+Warning\(([\d]+-[\d]+)p(\d)\)([ \t])+:([ \t])+([\d]+.[\d]+)([ \t])+mW',
    r'TX([ \t])+Power([ \t])+Low([ \t])+Warning\(([\d]+-[\d]+)p(\d)\)([ \t])+:([ \t])+([\d]+.[\d]+)([ \t])+mW',
    r'TX([ \t])+Bias([ \t])+High([ \t])+Alarm\(([\d]+-[\d]+)p(\d)\)([ \t])+:([ \t])+([\d]+.[\d]+)([ \t])+mA',
    r'TX([ \t])+Bias([ \t])+Low([ \t])+Alarm\(([\d]+-[\d]+)p(\d)\)([ \t])+:([ \t])+([\d]+.[\d]+)([ \t])+mA',
    r'TX([ \t])+Bias([ \t])+High([ \t])+Warning\(([\d]+-[\d]+)p(\d)\)([ \t])+:([ \t])+([\d]+.[\d]+)([ \t])+mA',
    r'TX([ \t])+Bias([ \t])+Low([ \t])+Warning\(([\d]+-[\d]+)p(\d)\)([ \t])+:([ \t])+([\d]+.[\d]+)([ \t])+mA',
    r'RX([ \t])+Power([ \t])+High([ \t])+Alarm\(([\d]+-[\d]+)p(\d)\)([ \t])+:([ \t])+([\d]+.[\d]+)([ \t])+mW',
    r'RX([ \t])+Power([ \t])+Low([ \t])+Alarm\(([\d]+-[\d]+)p(\d)\)([ \t])+:([ \t])+([\d]+.[\d]+)([ \t])+mW',
    r'RX([ \t])+Power([ \t])+High([ \t])+Warning\(([\d]+-[\d]+)p(\d)\)([ \t])+:([ \t])+([\d]+.[\d]+)([ \t])+mW',
    r'RX([ \t])+Power([ \t])+Low([ \t])+Warning\(([\d]+-[\d]+)p(\d)\)([ \t])+:([ \t])+([\d]+.[\d]+)([ \t])+mW',
]

# QSFP+ type output
cel_temp_volt_limit_pattern3 = [
    r'Identifier\(([\d]+)\)([ \t])+:([ \t])+([\w,\d]+)',
    r'Identifier([ \t])+description([ \t])+:([ \t])+([\w,\+]+)',
    r'Status([ \t])+Indicators\(([\d]+-[\d]+)\)([ \t])+:([ \t])+([\w,\d]+)([ \t])+([\w,\d]+)',
    r'Status([ \t])+indicators([ \t])+description([ \t])+:([ \t])+(\w+)',
    r'Interrupt([ \t])+Flag\(([\d]+-[\d]+)\)([ \t])+:([ \t])+([\w,\d]+)([ \t])+([\w,\d]+)([ \t])+([\w,\d]+)([ \t])+([\w,\d]+)([ \t])+([\w,\d]+)([ \t])+([\w,\d]+)([ \t])+([\w,\d]+)([ \t])+([\w,\d]+)',
    r':([ \t])+([\w,\d]+)([ \t])+([\w,\d]+)([ \t])+([\w,\d]+)([ \t])+([\w,\d]+)([ \t])+([\w,\d]+)([ \t])+([\w,\d]+)([ \t])+([\w,\d]+)([ \t])+([\w,\d]+)',
    r':([ \t])+([\w,\d]+)([ \t])+([\w,\d]+)([ \t])+([\w,\d]+)',
    r'Temperature\(([\d]+-[\d]+)\)([ \t])+:([ \t])+([\d]+.[\d]+)([ \t])+degrees([ \t])+C',
    r'Reserved\(([\d]+-[\d]+)\)([ \t])+:([ \t])+([\w,\d]+)([ \t])+([\w,\d]+)',
    r'Supply([ \t])+Voltage\(([\d]+-[\d]+)\)([ \t])+:([ \t])+([\d]+.[\d]+)([ \t])+V',
    r'Reserved\(([\d]+-[\d]+)\)([ \t])+:([ \t])+([\w,\d]+)([ \t])+([\w,\d]+)',
    r'Celestica([ \t])+VccTx([ \t])+:([ \t])+([\d]+.[\d]+)([ \t])+V',
    r'Vendor([ \t])+Specific\(([\d]+-[\d]+)\)([ \t])+:([ \t])+([\w,\d]+)([ \t])+([\w,\d]+)',
    r'Celestica([ \t])+VccRx([ \t])+:([ \t])+([\d]+.[\d]+)([ \t])+V',
    r'Channel([ \t])+1([ \t])+RX([ \t])+Power\(([\d]+-[\d]+)\)([ \t])+:([ \t])+([\d]+.[\d]+)([ \t])+mW',
    r'Channel([ \t])+2([ \t])+RX([ \t])+Power\(([\d]+-[\d]+)\)([ \t])+:([ \t])+([\d]+.[\d]+)([ \t])+mW',
    r'Channel([ \t])+3([ \t])+RX([ \t])+Power\(([\d]+-[\d]+)\)([ \t])+:([ \t])+([\d]+.[\d]+)([ \t])+mW',
    r'Channel([ \t])+4([ \t])+RX([ \t])+Power\(([\d]+-[\d]+)\)([ \t])+:([ \t])+([\d]+.[\d]+)([ \t])+mW',
    r'Channel([ \t])+1([ \t])+TX([ \t])+Bias\(([\d]+-[\d]+)\)([ \t])+:([ \t])+([\d]+.[\d]+)([ \t])+mA',
    r'Channel([ \t])+2([ \t])+TX([ \t])+Bias\(([\d]+-[\d]+)\)([ \t])+:([ \t])+([\d]+.[\d]+)([ \t])+mA',
    r'Channel([ \t])+3([ \t])+TX([ \t])+Bias\(([\d]+-[\d]+)\)([ \t])+:([ \t])+([\d]+.[\d]+)([ \t])+mA',
    r'Channel([ \t])+4([ \t])+TX([ \t])+Bias\(([\d]+-[\d]+)\)([ \t])+:([ \t])+([\d]+.[\d]+)([ \t])+mA',
    r'Channel([ \t])+1([ \t])+TX([ \t])+Power\(([\d]+-[\d]+)\)([ \t])+:([ \t])+([\d]+.[\d]+)([ \t])+mW',
    r'Channel([ \t])+2([ \t])+TX([ \t])+Power\(([\d]+-[\d]+)\)([ \t])+:([ \t])+([\d]+.[\d]+)([ \t])+mW',
    r'Channel([ \t])+3([ \t])+TX([ \t])+Power\(([\d]+-[\d]+)\)([ \t])+:([ \t])+([\d]+.[\d]+)([ \t])+mW',
    r'Channel([ \t])+4([ \t])+TX([ \t])+Power\(([\d]+-[\d]+)\)([ \t])+:([ \t])+([\d]+.[\d]+)([ \t])+mW',
    r'Reserved([ \t])+channel([ \t])+monitor([ \t])+set([ \t])+4\(([\d]+-[\d]+)\)([ \t])+:([ \t])+([\w,\d]+)([ \t])+([\w,\d]+)([ \t])+([\w,\d]+)([ \t])+([\w,\d]+)([ \t])+([\w,\d]+)([ \t])+([\w,\d]+)([ \t])+([\w,\d]+)([ \t])+([\w,\d]+)',
    r'Reserved([ \t])+channel([ \t])+monitor([ \t])+set([ \t])+5\(([\d]+-[\d]+)\)([ \t])+:([ \t])+([\w,\d]+)([ \t])+([\w,\d]+)([ \t])+([\w,\d]+)([ \t])+([\w,\d]+)([ \t])+([\w,\d]+)([ \t])+([\w,\d]+)([ \t])+([\w,\d]+)([ \t])+([\w,\d]+)',
    r'Vendor Specific\(([\d]+-[\d]+)\)([ \t])+:([ \t])+([\w,\d]+)([ \t])+([\w,\d]+)([ \t])+([\w,\d]+)([ \t])+([\w,\d]+)([ \t])+([\w,\d]+)([ \t])+([\w,\d]+)([ \t])+([\w,\d]+)([ \t])+([\w,\d]+)',
    r'Reserved\(([\d]+-[\d]+)\)([ \t])+:([ \t])+([\w,\d]+)([ \t])+([\w,\d]+)',
    r'Extended([ \t])+Identifier\((\d+)\)([ \t])+:([ \t])+([\w,\d]+)',
    r'Extended([ \t])+identifier([ \t])+description([ \t])+:([ \t])+Power([ \t])+Class([ \t])+(\d+)([ \t])+\(([\d]+.[\d]+)([ \t])+W([ \t])+max.\)',
    r'Extended([ \t])+identifier([ \t])+description([ \t])+:([ \t])+([\w,\d,\s]+)',
    r'Extended([ \t])+identifier([ \t])+description([ \t])+:([ \t])+([\w,\s]+)',
    r'Connector([ \t])+Type\((\d+)\)([ \t])+:([ \t])+([\w,\d]+)',
    r'Connector([ \t])+type([ \t])+description([ \t])+:([ \t])+([\w,\s]+)',
    r'Specification([ \t])+Compliance\(([\d]+-[\d]+)\)([ \t])+:([ \t])+([\w,\d]+)([ \t])+([\w,\d]+)([ \t])+([\w,\d]+)([ \t])+([\w,\d]+)([ \t])+([\w,\d]+)([ \t])+([\w,\d]+)([ \t])+([\w,\d]+)([ \t])+([\w,\d]+)',
    r'Encoding\((\d+)\)([ \t])+:([ \t])+([\w,\d]+)',
    r'Encoding([ \t])+description([ \t])+:([ \t])+Unspecified',
    r'Nominal([ \t])+Bit([ \t])+Rate\((\d+)\)([ \t])+:([ \t])+([\w,\d]+)',
    r'Extended([ \t])+Rate([ \t])+Select([ \t])+Compliance\((\d+)\)([ \t])+:([ \t])+([\w,\d]+)',
    r'Length([ \t])+\(Standard([ \t])+SM([ \t])+Fiber\)\((\d+)\)([ \t])+:([ \t])+0([ \t])+\(km\)',
    r'Length([ \t])+\(OM3\)\((\d+)\)([ \t])+:([ \t])+(\d+)([ \t])+\((\d+)m\)',
    r'Length([ \t])+\(OM2\)\((\d+)\)([ \t])+:([ \t])+(\d+)([ \t])+\(m\)',
    r'Length([ \t])+\(OM1\)\((\d+)\)([ \t])+:([ \t])+(\d+)([ \t])+\(m\)',
    r'Length([ \t])+\(OM4\)\((\d+)\)([ \t])+:([ \t])+(\d+)([ \t])+\(m\)',
    r'Device([ \t])+Technology\((\d+)\)([ \t])+:([ \t])+([\w,\d]+)',
    r'Device([ \t])+technology([ \t])+description([ \t])+:([ \t])+([\w,\s]+)',
    r'Vendor([ \t])+name\(([\d]+-[\d]+)\)([ \t])+:([ \t])+CELESTICA',
    r'Vendor([ \t])+OUI\(([\d]+-[\d]+)\)([ \t])+:([ \t])+(\d+):(\d+):(\d+)',
    r'Vendor([ \t])+PN\(([\d]+-[\d]+)\)([ \t])+:([ \t])+([\w,\d]+)-([\w,\d]+)-(\d+)',
    r'Vendor([ \t])+rev\(([\d]+-[\d]+)\)([ \t])+:([ \t])+(\d+)',
    r'Vendor([ \t])+SN\(([\d]+-[\d]+)\)([ \t])+:([ \t])+([\w,\d]+)',
    r'Date([ \t])+code\(([\d]+-[\d]+)\)([ \t])+:([ \t])+(\d+)__',
    r'Temp([ \t])+High([ \t])+Alarm\(([\d]+-[\d]+)p(\d)\)([ \t])+:([ \t])+((\d+).(\d+))([ \t])+degrees([ \t])+C',
    r'Temp([ \t])+Low([ \t])+Alarm\(([\d]+-[\d]+)p(\d)\)([ \t])+:([ \t])+((\d+).(\d+))([ \t])+degrees([ \t])+C',
    r'Temp([ \t])+High([ \t])+Warning\(([\d]+-[\d]+)p(\d)\)([ \t])+:([ \t])+((\d+).(\d+))([ \t])+degrees([ \t])+C',
    r'Temp([ \t])+Low([ \t])+Warning\(([\d]+-[\d]+)p(\d)\)([ \t])+:([ \t])+((\d+).(\d+))([ \t])+degrees([ \t])+C',
    r'Vcc([ \t])+High([ \t])+Alarm\(([\d]+-[\d]+)p(\d)\)([ \t])+:([ \t])+((\d+).(\d+))([ \t])+V',
    r'Vcc([ \t])+Low([ \t])+Alarm\(([\d]+-[\d]+)p(\d)\)([ \t])+:([ \t])+((\d+).(\d+))([ \t])+V',
    r'Vcc([ \t])+High([ \t])+Warning\(([\d]+-[\d]+)p(\d)\)([ \t])+:([ \t])+((\d+).(\d+))([ \t])+V',
    r'Vcc([ \t])+Low([ \t])+Warning\(([\d]+-[\d]+)p(\d)\)([ \t])+:([ \t])+((\d+).(\d+))([ \t])+V',
    r'RX([ \t])+Power([ \t])+High([ \t])+Alarm\(([\d]+-[\d]+)p(\d)\)([ \t])+:([ \t])+((\d+).(\d+))([ \t])+mW',
    r'RX([ \t])+Power([ \t])+Low([ \t])+Alarm\(([\d]+-[\d]+)p(\d)\)([ \t])+:([ \t])+((\d+).(\d+))([ \t])+mW',
    r'RX([ \t])+Power([ \t])+High([ \t])+Warning\(([\d]+-[\d]+)p(\d)\)([ \t])+:([ \t])+((\d+).(\d+))([ \t])+mW',
    r'RX([ \t])+Power([ \t])+Low([ \t])+Warning\(([\d]+-[\d]+)p(\d)\)([ \t])+:([ \t])+((\d+).(\d+))([ \t])+mW',
    r'TX([ \t])+Bias([ \t])+High([ \t])+Alarm\(([\d]+-[\d]+)p(\d)\)([ \t])+:([ \t])+((\d+).(\d+))([ \t])+mA',
    r'TX([ \t])+Bias([ \t])+Low([ \t])+Alarm\(([\d]+-[\d]+)p(\d)\)([ \t])+:([ \t])+((\d+).(\d+))([ \t])+mA',
    r'TX([ \t])+Bias([ \t])+High([ \t])+Warning\(([\d]+-[\d]+)p(\d)\)([ \t])+:([ \t])+((\d+).(\d+))([ \t])+mA',
    r'TX([ \t])+Bias([ \t])+Low([ \t])+Warning\(([\d]+-[\d]+)p(\d)\)([ \t])+:([ \t])+((\d+).(\d+))([ \t])+mA',
    r'TX([ \t])+Power([ \t])+High([ \t])+Alarm\(([\d]+-[\d]+)p(\d)\)([ \t])+:([ \t])+((\d+).(\d+))([ \t])+mW',
    r'TX([ \t])+Power([ \t])+Low([ \t])+Alarm\(([\d]+-[\d]+)p(\d)\)([ \t])+:([ \t])+((\d+).(\d+))([ \t])+mW',
    r'TX([ \t])+Power([ \t])+High([ \t])+Warning\(([\d]+-[\d]+)p(\d)\)([ \t])+:([ \t])+((\d+).(\d+))([ \t])+mW',
    r'TX([ \t])+Power([ \t])+Low([ \t])+Warning\(([\d]+-[\d]+)p(\d)\)([ \t])+:([ \t])+((\d+).(\d+))([ \t])+mW',
]

cel_temp_volt_limit_start_pattern = [
    r'^Min.*',
    r'^Max.*',
    r'^Low.*',
    r'^Num.*',
    r'^---.*',
    r'^Port([ \t])+#.*',
    r'^Ide.*',
    r'^Rev.*',
    r'^Sta.*',
    r'^Lan.*',
    r'^Mod.*',
    r'^Tem.*',
    r'^Sup.*',
    r'^AUX.*',
    r'^Cel.*',
    r'^Cus.*',
    r'^Ven.*',
    r'^Dat.*',
    r'^CLE.*',
    r'^Cab.*',
    r'^Med.*',
    r'^Con.*',
    r'^Cop.*',
    r'^Ina.*',
    r'^Aux.*',
    r'^Vcc.*',
    r'^TX.*',
    r'^RX.*',
    r'^p(\d+)#.*',
    r'^Int.*',
    r'^Cha.*',
    r'^Res.*',
    r'^Spe.*',
    r'^Enc.*',
    r'^Nom.*',
    r'^Ext.*',
    r'^Len.*',
    r'^Dev.*',
]

####FB_SYS_COMM_TCG1-17_OpenBMC Memory Stress Test####
cel_memtest_stress_tool = 'memtester'

cel_openmbc_memtest_pattern = [
    r'pagesize([ \t])+is([ \t])+(\d+)',
    r'pagesizemask([ \t])+is([ \t])+([\w,\d]+)',
    r'want([ \t])+(\d+)MB([ \t])+\((\d+)([ \t])+bytes\)',
    r'got([ \t])+(\d+)MB([ \t])+\((\d+)([ \t])+bytes\)\,([ \t])+trying([ \t])+mlock([ \t])+\.\.\.locked\.',
    r'Loop([ \t])+(\d+)\/(\d+):',
    r'Stuck([ \t])+Address([ \t])+:([ \t])+ok',
    r'Random([ \t])+Value([ \t])+:([ \t])+ok',
    r'Compare([ \t])+XOR([ \t])+:([ \t])+ok',
    r'Compare([ \t])+SUB([ \t])+:([ \t])+ok',
    r'Compare([ \t])+MUL([ \t])+:([ \t])+ok',
    r'Compare([ \t])+DIV([ \t])+:([ \t])+ok',
    r'Compare([ \t])+OR([ \t])+:([ \t])+ok',
    r'Compare([ \t])+AND([ \t])+:([ \t])+ok',
    r'Sequential([ \t])+Increment([ \t])+:([ \t])+ok',
    r'Solid([ \t])+Bits([ \t])+:([ \t])+ok',
    r'Block([ \t])+Sequential([ \t])+:([ \t])+ok',
    r'Checkerboard([ \t])+:([ \t])+ok',
    r'Bit([ \t])+Spread([ \t])+:([ \t])+ok',
    r'Bit([ \t])+Flip([ \t])+:([ \t])+ok',
    r'Walking([ \t])+Ones([ \t])+:([ \t])+ok',
    r'Walking([ \t])+Zeroes([ \t])+:([ \t])+ok',
    r'8-bit([ \t])+Writes([ \t])+:([ \t])+ok',
    r'16-bit([ \t])+Writes([ \t])+:([ \t])+ok',
    r'Done\.',
]


####FB_SYS_COMM_TCG1-18_OpenBMC I2C Bus Scan Stress Test####
cel_i2c_scan_stress_tool = 'cel-i2c-test'

cel_openmbc_i2c_key_list = [
   'show',
]

cel_openmbc_i2c_option_list = {
    'show' : '-s',
}

cel_openmbc_i2c_pattern = [
    r'(device)([ \t])+bus([ \t])+address([ \t])+status',
    r'(SCM_COMe_BIC)([ \t])+(\d+)([ \t])+0x20([ \t])+OK',
    r'(SCM_CPLD)([ \t])+(\d+)([ \t])+0x3e([ \t])+OK',
    r'(SCM_Hot_Swap)([ \t])+(\d+)([ \t])+(0x10|0x44)([ \t])+OK',
    r'(SCM_LM75_1)([ \t])+(\d+)([ \t])+0x4c([ \t])+OK',
    r'(SCM_LM75_2)([ \t])+(\d+)([ \t])+0x4d([ \t])+OK',
    r'(SCM_EEPROM)([ \t])+(\d+)([ \t])+0x52([ \t])+OK',
    r'(SCM_54616_EEPROM)([ \t])+(\d+)([ \t])+0x50([ \t])+OK',
    r'(SCM_PCIE_CLOCK_BUF)([ \t])+(\d+)([ \t])+0x6C([ \t])+OK',
    r'(BSM_EEPROM)([ \t])+(\d+)([ \t])+0x56([ \t])+OK',
    r'((SMB|PSB)_Power_Sequence)([ \t])+(\d+)([ \t])+0x3a([ \t])+OK',
    r'(SMB_Power_DC-DC_core_base)([ \t])+(\d+)([ \t])+0x28([ \t])+OK',
    r'(SMB_Power_DC-DC_core_pmbus)([ \t])+(\d+)([ \t])+0x40([ \t])+OK',
    r'(SMB_Power_Left_base)([ \t])+(\d+)([ \t])+0x35([ \t])+OK',
    r'(SMB_Power_Left_pmbus)([ \t])+(\d+)([ \t])+0x4d([ \t])+OK',
    r'(SMB_Power_Right_base)([ \t])+(\d+)([ \t])+0x2f([ \t])+OK',
    r'(SMB_Power_Right_pmbus)([ \t])+(\d+)([ \t])+0x47([ \t])+OK',
    r'(SMB_PXE1211)([ \t])+(\d+)([ \t])+0x0E([ \t])+OK',
    r'(SMB_Temp_LM75B_1)([ \t])+(\d+)([ \t])+0x48([ \t])+OK',
    r'(SMB_Temp_LM75B_2)([ \t])+(\d+)([ \t])+0x49([ \t])+OK',
    r'(SMB_Temp_LM75B_3)([ \t])+(\d+)([ \t])+0x4A([ \t])+OK',
    r'(SMB_Temp_LM75B_4)([ \t])+(\d+)([ \t])+0x4B([ \t])+OK',
    r'(SMB_Temp_TPM421_1)([ \t])+(\d+)([ \t])+0x4C([ \t])+OK',
    r'(SMB_Temp_TPM421_2)([ \t])+(\d+)([ \t])+0x4E([ \t])+OK',
    r'(Switch_Gibraltar)([ \t])+(\d+)([ \t])+0x2A([ \t])+OK',
    r'(SMB_PCA9555_Io_Expander)([ \t])+(\d+)([ \t])+0x27([ \t])+OK',
    r'(SMB_DOM_FPGA_2)([ \t])+(\d+)([ \t])+0x60([ \t])+OK',
    r'(SMB_EEPROM)([ \t])+(\d+)([ \t])+0x51([ \t])+OK',
    r'(RACKMON_EEPROM)([ \t])+(\d+)([ \t])+0x50([ \t])+OK',
    r'(SMB_LEDs)([ \t])+(\d+)([ \t])+0x20([ \t])+OK',
    r'(SMB_Board_ID)([ \t])+(\d+)([ \t])+0x21([ \t])+OK',
    r'(SMB_TPM)([ \t])+(\d+)([ \t])+0x2e([ \t])+OK',
    r'(SMB_PWR_CPLD)([ \t])+(\d+)([ \t])+0x3e([ \t])+OK',
    r'(SMB_GB_Clock)([ \t])+(\d+)([ \t])+0x74([ \t])+OK',
    r'(SMB_CPLD)([ \t])+(\d+)([ \t])+0x3E([ \t])+OK',
    r'(SMB_DOM_FPGA_1)([ \t])+(\d+)([ \t])+0x60([ \t])+OK',
    r'(PDB_PEM_1_EEPROM)([ \t])+(\d+)([ \t])+0x50([ \t])+OK',
    r'(PDB_PEM_1_Hot_Swap)([ \t])+(\d+)([ \t])+0x58([ \t])+OK',
    r'(PDB_PEM_1_Thermal)([ \t])+(\d+)([ \t])+0x18([ \t])+OK',
    r'(PDB_PEM_2_EEPROM)([ \t])+(\d+)([ \t])+0x50([ \t])+OK',
    r'(PDB_PEM_2_Hot_Swap)([ \t])+(\d+)([ \t])+0x58([ \t])+OK',
    r'(PDB_PEM_2_Thermal)([ \t])+(\d+)([ \t])+0x18([ \t])+OK',
    r'(PSU_1_EEPROM)([ \t])+(\d+)([ \t])+0x50([ \t])+OK',
    r'(PSU_1)([ \t])+(\d+)([ \t])+0x58([ \t])+OK',
    r'(PSU_2_EEPROM)([ \t])+(\d+)([ \t])+0x50([ \t])+OK',
    r'(PSU_2)([ \t])+(\d+)([ \t])+0x58([ \t])+OK',
    r'(Power_Hbm)([ \t])+(\d+)([ \t])+0x0E([ \t])+OK',
    r'(FCM_CPLD)([ \t])+(\d+)([ \t])+0x3e([ \t])+OK',
    r'(FCM_EEPROM)([ \t])+(\d+)([ \t])+0x51([ \t])+OK',
    r'(FCM_LM75_1)([ \t])+(\d+)([ \t])+0x48([ \t])+OK',
    r'(FCM_LM75_2)([ \t])+(\d+)([ \t])+0x49([ \t])+OK',
    r'(FCM_Hot_Swap)([ \t])+(\d+)([ \t])+(0x10|0x44)([ \t])+OK',
    r'(FCM_Fan_tray_1)([ \t])+(\d+)([ \t])+0x52([ \t])+OK',
    r'(FCM_Fan_tray_2)([ \t])+(\d+)([ \t])+0x52([ \t])+OK',
    r'(FCM_Fan_tray_3)([ \t])+(\d+)([ \t])+0x52([ \t])+OK',
    r'(FCM_Fan_tray_4)([ \t])+(\d+)([ \t])+0x52([ \t])+OK',
]

cel_openmbc_i2c_pattern_list = {
    'show' : cel_openmbc_i2c_pattern,
}


####FB_SYS_COMM_TCG1-19_TPM_Module_Access_Stress_test####
cel_tpm_stress_tool = 'cel-tpm-test'
cel_eltt2_stress_tool = 'eltt2'

cel_tpm_status_pattern = [
    r'run([ \t])+\.\.\/utility\/eltt2([ \t])+\-t([ \t])+full',
    r'Successfully([ \t])+tested\.([ \t])+Works([ \t])+as([ \t])+expected.',
    r'TPM([ \t])+testall([ \t])+\|([ \t])+PASS([ \t])+\|',
    r'TPM([ \t])+get([ \t])+PCRs([ \t])+\|([ \t])+PASS([ \t])+\|',
]


####FB_SYS_COMM_TCG1-20_All_Ports_Enable_Disable###
SDK_LOG_FILE = "/root/auto_load_user_output.log"
DUT_PHASE = 'EVT2'

local_Bin_Python3 = '/usr/local/bin/python3'
bin_Python3 = '/usr/bin/python3'
default_begin_check_line = 900
default_read_range = 1000
tmp_file_on_dut = '/tmp/dut_output'
end_of_cmd_mark = 'is not defined'

qsfpDDPortNum = list(range(0, 16))
qsfp56PortNum = list(range(16, 48))
qsfp2x25PortNum = list(range(16, 79))

ALL_PORT_NUM = qsfpDDPortNum + qsfp56PortNum
ALL_PORT_NUM_2X2X25G = qsfpDDPortNum + qsfp2x25PortNum
ALL_PORT_COUNT = len(ALL_PORT_NUM)
ALL_PORT_COUNT_2X2X25G = len(ALL_PORT_NUM_2X2X25G)

sensor_u_pattern = [
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
GB_INIT_PASS_MSG = '-do_reinit_test-.*?PASS'
GB_PORT_LINKUP_PASS_MSG = '-do_port_linkup_validation_test-.*?PASS'
SNAKE_TRAFFIC_PASS_MSG = 'L2 snake traffic with cpu injection.*?PASS'
true_keyword = 'PASS'
SDK_TIMEOUT1 = 600
SDK_TIMEOUT2 = 8000
COMMON_SDK_PROMPT = '>>>'
COMMON_SDK_PROMPT_II = 'Counters Consistency Check Passed!!!'
MINIPACK2_SDK_PROMPT = 'BCM.0>'
MINIPACK2_SDK_PROMPT_NOTH4 = 'BCM>'
ERROR_STR = 'Error'
FAIL_STR = 'Fail'
NO_SUCH_FILE_STR = 'No such file or directory'
SDK_WAIT_PATTERN_LIST = [ERROR_STR, COMMON_SDK_PROMPT, NO_SUCH_FILE_STR]
MINIPACK2_SDK_WAIT_PATTERN_LIST = [ERROR_STR, FAIL_STR, MINIPACK2_SDK_PROMPT, NO_SUCH_FILE_STR]
MINIPACK2_SDK_WAIT_PATTERN_LIST1 = [ERROR_STR, MINIPACK2_SDK_PROMPT, NO_SUCH_FILE_STR, MINIPACK2_SDK_PROMPT_NOTH4]

portStatusDD_8X50G_QSFP_4X50G = {}
for i in ALL_PORT_NUM:
    portStatusDD_8X50G_QSFP_4X50G[i] = {}
    if i in qsfpDDPortNum:
        portStatusDD_8X50G_QSFP_4X50G[i]['link_name'] = '8x50G'
    elif i in qsfp56PortNum:
        portStatusDD_8X50G_QSFP_4X50G[i]['link_name'] = '4x50G'
    portStatusDD_8X50G_QSFP_4X50G[i]['link_status'] = 'True'
    portStatusDD_8X50G_QSFP_4X50G[i]['pcs_status'] = 'True'
    if i == 0:
        portStatusDD_8X50G_QSFP_4X50G[i]['link_name'] = '4x50G'
    if i == 16:
        portStatusDD_8X50G_QSFP_4X50G[i]['link_name'] = '8x50G'


portStatusDD_8X50G_QSFP_4X25G = {}
for i in ALL_PORT_NUM:
    portStatusDD_8X50G_QSFP_4X25G[i] = {}
    if i in qsfpDDPortNum:
        portStatusDD_8X50G_QSFP_4X25G[i]['link_name'] = '8x50G'
    elif i in qsfp56PortNum:
        portStatusDD_8X50G_QSFP_4X25G[i]['link_name'] = '4x25G'
    portStatusDD_8X50G_QSFP_4X25G[i]['link_status'] = 'True'
    portStatusDD_8X50G_QSFP_4X25G[i]['pcs_status'] = 'True'
    if i == 0:
        portStatusDD_8X50G_QSFP_4X25G[i]['link_name'] = '4x25G'
    if i == 16:
        portStatusDD_8X50G_QSFP_4X25G[i]['link_name'] = '8x50G'


portStatusDD_4X50G_QSFP_4X25G = {}
for i in ALL_PORT_NUM:
    portStatusDD_4X50G_QSFP_4X25G[i] = {}
    if i in qsfpDDPortNum:
        portStatusDD_4X50G_QSFP_4X25G[i]['link_name'] = '4x50G'
    elif i in qsfp56PortNum:
        portStatusDD_4X50G_QSFP_4X25G[i]['link_name'] = '4x25G'
    portStatusDD_4X50G_QSFP_4X25G[i]['link_status'] = 'True'
    portStatusDD_4X50G_QSFP_4X25G[i]['pcs_status'] = 'True'


portStatusDD_4X25G_QSFP_4X25G = {}
for i in ALL_PORT_NUM:
    portStatusDD_4X25G_QSFP_4X25G[i] = {}
    portStatusDD_4X25G_QSFP_4X25G[i]['link_name'] = '4x25G'
    portStatusDD_4X25G_QSFP_4X25G[i]['link_status'] = 'True'
    portStatusDD_4X25G_QSFP_4X25G[i]['pcs_status'] = 'True'


portStatusDD_4X25G_QSFP_2X2X25G = {}
for i in ALL_PORT_NUM:
    portStatusDD_4X25G_QSFP_2X2X25G[i] = {}
    portStatusDD_4X25G_QSFP_2X2X25G[i]['link_name'] = '2x25G'
    portStatusDD_4X25G_QSFP_2X2X25G[i]['link_status'] = 'True'
    portStatusDD_4X25G_QSFP_2X2X25G[i]['pcs_status'] = 'True'


#"SDK Release Version, SDK Release Data, Cisco SDK Version, GB Serdes FW Version"
sdk_version_dict = ('V2.0.0', '2020-07-06', '1.30.1b', '0.19.0.1111')


portFEC_DD_8X50G_QSFP_4X50G = {}
for i in ALL_PORT_NUM:
    portFEC_DD_8X50G_QSFP_4X50G[i] = {}
    if i in [16, qsfpDDPortNum]:
        portFEC_DD_8X50G_QSFP_4X50G[i]['link_name'] = '8x50G'
    elif i in qsfp56PortNum:
        portFEC_DD_8X50G_QSFP_4X50G[i]['link_name'] = '4x50G'
    portFEC_DD_8X50G_QSFP_4X50G[i]['FEC'] = '3'
    if i == 0:
        portFEC_DD_8X50G_QSFP_4X50G[i]['link_name'] = '4x50G'


portFEC_DD_8X50G_QSFP_4X25G = {}
for i in ALL_PORT_NUM:
    portFEC_DD_8X50G_QSFP_4X25G[i] = {}
    if i in [16, qsfpDDPortNum]:
        portFEC_DD_8X50G_QSFP_4X25G[i]['link_name'] = '8x50G'
        portFEC_DD_8X50G_QSFP_4X25G[i]['FEC'] = '3'
    elif i in qsfp56PortNum:
        portFEC_DD_8X50G_QSFP_4X25G[i]['link_name'] = '4x25G'
        portFEC_DD_8X50G_QSFP_4X25G[i]['FEC'] = '2'
    if i == 0:
        portFEC_DD_8X50G_QSFP_4X25G[i]['link_name'] = '4x25G'
        portFEC_DD_8X50G_QSFP_4X25G[i]['FEC'] = '2'


portFEC_DD_4X50G_QSFP_4X25G = {}
for i in ALL_PORT_NUM:
    portFEC_DD_4X50G_QSFP_4X25G[i] = {}
    if i in [16, qsfpDDPortNum]:
        portFEC_DD_4X50G_QSFP_4X25G[i]['link_name'] = '4x50G'
        portFEC_DD_4X50G_QSFP_4X25G[i]['FEC'] = '3'
    elif i in qsfp56PortNum:
        portFEC_DD_4X50G_QSFP_4X25G[i]['link_name'] = '4x25G'
        portFEC_DD_4X50G_QSFP_4X25G[i]['FEC'] = '2'
    if i == 0:
        portFEC_DD_4X50G_QSFP_4X25G[i]['link_name'] = '4x25G'
        portFEC_DD_4X50G_QSFP_4X25G[i]['FEC'] = '2'


portFEC_DD_4X25G_QSFP_2X2X25G = {}
for i in ALL_PORT_NUM_2X2X25G:
    portFEC_DD_4X25G_QSFP_2X2X25G[i] = {}
    if i in [16, qsfpDDPortNum]:
        portFEC_DD_4X25G_QSFP_2X2X25G[i]['link_name'] = '4x25G'
        portFEC_DD_4X25G_QSFP_2X2X25G[i]['FEC'] = '2'
    elif i in qsfp2x25PortNum:
        portFEC_DD_4X25G_QSFP_2X2X25G[i]['link_name'] = '2x25G'
        portFEC_DD_4X25G_QSFP_2X2X25G[i]['FEC'] = '3'
    if i == 0:
        portFEC_DD_4X25G_QSFP_2X2X25G[i]['link_name'] = '2x25G'
        portFEC_DD_4X25G_QSFP_2X2X25G[i]['FEC'] = '2'


portFEC_DD_4X25G_QSFP_4X25G = {}
for i in ALL_PORT_NUM:
    portFEC_DD_4X25G_QSFP_4X25G[i] = {}
    portFEC_DD_4X25G_QSFP_4X25G[i]['link_name'] = '4x25G'
    portFEC_DD_4X25G_QSFP_4X25G[i]['FEC'] = '2'

##### Minipack2 definitions #####
xphyback = "xphyback_7nm"
xphy_tool = "xphy"
xphy_init_options = "init mode=2 pim={} iftype=11 txfir=1 txfirshow=0 dscdump=0 download=1 fecmode=0"
xphy_init_all_pims = "parinit mode=2 pim=9 iftype=11 txfir=1 txfirshow=0 dscdump=0 download=1 fecmode=0"
xphy_max_pims = 8
minipack2_set_vlan_cmd = "linespeed200G.soc"
minipack2_vlan_output_pattern = "ADD:([ \t])+mac=([\d]+:[\d]+:[\d]+:[\d]+:[\d]+:[\d]+)([ \t])+vlan=([\d]+)([ \t])+GPORT=([\w,\d]+)([ \t])+modid=[\d]+([ \t])+port=[\d]+\/cd[\d]+"
lb_mac_pimNum5_200G_200G = 'port cd4-cd7,cd12-cd15,cd20-cd23,cd28-cd31,cd44-cd47,cd52-cd55,cd36-cd39,cd60-cd63,cd66-cd67,cd72-cd73,cd80-cd81,cd88-cd89,cd96-cd97,cd104-cd105,cd112-cd113,cd120-cd121 lb=mac'
lb_mac_pimNum4_200G_200G = 'port cd12-cd15,cd4-cd7,cd20-cd23,cd28-cd31,cd36-cd37,cd44-cd45,cd62-cd63,cd52-cd53,cd38-cd39,cd46-cd47,cd54-cd55,cd60-cd61,cd64-cd67,cd72-cd75,cd80-cd83,cd88-cd91,cd120-cd123,cd112-cd115,cd104-cd107,cd96-cd99 lb=mac'
minipack2_start_cpu_traffic_cmd = "tx 100 pbm=cd0 vlan=10 length=295 SM=0x1 DM=0x2"
minipack2_stop_cpu_traffic_cmd = "pvlan set cd127 1888"

fail_pattern = ["fail", "ERROR", "cannot read file", "command not found",  "Unknown command"]

xphy_init_status = [
    'phy=0x[12345678]0,port=0.*?bcm_plp_force_tx_training_set.*?passed:.*?',
    'phy=0x[12345678]0,port=1.*?bcm_plp_force_tx_training_set.*?passed:.*?',
    'phy=0x[12345678]0,port=2.*?bcm_plp_force_tx_training_set.*?passed:.*?',
    'phy=0x[12345678]0,port=3.*?bcm_plp_force_tx_training_set.*?passed:.*?',
    'phy=0x[12345678]4,port=0.*?bcm_plp_force_tx_training_set.*?passed:.*?',
    'phy=0x[12345678]4,port=1.*?bcm_plp_force_tx_training_set.*?passed:.*?',
    'phy=0x[12345678]4,port=2.*?bcm_plp_force_tx_training_set.*?passed:.*?',
    'phy=0x[12345678]4,port=3.*?bcm_plp_force_tx_training_set.*?passed:.*?',
    'phy=0x[12345678]8,port=0.*?bcm_plp_force_tx_training_set.*?passed:.*?',
    'phy=0x[12345678]8,port=1.*?bcm_plp_force_tx_training_set.*?passed:.*?',
    'phy=0x[12345678]8,port=2.*?bcm_plp_force_tx_training_set.*?passed:.*?',
    'phy=0x[12345678]8,port=3.*?bcm_plp_force_tx_training_set.*?passed:.*?',
    'phy=0x[12345678]c,port=0.*?bcm_plp_force_tx_training_set.*?passed:.*?',
    'phy=0x[12345678]c,port=1.*?bcm_plp_force_tx_training_set.*?passed:.*?',
    'phy=0x[12345678]c,port=2.*?bcm_plp_force_tx_training_set.*?passed:.*?',
    'phy=0x[12345678]c,port=3.*?bcm_plp_force_tx_training_set.*?passed:.*?',
]


##### FB_SYS_COM_TCG1-04_IPMI_Interface_Stress_Test #####
minipack2_cel_ipmitool_pattern = [
    r'Device ID([ \t])+:([ \t])+(\d+)',
    r'Device Revision([ \t])+:([ \t])+(\d+)',
    r'Firmware Revision([ \t])+:([ \t])+((\d+).(\d+))',
    r'IPMI Version([ \t])+:([ \t])+((\d+).(\d+))',
    r'Manufacturer ID([ \t])+:([ \t])+(\d+)',
    r'Manufacturer Name([ \t])+:([ \t])+(\w+)([ \t])+\(([\w,\d]+)\)',
    r'Product ID([ \t])+:([ \t])+(\d+)([ \t])+\(([\w,\d]+)\)',
    r'Product Name([ \t])+:([ \t])+(\w+)([ \t])+\(([\w,\d]+)\)',
    r'Device Available([ \t])+:([ \t])+yes',
    r'Provides Device SDRs([ \t])+:([ \t])+yes',
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
]

xphyback_dict = {"16nm": "xphyback_16nm", "7nm": "xphyback_7nm"}
xphy_init_mode2 = "for pimx in $(seq 1 8); do ./xphy init mode=2 pim=$pimx iftype=11 txfir=1 txfirshow=0 dscdump=0 download=1 fecmode=0; done"
xphy_init_mode2_pim5 = "for pimx in 1 2 6 7 8; do ./xphy init mode=2 pim=$pimx iftype=11 txfir=1 txfirshow=0 dscdump=0 download=1 fecmode=0; done"
xphy_init_mode2_pim4 = "for pimx in 1 2 7 8; do ./xphy init mode=2 pim=$pimx iftype=11 txfir=1 txfirshow=0 dscdump=0 download=1 fecmode=0; done"
##### FB_SYS_COM_TCG1-13_OpenBMC_I2C_Bus_Scan_Stress_Test #####
minipack2_cel_openmbc_i2c_pattern_fcm_b = [
    r'device([ \t])+bus([ \t])+address([ \t])+status',
    r'FCM_B_CPLD([ \t])+72([ \t])+0x33([ \t])+OK',
    r'FCM_B_EEPROM([ \t])+73([ \t])+0x53([ \t])+OK',
    r'FCM_B_LM75_R([ \t])+74([ \t])+0x48([ \t])+OK',
    r'FCM_B_LM75_L([ \t])+74([ \t])+0x49([ \t])+OK',
    r'FCM_B_Hot_Swap([ \t])+75([ \t])+0x10([ \t])+OK',
    r'FCM_B_Fan_tray_2([ \t])+76([ \t])+0x52([ \t])+OK',
    r'FCM_B_Fan_tray_4([ \t])+77([ \t])+0x52([ \t])+OK',
    r'FCM_B_Fan_tray_6([ \t])+78([ \t])+0x52([ \t])+OK',
    r'FCM_B_Fan_tray_8([ \t])+79([ \t])+0x52([ \t])+OK',
    r'FCM_B_PCA9548([ \t])+27([ \t])+0x76([ \t])+OK',
]

minipack2_cel_openmbc_i2c_pattern_fcm_t = [
    r'device([ \t])+bus([ \t])+address([ \t])+status',
    r'FCM_T_CPLD([ \t])+64([ \t])+0x33([ \t])+OK',
    r'FCM_T_EEPROM([ \t])+65([ \t])+0x53([ \t])+OK',
    r'FCM_T_LM75_1([ \t])+66([ \t])+0x48([ \t])+OK',
    r'FCM_T_LM75_2([ \t])+66([ \t])+0x49([ \t])+OK',
    r'FCM_T_Hot_Swap([ \t])+67([ \t])+0x10([ \t])+OK',
    r'FCM_T_Fan_tray_1([ \t])+68([ \t])+0x52([ \t])+OK',
    r'FCM_T_Fan_tray_3([ \t])+69([ \t])+0x52([ \t])+OK',
    r'FCM_T_Fan_tray_5([ \t])+70([ \t])+0x52([ \t])+OK',
    r'FCM_T_Fan_tray_7([ \t])+71([ \t])+0x52([ \t])+OK',
    r'FCM_T_PCA9548([ \t])+26([ \t])+0x76([ \t])+OK',
]
minipack2_cel_openmbc_i2c_pattern_pdb_L = [
    r'device([ \t])+bus([ \t])+address([ \t])+status',
    r'PDB_L_TPM75_TOP[ \t]+52[ \t]+0x49[ \t]+OK',
    r'PDB_L_CPLD([ \t])+55([ \t])+0x60([ \t])+OK',
    r'PDB_L_CPLD_FW([ \t])+53([ \t])+0x40([ \t])+OK',
    r'PDB_L_TPM75_BOTTOM[ \t]+51[ \t]+0x48[ \t]+OK',
    r'PDB_L_PCA9548([ \t])+24([ \t])+0x71([ \t])+OK',
    r'PSU_1_EEPROM([ \t])+48([ \t])+0x50([ \t])+OK',
    r'PSU_1([ \t])+48([ \t])+0x58([ \t])+OK',
    r'PSU_2_EEPROM([ \t])+49([ \t])+0x52([ \t])+OK',
    r'PSU_2([ \t])+49([ \t])+0x5A([ \t])+OK',
    r'SIM_EEPROM([ \t])+50([ \t])+0x14([ \t])+OK',
    r'SIM_LED_DIRVER([ \t])+50([ \t])+0x51([ \t])+OK',
    r'SIM_LPM75([ \t])+50([ \t])+0x4C([ \t])+OK',
    r'TPM75_BOTTOM_L([ \t])+51([ \t])+0x48([ \t])+OK',
    r'TPM75_TOP_L([ \t])+52([ \t])+0x49([ \t])+OK',
    r'PCA9534([ \t])+54([ \t])+0x21([ \t])+OK',
    r'PDB_L_CPLD([ \t])+53([ \t])+0x60([ \t])+OK',
    r'PDB_L_CPLD_FW([ \t])+55([ \t])+0x40([ \t])+OK',
]

minipack2_cel_openmbc_i2c_pattern_pdb_R = [
    r'device([ \t])+bus([ \t])+address([ \t])+status',
    #r'PDB_R_PCA9548([ \t])+25([ \t])+0x72([ \t])+OK',
    #r'PSU_3_EEPROM([ \t])+56([ \t])+0x50([ \t])+OK',
    #r'PSU_3([ \t])+56([ \t])+0x58([ \t])+OK',
    #r'PSU_4_EEPROM([ \t])+57([ \t])+0x52([ \t])+OK',
    #r'PSU_4([ \t])+57([ \t])+0x5A([ \t])+OK',
    #r'TPM75_BOTTOM_R([ \t])+59([ \t])+0x48([ \t])+OK',
    #r'TPM75_TOP_R([ \t])+60([ \t])+0x49([ \t])+OK',
    #r'PCA9534_R([ \t])+62([ \t])+0x21([ \t])+OK',
    #r'PDB_R_CPLD([ \t])+61([ \t])+0x60([ \t])+OK',
    #r'PDB_R_CPLD_FW([ \t])+63([ \t])+0x40([ \t])+OK',
    r'PDB_R_PCA9548.*?OK',
    r'PSU_3_EEPROM.*?OK',
    r'PSU_3.*?OK',
    r'PSU_4_EEPROM.*?OK',
    r'PSU_4.*?OK',
    r'TPM75_BOTTOM.*?OK',
    r'TPM75_TOP.*?OK',
    r'PCA9534.*?OK',
    r'PDB_R_CPLD.*?OK',
    r'PDB_R_CPLD_FW.*?OK',
]

minipack2_cel_openmbc_i2c_pattern_sim = [
    r'device([ \t])+bus([ \t])+address([ \t])+status',
    r'SIM_EEPROM([ \t])+50([ \t])+0x52([ \t])+OK',
    r'SIM_LP5012([ \t])+50([ \t])+0x14([ \t])+OK',
    r'SIM_LM75([ \t])+50([ \t])+0x4C([ \t])+OK',
]

minipack2_cel_openmbc_i2c_pattern_bmc = [
    r'device([ \t])+bus([ \t])+address([ \t])+status',
    r'COMe_BIC([ \t])+0([ \t])+0x20([ \t])+OK',
    r'TPM([ \t])+7([ \t])+0x2E([ \t])+OK',
    r'BMC_LM75([ \t])+8([ \t])+0x4A([ \t])+OK',
    r'BMC_EEPROM([ \t])+8([ \t])+0x51([ \t])+OK',
]

minipack2_cel_openmbc_i2c_pattern_smb = [
    r'device([ \t])+bus([ \t])+address([ \t])+status',
    #r'SMB_DC-DC_1([ \t])+1([ \t])+0x53([ \t])+OK',
    #r'SMB_DC-DC_2([ \t])+1([ \t])+0x59([ \t])+OK',
    #r'SMB_DC-DC_core([ \t])+1([ \t])+0x28([ \t])+OK',
    #r'SMB_LM75_1([ \t])+3([ \t])+0x48([ \t])+OK',
    #r'SMB_LM75_2([ \t])+3([ \t])+0x49([ \t])+OK',
    #r'SMB_LM75_3([ \t])+3([ \t])+0x4A([ \t])+OK',
    #r'SMB_TMP422([ \t])+3([ \t])+0x4C([ \t])+OK',
    #r'SMB_UCD90160A_1([ \t])+5([ \t])+0x35([ \t])+OK',
    #r'SMB_UCD90160A_2([ \t])+5([ \t])+0x36([ \t])+OK',
    #r'SMB_SI53108_1([ \t])+6([ \t])+0x6C([ \t])+OK',
    #r'SMB_SI53108_2([ \t])+7([ \t])+0x6C([ \t])+OK',
    #r'SMB_PCA9548_1([ \t])+8([ \t])+0x70([ \t])+OK',
    #r'SMB_PHY_EEPROM([ \t])+28([ \t])+0x50([ \t])+OK',
    #r'SMB_SI5391B([ \t])+10([ \t])+0x74([ \t])+OK',
    #r'SMB_PCA9548_2([ \t])+11([ \t])+0x77([ \t])+OK',
    #r'SMB_CPLD([ \t])+12([ \t])+0x3E([ \t])+OK',
    #r'SMB_IOB_FPGA([ \t])+13([ \t])+0x35([ \t])+OK',
    r'SMB_DC-DC.*?OK',
    r'SMB_DC-DC_core.*?OK',
    r'SMB_LM75.*?OK',
    r'SMB_TMP422.*?OK',
    r'SMB_UCD90160A.*?OK',
    r'SMB_SI53108.*?OK',
    r'SMB_PCA9548_.*?OK',
    r'SMB_PHY_EEPROM.*?OK',
    r'SMB_SI5391B.*?OK',
    r'SMB_PCA9548.*?OK',
    r'SMB_CPLD.*?OK',
    r'SMB_IOB_FPGA.*?OK',
    r'SMB_PM40028.*?OK'
]

sdk_working_dir = '/usr/local/cls_diag/SDK'

minipack2_cel_openmbc_i2c_pattern_pim1 = [
    r'device([ \t])+bus([ \t])+address([ \t])+status',
    r'PIM1_PCA9548([ \t])+40([ \t])+0x76([ \t])+OK',
    r'PIM1_DOM_FPGA([ \t])+80([ \t])+0x60([ \t])+OK',
    r'PIM1_EEPROM([ \t])+81([ \t])+0x56([ \t])+OK',
    r'PIM1_TMP75_1([ \t])+82([ \t])+0x48([ \t])+OK',
    r'PIM1_TMP75_2([ \t])+83([ \t])+0x4b([ \t])+OK',
    r'PIM1_TMP75_3([ \t])+84([ \t])+0x4a([ \t])+OK',
    r'PIM1_HOT_SWAP([ \t])+84([ \t])+0x10([ \t])+OK',
    r'PIM1_VR([ \t])+86([ \t])+0x6B([ \t])+OK',
    r'PIM1_UCD90160A([ \t])+86([ \t])+0x34([ \t])+OK',
    r'PIM1_SI5391B([ \t])+87([ \t])+0x74([ \t])+OK',
    ]
minipack2_cel_openmbc_i2c_pattern_pim2 = [
    r'device([ \t])+bus([ \t])+address([ \t])+status',
    r'PIM2_PCA9548([ \t])+41([ \t])+0x76([ \t])+OK',
    r'PIM2_DOM_FPGA([ \t])+88([ \t])+0x60([ \t])+OK',
    r'PIM2_EEPROM([ \t])+89([ \t])+0x56([ \t])+OK',
    r'PIM2_TMP75_1([ \t])+90([ \t])+0x48([ \t])+OK',
    r'PIM2_TMP75_2([ \t])+91([ \t])+0x4b([ \t])+OK',
    r'PIM2_TMP75_3([ \t])+92([ \t])+0x4a([ \t])+OK',
    r'PIM2_HOT_SWAP([ \t])+92([ \t])+0x10([ \t])+OK',
    r'PIM2_VR([ \t])+94([ \t])+0x6B([ \t])+OK',
    r'PIM2_UCD90160A([ \t])+94([ \t])+0x34([ \t])+OK',
    r'PIM2_SI5391B([ \t])+95([ \t])+0x74([ \t])+OK',
    ]

minipack2_cel_openmbc_i2c_pattern_pim3 = [
    r'device([ \t])+bus([ \t])+address([ \t])+status',
    r'PIM3_PCA9548([ \t])+42([ \t])+0x76([ \t])+OK',
    r'PIM3_DOM_FPGA([ \t])+96([ \t])+0x60([ \t])+OK',
    r'PIM3_EEPROM([ \t])+97([ \t])+0x56([ \t])+OK',
    r'PIM3_TMP75_1([ \t])+98([ \t])+0x48([ \t])+OK',
    r'PIM3_TMP75_2([ \t])+99([ \t])+0x4B([ \t])+OK',
    r'PIM3_TMP75_3([ \t])+100([ \t])+0x4A([ \t])+OK',
    r'PIM3_HOT_SWAP([ \t])+100([ \t])+0x10([ \t])+OK',
    r'PIM3_VR([ \t])+102([ \t])+0x6B([ \t])+OK',
    r'PIM3_UCD90160A([ \t])+102([ \t])+0x34([ \t])+OK',
    r'PIM3_SI5391B([ \t])+103([ \t])+0x74([ \t])+OK',
    ]
minipack2_cel_openmbc_i2c_pattern_pim4 = {
    r'device([ \t])+bus([ \t])+address([ \t])+status',
    r'PIM4_PCA9548([ \t])+43([ \t])+0x76([ \t])+OK',
    r'PIM4_DOM_FPGA([ \t])+104([ \t])+0x60([ \t])+OK',
    r'PIM4_EEPROM([ \t])+105([ \t])+0x56([ \t])+OK',
    r'PIM4_TMP75_1([ \t])+106([ \t])+0x48([ \t])+OK',
    r'PIM4_TMP75_2([ \t])+107([ \t])+0x4B([ \t])+OK',
    r'PIM4_TMP75_3([ \t])+108([ \t])+0x4A([ \t])+OK',
    r'PIM4_HOT_SWAP([ \t])+108([ \t])+0x10([ \t])+OK',
    r'PIM4_VR([ \t])+110([ \t])+0x6B([ \t])+OK',
    r'PIM4_UCD90160A([ \t])+110([ \t])+0x34([ \t])+OK',
    r'PIM4_SI5391B([ \t])+111([ \t])+0x74([ \t])+OK',
}
minipack2_cel_openmbc_i2c_pattern_pim5 = {
    r'device([ \t])+bus([ \t])+address([ \t])+status',
    r'PIM5_PCA9548([ \t])+44([ \t])+0x76([ \t])+OK',
    r'PIM5_DOM_FPGA([ \t])+112([ \t])+0x60([ \t])+OK',
    r'PIM5_EEPROM([ \t])+113([ \t])+0x56([ \t])+OK',
    r'PIM5_TMP75_1([ \t])+114([ \t])+0x48([ \t])+OK',
    r'PIM5_TMP75_2([ \t])+115([ \t])+0x4B([ \t])+OK',
    r'PIM5_TMP75_3([ \t])+116([ \t])+0x4A([ \t])+OK',
    r'PIM5_HOT_SWAP([ \t])+116([ \t])+0x10([ \t])+OK',
    r'PIM5_VR([ \t])+118([ \t])+0x6B([ \t])+OK',
    r'PIM5_UCD90160A([ \t])+118([ \t])+0x34([ \t])+OK',
    r'PIM5_SI5391B([ \t])+119([ \t])+0x74([ \t])+OK',
}
minipack2_cel_openmbc_i2c_pattern_pim6 = {
    r'device([ \t])+bus([ \t])+address([ \t])+status',
    r'PIM6_PCA9548([ \t])+45([ \t])+0x76([ \t])+OK',
    r'PIM6_DOM_FPGA([ \t])+120([ \t])+0x60([ \t])+OK',
    r'PIM6_EEPROM([ \t])+121([ \t])+0x56([ \t])+OK',
    r'PIM6_TMP75_1([ \t])+122([ \t])+0x48([ \t])+OK',
    r'PIM6_TMP75_2([ \t])+123([ \t])+0x4B([ \t])+OK',
    r'PIM6_TMP75_3([ \t])+124([ \t])+0x4A([ \t])+OK',
    r'PIM6_HOT_SWAP([ \t])+124([ \t])+0x10([ \t])+OK',
    r'PIM6_VR([ \t])+126([ \t])+0x6B([ \t])+OK',
    r'PIM6_UCD90160A([ \t])+126([ \t])+0x34([ \t])+OK',
    r'PIM6_SI5391B([ \t])+127([ \t])+0x74([ \t])+OK',
}
minipack2_cel_openmbc_i2c_pattern_pim7 = {
    r'device([ \t])+bus([ \t])+address([ \t])+status',
    r'PIM7_PCA9548([ \t])+46([ \t])+0x76([ \t])+OK',
    r'PIM7_DOM_FPGA([ \t])+128([ \t])+0x60([ \t])+OK',
    r'PIM7_EEPROM([ \t])+129([ \t])+0x56([ \t])+OK',
    r'PIM7_TMP75_1([ \t])+130([ \t])+0x48([ \t])+OK',
    r'PIM7_TMP75_2([ \t])+131([ \t])+0x4B([ \t])+OK',
    r'PIM7_TMP75_3([ \t])+132([ \t])+0x4A([ \t])+OK',
    r'PIM7_HOT_SWAP([ \t])+132([ \t])+0x10([ \t])+OK',
    r'PIM7_VR([ \t])+134([ \t])+0x6B([ \t])+OK',
    r'PIM7_UCD90160A([ \t])+134([ \t])+0x34([ \t])+OK',
    r'PIM7_SI5391B([ \t])+135([ \t])+0x74([ \t])+OK',
}
minipack2_cel_openmbc_i2c_pattern_pim8 = {
    r'device([ \t])+bus([ \t])+address([ \t])+status',
    r'PIM8_PCA9548([ \t])+47([ \t])+0x76([ \t])+OK',
    r'PIM8_DOM_FPGA([ \t])+136([ \t])+0x60([ \t])+OK',
    r'PIM8_EEPROM([ \t])+137([ \t])+0x56([ \t])+OK',
    r'PIM8_TMP75_1([ \t])+138([ \t])+0x48([ \t])+OK',
    r'PIM8_TMP75_2([ \t])+139([ \t])+0x4B([ \t])+OK',
    r'PIM8_TMP75_3([ \t])+140([ \t])+0x4A([ \t])+OK',
    r'PIM8_HOT_SWAP([ \t])+140([ \t])+0x10([ \t])+OK',
    r'PIM8_VR([ \t])+142([ \t])+0x6B([ \t])+OK',
    r'PIM8_UCD90160A([ \t])+142([ \t])+0x34([ \t])+OK',
    r'PIM8_SI5391B([ \t])+143([ \t])+0x74([ \t])+OK',
}
minipack2_cel_openmbc_i2c_pattern_scm = [
    r'device([ \t])+bus([ \t])+address([ \t])+status',
    r'SCM_COMe_BIC([ \t])+0([ \t])+0x20([ \t])+OK',
    r'SCM_CPLD([ \t])+2([ \t])+0x35([ \t])+OK',
    r'SCM_PCA9548([ \t])+2([ \t])+0x70([ \t])+OK',
    r'SCM_HOT_SWAP([ \t])+16([ \t])+0x10([ \t])+OK',
    r'SCM_LM75_1([ \t])+17([ \t])+0x4c([ \t])+OK',
    r'SCM_LM75_2([ \t])+17([ \t])+0x4d([ \t])+OK',
    r'SCM_EEPROM([ \t])+19([ \t])+0x52([ \t])+OK',
    r'COME_PHY_EEPROM([ \t])+20([ \t])+0x50([ \t])+OK',
    r'OOB_PHY_EEPROM([ \t])+22([ \t])+0x52([ \t])+OK',
]

minipack2_cel_openmbc_i2c_dev_key_list = [
    'fcm_b',
    'fcm_t',
    'pdb_L',
    'pdn_R',
    'sim',
    'bmc',
    'smb',
    'pim1',
    'pim2',
    'pim3',
    'pim4',
    'pim5',
    'pim6',
    'pim7',
    'pim8',
    'scm',
]

minipack2_cel_openmbc_i2c_dev_key_list_pim5 = [
    'fcm_b',
    'fcm_t',
    'pdb_L',
    'pdn_R',
    'sim',
    'bmc',
    'smb',
    'pim1',
    'pim2',
    'pim6',
    'pim7',
    'pim8',
    'scm',
]

minipack2_cel_openmbc_i2c_dev_key_list_pim4 = [
    'fcm_b',
    'fcm_t',
    'pdb_L',
    'pdn_R',
    'sim',
    'bmc',
    'smb',
    'pim1',
    'pim2',
    'pim7',
    'pim8',
    'scm',
]

minipack2_cel_openmbc_i2c_dev_pattern_list = {
    'fcm_t' : minipack2_cel_openmbc_i2c_pattern_fcm_t,
    'fcm_b' : minipack2_cel_openmbc_i2c_pattern_fcm_b,
    'pdb_L' : minipack2_cel_openmbc_i2c_pattern_pdb_L,
    'pdn_R' : minipack2_cel_openmbc_i2c_pattern_pdb_R,
    'sim' : minipack2_cel_openmbc_i2c_pattern_sim,
    'bmc' : minipack2_cel_openmbc_i2c_pattern_bmc,
    'smb' : minipack2_cel_openmbc_i2c_pattern_smb,
    'pim1' : minipack2_cel_openmbc_i2c_pattern_pim1,
    'pim2' : minipack2_cel_openmbc_i2c_pattern_pim2,
    'pim3' : minipack2_cel_openmbc_i2c_pattern_pim3,
    'pim4' : minipack2_cel_openmbc_i2c_pattern_pim4,
    'pim5' : minipack2_cel_openmbc_i2c_pattern_pim5,
    'pim6' : minipack2_cel_openmbc_i2c_pattern_pim6,
    'pim7' : minipack2_cel_openmbc_i2c_pattern_pim7,
    'pim8' : minipack2_cel_openmbc_i2c_pattern_pim8,
    'scm' : minipack2_cel_openmbc_i2c_pattern_scm,
}

minipack2_cel_openmbc_i2c_dev_option_list = {
    'fcm_b' : '-s -b FCM_B',
    'fcm_t' : '-s -b FCM_T',
    'pdb_L' : '-s -b PDB_L',
    'pdn_R' : '-s -b PDB_R',
    'sim' : '-s -b SIM',
    'bmc' : '-s -b BMC',
    'smb' : '-s -b SMB',
    'pim1' : '-s -b PIM1',
    'pim2' : '-s -b PIM2',
    'pim3' : '-s -b PIM3',
    'pim4' : '-s -b PIM4',
    'pim5' : '-s -b PIM5',
    'pim6' : '-s -b PIM6',
    'pim7' : '-s -b PIM7',
    'pim8' : '-s -b PIM8',
    'scm' : '-s -b SCM',
}
##### FB_SYS_COM_TCG1-03_OpenBMC_Utility_Stability_Test #####
minipack2_cel_openbmc_util_all_version_pattern = [
    r'BMC[ \t]+Version:.*?',
    #r'^[ \t]*Fan[ \t]+Speed[ \t]+Controller[ \t]+Version:[ \t]+.*$',
    #r'^[ \t]*ROM[ \t]+Version:[ \t]+.*$'
    r'TPM[ \t]+Version:.*?',
    r'FCMCPLD[ \t]+B:.*?',
    r'FCMCPLD[ \t]+T:.*?',
    r'PWRCPLD[ \t]+L:.*?',
    r'PWRCPLD[ \t]+R:[ \t]+.*$',
    r'SCMCPLD:[ \t]+.*$',
    r'SMBCPLD:[ \t]+.*$',
    r'IOB[ \t]FPGA:[ \t]+.*$',
    r'PIM1[ \t]+DOMFPGA:[ \t]+.*$',
    r'PIM2[ \t]+DOMFPGA:[ \t]+.*$',
    r'PIM3[ \t]+DOMFPGA:[ \t]+.*$',
    r'PIM4[ \t]+DOMFPGA:[ \t]+.*$',
    r'PIM5[ \t]+DOMFPGA:[ \t]+.*$',
    r'PIM6[ \t]+DOMFPGA:[ \t]+.*$',
    r'PIM7[ \t]+DOMFPGA:[ \t]+.*$',
    r'PIM8[ \t]+DOMFPGA:[ \t]+.*$',
    r'Bridge-IC[ \t]+Version:[ \t]+.*$',
    r'Bridge-IC[ \t]+Bootloader[ \t]+Version:[ \t]+.*$',
    r'BIOS[ \t]+Version:[ \t]+.*$',
    r'CPLD[ \t]+Version:[ \t]+.*$',
    r'ME[ \t]+Version:[ \t]+.*$',
    r'PVCCIN[ \t]+VR[ \t]+Version:[ \t]+.*$',
    r'DDRAB[ \t]+VR[ \t]+Version:[ \t]+.*$',
    r'P1V05[ \t]+VR[ \t]+Version:[ \t]+.*$',
]

psu_connection_pattern = [
    r'PSU1 Present.*?OK',
    r'PSU1 ACOK.*?OK',
    r'PSU1 DCOK.*?OK',
    r'PSU2 Present.*?OK',
    r'PSU2 ACOK.*?OK',
    r'PSU2 DCOK.*?OK',
    r'PSU3 Present.*?OK',
    r'PSU3 ACOK.*?OK',
    r'PSU3 DCOK.*?OK',
    r'PSU4 Present.*?OK',
    r'PSU4 ACOK.*?OK',
    r'PSU4 DCOK.*?OK'
]

psu_connection_pattern_dc = [
    #r'PSU2 Present.*?OK',
    #r'PSU2 ACOK.*?OK',
    #r'PSU2 DCOK.*?OK',
    r'PSU3 Present.*?OK',
    r'PSU3 ACOK.*?OK',
    r'PSU3 DCOK.*?OK',
    r'PSU4 Present.*?OK',
    r'PSU4 ACOK.*?OK',
    r'PSU4 DCOK.*?OK'
]

minipack2_fwUtilPatternList = [minipack2_cel_openbmc_util_all_version_pattern]

####FB_SYS_COMM_TCG1-19_TPM_Module_Access_Stress_test####
minipack2_cel_tpm_status_pattern = [
    r'run([ \t])+systemctl([ \t])+restart([ \t])+tpm2-abrmd.service',
    r'run([ \t])+tpm2_getcap([ \t])+-c([ \t])+properties-fixed',
    r'WARN:([ \t])+More([ \t])+data([ \t])+to([ \t])+be([ \t])+queried:([ \t])+capability:([ \t])+0x6,([ \t])+property:([ \t])+0x100',
    r'tpm([ \t])+match:SLB9670',
    r'TPM([ \t])+test([ \t])+all([ \t])+Passed',
]

##### Cloudripper #####
cloudripper_cel_ipmitool_pattern = [
    r'Device ID([ \t])+:([ \t])+(\d+)',
    r'Device Revision([ \t])+:([ \t])+(\d+)',
    r'Firmware Revision([ \t])+:([ \t])+((\d+).(\d+))',
    r'IPMI Version([ \t])+:([ \t])+((\d+).(\d+))',
    r'Manufacturer ID([ \t])+:([ \t])+(\d+)',
    r'Manufacturer Name([ \t])+:([ \t])+(\w+)([ \t])+\(([\w,\d]+)\)',
    r'Product ID([ \t])+:([ \t])+(\d+)([ \t])+\(([\w,\d]+)\)',
    r'Product Name([ \t])+:([ \t])+(\w+)([ \t])+\(([\w,\d]+)\)',
    r'Device Available([ \t])+:([ \t])+yes',
    r'Provides Device SDRs([ \t])+:([ \t])+yes',
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
]

cloudripper_cel_openmbc_i2c_pattern = [
    r'device([ \t])+bus([ \t])+address([ \t])+status',
    r'SCM_COMe_BIC([ \t])+(\d+)([ \t])+0x20([ \t])+OK',
    r'SCM_CPLD([ \t])+(\d+)([ \t])+0x3e([ \t])+OK',
    r'SMB_LM75B_3([ \t])+(\d+)([ \t])+0x4A([ \t])+OK',
    r'SMB_PCA9555([ \t])+(\d+)([ \t])+0x27([ \t])+OK',
    r'SMB_DOM_FPGA_2([ \t])+(\d+)([ \t])+0x60([ \t])+OK',
    r'SMB_EEPROM([ \t])+(\d+)([ \t])+0x51([ \t])+OK',
    r'SMB_PCA9534([ \t])+(\d+)([ \t])+0x21([ \t])+OK',
    r'SMB_LEDs([ \t])+(\d+)([ \t])+0x14([ \t])+OK',
    r'RunBMC_TPM_MODULE([ \t])+(\d+)([ \t])+0x2E([ \t])+OK',
    r'RunBMC_EEPROM([ \t])+(\d+)([ \t])+0x51([ \t])+OK',
    r'RunBMC_LM75([ \t])+(\d+)([ \t])+0x4A([ \t])+OK',
    r'SMB_SI5391B([ \t])+(\d+)([ \t])+0x74([ \t])+OK',
    r'RunBMC_FPGA([ \t])+(\d+)([ \t])+0x0D([ \t])+OK',
    r'SMB_CPLD([ \t])+(\d+)([ \t])+0x3E([ \t])+OK',
    r'SMB_DOM_FPGA_1([ \t])+(\d+)([ \t])+0x60([ \t])+OK',
    r'SMB_I2C_IR35215_C0([ \t])+(\d+)([ \t])+0x2D([ \t])+OK',
    r'SMB_PMBUS_IR35215_C0([ \t])+(\d+)([ \t])+0x4D([ \t])+OK',
    r'SMB_XDPE132G5_I2_C1([ \t])+(\d+)([ \t])+0x10([ \t])+OK',
    r'SMB_XDPE132G5_PMBUS_C1([ \t])+(\d+)([ \t])+0x40([ \t])+OK',
    r'SMB_POWER1220_C2([ \t])+(\d+)([ \t])+0x3A([ \t])+OK',
    r'SMB_XDPE12284_LEFT_C3([ \t])+(\d+)([ \t])+0x68([ \t])+OK',
    r'SMB_PXE1211CPM_C4([ \t])+(\d+)([ \t])+0x0E([ \t])+OK',
    r'SMB_IR35215_I2C_C5([ \t])+(\d+)([ \t])+0x27([ \t])+OK',
    r'SMB_IR35215_PMBUS_C5([ \t])+(\d+)([ \t])+0x47([ \t])+OK',
    r'SMB_XDPE12284_RIGHT_C6([ \t])+(\d+)([ \t])+0x60([ \t])+OK',
    r'SCM_Hot_Swap([ \t])+(\d+)([ \t])+0x10([ \t])+OK',
    r'SCM_LM75_1([ \t])+(\d+)([ \t])+0x4C([ \t])+OK',
    r'SCM_LM75_2([ \t])+(\d+)([ \t])+0x4D([ \t])+OK',
    r'SCM_EEPROM([ \t])+(\d+)([ \t])+0x52([ \t])+OK',
    r'SCM_EEPROM_BCM54616S([ \t])+(\d+)([ \t])+0x50([ \t])+OK',
    r'SCM_SI53108([ \t])+(\d+)([ \t])+0x6C([ \t])+OK',
    r'SMB_LM75B_1_C0([ \t])+(\d+)([ \t])+0x48([ \t])+OK',
    r'SMB_LM75B_2_C1([ \t])+(\d+)([ \t])+0x49([ \t])+OK',
    r'SMB_LM75B_4_C2([ \t])+(\d+)([ \t])+0x4B([ \t])+OK',
    r'SMB_TMP421_1_C3([ \t])+(\d+)([ \t])+0x4C([ \t])+OK',
    r'SMB_TMP421_2_C4([ \t])+(\d+)([ \t])+0x4D([ \t])+OK',
    r'SMB_LM75B_5_C5([ \t])+(\d+)([ \t])+0x4E([ \t])+OK',
    r'SMB_GB_C6([ \t])+(\d+)([ \t])+0x2A([ \t])+OK',
    r'SMB_LM75B_6_C7([ \t])+(\d+)([ \t])+0x4F([ \t])+OK',
    r'PDBT_PSU1_EEPROM_C0([ \t])+(\d+)([ \t])+0x50([ \t])+OK',
    r'PDBT_PSU1_CTRL_C0([ \t])+(\d+)([ \t])+0x58([ \t])+OK',
    r'PDBB_PSU2_EEPROM_C1([ \t])+(\d+)([ \t])+0x50([ \t])+OK',
    r'PDBB_PSU2_CTRL_C1([ \t])+(\d+)([ \t])+0x58([ \t])+OK',
    r'SMB_BCM54616_BMC_C2([ \t])+(\d+)([ \t])+0x50([ \t])+OK',
    r'SMB_BCM54616_MDI_C3([ \t])+(\d+)([ \t])+0x50([ \t])+OK',
    r'SMB_PWR_CPLD([ \t])+(\d+)([ \t])+0x3E([ \t])+OK',
    r'FCM_24C64_EEPROM_C1([ \t])+(\d+)([ \t])+0x51([ \t])+OK',
    r'FCM_LM75_1_C2([ \t])+(\d+)([ \t])+0x48([ \t])+OK',
    r'FCM_LM75_2_C2([ \t])+(\d+)([ \t])+0x49([ \t])+OK',
    r'FCM_Hot_Swap([ \t])+(\d+)([ \t])+0x10([ \t])+OK',
    r'FCM_Fantray_4_C4([ \t])+(\d+)([ \t])+0x52([ \t])+OK',
    r'FCM_Fantray_3_C5([ \t])+(\d+)([ \t])+0x52([ \t])+OK',
    r'FCM_Fantray_2_C6([ \t])+(\d+)([ \t])+0x52([ \t])+OK',
    r'FCM_Fantray_1_C7([ \t])+(\d+)([ \t])+0x52([ \t])+OK',
    r'FCM_CPLD([ \t])+(\d+)([ \t])+0x3E([ \t])+OK',
]

cloudripper_cel_openmbc_i2c_pattern_list = {
    'show' : cloudripper_cel_openmbc_i2c_pattern,
}

################## wedge400 project #####################
devicename = os.environ.get("deviceName", "")
import logging
logging.info("devicename:{}".format(devicename))
if "wedge400_" in devicename.lower():
    ### TCG2-03 ###
    ssddev_num = '1'

    #### TC_09 ####
    sensor_u_pattern = [
        r'(get|check)_sensor_util_status.*?PASS'
    ]

    #### TC_15 ####
    w400_port_cmd = 'ps cd'
    w400_set_vlan_cmd = 'snake_script_loopback_DD_400G_56_200G.soc'
    w400_DD_traffic_cmd = "tx 10000 PBM=cd0 vlan=40 L=1280"
    w400_56_traffic_cmd = "tx 10000 PBM=cd16 vlan=216 L=1280"
    w400_DD_stop_cmd = 'pv set cd15 1888'
    w400_56_stop_cmd = 'pv set cd47 1666'
    w400_DD_counters = 'show c CDMIB_RPKT.cd0-cd15; show c CDMIB_TPKT.cd0-cd15; show c CDMIB_RFCS'
    w400_56_counters = 'show c CDMIB_RPKT.cd16-cd47; show c CDMIB_TPKT.cd16-cd47; show c CDMIB_RFCS'
    w400_rpkt = "CDMIB_RPKT\.\w+.*?([\d,]+)\s+.(\S+)"
    w400_tpkt = "CDMIB_TPKT\.\w+.*?([\d,]+)\s+.(\S+)"

    #### TC_16 ####
    w400_Reinit_DD_stop_cmd = 'pvlan set cd15 1666'
    w400_Reinit_56_stop_cmd = 'pvlan set cd47 1888'
    w400_traffic_counters = 'show c CDMIB_TPKT.cd;show c CDMIB_RPKT.cd;show c CDMIB_RFCS'

    #### TC_17 ####
    w400_traffic_cmd = 'snake_script_loopback_16x400G_32x200G_PAM4.soc'
    w400_snake_DD_stop_cmd = 'pvlan set cd15 1888'
    w400_snake_56_stop_cmd = 'pvlan set cd47 1889'
    w400_snake_traffic_counters = 'show c CDMIB_RPKT.cd0-cd47; show c CDMIB_TPKT.cd0-cd47; show c CDMIB_RFCS'

    #### TC_13 ####
    i2c_config_file_list = ['i2c_devices.cfg', 'devices.cfg']
    DOWNLOADABLE_DIR_WEDGE400 = '/home/automation/Auto_Test/automation/FB-Wedge400/autotest/downloadable'
    cel_openmbc_i2c_pattern_list_w400_dc = {
        'show':
            [
                r'(device)([ \t])+bus([ \t])+address([ \t])+status',
                r'(SCM_COMe_BIC)([ \t])+(\d+)([ \t])+0x20([ \t])+OK',
                r'(SCM_CPLD)([ \t])+(\d+)([ \t])+0x3e([ \t])+OK',
                r'(SCM_Hot_Swap)([ \t])+(\d+)([ \t])+0x10([ \t])+OK',
                r'(SCM_LM75_1)([ \t])+(\d+)([ \t])+0x4c([ \t])+OK',
                r'(SCM_LM75_2)([ \t])+(\d+)([ \t])+0x4d([ \t])+OK',
                r'(SCM_EEPROM)([ \t])+(\d+)([ \t])+0x52([ \t])+OK',
                r'(SCM_54616_EEPROM)([ \t])+(\d+)([ \t])+0x50([ \t])+OK',
                r'(SCM_PCIE_CLOCK_BUF)([ \t])+(\d+)([ \t])+0x6C([ \t])+OK',
                r'(BSM_EEPROM)([ \t])+(\d+)([ \t])+0x56([ \t])+OK',
                r'(PSB_Power_Sequence)([ \t])+(\d+)([ \t])+0x3a([ \t])+OK',
                r'(SMB_Power_DC-DC_core)([ \t])+(\d+)([ \t])+0x60([ \t])+OK',
                # r'SMB_Power_DC-DC_core_pmbus([ \t])+(\d+)([ \t])+0x40([ \t])+OK',
                r'(SMB_Power_Left_base)([ \t])+(\d+)([ \t])+0x35([ \t])+OK',
                r'(SMB_Power_Left_pmbus)([ \t])+(\d+)([ \t])+0x4d([ \t])+OK',
                r'(SMB_Power_Right_base)([ \t])+(\d+)([ \t])+0x2f([ \t])+OK',
                r'(SMB_Power_Right_pmbus)([ \t])+(\d+)([ \t])+0x47([ \t])+OK',
                # r'SMB_PXE1211([ \t])+(\d+)([ \t])+0x0E([ \t])+OK',
                r'(SMB_Temp_LM75B_1)([ \t])+(\d+)([ \t])+0x48([ \t])+OK',
                # r'SMB_Temp_LM75B_2([ \t])+(\d+)([ \t])+0x49([ \t])+OK',
                # r'SMB_Temp_LM75B_3([ \t])+(\d+)([ \t])+0x4A([ \t])+OK',
                r'(SMB_Temp_LM75B_4)([ \t])+(\d+)([ \t])+0x4B([ \t])+OK',
                # r'Switch_Gibraltar([ \t])+(\d+)([ \t])+0x2A([ \t])+OK',
                r'(SMB_OCP_IO_expander)([ \t])+(\d+)([ \t])+0x27([ \t])+OK',
                r'(SMB_DOM_FPGA_2)([ \t])+(\d+)([ \t])+0x60([ \t])+OK',
                r'(SMB_EEPROM)([ \t])+(\d+)([ \t])+0x51([ \t])+OK',
                r'(RACKMON_EEPROM)([ \t])+(\d+)([ \t])+0x50([ \t])+OK',
                r'(RACKMON_LEDs)([ \t])+(\d+)([ \t])+0x20([ \t])+OK',
                r'(SMB_Board_ID)([ \t])+(\d+)([ \t])+0x21([ \t])+OK',
                r'(BSM_TPM)([ \t])+(\d+)([ \t])+0x2e([ \t])+OK',
                r'(SMB_Temp_TPM421_2)([ \t])+(\d+)([ \t])+0x4d([ \t])+OK',
                r'(SMB_Temp_TPM421_1)([ \t])+(\d+)([ \t])+0x4d([ \t])+OK',
                r'(PSB_PWR_CPLD)([ \t])+(\d+)([ \t])+0x3e([ \t])+OK',
                r'(SMB_TH3_Clock)([ \t])+(\d+)([ \t])+0x74([ \t])+OK',
                r'(SMB_OOB_SWITCH_EEPROM)([ \t])+(\d+)([ \t])+0x50([ \t])+OK',
                r'(SMB_CPLD)([ \t])+(\d+)([ \t])+0x3E([ \t])+OK',
                r'(SMB_DOM_FPGA_1)([ \t])+(\d+)([ \t])+0x60([ \t])+OK',
                r'(PDB_PSU_2_EEPROM)([ \t])+(\d+)([ \t])+0x50([ \t])+OK',
                # r'PDB_PEM_1_Hot_Swap([ \t])+(\d+)([ \t])+0x58([ \t])+OK',
                # r'PDB_PEM_1_Thermal([ \t])+(\d+)([ \t])+0x18([ \t])+OK',
                # r'PDB_PEM_2_EEPROM([ \t])+(\d+)([ \t])+0x50([ \t])+OK',
                # r'PDB_PEM_2_Hot_Swap([ \t])+(\d+)([ \t])+0x58([ \t])+OK',
                # r'PDB_PEM_2_Thermal([ \t])+(\d+)([ \t])+0x18([ \t])+OK',
                # r'PSU_1_EEPROM([ \t])+(\d+)([ \t])+0x50([ \t])+OK',
                # r'PSU_1([ \t])+(\d+)([ \t])+0x58([ \t])+OK',
                # r'PSU_2_EEPROM([ \t])+(\d+)([ \t])+0x50([ \t])+OK',
                r'(PDB_PSU_2)([ \t])+(\d+)([ \t])+0x58([ \t])+OK',
                r'(SMB_Temp_TPM421_TH3_2)([ \t])+(\d+)([ \t])+0x4d([ \t])+OK',
                r'(SMB_Temp_TPM421_TH3_1)([ \t])+(\d+)([ \t])+0x4d([ \t])+OK',
                # r'Power_Hbm([ \t])+(\d+)([ \t])+0x0E([ \t])+OK',
                r'(FCM_CPLD)([ \t])+(\d+)([ \t])+0x3e([ \t])+OK',
                r'(FCM_EEPROM)([ \t])+(\d+)([ \t])+0x51([ \t])+OK',
                r'(FCM_LM75_1)([ \t])+(\d+)([ \t])+0x48([ \t])+OK',
                r'(FCM_LM75_2)([ \t])+(\d+)([ \t])+0x49([ \t])+OK',
                r'(FCM_Hot_Swap)([ \t])+(\d+)([ \t])+0x10([ \t])+OK',
                r'(FCM_Fan_tray_4)([ \t])+(\d+)([ \t])+0x52([ \t])+OK',
                r'(FCM_Fan_tray_3)([ \t])+(\d+)([ \t])+0x52([ \t])+OK',
                r'(FCM_Fan_tray_2)([ \t])+(\d+)([ \t])+0x52([ \t])+OK',
                r'(FCM_Fan_tray_1)([ \t])+(\d+)([ \t])+0x52([ \t])+OK',
            ]
    }
    cel_openmbc_i2c_pattern_list_w400_rsp_ac = {
        'show':
            [
                r'(device)([ \t])+bus([ \t])+address([ \t])+status',
                r'(SCM_COMe_BIC)([ \t])+(\d+)([ \t])+0x20([ \t])+OK',
                r'(SCM_CPLD)([ \t])+(\d+)([ \t])+0x3e([ \t])+OK',
                r'(SCM_Hot_Swap)([ \t])+(\d+)([ \t])+0x10([ \t])+OK',
                r'(SCM_LM75_1)([ \t])+(\d+)([ \t])+0x4c([ \t])+OK',
                r'(SCM_LM75_2)([ \t])+(\d+)([ \t])+0x4d([ \t])+OK',
                r'(SCM_EEPROM)([ \t])+(\d+)([ \t])+0x52([ \t])+OK',
                r'(SCM_54616_EEPROM)([ \t])+(\d+)([ \t])+0x50([ \t])+OK',
                r'(SCM_PCIE_CLOCK_BUF)([ \t])+(\d+)([ \t])+0x6C([ \t])+OK',
                r'(BSM_EEPROM)([ \t])+(\d+)([ \t])+0x56([ \t])+OK',
                r'(PSB_Power_Sequence)([ \t])+(\d+)([ \t])+0x3a([ \t])+OK',
                r'(SMB_Power_DC-DC_core)([ \t])+(\d+)([ \t])+0x60([ \t])+OK',
                r'(SMB_Power_Left_base)([ \t])+(\d+)([ \t])+0x35([ \t])+OK',
                r'(SMB_Power_Left_pmbus)([ \t])+(\d+)([ \t])+0x4d([ \t])+OK',
                r'(SMB_Power_Right_base)([ \t])+(\d+)([ \t])+0x2f([ \t])+OK',
                r'(SMB_Power_Right_pmbus)([ \t])+(\d+)([ \t])+0x47([ \t])+OK',
                r'(SMB_Temp_LM75B_1)([ \t])+(\d+)([ \t])+0x48([ \t])+OK',
                r'(SMB_Temp_LM75B_4)([ \t])+(\d+)([ \t])+0x4B([ \t])+OK',
                r'(SMB_OCP_IO_expander)([ \t])+(\d+)([ \t])+0x27([ \t])+OK',
                r'(SMB_DOM_FPGA_2)([ \t])+(\d+)([ \t])+0x60([ \t])+OK',
                r'(SMB_EEPROM)([ \t])+(\d+)([ \t])+0x51([ \t])+OK',
                r'(RACKMON_EEPROM)([ \t])+(\d+)([ \t])+0x50([ \t])+OK',
                r'(RACKMON_LEDs)([ \t])+(\d+)([ \t])+0x20([ \t])+OK',
                r'(SMB_Board_ID)([ \t])+(\d+)([ \t])+0x21([ \t])+OK',
                r'(BSM_TPM)([ \t])+(\d+)([ \t])+0x2e([ \t])+OK',
                r'(SMB_Temp_TPM421_2)([ \t])+(\d+)([ \t])+0x4d([ \t])+OK',
                r'(SMB_Temp_TPM421_1)([ \t])+(\d+)([ \t])+0x4d([ \t])+OK',
                r'(PSB_PWR_CPLD)([ \t])+(\d+)([ \t])+0x3e([ \t])+OK',
                r'(SMB_TH3_Clock)([ \t])+(\d+)([ \t])+0x74([ \t])+OK',
                r'(SMB_OOB_SWITCH_EEPROM)([ \t])+(\d+)([ \t])+0x50([ \t])+OK',
                r'(SMB_CPLD)([ \t])+(\d+)([ \t])+0x3E([ \t])+OK',
                r'(SMB_DOM_FPGA_1)([ \t])+(\d+)([ \t])+0x60([ \t])+OK',
                r'(PDB_PSU_1_EEPROM)([ \t])+(\d+)([ \t])+0x50([ \t])+OK',
                r'(PDB_PSU_1)([ \t])+(\d+)([ \t])+0x58([ \t])+OK',
                r'(PDB_PSU_2_EEPROM)([ \t])+(\d+)([ \t])+0x50([ \t])+OK',
                r'(PDB_PSU_2)([ \t])+(\d+)([ \t])+0x58([ \t])+OK',
                r'(SMB_Temp_TPM421_TH3_2)([ \t])+(\d+)([ \t])+0x4d([ \t])+OK',
                r'(SMB_Temp_TPM421_TH3_1)([ \t])+(\d+)([ \t])+0x4d([ \t])+OK',
                r'(FCM_CPLD)([ \t])+(\d+)([ \t])+0x3e([ \t])+OK',
                r'(FCM_EEPROM)([ \t])+(\d+)([ \t])+0x51([ \t])+OK',
                r'(FCM_LM75_1)([ \t])+(\d+)([ \t])+0x48([ \t])+OK',
                r'(FCM_LM75_2)([ \t])+(\d+)([ \t])+0x49([ \t])+OK',
                r'(FCM_Hot_Swap)([ \t])+(\d+)([ \t])+0x10([ \t])+OK',
                r'(FCM_Fan_tray_4)([ \t])+(\d+)([ \t])+0x52([ \t])+OK',
                r'(FCM_Fan_tray_3)([ \t])+(\d+)([ \t])+0x52([ \t])+OK',
                r'(FCM_Fan_tray_2)([ \t])+(\d+)([ \t])+0x52([ \t])+OK',
                r'(FCM_Fan_tray_1)([ \t])+(\d+)([ \t])+0x52([ \t])+OK',
            ]
    }
    cel_openmbc_i2c_pattern_list_w400_rsp_pem = {
        'show':
            [
                r'(device)([ \t])+bus([ \t])+address([ \t])+status',
                r'(SCM_COMe_BIC)([ \t])+(\d+)([ \t])+0x20([ \t])+OK',
                r'(SCM_CPLD)([ \t])+(\d+)([ \t])+0x3e([ \t])+OK',
                r'(SCM_Hot_Swap)([ \t])+(\d+)([ \t])+0x10([ \t])+OK',
                r'(SCM_LM75_1)([ \t])+(\d+)([ \t])+0x4c([ \t])+OK',
                r'(SCM_LM75_2)([ \t])+(\d+)([ \t])+0x4d([ \t])+OK',
                r'(SCM_EEPROM)([ \t])+(\d+)([ \t])+0x52([ \t])+OK',
                r'(SCM_54616_EEPROM)([ \t])+(\d+)([ \t])+0x50([ \t])+OK',
                r'(SCM_PCIE_CLOCK_BUF)([ \t])+(\d+)([ \t])+0x6C([ \t])+OK',
                r'(BSM_EEPROM)([ \t])+(\d+)([ \t])+0x56([ \t])+OK',
                r'(PSB_Power_Sequence)([ \t])+(\d+)([ \t])+0x3a([ \t])+OK',
                r'(SMB_Power_DC-DC_core)([ \t])+(\d+)([ \t])+0x60([ \t])+OK',
                r'(SMB_Power_Left_base)([ \t])+(\d+)([ \t])+0x35([ \t])+OK',
                r'(SMB_Power_Left_pmbus)([ \t])+(\d+)([ \t])+0x4d([ \t])+OK',
                r'(SMB_Power_Right_base)([ \t])+(\d+)([ \t])+0x2f([ \t])+OK',
                r'(SMB_Power_Right_pmbus)([ \t])+(\d+)([ \t])+0x47([ \t])+OK',
                r'(SMB_Temp_LM75B_1)([ \t])+(\d+)([ \t])+0x48([ \t])+OK',
                r'(SMB_Temp_LM75B_4)([ \t])+(\d+)([ \t])+0x4B([ \t])+OK',
                r'(SMB_OCP_IO_expander)([ \t])+(\d+)([ \t])+0x27([ \t])+OK',
                r'(SMB_DOM_FPGA_2)([ \t])+(\d+)([ \t])+0x60([ \t])+OK',
                r'(SMB_EEPROM)([ \t])+(\d+)([ \t])+0x51([ \t])+OK',
                r'(RACKMON_EEPROM)([ \t])+(\d+)([ \t])+0x50([ \t])+OK',
                r'(RACKMON_LEDs)([ \t])+(\d+)([ \t])+0x20([ \t])+OK',
                r'(SMB_Board_ID)([ \t])+(\d+)([ \t])+0x21([ \t])+OK',
                r'(BSM_TPM)([ \t])+(\d+)([ \t])+0x2e([ \t])+OK',
                r'(SMB_Temp_TPM421_2)([ \t])+(\d+)([ \t])+0x4d([ \t])+OK',
                r'(SMB_Temp_TPM421_1)([ \t])+(\d+)([ \t])+0x4d([ \t])+OK',
                r'(PSB_PWR_CPLD)([ \t])+(\d+)([ \t])+0x3e([ \t])+OK',
                r'(SMB_TH3_Clock)([ \t])+(\d+)([ \t])+0x74([ \t])+OK',
                r'(SMB_OOB_SWITCH_EEPROM)([ \t])+(\d+)([ \t])+0x50([ \t])+OK',
                r'(SMB_CPLD)([ \t])+(\d+)([ \t])+0x3E([ \t])+OK',
                r'(SMB_DOM_FPGA_1)([ \t])+(\d+)([ \t])+0x60([ \t])+OK',
                r'(PDB_PEM_2_EEPROM)([ \t])+(\d+)([ \t])+0x50([ \t])+OK',
                #r'PDB_PSU_1([ \t])+(\d+)([ \t])+0x58([ \t])+OK',
                r'(PDB_PEM_2_Hot_Swap)([ \t])+(\d+)([ \t])+0x58([ \t])+OK',
                r'(PDB_PEM_2_Thermal)([ \t])+(\d+)([ \t])+0x18([ \t])+OK',
                r'(SMB_Temp_TPM421_TH3_2)([ \t])+(\d+)([ \t])+0x4d([ \t])+OK',
                r'(SMB_Temp_TPM421_TH3_1)([ \t])+(\d+)([ \t])+0x4d([ \t])+OK',
                r'(FCM_CPLD)([ \t])+(\d+)([ \t])+0x3e([ \t])+OK',
                r'(FCM_EEPROM)([ \t])+(\d+)([ \t])+0x51([ \t])+OK',
                r'(FCM_LM75_1)([ \t])+(\d+)([ \t])+0x48([ \t])+OK',
                r'(FCM_LM75_2)([ \t])+(\d+)([ \t])+0x49([ \t])+OK',
                r'(FCM_Hot_Swap)([ \t])+(\d+)([ \t])+0x10([ \t])+OK',
                r'(FCM_Fan_tray_4)([ \t])+(\d+)([ \t])+0x52([ \t])+OK',
                r'(FCM_Fan_tray_3)([ \t])+(\d+)([ \t])+0x52([ \t])+OK',
                r'(FCM_Fan_tray_2)([ \t])+(\d+)([ \t])+0x52([ \t])+OK',
                r'(FCM_Fan_tray_1)([ \t])+(\d+)([ \t])+0x52([ \t])+OK',
            ]
    }
    cel_openmbc_i2c_pattern_list_w400_mp = {
        'show' :
        [
            r'(device)([ \t])+bus([ \t])+address([ \t])+status',
            r'(SCM_COMe_BIC)([ \t])+(\d+)([ \t])+0x20([ \t])+OK',
            r'(SCM_CPLD)([ \t])+(\d+)([ \t])+0x3e([ \t])+OK',
            r'(SCM_Hot_Swap)([ \t])+(\d+)([ \t])+0x10([ \t])+OK',
            r'(SCM_LM75_1)([ \t])+(\d+)([ \t])+0x4c([ \t])+OK',
            r'(SCM_LM75_2)([ \t])+(\d+)([ \t])+0x4d([ \t])+OK',
            r'(SCM_EEPROM)([ \t])+(\d+)([ \t])+0x52([ \t])+OK',
            r'(SCM_54616_EEPROM)([ \t])+(\d+)([ \t])+0x50([ \t])+OK',
            r'(SCM_PCIE_CLOCK_BUF)([ \t])+(\d+)([ \t])+0x6C([ \t])+OK',
            r'(BSM_EEPROM)([ \t])+(\d+)([ \t])+0x56([ \t])+OK',
            r'(SMB_Power_Sequence)([ \t])+(\d+)([ \t])+0x3a([ \t])+OK',
            r'(SMB_Power_DC-DC_core)([ \t])+(\d+)([ \t])+0x60([ \t])+OK',
            #r'SMB_Power_DC-DC_core_pmbus([ \t])+(\d+)([ \t])+0x40([ \t])+OK',
            r'(SMB_Power_Left_base)([ \t])+(\d+)([ \t])+0x35([ \t])+OK',
            r'(SMB_Power_Left_pmbus)([ \t])+(\d+)([ \t])+0x4d([ \t])+OK',
            r'(SMB_Power_Right_base)([ \t])+(\d+)([ \t])+0x2f([ \t])+OK',
            r'(SMB_Power_Right_pmbus)([ \t])+(\d+)([ \t])+0x47([ \t])+OK',
            #r'SMB_PXE1211([ \t])+(\d+)([ \t])+0x0E([ \t])+OK',
            r'(SMB_Temp_LM75B_1)([ \t])+(\d+)([ \t])+0x48([ \t])+OK',
            r'(SMB_Temp_LM75B_2)([ \t])+(\d+)([ \t])+0x49([ \t])+OK',
            r'(SMB_Temp_LM75B_3)([ \t])+(\d+)([ \t])+0x4A([ \t])+OK',
            r'(SMB_Temp_LM75B_4)([ \t])+(\d+)([ \t])+0x4B([ \t])+OK',
            r'(SMB_Temp_TPM421_1)([ \t])+(\d+)([ \t])+0x4C([ \t])+OK',
            r'(SMB_Temp_TPM421_2)([ \t])+(\d+)([ \t])+0x4E([ \t])+OK',
            r'(SMB_Temp_TPM422_TH3)([ \t])+(\d+)([ \t])+0x4F([ \t])+OK',
            r'(SMB_OCP_IO_expander)([ \t])+(\d+)([ \t])+0x27([ \t])+OK',
            r'(SMB_DOM_FPGA_2)([ \t])+(\d+)([ \t])+0x60([ \t])+OK',
            r'(SMB_EEPROM)([ \t])+(\d+)([ \t])+0x51([ \t])+OK',
            r'(SMB_LEDs)([ \t])+(\d+)([ \t])+0x20([ \t])+OK',
            r'(SMB_Board_ID)([ \t])+(\d+)([ \t])+0x21([ \t])+OK',
            r'(SMB_TPM)([ \t])+(\d+)([ \t])+0x2e([ \t])+OK',
            r'(SMB_TH3)([ \t])+(\d+)([ \t])+0x54([ \t])+OK',
            r'(SMB_PWR_CPLD)([ \t])+(\d+)([ \t])+0x3e([ \t])+OK',
            r'(SMB_TH3_Clock)([ \t])+(\d+)([ \t])+0x74([ \t])+OK',
            r'(SMB_CPLD)([ \t])+(\d+)([ \t])+0x3E([ \t])+OK',
            r'(SMB_DOM_FPGA_1)([ \t])+(\d+)([ \t])+0x60([ \t])+OK',
            r'(PDB_PEM_2_EEPROM)([ \t])+(\d+)([ \t])+0x50([ \t])+OK',
            r'(PDB_PEM_2_Hot_Swap)([ \t])+(\d+)([ \t])+0x58([ \t])+OK',
            r'(PDB_PEM_2_Thermal)([ \t])+(\d+)([ \t])+0x18([ \t])+OK',
            #r'PDB_PEM_2_EEPROM([ \t])+(\d+)([ \t])+0x50([ \t])+OK',
            #r'PDB_PEM_2_Hot_Swap([ \t])+(\d+)([ \t])+0x58([ \t])+OK',
            #r'PDB_PEM_2_Thermal([ \t])+(\d+)([ \t])+0x18([ \t])+OK',
            #r'PSU_1_EEPROM([ \t])+(\d+)([ \t])+0x50([ \t])+OK',
            #r'PSU_1([ \t])+(\d+)([ \t])+0x58([ \t])+OK',
            #r'PSU_2_EEPROM([ \t])+(\d+)([ \t])+0x50([ \t])+OK',
            #r'PDB_PSU_2([ \t])+(\d+)([ \t])+0x58([ \t])+OK',
            #r'SMB_Temp_TPM421_TH3_2([ \t])+(\d+)([ \t])+0x4d([ \t])+OK',
            #r'SMB_Temp_TPM421_TH3_1([ \t])+(\d+)([ \t])+0x4d([ \t])+OK',
            #r'Power_Hbm([ \t])+(\d+)([ \t])+0x0E([ \t])+OK',
            r'FCM_CPLD([ \t])+(\d+)([ \t])+0x3e([ \t])+OK',
            r'FCM_EEPROM([ \t])+(\d+)([ \t])+0x51([ \t])+OK',
            r'FCM_LM75_1([ \t])+(\d+)([ \t])+0x48([ \t])+OK',
            r'FCM_LM75_2([ \t])+(\d+)([ \t])+0x49([ \t])+OK',
            r'FCM_Hot_Swap([ \t])+(\d+)([ \t])+0x10([ \t])+OK',
            r'FCM_Fan_tray_4([ \t])+(\d+)([ \t])+0x52([ \t])+OK',
            r'FCM_Fan_tray_3([ \t])+(\d+)([ \t])+0x52([ \t])+OK',
            r'FCM_Fan_tray_2([ \t])+(\d+)([ \t])+0x52([ \t])+OK',
            r'FCM_Fan_tray_1([ \t])+(\d+)([ \t])+0x52([ \t])+OK',
        ]
    }



pcie_pattern=['errors: 0','\[PASS\]']
i2c_pattern=['errors: 0','\[PASS\]']
cpu_pattern=['\[PASS\]']
tpm_vendor=['TPM Vendor String: SLB9670']
minerva_tpm=['PM Manufacturer: IFX','TPM Vendor String: SLB9670']
sdk_working_dir = '/usr/local/cls_diag/SDK'
SDK_PATH = sdk_working_dir
SDK_SCRIPT = 'auto_load_user.py'
CENTOS_SDK_prompt='[root@localhost SDK]#'
BCM_VERSION_MiniPack3 = "Release: "
SDK_SHELL = 'auto_load_user.sh'
load_128x400 =  "./{} -m 128x400".format(SDK_SHELL)
load_128x200 =  "./{} -m 128x200".format(SDK_SHELL)
load_128x100 =  "./{} -m 128x100".format(SDK_SHELL)
load_64x400_64x200 =  "./{} -m 64x400_64x200".format(SDK_SHELL)
load_64x800 =  "./{} -m 64x800".format(SDK_SHELL)
load_64x200_64x400 =  "./{} -m 64x200_64x400".format(SDK_SHELL)
BCM_prompt = 'BCM.0>'
exit_BCM_Prompt='exit'
port_enable_status='passed'
port_disable_status='failed'
portdump_status_cmd = "portdump status all"
oob_test = ['OOB ping test passed','PASS']


minipack3_cel_nvme_smart_pattern = [
    r'Smart([ \t])+Log([ \t])+for([ \t])+NVME([ \t])+device:nvme((\d+)[ \t])+namespace-id:([\w,\d]+)',
    r'critical_warning([ \t])+:([ \t])+0',
    r'temperature([ \t])+:([ \t])+(\d+)([ \t])+C',
    r'available_spare([ \t])+:([ \t])+(\d+)\%',
    r'available_spare_threshold([ \t])+:([ \t])+(\d+)\%',
    r'percentage_used([ \t])+:([ \t])+(\d+)\%',
    r'endurance group critical warning summary:([ \t])+0',
    r'data_units_read([ \t])+:([ \t])+(\d+)',
    r'data_units_written([ \t])+:([ \t])+(\d+)',
    r'host_read_commands([ \t])+:([ \t])+(\d+)',
    r'host_write_commands([ \t])+:([ \t])+(\d+)',
    r'controller_busy_time([ \t])+:([ \t])+(\d+)',
    r'power_cycles([ \t])+:([ \t])+(\d+)',
    r'power_on_hours([ \t])+:([ \t])+(\d+)',
    r'unsafe_shutdowns([ \t])+:([ \t])+(\d+)',
    r'media_errors([ \t])+:([ \t])+0',
    r'num_err_log_entries([ \t])+:([ \t])+0',
    r'Warning([ \t])+Temperature([ \t])+Time([ \t])+:([ \t])+(\d+)',
    r'Critical([ \t])+Composite([ \t])+Temperature([ \t])+Time([ \t])+:([ \t])+(\d+)',
    r'Temperature([ \t])+Sensor([ \t])+(\d+)([ \t])+:([ \t])+(\d+)([ \t])+C',
    r'Temperature([ \t])+Sensor([ \t])+(\d+)([ \t])+:([ \t])+(\d+)([ \t])+C',
    r'Thermal([ \t])+Management([ \t])+T(\d+)([ \t])+Trans([ \t])+Count([ \t])+:([ \t])+(\d+)',
    r'Thermal([ \t])+Management([ \t])+T(\d+)([ \t])+Total([ \t])+Time([ \t])+:([ \t])+(\d+)',
]


workspace_sys = '/mnt/data/'
OPENBMC_MODE = 'openbmc'

#####################################################META SDK VARIABLES##############################################################################################
port_enable_cmd = "port cd en=1"
port_disable_cmd = "port cd en=0"
port_ce_enable_cmd = "port ce en=1"
port_ce_disable_cmd = "port ce en=0"
portdump_pass_pattern = ["(Port|P)\d+", "passed"]
PRBS_port_pattern = "(\d+) : PRBS (\S+)"
PRBS_ok = "OK!"
BER_port_pattern = "(\d+\[\d+\]) : ([e\-.0-9]+)"
port_BER_tolerance = 1e-6
port_exclude = ["50", "152"]
set_snake_vlan_400G_cmd = "linespeed64x200_32x400_2TG.soc"
set_snake_vlan_200G_cmd = "linespeed200G.soc"
set_snake_vlan_100G_cmd = "linespeed100G.soc"
SOC_400G_file_list = [set_snake_vlan_400G_cmd]
SOC_400G_file_path = "/home/automation/Auto_Test/automation/FB-Minipack2/autotest/SDK"
pvlan_show_cmd = "pvlan show"
vlan_show_cmd = "vlan show"
show_c_cmd = "show c"
clear_c_cmd = "clear c\n" + show_c_cmd
portdump_counters_cmd = "portdump counters all"
portdump_counters_32_cmd = "portdump counters 1-16,81-96"
portdump_counters_64_cmd = "portdump counters 17-80"
portdump_pass_pattern = ["(Port|P)\d+", "passed"]
PRBS_port_pattern = "(\d+) : PRBS (\S+)"
PRBS_ok = "OK!"
BER_port_pattern = "(\d+\[\d+\]) : ([e\-.0-9]+)"
port_BER_tolerance = 1e-6


########################## MINIPACK3 #############################
if "minipack3" in devicename.lower():
    CENTOS_SDK_prompt='[root@localhost SDK]#'
    BCM_VERSION_MiniPack3 = "Release: "
    SDK_SHELL = 'auto_load_user.sh'
    load_128x400 =  "./{} -m 128x400".format(SDK_SHELL)
    load_128x200 =  "./{} -m 128x200".format(SDK_SHELL)
    load_128x100 =  "./{} -m 128x100".format(SDK_SHELL)
    load_64x400_64x200 =  "./{} -m 64x400_64x200".format(SDK_SHELL)
    load_64x800 =  "./{} -m 64x800".format(SDK_SHELL)
    load_256x100 =  "./{} -m 256x100".format(SDK_SHELL)
    load_64x200_64x400 =  "./{} -m 64x200_64x400".format(SDK_SHELL)
    portdump_status_pass_regex= 'port status check test PASSED'
    PCIe_version_regex = 'PCIe FW loader version: '
    port_detail_passed_pattern = ["(P\d+)", "(UP)", "(FULL)","passed"]
    port_detail_failed_pattern = ["(P\d+)", "(DOWN)", "(N/A)","(N/A)", "failed"]
    portdump_pass_pattern_regex = "((Port|P)\d+)([\s+\S+]+)passed"
    portdump_failed_pattern = ["(Port|P)\d+", "failed"]
    portdump_failed_pattern_regex = "((Port|P)\d+)([\s+\S+]+)failed"
    port_d3c_enable_cmd = 'port d3c en=1'
    port_d3c_disable_cmd = 'port d3c en=0'
    bertest_cmd='bertest'
    clear_c_command = 'clear c'
    traffic_test_cmd='traffictest all'
    traffic_test_end_regex = 'str=tx([\s+\S+\n]+)\BCM\.0>'
    sdk_prompt='root@localhost SDK'
    cls_shell_d3c = './cls_shell ps d3c'
    cls_shell_d3c_check=['d3c\d+','up', '800G', 'FD','No', 'Forward', 'TX', 'RX', 'Backplane', '9412']
    cls_shell_exit = './cls_shell exit'
    lane_serdes_version_cmd = "phy diag 1-344 dsc"
    serdes_api_version_regex = 'SERDES API Version   = '
    ucode_version_regex = 'Common Ucode Version = '
    port_d3c_lb_cmd = 'port d3c lb='
    phy_diag_d3c_dsc_64 = 'phy diag d3c dsc (x=0~63)'
    phy_diag_d3c_dsc_128 = 'phy diag d3c dsc (x=0~127)'
    cls_shell_exit_output_regex = 'Disconnecting IRQ 0 blocked by kernel ISR'
    cls_shell_d3c_output_regex='RS544-2xN[\s+\n+\S+]+root@localhost SDK'
    bertest_threshold_value='1e-9'
    bertest_regex='\d+\[\d+\]\s+:\s+(([\d+.]+)(e[+-]\d+))'
    portdump_counters_all_cmd = 'portdump counters all'
    BCM_prompt = 'BCM.0>'
    exit_BCM_Prompt='exit'
    port_enable_status='passed'
    port_disable_status='failed'

######################################################
elif "minerva_janga" in devicename.lower():
    SDK_SHELL= "python3 -i diagtest_sdk.py"
    mgmt_port_regex='E\d+\/0'
    load_18x1x800= "{} --port_mode 18x1x800G".format(SDK_SHELL)
    load_18x1x400= "{} --port_mode 18x1x400G".format(SDK_SHELL)
    load_18x2x200= "{} --port_mode 18x2x200G".format(SDK_SHELL)
    load_18x2x100= "{} --port_mode 18x2x100G".format(SDK_SHELL)
    load_18x2x400= "{} --port_mode 18x2x400G".format(SDK_SHELL)
    load_18x4x100= "{} --port_mode 18x4x100G".format(SDK_SHELL)
    load_18x4x200= "{} --port_mode 18x4x200G".format(SDK_SHELL)
    port_enable_tag= "--enable_lt"
    CENTOS_SDK_prompt='[root@localhost SDK]#'
    BCM_SDK_version_cmd='sdk.do_show_version_test()'
    PCIe_version_cmd='sdk.dapi.pciephy_fw_show(unit=None)'
    PCIe_version_check='PCIe FW loader version: '
    show_version_test_passed_regex='do_show_version_test- TEST PASS'
    get_sdk_version = '([a-z0-9\.]+)\s+\S+\s+([a-z0-9\.-]+)'
    portdump_status_cmd = 'sdk.dapi.dump_ports()'
    port_name_regex='\S+\d+\/\d+'
    BCM_prompt='>>>'
    port_disable_cmd='sdk.dapi.port_enable(unit=None, port=None, enable=False)'
    port_enable_cmd='sdk.dapi.port_enable(unit=None, port=None, enable=True)'
    PSBR_passed_pattern= 'do_port_serdes_prbs_ber_test- TEST PASS'
    bertest_cmd=' --run_case 4 --prbs_running_sec 180'
    L2_cpu_traffic_cmd=' --run_case 7 --duration_sec 300'
    L2_cpu_traffic_passed_pattern= 'do_cpu_full_l2snake_test- TEST PASS'
    bertest_regex='\|\s*\d+\s*\|\s*\d+\s*\|\s*\d+\s*\|\s*PRBSlocked\s*\|\s*([\d+\.]+)\s*\|'
    bertest_threshold_value='1e-8'
    lane_serdes_version_cmd='sdk.dapi.phy_dsc(unit=0, port={})'
    ucode_version_regex= 'Common Ucode Version = D002_0B'
    serdes_api_version_regex= 'SERDES API Version   = A00406'
    manufacturing_test_command='--duration_sec 10 --max_temp 100 --min_temp 25 --prbs_running_sec 10 --auto_run_all'
    manufacturing_test_pattern_lst=['do_dram_bist_test- TEST PASS','do_sdk_reload_test- TEST PASS', 'do_sensor_test- TEST PASS', 'do_port_serdes_prbs_ber_test- TEST PASS', 'do_port_linkup_validation_test- TEST PASS', 'do_port_loopback_test- TEST PASS', 'do_cpu_full_l2snake_test- TEST PASS', 'do_show_version_test- TEST PASS']
    exit_BCM_Prompt='exit()'
    port_enable_status='up'
    port_disable_status='!ena'
    show_temperature_cmd='sdk.dapi.show_temperature(unit=None, main=False, max=False,is_print=True)'
    snake_config_cmd='sdk.dapi.snake_config(unit=0, vehicle=True, ports=None,loopback=True, force_fabric=True, clear=True, use_sat=False)'
    snake_test_start_cmd='sdk.dapi.snake_start_traffic(unit=0, inject=500,psrc=1,data=0x0000002222220000001111118100006408004500,length=360,random=True,use_sat=True,speed=400)'
    snake_test_stop_cmd='sdk.dapi.snake_stop_traffic(unit=0, psrc=1, use_sat=True)'
    port_detail_passed_pattern = ["(eth\d+)", "up", "No", "RS-544-2xN", "NONE"]
    port_loopback_test_pass_regex ='do_port_loopback_test- TEST PASS'
    port_loopback_test_tag= '--run_case 6  --duration_sec 300'
    L2_traffic_test_item_check_regex='(\|\s+[\d,]+\s+){14}'
    l2_traffic_total_tx_rx_packets_regex='-check_mib_counters-:\s+\S+\s+(\d+),\s+rx_gold_bytes:\s+(\d+),\s+tx_gold_frames:\s+(\d+),\s+tx_gold_bytes:\s+(\d+)'

elif "minerva_th5" in devicename.lower():
    CENTOS_SDK_prompt='[root@localhost SDK]#'
    BCM_VERSION_MiniPack3 = "Release: "
    SDK_SHELL = 'auto_load_user.sh'
    load_128x400 =  "./{} -m 128x400".format(SDK_SHELL)
    load_128x200 =  "./{} -m 128x200".format(SDK_SHELL)
    load_128x100 =  "./{} -m 128x100".format(SDK_SHELL)
    load_64x400_64x200 =  "./{} -m 64x400_64x200".format(SDK_SHELL)
    load_64x800 =  "./{} -m 64x800".format(SDK_SHELL)
    load_64x200_64x400 =  "./{} -m 64x200_64x400".format(SDK_SHELL)
    PCIe_version_regex = 'PCIe FW loader version: '
    port_detail_passed_pattern = ["(P\d+)", "(UP)", "(FULL)","passed"]
    port_detail_failed_pattern = ["(P\d+)", "(DOWN)", "(N/A)","(N/A)", "failed"]
    portdump_pass_pattern_regex = "((Port|P)\d+)([\s+\S+]+)passed"
    portdump_failed_pattern = ["(Port|P)\d+", "failed"]
    portdump_failed_pattern_regex = "((Port|P)\d+)([\s+\S+]+)failed"
    port_d3c_enable_cmd = 'port d3c en=1'
    port_d3c_disable_cmd = 'port d3c en=0'
    bertest_cmd='bertest'
    clear_c_command = 'clear c'
    traffic_test_cmd='snaketest'
    traffic_test_end_regex = 'port counters check test([\s+\S+\n]+)BCM\.0>'
    sdk_prompt='root@localhost SDK'
    cls_shell_d3c = './cls_shell ps d3c'
    cls_shell_d3c_check=['d3c\d+','up', '800G', 'FD','No', 'Forward', 'TX', 'RX', 'Backplane', '9412']
    cls_shell_exit = './cls_shell exit'
    lane_serdes_version_cmd = " dsh -c 'phydiag 1-342 dsc'"
    serdes_api_version_regex = 'SERDES API Version   = A00405'
    ucode_version_regex = 'Common Ucode Version = D002_0A'
    port_d3c_lb_cmd = 'port d3c lb='
    phy_diag_d3c_dsc_64 = 'phy diag d3c dsc (x=0~63)'
    phy_diag_d3c_dsc_128 = 'phy diag d3c dsc (x=0~127)'
    cls_shell_exit_output_regex = 'Disconnecting IRQ 0 blocked by kernel ISR'
    cls_shell_d3c_output_regex='RS544-2xN[\s+\n+\S+]+root@localhost SDK'
    bertest_threshold_value='1e-9'
    bertest_regex='\d+\[\d+\]\s+:\s+(([\d+.]+)(e[+-]\d+))'
    portdump_counters_all_cmd = 'portdump counters all'
    BCM_prompt = 'BCM.0>'
    exit_BCM_Prompt='exit'
    port_enable_status='passed'
    port_disable_status='failed'
    get_hmon_temperature_cmd= 'hmon temp'
    temperature_test_cmd='snake800G.soc'
    traffic_temp_traffic_cmd_1='tx 10000 pbm=ce0 vlan=998 l=295 SM=0x1 DM=0x2 '
    traffic_temp_traffic_cmd_2=' tx 80000 pbm=d3c16 vlan=199 length=295 SM=0x1 DM=0x2 data=0x000000000002000000000001810000c717fe49d06ee7bb6421afc028af8a7abd8a5a198232538823cbabd57da2f5e13e39c71fa249d7d6e65a112793cbabd57d9d7d6e65a145a313e382df27b277a3f907b9b37a3f907b9a145b3e11f9f85d8de7df1c12793cbabd57da2f593f88fd9d2e9c71fa249d7d6e65a145a313e382df27b277a3f907b9b3e11f9f85d8de7d886239a84a1942126200bc442e6983c6b3f6219a6425adc1202bca4aa5063c0b837af7d84819a2965be0ba4fefe7642617c1c9dff1e4439ad86183a8a3ed79bc849c582e2ebbd7f38253079067eb3935183f2c3fb557923f4babac7dbc4794696a328858c706804fad13741efbef830c3fc5178ecfccae6cb2c7f5d4729eb44225b5357dcd5ac2545bbd30e69c91b916db96573b6bcfba34'
    show_c_rate_cmd='show c rate'



