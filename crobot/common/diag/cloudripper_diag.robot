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
# Script       : Cloudripper_diag.robot                                                                                  #
# Date         : September 3, 2020                                                                                       #
# Author       : hemin                                                                                                   #
# Description  : This script will validate all Diag OS EDA tools                                                      #
#                                                                                                                     #
# Script Revision Details:                                                                                            #

#######################################################################################################################

*** Settings ***
Documentation   This Suite will validate all Diag OS

Library           DiagLibAdapter.py
Variables         Diag_OS_variable.py
Variables         ../sdk/Sdk_variable.py
Library           Keyword_Resource.py
Resource          Resource.robot


Suite Setup       Diag Connect Device
Suite Teardown    Diag Disconnect Device

*** Variables ***
${LoopCnt}        1
${MaxLoopNum}     2

*** Test Cases ***
#### Start - Facebook Common Diag Test Cases #####
FB_DIAG_COMM_TC_000_DIAG_INSTALL_UNINSTALL
    [Documentation]  Synopsis=> This test executes to ensure the DIAG properly version is installed.
    [Tags]  FB_DIAG_COMM_TC_000_DIAG_INSTALL_UNINSTALL  common  cloudripper  critical
    Log Info  ===== Start of testCase FB_DIAG_COMM_TC_000_DIAG_INSTALL_UNINSTALL ====
    FOR    ${INDEX}    IN RANGE    1    ${MaxLoopNum}
        Print Loop Info  ${INDEX}
        Set Testcase Timeout  1800
        Step  1  check diag version before
	Step  2  dhclient to set ipv4 and ipv6
        Step  3  copy diag image files
        Step  4  clean diag rpm
        Step  5  delete the diag on centos
        Critical Step  1  switch to openbmc
        Step  6  delete the diag on openbmc
        Step  7  install diag tools
        Step  8  check diag version
# comment this steps because cloudripper no pem machines --Jeff
        #Step  9  init diag test
        Critical Step  2  switch to openbmc
        Step  9  check openbmc version
    END
    [Teardown]  clear diag files
    Log Info  ===== End of testCase FB_DIAG_COMM_TC_000_DIAG_INSTALL_UNINSTALL ====


FB_DIAG_COMM_TC_001_MANAGEMENT_ETHER_PORT_MAC_CHECK_TEST
    [Documentation]  Synopsis=> This test executes to check that MAC should belong to Quanta.
    [Tags]  FB_DIAG_COMM_TC_001_MANAGEMENT_ETHER_PORT_MAC_CHECK_TEST  common  cloudripper
    Log Info  ===== Start of testCase FB_DIAG_COMM_TC_001_MANAGEMENT_ETHER_PORT_MAC_CHECK_TEST ====
    FOR    ${INDEX}    IN RANGE    1    ${MaxLoopNum}
         Print Loop Info  ${INDEX}
         Set Testcase Timeout  180
         Critical Step  1  switch to centos diag tool
         Step  1  verify mac help dict option h
         Step  2  verify mac help dict option help
         Step  3  verify mac help dict option a
         Step  4  verify mac help dict option all
    END
    Log Info  ===== End of testCase FB_DIAG_COMM_TC_001_MANAGEMENT_ETHER_PORT_MAC_CHECK_TEST ====


FB_DIAG_COMM_TC_002_CPU_Information_TEST
    [Documentation]  Synopsis=> This test executes to check the CPU information with diag script in Linux OS.
    [Tags]  FB_DIAG_COMM_TC_002_CPU_Information_TEST  common  cloudripper
    Log Info  ===== Start of testCase FB_DIAG_COMM_TC_002_CPU_INFORMATION_TEST =====
    FOR    ${INDEX}    IN RANGE    1    ${MaxLoopNum}
        Print Loop Info  ${INDEX}
        Set Testcase Timeout  18000
        Critical Step  1  switch to centos diag tool
        Step  1  verify cpu help dict option h
        Step  2  verify cpu help dict option help
        Step  3  verify cpu help dict option a  True
        Step  4  verify cpu help dict option all  True
        Step  5  verify lscpu info  True
        Step  6  reboot to centos and disable hyper threading
        Step  7  verify cpu help dict option a  False
        Step  8  verify cpu help dict option all  False
        Step  9  reboot to centos and disable hyper threading
        Step  10  verify cpu help dict option a  True
        Step  11  verify cpu help dict option all  True
        Step  12  verify lscpu info  True
    END
    Log Info  ===== End of testCase FB_DIAG_COMM_TC_002_CPU_INFORMATION_TEST =====

FB_DIAG_Cloudripper_TC_002_OOB_Gbe_Switch_Test
    [Documentation]  Synopsis=> This test executes to test the OOB Gbe Switch Test.
    [Tags]  FB_DIAG_Cloudripper_TC_002_OOB_Gbe_Switch_Test  common  cloudripper
    Log Info  ===== Start of testCase FB_DIAG_Cloudripper_TC_002_OOB_Gbe_Switch_Test =====
    FOR    ${INDEX}    IN RANGE    1    ${MaxLoopNum}
         Print Loop Info  ${INDEX}
         Set Testcase Timeout  300
         Critical Step  1  switch To Openbmc Check Tool
         Step  1  verify eth test option h
         Step  2  verify eth test option s
         Step  3  verify eth test option a
         Step  4  ping come usb0 ip
    END
    Log Info  ===== End of testCase FB_DIAG_Cloudripper_TC_002_OOB_Gbe_Switch_Test =====

