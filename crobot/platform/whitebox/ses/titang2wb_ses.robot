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
    [Tags]     create_gold_file  Titan_G2_WB
    [Timeout]  30 min 00 seconds
    [Setup]    get dut variable
    Sub-Case  create-gold-file_1  Create ses page gold file
    Sub-Case  create-gold-file_1  Compare ses page gold file

CONSR-SEST-SPCK-0037-0001
    [Documentation]  This test checks String In Diagnostic Pages(05h)
    [Tags]     CONSR-SEST-SPCK-0037-0001  Titan_G2_WB    Regression
    [Timeout]  10 min 00 seconds
    [Setup]    get dut variable
    Sub-Case  CONSR-SEST-SPCK-0037-0001_1  check esm mode status
    Sub-Case  CONSR-SEST-SPCK-0037-0001_2  check String In Diagnostic Pages(05h)
    Sub-Case  CONSR-SEST-SPCK-0037-0001_3  check esm mode status ESMB
    [Teardown]  Run Keywords  Server Disconnect
           ...  AND OSDisconnect

CONSR-SEST-STRS-0006-0001
    [Documentation]  This test checks Polling page stress Test
    [Tags]     CONSR-SEST-STRS-0006-0001  Titan_G2_WB    Regression
    [Timeout]  24 hours
    [Setup]    get dut variable
    FOR    ${INDEX}    IN RANGE    ${MAXINDEX}
        Print Loop Info  ${INDEX}
    Sub-Case  CONSR-SEST-STRS-0006-0001_1   check all supported diagnostic pages
    Sub-Case  CONSR-SEST-STRS-0006-0001_2   Configuration Diagnostic Pages(01h)
    Sub-Case  CONSR-SEST-STRS-0006-0001_3   Enclosure Status Diagnostic Pages(02h)
    Sub-Case  CONSR-SEST-STRS-0006-0001_4   check String In Diagnostic Pages(04h) Titan G2 WB
    Sub-Case  CONSR-SEST-STRS-0006-0001_5   check String In Diagnostic Pages(05h)
    Sub-Case  CONSR-SEST-STRS-0006-0001_6   check ESM And Connect Server
    Sub-Case  CONSR-SEST-STRS-0006-0001_7   check Disks Info On Page 0x0a
    Sub-Case  CONSR-SEST-STRS-0006-0001_8   Server Disconnect
    Sub-Case  CONSR-SEST-STRS-0006-0001_9   get FRU Info Titan G2 WB
    Sub-Case  CONSR-SEST-STRS-0006-0001_10   check Descriptor Length Titan G2 WB
    Sub-Case  CONSR-SEST-STRS-0006-0001_11  get FRU Info ESMB Titan G2 WB
    Sub-Case  CONSR-SEST-STRS-0006-0001_12  check Descriptor Length Titan G2 WB
    END
    [Teardown]  Run Keywords  Server Disconnect
           ...  AND OSDisconnect

CONSR-SEST-STRS-0005-0001
    [Documentation]  FW Reset stress Test
    [Tags]     CONSR-SEST-STRS-0005-0001  Titan_G2_WB    Regression
    [Timeout]  24 hours
    FOR    ${INDEX}    IN RANGE    ${MAXINDEX}
        Print Loop Info  ${INDEX}
        Step  1  reset And Check All Expanders Lenovo  ${reset_expander_00_cmd}
        Step  2  reset And Check All Expanders Lenovo  ${reset_expander_01_cmd}
        Step  3  reset And Check All Expanders Lenovo  ${reset_expander_03_cmd}
    END
    [Teardown]  Run Keywords  Server Disconnect
           ...  AND OSDisconnect

CONSR-SEST-SPCK-0020-0001
    [Documentation]  This test checks  Enclosure Control Diagnostic Pages(02h) - Fan current speed
    [Tags]     CONSR-SEST-SPCK-0020-0001  Titan_G2_WB    Regression
    [Timeout]  10 min 00 seconds
    [Setup]    get dut variable
    Sub-Case  CONSR-SEST-SPCK-0020-0001_1  check esm mode status
    Sub-Case  CONSR-SEST-SPCK-0020-0001_2  check Cooling external Mode
    Sub-Case  CONSR-SEST-SPCK-0020-0001_3  check Fan current speed Titan G2 WB
    Sub-Case  CONSR-SEST-SPCK-0020-0001_4  check esm mode status ESMB
    Sub-Case  CONSR-SEST-SPCK-0020-0001_5  check Cooling external Mode ESMB
    Sub-Case  CONSR-SEST-SPCK-0020-0001_6  check Fan current speed ESMB Titan G2 WB
    [Teardown]  Run Keywords  Server Disconnect
           ...  AND OSDisconnect

CONSR-SEST-SPCK-0022-0001
    [Documentation]  This test checks  Enclosure Control Diagnostic Pages(02h) - Fan min speed
    [Tags]     CONSR-SEST-SPCK-0022-0001  Titan_G2_WB    Regression
    [Timeout]  10 min 00 seconds
    [Setup]    get dut variable
    Sub-Case  CONSR-SEST-SPCK-0022-0001_1  check esm mode status
    Sub-Case  CONSR-SEST-SPCK-0022-0001_2  check Cooling external Mode
    Sub-Case  CONSR-SEST-SPCK-0022-0001_3  check Fan min speed Titan G2 WB
    Sub-Case  CONSR-SEST-SPCK-0022-0001_4  check esm mode status ESMB
    Sub-Case  CONSR-SEST-SPCK-0022-0001_5  check Cooling external Mode ESMB
    Sub-Case  CONSR-SEST-SPCK-0022-0001_6  check Fan min speed ESMB Titan G2 WB
    [Teardown]  Run Keywords  Server Disconnect
           ...  AND OSDisconnect

CONSR-SEST-SPCK-0021-0001
    [Documentation]  This test checks  Enclosure Control Diagnostic Pages(02h) - Fan max speed
    [Tags]     CONSR-SEST-SPCK-0021-0001  Titan_G2_WB    Regression
    [Timeout]  10 min 00 seconds
    [Setup]    get dut variable
    Sub-Case  CONSR-SEST-SPCK-0021-0001_1  check esm mode status
    Sub-Case  CONSR-SEST-SPCK-0021-0001_2  check Cooling external Mode
    Sub-Case  CONSR-SEST-SPCK-0021-0001_3  check Fan max speed Titan G2 WB
    Sub-Case  CONSR-SEST-SPCK-0021-0001_4  check esm mode status ESMB
    Sub-Case  CONSR-SEST-SPCK-0021-0001_5  check Cooling external Mode ESMB
    Sub-Case  CONSR-SEST-SPCK-0021-0001_6  check Fan max speed ESMB Titan G2 WB
    [Teardown]  Run Keywords  Server Disconnect
           ...  AND OSDisconnect

CONSR-SEST-SPCK-0001-0001
    [Documentation]  This test checks  SES Page - Supported Diagnostic Pages Diagnostic Page (00h)
    [Tags]     CONSR-SEST-SPCK-0001-0001   Titan_G2_WB    Regression
    [Timeout]  5 min 00 seconds
    [Setup]    get dut variable
    Sub-Case  CONSR-SEST-SPCK-0001-0001_1  check esm mode status
    Sub-Case  CONSR-SEST-SPCK-0001-0001_2  check all supported diagnostic pages
    Sub-Case  CONSR-SEST-SPCK-0001-0001_3  check esm mode status ESMB
    [Teardown]  Run Keyword If Test Failed  OSDisconnect

CONSR-SEST-SPCK-0002-0001
    [Documentation]  This test checks  SES Page - Configuration Diagnostic Pages(01h)
    [Tags]     CONSR-SEST-SPCK-0002-0001  Titan_G2_WB    Regression
    [Timeout]  5 min 00 seconds
    [Setup]    get dut variable
    Sub-Case  CONSR-SEST-SPCK-0002-0001_1  check esm mode status
    Sub-Case  CONSR-SEST-SPCK-0002-0001_2  Configuration Diagnostic Pages(01h)
    Sub-Case  CONSR-SEST-SPCK-0002-0001_3  check esm mode status ESMB
    [Teardown]  Run Keyword If Test Failed  OSDisconnect

CONSR-SEST-SPCK-0003-0001
    [Documentation]  This test checks  Enclosure Status Diagnostic Pages(02h)
    [Tags]     CONSR-SEST-SPCK-0003-0001  Titan_G2_WB    Regression
    [Timeout]  5 min 00 seconds
    [Setup]    get dut variable
    Sub-Case  CONSR-SEST-SPCK-0003-0001_1  check esm mode status
    Sub-Case  CONSR-SEST-SPCK-0003-0001_2  Enclosure Status Diagnostic Pages(02h)
    Sub-Case  CONSR-SEST-SPCK-0003-0001_3  check esm mode status ESMB

CONSR-SEST-SPCK-0004-0001
    [Documentation]  This test checks  Enclosure Control Diagnostic Pages(02h) - set control bits via raw data
    [Tags]     CONSR-SEST-SPCK-0004-0001  Titan_G2_WB    Regression
    [Timeout]  5 min 00 seconds
    [Setup]    get dut variable
    Sub-Case  CONSR-SEST-SPCK-0004-0001_1  check esm mode status
    Sub-Case  CONSR-SEST-SPCK-0004-0001_2  set control bits via raw data
    Sub-Case  CONSR-SEST-SPCK-0004-0001_3  check esm mode status ESMB
    [Teardown]  Run Keyword If Test Failed  OSDisconnect

CONSR-SEST-SPCK-0005-0001
    [Documentation]  This test checks  Enclosure Control Diagnostic Pages(02h) - check 'Info' bit
    [Tags]     CONSR-SEST-SPCK-0005-0001  Titan_G2_WB    Regression    
    [Timeout]  5 min 00 seconds
    [Setup]    get dut variable
    Sub-Case  CONSR-SEST-SPCK-0005-0001_1  check esm mode status
    Sub-Case  CONSR-SEST-SPCK-0005-0001_2  check 'Info' bit lenovo
    Sub-Case  CONSR-SEST-SPCK-0005-0001_3  check esm mode status ESMB
    [Teardown]  Run Keyword If Test Failed  OSDisconnect

