###############################################################################
# LEGALESE:   "Copyright (C) 2020-      Celestica Corp. All rights reserved." #
#                                                                             #
# This source code is confidential, proprietary, and contains trade           #
# secrets that are the sole property of Celestica Corp.                       #
# Copy and/or distribution of this source code or disassembly or reverse      #
# engineering of the resultant object code are strictly forbidden without     #
# the written consent of Celestica Corp.                                      #
#                                                                             #
###############################################################################

*** Settings ***
Documentation   Juniper common diagnostic suite
Resource        CommonKeywords.resource
Variables       lagavulin/JuniperDiagLagavulinVariablesLatest.py
#Resource        JuniperCommonKeywords.resource
#Resource        JuniperDiagKeywords.resource
Library         JuniperDiagLib.py
Library         CommonLib.py
Library         ../JuniperCommonLib.py

Suite Setup     DiagOS Connect Device
Suite Teardown  DiagOS Disconnect Device

*** Test Cases ***
LAGA_DIAG_13.1_Diag_Tool_Update
   [Documentation]   The purpose of this test is to check if the Diag tool can be updated successfully.
   [Tags]  LAGA_DIAG_13.1_Diag_Tool_Update  lagavulin  
   [Timeout]  25 mins 00 seconds
   #${old_image} =  get sw image  old
   #${new_image} =  get sw image
   Step  1  copy diag image tool
   Step  2  updatedeviceimage  ${diag_old_image}
   Step  3  updatedeviceimage  ${diag_new_image}

LAGA_DIAG_9.1_CPU_Information_Test
     [Documentation]  To test CPU Information
     [Tags]  LAGA_DIAG_9.1_CPU_Information_Test  lagavulin  
     Step  1  verify diag tool path
     Step  2  Check help info
     Step  3  Check the list of config info
     Step  4  Check the tool version
     Step  5  Read and write Register Operation
     Step  6  Auto check the CPU info
     Step  7  cpu linux command

LAGA_DIAG_9.2_Memory_Test
     [Documentation]  Memory Test
     [Tags]  LAGA_DIAG_9.2_Memory_Test  lagavulin  
     Step  1  verify diag tool path
     Step  2  Memory help info
     Step  3  Memory tool version
     Step  4  Read write data width and count
     Step  5  Auto check the memory info
     Step  6  Memory linux cmd

LAGA_DIAG_9.4_Mgmt_Ether_Port_MAC_Check_Test
     [Documentation]  Mgmt Ether Port MAC Check Test
     [Tags]  LAGA_DIAG_9.4_Mgmt_Ether_Port_MAC_Check_Test  lagavulin 
     Step  1  verify tool path
     Step  2  Verify I210 adapter
     Step  3  Default MAC addr
     Step  4  Modify Mac Addr

LAGA_DIAG_9.6_TPM_Test
     [Documentation]  TPM Test
     [Tags]  LAGA_DIAG_9.6_TPM_Test  lagavulin 
     Step  1  verify diag tool path
     Step  2  tpm help parameter
     Step  3  tpm list parameter
     Step  4  tpm all parameter
     
LAGA_DIAG_10.2_PCIe_Devices_Test
     [Documentation]  PCIe device test
     [Tags]  LAGA_DIAG_10.2_PCIe_Devices_Test  lagavulin  
     Step  1  verify diag tool path
     Step  2  pci help parameter
     Step  3  pci all parameter
     Step  4  pci version parameter
     Step  5  pci list parameter
     Step  6  pci linux command
     Step  7  pci read write operation

LAGA_DIAG_10.1_I2C_Device_Test
     [Documentation]  I2C Device Test
     [Tags]  LAGA_DIAG_10.1_I2C_Device_Test  lagavulin
     Step  1  verify diag tool path
     Step  2  i2c list parameter
     Step  3  i2c scan parameter  ${scan_pattern}
     Step  4  i2c all parameter
     Step  5  i2c scan bus parameter  ${single_scan_bus_pattern}
     Step  6  i2c dump test parameter  ${dump_test_pattern}
     Step  7  i2c detect parameter  ${i2c_detect_pattern}  
     Step  8  i2c read write parameter
      

