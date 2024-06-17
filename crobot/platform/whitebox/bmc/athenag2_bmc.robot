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
# Script       : athenag2_bmc.robot                                                                                   #
# Date         : March 06, 2022                                                                                       #
# Author       : Nataraj A <nataraja@celestica.com>                                                                   #
# Description  : This script will validate athena G2 BMC                                                              #
#                                                                                                                     #
# Script Revision Details:                                                                                            #
#   Initial Draft for athenag2 bmc testing                                                                            #
#######################################################################################################################

*** Settings ***
Documentation       Tests to verify athenag2 BMC functions described in the BMC function SPEC for the whiteboxproject.

# Force Tags        BMC
Variables         BMC_variable.py
Library           ../WhiteboxLibAdapter.py
Library           whitebox_lib.py
Library           bmc_lib.py
Library           bios_menu_lib.py
Library           ../ses/ses_lib.py

Resource          BIOS_keywords.robot
Resource          BMC_keywords.robot
Resource          CommonResource.robot

#Suite Setup       OS Connect Device
#Suite Teardown    OS Disconnect Device
** Variables ***
# It is recommended to use <{ScriptName}|{FeatureName}|{DomainName}_Variable> file for variable declaration with help of
# setting table. This section should keep blank.
#In extreme case if script requires variable then it should be defined in this table with documentaiton tag

*** Test Cases ***
# *** comment ***
CONSR-BMCT-BSFC-0008-0001
    [Documentation]  This test checks the Function_008_Power Restore Policy 
    [Tags]  CONSR-BMCT-BSFC-0008-0001  Athena-G2
    [Timeout]  20 min 00 seconds
    [Setup]  OS Connect Device
    ${ip}  get_ip_address_from_ipmitool  DUT
    Step  1  Change Power Restore Policy Status  DUT  ${ip}  ${set_power_restore_policy1}  ${expectedvalue}
    Step  2  Verify Power Restore status  DUT  ${ip}  ${exp_restorepolicy_status1}  ${exp_chassispower_status1}
    Step  3  Powercycle Pdu1  DUT 
    Step  4  Sleep  300
    Step  5  Verify Power Restore status  DUT  ${ip}  ${exp_restorepolicy_status1}  ${exp_chassispower_status2}
    Step  6  Change Power Restore Policy Status  DUT  ${ip}  ${set_power_restore_policy2}  ${expectedvalue}
    Step  7  Verify Power Restore status  DUT  ${ip}  ${exp_restorepolicy_status2}  ${exp_chassispower_status2}
    Step  8  Powercycle Pdu1  DUT 
    Step  9  Sleep  300
    Step  10  Verify Power Restore status  DUT  ${ip}  ${exp_restorepolicy_status2}  ${exp_chassispower_status2}  ${last_power_state}
    Step  11  Change Power Restore Policy Status  DUT  ${ip}  ${set_power_restore_policy3}  ${expectedvalue}
    Step  12  Verify Power Restore status  DUT  ${ip}  ${exp_restorepolicy_status3}  ${exp_chassispower_status2}
    Step  13  Power Up the unit  DUT  ${ip}  ${exp_chassispower_status1}
    [Teardown]  OS Disconnect Device

CONSR-BMCT-BSFC-0014-0001
   [Documentation]   SEL Time Check
   [Tags]   CONSR-BMCT-BSFC-0014-0001   Athena-G2

   Step  1   Set BMC SEL time and Check
   Step  2   Set the RTC time to current time and sync to hwclock
   Step  3   Check Time in BIOS
   Step  4   Check if BMC SEL time is synced
   Step  5   Trigger and event and check time in log
   Step  6   Warm reset BMC and then check BMC time
   Step  7   Reset SUT and boot to OS
   Step  8   AC cycle and then check the BMC time

CONSR-BMCT-BSFC-0009-0001
    [Documentation]  This test checks the Function_009_Sensor Summary Check
    [Tags]     CONSR-BMCT-BSFC-0009-0001  Athena-G2
    [Setup]     OS Connect Device
    ${ip}  get_ip_address_from_ipmitool  DUT
    Step  1  verify the sensor reading and check with funspec  DUT  ${ip}
    Step  2  verify IPMI Chassis Control to power offon  DUT  ${ip}  ${off_server}
    Step  3  verify the sensor reading and check with funspec  DUT  ${ip}
    Step  4  verify IPMI Chassis Control to power offon  DUT  ${ip}  ${on_server}
    Step  5  verify the sensor reading and check with funspec  DUT  ${ip}
    Step  6  verify IPMI command BMC coldreset  DUT  ${ip}
    Step  7  verify the sensor reading and check with funspec  DUT  ${ip}
    Step  8  Powercycle Pdu1  DUT
    Step  9  Sleep  300
    [Teardown]  OS Disconnect Device

CONSR-BMCT-BSFC-0017-0001
    [Documentation]  This test checks Inventory Management
    [Tags]  CONSR-BMCT-BSFC-0017-0001   Athena-G2
    [Timeout]  20 min 00 seconds
    Step  1   OS Connect Device
    Step  2   Check inventory details
    Step  3   OS Disconnect Device
    Step  4   ConnectESMB
    Step  5   Check inventory details
    Step  6   OS Disconnect Device

CONSR-BMCT-BHSI-0004-0001
    [Documentation]  BMC and Host System Interaction 1
    [Tags]  CONSR-BMCT-BHSI-0004-0001   Athena-G2

    Step  1  Verify Watchdog Timer for Power Cycle timeout action
    Step  2  Verify Watchdog Timer for hard reset timeout action
    Step  3  Verify Watchdog Timer for power down timeout action
    Step  4  Verify Watchdog Timer for no action

CONSR-BMCT-BHSI-0006-0001
    [Documentation]  This test checks BMC and Host System Interaction - Server Mgmt
    [Tags]   CONSR-BMCT-BHSI-0006-0001   Athena-G2
    [Timeout]  20 min 00 seconds
    Step  1   OS Connect Device
    Step  2   verify_BMC_self_test_status_version_log   DUT   ${BMC_Firmware_version}
    Step  3   Verify_BMC_fru_information
    Step  4   verify_system_event_log
    Step  5   OS Disconnect Device

CONSR-BMCT-BSFC-0012-0001
    [Documentation]  This test checks Function_012_SEL Summary Check
    [Tags]     CONSR-BMCT-BSFC-0012-0001  Athena-G2
    [Setup]     OS Connect Device
    ${ip}  get_ip_address_from_ipmitool  DUT
    Step  1  Verify event log SEL clear  DUT  ${ip}
    Step  2  Download Athena BMC FW image
    Step  3  Upgrade bmc FW
    Step  4  CheckinstalledBCMFWversion  DUT  Athena_FW_BMC_B  ${ip}  upgrade
    Step  5  Verify abnormal event log  DUT  ${ip}
    Step  6  Verify DC cycle BMC IP  DUT  ${ip}
    Step  7  Verify abnormal event log  DUT  ${ip}
    Step  8  Verify AC cycle BMC IP  DUT  ${ip}
    Step  9  Verify abnormal event log  DUT  ${ip}
    [Teardown]  OS Disconnect Device

CONSR-BMCT-FWUP-0012-0001
    [Documentation]  Firmware Update
    [Tags]   CONSR-BMCT-FWUP-0012-0001   Athena-G2
    [Setup]  Download Athena BMC image

    Step  1  Make SEL to contain full logs
    Step  2  Upgrade BMC using CFUFLASH Tool
    Step  3  Verify BMC version

    [Teardown]  Remove Athena FW image

CONSR-BMCT-SRTS-0007-0001
    [Documentation]  This test checks Stress Test - Read All fru VPD via bmc reset Stress
    [Tags]   CONSR-BMCT-SRTS-0007-0001     Athena-G2
    [Timeout]  20 min 00 seconds
    FOR    ${INDEX}    IN RANGE    ${MAXINDEX}
       Print Loop Info  ${INDEX}
       Step  1  OS Connect Device
       Step  2  verify fru vpd before and after cold reset
       Step  3  OS Disconnect Device
       Step  4  ConnectESMB
       Step  5  verify fru vpd before and after cold reset
       Step  6  OS Disconnect Device
    END

CONSR-BMCT-BHSI-0005-0001
    [Documentation]  This test checks BMC and Host System Interaction   Interaction_005_Boot Option
    [Tags]  CONSR-BMCT-BHSI-0005-0001   Athena-G2
    [Timeout]  50 min 00 seconds
    [Setup]     ConnectESMB
    ${ip}  get_ip_address_from_ipmitool  DUT
    Step  1  set boot device into BIOS Setup  ${ip}
    Step  2  Get the boot options  ${ip}
    Step  3  power cycle and check status  ${ip}  ${cmd_power_cycle_step}  ${TestSteps1}
    Step  4  verify_boot_sequence  DUT
    Step  5  power cycle and check status  ${ip}  ${cmd_power_cycle_step}  ${TestSteps2}
    FOR  ${index}  IN RANGE  0  3
       Print Loop Info  ${INDEX}
       Step  6  set boot device into BIOS Setup  ${ip}
       Step  7  Get the boot options  ${ip}
       Step  8  power cycle and check status  ${ip}  ${cmd_power_cycle_step}  ${TestSteps1}
       Step  9  verify_boot_sequence  DUT
    END    
    Step  10  enter_uefi_shell  DUT
    Step  11  set Force boot from default HDD single valid  ${ip}  ${cmd_single_valid}  ${cmd_single_valid_next}
    Step  12  power cycle and check status  ${ip}  ${cmd_power_cycle_step}  ${TestSteps10}
    Step  13  Check_unit_auto_boot_to_UEFI_PXE_page  DUT  ${validation1}
    Step  14  power reset and check status  ${ip}  ${TestSteps10_12}	
    Step  15  set Force boot from default HDD permanent  ${ip}  ${cmd_permanent_valid}  ${cmd_permanent_valid_next}
    Step  16  power cycle and check status  ${ip}  ${cmd_power_cycle_step}  ${TestSteps10}
    Step  17  Check_unit_auto_boot_to_UEFI_PXE_page  DUT  ${validation2}
    Step  18  power reset and check status  ${ip}  ${TestSteps10_12}
    Step  19  exit_uefi_shell    DUT
    Step  20  bios_menu_lib.revert_boot_order    DUT
    [Teardown]  OS Disconnect Device

