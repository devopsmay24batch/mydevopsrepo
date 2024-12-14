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
# Script       : minerva_bsp.robot                                                                                  #
# Date         : XXXXXXXXX X, 2024                                                                                    #
# Author       : Ishwariya Vetrivel <ivetrivel@celestica.com>                                                               #
# Description  : This script will validate bsp                                                                    #
#                                                                                                                     #
# Script Revision Details:                                                                                            #
#   Initial Draft for openbmc testing                                                                                 #
#######################################################################################################################

*** Settings ***
Documentation       Tests to verify BSP functions described in the BSP function SPEC for the project Minipack3.

# Force Tags        bsp
Library           bsp_lib.py
Variables         bsp_variable.py
Resource          bsp_keywords.robot
Resource          CommonResource.robot


Suite Setup       Diag Connect Device
Suite Teardown    Diag Disconnect Device


*** Test Cases ***
Meta_Minerva_BSP_TC_001_BSP_Driver_Install_Uninstall_Test
    [Documentation]  bsp driver install & uninstall test
    [Tags]     common  Meta_Minerva_BSP_TC_001_BSP_Driver_Install_Uninstall_Test  batch2
    Step  1  verify bsp version  DUT  ${bsp_ver2}
    Step  2  downgrade bsp  DUT
    Independent Step  3  verify bsp version  DUT  ${bsp_ver1}
    Step  4  upgrade bsp  DUT
    Step  5  verify bsp version  DUT  ${bsp_ver2}
	
Meta_Minerva_BSP_TC_002_Structure_of_BSP_Package
    [Documentation]  check file structure of BSP in FBOSS
    [Tags]     common  Meta_Minerva_BSP_TC_002_Structure_of_BSP_Package  minerva  batch1
    Step  1  check kernel version
    Step  2  check Diag Os version
    Step  3  check BSP Structure

Meta_Minerva_BSP_TC_003_Online_Update_SMB_CPLD_1_2_In_Diag_OS
    [Documentation]  test upgrade or downgrade SMB CPLD
    [Tags]     common  Meta_Minerva_BSP_TC_003_Online_Update_SMB_CPLD_1_2_In_Diag_OS  minerva  batch1
    [Timeout]  30 min 00 seconds
    [Setup]    download smb cpld images
    Independent Step  1  verify smb cpld version  DUT  ${cpld1_ver2}  ${cpld2_ver2}
    Independent Step  2  downgrade smb cpld  DUT
    Independent Step  3  verify smb cpld version  DUT  ${cpld1_ver1}  ${cpld2_ver1}
    Independent Step  4  upgrade smb cpld  DUT
    Independent Step  5  verify smb cpld version  DUT  ${cpld1_ver2}  ${cpld2_ver2}
    [Teardown]  clean smb cpld images

Meta_Minerva_BSP_TC_004_Online_Update_PWR_CPLD_In_Diag_OS
    [Documentation]  test upgrade or downgrade pwr cpld
    [Tags]     common  Meta_Minerva_BSP_TC_004_Online_Update_PWR_CPLD_In_Diag_OS  minerva  batch2
    [Timeout]  30 min 00 seconds
    [Setup]    download images  DUT  PWR
    Step  1  verify firmware version  DUT  pwr  ${pwr_ver2}
    Step  2  downgrade pwr cpld  DUT
    Step  3  verify firmware version  DUT  pwr  ${pwr_ver1}
    Step  4  upgrade pwr cpld  DUT
    Step  5  verify firmware version  DUT  pwr  ${pwr_ver2}
    [Teardown]  clean images  DUT  PWR

Meta_Minerva_BSP_TC_005_Online_Update_DOM_FPGA_In_Diag_OS
    [Documentation]  test upgrade or downgrade DOM FPGA
    [Tags]     common  Meta_Minerva_BSP_TC_005_Online_Update_DOM_FPGA_In_Diag_OS  minerva  batch1
    [Timeout]  30 min 00 seconds
    [Setup]    download images  DUT  FPGA
    Step  1  verify firmware version  DUT  dom  ${dom_ver2}
    Step  2  downgrade fpga  dom
    Step  3  verify firmware version  DUT  dom  ${dom_ver1}
    Step  4  upgrade fpga  dom
    Step  5  verify firmware version  DUT  dom  ${dom_ver2}
    [Teardown]  clean images  DUT  FPGA

