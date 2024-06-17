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
KAPOK_OINE_TC_01_Install_ONIE_via_Flashcp_on_ONIE
    [Documentation]  This test checks the Installing ONIE via Flashcp on ONIE
    [Tags]  common  KAPOK_OINE_TC_01_Install_ONIE_via_Flashcp_on_ONIE  briggs
    [Timeout]  20 min 00 seconds
    [Setup]  boot Into Onie Rescue Mode
    Step  1  Check network connectivity and download ONIE file from TFTP server  ${ONIE_RESCUE_MODE}
    Step  2  get The Current Onie Partition Erase and install onie  ${ONIE_RESCUE_MODE}
    Step  3  Clear Onie File  ${ONIE_RESCUE_MODE}
    Step  4  power Cycle To Onie Install Mode
    Step  5  verify Onie Version

KAPOK_OINE_TC_09_ERASE_ONIE
    [Documentation]  This test checks ONIE can be erased
    [Tags]  common  KAPOK_OINE_TC_09_ERASE_ONIE  briggs
    [Timeout]  10 min 00 seconds
    [Setup]  boot Into Onie Rescue Mode
    Step  1  Check network connectivity  ${ONIE_RESCUE_MODE}
    Step  2  get The Current Onie Partition And Erase  ${ONIE_RESCUE_MODE}
    Step  3  reboot And Check Cannot Find Image

KAPOK_OINE_TC_03_Install_ONIE_Nor_flash_by_TFTP_Test
    [Documentation]  This test checks the Installing ONIE via Flashcp on DiagOS
    [Tags]  common  KAPOK_OINE_TC_03_Install_ONIE_Nor_flash_by_TFTP_Test  briggs
    [Timeout]  10 min 00 seconds
    [Setup]  boot Into Uboot
    Step  1  set Uboot IP
    Step  2  install Onie Under Uboot
    Step  3  verify Onie Version

KAPOK_OINE_TC_04_Install_ONIE_via_Flashcp_on_DiagOS
    [Documentation]  This test checks the Installing ONIE via Flashcp on DiagOS
    [Tags]  common  KAPOK_OINE_TC_04_Install_ONIE_via_Flashcp_on_DiagOS  briggs
    [Timeout]  20 min 00 seconds
    [Setup]  boot Into DiagOS Mode
    Step  1  get Dhcp IP
    Step  2  Check network connectivity and download ONIE file from TFTP server  ${BOOT_MODE_DIAGOS}
    Step  3  get The Current Onie Partition Erase and install onie  ${BOOT_MODE_DIAGOS}
    Step  4  Clear Onie File  ${BOOT_MODE_DIAGOS}
    Step  5  power Cycle To Onie Install Mode
    Step  6  verify Onie Sys Info

KAPOK_OINE_TC_05_ONIE_Update_via_Static_IP+TFTP
    [Documentation]  This test checks the Installing ONIE via Static IP+TFTP
    [Tags]  common  KAPOK_OINE_TC_05_ONIE_Update_via_Static_IP+TFTP  briggs
    [Timeout]  20 min 00 seconds
    [Setup]  boot Into Onie Rescue Mode
    Step  1  Set Static IP And Check network connectivity
    Step  2  onie Self Update
    Step  3  verify Onie And CPLD Version

KAPOK_OINE_TC_06_ONIE_Update_via_DHCP_IP+TFTP
    [Documentation]  This test checks the Installing ONIE via DHCP IP+TFTP
                ...  need check next-server option for TFTP sever is configured in DHCP server
    [Tags]  common  KAPOK_OINE_TC_06_ONIE_Update_via_DHCP_IP+TFTP  briggs
    [Timeout]  20 min 00 seconds
    Step  1  auto Update In Update Mode
    Step  2  verify Onie And CPLD Version  version=new

KAPOK_OINE_TC_07_ONIE_Updater_Current_Test
    [Documentation]  This test checks the ONIE Updater from current version to current version
    [Tags]  common  KAPOK_OINE_TC_07_ONIE_Updater_Current_Test  briggs
    [Timeout]  180 min 00 seconds
    Step  1  Self Update Onie  new

KAPOK_OINE_TC_08_ONIE_Updater_Stress_Test
    [Documentation]  This test checks the ONIE Updater Stress Test
    [Tags]  common  KAPOK_OINE_TC_08_ONIE_Updater_Stress_Test  briggs
    [Timeout]  180 min 00 seconds
    FOR  ${CYCLE}  IN RANGE  0  2
        Step  1  Self Update Onie  old
        Step  2  Self Update Onie  new
    END

KAPOK_OINE_TC_10_ONIE_Booting_Mode_Check
    [Documentation]  This test checks the each support ONIE mode can boot into OS successfully
    [Tags]  common  KAPOK_OINE_TC_10_ONIE_Booting_Mode_Check  briggs
    [Timeout]  20 min 00 seconds
    Step  1  Switch And Check Booting Onie Version  installer
    Step  2  Switch And Check Booting Onie Version  update
    Step  3  Switch And Check Booting Onie Version  rescue
    Step  4  Switch And Check Booting Onie Version  Uninstall
    Step  5  switch To DiagOS

