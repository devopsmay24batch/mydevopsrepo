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
#######################################################################################################################
# Script       : BIOS_keywords.robot                                                                                  #
# Date         : July 29, 2020                                                                                        #
# Author       : James Shi <jameshi@celestica.com>                                                                    #
# Description  : This script used as keywords in bios.robot                                                           #
#                                                                                                                     #
# Script Revision Details:                                                                                            #
#   Initial Draft for BIOS testing                                                                                    #
#######################################################################################################################

*** Settings ***
Variables         BIOS_variable.py

Library           whitebox_lib.py
Library           openbmc_lib.py
#Library           common_lib.py
Library           bios_menu_lib.py
Library           CommonLib.py
Library           OperatingSystem
Library           ../WhiteboxLibAdapter.py
Library           ../ses/ses_lib.py
Library           ../bmc/bmc_lib.py
Library           bios_lib.py

Resource          BIOS_keywords.robot
Resource          CommonResource.robot
Resource          BMC_keywords.robot

*** Keywords ***
prepare BIOS images
    ${server_ipv4_ip} =  get_ip_address_from_config  PC
    Step  1  mkdir data path  DUT  ${workspace}/BIOS
    Step  2  download images  DUT  BIOS
    Step  3  change dir  DUT  ${workspace}/BIOS  mode=CENTOS_MODE
    Step  4  copy files from PC to OS  DUT  ${server_ipv4_ip}  filepath=/FW/bios  filename=CFUFLASH_4.93
              ...   destination_path=${workspace}/BIOS  size_MB=10
    Step  5  chmod file  DUT  filename=CFUFLASH_4.93

clean all
    Step  1  delete folder  DUT  ${workspace}/BIOS

upgrade bios and dc cycle to check version
    ${bmc_ipv4_ip} =  get_ip_address_from_ipmitool  DUT  eth_type=dedicated
    Step  1  update whitebox bios  DUT  cmd=./CFUFLASH_4.93 -cd -d 2  device_type=BIOS
              ...   ipAddress=${bmc_ipv4_ip}  reboot_method=dc_cycle  isUpgrade=True

downgrade bios and dc cycle to check version
    ${bmc_ipv4_ip} =  get_ip_address_from_ipmitool  DUT  eth_type=dedicated
    Step  1  change dir  DUT  ${workspace}/BIOS  mode=CENTOS_MODE
    Step  2  update whitebox bios  DUT  cmd=./CFUFLASH_4.93 -cd -d 2  device_type=BIOS
              ...   ipAddress=${bmc_ipv4_ip}  reboot_method=dc_cycle  isUpgrade=False

upgrade bios and reboot to check version
    ${bmc_ipv4_ip} =  get_ip_address_from_ipmitool  DUT  eth_type=dedicated
    Step  1  change dir  DUT  ${workspace}/BIOS  mode=CENTOS_MODE
    Step  2  update whitebox bios  DUT  cmd=./CFUFLASH_4.93 -cd -d 2  device_type=BIOS
              ...   ipAddress=${bmc_ipv4_ip}  reboot_method=reboot  isUpgrade=True

downgrade bios and reboot to check version
    ${bmc_ipv4_ip} =  get_ip_address_from_ipmitool  DUT  eth_type=dedicated
    Step  1  change dir  DUT  ${workspace}/BIOS  mode=CENTOS_MODE
    Step  2  update whitebox bios  DUT  cmd=./CFUFLASH_4.93 -cd -d 2  device_type=BIOS
              ...   ipAddress=${bmc_ipv4_ip}  reboot_method=reboot  isUpgrade=False

reboot os to check bios function
    Step  1  DUT  reboot os
    Step  2  set time delay  300

common FW check list
    Step  1  verify_BMC_product_id  DUT  ${Tyr_BMC_Product_ID}
    Step  2  verify_bmc_mac_address  DUT  cmd=ipmitool lan print 1  expected_result=${Tyr_BMC_lan_print_1_mac_address}
    Step  3  verify_bmc_mac_address  DUT  cmd=ipmitool lan print 8  expected_result=${Tyr_BMC_lan_print_8_mac_address}
    Step  4  verify_BMC_voltage_sensor  DUT
    Step  5  verify_BMC_version  DUT  ${Tyr_BMC_version}
    Step  6  verify_BMC_tmp_sensor  DUT
    Step  7  verify_BMC_Manufacturer_ID  DUT  ${Tyr_BMC_Manufacturer_ID}
    Step  8  CPLD version check
    Step  9  check_mac_address  DUT  interface=enp179s0f1  expected_result=${Tyr_eth_mac_addr}
    Step  10  verify_BMC_UUID  DUT  expected_result=${Tyr_BMC_UUID}
    Step  11  verify_pci_device_number  DUT  expected_result=${Tyr_pci_device_number}
    Step  12  verify_cmd_output_message  DUT  ipmitool sel list  ${error_messages_list}
    Step  14  verify_processor_model_name  DUT  ${CPU_model_name}
    Step  15  verify_memory_size  DUT  ${memory_size}

