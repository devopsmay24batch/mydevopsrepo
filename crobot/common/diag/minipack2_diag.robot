###############################################################################
# LEGALESE:   "Copyright (C) 2019_2020, Celestica Corp. All rights reserved." #
#                                                                             #
# This source code is confidential, proprietary, and contains trade           #
# secrets that are the sole property of Celestica Corp.                       #
# Copy and/or distribution of this source code or disassembly or reverse      #
# engineering of the resultant object code are strictly forbidden without     #
# the written consent of Celestica Corp.                                      #
#                                                                             #
###############################################################################
#######################################################################################################################
# Script       : minipack2_diag.robot                                                                                  #
# Date         : April 22, 2020                                                                                       #
# Author       : TK                                                                                                   #
# Description  : This script will validate all Diag OS EDA tools                                                      #
#                                                                                                                     #
# Script Revision Details:                                                                                            #

#######################################################################################################################

*** Settings ***
Documentation   This Suite will validate all Diag OS

Library           Keyword_Resource.py
Resource          Resource.robot
Library           DiagLibAdapter.py
Variables         Diag_OS_variable.py

Suite Setup       Diag Connect Device
Suite Teardown    Diag Disconnect Device

*** Variables ***
${LoopCnt}        1
${MaxLoopNum}     2

*** Test Cases ***
#### Start _ Facebook Common Diag Test Cases #####
FB_DIAG_COMM_TC_000_DIAG_INSTALL_UNINSTALL
    [Documentation]  Synopsis=> This test executes to ensure the DIAG properly version is installed.
    [Tags]  FB_DIAG_COMM_TC_000_DIAG_INSTALL_UNINSTALL  common  minipack2  critical
    Log Info  ===== Start of testCase FB_DIAG_COMM_TC_000_DIAG_INSTALL_UNINSTALL ====
    FOR    ${INDEX}    IN RANGE    1    ${MaxLoopNum}
        Print Loop Info  ${INDEX}
        Set Testcase Timeout  300
        Step  1  cat diag version
        Step  2  copy diag image files
        Step  3  clean diag rpm
        Step  4  delete the diag on centos
        Critical Step  1  switch to openbmc
        Step  5  delete the diag on openbmc
        Step  6  install diag tools
        Step  7  check diag version
        Step  8  init diag test  
        Critical Step  9  switch to openbmc
        Step  10  check openbmc version
    END
    [Teardown]  clear diag files
    Log Info  ===== End of testCase FB_DIAG_COMM_TC_000_DIAG_INSTALL_UNINSTALL ====

FB_DIAG_COMM_TC_001_I2C_DEVICE_TEST
    [Documentation]  Synopsis=> This test executes to detect all the I2C devices.
    [Tags]  FB_DIAG_COMM_TC_001_I2C_DEVICE_TEST  common  minipack2
    Log Info  ===== Start of testCase FB_DIAG_COMM_TC_001_I2C_DEVICE_TEST =====
    FOR    ${INDEX}    IN RANGE    1    ${MaxLoopNum}
        Print Loop Info  ${INDEX}
        Set Testcase Timeout  300
        Critical Step  1  switch to openbmc check tool
        Step  1  verify bmc i2c help dict option h
        Step  2  verify bmc i2c help dict option s  -b smb
        Step  3  verify bmc i2c help dict option l  SMB
        Step  4  verify bmc i2c help dict option a  -b smb
	Step  5  verify bmc i2c help dict option s  -b pim1
	Step  6  verify bmc i2c help dict option l  pim1
	Step  7  verify bmc i2c help dict option a  -b pim1
	Step  8  verify bmc i2c help dict option s  -b pim2
        Step  9  verify bmc i2c help dict option l  pim2
        Step  10  verify bmc i2c help dict option a  -b pim2
	Step  11  verify bmc i2c help dict option s  -b pim3
        Step  12  verify bmc i2c help dict option l  pim3
        Step  13  verify bmc i2c help dict option a  -b pim3
	Step  14  verify bmc i2c help dict option s  -b pim4
        Step  15  verify bmc i2c help dict option l  pim4
        Step  16  verify bmc i2c help dict option a  -b pim4
	Step  17  verify bmc i2c help dict option s  -b pim5
        Step  18  verify bmc i2c help dict option l  pim5
        Step  19  verify bmc i2c help dict option a  -b pim5
	Step  20  verify bmc i2c help dict option s  -b pim6
        Step  21  verify bmc i2c help dict option l  pim6
        Step  22  verify bmc i2c help dict option a  -b pim6
	Step  23  verify bmc i2c help dict option s  -b pim7
        Step  24  verify bmc i2c help dict option l  pim7
        Step  25  verify bmc i2c help dict option a  -b pim7
        Step  26  verify bmc i2c help dict option s  -b pim8
        Step  27  verify bmc i2c help dict option l  pim8
        Step  28  verify bmc i2c help dict option a  -b pim8
        Step  29  verify bmc i2c help dict option s  -b SCM
        Step  30  verify bmc i2c help dict option l  SCM
        Step  31  verify bmc i2c help dict option a  -b SCM
        Step  32  verify bmc i2c help dict option s  -b pdb_L
        Step  33  verify bmc i2c help dict option l  pdb_L
        Step  34  verify bmc i2c help dict option a  -b pdb_L
        Step  35  verify bmc i2c help dict option s  -b pdb_R
        Step  36  verify bmc i2c help dict option l  pdb_R
        Step  37  verify bmc i2c help dict option a  -b pdb_R
        Step  38  verify bmc i2c help dict option s  -b FCM_T
        Step  39  verify bmc i2c help dict option l  FCM_T
        Step  40  verify bmc i2c help dict option a  -b FCM_T
	Step  41  verify bmc i2c help dict option s  -b FCM_B
	Step  42  verify bmc i2c help dict option l  FCM_B
	Step  43  verify bmc i2c help dict option a  -b FCM_B
        Step  44  verify bmc i2c help dict option s  -b sim
        Step  45  verify bmc i2c help dict option l  sim
        Step  46  verify bmc i2c help dict option a  -b sim
        Step  47  verify bmc i2c help dict option s  -b bmc
        Step  48  verify bmc i2c help dict option l  bmc
        Step  49  verify bmc i2c help dict option a  -b bmc
		Step  50  verify bmc i2c other help dict option h
        Step  51  verify bmc i2c other help dict option  -s
        Step  52  verify bmc i2c other help dict option  -f
        Step  53  verify bmc i2c other help dict option  -m
        Step  54  verify bmc i2c other help dict option  -b
        Step  55  verify bmc i2c other help dict option  -p
        Step  56  verify bmc i2c other help dict option a
    END



FB_DIAG_COMM_TC_002_PCIe_Devices_Scan_Test
    [Documentation]  Synopsis=> This test executes to check the information of PCIe device scan.
    [Tags]  FB_DIAG_COMM_TC_002_PCIe_Devices_Scan_Test  common  minipack2
    Log Info  ===== Start of testCase FB_DIAG_COM_TC_002_PCIe_Devices_Scan_Test =====
    FOR    ${INDEX}    IN RANGE    1    ${MaxLoopNum}
        Print Loop Info  ${INDEX}
        Set Testcase Timeout  300
        Critical Step  1  switch to centos diag tool
        Step  1  verify pcie help dict option h
        Step  2  verify pcie help dict option help
        Step  3  verify pci option a
        Step  4  verify pci option all
		Step  5  check each pice lspci  06:00.0
		Step  6  check each pice lspci  07:00.0
		Step  7  check each pice lspci  08:00.0
		Step  8  check each pice lspci  12:00.0
		Step  9  check each pice lspci  14:00.0
		Step  10  run command lspci on centos
    END
    Log Info  ===== End of testCase FB_DIAG_TC_COM_002_PCIe_Devices_Scan_Test =====