CONSR-SEST-SPCK-0006-0001
    [Documentation]  Check 'crit' bit with sensors under UC condition - Enclosure Control Diagnostic Pages(02h)
    [Tags]     CONSR-SEST-SPCK-0006-0001  Titan_G2_WB    Regression
    [Timeout]  5 min 00 seconds
    [Setup]  check ESM And Connect Server
    Step  1  Run Keyword And Continue On Failure  check Temperature Alarm  high critical
    Step  2  restore Temperature Threshold  high critical
    Step  3  Server Disconnect
    Step  4  check esm mode status ESMB
    [Teardown]  Run Keywords  Server Disconnect
           ...  AND OSDisconnect

CONSR-SEST-SPCK-0008-0001
    [Documentation]  Check 'non-crit' bit with sensors under UW condition - Enclosure Control Diagnostic Pages(02h)
    [Tags]     CONSR-SEST-SPCK-0008-0001  Titan_G2_WB    Regression
    [Timeout]  5 min 00 seconds
    [Setup]  check ESM And Connect Server
    Step  1  Run Keyword And Continue On Failure  check Temperature Alarm  high warning
    Step  2  restore Temperature Threshold  high warning
    Step  3  Server Disconnect
    Step  4  check esm mode status ESMB
    [Teardown]  Run Keywords  Server Disconnect
           ...  AND OSDisconnect

CONSR-SEST-SPCK-0018-0001
    [Documentation]  This test checks  Enclosure Control Diagnostic Pages(02h) - Cooling external Mode
    [Tags]     CONSR-SEST-SPCK-0018-0001  Titan_G2_WB    Regression
    [Timeout]  5 min 00 seconds
    [Setup]    get dut variable
    Sub-Case  CONSR-SEST-SPCK-0018-0001_1  check esm mode status
    Sub-Case  CONSR-SEST-SPCK-0018-0001_2  check Cooling external Mode
    Sub-Case  CONSR-SEST-SPCK-0018-0001_3  check esm mode status ESMB
    Sub-Case  CONSR-SEST-SPCK-0018-0001_4  check Cooling external Mode ESMB
    [Teardown]  Run Keyword If Test Failed  OSDisconnect

CONSR-SEST-SPCK-0007-0001
    [Documentation]  Check 'crit' bit with sensors under LC condition - Enclosure Control Diagnostic Pages(02h)
    [Tags]     CONSR-SEST-SPCK-0007-0001  Titan_G2_WB    Regression
    [Timeout]  5 min 00 seconds
    [Setup]  Server Connect 1
    Step  1  Run Keyword And Continue On Failure  check Temperature Alarm  low critical
    Step  2  restore Temperature Threshold  low critical
    [Teardown]  Server Disconnect

CONSR-SEST-SPCK-0009-0001
    [Documentation]  Check 'non-crit' bit with sensors under LW condition - Enclosure Control Diagnostic Pages(02h)
    [Tags]     CONSR-SEST-SPCK-0009-0001  Titan_G2_WB    Regression
    [Timeout]  5 min 00 seconds
    [Setup]  Server Connect 1
    Step  1  Run Keyword And Continue On Failure  check Temperature Alarm  low warning
    Step  2  restore Temperature Threshold  low warning
    [Teardown]  Server Disconnect

CONSR-SEST-SPCK-0019-0001
    [Documentation]  This test checks  Enclosure Control Diagnostic Pages(02h) - Cooling external Mode
    [Tags]     CONSR-SEST-SPCK-0019-0001  Titan_G2_WB    Regression
    [Timeout]  5 min 00 seconds
    [Setup]    get dut variable
    Sub-Case  CONSR-SEST-SPCK-0019-0001_1  check esm mode status
    Sub-Case  CONSR-SEST-SPCK-0019-0001_2  check Cooling internal Mode
    Sub-Case  CONSR-SEST-SPCK-0019-0001_3  check esm mode status ESMB
    Sub-Case  CONSR-SEST-SPCK-0019-0001_4  check Cooling internal Mode ESMB
    [Teardown]  Run Keywords  Server Disconnect
           ...  AND OSDisconnect

CONSR-SEST-SPCK-0026-0001
    [Documentation]  Check array device OK bit - Enclosure Control Diagnostic Pages(02h)
    [Tags]     CONSR-SEST-SPCK-0026-0001  Titan_G2_WB    Regression
    [Timeout]  5 min 00 seconds
    [Setup]  Server Connect 1
    Step  1  check Array OK Bit
    [Teardown]  Run Keywords  Server Disconnect
           ...  AND OSDisconnect

CONSR-SEST-SPCK-0050-0001
    [Documentation]  Additional Element Status Diagnostic Page(0ah)
    [Tags]     CONSR-SEST-SPCK-0050-0001  Titan_G2_WB    Regression
    [Timeout]  5 min 00 seconds
    [Setup]  check ESM And Connect Server
    Step  1  check Disks Info On Page 0x0a
    Step  2  Server Disconnect
    Step  3  check esm mode status ESMB
    [Teardown]  Run Keywords  Server Disconnect
           ...  AND OSDisconnect

CONSR-SEST-SPCK-0046-0001
    [Documentation]  Element Descriptor Diagnostic Page(07h)
    [Tags]     CONSR-SEST-SPCK-0046-0001  Titan_G2_WB    Regression
    [Timeout]  5 min 00 seconds
    Step  1  get FRU Info Titan G2 WB
    Step  2  check Descriptor Length Titan G2 WB
    Step  3  get FRU Info ESMB Titan G2 WB
    Step  4  check Descriptor Length Titan G2 WB
    [Teardown]  Run Keywords  Server Disconnect
           ...  AND OSDisconnect

CONSR-SEST-SPCK-0027-0001
    [Documentation]  Check array device power off - Enclosure Control Diagnostic Pages(02h)
    [Tags]     CONSR-SEST-SPCK-0027-0001  Titan_G2_WB    Regression
    [Timeout]  5 min 00 seconds
    [Setup]  check ESM And Connect Server
    Step  1  check Disk Power Off
    Step  2  Server Disconnect
    Step  3  check esm mode status ESMB
    [Teardown]  Run Keywords  Server Disconnect
           ...  AND OSDisconnect

CONSR-SEST-SPCK-0036-0001
    [Documentation]  This test checks String In Diagnostic Pages(04h)
    [Tags]     CONSR-SEST-SPCK-0036-0001  Titan_G2_WB    Regression
    [Timeout]  10 min 00 seconds
    [Setup]    get dut variable
    Sub-Case  CONSR-SEST-SPCK-0036-0001_1  check esm mode status
    Sub-Case  CONSR-SEST-SPCK-0036-0001_2  Do power cycle
    Sub-Case  CONSR-SEST-SPCK-0036-0001_3  check String In Diagnostic Pages(04h) Titan G2 WB
    Sub-Case  CONSR-SEST-SPCK-0036-0001_4  check esm mode status ESMB
    [Teardown]  Run Keywords  Server Disconnect
           ...  AND OSDisconnect

CONSR-SEST-FWDL-0001-0001
    [Documentation]  Upgrade FW with mode 0x7
    [Tags]     CONSR-SEST-FWDL-0001-0001  Titan_G2_WB    Regression   FWDL 
    [Timeout]  20 min 00 seconds
    [Setup]    get dut variable
    Step  1  Server Connect 1
    Step  2  Download SES FW File And Update Titan G2 WB  True
    Step  3  check ESM SES FW Version  True
    Step  4  check SES FW Version On Server lenovo  True
    [Teardown]  Run Keywords  Server Disconnect
           ...  AND OSDisconnect

CONSR-SEST-FWDL-0002-0001
    [Documentation]  Downgrade FW with mode 0x7
    [Tags]     CONSR-SEST-FWDL-0002-0001  Titan_G2_WB    Regression   FWDL    
    [Timeout]  30 min 00 seconds
    [Setup]    get dut variable
    Step  1  check esm mode status
    Step  2  Download SES FW File And Update Titan G2 WB  False
    Step  3  check ESM SES FW Version  False
    Step  4  check SES FW Version On Server lenovo  False
    Step  5  Download SES FW File And Update Titan G2 WB  True
    Step  6  check ESM SES FW Version  True
    Step  7  check SES FW Version On Server lenovo  True
    [Teardown]  Run Keywords  Server Disconnect
           ...  AND OSDisconnect

CONSR-SEST-FWDL-0005-0001
    [Documentation]  This test checks upgrade FW with mode 0xe + mode 0xf
    [Tags]     CONSR-SEST-FWDL-0005-0001  Titan_G2_WB    Regression      FWDL
    [Timeout]  30 min 00 seconds
    [Setup]    get dut variable
    Step  1  check esm mode status
    Step  2  Download SES FW File
    Step  3  upgrade FW with mode 0xe + mode 0xf Titan G2 WB
    Step  4  check SES FW Version On Server lenovo  True
    [Teardown]  Run Keywords  Server Disconnect
           ...  AND OSDisconnect

CONSR-SEST-FWDL-0008-0001
    [Documentation]  This test checks upgrade FW with mode 0xe + reset 03h code
    [Tags]     CONSR-SEST-FWDL-0008-0001  Titan_G2_WB    Regression       FWDL
    [Timeout]  30 min 00 seconds
    [Setup]    get dut variable
    Step  1  check esm mode status
    Step  2  Download SES FW File
    Step  3  upgrade FW with mode 0xe + reset 03h code Lenovo
    Step  4  check SES FW Version On Server lenovo  True
    [Teardown]  Run Keywords  Server Disconnect
           ...  AND OSDisconnect

CONSR-SEST-FWDL-0009-0001
    [Documentation]  This test checks upgrade FW with mode 0xe + power cycle
    [Tags]     CONSR-SEST-FWDL-0009-0001  Titan_G2_WB    Regression     FWDL 
    [Timeout]  30 min 00 seconds
    [Setup]    get dut variable
    Step  1  check esm mode status
    Step  2  Download SES FW File
    Step  3  upgrade FW with mode 0xe + power cycle Lenovo
    Step  4  check SES FW Version On Server lenovo  True
    [Teardown]  Run Keywords  Server Disconnect
           ...  AND OSDisconnect

