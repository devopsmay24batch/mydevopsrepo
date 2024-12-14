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

# IMPORTANT NOTE:
#   Keep up-to-date Jenkins's SwImages.yaml every time you update it!

import os
import DeviceMgr
from SwImage import SwImage
from Const import BOOT_MODE_UBOOT, BOOT_MODE_DIAGOS, BOOT_MODE_ONIE,ONIE_RESCUE_MODE
from KapokConst import STOP_AUTOBOOT_PROMPT, STOP_AUTOBOOT_KEY


pc_info = DeviceMgr.getServerInfo('PC')
dev_info = DeviceMgr.getDevice()

diagos_mode = BOOT_MODE_DIAGOS
uboot_mode = BOOT_MODE_UBOOT
onie_mode = BOOT_MODE_ONIE

# SwImage shared objects
CPLD = SwImage.getSwImage("CPLD")
UBOOT = SwImage.getSwImage("UBOOT")
# End of SwImage shared objects

uboot_prompt = dev_info.promptUboot

tftp_server_ipv4 = pc_info.managementIP
tftp_interface = dhcp_interface = mgmt_interface = "eth0"
# mgmt_server_ip = pc_info.managementIP

diag_tools_path = "/root/diag"
diag_ld_lib_path = "/root/diag/output"
diag_export_env = "export LD_LIBRARY_PATH=" + diag_ld_lib_path + " && export CEL_DIAG_PATH=" + diag_tools_path + " && "
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
diagos_prompt = dev_info.promptDiagOS

diag_vmetool_arm_path="/root/vmetool_arm"
diag_vmetool_arm_f_command = "./vmetool_arm -f xx_Fan_Board_CPLD_v02.vme"
diag_vmetool_arm_f_patterns = [
    r"",
]
diag_vmetool_arm_command = "./vmetool_arm sys_fpga.vme"
diag_vmetool_arm_patterns = [
    r"",
]

diag_write_mac_addr_command = diag_export_env + "./cel-phy-test"
diag_write_mac_addr_options = "-w -d 1 -t mac -D "
diag_write_mac_addr_patterns = [
    r'(?m)[ \t]*(\./)?cel-phy-test[ \t]+-w[ \t]+-d[ \t]+1[ \t]-t[ \t]+mac[ \t]+-D[ \t]+(?P<MAC>[\w{2}:?]{17})[ \t]*$',
]

warm_reboot_cmd = 'warm-reboot'
cold_reboot_cmd = 'reboot'
hotswap_reboot_cmd = 'hotswap-reboot'
pwrcycle_reboot_cmd = 'pwrcycle-reboot'

diag_read_mac_addr_command = diag_export_env + "./cel-phy-test"
diag_read_mac_addr_options = "-r -d 1 -t mac"
diag_read_mac_addr_patterns = [
    r"(?m)^[ \t]*\'(?P<IF>\w+)\'[ \t]+MAC[ \t]+=[ \t]+(?P<MAC>[\w{2}:?]{17})[ \t]*$",
]

diag_cel_cpld_test_command = "./cel-cpld-test"
diag_cel_cpld_test_all_options = "--all"
diag_cel_cpld_test_all_patterns = [
    r"(?m)^[ \t]*Device:[ \t]+cpld1.*version:[ \t]+(?P<CPLD1_VER>\w+)",
    r"(?m)^[ \t]*Device:[ \t]+cpld2.*version:[ \t]+(?P<CPLD2_VER>\w+)",
    r"(?m)^[ \t]*Device:[ \t]+cpld3.*version:[ \t]+(?P<CPLD3_VER>\w+)",
    r"(?m)^[ \t]*Device:[ \t]+fan_cpld.*version:[ \t]+(?P<CPLD4_VER>[\w\.]+)",
    r"(?m)^[ \t]*CPLD[ \t]+test.*Passed[ \t]*$",
]
diag_cel_cpld_test_dump_d_options = "--dump -d "
diag_cel_cpld_test_dump_d_patterns = [
    r"(?m)^[ \t]*Dump[ \t]+device:[ \t]+cpld\d[ \t]+register",
]
diag_cel_cpld_test_s_d_options = "-s -d "
diag_cel_cpld_test_s_d_patterns = [
    r"(?m)^[ \t]*Device:.*?cpld.*version:[ \t]+(?P<CPLD_VER>\w+)",
    r"(?m)^[ \t]*CPLD[ \t]+Scan.*Passed[ \t]*$",
]
diag_cel_cpld_test_h_options = "--h"
diag_cel_cpld_test_h_patterns = [
    r"(?m)^[ \t]*(U|u)sage",
    r"(?m)^[ \t]*Options[ \t]+are",
    r"(?m)^[ \t]*-r,[ \t]+--read",
    r"(?m)^[ \t]*-w,[ \t]+--write",
    r"(?m)^[ \t]*-d,[ \t]+--dev",
    r"(?m)^[ \t]*-R,[ \t]+--reg",
    r"(?m)^[ \t]*-i,[ \t]+--input",
    r"(?m)^[ \t]*-D,[ \t]+--data",
    r"(?m)^[ \t]*--dump",
    r"(?m)^[ \t]*--all",
    r"(?m)^[ \t]*--width",
    r"(?m)^[ \t]*-s,[ \t]+--scan",  # This option have to a new line
    r"(?m)^[ \t]*-V,[ \t]+--verbose",
    r"(?m)^[ \t]*-v,[ \t]+--verion",
    r"(?m)^[ \t]*-h,[ \t]+--help",
    r"",
    r"(?m)^[ \t]*Example",
    r"(?m)^[ \t]*-r[ \t]+-d[ \t]+\d[ \t]+-i[ \t]+name",
    r"(?m)^[ \t]*-w[ \t]+-d[ \t]+\d[ \t]+-i[ \t]+name[ \t]+-D[ \t]+xxx",
    r"(?m)^[ \t]*-w[ \t]+-d[ \t]+\d[ \t]+-R[ \t]+\dx\d[ \t]+-D[ \t]\dx\d",
    r"(?m)^[ \t]*-s[ \t]+-d[ \t]+\d",
    r"(?m)^[ \t]*--dump[ \t]+-d[ \t]+\d",
    r"(?m)^[\[\w]+@[\w-]+ [~\w/\]]+(\$|#)[ \t]*$"  # End of menu
]

diag_cat_board_version_options = "/sys/bus/i2c/devices/15-0060/board_version"
diag_cat_board_version_patterns = [
    r"(?m)^[ \t]*(?P<BOARD_VERSION>\w+)[ \t]*$",
]
qsfp_optical_cmd_1 = 'QSFP_Optical_Module_ResetL_Signal_Eric_ELB_Test.sh'
qsfp_optical_pattern_1 = ['QSFP Optical Module ResetL Signal Test: Passed']
qsfp_optical_cmd = 'QSFP_Optical_Module_LPMode_Signal_Eric_ELB_Test.sh'
qsfp_optical_pattern = ['QSFP Optical Module LPMode Signal Test: Passed']
cat_tool = 'cat'
mtd_cat_option = '/proc/mtd'
mtd_cat_pattern = ['.*dev.*size.*erasesize.*name.*']
diag_cel_pci_test_command = "./cel-pci-test"
diag_cel_pci_test_all_options = "--all"
diag_cel_pci_test_all_table_pattern = [
    r"(?m)^[ \t]*(?P<ID>\d+)[ \t\|]+(?P<NAME>(?:\w+\ ?)*\w+)[ \t\|]+(?P<NUMBER1>\w+:\w+\.\w)[ \t\|]+(?P<VID_PID>\w+:\w+)[ \t\|]+(\w+\ ?)*\ (?P<RESULT>\w+)[ \t]*$",
    # r"(?m)^[ \t]*(?P<ID1>\d+)[ \t\|]+(?P<NAME1>(?:\w+\ ?)*\w+)[ \t\|]+(?P<NUMBER1>\w+:\w+\.\w)[ \t\|]+(?P<VID_PID1>\w+:\w+)[ \t\|]+(\w+\ ?)*\ (?P<RESULT1>\w+)[ \t]*$",
    # r"(?m)^[ \t]*(?P<ID2>\d+)[ \t\|]+(?P<NAME2>(?:\w+\ ?)*\w+)[ \t\|]+(?P<NUMBER2>\w+:\w+\.\w)[ \t\|]+(?P<VID_PID2>\w+:\w+)[ \t\|]+(\w+\ ?)*\ (?P<RESULT2>\w+)[ \t]*$"
    # r"(?m)^[ \t]*(?P<ID3>\d+)[ \t\|]+(?P<NAME3>(?:\w+\ ?)*\w+)[ \t\|]+(?P<NUMBER3>\w+:\w+\.\w)[ \t\|]+(?P<VID_PID3>\w+:\w+)[ \t\|]+(\w+\ ?)*\ (?P<RESULT3>\w+)[ \t]*$"
    # r"(?m)^[ \t]*(?P<ID4>\d+)[ \t\|]+(?P<NAME4>(?:\w+\ ?)*\w+)[ \t\|]+(?P<NUMBER4>\w+:\w+\.\w)[ \t\|]+(?P<VID_PID4>\w+:\w+)[ \t\|]+(\w+\ ?)*\ (?P<RESULT4>\w+)[ \t]*$"
    # r"(?m)^[ \t]*(?P<ID5>\d+)[ \t\|]+(?P<NAME5>(?:\w+\ ?)*\w+)[ \t\|]+(?P<NUMBER5>\w+:\w+\.\w)[ \t\|]+(?P<VID_PID5>\w+:\w+)[ \t\|]+(\w+\ ?)*\ (?P<RESULT5>\w+)[ \t]*$"
    # r"(?m)^[ \t]*(?P<ID6>\d+)[ \t\|]+(?P<NAME6>(?:\w+\ ?)*\w+)[ \t\|]+(?P<NUMBER6>\w+:\w+\.\w)[ \t\|]+(?P<VID_PID6>\w+:\w+)[ \t\|]+(\w+\ ?)*\ (?P<RESULT6>\w+)[ \t]*$"
    # r"(?m)^[ \t]*(?P<ID7>\d+)[ \t\|]+(?P<NAME7>(?:\w+\ ?)*\w+)[ \t\|]+(?P<NUMBER7>\w+:\w+\.\w)[ \t\|]+(?P<VID_PID7>\w+:\w+)[ \t\|]+(\w+\ ?)*\ (?P<RESULT7>\w+)[ \t]*$"
    # r"(?m)^[ \t]*(?P<ID8>\d+)[ \t\|]+(?P<NAME8>(?:\w+\ ?)*\w+)[ \t\|]+(?P<NUMBER8>\w+:\w+\.\w)[ \t\|]+(?P<VID_PID8>\w+:\w+)[ \t\|]+(\w+\ ?)*\ (?P<RESULT8>\w+)[ \t]*$"
    # r"(?m)^[ \t]*(?P<ID9>\d+)[ \t\|]+(?P<NAME9>(?:\w+\ ?)*\w+)[ \t\|]+(?P<NUMBER9>\w+:\w+\.\w)[ \t\|]+(?P<VID_PID9>\w+:\w+)[ \t\|]+(\w+\ ?)*\ (?P<RESULT9>\w+)[ \t]*$"
    # r"(?m)^[ \t]*(?P<ID10>\d+)[ \t\|]+(?P<NAME10>(?:\w+\ ?)*\w+)[ \t\|]+(?P<NUMBER10>\w+:\w+\.\w)[ \t\|]+(?P<VID_PID10>\w+:\w+)[ \t\|]+(\w+\ ?)*\ (?P<RESULT10>\w+)[ \t]*$"
    # r"(?m)^[ \t]*(?P<ID11>\d+)[ \t\|]+(?P<NAME11>(?:\w+\ ?)*\w+)[ \t\|]+(?P<NUMBER11>\w+:\w+\.\w)[ \t\|]+(?P<VID_PID11>\w+:\w+)[ \t\|]+(\w+\ ?)*\ (?P<RESULT11>\w+)[ \t]*$"
    # r"(?m)^[ \t]*(?P<ID12>\d+)[ \t\|]+(?P<NAME12>(?:\w+\ ?)*\w+)[ \t\|]+(?P<NUMBER12>\w+:\w+\.\w)[ \t\|]+(?P<VID_PID12>\w+:\w+)[ \t\|]+(\w+\ ?)*\ (?P<RESULT12>\w+)[ \t]*$"
    # r"(?m)^[ \t]*(?P<ID13>\d+)[ \t\|]+(?P<NAME13>(?:\w+\ ?)*\w+)[ \t\|]+(?P<NUMBER13>\w+:\w+\.\w)[ \t\|]+(?P<VID_PID13>\w+:\w+)[ \t\|]+(\w+\ ?)*\ (?P<RESULT13>\w+)[ \t]*$"
    # r"(?m)^[ \t]*(?P<ID14>\d+)[ \t\|]+(?P<NAME14>(?:\w+\ ?)*\w+)[ \t\|]+(?P<NUMBER14>\w+:\w+\.\w)[ \t\|]+(?P<VID_PID14>\w+:\w+)[ \t\|]+(\w+\ ?)*\ (?P<RESULT14>\w+)[ \t]*$"
]