LAGA_DIAG_9.5_Mgmt_Ether_Port_Connect_Test
     [Documentation]  Mgmt Ether Port Connect Test
     [Tags]  LAGA_DIAG_9.5_Mgmt_Ether_Port_Connect_Test  lagavulin  
     Step  1  verify diag tool path
     Step  2  eth help parameter
     Step  3  eth version parameter
     Step  4  check remote pc connected
     Step  5  eth speed parameter

LAGA_DIAG_10.5_CPLD_Access_Test
     [Documentation]  CPLD Acces test
     [Tags]  LAGA_DIAG_10.5_CPLD_Access_Test  lagavulin 
     Step  1  verify diag tool path
     Step  2  cpld help parameter
     Step  3  cpld list parameter
     Step  4  cpld version parameter
     Step  5  cpld all parameter
     Step  6  cpld read write data by register address
     Step  7  cpld read write data by register id

LAGA_DIAG_11.2_RTC_and_Battery_Test
     [Documentation]  RTc and Battery test
     [Tags]  LAGA_DIAG_11.2_RTC_and_Battery_Test  lagavulin 
     Step  1  verify diag tool path
     Step  2  rtc help parameter
     Step  3  rtc version parameter
     Step  4  set and read rtc time

LAGA_DIAG_11.6_Power_Monitor_Test
     [Documentation]  Power Monitor Test
     [Tags]  LAGA_DIAG_11.6_Power_Monitor_Test  lagavulin 
     Step  1  verify diag tool path
     Step  2  Pwmon help parameter
     Step  3  Pwmon version parameter
     Step  4  Pwmon list and all parameter
     Step  5  Pwmon set and get margin value
     Step  6  Pwmon read the Channel Voltage
	
LAGA_DIAG_11.14_Down_SFP_Test
     [Documentation]  Down SFP Test
     [Tags]  LAGA_DIAG_11.14_Down_SFP_Test  lagavulin 
     Step  1  Check DUT support SFP test
     Step  2  SFP tool path  
     Step  3  Down SFP test 

LAGA_DIAG_11.8_Firmware/Software_Information_Test 
     [Documentation]  Firmware/Software Information Test
     [Tags]  LAGA_DIAG_11.8_Firmware/Software_Information_Test  lagavulin  
     Step  1  verify diag tool path
     Step  2  version help parameter
     Step  3  version parameter
     Step  4  version show parameter
     Step  5  OS version

LAGA_DIAG_11.22_LPC_Access_Test
     [Documentation]  LPC Access Test
     [Tags]  LAGA_DIAG_11.22_LPC_Access_Test  lagavulin  
     Step  1  verify diag tool path
     Step  2  lpc help parameter
     Step  3  lpc read write operation 

LAGA_DIAG_11.21_Check_The_Reset_Reason_Test
     [Documentation]  Check the Reset Reason Test
     [Tags]  LAGA_DIAG_11.21_Check_The_Reset_Reason_Test  lagavulin  
     Step  1  verify diag tool path
     Step  2  reset help parameter
     Step  3  reset version parameter
     Step  4  reset list parameter
     Step  5  reset read parameter
     Step  6  reset set parameter

LAGA_DIAG_11.25_SI_USB_Controller_Test
     [Documentation]  SI USB Controller Test
     [Tags]  LAGA_DIAG_11.25_SI_USB_Controller_Test  lagavulin  
     Step  1  verify tool path
     Step  2  enable relax security
     Step  3  get and set USB register value
     Step  4  disable relax security

LAGA_DIAG_11.26_SI_SMBus_Controller_Test
     [Documentation]  SI SMBus Controller Test
     [Tags]  LAGA_DIAG_11.26_SI_SMBus_Controller_Test  lagavulin  
     Step  1  verify tool path
     Step  2  get and set SMBus clk value

LAGA_DIAG_11.27_SI_Sata_Controller_Test
     [Documentation]  SI Sata Controller Test
     [Tags]  LAGA_DIAG_11.27_SI_Sata_Controller_Test  lagavulin  
     Step  1  verify tool path
     Step  2  enable relax security
     Step  3  set and read sata3 dword6 register value
     Step  4  disable relax security