FB_DIAG_COMM_TC_003_FPGA_TEST
    [Documentation]  Synopsis=> This test executes to check FPGA value read/write correctly
    [Tags]  FB_DIAG_COMM_TC_003_FPGA_TEST  common  cloudripper
    Log Info  ===== Start of testCase FB_DIAG_COMM_TC_003_FPGA_TEST =====
    FOR    ${INDEX}    IN RANGE    1    ${MaxLoopNum}
        Print Loop Info  ${INDEX}
        Set Testcase Timeout  600
        Critical Step  1  switch to centos diag tool
        Step  1  verify fpga help dict option h
        Step  2  verify fpga help dict option help
        Step  3  verify fpga help dict option i
        Step  4  verify fpga help dict option info
        Step  5  verify fpga help dict option a
        Step  6  verify fpga help dict option all
        Step  7  verify fpga help dict option all with config

#        following steps changed to manual.
#        Step  7  handle DOM CPLD scratch  fpga_scm_query_cmd  fpga_scm_init_pattern
#        Step  8  handle DOM CPLD scratch  fpga_smb_query_cmd  fpga_scm_init_pattern
#        Step  9  handle DOM CPLD scratch  fpga_scm_set_cmd  fpga_scm_set_pattern
#        Step  10  handle DOM CPLD scratch  fpga_smb_set_cmd  fpga_smb_set_pattern
#        Step  11  handle DOM CPLD scratch  fpga_scm_query_cmd  fpga_scm_set_pattern
#        Step  12  handle DOM CPLD scratch  fpga_smb_query_cmd  fpga_smb_set_pattern
    END
    Log Info  ===== End of testCase FB_DIAG_COMM_TC_003_FPGA_TEST =====


FB_DIAG_COMM_TC_004_DIMM_SPD_TEST
    [Documentation]  Synopsis=> This test executes to verify the main information of memory.
    [Tags]  FB_DIAG_COMM_TC_004_DIMM_SPD_TEST  common  cloudripper
    Log Info  ===== Start of testCase FB_DIAG_COMM_TC_004_DIMM_SPD_TEST =====
    FOR    ${INDEX}    IN RANGE    1    ${MaxLoopNum}
        Print Loop Info  ${INDEX}
        Set Testcase Timeout  600
        Critical Step  1  switch to centos diag tool
        Step  1  verify mem help dict option h
        Step  2  verify mem help dict option help
        Step  3  verify mem help dict option K
        Step  4  verify mem help dict option check
        Step  5  verify mem help dict option a
        Step  6  verify mem help dict option all
        Step  7  verify meminfo dmidecode
    END
    Log Info  ===== End of testCase FB_DIAG_COMM_TC_004_DIMM_SPD_TEST =====


FB_DIAG_COMM_TC_005_USB_STORAGE_TEST
    [Documentation]  Synopsis=> This test executes to check the information of USB storage.
    [Tags]  FB_DIAG_COMM_TC_005_USB_Storage_TEST  common  cloudripper
    Log Info  ===== Start of testCase FB_DIAG_COMM_TC_005_USB_STORAGE_TEST =====
    FOR    ${INDEX}    IN RANGE    1    ${MaxLoopNum}
        Print Loop Info  ${INDEX}
        Set Testcase Timeout  300
        Critical Step  1  switch to centos diag tool
        Step  1  verify usb help dict option h
        Step  2  verify usb help dict option help
        Step  3  verify usb help dict option i
        Step  4  verify usb help dict option info
        Step  5  verify usb smart a
        Step  6  verify usb smart l
        Step  7  verify usb help dict option a
        Step  8  verify usb help dict option all
        Step  9  verify file is removed
    END
    Log Info  ===== End of testCase FB_DIAG_COMM_TC_005_USB_STORAGE_TEST =====


FB_DIAG_COMM_TC_006_RTC_Test
    [Documentation]  Synopsis=> This test executes to check the RTC date&time.
    [Tags]  FB_DIAG_COMM_TC_006_RTC_Test  common  cloudripper
    Log Info  ===== Start of testCase FB_DIAG_COMM_TC_006_RTC_TEST =====
    FOR    ${INDEX}    IN RANGE    1    ${MaxLoopNum}
        Print Loop Info  ${INDEX}
        Set Testcase Timeout  600
        Critical Step  1  switch to centos diag tool
        Step  1  verify RTC help dict option h
        Step  2  verify RTC help dict option help
        Step  3  verify RTC help dict option a
        Step  4  verify RTC help dict option all
        Step  5  verify RTC help dict option r
        Step  6  verify RTC help dict option read
        Step  7  verify RTC help dict option w
        Step  8  verify RTC help dict option write
        Step  9  verify RTC help dict option w data
        Step  10  power cycle device to openbmc
        Step  11  switch to centos diag tool
        Step  12  verify RTC help dict option r
        Step  13  verify RTC help dict option read
    END
    Log Info  ===== End of testCase FB_DIAG_COMM_TC_006_RTC_Test =====

FB_DIAG_COMM_TC_008_Firmware/Software_Information_Test
    [Documentation]  Synopsis=> This test executes to verify the firmware/software information test
    [Tags]  FB_DIAG_COMM_TC_008_Firmware/Software_Information_Test  common  cloudripper
    Log Info  ===== Start of testCase FB_DIAG_COMM_TC_008_Firmware/Software_Information_Test =====
    FOR    ${INDEX}    IN RANGE    1    ${MaxLoopNum}
        Print Loop Info  ${INDEX}
        Set Testcase Timeout  600
        Critical Step  1  switch to centos diag tool
        Step  1  verify cel version option h
        Step  2  verify cel version option help
        Step  3  verify cel version test S verify fpga
        Step  4  verify cel version test option show verify fpga
        Step  5  cat proc version
        Step  6  cat etc redhat release
        Step  7  check the cpu os version
        Step  8  cloudripper run eeupdate64e nic2 adapterinfo
        Critical Step  1  switch to openbmc check tool
        Step  9  check the openbmc version
        Step  10  cpld ver sh
        Step  11  fpga ver sh
        Step  12  fw util all version
    END
    Log Info  ===== End of testCase FB_DIAG_COMM_TC_008_Firmware/Software_Information_Test =====