CONSR-SEST-FWDL-0006-0001
    [Documentation]  This test checks upgrade FW with mode 0xe + reset 00h code
    [Tags]     CONSR-SEST-FWDL-0006-0001  Titan_G2_WB    Regression     FWDL
    [Timeout]  30 min 00 seconds
    [Setup]    get dut variable
    Step  1  check esm mode status
    Step  2  Download SES FW File
    Step  3  upgrade FW with mode 0xe + reset 00h code Titan G2 WB
    Step  4  check SES FW Version On Server lenovo  True
    [Teardown]  Run Keywords  Server Disconnect
           ...  AND OSDisconnect

CONSR-SEST-FWDL-0007-0001
    [Documentation]  This test checks upgrade FW with mode 0xe + reset 01h code
    [Tags]     CONSR-SEST-FWDL-0007-0001  Titan_G2_WB    Regression      FWDL
    [Timeout]  30 min 00 seconds
    [Setup]    get dut variable
    Step  1  check esm mode status
    Step  2  Download SES FW File
    Step  3  upgrade FW with mode 0xe + reset 01h code Lenovo
    Step  4  check SES FW Version On Server lenovo  True
    [Teardown]  Run Keywords  Server Disconnect
           ...  AND OSDisconnect

CONSR-SEST-FWDL-0010-0001
    [Documentation]  This test checks downgrade FW with mode 0xe + mode 0xf
    [Tags]     CONSR-SEST-FWDL-0010-0001  Titan_G2_WB    Regression       FWDL
    [Timeout]  60 min 00 seconds
    [Setup]    get dut variable
    Step  1  check esm mode status
    Step  2  Download SES FW File
    Step  3  downgrade FW with mode 0xe + mode 0xf Lenovo
    Step  4  upgrade FW with mode 0xe + mode 0xf Titan G2 WB
    Step  5  check SES FW Version On Server lenovo  True
    [Teardown]  Run Keywords  Server Disconnect
           ...  AND OSDisconnect

CONSR-SEST-FWDL-0011-0001
    [Documentation]  This test checks downgrade FW with mode 0xe + reset 00h code
    [Tags]     CONSR-SEST-FWDL-0011-0001  Titan_G2_WB    Regression     FWDL
    [Timeout]  60 min 00 seconds
    [Setup]    get dut variable
    Step  1  check esm mode status
    Step  2  Download SES FW File
    Step  3  downgrade FW with mode 0xe + reset 00h code Lenovo
    Step  4  upgrade FW with mode 0xe + reset 00h code Titan G2 WB
    Step  5  check SES FW Version On Server lenovo  True
    [Teardown]  Run Keywords  Server Disconnect
           ...  AND OSDisconnect

CONSR-SEST-FWDL-0012-0001
    [Documentation]  This test checks downgrade FW with mode 0xe + reset 01h code
    [Tags]     CONSR-SEST-FWDL-0012-0001  Titan_G2_WB    Regression       FWDL
    [Timeout]  50 min 00 seconds
    [Setup]    get dut variable
    Step  1  check esm mode status
    Step  2  Download SES FW File
    Step  3  downgrade FW with mode 0xe + reset 01h code Lenovo
    Step  4  upgrade FW with mode 0xe + reset 01h code Lenovo
    Step  5  check SES FW Version On Server lenovo  True
    [Teardown]  Run Keywords  Server Disconnect
           ...  AND OSDisconnect

CONSR-SEST-FWDL-0013-0001
    [Documentation]  This test checks downgrade FW with mode 0xe + reset 03h code
    [Tags]     CONSR-SEST-FWDL-0013-0001  Titan_G2_WB    Regression       FWDL
    [Timeout]  60 min 00 seconds
    [Setup]    get dut variable
    Step  1  check esm mode status
    Step  2  Download SES FW File
    Step  3  downgrade FW with mode 0xe + reset 03h code Lenovo
    Step  4  upgrade FW with mode 0xe + reset 03h code Lenovo
    Step  5  check SES FW Version On Server lenovo  True
    [Teardown]  Run Keywords  Server Disconnect
           ...  AND OSDisconnect

CONSR-SEST-FWDL-0014-0001
    [Documentation]  This test checks downgrade FW with mode 0xe + power cycle
    [Tags]     CONSR-SEST-FWDL-0014-0001  Titan_G2_WB    Regression       FWDL
    [Timeout]  50 min 00 seconds
    [Setup]    get dut variable
    Step  1  check esm mode status
    Step  2  Download SES FW File
    Step  3  downgrade FW with mode 0xe + power cycle
    Step  4  upgrade FW with mode 0xe + power cycle Lenovo
    Step  5  check SES FW Version On Server lenovo  True
    [Teardown]  Run Keywords  Server Disconnect
           ...  AND OSDisconnect

CONSR-SEST-STRS-0001-0001
    [Documentation]  This test checks stress upgrade/downgrade FW with mode 0xe
    [Tags]     CONSR-SEST-STRS-0001-0001  Titan_G2_WB    Regression   FWDL
    [Timeout]  48 hours
    [Setup]    get dut variable
    FOR    ${INDEX}    IN RANGE    ${MAXINDEX}
        Print Loop Info  ${INDEX}
    Step  1   check esm mode status
    Step  2   downgrade FW with mode 0xe + reset 00h code Lenovo
    Step  3   upgrade FW with mode 0xe + reset 00h code Titan G2 WB
    Step  4   downgrade FW with mode 0xe + mode 0xf Lenovo
    Step  5   upgrade FW with mode 0xe + mode 0xf Titan G2 WB
    Step  6   downgrade FW with mode 0xe + reset 01h code Lenovo
    Step  7   upgrade FW with mode 0xe + reset 01h code Lenovo
    Step  8   downgrade FW with mode 0xe + reset 03h code Lenovo
    Step  9   upgrade FW with mode 0xe + reset 03h code Lenovo
    Step  10  downgrade FW with mode 0xe + power cycle
    Step  11  upgrade FW with mode 0xe + power cycle Lenovo
    Step  12  check SES FW Version On Server lenovo  True
    END
    [Teardown]  Run Keywords  Server Disconnect
           ...  AND OSDisconnect

##########  Non Sanity Test-cases  ############################

CONSR-SEST-IVMT-0001-0001
    [Documentation]  This test case checks the canister A status - page 02h
    [Tags]   CONSR-SEST-IVMT-0001-0001   Titan_G2_WB     Non-Sanity   
    [Timeout]  5 min 00 seconds
    [Setup]    server Connect
    Step  1    verify cansiter status and FW version Titan G2 WB    ${page02_canisterA_cmd}    ${canisterA_status}
    [Teardown]  Server Disconnect

CONSR-SEST-IVMT-0007-0001
    [Documentation]  This test checks enclosure status - page 02h
    [Tags]   CONSR-SEST-IVMT-0007-0001   Titan_G2_WB     Non-Sanity   
    [Timeout]  8 min 00 seconds
    [Setup]    server Connect
    Step  1    check Command Pattern   ${pg2_enc_status_cmd}  ${pg2_enc_status}
    [Teardown]  Server Disconnect

CONSR-SEST-IVMT-0011-0001
    [Documentation]  This test case checks PSU 1 status - page 02h
    [Tags]     CONSR-SEST-IVMT-0011-0001  Titan_G2_WB     Non-Sanity   
    [Timeout]  5 min 00 seconds
    [Setup]    server Connect
    Step  1    check PSU status  ${psu1_status_pg2_cmd}  ${psu034_status_pg2_pattern}
    Step  2    Server Disconnect
    Step  3    CLI check for psu status Titan G2 WB  ${psu1_cli_pattern_titan_g2_wb}
    [Teardown]  Run Keywords  Server Disconnect
           ...  AND OSDisconnect

CONSR-SEST-IVMT-0012-0001
    [Documentation]  This test case checks PSU 2 status - page 02h
    [Tags]     CONSR-SEST-IVMT-0012-0001  Titan_G2_WB     Non-Sanity   
    [Timeout]  5 min 00 seconds
    [Setup]    server Connect
    Step  1    check PSU status  ${psu2_status_pg2_cmd}  ${psu034_status_pg2_pattern}
    Step  2    Server Disconnect
    Step  3    CLI check for psu status Titan G2 WB  ${psu2_cli_pattern_titan_g2_wb}
    [Teardown]  Run Keywords  Server Disconnect
           ...  AND OSDisconnect

CONSR-SEST-IVMT-0013-0001
    [Documentation]  This test case checks PSU 3 status - page 02h
    [Tags]     CONSR-SEST-IVMT-0013-0001  Titan_G2_WB     Non-Sanity   
    [Timeout]  5 min 00 seconds
    [Setup]    server Connect
    Step  1    check PSU status  ${psu3_status_pg2_cmd}  ${psu034_status_pg2_pattern}
    Step  2    Server Disconnect
    Step  3    CLI check for psu status Titan G2 WB  ${psu3_cli_pattern_titan_g2_wb}
    [Teardown]  Run Keywords  Server Disconnect
           ...  AND OSDisconnect

CONSR-SEST-IVMT-0014-0001
    [Documentation]  This test case checks PSU 0 Inventory - page 07h
    [Tags]     CONSR-SEST-IVMT-0014-0001  Titan_G2_WB     Non-Sanity   
    [Timeout]  5 min 00 seconds
    [Setup]    server Connect
    Step  1    compare PSU status with CLI Titan G2 WB  ${psu0_Find_pattern_titan_g2_wb}   ${psu0_status_pg7_cmd}  ${PSU1}
    [Teardown]  Server Disconnect

CONSR-SEST-SPCK-0038-0001
    [Documentation]  Threshold Out Diagnostic Pages(05h) - Temp LC
    [Tags]     CONSR-SEST-SPCK-0038-0001  Titan_G2_WB     Non-Sanity    
    [Timeout]  5 min 00 seconds
    [Setup]  server Connect
    Step  1  check Temperature Alarm On Page5  low critical
    Step  2  restore Temperature Threshold on Page5  low critical
    [Teardown]  Run Keywords  Server Disconnect

