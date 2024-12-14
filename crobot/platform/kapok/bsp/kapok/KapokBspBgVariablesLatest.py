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


import DeviceMgr
from SwImage import SwImage
from Const import BOOT_MODE_UBOOT, BOOT_MODE_DIAGOS, BOOT_MODE_ONIE
from KapokConst import STOP_AUTOBOOT_PROMPT, STOP_AUTOBOOT_KEY
import copy

pc_info = DeviceMgr.getServerInfo('PC')
dev_info = DeviceMgr.getDevice()

diagos_mode = BOOT_MODE_DIAGOS
uboot_mode = BOOT_MODE_UBOOT
onie_mode = BOOT_MODE_ONIE

# SwImage shared objects
BSP_DRIVER = SwImage.getSwImage("BSP_DRIVER")
FAN_CPLD = SwImage.getSwImage("FAN_CPLD")
SYS_CPLD = SwImage.getSwImage("SYS_CPLD")
# End of SwImage shared objects


diag_tools_path = "/root/diag"
diag_ld_lib_path = "/root/diag/output"
diag_export_env = "export LD_LIBRARY_PATH=" + diag_ld_lib_path + " && export CEL_DIAG_PATH=" + diag_tools_path + " && "

vmetool_path = str(FAN_CPLD.localImageDir)
vmetool_fan_cpld_new_image_file = str(FAN_CPLD.newImage)
vmetool_fan_cpld_new_image_version = str(FAN_CPLD.newVersion)
vmetool_sys_cpld_new_image_file = str(SYS_CPLD.newImage)
vmetool_sys_cpld_new_image_version = str(SYS_CPLD.newVersion)

bsp_driver_new_version = str(BSP_DRIVER.newVersion)
tftp_server_ipv4 = pc_info.managementIP
tftp_interface = dhcp_interface = "eth0"

uboot_prompt = dev_info.promptUboot
uboot_boot_to_diagos_command = "run diag_bootcmd"
uboot_kernel_boot_info_patterns = [
    r"Booting kernel.* (?P<kernel_ram_entry_point>\d+)",
    r"Image Type:[ \t]+(?P<kernel_arch>\w+)",
    r"Data Size:[ \t]+(?P<kernel_data_size_bytes>\w+)[ \t]+Bytes",
]

bsp_driver_file = "driver-" + bsp_driver_new_version + ".tar.xz"
bsp_driver_file_name_only = "driver-" + bsp_driver_new_version
bsp_driver_path_to_install = str(BSP_DRIVER.localImageDir)

bsp_driver_show_version_command = "cat /root/driver/releaseNotes | grep Ver"
bsp_driver_version_pattern = r" <(?P<bsp_installed_driver_version>\d+\.\d+\.\d+)>"

diagos_network_id = "192.168.0.30/24"  # For manual IP

i2c_lm75_devices = {
    "TERALYNX_FRONT" : {
        "PATH" : "/sys/bus/i2c/devices/28-0049/hwmon/hwmon11",
        "ATTRS" : {
            "name" : r"(?m)^(?P<name>lm75a)",

            "temp1_input" : r"(?m)^(?P<temp1_input>\d+)",
            "temp1_max" : r"(?m)^(?P<temp1_max>\d+)",
            "temp1_max_hyst" : r"(?m)^(?P<temp1_max_hyst>\d+)",
            "update_interval" : r"(?m)^(?P<update_interval>\d+)",
        },
    },
    "TERALYNX_LEFT" : {
        "PATH" : "/sys/bus/i2c/devices/14-0048/hwmon/hwmon7",
        "ATTRS" : {
            "name" : r"(?m)^(?P<name>lm75a)",

            "temp1_input" : r"(?m)^(?P<temp1_input>\d+)",
            "temp1_max" : r"(?m)^(?P<temp1_max>\d+)",
            "temp1_max_hyst" : r"(?m)^(?P<temp1_max_hyst>\d+)",
            "update_interval" : r"(?m)^(?P<update_interval>\d+)",
        },
    },
    "TERALYNX_LEFT_BACK_BOTTOM" : {
        "PATH" : "/sys/bus/i2c/devices/14-004b/hwmon/hwmon8",
        "ATTRS" : {
            "name" : r"(?m)^(?P<name>lm75a)",

            "temp1_input" : r"(?m)^(?P<temp1_input>\d+)",
            "temp1_max" : r"(?m)^(?P<temp1_max>\d+)",
            "temp1_max_hyst" : r"(?m)^(?P<temp1_max_hyst>\d+)",
            "update_interval" : r"(?m)^(?P<update_interval>\d+)",
        },
    },
    "TERALYNX_RIGHT_BACK_BOTTOM" : {
        "PATH" : "/sys/bus/i2c/devices/26-004a/hwmon/hwmon9",
        "ATTRS" : {
            "name" : r"(?m)^(?P<name>lm75a)",

            "temp1_input" : r"(?m)^(?P<temp1_input>\d+)",
            "temp1_max" : r"(?m)^(?P<temp1_max>\d+)",
            "temp1_max_hyst" : r"(?m)^(?P<temp1_max_hyst>\d+)",
            "update_interval" : r"(?m)^(?P<update_interval>\d+)",
        },
    },
    "TERALYNX_RIGHT" : {
        "PATH" : "/sys/bus/i2c/devices/26-004c/hwmon/hwmon10",
        "ATTRS" : {
            "name" : r"(?m)^(?P<name>lm75a)",

            "temp1_input" : r"(?m)^(?P<temp1_input>\d+)",
            "temp1_max" : r"(?m)^(?P<temp1_max>\d+)",
            "temp1_max_hyst" : r"(?m)^(?P<temp1_max_hyst>\d+)",
            "update_interval" : r"(?m)^(?P<update_interval>\d+)",
        },
    },
    "TERALYNX_FAN1" : {
        "PATH" : "/sys/bus/i2c/devices/6-004d/hwmon/hwmon4",
        "ATTRS" : {
            "name" : r"(?m)^(?P<name>lm75a)",

            "temp1_input" : r"(?m)^(?P<temp1_input>\d+)",
            "temp1_max" : r"(?m)^(?P<temp1_max>\d+)",
            "temp1_max_hyst" : r"(?m)^(?P<temp1_max_hyst>\d+)",
            "update_interval" : r"(?m)^(?P<update_interval>\d+)",
        },
    },
    "TERALYNX_FAN2" : {
        "PATH" : "/sys/bus/i2c/devices/6-004e/hwmon/hwmon5",
        "ATTRS" : {
            "name" : r"(?m)^(?P<name>lm75a)",

            "temp1_input" : r"(?m)^(?P<temp1_input>\d+)",
            "temp1_max" : r"(?m)^(?P<temp1_max>\d+)",
            "temp1_max_hyst" : r"(?m)^(?P<temp1_max_hyst>\d+)",
            "update_interval" : r"(?m)^(?P<update_interval>\d+)",
        },
    },
    "TERALYNX_FAN3" : {
        "PATH" : "/sys/bus/i2c/devices/6-004f/hwmon/hwmon6",
        "ATTRS" : {
            "name" : r"(?m)^(?P<name>lm75a)",

            "temp1_input" : r"(?m)^(?P<temp1_input>\d+)",
            "temp1_max" : r"(?m)^(?P<temp1_max>\d+)",
            "temp1_max_hyst" : r"(?m)^(?P<temp1_max_hyst>\d+)",
            "update_interval" : r"(?m)^(?P<update_interval>\d+)",
        },
    },
}

