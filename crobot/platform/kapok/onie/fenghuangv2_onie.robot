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
Documentation       This Suite will validate all Onie functions:

Variables         Const.py
Variables         KapokOnieVariable.py

Library          ../../../common/commonlib/CommonLib.py
Library          ../KapokCommonLib.py
Library           KapokOnieLib.py

Resource          KapokOnieKeywords.robot

Suite Setup       Onie Connect Device
Suite Teardown    Onie Disconnect Device

*** Variables ***

*** Test Cases ***
ONIE_10.1_Install_ONIE_via_Flashcp_on_ONIE
    [Documentation]  This test checks the Installing ONIE via Flashcp on ONIE
    [Tags]  common  ONIE_10.1_Install_ONIE_via_Flashcp_on_ONIE  fenghuangv2
    [Timeout]  20 min 00 seconds
    [Setup]  boot Into Onie Rescue Mode
    Step  1  Check network connectivity and download ONIE file from TFTP server  ${ONIE_RESCUE_MODE}
    Step  2  get The Current Onie Partition Erase and install onie  ${ONIE_RESCUE_MODE}
    Step  3  Clear Onie File  ${ONIE_RESCUE_MODE}
    Step  4  power Cycle To Onie Install Mode
    Step  5  verify Onie Version

ONIE_10.6.1_ERASE_ONIE
    [Documentation]  This test checks ONIE can be erased
    [Tags]  common  ONIE_10.6.1_ERASE_ONIE  fenghuangv2
    [Timeout]  10 min 00 seconds
    [Setup]  boot Into Onie Rescue Mode
    Step  1  Check network connectivity  ${ONIE_RESCUE_MODE}
    Step  2  get The Current Onie Partition And Erase  ${ONIE_RESCUE_MODE}
    Step  3  reboot And Check Cannot Find Image

ONIE_10.2_Install_ONIE_Nor_flash_by_TFTP_Test
    [Documentation]  This test checks the Installing ONIE via Flashcp on DiagOS
    [Tags]  common  ONIE_10.2_Install_ONIE_Nor_flash_by_TFTP_Test  fenghuangv2
    [Timeout]  10 min 00 seconds
    [Setup]  boot Into Uboot
    Step  1  set Uboot IP
    Step  2  install Onie Under Uboot
    Step  3  verify Onie Version

ONIE_10.3_Install_ONIE_via_Flashcp_on_DiagOS
    [Documentation]  This test checks the Installing ONIE via Flashcp on DiagOS
    [Tags]  common  ONIE_10.3_Install_ONIE_via_Flashcp_on_DiagOS fenghuangv2
    [Timeout]  20 min 00 seconds
    [Setup]  boot Into DiagOS Mode
    Step  1  get Dhcp IP
    Step  2  Check network connectivity and download ONIE file from TFTP server  ${BOOT_MODE_DIAGOS}
    Step  3  get The Current Onie Partition Erase and install onie  ${BOOT_MODE_DIAGOS}
    Step  4  Clear Onie File  ${BOOT_MODE_DIAGOS}
    Step  5  power Cycle To Onie Install Mode
    Step  6  verify Onie Sys Info

ONIE_10.4.1_ONIE_Update_via_Static_IP+TFTP
    [Documentation]  This test checks the Installing ONIE via Static IP+TFTP
    [Tags]  common  ONIE_10.4.1_ONIE_Update_via_Static_IP+TFTP  fenghuangv2
    [Timeout]  20 min 00 seconds
    [Setup]  boot Into Onie Rescue Mode
    Step  1  Set Static IP And Check network connectivity
    Step  2  onie Self Update
    Step  3  verify Onie And CPLD Version

ONIE_10.4.2_ONIE_Update_via_DHCP_IP+TFTP
    [Documentation]  This test checks the Installing ONIE via DHCP IP+TFTP
                ...  need check next-server option for TFTP sever is configured in DHCP server
    [Tags]  common  ONIE_10.4.2_ONIE_Update_via_DHCP_IP+TFTP  fenghuangv2
    [Timeout]  20 min 00 seconds
    Step  1  fhv2 auto Update In Update Mode
    Step  2  verify Onie And CPLD Version  version=new

ONIE_10.4.5_ONIE_Update_via_image_self_noforce
    [Documentation]  This test is to verify that ONIE can be updated via ./
    [Tags]  ONIE_10.4.5_ONIE_Update_via_image_self_noforce  fenghuangv2
    [Setup]   boot into Onie Rescue Mode
    Step  1  onie Self Update   old
    Step  2  check FW version   old
    ${Current_Loop}  Evaluate  2-1
    FOR    ${INDEX}    IN RANGE    0   2
      Step  3  boot Into Onie Rescue Mode
      Step  4  onie update   new
      Step  5  check FW version  new
    END