CONSR-BMCT-BSFC-0023-0001
   [Documentation]   Function_024_OEM Command
   [Tags]   CONSR-BMCT-BSFC-0023-0001   Athena-G2
   [Setup]  OS Connect Device
   ${ip}  get_ip_address_from_ipmitool  DUT
   Step  1  verify command execution  DUT  ${ip}  ${Get_slots_alive}   ${fail_pattern}
   Step  2  verify command execution  DUT  ${ip}  ${Get_cpld_info}   ${fail_pattern}
   Step  3  verify command execution  DUT  ${ip}  ${Set_Drive_power}   ${fail_pattern}
   Step  4  verify command execution  DUT  ${ip}  ${Set_canister_power}   ${fail_pattern}
   Step  5  verify command execution  DUT  ${ip}  ${Get_canister_power}   ${fail_pattern}
   Step  6  verify command execution  DUT  ${ip}  ${Set_switch_bios}   ${fail_pattern}
   Step  7  verify command execution  DUT  ${ip}  ${Get_current_canister}   ${fail_pattern}
   Step  8  verify command execution  DUT  ${ip}  ${Get_BMC_memory}   ${fail_pattern}
   Step  9  verify command execution  DUT  ${ip}  ${Set_BMC_memory}   ${fail_pattern}
   [Teardown]  OS Disconnect Device

CONSR-BMCT-BSFC-0019-0001
   [Documentation]   Function_019_Fan Status Monitor
   [Tags]   CONSR-BMCT-BSFC-0019-0001  Athena-G2
   [Setup]  OS Connect Device
   ${ip}  get_ip_address_from_ipmitool  DUT
   Step  1  verify command execution  DUT  ${ip}  ${fan_type}   ${fail_pattern}
   Step  2  verify command execution  DUT  ${ip}  ${set_fan_control}   ${fail_pattern}
   Step  3  verify command execution  DUT  ${ip}  ${Get_fan_status}   ${fail_pattern}
   Step  4  verify command execution  DUT  ${ip}  ${fan_control_automatic}   ${fail_pattern}
   Step  5  verify command execution  DUT  ${ip}  ${all_fan_PWM}   ${fail_pattern}
   Step  6  verify command execution  DUT  ${ip}  ${Get_fan_status}   ${fail_pattern}
   [Teardown]  OS Disconnect Device

CONSR-BMCT-SRTS-0001-0001
    [Documentation]  This test Stress Test Stress_001_BMC Local Stress Test
    [Tags]  CONSR-BMCT-SRTS-0001-0001   Athena-G2
    [Timeout]  24 hours
    [Setup]     OS Connect Device
    FOR    ${INDEX}    IN RANGE    ${MAXINDEX}
       Print Loop Info  ${INDEX}
       ${ip}  get_ip_address_from_ipmitool  DUT
       Step  1  Verify BMC Version and ip address from ipmitoolinfo  ${ip}
       Step  2  Verify the SEL and ensure no error
       Step  3  Verify the sensor and check status  ${ip}
       Step  4  Run BMC cold reset
    END
    [Teardown]  OS Disconnect Device

CONSR-BMCT-SRTS-0008-0001
    [Documentation]  This test checks Bmc power cycle command Stress
    [Tags]  CONSR-BMCT-SRTS-0008-0001  Athena-G2
    [Timeout]   12 hours
    [Setup]     OS Connect Device
    ${ip}  get_ip_address_from_ipmitool  DUT
    OS Disconnect Device
    ${fru_output}       execute_local_cmd    ipmitool -I lanplus -H ${ip} -U admin -P admin fru
    ${mc_info_output}   execute_local_cmd    ipmitool -I lanplus -H ${ip} -U admin -P admin mc info
    FOR    ${INDEX}    IN RANGE    ${MAXINDEX}
        Print Loop Info  ${INDEX}
        Step  1  Verify AC cycle BMC IP  DUT  ${ip}
        Step  2  Sleep  30
        Step  3  verify fru mc info  ${ip}   ${fru_output}     ${mc_info_output}
    END

CONSR-BMCT-SRTS-0014-0001
    [Documentation]  This test checks BMC remote Cold Reset Stress
    [Tags]  CONSR-BMCT-SRTS-0014-0001    Athena-G2
    [Timeout]   12 hours
    [Setup]     OS Connect Device
    ${ip}  get_ip_address_from_ipmitool  DUT
    OS Disconnect Device
    FOR    ${INDEX}    IN RANGE    ${MAXINDEX}
        Print Loop Info  ${INDEX}
        Step  1  verify IPMI commands  ${ip}
        Step  2  verify IPMI command BMC coldreset  DUT  ${ip}
        Step  3  Sleep  200
    END

CONSR-BMCT-SRTS-0002-0001
    [Documentation]  This test checks Stress_002_BMC FW Update Stress Test (Local)
    [Tags]     CONSR-BMCT-SRTS-0002-0001  Athena-G2
    [Timeout]  24 hours
    [Setup]     OS Connect Device
    FOR    ${INDEX}    IN RANGE    ${MAXINDEX}
       Print Loop Info  ${INDEX}
       Step  1  Download and verify BMC FW image  upgrade
       Step  2  Download and verify BMC FW image  downgrade
    END
    [Teardown]  OS Disconnect Device

CONSR-BMCT-SRTS-0005-0001
    [Documentation]  This test Stress_005_SOL Connection Stress Test
    [Tags]     CONSR-BMCT-SRTS-0005-0001  Athena-G2
    [Timeout]  24 hours
    [Setup]     OS Connect Device
    ${ip}  get_ip_address_from_ipmitool  DUT
    ${installed_BMC_Version}  get_bmc_version_ipmitool  DUT  ${ip}
    ${BIOS_info_output_before_SOL_active} =   execute_Linux_command  dmidecode -t 0   
    Step  1  get_SOL_info_remote_client  DUT  ${ip}  true
    Step  2  set_SOL_looptest  DUT  ${ip}  ${testloopcycle}
    Step  3  verify SOL Function  ${ip}  ${BIOS_info_output_before_SOL_active} 
    [Teardown]  OS Disconnect Device

CONSR-BMCT-FWUP-0002-0001
    [Documentation]  This test checks FWFlash_BIOS Firmware Update
    [Tags]  CONSR-BMCT-FWUP-0002-0001    Athena-G2
    [Timeout]   12 hours
    [Setup]     Prepare images of multiple versions
    Step  1  upgrade_downgrade_bios_FW     Athena_BIOS_Versions_A   oldImage  V3
    Step  2  upgrade_downgrade_bios_FW     Athena_BIOS_Versions_A   newImage  NV
    Step  3  upgrade_downgrade_bios_FW_remoteOS    Athena_BIOS_Versions_A   oldImage  V3
    Step  4  upgrade_downgrade_bios_FW_remoteOS     Athena_BIOS_Versions_A   newImage  NV
    Step  5  Sleep  60
    [Teardown]  remove Athena_G2 BIOS images

CONSR-BMCT-RDFT-0113-0001
    [Documentation]  Event Destination Collection_1
    [Tags]  CONSR-BMCT-RDFT-0113-0001    Athena-G2

    Step  1  Verify event sevice subscriptions info show up correctly

CONSR-BMCT-RDFT-0001-0001
    [Documentation]  This test checks Redfish   Service Root
    [Tags]   CONSR-BMCT-RDFT-0001-0001  Athena-G2
    [Timeout]   20 min 00 seconds
    Step  1   Verify service root property

CONSR-BMCT-RDFT-0002-0001
    [Documentation]  This test checks Redfish   Computer System Collection_1
    [Tags]   CONSR-BMCT-RDFT-0002-0001     Athena-G2
    [Timeout]   20 min 00 seconds
    Step  1   Verify service system property

CONSR-BMCT-RDFT-0004-0001
    [Documentation]  This test checks Redfish   Computer System_1
    [Tags]   CONSR-BMCT-RDFT-0004-0001   Athena-G2
    [Timeout]   20 min 00 seconds
    Step  1   Verify system instance property

CONSR-BMCT-RDFT-0009-0001
    [Documentation]  This test checks Redfish   BootOption Collection
    [Tags]   CONSR-BMCT-RDFT-0009-0001   Athena-G2
    [Timeout]   20 min 00 seconds
    [Setup]    OS Connect Device
    Step  1   Verify collections   ${resource_boot_options_collections}
    [TearDown]   OSDisconnect

CONSR-BMCT-RDFT-0012-0001
    [Documentation]  This test checks Redfish   Memory_1
    [Tags]   CONSR-BMCT-RDFT-0012-0001    Athena-G2
    [Timeout]   20 min 00 second
    [Setup]    OS Connect Device
    Step  1    Verify collections  ${resource_memory_options_collections}
    [TearDown]   OSDisconnect

CONSR-BMCT-RDFT-0150-0001
    [Documentation]  UpdateService_2
    [Tags]   CONSR-BMCT-RDFT-0150-0001  Athena-G2
    [Setup]     OS Connect Device

    Step  1   Set UpdateService ServiceEnabled to False
    Step  2   Check UpdateService ServiceEnabled value as False
    Step  3   Set UpdateService ServiceEnabled to True
    Step  4   Check UpdateService ServiceEnabled value as True

    [Teardown]   OS Disconnect Device

CONSR-BMCT-RDFT-0056-0001
    [Documentation]  This test checks Redfish Log Service_13
    [Tags]  CONSR-BMCT-RDFT-0056-0001    Athena-G2
    [Setup]     OS Connect Device

    Step  1  Verify service enable can be changed to False successfully
    [Teardown]   OS Disconnect Device

CONSR-BMCT-RDFT-0114-0001
    [Documentation]  Event Destination Collection_2
    [Tags]   CONSR-BMCT-RDFT-0114-0001  Athena-G2
    [Setup]     OS Connect Device

    Step  1   Create a new EventService Subscription and Verify

    [Teardown]   OS Disconnect Device

CONSR-BMCT-RDFT-0057-0001
    [Documentation]  This test checks Redfish Log Service_14
    [Tags]  CONSR-BMCT-RDFT-0057-0001    Athena-G2
    [Setup]     OS Connect Device
    Step  1  Verify time can be changed successfully
    Step  2  Verify time offset can be changed successfully
    [Teardown]   OS Disconnect Device

CONSR-BMCT-RDFT-0116-0001
    [Documentation]  Event Destination_2
    [Tags]   CONSR-BMCT-RDFT-0116-0001  Athena-G2
    [Setup]     OS Connect Device

    Step  1   Delete the previously created EventService Subscription

    [Teardown]   OS Disconnect Device

CONSR-BMCT-RDFT-0038-0001
    [Documentation]  This test checks Simple Storage Collection
    [Tags]   CONSR-BMCT-RDFT-0038-0001    Athena-G2
    [Timeout]   20 min 00 seconds
    Step  1    Verify storage collections

CONSR-BMCT-RDFT-0039-0001
    [Documentation]  This test checks Simple Storage
    [Tags]   CONSR-BMCT-RDFT-0039-0001    Athena-G2
    [Timeout]   20 min 00 seconds
    Step  1    Verify simple storage

CONSR-BMCT-RDFT-0040-0001
    [Documentation]  This test checks LogServiceCollection_1
    [Tags]   CONSR-BMCT-RDFT-0040-0001   Athena-G2
    [Timeout]   20 min 00 seconds
    Step  1    Verify log service collection