i2c_cd8200_fan_cpld_input = {
    "fan1_input" : r"(?m)^(?P<fan1_input>\d+)",
    "fan2_input" : r"(?m)^(?P<fan2_input>\d+)",
    "fan3_input" : r"(?m)^(?P<fan3_input>\d+)",
    "fan4_input" : r"(?m)^(?P<fan4_input>\d+)",
    "fan5_input" : r"(?m)^(?P<fan5_input>\d+)",
    "fan6_input" : r"(?m)^(?P<fan6_input>\d+)",
    "fan7_input" : r"(?m)^(?P<fan7_input>\d+)",
    "fan8_input" : r"(?m)^(?P<fan8_input>\d+)",
    "fan9_input" : r"(?m)^(?P<fan9_input>\d+)",
    "fan10_input" : r"(?m)^(?P<fan10_input>\d+)",
    "fan11_input" : r"(?m)^(?P<fan11_input>\d+)",
    "fan12_input" : r"(?m)^(?P<fan12_input>\d+)",
    "fan13_input" : r"(?m)^(?P<fan13_input>\d+)",
    "fan14_input" : r"(?m)^(?P<fan14_input>\d+)",
}

i2c_raw_access_comm_attrs = {
    "raw_access_data" : r"(?m)^(?P<raw_access_data>0x[0-9a-fA_F]+)",
    "raw_access_addr" : r"(?m)^(?P<raw_access_addr>0x[0-9a-fA_F]+)",
}

i2c_cd8200_fan_cpld_raw = {
    **i2c_raw_access_comm_attrs,
}

i2c_ir35215_comm_attrs = {
    "curr1_alarm" : r"(?m)^(?P<curr1_alarm>\d+)",
    "curr1_input" : r"(?m)^(?P<curr1_input>\d+)",
    "curr1_label" : r"(?m)^(?P<curr1_label>iin)",
    "curr1_max" : r"(?m)^(?P<curr1_max>\d+)",

    "curr2_alarm" : r"(?m)^(?P<curr2_alarm>\d+)",
    "curr2_crit" : r"(?m)^(?P<curr2_crit>\d+)",
    "curr2_input" : r"(?m)^(?P<curr2_input>\d+)",
    "curr2_label" : r"(?m)^(?P<curr2_label>iout1)",
    "curr2_max" : r"(?m)^(?P<curr2_max>\d+)",

    "curr3_alarm" : r"(?m)^(?P<curr3_alarm>\d+)",
    "curr3_crit" : r"(?m)^(?P<curr3_crit>\d+)",
    "curr3_input" : r"(?m)^(?P<curr3_input>\d+)",
    "curr3_label" : r"(?m)^(?P<curr3_label>iout2)",
    "curr3_max" : r"(?m)^(?P<curr3_max>\d+)",

    "in1_alarm" : r"(?m)^(?P<in1_alarm>\d+)",
    "in1_crit" : r"(?m)^(?P<in1_crit>\d+)",
    "in1_input" : r"(?m)^(?P<in1_input>\d+)",
    "in1_label" : r"(?m)^(?P<in1_label>vin)",
    "in1_min" : r"(?m)^(?P<in1_min>\d+)",

    "in2_crit" : r"(?m)^(?P<in2_crit>\d+)",
    "in2_crit_alarm" : r"(?m)^(?P<in2_crit_alarm>\d+)",
    "in2_input" : r"(?m)^(?P<in2_input>\d+)",
    "in2_label" : r"(?m)^(?P<in2_label>vout1)",
    "in2_lcrit" : r"(?m)^(?P<in2_lcrit>\d+)",
    "in2_lcrit_alarm" : r"(?m)^(?P<in2_lcrit_alarm>\d+)",
    "in2_max" : r"(?m)^(?P<in2_max>\d+)",
    "in2_max_alarm" : r"(?m)^(?P<in2_max_alarm>\d+)",
    "in2_min" : r"(?m)^(?P<in2_min>\d+)",
    "in2_min_alarm" : r"(?m)^(?P<in2_min_alarm>\d+)",

    "in3_crit" : r"(?m)^(?P<in3_crit>\d+)",
    "in3_crit_alarm" : r"(?m)^(?P<in3_crit_alarm>\d+)",
    "in3_input" : r"(?m)^(?P<in3_input>\d+)",
    "in3_label" : r"(?m)^(?P<in3_label>vout2)",
    "in3_lcrit" : r"(?m)^(?P<in3_lcrit>\d+)",
    "in3_lcrit_alarm" : r"(?m)^(?P<in3_lcrit_alarm>\d+)",
    "in3_max" : r"(?m)^(?P<in3_max>\d+)",
    "in3_max_alarm" : r"(?m)^(?P<in3_max_alarm>\d+)",
    "in3_min" : r"(?m)^(?P<in3_min>\d+)",
    "in3_min_alarm" : r"(?m)^(?P<in3_min_alarm>\d+)",

    "power1_alarm" : r"(?m)^(?P<power1_alarm>\d+)",
    "power1_input" : r"(?m)^(?P<power1_input>\d+)",
    "power1_label" : r"(?m)^(?P<power1_label>pin)",

    "power2_input" : r"(?m)^(?P<power2_input>\d+)",
    "power2_label" : r"(?m)^(?P<power2_label>pout1)",

    "power3_input" : r"(?m)^(?P<power3_input>\d+)",
    "power3_label" : r"(?m)^(?P<power3_label>pout2)",

    "temp1_crit" : r"(?m)^(?P<temp1_crit>\d+)",
    "temp1_crit_alarm" : r"(?m)^(?P<temp1_crit_alarm>\d+)",
    "temp1_input" : r"(?m)^(?P<temp1_input>\d+)",
    "temp1_max" : r"(?m)^(?P<temp1_max>\d+)",
    "temp1_max_alarm" : r"(?m)^(?P<temp1_max_alarm>\d+)",

    "temp2_crit" : r"(?m)^(?P<temp2_crit>\d+)",
    "temp2_crit_alarm" : r"(?m)^(?P<temp2_crit_alarm>\d+)",
    "temp2_max" : r"(?m)^(?P<temp2_max>\d+)",
    "temp2_input" : r"(?m)^(?P<temp2_input>\d+)",
    "temp2_max_alarm" : r"(?m)^(?P<temp2_max_alarm>\d+)",
}

