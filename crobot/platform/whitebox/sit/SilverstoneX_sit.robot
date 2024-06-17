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
# Script       : midstone100X_diag.robot
# Date         : 4/12/2021
# Author       : Yagami jiang <yajiang@celestica.com>


*** Settings ***
Variables         SIT_variable.py
Library           SITLib.py
Library           CommonLib.py
Library           ../WhiteboxLibAdapter.py
Resource          SIT_keywords.robot
Resource          CommonResource.robot

#Suite Setup       OS Connect Device
#Suite Teardown    OS Disconnect Device


*** Test Cases ***
Detection_and_Reporting
    [Documentation]  The information of CPU should be correctly detected and reported by system
    [Tags]     Detection_and_Reporting  CLSWB-SITG-CPU1-0001-0001  whitebox  Function  test_silverstoneX
    [Timeout]  3 min 00 seconds
    [Setup]  OS Connect Device
    Step  1  CheckCpuInfo
    Step  2  CheckLsCpu
    [Teardown]  OS Disconnect Device

System_Information
    [Documentation]  Validate each system information are correct, such as CPU, memory, switch chipset, SFP+ port, RJ45 port, and so on PCI devices.
    [Tags]     System_Information  CLSWB-SITG-OSCK-0002-0001  whitebox  test_silverstoneX
    [Timeout]  10 min 00 seconds
    [Setup]  OS Connect Device
	independent_step  1  InitForLspciAndFru
	independent_step  2  Check System Information
    #Sub-Case  System_Information_1  Check System Information
    [Teardown]  OS Disconnect Device


Reboot_Cycling_Test
    [Documentation]  No error occurs during 500 times cycling test for each canister
    [Tags]     Reboot_Cycling_Test  CLSWB-SITG-STAB-0004-0001  whitebox  Stability  test_silverstoneX
    [Setup]  OS Connect Device
    FOR  ${i}  IN RANGE  1  ${reboot_cycle_time}
    independent_step  0  show_loop  ${i}
    independent_step  1  SetSelClear
    independent_step  2  SetDmesgClear
    independent_step  3  execute_cmd  cat /dev/null > /var/log/meessages
    independent_step  4  RebootOS
	independent_step  5  check_log_info
    #Step  5  CheckDmesgInfo
    #Step  6  CheckCMDResponse  ipmitool sel list  ${sel_error_list}  False  False  False  True
    #Step  7  CheckCMDResponse  cat /var/log/messages  ${messages_error_list}  False  False  False  True
    independent_step  8  Check System Information
	independent_step  9  check_sw_main_or_minor  BMC
	independent_step  10  check_sw_main_or_minor  BIOS
	independent_step  11  check_res_nums_pass_or_fail
	independent_step  12  enter_sdk  ${pam4_400g_32_config}  
	independent_step  13  run_loopback_traffic_for_innovium  ${port_num_pam4_400g}  ${rate_num_config["${pam4_400g_32_config}"][0]}  test_time=60
	independent_step  14  exit_sdk 
    END
    [Teardown]  OS Disconnect Device


AC_Power_Cycling_Test
    [Documentation]  No error occurs during 500 times cycling test
    [Tags]     AC_Power_Cycling_Test  CLSWB-SITG-STAB-0005-0001  whitebox  Stability  test_silverstoneX
    [Setup]  OS Connect Device
    FOR  ${i}  IN RANGE  1  ${ac_power_cycle_time}
    independent_step  0  show_loop  ${i}
    independent_step  1  SetSelClear
    independent_step  2  SetDmesgClear
    independent_step  3  execute_cmd  cat /dev/null > /var/log/meessages
    independent_step  4  set_pdu_state_connect_os  reboot  ${PDU_Port}  300  30
       independent_step  4  SetWait  30
	independent_step  5  check_log_info
    #Step  5  CheckDmesgInfo
    #Step  6  CheckCMDResponse  ipmitool sel list  ${sel_error_list}  False  False  False  True
    #Step  7  CheckCMDResponse  cat /var/log/messages  ${messages_error_list}  False  False  False  True
	Step  8  Check System Information
	independent_step  9  check_sw_main_or_minor  BMC
	independent_step  10  check_sw_main_or_minor  BIOS
	independent_step  11  check_res_nums_pass_or_fail
	#independent_step  12  enter_sdk  ${pam4_400g_32_config}  
	#independent_step  13  run_loopback_traffic_for_innovium  ${port_num_pam4_400g}  ${rate_num_config["${pam4_400g_32_config}"][0]}  test_time=60
	#independent_step  14  exit_sdk 
    END
    [Teardown]  OS Disconnect Device


DC_Power_Cycling_Test
    [Documentation]  No error occurs during 500 times cycling test for each canister
    [Tags]     DC_Power_Cycling_Test  CLSWB-SITG-STAB-0006-0001  whitebox  Stability  test_silverstoneX
    [Setup]  OS Connect Device
    FOR  ${i}  IN RANGE  1  ${dc_power_cycle_time}
	independent_step  0  show_loop  ${i}
    independent_step  1  SetSelClear
    independent_step  2  SetDmesgClear
    independent_step  3  execute_cmd  cat /dev/null > /var/log/meessages
    independent_step  4  SetPowerStatus  cycle  connection=True
    #Step  5  CheckDmesgInfo
	independent_step  5  check_log_info
    #Step  6  CheckCMDResponse  ipmitool sel list  ${sel_error_list}  False  False  False  True
    #Step  7  CheckCMDResponse  cat /var/log/messages  ${messages_error_list}  False  False  False  True
	independent_step  11  check_res_nums_pass_or_fail
    independent_step  8  Check System Information
	independent_step  9  check_sw_main_or_minor  BMC
	independent_step  10  check_sw_main_or_minor  BIOS
	independent_step  12  enter_sdk  ${pam4_400g_32_config}  
	independent_step  13  run_loopback_traffic_for_innovium  ${port_num_pam4_400g}  ${rate_num_config["${pam4_400g_32_config}"][0]}  test_time=60
	independent_step  14  exit_sdk  
    END
    [Teardown]  OS Disconnect Device


Boot_From_USB_Flash_Drive
    [Documentation]  The system can boot from USB driver normally
    [Tags]     Boot_From_USB_Flash_Drive  CLSWB-SITG-USB1-0002-0001  whitebox  Function  USB
    [Timeout]  10 min 00 seconds
    [Setup]  OS Connect Device
    Step  1  SetBiosByStep  ${set_u_disk_first_boot}  True  False  ${u_disk_os_flag}
    Step  2  SetPduStatus  reboot  ${PDU_Port}
    Step  3  SetBiosByStep  ${resume_normal_boot}  False  True
    OS Disconnect Device
    [Teardown]  Run Keyword If Test Failed
    ...  Run Keywords
    ...  END AC And Connect OS  AND
    ...  OS Disconnect Device


File_Transfers_From_HDD_To_USB_Devices
    [Documentation]  Use md5 check tool to check the transfer file.
    [Tags]     File_Transfers_From_HDD_To_USB_Devices  CLSWB-SITG-USB1-0003-0001  whitebox  Function  USB  test_silverstoneX
    [Timeout]  3 min 00 seconds
    [Setup]  OS Connect Device
    Step  1  CheckFileFromUDisk
    OS Disconnect Device
    [Teardown]  Run Keyword If Test Failed
    ...  Run Keywords
    #...  execute_cmd  rm -rf ${dut_file_path}  AND
    ...  execute_cmd  umount /mnt  AND
    ...  OS Disconnect Device


USB_Link_Speed
    [Documentation]  USB device work at correct link speed mode, such as USB 1.0, USB 2.0 or USB 3.0.
    [Tags]     USB_Link_Speed  CLSWB-SITG-USB1-0005-0001  whitebox  Function  USB  test_silverstoneX
    # [Timeout]  3 min 00 seconds
    [Setup]  OS Connect Device
    Step  1  CheckUSBTransferSpeed  ${usb_min_speed}  10
    [Teardown]  OS Disconnect Device


Specification_Analysis
   [Documentation]  The information of memories installed should be correctly detected and reported by system
   [Tags]     Specification_Analysis  CLSWB-SITG-CPU1-0001-0001  whitebox  Function  test_silverstoneX
   [Timeout]  3 min 00 seconds
   [Setup]  OS Connect Device
   Step  1  CheckMemtotalSize
   Step  2  CheckMemFreeSize
   Step  3  CheckDmiMemoryInfo
   [Teardown]  OS Disconnect Device


Info_check
   [Documentation]  The HDD inventory is consistent with the HDD production information.
   [Tags]     Info_check  CLSWB-SITG-STOR-0001-0001  whitebox  Function  test_silverstoneX
   [Timeout]  3 min 00 seconds
   [Setup]  OS Connect Device
   Step  1  CheckLsBlk
   Step  2  CheckSmartctlInfo
   [Teardown]  OS Disconnect Device


