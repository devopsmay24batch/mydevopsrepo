###############################################################################
# LEGALESE:   "Copyright (C) 2020-      Celestica Corp. All rights reserved." #
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
from Const import BOOT_MODE_UBOOT, BOOT_MODE_DIAGOS, BOOT_MODE_ONIE,ONIE_RESCUE_MODE
import copy

devicename = os.environ.get("deviceName", "")
pc_info = DeviceMgr.getServerInfo('PC')
dev_info = DeviceMgr.getDevice()
server_ipv4 = pc_info.managementIP

pcb_version = "0x0"
image_version = "0x1"
board_version = "0x1"
current_version = "0x401"
raw_access_data = "0x11000401"
raw_access_addr = "0x00000000"
data_path = "/sys/devices/xilinx/pps-i2c/raw_access_data"
addr_path = "/sys/devices/xilinx/pps-i2c/raw_access_addr"
value1 = "0x55667788"
new_value1 = "\"0x0004 0x55667788\""
value2 = "0x0004"
new_value2 = "0x00000004"
new_raw_access_data = "\"0x0004 0x11000401\""
new_raw_access_addr = "0x0000"


accel_raw_data = "0x20000102"
accel_new_data = "\"0x0004 0x20000102\""
data_path1 = "/sys/devices/xilinx/accel-i2c/raw_access_data"
addr_path1 = "/sys/devices/xilinx/accel-i2c/raw_access_addr"


i2c_path = "/sys/devices/xilinx/pps-i2c/port"

fault_logger_path = "cd /sys/bus/i2c/devices/8-0060/"
fault_logger_cmd = "dd if=fault_logger_dump bs=128 count=1 status=none | hexdump -C"

