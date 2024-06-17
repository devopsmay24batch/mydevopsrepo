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
ONIE_TC_000_Onie_Initialize_And_Version_Check
    [Documentation]  This test checks onie and uboot are latest version
    [Tags]  ONIE_TC_000_Onie_Initialize_And_Version_Check  tianhe
	[Setup]  boot Into Onie Rescue Mode
	Step  1  get dhcp ip and ping server
    Step  2  check onie latest version

ONIE_TC_001_Install_ONIE_via_Flashcp_on_ONIE
    [Documentation]  This test checks the Installing ONIE via Flashcp on ONIE
    [Tags]  common  ONIE_TC_001_Install_ONIE_via_Flashcp_on_ONIE  tianhe
    [Timeout]  30 min 00 seconds
    [Setup]  boot Into Onie Rescue Mode
    Step  1  Check network connectivity and download ONIE file from TFTP server  ${ONIE_RESCUE_MODE}
    Step  2  get The Current Onie Partition Erase and install onie  ${ONIE_RESCUE_MODE}
    Step  3  Clear Onie File  ${ONIE_RESCUE_MODE}
    Step  4  power Cycle To Onie Install Mode
    Step  5  verify Onie Version

ONIE_TC_002_Install_ONIE_Nor_flash_by_TFTP_Test
    [Documentation]  This test checks the Installing ONIE via Flashcp on DiagOS
    [Tags]  common  ONIE_TC_002_Install_ONIE_Nor_flash_by_TFTP_Test  tianhe
    [Timeout]  30 min 00 seconds
    [Setup]  boot Into Uboot
    Step  1  set Uboot IP
    Step  2  install Onie Under Uboot
    Step  3  verify Onie Version

ONIE_TC_003_Install_ONIE_via_Flashcp_on_DiagOS
    [Documentation]  This test checks the Installing ONIE via Flashcp on DiagOS
    [Tags]  common  ONIE_TC_003_Install_ONIE_via_Flashcp_on_DiagOS  tianhe
    [Timeout]  60 min 00 seconds
    [Setup]  boot Into DiagOS Mode
    Step  1  get The Current Onie Partition And Erase  ${BOOT_MODE_DIAGOS}
    Step  2  check onie kernel image and boot to diagos  ${DIAG_BOOT_CMD}
    Step  3  get dhcp ip and ping server
    Step  4  Check network connectivity and download ONIE file from TFTP server  ${BOOT_MODE_DIAGOS}
    Step  5  flashcp Install Onie  ${display_onie_partition_cmd}  ${BOOT_MODE_DIAGOS}
    Step  6  Clear Onie File  ${BOOT_MODE_DIAGOS}
    Step  7  power Cycle To DiagOS
    Step  8  check onie version by system info tool  ${SYSTEM_INFO_TOOL}  ${SYSTEM_PATTERN}


ONIE_TC_004_ONIE_Update_via_Static_IP+TFTP
    [Documentation]  This test checks the Installing ONIE via Static IP+TFTP
    [Tags]  common  ONIE_TC_004_ONIE_Update_via_Static_IP+TFTP  tianhe
    [Timeout]  30 min 00 seconds
    [Setup]  boot Into Onie Rescue Mode
    Step  1  Set Static IP And Check network connectivity
    Step  2  onie self update test  new
    Step  3  verify Onie And CPLD Version

ONIE_TC_005_ONIE_Update_via_DHCP_IP+TFTP
    [Documentation]  This test checks the Installing ONIE via DHCP IP+TFTP
    [Tags]  common  ONIE_TC_005_ONIE_Update_via_DHCP_IP+TFTP  tianhe
    [Timeout]  60 min 00 seconds
    Step  1  fhv2 auto Update In Update Mode
    Step  2  verify Onie And CPLD Version  version=new

