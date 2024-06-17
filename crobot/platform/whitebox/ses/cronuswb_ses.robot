*** Settings ***
Documentation       Tests to verify ses functions described in the ses function spec for the whiteboxproject.

Variables         ses_variable.py
Variables         cronus_ses_variable.py
Library           ../WhiteboxLibAdapter.py
Library           whitebox_lib.py
Library           CommonLib.py
Library           ses_lib.py
Library           cronus_ses_lib.py
Resource          ses_keywords.robot
Resource          cronus_ses_keywords.robot

#Suite Setup       OS Connect Device
#Suite Teardown    OS Disconnect Device

** Variables ***
# It is recommended to use <{ScriptName}|{FeatureName}|{DomainName}_Variable> file for variable declaration with help of
# setting table. This section should keep blank.
#In extreme case if script requires variable then it should be defined in this table with documentaiton tag

*** Test Cases ***


CONSR-SEST-SPCK-0001-0001
    [Documentation]  This test checks  SES Page - Supported Diagnostic Pages Diagnostic Page (00h)
    [Tags]     CONSR-SEST-SPCK-0001-0001   Cronus_WB    Regression
    [Timeout]  5 min 00 seconds
    [Setup]    get dut variable
    Step  1    server Connect
    Step  2   check all supported diagnostic pages
    Step  3  Server Disconnect
	
CONSR-SEST-SPCK-0002-0001
    [Documentation]  This test checks  SES Page - Configuration Diagnostic Pages(01h)
    [Tags]     CONSR-SEST-SPCK-0002-0001  Cronus_WB    Regression  rerun
    [Timeout]  5 min 00 seconds
    [Setup]    get dut variable
    Step  1  server Connect
    Step  2  Configuration Diagnostic Pages(01h) Cronus
    Step  3  Server Disconnect

CONSR-SEST-SPCK-0026-0001
    [Documentation]  Check array device OK bit - Enclosure Control Diagnostic Pages(02h)
    [Tags]     CONSR-SEST-SPCK-0026-0001  Cronus_WB    Regression
    [Timeout]  5 min 00 seconds
    [Setup]  Server Connect
    Step  1  check Array OK Bit
    [Teardown]  Server Disconnect

CONSR-SEST-SPCK-0003-0001
    [Documentation]  This test checks  Enclosure Status Diagnostic Pages(02h)
    [Tags]     CONSR-SEST-SPCK-0003-0001  Cronus_WB    Regression
    [Timeout]  5 min 00 seconds
    [Setup]    get dut variable
    Step   1   server Connect
    Step   2   Enclosure Status Diagnostic Pages(02h)
    Step   3   Server Disconnect

CONSR-SEST-SPCK-0005-0001
    [Documentation]  This test checks  Enclosure Control Diagnostic Pages(02h) - check 'Info' bit
    [Tags]     CONSR-SEST-SPCK-0005-0001  Cronus_WB    Regression 
    [Timeout]  5 min 00 seconds
    [Setup]  get dut variable
    Step   1   server Connect 
    Step  2    check Info bit Cronus 
    Step   3   Server Disconnect

CONSR-SEST-SPCK-0006-0001
    [Documentation]  Check 'crit' bit with sensors under UC condition - Enclosure Control Diagnostic Pages(02h)
    [Tags]     CONSR-SEST-SPCK-0006-0001  Cronus_WB    Regression  rerun
    [Timeout]  5 min 00 seconds
    [Setup]  server Connect 
    Step  1  Run Keyword And Continue On Failure  check Temperature Alarm Cronus  high critical
    Step  2  restore Temperature Threshold  high critical
    [Teardown]  Server Disconnect

CONSR-SEST-SPCK-0007-0001
    [Documentation]  Check 'crit' bit with sensors under LC condition - Enclosure Control Diagnostic Pages(02h)
    [Tags]     CONSR-SEST-SPCK-0007-0001  Cronus_WB    Regression  rerun
    [Timeout]  5 min 00 seconds
    [Setup]  server Connect
    Step  1  Run Keyword And Continue On Failure  check Temperature Alarm Cronus  low critical
    Step  2  restore Temperature Threshold  low critical
    [Teardown]  Server Disconnect

CONSR-SEST-SPCK-0008-0001
    [Documentation]  Check 'non-crit' bit with sensors under UW condition - Enclosure Control Diagnostic Pages(02h)
    [Tags]     CONSR-SEST-SPCK-0008-0001  Cronus_WB    Regression  rerun
    [Timeout]  5 min 00 seconds
    [Setup]  server Connect
    Step  1  Run Keyword And Continue On Failure  check Temperature Alarm Cronus  high warning
    Step  2  restore Temperature Threshold  high warning
    [Teardown]  Server Disconnect

		   
CONSR-SEST-SPCK-0009-0001
    [Documentation]  Check 'non-crit' bit with sensors under LW condition - Enclosure Control Diagnostic Pages(02h)
    [Tags]     CONSR-SEST-SPCK-0009-0001  Cronus_WB    Regression  rerun
    [Timeout]  5 min 00 seconds
    [Setup]  server Connect
    Step  1  Run Keyword And Continue On Failure  check Temperature Alarm Cronus  low warning
    Step  2  restore Temperature Threshold  low warning
    [Teardown]  Server Disconnect
		   
