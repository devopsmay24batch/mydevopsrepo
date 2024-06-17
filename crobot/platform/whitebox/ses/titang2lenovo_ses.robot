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
    [Tags]     create_gold_file  Titan_G2_Lenovo
    [Timeout]  30 min 00 seconds
    [Setup]    get dut variable
    Sub-Case  create-gold-file_1  Create ses page gold file
    Sub-Case  create-gold-file_1  Compare ses page gold file

CONSR-SEST-SPCK-0001-0001
    [Documentation]  This test checks  SES Page - Supported Diagnostic Pages Diagnostic Page (00h)
    [Tags]     CONSR-SEST-SPCK-0001-0001   Titan_G2_Lenovo
    [Timeout]  5 min 00 seconds
    [Setup]    get dut variable
    Sub-Case  CONSR-SEST-SPCK-0001-0001_1  check esm mode status
    Sub-Case  CONSR-SEST-SPCK-0001-0001_2  check all supported diagnostic pages
    Sub-Case  CONSR-SEST-SPCK-0001-0001_3  check esm mode status ESMB
    [Teardown]  Run Keyword If Test Failed  Disconnect

CONSR-SEST-SPCK-0002-0001
    [Documentation]  This test checks  SES Page - Configuration Diagnostic Pages(01h)
    [Tags]     CONSR-SEST-SPCK-0002-0001  Titan_G2_Lenovo
    [Timeout]  5 min 00 seconds
    [Setup]    get dut variable
    Sub-Case  CONSR-SEST-SPCK-0002-0001_1  check esm mode status
    Sub-Case  CONSR-SEST-SPCK-0002-0001_2  Configuration Diagnostic Pages(01h)
    Sub-Case  CONSR-SEST-SPCK-0002-0001_3  check esm mode status ESMB
    [Teardown]  Run Keyword If Test Failed  Disconnect

CONSR-SEST-SPCK-0003-0001
    [Documentation]  This test checks  Enclosure Status Diagnostic Pages(02h)
    [Tags]     CONSR-SEST-SPCK-0003-0001  Titan_G2_Lenovo
    [Timeout]  5 min 00 seconds
    [Setup]    get dut variable
    Sub-Case  CONSR-SEST-SPCK-0003-0001_1  check esm mode status
    Sub-Case  CONSR-SEST-SPCK-0003-0001_2  Enclosure Status Diagnostic Pages(02h)
    Sub-Case  CONSR-SEST-SPCK-0003-0001_3  check esm mode status ESMB

CONSR-SEST-SPCK-0004-0001
    [Documentation]  This test checks  Enclosure Control Diagnostic Pages(02h) - set control bits via raw data
    [Tags]     CONSR-SEST-SPCK-0004-0001  Titan_G2_Lenovo
    [Timeout]  5 min 00 seconds
    [Setup]    get dut variable
    Sub-Case  CONSR-SEST-SPCK-0004-0001_1  check esm mode status
    Sub-Case  CONSR-SEST-SPCK-0004-0001_2  set control bits via raw data
    Sub-Case  CONSR-SEST-SPCK-0004-0001_3  check esm mode status ESMB
    [Teardown]  Run Keyword If Test Failed  Disconnect

CONSR-SEST-STRS-0005-0001
    [Documentation]  FW Reset stress Test
    [Tags]     CONSR-SEST-STRS-0005-0001  Titan_G2_Lenovo
    [Timeout]  24 hours
    FOR    ${INDEX}    IN RANGE    ${MAXINDEX}
        Print Loop Info  ${INDEX}
        Step  1  reset And Check All Expanders Lenovo  ${reset_expander_00_cmd}
        Step  2  reset And Check All Expanders Lenovo  ${reset_expander_01_cmd}
        Step  3  reset And Check All Expanders Lenovo  ${reset_expander_03_cmd}
    END
    [Teardown]  Run Keywords  Server Disconnect
           ...  AND Disconnect

