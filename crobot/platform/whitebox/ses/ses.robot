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
# Script       : ses.robot                                                                                            #
# Date         : April 11, 2021                                                                                       #
# Author       : James Shi <jameshi@celestica.com>                                                                    #
# Description  : This script will validate ses                                                                        #
#                                                                                                                     #
# Script Revision Details:                                                                                            #
#   Initial Draft for ses testing                                                                                     #
#######################################################################################################################

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
Debug-Test
    [Documentation]  Debug-Test
    [Tags]     Debug-Test
#    [Timeout]  60 min 00 seconds
    [Setup]    get dut variable
    FOR    ${INDEX}    IN RANGE    100
        Print Loop Info  ${INDEX}
#    Sub-Case  Debug-Test_1  update cpld stress
   Sub-Case  Debug-Test_4  power on/off JBOD via ses command to check info
   Sub-Case  Debug-Test_5  dc cycle server to check info
   Sub-Case  Debug-Test_6  dc cycle server + power on/off JBOD via ses command to check info
    END
#   [Teardown]  Run Keyword If Test Failed  reload expander to check info

create gold file
    [Documentation]  Debug-Test
    [Tags]     create-gold-file
    [Timeout]  10 min 00 seconds
    [Setup]    get dut variable
    Sub-Case  create-gold-file_1  Create ses page gold file
    Sub-Case  create-gold-file_1  Compare ses page gold file

CONSR-SEST-SPCK-0001-0001
    [Documentation]  This test checks  SES Page - Supported Diagnostic Pages Diagnostic Page (00h)
    [Tags]     CONSR-SEST-SPCK-0001-0001  Titan-K  regression
    [Timeout]  5 min 00 seconds
    [Setup]    get dut variable
    Sub-Case  CONSR-SEST-SPCK-0001-0001_1  check esm mode status
    Sub-Case  CONSR-SEST-SPCK-0001-0001_2  check all supported diagnostic pages
    [Teardown]  Run Keyword If Test Failed  Disconnect

CONSR-SEST-SPCK-0002-0001
    [Documentation]  This test checks  SES Page - Configuration Diagnostic Pages(01h)
    [Tags]     CONSR-SEST-SPCK-0002-0001  Titan-K  regression
    [Timeout]  5 min 00 seconds
    [Setup]    get dut variable
    Sub-Case  CONSR-SEST-SPCK-0002-0001_1  check esm mode status
    Sub-Case  CONSR-SEST-SPCK-0002-0001_2  Configuration Diagnostic Pages(01h)
    [Teardown]  Run Keyword If Test Failed  Disconnect

CONSR-SEST-SPCK-0003-0001
    [Documentation]  This test checks  Enclosure Status Diagnostic Pages(02h)
    [Tags]     CONSR-SEST-SPCK-0003-0001  Titan-K  regression
    [Timeout]  5 min 00 seconds
    [Setup]    get dut variable
    Sub-Case  CONSR-SEST-SPCK-0003-0001_1  check esm mode status
    Sub-Case  CONSR-SEST-SPCK-0003-0001_2  Enclosure Status Diagnostic Pages(02h)

CONSR-SEST-SPCK-0004-0001
    [Documentation]  This test checks  Enclosure Control Diagnostic Pages(02h) - set control bits via raw data
    [Tags]     CONSR-SEST-SPCK-0004-0001  Titan-K  regression
    [Timeout]  5 min 00 seconds
    [Setup]    get dut variable
    Sub-Case  CONSR-SEST-SPCK-0004-0001_1  check esm mode status
    Sub-Case  CONSR-SEST-SPCK-0004-0001_2  set control bits via raw data
    [Teardown]  Run Keyword If Test Failed  Disconnect

CONSR-SEST-SPCK-0005-0001
    [Documentation]  This test checks  Enclosure Control Diagnostic Pages(02h) - check 'Info' bit
    [Tags]     CONSR-SEST-SPCK-0005-0001  Titan-K  regression
    [Timeout]  5 min 00 seconds
    [Setup]    get dut variable
    Sub-Case  CONSR-SEST-SPCK-0005-0001_1  check esm mode status
    Sub-Case  CONSR-SEST-SPCK-0005-0001_2  check 'Info' bit
    [Teardown]  Run Keyword If Test Failed  Disconnect

CONSR-SEST-SPCK-0006-0001
    [Documentation]  Check 'crit' bit with sensors under UC condition - Enclosure Control Diagnostic Pages(02h)
    [Tags]     CONSR-SEST-SPCK-0006-0001  Titan-K  regression
    [Timeout]  5 min 00 seconds
    [Setup]  check ESM And Connect Server
    Step  1  Run Keyword And Continue On Failure  check Temperature Alarm  high critical
    Step  2  restore Temperature Threshold  high critical
    [Teardown]  Server Disconnect

CONSR-SEST-SPCK-0007-0001
    [Documentation]  Check 'crit' bit with sensors under LC condition - Enclosure Control Diagnostic Pages(02h)
    [Tags]     CONSR-SEST-SPCK-0007-0001  Titan-K  regression
    [Timeout]  5 min 00 seconds
    [Setup]  check ESM And Connect Server
    Step  1  Run Keyword And Continue On Failure  check Temperature Alarm  low critical
    Step  2  restore Temperature Threshold  low critical
    [Teardown]  Server Disconnect

CONSR-SEST-SPCK-0008-0001
    [Documentation]  Check 'non-crit' bit with sensors under UW condition - Enclosure Control Diagnostic Pages(02h)
    [Tags]     CONSR-SEST-SPCK-0008-0001  Titan-K  regression
    [Timeout]  5 min 00 seconds
    [Setup]  check ESM And Connect Server
    Step  1  Run Keyword And Continue On Failure  check Temperature Alarm  high warning
    Step  2  restore Temperature Threshold  high warning
    [Teardown]  Server Disconnect

CONSR-SEST-SPCK-0009-0001
    [Documentation]  Check 'non-crit' bit with sensors under LW condition - Enclosure Control Diagnostic Pages(02h)
    [Tags]     CONSR-SEST-SPCK-0009-0001  Titan-K  regression
    [Timeout]  5 min 00 seconds
    [Setup]  check ESM And Connect Server
    Step  1  Run Keyword And Continue On Failure  check Temperature Alarm  low warning
    Step  2  restore Temperature Threshold  low warning
    [Teardown]  Server Disconnect


CONSR-SEST-SPCK-0018-0001
    [Documentation]  This test checks  Enclosure Control Diagnostic Pages(02h) - Cooling external Mode
    [Tags]     CONSR-SEST-SPCK-0018-0001  Titan-K  regression
    [Timeout]  5 min 00 seconds
    [Setup]    get dut variable
    Sub-Case  CONSR-SEST-SPCK-0018-0001_1  check esm mode status
    Sub-Case  CONSR-SEST-SPCK-0018-0001_2  check Cooling external Mode
    [Teardown]  Run Keyword If Test Failed  Disconnect

CONSR-SEST-SPCK-0019-0001
    [Documentation]  This test checks  Enclosure Control Diagnostic Pages(02h) - Cooling external Mode
    [Tags]     CONSR-SEST-SPCK-0019-0001  Titan-K  regression
    [Timeout]  5 min 00 seconds
    [Setup]    get dut variable
    Sub-Case  CONSR-SEST-SPCK-0019-0001_1  check esm mode status
    Sub-Case  CONSR-SEST-SPCK-0019-0001_2  check Cooling internal Mode
    [Teardown]  Run Keywords  Server Disconnect
           ...  AND Disconnect

CONSR-SEST-SPCK-0020-0001
    [Documentation]  This test checks  Enclosure Control Diagnostic Pages(02h) - Fan current speed
    [Tags]     CONSR-SEST-SPCK-0020-0001  Titan-K  regression
    [Timeout]  10 min 00 seconds
    [Setup]    get dut variable
    Sub-Case  CONSR-SEST-SPCK-0020-0001_1  check esm mode status
    Sub-Case  CONSR-SEST-SPCK-0020-0001_2  check Cooling external Mode
    Sub-Case  CONSR-SEST-SPCK-0020-0001_3  check Fan current speed
    [Teardown]  Run Keywords  Server Disconnect
           ...  AND Disconnect

CONSR-SEST-SPCK-0021-0001
    [Documentation]  This test checks  Enclosure Control Diagnostic Pages(02h) - Fan max speed
    [Tags]     CONSR-SEST-SPCK-0021-0001  Titan-K  regression
    [Timeout]  10 min 00 seconds
    [Setup]    get dut variable
    Sub-Case  CONSR-SEST-SPCK-0021-0001_1  check esm mode status
    Sub-Case  CONSR-SEST-SPCK-0021-0001_2  check Cooling external Mode
    Sub-Case  CONSR-SEST-SPCK-0021-0001_3  check Fan max speed
    [Teardown]  Run Keywords  Server Disconnect
           ...  AND Disconnect

CONSR-SEST-SPCK-0022-0001
    [Documentation]  This test checks  Enclosure Control Diagnostic Pages(02h) - Fan min speed
    [Tags]     CONSR-SEST-SPCK-0022-0001  Titan-K
    [Timeout]  10 min 00 seconds
    [Setup]    get dut variable
    Sub-Case  CONSR-SEST-SPCK-0022-0001_1  check esm mode status
    Sub-Case  CONSR-SEST-SPCK-0022-0001_2  check Cooling external Mode
    Sub-Case  CONSR-SEST-SPCK-0022-0001_3  check Fan min speed
    [Teardown]  Run Keywords  Server Disconnect
           ...  AND Disconnect

CONSR-SEST-SPCK-0023-0001
    [Documentation]  This test checks  Enclosure Control Diagnostic Pages(02h) between ESM A and EAM B
    [Tags]     CONSR-SEST-SPCK-0023-0001  Titan-K
    [Timeout]  10 min 00 seconds
    [Setup]    get dut variable
    Sub-Case  CONSR-SEST-SPCK-0023-0001_1  check esm mode status
    Sub-Case  CONSR-SEST-SPCK-0023-0001_2  check Cooling external Mode
    Sub-Case  CONSR-SEST-SPCK-0023-0001_3  check Fan min speed
    [Teardown]  Run Keywords  Server Disconnect
           ...  AND Disconnect

CONSR-SEST-SPCK-0026-0001
    [Documentation]  Check array device OK bit - Enclosure Control Diagnostic Pages(02h)
    [Tags]     CONSR-SEST-SPCK-0026-0001  Titan-K  regression
    [Timeout]  5 min 00 seconds
    [Setup]  check ESM And Connect Server
    Step  1  check Array OK Bit
    [Teardown]  Run Keywords  Server Disconnect
           ...  AND Disconnect

CONSR-SEST-SPCK-0027-0001
    [Documentation]  Check array device power off - Enclosure Control Diagnostic Pages(02h)
    [Tags]     CONSR-SEST-SPCK-0027-0001  Titan-K  regression
    [Timeout]  5 min 00 seconds
    [Setup]  check ESM And Connect Server
    Step  1  check Disk Power Off
    [Teardown]  Run Keywords  Server Disconnect
           ...  AND Disconnect

CONSR-SEST-SPCK-0036-0001
    [Documentation]  This test checks String In Diagnostic Pages(04h)
    [Tags]     CONSR-SEST-SPCK-0036-0001  Titan-K  regression
    [Timeout]  10 min 00 seconds
    [Setup]    get dut variable
    Sub-Case  CONSR-SEST-SPCK-0036-0001_1  check esm mode status
    Sub-Case  CONSR-SEST-SPCK-0036-0001_2  check String In Diagnostic Pages(04h)
    [Teardown]  Run Keywords  Server Disconnect
           ...  AND Disconnect

CONSR-SEST-SPCK-0037-0001
    [Documentation]  This test checks String In Diagnostic Pages(05h)
    [Tags]     CONSR-SEST-SPCK-0037-0001  Titan-K  regression
    [Timeout]  10 min 00 seconds
    [Setup]    get dut variable
    Sub-Case  CONSR-SEST-SPCK-0037-0001_1  check esm mode status
    Sub-Case  CONSR-SEST-SPCK-0037-0001_2  check String In Diagnostic Pages(05h)
    [Teardown]  Run Keywords  Server Disconnect
           ...  AND Disconnect

CONSR-SEST-SPCK-0046-0001
    [Documentation]  Element Descriptor Diagnostic Page(07h)
    [Tags]     CONSR-SEST-SPCK-0046-0001  Titan-K  regression
    [Timeout]  5 min 00 seconds
    Step  1  get FRU Info
    Step  2  check Descriptor Length
    [Teardown]  Run Keywords  Server Disconnect
           ...  AND Disconnect

CONSR-SEST-SPCK-0050-0001
    [Documentation]  Additional Element Status Diagnostic Page(0ah)
    [Tags]     CONSR-SEST-SPCK-0050-0001  Titan-K  regression
    [Timeout]  5 min 00 seconds
    [Setup]  check ESM And Connect Server
    Step  1  check Disks Info On Page 0x0a
    [Teardown]  Run Keywords  Server Disconnect
           ...  AND Disconnect

CONSR-SEST-FWDL-0001-0001
    [Documentation]  Upgrade FW with mode 0x7
    [Tags]     CONSR-SEST-FWDL-0001-0001  Titan-K  regression
    [Timeout]  20 min 00 seconds
    [Setup]    get dut variable
    Step  1  check esm mode status
    Step  2  Download SES FW File And Update  True
    Step  3  check ESM SES FW Version  True
    Step  4  check SES FW Version On Server  True
    [Teardown]  Run Keywords  Server Disconnect
           ...  AND Disconnect

CONSR-SEST-FWDL-0002-0001
    [Documentation]  Downgrade FW with mode 0x7
    [Tags]     CONSR-SEST-FWDL-0002-0001  Titan-K  regression
    [Timeout]  30 min 00 seconds
    [Setup]    get dut variable
    Step  1  check esm mode status
    Step  2  Download SES FW File And Update  False
    Step  3  check ESM SES FW Version  False
    Step  4  check SES FW Version On Server  False
    Step  5  Download SES FW File And Update  True
    Step  6  check ESM SES FW Version  True
    Step  7  check SES FW Version On Server  True
    [Teardown]  Run Keywords  Server Disconnect
           ...  AND Disconnect

CONSR-SEST-FWDL-0005-0001
    [Documentation]  This test checks upgrade FW with mode 0xe + mode 0xf
    [Tags]     CONSR-SEST-FWDL-0005-0001  Titan-K  test  regression
    [Timeout]  30 min 00 seconds
    [Setup]    get dut variable
    Sub-Case  CONSR-SEST-FWDL-0005-0001_1  check esm mode status
    Sub-Case  CONSR-SEST-FWDL-0005-0001_2  Download SES FW File
    Sub-Case  CONSR-SEST-FWDL-0005-0001_3  upgrade FW with mode 0xe + mode 0xf
    [Teardown]  Run Keywords  Server Disconnect
           ...  AND Disconnect

CONSR-SEST-FWDL-0006-0001
    [Documentation]  This test checks upgrade FW with mode 0xe + reset 00h code
    [Tags]     CONSR-SEST-FWDL-0006-0001  Titan-K  regression
    [Timeout]  30 min 00 seconds
    [Setup]    get dut variable
    Sub-Case  CONSR-SEST-FWDL-0006-0001_1  check esm mode status
    Sub-Case  CONSR-SEST-FWDL-0006-0001_2  Download SES FW File
    Sub-Case  CONSR-SEST-FWDL-0006-0001_3  upgrade FW with mode 0xe + reset 00h code
    [Teardown]  Run Keywords  Server Disconnect
           ...  AND Disconnect

CONSR-SEST-FWDL-0007-0001
    [Documentation]  This test checks upgrade FW with mode 0xe + reset 01h code
    [Tags]     CONSR-SEST-FWDL-0007-0001  Titan-K  regression
    [Timeout]  30 min 00 seconds
    [Setup]    get dut variable
    Sub-Case  CONSR-SEST-FWDL-0007-0001_1  check esm mode status
    Sub-Case  CONSR-SEST-FWDL-0007-0001_2  Download SES FW File
    Sub-Case  CONSR-SEST-FWDL-0007-0001_3  upgrade FW with mode 0xe + reset 01h code
    [Teardown]  Run Keywords  Server Disconnect
           ...  AND Disconnect

CONSR-SEST-FWDL-0008-0001
    [Documentation]  This test checks upgrade FW with mode 0xe + reset 03h code
    [Tags]     CONSR-SEST-FWDL-0008-0001  Titan-K  regression
    [Timeout]  30 min 00 seconds
    [Setup]    get dut variable
    Sub-Case  CONSR-SEST-FWDL-0008-0001_1  check esm mode status
    Sub-Case  CONSR-SEST-FWDL-0008-0001_2  Download SES FW File
    Sub-Case  CONSR-SEST-FWDL-0008-0001_3  upgrade FW with mode 0xe + reset 03h code
    [Teardown]  Run Keywords  Server Disconnect
           ...  AND Disconnect

CONSR-SEST-FWDL-0009-0001
    [Documentation]  This test checks upgrade FW with mode 0xe + power cycle
    [Tags]     CONSR-SEST-FWDL-0009-0001  Titan-K  regression
    [Timeout]  30 min 00 seconds
    [Setup]    get dut variable
    Sub-Case  CONSR-SEST-FWDL-0009-0001_1  check esm mode status
    Sub-Case  CONSR-SEST-FWDL-0009-0001_2  Download SES FW File
    Sub-Case  CONSR-SEST-FWDL-0009-0001_2  upgrade FW with mode 0xe + power cycle
    [Teardown]  Run Keywords  Server Disconnect
           ...  AND Disconnect

CONSR-SEST-FWDL-0010-0001
    [Documentation]  This test checks downgrade FW with mode 0xe + mode 0xf
    [Tags]     CONSR-SEST-FWDL-0010-0001  Titan-K  regression
    [Timeout]  30 min 00 seconds
    [Setup]    get dut variable
    Sub-Case  CONSR-SEST-FWDL-0010-0001_1  check esm mode status
    Sub-Case  CONSR-SEST-FWDL-0010-0001_2  Download SES FW File
    Sub-Case  CONSR-SEST-FWDL-0010-0001_3  downgrade FW with mode 0xe + mode 0xf
    Sub-Case  CONSR-SEST-FWDL-0010-0001_4  upgrade FW with mode 0xe + mode 0xf
    [Teardown]  Run Keywords  Server Disconnect
           ...  AND Disconnect

CONSR-SEST-FWDL-0011-0001
    [Documentation]  This test checks downgrade FW with mode 0xe + reset 00h code
    [Tags]     CONSR-SEST-FWDL-0011-0001  Titan-K  regression
    [Timeout]  30 min 00 seconds
    [Setup]    get dut variable
    Sub-Case  CONSR-SEST-FWDL-0011-0001_1  check esm mode status
    Sub-Case  CONSR-SEST-FWDL-0011-0001_2  Download SES FW File
    Sub-Case  CONSR-SEST-FWDL-0011-0001_3  downgrade FW with mode 0xe + reset 00h code
    Sub-Case  CONSR-SEST-FWDL-0011-0001_4  upgrade FW with mode 0xe + reset 00h code
    [Teardown]  Run Keywords  Server Disconnect
           ...  AND Disconnect

