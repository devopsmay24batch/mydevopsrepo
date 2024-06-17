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
# Variable file used for Silverstone_sit.robot
"""
Basic Settings
"""
CENTOS_MODE = 'sonic'
deviceType = "DUT"
PDU_Port = 4
response_end_flag = r"sys\s.*\dm.*\ds"
a_z_number_correspondence = {
    'a': 1, 'b': 2, 'c': 3, 'd': 4, 'e': 5, 'f': 6, 'g': 7, 'h': 8, 'i': 9, 'j': 10, 'k': 11, 'l': 12, 'm': 13, 'n': 14,
    'o': 15, 'p': 16, 'q': 17, 'r': 18, 's': 19, 't': 20, 'u': 21, 'v': 22, 'w': 23, 'x': 24, 'y': 25, 'z': 26}
dut_file_path = r"/home/white_box"
fru_list_standard_comparison_log = r"/home/sit/system_information/fru_list_standard.log"    # Don't modify
lspci_standard_comparison_log = r"/home/sit/system_information/lspci_standard.log"  # Don't modify

deb_diag_name = r"R3240-J0016-01-cel_diag-silverstoneX.v2.0.2.deb"  # diag tool name (deb file)
diag_tool_install_path = r"/home/cel_diag/silverstoneX"  # diag tool install in whitch path on dut
sdk_filename = r"R3240-J0025-01_V2.0.1_SilverstoneX_SDK.zip"   # sdk zip name (.zip)
"""
Case Settings
"""
# CPU
# cat /proc/cpuinfo
# lscpu
cpu_model_name = r"Intel(R) Xeon(R) CPU D-1627 @ 2.90GHz"
cpu_info_list = [{"cpu_MHz": [790, 3250]},  # Enter in the value range
                  {"cache_size": 6144},  # When L3 cache does not exist, enter ""
                  {"cpu_cores": 4},  # of Cores
                  {"thread_number": 8},  # of Threads
                  {"thread_per_core": 2}]  # of Thread(s) per core 'lscpu'


#BMC
ExistBMC = 'True'
full_bmc_version = "2.51.02"
status_error_list = ["no reading", "", "na", "0", "ns"]  # ipmitool sdr
# ipmitool fru list
# The python server stores the diff fail file path, try not to modify it
pc_path_fail_fru_list = r"/home/sit/system_information/fru_list"
shared_flag = "False"  # ipmitool lan print 8
# ipmitool lan print 1
str_ip_address_source = r"DHCP Address"
str_bmc_ip = r"10.10.10.171"
str_subnet_mask = r"255.255.255.0"
str_mac = r"00:93:af:e5:c2:82"
bmc_sw_main_minor = "ipmitool raw 0x32 0x8f 7"  # check bmc main or minor command

# PCI
# lspci
# The python server stores the diff fail file path, try not to modify it
pc_path_fail_lspci = r"/home/sit/system_information/lspci"
# lspci -vvv
lnkcap_list = [{'03:00.0': ('2.5GT/s', 'x1')}, {'03:00.1': ('2.5GT/s', 'x1')}, {'09:00.0': ('2.5GT/s', 'x1')},
               {'0a:00.0': ('5GT/s', 'x1')}]

# eg [{"0b:00.0": ('2.5GT/s', 'x1')}] or [] # when it is [],the following will not be checked
lnksta_list = [{'03:00.0': ('2.5GT/s', 'x1')}, {'03:00.1': ('2.5GT/s', 'x1')}, {'09:00.0': ('2.5GT/s', 'x1')},
               {'0a:00.0': ('5GT/s', 'x1')}]
# eg [{"0b:00.0": ('2.5GT/s', 'x1')}] or [] # when it is [],above will not be checked

# [{device name: [[CESta ignore], [DevSta ignore], [UESta ignore]]}]
# [{"00:05.0": [["NonFatalErr+"], ["CorrErr+","UnsuppReq+"],[]]}]
ce_de_ue_ignore_list = []
bios_version = r"2.02.00"  # dmidecode -t bios

#LAN
# ifconfig -a
# e.g [{"eth0": ("inet","netmask", "broadcast", "ether", "RX errors", "TX errors")}]
# ps:If the broadcast field does not exist, write "" in the broadcast field value
os_ip_list = [{"eth0": ("10.10.10.8", "255.255.255.0", "10.10.10.255", "0c:48:c6:c3:58:54", "0", "0")}]
# enthtool Network
ethool_speed_link_detected_dict = {"eth0": "1000 yes"}  # ethtool {'Network port name': 'speed+Space+Link_detected'}