CONSR-SEST-SPCK-0006-0001
    [Documentation]  Check 'crit' bit with sensors under UC condition - Enclosure Control Diagnostic Pages(02h)
    [Tags]     CONSR-SEST-SPCK-0006-0001  Titan_G2_Lenovo
    [Timeout]  5 min 00 seconds
    [Setup]  check ESM And Connect Server
    Step  1  Run Keyword And Continue On Failure  check Temperature Alarm  high critical
    Step  2  restore Temperature Threshold  high critical
    Step  3  Server Disconnect
    Step  4  check esm mode status ESMB
    [Teardown]  Run Keywords  Server Disconnect
           ...  AND Disconnect

CONSR-SEST-SPCK-0008-0001
    [Documentation]  Check 'non-crit' bit with sensors under UW condition - Enclosure Control Diagnostic Pages(02h)
    [Tags]     CONSR-SEST-SPCK-0008-0001  Titan_G2_Lenovo
    [Timeout]  5 min 00 seconds
    [Setup]  check ESM And Connect Server
    Step  1  Run Keyword And Continue On Failure  check Temperature Alarm  high warning
    Step  2  restore Temperature Threshold  high warning
    Step  3  Server Disconnect
    Step  4  check esm mode status ESMB
    [Teardown]  Run Keywords  Server Disconnect
           ...  AND Disconnect

CONSR-SEST-FWDL-0010-0001
    [Documentation]  This test checks downgrade FW with mode 0xe + mode 0xf
    [Tags]     CONSR-SEST-FWDL-0010-0001  Titan_G2_Lenovo
    [Timeout]  60 min 00 seconds
    [Setup]    get dut variable
    Sub-Case  CONSR-SEST-FWDL-0010-0001_1  check esm mode status
    Sub-Case  CONSR-SEST-FWDL-0010-0001_2  Download SES FW File
    Sub-Case  CONSR-SEST-FWDL-0010-0001_3  downgrade FW with mode 0xe + mode 0xf Lenovo
    Sub-Case  CONSR-SEST-FWDL-0010-0001_4  upgrade FW with mode 0xe + mode 0xf Lenovo
    Sub-Case  CONSR-SEST-FWDL-0010-0001_5  check SES version on both ESMs
    [Teardown]  Run Keywords  Server Disconnect
           ...  AND Disconnect

CONSR-SEST-FWDL-0012-0001
    [Documentation]  This test checks downgrade FW with mode 0xe + reset 01h code
    [Tags]     CONSR-SEST-FWDL-0012-0001  Titan_G2_Lenovo
    [Timeout]  50 min 00 seconds
    [Setup]    get dut variable
    Sub-Case  CONSR-SEST-FWDL-0012-0001_1  check esm mode status
    Sub-Case  CONSR-SEST-FWDL-0012-0001_2  Download SES FW File
    Sub-Case  CONSR-SEST-FWDL-0012-0001_3  downgrade FW with mode 0xe + reset 01h code Lenovo
    Sub-Case  CONSR-SEST-FWDL-0012-0001_4  upgrade FW with mode 0xe + reset 01h code Lenovo
    Sub-Case  CONSR-SEST-FWDL-0012-0001_5  Do power cycle
    [Teardown]  Run Keywords  Server Disconnect
           ...  AND Disconnect

CONSR-SEST-FWDL-0014-0001
    [Documentation]  This test checks downgrade FW with mode 0xe + power cycle
    [Tags]     CONSR-SEST-FWDL-0014-0001  Titan_G2_Lenovo
    [Timeout]  50 min 00 seconds
    [Setup]    get dut variable
    Sub-Case  CONSR-SEST-FWDL-0014-0001_1  check esm mode status
    Sub-Case  CONSR-SEST-FWDL-0014-0001_2  Download SES FW File
    Sub-Case  CONSR-SEST-FWDL-0014-0001_3  downgrade FW with mode 0xe + power cycle
    #Sub-Case  CONSR-SEST-FWDL-0014-0001_4  Do power cycle
    Sub-Case  CONSR-SEST-FWDL-0014-0001_5  upgrade FW with mode 0xe + power cycle
    [Teardown]  Run Keywords  Server Disconnect
           ...  AND Disconnect