fw_cmd = ["asc_fwupd_arm -r --bus 21 --addr 0x60","asc_fwupd_arm -r --bus 21 --addr 0x61","asc_fwupd_arm -r --bus 21 --addr 0x62"]
eeprom_cmd = ["hexdump -C /sys/bus/i2c/devices/21-0060/eeprom","hexdump -C /sys/bus/i2c/devices/21-0061/eeprom","hexdump -C /sys/bus/i2c/devices/21-0062/eeprom"]
cat_crc_cmd = ["cat /sys/bus/i2c/devices/21-0060/crc","cat /sys/bus/i2c/devices/21-0061/crc","cat /sys/bus/i2c/devices/21-0062/crc"]
#### BSP_TC00_Diag_Initialize_And_Version_Check ####
drive_pattern_dict = {
    'sfp_module': 'sfp_module.*',
    '1pps_fpga': '1pps_fpga.*',
    'march_hare_fpga_core': 'march_hare_fpga_core.*',
    'sitime': 'sitime.*',
    'come_cpld': 'come_cpld.*',
    'fan_cpld': 'fan_cpld.*',
    'sys_cpld': 'sys_cpld.*',
    'cls_i2c_client': 'cls_i2c_client.*',
    'ltc4282': 'ltc4282.*',
    'asc10': 'asc10.*'
}
#### BSP_10.1.1.1_INSTALL_DRIVER_TEST ####
DRIVE_VER = 'head /root/driver/releaseNotes |grep Ver'
RMMODE_TOOL = 'rmmod -f *.ko'
RMDRIVE = 'rm -r driver'
MKDIRVE = 'mkdir driver'
DRIVXZ = 'xz -d driver.tar.xz'
DRIVETAR = 'tar -xf driver.tar'
DRIVEINST = './install.sh'
#### BSP_10.1.2.1.3_CPLD_RAW_ACCESS_TEST ####
RAW_ADDR_CMD = 'cat /sys/bus/i2c/drivers/celestica-cpld/19-0060/raw_access_addr'
RAW_DATA_CMD = 'cat /sys/bus/i2c/drivers/celestica-cpld/19-0060/raw_access_data'
RAW_ADDR_RES = '0x00'
RAW_ADDR_TEST = '0x31'
SysCpldObj = SwImage.getSwImage("SYS_CPLD")
SysCpldVer = SysCpldObj.newVersion
write_raw_data = 'echo "0x31 0x00" > /sys/bus/i2c/drivers/celestica-cpld/19-0060/raw_access_data'
write_raw_addr = 'echo "0x31" > /sys/bus/i2c/drivers/celestica-cpld/19-0060/raw_access_addr'
test_raw_data = 'echo "0x00 0x33" > /sys/bus/i2c/drivers/celestica-cpld/19-0060/raw_access_data'
test_raw_addr = 'echo "0x00" > /sys/bus/i2c/drivers/celestica-cpld/19-0060/raw_access_addr'
#### BSP_10.1.3_CONSOLE_LOGGER_DUMP_TEST ####
LOGGER_FOLDER = '/sys/bus/i2c/drivers/celestica-cpld/19-0060'
LOGGER_DUMP_CMD1 = 'dd if=console_logger_dump bs=128 count=1 | hexdump -C'
LOGGER_DUMP_CMD2 = 'dd if=console_logger_dump bs=2048 count=1 | hexdump -C'
LOGGER_RESET_CMD = 'echo 1 > console_logger_reset'
LOGGER_PAUSE_CMD = 'echo 1 > console_logger_pause'
LOGGER_START_CMD = 'echo 0 > console_logger_pause'
UNAME_TOOL = 'uname -r'
FDISK_TOOL = 'fdisk -l'
PAUSE_PATTERN = 'bs'
#### BSP_10.1.5.1_Port_Module_Interrupt_Test ####
i2c_tool = 'i2cset -y -f '
i2c_set_option = ' 0x50 0x41 0x02'
i2c_clear_option = ' 0x50 0x41 0x12'
sfp_tool = 'cel-sfp-test'
sfp_all_status_option = ' --show -t present'
sfp_status_cmd = 'cat /sys/devices/xilinx/pps-i2c/port'
sfp_set_cmd = '/sys/devices/xilinx/pps-i2c/port'
sfp_status_option = '_module_interrupt'
interrupt_value1 = '1'
interrupt_value2 = '0'
sfp_present_option = '_module_present'
sfp_reset_option = '_module_reset'
#### BSP_10.1.6.4_PSU_Voltage_Fault_Test ####
psu_fault_cmd = 'cat /sys/bus/i2c/drivers/celestica-cpld/19-0060/psu_voltage_fault'
psu_up_cmd = 'cat /sys/bus/i2c/drivers/celestica-cpld/19-0060/psu_voltage_up'
#### BSP_10.1.7.1_FAN_MAX_SPEED_TEST ####
DIAG_PATH = '/root/diag'
FAN_TOOL = 'cel-fan-test'
FAN_TOOL_OPTION = ' --show'
fan_50_option = ' -w -t pwm -D 50'
fan_100_option = ' -w -t pwm -D 100'
FAN_MAX_SPEED = '/sys/bus/i2c/drivers/celestica-cpld/19-0060/fan_max_speed'
FAN_MAX_STATUS = 'cat ' + FAN_MAX_SPEED
FAN_255_VALUE = '255'
FAN_100_VALUE = '100'
#### BSP_10.1.8.1_SYSTEM_WATCHDOG_ENABLE_TEST ####
WATCHDOG_ENABLE = '/sys/bus/i2c/drivers/celestica-cpld/19-0060/system_watchdog_enable'
TRIGGER_5_TIME = '5'
TRIGGER_10_TIME = '10'
WATCHDOG_SECOND = '/sys/bus/i2c/drivers/celestica-cpld/19-0060/system_watchdog_seconds'
#### BSP_10.1.8.3_FAN_Watchdog_Enable_Test ####
FAN_WATCHDOG_ENABLE_CMD = '/sys/bus/i2c/drivers/fan_cpld/34-0066/fan_watchdog_enable'
FAN_WATCHDOG_SEC_CMD = '/sys/bus/i2c/drivers/fan_cpld/34-0066/fan_watchdog_seconds'
FAN_50_VALUE = '50'
FAN_60_VALUE = '60'
#### BSP_10.1.10.1_WARM_RESET_TEST ####
WARM_REBOOT_CMD = 'warm-reboot'
COLD_REBOOT_CMD = 'reboot'
#### BSP_10.1.10.3_Fan_CPLD_Reset_Test ####
FAN_RESET_CMD = '/sys/bus/i2c/drivers/celestica-cpld/19-0060/fan_reset'
LED_CPLD_RESET_CMD = '/sys/bus/i2c/drivers/celestica-cpld/19-0060/led_cpld_reset'
FAN_RPM_TOOL = '/sys/bus/i2c/drivers/fan_cpld/34-0066/fan'
FAN_PRM_OPTION1 = '_direction'
FAN_PRM_OPTION2 = '_max'
FAN_PRM_OPTION3 = '_min'
FAN_RPM_PATTER1 = '24700'
FAN_RPM_PATTER2 = '65535'
FAN_RPM_PATTER3 = '1000'
FAN_RPM_PATTER4 = '29700'
FAN_EEPROM_CMD = '/sys/bus/i2c/drivers/fan_cpld/34-0066/fan_board_eeprom_protect'
FAN_HEX_OPTION = '/sys/bus/i2c/drivers/at24/35-0056/eeprom'
FAN_PWM_TOOL = '/sys/bus/i2c/drivers/fan_cpld/34-0066/pwm'
FAN_PWM_PATTERN1 = '127'
FAN_PWM_PATTERN2 = '135'
FAN_PWM_PATTERN3 = '204'
FAN_PWM_PATTERN4 = '229'
#### BSP_10.1.11.1_Swith_Board_EEPROM_Test ####
SYS_EEPROM_CMD = '/sys/bus/i2c/drivers/celestica-cpld/19-0060/system_eeprom_wp'
HEX_OPTION = '/sys/bus/i2c/drivers/at24/24-0056/eeprom'
HEX_TOOL = 'hexdump'
HEX_PATTERN1 = 'TlvInfo'
HEX_PATTERN2 = '1234.fo'
HEX_PATTERN3 = '1234'
HEX_PATTERN4 = 'echo: write error: Connection timed out'
#### BSP_10.1.12.10_FAN_CPLD_RAW_ACCESS_TEST ####
FAN_RAW_DATA = '/sys/bus/i2c/drivers/fan_cpld/34-0066/raw_access_data'
FAN_RAW_ADDR = '/sys/bus/i2c/drivers/fan_cpld/34-0066/raw_access_addr'
FAN_RAW_PATTERN1 = '0x03'
FAN_RAW_PATTERN2 = '0x00'
FAN_RAW_PATTERN3 = '0x02'
#### BSP_10.1.13_I2C_L-ASC10_DRIVER_TEST ####
LASC10_OPTION = '_input'
LASC10_0_VAL = '/sys/bus/i2c/drivers/L-ASC10/32-0060/in'
LASC10_1_VAL = '/sys/bus/i2c/drivers/L-ASC10/32-0061/in'
LASC10_2_VAL = '/sys/bus/i2c/drivers/L-ASC10/32-0062/in'
LASC10_3_VAL = '/sys/bus/i2c/drivers/L-ASC10/11-0060/in'
LASC10_4_VAL = '/sys/bus/i2c/drivers/L-ASC10/11-0061/in'
LASC10_LST = [LASC10_0_VAL, LASC10_1_VAL, LASC10_2_VAL, LASC10_3_VAL, LASC10_4_VAL]
DCDC_TOOL = 'cel-dcdc-test'
DCDC_ALL_OPTION = ' --all'
LASC10_0_VALUE_MIN = ['892', '887', '847', '3106', '3101', '851', '851', '1037', '3135', '10847']
LASC10_0_VALUE_MAX = ['988', '994', '952', '3496', '3490', '1017', '951', '1161', '3490', '13243']
LASC10_1_VALUE_MIN = ['1716', '3137', '2971', '4695', '753', '3101', '3101', '753', '3101', '11273']
LASC10_1_VALUE_MAX = ['1886', '3457', '3637', '5313', '895', '3511', '3490', '869', '3490', '13146']
LASC10_2_VALUE_MIN = ['927', '1114', '1655', '927', '3068', '3068', '0', '0', '0', '0']
LASC10_2_VALUE_MAX = ['1072', '1290', '1909', '1072', '3531', '3531', '0', '0', '0', '0']
LASC10_3_VALUE_MIN = ['1140', '1710', '870', '3135', '745', '570', '1710', '1710', '0', '11400']
LASC10_3_VALUE_MAX = ['1260', '1890', '950', '3465', '885', '630', '1890', '1890', '0', '12600']
LASC10_4_VALUE_MIN = ['2375', '1710', '1710', '770', '950', '1710', '3135', '0', '0', '475']
LASC10_4_VALUE_MAX = ['2625', '1890', '1890', '850', '1050', '1890', '3465', '0', '0', '525']
LASC10_VALUE_MIN_LST = [LASC10_0_VALUE_MIN, LASC10_1_VALUE_MIN, LASC10_2_VALUE_MIN, LASC10_3_VALUE_MIN, LASC10_4_VALUE_MIN]
LASC10_VALUE_MAX_LST = [LASC10_0_VALUE_MAX, LASC10_1_VALUE_MAX, LASC10_2_VALUE_MAX, LASC10_3_VALUE_MAX, LASC10_4_VALUE_MAX]
#### BSP_10.1.14.5_UBOOT_MGMT_TFTP_STRESS_TEST ####
check_uboot_log_pattern = {
    'PCIe5':'pcie@\d+ Root Complex: x4 gen3',
    'AHCI':'32 slots 1 ports 6 Gbps 0x1 impl SATA mode',
    'SystemCPLD':'RESET REASON',
    'COMeCPLD':'RESET REASON'
}
MDIO_TOOL = 'mdio read'
MDIO_OPTION = ' 0 0.21'
UBOOT_ADDRESS = 'setenv ipaddr 192.168.0.12'
UBOOT_SERVERIP = 'setenv serverip 192.168.0.5'
UBOOT_STRESS_FILE = 'tftpboot 0xa0000000 uboot_stress.tar'
UBOOT_RESET_TOOL = 'reset'
#### BSP_10.1.14.6_Uboot_environment_Variable_test ####
SET_ETH1ADDR_CMD = 'setenv eth1addr'
TEST_ETH1ADDR = 'd6:4e:4e:ff:4e:03'
SAVE_ENV1 = 'saveenv'
SAVE_ENV2 = 'savee'
PRINT_ENV = 'printenv'
PRINT_ENV_OPTION = 'ipaddr'
IPADDR_PATTERN1 = 'Error: \"ipaddr\" (not defined)'
IPADDR_PATTERN2 = 'ipaddr=(.*)'
onieObj = SwImage.getSwImage("ONIE_updater")
ONIE_NEW_VER = onieObj.newVersion
TEST_ETH1DICT = {
    'baudrate': '115200',
    'eth1addr': TEST_ETH1ADDR,
    'onie_version': ONIE_NEW_VER
}
ONIE_RESCUE_CMD = 'run onie_rescue'
ONIE_RESCUE_PATTERN = 'Please press Enter to activate this console'
PRINT_ENV2 = 'fw_printenv'
FW_SET_ENV = 'fw_setenv'
TEST_ENV1 = 'testenv1=mytestenv1'
TEST_ENV2 = 'testenv2=mytestenv2'
TEST_ENV3 = 'testenv3=mytestenv3'
TEST_ENV4 = 'testenv4=mytestenv4'
TEST_ENV_LST = [TEST_ENV1, TEST_ENV2, TEST_ENV3, TEST_ENV4]
ENV_DEFAULT_TOOL = 'env default -a'
ENV_DEF_LST = [ENV_DEFAULT_TOOL, SAVE_ENV2, UBOOT_RESET_TOOL]
TEST_PATTERN = ['eth1addr', 'testenv1', 'testenv2', 'testenv3', 'testenv4']
#### BSP_10.1.14.8_Uboot_DHCP_Client_Function_Test ####
SETENV_TOOL = 'setenv'
DHCP_OPTION1 = 'dhcp_user-class arm64-celestica_cs8274-r0_uboot'
DHCP_OPTION2 = 'dhcp_vendor-class-identifier arm64-celestica_cs8274-r0'
#### BSP_10.2.2.1_ASIC_Reset_Test ####
ASIC_RESET_TOOL = '/sys/bus/i2c/drivers/celestica-cpld/19-0060/asic_reset'
I2C_RESET_TOOL = '/sys/bus/i2c/drivers/celestica-cpld/19-0060/i2c_reset'
#### BSP_10.2.3.1_Fan_board_EEPROM_Test ####
FAN_BOARD_CMD = '/sys/bus/i2c/drivers/at24/35-0056/eeprom | hexdump -C'
FAN_BOARD_PATTERN1 = '\|\.\.\.\.\.\.\.\.\.\.\.\.\.\.\.c\|'
FAN_BOARD_PATTERN2 = '\|1234\.*c\|'
FAN_BOARD_FRU_CMD = '/sys/bus/i2c/drivers/at24/35-0056/eeprom'
FAN_ADDR_LST = ['36-0050', '37-0050', '38-0050', '39-0050', '40-0050', '41-0050']
#### BSP_10.2.3.3_Busbar_Board_EEPROM_Test ####
BUSBAR_TOOL = '/sys/bus/i2c/drivers/at24/26-0054/eeprom'
#### BSP_10.2.3.4_COMe_Card_EEPROM_Test ####
COME_EEPROM_TOOL = '/sys/bus/i2c/drivers/come-cpld/4-0060/come_eeprom_wp'
COME_BUS_TOOL = '/sys/bus/i2c/drivers/at24/12-0057/eeprom'
RISER_EEPROM_TOOL = '/sys/bus/i2c/drivers/at24/44-0050/eeprom'
#### BSP_10.2.4.1_Fan_eeprom_Power_Status_Test ####
FAN_POWER_TOOL = '/sys/bus/i2c/drivers/fan_cpld/34-0066/fan_eeprom_power'
FAN_MUX_TOOL = '/sys/bus/i2c/drivers/fan_cpld/34-0066/fan_mux_reset'
#### BSP_10.2.5.1_CPLD2_3_RAW_ACCESS_TEST ####
CPLD2_RAW_DATA = '/sys/bus/i2c/drivers/celestica-cpld/20-0063/raw_access_data'
CPLD2_RAW_ADDR = '/sys/bus/i2c/drivers/celestica-cpld/20-0063/raw_access_addr'
CPLD3_RAW_ADDR = '/sys/bus/i2c/drivers/celestica-cpld/22-0064/raw_access_addr'
CPLD3_RAW_DATA = '/sys/bus/i2c/drivers/celestica-cpld/22-0064/raw_access_data'
CPLD2_RAW_PATTERN1 = '0x00'
CPLD2_RAW_PATTERN2 = '0x06'
CPLD3_RAW_PATTERN1 = '0x05'
CPLD_RAW_pattern1 = '0x01'
CPLD_RAW_pattern2 = '0xab'
CPLD2_LED_TOOL = '/sys/bus/i2c/drivers/celestica-cpld/20-0063/led_enable'
CPLD3_LED_TOOL = '/sys/bus/i2c/drivers/celestica-cpld/22-0064/led_enable'
CPLD2_LED_COLOR = '/sys/bus/i2c/drivers/celestica-cpld/20-0063/led_color'
CPLD3_LED_COLOR = '/sys/bus/i2c/drivers/celestica-cpld/22-0064/led_color'
LED_COLOR_DEFAULT = 'off'
LED_COLOR_RED = 'red'
LED_COLOR_GREEN = 'green'
LED_COLOR_WHITE = 'white'
LED_COLOR_BLUE = 'blue'
#### BSP_10.2.6_LM75_DRIVER_TEST ####
LM75_TOOL = '/sys/bus/i2c/drivers/lm75/'
LM75_OPTION1 = 'temp1_input'
LM75_OPTION2 = 'temp1_max'
LM75_OPTION3 = 'temp1_max_hyst'
LM75_OPTION_LST = [LM75_OPTION1, LM75_OPTION2, LM75_OPTION3]
HWMON_LST = ['hwmon1', 'hwmon3', 'hwmon4', 'hwmon5', 'hwmon2', 'hwmon7', 'hwmon6', 'hwmon8', 'hwmon9', 'hwmon10',
             'hwmon23', 'hwmon26', 'hwmon27', 'hwmon28', 'hwmon25']
