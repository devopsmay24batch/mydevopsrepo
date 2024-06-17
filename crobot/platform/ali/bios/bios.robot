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


*** Settings ***
Documentation       Tests to verify BIOS functions described in the BIOS function SPEC for the project migaloo.

Library           AliBiosLib.py
Library           AliCommonLib.py
Library           CommonLib.py

Resource          CommonKeywords.resource
Resource          AliCommonKeywords.resource
Resource          AliBiosKeywords.resource

Suite Setup       Bios Connect Device
Suite Teardown    Bios Disconnect Device

*** Variables ***
${MAX_LOOP}     4

*** Test Cases ***
ALI_BIOS_TC_002_BIOS_UPDATE_TEST_UNDER_UEFI_SHELL
    [Tags]  ALI_BIOS_TC_002_BIOS_UPDATE_TEST_UNDER_UEFI_SHELL  migaloo  shamu
    [Setup]  prepare file on usb device
    Step  1  update bios in uefi shell  Master  False  ${bios_old_version_pattern}
    Step  2  update bios in uefi shell  Slave  False  ${bios_old_version_pattern}
    Step  3  power cycle to openbmc  timeout=900
    Step  4  verify current boot flash  BIOS  Master
    Step  5  switch bios flash  Slave
    BuiltIn.Sleep  30
    Step  6  update bios in uefi shell  Master  True  ${bios_version_pattern}
    Step  7  update bios in uefi shell  Slave  True  ${bios_version_pattern}
    Step  8  power cycle to openbmc  timeout=900
    Step  9  verify current boot flash  BIOS  Master
    Step  10  switch bios flash  Slave
    BuiltIn.Sleep  30
    [Teardown]  Run Keywords  open prompt  console=${diagos_mode}  sec=300
                ...      AND  clean images  DUT  BIOS
                ...      AND  switch to openbmc
                ...      AND  check and switch bios boot
                ...      AND  recover sonic


ALI_BIOS_TC_003_BIOS_UPDATE_TEST_UNDER_BMC_OS
    [Tags]  ALI_BIOS_TC_003_BIOS_UPDATE_TEST_UNDER_BMC_OS  migaloo  shamu
    Step  1  read smbios and tlv and all eeproms
    Step  2  execute command and verify exit code
    ...  console=${diagos_mode}
    ...  command=dmidecode -t 0 | grep -i version
    Step  3  check and switch bios boot  Master
    Step  4  prepare image  ${bios_local_image_path}  BIOS  upgrade=False
    Step  5  update bios in bmc  Master  False  ${bios_old_version_pattern}
    Step  6  update bios in bmc  Slave  False  ${bios_old_version_pattern}
    Step  7  power cycle to openbmc  timeout=600
    Step  8  verify current boot flash  BIOS  Master
    Step  9  switch bios flash  Slave
    BuiltIn.Sleep  30
    Step  10  check and switch bios boot  Master
    Step  11  prepare image  ${bios_local_image_path}  BIOS  upgrade=True
    Step  12  update bios in bmc  Master  True  ${bios_version_pattern}
    Step  13  update bios in bmc  Slave  True  ${bios_version_pattern}
    Step  14  power cycle to openbmc  timeout=600
    Step  15  verify current boot flash  BIOS  Master
    Step  16  switch bios flash  Slave
    BuiltIn.Sleep  30
    [Teardown]  Run Keywords  switch to openbmc
                ...      AND  clean images  DUT  BIOS
                ...      AND  check and switch bios boot


ALI_BIOS_TC_004_BIOS_INFORMATION_CHECK
    [Tags]  ALI_BIOS_TC_004_BIOS_INFORMATION_CHECK  migaloo  shamu
    Step  1  enter bios post and check bios info
    Step  2  enter bios setup and check bios info
    [Teardown]  exit bios setup


ALI_BIOS_TC_005_ME_INFORMATION_CHECK
    [Tags]  ALI_BIOS_TC_005_ME_INFORMATION_CHECK  migaloo  shamu
    Step  1  enter bios setup
    Step  2  Run Keywords  send key  KEY_RIGHT  2
             ...      AND  send key  KEY_DOWN  7
             ...      AND  send key  KEY_ENTER  1
             ...      AND  BuiltIn.Sleep  3
    ${me_text}  read until regexp
    ...  patterns=${me_config_last_line}
    ...  timeout=60
    Step  3  verify log with keywords  ${me_info_patterns}  ${me_text}
    [Teardown]  exit bios setup


ALI_BIOS_TC_007_BOOT_UEFI_OS_TEST
    [Tags]  ALI_BIOS_TC_007_BOOT_UEFI_OS_TEST  migaloo  shamu
    Step  1  enter bios setup
    Step  2  Run Keywords  send key  KEY_LEFT  2
             ...      AND  BuiltIn.Sleep  3
             ...      AND  send key  KEY_DOWN  4
             ...      AND  BuiltIn.Sleep  3
    ${boot_text}  read until regexp
    ...  patterns=${boot_option_1_selected}
    ...  timeout=60
    Step  3  Run Keywords  send key  KEY_ENTER  1
             ...      AND  BuiltIn.Sleep  3
    ${boot_select_text}  read until regexp
    ...  patterns=${boot_option_last_line}
    ...  timeout=60
    Step  4  select boot option  ${boot_text}  ${boot_select_text}  ${boot_sonic_str}
    Step  5  save and exit bios setup  prompt=${diagos_mode}
    [Teardown]  Run Keyword If Test Failed  recover sonic


ALI_BIOS_TC_008_BOOT_OS_SUPPORT_TEST
    [Tags]  ALI_BIOS_TC_008_BOOT_OS_SUPPORT_TEST  migaloo  shamu
    Step  1  enter bios setup
    Step  2  select boot override in bios setup  ${boot_onie_str}  ${onie_mode}
    Step  3  enter bios setup  ${onie_mode}
    Step  4  select boot override in bios setup  ${boot_uefi_str}  ${uefi_mode}
    Step  5  enter bios setup  ${uefi_mode}
    Step  6  select boot override in bios setup  ${boot_sonic_str}  ${diagos_mode}
    [Teardown]  Run Keyword If Test Failed  recover sonic