Memory_performance
    [Documentation]  The STREAM benchmark is a simple synthetic benchmark program that measures sustainable memory
                    ...  bandwidth (in MB/s) and the corresponding computation rate for simple vector kernels.
    [Tags]     Memory_performance  CLSWB-SITG-PERF-0003-0001  whitebox  Stream  test_silverstoneX
    [Timeout]  10 min 00 seconds
    [Setup]  OS Connect Device
    Step  1  RunStreamIray
    [Teardown]  OS Disconnect Device


Full_loading_stress_test
    [Documentation]  No error occurs during test
    [Tags]     Full_loading_stress_test  CLSWB-SITG-STAB-0001-0001  whitebox  stability  test_silverstoneX
    [Timeout]  15 day 0 min 00 seconds
    [Setup]  OS Connect Device
        Step  add-0  RebootOS
    Step  add-1  execute_cmd  rm -rf ${pc_log_path}  60  True
    Step  add-2  execute_cmd  rm -rf ${dut_file_path}
    Step  1  SetSelClear
    Step  2  SetDmesgClear
    Step  3  execute_cmd  cat /dev/null > /var/log/messages
    Step  4  execute_cmd  modprobe
    Step  5  RunOrKillCPUFullLoad
    Step  6  RunFio
    #Step  7  RunStressapptest
    Step  8  RunOrKillMemtester
    Step  9  SetWait  ${set_wait_time}
        Step  10  getPrompt
    Step  10  RunOrKillMemtester  True  True
    Step  11  RunOrKillCPUFullLoad  ${dut_cpu_platform}  True
    Step  12  CopyFileToPC
    Step  13  CopyFileToPC  ${dut_file_path}/log  .txt
    Step  14  CheckFioLog
    #Step  15  CheckStressapptestLog
    Step  16  CheckMemtesterLog
    Step  17  CheckCMDResponse  ipmitool sel list  ${sel_error_list}  False  False  False  True
    Step  18  CheckCMDResponse  dmesg  ${dmesg_error_list}  False  False  False  True
    Step  19  CheckCMDResponse  cat /var/log/messages  ${messages_error_list}  False  False  False  True
    Step  20  execute_cmd  rm -rf ${dut_file_path}
    [Teardown]  OS Disconnect Device


########################################## Caleb Start ############################################################
#InitForLspciAndFru
#    [Documentation]  initialization lspci and ipmitool fru list. pls run the case before testing
#    [T#ags]  InitForLspciAndFru
#    [Setup]  OS Connect Device
#    Step  1  InitForLspciAndFru
#    [Teardown]  OS Disconnect Device


Read_write_function_Check
    [Documentation]  The SSD read and write performance meet the spec
    [Tags]  Read_write_function_Check  CLSWB-SITG-STOR  CLSWB-SITG-STOR-0002-0001  SilverstoneX  test_silverstoneX
    [Setup]  OS Connect Device
    Step  1  write_object_on_hdd
    Step  2  check_storage_readwrite_speed  ${storage_min_speed}  10
    [Teardown]  OS Disconnect Device


USB_full_loading_test
    [Documentation]  all USB device should be work normally at the same time
    [Tags]  USB_full_loading_test  CLSWB-SITG-USB1  CLSWB-SITG-USB1-0004-0001  SilverstoneX  test_silverstoneX
    [Setup]  OS Connect Device
    Step  1  KillProcess  fio
    ${disk_name}  get_sandisk_usb_device_name
    Step  2  auto_detection_usb_device  ${disk_name}
    Step  3  run_fio_for_usb  ${disk_name}
    [Teardown]  OS Disconnect Device


Speedstep
    [Documentation]  Each CPU cores’ frequency should update the maximum value that the CPU spec defined
    [Tags]  Speedstep  CLSWB-SITG-CPU1  CLSWB-SITG-CPU1-0006-0001  SilverstoneX
    [Setup]  OS Connect Device
    Step  1  set_speedstep_from_bios  ${enter_speedstep_setup_interface}  ${setup_speedstep_step}  Enable
    Step  2  run_or_kill_cpuburn
    ${frequency_enable}  get_cpu_cores_frequency
    Step  3  run_or_kill_cpuburn  True  ${Speedstep_path}  True
    Step  4  check_frequency  ${expect_enable_frequency}  ${frequency_enable}  enable
    Step  5  set_speedstep_from_bios  ${enter_speedstep_setup_interface}  ${setup_speedstep_step}  Disable
    Step  6  run_or_kill_cpuburn
    ${frequency_disable}  get_cpu_cores_frequency
    Step  7  run_or_kill_cpuburn  True  ${Speedstep_path}  True
    Step  8  check_frequency  ${expect_disable_frequency}  ${frequency_disable}  disable
    OS Disconnect Device
    [Teardown]  Run Keyword If Test Failed
    ...  Run Keywords
    ...  END AC And Connect OS  AND
    ...  OS Disconnect Device


USB_detection_and_enumeration
    [Documentation]  USB detection and enumeration
    [Tags]  USB_detection_and_enumeration  CLSWB-SITG-USB1  CLSWB-SITG-USB1-0001-0001  test_silverstoneX
    [Setup]  OS Connect Device
    ${disk_name}  get_sandisk_usb_device_name
    Step  1  auto_detection_usb_device  ${disk_name}
    [Teardown]  OS Disconnect Device


CPU_loading_test
    [Documentation]  Check the CPU/Memory usage, they shall be lower than 50% if no Package Manager is running
    [Tags]  CPU_loading_test  CLSWB-SITG-CPU1  CLSWB-SITG-CPU1-0004-0001  test_silverstoneX
    [Setup]  OS Connect Device
    Step  1  RebootOS  10  180
    Step  2  set_system_idle  0.17
    ${cpu_usage}  get_cpu_usage
    Step  3  check_cpu_usage  ${cpu_usage}
    ${memory_usage}  get_memory_usage
    Step  4  check_memory_usage  ${memory_usage}
    [Teardown]  OS Disconnect Device


Port_connect_test
    [Documentation]  1. Serial port should use normally 2. Tera Term will output correct information.
    [Tags]  Port_connect_test  CLSWB-SITG-CONP  CLSWB-SITG-CONP-0002-0001  test_silverstoneX
    [Setup]  OS Connect Device
    FOR  ${index}  IN RANGE  1  6
    OS Disconnect Device
    OS Connect Device
    Step  1  SetWait  5
    Step  2  CheckCMDResponse  ${check_cmd}  ${check_keyword}
    END
    [Teardown]  OS Disconnect Device



i2c_read_write
    [Documentation]  All I2C devices can be read/write successfully (full configuration)
    [Tags]  i2c_read_write  CLSWB-SITG-I2CT  CLSWB-SITG-I2CT-0001-0001  SilverstoneX
    [Setup]  OS Connect Device
    Step  1  install_diag_tool
    Step  2  check_i2c_read  True
    Step  3  check_i2c_write  True
    [Teardown]  OS Disconnect Device


i2c_stress
    [Documentation]  No error occurs during stress test for each I2C device access 1000 times
    [Tags]  i2c_stress  CLSWB-SITG-I2CT  CLSWB-SITG-I2CT-0002-0001  SilverstoneX
    [Setup]  OS Connect Device
    Step  1  install_diag_tool
    Step  2  SetSelClear
    Step  3  SetDmesgClear
    Step  4  execute_cmd  cat /dev/null > /var/log/messages
    Step  5  i2c_stress  True
    Step  6  CheckDmesgInfo
    Step  7  CheckCMDResponse  ipmitool sel list  ${sel_error_list}  False  False  False  True
    Step  8  CheckCMDResponse  cat /var/log/messages  ${messages_error_list}  False  False  False  True
    Step  9  CheckBMCIP
    [Teardown]  OS Disconnect Device


System_idle_testing
    [Documentation]  No error occurs during test
    [Tags]  System_idle_testing  CLSWB-SITG-STAB  CLSWB-SITG-STAB-0007-0001  test_silverstoneX
    [Setup]  OS Connect Device
    Step  add_1  InitForLspciAndFru
    Step  1  SetSelClear
    Step  2  SetDmesgClear
    Step  3  execute_cmd  cat /dev/null > /var/log/messages
    Step  4  Check System Information
    Step  5  set_system_idle
    Step  5  getPrompt
    Step  6  CheckDmesgInfo
    Step  7  CheckCMDResponse  ipmitool sel list  ${sel_error_list}  False  False  False  True
    Step  8  CheckCMDResponse  cat /var/log/messages  ${messages_error_list}  False  False  False  True
    Step  9  Check System Information
    [Teardown]  OS Disconnect Device


SSD_Performance
    [Documentation]  Test results should meet SSD spec or get the system IO bottleneck
    [Tags]  SSD_Performance  CLSWB-SITG-PERF  CLSWB-SITG-PERF-0002-0001  test_silverstoneX
    [Setup]  OS Connect Device
    Step  1  detected_ssd
    FOR  ${filename}  IN  @{ssd_name}
        Step  2.1  format_ssd  ${filename}
        FOR  ${config}  IN  @{fio_config["${filename}"].keys()}
        ${log_path}  run_fio_from_config  ${filename}  ${fio_config["${filename}"]["${config}"]}  ${config}
        Step  2.2.1  check_fio_log_from_dut  ${log_path}  ${expect_ssd_performance["${filename}"]["${config}"]}
        END
    END
    [Teardown]  OS Disconnect Device