FB_DIAG_COMM_TC_003_USB_DEVICE_SCAN_TEST
    [Documentation]  Synopsis=> This test executes to check the information of USB device scan.
    [Tags]  FB_DIAG_COMM_TC_003_USB_DEVICE_SCAN_TEST  common  minipack2
    Log Info  ===== Start of testCase FB_DIAG_COMM_TC_003_USB_STORAGE_TEST =====
    FOR    ${INDEX}    IN RANGE    1    ${MaxLoopNum}
        Print Loop Info  ${INDEX}
        Set Testcase Timeout  300
        Critical Step  1  switch to openbmc check tool
        Step  1  verify usb device scan help dict option h
        Step  2  verify usb device scan help dict option help
        Step  3  verify usb device scan help dict option l
        Step  4  verify usb device scan help dict option a
    END
    Log Info  ===== End of testCase FB_DIAG_COMM_TC_003_USB_DEVICE_SCAN_TEST =====


FB_DIAG_COMM_TC_005_CPLD_Test
    [Documentation]  Synopsis=> This test executes to check the information of CPLD.
    [Tags]  FB_DIAG_COMM_TC_005_CPLD_Test  common  minipack2
    Log Info  ===== Start of testCase FB_DIAG_COMM_TC_005 CPLD Test =====
    FOR    ${INDEX}    IN RANGE    1    ${MaxLoopNum}
        Print Loop Info  ${INDEX}
        Set Testcase Timeout  300
        Critical Step  1  switch to openbmc check tool
        Step  1  verify cpld test h
        Step  2  verify cpld test v
        Step  3  verify cpld test k
	Step  4  check cpld main info
        Step  5  verify cpld test a
    END
    Log Info  ===== End of testCase FB_DIAG_COMM_TC_005_USB_DEVICE_SCAN_TEST =====


FB_DIAG_COMM_TC_006_INTERNAL_UART_TEST
    [Documentation]  Synopsis=> This test executes to test the SCM and FCM hot_swap function.
    [Tags]  FB_DIAG_COMM_TC_006_INTERNAL_UART_TEST  common  minipack2
    Log Info  ===== Start of testCase FB_DIAG_COMM_TC_006_INTERNAL_UART_TEST ====
    FOR    ${INDEX}    IN RANGE    1    ${MaxLoopNum}
        Print Loop Info  ${INDEX}
        Set Testcase Timeout  300
        Critical Step  1  switch To Openbmc
        Step  1  check the cpu os version
        Step  2  check bmc version  True
        Step  3  switch To Openbmc
        Step  4  check the cpu os version
        Step  5  check bmc version  True
        Step  6  switch To Openbmc
        Step  7  check the cpu os version
        Step  8  check bmc version  True
    END
    Log Info  ===== End of testCase FB_DIAG_COMM_TC_006_INTERNAL_UART_TEST ====


FB_DIAG_COMM_TC_007_Sensor_Test
    [Documentation]  Synopsis=> This test executes to test the senor function.
    [Tags]  FB_DIAG_COMM_TC_007_Sensor_Test  common  minipack2
    Log Info  ===== Start of testCase FB_DIAG_COMM_TC_007_Sensor_Test ====
    FOR    ${INDEX}    IN RANGE    1    ${MaxLoopNum}
        Print Loop Info  ${INDEX}
        Set Testcase Timeout  300
        Critical Step  1  switch To Openbmc
        Step  1  cel sensor test h
        Step  2  cel sensor test d
	Step  3  cel sensor test s
        Step  4  cel sensor test bc  smb
        Step  5  cel sensor test bc  pim1
        Step  6  cel sensor test bc  pim2
        Step  7  cel sensor test bc  pim3
        Step  8  cel sensor test bc  pim4
        Step  9  cel sensor test bc  pim5
        Step  10  cel sensor test bc  pim6
        Step  11  cel sensor test bc  pim7
        Step  12  cel sensor test bc  pim8
        Step  13  cel sensor test bc  scm
        Step  14  cel sensor test bc  pdb
        Step  15  cel sensor test bc  psu1
        Step  16  cel sensor test bc  psu2
        Step  17  cel sensor test bc  psu3
        Step  18  cel sensor test bc  psu4
        Step  19  cel sensor test bc  fcm
        Step  20  cel sensor test bc  sim
        Step  21  cel sensor test bc  all
        Step  22  cel sensor test a
    END
    Log Info  ===== End of testCase FB_DIAG_COMM_TC_007_Sensor_Test ====


FB_DIAG_COMM_TC_008_EEPROM_TEST
    [Documentation]  Synopsis=> This test executes to test SMB EEPROM info.
    [Tags]  FB_DIAG_COMM_TC_008_EEPROM_TEST  common  minipack2
    Log Info  ===== Start of testCase FB_DIAG_COMM_TC_008_EEPROM_TEST =====
    FOR    ${INDEX}    IN RANGE    1    ${MaxLoopNum}
        Print Loop Info  ${INDEX}
        Set Testcase Timeout  300
        Critical Step  1  switch To Openbmc Check Tool
        Step  1  cel platform test h
        Step  2  cel platform test i
        Step  3  cel platform test e smb
        Step  4  cel platform test e scm
        Step  5  cel platform test e fcm  fcm-t
        Step  6  cel platform test e fcm  fcm-b
        Step  7  cel platform test e  sim
        Step  8  cel platform test e  bmc
        Step  9  cel platform test e  fan1
        Step  10  cel platform test e  fan2
        Step  11  cel platform test e  fan3
        Step  12  cel platform test e  fan4
        Step  13  cel platform test e  fan5
        Step  14  cel platform test e  fan6
        Step  15  cel platform test e  fan7
        Step  16  cel platform test e  fan8
        Step  17  cel platform test e  pim1
        Step  18  cel platform test e  pim2
        Step  19  cel platform test e  pim3
        Step  20  cel platform test e  pim4
        Step  21  cel platform test e  pim5
        Step  22  cel platform test e  pim6
        Step  23  cel platform test e  pim7
        Step  24  cel platform test e  pim8
	Step  25  cel platform test p
        Step  26  cel platform test a
    END
    Log Info  ===== End of testCase FB_DIAG_COMM_TC_008_EEPROM_TEST =====

FB_DIAG_COMM_TC_009_NVME_SSD_TEST
    [Documentation]  Synopsis=> This test executes to check the information of NVMe Disk.
    [Tags]  FB_DIAG_COMM_TC_009_NVME_SSD_TEST  common  minipack2
    Log Info  ===== Start of testCase FB_DIAG_COMM_TC_009_NVME_SSD_TEST =====
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
    Log Info  ===== End of testCase FB_DIAG_COMM_TC_009_NVME_SSD_TEST =====


FB_DIAG_COMM_TC_010_EXTERNAL_USB_TEST
    [Documentation]  Synopsis=> This test executes to check the information of USB storage.
    [Tags]  FB_DIAG_COMM_TC_010_EXTERNAL_USB_TEST  common  minipack2
    Log Info  ===== Start of testCase FB_DIAG_COMM_TC_010_EXTERNAL_USB_TEST =====
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
    Log Info  ===== End of testCase FB_DIAG_COMM_TC_010_EXTERNAL_USB_TEST =====


FB_DIAG_COMM_TC_011_HOT_SWAP_CONTROL_TEST(SCM/FCM)
    [Documentation]  Synopsis=> This test executes to check the hot swap control.
    [Tags]  FB_DIAG_COMM_TC_011_HOT_SWAP_CONTROL_TEST  common  minipack2
    Log Info  ===== Start of testCase FB_DIAG_COMM_TC_011_HOT_SWAP_CONTROL_TEST(SCM/FCM) =====
    FOR    ${INDEX}    IN RANGE    1    ${MaxLoopNum}
        Print Loop Info  ${INDEX}
        Set Testcase Timeout  1000
        Critical Step  1  switch to openbmc check tool
        Step  1  verify bmc command  ce_hotswap_test_h  ce_hotswap_h_pattern
        Step  2  verify bmc command  ce_hotswap_test_h  fail_message  True
        Step  3  verify bmc command  ce_hotswap_test_a  ce_hotswap_a_pattern
        Step  4  verify bmc command  ce_hotswap_test_a  fail_message  True
    END
    Log Info  ===== End of testCase FB_DIAG_COMM_TC_011_HOT_SWAP_CONTROL_TEST(SCM/FCM) =====