ALI_BIOS_TC_011_BOOT_OVERRIDE_TEST
    [Tags]  ALI_BIOS_TC_011_BOOT_OVERRIDE_TEST  migaloo  shamu
    Step  1  enter bios setup
    Step  2  select boot override in bios setup  ${boot_onie_str}  ${onie_mode}
    Step  3  enter bios setup  ${onie_mode}
    Step  4  select boot override in bios setup  ${boot_sonic_str}  ${diagos_mode}
    [Teardown]  Run Keyword If Test Failed  recover sonic


ALI_BIOS_TC_012_CPU_INFORMATION_TEST
    [Tags]  ALI_BIOS_TC_012_CPU_INFORMATION_TEST  migaloo  shamu
    Step  1  set cores enabled  0
    Step  2  verify processor info in bios post and setup
    Step  3  check cpu information and number of processors  6
    Run Keyword If  'migaloo' in '${devicename}'
    ...  Step  4  check cpu real frequency with power thermal utility
    Step  5  set cores enabled  1
    Step  6  verify processor info in bios post and setup
    Step  7  check cpu information and number of processors  1
    Step  8  set cores enabled  2
    Step  9  verify processor info in bios post and setup
    Step  10  check cpu information and number of processors  2
    Step  11  set cores enabled  3
    Step  12  verify processor info in bios post and setup
    Step  13  check cpu information and number of processors  3
    Step  14  set cores enabled  4
    Step  15  verify processor info in bios post and setup
    Step  16  check cpu information and number of processors  4
    Step  17  set cores enabled  5
    Step  18  verify processor info in bios post and setup
    Step  19  check cpu information and number of processors  5
    [Teardown]  Run Keywords  recover sonic
                ...      AND  set cores enabled  0
                ...      AND  recover sonic


ALI_BIOS_TC_013_CPU_MICROCODE_TEST
    [Tags]  ALI_BIOS_TC_013_CPU_MICROCODE_TEST  migaloo  shamu
    Step  1  enter bios setup
    Step  2  Run Keywords  send key  KEY_RIGHT  2
    ...      AND  BuiltIn.Sleep  3
    ...      AND  send key  KEY_ENTER  1
    ...      AND  BuiltIn.Sleep  3
    ${proc_text}=  read until regexp
    ...  patterns=${proc_config_last_line}
    ...  timeout=60
    Step  3  search for a pattern  ${proc_text}  ${microcode_rev_setup_pattern}
    ${microcode_rev_in_setup}=  Convert To Hex  ${match['revision1']}  base=16
    Step  4  exit bios setup
    Step  5  execute command and verify with a pattern
    ...  console=${diagos_mode}
    ...  command=${dmesg_microcode_cmd}
    ...  pattern=${microcode_rev_dmesg_pattern}
    ${microcode_rev_in_dmesg}=  Convert To Hex  ${match['revision2']}  base=16
    Step  6  Should Be Equal  ${microcode_rev_in_setup}  ${microcode_rev_in_dmesg}
    [Teardown]  Run Keyword If Test Failed  recover sonic


ALI_BIOS_TC_014_HYPER_THREAD_FUNCTIONAL_TEST
    [Tags]  ALI_BIOS_TC_014_HYPER_THREAD_FUNCTIONAL_TEST  migaloo  shamu
    Step  1  verify cpu hyper thread status  Enable  need_exit=${TRUE}
    Step  2  verify processor info in bios post and setup
    Step  3  check cpu information  12
    Step  4  set cpu hyper thread  Disable
    Step  5  verify processor info in bios post and setup
    Step  6  check cpu information  6
    [Teardown]  Run Keywords  recover sonic
                ...      AND  set cpu hyper thread  Enable
                ...      AND  recover sonic


ALI_BIOS_TC_015_MEMORY_INFORMATION_TEST
    [Tags]  ALI_BIOS_TC_015_MEMORY_INFORMATION_TEST  migaloo  shamu
    ${post_text}=  enter bios setup
    ...  prompt=${diagos_mode}
    ...  post_list=${post_test_list}
    Step  1  search for a pattern  ${post_text}  ${memory_info_pattern}
    ${setup_text}=  read until regexp
    ...  patterns=${bios_info_last_line}
    ...  timeout=60
    Step  2  search for a pattern  ${setup_text}  ${memory_size_pattern}
    Step  3  exit bios setup
    Step  4  execute command and verify with ordered pattern list
    ...  console=${diagos_mode}
    ...  command=cat /proc/meminfo
    ...  patterns=${meminfo_patterns}
    ...  msg=Failed to show memory information
    #### Step to plug out DIMM memory should be manual test ####
    [Teardown]  Run Keyword If Test Failed  recover sonic


ALI_BIOS_TC_016_PCIE_BUS_SCAN
    [Tags]  ALI_BIOS_TC_016_PCIE_BUS_SCAN  migaloo  shamu
    Step  1  boot into uefi mode
    Step  2  verify pci command uefi mode
    ...  expected_list=${pci_uefi_patterns}
    Step  3  boot into diagos mode
    BuiltIn.Sleep  30
    Step  4  execute command and verify exit code
    ...  console=${diagos_mode}
    ...  command=lspci
    Step  5  verify log with keywords
    ...  regex_list=${pci_diag_patterns}
    ...  target_log=${text}
    [Teardown]  Run Keyword If Test Failed  recover sonic


ALI_BIOS_TC_017_CPU_I2C_INTERFACE_TEST
    [Tags]  ALI_BIOS_TC_017_CPU_I2C_INTERFACE_TEST  migaloo  shamu
    Step  1  execute command and verify exit code
    ...  console=${diagos_mode}
    ...  command=./cel-i2c-test -s
    ...  path=${diag_cpu_path}
    ...  sec=480
    Step  2  verify log with keywords
    ...  regex_list=${i2c_all_bus_patterns}
    ...  target_log=${text}