Meta_Minerva_BSP_TC_006_Online_Update_IOB_FPGA_In_Diag_OS
    [Documentation]  test upgrade or downgrade IOB FPGA
    [Tags]     common  Meta_Minerva_BSP_TC_006_Online_Update_IOB_FPGA_In_Diag_OS  minerva  batch1
    [Timeout]  30 min 00 seconds
    [Setup]    download images  DUT  IOB
    Step  1  verify firmware version  DUT  iob  ${iob_ver2}
    Step  2  downgrade fpga  iob
    Step  3  verify firmware version  DUT  iob  ${iob_ver1}
    Step  4  upgrade fpga  iob
    Step  5  verify firmware version  DUT  iob  ${iob_ver2}
    [Teardown]  clean images  DUT  IOB

Meta_Minerva_BSP_TC_007_Online_Update_OOB_Switch_FW_In_Diag_OS
    [Documentation]  test upgrade or downgrade OOB Switch firmware
    [Tags]     common  Meta_Minerva_BSP_TC_007_Online_Update_OOB_Switch_FW_In_Diag_OS  minerva  batch2
    [Timeout]  30 min 00 seconds
    [Setup]    make oob firmware writable
    Step  1  verify eeprom content  DUT  OOB
    Step  2  update oob switch firmware
    Step  3  verify eeprom content  DUT  OOB
    Step  4  ping bmc ipv6 address
    [Teardown]  clean oob firmware images

Meta_Minerva_BSP_TC_008_Online_Update_TH5_FW_In_Diag_OS
    [Documentation]  test upgrade or downgrade TH5 PCIE FW
    [Tags]     common  Meta_Minerva_BSP_TC_008_Online_Update_TH5_FW_In_Diag_OS  minerva  batch1
    [Timeout]  30 min 00 seconds
    [Setup]    download images  DUT  TH5
    Step  1  verify th5 version  DUT  ${th5_version}
    Step  2  upgrade firmware  th5
    Step  3  verify th5 version  DUT  ${th5_version}
    [Teardown]  clean images  DUT  TH5

BSP_TC_010_I2C_Devices_Test_in_FBOSS
    [Documentation]  scan and check all i2c devices informations,values,etc
    [Tags]     common  BSP_TC_010_I2C_Devices_Test_in_FBOSS  minerva  batch1
    [Timeout]  30 min 00 seconds
    FOR    ${INDEX}    IN RANGE    1    4
        Independent Step  1  verify i2scan
        Independent Step  2  verify cpld read write  DUT  smb1
        Independent Step  3  disable write protect  DUT  TH5_EEPROM
        Independent Step  4  enable write protect  DUT  TH5_EEPROM
    END

Meta_Minerva_BSP_TC_010_Power_Control
    [Documentation]  Power cycle DUT by set pwr cpld register
    [Tags]     common  Meta_Minerva_BSP_TC_010_Power_Control  minerva  batch1
    [Timeout]  30 min 00 seconds
    Step  1  power cycle by pwr cpld
   
Meta_Minerva_BSP_TC_015_GPIO_Controller_Test
    [Documentation]  GPIO test including gpiodetect/gpioinfo/gpioset/gpioget,etc
    [Tags]     common  Meta_Minerva_BSP_TC_015_GPIO_Controller_Test  minerva  batch1
    [Timeout]  30 min 00 seconds
    Step  1  print gpio controllers and lines
    #Step  2  set and get gpio lines
    FOR    ${INDEX}    IN RANGE    1    4
        Step  3  unload and reload gpio driver
        Step  4  print gpio controllers and lines
    END
    [Teardown]  load gpio driver  DUT  False

