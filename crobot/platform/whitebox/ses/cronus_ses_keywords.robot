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
Variables         cronus_ses_variable.py
Library           whitebox_lib.py
Library           ses_lib.py
Library           cronus_ses_lib.py
Library           OperatingSystem
Library           openbmc_lib.py
Library           ../bmc/bmc_lib.py
Resource          cronus_ses_keywords.robot
Resource          CommonResource.robot

*** Keywords ***

Configuration Diagnostic Pages(01h) Cronus
    ${sg_device_1} =  get_devicename  %{DUT_username}  %{DUT_ipv4_ip}  %{DUT_password}  Zone1
    ${sg_device_2} =  get_devicename  %{DUT_username}  %{DUT_ipv4_ip}  %{DUT_password}  Zone2
    ${ses_fw_version} =  get_ses_fw_version_by_ses_page_01h  %{DUT_username}  %{DUT_ipv4_ip}  %{DUT_password}  ${sg_device_1}
    Step  1  verify_ses_page_01h_info  %{DUT_username}  %{DUT_ipv4_ip}  %{DUT_password}  ${sg_device_1}  ${cronus_ses_page_01h_info}
    Step  2  verify_ses_page_01h_info  %{DUT_username}  %{DUT_ipv4_ip}  %{DUT_password}  ${sg_device_2}  ${cronus_ses_page_01h_info}

get FRU Info Cronus
    ESMAConnect  ${ESMA IP}  ${ESMA port}
    ${FRU_INFO}=  run ESM command  fru get
    exit_ESM_mode
    set Test Variable  ${FRU_INFO}  ${FRU_INFO}

CLI check for log entry Cronus
  [Arguments]
  ESMAConnect  ${ESMA_IP_1}  ${ESMA_port_1}
  check Log Status Cronus  DUT
  Disconnect

Verify element index flag as invalid Cronus
    [Arguments]  ${cmd}  ${dv1_index}  ${dv2_index}
    ${HDDs}=  query SG Devices
    verify Flag As Invalid  ${cmd}  ${dv1_index}   ${HDDs}[0]
   #verify Flag As Invalid  ${cmd}  ${dv2_index}  ${HDDs}[1]

verify page with expander log Cronus
   [Arguments]    ${pri_cmd}  ${page_cmd}
    ${HDDs}=  query SG Devices
    ESMAConnect  ${ESMA_IP_1}  ${ESMA_port_1}
    check page with expander log  ${pri_cmd}  ${page_cmd}  ${HDDs}[0]  DUT

check ESC Ident LED
    ${HDDs}=  query SG Devices
    setESCIDENTBit  ${HDDs}[0]

check disk Ident LED
    ${HDDs}=  query SG Devices
    setdiskIDENTBit  ${HDDs}[0]

check disk Fault LED
    ${HDDs}=  query SG Devices
    setdiskFaultBit  ${HDDs}[0]

check disk Rebuild/remap LED
    ${HDDs}=  query SG Devices
    setdiskremapledBit  ${HDDs}[0]

check ESC Fault Bit LED
    ${HDDs}=  query SG Devices
    setESCFaultBit  ${HDDs}[0]

check ENC Ident LED
    ${HDDs}=  query SG Devices
    setencIdentBit  ${HDDs}[0]

check ENC Fault LED
    ${HDDs}=  query SG Devices
    setencFaultBit  ${HDDs}[0]

check ENC Warning LED
    ${HDDs}=  query SG Devices
    setencWarningBit  ${HDDs}[0]

verify smp phy enable disable Cronus WB
  [Arguments]
  ${Expanders}=  Query Expanders  ${cronus_smp_exp_index}
  check SMP Phy Enable Disable   ${Expanders}[0]

verify smp phy link speed Cronus WB
  [Arguments]
  ${Expanders}=  Query Expanders  ${cronus_smp_exp_index}
  check SMP Phy link speed   ${Expanders}[0]  10

Setting partial pathway timeout value Cronus WB
  [Arguments]
  ${Expanders}=  Query Expanders  ${cronus_smp_exp_index}
  Set Partial Pathway Timeout   ${Expanders}[0]

Setting SMP Phy partial and slumber enable and disable for SAS and SATA Cronus WB
  [Arguments]
  ${Expanders}=  Query Expanders  ${cronus_smp_exp_index}
  Set SMP Phy partial and slumber   ${Expanders}[0]

