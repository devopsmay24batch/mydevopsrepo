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

*** Settings ***
Documentation       Tests to verify BIOS functions described in the BIOS function SPEC for the whiteboxproject.

Variables         BIOS_variable.py

Library           ../WhiteboxLibAdapter.py
Library           whitebox_lib.py
#Library           common_lib.py
Library           bios_menu_lib.py
Library           openbmc_lib.py
Library           bios_lib.py

Resource          BIOS_keywords.robot
Resource          CommonResource.robot

#Suite Setup       OS Connect Device
#Suite Teardown    OS Disconnect Device

** Variables ***
# It is recommended to use <{ScriptName}|{FeatureName}|{DomainName}_Variable> file for variable declaration with help of
# setting table. This section should keep blank.
#In extreme case if script requires variable then it should be defined in this table with documentaiton tag

# -- Important --
# It is required to set default BIOS Password if not already set to run the below test-cases
# except for CONSR-BIOS-BSST-0012-0001 

*** Test Cases ***

CONSR-BIOS-BSUP-0002-0001
   [Documentation]   BIOS_002_Flash utility for BIOS update under Linux
   [Tags]   CONSR-BIOS-BSUP-0002-0001   Athena-G2
   Step  1   prepare Athena_G2 BIOS images to upgrade using afuflash
   Step  2   upgrade bios using AFUFLASH     ${bios_update_cmd}
   Step  3   OS Connect Device
   Step  4   Check version in BIOS
   Step  5   OS Disconnect Device
   Step  6   ConnectESMB
   Step  7   Check version in BIOS
   Step  8   OS Disconnect Device
   Step  9   remove Athena_G2 BIOS images

   [Teardown]  OS Disconnect Device

CONSR-BIOS-INFO-0004-0001
   [Documentation]   InfoCheck_004_BIOS/OS time sync
   [Tags]   CONSR-BIOS-INFO-0004-0001   Athena-G2

   Step  1   Change System date and time in BIOS
   Step  2   Check date and time is sync with BIOS
   Step  3   Change System date and time in OS
   Step  4   Verify date and time is sync with OS

CONSR-BIOS-BSUP-0001-0001
   [Documentation]   This test checks Upgrade BIOS with CFUFLASH tool
   [Tags]   CONSR-BIOS-BSUP-0001-0001   Athena-G2
   [Timeout]    60 min 00 secs
   [Setup]  prepare Athena_G2 BIOS images to upgrade
   Step  1  upgrade bios using CFUFLASH
   [Teardown]  remove Athena_G2 BIOS images

CONSR-BIOS-BCFC-0017-0001
   [Documentation]   This test checks Basic_UUID Check
   [Tags]   CONSR-BIOS-BCFC-0017-0001   Athena-G2
   [Timeout]     10 mins 00 secs
   Step  1  UUID_Check

CONSR-BIOS-PROS-0005-0001
   [Documentation]   This test checks Processor MicroCode Check
   [Tags]   CONSR-BIOS-PROS-0005-0001  Athena-G2
   [Timeout]     20 mins 00 secs
   Step  1    Processor MicroCode Check

CONSR-BIOS-INFO-0006-0001
   [Documentation]   InfoCheck_006_BIOS_Version Check
   [Tags]   CONSR-BIOS-INFO-0006-0001   Athena-G2

   Step  1   Verify BIOS Version with UEFI Shell

CONSR-BIOS-BBIC-0001-0001
   [Documentation]   This test checks BMC/BIOS Interface check - BMC Self test status check
   [Tags]   CONSR-BIOS-BBIC-0001-0001  Athena-G2
   [Timeout]     20 mins 00 secs
   Step  1   OS Connect Device
   Step  2   verify_BMC_self_test_status_version_log   DUT   ${BMC_Firmware_version}
   Step  3   OS Disconnect Device

CONSR-BIOS-BBIC-0002-0001
   [Documentation]   SEL log clear in BIOS
   [Tags]   CONSR-BIOS-BBIC-0002-0001  Athena-G2

   Step  1   Verify SEL log clear in BIOS

CONSR-BIOS-DIMM-0004-0001
   [Documentation]   This test checks Memory info check
   [Tags]   CONSR-BIOS-DIMM-0004-0001   Athena-G2
   Step  1  BIOS memory topology check 

CONSR-BIOS-BSUP-0003-0001
   [Documentation]   This test checks Flash utility for BIOS and ME update under Linux
   [Tags]   CONSR-BIOS-BSUP-0003-0001    Athena-G2
   [Timeout]     45 mins 00 secs
   [Setup]   prepare Athena_G2 BIOS images to upgrade using afuflash
   Step  1   upgrade bios using AFUFLASH    ${bios_me_update_cmd}
   Step  2   OS Connect Device
   Step  3   Check version in BIOS
   Step  4   verify_version_in_ME    DUT    ${ME_FW_version}
   Step  5   OS Disconnect Device
   Step  6   ConnectESMB
   Step  7   Check version in BIOS
   Step  8   verify_version_in_ME    DUT    ${ME_FW_version}
   Step  9   OS Disconnect Device
   Step  10  Sleep  90
   [Teardown]   remove Athena_G2 BIOS images