CPLD version check
    Step  1  run ipmi get cmd  DUT  ipmitool raw 0x3a 0x4  ${Tyr_CPLD_version}

Idle overnight
    Step  1  set time delay  43200


Check version in BIOS
    ${bios_version} =  execute_Linux_command    dmidecode -s bios-version
    verify_bios_version_in_bios   DUT   ${athena_bios_password}   ${bios_version}

Change System date and time in BIOS
    OS Connect Device
    change_date_time_in_bios   DUT   ${athena_bios_password}  ${date_and_time}
    OS Disconnect Device
    Sleep  90


Check date and time is sync with BIOS
    OS Connect Device
    execute_Linux_command    hwclock --hctosys 
    ${os_date_output} =  execute_Linux_command    timedatectl
    verify_time_in_OS  ${os_date_output}   ${date_and_time}
    OS Disconnect Device

Change System date and time in OS
    OS Connect Device
    ${os_dt} =  change_date_time_in_os   DUT
    Set Suite Variable  ${os_dt} 
    execute_Linux_command    hwclock --systohc 
    OS Disconnect Device

Verify date and time is sync with OS
    OS Connect Device
    verify_time_in_BIOS  DUT   ${athena_bios_password}   ${os_dt}
    OS Disconnect Device

prepare Athena_G2 BIOS images to upgrade 
   OS Connect Device 
   ${server_ipv4_ip} =  get_ip_address_from_config  PC
   ${user_id} =   get_username_from_config   PC
   ${password} =  get_password_from_config   PC
   mkdir data path  DUT  /root/athena_gen2_fw/BIOS
   change_directory   DUT  /root/athena_gen2_fw/BIOS 
   download images  DUT   Athena_FW_BIOS_A
   copy files from PC to OS  DUT  ${user_id}   ${password}   ${server_ipv4_ip}  CFUFLASH   /root/Athena-G2-FW/BIOS  /root/athena_gen2_fw/BIOS   50 
   chmod file  DUT  filename=CFUFLASH
   copy files from PC to OS  DUT  ${user_id}   ${password}   ${server_ipv4_ip}  ipmi_driver.sh  /root/Athena-G2-FW/BIOS  /root/athena_gen2_fw/BIOS   50
   chmod file  DUT  filename=ipmi_driver.sh
   OS Disconnect Device
   ConnectESMB
   ${server_ipv4_ip} =  get_ip_address_from_config  PC1
   ${user_id} =   get_username_from_config   PC1
   ${password} =  get_password_from_config   PC1
   mkdir data path  DUT  /root/athena_gen2_fw/BIOS
   change_directory   DUT  /root/athena_gen2_fw/BIOS
   download images  DUT  Athena_FW_BIOS_B 
   copy files from PC to OS  DUT  ${user_id}   ${password}   ${server_ipv4_ip}  CFUFLASH   /root/Athena-G2-FW/BIOS  /root/athena_gen2_fw/BIOS   50
   chmod file  DUT  filename=CFUFLASH
   copy files from PC to OS  DUT  ${user_id}   ${password}   ${server_ipv4_ip}  ipmi_driver.sh  /root/Athena-G2-FW/BIOS  /root/athena_gen2_fw/BIOS   50
   chmod file  DUT  filename=ipmi_driver.sh
   OS Disconnect Device

remove Athena_G2 BIOS images
   OS Connect Device
   delete folder  DUT   /root/athena_gen2_fw/BIOS
   OS Disconnect Device
   ConnectESMB
   delete folder  DUT   /root/athena_gen2_fw/BIOS
   OS Disconnect Device

upgrade bios using CFUFLASH
  OS Connect Device
  Step  1  change_directory   DUT  /root/athena_gen2_fw/BIOS
  ${update} =   upgrade bios image using CFUFLASH    DUT   ./CFUFLASH -cd -d 2   device_type=BIOS  isUpgrade=True  module=Athena_FW_BIOS_A
  Step  2  Run Keyword If  '${update}'== '${1}'
                    ...  Run Keywords
                    ...  OS Disconnect Device  AND
                    ...  whitebox_lib.Powercycle Pdu1  DUT  AND
                    ...  set time delay   300  AND
                    ...  whitebox_lib.Powercycle Pdu1  DUT  AND
                    ...  set time delay   360  AND
                    ...  OS Connect Device  AND
                    ...  common BIOS FW check list in ESM A
  OS Disconnect Device
  ConnectESMB
  Step  3  change_directory   DUT  /root/athena_gen2_fw/BIOS
  ${update} =   upgrade bios image using CFUFLASH    DUT   ./CFUFLASH -cd -d 2   device_type=BIOS  isUpgrade=True  module=Athena_FW_BIOS_B
  Step  4  Run Keyword If  '${update}'== '${1}'
                    ...  Run Keywords
                    ...  OS Disconnect Device  AND
                    ...  whitebox_lib.Powercycle Pdu1  DUT  AND
                    ...  set time delay   300  AND
                    ...  whitebox_lib.Powercycle Pdu1  DUT  AND
                    ...  set time delay   300  AND
                    ...  ConnectESMB  AND
                    ...  common BIOS FW check list in ESM B
  OS Disconnect Device