i2c_cpld2n3_led_enable_comm_attr = {
    "led_enable" : r"(?m)^(?P<led_enable>\d)",
}

i2c_cpld2n3_led_color_comm_attr = {
    "led_color" : r"(?m)^(?P<led_color>\w+)",
}

i2c_ir35215_devices = {
    "DCDC-1" : {
        "PATH" : "/sys/bus/i2c/devices/23-0040/hwmon/hwmon15",
        "ATTRS" : {
            "name" : r"(?m)^(?P<name>ir35215)",

            **i2c_ir35215_comm_attrs,
        },
    },
    "DCDC-2" : {
        "PATH" : "/sys/bus/i2c/devices/24-004d/hwmon/hwmon16",
        "ATTRS" : {
            "name" : r"(?m)^(?P<name>ir35215)",

            **i2c_ir35215_comm_attrs,
        },
    },
    "DCDC-3" : {
        "PATH" : "/sys/bus/i2c/devices/25-0047/hwmon/hwmon17",
        "ATTRS" : {
            "name" : r"(?m)^(?P<name>ir35215)",

            **i2c_ir35215_comm_attrs,
        },
    },
}

i2c_asc10_comm_attrs = {
    "name" : r"(?m)^(?P<name>asc10)",

    "in1_input" : r"(?m)^(?P<in1_input>\d+)",
    "in1_label" : r"(?m)^(?P<in1_label>XP1R2V)",
    "in1_max" : r"(?m)^(?P<in1_max>\d+)",
    "in1_min" : r"(?m)^(?P<in1_min>\d+)",

    "in2_input" : r"(?m)^(?P<in2_input>\d+)",
    "in2_label" : r"(?m)^(?P<in2_label>PVDD0P8)",
    "in2_max" : r"(?m)^(?P<in2_max>\d+)",
    "in2_min" : r"(?m)^(?P<in2_min>\d+)",

    "in3_input" : r"(?m)^(?P<in3_input>\d+)",
    "in3_label" : r"(?m)^(?P<in3_label>TRVDD0R8V_1)",
    "in3_max" : r"(?m)^(?P<in3_max>\d+)",
    "in3_min" : r"(?m)^(?P<in3_min>\d+)",

    "in4_input" : r"(?m)^(?P<in4_input>\d+)",
    "in4_label" : r"(?m)^(?P<in4_label>TRVDD0R8V_2)",
    "in4_max" : r"(?m)^(?P<in4_max>\d+)",
    "in4_min" : r"(?m)^(?P<in4_min>\d+)",

    "in5_input" : r"(?m)^(?P<in5_input>\d+)",
    "in5_label" : r"(?m)^(?P<in5_label>XP3R3V_LEFT)",
    "in5_max" : r"(?m)^(?P<in5_max>\d+)",
    "in5_min" : r"(?m)^(?P<in5_min>\d+)",

    "in6_input" : r"(?m)^(?P<in6_input>\d+)",
    "in6_label" : r"(?m)^(?P<in6_label>TRVDD0R8V_1)",
    "in6_max" : r"(?m)^(?P<in6_max>\d+)",
    "in6_min" : r"(?m)^(?P<in6_min>\d+)",

    "in7_input" : r"(?m)^(?P<in7_input>\d+)",
    "in7_label" : r"(?m)^(?P<in7_label>TRVDD0R8V_2)",
    "in7_max" : r"(?m)^(?P<in7_max>\d+)",
    "in7_min" : r"(?m)^(?P<in7_min>\d+)",

    "in8_input" : r"(?m)^(?P<in8_input>\d+)",
    "in8_label" : r"(?m)^(?P<in8_label>PVDD0P8)",
    "in8_max" : r"(?m)^(?P<in8_max>\d+)",
    "in8_min" : r"(?m)^(?P<in8_min>\d+)",

    "in9_input" : r"(?m)^(?P<in9_input>\d+)",
    "in9_label" : r"(?m)^(?P<in9_label>XP3R3V_LEFT)",
    "in9_max" : r"(?m)^(?P<in9_max>\d+)",
    "in9_min" : r"(?m)^(?P<in9_min>\d+)",

    "in10_input" : r"(?m)^(?P<in10_input>\d+)",
    "in10_label" : r"(?m)^(?P<in10_label>XP12R0V)",
    "in10_max" : r"(?m)^(?P<in10_max>\d+)",
    "in10_min" : r"(?m)^(?P<in10_min>\d+)",

    "modalias" : r"(?m)^(?P<modalias>i2c:asc10)",

    "temp1_input" : r"(?m)^(?P<temp1_input>\d+)",
    "temp2_input" : r"(?m)^(?P<temp2_input>\d+)",
    "temp3_input" : r"(?m)^(?P<temp3_input>\d+)",
}

