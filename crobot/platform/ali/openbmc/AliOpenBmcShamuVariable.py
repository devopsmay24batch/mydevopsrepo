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

from AliOpenBmcVariable import *

diag_cpu_path = '/usr/local/CPU_Diag/bin'
cpld_update_timeout = 45*60
cpld_version_cmd = './cel-cpld-test -v'
fpga_version_cmd = './cel-fpga-test -v'

BASE_CPLD_KEY = "Base board CPLD version"
COME_CPLD_KEY = "COMe board CPLD version"
FAN_CPLD_KEY = "FAN CPLD Version"
SWITCH_CPLD1_KEY = "Switch CPLD-1 version"
SWITCH_CPLD2_KEY = "Switch CPLD-2 version"

cpld_type_image_dict = {
    "BASE_CPLD": "BASE_CPLD",
    "CPU_CPLD": "COME_CPLD",
    "FAN_CPLD": "FAN_CPLD",
    "SW_CPLD1": "SWITCH_CPLD",
    "SW_CPLD2": "SWITCH_CPLD",
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
]
fpga_buf_ctrl_default_val = '0x0'

MAX_RPM = 20000
FAN_NUM = 6

PSU_NUM = 2
psu_all_fru_normal_patterns = psu_1_fru_patterns + psu_2_fru_patterns
psu_all_sensors_cmd = "sensors dps1100-i2c-24-5b dps1100-i2c-25-5b"

psu_1_device_patterns = [r"(?P<sensor_psu_1>^dps1100-i2c-25-5b)"]
psu_2_device_patterns = [r"(?P<sensor_psu_2>^dps1100-i2c-24-5b)"]

psu_1_sensors_patterns[0] = psu_1_device_patterns[0]
psu_2_sensors_patterns[0] = psu_2_device_patterns[0]

psu_all_sensors_normal_patterns = psu_2_sensors_patterns + psu_1_sensors_patterns
psu_1_sensors_error_patterns = psu_2_sensors_patterns + psu_1_device_patterns + psu_sensors_error_patterns
psu_2_sensors_error_patterns = psu_2_device_patterns + psu_sensors_error_patterns + psu_1_sensors_patterns

switch_chip_sensors_cmd = 'sensors | grep -vE "SW.*XP5R0V" | grep -iE "Sw|LC"'
switch_chip_dev_path = '/etc/openbmc/devices/AS14-40D-F-CL'

cel_port_scan_cmd = "./cel-port-test -P"
cel_port1_scan_cmd = "./cel-port-test -P -p 1"
cel_port_reset_enable = "./cel-port-test -r enable"
cel_port_reset_disable = "./cel-port-test -r disable"
cel_port1_reset_enable = "./cel-port-test -r enable -p 1"
cel_port1_reset_disable = "./cel-port-test -r disable -p 1"

auto_test_dir = '/usr/share/sonic/device/x86_64-alibaba_as14-40d-cl-r0/bmc_api_unittest'
auto_test_cpld_img_dict = {
    "FAN_CPLD"  : "as14-40d_cpld_1_cpu_pwr.vme",
    "BASE_CPLD" : "as14-40d_cpld_2_cpu_pwr.vme",
    "COME_CPLD"  : "as14-40d_cpld_3_cpu_pwr.vme",
    "SWITCH_CPLD"  : "as14-40d_cpld_4_cpu_pwr.vme",
    "FAN_CPLD_REFRESH": "as14-40d_cpld_1_transfr_bmc.vme",
    "BASE_CPLD_REFRESH": "as14-40d_cpld_2_transfr_bmc.vme",
    "CPU_CPLD_REFRESH": "as14-40d_cpld_3_transfr_bmc.vme",
    "SWITCH_CPLD_REFRESH": "as14-40d_cpld_4_transfr_bmc.vme",
}

auto_fw_refresh_cpld_patterns = [
    r"(?i)start CPLD upgrade",
    r"(?i)start SW_CPLD1 upgrade",
    r"(?i)done",
    r"(?i)start BASE_CPLD upgrade",
    r"(?i)done",
    r"(?i)start FAN_CPLD upgrade",
    r"(?i)done",
    r"(?i)start CPU_CPLD upgrade",
    r"(?i)done",
    r"(?P<file_name_3>[\\-\\w]+\\.vme).*?(?P<file_name_4>[\\-\\w]+\\.vme).*?(?P<file_name_2>[\\-\w]+\\.vme).*?(?P<file_name_1>[\\-\\w]+\\.vme).*?(?P<done>(?:DONE\\:?){4})",
]