CONSR-SEST-FWDL-0012-0001
    [Documentation]  This test checks downgrade FW with mode 0xe + reset 01h code
    [Tags]     CONSR-SEST-FWDL-0012-0001  Titan-K  regression
    [Timeout]  30 min 00 seconds
    [Setup]    get dut variable
    Sub-Case  CONSR-SEST-FWDL-0012-0001_1  check esm mode status
    Sub-Case  CONSR-SEST-FWDL-0012-0001_2  Download SES FW File
    Sub-Case  CONSR-SEST-FWDL-0012-0001_3  downgrade FW with mode 0xe + reset 01h code
    Sub-Case  CONSR-SEST-FWDL-0012-0001_4  upgrade FW with mode 0xe + reset 01h code
    [Teardown]  Run Keywords  Server Disconnect
           ...  AND Disconnect

CONSR-SEST-FWDL-0013-0001
    [Documentation]  This test checks downgrade FW with mode 0xe + reset 03h code
    [Tags]     CONSR-SEST-FWDL-0013-0001  Titan-K  regression
    [Timeout]  30 min 00 seconds
    [Setup]    get dut variable
    Sub-Case  CONSR-SEST-FWDL-0013-0001_1  check esm mode status
    Sub-Case  CONSR-SEST-FWDL-0013-0001_2  Download SES FW File
    Sub-Case  CONSR-SEST-FWDL-0013-0001_3  downgrade FW with mode 0xe + reset 03h code
    Sub-Case  CONSR-SEST-FWDL-0013-0001_4  upgrade FW with mode 0xe + reset 03h code
    [Teardown]  Run Keywords  Server Disconnect
           ...  AND Disconnect

CONSR-SEST-FWDL-0014-0001
    [Documentation]  This test checks downgrade FW with mode 0xe + power cycle
    [Tags]     CONSR-SEST-FWDL-0014-0001  Titan-K  regression
    [Timeout]  30 min 00 seconds
    [Setup]    get dut variable
    Sub-Case  CONSR-SEST-FWDL-0014-0001_1  check esm mode status
    Sub-Case  CONSR-SEST-FWDL-0014-0001_2  Download SES FW File
    Sub-Case  CONSR-SEST-FWDL-0014-0001_3  downgrade FW with mode 0xe + power cycle
    Sub-Case  CONSR-SEST-FWDL-0014-0001_4  upgrade FW with mode 0xe + power cycle
    [Teardown]  Run Keywords  Server Disconnect
           ...  AND Disconnect

CONSR-SEST-FWDL-0028-0001
    [Documentation]  SES Download microcode Control Diagnostic Page
                ...  - with wrong image file under mode 7
    [Tags]     CONSR-SEST-FWDL-0028-0001  Titan-K
    [Timeout]  10 min 00 seconds
    [Setup]  server Connect
    Step  1  download And Verify With FW Fault Image
    [Teardown]  Run Keywords  Server Disconnect
           ...  AND disconnect TelnetObj

CONSR-SEST-FWDL-0029-0001
    [Documentation]  SES Download microcode Control Diagnostic Page
                ...  - with wrong image file under mode 0xe
    [Tags]     CONSR-SEST-FWDL-0029-0001  Titan-K
    [Timeout]  10 min 00 seconds
    [Setup]  server Connect
    Step  1  Verify With FW Fault Image Under Mode E
    [Teardown]  Run Keywords  Server Disconnect
           ...  AND disconnect TelnetObj

CONSR-SEST-FWDL-0030-0001
    [Documentation]  SES Download microcode Control Diagnostic Page
                ...  - remove Power during downloading image
    [Tags]     CONSR-SEST-FWDL-0030-0001  Titan-K
    [Timeout]  10 min 00 seconds
    [Setup]  server Connect
    Step  1  Download SES FW File And Power Cycle  ${download_microcode_mode7_cmd}
    [Teardown]  Run Keywords  Server Disconnect
           ...  AND disconnect TelnetObj

CONSR-SEST-FWDL-0031-0001
    [Documentation]  SES Download microcode Control Diagnostic Page
                ...  - remove Power during downloading image
    [Tags]     CONSR-SEST-FWDL-0031-0001  Titan-K
    [Timeout]  10 min 00 seconds
    [Setup]  server Connect
    Step  1  Download SES FW File And Power Cycle  ${download_microcode_modeE_cmd}
    [Teardown]  Run Keywords  Server Disconnect
           ...  AND disconnect TelnetObj

CONSR-SEST-FWDL-0032-0001
    [Documentation]  SES Download microcode Control Diagnostic Page
                ...  - Input new command to interrupt downloading image
                ...    under mode 0xe
    [Tags]     CONSR-SEST-FWDL-0032-0001  Titan-K
    [Timeout]  10 min 00 seconds
    [Setup]  server Connect
    Step  1     Download SES FW File And Interrupt with command
           ...  ${download_microcode_modeE_cmd}
    [Teardown]  Run Keywords  Server Disconnect
           ...  AND disconnect TelnetObj

CONSR-SEST-FWDL-0033-0001
    [Documentation]  SES Download microcode Control Diagnostic Page
                ...  - Input new command to interrupt downloading image
                ...    under mode 7
    [Tags]     CONSR-SEST-FWDL-0033-0001  Titan-K
    [Timeout]  10 min 00 seconds
    [Setup]  server Connect
    Step  1     Download SES FW File And Interrupt with command
           ...  ${download_microcode_mode7_cmd}
    [Teardown]  Run Keywords  Server Disconnect
           ...  AND disconnect TelnetObj

CONSR-SEST-FWDL-0034-0001
    [Documentation]  This test checks upgrade cpld via SES Page - mode 0xe and 0xf
    [Tags]     CONSR-SEST-FWDL-0034-0001  Titan-K  regression
    [Timeout]  30 min 00 seconds
    [Setup]    get dut variable
    Sub-Case  CONSR-SEST-FWDL-0034-0001_1  check esm mode status
    Sub-Case  CONSR-SEST-FWDL-0034-0001_2  Download CPLD FW File
    Sub-Case  CONSR-SEST-FWDL-0034-0001_3  upgrade cpld with mode 0xe + mode 0xf
    Sub-Case  CONSR-SEST-FWDL-0034-0001_4  check esm mode status
    [Teardown]  Run Keywords  Server Disconnect
           ...  AND Disconnect

CONSR-SEST-FWDL-0035-0001
    [Documentation]  This test checks upgrade cpld via SES Page - mode 0xe and reset 00h
    [Tags]     CONSR-SEST-FWDL-0035-0001  Titan-K  regression
    [Timeout]  30 min 00 seconds
    [Setup]    get dut variable
    Sub-Case  CONSR-SEST-FWDL-0035-0001_1  check esm mode status
    Sub-Case  CONSR-SEST-FWDL-0035-0001_2  Download CPLD FW File
    Sub-Case  CONSR-SEST-FWDL-0035-0001_3  upgrade cpld with mode 0xe + reset 00h
    Sub-Case  CONSR-SEST-FWDL-0035-0001_4  check esm mode status
    [Teardown]  Run Keywords  Server Disconnect
           ...  AND Disconnect

CONSR-SEST-FWDL-0036-0001
    [Documentation]  This test checks upgrade cpld via SES Page - mode 0xe and power cycle
    [Tags]     CONSR-SEST-FWDL-0036-0001  Titan-K  regression
    [Timeout]  30 min 00 seconds
    [Setup]    get dut variable
    Sub-Case  CONSR-SEST-FWDL-0036-0001_1  check esm mode status
    Sub-Case  CONSR-SEST-FWDL-0036-0001_2  Download CPLD FW File
    Sub-Case  CONSR-SEST-FWDL-0036-0001_3  upgrade cpld with mode 0xe + power cycle
    Sub-Case  CONSR-SEST-FWDL-0036-0001_4  check esm mode status
    [Teardown]  Run Keywords  Server Disconnect
           ...  AND Disconnect

CONSR-SEST-FWDL-0037-0001
    [Documentation]  This test checks downgrade cpld via SES Page - mode 0xe and 0xf
    [Tags]     CONSR-SEST-FWDL-0037-0001  Titan-K  regression
    [Timeout]  30 min 00 seconds
    [Setup]    get dut variable
    Sub-Case  CONSR-SEST-FWDL-0037-0001_1  Download CPLD FW File
    Sub-Case  CONSR-SEST-FWDL-0037-0001_2  downgrade cpld with mode 0xe + mode 0xf
    Sub-Case  CONSR-SEST-FWDL-0037-0001_3  check esm mode status
    Sub-Case  CONSR-SEST-FWDL-0037-0001_4  upgrade cpld with mode 0xe + mode 0xf
    Sub-Case  CONSR-SEST-FWDL-0037-0001_5  check esm mode status
    [Teardown]  Run Keywords  Server Disconnect
           ...  AND Disconnect

CONSR-SEST-FWDL-0038-0001
    [Documentation]  This test checks downgrade cpld via SES Page - mode 0xe  + reset 00h
    [Tags]     CONSR-SEST-FWDL-0038-0001  Titan-K  regression
    [Timeout]  30 min 00 seconds
    [Setup]    get dut variable
    Sub-Case  CONSR-SEST-FWDL-0038-0001_1  Download CPLD FW File
    Sub-Case  CONSR-SEST-FWDL-0038-0001_2  downgrade cpld with mode 0xe + reset 00h
    Sub-Case  CONSR-SEST-FWDL-0038-0001_3  check esm mode status
    Sub-Case  CONSR-SEST-FWDL-0038-0001_4  upgrade cpld with mode 0xe + reset 00h
    Sub-Case  CONSR-SEST-FWDL-0038-0001_5  check esm mode status
    [Teardown]  Run Keywords  Server Disconnect
           ...  AND Disconnect

CONSR-SEST-FWDL-0039-0001
    [Documentation]  This test checks downgrade cpld via SES Page - mode 0xe  + power cycle
    [Tags]     CONSR-SEST-FWDL-0039-0001  Titan-K  regression
    [Timeout]  30 min 00 seconds
    [Setup]    get dut variable
    Sub-Case  CONSR-SEST-FWDL-0039-0001_1  Download CPLD FW File
    Sub-Case  CONSR-SEST-FWDL-0039-0001_2  downgrade cpld with mode 0xe + power cycle
    Sub-Case  CONSR-SEST-FWDL-0039-0001_3  check esm mode status
    Sub-Case  CONSR-SEST-FWDL-0039-0001_4  upgrade cpld with mode 0xe + power cycle
    Sub-Case  CONSR-SEST-FWDL-0039-0001_5  check esm mode status
    [Teardown]  Run Keywords  Server Disconnect
           ...  AND Disconnect

CONSR-SEST-SPCK-0038-0001
    [Documentation]  Threshold Out Diagnostic Pages(05h) - Temp LC
    [Tags]     CONSR-SEST-SPCK-0038-0001  Titan-K
    [Timeout]  5 min 00 seconds
    [Setup]  server Connect
    Step  1  check Temperature Alarm On Page5  low critical
    Step  2  restore Temperature Threshold on Page5  low critical
    [Teardown]  Run Keywords  Server Disconnect
           ...  AND Disconnect

CONSR-SEST-SPCK-0039-0001
    [Documentation]  Threshold Out Diagnostic Pages(05h) - Temp LW
    [Tags]     CONSR-SEST-SPCK-0039-0001  Titan-K
    [Timeout]  5 min 00 seconds
    [Setup]  server Connect
    Step  1  check Temperature Alarm On Page5  low warning
    Step  2  restore Temperature Threshold on Page5  low warning
    [Teardown]  Run Keywords  Server Disconnect
           ...  AND Disconnect

CONSR-SEST-SPCK-0040-0001
    [Documentation]  Threshold Out Diagnostic Pages(05h) - Temp UC
    [Tags]     CONSR-SEST-SPCK-0040-0001  Titan-K
    [Timeout]  5 min 00 seconds
    [Setup]  server Connect
    Step  1  check Temperature Alarm On Page5  high critical
    Step  2  restore Temperature Threshold on Page5  high critical
    [Teardown]  Run Keywords  Server Disconnect
           ...  AND Disconnect

CONSR-SEST-SPCK-0041-0001
    [Documentation]  Threshold Out Diagnostic Pages(05h) - Temp UW
    [Tags]     CONSR-SEST-SPCK-0041-0001  Titan-K
    [Timeout]  5 min 00 seconds
    [Setup]  server Connect
    Step  1  check Temperature Alarm On Page5  high warning
    Step  2  restore Temperature Threshold on Page5  high warning
    [Teardown]  Run Keywords  Server Disconnect
           ...  AND Disconnect

CONSR-SEST-SPCK-0042-0001
    [Documentation]  Threshold Out Diagnostic Pages(05h) - Voltage LC
    [Tags]     CONSR-SEST-SPCK-0042-0001  Titan-K
    [Timeout]  5 min 00 seconds
    [Setup]  server Connect
    Step  1  check Sensor Alarm On Page5  low critical  Voltage sensor
    Step  2  restore Threshold on Page5  low critical  Voltage sensor
    [Teardown]  Run Keywords  Server Disconnect
           ...  AND Disconnect

CONSR-SEST-SPCK-0043-0001
    [Documentation]  Threshold Out Diagnostic Pages(05h) - Voltage LW
    [Tags]     CONSR-SEST-SPCK-0043-0001  Titan-K
    [Timeout]  5 min 00 seconds
    [Setup]  server Connect
    Step  1  check Sensor Alarm On Page5  low warning  Voltage sensor
    Step  2  restore Threshold on Page5  low warning  Voltage sensor
    [Teardown]  Run Keywords  Server Disconnect
           ...  AND Disconnect

CONSR-SEST-SPCK-0044-0001
    [Documentation]  Threshold Out Diagnostic Pages(05h) - Voltage UC
    [Tags]     CONSR-SEST-SPCK-0044-0001  Titan-K
    [Timeout]  5 min 00 seconds
    [Setup]  server Connect
    Step  1  check Sensor Alarm On Page5  high critical  Voltage sensor
    Step  2  restore Threshold on Page5  high critical  Voltage sensor
    [Teardown]  Run Keywords  Server Disconnect
           ...  AND Disconnect

CONSR-SEST-SPCK-0045-0001
    [Documentation]  Threshold Out Diagnostic Pages(05h) - Voltage UW
    [Tags]     CONSR-SEST-SPCK-0045-0001  Titan-K
    [Timeout]  5 min 00 seconds
    [Setup]  server Connect
    Step  1  check Sensor Alarm On Page5  high warning  Voltage sensor
    Step  2  restore Threshold on Page5  high warning  Voltage sensor
    [Teardown]  Run Keywords  Server Disconnect
           ...  AND Disconnect

CONSR-SEST-SPCK-0054-0001
    [Documentation]  SES Download microcode Control Diagnostic Page (mode 7)
                ...  - Checking download status
    [Tags]     CONSR-SEST-SPCK-0054-0001  Titan-K
    [Timeout]  10 min 00 seconds
    [Setup]  server Connect
    Step  1     Download SES FW File And Check Downloading Status
           ...  ${download_microcode_mode7_cmd}
    [Teardown]  Run Keywords  Server Disconnect
           ...  AND Disconnect

CONSR-SEST-SPCK-0055-0001
    [Documentation]  SES Download microcode Control Diagnostic Page (mode E)
                ...  - Checking download status
    [Tags]     CONSR-SEST-SPCK-0055-0001  Titan-K
    [Timeout]  10 min 00 seconds
    [Setup]  server Connect
    Step  1     Download SES FW File And Check Downloading Status Without Activate
           ...  ${download_microcode_modeE_cmd}
    [Teardown]  Run Keywords  Server Disconnect
           ...  AND Disconnect

CONSR-SEST-SPCK-0056-0001
    [Documentation]  SES Download microcode Control Diagnostic Page (mode F)
                ...  - Checking download status
    [Tags]     CONSR-SEST-SPCK-0056-0001  Titan-K
    [Timeout]  10 min 00 seconds
    [Setup]  server Connect
    Step  1     activate New FW Partition
    [Teardown]  Run Keywords  Server Disconnect
           ...  AND Disconnect

CONSR-SEST-SPCK-0057-0001
    [Documentation]  SES Download microcode Status Diagnostic Page
    [Tags]     CONSR-SEST-SPCK-0057-0001  Titan-K
    [Timeout]  10 min 00 seconds
    [Setup]  server Connect
    Step  1     check FW Download Status
    [Teardown]  Run Keywords  Server Disconnect
           ...  AND Disconnect

CONSR-SEST-SCSI-0001-0001
    [Documentation]  Test Unit Ready
    [Tags]     CONSR-SEST-SCSI-0001-0001  Titan-K
    [Timeout]  5 min 00 seconds
    [Setup]     server Connect
    Step  1     check SCISI Elements  ${check_scsi_ready_cmd}  ${scsi_ready_pattern}
    [Teardown]  Server Disconnect

CONSR-SEST-SCSI-0002-0001
    [Documentation]  check Enclosure Length
    [Tags]     CONSR-SEST-SCSI-0002-0001  Titan-K
    [Timeout]  5 min 00 seconds
    [Setup]     server Connect
    Step  1     check Enclosure Length  ${sg_inquiry_cmd}  ${sq_inquiry_pattern}
    ...         ${sq_inquiry_length}
    [Teardown]  Server Disconnect

CONSR-SEST-SCSI-0003-0001
    [Documentation]  SES Support Diagnostic Page - VPD 00h(Supported VPD)
    [Tags]     CONSR-SEST-SCSI-0003-0001  Titan-K
    [Timeout]  5 min 00 seconds
    [Setup]     server Connect
    Step  1     check SCISI Elements  ${sg_inquiry_page_0x00_cmd}  ${sg_inquiry_page_0x00_pattern}
    [Teardown]  Server Disconnect

CONSR-SEST-SCSI-0004-0001
    [Documentation]  SES Support Diagnostic Page - VPD 80h(Unit Serial Number)
    [Tags]     CONSR-SEST-SCSI-0004-0001  Titan-K
    [Timeout]  5 min 00 seconds
    [Setup]     server Connect
    Step  1     check Enclosure Length  ${sg_inquiry_page_0x80_cmd}  ${sq_inquiry_pattern}
    ...         ${sq_inquiry_length}
    [Teardown]  Server Disconnect

