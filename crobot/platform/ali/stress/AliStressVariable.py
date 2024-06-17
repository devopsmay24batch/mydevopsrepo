###############################################################################
# LEGALESE:   "Copyright (C) 2021, Celestica Corp. All rights reserved."      #
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
from AliDiagVariable import *
from crobot.SwImage import SwImage

new_bmc_version = SwImage.getSwImage(SwImage.BMC).newVersion
old_bmc_version = SwImage.getSwImage(SwImage.BMC).oldVersion
fpga_fw_path = SwImage.getSwImage(SwImage.FPGA).hostImageDir
fpga_old_fw_name = SwImage.getSwImage(SwImage.FPGA).oldImage
fpga_new_fw_name = SwImage.getSwImage(SwImage.FPGA).newImage
fpga_old_fw_version = SwImage.getSwImage(SwImage.FPGA).oldVersion
fpga_new_fw_version = SwImage.getSwImage(SwImage.FPGA).newVersion
fpga_multboot_new_fw_name = SwImage.getSwImage('FPGA_MULTBOOT').newImage
fpga_multboot_old_fw_name = SwImage.getSwImage('FPGA_MULTBOOT').oldImage
cpld_fw_path = SwImage.getSwImage(SwImage.BASE_CPLD).hostImageDir
basecpld_old_fw_name = SwImage.getSwImage(SwImage.BASE_CPLD).oldImage
basecpld_new_fw_name = SwImage.getSwImage(SwImage.BASE_CPLD).newImage
cpu_cpld_old_fw_name = SwImage.getSwImage(SwImage.COME_CPLD).oldImage
cpu_cpld_new_fw_name = SwImage.getSwImage(SwImage.COME_CPLD).newImage
fan_cpld_old_fw_name = SwImage.getSwImage(SwImage.FAN_CPLD).oldImage
fan_cpld_new_fw_name = SwImage.getSwImage(SwImage.FAN_CPLD).newImage
switch_cpld_old_fw_name = SwImage.getSwImage(SwImage.SWITCH_CPLD).oldImage
switch_cpld_new_fw_name = SwImage.getSwImage(SwImage.SWITCH_CPLD).newImage
basecpld_refresh_fw_name = SwImage.getSwImage('BASE_CPLD_REFRESH').newImage
cpu_cpld_refresh_fw_name = SwImage.getSwImage('CPU_CPLD_REFRESH').newImage
fan_cpld_refresh_fw_name = SwImage.getSwImage('FAN_CPLD_REFRESH').newImage


deviceName = os.environ.get("deviceName", "").lower()
logging.info("deviceName:{}".format(deviceName))
if "migaloo" in deviceName:
    platform = 'migaloo'
    diagos_cpu_sdk_path = '/usr/local/migaloo/SDK'
    diagos_cpu_diag_path = '/usr/local/migaloo/CPU_Diag'
    test_10gkr_cmd = './cel-10KR-test -a'
    diagos_tool_path = '/usr/local/migaloo/utility'
    diag_i2c_test_cmd = './cel-i2c-test --all'
    diag_i2c_test_pattern = '(?mi)^[ \\t]*I2C test.*\\[[ \\t]*(?P<result>PASS)'
    diag_utility_path = diagos_tool_path
    openbmc_mido_test = './cel-mdio-test -a'
    cpld_test_pattern = '(?mi)^[ \\t]*CPLD test.*\\[[ \\t]*(?P<result>PASS)'
    lspci_list_count = '83'
    sensor_lines = '252'
    read_fpga_version_cmd = './cel-version-test -S'
    read_cpld_version_cmd = './cel-version-test -S'
    program_new_cpld = """a.program_cpld(['BASE_CPLD', 'CPU_CPLD', 'FAN_CPLD', 'SW_CPLD1', 'SW_CPLD2', 'TOP_LC_CPLD', 'BOT_LC_CPLD'], ['/var/log/STRESS/%s', '/var/log/STRESS/%s', '/var/log/STRESS/%s', '/var/log/STRESS/%s', '/var/log/STRESS/%s', '/var/log/STRESS/%s', '/var/log/STRESS/%s'])""" % (basecpld_new_fw_name, cpu_cpld_new_fw_name, fan_cpld_new_fw_name, switch_cpld_new_fw_name, switch_cpld_new_fw_name, switch_cpld_new_fw_name, switch_cpld_new_fw_name)
    program_old_cpld = """a.program_cpld(['BASE_CPLD', 'CPU_CPLD', 'FAN_CPLD', 'SW_CPLD1', 'SW_CPLD2', 'TOP_LC_CPLD', 'BOT_LC_CPLD'], ['/var/log/STRESS/%s', '/var/log/STRESS/%s', '/var/log/STRESS/%s', '/var/log/STRESS/%s', '/var/log/STRESS/%s', '/var/log/STRESS/%s', '/var/log/STRESS/%s'])""" % (basecpld_old_fw_name, cpu_cpld_old_fw_name, fan_cpld_old_fw_name, switch_cpld_old_fw_name, switch_cpld_old_fw_name, switch_cpld_old_fw_name, switch_cpld_old_fw_name)

