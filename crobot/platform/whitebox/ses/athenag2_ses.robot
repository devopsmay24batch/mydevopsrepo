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
    [Setup]    get dut variables
    Sub-Case  create-gold-file_1  Create ses page gold file
    Sub-Case  create-gold-file_1  Create ses page gold file ESMB
    Sub-Case  create-gold-file_1  Compare ses page gold file
    Sub-Case  create-gold-file_1  Compare ses page gold file ESMB

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

CONSR-SEST-SCSI-0020-0001
  [Documentation]  This test checks SCSI Support page-Report LUNs
  [Tags]   CONSR-SEST-SCSI-0020-0001   Athena-G2
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

CONSR-SEST-SPCK-0023-0001
   [Documentation]  This test checks enclosure status diagnostics
   [Tags]   CONSR-SEST-SPCK-0023-0001   Athena-G2
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
   [Tags]   CONSR-SEST-FWDL-0054-0001   Athena-G2
   [Setup]    Download Athena FW image 

   Step  1    Upgrade Canister A PEX0 FW - Mode 7 and check upgrade status
   Step  2    Upgrade Canister A PEX1 FW - Mode 7 and check upgrade status
   Step  3    Upgrade Canister B PEX0 FW - Mode 7 and check upgrade status
   Step  4    Upgrade Canister B PEX1 FW - Mode 7 and check upgrade status
   [Teardown]   Remove Athena FW image 


CONSR-SEST-FWDL-0055-0001
   [Documentation]   Downgrade Canister A and B FW - Mode 7
   [Tags]   CONSR-SEST-FWDL-0055-0001   Athena-G2
   [Setup]    Download Athena FW image

   Step  1    Downgrade Canister A PEX0 FW - Mode 7 and check Downgrade status
   Step  2    Downgrade Canister A PEX1 FW - Mode 7 and check Downgrade status
   Step  3    Downgrade Canister B PEX0 FW - Mode 7 and check Downgrade status
   Step  4    Downgrade Canister B PEX1 FW - Mode 7 and check Downgrade status
   [Teardown]   Remove Athena FW image

CONSR-SEST-SPCK-0121-0001
  [Documentation]  This test checks Download Microcode Control/Status Diagnostic Page (0Eh) -  Check log info via CLI
  [Tags]  CONSR-SEST-SPCK-0121-0001  Athena-G2
  [Timeout]  10 min 00 seconds
  Step  1  OS Connect Device
  Step  2  Download Microcode -- Check log info via CLI
  Step  3  OS Disconnect Device
  Step  4  ConnectESMB
  Step  5  Download Microcode -- Check log info via CLI
  Step  6  OS Disconnect Device

CONSR-SEST-FWDL-0050-0001
  [Documentation]  This test checks CPLD Firmware Download-Event log check
  [Tags]  CONSR-SEST-FWDL-0050-0001  Athena-G2
  [Timeout]  10 min 00 seconds
  Step  1  OS Connect Device
  Step  2  CPLD Firmware Download-Event log check
  Step  3  OS Disconnect Device
  Step  4  ConnectESMB
  Step  5  CPLD Firmware Download-Event log check
  Step  6  OS Disconnect Device

CONSR-SEST-FWDL-0058-0001
  [Documentation]  This test checks SES Download – Write Buffer-Log event check
  [Tags]  CONSR-SEST-FWDL-0058-0001   Athena-G2
  [Timeout]  10 min 00 seconds
  Step  1  OS Connect Device
  Step  2  SES Download – Write Buffer log event check
  Step  3  OS Disconnect Device
  Step  4  ConnectESMB
  Step  5  SES Download – Write Buffer log event check
  Step  6  OS Disconnect Device

CONSR-SEST-FWDL-0056-0001
   [Documentation]   Upgrade Canister A and B FW - Mode E + F
   [Tags]   CONSR-SEST-FWDL-0056-0001   Athena-G2
   [Setup]    Download Athena FW image

   Step  1    Upgrade Canister A PEX0 FW - Mode E + F and check upgrade status
   Step  2    Upgrade Canister A PEX1 FW - Mode E + F and check upgrade status
   Step  3    Upgrade Canister B PEX0 FW - Mode E + F and check upgrade status
   Step  4    Upgrade Canister B PEX1 FW - Mode E + F and check upgrade status
   [Teardown]   Remove Athena FW image


CONSR-SEST-FWDL-0057-0001
   [Documentation]   Downgrade Canister A and B FW - Mode E + F
   [Tags]   CONSR-SEST-FWDL-0057-0001   Athena-G2
   [Setup]    Download Athena FW image

   Step  1    Downgrade Canister A PEX0 FW - Mode E + F and check Downgrade status
   Step  2    Downgrade Canister A PEX1 FW - Mode E + F and check Downgrade status
   Step  3    Downgrade Canister B PEX0 FW - Mode E + F and check Downgrade status
   Step  4    Downgrade Canister B PEX1 FW - Mode E + F and check Downgrade status
   [Teardown]   Remove Athena FW image

CONSR-SEST-SCSI-0008-0001
   [Documentation]   SCSI Support Diagnostic Page - Write Buffer - Download Microcode with offsets, save and activate (mode 07)
   [Tags]   CONSR-SEST-SCSI-0008-0001   Athena-G2
   [Setup]    Download Athena FW image

   Step  1    Download Microcode with offsets, save and activate - mode 07 for ESM A
   Step  2    Download Microcode with offsets, save and activate - mode 07 for ESM B

   [Teardown]   Remove Athena FW image

CONSR-SEST-FWDL-0049-0001
  [Documentation]  This test checks CPLD Download microcode Control Diagnostic Page (mode 7)
  [Tags]  CONSR-SEST-FWDL-0049-0001    Athena-G2
  [Timeout]  10 min 00 seconds
  [Setup]  Download Athena CPLD image
  Step  1  CPLD Download microcode Control Diagnostic Page - mode 7 and check version in canister A
  Step  2  CPLD Download microcode Control Diagnostic Page - mode 7 and check version in canister B
  [Teardown]  Remove Athena CPLD image

CONSR-SEST-SCSI-0009-0001
  [Documentation]  This test checks SCSI Support Diagnostic Page - Write Buffer - Download Microcode with offsets, save and defer activate (mode 0e)
  [Tags]  CONSR-SEST-SCSI-0009-0001   Athena-G2
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
   [Tags]   CONSR-SEST-SCSI-0010-0001    Athena-G2
   [Timeout]  10 min 00 seconds
   Step  1  Write Buffer - Download Microcode with offsets, save and defer activate (mode 0f) in canister A0
   Step  2  Write Buffer - Download Microcode with offsets, save and defer activate (mode 0f) in canister B0

CONSR-SEST-FWDL-0042-0001
  [Documentation]  This test checks Canisters status check during FW update - Upgrade Canister A FW
  [Tags]  CONSR-SEST-FWDL-0042-0001   Athena-G2
  [Timeout]  20 min 00 seconds
  [Setup]  Download Athena FW Image
  Step  1  Upgrade Canister A FW - Verify in ESM A
  Step  2  Upgrade Canister A FW - Verify in ESM B
  [Teardown]  Remove Athena FW image

CONSR-SEST-FWDL-0043-0001
  [Documentation]  This test checks Canisters status check during FW update - Upgrade Canister B FW
  [Tags]  CONSR-SEST-FWDL-0043-0001   Athena-G2
  [Timeout]  20 min 00 seconds
  [Setup]  Download Athena FW Image
  Step  1  Upgrade Canister A FW - Verify in ESM B
  Step  2  Upgrade Canister A FW - Verify in ESM A
  [Teardown]  Remove Athena FW image

CONSR-SEST-FWDL-0044-0001
  [Documentation]  This test checks PSU Download microcode Control Diagnostic Page (mode E)
  [Tags]  CONSR-SEST-FWDL-0044-0001    Athena-G2
  [Setup]  Download Athena PSU image
  Step  1  PSU Download microcode Control Diagnostic Page - mode e
  [Teardown]  Remove Athena PSU image

