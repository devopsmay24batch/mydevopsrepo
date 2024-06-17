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
from SwImage import SwImage
from sdk.AliSdkVariable import (sdk_path, BCM_promptstr, BCM_USER, SDK_SCRIPT,
 port_up_status, ps_cd_cmd, port_pattern)

devicename = os.environ.get("deviceName", "").lower()
logging.info("devicename:{}".format(devicename))

# SwImage shared objects
BASE_CPLD = SwImage.getSwImage("BASE_CPLD")
COME_CPLD = SwImage.getSwImage("COME_CPLD")
FAN_CPLD = SwImage.getSwImage("FAN_CPLD")
SWITCH_CPLD = SwImage.getSwImage("SWITCH_CPLD")
BASE_CPLD_REFRESH = SwImage.getSwImage("BASE_CPLD_REFRESH")
CPU_CPLD_REFRESH = SwImage.getSwImage("CPU_CPLD_REFRESH")
FAN_CPLD_REFRESH = SwImage.getSwImage("FAN_CPLD_REFRESH")
DIAG = SwImage.getSwImage("DIAG")
BMC = SwImage.getSwImage("BMC")
FPGA = SwImage.getSwImage("FPGA")
BIOS = SwImage.getSwImage("BIOS")
AFU_TOOL = SwImage.getSwImage("AFU_TOOL")
if "migaloo" in devicename:
    POWER_IMAGE_LOADLINE = SwImage.getSwImage("POWER_IMAGE_LOADLINE")
    POWER_IMAGE_NO_LOADLINE = SwImage.getSwImage("POWER_IMAGE_NO_LOADLINE")
    loadline_path = POWER_IMAGE_LOADLINE.localImageDir
    loadline_file = POWER_IMAGE_LOADLINE.newImage
    no_loadline_path = POWER_IMAGE_NO_LOADLINE.localImageDir
    no_loadline_file = POWER_IMAGE_NO_LOADLINE.newImage
# End of SwImage shared objects

cpld_baseboard_new_image = BASE_CPLD.newImage
cpld_come_new_image = COME_CPLD.newImage
cpld_fan_new_image = FAN_CPLD.newImage
cpld_switch_new_image = SWITCH_CPLD.newImage
cpld_base_refresh_image = BASE_CPLD_REFRESH.newImage
cpld_cpu_refresh_image = CPU_CPLD_REFRESH.newImage
cpld_fan_refresh_image = FAN_CPLD_REFRESH.newImage

cpld_baseboard_new_version = BASE_CPLD.newVersion
cpld_come_new_version = COME_CPLD.newVersion
cpld_fan_new_version = FAN_CPLD.newVersion
cpld_switch_new_version = SWITCH_CPLD.newVersion

installed_software_versions_patterns = [
    r"(?mi)^[ \t]*diag[ \t]+version[ \t]*:[ \t]*(?P<diag_version>[\.\w]+)[ \t]*$",
    r"(?mi)^[ \t]*SONiC[ \t]+SW[ \t]+Version[ \t]*:[ \t]*(?P<sonic_version>[\.\w\-]+)[ \t]*$",
    r"(?mi)^[ \t]*ONIE[ \t]+Version[ \t]*:[ \t]*(?P<onie_version>[\w\.]+)[ \t]*$",
    r"(?mi)^[ \t]*KERNEL[ \t]+Version[ \t]*:[ \t]*(?P<kernel_version>[\.\w\-]+)[ \t]*$",
    r"(?mi)^[ \t]*sdk[ \t]+diag[ \t]*:[ \t]*(?P<sdk_version>[\.\w]+)[ \t]*$",
    r"(?mi)^[ \t]*switch[ \t]+chip[ \t]+version[ \t]*:[ \t]*(?P<switch_chip_version>\w+)[ \t]*,?[ \t]*$",
    r"(?mi)^[ \t]*bmc[ \t]+slave[ \t]+version[ \t]*:[ \t]*(?P<bmc_slave_version>[\.\w]+)[ \t]*$",
    r"(?mi)^[ \t]*bios[ \t]+version[ \t]*:[ \t]*(?P<bios_version>[\.\w]+)[ \t]*$",
    r"(?mi)^[ \t]*fpga[ \t]+version[ \t]*:[ \t]*(?P<fpga_version>\w+)[ \t]*$",
    r"(?mi)^[ \t]*baseboard[ \t]+CPLD[ \t]+Version[ \t]*:[ \t]+(?P<baseboard_cpld_version>\w+)[ \t]*$",
    r"(?mi)^[ \t]*come[ \t]+CPLD[ \t]+version[ \t]*:[ \t]*(?P<come_version>\w+)[ \t]*$",
    r"(?mi)^[ \t]*FAN[ \t]+CPLD[ \t]+version[ \t]*:[ \t]*(?P<fan_cpld>\w+)[ \t]*$",
    r"(?mi)^[ \t]*SW[ \t]+CPLD1[ \t]+version[ \t]*:[ \t]*(?P<sw_cpld1_version>\w+)[ \t]*$",
    r"(?mi)^[ \t]*SW[ \t]+CPLD2[ \t]+version[ \t]*:[ \t]*(?P<sw_cpld2_version>\w+)[ \t]*$",
    r"(?mi)^[ \t]*top[ \t]+line[ \t]+cpld1[ \t]+version[ \t]*:[ \t]*(?P<top_line_cpld1_version>\w+)[ \t]*$",
    r"(?mi)^[ \t]*top[ \t]+line[ \t]+cpld2[ \t]+version[ \t]*:[ \t]*(?P<top_line_cpld2_version>\w+)[ \t]*$",
    r"(?mi)^[ \t]*bot[ \t]+line[ \t]+cpld1[ \t]+version[ \t]*:[ \t]*(?P<bot_line_cpld1_version>\w+)[ \t]*$",
    r"(?mi)^[ \t]*bot[ \t]+line[ \t]+cpld2[ \t]+version[ \t]*:[ \t]*(?P<bot_line_cpld2_version>\w+)[ \t]*$",
    r"(?mi)^[ \t]*i210[ \t]+fw[ \t]+version[ \t]*:[ \t]*(?P<i210_fw_version>[\.\w]+)[ \t]*$",
]