CONSR-SEST-SPCK-0013-0001
    [Documentation]  Set ESC element Ident LED and clear ESC element Ident LED - Enclosure Control Diagnostic Pages(02h)
    [Tags]     CONSR-SEST-SPCK-0013-0001  Cronus_WB    Regression
    [Setup]  server Connect
    Step  1  Run Keyword And Continue On Failure  check ESC Ident LED 
    [Teardown]  Server Disconnect

CONSR-SEST-SPCK-0036-0001
    [Documentation]  Threshold Out Diagnostic Pages(05h) - Temp LC
    [Tags]     CONSR-SEST-SPCK-0036-0001  Cronus_WB     Regression  rerun
    [Timeout]  5 min 00 seconds
    [Setup]  server Connect
    Step  1  check Temperature Alarm On Page5 Cronus  low critical
    Step  2  restore Temperature Threshold on Page5  low critical
    [Teardown]  Run Keywords  Server Disconnect

CONSR-SEST-SPCK-0037-0001
    [Documentation]  Threshold Out Diagnostic Pages(05h) - Temp LW
    [Tags]     CONSR-SEST-SPCK-0037-0001  Cronus_WB     Regression  rerun
    [Timeout]  5 min 00 seconds
    [Setup]  server Connect
    Step  1  check Temperature Alarm On Page5 Cronus  low warning
    Step  2  restore Temperature Threshold on Page5  low warning
    [Teardown]  Run Keywords  Server Disconnect

CONSR-SEST-SPCK-0038-0001
    [Documentation]  Threshold Out Diagnostic Pages(05h) - Temp UC
    [Tags]     CONSR-SEST-SPCK-0038-0001  Cronus_WB     Regression  rerun
    [Timeout]  5 min 00 seconds
    [Setup]  server Connect
    Step  1  Run Keyword And Continue On Failure  check Temperature Alarm Cronus  high critical
    Step  2  restore Temperature Threshold on Page5  high critical
    [Teardown]  Run Keywords  Server Disconnect

CONSR-SEST-SPCK-0039-0001
    [Documentation]  Threshold Out Diagnostic Pages(05h) - Temp UW
    [Tags]     CONSR-SEST-SPCK-0039-0001  Cronus_WB     Regression  rerun
    [Timeout]  5 min 00 seconds
    [Setup]  server Connect
    Step  1  check Temperature Alarm On Page5 Cronus  high warning
    Step  2  restore Temperature Threshold on Page5  high warning
    [Teardown]  Run Keywords  Server Disconnect

CONSR-SEST-SPCK-0048-0001
    [Documentation]  Additional Element Status Diagnostic Page(0ah)
    [Tags]     CONSR-SEST-SPCK-0048-0001  Cronus_WB    Regression
    [Timeout]  5 min 00 seconds
    [Setup]  server Connect
    Step  1  check Disks Info On Page 0x0a
    [Teardown]  Server Disconnect
	
CONSR-SEST-SCSI-0002-0001
    [Documentation]  check Enclosure Length
    [Tags]     CONSR-SEST-SCSI-0002-0001  Cronus_WB     Regression  rerun
    [Timeout]  5 min 00 seconds
    [Setup]     server Connect
    Step  1     check Enclosure Length  ${cronus_sg_inquiry_cmd}  ${cronus_sg_inquiry_pattern}
    ...         ${cronus_sg_inquiry_length}
    [Teardown]  Server Disconnect

CONSR-SEST-SPCK-0010-0001
    [Documentation]  Enclosure Control Diagnostic Pages(02h) -  Device Ident LED 
    [Tags]     CONSR-SEST-SPCK-0010-0001  Cronus_WB    Regression
    [Setup]  server Connect
    Step  1  Run Keyword And Continue On Failure  check disk Ident LED
    [Teardown]  Server Disconnect

CONSR-SEST-SPCK-0035-0001
    [Documentation]  SES Page - Threshold In Diagnostic Page (05h)
    [Tags]     CONSR-SEST-SPCK-0035-0001  Cronus_WB    Regression
    [Setup]  get dut variable
    Step  1  server Connect 
    Step  2  check String In Diagnostic Pages(05h)
    Step  3  Server Disconnect

CONSR-SEST-IVMT-0016-0001
    [Documentation]  This test checks the array device disk Inventory - page 07h
    [Tags]   CONSR-SEST-IVMT-0016-0001  Cronus_WB     Regression
    [Timeout]  5 min 00 seconds
    [Setup]    server Connect
    Step  1   check slot name format  ${cronus_page7_slotname_check_cmd}
    [Teardown]  Server Disconnect

CONSR-SEST-SPCK-0011-0001
    [Documentation]  Enclosure Control Diagnostic Pages(02h) -  Drive Fault LED
    [Tags]     CONSR-SEST-SPCK-0011-0001  Cronus_WB    Regression
    [Setup]  server Connect
    Step  1  Run Keyword And Continue On Failure  check disk Fault LED
    [Teardown]  Server Disconnect

CONSR-SEST-IVMT-0017-0001
    [Documentation]  This test case checks the array device disk Inventory - page 0Ah
    [Tags]     CONSR-SEST-IVMT-0017-0001  Cronus_WB     Regression
    [Timeout]  5 min 00 seconds
    [Setup]    server Connect
    #Step  1    Verify element index flag as invalid  ${page_0a_command}  ${sample_invalid_list_cronus_wb}  ${sample_invalid_list_cronus_wb}
    Step  2    Verify element index flag as valid Cronus    ${page_0a_command}  ${sample_valid_list_cronus_wb}    ${sample_valid_list_cronus_wb}
    [Teardown]  Server Disconnect

