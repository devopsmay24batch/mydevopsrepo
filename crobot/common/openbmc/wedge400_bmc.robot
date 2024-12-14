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
# Script       : Openbmc_test.robot                                                                                   #
# Date         : January 20, 2020                                                                                    #
# Author       : Prapatsorn W. <pwisutti@celestica.com>                                                               #
# Description  : This script will validate openbmc                                                                    #
#                                                                                                                     #
# Script Revision Details:                                                                                            #
#   Initial Draft for openbmc testing                                                                                 #
#######################################################################################################################

*** Settings ***
Documentation       Tests to verify OpenBMC functions described in the OpenBMC function SPEC for the project Wedge400.

# Force Tags        openbmc
Library           OpenBmcLibAdapter.py
Library           openbmc_lib.py
Variables         Openbmc_variable.py
Resource          Openbmc_keywords.robot
Resource          CommonResource.robot

Suite Setup       Bmc Connect Device
Suite Teardown    Bmc Disconnect Device

** Variables ***
# It is recommended to use <{ScriptName}|{FeatureName}|{DomainName}_Variable> file for variable declaration with help of
# setting table. This section should keep blank.
#In extreme case if script requires variable then it should be defined in this table with documentaiton tag
${LoopCnt}        2000
${MaxLoopNum}     2001

*** Test Cases ***
# *** comment ***

BMC_COMM_TC_000_Online_Update_slave_BMC_and_diag
    [Documentation]  This test checks the BMC FW programming functions by updating the BMC FW in BMC OS
    [Tags]     common  BMC_COMM_TC_000_Online_Update_slave_BMC_and_diag  wedge400  critical
    [Timeout]  180 min 00 seconds
    [Setup]    prepare BMC and diag images
    Sub-Case  FB_BMC_COMM_TC_000_1  upgrade slave bmc and check version
    Sub-Case  FB_BMC_COMM_TC_000_2  install diag package and init diag

FB_BMC_COMM_TC_003_Online_Update_BMC_in_BMC_OS
    [Documentation]  This test checks the BMC FW programming functions by updating the BMC FW in BMC OS
    [Tags]     common  FB_BMC_COMM_TC_003_Online_Update_BMC_in_BMC_OS  wedge400  critical
    [Timeout]  150 min 00 seconds
    [Setup]    prepare BMC images
    Sub-Case  FB_BMC_COMM_TC_003_1  upgrade master bmc and check version
    Sub-Case  FB_BMC_COMM_TC_003_2  downgrade master bmc and check version
    Sub-Case  FB_BMC_COMM_TC_003_3  upgrade master bmc and check version
    [Teardown]  clean images  DUT  BMC

FB_BMC_COMM_TC_004_OpenBMC_Uart_Information_Check
    [Documentation]  This test checks BMC booting log after reboot
    [Tags]     common  FB_BMC_COMM_TC_004_OpenBMC_Uart_Information_Check  wedge400
    [Timeout]  20 min 00 seconds
    Sub-Case  FB_BMC_COMM_TC_004_1  Reboot OpenBMC three times and Check booting log

FB_BMC_COMM_TC_005_Online_Update_BIOS_in_BMC_OS
    [Documentation]  This test checks the BMC FW programming functions by updating the BIOS FW in BMC OS
    [Tags]     common  FB_BMC_COMM_TC_005_Online_Update_BIOS_in_BMC_OS  wedge400  critical
    [Timeout]  150 min 00 seconds
    [Setup]    prepare BIOS images
    Sub-Case  FB_BMC_COMM_TC_005_1  upgrade master bios and check version
	Sub-Case  FB_BMC_COMM_TC_005_2  upgrade slave bios and check version
	Sub-Case  FB_BMC_COMM_TC_005_3  switch to master bios
    [Teardown]  clean images  DUT  BIOS

FB_BMC_COMM_TC_006_Online_update_CPLD_in_BMC_OS
    [Documentation]  This test checks the BMC FW programming functions by updating the cpld in BMC OS
    [Tags]     common  FB_BMC_COMM_TC_006_Online_update_CPLD_in_BMC_OS  wedge400  critical
    [Timeout]  150 min 00 seconds
    [Setup]    prepare images  CPLD
    Sub-Case  FB_BMC_COM_TC_006_1  CPLD upgrade and check CPLD version
    Sub-Case  FB_BMC_COM_TC_006_2  CPLD downgrade and check CPLD version
    Sub-Case  FB_BMC_COM_TC_006_3  CPLD upgrade and check CPLD version
    [Teardown]  clean images  DUT  CPLD

FB_BMC_COMM_TC_007_Online_Update_BIC_Bridge_in_BMC_OS
    [Documentation]  This test checks the BMC FW programming functions by updating the BIC FW in BMC OS
    [Tags]     common  FB_BMC_COMM_TC_007_Online_Update_BIC_Bridge_in_BMC_OS  wedge400  critical
    [Timeout]  40 min 00 seconds
    [Setup]    prepare images  BIC
    Sub-Case  FB_BMC_COMM_TC_007_1  upgrade bic and check version
	Sub-Case  FB_BMC_COMM_TC_007_2  downgrade bic and check version
    Sub-Case  FB_BMC_COMM_TC_007_3  upgrade bic and check version
    [Teardown]  clean images  DUT  BIC

FB_BMC_COMM_TC_008_BIC_Frequency_Auto_Set_Test
    [Documentation]  This test checks BIC Frequency auto set successfully in OpenBMC OS
    [Tags]     common  FB_BMC_COMM_TC_008_BIC_Frequency_Auto_Set_Test  wedge400
    [Timeout]  40 min 00 seconds
    Sub-Case  FB_BMC_COMM_TC_008_1  power cycle openbmc and check bic log

