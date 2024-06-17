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
# It's better not to call functions in variable files(e.g. BSP_DRIVER = SwImage.getSwImage("BSP_DRIVER")).
# Any error during the calling will make all the tests fail. We can use it in functions of lib/keywords files
# We have encountered this type of issue many many times in facebook projects.

import os
from collections import OrderedDict
import DeviceMgr
from Const import BOOT_MODE_UBOOT, BOOT_MODE_DIAGOS, BOOT_MODE_ONIE
from KapokConst import STOP_AUTOBOOT_PROMPT, STOP_AUTOBOOT_KEY
from KapokCommonLib import *
from SwImage import SwImage

device = DeviceMgr.getDevice()
if "fenghuangv2" in device.name:
    get_sys_cpld_version_cmd = "i2cget -f -y 8 0x60 0x00"
    get_fan_cpld_version_cmd = "i2cget -f -y 23 0x66 0x00"
    vmetool = "vmetool_arm "
else:
    get_sys_cpld_version_cmd = "i2cget -f -y 15 0x60 0x00"
    get_fan_cpld_version_cmd = "i2cget -f -y 10 0x66 0x00"
    vmetool = "./vmetool_arm "
pc_info = DeviceMgr.getServerInfo('PC')
dev_info = DeviceMgr.getDevice()
prbs_rx_31_25g_43200_cmd = get_data_from_yaml('prbs_rx_31_25g_43200_cmd')
prbs_rx_31_10g_43200_cmd = get_data_from_yaml('prbs_rx_31_10g_43200_cmd')
prbs_rx_pattern = '\|[ \t]+32[ \t]+:[ \t]+3.*\d+\.\d+e\-\d+[\s\S]+IVM:0>'
prbs_rx_pattern_port128 = '\|[ \t]+128[ \t]+:[ \t]+0.*\d+\.\d+e\-\d+[\s\S]+IVM:0>'
stress_BER_port_pattern = "(\d+\.\d+e\-\d+)"
stress_port_BER_tolerance= 1e-6
get_versions_cmd = "get_versions"
diagos_mode = BOOT_MODE_DIAGOS
uboot_mode = BOOT_MODE_UBOOT
tftp_server_ipv4 = pc_info.managementIP
tftp_client_ipv4 = dev_info.managementIP
uboot_prompt = dev_info.promptUboot
tools_script_stress_path = "/root/tools/stress_test"
vmetool_path = "/root/vmetool"
ifconfig_a_cmd = "ifconfig -a"
fail_dict = { "fail":"fail",
              "ERROR":"ERROR",
              "Failure": "Failure",
              "cannot read file":"cannot read file",
              "command not found":"command not found",
              "No such file": "No such file",
              "not found": "not found",
              "Unknown command":"Unknown command",
              "No space left on device": "No space left on device",
              "Command exited with non-zero status": "Command exited with non-zero status"
              }
reboot_cmd='reboot\r\n'
cat_ddr_log='cat /root/tools/stress_test/DDR_test.log\r\n'
cat_ddr_log_regexp = '.*Status:.*-.*'
cat_ddr_log_pattern = {".*Status:.*PASS":".*Status:.*PASS"}
diag_tools_path = "/root/diag"
diag_ld_lib_path = "/root/diag/output"
diag_export_env = "export LD_LIBRARY_PATH=" + diag_ld_lib_path + " && export CEL_DIAG_PATH=" + diag_tools_path + " && "
i2c_bus_scan_stress_pass_pattern = "I2C.*test.*:.*Passed"
ssd_stress_patterns = r"(?m)^[ \t]*Run[ \t]*status[ \t]*group[ \t]*"
diagnose_test_all_fail_pattern = r"(?mi)^[ \t]*(?P<number>\w+\-\w+\-\w+).*\|[ \t]*(?:(?!Passed).)*$"
uboot_tftpboot_patterns = [
    r"(?m)^TFTP from server (?P<uboot_tftp_server_ip>[\w\.]+); our IP address is (?P<uboot_tftp_our_ip>[\w\.]+)",
    r"(?m)^Filename '(?P<uboot_tftp_filename>[\w\-\.]+)'",
    r"(?m)^Load address: (?P<uboot_tftp_load_addr>\w+)",
    r"(?m)^[ \t]+(?P<uboot_tftp_speed>[\d\.]+.*\/s)$",
    r"(?m)^done$",
    r"(?m)^Bytes transferred = (?P<uboot_tftp_size_bytes>\d+)",
]
run_sfp_cmd = './cel-sfp-test --all'
D_1_cmd = "./cel-sfp-test -w -t profile -D 1"
D_1_cmd_pattern = {"SFP test : Passed":"SFP test : Passed"}
for i in range(1,33):
    patternname = "port "+str(i)
    regexp=".*?"+str(i)+" .*port.*"+str(i)+".*400K"
    D_1_cmd_pattern.update({patternname: regexp})
D_2_cmd = "./cel-sfp-test -w -t profile -D 2"
D_2_cmd_pattern = {"SFP test : Passed":"SFP test : Passed"}
for i in range(1,33):
    patternname = "port "+str(i)
    regexp=".*?"+str(i)+" .*port.*"+str(i)+".*1M"
    D_2_cmd_pattern.update({patternname: regexp})