USB_IO_performance
    [Documentation]  1. The speed of USB device meet the spec
    [Tags]  USB_IO_performance  CLSWB-SITG-PERF  CLSWB-SITG-PERF-0004-0001  test_silverstoneX
    [Setup]  OS Connect Device
    FOR  ${device_name}  IN  @{usb_performance.keys()}
        Step  1  touch_object_on_usb  ${device_name}
        FOR  ${time}  IN RANGE  1  11
        ${speed}  get_usb_speed_from_hdparm  ${device_name}
        Step  2  check_usb_performance  ${speed}  ${usb_performance["${device_name}"]}  ${time}
        END
    END
    [Teardown]  OS Disconnect Device



# This case need Manual operation
PSU_Redundant_stress_test
    [Documentation]  Check system stability when two PSU switch to one PSU under full loading mode.
    [Tags]  PSU_Redundant_stress_test  CLSWB-SITG-POWE  CLSWB-SITG-POWE-0001-0001  SilverstoneX
    [Setup]  OS Connect Device
    Step  add_1  InitForLspciAndFru
    Step  1  SetSelClear
    Step  2  SetDmesgClear
    Step  3  execute_cmd  cat /dev/null > /var/log/messages
    Step  4  Check System Information
    ${cpuburn}  run_or_kill_cpuburn  False  /home/white_box/cpuburn_log  True
    ${memtester}  run_or_kill_memtester_and_return_path
    @{fio_log}  run_fio_for_all_disk  43200
    Step  5  psu_redundant_test
    Step  6  SetWait  43200
    Step  7  getPrompt
    Step  7  run_or_kill_cpuburn  True
    Step  8  run_or_kill_memtester_and_return_path  True  True
    Step  9  check_memtester_success  ${memtester}
    Step  10  check_cpuburn_log  ${cpuburn}
    Step  11  check_all_fio_run_success  @{fio_log}
    Step  12  CheckDmesgInfo
    Step  13  CheckCMDResponse  ipmitool sel list  ${hot_plug_sel_error_list}  False  False  False  True
    Step  14  CheckCMDResponse  cat /var/log/messages  ${messages_error_list}  False  False  False  True
    Step  15  Check System Information For One PSU
    Step  16  recovery_psu
    Step  17  set_pdu_state_connect_os  reboot  ${PDU_Port}  300  30
    Step  18  Check System Information
    OS Disconnect Device
    [Teardown]  Run Keyword If Test Failed
    ...  Run Keywords
    ...  END AC And Connect OS  AND
    ...  OS Disconnect Device


# This case need Manual operation
Power_Consumption_test
    [Documentation]  The purpose of this test is to measure power consumption when system in idle and full loading mode.
    [Tags]  Power_Consumption_test  CLSWB-SITG-POWE  CLSWB-SITG-POWE-0002-0001  SilverstoneX
    [Setup]  OS Connect Device
    Step  1  RebootOS
    Step  2  set_system_idle  0.17
    ${ipmitool_idle}  get_consumption_from_ipmitool
    ${meter_idle}  record_power_consumption
    ${cpuburn}  run_or_kill_cpuburn  False  /home/white_box/cpuburn_log  True
    ${memtester}  run_or_kill_memtester_and_return_path
    Step  7  run_fio_for_all_disk  43200
    independent_step  8  enter_sdk  ${pam4_400g_32_config}  remote=True
	independent_step  9  run_loopback_traffic_for_innovium  ${port_num_pam4_400g}  ${rate_num_config["${pam4_400g_32_config}"][0]}  test_time=60  remote=True
    ${meter_full}  record_power_consumption
    ${ipmitool_full}  get_consumption_from_ipmitool
    independent_step  12  exit_sdk  remote=True
    Step  13  KillProcess  fio
    Step  14  run_or_kill_cpuburn  True
    Step  15  run_or_kill_memtester_and_return_path  True  True
    Step  16  check_memtester_success  ${memtester}
    Step  17  check_cpuburn_log  ${cpuburn}
    Step  18  check_consumption  ${ipmitool_full}  ${ipmitool_idle}  ${meter_full}  ${meter_idle}
    [Teardown]  OS Disconnect Device


Optical_module_eeprom_access_Test
    [Documentation]  All the ports should be show correct eeprom information
    [Tags]  Optical_module_eeprom_access_Test  CLSWB-SITG-COMP  CLSWB-SITG-COMP-0003-0001  SilverstoneX
    [Setup]  OS Connect Device
    Step  1  install_diag_tool
    Step  2  check_port_optical_module_eeprom_information
    [Teardown]  OS Disconnect Device


Optics_Module_EEPROM_Access_Stress_Test
    [Documentation]  No error (Information lose,Inaccessible)occurs during stress.
    [Tags]  Optics_Module_EEPROM_Access_Stress_Test  CLSWB-SITG-STAB  CLSWB-SITG-STAB-0011-0001  SilverstoneX
    [Setup]  OS Connect Device
    Step  1  install_diag_tool
    ${init}  check_port_optical_module_eeprom_information
    ${cpuburn}  run_or_kill_cpuburn  False  /home/white_box/module_eeprom/cpuburn_log  True
    ${memtester}  run_or_kill_memtester_and_return_path
    @{fio_log}  run_fio_for_all_disk  43200
    Step  2  SetWait  43200
    Step  3  getPrompt
    Step  3  run_or_kill_cpuburn  True
    Step  4  run_or_kill_memtester_and_return_path  True  True
    Step  5  check_memtester_success  ${memtester}
    Step  6  check_cpuburn_log  ${cpuburn}
    Step  7  check_all_fio_run_success  @{fio_log}
    ${new}  check_port_optical_module_eeprom_information
    Step  8  check_file_equal  ${init}  ${new}
    [Teardown]  OS Disconnect Device


# This case need Manual operation
Hot_Plug_check_10_cycles
    [Documentation]  The system should detect the Optical module and the system can work normally
    [Tags]  Hot_Plug_check_10_cycles  CLSWB-SITG-COMP  CLSWB-SITG-COMP-0002-0001  SilverstoneX
    [Setup]  OS Connect Device
    Step  0  install_diag_tool
    Step  1  SetSelClear
    Step  2  SetDmesgClear
    Step  3  execute_cmd  cat /dev/null > /var/log/meessages
    #Step  4  run_fio_for_all_disk  43200
    Step  4  RunFio
    Step  5  RunOrKillCPUFullLoad
    ${memtester}  run_or_kill_memtester_and_return_path
    ${port_number}  init_optical_module_hot_plug
    FOR  ${port_fast}  IN RANGE  ${port_number}
        FOR  ${cycle_fast}  IN RANGE  10
            Step  5  optical_module_hot_plug  ${port_fast}  ${cycle_fast}  num=${port_number}
        END
    END
    FOR  ${port_slow}  IN RANGE  ${port_number}
        FOR  ${cycle_slow}  IN RANGE  10
            Step  6  optical_module_hot_plug  ${port_slow}  ${cycle_slow}  False  num=${port_number}
        END
    END
    Step  9  KillProcess  fio
    Step  10  run_or_kill_memtester_and_return_path  True  True
    Step  11  RunOrKillCPUFullLoad  ${dut_cpu_platform}  True
    Step  12  check_memtester_success  ${memtester}
    Step  13  execute_cmd  cd /
    OS Disconnect Device
    [Teardown]  Run Keyword If Test Failed
    ...  Run Keywords
    ...  END AC And Connect OS  AND
    ...  OS Disconnect Device




LAN_Speed_Auto_negotiation
    [Documentation]  NIC speed/duplex state is meet specification under direct connection and connect swtich environment.
    [Tags]  LAN_Speed_Auto_negotiation  CLSWB-SITG-MGMT  CLSWB-SITG-MGMT-0004-0001
    [Setup]  OS Connect Device
    @{modes}  get_supported_link_modes  ${management_port_name}
    Step  1  set_lan_speed_auto_negotiation  ${management_port_name}  mode  True
    Step  2  check_nic_work_status
    Step  3  check_nic_speed_auto_negotiation  ${management_port_name}
    FOR  ${mode}  IN  @{modes}
        Step  4  set_lan_speed_auto_negotiation  ${management_port_name}  ${mode}
        Step  5  check_nic_work_status
        ${speed_duplex}  get_nic_speed_and_duplex_state  ${management_port_name}
        Step  6  check_nic_speed_and_duplex_state  ${speed_duplex}  ${mode}
    END
    [Teardown]  OS Disconnect Device