ONIE_TC_006_ONIE_Update_via_noforce_on_ONIE
    [Documentation]  This test is to verify onie self-update via static ip and tftp.
    [Tags]  common  ONIE_TC_006_ONIE_Update_via_noforce_on_ONIE  tianhe
    [Setup]  boot into Onie Rescue Mode
    Step  1  check network and ping dhcp server
    Step  2  onie Update Via No Force On ONIE  new
    Step  3  boot into Onie Rescue Mode
    Step  4  check onie all version  new
    Step  5  check network and ping dhcp server
    Step  6  onie Update Via No Force On ONIE  old
    Step  7  boot into Onie Rescue Mode
    Step  8  check onie all version  old
    Step  9  Onie Self Update  new

ONIE_TC_007_ONIE_Updat_via_image_self
    [Documentation]  The purpose of this test is to verify that ONIE can be updated via image self
    [Tags]  ONIE_TC_007_ONIE_Updat_via_image_self   tianhe  try
    [Timeout]  60 min 00 seconds
    [Setup]  boot Into Onie Rescue Mode
    Step  1  check onie latest version
    Step  2  check network and ping dhcp server
    Step  3  get file and update  old
    Step  4  check onie all version  old
    Step  5  check network and ping dhcp server
    Step  6  get file and update  new
    Step  7  check onie all version  new

ONIE_TC_008_ONIE_Update_via_image_self_noforce
    [Documentation]  This test is to verify that ONIE can be updated via ./
    [Tags]  ONIE_TC_008_ONIE_Update_via_image_self_noforce  tianhe
    [Setup]   boot into Onie Rescue Mode
    Step  1  check onie latest version
    Step  2  update onie and check cpld version  new
    Step  3  update onie and check cpld version  old
    Step  4  update onie and check cpld version  new

ONIE_TC_009_ONIE_Update_With_Current_Version
    [Documentation]  This test ensures that ONIE can be updated from current version to current version
    [Tags]  common  ONIE_TC_009_ONIE_Update_With_Current_Version  tianhe
    [Timeout]  60 min 00 seconds
    [Setup]  boot into Onie Rescue Mode
	Step  1  check onie latest version
    Step  2  Onie Update Current Version  ${onieCurrentImgCmd}
    Step  3  check onie current version

ONIE_TC_010_ONIE_Update_With_Higher_Version
    [Documentation]  This test ensures that ONIE can be updated from current version to higher version
    [Tags]  common  ONIE_TC_010_ONIE_Update_With_Higher_Version  tianhe
    [Timeout]  60 min 00 seconds
    [Setup]  boot into Onie Rescue Mode
	Step  1  check onie latest version
    Step  2  Onie Update Higher Version
    Step  3  check onie higher version
    Step  4  boot into Onie Rescue Mode
    Step  5  Onie Update Current Version  ${onieCurrentImgCmd}
    Step  6  check onie current version


ONIE_TC_011_ONIE_Update_With_Production_Version
    [Documentation]  This test ensures that ONIE can be updated from Production version to current version
    [Tags]  common  ONIE_TC_011_ONIE_Update_With_Production_Version  tianhe
    [Timeout]  60 min 00 seconds
    [Setup]  boot into Onie Rescue Mode
	Step  1  check onie latest version
    Step  2  Onie Update Production Version
    Step  3  check onie production version
    Step  4  boot into Onie Rescue Mode
    Step  5  Onie Update Current Version  ${onieCurrentImgCmd}
    Step  6  check onie current version

ONIE_TC_012_ONIE_Update_With_Customer_Version
    [Documentation]  This test ensures that ONIE can be updated from Customer version to current version
    [Tags]  common  ONIE_TC_012_ONIE_Update_With_Customer_Version  tianhe
    [Timeout]  60 min 00 seconds
    [Setup]  boot into Onie Rescue Mode
	Step  1  check onie latest version
    Step  2  Onie Update Customer Version
    Step  3  check onie customer version
    Step  4  boot into Onie Rescue Mode
    Step  5  Onie Update Current Version  ${onieCurrentImgCmd}
    Step  6  check onie current version