CONSR-SEST-SCSI-0005-0001
    [Documentation]  SES Support Diagnostic Page - VPD 83h(Device Identication)
    [Tags]     CONSR-SEST-SCSI-0005-0001  Titan-K
    [Timeout]  5 min 00 seconds
    [Setup]     server Connect
    Step  1     check SCISI Elements  ${sg_inquiry_page_0x83_cmd}  ${sg_inquiry_page_0x83_pattern}
    [Teardown]  Server Disconnect

CONSR-SEST-SCSI-0006-0001
    [Documentation]  SES Support Diagnostic Page
    [Tags]     CONSR-SEST-SCSI-0006-0001  Titan-K
    [Timeout]  5 min 00 seconds
    [Setup]     server Connect
    Step  1     check Command Sent  sg_ses  ${fail_dict}
    [Teardown]  Server Disconnect

#Not support yet
#CONSR-SEST-SCSI-0008-0001
#    [Documentation]  SCSI Support Diagnostic Page - Write Buffer
#    ...              - Download Microcode with offsets, save and activate (mode 07)
#    [Tags]     CONSR-SEST-SCSI-0008-0001  Titan-K
#    [Timeout]  10 min 00 seconds
#    Step  1  Write Buffer To Download Microcode  True  ${sg_write_buffer_mode7_cmd}
#    Step  2  check ESM Version
#    [Teardown]  Run Keywords  Server Disconnect
#           ...  AND disconnect TelnetObj

CONSR-SEST-SCSI-0012-0001
    [Documentation]  SCSI Support Diagnostic Page - Log Select
    [Tags]     CONSR-SEST-SCSI-0012-0001  Titan-K
    [Timeout]  5 min 00 seconds
    [Setup]     server Connect
    Step  1     check SCISI Elements  ${set_log_sense_cmd}  ${set_log_sense_pattern}
    [Teardown]  Server Disconnect

CONSR-SEST-SCSI-0013-0001
    [Documentation]  SCSI Support Diagnostic Page - Log Sense
    [Tags]     CONSR-SEST-SCSI-0013-0001  Titan-K
    [Timeout]  5 min 00 seconds
    [Setup]     server Connect
    Step  1     check SCISI Elements  ${get_log_sense_cmd}  ${get_log_sense_pattern}
    [Teardown]  Server Disconnect

CONSR-SEST-SCSI-0014-0001
    [Documentation]  SCSI Support Diagnostic Page - Mode Select (Control Mode Page)
    [Tags]     CONSR-SEST-SCSI-0014-0001  Titan-K
    [Timeout]  5 min 00 seconds
    [Setup]     server Connect
    Step  1     check Command Sent  ${select_control_mode_cmd}  ${fail_dict}
    [Teardown]  Server Disconnect

CONSR-SEST-SCSI-0015-0001
    [Documentation]  SCSI Support Diagnostic Page - Mode Select (Protocol Specific Port Mode Page)
    [Tags]     CONSR-SEST-SCSI-0015-0001  Titan-K
    [Timeout]  5 min 00 seconds
    [Setup]     server Connect
    Step  1     check Command Sent  ${select_protocol_specific_mode_cmd}  ${fail_dict}
    [Teardown]  Run Keywords  Server Disconnect
           ...  AND Disconnect

CONSR-SEST-STRS-0001-0001
    [Documentation]  This test checks stress upgrade/downgrade FW with mode 0xe
    [Tags]     CONSR-SEST-STRS-0001-0001  Titan-K  regression
    [Timeout]  48 hours
    [Setup]    get dut variable
    FOR    ${INDEX}    IN RANGE    ${MAXINDEX}
        Print Loop Info  ${INDEX}
    Sub-Case  CONSR-SEST-STRS-0001-0001_1  check esm mode status
    Sub-Case  CONSR-SEST-STRS-0001-0001_2  downgrade FW with mode 0xe + reset 00h code
    Sub-Case  CONSR-SEST-STRS-0001-0001_3  upgrade FW with mode 0xe + reset 00h code
    Sub-Case  CONSR-SEST-STRS-0001-0001_4  downgrade FW with mode 0xe + mode 0xf
    Sub-Case  CONSR-SEST-STRS-0001-0001_5  upgrade FW with mode 0xe + mode 0xf
    Sub-Case  CONSR-SEST-STRS-0001-0001_6  downgrade FW with mode 0xe + reset 01h code
    Sub-Case  CONSR-SEST-STRS-0001-0001_7  upgrade FW with mode 0xe + reset 01h code
    Sub-Case  CONSR-SEST-STRS-0001-0001_8  downgrade FW with mode 0xe + reset 03h code
    Sub-Case  CONSR-SEST-STRS-0001-0001_9  upgrade FW with mode 0xe + reset 03h code
    Sub-Case  CONSR-SEST-STRS-0001-0001_10  downgrade FW with mode 0xe + power cycle 
    Sub-Case  CONSR-SEST-STRS-0001-0001_11  upgrade FW with mode 0xe + power cycle
    END
    [Teardown]  Run Keywords  Server Disconnect
           ...  AND Disconnect

CONSR-SEST-STRS-0005-0001
    [Documentation]  FW Reset stress Test
    [Tags]     CONSR-SEST-STRS-0005-0001  Titan-K  regression
    [Timeout]  24 hours
    [Setup]  server Connect
    FOR    ${INDEX}    IN RANGE    ${MAXINDEX}
        Print Loop Info  ${INDEX}
        Step  1  reset And Check All Expanders  ${reset_expander_00_cmd}
        Step  2  reset And Check All Expanders  ${reset_expander_01_cmd}
        Step  3  reset And Check All Expanders  ${reset_expander_03_cmd}
    END
    [Teardown]  Run Keywords  Server Disconnect
           ...  AND Disconnect

CONSR-SEST-STRS-0006-0001
    [Documentation]  This test checks Polling page stress Test
    [Tags]     CONSR-SEST-STRS-0006-0001  Titan-K  regression
    [Timeout]  24 hours
    [Setup]    get dut variable
    FOR    ${INDEX}    IN RANGE    ${MAXINDEX}
        Print Loop Info  ${INDEX}
    Sub-Case  CONSR-SEST-STRS-0006-0001_1  check all supported diagnostic pages
    Sub-Case  CONSR-SEST-STRS-0006-0001_2  Configuration Diagnostic Pages(01h)
    Sub-Case  CONSR-SEST-STRS-0006-0001_3  Enclosure Status Diagnostic Pages(02h)
    Sub-Case  CONSR-SEST-STRS-0006-0001_4  check String In Diagnostic Pages(04h)
    Sub-Case  CONSR-SEST-STRS-0006-0001_5  check String In Diagnostic Pages(05h)
    Sub-Case  CONSR-SEST-STRS-0006-0001_6  check ESM And Connect Server
    Sub-Case  CONSR-SEST-STRS-0006-0001_7  check Disks Info On Page 0x0a
    Sub-Case  CONSR-SEST-STRS-0006-0001_8  get FRU Info
    Sub-Case  CONSR-SEST-STRS-0006-0001_9  check Descriptor Length
    END
    [Teardown]  Run Keywords  Server Disconnect
           ...  AND Disconnect

CONSR-SEST-STRS-0020-0001
    [Documentation]  This test checks Single drive power on/off
    [Tags]     CONSR-SEST-STRS-0020-0001  Titan-K  regression
    [Timeout]  48 hours
    [Setup]    get dut variable
    FOR    ${INDEX}    IN RANGE    ${MAXINDEX}
        Print Loop Info  ${INDEX}
    Sub-Case  CONSR-SEST-STRS-0020-0001_1  power on/off drive one by one via ses command to check info
    END
    [Teardown]  Run Keywords  Server Disconnect
           ...  AND Disconnect

CONSR-SEST-STRS-0021-0001
    [Documentation]  This test checks Multiple drives power on/off
    [Tags]     CONSR-SEST-STRS-0021-0001  Titan-K  regression
    [Timeout]  48 hours
    [Setup]    get dut variable
    FOR    ${INDEX}    IN RANGE    ${MAXINDEX}
        Print Loop Info  ${INDEX}
    Sub-Case  CONSR-SEST-STRS-0021-0001_1  power on/off drive all via ses command to check info
    END
    [Teardown]  Run Keywords  Server Disconnect
           ...  AND Disconnect

CONSR-SEST-STRS-0022-0001
    [Documentation]  This test checks Entire JBOD power cycle (DC Cycle)
    [Tags]     CONSR-SEST-STRS-0022-0001  Titan-K  regression
    [Timeout]  48 hours
    [Setup]    get dut variable
    FOR    ${INDEX}    IN RANGE    ${MAXINDEX}
        Print Loop Info  ${INDEX}
    Sub-Case  CONSR-SEST-STRS-0022-0001_1  dc JBOD via ses command to check info
    END
    [Teardown]  Run Keywords  Server Disconnect
           ...  AND Disconnect

CONSR-SEST-STRS-0023-0001
    [Documentation]  This test checks Entire JBOD power cycle (AC Cycle)
    [Tags]     CONSR-SEST-STRS-0023-0001  Titan-K  regression
    [Timeout]  48 hours
    [Setup]    get dut variable
    FOR    ${INDEX}    IN RANGE    ${MAXINDEX}
        Print Loop Info  ${INDEX}
    Sub-Case  CONSR-SEST-STRS-0023-0001_1  ac cycle JBOD to check info
    END
    [Teardown]  Run Keywords  Server Disconnect
           ...  AND Disconnect

CONSR-SEST-STRS-0024-0001
    [Documentation]  This test checks Host server power cycle (AC cycle)
    [Tags]     CONSR-SEST-STRS-0024-0001  Titan-K  regression
    [Timeout]  48 hours
    [Setup]    get dut variable
    FOR    ${INDEX}    IN RANGE    ${MAXINDEX}
        Print Loop Info  ${INDEX}
    Sub-Case  CONSR-SEST-STRS-0024-0001_1  ac cycle server to check info
    END
    [Teardown]  Run Keywords  Server Disconnect
           ...  AND Disconnect

CONSR-SEST-STRS-0025-0001
    [Documentation]  This test checks Host server and JBOD power cycle(AC cycle)
    [Tags]     CONSR-SEST-STRS-0025-0001  Titan-K  regression
    [Timeout]  48 hours
    [Setup]    get dut variable
    FOR    ${INDEX}    IN RANGE    ${MAXINDEX}
        Print Loop Info  ${INDEX}
    Sub-Case  CONSR-SEST-STRS-0025-0001_1  ac cycle JBOD + server to check info
    END
    [Teardown]  Run Keywords  Server Disconnect
           ...  AND Disconnect

CONSR-SEST-STRS-0026-0001
    [Documentation]  This test checks JBOD ESM reset
    [Tags]     CONSR-SEST-STRS-0026-0001  Titan-K  regression
    [Timeout]  48 hours
    [Setup]    get dut variable
    FOR    ${INDEX}    IN RANGE    ${MAXINDEX}
        Print Loop Info  ${INDEX}
    Sub-Case  CONSR-SEST-STRS-0026-0001_1  reset esm to check info
    END
    [Teardown]  Run Keywords  Server Disconnect
           ...  AND Disconnect

CONSR-SEST-STRS-0027-0001
    [Documentation]  This test checks update cpld stress
    [Tags]     CONSR-SEST-STRS-0027-0001  Titan-K  regression
    [Timeout]  48 hours
    [Setup]    get dut variable
    FOR    ${INDEX}    IN RANGE    ${MAXINDEX}
        Print Loop Info  ${INDEX}
    Sub-Case  CONSR-SEST-STRS-0027-0001_1  Download CPLD FW File
    Sub-Case  CONSR-SEST-STRS-0027-0001_2  downgrade cpld with mode 0xe + mode 0xf
    Sub-Case  CONSR-SEST-STRS-0027-0001_3  check esm mode status
    Sub-Case  CONSR-SEST-STRS-0027-0001_4  upgrade cpld with mode 0xe + mode 0xf
    Sub-Case  CONSR-SEST-STRS-0027-0001_5  check esm mode status
    Sub-Case  CONSR-SEST-STRS-0027-0001_6  downgrade cpld with mode 0xe + reset 00h
    Sub-Case  CONSR-SEST-STRS-0027-0001_7  check esm mode status
    Sub-Case  CONSR-SEST-STRS-0027-0001_8  upgrade cpld with mode 0xe + reset 00h
    Sub-Case  CONSR-SEST-STRS-0027-0001_9  check esm mode status
    Sub-Case  CONSR-SEST-STRS-0027-0001_10  downgrade cpld with mode 0xe + power cycle
    Sub-Case  CONSR-SEST-STRS-0027-0001_11  check esm mode status
    Sub-Case  CONSR-SEST-STRS-0027-0001_12  upgrade cpld with mode 0xe + power cycle
    Sub-Case  CONSR-SEST-STRS-0027-0001_13  check esm mode status
    END
    [Teardown]  Run Keywords  Server Disconnect
           ...  AND Disconnect

CONSR-SEST-SPCK-0062-0001
    [Documentation]  This test checks PHY Control Diagnostic Page (14h) - PHY Information Get
    [Tags]  CONSR-SEST-SPCK-0062-0001  Titan-K  
    [Timeout]  5 min 00 seconds
    [Setup]  server Connect
    Step  1  verify phy information  ${phy_read_command}  ${phy_get_command}  ${phy_check_pattern}
    [Teardown]  Server Disconnect

CONSR-SEST-SPCK-0064-0001
    [Documentation]  This test checks PHY Control Diagnostic Page (14h) - PHY Status Control (00 ON)
    [Tags]  CONSR-SEST-SPCK-0064-0001  Titan-K
    [Timeout]  5 min 00 seconds
    [Setup]  server Connect
    Step  1  verify phy information  ${enable_phy_command}  ${phy_get_command}  ${phy_enable_check_pattern}
    [Teardown]  Server Disconnect

CONSR-SEST-SCSI-0018-0001
    [Documentation]  SCSI Support Diagnostic Page - MODE SENSE (3Fh:00)
    [Tags]     CONSR-SEST-SCSI-0018-0001  Titan-K
    [Timeout]  5 min 00 seconds
    [Setup]     server Connect
    Step  1     check Command Pattern  ${mode_sense_page3Fh_00_cmd}  ${mode_sense_page3Fh_00_pattern}
    [Teardown]  Server Disconnect

CONSR-SEST-SCSI-0019-0001
    [Documentation]  SCSI Support Diagnostic Page - MODE SENSE  (3Fh:FF)
    [Tags]     CONSR-SEST-SCSI-0019-0001  Titan-K
    [Timeout]  5 min 00 seconds
    [Setup]     server Connect
    Step  1     check Command Pattern  ${mode_sense_page3Fh_ff_cmd}  ${mode_sense_page3Fh_ff_pattern}
    [Teardown]  Server Disconnect

CONSR-SEST-SPCK-0063-0001
    [Documentation]  This test checks PHY Control Diagnostic Page (14h) - PHY Status Control (01 OFF)
    [Tags]  CONSR-SEST-SPCK-0063-0001  Titan-K
    [Timeout]  5 min 00 seconds
    [Setup]  server Connect
    Step  1  verify phy information  ${disable_phy_command}  ${phy_get_command}  ${phy_disable_check_pattern}
    [Teardown]  Server Disconnect

CONSR-SEST-SCSI-0016-0001
    [Documentation]  SCSI Support Diagnostic Page - MODE SENSE (18h)
    [Tags]     CONSR-SEST-SCSI-0016-0001  Titan-K
    [Timeout]  5 min 00 seconds
    [Setup]     server Connect
    Step  1     check Command Pattern  ${mode_sense_page18_cmd}  ${mode_sense_page18_pattern}
    [Teardown]  Server Disconnect

CONSR-SEST-SCSI-0017-0001
    [Documentation]  SCSI Support Diagnostic Page - MODE SENSE (19h)
    [Tags]     CONSR-SEST-SCSI-0017-0001  Titan-K
    [Timeout]  5 min 00 seconds
    [Setup]     server Connect
    Step  1     check Command Pattern  ${mode_sense_page19_cmd}  ${mode_sense_page19_pattern}
    [Teardown]  Server Disconnect

CONSR-SEST-SPCK-0071-0001    
    [Documentation]  Error Injection Control Diagnostic Page (15h) - Configuration Descriptor
    [Tags]     CONSR-SEST-SPCK-0071-0001  Titan-K
    [Timeout]  5 min 00 seconds
    [Setup]     server Connect
    Step  1    get Control Decscriptor Information  ${control_descriptor_cmd}
    Step  2    check Command Pattern  ${page_15_status_cmd}  ${page_15_status_pattern}
    [Teardown]  Server Disconnect

CONSR-SEST-SPCK-0066-0001
    [Documentation]  This test checks Error Injection Control Diagnostic Page (15h) - Control Descriptor List (PS)
    [Tags]  CONSR-SEST-SPCK-0066-0001  Titan-K
    [Timeout]  5 min 00 seconds
    [Setup]  server Connect
    Step  1  error Injection Control Diagnostic Page Trigger   ${ses_page_tool_cmd}  ${elem_id_0}  ${psu_trigger_on_value}  ${psu_trigger_on_pattern_0}  ${page_15_status_cmd}  ${page_15_psu_trigger_on_pattern_0}  
    Step  2  error Injection Control Diagnostic Page Trigger   ${ses_page_tool_cmd}  ${elem_id_0}  ${psu_trigger_off_value}  ${psu_trigger_off_pattern_0}  ${page_15_status_cmd}  ${page_15_psu_trigger_off_pattern_0}
    Step  3  error Injection Control Diagnostic Page Trigger   ${ses_page_tool_cmd}  ${elem_id_1}  ${psu_trigger_on_value}  ${psu_trigger_on_pattern_1}  ${page_15_status_cmd}  ${page_15_psu_trigger_on_pattern_1}
    Step  4  error Injection Control Diagnostic Page Trigger   ${ses_page_tool_cmd}  ${elem_id_1}  ${psu_trigger_off_value}  ${psu_trigger_off_pattern_1}  ${page_15_status_cmd}  ${page_15_psu_trigger_off_pattern_0}
    Step  5  error Injection Control Diagnostic Page Trigger   ${ses_page_tool_cmd}  ${elem_id_2}  ${psu_trigger_on_value}  ${psu_trigger_on_pattern_2}  ${page_15_status_cmd}  ${page_15_psu_trigger_on_pattern_2}
    Step  6  error Injection Control Diagnostic Page Trigger   ${ses_page_tool_cmd}  ${elem_id_2}  ${psu_trigger_off_value}  ${psu_trigger_off_pattern_2}  ${page_15_status_cmd}  ${page_15_psu_trigger_off_pattern_0}
    Step  7  error Injection Control Diagnostic Page Trigger   ${ses_page_tool_cmd}  ${elem_id_3}  ${psu_trigger_on_value}  ${psu_trigger_on_pattern_3}  ${page_15_status_cmd}  ${page_15_psu_trigger_on_pattern_3}
    Step  8  error Injection Control Diagnostic Page Trigger   ${ses_page_tool_cmd}  ${elem_id_3}  ${psu_trigger_off_value}  ${psu_trigger_off_pattern_3}  ${page_15_status_cmd}  ${page_15_psu_trigger_off_pattern_0}
    Step  9  error Injection Control Diagnostic Page Trigger   ${ses_page_tool_cmd}  ${elem_id_4}  ${psu_trigger_on_value}  ${psu_trigger_on_pattern_4}  ${page_15_status_cmd}  ${page_15_psu_trigger_on_pattern_4}
    Step  10  error Injection Control Diagnostic Page Trigger   ${ses_page_tool_cmd}  ${elem_id_4}  ${psu_trigger_off_value}  ${psu_trigger_off_pattern_4}  ${page_15_status_cmd}  ${page_15_psu_trigger_off_pattern_0}
    Step  11  error Injection Control Diagnostic Page Trigger   ${ses_page_tool_cmd}  ${elem_id_5}  ${psu_trigger_on_value}  ${psu_trigger_on_pattern_5}  ${page_15_status_cmd}  ${page_15_psu_trigger_on_pattern_5}
    Step  12  error Injection Control Diagnostic Page Trigger   ${ses_page_tool_cmd}  ${elem_id_5}  ${psu_trigger_off_value}  ${psu_trigger_off_pattern_5}  ${page_15_status_cmd}  ${page_15_psu_trigger_off_pattern_0}
    [Teardown]  Server Disconnect