FB_DIAG_COMM_TC_012_IPMI_COMMAND_FROM_COMe_TO_BMC_TEST(SCM_Board)
    [Documentation]  Synopsis=> This test executes to check the COME access BMC.
    [Tags]  FB_DIAG_COMM_TC_012_IPMI_Command_FROM_COMe_TO_BMC_TEST  common  minipack2
    Log Info  ===== Start of testCase FB_DIAG_COMM_TC_012_IPMI_COMMAND_FROM_COMe_TO_BMC_TEST =====
    FOR    ${INDEX}    IN RANGE    1    ${MaxLoopNum}
        Print Loop Info  ${INDEX}
        Set Testcase Timeout  300
        Critical Step  1  switch to centos diag tool
        Step  1  verify ipmitool mc info
    END
    Log Info  ===== End of testCase FB_DIAG_COMM_TC_012_IPMI_COMMAND_FROM_COMe_TO_BMC_TEST =====


FB_DIAG_COMM_TC_014_PSU_EEPROM_test
    [Documentation]  Synopsis=> This test executes to test the PSU EEPROM function.
    [Tags]  FB_DIAG_COMM_TC_014_PSU_EEPROM_test  common  minipack2
    Log Info  ===== Start of testCase FB_DIAG_COMM_TC_014_PSU_EEPROM_test ====
    FOR    ${INDEX}    IN RANGE    1    ${MaxLoopNum}
        Print Loop Info  ${INDEX}
        Set Testcase Timeout  300
        Critical Step  1  switch To Openbmc
        Step  1  verify PSU EEPROM dict option h
        Step  2  verify PSU EEPROM dict option i
        Step  3  verify PSU EEPROM dict option s
        Step  4  verify PSU EEPROM dict option a
        Step  5  verify get psu info  psu1
        Step  6  verify get eeprom info  psu1
        Step  7  verify get psu info  psu2
        Step  8  verify get eeprom info  psu2
        Step  9  verify get psu info  psu3
        Step  10  verify get eeprom info  psu3
        Step  11  verify get psu info  psu4
        Step  12  verify get eeprom info  psu4
    END
    Log Info  ===== End of testCase FB_DIAG_COMM_TC_014_PSU_EEPROM_test ====


FB_DIAG_COMM_TC_016_CONTROL_FAN_TEST
    [Documentation]  Synopsis=> This test executes to test the fan.
    [Tags]  FB_DIAG_COMM_TC_016_CONTROL_FAN_TEST  common  minipack2
    Log Info  ===== Start of testCase FB_DIAG_COMM_TC_016_CONTROL_FAN_TEST =====
    FOR    ${INDEX}    IN RANGE    1    ${MaxLoopNum}
        Print Loop Info  ${INDEX}
        Set Testcase Timeout  600
        Critical Step  1  switch To Openbmc Check Tool
        Step  1  verify cel fan test h
		Step  2  collect all fan manufacturer is present
		Step  3  verify cel fan test c
        Step  4  verify cel fan test g
        Step  5  verify cel fan test s
        Step  6  verify cel fan test p 10
        Step  7  verify cel fan test g p 10
        Step  8  verify cel fan test p 100
        Step  9  verify cel fan test g p 100
        Step  10  verify cel fan test p 50
        Step  11  verify cel fan test g p 50
        Step  12  verify cel fan test p 70
        Step  13  verify cel fan test g p 70
        Step  14  verify cel fan test a
        Step  15  verify cel fan test e
    END
    Log Info  ===== End of testCase FB_DIAG_COMM_TC_016_CONTROL_FAN_TEST =====


FB_DIAG_COMM_TC_019_TPM_DEVICE_TEST
    [Documentation]  Synopsis=> This test executes to test the TPM function.
    [Tags]  FB_DIAG_COMM_TC_019_TPM_DEVICE_TEST  common  minipack2  critical
    Log Info  ===== Start of testCase FB_DIAG_COMM_TC_019_TPM_DEVICE_TEST =====
    FOR    ${INDEX}    IN RANGE    1    ${MaxLoopNum}
        Print Loop Info  ${INDEX}
        Set Testcase Timeout  300
        Critical Step  1  switch To Openbmc Check Tool
        Step  1  cel tpm test h
        Step  2  cel tpm device test i
	Step  3  cel tpm test c
        Step  4  cel tpm test a
    END
    Log Info  ===== End of testCase FB_DIAG_COMM_TC_019_TPM_DEVICE_TEST =====


FB_DIAG_COMM_TC_020_MDIO_TEST
    [Documentation]  Synopsis=> This test executes to test the MDIO test.
    [Tags]  FB_DIAG_COMM_TC_020_MDIO_TEST  common  minipack2
    Log Info  ===== Start of testCase FB_DIAG_COMM_TC_020_MDIO_TEST =====
    FOR    ${INDEX}    IN RANGE    1    ${MaxLoopNum}
        Print Loop Info  ${INDEX}
        Set Testcase Timeout  300
        Critical Step  1  switch To Openbmc Check Tool
        Step  1  cel mdio test h
        Step  2  cel mdio test a
    END
    Log Info  ===== End of testCase FB_DIAG_COMM_TC_020_MDIO_TEST =====

FB_DIAG_COMM_TC_021_BMC_CPU_TEST
    [Documentation]  Synopsis=> This test executes to check if the main information of BMC CPU is correct.
    [Tags]  FB_DIAG_COMM_TC_021_BMC_CPU_TEST  common  minipack2
    Log Info  ===== Start of testCase FB_DIAG_COMM_TC_021_BMC_CPU_TEST =====
    FOR    ${INDEX}    IN RANGE    1    ${MaxLoopNum}
        Print Loop Info  ${INDEX}
        Set Testcase Timeout  300
        Critical Step  1  switch to openbmc check tool
        Step  1  verify bmc cpu help dict option h
        Step  2  verify bmc cpu help dict option i
        Step  4  verify bmc cpu help dict option a
        Step  3  compare bmc cpu info and option i
    END
    Log Info  ===== End of testCase FB_DIAG_COMM_TC_021_BMC_CPU_TEST =====

FB_DIAG_COMM_TC_023_BMC_Memory_TEST
    [Documentation]  Synopsis=> This test executes to test the bmc memory.
    [Tags]  FB_DIAG_COMM_TC_023_BMC_Memory_TEST  common  minipack2
    Log Info  ===== Start of testCase FB_DIAG_COMM_TC_023_BMC_MEMORY_TEST =====
    FOR    ${INDEX}    IN RANGE    1    ${MaxLoopNum}
        Print Loop Info  ${INDEX}
        Set Testcase Timeout  780
        Critical Step  1  switch To Openbmc Check Tool
        Step  1  cel memory test h
        Step  2  cel memory test i
        Step  3  cel memory test m
        Step  4  compare cel memory info
        Step  5  cel memory test a
    END
    Log Info  ===== End of testCase FB_DIAG_COMM_TC_023_BMC_MEMORY_TEST =====

FB_DIAG_COMM_TC_024_EMMC_TEST
    [Documentation]  Synopsis=> This test executes to test the emmc.
    [Tags]  FB_DIAG_COMM_TC_024_EMMC_TEST  common  minipack2
    Log Info  ===== Start of testCase FB_DIAG_COMM_TC_043_EMMC_TEST =====
    FOR    ${INDEX}    IN RANGE    1    ${MaxLoopNum}
        Print Loop Info  ${INDEX}
        Set Testcase Timeout  300
        Critical Step  1  switch To Openbmc Check Tool
        Step  1  check emmc info
        Step  2  cel emmc test h
        Step  3  cel emmc test i
        Step  4  cel emmc test s
        Step  5  cel emmc test a
        Step  6  check disk dump file
    END
    Log Info  ===== End of testCase FB_DIAG_COMM_TC_024_MEMORY_TEST =====


FB_DIAG_COMM_TC_025_BMC_CONTROL_COME_BIOS_BOOT_TEST
    [Documentation]  Synopsis=> This test executes to test the bmc control come bios boot.
    [Tags]  FB_DIAG_COMM_TC_025_BMC_CONTROL_COME_BIOS_BOOT_TEST  common  minipack2
    Log Info  ===== Start of testCase FB_DIAG_COMM_TC_025_BMC_CONTROL_COME_BIOS_BOOT_TEST =====
    FOR    ${INDEX}    IN RANGE    1    ${MaxLoopNum}
        Print Loop Info  ${INDEX}
        Set Testcase Timeout  300
        Critical Step  1  switch to centos diag tool
        Step  1  reboot to centos
        Step  2  switch To Openbmc Check Tool
        Step  3  make power  off
        Step  4  check power status  off
        Step  5  make power  on
        Step  6  check power status  on
        Step  7  switch to centos diag tool
        Step  8  check the cpu os version
        Step  9  switch To Openbmc Check Tool
        Step  10  reboot to centos
        Step  11  switch To Openbmc Check Tool
        Step  12  make power  off
        Step  13  check power status  off
        Step  14  make power  on
        Step  15  check power status  on
        Step  16  switch to centos diag tool
        Step  17  check the cpu os version
    END
    Log Info  ===== End of testCase FB_DIAG_COMM_TC_025_BMC_CONTROL_COME_BIOS_BOOT_TEST =====