CONSR-SEST-SPCK-0018-0001
    [Documentation]  This test checks  Enclosure Control Diagnostic Pages(02h) - Cooling external Mode
    [Tags]     CONSR-SEST-SPCK-0018-0001  Titan_G2_Lenovo
    [Timeout]  5 min 00 seconds
    [Setup]    get dut variable
    Sub-Case  CONSR-SEST-SPCK-0018-0001_1  check esm mode status
    Sub-Case  CONSR-SEST-SPCK-0018-0001_2  check Cooling external Mode
    Sub-Case  CONSR-SEST-SPCK-0018-0001_3  check esm mode status ESMB
    Sub-Case  CONSR-SEST-SPCK-0018-0001_4  check Cooling external Mode ESMB
    [Teardown]  Run Keyword If Test Failed  Disconnect

CONSR-SEST-SPCK-0020-0001
    [Documentation]  This test checks  Enclosure Control Diagnostic Pages(02h) - Fan current speed
    [Tags]     CONSR-SEST-SPCK-0020-0001  Titan_G2_Lenovo
    [Timeout]  10 min 00 seconds
    [Setup]    get dut variable
    Sub-Case  CONSR-SEST-SPCK-0020-0001_1  check esm mode status
    Sub-Case  CONSR-SEST-SPCK-0020-0001_2  check Cooling external Mode
    Sub-Case  CONSR-SEST-SPCK-0020-0001_3  check Fan current speed
    Sub-Case  CONSR-SEST-SPCK-0020-0001_4  check esm mode status ESMB
    Sub-Case  CONSR-SEST-SPCK-0020-0001_5  check Cooling external Mode ESMB
    Sub-Case  CONSR-SEST-SPCK-0020-0001_6  check Fan current speed ESMB
    [Teardown]  Run Keywords  Server Disconnect
           ...  AND Disconnect

CONSR-SEST-SPCK-0022-0001
    [Documentation]  This test checks  Enclosure Control Diagnostic Pages(02h) - Fan min speed
    [Tags]     CONSR-SEST-SPCK-0022-0001  Titan_G2_Lenovo
    [Timeout]  10 min 00 seconds
    [Setup]    get dut variable
    Sub-Case  CONSR-SEST-SPCK-0022-0001_1  check esm mode status
    Sub-Case  CONSR-SEST-SPCK-0022-0001_2  check Cooling external Mode
    Sub-Case  CONSR-SEST-SPCK-0022-0001_3  check Fan min speed
    Sub-Case  CONSR-SEST-SPCK-0022-0001_4  check esm mode status ESMB
    Sub-Case  CONSR-SEST-SPCK-0022-0001_5  check Cooling external Mode ESMB
    Sub-Case  CONSR-SEST-SPCK-0022-0001_6  check Fan min speed ESMB
    [Teardown]  Run Keywords  Server Disconnect
           ...  AND Disconnect

CONSR-SEST-SPCK-0027-0001
    [Documentation]  Check array device power off - Enclosure Control Diagnostic Pages(02h)
    [Tags]     CONSR-SEST-SPCK-0027-0001  Titan_G2_Lenovo
    [Timeout]  5 min 00 seconds
    [Setup]  check ESM And Connect Server
    Step  1  check Disk Power Off
    Step  2  Server Disconnect
    Step  3  check esm mode status ESMB
    [Teardown]  Run Keywords  Server Disconnect
           ...  AND Disconnect

CONSR-SEST-SPCK-0037-0001
    [Documentation]  This test checks String In Diagnostic Pages(05h)
    [Tags]     CONSR-SEST-SPCK-0037-0001  Titan_G2_Lenovo
    [Timeout]  10 min 00 seconds
    [Setup]    get dut variable
    Sub-Case  CONSR-SEST-SPCK-0037-0001_1  check esm mode status
    Sub-Case  CONSR-SEST-SPCK-0037-0001_2  check String In Diagnostic Pages(05h)
    Sub-Case  CONSR-SEST-SPCK-0037-0001_3  check esm mode status ESMB
    [Teardown]  Run Keywords  Server Disconnect
           ...  AND Disconnect