FB_DIAG_COMM_TC_010_TPM_TEST
    [Documentation]  Synopsis=> This test executes to check TPM verison.
    [Tags]  FB_DIAG_COMM_TC_010_TPM_TEST  common  cloudripper
    Log Info  ===== Start of testCase FB_DIAG_COMM_TC_010_TPM_TEST =====
    FOR    ${INDEX}    IN RANGE    1    ${MaxLoopNum}
         Print Loop Info  ${INDEX}
         Set Testcase Timeout  300
         Critical Step  1  switch to centos diag tool
         Step  1  verify tpm help dict option h
         Step  2  verify tpm help dict option help
         Step  3  verify tpm help dict option a
         Step  4  verify tpm help dict option all
	 Step  5  config configs yaml file
         Step  6  read eltt2 pcr
    END
    Log Info  ===== End of testCase FB_DIAG_COMM_TC_010_TPM_TEST =====


FB_DIAG_COMM_TC_011_BIC_Test
    [Documentation]  Synopsis=> This test executes to check BIC verison.
    [Tags]  FB_DIAG_COMM_TC_011_BIC_Test  common  cloudripper
    Log Info  ===== Start of testCase FB_DIAG_COMM_TC_011_BIC_Test =====
    Set Test Variable     ${timeout}    300
    FOR    ${INDEX}    IN RANGE    1    ${MaxLoopNum}
        Print Loop Info  ${INDEX}
        Set Testcase Timeout  300
        Critical Step  1  switch to centos diag tool
        Step  1  verify cel version test S verify fpga
        Step  2  verify cel version test option show verify fpga
        Step  3  cat etc issue bmc
    END
    Log Info  ===== End of testCase FB_DIAG_COMM_TC_011_BIC_Test =====


FB_DIAG_COMM_TC_012_NVME_SSD_TEST
    [Documentation]  Synopsis=> This test executes to check the information of NVMe Disk.
    [Tags]  FB_DIAG_COMM_TC_012_NVME_SSD_TEST  common  cloudripper
    Log Info  ===== Start of testCase FB_DIAG_COMM_TC_012_NVME_SSD_TEST =====
    Set Test Variable     ${timeout}    300
    FOR    ${INDEX}    IN RANGE    1    ${MaxLoopNum}
        Print Loop Info  ${INDEX}
        Set Testcase Timeout  300
        Critical Step  1  switch to centos diag tool
        Step  1  verify nvme help dict option h
        Step  2  verify nvme help dict option help
        Step  3  verify nvme help dict option i
        Step  4  verify nvme help dict option info
        Step  5  verify nvme smart tool and log
        Step  6  verify nvme help dict option a
        Step  7  verify nvme help dict option all
        Step  8  verify nvme test file is removed
    END
    Log Info  ===== End of testCase FB_DIAG_COMM_TC_012_NVME_SSD_TEST =====


FB_DIAG_COMM_TC_014_QSFP_TEST
    [Documentation]  Synopsis=> This test executes to test the QSFP.
    [Tags]  FB_DIAG_COMM_TC_014_QSFP_TEST  common  cloudripper
    Log Info  ===== Start of testCase FB_DIAG_COMM_TC_014_QSFP_TEST =====
    FOR    ${INDEX}    IN RANGE    1    ${MaxLoopNum}
        Print Loop Info  ${INDEX}
        Set Testcase Timeout  3000
        Critical Step  1  switch to centos diag tool
        Step  1  cel qsfp test h
        Step  2  cel qsfp test help
        Step  3  cel qsfp test set reset  off
        Step  4  cloudripper cel qsfp test p 0 s  ${cel_qsfp_test_port_status_default}
        Step  5  cloudripper cel qsfp test port 0 status  ${cel_qsfp_test_port_status_default}
        Step  6  cloudripper cel qsfp test check port status one by one
        Step  7  cloudripper cel qsfp test check port s one by one
        Step  8  cloudripper cel qsfp test check port i one by one
	Step  9  cloudripper cel qsfp test check port info one by one
	Step  10  cloudripper cel qsfp test check port is one by one
	Step  11  cloudripper cel qsfp test check port Simple one by one
        Step  12  cel qsfp test set reset  off
        Step  13  cloudripper cel qsfp test p 0 s  ${cel_qsfp_test_port_status_pattern_reset_off}
        Step  14  cel qsfp test set reset  on
        Step  15  cloudripper cel qsfp test p 0 s  ${cel_qsfp_test_port_status_pattern_reset_on}
        Step  16  cel qsfp test set lpmode  off
        Step  17  cloudripper cel qsfp test p 0 s  ${cel_qsfp_test_port_status_pattern_lpmode_off}
        Step  18  cel qsfp test set lpmode  on
        Step  19  cloudripper cel qsfp test p 0 s  ${cel_qsfp_test_port_status_pattern_lpmode_on}
        Step  20  cel qsfp test set reset  on
        Step  21  cloudripper cel qsfp test p 0 s  ${cel_qsfp_test_port_status_pattern_reset_on}
        Step  22  cel qsfp test set reset  off
        Step  23  cel qsfp test set lpmode  on
        Step  24  cloudripper cel qsfp test p 0 s  ${cel_qsfp_test_port_status_pattern_lpmode_on}
        Step  25  cel qsfp test set lpmode  off
        Step  26  cel qsfp test all
        Step  27  verify QSFP automaticaly  option=-K  regex=${cel_qsfp_test_K_pattern}
        Step  28  verify QSFP automaticaly  option=--check  regex=${cel_qsfp_test_K_pattern}
    END
    [Teardown]  cel qsfp test set default
    Log Info  ===== End of testCase FB_DIAG_COMM_TC_014_QSFP_TEST =====