KAPOK_OINE_TC_11_ONIE_System_Information
    [Documentation]  This test checks ONIE system information is correct
    [Tags]  common  KAPOK_OINE_TC_11_ONIE_System_Information  briggs
    [Timeout]  5 min 00 seconds
    [Setup]  boot Into Onie Install Mode
    Step  1  check Onie Sys Info
    Step  2  check Onie Sys Info V
    Step  3  check Onie Os Release

KAPOK_OINE_TC_12_TLV_EEPROM_R/W_Test
    [Documentation]  This test checks TLV EEPROM can be read/write successfully in ONIE
    [Tags]  common  KAPOK_OINE_TC_12_TLV_EEPROM_R/W_Test  briggs
    [Timeout]  20 min 00 seconds
    [Setup]  Backup EEPROM TLV Value And Write Protect Value
    Step  1  Write TLV Value And Read To Check  ${TLV_Value_Test1}
    Step  2  Write TLV Value And Read To Check  ${TLV_Value_Test2}
    [Teardown]  Restore EEPROM TLV Value And Write Protect Value

KAPOK_OINE_TC_13_Auto_Discovery(Rescue Mode)
    [Documentation]  This test checks the system can enter ONIE rescue mode
    [Tags]  common  KAPOK_OINE_TC_13_Auto_Discovery(Rescue Mode)  briggs
    [Timeout]  5 min 00 seconds
    Step  1  switch And Check Booting  rescue
    Step  2  Check network connectivity  ${ONIE_RESCUE_MODE}
    Step  3  check Onie Tlv Value Existed


KAPOK_OINE_TC_16_CPLD/FPGA_Updates
    [Documentation]  This test checks that CPLD can be updated under ONIE mode
    [Tags]  common  KAPOK_OINE_TC_16_CPLD/FPGA_Updates  briggs
    [Timeout]  10 min 00 seconds
    Step  1  boot Into Onie Rescue Mode
    Step  2  Check network connectivity  ${ONIE_RESCUE_MODE}
    Step  3  upgrade Cpld
    Step  4  power Cycle To Onie Rescue Mode
    Step  5  check Cpld Version

KAPOK_OINE_TC_19_Startup_Sdk_Shell
    [Documentation]  This test checks the system can startup sdk shell
    [Tags]  common  KAPOK_OINE_TC_19_Startup_Sdk_Shell  briggs
    [Timeout]  5 min 00 seconds
    [Setup]  boot Into Onie Rescue Mode
    Step  1  Load Sdk Shell
    Step  2  Check Port Links Status
    Step  3  Exit Sdk Shell

KAPOK_OINE_TC_20_Telnet_Access
    [Documentation]  This test checks the ONIE supporting telnet access without password
    [Tags]  common  KAPOK_OINE_TC_20_Telnet_Access  briggs
    [Timeout]  5 min 00 seconds
    [Setup]  boot Into Onie Install Mode
    Step  1  Get Device IP And Ping
    Step  2  check Onie Telnet

KAPOK_ONIE_TC_22_Serial_Console_Access
    [Documentation]  This test checks the system can enter and verify ONIE boot mode successfully
    [Tags]  common  KAPOK_ONIE_TC_22_Serial_Console_Access  briggs
    [Timeout]  5 min 00 seconds
    [Setup]  boot Into Onie Install Mode
    Step  1  verify onie install mode works

KAPOK_OINE_TC_23_File_system_ext3/ext4_Supports
    [Documentation]  This test checks that ONIE will support file system type ext3 and ext4
    [Tags]  common  KAPOK_OINE_TC_23_File_system_ext3/ext4_Supports  briggs
    [Timeout]  20 min 00 seconds
    Step  1  boot Into Onie Rescue Mode
    Step  2  delete Partion
    Step  3  create Partion
    Step  4  test Format Disk With ext3/ext4  /dev/sda5

KAPOK_OINE_TC_24_File_System_Utilities_Test
    [Documentation]  This test checks that onie file system utilities
    [Tags]  common  KAPOK_OINE_TC_24_File_System_Utilities_Test  briggs
    [Timeout]  20 min 00 seconds
    Step  1  boot Into Onie Rescue Mode
    Step  2  check File System Utilities

KAPOK_OINE_TC_25_Default_file_Name_Search_Order
    [Documentation]  This test checks the ONIE will automatically search filename of NOS according
    ...  to regular rule by default
    [Tags]  common  KAPOK_OINE_TC_25_Default_file_Name_Search_Order  briggs
    [Timeout]  20 min 00 seconds
    Step  1  check File Search Order  installer  ${INSTALLER_FILE_SEARCH_ORDER}
    Step  2  check File Search Order  update  ${UPDATER_FILE_SEARCH_ORDER}
    Step  3  check Rescue Discovery Stop