FB_BMC_COMM_TC_009_Online_Update_FPGA_In_BMC_OS
    [Documentation]  This test checks the BMC FW programming functions by updating the FPGA in BMC OS
    [Tags]     common  FB_BMC_COMM_TC_009_Online_Update_FPGA_In_BMC_OS  wedge400  critical
    [Timeout]  70 min 00 seconds
    [Setup]    prepare images  FPGA
    Sub-Case  FB_BMC_COMM_TC_009_1  FPGA upgrade and check FPGA version
    [Teardown]  clean images  DUT  FPGA

#FB_BMC_COMM_TC_010_Online_Update_OOB_Switch_FW_in_BMC_OS
#    [Documentation]  This test checks the BMC FW programming functions by updating the OOB Switch FW in BMC OS
#    [Tags]     common  FB_BMC_COMM_TC_010_Online_Update_OOB_Switch_FW_in_BMC_OS  wedge400
#    [Timeout]  15 min 00 seconds
#    [Setup]    prepare images  OOB
#    Sub-Case  FB_BMC_COMM_TC_010_1  run command to read and write OOB Switch eeprom
#    Sub-Case  FB_BMC_COMM_TC_010_2  ping dhcp server with eth0
#    [Teardown]  clean OOB images and dump files

FB_BMC_COMM_TC_011_Backup_BMC_Manual_Booting_Test
    [Documentation]  This test checks BMC can boot from slave by command
    [Tags]     common  FB_BMC_COMM_TC_011_Backup_BMC_Manual_Booting_Test  wedge400
    [Timeout]  25 min 00 seconds
    Sub-Case  FB_BMC_COMM_TC_011_1   check current openbmc is booted from master
    Sub-Case  FB_BMC_COMM_TC_011_2   switch bmc flash to Slave then to Master
    [Teardown]  switch bmc flash to Master

FB_BMC_COMM_TC_013_Backup_BIOS_Manual_Booting_Test
    [Documentation]  This test checks BIOS can boot from BIOS by command
    [Tags]     common  FB_BMC_COMM_TC_013_Backup_BIOS_Manual_Booting_Test  wedge400
    [Timeout]  45 min 00 seconds
    [Setup]  switch bios flash to Master
    Sub-Case  FB_BMC_COMM_TC_013_1  switch bios flash to Slave and check version in cpu
    Sub-Case  FB_BMC_COMM_TC_013_2  check slave bios version and switch bios flash to Master again
    [Teardown]  power cycle unit and check bios master mode

FB_BMC_COMM_TC_014_BMC_Network_Config_Test
    [Documentation]  This test checks BMC port could communicate with CPU and Terminal PC with IPv6
    [Tags]     common  FB_BMC_COMM_TC_014_BMC_Network_Config_Test  wedge400
    [Timeout]  10 min 00 seconds
    [Setup]  go to openbmc
    Sub-Case  FB_BMC_COMM_TC_014_1  reboot and check dhcp setting info and check ipv6 address
    Sub-Case  FB_BMC_COMM_TC_014_2  ping dhcp server with eth0
    Sub-Case  FB_BMC_COMM_TC_014_3  using scp command to copy file from BMC to CPU by eth0 ipv6
    [Teardown]  clean up file on both bmc and cpu

FB_BMC_COMM_TC_016_IPv6_Ping_Test
    [Documentation]  This test verifies if ping could be executed successfully
    [Tags]     common  FB_BMC_COMM_TC_016_IPv6_Ping_Test  wedge400
    [Timeout]  10 min 00 seconds
    Sub-Case  FB_BMC_COMM_TC_016_1  verify bmc ipv6 address
    Sub-Case  FB_BMC_COMM_TC_016_2  ping dhcp server with eth0
    Sub-Case  FB_BMC_COMM_TC_016_3  ping openbmc from dhcp server

FB_BMC_COMM_TC_017_IPv6_SSH_Test
    [Documentation]  This test verifies if SSH could be executed successfully
    [Tags]     common  FB_BMC_COMM_TC_017_IPv6_SSH_Test  wedge400
    [Timeout]  10 min 00 seconds
    Sub-Case  FB_BMC_COMM_TC_017_1  verify bmc ipv6 address
    Sub-Case  FB_BMC_COMM_TC_017_2  ssh dhcp server from openbmc
    Sub-Case  FB_BMC_COMM_TC_017_3  ssh openbmc from dhcp server

FB_BMC_COMM_TC_018_Internal_USB_Network_Check
    [Documentation]  This test checks the internal usb network between CPU and BMC
    [Tags]     common  FB_BMC_COMM_TC_018_Internal_USB_Network_Check  wedge400
    [Timeout]  5 min 00 seconds
    [Setup]  go to openbmc
    Sub-Case  FB_BMC_COMM_TC_018_1  Check usb0 ipv6 address&mac&ping function
    Sub-Case  FB_BMC_COMM_TC_018_2  Using scp command to copy file from BMC to CPU by usb0 ipv6
    [Teardown]    clean up file on both bmc and cpu

FB_BMC_COMM_TC_019_OpenBMC_MAC_Address_Test
    [Documentation]  This test checks the BMC MAC address
    [Tags]     common  FB_BMC_COMM_TC_019_OpenBMC_MAC_Address_Test  wedge400
    [Timeout]  50 min 00 seconds
    [Setup]    prepare openbmc mac global variable
    Sub-Case  FB_BMC_COMM_TC_019_1  Check OpenBMC MAC address in SMB eeprom by Diag command
    Sub-Case  FB_BMC_COMM_TC_019_2  Use Diag tool eeprom to Update OpenBMC MAC address
    Sub-Case  FB_BMC_COMM_TC_019_3  Reset openbmc os to check mac address
    Sub-Case  FB_BMC_COMM_TC_019_4  Power cycle chassis to check mac address
    Sub-Case  FB_BMC_COMM_TC_019_5  Use Diag tool eeprom to Update OpenBMC MAC address back to previous value
    Sub-Case  FB_BMC_COMM_TC_019_6  Reset openbmc os to check mac address again
    [Teardown]    restore eeprom  ${mac_eeprom_path}  ${mac_eeprom_type}