CONSR-SEST-SPCK-0012-0001
    [Documentation]  Enclosure Control Diagnostic Pages(02h) - Device Rebuild/Remapping LED
    [Tags]     CONSR-SEST-SPCK-0012-0001  Cronus_WB    Regression
    [Setup]  server Connect
    Step  1  Run Keyword And Continue On Failure  check disk Rebuild/remap LED
    [Teardown]  Server Disconnect

CONSR-SEST-SPCK-0014-0001
    [Documentation]  Enclosure Control Diagnostic Pages(02h) - ESC Fault LED
    [Tags]     CONSR-SEST-SPCK-0014-0001  Cronus_WB    Regression  rerun
    [Setup]  server Connect
    Step  1  Run Keyword And Continue On Failure  check ESC Fault Bit LED
    [Teardown]  Server Disconnect

CONSR-SEST-SPCK-0017-0001
    [Documentation]  Enclosure Control Diagnostic Pages(02h) - Encolsure Ident LED
    [Tags]     CONSR-SEST-SPCK-0017-0001  Cronus_WB    Regression  rerun
    [Setup]  server Connect
    Step  1  Run Keyword And Continue On Failure  check ENC Ident LED
    [Teardown]  Server Disconnect

CONSR-SEST-SPCK-0024-0001
    [Documentation]  Enclosure Control Diagnostic Pages(02h) - Encolsure Fault LED
    [Tags]     CONSR-SEST-SPCK-0024-0001  Cronus_WB    Regression  rerun
    [Setup]  server Connect
    Step  1  Run Keyword And Continue On Failure  check ENC Fault LED
    [Teardown]  Server Disconnect

CONSR-SEST-SPCK-0025-0001
    [Documentation]  Enclosure Control Diagnostic Pages(02h) - Encolsure Warning LED
    [Tags]     CONSR-SEST-SPCK-0025-0001  Cronus_WB    Regression  rerun
    [Setup]  server Connect
    Step  1  Run Keyword And Continue On Failure  check ENC Warning LED
    [Teardown]  Server Disconnect

CONSR-SEST-CLMT-0004-0001
    [Documentation]  SES Threshold Control Page -Temperature - UC 
    [Tags]     CONSR-SEST-CLMT-0004-0001  Cronus_WB     Regression
    [Timeout]  5 min 00 seconds
    [Setup]  server Connect
    Step  1  CLITempVerifyNormal
    Step  2  check Temperature Alarm On Page5 Cronus  high critical
    Step  3  CLITempVerifyUC
    Step  4  restore Temperature Threshold on Page5  high critical
    Step  5  CLITempVerifyNormal
    [Teardown]  Server Disconnect

CONSR-SEST-CLMT-0005-0001
    [Documentation]  SES Threshold Control Page -Temperature - LC 
    [Tags]     CONSR-SEST-CLMT-0005-0001  Cronus_WB     Regression
    [Timeout]  5 min 00 seconds
    [Setup]  server Connect
    Step  1  CLITempVerifyNormal
    Step  2  check Temperature Alarm On Page5 Cronus  low critical
    Step  3  CLITempVerifyLC
    Step  4  restore Temperature Threshold on Page5  low critical
    Step  5  CLITempVerifyNormal
    [Teardown]  Run Keywords  Server Disconnect

CONSR-SEST-CLMT-0006-0001
    [Documentation]  To monitor the temperature status 
    [Tags]   CONSR-SEST-CLMT-0006-0001  Cronus_WB    Regression 
    [Timeout]  5 min 00 seconds
    [Setup]    Run Keywords  clearLogs
               ...  AND Server Connect
    Step  1    Run Keyword And Continue On Failure  Cronus set and verify UW
    Step  2    Run Keyword And Continue On Failure  Cronus set and verify UC
    Step  3    Run Keyword And Continue On Failure  Cronus set and verify LW
    Step  4    Run Keyword And Continue On Failure  Cronus set and verify LC
    [Teardown]  Server Disconnect	

CONSR-SEST-PWMT-0006-0001
    [Documentation]  This test checks Voltage Monitoring
    [Tags]   CONSR-SEST-PWMT-0006-0001   Cronus_WB    Regression 
    [Timeout]  10 min 00 seconds
    [Setup]    server Connect
    Step  1    Run Keyword And Continue On Failure  Cronus set voltage and verify UW
    Step  2    Run Keyword And Continue On Failure  Cronussetthresholdvoltageerror
    [Teardown]  Server Disconnect

CONSR-SEST-DRMT-0001-0001
    [Documentation]  SES Enclosure Control Page Array Device Slot element -LED
    [Tags]   CONSR-SEST-DRMT-0001-0001  Cronus_WB  Regression
    [Timeout]  8 min 00 seconds
    [Setup]    server Connect
    Step  1    Run Keyword And Continue On Failure  check disk Ident LED
    Step  2    Run Keyword And Continue On Failure  check disk Fault LED
    [Teardown]  Server Disconnect

CONSR-SEST-SPCK-0058-0001
    [Documentation]  Page 0x10 other CLI command test
    [Tags]   CONSR-SEST-SPCK-0058-0001  Cronus_WB  Regression
    [Setup]    server Connect
    Step  1    Verify page and log CLI pattern   ${log_filter_diag_cmd}  ${log_filter_page_cmd}  ${log_filter_CLI_cmd}
    Step  2    Verify page and log CLI pattern   ${log_about_diag_cmd}  ${log_about_page_cmd}  ${log_about_CLI_cmd}
    [Teardown]  Server Disconnect