#BIOS
vendor = r"American Megatrends Inc."  # When it is "", it will not  be checked
release_date = r"11/25/2021"  # When it is "", it will not  be checked
bios_sw_main_minor = "ipmitool raw 0x3a 0x64 0 1 0x70"  # check bios main or minor command

#DIMM
memtotal_G = 32  # cat /proc/meminfo
free_g = 29  # free -g
mem_num = 2  # number of memory
# dmidecode -t memory
dmi_memory_info_list = [{"size": ['16384 MB', '16384 MB']},
                        {"manufacturer": ['InnoDisk', 'InnoDisk']},
                        {"serial_number": ['1898002A', '1D3A003A']},
                        {"part_number": ['M4D0-AGS1QCUN', 'M4D0-AGS1QCUN']},
                        {"configured_clock_speed": ['2133 MHz', '2133 MHz']},
                        {"speed": ['2933 MHz', '2933 MHz']}]


#SSD
M2_ssd_number = 1  # lsblk
device_model = ["NETLIST SSD32GB-002"]  # Device Model
serial_number = ['511191218133000007']  # Serial Number
firmware_version = ["SBFMU1.1"]  # Firmware Version
user_capacity = ["32.0"]  # User Capacity

# OS_log
dmesg_error_list = ["scsi hang", "Blocked for more than", "call trace", "machine check events", "resetting link",
                    "Media error", "I/O error", "FPDMA", "Emask", "task abort", "correctable error", "Ata error", 
                    "Unrecovered read error", "Temperature above threshold", "transmit timed out", "out of memory", 
                    "TSC unstable"]  # dmesg
sel_error_list = ["single bit error", "going low", "single-bit ECC", "NMI", "Non-recoverable",
                    "going high", "Redundancy Lost", "Correctable ECC", "Uncorrectable ECC", "error",
                    "Critical", "Deasserted", "degraded", "unavailable", "IERR", "CATEER"]  #sel
messages_error_list = ["hardware error", "buffer i/o error", "MCA", "above temperature", "block & removing handle",
                    "pcie error", "hard resetting link"]  # messages

# Case: Reboot Cycling Test
reboot_cycle_time = 501

# Case: AC_Power_Cycling_Test
ac_power_cycle_time = 1002

# Case: DC_Power_Cycling_Test
dc_power_cycle_time = 501

# Case: Boot from USB Flash Drive/USB DVD
set_u_disk_first_boot = ["RIGHT", "RIGHT", "RIGHT", "RIGHT", "RIGHT", "DOWN", "DOWN", "DOWN", "DOWN", "DOWN", "DOWN",
                         "ENTER", "ENTER", "DOWN", "ENTER", "ESC", "RIGHT", "ENTER", "ENTER"]
resume_normal_boot = ["RIGHT", "RIGHT", "RIGHT", "RIGHT", "RIGHT", "DOWN", "DOWN", "DOWN", "DOWN", "DOWN", "DOWN",
                      "ENTER", "ENTER", "DOWN", "ENTER", "ESC", "RIGHT", "ENTER", "ENTER"]
u_disk_os_flag = r"ONIE: Rescue"

# Case: File_Transfers_From_HDD_To_USB_Devices
usb_mount_name = '/dev/sdb'

# Case: USB Link Speed
usb_min_speed = 10
cmd_usb_name = ['dev/sdb']

# Case: Memory performance
expect_min_num = 12000

# Case: Full loading stress test
runing_time = 2  # unit:Day
stressapptest_pass_keyword = r"Status: PASS - please verify no corrected errors"
fio_pass_keyword = r"Disk stats (read/write)"
pc_log_path = r"/home/white_box_log/sit"
cpu_full_load_path = r"/home/white_box/sit_cpu_full_load"
set_wait_time = runing_time * 3600 * 24 + 60
memtester_loop = 1
dut_cpu_platform = r"Grangeville- Broadwell DE"
cpu_platform_dict = {
    "Harrisonville- Denverton SoC": ["567138", "denverton-ptu-linux-rev1-1"],
    "Purley- Skylake/Cascade Lake": ["560556", "ptugen", "ptumon"],
    "Grangeville- Broadwell DE": ["556068", "BroadwellPTU_Re", "BroadwellPwrMon"],
    "River Forest - Broadwell": ["571108", "ptugen", "ptumon"],
    "Grantley- Broadwell": ["571108", "ptugen", "ptumon"],
    "Brickland - Broadwell": ["571108", "ptugen", "ptumon"],
    "River Forest - Haswell": ["536231", "ptugen", "ptumon"],
    "Grantley- Haswell": ["536231", "ptugen", "ptumon"],
    "Brickland - Haswell": ["536231", "ptugen", "ptumon"],
    "Edisonville- Rangeley": ["540527", "avoton-ptu-1-4"],
    "River Forest - Coleto Creek Chipset": ["544090", "intel-communications-chipsets"],
    "Highland Forest - Coleto Creek Chipset": ["544090", "intel-communications-chipsets"],
    "Glen Forest - Coleto Creek Chipset": ["544090", "intel-communications-chipsets"]
}