bmc_new_image = BMC.newImage
bmc_host_image_dir = BMC.hostImageDir
bmc_local_image_path = BMC.localImageDir
bmc_flash_pattern = r'Current Boot Code Source:\s*(\w+) Flash'
bmc_update_pass_msg = r'Verifying kb:.*100%'
no_such_file_msg = r"No such file or directory"
cpu_test_path = '/etc'
master_dev = 'mtd5'
slave_dev = 'mtd11'
bmc_new_version = BMC.newVersion
bmc_version_dict = {SwImage.BMC_VER: bmc_new_version}

interface_list = ['eth0', 'eth0.4088', 'lo', 'usb0']
default_interface = 'eth0'
mac_addr_pattern = r'HWaddr (\S+)'

openbmc_version_regex = r'OpenBMC Release .+-v?(.*)'

fpga_old_fw_name = FPGA.oldImage
fpga_new_fw_name = FPGA.newImage
fpga_fw_path = FPGA.hostImageDir
fpga_old_fw_version = FPGA.oldVersion
fpga_new_fw_version = FPGA.newVersion
fpga_fw_save_to = FPGA.localImageDir

fpga_prog_patterns = [
    r"(?mi)^[ \t]*FPGA[ \t]+PROGRAM.*version[ \t]+(?P<fpga_programming_version>[\w\.]+)[ \t]*$",
    r"(?mi)^[ \t]*Programing[ \t]+(?P<fpga_finish>finish)[ \t]*$",
]

fpga_old_version_patterns = r"(?mi)^[ \t]*fpga[ \t]+version[ \t]*:[ \t]*(?P<fpga_version>" + fpga_old_fw_version + r")[ \t]*$"
fpga_new_version_patterns = r"(?mi)^[ \t]*fpga[ \t]+version[ \t]*:[ \t]*(?P<fpga_version>" + fpga_new_fw_version + r")[ \t]*$"
bios_local_image_path = BIOS.localImageDir
bios_flash_pattern = r'COMe CPU boots from BIOS\s*(\w+) flash'
bios_update_pass_msg = r'Verifying flash.*VERIFIED'
bios_version_pattern = r'D0000\.(.+)'
bios_boot_version_pattern = r'D0000\.(.+)\s+\((Primary|Backup)'

diag_cpu_path = '/usr/local/migaloo/CPU_Diag/'
cpld_update_timeout = 90*60
cpld_version_cmd = './cel-version-test -S'
fpga_version_cmd = './cel-version-test -S'
version_test_pattern = r'(.+): V?(.+)'
cpld_local_image_path = BASE_CPLD.localImageDir

BASE_CPLD_KEY = "BaseBoard CPLD Version"
COME_CPLD_KEY = "COMe CPLD Version"
FAN_CPLD_KEY = "FAN CPLD Version"
SWITCH_CPLD1_KEY = "SW CPLD1 Version"
SWITCH_CPLD2_KEY = "SW CPLD2 Version"
TOPLINE_CPLD1_KEY = "Top Line CPLD1 Version"
TOPLINE_CPLD2_KEY = "Top Line CPLD2 Version"
BOTLINE_CPLD1_KEY = "BOT Line CPLD1 Version"
BOTLINE_CPLD2_KEY = "BOT Line CPLD2 Version"
FPGA_KEY = "FPGA Version"

cpld_update_pass_msg = r'\b0\b'
cpld_type_image_dict = {
    "BASE_CPLD": "BASE_CPLD",
    "CPU_CPLD": "COME_CPLD",
    "FAN_CPLD": "FAN_CPLD",
    "SW_CPLD1": "SWITCH_CPLD",
    "SW_CPLD2": "SWITCH_CPLD",
    "TOP_LC_CPLD": "SWITCH_CPLD",
    "BOT_LC_CPLD": "SWITCH_CPLD",
}
cpld_update_log_patterns = [
    r"program_cpld BASE_CPLD checksum is \w+",
    r"program_cpld: upgrade BASE_CPLD successfully",
    r"program_cpld FAN_CPLD checksum is \w+",
    r"program_cpld: upgrade FAN_CPLD successfully",
    r"program_cpld CPU_CPLD checksum is \w+",
    r"program_cpld: upgrade CPU_CPLD successfully",
    r"program_cpld SW_CPLD1 checksum is \w+",
    r"program_cpld: upgrade SW_CPLD1 successfully",
    r"program_cpld SW_CPLD2 checksum is \w+",
    r"program_cpld: upgrade SW_CPLD2 successfully",
    r"program_cpld TOP_LC_CPLD checksum is \w+",
    r"program_cpld: upgrade TOP_LC_CPLD successfully",
    r"program_cpld BOT_LC_CPLD checksum is \w+",
    r"program_cpld: upgrade BOT_LC_CPLD successfully",
]
syslog_path = '/var/log/syslog'
fwlog_path = '/var/log/fw_upgrade.log'
fpga_update_pass_msg = r'\b0\b'
fpga_update_log_cmd = 'cat %s | grep -i "program"'%(syslog_path)
fpga_update_log_patterns = [
    r'program_cpld FPGA checksum is \w+',
    r'program_cpld: upgrade FPGA successfully',
]