ALI_BIOS_TC_018_CPU_LPC_INTERFACE_TEST
    [Tags]  ALI_BIOS_TC_018_CPU_LPC_INTERFACE_TEST  migaloo  shamu
    Step  1  execute command and verify with a pattern
    ...  console=${diagos_mode}
    ...  command=./lpc_cpld_x64_64 blu r 0xa1e0
    ...  path=${diag_util_cpu_path}
    ...  sec=30
    ...  pattern=^ (?P<value>${cpld_c_hex_ver})
    Step  2  execute command and verify with a pattern
    ...  console=${diagos_mode}
    ...  command=./lpc_cpld_x64_64 blu r 0xa100
    ...  path=${diag_util_cpu_path}
    ...  sec=30
    ...  pattern=^ (?P<value>${cpld_b_hex_ver})
    Step  3  execute command and verify with a pattern
    ...  console=${diagos_mode}
    ...  command=./lpc_cpld_x64_64 blu w 0xa1e1 0x10
    ...  path=${diag_util_cpu_path}
    ...  sec=30
    ...  pattern=value: (?P<value>0x10)
    Step  4  execute command and verify with a pattern
    ...  console=${diagos_mode}
    ...  command=./lpc_cpld_x64_64 blu w 0xa101 0x2
    ...  path=${diag_util_cpu_path}
    ...  sec=30
    ...  pattern=value: (?P<value>0x2)
    Step  5  execute command and verify with a pattern
    ...  console=${diagos_mode}
    ...  command=./lpc_cpld_x64_64 blu r 0xa1e1
    ...  path=${diag_util_cpu_path}
    ...  sec=30
    ...  pattern=^ (?P<value>0x10)
    Step  6  execute command and verify with a pattern
    ...  console=${diagos_mode}
    ...  command=./lpc_cpld_x64_64 blu r 0xa101
    ...  path=${diag_util_cpu_path}
    ...  sec=30
    ...  pattern=^ (?P<value>0x2)
    Step  7  execute command and verify with a pattern
    ...  console=${diagos_mode}
    ...  command=./lpc_cpld_x64_64 blu w 0xa1e1 0x14
    ...  path=${diag_util_cpu_path}
    ...  sec=30
    ...  pattern=value: (?P<value>0x14)
    Step  8  execute command and verify with a pattern
    ...  console=${diagos_mode}
    ...  command=./lpc_cpld_x64_64 blu w 0xa101 0xe
    ...  path=${diag_util_cpu_path}
    ...  sec=30
    ...  pattern=value: (?P<value>0xe)
    Step  9  execute command and verify with a pattern
    ...  console=${diagos_mode}
    ...  command=./lpc_cpld_x64_64 blu r 0xa1e1
    ...  path=${diag_util_cpu_path}
    ...  sec=30
    ...  pattern=^ (?P<value>0x14)
    Step  10  execute command and verify with a pattern
    ...  console=${diagos_mode}
    ...  command=./lpc_cpld_x64_64 blu r 0xa101
    ...  path=${diag_util_cpu_path}
    ...  sec=30
    ...  pattern=^ (?P<value>0xe)


ALI_BIOS_TC_019_MANAGEMENT_PORT_INFORMATION_CHECK_TEST
    [Tags]  ALI_BIOS_TC_019_MANAGEMENT_PORT_INFORMATION_CHECK_TEST  migaloo  shamu
    Step  1  enter bios setup
    Step  2  verify management port info in bios setup
    Step  3  exit bios setup
    Step  4  boot into uefi mode
    Step  5  verify pci command uefi mode
    ...  expected_list=${pci_mgmt_patterns}
    Step  6  boot into diagos mode
    Step  7  verify pci management port
    [Teardown]  Run Keyword If Test Failed  recover sonic


ALI_BIOS_TC_021_SATA_INITIALIZATION
    [Tags]  ALI_BIOS_TC_021_SATA_INITIALIZATION  migaloo  shamu
    Step  1  enter bios setup
    Step  2  Run Keywords  send key  KEY_RIGHT  2
             ...      AND  send key  KEY_DOWN  5
             ...      AND  send key  KEY_ENTER  1
             ...      AND  send key  KEY_DOWN  2
             ...      AND  send key  KEY_ENTER  1
             ...      AND  BuiltIn.Sleep  3
    ${sata_text}  read until regexp
    ...  patterns=${pch_sata_last_line}
    ...  timeout=60
    Step  3  verify log with keywords  ${sata_config_patterns}  ${sata_text}
    Step  4  Run Keywords  send key  KEY_ESC  2
             ...      AND  send key  KEY_LEFT  2
             ...      AND  BuiltIn.Sleep  3
    Step  5  select boot override in bios setup  ${boot_sonic_str}  ${diagos_mode}
    [Teardown]  Run Keyword If Test Failed  recover sonic


ALI_BIOS_TC_022_USB_DETECT_TEST
    [Tags]  ALI_BIOS_TC_022_USB_DETECT_TEST  migaloo  shamu
    Step  1  enter bios setup
    Step  2  Run Keywords  send key  KEY_LEFT  1
             ...      AND  send key  KEY_UP  1
             ...      AND  BuiltIn.Sleep  5
    ${boot_override_text}=  read until regexp
    ...  patterns=${boot_override_last_line}
    ...  timeout=60
    Step  3  search for a pattern  ${boot_override_text}  ${boot_usb_pattern}
    Step  4  exit bios setup
    Step  5  boot into uefi mode
    Step  6  send cmd regexp  cls  ${uefi_prompt}  timeout=30
    Step  7  send cmd regexp  ${usb_uefi_path}  ${uefi_prompt}  timeout=30
    Step  8  send cmd regexp  dir  ${dir_last_line}  timeout=30
    Step  9  boot into diagos mode
    Step  10  execute command and verify with a pattern
    ...  console=${diagos_mode}
    ...  command=fdisk -l
    ...  pattern=${usb_diag_path}
    ...  msg=Not found USB disk
    [Teardown]  Run Keyword If Test Failed  recover sonic


ALI_BIOS_TC_023_USB_R/W_TEST
    [Tags]  ALI_BIOS_TC_023_USB_R/W_TEST  migaloo  shamu
    [Setup]  Run Keywords  create dir  /mnt  ${diagos_mode}
             ...      AND  execute command and verify exit code
                           ...  console=${diagos_mode}
                           ...  command=dd if=/dev/zero of=/home/admin/test bs=1M count=60
    Step  1  execute command and verify with a pattern
    ...  console=${diagos_mode}
    ...  command=fdisk -l
    ...  pattern=\\/dev\\/sdb1
    ...  msg=Not found USB disk
    Step  2  execute command and verify exit code
    ...  console=${diagos_mode}
    ...  command=mount /dev/sdb1 /mnt
    Step  3  execute command and verify exit code
    ...  console=${diagos_mode}
    ...  command=cp /home/admin/test /mnt
    Step  4  execute command and verify exit code
    ...  console=${diagos_mode}
    ...  command=sync
    Step  5  is file/folder exists
    ...  console=${diagos_mode}
    ...  file=/mnt/test
    Step  6  execute command and verify exit code
    ...  console=${diagos_mode}
    ...  command=cp /mnt/test /home
    Step  7  execute command and verify exit code
    ...  console=${diagos_mode}
    ...  command=sync
    Step  8  is file/folder exists
    ...  console=${diagos_mode}
    ...  file=/home/test
    [Teardown]  Run Keywords  remove file/folder  console=${diagos_mode}  file=/home/admin/test
                ...      AND  remove file/folder  console=${diagos_mode}  file=/home/test
                ...      AND  remove file/folder  console=${diagos_mode}  file=/mnt/test
                ...      AND  Run Keyword And Ignore Error  execute command and verify exit code
                              ...  console=${diagos_mode}
                              ...  command=umount /mnt