LAGA_DIAG_11.10_Module_FAN_Speed_SAT_stages_Test
     [Documentation]   Module FAN Speed SAT stages Test
     [Tags]   LAGA_DIAG_11.10_Module_FAN_Speed_SAT_stages_Test  lagavulin  
     [Timeout]  15 min 00 seconds
     Step  1  verify diag tool path
     Step  2  set fan speed  50  50  49


LAGA_DIAG_11.11_Module_FAN_Speed_RIT/ORT_stages_Test
     [Documentation]   Module FAN Speed RIT/ORT stages Test
     [Tags]  LAGA_DIAG_11.11_Module_FAN_Speed_RIT/ORT_stages_Test  lagavulin   
     [Timeout]  15 min 00 seconds
     Step  1  verify diag tool path
     Step  2  set fan speed  100  100  100

LAGA_DIAG_11.24_Cards_information_Test
     [Documentation]  The purpose of this test is to check the Card type is 24T/24P/48T/48P/48F and uplink card is 10G/25G mode.
     [Tags]  LAGA_DIAG_11.24_Cards_information_Test  lagavulin 
     [Timeout]  5 min 00 seconds
     Step  1  verify diag tool path
     Step  2  check card help
     Step  3  check card test
     Step  4  check type and mode

LAGA_DIAG_1.3.36_TPM_Manufacture_Test
     [Documentation]  TPM Manufacture Test
     [Tags]  LAGA_DIAG_1.3.36_TPM_Manufacture_Test  lagavulin
     Step  1  verify diag tool path
     Step  2  run Tpm Manufacture Test

LAGA_DIAG_13.2_System_CPLD_Update
     [Documentation]  System CPLD Update Test
     [Tags]  LAGA_DIAG_13.2_System_CPLD_Update  lagavulin
     Step  1  verify diag tool path
#     Step  2  downgrade Upgrade System Cpld Version  ${sys_cpld_vme_image_old}  Downgrading
#     Step  3  downgrade Upgrade System Cpld Version  ${sys_cpld_vme_image_new}

LAGA_DIAG_15.6_DDR_stress_test
    [Documentation]  The purpose of this test is to check DDR stress test.
    [Timeout]  43500 mins 00 seconds
    [Tags]  LAGA_DIAG_15.6_DDR_stress_test  lagavulin
    Step  1  check ddr test

LAGA_DIAG_11.28_DDR_ECC_Test
     [Documentation]  DDR ECC Test
     [Tags]  LAGA_DIAG_11.28_DDR_ECC_Test  lagavulin  
     Step  1  verify diag tool path
     Step  2  ecc help parameter
     Step  3  ecc version parameter
     Step  4  ecc list parameter
     Step  5  ecc status parameter

LAGA_DIAG_11.29_Margin_Test
     [Documentation]  Margin Test
     [Tags]  LAGA_DIAG_11.29_Margin_Test   lagavulin  
     Step  1  verify diag tool path
     Step  2  margin help parameter
     Step  3  set margin function

LAGA_DIAG_11.16_Temperature_Sensor_Test
    [Documentation]  This test is to check the value of this sensor is in the reasonable range HW defines
    [Tags]  LAGA_DIAG_11.16_Temperature_Sensor_Test  lagavulin  
    [Timeout]  5 min 00 seconds
    Step  1  Verify Diag Tool Path
    Step  2  Check help information tool
    Step  3  Verify the Tool Version  ${TempToolVersion_cmd1}  ${TempToolVersion_cmd2}
    Step  4  Check Yaml information  ${yamlinfo_cmd1}  ${yamlinfo_cmd2}
    Step  5  Check the Temp values  ${TempValue_cmd1}  ${TempValue_cmd2}  ${yamlinfo_cmd1}
    Step  6  Check Auto Test run  ${Sensor_cmdlist}

LAGA_DIAG_13.4_I210_fw_Update
     [Documentation]  To check diag tool Firmware upgrade function
     [Tags]  LAGA_DIAG_13.4_I210_fw_Update  lagavulin
     Step  1  verify diag tool path
     Step  2  check I210 Update

