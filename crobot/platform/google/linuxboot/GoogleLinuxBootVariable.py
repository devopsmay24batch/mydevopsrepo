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
from GoogleConst import STOP_AUTOBOOT_PROMPT, STOP_AUTOBOOT_KEY


pc_info = DeviceMgr.getServerInfo('PC')
dev_info = DeviceMgr.getDevice()

diagos_mode = BOOT_MODE_DIAGOS
uboot_mode = BOOT_MODE_UBOOT
onie_mode = BOOT_MODE_ONIE

# SwImage shared objects
# CPLD = SwImage.getSwImage("CPLD")
# UBOOT = SwImage.getSwImage("UBOOT")
# End of SwImage shared objects

uboot_prompt = dev_info.promptUboot

tftp_server_ipv4 = pc_info.managementIP
tftp_interface = dhcp_interface = mgmt_interface = "eth0"
# mgmt_server_ip = pc_info.managementIP


###tcs 06###

linux_menu=['Welcome to LinuxBoot\'s Menu',
'Enter a number to boot a kernel:',
'01. SONiC-OS-202106-brixia.pb20',
'02. Reboot',
'03. Enter a LinuxBoot shell',
"Enter an option (\'01\' is the default, 'e' to edit kernel cmdline):"]
linux_version='Linux version 5.4.23\+ \(user\@host\) \(gcc version 8.3.0 \(Debian 8.3.0-6\)\)'



###tcs08###

i2cdetect_list = ['i2c-3.*smbus.*i2c-0-mux.*SMBus adapter',
'i2c-10102.*i2c.*i2c-10100-mux.*I2C adapter',
'i2c-10130.*i2c.*i2c-10100-mux.*I2C adapter',
'i2c-20.*i2c.*i2c-11-mux.*I2C adapter',
'i2c-10120.*i2c.*i2c-10100-mux.*I2C adapter',
'i2c-10  i2c.*i2c-ocores.*.*I2C adapter',
'i2c-10110.*i2c.*i2c-10100-mux.*I2C adapter',
'i2c-1   i2c.*i2c-ocores.*.*I2C adapter',
'i2c-10100.*i2c.*GFPGA adapter.*I2C adapter',
'i2c-29  smbus.*iMC socket.*SMBus adapter',
'i2c-10129.*i2c.*i2c-10100-mux.*I2C adapter',
'i2c-19  i2c.*i2c-10-mux.*I2C adapter',
'i2c-10119.*i2c.*i2c-10100-mux.*I2C adapter',
'i2c-10109.*i2c.*i2c-10100-mux.*I2C adapter',
'i2c-27  i2c.*i2c-11-mux.*I2C adapter',
'i2c-10127.*i2c.*i2c-10100-mux.*I2C adapter',
'i2c-10004.*i2c.*i2c-10000-mux.*I2C adapter',
'i2c-17  i2c.*i2c-10-mux.*I2C adapter',
'i2c-10117.*i2c.*i2c-10100-mux.*I2C adapter',
'i2c-8   smbus.*i2c-0-mux.* SMBus adapter',
'i2c-10107.*i2c.*i2c-10100-mux.*I2C adapter',
'i2c-25  i2c.*i2c-11-mux.*I2C adapter',
'i2c-10125.*i2c.*i2c-10100-mux.*I2C adapter',
'i2c-10002.*i2c.*i2c-10000-mux.*I2C adapter',
'i2c-15  i2c.*i2c-10-mux .*I2C adapter',
'i2c-10115.*i2c.*i2c-10100-mux.*I2C adapter',
'i2c-6   smbus.*i2c-0-mux.*SMBus adapter',
'i2c-10105.*i2c.*i2c-10100-mux.*I2C adapter',
'i2c-10133.*i2c.*i2c-10100-mux.*I2C adapter',
'i2c-23  i2c.*i2c-11-mux.*I2C adapter',
'i2c-10123.*i2c.*i2c-10100-mux.*I2C adapter',
'i2c-10000.*i2c.*GFPGA adapter.*I2C adapter',
'i2c-13  i2c.*i2c-10-mux.*I2C adapter',
'i2c-10113.*i2c.*i2c-10100-mux.*I2C adapter',
'i2c-4   smbus.*i2c-0-mux.* SMBus adapter',
'i2c-10103.*i2c.*i2c-10100-mux.*I2C adapter',
'i2c-10131.*i2c.*i2c-10100-mux.*I2C adapter',
'i2c-21  i2c.*i2c-11-mux.*I2C adapter',
'i2c-10121.*i2c.*i2c-10100-mux.*I2C adapter',
'i2c-11  i2c.*i2c-ocores.*I2C adapter',
'i2c-10111.*i2c.*i2c-10100-mux.*I2C adapter',
'i2c-2   smbus.*i2c-0-mux.* SMBus adapter',
'i2c-10101.*i2c.*i2c-10100-mux.*I2C adapter',
'i2c-0   smbus.*SMBus I801 adapter at 3020.*SMBus adapter',
'i2c-28  smbus.*iMC socket 0 for channel pair 0-1.*SMBus adapter',
'i2c-10128.*i2c.*i2c-10100-mux.*I2C adapter',
'i2c-18  i2c.*i2c-10-mux.*I2C adapter',
'i2c-10118.*i2c.*i2c-10100-mux.*I2C adapter',
'i2c-9   smbus.*i2c-0-mux.* SMBus adapter',
'i2c-10108.*i2c.*i2c-10100-mux.*I2C adapter',
'i2c-26  i2c.*i2c-11-mux.*I2C adapter',
'i2c-10126.*i2c.*i2c-10100-mux.*I2C adapter',
'i2c-10003.*i2c.*i2c-10000-mux.*I2C adapter',
'i2c-16  i2c.*i2c-10-mux.*I2C adapter',
'i2c-10116.*i2c.*i2c-10100-mux.*I2C adapter',
'i2c-7   smbus.*i2c-0-mux.*SMBus adapter',
'i2c-10106.*i2c.*i2c-10100-mux.*I2C adapter',
'i2c-10134.*i2c.*i2c-10100-mux.*I2C adapter',
'i2c-24  i2c.*i2c-11-mux.*I2C adapter',
'i2c-10124.*i2c.*i2c-10100-mux.*I2C adapter',
'i2c-10001.*i2c.*i2c-10000-mux.*I2C adapter',
'i2c-14  i2c.*i2c-10-mux.*I2C adapter',
'i2c-10114.*i2c.*i2c-10100-mux.*I2C adapter',
'i2c-5   smbus.*i2c-0-mux.*SMBus adapter',
'i2c-10104.*i2c.*i2c-10100-mux.*I2C adapter',
'i2c-10132.*i2c.*i2c-10100-mux.*I2C adapter',
'i2c-22  i2c.*i2c-11-mux.*I2C adapter',
'i2c-10122.*i2c.*i2c-10100-mux.*I2C adapter',
'i2c-12  i2c.*i2c-10-mux.*I2C adapter',
'i2c-10112.*i2c.*i2c-10100-mux.*I2C adapter']



