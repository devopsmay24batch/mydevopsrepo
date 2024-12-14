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
Resource        CommonKeywords.resource
Library         String

*** Keywords ***


send key char
    [Arguments]
    ...  ${text}
    ...  ${delay}=0.5
    ...  ${CR}=False
    @{characters}=  Split String To Characters  ${text}
    FOR  ${c}  IN  @{characters}
        send a line  ${c}  CR=${CR}
        BuiltIn.Sleep  ${delay}
    END


enter bios post and check bios info
    [Arguments]
    ...  ${console}=${diagos_mode}
    ...  ${version_pattern}=${bios_version_pattern}
    ${post_text}=  enter bios setup
    ...  prompt=${console}
    ...  post_list=${post_test_list}
    search for a pattern  ${post_text}  ${bios_vendor}
    search for a pattern  ${post_text}  ${bios_date_pattern}
    search for a pattern  ${post_text}  ${version_pattern}
    verify log with keywords
    ...  regex_list=${evaluation_keywords}
    ...  target_log=${post_text}
    ...  check_fail=True


enter bios setup and check bios info
    [Arguments]
    ...  ${version_pattern}=${bios_version_pattern}
    ${setup_text}=  read until regexp
    ...  patterns=${bios_info_last_line}
    ...  timeout=60
    search for a pattern  ${setup_text}  ${bios_info_vendor}
    search for a pattern  ${setup_text}  ${bios_info_date}
    search for a pattern  ${setup_text}  ${version_pattern}


read eeprom
    [Arguments]
    ...  ${eeprom_path}
    ...  ${option}=d
    ...  ${console}=${openbmc_mode}
    ...  ${pattern}=${eeprom_pattern}

    change dir  ${eeprom_path}  ${console}
    ${eeprom_dict}=  run eeprom tool  option=${option}  prompt=${console}  pattern=${pattern}
    [Return]  ${eeprom_dict}


check eeprom
    [Arguments]
    ...  ${eeprom_path}
    ...  ${expected_result}
    ...  ${option}=d
    ...  ${console}=${openbmc_mode}
    ...  ${pattern}=${eeprom_pattern}

    change dir  ${eeprom_path}  ${console}
    ${eeprom_dict}=  run eeprom tool  option=${option}  prompt=${console}  pattern=${pattern}
    compare input dict to parsed  ${eeprom_dict}  ${expected_result}  True


check tlv eeprom
    [Arguments]
    ...  ${eeprom_path}
    ...  ${expected_result}
    ...  ${cmd}=${tlv_eeprom_cmd}
    ...  ${console}=${diagos_mode}
    ...  ${pattern}=${eeprom_tlv_patterns}

    execute command and verify with unordered pattern list
    ...  console=${console}
    ...  path=${eeprom_path}
    ...  command=${cmd}
    ...  patterns=${pattern}
    ...  msg=Failed to dump TLV eeprom!
    set test variable  ${tlv_eeprom_dict}  ${matches}
    compare input dict to parsed  ${tlv_eeprom_dict}  ${expected_result}  True


read smbios and tlv and all eeproms
    ${smbios_eeprom}=  read eeprom  ${smbios_eeprom_path}  d  ${diagos_mode}  ${smbios_eeprom_pattern}
    execute command and verify with unordered pattern list
    ...  console=${diagos_mode}
    ...  path=${tlv_eeprom_path}
    ...  command=${tlv_eeprom_cmd}
    ...  patterns=${eeprom_tlv_patterns}
    ...  msg=Failed to dump TLV eeprom!
    ${bmc_eeprom}=  read eeprom  ${bmc_eeprom_path}
    ${sys_eeprom}=  read eeprom  ${sys_eeprom_path}
    ${come_eeprom}=  read eeprom  ${come_eeprom_path}
    ${switch_eeprom}=  read eeprom  ${switch_eeprom_path}

    set test variable  ${smbios_eeprom}
    set test variable  ${tlv_eeprom}  ${matches}
    set test variable  ${bmc_eeprom}
    set test variable  ${sys_eeprom}
    set test variable  ${come_eeprom}
    set test variable  ${switch_eeprom}


check smbios and tlv and all eeproms
    check eeprom  ${smbios_eeprom_path}  ${smbios_eeprom}  d  ${diagos_mode}  ${smbios_eeprom_pattern}
    check tlv eeprom  ${tlv_eeprom_path}  ${tlv_eeprom}  ${tlv_eeprom_cmd}
    check eeprom  ${bmc_eeprom_path}  ${bmc_eeprom}
    check eeprom  ${sys_eeprom_path}  ${sys_eeprom}
    check eeprom  ${come_eeprom_path}  ${come_eeprom}
    check eeprom  ${switch_eeprom_path}  ${switch_eeprom}


check and switch bios boot
    [Arguments]
    ...  ${bios_flash}=Master
    ...  ${console}=${openbmc_mode}
    execute command and verify exit code
    ...  console=${console}
    ...  command=source /usr/local/bin/openbmc-utils.sh
    ...  msg=Failed to source the shell file!
    ${status}  ${value}=  Run Keyword And Ignore Error  execute command and verify with a pattern
    ...  console=${console}
    ...  command=come_boot_info
    ...  sec=30
    ...  pattern=(?i)(?P<boot_switch>${bios_flash})
    ...  msg=If found, no need to switch bios.
    ...  is_check_exit_code=${FALSE}
    Run Keyword If  '${status}' == 'FAIL'
    ...  switch bios flash  ${bios_flash}