FB_BMC_COMM_TC_020_Power_Control
    [Documentation]  This test verifies BMC can correctly control the system power to different states: power on, power off, power cycle, reset
    [Tags]     common  FB_BMC_COMM_TC_020_Power_Control  wedge400
    [Timeout]  40 min 00 seconds
    [Setup]  prepare dc unit init diag
    Sub-Case  FB_BMC_COMM_TC_020_1  chassis power cycle dut and check power status
    Sub-Case  FB_BMC_COMM_TC_020_2  run all the parameters of version utility
    Sub-Case  FB_BMC_COMM_TC_020_3  check power status and ping test
    Sub-Case  FB_BMC_COMM_TC_020_4  power off dut and ping test
    Sub-Case  FB_BMC_COMM_TC_020_5  power on dut and check the power status
    Sub-Case  FB_BMC_COMM_TC_020_6  ping cpu from bmc test
    Sub-Case  FB_BMC_COMM_TC_020_7  power reset cpu and check only cpu be reset
    [Teardown]  Run Keyword If Test Failed  set power on chassis

FB_BMC_COMM_TC_021_OpenBMC_Reset_Test
    [Documentation]  This test verifies BMC can reboot successfully without any impact on COM-e
    [Tags]     common  FB_BMC_COMM_TC_021_OpenBMC_Reset_Test  wedge400
    [Timeout]  30 min 00 seconds
    Sub-Case  FB_BMC_COMM_TC_021_1  check master openbmc and check com-e side
    [Teardown]  switch bmc flash to Master and change dir to default

FB_BMC_COMM_TC_022_Sensor_Info_Test
    [Documentation]  This test verifies the sensor information can be displayed correctly as the definition in BMC spec
    [Tags]     common  FB_BMC_COMM_TC_022_Sensor_Info_Test  wedge400
    [Timeout]  30 min 00 seconds
    [Setup]  set time delay  60
    Sub-Case  FB_BMC_COMM_TC_022_1  check all sensor list wedge400
    [Teardown]  change dir to default

FB_BMC_COMM_TC_023_Fan_Speed_Manual_Control
    [Documentation]  This test verifies BMC can control the fan speed manually
    [Tags]     common  FB_BMC_COMM_TC_023_Fan_Speed_Manual_Control  wedge400
    [Timeout]  10 min 00 seconds
    [Setup]  set time delay  60
    Sub-Case  FB_BMC_COMM_TC_023_1  read fan speed and disable fan auto control
    Sub-Case  FB_BMC_COMM_TC_023_2  run command to enable fan auto control and read fan speed
    Sub-Case  FB_BMC_COMM_TC_023_3  run commnad to disable fan auto control and set and get fan speed 25
    Sub-Case  FB_BMC_COMM_TC_023_4  set and get fan speed 50
    Sub-Case  FB_BMC_COMM_TC_023_5  set and get fan speed 70
    Sub-Case  FB_BMC_COMM_TC_023_6  set and get fan speed 10
    Sub-Case  FB_BMC_COMM_TC_023_7  set and get fan speed 70
    Sub-Case  FB_BMC_COMM_TC_023_8  set and get fan speed 10
    Sub-Case  FB_BMC_COMM_TC_023_9  set and get fan speed 70
    Sub-Case  FB_BMC_COMM_TC_023_10  set and get fan speed 10
    Sub-Case  FB_BMC_COMM_TC_023_11  run command to enable fan auto control
    [Teardown]  run command to enable fan auto control

FB_BMC_COMM_TC_032_GPIO_Config
    [Documentation]  This test verifies GPIO dir/value can be set/get successfully
    [Tags]     common  FB_BMC_COMM_TC_032_GPIO_Config  wedge400
    [Timeout]  15 min 00 seconds
    [Setup]  get board type
    Sub-Case  FB_BMC_COMM_TC_032_1  chassis power cycle dut and run command to config gpio
    Sub-Case  FB_BMC_COMM_TC_032_2  run command to config gpio direction to out
    Sub-Case  FB_BMC_COMM_TC_032_3  run command to config value to 1
    Sub-Case  FB_BMC_COMM_TC_032_4  run command to config direction to in
    [Teardown]  change dir

FB_BMC_COMM_TC_033_WD1_Test
    [Documentation]  This test verifies when WD1 be activated, system will auto reboot when stop feeding
    [Tags]     common  FB_BMC_COMM_TC_033_WD1_Test  wedge400
    [Timeout]  40 min 00 seconds
    Sub-Case  FB_BMC_COMM_TC_033_1  chassis power cycle dut and reset bmc os and check watchdog info
    Sub-Case  FB_BMC_COMM_TC_033_2  run command reboot to reset master bmc and check watchdog info
    Sub-Case  FB_BMC_COMM_TC_033_3  run command to boot from slave bmc and check watchdog info
    Sub-Case  FB_BMC_COMM_TC_033_4  run command to reset bmc os and check watchdog info
    Sub-Case  FB_BMC_COMM_TC_033_5  run command reboot to reset slave bmc and check watchdog info
    Sub-Case  FB_BMC_COMM_TC_033_6  run command to boot from master bmc and check watchdog info
    [Teardown]  switch bmc flash to Master