ONIE_10.4.6_ONIE_Updater_Current_Test
    [Documentation]  This test checks the ONIE Updater from current version to current version
    [Tags]  common  ONIE_10.4.6_ONIE_Updater_Current_Test  fenghuangv2
    [Timeout]  180 min 00 seconds
    Step  1  Self Update Onie  new

ONIE_10.4.8.1_ONIE_Update_With_Current_Version
    [Documentation]  This test ensures that ONIE can be updated from current version to current version
    [Tags]  common  ONIE_10.4.8.1_ONIE_Update_With_Current_Version  fenghuangv2
    [Timeout]  25 min 00 seconds
    [Setup]  boot into Onie Rescue Mode
    Step  1  Onie Self Update  new
    Step  2  check FW version  new
    Step  3  boot into Onie Rescue Mode

ONIE_10.4.8.2_ONIE_Update_With_Higher_Version
    [Documentation]  This test ensures that ONIE can be updated from current version to higher version
    [Tags]  common  ONIE_10.4.8.2_ONIE_Update_With_Higher_Version  fenghuangv2
    [Timeout]  25 min 00 seconds
    [Setup]  boot into Onie Rescue Mode
    Step  1  Onie Update Higher Version
    Step  2  check onie higher version
    Step  3  boot into Onie Rescue Mode
    Step  4  Onie Self Update  new
    Step  5  check FW version  new


ONIE_10.4.8.3_ONIE_Update_With_Production_Version
    [Documentation]  This test ensures that ONIE can be updated from Production version to current version
    [Tags]  common  ONIE_10.4.8.3_ONIE_Update_With_Production_Version  fenghuangv2
    [Timeout]  40 min 00 seconds
    [Setup]  boot into Onie Rescue Mode
    Step  1  Onie Self Update  new
    Step  2  check FW version  new
    Step  3  boot into Onie Rescue mode
    Step  4  Onie Update Production version
    Step  5  check onie production version
    Step  6  boot into Onie Rescue Mode
    Step  7  Onie Self Update  new
    Step  8  check FW version  new

ONIE_10.4.8.4_ONIE_Update_With_Customer_Version
    [Documentation]  This test ensures that ONIE can be updated from Customer version to current version
    [Tags]  common  ONIE_10.4.8.4_ONIE_Update_With_Customer_Version  fenghuangv2
    [Timeout]  40 min 00 seconds
    [Setup]  boot into Onie Rescue Mode
    Step  1  Onie Self Update   new
    Step  2  check FW version   new
    Step  3  boot into Onie Rescue mode
    Step  4  Onie Update Customer Version
    Step  5  check onie customer version
    Step  6  boot into Onie Rescue mode
    Step  7  Onie Self Update   new
    Step  8  check FW version   new


ONIE_10.5.1_ONIE_NOS_Install_via_Static_IP_TFTP
     [Documentation]   This test is to verify that onie self-update via static ip and tftp
     [Tags]   ONIE_10.5.1_ONIE_NOS_Install_via_Static_IP_TFTP   fenghuangv2
     [Timeout]  15 min 00 seconds
     [Setup]  boot into ONIE install mode
    Step  1  Set Interface IP
    Step  2  Onie NOS Self Update
    Step  3  boot into DiagOS mode
    Step  4  Check DiagOS Ver

ONIE_10.5.2_ONIE_NOS_Install_via_DHCP_IP_TFTP
     [Documentation]   This test is to verify that onie can be NOS installation via DHCP ip and TFTP server
     [Tags]   ONIE_10.5.2_ONIE_NOS_Install_via_DHCP_IP_TFTP   fenghuangv2
    Step  1  Auto update in install mode
    Step  2  boot into DiagOS mode
    Step  3  Check DiagOS Ver


ONIE_10.7.1_ONIE_Booting_Mode_Check
    [Documentation]  This test checks the each support ONIE mode can boot into OS successfully
    [Tags]  common  ONIE_10.7.1_ONIE_Booting_Mode_Check  fenghuangv2
    [Timeout]  20 min 00 seconds
    Step  1  Switch And Check Booting Onie Version  installer
    Step  2  Switch And Check Booting Onie Version  update
    Step  3  Switch And Check Booting Onie Version  rescue
    Step  4  Switch And Check Booting Onie Version  Uninstall
    Step  5  switch To DiagOS