LAGA_DIAG_13.7_Com-e_Card_Power_Monitor_Online_Update
   [Documentation]  The purpose of this test is to check diag tool Firmware upgrade function
   [Tags]  LAGA_DIAG_13.7_Com-e_Card_Power_Monitor_Online_Update  lagavulin   
   [Timeout]  20 mins 00 seconds
   Step  1  Verify Diag Tool Path
   Step  2  check firmware version  ${firmware_version}
   Step  3  update pwmon firmware   ${firmware_update}
   Step  4  check firmware version  ${firmware_version}

LAGA_DIAG_11.30_Boot_from_Golden_BIOS_Test
     [Documentation]  Boot from Golden BIOS Test
     [Tags]  LAGA_DIAG_11.30_Boot_from_Golden_BIOS_Test  lagavulin  
     Step  1  verify diag tool path
     Step  2  cpld help parameter
     Step  3  cpld list parameter
     Step  4  cpld version parameter
     Step  5  write cpld register and boot Golden bios 

LAGA_DIAG_11.31_EMMC_Test
     [Documentation]  EMMC Test
     [Tags]  LAGA_DIAG_11.31_EMMC_Test  lagavulin  
     Step  1  verify diag tool path
     Step  2  emmc help parameter
     Step  3  emmc list parameter
     Step  4  emmc version parameter
     Step  5  emmc info paramater
     Step  6  emmc all linux info parameter

LAGA_DIAG_12.2_Uplink_module_EEPROM_Test
     [Documentation]  To check diag tool if will program the whole file into the eeprom
     [Tags]  LAGA_DIAG_12.2_Uplink_module_EEPROM_Test  lagavulin
     Step  1  verify diag tool path
     Step  2  check Help With Cmd And Pattern  ${module_eeprom_help_cmd}  ${module_eeprom_help_pattern}
     Step  3  execute Eeprom Test

LAGA_DIAG_11.32_EMMC_FW_Revision_Check_Test
     [Documentation]  EMMC FW Revision Check Test
     [Tags]  LAGA_DIAG_11.32_EMMC_FW_Revision_Check_Test  lagavulin  
     Step  1  verify tool path
     Step  2  emmc info 
     Step  3  emmc FW revision

LAGA_DIAG_15.1_Disk_stress_test_SSD_USB
     [Documentation]  Disk stress test SSD USB
     [Tags]  LAGA_DIAG_15.1_Disk_stress_test_SSD_USB  lagavulin  
     Step  1  verify tool path
     Step  2  check device type
     Step  3  FIO stress test and log verification  ${stress_time}  ${timeout}

LAGA_DIAG_14.1_PoE_Firmware_Update
     [Documentation]  PoE Firmware update
     [Tags]  LAGA_DIAG_14.1_PoE_Firmware_Update  lagavulin
     Step  1  verify Diag Tool Path
     Step  2  check Help With Cmd And Pattern  ${poe_firmware_help_cmd}  ${poe_firmware_help_pattern}
     Step  3  poe Firmware Update

LAGA_DIAG_15.2_PCIe_Bus_stress_test
   [Documentation]  The purpose of this test is to check access the PCIe device continually test.
   [Tags]  LAGA_DIAG_15.2_PCIe_Bus_stress_test  lagavulin
   [Timeout]  250 mins 00 seconds
   ${Current_Loop}  Evaluate  100-1
   FOR    ${INDEX}    IN RANGE    1   100
      #Print Loop Info  ${INDEX}  ${Current_Loop}
      Step  1  verify sdk path
      Step  2  check pcie operation
   END

LAGA_DIAG_11.9_Fan_Speed_Test
    [Documentation]  The purpose of this test is to check two types of fan controller, EMC2305 and PSU fan.
    [Tags]  LAGA_DIAG_11.9_Fan_Speed_Test  lagavulin  test12
    [Timeout]  15 min 00 seconds
    Step  1  verify diag tool path
    Step  2  check fan test
    Step  3  check dcdc version  ${fanmod}   ${fanver}
    Step  4  check fan list
    Step  5  check fan operations
    Step  6  check fan status
    Step  6  fan led status
    Step  7  check fan all
    Step  8  check fan speed  10
    Step  9  check fan speed  50
    Step  10  check fan speed  100  yes