fan_ctrl_tool = 'cel-fan-test'
fan_ctrl_option = '--test -t fan_ctrl'
fan_ctrl_test_pattern = ['INFO:.*Current.*PWM=.*', 'INFO:.*temp_offset.*pwm=.*', 'INFO.*Inlet sensor.*', 'INFO:.*PID.*']
fan_wdt_pwm_pattern1 = ['.*PWM\s+\|.*\|.*\|.*127']
fan_wdt_pwm_pattern2 = ['.*PWM\s+\|.*\|.*\|.*255']
fan_wdt_pwm_pattern1 = fan_wdt_pwm_pattern1 * 12
fan_wdt_pwm_pattern2 = fan_wdt_pwm_pattern2 * 12
pattern_of_option4 = ['Id.*Name.*Type.*Ch.*Dev Path',
                      '1.*asc10-0.*ASC.*/sys/bus/i2c/devices/.*',
                      '2.*asc10-1.*ASC.*/sys/bus/i2c/devices/.*',
                      '3.*VCORE.*tps53647.*/sys/bus/i2c/devices/.*',
                      '4.*asc10-0.*ASC.*/sys/bus/i2c/devices/.*',
                      '5.*asc10-1.*ASC.*/sys/bus/i2c/devices/.*',
                      '6.*asc10-2.*ASC.*/sys/bus/i2c/devices/.*',
                      '7.*SW-VDDCORE.*tps536c7.*/sys/bus/i2c/devices/.*',
                      '8.*SW-AVDD/SW-3V3-R.*tps53688.*/sys/bus/i2c/devices/.*',
                      '9.*SW-AVDD-H/SW-3V3-L.*tps53688.*/sys/bus/i2c/devices/.*',
                     ]
diag_pcie_device_table = {
    "00:01.0" : {
        "ID" : r"\d",
        "NAME" : "Ethernet controller",
        "VID_PID" : "1c36:0001"
    },
    "00:03.0" : {
        "ID" : r"\d",
        "NAME" : "Ethernet controller",
        "VID_PID" : "1c36:0001"
    },
    "00:06.0" : {
        "ID" : r"\d",
        "NAME" : "System peripheral",
        "VID_PID" : "1c36:0022"
    },
    "00:08.0" : {
        "ID" : r"\d",
        "NAME" : "SATA controller",
        "VID_PID" : "1c36:0031"
    },
    "00:09.0" : {
        "ID" : r"\d",
        "NAME" : "SATA controller",
        "VID_PID" : "1c36:0031"
    },
    "00:0a.0" : {
        "ID" : r"\d",
        "NAME" : "SATA controller",
        "VID_PID" : "1c36:0031"
    },
    "00:0b.0" : {
        "ID" : r"\d",
        "NAME" : "SATA controller",
        "VID_PID" : "1c36:0031"
    },
    "00:0c.0" : {
        "ID" : r"\d",
        "NAME" : "SATA controller",
        "VID_PID" : "1c36:0031"
    },
    "00:0d.0" : {
        "ID" : r"\d",
        "NAME" : "SATA controller",
        "VID_PID" : "1c36:0031"
    },
    "00:0e.0" : {
        "ID" : r"\d",
        "NAME" : "SATA controller",
        "VID_PID" : "1c36:0031"
    },
    "00:0f.0" : {
        "ID" : r"\d",
        "NAME" : "SATA controller",
        "VID_PID" : "1c36:0031"
    },
    "00:10.0" : {
        "ID" : r"\d",
        "NAME" : "System peripheral  ",
        "VID_PID" : "1c36:0022"
    },
    "00:00.0" : {
        "ID" : r"\d",
        "NAME" : "PCI_bridge",
        "VID_PID" : "1c36:0031"
    },
    "01:00.0" : {
        "ID" : r"\d",
        "NAME" : "Innovium Ethernet controller",
        "VID_PID" : "1d98:1b58"
    },
}

psu_test_all_fail_pattern = r"(?mi)^[ \t]*(?P<psu_fail_number>\d+)[ \t]*\|.*FAILED"

temp_test_all_fail_pattern = r"(?mi)^[ \t]*(?P<number>\d+)(?:[ \t]*\|[ \t]*[\w\-\.\d]+[ \t]*){6}\|[ \t]*(?:(?!Passed).)*$"

cpld_fan_d4_fail_pattern = r"(?mi)^[ \t]*(?P<number>\d+).*\|[ \t]*(?:(?!Passed).)*$"

i2c_diagnose_loopback_fail_pattern = r"(?mi)^[ \t]*(?P<number>\d+).*\|[ \t]*(?:(?!Passed).)*$"

i2c_bus_scan_stress_pass_pattern = "I2C.*test.*:.*Passed"

diagnose_test_all_fail_pattern = r"(?mi)^[ \t]*(?P<number>\w+\-\w+\-\w+).*\|[ \t]*(?:(?!Passed).)*$"

diagnose_pci_detect_fail_pattern = r"(?P<PCIE_PASS>PCIe\s+test\s+:\s+Passed)"

cpld_test_all_patterns = [
    r"(?mi)^[ \t]*Device:[ \t]*(?P<syscpld_name>\w+).*type:[ \t]*(?P<syscpld_type>\w+).*addr:[ \t](?P<syscpld_addr>\w+).*version:[ \t]*(?P<syscpld_ver>[\w\.]+)",
    r"(?mi)^[ \t]*Device:[ \t]*(?P<ledcpld1_name>\w+).*type:[ \t]*(?P<ledcpld1_type>\w+).*addr:[ \t](?P<ledcpld1_addr>\w+).*version:[ \t]*(?P<ledcpld1_ver>[\w\.]+)",
    r"(?mi)^[ \t]*Device:[ \t]*(?P<ledcpld2_name>\w+).*type:[ \t]*(?P<ledcpld2_type>\w+).*addr:[ \t](?P<ledcpld2_addr>\w+).*version:[ \t]*(?P<ledcpld2_ver>[\w\.]+)",

    # Now, the FANCPLD version is displaying wrong format 0.D not 0xD
    r"(?mi)^[ \t]*Device:[ \t]*(?P<fancpld_name>\w+).*type:[ \t]*(?P<fancpld_type>\w+).*addr:[ \t](?P<fancpld_addr>\w+).*version:[ \t]*\d\.(?P<fancpld_ver>\d)",
]

cpld_test_all_new_versions = {
    "syscpld_ver" : '0x{0:x}'.format(int(CPLD.newVersion["SYSCPLD"], base=16)),
    "ledcpld1_ver" : '0x{0:x}'.format(int(CPLD.newVersion["SWLEDCPLD1"], base=16)),
    "ledcpld2_ver" : '0x{0:x}'.format(int(CPLD.newVersion["SWLEDCPLD2"], base=16)),

    # Now, the FANCPLD version is displaying wrong format! Need to edit it like above
    "fancpld_ver" : str(CPLD.newVersion["FANCPLD"]),
}

fan_pwm_rpm_all_patterns = [
    "Fan.*test.*:.*Passed",
]