check Info bit Cronus
    ${sg_device_1} =  get_devicename  %{DUT_username}  %{DUT_ipv4_ip}  %{DUT_password}  Zone1
	Step  0  ssh_command_set_ses_page_command  %{DUT_username}  %{DUT_ipv4_ip}  %{DUT_password}
          ...  sg_ses --page=0x02 --index=_24,0 --set=1:1:1=0 --byte1=0x00 ${sg_device_1}
    Step  1  set time delay  5
    Step  2  ssh_command_set_ses_page_command  %{DUT_username}  %{DUT_ipv4_ip}  %{DUT_password}
          ...  sg_ses -p 2 -I enc,0 --set=3:1:1=1 ${sg_device_1}
    Step  3  set time delay  10
    Step  4  ssh_command_set_ses_page_command  %{DUT_username}  %{DUT_ipv4_ip}  %{DUT_password}
          ...  sg_ses -p 2 -I enc,0 --set=3:1:1=0 ${sg_device_1}
    Step  5  set time delay  10
    Step  6  verify_ses_page_02h_info_bit  %{DUT_username}  %{DUT_ipv4_ip}  %{DUT_password}  ${sg_device_1}  ${info_bit_enable}
    Step  7  ssh_command_set_ses_page_command  %{DUT_username}  %{DUT_ipv4_ip}  %{DUT_password}
          ...  sg_ses --page=0x02 --index=_24,0 --set=1:1:1=0 --byte1=0x00 ${sg_device_1}
    Step  8  set time delay  5
    Step  9  verify_ses_page_02h_info_bit  %{DUT_username}  %{DUT_ipv4_ip}  %{DUT_password}  ${sg_device_1}  ${info_bit_off} 

Verify element index flag as valid Cronus
   [Arguments]  ${cmd}  ${dv1_index}  ${dv2_index}
   ${HDDs}=  query SG Devices
   Cronus verify Flag As Valid  ${cmd}  ${dv1_index}   ${HDDs}[0]
   Cronus verify Flag As Valid  ${cmd}  ${dv2_index}  ${HDDs}[1]

check Temperature Alarm On Page5 Cronus
    [Arguments]    ${alarm_level}
    ${HDDs}=  query SG Devices
    #${SENSORS}=  list Temperature Sensor  ${HDDs}[0]
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

check Temperature Alarm Cronus
    [Arguments]    ${alarm_level}
    ${HDDs}=  query SG Devices
    Log  ${HDDs}
    ${TEMPER_VALUE}=  get Sensor Temperature  ${SENSORS}[0]  ${HDDs}[0]
    ${THRESHOLDs}=  getTemperThreshold  ${SENSORS}[0]  ${HDDs}[0]
    set Test Variable  ${HDD}  ${HDDs}[0]
    set Test Variable  ${SENSOR}  ${SENSORS}[0]
    set Test Variable  ${THRESHOLDs}  ${THRESHOLDs}
    set Temper Threshold  ${SENSORS}[0]  ${HDDs}[0]  ${TEMPER_VALUE}  ${alarm_level}
    Log  ${HDD}
    getTemperThreshold  ${SENSORS}[0]  ${HDDs}[0]
    check Alarm Bit  ${SENSORS}[0]  ${HDDs}[0]  ${alarm_level}

check Sensor Alarm On Page5 Cronus
    [Arguments]    ${alarm_level}  ${sensor_type}
    ${HDDs}=  query SG Devices
    ${THRESHOLDs}=  get Sensor Threshold  ${voltage_SENSORS}[0][0]  ${HDDs}[0]  ${sensor_type}
    ${setting_value}=  set Voltage Threshold  ${voltage_SENSORS}[0][0]  ${HDDs}[0]  ${THRESHOLDs}  ${alarm_level}
    check Sensor Value On Page5  ${voltage_SENSORS}[0][0]  ${HDDs}[0]  ${alarm_level}
    ...  ${setting_value}  ${sensor_type}
    set Test Variable  ${HDD}  ${HDDs}[0]
    set Test Variable  ${SENSOR}  ${voltage_SENSORS}[0][0]
    set Test Variable  ${THRESHOLDs}  ${THRESHOLDs}

check Default Sensor Alarm On Page5 Cronus
    [Arguments]    ${alarm_level}  ${sensor_type}
    ${HDDs}=  query SG Devices
    ${THRESHOLDs}=  get Sensor Threshold  ${voltage_SENSORS}[0][0]  ${HDDs}[0]  ${sensor_type}
	set Test Variable  ${HDD}  ${HDDs}[0]
    set Test Variable  ${SENSOR}  ${voltage_SENSORS}[0][0]
    set Test Variable  ${THRESHOLDs}  ${THRESHOLDs}