CONSR-BIOS-BSUP-0007-0001
   [Documentation]   BIOS_007_BIOS FW Update--CONF save
   [Tags]   CONSR-BIOS-BSUP-0007-0001   Athena-G2
   [Setup]  Download Athena BIOS image

   Step  1  Do some config in BIOS
   Step  2  Upgrade BIOS using CFUFLASH Tool
   Step  3  Verify config saved in BIOS

   [Teardown]  Remove Athena FW image

CONSR-BIOS-BSUP-0009-0001
   [Documentation]   This test checks BIOS Upgrade and Downgrade between mutiple versions
   [Tags]   CONSR-BIOS-BSUP-0009-0001     Athena-G2
   [Setup]   Prepare images of multiple versions
   Step  1  upgrade_downgrade_bios_version     Athena_BIOS_Versions_A   oldImage  V3   ${ME_FW_version}   ${ME_Version_OS}
   Step  2  upgrade_downgrade_bios_version     Athena_BIOS_Versions_A   newImage  NV   ${ME_FW_version_new}  ${ME_Version_OS_new}
   Step  3  upgrade_downgrade_bios_version     Athena_BIOS_Versions_A   oldImage  V2   ${ME_FW_version}   ${ME_Version_OS}
   Step  4  upgrade_downgrade_bios_version     Athena_BIOS_Versions_A   newImage  NV   ${ME_FW_version_new}  ${ME_Version_OS_new}
   Step  5  upgrade_downgrade_bios_version     Athena_BIOS_Versions_A   oldImage  V1   ${ME_FW_version}   ${ME_Version_OS}
   Step  6  upgrade_downgrade_bios_version     Athena_BIOS_Versions_A   newImage  NV   ${ME_FW_version_new}  ${ME_Version_OS_new}   
   Step  7  Sleep  90
   [Teardown]   remove Athena_G2 BIOS images

CONSR-BIOS-STRS-0002-0001
   [Documentation]   This test checks Stress Test - Loop Flash BIOS under linux
   [Tags]   CONSR-BIOS-STRS-0002-0001     Athena-G2
   [Setup]   Prepare images of multiple versions
   FOR    ${INDEX}    IN RANGE    ${MAXINDEX}
        Print Loop Info  ${INDEX}
        Step  1  upgrade_downgrade_bios_version     Athena_BIOS_Versions_A   oldImage  V3   ${ME_FW_version}   ${ME_Version_OS}
        Step  2  upgrade_downgrade_bios_version     Athena_BIOS_Versions_A   newImage  NV   ${ME_FW_version_new}  ${ME_Version_OS_new}
        Step  3  upgrade_downgrade_bios_version     Athena_BIOS_Versions_A   oldImage  V2   ${ME_FW_version}   ${ME_Version_OS}
        Step  4  upgrade_downgrade_bios_version     Athena_BIOS_Versions_A   newImage  NV   ${ME_FW_version_new}  ${ME_Version_OS_new}
        Step  5  upgrade_downgrade_bios_version     Athena_BIOS_Versions_A   oldImage  V1   ${ME_FW_version}   ${ME_Version_OS}
        Step  6  upgrade_downgrade_bios_version     Athena_BIOS_Versions_A   newImage  NV   ${ME_FW_version_new}  ${ME_Version_OS_new}
   END
   Sleep   90
   [Teardown]   remove Athena_G2 BIOS images

CONSR-BIOS-BSUP-0010-0001
   [Documentation]   This test checks BIOS Update Test-MD5 Check
   [Tags]  CONSR-BIOS-BSUP-0010-0001    Athena-G2
   [Setup]  Prepare images of multiple versions
   Step  1   OS Connect Device
   Step  2   verify md5checksum with release notes   Athena_BIOS_Versions_A   oldImage  V1    ${md5_checksum_v1}
   Step  3   verify md5checksum with release notes   Athena_BIOS_Versions_A   oldImage  V2    ${md5_checksum_v2}
   Step  4   verify md5checksum with release notes   Athena_BIOS_Versions_A   oldImage  V3    ${md5_checksum_v3}
   Step  5   verify md5checksum with release notes   Athena_BIOS_Versions_A   newImage  NV    ${md5_checksum_NV}
   Step  6   OS Disconnect Device
   Step  7   ConnectESMB
   Step  8   verify md5checksum with release notes   Athena_BIOS_Versions_A   oldImage  V1    ${md5_checksum_v1}
   Step  9   verify md5checksum with release notes   Athena_BIOS_Versions_A   oldImage  V2    ${md5_checksum_v2}
   Step  10  verify md5checksum with release notes   Athena_BIOS_Versions_A   oldImage  V3    ${md5_checksum_v3}
   Step  11  verify md5checksum with release notes   Athena_BIOS_Versions_A   newImage  NV    ${md5_checksum_NV}
   Step  12  OS Disconnect Device
   [Teardown]   remove Athena_G2 BIOS images

CONSR-BIOS-INFO-0005-0001
   [Documentation]   This test checks NVME info Check
   [Tags]   CONSR-BIOS-INFO-0005-0001   Athena-G2
   Step  1  NVME information check