CONSR-SEST-SPCK-0039-0001
    [Documentation]  Threshold Out Diagnostic Pages(05h) - Temp LW
    [Tags]     CONSR-SEST-SPCK-0039-0001  Titan_G2_WB     Non-Sanity    
    [Timeout]  5 min 00 seconds
    [Setup]  server Connect
    Step  1  check Temperature Alarm On Page5  low warning
    Step  2  restore Temperature Threshold on Page5  low warning
    [Teardown]  Run Keywords  Server Disconnect

CONSR-SEST-SPCK-0040-0001
    [Documentation]  Threshold Out Diagnostic Pages(05h) - Temp UC
    [Tags]     CONSR-SEST-SPCK-0040-0001  Titan_G2_WB     Non-Sanity    
    [Timeout]  5 min 00 seconds
    [Setup]  server Connect
    Step  1  check Temperature Alarm On Page5  high critical
    Step  2  restore Temperature Threshold on Page5  high critical
    [Teardown]  Run Keywords  Server Disconnect

CONSR-SEST-SPCK-0041-0001
    [Documentation]  Threshold Out Diagnostic Pages(05h) - Temp UW
    [Tags]     CONSR-SEST-SPCK-0041-0001  Titan_G2_WB     Non-Sanity    
    [Timeout]  5 min 00 seconds
    [Setup]  server Connect
    Step  1  check Temperature Alarm On Page5  high warning
    Step  2  restore Temperature Threshold on Page5  high warning
    [Teardown]  Run Keywords  Server Disconnect

CONSR-SEST-SPCK-0042-0001
    [Documentation]  Threshold Out Diagnostic Pages(05h) - Voltage LC
    [Tags]     CONSR-SEST-SPCK-0042-0001  Titan_G2_WB     Non-Sanity    
    [Timeout]  5 min 00 seconds
    [Setup]  server Connect
    Step  1  check Sensor Alarm On Page5  low critical  Voltage sensor
    Step  2  restore Threshold on Page5  low critical  Voltage sensor
    [Teardown]  Run Keywords  Server Disconnect

CONSR-SEST-SPCK-0043-0001
    [Documentation]  Threshold Out Diagnostic Pages(05h) - Voltage LW
    [Tags]     CONSR-SEST-SPCK-0043-0001  Titan_G2_WB     Non-Sanity    
    [Timeout]  5 min 00 seconds
    [Setup]  server Connect
    Step  1  check Sensor Alarm On Page5  low warning  Voltage sensor
    Step  2  restore Threshold on Page5  low warning  Voltage sensor
    [Teardown]  Run Keywords  Server Disconnect

CONSR-SEST-SPCK-0044-0001
    [Documentation]  Threshold Out Diagnostic Pages(05h) - Voltage UC
    [Tags]     CONSR-SEST-SPCK-0044-0001  Titan_G2_WB     Non-Sanity    
    [Timeout]  5 min 00 seconds
    [Setup]  server Connect
    Step  1  check Sensor Alarm On Page5  high critical  Voltage sensor
    Step  2  restore Threshold on Page5  high critical  Voltage sensor
    [Teardown]  Run Keywords  Server Disconnect

CONSR-SEST-IVMT-0021-0001
    [Documentation]  This test case checks the array device disk Inventory - page 0Ah
    [Tags]     CONSR-SEST-IVMT-0021-0001  Titan_G2_WB     Non-Sanity    
    [Timeout]  5 min 00 seconds
    [Setup]    server Connect
    Step  1    Verify element index flag as invalid  ${page_0a_command}  ${sample_invalid_list_titan_g2_wb}  ${sample_invalid_list_titan_g2_wb}
    Step  4    Verify element index flag as valid    ${page_0a_command}  ${sample_valid_list_titan_g2_wb}    ${sample_valid_list_titan_g2_wb}
    [Teardown]  Server Disconnect

CONSR-SEST-SPCK-0031-0001
    [Documentation]  This test checks String Out Diagnostic Pages(04h) - Command Code and Data for Reset(A0h)
    [Tags]    CONSR-SEST-SPCK-0031-0001   Titan_G2_WB     Non-Sanity    
    [Timeout]  8 min 00 seconds
    Step  1    verify command code and data reset Titan G2 WB

CONSR-SEST-SPCK-0054-0001
    [Documentation]  SES Download microcode Control Diagnostic Page (mode 7)
                ...  - Checking download status
    [Tags]     CONSR-SEST-SPCK-0054-0001  Titan_G2_WB     Non-Sanity   
    [Timeout]  10 min 00 seconds
    [Setup]  server Connect
    Step  1     Download SES FW File And Check Downloading Status
           ...  ${download_microcode_mode7_cmd}
    [Teardown]  Run Keywords  Server Disconnect
           ...  AND OSDisconnect

CONSR-SEST-SPCK-0057-0001
    [Documentation]  SES Download microcode Status Diagnostic Page
    [Tags]     CONSR-SEST-SPCK-0057-0001  Titan_G2_WB     Non-Sanity   
    [Timeout]  10 min 00 seconds
    [Setup]  server Connect
    Step  1     check FW Download Status
    [Teardown]  Run Keywords  Server Disconnect
           ...  AND OSDisconnect

CONSR-SEST-CMDL-0002-0001
    [Documentation]  This test checks detailed CLI command setting and getting test
    [Tags]    CONSR-SEST-CMDL-0002-0001     Titan_G2_WB     Non-Sanity    
    [Timeout]  3 min 00 seconds
    [Setup]    Run Keywords  clearLogs
               ...  AND Server Connect
    Step  1    verify CLI set get CLI command
    [Teardown]  Server Disconnect

CONSR-SEST-SCSI-0001-0001
    [Documentation]  Test Unit Ready
    [Tags]     CONSR-SEST-SCSI-0001-0001  Titan_G2_WB     Non-Sanity   
    [Timeout]  5 min 00 seconds
    [Setup]     server Connect
    Step  1     check SCISI Elements  ${check_scsi_ready_cmd}  ${scsi_ready_pattern}
    [Teardown]  Server Disconnect

CONSR-SEST-SCSI-0002-0001
    [Documentation]  check Enclosure Length
    [Tags]     CONSR-SEST-SCSI-0002-0001  Titan_G2_WB     Non-Sanity   
    [Timeout]  5 min 00 seconds
    [Setup]     server Connect
    Step  1     check Enclosure Length  ${sg_inquiry_cmd}  ${sq_inquiry_pattern}
    ...         ${sq_inquiry_length}
    [Teardown]  Server Disconnect

CONSR-SEST-SCSI-0004-0001
    [Documentation]  SES Support Diagnostic Page - VPD 80h(Unit Serial Number)
    [Tags]     CONSR-SEST-SCSI-0004-0001  Titan_G2_WB     Non-Sanity   
    [Timeout]  5 min 00 seconds
    [Setup]     server Connect
    Step  1     check Enclosure Length  ${sg_inquiry_page_0x80_cmd}  ${sq_inquiry_pattern}
    ...         ${sq_inquiry_length}
    [Teardown]  Server Disconnect

CONSR-SEST-SCSI-0005-0001
    [Documentation]  SES Support Diagnostic Page - VPD 83h(Device Identication)
    [Tags]     CONSR-SEST-SCSI-0005-0001  Titan_G2_WB     Non-Sanity   
    [Timeout]  5 min 00 seconds
    [Setup]     server Connect
    Step  1     check SCISI Elements  ${sg_inquiry_page_0x83_cmd}  ${sg_inquiry_page_0x83_pattern}
    [Teardown]  Server Disconnect

CONSR-SEST-SCSI-0006-0001
    [Documentation]  SES Support Diagnostic Page
    [Tags]     CONSR-SEST-SCSI-0006-0001  Titan_G2_WB     Non-Sanity   
    [Timeout]  5 min 00 seconds
    [Setup]     server Connect
    Step  1     check Command Sent  sg_ses  ${fail_dict}
    [Teardown]  Server Disconnect

CONSR-SEST-SCSI-0012-0001
    [Documentation]  SCSI Support Diagnostic Page - Log Select
    [Tags]     CONSR-SEST-SCSI-0012-0001  Titan_G2_WB     Non-Sanity   
    [Timeout]  5 min 00 seconds
    [Setup]     server Connect
    Step  1     check SCISI Elements  ${set_log_sense_cmd}  ${set_log_sense_pattern}
    [Teardown]  Server Disconnect

CONSR-SEST-SCSI-0015-0001
    [Documentation]  SCSI Support Diagnostic Page - Mode Select (Protocol Specific Port Mode Page)
    [Tags]     CONSR-SEST-SCSI-0015-0001  Titan_G2_WB     Non-Sanity   
    [Timeout]  5 min 00 seconds
    [Setup]     server Connect
    Step  1     check Command Sent  ${select_protocol_specific_mode_cmd}  ${fail_dict}
    [Teardown]  Run Keywords  Server Disconnect
           ...  AND OSDisconnect

CONSR-SEST-SCSI-0016-0001
    [Documentation]  SCSI Support Diagnostic Page - MODE SENSE (18h)
    [Tags]     CONSR-SEST-SCSI-0016-0001  Titan_G2_WB     Non-Sanity   
    [Timeout]  5 min 00 seconds
    [Setup]     server Connect
    Step  1     check Command Pattern  ${mode_sense_page18_cmd}  ${mode_sense_page18_pattern}
    [Teardown]  Server Disconnect

CONSR-SEST-SCSI-0020-0001
    [Documentation]  This testcase checks the SCSI Support page - report LUNs
    [Tags]     CONSR-SEST-SCSI-0020-0001  Titan_G2_WB     Non-Sanity   
    [Timeout]  5 min 00 seconds
    [Setup]    server Connect
    Step  1    Verify lun report  ${scsi_support_ses_cmd}  ${scsi_option}   ${lun_ses_pattern}
    [Teardown]  Server Disconnect