CONSR-SEST-SPCK-0057-0001
   [Documentation]  This test case checks Page 0x10 read ESM A expander log
   [Tags]     CONSR-SEST-SPCK-0057-0001  Cronus_WB  Regression
   [Timeout]  5 min 00 seconds
   [Setup]    server Connect
   Step  1    verify page with expander log Cronus    ${pg10_diag_cmd}   ${pg10_status_cmd}
   [Teardown]  Server Disconnect

#CONSR-SEST-SPCK-0034-0001
#   [Documentation]  String In Diagnostic Pages(04h)
#   [Tags]     CONSR-SEST-SPCK-0034-0001  Cronus_WB  Regression
#   [Timeout]  5 min 00 seconds
#   [Setup]    get dut variable
#   Step  1    check String In Diagnostic Pages(04h) Cronus WB
#   [Teardown]  Server Disconnect

#CONSR-SEST-CLMT-0007-0001
#    [Documentation]  This test checks Fan Status Monitoring
#    [Tags]   CONSR-SEST-CLMT-0007-0001   Cronus_WB     Regression    
#    [Timeout]  8 min 00 seconds
#    [Setup]    get dut variable
#    Step  1    set and verify fan control mode Titan G2 WB
#    Step  2    set and verify pwm value Titan G2 WB
#    Step  3    set and verify level Titan G2 WB
#    [Teardown]  Server Disconnect

CONSR-SEST-SPCK-0044-0001
    [Documentation]  Element Descriptor Diagnostic Page(07h)
    [Tags]     CONSR-SEST-SPCK-0044-0001  Cronus_WB    Regression
    [Timeout]  5 min 00 seconds
    Step  1  get FRU Info Cronus 
    Step  2  check Descriptor Length
    [Teardown]  Server Disconnect

CONSRS-SM-06-0001
    [Documentation]  This test checks  SMP PHY Control - link speed program
    [Tags]  CONSRS-SM-06-0001  Cronus_WB    Regression 
    [Timeout]  3 min 00 seconds
    [Setup]    server Connect
    Step  1    verify smp phy link speed Cronus WB
    [Teardown]  Server Disconnect

CONSRS-SM-07-0001
    [Documentation]  This test checks  SMP PHY Control -  phy enable/disable
    [Tags]  CONSRS-SM-07-0001  Cronus_WB    Regression 
    [Timeout]  10 min 00 seconds
    [Setup]    server Connect
    Step  1    verify smp phy enable disable Cronus WB
    [Teardown]  Server Disconnect

CONSRS-SM-08-0001
     [Documentation]  This test checks partial pathway timeout
     [Tags]   CONSRS-SM-08-0001   Cronus_WB    Regression 
     [Timeout]  5 min 00 seconds
     [Setup]    server Connect
     Step  1    Setting partial pathway timeout value Cronus WB
     [Teardown]  Server Disconnect

CONSR-SEST-DRMT-0003-0001
    [Documentation]  This test case checks the array device disk Slot id and disk SAS address - page 0Ah
    [Tags]     CONSR-SEST-DRMT-0003-0001   Cronus_WB
    [Timeout]  5 min 00 seconds
    [Setup]    server Connect
    Step  1  Verify element index in pageA    ${page_a_command}  ${cronus_a_page_Output}
    [Teardown]  Server Disconnect

CONSRS-SM-09-0001
     [Documentation]  This test checks SMP Phy partial and slumber enable and disable for SAS and SATA
     [Tags]   CONSRS-SM-09-0001   Cronus_WB    Regression 
     [Timeout]  5 min 00 seconds
     [Setup]    server Connect
     Step  1    Setting SMP Phy partial and slumber enable and disable for SAS and SATA Cronus WB
     [Teardown]  Server Disconnect

CONSR-SEST-SPCK-0004-0001
    [Documentation]  This test checks  Enclosure Control Diagnostic Pages(02h) - set control bits via raw data
    [Tags]     CONSR-SEST-SPCK-0004-0001  Cronus_WB    Regression
    [Timeout]  5 min 00 seconds
    [Setup]    get dut variable
    Step  1    server Connect
    Step  2    set control bits via raw data
    Step  3  Server Disconnect

CONSR-SEST-SPCK-0027-0001
    [Documentation]  Check array device power off - Enclosure Control Diagnostic Pages(02h)
    [Tags]     CONSR-SEST-SPCK-0027-0001  Cronus_WB
    [Timeout]  5 min 00 seconds
    [Setup]  get dut variable
    Step  1    server Connect
    Step  2  check Disk Power Off
    Step  3  Server Disconnect

CONSR-SEST-SPCK-0040-0001
    [Documentation]  Threshold Out Diagnostic Pages(05h) - Voltage UC
    [Tags]     CONSR-SEST-SPCK-0040-0001  Cronus_WB     Non-Sanity
    [Timeout]  5 min 00 seconds
    [Setup]  server Connect
    Step  1  check Sensor Alarm On Page5 Cronus  high critical  Voltage sensor
    Step  2  restore Threshold on Page5 Cronus  high critical  Voltage sensor
    [Teardown]  Run Keywords  Server Disconnect