soft_reset_cmd = 'echo 1 > /sys/bus/i2c/devices/8-0060/warm_reset'

sfp_stress_test_cmd_ist = ['./cel-sfp-test --test -t single-1 -d 32 -C 1000',
                               './cel-sfp-test --test -t single-2 -d 32 -C 1000',
                               './cel-sfp-test --test -t single-8 -d 32 -C 1000',
                               './cel-sfp-test --test -t single-16 -d 32 -C 1000']
sfp_multi_threads_test_cmd_list = ['./cel-sfp-test --test -t multi-128 -C 1000']
sfp_burst_mode_test_cmd_list = ['./cel-sfp-test --test -t single-128 -d 32 -C 1000']
sfp_stress_test_patterns_dict = {'SFP test': 'SFP test \: Passed'}
change_profile_cmd1 = './cel-sfp-test -w -t profile -D 1'
change_profile_cmd2 = './cel-sfp-test -w -t profile -D 2'
SDK = SwImage.getSwImage("SDK")
sdkname_new = SDK.newImage
SDK_PATH_New = 'sdk/{}'.format(sdkname_new)
exit_cmd = "exit"
prbs_en_cmd= 'diagtest serdes prbs mode-en 1-{} 1'
prbs_set_cmd='diagtest serdes prbs set 1-{} 1 prbs31 4590000000 86400000'
prbs_sync_cmd='diagtest serdes prbs sync 1-{}'
prbs_get_cmd='diagtest serdes prbs get 1-{}'
prbs_clear_cmd='diagtest serdes prbs clear 1-{}'
prbs_mode_en_cmd='diagtest serdes prbs mode-en 1-{} 0'
#### tianhe_STRESS_TC_20_DIAG_PCIE_Test_With_PowerCycle ####
scratchTool = '/sys/devices/xilinx/pps-i2c/scratch'
PCIeTool = './cel-pci-test --all'
LSPCI_TOOL = 'lspci'
I2C_TOOL = './cel-i2c-test --all'
SSD_TOOL = './cel-storage-test --all'
SYS_TOOL = './cel-system-test --all'
TEMP_TOOL = './cel-temp-test --all'
DCDC_TOOL = './cel-dcdc-test --all'
DIAG_ALL_TOOL = './cel-all-test --all'
DDR_SSD_TOOL_LST = ['stress_test.zip']
STRESS_PATH = '/root/tools'
DDR_TOOL = 'ddr_test_tianhe.sh'
DDR_LOG = 'DDR_test.log'
SSD_CMD = 'ssd_test.sh'
SSD_PATH = '/root/tools/stress_test/'
ssdPatternLst = [
    r'Run status group 0 \(all jobs\):',
    r'Disk stats \(read/write\):',
    r'sda: ios=\d+/\d+, merge=\d+/\d+, ticks=\d+/\d+, in_queue=\d+, util=.*'
]
I2C_PATTERN = 'I2C test : Passed'
SFP_PATTERN = 'SFP test : Passed'
FW_PATH = '/root/fw/'
COMe_ASC10_0 = 'asc_fwupd_arm -w --bus 11 --addr 0x60 -f tianhe_asc0_v01.00.09h.hex --force'
COMe_ASC10_1 = 'asc_fwupd_arm -w --bus 11 --addr 0x61 -f tianhe_asc1_v01.00.09h.hex --force'
ASC10_1_CMD = 'asc_fwupd_arm -w --bus 32 --addr 0x60 -f Phoenix_ASC0.hex --force'
ASC10_2_CMD = 'asc_fwupd_arm -w --bus 32 --addr 0x61 -f Phoenix_ASC1.hex --force'
ASC10_3_CMD = 'asc_fwupd_arm -w --bus 32 --addr 0x62 -f Phoenix_ASC2_for_1pps_3EC1.hex --force'
ASC_FW_LST = [COMe_ASC10_0, COMe_ASC10_1, ASC10_1_CMD, ASC10_2_CMD, ASC10_3_CMD]
ASC_PATTERN = '+   PASS   +'
ASC10_0_VER = 'asc_fwupd_arm -r --bus 32 --addr 0x60'
ASC10_1_VER = 'asc_fwupd_arm -r --bus 32 --addr 0x61'
ASC10_2_VER = 'asc_fwupd_arm -r --bus 32 --addr 0x62'
ASC10_3_VER = 'asc_fwupd_arm -r --bus 11 --addr 0x60'
ASC10_4_VER = 'asc_fwupd_arm -r --bus 11 --addr 0x61'
ASC10_VER_LST = [ASC10_0_VER, ASC10_1_VER, ASC10_2_VER, ASC10_3_VER, ASC10_4_VER]
#### tianhe_STRESS_BSP_TC_01_CPLD_FPGA_Update_Stress_Test ####
COMe_CPLD_CMD = 'vmetool_arm -c tianhe_cpucpld-bp_v41.00.20230817.vme'
SYS_CPLD_CMD = 'vmetool_arm -s fhv2_sys_cpld_v34.1_1218.vme'
LED_CPLD_CMD = 'vmetool_arm -l fenghuang_v2_mainboard_cpld2_v0p6_cpld3_v05.vme'
FAN_PKILL = 'pkill cel-fan-test'
FAN_CPLD_CMD = 'vmetool_arm -f cs8260_CPLD_FAN_impl1_V03.vme'
PPS_FPGA_CMD = 'flashcp -v fpgaTop_ps1p1a_20230323.1826.bin /dev/mtd5'
CPLD_FPGA_LST = [COMe_CPLD_CMD, SYS_CPLD_CMD, LED_CPLD_CMD, FAN_CPLD_CMD, PPS_FPGA_CMD]
UBOOT_ROV_CMD = 'fw_setenv -f rov_volt_bits'
CLEAR_COUNTER_CMD1 = 'ifcs clear counters devport'
CLEAR_COUNTER_CMD2 = 'ifcs clear counters hardware'
CONSOLE_CMD1 = 'console'
CONSOLE_CMD2 = 'from aux_port_cel import *'
CONSOLE_CMD3 = 'aux_traffic_test()'
CONSOLE_LST = [CONSOLE_CMD1, CONSOLE_CMD2, CONSOLE_CMD3]
CLEAR_CMD_LST = [CLEAR_COUNTER_CMD1, CLEAR_COUNTER_CMD2]
SHOW_COUNTER_CMD = 'ifcs show counters devport'
XFI_TOOL1 = 'ifconfig xfi0'
XFI_TOOL2 = 'ethtool -S xfi0'
SDK_INIT_TOOL = 'python diagtest_sdk.py --case l2snake --port_mode 1x400 --stress_cycles'
SDK_INIT_OPTION = '--duration_seconds  120'
DIAG_SNAKE_TOOL = 'diagtest snake config -p 1-32 -lb NONE -v'
SHOW_PORT_TOOL = 'ifcs show devport'
CLEAR_COUNTER_LST = [CLEAR_COUNTER_CMD1, CLEAR_COUNTER_CMD2, DIAG_SNAKE_TOOL]
SNAKE_TRAFFIC_TOOL = 'diagtest snake start_traffic -n 500 -s 1518'
SHOW_RATE = 'ifcs show rate devport filter nz'
STOP_TRAFFIC_TOOL = 'diagtest snake stop_traffic'
SNAKE_GEN_TOOL = 'diagtest snake gen_report'
TRAFFIC_LST = [SNAKE_TRAFFIC_TOOL, SHOW_RATE, STOP_TRAFFIC_TOOL, SNAKE_GEN_TOOL]
PORT_DISABLE_TOOL = 'port disable all'
PORT_ENABLE_TOOL = 'port enable all'
SHELL_SLEEP_TOOL = 'shell sleep'
SLEEP10_OPTION = '10'
SLEEP120_OPTION = '120'
Sleep120_CMD = SHELL_SLEEP_TOOL + ' ' + SLEEP120_OPTION
TRAFFIC_LST2 = [SNAKE_TRAFFIC_TOOL, Sleep120_CMD, STOP_TRAFFIC_TOOL, SNAKE_GEN_TOOL]
IFCS_SHOW_TOOL = 'ifcs show counters devport filter nz'
SNAKE_UNCONFIG = 'diagtest snake unconfig'
RTC_TOOL = 'cel-rtc-test -r'
RTC_PATTERN = 'Rtc read : Passed'
TEMP_DIAG_TOOL = 'cel-temp-test --all'
DCDC_DIAG_TOOL = 'cel-dcdc-test --all'
PCI_DIAG_TOOL = 'cel-pci-test --all'
STORAGE_DIAG_TOOL = 'cel-storage-test --all'
I2c_DIAG_TOOL = 'cel-i2c-test --all'
SYSTEM_DIAG_TOOL = 'cel-system-test --all'
DIAG_TOOL_LST = [TEMP_DIAG_TOOL, DCDC_DIAG_TOOL, PCI_DIAG_TOOL, STORAGE_DIAG_TOOL, I2c_DIAG_TOOL, SYSTEM_DIAG_TOOL]
TEMP_DIAG_PATTERN = 'Temp test : Passed'
DCDC_DIAG_PATTERN = 'DCDC test : Passed'
PCI_DIAG_PATTERN = 'PCIe test : Passed'
STORAGE_DIAG_PATTERN = 'Storage test : Passed'
I2C_DIAG_PATTERN = 'I2C test : Passed'
SYS_DIAG_PATTERN = 'Sys test : Passed'
DIAG_PATTERN_LST = [TEMP_DIAG_PATTERN, DCDC_DIAG_PATTERN, PCI_DIAG_PATTERN, STORAGE_DIAG_PATTERN, I2C_DIAG_PATTERN, SYS_DIAG_PATTERN]
FW_SETENV_TOOL = 'fw_setenv -f rov_volt_bits'
SMARTCTL_TOOL = 'smartctl -a /dev/sda1'
SSD_SPEED_PATTERN = '6.0'