#### @WORKAROUND to recover openbmc network, because OpenBMC cannot get the IP by itself
check and flush eth0 interface
    [Arguments]
    ...  ${console}=${openbmc_mode}
    ${server_ip}=  get ip address from config  PC
    ${status}  ${value}=  Run Keyword And Ignore Error  execute command and verify with a pattern
    ...  console=${console}
    ...  command=ping ${server_ip} -c 5
    ...  pattern=(?i)(?P<ping_result>, 0% packet loss)
    ...  is_check_exit_code=${FALSE}
    Run Keyword If  '${status}' == 'FAIL'
    ...  Run Keywords  flush network interface  console=${console}  interface=eth0
    ...  AND  BuiltIn.Sleep  10


prepare image
    [Arguments]
    ...  ${localImageDir}
    ...  ${image}
    ...  ${console}=${openbmc_mode}
    ...  ${upgrade}=True
    ...  ${bmc_flash}=master
    switch bmc flash  ${bmc_flash}
    BuiltIn.Sleep  50
    create dir  ${localImageDir}  ${console}
    check and flush eth0 interface  ${console}  #### @WORKAROUND to recover openbmc network
    get dhcp ip address  DUT  eth0  ${console}
    BuiltIn.Sleep  10
    download image  DUT  ${image}  upgrade=${upgrade}


prepare file on usb device
    create dir  ${bios_local_image_path}  ${diagos_mode}
    get dhcp ip address  DUT  eth0  ${diagos_mode}
    download images  DUT  BIOS
    download image  DUT  AFU_TOOL
    execute command and verify with a pattern
    ...  console=${diagos_mode}
    ...  command=fdisk -l
    ...  pattern=\\/dev\\/sdb1
    ...  msg=Not found USB disk
    create dir  /mnt  ${diagos_mode}
    execute command and verify exit code
    ...  console=${diagos_mode}
    ...  command=mount /dev/sdb1 /mnt
    execute command and verify exit code
    ...  console=${diagos_mode}
    ...  command=cp ${bios_local_image_path}/${afu_new_image} /mnt
    execute command and verify exit code
    ...  console=${diagos_mode}
    ...  command=cp ${bios_local_image_path}/${bios_new_image} /mnt
    execute command and verify exit code
    ...  console=${diagos_mode}
    ...  command=cp ${bios_local_image_path}/${bios_old_image} /mnt
    execute command and verify exit code
    ...  console=${diagos_mode}
    ...  command=ls /mnt
    execute command and verify exit code
    ...  console=${diagos_mode}
    ...  command=umount /mnt


prepare ru on usb device
    [Arguments]
    ...  ${local_image_path}=${ru_local_image_path}
    ...  ${console}=${diagos_mode}
    create dir  ${local_image_path}  ${console}
    get dhcp ip address  DUT  eth0  ${console}
    download image  DUT  RU
    execute command and verify exit code
    ...  console=${diagos_mode}
    ...  command=unzip -o ${ru_new_image}
    ...  path=${local_image_path}
    execute command and verify with a pattern
    ...  console=${console}
    ...  command=fdisk -l
    ...  pattern=\\/dev\\/sdb1
    ...  msg=Not found USB disk
    create dir  /mnt  ${console}
    execute command and verify exit code
    ...  console=${console}
    ...  command=mount /dev/sdb1 /mnt
    execute command and verify exit code
    ...  console=${console}
    ...  command=cp -rf ${local_image_path}/${ru_dir_name}/ /mnt
    execute command and verify exit code
    ...  console=${console}
    ...  command=ls /mnt
    execute command and verify exit code
    ...  console=${console}
    ...  command=umount /mnt


update bios in bmc
    [Arguments]
    ...  ${bios_flash}
    ...  ${isUpgrade}
    ...  ${version_pattern}
    open prompt  console=${openbmc_mode}  sec=30
    online update fw  BIOS  ${bios_flash}  ${isUpgrade}
    switch bios flash  ${bios_flash}
    BuiltIn.Sleep  30
    execute command and verify with a pattern
    ...  console=${diagos_mode}
    ...  command=dmidecode -t 0 | grep -i version
    ...  pattern=${version_pattern}
    ...  msg=Failed to verify bios version!
    check smbios and tlv and all eeproms


update bios in uefi shell
    [Arguments]
    ...  ${bios_flash}
    ...  ${isUpgrade}
    ...  ${version_pattern}
    check and switch bios boot  bios_flash=${bios_flash}
    read smbios and tlv and all eeproms
    execute command and verify exit code
    ...  console=${diagos_mode}
    ...  command=dmidecode -t 0 | grep -i version
    update bios uefi mode  isUpgrade=${isUpgrade}
    enter bios post and check bios info  ${uefi_mode}  ${version_pattern}
    enter bios setup and check bios info  ${version_pattern}
    exit bios setup
    BuiltIn.Sleep  30
    execute command and verify with a pattern
    ...  console=${diagos_mode}
    ...  command=dmidecode -t 0 | grep -i version
    ...  pattern=${version_pattern}
    ...  msg=Failed to verify bios version!
    check smbios and tlv and all eeproms
    verify current boot flash  fw_type=BIOS  boot_flash=${bios_flash}