if "shamu" in deviceName:
    platform = 'shamu'
    diagos_cpu_sdk_path = '/usr/local/CPU_Diag/utility/Shamu_SDK'
    diagos_cpu_diag_path = '/usr/local/CPU_Diag/bin'
    test_10gkr_cmd = './cel-10gKR-test -t'
    diagos_tool_path = '/usr/local/CPU_Diag/utility/stress'
    diag_i2c_test_cmd = './cel-i2c-test -t'
    diag_i2c_test_pattern = r'All the I2C devices test.*?\[ PASS \]'
    diag_utility_path = '/usr/local/CPU_Diag/utility/'
    openbmc_mido_test = './cel-mdio-test -t'
    cpld_test_pattern = r'Switch CPLD-1.*?\[ PASS \].*?Switch CPLD-2.*?\[ PASS \].*?Base board.*?\[ PASS \].*?COMe board.*?\[ PASS \]'
    lspci_list_count = '83'
    sensor_lines = '141'
    read_fpga_version_cmd = './cel-fpga-test -v'
    read_cpld_version_cmd = './cel-cpld-test -v'
    program_new_cpld = """a.program_cpld(['BASE_CPLD', 'CPU_CPLD', 'FAN_CPLD', 'SW_CPLD1', 'SW_CPLD2'], ['/var/log/STRESS/%s', '/var/log/STRESS/%s', '/var/log/STRESS/%s', '/var/log/STRESS/%s', '/var/log/STRESS/%s'])""" % (basecpld_new_fw_name, cpu_cpld_new_fw_name, fan_cpld_new_fw_name, switch_cpld_new_fw_name, switch_cpld_new_fw_name)
    program_old_cpld = """a.program_cpld(['BASE_CPLD', 'CPU_CPLD', 'FAN_CPLD', 'SW_CPLD1', 'SW_CPLD2'], ['/var/log/STRESS/%s', '/var/log/STRESS/%s', '/var/log/STRESS/%s', '/var/log/STRESS/%s', '/var/log/STRESS/%s'])""" % (basecpld_old_fw_name, cpu_cpld_old_fw_name, fan_cpld_old_fw_name, switch_cpld_old_fw_name, switch_cpld_old_fw_name)

BCM_promptstr = "BCM.0>"
openbmc_diag_path = '/var/log/BMC_Diag/bin'
bmc_ddr_result_pattern = (r'Stuck Address.*?ok.*?Random Value.*?ok.*?Compare XOR.*?ok.*?Compare SUB.*?ok.*?'
                          r'Compare MUL.*?ok.*?Compare DIV.*?ok.*?Compare OR.*?ok.*?Compare AND.*?ok.*?'
                          r'Sequential Increment.*?ok.*?Solid Bits.*?ok.*?Block Sequential.*?ok.*?'
                          r'Checkerboard.*?ok.*?Bit Spread.*?ok.*?Bit Flip.*?ok.*?Walking Ones.*?ok.*?'
                          r'Walking Zeroes.*?ok')