ALI_BIOS_TC_027_POST_INFORMATION_TEST
    [Tags]  ALI_BIOS_TC_027_POST_INFORMATION_TEST  migaloo  shamu
    ${post_text}=  enter bios setup
    ...  prompt=${diagos_mode}
    ...  post_list=${post_test_list}
    Step  1  verify log with keywords
    ...  regex_list=${bios_post_info_patterns}
    ...  target_log=${post_text}
    Step  2  verify log with keywords
    ...  regex_list=${evaluation_keywords}
    ...  target_log=${post_text}
    ...  check_fail=True
    Step  3  exit bios setup
    [Teardown]  Run Keyword If Test Failed  recover sonic


ALI_BIOS_TC_028_POST_HOTKEY_TEST
    [Tags]  ALI_BIOS_TC_028_POST_HOTKEY_TEST  migaloo  shamu
    Step  1  enter bios setup  enter_key=KEY_DEL
    Step  2  exit bios setup
    Step  3  enter bios setup  enter_key=KEY_ESC
    Step  4  exit bios setup
    Step  5  enter bios boot selection  enter_key=KEY_F7  console=${diagos_mode}
    Step  6  select boot option  ${bbs_text}  ${bbs_text}  ${boot_onie_str}  is_bbs=True
    BuiltIn.Sleep  10
    Step  7  Run Keywords  open prompt  ${onie_mode}  300
             ...      AND  BuiltIn.Sleep  10
             ...      AND  send a line   onie-stop
    Step  8  enter bios boot selection  enter_key=KEY_ESC+7  console=${onie_mode}
    Step  9  send key  KEY_ENTER  1
    Step  10  open prompt  ${diagos_mode}  300
    [Teardown]  Run Keyword If Test Failed  recover sonic


ALI_BIOS_TC_029_SETUP_HOTKEY_TEST
    [Tags]  ALI_BIOS_TC_029_SETUP_HOTKEY_TEST  migaloo  shamu
    Step  1  enter bios setup
    Step  2  Run Keywords  send key  KEY_RIGHT  3
             ...      AND  BuiltIn.Sleep  3
             ...      AND  read until regexp  patterns=${security_last_line}  timeout=60
    Step  3  Run Keywords  send key  KEY_LEFT  1
             ...      AND  BuiltIn.Sleep  3
             ...      AND  read until regexp  patterns=${intel_setup_last_line}  timeout=60
    Step  4  Run Keywords  send key  KEY_DOWN  5
             ...      AND  send key  KEY_ENTER  1
             ...      AND  BuiltIn.Sleep  3
             ...      AND  read until regexp  patterns=${pch_config_last_line}  timeout=60
    Step  5  Run Keywords  send key  KEY_ESC  1
             ...      AND  BuiltIn.Sleep  3
             ...      AND  read until regexp  patterns=${intel_setup_last_line}  timeout=60
    Step  6  Run Keywords  send key  KEY_UP  5
             ...      AND  send key  KEY_ENTER  3
             ...      AND  BuiltIn.Sleep  3
             ...      AND  read until regexp  patterns=${cores_en_0_pattern}  timeout=60
    Step  7  Run Keywords  send key  KEY_PLUS  3
             ...      AND  send key  KEY_ESC  1
             ...      AND  send key  KEY_ENTER  1
             ...      AND  BuiltIn.Sleep  3
             ...      AND  read until regexp  patterns=${cores_en_3_pattern}  timeout=60
    Step  8  Run Keywords  send key  KEY_MINUS  2
             ...      AND  send key  KEY_ESC  1
             ...      AND  send key  KEY_ENTER  1
             ...      AND  BuiltIn.Sleep  3
             ...      AND  read until regexp  patterns=${cores_en_1_pattern}  timeout=60
    Step  9  Run Keywords  send key  KEY_F1  1
             ...      AND  BuiltIn.Sleep  3
             ...      AND  read until regexp  patterns=${help_last_line}  timeout=60
             ...      AND  send key  KEY_ESC  1
    Step  10  Run Keywords  send key  KEY_F2  1
              ...      AND  BuiltIn.Sleep  3
              ...      AND  read until regexp  patterns=${load_previous_line}  timeout=60
              ...      AND  send key  KEY_ESC  1
    Step  11  Run Keywords  send key  KEY_F9  1
              ...      AND  BuiltIn.Sleep  3
              ...      AND  read until regexp  patterns=${load_optimized_line}  timeout=60
              ...      AND  send key  KEY_ESC  1
    Step  12  save and exit bios setup
    Step  13  enter bios setup
    Step  14  Run Keywords  send key  KEY_RIGHT  2
             ...      AND  BuiltIn.Sleep  3
             ...      AND  send key  KEY_ENTER  3
             ...      AND  BuiltIn.Sleep  3
             ...      AND  read until regexp  patterns=${cores_en_1_pattern}  timeout=60
    Step  15  exit bios setup
    [Teardown]  Run Keywords  recover sonic
                ...      AND  set cores enabled  0
                ...      AND  recover sonic