auto_test_cmd = './api_unittest --run-tests '
auto_test_dir = '/usr/share/sonic/device/x86_64-alibaba_as24-128d-cl-r0/bmc_api_unittest'
auto_test_image_dir = '/home/admin/img/'
auto_test_export_cmd = 'export BMC_TEST_PLATFORM=CEL'
auto_test_delay = 60

refresh_cpld_cmd = "a.refresh_firmware(['FAN_CPLD', 'BASE_CPLD', 'CPU_CPLD'],['%s/%s', '%s/%s', '%s/%s'])" \
    %(cpld_local_image_path, cpld_fan_refresh_image, cpld_local_image_path, cpld_base_refresh_image, \
      cpld_local_image_path, cpld_cpu_refresh_image)
refresh_cpld_log_cmd = 'cat %s | grep -i "refresh_firmware\\\|program_cpld"'%(syslog_path)
refresh_fw_log_cmd = 'cat %s | grep -i "refresh_firmware"'%(syslog_path)
refresh_fw_log_patterns = [
    r"(?i)refresh_firmware: Power off.*CPU",
    r"(?i)refresh_firmware: power (cycle|on) cpu and then rebooting BMC"
]

fpga_hex_pattern = r"(?mi)^(?P<hex_val>0x\w+)"
fpga_buf_ctrl_default_val = '0x4'
fpga_buf_ctrl_test_val = '0x1'

auto_fail_patterns = ['FAIL', 'ERROR']
upgrade_fw_log_cmd = 'cat %s | grep -i "_upgrade"'%(fwlog_path)
upgrade_fpga_log_patterns = [
    r"(?i)fpga_upgrade : start FPGA upgrade",
    r"(?i)fpga_upgrade : done",
    r"(?i)last_upgrade_result :.*FPGA.*DONE",
]
unittest_config_file = 'unittest_config.py'
skip_reboot_cpu_true = r'SKIP_REBOOT_CPU = True'
skip_reboot_cpu_false = r'SKIP_REBOOT_CPU = False'

power_status_pattern = r'Microserver power is\s*(.|\n)*(on|off|fail)'
power_ctrl_pattern = r'Power \w+ microserver.*[5s]?(.|\n)*(Done|Skip|Failed)'
come_status_pattern = r'COMe CPU boots (.*OK)'
bios_boot_pattern = [
    r'Copyright \(C\) \d+ American Megatrends, Inc',
    # r'>>Checking Media Presence',
    r'Welcome to GRUB'
]

auto_test_cpld_img_dict = {
    "FAN_CPLD": "as24-128d_cpld_1_cpu_pwr.vme",
    "BASE_CPLD": "as24-128d_cpld_2_cpu_pwr.vme",
    "COME_CPLD": "as24-128d_cpld_3_cpu_pwr.vme",
    "SWITCH_CPLD": "as24-128d_cpld_4_cpu_pwr.vme",
    "FAN_CPLD_REFRESH": "as24-128d_cpld_1_transfr_bmc.vme",
    "BASE_CPLD_REFRESH": "as24-128d_cpld_2_transfr_bmc.vme",
    "CPU_CPLD_REFRESH": "as24-128d_cpld_3_transfr_bmc.vme",
    "SWITCH_CPLD_REFRESH": "as24-128d_cpld_4_transfr_bmc.vme",
}
auto_test_top_cpld_img = "as24-128d_cpld_5_cpu_pwr.vme"
auto_test_bot_cpld_img = "as24-128d_cpld_6_cpu_pwr.vme"

auto_fw_refresh_cpld_patterns = [
    r"(?i)start CPLD upgrade",
    r"(?i)start TOP_LC_CPLD upgrade",
    r"(?i)done",
    r"(?i)start BOT_LC_CPLD upgrade",
    r"(?i)done",
    r"(?i)start SW_CPLD1 upgrade",
    r"(?i)done",
    r"(?i)start BASE_CPLD upgrade",
    r"(?i)done",
    r"(?i)start FAN_CPLD upgrade",
    r"(?i)done",
    r"(?i)start CPU_CPLD upgrade",
    r"(?i)done",
    r"(?P<file_name_5>[\\-\\w]+\\.vme).*?(?P<file_name_3>[\\-\\w]+\\.vme).*?(?P<file_name_4>[\\-\w]+\\.vme).*?(?P<file_name_2>[\\-\\w]+\\.vme).*?(?P<file_name_1>[\\-\\w]+\\.vme).*?(?P<done>(?:DONE\\:?){6})",
]

auto_fw_refresh_cpld_openbmc_patterns = [
    r"(?i)refresh_firmware: Power off.*CPU",
    r"(?i)program_cpld BASE_CPLD checksum is \\w+",
    r"(?i)program_cpld: upgrade BASE_CPLD successfully",
    r"(?i)program_cpld FAN_CPLD checksum is \\w+",
    r"(?i)program_cpld: upgrade FAN_CPLD successfully",
    r"(?i)program_cpld CPU_CPLD checksum is \\w+",
    r"(?i)program_cpld: upgrade CPU_CPLD successfully",
    r"(?i)refresh_firmware: power (cycle|on) cpu and then rebooting BMC",
]