select boot override in bios setup
    [Arguments]
    ...  ${select_str}
    ...  ${expected_prompt}
    Run Keywords  send key  KEY_LEFT  1
    ...      AND  BuiltIn.Sleep  3
    ...      AND  send key  KEY_UP  1
    ...      AND  clean buffer
    ...      AND  send key  KEY_RIGHT  1
    ...      AND  send key  KEY_LEFT  1
    ...      AND  BuiltIn.Sleep  3
    ${boot_override_text}=  read until regexp
    ...  patterns=(UEFI:|ONIE:|SONiC).*v\\|
    ...  timeout=60
    select boot override  menu_text=${boot_override_text}  target_boot=${select_str}
    BuiltIn.Sleep  10
    open prompt  console=${expected_prompt}  sec=300
    Run Keyword If  '${expected_prompt}' == '${onie_mode}'
    ...  send a line   onie-stop


set cores enabled
    [Arguments]
    ...  ${cores_number}
    enter bios setup
    Run Keywords  send key  KEY_RIGHT  2
    ...      AND  BuiltIn.Sleep  3
    ...      AND  send key  KEY_ENTER  3
    ...      AND  BuiltIn.Sleep  3
    ${cores_text}=  read until regexp
    ...  patterns=${cores_en_patterns}
    ...  timeout=60
    send a line  ${cores_number}  CR=False
    BuiltIn.Sleep  3
    save and exit bios setup


verify processor info in bios post and setup
    ${post_text}=  enter bios setup
    ...  prompt=${diagos_mode}
    ...  post_list=${post_test_list}
    search for a pattern  ${post_text}  ${proc_type_pattern}
    search for a pattern  ${post_text}  ${proc_speed_pattern}
    Run Keywords  send key  KEY_RIGHT  2
    ...      AND  BuiltIn.Sleep  3
    ...      AND  send key  KEY_ENTER  1
    ...      AND  BuiltIn.Sleep  3
    ${proc_text}=  read until regexp
    ...  patterns=${proc_config_last_line}
    ...  timeout=60
    search for a pattern  ${proc_text}  ${proc_freq_pattern}
    search for a pattern  ${proc_text}  ${proc_l1_cache}
    search for a pattern  ${proc_text}  ${proc_l2_cache}
    search for a pattern  ${proc_text}  ${proc_l3_cache}
    search for a pattern  ${proc_text}  ${proc_0_ver_1}
    search for a pattern  ${proc_text}  ${proc_0_ver_2}
    exit bios setup


check cpu information and number of processors
    [Arguments]
    ...  ${cores_number}
    ...  ${console}=${diagos_mode}
    ...  ${cores_enable}=${TRUE}
    Run Keyword If  ${cores_enable} == ${TRUE}
    ...  set test variable  ${multi_core}  2
    ...  ELSE
    ...  set test variable  ${multi_core}  1
    ${total_cores}=  Evaluate  ${cores_number} * ${multi_core}
    execute command and set test variable
    ...  console=${console}
    ...  command=cat /proc/cpuinfo
    verify findall keywords
    ...  patterns=${proc_pattern}
    ...  target_log=${text}
    ...  expected_count=${total_cores}
    send a line  command=top
    BuiltIn.Sleep  3
    send a line  command=1  CR=False
    BuiltIn.Sleep  10
    ${top_text}=  read until regexp
    ...  patterns=${top_last_line}
    ...  timeout=30
    send a line  command=q  CR=False
    open prompt  console=${console}  sec=10
    verify findall keywords
    ...  patterns=${top_pattern}
    ...  target_log=${top_text}
    ...  expected_count=${total_cores}


check cpu information
    [Arguments]
    ...  ${cores_number}
    ...  ${console}=${diagos_mode}
    execute command and set test variable
    ...  console=${console}
    ...  command=cat /proc/cpuinfo
    verify findall keywords
    ...  patterns=${proc_pattern}
    ...  target_log=${text}
    ...  expected_count=${cores_number}


check cpu real frequency with power thermal utility
    prepare image  ${bdx_local_image_path}  BDX_DE_LINUX  ${diagos_mode}
    execute command and verify exit code
    ...  console=${diagos_mode}
    ...  command=unzip -o ${bdx_new_image}
    ...  path=${bdx_local_image_path}
    execute command and verify exit code
    ...  console=${diagos_mode}
    ...  command=cp BDX_DE_Linux_2.0 /root/. -rf
    execute command and verify exit code
    ...  console=${diagos_mode}
    ...  command=chmod 777 BroadwellPwrMon
    ...  path=/root/BDX_DE_Linux_2.0/
    execute command and verify exit code
    ...  console=${diagos_mode}
    ...  command=echo y | ./BroadwellPwrMon
    ...  exit_code_pattern=(?m)^(?P<exit_code>1)$


set cpu hyper thread
    [Arguments]  ${value}
    enter bios setup
    Run Keywords  send key  KEY_RIGHT  2
    ...      AND  BuiltIn.Sleep  3
    ...      AND  send key  KEY_ENTER  1
    ...      AND  BuiltIn.Sleep  3
    ...      AND  send key  KEY_DOWN  1
    ${proc_text}=  read until regexp
    ...  patterns=${proc_config_last_line}
    ...  timeout=60
    ${status}  ${value}=  Run Keyword And Ignore Error  search for a pattern
    ...  text=${proc_text}
    ...  pattern=(?i)Hyper-Threading.*(?P<hyper_thread>${value})
    Run Keyword If  '${status}' == 'PASS'
    ...  Log  cpu hyper thread already ${value}
    ...  ELSE
    ...  Run Keywords  send key  KEY_ENTER  1
    ...           AND  BuiltIn.Sleep  3
    ...           AND  send key  KEY_UP  1
    ...           AND  BuiltIn.Sleep  3
    ...           AND  send key  KEY_ENTER  1
    save and exit bios setup