CONSR-SEST-SPCK-0067-0001
    [Documentation]  This test checks Error Injection Control Diagnostic Page (15h) - Control Descriptor List (Cooling)
    [Tags]  CONSR-SEST-SPCK-0067-0001  Titan-K
    [Timeout]  5 min 00 seconds
    [Setup]  server Connect
    Step  1  error Injection Control Diagnostic Page Trigger   ${ses_page_tool_cmd}  ${elem_id_0}  ${cooling_trigger_on_value}  ${cooling_trigger_on_pattern_0}  ${page_15_status_cmd}  ${page_15_cooling_trigger_on_pattern_0}
    Step  2  error Injection Control Diagnostic Page Trigger   ${ses_page_tool_cmd}  ${elem_id_0}  ${cooling_trigger_off_value}  ${cooling_trigger_off_pattern_0}  ${page_15_status_cmd}  ${page_15_cooling_trigger_off_pattern_0}
    Step  3  error Injection Control Diagnostic Page Trigger   ${ses_page_tool_cmd}  ${elem_id_1}  ${cooling_trigger_on_value}  ${cooling_trigger_on_pattern_1}  ${page_15_status_cmd}  ${page_15_cooling_trigger_on_pattern_1}
    Step  4  error Injection Control Diagnostic Page Trigger   ${ses_page_tool_cmd}  ${elem_id_1}  ${cooling_trigger_off_value}  ${cooling_trigger_off_pattern_1}  ${page_15_status_cmd}  ${page_15_cooling_trigger_off_pattern_0}
    Step  5  error Injection Control Diagnostic Page Trigger   ${ses_page_tool_cmd}  ${elem_id_2}  ${cooling_trigger_on_value}  ${cooling_trigger_on_pattern_2}  ${page_15_status_cmd}  ${page_15_cooling_trigger_on_pattern_2}
    Step  6  error Injection Control Diagnostic Page Trigger   ${ses_page_tool_cmd}  ${elem_id_2}  ${cooling_trigger_off_value}  ${cooling_trigger_off_pattern_2}  ${page_15_status_cmd}  ${page_15_cooling_trigger_off_pattern_0}
    Step  7  error Injection Control Diagnostic Page Trigger   ${ses_page_tool_cmd}  ${elem_id_3}  ${cooling_trigger_on_value}  ${cooling_trigger_on_pattern_3}  ${page_15_status_cmd}  ${page_15_cooling_trigger_on_pattern_3}
    Step  8  error Injection Control Diagnostic Page Trigger   ${ses_page_tool_cmd}  ${elem_id_3}  ${cooling_trigger_off_value}  ${cooling_trigger_off_pattern_3}  ${page_15_status_cmd}  ${page_15_cooling_trigger_off_pattern_0}
    Step  9  error Injection Control Diagnostic Page Trigger   ${ses_page_tool_cmd}  ${elem_id_4}  ${cooling_trigger_on_value}  ${cooling_trigger_on_pattern_4}  ${page_15_status_cmd}  ${page_15_cooling_trigger_on_pattern_4}
    Step  10  error Injection Control Diagnostic Page Trigger   ${ses_page_tool_cmd}  ${elem_id_4}  ${cooling_trigger_off_value}  ${cooling_trigger_off_pattern_4}  ${page_15_status_cmd}  ${page_15_cooling_trigger_off_pattern_0}
    [Teardown]  Server Disconnect

CONSR-SEST-SPCK-0068-0001
    [Documentation]  This test checks Error Injection Control Diagnostic Page (15h) - Control Descriptor List (temp)
    [Tags]  CONSR-SEST-SPCK-0068-0001  Titan-K
    [Timeout]  5 min 00 seconds
    [Setup]  server Connect
    Step  1  error Injection Control Diagnostic Page Trigger   ${ses_page_tool_cmd}  ${elem_id_0}  ${temp_trigger_on_value}  ${temp_trigger_on_pattern_0}  ${page_15_status_cmd}  ${page_15_temp_trigger_on_pattern_0}
    Step  2  error Injection Control Diagnostic Page Trigger   ${ses_page_tool_cmd}  ${elem_id_0}  ${temp_trigger_off_value}  ${temp_trigger_off_pattern_0}  ${page_15_status_cmd}  ${page_15_temp_trigger_off_pattern_0} 
    Step  3  error Injection Control Diagnostic Page Trigger   ${ses_page_tool_cmd}  ${elem_id_1}  ${temp_trigger_on_value}  ${temp_trigger_on_pattern_1}  ${page_15_status_cmd}  ${page_15_temp_trigger_on_pattern_1}
    Step  4  error Injection Control Diagnostic Page Trigger   ${ses_page_tool_cmd}  ${elem_id_1}  ${temp_trigger_off_value}  ${temp_trigger_off_pattern_1}  ${page_15_status_cmd}  ${page_15_temp_trigger_off_pattern_0}
    Step  5  error Injection Control Diagnostic Page Trigger   ${ses_page_tool_cmd}  ${elem_id_2}  ${temp_trigger_on_value}  ${temp_trigger_on_pattern_2}  ${page_15_status_cmd}  ${page_15_temp_trigger_on_pattern_2}
    Step  6  error Injection Control Diagnostic Page Trigger   ${ses_page_tool_cmd}  ${elem_id_2}  ${temp_trigger_off_value}  ${temp_trigger_off_pattern_2}  ${page_15_status_cmd}  ${page_15_temp_trigger_off_pattern_0}
    Step  7  error Injection Control Diagnostic Page Trigger   ${ses_page_tool_cmd}  ${elem_id_3}  ${temp_trigger_on_value}  ${temp_trigger_on_pattern_3}  ${page_15_status_cmd}  ${page_15_temp_trigger_on_pattern_3}
    Step  8  error Injection Control Diagnostic Page Trigger   ${ses_page_tool_cmd}  ${elem_id_3}  ${temp_trigger_off_value}  ${temp_trigger_off_pattern_3}  ${page_15_status_cmd}  ${page_15_temp_trigger_off_pattern_0}
    Step  9  error Injection Control Diagnostic Page Trigger   ${ses_page_tool_cmd}  ${elem_id_4}  ${temp_trigger_on_value}  ${temp_trigger_on_pattern_4}  ${page_15_status_cmd}  ${page_15_temp_trigger_on_pattern_4}
    Step  10  error Injection Control Diagnostic Page Trigger   ${ses_page_tool_cmd}  ${elem_id_4}  ${temp_trigger_off_value}  ${temp_trigger_off_pattern_4}  ${page_15_status_cmd}  ${page_15_temp_trigger_off_pattern_0}
    Step  11  error Injection Control Diagnostic Page Trigger   ${ses_page_tool_cmd}  ${elem_id_5}  ${temp_trigger_on_value}  ${temp_trigger_on_pattern_5}  ${page_15_status_cmd}  ${page_15_temp_trigger_on_pattern_5}
    Step  12  error Injection Control Diagnostic Page Trigger   ${ses_page_tool_cmd}  ${elem_id_5}  ${temp_trigger_off_value}  ${temp_trigger_off_pattern_5}  ${page_15_status_cmd}  ${page_15_temp_trigger_off_pattern_0}
    Step  13  error Injection Control Diagnostic Page Trigger   ${ses_page_tool_cmd}  ${elem_id_6}  ${temp_trigger_on_value}  ${temp_trigger_on_pattern_6}  ${page_15_status_cmd}  ${page_15_temp_trigger_on_pattern_6}
    Step  14  error Injection Control Diagnostic Page Trigger   ${ses_page_tool_cmd}  ${elem_id_6}  ${temp_trigger_off_value}  ${temp_trigger_off_pattern_6}  ${page_15_status_cmd}  ${page_15_temp_trigger_off_pattern_0}
    Step  15  error Injection Control Diagnostic Page Trigger   ${ses_page_tool_cmd}  ${elem_id_7}  ${temp_trigger_on_value}  ${temp_trigger_on_pattern_7}  ${page_15_status_cmd}  ${page_15_temp_trigger_on_pattern_7}
    Step  16  error Injection Control Diagnostic Page Trigger   ${ses_page_tool_cmd}  ${elem_id_7}  ${temp_trigger_off_value}  ${temp_trigger_off_pattern_7}  ${page_15_status_cmd}  ${page_15_temp_trigger_off_pattern_0}
    [Teardown]  Server Disconnect

CONSR-SEST-SPCK-0061-0001
    [Documentation]  This test case checks Log Status Diagnostic Page (13h) - page status 
    [Tags]     CONSR-SEST-SPCK-0061-0001  Titan-K
    [Timeout]  5 min 00 seconds
    [Setup]    server Connect
    Step  1    check Command Pattern  ${page_13_status_cmd}  ${page_13_status_pattern}
    [Teardown]  Server Disconnect

CONSR-SEST-SPCK-0069-0001
    [Documentation]  This test checks Error Injection Control Diagnostic Page (15h) - Control Descriptor List (Voltage)
    [Tags]  CONSR-SEST-SPCK-0069-0001  Titan-K
    [Timeout]  5 min 00 seconds
    [Setup]  server Connect
    Step  1  error Injection Control Diagnostic Page Trigger   ${ses_page_tool_cmd}  ${elem_id_0}  ${voltage_trigger_on_value}  ${voltage_trigger_on_pattern_0}  ${page_15_status_cmd}  ${page_15_voltage_trigger_on_pattern_0}
    Step  2  error Injection Control Diagnostic Page Trigger   ${ses_page_tool_cmd}  ${elem_id_0}  ${voltage_trigger_off_value}  ${voltage_trigger_off_pattern_0}  ${page_15_status_cmd}  ${page_15_voltage_trigger_off_pattern_0}
    Step  3  error Injection Control Diagnostic Page Trigger   ${ses_page_tool_cmd}  ${elem_id_1}  ${voltage_trigger_on_value}  ${voltage_trigger_on_pattern_1}  ${page_15_status_cmd}  ${page_15_voltage_trigger_on_pattern_1}
    Step  4  error Injection Control Diagnostic Page Trigger   ${ses_page_tool_cmd}  ${elem_id_1}  ${voltage_trigger_off_value}  ${voltage_trigger_off_pattern_1}  ${page_15_status_cmd}  ${page_15_voltage_trigger_off_pattern_0}    
    Step  5  error Injection Control Diagnostic Page Trigger   ${ses_page_tool_cmd}  ${elem_id_2}  ${voltage_trigger_on_value}  ${voltage_trigger_on_pattern_2}  ${page_15_status_cmd}  ${page_15_voltage_trigger_on_pattern_2}
    Step  6  error Injection Control Diagnostic Page Trigger   ${ses_page_tool_cmd}  ${elem_id_2}  ${voltage_trigger_off_value}  ${voltage_trigger_off_pattern_2}  ${page_15_status_cmd}  ${page_15_voltage_trigger_off_pattern_0}    
    Step  7  error Injection Control Diagnostic Page Trigger   ${ses_page_tool_cmd}  ${elem_id_3}  ${voltage_trigger_on_value}  ${voltage_trigger_on_pattern_3}  ${page_15_status_cmd}  ${page_15_voltage_trigger_on_pattern_3}
    Step  8  error Injection Control Diagnostic Page Trigger   ${ses_page_tool_cmd}  ${elem_id_3}  ${voltage_trigger_off_value}  ${voltage_trigger_off_pattern_3}  ${page_15_status_cmd}  ${page_15_voltage_trigger_off_pattern_0}
    Step  9  error Injection Control Diagnostic Page Trigger   ${ses_page_tool_cmd}  ${elem_id_4}  ${voltage_trigger_on_value}  ${voltage_trigger_on_pattern_4}  ${page_15_status_cmd}  ${page_15_voltage_trigger_on_pattern_4}
    Step  10  error Injection Control Diagnostic Page Trigger   ${ses_page_tool_cmd}  ${elem_id_4}  ${voltage_trigger_off_value}  ${voltage_trigger_off_pattern_4}  ${page_15_status_cmd}  ${page_15_voltage_trigger_off_pattern_0}
    Step  11  error Injection Control Diagnostic Page Trigger   ${ses_page_tool_cmd}  ${elem_id_5}  ${voltage_trigger_on_value}  ${voltage_trigger_on_pattern_5}  ${page_15_status_cmd}  ${page_15_voltage_trigger_on_pattern_5}
    Step  12  error Injection Control Diagnostic Page Trigger   ${ses_page_tool_cmd}  ${elem_id_5}  ${voltage_trigger_off_value}  ${voltage_trigger_off_pattern_5}  ${page_15_status_cmd}  ${page_15_voltage_trigger_off_pattern_0}
    Step  13  error Injection Control Diagnostic Page Trigger   ${ses_page_tool_cmd}  ${elem_id_6}  ${voltage_trigger_on_value}  ${voltage_trigger_on_pattern_6}  ${page_15_status_cmd}  ${page_15_voltage_trigger_on_pattern_6}
    Step  14  error Injection Control Diagnostic Page Trigger   ${ses_page_tool_cmd}  ${elem_id_6}  ${voltage_trigger_off_value}  ${voltage_trigger_off_pattern_6}  ${page_15_status_cmd}  ${page_15_voltage_trigger_off_pattern_0}
    Step  15  error Injection Control Diagnostic Page Trigger   ${ses_page_tool_cmd}  ${elem_id_7}  ${voltage_trigger_on_value}  ${voltage_trigger_on_pattern_7}  ${page_15_status_cmd}  ${page_15_voltage_trigger_on_pattern_7}
    Step  16  error Injection Control Diagnostic Page Trigger   ${ses_page_tool_cmd}  ${elem_id_7}  ${voltage_trigger_off_value}  ${voltage_trigger_off_pattern_7}  ${page_15_status_cmd}  ${page_15_voltage_trigger_off_pattern_0}
    [Teardown]  Server Disconnect

CONSR-SEST-SMRD-0039-0001
    [Documentation]  This test checks Threshold Out Diagnostic Pages(05h) - Temp LW
    [Tags]  CONSR-SEST-SMRD-0039-0001  Titan-K
    [Timeout]  5 min 00 seconds
    [Setup]  server Connect
    Step  1  temp lm upgrade test  0  ^0$
    Step  2  ESMAConnect  ${ESMA_IP_1}  ${ESMA_port_1}
    Step  3  verify_esm_fan_mode_cli_command  DUT  internal
    Step  4  Disconnect
    [Teardown]  Server Disconnect

CONSR-SEST-SMRD-0040-0001
    [Documentation]  This test checks Threshold Out Diagnostic Pages(05h) - Temp UC
    [Tags]  CONSR-SEST-SMRD-0040-0001  Titan-K
    [Timeout]  5 min 00 seconds
    [Setup]  server Connect
    Step  1  temp lm upgrade test  1  ^1$
    Step  2  ESMAConnect  ${ESMA_IP_1}  ${ESMA_port_1}
    Step  3  verify_esm_fan_mode_cli_command  DUT  external
    Step  4  Disconnect
    [Teardown]  Server Disconnect

CONSR-SEST-SPCK-0074-0001
    [Documentation]  This test checks CLI Over SES Status Diagnostic Page (0x10h)
    [Tags]  CONSR-SEST-SPCK-0074-0001  Titan-K
    [Timeout]  5 min 00 seconds
    [Setup]  server Connect
    Step  1  Sending Diag Test  ${reset_expander_0x_cmd}
    Step  2  Sending Diag Reset Test
    [Teardown]  Server Disconnect

CONSR-SEST-SPCK-0076-0001
    [Documentation]  This test checks CONSR-SEST-SPCK-0076-0001
    [Tags]  CONSR-SEST-SPCK-0076-0001  Titan-K
    [Timeout]  5 min 00 seconds
    [Setup]  server Connect
    ${Value}=  Fru Sn Test  ${chassis_in_cmd_list}  ${chassis_fa_cmd_list}
    Step  2  ESMAConnect  ${ESMA_IP_1}  ${ESMA_port_1}
    Step  3  fru get and compare  ${Value}  ${compare_FRU_SN_76}  ${FRU_SN_76}  ${FRU_SN_76}
    Step  4  Disconnect
    [Teardown]  Server Disconnect

CONSR-SEST-SPCK-0077-0001
    [Documentation]  This test checks CONSR-SEST-SPCK-0077-0001
    [Tags]  CONSR-SEST-SPCK-0077-0001  Titan-K
    [Timeout]  5 min 00 seconds
    [Setup]  server Connect
    ${Value}=  Fru Sn Test  ${chassis_in_cmd_list_77}  ${chassis_fa_cmd_list_77}
    Step  1  ESMAConnect  ${ESMA_IP_1}  ${ESMA_port_1}
    Step  2  fru get and compare  ${Value}  ${compare_77}  ${FRU_87}  ${right_pattern_87}
    Step  3  Disconnect
    [Teardown]  Server Disconnect

CONSR-SEST-SPCK-0078-0001
    [Documentation]  This test checks CONSR-SEST-SPCK-0078-0001
    [Tags]  CONSR-SEST-SPCK-0078-0001  Titan-K
    [Timeout]  5 min 00 seconds
    [Setup]  server Connect
    ${Value}=  Fru Sn Test  ${chassis_in_cmd_list_78}  ${chassis_fa_cmd_list_78}
    Step  1  ESMAConnect  ${ESMA_IP_1}  ${ESMA_port_1}
    Step  2  fru get and compare  ${Value}  ${compare_78}  ${FRU_78}  ${right_pattern_78}
    Step  3  Disconnect
    [Teardown]  Server Disconnect