FB_DIAG_COMM_TC_028_FIRMWARE_SOFTWARE_TEST
    [Documentation]  Synopsis=> This test executes to verify the firmware and software version.
    [Tags]  FB_DIAG_COMM_TC_028_FIRMWARE_SOFTWARE_TEST  common  minipack2
    Log Info  ===== Start of testCase FB_DIAG_COMM_TC_028_FIRMWARE_SOFTWARE_TEST =====
    FOR    ${INDEX}    IN RANGE    1    ${MaxLoopNum}
        Print Loop Info  ${INDEX}
        Set Testcase Timeout  300
        Critical Step  1  switch To Openbmc Check Tool
        Step  2  cel software test h
        Step  3  cel software v
        Step  4  cel software test a
        Step  5  cat etc issue bmc
        Step  6  fw util all version
        Step  7  switch to centos diag tool
        Step  8  minipack2 fpga ver sh
        Step  9  verify dmidecode t bios
        Step  10  check the cpu os version
        Step  11  fw util all version
    END
    Log Info  ===== End of testCase FB_DIAG_COMM_TC_028_FIRMWARE_SOFTWARE_TEST =====

FB_DIAG_COMM_TC_029_DIMM_SPD_TEST
    [Documentation]  Synopsis=> This test executes to verify the dimm spd.
    [Tags]  FB_DIAG_COMM_TC_029_DIMM_SPD_TEST  common  minipack2
    Log Info  ===== Start of testCase FB_DIAG_COMM_TC_029_DIMM_SPD_TEST =====
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
        Step  7  cel memory info compare
        Step  8  verify meminfo dmidecode
    END
    Log Info  ===== End of testCase FB_DIAG_COMM_TC_029_DIMM_SPD_TEST =====


FB_DIAG_COMM_TC_031_TPM_DEVICE_TEST
    [Documentation]  Synopsis=> This test executes to check TPM verison.
    [Tags]  FB_DIAG_COMM_TC_031_TPM_DEVICE_TEST  common  minipack2
    Log Info  ===== Start of testCase FB_DIAG_COMM_TC_010_TPM_TEST =====
    FOR    ${INDEX}    IN RANGE    1    ${MaxLoopNum}
        Print Loop Info  ${INDEX}
        Set Testcase Timeout  300
        Critical Step  1  switch to centos diag tool
        Step  1  verify tpm help dict option h
        Step  2  verify tpm help dict option help
        Step  3  verify tpm help dict option l
        Step  4  verify tpm help dict option list
        Step  5  verify tpm help dict option a
        Step  6  verify tpm help dict option all
    END
    Log Info  ===== End of testCase FB_DIAG_COMM_TC_031_DEVICE_TPM_TEST =====

FB_DIAG_COMM_TC_032_CPU_INFORMATION_TEST
    [Documentation]  Synopsis=> This test executes to check the CPU information with diag script in Linux OS.
    [Tags]  FB_DIAG_COMM_TC_032_CPU_INFORMATION_TEST  common  minipack2
    Log Info  ===== Start of testCase FB_DIAG_COMM_TC_032_CPU_INFORMATION_TEST =====
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
        Step  9  verify lscpu info  False
        Step  10  reboot to centos and disable hyper threading
        Step  11  verify cpu help dict option a  True
        Step  12  verify cpu help dict option all  True
    END
    [Teardown]  Run Keyword If Test Failed  reboot to centos and disable hyper threading
    Log Info  ===== End of testCase FB_DIAG_COMM_TC_032_CPU_INFORMATION_TEST =====

FB_DAIG_COMM_TC_033_MEMORY_TEST
    [Documentation]  Synopsis=> This test executes to test the memory function.
    [Tags]  FB_DAIG_COMM_TC_033_MEMORY_TEST  common  minipack2
    Log Info  ===== Start of testCase FB_DAIG_COMM_TC_033_MEMORY_TEST =====
    FOR    ${INDEX}    IN RANGE    1    ${MaxLoopNum}
        Print Loop Info  ${INDEX}
        Set Testcase Timeout  18000
        Critical Step  1  switch to centos diag tool
        Step  1  verify mem help dict option h
        Step  2  verify mem help dict option help
        Step  3  verify mem help dict option K
        Step  4  verify mem help dict option check
        Step  5  verify mem help dict option test a
        Step  6  verify mem help dict option test all
        Step  7  verify meminfo dmidecode
        Step  8  verify mem help dict option K
        Step  9  verify mem help dict option check
        Step  10  verify mem help dict option test a
        Step  11  verify mem help dict option test all
        Step  12  verify mem help dict option K
        Step  13  verify mem help dict option check
        Step  14  verify mem help dict option test a
        Step  15  verify mem help dict option test all
    END
    Log Info  ===== End of testCase FB_DAIG_COMM_TC_033_MEMORY_TEST =====


FB_DIAG_COMM_TC_034_MANAGEMENT_ETHER_PORT_MAC_CHECK_TEST
    [Documentation]  Synopsis=> This test executes to check that MAC should belong to Quanta.
    [Tags]  FB_DIAG_COMM_TC_034_MANAGEMENT_ETHER_PORT_MAC_CHECK_TEST  common  minipack2
    Log Info  ===== Start of testCase FB_DIAG_COMM_TC_034_MANAGEMENT_ETHER_PORT_MAC_CHECK_TEST ====
    FOR    ${INDEX}    IN RANGE    1    ${MaxLoopNum}
         Print Loop Info  ${INDEX}
         Set Testcase Timeout  180
         Critical Step  1  switch to centos diag tool
         Step  1  verify mac help dict option h
         Step  2  verify mac help dict option help
         Step  3  verify mac help dict option a
         Step  4  verify mac help dict option all
         Step  5  get the MAC and compare with command
    END
    Log Info  ===== End of testCase FB_DIAG_COMM_TC_034_MANAGEMENT_ETHER_PORT_MAC_CHECK_TEST ====


FB_DIAG_COMM_TC_035_MANAGEMENT_ETHER_PORT_CONNECT_TEST_COME_MODULE
    [Documentation]  Synopsis=> This test executes to check the COMe management port.
    [Tags]  FB_DIAG_COMM_TC_035_MANAGEMENT_ETHER_PORT_CONNECT_TEST_COME_MODULE  common  minipack2
    Log Info  ===== Start of testCase FB_DIAG_COMM_TC_035_MANAGEMENT_ETHER_PORT_CONNECT_TEST_COME_MODULE =====
    [Setup]  ssh login bmc
    FOR    ${INDEX}    IN RANGE    1    ${MaxLoopNum}
        Print Loop Info  ${INDEX}
        Set Testcase Timeout  600
        Critical Step  1  switch to centos diag tool
        Step  1  check and ping server ip from centos
        Step  2  check and ping server ipv6 from centos
    END
    [Teardown]  ssh disconnect
    Log Info  ===== End of testCase FB_DIAG_COMM_TC_035_MANAGEMENT_ETHER_PORT_CONNECT_TEST_COME_MODULE =====


FB_DIAG_COMM_TC_036_RTC_Test
    [Documentation]  Synopsis=> This test executes to check the RTC date&time.
    [Tags]  FB_DIAG_COMM_TC_036_RTC_Test  common  minipack2
    Log Info  ===== Start of testCase FB_DIAG_COMM_TC_036_RTC_TEST =====
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
	Step  10  verify RTC help dict option r
        Step  11  power cycle device to openbmc
        Step  12  switch to centos diag tool
        Step  13  verify RTC help dict option r
        Step  14  verify RTC help dict option read
    END
    Log Info  ===== End of testCase FB_DIAG_COMM_TC_036_RTC_Test =====