verify cpu hyper thread status
    [Arguments]
    ...  ${status}
    ...  ${need_exit}=${FALSE}
    enter bios setup
    Run Keywords  send key  KEY_RIGHT  2
    ...      AND  BuiltIn.Sleep  3
    ...      AND  send key  KEY_ENTER  1
    ...      AND  BuiltIn.Sleep  3
    ...      AND  send key  KEY_DOWN  1
    ${proc_text}=  read until regexp
    ...  patterns=${proc_config_last_line}
    ...  timeout=60
    search for a pattern
    ...  text=${proc_text}
    ...  pattern=(?i)Hyper-Threading.*(?P<hyper_thread>${status})
    ...  msg=The status for "hyper thread" does not match
    Run Keyword If  ${need_exit} == ${TRUE}  exit bios setup


verify pci management port
    execute command and verify with a pattern
    ...  console=${diagos_mode}
    ...  command=lspci -s 03:00.0 -xxx
    ...  pattern=${pci_030_pattern}
    execute command and verify with a pattern
    ...  console=${diagos_mode}
    ...  command=lspci -s 03:00.1 -xxx
    ...  pattern=${pci_031_pattern}
    execute command and verify with a pattern
    ...  console=${diagos_mode}
    ...  command=lspci -s 04:00.0 -xxx
    ...  pattern=${pci_040_pattern}
    execute command and verify with a pattern
    ...  console=${diagos_mode}
    ...  command=lspci -s 04:00.1 -xxx
    ...  pattern=${pci_041_pattern}
    execute command and verify with a pattern
    ...  console=${diagos_mode}
    ...  command=lspci -s 05:00.0 -xxx
    ...  pattern=${pci_050_pattern}
    execute command and verify with a pattern
    ...  console=${diagos_mode}
    ...  command=lspci -s 08:00.0 -xxx
    ...  pattern=${pci_080_pattern}
    execute command and verify with a pattern
    ...  console=${diagos_mode}
    ...  command=lspci -s 09:00.0 -xxx
    ...  pattern=${pci_090_pattern}

verify management port info in bios setup
    Run Keywords  send key  KEY_RIGHT  1
             ...      AND  BuiltIn.Sleep  3
    ${mgmt_text}  read until regexp
    ...  patterns=${advance_last_line}
    ...  timeout=60
    Run Keywords  send key  KEY_UP  1
    ...      AND  send key  KEY_ENTER  1
    ...      AND  BuiltIn.Sleep  3
    ${i210_text}  read until regexp
    ...  patterns=${i210_last_line}
    ...  timeout=60
    verify log with keywords  ${i210_patterns}  ${i210_text}

    Run Keywords  send key  KEY_ESC  1
    ...      AND  send key  KEY_UP  1
    ...      AND  send key  KEY_ENTER  1
    ...      AND  BuiltIn.Sleep  3
    ${ethernet_text}  read until regexp
    ...  patterns=${ethernet_last_line}
    ...  timeout=60
    verify log with keywords  ${ethernet041_patterns}  ${ethernet_text}

    Run Keywords  send key  KEY_ESC  1
    ...      AND  send key  KEY_UP  1
    ...      AND  send key  KEY_ENTER  1
    ...      AND  BuiltIn.Sleep  3
    ${ethernet_text}  read until regexp
    ...  patterns=${ethernet_last_line}
    ...  timeout=60
    verify log with keywords  ${ethernet040_patterns}  ${ethernet_text}

    Run Keywords  send key  KEY_ESC  1
    ...      AND  send key  KEY_UP  1
    ...      AND  send key  KEY_ENTER  1
    ...      AND  BuiltIn.Sleep  3
    ${ethernet_text}  read until regexp
    ...  patterns=${ethernet_last_line}
    ...  timeout=60
    verify log with keywords  ${ethernet031_patterns}  ${ethernet_text}

    Run Keywords  send key  KEY_ESC  1
    ...      AND  send key  KEY_UP  1
    ...      AND  send key  KEY_ENTER  1
    ...      AND  BuiltIn.Sleep  3
    ${ethernet_text}  read until regexp
    ...  patterns=${ethernet_last_line}
    ...  timeout=60
    verify log with keywords  ${ethernet030_patterns}  ${ethernet_text}


enter bios boot selection
    [Arguments]
    ...  ${enter_key}=KEY_F7
    ...  ${console}=${diagos_mode}
    open prompt  console=${console}  sec=10
    send a line  command=reboot
    read until regexp
    ...  patterns=${BIOS_START_KEYWORD}
    ...  timeout=300
    read until regexp
    ...  patterns=${ENTER_BBS_KEYWORD}
    ...  timeout=180
    Run Keyword If  '${enter_key}' == 'KEY_F7'  send key  KEY_F7  1
    ...  ELSE
    ...  Run Keywords  send key  KEY_ESC  1  0.5  AND  send key  KEY_7  1
    ${bbs_text}=  read until regexp
    ...  patterns=${bbs_last_line}
    ...  timeout=60
    set test variable  ${bbs_text}


