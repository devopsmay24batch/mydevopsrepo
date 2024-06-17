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
##### Variable file used for bmc.robot #####
workspace = '/mnt/data1/'
CENTOS_MODE = 'centos'
Tyr_BMC_Product_ID = '988'
Tyr_BMC_lan_print_1_mac_address = '20:17:01:01:01:01'
Tyr_BMC_lan_print_8_mac_address = '20:17:00:00:01:01'
Tyr_BMC_version = '2.19'
Tyr_BMC_Manufacturer_ID = '12290'
Tyr_CPLD_version = '10 05'
Tyr_eth_mac_addr = '68:91:d0:63:9c:21'
Tyr_BMC_UUID = '29964E27-0101-03E7-0010-DEBF207B346C'
error_messages_list = 'error,fault,fail,warning,critical'
Tyr_pci_device_number = '152'
Tyr_BIOS_version = 'TSE.2.08.0110'
CPU_model_name = 'Intel(R) Xeon(R) Gold 6148 CPU @ 2.40GHz'
memory_size = '96G'
athena_bios_password = 'c411ie'
date_and_time = {
        'Month' : '01',
        'Day'   : '01',
        'Year'  : '2000',
        'Hour'  : '00',
        'Minute': '00',
        'Second': '00'
        }
BIOS_Version="ATHG2.2.02.01"
processor_name_version="Intel.*R.*Xeon.*R.*Gold"
mem_size="Size: 64 GB"
mem_speed="Speed: 3200 MT/s"
cfg_speed="Configured Memory Speed: 2933 MT/s"
Manufacturer="Manufacturer: Micron"
Athena_bios_mac_address="36:ed:26:aa:1a:72"
Athena_bios_ip_address="10.204.125.58"
device_numbers="345"
release_date="09/10/2021"
Athena_bios_mac_address_ESMA="36:ed:26:ab:aa:62"
device_numbers_ESMA="395"
Athena_bios_ip_address_ESMA="10.204.125.57"
processor_name_version_ESMA="Genuine Intel.*R.*"
expected_UUID_ipmitool_mc_guide="System GUID  : 00000000-0000-0000-0000-000000000000" 
expected_UUID_ipmitool_raw_6="00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00"
expected_UUID_dmidecode="Not Settable"
#User needs to analyse memory topology and update the value here
memory_topology_A="""Socket0.ChA.Dimm0: 2933MT/s Micron DRx4 64GB RDIMM
Socket1.ChA.Dimm0: 2933MT/s Micron DRx4 64GB RDIMM"""
memory_topology_B="""Socket0.ChB.Dimm0: 2933MT/s Micron DRx4 64GB RDIMM
Socket1.ChB.Dimm0: 2933MT/s Micron DRx4 64GB RDIMM"""
bios_update_cmd="/p /b /n /x"
bios_me_update_cmd="/p /b /n /x /me"
ME_FW_version='0F:4.4.3.257'
ME_Version_OS='04 43 25 70'
ME_FW_version_new='0F:4.4.4.58'
ME_Version_OS_new='04 44 05 80'
MAXINDEX= '1'
md5_checksum_v1='49e858932c85d67c13515c1d5765cbdb'
md5_checksum_v2='de9cc6fe42cff9825c13bee1584e0568'
md5_checksum_v3='d322028b2059f0ded07b75308e7bb2c9'
md5_checksum_NV='e669a2adb18a478624c2a02885d19851'
nvme_cmd = "nvme list"
nvme_device_count=3
reset_cmd="reset -w"
BMC_Firmware_version="2.17"
error_messages_sell_list = 'error,fault,fail,warning'
bios_recovery_cmd="/p /n /x"