ALI_BIOS_TC_030_FUNCTION_KEY_ERROR_INJECTION_TEST
    [Tags]  ALI_BIOS_TC_030_FUNCTION_KEY_ERROR_INJECTION_TEST  migaloo  shamu
    Step  1  enter bios setup
    Step  2  Run Keywords  send key  KEY_7  1
              ...     AND  BuiltIn.Sleep  3
              ...     AND  read until regexp  patterns=${bios_info_last_line}  timeout=60
    Step  3  Run Keywords  send key  KEY_LEFT  1
              ...     AND  send key  KEY_UP  1
              ...     AND  BuiltIn.Sleep  3
              ...     AND  read until regexp  patterns=${boot_override_last_line}  timeout=60
    Step  4  Run Keywords  send key  KEY_RIGHT  1
              ...     AND  BuiltIn.Sleep  3
              ...     AND  read until regexp  patterns=${bios_info_last_line}  timeout=60
    Step  5  Run Keywords  send key  KEY_DOWN  1
             ...      AND  send key char  ${mm_test}
             ...      AND  send key  KEY_ENTER  1
             ...      AND  send key char  ${dd_test}
             ...      AND  send key  KEY_ENTER  1
             ...      AND  send key char  ${yy_test}
    Step  6  Run Keywords  send key  KEY_DOWN  1
             ...      AND  send key char  ${hr_test}
             ...      AND  send key  KEY_ENTER  1
             ...      AND  send key char  ${min_test}
             ...      AND  send key  KEY_ENTER  1
             ...      AND  send key char  ${sec_test}
             ...      AND  BuiltIn.Sleep  3
    Step  7  save and exit bios setup
    Step  8  enter bios setup
    ${bios_info_text}=  read until regexp  patterns=${bios_info_last_line}  timeout=60
    Step  9  search for a pattern  ${bios_info_text}  ${system_date_pattern}
    Step  10  Should Be Equal  ${match['system_date']}  ${mm_test}/${dd_test}/${yy_test}
    Step  11  search for a pattern  ${bios_info_text}  ${system_time_pattern}
    ${diff_time}=  Subtract Time From Time  ${match['system_time']}  ${hr_test}:${min_test}:${sec_test}
    Step  12  Should Be True  ${diff_time} < 210  ### compare time should be different from changing value less than 210 sec.
    Step  13  exit bios setup
    [Teardown]  Run Keyword If Test Failed  recover sonic


ALI_BIOS_TC_031_S0_STATE_TEST
    [Tags]  ALI_BIOS_TC_031_S0_STATE_TEST  migaloo  shamu
    Step  1  power cycle to openbmc  timeout=600
    Step  2  execute command and verify exit code
    ...  path=${diag_cpu_path}
    ...  console=${diagos_mode}
    ...  command=${ali_version_test_command}
    ...  msg=Failed to run command '${ali_version_test_command}'
    Step  3  execute command and verify exit code
    ...  console=${diagos_mode}
    ...  command=${ali_mem_test_command}
    ...  sec=180
    ...  msg=Failed to run command '${ali_mem_test_command}'
    Step  4  execute command and verify exit code
    ...  path=/home/admin
    ...  console=${diagos_mode}
    ...  command=ls /home/admin
    ...  msg=Failed to run command 'ls'
    [Teardown]  Run Keyword If Test Failed  recover cpu

ALI_BIOS_TC_032_S5_STATE_TEST
    [Tags]  ALI_BIOS_TC_032_S5_STATE_TEST  migaloo  shamu
    [Setup]  Run Keyword And Ignore Error
    ...  change kernel log level  console=${openbmc_mode}  level=3
    Step  1  boot into diagos mode
    Step  2  send cmd regexp
    ...  cmd=poweroff
    ...  promptRegexp=reboot: Power down
    ...  timeout=150
    Step  3  switch to openbmc
    Step  4  verify power status  off
    Step  5  execute command and verify with a pattern
    ...  console=${openbmc_mode}
    ...  command=cat /tmp/powerled
    ...  pattern=yellow
    ...  msg=Failed to verify power led!
    Step  6  verify power control  on
    Step  7  power cycle to openbmc  timeout=600
    [Teardown]  Run Keywords  recover cpu
    ...  AND  Run Keyword And Ignore Error  change kernel log level  console=${openbmc_mode}  level=7


ALI_BIOS_TC_033_BACKUP_BIOS_AUTO_BOOT_TEST
    [Tags]  ALI_BIOS_TC_033_BACKUP_BIOS_AUTO_BOOT_TEST  migaloo  shamu
    [Setup]  check and switch bios boot  Master
    Step  1  prepare file on usb device
    Step  2  update bios crash
    Step  3  BuiltIn.Sleep  300
    Step  4  verify current boot flash  BIOS  slave
    Step  5  restore bios master
    [Teardown]  Run Keyword If Test Failed
                         ...  Run Keywords  open prompt  console=${diagos_mode}  sec=300
                         ...           AND  switch to openbmc
                         ...           AND  restore bios master
                         ...           AND  recover cpu

ALI_BIOS_TC_034_BACKUP_BIOS_BASIC_FUNCTION_TEST
    [Tags]  ALI_BIOS_TC_034_BACKUP_BIOS_BASIC_FUNCTION_TEST  migaloo  shamu
    [Setup]  switch bios flash  slave
    Step  1  execute command and verify exit code
    ...  console=${diagos_mode}
    ...  command=lspci
    Step  2  verify log with keywords
    ...  regex_list=${pci_diag_patterns}
    ...  target_log=${text}
    Step  3  execute command and verify exit code
    ...  console=${diagos_mode}
    ...  command=./cel-i2c-test -s
    ...  path=${diag_cpu_path}
    ...  sec=480
    Step  4  verify log with keywords
    ...  regex_list=${i2c_all_bus_patterns}
    ...  target_log=${text}
    Step  5  execute command and verify with a pattern
    ...  console=${diagos_mode}
    ...  command=./lpc_cpld_x64_64 blu r 0xa1e0
    ...  path=${diag_util_cpu_path}
    ...  sec=30
    ...  pattern=^ (?P<value>${cpld_c_hex_ver})
    Step  6  execute command and verify with a pattern
    ...  console=${diagos_mode}
    ...  command=./lpc_cpld_x64_64 blu r 0xa100
    ...  path=${diag_util_cpu_path}
    ...  sec=30
    ...  pattern=^ (?P<value>${cpld_b_hex_ver})
    Step  7  execute command and verify with a pattern
    ...  console=${diagos_mode}
    ...  command=./lpc_cpld_x64_64 blu w 0xa1e1 0x10
    ...  path=${diag_util_cpu_path}
    ...  sec=30
    ...  pattern=value: (?P<value>0x10)
    Step  8  execute command and verify with a pattern
    ...  console=${diagos_mode}
    ...  command=./lpc_cpld_x64_64 blu w 0xa101 0x2
    ...  path=${diag_util_cpu_path}
    ...  sec=30
    ...  pattern=value: (?P<value>0x2)
    Step  9  execute command and verify with a pattern
    ...  console=${diagos_mode}
    ...  command=./lpc_cpld_x64_64 blu r 0xa1e1
    ...  path=${diag_util_cpu_path}
    ...  sec=30
    ...  pattern=^ (?P<value>0x10)
    Step  10  execute command and verify with a pattern
    ...  console=${diagos_mode}
    ...  command=./lpc_cpld_x64_64 blu r 0xa101
    ...  path=${diag_util_cpu_path}
    ...  sec=30
    ...  pattern=^ (?P<value>0x2)
    [Teardown]  switch bios flash  master