restore bios master
    open prompt  console=${openbmc_mode}  sec=300
    create dir  ${bios_local_image_path}  ${openbmc_mode}
    check and flush eth0 interface  #### @WORKAROUND to recover openbmc network
    get dhcp ip address  DUT  eth0  ${openbmc_mode}
    BuiltIn.Sleep  10
    download image  DUT  BIOS
    online update fw  BIOS  master  True
    switch bios flash  master


write and read smbios eeprom
    [Arguments]
    ...  ${eeprom_name}
    ...  ${eeprom_path}=${smbios_eeprom_path}
    ...  ${console}=${diagos_mode}
    change dir  ${eeprom_path}  ${console}
    write eeprom tool diag  ${eeprom_name}
    run eeprom tool
    ...  option=u
    ...  prompt=${console}
    run eeprom tool
    ...  option=d
    ...  expected_result=${eeprom_name}
    ...  prompt=${console}
    ...  pattern=${smbios_eeprom_pattern}
    power cycle to openbmc  timeout=600
    change dir  ${eeprom_path}  ${console}
    run eeprom tool
    ...  option=d
    ...  expected_result=${eeprom_name}
    ...  prompt=${console}
    ...  pattern=${smbios_eeprom_pattern}


restore smbios eeprom
    [Arguments]
    ...  ${store_dict}
    ...  ${eeprom_path}=${smbios_eeprom_path}
    ...  ${console}=${diagos_mode}
    change dir  ${eeprom_path}  ${console}
    write eeprom tool diag  SMBIOS_EEPROM_TEST  store_dict=${store_dict}
    run eeprom tool
    ...  option=u
    ...  prompt=${console}
    read eeprom
    ...  eeprom_path=${eeprom_path}
    ...  console=${console}
    ...  pattern=${smbios_eeprom_pattern}


set bios password
    [Arguments]
    ...  ${level}
    ...  ${password}
    ...  ${current_pass}=${EMPTY}
    enter bios setup  bios_password=${current_pass}
    send key  KEY_RIGHT  3
    BuiltIn.Sleep  5
    read until regexp  patterns=${security_last_line}  timeout=60
    Run Keyword If  '${level}' == 'administrator'  send key  KEY_ENTER  1
    ...  ELSE  Run Keywords  send key  KEY_DOWN  1  AND  send key  KEY_ENTER  1
    BuiltIn.Sleep  3
    read until regexp  patterns=${create_pass_pattern}  timeout=60
    send key char  ${password}
    send key  KEY_ENTER  1
    BuiltIn.Sleep  3
    read until regexp  patterns=${confirm_pass_pattern}  timeout=60
    send key char  ${password}
    send key  KEY_ENTER  1
    BuiltIn.Sleep  3
    save and exit bios setup


clear bios password
    [Arguments]
    ...  ${level}
    ...  ${current_pass}
    recover sonic
    enter bios setup  bios_password=${current_pass}
    BuiltIn.Sleep  2
    send key  KEY_RIGHT  3
    BuiltIn.Sleep  5
    read until regexp  patterns=${security_last_line}  timeout=60
    Run Keyword If  '${level}' == 'administrator'  send key  KEY_ENTER  1
    ...  ELSE  Run Keywords  send key  KEY_DOWN  1  AND  send key  KEY_ENTER  1
    BuiltIn.Sleep  3
    read until regexp  patterns=${current_pass_pattern}  timeout=60
    send key char  ${current_pass}
    send key  KEY_ENTER  1
    BuiltIn.Sleep  3
    read until regexp  patterns=${create_pass_pattern}  timeout=60
    send key  KEY_ENTER  1
    read until regexp  patterns=${clear_pass_pattern}  timeout=60
    send key  KEY_ENTER  1
    save and exit bios setup
    recover sonic

set eist p-states
    [Arguments]
    ...  ${value}
    ...  ${need_save_and_exit}=${FALSE}
    enter bios setup
    Run Keywords  send key  KEY_RIGHT  2
    ...      AND  BuiltIn.Sleep  3
    ...      AND  send key  KEY_DOWN  1
    ...      AND  send key  KEY_ENTER  1
    ${advance_power_text}  read until regexp  patterns=${advance_power_mgmt_last_line}  timeout=60
    ${status}  ${value}=  Run Keyword And Ignore Error  search for a pattern
    ...  text=${advance_power_text}
    ...  pattern=(?i)EIST \\(P-states\\).*(?P<eist_cstate>${value})
    Run Keyword If  '${status}' == 'PASS'
    ...  Log  EIST P-states already ${value}
    ...  ELSE
    ...  Run Keywords  send key  KEY_DOWN  1
    ...           AND  send key  KEY_ENTER  1
    ...           AND  BuiltIn.Sleep  3
    ...           AND  send key  KEY_UP  1
    ...           AND  BuiltIn.Sleep  3
    ...           AND  send key  KEY_ENTER  1
    ...           AND  BuiltIn.Sleep  3
    Run Keyword If  ${need_save_and_exit} == ${TRUE}  save and exit bios setup