ONIE_TC_013_ONIE_NOS_Install_via_Static_IP_TFTP
    [Documentation]   This test is to verify that onie self-update via static ip and tftp
    [Tags]   ONIE_TC_013_ONIE_NOS_Install_via_Static_IP_TFTP   tianhe
    [Timeout]  15 min 00 seconds
    [Setup]  boot into ONIE install mode
    Step  1  Set Interface IP
    Step  2  Onie NOS Self Update
    Step  3  boot into DiagOS mode
    Step  4  Check DiagOS Ver

ONIE_TC_014_ONIE_NOS_Install_via_DHCP_IP_TFTP
    [Documentation]   This test is to verify that onie can be NOS installation via DHCP ip and TFTP server
    [Tags]   ONIE_TC_014_ONIE_NOS_Install_via_DHCP_IP_TFTP   tianhe
	[Setup]  boot into DiagOS mode
    Step  1  get dhcp ip and ping server
    Step  2  change the diagos image name  DIAGOS
	Step  3  onie auto update in install mode
    Step  4  Check DiagOS Ver
    [Teardown]  restore diagos image name  DIAGOS

ONIE_TC_015_ERASE_ONIE
    [Documentation]  This test checks ONIE can be erased
    [Tags]  common  ONIE_TC_015_ERASE_ONIE  tianhe
    [Timeout]  30 min 00 seconds
    [Setup]  boot Into Onie Rescue Mode
    Step  1  get The Current Onie Partition And Erase  ${ONIE_RESCUE_MODE}
    Step  2  reboot And Check Cannot Find Image
    [Teardown]  restore onie image in uboot mode

ONIE_TC_016_ONIE_Booting_Mode_Check
    [Documentation]  This test checks the each support ONIE mode can boot into OS successfully
    [Tags]  common  ONIE_TC_016_ONIE_Booting_Mode_Check  tianhe
    [Timeout]  20 min 00 seconds
    Step  1  Switch And Check Booting Onie Version  installer
    Step  2  Switch And Check Booting Onie Version  update
    Step  3  Switch And Check Booting Onie Version  rescue
    Step  4  switch To DiagOS

ONIE_TC_017_ONIE_System_Information
    [Documentation]  This test checks ONIE system information is correct
    [Tags]  common  ONIE_TC_017_ONIE_System_Information  tianhe
    [Timeout]  10 min 00 seconds
    [Setup]  boot Into Onie Install Mode
    Step  1  check Onie Sys Info
    Step  2  check Onie Sys Info V
    Step  3  check Onie Os Release
    Step  4  check psu info
    Step  5  check thermal info
    Step  6  check fan info
	Step  7  check tpm info  ${TPM_TOOL}  ${Tpm_Expect}
    Step  8  check onie initargs and bootargs  ${initargs_tool}  ${bootargs_tool}  ${initargs_res}  ${bootargs_res}

ONIE_TC_018_TLV_EEPROM_R/W_Test
    [Documentation]  This test checks TLV EEPROM can be read/write successfully in ONIE
    [Tags]  common  ONIE_TC_018_TLV_EEPROM_R/W_Test  tianhe
    [Timeout]  20 min 00 seconds
    [Setup]  boot into Onie Rescue Mode
    Step  1  read and backup tlv eeprom  ${ONIE_SYSEEPROM_CMD}
    Step  2  check eeprom wp status  ${ONIE_WP_ENBLE_VAL}  ${ONIE_WP_CMD}
    Step  3  check store tlv system eeprom  ${server_tmp_file}
    Step  4  write tlv system eeprom  ${ONIE_SYSEEPROM_TEST_DICT}  ${ONIE_WRITE_WP_CMD}
    Step  5  power cycle unit to rescue mode
    Step  6  read and check tlv test eeprom value  ${ONIE_SYSEEPROM_CMD}  ${ONIE_SYSEEPROM_TEST_DICT}
    [Teardown]  restore original tlv eeprom value  ${server_tmp_file}  ${ONIE_WRITE_WP_CMD}