FB_BMC_COMM_TC_034_SCM_EEPROM_R/W_Test
    [Documentation]  This test verifies SCM EEPROM could be R/W successfully
    [Tags]     common  FB_BMC_COMM_TC_034_SCM_EEPROM_R/W_Test  wedge400
    [Timeout]  35 min 00 seconds
    [Setup]  prepare store eeprom w400  ${scm_eeprom_path}  SCM
    Sub-Case  FB_BMC_COMM_TC_034_1  run command to read scm eeprom
    Sub-Case  FB_BMC_COMM_TC_034_2  run command to write and read scm eeprom
    Sub-Case  FB_BMC_COMM_TC_034_3  reset bmc and read scm eeprom
    Sub-Case  FB_BMC_COMM_TC_034_4  chassis power cycle and read scm eeprom
    Sub-Case  FB_BMC_COMM_TC_034_5  run command to write and read scm eeprom with different data
    Sub-Case  FB_BMC_COMM_TC_034_6  reset bmc and read scm eeprom with different data
    [Teardown]  restore eeprom  ${scm_eeprom_path}  SCM

FB_BMC_COMM_TC_035_SMB_EEPROM_R/W_Test
    [Documentation]  This test verifies SMB EEPROM could be R/W successfully
    [Tags]     common  FB_BMC_COMM_TC_035_SMB_EEPROM_R/W_Test  wedge400
    [Timeout]  35 min 00 seconds
    [Setup]  Run Keywords  prepare store eeprom  ${smb_eeprom_path}  SMB
             ...      AND  Run keyword if  ${has_pem}  check pem presence device  ELSE  set false pem device
    Sub-Case  FB_BMC_COMM_TC_035_1  run command to read smb eeprom
    Sub-Case  FB_BMC_COMM_TC_035_2  run command to write and read smb eeprom
    Sub-Case  FB_BMC_COMM_TC_035_3  reset bmc and read smb eeprom
    Sub-Case  FB_BMC_COMM_TC_035_4  chassis power cycle and read smb eeprom
    Sub-Case  FB_BMC_COMM_TC_035_5  run command to write and read smb eeprom with different data
    Sub-Case  FB_BMC_COMM_TC_035_6  reset bmc and read smb eeprom with different data
    [Teardown]  restore eeprom  ${smb_eeprom_path}  SMB

FB_BMC_COMM_TC_036_FCB_EEPROM_R/W_Test
    [Documentation]  This test verifies FCB EEPROM could be R/W successfully
    [Tags]     common  FB_BMC_COMM_TC_036_FCB_EEPROM_R/W_Test  wedge400
    [Timeout]  45 min 00 seconds
    [Setup]  prepare store eeprom  ${fcm_eeprom_path}  FCM
    Sub-Case  FB_BMC_COMM_TC_036_1  run command to read fcb eeprom
    Sub-Case  FB_BMC_COMM_TC_036_2  run command to write and read fcb eeprom
    Sub-Case  FB_BMC_COMM_TC_036_3  reset bmc and read fcb eeprom
    Sub-Case  FB_BMC_COMM_TC_036_4  chassis power cycle and read fcb eeprom
    Sub-Case  FB_BMC_COMM_TC_036_5  run command to write and read fcb eeprom with different data
    Sub-Case  FB_BMC_COMM_TC_036_6  reset bmc and read fcb eeprom with different data
    [Teardown]  restore eeprom  ${fcm_eeprom_path}  FCM

FB_BMC_COMM_TC_037_FAN_EEPROM_R/W_Test
    [Documentation]  This test verifies FAN EEPROM could be R/W successfully
    [Tags]     common  FB_BMC_COMM_TC_037_FAN_EEPROM_R/W_Test  wedge400
    [Timeout]  75 min 00 seconds
    [Setup]  prepare store all fan eeprom
    Sub-Case  FB_BMC_COMM_TC_037_1  run command to read fan eeprom
    Sub-Case  FB_BMC_COMM_TC_037_2  run command to write and read fan eeprom
    Sub-Case  FB_BMC_COMM_TC_037_3  reset bmc and read fan eeprom
    Sub-Case  FB_BMC_COMM_TC_037_4  chassis power cycle and read fan eeprom
    Sub-Case  FB_BMC_COMM_TC_037_5  run command to write and read fan eeprom with different data
    Sub-Case  FB_BMC_COMM_TC_037_6  reset bmc and read fan eeprom with different data
    [Teardown]  restore all fan eeprom

FB_BMC_COMM_TC_038_AC_PSU_EEPROM_Access_Test
    [Documentation]  This test verifies PSU EEPROM could be read successfully
    [Tags]     common  FB_BMC_COMM_TC_038_AC_PSU_EEPROM_Access_Test  wedge400
    [Timeout]  10 min 00 seconds
    Sub-Case  FB_BMC_COMM_TC_038_1  read ac psu eeprom

FB_BMC_COMM_TC_039_eMMC_R/W_Test
    [Documentation]  This test verifies eMMC can be R/W successfully without any error
    [Tags]     common  FB_BMC_COMM_TC_039_eMMC_R/W_Test  wedge400
    [Timeout]  40 min 00 seconds
    [Setup]  mount data  /dev/${emmc_disk_name}  ${emmc_path}  ${OPENBMC_MODE}
    Sub-Case  FB_BMC_COMM_TC_039_1  run command to check size of emmc
    Sub-Case  FB_BMC_COMM_TC_039_2  run command to read and write emmc
    [Teardown]  delete test file and change dir

FB_BMC_COMM_TC_040_Restful_fruid_test
    [Documentation]  This test verifies fru data can be read through Restful
    [Tags]     common  FB_BMC_COMM_TC_040_Restful_fruid_test  wedge400
    [Timeout]  10 min 00 seconds
    [Setup]  set time delay  90
    Sub-Case  FB_BMC_COMM_TC_040_1  check ipv4 address for bmc and cpu
    Sub-Case  FB_BMC_COMM_TC_040_2  read restful fruid via ipv4
    Sub-Case  FB_BMC_COMM_TC_040_3  check ipv6 address for bmc and cpu
    Sub-Case  FB_BMC_COMM_TC_040_4  read restful fruid via ipv6
    Sub-Case  FB_BMC_COMM_TC_040_5  compare restful fruid with fru data dumped in bmc os