fan_pwm_rpm_show_patterns = [
    r"(?m)^[ \t]*fan-1 Front",
    r"(?m)^[ \t]*PWM[ \t]+\|[ \t]+(?P<fan1_front_pwm_min>\d+)[ \t]+\|[ \t]+(?P<fan1_front_pwm_max>\d+)[[ \t]+\|[ \t]+(?P<fan1_front_pwm_value>\d+)([ \t]*\|[ \t]*(?P<fan1_front_pwm_result>\w+))?[ \t]*$",
    r"(?m)^[ \t]*RPM[ \t]+\|[ \t]+(?P<fan1_front_rpm_min>\d+)[ \t]+\|[ \t]+(?P<fan1_front_rpm_max>\d+)[[ \t]+\|[ \t]+(?P<fan1_front_rpm_value>\d+)([ \t]*\|[ \t]*(?P<fan1_front_rpm_result>\w+))?[ \t]*$",
    r"(?m)^[ \t]*fan-1 Panel",
    r"(?m)^[ \t]*PWM[ \t]+\|[ \t]+(?P<fan1_panel_pwm_min>\d+)[ \t]+\|[ \t]+(?P<fan1_panel_pwm_max>\d+)[[ \t]+\|[ \t]+(?P<fan1_panel_pwm_value>\d+)([ \t]*\|[ \t]*(?P<fan1_panel_pwm_result>\w+))?[ \t]*$",
    r"(?m)^[ \t]*RPM[ \t]+\|[ \t]+(?P<fan1_panel_rpm_min>\d+)[ \t]+\|[ \t]+(?P<fan1_panel_rpm_max>\d+)[[ \t]+\|[ \t]+(?P<fan1_panel_rpm_value>\d+)([ \t]*\|[ \t]*(?P<fan1_panel_rpm_result>\w+))?[ \t]*$",
    r"(?m)^[ \t]*fan-2 Front",
    r"(?m)^[ \t]*PWM[ \t]+\|[ \t]+(?P<fan2_front_pwm_min>\d+)[ \t]+\|[ \t]+(?P<fan2_front_pwm_max>\d+)[[ \t]+\|[ \t]+(?P<fan2_front_pwm_value>\d+)([ \t]*\|[ \t]*(?P<fan2_front_pwm_result>\w+))?[ \t]*$",
    r"(?m)^[ \t]*RPM[ \t]+\|[ \t]+(?P<fan2_front_rpm_min>\d+)[ \t]+\|[ \t]+(?P<fan2_front_rpm_max>\d+)[[ \t]+\|[ \t]+(?P<fan2_front_rpm_value>\d+)([ \t]*\|[ \t]*(?P<fan2_front_rpm_result>\w+))?[ \t]*$",
    r"(?m)^[ \t]*fan-2 Panel",
    r"(?m)^[ \t]*PWM[ \t]+\|[ \t]+(?P<fan2_panel_pwm_min>\d+)[ \t]+\|[ \t]+(?P<fan2_panel_pwm_max>\d+)[[ \t]+\|[ \t]+(?P<fan2_panel_pwm_value>\d+)([ \t]*\|[ \t]*(?P<fan2_panel_pwm_result>\w+))?[ \t]*$",
    r"(?m)^[ \t]*RPM[ \t]+\|[ \t]+(?P<fan2_panel_rpm_min>\d+)[ \t]+\|[ \t]+(?P<fan2_panel_rpm_max>\d+)[[ \t]+\|[ \t]+(?P<fan2_panel_rpm_value>\d+)([ \t]*\|[ \t]*(?P<fan2_panel_rpm_result>\w+))?[ \t]*$",
    r"(?m)^[ \t]*fan-3 Front",
    r"(?m)^[ \t]*PWM[ \t]+\|[ \t]+(?P<fan3_front_pwm_min>\d+)[ \t]+\|[ \t]+(?P<fan3_front_pwm_max>\d+)[[ \t]+\|[ \t]+(?P<fan3_front_pwm_value>\d+)([ \t]*\|[ \t]*(?P<fan3_front_pwm_result>\w+))?[ \t]*$",
    r"(?m)^[ \t]*RPM[ \t]+\|[ \t]+(?P<fan3_front_rpm_min>\d+)[ \t]+\|[ \t]+(?P<fan3_front_rpm_max>\d+)[[ \t]+\|[ \t]+(?P<fan3_front_rpm_value>\d+)([ \t]*\|[ \t]*(?P<fan3_front_rpm_result>\w+))?[ \t]*$",
    r"(?m)^[ \t]*fan-3 Panel",
    r"(?m)^[ \t]*PWM[ \t]+\|[ \t]+(?P<fan3_panel_pwm_min>\d+)[ \t]+\|[ \t]+(?P<fan3_panel_pwm_max>\d+)[[ \t]+\|[ \t]+(?P<fan3_panel_pwm_value>\d+)([ \t]*\|[ \t]*(?P<fan3_panel_pwm_result>\w+))?[ \t]*$",
    r"(?m)^[ \t]*RPM[ \t]+\|[ \t]+(?P<fan3_panel_rpm_min>\d+)[ \t]+\|[ \t]+(?P<fan3_panel_rpm_max>\d+)[[ \t]+\|[ \t]+(?P<fan3_panel_rpm_value>\d+)([ \t]*\|[ \t]*(?P<fan3_panel_rpm_result>\w+))?[ \t]*$",
    r"(?m)^[ \t]*fan-4 Front",
    r"(?m)^[ \t]*PWM[ \t]+\|[ \t]+(?P<fan4_front_pwm_min>\d+)[ \t]+\|[ \t]+(?P<fan4_front_pwm_max>\d+)[[ \t]+\|[ \t]+(?P<fan4_front_pwm_value>\d+)([ \t]*\|[ \t]*(?P<fan4_front_pwm_result>\w+))?[ \t]*$",
    r"(?m)^[ \t]*RPM[ \t]+\|[ \t]+(?P<fan4_front_rpm_min>\d+)[ \t]+\|[ \t]+(?P<fan4_front_rpm_max>\d+)[[ \t]+\|[ \t]+(?P<fan4_front_rpm_value>\d+)([ \t]*\|[ \t]*(?P<fan4_front_rpm_result>\w+))?[ \t]*$",
    r"(?m)^[ \t]*fan-4 Panel",
    r"(?m)^[ \t]*PWM[ \t]+\|[ \t]+(?P<fan4_panel_pwm_min>\d+)[ \t]+\|[ \t]+(?P<fan4_panel_pwm_max>\d+)[[ \t]+\|[ \t]+(?P<fan4_panel_pwm_value>\d+)([ \t]*\|[ \t]*(?P<fan4_panel_pwm_result>\w+))?[ \t]*$",
    r"(?m)^[ \t]*RPM[ \t]+\|[ \t]+(?P<fan4_panel_rpm_min>\d+)[ \t]+\|[ \t]+(?P<fan4_panel_rpm_max>\d+)[[ \t]+\|[ \t]+(?P<fan4_panel_rpm_value>\d+)([ \t]*\|[ \t]*(?P<fan4_panel_rpm_result>\w+))?[ \t]*$",
    r"(?m)^[ \t]*fan-5 Front",
    r"(?m)^[ \t]*PWM[ \t]+\|[ \t]+(?P<fan5_front_pwm_min>\d+)[ \t]+\|[ \t]+(?P<fan5_front_pwm_max>\d+)[[ \t]+\|[ \t]+(?P<fan5_front_pwm_value>\d+)([ \t]*\|[ \t]*(?P<fan5_front_pwm_result>\w+))?[ \t]*$",
    r"(?m)^[ \t]*RPM[ \t]+\|[ \t]+(?P<fan5_front_rpm_min>\d+)[ \t]+\|[ \t]+(?P<fan5_front_rpm_max>\d+)[[ \t]+\|[ \t]+(?P<fan5_front_rpm_value>\d+)([ \t]*\|[ \t]*(?P<fan5_front_rpm_result>\w+))?[ \t]*$",
    r"(?m)^[ \t]*fan-5 Panel",
    r"(?m)^[ \t]*PWM[ \t]+\|[ \t]+(?P<fan5_panel_pwm_min>\d+)[ \t]+\|[ \t]+(?P<fan5_panel_pwm_max>\d+)[[ \t]+\|[ \t]+(?P<fan5_panel_pwm_value>\d+)([ \t]*\|[ \t]*(?P<fan5_panel_pwm_result>\w+))?[ \t]*$",
    r"(?m)^[ \t]*RPM[ \t]+\|[ \t]+(?P<fan5_panel_rpm_min>\d+)[ \t]+\|[ \t]+(?P<fan5_panel_rpm_max>\d+)[[ \t]+\|[ \t]+(?P<fan5_panel_rpm_value>\d+)([ \t]*\|[ \t]*(?P<fan5_panel_rpm_result>\w+))?[ \t]*$",
    r"(?m)^[ \t]*fan-6 Front",
    r"(?m)^[ \t]*PWM[ \t]+\|[ \t]+(?P<fan6_front_pwm_min>\d+)[ \t]+\|[ \t]+(?P<fan6_front_pwm_max>\d+)[[ \t]+\|[ \t]+(?P<fan6_front_pwm_value>\d+)([ \t]*\|[ \t]*(?P<fan6_front_pwm_result>\w+))?[ \t]*$",
    r"(?m)^[ \t]*RPM[ \t]+\|[ \t]+(?P<fan6_front_rpm_min>\d+)[ \t]+\|[ \t]+(?P<fan6_front_rpm_max>\d+)[[ \t]+\|[ \t]+(?P<fan6_front_rpm_value>\d+)([ \t]*\|[ \t]*(?P<fan6_front_rpm_result>\w+))?[ \t]*$",
    r"(?m)^[ \t]*fan-6 Panel",
    r"(?m)^[ \t]*PWM[ \t]+\|[ \t]+(?P<fan6_panel_pwm_min>\d+)[ \t]+\|[ \t]+(?P<fan6_panel_pwm_max>\d+)[[ \t]+\|[ \t]+(?P<fan6_panel_pwm_value>\d+)([ \t]*\|[ \t]*(?P<fan6_panel_pwm_result>\w+))?[ \t]*$",
    r"(?m)^[ \t]*RPM[ \t]+\|[ \t]+(?P<fan6_panel_rpm_min>\d+)[ \t]+\|[ \t]+(?P<fan6_panel_rpm_max>\d+)[[ \t]+\|[ \t]+(?P<fan6_panel_rpm_value>\d+)([ \t]*\|[ \t]*(?P<fan6_panel_rpm_result>\w+))?[ \t]*$",
]

i2c_devices_tree = {
    "CD8200_FAN_CPLD" : {
        "PATH" : "/sys/bus/i2c/devices/5-0066",
    },
}

diag_tools_cel_fan_test_show_current_pwm_patterns = [
    r"(?m)^[ \t]+PWM.*?\|.*?\|.*\|[ \t]+(?P<fan1_front_current_rpm>\d+)",
    r"(?m)^[ \t]+PWM.*?\|.*?\|.*\|[ \t]+(?P<fan1_panel_current_rpm>\d+)",

    r"(?m)^[ \t]+PWM.*?\|.*?\|.*\|[ \t]+(?P<fan2_front_current_rpm>\d+)",
    r"(?m)^[ \t]+PWM.*?\|.*?\|.*\|[ \t]+(?P<fan2_panel_current_rpm>\d+)",

    r"(?m)^[ \t]+PWM.*?\|.*?\|.*\|[ \t]+(?P<fan3_front_current_rpm>\d+)",
    r"(?m)^[ \t]+PWM.*?\|.*?\|.*\|[ \t]+(?P<fan3_panel_current_rpm>\d+)",

    r"(?m)^[ \t]+PWM.*?\|.*?\|.*\|[ \t]+(?P<fan4_front_current_rpm>\d+)",
    r"(?m)^[ \t]+PWM.*?\|.*?\|.*\|[ \t]+(?P<fan4_panel_current_rpm>\d+)",

    r"(?m)^[ \t]+PWM.*?\|.*?\|.*\|[ \t]+(?P<fan5_front_current_rpm>\d+)",
    r"(?m)^[ \t]+PWM.*?\|.*?\|.*\|[ \t]+(?P<fan5_panel_current_rpm>\d+)",

    r"(?m)^[ \t]+PWM.*?\|.*?\|.*\|[ \t]+(?P<fan6_front_current_rpm>\d+)",
    r"(?m)^[ \t]+PWM.*?\|.*?\|.*\|[ \t]+(?P<fan6_panel_current_rpm>\d+)",

    r"(?m)^[ \t]+PWM.*?\|.*?\|.*\|[ \t]+(?P<fan7_front_current_rpm>\d+)",
    r"(?m)^[ \t]+PWM.*?\|.*?\|.*\|[ \t]+(?P<fan7_panel_current_rpm>\d+)",
]