CONSR-SEST-FWDL-0046-0001
  [Documentation]  This test checks PSU Download microcode Control Diagnostic Page (mode F)
  [Tags]   CONSR-SEST-FWDL-0046-0001      Athena-G2
  Step  1  PSU Download microcode Control Diagnostic Page - mode f

CONSR-SEST-FWDL-0045-0001
  [Documentation]  This test checks PSU Download microcode Control Diagnostic Page (Mode 7)
  [Tags]  CONSR-SEST-FWDL-0045-0001    Athena-G2
  [Setup]  Download Athena PSU image
  Step  1  PSU Download microcode Control Diagnostic Page - mode 7
  [Teardown]  Remove Athena PSU image

CONSR-SEST-FWDL-0047-0001
  [Documentation]  This test checks Download Event log check
  [Tags]  CONSR-SEST-FWDL-0047-0001    Athena-G2
  [Setup]    OS Connect Device
  Step  1  Veify PSU Firmware Download-Event log information
  [Teardown]  OS Disconnect Device

CONSR-SEST-STRS-0008-0001
  [Documentation]   This test checks PSU download Stress Test
  [Tags]  CONSR-SEST-STRS-0008-0001  Athena-G2
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
  [Tags]  CTLRS-SYTM-I2CT-0003-0001   Athena-G2
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
  [Tags]  CTLRS-SYTM-FWPG-0011-0001   Athena-G2
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

CONSR-SEST-SCSI-0001-0001
    [Documentation]  Test Unit Ready
    [Tags]     CONSR-SEST-SCSI-0001-0001   Athena-G2
    [Timeout]  5 min 00 seconds
    Step  1  server Connect
    Step  2  check SCISI Elements Athena  ${check_scsi_ready_cmd}  ${scsi_ready_pattern}
    Step  3  Server Disconnect
    Step  4  server Connect ESMB
    Step  5  check SCISI Elements Athena  ${check_scsi_ready_cmd}  ${scsi_ready_pattern}
    Step  6  Server Disconnect

CONSR-SEST-SCSI-0002-0001
    [Documentation]  check Enclosure Length
    [Tags]     CONSR-SEST-SCSI-0002-0001    Athena-G2
    [Timeout]  5 min 00 seconds
    Step  1  server Connect
    Step  2  check Enclosure Length Athena  ${sg_inquiry_cmd}  ${sq_inquiry_pattern_Athena}  ${sq_inquiry_length_Athena}
    Step  3  Server Disconnect
    Step  4  server Connect ESMB
    Step  5  check Enclosure Length Athena  ${sg_inquiry_cmd}  ${sq_inquiry_pattern_Athena}  ${sq_inquiry_length_Athena}
    Step  6  Server Disconnect

CONSR-SEST-SCSI-0003-0001
    [Documentation]  SES Support Diagnostic Page - VPD 00h(Supported VPD)
    [Tags]     CONSR-SEST-SCSI-0003-0001    Athena-G2
    [Timeout]  5 min 00 seconds
    Step  1  server Connect
    Step  2  check SCISI Elements Athena  ${sg_inquiry_page_0x00_cmd}  ${sg_inquiry_page_0x00_pattern}
    Step  3  Server Disconnect
    Step  4  server Connect ESMB
    Step  5  check SCISI Elements Athena  ${sg_inquiry_page_0x00_cmd}  ${sg_inquiry_page_0x00_pattern}
    Step  6  Server Disconnect

CONSR-SEST-SCSI-0004-0001
    [Documentation]  SES Support Diagnostic Page - VPD 80h(Unit Serial Number)
    [Tags]     CONSR-SEST-SCSI-0004-0001    Athena-G2
    [Timeout]  5 min 00 seconds
    Step  1  server Connect
    Step  2  check Enclosure Length Athena  ${sg_inquiry_page_0x80_cmd}  ${sq_inquiry_pattern_VPD_80_Athena}  ${sq_inquiry_length_VPD_80_Athena}
    Step  3  Server Disconnect
    Step  4  server Connect ESMB
    Step  5  check Enclosure Length Athena  ${sg_inquiry_page_0x80_cmd}  ${sq_inquiry_pattern_VPD_80_Athena}  ${sq_inquiry_length_VPD_80_Athena}
    Step  6  Server Disconnect

CONSR-SEST-SCSI-0005-0001
    [Documentation]  SES Support Diagnostic Page - VPD 83h(Device Identication)
    [Tags]     CONSR-SEST-SCSI-0005-0001   Athena-G2
    [Timeout]  5 min 00 seconds
    Step  1  server Connect
    Step  2  check SCISI Elements Athena  ${sg_inquiry_page_0x83_cmd}  ${sg_inquiry_page_0x83_pattern_Athena}
    Step  3  Server Disconnect
    Step  4  server Connect ESMB
    Step  5  check SCISI Elements Athena  ${sg_inquiry_page_0x83_cmd}  ${sg_inquiry_page_0x83_pattern_Athena}
    Step  6  Server Disconnect

CONSR-SEST-SCSI-0006-0001
    [Documentation]  SES Support Diagnostic Page
    [Tags]     CONSR-SEST-SCSI-0006-0001      Athena-G2
    [Timeout]  5 min 00 seconds
    Step  1  server Connect
    Step  2  check Command Sent Athena  sg_ses  ${fail_dict}
    Step  3  Server Disconnect
    Step  4  server Connect ESMB
    Step  5  check Command Sent Athena  sg_ses  ${fail_dict}
    Step  6  Server Disconnect

CONSR-SEST-SPCK-0061-0001
    [Documentation]  This test case checks Log Status Diagnostic Page (13h) - page status
    [Tags]     CONSR-SEST-SPCK-0061-0001    Athena-G2
    [Timeout]  5 min 00 seconds
    Step  1  server Connect
    Step  2  send a command Athena  ${Page13_run_diag_command}
    Step  3  verify Page Status Athena   ${page_13_status_cmd}
    Step  4  Server Disconnect
    Step  5  server Connect ESMB
    Step  6  send a command Athena  ${Page13_run_diag_command}
    Step  7  verify Page Status Athena   ${page_13_status_cmd}
    Step  8  Server Disconnect

CONSR-SEST-SPCK-0038-0001
    [Documentation]  Threshold Out Diagnostic Pages(05h) - Temp LC
    [Tags]     CONSR-SEST-SPCK-0038-0001   Athena-G2
    [Timeout]  5 min 00 seconds
    Step  1  server Connect
    Step  2  check Temperature Alarm On Page5 Athena  low critical
    Step  3  restore Temperature Threshold on Page5  low critical
    Step  4  Server Disconnect
    Step  5  server Connect ESMB
    Step  6  check Temperature Alarm On Page5 Athena  low critical
    Step  7  restore Temperature Threshold on Page5  low critical
    Step  8  Server Disconnect

CONSR-SEST-SPCK-0039-0001
    [Documentation]  Threshold Out Diagnostic Pages(05h) - Temp LW
    [Tags]     CONSR-SEST-SPCK-0039-0001   Athena-G2
    [Timeout]  5 min 00 seconds
    Step  1  server Connect
    Step  2  check Temperature Alarm On Page5 Athena  low warning
    Step  3  restore Temperature Threshold on Page5  low warning
    Step  4  Server Disconnect
    Step  5  server Connect ESMB
    Step  6  check Temperature Alarm On Page5 Athena  low warning
    Step  7  restore Temperature Threshold on Page5  low warning
    Step  8  Server Disconnect

CONSR-SEST-SPCK-0040-0001
    [Documentation]  Threshold Out Diagnostic Pages(05h) - Temp UC
    [Tags]     CONSR-SEST-SPCK-0040-0001   Athena-G2
    [Timeout]  5 min 00 seconds
    Step  1  server Connect
    Step  2  check Temperature Alarm On Page5 Athena  high critical
    Step  3  restore Temperature Threshold on Page5   high critical
    Step  4  Server Disconnect
    Step  5  server Connect ESMB
    Step  6  check Temperature Alarm On Page5 Athena  high critical
    Step  7  restore Temperature Threshold on Page5  high critical
    Step  8  Server Disconnect