FB_BMC_COMM_TC_041_Restful_BMC_Test
    [Documentation]  This test verifies BMC info can be read through Restful
    [Tags]     common  FB_BMC_COMM_TC_041_Restful_BMC_Test  wedge400
    [Timeout]  10 min 00 seconds
    [Setup]  set time delay  90
    Sub-Case  FB_BMC_COMM_TC_041_1  check ipv6 address for bmc and cpu
    Sub-Case  FB_BMC_COMM_TC_041_2  read restful bmc info via ipv6
    Sub-Case  FB_BMC_COMM_TC_041_3  compare bmc info dumped in cpu os

FB_BMC_COMM_TC_042_Restful_Sensors_Test
    [Documentation]  This test verifies sensor info can be read through Restful
    [Tags]     common  FB_BMC_COMM_TC_042_Restful_Sensors_Test  wedge400
    [Timeout]  10 min 00 seconds
    [Setup]  set time delay  90
    Sub-Case  FB_BMC_COMM_TC_042_1  check ipv6 address for bmc and cpu
    Sub-Case  FB_BMC_COMM_TC_042_2  read restful sensor via ipv6
    Sub-Case  FB_BMC_COMM_TC_042_3  compare restful sensor with sensor info dumped in bmc os

FB_BMC_COMM_TC_043_Restful_Status_Test
    [Documentation]  This test verifies the status can be got correctly by Restful
    [Tags]     common  FB_BMC_COMM_TC_043_Restful_Status_Test  wedge400
    [Timeout]  10 min 00 seconds
    [Setup]  set time delay  90
    Sub-Case  FB_BMC_COMM_TC_043_1  check ipv6 address for bmc and cpu
    Sub-Case  FB_BMC_COMM_TC_043_2  read restful status via ipv6
    Sub-Case  FB_BMC_COMM_TC_043_3  compare restful status with status dumped in bmc os

FB_BMC_COMM_TC_045_weutil_Test
    [Documentation]  This test verifies the utility could be executed successfully
    [Tags]     common  FB_BMC_COMM_TC_045_weutil_Test  wedge400
    [Timeout]  10 min 00 seconds
    Sub-Case  FB_BMC_COMM_TC_045_1  run weutil command
    Sub-Case  FB_BMC_COMM_TC_045_2  check smb fru data match with weutil command
    [Teardown]  change dir

FB_BMC_COMM_TC_046_feutil_Test
    [Documentation]  This test verifies the utility could be executed successfully with all support parameters
    [Tags]     common  FB_BMC_COMM_TC_046_feutil_Test  wedge400
    [Timeout]  10 min 00 seconds
    Sub-Case  FB_BMC_COMM_TC_046_1  run feutil command
    Sub-Case  FB_BMC_COMM_TC_046_2  check fan and fcm fru data match with feutil command
    [Teardown]  change dir

FB_BMC_COMM_TC_047_seutil_Test
    [Documentation]  This test verifies the utility could be executed successfully
    [Tags]     common  FB_BMC_COMM_TC_047_seutil_Test  wedge400
    [Timeout]  10 min 00 seconds
    Sub-Case  FB_BMC_COMM_TC_047_1  run seutil command
    Sub-Case  FB_BMC_COMM_TC_047_2  check scm fru data match with seutil command
    [Teardown]  change dir

FB_BMC_COMM_TC_048_BIC_Utility_Test
    [Documentation]  This test verifies the utility could be executed successfully with all support parameters
    [Tags]     common  FB_BMC_COMM_TC_048_BIC_Utility_Test  wedge400
    [Timeout]  15 min 00 seconds
    Sub-Case  FB_BMC_COMM_TC_048_1  run all the parameters of bic-util dev_id information
    Sub-Case  FB_BMC_COMM_TC_048_2  run all the parameters of bic-util gpio information
    Sub-Case  FB_BMC_COMM_TC_048_3  run all the parameters of bic-util config information
    Sub-Case  FB_BMC_COMM_TC_048_4  run all the parameters of bic-util post_code information
    Sub-Case  FB_BMC_COMM_TC_048_5  run all the parameters of bic-util sdr information
    Sub-Case  FB_BMC_COMM_TC_048_6  run all the parameters of bic-util sensor information
    Sub-Case  FB_BMC_COMM_TC_048_7  run all the parameters of bic-util fruid information
    Sub-Case  FB_BMC_COMM_TC_048_8  run all the parameters of bic-util mac information

FB_BMC_COMM_TC_049_SPI_Utility_Test
    [Documentation]  This test checks the output of spi_util command
    [Tags]     common  FB_BMC_COMM_TC_049_SPI_Utility_Test  wedge400
    [Timeout]  2 min 00 seconds
    Sub-Case  FB_BMC_COM_TC_049_1  run command and check output info

FB_BMC_COMM_TC_050_Version_Utility_Test
    [Documentation]  This test verifies the utility could be executed successfully and get the right version
    [Tags]     common  FB_BMC_COMM_TC_050_Version_Utility_Test  wedge400
    [Timeout]  5 min 00 seconds
    Sub-Case  FB_BMC_COMM_TC_050_1  run all the parameters of version utility

FB_BMC_COMM_TC_051_Presence_Utility_Test
    [Documentation]  This test verifies the utility could be executed successfully and get the right status
    [Tags]     common  FB_BMC_COMM_TC_051_Presence_Utility_Test  wedge400
    [Timeout]  3 min 00 seconds
    [Setup]  Run keyword if  ${has_pem}  check pem presence device  ELSE  set false pem device
    Sub-Case  FB_BMC_COMM_TC_051_1  run command to get fan/psu/debug card/scm status