#For silverstoneX
SFP+_10G_Optical_module_Traffic_Test
    [Documentation]  1.No packet loss during the testing 2.No error or system hang happened during and after testing
    [Tags]  SFP+_10G_Optical_module_Traffic_Test  CLSWB-SITG-COMP  CLSWB-SITG-COMP-0008-0001
    [Setup]  OS Connect Device
    Step  1  enter_sdk_c  -m PAM4_400G_32
    @{port}   create list  129  130
    Step  2  check_port_link_up  ${port}
    independent_step  3  config_snake  -p '129,130' -lb 'NONE' -v -b2
    independent_step  4  execute_sdk_cmd  diagtest snake start_traffic -n 300
    independent_step  5  SetWait  60
    FOR  ${i}  IN RANGE  3
    independent_step  1  check_rate  9.5  10.5
    END
    independent_step  7  SetWait  43200
    FOR  ${i}  IN RANGE  3
    independent_step  1  check_rate  9.5  10.5
    END
    independent_step  8  execute_sdk_cmd  diagtest snake stop_traffic -id 1
    independent_step  9  check_counters
    Step  10  exit_sdk_c
    independent_step  11  execute_cmd  cd /
    [Teardown]  OS Disconnect Device


CPU_performance
    [Documentation]  Test results should meet the CPU SPEC
    [Tags]  CPU_performance  CLSWB-SITG-PERF  CLSWB-SITG-PERF-0001-0001
    [Setup]  OS Connect Device
    Step  1  copy_lnkpack_to_dut
    Step  2  config_and_run_lnkpack
    [Teardown]  OS Disconnect Device


10G_Port_enable_disable_function_test
    [Documentation]  Enable/disable and check it works normal.
    [Tags]  10G_Port_enable_disable_function_test  CLSWB-SITG-LSFQ  CLSWB-SITG-LSFQ-0005-0001
    [Setup]  OS Connect Device
    Step  1  tenG_port_enable_and_disable
    [Teardown]  OS Disconnect Device


IPv6_Test
    [Documentation]  The purpose of this test is to validate LAN port function with IPv6 protocol by static method.
    [Tags]  IPv6_Test  CLSWB-SITG-MGMT  CLSWB-SITG-MGMT-0008-0001
    [Setup]  OS Connect Device
    Step  1  config_dut_or_pc_ipv6  True  ${dut_nic_name}  ${dut_ipv6}
    Step  2  config_dut_or_pc_ipv6  False  ${pc_nic_name}  ${pc_ipv6}
    Step  3  check_LAN_port_connectivity
    ${dut_dhcp_ipv6}  get_dut_ipv6_from_dhcp
    ${pc_dhcp_ipv6}  get_pc_ipv6  ${dut_dhcp_ipv6}
    Step  4  check_ping_dhcp_ipv6  ${dut_dhcp_ipv6}  ${pc_dhcp_ipv6}
    [Teardown]  OS Disconnect Device


1G_port_Link_Speed_Check_by_full_test
    [Documentation]  Check all the lan port speed is same and could meet the max speed.
    [Tags]  1G_port_Link_Speed_Check_by_full_test  CLSWB-SITG-LANT  CLSWB-SITG-LANT-0006-0001
    [Setup]  OS Connect Device
	Step  1  get_eth_speed_from_ethtool  DUT  net_name=${one_G_net_name}  exp_speed=${one_G_exp_lan_link_speed}
	Step  2  copy_tool_files_from_pc_to_os
	Step  3  run_iperf  expect_bw=${one_G_exp_bw}
    [Teardown]  OS Disconnect Device


1G_port_100_meter_NIC_cable_Test
    [Documentation]  use iperf to check the 100m lan port performance
    [Tags]  1G_port_100_meter_NIC_cable_Test  CLSWB-SITG-LANT  CLSWB-SITG-LANT-0005-0001
    [Setup]  OS Connect Device
	Step  1  run_iperf  300  expect_bw=${one_G_exp_bw}
    [Teardown]  OS Disconnect Device


LAN_Speed_check_Auto_and_Manual
    [Documentation]  NIC speed/duplex state is meet specification under direct connection and connect swtich environment.
    [Tags]  LAN_Speed_check_Auto_and_Manual  CLSWB-SITG-LANT  CLSWB-SITG-LANT-0004-0001
    [Setup]  OS Connect Device
    @{modes}  get_supported_link_modes  ${one_G_net_name}
    Step  1  set_lan_speed_auto_negotiation  ${one_G_net_name}  auto_negotiation=True
    Step  2  check_nic_work_status
    Step  3  check_nic_speed_auto_negotiation  ${one_G_net_name}
    FOR  ${mode}  IN  @{modes}
        Step  4  set_lan_speed_auto_negotiation  ${one_G_net_name}  ${mode}
        Step  5  check_nic_work_status
        ${speed_duplex}  get_nic_speed_and_duplex_state  ${one_G_net_name}
        Step  6  check_nic_speed_and_duplex_state  ${speed_duplex}  ${mode}
    END
    [Teardown]  OS Disconnect Device


PSU_Info_and_Hot_Plug
    [Documentation]  BMC should record the current PSU state in SEL and the system can work normally.
    [Tags]  PSU_Info_and_Hot_Plug  CLSWB-SITG-HOTP  CLSWB-SITG-HOTP-0003-0001
    [Setup]  OS Connect Device
    Step  1  SetSelClear
    Step  2  SetDmesgClear
    Step  3  execute_cmd  cat /dev/null > /var/log/meessages
    #Step  4  run_fio_for_all_disk  43200
    Step  4  RunFio
    Step  5  RunOrKillCPUFullLoad
    ${memtester}  run_or_kill_memtester_and_return_path
    FOR  ${psu}  IN RANGE  ${psu_hot_plug_num}
        FOR  ${cycle_fast}  IN RANGE  ${psu_hot_plug_cycle}
            Step  7  hot_plug_sit   ${psu}  ${cycle_fast}
            Step  8  save_log_then_clear
        END
        FOR  ${cycle_slow}  IN RANGE  ${psu_hot_plug_cycle}
            Step  7  hot_plug_sit   ${psu}  ${cycle_slow}  False
            Step  8  save_log_then_clear
        END
    END
    Step  9  KillProcess  fio
    Step  10  run_or_kill_memtester_and_return_path  True  True
    Step  11  RunOrKillCPUFullLoad  ${dut_cpu_platform}  True
    Step  12  check_memtester_success  ${memtester}
    OS Disconnect Device
    [Teardown]  Run Keyword If Test Failed
    ...  Run Keywords
    ...  END AC And Connect OS  AND
    ...  OS Disconnect Device


Power_cable_Hot_Plug
    [Documentation]  BMC should record the current PSU state in SEL and the system can work normally.
    [Tags]  Power_cable_Hot_Plug  CLSWB-SITG-HOTP  CLSWB-SITG-HOTP-0004-0001
    [Setup]  OS Connect Device
    Step  1  SetSelClear
    Step  2  SetDmesgClear
    Step  3  execute_cmd  cat /dev/null > /var/log/meessages
    #Step  4  run_fio_for_all_disk  43200
    Step  4  RunFio
    Step  5  RunOrKillCPUFullLoad
    ${memtester}  run_or_kill_memtester_and_return_path
    FOR  ${cable}  IN RANGE  ${power_cable_hot_plug_num}
        FOR  ${cycle_fast}  IN RANGE  ${power_cable_hot_plug_cycle}
            Step  7  hot_plug_sit   ${cable}  ${cycle_fast}  True  ${psu_cable_unplug_flag}  ${psu_cable_insert_flag}  PSU_Cable
            Step  8  save_log_then_clear
        END
        FOR  ${cycle_slow}  IN RANGE  ${power_cable_hot_plug_cycle}
            Step  7  hot_plug_sit   ${cable}  ${cycle_slow}  False  ${psu_cable_unplug_flag}  ${psu_cable_insert_flag}  PSU_Cable
            Step  8  save_log_then_clear
        END
    END
    Step  9  KillProcess  fio
    Step  10  run_or_kill_memtester_and_return_path  True  True
    Step  11  RunOrKillCPUFullLoad  ${dut_cpu_platform}  True
    Step  12  check_memtester_success  ${memtester}
    OS Disconnect Device
    [Teardown]  Run Keyword If Test Failed
    ...  Run Keywords
    ...  END AC And Connect OS  AND
    ...  OS Disconnect Device