FB_DIAG_COMM_TC_015_CPLD_TEST
    [Documentation]  Synopsis=> This test executes to check CPLD.
    [Tags]  FB_DIAG_COMM_TC_015_CPLD_TEST  common  cloudripper
    Log Info  ===== Start of testCase FB_DIAG_COMM_TC_015_CPLD_TEST =====
    FOR    ${INDEX}    IN RANGE    1    ${MaxLoopNum}
         Print Loop Info  ${INDEX}
         Set Testcase Timeout  300
         Critical Step  1  switch to centos
         Step  1  verify cpld help dict option h
         Step  2  verify cpld help dict option help
         Step  3  verify_cpld_help_dict_option_a
         Step  4  verify_cpld_help_dict_option_all
    END
    Log Info  ===== End of testCase FB_DIAG_COMM_TC_015_CPLD_TEST =====


FB_DIAG_COMM_TC_016_E_Loopback_High_power_mode
    [Documentation]  Synopsis=> Check tool can find in Diag path and check high power mode
    [Tags]  FB_DIAG_COMM_TC_016_E_Loopback_High_power_mode  common  cloudripper
    Log Info  ===== Start of testCase FB_DIAG_COMM_TC_016_E_Loopback_High_power_mode =====
    FOR    ${INDEX}    IN RANGE    1    ${MaxLoopNum}
         Print Loop Info  ${INDEX}
         Set Testcase Timeout  300
         Critical Step  1  switch to centos diag system_log
         Step  1  set E Loopback to high power mode
    END
    Log Info  ===== End of testCase FB_DIAG_COMM_TC_016_E_Loopback_High_power_mode =====


FB_DIAG_COMM_TC_017_RJ45_MANAGEMENT_PORT_CONNECT_TEST
    [Documentation]  Synopsis=> This test executes to check RJ45 for Management eth port. Ping remote PC from DUT.
    [Tags]  FB_DIAG_COMM_TC_017_RJ45_MANAGEMENT_PORT_CONNECT_TEST  common  cloudripper
    Log Info  ===== Start of testCase FB_DIAG_COMM_TC_017_RJ45_MANAGEMENT_PORT_CONNECT_TEST =====
    Set Test Variable     ${timeout}    300
    FOR    ${INDEX}    IN RANGE    1    ${MaxLoopNum}
         Print Loop Info  ${INDEX}
         Set Testcase Timeout  300
         Step  1  switch to centos
         Step  2  check and ping server ip from centos
    END
    Log Info  ===== End of testCase FB_DIAG_COMM_TC_017_RJ45_MANAGEMENT_PORT_CONNECT_TEST =====


FB_DIAG_COMM_TC_018_CPU_STRESS_TEST
    [Documentation]  Synopsis=> This test executes to check CPU Stress
    [Tags]  FB_DIAG_COMM_TC_018_CPU_STRESS_TEST  common  cloudripper
    Log Info  ===== Start of testCase FB_DIAG_COMM_TC_018_CPU_STRESS_TEST =====
    FOR    ${INDEX}    IN RANGE    1    ${MaxLoopNum}
        Print Loop Info  ${INDEX}
        Set Testcase Timeout  600
        Critical Step  1  switch to centos diag tool
        Step  1  run mcelog under daemon mode
        Step  2  test cpu stress
        Step  3  check MCE log
    END
    Log Info  ===== End of testCase FB_DIAG_COMM_TC_018_CPU_STRESS_TEST =====


FB_DIAG_COMM_TC_020_DDR_STRESS_TEST
    [Documentation]  Synopsis=> This test executes to check DDR Stress
    [Tags]  FB_DIAG_COMM_TC_020_DDR_STRESS_TEST  common  cloudripper
    Log Info  ===== Start of testCase FB_DIAG_COMM_TC_020_DDR_STRESS_TEST =====
    FOR    ${INDEX}    IN RANGE    1    ${MaxLoopNum}
         Print Loop Info  ${INDEX}
         Set Testcase Timeout  1200
         Critical Step  1  switch to centos diag tool
         Step  1  run mcelog under daemon mode
         Step  2  test ddr stress
         Step  3  check MCE log
    END
    Log Info  ===== End of testCase FB_DIAG_COMM_TC_020_DDR_STRESS_TEST =====


FB_DIAG_COMM_TC_021_SSD_STRESS_TEST
    [Documentation]  Synopsis=> This test executes to check SSD Stress
    [Tags]  FB_DIAG_COMM_TC_021_SSD_STRESS_TEST  common  cloudripper
    Log Info  ===== Start of testCase FB_DIAG_COMM_TC_021_SSD_STRESS_TEST =====
    FOR    ${INDEX}    IN RANGE    1    ${MaxLoopNum}
         Print Loop Info  ${INDEX}
         Set Testcase Timeout  600
         Critical Step  1  switch to centos diag tool
         Step  1  run mcelog under daemon mode
         Step  2  test ssd stress
         Step  3  check MCE log
    END
    Log Info  ===== End of testCase FB_DIAG_COMM_TC_021_SSD_STRESS_TEST =====

FB_DIAG_COMM_TC_022_PCIE_STRESS_TEST
    [Documentation]  Synopsis=> This test executes to check PCIE Stress
    [Tags]  FB_DIAG_COMM_TC_022_PCIE_STRESS_TEST  common  cloudripper
    Log Info  ===== Start of testCase FB_DIAG_COMM_TC_022_PCIE_STRESS_TEST =====
    FOR    ${INDEX}    IN RANGE    1    ${MaxLoopNum}
         Print Loop Info  ${INDEX}
         Set Testcase Timeout  600
         Critical Step  1  switch to centos diag tool
         Step  1  run mcelog under daemon mode
         Step  2  check sys before log  False
         Step  3  test pcie stress
         Step  4  check sys after log  False
    END
    Log Info  ===== End of testCase FB_DIAG_COMM_TC_022_PCIE_STRESS_TEST =====