lscpu = ['Architecture:        x86_6',
        'CPU op-mode\(s\):.*32-bit, 64-bit',
        'Byte Order:          Little Endian',
        'CPU\(s\):              16',
        'Vendor ID:           GenuineIntel',
        'CPU family:          6',
        'Model:               86',
        'Model name:          Intel\(R\) Xeon\(R\) CPU D-1649N @ 2.30GHz',
        'Stepping:            5',
        'Virtualization:      VT-x']

cpu_proc=[]
for i in range(0,16):
    cpu_proc.append('processor.*:.*'+str(i))
    cpu_proc.append('vendor_id.*:.*GenuineIntel')
    cpu_proc.append('cpu family.*:.*6')
    cpu_proc.append('model.*:.*86')
    cpu_proc.append('model name.*:.*Intel\(R\) Xeon\(R\) CPU D-1649N @ 2.30GHz')
    cpu_proc.append('stepping.*:.*5')
    cpu_proc.append('microcode.*:.*0xe00000f')
    cpu_proc.append('cpu cores.*:.*8')
    cpu_proc.append('fpu.*:.*yes')
    cpu_proc.append('fpu_exception.*:.*yes')
    cpu_proc.append('cpuid level.*:.*20')
    cpu_proc.append('wp.*:.*yes')


fdisk=['Disk /dev/sda: 44.7 GiB, 48020152320 bytes, 93789360 sectors',
        '/dev/sda1    2048     6143     4096    2M BIOS boot',
        '/dev/sda2    6144   268287   262144  128M ONIE boot',
        '/dev/sda3  268288 67377151 67108864   32G Linux filesystem',
        'Disk /dev/loop0: .*',
        'Disk /dev/loop1: 4 GiB, 4294967296 bytes, 8388608 sectors']
ifconfig=['Bridge: flags=4099<UP,BROADCAST,MULTICAST>  mtu 9100',
          'Loopback0: flags=195<UP,BROADCAST,RUNNING,NOARP>  mtu 65536',
          'docker0: flags=4099<UP,BROADCAST,MULTICAST>  mtu 1500',
          'eth0: flags=4163<UP,BROADCAST,RUNNING,MULTICAST>  mtu 1500',
          'lo: flags=73<UP,LOOPBACK,RUNNING>  mtu 65536']



# ......................... TC_027 PCIE Bus Scan .........................