# ######################################### Caleb Start ############################################################
# Case : Read_write_function_Check
storage_min_speed = 400  # unit : MB/sec
cmd_storage_name = ['/dev/sda']

# Case : USB_full_loading_test
usb_fio_running_time = 1  # unit:hours
# usb_device_name = ['/dev/sdc']
USB_full_loading_path = r"/home/white_box/USB_full_loading"
fio_expected_value = 15

# Case : Speedstep
Speedstep_path = r"/home/white_box/Speedstep"
expect_disable_frequency = [2100, 2300]   # Enter in the value range of disable_frequency
expect_enable_frequency = [2300, 2500]    # Enter in the value range of enable_frequency
enter_speedstep_setup_interface = ["RIGHT", "RIGHT", "DOWN", "ENTER"]   # Switch to the speedstep setting interface
# change speedstep status and switch to the save interface
setup_speedstep_step = ["ENTER", "DOWN", "ENTER", "ESC", "LEFT", "LEFT", "LEFT"]

# Case : Port_connect_test
check_cmd = r"cat /proc/cpuinfo"
check_keyword = ["model name"]

# Case : i2c_read_write
i2c_read_cmd_and_exp_res = {
    "i2cget -y -f 0 0x18 0x05": "0xc1",     # "read i2c command":"expect result"
    "i2cget -y -f 0 0x18 0x06": "0x10"      # "read i2c command":"expect result"
}
# write i2c cmd  e.g:i2cset -y -f 0 0x18 0x05 0xc1 (0xc1 is the value to be write)
i2c_write_cmd = ["i2cset -y -f 0 0x18 0x05 0xc1", "i2cset -y -f 0 0x18 0x06 0x10"]

diag_i2c_read_cmd = r"./cel-i2c-bmc-test -r -p /dev/i2c-8 -A 0x0d -R 0x26 -C 1"
diag_i2c_write_cmd = r"./cel-i2c-bmc-test  -w -p /dev/i2c-8 -A 0x0d -R 0x32 -D 0x20 -C 1"


# Case : i2c_stress
i2c_stress_running_time = 12   # unit:hour

# Case : system_idle_testing
system_idle_time = 12   # unit:hour ,EVT for 12 hours , DVT for 24 hours

# Case : SSD Performance
ssd_performance_path = r"/home/white_box/ssd_performance"
LIST__ssd_name = ["/dev/sdb"]
# Fill in the expected value in the order of "LIST__ssd_name"
DICT__expect_ssd_performance = { # 80% performance of the drive spec
    "/dev/sdb": {
        "config_1": {
            "min_bw": 1,
            "min_IOPS": 1
        },
        "config_2": {
            "min_bw": 1,
            "min_IOPS": 1
        }
    },
    "/dev/sdc": {

    },
}
DICT__fio_config = {    # Parameters can be added and modified according to requirements
    "/dev/sdb": {
        "config_1": r"--runtime=60 --size=100% --group_reporting=1 --bs=4K --ioengine=libaio --iodepth=64 "
                    r"--rw=randread --name=preheat --numjobs=4 --direct=1",  # runtime unit:seconds
        "config_2": r"--runtime=60 --size=100% --group_reporting=1 --bs=8K --ioengine=libaio --iodepth=64 "
                    r"--rw=randread --name=preheat --numjobs=4 --direct=1"
    },
    "/dev/sdc": {

    },
}

# Case: USB IO performance
DICT__usb_performance = {
    "/dev/sdb": 30,  # e.g "device name": min_speed  unit:MB/sec
}

