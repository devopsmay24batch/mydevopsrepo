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
Documentation       Tests to verify ses functions described in the ses function spec for the whiteboxproject.

Variables         ses_variable.py
Library           ../WhiteboxLibAdapter.py
Library           whitebox_lib.py
Library           CommonLib.py
Library           ses_lib.py
Resource          ses_keywords.robot

#Suite Setup       OS Connect Device
#Suite Teardown    OS Disconnect Device

** Variables ***
# It is recommended to use <{ScriptName}|{FeatureName}|{DomainName}_Variable> file for variable declaration with help of
# setting table. This section should keep blank.
#In extreme case if script requires variable then it should be defined in this table with documentaiton tag

*** Test Cases ***

create gold file
    [Documentation]  Debug-Test
    [Tags]     create_gold_file  Nebula_G2F
    [Timeout]  30 min 00 seconds
    [Setup]    get dut variable
    Sub-Case  create-gold-file_1  Create ses page gold file nebula
    Sub-Case  create-gold-file_1  Compare ses page gold file nebula

CONSR-SEST-SPCK-0001-0001
    [Documentation]  This test checks  SES Page - Supported Diagnostic Pages Diagnostic Page (00h)
    [Tags]     CONSR-SEST-SPCK-0001-0001  Nebula_G2F
    [Timeout]  10 min 00 seconds
    [Setup]    get dut variable
    Sub-Case  CONSR-SEST-SPCK-0001-0001_1  check esm mode status
    Sub-Case  CONSR-SEST-SPCK-0001-0001_2  check esm mode status ESMB
    Sub-Case  CONSR-SEST-SPCK-0001-0001_3  check all supported diagnostic pages nebula
    [Teardown]  Run Keyword If Test Failed  Disconnect

CONSR-SEST-SPCK-0002-0001
    [Documentation]  This test checks  SES Page - Configuration Diagnostic Pages(01h)
    [Tags]     CONSR-SEST-SPCK-0002-0001  Nebula_G2F
    [Timeout]  10 min 00 seconds
    [Setup]    get dut variable
    Sub-Case  CONSR-SEST-SPCK-0002-0001_1  check esm mode status
    Sub-Case  CONSR-SEST-SPCK-0002-0001_2  Configuration Diagnostic Pages(01h) nebula
    Sub-Case  CONSR-SEST-SPCK-0002-0001_3  check esm mode status ESMB
    [Teardown]  Run Keyword If Test Failed  Disconnect

CONSR-SEST-SPCK-0003-0001
    [Documentation]  This test checks  Enclosure Status Diagnostic Pages(02h)
    [Tags]     CONSR-SEST-SPCK-0003-0001   Nebula_G2F
    [Timeout]  10 min 00 seconds
    [Setup]    get dut variable
    Sub-Case  CONSR-SEST-SPCK-0003-0001_1  check esm mode status
    Sub-Case  CONSR-SEST-SPCK-0003-0001_2  Enclosure Status Diagnostic Pages(02h) nebula
    Sub-Case  CONSR-SEST-SPCK-0003-0001_3  check esm mode status ESMB

CONSR-SEST-SPCK-0006-0001
    [Documentation]  Check 'crit' bit with sensors under UC condition - Enclosure Control Diagnostic Pages(02h)
    [Tags]     CONSR-SEST-SPCK-0006-0001  Nebula_G2F
    [Timeout]  10 min 00 seconds
    [Setup]  check ESM And Connect Server
    Step  1  get dut variable
    Step  2  Server Connect 1
    ${HDDs}=  get_device_list_nebula    %{DUT_username}  %{DUT_ipv4_ip}  %{DUT_password}
    Step  3  Run Keyword And Continue On Failure  check Temperature Alarm nebula  ${HDDs}[0]  high critical
    Step  4  restore Temperature Threshold  high critical
    Step  5  Run Keyword And Continue On Failure  check Temperature Alarm nebula  ${HDDs}[1]  high critical
    Step  6  restore Temperature Threshold  high critical
    Step  7  Server Disconnect
    Step  8  check esm mode status ESMB
    [Teardown]  Run Keywords  Server Disconnect
           ...  AND Disconnect