LM75_SENSOR_ADDR = ['18-0048', '24-004a', '24-004c', '33-0049', '18-004b', '35-004e', '35-004d', '35-004f']
#### BSP_10.2.7_I2C_SA5604_SENSOR_DRIVER_TEST ####
LM90_TOOL = '/sys/bus/i2c/drivers/lm90'
LM90_OPTION_LST = ['temp1_input', 'temp1_max', 'temp1_max_alarm', 'temp1_min', 'temp1_min_alarm', 'temp1_crit', 'temp1_crit_alarm',
                   'temp1_crit_hyst', 'temp2_input', 'temp2_fault', 'temp2_max', 'temp2_max_alarm', 'temp2_min', 'temp2_min_alarm',
                   'temp2_crit', 'temp2_crit_alarm', 'temp2_crit_hyst', 'temp2_offset']
LM90_SENSOR_ADDR = ['8-0048', '9-0048']
#### BSP_10.2.8.1_I2C_LTC4282_DRIVER_TEST ####
LTC_TOOL = '/sys/bus/i2c/drivers/ltc4282'
LTC_OPTION_LST = ['in1_input', 'curr1_input', 'power1_input']
LTC_ADDR = '27-0058'
#### BSP_10.2.9.1_TPS53679_DRIVER_TEST ####
TPS_TOOL = '/sys/bus/i2c/drivers/tps5xxxx'
TPS_OPTION_LST = ['in1_label', 'in1_input', 'in1_min', 'in1_max', 'in1_min_alarm', 'in1_max_alarm', 'in1_crit', 'in1_crit_alarm',
                  'in1_lcrit', 'in1_lcrit_alarm', 'in2_label', 'in2_input', 'in2_min', 'in2_max', 'in2_min_alarm', 'in2_max_alarm',
                  'in2_crit', 'in2_crit_alarm', 'in2_lcrit', 'in2_lcrit_alarm', 'in2_rated_max', 'in2_rated_min', 'curr1_label',
                  'curr1_input', 'curr1_max', 'curr1_max_alarm', 'curr1_crit', 'curr1_crit_alarm', 'curr2_label', 'curr2_input',
                  'curr2_max', 'curr2_max_alarm', 'curr2_crit', 'curr2_crit_alarm', 'curr2_lcrit', 'curr2_lcrit_alarm', 'power1_label',
                  'power1_input', 'power1_max', 'power1_alarm', 'power2_label', 'power2_input', 'temp1_input', 'temp1_max',
                  'temp1_max_alarm', 'temp1_crit', 'temp1_crit_alarm']