refresh_cpld_cmd = "a.refresh_firmware(['FAN_CPLD', 'BASE_CPLD', 'CPU_CPLD'],['/var/log/STRESS/%s', '/var/log/STRESS/%s', '/var/log/STRESS/%s'])" % (fan_cpld_refresh_fw_name, basecpld_refresh_fw_name, cpu_cpld_refresh_fw_name)
program_old_fpga = "a.program_cpld(['FPGA'],['/var/log/STRESS/%s'])" % fpga_multboot_old_fw_name
program_new_fpga = "a.program_cpld(['FPGA'],['/var/log/STRESS/%s'])" % fpga_multboot_new_fw_name

# How long to run stress test
times_20 = 1
times_500 = 3
times_512 = 2
times_200 = 2
times_100 = 2
times_1000 = 3
times_10000000 = 3
times_1000000 = 3

time_sec_12_60_60 = 12     # For 500 times   12*60*60
time_sec_24_60_60 = 180
time_sec_48_60_60 = 48
time_sec_96_60_60 = 96

stress_tc001_total_test_time_sec = time_sec_12_60_60
stress_tc002_total_test_time_sec = 600  # if the test size=10g, it needs 400s
stress_tc003_total_test_time_sec = time_sec_24_60_60
stress_tc004_total_test_time_sec = time_sec_12_60_60
stress_tc006_total_test_time_sec = 60
stress_tc007_total_test_time_sec = 60
stress_tc008_total_test_time_sec = 60
stress_tc009_total_test_time_sec = time_sec_12_60_60
stress_tc010_total_test_time_sec = time_sec_24_60_60
stress_tc014_total_test_time_sec = 120
stress_tc015_total_test_time_sec = time_sec_12_60_60
stress_tc022_total_test_time_sec = time_sec_12_60_60  # For 500 times
stress_tc023_total_test_time_sec = time_sec_24_60_60
stress_tc024_total_test_time_sec = time_sec_24_60_60  # For 200 times
stress_tc025_total_test_time_sec = time_sec_24_60_60  # For 200 times
stress_tc025_total_test_times = times_200
stress_tc027_total_test_time_sec = time_sec_24_60_60  # For 200 times
stress_tc028_total_test_time_sec = time_sec_24_60_60
stress_tc029_total_test_time_sec = time_sec_24_60_60
stress_tc030_total_test_time_sec = time_sec_24_60_60  # For 200 times
stress_tc030_total_test_times = times_200
stress_tc031_total_test_time_sec = time_sec_24_60_60
stress_tc031_total_test_times = times_200
stress_tc032_total_test_time_sec = time_sec_24_60_60  # For 200 times
stress_tc032_total_test_times = times_200
stress_tc033_total_test_time_sec = time_sec_24_60_60  # For 200 times
stress_tc033_total_test_times = times_200
stress_tc034_total_test_time_sec = time_sec_24_60_60  # For 200 times
stress_tc034_total_test_times = times_200
stress_tc035_total_test_time_sec = time_sec_24_60_60
stress_tc036_total_test_time_sec = time_sec_24_60_60
stress_tc038_total_test_times = times_500
stress_tc039_total_test_time_sec = time_sec_24_60_60
stress_tc040_total_test_time_sec = time_sec_24_60_60
stress_tc040_total_test_times = times_200
stress_tc041_total_test_time_sec = time_sec_96_60_60  # 4 Days for 200 times
stress_tc041_total_test_times = times_200
stress_tc042_total_test_time_sec = time_sec_24_60_60
stress_tc042_total_test_times = times_200
stress_tc043_total_test_time_sec = time_sec_24_60_60  # For 500 times
stress_tc043_total_test_times = times_500


# End of How long to run stress test

# SwImage shared objects

# End of SwImage shared objects

stress_script_tarball_file = "STRESS-20210802.tar.xz"

iperf_unexpected_patterns = [
    r"(?i)connect failed: Connection refused",
]

idle_system_log_unexpected_patterns = [
    r"(?i)error",
    r"(?i)bug",
    r"(?i)unable to handle",
    r"(?i)null",
]

restful_cpld_response_pass_patterns = [
    r"(?i)Outputs.*(?P<pass>PASS)",
    r"(?i)status.*(?P<ok>OK)",
]