CONSR-BMCT-RDFT-0041-0001
    [Documentation]  This test checks LogServiceCollection_2
    [Tags]   CONSR-BMCT-RDFT-0041-0001   Athena-G2
    [Timeout]   20 min 00 seconds
    Step  1    Verify log service collection_2

CONSR-BMCT-RDFT-0115-0001
    [Documentation]  Event Destination_1
    [Tags]   CONSR-BMCT-RDFT-0115-0001    Athena-G2
    [Setup]     OS Connect Device

    Step  1   Modify the context of previously created EventService Subscription

    [Teardown]   OS Disconnect Device

CONSR-BMCT-RDFT-0060-0001
    [Documentation]  This test checks Redfish LogEntry Collection_3
    [Tags]  CONSR-BMCT-RDFT-0060-0001    Athena-G2
    [Setup]     OS Connect Device
    Step  1  Verify BMC Log ID entries successfully
    [Teardown]   OS Disconnect Device

CONSR-BMCT-RDFT-0015-0001
    [Documentation]  This test checks Redfish   Processor Collection_1
    [Tags]   CONSR-BMCT-RDFT-0015-0001    Athena-G2
    [Timeout]   20 min 00 second
    [Setup]     OS Connect Device
    Step  1    Verify collections   ${resource_processor_collections}
    [TearDown]   OSDisconnect

CONSR-BMCT-RDFT-0019-0001
    [Documentation]  This test checks Redfish   Ethernet Interface Collection_1
    [Tags]   CONSR-BMCT-RDFT-0019-0001   Athena-G2
    [Timeout]   20 min 00 second
    [Setup]     OS Connect Device
    Step  1    Verify collections   ${resource_Ethernet_interface_collections}
    [TearDown]   OSDisconnect

CONSR-BMCT-RDFT-0043-0001
    [Documentation]  This test checks Redfish   Redfish LogServiceCollection_4
    [Tags]   CONSR-BMCT-RDFT-0043-0001  Athena-G2
    [Timeout]   20 min 00 second
    [Setup]     OS Connect Device
    Step  1    Verify collections   ${resource_LogService_chassis}
    [TearDown]   OSDisconnect

CONSR-BMCT-RDFT-0010-0001
    [Documentation]  This test checks Redfish   BootOption_1
    [Tags]   CONSR-BMCT-RDFT-0010-0001    Athena-G2
    [Timeout]   20 min 00 second
    Step  1  verify BootOption_1  ${resource_bootoption1_1}
    Step  2  verify BootOption_1  ${resource_bootoption1_2}
    Step  3  verify BootOption_1  ${resource_bootoption1_3} 
    Step  4  verify BootOption_1  ${resource_bootoption1_4}

CONSR-BMCT-RDFT-0030-0001
    [Documentation]  This test checks Redfish   Ethernet Interface Collection_12
    [Tags]   CONSR-BMCT-RDFT-0030-0001   Athena-G2
    [Timeout]   20 min 00 second
    [Setup]     OS Connect Device
    Step  1    Verify collections   ${resource_Ethernet_Interface_Collection_12}
    [TearDown]   OSDisconnect

CONSR-BMCT-RDFT-0064-0001
    [Documentation]  This test checks Redfish LogEntry Collection_7
    [Tags]  CONSR-BMCT-RDFT-0064-0001    Athena-G2
    [Setup]     OS Connect Device
    Step  1  Verify LogEntry Collection_7
    [Teardown]   OS Disconnect Device

CONSR-BMCT-RDFT-0216-0001
    [Documentation]  This test checks Redfish ResourceBlocksCollection
    [Tags]  CONSR-BMCT-RDFT-0216-0001   Athena-G2
    [Setup]     ConnectESMB
    Step  1  Verify composition service resource block info show up correctly
    [Teardown]   OS Disconnect Device

CONSR-BMCT-RDFT-0217-0001
    [Documentation]  This test checks Redfish ResourceBlocks_1
    [Tags]  CONSR-BMCT-RDFT-0217-0001   Athena-G2
    [Setup]     ConnectESMB
    Step  1  Verify computeBlock resource block info show up correctly
    Step  2  Verify drivesblock resource block info show up correctly
    Step  3  Verify networkBlock resource block info show up correctly
    [Teardown]   OS Disconnect Device

CONSR-BMCT-RDFT-0117-0001
    [Documentation]  Event Destination_3 - Do POST and DELETE once again
    [Tags]   CONSR-BMCT-RDFT-0117-0001  Athena-G2
    [Setup]     OS Connect Device

    Step  1   Create a new EventService Subscription and Verify
    Step  2   Verify GET operation on the previously created EventService Subscription doesnt work after DELETE

    [Teardown]   OS Disconnect Device

CONSR-BMCT-RDFT-0218-0001
    [Documentation]  This test checks Redfish ResourceBlocks_2
    [Tags]  CONSR-BMCT-RDFT-0218-0001   Athena-G2
    [Setup]     OS Connect Device
    Step  1  Set ComputeBlock CompositionStatus Reserved to False
    Step  2  Verify ComputeBlock CompositionStatus Reserved value as False
    Step  3  Set DrivesBlock CompositionStatus Reserved to False
    Step  4  Verify DrivesBlock CompositionStatus Reserved value as False
    Step  5  Set NetworkBlock CompositionStatus Reserved to False
    Step  6  Verify NetworkBlock CompositionStatus Reserved value as False
    [Teardown]   OS Disconnect Device

CONSR-BMCT-RDFT-0214-0001
    [Documentation]  This test checks Redfish CompositionService_1
    [Tags]  CONSR-BMCT-RDFT-0214-0001   Athena-G2
    [Setup]     OS Connect Device
    Step  1  Verify composition service info show up correctly    
    [Teardown]   OS Disconnect Device

CONSR-BMCT-RDFT-0215-0001
    [Documentation]  CompositionService_2
    [Tags]   CONSR-BMCT-RDFT-0215-0001  Athena-G2
    [Setup]     OS Connect Device
    Step  1   Set CompositionService ServiceEnabled to False
    Step  2   Verify CompositionService ServiceEnabled value as False
    Step  3   Set CompositionService ServiceEnabled to True
    Step  4   Verify CompositionService ServiceEnabled value as True
    [Teardown]   OS Disconnect Device

CONSR-BMCT-RDFT-0212-0001
    [Documentation]  This test checks Redfish Telemetry LogEntry Collection
    [Tags]  CONSR-BMCT-RDFT-0212-0001   Athena-G2
    [Setup]     OS Connect Device
    Step  1  Verify telemetry service log service entries info show up correctly
    [Teardown]   OS Disconnect Device

CONSR-BMCT-RDFT-0210-0001
    [Documentation]  This test checks Redfish Telemetry LogService_1
    [Tags]  CONSR-BMCT-RDFT-0210-0001   Athena-G2
    [Setup]     OS Connect Device
    Step  1  Verify telemetry service log service info show up correctly
    [Teardown]   OS Disconnect Device

CONSR-BMCT-RDFT-0206-0001
    [Documentation]  This test checks Redfish Trigger Collection_1
    [Tags]  CONSR-BMCT-RDFT-0206-0001   Athena-G2
    [Setup]     OS Connect Device
    Step  1  Verify telemetry service triggers info show up correctly
    [Teardown]   OS Disconnect Device

CONSR-BMCT-RDFT-0204-0001
    [Documentation]  This test checks Redfish Metric Report Collection
    [Tags]  CONSR-BMCT-RDFT-0204-0001   Athena-G2
    [Setup]     OS Connect Device
    Step  1  Verify telemetry service metric reports info show up correctly
    [Teardown]   OS Disconnect Device

CONSR-BMCT-RDFT-0200-0001
    [Documentation]  This test checks Redfish Report Definition Collection
    [Tags]  CONSR-BMCT-RDFT-0200-0001   Athena-G2
    [Setup]     OS Connect Device
    Step  1  Verify telemetry service metric report definition info show up correctly
    [Teardown]   OS Disconnect Device

CONSR-BMCT-RDFT-0199-0001
    [Documentation]  This test checks Redfish MetricDefinition
    [Tags]  CONSR-BMCT-RDFT-0199-0001   Athena-G2
    [Setup]     OS Connect Device
    Step  1  Verify telemetry service metric definition instance info show up correctly
    [Teardown]   OS Disconnect Device

CONSR-BMCT-RDFT-0198-0001
    [Documentation]  This test checks Redfish MetricDefinition Collection
    [Tags]  CONSR-BMCT-RDFT-0198-0001   Athena-G2
    [Setup]     OS Connect Device
    Step  1  Verify telemetry service metric definition info show up correctly
    [Teardown]   OS Disconnect Device

CONSR-BMCT-RDFT-0013-0001
    [Documentation]  This test checks Redfish   Memory_2
    [Tags]   CONSR-BMCT-RDFT-0013-0001   Athena-G2
    [Timeout]   20 min 00 second
    [Setup]    OS Connect Device
    Step  1     verify memory instance    ${resource_memory_instance_3}
    Step  2     verify memory instance    ${resource_memory_instance_12}
    Step  3     verify memory instance without error    ${resource_memory_instance_1}
    Step  4     verify memory instance without error   ${resource_memory_instance_2}
    Step  5     verify memory instance without error   ${resource_memory_instance_4}
    Step  6     verify memory instance without error    ${resource_memory_instance_5}
    Step  7     verify memory instance without error    ${resource_memory_instance_6}
    Step  8     verify memory instance without error   ${resource_memory_instance_7}
    Step  9     verify memory instance without error   ${resource_memory_instance_8}
    Step  10    verify memory instance without error    ${resource_memory_instance_9}
    Step  11    verify memory instance without error   ${resource_memory_instance_10}
    Step  12    verify memory instance without error   ${resource_memory_instance_11}
    Step  13    verify memory instance without error   ${resource_memory_instance_13}
    Step  14    verify memory instance without error    ${resource_memory_instance_14}
    Step  15    verify memory instance without error    ${resource_memory_instance_15}
    Step  16    verify memory instance without error   ${resource_memory_instance_16}
    Step  17    verify memory instance without error   ${resource_memory_instance_17}
    Step  18    verify memory instance without error   ${resource_memory_instance_18}
    [Teardown]   OS Disconnect Device

CONSR-BMCT-RDFT-0016-0001
    [Documentation]  This test checks Redfish   Processor Collection_2
    [Tags]   CONSR-BMCT-RDFT-0016-0001    Athena-G2
    [Timeout]   20 min 00 second
    Step  1    verify sub processor collection    ${resource_subprocessor_collection_1}
    Step  2    verify sub processor collection    ${resource_subprocessor_collection_2}