IN_LABEL_LST = ['in1_label', 'in1_input', 'in1_min', 'in1_max', 'in1_min_alarm', 'in1_max_alarm', 'in1_crit', 'in1_crit_alarm',
                'in1_lcrit', 'in1_lcrit_alarm', 'in2_label', 'in2_input', 'in2_min', 'in2_max', 'in2_min_alarm', 'in2_max_alarm',
                'in2_crit', 'in2_crit_alarm', 'in2_lcrit', 'in2_lcrit_alarm', 'in2_rated_max', 'in2_rated_min', 'in3_label',
                'in3_input', 'in3_min', 'in3_max', 'in3_min_alarm', 'in3_max_alarm', 'in3_crit', 'in3_crit_alarm', 'in3_lcrit',
                'in3_lcrit_alarm', 'in3_rated_max', 'in3_rated_min', 'curr1_label', 'curr1_input', 'curr1_max', 'curr1_max_alarm',
                'curr1_crit', 'curr1_crit_alarm', 'curr2_label', 'curr2_input', 'curr2_max', 'curr2_max_alarm', 'curr2_crit',
                'curr2_crit_alarm', 'curr2_lcrit', 'curr2_lcrit_alarm', 'curr3_label', 'curr3_input', 'curr3_max', 'curr3_max_alarm',
                'curr3_crit', 'curr3_crit_alarm', 'curr3_lcrit', 'curr3_lcrit_alarm', 'power1_label', 'power1_input', 'power1_max',
                'power1_alarm', 'power2_label', 'power2_input', 'power3_label', 'power3_input', 'temp1_input', 'temp1_max',
                'temp1_max_alarm', 'temp1_crit', 'temp1_crit_alarm', 'temp1_input', 'temp1_max', 'temp1_max_alarm',
                'temp1_crit', 'temp1_crit_alarm']