#CONSR-SEST-SPCK-0041-0001
#    [Documentation]  Threshold Out Diagnostic Pages(05h) - Voltage UW
#    [Tags]     CONSR-SEST-SPCK-0041-0001  Cronus_WB     Non-Sanity
#    [Timeout]  5 min 00 seconds
#    [Setup]  server Connect
#    Step  1  check Sensor Alarm On Page5 Cronus  high warning  Voltage sensor
#    Step  2  restore Threshold on Page5 Cronus  high warning  Voltage sensor
#    [Teardown]  Run Keywords  Server Disconnect

CONSR-SEST-SPCK-0042-0001
    [Documentation]  Threshold Out Diagnostic Pages(05h) - Voltage LC
    [Tags]     CONSR-SEST-SPCK-0042-0001  Cronus_WB     Non-Sanity
    [Timeout]  5 min 00 seconds
    [Setup]  server Connect
    Step  1  check Sensor Alarm On Page5 Cronus  low critical  Voltage sensor
    Step  2  restore Threshold on Page5 Cronus  low critical  Voltage sensor
    [Teardown]  Run Keywords  Server Disconnect

#CONSR-SEST-SPCK-0043-0001
#    [Documentation]  Threshold Out Diagnostic Pages(05h) - Voltage LW
#    [Tags]     CONSR-SEST-SPCK-0043-0001  Cronus_WB     Non-Sanity
#    [Timeout]  5 min 00 seconds
#    [Setup]  server Connect
#    Step  1  check Sensor Alarm On Page5 Cronus  low warning  Voltage sensor
#    Step  2  restore Threshold on Page5 Cronus  low warning  Voltage sensor
#    [Teardown]  Run Keywords  Server Disconnect

CONSR-SEST-SPCK-0061-0001
    [Documentation]  This test case checks Log Status Diagnostic Page (13h) - page status
    [Tags]     CONSR-SEST-SPCK-0061-0001  Cronus_WB
    [Timeout]  5 min 00 seconds
    [Setup]    server Connect
    Step  1    send a command  ${Page13_run_diag_command}
    Step  2    verify Page Status  ${page_13_status_cmd}
    [Teardown]  Server Disconnect

CONSR-SEST-SPCK-0062-0001
    [Documentation]  This test checks Log Control Diagnostic Page (13h) - Get Log Entry Descriptor
    [Tags]  CONSR-SEST-SPCK-0062-0001  Cronus_WB
    [Timeout]  5 min 00 seconds
    [Setup]  server Connect
    Step  1    get Control Decscriptor Information   ${page_13_entries_num_cmd}
    Step  2    Verify log pattern   ${page_13_status_cmd}  ${log_entry_code}  ${clear_log_entry_pattern}
    Step  3    get Control Decscriptor Information   ${page_13_clear_log_cmd}
    Step  4    Verify log pattern   ${page_13_status_cmd}  ${clear_log_entry_code}  ${clear_log_entry_pattern}
    Step  5    CLI check for log entry
    [Teardown]  Server Disconnect

CONSR-SEST-SPCK-0063-0001
    [Documentation]  This test checks Log Status Diagnostic Page (13h)
    [Tags]  CONSR-SEST-SPCK-0063-0001  Cronus_WB
    [Timeout]  5 min 00 seconds
    [Setup]  server Connect
    Step  1    send a command  ${Page13_run_diag_command}
    Step  2    verify Page Status  ${page_13_status_cmd}
    [Teardown]  Server Disconnect

CONSR-SEST-SCSI-0006-0001
    [Documentation]  SES Support Diagnostic Page
    [Tags]     CONSR-SEST-SCSI-0006-0001    Cronus_WB
    [Timeout]  5 min 00 seconds
    Step  1  server Connect
    Step  2  check Command Sent Athena  sg_ses  ${fail_dict}
    Step  3  Server Disconnect

CONSR-SEST-SCSI-0007-0001
    [Documentation]  This test checks Ensure send SES control commands to the CLS SES firmware successfully
    [Tags]     CONSR-SEST-SCSI-0007-0001  Cronus_WB    Regression
    [Timeout]  5 min 00 seconds
    [Setup]    get dut variable
    Step  1    server Connect
    Step  2    set control bits via raw data
    Step  3  Server Disconnect

CONSR-SEST-SCSI-0012-0001
    [Documentation]  SCSI Support Diagnostic Page - Log Select
    [Tags]     CONSR-SEST-SCSI-0012-0001  Cronus_WB     Non-Sanity
    [Timeout]  5 min 00 seconds
    [Setup]     server Connect
    Step  1     check SCISI Elements  ${set_log_sense_cmd}  ${set_log_sense_pattern}
    [Teardown]  Server Disconnect

CONSR-SEST-DRMT-0007-0001
    [Documentation]  This test checks Drive Disk Power On/Off Check - SES01001
    [Tags]     CONSR-SEST-DRMT-0007-0001   Cronus_WB
    [Timeout]  5 min 00 seconds
    [Setup]  get dut variable
    Step  1    server Connect
    Step  2  check Disk Power Off
    Step  3  Server Disconnect

CONSR-SEST-SPCK-0060-0001
    [Documentation]  This test case checks Log Control/Status Diagnostic Page (13h)
    [Tags]     CONSR-SEST-SPCK-0060-0001  Cronus_WB
    [Timeout]  5 min 00 seconds
    [Setup]    server Connect
    Step  1    send a command   ${page13_readlog_cmd}
    Step  2    compare log info with CLI Cronus   ${page_13_status_cmd}
    [Teardown]  Server Disconnect


