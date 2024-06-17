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
#######################################################################################################################

*** Settings ***
Variables         ONL_variable.py

Library           whitebox_lib.py
#Library           openbmc_lib.py
#Library           common_lib.py
Library           bios_menu_lib.py
Library           CommonLib.py
Library           OperatingSystem
#Library           ../WhiteboxLibAdapter.py
#Library           ../ses/ses_lib.py
#Library           ../bmc/bmc_lib.py
Library           ONL_lib.py

Resource          ONL_keywords.robot
Resource          CommonResource.robot
#Resource          BMC_keywords.robot

*** Keywords ***
Enter bios now
    enter_into_bios_setup_now  DUT  


Enter bios as user
    enter_into_bios_setup  DUT  ${user_pass}


leave bios
    exit bios menu  DUT

boot sonic via bios
    check sonic boot via bios  DUT

check the microcode
    check_cpu_microcode  DUT


access bios via shell
    enter bios with shell

Verify BIOS Version
    ${act_bios_version}  get_bios_version  DUT
    check_info_equal  ${act_bios_version}  ${exp_bios_version}

Verify ONIE Version
    ${act_onie_version}  get_onie_version  DUT
    check_info_equal  ${act_onie_version}  ${exp_onie_version}

Verify BMC Version
   #${bmc_ip}  get_bmc_ip_address_from_ipmitool  DUT
    ${act_bmc_version}  get_bmc_version_ipmitool  DUT 
    check_info_equal  ${act_bmc_version}  ${exp_bmc_version}

Verify FPGA Version
    ${act_fpga_version}  get_fpga_version  DUT
    check_info_equal  ${act_fpga_version}  ${exp_fpga_version}

Verify Baseboard CPLD Version
    ${act_bb_cpld_version}  get_baseboard_cpld_version  DUT
    check_info_equal  ${act_bb_cpld_version}  ${exp_bb_cpld_version}

Verify Switch CPLD Version
    ${act_switch_cpld_version}  get_switch_cpld_version  DUT
    check_info_equal  ${act_switch_cpld_version}  ${exp_switch_cpld_version}

Verify COME CPLD Version
    ${act_come_cpld_version}  get_come_cpld_version  DUT
    check_info_equal  ${act_come_cpld_version}  ${exp_come_cpld_version}

Verify ONL booting check
    verify_onl_booting_check_log  DUT

Verify ONL Login check
    verify_onl_login  DUT 

Verify ONL Version
    ${act_onl_version}  get_onl_version  DUT
    check_info_equal  ${act_onl_version}  ${exp_onl_version}

Verify ONL system info check
    ${act_onl_sysinfo}  get_onl_sysinfo  DUT
    check_info_equal  ${act_onl_sysinfo}  ${exp_onl_sysinfo}

Verify system info test
    ${act_sysinfo}  get_system_info_detail  DUT 
    burningTlvData_SV2  DUT  ${tlv_onie}
    ${act_sysinfo}  get_system_info_detail  DUT
    check_info_equal  ${act_sysinfo['ONIE_Version']}  ${onie_version}

Install ONL from ONL and Check
    ONL_Install_UnInstall_Mode  DUT  ${ONIE_INSTALL_MODE}
    Install_ONL_OS_from_ONIE  DUT  ${version}  ${PROTOCOL_TFTP}  ${install_wait_time}
    Verify ONL Version

Uninstall ONL then Install ONL and Check
    ONL_Install_UnInstall_Mode  DUT  ${ONIE_UNINSTALL_MODE}
    Install_ONL_OS_from_ONIE  DUT  ${version}  ${PROTOCOL_TFTP}
    Verify ONL Version

Verify PSU Status
    test_CheckPSUStatus  DUT  ${PlatformEnv}
    test_CheckPSUVoltage  DUT  ${PlatformEnv}
    test_CheckPSUTypeTest  DUT  ${PlatformEnv}  

Verify PSU State
    test_CheckPSUState  DUT  ${PlatformEnv}

Verify FAN Test
    test_FanNoAndDescTest  DUT  ${PlatformEnv}
    test_FanRPMAndSpeedTest  DUT  ${PlatformEnv}

Verify FAN State
    test_FanStateTest  DUT  ${PlatformEnv}
   
Verify Thermal Sensor Test
    test_CheckSensorDescription  DUT  ${PlatformEnv}
    test_SensorTemperatureTest  DUT  ${PlatformEnv}
    test_SensorThresholdTest  DUT  ${PlatformEnv}

Verify Thermal Sensor State
    test_SensorStatusTest  DUT  ${PlatformEnv}

Verify Device data test
    ${parsed_data}=  dump_device_data  DUT
    compare_device_data  ${exp_device_info}  ${parsed_data}

Verify data in json format
    verify_data_json_format  DUT   

Verify System LED
    test_CheckSystemLED  DUT  ${PlatformEnv}
    
Verify Alarm LED
    test_CheckAlertLED  DUT  ${PlatformEnv}

Verify PSU LED
    test_CheckPSULED  DUT  ${PlatformEnv}

Verify Optics present status
    test_Check_Optics_Presence  DUT  ${portlist}

Verify ONL Stress test
    test_stress_onl  DUT  ${reboot_count}

Verify Device OID test
    ${act_sys_OID}  get_device_OID  DUT
    check_info_equal  ${act_sys_OID}  ${exp_sys_OID}
   
Verify Device SNMP test
    test_device_ONL_SNMP  DUT  ${device_OID}
    
Verify device reset test
    test_device_reset  DUT  ${exp_device_info}

Verify TLV EEPROM info
    ${parsed_data}=  exec_ipmitool_fru_print  DUT
    compare_device_data  ${exp_ipmi_info}  ${parsed_data}
 
AC power device
    Step  1  EDK2CommonLib.Powercycle Device   DUT   no


chuck it
    Step  1  exit bios shelll  DUT
    Step  2  exit the shell


Power me up
    Step  1   EDK2CommonLib.Powercycle Device   DUT   yes

exit the shell
    EDK2CommonLib.exit the shell