# Case: Power_Consumption_test
expect_consumption = {
    "idle_mode": [200, 400],  # Power range under idle mode
    "full_loading": [300, 600]  # Power range under full_loading mode
}


# Case: PSU Redundant stress test
# This case needs to manually remove one of the psu cable

# Case: LAN_Speed_Auto_negotiation
# This case need to Check NIC LED by yourself
management_port_name = r"eth0"

# Case : 25G Optical module Traffic Test


# Case : 100G Optical module Traffic Test
start_100G_optical_cmd = r"tx 100 pbm=ce0 vlan=200"
stop_100G_optical_cmd = r"port ce0 en=off"

# Case : CPU performance
# lnkpack config:
psize = 15000
expect_min_gflops = "1.05000e+02"

# Case:10G_port_enable_disable_function_test
tenG_port_name = "eth0"

# Case:IPv6 Test
dut_nic_name = "eth0"
dut_ipv6 = r"2001:250:4000:2000::53"
pc_nic_name = r"ens256"
pc_ipv6 = r"2001:250:4000:2000::54"
# netperf
dut_netperf_name = r"netperf_2.7.0-0.1_amd64.deb"
pc_netperf_name = r"netperf-2.7.0-1.el7.lux.x86_64.rpm"
# expect_throughput_via_ipv6 = 900   # unit:MB/s

#  Case:Link_Speed_Check_by_full_test(1G RJ45 port)
one_G_net_name = "eth0"
one_G_exp_lan_link_speed = r"1000Mb/s"
one_G_exp_bw = 1000

#  Case:LAN Speed check(Auto and Manual)
# This case need to Check NIC LED by yourself

#  Case: PSU_Info_and_Hot_Plug
psu_hot_plug_num = 1    # The number of psu of the machine
psu_hot_plug_cycle = 1  # Hot plug cycle for each psu
psu_unplug_flag = r"Presence detected | Deasserted"     # unplug log flag in "ipmitool sel list"
psu_insert_flag = r"Presence detected | Asserted"       # insert log flag in "ipmitool sel list"
hot_plug_sel_error_list = ["single bit error", "single-bit ECC", "NMI", "Non-recoverable",
                    "going high", "Redundancy Lost", "Correctable ECC", "Uncorrectable ECC", "error",
                    "degraded", "unavailable", "IERR", "CATEER"]  # sel

# Case: Power_cable_Hot_Plug
power_cable_hot_plug_num = 1    # The number of psu of the machine
power_cable_hot_plug_cycle = 1  # Hot plug cycle for each psu
psu_cable_unplug_flag = r"Power Supply AC lost | Asserted"  # unplug log flag in "ipmitool sel list"
psu_cable_insert_flag = r"Power Supply AC lost | Deasserted"    # insert log flag in "ipmitool sel list"

# Case: Fan_Hot_Plug
fan_hot_plug_num = 1  # The number of fan of the machine
fan_hot_plug_cycle = 1  # Hot plug cycle for each fan
fan_unplug_flag = r"Absent | Asserted"   # unplug log flag in "ipmitool sel list"
fan_insert_flag = r"Present | Asserted"     # insert log flag in "ipmitool sel list"
front_fan_max_rpm = [23000, 25000]  # front fan max rpm when unplug fan
rear_fan_max_rpm = [28000, 30000]   # rear fan max rpm when unplug fan


# Case: Fan_tray_Hot_Plug
fan_tray_hot_plug_num = 1  # The number of fan_tray of the machine
fan_tray_hot_plug_cycle = 1     # Hot plug cycle for each fan_tray
fan_num_in_tray = 1     # Fan number in each fan tray
fan_tray_unplug_flag = r"Absent | Asserted"  # unplug log flag in "ipmitool sel list"
fan_tray_insert_flag = r"Present | Asserted"    # insert log flag in "ipmitool sel list"

# Case: RJ45_cable_Hot_Plug
rj_hot_plug_num = 1     # The number of rj45 port of the machine
rj_hot_plug_cycle = 1   # Hot plug cycle for each rj45 port
rj_unplug_flag = r"NIC Link is Down"    # unplug log flag in "dmesg"
rj_insert_flag = r"NIC Link is Up"      # insert log flag in "dmesg"

# Case: USB_device_Hot_Plug
usb_hot_plug_num = 1    # The number of usb port of the machine
usb_hot_plug_cycle = 1  # Hot plug cycle for each usb port
usb_unplug_flag = r"USB disconnect"   # unplug log flag in "dmesg"
usb_insert_flag = r"New USB device found"     # insert log flag in "dmesg"