show_pci_device_with_slot_cmds = []
linuxboot_pci_device_pattern = """
.*Intel Corporation Xeon E7 v4/Xeon E5 v4/Xeon E3 v4/Xeon D DMI2
.*Intel Corporation Xeon E7 v4/Xeon E5 v4/Xeon E3 v4/Xeon D PCI Express Root Port 1
.*Intel Corporation Xeon E7 v4/Xeon E5 v4/Xeon E3 v4/Xeon D PCI Express Root Port 1
.*Intel Corporation Xeon E7 v4/Xeon E5 v4/Xeon E3 v4/Xeon D PCI Express Root Port 2
.*Intel Corporation Xeon E7 v4/Xeon E5 v4/Xeon E3 v4/Xeon D PCI Express Root Port 2
.*Intel Corporation Xeon E7 v4/Xeon E5 v4/Xeon E3 v4/Xeon D PCI Express Root Port 2
.*Intel Corporation Xeon E7 v4/Xeon E5 v4/Xeon E3 v4/Xeon D PCI Express Root Port 2
.*Intel Corporation Xeon E7 v4/Xeon E5 v4/Xeon E3 v4/Xeon D PCI Express Root Port 3
.*Intel Corporation Xeon E7 v4/Xeon E5 v4/Xeon E3 v4/Xeon D PCI Express Root Port 3
.*Intel Corporation Xeon E7 v4/Xeon E5 v4/Xeon E3 v4/Xeon D Crystal Beach DMA Channel 0
.*Intel Corporation Xeon E7 v4/Xeon E5 v4/Xeon E3 v4/Xeon D Crystal Beach DMA Channel 1
.*Intel Corporation Xeon E7 v4/Xeon E5 v4/Xeon E3 v4/Xeon D Crystal Beach DMA Channel 2
.*Intel Corporation Xeon E7 v4/Xeon E5 v4/Xeon E3 v4/Xeon D Crystal Beach DMA Channel 3
.*Intel Corporation Xeon E7 v4/Xeon E5 v4/Xeon E3 v4/Xeon D Crystal Beach DMA Channel 4
.*Intel Corporation Xeon E7 v4/Xeon E5 v4/Xeon E3 v4/Xeon D Crystal Beach DMA Channel 5
.*Intel Corporation Xeon E7 v4/Xeon E5 v4/Xeon E3 v4/Xeon D Crystal Beach DMA Channel 6
.*Intel Corporation Xeon E7 v4/Xeon E5 v4/Xeon E3 v4/Xeon D Crystal Beach DMA Channel 7
.*Intel Corporation Xeon E7 v4/Xeon E5 v4/Xeon E3 v4/Xeon D Map/VTd_Misc/System Management
.*Intel Corporation Xeon E7 v4/Xeon E5 v4/Xeon E3 v4/Xeon D IIO Hot Plug
.*Intel Corporation Xeon E7 v4/Xeon E5 v4/Xeon E3 v4/Xeon D IIO RAS/Control Status/Global Errors
.*Intel Corporation Xeon E7 v4/Xeon E5 v4/Xeon E3 v4/Xeon D I/O APIC
.*Intel Corporation 8 Series/C220 Series Chipset Family USB xHCI
.*Intel Corporation 8 Series/C220 Series Chipset Family USB EHCI #2
.*Intel Corporation 8 Series/C220 Series Chipset Family PCI Express Root Port #1
.*Intel Corporation 8 Series/C220 Series Chipset Family PCI Express Root Port #2
.*Intel Corporation 8 Series/C220 Series Chipset Family PCI Express Root Port #3
.*Intel Corporation 8 Series/C220 Series Chipset Family USB EHCI #1
.*Intel Corporation C224 Series Chipset Family Server Standard SKU LPC Controller
.*Intel Corporation 8 Series/C220 Series Chipset Family 6-port SATA Controller 1.*
.*Intel Corporation 8 Series/C220 Series Chipset Family SMBus Controller
.*Broadcom Limited b996
.*Intel Corporation 6f54
.*Intel Corporation Ethernet Connection X552 10 GbE SFP+
.*Google, Inc. 0065
.*Intel Corporation I210 Gigabit Network Connection
.*Intel Corporation Xeon E7 v4/Xeon E5 v4/Xeon E3 v4/Xeon D R3 QPI Link 0/1
.*Intel Corporation Xeon E7 v4/Xeon E5 v4/Xeon E3 v4/Xeon D R3 QPI Link Debug
.*Intel Corporation Xeon E7 v4/Xeon E5 v4/Xeon E3 v4/Xeon D Caching Agent
.*Intel Corporation Xeon E7 v4/Xeon E5 v4/Xeon E3 v4/Xeon D R2PCIe Agent
.*Intel Corporation Xeon E7 v4/Xeon E5 v4/Xeon E3 v4/Xeon D Ubox
.*Intel Corporation Xeon E7 v4/Xeon E5 v4/Xeon E3 v4/Xeon D Home Agent 0
.*Intel Corporation Xeon E7 v4/Xeon E5 v4/Xeon E3 v4/Xeon D Memory Controller 0 - Target Address/Thermal/RAS
.*Intel Corporation Xeon E7 v4/Xeon E5 v4/Xeon E3 v4/Xeon D Memory Controller 0 - Channel Target Address Decoder
.*Intel Corporation Xeon E7 v4/Xeon E5 v4/Xeon E3 v4/Xeon D DDRIO Channel 0/1 Broadcast
.*Intel Corporation Xeon E7 v4/Xeon E5 v4/Xeon E3 v4/Xeon D DDRIO Global Broadcast
.*Intel Corporation Xeon E7 v4/Xeon E5 v4/Xeon E3 v4/Xeon D Memory Controller 0 - Channel 0 Thermal Control
.*Intel Corporation Xeon E7 v4/Xeon E5 v4/Xeon E3 v4/Xeon D Memory Controller 0 - Channel 1 Thermal Control
.*Intel Corporation Xeon E7 v4/Xeon E5 v4/Xeon E3 v4/Xeon D Memory Controller 0 - Channel 0 Error
.*Intel Corporation Xeon E7 v4/Xeon E5 v4/Xeon E3 v4/Xeon D Memory Controller 0 - Channel 1 Error
.*Intel Corporation Xeon E7 v4/Xeon E5 v4/Xeon E3 v4/Xeon D DDRIO Channel 0/1 Interface
.*Intel Corporation Xeon E7 v4/Xeon E5 v4/Xeon E3 v4/Xeon D Memory Controller 0 - Channel 2 Thermal Control
.*Intel Corporation Xeon E7 v4/Xeon E5 v4/Xeon E3 v4/Xeon D Memory Controller 0 - Channel 3 Thermal Control
.*Intel Corporation Xeon E7 v4/Xeon E5 v4/Xeon E3 v4/Xeon D Memory Controller 0 - Channel 2 Error
.*Intel Corporation Xeon E7 v4/Xeon E5 v4/Xeon E3 v4/Xeon D Memory Controller 0 - Channel 3 Error
.*Intel Corporation Xeon E7 v4/Xeon E5 v4/Xeon E3 v4/Xeon D Power Control Unit
""".splitlines()
sonic_pci_device_pattern = [
    "00.*Host bridge:.*",
    "00.*System peripheral:.*",
    "00.*PIC: .*",
    "00.*USB controller:.*",
    "00.*Communication controller:.*",
    "00.*IDE interface:.*",
    "00.*Serial controller:.*",
    "00.*PCI bridge:.*",
    "00.*ISA bridge:.*",
    "00.*SATA controller:.*",
    "00.*SMBus: .*",
    "01.*Ethernet controller:.*",
    "02.*Co-processor:.*",
    "03.*Ethernet controller:.*",
    "04.*Ethernet controller:.*",
    "07.*Ethernet controller:.*",
    "08.*Ethernet controller:.*",
    "ff.*Performance counters:.*",
]
pci_slots = [
    "01:00.0",
    "02:00.0",
    "03:00.0",
    "03:00.1",
    "04:00.0",
    "04:00.1",
    "06:00.0",
    "07:00.0",
    "08:00.0"
]
for each in pci_slots:
    cmd = "lspci -s {} -vvvxxx".format(each)
    show_pci_device_with_slot_cmds.append(cmd)

# ......................... TC_028 PCIE Configuration Test .........................

pcie_config_cmd1 = [
    "02:00.0",
    "03:00.0",
    "03:00.1",
    "04:00.0",
    "04:00.1"
]

pcie_config_cmd2 = [
    "msi",
    "bridge",
    "Device",
    '"Speed 2.5GT/s"',
    '"Speed 5GT/s"',
    '"Speed 8GT/s"'
]

# ......................... TC_29 CPU I2C/SMBus/SMLink Interface Test .........................

