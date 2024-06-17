
*** settings ***
Variables         Const.py
Variables         KapokOnieVariable.py
Library           CommonLib.py
Library           KapokCommonLib.py
Library           KapokOnieLib.py

*** keywords ***

Check network connectivity and download ONIE file from TFTP server
    [Arguments]  ${MODE}
    execute_check_dict  DUT  ifconfig  mode=${MODE}
    ...  patterns_dict=${fail_dict}  timeout=5  is_negative_test=True
    ${ip} =  get ip address from config  PC
    exec_ping  DUT  ipAddress=${ip}  count=3  mode=${MODE}
    fetch File With Tftp  ${tftp_get_onie_file_cmd}  ONIE_Installer  ${MODE}

get The Current Onie Partition Erase and Install Onie
    [Arguments]  ${MODE}
    ${partition} =  get The Current Onie Partition And Erase  ${MODE}
    flashcp Install Onie  ${partition}  ${MODE}

Clear Onie File
    [Arguments]  ${MODE}
    clear Image File  ONIE_Installer  ${MODE}

Set Static IP And Check network connectivity
    config Static IP
    ${server_ip} =  get ip address from config  PC
    exec_ping  DUT  ipAddress=${server_ip}  count=3  mode=${ONIE_RESCUE_MODE}

Self Update Onie
    [Arguments]  ${version}
    Step  1  boot Into Onie Rescue Mode
    Step  2  config Static IP
    Step  3  onie Self Update  update=${version}
    Step  4  verify Onie And CPLD Version  version=${version}

Switch And Check Booting Onie Version
    [Arguments]  ${onie_mode}
    Step  1  boot Into Uboot
    Step  2  switch And Check Output  ${onie_mode}

Backup EEPROM TLV Value And Write Protect Value
    Step  1  boot Into Onie Rescue Mode
    Step  2  backup Syseeprom And Write Protect Value

Restore EEPROM TLV Value And Write Protect Value
    Step  1  boot Into Onie Rescue Mode
    Step  2  restore Syseeprom And Write Protect Value

Write TLV Value And Read To Check
    [Arguments]  ${TLV_VALUE}
    boot Into Onie Rescue Mode
    ${BackupValue} =  get Onie Tlv Value
    ${WriteProtectValue} =  enable Eeprom Write
    write Tlv Value To Eeprom  ${TLV_VALUE}
    power Cycle To Onie Rescue Mode
    check Tlv Value From Eeprom  ${TLV_VALUE}
    write Tlv Value To Eeprom  ${BackupValue}
    disable Eeprom Write  ${WriteProtectValue}

Check network connectivity
    [Arguments]  ${MODE}
    execute_check_dict  DUT  ${ifconfig_a_cmd}  mode=${MODE}
    ...  patterns_dict=${fail_dict}  timeout=5  is_negative_test=True
    ${ip} =  get ip address from config  PC
    exec_ping  DUT  ipAddress=${ip}  count=5  mode=${MODE}

Get Device IP And Ping
    ${ip} =  get Device Ip  eth0
    exec local ping  ${server_ipv4}  3  mode=None

test Format Disk With ext3/ext4
    [Arguments]  ${partition}
    format Disk  cmd=mkfs.ext3 ${partition}  umount_mnt=False
    format Disk  cmd=mkfs.ext4 ${partition}  umount_mnt=False

check Driver Information
    [Arguments]  ${MODE}  ${SAVE_LOG}
    Step  1  switch And Check Booting  ${MODE}  save_log=${SAVE_LOG}
    ...  pattern_dict=${DRIVER_INFO_IN_BOOTING_PATTERN}  negative_check=False
    Step  2  check Loaded Driver  ${MODE}
    Step  3  check Driver Version

fenghuangv2 check Driver Information
    [Arguments]  ${MODE}  ${SAVE_LOG}
    Step  1  switch And Check Booting  ${MODE}  save_log=${SAVE_LOG}
    ...  pattern_dict=${FENGHUANGV2_DRIVER_INFO_IN_BOOTING_PATTERN}  negative_check=False
    Step  2  fhv2 check Loaded Driver  ${MODE}
    Step  3  fhv2 check Driver Version

check Fpp Mode
    [Arguments]  ${PORT_MODE}
    Step  1  boot Into Uboot
    Step  2  set Onie Fpp Mode  ${PORT_MODE}
    Step  3  check Fpp Info  ${PORT_MODE}

restore Fpp Mode
    Step  1  boot Into Uboot
    Step  2  set Onie Fpp Mode  sfp_detect

update onie and check cpld version
    [Arguments]  ${imageType}
    Step  1  boot Into Onie Rescue Mode
    Step  2  onie update   ${imageType}
    Step  3  check onie all version  ${imageType}

restore onie image in uboot mode
    Step  1  set Uboot IP
    Step  2  install Onie Under Uboot
    Step  3  verify Onie Version