#  Case:Link_Speed_Check_by_full_test(10G SFP+ port)
ten_G_net_name = "eth0"
ten_G_exp_lan_link_speed = r"1000Mb/s"
ten_G_exp_bw = 1000

# Case: Optical_module_eeprom_access_Test
diag_check_eeprom_cmd = r"./cel-qsfp-test --all"
present_status = r"present"
qsfp_present_num = 4
sfp_present_num = 2
qsfp_vendor_name = r""
qsfp_part_number = r""
sfp_vendor_name = r""
sfp_part_number = r""

# ######################################### Caleb END ###############################################################


# ######################################### Janson Start ############################################################
"""
SDK common setting
"""
sdk_path = "/home/R3240-J0025-01_V2.0.2_SilverstoneX_SDK/"
cls_name = "cls_shell "
sdk_sh = r"auto_load_user.sh"
pre_emphasis_configure_file = r"preemphasis_PAM4_400G_32_3MDAC_v2.txt"
# ps:sdk config file name
pam4_400g_32_config = "PAM4_400G_32"
pam4_200g_64_config = "PAM4_200G_64"
pam4_100g_128_config = "PAM4_100G_128"
nrz_200g_32_config = "NRZ_200G_32"
nrz_100g_64_config = "NRZ_100G_64"
nrz_50g_128_config = "NRZ_50G_128"
nrz_40g_64_config = "NRZ_40G_64"
nrz_25g_128_config = "NRZ_25G_128"
nrz_10g_128_config = "NRZ_10G_128"

# ps:if don't want to test all port,set special_port_num variable
special_port_num = 4

rate_num_config = {pam4_400g_32_config: [400, 1], pam4_200g_64_config: [200, 2], pam4_100g_128_config: [100, 4],
                   nrz_200g_32_config: [200, 1], nrz_100g_64_config: [100, 2], nrz_50g_128_config: [50, 4],
                   nrz_40g_64_config: [40, 2], nrz_25g_128_config: [25, 4], nrz_10g_128_config: [10, 4]}

# case:loopback_pam4_400g_traffic_test
port_num_pam4_400g = special_port_num
# case:loopback_pam4_200g_traffic_test
port_num_pam4_200g = special_port_num * 2
# case:loopback_pam4_100g_traffic_test
port_num_pam4_100g = special_port_num * 4
# case:nrz_200g_32_config
port_num_nrz_200g = special_port_num
# case:nrz_100g_32_config
port_num_nrz_100g = special_port_num * 2
# case:loopback_nrz_50g_traffic_test
port_num_nrz_50g = special_port_num * 4
# case:loopback_nrz_40g_traffic_test
port_num_nrz_40g = special_port_num * 2
# case:loopback_nrz_25g_traffic_test
port_num_nrz_25g = special_port_num * 4
# case:loopback_nrz_10g_traffic_test
port_num_nrz_10g = special_port_num * 4

# case:static_function_test
exp_eth_ip = '10.10.10.89'
exp_eth = 'eth0'

# case:port_enable_disable_function_test
set_enable_disable_name = "eth0"

# cae:1Gb_10Gb_performance
# not need add unit
exp_lan_link_bw = 1000

# case:link_speed_check_by_manual
# need to add unit Mb/s
exp_lan_link_speed = r"1000Mb/s"
exp_lan_name = "eth0"


"""
Diag common setting
"""
diag_path = r"/home/cel_diag/silverstoneX/bin"


# case:loopback_info_check
# ps:default all loopback vendor and pn is same.
cel_qsfp_test = "cel-qsfp-test"
qsfp_vendor = "LUXSHARE-ICT"
qsfp_pn = "LR3DD001-SD-R"
loopback_num = special_port_num


check_command = "check_qsfp.sh"
key_word = "present"
exp_nums = 0

# ######################################### Janson END ############################################################

# case:dac_info_check
# ps:default all loopback vendor and pn is same.
dac_qsfp_vendor = "LUXSHARE-TECH"
dac_qsfp_pn = "LZKDD002-SD-R"
dac_num = special_port_num

# case:Optical_module_info_check
# ps:default all loopback vendor and pn is same.
module_qsfp_vendor = "LUXSHARE-TECH"
module_qsfp_pn = "LZKDD002-SD-R"
module_num = special_port_num
