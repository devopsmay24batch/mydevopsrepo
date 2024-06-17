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
    check_info_equal  ${act_onie_version}  ${onie_version}

Verify BMC Version
    ${act_bmc_version}  get_bmc_version_ipmitool  DUT 
    check_info_equal  ${act_bmc_version}  ${exp_bmc_version}

Verify FPGA Version
    ${act_fpga_version}  get_fpga_version  DUT
    check_info_equal  ${act_fpga_version}  ${exp_fpga_version}
    check_set_fpga_scratch  DUT  ${write_fpga_scratch1}
    check_set_fpga_scratch  DUT  ${write_fpga_scratch2}
    check_setreg_fpga  DUT  ${test_register}  ${test_register_value}
    check_default_fpga_scratch_getreg  DUT

Verify COME CPLD Version
    ${act_come_cpld_version}  get_come_cpld_version  DUT
    check_info_equal  ${act_come_cpld_version}  ${exp_come_cpld_version}

Verify ONL booting check
    verify_onl_booting_check_log  DUT

Verify ONL Login check
    verify_onl_login  DUT 

Verify Switch CPLD Version
    check_default_switch_cpld_version  DUT
    check_switch_cpld_read_write_operation  DUT
    check_default_switch_cpld_version  DUT

Verify system info test
    check_system_platform_information  DUT  ${exp_mac_addr}  ${exp_diag_version}
    update_onie_eeprom_information  DUT  ${exp_mac_addr}  ${old_diag_version}
    check_system_platform_information  DUT  ${exp_mac_addr}  ${old_diag_version}
    update_onie_eeprom_information  DUT  ${exp_mac_addr}  ${exp_diag_version}
    check_system_platform_information  DUT  ${exp_mac_addr}  ${exp_diag_version}

Install ONL from ONL and Check
    verify_onl_version  DUT
    ONL_Install_UnInstall_Mode  DUT  ${ONIE_INSTALL_MODE}
    Install_ONL_OS_from_ONIE  DUT  ${version}  ${PROTOCOL_TFTP}
    verify_onl_version  DUT
    
Uninstall ONL then Install ONL and Check
    verify_onl_version  DUT
    ONL_Install_UnInstall_Mode  DUT  ${ONIE_UNINSTALL_MODE}
    Install_ONL_OS_from_ONIE  DUT  ${version}  ${PROTOCOL_TFTP}
    verify_onl_version  DUT
    
Verify PSU Status
    test_CheckPSUStatus  DUT  ${PlatformEnv}
    test_CheckPSUVoltage  DUT  ${PlatformEnv}
    test_CheckPSUTypeTest  DUT  ${PlatformEnv}  

Verify PSU Test
    test_CheckPSUInformation  DUT  

Verify FAN Test
    test_FanNoAndDescAndAirflowTest  DUT  ${PlatformEnv}
    test_FanStateAndStatusTest  DUT  ${PlatformEnv}
    test_FanRPMAndSpeedTest  DUT  
    
Verify FAN State
    test_FanStateTest  DUT  ${PlatformEnv}
   
Verify Thermal Sensor Test
    verify_onl_bmc_thermal_temp  DUT
    verify_thermal_information  DUT

Verify data in json format
    verify_data_json_format  DUT   

Verify System LED
    test_CheckSystemLED  DUT  ${PlatformEnv}
    
Verify Alarm LED
    test_CheckAlertLED  DUT  ${PlatformEnv}

Verify PSU LED
    test_CheckPSULED  DUT  ${PlatformEnv}

Verify Optics present status
    test_Check_Optics_Presence  DUT  ${port}

Verify ONL Stress test
    test_stress_onl  DUT  ${iterations}

Verify Device SNMP test
    test_device_ONL_SNMP  DUT  ${device_OID}
    
Verify device reset test
    powerCycle  DUT
    reset_test_commands  DUT
    reboot_device  DUT
    reset_test_commands  DUT  baseboard_value_1=${baseboard_scratch_write_1}  baseboard_value_2=${baseboard_scratch_write_2}  switch_value_1=0x21  switch_value_2=0x13  fgpa_value_1=${write_fpga_scratch1}  fgpa_value_2=${write_fpga_scratch2}
    device_poweroff  DUT
    reset_test_commands  DUT

Verify platform management daemon function driver
    check_platform_daemon  DUT
    check_platform_function  DUT
    check_platform_driver  DUT

Verify SFP SYSFS
    check_SFP_present_status  DUT
    check_loss_of_signal_assertion_status  DUT
    check_module_transmission_status  DUT
    check_transmission_fault_assert_signal  DUT

Verify OSFP SYSFS
    check_OSFP_present_status  DUT
    check_Low_power_mode  DUT
    check_reset_signal_logic_level  DUT
    check_Indicating_the_module_Interrupt_status  DUT

Verify TLV EEPROM info
    check_onie_eeprom_info  DUT
    verify_device_data  DUT
    exec_ipmitool_fru_print  DUT
    #compare_device_data  ${exp_ipmi_info}  ${parsed_data}
 
Verify SYSFS Interface
    check_I2C_device_sysfs  DUT
    check_platform_device_sysfs  DUT
    check_SFPs_and_OSFPs_EEPROM_sysfs  DUT