FB_BMC_COMM_TC_053_Sensor_Utility_Test
    [Documentation]  This test verifies the utility could be executed successfully with all support parameters
    [Tags]     common  FB_BMC_COMM_TC_053_Sensor_Utility_Test  wedge400
    [Timeout]  30 min 00 seconds
    [Setup]  check pem presence device
    Sub-Case  FB_BMC_COMM_TC_053_1  run all the support parameters of sensor-util threshold
    Sub-Case  FB_BMC_COMM_TC_053_2  run all the support parameters of sensor-util history information
    Sub-Case  FB_BMC_COMM_TC_053_3  run all the support parameters of sensor-util history clear
    Sub-Case  FB_BMC_COMM_TC_053_4  run all the support parameters of sensor-util firmware information
    [Teardown]  change dir to default

FB_BMC_COMM_TC_054_PSU_Utility_Test_AC_PSU
    [Documentation]  This test verifies the utility could be executed successfully with all support parameters
    [Tags]     common  FB_BMC_COMM_TC_054_PSU_Utility_Test_AC_PSU  wedge400
    [Timeout]  5 min 00 seconds
    Sub-Case  FB_BMC_COMM_TC_054_1  run all the parameters of psu-util

FB_BMC_COMM_TC_055_Tftp_Client_Tool_Test
    [Documentation]  This test verifies the tftp tool could be executed successfully to download file
    [Tags]     common  FB_BMC_COMM_TC_055_Tftp_Client_Tool_Test  wedge400
    [Timeout]  10 min 00 seconds
    [Setup]  check file size on tftp server
    Sub-Case  FB_BMC_COMM_TC_055_1  copy the image file from tftp server and check size
    [Teardown]  clean up file  DUT  ${tftp_file_test}

FB_BMC_COMM_TC_056_Get_Device_ID
    [Documentation]  This test verifies the generic OpenBMC info can be got correctly,
                     ...  including OpenBMC version, manufacture ID and product ID
    [Tags]     common  FB_BMC_COMM_TC_056_Get_Device_ID  wedge400
    [Timeout]  40 min 00 seconds
    Sub-Case  FB_BMC_COMM_TC_056_1  run ipmi command "get device id" to get openbmc info in master openbmc
    Sub-Case  FB_BMC_COMM_TC_056_2  run ipmi command "get device id" to get openbmc info in slave openbmc
    [Teardown]  switch bmc flash to Master

FB_BMC_COMM_TC_057_Reset_BMC_From_Host
    [Documentation]  This test verifies the reset BMC function from host ipmitool command
    [Tags]     common  FB_BMC_COMM_TC_057_Reset_BMC_From_Host  wedge400
    [Timeout]  10 min 00 seconds
    Sub-Case  FB_BMC_COMM_TC_057_1  run ipmi command "reset bmc from host" in master openbmc

FB_BMC_COMM_TC_058_Get_Selftest_Results
    [Documentation]  This test verifies if the bmc selftest result can be get correctly
                     ...  no matter the selftest result is passed or failed
    [Tags]     common  FB_BMC_COMM_TC_058_Get_Selftest_Results  wedge400
    [Timeout]  30 min 00 seconds
    Sub-Case  FB_BMC_COMM_TC_058_1  get the bmc selftest result via ipmi command "get self results" in master openbmc
    [Teardown]  Run Keyword If Test Failed  set power reset chassis

FB_BMC_COMM_TC_059_Get_Device_GUID
    [Documentation]  This test checks the command could be executed successfully to set/get system guid
    [Tags]     common  FB_BMC_COMM_TC_059_Get_Device_GUID  wedge400
    [Timeout]  2 min 00 seconds
    Sub-Case  FB_BMC_COMM_TC_059_1  run command to get device guid

FB_BMC_COMM_TC_064_System_Info_Parameters_Test
    [Documentation]  This test verifies if the BIOS version can be get/set successfully via IPMI commands
    [Tags]     common  FB_BMC_COMM_TC_064_System_Info_Parameters_Test  wedge400
    [Timeout]  15 min 00 seconds
    Sub-Case  FB_BMC_COMM_TC_064_1  run ipmi command "get system info parameters" to get actual bios version
    Sub-Case  FB_BMC_COMM_TC_064_2  run ipmi command "set system info parameters" to set virtual bios version
    Sub-Case  FB_BMC_COMM_TC_064_3  run ipmi command "get system info parameters" to check virtual bios version
    Sub-Case  FB_BMC_COMM_TC_064_4  reboot unit and then get the bios version again
    [Teardown]  Run Keyword If Test Failed  reboot diag os

FB_BMC_COMM_TC_066_Get_Lan_Configuration
    [Documentation]  This test checks the command could be executed successfully to get lan config
    [Tags]     common  FB_BMC_COMM_TC_066_Get_Lan_Configuration  wedge400
    [Timeout]  2 min 00 seconds
    Sub-Case  FB_BMC_COMM_TC_066_1  run ipmi command "get lan config"

FB_BMC_COMM_TC_067_Get_SOL_Configuration
    [Documentation]  This test checks the command could be executed successfully to get sol config
    [Tags]     common  FB_BMC_COMM_TC_067_Get_SOL_Configuration  wedge400
    [Timeout]  2 min 00 seconds
    Sub-Case  FB_BMC_COMM_TC_067_1  run ipmi command to get sol info

FB_BMC_COMM_TC_070_Get_Board_ID
    [Documentation]  This test verifies the command can response the correct board id information
    [Tags]     common  FB_BMC_COMM_TC_070_Get_Board_ID  wedge400
    [Timeout]  2 min 00 seconds
    Sub-Case  FB_BMC_COMM_TC_070_1  get board id via command "get board id"

FB_BMC_COMM_TC_071_Get_Port80_Record
    [Documentation]  This test verifies the command can response the correct BIOS post code
    [Tags]     common  FB_BMC_COMM_TC_071_Get_Port80_Record  wedge400
    [Timeout]  2 min 00 seconds
    Sub-Case  FB_BMC_COMM_TC_071_1  read port80 record via command "get port80 record"