mtd_uboot_partition_pattern = r"(?m)^(?P<mtd_number>mtd0): (?P<mtd_size>\w+) (?P<mtd_erase_size>\w+) \"(?P<mtd_name>\w+)\"$"
mtd_uboot_boot_img_download_location = UBOOT.hostImageDir
mtd_uboot_boot_img_file = UBOOT.newImage
mtd_uboot_boot_img_save_location = UBOOT.localImageDir

qsfp_dd_port_bus_32_modules = {
    1  : 37, 2  : 38, 3  : 35, 4  : 36, 5  : 41, 6  : 40, 7  : 50, 8  : 39,
    9  : 47, 10 : 46, 11 : 49, 12 : 45, 13 : 44, 14 : 48, 15 : 42, 16 : 43,
    17 : 60, 18 : 66, 19 : 63, 20 : 59, 21 : 64, 22 : 61, 23 : 56, 24 : 65,
    25 : 62, 26 : 57, 27 : 51, 28 : 58, 29 : 53, 30 : 55, 31 : 54, 32 : 52,
}

tools_script_stress_path = "/root/tools/stress_test"

ssd_stress_patterns = [
    r"(?m)^[ \t]*Run[ \t]*status[ \t]*group[ \t]*(?P<group_number>\d+)",
    r"(?m)^[ \t]*Disk[ \t]*stats",
    r"(?m)^[ \t]*(?P<ssd_name>\w+):",
]

##################==============================================================================##################
##### DIAG_TC00_Diag_Initialize_And_Version_Check #####
drive_pattern = {
        "psu_dps800"     : "psu_dps800.*",
        "sfp_module"     : "sfp_module.*",
        "pktgen"         : "pktgen.*",
        "mcp3422"        : "mcp3422.*",
        "ir35215"        : "ir35215.*",
        "asc10"          : "asc10.*",
        "i2c_sc18is600"  : "i2c_sc18is600.*",
        "fan_cpld"       : "fan_cpld.*",
        "sys_cpld"       : "sys_cpld.*",
        "cls_i2c_client" : "cls_i2c_client.*",
        "pmbus_core"     : "pmbus_core.*"
        }

drive_pattern_tianhe = {
        "sfp_module"     : "sfp_module.*",
        "1pps_fpga"     : "1pps_fpga.*",
        "march_hare_fpga_core"  : "march_hare_fpga_core.*",
        "come_cpld"        : "come_cpld.*",
        "fan_cpld"        : "fan_cpld.*",
        "sys_cpld"          : "sys_cpld.*",
        "cls_i2c_client"  : "cls_i2c_client.*",
        "ltc4282"       : "ltc4282.*",
        "asc10"       : "asc10.*"
}

##### DIAG_TC01_POST_Test #####
export_cmd_list = ['export LD_LIBRARY_PATH=/root/diag/output', 'export CEL_DIAG_PATH=/root/diag']
get_hw_version_path = '/root/diag'
get_hw_versions_tool = 'cel-system-test'
get_hw_versions_option = '--all'
hw_version_dict = {'uc_app': '2.1.14', 'uc_bl': '2.28', 'asc1': 'none', 'asc2': 'none'}

post_test_pattern = ['DRAM:.*8 GiB', 'SF: Detected .* with page size 256 Bytes, erase size 4 KiB, total 32 MiB',
                     'Board config ID: CS8260', 'PCIE_0: Link up. Speed 8GT/s Width x4',
                     '.*01:00.0.*1d98:1b58.*Network controller',
                     'PCIE_1: Link up. Speed 5GT/s Width x1', '.*02:00.0.*Memory controller',
                     'AHCI 0001.0300 32 slots 4 ports 6 Gbps 0xf impl SATA mode', r'Model.*CS82\d0\-32X\-DC\-11', 'Revision: R0A']

post_test_pattern_tianhe = [
    r'DRAM:[ \t]+\d\.\d GiB',
    r'SF: Detected .* with page size \d+ Bytes, erase size \d+ KiB, total \d+ MiB',
    r'AHCI \d{4}\.\d{4} \d{2} slots \d ports \d Gbps 0x\d impl SATA mode',
    r'Model[ \t]+\w+\d+\-32X\-DC\-(11|42)',
    r'Revision[ \t]+R0B'
]

##### DIAG_TC02_Boot-up_Image_Updating(Only for NPI stage) #####
ipaddr = '192.168.0.200'
serverip = pc_info.managementIP
get_versions_cmd = 'get_versions'
ubootImgHostPath = UBOOT.hostImageDir
ubootImgFile = UBOOT.newImage
ubootImgUnitPath = UBOOT.localImageDir
ubootDevice = '/dev/mtd0'
flashTool = 'flashcp'
uboot_pattern = r'Verifying kb:[ \t]+\d+/\d+[ \t]+\(100%\)'


##### DIAG_TC03_CPLD_Image_Updating(Only for NPI stage) #####
vmetool = "vmetool_arm "
vmetool_path = "/root/fw"
flash_cmd = "flashcp"
device = "/dev/mtd5"

##### DIAG_TC05_#####
check_uart_cmd = ['i2cset -f -y 15 0x60 0x05 0x84']

##### DIAG_TC07_Switch_Board_EEPROM_Burning #####
eeprom_burning_cmd = [
            "cd /root/diag",
            "export LD_LIBRARY_PATH=/root/diag/output",
            "export CEL_DIAG_PATH=/root/diag",
            "i2cset -f -y 15 0x60 0x05 0x80",
            "./cel-eeprom-test --all",
            "./cel-eeprom-test -r -t tlv -d 1",
            "./cel-eeprom-test --dump -t tlv -d 1"
]
TLV_Value_Test = {  "Product Name"     : ["0x21", "CS8200-32X-UN-00"],
                    "Part Number"      : ["0x22", "R1276-F0001-03"],
                    "Serial Number"    : ["0x23", "R1276F2B0119470500093"],
                    "Base MAC Address" : ["0x24", "00:E0:EC:ED:FC:82"],
                    "Manufacture Date" : ["0x25", "12/12/2019 21:41:41"],
                    "Device Version"   : ["0x26", "0"],
                    "Label Revision"   : ["0x27", "R01"],
                    "Platform Name"    : ["0x28", "arm64-celestica_cs8200_12v-r0"],
                    "ONIE Version"     : ["0x29", "2017.110.0.21"],
                    "MAC Addresses"    : ["0x2A", "3"],
                    "Manufacturer"     : ["0x2B", "CSA"],
                    "Country Code"     : ["0x2C", "US"],
                    "Vendor Name"      : ["0x2D", "CSB"],
                    "Diag Version"     : ["0x2E", "0.2"],
                    "Service Tag"      : ["0x2F", "0"]
        }

##### DIAG_10.8_TLV_EEPROM_Burning #####
disableEEValue = '1'
enableEEValue = '0'
COMeEEWP = '/sys/bus/i2c/devices/4-0060/come_eeprom_wp'
sysEEWP = '/sys/bus/i2c/devices/19-0060/system_eeprom_wp'
eepromTool = 'cel-eeprom-test'
eraseTlvCmd = ' --erase -t tlv -d '
readTlvCmd = ' -r -t tlv -d '
writeTlvCmd = ' -w -t tlv -d '
storeFile = 'store_sys_eeprom.txt'
fdValue = ['0x00 0x00 0x12 0xEB',
            '0x01=4221000154',
            '0x02=4140 2484 2301 1460 2401 3750 4461 2370 2571 2970 3591 3400 3881 2870 3680 2210 3790 3820 4140 4090 2990 4370 3040 3270 3470 4070 3670 3660 3970 3550 3420 2220',
            '0x03=R4017-F0001-01'
            ]

##### DIAG_10.9_FAN_Control_Board_EEPROM_Burning #####
fanDevice = [
    '/sys/bus/i2c/devices/19-0060/i2cfpga_eeprom_write_protect',
    '/sys/bus/i2c/devices/34-0066/fan_board_eeprom_protect',
    '/sys/bus/i2c/devices/34-0066/fan1_eeprom_protect',
    '/sys/bus/i2c/devices/34-0066/fan3_eeprom_protect',
    '/sys/bus/i2c/devices/34-0066/fan5_eeprom_protect',
    '/sys/bus/i2c/devices/34-0066/fan7_eeprom_protect',
    '/sys/bus/i2c/devices/34-0066/fan9_eeprom_protect',
    '/sys/bus/i2c/devices/34-0066/fan11_eeprom_protect'
]
configPath = '/root/diag/configs'
fanSampleFile = 'fru-fan-eeprom'
defSampleFile = 'fru-def-eeprom'
fruFanEeprom = [
    '[bia]',
    'mfg_datetime = 12885120',
    'manufacturer = CELESTICA',
    'serial_number = R1276-G0006-01FH0520220230',
    'part_number = R1276-G0001-000000'
]
fruDefEeprom = [
    '[bia]',
    'mfg_datetime = 12885120',
    'manufacturer = CELESTICA',
    'serial_number = R0000-X0000-00XX0123456789',
    'part_number = R0000-X0000-012345'
]
writeFanCmd = ' -w -t fru -d '
readFanCmd = ' -r -t fru -d '
storeType = 'fru-'
storeType1 = 'fru-1-'
storeType2 = 'fru-2-'
fanFolder = 'configs/fru-fan-eeprom'
defFolder = 'configs/fru-def-eeprom'

##### DIAG_10.39_Interrupt_Checking_Test #####
HotSwap_Alter_TOOL1 = 'cel-cpld-test -r -d 2 -R 0x0d'
I2CSET_TOOL1 = 'i2cset -y -f 27 0x11 0xf4 0x0293 w'
I2CSET_TOOL2 = 'i2cset -y -f 27 0x11 0xf4 0x029b w'
HotSwap_Alter_TOOL2 = 'cel-cpld-test -r -d 2 -R 0x08'
I2CSET_TOOL3 = 'i2cset -y -f 27 0x11 0xf4 0x0299 w'
I2CSET_TOOL4 = 'i2cset -y -f 27 0x11 0xf4 0x029b w'
##### DIAG_10.41_RJ45_MANAGEMENT_PORT_PING_TEST #####
dhcpTool = 'udhcpc'
phyTool = 'cel-phy-test'
ethSpeedTool = 'ethtool'
writeSpeedTool = ' --write -d 1 -t speed -D '
phyFile = 'phys.yaml'