refresh_base_log_patterns = refresh_fw_log_patterns.copy()
refresh_base_log_patterns[1:1] = [
    r"(?i)program_cpld BASE_CPLD checksum is \\w+",
    r"(?i)program_cpld: upgrade BASE_CPLD successfully"
]
refresh_fan_log_patterns = refresh_fw_log_patterns.copy()
refresh_fan_log_patterns[1:1] = [
    r"(?i)program_cpld FAN_CPLD checksum is \\w+",
    r"(?i)program_cpld: upgrade FAN_CPLD successfully"
]
refresh_cpu_log_patterns = refresh_fw_log_patterns.copy()
refresh_cpu_log_patterns[1:1] = [
    r"(?i)program_cpld CPU_CPLD checksum is \\w+",
    r"(?i)program_cpld: upgrade CPU_CPLD successfully"
]

upgrade_cpld_log_patterns = [
    r"(?i)cpld_upgrade : start CPLD upgrade",
    r"(?i)cpld_upgrade : done",
    r"(?i)last_upgrade_result :.*CPLD.*DONE",
]
upgrade_base_log_patterns = upgrade_cpld_log_patterns.copy()
upgrade_base_log_patterns.insert(1, r'(?i)cpld_upgrade : start BASE_CPLD upgrade')
upgrade_fan_log_patterns = upgrade_cpld_log_patterns.copy()
upgrade_fan_log_patterns.insert(1, r'(?i)cpld_upgrade : start FAN_CPLD upgrade')
upgrade_cpu_log_patterns = upgrade_cpld_log_patterns.copy()
upgrade_cpu_log_patterns.insert(1, r'(?i)cpld_upgrade : start CPU_CPLD upgrade')
upgrade_sw1_log_patterns = upgrade_cpld_log_patterns.copy()
upgrade_sw1_log_patterns.insert(1, r'(?i)cpld_upgrade : start SW_CPLD1 upgrade')
upgrade_sw2_log_patterns = upgrade_cpld_log_patterns.copy()
upgrade_sw2_log_patterns.insert(1, r'(?i)cpld_upgrade : start BOT_LC_CPLD upgrade')
upgrade_tplc_log_patterns = upgrade_cpld_log_patterns.copy()
upgrade_tplc_log_patterns.insert(1, r'(?i)cpld_upgrade : start TOP_LC_CPLD upgrade')

hal_unit_test_cmd = 'hal_unittest --run-tests '
hal_unit_test_path = '/usr/lib/python3.5/unittest'

util_fail_patterns = ['fail', 'error', no_such_file_msg]
UTIL_EEPROM_MAP_KEY = {
    'Board Custom Data 1'   : 'Board Extra_1',
    'Product Custom Data 1' : 'Product Extra_1',
    'Product Custom Data 2' : 'Product Extra_2',
    'Product Custom Data 3' : 'Product Extra_3',
    'Product Custom Data 4' : 'Product Extra_4',
}
eeprom_pattern = r'((?:Board|Product).+): (.+)'
diag_util_path = '/var/log/BMC_Diag/utility/'

bmc_eeprom_test = 'BMC_EEPROM_TEST'
bmc_eeprom_test2 = 'BMC_EEPROM_TEST2'
bmc_fru = 'bmc'
bmc_fru_type = 'bia'
bmc_eeprom_path = diag_util_path + 'BMC_fru_eeprom'

sys_eeprom_test = 'SYS_EEPROM_TEST'
sys_eeprom_test2 = 'SYS_EEPROM_TEST2'
sys_fru = 'sys'
sys_fru_type = 'biapia'
sys_eeprom_path = diag_util_path + 'system_fru_eeprom'

fcb_eeprom_test = 'FCB_EEPROM_TEST'
fcb_eeprom_test2 = 'FCB_EEPROM_TEST2'
fcb_fru = 'fb'
fcb_fru_type = 'bia'
fcb_eeprom_path = diag_util_path + 'FCB_fru_eeprom'

come_eeprom_test = 'COME_EEPROM_TEST'
come_eeprom_test2 = 'COME_EEPROM_TEST2'
come_fru = 'come'
come_fru_type = 'bia'
come_eeprom_path = diag_util_path + 'COMe_fru_eeprom'

switch_eeprom_test = 'SWITCH_EEPROM_TEST'
switch_eeprom_test2 = 'SWITCH_EEPROM_TEST2'
switch_fru = 'switch'
switch_fru_type = 'bia'
switch_eeprom_path = diag_util_path + 'switch_fru_eeprom'

FAN_NUM = 5
fan_eeprom_test = 'FAN_EEPROM_TEST'
fan_eeprom_test2 = 'FAN_EEPROM_TEST2'
fan_fru = 'fan'
fan_fru_type = 'pia'
fan_eeprom_path = '/var/log/BMC_Diag/utility/fan_fru_eeprom'

uart_log_file = '/var/log/console.log'

fand_log = '/var/log/fand.log'
dcdcmon_log = '/var/log/dcdcmon.log'
cpumon_log = '/var/log/cpumon.log'
powermon_log = '/var/log/powermon.log'