CONSR-SEST-SPCK-0050-0001
    [Documentation]  Additional Element Status Diagnostic Page(0ah)
    [Tags]     CONSR-SEST-SPCK-0050-0001  Titan_G2_Lenovo
    [Timeout]  5 min 00 seconds
    [Setup]  check ESM And Connect Server
    Step  1  check Disks Info On Page 0x0a
    Step  2  Server Disconnect
    Step  3  check esm mode status ESMB
    [Teardown]  Run Keywords  Server Disconnect
           ...  AND Disconnect

CONSR-SEST-SPCK-0007-0001
    [Documentation]  Check 'crit' bit with sensors under LC condition - Enclosure Control Diagnostic Pages(02h)
    [Tags]     CONSR-SEST-SPCK-0007-0001  Titan_G2_Lenovo
    [Timeout]  5 min 00 seconds
    [Setup]  Server Connect 1
    Step  1  Run Keyword And Continue On Failure  check Temperature Alarm  low critical
    Step  2  restore Temperature Threshold  low critical
    [Teardown]  Server Disconnect

CONSR-SEST-SPCK-0009-0001
    [Documentation]  Check 'non-crit' bit with sensors under LW condition - Enclosure Control Diagnostic Pages(02h)
    [Tags]     CONSR-SEST-SPCK-0009-0001  Titan_G2_Lenovo
    [Timeout]  5 min 00 seconds
    [Setup]  Server Connect 1
    Step  1  Run Keyword And Continue On Failure  check Temperature Alarm  low warning
    Step  2  restore Temperature Threshold  low warning
    [Teardown]  Server Disconnect

CONSR-SEST-SPCK-0019-0001
    [Documentation]  This test checks  Enclosure Control Diagnostic Pages(02h) - Cooling external Mode
    [Tags]     CONSR-SEST-SPCK-0019-0001  Titan_G2_Lenovo
    [Timeout]  5 min 00 seconds
    [Setup]    get dut variable
    Sub-Case  CONSR-SEST-SPCK-0019-0001_1  check esm mode status
    Sub-Case  CONSR-SEST-SPCK-0019-0001_2  check Cooling internal Mode
    Sub-Case  CONSR-SEST-SPCK-0019-0001_3  check esm mode status ESMB
    Sub-Case  CONSR-SEST-SPCK-0019-0001_4  check Cooling internal Mode ESMB
    [Teardown]  Run Keywords  Server Disconnect
           ...  AND Disconnect

CONSR-SEST-SPCK-0021-0001
    [Documentation]  This test checks  Enclosure Control Diagnostic Pages(02h) - Fan max speed
    [Tags]     CONSR-SEST-SPCK-0021-0001  Titan_G2_Lenovo
    [Timeout]  10 min 00 seconds
    [Setup]    get dut variable
    Sub-Case  CONSR-SEST-SPCK-0021-0001_1  check esm mode status
    Sub-Case  CONSR-SEST-SPCK-0021-0001_2  check Cooling external Mode
    Sub-Case  CONSR-SEST-SPCK-0021-0001_3  check Fan max speed
    Sub-Case  CONSR-SEST-SPCK-0021-0001_4  check esm mode status ESMB
    Sub-Case  CONSR-SEST-SPCK-0021-0001_5  check Cooling external Mode ESMB
    Sub-Case  CONSR-SEST-SPCK-0021-0001_6  check Fan max speed ESMB
    [Teardown]  Run Keywords  Server Disconnect
           ...  AND Disconnect

CONSR-SEST-SPCK-0026-0001
    [Documentation]  Check array device OK bit - Enclosure Control Diagnostic Pages(02h)
    [Tags]     CONSR-SEST-SPCK-0026-0001  Titan_G2_Lenovo
    [Timeout]  5 min 00 seconds
    [Setup]  Server Connect 1
    Step  1  check Array OK Bit
    [Teardown]  Run Keywords  Server Disconnect
           ...  AND Disconnect