restore Threshold on Page5 Cronus
    [Arguments]    ${alarm_level}  ${sensor_type}
    ${setting_value}=  set Back Threshold  ${SENSOR}  ${HDD}  ${THRESHOLDs}
    ...  ${alarm_level}  ${sensor_type}
    check Sensor Value On Page5  ${SENSOR}  ${HDD}  ${alarm_level}
    ...  ${setting_value}  ${sensor_type}

check Default Sensor Alarm On Page5 for V11 sensor Cronus
    [Arguments]    ${alarm_level}  ${sensor_type}
    ${HDDs}=  query SG Devices
    ${THRESHOLDs}=  get Sensor Threshold  ${voltage_SENSORS}[11][0]  ${HDDs}[0]  ${sensor_type}
    set Test Variable  ${HDD}  ${HDDs}[0]
    set Test Variable  ${SENSOR}  ${voltage_SENSORS}[11][0]
    set Test Variable  ${THRESHOLDs}  ${THRESHOLDs}

check Default Sensor Alarm On Page5 for V6 sensor Cronus
    [Arguments]    ${alarm_level}  ${sensor_type}
    ${HDDs}=  query SG Devices
    ${THRESHOLDs}=  get Sensor Threshold  ${voltage_SENSORS}[6][0]  ${HDDs}[0]  ${sensor_type}
    set Test Variable  ${HDD}  ${HDDs}[0]
    set Test Variable  ${SENSOR}  ${voltage_SENSORS}[6][0]
    set Test Variable  ${THRESHOLDs}  ${THRESHOLDs}

Threshold Control Page Cronus (Voltage UC)
    ${sg_device_1} =  get_primary_device
    ${HDDs} =  query SG Devices
    Step  1  set_voltage_sensor_high_crit  ${HDDs}[0]
    Step  2  get_voltage_sensor_threshold  ${HDDs}[0]

Threshold Control Page Cronus (Voltage LC)
    ${sg_device_1} =  get_primary_device
    ${HDDs} =  query SG Devices
    Step  1  set_voltage_sensor_low_crit  ${HDDs}[0]
    Step  2  get_voltage_sensor_threshold_status  ${HDDs}[0]

check allsasadd
    ${sg_device_1} =  get_primary_device
    ${sg_device_2} =   get_non_primary_device
    ${HDDs} =  query SG Devices
    Step  1  get_sasadd3  ${HDDs}[0]
    Step  2  get_sasadd3  ${HDDs}[1]

compare PSU status with CLI Cronus
   [Arguments]   ${psu_pattern}  ${cmd}  ${PSU_NO}
   ${HDDs}=  query SG Devices
   check PSU Details With CLI Cronus  ${psu_pattern}  ${cmd}  ${PSU_NO}  ${HDDs}[0]  DUT
   Disconnect

check Driver Status Cronus 
  [Arguments]   ${cmd}  ${drv_nums}  ${dev1_status}  
  ${HDDs}=  query SG Devices
  Verify driver status  ${cmd}  ${HDDs}[0]   ${drv_nums}  ${dev1_status}

Verify Enclosure Inventory details on CLI and page command cronus
   [Arguments]  ${page_cmd}  ${CLI_cmd}
   ${HDDs}=  query SG Devices
   Verify Enclosure Inventory details cronus  ${page_cmd}  ${CLI_cmd}  ${HDDs}[0]  DUT
   Disconnect

Threshold Control Page Cronus (Voltage LW)
    ${sg_device_1} =  get_primary_device
    ${HDDs} =  query SG Devices
    Step  1  set_voltage_sensor_low_warning  ${HDDs}[0]
    Step  2  get_voltage_sensor_threshold_low_warning  ${HDDs}[0]

Threshold Control Page Cronus (Voltage OW)
    ${sg_device_1} =  get_primary_device
    ${HDDs} =  query SG Devices
    Step  1  set_voltage_sensor_high_warning  ${HDDs}[0]
    Step  2  get_voltage_sensor_threshold_high_warning  ${HDDs}[0]

check Altitude configuration Cronus
    ${sg_device_1} =  get_devicename  %{DUT_username}  %{DUT_ipv4_ip}  %{DUT_password}  Zone1
    Step  1  set_verify_altitude_config  %{DUT_username}  %{DUT_ipv4_ip}  %{DUT_password}  ${sg_device_1}