CONSR-SEST-DRMT-0006-0001
    [Documentation]  This test checks Drive PHY Control
    [Tags]    CONSR-SEST-DRMT-0006-0001    Cronus_WB
    [Timeout]  10 min 00 seconds
    [Setup]    server Connect
    Step  1    verify PHY enable disable Cronus
    [Teardown]  Server Disconnect

CONSR-SEST-IVMT-0014-0001
    [Documentation]  This test case checks PSU 0 Inventory - page 07h
    [Tags]     CONSR-SEST-IVMT-0014-0001  Cronus_WB
    [Timeout]  5 min 00 seconds
    [Setup]    server Connect
    Step  1    compare PSU status with CLI Cronus  ${psu0_Find_pattern}   ${psu0_status_pg7_cmd}  ${PSU1}
    [Teardown]  Server Disconnect

CONSR-SEST-IVMT-0011-0001
    [Documentation]  This test case checks PSU 1 status - page 02h
    [Tags]     CONSR-SEST-IVMT-0011-0001  Cronus_WB
    [Timeout]  5 min 00 seconds
    [Setup]    server Connect
    Step  1    check PSU status  ${psu1_status_pg2_cmd}  ${psu125_status_pg2_pattern_cronus}
    Step  2    CLI check for psu status  ${psu1_cli_pattern_cronus}
    [Teardown]  Server Disconnect

CONSR-SEST-IVMT-0010-0001
    [Documentation]  This test case checks PSU 0 status - page 02h
    [Tags]    CONSR-SEST-IVMT-0010-0001  Cronus_WB
    [Timeout]  5 min 00 seconds
    [Setup]    server Connect
    Step  1    check PSU status  ${psu0_status_pg2_cmd}  ${psu034_status_pg2_pattern}
    Step  2    CLI check for psu status  ${psu0_cli_pattern_cronus}
    [Teardown]  Server Disconnect

CONSR-SEST-IVMT-0008-0001
    [Documentation]  This test checks the enclosure Inventory - page 07h
    [Tags]   CONSR-SEST-IVMT-0008-0001   Cronus_WB
    [Timeout]  5 min 00 seconds
    [Setup]    server Connect
    Step  1    Verify Enclosure Inventory details on CLI and page command cronus  ${Inventory_ses_cmd}  ${Inventory_CLI_cmd}
    [Teardown]  Server Disconnect

CONSR-SEST-IVMT-0007-0001
    [Documentation]  This test checks enclosure status - page 02h
    [Tags]   CONSR-SEST-IVMT-0007-0001   Cronus_WB
    [Timeout]  8 min 00 seconds
    [Setup]    server Connect
    Step  1    check Command Pattern   ${pg2_enc_status_cmd}  ${pg2_enc_status_cronus}
    [Teardown]  Server Disconnect

CONSR-SEST-IVMT-0003-0001
    [Documentation]  This test case Check the canister A Inventory - page 07h
    [Tags]     CONSR-SEST-IVMT-0003-0001   Cronus_WB
    [Timeout]  5 min 00 seconds
    [Setup]    server Connect
    Step  1    Verify canister details on CLI and page command  ${canister_a_ses_cmd}  ${canister_CLI_cmd}
    [Teardown]  Server Disconnect

CONSR-SEST-IVMT-0001-0001
    [Documentation]  This test case checks the canister A status - page 02h
    [Tags]   CONSR-SEST-IVMT-0001-0001   Cronus_WB
    [Timeout]  5 min 00 seconds
    [Setup]    server Connect
    Step  1    verify cansiter status and FW version    ${page02_canisterA_cmd}    ${canisterA_status}
    [Teardown]  Server Disconnect

CONSR-SEST-SCSI-0001-0001
    [Documentation]  Test Unit Ready
    [Tags]     CONSR-SEST-SCSI-0001-0001  Cronus_WB
    [Timeout]  5 min 00 seconds
    [Setup]     server Connect
    Step  1     check SCISI Elements  ${check_scsi_ready_cmd}  ${scsi_ready_pattern}
    [Teardown]  Server Disconnect

CONSR-SEST-SCSI-0003-0001
    [Documentation]  SES Support Diagnostic Page - VPD 00h(Supported VPD)
    [Tags]     CONSR-SEST-SCSI-0003-0001  Cronus_WB
    [Timeout]  5 min 00 seconds
    [Setup]     server Connect
    Step  1     check SCISI Elements  ${sg_inquiry_page_0x00_cmd}  ${sg_inquiry_page_0x00_pattern}
    [Teardown]  Server Disconnect

CONSR-SEST-SCSI-0004-0001
    [Documentation]  SES Support Diagnostic e - VPD 80h(Unit Serial Number)
    [Tags]     CONSR-SEST-SCSI-0004-0001  Cronus_WB
    [Timeout]  5 min 00 seconds
    [Setup]     server Connect
    Step  1     check Enclosure Length  ${sg_inquiry_page_0x80_cmd}  ${cronus_sg_inquiry_pattern}
    ...         ${cronus_sg_inquiry_length}
    [Teardown]  Server Disconnect

CONSR-SEST-SCSI-0005-0001
    [Documentation]  SES Support Diagnostic Page - VPD 83h(Device Identication)
    [Tags]     CONSR-SEST-SCSI-0005-0001  Cronus_WB
    [Timeout]  5 min 00 seconds
    [Setup]     server Connect
    Step  1     check SCISI Elements  ${sg_inquiry_page_0x83_cmd}  ${sg_inquiry_page_0x83_pattern}
    [Teardown]  Server Disconnect