CONSR-SEST-SPCK-0046-0001
    [Documentation]  Element Descriptor Diagnostic Page(07h)
    [Tags]     CONSR-SEST-SPCK-0046-0001  Titan_G2_Lenovo
    [Timeout]  5 min 00 seconds
    Step  1  get FRU Info
    Step  2  check Descriptor Length
    Step  3  get FRU Info ESMB
    Step  4  check Descriptor Length
    [Teardown]  Run Keywords  Server Disconnect
           ...  AND Disconnect

CONSR-SEST-FWDL-0001-0001
    [Documentation]  Upgrade FW with mode 0x7
    [Tags]     CONSR-SEST-FWDL-0001-0001  Titan_G2_Lenovo
    [Timeout]  20 min 00 seconds
    [Setup]    get dut variable
    Step  1  Server Connect 1
    Step  2  Download SES FW File And Update  True
    Step  3  check ESM SES FW Version  True
    Step  4  check SES FW Version On Server lenovo  True
    [Teardown]  Run Keywords  Server Disconnect
           ...  AND Disconnect

CONSR-SEST-FWDL-0002-0001
    [Documentation]  Downgrade FW with mode 0x7
    [Tags]     CONSR-SEST-FWDL-0002-0001  Titan_G2_Lenovo
    [Timeout]  30 min 00 seconds
    [Setup]    get dut variable
    Step  1  check esm mode status
    Step  2  Download SES FW File And Update  False
    Step  3  check ESM SES FW Version  False
    Step  4  check SES FW Version On Server lenovo  False
    Step  5  Download SES FW File And Update  True
    Step  6  check ESM SES FW Version  True
    Step  7  check SES FW Version On Server lenovo  True
    [Teardown]  Run Keywords  Server Disconnect
           ...  AND Disconnect

CONSR-SEST-SPCK-0005-0001
    [Documentation]  This test checks  Enclosure Control Diagnostic Pages(02h) - check 'Info' bit
    [Tags]     CONSR-SEST-SPCK-0005-0001  Titan_G2_Lenovo
    [Timeout]  5 min 00 seconds
    [Setup]    get dut variable
    Sub-Case  CONSR-SEST-SPCK-0005-0001_1  check esm mode status
    Sub-Case  CONSR-SEST-SPCK-0005-0001_2  check 'Info' bit lenovo
    Sub-Case  CONSR-SEST-SPCK-0005-0001_3  check esm mode status ESMB
    [Teardown]  Run Keyword If Test Failed  Disconnect

CONSR-SEST-FWDL-0006-0001
    [Documentation]  This test checks upgrade FW with mode 0xe + reset 00h code
    [Tags]     CONSR-SEST-FWDL-0006-0001  Titan_G2_Lenovo
    [Timeout]  30 min 00 seconds
    [Setup]    get dut variable
    Sub-Case  CONSR-SEST-FWDL-0006-0001_1  check esm mode status
    Sub-Case  CONSR-SEST-FWDL-0006-0001_2  Download SES FW File
    Sub-Case  CONSR-SEST-FWDL-0006-0001_3  upgrade FW with mode 0xe + reset 00h code Lenovo
    Sub-Case  CONSR-SEST-FWDL-0006-0001_4  check SES version on both ESMs
    [Teardown]  Run Keywords  Server Disconnect
           ...  AND Disconnect

CONSR-SEST-FWDL-0008-0001
    [Documentation]  This test checks upgrade FW with mode 0xe + reset 03h code
    [Tags]     CONSR-SEST-FWDL-0008-0001  Titan_G2_Lenovo
    [Timeout]  30 min 00 seconds
    [Setup]    get dut variable
    Sub-Case  CONSR-SEST-FWDL-0008-0001_1  check esm mode status
    Sub-Case  CONSR-SEST-FWDL-0008-0001_2  Download SES FW File
    Sub-Case  CONSR-SEST-FWDL-0008-0001_3  upgrade FW with mode 0xe + reset 03h code Lenovo
	Sub-Case  CONSR-SEST-FWDL-0008-0001_4  check SES version on both ESMs
    [Teardown]  Run Keywords  Server Disconnect
           ...  AND Disconnect