Fan_Hot_Plug
    [Documentation]  BMC should record the current PSU state in SEL and the system can work normally.
    [Tags]  Fan_Hot_Plug  CLSWB-SITG-HOTP  CLSWB-SITG-HOTP-0005-0001
    [Setup]  OS Connect Device
    Step  1  SetSelClear
    Step  2  SetDmesgClear
    Step  3  execute_cmd  cat /dev/null > /var/log/meessages
    #Step  4  run_fio_for_all_disk  43200
    Step  4  RunFio
    Step  5  RunOrKillCPUFullLoad
    ${memtester}  run_or_kill_memtester_and_return_path
    FOR  ${fan}  IN RANGE  ${fan_hot_plug_num}
        FOR  ${cycle_fast}  IN RANGE  ${fan_hot_plug_cycle}
            Step  7  hot_plug_sit   ${fan}  ${cycle_fast}  True  ${fan_unplug_flag}  ${fan_insert_flag}  Fan
            Step  8  save_log_then_clear
        END
        FOR  ${cycle_slow}  IN RANGE  ${fan_hot_plug_cycle}
            Step  7  hot_plug_sit   ${fan}  ${cycle_slow}  False  ${fan_unplug_flag}  ${fan_insert_flag}  Fan
            Step  8  save_log_then_clear
        END
    END
    Step  9  KillProcess  fio
    Step  10  run_or_kill_memtester_and_return_path  True  True
    Step  11  RunOrKillCPUFullLoad  ${dut_cpu_platform}  True
    Step  12  check_memtester_success  ${memtester}
    OS Disconnect Device
    [Teardown]  Run Keyword If Test Failed
    ...  Run Keywords
    ...  END AC And Connect OS  AND
    ...  OS Disconnect Device


Fan_tray_Hot_Plug
    [Documentation]  BMC should record the current PSU state in SEL and the system can work normally.
    [Tags]  Fan_tray_Hot_Plug  CLSWB-SITG-HOTP  CLSWB-SITG-HOTP-0006-0001
    [Setup]  OS Connect Device
    Step  1  SetSelClear
    Step  2  SetDmesgClear
    Step  3  execute_cmd  cat /dev/null > /var/log/meessages
    #Step  4  run_fio_for_all_disk  43200
    Step  4  RunFio
    Step  5  RunOrKillCPUFullLoad
    ${memtester}  run_or_kill_memtester_and_return_path
    FOR  ${fan_tray}  IN RANGE  ${fan_tray_hot_plug_num}
        FOR  ${cycle_fast}  IN RANGE  ${fan_tray_hot_plug_cycle}
            Step  7  hot_plug_sit   ${fan_tray}  ${cycle_fast}  True  ${fan_tray_unplug_flag}  ${fan_tray_insert_flag}  Fan_tray
            Step  8  save_log_then_clear
        END
        FOR  ${cycle_slow}  IN RANGE  ${fan_tray_hot_plug_cycle}
            Step  7  hot_plug_sit   ${fan_tray}  ${cycle_slow}  False  ${fan_tray_unplug_flag}  ${fan_tray_insert_flag}  Fan_tray
            Step  8  save_log_then_clear
        END
    END
    Step  9  KillProcess  fio
    Step  10  run_or_kill_memtester_and_return_path  True  True
    Step  11  RunOrKillCPUFullLoad  ${dut_cpu_platform}  True
    Step  12  check_memtester_success  ${memtester}
    OS Disconnect Device
    [Teardown]  Run Keyword If Test Failed
    ...  Run Keywords
    ...  END AC And Connect OS  AND
    ...  OS Disconnect Device


RJ45_Cable_hot_plug
    [Documentation]  The system should detect the RJ45 port and the system can work normally,run 10 times hotplug test for each cable
    [Tags]  RJ45_Cable_hot_plug  CLSWB-SITG-HOTP  CLSWB-SITG-HOTP-0008-0001
    [Setup]  OS Connect Device
    Step  1  execute_cmd  dhclient
    Step  2  ping_to_pc  DUT
    Step  3  SetSelClear
    Step  4  SetDmesgClear
    Step  5  execute_cmd  cat /dev/null > /var/log/meessages
    #Step  6  run_fio_for_all_disk  43200
    Step  6  RunFio
    Step  7  RunOrKillCPUFullLoad
    ${memtester}  run_or_kill_memtester_and_return_path
    Step  9  run_iperf3_for_hot_plug
    FOR  ${rj}  IN RANGE  ${rj_hot_plug_num}
        FOR  ${cycle_fast}  IN RANGE  ${rj_hot_plug_cycle}
            Step  10  hot_plug_sit   ${rj}  ${cycle_fast}  True  ${rj_unplug_flag}  ${rj_insert_flag}  RJ45
            Step  11  save_log_then_clear
        END
        FOR  ${cycle_slow}  IN RANGE  ${rj_hot_plug_cycle}
            Step  10  hot_plug_sit   ${rj}  ${cycle_slow}  False  ${rj_unplug_flag}  ${rj_insert_flag}  RJ45
            Step  11  save_log_then_clear
        END
    END
    Step  12  KillProcess  fio
    Step  13  KillProcess  iperf3
    Step  14  run_or_kill_memtester_and_return_path  True  True
    Step  15  RunOrKillCPUFullLoad  ${dut_cpu_platform}  True
    Step  16  check_memtester_success  ${memtester}
    OS Disconnect Device
    [Teardown]  Run Keyword If Test Failed
    ...  Run Keywords
    ...  END AC And Connect OS  AND
    ...  OS Disconnect Device


USB_device_Hot_Plug
    [Documentation]  BMC should record the current PSU state in SEL and the system can work normally.
    [Tags]  USB_device_Hot_Plug  CLSWB-SITG-HOTP  CLSWB-SITG-HOTP-0009-0001
    [Setup]  OS Connect Device
    Step  1  SetSelClear
    Step  2  SetDmesgClear
    Step  3  execute_cmd  cat /dev/null > /var/log/meessages
    #Step  4  run_fio_for_all_disk  43200
    Step  4  RunFio
    Step  5  RunOrKillCPUFullLoad
    ${memtester}  run_or_kill_memtester_and_return_path
    FOR  ${usb}  IN RANGE  ${usb_hot_plug_num}
        FOR  ${cycle_fast}  IN RANGE  ${usb_hot_plug_cycle}
            Step  7  hot_plug_sit   ${usb}  ${cycle_fast}  True  ${usb_unplug_flag}  ${usb_insert_flag}  USB
            Step  8  save_log_then_clear
        END
        FOR  ${cycle_slow}  IN RANGE  ${fan_tray_hot_plug_cycle}
            Step  7  hot_plug_sit   ${usb}  ${cycle_slow}  False  ${usb_unplug_flag}  ${usb_insert_flag}  USB
            Step  8  save_log_then_clear
        END
    END
    Step  9  KillProcess  fio
    Step  10  run_or_kill_memtester_and_return_path  True  True
    Step  11  RunOrKillCPUFullLoad  ${dut_cpu_platform}  True
    Step  12  check_memtester_success  ${memtester}
    OS Disconnect Device
    [Teardown]  Run Keyword If Test Failed
    ...  Run Keywords
    ...  END AC And Connect OS  AND
    ...  OS Disconnect Device


Loopback_Hot_Plug_check_10_cycles
    [Documentation]  The system should detect the Optical module and the system can work normally
    [Tags]  Loopback_Hot_Plug_check_10_cycles  CLSWB-SITG-COMP  CLSWB-SITG-COMP-00018-0001  SilverstoneX
    [Setup]  OS Connect Device
    Step  0  install_diag_tool
    Step  1  SetSelClear
    Step  2  SetDmesgClear
    Step  3  execute_cmd  cat /dev/null > /var/log/meessages
    #Step  4  run_fio_for_all_disk  43200
    Step  4  RunFio
    Step  5  RunOrKillCPUFullLoad
    ${memtester}  run_or_kill_memtester_and_return_path
    ${port_number}  init_optical_module_hot_plug
    FOR  ${port_fast}  IN RANGE  ${port_number}
        FOR  ${cycle_fast}  IN RANGE  10
            Step  5  optical_module_hot_plug  ${port_fast}  ${cycle_fast}  True  Loopback  num=${port_number}
        END
    END
    FOR  ${port_slow}  IN RANGE  ${port_number}
        FOR  ${cycle_slow}  IN RANGE  10
            Step  6  optical_module_hot_plug  ${port_slow}  ${cycle_slow}  False  Loopback  num=${port_number}
        END
    END
    Step  9  KillProcess  fio
    Step  10  run_or_kill_memtester_and_return_path  True  True
    Step  11  RunOrKillCPUFullLoad  ${dut_cpu_platform}  True
    Step  12  check_memtester_success  ${memtester}
    Step  13  execute_cmd  cd /
    OS Disconnect Device
    [Teardown]  Run Keyword If Test Failed
    ...  Run Keywords
    ...  END AC And Connect OS  AND
    ...  OS Disconnect Device