CONSR-SEST-SCSI-0011-0001
  [Documentation]  This test checks SCSI Support Diagnostic Page - Read Buffer
  [Tags]   CONSR-SEST-SCSI-0011-0001   Cronus_WB
  [Timeout]  5 min 00 seconds
  Step  1  server Connect
  Step  2  verify read buffer
  Step  3  Server Disconnect

CONSRS-SM-01-0001
    [Documentation]  This test checks SMP General Commands
    [Tags]    CONSRS-SM-01-0001   Cronus_WB
    [Timeout]  5 min 00 seconds
    [Setup]    server Connect
    Step  1    verify SMP commands Cronus
    [Teardown]  Server Disconnect

CONSR-SEST-SCSI-0015-0001
    [Documentation]  SCSI Support Diagnostic Page - Mode Select (Protocol Specific Port Mode Page)
    [Tags]     CONSR-SEST-SCSI-0015-0001  Cronus_WB
    [Timeout]  5 min 00 seconds
    [Setup]     server Connect
    Step  1     check Command Sent  ${select_protocol_specific_mode_cmd}  ${fail_dict}
    [Teardown]  Run Keywords  Server Disconnect
           ...  AND Disconnect

CONSR-SEST-SCSI-0016-0001
    [Documentation]  SCSI Support Diagnostic Page - MODE SENSE (18h)
    [Tags]     CONSR-SEST-SCSI-0016-0001   Cronus_WB
    [Timeout]  5 min 00 seconds
    [Setup]     server Connect
    Step  1     check Command Pattern  ${mode_sense_page18_cmd}  ${mode_sense_page18_pattern}
    [Teardown]  Server Disconnect

CONSR-SEST-SCSI-0017-0001
    [Documentation]  SCSI Support Diagnostic Page - MODE SENSE (19h)
    [Tags]     CONSR-SEST-SCSI-0017-0001  Cronus_WB
    [Timeout]  5 min 00 seconds
    [Setup]     server Connect
    Step  1     check Command Pattern  ${mode_sense_page19_cmd}  ${mode_sense_page19_pattern_cronus}
    [Teardown]  Server Disconnect

CONSR-SEST-SCSI-0018-0001
    [Documentation]  SCSI Support Diagnostic Page - MODE SENSE (3Fh:00)
    [Tags]     CONSR-SEST-SCSI-0018-0001  Cronus_WB
    [Timeout]  5 min 00 seconds
    [Setup]     server Connect
    Step  1     check Command Pattern  ${mode_sense_page3Fh_00_cmd}  ${mode_sense_page3Fh_00_pattern_titan_g2_wb}
    [Teardown]  Server Disconnect

CONSR-SEST-SCSI-0019-0001
    [Documentation]  SCSI Support Diagnostic Page - MODE SENSE  (3Fh:FF)
    [Tags]     CONSR-SEST-SCSI-0019-0001   Cronus_WB
    [Timeout]  5 min 00 seconds
    [Setup]     server Connect
    Step  1     check Command Pattern  ${mode_sense_page3Fh_ff_cmd}  ${mode_sense_page3Fh_ff_pattern_cronus}
    [Teardown]  Server Disconnect

CONSR-SEST-SCSI-0020-0001
  [Documentation]  This test checks SCSI Support page-Report LUNs
  [Tags]   CONSR-SEST-SCSI-0020-0001  Cronus_WB
  [Timeout]  5 min 00 seconds
  Step  1  server Connect
  Step  2  verify report luns
  Step  3  Server Disconnect

CONSR-SEST-CMDL-0002-0001
    [Documentation]  This test checks detailed CLI command setting and getting test
    [Tags]    CONSR-SEST-CMDL-0002-0001     Cronus_WB
    [Timeout]  3 min 00 seconds
    [Setup]    server Connect
    Step  1    verify CLI set get CLI command
    [Teardown]  Server Disconnect

CONSR-SEST-SPCK-0105-0001
  [Documentation]  This test checks Timestamp Set Diagnostic Page (11h) --- Get status page
  [Tags]  CONSR-SEST-SPCK-0105-0001   Cronus_WB
  [Timeout]  10 min 00 seconds
  Step  1  server Connect
  Step  2  Timestamp Set Diagnostic Page (11h) --- Get status page
  Step  3  Server Disconnect

CONSRS-DP-02-0001_1
    [Documentation]  This test checks Drive Disk Power On/Off Check - SES01002
    [Tags]    CONSRS-DP-02-0001_1   Cronus_WB
    [Timeout]  8 min 00 seconds
    [Setup]    server Connect
    Step  1    verify drive disk power on_off Cronus
    [Teardown]  Server Disconnect

CONSR-SEST-IVMT-0015-0001
    [Documentation]  This test checks Drive Inventory - SES010001
    [Tags]    CONSR-SEST-IVMT-0015-0001   Cronus_WB
    [Timeout]  8 min 00 seconds
    [Setup]    server Connect
    Step  1   Verify drive inventory check
    [Teardown]  Server Disconnect

CONSR-SEST-DRMT-0009-0001
    [Documentation]  This test checks Drive Disk Temperature Check
    [Tags]    CONSR-SEST-DRMT-0009-0001  Cronus_WB
    [Timeout]  8 min 00 seconds
    [Setup]    server Connect
    Step  1  Verify drives temp check
    [Teardown]  Server Disconnect