common BIOS FW check list in ESM A
   Step  1  verify_bios_version_athena   DUT  module=Athena_FW_BIOS_A
   Step  2  verify_bios_memory  DUT  ${mem_size}  ${mem_speed}  ${cfg_speed}  ${Manufacturer}
   Step  3  verify_bmc_mac_address  DUT  cmd=ipmitool lan print 1  expected_result=${Athena_bios_mac_address_ESMA}
   Step  4  verify_device_numbers  DUT   expected_result=${device_numbers_ESMA}
   Step  5  verify_release_date   DUT   expected_result=${release_date}
   Step  6  verify_bios_ip_address  DUT  cmd=ipmitool lan print 1  expected_result=${Athena_bios_ip_address_ESMA}
   Step  7  verify_bios_processor_version  DUT   ${processor_name_version_ESMA}


common BIOS FW check list in ESM B
   Step  1  verify_bios_version_athena   DUT  module=Athena_FW_BIOS_B
   Step  2  verify_bios_memory  DUT  ${mem_size}  ${mem_speed}  ${cfg_speed}  ${Manufacturer}
   Step  3  verify_bmc_mac_address  DUT  cmd=ipmitool lan print 1  expected_result=${Athena_bios_mac_address}
   Step  4  verify_device_numbers  DUT   expected_result=${device_numbers}
   Step  5  verify_release_date   DUT   expected_result=${release_date}
   Step  6  verify_bios_ip_address  DUT  cmd=ipmitool lan print 1  expected_result=${Athena_bios_ip_address}
   Step  7  verify_bios_processor_version  DUT   ${processor_name_version}

UUID_Check
   OS Connect Device
   verify UUID   DUT   ${expected_UUID_ipmitool_mc_guide}   ${expected_UUID_ipmitool_raw_6}    ${expected_UUID_dmidecode}
   OS Disconnect Device
   ConnectESMB
   verify UUID   DUT   ${expected_UUID_ipmitool_mc_guide}   ${expected_UUID_ipmitool_raw_6}    ${expected_UUID_dmidecode}
   OS Disconnect Device

prepare Athena_G2 BIOS images to upgrade using afuflash
   OS Connect Device
   ${server_ipv4_ip} =  get_ip_address_from_config  PC
   ${user_id} =   get_username_from_config   PC
   ${password} =  get_password_from_config   PC
   mkdir data path  DUT  /root/athena_gen2_fw/BIOS
   change_directory   DUT  /root/athena_gen2_fw/BIOS
   download images  DUT   Athena_FW_BIOS_A
   copy files from PC to OS  DUT  ${user_id}   ${password}   ${server_ipv4_ip}  afulnx_64   /root/Athena-G2-FW/BIOS  /root/athena_gen2_fw/BIOS   50
   chmod file  DUT  filename=afulnx_64
   copy files from PC to OS  DUT  ${user_id}   ${password}   ${server_ipv4_ip}  ipmi_driver.sh  /root/Athena-G2-FW/BIOS  /root/athena_gen2_fw/BIOS   50
   chmod file  DUT  filename=ipmi_driver.sh
   OS Disconnect Device
   ConnectESMB
   ${server_ipv4_ip} =  get_ip_address_from_config  PC1
   ${user_id} =   get_username_from_config   PC1
   ${password} =  get_password_from_config   PC1
   mkdir data path  DUT  /root/athena_gen2_fw/BIOS
   change_directory   DUT  /root/athena_gen2_fw/BIOS
   download images  DUT  Athena_FW_BIOS_B
   copy files from PC to OS  DUT  ${user_id}   ${password}   ${server_ipv4_ip}  afulnx_64   /root/Athena-G2-FW/BIOS  /root/athena_gen2_fw/BIOS   50
   chmod file  DUT  filename=afulnx_64
   copy files from PC to OS  DUT  ${user_id}   ${password}   ${server_ipv4_ip}  ipmi_driver.sh  /root/Athena-G2-FW/BIOS  /root/athena_gen2_fw/BIOS   50
   chmod file  DUT  filename=ipmi_driver.sh
   OS Disconnect Device