ONIE_TC_019_Auto_Discovery_Rescue_Mode
    [Documentation]  This test checks the system can enter ONIE rescue mode
    [Tags]  common  ONIE_TC_019_Auto_Discovery_Rescue Mode  tianhe
    [Timeout]  10 min 00 seconds
	Step  1  check onie rescue booting mode
    Step  2  Check network connectivity  ${ONIE_RESCUE_MODE}
    Step  3  check Onie Tlv Value Existed

ONIE_TC_020_CPLD/FPGA_Updates
    [Documentation]  This test checks that CPLD can be updated under ONIE mode
    [Tags]  common  ONIE_TC_020_CPLD/FPGA_Updates  tianhe
    [Timeout]  20 min 00 seconds
    Step  1  boot Into Onie Rescue Mode
    Step  2  Check network connectivity  ${ONIE_RESCUE_MODE}
    Step  3  tftp download image file  ${localCpldPath}  ${cpldNewImgPathLst}
    Step  4  tianhe upgrade cpld  ${vmetool}  ${cpldOptionLst}  ${cpldNewImgLst}
    Step  5  power Cycle To Onie Rescue Mode
    Step  6  check Cpld Version
    [Teardown]  delete image file  ${localCpldPath}  ${cpldNewImgLst}

ONIE_TC_021_1pps_Accelerator_FPGA_Update_Test
    [Documentation]  This test checks FPGA update
    [Tags]  common  ONIE_TC_021_1pps_Accelerator_FPGA_Update_Test  tianhe
    [Timeout]  15 min 00 seconds
    [Setup]  boot Into Onie Rescue Mode
    Step  1  Check network connectivity  ${ONIE_RESCUE_MODE}
    Step  2  tftp download image file  ${localFpgaPath}  ${ppsFpgaNewPathLst}
    Step  3  pps fpga upgrade test  ${fpgaFwTool}  ${fpgaOption}  ${ppsFpgaNewImg}
    Step  4  cat i2c version
    Step  5  power Cycle To Onie Rescue Mode
    Step  6  cat i2c version
    [Teardown]  delete image file  ${localFpgaPath}  ${ppsFpgaNewImg}


ONIE_TC_022_Startup_Sdk_Shell
    [Documentation]  This test checks the system can startup sdk shell
    [Tags]  common  ONIE_TC_022_Startup_Sdk_Shell  tianhe
    [Timeout]  10 min 00 seconds
    [Setup]  boot Into Onie Rescue Mode
    Step  1  Load Sdk Shell
    BuiltIn.Sleep  300  #WORKAROUND, as the proposal of wubin we set this delay, otherwise some port can't up!!!!
    Step  2  Check Port Links Status
    [Teardown]  Exit Sdk Shell

ONIE_TC_023_Telnet_Access
    [Documentation]  This test checks the ONIE supporting telnet access without password
    [Tags]  common  ONIE_TC_023_Telnet_Access  tianhe
    [Timeout]  5 min 00 seconds
    [Setup]  boot Into Onie Install Mode
	Step  1  get dhcp ip and ping server
	Step  2  uut via telnet login onie from server side
#Step  2  check Onie Telnet

ONIE_TC_024_SSH_Access
    [Documentation]  This test checks the ONIE supporting SSH access without password
    [Tags]  common  ONIE_TC_024_SSH_Access  tianhe
    [Setup]  boot Into Onie Rescue Mode
	Step  1  get dhcp ip and ping server
    Step  2  ssh dhcp connect from onie side
    Step  3  ssh dut connect from server side


ONIE_TC_025_Serial_Console_Access
    [Documentation]  This test checks the system can enter and verify ONIE boot mode successfully
    [Tags]  common  ONIE_TC_025_Serial_Console_Access  tianhe
    [Timeout]  5 min 00 seconds
    [Setup]  boot Into Onie Install Mode
    Step  1  verify onie install mode works