CONSR-SEST-FWDL-0005-0001
    [Documentation]  This test checks upgrade FW with mode 0xe + mode 0xf
    [Tags]     CONSR-SEST-FWDL-0005-0001  Titan_G2_Lenovo
    [Timeout]  30 min 00 seconds
    [Setup]    get dut variable
    Sub-Case  CONSR-SEST-FWDL-0005-0001_1  check esm mode status
    Sub-Case  CONSR-SEST-FWDL-0005-0001_2  Download SES FW File
    Sub-Case  CONSR-SEST-FWDL-0005-0001_3  upgrade FW with mode 0xe + mode 0xf
    [Teardown]  Run Keywords  Server Disconnect
           ...  AND Disconnect

CONSR-SEST-FWDL-0007-0001
    [Documentation]  This test checks upgrade FW with mode 0xe + reset 01h code
    [Tags]     CONSR-SEST-FWDL-0007-0001  Titan_G2_Lenovo
    [Timeout]  30 min 00 seconds
    [Setup]    get dut variable
    Sub-Case  CONSR-SEST-FWDL-0007-0001_1  check esm mode status
    Sub-Case  CONSR-SEST-FWDL-0007-0001_2  Download SES FW File
    Sub-Case  CONSR-SEST-FWDL-0007-0001_3  upgrade FW with mode 0xe + reset 01h code Lenovo
    Sub-Case  CONSR-SEST-FWDL-0007-0001_4  check SES version on both ESMs
    [Teardown]  Run Keywords  Server Disconnect
           ...  AND Disconnect

CONSR-SEST-SPCK-0036-0001
    [Documentation]  This test checks String In Diagnostic Pages(04h)
    [Tags]     CONSR-SEST-SPCK-0036-0001  Titan_G2_Lenovo
    [Timeout]  10 min 00 seconds
    [Setup]    get dut variable
    Sub-Case  CONSR-SEST-SPCK-0036-0001_1  check esm mode status
    Sub-Case  CONSR-SEST-SPCK-0036-0001_2  Do power cycle
    Sub-Case  CONSR-SEST-SPCK-0036-0001_3  check String In Diagnostic Pages(04h) lenovo
    Sub-Case  CONSR-SEST-SPCK-0036-0001_4  check esm mode status ESMB
    [Teardown]  Run Keywords  Server Disconnect
           ...  AND Disconnect

CONSR-SEST-FWDL-0011-0001
    [Documentation]  This test checks downgrade FW with mode 0xe + reset 00h code
    [Tags]     CONSR-SEST-FWDL-0011-0001  Titan_G2_Lenovo
    [Timeout]  60 min 00 seconds
    [Setup]    get dut variable
    Sub-Case  CONSR-SEST-FWDL-0011-0001_1  check esm mode status
    Sub-Case  CONSR-SEST-FWDL-0011-0001_2  Download SES FW File
    Sub-Case  CONSR-SEST-FWDL-0011-0001_3  downgrade FW with mode 0xe + reset 00h code Lenovo
    Sub-Case  CONSR-SEST-FWDL-0011-0001_4  activitate whitebox FW power cycle
    Sub-Case  CONSR-SEST-FWDL-0011-0001_5  upgrade FW with mode 0xe + reset 00h code Lenovo
    Sub-Case  CONSR-SEST-FWDL-0011-0001_6  check SES version on both ESMs
    [Teardown]  Run Keywords  Server Disconnect
           ...  AND Disconnect