CONSR-SEST-SPCK-0041-0001
    [Documentation]  Threshold Out Diagnostic Pages(05h) - Temp UW
    [Tags]     CONSR-SEST-SPCK-0041-0001    Athena-G2
    [Timeout]  5 min 00 seconds
    Step  1  server Connect
    Step  2  check Temperature Alarm On Page5 Athena  high warning
    Step  3  restore Temperature Threshold on Page5   high warning
    Step  4  Server Disconnect
    Step  5  server Connect ESMB
    Step  6  check Temperature Alarm On Page5 Athena  high warning
    Step  7  restore Temperature Threshold on Page5  high warning
    Step  8  Server Disconnect

CONSR-SEST-SPCK-0008-0001
    [Documentation]  Check 'non-crit' bit with sensors under UW condition - Enclosure Control Diagnostic Pages(02h)
    [Tags]     CONSR-SEST-SPCK-0008-0001   Athena-G2
    [Timeout]  5 min 00 seconds
    Step  1  server Connect
    Step  2  Run Keyword And Continue On Failure  check Temperature Alarm Athena  high warning
    Step  3  restore Temperature Threshold  high warning
    Step  4  Server Disconnect
    Step  5  server Connect ESMB
    Step  6  Run Keyword And Continue On Failure  check Temperature Alarm Athena   high warning
    Step  7  restore Temperature Threshold  high warning
    Step  8  Server Disconnect
    [Teardown]  Server Disconnect

CONSR-SEST-SPCK-0009-0001
    [Documentation]  Check 'non-crit' bit with sensors under LW condition - Enclosure Control Diagnostic Pages(02h)
    [Tags]     CONSR-SEST-SPCK-0009-0001   Athena-G2
    [Timeout]  5 min 00 seconds
    Step  1  server Connect
    Step  2  Run Keyword And Continue On Failure  check Temperature Alarm Athena  low warning
    Step  3  restore Temperature Threshold  low warning
    Step  4  Server Disconnect
    Step  5  server Connect ESMB
    Step  6  Run Keyword And Continue On Failure  check Temperature Alarm Athena  low warning
    Step  7  restore Temperature Threshold  low warning
    Step  8  Server Disconnect

CONSR-SEST-IVMT-0020-0001
    [Documentation]  This test checks the array device disk Inventory - page 07h
    [Tags]   CONSR-SEST-IVMT-0020-0001   Athena-G2    cm
    [Timeout]  5 min 00 seconds
    Step  1   server Connect
    Step  2   check slot name format Athena  ${page7_slotname_check_cmd}
    Step  3   Server Disconnect
    Step  4   server Connect ESMB
    Step  5   check slot name format Athena  ${page7_slotname_check_cmd}
    Step  6   Server Disconnect

CONSR-SEST-SPCK-0018-0001
    [Documentation]  This test checks  Enclosure Control Diagnostic Pages(02h) - Cooling external Mode
    [Tags]     CONSR-SEST-SPCK-0018-0001  Athena-G2    cm
    [Timeout]  5 min 00 seconds
    [Setup]    get dut variables
    Sub-Case  CONSR-SEST-SPCK-0018-0001_1  check esm mode status Athena
    Sub-Case  CONSR-SEST-SPCK-0018-0001_2  check Cooling external Mode ESMA Athena
    Sub-Case  CONSR-SEST-SPCK-0018-0001_3  check esm mode status ESMB Athena
    Sub-Case  CONSR-SEST-SPCK-0018-0001_4  check Cooling external Mode ESMB Athena

CONSR-SEST-SPCK-0019-0001
    [Documentation]  This test checks  Enclosure Control Diagnostic Pages(02h) - Cooling internal Mode
    [Tags]     CONSR-SEST-SPCK-0019-0001  Athena-G2   
    [Timeout]  5 min 00 seconds
    [Setup]    get dut variables
    Sub-Case  CONSR-SEST-SPCK-0019-0001_1  check esm mode status Athena
    Sub-Case  CONSR-SEST-SPCK-0019-0001_2  check Cooling internal Mode ESMA Athena
    Sub-Case  CONSR-SEST-SPCK-0019-0001_3  check esm mode status ESMB Athena
    Sub-Case  CONSR-SEST-SPCK-0019-0001_4  check Cooling internal Mode ESMB Athena

CONSR-SEST-IVMT-0014-0001
    [Documentation]  This test case checks PSU 0 Inventory - page 07h
    [Tags]     CONSR-SEST-IVMT-0014-0001  Athena-G2    cm
    [Timeout]  5 min 00 seconds
    Step  1    compare PSU status with CLI ESMA Athena  ${psu0_status_pg7_cmd}   ${psu0_cli_pattern_Athena}
    Step  2    compare PSU status with CLI ESMB Athena  ${psu0_status_pg7_cmd}   ${psu0_cli_pattern_Athena}

CONSR-SEST-IVMT-0015-0001
    [Documentation]  This test case checks PSU 1 Inventory - page 07h
    [Tags]     CONSR-SEST-IVMT-0015-0001  Athena-G2   cm
    [Timeout]  5 min 00 seconds
    Step  1    compare PSU status with CLI ESMA Athena  ${psu1_status_pg7_cmd}   ${psu1_cli_pattern_Athena}
    Step  2    compare PSU status with CLI ESMB Athena  ${psu1_status_pg7_cmd}   ${psu1_cli_pattern_Athena}

CONSR-SEST-SPCK-0003-0001
    [Documentation]  This test checks  Enclosure Status Diagnostic Pages(02h)
    [Tags]     CONSR-SEST-SPCK-0003-0001  Athena-G2    cm
    [Timeout]  5 min 00 seconds
    [Setup]    get dut variables
    Sub-Case  CONSR-SEST-SPCK-0003-0001_1  check esm mode status Athena
    Sub-Case  CONSR-SEST-SPCK-0003-0001_2  Enclosure Status Diagnostic Pages(02h) Athena ESMA
    Sub-Case  CONSR-SEST-SPCK-0003-0001_3  check esm mode status ESMB Athena
    Sub-Case  CONSR-SEST-SPCK-0003-0001_4  Enclosure Status Diagnostic Pages(02h) Athena ESMB

CONSR-SEST-SPCK-0058-0001
    [Documentation]  This test case checks Log Control Diagnostic Page (13h) - get log info
    [Tags]     CONSR-SEST-SPCK-0058-0001  Athena-G2   cm
    [Timeout]  5 min 00 seconds
    Step  1    server Connect
    Step  2    send a command Athena   ${page13_readlog_cmd}
    Step  3    compare log info with CLI Athena ESMA   ${page_13_status_cmd}
    Step  4    Server Disconnect
    Step  5    server Connect ESMB
    Step  6    send a command Athena   ${page13_readlog_cmd}
    Step  7    compare log info with CLI Athena ESMB   ${page_13_status_cmd}
    Step  8    Server Disconnect

CONSRS-PO-01-0001
    [Documentation]  This test checks Drive Disk Power On/Off Check with SES Page.
    [Tags]     CONSRS-PO-01-0001   Athena-G2
    [Timeout]  8 min 00 seconds
    [Setup]    server Connect
    Step  1    verify Drive Disk Power Athena
    [Teardown]  Server Disconnect

CONSR-SEST-CLMT-0002-0001
    [Documentation]  This test checks SES Enclosure Control Page Cooling element- lowest fan speed
    [Tags]   CONSR-SEST-CLMT-0002-0001   Athena-G2
    [Timeout]  5 min 00 seconds
    [Setup]    get dut variables
    Step  1    check fan speed Athena    ${fan_min_speed}   ${fan_min_speed_athena}
    [Teardown]  Run Keywords  Server Disconnect
           ...  AND Disconnect