ONIE_TC_026_ONIE_Diag_OS_recovery_Test
    [Documentation]  This test checks that Diag os can be recoveried via ONIE
    [Tags]  common  ONIE_TC_026_ONIE_Diag_OS_recovery_Test  tianhe
    [Timeout]  20 min 00 seconds
    Step  1  boot Into Onie Rescue Mode
    Step  2  Check network connectivity  ${ONIE_RESCUE_MODE}
    Step  3  format Disk
    Step  4  try To Access DiagOS
    Step  5  fhv2 download Images And Recovery DiagOS
    Step  6  power Cycle To DiagOS

ONIE_TC_027_File_system_ext3/ext4_Supports
    [Documentation]  This test checks that ONIE will support file system type ext3 and ext4
    [Tags]  common  ONIE_TC_027_File_system_ext3/ext4_Supports  tianhe
    [Timeout]  20 min 00 seconds
    Step  1  boot Into Onie Rescue Mode
    Step  2  delete Partion
    Step  3  create Partion
    Step  4  test Format Disk With ext3/ext4  /dev/sda5

ONIE_TC_028_File_System_Utilities_Test
    [Documentation]  This test checks that onie file system utilities
    [Tags]  common  ONIE_TC_028_File_System_Utilities_Test  tianhe
    [Timeout]  20 min 00 seconds
    Step  1  boot Into Onie Rescue Mode
    Step  2  check File System Utilities

ONIE_TC_029_Default_file_Name_Search_Order
    [Documentation]  This test checks the ONIE will automatically search filename
    [Tags]  common  ONIE_TC_029_Default_file_Name_Search_Order  tianhe
    [Timeout]  30 min 00 seconds
	Step  1  rename onie image  DIAGOS  toBackup=${TRUE}
    Step  2  check File Search Order  installer  ${INSTALLER_FILE_SEARCH_ORDER}
    Step  3  rename onie image  DIAGOS  toBackup=${FALSE}
    Step  4  rename onie image  ONIE_updater  toBackup=${TRUE}
    Step  5  check File Search Order  update  ${UPDATER_FILE_SEARCH_ORDER}
	Step  6  check onie rescue booting mode
    [Teardown]  rename onie image  ONIE_updater  toBackup=${FALSE}

ONIE_TC_030_Installer_Discovery_Methods
    [Documentation]  This test checks the ONIE can locate the installer through a number of discovery methods
    [Tags]  common  ONIE_TC_030_Installer_Discovery_Methods  tianhe
    [Timeout]  20 min 00 seconds
    [Setup]  boot Into Onie Install Mode
    Step  1  installer Discovery Check

ONIE_TC_031_Uboot_Environment_Access
    [Documentation]  This test checks that uboot environment access
    [Tags]  common  ONIE_TC_031_Uboot_Environment_Access  tianhe
    [Timeout]  20 min 00 seconds
	Step  1  boot Into Onie Rescue Mode
    Step  2  onie Ifconfig Eth0
    Step  3  boot Into Uboot
    Step  4  set Eth1 Addr
    Step  5  boot Into Onie Rescue Mode
    Step  6  compare onie mac address in rescue mode  ${envTool}  ${setenvaddr}
    Step  7  add Test Parameters  1
    Step  8  add Test Parameters  2
    Step  9  add Test Parameters  3
    Step  10  add Test Parameters  4
    Step  11  boot Into Uboot
    Step  12  check some test parameters in uboot mode  ${ubootEnvTool}  ${testEnvLst}
    Step  13  restore Uboot Env

ONIE_TC_032_SSD_Device_Health_Status
    [Documentation]  This test checks that ONIE will support checking SSD device health
    [Tags]  common  ONIE_TC_032_SSD_Device_Health_Status  tianhe
    [Timeout]  5 min 00 seconds
    [Setup]  boot Into Onie Install Mode
    Step  1  check Ssd Health

ONIE_TC_033_FSC_Check_Test
    [Documentation]  This test checks that ONIE will support FSC function
    [Tags]  common  ONIE_TC_033_FSC_Check_Test  tianhe
    [Timeout]  10 min 00 seconds
    [Setup]  boot Into Onie Install Mode
    ${fanspeed}=  KapokOnieLib.get fan speed percent
    Step  1  check Fsc Code
    Step  2  check Fan Speed  ${fanspeed}
    Step  3  check Fan Ctrl