CONSR-SEST-SPCK-0079-0001
    [Documentation]  This test checks CONSR-SEST-SPCK-0079-0001
    [Tags]  CONSR-SEST-SPCK-0079-0001  Titan-K
    [Timeout]  5 min 00 seconds
    [Setup]  server Connect
    ${Value}=  Fru Sn Test  ${chassis_in_cmd_list_79}  ${chassis_fa_cmd_list_79}
    Step  1  ESMAConnect  ${ESMA_IP_1}  ${ESMA_port_1}
    Step  2  fru get and compare  ${Value}  ${compare_79}  ${FRU_87}  ${right_pattern_87}
    Step  3  Disconnect
    [Teardown]  Server Disconnect

CONSR-SEST-SPCK-0080-0001
    [Documentation]  This test checks CONSR-SEST-SPCK-0080-0001
    [Tags]  CONSR-SEST-SPCK-0080-0001  Titan-K
    [Timeout]  5 min 00 seconds
    [Setup]  server Connect
    ${Value}=  Fru Sn Test  ${chassis_in_cmd_list_80}  ${chassis_fa_cmd_list_80}
    Step  1  ESMAConnect  ${ESMA_IP_1}  ${ESMA_port_1}
    Step  2  fru get and compare  ${Value}  ${compare_80}  ${FRU_80}  ${right_pattern_80}
    Step  3  Disconnect
    [Teardown]  Server Disconnect

CONSR-SEST-SPCK-0082-0001
    [Documentation]  This test checks CONSR-SEST-SPCK-0082-0001
    [Tags]  CONSR-SEST-SPCK-0082-0001  Titan-K
    [Timeout]  5 min 00 seconds
    [Setup]  server Connect
    ${Value}=  Fru Sn Test  ${chassis_in_cmd_list_82}  ${chassis_fa_cmd_list_82}
    Step  1  ESMAConnect  ${ESMA_IP_1}  ${ESMA_port_1}
    Step  2  fru get and compare  ${Value}  ${compare_82}  ${FRU_82}  ${right_pattern_82}
    Step  3  Disconnect
    [Teardown]  Server Disconnect

CONSR-SEST-SPCK-0083-0001
    [Documentation]  This test checks CONSR-SEST-SPCK-0083-0001
    [Tags]  CONSR-SEST-SPCK-0083-0001  Titan-K
    [Timeout]  5 min 00 seconds
    [Setup]  server Connect
    ${Value}=  Fru Sn Test  ${chassis_in_cmd_list_83}  ${chassis_fa_cmd_list_83}
    Step  1  ESMAConnect  ${ESMA_IP_1}  ${ESMA_port_1}
    Step  2  fru get and compare  ${Value}  ${compare_83}  ${FRU_83}  ${right_pattern_83}
    Step  3  Disconnect
    [Teardown]  Server Disconnect

CONSR-SEST-SPCK-0084-0001
    [Documentation]  This test checks CONSR-SEST-SPCK-0084-0001
    [Tags]  CONSR-SEST-SPCK-0084-0001  Titan-K
    [Timeout]  5 min 00 seconds
    [Setup]  server Connect
    ${Value}=  Fru Sn Test  ${chassis_in_cmd_list_84}  ${chassis_fa_cmd_list_84}
    Step  1  ESMAConnect  ${ESMA_IP_1}  ${ESMA_port_1}
    Step  2  fru get and compare  ${Value}  ${compare_84}  ${FRU_PN}  ${right_pattern_PN}
    Step  3  Disconnect
    [Teardown]  Server Disconnect

CONSR-SEST-SPCK-0085-0001
    [Documentation]  This test checks CONSR-SEST-SPCK-0085-0001
    [Tags]  CONSR-SEST-SPCK-0085-0001  Titan-K
    [Timeout]  5 min 00 seconds
    [Setup]  server Connect
    ${Value}=  Fru Sn Test  ${chassis_in_cmd_list_85}  ${chassis_fa_cmd_list_85}
    Step  1  ESMAConnect  ${ESMA_IP_1}  ${ESMA_port_1}
    Step  2  fru get and compare  ${Value}  ${compare_85}  ${FRU_SN}  ${right_pattern_SN}
    Step  3  Disconnect
    [Teardown]  Server Disconnect

CONSR-SEST-SPCK-0086-0001
    [Documentation]  This test checks CONSR-SEST-SPCK-0086-0001
    [Tags]  CONSR-SEST-SPCK-0086-0001  Titan-K
    [Timeout]  5 min 00 seconds
    [Setup]  server Connect
    ${Value}=  Fru Sn Test  ${chassis_in_cmd_list_86}  ${chassis_fa_cmd_list_86}
    Step  1  ESMAConnect  ${ESMA_IP_1}  ${ESMA_port_1}
    Step  2  fru get and compare  ${Value}  ${compare_86}  ${FRU_86}  ${right_pattern_86}
    Step  3  Disconnect
    [Teardown]  Server Disconnect

CONSR-SEST-SPCK-0087-0001
    [Documentation]  This test checks CONSR-SEST-SPCK-0087-0001
    [Tags]  CONSR-SEST-SPCK-0087-0001  Titan-K
    [Timeout]  5 min 00 seconds
    [Setup]  server Connect
    ${Value}=  Fru Sn Test  ${chassis_in_cmd_list_87}  ${chassis_fa_cmd_list_87}
    Step  1  ESMAConnect  ${ESMA_IP_1}  ${ESMA_port_1}
    Step  2  fru get and compare  ${Value}  ${compare_87}  ${FRU_87}  ${right_pattern_87}
    Step  3  Disconnect
    [Teardown]  Server Disconnect

CONSR-SEST-SPCK-0088-0001
    [Documentation]  This test checks CONSR-SEST-SPCK-0088-0001
    [Tags]  CONSR-SEST-SPCK-0088-0001  Titan-K
    [Timeout]  5 min 00 seconds
    [Setup]  server Connect
    ${Value}=  Fru Sn Test  ${chassis_in_cmd_list_88}  ${chassis_fa_cmd_list_88}
    Step  1  ESMAConnect  ${ESMA_IP_1}  ${ESMA_port_1}
    Step  2  fru get and compare  ${Value}  ${compare_88}  ${FRU_88}  ${right_pattern_88}
    Step  3  Disconnect
    [Teardown]  Server Disconnect

CONSR-SEST-SPCK-0089-0001
    [Documentation]  This test checks CONSR-SEST-SPCK-0089-0001
    [Tags]  CONSR-SEST-SPCK-0089-0001  Titan-K
    [Timeout]  5 min 00 seconds
    [Setup]  server Connect
    ${Value}=  Fru Sn Test  ${chassis_in_cmd_list_89}  ${chassis_fa_cmd_list_89}
    Step  1  ESMAConnect  ${ESMA_IP_1}  ${ESMA_port_1}
    Step  2  fru get and compare  ${Value}  ${compare_89}  ${FRU_89}  ${right_pattern_89}
    Step  3  Disconnect
    [Teardown]  Server Disconnect

CONSR-SEST-SPCK-0090-0001
    [Documentation]  This test checks CONSR-SEST-SPCK-0090-0001
    [Tags]  CONSR-SEST-SPCK-0090-0001  Titan-K
    [Timeout]  5 min 00 seconds
    [Setup]  server Connect
    ${Value}=  Fru Sn Test  ${chassis_in_cmd_list_90}  ${chassis_fa_cmd_list_90}
    Step  1  ESMAConnect  ${ESMA_IP_1}  ${ESMA_port_1}
    Step  2  fru get and compare  ${Value}  ${compare_90}  ${FRU_90}  ${right_pattern_90}
    Step  3  Disconnect
    [Teardown]  Server Disconnect

CONSR-SEST-SPCK-0091-0001
    [Documentation]  This test checks CONSR-SEST-SPCK-0091-0001
    [Tags]  CONSR-SEST-SPCK-0091-0001  Titan-K
    [Timeout]  5 min 00 seconds
    [Setup]  server Connect
    ${Value}=  Fru Sn Test  ${chassis_in_cmd_list_91}  ${chassis_fa_cmd_list_91}
    Step  1  ESMAConnect  ${ESMA_IP_1}  ${ESMA_port_1}
    Step  2  fru get and compare  ${Value}  ${compare_FRU_PN}  ${FRU_PN}  ${right_pattern_PN}
    Step  3  Disconnect
    [Teardown]  Server Disconnect

CONSR-SEST-SPCK-0092-0001
    [Documentation]  This test checks VPD information - Canister Customer FRU SN
    [Tags]  CONSR-SEST-SPCK-0092-0001  Titan-K
    [Timeout]  5 min 00 seconds
    [Setup]  server Connect
    ${Value}=  Fru Sn Test  ${Fru_in_cmd_list}  ${Fru_fa_cmd_list}
    Step  1  ESMAConnect  ${ESMA_IP_1}  ${ESMA_port_1}
    Step  2  fru get and compare  ${Value}  ${compare_FRU_SN}  ${FRU_SN}  ${right_pattern_SN}
    Step  3  Disconnect
    [Teardown]  Server Disconnect

CONSR-SEST-SPCK-0060-0001
    [Documentation]  This test checks Log Control Diagnostic Page (13h) - Get Log Entry Descriptor
    [Tags]   CONSR-SEST-SPCK-0060-0001  Titan-K
    [Timeout]  5 min 00 seconds
    [Setup]    server Connect
    Step  1    get Control Decscriptor Information   ${page_13_entries_num_cmd}
    Step  2    Verify log pattern   ${page_13_status_cmd}  ${log_entry_code}  ${clear_log_entry_pattern}
    Step  3    get Control Decscriptor Information   ${page_13_clear_log_cmd}
    Step  4    Verify log pattern   ${page_13_status_cmd}  ${clear_log_entry_code}  ${clear_log_entry_pattern}
    Step  5    CLI check for log entry
    [Teardown]  Server Disconnect


CONSR-SEST-SPCK-0061-0001
    [Documentation]  This test case checks Log Status Diagnostic Page (13h) - page status
    [Tags]     CONSR-SEST-SPCK-0061-0001  Titan-K
    [Timeout]  5 min 00 seconds
    [Setup]    server Connect
    Step  1    send a command  ${Page13_run_diag_command}
    Step  2    verify Page Status  ${page_13_status_cmd}
    [Teardown]  Server Disconnect

CONSR-SEST-IVMT-0010-0001
    [Documentation]  This test case checks PSU 0 status - page 02h
    [Tags]    CONSR-SEST-IVMT-0010-0001  Titan-K
    [Timeout]  5 min 00 seconds
    [Setup]    server Connect
    Step  1    check PSU status  ${psu0_status_pg2_cmd}  ${psu034_status_pg2_pattern}
    Step  2    CLI check for psu status  ${psu0_cli_pattern}
    [Teardown]  Server Disconnect

CONSR-SEST-IVMT-0011-0001
    [Documentation]  This test case checks PSU 1 status - page 02h
    [Tags]     CONSR-SEST-IVMT-0011-0001  Titan-K
    [Timeout]  5 min 00 seconds
    [Setup]    server Connect
    Step  1    check PSU status  ${psu1_status_pg2_cmd}  ${psu125_status_pg2_pattern}
    Step  2    CLI check for psu status  ${psu1_cli_pattern}
    [Teardown]  Server Disconnect

CONSR-SEST-IVMT-0012-0001
    [Documentation]  This test case checks PSU 2 status - page 02h
    [Tags]     CONSR-SEST-IVMT-0012-0001  Titan-K
    [Timeout]  5 min 00 seconds
    [Setup]    server Connect
    Step  1    check PSU status  ${psu2_status_pg2_cmd}  ${psu125_status_pg2_pattern}
    Step  2    CLI check for psu status  ${psu2_cli_pattern}
    [Teardown]  Server Disconnect

CONSR-SEST-IVMT-0013-0001
    [Documentation]  This test case checks PSU 3 status - page 02h
    [Tags]     CONSR-SEST-IVMT-0013-0001  Titan-K
    [Timeout]  5 min 00 seconds
    [Setup]    server Connect
    Step  1    check PSU status  ${psu3_status_pg2_cmd}  ${psu034_status_pg2_pattern}
    Step  2    check PSU status  ${psu4_status_pg2_cmd}  ${psu034_status_pg2_pattern}
    Step  3    check PSU status  ${psu5_status_pg2_cmd}  ${psu125_status_pg2_pattern}
    Step  4    CLI check for psu status  ${psu3_cli_pattern}
    Step  5    CLI check for psu status  ${psu4_cli_pattern}
    Step  6    CLI check for psu status  ${psu5_cli_pattern}
    [Teardown]  Server Disconnect

CONSR-SEST-IVMT-0014-0001
    [Documentation]  This test case checks PSU 0 Inventory - page 07h
    [Tags]     CONSR-SEST-IVMT-0014-0001  Titan-K
    [Timeout]  5 min 00 seconds
    [Setup]    server Connect
    Step  1    compare PSU status with CLI  ${psu0_Find_pattern}   ${psu0_status_pg7_cmd}  ${PSU1}
    [Teardown]  Server Disconnect

CONSR-SEST-IVMT-0015-0001
    [Documentation]  This test case checks PSU 1 Inventory - page 07h
    [Tags]     CONSR-SEST-IVMT-0015-0001  Titan-K
    [Timeout]  5 min 00 seconds
    [Setup]    server Connect
    Step  1    check Command Pattern  ${psu1_status_pg7_cmd}  ${psu1_status_pg7_pattern}
    Step  2    CLI check for psu status  ${psu1_cli_pattern}
    [Teardown]  Server Disconnect

CONSR-SEST-IVMT-0016-0001
    [Documentation]  This test case checks PSU 2 Inventory - page 07h
    [Tags]     CONSR-SEST-IVMT-0016-0001  TitanK
    [Timeout]  5 min 00 seconds
    [Setup]    server Connect
    Step  1    check Command Pattern  ${psu2_status_pg7_cmd}  ${psu2_status_pg7_pattern}
    Step  2    CLI check for psu status  ${psu2_cli_pattern}
    [Teardown]  Server Disconnect

CONSR-SEST-IVMT-0017-0001
    [Documentation]  This test case checks PSU 3 Inventory - page 07h
    [Tags]     CONSR-SEST-IVMT-0017-0001  Titan-K
    [Timeout]  5 min 00 seconds
    [Setup]    server Connect
    Step  1    compare PSU status with CLI  ${psu3_Find_pattern}  ${psu3_status_pg7_cmd}  ${PSU3}
    Step  2    compare PSU status with CLI  ${psu4_Find_pattern}  ${psu4_status_pg7_cmd}  ${PSU4}
    Step  3    check Command Pattern  ${psu5_status_pg7_cmd}  ${psu5_status_pg7_pattern}
    [Teardown]  Server Disconnect

CONSR-SEST-SPCK-0059-0001
    [Documentation]  This test checks Log Control Diagnostic Page (13h) - Log Misc Control
    [Tags]   CONSR-SEST-SPCK-0059-0001  Titan-K
    [Timeout]  5 min 00 seconds
    [Setup]    server Connect
    Step  1    send a command   ${page_13_new_log_check_cmd}
    Step  2    compare new log with CLI   ${page_13_status_cmd}
    Step  3    send a command  ${page_13_read_status_cmd}
    Step  4    Verify log pattern  ${page_13_status_cmd}  ${log_read_code}  ${page_13_read_status_pattern}
    Step  5    send a command  ${page_13_unread_status_cmd}
    Step  6    Verify log pattern  ${page_13_status_cmd}  ${log_unread_code}  ${page_13_unread_status_pattern}
    Step  7    send a command  ${page_13_clear_log_cmd}
    Step  8    Verify log pattern   ${page_13_status_cmd}  ${clear_log_entry_code}  ${clear_log_entry_pattern}
    Step  9    CLI check for log entry
    [Teardown]  Server Disconnect

CONSR-SEST-IVMT-0021-0001
    [Documentation]  This test case checks the array device disk Inventory - page 0Ah
    [Tags]     CONSR-SEST-IVMT-0021-0001  Titan-K
    [Timeout]  5 min 00 seconds
    [Setup]    server Connect
    Step  1    Verify element index flag as invalid  ${page_0a_command}  ${dev1_index31_60}  ${dev2_index1_30}
    Step  2    Verify element index flag as invalid  ${page_0a_command}  ${dev1_index68_90}  ${dev2_index61_67}
    Step  3    Verify element index flag as invalid  ${page_0a_command}  ${dev1_index31_60}  ${dev2_index76_90}
    Step  4    Verify element index flag as valid    ${page_0a_command}  ${dev1_index1_30}   ${dev2_index31_60}
    Step  5    Verify element index flag as valid    ${page_0a_command}  ${dev1_index61_67}   ${dev2_index68_75}
    [Teardown]  Server Disconnect

CONSR-SEST-IVMT-0019-0001
    [Documentation]  This test checks the array device disk status - page 02h
    [Tags]   CONSR-SEST-IVMT-0019-0001  Titan-K
    [Timeout]  5 min 00 seconds
    [Setup]    server Connect
    Step  1   check driver status  ${page_drvstatus_cmd}  ${drv0_29}  ${OK_status}  ${unsupported_status}
    Step  2   check driver status  ${page_drvstatus_cmd}  ${drv30_59}  ${unsupported_status}  ${OK_status}
    Step  3   check driver status  ${page_drvstatus_cmd}  ${drv75_82}  ${Notinstalled_status}   ${unsupported_status}
    Step  4   check driver status  ${page_drvstatus_cmd}  ${drv83_89}   ${unsupported_status}    ${Notinstalled_status}
    Step  5   check driver count and status  ${page_drvstatus_cmd}  ${drv60_66}  ${Notinstalled_status}  ${unsupported_status}  ${OK_status}  ${unsupported_status}
    Step  6   check driver count and status  ${page_drvstatus_cmd}  ${drv67_74}  ${unsupported_status}  ${Notinstalled_status}  ${unsupported_status}  ${OK_status}
    [Teardown]  Server Disconnect

CONSR-SEST-IVMT-0020-0001
    [Documentation]  This test checks the array device disk Inventory - page 07h
    [Tags]   CONSR-SEST-IVMT-0020-0001  Titan-K
    [Timeout]  5 min 00 seconds
    [Setup]    server Connect
    Step  1   check slot name format  ${page7_slotname_check_cmd}
    [Teardown]  Server Disconnect

CONSR-SEST-CLMT-0002-0001
    [Documentation]  This test checks SES Enclosure Control Page Cooling element- lowest fan speed
    [Tags]   CONSR-SEST-CLMT-0002-0001  Titan-K
    [Timeout]  5 min 00 seconds
    [Setup]    get dut variable
    Step  1    check fan speed   ${fan_min_speed}   ${fan_min_speed_cli}    ${fan_min_speed_g75cli}
    [Teardown]  Run Keywords  Server Disconnect
           ...  AND Disconnect