FB_DIAG_COMM_TC_024_SYSTEM_LOG_CHECK_TEST
    [Documentation]  Synopsis=> This test executes to check System log
    [Tags]  FB_DIAG_COMM_TC_024_System_log_check_Test  common  cloudripper
    Log Info  ===== Start of testCase FB_DIAG_COMM_TC_024_SYSTEM_LOG_CHECK_TEST =====
    FOR    ${INDEX}    IN RANGE    1    ${MaxLoopNum}
         Print Loop Info  ${INDEX}
         Set Testcase Timeout  300
         Critical Step  1  switch to centos diag system log
         Step  1  verify diag system log help dict option h
         Step  2  check sys before log  False
         Step  3  run system load stress  False
         Step  4  check sys after log  False
         Step  5  clean system logs  False

    END
    Log Info  ===== End of testCase FB_DIAG_COMM_TC_024_SYSTEM_LOG_CHECK_TEST =====

FB_DIAG_COMM_TC_033_FRU_EEPROM_UPDATE
    [Documentation]  Synopsis=> This test check the function of FRU eeprom update.
    [Tags]  FB_DIAG_COMM_TC_033_FRU_EEPROM_UPDATE  common  cloudripper
    Log Info  ===== Start of testCase FB_DIAG_COMM_TC_033_FRU_EEPROM_UPDATE =====
    FOR    ${INDEX}    IN RANGE    1    ${MaxLoopNum}
        Print loop info  ${INDEX}
        Set testcase timeout  3000
        Critical Step  1  switch to openbmc check tool
        Step  1  verify eeprom tool help dict option h
        Step  2  verify SCM eeprom tool update
        Step  3  verify FCM eeprom tool update
        Step  4  verify SMB eeprom tool update
        Step  5  verify FAN eeprom tool update
        #Step  6  verify eeprom tool BSM info
    END
    Log Info  ===== End of testCase FB_DIAG_COMM_TC_033_FRU_EEPROM_UPDATE =====

FB_DIAG_COMM_TC_036_BMC_BIOS_BOOT_TEST
    [Documentation]  Synopsis=> This test check the function of BIOS booting test.
    [Tags]  FB_DIAG_COMM_TC_036_BMC_BIOS_BOOT_TEST  common  cloudripper
    Log Info  ===== Start of testCase FB_DIAG_COMM_TC_036_BMC_BIOS_BOOT_TEST =====
    FOR    ${INDEX}    IN RANGE    1    ${MaxLoopNum}
        Print loop info  ${INDEX}
        Set testcase timeout  3000
        Critical Step  1  switch to openbmc check tool
        Step  2  verify bmc cel boot test h
        Step  3  verify cel boot test b bmc s master
        Step  4  verify cel boot test b bmc r slave
        Step  5  wait for openbmc prompt back
        Step  6  verify cel boot test b bmc s slave
        Step  7  verify cel boot test b bmc r master
        Step  8  wait for openbmc prompt back
        Step  9  verify cel boot test b bmc s master
        Step  10  make sure bios boot from master
        Step  11  verify boot info bios master
        Step  12  verify cel boot test b bios r slave
        Step  13  verify boot info bios slave
	Step  14  wait for centos prompt back
        Step  15  verify cel boot test b bios r master
        Step  16  verify boot info bios master
	Step  17  wait for centos prompt back
        Step  18  verify cel boot test a
        Step  19  verify cel boot test b bios r slave
        Step  20  verify boot info bios slave
	Step  21  wait for centos prompt back
        Step  22  verify cel boot test a bios fail
        Step  23  verify cel boot test b bmc r slave
        Step  24  wait for openbmc prompt back
        Step  25  verify cel boot test b bmc s slave
	Step  26  verify cel boot test b bmc r master
        Step  27  wait for openbmc prompt back
	Step  28  verify cel boot test b bmc s master
	Step  29  verify cel boot test b bios r master
	Step  30  verify boot info bios master
	Step  31  wait for centos prompt back
    END
    Log Info  ===== End of testCase FB_DIAG_COMM_TC_036_BMC_BIOS_BOOT_TEST =====

FB_DIAG_COMM_TC_037_BMC_CPU_TEST
    [Documentation]  Synopsis=> This test executes to check if the main information of BMC CPU is correct.
    [Tags]  FB_DIAG_COMM_TC_037_BMC_CPU_TEST  common  cloudripper
    Log Info  ===== Start of testCase FB_DIAG_COMM_TC_037_BMC_CPU_TEST =====
    FOR    ${INDEX}    IN RANGE    1    ${MaxLoopNum}
        Print Loop Info  ${INDEX}
        Set Testcase Timeout  300
        Critical Step  1  switch to openbmc check tool
        Step  1  verify bmc cpu help dict option h
        Step  2  verify bmc cpu help dict option i
        Step  3  compare bmc cpu info and option i
        Step  4  verify bmc cpu help dict option a
        Step  5  verify bmc top
    END
    Log Info  ===== End of testCase FB_DIAG_COMM_TC_037_BMC_CPU_TEST =====


FB_DIAG_COMM_TC_038_BMC_FPGA_TEST
    [Documentation]  Synopsis=> This test executes to check if the main information of BMC FPGA is correct.
    [Tags]  FB_DIAG_COMM_TC_038_BMC_FPGA_TEST  common  cloudripper
    Log Info  ===== Start of testCase FB_DIAG_COMM_TC_038_BMC_FPGA_TEST =====
    FOR    ${INDEX}    IN RANGE    1    ${MaxLoopNum}
         Print Loop Info  ${INDEX}
         Set Testcase Timeout  300
         Critical Step  1  switch to openbmc check tool
         Step  1  verify bmc fpga help dict option h
         Step  2  verify bmc fpga 1 device write read
         Step  3  verify bmc fpga 2 device write read
         Step  4  verify bmc fpga help dict option a
         Step  5  verify bmc fpga help dict option v
	 Step  6  verify bmc fpga help dict option k
    END

    Log Info  ===== End of testCase FB_DIAG_COMM_TC_038_BMC_FPGA_TEST =====