upgrade bios using AFUFLASH
  [Arguments]   ${update_cmd}
  OS Connect Device
  Step  1  change_directory   DUT  /root/athena_gen2_fw/BIOS
  ${update} =   upgrade bios image using AFUFLASH    DUT   ${update_cmd}   ./afulnx_64   device_type=BIOS  isUpgrade=True  module=Athena_FW_BIOS_A
  Step  2  Run Keyword If  '${update}'== '${1}'
                    ...  Run Keywords
                    ...  OS Disconnect Device  AND
                    ...  whitebox_lib.Powercycle Pdu1  DUT  AND
                    ...  set time delay   300  AND
                    ...  whitebox_lib.Powercycle Pdu1  DUT  AND
                    ...  set time delay   360  AND
                    ...  OS Connect Device  AND
                    ...  common BIOS FW check list in ESM A
  OS Disconnect Device
  ConnectESMB
  Step  3  change_directory   DUT  /root/athena_gen2_fw/BIOS
  ${update} =   upgrade bios image using AFUFLASH    DUT    ${update_cmd}   ./afulnx_64   device_type=BIOS  isUpgrade=True  module=Athena_FW_BIOS_B
  Step  4  Run Keyword If  '${update}'== '${1}'
                    ...  Run Keywords
                    ...  OS Disconnect Device  AND
                    ...  whitebox_lib.Powercycle Pdu1  DUT  AND
                    ...  set time delay   300  AND
                    ...  whitebox_lib.Powercycle Pdu1  DUT  AND
                    ...  set time delay   300  AND
                    ...  ConnectESMB  AND
                    ...  common BIOS FW check list in ESM B
  OS Disconnect Device

Processor MicroCode Check
   OS Connect Device
   ${microcode_cmd_ouput}=   get_cpu_microcode  DUT
   ${microcode_rev_cmd}=  Convert To Hex   ${microcode_cmd_ouput}  base=16
   ${microcode_bios_output}=   get_cpu_microcode_revision_from_bios  DUT
   ${microcode_rev_bios}=  Convert To Hex  ${microcode_bios_output}   base=16
   Should Be Equal  ${microcode_rev_cmd}   ${microcode_rev_bios}
   OS Disconnect Device

Verify BIOS Version with UEFI Shell
   OS Connect Device
   ${bios_version} =  execute_Linux_command    dmidecode -s bios-version
   enter_uefi_shell  DUT    bios_password=${athena_bios_password}
   verify_bios_version_in_uefi_shell  DUT    ${bios_version}
   exit_uefi_shell    DUT
   OS Disconnect Device
   Sleep  90

   OS Connect Device
   revert_boot_order    DUT    bios_password=${athena_bios_password}
   OS Disconnect Device

Verify SEL log clear in BIOS
   OS Connect Device
   clear_SEL_log_in_BIOS    DUT   bios_password=${athena_bios_password}
   OS Disconnect Device
   Sleep  90

   OS Connect Device
   verify_in_BIOS_if_SEL_logs_are_cleared    DUT   bios_password=${athena_bios_password}
   OS Disconnect Device

BIOS memory topology check
  OS Connect Device
  BIOS Memory Topology validation   DUT  ${memory_topology_A}
  OS Disconnect Device
  ConnectESMB
  BIOS Memory Topology validation   DUT  ${memory_topology_B}
  OS Disconnect Device

Download Athena BIOS image
   OS Connect Device
   downloadAthenaSesFwImage    DUT   Athena_FW_BIOS
   OS Disconnect Device

Upgrade BIOS using CFUFLASH Tool
   OS Connect Device
   upgrade_bios_FW_with_save_config    DUT   Athena_FW_BIOS
   ses_lib.powercycle_pdu1  DUT
   OS Disconnect Device
   Sleep  300

Do some config in BIOS
   OS Connect Device
   change_some_settings_in_BIOS     DUT   bios_password=${athena_bios_password}
   ses_lib.powercycle_pdu1  DUT
   OS Disconnect Device
   Sleep  300

Verify config saved in BIOS
   OS Connect Device
   verify_settings_saved_in_BIOS     DUT   Athena_FW_BIOS   bios_password=${athena_bios_password}
   ses_lib.powercycle_pdu1  DUT
   OS Disconnect Device
   Sleep  300

Remove Athena FW image
    OS Connect Device
    RemoveAthenaBIOSFwImage    DUT   Athena_FW_BIOS
    OS Disconnect Device

Prepare images of multiple versions
   OS Connect Device
   ${server_ipv4_ip} =  get_ip_address_from_config  PC
   ${user_id} =   get_username_from_config   PC
   ${password} =  get_password_from_config   PC
   mkdir data path  DUT  /root/athena_gen2_fw/BIOS
   change_directory   DUT  /root/athena_gen2_fw/BIOS
   copy files from PC to OS  DUT  ${user_id}   ${password}   ${server_ipv4_ip}  CFUFLASH   /root/Athena-G2-FW/BIOS  /root/athena_gen2_fw/BIOS   50
   chmod file  DUT  filename=CFUFLASH
   copy files from PC to OS  DUT  ${user_id}   ${password}   ${server_ipv4_ip}  ipmi_driver.sh  /root/Athena-G2-FW/BIOS  /root/athena_gen2_fw/BIOS   50
   chmod file  DUT  filename=ipmi_driver.sh
   downloadBIOSImages   DUT   Athena_BIOS_Versions_A
   OS Disconnect Device
   ConnectESMB
   ${server_ipv4_ip} =  get_ip_address_from_config  PC1
   ${user_id} =   get_username_from_config   PC1
   ${password} =  get_password_from_config   PC1
   mkdir data path  DUT  /root/athena_gen2_fw/BIOS
   change_directory   DUT  /root/athena_gen2_fw/BIOS
   copy files from PC to OS  DUT  ${user_id}   ${password}   ${server_ipv4_ip}  CFUFLASH   /root/Athena-G2-FW/BIOS  /root/athena_gen2_fw/BIOS   50
   chmod file  DUT  filename=CFUFLASH
   copy files from PC to OS  DUT  ${user_id}   ${password}   ${server_ipv4_ip}  ipmi_driver.sh  /root/Athena-G2-FW/BIOS  /root/athena_gen2_fw/BIOS   50
   chmod file  DUT  filename=ipmi_driver.sh
   downloadBIOSImages   DUT   Athena_BIOS_Versions_B
   OS Disconnect Device


