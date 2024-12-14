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
# Script       : ses_keywords.robot                                                                                   #
# Date         : April 11, 2021                                                                                       #
# Author       : James Shi <jameshi@celestica.com>                                                                    #
# Description  : This script used as keywords in ses.robot                                                             #
#                                                                                                                     #
# Script Revision Details:                                                                                            #
#   Initial Draft for ses testing                                                                                      #
#######################################################################################################################

*** Settings ***
Variables         ses_variable.py
Library           whitebox_lib.py
Library           ses_lib.py
Library           OperatingSystem
Library           openbmc_lib.py
Library           ../bmc/bmc_lib.py
Resource          ses_keywords.robot
Resource          CommonResource.robot

*** Keywords ***
check esm mode status
    #Step  1  ESMAConnect  ${ESMA IP}  ${ESMA port}
    Step  1  OS Connect Device
    Step  2  verify esm mode cli command  DUT
    Step  3  OS Disconnect Device

check esm mode status ESMB
    #Step  1  ESMAConnect   ${ESMB IP}  ${ESMB port}
    Step  1  ConnectESMB
    Step  2  verify esm mode cli command  DUT
    Step  3  OS Disconnect Device

get dut variable
    ${DUT_ipv4_ip} =  get_deviceinfo_from_config  UUT  managementIP
    ${DUT_username} =  get_deviceinfo_from_config  UUT  rootUserName
    ${DUT_password} =  get_deviceinfo_from_config  UUT  rootPassword
    ${bmcip} =  get_deviceinfo_from_config  UUT  bmcIP
    ${bmcusername} =  get_deviceinfo_from_config  UUT  bmcUserName
    ${bmcpassword} =  get_deviceinfo_from_config  UUT  bmcPassword
    Set Environment Variable  DUT_ipv4_ip  ${DUT_ipv4_ip}
    Set Environment Variable  DUT_username  ${DUT_username}
    Set Environment Variable  DUT_password  ${DUT_password}
    Set Environment Variable  bmcip  ${bmcip}
    Set Environment Variable  bmcusername  ${bmcusername}
    Set Environment Variable  bmcpassword  ${bmcpassword}

check all supported diagnostic pages
    ${sg_device_1} =  get_devicename  %{DUT_username}  %{DUT_ipv4_ip}  %{DUT_password}  Zone1
   # ${sg_device_2} =  get_devicename  %{DUT_username}  %{DUT_ipv4_ip}  %{DUT_password}  Zone2
    Step  1  verify_ses_page_00h  %{DUT_username}  %{DUT_ipv4_ip}  %{DUT_password}  ${sg_device_1}


Create ses page gold file
    #${sg_device_1} =  get_devicename  %{DUT_username}  %{DUT_ipv4_ip}  %{DUT_password}  Zone1
    #${sg_device_2} =  get_devicename  %{DUT_username}  %{DUT_ipv4_ip}  %{DUT_password}  Zone2
    server Connect
    ${sg_device_1} =   get_primary_device
    Log  ${sg_device_1}
    ${sg_device_2} =   get_non_primary_device
    Log  ${sg_device_2}
    Server Disconnect   
    ${ses_fw_version} =  get_ses_fw_version_by_ses_page_01h  %{DUT_username}  %{DUT_ipv4_ip}  %{DUT_password}  ${sg_device_1}
    ${cpld_version_1} =  get_cpld_version_ses_page  %{DUT_username}  %{DUT_ipv4_ip}  %{DUT_password}  ${sg_device_1}  isUpgrade=True
    ${cpld_version_2} =  get_cpld_version_ses_page  %{DUT_username}  %{DUT_ipv4_ip}  %{DUT_password}  ${sg_device_1}  isUpgrade=False
    Step  1  create_gold_file  %{DUT_username}  %{DUT_ipv4_ip}  %{DUT_password}
          ...  sg_ses --page=0x01 ${sg_device_1}|grep -v '${ses_fw_version}'  ${ses_page_01h_gold_file}
    Step  2  create_gold_file  %{DUT_username}  %{DUT_ipv4_ip}  %{DUT_password}
          ...  sg_ses --page=0x01 ${sg_device_2}|grep -v '${ses_fw_version}'  ${ses_page_01h_gold_file_2}
    Step  3  create_gold_file  %{DUT_username}  %{DUT_ipv4_ip}  %{DUT_password}
          ...  sg_ses --page=0x02 ${sg_device_1}|grep -v '${ses_fw_version}'|grep -v rpm|grep -v Voltage:|grep -v amps|grep -v Temperature=|grep -v INFO  ${ses_page_02h_gold_file_1}
    Step  4  create_gold_file  %{DUT_username}  %{DUT_ipv4_ip}  %{DUT_password}
          ...  sg_ses --page=0x02 ${sg_device_2}|grep -v '${ses_fw_version}'|grep -v rpm|grep -v Voltage:|grep -v amps|grep -v Temperature=|grep -v INFO  ${ses_page_02h_gold_file_2}
    Step  5  create_gold_file  %{DUT_username}  %{DUT_ipv4_ip}  %{DUT_password}
          ...  sg_ses --page=0x04 ${sg_device_1}|grep -v '${ses_fw_version}'  ${ses_page_04h_gold_file}
    Step  6  create_gold_file  %{DUT_username}  %{DUT_ipv4_ip}  %{DUT_password}
          ...  sg_ses --page=0x05 ${sg_device_1}|grep -v '${ses_fw_version}'  ${ses_page_05h_gold_file}
    Step  7  create_gold_file  %{DUT_username}  %{DUT_ipv4_ip}  %{DUT_password}
          ...  sg_ses --page=0x07 ${sg_device_1}|grep -v '${ses_fw_version}'|grep -v Secondary|grep -v Primary|grep -v ${cpld_version_1}|grep -v ${cpld_version_2}   ${ses_page_07h_gold_file}
    Step  8  create_gold_file  %{DUT_username}  %{DUT_ipv4_ip}  %{DUT_password}
          ...  sg_ses --page=0x0a ${sg_device_1}|grep -v '${ses_fw_version}'  ${ses_page_a_gold_file_1}
    Step  9  create_gold_file  %{DUT_username}  %{DUT_ipv4_ip}  %{DUT_password}
          ...  sg_ses --page=0x0a ${sg_device_2}|grep -v '${ses_fw_version}'  ${ses_page_a_gold_file_2}
    Step  10  create_gold_file  %{DUT_username}  %{DUT_ipv4_ip}  %{DUT_password}
          ...  sg_ses --page=0x0e ${sg_device_1}|grep -v '${ses_fw_version}'|grep -v offset  ${ses_page_e_gold_file}

Compare ses page gold file
    #${sg_device_1} =  get_devicename  %{DUT_username}  %{DUT_ipv4_ip}  %{DUT_password}  Zone1
    #${sg_device_2} =  get_devicename  %{DUT_username}  %{DUT_ipv4_ip}  %{DUT_password}  Zone2
    server Connect
    ${sg_device_1} =   get_primary_device
    Log  ${sg_device_1}
    ${sg_device_2} =   get_non_primary_device
    Log  ${sg_device_2}
    Server Disconnect    
    ${ses_fw_version} =  get_ses_fw_version_by_ses_page_01h  %{DUT_username}  %{DUT_ipv4_ip}  %{DUT_password}  ${sg_device_1}
    ${cpld_version_1} =  get_cpld_version_ses_page  %{DUT_username}  %{DUT_ipv4_ip}  %{DUT_password}  ${sg_device_1}  isUpgrade=True
    ${cpld_version_2} =  get_cpld_version_ses_page  %{DUT_username}  %{DUT_ipv4_ip}  %{DUT_password}  ${sg_device_1}  isUpgrade=False
    Sleep  90
    Step  1  create_gold_file  %{DUT_username}  %{DUT_ipv4_ip}  %{DUT_password}
          ...  sg_ses --page=0x01 ${sg_device_1}|grep -v '${ses_fw_version}'  ${ses_page_tmp_file}
    Step  2  compare_file  ${ses_page_01h_gold_file}  ${ses_page_tmp_file}  ses_page_01h
    Sleep  60
    Step  3  create_gold_file  %{DUT_username}  %{DUT_ipv4_ip}  %{DUT_password}
          ...  sg_ses --page=0x01 ${sg_device_2}|grep -v '${ses_fw_version}'  ${ses_page_tmp_file}
    Step  4  compare_file  ${ses_page_01h_gold_file_2}  ${ses_page_tmp_file}  ses_page_01h
    Sleep  60
    Step  5  create_gold_file  %{DUT_username}  %{DUT_ipv4_ip}  %{DUT_password}
          ...  sg_ses --page=0x02 ${sg_device_1}|grep -v '${ses_fw_version}'|grep -v rpm|grep -v Voltage:|grep -v amps|grep -v Temperature=|grep -v INFO  ${ses_page_tmp_file}
    Step  6  compare_file  ${ses_page_02h_gold_file_1}  ${ses_page_tmp_file}  ses_page_02h_1
    Sleep  120
    Step  7  create_gold_file  %{DUT_username}  %{DUT_ipv4_ip}  %{DUT_password}
          ...  sg_ses --page=0x02 ${sg_device_2}|grep -v '${ses_fw_version}'|grep -v rpm|grep -v Voltage:|grep -v amps|grep -v Temperature=|grep -v INFO  ${ses_page_tmp_file}
    Step  8  compare_file  ${ses_page_02h_gold_file_2}  ${ses_page_tmp_file}  ses_page_02h_2
#    Step  7  create_gold_file  %{DUT_username}  %{DUT_ipv4_ip}  %{DUT_password}
#         ...  sg_ses --page=0x04 ${sg_device_1}|grep -v '${ses_fw_version}'  ${ses_page_tmp_file}
#    Step  8  compare_file  ${ses_page_04h_gold_file}  ${ses_page_tmp_file}  ses_page_04h
    Sleep  60
    Step  9  create_gold_file  %{DUT_username}  %{DUT_ipv4_ip}  %{DUT_password}
          ...  sg_ses --page=0x05 ${sg_device_1}|grep -v '${ses_fw_version}'  ${ses_page_tmp_file}
    Step  10  compare_file  ${ses_page_05h_gold_file}  ${ses_page_tmp_file}  ses_page_05h
    Sleep  60
    Step  11  create_gold_file  %{DUT_username}  %{DUT_ipv4_ip}  %{DUT_password}
          ...  sg_ses --page=0x07 ${sg_device_1}|grep -v '${ses_fw_version}'|grep -v Secondary|grep -v Primary|grep -v ${cpld_version_1}|grep -v ${cpld_version_2}  ${ses_page_tmp_file}
    Step  12  compare_file  ${ses_page_07h_gold_file}  ${ses_page_tmp_file}  ses_page_07h
    Sleep  60
    Step  13  create_gold_file  %{DUT_username}  %{DUT_ipv4_ip}  %{DUT_password}
          ...  sg_ses --page=0x0a ${sg_device_1}|grep -v '${ses_fw_version}'  ${ses_page_tmp_file}
    Step  14  compare_file  ${ses_page_a_gold_file_1}  ${ses_page_tmp_file}  ses_page_a_1
    Sleep  60
    Step  15  create_gold_file  %{DUT_username}  %{DUT_ipv4_ip}  %{DUT_password}
          ...  sg_ses --page=0x0a ${sg_device_2}|grep -v '${ses_fw_version}'  ${ses_page_tmp_file}
    Step  16  compare_file  ${ses_page_a_gold_file_2}  ${ses_page_tmp_file}  ses_page_a_2
    Sleep  60
    Step  17  create_gold_file  %{DUT_username}  %{DUT_ipv4_ip}  %{DUT_password}
          ...  sg_ses --page=0x0e ${sg_device_1}|grep -v '${ses_fw_version}'|grep -v offset  ${ses_page_tmp_file}
    Step  18  compare_file  ${ses_page_e_gold_file}  ${ses_page_tmp_file}  ses_page_e

Configuration Diagnostic Pages(01h)
    ${sg_device_1} =  get_devicename  %{DUT_username}  %{DUT_ipv4_ip}  %{DUT_password}  Zone1
   # ${sg_device_2} =  get_devicename  %{DUT_username}  %{DUT_ipv4_ip}  %{DUT_password}  Zone2
    ${ses_fw_version} =  get_ses_fw_version_by_ses_page_01h  %{DUT_username}  %{DUT_ipv4_ip}  %{DUT_password}  ${sg_device_1}
    Step  1  verify_ses_page_01h_info  %{DUT_username}  %{DUT_ipv4_ip}  %{DUT_password}  ${sg_device_1}  ${ses_page_01h_info}
   # Step  2  verify_ses_page_01h_info  %{DUT_username}  %{DUT_ipv4_ip}  %{DUT_password}  ${sg_device_2}  ${ses_page_01h_info}
#    Sleep  60
#    Step  3  create_gold_file  %{DUT_username}  %{DUT_ipv4_ip}  %{DUT_password}
#          ...  sg_ses --page=0x01 ${sg_device_1} |grep -v '${ses_fw_version}'  ${ses_page_tmp_file}
#    Step  4  compare_file  ${ses_page_01h_gold_file}  ${ses_page_tmp_file}
    #Step  5  create_gold_file  %{DUT_username}  %{DUT_ipv4_ip}  %{DUT_password}
    #      ...  sg_ses --page=0x01 ${sg_device_2} |grep -v '${ses_fw_version}'  ${ses_page_tmp_file}
    #Sleep  60
    #Step  6  compare_file  ${ses_page_01h_gold_file_2}  ${ses_page_tmp_file}

Enclosure Status Diagnostic Pages(02h)
    ${sg_device_1} =  get_devicename  %{DUT_username}  %{DUT_ipv4_ip}  %{DUT_password}  Zone1
    #${sg_device_2} =  get_devicename  %{DUT_username}  %{DUT_ipv4_ip}  %{DUT_password}  Zone2
    ${ses_fw_version} =  get_ses_fw_version_by_ses_page_01h  %{DUT_username}  %{DUT_ipv4_ip}  %{DUT_password}  ${sg_device_1}
    Step  1  create_gold_file  %{DUT_username}  %{DUT_ipv4_ip}  %{DUT_password}
          ...  sg_ses --page=0x02 ${sg_device_1}|grep -v '${ses_fw_version}'|grep -v rpm|grep -v Voltage:|grep -v amps|grep -v Temperature=|grep -v INFO  ${ses_page_02h_gold_file_1}
    Step  3  create_gold_file  %{DUT_username}  %{DUT_ipv4_ip}  %{DUT_password}
          ...  sg_ses --page=0x02 ${sg_device_1}|grep -v rpm|grep -v Voltage:|grep -v amps|grep -v Temperature=|grep -v INFO|grep -v '${ses_fw_version}'  ${ses_page_tmp_file}
    Step  4  compare_file  ${ses_page_02h_gold_file_1}  ${ses_page_tmp_file}
    #Step  5  create_gold_file  %{DUT_username}  %{DUT_ipv4_ip}  %{DUT_password}
     #     ...  sg_ses --page=0x02 ${sg_device_2}|grep -v rpm|grep -v Voltage:|grep -v amps|grep -v Temperature=|grep -v INFO|grep -v '${ses_fw_version}'  ${ses_page_tmp_file}
           #Step  2  create_gold_file  %{DUT_username}  %{DUT_ipv4_ip}  %{DUT_password}
          #...  sg_ses --page=0x02 ${sg_device_2}|grep -v '${ses_fw_version}'|grep -v rpm|grep -v Voltage:|grep -v amps|grep -v Temperature=|grep -v INFO  ${ses_page_02h_gold_file_2} 
   #Step  6  compare_file  ${ses_page_02h_gold_file_2}  ${ses_page_tmp_file}

set control bits via raw data
    ${sg_device_1} =  get_devicename  %{DUT_username}  %{DUT_ipv4_ip}  %{DUT_password}  Zone1
    Step  1  ssh_command_set_ses_page_command  %{DUT_username}  %{DUT_ipv4_ip}  %{DUT_password}
          ...  sg_ses --page=0x02 --index=_24,0 --set=1:1:1=0 --byte1=0x0f ${sg_device_1}
    Step  2  verify_page_02h_control_bits_via_raw_data  %{DUT_username}  %{DUT_ipv4_ip}  %{DUT_password}  ${sg_device_1}  1
    Step  3  ssh_command_set_ses_page_command  %{DUT_username}  %{DUT_ipv4_ip}  %{DUT_password}
          ...  sg_ses --page=0x02 --index=_24,0 --set=1:1:1=0 --byte1=0x00 ${sg_device_1}
    Step  4  verify_page_02h_control_bits_via_raw_data  %{DUT_username}  %{DUT_ipv4_ip}  %{DUT_password}  ${sg_device_1}  0

check 'Info' bit
    ${sg_device_1} =  get_devicename  %{DUT_username}  %{DUT_ipv4_ip}  %{DUT_password}  Zone1
    Step  1  ssh_command_set_ses_page_command  %{DUT_username}  %{DUT_ipv4_ip}  %{DUT_password}
          ...  sg_ses -p 2 -I enc,0 --set=3:1:1=1 ${sg_device_1}
    Step  2  set time delay  10
    Step  3  ssh_command_set_ses_page_command  %{DUT_username}  %{DUT_ipv4_ip}  %{DUT_password}
          ...  sg_ses -p 2 -I enc,0 --set=3:1:1=0 ${sg_device_1}
    Step  4  set time delay  10
    Step  5  verify_ses_page_02h_info_bit  %{DUT_username}  %{DUT_ipv4_ip}  %{DUT_password}  ${sg_device_1}  1
    Step  6  ssh_command_set_ses_page_command  %{DUT_username}  %{DUT_ipv4_ip}  %{DUT_password}
          ...  sg_ses --page=0x02 --index=_24,0 --set=1:1:1=0 --byte1=0x00 ${sg_device_1}
    Step  7  set time delay  5
    Step  8  verify_ses_page_02h_info_bit  %{DUT_username}  %{DUT_ipv4_ip}  %{DUT_password}  ${sg_device_1}  0

check Cooling external Mode
    ${sg_device_1} =  get_devicename  %{DUT_username}  %{DUT_ipv4_ip}  %{DUT_password}  Zone1
    Step  1  verify_ses_page_02_cooling_Mode  %{DUT_username}  %{DUT_ipv4_ip}  %{DUT_password}  ${sg_device_1}  external
    Step  2  OS Connect Device
    Step  3  verify_esm_fan_mode_cli_command  DUT  external
    Step  4  OS Disconnect Device

check Cooling external Mode ESMB
    ${sg_device_1} =  get_devicename  %{DUT_username}  %{DUT_ipv4_ip}  %{DUT_password}  Zone1
    Step  1  verify_ses_page_02_cooling_Mode  %{DUT_username}  %{DUT_ipv4_ip}  %{DUT_password}  ${sg_device_1}  external
    Step  2  ConnectESMB
    Step  3  verify_esm_fan_mode_cli_command  DUT  external
    Step  4  OS Disconnect Device

check Cooling internal Mode
    ${sg_device_1} =  get_devicename  %{DUT_username}  %{DUT_ipv4_ip}  %{DUT_password}  Zone1
    Step  1  verify_ses_page_02_cooling_Mode  %{DUT_username}  %{DUT_ipv4_ip}  %{DUT_password}  ${sg_device_1}  internal
    Step  2  OS Connect Device
    Step  3  verify_esm_fan_mode_cli_command  DUT  internal
    Step  4  OS Disconnect Device

check Cooling internal Mode ESMB
    ${sg_device_1} =  get_devicename  %{DUT_username}  %{DUT_ipv4_ip}  %{DUT_password}  Zone1
    Step  1  verify_ses_page_02_cooling_Mode  %{DUT_username}  %{DUT_ipv4_ip}  %{DUT_password}  ${sg_device_1}  internal
    Step  2  ConnectESMB
    Step  3  verify_esm_fan_mode_cli_command  DUT  internal
    Step  4  OS Disconnect Device

check Fan current speed
    ${sg_device_1} =  get_devicename  %{DUT_username}  %{DUT_ipv4_ip}  %{DUT_password}  Zone1
    Step  1  verify_ses_page_02_fan_current_speed  %{DUT_username}  %{DUT_ipv4_ip}  %{DUT_password}  ${sg_device_1}  ${fan_speed_1}
    Step  2  ESMAConnect  ${ESMA IP}  ${ESMA port}
    Step  3  verify_fan_speed_cli_command  DUT  ${fan_speed_cli_1}
    Step  4  verify_esm_fan_mode_cli_command  DUT  external
    Step  5  Disconnect
    Step  6  verify_ses_page_02_fan_current_speed  %{DUT_username}  %{DUT_ipv4_ip}  %{DUT_password}  ${sg_device_1}  ${fan_speed_2}
    Step  7  ESMAConnect  ${ESMA IP}  ${ESMA port}
    Step  8  verify_fan_speed_cli_command  DUT  ${fan_speed_cli_2}
    Step  9  verify_esm_fan_mode_cli_command  DUT  external
    Step  10  Disconnect
    Step  11  set_ses_page_02_fan_speed  %{DUT_username}  %{DUT_ipv4_ip}  %{DUT_password}  ${sg_device_1}  8
    Step  12  get_ses_page_02_fan_speed  %{DUT_username}  %{DUT_ipv4_ip}  %{DUT_password}  ${sg_device_1}  ${fan_speed_2}
    Step  13  ESMAConnect  ${ESMA IP}  ${ESMA port}
    Step  14  verify_fan_speed_cli_command  DUT  ${fan_speed_cli_2}
    Step  15  verify_esm_fan_mode_cli_command  DUT  external
    Step  16  Disconnect

check Fan current speed ESMB
    ${sg_device_1} =  get_devicename  %{DUT_username}  %{DUT_ipv4_ip_ESMB}  %{DUT_password}  Zone1
    Step  1  verify_ses_page_02_fan_current_speed  %{DUT_username}  %{DUT_ipv4_ip}  %{DUT_password}  ${sg_device_1}  ${fan_speed_1}
    Step  2  ESMAConnect  ${ESMB IP}  ${ESMB port}
    Step  3  verify_fan_speed_cli_command  DUT  ${fan_speed_cli_1}
    Step  4  verify_esm_fan_mode_cli_command  DUT  external
    Step  5  Disconnect
    Step  6  verify_ses_page_02_fan_current_speed  %{DUT_username}  %{DUT_ipv4_ip}  %{DUT_password}  ${sg_device_1}  ${fan_speed_2}
    Step  7  ESMAConnect  ${ESMB IP}  ${ESMB port}
    Step  8  verify_fan_speed_cli_command  DUT  ${fan_speed_cli_2}
    Step  9  verify_esm_fan_mode_cli_command  DUT  external
    Step  10  Disconnect
    Step  11  set_ses_page_02_fan_speed  %{DUT_username}  %{DUT_ipv4_ip}  %{DUT_password}  ${sg_device_1}  8
    Step  12  get_ses_page_02_fan_speed  %{DUT_username}  %{DUT_ipv4_ip}  %{DUT_password}  ${sg_device_1}  ${fan_speed_2}
    Step  13  ESMAConnect  ${ESMB IP}  ${ESMB port}
    Step  14  verify_fan_speed_cli_command  DUT  ${fan_speed_cli_2}
    Step  15  verify_esm_fan_mode_cli_command  DUT  external
    Step  16  Disconnect

Keyword Retry
    [Arguments]    ${keyword}    @{args}    &{config}
    ${result}=    Wait Until Keyword Succeeds    ${G Retry Count}    10s    ${keyword}    @{args}    &{config}
    [Return]    ${result}

check Temperature Alarm
    [Arguments]    ${alarm_level}
    ${HDDs}=  query SG Devices
    Log  ${HDDs}
    ${SENSORS}=  list Temperature Sensor  ${HDDs}[0]
    ${TEMPER_VALUE}=  get Sensor Temperature  ${SENSORS}[0]  ${HDDs}[0]
    ${THRESHOLDs}=  getTemperThreshold  ${SENSORS}[0]  ${HDDs}[0]
    set Test Variable  ${HDD}  ${HDDs}[0]
    set Test Variable  ${SENSOR}  ${SENSORS}[0]
    set Test Variable  ${THRESHOLDs}  ${THRESHOLDs}
    set Temper Threshold  ${SENSORS}[0]  ${HDDs}[0]  ${TEMPER_VALUE}  ${alarm_level}
    Log  ${HDD}
    getTemperThreshold  ${SENSORS}[0]  ${HDDs}[0]
    check Alarm Bit  ${SENSORS}[0]  ${HDDs}[0]  ${alarm_level}

restore Temperature Threshold
    [Arguments]    ${alarm_level}
    set Back Threshold  ${SENSOR}  ${HDD}  ${THRESHOLDs}  ${alarm_level}
    check Alarm Normal  ${SENSOR}  ${HDD}  ${alarm_level}
    clear Alarm Bit  ${HDD}  ${alarm_level}

check Temperature Alarm On Page5
    [Arguments]    ${alarm_level}
    ${HDDs}=  query SG Devices
    ${SENSORS}=  list Temperature Sensor  ${HDDs}[0]
    ${TEMPER_VALUE}=  get Sensor Temperature  ${SENSORS}[0]  ${HDDs}[0]
    ${THRESHOLDs}=  getTemperThreshold  ${SENSORS}[0]  ${HDDs}[0]
    set Test Variable  ${HDD}  ${HDDs}[0]
    set Test Variable  ${SENSOR}  ${SENSORS}[0]
    set Test Variable  ${THRESHOLDs}  ${THRESHOLDs}
    ${setting_value}=  set Temper Threshold  ${SENSORS}[0]  ${HDDs}[0]  ${TEMPER_VALUE}  ${alarm_level}
    check Sensor Value On Page5  ${SENSORS}[0]  ${HDDs}[0]  ${alarm_level}
    ...  ${setting_value}
    getTemperThreshold  ${SENSORS}[0]  ${HDDs}[0]
    check Alarm Bit  ${SENSORS}[0]  ${HDDs}[0]  ${alarm_level}

restore Temperature Threshold on Page5
    [Arguments]    ${alarm_level}
    ${setting_value}=  set Back Threshold  ${SENSOR}  ${HDD}  ${THRESHOLDs}  ${alarm_level}
    check Sensor Value On Page5  ${SENSOR}  ${HDD}  ${alarm_level}
    ...  ${setting_value}
    check Alarm Normal  ${SENSOR}  ${HDD}  ${alarm_level}

check Sensor Alarm On Page5
    [Arguments]    ${alarm_level}  ${sensor_type}
    ${HDDs}=  query SG Devices
    ${SENSORS}=  list Sensors  ${sensor_type}  ${HDDs}[0]
    ${THRESHOLDs}=  get Sensor Threshold  ${SENSORS}[0][0]  ${HDDs}[0]  ${sensor_type}
    ${setting_value}=  set Voltage Threshold  ${SENSORS}[0][0]  ${HDDs}[0]  ${THRESHOLDs}  ${alarm_level}
    check Sensor Value On Page5  ${SENSORS}[0][0]  ${HDDs}[0]  ${alarm_level}
    ...  ${setting_value}  ${sensor_type}
    set Test Variable  ${HDD}  ${HDDs}[0]
    set Test Variable  ${SENSOR}  ${SENSORS}[0][0]
    set Test Variable  ${THRESHOLDs}  ${THRESHOLDs}

restore Threshold on Page5
    [Arguments]    ${alarm_level}  ${sensor_type}
    ${setting_value}=  set Back Threshold  ${SENSOR}  ${HDD}  ${THRESHOLDs}
    ...  ${alarm_level}  ${sensor_type}
    check Sensor Value On Page5  ${SENSOR}  ${HDD}  ${alarm_level}
    ...  ${setting_value}  ${sensor_type}

power on/off JBOD via ses command to check info
    Step  1  check info
    Step  2  power_on_off_JBOD_via_ses_command  %{DUT_username}  %{DUT_ipv4_ip}  %{DUT_password}  %{sg_device_1}
    Step  3  set time delay  120
    Step  4  check info

ac cycle JBOD to check info
    ###1(server)|2(JBOD)|3(ALL)
    ${sg_device_1} =  get_devicename  %{DUT_username}  %{DUT_ipv4_ip}  %{DUT_password}  Zone1
    Step  1  powercycle_pdu2  DUT
    Step  2  set time delay  60
    Step  3  check_disk_number_via_ses_cmd  %{DUT_username}  %{DUT_ipv4_ip}  %{DUT_password}  ${cmd_check_disk_num}  0  ${not_test_hdd}  off
    Step  4  set time delay  200
    Step  5  check info
    Step  6  Compare ses page gold file

ac cycle server to check info
    ###1(server)|2(JBOD)|3(ALL)
    Step  1  whitebox_lib.Powercycle Pdu1  DUT
    Step  2  set time delay  360
    Step  3  check info
    Step  4  Compare ses page gold file

ac cycle JBOD + server to check info
    Step  1  powercycle_pdu3  DUT
    Step  2  set time delay  360
    Step  3  check info
    Step  4  Compare ses page gold file

reload expander to check info
    Step  1  reload expander driver
    Step  2  check info

reload expander driver
    Step  1  ssh_login_OS  DUT  %{DUT_ipv4_ip}  %{DUT_username}  %{DUT_password}
    Step  2  verify_ipmi_set_cmd  SSH_DUT  cd /root/mpt3sas/
    Step  3  verify_ipmi_set_cmd  SSH_DUT  ./uload.sh
    Step  4  set time delay  1
    Step  5  verify_ipmi_set_cmd  SSH_DUT  ./load.sh
    Step  6  CommonLib.ssh_disconnect  DUT
    Step  7  set time delay  60

dc cycle server to check info
    Step  1  dc_cycle_server
    Step  2  set time delay  360
    Step  3  check info
    Step  4  Compare ses page gold file

dc cycle server + power on/off JBOD via ses command to check info
    Step  1  power_on_off_JBOD_via_ses_command  %{DUT_username}  %{DUT_ipv4_ip}  %{DUT_password}  %{sg_device_1}
    Step  2  dc_cycle_server
    Step  3  set time delay  300
    Step  4  check info
    Step  5  Compare ses page gold file

dc JBOD via ses command to check info
    ${sg_device_1} =  get_devicename  %{DUT_username}  %{DUT_ipv4_ip}  %{DUT_password}  Zone1
    Step  1  power_cycle_JBOD_via_ses_command  %{DUT_username}  %{DUT_ipv4_ip}  %{DUT_password}  ${sg_device_1}
    Step  2  set time delay  120
    Step  3  check info
    Step  4  Compare ses page gold file

reset esm to check info
    Step  1  reset ESMA by ses command
    Step  2  set time delay  180
    Step  3  check info
    Step  4  Compare ses page gold file

power on/off drive all via ses command to check info
    ${sg_device_1} =  get_devicename  %{DUT_username}  %{DUT_ipv4_ip}  %{DUT_password}  Zone1
    Step  1  turn_off_drive  %{DUT_username}  %{DUT_ipv4_ip}  %{DUT_password}  ${sg_device_1}
    Step  2  set time delay  60
    Step  3  check_disk_number_via_ses_cmd  %{DUT_username}  %{DUT_ipv4_ip}  %{DUT_password}  ${cmd_check_disk_num}  0  ${not_test_hdd}  Off
    Step  4  turn_on_drive  %{DUT_username}  %{DUT_ipv4_ip}  %{DUT_password}  ${sg_device_1}
    Step  5  set time delay  60
    Step  6  check_disk_number_via_ses_cmd  %{DUT_username}  %{DUT_ipv4_ip}  %{DUT_password}  ${cmd_check_disk_num}  ${rsp_check_disk_num}  ${not_test_hdd}
#    Step  6  check info
    Step  7  Compare ses page gold file

power on/off drive one by one via ses command to check info
    ${sg_device_1} =  get_devicename  %{DUT_username}  %{DUT_ipv4_ip}  %{DUT_password}  Zone1
    Step  1   turn_off_drive  %{DUT_username}  %{DUT_ipv4_ip}  %{DUT_password}  ${sg_device_1}  ${rsp_check_disk_num}  mode=one by one
    Step  2   set time delay  60
    Step  3  check_disk_number_via_ses_cmd  %{DUT_username}  %{DUT_ipv4_ip}  %{DUT_password}  ${cmd_check_disk_num}  0  ${not_test_hdd}
    Step  4   turn_on_drive  %{DUT_username}  %{DUT_ipv4_ip}  %{DUT_password}  ${sg_device_1}  ${rsp_check_disk_num}  mode=one by one
    Step  5  set time delay  180
    Step  6  check_disk_number_via_ses_cmd  %{DUT_username}  %{DUT_ipv4_ip}  %{DUT_password}  ${cmd_check_disk_num}   ${rsp_check_disk_num}  ${not_test_hdd}
    Step  7  Compare ses page gold file

check info
    ${sg_device_1} =  get_devicename  %{DUT_username}  %{DUT_ipv4_ip}  %{DUT_password}  Zone1
#    ${sg_device_2} =  get_devicename  %{DUT_username}  %{DUT_ipv4_ip}  %{DUT_password}  Zone2
    Step  1  check_disk_number_via_ses_cmd  %{DUT_username}  %{DUT_ipv4_ip}  %{DUT_password}  ${cmd_check_disk_num}  ${rsp_check_disk_num}  ${not_test_hdd}
    Step  2  check_disk_number_via_os_cmd  %{DUT_username}  %{DUT_ipv4_ip}  %{DUT_password}  ${rsp_check_disk_os_num}  ${remove_disk}
    Step  3  verify_sbb_mode  %{DUT_username}  %{DUT_ipv4_ip}  %{DUT_password}  ${sg_device_1}  2

reset ESMA by cli
    Step  1  ESMAConnect  ${ESMA IP}  ${ESMA port}
    Step  2  run_cli_command  DUT  ${cmd_reset_esm_cli_command}
    Step  3  Disconnect

reset ESMA by ses command
    ${sg_device_1} =  get_devicename  %{DUT_username}  %{DUT_ipv4_ip}  %{DUT_password}  Zone1
    Step  1  ssh_command_run_ipmi_set_cmd  %{DUT_username}  %{DUT_ipv4_ip}  %{DUT_password}  ${cmd_reset_esm_ses_command} ${sg_device_1}

check Fan max speed
    ${sg_device_1} =  get_devicename  %{DUT_username}  %{DUT_ipv4_ip}  %{DUT_password}  Zone1
    Step  1  verify_ses_page_02_fan_current_speed  %{DUT_username}  %{DUT_ipv4_ip}  %{DUT_password}  ${sg_device_1}  ${fan_speed_1}
    Step  2  ESMAConnect  ${ESMA IP}  ${ESMA port}
    Step  3  verify_fan_speed_cli_command  DUT  ${fan_speed_cli_1}
    Step  4  verify_esm_fan_mode_cli_command  DUT  external
    Step  5  Disconnect
    Step  6  verify_ses_page_02_fan_current_speed  %{DUT_username}  %{DUT_ipv4_ip}  %{DUT_password}  ${sg_device_1}  ${fan_max_speed}
    Step  7  ESMAConnect  ${ESMA IP}  ${ESMA port}
    Step  8  verify_fan_speed_cli_command  DUT  ${fan_max_speed_cli}
    Step  9  verify_esm_fan_mode_cli_command  DUT  external
    Step  10  Disconnect
    Step  11  verify_ses_page_02_fan_current_speed  %{DUT_username}  %{DUT_ipv4_ip}  %{DUT_password}  ${sg_device_1}  ${fan_speed_1}
    Step  12  ESMAConnect  ${ESMA IP}  ${ESMA port}
    Step  13  verify_fan_speed_cli_command  DUT  ${fan_speed_cli_1}
    Step  14  verify_esm_fan_mode_cli_command  DUT  external
    Step  15  Disconnect

check Fan max speed ESMB
    ${sg_device_1} =  get_devicename  %{DUT_username}  %{DUT_ipv4_ip}  %{DUT_password}  Zone1
    Step  1  verify_ses_page_02_fan_current_speed  %{DUT_username}  %{DUT_ipv4_ip}  %{DUT_password}  ${sg_device_1}  ${fan_speed_1}
    Step  2  ESMAConnect  ${ESMB IP}  ${ESMB port}
    Step  3  verify_fan_speed_cli_command  DUT  ${fan_speed_cli_1}
    Step  4  verify_esm_fan_mode_cli_command  DUT  external
    Step  5  Disconnect
    Step  6  verify_ses_page_02_fan_current_speed  %{DUT_username}  %{DUT_ipv4_ip}  %{DUT_password}  ${sg_device_1}  ${fan_max_speed}
    Step  7  ESMAConnect  ${ESMB IP}  ${ESMB port}
    Step  8  verify_fan_speed_cli_command  DUT  ${fan_max_speed_cli}
    Step  9  verify_esm_fan_mode_cli_command  DUT  external
    Step  10  Disconnect
    Step  11  verify_ses_page_02_fan_current_speed  %{DUT_username}  %{DUT_ipv4_ip}  %{DUT_password}  ${sg_device_1}  ${fan_speed_1}
    Step  12  ESMAConnect  ${ESMB IP}  ${ESMB port}
    Step  13  verify_fan_speed_cli_command  DUT  ${fan_speed_cli_1}
    Step  14  verify_esm_fan_mode_cli_command  DUT  external
    Step  15  Disconnect

check Fan min speed
    ${sg_device_1} =  get_devicename  %{DUT_username}  %{DUT_ipv4_ip}  %{DUT_password}  Zone1
    Step  1  verify_ses_page_02_fan_current_speed  %{DUT_username}  %{DUT_ipv4_ip}  %{DUT_password}  ${sg_device_1}  ${fan_min_speed}
    Step  2  ESMAConnect  ${ESMA IP}  ${ESMA port}
    Step  3  verify_fan_speed_cli_command  DUT  ${fan_min_speed_cli}
    Step  4  verify_esm_fan_mode_cli_command  DUT  external
    Step  5  Disconnect
    Step  6  verify_ses_page_02_fan_current_speed  %{DUT_username}  %{DUT_ipv4_ip}  %{DUT_password}  ${sg_device_1}  ${fan_max_speed}
    Step  7  ESMAConnect  ${ESMA IP}  ${ESMA port}
    Step  8  verify_fan_speed_cli_command  DUT  ${fan_max_speed_cli}
    Step  9  verify_esm_fan_mode_cli_command  DUT  external
    Step  10  Disconnect
    Step  1  verify_ses_page_02_fan_current_speed  %{DUT_username}  %{DUT_ipv4_ip}  %{DUT_password}  ${sg_device_1}  ${fan_min_speed}
    Step  2  ESMAConnect  ${ESMA IP}  ${ESMA port}
    Step  3  verify_fan_speed_cli_command  DUT  ${fan_min_speed_cli}
    Step  4  verify_esm_fan_mode_cli_command  DUT  external
    Step  5  Disconnect

check Fan min speed ESMB
    ${sg_device_1} =  get_devicename  %{DUT_username}  %{DUT_ipv4_ip}  %{DUT_password}  Zone1
    Step  1  verify_ses_page_02_fan_current_speed  %{DUT_username}  %{DUT_ipv4_ip}  %{DUT_password}  ${sg_device_1}  ${fan_min_speed}
    Step  2  ESMAConnect  ${ESMB IP}  ${ESMB port}
    Step  3  verify_fan_speed_cli_command  DUT  ${fan_min_speed_cli}
    Step  4  verify_esm_fan_mode_cli_command  DUT  external
    Step  5  Disconnect
    Step  6  verify_ses_page_02_fan_current_speed  %{DUT_username}  %{DUT_ipv4_ip}  %{DUT_password}  ${sg_device_1}  ${fan_max_speed}
    Step  7  ESMAConnect  ${ESMB IP}  ${ESMB port}
    Step  8  verify_fan_speed_cli_command  DUT  ${fan_max_speed_cli}
    Step  9  verify_esm_fan_mode_cli_command  DUT  external
    Step  10  Disconnect
    Step  1  verify_ses_page_02_fan_current_speed  %{DUT_username}  %{DUT_ipv4_ip}  %{DUT_password}  ${sg_device_1}  ${fan_min_speed}
    Step  2  ESMAConnect  ${ESMB IP}  ${ESMB port}
    Step  3  verify_fan_speed_cli_command  DUT  ${fan_min_speed_cli}
    Step  4  verify_esm_fan_mode_cli_command  DUT  external
    Step  5  Disconnect

update cpld stress
    downgrade cpld with mode 0xe + mode 0xf
    upgrade cpld with mode 0xe + mode 0xf

upgrade cpld with mode 0xe + mode 0xf
    Step  1  upgrade whitebox cpld with mode e
    Step  2  activitate whitebox FW mode 0xf
    Step  3  set time delay  120
    ${sg_device_1} =  get_devicename  %{DUT_username}  %{DUT_ipv4_ip}  %{DUT_password}
    Step  4  check_cpld_version_via_ses_page  %{DUT_username}  %{DUT_ipv4_ip}  %{DUT_password}  ${sg_device_1}  isUpgrade=True
    Step  5  check_disk_number_via_ses_cmd  %{DUT_username}  %{DUT_ipv4_ip}  %{DUT_password}  ${cmd_check_disk_num}  ${rsp_check_disk_num}  ${not_test_hdd}
    #Step  5  check info
    Step  6  Compare ses page gold file

upgrade cpld with mode 0xe + mode 0xf Titan G2 WB
    Step  1  upgrade whitebox cpld with mode e Titan G2 WB
    Step  2  activitate whitebox FW mode 0xf for CPLD Titan G2 WB
    ${sg_device_1} =  get_devicename  %{DUT_username}  %{DUT_ipv4_ip}  %{DUT_password}
    Step  3  check_cpld_version_via_ses_page  %{DUT_username}  %{DUT_ipv4_ip}  %{DUT_password}  ${sg_device_1}  isUpgrade=True
    Step  4  check_disk_number_via_ses_cmd  %{DUT_username}  %{DUT_ipv4_ip}  %{DUT_password}  ${cmd_check_disk_num}  ${rsp_check_disk_num_titan_g2_wb}  ${not_test_hdd}

upgrade cpld with mode 0xe + reset 00h
    Step  1  upgrade whitebox cpld with mode e
    Step  2  activitate whitebox FW reset 00h
    Step  3  set time delay  120
    ${sg_device_1} =  get_devicename  %{DUT_username}  %{DUT_ipv4_ip}  %{DUT_password}
    Step  4  check_cpld_version_via_ses_page  %{DUT_username}  %{DUT_ipv4_ip}  %{DUT_password}  ${sg_device_1}  isUpgrade=True
    Step  5  check_disk_number_via_ses_cmd  %{DUT_username}  %{DUT_ipv4_ip}  %{DUT_password}  ${cmd_check_disk_num}  ${rsp_check_disk_num}  ${not_test_hdd}
    #Step  5  check info
    Step  6  Compare ses page gold file

upgrade cpld with mode 0xe + reset 00h Titan G2 WB
    Step  1  upgrade whitebox cpld with mode e Titan G2 WB
    Step  2  activitate whitebox FW reset 00h for CPLD Titan G2 WB
    ${sg_device_1} =  get_devicename  %{DUT_username}  %{DUT_ipv4_ip}  %{DUT_password}
    Step  3  check_cpld_version_via_ses_page  %{DUT_username}  %{DUT_ipv4_ip}  %{DUT_password}  ${sg_device_1}  isUpgrade=True
    Step  4  check_disk_number_via_ses_cmd  %{DUT_username}  %{DUT_ipv4_ip}  %{DUT_password}  ${cmd_check_disk_num}  ${rsp_check_disk_num_titan_g2_wb}  ${not_test_hdd}

upgrade cpld with mode 0xe + power cycle
    Step  1  upgrade whitebox cpld with mode e
    Step  2  activitate whitebox FW power cycle
    Step  3  set time delay  120
    ${sg_device_1} =  get_devicename  %{DUT_username}  %{DUT_ipv4_ip}  %{DUT_password}
    Step  4  check_cpld_version_via_ses_page  %{DUT_username}  %{DUT_ipv4_ip}  %{DUT_password}  ${sg_device_1}  isUpgrade=True
    Step  5  check_disk_number_via_ses_cmd  %{DUT_username}  %{DUT_ipv4_ip}  %{DUT_password}  ${cmd_check_disk_num}  ${rsp_check_disk_num}  ${not_test_hdd}
    #Step  5  check info
    Step  6  Compare ses page gold file

upgrade cpld with mode 0xe + power cycle Titan G2 WB
    Step  1  upgrade whitebox cpld with mode e Titan G2 WB
    Step  2  whitebox_lib.powercycle_pdu1  DUT
    Step  3  set time delay  150
    ${sg_device_1} =  get_devicename  %{DUT_username}  %{DUT_ipv4_ip}  %{DUT_password}
    Step  4  check_cpld_version_via_ses_page  %{DUT_username}  %{DUT_ipv4_ip}  %{DUT_password}  ${sg_device_1}  isUpgrade=True
    Step  5  check_disk_number_via_ses_cmd  %{DUT_username}  %{DUT_ipv4_ip}  %{DUT_password}  ${cmd_check_disk_num}  ${rsp_check_disk_num_titan_g2_wb}  ${not_test_hdd}

downgrade cpld with mode 0xe + mode 0xf
    Step  1  downgrade whitebox cpld with mode e
    Step  2  activitate whitebox FW mode 0xf
    Step  3  set time delay  120
    ${sg_device_1} =  get_devicename  %{DUT_username}  %{DUT_ipv4_ip}  %{DUT_password}
    Step  4  check_cpld_version_via_ses_page  %{DUT_username}  %{DUT_ipv4_ip}  %{DUT_password}  ${sg_device_1}  isUpgrade=False
    Step  5  check_disk_number_via_ses_cmd  %{DUT_username}  %{DUT_ipv4_ip}  %{DUT_password}  ${cmd_check_disk_num}  ${rsp_check_disk_num}  ${not_test_hdd}
    #Step  5  check info
    Step  6  Compare ses page gold file

downgrade cpld with mode 0xe + mode 0xf Titan G2 WB
    Step  1  downgrade whitebox cpld with mode e Titan G2 WB
    Step  2  activitate whitebox FW mode 0xf for CPLD Titan G2 WB
    ${sg_device_1} =  get_devicename  %{DUT_username}  %{DUT_ipv4_ip}  %{DUT_password}
    Step  3  check_cpld_version_via_ses_page  %{DUT_username}  %{DUT_ipv4_ip}  %{DUT_password}  ${sg_device_1}  isUpgrade=False
    Step  4  check_disk_number_via_ses_cmd  %{DUT_username}  %{DUT_ipv4_ip}  %{DUT_password}  ${cmd_check_disk_num}  ${rsp_check_disk_num_titan_g2_wb}  ${not_test_hdd}

downgrade cpld with mode 0xe + reset 00h
    Step  1  downgrade whitebox cpld with mode e
    Step  2  activitate whitebox FW reset 00h
    Step  3  set time delay  120
    ${sg_device_1} =  get_devicename  %{DUT_username}  %{DUT_ipv4_ip}  %{DUT_password}
    Step  4  check_cpld_version_via_ses_page  %{DUT_username}  %{DUT_ipv4_ip}  %{DUT_password}  ${sg_device_1}  isUpgrade=False
    Step  5  check_disk_number_via_ses_cmd  %{DUT_username}  %{DUT_ipv4_ip}  %{DUT_password}  ${cmd_check_disk_num}  ${rsp_check_disk_num}  ${not_test_hdd}
    #Step  5  check info
    Step  6  Compare ses page gold file

downgrade cpld with mode 0xe + reset 00h Titan G2 WB
    Step  1  downgrade whitebox cpld with mode e Titan G2 WB
    Step  2  activitate whitebox FW reset 00h for CPLD Titan G2 WB 
    ${sg_device_1} =  get_devicename  %{DUT_username}  %{DUT_ipv4_ip}  %{DUT_password}
    Step  3  check_cpld_version_via_ses_page  %{DUT_username}  %{DUT_ipv4_ip}  %{DUT_password}  ${sg_device_1}  isUpgrade=False
    Step  4  check_disk_number_via_ses_cmd  %{DUT_username}  %{DUT_ipv4_ip}  %{DUT_password}  ${cmd_check_disk_num}  ${rsp_check_disk_num_titan_g2_wb}  ${not_test_hdd}

downgrade cpld with mode 0xe + power cycle
    Step  1  downgrade whitebox cpld with mode e
    Step  2  activitate whitebox FW power cycle
    Step  3  set time delay  120
    ${sg_device_1} =  get_devicename  %{DUT_username}  %{DUT_ipv4_ip}  %{DUT_password}
    Step  4  check_cpld_version_via_ses_page  %{DUT_username}  %{DUT_ipv4_ip}  %{DUT_password}  ${sg_device_1}  isUpgrade=False
    Step  5  check_disk_number_via_ses_cmd  %{DUT_username}  %{DUT_ipv4_ip}  %{DUT_password}  ${cmd_check_disk_num}  ${rsp_check_disk_num}  ${not_test_hdd}
    #Step  5  check info
    Step  6  Compare ses page gold file

downgrade cpld with mode 0xe + power cycle Titan G2 WB
    Step  1  downgrade whitebox cpld with mode e Titan G2 WB
    Step  2  whitebox_lib.powercycle_pdu1  DUT
    Step  3  set time delay  180
    ${sg_device_1} =  get_devicename  %{DUT_username}  %{DUT_ipv4_ip}  %{DUT_password}
    Step  4  check_cpld_version_via_ses_page  %{DUT_username}  %{DUT_ipv4_ip}  %{DUT_password}  ${sg_device_1}  isUpgrade=False
    Step  5  check_disk_number_via_ses_cmd  %{DUT_username}  %{DUT_ipv4_ip}  %{DUT_password}  ${cmd_check_disk_num}  ${rsp_check_disk_num_titan_g2_wb}  ${not_test_hdd}

upgrade whitebox cpld with mode e
    ${sg_device_1} =  get_devicename  %{DUT_username}  %{DUT_ipv4_ip}  %{DUT_password}
    Step  1  update_whitebox_fw_force  CPLD  ${download_microcode_modeE_cmd}  %{DUT_username}  %{DUT_ipv4_ip}  %{DUT_password}  ${sg_device_1}  isUpgrade=True

upgrade whitebox cpld with mode e Titan G2 WB
    ${sg_device_1} =  get_devicename  %{DUT_username}  %{DUT_ipv4_ip}  %{DUT_password}
    Step  1  update_whitebox_fw_force  CPLD  ${download_cpld_microcode_modeE_cmd_titan_g2_wb}  %{DUT_username}  %{DUT_ipv4_ip}  %{DUT_password}  ${sg_device_1}  isUpgrade=True

downgrade whitebox cpld with mode e
    ${sg_device_1} =  get_devicename  %{DUT_username}  %{DUT_ipv4_ip}  %{DUT_password}
    Step  1  update_whitebox_fw_force  CPLD  ${download_microcode_modeE_cmd}  %{DUT_username}  %{DUT_ipv4_ip}  %{DUT_password}  ${sg_device_1}  isUpgrade=False

downgrade whitebox cpld with mode e Titan G2 WB
    ${sg_device_1} =  get_devicename  %{DUT_username}  %{DUT_ipv4_ip}  %{DUT_password}
    Step  1  update_whitebox_fw_force  CPLD  ${download_cpld_microcode_modeE_cmd_titan_g2_wb}  %{DUT_username}  %{DUT_ipv4_ip}  %{DUT_password}  ${sg_device_1}  isUpgrade=False

upgrade FW with mode 0xe + mode 0xf
    Step  1  upgrade whitebox FW with mode 0xe
    Step  2  activitate whitebox FW mode 0xf
    Step  3  check upgrade FW version
#    Step  4  check info
    Step  5  Compare ses page gold file

downgrade FW with mode 0xe + mode 0xf
    Step  1  downgrade whitebox FW with mode 0xe
    Step  2  activitate whitebox FW mode 0xf
    Step  3  check downgrade FW version
    Step  4  check info
    Step  5  Compare ses page gold file

upgrade FW with mode 0xe + reset 00h code
    Step  1  upgrade whitebox FW with mode 0xe
    Step  2  activitate whitebox FW reset 00h
    Step  3  check upgrade FW version
    Step  4  check info
    Step  5  Compare ses page gold file

downgrade FW with mode 0xe + reset 00h code
    Step  1  downgrade whitebox FW with mode 0xe
    Step  2  activitate whitebox FW reset 00h
    Step  3  check downgrade FW version
    set time delay  60
    Step  4  check info
    Step  5  Compare ses page gold file

upgrade FW with mode 0xe + reset 01h code
    Step  1  upgrade whitebox FW with mode 0xe
    Step  2  activitate whitebox FW reset 01h
    Step  3  check upgrade FW version
    Step  4  check info
    Step  5  Compare ses page gold file

downgrade FW with mode 0xe + reset 01h code
    Step  1  downgrade whitebox FW with mode 0xe
    Step  2  activitate whitebox FW reset 01h
    Step  3  check downgrade FW version
    Step  4  check info
    Step  5  Compare ses page gold file

upgrade FW with mode 0xe + reset 03h code
    Step  1  upgrade whitebox FW with mode 0xe
    Step  2  activitate whitebox FW reset 03h
    Step  3  check upgrade FW version
    Step  4  check SES version on both ESMs
    Step  4  check info
    Step  5  Compare ses page gold file

downgrade FW with mode 0xe + reset 03h code
    Step  1  downgrade whitebox FW with mode 0xe
    Step  2  activitate whitebox FW reset 03h
    Step  3  check downgrade FW version
    Step  4  check info
    Step  5  check SES version on both ESMs
    Step  5  Compare ses page gold file

upgrade FW with mode 0xe + power cycle
    Step  1  upgrade whitebox FW with mode 0xe
    Step  2  activitate whitebox FW power cycle
    Step  3  check upgrade FW version
#    Step  4  check info
    Step  5  Compare ses page gold file

downgrade FW with mode 0xe + power cycle
    Step  1  downgrade whitebox FW with mode 0xe
    Step  2  activitate whitebox FW power cycle
    Step  3  check downgrade FW version
#    Step  4  check info
#    Step  5  Compare ses page gold file

upgrade whitebox FW with mode 0xe
    #${sg_device_1} =  get_devicename  %{DUT_username}  %{DUT_ipv4_ip}  %{DUT_password}  Zone1
    server Connect
    ${sg_device_1} =   get_primary_device
    Server Disconnect    
    Step  1  update_whitebox_fw_force  SES  ${download_microcode_modeE_cmd}  %{DUT_username}  %{DUT_ipv4_ip}  %{DUT_password}  ${sg_device_1}  isUpgrade=True
    #${sg_device_2} =  get_devicename  %{DUT_username}  %{DUT_ipv4_ip}  %{DUT_password}  Zone2
    server Connect
    ${sg_device_2} =   get_non_primary_device
    Server Disconnect    
    Step  2  update_whitebox_fw_force  SES  ${download_microcode_modeE_cmd}  %{DUT_username}  %{DUT_ipv4_ip}  %{DUT_password}  ${sg_device_2}  isUpgrade=True
    server Connect
    ${sg_device_1} =   get_primary_device
    ${sg_device_2} =   get_non_primary_device
    Server Disconnect
    #${sg_device_1} =  get_devicename  %{DUT_username}  %{DUT_ipv4_ip}  %{DUT_password}  Zone1
    #${sg_device_2} =  get_devicename  %{DUT_username}  %{DUT_ipv4_ip}  %{DUT_password}  Zone2

downgrade whitebox FW with mode 0xe
    #${sg_device_1} =  get_devicename  %{DUT_username}  %{DUT_ipv4_ip}  %{DUT_password}  Zone1
    #${sg_device_2} =  get_devicename  %{DUT_username}  %{DUT_ipv4_ip}  %{DUT_password}  Zone2
    server Connect
    ${sg_device_1} =   get_primary_device
    ${sg_device_2} =   get_non_primary_device
    Server Disconnect
    Step  1  update_whitebox_fw_force  SES  ${download_microcode_modeE_cmd}  %{DUT_username}  %{DUT_ipv4_ip}  %{DUT_password}  ${sg_device_1}  isUpgrade=False
    Step  2  update_whitebox_fw_force  SES  ${download_microcode_modeE_cmd}  %{DUT_username}  %{DUT_ipv4_ip}  %{DUT_password}  ${sg_device_2}  isUpgrade=False    
    server Connect
    ${sg_device_1} =   get_primary_device
    ${sg_device_2} =   get_non_primary_device
    Server Disconnect
    #${sg_device_1} =  get_devicename  %{DUT_username}  %{DUT_ipv4_ip}  %{DUT_password}  Zone1
    #${sg_device_2} =  get_devicename  %{DUT_username}  %{DUT_ipv4_ip}  %{DUT_password}  Zone2

activitate whitebox FW mode 0xf
    ${sg_device_1} =  get_devicename  %{DUT_username}  %{DUT_ipv4_ip}  %{DUT_password}  Zone1
    Step  1  ses_activitate  %{DUT_username}  %{DUT_ipv4_ip}  %{DUT_password}  ${sg_device_1}  0xf
    Step  2  set time delay  90
    ${sg_device_1} =  get_devicename  %{DUT_username}  %{DUT_ipv4_ip}  %{DUT_password}  Zone1
    ${sg_device_2} =  get_devicename  %{DUT_username}  %{DUT_ipv4_ip}  %{DUT_password}  Zone2
    Step  3  ses_activitate  %{DUT_username}  %{DUT_ipv4_ip}  %{DUT_password}  ${sg_device_2}  0xf
    Step  4  set time delay  90
    ${sg_device_2} =  get_devicename  %{DUT_username}  %{DUT_ipv4_ip}  %{DUT_password}  Zone2

activitate whitebox FW mode 0xf for CPLD Titan G2 WB
    ${sg_device_1} =  get_devicename  %{DUT_username}  %{DUT_ipv4_ip}  %{DUT_password}  Zone1
    Step  1  ses_activitate  %{DUT_username}  %{DUT_ipv4_ip}  %{DUT_password}  ${sg_device_1}  0xf
    Step  2  set time delay  150
    ${sg_device_1} =  get_devicename  %{DUT_username}  %{DUT_ipv4_ip}  %{DUT_password}  Zone1

activitate whitebox FW reset 00h
    ${sg_device_1} =  get_devicename  %{DUT_username}  %{DUT_ipv4_ip}  %{DUT_password}  Zone1
    Log  ${sg_device_1}
    Step  1  ses_activitate  %{DUT_username}  %{DUT_ipv4_ip}  %{DUT_password}  ${sg_device_1}  00h
    Step  2  set time delay  90
    ${sg_device_1} =  get_devicename  %{DUT_username}  %{DUT_ipv4_ip}  %{DUT_password}  Zone1
    Log  ${sg_device_1}
    ${sg_device_2} =  get_devicename  %{DUT_username}  %{DUT_ipv4_ip}  %{DUT_password}  Zone2
    Log  ${sg_device_2}
    Step  3  ses_activitate  %{DUT_username}  %{DUT_ipv4_ip}  %{DUT_password}  ${sg_device_2}  00h
    Step  4  set time delay  90
    ${sg_device_2} =  get_devicename  %{DUT_username}  %{DUT_ipv4_ip}  %{DUT_password}  Zone2
    Log  ${sg_device_2}

activitate whitebox FW reset 00h for CPLD Titan G2 WB
    ${sg_device_1} =  get_devicename  %{DUT_username}  %{DUT_ipv4_ip}  %{DUT_password}  Zone1
    Log  ${sg_device_1}
    Step  1  ses_activitate  %{DUT_username}  %{DUT_ipv4_ip}  %{DUT_password}  ${sg_device_1}  00h
    Step  2  set time delay  150
    ${sg_device_1} =  get_devicename  %{DUT_username}  %{DUT_ipv4_ip}  %{DUT_password}  Zone1
    Log  ${sg_device_1}

activitate whitebox FW reset 01h
    ${sg_device_1} =  get_devicename  %{DUT_username}  %{DUT_ipv4_ip}  %{DUT_password}  Zone1
    Step  1  ses_activitate  %{DUT_username}  %{DUT_ipv4_ip}  %{DUT_password}  ${sg_device_1}  01h
    Step  2  set time delay  90
    ${sg_device_2} =  get_devicename  %{DUT_username}  %{DUT_ipv4_ip}  %{DUT_password}  Zone2
    Step  3  ses_activitate  %{DUT_username}  %{DUT_ipv4_ip}  %{DUT_password}  ${sg_device_2}  01h
    Step  4  set time delay  90
    ${sg_device_1} =  get_devicename  %{DUT_username}  %{DUT_ipv4_ip}  %{DUT_password}  Zone1
    ${sg_device_2} =  get_devicename  %{DUT_username}  %{DUT_ipv4_ip}  %{DUT_password}  Zone2

activitate whitebox FW reset 03h
    ${sg_device_1} =  get_devicename  %{DUT_username}  %{DUT_ipv4_ip}  %{DUT_password}  Zone1
    Step  1  ses_activitate  %{DUT_username}  %{DUT_ipv4_ip}  %{DUT_password}  ${sg_device_1}  03h
    Step  2  set time delay  90
    ${sg_device_2} =  get_devicename  %{DUT_username}  %{DUT_ipv4_ip}  %{DUT_password}  Zone2
    Step  3  ses_activitate  %{DUT_username}  %{DUT_ipv4_ip}  %{DUT_password}  ${sg_device_2}  03h
    Step  4  set time delay  90
    ${sg_device_1} =  get_devicename  %{DUT_username}  %{DUT_ipv4_ip}  %{DUT_password}  Zone1
    ${sg_device_2} =  get_devicename  %{DUT_username}  %{DUT_ipv4_ip}  %{DUT_password}  Zone2

activitate whitebox FW power cycle
    ###1(server)|2(JBOD)|3(ALL)
    #Keyword Retry  Step  1  powercycle_pdu2  DUT
    #Step  2  set time delay  200
    whitebox_lib.powercycle_pdu1  DUT
    set time delay  360
    
Do power cycle 
    ###1(server)|2(JBOD)|3(ALL)
    Keyword Retry  Step  1  powercycle_pdu2  DUT
    Step  2  set time delay  200

check upgrade FW version
    #${sg_device_1} =  get_devicename  %{DUT_username}  %{DUT_ipv4_ip}  %{DUT_password}  Zone1
    server Connect
    ${sg_device_1} =   get_primary_device
    Server Disconnect   
    #Step  1  ESMAConnect  ${ESMA IP}  ${ESMA port}
    Step  1  OS Connect Device
    Step  2  verify_ses_version_fru_get  DUT  isUpgrade=True
    Step  3  OS Disconnect Device
    server Connect
    ${sg_device_1} =   get_primary_device
    Log  ${sg_device_1}
    ${sg_device_2} =   get_non_primary_device
    Log  ${sg_device_2}
    Server Disconnect
    #${sg_device_1} =  get_devicename  %{DUT_username}  %{DUT_ipv4_ip}  %{DUT_password}  Zone1
    #Log  ${sg_device_1}
    #${sg_device_2} =  get_devicename  %{DUT_username}  %{DUT_ipv4_ip}  %{DUT_password}  Zone2
    #Step  4  ESMAConnect  ${ESMB IP}  ${ESMB port}
    Step  4  ConnectESMB
    Step  5  verify_ses_version_fru_get  DUT  isUpgrade=True
    Step  6  OS Disconnect Device
    server Connect
    ${sg_device_2} =   get_non_primary_device
    Server Disconnect
    #${sg_device_2} =  get_devicename  %{DUT_username}  %{DUT_ipv4_ip}  %{DUT_password}  Zone2
    #Log  ${sg_device_2}
    #check SES version on both ESMs

check downgrade FW version
    #${sg_device_1} =  get_devicename  %{DUT_username}  %{DUT_ipv4_ip}  %{DUT_password}  Zone1
    server Connect
    ${sg_device_1} =   get_primary_device
    ${sg_device_2} =   get_non_primary_device
    Server Disconnect
    #Step  1  ESMAConnect  ${ESMA IP}  ${ESMA port}
    Step  1  OS Connect Device
    Step  2  verify_ses_version_fru_get  DUT  isUpgrade=False
    Step  3  OS Disconnect Device
    #${sg_device_2} =  get_devicename  %{DUT_username}  %{DUT_ipv4_ip}  %{DUT_password}  Zone2
    server Connect
    ${sg_device_1} =   get_primary_device
    ${sg_device_2} =   get_non_primary_device
    Server Disconnect    
    #Step  4  ESMAConnect  ${ESMB IP}  ${ESMB port}
    Step  4  ConnectESMB
    Step  5  verify_ses_version_fru_get  DUT  isUpgrade=False
    Step  6  OS Disconnect Device
    server Connect
    ${sg_device_1} =   get_primary_device
    Log  ${sg_device_1}
    ${sg_device_2} =   get_non_primary_device
    Log  ${sg_device_2}
    Server Disconnect
    #${sg_device_1} =  get_devicename  %{DUT_username}  %{DUT_ipv4_ip}  %{DUT_password}  Zone1
    #Log  ${sg_device_1}
    #${sg_device_2} =  get_devicename  %{DUT_username}  %{DUT_ipv4_ip}  %{DUT_password}  Zone2
    #Log  ${sg_device_2}
    #check SES version on both ESMs

check Array OK Bit
    ${HDDs}=  query SG Devices
    ${DEVICEs}=  list Array Devices  ${HDDs}[0]
    verify RQST Fault Bit  ${HDDs}[0]  ${DEVICEs}[0]


check Disk Power Off
    ${HDDs}=  query SG Devices
    ${DEVICEs}=  list Array Devices  ${HDDs}[0]
    verify Device Power Off  ${HDDs}[0]  ${DEVICEs}[0]

check String In Diagnostic Pages(04h)
    ${sg_device_1} =  get_devicename  %{DUT_username}  %{DUT_ipv4_ip}  %{DUT_password}
    Step  1  ESMAConnect  ${ESMA IP}  ${ESMA port}
    ${expect_ESMA_IP} =  get_ipconfig_cli  DUT  ip
    ${expect_gateway} =  get_ipconfig_cli  DUT  gateway
    ${expect_ESM_A_DHCP_Mode} =  get_ipconfig_cli  DUT  dhcp
    ${expect_ESMA_up_time} =  get_esm_up_time  DUT
    Step  2  Disconnect
    Step  3  verify_ses_page_04  %{DUT_username}  %{DUT_ipv4_ip}  %{DUT_password}  ${sg_device_1}  ${expect_ESMA_IP}  ${expect_gateway}
          ...  ${expect_ESM_A_DHCP_Mode}  ${expect_ESMA_up_time}

check String In Diagnostic Pages(05h)
    ${sg_device_1} =  get_devicename  %{DUT_username}  %{DUT_ipv4_ip}  %{DUT_password}
    Step  1  verify_ses_page_05  %{DUT_username}  %{DUT_ipv4_ip}  %{DUT_password}  ${sg_device_1}

get FRU Info
    ESMAConnect  ${ESMA IP}  ${ESMA port}
   # OS Connect Device
    verify esm mode cli command  DUT
    ${FRU_INFO}=  run ESM command  fru get
    OS Disconnect Device
    set Test Variable  ${FRU_INFO}  ${FRU_INFO}

get FRU Info ESMB
    ESMAConnect  ${ESMB IP}  ${ESMB port}
    #ConnectESMB
    verify esm mode cli command  DUT
    ${FRU_INFO}=  run ESM command  fru get
    OS Disconnect Device
    set Test Variable  ${FRU_INFO}  ${FRU_INFO}

check Descriptor Length
    Server Connect 1
    ${HDDs}=  query SG Devices
    verify Descriptor Length  ${HDDs}[0]  ${FRU_INFO}

check Disks Info On Page 0x0a
    ${HDDs}=  query SG Devices
    verify Disk Info  ${HDDs}[0]

Download SES FW File
    Server Connect 1
    download Ses Fw Image  upgrade=True
    download Ses Fw Image  upgrade=False
    server Disconnect

Download CPLD FW File
    server Connect
    download Cpld Fw Image  upgrade=True
    download Cpld Fw Image  upgrade=False
    server Disconnect

Download SES FW File And Update
    [Arguments]  ${UPGRADE}
    Server Connect 1
#    mkdir_data_path    DUT  "/root/titanlenovoG2"
    change_directory   DUT  "/root/titanlenovoG2"
    download Ses Fw Image  upgrade=${UPGRADE}
    ${HDDs}=  query SG Devices
    Log  ${HDDs}
    Log  ${HDDs}[0]
    Log  ${HDDs}[1]
    update Ses Fw  ${HDDs}[0]  upgrade=${UPGRADE}
    update Ses Fw  ${HDDs}[1]  upgrade=${UPGRADE} 
    server Disconnect
    activitate whitebox FW mode 0xf
    set Test Variable   ${HDDs}  ${HDDs}

Remove SES FW File
    Server Connect 1
    change_directory   DUT  "/root/titanlenovoG2"
    RemoveAthenaBIOSFwImage    DUT   SES 
    server Disconnect

check ESM SES FW Version
    [Arguments]  ${UPGRADE}
    #ESMAConnect  ${ESMA IP}  ${ESMA port}
    OS Connect Device
    verify_ses_version_fru_get  DUT  ${UPGRADE}
    OS Disconnect Device
    ConnectESMB
    verify_ses_version_fru_get  DUT  ${UPGRADE}
    OS Disconnect Device

Write Buffer To Download Microcode
    [Arguments]  ${UPGRADE}  ${TOOL}
    server Connect
    download Ses Fw Image  upgrade=${UPGRADE}
    ${HDDs}=  query SG Devices
    update Ses Fw  ${HDDs}[0]  upgrade=${UPGRADE}  tool=${TOOL}
    server Disconnect
    set Test Variable   ${HDDs}  ${HDDs}

check ESM Version
    Telnet ESM
    check ESM Updated Version

check SES FW Version On Server
    [Arguments]  ${UPGRADE}
    Server Connect 1
    ${HDDs}=  query SG Devices
    run And Check  ${check_sbb_cmd} ${HDDs}[0]  ${check_sbb_result}
    check Page7 Fw Version  ${HDDs}[0]  upgrade=${UPGRADE}
    check Page2 Page10 Fw Version  ${HDDs}[0]  upgrade=${UPGRADE}
    run And Check  ${bsp_expander_cmd}  ${search_bsp_expander}
    server Disconnect

reset And Check All Expanders
    [Arguments]  ${reset_cmd}
    ${HDDs}=  query SG Devices
    ${PageInfo}=  save Page7 And PageA Info  ${HDDs}
    ${Page2Info}=  check Devices Elements On Page2  ${HDDs}
    Telnet ESM
    runAndCheckCLI  log clear\r
    reset All Expanders  ${HDDs}  ${reset_cmd}
    set time delay  140
    ${HDDs}=  query SG Devices
    check Sbb Status  ${HDDs}
    Log  ${HDDs}
    Log  ${Page2Info}
    check Devices Elements On Page2  ${HDDs}  ${Page2Info}
    compare Page7 And PageA Info  ${HDDs}  ${PageInfo}
    disconnect TelnetObj
    Telnet ESM
    verify CLI Reset Info

reset And Check All Expanders Lenovo
    [Arguments]  ${reset_cmd}
    server Connect
    ${HDDs}=  query SG Devices
    ${PageInfo}=  save Page7 And PageA Info  ${HDDs}
    ${Page2Info}=  check Devices Elements On Page2  ${HDDs}
    server Disconnect
    OS Connect Device
    runAndCheckESMCLI  log clear\r
    OS Disconnect Device
    server Connect
    reset All Expanders  ${HDDs}  ${reset_cmd}
    set time delay  140
    ${HDDs}=  query SG Devices
    check Sbb Status  ${HDDs}
    Log  ${HDDs}
    Log  ${Page2Info}
    check Devices Elements On Page2  ${HDDs}  ${Page2Info}
    compare Page7 And PageA Info  ${HDDs}  ${PageInfo}
    server Disconnect
    OS Connect Device
    verify CLI Reset Info ESM
    OS Disconnect Device

download And Verify With FW Fault Image
    ${HDDs}=  query SG Devices
    download Ses Fw Image  module=FAULT_IMAGE
    Telnet ESM
    ${CLI_version}=  get ESM Version And Check
    ...  version_pattern=${esm_fw_version_pattern}
    download Microcode
    ...  cmd=${download_microcode_mode7_cmd}  HDD=${HDDs}[0]
    get ESM Version And Check
    ...  cmp_dict=${CLI_version}  version_pattern=${esm_fw_version_pattern}
    reset All Expanders  ${HDDs}  ${reset_expander_00_cmd}
    disconnect TelnetObj
    Telnet ESM
    check ESM Status
    disconnect TelnetObj

download And Verify With FW Fault Image Titan G2 WB
    server Connect
    ${HDDs}=  query SG Devices
    download Ses Fw Image  module=FAULT_IMAGE
    server Disconnect
    ${CLI_version}=  get ESM Version And Check
    ...  version_pattern=${esm_fw_version_pattern}
    server Connect
    download Microcode
    ...  cmd=${download_microcode_mode7_cmd}  HDD=${HDDs}[0]
    get ESM Version And Check
    ...  cmp_dict=${CLI_version}  version_pattern=${esm_fw_version_pattern}
    reset All Expanders  ${HDDs}  ${reset_expander_00_cmd}
    server Disconnect
    OSConnect
    check ESM Status

Verify With FW Fault Image Under Mode E
    ${HDDs}=  query SG Devices
    download Ses Fw Image  module=FAULT_IMAGE
    Telnet ESM
    ${CLI_version}=  get ESM Version And Check
    ...  version_pattern=${esm_fw_version_pattern}
    download Microcode
    ...  cmd=${download_microcode_modeE_cmd}  HDD=${HDDs}[0]
    active FW  ${HDDs}[0]
    verify CLI Log
    get ESM Version And Check
    ...  cmp_dict=${CLI_version}  version_pattern=${esm_fw_version_pattern}
    reset All Expanders  ${HDDs}  ${reset_expander_00_cmd}
    disconnect TelnetObj
    Telnet ESM
    check ESM Status
    disconnect TelnetObj

Verify With FW Fault Image Under Mode E Titan G2 WB
    ${HDDs}=  query SG Devices
    download Ses Fw Image  module=FAULT_IMAGE
    ${CLI_version}=  get ESM Version And Check
    ...  version_pattern=${esm_fw_version_pattern}
    server Connect
    download Microcode
    ...  cmd=${download_microcode_modeE_cmd}  HDD=${HDDs}[0]
    get ESM Version And Check
    ...  cmp_dict=${CLI_version}  version_pattern=${esm_fw_version_pattern}
    reset All Expanders  ${HDDs}  ${reset_expander_00_cmd}
    server Disconnect
    OSConnect
    check ESM Status

Download SES FW File And Power Cycle
    [Arguments]  ${upgrade_cmd}
    server Connect
    download Ses Fw Image  upgrade=True
    ${HDDs}=  query SG Devices
    ${PageInfo}=  save Page7 And PageA Info  ${HDDs}
    Telnet ESM
    ${CLI_version}=  get ESM Version And Check
    ...  version_pattern=${esm_fw_version_pattern}
    send Download Microcode  ${upgrade_cmd}  HDD=${HDDs}[0]
    Keyword Retry  powercycle_pdu2  DUT
    set time delay  90
    server Disconnect
    get ESM Version And Check
    ...  cmp_dict=${CLI_version}  version_pattern=${esm_fw_version_pattern}
    server Connect
    run And Check  ${check_modeE_cmd} ${HDDs}[0]  ${modeE_status}
    compare Page7 And PageA Info  ${HDDs}  ${PageInfo}

Download SES FW File And Power Cycle Titan G2 WB
    [Arguments]  ${upgrade_cmd}
    server Connect
    download Ses Fw Image  upgrade=True
    ${HDDs}=  query SG Devices
    ${PageInfo}=  save Page7 And PageA Info  ${HDDs}
    ${CLI_version}=  get ESM Version And Check
    ...  version_pattern=${esm_fw_version_pattern}
    server Connect
    send Download Microcode  ${upgrade_cmd}  HDD=${HDDs}[0]
    server Disconnect
    whitebox_lib.powercycle_pdu1  DUT
    set time delay  90
    get ESM Version And Check
    ...  cmp_dict=${CLI_version}  version_pattern=${esm_fw_version_pattern}
    server Connect
    ${HDDs}=  query SG Devices
    run And Check  ${check_modeE_cmd} ${HDDs}[0]  ${modeE_status}
    compare Page7 And PageA Info  ${HDDs}  ${PageInfo}

Download SES FW File And Interrupt with command
    [Arguments]  ${upgrade_cmd}
    server Connect
    download Ses Fw Image  upgrade=True
    ${HDDs}=  query SG Devices
    Telnet ESM
    ${CLI_version}=  get ESM Version And Check
    ...  version_pattern=${esm_fw_version_pattern}
    send Download Microcode  ${upgrade_cmd}  HDD=${HDDs}[0]
    run And Check  ${get_page2_cmd} ${HDDs}[0]  {}  prompt_cnt=3
    run Keyword If  '0xe' in $upgrade_cmd  active FW  ${HDDs}[0]
    sleep  ${ESM_BOOTING_TIME}
    check ESM Updated Version
    ${HDDs}=  query SG Devices
    check Page7 Fw Version  ${HDDs}[0]  upgrade=True

Download SES FW File And Interrupt with command Titan G2 WB
    [Arguments]  ${upgrade_cmd}
    server Connect
    download Ses Fw Image  upgrade=True
    ${HDDs}=  query SG Devices
    ${CLI_version}=  get ESM Version And Check
    ...  version_pattern=${esm_fw_version_pattern}
    server Connect
    send Download Microcode  ${upgrade_cmd}  HDD=${HDDs}[0]
    run And Check  ${get_page2_cmd} ${HDDs}[0]  {}  prompt_cnt=3
    run Keyword If  '0xe' in $upgrade_cmd  active FW  ${HDDs}[0]
    sleep  ${ESM_BOOTING_TIME}
    check ESM Updated Version
    server Connect
    ${HDDs}=  query SG Devices
    check Page7 Fw Version  ${HDDs}[0]  upgrade=True

Download SES FW File And Check Downloading Status
    [Arguments]  ${upgrade_cmd}
    server Connect
    download Ses Fw Image  upgrade=True
    ${HDDs}=  query SG Devices
    send Download Microcode  ${upgrade_cmd}  HDD=${HDDs}[0]
    check In New SSH Session  ${check_modeE_cmd} ${HDDs}[0]  ${modeE_downloading_status}
    sleep  120 s
    ${HDDs}=  query SG Devices
    check Page7 Fw Version  ${HDDs}[0]  upgrade=True
    Server Disconnect

Download SES FW File And Check Downloading Status Without Activate
    [Arguments]  ${upgrade_cmd}
    server Connect
    download Ses Fw Image  upgrade=True
    ${HDDs}=  query SG Devices
    ${PageInfo}=  save Page7 And PageA Info  ${HDDs}
    send Download Microcode  ${upgrade_cmd}  HDD=${HDDs}[0]
    check In New SSH Session  ${check_modeE_cmd} ${HDDs}[0]  ${modeE_downloading_status}
    sleep  120 s
    ${HDDs}=  query SG Devices
    compare Page7 And PageA Info  ${HDDs}  ${PageInfo}

Download SES FW File And Check Downloading Status Without Activate Titan G2 WB
    [Arguments]  ${upgrade_cmd}
    server Connect
    download Ses Fw Image  upgrade=True
    ${HDDs}=  query SG Devices
    ${PageInfo}=  save Page7 Info  ${HDDs}
    send Download Microcode  ${upgrade_cmd}  HDD=${HDDs}[0]
    check In New SSH Session  ${check_modeE_cmd} ${HDDs}[0]  ${modeE_downloading_status}
    sleep  120 s
    ${HDDs}=  query SG Devices
    compare Page7 Info  ${HDDs}  ${PageInfo}

activate New FW Partition
    server Connect
    ${HDDs}=  query SG Devices
    active FW  ${HDDs}[0]
    sleep  ${HDD_RESET_TIME} s
    ${HDDs}=  query SG Devices
    run And Check  ${check_modeE_cmd} ${HDDs}[0]  ${modeE_status}
    check Page7 Fw Version  ${HDDs}[0]  upgrade=True


activate New FW Partition Titan G2 WB
    [Arguments]  ${upgrade_cmd}
    download Ses Fw Image  upgrade=True
    ${HDDs}=  query SG Devices
    send Download Microcode  ${upgrade_cmd}  HDD=${HDDs}[0]
    sleep  120 s
    active FW  ${HDDs}[0]
    sleep  ${HDD_RESET_TIME} s
    ${HDDs}=  query SG Devices
    run And Check  ${check_modeE_cmd} ${HDDs}[0]  ${modeE_status}
    check Page7 Fw Version  ${HDDs}[0]  upgrade=True



check FW Download Status
    ${HDDs}=  query SG Devices
    check In New SSH Session  ${check_modeE_cmd} ${HDDs}[0]  ${modeE_status}


check SCISI Elements
    [Arguments]  ${check_cmd}  ${check_pattern}
    ${HDDs}=  query SG Devices
    run And Check  ${check_cmd} ${HDDs}[0]  ${check_pattern}

check Command Sent
    [Arguments]  ${check_cmd}  ${check_pattern}
    ${HDDs}=  query SG Devices
    run And Check  ${check_cmd} ${HDDs}[0]  ${check_pattern}  is_negative=True


check Enclosure Length
    [Arguments]  ${query_cmd}  ${query_pattern}  ${length_dict}
    ${HDDs}=  query SG Devices
    check Return Data  ${HDDs}[0]  ${query_cmd}  ${query_pattern}  ${length_dict}

verify phy information
    [Arguments]  ${read_cmd}  ${get_cmd}  ${check_pattern}
    ${HDDs}=  query SG Devices
    command Execute  ${HDDs}  ${read_cmd}
    validate Dict Pattern   ${HDDs}  ${get_cmd}  ${check_pattern}

check Command Pattern
    [Arguments]  ${check_cmd}  ${check_pattern}
    ${HDDs}=  query SG Devices
    run And Check  ${check_cmd} ${HDDs}[0]  ${check_pattern}

get Control Decscriptor Information 
    [Arguments]  ${check_cmd}
    ${HDDs}=  query SG Devices
    command Execute  ${HDDs}  ${check_cmd}

error Injection Control Diagnostic Page Trigger
    [Arguments]  ${page_tool_cmd}  ${el_id}  ${trigger_value}  ${tool_pattern}  ${page_status_cmd}  ${page_pattern}
    ${HDDs}=  query SG Devices 
    verify Error Injection Control   ${page_tool_cmd}  ${HDDs}[0]  ${el_id}  ${trigger_value}  ${tool_pattern}  ${page_status_cmd}  ${page_pattern}

CLI check for log entry
  [Arguments]
  ESMAConnect  ${ESMA_IP_1}  ${ESMA_port_1}
  check Log Status  DUT
  Disconnect

CLI check for log entry Titan G2 WB
  [Arguments]
  check Log Status  DUT
  OSDisconnect

Verify log pattern
  [Arguments]   ${cmd}  ${code}  ${pattern}
  ${HDDs}=  query SG Devices
  verify Log  ${HDDs}[0]  ${cmd}  ${code}  ${pattern}

verify Page Status
   [Arguments]   ${cmd}
   ${HDDs}=  query SG Devices
   checkLogPageStatus   ${cmd}   ${HDDs}[0]

check PSU status
  [Arguments]  ${cmd}  ${pattern}
  ${HDDs}=  query SG Devices
  verify PSU status  ${cmd}  ${HDDs}[0]  ${pattern}

CLI check for psu status
  [Arguments]   ${pattern}
  ESMAConnect  ${ESMA_IP_1}  ${ESMA_port_1}
  check CLI PSU Status  DUT   ${pattern}
  Disconnect

CLI check for psu status Titan G2 WB
  [Arguments]   ${pattern}
  OSConnect
  check CLI PSU Status  DUT   ${pattern}
  Disconnect


send A Command
   [Arguments]   ${cmd}
   ${HDDs}=  query SG Devices
   command run   ${cmd}  ${HDDs}[0]


compare PSU status with CLI
   [Arguments]   ${psu_pattern}  ${cmd}  ${PSU_NO}
   ${HDDs}=  query SG Devices
   ESMAConnect  ${ESMA_IP_1}  ${ESMA_port_1}
   check PSU Details With CLI  ${psu_pattern}  ${cmd}  ${PSU_NO}  ${HDDs}[0]  DUT
   Disconnect

compare PSU status with CLI Titan G2 WB
   [Arguments]   ${psu_pattern}  ${cmd}  ${PSU_NO}
   ${HDDs}=  query SG Devices
   checkPSUDetailsWithCLI_titan_g2_wb  ${psu_pattern}  ${cmd}  ${PSU_NO}  ${HDDs}[0]  DUT
   Disconnect

compare new log with CLI
   [Arguments]   ${cmd}
   ${HDDs}=  query SG Devices
   ESMAConnect  ${ESMA_IP_1}  ${ESMA_port_1}
   check Log Details With CLI   ${cmd}  ${HDDs}[0]  DUT
   Disconnect

compare new log with CLI Titan G2 WB
   [Arguments]   ${cmd}
   ${HDDs}=  query SG Devices
   check Log Details With CLI   ${cmd}  ${HDDs}[0]  DUT
   Disconnect

Verify element index flag as invalid
   [Arguments]  ${cmd}  ${dv1_index}  ${dv2_index}
   ${HDDs}=  query SG Devices
   verify Flag As Invalid  ${cmd}  ${dv1_index}   ${HDDs}[0]
   verify Flag As Invalid  ${cmd}  ${dv2_index}  ${HDDs}[1]

Verify element index flag as valid
   [Arguments]  ${cmd}  ${dv1_index}  ${dv2_index}
   ${HDDs}=  query SG Devices
   verify Flag As Valid  ${cmd}  ${dv1_index}   ${HDDs}[0]
   verify Flag As Valid  ${cmd}  ${dv2_index}  ${HDDs}[1]

check Driver Status
  [Arguments]   ${cmd}  ${drv_nums}  ${dev1_status}  ${dev2_status}
  ${HDDs}=  query SG Devices
  Verify driver status  ${cmd}  ${HDDs}[0]   ${drv_nums}  ${dev1_status}
  Verify driver status  ${cmd}  ${HDDs}[1]   ${drv_nums}  ${dev2_status}

check driver count and status
  [Arguments]   ${cmd}  ${drv_nums}  ${dev1_status_60drv}  ${dev2_status_60drv}  ${dev1_status_75drv}  ${dev2_status_75drv}
  ${HDDs}=  query SG Devices
  Verify driver count and status  ${cmd}  ${HDDs}[0]   ${drv_nums}  ${dev1_status_60drv}  ${dev1_status_75drv}
  Verify driver count and status   ${cmd}  ${HDDs}[1]   ${drv_nums}  ${dev2_status_60drv}  ${dev2_status_75drv}

check slot name format
   [Arguments]   ${cmd}
   ${HDDs}=  query SG Devices
   Verify slot name format  ${cmd}  ${HDDs}[0]
   Verify slot name format  ${cmd}  ${HDDs}[1]

check fan speed
   [Arguments]   ${fan_speed}  ${cli_pattern_l75}   ${cli_pattern_g75}
   ${sg_device_1} =  get_devicename  %{DUT_username}  %{DUT_ipv4_ip}  %{DUT_password}  Zone1
   set_ses_page_02_fan_speed  %{DUT_username}  %{DUT_ipv4_ip}  %{DUT_password}  ${sg_device_1}  ${fan_speed}
   get_ses_page_02_fan_speed  %{DUT_username}  %{DUT_ipv4_ip}  %{DUT_password}  ${sg_device_1}  ${fan_speed}
   ${No_of_drives} =  get the number of drives  %{DUT_username}  %{DUT_ipv4_ip}  %{DUT_password}
   ESMAConnect  ${ESMA_IP_1}  ${ESMA_port_1}
   verify fan speed  ${No_of_drives}   ${cli_pattern_l75}   ${cli_pattern_g75}  DUT
   Disconnect

check fan speed Titan G2 WB
   [Arguments]   ${fan_speed}  ${cli_pattern_l75}   ${cli_pattern_g75}
   ${sg_device_1} =  get_devicename  %{DUT_username}  %{DUT_ipv4_ip}  %{DUT_password}  Zone1
   set_ses_page_02_fan_speed  %{DUT_username}  %{DUT_ipv4_ip}  %{DUT_password}  ${sg_device_1}  ${fan_speed}
   get_ses_page_02_fan_speed  %{DUT_username}  %{DUT_ipv4_ip}  %{DUT_password}  ${sg_device_1}  ${fan_speed}
   ${No_of_drives} =  get the number of drives  %{DUT_username}  %{DUT_ipv4_ip}  %{DUT_password}
   OSConnect
   verify_fan_speed_cli_command  DUT  ${cli_pattern_l75}
   OSDisconnect

verify current fan speed
   ${sg_device_1} =  get_devicename  %{DUT_username}  %{DUT_ipv4_ip}  %{DUT_password}  Zone1
   set_ses_page_02_fan_speed  %{DUT_username}  %{DUT_ipv4_ip}  %{DUT_password}  ${sg_device_1}  ${fan_speed_14}
   get_ses_page_02_fan_speed  %{DUT_username}  %{DUT_ipv4_ip}  %{DUT_password}  ${sg_device_1}  ${fan_speed_14}
   ${No_of_drives} =  get the number of drives  %{DUT_username}  %{DUT_ipv4_ip}  %{DUT_password}
   ESMAConnect  ${ESMA_IP_1}  ${ESMA_port_1}
   verify fan speed  ${No_of_drives}  ${fan_speed_14_l75cli}  ${fan_speed_14_g75cli}  DUT
   Disconnect
   set_ses_page_02_fan_speed  %{DUT_username}  %{DUT_ipv4_ip}  %{DUT_password}  ${sg_device_1}  ${fan_speed_8}
   get_ses_page_02_fan_speed  %{DUT_username}  %{DUT_ipv4_ip}  %{DUT_password}  ${sg_device_1}  ${fan_speed_14}
   ESMAConnect  ${ESMA_IP_1}  ${ESMA_port_1}
   verify fan speed   ${No_of_drives}  ${fan_speed_14_l75cli}  ${fan_speed_14_g75cli}  DUT
   Disconnect

compare log info with CLI
   [Arguments]      ${cmd}
   ${HDDs}=  query SG Devices
   ESMAConnect  ${ESMA_IP_1}  ${ESMA_port_1}
   check log info with CLI  ${cmd}  ${HDDs}[0]  DUT
   Disconnect

compare log info with CLI Cronus
   [Arguments]      ${cmd}
   ${sg_device_1} =   get_non_primary_device
   ${output} =  execute_Linux_command   ${cmd} ${sg_device_1}
###   ESMAConnect  ${ESMA_IP_1}  ${ESMA_port_1}
   check log info with CLI Athena  ${output}  DUT
   Disconnect

compare log info with CLI Titan G2 WB
   [Arguments]      ${cmd}
   ${HDDs}=  query SG Devices
   check log info with CLI  ${cmd}  ${HDDs}[0]  DUT

verify display of page with timeout
   [Arguments]    ${diag_cmd}  ${page_cmd}  ${pattern}
   ${HDDs}=  query SG Devices
   check display of page once   ${diag_cmd}  ${page_cmd}  ${HDDs}[0]    ${pattern}

verify page with expander log
   [Arguments]    ${pri_cmd}  ${sec1_cmd}  ${sec2_cmd}   ${page_cmd}
   ${HDDs}=  query SG Devices
   ESMAConnect  ${ESMA_IP_1}  ${ESMA_port_1}
   check page with expander log  ${pri_cmd}  ${page_cmd}  ${HDDs}[0]  DUT
   execute ESM command  ${expdr_sec_1}
   check page with expander log  ${sec1_cmd}  ${page_cmd}  ${HDDs}[0]  DUT
   execute ESM command   ${expdr_sec_2}
   check page with expander log   ${sec2_cmd}  ${page_cmd}  ${HDDs}[0]  DUT
   execute ESM command   ${expdr_pri}
   Disconnect

Verify pattern match for 0x17 ses_page
   [Arguments]  ${diag_cmd}  ${ses_cmd}  ${pattern}
   ${HDDs}=  query SG Devices
   verify Page 0x10 and 0x17 Status  ${diag_cmd}   ${ses_cmd}  ${pattern}   ${HDDs}[0]

Verify pattern match for 0x10 ses_page
   [Arguments]  ${diag_cmd}  ${ses_cmd}  ${pattern}
   ${HDDs}=  query SG Devices
   verify Page 0x17 and 0x10 Status  ${diag_cmd}   ${ses_cmd}  ${pattern}   ${HDDs}[0]

Verify page and log CLI pattern
   [Arguments]  ${diag_cmd}  ${page_cmd}  ${CLI_cmd}
   ${HDDs}=  query SG Devices
   ESMAConnect  ${ESMA_IP_1}  ${ESMA_port_1}
   check log filter  ${diag_cmd}  ${page_cmd}  ${CLI_cmd}  ${HDDs}[0]  DUT   
   Disconnect

Verify page and LED CLI pattern   
   [Arguments]  ${diag_cmd}  ${page_cmd}  ${CLI_cmd}
   ${HDDs}=  query SG Devices
   ESMAConnect  ${ESMA_IP_1}  ${ESMA_port_1}
   Check LED CLI  ${diag_cmd}  ${page_cmd}  ${CLI_cmd}  ${HDDs}[0]  DUT
   Disconnect

Verify ses page and log CLI pattern
   [Arguments]    ${diag_cmd}  ${page_cmd}
   ${HDDs}=  query SG Devices
   ESMAConnect  ${ESMA_IP_1}  ${ESMA_port_1}
   check Page Status  ${diag_cmd}  ${page_cmd}  ${HDDs}[0] 
   check Log Status  DUT
   Disconnect

verify canister status 
   [Arguments]   ${page_cmd}   ${pattern}
   ${HDDs}=  query SG Devices
   Check canister status   ${page_cmd}    ${HDDs}[0]    ${pattern}
   
verify cansiter status and FW version
   [Arguments]   ${page_cmd}   ${pattern}
   ${HDDs}=  query SG Devices
   ESMAConnect  ${ESMA_IP_1}  ${ESMA_port_1}
   ${FW_Version}=  get FW version    DUT
   Disconnect
   check cansiter status and version   ${page_cmd}    ${HDDs}[0]    ${pattern}   ${FW_Version}

verify cansiter status and FW version Titan G2 WB
   [Arguments]   ${page_cmd}   ${pattern}
   ${HDDs}=  query SG Devices
   Server Disconnect
   OSConnect
   ${FW_Version}=  get FW version    DUT
   OSDisconnect
   server Connect
   check cansiter status and version   ${page_cmd}    ${HDDs}[0]    ${pattern}   ${FW_Version}

verify cansiter status and FW version Athena1
   [Arguments]   ${page_cmd}   ${pattern}
   ${sg_device_1} =   get_primary_device
   Server Disconnect
   OS Connect Device   
   change_to_ESM_mode
   ${FW_Version}=  get FW version    DUT
   exit_ESM_mode
   OSDisconnect
   server Connect
   check cansiter status and version   ${page_cmd}  ${sg_device_1}   ${pattern}   ${FW_Version}

set and verify fan control mode
    ESMAConnect  ${ESMA_IP_1}  ${ESMA_port_1}
    set_esm_fan_mode_cli_command  DUT   ${setmode_internal_cmd}
    verify_esm_fan_mode_cli_command  DUT  internal
    set_esm_fan_mode_cli_command  DUT   ${setmode_external_cmd}
    verify_esm_fan_mode_cli_command  DUT  external
    Disconnect

set and verify fan control mode Titan G2 WB
    OSConnect
    set_esm_fan_mode_cli_command  DUT   ${setmode_internal_cmd}
    verify_esm_fan_mode_cli_command  DUT  internal
    set_esm_fan_mode_cli_command  DUT   ${setmode_external_cmd}
    verify_esm_fan_mode_cli_command  DUT  external
    OSDisconnect

set and verify pwm value
    ESMAConnect  ${ESMA_IP_1}  ${ESMA_port_1}
    run_cli_command  DUT  ${set_pwm_cli_cmd}    
    sleep  15s
    verify_fan_speed_cli_command  DUT  ${set_pwm_value}
    Disconnect

set and verify pwm value Titan G2 WB
    OSConnect
    run_cli_command  DUT  ${set_pwm_cli_cmd}
    sleep  15s
    verify_fan_speed_cli_command  DUT  ${set_pwm_value}
    OSDisconnect

set and verify level
   ${No_of_drives} =  get the number of drives  %{DUT_username}  %{DUT_ipv4_ip}  %{DUT_password}
   ESMAConnect  ${ESMA_IP_1}  ${ESMA_port_1}
   run_cli_command  DUT   ${fan_speed_1_cmd}
   sleep  15s
   verify fan speed1  ${No_of_drives}  ${fan_min_speed_cli}  ${fan_min_speed_g75cli}  DUT
   verify_esm_fan_mode_cli_command  DUT  external
   run_cli_command  DUT   ${fan_speed_2_cmd}
   sleep  15s
   verify fan speed1  ${No_of_drives}  ${fan_speed_10_l75cli}  ${fan_speed_10_g75cli}  DUT
   verify_esm_fan_mode_cli_command  DUT  external
   run_cli_command  DUT   ${fan_speed_3_cmd}
   sleep  15s
   verify fan speed1  ${No_of_drives}  ${fan_speed_11_l75cli}  ${fan_speed_11_g75cli}  DUT
   verify_esm_fan_mode_cli_command  DUT  external
   run_cli_command  DUT   ${fan_speed_4_cmd}
   sleep  15s
   verify fan speed1  ${No_of_drives}  ${fan_speed_12_l75cli}  ${fan_speed_12_g75cli}  DUT
   verify_esm_fan_mode_cli_command  DUT  external
   run_cli_command  DUT   ${fan_speed_5_cmd}
   sleep  15s
   verify fan speed1  ${No_of_drives}  ${fan_speed_13_l75cli}  ${fan_speed_13_g75cli}  DUT
   verify_esm_fan_mode_cli_command  DUT  external
   run_cli_command  DUT   ${fan_speed_6_cmd}
   sleep  15s
   verify fan speed1  ${No_of_drives}  ${fan_speed_14_l75cli}  ${fan_speed_14_g75cli}  DUT
   verify_esm_fan_mode_cli_command  DUT  external
   run_cli_command  DUT   ${fan_speed_7_cmd}
   sleep  15s
   verify fan speed1  ${No_of_drives}  ${fan_max_speed_l75cli}  ${fan_max_speed_g75cli}  DUT
   verify_esm_fan_mode_cli_command  DUT  external
   Disconnect

set and verify level Titan G2 WB
   ${No_of_drives} =  get the number of drives  %{DUT_username}  %{DUT_ipv4_ip}  %{DUT_password}
   OSConnect
   run_cli_command  DUT   ${fan_speed_1_cmd}
   sleep  15s
   verifyFanSpeed1  ${No_of_drives}  ${fan_min_speed_cli}  ${fan_min_speed_g75cli}  DUT
   verify_esm_fan_mode_cli_command  DUT  external
   run_cli_command  DUT   ${fan_speed_2_cmd}
   sleep  15s
   verifyFanSpeed1  ${No_of_drives}  ${fan_speed_10_l75cli}  ${fan_speed_10_g75cli}  DUT
   verify_esm_fan_mode_cli_command  DUT  external
   run_cli_command  DUT   ${fan_speed_3_cmd}
   sleep  15s
   verifyFanSpeed1  ${No_of_drives}  ${fan_speed_11_l75cli}  ${fan_speed_11_g75cli}  DUT
   verify_esm_fan_mode_cli_command  DUT  external
   run_cli_command  DUT   ${fan_speed_4_cmd}
   sleep  15s
   verifyFanSpeed1  ${No_of_drives}  ${fan_speed_12_l75cli}  ${fan_speed_12_g75cli}  DUT
   verify_esm_fan_mode_cli_command  DUT  external
   run_cli_command  DUT   ${fan_speed_5_cmd}
   sleep  15s
   verifyFanSpeed1  ${No_of_drives}  ${fan_speed_13_l75cli}  ${fan_speed_13_g75cli}  DUT
   verify_esm_fan_mode_cli_command  DUT  external
   run_cli_command  DUT   ${fan_speed_6_cmd}
   sleep  15s
   verifyFanSpeed1  ${No_of_drives}  ${fan_speed_14_l75cli}  ${fan_speed_14_g75cli}  DUT
   verify_esm_fan_mode_cli_command  DUT  external
   run_cli_command  DUT   ${fan_speed_7_cmd}
   sleep  15s
   verifyFanSpeed1  ${No_of_drives}  ${fan_max_speed_l75cli}  ${fan_max_speed_g75cli}  DUT
   verify_esm_fan_mode_cli_command  DUT  external
   OSDisconnect
 
Verify canister B inventory in page command
   [Arguments]  ${cmd}   ${pattern}
   ${HDDs}=  query SG Devices
   Check Canister Status  ${cmd}   ${HDDs}[0]  ${pattern}
   Disconnect

Verify canister details on CLI and page command
   [Arguments]  ${page_cmd}  ${CLI_cmd}
   ${HDDs}=  query SG Devices
   ESMAConnect  ${ESMA_IP_1}  ${ESMA_port_1}
   Verify canister details  ${page_cmd}  ${CLI_cmd}  ${HDDs}[0]  DUT
   Disconnect

Verify canister details on CLI and page command Titan G2 WB
   [Arguments]  ${page_cmd}  ${CLI_cmd}
   ${HDDs}=  query SG Devices
   Verifycanisterdetails_titan_g2_wb  ${page_cmd}  ${CLI_cmd}  ${HDDs}[0]  DUT

Verify lun report 
   [Arguments]  ${ses_cmd}  ${option}  ${pattern}
   ${HDDs}=  query SG Devices
   verify ses page lun  ${ses_cmd}  ${option}  ${pattern}  ${HDDs}[0]
   Disconnect

verify log with wrong data
   [Arguments]  ${cmd}
   ${HDDs}=  query SG Devices
   check log with wrong data   ${cmd}  ${HDDs}[0]

verify ESCE report bit
   [Arguments]  ${esc0_cmd}  ${esc1_cmd}  ${diag_cmd}  ${esc0_report}  ${esc1_report}
   ${HDDs}=  query SG Devices
   check esce report bit   ${esc0_cmd}   ${HDDs}[0]   ${esc0_report}
   check esce report bit   ${esc1_cmd}   ${HDDs}[0]   ${esc1_report}
   command run   ${diag_cmd}  ${HDDs}[0]
   check esce report bit   ${esc0_cmd}   ${HDDs}[0]   ${esc0_report}
   check esce report bit   ${esc1_cmd}   ${HDDs}[0]   ${esc1_report}

verify VPD information
   [Arguments] 
   ${HDDs}=  query SG Devices
   ESMAConnect  ${ESMA_IP_1}  ${ESMA_port_1}
   ${fru_get_output}=   run_ESM_command    ${canister_CLI_cmd}
   Disconnect
   verify mid plane VPD information   ${read_mid_plane_VPD_cmd}  ${get_VPD_cmd}  ${HDDs}[0]  ${fru_get_output}	
   verify canister VPD information   ${read_canister_VPD_cmd}  ${get_VPD_cmd} 	${HDDs}[0]  ${fru_get_output}
   verify PSU VPD information   ${read_PSU_VPD_cmd}  ${get_VPD_cmd}  ${HDDs}[0]  ${fru_get_output}
   verify all VPD information   ${read_all_VPD_cmd}  ${get_VPD_cmd}   ${HDDs}[0]  ${fru_get_output}

verify drive disk LED on off status 
   [Arguments]   ${set_on_LED}   ${set_off_LED}  ${get_page_cmd}  ${get_LED}  ${LED_on_pattern}  ${LED_off_pattern}
   ${HDDs}=  query SG Devices
   command run   ${set_on_LED}  ${HDDs}[0]
   check LED status    ${get_page_cmd}  ${get_LED_1}  ${get_LED_2}  ${get_LED_3}  ${get_LED}  ${get_LED_4}  ${LED_on_pattern}  ${HDDs}
   command run   ${set_off_LED}  ${HDDs}[0]
   check LED status    ${get_page_cmd}  ${get_LED_1}  ${get_LED_2}  ${get_LED_3}  ${get_LED}  ${get_LED_4}  ${LED_off_pattern}  ${HDDs}


verify Enclosure LED on off status 
   [Arguments]   ${set_on_LED}   ${set_off_LED}  ${pg_cmd}  ${get_page_cmd}  ${enc_LED}  ${LED_on_pattern}  ${LED_off_pattern}
   ${HDDs}=  query SG Devices
   command run  ${set_on_LED}  ${HDDs}[0]
   check enclosure LED status  ${pg_cmd}  ${get_page_cmd}  ${HDDs}[0]  ${get_LED_1}   ${enc_LED}  ${get_LED_4}  ${get_LED_5}  ${get_ident_LED}  ${LED_on_pattern}
   command run  ${set_off_LED}  ${HDDs}[0]
   check enclosure LED status  ${pg_cmd}  ${get_page_cmd}  ${HDDs}[0]  ${get_LED_1}   ${enc_LED}  ${get_LED_4}  ${get_LED_5}  ${get_ident_LED}  ${LED_off_pattern}

verify canister LED on off status 
   [Arguments]   ${set_on}  ${clear_canister}  ${check_can0_cmd}  ${check_can1_cmd}  ${ident_fail_cmd}  ${can_on_pattern}  ${can_off_pattern}  ${can_on_pattern_total}
   ${HDDs}=  query SG Devices
   command run  ${set_on}  ${HDDs}[0]
   check canister LED status   ${check_can0_cmd}  ${check_can1_cmd}  ${get_page2_cmd}  ${HDDs}[0]   ${get_LED_1}  ${get_LED_6}  ${get_LED_7}  ${ident_fail_cmd}   ${get_LED_4}  ${can_on_pattern}  ${can_on_pattern_total}
   command run  ${clear_canister}  ${HDDs}[0]
   check canister LED status   ${check_can0_cmd}  ${check_can1_cmd}  ${get_page2_cmd}  ${HDDs}[0]   ${get_LED_1}  ${get_LED_6}  ${get_LED_7}  ${ident_fail_cmd}   ${get_LED_4}  ${can_off_pattern}  ${can_off_pattern}


read write product asset tag
   [Arguments]
   ${HDDs}=  query SG Devices
   check product asset tag write read with correct byte length   ${write_asset_tag_cmd}   ${read_asset_tag_cmd}  ${updated_asset_tag_pattern}   ${HDDs}[0]
   check product asset tag write read with incorrect byte length   ${write_asset_tag_lesslength_cmd}    ${asset_tag_update_error_pattern}  ${HDDs}[0]
   check product asset tag write read with incorrect byte length   ${write_asset_tag_morelength_cmd}    ${asset_tag_update_error_pattern}  ${HDDs}[0]

Verify Enclosure Inventory details on CLI and page command
   [Arguments]  ${page_cmd}  ${CLI_cmd}
   ${HDDs}=  query SG Devices
   ESMAConnect  ${ESMA_IP_1}  ${ESMA_port_1}
   Verify Enclosure Inventory details  ${page_cmd}  ${CLI_cmd}  ${HDDs}[0]  DUT
   Disconnect

Verify Enclosure Inventory details on CLI and page command Titan G2 WB
   [Arguments]  ${page_cmd}  ${CLI_cmd}
   ${HDDs}=  query SG Devices
   VerifyEnclosureInventorydetails_titan_g2_wb  ${page_cmd}  ${CLI_cmd}  ${HDDs}[0]  DUT

verify Drive Disk Power
    [Arguments]
    ${No_of_drives}=  get number of drives
    ${HDDs}=  query SG Devices
    check drive disk power   ${set_drivedisk_power_off_cmd}   ${get_drivedisk_power_cmd}  ${HDDs}[0]  ${HDDs}[1]   ${No_of_drives}   ${device_on_pattern}
    check drive disk power   ${set_drivedisk_power_on_cmd}   ${get_drivedisk_power_cmd}  ${HDDs}[0]  ${HDDs}[1]   ${No_of_drives}   ${device_off_pattern}

Verify configuring and validating manufacturer date
    [Arguments]   ${set_cmd}  ${pattern}
    ESMAConnect  ${ESMA_IP_1}  ${ESMA_port_1}
    verify date modification  ${set_cmd}  ${pattern}  DUT
    Disconnect

Verify configuring and validating manufacturer date Titan G2 WB
    [Arguments]   ${set_cmd}  ${pattern}
    verifyDateModification_titan_g2_wb  ${set_cmd}  ${pattern}  DUT

verify command code and data reset
   [Arguments]
   ${HDDs}=  query SG Devices
   check local expander reset   ${reset_all_expanders_cmd}  ${HDDs}[0]
   sleep  120 s
   check local expander reset   ${reset_expanders_in_ESMA_cmd}  ${HDDs}[0]
   sleep  90 s
   check enter single mode print  ${reset_expanders_in_ESMB_cmd}  ${HDDs}[0]
   check local expander reset  ${reset_local_ESMs_cmd}  ${HDDs}[1]
   sleep  90 s
   check enter single mode print  ${reset_peer_ESM_cmd}   ${HDDs}[1]

verify smp phy enable disable
  [Arguments]
  ${Expanders}=  Query Expanders
  check SMP Phy Enable Disable   ${Expanders}[0]

verify smp phy enable disable Titan G2 WB
  [Arguments]
  ${Expanders}=  Query Expanders  ${smp_exp_index}
  check SMP Phy Enable Disable   ${Expanders}[0]

verify smp phy link speed
  [Arguments]
  ${Expanders}=  Query Expanders
  check SMP Phy link speed   ${Expanders}[0]

verify smp phy link speed Titan G2 WB
  [Arguments]
  ${Expanders}=  Query Expanders  ${smp_exp_index}
  check SMP Phy link speed   ${Expanders}[0]  10

verify command code and data for IP Configuration
   [Arguments]
   ${HDDs}=  query SG Devices
   check ip configuration   ${set_dhcp_ip_cmd}  ${pg4_cmd}  ${HDDs}[0]  ${dhcp_ip_pattern}
   check ip configuration   ${set_static_ip_cmd}  ${pg4_cmd}  ${HDDs}[0]  ${static_ip_pattern}

verify command code and data for IP Configuration Titan G2 WB
   [Arguments]
   ${HDDs}=  query SG Devices
   check ip configuration   ${set_dhcp_ip_cmd}  ${pg4_cmd}  ${HDDs}[0]  ${dhcp_ip_pattern_titan_g2_wb}
   check ip configuration   ${set_static_ip_cmd}  ${pg4_cmd}  ${HDDs}[0]  ${static_ip_pattern_titan_g2_wb}

Setting partial pathway timeout value
  [Arguments]
  ${Expanders}=  Query Expanders
  Set Partial Pathway Timeout   ${Expanders}[0]

Setting partial pathway timeout value Titan G2 WB
  [Arguments]  
  ${Expanders}=  Query Expanders  ${smp_exp_index}
  Set Partial Pathway Timeout   ${Expanders}[0]

verify fan mode
  [Arguments]
  change_to_ESM_mode
  set and get fan mode  ${fan_mode_set_internal_cmd}  ${fan_mode_get_cmd}  ${mode_external_pattern}
  set and get fan mode  ${fan_mode_set_external_cmd}  ${fan_mode_get_cmd}  ${mode_internal_pattern}
  exit_ESM_mode

Verify fan speed
  [Arguments]  ${dev}
  change_to_ESM_mode
  set and get fan speed   ${dev}
  exit_ESM_mode

VPD Function Check 
   change_to_ESM_mode

   ${poa_output}=   execute_ESM_command_1    poa
   common_check_patern_2    ${poa_output}  Current State.*SHARED MODE   POA mode check   expect=True

   ${fru_get_output_1}=   execute_ESM_command_1    fru get

   ${vpd_get_output_c_0}=   execute_ESM_command_1    vpd get -c 0
   common_check_patern_2    ${vpd_get_output_c_0}    Canister A Vpd.*Normal   VPD Check C 0 in ESM   expect=True
   common_check_patern_2    ${vpd_get_output_c_0}    VPD status OK   VPD Check C 0 in ESM   expect=True

   ${vpd_get_output_c_1}=   execute_ESM_command_1    vpd get -c 1
   common_check_patern_2    ${vpd_get_output_c_1}    Canister B Vpd.*Normal   VPD Check C 1 in ESM   expect=True
   common_check_patern_2    ${vpd_get_output_c_1}    VPD status OK   VPD Check C 1 in ESM   expect=True

   ${vpd_get_output_d_0}=   execute_ESM_command_1    vpd get -d 0
   common_check_patern_2    ${vpd_get_output_d_0}    Midplane Vpd 0.*Normal   VPD Check D 0 in ESM   expect=True
   common_check_patern_2    ${vpd_get_output_d_0}    VPD status OK   VPD Check D 0 in ESM   expect=True

   ${vpd_get_output_d_1}=   execute_ESM_command_1    vpd get -d 1
   common_check_patern_2    ${vpd_get_output_d_1}    Midplane Vpd 1.*Normal   VPD Check D 1 in ESM   expect=True
   common_check_patern_2    ${vpd_get_output_d_1}    VPD status OK   VPD Check 1 0 in ESM   expect=True

   ${vpd_get_output_p_0}=   execute_ESM_command_1    vpd get -p 0
   common_check_patern_2    ${vpd_get_output_p_0}    Power Supply A Vpd.*Normal   VPD Check P 0 in ESM   expect=True
   common_check_patern_2    ${vpd_get_output_p_0}    VPD status OK   VPD Check P 0 in ESM   expect=True

   ${vpd_get_output_p_1}=   execute_ESM_command_1    vpd get -p 1
   common_check_patern_2    ${vpd_get_output_p_1}    Power Supply B Vpd.*Normal   VPD Check P 1 in ESM   expect=True
   common_check_patern_2    ${vpd_get_output_p_1}    VPD status OK   VPD Check P 1 in ESM   expect=True

   execute_ESM_command_1  vpd reset -c 0
   execute_ESM_command_1  vpd reset -c 1
   execute_ESM_command_1  vpd reset -d 0 1
   execute_ESM_command_1  vpd reset -d 1 1

   Sleep  10

   ${fru_get_output_2}=   execute_ESM_command_1    fru get

   compare_fru_get_outputs   ${fru_get_output_1}   ${fru_get_output_2}

   exit_ESM_mode

Perform local chip reset in a primary device
   server Connect
   ${prim_dev} =   get_primary_device
   Set Suite Variable  ${prim_dev}

   FOR    ${INDEX}    IN RANGE  40
       Print Loop Info  ${INDEX}

       execute_Linux_command   sg_ses -p 2 -I esc,-1 --set=1:2:1=1 ${prim_dev}
       Sleep  40

       execute_Linux_command   sg_ses -p 0 ${prim_dev}
       execute_Linux_command   sg_ses -p 1 ${prim_dev}
       execute_Linux_command   sg_ses -p 2 ${prim_dev}
       execute_Linux_command   sg_ses -p 4 ${prim_dev}
       execute_Linux_command   sg_ses -p 5 ${prim_dev}
       execute_Linux_command   sg_ses -p 7 ${prim_dev}
       execute_Linux_command   sg_ses -p 0xa ${prim_dev}
       execute_Linux_command   sg_ses -p 0xe ${prim_dev}

   END
   Server Disconnect

Check the basic parameters in ESM mode after local chip reset
   OS Connect Device

   change_to_ESM_mode

   ${poa_output}=   execute_ESM_command_1    poa
   common_check_patern_2    ${poa_output}  Current State.*SHARED MODE   POA mode check   expect=True

   execute_ESM_command_1    log get

   execute_ESM_command_1    drv get
   
   ${led_output}=   execute_ESM_command_1    led get
   ${canister_version}=   get_canister_FW
   Log  ${canister_version}

   exit_ESM_mode
   OS Disconnect Device
   common_check_patern_2    ${led_output}  Drive Fault LED.*0.*OFF   LED Check  expect=True
   common_check_patern_2    ${led_output}  Drive Fault LED.*1.*OFF   LED Check  expect=True
   common_check_patern_2    ${led_output}  Drive Fault LED.*2.*OFF   LED Check  expect=True
   common_check_patern_2    ${led_output}  Drive Fault LED.*3.*OFF   LED Check  expect=True
   common_check_patern_2    ${led_output}  Drive Fault LED.*4.*OFF   LED Check  expect=True
   common_check_patern_2    ${led_output}  Drive Fault LED.*5.*OFF   LED Check  expect=True
   common_check_patern_2    ${led_output}  Drive Fault LED.*6.*OFF   LED Check  expect=True
   common_check_patern_2    ${led_output}  Drive Fault LED.*7.*OFF   LED Check  expect=True
   common_check_patern_2    ${led_output}  Drive Fault LED.*8.*OFF   LED Check  expect=True
   common_check_patern_2    ${led_output}  Drive Fault LED.*9.*OFF   LED Check  expect=True
   common_check_patern_2    ${led_output}  Drive Fault LED.*10.*OFF   LED Check  expect=True
   common_check_patern_2    ${led_output}  Drive Fault LED.*11.*OFF   LED Check  expect=True
   common_check_patern_2    ${led_output}  Drive Fault LED.*12.*OFF   LED Check  expect=True
   common_check_patern_2    ${led_output}  Drive Fault LED.*13.*OFF   LED Check  expect=True
   common_check_patern_2    ${led_output}  Drive Fault LED.*14.*OFF   LED Check  expect=True
   common_check_patern_2    ${led_output}  Drive Fault LED.*15.*OFF   LED Check  expect=True
   common_check_patern_2    ${led_output}  Drive Fault LED.*16.*OFF   LED Check  expect=True
   common_check_patern_2    ${led_output}  Drive Fault LED.*17.*OFF   LED Check  expect=True
   common_check_patern_2    ${led_output}  Drive Fault LED.*18.*OFF   LED Check  expect=True
   common_check_patern_2    ${led_output}  Drive Fault LED.*19.*OFF   LED Check  expect=True
   common_check_patern_2    ${led_output}  Drive Fault LED.*20.*OFF   LED Check  expect=True
   common_check_patern_2    ${led_output}  Drive Fault LED.*21.*OFF   LED Check  expect=True
   common_check_patern_2    ${led_output}  Drive Fault LED.*22.*OFF   LED Check  expect=True
   common_check_patern_2    ${led_output}  Drive Fault LED.*23.*OFF   LED Check  expect=True
   common_check_patern_2    ${led_output}  System Fault LED.*OFF   LED Check  expect=True
   common_check_patern_2    ${led_output}  System Identify LED.*OFF   LED Check  expect=True
   common_check_patern_2    ${led_output}  Canister Fault LED.*0.*OFF   LED Check  expect=True
   common_check_patern_2    ${led_output}  Canister Fault LED.*1.*OFF   LED Check  expect=True
   common_check_patern_2    ${led_output}  Local Canister Locate LED.*OFF   LED Check  expect=True
   common_check_patern_2    ${led_output}  Local Canister Power LED.*ON   LED Check  expect=True
   common_check_patern_2    ${led_output}  System ONLINE LED.*ON   LED Check  expect=True

Check the basic parameters in Linux OS after local chip reset
    server Connect
    ${HDDs}=  query SG Devices
    Log  ${HDDs}

    execute_Linux_command   sg_ses --page=0x2 ${prim_dev}

    execute_Linux_command   lspci -v -t
    Server Disconnect

Execute SES Page Command for multiple iterations
   server Connect
   ${prim_dev} =   get_primary_device
   Set Suite Variable  ${prim_dev}

   FOR    ${INDEX}    IN RANGE  100
       Print Loop Info  ${INDEX}
       ${HDDs}=  query SG Devices
       Log  ${HDDs}

       execute_Linux_command   sg_ses -p 0 ${prim_dev}
       execute_Linux_command   sg_ses -p 1 ${prim_dev}
       execute_Linux_command   sg_ses -p 2 ${prim_dev}
       execute_Linux_command   sg_ses -p 4 ${prim_dev}
       execute_Linux_command   sg_ses -p 5 ${prim_dev}
       execute_Linux_command   sg_ses -p 7 ${prim_dev}
       execute_Linux_command   sg_ses -p 0xa ${prim_dev}
       execute_Linux_command   sg_ses -p 0xe ${prim_dev}
       execute_Linux_command   sg_ses -p 0x11 ${prim_dev}
       execute_Linux_command   sg_ses -p 0x12 ${prim_dev}
       execute_Linux_command   sg_ses -p 0x13 ${prim_dev}

   END
   Server Disconnect

Check the basic parameters in ESM mode after SES Page Command is executed multiple times
   OS Connect Device

   change_to_ESM_mode

   ${poa_output}=   execute_ESM_command_1    poa
   common_check_patern_2    ${poa_output}  Current State.*SHARED MODE   POA mode check   expect=True

   ${canister_version}=   get_canister_FW
   Log  ${canister_version}

   exit_ESM_mode
   OS Disconnect Device

String Out Diagnostic Pages-04h--VPD update--Board info area_field id 02
   ${prim_dev} =   get_primary_device
   Set Suite Variable  ${prim_dev}

   execute_Linux_command   sg_senddiag -p -r ${set_board_product_name} ${prim_dev}
   execute_Linux_command   sg_senddiag -p -r ${VPD_update_status_diag_1} ${prim_dev}
   ${update_status} =  execute_Linux_command  sg_ses -p 0x4 ${prim_dev}
   common_check_patern_2  ${update_status}  ${check_update_status_1}  Check VPD update Status  expect=True
   execute_Linux_command  sg_senddiag -p -r ${VPD_field_data_diag_1} ${prim_dev}
   ${board_name_VPD} =  execute_Linux_command  sg_ses -p 0x4 ${prim_dev}
   common_check_patern_2  ${board_name_VPD}  ${check_board_product_name}  Check board name VPD  expect=True
   ${illegal_message} =  execute_Linux_command  sg_senddiag -p -r ${illegal_request_1} ${prim_dev}
   common_check_patern_2  ${illegal_message}  Illegal  Check error Message  expect=True

Compare enclosure status of two ESMs
    [Arguments]  ${cmd}
    compare_outputs  ${cmd}

String Out Diagnostic Pages(04h)--VPD update--Board info area_field id 01
   ${prim_dev} =   get_primary_device
   Set Suite Variable  ${prim_dev}
   execute_Linux_command   sg_senddiag -p -r ${set_board_product_name_106} ${prim_dev}
   execute_Linux_command   sg_senddiag -p -r ${VPD_update_status_diag_106} ${prim_dev}
   ${update_status} =  execute_Linux_command  sg_ses -p 0x4 ${prim_dev}
   common_check_patern_2  ${update_status}  ${check_update_status_106}  Check VPD update Status  expect=True
   execute_Linux_command  sg_senddiag -p -r ${VPD_field_data_diag_106} ${prim_dev}
   ${board_name_VPD} =  execute_Linux_command  sg_ses -p 0x4 ${prim_dev}
   common_check_patern_2  ${board_name_VPD}  ${check_board_product_name_106}  Check board name VPD  expect=True
   ${illegal_message} =  execute_Linux_command  sg_senddiag -p -r ${illegal_request_106} ${prim_dev}
   common_check_patern_2  ${illegal_message}  Illegal  Check error Message  expect=True

String Out Diagnostic Pages(04h)--VPD update--Board info area_field id 03
   ${prim_dev} =   get_primary_device
   Set Suite Variable  ${prim_dev}
   execute_Linux_command   sg_senddiag -p -r ${set_board_product_name_108} ${prim_dev}
   execute_Linux_command   sg_senddiag -p -r ${VPD_update_status_diag_108} ${prim_dev}
   ${update_status} =  execute_Linux_command  sg_ses -p 0x4 ${prim_dev}
   common_check_patern_2  ${update_status}  ${check_update_status_108}  Check VPD update Status  expect=True
   execute_Linux_command  sg_senddiag -p -r ${VPD_field_data_diag_108} ${prim_dev}
   ${board_name_VPD} =  execute_Linux_command  sg_ses -p 0x4 ${prim_dev}
   common_check_patern_2  ${board_name_VPD}  ${check_board_product_name_108}  Check board name VPD  expect=True
   ${illegal_message} =  execute_Linux_command  sg_senddiag -p -r ${illegal_request_108} ${prim_dev}
   common_check_patern_2  ${illegal_message}  Illegal  Check error Message  expect=True


execute and check completion of CLI commands
  change_to_ESM_mode
  FOR    ${INDEX}    IN RANGE    ${MAXINDEX}
       Print Loop Info  ${INDEX}
       check execution of CLI 
  END
  exit_ESM_mode


String Out Diagnostic Pages(04h)--VPD update--Board info area_field id 04
   ${prim_dev} =   get_primary_device
   Set Suite Variable  ${prim_dev}
   execute_Linux_command   sg_senddiag -p -r ${set_board_part_number_109} ${prim_dev}
   execute_Linux_command   sg_senddiag -p -r ${VPD_update_status_diag_109} ${prim_dev}
   ${update_status} =  execute_Linux_command  sg_ses -p 0x4 ${prim_dev}
   common_check_patern_2  ${update_status}  ${check_update_status_109}  Check VPD update Status  expect=True
   execute_Linux_command  sg_senddiag -p -r ${VPD_field_data_diag_109} ${prim_dev}
   ${board_part_number_VPD} =  execute_Linux_command  sg_ses -p 0x4 ${prim_dev}
   common_check_patern_2  ${board_part_number_VPD}  ${check_board_part_number_109}  Check board part number VPD  expect=True
   ${illegal_message} =  execute_Linux_command  sg_senddiag -p -r ${illegal_request_109} ${prim_dev}
   common_check_patern_2  ${illegal_message}  Illegal  Check error Message  expect=True

String Out Diagnostic Pages(04h)--VPD update--Chassis info area_field id 01
   ${prim_dev} =   get_primary_device
   Set Suite Variable  ${prim_dev}

   execute_Linux_command   sg_senddiag -p -r ${set_chassis_part_number} ${prim_dev}
   execute_Linux_command   sg_senddiag -p -r ${VPD_update_status_diag_2} ${prim_dev}
   ${update_status} =  execute_Linux_command  sg_ses -p 0x4 ${prim_dev}
   common_check_patern_2  ${update_status}  ${check_update_status_2}  Check VPD update Status  expect=True
   execute_Linux_command  sg_senddiag -p -r ${VPD_field_data_diag_2} ${prim_dev}
   ${chassis_part_number_VPD} =  execute_Linux_command  sg_ses -p 0x4 ${prim_dev}
   common_check_patern_2  ${chassis_part_number_VPD}  ${check_chassis_part_number}  Check Chassis Part Number VPD  expect=True
   ${illegal_message} =  execute_Linux_command  sg_senddiag -p -r ${illegal_request_2} ${prim_dev}
   common_check_patern_2  ${illegal_message}  Illegal  Check error Message  expect=True

String Out Diagnostic Pages(04h)--VPD update--Chassis info area_field id 03
  ${prim_dev} =   get_primary_device
   Set Suite Variable  ${prim_dev}
   execute_Linux_command   sg_senddiag -p -r ${set_chassis_product_name} ${prim_dev}
   execute_Linux_command   sg_senddiag -p -r ${VPD_update_status_diag_2} ${prim_dev}
   ${update_status} =  execute_Linux_command  sg_ses -p 0x4 ${prim_dev}
   common_check_patern_2  ${update_status}  ${check_update_status_112}  Check VPD update Status  expect=True
   execute_Linux_command  sg_senddiag -p -r ${VPD_field_data_diag_112} ${prim_dev}
   ${chassis_product_name_VPD} =  execute_Linux_command  sg_ses -p 0x4 ${prim_dev}
   common_check_patern_2  ${chassis_product_name_VPD}  ${check_chassis_product_name}  Check Chassis product name VPD  expect=True
   ${illegal_message} =  execute_Linux_command  sg_senddiag -p -r ${illegal_request_112} ${prim_dev}
   common_check_patern_2  ${illegal_message}  Illegal  Check error Message  expect=True


String Out Diagnostic Pages(04h)--VPD update--Chassis info area_field id 03-ESM
   execute_Linux_command  sg_senddiag -p -r ${VPD_field_data_diag_112} ${prim_dev}
   ${chassis_product_name_VPD} =  execute_Linux_command  sg_ses -p 0x4 ${prim_dev}
   common_check_patern_2  ${chassis_product_name_VPD}  ${check_chassis_product_name}  Check Chassis Product name VPD  expect=True


String Out Diagnostic Pages(04h)--VPD update--Product info area_field id 01
   ${prim_dev} =   get_primary_device
   Set Suite Variable  ${prim_dev}

   execute_Linux_command   sg_senddiag -p -r ${set_product_manufacturer} ${prim_dev}
   execute_Linux_command   sg_senddiag -p -r ${VPD_update_status_diag_3} ${prim_dev}
   ${update_status} =  execute_Linux_command  sg_ses -p 0x4 ${prim_dev}
   common_check_patern_2  ${update_status}  ${check_update_status_3}  Check VPD update Status  expect=True
   execute_Linux_command  sg_senddiag -p -r ${VPD_field_data_diag_3} ${prim_dev}
   ${product_manufacturer_VPD} =  execute_Linux_command  sg_ses -p 0x4 ${prim_dev}
   common_check_patern_2  ${product_manufacturer_VPD}  ${check_product_manufacturer}  Check Product Manufacturer VPD  expect=True
   ${illegal_message} =  execute_Linux_command  sg_senddiag -p -r ${illegal_request_3} ${prim_dev}
   common_check_patern_2  ${illegal_message}  Illegal  Check error Message  expect=True

String Out Diagnostic Pages(04h)--VPD update--Product info area_field id 03
   ${prim_dev} =   get_primary_device
   Set Suite Variable  ${prim_dev}
   execute_Linux_command   sg_senddiag -p -r ${set_product_part_number} ${prim_dev}
   execute_Linux_command   sg_senddiag -p -r ${VPD_update_status_diag_2} ${prim_dev}
   ${update_status} =  execute_Linux_command  sg_ses -p 0x4 ${prim_dev}
   common_check_patern_2  ${update_status}  ${check_update_status_115}  Check VPD update Status  expect=True
   execute_Linux_command  sg_senddiag -p -r ${VPD_field_data_diag_115} ${prim_dev}
   ${product_part_number_VPD} =  execute_Linux_command  sg_ses -p 0x4 ${prim_dev}
   common_check_patern_2  ${product_part_number_VPD}  ${check_product_part_number}  Check product part number VPD  expect=True
   ${illegal_message} =  execute_Linux_command  sg_senddiag -p -r ${illegal_request_115} ${prim_dev}
   common_check_patern_2  ${illegal_message}  Illegal  Check error Message  expect=True

String Out Diagnostic Pages(04h)--VPD update--Product info area_field id 04
   ${prim_dev} =   get_primary_device
   Set Suite Variable  ${prim_dev}
   execute_Linux_command   sg_senddiag -p -r ${set_product_version} ${prim_dev}
   execute_Linux_command   sg_senddiag -p -r ${VPD_update_status_diag_2} ${prim_dev}
   ${update_status} =  execute_Linux_command  sg_ses -p 0x4 ${prim_dev}
   common_check_patern_2  ${update_status}  ${check_update_status_116}  Check VPD update Status  expect=True
   execute_Linux_command  sg_senddiag -p -r ${VPD_field_data_diag_116} ${prim_dev}
   ${product_version_VPD} =  execute_Linux_command  sg_ses -p 0x4 ${prim_dev}
   common_check_patern_2  ${product_version_VPD}  ${check_product_version}  Check product version VPD  expect=True
   ${illegal_message} =  execute_Linux_command  sg_senddiag -p -r ${illegal_request_116} ${prim_dev}
   common_check_patern_2  ${illegal_message}  Illegal  Check error Message  expect=True

String Out Diagnostic Pages(04h)--VPD update--Product info area_field id 02
   ${prim_dev} =   get_primary_device
   Set Suite Variable  ${prim_dev}

   execute_Linux_command   sg_senddiag -p -r ${set_product_name} ${prim_dev}
   execute_Linux_command   sg_senddiag -p -r ${VPD_update_status_diag_4} ${prim_dev}
   ${update_status} =  execute_Linux_command  sg_ses -p 0x4 ${prim_dev}
   common_check_patern_2  ${update_status}  ${check_update_status_4}  Check VPD update Status  expect=True
   execute_Linux_command  sg_senddiag -p -r ${VPD_field_data_diag_4} ${prim_dev}
   ${product_name_VPD} =  execute_Linux_command  sg_ses -p 0x4 ${prim_dev}
   common_check_patern_2  ${product_name_VPD}  ${check_product_name}  Check Product Name VPD  expect=True
   ${illegal_message} =  execute_Linux_command  sg_senddiag -p -r ${illegal_request_4} ${prim_dev}
   common_check_patern_2  ${illegal_message}  Illegal  Check error Message  expect=True

Timestamp Set Diagnostic Page (11h) --- set outer margin of timestamp
   ${prim_dev} =   get_primary_device
   Set Suite Variable  ${prim_dev}
   ${update_Status} =   execute_Linux_command   sg_senddiag -p -r ${set_wrong_timestamp} ${prim_dev}
   common_check_patern_2   ${update_Status}  ${diag_failed_check}  Check wrong timestamp  expect=True
   ${Status_page} =  execute_Linux_command  sg_ses -p 0x11 ${prim_dev}
   common_check_patern_2   ${Status_page}  Error  Timestamp page status check  expect=False
   common_check_patern_2   ${Status_page}  sg_ses failed: Illegal request  Timestamp page status check  expect=False

Timestamp Set Diagnostic Page (11h) --- Get status page
   ${prim_dev} =   get_primary_device
   Set Suite Variable  ${prim_dev}
   ${Status_page} =  execute_Linux_command  sg_ses -p 0x11 ${prim_dev}
   common_check_patern_2   ${Status_page}  Error  Timestamp page status check  expect=False
   common_check_patern_2   ${Status_page}  sg_ses failed: Illegal request  Timestamp page status check  expect=False


String Out Diagnostic Pages(04h)--VPD update--Chassis info area_field id 02
   ${prim_dev} =   get_primary_device
   Set Suite Variable  ${prim_dev}
   execute_Linux_command   sg_senddiag -p -r ${set_chassis_part_number_111} ${prim_dev}
   execute_Linux_command   sg_senddiag -p -r ${VPD_update_status_diag_111} ${prim_dev}
   ${update_status} =  execute_Linux_command  sg_ses -p 0x4 ${prim_dev}
   common_check_patern_2  ${update_status}  ${check_update_status_111}  Check VPD update Status  expect=True
   execute_Linux_command  sg_senddiag -p -r ${VPD_field_data_diag_111} ${prim_dev}
   ${chassis_part_number_VPD} =  execute_Linux_command  sg_ses -p 0x4 ${prim_dev}
   common_check_patern_2  ${chassis_part_number_VPD}  ${check_chassis_part_number_111}  Check Chassis Part Number VPD  expect=True
   ${illegal_message} =  execute_Linux_command  sg_senddiag -p -r ${illegal_request_111} ${prim_dev}
   common_check_patern_2  ${illegal_message}  Illegal  Check error Message  expect=True

String Out Diagnostic Pages(04h)--VPD update--Chassis info area_field id 02-ESM
   execute_Linux_command  sg_senddiag -p -r ${VPD_field_data_diag_111} ${prim_dev}
   ${chassis_part_number_VPD} =  execute_Linux_command  sg_ses -p 0x4 ${prim_dev}
   common_check_patern_2  ${chassis_part_number_VPD}  ${check_chassis_part_number_111}  Check Chassis Part Number VPD  expect=True

String Out Diagnostic Pages(04h)--VPD update--Product info area_field id 05
   ${prim_dev} =   get_primary_device
   Set Suite Variable  ${prim_dev}
   execute_Linux_command   sg_senddiag -p -r ${set_chassis_part_number_117} ${prim_dev}
   execute_Linux_command   sg_senddiag -p -r ${VPD_update_status_diag_117} ${prim_dev}
   ${update_status} =  execute_Linux_command  sg_ses -p 0x4 ${prim_dev}
   common_check_patern_2  ${update_status}  ${check_update_status_117}  Check VPD update Status  expect=True
   execute_Linux_command  sg_senddiag -p -r ${VPD_field_data_diag_117} ${prim_dev}
   ${chassis_part_number_VPD} =  execute_Linux_command  sg_ses -p 0x4 ${prim_dev}
   common_check_patern_2  ${chassis_part_number_VPD}  ${check_chassis_part_number_117}  Check Chassis Part Number VPD  expect=True
   ${illegal_message} =  execute_Linux_command  sg_senddiag -p -r ${illegal_request_117} ${prim_dev}
   common_check_patern_2  ${illegal_message}  Illegal  Check error Message  expect=True

String Out Diagnostic Pages(04h)--VPD update--Product info area_field id 06
   ${prim_dev} =   get_primary_device
   Set Suite Variable  ${prim_dev}
   execute_Linux_command   sg_senddiag -p -r ${set_chassis_part_number_118} ${prim_dev}
   execute_Linux_command   sg_senddiag -p -r ${VPD_update_status_diag_118} ${prim_dev}
   ${update_status} =  execute_Linux_command  sg_ses -p 0x4 ${prim_dev}
   common_check_patern_2  ${update_status}  ${check_update_status_118}  Check VPD update Status  expect=True
   execute_Linux_command  sg_senddiag -p -r ${VPD_field_data_diag_118} ${prim_dev}
   ${chassis_part_number_VPD} =  execute_Linux_command  sg_ses -p 0x4 ${prim_dev}
   common_check_patern_2  ${chassis_part_number_VPD}  ${check_chassis_part_number_118}  Check Chassis Part Number VPD  expect=True
   ${illegal_message} =  execute_Linux_command  sg_senddiag -p -r ${illegal_request_118} ${prim_dev}
   common_check_patern_2  ${illegal_message}  Illegal  Check error Message  expect=True

Validate minimum timestamp value ESMA
   server Connect
   ${prim_dev} =   get_primary_device
   Set Suite Variable  ${prim_dev}
   execute_Linux_command   sg_senddiag -p -r ${timestamp_min} ${prim_dev}
   ${page_output} =  execute_Linux_command  sg_ses -p 0x11 ${prim_dev}
   common_check_patern_2  ${page_output}  Error  Check error Message  expect=False
   Sleep  4
   Server Disconnect
   OS Connect Device
   change_to_ESM_mode
   ${log_output} =  execute_ESM_command_1  log get
   common_check_patern_2  ${log_output}  .*Local Canister Running Time: 0 day 0 hours 0 minutes.*  Timestap min value validation  expect=True
   exit_ESM_mode
   Sleep  10
   OS Disconnect Device

Validate maximum timestamp value ESMA
   server Connect
   ${prim_dev} =   get_primary_device
   Set Suite Variable  ${prim_dev}
   execute_Linux_command   sg_senddiag -p -r ${timestamp_max} ${prim_dev}
   ${page_output} =  execute_Linux_command  sg_ses -p 0x11 ${prim_dev}
   common_check_patern_2  ${page_output}  Error  Check error Message  expect=False
   Sleep  10
   Server Disconnect
   OS Connect Device
   change_to_ESM_mode
   ${log_output} =  execute_ESM_command_1  log get
   common_check_patern_2  ${log_output}  .*Local Canister Running Time: 12725 day 19 hours 5.*minutes.*  Timestap max value validation  expect=True
   exit_ESM_mode
   Sleep  10
   OS Disconnect Device

Validate minimum timestamp value ESMB
   server Connect ESMB
   ${prim_dev} =   get_primary_device
   Set Suite Variable  ${prim_dev}
   execute_Linux_command   sg_senddiag -p -r ${timestamp_min} ${prim_dev}
   ${page_output} =  execute_Linux_command  sg_ses -p 0x11 ${prim_dev}
   common_check_patern_2  ${page_output}  Error  Check error Message  expect=False
   Sleep  4
   Server Disconnect
   ConnectESMB
   change_to_ESM_mode
   ${log_output} =  execute_ESM_command_1  log get
   common_check_patern_2  ${log_output}  .*Local Canister Running Time: 0 day 0 hours 0 minutes.*  Timestap min value validation  expect=True
   exit_ESM_mode
   Sleep  10
   OS Disconnect Device

Validate maximum timestamp value ESMB
   server Connect ESMB
   ${prim_dev} =   get_primary_device
   Set Suite Variable  ${prim_dev}
   execute_Linux_command   sg_senddiag -p -r ${timestamp_max} ${prim_dev}
   ${page_output} =  execute_Linux_command  sg_ses -p 0x11 ${prim_dev}
   common_check_patern_2  ${page_output}  Error  Check error Message  expect=False
   Sleep  10
   Server Disconnect
   ConnectESMB
   change_to_ESM_mode
   ${log_output} =  execute_ESM_command_1  log get
   common_check_patern_2  ${log_output}  .*Local Canister Running Time: 12725 day 19 hours 5.*minutes.*  Timestap max value validation  expect=True
   exit_ESM_mode
   Sleep  10
   OS Disconnect Device


AC Power Cycle the Device
    OS Connect Device
    whitebox_lib.powercycle_pdu1  DUT
    OS Disconnect Device
    Sleep  300

Set maximum timestamp value
    Validate maximum timestamp value ESMA

Validate default timestamp value in both ESMs
    Validate default timestamp value ESMA
    Validate default timestamp value ESMB

Validate default timestamp value ESMA
   server Connect
   ${prim_dev} =   get_primary_device
   Set Suite Variable  ${prim_dev}
   ${page_output} =  execute_Linux_command  sg_ses -p 0x11 ${prim_dev}
   common_check_patern_2  ${page_output}  Error  Check error Message  expect=False
   Sleep  4
   Server Disconnect
   OS Connect Device
   change_to_ESM_mode
   ${log_output} =  execute_ESM_command_1  log get
   common_check_patern_2  ${log_output}  .*Local Canister Running Time: 0 day 0 hours  Timestap min value validation  expect=True
   exit_ESM_mode
   Sleep  10
   OS Disconnect Device

Validate default timestamp value ESMB
   server Connect ESMB
   ${prim_dev} =   get_primary_device
   Set Suite Variable  ${prim_dev}
   ${page_output} =  execute_Linux_command  sg_ses -p 0x11 ${prim_dev}
   common_check_patern_2  ${page_output}  Error  Check error Message  expect=False
   Sleep  4
   Server Disconnect
   ConnectESMB
   change_to_ESM_mode
   ${log_output} =  execute_ESM_command_1  log get
   common_check_patern_2  ${log_output}  .*Local Canister Running Time: 0 day 0 hours  Timestap min value validation  expect=True
   exit_ESM_mode
   Sleep  10
   OS Disconnect Device

Upgrade Canister A PEX0 FW - Mode 7 and check upgrade status
    OS Connect Device
    ${prim_dev} =   get_primary_device
    Set Suite Variable  ${prim_dev}
    execute_Linux_command   sg_ses -p 1 ${prim_dev}
    ${image_to_upgrade} =   GetCanisterImageName    A0  Athena_FW_A 
    ${rev_to_check} =  GetRevFromCanisterImage  ${image_to_upgrade} 
    execute_Linux_command   sg_write_buffer -b 4k -I ${image_to_upgrade} -m 0x7 ${prim_dev}
    Sleep  10
    reboot_os  DUT
    OS Disconnect Device
    Sleep  300

    OS Connect Device
    ${page_output} =  execute_Linux_command   sg_ses -p 1 ${prim_dev}
    common_check_patern_2  ${page_output}  ${rev_to_check}  Check Rev Version after Download  expect=True
    ${inq_output} =  execute_Linux_command   sg_inq ${prim_dev}
    common_check_patern_2  ${inq_output}   ${rev_to_check}  Check Rev Version after Download  expect=True
 
    change_to_ESM_mode
    ${poa_output}=   execute_ESM_command_1    poa
    common_check_patern_2    ${poa_output}  Current State.*SHARED MODE   POA mode check   expect=True
    exit_ESM_mode

    OS Disconnect Device


Upgrade Canister A PEX1 FW - Mode 7 and check upgrade status
    OS Connect Device
    ${non_prim_dev} =   get_non_primary_device
    Set Suite Variable  ${non_prim_dev}
    execute_Linux_command   sg_ses -p 1 ${non_prim_dev}
    ${image_to_upgrade} =   GetCanisterImageName    A1  Athena_FW_A
    ${rev_to_check} =  GetRevFromCanisterImage  ${image_to_upgrade}
    execute_Linux_command   sg_write_buffer -b 4k -I ${image_to_upgrade} -m 0x7 ${non_prim_dev}
    Sleep  10
    reboot_os  DUT
    OS Disconnect Device
    Sleep  300

    OS Connect Device
    ${page_output} =  execute_Linux_command   sg_ses -p 1 ${non_prim_dev}
    common_check_patern_2  ${page_output}  ${rev_to_check}  Check Rev Version after Download  expect=True
    ${inq_output} =  execute_Linux_command   sg_inq ${non_prim_dev}
    common_check_patern_2  ${inq_output}   ${rev_to_check}  Check Rev Version after Download  expect=True

    change_to_ESM_mode_1
    ${poa_output}=   execute_ESM_command_1    poa
    common_check_patern_2    ${poa_output}  Current State.*SINGLE MODE   POA mode check   expect=True
    exit_ESM_mode

    OS Disconnect Device

Upgrade Canister B PEX0 FW - Mode 7 and check upgrade status
    ConnectESMB
    ${prim_dev} =   get_primary_device
    Set Suite Variable  ${prim_dev}
    execute_Linux_command   sg_ses -p 1 ${prim_dev}
    ${image_to_upgrade} =   GetCanisterImageName    B0  Athena_FW_B
    ${rev_to_check} =  GetRevFromCanisterImage  ${image_to_upgrade}
    execute_Linux_command   sg_write_buffer -b 4k -I ${image_to_upgrade} -m 0x7 ${prim_dev}
    Sleep  10
    reboot_os  DUT
    OS Disconnect Device
    Sleep  300

    ConnectESMB
    ${page_output} =  execute_Linux_command   sg_ses -p 1 ${prim_dev}
    common_check_patern_2  ${page_output}  ${rev_to_check}  Check Rev Version after Download  expect=True
    ${inq_output} =  execute_Linux_command   sg_inq ${prim_dev}
    common_check_patern_2  ${inq_output}   ${rev_to_check}  Check Rev Version after Download  expect=True

    change_to_ESM_mode
    ${poa_output}=   execute_ESM_command_1    poa
    common_check_patern_2    ${poa_output}  Current State.*SHARED MODE   POA mode check   expect=True
    exit_ESM_mode

    OS Disconnect Device

Upgrade Canister B PEX1 FW - Mode 7 and check upgrade status
    ConnectESMB
    ${non_prim_dev} =   get_non_primary_device
    Set Suite Variable  ${non_prim_dev}
    execute_Linux_command   sg_ses -p 1 ${non_prim_dev}
    ${image_to_upgrade} =   GetCanisterImageName    B1  Athena_FW_B
    ${rev_to_check} =  GetRevFromCanisterImage  ${image_to_upgrade}
    execute_Linux_command   sg_write_buffer -b 4k -I ${image_to_upgrade} -m 0x7 ${non_prim_dev}
    Sleep  10
    reboot_os  DUT
    OS Disconnect Device
    Sleep  300

    ConnectESMB
    ${page_output} =  execute_Linux_command   sg_ses -p 1 ${non_prim_dev}
    common_check_patern_2  ${page_output}  ${rev_to_check}  Check Rev Version after Download  expect=True
    ${inq_output} =  execute_Linux_command   sg_inq ${non_prim_dev}
    common_check_patern_2  ${inq_output}   ${rev_to_check}  Check Rev Version after Download  expect=True

    change_to_ESM_mode_1
    ${poa_output}=   execute_ESM_command_1    poa
    common_check_patern_2    ${poa_output}  Current State.*SINGLE MODE   POA mode check   expect=True
    exit_ESM_mode

    OS Disconnect Device

Download Athena FW image
    OS Connect Device
    downloadAthenaSesFwImage    DUT   Athena_FW_A
    OS Disconnect Device
    ConnectESMB
    downloadAthenaSesFwImage    DUT   Athena_FW_B
    OS Disconnect Device

Remove Athena FW image
    OS Connect Device
    RemoveAthenaSesFwImage    DUT   Athena_FW_A
    OS Disconnect Device
    ConnectESMB
    RemoveAthenaSesFwImage    DUT   Athena_FW_B
    OS Disconnect Device

Downgrade Canister A PEX0 FW - Mode 7 and check Downgrade status
    OS Connect Device
    ${prim_dev} =   get_primary_device
    Set Suite Variable  ${prim_dev}
    execute_Linux_command   sg_ses -p 1 ${prim_dev}
    ${image_to_Downgrade} =   GetCanisterImageName    A0  Athena_FW_A  False
    ${rev_to_check} =  GetRevFromCanisterImage  ${image_to_Downgrade}
    execute_Linux_command   sg_write_buffer -b 4k -I ${image_to_Downgrade} -m 0x7 ${prim_dev}
    Sleep  10
    reboot_os  DUT
    OS Disconnect Device
    Sleep  150

    OS Connect Device
    ${page_output} =  execute_Linux_command   sg_ses -p 1 ${prim_dev}
    common_check_patern_2  ${page_output}  ${rev_to_check}  Check Rev Version after Download  expect=True
    ${inq_output} =  execute_Linux_command   sg_inq ${prim_dev}
    common_check_patern_2  ${inq_output}   ${rev_to_check}  Check Rev Version after Download  expect=True

    change_to_ESM_mode
    ${poa_output}=   execute_ESM_command_1    poa
    common_check_patern_2    ${poa_output}  Current State.*SHARED MODE   POA mode check   expect=True
    exit_ESM_mode

    OS Disconnect Device


Downgrade Canister A PEX1 FW - Mode 7 and check Downgrade status
    OS Connect Device
    ${non_prim_dev} =   get_non_primary_device
    Set Suite Variable  ${non_prim_dev}
    execute_Linux_command   sg_ses -p 1 ${non_prim_dev}
    ${image_to_Downgrade} =   GetCanisterImageName    A1  Athena_FW_A  False
    ${rev_to_check} =  GetRevFromCanisterImage  ${image_to_Downgrade}
    execute_Linux_command   sg_write_buffer -b 4k -I ${image_to_Downgrade} -m 0x7 ${non_prim_dev}
    Sleep  10
    reboot_os  DUT
    OS Disconnect Device
    Sleep  150

    OS Connect Device
    ${page_output} =  execute_Linux_command   sg_ses -p 1 ${non_prim_dev}
    common_check_patern_2  ${page_output}  ${rev_to_check}  Check Rev Version after Download  expect=True
    ${inq_output} =  execute_Linux_command   sg_inq ${non_prim_dev}
    common_check_patern_2  ${inq_output}   ${rev_to_check}  Check Rev Version after Download  expect=True

    change_to_ESM_mode_1
    ${poa_output}=   execute_ESM_command_1    poa
    common_check_patern_2    ${poa_output}  Current State.*SINGLE MODE   POA mode check   expect=True
    exit_ESM_mode

    OS Disconnect Device

Downgrade Canister B PEX0 FW - Mode 7 and check Downgrade status
    ConnectESMB
    ${prim_dev} =   get_primary_device
    Set Suite Variable  ${prim_dev}
    execute_Linux_command   sg_ses -p 1 ${prim_dev}
    ${image_to_Downgrade} =   GetCanisterImageName    B0  Athena_FW_B  False
    ${rev_to_check} =  GetRevFromCanisterImage  ${image_to_Downgrade}
    execute_Linux_command   sg_write_buffer -b 4k -I ${image_to_Downgrade} -m 0x7 ${prim_dev}
    Sleep  10
    reboot_os  DUT
    OS Disconnect Device
    Sleep  150

    ConnectESMB
    ${page_output} =  execute_Linux_command   sg_ses -p 1 ${prim_dev}
    common_check_patern_2  ${page_output}  ${rev_to_check}  Check Rev Version after Download  expect=True
    ${inq_output} =  execute_Linux_command   sg_inq ${prim_dev}
    common_check_patern_2  ${inq_output}   ${rev_to_check}  Check Rev Version after Download  expect=True

    change_to_ESM_mode
    ${poa_output}=   execute_ESM_command_1    poa
    common_check_patern_2    ${poa_output}  Current State.*SHARED MODE   POA mode check   expect=True
    exit_ESM_mode

    OS Disconnect Device

Downgrade Canister B PEX1 FW - Mode 7 and check Downgrade status
    ConnectESMB
    ${non_prim_dev} =   get_non_primary_device
    Set Suite Variable  ${non_prim_dev}
    execute_Linux_command   sg_ses -p 1 ${non_prim_dev}
    ${image_to_Downgrade} =   GetCanisterImageName    B1  Athena_FW_B  False
    ${rev_to_check} =  GetRevFromCanisterImage  ${image_to_Downgrade}
    execute_Linux_command   sg_write_buffer -b 4k -I ${image_to_Downgrade} -m 0x7 ${non_prim_dev}
    Sleep  10
    reboot_os  DUT
    OS Disconnect Device
    Sleep  150

    ConnectESMB
    ${page_output} =  execute_Linux_command   sg_ses -p 1 ${non_prim_dev}
    common_check_patern_2  ${page_output}  ${rev_to_check}  Check Rev Version after Download  expect=True
    ${inq_output} =  execute_Linux_command   sg_inq ${non_prim_dev}
    common_check_patern_2  ${inq_output}   ${rev_to_check}  Check Rev Version after Download  expect=True

    change_to_ESM_mode_1
    ${poa_output}=   execute_ESM_command_1    poa
    common_check_patern_2    ${poa_output}  Current State.*SINGLE MODE   POA mode check   expect=True
    exit_ESM_mode

    OS Disconnect Device

Download Microcode -- Check log info via CLI
   change_to_ESM_mode
   ${poa_output}=   execute_ESM_command_1    poa
   common_check_patern_2    ${poa_output}  Current State.*SHARED MODE   POA mode check   expect=True
   ${about_output}=   execute_ESM_command_1    about
   common_check_patern_2    ${about_output}    ${version_pattern}     FW Revision check   expect=True
   ${log_output}=   execute_ESM_command_1     log get
   common_check_patern_2     ${log_output}     ${download_log_check}    Download Microcode log check   expect=True
   exit_ESM_mode

CPLD Firmware Download-Event log check
   change_to_ESM_mode
   ${log_output}=   execute_ESM_command_1     log get
   common_check_patern_2     ${log_output}     ${CPLD_FW_download_log_check}    CPLD FW Download log check   expect=True
   exit_ESM_mode

SES Download – Write Buffer log event check
   change_to_ESM_mode
   ${log_output}=   execute_ESM_command_1     log get
   common_check_patern_2     ${log_output}     ${download_log_check}    write Buffer log check   expect=True
   exit_ESM_mode

Downgrade Canister A PEX0 FW - Mode E + F and check Downgrade status
    OS Connect Device
    ${prim_dev} =   get_primary_device
    Set Suite Variable  ${prim_dev}
    execute_Linux_command   sg_ses -p 1 ${prim_dev}
    ${image_to_Downgrade} =   GetCanisterImageName    A0  Athena_FW_A  False
    ${rev_to_check} =  GetRevFromCanisterImage  ${image_to_Downgrade}
    execute_Linux_command   sg_write_buffer -b 4k -I ${image_to_Downgrade} -m 0xe ${prim_dev}
    execute_Linux_command   sg_write_buffer -m 0xf ${prim_dev}
    Sleep  300
    reboot_os  DUT
    OS Disconnect Device
    Sleep  300

    OS Connect Device
    ${page_output} =  execute_Linux_command   sg_ses -p 1 ${prim_dev}
    common_check_patern_2  ${page_output}  ${rev_to_check}  Check Rev Version after Download  expect=True
    ${inq_output} =  execute_Linux_command   sg_inq ${prim_dev}
    common_check_patern_2  ${inq_output}   ${rev_to_check}  Check Rev Version after Download  expect=True

    change_to_ESM_mode
    ${poa_output}=   execute_ESM_command_1    poa
    common_check_patern_2    ${poa_output}  Current State.*SHARED MODE   POA mode check   expect=True
    exit_ESM_mode

    OS Disconnect Device


Downgrade Canister A PEX1 FW - Mode E + F and check Downgrade status
    OS Connect Device
    ${non_prim_dev} =   get_non_primary_device
    Set Suite Variable  ${non_prim_dev}
    execute_Linux_command   sg_ses -p 1 ${non_prim_dev}
    ${image_to_Downgrade} =   GetCanisterImageName    A1  Athena_FW_A  False
    ${rev_to_check} =  GetRevFromCanisterImage  ${image_to_Downgrade}
    execute_Linux_command   sg_write_buffer -b 4k -I ${image_to_Downgrade} -m 0xe ${non_prim_dev}
    execute_Linux_command   sg_write_buffer -m 0xf ${non_prim_dev}
    Sleep  300
    reboot_os  DUT
    OS Disconnect Device
    Sleep  300

    OS Connect Device
    ${page_output} =  execute_Linux_command   sg_ses -p 1 ${non_prim_dev}
    common_check_patern_2  ${page_output}  ${rev_to_check}  Check Rev Version after Download  expect=True
    ${inq_output} =  execute_Linux_command   sg_inq ${non_prim_dev}
    common_check_patern_2  ${inq_output}   ${rev_to_check}  Check Rev Version after Download  expect=True

    change_to_ESM_mode_1
    ${poa_output}=   execute_ESM_command_1    poa
    common_check_patern_2    ${poa_output}  Current State.*SINGLE MODE   POA mode check   expect=True
    exit_ESM_mode

    OS Disconnect Device

Downgrade Canister B PEX0 FW - Mode E + F and check Downgrade status
    ConnectESMB
    ${prim_dev} =   get_primary_device
    Set Suite Variable  ${prim_dev}
    execute_Linux_command   sg_ses -p 1 ${prim_dev}
    ${image_to_Downgrade} =   GetCanisterImageName    B0  Athena_FW_B  False
    ${rev_to_check} =  GetRevFromCanisterImage  ${image_to_Downgrade}
    execute_Linux_command   sg_write_buffer -b 4k -I ${image_to_Downgrade} -m 0xe ${prim_dev}
    execute_Linux_command   sg_write_buffer -m 0xf ${prim_dev}
    Sleep  300
    reboot_os  DUT
    OS Disconnect Device
    Sleep  300

    ConnectESMB
    ${page_output} =  execute_Linux_command   sg_ses -p 1 ${prim_dev}
    common_check_patern_2  ${page_output}  ${rev_to_check}  Check Rev Version after Download  expect=True
    ${inq_output} =  execute_Linux_command   sg_inq ${prim_dev}
    common_check_patern_2  ${inq_output}   ${rev_to_check}  Check Rev Version after Download  expect=True

    change_to_ESM_mode
    ${poa_output}=   execute_ESM_command_1    poa
    common_check_patern_2    ${poa_output}  Current State.*SHARED MODE   POA mode check   expect=True
    exit_ESM_mode

    OS Disconnect Device

Downgrade Canister B PEX1 FW - Mode E + F and check Downgrade status
    ConnectESMB
    ${non_prim_dev} =   get_non_primary_device
    Set Suite Variable  ${non_prim_dev}
    execute_Linux_command   sg_ses -p 1 ${non_prim_dev}
    ${image_to_Downgrade} =   GetCanisterImageName    B1  Athena_FW_B  False
    ${rev_to_check} =  GetRevFromCanisterImage  ${image_to_Downgrade}
    execute_Linux_command   sg_write_buffer -b 4k -I ${image_to_Downgrade} -m 0xe ${non_prim_dev}
    execute_Linux_command   sg_write_buffer -m 0xf ${non_prim_dev}
    Sleep  300
    reboot_os  DUT
    OS Disconnect Device
    Sleep  300

    ConnectESMB
    ${page_output} =  execute_Linux_command   sg_ses -p 1 ${non_prim_dev}
    common_check_patern_2  ${page_output}  ${rev_to_check}  Check Rev Version after Download  expect=True
    ${inq_output} =  execute_Linux_command   sg_inq ${non_prim_dev}
    common_check_patern_2  ${inq_output}   ${rev_to_check}  Check Rev Version after Download  expect=True

    change_to_ESM_mode_1
    ${poa_output}=   execute_ESM_command_1    poa
    common_check_patern_2    ${poa_output}  Current State.*SINGLE MODE   POA mode check   expect=True
    exit_ESM_mode

    OS Disconnect Device

Upgrade Canister A PEX0 FW - Mode E + F and check upgrade status
    OS Connect Device
    ${prim_dev} =   get_primary_device
    Set Suite Variable  ${prim_dev}
    execute_Linux_command   sg_ses -p 1 ${prim_dev}
    ${image_to_upgrade} =   GetCanisterImageName    A0  Athena_FW_A
    ${rev_to_check} =  GetRevFromCanisterImage  ${image_to_upgrade}
    execute_Linux_command   sg_write_buffer -b 4k -I ${image_to_upgrade} -m 0xe ${prim_dev}
    execute_Linux_command   sg_write_buffer -m 0xf ${prim_dev}
    Sleep  300
    reboot_os  DUT
    OS Disconnect Device
    Sleep  300

    OS Connect Device
    ${page_output} =  execute_Linux_command   sg_ses -p 1 ${prim_dev}
    common_check_patern_2  ${page_output}  ${rev_to_check}  Check Rev Version after Download  expect=True
    ${inq_output} =  execute_Linux_command   sg_inq ${prim_dev}
    common_check_patern_2  ${inq_output}   ${rev_to_check}  Check Rev Version after Download  expect=True

    change_to_ESM_mode
    ${poa_output}=   execute_ESM_command_1    poa
    common_check_patern_2    ${poa_output}  Current State.*SHARED MODE   POA mode check   expect=True
    exit_ESM_mode

    OS Disconnect Device


Upgrade Canister A PEX1 FW - Mode E + F and check upgrade status
    OS Connect Device
    ${non_prim_dev} =   get_non_primary_device
    Set Suite Variable  ${non_prim_dev}
    execute_Linux_command   sg_ses -p 1 ${non_prim_dev}
    ${image_to_upgrade} =   GetCanisterImageName    A1  Athena_FW_A
    ${rev_to_check} =  GetRevFromCanisterImage  ${image_to_upgrade}
    execute_Linux_command   sg_write_buffer -b 4k -I ${image_to_upgrade} -m 0xe ${non_prim_dev}
    execute_Linux_command   sg_write_buffer -m 0xf ${non_prim_dev}
    Sleep  300
    reboot_os  DUT
    OS Disconnect Device
    Sleep  300

    OS Connect Device
    ${page_output} =  execute_Linux_command   sg_ses -p 1 ${non_prim_dev}
    common_check_patern_2  ${page_output}  ${rev_to_check}  Check Rev Version after Download  expect=True
    ${inq_output} =  execute_Linux_command   sg_inq ${non_prim_dev}
    common_check_patern_2  ${inq_output}   ${rev_to_check}  Check Rev Version after Download  expect=True

    change_to_ESM_mode_1
    ${poa_output}=   execute_ESM_command_1    poa
    common_check_patern_2    ${poa_output}  Current State.*SINGLE MODE   POA mode check   expect=True
    exit_ESM_mode

    OS Disconnect Device

Upgrade Canister B PEX0 FW - Mode E + F and check upgrade status
    ConnectESMB
    ${prim_dev} =   get_primary_device
    Set Suite Variable  ${prim_dev}
    execute_Linux_command   sg_ses -p 1 ${prim_dev}
    ${image_to_upgrade} =   GetCanisterImageName    B0  Athena_FW_B
    ${rev_to_check} =  GetRevFromCanisterImage  ${image_to_upgrade}
    execute_Linux_command   sg_write_buffer -b 4k -I ${image_to_upgrade} -m 0xe ${prim_dev}
    execute_Linux_command   sg_write_buffer -m 0xf ${prim_dev}
    Sleep  300
    reboot_os  DUT
    OS Disconnect Device
    Sleep  300

    ConnectESMB
    ${page_output} =  execute_Linux_command   sg_ses -p 1 ${prim_dev}
    common_check_patern_2  ${page_output}  ${rev_to_check}  Check Rev Version after Download  expect=True
    ${inq_output} =  execute_Linux_command   sg_inq ${prim_dev}
    common_check_patern_2  ${inq_output}   ${rev_to_check}  Check Rev Version after Download  expect=True

    change_to_ESM_mode
    ${poa_output}=   execute_ESM_command_1    poa
    common_check_patern_2    ${poa_output}  Current State.*SHARED MODE   POA mode check   expect=True
    exit_ESM_mode

    OS Disconnect Device

Upgrade Canister B PEX1 FW - Mode E + F and check upgrade status
    ConnectESMB
    ${non_prim_dev} =   get_non_primary_device
    Set Suite Variable  ${non_prim_dev}
    execute_Linux_command   sg_ses -p 1 ${non_prim_dev}
    ${image_to_upgrade} =   GetCanisterImageName    B1  Athena_FW_B
    ${rev_to_check} =  GetRevFromCanisterImage  ${image_to_upgrade}
    execute_Linux_command   sg_write_buffer -b 4k -I ${image_to_upgrade} -m 0xe ${non_prim_dev}
    execute_Linux_command   sg_write_buffer -m 0xf ${non_prim_dev}
    Sleep  300
    reboot_os  DUT
    OS Disconnect Device
    Sleep  300

    ConnectESMB
    ${page_output} =  execute_Linux_command   sg_ses -p 1 ${non_prim_dev}
    common_check_patern_2  ${page_output}  ${rev_to_check}  Check Rev Version after Download  expect=True
    ${inq_output} =  execute_Linux_command   sg_inq ${non_prim_dev}
    common_check_patern_2  ${inq_output}   ${rev_to_check}  Check Rev Version after Download  expect=True

    change_to_ESM_mode_1
    ${poa_output}=   execute_ESM_command_1    poa
    common_check_patern_2    ${poa_output}  Current State.*SINGLE MODE   POA mode check   expect=True
    exit_ESM_mode

    OS Disconnect Device

Download Microcode with offsets, save and activate - mode 07 for ESM A
    OS Connect Device
    ${prim_dev} =   get_primary_device
    Set Suite Variable  ${prim_dev}
    execute_Linux_command   sg_ses -p 1 ${prim_dev}
    ${image_to_upgrade} =   GetCanisterImageName    A0  Athena_FW_A
    ${rev_to_check} =  GetRevFromCanisterImage  ${image_to_upgrade}
    execute_Linux_command   sg_write_buffer -b 4k -I ${image_to_upgrade} -m 0x7 ${prim_dev}
    Sleep  60
    OS Disconnect Device

    OS Connect Device
    change_to_ESM_mode
    ${about_output}=   execute_ESM_command_1   about
    common_check_patern_2    ${about_output}  ${rev_to_check}  check in about command   expect=True
    exit_ESM_mode
    OS Disconnect Device

    OS Connect Device
    Sleep  10
    reboot_os  DUT
    OS Disconnect Device
    Sleep  150

Download Microcode with offsets, save and activate - mode 07 for ESM B
    ConnectESMB
    ${prim_dev} =   get_primary_device
    Set Suite Variable  ${prim_dev}
    execute_Linux_command   sg_ses -p 1 ${prim_dev}
    ${image_to_upgrade} =   GetCanisterImageName    B0  Athena_FW_B
    ${rev_to_check} =  GetRevFromCanisterImage  ${image_to_upgrade}
    execute_Linux_command   sg_write_buffer -b 4k -I ${image_to_upgrade} -m 0x7 ${prim_dev}
    Sleep  60
    OS Disconnect Device

    ConnectESMB
    change_to_ESM_mode
    ${about_output}=   execute_ESM_command_1   about
    common_check_patern_2    ${about_output}  ${rev_to_check}  check in about command   expect=True
    exit_ESM_mode
    OS Disconnect Device

    ConnectESMB
    Sleep  10
    reboot_os  DUT
    OS Disconnect Device
    Sleep  150

Download Athena CPLD image
    OS Connect Device
    downloadAthenaSesFwImage    DUT   Athena_FW_CPLD_A
    OS Disconnect Device
    ConnectESMB
    downloadAthenaSesFwImage    DUT   Athena_FW_CPLD_B
    OS Disconnect Device

Remove Athena CPLD image
    OS Connect Device
    RemoveAthenaSesFwImage    DUT   Athena_FW_CPLD_A
    OS Disconnect Device
    ConnectESMB
    RemoveAthenaSesFwImage    DUT   Athena_FW_CPLD_B
    OS Disconnect Device

CPLD Download microcode Control Diagnostic Page - mode 7 and check version in canister A
   OS Connect Device
   ${prim_dev} =   get_primary_device
   Set Suite Variable  ${prim_dev}
   ${image_to_upgrade} =   GetCanisterImageName   A0    Athena_FW_CPLD_A
   ${rev_to_check} =  GetRevFromCanisterImage  ${image_to_upgrade}
   execute_Linux_command   sg_ses_microcode -m 0x7 -b 4k -I ${image_to_upgrade} -i 4 ${prim_dev}
   Sleep   60
   OS Disconnect Device

   OS Connect Device
   verify_CPLD_version   ${rev_to_check}  A
   execute_ESM_command_1   about
   exit_ESM_mode
   OS Disconnect Device

CPLD Download microcode Control Diagnostic Page - mode 7 and check version in canister B
   ConnectESMB
   ${prim_dev} =   get_primary_device
   Set Suite Variable  ${prim_dev}
   ${image_to_upgrade} =   GetCanisterImageName   A0    Athena_FW_CPLD_B
   ${rev_to_check} =  GetRevFromCanisterImage  ${image_to_upgrade}
   execute_Linux_command   sg_ses_microcode -m 0x7 -b 4k -I ${image_to_upgrade} -i 4 ${prim_dev}
   Sleep   60
   OS Disconnect Device

   ConnectESMB
   verify_CPLD_version   ${rev_to_check}  B
   execute_ESM_command_1   about
   exit_ESM_mode
   OS Disconnect Device

Write Buffer - Download Microcode with offsets, save and defer activate (mode 0e) in canister A0
    OS Connect Device
    ${prim_dev} =   get_primary_device
    Set Suite Variable  ${prim_dev}
    execute_Linux_command   sg_ses -p 1 ${prim_dev}
    ${image_to_upgrade} =   GetCanisterImageName    A0  Athena_FW_A   False
    ${rev_to_check} =  GetRevFromCanisterImage   ${image_to_upgrade}
    execute_Linux_command   sg_write_buffer -b 4k -I ${image_to_upgrade} -m 0xe ${prim_dev}
    Sleep  30
    OS Disconnect Device

    OS Connect Device
    change_to_ESM_mode
    ${about_output}=   execute_ESM_command_1   about
    common_check_patern_2    ${about_output}  ${rev_to_check}  check in about command   expect=False
    exit_ESM_mode
    OS Disconnect Device

    OS Connect Device
    Sleep  10
    reboot_os  DUT
    OS Disconnect Device
    Sleep  150

Write Buffer - Download Microcode with offsets, save and defer activate (mode 0e) in canister B0
    ConnectESMB
    ${prim_dev} =   get_primary_device
    Set Suite Variable  ${prim_dev}
    execute_Linux_command   sg_ses -p 1 ${prim_dev}
    ${image_to_upgrade} =   GetCanisterImageName    B0  Athena_FW_B  False
    ${rev_to_check} =  GetRevFromCanisterImage  ${image_to_upgrade}
    execute_Linux_command   sg_write_buffer -b 4k -I ${image_to_upgrade} -m 0xe ${prim_dev}
    Sleep  60
    OS Disconnect Device

    ConnectESMB
    change_to_ESM_mode
    ${about_output}=   execute_ESM_command_1   about
    common_check_patern_2    ${about_output}  ${rev_to_check}  check in about command   expect=False
    exit_ESM_mode
    OS Disconnect Device

    ConnectESMB
    Sleep  10
    reboot_os  DUT
    OS Disconnect Device
    Sleep  150

SES Reset Validation Canister A
   [Arguments]  ${cmd1}  ${cmd2}
   OS Connect Device
   change_to_ESM_mode
   execute_ESM_command_1   log clear
   exit_ESM_mode
   Sleep  20 
   OS Disconnect Device
   server Connect
   ${prim_dev} =   get_primary_device
   Set Suite Variable  ${prim_dev}
   execute_Linux_command   ${cmd1} ${prim_dev}
   Sleep  100
   reboot_os  DUT
   Server Disconnect
   Sleep  250
   OS Connect Device
   change_to_ESM_mode
   ${log_output} =  execute_ESM_command_1  log get
   common_check_patern_2  ${log_output}  .*ESM Reset.*  ESM Reset log check  expect=True
   exit_ESM_mode
   Sleep  10
   OS Disconnect Device
   server Connect
   ${prim_dev} =   get_primary_device
   Set Suite Variable  ${prim_dev}
   ${output} =  execute_Linux_command  ${cmd2} ${prim_dev}
   common_check_patern_2  ${output}  Error  Check error message  expect=False
   Server Disconnect

SES Reset Validation Canister B
   [Arguments]  ${cmd1}  ${cmd2}
   ConnectESMB
   change_to_ESM_mode
   execute_ESM_command_1   log clear
   exit_ESM_mode
   Sleep  20
   OS Disconnect Device
   server Connect ESMB
   ${prim_dev} =   get_primary_device
   Set Suite Variable  ${prim_dev}
   execute_Linux_command   ${cmd1} ${prim_dev}
   Sleep  100
   reboot_os  DUT
   Server Disconnect
   Sleep  250
   ConnectESMB
   change_to_ESM_mode
   ${log_output} =  execute_ESM_command_1  log get
   common_check_patern_2  ${log_output}  .*ESM Reset.*  ESM Reset log check  expect=True
   exit_ESM_mode
   Sleep  10
   OS Disconnect Device
   server Connect ESMB
   ${prim_dev} =   get_primary_device
   Set Suite Variable  ${prim_dev}
   ${output} =  execute_Linux_command  ${cmd2} ${prim_dev}
   common_check_patern_2  ${output}  Error  Check error message  expect=False
   Server Disconnect

Write Buffer - Download Microcode with offsets, save and defer activate (mode 0f) in canister A0
    OS Connect Device
    ${prim_dev} =   get_primary_device
    Set Suite Variable  ${prim_dev}
    execute_Linux_command   sg_ses -p 1 ${prim_dev}
    ${image_to_upgrade} =   GetCanisterImageName    A0  Athena_FW_A   False
    ${rev_to_check} =  GetRevFromCanisterImage   ${image_to_upgrade}
    execute_Linux_command   sg_write_buffer -m 0x0f ${prim_dev}
    Sleep  30
    OS Disconnect Device

    OS Connect Device
    change_to_ESM_mode
    ${about_output}=   execute_ESM_command_1   about
    common_check_patern_2    ${about_output}  ${rev_to_check}  check in about command   expect=True
    exit_ESM_mode
    OS Disconnect Device

Write Buffer - Download Microcode with offsets, save and defer activate (mode 0f) in canister B0
    ConnectESMB
    ${prim_dev} =   get_primary_device
    Set Suite Variable  ${prim_dev}
    execute_Linux_command   sg_ses -p 1 ${prim_dev}
    ${image_to_upgrade} =   GetCanisterImageName    B0  Athena_FW_B  False
    ${rev_to_check} =  GetRevFromCanisterImage  ${image_to_upgrade}
    execute_Linux_command   sg_write_buffer -m 0x0f ${prim_dev}
    Sleep  60
    OS Disconnect Device

    ConnectESMB
    change_to_ESM_mode
    ${about_output}=   execute_ESM_command_1   about
    common_check_patern_2    ${about_output}  ${rev_to_check}  check in about command   expect=True
    exit_ESM_mode
    OS Disconnect Device

Upgrade Canister A FW - Verify in ESM A
    OS Connect Device
    ${prim_dev} =   get_primary_device
    Set Suite Variable  ${prim_dev}
    execute_Linux_command   sg_ses -p 1 ${prim_dev}
    ${image_to_upgrade} =   GetCanisterImageName    A0  Athena_FW_A   True
    ${rev_to_check} =  GetRevFromCanisterImage   ${image_to_upgrade}
    execute_Linux_command   sg_ses_microcode -b 4k -I ${image_to_upgrade} -m 0xe ${prim_dev}  sg_ses_microcode failed
    command run  sg_ses_microcode -m 0xf  ${prim_dev}
    Sleep  120
    reboot_os  DUT
    OS Disconnect Device
    Sleep  150

    OS Connect Device
    verify_disk_count   ${installed_disk_count}
    change_to_ESM_mode
    ${poa_output}=   execute_ESM_command_1    poa
    common_check_patern_2    ${poa_output}  Current State.*SHARED MODE   POA mode check   expect=True
    exit_ESM_mode
    OS Disconnect Device

    ConnectESMB
    verify_disk_count   ${installed_disk_count}
    change_to_ESM_mode
    ${poa_output}=   execute_ESM_command_1    poa
    common_check_patern_2    ${poa_output}  Current State.*SHARED MODE   POA mode check   expect=True
    exit_ESM_mode
    OS Disconnect Device

Upgrade Canister A FW - Verify in ESM B
    ConnectESMB
    ${prim_dev} =   get_primary_device
    Set Suite Variable  ${prim_dev}
    execute_Linux_command   sg_ses -p 1 ${prim_dev}
    ${image_to_upgrade} =   GetCanisterImageName    B0  Athena_FW_B   True
    ${rev_to_check} =  GetRevFromCanisterImage   ${image_to_upgrade}
    execute_Linux_command   sg_ses_microcode -b 4k -I ${image_to_upgrade} -m 0xe ${prim_dev}  sg_ses_microcode failed
    command run  sg_ses_microcode -m 0xf  ${prim_dev}
    Sleep  120
    reboot_os  DUT
    OS Disconnect Device
    Sleep  150

    ConnectESMB
    verify_disk_count   ${installed_disk_count}
    change_to_ESM_mode
    ${poa_output}=   execute_ESM_command_1    poa
    common_check_patern_2    ${poa_output}  Current State.*SHARED MODE   POA mode check   expect=True
    exit_ESM_mode
    OS Disconnect Device

    OS Connect Device
    verify_disk_count   ${installed_disk_count}
    change_to_ESM_mode
    ${poa_output}=   execute_ESM_command_1    poa
    common_check_patern_2    ${poa_output}  Current State.*SHARED MODE   POA mode check   expect=True
    exit_ESM_mode
    OS Disconnect Device

Download Athena PSU image
    OS Connect Device
    downloadAthenaSesFwImage    DUT   Athena_FW_PSU_A
    OS Disconnect Device
    ConnectESMB
    downloadAthenaSesFwImage    DUT   Athena_FW_PSU_B
    OS Disconnect Device

Remove Athena PSU image
    OS Connect Device
    RemoveAthenaSesFwImage    DUT   Athena_FW_PSU_A
    OS Disconnect Device
    ConnectESMB
    RemoveAthenaSesFwImage    DUT   Athena_FW_PSU_B
    OS Disconnect Device

PSU Download microcode Control Diagnostic Page - mode e
    [Arguments]    ${isupgrade}
    OS Connect Device
    ${prim_dev} =   get_primary_device
    Set Suite Variable  ${prim_dev}
    change_to_ESM_mode
    ${fru_get_output}=   execute_ESM_command_1    fru get
    Log   ${fru_get_output}
    exit_ESM_mode
    ${ps_hardware} =  get_ps_hardware    ${fru_get_output}
    Log   ${ps_hardware}
    ${image_to_upgrade} =   GetCanisterImageName   ${ps_hardware}   Athena_FW_PSU_B   ${isupgrade}
    Log  ${image_to_upgrade}
    ${psu_version} =  GetPSUVersion  Athena_FW_PSU_B   ${isupgrade}
    Log  ${psu_version}
    execute_Linux_command   sg_ses_microcode -m 0xe -b 4096 -I ${image_to_upgrade} -i 5 ${prim_dev}
    OS Disconnect Device
    Sleep  60
    OS Connect Device
    ${output} =  execute_Linux_command1  sg_ses -p 0xe ${prim_dev}
    Log  ${output}
    common_check_patern_2    ${output}  download microcode status: No download microcode operation in progress   verify the completion of FW download    expect=True
    ${output} =  execute_Linux_command   sg_ses -p 7 ${prim_dev}
    common_check_patern_2    ${output}     Element 0 descriptor: PSU1.*${psu_version}    verison_check_in_psu1  expect=False
    common_check_patern_2    ${output}     Element 1 descriptor: PSU2.*${psu_version}    verison_check_in_psu2   expect=False
    change_to_ESM_mode
    ${fru_get_output}=   execute_ESM_command_1    fru get
    Log   ${fru_get_output}
    exit_ESM_mode
    common_check_patern_2  ${fru_get_output}   ${psu_version}    check_psu_version  expect=false
    OS Disconnect Device

PSU Download microcode Control Diagnostic Page - mode f
    [Arguments]    ${isupgrade}    ${isdowngrade}
    OS Connect Device
    ${prim_dev} =   get_primary_device
    Set Suite Variable  ${prim_dev}
    ${psu_version} =  GetPSUVersion  Athena_FW_PSU_B   ${isupgrade}
    Log  ${psu_version}
    ${psu_version_old} =  GetPSUVersion  Athena_FW_PSU_B   ${isdowngrade}
    Log  ${psu_version_old}
    execute_Linux_command   sg_ses_microcode -m 0xf ${prim_dev}
    Sleep   1200
    OS Disconnect Device
    OS Connect Device
    Sleep   60
    execute_Linux_command1  sg_ses -p 0xe ${prim_dev}
    Sleep   20
    execute_Linux_command1  sg_ses -p 0xe ${prim_dev}
    Sleep   20
    execute_Linux_command1  sg_ses -p 0xe ${prim_dev}
    Sleep   20
    ${output} =  execute_Linux_command1  sg_ses -p 0xe ${prim_dev}
    Log  ${output}
    common_check_patern_2    ${output}  download microcode status: No download microcode operation in progress   verify the completion of FW download    expect=True
    ${output} =  execute_Linux_command1   sg_ses -p 7 ${prim_dev}
    common_check_patern_2    ${output}     Element 0 descriptor: PSU1.*${psu_version}    verison_check_in_psu1  expect=True
    common_check_patern_2    ${output}     Element 1 descriptor: PSU2.*${psu_version}    verison_check_in_psu2   expect=True
    common_check_patern_2    ${output}     Element 0 descriptor: PSU1.*${psu_version_old}    verison_check_in_psu1  expect=False
    common_check_patern_2    ${output}     Element 1 descriptor: PSU2.*${psu_version_old}    verison_check_in_psu2   expect=False
    change_to_ESM_mode
    ${fru_get_output}=   execute_ESM_command_1    fru get
    Log   ${fru_get_output}
    exit_ESM_mode
    common_check_patern_2  ${fru_get_output}   ${psu_version}    check_psu_version  expect=True
    common_check_patern_2  ${fru_get_output}   ${psu_version_old}    check_psu_version  expect=False
    OS Disconnect Device

PSU Download microcode Control Diagnostic Page - mode 7
    OS Connect Device
    ${prim_dev} =   get_primary_device
    Set Suite Variable  ${prim_dev}
    change_to_ESM_mode
    ${fru_get_output}=   execute_ESM_command_1    fru get
    Log   ${fru_get_output}
    exit_ESM_mode
    ${ps_hardware} =  get_ps_hardware    ${fru_get_output}
    Log   ${ps_hardware}
    ${psu_version} =  GetPSUVersion  Athena_FW_PSU_A   True
    Log  ${psu_version}
    ${image_to_upgrade}    ${psu_version_expected} =   GetCanisterUpdateImageName   ${ps_hardware}   Athena_FW_PSU_A   ${psu_version}
    Log  ${image_to_upgrade}
    Log  ${psu_version_expected}
    execute_Linux_command   sg_ses_microcode -m 0x7 -b 4096 -I ${image_to_upgrade} -i 5 ${prim_dev}
    OS Disconnect Device
    Sleep  720
    OS Connect Device
    ${output} =  execute_Linux_command  sg_ses -p 0xe ${prim_dev}
    Log  ${output}
    common_check_patern_2    ${output}  download microcode status: No download microcode operation in progress   verify the completion of FW download    expect=True
    ${output} =  execute_Linux_command   sg_ses -p 7 ${prim_dev}
    common_check_patern_2    ${output}     Element 0 descriptor: PSU1.*${psu_version_expected}    version_check_in_psu1   expect=True
    common_check_patern_2    ${output}     Element 1 descriptor: PSU2.*${psu_version_expected}    version_check_in_psu2   expect=True
    common_check_patern_2    ${output}     ${psu_version}    version_check_in_psu1   expect=False
    change_to_ESM_mode
    ${fru_get_output}=   execute_ESM_command_1    fru get
    Log   ${fru_get_output}
    exit_ESM_mode
    common_check_patern_2  ${fru_get_output}   ${psu_version}    check_psu_version  expect=False
    OS Disconnect Device

Veify PSU Firmware Download-Event log information
   change_to_ESM_mode
   ${log_output}=   execute_ESM_command_1     log get
   log   ${log_output}
   common_check_patern_2     ${log_output}     Upgrade cmpl with no ErrN/A, N/A, i.*PSU    PSU FW Download log check   expect=True
   exit_ESM_mode

check 'Info' bit lenovo
    ${sg_device_1} =  get_devicename  %{DUT_username}  %{DUT_ipv4_ip}  %{DUT_password}  Zone1
    Step  1  ssh_command_set_ses_page_command  %{DUT_username}  %{DUT_ipv4_ip}  %{DUT_password}
          ...  sg_ses -p 5 -I ts,0 --set=high_crit=50 ${sg_device_1}
    Step  2  set time delay  10
    Step  3  ssh_command_set_ses_page_command  %{DUT_username}  %{DUT_ipv4_ip}  %{DUT_password}
          ...  sg_ses -p 5 -I ts,0 --set=high_crit=95 ${sg_device_1}
    Step  4  set time delay  20
    Step  5  verify_ses_page_02h_info_bit  %{DUT_username}  %{DUT_ipv4_ip}  %{DUT_password}  ${sg_device_1}  1
    Step  6  ssh_command_set_ses_page_command  %{DUT_username}  %{DUT_ipv4_ip}  %{DUT_password}
          ...  sg_ses --page=0x02 --index=_24,0 --set=1:1:1=0 --byte1=0x00 ${sg_device_1}
    Step  7  set time delay  10
    Step  8  verify_ses_page_02h_info_bit  %{DUT_username}  %{DUT_ipv4_ip}  %{DUT_password}  ${sg_device_1}  0

check SES FW Version On Server lenovo
    [Arguments]  ${UPGRADE}
    server Connect
    ${HDDs}=  query SG Devices
    run And Check  ${check_sbb_cmd} ${HDDs}[0]  ${check_sbb_result_lenovo}
    check Page7 Fw Version  ${HDDs}[0]  upgrade=${UPGRADE}
    check Page2 Page10 Fw Version  ${HDDs}[0]  upgrade=${UPGRADE}
    run And Check  ${check_sbb_cmd} ${HDDs}[1]  ${check_sbb_result_lenovo}
    check Page7 Fw Version  ${HDDs}[1]  upgrade=${UPGRADE}
    check Page2 Page10 Fw Version  ${HDDs}[1]  upgrade=${UPGRADE}
    run And Check  ${bsp_expander_cmd}  ${search_bsp_expander}
    server Disconnect

check String In Diagnostic Pages(04h) lenovo
    ${sg_device_1} =  get_devicename  %{DUT_username}  %{DUT_ipv4_ip}  %{DUT_password}
    #Step  1  ESMAConnect  ${ESMA IP}  ${ESMA port}
    Step  1  OS Connect Device
    ${expect_ESMA_up_time} =  get_esm_up_time  DUT
    Step  2  OS Disconnect Device
    #Step  2  Disconnect
    #Step  3  ESMAConnect  ${ESMB IP}  ${ESMB port}
    Step  3   ConnectESMB
    ${expect_ESMB_up_time} =  get_esm_up_time  DUT
    #Step  4  Disconnect
    Step  4  OS Disconnect Device
    verify_ses_page_04_lenovo  %{DUT_username}  %{DUT_ipv4_ip}  %{DUT_password}  ${sg_device_1}  ${expect_ESMA_IP_lenovo}  ${expect_gateway_lenovo}
          ...  ${expect_ESM_A_DHCP_Mode_lenovo}  ${expect_ESMA_up_time}   ${expect_ESMB_up_time}  ${expect_ESM_Zoning_Mode}   ${expect_ESMB_IP_lenovo}  ${expect_ESM_B_DHCP_Mode_lenovo}  ${expect_netmask}

check String In Diagnostic Pages(04h) kiwi
    ${sg_device_1} =  get_devicename  %{DUT_username}  %{DUT_ipv4_ip}  %{DUT_password}
    Step  1  ESMAConnect  ${ESMA IP}  ${ESMA port}
    ${expect_ESMA_up_time} =  get_esm_up_time  DUT
    Step  2  Disconnect
    verify_ses_page_04_kiwi  %{DUT_username}  %{DUT_ipv4_ip}  %{DUT_password}  ${sg_device_1}  ${expect_ESMA_IP_lenovo}  ${expect_gateway_lenovo}
          ...  ${expect_ESM_A_DHCP_Mode_lenovo}  ${expect_ESMA_up_time}   ${expect_ESM_Zoning_Mode}   ${expect_netmask}

Read VPD from one canister with 0x10 Diag page
    ${sg_device_1} =  get_devicename  %{DUT_username}  %{DUT_ipv4_ip}  %{DUT_password}  Zone1
    ${ses_fw_version} =  get_ses_fw_version_by_ses_page_01h  %{DUT_username}  %{DUT_ipv4_ip}  %{DUT_password}  ${sg_device_1}
    Step  1  Lenovo_JBOD_via_ses_command  %{DUT_username}  %{DUT_ipv4_ip}  %{DUT_password}  ${sg_pg10_diag_cmd1}  ${sg_device_1}
    Step  2  create_gold_file  %{DUT_username}  %{DUT_ipv4_ip}  %{DUT_password}  sg_ses -p 0x10 ${sg_device_1}  ${ses_page_10h_gold_file_tmp}
    Step  3  compare_file  ${ses_page_10h_gold_file_1}  ${ses_page_10h_gold_file_tmp}  ses_page_10

Read VPD from two canister with 0x10 Diag page
    ${sg_device_1} =  get_devicename  %{DUT_username}  %{DUT_ipv4_ip}  %{DUT_password}  Zone1
    ${sg_device_2} =  get_devicename  %{DUT_username}  %{DUT_ipv4_ip}  %{DUT_password}  Zone2
    Step  1  Lenovo_JBOD_via_ses_command  %{DUT_username}  %{DUT_ipv4_ip}  %{DUT_password}  ${sg_pg10_diag_cmd1}  ${sg_device_1}
    Step  2  create_gold_file  %{DUT_username}  %{DUT_ipv4_ip}  %{DUT_password}  sg_ses -p 0x10 ${sg_device_1}  ${ses_page_10h_gold_file_tmp}
    Step  3  compare_file  ${ses_page_10h_gold_file_1}  ${ses_page_10h_gold_file_tmp}  ses_page_10
    Step  4  Lenovo_JBOD_via_ses_command  %{DUT_username}  %{DUT_ipv4_ip}  %{DUT_password}  ${sg_pg10_diag_cmd1}  ${sg_device_2}
    Step  5  create_gold_file  %{DUT_username}  %{DUT_ipv4_ip}  %{DUT_password}  sg_ses -p 0x10 ${sg_device_2}  ${ses_page_10h_gold_file_tmp}
    Step  6  compare_file  ${ses_page_10h_gold_file_2}  ${ses_page_10h_gold_file_tmp}  ses_page_10

Read VPD from one canister with 0x17 Diag page
    ${sg_device_1} =  get_devicename  %{DUT_username}  %{DUT_ipv4_ip}  %{DUT_password}  Zone1
    ${ses_fw_version} =  get_ses_fw_version_by_ses_page_01h  %{DUT_username}  %{DUT_ipv4_ip}  %{DUT_password}  ${sg_device_1}
    Step  1  Lenovo_JBOD_via_ses_command  %{DUT_username}  %{DUT_ipv4_ip}  %{DUT_password}  ${sg_pg17_diag_cmd1}  ${sg_device_1}
    Step  2  create_gold_file  %{DUT_username}  %{DUT_ipv4_ip}  %{DUT_password}  sg_ses -p 0x17 ${sg_device_1}  ${ses_page_17h_gold_file_tmp}
    Step  3  compare_file  ${ses_page_17h_gold_file_1}  ${ses_page_17h_gold_file_tmp}  ses_page_17

Read VPD from two canister with 0x17 Diag page
    ${sg_device_1} =  get_devicename  %{DUT_username}  %{DUT_ipv4_ip}  %{DUT_password}  Zone1
    ${sg_device_2} =  get_devicename  %{DUT_username}  %{DUT_ipv4_ip}  %{DUT_password}  Zone2
    Step  1  Lenovo_JBOD_via_ses_command  %{DUT_username}  %{DUT_ipv4_ip}  %{DUT_password}  ${sg_pg17_diag_cmd1}  ${sg_device_1}
    Step  2  create_gold_file  %{DUT_username}  %{DUT_ipv4_ip}  %{DUT_password}  sg_ses -p 0x17 ${sg_device_1}  ${ses_page_17h_gold_file_tmp}
    Step  3  compare_file  ${ses_page_17h_gold_file_1}  ${ses_page_17h_gold_file_tmp}  ses_page_17
    Step  4  Lenovo_JBOD_via_ses_command  %{DUT_username}  %{DUT_ipv4_ip}  %{DUT_password}  ${sg_pg17_diag_cmd1}  ${sg_device_2}
    Step  5  create_gold_file  %{DUT_username}  %{DUT_ipv4_ip}  %{DUT_password}  sg_ses -p 0x17 ${sg_device_2}  ${ses_page_17h_gold_file_tmp}
    Step  6  compare_file  ${ses_page_17h_gold_file_2}  ${ses_page_17h_gold_file_tmp}  ses_page_17

Create ses Diag page gold file
    server Connect 1
    execute_Linux_command  rm -f ses_page_10h_gold_file_*
    execute_Linux_command  rm -f ses_page_17h_gold_file_*
    server Disconnect
    ${sg_device_1} =  get_devicename  %{DUT_username}  %{DUT_ipv4_ip}  %{DUT_password}  Zone1
    ${sg_device_2} =  get_devicename  %{DUT_username}  %{DUT_ipv4_ip}  %{DUT_password}  Zone2
    ${ses_fw_version} =  get_ses_fw_version_by_ses_page_01h  %{DUT_username}  %{DUT_ipv4_ip}  %{DUT_password}  ${sg_device_1}
    ${cpld_version_1} =  get_cpld_version_ses_page  %{DUT_username}  %{DUT_ipv4_ip}  %{DUT_password}  ${sg_device_1}  isUpgrade=True
    ${cpld_version_2} =  get_cpld_version_ses_page  %{DUT_username}  %{DUT_ipv4_ip}  %{DUT_password}  ${sg_device_1}  isUpgrade=False
    Step  1  Lenovo_JBOD_via_ses_command  %{DUT_username}  %{DUT_ipv4_ip}  %{DUT_password}  ${sg_pg10_diag_cmd1}  ${sg_device_1}
    Step  2  create_gold_file  %{DUT_username}  %{DUT_ipv4_ip}  %{DUT_password}  sg_ses -p 0x10 ${sg_device_1}  ${ses_page_10h_gold_file_1}
    Step  3  Lenovo_JBOD_via_ses_command  %{DUT_username}  %{DUT_ipv4_ip}  %{DUT_password}  ${sg_pg10_diag_cmd1}  ${sg_device_2}
    Step  4  create_gold_file  %{DUT_username}  %{DUT_ipv4_ip}  %{DUT_password}  sg_ses -p 0x10 ${sg_device_2}  ${ses_page_10h_gold_file_2}
    Step  5  Lenovo_JBOD_via_ses_command  %{DUT_username}  %{DUT_ipv4_ip}  %{DUT_password}  ${sg_pg17_diag_cmd1}  ${sg_device_1}
    Step  6  create_gold_file  %{DUT_username}  %{DUT_ipv4_ip}  %{DUT_password}  sg_ses -p 0x17 ${sg_device_1}  ${ses_page_17h_gold_file_1}
    Step  7  Lenovo_JBOD_via_ses_command  %{DUT_username}  %{DUT_ipv4_ip}  %{DUT_password}  ${sg_pg17_diag_cmd1}  ${sg_device_2}
    Step  8  create_gold_file  %{DUT_username}  %{DUT_ipv4_ip}  %{DUT_password}  sg_ses -p 0x17 ${sg_device_2}  ${ses_page_17h_gold_file_2}

Compare ses Diag page gold file
    ${sg_device_1} =  get_devicename  %{DUT_username}  %{DUT_ipv4_ip}  %{DUT_password}  Zone1
    ${sg_device_2} =  get_devicename  %{DUT_username}  %{DUT_ipv4_ip}  %{DUT_password}  Zone2
    ${ses_fw_version} =  get_ses_fw_version_by_ses_page_01h  %{DUT_username}  %{DUT_ipv4_ip}  %{DUT_password}  ${sg_device_1}
    ${cpld_version_1} =  get_cpld_version_ses_page  %{DUT_username}  %{DUT_ipv4_ip}  %{DUT_password}  ${sg_device_1}  isUpgrade=True
    ${cpld_version_2} =  get_cpld_version_ses_page  %{DUT_username}  %{DUT_ipv4_ip}  %{DUT_password}  ${sg_device_1}  isUpgrade=False
    Step  1  Lenovo_JBOD_via_ses_command  %{DUT_username}  %{DUT_ipv4_ip}  %{DUT_password}  ${sg_pg10_diag_cmd1}  ${sg_device_1}
    Step  2  create_gold_file  %{DUT_username}  %{DUT_ipv4_ip}  %{DUT_password}  sg_ses -p 0x10 ${sg_device_1}  ${ses_page_10h_gold_file_tmp}
    Step  3  compare_file  ${ses_page_10h_gold_file_1}  ${ses_page_10h_gold_file_tmp}  ses_page_10
    Step  4  Lenovo_JBOD_via_ses_command  %{DUT_username}  %{DUT_ipv4_ip}  %{DUT_password}  ${sg_pg10_diag_cmd1}  ${sg_device_2}
    Step  5  create_gold_file  %{DUT_username}  %{DUT_ipv4_ip}  %{DUT_password}  sg_ses -p 0x10 ${sg_device_2}  ${ses_page_10h_gold_file_tmp}
    Step  6  compare_file  ${ses_page_10h_gold_file_2}  ${ses_page_10h_gold_file_tmp}  ses_page_10
    #sleep  60
    Step  7  Lenovo_JBOD_via_ses_command  %{DUT_username}  %{DUT_ipv4_ip}  %{DUT_password}  ${sg_pg17_diag_cmd1}  ${sg_device_1}
    Step  8  create_gold_file  %{DUT_username}  %{DUT_ipv4_ip}  %{DUT_password}  sg_ses -p 0x17 ${sg_device_1}  ${ses_page_17h_gold_file_tmp}
    Step  9  compare_file  ${ses_page_17h_gold_file_1}  ${ses_page_17h_gold_file_tmp}  ses_page_17
    #sleep  60
    Step  10  Lenovo_JBOD_via_ses_command  %{DUT_username}  %{DUT_ipv4_ip}  %{DUT_password}  ${sg_pg17_diag_cmd1}  ${sg_device_2}
    Step  11  create_gold_file  %{DUT_username}  %{DUT_ipv4_ip}  %{DUT_password}  sg_ses -p 0x17 ${sg_device_2}  ${ses_page_17h_gold_file_tmp}
    Step  12  compare_file  ${ses_page_17h_gold_file_2}  ${ses_page_17h_gold_file_tmp}  ses_page_17

verify processors information
   [Arguments]   ${expected_cpu_model_name}    ${expected_BIOS_Model_name}
   ${cpu_info} =  execute_Linux_command    lscpu | grep "Model name"
   common_check_patern_2    ${cpu_info}    ${expected_cpu_model_name}    verify_processor_info   expect=True
   common_check_patern_2    ${cpu_info}    ${expected_BIOS_Model_name}   verify_processor_info   expect=True

verify memory serial presence detect
   [Arguments]   ${expected_part_number1}    ${expected_part_number2}
   ${part_number} =   execute_Linux_command    dmidecode -t 17 | grep "Part Number"
   common_check_patern_2    ${part_number}   ${expected_part_number1}  verify_part_number  expect=True
   common_check_patern_2    ${part_number}   ${expected_part_number2}  verify_part_number  expect=True

verify USB Link Speeed
   [Arguments]   ${expected_usb_link_speed}
   ${usb_link_speed} =   execute_Linux_command  lsusb -t
   common_check_patern_2    ${usb_link_speed}    ${expected_usb_link_speed}   verify_usb_link_speed   expect=True

verify memory information
   [Arguments]   ${expected_memory_info}
   ${memory_info} =  execute_Linux_command    cat /proc/meminfo | grep MemTotal
   common_check_patern_2    ${memory_info}    ${expected_memory_info}    verify_memory_information   expect=True

verify USB Devices
   [Arguments]   ${expected_USB_Devices1}    ${expected_USB_Devices2}    ${expected_USB_Devices3}
   ${usb_device_info} =   execute_Linux_command  lsusb
   common_check_patern_2    ${usb_device_info}    ${expected_USB_Devices1}    verify_usb_device1   expect=True
   common_check_patern_2    ${usb_device_info}    ${expected_USB_Devices2}    verify_usb_device2   expect=True
   common_check_patern_2    ${usb_device_info}    ${expected_USB_Devices3}    verify_usb_device3   expect=True

verify the number of PCIE devices
   [Arguments]   ${expected_number_PCIE_devices}
   ${PCIE_devices_count} =   execute_Linux_command  lspci | wc -l
   common_check_patern_2    ${PCIE_devices_count}    ${expected_number_PCIE_devices}    verify_the_number_of_PCIE_Devices   expect=True

verify PCIE device id information
   [Arguments]   ${PCIE_device_id}    ${PCIE_device_info}
       FOR  ${id}  IN  @{PCIE_device_id}
           Log    ${id}
           ${PCIE_devices_id_output} =   execute_Linux_command  lspci -s ${id}
           common_check_patern_2    ${PCIE_devices_id_output}    ${PCIE_device_info}    verify_PCIE_device_${id}_information   expect=True
       END

verify BMC sub system sensor reading
  ${sensor_check} =   execute_Linux_command  ipmitool sensor list
  common_check_patern_2   ${sensor_check}  Abnormal   check sensor list  expect=False
  common_check_patern_2   ${sensor_check}  fault   check sensor list  expect=False
  common_check_patern_2   ${sensor_check}  warning  check sensor list  expect=False
  common_check_patern_2   ${sensor_check}  fail   check sensor list  expect=False
  common_check_patern_2   ${sensor_check}  Error  check sensor list  expect=False

verify UUID_serialnumber
  [Arguments]   ${expected_serial_number}
  ${UUID_serialnumber} =   execute_Linux_command  dmidecode -t 1 | grep -i serial
  common_check_patern_2     ${UUID_serialnumber}  ${expected_serial_number}   verify_serial_number   expect=True

verify mc_info before and after warm reset
   ${mc_info_output_before_reset} =  execute_Linux_command  ipmitool mc info
   ${reset_output} =    execute_Linux_command  ipmitool mc reset warm
   common_check_patern_2    ${reset_output}     Sent warm reset command to MC      check warm reset command   expect=True
   Sleep  120
   ${mc_info_output_after_reset} =  execute_Linux_command  ipmitool mc info
   compare_mc_info_before_and_after_reset    ${mc_info_output_before_reset}     ${mc_info_output_after_reset}

BMC time check
    ${time_output} =  execute_Linux_command   ipmitool sel time get
    common_check_patern_2  ${time_output}  Error   Check error message  expect=False
    common_check_patern_2  ${time_output}  Invalid SEL command   Check error message  expect=False
    ${date_output} =  execute_Linux_command   date
    common_check_patern_2  ${date_output}  Error  Check error message  expect=False
    common_check_patern_2  ${date_output}  Fail   Check error message  expect=False
    execute_Linux_command   ipmitool sel time set "2/15/2022 21:26:00"
    ${SEL_time_output} =  execute_Linux_command   ipmitool sel time get
    common_check_patern_2    ${SEL_time_output}  2.*15.*2022 21.*26  check in sel time get command   expect=True
    ${current_time} =  getcurrenttime
    Sleep  30
    execute_Linux_command   ipmitool sel time set "${current_time}"
    ${time_output} =  execute_Linux_command   ipmitool sel time get
    Log   ${time_output}

Download PSU image File lenovo
    Server Connect 1
    download PSU Fw Image  upgrade=True
    download PSU Fw Image  upgrade=False
    server Disconnect

Remove Lenovo PSU image
    Server Connect 1
    RemoveAthenaSesFwImage    DUT   PSU
    OS Disconnect Device

PSU Download microcode Control Diagnostic Page Lenovo ESM-A - mode e
    [Arguments]    ${isupgrade}
    Server Connect 1
    ${prim_dev} =   get_primary_device
    Set Suite Variable  ${prim_dev}
    ${prim_dev_ESMB} =   get_non_primary_device
    Set Suite Variable  ${prim_dev_ESMB}
    server Disconnect
    #ESMAConnect  ${ESMA IP}  ${ESMA port}
    OS Connect Device
    ${fru_get_output}=   run ESM command    fru get
    Log   ${fru_get_output}
    ${ps_hardware} =  get_ps_hardware    ${fru_get_output}
    Log   ${ps_hardware}
    ${image_to_upgrade} =   GetCanisterImageName   ${ps_hardware}   PSU   ${isupgrade}
    Log  ${image_to_upgrade}
    ${psu_version} =  GetPSUVersion  PSU   ${isupgrade}
    Log  ${psu_version}
    OS Disconnect Device
    Server Connect 1
    ${imageoutput} =   whitebox_lib.execute  DUT  sg_ses_microcode -m 0xe -b 4096 -I ${image_to_upgrade} -i 5 ${prim_dev}
    Log  ${imageoutput}
    ${output} =  execute_Linux_command1  sg_ses -p 0xe ${prim_dev}
    Log  ${output}
    set time delay  120
    ${output} =  execute_Linux_command1  sg_ses -p 0xe ${prim_dev}
    Log  ${output}
    common_check_patern_2    ${output}  download microcode status: No download microcode operation in progress   verify the completion of FW download    expect=True
    ${output} =  execute_Linux_command   sg_ses -p 7 ${prim_dev}
    common_check_patern_2    ${output}     Element 0 descriptor: PSU1.*${psu_version}    verison_check_in_psu1_ESM-A  expect=False
    common_check_patern_2    ${output}     Element 1 descriptor: PSU2.*${psu_version}    verison_check_in_psu2_ESM-A   expect=False
    server Disconnect
    #ESMAConnect  ${ESMA IP}  ${ESMA port}
    OS Connect Device
    ${fru_get_output}=   run ESM command    fru get
    Log   ${fru_get_output}
    common_check_patern_2  ${fru_get_output}   ${psu_version}    check_psu_version_ESM-A  expect=False
    OS Disconnect Device

PSU Download microcode Control Diagnostic Page Lenovo ESM-A - mode f
    [Arguments]    ${isupgrade}    ${isdowngrade}
    Server Connect 1
    ${prim_dev} =   get_primary_device
    Set Suite Variable  ${prim_dev}
    server Disconnect
    #ESMAConnect  ${ESMA IP}  ${ESMA port}
    OS Connect Device
    ${psu_version} =  GetPSUVersion  PSU   ${isupgrade}
    Log  ${psu_version}
    ${psu_version_old} =  GetPSUVersion  PSU   ${isdowngrade}
    Log  ${psu_version_old}
    OS Disconnect Device
    Server Connect 1
    whitebox_lib.execute  DUT  sg_ses_microcode -m 0xf -i 5 ${prim_dev}
    set time delay  1500
    execute_Linux_command1  sg_ses -p 0xe ${prim_dev}
    set time delay  100
    execute_Linux_command1  sg_ses -p 0xe ${prim_dev}
    set time delay  100
    execute_Linux_command1  sg_ses -p 0xe ${prim_dev}
    set time delay  100
    ${output} =  execute_Linux_command1  sg_ses -p 0xe ${prim_dev}
    Log  ${output}
    common_check_patern_2    ${output}  download microcode status: No download microcode operation in progress   verify the completion of FW download    expect=True
    ${output} =  execute_Linux_command1   sg_ses -p 7 ${prim_dev}
    common_check_patern_2    ${output}     Element 0 descriptor: PSU.*1.*${psu_version}    verison_check_in_psu1_ESM-A  expect=True
    common_check_patern_2    ${output}     Element 1 descriptor: PSU.*2.*${psu_version}    verison_check_in_psu2_ESM-A   expect=True
    common_check_patern_2    ${output}     Element 0 descriptor: PSU.*1.*${psu_version_old}    verison_check_in_psu1_ESM-A  expect=False
    common_check_patern_2    ${output}     Element 1 descriptor: PSU.*2.*${psu_version_old}    verison_check_in_psu2_ESM-A   expect=False
    server Disconnect
    #ESMAConnect  ${ESMA IP}  ${ESMA port}
    OS Connect Device
    ${fru_get_output}=   run ESM command    fru get
    Log   ${fru_get_output}
    OS Disconnect Device
    common_check_patern_2  ${fru_get_output}   ${psu_version}    check_psu_version_ESM-A  expect=True
    common_check_patern_2  ${fru_get_output}   ${psu_version_old}    check_psu_version_ESM-A  expect=False

PSU Download microcode Control Diagnostic Page Lenovo ESM-A - mode 7
    [Arguments]    ${isupgrade}    ${isdowngrade}
    Server Connect 1
    ${prim_dev} =   get_primary_device
    Set Suite Variable  ${prim_dev}
    server Disconnect
    #ESMAConnect  ${ESMA IP}  ${ESMA port}
    OS Connect Device
    ${fru_get_output}=   run ESM command    fru get
    Log   ${fru_get_output}
    ${ps_hardware} =  get_ps_hardware    ${fru_get_output}
    Log   ${ps_hardware}
    ${image_to_upgrade} =   GetCanisterImageName   ${ps_hardware}   PSU   ${isupgrade}
    Log  ${image_to_upgrade}
    ${psu_version_expected} =  GetPSUVersion  PSU   ${isupgrade}
    Log  ${psu_version_expected}
    ${psu_version_old} =  GetPSUVersion  PSU   ${isdowngrade}
    Log  ${psu_version_old}
    #${image_to_upgrade}    ${psu_version_expected} =   GetCanisterUpdateImageName   ${ps_hardware}   PSU   ${psu_version}
    #Log  ${image_to_upgrade}
    ${image_to_upgrade} =   GetCanisterImageName   ${ps_hardware}   PSU   ${isupgrade}
    Log  ${image_to_upgrade}
    #Log  ${psu_version_expected}
    OS Disconnect Device
    Server Connect 1
    whitebox_lib.execute  DUT  sg_ses_microcode -m 0x7 -b 4096 -I ${image_to_upgrade} -i 5 ${prim_dev}
    set time delay  1500
    ${output} =  execute_Linux_command1  sg_ses -p 0xe ${prim_dev}
    Log  ${output}
    set time delay  200
    ${output} =  execute_Linux_command1  sg_ses -p 0xe ${prim_dev}
    Log  ${output}
    common_check_patern_2    ${output}  download microcode status: No download microcode operation in progress   verify the completion of FW download ESM-A    expect=True
    ${output} =  execute_Linux_command1   sg_ses -p 7 ${prim_dev}
    common_check_patern_2    ${output}     Element 0 descriptor: PSU.*1.*${psu_version_expected}    version_check_in_psu1_ESM-A   expect=True
    common_check_patern_2    ${output}     Element 1 descriptor: PSU.*2.*${psu_version_expected}    version_check_in_psu2_ESM-A   expect=True
    common_check_patern_2    ${output}     ${psu_version_old}    version_check_in_psu1   expect=False
    server Disconnect
    #ESMAConnect  ${ESMA IP}  ${ESMA port}
    OS Connect Device
    ${fru_get_output}=   run ESM command    fru get
    Log   ${fru_get_output}
    common_check_patern_2  ${fru_get_output}   ${psu_version_old}    check_psu_version_ESM-A  expect=False
    OS Disconnect Device

PSU Download microcode Control Diagnostic Page Lenovo ESM-B - mode e
    [Arguments]    ${isupgrade}
    Server Connect 1
    ${prim_dev} =   get_primary_device
    Set Suite Variable  ${prim_dev}
    ${prim_dev_ESMB} =   get_non_primary_device
    Set Suite Variable  ${prim_dev_ESMB}
    server Disconnect
    #ESMAConnect  ${ESMB IP}  ${ESMB port}
    ConnectESMB
    ${fru_get_output}=   run ESM command    fru get
    Log   ${fru_get_output}
    ${ps_hardware} =  get_ps_hardware    ${fru_get_output}
    Log   ${ps_hardware}
    ${image_to_upgrade} =   GetCanisterImageName   ${ps_hardware}   PSU   ${isupgrade}
    Log  ${image_to_upgrade}
    ${psu_version} =  GetPSUVersion  PSU   ${isupgrade}
    Log  ${psu_version}
    OS Disconnect Device
    Server Connect 1
    ${imageoutput} =   whitebox_lib.execute  DUT  sg_ses_microcode -m 0xe -b 4096 -I ${image_to_upgrade} -i 5 ${prim_dev_ESMB}
    Log  ${imageoutput}
    ${output} =  execute_Linux_command1  sg_ses -p 0xe ${prim_dev_ESMB}
    Log  ${output}
    set time delay  120
    ${output} =  execute_Linux_command1  sg_ses -p 0xe ${prim_dev_ESMB}
    Log  ${output}
    common_check_patern_2    ${output}  download microcode status: No download microcode operation in progress   verify the completion of FW download ESM-B    expect=True
    ${output} =  execute_Linux_command   sg_ses -p 7 ${prim_dev_ESMB}
    common_check_patern_2    ${output}     Element 0 descriptor: PSU1.*${psu_version}    verison_check_in_psu1_ESM-B  expect=False
    common_check_patern_2    ${output}     Element 1 descriptor: PSU2.*${psu_version}    verison_check_in_psu2_ESM-B   expect=False
    server Disconnect
    #ESMAConnect  ${ESMB IP}  ${ESMB port}
    ConnectESMB
    ${fru_get_output}=   run ESM command    fru get
    Log   ${fru_get_output}
    common_check_patern_2  ${fru_get_output}   ${psu_version}    check_psu_version_ESM-B  expect=False
    OS Disconnect Device

PSU Download microcode Control Diagnostic Page Lenovo ESM-B - mode f
    [Arguments]    ${isupgrade}    ${isdowngrade}
    Server Connect 1
    ${prim_dev} =   get_primary_device
    Set Suite Variable  ${prim_dev}
    ${prim_dev_ESMB} =   get_non_primary_device
    Set Suite Variable  ${prim_dev_ESMB}
    server Disconnect
    #ESMAConnect  ${ESMB IP}  ${ESMB port}
    ConnectESMB
    ${psu_version} =  GetPSUVersion  PSU   ${isupgrade}
    Log  ${psu_version}
    ${psu_version_old} =  GetPSUVersion  PSU   ${isdowngrade}
    Log  ${psu_version_old}
    OS Disconnect Device
    Server Connect 1
    whitebox_lib.execute  DUT  sg_ses_microcode -m 0xf -i 5 ${prim_dev_ESMB}
    set time delay  1500
    execute_Linux_command1  sg_ses -p 0xe ${prim_dev_ESMB}
    set time delay  100
    execute_Linux_command1  sg_ses -p 0xe ${prim_dev_ESMB}
    set time delay  100
    execute_Linux_command1  sg_ses -p 0xe ${prim_dev_ESMB}
    set time delay  100
    ${output} =  execute_Linux_command1  sg_ses -p 0xe ${prim_dev_ESMB}
    Log  ${output}
    common_check_patern_2    ${output}  download microcode status: No download microcode operation in progress   verify the completion of FW download ESM-B    expect=True
    ${output} =  execute_Linux_command1   sg_ses -p 7 ${prim_dev_ESMB}
    common_check_patern_2    ${output}     Element 0 descriptor: PSU.*1.*${psu_version}    verison_check_in_psu1_ESM-B  expect=True
    common_check_patern_2    ${output}     Element 1 descriptor: PSU.*2.*${psu_version}    verison_check_in_psu2_ESM-B   expect=True
    common_check_patern_2    ${output}     Element 0 descriptor: PSU.*1.*${psu_version_old}    verison_check_in_psu1_ESM-B  expect=False
    common_check_patern_2    ${output}     Element 1 descriptor: PSU.*2.*${psu_version_old}    verison_check_in_psu2_ESM-B   expect=False
    server Disconnect
    #ESMAConnect  ${ESMB IP}  ${ESMB port}
    ConnectESMB
    ${fru_get_output}=   run ESM command    fru get
    Log   ${fru_get_output}
    OS Disconnect Device
    common_check_patern_2  ${fru_get_output}   ${psu_version}    check_psu_version_ESM-B  expect=True
    common_check_patern_2  ${fru_get_output}   ${psu_version_old}    check_psu_version_ESM-B  expect=False

PSU Download microcode Control Diagnostic Page Lenovo ESM-B - mode 7
    [Arguments]    ${isupgrade}    ${isdowngrade}
    Server Connect 1
    ${prim_dev} =   get_primary_device
    Set Suite Variable  ${prim_dev}
    ${prim_dev_ESMB} =   get_non_primary_device
    Set Suite Variable  ${prim_dev_ESMB}
    server Disconnect
    #ESMAConnect  ${ESMB IP}  ${ESMB port}
    ConnectESMB
    ${fru_get_output}=   run ESM command    fru get
    Log   ${fru_get_output}
    ${ps_hardware} =  get_ps_hardware    ${fru_get_output}
    Log   ${ps_hardware}
    ${image_to_upgrade} =   GetCanisterImageName   ${ps_hardware}   PSU   ${isupgrade}
    Log  ${image_to_upgrade}
    ${psu_version_expected} =  GetPSUVersion  PSU   ${isupgrade}
    Log  ${psu_version_expected}
    ${psu_version_old} =  GetPSUVersion  PSU   ${isdowngrade}
    Log  ${psu_version_old}
    #${image_to_upgrade}    ${psu_version_expected} =   GetCanisterUpdateImageName   ${ps_hardware}   PSU   ${psu_version}
    #Log  ${image_to_upgrade}
    ${image_to_upgrade} =   GetCanisterImageName   ${ps_hardware}   PSU   ${isupgrade}
    Log  ${image_to_upgrade}
    #Log  ${psu_version_expected}
    OS Disconnect Device
    Server Connect 1
    whitebox_lib.execute  DUT  sg_ses_microcode -m 0x7 -b 4096 -I ${image_to_upgrade} -i 5 ${prim_dev_ESMB}
    set time delay  1500
    ${output} =  execute_Linux_command1  sg_ses -p 0xe ${prim_dev_ESMB}
    Log  ${output}
    set time delay  200
    ${output} =  execute_Linux_command1  sg_ses -p 0xe ${prim_dev_ESMB}
    Log  ${output}
    common_check_patern_2    ${output}  download microcode status: No download microcode operation in progress   verify the completion of FW download ESM-A    expect=True
    ${output} =  execute_Linux_command1   sg_ses -p 7 ${prim_dev_ESMB}
    common_check_patern_2    ${output}     Element 0 descriptor: PSU.*1.*${psu_version_expected}    version_check_in_psu1_ESM-B   expect=True
    common_check_patern_2    ${output}     Element 1 descriptor: PSU.*2.*${psu_version_expected}    version_check_in_psu2_ESM-B   expect=True
    common_check_patern_2    ${output}     ${psu_version_old}    version_check_in_psu1_ESM-B   expect=False
    server Disconnect
    #ESMAConnect  ${ESMB IP}  ${ESMB port}
    ConnectESMB
    ${fru_get_output}=   run ESM command    fru get
    Log   ${fru_get_output}
    common_check_patern_2  ${fru_get_output}   ${psu_version_old}    check_psu_version_ESM-B  expect=False
    OS Disconnect Device

verify drive count after ses reset ESMA
   server Connect
   ${drive_count_before_reset} =   Get Total Number Of Drives
   Log   ${drive_count_before_reset}
   Server Disconnect
   OS Connect Device
   change_to_ESM_mode
   execute_ESM_command_1   reset 1
   set time delay   300
   exit_ESM_mode
   OS Disconnect Device
   server Connect
   ${drive_count_after_reset} =  Get Total Number Of Drives
   Log   ${drive_count_after_reset}
   Should Be Equal  ${drive_count_before_reset}    ${drive_count_after_reset}
   Server Disconnect

verify drive count after ses reset ESMB
   server Connect ESMB
   ${drive_count_before_reset} =   Get Total Number Of Drives
   Log   ${drive_count_before_reset}
   Server Disconnect
   ConnectESMB
   change_to_ESM_mode
   execute_ESM_command_1   reset 1
   set time delay   60
   exit_ESM_mode
   OS Disconnect Device
   server Connect ESMB
   ${drive_count_after_reset} =  Get Total Number Of Drives
   Log   ${drive_count_after_reset}
   Should Be Equal  ${drive_count_before_reset}    ${drive_count_after_reset}
   Server Disconnect

verify BMC Power Reset on both ESMs
    server Connect
    ${Before_drive_count} =   getNumberOfDrives
    Log  ${Before_drive_count}
    ${Before_PCIE_count} =   getNumberOfPCIEDrives
    Log  ${Before_PCIE_count}
    ${power_reset_output} =    execute_Linux_command  ipmitool power reset
    common_check_patern_2    ${power_reset_output}     Chassis Power Control: Reset      verify power reset command   expect=True
    Server Disconnect
    set time delay  300
    server Connect
    ${After_drive_count} =   getNumberOfDrives
    Log  ${After_drive_count}
    ${After_PCIE_count} =   getNumberOfPCIEDrives
    Log  ${After_PCIE_count}
    Should Be Equal As Strings    ${Before_drive_count}    ${After_drive_count}
    Should Be Equal  ${Before_PCIE_count}    ${After_PCIE_count}
    Server Disconnect	
    server Connect ESMB
    ${Before_drive_count} =   getNumberOfDrives
    Log  ${Before_drive_count}
    ${Before_PCIE_count} =   getNumberOfPCIEDrives
    Log  ${Before_PCIE_count}
    ${power_reset_output} =    execute_Linux_command  ipmitool power reset
    common_check_patern_2    ${power_reset_output}     Chassis Power Control: Reset      verify power reset command   expect=True
    Server Disconnect
    set time delay  300
    server Connect ESMB
    ${After_drive_count} =   getNumberOfDrives
    Log  ${After_drive_count}
    ${After_PCIE_count} =   getNumberOfPCIEDrives
    Log  ${After_PCIE_count}
    Should Be Equal As Strings    ${Before_drive_count}    ${After_drive_count}
    Should Be Equal  ${Before_PCIE_count}    ${After_PCIE_count}
    Server Disconnect

verify Sensor Status via ipmitool
    ${Sensor_Status_Output} =   execute_Linux_command  ipmitool sdr list
    common_check_patern_2   ${Sensor_Status_Output}  Abnormal   check sensor list  expect=False
    common_check_patern_2   ${Sensor_Status_Output}  fault   check sensor list  expect=False
    common_check_patern_2   ${Sensor_Status_Output}  warning  check sensor list  expect=False
    common_check_patern_2   ${Sensor_Status_Output}  fail   check sensor list  expect=False
    common_check_patern_2   ${Sensor_Status_Output}  Error  check sensor list  expect=False

verify esm details
    ${sg_device_1} =  get_devicename  %{DUT_username}  %{DUT_ipv4_ip}  %{DUT_password}  Zone1
    Log  ${sg_device_1}
    ${sg_device_2} =  get_devicename  %{DUT_username}  %{DUT_ipv4_ip}  %{DUT_password}  Zone2
    Log  ${sg_device_2}
    ${prim_dev} =   get_primary_device
    Log  ${prim_dev}
    ${prim_dev_ESMB} =   get_non_primary_device
    Log  ${prim_dev_ESMB}

downgrade FW with mode 0xe + reset 00h code Lenovo
    Server Connect 1
    ${prim_dev} =   get_primary_device
    Log  ${prim_dev}
    ${non_prim_dev} =   get_non_primary_device
    Log  ${non_prim_dev}
    server Disconnect
    Step  1  downgrade whitebox FW with mode 0xe ESM A  ${prim_dev}
    Step  2  activitate whitebox FW reset 00h ESM A  ${prim_dev}
    Step  3  check downgrade FW version ESM A 
    Server Connect 1
    ${non_prim_dev} =   get_non_primary_device
    Log  ${non_prim_dev}
    server Disconnect
    Step  4  downgrade whitebox FW with mode 0xe ESM B  ${non_prim_dev}
    Step  5  activitate whitebox FW reset 00h ESM B  ${non_prim_dev}
    Step  6  check downgrade FW version ESM B
    Server Connect 1
    ${prim_dev} =   get_primary_device
    Log  ${prim_dev}
    ${non_prim_dev} =   get_non_primary_device
    Log  ${non_prim_dev}
    server Disconnect

downgrade whitebox FW with mode 0xe ESM A 
    [Arguments]    ${sg_device_1}
    Step  1  update_whitebox_fw_force  SES  ${download_microcode_modeE_cmd}  %{DUT_username}  %{DUT_ipv4_ip}  %{DUT_password}  ${sg_device_1}  isUpgrade=False    
	
activitate whitebox FW reset 00h ESM A
    [Arguments]    ${sg_device_1}
    Step  1  ses_activitate  %{DUT_username}  %{DUT_ipv4_ip}  %{DUT_password}  ${sg_device_1}  00h
    Step  2  set time delay  120

check downgrade FW version ESM A 
    #Step  1  ESMAConnect  ${ESMA IP}  ${ESMA port}
    Step  1  OS Connect Device
    Step  2  verify_ses_version_fru_get  DUT  isUpgrade=False
    Step  3  OS Disconnect Device

downgrade whitebox FW with mode 0xe ESM B
    [Arguments]    ${sg_device_2}
    Step  1  update_whitebox_fw_force  SES  ${download_microcode_modeE_cmd}  %{DUT_username}  %{DUT_ipv4_ip}  %{DUT_password}  ${sg_device_2}  isUpgrade=False    
	
activitate whitebox FW reset 00h ESM B
    [Arguments]    ${sg_device_2}
    Step  1  ses_activitate  %{DUT_username}  %{DUT_ipv4_ip}  %{DUT_password}  ${sg_device_2}  00h
    Step  2  set time delay  120

check downgrade FW version ESM B
    Step  1  ConnectESMB
    Step  2  verify_ses_version_fru_get  DUT  isUpgrade=False
    Step  3  OS Disconnect Device

upgrade FW with mode 0xe + reset 00h code Lenovo
    Server Connect 1
    ${prim_dev} =   get_primary_device
    Log  ${prim_dev}
    ${non_prim_dev} =   get_non_primary_device
    Log  ${non_prim_dev}
    server Disconnect
    Step  1  upgrade whitebox FW with mode 0xe ESM A  ${prim_dev}
    Step  2  activitate whitebox FW reset 00h ESM A  ${prim_dev}
    Step  3  check upgrade FW version ESM A 
    Server Connect 1
    ${non_prim_dev} =   get_non_primary_device
    Log  ${non_prim_dev}
    server Disconnect
    Step  4  upgrade whitebox FW with mode 0xe ESM B  ${non_prim_dev}
    Step  5  activitate whitebox FW reset 00h ESM B  ${non_prim_dev}
    Step  6  check upgrade FW version ESM B 
#    Step  7  check info
    Step  8  Compare ses page gold file
    Server Connect 1
    ${prim_dev} =   get_primary_device
    Log  ${prim_dev}
    ${non_prim_dev} =   get_non_primary_device
    Log  ${non_prim_dev}
    server Disconnect
	
upgrade whitebox FW with mode 0xe ESM A
    [Arguments]    ${sg_device_1}
    Step  1  update_whitebox_fw_force  SES  ${download_microcode_modeE_cmd}  %{DUT_username}  %{DUT_ipv4_ip}  %{DUT_password}  ${sg_device_1}  isUpgrade=True

check upgrade FW version ESM A
    Step  1  OS Connect Device
    Step  2  verify_ses_version_fru_get  DUT  isUpgrade=True
    Step  3  OS Disconnect Device

upgrade whitebox FW with mode 0xe ESM B
    [Arguments]    ${sg_device_2}
    Step  1  update_whitebox_fw_force  SES  ${download_microcode_modeE_cmd}  %{DUT_username}  %{DUT_ipv4_ip}  %{DUT_password}  ${sg_device_2}  isUpgrade=True

check upgrade FW version ESM B
    Step  1  ConnectESMB
    Step  2  verify_ses_version_fru_get  DUT  isUpgrade=True
    Step  3  OS Disconnect Device

check SES version on both ESMs
    checkFwVersionESM  %{DUT_username}  %{DUT_ipv4_ip}  %{DUT_password}

downgrade FW with mode 0xe + reset 03h code Lenovo
    Server Connect 1   
    ${prim_dev} =   get_primary_device
    Log  ${prim_dev}
    ${non_prim_dev} =   get_non_primary_device
    Log  ${non_prim_dev}
    server Disconnect
    Step  1  downgrade whitebox FW with mode 0xe ESM A  ${prim_dev}
    Step  2  activitate whitebox FW reset 03h ESM A  ${prim_dev}
    Step  3  check downgrade FW version ESM A
    Server Connect 1
    ${non_prim_dev} =   get_non_primary_device
    Log  ${non_prim_dev}
    server Disconnect
    Step  4  downgrade whitebox FW with mode 0xe ESM B  ${non_prim_dev}
    Step  5  activitate whitebox FW reset 03h ESM B  ${non_prim_dev}
    Step  6  check downgrade FW version ESM B
#    Step  7  check info
    Server Connect 1
    ${prim_dev} =   get_primary_device
    Log  ${prim_dev}
    ${non_prim_dev} =   get_non_primary_device
    Log  ${non_prim_dev}
    server Disconnect

upgrade FW with mode 0xe + reset 03h code Lenovo
    Server Connect 1
    ${prim_dev} =   get_primary_device
    Log  ${prim_dev}
    ${non_prim_dev} =   get_non_primary_device
    Log  ${non_prim_dev}
    server Disconnect
    Step  1  upgrade whitebox FW with mode 0xe ESM A  ${prim_dev}
    Step  2  activitate whitebox FW reset 03h ESM A  ${prim_dev}
    Step  3  check upgrade FW version ESM A
    Server Connect 1
    ${non_prim_dev} =   get_non_primary_device
    Log  ${non_prim_dev}
    server Disconnect
    Step  4  upgrade whitebox FW with mode 0xe ESM B  ${non_prim_dev}
    Step  5  activitate whitebox FW reset 03h ESM B  ${non_prim_dev}
    Step  6  check upgrade FW version ESM B
#    Step  7  check info
    Server Connect 1
    ${prim_dev} =   get_primary_device
    Log  ${prim_dev}
    ${non_prim_dev} =   get_non_primary_device
    Log  ${non_prim_dev}
    server Disconnect

activitate whitebox FW reset 03h ESM A
    [Arguments]    ${sg_device_1}
    Step  1  ses_activitate  %{DUT_username}  %{DUT_ipv4_ip}  %{DUT_password}  ${sg_device_1}  03h
    Step  2  set time delay  120

activitate whitebox FW reset 03h ESM B
    [Arguments]    ${sg_device_2}
    Step  1  ses_activitate  %{DUT_username}  %{DUT_ipv4_ip}  %{DUT_password}  ${sg_device_2}  03h
    Step  2  set time delay  120

upgrade FW with mode 0xe + reset 01h code Lenovo
    Server Connect 1
    ${prim_dev} =   get_primary_device
    Log  ${prim_dev}
    ${non_prim_dev} =   get_non_primary_device
    Log  ${non_prim_dev}
    server Disconnect
    Step  1  upgrade whitebox FW with mode 0xe ESM A  ${prim_dev}
    Step  2  activitate whitebox FW reset 01h ESM A  ${prim_dev}
    Step  3  check upgrade FW version ESM A
    Server Connect 1
    ${non_prim_dev} =   get_non_primary_device
    Log  ${non_prim_dev}
    server Disconnect
    Step  4  upgrade whitebox FW with mode 0xe ESM B  ${non_prim_dev}
    Step  5  activitate whitebox FW reset 01h ESM B  ${non_prim_dev}
    Step  6  check upgrade FW version ESM B
#    Step  7  check info	
    Server Connect 1
    ${prim_dev} =   get_primary_device
    Log  ${prim_dev}
    ${non_prim_dev} =   get_non_primary_device
    Log  ${non_prim_dev}
    server Disconnect
	
activitate whitebox FW reset 01h ESM A
    [Arguments]    ${sg_device_1}
    Step  1  ses_activitate  %{DUT_username}  %{DUT_ipv4_ip}  %{DUT_password}  ${sg_device_1}  01h
    Step  2  set time delay  120

activitate whitebox FW reset 01h ESM B
    [Arguments]    ${sg_device_2}
    Step  1  ses_activitate  %{DUT_username}  %{DUT_ipv4_ip}  %{DUT_password}  ${sg_device_2}  01h
    Step  2  set time delay  120

downgrade FW with mode 0xe + mode 0xf Lenovo
    Server Connect 1
    ${prim_dev} =   get_primary_device
    Log  ${prim_dev}
    ${non_prim_dev} =   get_non_primary_device
    Log  ${non_prim_dev}
    server Disconnect
    Step  1  downgrade whitebox FW with mode 0xe ESM A  ${prim_dev}
    Step  2  activitate whitebox FW mode 0xf ESM A  ${prim_dev}
    Step  3  check downgrade FW version ESM A
    Server Connect 1
    ${non_prim_dev} =   get_non_primary_device
    Log  ${non_prim_dev}
    server Disconnect
    Step  4  downgrade whitebox FW with mode 0xe ESM B  ${non_prim_dev}
    Step  5  activitate whitebox FW mode 0xf ESM B  ${non_prim_dev}
    Step  6  check downgrade FW version ESM B
#    Step  7  check info
    Server Connect 1
    ${prim_dev} =   get_primary_device
    Log  ${prim_dev}
    ${non_prim_dev} =   get_non_primary_device
    Log  ${non_prim_dev}
    server Disconnect
	
upgrade FW with mode 0xe + mode 0xf Lenovo
    Server Connect 1
    ${prim_dev} =   get_primary_device
    Log  ${prim_dev}
    ${non_prim_dev} =   get_non_primary_device
    Log  ${non_prim_dev}
    server Disconnect
    Step  1  upgrade whitebox FW with mode 0xe ESM A  ${prim_dev}
    Step  2  activitate whitebox FW mode 0xf ESM A  ${prim_dev}
    Step  3  check upgrade FW version ESM A
    Server Connect 1
    ${non_prim_dev} =   get_non_primary_device
    Log  ${non_prim_dev}
    server Disconnect
    Step  4  upgrade whitebox FW with mode 0xe ESM B  ${non_prim_dev}
    Step  5  activitate whitebox FW mode 0xf ESM B  ${non_prim_dev}
    Step  6  check upgrade FW version ESM B
#    Step  7  check info
    Server Connect 1
    ${prim_dev} =   get_primary_device
    Log  ${prim_dev}
    ${non_prim_dev} =   get_non_primary_device
    Log  ${non_prim_dev}
    server Disconnect
	
activitate whitebox FW mode 0xf ESM A
    [Arguments]    ${sg_device_1}
    Step  1  ses_activitate  %{DUT_username}  %{DUT_ipv4_ip}  %{DUT_password}  ${sg_device_1}  0xf
    Step  2  set time delay  90

activitate whitebox FW mode 0xf ESM B
    [Arguments]    ${sg_device_2}
    Step  1  ses_activitate  %{DUT_username}  %{DUT_ipv4_ip}  %{DUT_password}  ${sg_device_2}  0xf
    Step  2  set time delay  90

downgrade FW with mode 0xe + reset 01h code Lenovo
    Server Connect 1
    ${prim_dev} =   get_primary_device
    Log  ${prim_dev}
    server Disconnect
    Step  1  downgrade whitebox FW with mode 0xe ESM A  ${prim_dev}
    Step  2  activitate whitebox FW reset 01h ESM A  ${prim_dev}
    Step  3  check downgrade FW version ESM A
    Server Connect 1
    ${non_prim_dev} =   get_non_primary_device
    Log  ${non_prim_dev}
    server Disconnect
    Step  4  downgrade whitebox FW with mode 0xe ESM B  ${non_prim_dev}
    Step  5  activitate whitebox FW reset 01h ESM B  ${non_prim_dev}
    Step  6  check downgrade FW version ESM B
#    Step  7  check info

upgrade FW with mode 0xe + power cycle Lenovo
    Server Connect 1
    ${prim_dev} =   get_primary_device
    Log  ${prim_dev}
    server Disconnect
    Step  1  upgrade whitebox FW with mode 0xe ESM A  ${prim_dev}
    Step  2  activitate whitebox FW power cycle
    Step  3  check upgrade FW version ESM A
    Server Connect 1
    ${non_prim_dev} =   get_non_primary_device
    Log  ${non_prim_dev}
    server Disconnect
    Step  4  upgrade whitebox FW with mode 0xe ESM B  ${non_prim_dev}
    Step  5  activitate whitebox FW power cycle
    Step  6  check upgrade FW version ESM B

Create ses Diag page gold file Lenovo 
    server Connect 1
    execute_Linux_command  rm -f ses_page_10h_gold_file_*
    execute_Linux_command  rm -f ses_page_17h_gold_file_*    
    ${prim_dev} =   get_primary_device
    ${non_prim_dev} =   get_non_primary_device
    server Disconnect	    
    ${ses_fw_version} =  get_ses_fw_version_by_ses_page_01h  %{DUT_username}  %{DUT_ipv4_ip}  %{DUT_password}  ${prim_dev}
    ${cpld_version_1} =  get_cpld_version_ses_page  %{DUT_username}  %{DUT_ipv4_ip}  %{DUT_password}  ${prim_dev}  isUpgrade=True
    ${cpld_version_2} =  get_cpld_version_ses_page  %{DUT_username}  %{DUT_ipv4_ip}  %{DUT_password}  ${prim_dev}  isUpgrade=False
    Step  1  Lenovo_JBOD_via_ses_command  %{DUT_username}  %{DUT_ipv4_ip}  %{DUT_password}  ${sg_pg10_diag_cmd1}  ${prim_dev}
    Step  2  create_gold_file  %{DUT_username}  %{DUT_ipv4_ip}  %{DUT_password}  sg_ses -p 0x10 ${prim_dev}  ${ses_page_10h_gold_file_1}
    Step  3  Lenovo_JBOD_via_ses_command  %{DUT_username}  %{DUT_ipv4_ip}  %{DUT_password}  ${sg_pg10_diag_cmd1}  ${non_prim_dev}
    Step  4  create_gold_file  %{DUT_username}  %{DUT_ipv4_ip}  %{DUT_password}  sg_ses -p 0x10 ${non_prim_dev}  ${ses_page_10h_gold_file_2}
    Step  5  Lenovo_JBOD_via_ses_command  %{DUT_username}  %{DUT_ipv4_ip}  %{DUT_password}  ${sg_pg17_diag_cmd1}  ${prim_dev}
    Step  6  create_gold_file  %{DUT_username}  %{DUT_ipv4_ip}  %{DUT_password}  sg_ses -p 0x17 ${prim_dev}  ${ses_page_17h_gold_file_1}
    Step  7  Lenovo_JBOD_via_ses_command  %{DUT_username}  %{DUT_ipv4_ip}  %{DUT_password}  ${sg_pg17_diag_cmd1}  ${non_prim_dev}
    Step  8  create_gold_file  %{DUT_username}  %{DUT_ipv4_ip}  %{DUT_password}  sg_ses -p 0x17 ${non_prim_dev}  ${ses_page_17h_gold_file_2}

Compare ses Diag page gold file Lenovo
    server Connect 1
    ${prim_dev} =   get_primary_device
    ${non_prim_dev} =   get_non_primary_device
    server Disconnect	
    ${ses_fw_version} =  get_ses_fw_version_by_ses_page_01h  %{DUT_username}  %{DUT_ipv4_ip}  %{DUT_password}  ${prim_dev}
    ${cpld_version_1} =  get_cpld_version_ses_page  %{DUT_username}  %{DUT_ipv4_ip}  %{DUT_password}  ${prim_dev}  isUpgrade=True
    ${cpld_version_2} =  get_cpld_version_ses_page  %{DUT_username}  %{DUT_ipv4_ip}  %{DUT_password}  ${prim_dev}  isUpgrade=False
    Step  1  Lenovo_JBOD_via_ses_command  %{DUT_username}  %{DUT_ipv4_ip}  %{DUT_password}  ${sg_pg10_diag_cmd1}  ${prim_dev}
    Step  2  create_gold_file  %{DUT_username}  %{DUT_ipv4_ip}  %{DUT_password}  sg_ses -p 0x10 ${prim_dev}  ${ses_page_10h_gold_file_tmp}
    Step  3  compare_file  ${ses_page_10h_gold_file_1}  ${ses_page_10h_gold_file_tmp}  ses_page_10
    Step  4  Lenovo_JBOD_via_ses_command  %{DUT_username}  %{DUT_ipv4_ip}  %{DUT_password}  ${sg_pg10_diag_cmd1}  ${non_prim_dev}
    Step  5  create_gold_file  %{DUT_username}  %{DUT_ipv4_ip}  %{DUT_password}  sg_ses -p 0x10 ${non_prim_dev}  ${ses_page_10h_gold_file_tmp}
    Step  6  compare_file  ${ses_page_10h_gold_file_2}  ${ses_page_10h_gold_file_tmp}  ses_page_10
    #sleep  60
    Step  7  Lenovo_JBOD_via_ses_command  %{DUT_username}  %{DUT_ipv4_ip}  %{DUT_password}  ${sg_pg17_diag_cmd1}  ${prim_dev}
    Step  8  create_gold_file  %{DUT_username}  %{DUT_ipv4_ip}  %{DUT_password}  sg_ses -p 0x17 ${prim_dev}  ${ses_page_17h_gold_file_tmp}
    Step  9  compare_file  ${ses_page_17h_gold_file_1}  ${ses_page_17h_gold_file_tmp}  ses_page_17
    #sleep  60
    Step  10  Lenovo_JBOD_via_ses_command  %{DUT_username}  %{DUT_ipv4_ip}  %{DUT_password}  ${sg_pg17_diag_cmd1}  ${non_prim_dev}
    Step  11  create_gold_file  %{DUT_username}  %{DUT_ipv4_ip}  %{DUT_password}  sg_ses -p 0x17 ${non_prim_dev}  ${ses_page_17h_gold_file_tmp}
    Step  12  compare_file  ${ses_page_17h_gold_file_2}  ${ses_page_17h_gold_file_tmp}  ses_page_17

Read VPD from one canister with 0x10 Diag page Lenovo
    server Connect 1
    ${prim_dev} =   get_primary_device
    ${non_prim_dev} =   get_non_primary_device
    server Disconnect    
    ${ses_fw_version} =  get_ses_fw_version_by_ses_page_01h  %{DUT_username}  %{DUT_ipv4_ip}  %{DUT_password}  ${prim_dev}
    Step  1  Lenovo_JBOD_via_ses_command  %{DUT_username}  %{DUT_ipv4_ip}  %{DUT_password}  ${sg_pg10_diag_cmd1}  ${prim_dev}
    Step  2  create_gold_file  %{DUT_username}  %{DUT_ipv4_ip}  %{DUT_password}  sg_ses -p 0x10 ${prim_dev}  ${ses_page_10h_gold_file_tmp}
    Step  3  compare_file  ${ses_page_10h_gold_file_1}  ${ses_page_10h_gold_file_tmp}  ses_page_10

Read VPD from two canister with 0x10 Diag page Lenovo
    server Connect 1
    ${prim_dev} =   get_primary_device
    ${non_prim_dev} =   get_non_primary_device
    server Disconnect    
    Step  1  Lenovo_JBOD_via_ses_command  %{DUT_username}  %{DUT_ipv4_ip}  %{DUT_password}  ${sg_pg10_diag_cmd1}  ${prim_dev}
    Step  2  create_gold_file  %{DUT_username}  %{DUT_ipv4_ip}  %{DUT_password}  sg_ses -p 0x10 ${prim_dev}  ${ses_page_10h_gold_file_tmp}
    Step  3  compare_file  ${ses_page_10h_gold_file_1}  ${ses_page_10h_gold_file_tmp}  ses_page_10
    Step  4  Lenovo_JBOD_via_ses_command  %{DUT_username}  %{DUT_ipv4_ip}  %{DUT_password}  ${sg_pg10_diag_cmd1}  ${non_prim_dev}
    Step  5  create_gold_file  %{DUT_username}  %{DUT_ipv4_ip}  %{DUT_password}  sg_ses -p 0x10 ${non_prim_dev}  ${ses_page_10h_gold_file_tmp}
    Step  6  compare_file  ${ses_page_10h_gold_file_2}  ${ses_page_10h_gold_file_tmp}  ses_page_10

Read VPD from both canisters with 0x17 Diag page Lenovo
    server Connect 1
    ${prim_dev} =   get_primary_device
    ${non_prim_dev} =   get_non_primary_device
    server Disconnect    
    ${ses_fw_version} =  get_ses_fw_version_by_ses_page_01h  %{DUT_username}  %{DUT_ipv4_ip}  %{DUT_password}  ${prim_dev}
    Step  1  Lenovo_JBOD_via_ses_command  %{DUT_username}  %{DUT_ipv4_ip}  %{DUT_password}  ${sg_pg17_diag_cmd1}  ${prim_dev}
    sleep  60
    Step  2  create_gold_file  %{DUT_username}  %{DUT_ipv4_ip}  %{DUT_password}  sg_ses -p 0x17 ${prim_dev}  ${ses_page_17h_gold_file_tmp}
    Step  3  compare_file  ${ses_page_17h_gold_file_1}  ${ses_page_17h_gold_file_tmp}  ses_page_17
    Step  4  Lenovo_JBOD_via_ses_command  %{DUT_username}  %{DUT_ipv4_ip}  %{DUT_password}  ${sg_pg17_diag_cmd1}  ${non_prim_dev}
    sleep  60
    Step  5  create_gold_file  %{DUT_username}  %{DUT_ipv4_ip}  %{DUT_password}  sg_ses -p 0x17 ${non_prim_dev}  ${ses_page_17h_gold_file_tmp}
    Step  6  compare_file  ${ses_page_17h_gold_file_2}  ${ses_page_17h_gold_file_tmp}  ses_page_17


Read VPD from two canister with 0x17 Diag page Lenovo
    server Connect 1
    ${prim_dev} =   get_primary_device
    ${non_prim_dev} =   get_non_primary_device
    server Disconnect    
    Step  1  Lenovo_JBOD_via_ses_command  %{DUT_username}  %{DUT_ipv4_ip}  %{DUT_password}  ${sg_pg17_diag_cmd1}  ${prim_dev}
    Step  2  create_gold_file  %{DUT_username}  %{DUT_ipv4_ip}  %{DUT_password}  sg_ses -p 0x17 ${prim_dev}  ${ses_page_17h_gold_file_tmp}
    Step  3  compare_file  ${ses_page_17h_gold_file_1}  ${ses_page_17h_gold_file_tmp}  ses_page_17
    Step  4  Lenovo_JBOD_via_ses_command  %{DUT_username}  %{DUT_ipv4_ip}  %{DUT_password}  ${sg_pg17_diag_cmd1}  ${non_prim_dev}
    sleep  60
    Step  5  create_gold_file  %{DUT_username}  %{DUT_ipv4_ip}  %{DUT_password}  sg_ses -p 0x17 ${non_prim_dev}  ${ses_page_17h_gold_file_tmp}
    Step  6  compare_file  ${ses_page_17h_gold_file_2}  ${ses_page_17h_gold_file_tmp}  ses_page_17

check PSU Redundant available
    server Connect 1
    check_PSU_Redundant
    server Disconnect

verify the number of drives and pcie devices on ESM-A
    server Connect 1
    whitebox_lib.run_ipmi_cmd_sel_clear  DUT
    ${Before_drive_count} =   getNumberOfDrives
    Log  ${Before_drive_count}
    ${Before_PCIE_count} =   getNumberOfPCIEDrives
    Log  ${Before_PCIE_count}
    server Disconnect
    OS Connect Device
    change_to_ESM_mode
    execute_ESM_command_1    log clear
    poweroff_pdu3  DUT
    OS Disconnect Device
    set time delay  20
    server Connect 1
    ${AfterOff_drive_count} =   getNumberOfDrives
    Log  ${AfterOff_drive_count}
    ${AfterOff_PCIE_count} =   getNumberOfPCIEDrives
    Log  ${AfterOff_PCIE_count}
    Should Be Equal As Strings    ${Before_drive_count}    ${AfterOff_drive_count}
    server Disconnect
    OS Connect Device
    ${led_output}=   execute_ESM_command_1    log get
    common_check_patern_2    ${led_output}  PSU.*Power State Change.*Off.*N/A.*c   Power off Redundant PSU  expect=True
    common_check_patern_2    ${led_output}  PSU.*AC Failure.*Assert.*N/A.*c   Power off Redundant PSU  expect=True
    poweron_pdu3  DUT
    set time delay  20
    ${led_output}=   execute_ESM_command_1    log get
    common_check_patern_2    ${led_output}  PSU.*Power State Change.*On.*N/A.*i   Power on Redundant PSU  expect=True
    common_check_patern_2    ${led_output}  PSU.*AC Failure.*De-assert.*N/A.*i   Power on Redundant PSU  expect=True
    exit_ESM_mode
    OS Disconnect Device
    server Connect 1
    ${AfterOn_drive_count} =   getNumberOfDrives
    Log  ${AfterOn_drive_count}
    ${AfterOn_PCIE_count} =   getNumberOfPCIEDrives
    Log  ${AfterOn_PCIE_count}
    Should Be Equal As Strings    ${Before_drive_count}    ${AfterOff_drive_count}
    whitebox_lib.verify_cmd_output_message  DUT  ipmitool sel list  ${error_messages_sell_list}
    server Disconnect

verify the number of drives and pcie devices on ESM-B
    server Connect 1
    whitebox_lib.run_ipmi_cmd_sel_clear  DUT
    ${Before_drive_count} =   getNumberOfDrives
    Log  ${Before_drive_count}
    ${Before_PCIE_count} =   getNumberOfPCIEDrives
    Log  ${Before_PCIE_count}
    server Disconnect
    ConnectESMB
    change_to_ESM_mode
    execute_ESM_command_1    log clear
    poweroff_pdu3  DUT
    OS Disconnect Device
    set time delay  20    
    server Connect 1
    ${AfterOff_drive_count} =   getNumberOfDrives
    Log  ${AfterOff_drive_count}
    ${AfterOff_PCIE_count} =   getNumberOfPCIEDrives
    Log  ${AfterOff_PCIE_count}
    Should Be Equal As Strings    ${Before_drive_count}    ${AfterOff_drive_count}
    server Disconnect
    ConnectESMB
    ${led_output}=   execute_ESM_command_1    log get
    common_check_patern_2    ${led_output}  PSU.*Power State Change.*Off.*N/A.*c   Power off Redundant PSU  expect=True
    common_check_patern_2    ${led_output}  PSU.*AC Failure.*Assert.*N/A.*c   Power off Redundant PSU  expect=True
    poweron_pdu3  DUT
    set time delay  20
    ${led_output}=   execute_ESM_command_1    log get
    common_check_patern_2    ${led_output}  PSU.*Power State Change.*On.*N/A.*i   Power on Redundant PSU  expect=True
    common_check_patern_2    ${led_output}  PSU.*AC Failure.*De-assert.*N/A.*i   Power on Redundant PSU  expect=True
    exit_ESM_mode
    OS Disconnect Device
    server Connect 1
    ${AfterOn_drive_count} =   getNumberOfDrives
    Log  ${AfterOn_drive_count}
    ${AfterOn_PCIE_count} =   getNumberOfPCIEDrives
    Log  ${AfterOn_PCIE_count}
    Should Be Equal As Strings    ${Before_drive_count}    ${AfterOff_drive_count}
    whitebox_lib.verify_cmd_output_message  DUT  ipmitool sel list  ${error_messages_sell_list}
    server Disconnect


check all supported diagnostic pages nebula
    ${nebula_devices} =  get_device_list_nebula    %{DUT_username}  %{DUT_ipv4_ip}  %{DUT_password}
    Log  ${nebula_devices}
    Step  1  verify_ses_page_00h  %{DUT_username}  %{DUT_ipv4_ip}  %{DUT_password}  ${nebula_devices}[0]
    Step  2  verify_ses_page_00h  %{DUT_username}  %{DUT_ipv4_ip}  %{DUT_password}  ${nebula_devices}[1]

restore Temperature Threshold nebula
    [Arguments]    ${alarm_level}
    Log  ${SENSOR}
    Log  ${HDD}
    Log  ${THRESHOLDs}
    Log  ${alarm_level}
    set Back Threshold  ${SENSOR}  ${HDD}  ${THRESHOLDs}  ${alarm_level}
    check Alarm Normal  ${SENSOR}  ${HDD}  ${alarm_level}
    clear Alarm Bit  ${HDD}  ${alarm_level}
    set Back Threshold  ${SENSOR1}  ${HDD1}  ${THRESHOLDs1}  ${alarm_level}
    check Alarm Normal  ${SENSOR1}  ${HDD1}  ${alarm_level}
    clear Alarm Bit  ${HDD1}  ${alarm_level}

Create ses page gold file nebula
    ${nebula_devices}=  get_device_list_nebula    %{DUT_username}  %{DUT_ipv4_ip}  %{DUT_password}
    set Test Variable  ${sg_device_1}  ${nebula_devices}[0]
    set Test Variable  ${sg_device_2}  ${nebula_devices}[1]
    Log  ${sg_device_1}
    Log  ${sg_device_2}
    ${ses_fw_version} =  get_ses_fw_version_by_ses_page_01h  %{DUT_username}  %{DUT_ipv4_ip}  %{DUT_password}  ${sg_device_1}
    ${cpld_version_1} =  get_cpld_version_ses_page  %{DUT_username}  %{DUT_ipv4_ip}  %{DUT_password}  ${sg_device_1}  isUpgrade=True
    ${cpld_version_2} =  get_cpld_version_ses_page  %{DUT_username}  %{DUT_ipv4_ip}  %{DUT_password}  ${sg_device_1}  isUpgrade=False
    Log  ${ses_fw_version}
    Log  ${cpld_version_1}
    Log  ${cpld_version_2}
    Step  1  create_gold_file  %{DUT_username}  %{DUT_ipv4_ip}  %{DUT_password}
          ...  sg_ses --page=0x01 ${sg_device_1}|grep -v '${ses_fw_version}'  ${ses_page_01h_gold_file}
    Step  2  create_gold_file  %{DUT_username}  %{DUT_ipv4_ip}  %{DUT_password}
          ...  sg_ses --page=0x01 ${sg_device_2}|grep -v '${ses_fw_version}'  ${ses_page_01h_gold_file_2}
    Step  3  create_gold_file  %{DUT_username}  %{DUT_ipv4_ip}  %{DUT_password}
          ...  sg_ses --page=0x02 ${sg_device_1}|grep -v '${ses_fw_version}'|grep -v rpm|grep -v Voltage:|grep -v amps|grep -v Temperature=|grep -v INFO  ${ses_page_02h_gold_file_1}
    Step  4  create_gold_file  %{DUT_username}  %{DUT_ipv4_ip}  %{DUT_password}
          ...  sg_ses --page=0x02 ${sg_device_2}|grep -v '${ses_fw_version}'|grep -v rpm|grep -v Voltage:|grep -v amps|grep -v Temperature=|grep -v INFO  ${ses_page_02h_gold_file_2}
    Step  5  create_gold_file  %{DUT_username}  %{DUT_ipv4_ip}  %{DUT_password}
          ...  sg_ses --page=0x04 ${sg_device_1}|grep -v '${ses_fw_version}'  ${ses_page_04h_gold_file}
    Step  6  create_gold_file  %{DUT_username}  %{DUT_ipv4_ip}  %{DUT_password}
          ...  sg_ses --page=0x05 ${sg_device_1}|grep -v '${ses_fw_version}'  ${ses_page_05h_gold_file}
    Step  7  create_gold_file  %{DUT_username}  %{DUT_ipv4_ip}  %{DUT_password}
          ...  sg_ses --page=0x07 ${sg_device_1}|grep -v '${ses_fw_version}'|grep -v Secondary|grep -v Primary|grep -v ${cpld_version_1}|grep -v ${cpld_version_2}   ${ses_page_07h_gold_file}
    Step  8  create_gold_file  %{DUT_username}  %{DUT_ipv4_ip}  %{DUT_password}
          ...  sg_ses --page=0x0a ${sg_device_1}|grep -v '${ses_fw_version}'  ${ses_page_a_gold_file_1}
    Step  9  create_gold_file  %{DUT_username}  %{DUT_ipv4_ip}  %{DUT_password}
          ...  sg_ses --page=0x0a ${sg_device_2}|grep -v '${ses_fw_version}'  ${ses_page_a_gold_file_2}
    Step  10  create_gold_file  %{DUT_username}  %{DUT_ipv4_ip}  %{DUT_password}
          ...  sg_ses --page=0x0e ${sg_device_1}|grep -v '${ses_fw_version}'|grep -v offset  ${ses_page_e_gold_file}

Compare ses page gold file nebula
    ${nebula_devices}=  get_device_list_nebula    %{DUT_username}  %{DUT_ipv4_ip}  %{DUT_password}
    set Test Variable  ${sg_device_1}  ${nebula_devices}[0]
    set Test Variable  ${sg_device_2}  ${nebula_devices}[1]
    Log  ${sg_device_1}
    Log  ${sg_device_2}
    ${ses_fw_version} =  get_ses_fw_version_by_ses_page_01h  %{DUT_username}  %{DUT_ipv4_ip}  %{DUT_password}  ${sg_device_1}
    ${cpld_version_1} =  get_cpld_version_ses_page  %{DUT_username}  %{DUT_ipv4_ip}  %{DUT_password}  ${sg_device_1}  isUpgrade=True
    ${cpld_version_2} =  get_cpld_version_ses_page  %{DUT_username}  %{DUT_ipv4_ip}  %{DUT_password}  ${sg_device_1}  isUpgrade=False
    Log  ${ses_fw_version}
    Log  ${cpld_version_1}
    Log  ${cpld_version_2}
    Sleep  90
    Step  1  create_gold_file  %{DUT_username}  %{DUT_ipv4_ip}  %{DUT_password}
          ...  sg_ses --page=0x01 ${sg_device_1}|grep -v '${ses_fw_version}'  ${ses_page_tmp_file}
    Step  2  compare_file  ${ses_page_01h_gold_file}  ${ses_page_tmp_file}  ses_page_01h
    Sleep  60
    Step  3  create_gold_file  %{DUT_username}  %{DUT_ipv4_ip}  %{DUT_password}
          ...  sg_ses --page=0x01 ${sg_device_2}|grep -v '${ses_fw_version}'  ${ses_page_tmp_file}
    Step  4  compare_file  ${ses_page_01h_gold_file_2}  ${ses_page_tmp_file}  ses_page_01h
    Sleep  60
    Step  5  create_gold_file  %{DUT_username}  %{DUT_ipv4_ip}  %{DUT_password}
          ...  sg_ses --page=0x02 ${sg_device_1}|grep -v '${ses_fw_version}'|grep -v rpm|grep -v Voltage:|grep -v amps|grep -v Temperature=|grep -v INFO  ${ses_page_tmp_file}
    Step  6  compare_file  ${ses_page_02h_gold_file_1}  ${ses_page_tmp_file}  ses_page_02h_1
    Sleep  120
    Step  7  create_gold_file  %{DUT_username}  %{DUT_ipv4_ip}  %{DUT_password}
          ...  sg_ses --page=0x02 ${sg_device_2}|grep -v '${ses_fw_version}'|grep -v rpm|grep -v Voltage:|grep -v amps|grep -v Temperature=|grep -v INFO  ${ses_page_tmp_file}
    Step  8  compare_file  ${ses_page_02h_gold_file_2}  ${ses_page_tmp_file}  ses_page_02h_2
    Sleep  60
    Step  9  create_gold_file  %{DUT_username}  %{DUT_ipv4_ip}  %{DUT_password}
          ...  sg_ses --page=0x05 ${sg_device_1}|grep -v '${ses_fw_version}'  ${ses_page_tmp_file}
    Step  10  compare_file  ${ses_page_05h_gold_file}  ${ses_page_tmp_file}  ses_page_05h
    Sleep  60
    Step  11  create_gold_file  %{DUT_username}  %{DUT_ipv4_ip}  %{DUT_password}
          ...  sg_ses --page=0x07 ${sg_device_1}|grep -v '${ses_fw_version}'|grep -v Secondary|grep -v Primary|grep -v ${cpld_version_1}|grep -v ${cpld_version_2}  ${ses_page_tmp_file}
    Step  12  compare_file  ${ses_page_07h_gold_file}  ${ses_page_tmp_file}  ses_page_07h
    Sleep  60
    Step  13  create_gold_file  %{DUT_username}  %{DUT_ipv4_ip}  %{DUT_password}
          ...  sg_ses --page=0x0a ${sg_device_1}|grep -v '${ses_fw_version}'  ${ses_page_tmp_file}
    Step  14  compare_file  ${ses_page_a_gold_file_1}  ${ses_page_tmp_file}  ses_page_a_1
    Sleep  60
    Step  15  create_gold_file  %{DUT_username}  %{DUT_ipv4_ip}  %{DUT_password}
          ...  sg_ses --page=0x0a ${sg_device_2}|grep -v '${ses_fw_version}'  ${ses_page_tmp_file}
    Step  16  compare_file  ${ses_page_a_gold_file_2}  ${ses_page_tmp_file}  ses_page_a_2
    Sleep  60
    Step  17  create_gold_file  %{DUT_username}  %{DUT_ipv4_ip}  %{DUT_password}
          ...  sg_ses --page=0x0e ${sg_device_1}|grep -v '${ses_fw_version}'|grep -v offset  ${ses_page_tmp_file}
    Step  18  compare_file  ${ses_page_e_gold_file}  ${ses_page_tmp_file}  ses_page_e

Configuration Diagnostic Pages(01h) nebula
    ${nebula_devices}=  get_device_list_nebula    %{DUT_username}  %{DUT_ipv4_ip}  %{DUT_password}
    set Test Variable  ${sg_device_1}  ${nebula_devices}[0]
    set Test Variable  ${sg_device_2}  ${nebula_devices}[1]    
    ${ses_fw_version} =  get_ses_fw_version_by_ses_page_01h  %{DUT_username}  %{DUT_ipv4_ip}  %{DUT_password}  ${sg_device_1}
    Step  1  verify_ses_page_01h_info  %{DUT_username}  %{DUT_ipv4_ip}  %{DUT_password}  ${sg_device_1}  ${ses_page_01h_info}
    Step  2  verify_ses_page_01h_info  %{DUT_username}  %{DUT_ipv4_ip}  %{DUT_password}  ${sg_device_2}  ${ses_page_01h_info}
    Sleep  60
    Step  3  create_gold_file  %{DUT_username}  %{DUT_ipv4_ip}  %{DUT_password}
          ...  sg_ses --page=0x01 ${sg_device_1} |grep -v '${ses_fw_version}'  ${ses_page_tmp_file}
    Step  4  compare_file  ${ses_page_01h_gold_file}  ${ses_page_tmp_file}
    Step  5  create_gold_file  %{DUT_username}  %{DUT_ipv4_ip}  %{DUT_password}
          ...  sg_ses --page=0x01 ${sg_device_2} |grep -v '${ses_fw_version}'  ${ses_page_tmp_file}
    Sleep  60
    Step  6  compare_file  ${ses_page_01h_gold_file_2}  ${ses_page_tmp_file}

check Cooling external Mode nebula
    ${nebula_devices}=  get_device_list_nebula    %{DUT_username}  %{DUT_ipv4_ip}  %{DUT_password}
    set Test Variable  ${sg_device_1}  ${nebula_devices}[0]
    set Test Variable  ${sg_device_2}  ${nebula_devices}[1]
    Step  1  verify_ses_page_02_cooling_Mode  %{DUT_username}  %{DUT_ipv4_ip}  %{DUT_password}  ${sg_device_1}  external
    Step  2  verify_ses_page_02_cooling_Mode  %{DUT_username}  %{DUT_ipv4_ip}  %{DUT_password}  ${sg_device_2}  external
    Step  3  OS Connect Device
    Step  4  verify_esm_fan_mode_cli_command  DUT  external
    Step  5  OS Disconnect Device
    Step  6  ConnectESMB
    Step  7  verify_esm_fan_mode_cli_command  DUT  external
    Step  8  OS Disconnect Device

check Fan current speed nebula
    ${nebula_devices}=  get_device_list_nebula    %{DUT_username}  %{DUT_ipv4_ip}  %{DUT_password}
    set Test Variable  ${sg_device_1}  ${nebula_devices}[0]
    set Test Variable  ${sg_device_2}  ${nebula_devices}[1]    
    Step  1  verify_ses_page_02_fan_current_speed  %{DUT_username}  %{DUT_ipv4_ip}  %{DUT_password}  ${sg_device_1}  ${fan_speed_1}
    Step  2  OS Connect Device
    Step  3  verify_fan_speed_cli_command  DUT  ${fan_speed_cli_1}
    Step  4  verify_esm_fan_mode_cli_command  DUT  external
    Step  5  OS Disconnect Device
    Step  6  verify_ses_page_02_fan_current_speed  %{DUT_username}  %{DUT_ipv4_ip}  %{DUT_password}  ${sg_device_1}  ${fan_speed_2}
    Step  7  OS Connect Device
    Step  8  verify_fan_speed_cli_command  DUT  ${fan_speed_cli_2}
    Step  9  verify_esm_fan_mode_cli_command  DUT  external
    Step  10  OS Disconnect Device
    Step  11  set_ses_page_02_fan_speed  %{DUT_username}  %{DUT_ipv4_ip}  %{DUT_password}  ${sg_device_1}  8
    Step  12  get_ses_page_02_fan_speed  %{DUT_username}  %{DUT_ipv4_ip}  %{DUT_password}  ${sg_device_1}  ${fan_speed_2}
    Step  13  OS Connect Device
    Step  14  verify_fan_speed_cli_command  DUT  ${fan_speed_cli_2}
    Step  15  verify_esm_fan_mode_cli_command  DUT  external
    Step  16  OS Disconnect Device

check Fan current speed nebula ESMB
    ${nebula_devices}=  get_device_list_nebula    %{DUT_username}  %{DUT_ipv4_ip}  %{DUT_password}    
    set Test Variable  ${sg_device_2}  ${nebula_devices}[1]
    Step  1  verify_ses_page_02_fan_current_speed  %{DUT_username}  %{DUT_ipv4_ip}  %{DUT_password}  ${sg_device_2}  ${fan_speed_1}
    Step  2  ConnectESMB
    Step  3  verify_fan_speed_cli_command  DUT  ${fan_speed_cli_1}
    Step  4  verify_esm_fan_mode_cli_command  DUT  external
    Step  5  OS Disconnect Device
    Step  6  verify_ses_page_02_fan_current_speed  %{DUT_username}  %{DUT_ipv4_ip}  %{DUT_password}  ${sg_device_2}  ${fan_speed_2}
    Step  7  ConnectESMB
    Step  8  verify_fan_speed_cli_command  DUT  ${fan_speed_cli_2}
    Step  9  verify_esm_fan_mode_cli_command  DUT  external
    Step  10  OS Disconnect Device
    Step  11  set_ses_page_02_fan_speed  %{DUT_username}  %{DUT_ipv4_ip}  %{DUT_password}  ${sg_device_2}  8
    Step  12  get_ses_page_02_fan_speed  %{DUT_username}  %{DUT_ipv4_ip}  %{DUT_password}  ${sg_device_2}  ${fan_speed_2}
    Step  13  ConnectESMB
    Step  14  verify_fan_speed_cli_command  DUT  ${fan_speed_cli_2}
    Step  15  verify_esm_fan_mode_cli_command  DUT  external
    Step  16  OS Disconnect Device

Enclosure Status Diagnostic Pages(02h) nebula
    ${nebula_devices}=  get_device_list_nebula    %{DUT_username}  %{DUT_ipv4_ip}  %{DUT_password}
    set Test Variable  ${sg_device_1}  ${nebula_devices}[0]
    set Test Variable  ${sg_device_2}  ${nebula_devices}[1]
    ${ses_fw_version} =  get_ses_fw_version_by_ses_page_01h  %{DUT_username}  %{DUT_ipv4_ip}  %{DUT_password}  ${sg_device_1}
    Step  1  create_gold_file  %{DUT_username}  %{DUT_ipv4_ip}  %{DUT_password}
          ...  sg_ses --page=0x02 ${sg_device_1}|grep -v '${ses_fw_version}'|grep -v rpm|grep -v Voltage:|grep -v amps|grep -v Temperature=|grep -v INFO  ${ses_page_02h_gold_file_1}
    Step  2  create_gold_file  %{DUT_username}  %{DUT_ipv4_ip}  %{DUT_password}
          ...  sg_ses --page=0x02 ${sg_device_2}|grep -v '${ses_fw_version}'|grep -v rpm|grep -v Voltage:|grep -v amps|grep -v Temperature=|grep -v INFO  ${ses_page_02h_gold_file_2}
    Step  3  create_gold_file  %{DUT_username}  %{DUT_ipv4_ip}  %{DUT_password}
          ...  sg_ses --page=0x02 ${sg_device_1}|grep -v rpm|grep -v Voltage:|grep -v amps|grep -v Temperature=|grep -v INFO|grep -v '${ses_fw_version}'  ${ses_page_tmp_file}
    Step  4  compare_file  ${ses_page_02h_gold_file_1}  ${ses_page_tmp_file}
    Step  5  create_gold_file  %{DUT_username}  %{DUT_ipv4_ip}  %{DUT_password}
          ...  sg_ses --page=0x02 ${sg_device_2}|grep -v rpm|grep -v Voltage:|grep -v amps|grep -v Temperature=|grep -v INFO|grep -v '${ses_fw_version}'  ${ses_page_tmp_file}
    Step  6  compare_file  ${ses_page_02h_gold_file_2}  ${ses_page_tmp_file}

check Cooling internal Mode nebula
    ${nebula_devices}=  get_device_list_nebula    %{DUT_username}  %{DUT_ipv4_ip}  %{DUT_password}
    set Test Variable  ${sg_device_1}  ${nebula_devices}[0]
    set Test Variable  ${sg_device_2}  ${nebula_devices}[1]
    Log  ${sg_device_1}
    Log  ${sg_device_2}
    Step  1  verify_ses_page_02_cooling_Mode  %{DUT_username}  %{DUT_ipv4_ip}  %{DUT_password}  ${sg_device_1}  internal
    Step  2  verify_ses_page_02_cooling_Mode  %{DUT_username}  %{DUT_ipv4_ip}  %{DUT_password}  ${sg_device_2}  internal
    Step  3  OS Connect Device
    Step  4  verify_esm_fan_mode_cli_command  DUT  internal
    Step  5  OS Disconnect Device
    Step  6  ConnectESMB
    Step  7  verify_esm_fan_mode_cli_command  DUT  internal
    Step  8  OS Disconnect Device

check Fan max speed nebula
    ${nebula_devices}=  get_device_list_nebula    %{DUT_username}  %{DUT_ipv4_ip}  %{DUT_password}
    set Test Variable  ${sg_device_1}  ${nebula_devices}[0]
    set Test Variable  ${sg_device_2}  ${nebula_devices}[1]
    Step  1  verify_ses_page_02_fan_current_speed  %{DUT_username}  %{DUT_ipv4_ip}  %{DUT_password}  ${sg_device_1}  ${fan_speed_1}
    Step  2  OS Connect Device
    Step  3  verify_fan_speed_cli_command  DUT  ${fan_speed_cli_1}
    Step  4  verify_esm_fan_mode_cli_command  DUT  external
    Step  5  OS Disconnect Device
    Step  6  verify_ses_page_02_fan_current_speed  %{DUT_username}  %{DUT_ipv4_ip}  %{DUT_password}  ${sg_device_1}  ${fan_max_speed}
    Step  7  OS Connect Device
    Step  8  verify_fan_speed_cli_command  DUT  ${fan_max_speed_cli}
    Step  9  verify_esm_fan_mode_cli_command  DUT  external
    Step  10  OS Disconnect Device
    Step  11  verify_ses_page_02_fan_current_speed  %{DUT_username}  %{DUT_ipv4_ip}  %{DUT_password}  ${sg_device_1}  ${fan_speed_1}
    Step  12  OS Connect Device
    Step  13  verify_fan_speed_cli_command  DUT  ${fan_speed_cli_1}
    Step  14  verify_esm_fan_mode_cli_command  DUT  external
    Step  15  OS Disconnect Device

check Fan max speed nebula ESMB
    ${nebula_devices}=  get_device_list_nebula    %{DUT_username}  %{DUT_ipv4_ip}  %{DUT_password}
    set Test Variable  ${sg_device_1}  ${nebula_devices}[0]
    set Test Variable  ${sg_device_2}  ${nebula_devices}[1]
    Step  1  verify_ses_page_02_fan_current_speed  %{DUT_username}  %{DUT_ipv4_ip}  %{DUT_password}  ${sg_device_2}  ${fan_speed_1}
    Step  2  ConnectESMB
    Step  3  verify_fan_speed_cli_command  DUT  ${fan_speed_cli_1}
    Step  4  verify_esm_fan_mode_cli_command  DUT  external
    Step  5  OS Disconnect Device
    Step  6  verify_ses_page_02_fan_current_speed  %{DUT_username}  %{DUT_ipv4_ip}  %{DUT_password}  ${sg_device_2}  ${fan_max_speed}
    Step  7  ConnectESMB
    Step  8  verify_fan_speed_cli_command  DUT  ${fan_max_speed_cli}
    Step  9  verify_esm_fan_mode_cli_command  DUT  external
    Step  10  OS Disconnect Device
    Step  11  verify_ses_page_02_fan_current_speed  %{DUT_username}  %{DUT_ipv4_ip}  %{DUT_password}  ${sg_device_2}  ${fan_speed_1}
    Step  12  ConnectESMB
    Step  13  verify_fan_speed_cli_command  DUT  ${fan_speed_cli_1}
    Step  14  verify_esm_fan_mode_cli_command  DUT  external
    Step  15  OS Disconnect Device

check Disk Power Off nebula
    ${nebula_devices}=  get_device_list_nebula    %{DUT_username}  %{DUT_ipv4_ip}  %{DUT_password}
    ${DEVICEs}=  list Array Devices  ${nebula_devices}[0]
    verify Device Power Off    ${nebula_devices}[0]    ${DEVICEs}[0]
    ${DEVICEs}=  list Array Devices  ${nebula_devices}[1]
    verify Device Power Off    ${nebula_devices}[1]    ${DEVICEs}[0]

check Disks Info On Page 0x0a nebula
    ${nebula_devices}=  get_device_list_nebula    %{DUT_username}  %{DUT_ipv4_ip}  %{DUT_password}
    verify Disk Info  ${nebula_devices}[0]
    verify Disk Info  ${nebula_devices}[1]

check Fan min speed nebula
    ${nebula_devices}=  get_device_list_nebula    %{DUT_username}  %{DUT_ipv4_ip}  %{DUT_password}
    set Test Variable  ${sg_device_1}  ${nebula_devices}[0]
    Step  1  verify_ses_page_02_fan_current_speed  %{DUT_username}  %{DUT_ipv4_ip}  %{DUT_password}  ${sg_device_1}  ${fan_min_speed}
    Step  2  OS Connect Device
    Step  3  verify_fan_speed_cli_command  DUT  ${fan_min_speed_cli}
    Step  4  verify_esm_fan_mode_cli_command  DUT  external
    Step  5  OS Disconnect Device
    Step  6  verify_ses_page_02_fan_current_speed  %{DUT_username}  %{DUT_ipv4_ip}  %{DUT_password}  ${sg_device_1}  ${fan_max_speed}
    Step  7  OS Connect Device
    Step  8  verify_fan_speed_cli_command  DUT  ${fan_max_speed_cli}
    Step  9  verify_esm_fan_mode_cli_command  DUT  external
    Step  10  OS Disconnect Device
    Step  11  verify_ses_page_02_fan_current_speed  %{DUT_username}  %{DUT_ipv4_ip}  %{DUT_password}  ${sg_device_1}  ${fan_min_speed}
    Step  12  OS Connect Device
    Step  13  verify_fan_speed_cli_command  DUT  ${fan_min_speed_cli}
    Step  14  verify_esm_fan_mode_cli_command  DUT  external
    Step  15  OS Disconnect Device

check Fan min speed ESMB nebula
    ${nebula_devices}=  get_device_list_nebula    %{DUT_username}  %{DUT_ipv4_ip}  %{DUT_password}
    set Test Variable  ${sg_device_2}  ${nebula_devices}[0]
    Step  1  verify_ses_page_02_fan_current_speed  %{DUT_username}  %{DUT_ipv4_ip}  %{DUT_password}  ${sg_device_2}  ${fan_min_speed}
    Step  2  ConnectESMB
    Step  3  verify_fan_speed_cli_command  DUT  ${fan_min_speed_cli}
    Step  4  verify_esm_fan_mode_cli_command  DUT  external
    Step  5  OS Disconnect Device
    Step  6  verify_ses_page_02_fan_current_speed  %{DUT_username}  %{DUT_ipv4_ip}  %{DUT_password}  ${sg_device_2}  ${fan_max_speed}
    Step  7  ConnectESMB
    Step  8  verify_fan_speed_cli_command  DUT  ${fan_max_speed_cli}
    Step  9  verify_esm_fan_mode_cli_command  DUT  external
    Step  10  OS Disconnect Device
    Step  11  verify_ses_page_02_fan_current_speed  %{DUT_username}  %{DUT_ipv4_ip}  %{DUT_password}  ${sg_device_2}  ${fan_min_speed}
    Step  12  ConnectESMB
    Step  13  verify_fan_speed_cli_command  DUT  ${fan_min_speed_cli}
    Step  14  verify_esm_fan_mode_cli_command  DUT  external
    Step  15  OS Disconnect Device

Download SES FW File And Update Nebula
    [Arguments]  ${UPGRADE}
    Server Connect 1
    mkdir_data_path    DUT  "/root/titanlenovoG2"
    download Ses Fw Image  upgrade=${UPGRADE}
    ${HDDs}=  get_device_list_nebula    %{DUT_username}  %{DUT_ipv4_ip}  %{DUT_password}
    Log  ${HDDs}
    Log  ${HDDs}[0]
    Log  ${HDDs}[1]
    ${Image_list}=  getFWImage    upgrade=${UPGRADE}
    Log  ${Image_list}
    update Ses Fw  ${HDDs}[0]  ${UPGRADE}  ${Image_list}[0]
    Reboot_OS_via_MGMT    %{DUT_username}  %{DUT_ipv4_ip}  %{DUT_password}  reboot
    server Disconnect
    set time delay  130
    Server Connect 1        
    update Ses Fw  ${HDDs}[0]  ${UPGRADE}  ${Image_list}[1]
    Reboot_OS_via_MGMT    %{DUT_username}  %{DUT_ipv4_ip}  %{DUT_password}  reboot
    server Disconnect
    set time delay  130
    Server Connect 1
    update Ses Fw  ${HDDs}[1]  ${UPGRADE}  ${Image_list}[0]
    Reboot_OS_via_MGMT    %{DUT_username}  %{DUT_ipv4_ip}  %{DUT_password}  reboot
    server Disconnect
    set time delay  130
    Server Connect 1
    update Ses Fw  ${HDDs}[1]  ${UPGRADE}  ${Image_list}[1]
    Reboot_OS_via_MGMT    %{DUT_username}  %{DUT_ipv4_ip}  %{DUT_password}  reboot
    server Disconnect
    set time delay  130
    set Test Variable   ${HDDs}  ${HDDs}

check ESM SES FW Version Nebula
    [Arguments]  ${UPGRADE}
    OS Connect Device
    verify_ses_version_fru_get_nebula  DUT  ${UPGRADE}
    OS Disconnect Device
    ConnectESMB
    verify_ses_version_fru_get_nebula  DUT  ${UPGRADE}
    OS Disconnect Device

check SES FW Version On Server Nebula
    [Arguments]  ${UPGRADE}
    server Connect
    ${HDDs}=  get_device_list_nebula    %{DUT_username}  %{DUT_ipv4_ip}  %{DUT_password}
    run And Check  ${check_sbb_cmd} ${HDDs}[0]  ${check_sbb_result_nebula}
    check Page2 Page10 Fw Version  ${HDDs}[0]  upgrade=${UPGRADE}
    run And Check  ${check_sbb_cmd} ${HDDs}[1]  ${check_sbb_result_nebula}
    check Page2 Page10 Fw Version  ${HDDs}[1]  upgrade=${UPGRADE}
    check_Ses_Fw_Version_nebula    %{DUT_username}  %{DUT_ipv4_ip}  %{DUT_password}  ${HDDs}  ${UPGRADE}
    server Disconnect

upgrade FW with mode 0xe + mode 0xf nebula
    Server Connect 1
    ${prim_dev} =   get_primary_device_nebula    %{DUT_username}  %{DUT_ipv4_ip}  %{DUT_password}
    Log  ${prim_dev}
    ${non_prim_dev} =   get_non_primary_device_nebula    %{DUT_username}  %{DUT_ipv4_ip}  %{DUT_password}
    Log  ${non_prim_dev}
    ${Image_list}=  getFWImage    upgrade=True
    Log  ${Image_list}
    Step  1   upgrade whitebox FW with mode 0xe ESM A nebula  ${prim_dev}  ${Image_list}[0]
    Step  2   upgrade whitebox FW with mode 0xe ESM A nebula  ${prim_dev}  ${Image_list}[1]
    Step  3   activitate whitebox FW mode 0xf ESM A  ${prim_dev}
    Step  4   upgrade whitebox FW with mode 0xe ESM B nebula  ${non_prim_dev}  ${Image_list}[0]
    Step  5   upgrade whitebox FW with mode 0xe ESM B nebula  ${non_prim_dev}  ${Image_list}[1]
    Step  6   activitate whitebox FW mode 0xf ESM B  ${non_prim_dev}
    Step  7   Reboot_OS_via_MGMT    %{DUT_username}  %{DUT_ipv4_ip}  %{DUT_password}  reboot
    server Disconnect
    set time delay  130
    Step  8   check upgrade FW version ESM A nebula
    Step  9   check upgrade FW version ESM B nebula
    Server Connect 1
    Step  10  check info nebula  ${prim_dev}
    Step  11  check info nebula  ${non_prim_dev}
    server Disconnect

upgrade whitebox FW with mode 0xe ESM A nebula
    [Arguments]    ${sg_device_1}  ${image}    
    Step  1  update_whitebox_fw_force  SES  ${download_microcode_modeE_cmd_nebula}  %{DUT_username}  %{DUT_ipv4_ip}  %{DUT_password}  ${sg_device_1}  True  ${image}

upgrade whitebox FW with mode 0xe ESM B nebula
    [Arguments]    ${sg_device_2}  ${image}    
    Step  1  update_whitebox_fw_force  SES  ${download_microcode_modeE_cmd_nebula}  %{DUT_username}  %{DUT_ipv4_ip}  %{DUT_password}  ${sg_device_2}  True  ${image}

check upgrade FW version ESM A nebula
    Step  1  OS Connect Device
    Step  2  verify_ses_version_fru_get_nebula  DUT  isUpgrade=True
    Step  3  OS Disconnect Device
	
check upgrade FW version ESM B nebula
    Step  1  ConnectESMB
    Step  2  verify_ses_version_fru_get_nebula  DUT  isUpgrade=True
    Step  3  OS Disconnect Device

check info nebula
    [Arguments]    ${sg_device_1}
    ${Disc_count_output} =   execute_Linux_command   ${cmd_check_disk_num_nebula}
    common_check_patern_2       ${Disc_count_output}    ${expected_disk_count}   FRU Area size check   expect=True
    verify_sbb_mode  %{DUT_username}  %{DUT_ipv4_ip}  %{DUT_password}  ${sg_device_1}  0

downgrade FW with mode 0xe + mode 0xf nebula
    Server Connect 1
    ${prim_dev} =   get_primary_device_nebula    %{DUT_username}  %{DUT_ipv4_ip}  %{DUT_password}
    Log  ${prim_dev}
    ${non_prim_dev} =   get_non_primary_device_nebula    %{DUT_username}  %{DUT_ipv4_ip}  %{DUT_password}
    Log  ${non_prim_dev}
    ${Image_list}=  getFWImage    upgrade=False
    Log  ${Image_list}
    Step  1   upgrade whitebox FW with mode 0xe ESM A nebula  ${prim_dev}  ${Image_list}[0]
    Step  2   upgrade whitebox FW with mode 0xe ESM A nebula  ${prim_dev}  ${Image_list}[1]
    Step  3   activitate whitebox FW mode 0xf ESM A  ${prim_dev}
    Step  4   upgrade whitebox FW with mode 0xe ESM B nebula  ${non_prim_dev}  ${Image_list}[0]
    Step  5   upgrade whitebox FW with mode 0xe ESM B nebula  ${non_prim_dev}  ${Image_list}[1]
    Step  6   activitate whitebox FW mode 0xf ESM B  ${non_prim_dev}
    Step  7   Reboot_OS_via_MGMT    %{DUT_username}  %{DUT_ipv4_ip}  %{DUT_password}  reboot
    server Disconnect
    set time delay  130
    Step  8   check downgrade FW version ESM A nebula
    Step  9  check downgrade FW version ESM B nebula
    Server Connect 1
    Step  10  check info nebula  ${prim_dev}
    Step  11  check info nebula  ${non_prim_dev}
    server Disconnect

check downgrade FW version ESM A nebula
    Step  1  OS Connect Device
    Step  2  verify_ses_version_fru_get_nebula  DUT  isUpgrade=False
    Step  3  OS Disconnect Device

check downgrade FW version ESM B nebula
    Step  1  ConnectESMB
    Step  2  verify_ses_version_fru_get_nebula  DUT  isUpgrade=False
    Step  3  OS Disconnect Device

check Temperature Alarm nebula
    [Arguments]  ${HDD}  ${alarm_level}
    Log  ${HDD}
    ${SENSORS}=  list Temperature Sensor  ${HDD}
    ${TEMPER_VALUE}=  get Sensor Temperature  ${SENSORS}[0]  ${HDD}
    ${THRESHOLDs}=  getTemperThreshold  ${SENSORS}[0]  ${HDD}
    set Test Variable  ${HDD}  ${HDD}
    set Test Variable  ${SENSOR}  ${SENSORS}[0]
    set Test Variable  ${THRESHOLDs}  ${THRESHOLDs}
    set Temper Threshold  ${SENSORS}[0]  ${HDD}  ${TEMPER_VALUE}  ${alarm_level}
    getTemperThreshold  ${SENSORS}[0]  ${HDD}
    Sleep  30
    check Alarm Bit  ${SENSORS}[0]  ${HDD}  ${alarm_level}

check String In Diagnostic Pages(05h) nebula
    ${nebula_devices}=  get_device_list_nebula    %{DUT_username}  %{DUT_ipv4_ip}  %{DUT_password}
    set Test Variable  ${sg_device_1}  ${nebula_devices}[0]
    set Test Variable  ${sg_device_2}  ${nebula_devices}[1]
    Step  1  verify_ses_page_05  %{DUT_username}  %{DUT_ipv4_ip}  %{DUT_password}  ${sg_device_1}
    Step  2  verify_ses_page_05  %{DUT_username}  %{DUT_ipv4_ip}  %{DUT_password}  ${sg_device_2}

check Descriptor Length nebula
    Server Connect 1
    ${HDDs}=  get_device_list_nebula    %{DUT_username}  %{DUT_ipv4_ip}  %{DUT_password}
    Log  ${HDDs}[0]
    Log  ${FRU_INFO}
    verify Descriptor Length  ${HDDs}[0]  ${FRU_INFO}
    server Disconnect

check Descriptor Length nebula ESM B
    Server Connect 1
    ${HDDs}=  get_device_list_nebula    %{DUT_username}  %{DUT_ipv4_ip}  %{DUT_password}
    Log  ${HDDs}[1]
    Log  ${FRU_INFO}
    verify Descriptor Length  ${HDDs}[1]  ${FRU_INFO}
    server Disconnect

check String In Diagnostic Pages(04h) nebula
    ${nebula_devices}=  get_device_list_nebula    %{DUT_username}  %{DUT_ipv4_ip}  %{DUT_password}
    set Test Variable  ${sg_device_1}  ${nebula_devices}[0]
    set Test Variable  ${sg_device_2}  ${nebula_devices}[1]
    Step  1  OS Connect Device
    ${expect_ESMA_up_time} =  get_esm_up_time  DUT
    Step  2  OS Disconnect Device
    Step  3  ConnectESMB
    ${expect_ESMB_up_time} =  get_esm_up_time  DUT
    Step  4  OS Disconnect Device
    verify_ses_page_04_nebula  %{DUT_username}  %{DUT_ipv4_ip}  %{DUT_password}  ${sg_device_1}
    verify_ses_page_04_nebula  %{DUT_username}  %{DUT_ipv4_ip}  %{DUT_password}  ${sg_device_2}

VPD update clean up
   OS Connect Device
   change_to_ESM_mode
   execute_ESM_command_1  vpd reset -c 0
   execute_ESM_command_1  vpd reset -d 0 1
   execute_ESM_command_1  vpd reset -d 1 1
   exit_ESM_mode
   OS Disconnect Device
   ConnectESMB
   change_to_ESM_mode
   execute_ESM_command_1  vpd reset -c 1
   execute_ESM_command_1  vpd reset -d 0 1
   execute_ESM_command_1  vpd reset -d 1 1
   exit_ESM_mode
   OS Disconnect Device
   Sleep  300
   AC Power Cycle the Device

check Fan current speed Titan G2 WB
    ${sg_device_1} =  get_devicename  %{DUT_username}  %{DUT_ipv4_ip}  %{DUT_password}  Zone1
    Step  1  verify_ses_page_02_fan_current_speed  %{DUT_username}  %{DUT_ipv4_ip}  %{DUT_password}  ${sg_device_1}  ${fan_speed_1}
    Step  2  OSConnect
    Step  3  verify_fan_speed_cli_command  DUT  ${fan_speed_cli_1}
    Step  4  verify_esm_fan_mode_cli_command  DUT  external
    Step  5  OSDisconnect
    Step  6  verify_ses_page_02_fan_current_speed  %{DUT_username}  %{DUT_ipv4_ip}  %{DUT_password}  ${sg_device_1}  ${fan_speed_2}
    Step  7  OSConnect
    Step  8  verify_fan_speed_cli_command  DUT  ${fan_speed_cli_2}
    Step  9  verify_esm_fan_mode_cli_command  DUT  external
    Step  10  OSDisconnect
    Step  11  set_ses_page_02_fan_speed  %{DUT_username}  %{DUT_ipv4_ip}  %{DUT_password}  ${sg_device_1}  ${fan_speed_2}
    Step  12  get_ses_page_02_fan_speed  %{DUT_username}  %{DUT_ipv4_ip}  %{DUT_password}  ${sg_device_1}  ${fan_speed_2}
    Step  13  OSConnect
    Step  14  verify_fan_speed_cli_command  DUT  ${fan_speed_cli_2}
    Step  15  verify_esm_fan_mode_cli_command  DUT  external
    Step  16  OSDisconnect

check Fan current speed ESMB Titan G2 WB
    ${sg_device_1} =  get_devicename  %{DUT_username}  %{DUT_ipv4_ip}  %{DUT_password}  Zone1
    Step  1  verify_ses_page_02_fan_current_speed  %{DUT_username}  %{DUT_ipv4_ip}  %{DUT_password}  ${sg_device_1}  ${fan_speed_1}
    Step  2  ConnectESMB
    Step  3  verify_fan_speed_cli_command  DUT  ${fan_speed_cli_1}
    Step  4  verify_esm_fan_mode_cli_command  DUT  external
    Step  5  OSDisconnect
    Step  6  verify_ses_page_02_fan_current_speed  %{DUT_username}  %{DUT_ipv4_ip}  %{DUT_password}  ${sg_device_1}  ${fan_speed_2}
    Step  7  ConnectESMB
    Step  8  verify_fan_speed_cli_command  DUT  ${fan_speed_cli_2}
    Step  9  verify_esm_fan_mode_cli_command  DUT  external
    Step  10  OSDisconnect
    Step  11  set_ses_page_02_fan_speed  %{DUT_username}  %{DUT_ipv4_ip}  %{DUT_password}  ${sg_device_1}  ${fan_speed_2}
    Step  12  get_ses_page_02_fan_speed  %{DUT_username}  %{DUT_ipv4_ip}  %{DUT_password}  ${sg_device_1}  ${fan_speed_2}
    Step  13  ConnectESMB
    Step  14  verify_fan_speed_cli_command  DUT  ${fan_speed_cli_2}
    Step  15  verify_esm_fan_mode_cli_command  DUT  external
    Step  16  OSDisconnect

check Fan min speed Titan G2 WB
    ${sg_device_1} =  get_devicename  %{DUT_username}  %{DUT_ipv4_ip}  %{DUT_password}  Zone1
    Step  1  verify_ses_page_02_fan_current_speed  %{DUT_username}  %{DUT_ipv4_ip}  %{DUT_password}  ${sg_device_1}  ${fan_min_speed}
    Step  2  OSConnect
    Step  3  verify_fan_speed_cli_command  DUT  ${fan_min_speed_cli}
    Step  4  verify_esm_fan_mode_cli_command  DUT  external
    Step  5  OSDisconnect
    Step  6  verify_ses_page_02_fan_current_speed  %{DUT_username}  %{DUT_ipv4_ip}  %{DUT_password}  ${sg_device_1}  ${fan_max_speed}
    Step  2  OSConnect
    Step  8  verify_fan_speed_cli_command  DUT  ${fan_max_speed_cli}
    Step  9  verify_esm_fan_mode_cli_command  DUT  external
    Step  10  OSDisconnect
    Step  11  verify_ses_page_02_fan_current_speed  %{DUT_username}  %{DUT_ipv4_ip}  %{DUT_password}  ${sg_device_1}  ${fan_min_speed}
    Step  12  OSConnect
    Step  13  verify_fan_speed_cli_command  DUT  ${fan_min_speed_cli}
    Step  14  verify_esm_fan_mode_cli_command  DUT  external
    Step  15  OSDisconnect

check Fan min speed ESMB Titan G2 WB
    ${sg_device_1} =  get_devicename  %{DUT_username}  %{DUT_ipv4_ip}  %{DUT_password}  Zone1
    Step  1  verify_ses_page_02_fan_current_speed  %{DUT_username}  %{DUT_ipv4_ip}  %{DUT_password}  ${sg_device_1}  ${fan_min_speed}
    Step  2  ConnectESMB
    Step  3  verify_fan_speed_cli_command  DUT  ${fan_min_speed_cli}
    Step  4  verify_esm_fan_mode_cli_command  DUT  external
    Step  5  OSDisconnect
    Step  6  verify_ses_page_02_fan_current_speed  %{DUT_username}  %{DUT_ipv4_ip}  %{DUT_password}  ${sg_device_1}  ${fan_max_speed}
    Step  7  ConnectESMB
    Step  8  verify_fan_speed_cli_command  DUT  ${fan_max_speed_cli}
    Step  9  verify_esm_fan_mode_cli_command  DUT  external
    Step  10  OSDisconnect
    Step  11  verify_ses_page_02_fan_current_speed  %{DUT_username}  %{DUT_ipv4_ip}  %{DUT_password}  ${sg_device_1}  ${fan_min_speed}
    Step  12  ConnectESMB
    Step  13  verify_fan_speed_cli_command  DUT  ${fan_min_speed_cli}
    Step  14  verify_esm_fan_mode_cli_command  DUT  external
    Step  15  OSDisconnect

check Fan max speed Titan G2 WB
    ${sg_device_1} =  get_devicename  %{DUT_username}  %{DUT_ipv4_ip}  %{DUT_password}  Zone1
    Step  1  verify_ses_page_02_fan_current_speed  %{DUT_username}  %{DUT_ipv4_ip}  %{DUT_password}  ${sg_device_1}  ${fan_speed_1}
    Step  2  OSConnect
    Step  3  verify_fan_speed_cli_command  DUT  ${fan_speed_cli_1}
    Step  4  verify_esm_fan_mode_cli_command  DUT  external
    Step  5  OSDisconnect
    Step  6  verify_ses_page_02_fan_current_speed  %{DUT_username}  %{DUT_ipv4_ip}  %{DUT_password}  ${sg_device_1}  ${fan_max_speed}
    Step  7  OSConnect
    Step  8  verify_fan_speed_cli_command  DUT  ${fan_max_speed_cli}
    Step  9  verify_esm_fan_mode_cli_command  DUT  external
    Step  10  OSDisconnect
    Step  11  verify_ses_page_02_fan_current_speed  %{DUT_username}  %{DUT_ipv4_ip}  %{DUT_password}  ${sg_device_1}  ${fan_speed_1}
    Step  12  OSConnect
    Step  13  verify_fan_speed_cli_command  DUT  ${fan_speed_cli_1}
    Step  14  verify_esm_fan_mode_cli_command  DUT  external
    Step  15  OSDisconnect

check Fan max speed ESMB Titan G2 WB
    ${sg_device_1} =  get_devicename  %{DUT_username}  %{DUT_ipv4_ip}  %{DUT_password}  Zone1
    Step  1  verify_ses_page_02_fan_current_speed  %{DUT_username}  %{DUT_ipv4_ip}  %{DUT_password}  ${sg_device_1}  ${fan_speed_1}
    Step  2  ConnectESMB
    Step  3  verify_fan_speed_cli_command  DUT  ${fan_speed_cli_1}
    Step  4  verify_esm_fan_mode_cli_command  DUT  external
    Step  5  OSDisconnect
    Step  6  verify_ses_page_02_fan_current_speed  %{DUT_username}  %{DUT_ipv4_ip}  %{DUT_password}  ${sg_device_1}  ${fan_max_speed}
    Step  2  ConnectESMB
    Step  8  verify_fan_speed_cli_command  DUT  ${fan_max_speed_cli}
    Step  9  verify_esm_fan_mode_cli_command  DUT  external
    Step  10  OSDisconnect
    Step  11  verify_ses_page_02_fan_current_speed  %{DUT_username}  %{DUT_ipv4_ip}  %{DUT_password}  ${sg_device_1}  ${fan_speed_1}
    Step  12  ConnectESMB
    Step  13  verify_fan_speed_cli_command  DUT  ${fan_speed_cli_1}
    Step  14  verify_esm_fan_mode_cli_command  DUT  external
    Step  15  OSDisconnect

get FRU Info Titan G2 WB
    OSConnect
    verify esm mode cli command  DUT
    ${FRU_INFO}=  run ESM command  fru get
    OS Disconnect Device
    set Test Variable  ${FRU_INFO}  ${FRU_INFO}

get FRU Info ESMB Titan G2 WB
    ConnectESMB
    verify esm mode cli command  DUT
    ${FRU_INFO}=  run ESM command  fru get
    OS Disconnect Device
    set Test Variable  ${FRU_INFO}  ${FRU_INFO}

check Descriptor Length Titan G2 WB
    Server Connect 1
    ${HDDs}=  query SG Devices
    verify Descriptor Length  ${HDDs}[0]  ${FRU_INFO}
    server Disconnect

Download SES FW File And Update Titan G2 WB
    [Arguments]  ${UPGRADE}
    Server Connect 1
#    change_directory   DUT  "/root/Titan-g2-wb/SES/2.1.2.31"
    download Ses Fw Image  upgrade=${UPGRADE}
    ${HDDs}=  query SG Devices
    Log  ${HDDs}
    Log  ${HDDs}[0]
    Log  ${HDDs}[1]
    update Ses Fw  ${HDDs}[0]  upgrade=${UPGRADE}
    Sleep  60
    ${HDDs}=  query SG Devices
    Log  ${HDDs}
    Log  ${HDDs}[0]
    Log  ${HDDs}[1]
    update Ses Fw  ${HDDs}[1]  upgrade=${UPGRADE}
    server Disconnect
    Sleep  30
    set Test Variable   ${HDDs}  ${HDDs}

upgrade FW with mode 0xe + mode 0xf Titan G2 WB
    Step  1  upgrade whitebox FW with mode 0xe
    Step  2  activitate whitebox FW mode 0xf
    Step  3  check upgrade FW version

check String In Diagnostic Pages(04h) Titan G2 WB
    ${sg_device_1} =  get_devicename  %{DUT_username}  %{DUT_ipv4_ip}  %{DUT_password}
    #Step  1  ESMAConnect  ${ESMA IP}  ${ESMA port}
    Step  1  OS Connect Device
    ${expect_ESMA_up_time} =  get_esm_up_time  DUT
    Step  2  OS Disconnect Device
    #Step  2  Disconnect
    #Step  3  ESMAConnect  ${ESMB IP}  ${ESMB port}
    Step  3   ConnectESMB
    ${expect_ESMB_up_time} =  get_esm_up_time  DUT
    #Step  4  Disconnect
    Step  4  OS Disconnect Device
    verify_ses_page_04_lenovo  %{DUT_username}  %{DUT_ipv4_ip}  %{DUT_password}  ${sg_device_1}  ${expect_ESMA_IP_lenovo}  ${expect_gateway_lenovo}
          ...  ${expect_ESM_A_DHCP_Mode_lenovo}  ${expect_ESMA_up_time}   ${expect_ESMB_up_time}  ${expect_ESM_Zoning_Mode_titan_g2_wb}   ${expect_ESMB_IP_lenovo}  ${expect_ESM_B_DHCP_Mode_lenovo}  ${expect_netmask}

upgrade FW with mode 0xe + reset 00h code Titan G2 WB
    Server Connect 1
    ${prim_dev} =   get_primary_device
    Log  ${prim_dev}
    ${non_prim_dev} =   get_non_primary_device
    Log  ${non_prim_dev}
    server Disconnect
    Step  1  upgrade whitebox FW with mode 0xe ESM A  ${prim_dev}
    Step  2  activitate whitebox FW reset 00h ESM A  ${prim_dev}
    Step  3  check upgrade FW version ESM A
    Server Connect 1
    ${non_prim_dev} =   get_non_primary_device
    Log  ${non_prim_dev}
    server Disconnect
    Step  4  upgrade whitebox FW with mode 0xe ESM B  ${non_prim_dev}
    Step  5  activitate whitebox FW reset 00h ESM B  ${non_prim_dev}
    Step  6  check upgrade FW version ESM B
    Server Connect 1
    ${prim_dev} =   get_primary_device
    Log  ${prim_dev}
    ${non_prim_dev} =   get_non_primary_device
    Log  ${non_prim_dev}
    server Disconnect

verify command code and data reset Titan G2 WB
   server Connect
   ${sg_device_1} =   get_primary_device
   Log  ${sg_device_1}
   ${sg_device_2} =   get_non_primary_device
   Log  ${sg_device_2}
   check local expander reset   ${reset_all_expanders_cmd}  ${sg_device_1}
   sleep  5 s
   Server Disconnect

   server Connect
   ${sg_device_1} =   get_primary_device
   Log  ${sg_device_1}
   ${sg_device_2} =   get_non_primary_device
   Log  ${sg_device_2}
   check local expander reset   ${reset_expanders_in_ESMA_cmd}  ${sg_device_1}
   sleep  5 s
   Server Disconnect

   server Connect
   ${sg_device_1} =   get_primary_device
   Log  ${sg_device_1}
   ${sg_device_2} =   get_non_primary_device
   Log  ${sg_device_2}
   check local expander reset  ${reset_peer_ESM_cmd}  ${sg_device_2}
   sleep  5 s
   Server Disconnect

   server Connect
   ${sg_device_1} =   get_primary_device
   Log  ${sg_device_1}
   ${sg_device_2} =   get_non_primary_device
   Log  ${sg_device_2}
   check local expander reset B  ${reset_all_expanders_cmd}  ${sg_device_2}
   sleep  5 s
   Server Disconnect

   server Connect
   ${sg_device_1} =   get_primary_device
   Log  ${sg_device_1}
   ${sg_device_2} =   get_non_primary_device
   Log  ${sg_device_2}
   check local expander reset B  ${reset_expanders_in_ESMB_cmd}  ${sg_device_2}
   sleep  5 s
   Server Disconnect

   server Connect
   ${sg_device_1} =   get_primary_device
   Log  ${sg_device_1}
   ${sg_device_2} =   get_non_primary_device
   Log  ${sg_device_2}
   check local expander reset B  ${reset_peer_ESM_cmd}  ${sg_device_1}
   sleep  5 s
   Server Disconnect

upgrade cpld via SES Page - mode 0xe and 0xf Titan G2 WB
    check esm mode status
    Download CPLD FW File
    upgrade cpld with mode 0xe + mode 0xf Titan G2 WB
    check esm mode status

upgrade cpld via SES Page - mode 0xe and reset 00h Titan G2 WB
    check esm mode status
    Download CPLD FW File
    upgrade cpld with mode 0xe + reset 00h Titan G2 WB
    check esm mode status

Temperature lm Upgrade Test Titan G2 WB
    [Arguments]   ${num}  ${pattern}
    server Connect
    ${HDDs}=  query SG Devices
    temp lm upgrade test  ${num}  ${pattern}  ${HDDs}[${num}]
    Server Disconnect


check esm mode status Athena
    OS Connect Device
    change_to_ESM_mode   
    verify esm mode cli command  DUT
    exit_ESM_mode
    OS Disconnect Device    

check SCISI Elements Athena
    [Arguments]  ${check_cmd}  ${check_pattern}
    ${sg_device_1} =   get_primary_device
    Log  ${sg_device_1}
    run And Check  ${check_cmd} ${sg_device_1}  ${check_pattern}

check Enclosure Length Athena
    [Arguments]  ${query_cmd}  ${query_pattern}  ${length_dict}
    ${sg_device_1} =   get_primary_device
    Log  ${sg_device_1}
    check Return Data  ${sg_device_1}  ${query_cmd}  ${query_pattern}  ${length_dict}

check Command Sent Athena
    [Arguments]  ${check_cmd}  ${check_pattern}
    ${sg_device_1} =   get_primary_device
    Log  ${sg_device_1}
    run And Check  ${check_cmd} ${sg_device_1}  ${check_pattern}  is_negative=True

send A Command Athena1
   [Arguments]   ${cmd}
   ${sg_device_1} =   get_primary_device
   Log  ${sg_device_1}   
   command run   ${cmd}  ${sg_device_1}

verify Page Status Athena
   [Arguments]   ${cmd}
   ${sg_device_1} =   get_primary_device
   Log  ${sg_device_1}  
   checkLogPageStatus   ${cmd}  ${sg_device_1}

check Temperature Alarm On Page5 Athena
    [Arguments]    ${alarm_level}
    ${sg_device_1} =   get_primary_device
    Log  ${sg_device_1}    
    ${SENSORS}=  list Temperature Sensor  ${sg_device_1}
    ${TEMPER_VALUE}=  get Sensor Temperature  ${SENSORS}[0]  ${sg_device_1}
    ${THRESHOLDs}=  getTemperThreshold  ${SENSORS}[0]  ${sg_device_1}
    set Test Variable  ${HDD}  ${sg_device_1}
    set Test Variable  ${SENSOR}  ${SENSORS}[0]
    set Test Variable  ${THRESHOLDs}  ${THRESHOLDs}
    ${setting_value}=  set Temper Threshold  ${SENSORS}[0]  ${sg_device_1}   ${TEMPER_VALUE}  ${alarm_level}
    check Sensor Value On Page5  ${SENSORS}[0]  ${sg_device_1}   ${alarm_level}
    ...  ${setting_value}
    getTemperThreshold  ${SENSORS}[0]  ${sg_device_1}
    check Alarm Bit  ${SENSORS}[0]  ${sg_device_1}   ${alarm_level}

check Temperature Alarm Athena
    [Arguments]    ${alarm_level}
    ${sg_device_1} =   get_primary_device
    Log  ${sg_device_1}
    ${SENSORS}=  list Temperature Sensor  ${sg_device_1}
    ${TEMPER_VALUE}=  get Sensor Temperature  ${SENSORS}[0]  ${sg_device_1}
    ${THRESHOLDs}=  getTemperThreshold  ${SENSORS}[0]  ${sg_device_1}
    set Test Variable  ${HDD}  ${sg_device_1}
    set Test Variable  ${SENSOR}  ${SENSORS}[0]
    set Test Variable  ${THRESHOLDs}  ${THRESHOLDs}
    set Temper Threshold  ${SENSORS}[0]  ${sg_device_1}  ${TEMPER_VALUE}  ${alarm_level}
    Log  ${HDD}
    getTemperThreshold  ${SENSORS}[0]  ${sg_device_1}
    check Alarm Bit  ${SENSORS}[0]  ${sg_device_1}  ${alarm_level}


check Array OK Bit Athena
    ${sg_device_1} =   get_primary_device
    ${DEVICEs}=  list Array Devices  ${sg_device_1}
    verify RQST Fault Bit  ${sg_device_1}  ${DEVICEs}[0]



check slot name format Athena
   [Arguments]   ${cmd}
   ${sg_device_1} =   get_primary_device
   Verify slot name format  ${cmd}  ${sg_device_1}

check Disks Info On Page 0x0a Athena
    server Connect
    ${sg_device_1} =   get_primary_device
    verify Disk Info   ${sg_device_1}
    Server Disconnect
    server connect ESMB
    ${sg_device_1} =   get_primary_device
    verify Disk Info   ${sg_device_1}
    Server Disconnect

check Cooling external Mode ESMA Athena
    server Connect
    ${sg_device_1} =   get_primary_device
    Server Disconnect
    Step  1  verify_ses_page_02_cooling_Mode  %{DUT_username}  %{DUT_ipv4_ip}  %{DUT_password}  ${sg_device_1}  external
    Step  2  OS Connect Device
    Step  3  change_to_ESM_mode
    Step  4  verify_esm_fan_mode_cli_command  DUT  external
    Step  5  exit_ESM_mode
    Step  6  OS Disconnect Device

check Cooling external Mode ESMB Athena
    server connect ESMB
    ${sg_device_1} =   get_primary_device
    Server Disconnect
    Step  1  verify_ses_page_02_cooling_Mode  %{DUT_username}  %{DUT_ipv4_ip_ESMB}  %{DUT_password}  ${sg_device_1}  external
    Step  2  ConnectESMB
    Step  3  change_to_ESM_mode
    Step  4  verify_esm_fan_mode_cli_command  DUT  external
    Step  5  exit_ESM_mode
    Step  6  OS Disconnect Device

check esm mode status ESMB Athena
    ConnectESMB
    change_to_ESM_mode
    verify esm mode cli command  DUT
    exit_ESM_mode
    OS Disconnect Device

get dut variable ESMB
    ${DUT_ipv4_ip} =  get_deviceinfo_from_config  UUT  esmbManagementIP
    Set Environment Variable  DUT_ipv4_ip_ESMB  ${DUT_ipv4_ip}
    
check Cooling internal Mode ESMA Athena
    server Connect
    ${sg_device_1} =   get_primary_device
    Server Disconnect
    Step  1  verify_ses_page_02_cooling_Mode  %{DUT_username}  %{DUT_ipv4_ip}  %{DUT_password}  ${sg_device_1}  internal
    Step  2  OS Connect Device
    Step  3  change_to_ESM_mode
    Step  4  verify_esm_fan_mode_cli_command  DUT  internal
    Step  5  exit_ESM_mode
    Step  6  OS Disconnect Device

check Cooling internal Mode ESMB Athena
    server connect ESMB
    ${sg_device_1} =   get_primary_device
    Server Disconnect
    Step  1  verify_ses_page_02_cooling_Mode  %{DUT_username}  %{DUT_ipv4_ip_ESMB}  %{DUT_password}  ${sg_device_1}  internal
    Step  2  ConnectESMB
    Step  3  change_to_ESM_mode
    Step  4  verify_esm_fan_mode_cli_command  DUT  internal
    Step  5  exit_ESM_mode
    Step  6  OS Disconnect Device


compare PSU status with CLI ESMA Athena
   [Arguments]   ${cmd}   ${psu_cli_pattern}
   server Connect
   ${sg_device_1} =   get_primary_device
   ${psu_page_output} =  execute_Linux_command   ${cmd} ${sg_device_1}
   Server Disconnect
   OS Connect Device
   check PSU Details With CLI_athena   ${psu_page_output}   ${psu_cli_pattern}  DUT
   OS Disconnect Device

compare PSU status with CLI ESMB Athena
   [Arguments]   ${cmd}   ${psu_cli_pattern}
   server connect ESMB
   ${sg_device_1} =   get_primary_device
   ${psu_page_output} =  execute_Linux_command   ${cmd} ${sg_device_1}
   Server Disconnect
   ConnectESMB
   check PSU Details With CLI_athena   ${psu_page_output}   ${psu_cli_pattern}  DUT
   OS Disconnect Device

verify Drive Disk Power Athena
    ${No_of_drives}=  get number of drives
    ${sg_device_1} =   get_primary_device
    ${sg_device_2} =   get_non_primary_device
    check drive disk power   ${set_drivedisk_power_off_cmd}   ${get_drivedisk_power_cmd}  ${sg_device_1}  ${sg_device_2}   ${No_of_drives}   ${device_on_pattern}
    check drive disk power   ${set_drivedisk_power_on_cmd}   ${get_drivedisk_power_cmd}  ${sg_device_1}  ${sg_device_2}  ${No_of_drives}   ${device_off_pattern}


Enclosure Status Diagnostic Pages(02h) Athena ESMA
    server Connect
    ${sg_device_1} =   get_primary_device
    ${sg_device_2} =   get_non_primary_device
    Server Disconnect
    ${ses_fw_version} =  get_ses_fw_version_by_ses_page_01h  %{DUT_username}  %{DUT_ipv4_ip}  %{DUT_password}  ${sg_device_1}
    Step  1  create_gold_file  %{DUT_username}  %{DUT_ipv4_ip}  %{DUT_password}
          ...  sg_ses --page=0x02 ${sg_device_1}|grep -v '${ses_fw_version}'|grep -v rpm|grep -v Voltage:|grep -v amps|grep -v Temperature=|grep -v INFO  ${ses_page_02h_gold_file_1}
    Step  2  create_gold_file  %{DUT_username}  %{DUT_ipv4_ip}  %{DUT_password}
          ...  sg_ses --page=0x02 ${sg_device_2}|grep -v '${ses_fw_version}'|grep -v rpm|grep -v Voltage:|grep -v amps|grep -v Temperature=|grep -v INFO  ${ses_page_02h_gold_file_2}
    Step  3  create_gold_file  %{DUT_username}  %{DUT_ipv4_ip}  %{DUT_password}
          ...  sg_ses --page=0x02 ${sg_device_1}|grep -v rpm|grep -v Voltage:|grep -v amps|grep -v Temperature=|grep -v INFO|grep -v '${ses_fw_version}'  ${ses_page_tmp_file}
    Step  4  compare_file  ${ses_page_02h_gold_file_1}  ${ses_page_tmp_file}
    Step  5  create_gold_file  %{DUT_username}  %{DUT_ipv4_ip}  %{DUT_password}
          ...  sg_ses --page=0x02 ${sg_device_2}|grep -v rpm|grep -v Voltage:|grep -v amps|grep -v Temperature=|grep -v INFO|grep -v '${ses_fw_version}'  ${ses_page_tmp_file}
    Step  6  compare_file  ${ses_page_02h_gold_file_2}  ${ses_page_tmp_file}

Enclosure Status Diagnostic Pages(02h) Athena ESMB
    server connect ESMB
    ${sg_device_1} =   get_primary_device
    ${sg_device_2} =   get_non_primary_device
    Server Disconnect
    ${ses_fw_version} =  get_ses_fw_version_by_ses_page_01h  %{DUT_username}  %{DUT_ipv4_ip_ESMB}  %{DUT_password}  ${sg_device_1}
    Step  1  create_gold_file  %{DUT_username}  %{DUT_ipv4_ip_ESMB}  %{DUT_password}
          ...  sg_ses --page=0x02 ${sg_device_1}|grep -v '${ses_fw_version}'|grep -v rpm|grep -v Voltage:|grep -v amps|grep -v Temperature=|grep -v INFO  ${ses_page_02h_gold_file_1_ESMB}
    Step  2  create_gold_file  %{DUT_username}  %{DUT_ipv4_ip_ESMB}  %{DUT_password}
          ...  sg_ses --page=0x02 ${sg_device_2}|grep -v '${ses_fw_version}'|grep -v rpm|grep -v Voltage:|grep -v amps|grep -v Temperature=|grep -v INFO  ${ses_page_02h_gold_file_2_ESMB}
    Step  3  create_gold_file  %{DUT_username}  %{DUT_ipv4_ip_ESMB}  %{DUT_password}
          ...  sg_ses --page=0x02 ${sg_device_1}|grep -v rpm|grep -v Voltage:|grep -v amps|grep -v Temperature=|grep -v INFO|grep -v '${ses_fw_version}'  ${ses_page_tmp_file}
    Step  4  compare_file  ${ses_page_02h_gold_file_1_ESMB}  ${ses_page_tmp_file}
    Step  5  create_gold_file  %{DUT_username}  %{DUT_ipv4_ip_ESMB}  %{DUT_password}
          ...  sg_ses --page=0x02 ${sg_device_2}|grep -v rpm|grep -v Voltage:|grep -v amps|grep -v Temperature=|grep -v INFO|grep -v '${ses_fw_version}'  ${ses_page_tmp_file}
    Step  6  compare_file  ${ses_page_02h_gold_file_2_ESMB}  ${ses_page_tmp_file}

Create ses page gold file ESMB
    server Connect ESMB    
    ${sg_device_1} =   get_primary_device
    Log  ${sg_device_1}
    ${sg_device_2} =   get_non_primary_device
    Log  ${sg_device_2}
    Server Disconnect
    ${ses_fw_version} =  get_ses_fw_version_by_ses_page_01h  %{DUT_username}  %{DUT_ipv4_ip_ESMB}  %{DUT_password}  ${sg_device_1}
    ${cpld_version_1} =  get_cpld_version_ses_page  %{DUT_username}  %{DUT_ipv4_ip_ESMB}  %{DUT_password}  ${sg_device_1}  isUpgrade=True
    ${cpld_version_2} =  get_cpld_version_ses_page  %{DUT_username}  %{DUT_ipv4_ip_ESMB}  %{DUT_password}  ${sg_device_1}  isUpgrade=False
    Step  1  create_gold_file  %{DUT_username}  %{DUT_ipv4_ip_ESMB}  %{DUT_password}
          ...  sg_ses --page=0x01 ${sg_device_1}|grep -v '${ses_fw_version}'  ${ses_page_01h_gold_file_ESMB}
    Step  2  create_gold_file  %{DUT_username}  %{DUT_ipv4_ip_ESMB}  %{DUT_password}
          ...  sg_ses --page=0x01 ${sg_device_2}|grep -v '${ses_fw_version}'  ${ses_page_01h_gold_file_2_ESMB}

    Step  3  create_gold_file  %{DUT_username}  %{DUT_ipv4_ip_ESMB}  %{DUT_password}
          ...  sg_ses --page=0x02 ${sg_device_1}|grep -v '${ses_fw_version}'|grep -v rpm|grep -v Voltage:|grep -v amps|grep -v Temperature=|grep -v INFO  ${ses_page_02h_gold_file_1_ESMB}
    Step  4  create_gold_file  %{DUT_username}  %{DUT_ipv4_ip_ESMB}  %{DUT_password}
          ...  sg_ses --page=0x02 ${sg_device_2}|grep -v '${ses_fw_version}'|grep -v rpm|grep -v Voltage:|grep -v amps|grep -v Temperature=|grep -v INFO  ${ses_page_02h_gold_file_2_ESMB}
    Step  5  create_gold_file  %{DUT_username}  %{DUT_ipv4_ip_ESMB}  %{DUT_password}
          ...  sg_ses --page=0x04 ${sg_device_1}|grep -v '${ses_fw_version}'  ${ses_page_04h_gold_file_ESMB}
    Step  6  create_gold_file  %{DUT_username}  %{DUT_ipv4_ip_ESMB}  %{DUT_password}
          ...  sg_ses --page=0x05 ${sg_device_1}|grep -v '${ses_fw_version}'  ${ses_page_05h_gold_file_ESMB}
    Step  7  create_gold_file  %{DUT_username}  %{DUT_ipv4_ip_ESMB}  %{DUT_password}
          ...  sg_ses --page=0x07 ${sg_device_1}|grep -v '${ses_fw_version}'|grep -v Secondary|grep -v Primary|grep -v ${cpld_version_1}|grep -v ${cpld_version_2}   ${ses_page_07h_gold_file_ESMB}
    Step  8  create_gold_file  %{DUT_username}  %{DUT_ipv4_ip_ESMB}  %{DUT_password}
          ...  sg_ses --page=0x0a ${sg_device_1}|grep -v '${ses_fw_version}'  ${ses_page_a_gold_file_1_ESMB}
    Step  9  create_gold_file  %{DUT_username}  %{DUT_ipv4_ip_ESMB}  %{DUT_password}
          ...  sg_ses --page=0x0a ${sg_device_2}|grep -v '${ses_fw_version}'  ${ses_page_a_gold_file_2_ESMB}
    Step  10  create_gold_file  %{DUT_username}  %{DUT_ipv4_ip_ESMB}  %{DUT_password}
          ...  sg_ses --page=0x0e ${sg_device_1}|grep -v '${ses_fw_version}'|grep -v offset  ${ses_page_e_gold_file_ESMB}

Compare ses page gold file ESMB
    server Connect ESMB
    ${sg_device_1} =   get_primary_device
    Log  ${sg_device_1}
    ${sg_device_2} =   get_non_primary_device
    Log  ${sg_device_2}
    Server Disconnect
    ${ses_fw_version} =  get_ses_fw_version_by_ses_page_01h  %{DUT_username}  %{DUT_ipv4_ip_ESMB}  %{DUT_password}  ${sg_device_1}
    ${cpld_version_1} =  get_cpld_version_ses_page  %{DUT_username}  %{DUT_ipv4_ip_ESMB}  %{DUT_password}  ${sg_device_1}  isUpgrade=True
    ${cpld_version_2} =  get_cpld_version_ses_page  %{DUT_username}  %{DUT_ipv4_ip_ESMB}  %{DUT_password}  ${sg_device_1}  isUpgrade=False
    Sleep  90
    Step  1  create_gold_file  %{DUT_username}  %{DUT_ipv4_ip_ESMB}  %{DUT_password}
          ...  sg_ses --page=0x01 ${sg_device_1}|grep -v '${ses_fw_version}'  ${ses_page_tmp_file}
    Step  2  compare_file  ${ses_page_01h_gold_file_ESMB}  ${ses_page_tmp_file}  ses_page_01h
    Sleep  60
    Step  3  create_gold_file  %{DUT_username}  %{DUT_ipv4_ip_ESMB}  %{DUT_password}
          ...  sg_ses --page=0x01 ${sg_device_2}|grep -v '${ses_fw_version}'  ${ses_page_tmp_file}
    Step  4  compare_file  ${ses_page_01h_gold_file_2_ESMB}  ${ses_page_tmp_file}  ses_page_01h
    Sleep  60
    Step  5  create_gold_file  %{DUT_username}  %{DUT_ipv4_ip_ESMB}  %{DUT_password}
          ...  sg_ses --page=0x02 ${sg_device_1}|grep -v '${ses_fw_version}'|grep -v rpm|grep -v Voltage:|grep -v amps|grep -v Temperature=|grep -v INFO  ${ses_page_tmp_file}
    Step  6  compare_file  ${ses_page_02h_gold_file_1_ESMB}  ${ses_page_tmp_file}  ses_page_02h_1
    Sleep  120
    Step  7  create_gold_file  %{DUT_username}  %{DUT_ipv4_ip_ESMB}  %{DUT_password}
          ...  sg_ses --page=0x02 ${sg_device_2}|grep -v '${ses_fw_version}'|grep -v rpm|grep -v Voltage:|grep -v amps|grep -v Temperature=|grep -v INFO  ${ses_page_tmp_file}
    Step  8  compare_file  ${ses_page_02h_gold_file_2_ESMB}  ${ses_page_tmp_file}  ses_page_02h_2
    Sleep  60
    Step  9  create_gold_file  %{DUT_username}  %{DUT_ipv4_ip_ESMB}  %{DUT_password}
          ...  sg_ses --page=0x05 ${sg_device_1}|grep -v '${ses_fw_version}'  ${ses_page_tmp_file}
    Step  10  compare_file  ${ses_page_05h_gold_file_ESMB}  ${ses_page_tmp_file}  ses_page_05h
    Sleep  60
    Step  11  create_gold_file  %{DUT_username}  %{DUT_ipv4_ip_ESMB}  %{DUT_password}
          ...  sg_ses --page=0x07 ${sg_device_1}|grep -v '${ses_fw_version}'|grep -v Secondary|grep -v Primary|grep -v ${cpld_version_1}|grep -v ${cpld_version_2}  ${ses_page_tmp_file}
    Step  12  compare_file  ${ses_page_07h_gold_file_ESMB}  ${ses_page_tmp_file}  ses_page_07h
    Sleep  60
    Step  13  create_gold_file  %{DUT_username}  %{DUT_ipv4_ip_ESMB}  %{DUT_password}
          ...  sg_ses --page=0x0a ${sg_device_1}|grep -v '${ses_fw_version}'  ${ses_page_tmp_file}
    Step  14  compare_file  ${ses_page_a_gold_file_1_ESMB}  ${ses_page_tmp_file}  ses_page_a_1
    Sleep  60
    Step  15  create_gold_file  %{DUT_username}  %{DUT_ipv4_ip_ESMB}  %{DUT_password}
          ...  sg_ses --page=0x0a ${sg_device_2}|grep -v '${ses_fw_version}'  ${ses_page_tmp_file}
    Step  16  compare_file  ${ses_page_a_gold_file_2_ESMB}  ${ses_page_tmp_file}  ses_page_a_2
    Sleep  60
    Step  17  create_gold_file  %{DUT_username}  %{DUT_ipv4_ip_ESMB}  %{DUT_password}
          ...  sg_ses --page=0x0e ${sg_device_1}|grep -v '${ses_fw_version}'|grep -v offset  ${ses_page_tmp_file}
    Step  18  compare_file  ${ses_page_e_gold_file_ESMB}  ${ses_page_tmp_file}  ses_page_e

compare log info with CLI Athena ESMA
   [Arguments]      ${cmd}
   ${sg_device_1} =   get_primary_device
   ${output} =  execute_Linux_command   ${cmd} ${sg_device_1}
   Server Disconnect
   OS Connect Device
   check log info with CLI Athena    ${output}  DUT
   OS Disconnect Device 

compare log info with CLI Athena ESMB
   [Arguments]      ${cmd}
   ${sg_device_1} =   get_primary_device
   ${output} =  execute_Linux_command   ${cmd} ${sg_device_1}
   Server Disconnect
   ConnectESMB
   check log info with CLI Athena    ${output}  DUT
   OS Disconnect Device

check fan speed Athena 
   [Arguments]   ${fan_speed}  ${cli_fan_speed}
   server Connect
   ${sg_device_1} =   get_primary_device
   Server Disconnect
   set_ses_page_02_fan_speed  %{DUT_username}  %{DUT_ipv4_ip}  %{DUT_password}  ${sg_device_1}  ${fan_speed}
   get_ses_page_02_fan_speed  %{DUT_username}  %{DUT_ipv4_ip}  %{DUT_password}  ${sg_device_1}  ${fan_speed}
   OS Connect Device
   change_to_ESM_mode  
   verify_fan_speed_cli_command     DUT    ${cli_fan_speed}   
   exit_ESM_mode
   OS Disconnect Device
   server connect ESMB
   ${sg_device_1} =   get_primary_device
   Server Disconnect
   set_ses_page_02_fan_speed  %{DUT_username}  %{DUT_ipv4_ip_ESMB}  %{DUT_password}  ${sg_device_1}  ${fan_speed}
   get_ses_page_02_fan_speed  %{DUT_username}  %{DUT_ipv4_ip_ESMB}  %{DUT_password}  ${sg_device_1}  ${fan_speed}
   ConnectESMB
   change_to_ESM_mode
   verify_fan_speed_cli_command     DUT    ${cli_fan_speed}
   exit_ESM_mode
   OS Disconnect Device

Download Athena FW FAULT image
    OS Connect Device
    downloadAthenaSesFwImage    DUT   FAULT_IMAGE_A
    OS Disconnect Device
    ConnectESMB
    downloadAthenaSesFwImage    DUT   FAULT_IMAGE_B
    OS Disconnect Device

Verify With FW Fault Image Under Mode E Athena ESMA
   OS Connect Device 
   ${CLI_version}=  get ESM Version And Check
    ...  version_pattern=${esm_fw_version_pattern}
   OS Disconnect Device
   server Connect
   ${sg_device_1} =   get_primary_device
   ${Fault_image_name} =  GetCanisterImageName   A0   FAULT_IMAGE_A   True
   download Microcode Athena    FAULT_IMAGE_A   ${Fault_image_name}   ${download_microcode_modeE_cmd_Athena}   ${sg_device_1}
  
   ${image_activation_log} =  execute_Linux_command    ${fw_active_cmd} ${sg_device_1}
   common_check_patern_2   ${image_activation_log}   ${fw_active_fail_msg_fault_image}   check fault image activation log  expect=True
   common_check_patern_2   ${image_activation_log}   sg_ses_mocrocode failed: Illegal request    check fault image activation log  expect=True

   Server Disconnect
   
   OS Connect Device
   ${output} =   verifyCLILogAthena
   common_check_patern_2    ${output}   Upgrade cmpl with Errs    Check error message for falut image   expect=True
   get ESM Version And Check
    ...  cmp_dict=${CLI_version}  version_pattern=${esm_fw_version_pattern}
   change_to_ESM_mode
   verify esm mode cli command  DUT
   exit_ESM_mode
   OS Disconnect Device

Verify With FW Fault Image Under Mode E Athena ESMB
   ConnectESMB
   ${CLI_version}=  get ESM Version And Check
    ...  version_pattern=${esm_fw_version_pattern}
   OS Disconnect Device
   server connect ESMB
   ${sg_device_1} =   get_primary_device
   ${Fault_image_name} =  GetCanisterImageName   A0   FAULT_IMAGE_A   True
   download Microcode Athena    FAULT_IMAGE_A   ${Fault_image_name}   ${download_microcode_modeE_cmd_Athena}   ${sg_device_1}

   ${image_activation_log} =  execute_Linux_command    ${fw_active_cmd} ${sg_device_1}
   common_check_patern_2   ${image_activation_log}   ${fw_active_fail_msg_fault_image}   check fault image activation log  expect=True
   common_check_patern_2   ${image_activation_log}   sg_ses_mocrocode failed: Illegal request    check fault image activation log  expect=True

   Server Disconnect

   ConnectESMB
   ${output} =   verifyCLILogAthena
   common_check_patern_2    ${output}   Upgrade cmpl with Errs    Check error message for falut image   expect=True

   get ESM Version And Check
    ...  cmp_dict=${CLI_version}  version_pattern=${esm_fw_version_pattern}
   change_to_ESM_mode
   verify esm mode cli command  DUT
   exit_ESM_mode
   OS Disconnect Device

upgrade cpld with mode 0xe + mode 0xf Athena ESMA
    OS Connect Device
    ${prim_dev} =   get_primary_device
    Set Suite Variable  ${prim_dev}
    ${image_to_upgrade} =   GetCanisterImageName   A0    Athena_FW_CPLD_A
    ${rev_to_check} =  GetRevFromCanisterImage  ${image_to_upgrade}

    execute_Linux_command    ${download_microcode_modeE_cmd_Athena} -I ${image_to_upgrade} -i 4 ${prim_dev}
    command run  sg_ses_microcode -m 0xf  ${prim_dev}
    Sleep  240
    
    reboot_os  DUT
    OS Disconnect Device
    Sleep  300

    OS Connect Device
    verify_CPLD_version   ${rev_to_check}  A
    execute_ESM_command_1   about
    exit_ESM_mode
    OS Disconnect Device

upgrade cpld with mode 0xe + mode 0xf Athena ESMB
    ConnectESMB
    ${prim_dev} =   get_primary_device
    Set Suite Variable  ${prim_dev}
    ${image_to_upgrade} =   GetCanisterImageName   A0    Athena_FW_CPLD_B
    ${rev_to_check} =  GetRevFromCanisterImage  ${image_to_upgrade}

    execute_Linux_command    ${download_microcode_modeE_cmd_Athena} -I ${image_to_upgrade} -i 4 ${prim_dev}
    command run  sg_ses_microcode -m 0xf  ${prim_dev}
    Sleep  420

    OS Disconnect Device
    Sleep  60

    ConnectESMB
    verify_CPLD_version   ${rev_to_check}  A
    execute_ESM_command_1   about
    exit_ESM_mode
    OS Disconnect Device

check Sensor Alarm On Page5 Athena
    [Arguments]    ${alarm_level}  ${sensor_type}
    ${sg_device_1} =   get_primary_device
    Log  ${sg_device_1}
    ${SENSORS}=  list Sensors  ${sensor_type}  ${sg_device_1}
    ${THRESHOLDs}=  get Sensor Threshold  ${SENSORS}[0][0]  ${sg_device_1}  ${sensor_type}
    ${setting_value}=  set Voltage Threshold  ${SENSORS}[0][0]  ${sg_device_1}  ${THRESHOLDs}  ${alarm_level}
    check Sensor Value On Page5  ${SENSORS}[0][0]  ${sg_device_1}  ${alarm_level}
    ...  ${setting_value}  ${sensor_type}
    set Test Variable  ${HDD}  ${sg_device_1}
    set Test Variable  ${SENSOR}  ${SENSORS}[0][0]
    set Test Variable  ${THRESHOLDs}  ${THRESHOLDs}

Verify Enclosure Inventory details on CLI and page command AthenaA
   [Arguments]  ${page_cmd}  ${CLI_cmd}
   ${sg_device_1} =   get_primary_device
   Verify Enclosure Inventory details Athena  ${page_cmd}  ${CLI_cmd}  ${sg_device_1}  DUT
   exit_ESM_mode

Verify Enclosure Inventory details on CLI and page command AthenaB
   [Arguments]  ${page_cmd}  ${CLI_cmd}
   ${sg_device_1} =   get_primary_device
   Verify Enclosure Inventory details Athena  ${page_cmd}  ${CLI_cmd}  ${sg_device_1}  DUT
   exit_ESM_mode

check Command Pattern Athena
    [Arguments]  ${check_cmd}  ${check_pattern}
    ${sg_device_1} =   get_primary_device
    run And Check  ${check_cmd} ${sg_device_1}  ${check_pattern}

verify canister status Athena
   [Arguments]   ${page_cmd}   ${pattern}
   ${sg_device_1} =   get_primary_device
   Check canister status   ${page_cmd}    ${sg_device_1}    ${pattern}

Verify canister B inventory in page command Athena
   [Arguments]  ${cmd}   ${pattern}
   ${sg_device_1} =   get_primary_device
   Check Canister Status  ${cmd}   ${sg_device_1}  ${pattern}
   Disconnect

Verify canister details on CLI and page command Athena
   [Arguments]  ${page_cmd}  ${CLI_cmd}
   ${sg_device_1} =   get_primary_device
   Verify canister details Athena  ${page_cmd}  ${CLI_cmd}  ${sg_device_1}  DUT
   exit_ESM_mode



check fan current speed Athena ESMA
   server Connect
   ${sg_device_1} =   get_primary_device
   Server Disconnect
   verify_ses_page_02_fan_current_speed  %{DUT_username}  %{DUT_ipv4_ip}  %{DUT_password}  ${sg_device_1}  ${fan_speed_1_Athena}
   OS Connect Device
   change_to_ESM_mode
   verify_fan_speed_cli_command     DUT    ${fan_speed_cli_1_Athena}
   verify_esm_fan_mode_cli_command  DUT  external
   exit_ESM_mode
   OS Disconnect Device

   verify_ses_page_02_fan_current_speed  %{DUT_username}  %{DUT_ipv4_ip}  %{DUT_password}  ${sg_device_1}  ${fan_speed_2_Athena}
   OS Connect Device
   change_to_ESM_mode
   verify_fan_speed_cli_command     DUT    ${fan_speed_cli_2_Athena}
   verify_esm_fan_mode_cli_command  DUT  external
   exit_ESM_mode
   OS Disconnect Device

   set_ses_page_02_fan_speed  %{DUT_username}  %{DUT_ipv4_ip}  %{DUT_password}  ${sg_device_1}  8
   get_ses_page_02_fan_speed  %{DUT_username}  %{DUT_ipv4_ip}  %{DUT_password}  ${sg_device_1}  ${fan_speed_2_Athena}

   OS Connect Device
   change_to_ESM_mode
   verify_fan_speed_cli_command     DUT    ${fan_speed_cli_2_Athena}
   verify_esm_fan_mode_cli_command  DUT  external
   exit_ESM_mode
   OS Disconnect Device

check fan current speed Athena ESMB
   server connect ESMB
   ${sg_device_1} =   get_primary_device
   Server Disconnect
   verify_ses_page_02_fan_current_speed  %{DUT_username}  %{DUT_ipv4_ip_ESMB}  %{DUT_password}  ${sg_device_1}  ${fan_speed_1_Athena}
   ConnectESMB
   change_to_ESM_mode
   verify_fan_speed_cli_command     DUT    ${fan_speed_cli_1_Athena}
   verify_esm_fan_mode_cli_command  DUT  external
   exit_ESM_mode
   OS Disconnect Device

   verify_ses_page_02_fan_current_speed  %{DUT_username}  %{DUT_ipv4_ip_ESMB}  %{DUT_password}  ${sg_device_1}  ${fan_speed_2_Athena}
   ConnectESMB
   change_to_ESM_mode
   verify_fan_speed_cli_command     DUT    ${fan_speed_cli_2_Athena}
   verify_esm_fan_mode_cli_command  DUT  external
   exit_ESM_mode
   OS Disconnect Device

   set_ses_page_02_fan_speed  %{DUT_username}  %{DUT_ipv4_ip_ESMB}  %{DUT_password}  ${sg_device_1}  8
   get_ses_page_02_fan_speed  %{DUT_username}  %{DUT_ipv4_ip_ESMB}  %{DUT_password}  ${sg_device_1}  ${fan_speed_2_Athena}

   ConnectESMB
   change_to_ESM_mode
   verify_fan_speed_cli_command     DUT    ${fan_speed_cli_2_Athena}
   verify_esm_fan_mode_cli_command  DUT  external
   exit_ESM_mode
   OS Disconnect Device

check Fan max_min speed Athena ESMA
   [Arguments]   ${fan_speed_min_max}  ${cli_fan_speed}
   server Connect
   ${sg_device_1} =   get_primary_device
   Server Disconnect
   verify_ses_page_02_fan_current_speed  %{DUT_username}  %{DUT_ipv4_ip}  %{DUT_password}  ${sg_device_1}  ${fan_speed_1_Athena}
   OS Connect Device
   change_to_ESM_mode
   verify_fan_speed_cli_command     DUT    ${fan_speed_cli_1_Athena}
   verify_esm_fan_mode_cli_command  DUT  external
   exit_ESM_mode
   OS Disconnect Device

   verify_ses_page_02_fan_current_speed  %{DUT_username}  %{DUT_ipv4_ip}  %{DUT_password}  ${sg_device_1}  ${fan_speed_min_max}
   OS Connect Device
   change_to_ESM_mode
   verify_fan_speed_cli_command     DUT    ${cli_fan_speed}
   verify_esm_fan_mode_cli_command  DUT  external
   exit_ESM_mode
   OS Disconnect Device

   verify_ses_page_02_fan_current_speed  %{DUT_username}  %{DUT_ipv4_ip}  %{DUT_password}  ${sg_device_1}  ${fan_speed_1_Athena}
   OS Connect Device
   change_to_ESM_mode
   verify_fan_speed_cli_command     DUT    ${fan_speed_cli_1_Athena}
   verify_esm_fan_mode_cli_command  DUT  external
   exit_ESM_mode
   OS Disconnect Device

check Fan max_min speed Athena ESMB
   [Arguments]   ${fan_speed_min_max}  ${cli_fan_speed}
   server connect ESMB
   ${sg_device_1} =   get_primary_device
   Server Disconnect
   verify_ses_page_02_fan_current_speed  %{DUT_username}  %{DUT_ipv4_ip_ESMB}  %{DUT_password}  ${sg_device_1}  ${fan_speed_1_Athena}
   ConnectESMB
   change_to_ESM_mode
   verify_fan_speed_cli_command     DUT    ${fan_speed_cli_1_Athena}
   verify_esm_fan_mode_cli_command  DUT  external
   exit_ESM_mode
   OS Disconnect Device

   verify_ses_page_02_fan_current_speed  %{DUT_username}  %{DUT_ipv4_ip_ESMB}  %{DUT_password}  ${sg_device_1}   ${fan_speed_min_max}
   ConnectESMB
   change_to_ESM_mode
   verify_fan_speed_cli_command     DUT   ${cli_fan_speed}
   verify_esm_fan_mode_cli_command  DUT  external
   exit_ESM_mode
   OS Disconnect Device

   verify_ses_page_02_fan_current_speed  %{DUT_username}  %{DUT_ipv4_ip_ESMB}  %{DUT_password}  ${sg_device_1}  ${fan_speed_1_Athena}
   ConnectESMB
   change_to_ESM_mode
   verify_fan_speed_cli_command     DUT    ${fan_speed_cli_1_Athena}
   verify_esm_fan_mode_cli_command  DUT  external
   exit_ESM_mode
   OS Disconnect Device

Check Downloading Status Without Activate Athena ESMA
    OS Connect Device
    ${prim_dev} =   get_primary_device
    Set Suite Variable  ${prim_dev}
    ${image_to_upgrade} =   GetCanisterImageName    A0  Athena_FW_A
    ${PageInfo}=  save Page7 And PageA Info Athena   ${prim_dev}
    verify download status without activate   ${download_microcode_modeE_cmd_Athena}  ${image_to_upgrade}  ${check_modeE_cmd}   ${modeE_downloading_status_Athena}  ${prim_dev}  DUT
    sleep  120 s
    ${prim_dev} =   get_primary_device
    compare Page7 And PageA Info  ${prim_dev}  ${PageInfo}
    ${image_to_upgrade} =   GetCanisterImageName    A1  Athena_FW_A
    ${PageInfo}=  save Page7 And PageA Info Athena   ${prim_dev}
    verify download status without activate   ${download_microcode_modeE_cmd_Athena}  ${image_to_upgrade}  ${check_modeE_cmd}   ${modeE_downloading_status_Athena}  ${prim_dev}  DUT
    sleep  120 s
    ${prim_dev} =   get_primary_device
    compare Page7 And PageA Info  ${prim_dev}  ${PageInfo}
    OS Disconnect Device

Check Downloading Status Without Activate Athena ESMB
    ConnectESMB
    ${prim_dev} =   get_primary_device
    Set Suite Variable  ${prim_dev}
    ${image_to_upgrade} =   GetCanisterImageName    B0  Athena_FW_B
    ${PageInfo}=  save Page7 And PageA Info Athena   ${prim_dev}
    verify download status without activate   ${download_microcode_modeE_cmd_Athena}  ${image_to_upgrade}  ${check_modeE_cmd}   ${modeE_downloading_status_Athena}  ${prim_dev}  DUT
    sleep  120 s
    ${prim_dev} =   get_primary_device
    compare Page7 And PageA Info  ${prim_dev}  ${PageInfo}
    ${image_to_upgrade} =   GetCanisterImageName    B1  Athena_FW_B
    ${PageInfo}=  save Page7 And PageA Info Athena   ${prim_dev}
    verify download status without activate   ${download_microcode_modeE_cmd_Athena}  ${image_to_upgrade}  ${check_modeE_cmd}   ${modeE_downloading_status_Athena}  ${prim_dev}  DUT
    sleep  120 s
    ${prim_dev} =   get_primary_device
    compare Page7 And PageA Info  ${prim_dev}  ${PageInfo}
    OS Disconnect Device

activate New FW Partition Athena ESMA
    OS Connect Device
    ${prim_dev} =   get_primary_device
    Set Suite Variable  ${prim_dev}
    ${image_to_upgrade} =   GetCanisterImageName   A0    Athena_FW_A
    ${rev_to_check} =  GetRevFromCanisterImage  ${image_to_upgrade}
    activate_fw_mode_f_athena   ${fw_active_cmd}    ${prim_dev}    DUT
    OS Disconnect Device
    sleep    300 s
    OS Connect Device
    ${output} =  execute_Linux_command  sg_ses -p 0xe ${prim_dev}
    Log  ${output}
    common_check_patern_2    ${output}  download microcode status: No download microcode operation in progress   verify the completion of FW download    expect=True
    ${page_output} =  execute_Linux_command   sg_ses -p 1 ${prim_dev}
    common_check_patern_2  ${page_output}  ${rev_to_check}  Check Rev Version after Download  expect=True
    OS Disconnect Device

activate New FW Partition Athena ESMB
    ConnectESMB
    ${prim_dev} =   get_primary_device
    Set Suite Variable  ${prim_dev}
    ${image_to_upgrade} =   GetCanisterImageName   A0    Athena_FW_A
    ${rev_to_check} =  GetRevFromCanisterImage  ${image_to_upgrade}
    activate_fw_mode_f_athena   ${fw_active_cmd}    ${prim_dev}    DUT
    OS Disconnect Device
    sleep    300 s
    ConnectESMB
    ${output} =  execute_Linux_command  sg_ses -p 0xe ${prim_dev}
    Log  ${output}
    common_check_patern_2    ${output}  download microcode status: No download microcode operation in progress   verify the completion of FW download    expect=True
    ${page_output} =  execute_Linux_command   sg_ses -p 1 ${prim_dev}
    common_check_patern_2  ${page_output}  ${rev_to_check}  Check Rev Version after Download  expect=True
    OS Disconnect Device

check FW Download Status Athena
    OS Connect Device
    ${prim_dev} =   get_primary_device
    ${output} =  execute_Linux_command  sg_ses -p 0xe ${prim_dev}
    Log  ${output}
    common_check_patern_2    ${output}  download microcode status: No download microcode operation in progress   verify the completion of FW download    expect=True
    OS Disconnect Device
    ConnectESMB
    ${output} =  execute_Linux_command  sg_ses -p 0xe ${prim_dev}
    Log  ${output}
    common_check_patern_2    ${output}  download microcode status: No download microcode operation in progress   verify the completion of FW download    expect=True
    OS Disconnect Device

Download SES FW File And Check Downloading Status Athena ESMA
    OS Connect Device
    downloadAthenaSesFwImage    DUT   Athena_FW_A
    ${prim_dev} =   get_primary_device
    Set Suite Variable  ${prim_dev}
    ${image_to_upgrade} =   GetCanisterImageName    A0  Athena_FW_A
    ${rev_to_check} =  GetRevFromCanisterImage  ${image_to_upgrade}
    execute_Linux_command   sg_ses_microcode -m 0x7 -b 4k -I ${image_to_upgrade} -i 4 ${prim_dev}
    ${output} =  execute_Linux_command  sg_ses -p 0xe ${prim_dev}
    Log  ${output}
    common_check_patern_2    ${output}   No download microcode operation in progress    verify the status of FW download    expect=True
    OS Disconnect Device
    Sleep  450
    OS Connect Device
    ${page_output} =  execute_Linux_command   sg_ses -p 1 ${prim_dev}
    common_check_patern_2  ${page_output}  ${rev_to_check}  Check Rev Version after Download  expect=True
    RemoveAthenaSesFwImage    DUT   Athena_FW_A
    OS Disconnect Device

Download SES FW File And Check Downloading Status Athena ESMB
    ConnectESMB
    downloadAthenaSesFwImage    DUT   Athena_FW_B
    ${prim_dev} =   get_primary_device
    Set Suite Variable  ${prim_dev}
    ${image_to_upgrade} =   GetCanisterImageName    A0  Athena_FW_A
    ${rev_to_check} =  GetRevFromCanisterImage  ${image_to_upgrade}
    execute_Linux_command   sg_ses_microcode -m 0x7 -b 4k -I ${image_to_upgrade} -i 4 ${prim_dev}
    ${output} =  execute_Linux_command  sg_ses -p 0xe ${prim_dev}
    Log  ${output}
    common_check_patern_2    ${output}   No download microcode operation in progress    verify the status of FW download    expect=True
    OS Disconnect Device
    Sleep  450
    ConnectESMB
    ${page_output} =  execute_Linux_command   sg_ses -p 1 ${prim_dev}
    common_check_patern_2  ${page_output}  ${rev_to_check}  Check Rev Version after Download  expect=True
    RemoveAthenaSesFwImage    DUT   Athena_FW_B
    OS Disconnect Device


verify Enclosure LED on off status Athena
   [Arguments]   ${set_on_LED}   ${set_off_LED}  ${pg_cmd}  ${get_page_cmd}  ${enc_LED}  ${LED_on_pattern}  ${LED_off_pattern}
   ${prim_dev} =   get_primary_device
   Set Suite Variable  ${prim_dev}
   command run  ${set_on_LED}  ${prim_dev}
   check enclosure LED status  ${pg_cmd}  ${get_page_cmd}  ${prim_dev}  ${get_LED_1}   ${enc_LED}  ${get_LED_4}  ${get_LED_5}  ${get_ident_LED}  ${LED_on_pattern}
   command run  ${set_off_LED}  ${prim_dev}
   check enclosure LED status  ${pg_cmd}  ${get_page_cmd}  ${prim_dev}  ${get_LED_1}   ${enc_LED}  ${get_LED_4}  ${get_LED_5}  ${get_ident_LED}  ${LED_off_pattern}

verify canister LED on off status Athena
   [Arguments]   ${set_on}  ${clear_canister}  ${check_can0_cmd}  ${check_can1_cmd}  ${ident_fail_cmd}  ${can_on_pattern}  ${can_off_pattern}  ${can_on_pattern_total}
   ${prim_dev} =   get_primary_device
   Set Suite Variable  ${prim_dev}
   command run  ${set_on}  ${prim_dev}
   check canister LED status   ${check_can0_cmd}  ${check_can1_cmd}  ${get_page2_cmd}  ${prim_dev}  ${get_LED_1}  ${get_LED_6}  ${get_LED_7}  ${ident_fail_cmd}   ${get_LED_4}  ${can_on_pattern}  ${can_on_pattern_total}
   command run  ${clear_canister}  ${prim_dev}
   check canister LED status   ${check_can0_cmd}  ${check_can1_cmd}  ${get_page2_cmd}  ${prim_dev}  ${get_LED_1}  ${get_LED_6}  ${get_LED_7}  ${ident_fail_cmd}   ${get_LED_4}  ${can_off_pattern}  ${can_off_pattern}

verify drive disk LED on off status Athena
   [Arguments]   ${set_on_LED}   ${set_off_LED}  ${get_page_cmd}  ${get_LED}  ${LED_on_pattern}  ${LED_off_pattern}
   ${prim_dev} =   get_primary_device
   Set Suite Variable  ${prim_dev}
   command run   ${set_on_LED}   ${prim_dev}
   check LED status    ${get_page_cmd}  ${get_LED_1}  ${get_LED_2}  ${get_LED_3}  ${get_LED}  ${get_LED_4}  ${LED_on_pattern}  ${prim_dev}
   command run   ${set_off_LED}   ${prim_dev}
   check LED status    ${get_page_cmd}  ${get_LED_1}  ${get_LED_2}  ${get_LED_3}  ${get_LED}  ${get_LED_4}  ${LED_off_pattern}  ${prim_dev}


verify cansiter status and FW version Athena
   [Arguments]   ${page_cmd}   ${pattern}
   ${sg_device_1} =   get_primary_device
   change_to_ESM_mode
   ${FW_Version}=  get FW version athena    DUT
   exit_ESM_mode
   check cansiter status and version athena   ${page_cmd}    ${sg_device_1}    ${pattern}   ${FW_Version}

check Temperature Alarm Athena1
    [Arguments]    ${alarm_level}
    ${sg_device_1} =   get_primary_device
    ${SENSORS}=  list Temperature Sensor  ${sg_device_1}
    ${TEMPER_VALUE}=  get Sensor Temperature  ${SENSORS}[0]  ${sg_device_1}
    ${THRESHOLDs}=  getTemperThreshold  ${SENSORS}[0]  ${sg_device_1}
    set Test Variable  ${HDD}  ${sg_device_1}
    set Test Variable  ${SENSOR}  ${SENSORS}[0]
    set Test Variable  ${THRESHOLDs}  ${THRESHOLDs}
    set Temper Threshold  ${SENSORS}[0]  ${sg_device_1}  ${TEMPER_VALUE}  ${alarm_level}
    getTemperThreshold  ${SENSORS}[0]  ${sg_device_1}
    check Alarm Bit  ${SENSORS}[0]  ${sg_device_1}  ${alarm_level}

check PSU status Athena
  [Arguments]  ${cmd}  ${pattern}
  ${sg_device_1} =   get_primary_device
  verify PSU status  ${cmd}  ${sg_device_1}  ${pattern}

CLI check for psu status Athena
  [Arguments]   ${pattern}
  change_to_ESM_mode
  check CLI PSU Status  DUT   ${pattern}
  exit_ESM_mode

Verify element index in pageA
  [Arguments]  ${page_cmd}  ${output}
  ${sg_device_1} =   get_primary_device
  Verify element Index Page 0A  ${sg_device_1}  ${page_cmd}  ${output}

check Driver Status Athena
  [Arguments]   ${cmd}  ${drv_nums}  ${dev1_status}
  ${sg_device_1} =   get_primary_device
  Verify driver status  ${cmd}  ${sg_device_1}   ${drv_nums}  ${dev1_status}

get Control Decscriptor Information Athena
    [Arguments]  ${check_cmd}
    ${sg_device_1} =   get_primary_device
    command Execute  ${sg_device_1}  ${check_cmd}

Verify log pattern Athena
  [Arguments]   ${cmd}  ${code}  ${pattern}
  ${sg_device_1} =   get_primary_device
  verify Log  ${sg_device_1}  ${cmd}  ${code}  ${pattern}

CLI check for log entry Athena
  [Arguments]
  change_to_ESM_mode
  check Log Status Athena  DUT
  exit_ESM_mode

send A Command Athena
   [Arguments]   ${cmd}
   sleep  10 s
   ${sg_device_1} =   get_primary_device
   command run   ${cmd}  ${sg_device_1}

compare new log with CLI Athena
   [Arguments]   ${cmd}
   ${sg_device_1} =   get_primary_device
   check Log Details With CLI Athena   ${cmd}  ${sg_device_1}  DUT

check Disk Power Off Athena
    ${sg_device_1} =   get_primary_device
    ${DEVICEs}=  list Array Devices  ${sg_device_1}
    verify Device Power Off Athena  ${sg_device_1}  ${DEVICEs}[0]

set and verify fan control mode Athena
    change_to_ESM_mode
    set_esm_fan_mode_cli_command  DUT   ${setmode_internal_cmd}
    verify_esm_fan_mode_cli_command  DUT  internal
    set_esm_fan_mode_cli_command  DUT   ${setmode_external_cmd}
    sleep  10 s
    verify_esm_fan_mode_cli_command  DUT  external
    exit_ESM_mode

set and verify pwm value Athena
    change_to_ESM_mode
    run_cli_command  DUT  ${set_pwm_cli_cmd}
    sleep  15s
    verify_fan_speed_cli_command  DUT  ${set_pwm_value}
    exit_ESM_mode

set and verify level Athena
   ${No_of_drives} =  get the number of drives  %{DUT_username}  %{DUT_ipv4_ip}  %{DUT_password}
   change_to_ESM_mode
   run_cli_command  DUT   ${fan_speed_1_cmd}
   sleep  15s
   verify fan speed1  ${No_of_drives}  ${athena_fan_min_speed_cli}  ${fan_min_speed_g75cli}  DUT
   verify_esm_fan_mode_cli_command  DUT  external
   run_cli_command  DUT   ${fan_speed_2_cmd}
   sleep  15s
   verify fan speed1  ${No_of_drives}  ${athena_fan_speed_10_l75cli}  ${fan_speed_10_g75cli}  DUT
   verify_esm_fan_mode_cli_command  DUT  external
   run_cli_command  DUT   ${fan_speed_3_cmd}
   sleep  15s
   verify fan speed1  ${No_of_drives}  ${athena_fan_speed_11_l75cli}  ${fan_speed_11_g75cli}  DUT
   verify_esm_fan_mode_cli_command  DUT  external
   run_cli_command  DUT   ${fan_speed_4_cmd}
   sleep  15s
   verify fan speed1  ${No_of_drives}  ${athena_fan_speed_12_l75cli}  ${fan_speed_12_g75cli}  DUT
   verify_esm_fan_mode_cli_command  DUT  external
   run_cli_command  DUT   ${fan_speed_5_cmd}
   sleep  15s
   verify fan speed1  ${No_of_drives}  ${athena_fan_speed_13_l75cli}  ${fan_speed_13_g75cli}  DUT
   verify_esm_fan_mode_cli_command  DUT  external
   run_cli_command  DUT   ${fan_speed_6_cmd}
   sleep  15s
   verify fan speed1  ${No_of_drives}  ${athena_fan_speed_14_l75cli}  ${fan_speed_14_g75cli}  DUT
   verify_esm_fan_mode_cli_command  DUT  external
   run_cli_command  DUT   ${fan_speed_7_cmd}
   sleep  15s
   verify fan speed1  ${No_of_drives}  ${athena_fan_max_speed_l75cli}  ${fan_max_speed_g75cli}  DUT
   verify_esm_fan_mode_cli_command  DUT  external
   exit_ESM_mode

verify VPD information Athena
   [Arguments]
   ${sg_device_1} =   get_primary_device
   change_to_ESM_mode
   ${fru_get_output}=   run_ESM_command    ${canister_CLI_cmd}
   exit_ESM_mode
   verify mid plane VPD information   ${athena_read_mid_plane_VPD_cmd}  ${get_VPD_cmd}  ${sg_device_1}  ${fru_get_output}
   verify canister VPD information Athena   ${athena_read_canister_VPD_cmd}  ${get_VPD_cmd}   ${sg_device_1}  ${fru_get_output}
   verify PSU VPD information Athena   ${athena_read_PSU_VPD_cmd}  ${get_VPD_cmd}  ${sg_device_1}  ${fru_get_output}
   verify all VPD information Athena   ${athena_read_all_VPD_cmd}  ${get_VPD_cmd}   ${sg_device_1}  ${fru_get_output}

check String In Diagnostic Pages Athena (04h)
#    ${sg_device_1} =  get_devicename  %{DUT_username}  %{DUT_ipv4_ip}  %{DUT_password}
    ${sg_device_1} =   get_primary_device
    change_to_ESM_mode
    ${expect_ESMA_IP} =  get_ipconfig_cli  DUT  ip
    ${expect_gateway} =  get_ipconfig_cli  DUT  gateway
    ${expect_ESM_A_DHCP_Mode} =  get_ipconfig_cli  DUT  dhcp
    ${expect_ESMA_up_time} =  get_esm_up_time  DUT
    exit_ESM_mode
    verify_ses_page_04  %{DUT_username}  %{DUT_ipv4_ip}  %{DUT_password}  ${sg_device_1}  ${expect_ESMA_IP}  ${expect_gateway}
          ...  ${expect_ESM_A_DHCP_Mode}  ${expect_ESMA_up_time}

get FRU Info Athena
    change_to_ESM_mode
    ${FRU_INFO}=  run ESM command  fru get
    exit_ESM_mode
    set Test Variable  ${FRU_INFO}  ${FRU_INFO}

check Descriptor Length Athena
    ${sg_device_1} =   get_primary_device
    verify Descriptor Length  ${sg_device_1}  ${FRU_INFO}

check String In Diagnostic Pages Athena(05h)
    server Connect
    ${sg_device_1} =   get_primary_device
    Server Disconnect
    Step  1  OS Connect Device
    Step  2  verify_ses_page_05  %{DUT_username}  %{DUT_ipv4_ip}  %{DUT_password}  ${sg_device_1}
    Step  3  OS Disconnect Device

check String In Diagnostic Pages Athena ESMB(05h)
    server connect ESMB
    ${sg_device_1} =   get_primary_device
    Server Disconnect
    Step  1  ConnectESMB
    Step  2  verify_ses_page_05  %{DUT_username}  %{DUT_ipv4_ip_ESMB}  %{DUT_password}  ${sg_device_1}
    Step  3  OS Disconnect Device