CONSR-SEST-CLMT-0003-0001
    [Documentation]  This test checks SES Enclosure Control Page Cooling element- highest speed
    [Tags]   CONSR-SEST-CLMT-0003-0001  Titan-K
    [Timeout]  5 min 00 seconds
    [Setup]    get dut variable
    Step  1    check fan speed   ${fan_max_speed}   ${fan_max_speed_l75cli}    ${fan_max_speed_g75cli}
    [Teardown]  Run Keywords  Server Disconnect
           ...  AND Disconnect

CONSR-SEST-CLMT-0001-0001
    [Documentation]  This test checks SES Enclosure Control Page Cooling element- current speed
    [Tags]   CONSR-SEST-CLMT-0001-0001   Titan-K
    [Timeout]  8 min 00 seconds
    [Setup]    get dut variable
    Step  1    check fan speed   ${fan_speed_10}   ${fan_speed_10_l75cli}    ${fan_speed_10_g75cli}
    Step  2    check fan speed   ${fan_speed_11}   ${fan_speed_11_l75cli}    ${fan_speed_11_g75cli}
    Step  3    check fan speed   ${fan_speed_12}   ${fan_speed_12_l75cli}    ${fan_speed_12_g75cli}
    Step  4    check fan speed   ${fan_speed_13}   ${fan_speed_13_l75cli}    ${fan_speed_13_g75cli}
    Step  5    verify current fan speed
    [Teardown]  Run Keywords  Server Disconnect
           ...  AND Disconnect

CONSR-SEST-SPCK-0058-0001
    [Documentation]  This test case checks Log Control Diagnostic Page (13h) - get log info
    [Tags]     CONSR-SEST-SPCK-0058-0001  Titan-K
    [Timeout]  5 min 00 seconds
    [Setup]    server Connect
    Step  1    send a command   ${page13_readlog_cmd}
    Step  2    compare log info with CLI    ${page_13_status_cmd}
    [Teardown]  Server Disconnect

CONSR-SEST-SPCK-0098-0001
   [Documentation]  This test case checks Page 0x10 timeout bit test
   [Tags]     CONSR-SEST-SPCK-0098-0001  Titan-K
   [Timeout]  5 min 00 seconds
   [Setup]    server Connect
   Step  1    verify display of page with timeout   ${pg10_diag_cmd}  ${pg10_status_cmd}  ${pg_Fail_pattern}
   [Teardown]  Server Disconnect

CONSR-SEST-SPCK-0097-0001
   [Documentation]  This test case checks Page 0x10 read ESM A primary expander log
   [Tags]     CONSR-SEST-SPCK-0097-0001  Titan-K
   [Timeout]  5 min 00 seconds
   [Setup]    server Connect
   Step  1    verify page with expander log    ${pg10_diag_cmd}   ${pg10_status_cmd}
   [Teardown]  Server Disconnect

CONSR-SEST-SPCK-0095-0001
   [Documentation]  This test case checks Page 0x17 timeout bit test
   [Tags]     CONSR-SEST-SPCK-0095-0001   Titan-K
   [Timeout]  5 min 00 seconds
   [Setup]    server Connect
   Step  1    verify display of page with timeout   ${pg17_diag_cmd}  ${pg17_status_cmd}  ${pg_Fail_pattern}
   Step  2    verify display of page with timeout   ${pg17_diag_sec1_cmd}  ${pg17_status_cmd}  ${pg_Fail_pattern}
   Step  3    verify display of page with timeout   ${pg17_diag_sec2_cmd}  ${pg17_status_cmd}  ${pg_Fail_pattern}
   [Teardown]  Server Disconnect

CONSR-SEST-SPCK-0094-0001
   [Documentation]  This test case checks Page 0x17  ESM A  all  expander log
   [Tags]     CONSR-SEST-SPCK-0094-0001    Titan-K
   [Timeout]  10 min 00 seconds
   [Setup]    server Connect
   Step  1   verify page with expander log  ${pg17_diag_cmd}   ${pg17_diag_sec1_cmd}    ${pg17_diag_sec2_cmd}   ${pg17_status_cmd}
   [Teardown]  Server Disconnect

CONSR-SEST-SPCK-0100-0001
    [Documentation]  This test case verify the Page 0x17 control + Page 0x10 status 
    [Tags]     CONSR-SEST-SPCK-0100-0001  Titan-K
    [Timeout]  5 min 00 seconds
    [Setup]    server Connect
    Step  1    Verify pattern match for 0x10 ses_page  ${ses_diag_10cmd}  ${ses_10page_cmd}  ${pattern0x10}
    [Teardown]  Server Disconnect  

CONSR-SEST-SPCK-0101-0001
    [Documentation]  This test case verify the Page 0x10 control + Page 0x17 status 
    [Tags]     CONSR-SEST-SPCK-0101-0001  Titan-K
    [Timeout]  5 min 00 seconds
    [Setup]    server Connect
    Step  1    Verify pattern match for 0x17 ses_page  ${ses_diag_17cmd}  ${ses_17page_cmd}  ${pattern}
    [Teardown]  Server Disconnect

CONSR-SEST-SPCK-0099-0001
    [Documentation]  This test case verify the Page 0x10 other CLI command test
    [Tags]     CONSR-SEST-SPCK-0099-0001  Titan-K
    [Timeout]  5 min 00 seconds
    [Setup]    server Connect
    Step  1    Verify page and log CLI pattern   ${log_filter_diag_cmd}  ${log_filter_page_cmd}  ${log_filter_CLI_cmd}
    Step  2    Verify page and log CLI pattern   ${log_about_diag_cmd}  ${log_about_page_cmd}  ${log_about_CLI_cmd}
    Step  3    Verify page and LED CLI pattern   ${log_LED_diag_cmd}  ${log_LED_page_cmd}  ${log_LED_CLI_cmd}
    Step  4    Verify ses page and log CLI pattern   ${log_sespage_diag_cmd}  ${log_sespage_page_cmd}
    [Teardown]  Server Disconnect

CONSR-SEST-SPCK-0096-0001
    [Documentation]  This test case verify the Page 0x17 other CLI command test
    [Tags]     CONSR-SEST-SPCK-0096-0001  Titan-K
    [Timeout]  5 min 00 seconds
    [Setup]    server Connect
    Step  1    Verify page and log CLI pattern   ${log_filter_diag_17cmd}  ${log_filter_page_17cmd}  ${log_filter_CLI_cmd}
    Step  2    Verify page and log CLI pattern   ${log_about_diag_17cmd}  ${log_filter_page_17cmd}  ${log_about_CLI_cmd}
    Step  3    Verify page and LED CLI pattern   ${log_LED_diag_17cmd}  ${log_filter_page_17cmd}  ${log_LED_CLI_cmd}
    Step  4    Verify ses page and log CLI pattern   ${log_sespage_diag_17cmd}  ${log_filter_page_17cmd}
    [Teardown]  Server Disconnect

CONSR-SEST-IVMT-0002-0001
    [Documentation]  This test case checks the canister B status - page 02h 
    [Tags]   CONSR-SEST-IVMT-0002-0001   Titan-K
    [Timeout]  5 min 00 seconds
    [Setup]    server Connect
    Step  1   verify canister status  ${page02_canisterB_cmd}    ${canisterB_status}
    [Teardown]  Server Disconnect

CONSR-SEST-IVMT-0001-0001
    [Documentation]  This test case checks the canister A status - page 02h
    [Tags]   CONSR-SEST-IVMT-0001-0001   Titan-K
    [Timeout]  5 min 00 seconds
    [Setup]    server Connect
    Step  1    verify cansiter status and FW version    ${page02_canisterA_cmd}    ${canisterA_status}
    [Teardown]  Server Disconnect

CONSR-SEST-CLMT-0007-0001
    [Documentation]  This test checks Fan Status Monitoring
    [Tags]   CONSR-SEST-CLMT-0007-0001   Titan-K
    [Timeout]  8 min 00 seconds
    [Setup]    get dut variable
    Step  1    set and verify fan control mode
    Step  2    set and verify pwm value
    Step  3    set and verify level
    [Teardown]  Run Keywords  Server Disconnect
           ...  AND Disconnect

CONSR-SEST-CLMT-0006-0001
    [Documentation]  This test checks Temperature Monitoring
    [Tags]   CONSR-SEST-CLMT-0006-0001   Titan-K
    [Timeout]  8 min 00 seconds
    [Setup]    server Connect
    Step  1    set and verify UW 
    Step  2    set and verify UC
    Step  3    set and verify LW
    Step  4    set and verify LC
    [Teardown]  Server Disconnect

CONSR-SEST-IVMT-0004-0001
    [Documentation]  This test case Check the canister B Inventory - page 07h
    [Tags]     CONSR-SEST-IVMT-0004-0001  Titan-K
    [Timeout]  5 min 00 seconds
    [Setup]    server Connect
    Step  1    Verify canister B inventory in page command   ${canister_b_ses_cmd}   ${canister_b_pattern} 
    [Teardown]  Server Disconnect

CONSR-SEST-IVMT-0003-0001
    [Documentation]  This test case Check the canister A Inventory - page 07h
    [Tags]     CONSR-SEST-IVMT-0003-0001  Titan-K
    [Timeout]  5 min 00 seconds
    [Setup]    server Connect
    Step  1    Verify canister details on CLI and page command  ${canister_a_ses_cmd}  ${canister_CLI_cmd}
    [Teardown]  Server Disconnect    

CONSR-SEST-SCSI-0020-0001
    [Documentation]  This testcase checks the SCSI Support page - report LUNs
    [Tags]     CONSR-SEST-SCSI-0020-0001  Titan-K  
    [Timeout]  5 min 00 seconds
    [Setup]    server Connect
    Step  1    Verify lun report  ${scsi_support_ses_cmd}  ${scsi_option}   ${lun_ses_pattern}
    [Teardown]  Server Disconnect

CONSR-SEST-PWMT-0006-0001
    [Documentation]  This test checks Voltage Monitoring
    [Tags]   CONSR-SEST-PWMT-0006-0001   Titan-K
    [Timeout]  8 min 00 seconds
    [Setup]    server Connect
    Step  1    set voltage and verify UW
    Step  2    set voltage and verify UC
    Step  3    set voltage and verify OW
    Step  4    set voltage and verify OC
    [Teardown]  Server Disconnect

CONSR-SEST-IVMT-0007-0001
    [Documentation]  This test checks enclosure status - page 02h
    [Tags]   CONSR-SEST-IVMT-0007-0001   Titan-K
    [Timeout]  8 min 00 seconds
    [Setup]    server Connect
    Step  1    check Command Pattern   ${pg2_enc_status_cmd}  ${pg2_enc_status}
    [Teardown]  Server Disconnect

CONSR-SEST-SPCK-0093-0001
    [Documentation]  This test checks Log Status Diagnostic Page (13h)- with wrong data
    [Tags]   CONSR-SEST-SPCK-0093-0001   Titan-K
    [Timeout]  8 min 00 seconds
    [Setup]    server Connect
    Step  1    verify log with wrong data   ${log_wrongdata_cmd}
    [Teardown]  Server Disconnect 

CONSR-SEST-SPCK-0073-0001
    [Documentation]  This test checks Enclosure Control Diagnostic Pages(02h) - ESCE report bit 
    [Tags]   CONSR-SEST-SPCK-0073-0001   Titan-K
    [Timeout]  8 min 00 seconds
    [Setup]    server Connect
    Step  1    verify ESCE report bit  ${pg2_esc0_cmd}  ${pg2_esc1_cmd}  ${reset_exp_cmd}  ${esc0_report_bit}  ${esc1_report_bit}
    [Teardown]  Server Disconnect

CONSR-SEST-DRMT-0006-0001 
    [Documentation]  This test checks phy enable_disable on expanders
    [Tags]    CONSR-SEST-DRMT-0006-0001    Titan-K
    [Timeout]  8 min 00 seconds
    [Setup]    server Connect
    Step  1    verify phy enable_disable on secondary expander1
    Step  2    verify phy enable_disable on secondary expander2
    Step  3    verify phy enable_disable on primary expander
    [Teardown]  Server Disconnect

CONSRS-DP-02-0001
    [Documentation]  This test checks Drive Disk Power On-Off - CLI
    [Tags]    CONSRS-DP-02-0001   Titan-K
    [Timeout]  8 min 00 seconds
    [Setup]    server Connect
    Step  1    verify drive disk power on_off  ${expdr_sec_1}  ${slot_num_sec1}  ${expdr_pri}   ${slot_num_pri_sec1}
    Step  2    verify drive disk power on_off  ${expdr_sec_2}  ${slot_num_sec2}  ${expdr_pri}   ${slot_num_pri_sec2}
    [Teardown]  Server Disconnect

CONSR-SEST-SPCK-0075-0001
    [Documentation]  This test checks VPD information Control/Status Diagnostic Page (12h)- VPD information-get all 
    [Tags]    CONSR-SEST-SPCK-0075-0001  Titan-K
    [Timeout]  8 min 00 seconds
    [Setup]    server Connect
    Step  1    verify VPD information 
    [Teardown]  Server Disconnect

CONSR-SEST-STRS-0002-0001
    [Documentation]   Drive Disk LED stress Test
    [Tags]     CONSR-SEST-STRS-0002-0001  Titan-K  regression
    [Timeout]  24 hours
    [Setup]  server Connect
    FOR    ${INDEX}    IN RANGE    ${MAXINDEX}
        Print Loop Info  ${INDEX}
	Step  1  verify drive disk LED on off status  ${set_on_ident_LED}   ${set_off_ident_LED}  ${get_page2_cmd}  ${get_ident_LED}  ${ident_disk_fault_LED_on_pattern}  ${ident_disk_fault_LED_off_pattern}
        Step  2  verify drive disk LED on off status  ${set_on_disk_fault_LED}  ${set_off_disk_fault_LED}  ${get_page2_cmd}  ${get_disk_fault_LED}  ${ident_disk_fault_LED_on_pattern}  ${ident_disk_fault_LED_off_pattern}
    END
    [Teardown]  Run Keywords  Server Disconnect
           ...  AND Disconnect

CONSR-SEST-STRS-0004-0001
    [Documentation]  Enclosure LED Stress Test
    [Tags]     CONSR-SEST-STRS-0004-0001  Titan-K  regression
    [Timeout]  24 hours
    [Setup]  server Connect
    FOR    ${INDEX}    IN RANGE    ${MAXINDEX}
        Print Loop Info  ${INDEX}
        Step  1  verify Enclosure LED on off status  ${set_on_enc_LED}   ${set_off_enc_LED}  ${get_cmd}  ${get_page2_cmd}  ${get_enc_LED}  ${enc_LED_on_pattern}  ${enc_LED_off_pattern}
    END
    [Teardown]  Run Keywords  Server Disconnect
           ...  AND Disconnect


CONSR-SEST-STRS-0003-0001
    [Documentation]   Canister LED stress Test
    [Tags]     CONSR-SEST-STRS-0003-0001  Titan-K  regression
    [Timeout]  24 hours
    [Setup]  server Connect
    FOR    ${INDEX}    IN RANGE    ${MAXINDEX}
        Print Loop Info  ${INDEX}
        Step  1  verify canister LED on off status  ${set_canister_ident_on}  ${clear_canister_ident}  ${check_can_ident0_cmd}  ${check_can_ident1_cmd}  ${get_ident_LED}   ${can_iden_on_pattern}  ${can_ident_off_pattern}  ${can_ident_on_pattern_total}  
        Step  2  verify canister LED on off status  ${set_canister_fault_on}  ${clear_canister_fault}  ${check_can_fault0_cmd}  ${check_can_fault1_cmd}  ${get_LED_8}  ${can_fault_on_pattern}  ${can_fault_off_pattern}  ${can_fault_on_pattern_total}

    END
    [Teardown]  Run Keywords  Server Disconnect
           ...  AND Disconnect

CONSR-SEST-SPCK-0081-0001                  	 	
    [Documentation]  This test checks VPD information - Product asset tag
    [Tags]    CONSR-SEST-SPCK-0081-0001     Titan-K
    [Timeout]  8 min 00 seconds
    [Setup]    server Connect
    Step  1   read write product asset tag
    [Teardown]  Server Disconnect

CONSR-SEST-IVMT-0008-0001
    [Documentation]  This test checks the enclosure Inventory - page 07h
    [Tags]   CONSR-SEST-IVMT-0008-0001   Titan-K
    [Timeout]  5 min 00 seconds
    [Setup]    server Connect
    Step  1    Verify Enclosure Inventory details on CLI and page command  ${Inventory_ses_cmd}  ${Inventory_CLI_cmd}
    [Teardown]  Server Disconnect

CONSRS-NI-01-0001
    [Documentation]  This test checks the Network IP config
    [Tags]   CONSRS-NI-01-0001   Titan-K
    [Timeout]  5 min 00 seconds
    [Setup]    server Connect
    Step  1    Verify IPconfig
    [Teardown]  Server Disconnect

CONSRS-PO-01-0001
    [Documentation]  This test checks Drive Disk Power On/Off Check with SES Page.
    [Tags]     CONSRS-PO-01-0001   Titan-K
    [Timeout]  8 min 00 seconds
    [Setup]    server Connect
    Step  1    verify Drive Disk Power
    [Teardown]  Server Disconnect

CONSR-SEST-IVMT-0027-0001
    [Documentation]  This test checks the modification of canister MFG date.
    [Tags]   CONSR-SEST-IVMT-0027-0001   Titan-K
    [Timeout]  15 min 00 seconds
    [Setup]    server Connect
    Step  1    Verify configuring and validating manufacturer date  ${date_set_cmd1}  ${mfg_date_pattern1}
    Step  2    Verify configuring and validating manufacturer date  ${date_set_cmd2}  ${mfg_date_pattern2}
    [Teardown]  Server Disconnect

CONSR-SEST-IVMT-0026-0001
    [Documentation]  This test checks the Fan VPD
    [Tags]   CONSR-SEST-IVMT-0026-0001   Titan-K
    [Timeout]  5 min 00 seconds
    [Setup]    server Connect
    Step  1    Modify Fan serial and HW EC number
    [Teardown]  Server Disconnect

CONSR-SEST-SPCK-0031-0001
    [Documentation]  This test checks String Out Diagnostic Pages(04h) - Command Code and Data for Reset(A0h)
    [Tags]    CONSR-SEST-SPCK-0031-0001     Titan-K
    [Timeout]  3 min 00 seconds
    [Setup]    server Connect
    Step  1    verify command code and data reset
    [Teardown]  Server Disconnect

CONSRS-SM-04-0001
    [Documentation]  This test checks  SMP PHY Control -  phy enable/disable
    [Tags]  CONSRS-SM-04-0001  Titan-K
    [Timeout]  10 min 00 seconds
    [Setup]    server Connect
    Step  1    verify smp phy enable disable
    [Teardown]  Server Disconnect