upgrade_downgrade_bios_version
  [Arguments]    ${module}  ${version}  ${key}  ${ME_version_BIOS}   ${ME_ver_OS}
  ${image_to_upgrade_downgrade} =  get_image_version_for_upgrade_downgrade   ${module}  ${version}   ${key}
  ${rev_to_check} =  GetRevFromImage  ${image_to_upgrade_downgrade}
  OS Connect Device
  change_directory   DUT  /root/athena_gen2_fw/BIOS
  update_bios_version   DUT    ./CFUFLASH -cd -d 2      ${image_to_upgrade_downgrade}
  OS Disconnect Device
  ConnectESMB
  change_directory   DUT  /root/athena_gen2_fw/BIOS
  update_bios_version   DUT    ./CFUFLASH -cd -d 2      ${image_to_upgrade_downgrade}
  OS Disconnect Device
  whitebox_lib.Powercycle Pdu1  DUT
  Sleep  300
  whitebox_lib.Powercycle Pdu1  DUT
  Sleep  360
  OS Connect Device
  Sleep  30
  ${version_output} =  execute_Linux_command    dmidecode -s bios-version
  common_check_patern_2     ${version_output}     ${rev_to_check}    BIOS_Version_check  expect=True
  ${ME_output} =     execute_Linux_command     ipmitool -b 0x6 -t 0x2c raw 6 1
  verify_me_version_in_os      ${ME_output}    ${ME_ver_OS}
  verify_bios_memory  DUT  ${mem_size}  ${mem_speed}  ${cfg_speed}  ${Manufacturer}
  verify_bmc_mac_address  DUT  cmd=ipmitool lan print 1  expected_result=${Athena_bios_mac_address_ESMA}
  verify_device_numbers  DUT   expected_result=${device_numbers_ESMA}
  verify_bios_ip_address  DUT  cmd=ipmitool lan print 1  expected_result=${Athena_bios_ip_address_ESMA}
  verify_bios_processor_version  DUT   ${processor_name_version_ESMA}
  Check version in BIOS
  Sleep  60	
  verify_version_in_ME    DUT    ${ME_version_BIOS}
  OS Disconnect Device
  ConnectESMB
  ${version_output} =  execute_Linux_command    dmidecode -s bios-version
  common_check_patern_2     ${version_output}     ${rev_to_check}    BIOS_Version_check  expect=True
  ${ME_output} =     execute_Linux_command     ipmitool -b 0x6 -t 0x2c raw 6 1
  verify_me_version_in_os      ${ME_output}    ${ME_ver_OS}
  verify_bios_memory  DUT  ${mem_size}  ${mem_speed}  ${cfg_speed}  ${Manufacturer}
  verify_bmc_mac_address  DUT  cmd=ipmitool lan print 1  expected_result=${Athena_bios_mac_address}
  verify_device_numbers  DUT   expected_result=${device_numbers}
  verify_bios_ip_address  DUT  cmd=ipmitool lan print 1  expected_result=${Athena_bios_ip_address}
  verify_bios_processor_version  DUT   ${processor_name_version}  
  Check version in BIOS
  Sleep  60
  verify_version_in_ME    DUT    ${ME_version_BIOS}
  OS Disconnect Device

verify md5checksum with release notes
  [Arguments]    ${module}  ${version}  ${key}  ${md5_checksum}
  ${image_to_upgrade_downgrade} =  get_image_version_for_upgrade_downgrade   ${module}  ${version}   ${key}
  ${check_sum_output} =  execute_Linux_command   md5sum ${image_to_upgrade_downgrade}
  common_check_patern_2    ${check_sum_output}     ${md5_checksum}     md5checksum_check  expect=True

NVME information check
  OS Connect Device
  ${output} =  execute_Linux_command  ${nvme_cmd}
  NVME info validation   DUT  ${output}  ${nvme_device_count}
  OS Disconnect Device
  ConnectESMB
  ${output} =  execute_Linux_command  ${nvme_cmd}
  NVME info validation   DUT  ${output}   ${nvme_device_count}
  OS Disconnect Device