CONSR-BMCT-RDFT-0017-0001
    [Documentation]  This test checks Redfish   Redfish	Processor_1
    [Tags]   CONSR-BMCT-RDFT-0017-0001      Athena-G2
    [Timeout]   20 min 00 second
    Step  1    Verify processor instance property   ${resource_processor_instance_property_1}
    Step  2    Verify processor instance property   ${resource_processor_instance_property_2}
 
CONSR-BMCT-RDFT-0020-0001
    [Documentation]  This test checks Redfish	Ethernet Interface Collection_2
    [Tags]   CONSR-BMCT-RDFT-0020-0001    Athena-G2
    [Timeout]   20 min 00 second
    Step  1   Verify all network interfaces instance   ${resource_network_interface_instance_2}
    Step  2   Verify all network interfaces instance without error   ${resource_network_interface_instance_1}
    Step  3   Verify all network interfaces instance without error   ${resource_network_interface_instance_3}
    Step  4   Verify all network interfaces instance without error   ${resource_network_interface_instance_4} 

CONSR-BMCT-RDFT-0118-0001
    [Documentation]  EventService_1
    [Tags]   CONSR-BMCT-RDFT-0118-0001  Athena-G2
    [Setup]     OS Connect Device

    Step  1   Verify GET on EventService

    [Teardown]   OS Disconnect Device

CONSR-BMCT-RDFT-0119-0001
    [Documentation]  EventService_2
    [Tags]   CONSR-BMCT-RDFT-0119-0001  Athena-G2
    [Setup]     OS Connect Device

    Step  1   Create a new EventService SubmitTestEvent and Verify

    [Teardown]   OS Disconnect Device

CONSR-BMCT-RDFT-0120-0001
    [Documentation]  TaskService
    [Tags]   CONSR-BMCT-RDFT-0120-0001  Athena-G2
    [Setup]     OS Connect Device

    Step  1   Verify GET on TasksService

    [Teardown]   OS Disconnect Device

CONSR-BMCT-RDFT-0121-0001
    [Documentation]  Task Collection
    [Tags]   CONSR-BMCT-RDFT-0121-0001  Athena-G2
    [Setup]     OS Connect Device

    Step  1   Verify GET on Task Collections

    [Teardown]   OS Disconnect Device

CONSR-BMCT-RDFT-0086-0001
    [Documentation]  This test checks Redfish Manager_2
    [Tags]  CONSR-BMCT-RDFT-0086-0001    Athena-G2
    [Setup]     OS Connect Device
    Step  1  Verify manager date time can be changed successfully
    [Teardown]   OS Disconnect Device

CONSR-BMCT-RDFT-0196-0001
    [Documentation]  This test checks Redfish TelemetryService_2
    [Tags]   CONSR-BMCT-RDFT-0196-0001  Athena-G2
    [Setup]     OS Connect Device
    Step  1   Verify telemetry test metric report can be sent successfully
    [Teardown]   OS Disconnect Device

CONSR-BMCT-RDFT-0085-0001
    [Documentation]  This test checks Redfish Manager_1
    [Tags]   CONSR-BMCT-RDFT-0085-0001    Athena-G2
    [Setup]     OS Connect Device
    Step  1   Verify manager instance info show up correctly 
    [Teardown]   OS Disconnect Device

CONSR-BMCT-RDFT-0078-0001
    [Documentation]  This test checks Redfish Chassis_1
    [Tags]   CONSR-BMCT-RDFT-0078-0001    Athena-G2
    [Setup]     OS Connect Device
    Step  1   Verify chassis instance property show up correctly
    [Teardown]   OS Disconnect Device

CONSR-BMCT-RDFT-0081-0001
    [Documentation]  This test checks Redfish Chassis_1
    [Tags]   CONSR-BMCT-RDFT-0081-0001    Athena-G2
    [Setup]     OS Connect Device
    ${ip}  get_ip_address_from_ipmitool  DUT
    ${curl_output} =  run_curl_BMCIP_get  ${resource_ChassisSelfPower}  ${ip}
    Step  1  Verify power control info show up correctly  ${curl_output}
    Step  2  Verify power supply info show up correctly  ${curl_output}
    Step  3  Verify voltage info show up correctly  ${curl_output}
    Step  4  Verify the curl output and ensure no error    ${curl_output}
    [Teardown]   OS Disconnect Device

CONSR-BMCT-RDFT-0083-0001
    [Documentation]  This test checks Redfish Thermal
    [Tags]   CONSR-BMCT-RDFT-0083-0001    Athena-G2
    [Setup]     OS Connect Device
    ${ip}  get_ip_address_from_ipmitool  DUT
    ${curl_output} =  run_curl_BMCIP_get  ${resource_ChassisSelfThermal}  ${ip}
    Step  1  Verify fan and temperature sensor info show up correctly  ${curl_output}
    Step  2  Verify the curl output and ensure no error    ${curl_output}
    [Teardown]   OS Disconnect Device

CONSR-BMCT-RDFT-0219-0001
    [Documentation]  This test checks Resource Zone Collection
    [Tags]   CONSR-BMCT-RDFT-0219-0001   Athena-G2
    [Timeout]   20 min 00 seconds
    Step  1    Verify Resource Zone Collection

CONSR-BMCT-RDFT-0220-0001
    [Documentation]  This test checks Resource Zone Collection instance
    [Tags]   CONSR-BMCT-RDFT-0220-0001   Athena-G2
    [Timeout]   20 min 00 seconds
    Step  1    Verify Resource Zone Collection instance

CONSR-BMCT-RDFT-0221-0001
    [Documentation]  This test checks Capabilities
    [Tags]   CONSR-BMCT-RDFT-0221-0001   Athena-G2
    [Timeout]   20 min 00 seconds
    Step  1     Verify capabilites

CONSR-BMCT-RDFT-0181-0001
    [Documentation]  This test checks Configurations_1
    [Tags]   CONSR-BMCT-RDFT-0181-0001   Athena-G2
    [Timeout]   20 min 00 seconds
    Step  1     Verify Configurations_1

CONSR-BMCT-RDFT-0183-0001
    [Documentation]  This test checks AccountService Configurations_1
    [Tags]   CONSR-BMCT-RDFT-0183-0001   Athena-G2
    [Timeout]   20 min 00 seconds
    Step  1     Verify AccountService Configurations_1

CONSR-BMCT-RDFT-0185-0001
    [Documentation]  This test checks CertificateService_1
    [Tags]   CONSR-BMCT-RDFT-0185-0001   Athena-G2
    [Timeout]   20 min 00 seconds
    Step  1     Verify CertificateService_1

CONSR-BMCT-RDFT-0122-0001
    [Documentation]  Task_1
    [Tags]   CONSR-BMCT-RDFT-0122-0001  Athena-G2
    [Setup]     OS Connect Device

    Step  1   Log  This Test case already covered in CONSR-BMCT-RDFT-0119-0001

    [Teardown]   OS Disconnect Device

CONSR-BMCT-RDFT-0123-0001
    [Documentation]  Task_2
    [Tags]   CONSR-BMCT-RDFT-0123-0001  Athena-G2
    [Setup]     OS Connect Device

    Step  1   Delete the previously created EventService Task

    [Teardown]   OS Disconnect Device

CONSR-BMCT-RDFT-0031-0001
    [Documentation]  This test checks Redfish   Ethernet Interface Collection_13
    [Tags]   CONSR-BMCT-RDFT-0031-0001   Athena-G2
    [Timeout]   20 min 00 second
    [Setup]    OS Connect Device
    Step  1    Verify all network interfaces properties    ${resource_ethernet_interface_instance_1}
    Step  2    Verify all network interfaces properties    ${resource_ethernet_interface_instance_2}
    Step  3    Verify all network interfaces properties    ${resource_ethernet_interface_instance_3}
    [TearDown]   OSDisconnect

CONSR-BMCT-RDFT-0033-0001
    [Documentation]  This test checks Redfish   Bios_1
    [Tags]   CONSR-BMCT-RDFT-0033-0001      Athena-G2
    [Timeout]   20 min 00 second
    [Setup]    OS Connect Device
    Step  1    Verify bios attribution 
    [TearDown]   OSDisconnect

CONSR-BMCT-RDFT-0034-0001
    [Documentation]  This test checks Redfish  Bios_2
    [Tags]  CONSR-BMCT-RDFT-0034-0001     Athena-G2
    [Timeout]   20 min 00 second
    [Setup]    OS Connect Device
    Step  1    Verify bios property
    [TearDown]   OSDisconnect

CONSR-BMCT-RDFT-0055-0001
    [Documentation]  This test checks Redfish  Log Service_12
    [Tags]  CONSR-BMCT-RDFT-0055-0001    Athena-G2
    [Timeout]   20 min 00 second
    [Setup]    OS Connect Device
    Step  1    verify log properties  ${resource_chassis_log_property}
    [TearDown]   OSDisconnect

CONSR-BMCT-RDFT-0052-0001
    [Documentation]  This test checks Redfish  Log Service_9
    [Tags]  CONSR-BMCT-RDFT-0052-0001      Athena-G2
    [Timeout]   20 min 00 second
    [Setup]    OS Connect Device
    Step  1    verify log properties   ${resource_telemetry_log_property}
    [TearDown]   OSDisconnect

CONSR-BMCT-RDFT-0049-0001
    [Documentation]  This test checks Redfish  Log Service_6
    [Tags]  CONSR-BMCT-RDFT-0049-0001     Athena-G2
    [Timeout]   20 min 00 second
    [Setup]    OS Connect Device
    Step  1   Verify collections   ${resource_managers_logservices}
    Step  2   verify log properties   ${resource_managerslog_property_1}
    Step  3   verify log properties   ${resource_managerslog_property_2}
    Step  4   verify log properties   ${resource_managerslog_property_3}
    [TearDown]   OSDisconnect

CONSR-BMCT-RDFT-0047-0001
    [Documentation]  This test checks Redfish  Log Service_4
    [Tags]  CONSR-BMCT-RDFT-0047-0001      Athena-G2
    [Timeout]   20 min 00 second
    [Setup]    OS Connect Device
    Step  1   Verify collections   ${resource_bios_logentries}
    [TearDown]   OSDisconnect


CONSR-BMCT-RDFT-0044-0001
    [Documentation]  This test checks Redfish  Log Service_1
    [Tags]  CONSR-BMCT-RDFT-0044-0001      Athena-G2
    [Timeout]   20 min 00 second
    [Setup]    OS Connect Device
    Step  1    verify log properties   ${resource_log_bios_properties}
    [TearDown]   OSDisconnect