IN_MIN_LST = ['in1_label', 'in1_input', 'in1_min', 'in1_max', 'in1_min_alarm', 'in1_max_alarm', 'in1_crit', 'in1_crit_alarm',
              'in1_lcrit', 'in1_lcrit_alarm', 'in2_label', 'in2_input', 'in2_min', 'in2_max', 'in2_min_alarm', 'in2_max_alarm',
              'in2_crit', 'in2_crit_alarm', 'in2_lcrit', 'in2_lcrit_alarm', 'in2_rated_max', 'in2_rated_min', 'in3_label',
              'in3_input', 'in3_min', 'in3_max', 'in3_min_alarm', 'in3_max_alarm', 'in3_crit', 'in3_crit_alarm',
              'in3_lcrit', 'in3_lcrit_alarm', 'in3_rated_max', 'in3_rated_min', 'curr1_label', 'curr1_input', 'curr1_max',
              'curr1_max_alarm', 'curr1_crit', 'curr1_crit_alarm', 'curr2_label', 'curr2_input', 'curr2_max', 'curr2_max_alarm',
              'curr2_crit', 'curr2_crit_alarm', 'curr2_lcrit', 'curr2_lcrit_alarm', 'curr3_label', 'curr3_input', 'curr3_max',
              'curr3_max_alarm', 'curr3_crit', 'curr3_crit_alarm', 'curr3_lcrit', 'curr3_lcrit_alarm', 'power1_label',
              'power1_input', 'power1_max', 'power1_alarm', 'power2_label', 'power2_input', 'power3_label', 'power3_input',
              'temp1_input', 'temp1_max', 'temp1_max_alarm', 'temp1_crit', 'temp1_crit_alarm', 'temp1_input', 'temp1_max',
              'temp1_max_alarm', 'temp1_crit', 'temp1_crit_alarm']