CONSR-SEST-SCSI-0017-0001
    [Documentation]  SCSI Support Diagnostic Page - MODE SENSE (19h)
    [Tags]     CONSR-SEST-SCSI-0017-0001  Titan_G2_WB     Non-Sanity   
    [Timeout]  5 min 00 seconds
    [Setup]     server Connect
    Step  1     check Command Pattern  ${mode_sense_page19_cmd}  ${mode_sense_page19_pattern_titan_g2_wb}
    [Teardown]  Server Disconnect

CONSR-SEST-SCSI-0018-0001
    [Documentation]  SCSI Support Diagnostic Page - MODE SENSE (3Fh:00)
    [Tags]     CONSR-SEST-SCSI-0018-0001  Titan_G2_WB     Non-Sanity   
    [Timeout]  5 min 00 seconds
    [Setup]     server Connect
    Step  1     check Command Pattern  ${mode_sense_page3Fh_00_cmd}  ${mode_sense_page3Fh_00_pattern_titan_g2_wb}
    [Teardown]  Server Disconnect

CONSR-SEST-SCSI-0019-0001
    [Documentation]  SCSI Support Diagnostic Page - MODE SENSE  (3Fh:FF)
    [Tags]     CONSR-SEST-SCSI-0019-0001  Titan_G2_WB     Non-Sanity   
    [Timeout]  5 min 00 seconds
    [Setup]     server Connect
    Step  1     check Command Pattern  ${mode_sense_page3Fh_ff_cmd}  ${mode_sense_page3Fh_ff_pattern_titan_g2_wb}
    [Teardown]  Server Disconnect

CONSR-SEST-CLMT-0001-0001
    [Documentation]  This test checks SES Enclosure Control Page Cooling element- current speed
    [Tags]   CONSR-SEST-CLMT-0001-0001   Titan_G2_WB     Non-Sanity   
    [Timeout]  8 min 00 seconds
    [Setup]    get dut variable
    Step  1    check fan speed Titan G2 WB   ${fan_speed_10}   ${fan_speed_10_l75cli}    ${fan_speed_10_g75cli}
    Step  2    check fan speed Titan G2 WB   ${fan_speed_11}   ${fan_speed_11_l75cli}    ${fan_speed_11_g75cli}
    Step  3    check fan speed Titan G2 WB   ${fan_speed_12}   ${fan_speed_12_l75cli}    ${fan_speed_12_g75cli}
    Step  4    check fan speed Titan G2 WB   ${fan_speed_13}   ${fan_speed_13_l75cli}    ${fan_speed_13_g75cli}
    [Teardown]  Run Keywords  Server Disconnect
           ...  AND OSDisconnect

CONSR-SEST-CLMT-0002-0001
    [Documentation]  This test checks SES Enclosure Control Page Cooling element- lowest fan speed
    [Tags]   CONSR-SEST-CLMT-0002-0001  Titan_G2_WB     Non-Sanity   
    [Timeout]  5 min 00 seconds
    [Setup]    get dut variable
    Step  1    check fan speed Titan G2 WB  ${fan_min_speed}   ${fan_min_speed_l75cli}    ${fan_min_speed_g75cli}
    [Teardown]  Run Keywords  Server Disconnect
           ...  AND OSDisconnect

CONSR-SEST-CLMT-0003-0001
    [Documentation]  This test checks SES Enclosure Control Page Cooling element- highest speed
    [Tags]   CONSR-SEST-CLMT-0003-0001  Titan_G2_WB     Non-Sanity   
    [Timeout]  5 min 00 seconds
    [Setup]    get dut variable
    Step  1    check fan speed Titan G2 WB  ${fan_max_speed_titan_g2_wb}   ${fan_max_speed_l75cli}    ${fan_max_speed_g75cli}
    [Teardown]  Run Keywords  Server Disconnect
           ...  AND OSDisconnect

CONSR-SEST-IVMT-0002-0001
    [Documentation]  This test case checks the canister B status - page 02h
    [Tags]   CONSR-SEST-IVMT-0002-0001   Titan_G2_WB     Non-Sanity    
    [Timeout]  5 min 00 seconds
    [Setup]    server Connect
    Step  1   verify canister status  ${page02_canisterB_cmd}    ${canisterB_status_titan_G2_WB}
    [Teardown]  Server Disconnect

CONSR-SEST-IVMT-0003-0001
    [Documentation]  This test case Check the canister A Inventory - page 07h
    [Tags]     CONSR-SEST-IVMT-0003-0001  Titan_G2_WB     Non-Sanity    
    [Timeout]  5 min 00 seconds
    [Setup]    server Connect
    Step  1    Verify canister details on CLI and page command Titan G2 WB  ${canister_a_ses_cmd}  ${canister_CLI_cmd}
    [Teardown]  Server Disconnect

CONSR-SEST-IVMT-0004-0001
    [Documentation]  This test case Check the canister B Inventory - page 07h
    [Tags]     CONSR-SEST-IVMT-0004-0001  Titan_G2_WB     Non-Sanity   
    [Timeout]  5 min 00 seconds
    [Setup]    server Connect
    Step  1    Verify canister B inventory in page command   ${canister_b_ses_cmd}   ${canister_b_pattern}
    [Teardown]  Server Disconnect

CONSR-SEST-IVMT-0008-0001
    [Documentation]  This test checks the enclosure Inventory - page 07h
    [Tags]   CONSR-SEST-IVMT-0008-0001   Titan_G2_WB     Non-Sanity   
    [Timeout]  5 min 00 seconds
    [Setup]    server Connect
    Step  1    Verify Enclosure Inventory details on CLI and page command Titan G2 WB  ${Inventory_ses_cmd}  ${Inventory_CLI_cmd}
    [Teardown]  Server Disconnect

CONSR-SEST-IVMT-0010-0001
    [Documentation]  This test case checks PSU 0 status - page 02h
    [Tags]    CONSR-SEST-IVMT-0010-0001  Titan_G2_WB     Non-Sanity   
    [Timeout]  5 min 00 seconds
    [Setup]    server Connect
    Step  1    check PSU status  ${psu0_status_pg2_cmd}  ${psu034_status_pg2_pattern}
    Step  2    Server Disconnect
    Step  3    CLI check for psu status Titan G2 WB  ${psu0_cli_pattern_titan_g2_wb}
    [Teardown]  Run Keywords  Server Disconnect
           ...  AND OSDisconnect

CONSR-SEST-IVMT-0015-0001
    [Documentation]  This test case checks PSU 1 Inventory - page 07h
    [Tags]     CONSR-SEST-IVMT-0015-0001  Titan_G2_WB     Non-Sanity    
    [Timeout]  5 min 00 seconds
    [Setup]    server Connect
    Step  1    compare PSU status with CLI Titan G2 WB  ${psu1_Find_pattern_titan_g2_wb}   ${psu1_status_pg7_cmd}  ${PSU2}
    [Teardown]  Server Disconnect

CONSR-SEST-IVMT-0016-0001
    [Documentation]  This test case checks PSU 2 Inventory - page 07h
    [Tags]     CONSR-SEST-IVMT-0016-0001  Titan_G2_WB     Non-Sanity   
    [Timeout]  5 min 00 seconds
    [Setup]    server Connect
    Step  1    compare PSU status with CLI Titan G2 WB  ${psu2_Find_pattern_titan_g2_wb}   ${psu2_status_pg7_cmd}  ${PSU3}
    [Teardown]  Server Disconnect

CONSR-SEST-IVMT-0017-0001
    [Documentation]  This test case checks PSU 3 Inventory - page 07h
    [Tags]     CONSR-SEST-IVMT-0017-0001  Titan_G2_WB     Non-Sanity   
    [Timeout]  5 min 00 seconds
    [Setup]    server Connect
    Step  1    compare PSU status with CLI Titan G2 WB  ${psu3_Find_pattern_titan_g2_wb}   ${psu3_status_pg7_cmd}  ${PSU4}
    [Teardown]  Server Disconnect

CONSR-SEST-IVMT-0019-0001
    [Documentation]  This test checks the array device disk status - page 02h
    [Tags]   CONSR-SEST-IVMT-0019-0001  Titan_G2_WB     Non-Sanity    
    [Timeout]  5 min 00 seconds
    [Setup]    server Connect
    Step  1   check driver status  ${page_drvstatus_cmd}  ${drv0_29}   ${OK_status_titan_g2_wb}  ${OK_status_titan_g2_wb}
    Step  2   check driver status  ${page_drvstatus_cmd}  ${drv30_59}  ${OK_status_titan_g2_wb}  ${OK_status_titan_g2_wb}
    Step  3   check driver status  ${page_drvstatus_cmd}  ${drv75_82}  ${OK_status_titan_g2_wb}  ${OK_status_titan_g2_wb}
    Step  4   check driver status  ${page_drvstatus_cmd}  ${drv60_66}  ${OK_status_titan_g2_wb}  ${OK_status_titan_g2_wb}
    Step  5   check driver status  ${page_drvstatus_cmd}  ${drv67_74}  ${OK_status_titan_g2_wb}  ${OK_status_titan_g2_wb}
    Step  6   check driver status  ${page_drvstatus_cmd}  ${drv83_89}  ${OK_status_titan_g2_wb}  ${OK_status_titan_g2_wb}
    [Teardown]  Server Disconnect

CONSR-SEST-IVMT-0020-0001
    [Documentation]  This test checks the array device disk Inventory - page 07h
    [Tags]   CONSR-SEST-IVMT-0020-0001  Titan_G2_WB     Non-Sanity    
    [Timeout]  5 min 00 seconds
    [Setup]    server Connect
    Step  1   check slot name format  ${page7_slotname_check_cmd}
    [Teardown]  Server Disconnect

CONSR-SEST-IVMT-0026-0001
    [Documentation]  This test checks the Fan VPD
    [Tags]   CONSR-SEST-IVMT-0026-0001   Titan_G2_WB     Non-Sanity   
    [Timeout]  5 min 00 seconds
    [Setup]    OSConnect
    Step  1    ModifyFanSerialAndHWECNumber_titan_g2_wb
    [Teardown]  OSDisconnect