CONSR-BMCT-RDFT-0018-0001
    [Documentation]  This test checks Redfish  Processor_2
    [Tags]  CONSR-BMCT-RDFT-0018-0001   Athena-G2
    [Timeout]   20 min 00 second
    [Setup]    OS Connect Device
    Step  1    Verify sub processor instance property   ${resource_proc1_subproc1}
    Step  2    Verify sub processor instance property   ${resource_proc1_subproc2}
    Step  3    Verify sub processor instance property   ${resource_proc1_subproc3}
    Step  4    Verify sub processor instance property   ${resource_proc1_subproc4}
    Step  5    Verify sub processor instance property   ${resource_proc1_subproc5}
    Step  6    Verify sub processor instance property   ${resource_proc1_subproc6}
    Step  7    Verify sub processor instance property   ${resource_proc1_subproc7}
    Step  8    Verify sub processor instance property   ${resource_proc1_subproc8}
    Step  9    Verify sub processor instance property   ${resource_proc1_subproc9}
    Step  10   Verify sub processor instance property   ${resource_proc1_subproc10}
    Step  11   Verify sub processor instance property   ${resource_proc1_subproc11}
    Step  12   Verify sub processor instance property   ${resource_proc1_subproc12}
    Step  13   Verify sub processor instance property   ${resource_proc1_subproc13}
    Step  14   Verify sub processor instance property   ${resource_proc1_subproc14}
    Step  15   Verify sub processor instance property   ${resource_proc1_subproc15}
    Step  16   Verify sub processor instance property   ${resource_proc1_subproc16}
    Step  17   Verify sub processor instance property   ${resource_proc1_subproc17}
    Step  18   Verify sub processor instance property   ${resource_proc1_subproc18}
    Step  19   Verify sub processor instance property   ${resource_proc1_subproc19}
    Step  20   Verify sub processor instance property   ${resource_proc1_subproc20}
    Step  21   Verify sub processor instance property   ${resource_proc1_subproc21}
    Step  22   Verify sub processor instance property   ${resource_proc1_subproc22}
    Step  23   Verify sub processor instance property   ${resource_proc1_subproc23}
    Step  24   Verify sub processor instance property   ${resource_proc1_subproc24}
    Step  25   Verify sub processor instance property   ${resource_proc2_subproc1}
    Step  26   Verify sub processor instance property   ${resource_proc2_subproc2}
    Step  27   Verify sub processor instance property   ${resource_proc2_subproc3}
    Step  28   Verify sub processor instance property   ${resource_proc2_subproc4}
    Step  29   Verify sub processor instance property   ${resource_proc2_subproc5}
    Step  30   Verify sub processor instance property   ${resource_proc2_subproc6}
    Step  31   Verify sub processor instance property   ${resource_proc2_subproc7}
    Step  32   Verify sub processor instance property   ${resource_proc2_subproc8}
    Step  33   Verify sub processor instance property   ${resource_proc2_subproc9}
    Step  34   Verify sub processor instance property   ${resource_proc2_subproc10}
    Step  35   Verify sub processor instance property   ${resource_proc2_subproc11}
    Step  36   Verify sub processor instance property   ${resource_proc2_subproc12}
    Step  37   Verify sub processor instance property   ${resource_proc2_subproc13}
    Step  38   Verify sub processor instance property   ${resource_proc2_subproc14}
    Step  39   Verify sub processor instance property   ${resource_proc2_subproc15}
    Step  40   Verify sub processor instance property   ${resource_proc2_subproc16}
    Step  41   Verify sub processor instance property   ${resource_proc2_subproc17}
    Step  42   Verify sub processor instance property   ${resource_proc2_subproc18}
    Step  43   Verify sub processor instance property   ${resource_proc2_subproc19}
    Step  44   Verify sub processor instance property   ${resource_proc2_subproc20}
    Step  45   Verify sub processor instance property   ${resource_proc2_subproc21}
    Step  46   Verify sub processor instance property   ${resource_proc2_subproc22}
    Step  47   Verify sub processor instance property   ${resource_proc2_subproc23}
    Step  48   Verify sub processor instance property   ${resource_proc2_subproc24}
    [TearDown]   OSDisconnect

CONSR-BMCT-RDFT-0088-0001
    [Documentation]  This test checks Redfish ManagersNetworkProtocol_1
    [Tags]   CONSR-BMCT-RDFT-0088-0001    Athena-G2
    [Setup]     OS Connect Device
    Step  1  Verify manager network protocal info show up correctly
    [Teardown]   OS Disconnect Device

CONSR-BMCT-RDFT-0090-0001
    [Documentation]  This test checks Redfish SerialInterfaces Collection
    [Tags]   CONSR-BMCT-RDFT-0090-0001    Athena-G2
    [Setup]     OS Connect Device
    Step  1  Verify manager serial interfaces info show up correctly
    [Teardown]   OS Disconnect Device

CONSR-BMCT-RDFT-0091-0001
    [Documentation]  This test checks Redfish SerialInterfaces_1
    [Tags]   CONSR-BMCT-RDFT-0091-0001    Athena-G2
    [Setup]     OS Connect Device
    Step  1  Verify manager sol info can be changed successfully
    [Teardown]   OS Disconnect Device

CONSR-BMCT-RDFT-0092-0001
    [Documentation]  This test checks Redfish SerialInterfaces_2
    [Tags]   CONSR-BMCT-RDFT-0092-0001    Athena-G2
    [Setup]     OS Connect Device
    Step  1  Verfiy manager sol can be disable successfully
    Step  2  Verfiy manager sol can be enable successfully
    [Teardown]   OS Disconnect Device

CONSR-BMCT-RDFT-0079-0001
    [Documentation]  This test checks Redfish Chassis_2
    [Tags]   CONSR-BMCT-RDFT-0079-0001    Athena-G2
    [Setup]     OS Connect Device
    Step  1  Verify chassis assettag can be modified successfully
    [Teardown]   OS Disconnect Device

CONSR-BMCT-RDFT-0097-0001
    [Documentation]  This test checks Redfish AccountService_1
    [Tags]   CONSR-BMCT-RDFT-0097-0001    Athena-G2
    [Setup]     OS Connect Device
    ${ip}  get_ip_address_from_ipmitool  DUT
    ${curl_output} =  run_curl_BMCIP_get  ${resource_accountservice}  ${ip}
    Step  1  Verify account service info show up correctly  ${curl_output}
    Step  2  Verify the curl output and ensure no error    ${curl_output}
    [Teardown]   OS Disconnect Device

CONSR-BMCT-RDFT-0053-0001
    [Documentation]    This test checks Redfish  Log Service_10
    [Tags]   CONSR-BMCT-RDFT-0053-0001   Athena-G2
    [Setup]   OS Connect Device
    Step  1   Set ServiceEnabled to False    ${resource_telemetry_log_property}
    Step  2   Check ServiceEnabled value as False     ${resource_telemetry_log_property}
    Step  3   Set ServiceEnabled to True   ${resource_telemetry_log_property}
    Step  4   Check ServiceEnabled value as True    ${resource_telemetry_log_property}
    [Teardown]   OS Disconnect Device 

CONSR-BMCT-RDFT-0050-0001
    [Documentation]    This test checks Redfish  Log Service_7
    [Tags]   CONSR-BMCT-RDFT-0050-0001   Athena-G2
    [Setup]   OS Connect Device
    Step  1   Set ServiceEnabled to False    ${resource_managerslog_property_1}
    Step  2   Check ServiceEnabled value as False     ${resource_managerslog_property_1}
    Step  3   Set ServiceEnabled to True   ${resource_managerslog_property_1}
    Step  4   Check ServiceEnabled value as True    ${resource_managerslog_property_1}
    Step  5   Set ServiceEnabled to False    ${resource_managerslog_property_2}
    Step  6   Check ServiceEnabled value as False     ${resource_managerslog_property_2}
    Step  7   Set ServiceEnabled to True   ${resource_managerslog_property_2}
    Step  8   Check ServiceEnabled value as True    ${resource_managerslog_property_2}
    Step  9   Set ServiceEnabled to False    ${resource_managerslog_property_3}
    Step  10  Check ServiceEnabled value as False     ${resource_managerslog_property_3}
    Step  11  Set ServiceEnabled to True   ${resource_managerslog_property_3}
    Step  12  Check ServiceEnabled value as True    ${resource_managerslog_property_3}
    [Teardown]   OS Disconnect Device

CONSR-BMCT-RDFT-0045-0001
    [Documentation]    This test checks Redfish  Log Service_2
    [Tags]   CONSR-BMCT-RDFT-0045-0001      Athena-G2
    [Setup]   OS Connect Device
    Step  1   Set ServiceEnabled to False    ${resource_log_bios_properties}
    Step  2   Check ServiceEnabled value as False     ${resource_log_bios_properties}
    Step  3   Set ServiceEnabled to True   ${resource_log_bios_properties}
    Step  4   Check ServiceEnabled value as True    ${resource_log_bios_properties}
    [Teardown]   OS Disconnect Device

CONSR-BMCT-RDFT-0124-0001
    [Documentation]  JSON Schema file collection
    [Tags]   CONSR-BMCT-RDFT-0124-0001  Athena-G2
    [Setup]     OS Connect Device

    Step  1   Verify GET on JsonSchemas

    [Teardown]   OS Disconnect Device

CONSR-BMCT-RDFT-0125-0001
    [Documentation]  JSON Schema file
    [Tags]   CONSR-BMCT-RDFT-0125-0001  Athena-G2
    [Setup]     OS Connect Device

    Step  1   Verify GET on JsonSchemas Members

    [Teardown]   OS Disconnect Device

CONSR-BMCT-RDFT-0046-0001
    [Documentation]    This test checks Redfish  Log Service_3
    [Tags]   CONSR-BMCT-RDFT-0046-0001       Athena-G2
    [Setup]   OS Connect Device
    Step  1   verify time and timeoffset    ${resource_log_bios_properties}    ${data_DateTime}    ${expected_DateTime}    ${expected_DateTimeOffset}
    Step  2   verify time and timeoffset    ${resource_log_bios_properties}    ${data_DateTime_1}  ${expected_DateTime_1}    ${expected_DateTimeOffset}
    [Teardown]   OS Disconnect Device

CONSR-BMCT-RDFT-0051-0001
    [Documentation]    This test checks Redfish   Log Service_8
    [Tags]   CONSR-BMCT-RDFT-0051-0001    Athena-G2
    [Setup]   OS Connect Device
    Step  1   verify time and timeoffset    ${resource_managerslog_property_1}  ${set_DateTime}  ${expected_DateTime_2}  ${expected_DateTimeOffset_1}
    Step  2   verify time and timeoffset    ${resource_managerslog_property_2}  ${set_DateTime}  ${expected_DateTime_2}  ${expected_DateTimeOffset_1}
    Step  3   verify time and timeoffset    ${resource_managerslog_property_3}  ${set_DateTime}  ${expected_DateTime_2}  ${expected_DateTimeOffset_1}
    [Teardown]   OS Disconnect Device