CONSR-SEST-CLMT-0003-0001
    [Documentation]  This test checks SES Enclosure Control Page Cooling element- highest speed
    [Tags]   CONSR-SEST-CLMT-0003-0001   Athena-G2
    [Timeout]  5 min 00 seconds
    [Setup]    get dut variables
    Step  1    check fan speed Athena    ${fan_max_speed}   ${fan_max_speed_athena}
    #Restore the fan speed to minimum 
    Step  2    check fan speed Athena    ${fan_min_speed}   ${fan_min_speed_athena}
    [Teardown]  Run Keywords  Server Disconnect
           ...  AND Disconnect

CONSR-SEST-FWDL-0029-0001
    [Documentation]  SES Download microcode Control Diagnostic Page
                ...  - with wrong image file under mode 0xe
    [Tags]     CONSR-SEST-FWDL-0029-0001  Athena-G2
    [Timeout]  10 min 00 seconds
    Step  1   Download Athena FW FAULT image
    Step  2   Verify With FW Fault Image Under Mode E Athena ESMA
    Step  3   Verify With FW Fault Image Under Mode E Athena ESMB

CONSR-SEST-FWDL-0034-0001
    [Documentation]  This test checks upgrade cpld via SES Page - mode 0xe and 0xf
    [Tags]     CONSR-SEST-FWDL-0034-0001    Athena-G2
    [Timeout]  30 min 00 seconds
    [Setup]    get dut variables
    Sub-Case  CONSR-SEST-FWDL-0034-0001_1  check esm mode status Athena
    Sub-Case  CONSR-SEST-FWDL-0034-0001_2  check esm mode status ESMB Athena
    Sub-Case  CONSR-SEST-FWDL-0034-0001_3  Download Athena CPLD image
    Sub-Case  CONSR-SEST-FWDL-0034-0001_4  upgrade cpld with mode 0xe + mode 0xf Athena ESMA
    Sub-Case  CONSR-SEST-FWDL-0034-0001_4  upgrade cpld with mode 0xe + mode 0xf Athena ESMB
    Sub-Case  CONSR-SEST-FWDL-0034-0001_5  check esm mode status Athena
    Sub-Case  CONSR-SEST-FWDL-0034-0001_6  check esm mode status ESMB Athena
    Sub-Case  CONSR-SEST-FWDL-0034-0001_7  Remove Athena CPLD image
    [Teardown]  Run Keywords  Server Disconnect
           ...  AND Disconnect

CONSR-SEST-SPCK-0042-0001
    [Documentation]  Threshold Out Diagnostic Pages(05h) - Voltage LC
    [Tags]     CONSR-SEST-SPCK-0042-0001    Athena-G2
    [Timeout]  5 min 00 seconds
    Step  1  server Connect
    Step  2  check Sensor Alarm On Page5 Athena  low critical  Voltage sensor
    Step  3  restore Threshold on Page5  low critical  Voltage sensor
    Step  4  Server Disconnect
    Step  5  server Connect ESMB
    Step  6  check Sensor Alarm On Page5 Athena  low critical  Voltage sensor
    Step  7  restore Threshold on Page5  low critical  Voltage sensor
    Step  8  Server Disconnect

CONSR-SEST-SPCK-0043-0001
    [Documentation]  Threshold Out Diagnostic Pages(05h) - Voltage LW
    [Tags]     CONSR-SEST-SPCK-0043-0001    Athena-G2
    [Timeout]  5 min 00 seconds
    Step  1  server Connect
    Step  2  check Sensor Alarm On Page5 Athena  low warning  Voltage sensor
    Step  3  restore Threshold on Page5  low warning  Voltage sensor
    Step  4  Server Disconnect
    Step  5  server Connect ESMB
    Step  6  check Sensor Alarm On Page5 Athena  low warning  Voltage sensor
    Step  7  restore Threshold on Page5  low warning  Voltage sensor
    Step  8  Server Disconnect

CONSR-SEST-SPCK-0044-0001
    [Documentation]  Threshold Out Diagnostic Pages(05h) - Voltage UC
    [Tags]     CONSR-SEST-SPCK-0044-0001    Athena-G2
    [Timeout]  5 min 00 seconds
    Step  1  server Connect
    Step  2  check Sensor Alarm On Page5 Athena  high critical  Voltage sensor
    Step  3  restore Threshold on Page5  high critical  Voltage sensor
    Step  4  Server Disconnect
    Step  5  server Connect ESMB
    Step  6  check Sensor Alarm On Page5 Athena  high critical  Voltage sensor
    Step  7  restore Threshold on Page5  high critical  Voltage sensor
    Step  8  Server Disconnect

CONSR-SEST-SPCK-0045-0001
    [Documentation]  Threshold Out Diagnostic Pages(05h) - Voltage UW
    [Tags]     CONSR-SEST-SPCK-0045-0001     Athena-G2
    [Timeout]  5 min 00 seconds
    Step  1  server Connect
    Step  2  check Sensor Alarm On Page5 Athena  high warning  Voltage sensor
    Step  3  restore Threshold on Page5  high warning  Voltage sensor
    Step  4  Server Disconnect
    Step  5  server Connect ESMB
    Step  6  check Sensor Alarm On Page5 Athena  high warning  Voltage sensor
    Step  7  restore Threshold on Page5  high warning  Voltage sensor
    Step  8  Server Disconnect

CONSR-SEST-IVMT-0007-0001
    [Documentation]  This test checks enclosure status - page 02h
    [Tags]   CONSR-SEST-IVMT-0007-0001          Athena-G2
    [Timeout]  8 min 00 seconds
    Step  1    server Connect
    Step  2    check Command Pattern Athena   ${pg2_enc_status_cmd}  ${Athena_pg2_enc_status}
    Step  3    Server Disconnect
    Step  4    server Connect ESMB
    Step  5    check Command Pattern Athena   ${pg2_enc_status_cmd}  ${Athena_pg2_enc_status}
    Step  6    Server Disconnect

CONSR-SEST-SPCK-0007-0001
    [Documentation]  Check \'crit\' bit with sensors under LC condition - Enclosure Control Diagnostic Pages(02h)
    [Tags]     CONSR-SEST-SPCK-0007-0001   Athena-G2
    [Timeout]  5 min 00 seconds
    Step  1  server Connect
    Step  2  Run Keyword And Continue On Failure  check Temperature Alarm Athena  low critical
    Step  3  restore Temperature Threshold  low critical
    Step  4  Server Disconnect
    Step  5  server Connect ESMB
    Step  6  Run Keyword And Continue On Failure  check Temperature Alarm Athena  low critical
    Step  7  restore Temperature Threshold  low critical
    Step  8  Server Disconnect

CONSR-SEST-IVMT-0008-0001
    [Documentation]  This test checks the enclosure Inventory - page 07h
    [Tags]   CONSR-SEST-IVMT-0008-0001    Athena-G2
    [Timeout]  5 min 00 seconds
    Step  1      OS Connect Device
    Step  2      Verify Enclosure Inventory details on CLI and page command AthenaA  ${Inventory_ses_cmd}  ${Inventory_CLI_cmd}
    Step  3      OS Disconnect Device
    Step  4      ConnectESMB
    Step  5      Verify Enclosure Inventory details on CLI and page command AthenaB  ${Inventory_ses_cmd}  ${Inventory_CLI_cmd}
    Step  6      OS Disconnect Device

CONSR-SEST-IVMT-0001-0001
    [Documentation]  This test case checks the canister A status - page 02h
    [Tags]   CONSR-SEST-IVMT-0001-0001    Athena-G2
    [Timeout]  5 min 00 seconds
    Step  1    OS Connect Device
    Step  2    verify cansiter status and FW version Athena    ${page02_canisterA_cmd}    ${canisterA_status}
    Step  3    OS Disconnect Device

CONSR-SEST-IVMT-0002-0001
    [Documentation]  This test case checks the canister B status - page 02h
    [Tags]   CONSR-SEST-IVMT-0002-0001    Athena-G2
    [Timeout]  5 min 00 seconds
    Step  1   ConnectESMB
    Step  2   verify canister status Athena  ${page02_canisterB_cmd}    ${canisterB_status_Athena}
    Step  3   OS Disconnect Device