CONSR-SEST-DRMT-0004-0001
    [Documentation]  This test checks port mapping tables from Drive Board VPD and firmware configuration
    [Tags]    CONSR-SEST-DRMT-0004-0001  Cronus_WB
    [Timeout]  8 min 00 seconds
    [Setup]    server Connect
    Step  1  verify port mapping tables
    [Teardown]  Server Disconnect

CONSR-SEST-SPCK-0072-0001
    [Documentation]  SES Threshold Control Page -Voltage - UC
    [Tags]     CONSR-SEST-SPCK-0072-0001  Cronus_WB
    [Timeout]  5 min 00 seconds
    [Setup]     server Connect
    Step  1     check Default Sensor Alarm On Page5 for V11 sensor Cronus  high critical  Voltage sensor
    Step  2     Run Keyword And Continue On Failure  Threshold Control Page Cronus (Voltage UC)
    Step  3     Run Keyword And Continue On Failure  get_power_and_threshold_status
    Step  4     restore Threshold on Page5 Cronus  high critical  Voltage sensor 
    [Teardown]  Server Disconnect

CONSR-SEST-SPCK-0073-0001
    [Documentation]  This test will test SES Threshold Control Page -Voltage - LC
    [Tags]  CONSR-SEST-SPCK-0073-0001  Cronus_WB  Regression
    Step  1  server Connect
    Step  2  check Default Sensor Alarm On Page5 Cronus  low critical  Voltage sensor
    Step  3  Run Keyword And Continue On Failure  Threshold Control Page Cronus (Voltage LC)
    Step  4  Run Keyword And Continue On Failure  check_power_and_threshold_status
    Step  5  restore Threshold on Page5 Cronus  low critical  Voltage sensor
    [Teardown]  Server Disconnect

CONSR-SEST-DISCOVERY-0001-0001
    [Documentation]  This test will test the canisters are properly discovered in Cronus enclosure
    [Tags]     CONSR-SEST-DISCOVERY-0001-0001   Cronus_WB    Regression
    [Timeout]  5 min 00 seconds
    [Setup]     server Connect
    Step  1     check allsasadd
    [Teardown]  Server Disconnect

CONSR-SEST-DISCOVERY-0003-0001
    [Documentation]  This test checks the array device disk status - page 02h
    [Tags]   CONSR-SEST-DISCOVERY-0003-0001  Cronus_WB
    [Timeout]  5 min 00 seconds
    [Setup]    server Connect
    Step  1   check driver status Cronus  ${page_drvstatus_cmd}  ${drv0_11}  ${OK_status_cronus_wb}  
    Step  2   Verify drive inventory check
    [Teardown]  Server Disconnect

CONSR-SEST-IVMT-0012-0001
    [Documentation]  This test case checks PSU 0 status - page 07h
    [Tags]     CONSR-SEST-IVMT-0012-0001  Cronus_WB
    [Timeout]  5 min 00 seconds
    [Setup]    server Connect
    Step  1    compare PSU status with CLI Cronus  ${psu0_Find_pattern_cronus}   ${psu0_status_pg7_cmd}  ${PSU1}
    [Teardown]  Server Disconnect

CONSR-SEST-IVMT-0013-0001
    [Documentation]  This test case checks PSU 1 Inventory - page 07h
    [Tags]     CONSR-SEST-IVMT-0013-0001  Cronus_WB
    [Timeout]  5 min 00 seconds
    [Setup]    server Connect
    Step  1    check Command Pattern  ${psu1_status_pg7_cmd}  ${psu1_status_pg7_pattern}
    Step  2    CLI check for psu status  ${psu1_cli_pattern_cronus}
    [Teardown]  Server Disconnect

CONSR-SEST-SPCK-0041-0001
    [Documentation]  SES Threshold Control Page -Voltage - LW
    [Tags]     CONSR-SEST-SPCK-0041-0001  Cronus_WB
    [Timeout]  5 min 00 seconds
    [Setup]     server Connect
    Step  1     check Default Sensor Alarm On Page5 Cronus  low warning  Voltage sensor
    Step  2     Run Keyword And Continue On Failure  Threshold Control Page Cronus (Voltage LW)
    Step  4     restore Threshold on Page5 Cronus  low warning  Voltage sensor
    [Teardown]  Server Disconnect

CONSR-SEST-SPCK-0043-0001
    [Documentation]  SES Threshold Control Page -Voltage - OW
    [Tags]     CONSR-SEST-SPCK-0043-0001  Cronus_WB
    [Timeout]  5 min 00 seconds
    [Setup]     server Connect
    Step  1     check Default Sensor Alarm On Page5 for V6 Sensor Cronus  high warning  Voltage sensor
    Step  2     Run Keyword And Continue On Failure  Threshold Control Page Cronus (Voltage OW)
    Step  4     restore Threshold on Page5 Cronus  high warning  Voltage sensor
    [Teardown]  Server Disconnect

CONSR-SEST-SPCK-0033-0001
  [Documentation]  This test checks String Out Diagnostic Pages(04h)--Altitude configuration
  [Tags]   CONSR-SEST-SPCK-0033-0001   Cronus_WB
  [Timeout]  10 min 00 seconds
  [Setup]    get dut variable
  Step  1  server Connect
  Step  2  check Altitude configuration Cronus 
  Step  3  Server Disconnect

*** Keywords ***
OS Connect Device
    OSConnect

OS Disconnect Device
    OSDisconnect