i2c_devices_tree = {
    "BOARD_VERSION" : {
        "PATH" : "/sys/bus/i2c/devices/8-0060/"
    },
    "LOGGER_DUMP" : {
        "PATH" : "/sys/bus/i2c/devices/8-0060",
        "ATTRS" : {
            "name" : r"(?m)^(?P<driver_name>cs8200_sys_cpld)",

            "board_version" : r"(?m)^(?P<board_version>0x[0-9a-fA-F]{2})",
            **i2c_raw_access_comm_attrs,
        },
    },
    "ASC10-1" : {
        "PATH" : "/sys/bus/i2c/devices/27-0060",
        "ATTRS" : {
            **i2c_asc10_comm_attrs,
        },
    },
    "ASC10-2" : {
        "PATH" : "/sys/bus/i2c/devices/27-0061",
        "ATTRS" : {
            **i2c_asc10_comm_attrs,
        },
    },
    **i2c_lm75_devices,
    "CD8200_FAN_CPLD" : {
        "PATH" : "/sys/bus/i2c/devices/5-0066",
        "ATTRS" : {
            "name" : r"(?m)^(?P<driver_name>cs8200_fan_cpld)",

            **i2c_cd8200_fan_cpld_input,
            **i2c_cd8200_fan_cpld_raw,
            "fan_watchdog_enable" : r"(?m)^(?P<fan_watchdog_enable>\d)",
        },
    },
    "PSU1_DPS_1500" : {
        "PATH" : "/sys/bus/i2c/devices/21-0059",
        "ATTRS" : {
            "name" : r"(?m)^(?P<name>dps_1500)",

            "curr1_input" : r"(?m)^(?P<curr1_input>\d+)",
            "curr1_label" : r"(?m)^(?P<curr1_label>current_input)",
            "curr1_max" : r"(?m)^(?P<curr1_max>15000)",
            "curr1_min" : r"(?m)^(?P<curr1_min>0)",

            "curr2_input" : r"(?m)^(?P<curr2_input>\d+)",
            "curr2_label" : r"(?m)^(?P<curr2_label>current_output)",
            "curr2_max" : r"(?m)^(?P<curr2_max>135000)",
            "curr2_min" : r"(?m)^(?P<curr2_min>0)",

            "fan1_alarm" : r"(?m)^(?P<fan1_alarm>\d+)",
            "fan1_fault" : r"(?m)^(?P<fan1_fault>\d+)",
            "fan1_input" : r"(?m)^(?P<fan1_input>\d+)",

            # "fan2_alarm" : r"(?m)^(?P<fan2_alarm>Fan2 is not installed on this PSU)",
            # "fan2_fault" : r"(?m)^(?P<fan2_fault>Fan2 is not installed on this PSU)",
            # "fan2_input" : r"(?m)^(?P<fan2_input>Fan2 is not installed on this PSUs)",

            "in1_input" : r"(?m)^(?P<in1_input>\d+)",
            "in1_label" : r"(?m)^(?P<in1_label>voltage_input)",
            "in1_max" : r"(?m)^(?P<in1_max>\d+)",
            "in1_min" : r"(?m)^(?P<in1_min>\d+)",

            "in2_input" : r"(?m)^(?P<in2_input>\d+)",
            "in2_label" : r"(?m)^(?P<in2_label>voltage_output)",
            "in2_max" : r"(?m)^(?P<in2_max>\d+)",
            "in2_min" : r"(?m)^(?P<in2_min>\d+)",

            "mfr_date" : r"(?m)^(?P<mfr_date>\d+\/\d+\/\d+)",
            "mfr_id" : r"(?m)^(?P<mfr_id>DELTA)",
            "mfr_model" : r"(?m)^(?P<mfr_model>TDPS-1500AB-6 B)",
            "mfr_serial" : r"(?m)^(?P<mfr_serial>[A-Z0-9]+)",
            "mfr_version" : r"(?m)^(?P<mfr_version>\d+)",

            "power1_input" : r"(?m)^(?P<power1_input>\d+)",
            "power1_label" : r"(?m)^(?P<power1_label>power_input)",
            "power1_max" : r"(?m)^(?P<power1_max>1900000)",

            "power2_input" : r"(?m)^(?P<power2_input>\d+)",
            "power2_label" : r"(?m)^(?P<power2_label>power_output)",
            "power2_max" : r"(?m)^(?P<power2_max>1650000)",

            "pwm1" : r"(?m)^(?P<pwm1>\d+)",
            # "pwm2" : r"(?P<pwm2>Fan2 is not installed on this PSU)",

            "temp1_alarm" : r"(?m)^(?P<temp1_alarm>\d+)",
            "temp1_input" : r"(?m)^(?P<temp1_input>\d+)",
        },
    },
    "PSU2_DPS_1500" : {
        "PATH" : "/sys/bus/i2c/devices/22-0058",
        "ATTRS" : {
            "name" : r"(?m)^(?P<name>dps_1500)",

            "curr1_input" : r"(?m)^(?P<curr1_input>\d+)",
            "curr1_label" : r"(?m)^(?P<curr1_label>current_input)",
            "curr1_max" : r"(?m)^(?P<curr1_max>15000)",
            "curr1_min" : r"(?m)^(?P<curr1_min>0)",

            "curr2_input" : r"(?m)^(?P<curr2_input>\d+)",
            "curr2_label" : r"(?m)^(?P<curr2_label>current_output)",
            "curr2_max" : r"(?m)^(?P<curr2_max>135000)",
            "curr2_min" : r"(?m)^(?P<curr2_min>0)",

            "fan1_alarm" : r"(?m)^(?P<fan1_alarm>\d+)",
            "fan1_fault" : r"(?m)^(?P<fan1_fault>\d+)",
            "fan1_input" : r"(?m)^(?P<fan1_input>\d+)",

            # "fan2_alarm" : r"(?m)^(?P<fan2_alarm>Fan2 is not installed on this PSU)",
            # "fan2_fault" : r"(?m)^(?P<fan2_fault>Fan2 is not installed on this PSU)",
            # "fan2_input" : r"(?m)^(?P<fan2_input>Fan2 is not installed on this PSU)",

            "in1_input" : r"(?m)^(?P<in1_input>\d+)",
            "in1_label" : r"(?m)^(?P<in1_label>voltage_input)",
            "in1_max" : r"(?m)^(?P<in1_max>\d+)",
            "in1_min" : r"(?m)^(?P<in1_min>\d+)",

            "in2_input" : r"(?m)^(?P<in2_input>\d+)",
            "in2_label" : r"(?m)^(?P<in2_label>voltage_output)",
            "in2_max" : r"(?m)^(?P<in2_max>\d+)",
            "in2_min" : r"(?m)^(?P<in2_min>\d+)",

            "mfr_date" : r"(?m)^(?P<mfr_date>\d+\/\d+\/\d+)",
            "mfr_id" : r"(?m)^(?P<mfr_id>DELTA)",
            "mfr_model" : r"(?m)^(?P<mfr_model>TDPS-1500AB-6 B)",
            "mfr_serial" : r"(?m)^(?P<mfr_serial>[A-Z0-9]+)",
            "mfr_version" : r"(?m)^(?P<mfr_version>\d+)",

            "power1_input" : r"(?m)^(?P<power1_input>\d+)",
            "power1_label" : r"(?m)^(?P<power1_label>power_input)",
            "power1_max" : r"(?m)^(?P<power1_max>1900000)",

            "power2_input" : r"(?m)^(?P<power2_input>\d+)",
            "power2_label" : r"(?m)^(?P<power2_label>power_output)",
            "power2_max" : r"(?m)^(?P<power2_max>1650000)",

            "pwm1" : r"(?m)^(?P<pwm1>\d+)",
            # "pwm2" : r"(?P<pwm2>Fan2 is not installed on this PSU)",

            "temp1_alarm" : r"(?m)^(?P<temp1_alarm>\d+)",
            "temp1_input" : r"(?m)^(?P<temp1_input>\d+)",
        },
    },
    "PSU1_EEPROM" : {
        "PATH" : "/sys/bus/i2c/devices/22-0050",
        "ATTRS" : {
            "name" : r"(?m)^(?P<name>24c02)",

            # For this attribute has to run with hexdump -C, as such put it to a higher level on *.robot
            # "eeprom" : r"(?m)^(?P<eeprom>????)",
        },
    },
    "PSU2_EEPROM" : {
        "PATH" : "/sys/bus/i2c/devices/21-0051",
        "ATTRS" : {
            "name" : r"(?m)^(?P<name>24c02)",

            # For this attribute has to run with hexdump -C, as such put it to a higher level on *.robot
            # "eeprom" : r"(?m)^(?P<eeprom>????)",
        },
    },
    **i2c_ir35215_devices,
    "CPLD2" : {
        "PATH" : "/sys/bus/i2c/devices/16-0063",
        "ATTRS" : {
            "name" : r"(?m)^(?P<name>led_cpld)",

            **i2c_raw_access_comm_attrs,
            **i2c_cpld2n3_led_enable_comm_attr,
            **i2c_cpld2n3_led_color_comm_attr,
        },
    },
    "CPLD3" : {
        "PATH" : "/sys/bus/i2c/devices/18-0064",
        "ATTRS" : {
            "name" : r"(?m)^(?P<name>led_cpld)",

            **i2c_raw_access_comm_attrs,
            **i2c_cpld2n3_led_enable_comm_attr,
            **i2c_cpld2n3_led_color_comm_attr,
        },
    },
}