CONSR-SEST-IVMT-0003-0001
    [Documentation]  This test case Check the canister A Inventory - page 07h
    [Tags]     CONSR-SEST-IVMT-0003-0001   Athena-G2
    [Timeout]  5 min 00 seconds
    Step  1    OS Connect Device
    Step  2    Verify canister details on CLI and page command Athena  ${canister_a_ses_cmd}  ${canister_CLI_cmd}
    Step  3    OS Disconnect Device

CONSR-SEST-IVMT-0004-0001
    [Documentation]  This test case Check the canister B Inventory - page 07h
    [Tags]     CONSR-SEST-IVMT-0004-0001  Athena-G2
    [Timeout]  5 min 00 seconds
    Step  1    ConnectESMB
    Step  2    Verify canister B inventory in page command Athena   ${canister_b_ses_cmd}   ${canister_b_pattern_athena}
    Step  3    OS Disconnect Device

CONSR-SEST-CMDL-0002-0001
    [Documentation]  This test checks detailed CLI command setting and getting test
    [Tags]    CONSR-SEST-CMDL-0002-0001   Athena-G2
    [Timeout]  3 min 00 seconds
    Step  1    OS Connect Device
    Step  2    verify CLI set get CLI command Athena
    Step  3    OS Disconnect Device
    Step  4    ConnectESMB
    Step  5    verify CLI set get CLI command Athena
    Step  6    OS Disconnect Device

CONSR-SEST-IVMT-0010-0001
    [Documentation]  This test case checks PSU 0 status - page 02h
    [Tags]    CONSR-SEST-IVMT-0010-0001  Athena-G2
    [Timeout]  5 min 00 seconds
    Step  1    OS Connect Device
    Step  2    check PSU status Athena  ${psu0_status_pg2_cmd}  ${psu034_status_pg2_pattern}
    Step  3    CLI check for psu status Athena  ${psu0_cli_pattern_athena}
    Step  4    OS Disconnect Device
    Step  5    ConnectESMB
    Step  6    check PSU status Athena  ${psu0_status_pg2_cmd}  ${psu034_status_pg2_pattern}
    Step  7    CLI check for psu status Athena  ${psu0_cli_pattern_athena}
    Step  8    OS Disconnect Device

CONSR-SEST-IVMT-0011-0001
    [Documentation]  This test case checks PSU 1 status - page 02h
    [Tags]     CONSR-SEST-IVMT-0011-0001   Athena-G2
    [Timeout]  5 min 00 seconds
    Step  1    OS Connect Device
    Step  2    check PSU status Athena  ${psu1_status_pg2_cmd}  ${psu125_status_pg2_pattern_athena}
    Step  3    CLI check for psu status Athena  ${psu1_cli_pattern_athena}
    Step  4    OS Disconnect Device
    Step  5    ConnectESMB
    Step  6    check PSU status Athena  ${psu1_status_pg2_cmd}  ${psu125_status_pg2_pattern_athena}
    Step  7    CLI check for psu status Athena  ${psu1_cli_pattern_athena}
    Step  8    OS Disconnect Device

CONSR-SEST-SMRD-0039-0001
    [Documentation]  This test checks Threshold Out Diagnostic Pages(05h) - Temp LW
    [Tags]  CONSR-SEST-SMRD-0039-0001   Athena-G2
    [Timeout]  5 min 00 seconds
    Step  1  OS Connect Device
    Step  2  temp lm upgrade test Athena  0  ^0$
    Step  3  verify_esm_fan_mode_cli_command  DUT  internal
    Step  4  OS Disconnect Device
    Step  5  ConnectESMB
    Step  6  temp lm upgrade test Athena  0  ^0$
    Step  7  verify_esm_fan_mode_cli_command  DUT  internal
    Step  8  OS Disconnect Device

CONSR-SEST-SMRD-0040-0001
    [Documentation]  This test checks Threshold Out Diagnostic Pages(05h) - Temp UC
    [Tags]  CONSR-SEST-SMRD-0040-0001   Athena-G2
    [Timeout]  5 min 00 seconds
    Step  1  OS Connect Device
    Step  2  temp lm upgrade test Athena  1  ^1$
    Step  3  verify_esm_fan_mode_cli_command  DUT  external
    Step  4  OS Disconnect Device
    Step  5  ConnectESMB
    Step  6  temp lm upgrade test Athena  1  ^1$
    Step  7  verify_esm_fan_mode_cli_command  DUT  external
    Step  8  OS Disconnect Device

CONSR-SEST-STRS-0007-0001
    [Documentation]  This test checks CPLD download Stress Test
    [Tags]  CONSR-SEST-STRS-0007-0001   Athena-G2
    [Timeout]  30 min 00 seconds
    [Setup]    get dut variables
    Step  1  Download Athena CPLD image
    Step  2  check esm mode status Athena
    Step  3  check esm mode status ESMB Athena
    FOR    ${INDEX}    IN RANGE    ${MAXINDEX}
        Print Loop Info  ${INDEX}
        Step  1  upgrade cpld with mode 0xe + mode 0xf Athena ESMA
        Step  2  upgrade cpld with mode 0xe + mode 0xf Athena ESMB
    END
    Step  5  check esm mode status Athena
    Step  6  check esm mode status ESMB Athena
    Step  7  Remove Athena CPLD image

CONSR-SEST-STRS-0001-0001
    [Documentation]  This test checks stress upgrade/downgrade FW with mode 0xe
    [Tags]     CONSR-SEST-STRS-0001-0001  Athena-G2
    [Timeout]  48 hours
    Step  1  Download Athena FW image
    FOR    ${INDEX}    IN RANGE    ${MAXINDEX}
        Print Loop Info  ${INDEX}        
        Step  1    Downgrade Canister A PEX0 FW - Mode E + F and check Downgrade status
        Step  2    Downgrade Canister A PEX1 FW - Mode E + F and check Downgrade status
        Step  3    Downgrade Canister B PEX0 FW - Mode E + F and check Downgrade status
        Step  4    Downgrade Canister B PEX1 FW - Mode E + F and check Downgrade status
        Step  5    Upgrade Canister A PEX0 FW - Mode E + F and check upgrade status
        Step  6    Upgrade Canister A PEX1 FW - Mode E + F and check upgrade status
        Step  7    Upgrade Canister B PEX0 FW - Mode E + F and check upgrade status
        Step  8    Upgrade Canister B PEX1 FW - Mode E + F and check upgrade status
    END
    Step  2  Remove Athena FW image
    [Teardown]  Run Keywords  Server Disconnect
           ...  AND Disconnect

CONSR-SEST-STRS-0004-0001
    [Documentation]  Enclosure LED Stress Test
    [Tags]     CONSR-SEST-STRS-0004-0001  Athena-G2
    [Timeout]  24 hours
    FOR    ${INDEX}    IN RANGE    ${MAXINDEX}
        Print Loop Info  ${INDEX}
        Step  1  server Connect
        Step  2  verify Enclosure LED on off status Athena  ${set_on_enc_LED}   ${set_off_enc_LED}  ${get_cmd}  ${get_page2_cmd}  ${get_enc_LED}  ${enc_LED_on_pattern}  ${enc_LED_off_pattern}
        Step  3  Server Disconnect
        Step  4  server Connect ESMB
        Step  5  verify Enclosure LED on off status Athena  ${set_on_enc_LED}   ${set_off_enc_LED}  ${get_cmd}  ${get_page2_cmd}  ${get_enc_LED}  ${enc_LED_on_pattern}  ${enc_LED_off_pattern}
        Step  6  Server Disconnect
    END
    [Teardown]  Run Keywords  Server Disconnect
           ...  AND Disconnect

CONSR-SEST-SPCK-0054-0001
    [Documentation]  SES Download microcode Control Diagnostic Page (mode 7)
                ...  - Checking download status
    [Tags]     CONSR-SEST-SPCK-0054-0001   Athena-G2
    [Timeout]  60 min 00 seconds
    Step  1     Download SES FW File And Check Downloading Status Athena ESMA
    Step  2     Download SES FW File And Check Downloading Status Athena ESMB