CONSR-BIOS-STRS-0001-0001
   [Documentation]   This test checks Stress test
   [Tags]   CONSR-BIOS-STRS-0001-0001   Athena-G2
   [Timeout]  24 hours
   FOR    ${INDEX}    IN RANGE    ${MAXINDEX}
       Step  1   UEFI shell mode reset
   END
   Step  2   OS Connect Device
   Step  3   common BIOS FW check list in ESM A
   Step  4   OS Disconnect Device

CONSR-BIOS-PROS-0002-0001
   [Documentation]   Processor_002_CPU P State
   [Tags]   CONSR-BIOS-PROS-0002-0001  Athena-G2

   Step  1   Record the CPU Frequency with EIST as Enabled
   Step  2   Record the CPU Frequency with EIST as Disabled

CONSR-BIOS-BCFC-0010-0001
   [Documentation]   This test checks BIOS Basic Test-PCIe_Device_Check
   [Tags]   CONSR-BIOS-BCFC-0010-0001   Athena-G2
   [Timeout]  45 mins 00 secs
   Step  1    PCIe_Device_Check_in_BIOS_UEFI_shell

CONSR-BIOS-BSST-0012-0001
   [Documentation]   Customer default password Check
   [Tags]   CONSR-BIOS-BSST-0012-0001   Athena-G2

   Step  1   Verify default user password in BIOS 

CONSR-BIOS-BBIC-0003-0001
   [Documentation]   BMC_003_FB2 watchdog function
   [Tags]   CONSR-BIOS-BBIC-0003-0001   Athena-G2

#   Step  1   Verify FRB-2 Timer Functionality
   Step  2  Verify OS Watchdog Timer Functionality

CONSR-BIOS-BSUP-0005-0001
   [Documentation]   This test checks BIOS_005_Flash BIOS and ME under UEFI shell
   [Tags]   CONSR-BIOS-BSUP-0005-0001   Athena-G2
   [Timeout]  45 mins 00 secs
   Step  1   Verify BIOS_005_Flash BIOS and ME under UEFI shell   Athena_BIOS_Versions_A   newImage  NV  ${bios_me_update_cmd}

CONSR-BIOS-BSUP-0008-0001
   [Documentation]   This test checks BIOS_008_BIOS flash recovery test	
   [Tags]   CONSR-BIOS-BSUP-0008-0001   Athena-G2
   [Timeout]  45 mins 00 secs   
   Step  1   Verify BIOS_008_BIOS flash recovery test   Athena_BIOS_Versions_A   newImage  NV  ${bios_recovery_cmd}

CONSR-BIOS-BSUP-0006-0001
   [Documentation]   This test checks Flash BIOS under UEFI shell
   [Tags]   CONSR-BIOS-BSUP-0006-0001   Athena-G2
   [Timeout]  45 mins 00 secs
   Step  1    Flash BIOS under UEFI shell   Athena_BIOS_Versions_A   newImage  NV

CONSR-BIOS-STRS-0005-0001
    [Documentation]  This test checks Linux OS reboot stress
    [Tags]     CONSR-BIOS-STRS-0005-0001   Athena-G2
    [Setup]    server Connect
    Step  1    Linux OS reboot stress
   [Teardown]  Server Disconnect

CONSR-BIOS-STRS-0008-0001
    [Documentation]  This test checks system idle stress
    [Tags]     CONSR-BIOS-STRS-0008-0001    Athena-G2
    [Setup]    server Connect
    ${ip}  get_ip_address_from_ipmitool  DUT
    Step  1    clear logs before idle stress   ${ip}
    Step  2    Idle overnight
    Step  3    check logs after idle stress     ${ip}
   [Teardown]  Server Disconnect

CONSR-BIOS-BCFC-0005-0001
   [Documentation]   This test checks Basic_005_TXT Check
   [Tags]   CONSR-BIOS-BCFC-0005-0001    Athena-G2
   [Timeout]  45 mins 00 secs
   Step  1    Boot into BIOS Setup and set configuration

CONSR-BIOS-AEPT-0001-0001
   [Documentation]   This test checks AEP_001_AppDirect
   [Tags]   CONSR-BIOS-AEPT-0001-0001    Athena-G2
   [Timeout]    60 min 00 secs
   Step  1    Check Intel Optane DC Persistent Memory Configuration DIMMs
   Step  2    Check Two Regions are created and each region info shows right
   Step  3    Check namespace and App Direct Capacity
   Step  4    Check namespace and App Direct Capacity after power cycle

CONSR-BIOS-AEPT-0004-0001
   [Documentation]   This test checks AEP DIMM Security
   [Tags]   CONSR-BIOS-AEPT-0004-0001      Athena-G2
   [Timeout]  60 mins 00 secs
   Step  1    Enable Disable AEP security in BIOS setup

*** Keywords ***
OS Connect Device
    OSConnect

OS Disconnect Device
    OSDisconnect

Print Loop Info
    [Arguments]    ${CUR_INDEX}
    Log  *******************************************
    Log  *** Test Loop \#: ${CUR_INDEX} / ${LoopCnt} ***
    Log  *