diag_tools_cel_fan_test_show_current_pwm_patterns = [
    r"(?m)^[ \t]+PWM.*?\|.*?\|.*\|[ \t]+(?P<fan1_front_current_pwm>\d+)",
    r"(?m)^[ \t]+PWM.*?\|.*?\|.*\|[ \t]+(?P<fan1_panel_current_pwm>\d+)",

    r"(?m)^[ \t]+PWM.*?\|.*?\|.*\|[ \t]+(?P<fan2_front_current_pwm>\d+)",
    r"(?m)^[ \t]+PWM.*?\|.*?\|.*\|[ \t]+(?P<fan2_panel_current_pwm>\d+)",

    r"(?m)^[ \t]+PWM.*?\|.*?\|.*\|[ \t]+(?P<fan3_front_current_pwm>\d+)",
    r"(?m)^[ \t]+PWM.*?\|.*?\|.*\|[ \t]+(?P<fan3_panel_current_pwm>\d+)",

    r"(?m)^[ \t]+PWM.*?\|.*?\|.*\|[ \t]+(?P<fan4_front_current_pwm>\d+)",
    r"(?m)^[ \t]+PWM.*?\|.*?\|.*\|[ \t]+(?P<fan4_panel_current_pwm>\d+)",

    r"(?m)^[ \t]+PWM.*?\|.*?\|.*\|[ \t]+(?P<fan5_front_current_pwm>\d+)",
    r"(?m)^[ \t]+PWM.*?\|.*?\|.*\|[ \t]+(?P<fan5_panel_current_pwm>\d+)",

    r"(?m)^[ \t]+PWM.*?\|.*?\|.*\|[ \t]+(?P<fan6_front_current_pwm>\d+)",
    r"(?m)^[ \t]+PWM.*?\|.*?\|.*\|[ \t]+(?P<fan6_panel_current_pwm>\d+)",

    r"(?m)^[ \t]+PWM.*?\|.*?\|.*\|[ \t]+(?P<fan7_front_current_pwm>\d+)",
    r"(?m)^[ \t]+PWM.*?\|.*?\|.*\|[ \t]+(?P<fan7_panel_current_pwm>\d+)",
]

