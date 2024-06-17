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
# Script       : minipack3_bsp.robot                                                                                  #
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
BSP_TC_001_BSP_Structure_of_FBOSS
    [Documentation]  check file structure of BSP in FBOSS
    [Tags]     common  BSP_TC_001_BSP_Structure_of_FBOSS  minipack3  batch1
    Step  1  check kernel version
    Step  2  check Diag Os version
    Step  3  check BSP Structure

BSP_TC_002_BSP_Driver_Install_Uninstall_Test
    [Documentation]  bsp driver install & uninstall test
    [Tags]     common  BSP_TC_002_BSP_Driver_Install_Uninstall_Test  minipack3  batch2
    Step  1  verify bsp version  DUT  ${bsp_ver2}
    Step  2  downgrade bsp  DUT
    Independent Step  3  verify bsp version  DUT  ${bsp_ver1}
    Step  4  upgrade bsp  DUT
    Step  5  verify bsp version  DUT  ${bsp_ver2}

BSP_TC_003_Online_update_CPLD_in_FBOSS
    [Documentation]  test upgrade or downgrade MCB SCM SMB CPLD
    [Tags]     common  BSP_TC_003_Online_update_CPLD_in_FBOSS  minipack3  batch1
    [Timeout]  30 min 00 seconds
    [Setup]    download cpld images
    Independent Step  1  verify cpld version  DUT  ${cpld_ver2}
    Independent Step  2  downgrade cpld  DUT
    Independent Step  3  verify cpld version  DUT  ${cpld_ver1}
    Independent Step  4  upgrade cpld  DUT
    Independent Step  5  verify cpld version  DUT  ${cpld_ver2}
    sleep  10s
    [Teardown]  clean cpld images

BSP_TC_004_Online_Update_DOM1_FPGA_In_FBOSS
    [Documentation]  test upgrade or downgrade DOM1 FPGA
    [Tags]     common  BSP_TC_004_Online_Update_DOM1_FPGA_In_FBOSS  minipack3  batch1
    [Timeout]  30 min 00 seconds
    [Setup]    download images  DUT  FPGA
    Step  1  verify firmware version  DUT  dom1  ${dom1_ver2}
    Step  2  downgrade fpga  dom1
    Step  3  verify firmware version  DUT  dom1  ${dom1_ver1}
    Step  4  upgrade fpga  dom1
    Step  5  verify firmware version  DUT  dom1  ${dom1_ver2}
    sleep  10s
    [Teardown]  clean images  DUT  FPGA

BSP_TC_005_Online_Update_DOM2_FPGA_In_FBOSS
    [Documentation]  test upgrade or downgrade DOM2 FPGA
    [Tags]     common  BSP_TC_005_Online_Update_DOM2_FPGA_In_FBOSS  minipack3  batch1
    [Timeout]  30 min 00 seconds
    [Setup]    download images  DUT  FPGA
    Step  1  verify firmware version  DUT  dom2  ${dom2_ver2}
    Step  2  downgrade fpga  dom2
    Step  3  verify firmware version  DUT  dom2  ${dom2_ver1}
    Step  4  upgrade fpga  dom2
    Step  5  verify firmware version  DUT  dom2  ${dom2_ver2}
    sleep  10s
    [Teardown]  clean images  DUT  FPGA

BSP_TC_006_Online_Update_IOB_FPGA_In_FBOSS
    [Documentation]  test upgrade or downgrade IOB FPGA
    [Tags]     common  BSP_TC_006_Online_Update_IOB_FPGA_In_FBOSS  minipack3  batch1
    [Timeout]  30 min 00 seconds
    [Setup]    download images  DUT  IOB
    Step  1  verify firmware version  DUT  iob  ${iob_ver2}
    Step  2  downgrade fpga  iob
    Step  3  verify firmware version  DUT  iob  ${iob_ver1}
    Step  4  upgrade fpga  iob
    Step  5  verify firmware version  DUT  iob  ${iob_ver2}
    [Teardown]  clean images  DUT  IOB