FB_DIAG_COMM_TC_037_FW_SW_INFO_TEST
    [Documentation]  Synopsis=> This test executes to check all SW/FW verison.
    [Tags]  FB_DIAG_COMM_TC_037_FW_SW_INFO_TEST  common  minipack2
    Log Info  ===== Start of testCase FB_DIAG_COMM_TC_037_FW_SW_INFO_TEST =====
    FOR    ${INDEX}    IN RANGE    1    ${MaxLoopNum}
        Print Loop Info  ${INDEX}
        Set Testcase Timeout  300
        Critical Step  1  switch to centos diag tool
        Step  1  verify sw version help dict option h
        Step  2  verify sw version help dict option help
        Step  3  minipack2 verify sw dict option S
        Step  4  minipack2 verify sw dict option show
        Step  5  cat etc product version
        Step  6  cat proc version
        Step  7  cat etc redhat release
        Step  8  minipack2 run eeupdate64e nic2 adapterinfo
        Step  9  switch to openbmc
        Step  10  fw util all version
	Step  11  fw util pim fpga version
    END
    Log Info  ===== End of testCase FB_DIAG_COMM_TC_037_FW_SW_INFO_TEST =====


FB_DIAG_COMM_TC_038_INTERNAL_USB_TEST_COME
    [Documentation]  Synopsis=> This test executes to check the interlink over USB
    [Tags]  FB_DIAG_COMM_TC_038_INTERNAL_USB_TEST_COME  common  minipack2
    Log Info  ===== Start of testCase FB_DIAG_COMM_TC_038_INTERNAL_USB_TEST_COME =====
    [Setup]  ssh login bmc
    FOR    ${INDEX}    IN RANGE    1    ${MaxLoopNum}
        Print Loop Info  ${INDEX}
        Set Testcase Timeout  600
        step  1  switch to openbmc
        step  2  check default of USB interface  mode=openbmc  interface=${internal_interface}  ip=${openbmc_default_ipv6}
        step  3  ping to check  mode=openbmc  interface=${internal_interface}  ip=${centos_default_ipv6}
        step  4  switch to centos diag tool
        step  5  check default of USB interface  mode=centos  interface=${internal_interface}  ip=${centos_default_ipv6}
        step  6  ping to check  mode=centos  interface=${internal_interface}  ip=${openbmc_default_ipv6}
    END
    [Teardown]  ssh disconnect
    Log Info  ===== End of testCase FB_DIAG_COMM_TC_038_INTERNAL_USB_TEST_COME =====


#FB_DIAG_COMM_TC_039_REVISION_AND_DEVICE/BOARD ID/SCRATCH_PAD_TEST
#    [Documentation]  Synopsis=> This test executes to check FPGA value read/write correctly
#    [Tags]  FB_DIAG_COMM_TC_039_REVISION_AND_DEVICE/BOARD ID/SCRATCH_PAD_TEST  common  minipack2
#    Log Info  ===== Start of testCase FB_DIAG_COMM_TC_039_REVISION_AND_DEVICE/BOARD ID/SCRATCH_PAD_TEST =====
#    FOR    ${INDEX}    IN RANGE    1    ${MaxLoopNum}
#        Print Loop Info  ${INDEX}
#        Set Testcase Timeout  600
#        Critical Step  1  switch to centos diag tool
#        Step  1  verify fpga help dict option h
#        Step  2  verify fpga help dict option help
#        Step  3  verify fpga help dict option a
#        Step  4  check fpga driver version
#    END
#    Log Info  ===== End of testCase FB_DIAG_COMM_TC_039_REVISION_AND_DEVICE/BOARD ID/SCRATCH_PAD_TEST =====


#FB_DIAG_COMM_TC_040_UPTIME_TEST
#    [Documentation]  Synopsis=> This test executes to check FPGA IOB test correctly
#    [Tags]  FB_DIAG_COMM_TC_040_UPTIME_TEST  common  minipack2
#    Log Info  ===== Start of testCase FB_DIAG_COMM_TC_040_UPTIME_TEST =====
#    FOR    ${INDEX}    IN RANGE    1    ${MaxLoopNum}
#        Print Loop Info  ${INDEX}
#        Set Testcase Timeout  600
#        Critical Step  1  switch to centos diag tool
#        Step  1  verify fpga help dict option h
#        Step  2  verify fpga help dict option help
#        Step  3  verify fpga help dict option a with config
#    END
#    Log Info  ===== End of testCase FB_DIAG_COMM_TC_040_UPTIME_TEST =====
#

FB_DIAG_COMM_TC_041_MSI_TEST
     [Documentation]  Synopsis=> This test executes to check the function of FPGA.
     [Tags]  FB_DIAG_COMM_TC_041_MSI_TEST  common  minipack2
     Log Info  ===== Start of testCase FB_DIAG_COMM_TC_041_MSI_TEST =====
     Set Test Variable     ${timeout}    300
     FOR    ${INDEX}    IN RANGE    1    ${MaxLoopNum}
          Print Loop Info  ${INDEX}
          Set Testcase Timeout  300
          Critical Step  1  switch to centos diag system log
          Step  1  fpga test
	  Step  2  rmmod uio pci
     END
     Log Info  ===== End of testCase FB_DIAG_COMM_TC_041_MSI_TEST =====


FB_DIAG_COMM_TC_042_IOB_FPGA_RESET_HOT_PLUG_TEST
     [Documentation]  Synopsis=> This test executes to check the function of FPGA.
     [Tags]  FB_DIAG_COMM_TC_042_IOB_FPGA_RESET_HOT_PLUG_TEST  common  minipack2
     Log Info  ===== Start of testCase FB_DIAG_COMM_TC_042_IOB_FPGA_RESET_HOT_PLUG_TEST =====
     Set Test Variable     ${timeout}    300
     FOR    ${INDEX}    IN RANGE    1    ${MaxLoopNum}
         Print Loop Info  ${INDEX}
         Set Testcase Timeout  300
         Critical Step  1  switch to centos diag system log
         Step  1  set iob fpga card to present  regex=
         Step  2  list of pci devices and verify  device_list=${mp2_lspci_device_lists}
         Step  3  set iob fpga card to not present
         Step  4  run i2cdump and check for the data change  where=${mp2_tc042_i2cdump_changes}
         Step  5  set iob fpga card to present
         Step  6  run fb sh
         Step  7  run fpga ver
    END
     Log Info  ===== End of testCase FB_DIAG_COMM_TC_042_IOB_FPGA_RESET_HOT_PLUG_TEST =====

FB_DIAG_COMM_TC_046_sLPC_test
     [Documentation]  Synopsis=> This test executes to check the function of sLPC.
     [Tags]  FB_DIAG_COMM_TC_046_sLPC_test  common  minipack2
     Log Info  ===== Start of testCase FB_DIAG_COMM_TC_046_sLPC_test =====
     Set Test Variable     ${timeout}    1500
     FOR    ${INDEX}    IN RANGE    1    ${MaxLoopNum}
         Print Loop Info  ${INDEX}
         Set Testcase Timeout  300
         Critical Step  1  switch to centos diag tool
         Step  1  minipack2 verify fpga option h
         Step  2  fpga check sLPC  1
         Step  3  fpga check sLPC  2
         Step  4  fpga check sLPC  3
         Step  5  fpga check sLPC  4
         Step  6  fpga check sLPC  5
         Step  7  fpga check sLPC  6
         Step  8  fpga check sLPC  7
         Step  9  fpga check sLPC  8
    END
     Log Info  ===== End of testCase FB_DIAG_COMM_TC_046_sLPC_test =====