ONIE_TC_034_QSFP_Access_Test
    [Documentation]  This test checks that ONIE can access QSFP via i2c interface
    [Tags]  common  ONIE_TC_034_QSFP_Access_Test  tianhe
    [Timeout]  5 min 00 seconds
    [Setup]  boot Into Onie Install Mode
    Step  1  fenghuangv2 check Qsfp Access

ONIE_TC_035_Check_Driver_Information_in_ONIE
    [Documentation]  This test checks that driver works normal in ONIE
    [Tags]  common  ONIE_TC_035_Check_Driver_Information_in_ONIE  tianhe
    [Timeout]  20 min 00 seconds
    Step  1  check driver information test  ${onieUbootMode}  ${onieDriveTool}  ${onieInstallDrivePattern}
    Step  2  check driver information test  ${onieToUpdateMode}  ${onieDriveTool}  ${onieUpdateDrivePattern}
    Step  3  check driver information test  ${onieToRescueMode}  ${onieDriveTool}  ${onieUpdateDrivePattern}

ONIE_TC_036_Check_onie_Platform_Information_in_uboot
    [Documentation]  This test checks whether onie_platform value in uboot is correct
    [Tags]  common  ONIE_TC_036_Check_onie_Platform_Information_in_uboot  tianhe
    [Timeout]  20 min 00 seconds
    [Setup]  boot Into Uboot
    Step  1  check platform info
    Step  2  check sys eeprom

ONIE_TC_037_FPP_Modes_Test
    [Documentation]  This test checks that the onie_fpp uboot env variable setting is valid
    [Tags]  common  ONIE_TC_037_FPP_Modes_Test  tianhe
    [Timeout]  50 min 00 seconds
    FOR  ${PORT_MODE}  IN  @{FPP_MODES}
        Step  1  check Fpp Mode  ${PORT_MODE}
    END
    [Teardown]  restore Fpp Mode

ONIE_TC_038_Integrator_Mode_Test
    [Documentation]  This test checks that could access integrator mode and set port status
    [Tags]  common  ONIE_TC_038_Integrator_Mode_Test  tianhe
    [Timeout]  20 min 00 seconds
    [Setup]  boot Into Onie Install Mode
	Step  1  quit Sdk Shell
    FOR  ${PORT_MODE}  IN  @{INTEGRATOR_TEST_MODES}
        Step  2  verify Can Access Integrator Mode  ${PORT_MODE}
        Step  3  enable Some Port And Verify Port Enable  1  32  ${PORT_MODE}
    END

ONIE_TC_039_SFP_Test
    [Documentation]  This test checks detecting sfp type
    [Tags]  common  ONIE_TC_039_SFP_Test  tianhe
    [Timeout]  10 min 00 seconds
	[Setup]  boot Into Onie Install Mode
    Step  1  check Qsfp Type
    Step  2  check Qsfp Manufacture Info
    Step  3  check and reset sfp eeprom  ${sfp_tool}
    Step  4  read and write aws eeprom  ${sfp_tool}  ${stp_value_pattern}  ${stp_test_value_pattern}  ${enable_lpmode_option}

#ONIE_TC_040_ONIE_Updater_Stress_Test
#    [Documentation]  This test checks the ONIE Updater Stress Test
#    [Tags]  common  ONIE_TC_040_ONIE_Updater_Stress_Test  tianhe
#    [Timeout]  180 min 00 seconds
#    FOR  ${CYCLE}  IN RANGE  0  4
#        Step  1  boot into Onie Rescue mode
#        Step  2  check eth0 ip and onie version  new
#        Step  3  Onie Self Update  old
#        Step  4  check FW version  old
#        Step  5  boot into Onie Rescue mode
#        Step  6  check eth0 ip and onie version  old
#        Step  7  Onie Self Update  new
#        Step  8  check FW version  new
#    END

*** Keywords ***
Onie Connect Device
    OnieConnect

Onie Disconnect Device
    OnieDisconnect