CONSR-BMCT-RDFT-0054-0001
    [Documentation]    This test checks Redfish   Log Service_11
    [Tags]   CONSR-BMCT-RDFT-0054-0001        Athena-G2
    [Setup]   OS Connect Device
    Step  1   verify time and timeoffset    ${resource_telemetry_log_property}   ${set_DateTime}  ${expected_DateTime_2}  ${expected_DateTimeOffset_1}
    Step  2   verify time and timeoffset    ${resource_telemetry_log_property}   ${set_DateTime_1}  ${expected_DateTime_3}  ${expected_DateTimeOffset_1}
    [Teardown]   OS Disconnect Device

CONSR-BMCT-RDFT-0058-0001
    [Documentation]  This test checks Redfish LogEntry Collection_1
    [Tags]   CONSR-BMCT-RDFT-0058-0001    Athena-G2
    [Setup]     OS Connect Device
    Step  1  Verify log entries show up correctly
    [Teardown]   OS Disconnect Device

CONSR-BMCT-RDFT-0062-0001
    [Documentation]  This test checks Redfish LogEntry Collection_5
    [Tags]   CONSR-BMCT-RDFT-0062-0001    Athena-G2
    [Setup]     OS Connect Device
    Step  1  Verify log entries show up correctly
    [Teardown]   OS Disconnect Device

CONSR-BMCT-RDFT-0105-0001
    [Documentation]  This test checks Redfish Manager Account Collection_3
    [Tags]   CONSR-BMCT-RDFT-0105-0001    Athena-G2
    [Setup]     OS Connect Device
    Step  1  Verify account instance info show up correctly
    [Teardown]   OS Disconnect Device

CONSR-BMCT-RDFT-0108-0001
    [Documentation]  This test checks Redfish Collection_1
    [Tags]   CONSR-BMCT-RDFT-0108-0001    Athena-G2
    [Setup]     OS Connect Device
    Step  1  Verify account roles info show up correctly
    [Teardown]   OS Disconnect Device

CONSR-BMCT-RDFT-0110-0001
    [Documentation]  This test checks Redfish Role Collection_3
    [Tags]   CONSR-BMCT-RDFT-0110-0001    Athena-G2
    [Setup]     OS Connect Device
    Step  1  Verify account role info show up correctly
    [Teardown]   OS Disconnect Device

CONSR-BMCT-RDFT-0154-0001
    [Documentation]  This test checks Redfish	UpdateService_6
    [Tags]   CONSR-BMCT-RDFT-0154-0001   Athena-G2
    [Timeout]   20 min 00 seconds
    [Setup]    OS Connect Device
    Step  1   Verify collections   ${resource_FirmwareInventory_collections}
    [TearDown]   OSDisconnect

CONSR-BMCT-RDFT-0155-0001
    [Documentation]  This test checks Redfish   UpdateService_7
    [Tags]   CONSR-BMCT-RDFT-0155-0001        Athena-G2
    [Timeout]   20 min 00 seconds
    [Setup]    OS Connect Device
    Step  1    Verify firmware inventory instance
    [TearDown]   OSDisconnect

CONSR-BMCT-RDFT-0156-0001
    [Documentation]  This test checks Redfish SecureBoot_1
    [Tags]   CONSR-BMCT-RDFT-0156-0001        Athena-G2
    [Timeout]   20 min 00 seconds
    [Setup]    OS Connect Device
    Step   1   Verify secure boot info
    [TearDown]   OSDisconnect

CONSR-BMCT-RDFT-0126-0001
    [Documentation]  Session Collection_1
    [Tags]   CONSR-BMCT-RDFT-0126-0001  Athena-G2
    [Setup]     OS Connect Device

    Step  1   Verify GET on SessionService's Sessions

    [Teardown]   OS Disconnect Device

CONSR-BMCT-RDFT-0195-0001
    [Documentation]  This test checks TelemetryService_1
    [Tags]   CONSR-BMCT-RDFT-0195-0001   Athena-G2
    [Timeout]   20 min 00 seconds
    Step  1     Verify TelemetryService_1

CONSR-BMCT-RDFT-0100-0001
    [Documentation]  This test checks AccountService_4
    [Tags]   CONSR-BMCT-RDFT-0100-0001   Athena-G2
    [Timeout]   20 min 00 seconds
    Step  1     Verify AccountService_4

CONSR-BMCT-RDFT-0103-0001
    [Documentation]  This test checks Manager Account Collection_1
    [Tags]   CONSR-BMCT-RDFT-0103-0001   Athena-G2
    [Timeout]   20 min 00 seconds
    Step  1     Verify Manager_Account_Collection_1

CONSR-BMCT-RDFT-0084-0001
    [Documentation]  This test checks ManagerCollection
    [Tags]   CONSR-BMCT-RDFT-0084-0001   Athena-G2
    [Timeout]   20 min 00 seconds
    Step  1     Verify ManagerCollection

CONSR-BMCT-RDFT-0191-0001
    [Documentation]  This test checks HostInterface Collection
    [Tags]   CONSR-BMCT-RDFT-0191-0001  Athena-G2
    [Timeout]   20 min 00 seconds
    Step  1     Verify HostInterface_Collection

CONSR-BMCT-RDFT-0192-0001
    [Documentation]  This test checks HostInterface
    [Tags]   CONSR-BMCT-RDFT-0192-0001  Athena-G2
    [Timeout]   20 min 00 seconds
    Step  1     Verify HostInterface

CONSR-BMCT-RDFT-0193-0001
    [Documentation]  This test checks HostEthernetInterfaceCollection
    [Tags]   CONSR-BMCT-RDFT-0193-0001  Athena-G2
    [Timeout]   20 min 00 seconds
    Step  1     Verify HostEthernetInterfaceCollection

CONSR-BMCT-RDFT-0194-0001
    [Documentation]  This test checks ManagerEthernetInterface_Instance
    [Tags]   CONSR-BMCT-RDFT-0194-0001  Athena-G2
    [Timeout]   20 min 00 seconds
    Step  1     Verify ManagerEthernetInterface_Instance

CONSR-BMCT-RDFT-0107-0001
    [Documentation]  This test checks Redfish Manager Account_2
    [Tags]   CONSR-BMCT-RDFT-0107-0001    Athena-G2
    [Setup]     OS Connect Device    
    Step  1  Verify account instance can be deleted successfully
    [Teardown]   OS Disconnect Device

CONSR-BMCT-RDFT-0003-0001
    [Documentation]  This test checks Redfish Computer System Collection_2
    [Tags]   CONSR-BMCT-RDFT-0003-0001    Athena-G2
    [Setup]     OS Connect Device
    Step  1  Verify new system can be created successfully
    [Teardown]   OS Disconnect Device

CONSR-BMCT-RDFT-0104-0001
    [Documentation]  This test checks Redfish Manager Account Collection_2
    [Tags]   CONSR-BMCT-RDFT-0104-0001    Athena-G2
    [Setup]     OS Connect Device
    Step  1  Verify new account can be created
    [Teardown]   OS Disconnect Device

CONSR-BMCT-RDFT-0098-0001
    [Documentation]  This test checks Redfish AccountService_2
    [Tags]   CONSR-BMCT-RDFT-0098-0001    Athena-G2
    [Setup]     OS Connect Device
    Step  1  Verify account locked after enough unsuccessfu login
    [Teardown]   OS Disconnect Device

CONSR-BMCT-RDFT-0069-0001
    [Documentation]  This test checks Redfish Log Entry_4
    [Tags]   CONSR-BMCT-RDFT-0069-0001    Athena-G2
    [Setup]     OS Connect Device
    Step  1  Verify log entry show up correctly
    [Teardown]   OS Disconnect Device

CONSR-BMCT-RDFT-0070-0001
    [Documentation]  This test checks Redfish VLANNetwork InterfaceCollection_1
    [Tags]   CONSR-BMCT-RDFT-0070-0001    Athena-G2
    [Setup]     OS Connect Device
    Step  1  Verify system network info show up correctly
    [Teardown]   OS Disconnect Device

CONSR-BMCT-RDFT-0071-0001
    [Documentation]  This test checks Redfish VLANNetwork InterfaceCollection_2
    [Tags]   CONSR-BMCT-RDFT-0071-0001    Athena-G2
    [Setup]     OS Connect Device
    Step  1  Verify system network vlan can be created successfully
    [Teardown]   OS Disconnect Device

CONSR-BMCT-RDFT-0168-0001
    [Documentation]  This test checks Redfish PCIeSlots
    [Tags]   CONSR-BMCT-RDFT-0168-0001     Athena-G2
    [Timeout]   20 min 00 seconds
    [Setup]    OS Connect Device
    Step   1   Verify pcie slots info 
    [TearDown]   OSDisconnect

CONSR-BMCT-RDFT-0179-0001
    [Documentation]  This test checks Redfish SensorCollection
    [Tags]   CONSR-BMCT-RDFT-0179-0001     Athena-G2
    [Timeout]   20 min 00 seconds
    [Setup]   OS Connect Device
    Step  1   Verify collections   ${resource_sensor_collections}
    [TearDown]   OSDisconnect

CONSR-BMCT-RDFT-0180-0001
    [Documentation]  This test checks Redfish Sensor
    [Tags]   CONSR-BMCT-RDFT-0180-0001     Athena-G2
    [Timeout]   20 min 00 seconds
    [Setup]   OS Connect Device
    Step  1   Verify chassis sensor instance info
    [TearDown]   OSDisconnect

CONSR-BMCT-RDFT-0158-0001
    [Documentation]  This test checks Redfish Drives
    [Tags]   CONSR-BMCT-RDFT-0158-0001         Athena-G2
    [Timeout]   20 min 00 seconds
    [Setup]   OS Connect Device
    Step  1   Verify drive instance info NVMe   ${resource_storage_drive1}
    Step  2   Verify drive instance info NVMe   ${resource_storage_drive2}
    Step  3   Verify drive instance info NVMe   ${resource_storage_drive3}
    Step  4   Verify drive instance info NVMe   ${resource_storage_drive4}
    Step  5   Verify drive instance info NVMe   ${resource_storage_drive5}
    Step  6   Verify drive instance info SATA   ${resource_storage_drive6}
    Step  7   Verify drive instance info USB    ${resource_storage_drive7}
    Step  8   Verify drive instance info USB    ${resource_storage_drive8}
    [TearDown]   OSDisconnect

CONSR-BMCT-RDFT-0159-0001
    [Documentation]  This test checks Redfish NetworkPort Collection
    [Tags]   CONSR-BMCT-RDFT-0159-0001           Athena-G2
    [Timeout]   20 min 00 seconds
    [Setup]   OS Connect Device
    Step  1   Verify network port info
    [TearDown]   OSDisconnect

CONSR-BMCT-RDFT-0129-0001
    [Documentation]  Session Service
    [Tags]   CONSR-BMCT-RDFT-0129-0001  Athena-G2
    [Setup]     OS Connect Device

    Step  1   Verify GET on SessionService

    [Teardown]   OS Disconnect Device