FB_DIAG_COMM_TC_039_BMC_CPLD_TEST
    [Documentation]  Synopsis=> This test executes to check if the main information of BMC CPLD is correct.
    [Tags]  FB_DIAG_COMM_TC_039_BMC_CPLD_TEST  common  cloudripper
    Log Info  ===== Start of testCase FB_DIAG_COMM_TC_039_BMC_CPLD_TEST =====
    FOR    ${INDEX}    IN RANGE    1    ${MaxLoopNum}
         Print Loop Info  ${INDEX}
         Set Testcase Timeout  300
         Critical Step  1  switch to openbmc check tool
         Step  1  verify bmc cpld help dict option h
         Step  2  verify bmc fcm cpld device write read
         Step  3  verify bmc scm cpld device write read
         Step  4  verify bmc smb cpld device write read
         Step  5  verify bmc smb pwr cpld device write read
         Step  6  verify bmc cpld help dict option a
         Step  7  verify bmc cpld help dict option v
    END
    Log Info  ===== End of testCase FB_DIAG_COMM_TC_039_BMC_CPLD_TEST =====

FB_DIAG_COMM_TC_040_I2C_DEVICE_TEST
    [Documentation]  Synopsis=> This test executes to detect all the I2C devices.
    [Tags]  FB_DIAG_COMM_TC_040_I2C_DEVICE_TEST  common  cloudripper
    Log Info  ===== Start of testCase FB_DIAG_COMM_TC_040_I2C_DEVICE_TEST =====
    FOR    ${INDEX}    IN RANGE    1    ${MaxLoopNum}
         Print Loop Info  ${INDEX}
         Set Testcase Timeout  600
	 Critical Step  1  switch to openbmc check tool
         Step  1  verify bmc i2c help dict option h
         Step  2  verify bmc i2c help dict option s
         Step  3  verify bmc i2c help dict option s  -b SCM
         Step  4  verify bmc i2c help dict option s  -b SMB
         Step  5  verify bmc i2c help dict option s  -b FCM
         Step  6  verify bmc i2c help dict option s  -b PDBB
         Step  7  verify bmc i2c help dict option s  -b PDBT
	 Step  8  verify bmc i2c help dict option s  -b RUNBMC
         Step  8  verify bmc i2c help dict option l
         Step  9  verify bmc i2c help dict option l  -b SCM
         Step  10  verify bmc i2c help dict option l  -b SMB
         Step  11  verify bmc i2c help dict option l  -b FCM
         Step  12  verify bmc i2c help dict option l  -b PDBB
         Step  13  verify bmc i2c help dict option l  -b PDBT
	 Step  14  verify bmc i2c help dict option l  -b RUNBMC
         Step  14  verify bmc i2c help dict option a
    END
    Log Info  ===== End of testCase FB_DIAG_COMM_TC_040_I2C_DEVICE_TEST =====
FB_DIAG_COMM_TC_041_FAN_TEST
    [Documentation]  Synopsis=> This test executes to test the fan.
    [Tags]  FB_DIAG_COMM_TC_041_FAN_TEST  common  cloudripper
    Log Info  ===== Start of testCase FB_DIAG_COMM_TC_041_FAN_TEST =====
    FOR    ${INDEX}    IN RANGE    1    ${MaxLoopNum}
         Print Loop Info  ${INDEX}
         Set Testcase Timeout  300
         Critical Step  1  switch To Openbmc Check Tool
         Step  1  collect all fan manufacturer is present
         Step  2  verify cel fan test c
         Step  3  verify cel fan test h
         Step  4  verify cel fan test g
         Step  5  verify cel fan test s
         Step  6  verify cel fan test p 10
         Step  7  verify cel fan test g p 10
         Step  8  verify cel fan test p 100
         Step  9  verify cel fan test g p 100
         Step  10  verify cel fan test p 50
         Step  11  verify cel fan test g p 50
         Step  12  verify cel fan test a
         Step  13  verify cel fan test e
    END
    Log Info  ===== End of testCase FB_DIAG_COMM_TC_041_FAN_TEST =====

FB_DIAG_COMM_TC_042_MEMORY_TEST
    [Documentation]  Synopsis=> This test executes to test the fan.
    [Tags]  eric42  FB_DIAG_COMM_TC_042_MEMORY_TEST  common  cloudripper
    Log Info  ===== Start of testCase FB_DIAG_COMM_TC_042_MEMORY_TEST =====
    FOR    ${INDEX}    IN RANGE    1    ${MaxLoopNum}
         Print Loop Info  ${INDEX}
         Set Testcase Timeout  780
         Critical Step  1  switch To Openbmc Check Tool
         Step  1  cel memory test h
         Step  2  cel memory test i
         Step  3  cel memory test m
         Step  4  cel memory test a
         Step  5  cel memory info compare
    END
    Log Info  ===== End of testCase FB_DIAG_COMM_TC_042_MEMORY_TEST =====


FB_DIAG_COMM_TC_043_EMMC_TEST
    [Documentation]  Synopsis=> This test executes to test the fan.
    [Tags]  FB_DIAG_COMM_TC_043_EMMC_TEST  common  cloudripper
    Log Info  ===== Start of testCase FB_DIAG_COMM_TC_043_EMMC_TEST =====
    FOR    ${INDEX}    IN RANGE    1    ${MaxLoopNum}
         Print Loop Info  ${INDEX}
         Set Testcase Timeout  300
         Critical Step  1  switch To Openbmc Check Tool
         Step  1  cel emmc test h
         Step  2  cel emmc test i
         #Step  3  cel emmc info compare
         Step  3  cel emmc test s
         Step  4  cel emmc test a
         #Step  5  verify a disk.dump file was removed after ran "cel-emmc-test -a"
    END
    Log Info  ===== End of testCase FB_DIAG_COMM_TC_043_MEMORY_TEST =====


