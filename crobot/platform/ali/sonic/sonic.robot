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
Documentation       This Suite will validate Sonic package

Library           AliSonicLib.py
Library           AliCommonLib.py
Library           CommonLib.py
Variables         AliCommonVariable.py
Variables         AliSonicVariable.py

Resource          AliSonicKeywords.resource

Suite Setup       Connect Device
Suite Teardown    Disconnect Device

*** Variables ***
${LoopCnt}      1
${MAX_LOOP}     3

*** Test Cases ***


ALI_SONIC_TC_001_BSP_sysfs_interfaces_check
    [Documentation]  This test checks BSP sysfs interfaces check
    [Tags]    ALI_SONIC_TC_001_BSP_sysfs_interfaces_check
    [Timeout]  10 min 00 seconds
    Step  1  Run Keywords  execute command  cd /sys/
    ...  AND  check driver tree  ${sys_interfaces}
    Step  2  Run Keywords  execute command  cd /sys/bus/i2c/devices/
    ...  AND  check driver tree  ${sys_i2c_devices_interfaces}
    ...  AND  execute command  cd 0-0056/
    ...  AND  check driver tree  eeprom
    Step  3  Run Keywords  execute command  cd /sys/devices/platform/
    ...  AND  check driver tree  ${sys_devices_platform}
    Step  4  Run Keywords  execute command  cd /sys/devices/platform/AS*.switchboard/
    ...  AND  check driver tree  ${sys_switchboard_interfaces}
    ...  AND  execute command  cd SFF
    ...  AND  check driver tree  ${sys_switch_SFF_interfaces}
    FOR  ${qsfp}  IN  @{QSFP_num_list}
        Step  5  Run Keywords  check driver tree  ${sys_switch_SFF_QSFP_interfaces}  ls ${qsfp}
        ...  AND  check driver tree  ${sys_switch_SFF_QSFP_i2c_interfaces}  ls ${qsfp}/i2c
    END
    Step  6  execute command  cd /etc/sonic/
    Step  7  check poap file  ${poap_file}
    Step  8  check monitor status


ALI_SONIC_TC_002_Baseboard_CPLD_register_access
    [Documentation]  This test checks Baseboard CPLD register access
    [Tags]     ALI_SONIC_TC_002_Baseboard_CPLD_register_access
    [Timeout]  15 min 00 seconds
    Step  1  execute command  cd /sys/devices/platform/AS*.cpldb/
    Step  2  check driver tree  ${sys_BaseCPLD_interfaces}
    Step  3  read cpld version  ${cat_version_cmd}  BASE_CPLD
    Step  4  write cpld register


ALI_SONIC_TC_003_System_Led_Test
    [Documentation]  This test checks System Led Test
    [Tags]     ALI_SONIC_TC_003_System_Led_Test
    [Timeout]  15 min 00 seconds
    Step  1  execute command  cd /sys/devices/platform/AS*.cpldb/
    Step  2  change_sys_led_command


ALI_SONIC_TC_004_FPGA_register_access
    [Documentation]  This test checks FPGA register access
    [Tags]     ALI_SONIC_TC_004_FPGA_register_access
    [Timeout]  15 min 00 seconds
    Step  1  execute command  cd /sys/devices/platform/AS*.switchboard/FPGA/
    Step  2  check driver tree  ${sysfs_interfaces}
    Step  3  read fpga version
    Step  4  write fpga register


ALI_SONIC_TC_005_Switch_board_CPLD_register_access
    [Documentation]  This test checks Switch_board_CPLD_register_access
    [Tags]    ALI_SONIC_TC_005_Switch_board_CPLD_register_access
    [Timeout]  10 min 00 seconds
    FOR  ${sw_cpld}  IN  @{port_cpld}
        Step  1  Run Keywords  execute command and verify exit code
        ...  console=${diagos_mode}  command=cd /sys/devices/platform/AS*.switchboard/${sw_cpld}
        ...  AND  check driver tree  ${sysfs_interfaces}
        ...  AND  read cpld version  ${cat_getreg_cmd}  ${SWITCH_CPLD}
        ...  AND  write cpld register
    END


ALI_SONIC_TC_007_SONiC_Login_Check_Test
    [Documentation]  This test checks SONiC Login Test
    [Tags]    ALI_SONIC_TC_007_SONiC_Login_Check_Test
    [Timeout]  10 min 00 seconds
    Step  1  diagos login check


ALI_SONIC_TC_008_SONiC_Version_Check
    [Documentation]  This test checks SONiC version
    [Tags]    ALI_SONIC_TC_008_SONiC_Version_Check
    [Timeout]  10 min 00 seconds
    Step  1  check sonic version  ${show_version_cmd}  ${BOOT_MODE_DIAGOS}


ALI_SONIC_TC_011_SONiC_Booting_info_Check
    [Documentation]  This test checks SONiC booting info
    [Tags]    ALI_SONIC_TC_011_SONiC_Booting_info_Check
    [Timeout]  6 min 00 seconds
    Step  1  sonic_booting_info_check  ${platform}


ALI_SONIC_TC_012_Dependent_Software_Version_Check
    [Documentation]  This test check dependent software version
    [Tags]    ALI_SONIC_TC_012_Dependent_Software_Version_Check
    [Timeout]  10 min 00 seconds
    Step  1  execute command  cd /usr/share/sonic/device/${platform_name}/plugins
    Step  2  check software version  ${platform}


ALI_SONIC_TC_013_Hardware_Interface_Access_Scan_Check
    [Documentation]  This test check cpu and memory info
    [Tags]    ALI_SONIC_TC_013_Hardware_Interface_Access_Scan_Check
    [Timeout]  10 min 00 seconds
    Step  1  check cpu and memory info

ALI_SONIC_TC_014_TLV_EEPROM_Info_Read
    [Documentation]  This test check cpu tlv eeprom info
    [Tags]    ALI_SONIC_TC_014_TLV_EEPROM_Info_Read
    [Timeout]  10 min 00 seconds
    Step  1  check tlv eeprom info  ${platform}

ALI_SONIC_TC_016_Sensor_Info_Check
    [Documentation]  This test check sensor info
    [Tags]    ALI_SONIC_TC_016_Sensor_Info_Check
    [Timeout]  10 min 00 seconds
    Step  1  sonic_sensors_info_check  ${platform}

ALI_SONIC_TC_022_Loopback_module_temperature_read
    [Documentation]  This test check loopback module temperature
    [Tags]    ALI_SONIC_TC_022_Loopback_module_temperature_read
    [Timeout]  10 min 00 seconds
    Step  1  check loopback temperature

ALI_SONIC_TC_023_CPLD1_and_CPLD2_R/W_Test
    [Documentation]  This test test CPLD1 and CPLD2 read and write
    [Tags]    ALI_SONIC_TC_023_CPLD1_and_CPLD2_R/W_Test  shamu_specific
    [Timeout]  10 min 00 seconds
    Step  1  execute command  cd /sys/devices/platform/AS*.switchboard/CPLD1/
    Step  2  test CPLD read write
    Step  3  execute command  cd /sys/devices/platform/AS*.switchboard/CPLD2/
    Step  4  test CPLD read write

*** Keywords ***
Connect Device
    Login Device

Disconnect Device
    Sonic Disconnect