bmc_init_patterns = [r'random: nonblocking pool is initialized']
boot_syslog_cmd = 'cat %s | grep -i "boot from"'%(syslog_path)
boot_cpumon_cmd = 'cat %s | grep -i "boot from"'%(cpumon_log)

bmc_boot_slave_pattern = 'BMC boot from slave flash succeeded'
bmc_boot_master_pattern = 'BMC boot from master flash succeeded'
bios_boot_slave_pattern = 'BIOS boot from secondary flash succeeded'
bios_boot_master_pattern = 'BIOS boot from primary flash succeeded'
bios_version_dict = {SwImage.BIOS_VER: BIOS.newVersion}

bios_image = "bios.bin"
afu_new_image = AFU_TOOL.newImage
bmc_crash_pattern = r'Writing.*20%'
bios_crash_pattern = r'Updating Main Block.*20%'

bios_boot_master_fail_pattern = 'BIOS boot from primary flash failed'
bios_boot_slave_fail_pattern = 'BIOS boot from secondary flash failed'

meminfo_pattern = [
    r'MemTotal:      .*?kB',
    r'MemFree:       .*?kB',
    r'MemAvailable:  .*?kB',
    r'Buffers:       .*?kB',
    r'Cached:        .*?kB',
    r'SwapCached:    .*?kB',
    r'Active:        .*?kB',
    r'Inactive:      .*?kB',
    r'Active\(anon\):  .*?kB',
    r'Inactive\(anon\):.*?kB',
    r'Active\(file\):  .*?kB',
    r'Inactive\(file\):.*?kB',
    r'Unevictable:   .*?kB',
    r'Mlocked:       .*?kB',
    r'SwapTotal:     .*?kB',
    r'SwapFree:      .*?kB',
    r'Dirty:         .*?kB',
    r'Writeback:     .*?kB',
    r'AnonPages:     .*?kB',
    r'Mapped:        .*?kB',
    r'Shmem:         .*?kB',
    r'Slab:          .*?kB',
    r'SReclaimable:  .*?kB',
    r'SUnreclaim:    .*?kB',
    r'KernelStack:   .*?kB',
    r'PageTables:    .*?kB',
    r'NFS_Unstable:  .*?kB',
    r'Bounce:        .*?kB',
    r'WritebackTmp:  .*?kB',
    r'CommitLimit:   .*?kB',
    r'Committed_AS:  .*?kB',
    r'VmallocTotal:  .*?kB',
    r'VmallocUsed:   .*?kB',
    r'VmallocChunk:  .*?kB',
]

memtest_pattern = [
    r'Stuck Address       :.*?ok',
    r'Random Value        :.*?ok',
    r'Compare XOR         :.*?ok',
    r'Compare SUB         :.*?ok',
    r'Compare MUL         :.*?ok',
    r'Compare DIV         :.*?ok',
    r'Compare OR          :.*?ok',
    r'Compare AND         :.*?ok',
    r'Sequential Increment:.*?ok',
    r'Solid Bits          :.*?ok',
    r'Block Sequential    :.*?ok',
    r'Checkerboard        :.*?ok',
    r'Bit Spread          :.*?ok',
    r'Bit Flip            :.*?ok',
    r'Walking Ones        :.*?ok',
    r'Walking Zeroes      :.*?ok',
    r'8-bit Writes        :.*?ok',
    r'16-bit Writes       :.*?ok',
]

reboot_error_patterns = [
    r'\b(error)\b',
    r'no driver bound',
    r'module lm75 not found',
    r'module pmbus not found'
]

monlog_error_patterns = [
    r'exception',
    r'unexpected',
    r'error'
]

MIN_RPM = 0
MAX_RPM = 15000

wdt_patterns_1 = [
    r"(?i)WDT1.*Count:\s*(?P<wdt1>1)",
    r"(?i)WDT2.*Count:\s*(?P<wdt2>0)",
    r"(?i)Current Boot Code Source:\s*(?P<current_booy>Master)"
]

wdt_patterns_2 = [
    r"(?i)WDT1.*Count:\s*(?P<wdt1>2)",
    r"(?i)WDT2.*Count:\s*(?P<wdt2>0)",
    r"(?i)Current Boot Code Source:\s*(?P<current_boot>Master)"
]

wdt_patterns_3 = [
    r"(?i)WDT1.*Count:\s*(?P<wdt1>2)",
    r"(?i)WDT2.*Count:\s*(?P<wdt2>1)",
    r"(?i)Current Boot Code Source:\s*(?P<current_boot>Slave)"
]

wdt_patterns_4 = [
    r"(?i)WDT1.*Count:\s*(?P<wdt1>3)",
    r"(?i)WDT2.*Count:\s*(?P<wdt2>1)",
    r"(?i)Current Boot Code Source:\s*(?P<current_boot>Slave)"
]

wdt_patterns_5 = [
    r"(?i)WDT1.*Count:\s*(?P<wdt1>4)",
    r"(?i)WDT2.*Count:\s*(?P<wdt2>1)",
    r"(?i)Current Boot Code Source:\s*(?P<current_boot>Slave)"
]

wdt_patterns_6 = [
    r"(?i)WDT1.*Count:\s*(?P<wdt1>4)",
    r"(?i)WDT2.*Count:\s*(?P<wdt2>2)",
    r"(?i)Current Boot Code Source:\s*(?P<current_boot>Master)"
]