FB_DIAG_COM_TC_052_FRU_EEPROM_UPDATE
    [Documentation]  Synopsis=> This test executes to update eeprom.
     [Tags]  FB_DIAG_COM_TC_052_FRU_EEPROM_UPDATE  common  minipack2
     Log Info  ===== Start of testCase FB_DIAG_COM_TC_084_PCIE_SWITCH_FIRMWARE_UPDATE =====
     Set Test Variable     ${timeout}    1000
     FOR    ${INDEX}    IN RANGE    1    ${MaxLoopNum}
          Print Loop Info  ${INDEX}
          Set Testcase Timeout  600
          Critical Step  1  switch to openbmc
          Step  1  verify scm eeprom update
          Step  2  verify smb eeprom update
          Step  3  verify sim eeprom update
          Step  4  verify bmc eeprom update
          Step  5  verify fcm t eeprom update
          Step  6  verify fcm b eeprom update
          Step  7  reset the whole system
	  Step  8  wait for openbmc prompt back
	  Step  9  wait for centos prompt back
	  Critical Step  2  switch to openbmc
          Step  10  verify scm eeprom update
          Step  11  verify smb eeprom update
          Step  12  verify sim eeprom update
          Step  13  verify bmc eeprom update
          Step  14  verify fcm t eeprom update
          Step  15  verify fcm b eeprom update
          Step  16  verify pim eeprom update
          Step  17  auto pim eeprom update
          Step  18  reset the whole system
	  Step  19  wait for openbmc prompt back
          Step  20  wait for centos prompt back
          Critical Step  3  switch to openbmc
          Step  21  verify pim eeprom update
          Step  22  verify fan eeprom update
          Step  23  auto fan eeprom update
          Step  24  reset the whole system
	  Step  25  wait for openbmc prompt back
          Step  26  wait for centos prompt back
          Critical Step  4  switch to openbmc
          Step  27  verify fan eeprom update
     END
     Log Info  ===== End of testCase FB_DIAG_COM_TC_052_FRU_EEPROM_UPDATE =====

FB_DIAG_COM_TS_054_MDIO_ERROR_STATUS_TEST
    [Documentation]  Synopsis=> This test executes to check the information of MDIO.
    [Tags]  FB_DIAG_COM_TS_054_MDIO_ERROR_STATUS_TEST  minipack2
    Log Info  ===== Start of testCase FB_DIAG_COM_TS_054_MDIO_ERROR_STATUS_TEST =====
    FOR    ${INDEX}    IN RANGE    1    ${MaxLoopNum}
        Print Loop Info  ${INDEX}
        Set Testcase Timeout  300
        Critical Step  1  switch to centos
        Step  1  verify mdio tool fpga option h
        Step  2  verify mdio tool fpga option 0x9c
        Step  3  verify mdio tool fpga option 0x5201d000
	Step  4  verify mdio tool fpga option 0x5201d001
        Step  5  verify mdio tool fpga option 0x210
    END
    Log Info  ===== End of testCase FB_DIAG_COM_TS_054_MDIO_ERROR_STATUS_TEST =====

FB_DIAG_COM_TS_055_MDIO_ERROR_INTERRUPT_TEST
    [Documentation]  Synopsis=> This test executes to check the information of MDIO.
    [Tags]  FB_DIAG_COM_TS_055_MDIO_ERROR_INTERRUPT_TEST  common  minipack2
    Log Info  ===== Start of testCase FB_DIAG_COM_TS_055_MDIO_ERROR_INTERRUPT_TEST =====
    FOR    ${INDEX}    IN RANGE    1    ${MaxLoopNum}
        Print Loop Info  ${INDEX}
        Set Testcase Timeout  300
        Critical Step  1  switch to centos
        Step  1  verify mdio tool fpga option h
        Step  2  verify mdio tool fpga option 0x214
        Step  3  verify mdio tool fpga option 0x5200cb20
        Step  4  verify mdio tool fpga option 0x2c
    END
    Log Info  ===== End of testCase FB_DIAG_COM_TS_055_MDIO_ERROR_INTERRUPT_TEST =====

FB_DIAG_COMM_TC_056_MDIO_SCK_Freq_test
    [Documentation]  Synopsis=> This test executes to check MDID SCK Freq
    [Tags]  FB_DIAG_COMM_TC_056_MDIO_SCK_Freq_test  common  minipack2
    Log Info  ===== Start of testCase FB_DIAG_COMM_TC_056_MDIO_SCK_Freq_test =====
    FOR    ${INDEX}    IN RANGE    1    ${MaxLoopNum}
        Print Loop Info  ${INDEX}
        Set Testcase Timeout  600
        Critical Step  1  switch to centos diag tool
        Step  1  minipack2 verify fpga option h
        Step  2  mdc freq mhz test option w
        Step  3  mdc freq mhz test option r
        Step  4  mdc freq mhz test option wA
        Step  5  mdc freq mhz test option r
    END
    Log Info  ===== End of testCase FB_DIAG_COMM_TC_056_MDIO_SCK_Freq_test =====

FB_DIAG_COMM_TC_057_IOB_FPGA_ACCESS_SMB_CPLD_TEST
    [Documentation]  Synopsis=> This test executes to check the information of SMB CPLD
    [Tags]  FB_DIAG_COMM_TC_057_IOB_FPGA_ACCESS_SMB_CPLD_TEST  common  minipack2
    Log Info  ===== Start of testCase FB_DIAG_COMM_TC_057_IOB_FPGA_ACCESS_SMB_CPLD_TEST =====
    FOR    ${INDEX}    IN RANGE    1    ${MaxLoopNum}
        Print Loop Info  ${INDEX}
        Set Testcase Timeout  600
        Critical Step  1  switch to centos diag tool
        Step  1  minipack2 verify fpga option h
        Step  2  test iob fpga access smb cpld 0
        Step  3  test iob fpga access smb cpld 1
        Step  4  test iob fpga access smb cpld 2
        Step  5  test iob fpga access smb cpld 3
    END
    Log Info  ===== End of testCase FB_DIAG_COMM_TC_057_IOB_FPGA_ACCESS_SMB_CPLD_TEST =====

FB_DIAG_COMM_TC_058_IOB_FPGA_ACCESS_SCM_CPLD_TEST
    [Documentation]  Synopsis=> This test executes to check IOB FPGA access to/from SCM CPLD
    [Tags]  FB_DIAG_COMM_TC_058_IOB_FPGA_ACCESS_SCM_CPLD_TEST  common  minipack2
    Log Info  ===== Start of testCase FB_DIAG_COMM_TC_058_IOB_FPGA_ACCESS_SCM_CPLD_TEST =====
    FOR    ${INDEX}    IN RANGE    1    ${MaxLoopNum}
        Print Loop Info  ${INDEX}
        Set Testcase Timeout  600
        Critical Step  1  switch to centos diag tool
        Step  1  minipack2 verify fpga option h
        Step  2  verify scm cpld accessed  0
        Step  3  verify scm cpld accessed  1
        Step  4  verify scm cpld accessed  2
        Step  5  verify scm cpld accessed  3
    END
    Log Info  ===== End of testCase FB_DIAG_COMM_TC_058_IOB_FPGA_ACCESS_SCM_CPLD_TEST =====

FB_DIAG_COM_TC_061_PARSE_EEPROM_TEST
    [Documentation]  Synopsis=> This test executes to check the information of QSFP.
    [Tags]  FB_DIAG_COM_TC_061_PARSE_EEPROM_TEST  common  minipack2
    Log Info  ===== Start of testCase FB_DIAG_COM_TC_061_PARSE_EEPROM_TEST =====
    FOR    ${INDEX}    IN RANGE    1    ${MaxLoopNum}
        Print Loop Info  ${INDEX}
        Set Testcase Timeout  600
        Critical Step  1  switch to centos
        Step  1  verify eeprom qsfp option h
        Step  2  verify eeprom qsfp option help
        Step  3  verify eeprom qsfp test
    END
    Log Info  ===== End of testCase FB_DIAG_COM_TC_061_PARSE_EEPROM_TEST =====

FB_DIAG_COMM_TC_088_COM-e_CPU_Power_stress_test
    [Documentation]  Synopsis=> This test executes to check CPU Power Stress
    [Tags]  FB_DIAG_COMM_TC_088_COM-e_CPU_Power_stress_test  common  minipack2
    Log Info  ===== Start of testCase FB_DIAG_COMM_TC_088_COM-e_CPU_Power_stress_test =====
    FOR    ${INDEX}    IN RANGE    1    ${MaxLoopNum}
        Print Loop Info  ${INDEX}
        Set Testcase Timeout  600
        Critical Step  1  switch To Openbmc Check Tool
        Step  1  run mcelog under daemon mode
        Step  2  test cpu power stress
    END
    Log Info  ===== End of testCase FB_DIAG_COMM_TC_088_COM-e_CPU_Power_stress_test =====