UEFI shell mode reset
  OS Connect Device
  UEFI shell reset   DUT   ${reset_cmd}
  Sleep  20
  OS Disconnect Device
  Sleep  60

Record the CPU Frequency with EIST as Enabled
   OS Connect Device
   enable_p_state   DUT   bios_password=${athena_bios_password}
   OS Disconnect Device
   Sleep  200

   OS Connect Device
   FOR    ${INDEX}    IN RANGE  10
       ${output} =  execute_Linux_command   cat /proc/cpuinfo | grep "cpu MHz"
       Log  ${output}
       Sleep  2
   END
   OS Disconnect Device

Record the CPU Frequency with EIST as Disabled
   OS Connect Device
   disable_p_state   DUT   bios_password=${athena_bios_password}
   OS Disconnect Device
   Sleep  200

   OS Connect Device
   FOR    ${INDEX}    IN RANGE  10
       ${output} =  execute_Linux_command   cat /proc/cpuinfo | grep "cpu MHz"
       Log  ${output}
       Sleep  2
   END
   OS Disconnect Device

PCIe_Device_Check_in_BIOS_UEFI_shell
  OS Connect Device
  Check_PCIE_ports_in_BIOS  DUT
  ${pci_op_list} =  get_PCIE_in_UEFI_shell  DUT
  OS Disconnect Device
  Sleep  120
  OS Connect Device
  reboot_os  DUT
  OS Disconnect Device
  Sleep  150
  OS Connect Device
  Check_PCIE_ports_in_BIOS  DUT
  ${pci_op_list_after_reboot} =  get_PCIE_in_UEFI_shell  DUT
  compare pci_op_list    ${pci_op_list}    ${pci_op_list_after_reboot}
  OS Disconnect Device
  Sleep  120
  ses_lib.powercycle_pdu1  DUT
  Sleep  300
  OS Connect Device
  Check_PCIE_ports_in_BIOS  DUT
  ${pci_op_list_after_powercycle} =  get_PCIE_in_UEFI_shell  DUT
  compare pci_op_list    ${pci_op_list}    ${pci_op_list_after_powercycle}
  OS Disconnect Device

Verify default user password in BIOS
  OS Connect Device
  verify_bios_default_password  DUT   bios_password=${athena_bios_password}
  OS Disconnect Device

Clear SEL Logs
    execute_Linux_command    ipmitool sel clear
    Sleep  10

Verify OS Watchdog Timer Functionality
   OS Connect Device
   Clear SEL Logs
   enable_watchdog_timer_in_bios       DUT   bios_password=${athena_bios_password}
   verify system hard reset after count down
   OS Disconnect Device
   Sleep  80

   OS Connect Device
   disable_watchdog_timer_in_bios       DUT   bios_password=${athena_bios_password}
   OS Disconnect Device

Verify BIOS_005_Flash BIOS and ME under UEFI shell
  [Arguments]    ${module}  ${version}  ${key}  ${bios_flash_cmd}
  ${image_to_upgrade_downgrade} =  get_image_version_for_upgrade_downgrade  ${module}  ${version}  ${key}
  Log  ${image_to_upgrade_downgrade}
  ${rev_to_check} =  GetRevFromImage  ${image_to_upgrade_downgrade}
  OS Connect Device
  ${ip}  get_ip_address_from_ipmitool  DUT
  verifyeventlogSELclear  DUT  ${ip}
  ${BMC_MAC_address1a}  get_info_from_lan_print  DUT  MAC Address  True  ${ip}
  ${version_output} =  execute_Linux_command    dmidecode -s bios-version
  ${ME_output1} =     execute_Linux_command     ipmitool -b 0x6 -t 0x2c raw 6 1
  Flash BIOS under UEFI shell mode   DUT   ${image_to_upgrade_downgrade}  ${bios_flash_cmd}
  OS Disconnect Device
  whitebox_lib.Powercycle Pdu1  DUT
  Sleep  300
  whitebox_lib.Powercycle Pdu1  DUT
  Sleep  450
  OS Connect Device
  ${ME_output2} =     execute_Linux_command     ipmitool -b 0x6 -t 0x2c raw 6 1
  verify_me_version_in_os      ${ME_output2}    ${ME_Version_OS}
  OS Disconnect Device
  Verify system after flash update  ${BMC_MAC_address1a}  ${ip}  ${rev_to_check}

Verify BIOS_008_BIOS flash recovery test
  [Arguments]    ${module}  ${version}  ${key}  ${bios_flash_cmd}
  ${image_to_upgrade_downgrade} =  get_image_version_for_upgrade_downgrade  ${module}  ${version}  ${key}
  Log  ${image_to_upgrade_downgrade}
  ${rev_to_check} =  GetRevFromImage  ${image_to_upgrade_downgrade}
  OS Connect Device
  ${ip}  get_ip_address_from_ipmitool  DUT
  verifyeventlogSELclear  DUT  ${ip}
  ${BMC_MAC_address1a}  get_info_from_lan_print  DUT  MAC Address  True  ${ip}
  Flash BIOS under UEFI shell mode   DUT   ${image_to_upgrade_downgrade}  ${bios_flash_cmd}
  OS Disconnect Device
  whitebox_lib.Powercycle Pdu1  DUT
  Sleep  300
  whitebox_lib.Powercycle Pdu1  DUT
  Sleep  450
  Verify system after flash update  ${BMC_MAC_address1a}  ${ip}  ${rev_to_check}