CONSR-SEST-IVMT-0027-0001
    [Documentation]  This test checks the modification of canister MFG date.
    [Tags]   CONSR-SEST-IVMT-0027-0001   Titan_G2_WB     Non-Sanity   
    [Timeout]  15 min 00 seconds
    [Setup]    OSConnect
    Step  1    Verify configuring and validating manufacturer date Titan G2 WB  ${date_set_cmd1}  ${mfg_date_pattern1}
    Step  2    Verify configuring and validating manufacturer date Titan G2 WB  ${date_set_cmd2}  ${mfg_date_pattern2}
    [Teardown]  OSDisconnect

CONSR-SEST-SPCK-0045-0001
    [Documentation]  Threshold Out Diagnostic Pages(05h) - Voltage UW
    [Tags]     CONSR-SEST-SPCK-0045-0001  Titan_G2_WB     Non-Sanity    
    [Timeout]  5 min 00 seconds
    [Setup]  server Connect
    Step  1  check Sensor Alarm On Page5  high warning  Voltage sensor
    Step  2  restore Threshold on Page5  high warning  Voltage sensor
    [Teardown]  Run Keywords  Server Disconnect

CONSR-SEST-SPCK-0055-0001
    [Documentation]  SES Download microcode Control Diagnostic Page (mode E)
                ...  - Checking download status
    [Tags]     CONSR-SEST-SPCK-0055-0001  Titan_G2_WB       FWDL    
    [Timeout]  10 min 00 seconds
    [Setup]  server Connect
    Step  1     Download SES FW File And Check Downloading Status Without Activate Titan G2 WB   
           ...  ${download_microcode_modeE_cmd}
    [Teardown]  Run Keywords  Server Disconnect

CONSR-SEST-SPCK-0056-0001
    [Documentation]  SES Download microcode Control Diagnostic Page (mode F)
                ...  - Checking download status
    [Tags]     CONSR-SEST-SPCK-0056-0001  Titan_G2_WB        FWDL    
    [Timeout]  10 min 00 seconds
    [Setup]  server Connect
    Step  1     activate New FW Partition Titan G2 WB  ${download_microcode_modeE_cmd}
    [Teardown]  Run Keywords  Server Disconnect

CONSR-SEST-CLMT-0006-0001
    [Documentation]  This test checks Temperature Monitoring
    [Tags]   CONSR-SEST-CLMT-0006-0001   Titan_G2_WB     Non-Sanity    
    [Timeout]  8 min 00 seconds
    [Setup]    server Connect
    Step  1    set and verify UW
    Step  2    set and verify UC
    Step  3    set and verify LW
    Step  4    set and verify LC
    [Teardown]  Server Disconnect

CONSR-SEST-SPCK-0058-0001
    [Documentation]  This test case checks Log Control Diagnostic Page (13h) - get log info
    [Tags]     CONSR-SEST-SPCK-0058-0001  Titan_G2_WB     Non-Sanity    
    [Timeout]  5 min 00 seconds
    [Setup]    Run Keywords  clearLogs
               ...  AND Server Connect
    Step  1    send a command   ${page13_readlog_cmd}
    Step  2    compare log info with CLI Titan G2 WB    ${page_13_status_cmd}
    [Teardown]  Server Disconnect

CONSR-SEST-SPCK-0059-0001
    [Documentation]  This test checks Log Control Diagnostic Page (13h) - Log Misc Control
    [Tags]   CONSR-SEST-SPCK-0059-0001  Titan_G2_WB     Non-Sanity    
    [Timeout]  5 min 00 seconds
    [Setup]    Run Keywords  clearLogs
               ...  AND Server Connect   
    Step  1    send a command   ${page_13_new_log_check_cmd}
    Step  2    compare new log with CLI Titan G2 WB  ${page_13_status_cmd}
    Step  3    send a command  ${page_13_read_status_cmd}
    Step  4    Verify log pattern  ${page_13_status_cmd}  ${log_read_code}  ${page_13_read_status_pattern}
    Step  5    send a command  ${page_13_unread_status_cmd}
    Step  6    Verify log pattern  ${page_13_status_cmd}  ${log_unread_code}  ${page_13_unread_status_pattern}
    Step  7    send a command  ${page_13_clear_log_cmd}
    Step  8    Verify log pattern   ${page_13_status_cmd}  ${clear_log_entry_code}  ${clear_log_entry_pattern}
    Step  9    CLI check for log entry Titan G2 WB
    [Teardown]  Server Disconnect

CONSR-SEST-SPCK-0060-0001
    [Documentation]  This test checks Log Control Diagnostic Page (13h) - Get Log Entry Descriptor
    [Tags]   CONSR-SEST-SPCK-0060-0001  Titan_G2_WB     Non-Sanity    
    [Timeout]  5 min 00 seconds
    [Setup]    Run Keywords  clearLogs
               ...  AND Server Connect
    Step  1    get Control Decscriptor Information   ${page_13_entries_num_cmd}
    Step  2    Verify log pattern   ${page_13_status_cmd}  ${log_entry_code}  ${clear_log_entry_pattern}
    Step  3    get Control Decscriptor Information   ${page_13_clear_log_cmd}
    Step  4    Verify log pattern   ${page_13_status_cmd}  ${clear_log_entry_code}  ${clear_log_entry_pattern}
    Step  5    CLI check for log entry Titan G2 WB
    [Teardown]  Server Disconnect

CONSR-SEST-SPCK-0061-0001
    [Documentation]  This test case checks Log Status Diagnostic Page (13h) - page status
    [Tags]     CONSR-SEST-SPCK-0061-0001  Titan_G2_WB     Non-Sanity    
    [Timeout]  5 min 00 seconds
    [Setup]    Run Keywords  clearLogs
               ...  AND Server Connect
    Step  1    send a command  ${Page13_run_diag_command}
    Step  2    verify Page Status  ${page_13_status_cmd}
    [Teardown]  Server Disconnect

CONSR-SEST-FWDL-0030-0001
    [Documentation]  SES Download microcode Control Diagnostic Page
                ...  - remove Power during downloading image
    [Tags]     CONSR-SEST-FWDL-0030-0001  Titan_G2_WB      Non-Sanity      FWDL
    [Timeout]  10 min 00 seconds
    [Setup]  server Connect
    Step  1  Download SES FW File And Power Cycle Titan G2 WB  ${download_microcode_mode7_cmd}
    [Teardown]  Server Disconnect

CONSR-SEST-FWDL-0031-0001
    [Documentation]  SES Download microcode Control Diagnostic Page
                ...  - remove Power during downloading image
    [Tags]     CONSR-SEST-FWDL-0031-0001  Titan_G2_WB     Non-Sanity        FWDL
    [Timeout]  10 min 00 seconds
    [Setup]  server Connect
    Step  1  Download SES FW File And Power Cycle Titan G2 WB   ${download_microcode_modeE_cmd}
    [Teardown]  Server Disconnect

CONSR-SEST-FWDL-0032-0001
    [Documentation]  SES Download microcode Control Diagnostic Page
                ...  - Input new command to interrupt downloading image
                ...    under mode 0xe
    [Tags]     CONSR-SEST-FWDL-0032-0001  Titan_G2_WB     Non-Sanity   FWDL
    [Timeout]  10 min 00 seconds
    [Setup]  server Connect
    Step  1     Download SES FW File And Interrupt with command Titan G2 WB
           ...  ${download_microcode_modeE_cmd}
    [Teardown]  Server Disconnect

CONSR-SEST-FWDL-0033-0001
    [Documentation]  SES Download microcode Control Diagnostic Page
                ...  - Input new command to interrupt downloading image
                ...    under mode 7
    [Tags]     CONSR-SEST-FWDL-0033-0001  Titan_G2_WB     Non-Sanity   FWDL
    [Timeout]  10 min 00 seconds
    [Setup]  server Connect
    Step  1     Download SES FW File And Interrupt with command Titan G2 WB
           ...  ${download_microcode_mode7_cmd}
    [Teardown]  Server Disconnect

CONSR-SEST-FWDL-0034-0001
    [Documentation]  This test checks upgrade cpld via SES Page - mode 0xe and 0xf
    [Tags]     CONSR-SEST-FWDL-0034-0001  Titan_G2_WB     Non-Sanity   FWDL
    [Timeout]  30 min 00 seconds
    [Setup]    get dut variable
    Sub-Case  CONSR-SEST-FWDL-0034-0001_1  check esm mode status
    Sub-Case  CONSR-SEST-FWDL-0034-0001_2  Download CPLD FW File
    Sub-Case  CONSR-SEST-FWDL-0034-0001_3  upgrade cpld with mode 0xe + mode 0xf Titan G2 WB
    Sub-Case  CONSR-SEST-FWDL-0034-0001_4  check esm mode status
    [Teardown]  Run Keywords  Server Disconnect
           ...  AND OSDisconnect

CONSR-SEST-FWDL-0035-0001
    [Documentation]  This test checks upgrade cpld via SES Page - mode 0xe and reset 00h
    [Tags]     CONSR-SEST-FWDL-0035-0001  Titan_G2_WB     Non-Sanity   FWDL
    [Timeout]  30 min 00 seconds
    [Setup]    get dut variable
    Sub-Case  CONSR-SEST-FWDL-0035-0001_1  check esm mode status
    Sub-Case  CONSR-SEST-FWDL-0035-0001_2  Download CPLD FW File
    Sub-Case  CONSR-SEST-FWDL-0035-0001_3  upgrade cpld with mode 0xe + reset 00h Titan G2 WB
    Sub-Case  CONSR-SEST-FWDL-0035-0001_4  check esm mode status
    [Teardown]  Run Keywords  Server Disconnect
           ...  AND OSDisconnect

CONSR-SEST-FWDL-0036-0001
    [Documentation]  This test checks upgrade cpld via SES Page - mode 0xe and power cycle
    [Tags]     CONSR-SEST-FWDL-0036-0001  Titan_G2_WB     Non-Sanity   FWDL
    [Timeout]  30 min 00 seconds
    [Setup]    get dut variable
    Sub-Case  CONSR-SEST-FWDL-0036-0001_1  check esm mode status
    Sub-Case  CONSR-SEST-FWDL-0036-0001_2  Download CPLD FW File
    Sub-Case  CONSR-SEST-FWDL-0036-0001_3  upgrade cpld with mode 0xe + power cycle Titan G2 WB
    Sub-Case  CONSR-SEST-FWDL-0036-0001_4  check esm mode status
    [Teardown]  Run Keywords  Server Disconnect
           ...  AND OSDisconnect