CONSR-BMCT-RDFT-0132-0001
    [Documentation]  MessageRegistry
    [Tags]   CONSR-BMCT-RDFT-0132-0001  Athena-G2
    [Setup]     OS Connect Device

    Step  1   Verify GET on Registries Members JSON

    [Teardown]   OS Disconnect Device

CONSR-BMCT-RDFT-0133-0001
    [Documentation]  MessageRegistryFileCollection
    [Tags]   CONSR-BMCT-RDFT-0133-0001  Athena-G2
    [Setup]     OS Connect Device

    Step  1   Verify GET on Registries

    [Teardown]   OS Disconnect Device

CONSR-BMCT-RDFT-0134-0001
    [Documentation]  Message Registry File
    [Tags]   CONSR-BMCT-RDFT-0134-0001  Athena-G2
    [Setup]     OS Connect Device

    Step  1   Verify GET on Registries Members File

    [Teardown]   OS Disconnect Device

CONSR-BMCT-RDFT-0072-0001
    [Documentation]  This test checks Redfish VLANNetwork InterfaceCollection_3
    [Tags]   CONSR-BMCT-RDFT-0072-0001    Athena-G2
    [Setup]     OS Connect Device
    Step  1  Verify chassis network info show up correctly
    [Teardown]   OS Disconnect Device

CONSR-BMCT-RDFT-0073-0001
    [Documentation]  This test checks Redfish VLAN Network Interface_1
    [Tags]   CONSR-BMCT-RDFT-0073-0001    Athena-G2
    [Setup]     OS Connect Device
    Step  1  Verify chassis network info show up correctly
    [Teardown]   OS Disconnect Device

CONSR-BMCT-RDFT-0075-0001
    [Documentation]  This test checks Redfish VLAN Network Interface_3
    [Tags]   CONSR-BMCT-RDFT-0075-0001    Athena-G2
    [Setup]     OS Connect Device
    Step  1  Verify system network vlan can be deleted successfully
    [Teardown]   OS Disconnect Device

CONSR-BMCT-RDFT-0076-0001
    [Documentation]  This test checks Redfish VLAN Network Interface_4
    [Tags]   CONSR-BMCT-RDFT-0076-0001    Athena-G2
    [Setup]     OS Connect Device
    Step  1  Verify VLAN Network Interface_4 info show up correctly
    [Teardown]   OS Disconnect Device

CONSR-BMCT-RDFT-0067-0001
    [Documentation]  This test checks Redfish Log Entry_2
    [Tags]   CONSR-BMCT-RDFT-0067-0001               Athena-G2
    [Timeout]   20 min 00 seconds
    [Setup]   OS Connect Device
    Step  1   verify manager_logentry_instance showup
    [TearDown]   OSDisconnect

CONSR-BMCT-RDFT-0077-0001
    [Documentation]  This test checks Redfish ChassisCollection
    [Tags]   CONSR-BMCT-RDFT-0077-0001              Athena-G2
    [Timeout]   20 min 00 seconds
    [Setup]   OS Connect Device
    Step  1   Verify chassis property
    [TearDown]   OSDisconnect

CONSR-BMCT-RDFT-0135-0001
    [Documentation]  NetworkInterface Collection
    [Tags]   CONSR-BMCT-RDFT-0135-0001  Athena-G2
    [Setup]     OS Connect Device

    Step  1   Verify GET on NetworkInterface Collection

    [Teardown]   OS Disconnect Device

CONSR-BMCT-RDFT-0136-0001
    [Documentation]  NetworkInterface
    [Tags]   CONSR-BMCT-RDFT-0136-0001  Athena-G2
    [Setup]     OS Connect Device

    Step  1   Verify GET on NetworkInterface Ethernet Members

    [Teardown]   OS Disconnect Device

CONSR-BMCT-RDFT-0137-0001
    [Documentation]  NetworkDeviceFunction Collection
    [Tags]   CONSR-BMCT-RDFT-0137-0001  Athena-G2
    [Setup]     OS Connect Device

    Step  1   Verify GET on NetworkDeviceFunction Collection

    [Teardown]   OS Disconnect Device

CONSR-BMCT-RDFT-0138-0001
    [Documentation]  NetworkDeviceFunction
    [Tags]   CONSR-BMCT-RDFT-0138-0001  Athena-G2
    [Setup]     OS Connect Device

    Step  1   Verify GET on NetworkDeviceFunction Members

    [Teardown]   OS Disconnect Device

CONSR-BMCT-RDFT-0139-0001
    [Documentation]  NetworkAdapter Collection
    [Tags]   CONSR-BMCT-RDFT-0139-0001  Athena-G2
    [Setup]     OS Connect Device

    Step  1   Verify GET on NetworkAdapter Collection

    [Teardown]   OS Disconnect Device

CONSR-BMCT-RDFT-0140-0001
    [Documentation]  NetworkAdapter
    [Tags]   CONSR-BMCT-RDFT-0140-0001  Athena-G2
    [Setup]     OS Connect Device

    Step  1   Verify GET on NetworkAdapter Members

    [Teardown]   OS Disconnect Device

CONSR-BMCT-RDFT-0141-0001
    [Documentation]  Storage Collection
    [Tags]   CONSR-BMCT-RDFT-0141-0001  Athena-G2
    [Setup]     OS Connect Device

    Step  1   Verify GET on Storage Collection

    [Teardown]   OS Disconnect Device

CONSR-BMCT-RDFT-0142-0001
    [Documentation]  Storage
    [Tags]   CONSR-BMCT-RDFT-0142-0001  Athena-G2
    [Setup]     OS Connect Device

    Step  1   Verify GET on Storage Members

    [Teardown]   OS Disconnect Device

CONSR-BMCT-RDFT-0143-0001
    [Documentation]  Volume Collection
    [Tags]   CONSR-BMCT-RDFT-0143-0001  Athena-G2
    [Setup]     OS Connect Device

    Step  1   Verify GET on Volume Collection

    [Teardown]   OS Disconnect Device

CONSR-BMCT-RDFT-0144-0001
    [Documentation]  Volume
    [Tags]   CONSR-BMCT-RDFT-0144-0001  Athena-G2
    [Setup]     OS Connect Device

    Step  1   Verify GET on Volume Members

    [Teardown]   OS Disconnect Device

CONSR-BMCT-RDFT-0145-0001
    [Documentation]  PCIeDevice Collection
    [Tags]   CONSR-BMCT-RDFT-0145-0001  Athena-G2
    [Setup]     OS Connect Device

    Step  1   Verify GET on PCIeDevice Collection

    [Teardown]   OS Disconnect Device

CONSR-BMCT-RDFT-0146-0001
    [Documentation]  PCIeDevice
    [Tags]   CONSR-BMCT-RDFT-0146-0001  Athena-G2
    [Setup]     OS Connect Device

    Step  1   Verify GET on PCIeDevice Members

    [Teardown]   OS Disconnect Device

CONSR-BMCT-RDFT-0147-0001
    [Documentation]  PCIeDeviceFunction Collection
    [Tags]   CONSR-BMCT-RDFT-0147-0001  Athena-G2
    [Setup]     OS Connect Device

    Step  1   Verify GET on PCIeFunction Collection

    [Teardown]   OS Disconnect Device

CONSR-BMCT-RDFT-0148-0001
    [Documentation]  PCIeFunction
    [Tags]   CONSR-BMCT-RDFT-0148-0001  Athena-G2
    [Setup]     OS Connect Device

    Step  1   Verify GET on PCIeFunction Members

    [Teardown]   OS Disconnect Device

CONSR-BMCT-RDFT-0149-0001
    [Documentation]  UpdateService_1
    [Tags]   CONSR-BMCT-RDFT-0149-0001  Athena-G2
    [Setup]     OS Connect Device

    Step  1   Verify GET on UpdateService

    [Teardown]   OS Disconnect Device

CONSR-BMCT-RDFT-0160-0001
    [Documentation]  This test checks NetworkPort
    [Tags]   CONSR-BMCT-RDFT-0160-0001   Athena-G2
    [Timeout]   20 min 00 seconds
    Step  1     Verify NetworkPort

CONSR-BMCT-RDFT-0197-0001
    [Documentation]  This test checks TelemetryService_3
    [Tags]   CONSR-BMCT-RDFT-0197-0001   Athena-G2
    [Timeout]   20 min 00 seconds
    Step  1     Verify get command TelemetryService_3
    Step  2     Verify patch command on TelemetryService_3
    Step  3     Verify set value on TelemetryService_3
    Step  4     Verify get command TelemetryService_3

CONSR-BMCT-RDFT-0157-0001
    [Documentation]  This test checks SecureBoot_2
    [Tags]   CONSR-BMCT-RDFT-0157-0001   Athena-G2
    [Timeout]   20 min 00 seconds
    [Setup]   OS Connect Device
    Step  1   Set SecureBootEnable to False    ${Secure_Boot}
    Step  2   Check SecureBootEnable value as False     ${Secure_Boot}
    Step  3   Set SecureBootEnable to True   ${Secure_Boot}
    Step  4   Check SecureBootEnable value as True    ${Secure_Boot}
    [Teardown]   OS Disconnect Device

CONSR-BMCT-FWUP-0021-0001
    [Documentation]  This test checks Firmware Update - Update BMC with BIOS image
    [Tags]   CONSR-BMCT-FWUP-0021-0001    Athena-G2
    [Timeout]   20 min 00 seconds
    [Setup]  prepare Athena_G2 BIOS images to upgrade
    Step  1  update BMC with BIOS image   Athena_BIOS_Versions_A   newImage  NV
    [Teardown]   remove Athena_G2 BIOS images

CONSR-BMCT-FWUP-0022-0001
    [Documentation]  This test checks FWFlash_021_Update BIOS with BMC image
    [Tags]     CONSR-BMCT-FWUP-0022-0001  Athena-G2
    [Setup]     OS Connect Device
    ${ip}  get_ip_address_from_ipmitool  DUT
    Step  1  Verify event log SEL clear  DUT  ${ip}
    Step  2  Download Athena BMC FW image
    Step  3  Update BIOS with BMC image
    Step  4  Verify abnormal event log  DUT  ${ip}
    [Teardown]  OS Disconnect Device