CONSR-SEST-STRS-0012-0001
    [Documentation]  Stress Test in Diagnostic page 10 and 17
    [Tags]     CONSR-SEST-STRS-0012-0001  Titan_G2_Lenovo
    [Timeout]  24 hours
    [Setup]  get dut variable
    Step  1  Create ses Diag page gold file Lenovo
    Step  2  Compare ses Diag page gold file Lenovo
    FOR    ${INDEX}    IN RANGE    ${MAXINDEX}
        Print Loop Info  ${INDEX}
       Step  3  Read VPD from one canister with 0x10 Diag page Lenovo
       Step  4  Read VPD from two canister with 0x10 Diag page Lenovo
       Step  5  Read VPD from both canisters with 0x17 Diag page Lenovo
       #Step  6  Read VPD from two canister with 0x17 Diag page Lenovo
    END
    [Teardown]  Run Keywords  Server Disconnect
           ...  AND Disconnect

CONSR-SEST-FWDL-0013-0001
    [Documentation]  This test checks downgrade FW with mode 0xe + reset 03h code
    [Tags]     CONSR-SEST-FWDL-0013-0001  Titan_G2_Lenovo
    [Timeout]  60 min 00 seconds
    [Setup]    get dut variable
    Sub-Case  CONSR-SEST-FWDL-0013-0001_1  check esm mode status
    Sub-Case  CONSR-SEST-FWDL-0013-0001_2  Download SES FW File
    Sub-Case  CONSR-SEST-FWDL-0013-0001_3  downgrade FW with mode 0xe + reset 03h code Lenovo
    Sub-Case  CONSR-SEST-FWDL-0013-0001_4  check SES version on both ESMs
    #Sub-Case  CONSR-SEST-FWDL-0013-0001_5  Do power cycle
    Sub-Case  CONSR-SEST-FWDL-0013-0001_6  upgrade FW with mode 0xe + reset 03h code Lenovo
    Sub-Case  CONSR-SEST-FWDL-0013-0001_7  check SES version on both ESMs
    [Teardown]  Run Keywords  Server Disconnect
           ...  AND Disconnect

CONSR-SEST-STRS-0006-0001
    [Documentation]  This test checks Polling page stress Test
    [Tags]     CONSR-SEST-STRS-0006-0001  Titan_G2_Lenovo
    [Timeout]  24 hours
    [Setup]    get dut variable
    FOR    ${INDEX}    IN RANGE    ${MAXINDEX}
        Print Loop Info  ${INDEX}
    Sub-Case  CONSR-SEST-STRS-0006-0001_1  check all supported diagnostic pages
    Sub-Case  CONSR-SEST-STRS-0006-0001_2  Configuration Diagnostic Pages(01h)
    Sub-Case  CONSR-SEST-STRS-0006-0001_3  Enclosure Status Diagnostic Pages(02h)
    Sub-Case  CONSR-SEST-STRS-0006-0001_4  check String In Diagnostic Pages(04h) lenovo
    Sub-Case  CONSR-SEST-STRS-0006-0001_5  check String In Diagnostic Pages(05h)
    Sub-Case  CONSR-SEST-STRS-0006-0001_6  check ESM And Connect Server
    Sub-Case  CONSR-SEST-STRS-0006-0001_7  check Disks Info On Page 0x0a
    Sub-Case  CONSR-SEST-STRS-0006-0001_8  get FRU Info
    Sub-Case  CONSR-SEST-STRS-0006-0001_9  check Descriptor Length
    END
    [Teardown]  Run Keywords  Server Disconnect
           ...  AND Disconnect