CONSR-SEST-FWDL-0037-0001
    [Documentation]  This test checks downgrade cpld via SES Page - mode 0xe and 0xf
    [Tags]     CONSR-SEST-FWDL-0037-0001  Titan_G2_WB     Non-Sanity   FWDL
    [Timeout]  30 min 00 seconds
    [Setup]    get dut variable
    Sub-Case  CONSR-SEST-FWDL-0037-0001_1  Download CPLD FW File
    Sub-Case  CONSR-SEST-FWDL-0037-0001_2  downgrade cpld with mode 0xe + mode 0xf Titan G2 WB
    Sub-Case  CONSR-SEST-FWDL-0037-0001_3  check esm mode status
    Sub-Case  CONSR-SEST-FWDL-0037-0001_4  upgrade cpld with mode 0xe + mode 0xf Titan G2 WB
    Sub-Case  CONSR-SEST-FWDL-0037-0001_5  check esm mode status
    [Teardown]  Run Keywords  Server Disconnect
           ...  AND OSDisconnect

CONSR-SEST-FWDL-0038-0001
    [Documentation]  This test checks downgrade cpld via SES Page - mode 0xe  + reset 00h
    [Tags]     CONSR-SEST-FWDL-0038-0001  Titan_G2_WB     Non-Sanity   FWDL
    [Timeout]  30 min 00 seconds
    [Setup]    get dut variable
    Sub-Case  CONSR-SEST-FWDL-0038-0001_1  Download CPLD FW File
    Sub-Case  CONSR-SEST-FWDL-0038-0001_2  downgrade cpld with mode 0xe + reset 00h Titan G2 WB
    Sub-Case  CONSR-SEST-FWDL-0038-0001_3  check esm mode status
    Sub-Case  CONSR-SEST-FWDL-0038-0001_4  upgrade cpld with mode 0xe + reset 00h Titan G2 WB
    Sub-Case  CONSR-SEST-FWDL-0038-0001_5  check esm mode status
    [Teardown]  Run Keywords  Server Disconnect
           ...  AND OSDisconnect

CONSR-SEST-FWDL-0039-0001
    [Documentation]  This test checks downgrade cpld via SES Page - mode 0xe  + power cycle
    [Tags]     CONSR-SEST-FWDL-0039-0001  Titan_G2_WB     Non-Sanity   FWDL
    [Timeout]  30 min 00 seconds
    [Setup]    get dut variable
    Sub-Case  CONSR-SEST-FWDL-0039-0001_1  Download CPLD FW File
    Sub-Case  CONSR-SEST-FWDL-0039-0001_2  downgrade cpld with mode 0xe + power cycle Titan G2 WB
    Sub-Case  CONSR-SEST-FWDL-0039-0001_3  check esm mode status
    Sub-Case  CONSR-SEST-FWDL-0039-0001_4  upgrade cpld with mode 0xe + power cycle Titan G2 WB
    Sub-Case  CONSR-SEST-FWDL-0039-0001_5  check esm mode status
    [Teardown]  Run Keywords  Server Disconnect
           ...  AND OSDisconnect

CONSR-SEST-CLMT-0007-0001
    [Documentation]  This test checks Fan Status Monitoring
    [Tags]   CONSR-SEST-CLMT-0007-0001   Titan_G2_WB     Non-Sanity    
    [Timeout]  8 min 00 seconds
    [Setup]    get dut variable
    Step  1    set and verify fan control mode Titan G2 WB
    Step  2    set and verify pwm value Titan G2 WB
    Step  3    set and verify level Titan G2 WB
    [Teardown]  Run Keywords  Server Disconnect
           ...  AND OSDisconnect

CONSR-SEST-FWDL-0028-0001
    [Documentation]  SES Download microcode Control Diagnostic Page
                ...  - with wrong image file under mode 7
    [Tags]     CONSR-SEST-FWDL-0028-0001  Titan_G2_WB     Non-Sanity
    [Timeout]  10 min 00 seconds
    [Setup]  server Connect
    Step  1  download And Verify With FW Fault Image Titan G2 WB
    [Teardown]  Run Keywords  Server Disconnect
           ...  AND OSDisconnect

CONSR-SEST-FWDL-0029-0001
    [Documentation]  SES Download microcode Control Diagnostic Page
                ...  - with wrong image file under mode 0xe
    [Tags]     CONSR-SEST-FWDL-0029-0001  Titan_G2_WB     Non-Sanity
    [Timeout]  10 min 00 seconds
    [Setup]  server Connect
    Step  1  Verify With FW Fault Image Under Mode E Titan G2 WB
    [Teardown]  Run Keywords  Server Disconnect
           ...  AND OSDisconnect

CONSR-SEST-SMRD-0039-0001
    [Documentation]  This test checks Threshold Out Diagnostic Pages(05h) - Temp LW
    [Tags]  CONSR-SEST-SMRD-0039-0001  Titan_G2_WB     Non-Sanity    
    [Timeout]  5 min 00 seconds
    [Setup]  server Connect
    Step  1  Temperature lm Upgrade Test Titan G2 WB  0  ^0$
    Step  2  OSConnect
    Step  3  verify_esm_fan_mode_cli_command  DUT  internal
    Step  4  execute_ESM_command  $%^1\r
    Step  5  OSDisconnect
    [Teardown]  Server Disconnect

CONSR-SEST-SMRD-0040-0001
    [Documentation]  This test checks Threshold Out Diagnostic Pages(05h) - Temp UC
    [Tags]  CONSR-SEST-SMRD-0040-0001  Titan_G2_WB     Non-Sanity    
    [Timeout]  5 min 00 seconds
    [Setup]  server Connect
    Step  1  Temperature lm Upgrade Test Titan G2 WB  1  ^1$
    Step  2  ConnectESMB
    Step  3  verify_esm_fan_mode_cli_command  DUT  external
    Step  4  execute_ESM_command  $%^1\r
    Step  5  OSDisconnect
    [Teardown]  Server Disconnect

CONSRS-SM-01-0001
    [Documentation]  This test checks SMP General Commands
    [Tags]    CONSRS-SM-01-0001   Titan_G2_WB     Non-Sanity   
    [Timeout]  5 min 00 seconds
    [Setup]    server Connect
    Step  1    verify SMP commands
    [Teardown]  Server Disconnect

CONSRS-SM-04-0001
    [Documentation]  This test checks  SMP PHY Control -  phy enable/disable
    [Tags]  CONSRS-SM-04-0001  Titan_G2_WB     Non-Sanity   
    [Timeout]  10 min 00 seconds
    [Setup]    server Connect
    Step  1    verify smp phy enable disable Titan G2 WB
    [Teardown]  Server Disconnect

CONSRS-SM-05-0001
     [Documentation]  This test checks partial pathway timeout
     [Tags]   CONSRS-SM-05-0001   Titan_G2_WB     Non-Sanity   
     [Timeout]  5 min 00 seconds
     [Setup]    server Connect
     Step  1    Setting partial pathway timeout value Titan G2 WB
     [Teardown]  Server Disconnect

CONSR-SEST-SPCK-0073-0001
    [Documentation]  This test checks Enclosure Control Diagnostic Pages(02h) - ESCE report bit
    [Tags]   CONSR-SEST-SPCK-0073-0001   Titan_G2_WB     Non-Sanity   
    [Timeout]  8 min 00 seconds
    [Setup]    Server Connect 1
    Step  1    verify ESCE report bit  ${pg2_esc0_cmd}  ${pg2_esc1_cmd}  ${reset_exp_cmd}  ${esc0_report_bit}  ${esc1_report_bit}
    [Teardown]  Server Disconnect

CONSR-SEST-SPCK-0093-0001
    [Documentation]  This test checks Log Status Diagnostic Page (13h)- with wrong data
    [Tags]   CONSR-SEST-SPCK-0093-0001   Titan_G2_WB     Non-Sanity    
    [Timeout]  8 min 00 seconds
    [Setup]    Server Connect
    Step  1    verify log with wrong data   ${log_wrongdata_cmd}
    [Teardown]  Server Disconnect

##########  Semi Automated Test-cases  ############################


CONSR-SEST-SCSI-0003-0001
    [Documentation]  SES Support Diagnostic Page - VPD 00h(Supported VPD)
    [Tags]     CONSR-SEST-SCSI-0003-0001  Titan_G2_WB     Semi-Automated
    [Timeout]  5 min 00 seconds
    [Setup]     server Connect
    Step  1     check SCISI Elements  ${sg_inquiry_page_0x00_cmd}  ${sg_inquiry_page_0x00_pattern}
    [Teardown]  Server Disconnect

CONSR-SEST-SPCK-0066-0001
    [Documentation]  This test checks Error Injection Control Diagnostic Page (15h) - Control Descriptor List (PS)
    [Tags]  CONSR-SEST-SPCK-0066-0001  Titan_G2_WB     Semi-Automated
    [Timeout]  5 min 00 seconds
    [Setup]  server Connect
    Step  1  error Injection Control Diagnostic Page Trigger   ${ses_page_tool_cmd}  ${elem_id_0}  ${psu_trigger_on_value}  ${psu_trigger_on_pattern_0_titan_g2_wb}  ${page_15_status_cmd}  ${page_15_psu_trigger_on_pattern_0_titan_g2_wb}
    Step  2  error Injection Control Diagnostic Page Trigger   ${ses_page_tool_cmd}  ${elem_id_0}  ${psu_trigger_off_value}  ${psu_trigger_off_pattern_0_titan_g2_wb}  ${page_15_status_cmd}  ${page_15_psu_trigger_off_pattern_0_titan_g2_wb}
    [Teardown]  Server Disconnect