Verify system after flash update
  [Arguments]    ${BMC_MAC_address1a}  ${ip}  ${rev_to_check}
  OS Connect Device
  ${version_output} =  execute_Linux_command    dmidecode -s bios-version
  common_check_patern_2     ${version_output}     ${rev_to_check}    BIOS_Version_check  expect=True
  verify_bios_memory  DUT  ${mem_size}  ${mem_speed}  ${cfg_speed}  ${Manufacturer}
  ${BMC_MAC_address2a}  get_info_from_lan_print  DUT  MAC Address  True  ${ip}
  common_check_patern_2    ${BMC_MAC_address1a}     ${BMC_MAC_address2a}      verify bmc mac address on ESMA  expect=True
  verify_device_numbers  DUT   expected_result=${device_numbers_ESMA}
  verify_bios_ip_address  DUT  cmd=ipmitool lan print 1  expected_result=${ip}
  verify_bios_processor_version  DUT   ${processor_name_version_ESMA}
  verify_cmd_output_message  DUT  ipmitool sel list  ${error_messages_sell_list}
  Check version in BIOS
  Sleep  60
  OS Disconnect Device

verify system hard reset after count down
    verify_hard_reset_after_watchdog_timer_expiry  DUT
    Sleep  5

Flash BIOS under UEFI shell
  [Arguments]    ${module}  ${version}  ${key}  
  ${image_to_upgrade_downgrade} =  get_image_version_for_upgrade_downgrade  ${module}  ${version}  ${key}
  Log  ${image_to_upgrade_downgrade}
  ${rev_to_check} =  GetRevFromImage  ${image_to_upgrade_downgrade}
  Log   ${rev_to_check}
  OS Connect Device
  Flash BIOS under UEFI shell mode   DUT   ${image_to_upgrade_downgrade}   ${bios_update_cmd}
  OS Disconnect Device
  Sleep  60
  whitebox_lib.Powercycle Pdu1  DUT
  Sleep  300
  whitebox_lib.Powercycle Pdu1  DUT
  Sleep  420
  OS Connect Device
  Sleep  60
  ${ip}  get_ip_address_from_ipmitool  DUT
  verifyeventlogSELclear  DUT  ${ip}
  ${BMC_MAC_address1a}  get_info_from_lan_print  DUT  MAC Address  True  ${ip}
  ${version_output} =  execute_Linux_command    dmidecode -s bios-version
  common_check_patern_2     ${version_output}     ${rev_to_check}    BIOS_Version_check  expect=True
  ${BMC_MAC_address2a}  get_info_from_lan_print  DUT  MAC Address  True  ${ip}
  common_check_patern_2    ${BMC_MAC_address1a}     ${BMC_MAC_address2a}      verify bmc mac address on ESMA  expect=True
  verify_bios_memory  DUT  ${mem_size}  ${mem_speed}  ${cfg_speed}  ${Manufacturer}
  verify_device_numbers  DUT   expected_result=${device_numbers_ESMA}
  verify_bios_ip_address  DUT  cmd=ipmitool lan print 1  expected_result=${ip}
  verify_bios_processor_version  DUT   ${processor_name_version_ESMA}
  verify_cmd_output_message  DUT  ipmitool sel list  ${error_messages_sell_list}
  Check version in BIOS
  Sleep  60
  OS Disconnect Device

Linux OS reboot stress
  ${ip}  get_ip_address_from_ipmitool  DUT
  Verify event log SEL clear  DUT  ${ip}
  ${BMC_MAC_address1a}  get_info_from_lan_print  DUT  MAC Address  True  ${ip}
  FOR  ${INDEX}    IN RANGE    ${MAXINDEX}
      Step  1  CommonLib.transmit   reboot
      Step  2  Sleep   200
      Step  3  server Connect
  END
  ${BMC_MAC_address2a}  get_info_from_lan_print  DUT  MAC Address  True  ${ip}
  common_check_patern_2    ${BMC_MAC_address1a}     ${BMC_MAC_address2a}      verify bmc mac address on ESMA  expect=True
  Verify the SEL and ensure no error
  Verify abnormal event log  DUT  ${ip}
  verifythesensorreadingandcheckstatus  DUT  ${ip}

clear logs before idle stress
  [Arguments]    ${ip}
  Verify event log SEL clear  DUT  ${ip}
  CommonLib.execute_command     dmesg -C