FB_DIAG_COMM_TC_044_INTERNAL_UART_TEST
    [Documentation]  Synopsis=> This test executes to test the SCM and FCM hot_swap function.
    [Tags]  FB_DIAG_COMM_TC_044_INTERNAL_UART_TEST  common  cloudripper
    Log Info  ===== Start of testCase FB_DIAG_COMM_TC_044_INTERNAL_UART_TEST ====
    FOR    ${INDEX}    IN RANGE    1    ${MaxLoopNum}
         Print Loop Info  ${INDEX}
         Set Testcase Timeout  300
         Critical Step  1  switch To Openbmc
         Step  1  check the cpu os version
         Step  2  check the bmc version
    END
    Log Info  ===== End of testCase FB_DIAG_COMM_TC_044_INTERNAL_UART_TEST ====


FB_DIAG_COMM_TC_046_HOT_SWAP_CONTROLLER_ACCESS_TEST
    [Documentation]  Synopsis=> This test executes to test the SCM and FCM hot_swap function.
    [Tags]  FB_DIAG_COMM_TC_046_HOT_SWAP_CONTROLLER_ACCESS_TEST  common  cloudripper
    Log Info  ===== Start of testCase FB_DIAG_COMM_TC_046_HOT_SWAP_CONTROLLER_ACCESS_TEST =====
    FOR    ${INDEX}    IN RANGE    1    ${MaxLoopNum}
         Print Loop Info  ${INDEX}
         Set Testcase Timeout  300
         Critical Step  1  switch To Openbmc Check Tool
         Step  1  cel hotswap test h
         Step  2  cel hotswap test a
         #Step  3  i2cset scm hotswap
         #Step  4  i2cset fcm hotswap
    END
    Log Info  ===== End of testCase FB_DIAG_COMM_TC_046_HOT_SWAP_CONTROLLER_ACCESS_TEST =====


FB_DIAG_COMM_TC_047_TPM_DEVICE_ACCESS_TEST
    [Documentation]  Synopsis=> This test executes to test the TPM function.
    [Tags]  FB_DIAG_COMM_TC_047_TPM_DEVICE_ACCESS_TEST  common  cloudripper
    Log Info  ===== Start of testCase FB_DIAG_COMM_TC_047_TPM_DEVICE_ACCESS_TEST =====
    FOR    ${INDEX}    IN RANGE    1    ${MaxLoopNum}
         Print Loop Info  ${INDEX}
         Set Testcase Timeout  300
         Critical Step  1  switch To Openbmc Check Tool
         Step  1  cel tpm test h
         Step  2  cel tpm test i
         Step  3  cel tpm test a
    END
    Log Info  ===== End of testCase FB_DIAG_COMM_TC_047_TPM_DEVICE_ACCESS_TEST =====

FB_DIAG_COMM_TC_049_PSU_TEST
    [Documentation]  Synopsis=> This test executes to test the PSU function.
    [Tags]  FB_DIAG_COMM_TC_049_PSU_TEST  common  cloudripper
    Log Info  ===== Start of testCase FB_DIAG_COMM_TC_049_PSU_TEST =====
    FOR    ${INDEX}    IN RANGE    1    ${MaxLoopNum}
         Print Loop Info  ${INDEX}
         Set Testcase Timeout  300
         Critical Step  1  switch To Openbmc Check Tool
         Step  1  cel psu test h
         Step  2  cloudripper cel psu test s
         Step  3  cel psu test i
         Step  4  cel psu test a
         Step  5  psu util psu1 get psu info
         Step  6  psu util psu1 get eeprom info
         Step  7  psu util psu2 get psu info
         Step  8  psu util psu2 get eeprom info
         Step  9  compare psu info diag and openbmc tools
    END
    Log Info  ===== End of testCase FB_DIAG_COMM_TC_049_PSU_TEST =====

FB_DIAG_COMM_TC_050_SENSOR_TEST
    [Documentation]  Synopsis=> This test executes to test the sensor function.
    [Tags]  ericzhang  FB_DIAG_COMM_TC_050_SENSOR_TEST  common  cloudripper
    Log Info  ===== Start of testCase FB_DIAG_COMM_TC_050_SENSOR_TEST =====
        Set Testcase Timeout  3000
        Critical Step  1  switch to centos diag system log
        Step  2  run sdk init without exit
        Step  3  cel sensor test h
        Step  4  cel sensor test s with high power
        Step  5  cel sensor test a with high power
        Step  6  cel sensor test u with high power
        Step  7  sensor util all threshold with high power
        Step  8  sensors with high power
        Step  9  exit sdk init mode
    Log Info  ===== End of testCase FB_DIAG_COMM_TC_050_SENSOR_TEST =====

FB_DIAG_COMM_TC_051_RJ45_MANAGEMENT_PORT_CONNECT_TEST
    [Documentation]  Synopsis=> This test executes to check RJ45 for Management eth port. Ping remote PC from DUT.
    [Tags]  FB_DIAG_COMM_TC_051_RJ45_MANAGEMENT_Port_CONNECT_TEST  common  cloudripper
    Log Info  ===== Start of testCase FB_DIAG_COMM_TC_051_RJ45_MANAGEMENT_PORT_CONNECT_TEST =====
    Set Test Variable     ${timeout}    300
    FOR    ${INDEX}    IN RANGE    1    ${MaxLoopNum}
        Print Loop Info  ${INDEX}
        Set Testcase Timeout  300
        Step  1  get ip and ping
    END
    Log Info  ===== End of testCase FB_DIAG_COMM_TC_051_RJ45_MANAGEMENT_PORT_CONNECT_TEST =====