ls_lh_pattern = r'[d|c|b|s|p|l|r|w|x|t|-]+\\s+\\d+\\s+\\w+.*'

api_bmc_url = "http://240.1.1.1:8080/api"
api_bmc_nextboot = "bmc/nextboot"
api_bmc_info = "bmc/info"
api_bios_nextboot = "firmware/biosnextboot"
api_bios_info = "misc/biosbootstatus"

nextboot_master_patterns = [
    r'(?i)"Flash": "(?P<flashboot>master)"',
    r'(?i)"status": "(?P<status>OK)"'
]

nextboot_slave_patterns = [
    r'(?i)"Flash": "(?P<flashboot>slave)"',
    r'(?i)"status": "(?P<status>OK)"'
]

info_master_master_patterns = [
    r'(?i)"Flash": "(?P<flashboot>master)"',
    r'(?i)"Next": "(?P<nextboot>master)"',
    r'(?i)"status": "(?P<status>OK)"'
]

info_master_slave_patterns = [
    r'(?i)"Flash": "(?P<flashboot>master)"',
    r'(?i)"Next": "(?P<nextboot>slave)"',
    r'(?i)"status": "(?P<status>OK)"'
]

info_slave_slave_patterns = [
    r'(?i)"Flash": "(?P<flashboot>slave)"',
    r'(?i)"Next": "(?P<nextboot>slave)"',
    r'(?i)"status": "(?P<status>OK)"'
]

info_slave_master_patterns = [
    r'(?i)"Flash": "(?P<flashboot>slave)"',
    r'(?i)"Next": "(?P<nextboot>master)"',
    r'(?i)"status": "(?P<status>OK)"'
]

status_ok_patterns = [
    r'(?i)"message": "(?P<message>OK)"',
    r'(?i)"status": "(?P<status>OK)"'
]

date_pattern = r'(\w+\s+\w+\s+\d+\s+\d+:\d+:\d+\s+\w+\s+\d+)'
ntpstat_patterns = [
    r'(?mi)synchronised to local net at stratum \\d+',
    r'(?mi)time correct to within \\d+ ms',
    r'(?mi)polling server every \\d+ s'
]

ntp_conf_file = "/etc/ntp.conf"
ntp_config_list = [
    "server 127.127.1.0",
    "fudge 127.127.1.0 stratum 8",
    "server 2.debian.pool.ntp.org iburst",
    "server 1.debian.pool.ntp.org iburst",
    "server 3.debian.pool.ntp.org iburst",
    "server 0.debian.pool.ntp.org iburst",
    "interface ignore wildcard",
    "interface listen eth0.4088",
    "interface listen 127.0.0.1",
]

get_on_pattern = r"^'?(?P<status>on)'?$"
get_off_pattern = r"^'?(?P<status>off)'?$"
set_pass_pattern = r'^(?P<status>0)$'
set_fail_pattern = r'^(?P<status>-1)$'
get_fail_pattern = r"^'(?P<status>N/A)'$"

ssd_off_err_patterns = [
    r'ext4_journal_check_start:56: Detected aborted journal',
    r'Remounting filesystem read-only',
    r'previous I/O error to superblock detected',
    r'blk_update_request: I/O error, dev \\w+, sector \\d+',
    r'Aborting journal on device loop1-8',
    r'loop: Write error at byte offset \\d+, length \\d+',
    r'ext4_find_entry:\\d+: inode #\\d+: comm \\w+: reading directory lblock \\d+'
]
ssd_on_err_patterns = [
    r'Unable to read.*',
    r'ext4_find_entry:\\d+: inode #\\d+: comm \\w+: reading directory lblock \\d+'
]
ssd_off_err_pattern = "|".join(ssd_off_err_patterns)
ssd_on_err_pattern = "|".join(ssd_on_err_patterns)

switch_chip_sensors_cmd = 'sensors | grep -iE "SW.*QSFP|TOP_LC_XP3R3V|BOTTOM_LC_XP3R3V"'
sensors_pattern = r'(.+):\s+([+|-]?\d+.\d+)\s+\w+'
switch_chip_dev_path = '/etc/openbmc/devices/AS24-128D-CL'
sensors_conf_file = 'sensors_config.json'
power_ctrl_config_list = [
    r'"power_force_ctrl":"/sys/bus/i2c/devices/i2c-0/0-000d/pwr_force_ctrl_en',
    r'"power_ctrl_switch_ports":"/sys/bus/i2c/devices/i2c-0/0-000d/pwr_switch_ports',
    r'"power_ctrl_switch_chip":"/sys/bus/i2c/devices/i2c-0/0-000d/pwr_switch_chip',
    r'"power_ctrl_ssd":"/sys/bus/i2c/devices/i2c-0/0-000d/pwr_ssd'
]
cel_port_scan_cmd = "./cel-port-test -s"
cel_port1_scan_cmd = "./cel-port-test -s -d 1"
cel_port_reset_enable = "./cel-port-test -c -t reset -D 0"
cel_port_reset_disable = "./cel-port-test -c -t reset -D 1"
cel_port1_reset_enable = "./cel-port-test -c -t reset -D 0 -d 1"
cel_port1_reset_disable = "./cel-port-test -c -t reset -D 1 -d 1"

PSU_NUM = 4
psu_all_fru_cmd = "fru-util psu -a"
psu_all_sensors_cmd = "sensors dps1100-i2c-24-5b dps1100-i2c-25-5b dps1100-i2c-26-5b dps1100-i2c-27-5b"