FB_BMC_COMM_TC_072_Get_PCIE_Configuration
    [Documentation]  This test checks pcie configuration could be got correctly
    [Tags]     common  FB_BMC_COMM_TC_072_Get_PCIE_Configuration  wedge400
    [Timeout]  2 min 00 seconds
    Sub-Case  FB_BMC_COMM_TC_072_1  get pcie configuration via "get pcie configuration" command

FB_BMC_COMM_TC_073_Set_POST_Start
    [Documentation]  This test verifies the OEM command can be executed successfully
    [Tags]     common  FB_BMC_COMM_TC_073_Set_POST_Start  wedge400
    [Timeout]  2 min 00 seconds
    Sub-Case  FB_BMC_COMM_TC_073_1  issue "set post start" command

FB_BMC_COMM_TC_074_Set_POST_End
    [Documentation]  This test verifies the OEM command can be executed successfully
    [Tags]     common  FB_BMC_COMM_TC_074_Set_POST_End  wedge400
    [Timeout]  2 min 00 seconds
    Sub-Case  FB_BMC_COMM_TC_074_1  issue "set post end" command

FB_BMC_COMM_TC_076_DIMM_Information_Get/Set_Test
    [Documentation]  This test verifies the DIMM information could be got/set successfully via the OEM command
    [Tags]     common  FB_BMC_COMM_TC_076_DIMM_Information_Get/Set_Test  wedge400
    [Timeout]  20 min 00 seconds
    [Setup]  go to centos
    Sub-Case  FB_BMC_COMM_TC_076_1  get default dimm 0 information via "get dimm information" command
    Sub-Case  FB_BMC_COMM_TC_076_2  set dimm 0 info with "set dimm Information" command
    Sub-Case  FB_BMC_COMM_TC_076_3  get dimm 0 information via "get dimm information" command
    Sub-Case  FB_BMC_COMM_TC_076_4  get default dimm 1 information via "get dimm Information" command
    Sub-Case  FB_BMC_COMM_TC_076_5  set dimm 1 info with "set dimm information" command
    Sub-Case  FB_BMC_COMM_TC_076_6  get dimm 1 information via "get dimm Information" command
    Sub-Case  FB_BMC_COMM_TC_076_7  reboot diag os and check the dimm info should restore to default value
    [Teardown]  Run Keyword If Test Failed  set power reset chassis

FB_BMC_COMM_TC_077_Processor_Information_Get/Set_Test
    [Documentation]  This test verifies the Processor information can be get/set successfully via the OEM command
    [Tags]     common  FB_BMC_COMM_TC_077_Processor_Information_Get/Set_Test  wedge400
    [Timeout]  15 min 00 seconds
    [Setup]  go to centos
    Sub-Case  FB_BMC_COMM_TC_077_1  get default processor 0 information via "get processor 0 information" command
    Sub-Case  FB_BMC_COMM_TC_077_2  set processor 0 info with "set processor 0 information" command
    Sub-Case  FB_BMC_COMM_TC_077_3  get processor 0 information via "get processor 0 information" command
    Sub-Case  FB_BMC_COMM_TC_077_4  reboot dut and check the processor info 0 should restore to default value
    Sub-Case  FB_BMC_COMM_TC_077_5  go to openbmc
    [Teardown]  Run Keyword If Test Failed  set power reset chassis

FB_BMC_COMM_TC_084_OpenBMC_Memory_Test
    [Documentation]  This test verifies OpenBMC Memory can be R/W without any error
    [Tags]     common  FB_BMC_COMM_TC_084_OpenBMC_Memory_Test  wedge400
    [Timeout]  30 min 00 seconds
    Sub-Case  FB_BMC_COMM_TC_084_1  get memory information
    Sub-Case  FB_BMC_COMM_TC_084_2  assign memory size to run memory rw test with tool memtester
    [Teardown]  change dir

FB_BMC_COMM_TC_085_SOL_Test
    [Documentation]  This test verifies BMC can access COMe through SOL
    [Tags]     common  FB_BMC_COMM_TC_085_SOL_Test  wedge400
    [Timeout]  10 min 00 seconds
    [Setup]    go to openbmc
    Sub-Case  FB_BMC_COMM_TC_085_1  run command to verify sol test

FB_BMC_COMM_TC_086_CPLD_Register_R/W_Test
    [Documentation]  This test verifies the SCM CPLD REG could be RW successfully
    [Tags]     common  FB_BMC_COMM_TC_086_CPLD_Register_R/W_Test  wedge400
    [Timeout]  15 min 00 seconds
    Sub-Case  FB_BMC_COMM_TC_086_1  run command "wedge_power.sh status"
    Sub-Case  FB_BMC_COMM_TC_086_2  run command to read/write scm cpld reg to power off com-e
    Sub-Case  FB_BMC_COMM_TC_086_3  run command to read/write scm cpld reg to power on com-e
    [Teardown]  Run Keyword If Test Failed  set power on chassis

FB_BMC_COMM_TC_087_TPM_Test
    [Documentation]  This test verifies TPM test
    [Tags]     common  FB_BMC_COMM_TC_087_TPM_Test  wedge400
    [Timeout]  30 min 00 seconds
    [Setup]  prepare images  TPM
    Sub-Case  FB_BMC_COMM_TC_087_1  run tpm script
    [Teardown]  clean tmp script and change dir

FB_BMC_COMM_TC_089_MDIO_Test
    [Documentation]  This test verifies MDIO function
    [Tags]     common  FB_BMC_COMM_TC_089_MDIO_Test  wedge400
    [Timeout]  4 min 00 seconds
    Sub-Case  FB_BMC_COMM_TC_089_1  run command to enable mdio and read reg
    Sub-Case  FB_BMC_COMM_TC_089_2  run command to write and read mdio reg
    Sub-Case  FB_BMC_COMM_TC_089_3  run command to write and read mdio reg again
    [Teardown]  run command to write mdio to default value