TPS_ADDR = ['28-0062', '29-0066', '30-0068', '14-0071']
DCDC_OPTION_LST = ['in1_label', 'in1_input', 'in1_crit', 'in1_crit_alarm', 'in2_label', 'in2_input', 'in2_alarm', 'in2_rated_min',
                   'curr1_label', 'curr1_input', 'curr1_max', 'curr1_max_alarm', 'curr1_crit', 'curr1_crit_alarm', 'curr2_label',
                   'curr2_input', 'curr2_max', 'curr2_max_alarm', 'curr2_crit', 'curr2_crit_alarm']
#### BSP_10.2.10.1.1_COMe_CPLD_Version_Test ####
COMe_CPLD_TOOL = '/sys/bus/i2c/drivers/come-cpld/4-0060/cpld_version'
COMeObj = SwImage.getSwImage("COME_CPLD")
COMe_NEW_VER = COMeObj.newVersion
Board_VER_TOOL = '/sys/bus/i2c/drivers/come-cpld/4-0060/board_version'
BoardObj = SwImage.getSwImage("Board_version")
Board_NEW_VER = BoardObj.newVersion
#### BSP_10.2.10.1.3_COMe_CPLD_Raw_Access_Test ####
PAGE_SELECT_TOOL = '/sys/bus/i2c/drivers/come-cpld/4-0060/page_select'
PAGE_ADDR = '/sys/bus/i2c/drivers/come-cpld/4-0060/raw_access_addr'
PAGE_DATA = '/sys/bus/i2c/drivers/come-cpld/4-0060/raw_access_data'
PAGE_OPTION = '0xd1'
HRESET_TOOL = '/sys/bus/i2c/drivers/come-cpld/4-0060/hreset'
#### BSP_10.2.11_I2C_MCP3422_ADC_Driver_Test ####
VOLTAGE_RAW = '/sys/bus/i2c/drivers/mcp3422/33-0068/iio:device0/in_voltage0_raw'
VOLTAGE_SCALE = '/sys/bus/i2c/drivers/mcp3422/33-0068/iio:device0/in_voltage0_scale'
VOLTAGE_FREQ = '/sys/bus/i2c/drivers/mcp3422/33-0068/iio:device0/in_voltage_sampling_frequency'
VOLTAGE_AVAIL = '/sys/bus/i2c/drivers/mcp3422/33-0068/iio:device0/in_voltage_scale_available'
VOLTAGE_FREQ_AVAIL = '/sys/bus/i2c/drivers/mcp3422/33-0068/iio:device0/sampling_frequency_available'
I2CFPGA_PRE = '/sys/bus/i2c/drivers/celestica-cpld/19-0060/i2cfpga_present'
#### BSP_10.2.12.2_I2cfpga_Eeprom_Protect_Test ####
I2CFPGA_WRITE_PROTECT = '/sys/bus/i2c/drivers/celestica-cpld/19-0060/i2cfpga_eeprom_write_protect'
I2CFPGA_EEPROM_TOOL = '/sys/bus/i2c/devices/17-0056/eeprom'
I2CFPGA_LM75_TOOL = '/sys/bus/i2c/drivers/celestica-cpld/19-0060/i2cfpga_lm75_interrupt'
#### BSP_10.2.14.1.1_1PPS-I2C-FPGA_Version_Test ####
PPS_VER_TOOL = '/sys/devices/xilinx/pps-i2c/version'
PPS_BORAD_VER_TOOL = '/sys/devices/xilinx/pps-i2c/board_version'
fpagImge = '1PPS_FPGA'
PCB_VER_TOOL = '/sys/devices/xilinx/pps-i2c/pcb_version'
I2C_VER_TOOL = '/sys/devices/xilinx/pps-i2c/image_version'
#### BSP_10.2.14.1.5_1PPS-I2C_Raw_Access_Test ####
I2C_RAW_ACCESS_DATA = '/sys/devices/xilinx/pps-i2c/raw_access_data'
I2C_RAW_ACCESS_ADDR = '/sys/devices/xilinx/pps-i2c/raw_access_addr'
I2C_RAW_PATTERN1 = '0x31000502'
I2C_RAW_PATTERN2 = '0x00000000'
I2C_RAW_PATTERN3 = '0x00667788'
I2C_RAW_PATTERN4 = '0x00001000'
I2C_WRITE_DATA1 = '0x1000'
I2C_WRITE_DATA2 = '0x55667788'
I2C_SCRATCH_TOOL = '/sys/devices/xilinx/pps-i2c/scratch'
I2C_SCRATCH_PATTERN = '0x12345678'
#### BSP_10.2.14.2.1_Port_I2C_Profile_Select_Test ####
PORT_PROFILE_TOOL = '/sys/devices/xilinx/pps-i2c/port'
PORT_PROFILE_OPTION = '_i2c_profile_select'
PORT_PROFILE_PATTERN = '2'
PORT_SPEED_OPTION1 = '_i2c_profile'
PORT_SPEED_OPTION2 = '_speed'
SPEED_PATTERN1 = '100000'
SPEED_PATTERN2 = '400000'
SPEED_PATTERN3 = '1000000'
I2C_CLOCK_OPTION = '_i2c_9_clock'
I2C_MASTER_OPTION = '_i2c_master_reset'
PORT_MASK_OPTION = '_module_interrupt_mask'
PORT_LPMOD_OPTION = '_lpmod'
#### BSP_10.2.16_ASC10_EEPROM_And_CRC_Sysfs_Node_Test ####
ASC10_0_TOOL = 'asc_fwupd_arm -r --bus 32 --addr 0x60'
ASC10_1_TOOL = 'asc_fwupd_arm -r --bus 32 --addr 0x61'
ASC10_2_TOOL = 'asc_fwupd_arm -r --bus 32 --addr 0x62'
ASC10_3_TOOL = 'asc_fwupd_arm -r --bus 11 --addr 0x60'
ASC10_4_TOOL = 'asc_fwupd_arm -r --bus 11 --addr 0x61'
ASC10_TOOL_LST = [ASC10_0_TOOL, ASC10_1_TOOL, ASC10_2_TOOL, ASC10_3_TOOL, ASC10_4_TOOL]
ASC10_0_EEPROM = 'hexdump -C /sys/bus/i2c/drivers/L-ASC10/32-0060/eeprom'
ASC10_1_EEPROM = 'hexdump -C /sys/bus/i2c/drivers/L-ASC10/32-0061/eeprom'
ASC10_2_EEPROM = 'hexdump -C /sys/bus/i2c/drivers/L-ASC10/32-0062/eeprom'
ASC10_3_EEPROM = 'hexdump -C /sys/bus/i2c/drivers/L-ASC10/11-0060/eeprom'
ASC10_4_EEPROM = 'hexdump -C /sys/bus/i2c/drivers/L-ASC10/11-0061/eeprom'
ASC10_EEPROM_LST = [ASC10_0_EEPROM, ASC10_1_EEPROM, ASC10_2_EEPROM, ASC10_3_EEPROM, ASC10_4_EEPROM]
ASC10_0_CRC = '/sys/bus/i2c/drivers/L-ASC10/32-0060/crc'
ASC10_1_CRC = '/sys/bus/i2c/drivers/L-ASC10/32-0061/crc'
ASC10_2_CRC = '/sys/bus/i2c/drivers/L-ASC10/32-0062/crc'
ASC10_3_CRC = '/sys/bus/i2c/drivers/L-ASC10/11-0060/crc'
ASC10_4_CRC = '/sys/bus/i2c/drivers/L-ASC10/11-0061/crc'
ASC10_CRC_LST = [ASC10_0_CRC, ASC10_1_CRC, ASC10_2_CRC, ASC10_3_CRC, ASC10_4_CRC]
#### BSP_10.2.17.1_Conn_Type_Test ####
CONN_TOOL = '/sys/bus/i2c/drivers/cls-sfp/'
CONN_OPTION = '/conn_type'
CONN_PATTERN = 'No separate connector'
EEPROM_LOWER_OPTION = 'eeprom_lower | hexdump -c'
EEPROM_LOWER_PATTERN = '0000000 030   0 002 001'
EEPROM_UPPER_OPTION ='eeprom_upper | hexdump -c'
EEPROM_UPPER_PATTERN = '0000000 030   A   W   S'
EEPROM_UP_PAGE_OPTION = 'eeprom_upper_page_select'
EEPROM_VALID_OPTION ='eeprom_valid'
HIGH_POWER_OPTION = 'high_power_class_enable'
IN1_OPTION = 'in1_highest'
INI_PATTERN = '3296'
IN1_INPUT_OPTION = 'in1_input'
IN1_LOWEST_OPTION = 'in1_lowest'
IN1_MAX_OPTION = 'in1_max'
IN1_MAX_PATTERN = '3565'
IN1_MIN_OPTION = 'in1_min'
IN1_MIN_PATTERN = '3035'
IN1_HISTORY_OPTION = 'in1_reset_history'
LANE_CTLE_OPTION = 'lane1_ctle'
LANE_CTLE_PATTERN = '12'
RX_LOS_OPTION = '_rx_los'
TX_LOS_OPTION = '_tx_los'
TX_POWER_OPTION = '_tx_power_highest'
RX_POWER_OPTION = '_rx_power_highest'
RX_INPUT_OPTION = '_rx_power_input'
TX_INPUT_OPTION = '_tx_power_input'
RX_LOWEST_OPTION = '_rx_power_lowest'
TX_LOWEST_OPTION = '_tx_power_lowest'
CABLE_LENGTH_OPTION = 'length'
CABLE_TYPE_OPTION = 'medium_type'
CABLE_TYPE_PATTERN = '400G-CR8'
MODULE_TYPE_OPTION = 'module_type'
MODULE_TYPE_PATTERN = 'QSFP-DD'
WAVELENGTH_OPTION = 'nominal_wavelength'
WAVELENGTH_PATTERN = '3276'
PORT_NUM_OPTION = 'port_num'
PORT_NUM_PATTERN = '80'
OVERRIDE_OPTION = 'power_override'
POWER_SET_OPTION = 'power_set'
POWERCLASS_OPTION = 'powerclass'
POWERCLASS_PATTERN1 = '1.5'
POWERCLASS_PATTERN2 = '16'
TEMP1_OPTION = 'temp1_highest'
TEMP1_INPUT_OPTION = 'temp1_input'
TEMP1_LABEL_OPTION = 'temp1_label'
TEMP1_LABEL_PATTERN = 'module80Temperature'
TEMP1_LOWEST_OPTION = 'temp1_lowest'
TEMP1_RESET_OPTION = 'temp1_reset_history'
VENDOR_NAME_TOOL = 'vendor_name'
VENDOR_NAME_PATTERN = 'AWS'
VENDOR_PARTNUM_TOOL = 'vendor_part_num'
VENDOR_PARTNUM_PATTERN = 'F0OZZGIGA030A'
VENDOR_REVISION_OPTION = 'vendor_revision_num'
VENDOR_REVISION_PATTERN = '0A'
VENDOR_SERIAL_OPTION = 'vendor_serial_num'
#### BSP_10.1.6.1_PSU_Input_Good_Test ####
PSU1_INPUT_TOOL = '/sys/bus/i2c/drivers/celestica-cpld/19-0060/psu1_input_good'
PSU1_OUTPUT_TOOL = '/sys/bus/i2c/drivers/celestica-cpld/19-0060/psu1_output_good'
PSU1_PRESENT_TOOL = '/sys/bus/i2c/drivers/celestica-cpld/19-0060/psu1_present'
#### BSP_10.1.8.1_System_Watchdog_Enable_Test ####
WATCHDOG_STATUS_TOOL = '/sys/bus/i2c/drivers/celestica-cpld/19-0060/system_watchdog_enable'
COME_WATCHDOG_TOOL = '/sys/bus/i2c/drivers/come-cpld/4-0060/come_watchdog_enable'
RSENSE_TREE_TOOL = 'hd /proc/device-tree/soc/i2c@2010000/pca9548@74/i2c@1/pca9548@72/i2c@1/hotswap@58/rsense'
RSENSE_TREE_PATTERN = '1189'
PORESET_TOOL = '/sys/bus/i2c/drivers/come-cpld/4-0060/poreset'
COME_WATCHDOG_SEC_TOOL = '/sys/bus/i2c/drivers/come-cpld/4-0060/come_watchdog_seconds'
COME_WATCHDOG_ENABLE_TOOL = '/sys/bus/i2c/drivers/come-cpld/4-0060/come_watchdog_enable'
COME_CPLD_PATH = '/sys/bus/i2c/drivers/come-cpld/4-0060/'
MB_CPLD_PATH = '/sys/bus/i2c/drivers/celestica-cpld/19-0060/'
LOGGER_DUMP_TOOL = 'dd if=fault_logger_dump bs=128 count=1 status=none | hexdump -C'
RESET_LOGGER  = 'fault_logger_reset'
PAUSE_LOGGER = 'fault_logger_pause'
BIAS_HIGHEST_OPTION = '_tx_bias_highest'
BIAS_INPUT_OPTION = '_tx_bias_input'
BIAS_LOWEST_OPTION = '_tx_bias_lowest'
TX_DISABLE_OPTION = '_tx_disable'
TX_FAULT_OPTION = '_tx_fault'