BSP_TC_008_Online_Update_OOB_Switch_FW_in_FBOSS
    [Documentation]  test upgrade or downgrade OOB Switch firmware
    [Tags]     common  BSP_TC_008_Online_Update_OOB_Switch_FW_in_FBOSS  minipack3  batch1   
    [Timeout]  30 min 00 seconds
    [Setup]    make oob firmware writable
    Step  1  verify eeprom readable  DUT  OOB
    Step  2  update oob switch firmware
    Step  3  verify eeprom readable  DUT  OOB
    Step  4  ping bmc ipv6 address
    [Teardown]  clean oob firmware images

BSP_TC_009_Online_Update_TH5_PCIE_FW_in_FBOSS
    [Documentation]  test upgrade or downgrade TH5 PCIE FW
    [Tags]     common  BSP_TC_009_Online_Update_TH5_PCIE_FW_in_FBOSS  minipack3  batch1
    [Timeout]  30 min 00 seconds
    [Setup]    download images  DUT  TH5
    Step  1  verify th5 version  DUT  ${th5_version}
    Step  2  upgrade firmware  th5
    Step  3  verify th5 version  DUT  ${th5_version}
    [Teardown]  clean images  DUT  TH5

BSP_TC_010_I2C_Devices_Test_in_FBOSS
    [Documentation]  scan and check all i2c devices informations,values,etc
    [Tags]     common  BSP_TC_010_I2C_Devices_Test_in_FBOSS  minipack3  batch1
    [Timeout]  30 min 00 seconds
    FOR    ${INDEX}    IN RANGE    1    4
        Independent Step  1  verify i2scan
        Independent Step  2  verify cpld read write  DUT  mcb
        Step  3  disable write protect  DUT  88E6321_EEPROM
        Step  4  enable write protect  DUT  88E6321_EEPROM
    END

BSP_TC_012_Fan_Speed_Manual_Control
    [Documentation]  R/W Register of PWM: fan speed get/set test
    [Tags]     common  BSP_TC_012_Fan_Speed_Manual_Control  minipack3  batch1
    [Timeout]  30 min 00 seconds
    Independent Step  1  set and get fan speed  10
    Independent Step  2  set and get fan speed  20
    Independent Step  3  set and get fan speed  50
    Independent Step  4  set and get fan speed  70
    Independent Step  5  set and get fan speed  80
    Independent Step  6  set and get fan speed  100
    [Teardown]  set and get fan speed  34

BSP_TC_013_GPIO_Controller_Test
    [Documentation]  GPIO test including gpiodetect/gpioinfo/gpioset/gpioget,etc
    [Tags]     common  BSP_TC_013_GPIO_Controller_Test  minipack3  batch1
    [Timeout]  30 min 00 seconds
    Step  1  print gpio controllers and lines
    #Step  2  set and get gpio lines
    FOR    ${INDEX}    IN RANGE    1    4
        Step  3  unload and reload gpio driver
        Step  4  print gpio controllers and lines
    END
    [Teardown]  load gpio driver  DUT  False

BSP_TC_014_SPI_Controller_Driver_Test 
    [Documentation]  spi controller driver test
    [Tags]     common  BSP_TC_014_SPI_Controller_Driver_Test  minipack3  batch1
    [Timeout]  30 min 00 seconds
    [Setup]    spi driver override  DUT
    Step  1  spi driver bind  DUT
    Step  2  spi driver unbind  DUT
    [Teardown]  spi driver bind  DUT

BSP_TC_016_SCM_EEPROM_R/W_Test
    [Documentation]  This test verifies SCM EEPROM could be R/W successfully
    [Tags]     common  BSP_TC_016_SCM_EEPROM_R/W_Test  minipack3  batch1
    [Timeout]  30 min 00 seconds
    [Setup]   store eeprom  SCM
    Step  1  verify eeprom content  SCM  ${eeprom_path}
    Step  2  write eeprom data  SCM  ${scm_eeprom_modified}
    Step  3  verify eeprom content  SCM  ${scm_eeprom_modified}
    Step  4  power reset chassis  DUT
    Step  5  verify eeprom content  SCM  ${scm_eeprom_modified}
    [Teardown]  restore eeprom  SCM