CONSRS-SM-03-0001
    [Documentation]  This test checks  SMP PHY Control - link speed program
    [Tags]  CONSRS-SM-03-0001  Titan-K
    [Timeout]  3 min 00 seconds
    [Setup]    server Connect
    Step  1    verify smp phy link speed
    [Teardown]  Server Disconnect

CONSR-SEST-SPCK-0032-0001
    [Documentation]  This test checks String Out Diagnostic Pages(04h) - Command Code and Data for IP Configuration(A1)
    [Tags]    CONSR-SEST-SPCK-0032-0001     Titan-K
    [Timeout]  3 min 00 seconds
    [Setup]    server Connect   
    Step  1    verify command code and data for IP Configuration
    [Teardown]  Server Disconnect

CONSR-SEST-CMDL-0002-0001
    [Documentation]  This test checks detailed CLI command setting and getting test
    [Tags]    CONSR-SEST-CMDL-0002-0001     Titan-K
    [Timeout]  3 min 00 seconds
    [Setup]    server Connect
    Step  1    verify CLI set get CLI command
    [Teardown]  Server Disconnect

CONSRS-SM-01-0001
    [Documentation]  This test checks SMP General Commands
    [Tags]    CONSRS-SM-01-0001   Titan-K
    [Timeout]  5 min 00 seconds
    [Setup]    server Connect
    Step  1    verify SMP commands
    [Teardown]  Server Disconnect

CONSRS-SM-05-0001
     [Documentation]  This test checks partial pathway timeout
     [Tags]   CONSRS-SM-05-0001   Titan-K
     [Timeout]  5 min 00 seconds
     [Setup]    server Connect
     Step  1    Setting partial pathway timeout value
     [Teardown]  Server Disconnect

CONSR-SEST-STRS-0007-0001
     [Documentation]  This test checks CPLD download Stress Test
     [Tags]  CONSR-SEST-STRS-0007-0001  Titan-K
     [Timeout]  30 min 00 seconds
     [Setup]   server Connect
     FOR    ${INDEX}    IN RANGE    ${MAXINDEX}
        Print Loop Info  ${INDEX}
        Sub-Case   CONSR-SEST-STRS-0007-0001_1   CONSR-SEST-FWDL-0035-0001
        Sub-Case   CONSR-SEST-STRS-0007-0001_2   CONSR-SEST-FWDL-0034-0001
     END
     [Teardown]  Run Keywords  Server Disconnect
           ...  AND Disconnect

FUN-09-01
    [Documentation]  This test checks I2C Sub System - I2C Read/Write	I2C Read/Write
    [Tags]   FUN-09-01   Titan-K 
    [Timeout]  8 min 00 seconds
    [Setup]    server Connect
	Step  1    verify i2c read write cli commands
    [Teardown]  Server Disconnect

FUN-09-02
    [Documentation]  This test checks I2C Sub System - I2C Read/Write-I2c Bus Stress
    [Tags]   FUN-09-02   Titan-K 
    [Timeout]  8 min 00 seconds
    [Setup]    server Connect
    FOR    ${INDEX}    IN RANGE    ${MAXINDEX}
        Print Loop Info  ${INDEX}
	Step  1    verify i2c read write cli commands
    END
    [Teardown]  Run Keywords  Server Disconnect
           ...  AND Disconnect

CONSR-SEST-SMRD-0046-0001
   [Documentation]  This test checks Fan mode cli check
   [Tags]   CONSR-SEST-SMRD-0046-0001   Athena-G2
   [Timeout]  5 min 00 seconds
   Step  1  OS Connect Device
   Step  2  verify fan mode
   Step  3  OS Disconnect Device
   Step  4  ConnectESMB
   Step  5  verify fan mode
   Step  6  OS Disconnect

CONSR-SEST-SMRD-0047-0001
   [Documentation]  This test checks Fan speed check
   [Tags]   CONSR-SEST-SMRD-0047-0001   Athena-G2
   [Timeout]  10 min 00 seconds
   Step  1   OS Connect Device
   Step  2   Verify fan speed  ${canisterA}
   Step  3   OS Disconnect Device
   Step  4   ConnectESMB
   Step  5   Verify fan speed  ${canisterB}
   Step  6   OS Disconnect

CONSR-SEST-SCSI-0011-0001
  [Documentation]  This test checks SCSI Support Diagnostic Page - Read Buffer
  [Tags]   CONSR-SEST-SCSI-0011-0001   Athena-G2
  [Timeout]  5 min 00 seconds
  Step  1  server Connect
  Step  2  verify read buffer
  Step  3  Server Disconnect
  Step  4  server Connect ESMB
  Step  5  verify read buffer
  Step  6  Server Disconnect

CONSR-SEST-SCSI-0020-0001-AthenaG2
  [Documentation]  This test checks SCSI Support page-Report LUNs
  [Tags]   CONSR-SEST-SCSI-0020-0001-AthenaG2  Athena-G2
  [Timeout]  5 min 00 seconds
  Step  1  server Connect
  Step  2  verify report luns
  Step  3  Server Disconnect
  Step  4  server Connect ESMB
  Step  5  verify report luns
  Step  6  Server Disconnect


CONSR-SEST-STRS-0011-0001
   [Documentation]  Stress Test of reset
   [Tags]   CONSR-SEST-STRS-0011-0001   Athena-G2
   Step  1    Perform local chip reset in a primary device
   Step  2    Check the basic parameters in ESM mode after local chip reset
   Step  3    Check the basic parameters in Linux OS after local chip reset


CONSR-SEST-STRS-0010-0001
   [Documentation]   SES Page Command Stress Test
   [Tags]   CONSR-SEST-STRS-0010-0001    Athena-G2

   Step  1    Execute SES Page Command for multiple iterations
   Step  2    Check the basic parameters in ESM mode after SES Page Command is executed multiple times


CONSR-SEST-SPCK-0107-0001
   [Documentation]   String Out Diagnostic Pages(04h)--VPD update--Board info area_field id 02
   [Tags]   CONSR-SEST-SPCK-0107-0001   Athena-G2

   Step  1    server Connect
   Step  2    String Out Diagnostic Pages-04h--VPD update--Board info area_field id 02
   Step  3    Server Disconnect
   Step  4    server Connect ESMB
   Step  5    String Out Diagnostic Pages-04h--VPD update--Board info area_field id 02
   Step  6    Server Disconnect

CONSR-SEST-SPCK-0023-0001-AthenaG2
   [Documentation]  This test checks enclosure status diagnostics
   [Tags]   CONSR-SEST-SPCK-0023-0001-AthenaG2   Athena-G2
   [Timeout]  10 min 00 seconds
   Step  1   server Connect
   Step  2   Compare enclosure status of two ESMs   ${encl_cmd}
   Step  3   Server Disconnect

CONSR-SEST-SPCK-0106-0001
   [Documentation]  This test checks String Out Diagnostic Pages(04h)--VPD update--Board info area_field id 01
   [Tags]   CONSR-SEST-SPCK-0106-0001   Athena-G2
   [Timeout]  10 min 00 seconds
   Step  1    server Connect
   Step  2    String Out Diagnostic Pages(04h)--VPD update--Board info area_field id 01
   Step  3    Server Disconnect
   Step  4    server Connect ESMB
   Step  5    String Out Diagnostic Pages(04h)--VPD update--Board info area_field id 01
   Step  6    Server Disconnect

CONSR-SEST-SPCK-0108-0001
   [Documentation]  This test checks String Out Diagnostic Pages(04h)--VPD update--Board info area_field id 03
   [Tags]   CONSR-SEST-SPCK-0108-0001   Athena-G2
   [Timeout]  10 min 00 seconds
   Step  1    server Connect
   Step  2    String Out Diagnostic Pages(04h)--VPD update--Board info area_field id 03
   Step  3    Server Disconnect
   Step  4    server Connect ESMB
   Step  5    String Out Diagnostic Pages(04h)--VPD update--Board info area_field id 03
   Step  6    Server Disconnect


CONSR-SEST-STRS-0009-0001
  [Documentation]  This test checks CLI Command Stress Test
  [Tags]  CONSR-SEST-STRS-0009-0001  Athena-G2
  [Timeout]  48 hours
  Step  1    OS Connect Device
  Step  2    execute and check completion of CLI commands
  Step  3    OS Disconnect Device
  Step  4    ConnectESMB
  Step  5    execute and check completion of CLI commands
  Step  6    OS Disconnect Device

CONSR-SEST-SPCK-0109-0001
  [Documentation]  This test checks String Out Diagnostic Pages(04h)--VPD update--Board info area_field id 04
  [Tags]   CONSR-SEST-SPCK-0109-0001   Athena-G2
  [Timeout]  10 min 00 seconds
  Step  1  server Connect
  Step  2  String Out Diagnostic Pages(04h)--VPD update--Board info area_field id 04
  Step  3  Server Disconnect
  Step  4  server Connect ESMB
  Step  5  String Out Diagnostic Pages(04h)--VPD update--Board info area_field id 04
  Step  6  Server Disconnect

CONSR-SEST-SPCK-0110-0001
   [Documentation]   String Out Diagnostic Pages(04h)--VPD update--Chassis info area_field id 01
   [Tags]   CONSR-SEST-SPCK-0110-0001   Athena-G2

   Step  1    server Connect
   Step  2    String Out Diagnostic Pages(04h)--VPD update--Chassis info area_field id 01
   Step  3    Server Disconnect
   Step  4    server Connect ESMB
   Step  5    String Out Diagnostic Pages(04h)--VPD update--Chassis info area_field id 01
   Step  6    Server Disconnect

CONSR-SEST-SPCK-0112-0001
  [Documentation]  This test checks String Out Diagnostic Pages(04h)--VPD update--Chassis info area_field id 03
  [Tags]  CONSR-SEST-SPCK-0112-0001  Athena-G2
  [Timeout]  10 min 00 seconds
  Step  1  server Connect
  Step  2  String Out Diagnostic Pages(04h)--VPD update--Chassis info area_field id 03
  Step  3  Server Disconnect
  Step  4  server Connect ESMB
  Step  5  String Out Diagnostic Pages(04h)--VPD update--Chassis info area_field id 03-ESM
  Step  5  String Out Diagnostic Pages(04h)--VPD update--Chassis info area_field id 03
  Step  6  Server Disconnect
  Step  7  server Connect
  Step  8  String Out Diagnostic Pages(04h)--VPD update--Chassis info area_field id 03-ESM
  Step  9  Server Disconnect

CONSR-SEST-SPCK-0113-0001
   [Documentation]   String Out Diagnostic Pages(04h)--VPD update--Product info area_field id 01
   [Tags]   CONSR-SEST-SPCK-0113-0001   Athena-G2

   Step  1    server Connect
   Step  2    String Out Diagnostic Pages(04h)--VPD update--Product info area_field id 01
   Step  3    Server Disconnect
   Step  4    server Connect ESMB
   Step  5    String Out Diagnostic Pages(04h)--VPD update--Product info area_field id 01
   Step  6    Server Disconnect

CONSR-SEST-SPCK-0115-0001
  [Documentation]  This test checks String Out Diagnostic Pages(04h)--VPD update--Product info area_field id 03
  [Tags]  CONSR-SEST-SPCK-0115-0001  Athena-G2
  [Timeout]  10 min 00 seconds
  Step  1  server Connect
  Step  2  String Out Diagnostic Pages(04h)--VPD update--Product info area_field id 03
  Step  3  Server Disconnect
  Step  4  server Connect ESMB
  Step  5  String Out Diagnostic Pages(04h)--VPD update--Product info area_field id 03
  Step  6  Server Disconnect

CONSR-SEST-SPCK-0116-0001
  [Documentation]  This test checks String Out Diagnostic Pages(04h)--VPD update--Product info area_field id 04
  [Tags]  CONSR-SEST-SPCK-0116-0001  Athena-G2
  [Timeout]  10 min 00 seconds
  Step  1  server Connect
  Step  2  String Out Diagnostic Pages(04h)--VPD update--Product info area_field id 04
  Step  3  Server Disconnect
  Step  4  server Connect ESMB
  Step  5  String Out Diagnostic Pages(04h)--VPD update--Product info area_field id 04
  Step  6  Server Disconnect

CONSR-SEST-SPCK-0114-0001
  [Documentation]  String Out Diagnostic Pages(04h)--VPD update--Product info area_field id 02
  [Tags]  CONSR-SEST-SPCK-0114-0001  Athena-G2
  [Timeout]  10 min 00 seconds
  Step  1  server Connect
  Step  2  String Out Diagnostic Pages(04h)--VPD update--Product info area_field id 02
  Step  3  Server Disconnect
  Step  4  server Connect ESMB
  Step  5  String Out Diagnostic Pages(04h)--VPD update--Product info area_field id 02
  Step  6  Server Disconnect

CONSR-SEST-SPCK-0104-0001
  [Documentation]  This test checks Timestamp Set Diagnostic Page (11h) --- set outer margin of timestamp
  [Tags]  CONSR-SEST-SPCK-0104-0001   Athena-G2
  [Timeout]  10 min 00 seconds
  Step  1  server Connect
  Step  2  Timestamp Set Diagnostic Page (11h) --- set outer margin of timestamp
  Step  3  Server Disconnect
  Step  4  server Connect ESMB
  Step  5  Timestamp Set Diagnostic Page (11h) --- set outer margin of timestamp
  Step  6  Server Disconnect

CONSR-SEST-SPCK-0105-0001
  [Documentation]  This test checks Timestamp Set Diagnostic Page (11h) --- Get status page
  [Tags]  CONSR-SEST-SPCK-0105-0001   Athena-G2
  [Timeout]  10 min 00 seconds
  Step  1  server Connect
  Step  2  Timestamp Set Diagnostic Page (11h) --- Get status page
  Step  3  Server Disconnect
  Step  4  server Connect ESMB
  Step  5  Timestamp Set Diagnostic Page (11h) --- Get status page
  Step  6  Server Disconnect

CONSR-SEST-SPCK-0111-0001
   [Documentation]  This test checks String Out Diagnostic Pages(04h)--VPD update--Chassis info area_field id 02
   [Tags]   CONSR-SEST-SPCK-0111-0001   Athena-G2
   Step  1    server Connect
   Step  2    String Out Diagnostic Pages(04h)--VPD update--Chassis info area_field id 02
   Step  3    Server Disconnect
   Step  4    server Connect ESMB
   Step  5    String Out Diagnostic Pages(04h)--VPD update--Chassis info area_field id 02-ESM
   Step  6    String Out Diagnostic Pages(04h)--VPD update--Chassis info area_field id 02
   Step  6    Server Disconnect
   Step  7    server Connect
   Step  8    String Out Diagnostic Pages(04h)--VPD update--Chassis info area_field id 02-ESM
   Step  9    Server Disconnect
 
CONSR-SEST-SPCK-0117-0001
   [Documentation]  This test checks String Out Diagnostic Pages(04h)--VPD update--Product info area_field id 05
   [Tags]   CONSR-SEST-SPCK-0117-0001   Athena-G2
   Step  1    server Connect
   Step  2    String Out Diagnostic Pages(04h)--VPD update--Product info area_field id 05
   Step  3    Server Disconnect
   Step  4    server Connect ESMB
   Step  5    String Out Diagnostic Pages(04h)--VPD update--Product info area_field id 05
   Step  6    Server Disconnect
       
CONSR-SEST-SPCK-0118-0001
   [Documentation]  This test checks String Out Diagnostic Pages(04h)--VPD update--Product info area_field id 06
   [Tags]   CONSR-SEST-SPCK-0118-0001   Athena-G2
   Step  1    server Connect
   Step  2    String Out Diagnostic Pages(04h)--VPD update--Product info area_field id 06
   Step  3    Server Disconnect
   Step  4    server Connect ESMB
   Step  5    String Out Diagnostic Pages(04h)--VPD update--Product info area_field id 06
   Step  6    Server Disconnect
   [Teardown]   VPD update clean up

CONSR-SEST-SPCK-0102-0001
   [Documentation]  This test checks Timestamp Set Diagnostic Page (11h) --- set margin of timestamp
   [Tags]   CONSR-SEST-SPCK-0102-0001   Athena-G2
   Step  1    Validate minimum timestamp value ESMA
   Step  2    Validate maximum timestamp value ESMA
   Step  3    Validate minimum timestamp value ESMB
   Step  4    Validate maximum timestamp value ESMB

CONSR-SEST-SPCK-0103-0001
   [Documentation]   Timestamp Set Diagnostic Page (11h) --- Check timestamp after AC power cycle
   [Tags]   CONSR-SEST-SPCK-0103-0001   Athena-G2

   Step  1    Set maximum timestamp value
   Step  2    AC Power Cycle the Device
   Step  3    Validate default timestamp value in both ESMs

CONSR-SEST-FWDL-0054-0001
   [Documentation]   Upgrade Canister A and B FW - Mode 7
   [Tags]   CONSR-SEST-FWDL-0054-0001   Athena-G2FW
   [Setup]    Download Athena FW image 

   Step  1    Upgrade Canister A PEX0 FW - Mode 7 and check upgrade status
   Step  2    Upgrade Canister A PEX1 FW - Mode 7 and check upgrade status
   Step  3    Upgrade Canister B PEX0 FW - Mode 7 and check upgrade status
   Step  4    Upgrade Canister B PEX1 FW - Mode 7 and check upgrade status
   [Teardown]   Remove Athena FW image 


CONSR-SEST-FWDL-0055-0001
   [Documentation]   Downgrade Canister A and B FW - Mode 7
   [Tags]   CONSR-SEST-FWDL-0055-0001   Athena-G2FW
   [Setup]    Download Athena FW image

   Step  1    Downgrade Canister A PEX0 FW - Mode 7 and check Downgrade status
   Step  2    Downgrade Canister A PEX1 FW - Mode 7 and check Downgrade status
   Step  3    Downgrade Canister B PEX0 FW - Mode 7 and check Downgrade status
   Step  4    Downgrade Canister B PEX1 FW - Mode 7 and check Downgrade status
   [Teardown]   Remove Athena FW image

CONSR-SEST-SPCK-0121-0001
  [Documentation]  This test checks Download Microcode Control/Status Diagnostic Page (0Eh) -  Check log info via CLI
  [Tags]  CONSR-SEST-SPCK-0121-0001  Athena-G2FW
  [Timeout]  10 min 00 seconds
  Step  1  OS Connect Device
  Step  2  Download Microcode -- Check log info via CLI
  Step  3  OS Disconnect Device
  Step  4  ConnectESMB
  Step  5  Download Microcode -- Check log info via CLI
  Step  6  OS Disconnect Device

CONSR-SEST-FWDL-0050-0001
  [Documentation]  This test checks CPLD Firmware Download-Event log check
  [Tags]  CONSR-SEST-FWDL-0050-0001  Athena-G2FW
  [Timeout]  10 min 00 seconds
  Step  1  OS Connect Device
  Step  2  CPLD Firmware Download-Event log check
  Step  3  OS Disconnect Device
  Step  4  ConnectESMB
  Step  5  CPLD Firmware Download-Event log check
  Step  6  OS Disconnect Device