diag_tools_cel_fan_test_show_current_rpm_patterns = [
    r"(?m)^[ \t]+RPM.*?\|.*?\|.*\|[ \t]+(?P<fan1_front_current_rpm>\d+)",
    r"(?m)^[ \t]+RPM.*?\|.*?\|.*\|[ \t]+(?P<fan1_panel_current_rpm>\d+)",

    r"(?m)^[ \t]+RPM.*?\|.*?\|.*\|[ \t]+(?P<fan2_front_current_rpm>\d+)",
    r"(?m)^[ \t]+RPM.*?\|.*?\|.*\|[ \t]+(?P<fan2_panel_current_rpm>\d+)",

    r"(?m)^[ \t]+RPM.*?\|.*?\|.*\|[ \t]+(?P<fan3_front_current_rpm>\d+)",
    r"(?m)^[ \t]+RPM.*?\|.*?\|.*\|[ \t]+(?P<fan3_panel_current_rpm>\d+)",

    r"(?m)^[ \t]+RPM.*?\|.*?\|.*\|[ \t]+(?P<fan4_front_current_rpm>\d+)",
    r"(?m)^[ \t]+RPM.*?\|.*?\|.*\|[ \t]+(?P<fan4_panel_current_rpm>\d+)",

    r"(?m)^[ \t]+RPM.*?\|.*?\|.*\|[ \t]+(?P<fan5_front_current_rpm>\d+)",
    r"(?m)^[ \t]+RPM.*?\|.*?\|.*\|[ \t]+(?P<fan5_panel_current_rpm>\d+)",

    r"(?m)^[ \t]+RPM.*?\|.*?\|.*\|[ \t]+(?P<fan6_front_current_rpm>\d+)",
    r"(?m)^[ \t]+RPM.*?\|.*?\|.*\|[ \t]+(?P<fan6_panel_current_rpm>\d+)",

    r"(?m)^[ \t]+RPM.*?\|.*?\|.*\|[ \t]+(?P<fan7_front_current_rpm>\d+)",
    r"(?m)^[ \t]+RPM.*?\|.*?\|.*\|[ \t]+(?P<fan7_panel_current_rpm>\d+)",
]

diag_tools_asc10_comm_patterns = [
    r"(?mi)^ *1 *\| *\S+ *\| *\S+\| *[\d\.]+ *\| *(?P<in1_max>[\d\.]+) *\| *(?P<in1_min>[\d\.]+) *\| *(?P<in1_input>[\d\.]+) *\| *(?P<in1_result>Passed)",
    r"(?mi)^ *2 *\| *\S+ *\| *\S+\| *[\d\.]+ *\| *(?P<in2_max>[\d\.]+) *\| *(?P<in2_min>[\d\.]+) *\| *(?P<in2_input>[\d\.]+) *\| *(?P<in2_result>Passed)",
    r"(?mi)^ *3 *\| *\S+ *\| *\S+\| *[\d\.]+ *\| *(?P<in3_max>[\d\.]+) *\| *(?P<in3_min>[\d\.]+) *\| *(?P<in3_input>[\d\.]+) *\| *(?P<in3_result>Passed)",
    r"(?mi)^ *4 *\| *\S+ *\| *\S+\| *[\d\.]+ *\| *(?P<in4_max>[\d\.]+) *\| *(?P<in4_min>[\d\.]+) *\| *(?P<in4_input>[\d\.]+) *\| *(?P<in4_result>Passed)",
    r"(?mi)^ *5 *\| *\S+ *\| *\S+\| *[\d\.]+ *\| *(?P<in5_max>[\d\.]+) *\| *(?P<in5_min>[\d\.]+) *\| *(?P<in5_input>[\d\.]+) *\| *(?P<in5_result>Passed)",
    r"(?mi)^ *6 *\| *\S+ *\| *\S+\| *[\d\.]+ *\| *(?P<in6_max>[\d\.]+) *\| *(?P<in6_min>[\d\.]+) *\| *(?P<in6_input>[\d\.]+) *\| *(?P<in6_result>Passed)",
    r"(?mi)^ *7 *\| *\S+ *\| *\S+\| *[\d\.]+ *\| *(?P<in7_max>[\d\.]+) *\| *(?P<in7_min>[\d\.]+) *\| *(?P<in7_input>[\d\.]+) *\| *(?P<in7_result>Passed)",
    r"(?mi)^ *8 *\| *\S+ *\| *\S+\| *[\d\.]+ *\| *(?P<in8_max>[\d\.]+) *\| *(?P<in8_min>[\d\.]+) *\| *(?P<in8_input>[\d\.]+) *\| *(?P<in8_result>Passed)",
    r"(?mi)^ *9 *\| *\S+ *\| *\S+\| *[\d\.]+ *\| *(?P<in9_max>[\d\.]+) *\| *(?P<in9_min>[\d\.]+) *\| *(?P<in9_input>[\d\.]+) *\| *(?P<in9_result>Passed)",
    r"(?mi)^ *10 *\| *\S+ *\| *\S+\| *[\d\.]+ *\| *(?P<in10_max>[\d\.]+) *\| *(?P<in10_min>[\d\.]+) *\| *(?P<in10_input>[\d\.]+) *\| *(?P<in10_result>Passed)",
]