ONIE_10.7.2_ONIE_System_Information
    [Documentation]  This test checks ONIE system information is correct
    [Tags]  common  ONIE_10.7.2_ONIE_System_Information  fenghuangv2
    [Timeout]  5 min 00 seconds
    [Setup]  boot Into Onie Install Mode
    Step  1  check Onie Sys Info
    Step  2  check Onie Sys Info V
    Step  3  check Onie Os Release
    Step  4  check psu info
    Step  5  check thermal info
    Step  6  check fan info

ONIE_10.7.3_TLV_EEPROM_R/W_Test
    [Documentation]  This test checks TLV EEPROM can be read/write successfully in ONIE
    [Tags]  common  ONIE_10.7.3_TLV_EEPROM_R/W_Test  fenghuangv2
    [Timeout]  20 min 00 seconds
    [Setup]  Backup EEPROM TLV Value And Write Protect Value
    Step  1  Write TLV Value And Read To Check  ${TLV_Value_Test1}
    Step  2  Write TLV Value And Read To Check  ${TLV_Value_Test2}
    [Teardown]  Restore EEPROM TLV Value And Write Protect Value

ONIE_10.7.4_Auto_Discovery(Rescue Mode)
    [Documentation]  This test checks the system can enter ONIE rescue mode
    [Tags]  common  ONIE_10.7.4_Auto_Discovery(Rescue Mode)  fenghuangv2
    [Timeout]  5 min 00 seconds
    Step  1  switch And Check Booting  rescue
    Step  2  Check network connectivity  ${ONIE_RESCUE_MODE}
    Step  3  check Onie Tlv Value Existed


ONIE_10.7.7_CPLD/FPGA_Updates
    [Documentation]  This test checks that CPLD can be updated under ONIE mode
    [Tags]  common  ONIE_10.7.7_CPLD/FPGA_Updates  fenghuangv2
    [Timeout]  20 min 00 seconds
    Step  1  boot Into Onie Rescue Mode
    Step  2  Check network connectivity  ${ONIE_RESCUE_MODE}
    Step  3  fenghuangv2 upgrade cpld
    Step  4  power Cycle To Onie Rescue Mode
    Step  5  check Cpld Version

ONIE_10.7.8_I2C_Accelerator_FPGA_Update_Test
    [Documentation]  This test checks FPGA update
    [Tags]  common  ONIE_10.7.8_I2C_Accelerator_FPGA_Update_Test  fenghuangv2
    [Timeout]  15 min 00 seconds
    [Setup]  boot Into Onie Install Mode
    Step  1  run i2c update test
    Step  2  cat i2c version
    Step  3  power Cycle To Onie Rescue Mode
    Step  4  cat i2c version

ONIE_10.7.9_Startup_Sdk_Shell
    [Documentation]  This test checks the system can startup sdk shell
    [Tags]  common  ONIE_10.7.9_Startup_Sdk_Shell  fenghuangv2
    [Timeout]  10 min 00 seconds
    [Setup]  boot Into Onie Rescue Mode
    Step  1  Load Sdk Shell
    BuiltIn.Sleep  300  #WORKAROUND, as the proposal of wubin we set this delay, otherwise some port can't up!!!!
    Step  2  Check Port Links Status
    [Teardown]  Exit Sdk Shell

ONIE_10.7.10_Telnet_Access
    [Documentation]  This test checks the ONIE supporting telnet access without password
    [Tags]  common  ONIE_10.7.10_Telnet_Access  fenghuangv2
    [Timeout]  5 min 00 seconds
    [Setup]  boot Into Onie Install Mode
    Step  1  Get Device IP And Ping
    Step  2  check Onie Telnet

ONIE_10.7.11_SSH_Access
    [Documentation]  This test checks the ONIE supporting SSH access without password
    [Tags]     ONIE_10.7.11_SSH_Access  fenghuangv2
    [Setup]  boot Into Onie Rescue Mode
    Step  1  Get Device IP And Ping
    Step  2  ssh connect


ONIE_10.7.12_Serial_Console_Access
    [Documentation]  This test checks the system can enter and verify ONIE boot mode successfully
    [Tags]  common  ONIE_10.7.12_Serial_Console_Access  fenghuangv2
    [Timeout]  5 min 00 seconds
    [Setup]  boot Into Onie Install Mode
    Step  1  verify onie install mode works