CONSR-SEST-SPCK-0007-0001
    [Documentation]  Check 'crit' bit with sensors under LC condition - Enclosure Control Diagnostic Pages(02h)
    [Tags]     CONSR-SEST-SPCK-0007-0001  Nebula_G2F
    [Timeout]  10 min 00 seconds
    [Setup]  get dut variable
    Step  1  Server Connect 1
    ${HDDs}=  get_device_list_nebula    %{DUT_username}  %{DUT_ipv4_ip}  %{DUT_password}
    Step  2  Run Keyword And Continue On Failure  check Temperature Alarm nebula  ${HDDs}[0]  low critical
    Step  3  restore Temperature Threshold  low critical
    Step  4  Run Keyword And Continue On Failure  check Temperature Alarm nebula  ${HDDs}[1]  low critical
    Step  5  restore Temperature Threshold  low critical
    [Teardown]  Server Disconnect
	
CONSR-SEST-SPCK-0008-0001
    [Documentation]  Check 'non-crit' bit with sensors under UW condition - Enclosure Control Diagnostic Pages(02h)
    [Tags]     CONSR-SEST-SPCK-0008-0001  Nebula_G2F
    [Timeout]  10 min 00 seconds
    [Setup]  check ESM And Connect Server
    Step  1  get dut variable
    Step  2  Server Connect 1
    ${HDDs}=  get_device_list_nebula    %{DUT_username}  %{DUT_ipv4_ip}  %{DUT_password}
    Step  3  Run Keyword And Continue On Failure  check Temperature Alarm nebula  ${HDDs}[0]  high warning
    Step  4  restore Temperature Threshold  high warning
    Step  5  Run Keyword And Continue On Failure  check Temperature Alarm nebula  ${HDDs}[1]  high warning
    Step  6  restore Temperature Threshold  high warning
    Step  7  Server Disconnect
    Step  8  check esm mode status ESMB
    [Teardown]  Run Keywords  Server Disconnect
           ...  AND Disconnect

CONSR-SEST-SPCK-0009-0001
    [Documentation]  Check 'non-crit' bit with sensors under LW condition - Enclosure Control Diagnostic Pages(02h)
    [Tags]     CONSR-SEST-SPCK-0009-0001  Nebula_G2F
    [Timeout]  10 min 00 seconds
    [Setup]  get dut variable
    Step  1  Server Connect 1
    ${HDDs}=  get_device_list_nebula    %{DUT_username}  %{DUT_ipv4_ip}  %{DUT_password}
    Step  2  Run Keyword And Continue On Failure  check Temperature Alarm nebula  ${HDDs}[0]  low warning
    Step  3  restore Temperature Threshold  low warning
    Step  4  Run Keyword And Continue On Failure  check Temperature Alarm nebula  ${HDDs}[1]  low warning
    Step  5  restore Temperature Threshold  low warning
    [Teardown]  Server Disconnect
	
CONSR-SEST-SPCK-0018-0001
    [Documentation]  This test checks  Enclosure Control Diagnostic Pages(02h) - Cooling external Mode
    [Tags]     CONSR-SEST-SPCK-0018-0001  Nebula_G2F
    [Timeout]  10 min 00 seconds
    [Setup]    get dut variable
    Sub-Case  CONSR-SEST-SPCK-0018-0001_1  check esm mode status
    Sub-Case  CONSR-SEST-SPCK-0018-0001_2  check Cooling external Mode nebula
    Sub-Case  CONSR-SEST-SPCK-0018-0001_3  check esm mode status ESMB
    [Teardown]  Run Keyword If Test Failed  Disconnect

CONSR-SEST-SPCK-0019-0001
    [Documentation]  This test checks  Enclosure Control Diagnostic Pages(02h) - Cooling external Mode
    [Tags]     CONSR-SEST-SPCK-0019-0001   Nebula_G2F
    [Timeout]  10 min 00 seconds
    [Setup]    get dut variable
    Sub-Case  CONSR-SEST-SPCK-0019-0001_1  check esm mode status
    Sub-Case  CONSR-SEST-SPCK-0019-0001_2  check Cooling internal Mode nebula
    Sub-Case  CONSR-SEST-SPCK-0019-0001_3  check esm mode status ESMB
    [Teardown]  Run Keywords  Server Disconnect
           ...  AND Disconnect
		   
CONSR-SEST-SPCK-0020-0001
    [Documentation]  This test checks  Enclosure Control Diagnostic Pages(02h) - Fan current speed
    [Tags]     CONSR-SEST-SPCK-0020-0001  Nebula_G2F
    [Timeout]  20 min 00 seconds
    [Setup]    get dut variable
    Sub-Case  CONSR-SEST-SPCK-0020-0001_1  check esm mode status
    Sub-Case  CONSR-SEST-SPCK-0020-0001_2  check Cooling external Mode nebula
    Sub-Case  CONSR-SEST-SPCK-0020-0001_3  check Fan current speed nebula
    [Teardown]  Run Keywords  Server Disconnect
           ...  AND Disconnect