diag_tools_asc10_1_patterns = [
    r"(?m)^[ \t]*\d+[ \t]*\|[ \t]*asc10-1[ \t]*\|",
] + diag_tools_asc10_comm_patterns

diag_tools_asc10_2_patterns = [
    r"(?m)^[ \t]*\d+[ \t]*\|[ \t]*asc10-2[ \t]*\|",
] + diag_tools_asc10_comm_patterns

uboot_run_uploadonie_patterns = [
    r"(?m)^TFTP from server (?P<uboot_itb_server_ip>[\w\.]+); our IP address is (?P<uboot_itb_our_ip>[\w\.]+)",
    r"(?m)^Filename '(?P<uboot_tftp_itb_filename>[\w\-\.]+)'",
    r"(?m)^done$",
    r"(?m)Bytes transferred = (?P<uboot_itb_size_bytes>\d+)",
    r"(?m)^SF.*Erased: OK$",
    r"(?m)^SF.*Written: OK$",
]

uboot_tftpboot_patterns = [
    r"(?m)^TFTP from server (?P<uboot_tftp_server_ip>[\w\.]+); our IP address is (?P<uboot_tftp_our_ip>[\w\.]+)",
    r"(?m)^Filename '(?P<uboot_tftp_filename>[\w\-\.]+)'",
    r"(?m)^Load address: (?P<uboot_tftp_load_addr>\w+)",
    r"(?m)^[ \t]+(?P<uboot_tftp_speed>[\d\.]+.*\/s)$",
    r"(?m)^done$",
    r"(?m)^Bytes transferred = (?P<uboot_tftp_size_bytes>\d+)",
]

# This section to keep compatible for the existing code
device_15_0060_path = '/sys/bus/i2c/devices/8-0060/'
device_20_0056_path = '/sys/bus/i2c/devices/13-0056/'
device_5_0056_path = '/sys/bus/i2c/devices/5-0056/'
device_5_0066_path = '/sys/bus/i2c/devices/40-0066/'
device_31_0066_path = '/sys/bus/i2c/devices/31-0066/'


##### BSP TC11 Port Module Interrupt Test #####
interrupt_port_file_path = '/sys/devices/xilinx/accel-i2c/'
file_pre = 'port'
file_suf = '_module_interrupt'
interrupt_port_info_passpattern_list = ['^0', '^1']

psu_voltage_file_path = '/sys/bus/i2c/devices/8-0060/'
psu_filename = 'psu_voltage_fault'
voltage_passpattern = ['^0$']

##### BSP_TC12_Port_Module_Present_Test #####
present_file_pre = 'port'
present_file_suf = '_module_present'
present_passpattern_list = ['^0', '^1']

##### BSP_TC13_Port_Module_Reset_Test #####
reset_file_pre = 'port'
reset_file_suf = '_module_reset'
echo_value = '1'
port_module_reset_value = '0'
reset_passpattern_list1 = ['^0']
reset_passpattern_list2 = ['^1']

##### BSP_TC14_Port_Module_Lpmod_Test #####
lpmod_file_pre = 'port'
lpmod_file_suf = '_module_lpmod'
lpmod_default_value = '1'
lpmod_reset_value = '0'
lpmod_passpattern_list1 = ['^0']
lpmod_passpattern_list2 = ['^1']

##### BSP_TC19_PSU_Voltage_Up_Test #####
psu_voltage_up_file_path = '/sys/bus/i2c/devices/8-0060/'
psu_up_filename = 'psu_voltage_up'
voltage_up_passpattern = ['^0$']

##### BSP_TC23_System_Watchdog_Seconds_Test #####
watchdog_time_file = 'system_watchdog_seconds'
watchdog_enable_file = 'system_watchdog_enable'
watchdog_time_value = '10'
watchdog_enable_value = '1'
loop_times = 3
watchdog_time_pass_list = ['^0$']
watchdog_enable_pass_list = ['^0$']

##### BSP_TC29_LED_CPLD_Reset_Test #####
#platform_15_0060_path = '/sys/devices/platform/soc/fd880000.i2c-pld/i2c-0/i2c-4/i2c-15/15-0060/'
platform_15_0060_path = '/sys/devices/platform/soc/fd880000.i2c-pld/i2c-0/i2c-4/i2c-5/i2c-8/8-0060/'
led_cpld_reset = 'led_cpld_reset'
led_reset_value = '1'
led_reset_passpattern = ['^0$']

##### BSP_TC_30_I2C_Reset_Test #####
i2c_reset_file = 'i2c_reset'
i2c_reset_passpattern = ['^0$']
i2c_reset_value = '1'

##### BSP_TC33_Fan_CPLD_Reset_Test #####
fan_reset = 'fan_reset'
fan_reset_default_value = ['^0$']
fan_reset_value = '1'

##### BSP_TC34_ASIC(BCM5980)_Reset_Test #####
asic_reset = 'asic_reset'
asic_reset_reset_value = '1'
asic_reset_passpattern_list = ['^0$']

##### BSP_TC_35_LED_CPLD(CPLD2/3)_Reset_Test #####
led_cpld2_3_reset = 'led_cpld_reset'
led_cpld2_3_reset_value = '1'
led_cpld2_3_reset_passpattern = ['^0$']

##### BSP_TC36_QSFP_MUX[1..4]_Reset_Test #####
qsfp_mux_file_pre = 'qsfp_mux'
qsfp_mux_file_suf = '_reset'
qsfp_mux_passpattern_list1 = ['^0$']
qsfp_mux_passpattern_list2 = ['^1$']
qsfp_mux_default_value = '0'
qsfp_mux_reset_value = '1'