FB_BMC_COMM_TC_090_CIT_Test
    [Documentation]  This test verifies CIT Test
    [Tags]     common  FB_BMC_COMM_TC_090_CIT_Test  wedge400
    [Timeout]  60 min 00 seconds
    [Setup]  prepare CIT scripts and check pem presence
    Sub-Case  FB_BMC_COMM_TC_090_1  install and run cit test w400
    [Teardown]  clean cit script and change dir

FB_BMC_COMM_TC_091_COMe_Mac_Test
    [Documentation]  This test verifies COMe side mac address Test
    [Tags]     common  FB_BMC_COMM_TC_091_COMe_Mac_Test  wedge400
    [Timeout]  5 min 00 seconds
    [Setup]    go to openbmc
    Sub-Case  FB_BMC_COMM_TC_090_1  check come side mac address
    [Teardown]  change dir

FB_BMC_COMM_TC_092_BIC_Power_Cycle_Stress_Test
    [Documentation]  This test verifies COMe side mac address Test
    [Tags]     common  FB_BMC_COMM_TC_092_BIC_Power_Cycle_Stress_Test  wedge400  critical
	FOR    ${INDEX}    IN RANGE    1    ${MaxLoopNum}
        Print Loop Info  ${INDEX}
        Sub-Case  FB_BMC_COMM_TC_092_1  check bic power cycle stress
    END
    [Teardown]  change dir

FB_BMC_W400_TC_001_Online_Update_AC_PSU_FW_in_BMC_OS
    [Documentation]  This test checks the BMC FW programming functions by updating the AC PSU FW in BMC OS
    [Tags]     wedge400  FB_BMC_W400_TC_001_Online_Update_AC_PSU_FW_in_BMC_OS  critical
    [Timeout]  40 min 00 seconds
    [Setup]  prepare PSU images
    Sub-Case  FB_BMC_W400_TC_001_1  upgrade psu1 fw
    Sub-Case  FB_BMC_W400_TC_001_2  downgrade psu1 fw
    Sub-Case  FB_BMC_W400_TC_001_3  upgrade psu1 fw
    Sub-Case  FB_BMC_W400_TC_001_4  upgrade psu2 fw
    Sub-Case  FB_BMC_W400_TC_001_5  downgrade psu2 fw
    Sub-Case  FB_BMC_W400_TC_001_6  upgrade psu2 fw
    Sub-Case  FB_BMC_W400_TC_001_7  chassis power cycle and check psu info and status if psu power on
    [Teardown]  clean images  DUT  PSU

FB_BMC_W400_TC_002_Online_Update_DC_PSU_FW_in_BMC_OS
    [Documentation]  This test checks the BMC FW programming functions by updating the DC PSU FW in BMC OS
    [Tags]     wedge400  FB_BMC_W400_TC_002_Online_Update_DC_PSU_FW_in_BMC_OS  critical
    [Timeout]  60 min 00 seconds
    [Setup]  prepare dc PSU images
    Sub-Case  FB_BMC_W400_TC_001_1  upgrade dc psu1 fw
    Sub-Case  FB_BMC_W400_TC_001_2  downgrade dc psu1 fw
    Sub-Case  FB_BMC_W400_TC_001_3  upgrade dc psu1 fw
    Sub-Case  FB_BMC_W400_TC_001_4  upgrade dc psu2 fw
    Sub-Case  FB_BMC_W400_TC_001_5  downgrade dc psu2 fw
    Sub-Case  FB_BMC_W400_TC_001_6  upgrade dc psu2 fw
    Sub-Case  FB_BMC_W400_TC_001_7  chassis power cycle and check psu info and status if psu power on
    [Teardown]  clean images  DUT  PSU

#FB_BMC_W400C_TC_003_PEM_EEPROM_R/W_Test
#    [Documentation]  This test verifies PEM EEPROM can be R/W successfully
#    [Tags]     wedge400  FB_BMC_W400C_TC_003_PEM_EEPROM_R/W_Test
#    [Timeout]  15 min 00 seconds
#    [Setup]  check pem presence device and prepare store pem eeprom
#    Sub-Case  FB_BMC_W400C_TC_003_1  run command to read pem eeprom if pem present
#    Sub-Case  FB_BMC_W400C_TC_003_2  run command to write and read pem eeprom if pem present
#    Sub-Case  FB_BMC_W400C_TC_003_3  run command to write and read pem eeprom with different data if pem present
#    Sub-Case  FB_BMC_W400C_TC_003_4  chassis power cycle and read pem eeprom with different data if pem present
#    [Teardown]  restore pem eeprom and hotswap eeprom if pem present
#
#FB_BMC_W400C_TC_006_RackmonTest
#    [Documentation]  This test checks Rackmon service
#    [Tags]     wedge400  FB_BMC_W400C_TC_006_RackmonTest
#    [Timeout]  20 min 00 seconds
#    Sub-Case  FB_BMC_W400C_TC_006_2  Reboot OpenBMC and Check the rackmon service
#    Sub-Case  FB_BMC_W400C_TC_006_3  Check /tty/USB0 can be found
#
#FB_BMC_W400C_TC_007_bsm-eutil_Test
#    [Documentation]  This test verifies the utility could be executed successfully
#    [Tags]     wedge400  FB_BMC_W400C_TC_007_bsm-eutil_Test
#    [Timeout]  2 min 00 seconds
#    Sub-Case  FB_BMC_W400C_TC_007_1  run bsm-eutil command
#    Sub-Case  FB_BMC_W400C_TC_007_2  check bsm fru data match with bsm-eutil command
#    [Teardown]  change dir

*** Keywords ***
Bmc Connect Device
    BmcConnect

Bmc Disconnect Device
    BmcDisconnect