CONSR-SEST-STRS-0008-0001
  [Documentation]   This test checks PSU download Stress Test
  [Tags]  CONSR-SEST-STRS-0008-0001  Titan_G2_Lenovo
  [Setup]  Download PSU image File lenovo
  get dut variable
  FOR    ${INDEX}    IN RANGE    ${MAXINDEX}
        Print Loop Info  ${INDEX}
        Step  1  PSU Download microcode Control Diagnostic Page Lenovo ESM-A - mode e  True
        Step  2  PSU Download microcode Control Diagnostic Page Lenovo ESM-A - mode f  True   False
        Step  3  PSU Download microcode Control Diagnostic Page Lenovo ESM-A - mode e  False
        Step  4  PSU Download microcode Control Diagnostic Page Lenovo ESM-A - mode f  False   True
        Step  5  PSU Download microcode Control Diagnostic Page Lenovo ESM-A - mode 7  True   False
        Step  6  PSU Download microcode Control Diagnostic Page Lenovo ESM-A - mode 7  False   True
        Step  7  PSU Download microcode Control Diagnostic Page Lenovo ESM-B - mode e  True
        Step  8  PSU Download microcode Control Diagnostic Page Lenovo ESM-B - mode f  True   False
        Step  9  PSU Download microcode Control Diagnostic Page Lenovo ESM-B - mode e  False
        Step  10  PSU Download microcode Control Diagnostic Page Lenovo ESM-B - mode f  False   True
        Step  11  PSU Download microcode Control Diagnostic Page Lenovo ESM-B - mode 7  True   False
        Step  12  PSU Download microcode Control Diagnostic Page Lenovo ESM-B - mode 7  False   True
  END
  [Teardown]  Run Keywords  Server Disconnect
           ...  AND Disconnect

CONSR-SEST-FWDL-0009-0001
    [Documentation]  This test checks upgrade FW with mode 0xe + power cycle
    [Tags]     CONSR-SEST-FWDL-0009-0001  Titan_G2_Lenovo
    [Timeout]  30 min 00 seconds
    [Setup]    get dut variable
    Sub-Case  CONSR-SEST-FWDL-0009-0001_1  check esm mode status
    Sub-Case  CONSR-SEST-FWDL-0009-0001_2  Download SES FW File
    Sub-Case  CONSR-SEST-FWDL-0009-0001_3  upgrade FW with mode 0xe + power cycle Lenovo
	Sub-Case  CONSR-SEST-FWDL-0009-0001_4  check SES version on both ESMs
    [Teardown]  Run Keywords  Server Disconnect
           ...  AND Disconnect

CONSR-SEST-STRS-0001-0001
    [Documentation]  This test checks stress upgrade/downgrade FW with mode 0xe
    [Tags]     CONSR-SEST-STRS-0001-0001  Titan_G2_Lenovo  LenovoG2
    [Timeout]  48 hours
    [Setup]    get dut variable
    FOR    ${INDEX}    IN RANGE    ${MAXINDEX}
        Print Loop Info  ${INDEX}
    Sub-Case  CONSR-SEST-STRS-0001-0001_1  check esm mode status
    Sub-Case  CONSR-SEST-STRS-0001-0001_2  downgrade FW with mode 0xe + reset 00h code Lenovo
    Sub-Case  CONSR-SEST-STRS-0001-0001_3  upgrade FW with mode 0xe + reset 00h code Lenovo
    Sub-Case  CONSR-SEST-STRS-0001-0001_4  downgrade FW with mode 0xe + mode 0xf Lenovo
    #Sub-Case  CONSR-SEST-STRS-0001-0001_5  Do power cycle
    Sub-Case  CONSR-SEST-STRS-0001-0001_6  upgrade FW with mode 0xe + mode 0xf Lenovo
    Sub-Case  CONSR-SEST-STRS-0001-0001_7  downgrade FW with mode 0xe + reset 01h code Lenovo
    #Sub-Case  CONSR-SEST-STRS-0001-0001_10  Do power cycle
    Sub-Case  CONSR-SEST-STRS-0001-0001_11  upgrade FW with mode 0xe + reset 01h code Lenovo
    Sub-Case  CONSR-SEST-STRS-0001-0001_12  downgrade FW with mode 0xe + reset 03h code Lenovo
    Sub-Case  CONSR-SEST-STRS-0001-0001_13  upgrade FW with mode 0xe + reset 03h code Lenovo
    Sub-Case  CONSR-SEST-STRS-0001-0001_14  downgrade FW with mode 0xe + power cycle
    Sub-Case  CONSR-SEST-STRS-0001-0001_15  upgrade FW with mode 0xe + power cycle
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