FB_DIAG_COMM_TC_087_CPU_STRESS_TEST
    [Documentation]  Synopsis=> This test executes to check CPU Stress
    [Tags]  FB_DIAG_COMM_TC_087_CPU_STRESS_TEST  common  minipack2
    Log Info  ===== Start of testCase FB_DIAG_COMM_TC_087_CPU_STRESS_TEST =====
    FOR    ${INDEX}    IN RANGE    1    ${MaxLoopNum}
        Print Loop Info  ${INDEX}
        Set Testcase Timeout  1500
        Critical Step  1  switch to centos diag tool
        Step  1  run mcelog under daemon mode
        Step  2  test cpu stress
        Step  3  check MCE log
    END
    Log Info  ===== End of testCase FB_DIAG_COMM_TC_087_CPU_STRESS_TEST =====

FB_DIAG_COMM_TC_089_DDR_STRESS_TEST
    [Documentation]  Synopsis=> This test executes to check DDR Stress
    [Tags]  FB_DIAG_COMM_TC_089_DDR_STRESS_TEST  common  minipack2
    Log Info  ===== Start of testCase FB_DIAG_COMM_TC_089_DDR_STRESS_TEST =====
    FOR    ${INDEX}    IN RANGE    1    ${MaxLoopNum}
         Print Loop Info  ${INDEX}
         Set Testcase Timeout  1200
         Critical Step  1  switch to centos diag tool
         Step  1  run mcelog under daemon mode
         Step  2  minipack2 test ddr stress
         Step  3  check MCE log
    END
    Log Info  ===== End of testCase FB_DIAG_COMM_TC_089_DDR_STRESS_TEST =====

FB_DIAG_COMM_TC_090_SSD_STRESS_TEST
    [Documentation]  Synopsis=> This test executes to check SSD Stress
    [Tags]  FB_DIAG_COMM_TC_090_SSD_STRESS_TEST  common  minipack2
    Log Info  ===== Start of testCase FB_DIAG_COMM_TC_090_SSD_STRESS_TEST =====
    FOR    ${INDEX}    IN RANGE    1    ${MaxLoopNum}
         Print Loop Info  ${INDEX}
         Set Testcase Timeout  600
         Critical Step  1  switch to centos diag tool
         Step  1  run mcelog under daemon mode
         Step  2  test ssd stress
         Step  3  check MCE log
    END
    Log Info  ===== End of testCase FB_DIAG_COMM_TC_090_SSD_STRESS_TEST =====

FB_DIAG_COMM_TC_091_LPMODE_STRESS_TEST
    [Documentation]  Synopsis=> This test executes to check LPMODE Stress
    [Tags]  FB_DIAG_COMM_TC_091_LPMODE_STRESS_TEST  common  minipack2
    Log Info  ===== Start of testCase FB_DIAG_COMM_TC_091_LPMODE_STRESS_TEST =====
    FOR    ${INDEX}    IN RANGE    1    ${MaxLoopNum}
         Print Loop Info  ${INDEX}
         Set Testcase Timeout  600
         Critical Step  1  switch to centos diag tool
	 Step  1  mp2 copy lpmode script files
         Step  2  run mcelog under daemon mode
         Step  3  test lpmode stress
         Step  4  check MCE log
    END
    Log Info  ===== End of testCase FB_DIAG_COMM_TC_091_LPMODE_STRESS_TEST =====

#Note: SVT wants to temporary disable this test case because of SW issue in MP2.
#FB_DIAG_COMM_TC_092_FPGA_UPGRADE_STRESS_TEST
#    [Documentation]  Synopsis=> This test executes to check FPGA upgrade stress test
#    [Tags]  FB_DIAG_COMM_TC_092_FPGA_UPGRADE_STRESS_TEST  common  minipack2
#    Log Info  ===== Start of testCase FB_DIAG_COMM_TC_092_FPGA_UPGRADE_STRESS_TEST =====
#    FOR    ${INDEX}    IN RANGE    1    ${MaxLoopNum}
#        Print Loop Info  ${INDEX}
#        Set Testcase Timeout  900
#        Critical Step  1  switch to centos diag tool
#        Step  1  run mcelog under daemon mode
#        Step  2  verify bmc command  FPGA_upgrade_stress_cmd  FPGA_upgrade_stress_pattern  path=${FPGA_upgrade_stress_path}
#        Step  3  verify bmc command  verify_log_cmd  FPGA_upgrade_stress_pattern  path=${FPGA_upgrade_stress_path}
#    END
#    Log Info  ===== End of testCase FB_DIAG_COMM_TC_092_FPGA_UPGRADE_STRESS_TEST =====

#Note: SVT wants to temporary disable this test case because of SW issue in MP2.
#FB_DIAG_COMM_TC_095_BIC_UPGRADE_STRESS_TEST
#    [Documentation]  Synopsis=> This test executes to check BIC upgrade stress test
#    [Tags]  FB_DIAG_COMM_TC_095_BIC_UPGRADE_STRESS_TEST  common  minipack2
#    Log Info  ===== Start of testCase FB_DIAG_COMM_TC_095_BIC_UPGRADE_STRESS_TEST =====
#    FOR    ${INDEX}    IN RANGE    1    ${MaxLoopNum}
#        Print Loop Info  ${INDEX}
#        Set Testcase Timeout  900
#        Critical Step  1  switch to centos diag tool
#        Step  2  verify bmc command  BIC_upgrade_stress_cmd  BIC_upgrade_stress_pattern  path=${BIC_upgrade_stress_path}
#        Step  3  verify bmc command  verify_log_cmd  BIC_upgrade_stress_pattern  path=${BIC_upgrade_stress_path}
#    END
#    Log Info  ===== End of testCase FB_DIAG_COMM_TC_095_BIC_UPGRADE_STRESS_TEST =====

FB_DIAG_COMM_TC_096_BIC_stress_test
    [Documentation]  Synopsis=> This test to do Power cycle stress test from BMC side
    [Tags]  FB_DIAG_COMM_TC_096_BIC_stress_test  common  minipack2
     Log Info  ===== Start of testCase FB_DIAG_COMM_TC_096_BIC_stress_test =====
     FOR    ${INDEX}    IN RANGE    1    ${MaxLoopNum}
         Print Loop Info  ${INDEX}
         Set Testcase Timeout  600
         Critical Step  1  switch to openbmc
	 Step  1  mp2 copy bic script files
         Step  2  check bic stress option h
         Step  3  check bic stress option n  2
     END
     Log Info  ===== End of testCase FB_DIAG_COMM_TC_096_BIC_stress_test =====

FB_DIAG_COMM_TC_097_I2C_stress_test
    [Documentation]  Synopsis=> This test to do Power cycle stress test from BMC side
    [Tags]  FB_DIAG_COMM_TC_097_I2C_stress_test  common  minipack2
     Log Info  ===== Start of testCase FB_DIAG_COMM_TC_097_I2C_stress_test =====
     FOR    ${INDEX}    IN RANGE    1    ${MaxLoopNum}
         Print Loop Info  ${INDEX}
         Set Testcase Timeout  2000
         Critical Step  1  switch to openbmc
         Step  1  check i2c stress option h
         Step  2  check i2c stress option n  2
     END
     Log Info  ===== End of testCase FB_DIAG_COMM_TC_097_I2C_stress_test =====

FB_DIAG_COMM_TC_098_FPGA_PCIe_stress_test
    [Documentation]  Synopsis=> This test to do Power cycle stress test from BMC side
    [Tags]  FB_DIAG_COMM_TC_098_FPGA_PCIe_stress_test  common  minipack2
     Log Info  ===== Start of testCase FB_DIAG_COMM_TC_098_FPGA_PCIe_stress_test =====
     FOR    ${INDEX}    IN RANGE    1    ${MaxLoopNum}
         Print Loop Info  ${INDEX}
         Set Testcase Timeout  600
         Critical Step  1  switch to centos
         Step  1  run mcelog under daemon mode
         Step  2  check fpga pcie stress option n  10
     END
     Log Info  ===== End of testCase FB_DIAG_COMM_TC_098_FPGA_PCIe_stress_test =====