i2c_detect_list_pattern = [
    "i2c-3   smbus           i2c-0-mux [(]chan_id 1[)]                   SMBus adapter",
    "i2c-10102       i2c             i2c-10100-mux [(]chan_id 1[)]               I2C adapter",
    "i2c-10130       i2c             i2c-10100-mux [(]chan_id 29[)]              I2C adapter",
    "i2c-10120       i2c             i2c-10100-mux [(]chan_id 19[)]              I2C adapter",
    "i2c-10  i2c             i2c-ocores                              I2C adapter",
    "i2c-10110       i2c             i2c-10100-mux [(]chan_id 9[)]               I2C adapter",
    "i2c-1   i2c             i2c-ocores                              I2C adapter",
    "i2c-10100       i2c             GFPGA adapter                           I2C adapter",
    "i2c-10129       i2c             i2c-10100-mux [(]chan_id 28[)]              I2C adapter",
    "i2c-10119       i2c             i2c-10100-mux [(]chan_id 18[)]              I2C adapter",
    "i2c-10109       i2c             i2c-10100-mux [(]chan_id 8[)]               I2C adapter",
    "i2c-10127       i2c             i2c-10100-mux [(]chan_id 26[)]              I2C adapter",
    "i2c-10004       i2c             i2c-10000-mux [(]chan_id 3[)]               I2C adapter",
    "i2c-10117       i2c             i2c-10100-mux [(]chan_id 16[)]              I2C adapter",
    "i2c-8   smbus           i2c-0-mux [(]chan_id 6[)]                   SMBus adapter",
    "i2c-10107       i2c             i2c-10100-mux [(]chan_id 6[)]               I2C adapter",
    "i2c-10125       i2c             i2c-10100-mux [(]chan_id 24[)]              I2C adapter",
    "i2c-10002       i2c             i2c-10000-mux [(]chan_id 1[)]               I2C adapter",
    "i2c-10115       i2c             i2c-10100-mux [(]chan_id 14[)]              I2C adapter",
    "i2c-6   smbus           i2c-0-mux [(]chan_id 4[)]                   SMBus adapter",
    "i2c-10105       i2c             i2c-10100-mux [(]chan_id 4[)]               I2C adapter",
    "i2c-10133       i2c             i2c-10100-mux [(]chan_id 32[)]              I2C adapter",
    "i2c-10123       i2c             i2c-10100-mux [(]chan_id 22[)]              I2C adapter",
    "i2c-10000       i2c             GFPGA adapter                           I2C adapter",
    "i2c-10113       i2c             i2c-10100-mux [(]chan_id 12[)]              I2C adapter",
    "i2c-4   smbus           i2c-0-mux [(]chan_id 2[)]                   SMBus adapter",
    "i2c-10103       i2c             i2c-10100-mux [(]chan_id 2[)]               I2C adapter",
    "i2c-10131       i2c             i2c-10100-mux [(]chan_id 30[)]              I2C adapter",
    "i2c-10121       i2c             i2c-10100-mux [(]chan_id 20[)]              I2C adapter",
    "i2c-11  i2c             i2c-ocores                              I2C adapter",
    "i2c-10111       i2c             i2c-10100-mux [(]chan_id 10[)]              I2C adapter",
    "i2c-2   smbus           i2c-0-mux [(]chan_id 0[)]                   SMBus adapter",
    "i2c-10101       i2c             i2c-10100-mux [(]chan_id 0[)]               I2C adapter",
    "i2c-10128       i2c             i2c-10100-mux [(]chan_id 27[)]              I2C adapter",
    "i2c-10118       i2c             i2c-10100-mux [(]chan_id 17[)]              I2C adapter",
    "i2c-9   smbus           i2c-0-mux [(]chan_id 7[)]                   SMBus adapter",
    "i2c-10108       i2c             i2c-10100-mux [(]chan_id 7[)]               I2C adapter",
    "i2c-10126       i2c             i2c-10100-mux [(]chan_id 25[)]              I2C adapter",
    "i2c-10003       i2c             i2c-10000-mux [(]chan_id 2[)]               I2C adapter",
    "i2c-10116       i2c             i2c-10100-mux [(]chan_id 15[)]              I2C adapter",
    "i2c-7   smbus           i2c-0-mux [(]chan_id 5[)]                   SMBus adapter",
    "i2c-10106       i2c             i2c-10100-mux [(]chan_id 5[)]               I2C adapter",
    "i2c-10134       i2c             i2c-10100-mux [(]chan_id 33[)]              I2C adapter",
    "i2c-10124       i2c             i2c-10100-mux [(]chan_id 23[)]              I2C adapter",
    "i2c-10001       i2c             i2c-10000-mux [(]chan_id 0[)]               I2C adapter",
    "i2c-10114       i2c             i2c-10100-mux [(]chan_id 13[)]              I2C adapter",
    "i2c-5   smbus           i2c-0-mux [(]chan_id 3[)]                   SMBus adapter",
    "i2c-10104       i2c             i2c-10100-mux [(]chan_id 3[)]               I2C adapter",
    "i2c-10132       i2c             i2c-10100-mux [(]chan_id 31[)]              I2C adapter",
    "i2c-10122       i2c             i2c-10100-mux [(]chan_id 21[)]              I2C adapter",
    "i2c-10112       i2c             i2c-10100-mux [(]chan_id 11[)]              I2C adapter",
]

i2c_detect_ls_pattern = ["lrwxrwxrwx 1 root root 0 Jul 25 17:00 /sys/bus/i2c/devices/i2c-1 ->.*"]

i2c_detect_y_pattern = [
    "     0  1  2  3  4  5  6  7  8  9  a  b  c  d  e  f",
    "00:",
    "10:",
    "20:",
    "30:             (UU|34)",
    "40:",
    "50:",
    "60:",
    "70:"
]

# ......................... TC_030_CPU_LPC_Interface_Test .........................

come_cpld_ports = [
    "0xa100",
    "0xa101",
    "0xa1e0",
    "0xa1e1",
]

# ......................... TC_21 EEPROM update test .........................

powercycle_cmd = "echo 0x4449454a > /sys/devices/gfpga-platform/board_powercycle"