#All preconditions are not met, need all before runnning
LAGA_DIAG_15.7_Warm_Boot_stress_test
   [Documentation]  The purpose of this test is to check device reboot test.
   [Tags]  LAGA_DIAG_15.7_Warm_Boot_stress_test  lagavulin
   [Timeout]  250 mins 00 seconds
   ${Current_Loop}  Evaluate  10-1
   FOR    ${INDEX}    IN RANGE    1   10

      Step  1   Verify Diag Tool Path
#      Step  2   warm reboot test
   END

LAGA_DIAG_16.2_FCT_Test_10G_and_25G_uplink_card
     [Documentation]  To test FCT - 10G and 25G uplink card
     [Tags]  LAGA_DIAG_16.2_FCT_Test_10G_and_25G_uplink_card  lagavulin
     Step  1  verify diag tool path
     #Step  2  temp Sensor Test
     Step  3  Led Test 10G_25G
     Step  4  run Eeprom Test
     Step  5  SFP Test
     Step  6  margin Test

LAGA_DIAG_13.3_CPU_CPLD_Update
     [Documentation]  To check diag tool Firmware upgrade function
     [Tags]  LAGA_DIAG_13.3_CPU_CPLD_Update  lagavulin
     Step  1  verify diag tool path
#     Step  2  upgrade downgrade cpu cpld version  ${cpu_cpld_old_bin}  downgrading
#     Step  3  upgrade downgrade cpu cpld version  ${cpu_cpld_new_bin}

LAGA_DIAG_13.6_Switch_Card_Power_Monitor_Online_Update
     [Documentation]  To check diag tool Firmware upgrade function
     [Tags]  LAGA_DIAG_13.6_Switch_Card_Power_Monitor_Online_Update  lagavulin
     Step  1  verify diag tool path
     Step  2  check Switch Card Help
     Step  3  check Switch Card Version
#     Step  4  update Image By Pwon

LAGA_DIAG_13.8_eMMC_FFU
     [Documentation]  To check eMMC FFU upgrade function
     [Tags]  LAGA_DIAG_13.8_eMMC_FFU  lagavulin
     Step  1  verify diag tool path
#     Step  2  upgrade Emmc Ffu

LAGA_DIAG_11.33_Fly_back_cable_Voltage_drop_Test
     [Documentation]  To check fly back cable Voltage drop should be correct.
     [Tags]  LAGA_DIAG_11.33_Fly_back_cable_Voltage_drop_Test  lagavulin
     Step  1  verify diag tool path
#     Step  2  execute Cable Voltage Drop Test

LAGA_DIAG_11.7_DC/DC_Controller_Access_Test
     [Documentation]  The purpose of this test is to check the diagnostic tool can check the voltage, current of DC/DC controller is in the reasonable region through the PMBus protocol.
     [Tags]  LAGA_DIAG_11.7_DC/DC_Controller_Access_Test  lagavulin
     [Timeout]  15 min 00 seconds
     Step  1  verify diag tool path
     Step  2  dcdc help info
     Step  3  list the config yaml
     Step  4  check dcdc version  ${dcdcmod}   ${dcdcver}
     Step  5  check dcdc voltage
     Step  7  dcdc test all
#     Step  8  set avs voltage  s  ${volt}
#     Step  9  set avs voltage  c  ${volt}

LAGA_DIAG_11.20_FRU_EEPROM_Test
     [Documentation]   The purpose of this test is to check FRU eeprom
     [Tags]   LAGA_DIAG_11.20_11.20_FRU_EEPROM_Test  lagavulin
     [Timeout]  15 min 00 seconds
     Step  1  verify tool path
     Step  2  Check eeprom list
     Step  3  check set model
     Step  4  reset list
     Step  5  reset list   "yes"

LAGA_DIAG_15.3_Mgmt_Eth_Port_test
     [Documentation]   Management ethernet port stress test
     [Tags]  LAGA_DIAG_15.3_Mgmt_Eth_Port_test  lagavulin
     Step  1  iperf stress test




*** Keywords ***
DiagOS Connect Device
    DiagOSConnect

DiagOS Disconnect Device
    DiagOSDisconnect