KAPOK_OINE_TC_26_Installer_Discovery_Methods
    [Documentation]  This test checks the ONIE can locate the installer through a number of discovery methods
    [Tags]  common  KAPOK_OINE_TC_26_Installer_Discovery_Methods  briggs
    [Timeout]  20 min 00 seconds
    [Setup]  boot Into Onie Install Mode
    Step  1  installer Discovery Check

KAPOK_OINE_TC_27_Uboot_Environment_Access
    [Documentation]  This test checks that uboot environment access
    [Tags]  common  KAPOK_OINE_TC_27_Uboot_Environment_Access  briggs
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

KAPOK_OINE_TC_28_SSD_Device_Health_Status
    [Documentation]  This test checks that ONIE will support checking SSD device health
    [Tags]  common  KAPOK_OINE_TC_28_SSD_Device_Health_Status  briggs
    [Timeout]  5 min 00 seconds
    [Setup]  boot Into Onie Install Mode
    Step  1  check Ssd Health

KAPOK_OINE_TC_29_FSC_Check_Test
    [Documentation]  This test checks that ONIE will support FSC function
    [Tags]  common  KAPOK_OINE_TC_29_FSC_Check_Test  briggs
    [Timeout]  10 min 00 seconds
    [Setup]  power Cycle To Onie Install Mode
    Step  1  check Fsc Code
    Step  2  check Fan Speed

KAPOK_OINE_TC_30_QSFP_Access_Test
    [Documentation]  This test checks that ONIE can access QSFP via i2c interface
    [Tags]  common  KAPOK_OINE_TC_30_QSFP_Access_Test  briggs
    [Timeout]  5 min 00 seconds
    [Setup]  boot Into Onie Install Mode
    Step  1  check Qsfp Access

KAPOK_OINE_TC_31_ONIE_Diag_OS_recovery_Test
    [Documentation]  This test checks that Diag os can be recoveried via ONIE
    [Tags]  common  KAPOK_OINE_TC_31_ONIE_Diag_OS_recovery_Test  briggs
    [Timeout]  20 min 00 seconds
    Step  1  boot Into Onie Rescue Mode
    Step  2  Check network connectivity  ${ONIE_RESCUE_MODE}
    Step  3  format Disk
    Step  4  mount Disk
    Step  5  download Images And Recovery DiagOS
    Step  6  power Cycle To DiagOS

KAPOK_OINE_TC_32_Check_Driver_Information_in_ONIE
    [Documentation]  This test checks that driver works normal in ONIE
    [Tags]  common  KAPOK_OINE_TC_32_Check_Driver_Information_in_ONIE  briggs
    [Timeout]  20 min 00 seconds
    Step  1  check Driver Information  installer  True
    Step  2  check Driver Information  update  False
    Step  3  check Driver Information  rescue  False

KAPOK_OINE_TC_33_Check_onie_Platform_Information_in_uboot
    [Documentation]  This test checks whether onie_platform value in uboot is correct
    [Tags]  common  KAPOK_OINE_TC_33_Check_onie_Platform_Information_in_uboot  fenghuang
    [Timeout]  20 min 00 seconds
    [Setup]  boot Into Uboot
    Step  1  check platform info
    Step  2  check sys eeprom

KAPOK_OINE_TC_34_QSFP_Test
    [Documentation]  This test checks detecting sfp type
    [Tags]  common  KAPOK_OINE_TC_34_QSFP_Test  fenghuang
    [Timeout]  5 min 00 seconds
    [Setup]  boot Into Onie Install Mode
    Step  1  check Qsfp Type
    Step  2  check Qsfp Manufacture Info

KAPOK_OINE_TC_36_FPP_Modes_Test
    [Documentation]  This test checks that the onie_fpp uboot env variable setting is valid
    [Tags]  common  KAPOK_OINE_TC_36_FPP_Modes_Test  briggs
    [Timeout]  50 min 00 seconds
    FOR  ${PORT_MODE}  IN  @{FPP_MODES}
        Step  1  check Fpp Mode  ${PORT_MODE}
    END
    [Teardown]  restore Fpp Mode

KAPOK_OINE_TC_37_Integrator_Mode_Test
    [Documentation]  This test checks that could access integrator mode and set port status
    [Tags]  common  KAPOK_OINE_TC_37_Integrator_Mode_Test  fenghuang
    [Timeout]  20 min 00 seconds
    [Setup]  boot Into Onie Install Mode
	Step  1  quit Sdk Shell
    FOR  ${PORT_MODE}  IN  @{INTEGRATOR_TEST_MODES}
        Step  2  verify Can Access Integrator Mode  ${PORT_MODE}
        Step  3  enable Some Port And Verify Port Enable  1  32
    END

*** Keywords ***
Onie Connect Device
    OnieConnect

Onie Disconnect Device
    OnieDisconnect