eeprom_help_pattern = [
    "usage:",
    "Options are:",
    "--all           Test all configure options",
    "--dump          Dump eeprom info",
    "-v, --version       Display the version and exit",
    "-h, --help          Display this help text and exit",
    "-f, --file          Defined configuration file",
    "-l, --list          List yaml information",
    "-d, --dev           .device id. run -l for see all device id",
    "-t, --type          .eeprom type:tlv.",
    "-D, --data          .data information.",
    "-A, --addr          .TLV address. run -l to see support address",
    "",
    "",
    "Example:",
    "-h , --help                                          Show this help menu",
    "--all                                                Program eeprom[(]TLV[)] by default config information",
    "-r -d 1 -t tlv                                       Read device id TLV information",
    '-w -d 1 -t tlv -A product_name -D "ELM-Capitaine"    Write TLV information to defined address',
    "--dump -d 1 -t tlv                                   Dump device id TLV raw data"
]

tlv_post = "TLV info default config value:"
tlv_path = "/sys/bus/i2c/devices/i2c-"
default_config_values=[
    "product_name     =.*",
    "pn               =.*",
    "sn               =.*",
    "mac_address      =.*",
    "mfg_date         =.*",
    "card_type        =.*",
    "hw_revision      =.*",
    "board_pn         =.*",
    "board_sn         =.*",
    "mac_count        =.*",
    "psu_type         =.*",
    "margin_low       =.*",
    "margin_high      =.*",
    "margin_off       =.*",
    "subassy_pn       =.*",
    "subassy_sn       =.*",
    "fan_maxspeed     =.*",
    "fan_pn           =.*",
    "---------------------------------------------------------------------------------------",
]

device_list = [
    "come",
    "come",
    "baseboard",
    "switch",
    "fan-1",
    "fan-2",
    "fan-3",
    "fan-4"
]

eeprom_list_pattern = [
    "=================================== EEPROM list cfg ===================================",
    "",
    "---------------------------------------------------------------------------------------",
    "group:1, type: tlv, format: tlv, dev_num:8",
    "---------------------------------------------------------------------------------------",
    "| id |          name        |                            dev_path                     |",
    "---------------------------------------------------------------------------------------",
    "|  1 | come                 | /sys/bus/i2c/devices/i2c-1/1-0050                       |",
    "|  2 | come                 | /sys/bus/i2c/devices/i2c-1/1-0051                       |",
    "|  3 | baseboard            | /sys/bus/i2c/devices/i2c-19/19-0051                     |",
    "|  4 | switch               | /sys/bus/i2c/devices/i2c-10001/10001-0050               |",
    "|  5 | fan-1                | /sys/bus/i2c/devices/i2c-12/12-0050                     |",
    "|  6 | fan-2                | /sys/bus/i2c/devices/i2c-13/13-0050                     |",
    "|  7 | fan-3                | /sys/bus/i2c/devices/i2c-14/14-0050                     |",
    "|  8 | fan-4                | /sys/bus/i2c/devices/i2c-15/15-0050                     |",
    "---------------------------------------------------------------------------------------",
]

for each in device_list:
    a = each+" TLV info default config value:"
    eeprom_list_pattern.append(a)
    for b in default_config_values:
        eeprom_list_pattern.append(b)

eeprom_hexdump_dirs = [
    "1/1-0050",
    "1/1-0051",
    "19/19-0051",
    "10001/10001-0050",
    "12/12-0050",
    "13/13-0050",
    "14/14-0050",
    "15/15-0050",
]

tlv_come_cmd1 = [
    'pn -D "R3152-M0001-01"',
    'sn -D "R1207-G0002-01XXXXXXXX"',
    'mac_address -D "00:1A:11:01:02:03"',
    'mfg_date -D "2042"',
    'card_type -D "0x54"',
    'hw_revision -D "0x01"',
    'board_pn -D "ABC1234567-01"',
    'board_sn -D "161812345678901"',
    'mac_count -D "128"',
    'psu_type -D "0xDC"'
]

tlv_come_cmd2 = [
    'pn -D "R3153-M0001-01"',
    'sn -D "R1307-G0002-01XXXXXXXX"',
    'mac_address -D "00:3A:11:01:02:03"',
    'mfg_date -D "3043"',
    'card_type -D "0x56"',
    'hw_revision -D "0x03"',
    'board_pn -D "ABC1234567-03"',
    'board_sn -D "161833345678901"',
    'mac_count -D "127"',
    'psu_type -D "0xDB"'
]

tlv_baseboard_cmd1 = [
    'product_name -D "BX"',
    'pn -D "1075455-02"',
    'sn -D "TMBCTH194201434"',
    'mac_address -D "00:1A:11:44:55:66"',
    'mfg_date -D "2042"',
    'card_type -D "0x60"',
    'hw_revision -D "0x01"',
    'board_pn -D "1075637-02"',
    'board_sn -D "abc123456"',
    'mac_count -D "CBX07248404"',
    'psu_type -D "0xDC"'
]

tlv_baseboard_cmd2 = [
    'product_name -D "CX"',
    'pn -D "1075455-03"',
    'sn -D "TMBCTH194301434"',
    'mac_address -D "00:1A:22:33:44:55"',
    'mfg_date -D "3043"',
    'card_type -D "0x52"',
    'hw_revision -D "0x23"',
    'board_pn -D "2475637-32"',
    'board_sn -D "abc232323"',
    'mac_count -D "CBX77778404"',
    'psu_type -D "0xAC"'
]

tlv_switchboard_cmd1 = [
    'mfg_date -D "2042"',
    'card_type -D "0x61"',
    'hw_revision -D "0x01"',
    'board_pn -D "R3152-M0001-01"',
    'board_sn -D "12345678"',
    'psu_type -D "0xDC"',
    'subassy_pn -D "ABC1234567-01"',
    'subassy_sn -D "161812345678901"'
]

tlv_switchboard_cmd2 = [
    'mfg_date -D "3343"',
    'card_type -D "0x88"',
    'hw_revision -D "0x88"',
    'board_pn -D "R3152-M8881-88"',
    'board_sn -D "12123434"',
    'psu_type -D "0xBC"',
    'subassy_pn -D "BCD2312165-01"',
    'subassy_sn -D "363832345678903"'
]