FB_DIAG_COMM_TC_053_FIRMWARE_SOFTWARE_TEST
    [Documentation]  Synopsis=> This test executes to verify the firmware and software version.
    [Tags]  FB_DIAG_COMM_TC_053_FIRMWARE_SOFTWARE_TEST  common  cloudripper
    Log Info  ===== Start of testCase FB_DIAG_COMM_TC_053_FIRMWARE_SOFTWARE_TEST =====
    FOR    ${INDEX}    IN RANGE    1    ${MaxLoopNum}
         Print Loop Info  ${INDEX}
         Set Testcase Timeout  300
         Critical Step  1  switch To Openbmc Check Tool
         Step  1  cel software test h
         Step  2  cel software test i
         Step  3  cel software test v
         Step  4  cel software test a
         Step  6  cat etc issue bmc
         Step  7  cpld ver sh
         Step  8  fpga ver sh
    # ***Need to install DiagOS version 3.0***
         Step  9  cat etc product version
    END
    Log Info  ===== End of testCase FB_DIAG_COMM_TC_053_FIRMWARE_SOFTWARE_TEST =====

FB_DIAG_COMM_TC_054_PLATFORM_TEST
    [Documentation]  Synopsis=> This test executes to test all platform function.
    [Tags]  FB_DIAG_COMM_TC_054_PLATFORM_TEST  common  cloudripper
    Log Info  ===== Start of testCase FB_DIAG_COMM_TC_054_PLATFORM_TEST =====
    FOR    ${INDEX}    IN RANGE    1    ${MaxLoopNum}
         Print Loop Info  ${INDEX}
         Set Testcase Timeout  300
         Critical Step  1  switch To Openbmc Check Tool
         Step  1  cel platform test h
         Step  2  cel platform test i
         Step  3  cel platform test a
    # ***PEM2 not present***
         Step  4  cel platform test e all
         Step  5  cel platform test e fcm
         Step  6  cel platform test e fan1
         Step  7  cel platform test e fan2
         Step  8  cel platform test e fan3
         Step  9  cel platform test e fan4
         Step  10  cel platform test e smb
         Step  11  cel platform test e scm
    # ***PEM2 not present***
         Step  12  cel platform test e pem
    END
    Log Info  ===== End of testCase FB_DIAG_COMM_TC_054_PLATFORM_TEST =====

FB_DIAG_COMM_TC_056_DDR_AND_EMMC_STRESS_TEST
    [Documentation]  Synopsis=> This test executes to test the DDR and eMMC memory.
    [Tags]  FB_DIAG_COMM_TC_056_DDR_AND_EMMC_STRESS_TEST  common  cloudripper
    Log Info  ===== Start of testCase FB_DIAG_COMM_TC_056_DDR_AND_EMMC_STRESS_TEST =====
    FOR    ${INDEX}    IN RANGE    1    ${MaxLoopNum}
         Print Loop Info  ${INDEX}
         Set Testcase Timeout  300
         Critical Step  1  switch To Openbmc Check Tool
         Step  1  disable watchdog for ddr test
         Step  2  remove ddr log
         Step  3  ddr test sh
    END
    Log Info  ===== End of testCase FB_DIAG_COMM_TC_056_DDR_AND_EMMC_STRESS_TEST =====

FB_DIAG_COMM_TC_058_BIOS_CONFIG_CHECK_TEST
    [Documentation]  Synopsis=> This test executes to check the BIOS config.
    [Tags]  FB_DIAG_COMM_TC_058_BIOS_CONFIG_CHECK_TEST  common  cloudripper
    Log Info  ===== Start of testCase FB_DIAG_COMM_TC_058_BIOS_CONFIG_CHECK_TEST =====
    FOR    ${INDEX}    IN RANGE    1    ${MaxLoopNum}
         Print Loop Info  ${INDEX}
         Set Testcase Timeout  3000
         Critical Step  1  switch To Openbmc Check Tool
         Step  1  copy bios config files
         Step  2  verify bios check tool help dict
         Step  3  check bios default config
         Step  4  reboot and reset bios setup bootorder 1st
         Step  5  verify bios modified info
         Step  6  reboot and reset bios setup to default
         Step  7  check bios default config
    END
    Log Info  ===== End of testCase FB_DIAG_COMM_TC_058_BIOS_CONFIG_CHECK_TEST =====


FB_DIAG_COMM_TC_057_SYSTEM_LOG_CHECK_TEST
    [Documentation]  Synopsis=> This test executes to verify the syslog utility.
    [Tags]  FB_DIAG_COMM_TC_057_SYSTEM_LOG_CHECK_TEST  common  cloudripper
    Log Info  ===== Start of testCase FB_DIAG_COMM_TC_057_SYSTEM_LOG_CHECK_TEST =====
    FOR    ${INDEX}    IN RANGE    1    ${MaxLoopNum}
         Print Loop Info  ${INDEX}
         Set Testcase Timeout  300
         Critical Step  1  switch To Openbmc Check Tool
         Step  1  syslog h
         Step  2  check sys before log  True
         Step  3  run system load stress  True
         Step  4  check sys after log  True
         Step  5  clean system logs  True
    END
    Log Info  ===== End of testCase FB_DIAG_COMM_TC_057_SYSTEM_LOG_CHECK_TEST =====


*** Keywords ***
Diag Connect Device
    WPL Set Library Order
    WPL Diag Device Connect
    WPL Init Test Library

Diag Disconnect Device
    WPL Diag Device Disconnect

Set Testcase Timeout
    [Arguments]    ${TIMEOUT}
    [Timeout]      ${TIMEOUT} seconds
    Log Debug      *** Set Testcase Timeout: ${TIMEOUT} Seconds ***
    sleep          1s

Print Loop Info
    [Arguments]    ${CUR_INDEX}
    Log Info  *******************************************
    Log Info  *** Test Loop \#: ${CUR_INDEX} / ${LoopCnt} ***
    Log Info  *******************************************