DAC_cable_Hot_Plug_check_10_cycles
    [Documentation]  The system should detect the Optical module and the system can work normally
    [Tags]  DAC_cable_Hot_Plug_check_10_cycles  CLSWB-SITG-COMP  CLSWB-SITG-COMP-00028-0001  SilverstoneX
    [Setup]  OS Connect Device
    Step  0  install_diag_tool
    Step  1  SetSelClear
    Step  2  SetDmesgClear
    Step  3  execute_cmd  cat /dev/null > /var/log/meessages
    #Step  4  run_fio_for_all_disk  43200
    Step  4  RunFio
    Step  5  RunOrKillCPUFullLoad
    ${memtester}  run_or_kill_memtester_and_return_path
    ${port_number}  init_optical_module_hot_plug
    FOR  ${port_fast}  IN RANGE  ${port_number}
        FOR  ${cycle_fast}  IN RANGE  10
            Step  5  optical_module_hot_plug  ${port_fast}  ${cycle_fast}  True  DAC_cable  num=${port_number}
        END
    END
    FOR  ${port_slow}  IN RANGE  ${port_number}
        FOR  ${cycle_slow}  IN RANGE  10
            Step  6  optical_module_hot_plug  ${port_slow}  ${cycle_slow}  False  DAC_cable  num=${port_number}
        END
    END
    Step  9  KillProcess  fio
    Step  10  run_or_kill_memtester_and_return_path  True  True
    Step  11  RunOrKillCPUFullLoad  ${dut_cpu_platform}  True
    Step  12  check_memtester_success  ${memtester}
    Step  13  execute_cmd  cd /
    OS Disconnect Device
    [Teardown]  Run Keyword If Test Failed
    ...  Run Keywords
    ...  END AC And Connect OS  AND
    ...  OS Disconnect Device


10G_port_Link_Speed_Check_by_full_test
    [Documentation]  Check all the lan port speed is same and could meet the max speed.
    [Tags]  10G_port_Link_Speed_Check_by_full_test  CLSWB-SITG-LSFQ  CLSWB-SITG-LSFQ-0004-0001
    [Setup]  OS Connect Device
	Step  1  get_eth_speed_from_ethtool  DUT  net_name=${ten_G_net_name}  exp_speed=${ten_G_exp_lan_link_speed}
	Step  2  copy_tool_files_from_pc_to_os
	Step  3  run_iperf  expect_bw=${ten_G_exp_bw}
    [Teardown]  OS Disconnect Device


10G_LAN_Speed_check_Auto_and_Manual
    [Documentation]  NIC speed/duplex state is meet specification under direct connection and connect swtich environment.
    [Tags]  10G_LAN_Speed_check_Auto_and_Manual  CLSWB-SITG-LSFQ  CLSWB-SITG-LSFQ-0003-0001
    [Setup]  OS Connect Device
    @{modes}  get_supported_link_modes  ${ten_G_net_name}
    Step  1  set_lan_speed_auto_negotiation  ${ten_G_net_name}  auto_negotiation=True
    Step  2  check_nic_work_status
    Step  3  check_nic_speed_auto_negotiation  ${ten_G_net_name}
    FOR  ${mode}  IN  @{modes}
        Step  4  set_lan_speed_auto_negotiation  ${ten_G_net_name}  ${mode}
        Step  5  check_nic_work_status
        ${speed_duplex}  get_nic_speed_and_duplex_state  ${ten_G_net_name}
        Step  6  check_nic_speed_and_duplex_state  ${speed_duplex}  ${mode}
    END
    [Teardown]  OS Disconnect Device


10G_DHCP_function_test
    [Documentation]  check the RJ45 Management port DHCP function
    [Tags]  10G_DHCP_function_test  CLSWB-SITG-LSFQ  CLSWB-SITG-LSFQ-0006-0001
    [Setup]  OS Connect Device
	Step  1  set_os_ip_by_dhclient  DUT
	Step  2  ping_to_pc_via_designated_port  DUT  600  port=${ten_G_net_name}
    [Teardown]  OS Disconnect Device

########################################## Caleb END #################################################################


########################################## Janson Start ##############################################################
console_port_bmc_login_out
    [Documentation]  check the Console port Login/out BMC function
    [Tags]  console_port_bmc_login_out  SilverstoneX  CLSWB-SITG-MGMT-0007-0001 
    [Setup]  OS Connect Device
	Step  1  setroot  DUT
	FOR  ${index}  IN RANGE  5
	Step  2  check_bmc_ready  DUT
	END
    [Teardown]  OS Disconnect Device


management_port_bmc_login_out
    [Documentation]  check the Management LAN port Login/out BMC function
    [Tags]  management_port_bmc_login_out  SilverstoneX  CLSWB-SITG-CONP-0006-0001
    [Setup]  OS Connect Device
	Step  1  setroot  DUT
	${info}  GetBmcIP
	FOR  ${index}  IN RANGE  5
	Step  2  check_communication_lan_pc  DUT  ${info}
	END
    [Teardown]  OS Disconnect Device


DHCP_function_test
    [Documentation]  check the RJ45 Management port DHCP function
    [Tags]  DHCP_function_test  SilverstoneX  CLSWB-SITG-MGMT-0002-0001  
    [Setup]  OS Connect Device
	Step  1  setroot  DUT
	Step  2  set_os_ip_by_dhclient  DUT
	Step  3  ping_to_pc  DUT  600
    [Teardown]  OS Disconnect Device


static_function_test
    [Documentation]  check the RJ45 Management port static IP function
    [Tags]  static_function_test  SilverstoneX  CLSWB-SITG-MGMT-0001-0001  
    [Setup]  OS Connect Device
	Step  1  setroot  DUT
	Step  2  set_static_ip  DUT
	Step  3  ping_to_pc  DUT  600
    [Teardown]  OS Disconnect Device


port_enable_disable_function_test
    [Documentation]  check the port diaable and enable function
    [Tags]  port_enable_disable_function_test  SilverstoneX  CLSWB-SITG-LANT-0006-0001  
    [Setup]  OS Connect Device
	Step  1  setroot  DUT
	Step  2  set_port_disable_then_enable  DUT  net_name=${set_enable_disable_name}
	Step  3  set_os_ip_by_dhclient  DUT
	Step  4  ping_to_pc  DUT
    [Teardown]  OS Disconnect Device


1Gb_performance
    [Documentation]  use iperf to check the 1G/10G lan port performance
    [Tags]  1Gb_performance  SilverstoneX  CLSWB-SITG-PERF-0006-0001  
    [Setup]  OS Connect Device
	Step  1  setroot  DUT
	Step  2  copy_tool_files_from_pc_to_os
	Step  3  run_iperf  300  expect_bw=${exp_lan_link_bw}
    [Teardown]  OS Disconnect Device


Hundred_meter_NIC_cable_Test
    [Documentation]  use iperf to check the 100m lan port performance
    [Tags]  Hundred_meter_NIC_cable_Test  SilverstoneX  CLSWB-SITG-MGMT-0005-0001  
    [Setup]  OS Connect Device
	Step  1  setroot  DUT
	Step  2  run_iperf  300  expect_bw=${exp_lan_link_bw}
    [Teardown]  OS Disconnect Device
	
	
link_speed_check_by_manual
    [Documentation]  mamual check the 1G/10G lan port speed
    [Tags]  link_speed_check_by_manual  SilverstoneX  CLSWB-SITG-MGMT-0006-0001  
    [Setup]  OS Connect Device
	Step  1  setroot  DUT
	Step  2  get_eth_speed_from_ethtool  DUT  net_name=${exp_lan_name}  exp_speed=${exp_lan_link_speed}
	Step  2  copy_tool_files_from_pc_to_os
	Step  3  run_iperf
    [Teardown]  OS Disconnect Device


switch_port_bcm_cli
    [Documentation]  Repeat 1000 times by shell script no error occur.
    [Tags]  switch_port_bcm_cli  SilverstoneX  CLSWB-SITG-BCML-0001-0001  
    [Setup]  OS Connect Device
	Step  1  setroot  DUT
	FOR  ${index}  IN RANGE  1000
	independent_step  2  enter_sdk  ${pam4_400g_32_config}
	independent_step  3  exit_sdk
	END
    [Teardown]  OS Disconnect Device
	

switch_port_enable_and_disable
    [Documentation]  set switch port enable and disable
    [Tags]  switch_port_enable_and_disable  SilverstoneX  CLSWB-SITG-LANT-0006-0001  
    [Setup]  OS Connect Device
	Step  1  setroot  DUT
	FOR  ${index}  IN RANGE  501
	Step  2  enter_sdk  ${pam4_400g_32_config}  
	independent_step  3  set_switch_port_enable_or_disable  ${port_num_pam4_400g}  enable
	independent_step  4  set_switch_port_enable_or_disable  ${port_num_pam4_400g}  disable
	Step  5  exit_sdk
	END
    [Teardown]  OS Disconnect Device


switch_port_communication_check
    [Documentation]  check switch port  whether no packet loss during the testing
    [Tags]  switch_port_communication_check  SilverstoneX  CLSWB-SITG-LSFQ-0001-0001  
    [Setup]  OS Connect Device
	Step  1  setroot  DUT
	independent_step  2  enter_sdk  ${pam4_400g_32_config}
	independent_step  3  run_loopback_traffic_for_innovium  ${port_num_pam4_400g}  ${rate_num_config["${pam4_400g_32_config}"][0]}  test_time=600
	Step  4  exit_sdk
    [Teardown]  OS Disconnect Device


switch_port_speed_check
    [Documentation]  check switch port  default status and speed. 
    [Tags]  switch_port_speed_check  SilverstoneX  CLSWB-SITG-QSFP-0003-0001  
    [Setup]  OS Connect Device
	Step  1  setroot  DUT
	independent_step  2  enter_sdk  ${pam4_400g_32_config}  
	independent_step  3  check_port_default_status  ${port_num_pam4_400g}  ${rate_num_config["${pam4_400g_32_config}"][0]}
	Step  4  exit_sdk  
    [Teardown]  OS Disconnect Device
	