BSP_TC_017_SMB_EEPROM_R/W_Test
    [Documentation]  This test verifies SMB EEPROM could be R/W successfully
    [Tags]     common  BSP_TC_017_SMB_EEPROM_R/W_Test  minipack3  batch1
    [Timeout]  30 min 00 seconds
    [Setup]    store eeprom  SMB
    Step  1  verify eeprom content  SMB  ${eeprom_path}
    Step  2  write eeprom data  SMB  ${smb_eeprom_modified}
    Step  3  verify eeprom content  SMB  ${smb_eeprom_modified}
    Step  4  power reset chassis  DUT
    Step  5  verify eeprom content  SMB  ${smb_eeprom_modified}
    [Teardown]  restore eeprom  SMB

BSP_TC_018_FCB_EEPROM_R/W_Test
    [Documentation]  This test verifies FCB EEPROM could be R/W successfully
    [Tags]     common  BSP_TC_018_FCB_EEPROM_R/W_Test  minipack3  batch2
    [Timeout]  30 min 00 seconds
    [Setup]   make eeprom ready  FCB
    Step  1  verify eeprom content  FCB  ${eeprom_path}
    Step  2  write eeprom data  FCB  ${fcb_eeprom_modified}
    Step  3  verify eeprom content  FCB  ${fcb_eeprom_modified}
    Step  4  power reset chassis  DUT
    Step  5  verify eeprom content  FCB  ${fcb_eeprom_modified}
    [Teardown]  restore eeprom state  FCB

BSP_TC_020_MCB_EEPROM_R/W_Test
    [Documentation]  This test verifies MCB EEPROM could be R/W successfully
    [Tags]     common  BSP_TC_020_MCB_EEPROM_R/W_Test  minipack3  batch1
    [Timeout]  30 min 00 seconds
    [Setup]   make eeprom ready  MCB
    Step  1  verify eeprom content  MCB  ${eeprom_path}
    Step  2  write eeprom data  MCB  ${mcb_eeprom_modified}
    Step  3  verify eeprom content  MCB  ${mcb_eeprom_modified}
    Step  4  power reset chassis  DUT
    Step  5  verify eeprom content  MCB  ${mcb_eeprom_modified}
    [Teardown]  restore eeprom state  MCB

BSP_TC_021_weutil_Test
    [Documentation]  check all support FRU ID EEPROMS
    [Tags]     common  BSP_TC_021_weutil_Test  minipack3  batch2
    [Timeout]  30 min 00 seconds
    [Setup]    copy weutil files and make eeprom ready
    FOR    ${INDEX}    IN RANGE    1    4
        Step  1  verify weutil eeprom output  DUT  SCM  ${scm_eeprom_modified}
        Step  2  verify weutil eeprom output  DUT  SMB  ${smb_eeprom_modified}
        Step  3  verify weutil eeprom output  DUT  MCB  ${mcb_eeprom_modified}
    END
    [Teardown]  restore eeprom data and state

BSP_TC_022_Version_Utility_Test
    [Documentation]  version check by version utility
    [Tags]     common  BSP_TC_022_Version_Utility_Test  minipack3  batch1
    [Timeout]  30 min 00 seconds
    Independent Step  1  flashrom version check  DUT
    Independent Step  2  ddtool version check  DUT
    Independent Step  3  verify system version  DUT

BSP_TC_024_CPLD_Register_R/W_Test
    [Documentation]  CPLD Reisger R/W test including SCM/SMB/MCB,etc
    [Tags]     common  BSP_TC_024_CPLD_Register_R/W_Test  minipack3  batch1
    [Timeout]  30 min 00 seconds
    Independent Step  1  verify cpld read write  DUT  mcb
    Independent Step  2  verify cpld read write  DUT  scm
    Independent Step  2  verify cpld read write  DUT  smb

*** Keywords ***
Diag Connect Device
    Diag Connect
    #download images  DUT  BSP
    #copy bsp package files  DUT

Diag Disconnect Device
    Diag Disconnect