CONSR-SEST-SPCK-0021-0001
    [Documentation]  This test checks  Enclosure Control Diagnostic Pages(02h) - Fan max speed
    [Tags]     CONSR-SEST-SPCK-0021-0001   Nebula_G2F
    [Timeout]  20 min 00 seconds
    [Setup]    get dut variable
    Sub-Case  CONSR-SEST-SPCK-0021-0001_1  check esm mode status
    Sub-Case  CONSR-SEST-SPCK-0021-0001_2  check Cooling external Mode nebula
    Sub-Case  CONSR-SEST-SPCK-0021-0001_3  check Fan max speed nebula
    Sub-Case  CONSR-SEST-SPCK-0021-0001_4  check esm mode status ESMB
    Sub-Case  CONSR-SEST-SPCK-0021-0001_6  check Fan max speed nebula ESMB
    [Teardown]  Run Keywords  Server Disconnect
           ...  AND Disconnect

CONSR-SEST-SPCK-0022-0001
    [Documentation]  This test checks  Enclosure Control Diagnostic Pages(02h) - Fan min speed
    [Tags]     CONSR-SEST-SPCK-0022-0001  Nebula_G2F
    [Timeout]  30 min 00 seconds
    [Setup]    get dut variable
    Sub-Case  CONSR-SEST-SPCK-0022-0001_1  check esm mode status
    Sub-Case  CONSR-SEST-SPCK-0022-0001_2  check Cooling external Mode nebula
    Sub-Case  CONSR-SEST-SPCK-0022-0001_3  check Fan min speed nebula
    Sub-Case  CONSR-SEST-SPCK-0022-0001_4  check esm mode status ESMB
    Sub-Case  CONSR-SEST-SPCK-0022-0001_5  check Fan min speed ESMB nebula
    [Teardown]  Run Keywords  Server Disconnect
           ...  AND Disconnect

CONSR-SEST-SPCK-0027-0001
    [Documentation]  Check array device power off - Enclosure Control Diagnostic Pages(02h)
    [Tags]     CONSR-SEST-SPCK-0027-0001   Nebula_G2F
    [Timeout]  10 min 00 seconds
    [Setup]  check ESM And Connect Server
    Step  1  get dut variable
    Step  2  check Disk Power Off nebula
    Step  3  Server Disconnect
    Step  4  check esm mode status ESMB
    [Teardown]  Run Keywords  Server Disconnect
           ...  AND Disconnect

CONSR-SEST-SPCK-0036-0001
    [Documentation]  This test checks String In Diagnostic Pages(04h)
    [Tags]     CONSR-SEST-SPCK-0036-0001  Nebula_G2F
    [Timeout]  10 min 00 seconds
    [Setup]    get dut variable
    Sub-Case  CONSR-SEST-SPCK-0036-0001_1  check esm mode status
    Sub-Case  CONSR-SEST-SPCK-0036-0001_2  check String In Diagnostic Pages(04h) nebula
    Sub-Case  CONSR-SEST-SPCK-0036-0001_4  check esm mode status ESMB
    [Teardown]  Run Keywords  Server Disconnect
           ...  AND Disconnect
		   
CONSR-SEST-SPCK-0037-0001
    [Documentation]  This test checks String In Diagnostic Pages(05h)
    [Tags]     CONSR-SEST-SPCK-0037-0001   Nebula_G2F
    [Timeout]  20 min 00 seconds
    [Setup]    get dut variable
    Sub-Case  CONSR-SEST-SPCK-0037-0001_1  check esm mode status
    Sub-Case  CONSR-SEST-SPCK-0037-0001_2  check String In Diagnostic Pages(05h) nebula
    Sub-Case  CONSR-SEST-SPCK-0037-0001_3  check esm mode status ESMB
    [Teardown]  Run Keywords  Server Disconnect
           ...  AND Disconnect
		   
CONSR-SEST-SPCK-0046-0001
    [Documentation]  Element Descriptor Diagnostic Page(07h)
    [Tags]     CONSR-SEST-SPCK-0046-0001  Nebula_G2F
    [Timeout]  10 min 00 seconds
    [Setup]    get dut variable
    Step  1  get FRU Info
    Step  2  check Descriptor Length nebula
    Step  3  get FRU Info ESMB
    Step  4  check Descriptor Length nebula
    [Teardown]  Run Keywords  Server Disconnect
           ...  AND Disconnect
		   