tlv_fan_cmd1 = [
    'pn -D "R1257-F0002-01"',
    'sn -D "12345678"',
    'mfg_date -D "2042"',
    'card_type -D "0x64"',
    'hw_revision -D "0x01"',
    'board_pn -D "112233-44"',
    'board_sn -D "abc123456"',
    'psu_type -D "0xDC"',
    'fan_maxspeed -D "22000"',
    'fan_pn -D "R40W12BGNL9"'
]

tlv_fan_cmd2 = [
    'pn -D "R3267-F0002-01"',
    'sn -D "22233345"',
    'mfg_date -D "3044"',
    'card_type -D "0x128"',
    'hw_revision -D "0x33"',
    'board_pn -D "333333-33"',
    'board_sn -D "abc333456"',
    'psu_type -D "0xAC"',
    'fan_maxspeed -D "22222"',
    'fan_pn -D "R44W44BGNL4"'
]

write_tlf_commands1 = [tlv_come_cmd1, tlv_come_cmd1, tlv_baseboard_cmd1, tlv_switchboard_cmd1]
for i in range(4):
    write_tlf_commands1.append(tlv_fan_cmd1)

write_tlf_commands2 = [tlv_come_cmd2, tlv_come_cmd2, tlv_baseboard_cmd2, tlv_switchboard_cmd2]
for i in range(4):
    write_tlf_commands2.append(tlv_fan_cmd2)
##tc 24##
cpu_microcode_ver=[".* microcode: sig=0x50665, pf=0x10, revision=0xe00000f",
                   ".* microcode: Microcode Update Driver: v2.2."]


#TC14
Memory_info_sonic = [
        "MemTotal:.*kB",
        "MemFree:.*kB",
        "MemAvailable:.*kB",
        "Buffers:.*kB",
        "Cached:.*kB",
        "SwapCached:.*kB",
        "Active:.*kB",
        "Inactive:.*kB",
        "Active.*(anon).*:.*kB",
        "Inactive.*(anon).*:.*kB",
        "Active.*(file).*:.*kB",
        "Inactive.*(file).*:.*kB",
        "Unevictable:.*kB",
        "Mlocked:.*kB",
        "SwapTotal:.*kB",
        "SwapFree:.*kB",
        "Dirty:.*kB",
        "Writeback:.*kB",
        "AnonPages:.*kB",
        "Mapped:.*kB",
        "Shmem:.*kB",
        "Slab:.*kB",
        "SReclaimable:.*kB",
        "SUnreclaim:.*kB",
        "KernelStack:.*kB",
        "PageTables:.*kB",
        "NFS_Unstable:.*kB",
        "Bounce:.*kB",
        "WritebackTmp:.*kB",
        "CommitLimit:.*kB",
        "Committed_AS:.*kB",
        "VmallocTotal:.*kB",
        "VmallocUsed:.*kB",
        "VmallocChunk:.*kB",
        "Percpu:.*kB",
        "HardwareCorrupted:.*kB",
        "AnonHugePages:.*kB",
        "ShmemHugePages:.*kB",
        "ShmemPmdMapped:.*kB",
        "HugePages_Total:.*",
        "HugePages_Free:.*",
        "HugePages_Rsvd:.*",
        "HugePages_Surp:.*",
        "Hugepagesize:.*kB",
        "Hugetlb:.*kB",
        "DirectMap4k:.*kB",
        "DirectMap2M:.*kB",
        "DirectMap1G:.*kB"
        ]
Memory_info_linuxboot = [
        "MemTotal:.*kB",
        "MemFree:.*kB",
        "MemAvailable:.*kB",
        "Buffers:.*kB",
        "Cached:.*kB",
        "SwapCached:.*kB",
        "Active:.*kB",
        "Inactive:.*kB",
        "Active.*(anon).*:.*kB",
        "Inactive.*(anon).*:.*kB",
        "Active.*(file).*:.*kB",
        "Inactive.*(file).*:.*kB",
        "Unevictable:.*kB",
        "Mlocked:.*kB",
        "SwapTotal:.*kB",
        "SwapFree:.*kB",
        "Dirty:.*kB",
        "Writeback:.*kB",
        "AnonPages:.*kB",
        "Mapped:.*kB",
        "Shmem:.*kB",
        "Slab:.*kB",
        "SReclaimable:.*kB",
        "SUnreclaim:.*kB",
        "KernelStack:.*kB",
        "PageTables:.*kB",
        "NFS_Unstable:.*kB",
        "Bounce:.*kB",
        "WritebackTmp:.*kB",
        "CommitLimit:.*kB",
        "Committed_AS:.*kB",
        "VmallocTotal:.*kB",
        "VmallocUsed:.*kB",
        "VmallocChunk:.*kB",
        "Percpu:.*kB",
        "DirectMap4k:.*kB",
        "DirectMap2M:.*kB",
        "DirectMap1G:.*kB"
        ]



# .................... TC 025 CPU Frequency Check Under Full Loading ....................

lscpu_pattern = """Architecture:        x86_64
CPU op-mode[(]s[)]:      32-bit, 64-bit
Byte Order:          Little Endian
Address sizes:       46 bits physical, 48 bits virtual
CPU[(]s[)]:              16
On-line CPU[(]s[)] list: 0-15
Thread[(]s[)] per core:  2
Core[(]s[)] per socket:  8
Socket[(]s[)]:           1
NUMA node[(]s[)]:        1
Vendor ID:           GenuineIntel
CPU family:          6
Model:               86
Model name:          Intel[(]R[)] Xeon[(]R[)] CPU D-1649N @ 2.30GHz
Stepping:            5
CPU MHz:             .*
CPU max MHz:         .*
CPU min MHz:         800.0000
BogoMIPS:            .*
Virtualization:      VT-x
L1d cache:           32K
L1i cache:           32K
L2 cache:            256K
L3 cache:            12288K
NUMA node0 CPU[(]s[)]:   0-15
""".splitlines()

cat_scaling_gov_cmd = "cat /sys/devices/system/cpu/cpufreq/policy*/scaling_governor"
power_cmd = "echo {} > /sys/devices/system/cpu/cpufreq/policy{}/scaling_governor"