ALI_BIOS_TC_035_SMBIOS_TABLE_R/W
    [Tags]  ALI_BIOS_TC_035_SMBIOS_TABLE_R/W  migaloo  shamu
    [Setup]  set test variable  ${smbios_store}  ${None}
    Step  1  check and switch bios boot  Master
    ${smbios_store}=  read eeprom
    ...  eeprom_path=${smbios_eeprom_path}
    ...  console=${diagos_mode}
    ...  pattern=${smbios_eeprom_pattern}
    Step  2   execute command and verify with ordered pattern list
    ...  console=${diagos_mode}
    ...  command=dmidecode -t 1
    ...  patterns=${diagos_dmidecode_t1_patterns}
    ...  msg=Failed to show dmidecode/system info!
    Step  3   execute command and verify with ordered pattern list
    ...  console=${diagos_mode}
    ...  command=dmidecode -t 2
    ...  patterns=${diagos_dmidecode_t2_patterns}
    ...  msg=Failed to show dmidecode/board info!
    Step  4   execute command and verify with ordered pattern list
    ...  console=${diagos_mode}
    ...  command=dmidecode -t 3
    ...  patterns=${diagos_dmidecode_t2_patterns}
    ...  msg=Failed to show dmidecode/board info!
    Step  5  write and read smbios eeprom  SMBIOS_EEPROM_TEST
    Step  6  write and read smbios eeprom  SMBIOS_EEPROM_TEST2
    Step  7  switch bios flash  slave
    Step  8  write and read smbios eeprom  SMBIOS_EEPROM_TEST
    Step  9  switch bios flash  slave
    Step  10  write and read smbios eeprom  SMBIOS_EEPROM_TEST2
    [Teardown]  Run Keywords  check and switch bios boot  Master
                ...      AND  Run Keyword Unless  ${smbios_store} is ${None}
                ...           restore smbios eeprom  ${smbios_store}


ALI_BIOS_TC_036_GPIO_CHECK
    [Tags]  ALI_BIOS_TC_036_GPIO_CHECK  migaloo  shamu
    [Setup]  prepare ru on usb device
    Step  1  boot into uefi mode
    Step  2  send a line  cls
    Step  3  Run Keywords  send a line  ${usb_uefi_path}
             ...      AND  send cmd regexp  cmd=dir  promptRegexp=${dir_last_line}  timeout=30
    Step  4  Run Keywords  send a line  cd ${ru_dir_name}
             ...      AND  send cmd regexp  cmd=dir  promptRegexp=${dir_last_line}  timeout=30
    Step  5  send cmd regexp  cmd=${ru_cmd}  promptRegexp=${ru_last_line}  timeout=90
    Step  6  select IO space
    Step  7  change data width to 32

    Step  8  verify gpio target  ${gpio_0_31_list}  ${gpio_0_31_target_dict}
    Step  9  verify gpio IO  ${gpio_0_31_list}  ${gpio_0_31_io_dict}
#    Step  10  verify gpio value  ${gpio_0_31_list}  ${gpio_0_31_val_dict}  key_count=${2}

    Step  11  Run Keywords  send key  KEY_DOWN  3  ${10}
              ...      AND  send key  KEY_LEFT  1  ${10}
              ...      AND  BuiltIn.Sleep  10
    Step  12  verify gpio target  ${gpio_32_63_list}  ${gpio_32_63_target_dict}  mult=1
    Step  13  verify gpio IO  ${gpio_32_63_list}  ${gpio_32_63_io_dict}  mult=1
#    Step  14  verify gpio value  ${gpio_32_63_list}  ${gpio_32_63_val_dict}  mult=1

    Step  15  Run Keywords  send key  KEY_DOWN  1  ${10}
              ...      AND  send key  KEY_LEFT  1  ${10}
              ...      AND  BuiltIn.Sleep  10
    Step  16  verify gpio target  ${gpio_65_95_list}  ${gpio_65_95_target_dict}  mult=2
    Step  17  verify gpio IO  ${gpio_65_95_list}  ${gpio_65_95_io_dict}  mult=2
#    Step  18  verify gpio value  ${gpio_65_95_list}  ${gpio_65_95_val_dict}  mult=2

    [Teardown]  Run Keywords  exit ru.efi
                ...      AND  boot into diagos mode
                ...      AND  recover cpu


ALI_BIOS_TC_037_ADMINISTRATOR_PASSWORD_TEST
    [Tags]  ALI_BIOS_TC_037_ADMINISTRATOR_PASSWORD_TEST  migaloo  shamu
    [Setup]  set test variable  ${current_pass}  ${EMPTY}
    ### Set an administrator password
    Step  1  set bios password  administrator  password=1234
    set test variable  ${current_pass}  1234

    ### Boot to setup with the new administrator password
    Step  2  enter bios setup  bios_password=1234
    Step  3  exit bios setup  prompt=${diagos_mode}

    ### Boot to setup with an incorrect administrator password
    Step  4  enter bios setup  bios_password=0000  enter_line=${invalid_pass_pattern}

    ### Try again with an correct administrator password
    Step  5  Run Keywords  send key  KEY_ENTER  1
             ...      AND  send key char  1234
             ...      AND  send key  KEY_ENTER  1
             ...      AND  BuiltIn.Sleep  3
             ...      AND  read until regexp  patterns=${BIOS_HEADER_KEYWORD}  timeout=60

    ### Set another administrator password
    Step  6  Run Keywords  send key  KEY_RIGHT  3
              ...      AND  BuiltIn.Sleep  5
              ...      AND  read until regexp  patterns=${security_last_line}  timeout=60
    Step  7  Run Keywords  send key  KEY_ENTER  1
              ...      AND  BuiltIn.Sleep  3
              ...      AND  read until regexp  patterns=${current_pass_pattern}  timeout=60
              ...      AND  send key char  1234
              ...      AND  send key  KEY_ENTER  1
              ...      AND  BuiltIn.Sleep  3
    Step  8  Run Keywords  read until regexp  patterns=${create_pass_pattern}  timeout=60
              ...      AND  send key char  5678
              ...      AND  send key  KEY_ENTER  1
              ...      AND  BuiltIn.Sleep  3
    Step  9  Run Keywords  read until regexp  patterns=${confirm_pass_pattern}  timeout=60
              ...      AND  send key char  5678
              ...      AND  send key  KEY_ENTER  1
              ...      AND  BuiltIn.Sleep  3
    Step  10  save and exit bios setup
    set test variable  ${current_pass}  5678

    ### Boot to setup with the new administrator password
    Step  11  enter bios setup  bios_password=5678
    Step  12  exit bios setup  prompt=${diagos_mode}

    [Teardown]  Run Keyword Unless  '${current_pass}' == '${EMPTY}'
    ...  clear bios password  administrator  ${current_pass}