switch_port_link_speed_check_by_full_test
    [Documentation]  Check all the lan port speed is same and could meet the max speed.
    [Tags]  switch_port_link_speed_check_by_full_test  SilverstoneX  CLSWB-SITG-LANT-0005-0001  
    [Setup]  OS Connect Device
	Step  1  setroot  DUT
	independent_step  2  enter_sdk  ${pam4_400g_32_config}  
	independent_step  3  check_link_speed_by_full_test  ${port_num_pam4_400g}  ${rate_num_config["${pam4_400g_32_config}"][0]}
	Step  4  exit_sdk  
    [Teardown]  OS Disconnect Device


loopback_pam4_400g_traffic_test
    [Documentation]  check switch port  whether no packet loss during the testing
    [Tags]  loopback_pam4_400g_traffic_test  SilverstoneX  CLSWB-SITG-COMP-0025-0001  SDK
    [Setup]  OS Connect Device
	Step  1  setroot  DUT
	independent_step  2  enter_sdk  ${pam4_400g_32_config}  
	independent_step  3  run_loopback_traffic_for_innovium  ${port_num_pam4_400g}  ${rate_num_config["${pam4_400g_32_config}"][0]}
	Step  4  exit_sdk  
    [Teardown]  OS Disconnect Device


loopback_pam4_200g_traffic_test
    [Documentation]  check switch port  whether no packet loss during the testing
    [Tags]  loopback_pam4_200g_traffic_test  SilverstoneX  CLSWB-SITG-COMP-0025-0001  SDK
    [Setup]  OS Connect Device
	Step  1  setroot  DUT
	independent_step  2  enter_sdk  ${pam4_200g_64_config}  
	independent_step  3  run_loopback_traffic_for_innovium  ${port_num_pam4_200g}  ${rate_num_config["${pam4_200g_64_config}"][0]}
	Step  4  exit_sdk  
    [Teardown]  OS Disconnect Device
	

loopback_pam4_100g_traffic_test
    [Documentation]  check switch port  whether no packet loss during the testing
    [Tags]  loopback_pam4_100g_traffic_test  SilverstoneX  CLSWB-SITG-COMP-0025-0001  SDK
    [Setup]  OS Connect Device
	Step  1  setroot  DUT
	independent_step  2  enter_sdk  ${pam4_100g_128_config}  
	independent_step  3  run_loopback_traffic_for_innovium  ${port_num_pam4_100g}  ${rate_num_config["${pam4_100g_128_config}"][0]}
	Step  4  exit_sdk  
    [Teardown]  OS Disconnect Device
	

loopback_nrz_200g_traffic_test
    [Documentation]  check switch port  whether no packet loss during the testing
    [Tags]  loopback_nrz_200g_traffic_test  SilverstoneX  CLSWB-SITG-COMP-0025-0001  SDK
    [Setup]  OS Connect Device
	Step  1  setroot  DUT
	independent_step  2  enter_sdk  ${nrz_200g_32_config}  
	independent_step  3  run_loopback_traffic_for_innovium  ${port_num_nrz_200g}  ${rate_num_config["${nrz_200g_32_config}"][0]}
	Step  4  exit_sdk  
    [Teardown]  OS Disconnect Device
	

loopback_nrz_100g_traffic_test
    [Documentation]  check switch port  whether no packet loss during the testing
    [Tags]  loopback_nrz_100g_traffic_test  SilverstoneX  CLSWB-SITG-COMP-0025-0001  SDK
    [Setup]  OS Connect Device
	Step  1  setroot  DUT
	independent_step  2  enter_sdk  ${nrz_100g_64_config}  
	independent_step  3  run_loopback_traffic_for_innovium  ${port_num_nrz_100g}  ${rate_num_config["${nrz_100g_64_config}"][0]}
	Step  4  exit_sdk  
    [Teardown]  OS Disconnect Device


loopback_nrz_50g_traffic_test
    [Documentation]  check switch port  whether no packet loss during the testing
    [Tags]  loopback_nrz_50g_traffic_test  SilverstoneX  CLSWB-SITG-COMP-0025-0001  SDK
    [Setup]  OS Connect Device
	Step  1  setroot  DUT
	independent_step  2  enter_sdk  ${nrz_50g_128_config}  
	independent_step  3  run_loopback_traffic_for_innovium  ${port_num_nrz_50g}  ${rate_num_config["${nrz_50g_128_config}"][0]}
	Step  4  exit_sdk  
    [Teardown]  OS Disconnect Device


loopback_nrz_40g_traffic_test
    [Documentation]  check switch port  whether no packet loss during the testing
    [Tags]  loopback_nrz_40g_traffic_test  SilverstoneX  CLSWB-SITG-COMP-0025-0001  SDK
    [Setup]  OS Connect Device
	Step  1  setroot  DUT
	independent_step  2  enter_sdk  ${nrz_40g_64_config}  
	independent_step  3  run_loopback_traffic_for_innovium  ${port_num_nrz_40g}  ${rate_num_config["${nrz_40g_64_config}"][0]}
	Step  4  exit_sdk  
    [Teardown]  OS Disconnect Device


loopback_nrz_25g_traffic_test
    [Documentation]  check switch port  whether no packet loss during the testing
    [Tags]  loopback_nrz_25g_traffic_test  SilverstoneX  CLSWB-SITG-COMP-0025-0001  SDK
    [Setup]  OS Connect Device
	Step  1  setroot  DUT
	independent_step  2  enter_sdk  ${nrz_25g_128_config}  
	independent_step  3  run_loopback_traffic_for_innovium  ${port_num_nrz_25g}  ${rate_num_config["${nrz_25g_128_config}"][0]}
	Step  4  exit_sdk  
    [Teardown]  OS Disconnect Device
	

loopback_nrz_10g_traffic_test
    [Documentation]  check switch port  whether no packet loss during the testing
    [Tags]  loopback_nrz_10g_traffic_test  SilverstoneX  CLSWB-SITG-COMP-0025-0001  SDK
    [Setup]  OS Connect Device
	Step  1  setroot  DUT
	independent_step  2  enter_sdk  ${nrz_10g_128_config}  
	independent_step  3  run_loopback_traffic_for_innovium  ${port_num_nrz_10g}  ${rate_num_config["${nrz_10g_128_config}"][0]}
	Step  4  exit_sdk  
    [Teardown]  OS Disconnect Device

	
loopback_info_check
    [Documentation]  The information of Loopback should be correctly detected and reported by system
    [Tags]  loopback_info_check  SilverstoneX  CLSWB-SITG-COMP-0016-0001
    [Setup]  OS Connect Device
	Step  1  setroot  DUT
	Step  2  loopback_info_check  ${loopback_num}  ${qsfp_vendor}  ${qsfp_pn}
    [Teardown]  OS Disconnect Device


daccable_pam4_400G_snake_traffic_test
	[Documentation]  check switch port  whether no packet loss during the testing
    [Tags]  daccable_pam4_400G_snake_traffic_test  SilverstoneX  CLSWB-SITG-COMP-0038-0001  SDK_DAC_Cable  
    [Setup]  OS Connect Device
	Step  1  setroot  DUT
	independent_step  2  enter_sdk  ${pam4_400g_32_config}  
	independent_step  3  run_dac_cable_traffic_for_innovium  ${port_num_pam4_400g}  ${rate_num_config["${pam4_400g_32_config}"][0]}  str_num=${rate_num_config["${pam4_400g_32_config}"][1]}
	Step  4  exit_sdk  
    [Teardown]  OS Disconnect Device


optical_module_pam4_400G_snake_traffic_test
	[Documentation]  check switch port  whether no packet loss during the testing
    [Tags]  optical_module_pam4_400G_snake_traffic_test  SilverstoneX  CLSWB-SITG-COMP-0012-0001 
    [Setup]  OS Connect Device
	Step  1  setroot  DUT
	independent_step  2  enter_sdk  ${pam4_400g_32_config}  
	independent_step  3  run_dac_cable_traffic_for_innovium  ${port_num_pam4_400g}  ${rate_num_config["${pam4_400g_32_config}"][0]}  str_num=${rate_num_config["${pam4_400g_32_config}"][1]}
	Step  4  exit_sdk  
    [Teardown]  OS Disconnect Device
	
	
daccable_pam4_200G_snake_traffic_test
	[Documentation]  check switch port  whether no packet loss during the testing
    [Tags]  daccable_pam4_200G_snake_traffic_test  SilverstoneX  CLSWB-SITG-COMP-0039-0001  SDK_DAC_Cable  
    [Setup]  OS Connect Device
	Step  1  setroot  DUT
	independent_step  2  enter_sdk  ${pam4_200g_64_config}  
	independent_step  3  run_dac_cable_traffic_for_innovium  ${port_num_pam4_200g}  ${rate_num_config["${pam4_200g_64_config}"][0]}  str_num=${rate_num_config["${pam4_200g_64_config}"][1]}
	Step  4  exit_sdk  
    [Teardown]  OS Disconnect Device