disable_power_cmds = []
enable_power_cmds = []
for i in range(16):
    disable_power_cmds.append(power_cmd.format("performance", i))
    enable_power_cmds.append(power_cmd.format("powersave", i))

power_saving_dict = {
    "powersave": enable_power_cmds,
    "performance": disable_power_cmds,
    }
#TC 13 and 11
sysinfo_onie="2020.08.0.0.2"
sonic_ver_old="SONiC Software Version: SONiC.202106-brixia.pb19"
sonic_ver_new="SONiC Software Version: SONiC.202106-brixia.pb20"

# .................... TC_09_SONiC_install_by_pxeboot_test ....................

pxeboot_cpuinfo_pattern = [
    "processor.*: ([0-9]|1[0-5])",
    "vendor_id.*: GenuineIntel",
    "cpu family.*",
    "model.*",
    "model name.*: Intel[(]R[)] Xeon[(]R[)] CPU D-1649N @ 2.30GHz",
    "stepping .*",
    "microcode.*",
    "cpu MHz  .*",
    "cache size.*",
    "physical id.*",
    "siblings.*",
    "core id.*",
    "cpu cores.*",
    "apicid.*",
    "initial apicid.*",
    "fpu.*",
    "fpu_exception.*",
    "cpuid level.*",
    "wp.*",
    "flags.*",
    "bugs.*",
    "bogomips.*",
    "clflush size.*",
    "cache_alignment.*",
    "address sizes.*",
    "power management.*"
]

pxeboot_meminfo_pattern = [
"MemTotal:.*",
"MemFree:.*",
"MemAvailable:.*",
"Buffers:.*",
"Cached:.*",
"SwapCached:.*",
"Active:.*",
"Inactive:.*",
"Active[(]anon[)]: .*",
"Inactive[(]anon[)]: .*",
"Active[(]file[)]: .*",
"Inactive[(]file[)]: .*",
"Unevictable:.*",
"Mlocked:.*",
"SwapTotal:.*",
"SwapFree:.*",
"Dirty:.*",
"Writeback:.*",
"AnonPages:.*",
"Mapped:.*",
"Shmem:.*",
"Slab:.*",
"SReclaimable:.*",
"SUnreclaim:.*",
"KernelStack:.*",
"PageTables:.*",
"NFS_Unstable:.*",
"Bounce:.*",
"WritebackTmp:.*",
"CommitLimit:.*",
"Committed_AS:.*",
"VmallocTotal:.*",
"VmallocUsed:.*",
"VmallocChunk:.*",
"Percpu:.*",
"HardwareCorrupted:.*",
"AnonHugePages:.*",
"ShmemHugePages:.*",
"ShmemPmdMapped:.*",
"HugePages_Total:.*",
"HugePages_Free:.*",
"HugePages_Rsvd:.*",
"HugePages_Surp:.*",
"Hugepagesize:.*",
"Hugetlb:.*",
"DirectMap4k:.*",
"DirectMap2M:.*",
"DirectMap1G:.*"
]

pxeboot_ifconfig_pattern = [
    "docker0: flags=.* mtu .*",
    "eth0: flags=.*  mtu .*",
    "lo: flags=.* mtu .*"
]

pxeboot_fdisk_pattern = [
    "Disk /dev/sda:.*",
    "Disk model:.*",
    "Units:.*",
    "Sector size [(]logical/physical[)]:.*",
    "I/O size [(]minimum/optimal[)]:.*",
    "Disklabel type:.*",
    "Disk identifier:.*",
    "Device.*Start.*End.*Sectors.*Size.*Type"
]