##### DIAG_10.43_RTC_ACCESS_TEST #####
rtcTool = 'cel-rtc-test'
allOption = ' --all'
setRtcOption = " -w -D '20181231 235959'"
readRtcOption = ' -r'
rtcPattern1 = r'Rtc test : Passed'
rtcPattern2 = r'Rtc write : Passed'
rtcPattern3 = r'Rtc read : Passed'
#### DIAG_10.54.1_1-16byte_burst_mode_with_I2C_speed_400K_1M ####
SFP_TOOL_OPTION1 = 'cel-sfp-test --test -t single-'
SFP_TOOL_OPTION2 = '-C 10'
SFP_PROFILE_TOOL1 = './cel-sfp-test -w -t profile -D 3'
SFP_PROFILE_TOOL2 = './cel-sfp-test -w -t profile -D 2'
SFP_PROFILE_TOOL3 = './cel-sfp-test -w -t profile -D 1'
SINGLE_lst1 = [1, 2, 8 ,16]
SINGLE_lst2 = [128]
SFP_MULTI_TOOL = './cel-sfp-test --test -t multi-128 -C 1000'
##### DIAG_11.1_Check_FPGA_version_and_board_version #####
fpga1ppsTool = '/sys/devices/xilinx/pps-i2c/version'
boardTool = '/sys/devices/xilinx/pps-i2c/board_version'
boardVer = '0x3'

##### DIAG_11.5_QSFP Management registers’ status functional check #####
qsfpPresentOption = ' --show -t present'

##### DIAG_12.6_SSD_STRESS_TEST #####
ssdLogFile = 'SSD_test.log'
ssdTool = 'ssd_test.sh'
ssdpatternLst = [
    r'Run status group 0 \(all jobs\):',
    r'Disk stats \(read/write\):',
    r'sda: ios=\d+/\d+, merge=\d+/\d+, ticks=\d+/\d+, in_queue=\d+, util=.*'
]

##### DIAG_12.8_DIAG_ALL_TEST #####
diagAllTool = 'cel-all-test'
diagAlloption = ' --all'

##### DIAG_TC13_CPU_DDR_Memory_Test #####
mem_test_tool_name = 'cel-mem-test'
mem_test_option = '--all'
cores_option1 = '--test -t cores'
stress_option1 = '--test -t stress'
stress_option2 = '--test -t stress -T 30'
mem_test_option2 = '--all -C 512K'
cores_option2 = '--test -t cores -C 16M'
stress_option3 = '--test -t stress -T 30 -C 1G'
edac_option = '--test -t edac'
mem_test_passPattern = ['Stuck address test.*OK', 'Random comparison Test.*OK', 'OR comparison Test.*OK',
                        'XOR comparison Test.*OK', 'SUB comparison Test.*OK', 'Multiple comparison Test.*OK',
                        'Div comparison Test.*OK', 'sequential increment Test.*OK', 'Solid Bits comparison Test.*OK',
                        'Block seq comparison Test.*OK', 'Check board comparison Test.*OK',
                        'Bits Spread comparison Test.*OK', 'Bit Flip comparison Test.*OK',
                        'walkbits0 comparison Test.*OK', 'walkbits1 comparison Test.*OK', 'Mem test : Passed']
option_cores_pattern = ['multi-cores test : Passed']
option_stress_pattern = ['Status: PASS - please verify no corrected errors']
option_edac_pattern = ['EDAC test : Passed']

##### DIAG_TC14_I2C_Bus_Scan_Test #####
i2c_test_tool_name = 'cel-i2c-test'
i2c_test_option = '--all'
i2c_test_pattern = ['I2C test : Passed']

##### DIAG_TC16_Switch_Device_Access_Test #####
device_access_test_cmd = 'lspci'
device_access_test_option = '-s 0000:01:00.0 -vvv'
device_access_test_pattern = ['0000:01:00.0 Ethernet controller: Device \w{4}:\w{4}', 'Subsystem: Device \w{4}:\w{4}', 'Capabilities.*Management']

##### DIAG_TC18_On-board_DC/DC_Controller_Access_Test #####
dcdc_test_tool_name = 'cel-dcdc-test'
dcdc_test_option1 = '--all'
dcdc_test_option2 = '--show -d 3'
dcdc_test_option3 = '--show -d 3 4'
dcdc_test_option4 = '--show -d 4 5'
pattern_of_option1 = ['DCDC test : Passed']
pattern_of_option2 = ['Id.*Name.*Type.*channels.*Dev Path',
                      '.*ir35215-.*DCDC.*/sys/bus/i2c/devices/.*/hwmon/hwmon.*',
                      '1.*voltage.*vin.*[0-9]+\.[0-9]+.*[0-9]+\.[0-9]+.*[0-9]+\.[0-9]+.*[0-9]+\.[0-9]+',
                      '2.*voltage.*vout1.*[0-9]+\.[0-9]+.*[0-9]+\.[0-9]+.*[0-9]+\.[0-9]+.*[0-9]+\.[0-9]+',
                      '3.*voltage.*vout2.*[0-9]+\.[0-9]+.*[0-9]+\.[0-9]+.*[0-9]+\.[0-9]+.*[0-9]+\.[0-9]+',
                      '4.*current.*iin.*-.*[0-9]+\.[0-9]+.*0.*[0-9]+\.[0-9]+',
                      '5.*current.*iout1.*-.*[0-9]+\.[0-9]+.*0.*[0-9]+\.[0-9]+',
                      '6.*current.*iout2.*-.*[0-9]+\.[0-9]+.*0.*[0-9]+\.[0-9]+']

##### DIAG_TC19_Power_Monitor_Functional_Test #####
dcdc_test_option5 = '--show'
dcdc_test_option6 = '--mode low'
dcdc_test_option7 = '--mode low ll  --show'
dcdc_test_option8 = '--mode normal --show'
dcdc_test_option9 = '--mode high --show'
dcdc_test_option10 = '--mode low --all'
dcdc_test_option11 = '--mode normal --all'
dcdc_test_option12 = '--mode high --all'
pattern_of_option3 = ['1.*asc10-1.*ASC.*10.*/sys/bus/i2c/devices/27-0060',
                      '2.*asc10-2.*ASC.*10.*/sys/bus/i2c/devices/27-0061',
                      '3.*ir35215-40.*DCDC.*6.*/sys/bus/i2c/devices/.*/hwmon/hwmon.*/',
                      '4.*ir35215-4d.*DCDC.*6.*/sys/bus/i2c/devices/.*/hwmon/hwmon.*/',
                      '5.*ir35215-47.*DCDC.*6.*/sys/bus/i2c/devices/.*/hwmon/hwmon.*/'
                      ]

##### DIAG_TC20_SATA_Device_Access_Test #####
sata_device_test_tool_name = 'cel-storage-test'
sata_device_test_option = '--all'
sata_device_test_pattern = ['Starting sda1 auto test', 'Starting sda3 auto test', 'Storage test : Passed']
sata_multi_test_option = '--test -t cores'
sata_multi_test_pattern = ['multi-cores test : Passed']

##### DIAG_TC21_SSD_Device_Health_Status_Test #####
is_ssd_cmd = True
ssd_test_path = ''
ssd_test_tool_name = 'smartctl'
ssd_test_option = '-t short /dev/sda'
ssd_status_check_option = '-a /dev/sda'
ssd_test_time_stamp = 2
ssd_test_pattern = ['Sending command.*', 'Drive command.*successful', 'Testing has begun', 'Test will complete.*']
ssd_test_verify_pattern = ['SMART overall-health self-assessment test result: PASSED', 'No Errors Logged', 'If Selective self-test is pending.*']

##### DIAG_TC22_SPI_to_I2C&I/O_Device(SC18IS600)_Access_Test #####
spi_test_tool = 'cel-sfp-test'
spi_test_option = '--all'
spi_test_pattern = ['SFP test : Passed']
spi_i2c_test_cmd = 'i2cdetect'
spi_i2c_test_option = '-l'
spi_i2c_test_option1 = '-y -r 34'
spi_i2c_test_pattern = ['00:\s+.*', '10.*', '20.*', '30.*', '40.*', '50: UU.*', '60.*', '70: UU UU UU UU.*\s+']

#### DIAG_11.5.2_QSFP_LPmode_register_(0x0170)_check ####
lpmode_all_option = ' -w -t lpmod -D '
i2cget_tool = 'i2cget -y -f '
i2cget_option = ' 0x50 0x41'
low_power_mode = '1'
high_power_mode = '0'
pps_i2c_tool = '/sys/devices/xilinx/pps-i2c/port'
pps_i2c_option = '_lpmod'
lpmode_register_pattern = r'QSFP Optical Module LPMode Signal Test: Passed'

#### DIAG_11.5.3_QSFP_Reset_register_(0x0178)_check ####
resetL_all_option = ' -w -t reset -D '
reset_register_option = '_module_reset'
reset_register_pattern = r'QSFP Optical Module ResetL Signal Test: Passed'

#### DIAG_10.14_TPM_Device_Access_Test ####
tpm_output_path = '/root/diag/output'
dump_tpm_tool = 'dump_tpm.sh'
tpm_pattern = 'CELESTICA'

##### DIAG_TC23_System_Watchdog_Test #####
system_watchdog_test_cmd = 'echo 10 > /sys/bus/i2c/devices/19-0060/system_watchdog_seconds'

##### DIAG_TC24_System_Reset_Test #####
warm_reset_cmd = 'echo 1 > /sys/bus/i2c/devices/15-0060/warm_reset'
cold_reset_cmd = 'echo 1 > /sys/bus/i2c/devices/15-0060/cold_reset'

##### DIAG_TC26_TEST #######
fault_log_cmd = [
            "i2cset -y -f 15 0x60 0x31 0x01",
            "i2cset -y -f 15 0x60 0x32 0x00",
            "i2cset -y -f 15 0x60 0x33 0x00",
            "i2cset -y -f 15 0x60 0x34 0xaa",
            "i2cset -y -f 15 0x60 0x30 0x01",
            "i2cset -y -f 15 0x60 0x30 0x03",
            "i2cget -y -f 15 0x60 0x35 ",
            "cd /root/diag",
            "./cel-log-test -r -d 1"
]
log_pattern = {"0xaa":"0xaa"}
##### DIAG_TC31_FAN_Present_Test #####
fan_test_tool_name = 'cel-fan-test'
fan_test_option1 = '--show'
fan_test_option2 = '--show -t present'
la = list(map(lambda x: 'fan-' + x + '.*Front.*F2B', list(str(a) for a in range(1, 7))))
lb = list(map(lambda x: 'fan-' + x + '.*Panel.*F2B', list(str(a) for a in range(1, 7))))
list_ab = list(zip(la, lb))
fan_test_pattern = []
new_pattern = [fan_test_pattern.extend(list(a)) for a in list_ab]

present_status_cmd = 'echo $((`i2cget -f -y 15 0x60 0x09` & 0x80))'

cat_intl_signal_cmd_start = 'cat /sys/bus/i2c/devices/15-0060/port'
cat_intl_signal_cmd_end = '_module_interrupt'