ONIE_10.7.13_ONIE_Diag_OS_recovery_Test
    [Documentation]  This test checks that Diag os can be recoveried via ONIE
    [Tags]  common  ONIE_10.7.13_ONIE_Diag_OS_recovery_Test  fenghuangv2
    [Timeout]  20 min 00 seconds
    Step  1  boot Into Onie Rescue Mode
    Step  2  Check network connectivity  ${ONIE_RESCUE_MODE}
    Step  3  format Disk
    Step  4  try To Access DiagOS
    Step  5  fhv2 download Images And Recovery DiagOS
    Step  6  power Cycle To DiagOS
    Step  7  get Dhcp IP
    Step  8  Check network connectivity  ${BOOT_MODE_DIAGOS}
    Step  9  fhv2 download stress And Recovery DiagOS
    [Teardown]  decompress sdk

ONIE_10.7.14_File_system_ext3/ext4_Supports
    [Documentation]  This test checks that ONIE will support file system type ext3 and ext4
    [Tags]  common  ONIE_10.7.14_File_system_ext3/ext4_Supports  fenghuangv2
    [Timeout]  20 min 00 seconds
    Step  1  boot Into Onie Rescue Mode
    Step  2  delete Partion
    Step  3  create Partion
    Step  4  test Format Disk With ext3/ext4  /dev/sda5

ONIE_10.7.15_File_System_Utilities_Test
    [Documentation]  This test checks that onie file system utilities
    [Tags]  common  ONIE_10.7.15_File_System_Utilities_Test  fenghuangv2
    [Timeout]  20 min 00 seconds
    Step  1  boot Into Onie Rescue Mode
    Step  2  check File System Utilities

ONIE_10.7.16_Default_file_Name_Search_Order
    [Documentation]  This test checks the ONIE will automatically search filename of NOS according
    ...  to regular rule by default
    [Tags]  common  ONIE_10.7.16_Default_file_Name_Search_Order  fenghuangv2
    [Timeout]  30 min 00 seconds
    Step  1  check File Search Order  installer  ${INSTALLER_FILE_SEARCH_ORDER}
    Step  2  rename onie image  toBackup=${TRUE}
    Step  3  check File Search Order  update  ${UPDATER_FILE_SEARCH_ORDER}
    Step  4  check Rescue Discovery Stop
    [Teardown]  rename onie image  toBackup=${FALSE}

ONIE_10.7.17_Installer_Discovery_Methods
    [Documentation]  This test checks the ONIE can locate the installer through a number of discovery methods
    [Tags]  common  ONIE_10.7.17_Installer_Discovery_Methods  fenghuangv2
    [Timeout]  20 min 00 seconds
    [Setup]  boot Into Onie Install Mode
    Step  1  installer Discovery Check

ONIE_10.7.18_Uboot_Environment_Access
    [Documentation]  This test checks that uboot environment access
    [Tags]  common  ONIE_10.7.18_Uboot_Environment_Access  fenghuangv2
    [Timeout]  20 min 00 seconds
    Step  1  boot Into Onie Rescue Mode
    Step  2  onie Ifconfig Eth0
    Step  3  boot Into Uboot
    Step  4  set Eth1 Addr
    Step  5  boot Into Onie Rescue Mode
    Step  6  compare Onie Uboot address
    Step  7  add Test Parameters  1
    Step  8  add Test Parameters  2
    Step  9  add Test Parameters  3
    Step  10  add Test Parameters  4
    Step  11  boot Into Uboot
    Step  12  printenv On Uboot
    Step  13  restore Uboot Env

ONIE_10.7.19_SSD_Device_Health_Status
    [Documentation]  This test checks that ONIE will support checking SSD device health
    [Tags]  common  ONIE_10.7.19_SSD_Device_Health_Status  fenghuangv2
    [Timeout]  5 min 00 seconds
    [Setup]  boot Into Onie Install Mode
    Step  1  check Ssd Health

ONIE_10.7.20_FSC_Check_Test
    [Documentation]  This test checks that ONIE will support FSC function
    [Tags]  common  ONIE_10.7.20_FSC_Check_Test  fenghuangv2
    [Timeout]  10 min 00 seconds
    [Setup]  boot Into Onie Install Mode
    ${fanspeed}=  KapokOnieLib.get fan speed percent
    Step  1  check Fsc Code
    Step  2  check Fan Speed  ${fanspeed}
    Step  3  check Fan Ctrl

ONIE_10.7.21_QSFP_Access_Test
    [Documentation]  This test checks that ONIE can access QSFP via i2c interface
    [Tags]  common  ONIE_10.7.21_QSFP_Access_Test  fenghuangv2
    [Timeout]  5 min 00 seconds
    [Setup]  boot Into Onie Install Mode
    Step  1  fenghuangv2 check Qsfp Access