##### BSP_TC37_Swith_Board_EEPROM_Test #####
board_eeprom_wp = 'system_eeprom_wp'
board_eeprom = 'eeprom'
board_eeprom_cmd = 'eeprom | hexdump -C'
board_eeprom_default_passpattern = ['^1$']
board_eeprom_wp_reset_passpattern = ['^0$']
board_eeprom_reset_passpattern = ['^0$']
board_eeprom_wp_reset_value = '0'
board_eeprom_wp_default_value = '1'
board_eeprom_reset_value1 = '1234'
board_eeprom_reset_value2 = "-n -e '\x54\x6c\x76\x49\x6e\x66'"
board_eeprom_passpattern = list(map(lambda x: '000000' + str(x[2:]) + '.*\|.*\|', list(hex(a) for a in range(0, 14))))
board_eeprom_passpattern[0] = '0000000.*\|TlvInfo.*'
board_eeprom_reset_passpattern = copy.deepcopy(board_eeprom_passpattern)
board_eeprom_reset_passpattern[0] = '0000000.*\|1234.*'

##### eeprom common variables #####
cmd_close_eeprom_protect = 'echo "Close eeprom protect ..."'
cmd_open_eeprom_protect = 'echo "Open eeprom protect ..."'
cmd_val = 'val=`i2cget -y -f 15 0x60 0x05`'
cmd_i2cset = 'i2cset -y -f 15 0x60 0x05 0x0'
cmd_i2cset_val = 'i2cset -y -f 15 0x60 0x05 $val'

##### BSP TC38 Fan board EEPROM Test #####
fan_board_eeprom_str = 'eeprom | hexdump -C'
fan_board_eeprom = 'eeprom'
echo_fan_board_eeprom_value1 = '1234'
cd_device_5_0056_path_cmd = 'cd ' + device_5_0056_path
#echo_fan_board_eeprom_value2 = "-n -e '\x01\x00\x00\x01\x00\x00'" same as echo_fan_board_eeprom_value2 = "-n -e ...."
echo_fan_board_eeprom_value2 = "-n -e ...."
fan_board_eeprom_passpattern1 = ['000000.*\|\.+.*']
fan_board_eeprom_passpattern2 = ['000000.*31 32 33 34.*\|1234\.+.*']

##### BSP_TC40_FAN_Module_EEPROM_Test #####
fan_module_eeprom_path = '/sys/bus/i2c/devices/'
fan_module_eeprom_suf = '-0050/eeprom | hexdump -C'
fan_module_eeprom_passpattern1 = ['000000.*\|\.+.*']
fan_module_eeprom_value1 = '1234'
fan_module_eeprom_file_suf = '-0050/eeprom'
fan_module_eeprom_passpattern2 = ['000000.*\|1234\.+.*']
fan_module_eeprom_value2 = '-n -e ....'

##### BSP_TC45_Fan_Label_Test #####
fan_label_file_pre = 'fan'
fan_label_file_suf = '_label'
fan_label_pattern1_pre = 'fan'
fan_label_pattern1_suf = '-front'
fan_label_pattern2_pre = 'fan'
fan_label_pattern2_suf = '-rear'

##### BSP_TC47_Fan_max_Speed(RPM)_Test #####
fan_max_speed_path_pre = 'fan'
fan_max_speed_path_suf = '_max'
echo_max_speed = '65535'
fan_max_speed_passpattern1 = ['^\d+$']
fan_max_speed_passpattern2 = ['^65535$']

##### BSP_TC43_Fan_Direction_Test #####
fan_direction_file_pre = 'fan'
fan_direction_file_suf = '_direction'
fan_direction_passpattern = ['^0$']

##### BSP TC48 Fan min Speed(RPM)Test #####
fan_min_speed_path_pre = 'fan'
fan_min_speed_path_suf = '_min'
echo_min_speed = '1000'
echo_min_default = '0'
fan_min_speed_passpattern1 = ['^0$']
fan_min_speed_passpattern2 = ['^1000$']

##### BSP_TC49_Fan_Present_Test #####
fan_present_file_pre = 'fan'
fan_present_file_suf = '_present'
fan_present_passpattern = ['^1$']

##### BSP_TC50_Fan_board_EEPROM_protect_Test #####
fan_board_eeprom_protect = 'fan_board_eeprom_protect'
fan_board_eeprom_protect_value = '1'
fan_board_eeprom_protect_default = '0'
fan_board_eeprom_protect_passpattern1 = ['^0$']
fan_board_eeprom_protect_passpattern2 = ['^1$']

##### BSP_TC51_FAN_Watchdog_Enable_Test #####
fan_watchdog_export_cmd1 = 'export LD_LIBRARY_PATH=/root/diag/output'
fan_watchdog_export_cmd2 = 'export CEL_DIAG_PATH=/root/diag'
fan_watchdog_enable = 'fan_watchdog_enable'
cd_fan_watchdog_path = 'cd /root/diag'
fan_watchdog_test_cmd = './cel-fan-test -w -t pwm -D 50'
fan_watchdog_default = '1'
fan_watchdog_value = '0'
fan_watchdog_passpattern1 = ['^1$']
fan_watchdog_passpattern2 = ['^0$']

##### BSP_TC52_FAN_Watchdog_Seconds_Test #####
fan_watchdog_seconds = 'fan_watchdog_seconds'
fan_watchdog_seconds_default = '60'
fan_watchdog_seconds_value = '10'
fan_watchdog_seconds_passpattern1 = ['^60$']
fan_watchdog_seconds_passpattern2 = ['^10$']
fan_watchdog_path = '/root/diag'
fan_tool_name = 'cel-fan-test'
fan_test_option1 = '-w -t pwm -D 50'
fan_test_option2 = '--show'
fan_speed_pattern1 = ['\s+PWM.*255.*255']
fan_speed_pattern2 = ['\s+PWM.*255.*50']

##### BSP_TC53_Fan_Speed_PWM_test #####
fan_speed_pwm_pre = 'pwm'
fan_speed_pwm_value = '100'
fan_speed_pwd_default = '255'
fan_speed_pwm_passpattern1 = ['^255$']
fan_speed_pwm_passpattern2 = ['^100$']