devicename = os.environ.get("deviceName", "")
import logging
logging.info("devicename:{}".format(devicename))
temp_test_tool_name = 'cel-temp-test'
temp_test_option1 = '--all'
temp_test_option2 = '--list'
temp_test_option3 = '--mode low --all'
temp_test_option4 = '--mode normal --all'
temp_test_option5 = '--mode high --all'
temp_test_pattern1 = ['Temp test : Passed']
temp_test_fail_pattern = ['Temp test : FAILED']
if "tianhe" in devicename.lower():
    margin_cmd_list_low = 'cs8264_vrm_low.sh'
    margin_cmd_list_high = 'cs8264_vrm_high.sh'
    margin_option = ''
    margin_pattern = ['.*PASS'] * 28
    temp_test_pattern2 = ['Id.*type.*refdes.*location.*ch.*mag.*min.*max.*DevPath',
                          '1.*lm75.*/sys/bus/i2c/devices/.*',
                          '2.*lm75.*/sys/bus/i2c/devices/.*',
                          '3.*lm75.*/sys/bus/i2c/devices/.*',
                          '4.*lm75.*/sys/bus/i2c/devices/.*',
                          '5.*lm75.*/sys/bus/i2c/devices/.*',
                          '6.*lm75.*/sys/bus/i2c/devices/.*',
                          '7.*lm75.*/sys/bus/i2c/devices/.*',
                          '8.*lm75.*/sys/bus/i2c/devices/.*',
                          '9.*lm75.*/sys/bus/i2c/devices/.*',
                          '10.*sa56004.*/sys/bus/i2c/devices/.*',
                          '11.*sa56004.*/sys/bus/i2c/devices/.*',
                          '12.*sa56004.*/sys/bus/i2c/devices/.*',
                          '13.*sa56004.*/sys/bus/i2c/devices/.*',
                          '14.*asc10.*/sys/bus/i2c/devices/.*',
                          '15.*asc10.*/sys/bus/i2c/devices/.*',
                          '16.*asc10.*.*/sys/bus/i2c/devices/.*',
                          '17.*asc10.*.*/sys/bus/i2c/devices/.*',
                          '18.*asc10.*.*/sys/bus/i2c/devices/.*',
                          '19.*asc10.*.*/sys/bus/i2c/devices/.*',
                          '20.*asc10.*.*/sys/bus/i2c/devices/.*',
                          '21.*asc10.*.*/sys/bus/i2c/devices/.*',
                          '22.*asc10.*.*/sys/bus/i2c/devices/.*',
                          '23.*asc10.*.*/sys/bus/i2c/devices/.*',
                          '24.*asc10.*.*/sys/bus/i2c/devices/.*',
                          '25.*asc10.*.*/sys/bus/i2c/devices/.*',
                          '26.*asc10.*.*/sys/bus/i2c/devices/.*',
                          '27.*asc10.*.*/sys/bus/i2c/devices/.*',
                          '28.*asc10.*.*/sys/bus/i2c/devices/.*',
                          '29.*tps53647.*.*/sys/bus/i2c/devices/.*',
                          '30.*tps536c7.*.*/sys/bus/i2c/devices/.*',
                          '31.*tps53688.*.*/sys/bus/i2c/devices/.*',
                          '32.*tps53688.*.*/sys/bus/i2c/devices/.*',
                          '33.*tps53688.*.*/sys/bus/i2c/devices/.*',
                          '34.*tps53688.*.*/sys/bus/i2c/devices/.*',
                          '35.*CPU.*/sys/class/thermal/thermal_zone0/',
                          '36.*CPU.*/sys/class/thermal/thermal_zone1/',
                          '37.*CPU.*/sys/class/thermal/thermal_zone2/',
                          '38.*CPU.*/sys/class/thermal/thermal_zone3/',
                          '39.*CPU.*/sys/class/thermal/thermal_zone4/',
                          '40.*CPU.*/sys/class/thermal/thermal_zone5/',
                          '41.*CPU.*/sys/class/thermal/thermal_zone6/',
                          '42.*app.*/sys/bus/i2c/devices/.*',
                          ]
    temp_test_pattern2_48V = ['Id.*type.*refdes.*location.*ch.*mag.*min.*max.*DevPath',
                          '1.*lm75.*/sys/bus/i2c/devices/.*',
                          '2.*lm75.*/sys/bus/i2c/devices/.*',
                          '3.*lm75.*/sys/bus/i2c/devices/.*',
                          '4.*lm75.*/sys/bus/i2c/devices/.*',
                          '5.*lm75.*/sys/bus/i2c/devices/.*',
                          '6.*lm75.*/sys/bus/i2c/devices/.*',
                          '7.*lm75.*/sys/bus/i2c/devices/.*',
                          '8.*lm75.*/sys/bus/i2c/devices/.*',
                          '9.*lm75.*/sys/bus/i2c/devices/.*',
                          '10.*sa56004.*/sys/bus/i2c/devices/.*',
                          '11.*sa56004.*/sys/bus/i2c/devices/.*',
                          '12.*sa56004.*/sys/bus/i2c/devices/.*',
                          '13.*sa56004.*/sys/bus/i2c/devices/.*',
                          '14.*asc10.*/sys/bus/i2c/devices/.*',
                          '15.*asc10.*/sys/bus/i2c/devices/.*',
                          '16.*asc10.*.*/sys/bus/i2c/devices/.*',
                          '17.*asc10.*.*/sys/bus/i2c/devices/.*',
                          '18.*asc10.*.*/sys/bus/i2c/devices/.*',
                          '19.*asc10.*.*/sys/bus/i2c/devices/.*',
                          '20.*asc10.*.*/sys/bus/i2c/devices/.*',
                          '21.*asc10.*.*/sys/bus/i2c/devices/.*',
                          '22.*asc10.*.*/sys/bus/i2c/devices/.*',
                          '23.*asc10.*.*/sys/bus/i2c/devices/.*',
                          '24.*asc10.*.*/sys/bus/i2c/devices/.*',
                          '25.*asc10.*.*/sys/bus/i2c/devices/.*',
                          '26.*asc10.*.*/sys/bus/i2c/devices/.*',
                          '27.*asc10.*.*/sys/bus/i2c/devices/.*',
                          '28.*asc10.*.*/sys/bus/i2c/devices/.*',
                          '29.*tps53647.*.*/sys/bus/i2c/devices/.*',
                          '30.*tps536c7.*.*/sys/bus/i2c/devices/.*',
                          '31.*tps53688.*.*/sys/bus/i2c/devices/.*',
                          '32.*tps53688.*.*/sys/bus/i2c/devices/.*',
                          '33.*tps53688.*.*/sys/bus/i2c/devices/.*',
                          '34.*tps53688.*.*/sys/bus/i2c/devices/.*',
                          '35.*tps546a24a.*.*/sys/bus/i2c/devices/.*',
                          '36.*q50sn120a4.*.*/sys/bus/i2c/devices/.*',
                          '37.*ltc4287.*.*/sys/bus/i2c/devices/.*',
                          '38.*CPU.*.*/sys/class/thermal/.*',
                          '39.*CPU.*.*/sys/class/thermal/.*',
                          '40.*CPU.*.*/sys/class/thermal/.*',
                          '41.*CPU.*.*/sys/class/thermal/.*',
                          '42.*CPU.*.*/sys/class/thermal/.*',
                          '43.*CPU.*.*/sys/class/thermal/.*',
                          '44.*CPU.*.*/sys/class/thermal/.*',
                          '45.*app.*/sys/bus/i2c/devices/.*',
                          ]
    dcdc_access_option1 = '--show -d 4'
    dcdc_access_option2 = '--show -d 5'
    dcdc_access_option3 = '--show -d 6'
    base_of_passpattern = ['Id.*Name.*Type.*Ch.*Dev Path',
                           '.*/sys/bus/i2c/devices/.*',
                           '.*Ch\s*\|\s*type\s*\|\s*name\s*\|\s*def_val\s*\|\s*max_val\s*\|\s*min_val\s*\|\s*value.*'
                           ]
    base_ptn = '{}.*voltage.*{}' + ".*([0-9]+\.[0-9]+|\d+)" * 3
    passpattern_of_option1 = []
    passpattern_of_option2 = []
    passpattern_of_option3 = []
    passpattern_names1 = ["PLL_AVDD1", "PLL_AVDD2", "PLL_VDD", "XP3R3V_CPU", "XP3R3V_AUX_CPU", "AVDD_XP0R9V",
                          "AVDD_XP0R9V", "AVDDH_XP1R1V", "XP3R3V_LEFT", "XP12R0V"]
    passpattern_names2 = ["XP1R8V_VDDH", "XP3R3V", "I2C_FPGA_3V3", "XP5R0V", "VDD_CORE", "XP3R3V_SATA1", "XP3R3V_AUX",
                          "VDD_CORE", "XP3R3V_RIGHT", "XP12R0V_CPU"]
    passpattern_names3 = ["FPGA_1.0V", "FPGA_1.2V", "FPGA_1.8V", "FPGA_MGTAVCC", "FPGA_3.3V", "3.3V_AUX", "NC", "NC",
                          "NC", "NC"]

    for i in range(1, 11):
        passpattern_of_option1.append(base_ptn.format(i, passpattern_names1[i - 1]))
        passpattern_of_option2.append(base_ptn.format(i, passpattern_names2[i - 1]))
        passpattern_of_option3.append(base_ptn.format(i, passpattern_names3[i - 1]))

    passpattern_of_option1 = base_of_passpattern + passpattern_of_option1
    passpattern_of_option2 = base_of_passpattern + passpattern_of_option2
    passpattern_of_option3 = base_of_passpattern + passpattern_of_option3

    mem_test_passPattern = ['Stuck Address.*OK', 'Random Value.*OK', 'Compare XOR.*OK', 'Compare SUB.*OK',
                            'Compare MUL.*OK', 'Compare DIV.*OK', 'Compare OR.*OK', 'Compare AND.*OK',
                            'Sequential Increment.*OK', 'Solid Bits.*OK', 'Block Sequential.*OK', 'Checkerboard.*OK',
                            'Bit Spread.*OK', 'Bit Flip.*OK', 'Walking Ones.*OK', 'Walking Zeroes.*OK',
                            '.*Mem test : Passed']
    system_watchdog_reset_cmd = 'echo 1 > /sys/bus/i2c/devices/19-0060/system_watchdog_enable'
    COME_fault_log_cmd = [
        "cd /root/diag",
        "echo 1 > /sys/bus/i2c/devices/4-0060/fault_logger_reset",
        "i2cset -y -f 4 0x60 0x7f 0x01",
        "i2cset -y -f 4 0x60 0xd0 0x12",
        "i2cset -y -f 4 0x60 0xd0 0x02",
        "./cel-log-test -r -d 1",
        ]
    fault_log_cmd = [
        "cd /root/diag",
        "echo 1 > /sys/bus/i2c/devices/19-0060/fault_logger_reset",
        "i2cset -y -f 19 0x60 0x30 0x12",
        "i2cset -y -f 19 0x60 0x30 0x02",
        "./cel-log-test -r -d 2"
        ]
    console_log_cmd1 = ['echo 1 > /sys/bus/i2c/devices/19-0060/console_logger_reset',
                   './cel-log-test -w -d 3 -A 0 -D "1234567890ABCDEF"',
                   './cel-log-test --dump -d 3']
    console_log_cmd2 = ['./cel-log-test --dump -d 3',
                   'echo 1 > /sys/bus/i2c/devices/19-0060/console_logger_reset',
                   'ls',
                   './cel-log-test --dump -d 3']
    console_log_pattern1 = ['write done', '\[\d+\].*1234567890ABCDEF']
    console_log_pattern2 = ['\[\d+\].*1234567890ABCDEF', '\[\d+\].*root\@diagos\-hos']
    fault_log_pattern1 = ['FAULT log data addr=0x0', 'Log test : Passed']
    fault_log_pattern2 = ['FAULT log data addr=0x\w+', 'Log test : Passed']

    psu_show_ptn = [
        "-- DC-busbar present --",
        "voltage :\s+(\d+.\d+|\d+)\s+V",
        "current :\s+(\d+.\d+|\d+)\s+A",
        "power :\s+(\d+.\d+|\d+)\s+W"
    ]

    temp_location_pattern = ["I2C-FPGA", "Switch-LEFT", "Switch-RBB", "Switch-LBB", "Switch-RIGHT",
                             "Switch-FRONT", "Fan-RIGHT", "Fan-CENTER", "Fan-LEFT", "on-chip", "CPU sensor", "on-chip",
                             "CPU sensor", "COMe-Q1", "COMe-Q2", "COMe-ASC0", "COMe-Q3", "COMe-Q4", "COMe-ASC1",
                             "Switch-Q16", "Switch-Q10", "Switch-asc-0", "Switch-Q17", "Switch-Q18", "Switch-asc-1",
                             "I2C_FPGA-Q1", "I2C_FPGA-Q2", "I2C_FPGA-asc-2", "COMe-VDD core", "Switch-VDDCORE",
                             "Switch-AVDD",
                             "Switch-3V3-R", "Switch-AVDD-H", "Switch-3V3-L", "thermal_zone0", "thermal_zone1",
                             "thermal_zone2",
                             "thermal_zone3", "thermal_zone4", "thermal_zone5", "thermal_zone6", "switch-core"]

    temp_all_cmd = "./cel-temp-test --all"
    temp_mode_cmds = []
    for each in ["log", "medium", "high"]:
        temp_mode_cmds.append(f"./cel-temp-test --mode {each} --all")

    temp_list_pattern = ".*{}.*{}.*" + "(\d+.\d+|\d+).*" * 3
    temp_list_all_pattern = [
        ".*Id \|   type   \| refdes \|    location    \| ch \|  mag \|  min \|  max  \|  DevPath"
    ]
    for i in range(len(temp_location_pattern)):
        ptn = temp_list_pattern.format(i + 1, temp_location_pattern[i])
        temp_list_all_pattern.append(ptn)

    fan_speed_tool_name = 'cel-fan-test'
    fan_speed_option = '--show'
    fan_speed_pattern1 = ['.*PWM.*255.*'] * 12
    fan_speed_pattern2 = ['.*PWM.*229.*'] * 12
    fan_speed_pattern3 = ['.*PWM.*204.*'] * 12
    fan_speed_pattern4 = ['.*PWM.*178.*'] * 12
    fan_speed_pattern5 = ['.*PWM.*140.*'] * 12

    sfp_cmd = 'cel-sfp-test'
    sfp_option_all = '--all'
    sfp_option_show = '--show -t present'
    sfp_profile1_cmd = './cel-sfp-test -w -t profile -D 1'
    sfp_profile2_cmd = './cel-sfp-test -w -t profile -D 2'
    sfp_profile3_cmd = './cel-sfp-test -w -t profile -D 3'
    sfp_profile1_pattern = ['.*port.*Present.*100K.*', 'Passed']
    sfp_profile1_pattern = sfp_profile1_pattern * 32
    sfp_profile1_pattern.append('SFP test : Passed')
    sfp_profile2_pattern = ['.*port.*Present.*400K', 'Passed']
    sfp_profile2_pattern = sfp_profile2_pattern * 32
    sfp_profile2_pattern.append('SFP test : Passed')
    sfp_profile3_pattern = ['.*port.*Present.*1M', 'Passed']
    sfp_profile3_pattern = sfp_profile3_pattern * 32
    sfp_profile3_pattern.append('SFP test : Passed')
    sfp_show_pattern = ['.*port.*Present.*']
    sfp_show_pattern = sfp_show_pattern * 32