psu_1_fru_patterns = [
    r"(?mi)^[ \\t]*FRU Information[ \\t]+:[ \\t]*(?P<psu_1>PSU1)",
    r"(?mi)^[ \\t]*Product Manufacturer[ \\t]+:[ \\t]*(?P<psu_1_manu>\S+)",
    r"(?mi)^[ \\t]*Product Name[ \\t]+:[ \\t]*(?P<psu_1_name>\S+)",
    r"(?mi)^[ \\t]*Product Serial[ \\t]+:[ \\t]*(?P<psu_1_serial>\S+)",
    r"(?mi)^[ \\t]*Product Version[ \\t]+:[ \\t]*(?P<psu_1_version>\S+)",
]
psu_2_fru_patterns = [
    r"(?mi)^[ \\t]*FRU Information[ \\t]+:[ \\t]*(?P<psu_2>PSU2)",
    r"(?mi)^[ \\t]*Product Manufacturer[ \\t]+:[ \\t]*(?P<psu_2_manu>\S+)",
    r"(?mi)^[ \\t]*Product Name[ \\t]+:[ \\t]*(?P<psu_2_name>\S+)",
    r"(?mi)^[ \\t]*Product Serial[ \\t]+:[ \\t]*(?P<psu_2_serial>\S+)",
    r"(?mi)^[ \\t]*Product Version[ \\t]+:[ \\t]*(?P<psu_2_version>\S+)",
]
psu_3_fru_patterns = [
    r"(?mi)^[ \\t]*FRU Information[ \\t]+:[ \\t]*(?P<psu_3>PSU3)",
    r"(?mi)^[ \\t]*Product Manufacturer[ \\t]+:[ \\t]*(?P<psu_3_manu>\S+)",
    r"(?mi)^[ \\t]*Product Name[ \\t]+:[ \\t]*(?P<psu_3_name>\S+)",
    r"(?mi)^[ \\t]*Product Serial[ \\t]+:[ \\t]*(?P<psu_3_serial>\S+)",
    r"(?mi)^[ \\t]*Product Version[ \\t]+:[ \\t]*(?P<psu_3_version>\S+)",
]
psu_4_fru_patterns = [
    r"(?mi)^[ \\t]*FRU Information[ \\t]+:[ \\t]*(?P<psu_4>PSU4)",
    r"(?mi)^[ \\t]*Product Manufacturer[ \\t]+:[ \\t]*(?P<psu_4_manu>\S+)",
    r"(?mi)^[ \\t]*Product Name[ \\t]+:[ \\t]*(?P<psu_4_name>\S+)",
    r"(?mi)^[ \\t]*Product Serial[ \\t]+:[ \\t]*(?P<psu_4_serial>\S+)",
    r"(?mi)^[ \\t]*Product Version[ \\t]+:[ \\t]*(?P<psu_4_version>\S+)",
]
psu_all_fru_normal_patterns = psu_1_fru_patterns + psu_2_fru_patterns + psu_3_fru_patterns + psu_4_fru_patterns