CONSR-SEST-SPCK-0055-0001
    [Documentation]  SES Download microcode Control Diagnostic Page (mode E)
                ...  - Checking download status
    [Tags]     CONSR-SEST-SPCK-0055-0001  Athena-G2
    [Timeout]  60 min 00 seconds
    [Setup]  Download Athena FW image
    Step  1  Check Downloading Status Without Activate Athena ESMA
    Step  2  Check Downloading Status Without Activate Athena ESMB
    Step  3  Remove Athena FW image
    [Teardown]  Run Keywords  Server Disconnect
           ...  AND Disconnect

CONSR-SEST-SPCK-0056-0001
    [Documentation]  SES Download microcode Control Diagnostic Page (mode F)
                ...  - Checking download status
    [Tags]     CONSR-SEST-SPCK-0056-0001   Athena-G2
    [Timeout]  30 min 00 seconds
    Step  1     activate New FW Partition Athena ESMA
    Step  2     activate New FW Partition Athena ESMB
    [Teardown]  Run Keywords  Server Disconnect
           ...  AND Disconnect

CONSR-SEST-SPCK-0057-0001
    [Documentation]  SES Download microcode Status Diagnostic Page
    [Tags]     CONSR-SEST-SPCK-0057-0001   Athena-G2
    [Timeout]  10 min 00 seconds
    Step  1     check FW Download Status Athena

CONSR-SEST-SPCK-0020-0001
    [Documentation]  This test checks  Enclosure Control Diagnostic Pages(02h) - Fan current speed
    [Tags]     CONSR-SEST-SPCK-0020-0001   Athena-G2
    [Timeout]  10 min 00 seconds
    [Setup]    get dut variables
    Sub-Case  CONSR-SEST-SPCK-0020-0001_1  check esm mode status Athena
    Sub-Case  CONSR-SEST-SPCK-0020-0001_2  check Cooling external Mode ESMA Athena
    Sub-Case  CONSR-SEST-SPCK-0020-0001_3  check Fan current speed Athena ESMA
    Sub-Case  CONSR-SEST-SPCK-0020-0001_4  check esm mode status ESMB Athena
    Sub-Case  CONSR-SEST-SPCK-0020-0001_5  check Cooling external Mode ESMB Athena
    Sub-Case  CONSR-SEST-SPCK-0020-0001_6  check Fan current speed Athena ESMB

    [Teardown]  Run Keywords  Server Disconnect
           ...  AND Disconnect

CONSR-SEST-SPCK-0021-0001
    [Documentation]  This test checks  Enclosure Control Diagnostic Pages(02h) - Fan max speed
    [Tags]     CONSR-SEST-SPCK-0021-0001   Athena-G2
    [Timeout]  10 min 00 seconds
    [Setup]    get dut variables
    Sub-Case  CONSR-SEST-SPCK-0021-0001_1  check esm mode status Athena
    Sub-Case  CONSR-SEST-SPCK-0021-0001_2  check Cooling external Mode ESMA Athena
    Sub-Case  CONSR-SEST-SPCK-0021-0001_3  check Fan max_min speed Athena ESMA   ${fan_max_speed}  ${fan_max_speed_cli_Athena}
    Sub-Case  CONSR-SEST-SPCK-0021-0001_4  check esm mode status ESMB Athena
    Sub-Case  CONSR-SEST-SPCK-0021-0001_5  check Cooling external Mode ESMB Athena
    Sub-Case  CONSR-SEST-SPCK-0021-0001_6  check Fan max_min speed Athena ESMB   ${fan_max_speed}  ${fan_max_speed_cli_Athena}
    [Teardown]  Run Keywords  Server Disconnect
           ...  AND Disconnect

CONSR-SEST-SPCK-0022-0001
    [Documentation]  This test checks  Enclosure Control Diagnostic Pages(02h) - Fan min speed
    [Tags]     CONSR-SEST-SPCK-0022-0001    Athena-G2
    [Timeout]  10 min 00 seconds
    [Setup]    get dut variables
    Sub-Case  CONSR-SEST-SPCK-0022-0001_1  check esm mode status Athena
    Sub-Case  CONSR-SEST-SPCK-0022-0001_2  check Cooling external Mode ESMA Athena
    Sub-Case  CONSR-SEST-SPCK-0022-0001_3  check Fan max_min speed Athena ESMA   ${fan_min_speed}  ${fan_min_speed_cli_Athena}
    Sub-Case  CONSR-SEST-SPCK-0022-0001_4  check esm mode status ESMB Athena
    Sub-Case  CONSR-SEST-SPCK-0022-0001_5  check Cooling external Mode ESMB Athena
    Sub-Case  CONSR-SEST-SPCK-0022-0001_6  check Fan max_min speed Athena ESMB   ${fan_min_speed}  ${fan_min_speed_cli_Athena}
    [Teardown]  Run Keywords  Server Disconnect
           ...  AND Disconnect


CONSR-SEST-CLMT-0001-0001
    [Documentation]  This test checks SES Enclosure Control Page Cooling element- current speed
    [Tags]   CONSR-SEST-CLMT-0001-0001   Athena-G2
    [Timeout]  8 min 00 seconds
    [Setup]    get dut variables
    Step  1    check fan speed Athena   ${fan_min_speed}   ${fan_min_speed_athena}
    Step  2    check fan speed Athena   ${fan_speed_10}   ${fan_speed_10_cli_athena}
    Step  3    check fan speed Athena   ${fan_speed_11}   ${fan_speed_11_cli_athena}
    Step  4    check fan speed Athena   ${fan_speed_12}   ${fan_speed_12_cli_athena}
    Step  5    check fan speed Athena   ${fan_speed_13}   ${fan_speed_13_cli_athena}
    Step  6    check fan speed Athena   ${fan_speed_14}   ${fan_speed_14_cli_athena}
    Step  7    check fan current speed Athena ESMA
    Step  8    check Fan current speed Athena ESMB
    [Teardown]  Run Keywords  Server Disconnect
           ...  AND Disconnect


CONSR-SEST-STRS-0002-0001
    [Documentation]   Drive Disk LED stress Test
    [Tags]     CONSR-SEST-STRS-0002-0001    Athena-G2
    [Timeout]  24 hours
    FOR    ${INDEX}    IN RANGE    ${MAXINDEX}
        Print Loop Info  ${INDEX}
        Step  1  server Connect
        Step  2  verify drive disk LED on off status Athena    ${set_on_ident_LED}   ${set_off_ident_LED}  ${get_page2_cmd}  ${get_ident_LED}  ${ident_disk_fault_LED_on_pattern}  ${ident_disk_fault_LED_off_pattern}
        Step  3  verify drive disk LED on off status Athena    ${set_on_disk_fault_LED}  ${set_off_disk_fault_LED}  ${get_page2_cmd}  ${get_disk_fault_LED}  ${ident_disk_fault_LED_on_pattern}  ${ident_disk_fault_LED_off_pattern}
        Step  4  Server Disconnect
        Step  5  server Connect ESMB
        Step  6  verify drive disk LED on off status Athena    ${set_on_ident_LED}   ${set_off_ident_LED}  ${get_page2_cmd}  ${get_ident_LED}  ${ident_disk_fault_LED_on_pattern}  ${ident_disk_fault_LED_off_pattern}
        Step  7  verify drive disk LED on off status Athena    ${set_on_disk_fault_LED}  ${set_off_disk_fault_LED}  ${get_page2_cmd}  ${get_disk_fault_LED}  ${ident_disk_fault_LED_on_pattern}  ${ident_disk_fault_LED_off_pattern}
        Step  8  Server Disconnect
    END
    [Teardown]  Run Keywords  Server Disconnect
           ...  AND Disconnect