if "fenghuangv2" in devicename.lower():
    temp_test_pattern2 = ['Id.*type.*refdes.*location.*ch.*mag.*min.*max.*DevPath',
                          '1.*lm75.*/sys/bus/i2c/devices/.*',
                          '2.*lm75.*/sys/bus/i2c/devices/.*',
                          '3.*lm75.*/sys/bus/i2c/devices/.*',
	                  '4.*lm75.*/sys/bus/i2c/devices/.*',
	                  '5.*lm75.*/sys/bus/i2c/devices/.*',
	                  '6.*lm75.*/sys/bus/i2c/devices/.*',
	                  '7.*lm75.*/sys/bus/i2c/devices/.*',
	                  '8.*lm75.*/sys/bus/i2c/devices/.*',
	                  '9.*lm75.*/sys/bus/i2c/devices/.*',
	                  '10.*asc10.*/sys/bus/i2c/devices/.*',
	                  '11.*asc10.*/sys/bus/i2c/devices/.*',
	                  '12.*asc10.*.*/sys/bus/i2c/devices/.*',
	                  '13.*asc10.*.*/sys/bus/i2c/devices/.*',
	                  '14.*asc10.*.*/sys/bus/i2c/devices/.*',
	                  '15.*asc10.*.*/sys/bus/i2c/devices/.*',
                          '16.*asc10.*.*/sys/bus/i2c/devices/.*',
                          '17.*asc10.*.*/sys/bus/i2c/devices/.*',
	                  '18.*asc10.*.*/sys/bus/i2c/devices/.*',
	                  '19.*tps536c7.*.*/sys/bus/i2c/devices/.*',
                          '20.*tps53688.*.*/sys/bus/i2c/devices/.*',
	                  '21.*tps53688.*.*/sys/bus/i2c/devices/.*',
	                  '22.*tps53688.*.*/sys/bus/i2c/devices/.*',
	                  '23.*tps53688.*.*/sys/bus/i2c/devices/.*',
	                  '24.*CPU.*/sys/class/thermal/thermal_zone0/',
	                  '25.*CPU.*/sys/class/thermal/thermal_zone1/',
                          '26.*CPU.*/sys/class/thermal/thermal_zone2/',
	                  '27.*CPU.*/sys/class/thermal/thermal_zone3/',
                          '28.*app.*/sys/bus/i2c/devices/.*',
                          ]
    diag_cel_cpld_test_all_patterns = [
        r"(?m)^[ \t]*Device:[ \t]+system_cpld.*",
        r"(?m)^dev_path.*version:[ \t]+(?P<system_cpld>\w+)",
        r"(?m)^[ \t]*Device:[ \t]+led_cpld1",
        r"(?m)^dev_path.*version:[ \t]+(?P<led_cpld1>\w+)",
        r"(?m)^[ \t]*Device:[ \t]+led_cpld2",
        r"(?m)^dev_path.*version:[ \t]+(?P<led_cpld2>\w+)",
        r"(?m)^[ \t]*Device:[ \t]+fan_cpld",
        r"(?m)^dev_path.*version:[ \t]+(?P<fan_cpld>[\w\.]+)",
        r"(?m)^[ \t]*Device:[ \t]+.*fpga",
        r"(?m)^dev_path.*version:[ \t]+(?P<fpga_VER>[\w\.]+)",
        r"(?m)^[ \t]*CPLD[ \t]+test.*Passed[ \t]*$",
    ]
    fan_test_pattern = fan_test_pattern[0:12]
    dev_type = DeviceMgr.getDevice(devicename).get('cardType')
    drive_pattern = {
        "cms": "cms50216.*",
        "sfp_module": "sfp_module.*",
        "i2c_accel_fpga": "i2c_accel_fpga.*",
        "fan_cpld": "fan_cpld.*",
        "sys_cpld": "sys_cpld.*",
        "cls_i2c_client": "cls_i2c_client.*",
        "ltc4282": "ltc4282.*",
        "psu_dps800": "psu_dps800.*",
        "tps53679": "tps53679.*",
        "asc10": "asc10.*"
    }
    TLV_Value_Test = {  "Product Name"     : ["0x21", "CS8000-64X-UN-00"],
                    "Part Number"      : ["0x22", "R1276-F0001-04"],
                    "Serial Number"    : ["0x23", "R1165F2B041846SZ00021"],
                    "Base MAC Address" : ["0x24", "00:E0:EC:C9:B1:B4"],
                    "Manufacture Date" : ["0x25", "12/14/2018 03:01:52"],
                    "Device Version"   : ["0x26", "2"],
                    "Label Revision"   : ["0x27", "R0B"],
                    "Platform Name"    : ["0x28", "arm64-celestica_cs8000-r0"],
                    "ONIE Version"     : ["0x29", "2017.11.002"],
                    "MAC Addresses"    : ["0x2A", "3"],
                    "Manufacturer"     : ["0x2B", "CSA"],
                    "Country Code"     : ["0x2C", "US"],
                    "Vendor Name"      : ["0x2D", "CSB"],
                    "Diag Version"     : ["0x2E", "0.07"],
                    "Service Tag"      : ["0x2F", "1"],
                    "Vendor Extension" : ["0xFD", "0x0c"]
        }
    log_pattern = {"0xff":"0xff"}
    fault_log_cmd = [
        "cd /root/diag",
        "echo 1 > /sys/bus/i2c/devices/8-0060/fault_logger_reset",
        "i2cset -y -f 8 0x60 0x30 0x12",
        "i2cset -y -f 8 0x60 0x30 0x02",
        "./cel-log-test -r -d 1"
    ]
    fault_log_pattern1 = ['FAULT log data addr=0x0', 'Log test : Passed']
    fault_log_pattern2 = ['FAULT log data addr=0x\w+', 'Log test : Passed']
    console_log_cmd1 = ['echo 1 > /sys/bus/i2c/devices/8-0060/console_logger_reset',
                    './cel-log-test -w -d 2 -A 0 -D "1234567890ABCDEF"',
                    './cel-log-test --dump -d 2']
    console_log_cmd2 = ['./cel-log-test --dump -d 2',
                    'echo 1 > /sys/bus/i2c/devices/8-0060/console_logger_reset',
                    './cel-log-test --dump -d 2']
    console_log_pattern1 = ['write done', '\[\d+\].*1234567890ABCDEF']
    console_log_pattern2 = ['\[\d+\].*1234567890ABCDEF', '\[\d+\].*root\@CEL\-DiagOS:']
    console_log_pattern = ['write done', '\[\d+\].*1234567890ABCDEF', '\[\d+\].*root\@CEL\-DiagOS:']
    hw_version_dict = {'uC_app': '2.1.14', 'uC_bl': '2.28', 'ASC10-0': '\w+', 'ASC10-1': '\w+', 'ASC10-2': '\w+'}
    eeprom_burning_cmd = [
        "cd /root/diag",
        "echo 0 > /sys/bus/i2c/devices/8-0060/system_eeprom_wp",
        "./cel-eeprom-test -r -t tlv -d 1",
        "echo 0 > /sys/bus/i2c/devices/8-0060/i2cfpga_eeprom_write_protect",
        "./cel-eeprom-test --init",
    ]
    eeprom_d1_cmd = "./cel-eeprom-test -r -t tlv -d 1"
    eeprom_init_cmd = "./cel-eeprom-test --init"
    eeprom_burning_cmd2 = [
        "cd /root/diag",
        "./cel-eeprom-test -w -t tlv -d 1 -A 0xfd",
        "./cel-eeprom-test -r -t tlv -d 1"
    ]
    check_uart_cmd = [
        'i2cset -f -y 8 0x60 0x05 0xe4'
    ]

    mem_test_passPattern = ['Stuck Address.*OK', 'Random Value.*OK', 'Compare XOR.*OK', 'Compare SUB.*OK',
                            'Compare MUL.*OK', 'Compare DIV.*OK', 'Compare OR.*OK', 'Compare AND.*OK',
                            'Sequential Increment.*OK', 'Solid Bits.*OK', 'Block Sequential.*OK', 'Checkerboard.*OK',
                            'Bit Spread.*OK', 'Bit Flip.*OK', 'Walking Ones.*OK', 'Walking Zeroes.*OK', '.*Mem test : Passed']

    dcdc_access_option1 = '--show -d 4'
    dcdc_access_option2 = '--show -d 5'
    dcdc_access_option3 = '--show -d 6'
    passpattern_of_option1 = ['Id.*Name.*Type.*Ch.*Dev Path',
                          '.*/sys/bus/i2c/devices/.*/hwmon',
                          '1.*voltage.*vin.*[0-9]+\.[0-9]+.*[0-9]+\.[0-9]+.*[0-9]+\.[0-9]+.*[0-9]+\.[0-9]+',
                          '2.*voltage.*vout1.*[0-9]+\.[0-9]+.*[0-9]+\.[0-9]+.*[0-9]+\.[0-9]+.*[0-9]+\.[0-9]+',
                          '3.*current.*iin.*-.*[0-9]+\.[0-9]+.*0.*[0-9]+\.[0-9]+',
                          '4.*current.*iout1.*-.*[0-9]+\.[0-9]+.*0.*[0-9]+\.[0-9]+']
    passpattern_of_option2 = ['Id.*Name.*Type.*Ch.*Dev Path',
                          '.*/sys/bus/i2c/devices/.*/hwmon',
                          '1.*voltage.*vin.*[0-9]+\.[0-9]+.*[0-9]+\.[0-9]+.*[0-9]+\.[0-9]+.*[0-9]+\.[0-9]+',
                          '2.*voltage.*vout1.*[0-9]+\.[0-9]+.*[0-9]+\.[0-9]+.*[0-9]+\.[0-9]+.*[0-9]+\.[0-9]+',
                          '3.*voltage.*vout2.*[0-9]+\.[0-9]+.*[0-9]+\.[0-9]+.*[0-9]+\.[0-9]+.*[0-9]+\.[0-9]+',
                          '4.*current.*iin.*-.*[0-9]+\.[0-9]+.*0.*[0-9]+\.[0-9]+',
                          '5.*current.*iout1.*-.*[0-9]+\.[0-9]+.*0.*[0-9]+\.[0-9]+',
                          '6.*current.*iout2.*-.*[0-9]+\.[0-9]+.*0.*[0-9]+\.[0-9]+']

    dcdc_test_tool_name = 'cel-dcdc-test'
    dcdc_test_option1 = '--show'
    dcdc_test_option2 = '--all'
    pattern_of_option2 = ['DCDC test : Passed']
    pattern_of_option1 = ['Id.*Name.*Type.*Ch.*Dev Path',
                          '1.*asc10-0.*ASC.*/sys/bus/i2c/devices/.*',
                          '2.*asc10-1.*ASC.*/sys/bus/i2c/devices/.*',
                          '3.*asc10-2.*ASC.*/sys/bus/i2c/devices/.*',
                          '4.*SW-VDDCORE.*tps.*/sys/bus/i2c/devices/.*',
                          '5.*SW-AVDD/SW-3V3-R.*tps.*/sys/bus/i2c/devices/.*',
                          '6.*SW-AVDD-H/SW-3V3-L.*tps.*/sys/bus/i2c/devices/.*'
                         ]

    spi_i2c_test_pattern = ['00:\s+.*', '10.*', '20.*', '30.*', '40.*', '50.*UU UU.*UU.*', '60.*', '70: UU.*\s+']

    system_watchdog_test_cmd = 'echo 10 > /sys/bus/i2c/devices/8-0060/system_watchdog_seconds'
    system_watchdog_reset_cmd = 'echo 1 > /sys/bus/i2c/devices/8-0060/system_watchdog_enable'

    warm_reset_cmd = 'echo 1 > /sys/bus/i2c/devices/8-0060/warm_reset'
    cold_reset_cmd = 'echo 1 > /sys/bus/i2c/devices/8-0060/cold_reset'

    present_status_cmd = 'echo $((`i2cget -f -y 8 0x60 0x09` & 0x80))'



    qsfp_dd_port_bus_32_modules = {1: 101, 2: 102, 3: 103, 4: 104, 5: 105, 6: 106, 7: 107, 8: 108, 9: 109, 10: 110, 11: 111, 12: 112, 13: 113,
     14: 114, 15: 115, 16: 116, 17: 117, 18: 118, 19: 119, 20: 120, 21: 121, 22: 122, 23: 123, 24: 124, 25: 125,
     26: 126, 27: 127, 28: 128, 29: 129, 30: 130, 31: 131, 32: 132}
    qsfp_dd_cmd1 = '0x50 0xe1'
    qsfp_dd_cmd2 = '0x50 0x41'

    device_access_test_option = '-s  0000:00:01.0  -vvv'
    device_access_test_pattern = ['0000:00:01.0 Ethernet controller: Device \w{4}:\w{4}',
                                  'Control.*', 'Status:.*', 'Capabilities.*Management']

    fan_speed_tool_name = 'cel-fan-test'
    fan_speed_option = '--show'
    fan_speed_pattern1 = ['.*PWM.*255.*']
    fan_speed_pattern2 = ['.*PWM.*191.*']
    fan_speed_pattern3 = ['.*PWM.*127.*']
    fan_speed_pattern1 = fan_speed_pattern1 * 12
    fan_speed_pattern2 = fan_speed_pattern2 * 12
    fan_speed_pattern3 = fan_speed_pattern3 * 12

    fan_wdt_pwm_pattern1 = ['.*PWM\s+\|.*\|.*\|.*127']
    fan_wdt_pwm_pattern2 = ['.*PWM\s+\|.*\|.*\|.*255']
    fan_wdt_pwm_pattern1 = fan_wdt_pwm_pattern1 * 12
    fan_wdt_pwm_pattern2 = fan_wdt_pwm_pattern2 * 12

    fan_ctrl_tool = 'cel-fan-test'
    fan_ctrl_option = '--test -t fan_ctrl'
    fan_ctrl_test_pattern = ['INFO:.*Current.*PWM=.*', 'INFO:.*temp_offset.*pwm=.*', 'INFO.*Inlet sensor.*',
                             'INFO:.*PID.*']

    rtc_access_tool = 'cel-rtc-test'
    rtc_access_option1 = '--all'
    rtc_access_pattern1 = ['Rtc test : Passed']

    cat_intl_signal_cmd_start = 'cat /sys/devices/xilinx/accel-i2c/port'
    cat_intl_signal_cmd_end = '_module_interrupt'
    if dev_type == '1PPS':
        cat_intl_signal_cmd_start = 'cat /sys/devices/xilinx/pps-i2c/port'
        cat_intl_signal_cmd_end = '_module_interrupt'

    qsfp_reset_module_cmd1 = './cel-sfp-test -w -t reset -D 1'
    qsfp_reset_module_cmd2 = './cel-sfp-test -w -t reset -D 0'
    qsfp_lpmode_module_cmd1 = './cel-sfp-test -w -t lpmod -D 1'
    qsfp_lpmode_module_cmd2 = './cel-sfp-test -w -t lpmod -D 0'
    check_qsfp_lpmode_module_cmd = '0x50 0xe1'
    qsfp_lpmode_module_pattern1 = ['^0x1b$']
    qsfp_lpmode_module_pattern2 = ['^0x19$']
    check_qsfp_reset_module_cmd = 'cat /sys/devices/xilinx/accel-i2c/port1_module_reset'
    if dev_type == '1PPS':
        check_qsfp_reset_module_cmd = 'cat /sys/devices/xilinx/pps-i2c/port1_module_reset'
    qsfp_reset_module_pattern1 = ['^1$']
    qsfp_reset_module_pattern2 = ['^0$']

    sfp_cmd = 'cel-sfp-test'
    sfp_option_all = '--all'
    sfp_option_show = '--show -t present'
    sfp_profile1_cmd = './cel-sfp-test -w -t profile -D 1'
    sfp_profile2_cmd = './cel-sfp-test -w -t profile -D 2'
    sfp_profile1_pattern = ['.*port.*Present.*400K.*', 'Passed']
    sfp_profile1_pattern = sfp_profile1_pattern * 32
    sfp_profile1_pattern.append('SFP test : Passed')
    sfp_profile2_pattern = ['.*port.*Present.*1M', 'Passed']
    sfp_profile2_pattern = sfp_profile2_pattern * 32
    sfp_profile2_pattern.append('SFP test : Passed')
    sfp_show_pattern = ['.*port.*Present.*']
    sfp_show_pattern = sfp_show_pattern * 32

    cat_ddr_log = 'cat /root/tools/stress_test/DDR_test.log\r\n'
    cat_ddr_log_regexp = '.*Status:.*-.*'
    cat_ddr_log_pattern = {".*Status:.*PASS":".*Status:.*PASS"}

    ssd_stress_pass_patterns = r"(?m)^[ \t]*Run[ \t]*status[ \t]*group[ \t]*"