check logs after idle stress
  [Arguments]    ${ip}
  Verify the SEL and ensure no error
  Verify abnormal event log  DUT  ${ip}
  verifythesensorreadingandcheckstatus  DUT  ${ip}
  ${output} =  CommonLib.execute_command    dmesg | grep -i Error
  check_pattern_in_output     ${output}  Error   check for error message in dmesg
  ${output} =  CommonLib.execute_command    dmesg | grep -i fail
  check_pattern_in_output   ${output}  Fail    check for Fail message in dmesg
  ${output} =  CommonLib.execute_command    dmesg | grep -i shutdown
  check_pattern_in_output     ${output}  Shutdown   check for Shutdown message in dmesg
  ${output} =  CommonLib.execute_command    dmesg | grep -i reboot
  check_pattern_in_output      ${output}  reboot   check for reboot message in dmesg
  ${output} =  CommonLib.execute_command    dmesg | grep -i start
  check_pattern_in_output     ${output}  start    check for start message in dmesg
 
Boot into BIOS Setup and set configuration
  ConnectESMB
  ${ipb}  get_ip_address_from_ipmitool  DUT
  Verify event log SEL clear  DUT  ${ipb}
  enter_into_bios_setup  DUT   bios_password=${athena_bios_password}
  set_configuration1_BIOS_setup  DUT
  OS Disconnect Device
  whitebox_lib.Powercycle Pdu1  DUT
  Sleep  300
  ConnectESMB
  enter_into_bios_setup  DUT   bios_password=${athena_bios_password}
  BIOS_BasicTest1_under_UEFI_shell_mode  DUT
  OS Disconnect Device
  Sleep  300
  ConnectESMB
  ${ipb}  get_ip_address_from_ipmitool  DUT
  Verify system logs after BIOS test  ${ipb}
  OS Disconnect Device
  ConnectESMB
  enter_into_bios_setup  DUT   bios_password=${athena_bios_password}
  set_configuration2_BIOS_setup  DUT
  OS Disconnect Device
  Sleep  300
  ConnectESMB
  enter_into_bios_setup  DUT   bios_password=${athena_bios_password}
  BIOS_BasicTest2_under_UEFI_shell_mode  DUT
  OS Disconnect Device
  Sleep  300
  ConnectESMB
  ${ipb}  get_ip_address_from_ipmitool  DUT
  Verify system logs after BIOS test  ${ipb}
  OS Disconnect Device

Verify system logs after BIOS test
  [Arguments]    ${ip}
  Verify the SEL and ensure no error
  Verify abnormal event log  DUT  ${ip}
  verifythesensorreadingandcheckstatus  DUT  ${ip}

Check Intel Optane DC Persistent Memory Configuration DIMMs
  ConnectESMB
  ${ipb}  get_ip_address_from_ipmitool  DUT
  Verify event log SEL clear  DUT  ${ipb}
  enter_into_bios_setup  DUT   bios_password=${athena_bios_password}
  Check DIMMs GoldConfig information  DUT
  OS Disconnect Device
  Sleep  90
  ConnectESMB
  Verify system logs after BIOS test  ${ipb}
  OS Disconnect Device

Check Two Regions are created and each region info shows right
  ConnectESMB
  ${ipb}  get_ip_address_from_ipmitool  DUT
  Verify event log SEL clear  DUT  ${ipb}
  enter_into_bios_setup  DUT   bios_password=${athena_bios_password}
  Check Two Regions Created with Information  DUT
  OS Disconnect Device
  Sleep  90
  ConnectESMB
  Verify system logs after BIOS test  ${ipb}
  OS Disconnect Device

Check namespace and App Direct Capacity
  ConnectESMB
  enter_into_bios_setup  DUT   bios_password=${athena_bios_password}
  Check Namespace AppDirect Capacity Information  DUT
  OS Disconnect Device
  Sleep  90

Check namespace and App Direct Capacity after power cycle
  FOR    ${INDEX}    IN RANGE    1    3
      Print Loop Info  ${INDEX}
      ConnectESMB
      ses_lib.powercycle_pdu1  DUT
      OS Disconnect Device
      Sleep  360
  END
  Sleep  120
  ConnectESMB
  ${ipb}  get_ip_address_from_ipmitool  DUT
  enter_into_bios_setup  DUT   bios_password=${athena_bios_password}
  Check Namespace AppDirect Capacity Information  DUT
  Verify system logs after BIOS test  ${ipb}
  OS Disconnect Device
  Sleep  90

Enable Disable AEP security in BIOS setup
  ConnectESMB
  Navigate to AEP security   DUT   bios_password=${athena_bios_password}
  Enable AEP security  DUT
  Sleep  300
  OS Disconnect Device
  Sleep  60
  ConnectESMB
  Sleep  60
  Navigate to AEP security   DUT   bios_password=${athena_bios_password}
  verify AEP security state  DUT   enabled
  disable_AEP_security    DUT
  Sleep  300
  OS Disconnect Device
  Sleep  60
  ConnectESMB
  Sleep  60
  Navigate to AEP security   DUT   bios_password=${athena_bios_password}
  verify AEP security state  DUT   disabled
  exit_from_AEP_security  DUT
  OS Disconnect Device