FB_DIAG_COMM_TC_100_EMMC_stress_test
    [Documentation]  Synopsis=> This test to do EMMC stress test from BMC side
    [Tags]  FB_DIAG_COMM_TC_100_EMMC_stress_test  common  minipack2
     Log Info  ===== Start of testCase FB_DIAG_COMM_TC_100_EMMC_stress_test =====
     FOR    ${INDEX}    IN RANGE    1    ${MaxLoopNum}
         Print Loop Info  ${INDEX}
         Set Testcase Timeout  600
         Critical Step  1  switch to openbmc
         Step  1  check emmc stress option h
         Step  2  check emmc stress option n  10
     END
     Log Info  ===== End of testCase FB_DIAG_COMM_TC_100_EMMC_stress_test =====

#FB_DIAG_COMM_TC_101_SPI_Device_Scan_Test
#    [Documentation]  Synopsis=> This test to do spi device scan test
#    [Tags]  FB_DIAG_COMM_TC_101_SPI_Device_Scan_Test  common  minipack2
#     Log Info  ===== Start of testCase FB_DIAG_COMM_TC_101_SPI_Device_Scan_Test =====
#     FOR    ${INDEX}    IN RANGE    1    ${MaxLoopNum}
#         Print Loop Info  ${INDEX}
#         Set Testcase Timeout  600
#         Critical Step  1  switch to openbmc
#         Step  1  check flashScan option h
#         Step  2  check flashScan option a
#     END
#     Log Info  ===== End of testCase FB_DIAG_COMM_TC_101_SPI_Device_Scan_Test =====

FB_DIAG_COMM_TC_102_AVS_Test
    [Documentation]  Synopsis=> This test to do avs test
    [Tags]  FB_DIAG_COMM_TC_102_AVS_Test  common  minipack2
     Log Info  ===== Start of testCase FB_DIAG_COMM_TC_102_AVS_Test =====
     FOR    ${INDEX}    IN RANGE    1    ${MaxLoopNum}
         Print Loop Info  ${INDEX}
         Set Testcase Timeout  600
         Critical Step  1  switch to openbmc
         Step  1  check avs option h
         Step  2  check avs option a
     END
     Log Info  ===== End of testCase FB_DIAG_COMM_TC_102_AVS_Test =====

FB_DIAG_COMM_TC_104_PIM_UCD90160_Trim_Test
    [Documentation]  Synopsis=> This test to do pim ucd90160 trim test
    [Tags]  FB_DIAG_COMM_TC_104_PIM_UCD90160_Trim_Test  common  minipack2
     Log Info  ===== Start of testCase FB_DIAG_COMM_TC_104_PIM_UCD90160_Trim_Test =====
     FOR    ${INDEX}    IN RANGE    1    ${MaxLoopNum}
         Print Loop Info  ${INDEX}
         Set Testcase Timeout  3000
         Critical Step  1  switch to openbmc
         Step  1  set pim ucd90160 level  low
         Step  2  verify sensor port1 8 status
         Step  3  set pim ucd90160 level  normal
         Step  4  verify sensor port1 8 status
         Step  5  set pim ucd90160 level  high
         Step  6  verify sensor port1 8 status
         Step  7  set pim ucd90160 level  normal
	 Step  8  cel sensor test bc  pim1
         Step  9  cel sensor test bc  pim2
         Step  10  cel sensor test bc  pim3
         Step  11  cel sensor test bc  pim4
         Step  12  cel sensor test bc  pim5
         Step  13  cel sensor test bc  pim6
         Step  14  cel sensor test bc  pim7
         Step  15  cel sensor test bc  pim8
     END
     Log Info  ===== End of testCase FB_DIAG_COMM_TC_104_PIM_UCD90160_Trim_Test =====

FB_DIAG_COMM_TC_103_Dual_BMC_Flash_Boot_Test
    [Documentation]  Synopsis=> This test to do dula bmc flash boot test
    [Tags]  FB_DIAG_COMM_TC_103_Dual_BMC_Flash_Boot_Test  common  minipack2
     Log Info  ===== Start of testCase FB_DIAG_COMM_TC_103_Dual_BMC_Flash_Boot_Test =====
     FOR    ${INDEX}    IN RANGE    1    ${MaxLoopNum}
         Print Loop Info  ${INDEX}
         Set Testcase Timeout  3000
         Critical Step  1  switch to openbmc
         Step  1  make sure bmc boot from master
         Step  2  verify bmc cel boot test h
         Step  3  verify cel boot test b bmc s master
         Step  4  verify cel boot test b bmc r slave
         Step  5  wait for openbmc prompt back
         Step  6  verify cel boot test b bmc s slave
         Step  7  verify cel boot test b bmc r master
         Step  8  wait for openbmc prompt back
         Step  9  verify cel boot test b bmc s master
         Step  10  make sure bios boot from master
         Step  11  check bios boot info
         Step  12  verify cel boot test a
         Step  13  verify cel boot test b bmc r slave
         Step  14  wait for openbmc prompt back
         Step  15  verify cel boot test b bmc s slave
         Step  16  verify cel boot test a fail
         Step  17  make sure bmc boot from master
	 Step  18  wait for openbmc prompt back
         Step  19  verify cel boot test b bmc s master
     END
     Log Info  ===== End of testCase FB_DIAG_COMM_TC_103_Dual_BMC_Flash_Boot_Test =====

FB_DIAG_COMM_TC_063_UCD_Security_Mode_Check
    [Documentation]  Synopsis=> This test to do UCD Security Mode Check
    [Tags]  FB_DIAG_COMM_TC_063_UCD_Security_Mode_Check  common  minipack2
     Log Info  ===== Start of testCase FB_DIAG_COMM_TC_063_UCD_Security_Mode_Check =====
     FOR    ${INDEX}    IN RANGE    1    ${MaxLoopNum}
         Print Loop Info  ${INDEX}
         Set Testcase Timeout  3000
         Critical Step  1  switch to openbmc check tool
         Step  1  verify ucd security help dict option h
         Step  2  verify ucd security help dict option  -s SMB_1
         Step  3  verify ucd security help dict option  -s SMB_2
         Step  4  verify ucd security help dict option  -s PIM_1
         Step  5  verify ucd security help dict option  -s PIM_2
         Step  6  verify ucd security help dict option  -s PIM_3
         Step  7  verify ucd security help dict option  -s PIM_4
         Step  8  verify ucd security help dict option  -s PIM_5
         Step  9  verify ucd security help dict option  -s PIM_6
         Step  10  verify ucd security help dict option  -s PIM_7
         Step  11  verify ucd security help dict option  -s PIM_8
     END
     Log Info  ===== End of testCase FB_DIAG_COMM_TC_063_UCD_Security_Mode_Check =====

FB_DIAG_COMM_TC_099_Power_cycle_from_BMC_stress_test_BMC
    [Documentation]  Synopsis=> This test to do Power cycle stress test from BMC side
    [Tags]  FB_DIAG_COMM_TC_099_Power_cycle_from_BMC_stress_test  common  minipack2
     Log Info  ===== Start of testCase FB_DIAG_COMM_TC_099_Power_cycle_from_BMC_stress_test =====
     FOR    ${INDEX}    IN RANGE    1    ${MaxLoopNum}
         Print Loop Info  ${INDEX}
         Set Testcase Timeout  900
         Critical Step  1  switch to openbmc
         Step  1  check power cycle stress option h
         Step  2  check power cycle stress option n  2
     END
     Log Info  ===== End of testCase FB_DIAG_COMM_TC_099_Power_cycle_from_BMC_stress_test =====

BMC_DIAG_COMM_TC_105_BMC_reboot_stress_test
    [Documentation]  Synopsis=> This test to do reboot cycle stress test from BMC side
    [Tags]  BMC_DIAG_COMM_TC_105_BMC_reboot_stress_test  common  minipack2
     Log Info  ===== Start of testCase BMC_DIAG_COMM_TC_105_BMC_reboot_stress_test =====
     FOR    ${INDEX}    IN RANGE    1    501
         Print Loop Info  ${INDEX}
         Set Testcase Timeout  900
         Critical Step  1  switch to openbmc
         Step  1  power chassis system
         Step  2  check dmesg log about error
     END
     Log Info  ===== End of testCase BMC_DIAG_COMM_TC_105_BMC_reboot_stress_test =====

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