CONSR-BMCT-FWUP-0001-0001
    [Documentation]   This test checks BMC Firmware Update
    [Tags]   CONSR-BMCT-FWUP-0001-0001  Athena-G2
    Step  1  Update BMC with Local OS and CFUFLASH ESM A   Athena_FW_BMC_A    newImage   BIN   upgrade
    Step  2  Update BMC with Local OS and CFUFLASH ESM A   Athena_FW_BMC_A    oldImage   BIN   downgrade
    Step  3  Update BMC with Local OS and CFUFLASH ESM B   Athena_FW_BMC_B    newImage   BIN   upgrade
    Step  4  Update BMC with Local OS and CFUFLASH ESM B   Athena_FW_BMC_B    oldImage   BIN   downgrade
    Step  5  Remote OS with CFUFLASH Update  upgrade
    Step  6  Remote OS with CFUFLASH Update  downgrade
    [Teardown]  Remove Athena BMC FW image

CONSR-BMCT-SRTS-0015-0001
    [Documentation]   This test checks Fan_tach Stress Test
    [Tags]   CONSR-BMCT-SRTS-0015-0001    Athena-G2
    [Setup]       ConnectESMB
    ${ip}  get_ip_address_from_ipmitool  DUT
    Step  1  Verify event log SEL clear  DUT  ${ip}
    FOR    ${INDEX}    IN RANGE    ${MAXINDEX}
       Print Loop Info  ${INDEX}
       Step  1  check_fan_info   DUT  ${ip}
    END
    Step  3  Verify the SEL and ensure no error
    Step  4  Verify abnormal event log  DUT  ${ip}
    Step  5  verifythesensorreadingandcheckstatus  DUT  ${ip}
    [Teardown]  OS Disconnect Device

CONSR-BMCT-SRTS-0016-0001
   [Documentation]   This test checks Stress Test - Stress_017_BIOS Firmware Update with pc
   [Tags]   CONSR-BMCT-SRTS-0016-0001     Athena-G2
   [Setup]   Prepare images of multiple versions
   FOR    ${INDEX}    IN RANGE    ${MAXINDEX}
        Print Loop Info  ${INDEX}
        Step  1  BIOS Firmware Update with pc     Athena_BIOS_Versions_A   oldImage  V3   ${ME_FW_version}   ${ME_Version_OS}
        Step  2  BIOS Firmware Update with pc     Athena_BIOS_Versions_A   newImage  NV   ${ME_FW_version_new}  ${ME_Version_OS_new}
   END
   Sleep   90
   [Teardown]   remove Athena_G2 BIOS images

CONSR-BMCT-SRTS-0004-0001
    [Documentation]   This test checks BIOS FW Update Stress Test(remote)
    [Tags]   CONSR-BMCT-SRTS-0004-0001      Athena-G2
    FOR    ${INDEX}    IN RANGE    ${MAXINDEX}
       Print Loop Info  ${INDEX}
       Step  1  upgrade_downgrade_bios_FW_remoteOS    Athena_BIOS_Versions_B   oldImage  V3
       Step  2  upgrade_downgrade_bios_FW_remoteOS    Athena_BIOS_Versions_B   newImage  NV
    END

CONSR-BMCT-SRTS-0017-0001
    [Documentation]  This test checks Stress_018_BMC Firmware Update with pc
    [Tags]     CONSR-BMCT-SRTS-0017-0001  Athena-G2
    FOR    ${INDEX}    IN RANGE    ${MAXINDEX}
         Print Loop Info  ${INDEX}
         Step  1  BMC Firmware Update with pc and verify  upgrade
         Step  2  BMC Firmware Update with pc and verify  downgrade
    END

CONSR-BMCT-FWUP-0006-0001
    [Documentation]  This test checks FWFlash_005_CPLD Firmware Update Local and Remote OS
    [Tags]     CONSR-BMCT-FWUP-0006-0001  Athena-G2
    Step  1  CPLD Firware Update with Local OS  upgrade
    Step  2  CPLD Firware Update with Local OS  downgrade
    Step  3  CPLD Firware Update with Remote OS  upgrade
    Step  4  CPLD Firware Update with Remote OS  downgrade

CONSR-BMCT-FWUP-0009-0001
    [Documentation]  This test checks FWFlash_008_Uboot test
    [Tags]     CONSR-BMCT-FWUP-0009-0001  Athena-G2
    Step  1  BMC FWFlash Update with socflash  upgrade

CONSR-BMCT-SRTS-0010-0001
    [Documentation]  This test checks Stress_011_ CPLD update Stress
    [Tags]     CONSR-BMCT-SRTS-0010-0001  Athena-G2
    FOR    ${INDEX}    IN RANGE    ${MAXINDEX}
         Print Loop Info  ${INDEX}
    	 Step  1  CPLD Firware Update with Local OS  upgrade
	 Step  2  CPLD Firware Update with Local OS  downgrade
	 Step  3  CPLD Firware Update with Remote OS  upgrade
	 Step  4  CPLD Firware Update with Remote OS  downgrade
    END

CONSR-BMCT-FWUP-0007-0001
    [Documentation]  This test checks Update bmc firmware with socflash under linux
    [Tags]     CONSR-BMCT-FWUP-0007-0001     Athena-G2
    Step  1    BMC firmware upgrade with socflash  Athena_FW_BMC_B    newImage   BIN   upgrade
    Step  2    BMC firmware upgrade with socflash  Athena_FW_BMC_B    oldImage   BIN   downgrade

CONSR-BMCT-FWUP-0011-0001
    [Documentation]  This test checks FWFlash_010_BMC flash cornel Test
    [Tags]     CONSR-BMCT-FWUP-0011-0001     Athena-G2
    Step  1    Flash bmc and Terminate the flash process during bmc load driver  upgrade
    Step  2    Flash bmc and Terminate the flash process during bmc load driver  downgrade
    Step  3    Flash bmc and Terminate the flash process during bmc load driver  upgrade
    Step  4    Flash bmc and Terminate the flash process during bmc load driver  downgrade

CONSR-BMCT-BSFC-0001-0001
    [Documentation]  This test checks BMC Version
    [Tags]     CONSR-BMCT-BSFC-0001-0001   Athena-G2
    [Timeout]  30 min 00 seconds
    Step  1    get DUT variables Athena
    Step  2    check BMC Version after mc reset warm
    Step  3    check BMC Version after mc reset cold
    Step  4    check BMC Version after mc reset warm ESMB
    Step  5    check BMC Version after mc reset cold ESMB
   
CONSR-BMCT-FWUP-0016-0001
    [Documentation]  This test checks the remote BMC programming functions by dc cycle
    [Tags]     CONSR-BMCT-FWUP-0016-0001    Athena-G2
    [Timeout]  150 min 00 seconds
    [Setup]   Download Athena BMC FW image
    Step  1   get DUT variables Athena
    Step  2   Remote OS with CFUFLASH Update  upgrade
    Step  3   Remote OS with CFUFLASH Update  downgrade
    [Teardown]  Remove Athena BMC FW image

CONSR-BMCT-NTWT-0001-0001
    [Documentation]  This test checks BMC lan static&dhcp function
    [Tags]     CONSR-BMCT-NTWT-0001-0001  Athena-G2
    [Timeout]  30 min 00 seconds
    [Setup]   get DUT variables Athena
    Step  1   OS Connect Device
    Step  2   modify bmc lan static function Athena
    Step  3   OS Disconnect Device
    Step  4   ConnectESMB
    Step  5   modify bmc lan static function Athena
    Step  6   OS Disconnect Device

CONSR-BMCT-BSFC-0003-0001
    [Documentation]  This test checks the Serial over LAN
    [Tags]     CONSR-BMCT-BSFC-0003-0001  Athena-G2
    [Timeout]  90 min 00 seconds
    [Setup]  get DUT variables Athena
    OS Connect Device
    Sub-Case  CONSR-BMCT-BSFC-0003-0001_1  check COM0 BIOS settings Athena
    Sub-Case  CONSR-BMCT-BSFC-0003-0001_2  Enter command to active SOL
    OS Disconnect Device
    ConnectESMB
    Sub-Case  CONSR-BMCT-BSFC-0003-0001_1  check COM0 BIOS settings Athena
    Sub-Case  CONSR-BMCT-BSFC-0003-0001_2  Enter command to active SOL
    OS Disconnect Device

CONSR-BMCT-BSFC-0002-0001
    [Documentation]  This test checks KCS Function
    [Tags]     CONSR-BMCT-BSFC-0002-0001  Athena-G2
    [Timeout]  80 min 00 seconds
    [Setup]  get DUT variables Athena
    OS Connect Device
    Sub-Case   CONSR-BMCT-BSFC-0002-0001_1  check KCS Function
    OS Disconnect Device
    ConnectESMB
    Sub-Case   CONSR-BMCT-BSFC-0002-0001_1  check KCS Function
    OS Disconnect Device

CONSR-BMCT-BSFC-0005-0001
    [Documentation]  This test checks Function_005_User Privilege Check
    [Tags]     CONSR-BMCT-BSFC-0005-0001  Athena-G2
    [Timeout]  40 min 00 seconds
    [Setup]  get DUT variables Athena
    OS Connect Device
    Sub-Case  CONSR-BMCT-BSFC-0005-0001_1  User Privilege Check Athena A
    OS Disconnect Device
    ConnectESMB
    Sub-Case  CONSR-BMCT-BSFC-0005-0001_1  User Privilege Check Athena B
    OS Disconnect Device

CONSR-BMCT-BSFC-0006-0001
    [Documentation]  This test checks Function_006_Power Control
    [Tags]     CONSR-BMCT-BSFC-0006-0001  Athena-G2
    [Timeout]  40 min 00 seconds
    [Setup]  get DUT variables Athena
    OS Connect Device
    Sub-Case  CONSR-BMCT-BSFC-0006-0001_1  Power Control Check Athena A
    OS Disconnect Device
    ConnectESMB
    Sub-Case  CONSR-BMCT-BSFC-0006-0001_1  Power Control Check Athena B
    OS Disconnect Device

CONSR-BMCT-BSFC-0004-0001
    [Documentation]  This test checks User Name and Password Check
    [Tags]     CONSR-BMCT-BSFC-0004-0001  Athena-G2
    [Timeout]  40 min 00 seconds
    [Setup]   get DUT variables Athena
    OS Connect Device
    Sub-Case  CONSR-BMCT-BSFC-0004-0001_1  User Name and Password Check
    OS Disconnect Device
    ConnectESMB
    Sub-Case  CONSR-BMCT-BSFC-0004-0001_1  User Name and Password Check
    OS Disconnect Device

CONSR-BMCT-BSFC-0025-0001
    [Documentation]  This test checks BMC POH status after BMC FW refresh
    [Tags]     CONSR-BMCT-BSFC-0025-0001  Athena-G2
    [Timeout]  720 min 00 seconds
    [Setup]  get DUT variables Athena
    OS Connect Device
    Sub-Case  CONSR-BMCT-BSFC-0025-0001_1  check BMC POH status after BMC FW update Athena A
    OS Disconnect Device
    ConnectESMB
    Sub-Case  CONSR-BMCT-BSFC-0025-0001_1  check BMC POH status after BMC FW update Athena B
    OS Disconnect Device

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

