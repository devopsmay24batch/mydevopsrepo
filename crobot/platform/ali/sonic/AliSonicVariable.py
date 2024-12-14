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
devicename = os.environ.get("deviceName", "").lower()
logging.info("devicename:{}".format(devicename))
if "migaloo" in devicename:
    sys_i2c_devices_interfaces = ['1-0050', '0-0041', '0-0056', '1-0018'] + ['%d-0050' % i for i in range(17, 39)] + \
                                 ['%d-0050' % i for i in range(41, 63)] + ['%d-0050' % i for i in range(65, 127)] + \
                                 ['%d-0050' % i for i in range(129, 151)] + ['i2c-%d' % i for i in range(0, 153)] + \
                                 ['%d-00%d' % (i, j) for i in range(11, 17) for j in range(70, 73)]
    sys_i2c_devices_interfaces.remove('14-0072')
    sys_devices_platform = ['alarmtimer', 'AS24128D.switchboard', 'efivars.0', 'pcspkr', 'PNP0C0C:00', 'power', 'uevent', \
                            'AS24128D.cpldb', 'coretemp.0', 'microcode', 'platform-framebuffer.0', 'PNP0C14:00', 'serial8250']
    sys_switchboard_interfaces = ['CPLD1', 'CPLD2', 'CPLD3', 'CPLD4', 'CPLD5', 'CPLD6', 'driver', 'driver_override', \
                                  'FAN_CPLD', 'FPGA', 'modalias', 'power', 'SFF', 'subsystem', 'uevent']
    QSFP_num_list = ['QSFP%d' % i for i in range(1, 129)]
    sys_switch_SFF_interfaces = ['port_led_color', 'port_led_mode', 'power', 'subsystem', 'uevent'] + QSFP_num_list
    port_cpld = ['CPLD1', 'CPLD2', 'CPLD3', 'CPLD4', 'CPLD5', 'CPLD6']
    platform_name = 'x86_64-alibaba_as24-128d-cl-r0'
    platform = 'migaloo'
else:  # Shamu
    sys_i2c_devices_interfaces = ['1-0050', '0-0041', '0-0056', '1-0018'] + ['%d-0050' % i for i in range(13, 53)]+ \
                                 ['12-00%d' % i for i in range(70, 75)]
    sys_devices_platform = ['alarmtimer', 'AS1440D.cpldb', 'AS1440D.switchboard', 'coretemp.0', 'efivars.0', 'microcode', \
                            'pcspkr', 'platform-framebuffer.0', 'PNP0C0C:00', 'PNP0C14:00', 'power', 'serial8250', 'uevent']
    sys_switchboard_interfaces = ['CPLD1', 'CPLD2', 'driver', 'driver_override', 'FPGA', 'modalias', 'power', 'SFF', \
                                  'subsystem', 'uevent']
    QSFP_num_list = ['QSFP%d' % i for i in range(1, 41)]
    sys_switch_SFF_interfaces = ['port_led_color', 'port_led_mode', 'power', 'subsystem', 'uevent'] + QSFP_num_list
    port_cpld = ['CPLD1', 'CPLD2']
    platform_name = 'x86_64-alibaba_as14-40d-cl-r0'
    platform = 'shamu'


sys_switch_SFF_QSFP_interfaces = ['device', 'i2c', 'port_ctl', 'power', 'qsfp_lpmod', 'qsfp_modirq', 'qsfp_modprs',\
                                  'qsfp_modsel', 'qsfp_reset', 'sfp_modabs', 'sfp_rxlos', 'sfp_txdisable', 'sfp_txfault',\
                                  'subsystem', 'uevent']
sys_switch_SFF_QSFP_i2c_interfaces = ['dev_class', 'driver', 'eeprom', 'modalias', 'name', 'port_name', 'power', \
                                      'subsystem', 'uevent']
sysfs_interfaces = ['getreg', 'scratch', 'setreg']
sys_interfaces = ['block', 'bus', 'class', 'dev', 'devices', 'firmware', 'fs', 'hypervisor', 'kernel', 'module', 'power']
cat_getreg_cmd = 'cat getreg'
cat_scratch_cmd = 'cat scratch'
cat_version_cmd = 'cat version'
show_version_cmd = 'show version'
SWITCH_CPLD = 'SWITCH_CPLD'

sys_switch_interfaces = ['CPLD1', 'CPLD2', 'driver', 'driver_override', 'FPGA', 'modalias', 'power', 'SFF', \
                         'subsystem', 'uevent']
sys_BaseCPLD_interfaces = ['driver', 'driver_override', 'dump', 'getreg', 'modalias', 'power', 'scratch', 'setreg', \
                           'subsystem', 'sys_led', 'sys_led_color', 'uevent', 'version']
poap_file = ['poap.ok']
led_on = 'on'
led_off = 'off'
led_1k_blink = '1k'
led_4k_blink = '4k'
led_green = 'green'
led_yellow = 'yellow'
led_both = 'both'
diagos_login_info = [r'Linux sonic 4.9.0-11-2-amd64 #1 SMP Debian 4.9.189-3+deb9u2 (2019-11-11) x86_64', \
                     r'set serial console size', r'You are on', r'-- Software for Open Networking in the Cloud --', \
                     r'Unauthorized access and/or use are prohibited', 'All access and/or use are subject to monitoring', \
                     r'Help:    http://azure.github.io/SONiC/']