ALI_BIOS_TC_038_USER_PASSWORD_TEST
    [Tags]  ALI_BIOS_TC_038_USER_PASSWORD_TEST  migaloo  shamu
    [Setup]  Run Keywords  set test variable  ${current_admin_pass}  ${EMPTY}
             ...      AND  set test variable  ${current_user_pass}  ${EMPTY}
             ...      AND  set bios password  administrator  password=4321
             ...      AND  set test variable  ${current_admin_pass}  4321

    ### Set a new user password
    Step  1  set bios password  user  password=2345  current_pass=${current_admin_pass}
    set test variable  ${current_user_pass}  2345

    ### Boot to setup with the user password
    Step  2  enter bios setup  bios_password=2345

    ### Set another user password
    Step  3  Run Keywords  BuiltIn.Sleep  2
             ...      AND  send key  KEY_RIGHT  3
             ...      AND  BuiltIn.Sleep  5
             ...      AND  read until regexp  patterns=${security_last_line}  timeout=60
    Step  4  Run Keywords  send key  KEY_DOWN  1
             ...      AND  send key  KEY_ENTER  1
             ...      AND  BuiltIn.Sleep  3
             ...      AND  read until regexp  patterns=${current_pass_pattern}  timeout=60
             ...      AND  send key char  2345
             ...      AND  send key  KEY_ENTER  1
             ...      AND  BuiltIn.Sleep  3
    Step  5  Run Keywords  read until regexp  patterns=${create_pass_pattern}  timeout=60
             ...      AND  send key char  6789
             ...      AND  send key  KEY_ENTER  1
             ...      AND  BuiltIn.Sleep  3
    Step  6  Run Keywords  read until regexp  patterns=${confirm_pass_pattern}  timeout=60
             ...      AND  send key char  6789
             ...      AND  send key  KEY_ENTER  1
             ...      AND  BuiltIn.Sleep  3
    Step  7  save and exit bios setup
    set test variable  ${current_user_pass}  6789

    ### Boot to setup with an incorrect user password
    Step  8  enter bios setup  bios_password=0000  enter_line=${invalid_pass_pattern}

    ### Try again with an correct user password
    Step  9  Run Keywords  send key  KEY_ENTER  1
              ...      AND  send key char  6789
              ...      AND  send key  KEY_ENTER  1
              ...      AND  BuiltIn.Sleep  3
              ...      AND  read until regexp  patterns=${ENTER_BIOS_KEYWORD}  timeout=60
              ...      AND  send key  KEY_DEL  1
              ...      AND  read until regexp  patterns=${BIOS_HEADER_KEYWORD}  timeout=60
    Step  10  exit bios setup  prompt=${diagos_mode}

    [Teardown]  Run Keywords  Run Keyword Unless  '${current_admin_pass}' == '${EMPTY}'
                              ...  clear bios password  administrator  ${current_admin_pass}
                ...      AND  Run Keyword Unless  '${current_user_pass}' == '${EMPTY}'
                              ...  clear bios password  user  ${current_user_pass}


ALI_BIOS_TC_039_ACCESS_LEVEL_TEST
    [Tags]  ALI_BIOS_TC_039_ACCESS_LEVEL_TEST  migaloo  shamu
    [Setup]  Run Keywords  set test variable  ${current_admin_pass}  ${EMPTY}
             ...      AND  set test variable  ${current_user_pass}  ${EMPTY}
    Step  1  set bios password  administrator  password=1234
    set test variable  ${current_admin_pass}  1234
    Step  2  set bios password  user  password=5678  current_pass=${current_admin_pass}
    set test variable  ${current_user_pass}  5678
    Step  3  enter bios setup  bios_password=${current_admin_pass}
    ${bios_info_text}=  read until regexp  patterns=${bios_info_last_line}  timeout=60
    Step  4  search for a pattern  ${bios_info_text}  ${level_admin_pattern}
    Step  5  exit bios setup
    Step  6  enter bios setup  bios_password=${current_user_pass}
    ${bios_info_text}=  read until regexp  patterns=${bios_info_last_line}  timeout=60
    Step  7  search for a pattern  ${bios_info_text}  ${level_user_pattern}
    Step  8  exit bios setup

    [Teardown]  Run Keywords  Run Keyword Unless  '${current_admin_pass}' == '${EMPTY}'
                              ...  clear bios password  administrator  ${current_admin_pass}
                ...      AND  Run Keyword Unless  '${current_user_pass}' == '${EMPTY}'
                              ...  clear bios password  user  ${current_user_pass}


ALI_BIOS_TC_040_SETUP_MENU_CHECK
    [Tags]  ALI_BIOS_TC_040_SETUP_MENU_CHECK  migaloo  shamu
    Step  1  Run Keywords  enter bios setup
             ...      AND  BuiltIn.Sleep  3
             ...      AND  read until regexp  patterns=${bios_info_last_line}  timeout=30
    Step  2  Run Keywords  send key  KEY_RIGHT  1
             ...      AND  BuiltIn.Sleep  5
             ...      AND  read until regexp  patterns=${advance_last_line}  timeout=30
    Step  3  enter sub menu 2
    Step  4  Run Keywords  send key  KEY_ESC  1
             ...      AND  BuiltIn.Sleep  5
             ...      AND  send key  KEY_RIGHT  1
             ...      AND  BuiltIn.Sleep  5
             ...      AND  read until regexp  patterns=${intel_setup_last_line}  timeout=30
    Step  5  enter sub menu 3
    Step  6  Run Keywords  send key  KEY_ESC  1
             ...      AND  BuiltIn.Sleep  5
             ...      AND  send key  KEY_RIGHT  1
             ...      AND  BuiltIn.Sleep  5
             ...      AND  read until regexp  patterns=${security_last_line}  timeout=30
    Step  7  enter sub menu 4
    Step  8  Run Keywords  send key  KEY_ESC  1
             ...      AND  BuiltIn.Sleep  5
             ...      AND  send key  KEY_RIGHT  1
             ...      AND  BuiltIn.Sleep  5
             ...      AND  read until regexp  patterns=${boot_last_line}  timeout=30
    Step  9  Run Keywords  send key  KEY_RIGHT  1
             ...      AND  send key  KEY_UP  1
             ...      AND  BuiltIn.Sleep  5
             ...      AND  read until regexp  patterns=${boot_override_last_line}  timeout=30
    [Teardown]  exit bios setup