enter sub menu 2
    Run Keywords  send key  KEY_ENTER  1
    ...      AND  BuiltIn.Sleep  3
    ...      AND  read until regexp  patterns=${sub_2a_last_line}  timeout=30
    Run Keywords  send key  KEY_ESC  1
    ...      AND  send key  KEY_DOWN  1
    ...      AND  send key  KEY_ENTER  1
    ...      AND  BuiltIn.Sleep  3
    ...      AND  read until regexp  patterns=${sub_2b_last_line}  timeout=30
    Run Keywords  send key  KEY_DOWN  1
    ...      AND  send key  KEY_ENTER  1
    ...      AND  BuiltIn.Sleep  3
    ...      AND  read until regexp  patterns=${sub_2b_1_last_line}  timeout=30
    Run Keywords  send key  KEY_ESC  1
    ...      AND  send key  KEY_DOWN  2
    ...      AND  send key  KEY_ENTER  1
    ...      AND  BuiltIn.Sleep  3
    ...      AND  read until regexp  patterns=${sub_2b_2_last_line}  timeout=30
    clean buffer
    Run Keywords  send key  KEY_ESC  2
    ...      AND  BuiltIn.Sleep  3
    ...      AND  send key  KEY_DOWN  1
    ...      AND  send key  KEY_ENTER  1
    ...      AND  BuiltIn.Sleep  3
    ...      AND  read until regexp  patterns=${sub_2c_last_line}  timeout=30
    Run Keywords  send key  KEY_ESC  1
    ...      AND  send key  KEY_DOWN  1
    ...      AND  send key  KEY_ENTER  1
    ...      AND  BuiltIn.Sleep  3
    ...      AND  read until regexp  patterns=${sub_2d_last_line}  timeout=30
    Run Keywords  send key  KEY_ESC  1
    ...      AND  send key  KEY_DOWN  1
    ...      AND  send key  KEY_ENTER  1
    ...      AND  BuiltIn.Sleep  3
    ...      AND  read until regexp  patterns=${sub_2e_last_line}  timeout=30
    Run Keywords  send key  KEY_ESC  1
    ...      AND  send key  KEY_DOWN  1
    ...      AND  send key  KEY_ENTER  1
    ...      AND  BuiltIn.Sleep  3
    ...      AND  read until regexp  patterns=${sub_2f_last_line}  timeout=30
    clean buffer
    Run Keywords  send key  KEY_ESC  1
    ...      AND  BuiltIn.Sleep  10
    ...      AND  send key  KEY_DOWN  1
    ...      AND  BuiltIn.Sleep  3
    ...      AND  clean buffer
    ...      AND  send key  KEY_ENTER  1
    ...      AND  BuiltIn.Sleep  5
    ...      AND  read until regexp  patterns=${ethernet_last_line}  timeout=30
    Run Keywords  send key  KEY_ESC  1
    ...      AND  BuiltIn.Sleep  10
    ...      AND  send key  KEY_DOWN  4
    ...      AND  BuiltIn.Sleep  3
    ...      AND  clean buffer
    ...      AND  send key  KEY_ENTER  1
    ...      AND  BuiltIn.Sleep  5
    ...      AND  read until regexp  patterns=${i210_last_line}  timeout=30
    clean buffer