pxe_install_i2cdetect_ptn = [
    "i2c-3   smbus           i2c-0-mux [(]chan_id 1[)]                   SMBus adapter",
    "i2c-10102       i2c             i2c-10100-mux [(]chan_id 1[)]               I2C adapter",
    "i2c-10130       i2c             i2c-10100-mux [(]chan_id 29[)]              I2C adapter",
    "i2c-20  i2c             i2c-11-mux [(]chan_id 0[)]                  I2C adapter",
    "i2c-10120       i2c             i2c-10100-mux [(]chan_id 19[)]              I2C adapter",
    "i2c-10  i2c             i2c-ocores                              I2C adapter",
    "i2c-10110       i2c             i2c-10100-mux [(]chan_id 9[)]               I2C adapter",
    "i2c-1   i2c             i2c-ocores                              I2C adapter",
    "i2c-10100       i2c             GFPGA adapter                           I2C adapter",
    "i2c-29  smbus           iMC socket 0 for channel pair 2-3       SMBus adapter",
    "i2c-10129       i2c             i2c-10100-mux [(]chan_id 28[)]              I2C adapter",
    "i2c-19  i2c             i2c-10-mux [(]chan_id 7[)]                  I2C adapter",
    "i2c-10119       i2c             i2c-10100-mux [(]chan_id 18[)]              I2C adapter",
    "i2c-10109       i2c             i2c-10100-mux [(]chan_id 8[)]               I2C adapter",
    "i2c-27  i2c             i2c-11-mux [(]chan_id 7[)]                  I2C adapter",
    "i2c-10127       i2c             i2c-10100-mux [(]chan_id 26[)]              I2C adapter",
    "i2c-10004       i2c             i2c-10000-mux [(]chan_id 3[)]               I2C adapter",
    "i2c-17  i2c             i2c-10-mux [(]chan_id 5[)]                  I2C adapter",
    "i2c-10117       i2c             i2c-10100-mux [(]chan_id 16[)]              I2C adapter",
    "i2c-8   smbus           i2c-0-mux [(]chan_id 6[)]                   SMBus adapter",
    "i2c-10107       i2c             i2c-10100-mux [(]chan_id 6[)]               I2C adapter",
    "i2c-25  i2c             i2c-11-mux [(]chan_id 5[)]                  I2C adapter",
    "i2c-10125       i2c             i2c-10100-mux [(]chan_id 24[)]              I2C adapter",
    "i2c-10002       i2c             i2c-10000-mux [(]chan_id 1[)]               I2C adapter",
    "i2c-15  i2c             i2c-10-mux [(]chan_id 3[)]                  I2C adapter",
    "i2c-10115       i2c             i2c-10100-mux [(]chan_id 14[)]              I2C adapter",
    "i2c-6   smbus           i2c-0-mux [(]chan_id 4[)]                   SMBus adapter",
    "i2c-10105       i2c             i2c-10100-mux [(]chan_id 4[)]               I2C adapter",
    "i2c-10133       i2c             i2c-10100-mux [(]chan_id 32[)]              I2C adapter",
    "i2c-23  i2c             i2c-11-mux [(]chan_id 3[)]                  I2C adapter",
    "i2c-10123       i2c             i2c-10100-mux [(]chan_id 22[)]              I2C adapter",
    "i2c-10000       i2c             GFPGA adapter                           I2C adapter",
    "i2c-13  i2c             i2c-10-mux [(]chan_id 1[)]                  I2C adapter",
    "i2c-10113       i2c             i2c-10100-mux [(]chan_id 12[)]              I2C adapter",
    "i2c-4   smbus           i2c-0-mux [(]chan_id 2[)]                   SMBus adapter",
    "i2c-10103       i2c             i2c-10100-mux [(]chan_id 2[)]               I2C adapter",
    "i2c-10131       i2c             i2c-10100-mux [(]chan_id 30[)]              I2C adapter",
    "i2c-21  i2c             i2c-11-mux [(]chan_id 1[)]                  I2C adapter",
    "i2c-10121       i2c             i2c-10100-mux [(]chan_id 20[)]              I2C adapter",
    "i2c-11  i2c             i2c-ocores                              I2C adapter",
    "i2c-10111       i2c             i2c-10100-mux [(]chan_id 10[)]              I2C adapter",
    "i2c-2   smbus           i2c-0-mux [(]chan_id 0[)]                   SMBus adapter",
    "i2c-10101       i2c             i2c-10100-mux [(]chan_id 0[)]               I2C adapter",
    "i2c-0   smbus           SMBus I801 adapter at f000              SMBus adapter",
    "i2c-28  smbus           iMC socket 0 for channel pair 0-1       SMBus adapter",
    "i2c-10128       i2c             i2c-10100-mux [(]chan_id 27[)]              I2C adapter",
    "i2c-18  i2c             i2c-10-mux [(]chan_id 6[)]                  I2C adapter",
    "i2c-10118       i2c             i2c-10100-mux [(]chan_id 17[)]              I2C adapter",
    "i2c-9   smbus           i2c-0-mux [(]chan_id 7[)]                   SMBus adapter",
    "i2c-10108       i2c             i2c-10100-mux [(]chan_id 7[)]               I2C adapter",
    "i2c-26  i2c             i2c-11-mux [(]chan_id 6[)]                  I2C adapter",
    "i2c-10126       i2c             i2c-10100-mux [(]chan_id 25[)]              I2C adapter",
    "i2c-10003       i2c             i2c-10000-mux [(]chan_id 2[)]               I2C adapter",
    "i2c-16  i2c             i2c-10-mux [(]chan_id 4[)]                  I2C adapter",
    "i2c-10116       i2c             i2c-10100-mux [(]chan_id 15[)]              I2C adapter",
    "i2c-7   smbus           i2c-0-mux [(]chan_id 5[)]                   SMBus adapter",
    "i2c-10106       i2c             i2c-10100-mux [(]chan_id 5[)]               I2C adapter",
    "i2c-10134       i2c             i2c-10100-mux [(]chan_id 33[)]              I2C adapter",
    "i2c-24  i2c             i2c-11-mux [(]chan_id 4[)]                  I2C adapter",
    "i2c-10124       i2c             i2c-10100-mux [(]chan_id 23[)]              I2C adapter",
    "i2c-10001       i2c             i2c-10000-mux [(]chan_id 0[)]               I2C adapter",
    "i2c-14  i2c             i2c-10-mux [(]chan_id 2[)]                  I2C adapter",
    "i2c-10114       i2c             i2c-10100-mux [(]chan_id 13[)]              I2C adapter",
    "i2c-5   smbus           i2c-0-mux [(]chan_id 3[)]                   SMBus adapter",
    "i2c-10104       i2c             i2c-10100-mux [(]chan_id 3[)]               I2C adapter",
    "i2c-10132       i2c             i2c-10100-mux [(]chan_id 31[)]              I2C adapter",
    "i2c-22  i2c             i2c-11-mux [(]chan_id 2[)]                  I2C adapter",
    "i2c-10122       i2c             i2c-10100-mux [(]chan_id 21[)]              I2C adapter",
    "i2c-12  i2c             i2c-10-mux [(]chan_id 0[)]                  I2C adapter",
    "i2c-10112       i2c             i2c-10100-mux [(]chan_id 11[)]              I2C adapter",
]
#TC_03
bios_ver = "Version: Captaine-LinuxBoot.0.01.18"

# TC_42 CPU Stress Test
stress_cmd1 = "./stress --cpu 8 --io 1 &"
stress_cmd2 = "./stress --cpu 8 --vm 4 --vm-bytes 1024 --vm-hang 1 &"
fetch_cmd = "curl -O http://192.168.0.1/stress"

# TC_12_SONiC_uninstall_test

sonic_old_ptn = "SONiC-OS-202106-brixia.pb19"
sonic_new_ptn = "SONiC-OS-202106-brixia.pb20"
sonic_old_image = "onie-installer-x86_64.bin"
fetch_old_sonic = "curl -O http://192.168.0.1/" + sonic_old_image

#TC13
fdisk_onie=['Disk /dev/sda.*GB',
        '/dev/sda1.*']
ifconfig_onie=['eth0.*','UP.*BROADCAST.*MULTICAST.*MTU:1500',
          'eth1.*','UP.*BROADCAST.*MULTICAST.*MTU:1500',
          'lo.*','UP.*LOOPBACK RUNNING.*MTU:65536']

#TC23
Cpu_info_check='''
System Info:
        CPU Brand String     : Intel(R) Xeon(R) CPU D-1649N @ 2.30GHz
        No. of Physical Cores: 8        No. of Logical Cores: 16
        HyperThreading       : Enabled  Turbo Boost: Enabled
'''.splitlines()