ONIE_10.7.22_Check_Driver_Information_in_ONIE
    [Documentation]  This test checks that driver works normal in ONIE
    [Tags]  common  ONIE_10.7.22_Check_Driver_Information_in_ONIE  fenghuangv2
    [Timeout]  20 min 00 seconds
    Step  1  fenghuangv2 check Driver Information  installer  True
    Step  2  fenghuangv2 check Driver Information  update  False
    Step  3  fenghuangv2 check Driver Information  rescue  False

ONIE_10.7.23_Check_onie_Platform_Information_in_uboot
    [Documentation]  This test checks whether onie_platform value in uboot is correct
    [Tags]  common  ONIE_10.7.23_Check_onie_Platform_Information_in_uboot  fenghuangv2
    [Timeout]  20 min 00 seconds
    [Setup]  boot Into Uboot
    Step  1  check platform info
    Step  2  check sys eeprom

ONIE_10.7.24_FPP_Modes_Test
    [Documentation]  This test checks that the onie_fpp uboot env variable setting is valid
    [Tags]  common  ONIE_10.7.24_FPP_Modes_Test  fenghuangv2
    [Timeout]  50 min 00 seconds
    FOR  ${PORT_MODE}  IN  @{FPP_MODES}
        Step  1  check Fpp Mode  ${PORT_MODE}
    END
    [Teardown]  restore Fpp Mode

ONIE_10.7.25_Integrator_Mode_Test
    [Documentation]  This test checks that could access integrator mode and set port status
    [Tags]  common  ONIE_10.7.25_Integrator_Mode_Test  fenghuangv2
    [Timeout]  20 min 00 seconds
    [Setup]  boot Into Onie Install Mode
	Step  1  quit Sdk Shell
    FOR  ${PORT_MODE}  IN  @{INTEGRATOR_TEST_MODES}
        Step  2  verify Can Access Integrator Mode  ${PORT_MODE}
        Step  3  enable Some Port And Verify Port Enable  1  32
    END

ONIE_10.7.26_SFP_Test
    [Documentation]  This test checks detecting sfp type
    [Tags]  common  ONIE_10.7.26_SFP_Test  fenghuangv2
    [Timeout]  5 min 00 seconds
    [Setup]  boot Into Onie Install Mode
    Step  1  check Qsfp Type
    Step  2  check Qsfp Manufacture Info
    Step  3  check Sfp Info

ONIE_11.3_ONIE_Updater_Stress_Test
    [Documentation]  This test checks the ONIE Updater Stress Test
    [Tags]  common  ONIE_11.3_ONIE_Updater_Stress_Test  fenghuangv2
    [Timeout]  1800 min 00 seconds
    FOR  ${CYCLE}  IN RANGE  0  10
        Step  1  boot into Onie Rescue mode
        Step  2  Onie Self Update  old
        Step  3  check FW version  old
        Step  4  boot into Onie Rescue mode
        Step  5  Set Interface IP
        Step  6  Onie Self Update  new
        Step  7  check FW version  new
        
    END

ONIE_10.4.3_ONIE_Update_via_noforce_on_ONIE
    [Documentation]  This test is to verify onie self-update via static ip and tftp.
    [Tags]  common  ONIE_10.4.3_ONIE_Update_via_noforce_on_ONIE  fenghuangv2
    [Setup]  boot into Onie Rescue Mode
    Step  1  onie Update Via No Force On ONIE  new
    Step  2  boot into Onie Rescue Mode
    Step  3  check FW version  new
    Step  4  onie Update Via No Force On ONIE  old
    Step  5  boot into Onie Rescue Mode
    Step  6  check FW version  old
    Step  7  Onie Self Update  new


ONIE_10.4.4_ONIE_Updat_via_image_self
    [Documentation]  The purpose of this test is to verify that ONIE can be updated via image self
    [Tags]  ONIE_10.4.4_ONIE_Updat_via_image_self   fenghuang  try
    [Timeout]  30 min 00 seconds
    ${ip} =  get ip address from config  PC
    [Setup]  boot Into Onie Rescue Mode
    Step  1  Check network connectivity and download ONIE file from TFTP server  ${ONIE_RESCUE_MODE}
    Step  2  get file and update  old
    Step  3  check Onie System version  old
    Step  5  get file and update  new
    Step  6  check Onie System version  new







*** Keywords ***
Onie Connect Device
    OnieConnect

Onie Disconnect Device
    OnieDisconnect