enter sub menu 3
    Run Keywords  send key  KEY_ENTER  1
    ...      AND  BuiltIn.Sleep  5
    ...      AND  read until regexp  patterns=${sub_3a_last_line}  timeout=60
    Run Keywords  send key  KEY_ENTER  2
    ...      AND  BuiltIn.Sleep  3
    ...      AND  read until regexp  patterns=${sub_3a_1_last_line}  timeout=30
    Run Keywords  send key  KEY_ESC  3  delay=${4}
    ...      AND  BuiltIn.Sleep  3
    ...      AND  send key  KEY_DOWN  1
    ...      AND  send key  KEY_ENTER  1
    ...      AND  BuiltIn.Sleep  3
    ...      AND  read until regexp  patterns=${sub_3b_last_line}  timeout=30
    Run Keywords  send key  KEY_DOWN  2
    ...      AND  send key  KEY_ENTER  1
    ...      AND  BuiltIn.Sleep  3
    ...      AND  read until regexp  patterns=${sub_3b_2_last_line}  timeout=30
    clean buffer
    Run Keywords  send key  KEY_ESC  1
    ...      AND  send key  KEY_DOWN  1
    ...      AND  send key  KEY_ENTER  1
    ...      AND  BuiltIn.Sleep  3
    ...      AND  read until regexp  patterns=${sub_3b_3_last_line}  timeout=30
    Run Keywords  send key  KEY_ESC  1
    ...      AND  send key  KEY_DOWN  1
    ...      AND  send key  KEY_ENTER  1
    ...      AND  BuiltIn.Sleep  3
    ...      AND  read until regexp  patterns=${sub_3b_4_last_line}  timeout=30
    Run Keywords  send key  KEY_ESC  1
    ...      AND  send key  KEY_DOWN  1
    ...      AND  send key  KEY_ENTER  1
    ...      AND  BuiltIn.Sleep  3
    ...      AND  read until regexp  patterns=${sub_3b_5_last_line}  timeout=30
    Run Keywords  send key  KEY_ENTER  1
    ...      AND  BuiltIn.Sleep  3
    ...      AND  read until regexp  patterns=${sub_3b_5_1_last_line}  timeout=30
    Run Keywords  send key  KEY_ESC  1
    ...      AND  send key  KEY_DOWN  1
    ...      AND  send key  KEY_ENTER  1
    ...      AND  BuiltIn.Sleep  3
    ...      AND  read until regexp  patterns=${sub_3b_5_2_last_line}  timeout=30
    clean buffer
    Run Keywords  send key  KEY_ESC  2
    ...      AND  BuiltIn.Sleep  3
    ...      AND  send key  KEY_DOWN  1
    ...      AND  send key  KEY_ENTER  1
    ...      AND  BuiltIn.Sleep  3
    ...      AND  read until regexp  patterns=${sub_3b_6_last_line}  timeout=30
    Run Keywords  send key  KEY_ESC  2
    ...      AND  BuiltIn.Sleep  3
    ...      AND  send key  KEY_DOWN  1
    ...      AND  send key  KEY_ENTER  1
    ...      AND  BuiltIn.Sleep  3
    ...      AND  read until regexp  patterns=${sub_3c_last_line}  timeout=30
    Run Keywords  send key  KEY_ESC  1
    ...      AND  send key  KEY_DOWN  1
    ...      AND  send key  KEY_ENTER  1
    ...      AND  BuiltIn.Sleep  3
    ...      AND  read until regexp  patterns=${sub_3d_last_line}  timeout=30
    Run Keywords  send key  KEY_DOWN  7
    ...      AND  send key  KEY_ENTER  1
    ...      AND  BuiltIn.Sleep  3
    ...      AND  read until regexp  patterns=${sub_3d_1_last_line}  timeout=30
    clean buffer
    Run Keywords  send key  KEY_ESC  1
    ...      AND  send key  KEY_DOWN  1
    ...      AND  send key  KEY_ENTER  1
    ...      AND  BuiltIn.Sleep  3
    ...      AND  read until regexp  patterns=${sub_3d_2_last_line}  timeout=30
    Run Keywords  send key  KEY_ESC  1
    ...      AND  send key  KEY_DOWN  1
    ...      AND  send key  KEY_ENTER  1
    ...      AND  BuiltIn.Sleep  3
    ...      AND  read until regexp  patterns=${sub_3d_3_last_line}  timeout=30
    Run Keywords  send key  KEY_ESC  1
    ...      AND  send key  KEY_DOWN  1
    ...      AND  send key  KEY_ENTER  1
    ...      AND  BuiltIn.Sleep  3
    ...      AND  read until regexp  patterns=${sub_3d_4_last_line}  timeout=30
    Run Keywords  send key  KEY_ESC  2
    ...      AND  BuiltIn.Sleep  3
    ...      AND  send key  KEY_DOWN  1
    ...      AND  send key  KEY_ENTER  1
    ...      AND  BuiltIn.Sleep  3
    ...      AND  read until regexp  patterns=${sub_3e_last_line}  timeout=30
    Run Keywords  send key  KEY_DOWN  2
    ...      AND  send key  KEY_ENTER  1
    ...      AND  BuiltIn.Sleep  3
    ...      AND  read until regexp  patterns=${sub_3e_1_last_line}  timeout=30
    Run Keywords  send key  KEY_DOWN  2
    ...      AND  send key  KEY_ENTER  1
    ...      AND  BuiltIn.Sleep  3
    ...      AND  read until regexp  patterns=${sub_3e_1_1_last_line}  timeout=30
    Run Keywords  send key  KEY_ESC  2
    ...      AND  BuiltIn.Sleep  3
    ...      AND  send key  KEY_DOWN  1
    ...      AND  send key  KEY_ENTER  1
    ...      AND  BuiltIn.Sleep  3
    ...      AND  read until regexp  patterns=${sub_3e_2_last_line}  timeout=30
    clean buffer
    Run Keywords  send key  KEY_ESC  2
    ...      AND  BuiltIn.Sleep  3
    ...      AND  send key  KEY_DOWN  1
    ...      AND  send key  KEY_ENTER  1
    ...      AND  BuiltIn.Sleep  3
    ...      AND  read until regexp  patterns=${sub_3f_last_line}  timeout=30
    Run Keywords  send key  KEY_ENTER  1
    ...      AND  BuiltIn.Sleep  3
    ...      AND  read until regexp  patterns=${sub_3f_1_last_line}  timeout=30
    Run Keywords  send key  KEY_ESC  1
    ...      AND  send key  KEY_DOWN  1
    ...      AND  send key  KEY_ENTER  1
    ...      AND  BuiltIn.Sleep  3
    ...      AND  read until regexp  patterns=${sub_3f_2_last_line}  timeout=30
    Run Keywords  send key  KEY_DOWN  1
    ...      AND  send key  KEY_ENTER  1
    ...      AND  BuiltIn.Sleep  3
    ...      AND  read until regexp  patterns=${sub_3f_2_1_last_line}  timeout=30
    Run Keywords  send key  KEY_ESC  2
    ...      AND  BuiltIn.Sleep  3
    ...      AND  send key  KEY_DOWN  1
    ...      AND  send key  KEY_ENTER  1
    ...      AND  BuiltIn.Sleep  3
    ...      AND  read until regexp  patterns=${sub_3f_3_last_line}  timeout=30
    clean buffer
    Run Keywords  send key  KEY_ESC  2
    ...      AND  BuiltIn.Sleep  3
    ...      AND  send key  KEY_DOWN  1
    ...      AND  send key  KEY_ENTER  1
    ...      AND  BuiltIn.Sleep  3
    ...      AND  read until regexp  patterns=${sub_3g_last_line}  timeout=30
    Run Keywords  send key  KEY_ESC  1
    ...      AND  send key  KEY_DOWN  1
    ...      AND  send key  KEY_ENTER  1
    ...      AND  BuiltIn.Sleep  3
    ...      AND  read until regexp  patterns=${sub_3h_last_line}  timeout=30
    Run Keywords  send key  KEY_ESC  1
    ...      AND  send key  KEY_DOWN  1
    ...      AND  send key  KEY_ENTER  1
    ...      AND  BuiltIn.Sleep  3
    ...      AND  read until regexp  patterns=${sub_3i_last_line}  timeout=30
    Run Keywords  send key  KEY_DOWN  7
    ...      AND  send key  KEY_ENTER  1
    ...      AND  BuiltIn.Sleep  3
    ...      AND  read until regexp  patterns=${sub_3i_1_last_line}  timeout=30
    clean buffer
    Run Keywords  send key  KEY_ESC  1
    ...      AND  send key  KEY_DOWN  1
    ...      AND  send key  KEY_ENTER  1
    ...      AND  BuiltIn.Sleep  3
    ...      AND  read until regexp  patterns=${sub_3i_2_last_line}  timeout=30
    Run Keywords  send key  KEY_ESC  1
    ...      AND  send key  KEY_DOWN  1
    ...      AND  send key  KEY_ENTER  1
    ...      AND  BuiltIn.Sleep  3
    ...      AND  read until regexp  patterns=${sub_3i_3_last_line}  timeout=30
    Run Keywords  send key  KEY_ESC  1
    ...      AND  send key  KEY_DOWN  1
    ...      AND  send key  KEY_ENTER  1
    ...      AND  BuiltIn.Sleep  3
    ...      AND  read until regexp  patterns=${sub_3i_4_last_line}  timeout=30
    Run Keywords  send key  KEY_ESC  2
    ...      AND  BuiltIn.Sleep  3
    ...      AND  send key  KEY_DOWN  1
    ...      AND  send key  KEY_ENTER  1
    ...      AND  BuiltIn.Sleep  3
    ...      AND  read until regexp  patterns=${sub_3j_last_line}  timeout=30
    clean buffer