psu_1_device_patterns = [r"(?P<sensor_psu_1>^dps1100-i2c-27-5b)"]
psu_2_device_patterns = [r"(?P<sensor_psu_2>^dps1100-i2c-26-5b)"]
psu_3_device_patterns = [r"(?P<sensor_psu_3>^dps1100-i2c-25-5b)"]
psu_4_device_patterns = [r"(?P<sensor_psu_4>^dps1100-i2c-24-5b)"]
psu_sensors_error_patterns = [
    r"Adapter:\s+(?P<i2c_psu>i2c-6-mux.*)",
    r"vin:\s+(?P<vin_psu>N\/A)",
    r"vout1:\s+(?P<vout1_psu>N\/A)",
    r"fan1:\s+(?P<fan1_psu>N\/A)",
    r"temp1:\s+(?P<temp1_psu>N\/A)",
    r"temp2:\s+(?P<temp2_psu>N\/A)",
    r"pin:\s+(?P<pin_psu>N\/A)",
    r"pout1:\s+(?P<pout1_psu>N\/A)",
    r"iin:\s+(?P<iin_psu>N\/A)",
    r"iout1:\s+(?P<iout1_psu>N\/A)",
]
psu_1_sensors_patterns = [
    r"(?P<sensor_psu_1>^dps1100-i2c-27-5b)",
    r"Adapter:\s+(?P<i2c_psu_1>i2c-6-mux.*)",
    r"vin:\s+(?P<vin_psu_1>[+|-]?\d+.\d+)\s+\w+",
    r"vout1:\s+(?P<vout1_psu_1>[+|-]?\d+.\d+)\s+\w+",
    r"fan1:\s+(?P<fan1_psu_1>[+|-]?\d+.\d+)\s+\w+",
    r"temp1:\s+(?P<temp1_psu_1>[+|-]?\d+.\d+)\s+\w+",
    r"temp2:\s+(?P<temp2_psu_1>[+|-]?\d+.\d+)\s+\w+",
    r"pin:\s+(?P<pin_psu_1>[+|-]?\d+.\d+)\s+\w+",
    r"pout1:\s+(?P<pout1_psu_1>[+|-]?\d+.\d+)\s+\w+",
    r"iin:\s+(?P<iin_psu_1>[+|-]?\d+.\d+)\s+\w+",
    r"iout1:\s+(?P<iout1_psu_1>[+|-]?\d+.\d+)\s+\w+",
]
psu_2_sensors_patterns = [
    r"(?P<sensor_psu_2>^dps1100-i2c-26-5b)",
    r"Adapter:\s+(?P<i2c_psu_2>i2c-6-mux.*)",
    r"vin:\s+(?P<vin_psu_2>[+|-]?\d+.\d+)\s+\w+",
    r"vout1:\s+(?P<vout1_psu_2>[+|-]?\d+.\d+)\s+\w+",
    r"fan1:\s+(?P<fan1_psu_2>[+|-]?\d+.\d+)\s+\w+",
    r"temp1:\s+(?P<temp1_psu_2>[+|-]?\d+.\d+)\s+\w+",
    r"temp2:\s+(?P<temp2_psu_2>[+|-]?\d+.\d+)\s+\w+",
    r"pin:\s+(?P<pin_psu_2>[+|-]?\d+.\d+)\s+\w+",
    r"pout1:\s+(?P<pout1_psu_2>[+|-]?\d+.\d+)\s+\w+",
    r"iin:\s+(?P<iin_psu_2>[+|-]?\d+.\d+)\s+\w+",
    r"iout1:\s+(?P<iout1_psu_2>[+|-]?\d+.\d+)\s+\w+",
]
psu_3_sensors_patterns = [
    r"(?P<sensor_psu_3>^dps1100-i2c-25-5b)",
    r"Adapter:\s+(?P<i2c_psu_3>i2c-6-mux.*)",
    r"vin:\s+(?P<vin_psu_3>[+|-]?\d+.\d+)\s+\w+",
    r"vout1:\s+(?P<vout1_psu_3>[+|-]?\d+.\d+)\s+\w+",
    r"fan1:\s+(?P<fan1_psu_3>[+|-]?\d+.\d+)\s+\w+",
    r"temp1:\s+(?P<temp1_psu_3>[+|-]?\d+.\d+)\s+\w+",
    r"temp2:\s+(?P<temp2_psu_3>[+|-]?\d+.\d+)\s+\w+",
    r"pin:\s+(?P<pin_psu_3>[+|-]?\d+.\d+)\s+\w+",
    r"pout1:\s+(?P<pout1_psu_3>[+|-]?\d+.\d+)\s+\w+",
    r"iin:\s+(?P<iin_psu_3>[+|-]?\d+.\d+)\s+\w+",
    r"iout1:\s+(?P<iout1_psu_3>[+|-]?\d+.\d+)\s+\w+",
]
psu_4_sensors_patterns = [
    r"(?P<sensor_psu_4>^dps1100-i2c-24-5b)",
    r"Adapter:\s+(?P<i2c_psu_4>i2c-6-mux.*)",
    r"vin:\s+(?P<vin_psu_4>[+|-]?\d+.\d+)\s+\w+",
    r"vout1:\s+(?P<vout1_psu_4>[+|-]?\d+.\d+)\s+\w+",
    r"fan1:\s+(?P<fan1_psu_4>[+|-]?\d+.\d+)\s+\w+",
    r"temp1:\s+(?P<temp1_psu_4>[+|-]?\d+.\d+)\s+\w+",
    r"temp2:\s+(?P<temp2_psu_4>[+|-]?\d+.\d+)\s+\w+",
    r"pin:\s+(?P<pin_psu_4>[+|-]?\d+.\d+)\s+\w+",
    r"pout1:\s+(?P<pout1_psu_4>[+|-]?\d+.\d+)\s+\w+",
    r"iin:\s+(?P<iin_psu_4>[+|-]?\d+.\d+)\s+\w+",
    r"iout1:\s+(?P<iout1_psu_4>[+|-]?\d+.\d+)\s+\w+",
]
psu_all_sensors_normal_patterns = psu_4_sensors_patterns + psu_3_sensors_patterns + psu_2_sensors_patterns + psu_1_sensors_patterns
psu_1_sensors_error_patterns = psu_4_sensors_patterns + psu_3_sensors_patterns + psu_2_sensors_patterns + \
                               psu_1_device_patterns + psu_sensors_error_patterns
psu_2_sensors_error_patterns = psu_4_sensors_patterns + psu_3_sensors_patterns + \
                               psu_2_device_patterns + psu_sensors_error_patterns + psu_1_sensors_patterns
psu_3_sensors_error_patterns = psu_4_sensors_patterns + psu_3_device_patterns + psu_sensors_error_patterns + \
                               psu_2_sensors_patterns + psu_1_sensors_patterns
psu_4_sensors_error_patterns = psu_4_device_patterns + psu_sensors_error_patterns + psu_3_sensors_patterns + \
                               psu_2_sensors_patterns + psu_1_sensors_patterns

test1_script = '''#!/bin/bash
while :
do
cat /sys/bus/i2c/devices/16-000e/in0_input > /dev/null &
sleep 0.5
done
'''

test2_script = '''#!/bin/bash
while :
do
cat /sys/bus/i2c/devices/16-000e/in1_input > /dev/null &
sleep 0.5
done
'''

board_util_script = "/usr/local/bin/board-utils.sh"
board_util_old_str = "        sleep 7"
board_util_new_str = "        sleep 3"

power_off_fail_log_patterns = [
    r"(?i)root: Failed to power off micro-server,retry 1 times",
    r"(?i)root: Failed to power off micro-server,retry 2 times",
    r"(?i)root: Failed to power off micro-server,retry 3 times",
]