ALI_BIOS_TC_041_BIOS_REQUIREMENT_CHECK
    [Tags]  ALI_BIOS_TC_041_BIOS_REQUIREMENT_CHECK  migaloo  shamu
    Step  1  verify cpu hyper thread status  Enable
    Step  2  Run Keywords  send key  KEY_ESC  1
             ...      AND  BuiltIn.Sleep  3
             ...      AND  send key  KEY_DOWN  1
             ...      AND  send key  KEY_ENTER  1
             ...      AND  read until regexp  patterns=${advance_power_mgmt_last_line}  timeout=60
    Step  3  Run Keywords  send key  KEY_DOWN  3
             ...      AND  send key  KEY_ENTER  1
             ...      AND  BuiltIn.Sleep  3
    ${cpu_c_text}=  read until regexp  patterns=${cpu_cstate_last_line}  timeout=60
    Step  4  verify log with keywords  ${cpu_cstate_patterns}  ${cpu_c_text}
    Step  5  exit bios setup
    Step  6  execute command and verify exit code
    ...  console=${diagos_mode}
    ...  command=set "processor.max_cstate=0 intel_idle.max_cstate=0"
    ...  sec=30
    Step  7  execute command and verify with a pattern
    ...  console=${diagos_mode}
    ...  command=cat /sys/devices/system/cpu/cpuidle/current_driver
    ...  sec=30
    ...  pattern=^(?P<idle_driver>none)
    Step  8  execute command and verify exit code
    ...  console=${diagos_mode}
    ...  command=dmesg | grep idle
    ...  sec=30
    Step  9  verify log with keywords  ${cstate_sonic_patterns}  ${text}
    Step  10  execute command and verify with a pattern
    ...  console=${diagos_mode}
    ...  command=cat /sys/module/intel_idle/parameters/max_cstate
    ...  sec=30
    ...  pattern=^(?P<max_cstate>0)

    Step  11  enter bios setup
    Step  12  Run Keywords  send key  KEY_RIGHT  2
              ...      AND  BuiltIn.Sleep  3
              ...      AND  send key  KEY_DOWN  1
              ...      AND  send key  KEY_ENTER  1
              ...      AND  read until regexp  patterns=${advance_power_mgmt_last_line}  timeout=60
    Step  13  Run Keywords  send key  KEY_DOWN  2
              ...      AND  BuiltIn.Sleep  3
              ...      AND  send key  KEY_ENTER  1
    ${cpu_hwpm_text}=  read until regexp  patterns=${cpu_hwpm_last_line}  timeout=60
    Step  14  search for a pattern  ${cpu_hwpm_text}  ${cpu_hwpm_patterns}
    Step  15  Run Keywords  send key  KEY_ESC  1
              ...      AND  BuiltIn.Sleep  3
    ${eist_text}=  read until regexp  patterns=${advance_power_mgmt_last_line}  timeout=60
    Step  16  search for a pattern  ${eist_text}  ${eist_patterns}
    Step  17  exit bios setup

    Step  18  execute command and verify exit code
    ...  console=${diagos_mode}
    ...  command=cpupower frequency-info
    ...  sec=30
    Step  19  execute command and verify exit code
    ...  console=${diagos_mode}
    ...  command=cat /sys/devices/system/cpu/cpu0/cpufreq/scaling_driver
    ...  sec=30
    ...  exit_code_pattern=(?m)^(?P<exit_code>1)$

    Step  20  set eist p-states  Enable
    Step  21  Run Keywords  send key  KEY_DOWN  1
              ...      AND  send key  KEY_ENTER  1
              ...      AND  BuiltIn.Sleep  3
    ${cpu_pstate_text}=  read until regexp  patterns=${cpu_pstate_last_line}  timeout=60
    Step  22  search for a pattern  ${cpu_pstate_text}  ${cpu_pstate_patterns}
    Step  23  Run Keywords  send key  KEY_ESC  1
              ...      AND  send key  KEY_DOWN  3
              ...      AND  send key  KEY_ENTER  1
              ...      AND  BuiltIn.Sleep  3
    ${cpu_tstate_text}=  read until regexp  patterns=${cpu_tstate_last_line}  timeout=60
    Step  24  search for a pattern  ${cpu_tstate_text}  ${cpu_tstate_patterns}
    Step  25  Run Keywords  send key  KEY_ESC  2
              ...      AND  send key  KEY_DOWN  4
              ...      AND  send key  KEY_ENTER  1
              ...      AND  BuiltIn.Sleep  3
              ...      AND  read until regexp  patterns=${pch_config_last_line}  timeout=60
              ...      AND  send key  KEY_DOWN  1
              ...      AND  send key  KEY_ENTER  1
              ...      AND  BuiltIn.Sleep  3
    ${pcie_aspm_text}=  read until regexp  patterns=${pcie_aspm_last_line}  timeout=60
    Step  26  search for a pattern  ${pcie_aspm_text}  ${pcie_aspm_patterns}
    Step  27  save and exit bios setup
    Step  28  execute command and verify with a pattern
    ...  console=${diagos_mode}
    ...  command=cpupower frequency-info
    ...  sec=30
    ...  pattern=(?i)current CPU frequency: (?P<cpu_freq>\\\\d+.*Hz)
    Step  29  execute command and verify with a pattern
    ...  console=${diagos_mode}
    ...  command=cat /sys/devices/system/cpu/cpu0/cpufreq/scaling_driver
    ...  sec=30
    ...  pattern=^(?P<scaling_driver>acpi-cpufreq)
    [Teardown]  Run Keywords  recover sonic
                ...      AND  set eist p-states  Disable  need_save_and_exit=${TRUE}
                ...      AND  recover sonic

*** Keywords ***
Bios Connect Device
    Bios Connect

Bios Disconnect Device
    Bios Disconnect