enter sub menu 4
    Run Keywords  send key  KEY_UP  1
    ...      AND  send key  KEY_ENTER  1
    ...      AND  BuiltIn.Sleep  3
    ...      AND  read until regexp  patterns=${sub_4b_last_line}  timeout=30
    Run Keywords  send key  KEY_DOWN  3
    ...      AND  send key  KEY_ENTER  1
    ...      AND  BuiltIn.Sleep  3
    ...      AND  read until regexp  patterns=${sub_4b_1_last_line}  timeout=30
    Run Keywords  send key  KEY_ESC  2
    ...      AND  BuiltIn.Sleep  3
    ...      AND  send key  KEY_UP  1
    ...      AND  send key  KEY_ENTER  1
    ...      AND  BuiltIn.Sleep  3
    ...      AND  read until regexp  patterns=${sub_4a_last_line}  timeout=30
    clean buffer

select IO space
    send key  KEY_UP  1  ${10}
    send key  KEY_F5  1  ${10}
    read until regexp
    ...  patterns=${select_space_pattern}
    ...  timeout=60
    send key  KEY_DOWN  3  ${3}
    send key  KEY_ENTER  1  ${5}
    send key char  0500
    send key  KEY_ENTER  1  ${10}
    read until regexp
    ...  patterns=${io_space_pattern}
    ...  timeout=60
    BuiltIn.Sleep  10

change data width to 32
    send key  KEY_F7  2  ${10}
    read until regexp
    ...  patterns=${ru_32_bit_last_line2}
    ...  timeout=60

exit ru.efi
    BuiltIn.Sleep  5
    #### change data width to 8
    send key  KEY_F7  1  ${10}

    #### exit RU.EFI
    send key  KEY_F10  1
    send key  KEY_ENTER  1
    open prompt  console=${uefi_mode}  sec=30


verify gpio target
    [Arguments]
    ...  ${gpio_target_list}
    ...  ${gpio_target_dict}
    ...  ${mult}=0

    ${gpio_text}=  read until regexp
    ...  patterns=${window_pattern}
    ...  timeout=60
    ${gpio_dict}=  parse gpio  ${gpio_text}  ${gpio_target_list}  ${mult}
    ${err_count}=  compare input dict to parsed  ${gpio_dict}  ${gpio_target_dict}  True
    Should Be Equal  ${err_count}  ${0}
    ...  msg=Mismatch value when verifying gpio target (err_count)


verify gpio IO
    [Arguments]
    ...  ${gpio_target_list}
    ...  ${gpio_target_io_dict}
    ...  ${mult}=0

    send key  KEY_RIGHT  1  ${10}
    ${gpio_io_text}=  read until regexp
    ...  patterns=${window_pattern}
    ...  timeout=60
    ${gpio_io_dict}=  parse gpio  ${gpio_io_text}  ${gpio_target_list}  ${mult}
    ${err_count}=  compare input dict to parsed  ${gpio_io_dict}  ${gpio_target_io_dict}  True
    Should Be Equal  ${err_count}  ${0}
    ...  msg=Mismatch value when verifying gpio I/O (err_count)


verify gpio value
    [Arguments]
    ...  ${gpio_target_list}
    ...  ${gpio_target_val_dict}
    ...  ${key_count}=${1}
    ...  ${mult}=0

    send key  KEY_RIGHT  ${key_count}  ${10}
    ${gpio_val_text}=  read until regexp
    ...  patterns=${window_pattern}
    ...  timeout=60
    ${gpio_val_dict}=  parse gpio  ${gpio_val_text}  ${gpio_target_list}  ${mult}
    ${err_count}=  compare input dict to parsed  ${gpio_val_dict}  ${gpio_target_val_dict}  True
    Should Be Equal  ${err_count}  ${0}
    ...  msg=Mismatch value when verifying gpio value (err_count)