CONSR-SEST-SPCK-0050-0001
    [Documentation]  Additional Element Status Diagnostic Page(0ah)
    [Tags]     CONSR-SEST-SPCK-0050-0001  Nebula_G2F
    [Timeout]  10 min 00 seconds
    [Setup]  check ESM And Connect Server
    Step  1  get dut variable
    Step  2  check Disks Info On Page 0x0a nebula
    Step  3  Server Disconnect
    Step  4  check esm mode status ESMB
    [Teardown]  Run Keywords  Server Disconnect
           ...  AND Disconnect

CONSR-SEST-FWDL-0001-0001
    [Documentation]  Upgrade FW with mode 0x7
    [Tags]     CONSR-SEST-FWDL-0001-0001  Nebula_G2F
    [Timeout]  60 min 00 seconds
    [Setup]    get dut variable
    Step  1  Server Connect 1
    Step  2  Download SES FW File And Update Nebula  True
    Step  3  check ESM SES FW Version Nebula  True
    Step  4  check SES FW Version On Server Nebula  True
    [Teardown]  Run Keywords  Server Disconnect
           ...  AND Disconnect

CONSR-SEST-FWDL-0002-0001
    [Documentation]  Downgrade FW with mode 0x7
    [Tags]     CONSR-SEST-FWDL-0002-0001  Nebula_G2F
    [Timeout]  60 min 00 seconds
    [Setup]    get dut variable
    Step  1  Server Connect 1
    Step  2  Download SES FW File And Update Nebula  False
    Step  3  check ESM SES FW Version Nebula  False
    Step  4  check SES FW Version On Server Nebula  False
    Step  5  Download SES FW File And Update Nebula  True
    Step  6  check ESM SES FW Version Nebula  True
    Step  7  check SES FW Version On Server Nebula  True
    [Teardown]  Run Keywords  Server Disconnect
           ...  AND Disconnect

CONSR-SEST-FWDL-0005-0001
    [Documentation]  This test checks upgrade FW with mode 0xe + mode 0xf
    [Tags]     CONSR-SEST-FWDL-0005-0001  Nebula_G2F
    [Timeout]  40 min 00 seconds
    [Setup]    get dut variable
    Sub-Case  CONSR-SEST-FWDL-0005-0001_1  check esm mode status
    Sub-Case  CONSR-SEST-FWDL-0005-0001_2  Download SES FW File
    Sub-Case  CONSR-SEST-FWDL-0005-0001_3  upgrade FW with mode 0xe + mode 0xf nebula
    [Teardown]  Run Keywords  Server Disconnect
           ...  AND Disconnect
		   
CONSR-SEST-FWDL-0010-0001
    [Documentation]  This test checks downgrade FW with mode 0xe + mode 0xf
    [Tags]     CONSR-SEST-FWDL-0010-0001  Nebula_G2F
    [Timeout]  60 min 00 seconds
    [Setup]    get dut variable
    Sub-Case  CONSR-SEST-FWDL-0010-0001_1  check esm mode status
    Sub-Case  CONSR-SEST-FWDL-0010-0001_2  Download SES FW File
    Sub-Case  CONSR-SEST-FWDL-0010-0001_3  downgrade FW with mode 0xe + mode 0xf nebula
    Sub-Case  CONSR-SEST-FWDL-0010-0001_4  upgrade FW with mode 0xe + mode 0xf nebula
    [Teardown]  Run Keywords  Server Disconnect
           ...  AND Disconnect

CONSR-SEST-STRS-0001-0001
    [Documentation]  This test checks stress upgrade/downgrade FW with mode 0xe
    [Tags]     CONSR-SEST-STRS-0001-0001  Nebula_G2F
    [Timeout]  48 hours
    [Setup]    get dut variable
    FOR    ${INDEX}    IN RANGE    ${MAXINDEX}
        Print Loop Info  ${INDEX}
    Sub-Case  CONSR-SEST-STRS-0001-0001_1  check esm mode status
    Sub-Case  CONSR-SEST-STRS-0001-0001_2  downgrade FW with mode 0xe + mode 0xf Nebula
    Sub-Case  CONSR-SEST-STRS-0001-0001_3  upgrade FW with mode 0xe + mode 0xf Nebula
    END
    [Teardown]  Run Keywords  Server Disconnect
           ...  AND Disconnect

*** Keywords ***
OS Connect Device
    OSConnect

OS Disconnect Device
    OSDisconnect

check ESM And Connect Server
    check esm mode status
    server Connect

Print Loop Info
    [Arguments]    ${CUR_INDEX}
    Log  *******************************************
    Log  *** Test Loop \#: ${CUR_INDEX} / ${LoopCnt} ***
    Log  *