CONSR-SEST-SPCK-0067-0001
    [Documentation]  This test checks Error Injection Control Diagnostic Page (15h) - Control Descriptor List (Cooling)
    [Tags]  CONSR-SEST-SPCK-0067-0001  Titan_G2_WB     Semi-Automated
    [Timeout]  5 min 00 seconds
    [Setup]  server Connect
    Step  1  error Injection Control Diagnostic Page Trigger   ${ses_page_tool_cmd}  ${elem_id_2}  ${cooling_trigger_on_value}  ${cooling_trigger_on_pattern_2_titan_g2_wb}  ${page_15_status_cmd}  ${page_15_cooling_trigger_on_pattern_2_titan_g2_wb}
    Step  2  error Injection Control Diagnostic Page Trigger   ${ses_page_tool_cmd}  ${elem_id_2}  ${cooling_trigger_off_value}  ${cooling_trigger_off_pattern_2_titan_g2_wb}  ${page_15_status_cmd}  ${page_15_cooling_trigger_off_pattern_2_titan_g2_wb}
    [Teardown]  Server Disconnect

CONSR-SEST-SPCK-0068-0001
    [Documentation]  This test checks Error Injection Control Diagnostic Page (15h) - Control Descriptor List (temp)
    [Tags]  CONSR-SEST-SPCK-0068-0001  Titan_G2_WB     Semi-Automated
    [Timeout]  5 min 00 seconds
    [Setup]  server Connect
    Step  1  error Injection Control Diagnostic Page Trigger   ${ses_page_tool_cmd}  ${elem_id_6}  ${temp_trigger_on_value}  ${temp_trigger_on_pattern_6_titan_g2_wb}  ${page_15_status_cmd}  ${page_15_temp_trigger_on_pattern_6_titan_g2_wb}
    Step  2  error Injection Control Diagnostic Page Trigger   ${ses_page_tool_cmd}  ${elem_id_6}  ${temp_trigger_off_value}  ${temp_trigger_off_pattern_6_titan_g2_wb}  ${page_15_status_cmd}  ${page_15_temp_trigger_off_pattern_6_titan_g2_wb}
    [Teardown]  Server Disconnect

CONSR-SEST-SPCK-0069-0001
    [Documentation]  This test checks Error Injection Control Diagnostic Page (15h) - Control Descriptor List (Voltage)
    [Tags]  CONSR-SEST-SPCK-0069-0001  Titan_G2_WB     Semi-Automated    
    [Timeout]  5 min 00 seconds
    [Setup]  server Connect
    Step  1  error Injection Control Diagnostic Page Trigger   ${ses_page_tool_cmd}  ${elem_id_4}  ${voltage_trigger_on_value}  ${voltage_trigger_on_pattern_4_titan_g2_wb}  ${page_15_status_cmd}  ${page_15_voltage_trigger_on_pattern_4_titan_g2_wb}
    Step  2  error Injection Control Diagnostic Page Trigger   ${ses_page_tool_cmd}  ${elem_id_4}  ${voltage_trigger_off_value}  ${voltage_trigger_off_pattern_4_titan_g2_wb}  ${page_15_status_cmd}  ${page_15_voltage_trigger_off_pattern_4_titan_g2_wb}
    [Teardown]  Server Disconnect

CONSR-SEST-SPCK-0071-0001
    [Documentation]  Error Injection Control Diagnostic Page (15h) - Configuration Descriptor
    [Tags]     CONSR-SEST-SPCK-0071-0001  Titan_G2_WB     Semi-Automated
    [Timeout]  5 min 00 seconds
    [Setup]     server Connect
    Step  1    get Control Decscriptor Information  ${control_descriptor_cmd}
    Step  2    check Command Pattern  ${page_15_status_cmd}  ${page_15_status_pattern}
    [Teardown]  Server Disconnect

CONSR-SEST-STRS-0003-0001
    [Documentation]   Canister LED stress Test
    [Tags]     CONSR-SEST-STRS-0003-0001  Titan_G2_WB     Semi-Automated
    [Timeout]  24 hours
    [Setup]  server Connect
    FOR    ${INDEX}    IN RANGE    ${MAXINDEX}
        Print Loop Info  ${INDEX}
        Step  1  verify canister LED on off status  ${set_canister_ident_on}  ${clear_canister_ident}  ${check_can_ident0_cmd}  ${check_can_ident1_cmd}  ${get_ident_LED}   ${can_iden_on_pattern}  ${can_ident_off_pattern}  ${can_ident_on_pattern_total}
        Step  2  verify canister LED on off status  ${set_canister_fault_on}  ${clear_canister_fault}  ${check_can_fault0_cmd}  ${check_can_fault1_cmd}  ${get_LED_8}  ${can_fault_on_pattern}  ${can_fault_off_pattern}  ${can_fault_on_pattern_total}

    END
    [Teardown]  Run Keywords  Server Disconnect

CONSR-SEST-STRS-0004-0001
    [Documentation]  Enclosure LED Stress Test
    [Tags]     CONSR-SEST-STRS-0004-0001  Titan_G2_WB     Semi-Automated
    [Timeout]  24 hours
    [Setup]  server Connect
    FOR    ${INDEX}    IN RANGE    ${MAXINDEX}
        Print Loop Info  ${INDEX}
        Step  1  verify Enclosure LED on off status  ${set_on_enc_LED}   ${set_off_enc_LED}  ${get_cmd}  ${get_page2_cmd}  ${get_enc_LED}  ${enc_LED_on_pattern}  ${enc_LED_off_pattern}
    END
    [Teardown]  Run Keywords  Server Disconnect

CONSR-SEST-STRS-0007-0001
     [Documentation]  This test checks CPLD download Stress Test
     [Tags]  CONSR-SEST-STRS-0007-0001  Titan_G2_WB     Semi-Automated
     [Timeout]  30 min 00 seconds
     [Setup]   get dut variable
     FOR    ${INDEX}    IN RANGE    ${MAXINDEX}
        Print Loop Info  ${INDEX}
        Sub-Case   CONSR-SEST-STRS-0007-0001_1   upgrade cpld via SES Page - mode 0xe and 0xf Titan G2 WB
        Sub-Case   CONSR-SEST-STRS-0007-0001_2   upgrade cpld via SES Page - mode 0xe and reset 00h Titan G2 WB
     END
     [Teardown]  Run Keywords  Server Disconnect
           ...  AND OSDisconnect

CONSRS-DP-02-0001
    [Documentation]  This test checks Drive Disk Power On-Off - CLI
    [Tags]    CONSRS-DP-02-0001   Titan_G2_WB     Semi-Automated
    [Timeout]  8 min 00 seconds
    Step  1    verifyDriveDiskPowerOnOfftitang2wb  ${expdr_sec_1}  ${slot_num_sec1}  ${expdr_pri}   ${slot_num_pri_sec1}
    Step  2    verifyDriveDiskPowerOnOfftitang2wb  ${expdr_sec_2}  ${slot_num_sec2}  ${expdr_pri}   ${slot_num_pri_sec2}

CONSR-SEST-STRS-0002-0001
    [Documentation]   Drive Disk LED stress Test
    [Tags]     CONSR-SEST-STRS-0002-0001  Titan_G2_WB     Semi-Automated

    [Setup]  server Connect
    FOR    ${INDEX}    IN RANGE    ${MAXINDEX}
        Print Loop Info  ${INDEX}
        Step  1  verify drive disk LED on off status  ${set_on_ident_LED}   ${set_off_ident_LED}  ${get_page2_cmd}  ${get_ident_LED}  ${ident_disk_fault_LED_on_pattern}  ${ident_disk_fault_LED_off_pattern}
        Step  2  verify drive disk LED on off status  ${set_on_disk_fault_LED}  ${set_off_disk_fault_LED}  ${get_page2_cmd}  ${get_disk_fault_LED}  ${ident_disk_fault_LED_on_pattern}  ${ident_disk_fault_LED_off_pattern}
    END
    [Teardown]  Run Keywords  Server Disconnect
           ...  AND OSDisconnect

CONSRS-SM-03-0001
    [Documentation]  This test checks  SMP PHY Control - link speed program
    [Tags]  CONSRS-SM-03-0001  Titan_G2_WB     Semi-Automated
    [Timeout]  3 min 00 seconds
    [Setup]    server Connect
    Step  1    verify smp phy link speed Titan G2 WB
    [Teardown]  Server Disconnect

CONSR-SEST-PWMT-0006-0001
    [Documentation]  This test checks Voltage Monitoring
    [Tags]   CONSR-SEST-PWMT-0006-0001   Titan_G2_WB     Semi-Automated
    [Timeout]  8 min 00 seconds
    [Setup]    server Connect
    Step  1    set voltage and verify UW
    Step  2    set voltage and verify UC
    Step  3    set voltage and verify OW
    Step  4    set voltage and verify OC
    [Teardown]  Server Disconnect

CONSR-SEST-SPCK-0032-0001
    [Documentation]  This test checks String Out Diagnostic Pages(04h) - Command Code and Data for IP Configuration(A1)
    [Tags]    CONSR-SEST-SPCK-0032-0001     Titan_G2_WB     Semi-Automated
    [Timeout]  3 min 00 seconds
    [Setup]    server Connect
    Step  1    verify command code and data for IP Configuration
    [Teardown]  Server Disconnect

CONSR-SEST-DRMT-0006-0001
    [Documentation]  This test checks phy enable_disable on expanders
    [Tags]    CONSR-SEST-DRMT-0006-0001    Titan_G2_WB     Semi-Automated
    [Timeout]  8 min 00 seconds
    [Setup]    server Connect
    Step  1    verify phy enable_disable on secondary expander1
    Step  2    verify phy enable_disable on secondary expander2
    Step  3    verify phy enable_disable on primary expander
    [Teardown]  Server Disconnect

CONSRS-PO-01-0001
    [Documentation]  This test checks Drive Disk Power On/Off Check with SES Page.
    [Tags]     CONSRS-PO-01-0001   Titan_G2_WB     Semi-Automated
    [Timeout]  8 min 00 seconds
    [Setup]    server Connect
    Step  1    verify Drive Disk Power
    [Teardown]  Server Disconnect

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