CONSR-SEST-STRS-0003-0001
    [Documentation]   Canister LED stress Test
    [Tags]     CONSR-SEST-STRS-0003-0001   Athena-G2
    [Timeout]  24 hours
    FOR    ${INDEX}    IN RANGE    ${MAXINDEX}
        Print Loop Info  ${INDEX}
        Step  1  server Connect
        Step  2  verify canister LED on off status Athena  ${set_canister_ident_on}  ${clear_canister_ident}  ${check_can_ident0_cmd}  ${check_can_ident1_cmd}  ${get_ident_LED}   ${can_iden_on_pattern}  ${can_ident_off_pattern}  ${can_ident_on_pattern_total}
        Step  3  verify canister LED on off status Athena   ${set_canister_fault_on}  ${clear_canister_fault}  ${check_can_fault0_cmd}  ${check_can_fault1_cmd}  ${get_LED_8}  ${can_fault_on_pattern}  ${can_fault_off_pattern}   ${can_fault_on_pattern_total}
        Step  4  Server Disconnect
        Step  5  server Connect ESMB
        Step  6  verify canister LED on off status Athena  ${set_canister_ident_on}  ${clear_canister_ident}  ${check_can_ident0_cmd}  ${check_can_ident1_cmd}  ${get_ident_LED}   ${can_iden_on_pattern}  ${can_ident_off_pattern}  ${can_ident_on_pattern_total}
        Step  7  verify canister LED on off status Athena   ${set_canister_fault_on}  ${clear_canister_fault}  ${check_can_fault0_cmd}  ${check_can_fault1_cmd}  ${get_LED_8}  ${can_fault_on_pattern}  ${can_fault_off_pattern}   ${can_fault_on_pattern_total}
        Step  8  Server Disconnect
    END
    [Teardown]  Run Keywords  Server Disconnect
           ...  AND Disconnect


CONSR-SEST-SPCK-0050-0001
    [Documentation]  Additional Element Status Diagnostic Page(0ah)
    [Tags]     CONSR-SEST-SPCK-0050-0001  Athena_G2
    [Timeout]  5 min 00 seconds
    Step  1  check esm mode status Athena
    Step  2  check esm mode status ESMB Athena
    Step  3  check Disks Info On Page 0x0a Athena
    [Teardown]  Run Keywords  Server Disconnect
           ...  AND Disconnect

CONSR-SEST-SMRD-0041-0001
    [Documentation]   Fan Speed via SES - Current Speed
    [Tags]   CONSR-SEST-SMRD-0041-0001   Athena_G2
    [Timeout]  5 min 00 seconds
    Step  1  OS Connect Device
    Step  2  temp lm upgrade test Athena  8  ^0$
    change_to_ESM_mode
    Step  3  verify_esm_fan_mode_cli_command  DUT  external
    exit_ESM_mode
    Step  4  OS Disconnect Device
    Step  5  ConnectESMB
    Step  6  temp lm upgrade test Athena  8  ^0$
    change_to_ESM_mode
    Step  7  verify_esm_fan_mode_cli_command  DUT  external
    exit_ESM_mode
    Step  8  OS Disconnect Device

CONSR-SEST-SMRD-0042-0001
    [Documentation]   Fan Speed via SES - Min Speed
    [Tags]   CONSR-SEST-SMRD-0042-0001   Athena_G2
    [Timeout]  5 min 00 seconds
    Step  1  OS Connect Device
    Step  2  temp lm upgrade test Athena  9  ^0$
    change_to_ESM_mode
    Step  3  verify_esm_fan_mode_cli_command  DUT  external
    exit_ESM_mode
    Step  4  OS Disconnect Device
    Step  5  ConnectESMB
    Step  6  temp lm upgrade test Athena  9  ^0$
    change_to_ESM_mode
    Step  7  verify_esm_fan_mode_cli_command  DUT  external
    exit_ESM_mode
    Step  8  OS Disconnect Device

CONSR-SEST-SMRD-0043-0001
    [Documentation]   Fan Speed via SES - Max Speed
    [Tags]   CONSR-SEST-SMRD-0043-0001    Athena_G2
    [Timeout]  5 min 00 seconds
    Step  1  OS Connect Device
    Step  2  temp lm upgrade test Athena  15  ^0$
    change_to_ESM_mode
    Step  3  verify_esm_fan_mode_cli_command  DUT  external
    exit_ESM_mode
    Step  4  OS Disconnect Device
    Step  5  ConnectESMB
    Step  6  temp lm upgrade test Athena  15  ^0$
    change_to_ESM_mode
    Step  7  verify_esm_fan_mode_cli_command  DUT  external
    exit_ESM_mode
    Step  8  OS Disconnect Device

CONSR-SEST-SMRD-0044-0001
    [Documentation]   Fan Speed via SES - CLI Check
    [Tags]   CONSR-SEST-SMRD-0044-0001   Athena_G2
    [Timeout]  5 min 00 seconds
    Step  1  OS Connect Device
    Step  2  verify Fan CLI Set Get CLI Command
    Step  3  OS Disconnect Device
    Step  4  ConnectESMB
    Step  5  verify Fan CLI Set Get CLI Command
    Step  6  OS Disconnect Device

CONSRS-DP-02-0001
    [Documentation]  This test checks Drive Disk Power OnOff - CLI
    [Tags]    CONSRS-DP-02-0001    Athena_G2
    [Timeout]  8 min 00 seconds
    Step  1  OS Connect Device
    Step  2  verify Drive Disk power On Off Athena
    Step  3  OS Disconnect Device
    Step  4  ConnectESMB
    Step  5  verify Drive Disk power On Off Athena
    Step  6  OS Disconnect Device

CONSR-SEST-IVMT-0021-0001
    [Documentation]  This test case checks the array device disk Inventory - page 0Ah
    [Tags]     CONSR-SEST-IVMT-0021-0001   Athena_G2
    [Timeout]  5 min 00 seconds
    Step  1  OS Connect Device
    Step  2  Verify element index in pageA    ${page_a_command}  ${a_page_Output}
    Step  3  OS Disconnect Device
    Step  4  ConnectESMB
    Step  5  Verify element index in pageA    ${page_a_command}  ${a_page_Output}
    Step  6  OS Disconnect Device

CONSR-SEST-IVMT-0019-0001
    [Documentation]  This test checks the array device disk status - page 02h
    [Tags]   CONSR-SEST-IVMT-0019-0001   Athena_G2
    [Timeout]  5 min 00 seconds
    Step  1   OS Connect Device
    Step  2   check driver status Athena  ${page_drvstatus_cmd}  ${drv0_2}  ${OK_status1}
    Step  3   check driver status Athena  ${page_drvstatus_cmd}  ${drv3}  ${unsupported_status1}
    Step  4   check driver status Athena  ${page_drvstatus_cmd}  ${drv4}  ${OK_status1}
    Step  5   check driver status Athena  ${page_drvstatus_cmd}  ${drv5}   ${unsupported_status1}
    Step  6   check driver count Athena
    Step  8  OS Disconnect Device
    Step  9     ConnectESMB
    Step  10   check driver status Athena  ${page_drvstatus_cmd}  ${drv0_2}  ${OK_status1}
    Step  11   check driver status Athena  ${page_drvstatus_cmd}  ${drv3}  ${unsupported_status1}
    Step  12   check driver status Athena  ${page_drvstatus_cmd}  ${drv4}  ${OK_status1}
    Step  13   check driver status Athena  ${page_drvstatus_cmd}  ${drv5}   ${unsupported_status1}
    Step  14   check driver count Athena
    Step  16  OS Disconnect Device