CONSR-SEST-FWDL-0058-0001
  [Documentation]  This test checks SES Download – Write Buffer-Log event check
  [Tags]  CONSR-SEST-FWDL-0058-0001   Athena-G2FW
  [Timeout]  10 min 00 seconds
  Step  1  OS Connect Device
  Step  2  SES Download – Write Buffer log event check
  Step  3  OS Disconnect Device
  Step  4  ConnectESMB
  Step  5  SES Download – Write Buffer log event check
  Step  6  OS Disconnect Device

CONSR-SEST-FWDL-0056-0001
   [Documentation]   Upgrade Canister A and B FW - Mode E + F
   [Tags]   CONSR-SEST-FWDL-0056-0001   Athena-G2FW
   [Setup]    Download Athena FW image

   Step  1    Upgrade Canister A PEX0 FW - Mode E + F and check upgrade status
   Step  2    Upgrade Canister A PEX1 FW - Mode E + F and check upgrade status
   Step  3    Upgrade Canister B PEX0 FW - Mode E + F and check upgrade status
   Step  4    Upgrade Canister B PEX1 FW - Mode E + F and check upgrade status
   [Teardown]   Remove Athena FW image


CONSR-SEST-FWDL-0057-0001
   [Documentation]   Downgrade Canister A and B FW - Mode E + F
   [Tags]   CONSR-SEST-FWDL-0057-0001   Athena-G2FW
   [Setup]    Download Athena FW image

   Step  1    Downgrade Canister A PEX0 FW - Mode E + F and check Downgrade status
   Step  2    Downgrade Canister A PEX1 FW - Mode E + F and check Downgrade status
   Step  3    Downgrade Canister B PEX0 FW - Mode E + F and check Downgrade status
   Step  4    Downgrade Canister B PEX1 FW - Mode E + F and check Downgrade status
   [Teardown]   Remove Athena FW image

CONSR-SEST-SCSI-0008-0001
   [Documentation]   SCSI Support Diagnostic Page - Write Buffer - Download Microcode with offsets, save and activate (mode 07)
   [Tags]   CONSR-SEST-SCSI-0008-0001   Athena-G2FW
   [Setup]    Download Athena FW image

   Step  1    Download Microcode with offsets, save and activate - mode 07 for ESM A
   Step  2    Download Microcode with offsets, save and activate - mode 07 for ESM B

   [Teardown]   Remove Athena FW image

CONSR-SEST-FWDL-0049-0001
  [Documentation]  This test checks CPLD Download microcode Control Diagnostic Page (mode 7)
  [Tags]  CONSR-SEST-FWDL-0049-0001    Athena-G2FW
  [Timeout]  10 min 00 seconds
  [Setup]  Download Athena CPLD image
  Step  1  CPLD Download microcode Control Diagnostic Page - mode 7 and check version in canister A
  Step  2  CPLD Download microcode Control Diagnostic Page - mode 7 and check version in canister B
  [Teardown]  Remove Athena CPLD image

CONSR-SEST-SCSI-0009-0001
  [Documentation]  This test checks SCSI Support Diagnostic Page - Write Buffer - Download Microcode with offsets, save and defer activate (mode 0e)
  [Tags]  CONSR-SEST-SCSI-0009-0001   Athena-G2FW
  [Timeout]  10 min 00 seconds
  [Setup]  Download Athena FW Image
  Step  1  Write Buffer - Download Microcode with offsets, save and defer activate (mode 0e) in canister A0
  Step  2  Write Buffer - Download Microcode with offsets, save and defer activate (mode 0e) in canister B0
  [Teardown]  Remove Athena FW image

CONSRI2C-0001
   [Documentation]  This test checks I2C Bus Check
   [Tags]   CONSRI2C-0001   Athena-G2
   Step  1    OS Connect Device
   Step  2    Verify command validation
   Step  3    OS Disconnect Device
   Step  4    ConnectESMB
   Step  5    Verify command validation
   Step  6    OS Disconnect Device  


CONSR-SEST-SCSI-0010-0001
   [Documentation]  This test checks SCSI Support Diagnostic Page - Write Buffer - Activate deferred microcode (mode 0f)
   [Tags]   CONSR-SEST-SCSI-0010-0001    Athena-G2FW
   [Timeout]  10 min 00 seconds
   Step  1  Write Buffer - Download Microcode with offsets, save and defer activate (mode 0f) in canister A0
   Step  2  Write Buffer - Download Microcode with offsets, save and defer activate (mode 0f) in canister B0

CONSR-SEST-FWDL-0042-0001
  [Documentation]  This test checks Canisters status check during FW update - Upgrade Canister A FW
  [Tags]  CONSR-SEST-FWDL-0042-0001   Athena-G2FW
  [Timeout]  20 min 00 seconds
  [Setup]  Download Athena FW Image
  Step  1  Upgrade Canister A FW - Verify in ESM A
  Step  2  Upgrade Canister A FW - Verify in ESM B
  [Teardown]  Remove Athena FW image

CONSR-SEST-FWDL-0043-0001
  [Documentation]  This test checks Canisters status check during FW update - Upgrade Canister B FW
  [Tags]  CONSR-SEST-FWDL-0043-0001   Athena-G2FW
  [Timeout]  20 min 00 seconds
  [Setup]  Download Athena FW Image
  Step  1  Upgrade Canister A FW - Verify in ESM B
  Step  2  Upgrade Canister A FW - Verify in ESM A
  [Teardown]  Remove Athena FW image

CONSR-SEST-FWDL-0044-0001
  [Documentation]  This test checks PSU Download microcode Control Diagnostic Page (mode E)
  [Tags]  CONSR-SEST-FWDL-0044-0001    Athena-G2FW
  [Setup]  Download Athena PSU image
  Step  1  PSU Download microcode Control Diagnostic Page - mode e
  [Teardown]  Remove Athena PSU image

CONSR-SEST-FWDL-0046-0001
  [Documentation]  This test checks PSU Download microcode Control Diagnostic Page (mode F)
  [Tags]   CONSR-SEST-FWDL-0046-0001      Athena-G2FW
  Step  1  PSU Download microcode Control Diagnostic Page - mode f

CONSR-SEST-FWDL-0045-0001
  [Documentation]  This test checks PSU Download microcode Control Diagnostic Page (Mode 7)
  [Tags]  CONSR-SEST-FWDL-0045-0001    Athena-G2FW
  [Setup]  Download Athena PSU image
  Step  1  PSU Download microcode Control Diagnostic Page - mode 7
  [Teardown]  Remove Athena PSU image

CONSR-SEST-FWDL-0047-0001
  [Documentation]  This test checks Download Event log check
  [Tags]  CONSR-SEST-FWDL-0047-0001    Athena-G2FW
  [Setup]    OS Connect Device
  Step  1  Veify PSU Firmware Download-Event log information
  [Teardown]  OS Disconnect Device

CONSR-SEST-STRS-0008-0001
  [Documentation]   This test checks PSU download Stress Test
  [Tags]  CONSR-SEST-STRS-0008-0001  Athena-G2FW
  [Setup]  Download Athena PSU image
  FOR    ${INDEX}    IN RANGE    ${MAXINDEX}
        Print Loop Info  ${INDEX}
        Step  1  PSU Download microcode Control Diagnostic Page - mode e   True
        Step  2  PSU Download microcode Control Diagnostic Page - mode f   True   False
        Step  3  PSU Download microcode Control Diagnostic Page - mode e   False
        Step  4  PSU Download microcode Control Diagnostic Page - mode f   False  True
        Step  5  PSU Download microcode Control Diagnostic Page - mode 7   
  END
  [Teardown]  Remove Athena PSU image

CTLRS-SYTM-CPU1-0001-0001
  [Documentation]  This test checks Processor-Detection and Reporting
  [Tags]  CTLRS-SYTM-CPU1-0001-0001    Athena-G2
  Step  1    server Connect
  Step  2    verify processors information     ${expected_cpu_model_name_ESMA}  ${expected_BIOS_Model_name_ESMA}
  Step  3    Server Disconnect
  Step  4    server Connect ESMB
  Step  5    verify processors information     ${expected_cpu_model_name_ESMB}  ${expected_BIOS_Model_name_ESMB}
  Step  6    Server Disconnect

CTLRS-SYTM-DMT1-0001-0001
  [Documentation]  This test checks Memory Serial Presence Detect (SPD)
  [Tags]  CTLRS-SYTM-DMT1-0001-0001     Athena-G2
  Step  1    server Connect
  Step  2    verify memory serial presence detect   ${expected_part_number1}    ${expected_part_number2}
  Step  3    Server Disconnect
  Step  4    server Connect ESMB
  Step  5    verify memory serial presence detect   ${expected_part_number1}    ${expected_part_number2}
  Step  6    Server Disconnect

CTLRS-SYTM-DMT1-0009-0001
  [Documentation]  This test checks Capture memory information and Specification Analysis
  [Tags]  CTLRS-SYTM-DMT1-0009-0001     Athena-G2
  Step  1    server Connect
  Step  2    verify memory information   ${expected_memory_info_A}
  Step  3    Server Disconnect
  Step  4    server Connect ESMB
  Step  5    verify memory information   ${expected_memory_info_B}
  Step  6    Server Disconnect

CTLRS-SYTM-USB1-0005-0001
  [Documentation]  This test checks USB function USB Link Speed
  [Tags]  CTLRS-SYTM-USB1-0005-0001     Athena-G2
  Step  1    server Connect
  Step  2    verify USB Link Speeed    ${expected_usb_link_speed}
  Step  3    Server Disconnect
  Step  4    server Connect ESMB
  Step  5    verify USB Link Speeed    ${expected_usb_link_speed}
  Step  6    Server Disconnect

CTLRS-SYTM-USB1-0001-0001
  [Documentation]  This test checks USB detection and enumeration
  [Tags]  CTLRS-SYTM-USB1-0001-0001     Athena-G2
  Step  1    server Connect
  Step  2    verify USB Devices    ${expected_USB_Devices1}    ${expected_USB_Devices2}    ${expected_USB_Devices3}
  Step  3    Server Disconnect
  Step  4    server Connect ESMB
  Step  5    verify USB Devices    ${expected_USB_Devices1}    ${expected_USB_Devices2}    ${expected_USB_Devices3}
  Step  6    Server Disconnect

CTLRS-SYTM-PCIE-0001-001
  [Documentation]  This test checks HIC Card Detection and Number of PCIE Devices
  [Tags]  CTLRS-SYTM-PCIE-0001-001   Athena-G2
  Step  1    server Connect
  Step  2    verify the number of PCIE devices   ${expected_number_PCIE_devices}
  Step  3    Server Disconnect
  Step  5    server Connect ESMB
  Step  6    verify the number of PCIE devices   ${expected_number_PCIE_devices}
  Step  7    Server Disconnect

CTLRS-SYTM-PCIE-0002-0001
  [Documentation]  This test checks PCIE Port HIC Card Link Speed Check
  [Tags]  CTLRS-SYTM-PCIE-0002-0001   Athena-G2
  Step  1    server Connect
  #Step  2    verify HIC card link speed   ${pcie_slotlist_1_A}   ${expected_pcie_speed}    ${expected_width_list1}
  Step  3    verify HIC card link speed   ${pcie_slotlist_2_A}   ${expected_pcie_speed}    ${expected_width_list2}
  Step  4    Server Disconnect
  Step  5    server Connect ESMB
  Step  6    verify HIC card link speed   ${pcie_slotlist_1_B}   ${expected_pcie_speed}    ${expected_width_list1}
  Step  7    verify HIC card link speed   ${pcie_slotlist_2_B}   ${expected_pcie_speed}    ${expected_width_list2}
  Step  8    Server Disconnect

CTLRS-SYTM-PCIE-0004-0001
  [Documentation]  This test checks IRQ and slot address fix
  [Tags]  CTLRS-SYTM-PCIE-0004-0001   Athena-G2
  Step  1    server Connect
  Step  2    verify PCIE device id information   ${PCIE_device_id}   ${PCIE_device_info}
  Step  3    Server Disconnect

CTLRS-SYTM-LANT-0003-0001
  [Documentation]  This test checks LAN Speed Auto-negotiation
  [Tags]  CTLRS-SYTM-LANT-0003-0001   Athena-G2
  Step  1    server Connect
  Step  2    verifyLAN_Speed_Auto_negotiation   ${expected_auto_neg_support}
  Step  3    Server Disconnect

CTLRS-SYTM-BMCS-0001-0001
  [Documentation]  This test checks BMC sub-system Sensor reading test
  [Tags]  CTLRS-SYTM-BMCS-0001-0001   Athena-G2
  Step  1    server Connect
  Step  2    verify BMC sub system sensor reading
  Step  3    Server Disconnect
  Step  4    server Connect ESMB
  Step  5    verify BMC sub system sensor reading
  Step  6    Server Disconnect

CTLRS-SYTM-UUID-0001-0001
  [Documentation]  This test checks UUID check
  [Tags]  CTLRS-SYTM-UUID-0001-0001   Athena-G2
  Step  1    server Connect
  Step  2    verify UUID_serialnumber    ${serial_number}
  Step  3    Server Disconnect
  Step  4    server Connect ESMB
  Step  5    verify UUID_serialnumber    ${serial_number}
  Step  6    Server Disconnect

CTLRS-SYTM-BMCS-0003-0001
  [Documentation]  This test checks BMC sub-system BMC time check
  [Tags]  CTLRS-SYTM-BMCS-0003-0001   Athena-G2
  Step  1  server Connect
  Step  2  BMC time check
  Step  3  Server Disconnect
  Step  4  server Connect ESMB
  Step  5  BMC time check
  Step  6  Server Disconnect

CTLRS-SYTM-STOR-0004-0001
  [Documentation]  This test checks  Drive temperature get
  [Tags]  CTLRS-SYTM-ST0R-0004-0001   Athena-G2
  Step  1  server Connect
  Step  2  verifyDisk_Temperature
  Step  3  Server Disconnect
  Step  4  server Connect ESMB
  Step  5  verifyDisk_Temperature
  Step  6  Server Disconnect

CTLRS-SYTM-STAB-0022-0001
  [Documentation]  This test checks BMC Power Reset Test
  [Tags]  CTLRS-SYTM-STAB-0022-0001   Athena-G2
  Step  1    verify BMC Power Reset on both ESMs

CTLRS-SYTM-BMCS-0002-0001
  [Documentation]  This test checks SDR get stress
  [Tags]  CTLRS-SYTM-BMCS-0002-0001   Athena-G2
  FOR    ${INDEX}    IN RANGE    ${MAXINDEX}
        Print Loop Info  ${INDEX}
	Step  1  server Connect
	Step  2  verify Sensor Status via ipmitool
	Step  3  Server Disconnect
        Step  4  server Connect ESMB
        Step  5  verify Sensor Status via ipmitool
        Step  6  Server Disconnect
  END

CTLRS-SYTM-STAB-0023-0001
  [Documentation]  This test checks BMC Self reset Test
  [Tags]  CTLRS-SYTM-STAB-0023-0001    Athena-G2
  Step  1  server Connect
  Step  2  verify mc_info before and after warm reset
  Step  3  Server Disconnect
  Step  4  server Connect ESMB
  Step  5  verify mc_info before and after warm reset
  Step  6  Server Disconnect

CTLRS-SYTM-STOR-0007-0001
  [Documentation]  This test checks Storage function SES reset test
  [Tags]  CTLRS-SYTM-ST0R-0007-0001  Athena-G2
  Step  1  verify drive count after ses reset ESMA
  Step  2  verify drive count after ses reset ESMB

CTLRS-SYTM-I2CT-0003-0001
  [Documentation]  This test checks Global I2C Stress Test
  [Tags]  CTLRS-SYTM-I2CT-0003-0001   Athena-G2FW
  FOR    ${INDEX}    IN RANGE    ${MAXINDEX}
        Print Loop Info  ${INDEX}
        Step  1  OS Connect Device
        Step  2  whitebox_lib.run_ipmi_cmd_sel_clear  DUT
        Step  4  verify i2c read and write cli commands
        Step  6  whitebox_lib.verify_cmd_output_message  DUT  ipmitool sel list  ${error_messages_sell_list}
        Step  7  OS Disconnect Device
        Step  8  ConnectESMB
        Step  9  whitebox_lib.run_ipmi_cmd_sel_clear  DUT
        Step  11  verify i2c read and write cli commands
        Step  13  whitebox_lib.verify_cmd_output_message  DUT  ipmitool sel list  ${error_messages_sell_list}
        Step  14  OS Disconnect Device
  END

CTLRS-SYTM-FWPG-0011-0001
  [Documentation]  This test checks Firmware cross version update test
  [Tags]  CTLRS-SYTM-FWPG-0011-0001   Athena-G2FW
  Step  1  Prepare images for BMC BIOS SES CPLD
  Step  2  Upgrade and downgrade FW

CTLRS-SYTM-POWE-0003-0001
  [Documentation]  This test checks PSU Redundant stress test
  [Tags]  CTLRS-SYTM-POWE-0003-0001  Athena-G2
  FOR    ${INDEX}    IN RANGE    ${MAXINDEX}
        Print Loop Info  ${INDEX}
        Step  1  check PSU Redundant available
	Step  2  verify the number of drives and pcie devices on ESM-A
	Step  3  verify the number of drives and pcie devices on ESM-B 
  END

CONSR-SEST-IVMT-0029-0001
   [Documentation]  This test does VPD Function Check
   [Tags]   CONSR-SEST-IVMT-0029-0001   Athena-G2
   [Timeout]  5 min 00 seconds

   Step  1    OS Connect Device
   Step  2    VPD Function Check
   Step  3    OS Disconnect Device
   Step  4    ConnectESMB
   Step  5    VPD Function Check
   Step  6    OS Disconnect Device

CONSR-RESET-0001
   [Documentation]  This test checks Reset Function Test
   [Tags]   CONSR-RESET-0001   Athena-G2
   [Timeout]  50 min 00 seconds
   Step  1    OS Connect Device
   Step  2    CLI Reset Validation
   Step  3    OS Disconnect Device
   Step  4    SES Reset Validation Canister A  ${ses_reset_cmd1}  ${ses_reset_cmd2}
   Step  5    ConnectESMB
   Step  6    CLI Reset Validation
   Step  7    OS Disconnect Device
   Step  8    SES Reset Validation Canister B  ${ses_reset_cmd2}  ${ses_reset_cmd1}

TestDebug
   [Documentation]  This test checks Reset Function Test
   [Tags]   TestDebug   Athena-G2
   [Timeout]  50 min 00 seconds
   Step  1    OS Connect Device
   Step  2    OS Disconnect Device
   Step  3    ConnectESMB
   Step  4    OS Disconnect Device
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