daccable_pam4_100G_snake_traffic_test
	[Documentation]  check switch port  whether no packet loss during the testing
    [Tags]  daccable_pam4_100G_snake_traffic_test  SilverstoneX  CLSWB-SITG-COMP-0040-0001  SDK_DAC_Cable  
    [Setup]  OS Connect Device
	Step  1  setroot  DUT
	independent_step  2  enter_sdk  ${pam4_100g_128_config}  
	independent_step  3  run_dac_cable_traffic_for_innovium  ${port_num_pam4_100g}  ${rate_num_config["${pam4_100g_128_config}"][0]}  str_num=${rate_num_config["${pam4_100g_128_config}"][1]}
	Step  4  exit_sdk  
    [Teardown]  OS Disconnect Device
	

daccable_nrz_200G_snake_traffic_test
	[Documentation]  check switch port  whether no packet loss during the testing
    [Tags]  daccable_nrz_200G_snake_traffic_test  SilverstoneX  CLSWB-SITG-COMP-0039-0001  SDK_DAC_Cable  
    [Setup]  OS Connect Device
	Step  1  setroot  DUT
	independent_step  2  enter_sdk  ${nrz_200g_32_config}  
	independent_step  3  run_dac_cable_traffic_for_innovium  ${port_num_nrz_200g}  ${rate_num_config["${nrz_200g_32_config}"][0]}  str_num=${rate_num_config["${nrz_200g_32_config}"][1]}
	Step  4  exit_sdk  
    [Teardown]  OS Disconnect Device


daccable_nrz_100G_snake_traffic_test
	[Documentation]  check switch port  whether no packet loss during the testing
    [Tags]  daccable_nrz_100G_snake_traffic_test  SilverstoneX  CLSWB-SITG-COMP-0040-0001  SDK_DAC_Cable  
    [Setup]  OS Connect Device
	Step  1  setroot  DUT
	independent_step  2  enter_sdk  ${nrz_100g_64_config}  
	independent_step  3  run_dac_cable_traffic_for_innovium  ${port_num_nrz_100g}  ${rate_num_config["${nrz_100g_64_config}"][0]}  str_num=${rate_num_config["${nrz_100g_64_config}"][1]}
	Step  4  exit_sdk  
    [Teardown]  OS Disconnect Device


daccable_nrz_50G_snake_traffic_test
	[Documentation]  check switch port  whether no packet loss during the testing
    [Tags]  daccable_nrz_50G_snake_traffic_test  SilverstoneX  CLSWB-SITG-COMP-0040-0001  SDK_DAC_Cable  
    [Setup]  OS Connect Device
	Step  1  setroot  DUT
	independent_step  2  enter_sdk  ${nrz_50g_128_config}  
	independent_step  3  run_dac_cable_traffic_for_innovium  ${port_num_nrz_50g}  ${rate_num_config["${nrz_50g_128_config}"][0]}  str_num=${rate_num_config["${nrz_50g_128_config}"][1]}
	Step  4  exit_sdk  
    [Teardown]  OS Disconnect Device


daccable_nrz_40G_snake_traffic_test
	[Documentation]  check switch port  whether no packet loss during the testing
    [Tags]  daccable_nrz_40G_snake_traffic_test  SilverstoneX  CLSWB-SITG-COMP-0040-0001  SDK_DAC_Cable  
    [Setup]  OS Connect Device
	Step  1  setroot  DUT
	independent_step  2  enter_sdk  ${nrz_40g_64_config}  
	independent_step  3  run_dac_cable_traffic_for_innovium  ${port_num_nrz_40g}  ${rate_num_config["${nrz_40g_64_config}"][0]}  str_num=${rate_num_config["${nrz_40g_64_config}"][1]}
	Step  4  exit_sdk  
    [Teardown]  OS Disconnect Device
	
	
daccable_nrz_25G_snake_traffic_test
	[Documentation]  check switch port  whether no packet loss during the testing
    [Tags]  daccable_nrz_25G_snake_traffic_test  SilverstoneX  CLSWB-SITG-COMP-0040-0001  SDK_DAC_Cable  
    [Setup]  OS Connect Device
	Step  1  setroot  DUT
	independent_step  2  enter_sdk  ${nrz_25g_128_config}  
	independent_step  3  run_dac_cable_traffic_for_innovium  ${port_num_nrz_25g}  ${rate_num_config["${nrz_25g_128_config}"][0]}  str_num=${rate_num_config["${nrz_25g_128_config}"][1]}
	Step  4  exit_sdk  
    [Teardown]  OS Disconnect Device


daccable_nrz_10G_snake_traffic_test
	[Documentation]  check switch port  whether no packet loss during the testing
    [Tags]  daccable_nrz_10G_snake_traffic_test  SilverstoneX  CLSWB-SITG-COMP-0040-0001  SDK_DAC_Cable  
    [Setup]  OS Connect Device
	Step  1  setroot  DUT
	independent_step  2  enter_sdk  ${nrz_10g_128_config}  
	independent_step  3  run_dac_cable_traffic_for_innovium  ${port_num_nrz_10g}  ${rate_num_config["${nrz_10g_128_config}"][0]}  str_num=${rate_num_config["${nrz_10g_128_config}"][1]}
	Step  4  exit_sdk  
    [Teardown]  OS Disconnect Device
	

i2c_stress_use_diag
	[Documentation]  check switch port  whether no packet loss during the testing
    [Tags]  i2c_stress_use_diag  SilverstoneX  CLSWB-SITG-COMP-0040-0001  SDK_DAC_Cable  
    [Setup]  OS Connect Device
	Step  1  setroot  DUT
	independent_step  2  check_log_info
	independent_step  3  i2c_diag_stress
	independent_step  4  check_log_info 
    [Teardown]  OS Disconnect Device	


memtester_diagnostic_package
	[Documentation]  check switch port  whether no packet loss during the testing
    [Tags]  memtester_diagnostic_package  SilverstoneX  CLSWB-SITG-DMT1-0002-0001
    [Setup]  OS Connect Device
	Step  1  RunOrKillMemtester  False
    Step  2  CopyFileToPC
    Step  3  CopyFileToPC  ${dut_file_path}/log  .txt
    Step  4  CheckMemtesterLog
    [Teardown]  OS Disconnect Device
	
	
########################################## Janson END ##############################################################

dac_info_check
    [Documentation]  The information of dac cable should be correctly detected and reported by system
    [Tags]  dac_info_check  SilverstoneX  CLSWB-SITG-COMP-0026-0001  SDK
    [Setup]  OS Connect Device
	Step  1  setroot  DUT
	Step  2  loopback_info_check  ${dac_num}  ${dac_qsfp_vendor}  ${dac_qsfp_pn}
    [Teardown]  OS Disconnect Device


Optical_module_info_check
    [Documentation]  The information of optical module should be correctly detected and reported by system
    [Tags]  Optical_module_info_check  SilverstoneX  CLSWB-SITG-COMP-0001-0001  SDK
    [Setup]  OS Connect Device
	Step  1  setroot  DUT
	Step  2  loopback_info_check  ${module_num}  ${module_qsfp_vendor}  ${module_qsfp_pn}
    [Teardown]  OS Disconnect Device


Optical_module_pam4_400G_snake_traffic_test
	[Documentation]  check switch port  whether no packet loss during the testing
    [Tags]  Optical_module_pam4_400G_snake_traffic_test  SilverstoneX  CLSWB-SITG-COMP-0012-0001  SDK_DAC_Cable  
    [Setup]  OS Connect Device
	Step  1  setroot  DUT
	independent_step  2  enter_sdk  ${pam4_400g_32_config}  
	independent_step  3  run_dac_cable_traffic_for_innovium  ${port_num_pam4_400g}  ${rate_num_config["${pam4_400g_32_config}"][0]}  test_time=120  str_num=${rate_num_config["${pam4_400g_32_config}"][1]}
	Step  4  exit_sdk  
    [Teardown]  OS Disconnect Device


1G_port_DHCP_function_test
    [Documentation]  check the RJ45 Management port DHCP function
    [Tags]  1G_port_DHCP_function_test  SilverstoneX  CLSWB-SITG-LANT-0002-0001  
    [Setup]  OS Connect Device
	Step  1  setroot  DUT
	Step  2  set_os_ip_by_dhclient  DUT
	Step  3  ping_to_pc  DUT  600
    [Teardown]  OS Disconnect Device


1G_port_static_function_test
    [Documentation]  check the RJ45 Management port static IP function
    [Tags]  1G_port_static_function_test  SilverstoneX  CLSWB-SITG-LANT-0001-0001  
    [Setup]  OS Connect Device
	Step  1  setroot  DUT
	Step  2  set_static_ip  DUT
	Step  3  ping_to_pc  DUT  600
    [Teardown]  OS Disconnect Device