CONSR-SEST-SPCK-0060-0001
    [Documentation]  This test checks Log Control Diagnostic Page (13h) - Get Log Entry Descriptor
    [Tags]   CONSR-SEST-SPCK-0060-0001   Athena_G2
    [Timeout]  5 min 00 seconds
    Step  1    OS Connect Device
    Step  2    get Control Decscriptor Information Athena  ${page_13_entries_num_cmd}
    Step  3    Verify log pattern Athena   ${page_13_status_cmd}  ${log_entry_code}  ${clear_log_entry_pattern_athena}
    Step  4    get Control Decscriptor Information Athena   ${page_13_clear_log_cmd}
    Step  5    Verify log pattern Athena   ${page_13_status_cmd}  ${clear_log_entry_code}  ${clear_log_entry_pattern_athena}
    Step  6    CLI check for log entry Athena
    Step  7    OS Disconnect Device
    Step  8    ConnectESMB
    Step  9    get Control Decscriptor Information Athena   ${page_13_entries_num_cmd_b}
    Step  10    Verify log pattern Athena   ${page_13_status_cmd}  ${log_entry_code}  ${clear_log_entry_pattern_athena_b}
    Step  11    get Control Decscriptor Information Athena   ${page_13_clear_log_cmd_b}
    Step  12    Verify log pattern Athena   ${page_13_status_cmd}  ${clear_log_entry_code}  ${clear_log_entry_pattern_athena_b}
    Step  13    CLI check for log entry Athena
    Step  14    OS Disconnect Device

CONSR-SEST-SPCK-0059-0001
    [Documentation]  This test checks Log Control Diagnostic Page (13h) - Log Misc Control
    [Tags]   CONSR-SEST-SPCK-0059-0001   Athena_G2
    [Timeout]  5 min 00 seconds
    Step  1    OS Connect Device
    Step  2    send a command Athena   ${page_13_new_log_check_cmd}
    Step  3    compare new log with CLI Athena   ${page_13_status_cmd}
    Step  4    send a command Athena   ${page_13_read_status_cmd}
    Step  5    Verify log pattern Athena  ${page_13_status_cmd}  ${log_read_code}  ${page_13_read_status_pattern}
    Step  6    send a command Athena  ${page_13_unread_status_cmd}
    Step  7    Verify log pattern Athena  ${page_13_status_cmd}  ${log_unread_code}  ${page_13_unread_status_pattern}
    Step  8    send a command Athena  ${page_13_clear_log_cmd}
    Step  9    Verify log pattern Athena   ${page_13_status_cmd}  ${clear_log_entry_code}  ${clear_log_entry_pattern}
    Step  10   CLI check for log entry Athena
    Step  11   OS Disconnect Device
    Step  12   ConnectESMB
    Step  13   send a command Athena   ${page_13_new_log_check_cmd}
    Step  14   compare new log with CLI Athena   ${page_13_status_cmd}
    Step  15   send a command Athena   ${page_13_read_status_cmd}
    Step  16   Verify log pattern Athena  ${page_13_status_cmd}  ${log_read_code}  ${page_13_read_status_pattern}
    Step  17   send a command Athena  ${page_13_unread_status_cmd}
    Step  18   Verify log pattern Athena  ${page_13_status_cmd}  ${log_unread_code}  ${page_13_unread_status_pattern}
    Step  19   send a command Athena  ${page_13_clear_log_cmd}
    Step  20   Verify log pattern Athena   ${page_13_status_cmd}  ${clear_log_entry_code}  ${clear_log_entry_pattern}
    Step  21   CLI check for log entry Athena
    Step  22   OS Disconnect Device

CONSR-SEST-SPCK-0027-0001
    [Documentation]  Check array device power off - Enclosure Control Diagnostic Pages(02h)
    [Tags]     CONSR-SEST-SPCK-0027-0001  Athena_G2
    [Timeout]  5 min 00 seconds
    Step  1    OS Connect Device
    Step  2    check Disk Power Off Athena
    Step  3    OS Disconnect Device
    Step  4    ConnectESMB
    Step  5    check Disk Power Off Athena
    Step  6    OS Disconnect Device

CONSR-SEST-CLMT-0007-0001
    [Documentation]  This test checks Fan Status Monitoring
    [Tags]   CONSR-SEST-CLMT-0007-0001    Athena_G2
    [Timeout]  10 min 00 seconds
    [Setup]    get dut variable
    Step  1    OS Connect Device
    Step  2    set and verify fan control mode Athena
    Step  3    set and verify pwm value Athena
    Step  4    set and verify level Athena
    Step  5    OS Disconnect Device
    Step  6    ConnectESMB
    Step  7    set and verify fan control mode Athena
    Step  8    set and verify pwm value Athena
    Step  9    set and verify level Athena
    Step  10   OS Disconnect Device

CONSR-SEST-SPCK-0075-0001
    [Documentation]  This test checks VPD information Control/Status Diagnostic Page (12h)- VPD information-get all
    [Tags]    CONSR-SEST-SPCK-0075-0001   Athena_G2
    [Timeout]  8 min 00 seconds
    Step  1    OS Connect Device
    Step  2    verify VPD information Athena
    Step  3    OS Disconnect Device
    Step  4    ConnectESMB
    Step  5    verify VPD information Athena
    Step  6    OS Disconnect Device

CONSR-SEST-CLMT-0006-0001
    [Documentation]  This test checks Temperature Monitoring
    [Tags]   CONSR-SEST-CLMT-0006-0001  Athena_G2
    [Timeout]  8 min 00 seconds
    Step  1    OS Connect Device
    Step  2    set and verify UW Athena
    Step  3    set and verify UC Athena
    Step  4    set and verify LW Athena
    Step  5    set and verify LC Athena
    Step  6    OS Disconnect Device
    Step  7    ConnectESMB
    Step  8    set and verify UW Athena
    Step  9    set and verify UC Athena
    Step  10    set and verify LW Athena
    Step  11    set and verify LC Athena
    Step  12    OS Disconnect Device

CONSR-SEST-SPCK-0046-0001
    [Documentation]  Element Descriptor Diagnostic Page(07h)
    [Tags]     CONSR-SEST-SPCK-0046-0001   Athena_G2
    [Timeout]  5 min 00 seconds
    Step  1    OS Connect Device
    Step  2    get FRU Info Athena
    Step  3    check Descriptor Length Athena
    Step  4    OS Disconnect Device
    Step  5    ConnectESMB
    Step  6    get FRU Info Athena
    Step  7    check Descriptor Length Athena
    Step  8    OS Disconnect Device

CONSR-SEST-SPCK-0037-0001
    [Documentation]  This test checks String In Diagnostic Pages(05h)
    [Tags]     CONSR-SEST-SPCK-0037-0001   Athena_G2
    [Timeout]  10 min 00 seconds
    [Setup]    get dut variables
    Sub-Case  CONSR-SEST-SPCK-0037-0001_1    check String In Diagnostic Pages Athena(05h)
    Sub-Case  CONSR-SEST-SPCK-0037-0001_1    check String In Diagnostic Pages Athena ESMB(05h)

CONSR-SEST-CMDL-0003-0001
    [Documentation]  This test combination of CLI commands with delays between the commands
    [Tags]    CONSR-SEST-CMDL-0003-0001   Athena-G2
    [Timeout]  30 min 00 seconds
    Step  1    OS Connect Device
    Step  2    verify CLI Set Get Command With Delays Athena  ${delay_seconds}
    Step  3    OS Disconnect Device
    Step  4    ConnectESMB
    Step  5    verify CLI Set Get Command With Delays Athena  ${delay_seconds}
    Step  6    OS Disconnect Device

CONSR-SEST-CMDL-0004-0001
    [Documentation]  This test CLI interface with invalid, incorrect & variable sized arguments.
    [Tags]    CONSR-SEST-CMDL-0004-0001   Athena-G2
    Step  1    OS Connect Device
    Step  2    verify CLI Invalid Incorrect Command Athena
    Step  3    OS Disconnect Device
    Step  4    ConnectESMB
    Step  5    verify CLI Invalid Incorrect Command Athena
    Step  6    OS Disconnect Device

*** Keywords ***
OS Connect Device
    OSConnect

OS Disconnect Device
    OSDisconnect

check ESM And Connect Server
    check esm mode status
    server Connect

get dut variables
    get dut variable
    get dut variable ESMB

Print Loop Info
    [Arguments]    ${CUR_INDEX}
    Log  *******************************************
    Log  *** Test Loop \#: ${CUR_INDEX} / ${LoopCnt} ***
    Log  *