Meta_Minerva_BSP_TC_016_COMe_Board_EEPROM_R/W_Test
    [Documentation]  This test verifies COMe Board EEPROM could be R/W successfully
    [Tags]     common  Meta_Minerva_BSP_TC_016_COMe_Board_EEPROM_R/W_Test  minerva  batch1
    [Timeout]  30 min 00 seconds    
    [Setup]    store eeprom  COME
    Step  1  verify eeprom content  COME  ${eeprom_path}
    Step  2  write eeprom data  COME  ${come_eeprom_modified}
    Step  3  verify eeprom content  COME  ${come_eeprom_modified}
    Step  4  reboot come  DUT
    Step  5  disable write protect  DUT  COME_EEPROM
    Step  6  verify eeprom content  COME  ${come_eeprom_modified}
    Step  7  power reset chassis  DUT
    Step  8  disable write protect  DUT  COME_EEPROM
    Step  9  verify eeprom content  COME  ${come_eeprom_modified}    
    [Teardown]  restore eeprom   COME

Meta_Minerva_BSP_TC_017_SMB_EEPROM_R/W_Test
    [Documentation]  This test verifies SMB EEPROM could be R/W successfully
    [Tags]     common  Meta_Minerva_BSP_TC_017_SMB_EEPROM_R/W_Test  minerva  batch1
    [Timeout]  30 min 00 seconds
    [Setup]   make eeprom ready  SMB
    Step  1  verify eeprom content  SMB  ${eeprom_path}
    Step  2  write eeprom data  SMB  ${smb_eeprom_modified}
    Step  3  verify eeprom content  SMB  ${smb_eeprom_modified}
    Step  4  reboot come  DUT
    Step  5  disable write protect  DUT  SMB_EEPROM
    Step  6  verify eeprom content  SMB  ${smb_eeprom_modified}
    Step  7  power reset chassis  DUT
    Step  8  disable write protect  DUT  SMB_EEPROM
    Step  9  verify eeprom content  SMB  ${smb_eeprom_modified}
    [Teardown]  restore eeprom state  SMB

Meta_Minerva_BSP_TC_018_weutil_Test
    [Documentation]  check all support FRU ID EEPROMS
    [Tags]     common  Meta_Minerva_BSP_TC_018_weutil_Test  batch2
    [Timeout]  30 min 00 seconds
    [Setup]    copy weutil files and make eeprom ready
    FOR    ${INDEX}    IN RANGE    1    4
        Step  1  verify weutil eeprom output  SMB  ${smb_eeprom_modified}
        Step  2  verify weutil eeprom output  DUT  COME  ${come_eeprom_modified}
    END
    [Teardown]  restore eeprom data and state

Meta_Minerva_BSP_TC_019_SPI_Controller_Driver_Test 
    [Documentation]  spi controller driver test
    [Tags]     common  Meta_Minerva_BSP_TC_019_SPI_Controller_Driver_Test  minerva  batch1
    [Timeout]  30 min 00 seconds
    [Setup]    spi driver override  DUT
    Step  1  spi driver bind  DUT
    Step  2  spi driver unbind  DUT
    [Teardown]  spi driver bind  DUT
	
Meta_Minerva_BSP_TC_020_Version_Utility_Test
    [Documentation]  version check by version utility
    [Tags]     common  Meta_Minerva_BSP_TC_020_Version_Utility_Test  minipack3  batch1  minerva
    [Timeout]  30 min 00 seconds
    Independent Step  1  flashrom version check  DUT
    Independent Step  2  ddtool version check  DUT
    Independent Step  3  verify system version  DUT

Meta_Minerva_BSP_TC_022_CPLD_Register_R/W_Test
    [Documentation]  CPLD Reisger R/W test including SCM/SMB/MCB,etc
    [Tags]     common  Meta_Minerva_BSP_TC_022_CPLD_Register_R/W_Test  minerva  batch1
    [Timeout]  30 min 00 seconds
    Independent Step  1  verify cpld read write  DUT  smb1
    Independent Step  2  verify cpld read write  DUT  smb2
    Independent Step  2  verify cpld read write  DUT  pwr


*** Keywords ***
Diag Connect Device
    Diag Connect
    #download images  DUT  BSP
    #copy bsp package files  DUT

Diag Disconnect Device
    Diag Disconnect

