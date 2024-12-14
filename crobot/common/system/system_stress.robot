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
# Script       : STRESStem_stress.robot                                                                                         #
# Date         : Aug 16, 2023                                                                                        #
# Author       : Jeff Gong                                                                                                   #
# Description  : This script will run all stress tests(TCG1&TCG2).                                                        #
#                                                                                                                     #
# Script Revision Details:                                                                                            #

#######################################################################################################################

*** Settings ***
Documentation     This suite will perform all stress tests.

#Library           Keyword_Resource.py
Resource          Resource.robot
Library           DiagLibAdapter.py
Variables         Diag_OS_variable.py

Suite Setup       Diag Connect Device
Suite Teardown    Diag Disconnect Device

*** Variables ***
${MaxLoopNum}     6

*** Test Cases ***
##### Start - Facebook Common STRESStem Stress Test Case Group 1 #####
META_STRESS_COM_TCG1_00_Precondition_Check_Test
    [Documentation]  Synopsis=> This test executes precondition checks before starting any stress test.
    [Tags]  META_STRESS_COM_TCG1_00_Precondition_Check_Test  meta_stress  wedge400c  wedge400  minipack2
    [Setup]  set verbose level
    Log Info  ===== Start of META_STRESS_COM_TCG1_00_Precondition_Check_Test =====
    Set Testcase Timeout  ${Timeout1800}
   # wedge400c check all system sw fw versions
   # check usb disk presence
   # check cpu and openbmc ipv6 interface
   # wedge400c init and check all eloop modules presence
    copy sdk soc files for BCM  ${centos_mode}   #for w400
    wedge400c check pem psu connection    #for wedge
    check psu connection           #for mp2
    check emmc available space
    remove all cpu logs
	check all cpu test tools and fw version
    check all bmc test directories and fw version
    check dev ttyusb0     #for wedge
    Log Info  ===== End of FB_STRESS_COM_TCG1_00_Precondition_Check_Test =====


META_STRESS_COM_TCG1_01_Sensor_Reading_Stress-High_Loading
    [Documentation]  Synopsis=> This test checks the sensor readings under cpu high loading condition.
    [Tags]  META_STRESS_COM_TCG1_01_Sensor_Reading_Stress-High_Loading  meta_stress  wedge400c  wedge400  minipack2
    Log Info  ===== Start of testCase META_STRESS_COM_TCG1_01_Sensor_Reading_Stress-High_Loading =====
    #Set Testcase Timeout  ${Timeout30000}
    #Set Global Variable     ${MaxRepeatCount5}       1
    #Set Global Variable     ${StressLoopTime1800}    600
    set sensor reading stress cycles  ${MaxRepeatCount70}
    set auto load script stress loop time  ${StressLoopTime25500}
    #switch to openbmc check tool
    run sensor reading high loading stress test    #for w400c
    w400 run sensor reading high loading stress test     #for w400
    minipack2 run sensor reading high loading stress test     #for mp2
    Log Info  ===== End of testCase META_STRESS_COM_TCG1_01_Sensor_Reading_Stress-High_Loading =====


META_STRESS_COM_TCG1_02_FPGA_PCIE_Bus_Stress_Test
    [Documentation]  Synopsis=> This test checks the function of FPGA PCIE bus.
    [Tags]  META_STRESS_COM_TCG1_02_FPGA_PCIE_Bus_Stress_Test  common  wedge400c  wedge400  minipack2
    Log Info  ===== Start of META_STRESS_COM_TCG1_02_FPGA_PCIE_Bus_Stress_Test =====
    [Setup]  ssh login bmc
    #Set Testcase Timeout  ${Timeout8000}
    #Set Global Variable     ${StressLoopTime1800}    60
    set fpga stress loop time  ${StressLoopTime10000}
    switch to centos diag tool
    run fpga pcie bus stress test
    Log Info  ===== End of META_STRESS_COM_TCG1_02_FPGA_PCIE_Bus_Stress_Test =====
    [Teardown]  ssh disconnect


META_STRESS_COM_TCG1_03_OpenBMC_Utility_Stability_Test
    [Documentation]  Synopsis=> This test checks the stability of openbmc utility.
    [Tags]  META_STRESS_COM_TCG1_03_OpenBMC_Utility_Stability_Test  wedge400c  wedge400  minipack2
    Log Info  ===== Start of META_STRESS_COM_TCG1_03_OpenBMC_Utility_Stability_Test =====
    #Set Testcase Timeout  ${Timeout18000}
    #Set Global Variable     ${MaxRepeatCount200}    1
    set openbmc utility test cycles    ${MaxRepeatCount2000}
    switch to openbmc check tool
    run openbmc utility stability test    #for wedge
    minipack2 run openbmc utility stability test    #for mp2
    Log Info  ===== End of META_STRESS_COM_TCG1_03_OpenBMC_Utility_Stability_Test =====


META_STRESS_COM_TCG1_04_IPMI_Interface_Stress_Test
    [Documentation]  Synopsis=> This test checks the function of IPMI interface.
    [Tags]  META_STRESS_COM_TCG1_04_IPMI_Interface_Stress_Test  wedge400c  wedge400  minipack2
    Log Info  ===== Start of META_STRESS_COM_TCG1_04_IPMI_Interface_Stress_Test =====
    #Set Testcase Timeout  ${Timeout8000}
    #Set Global Variable     ${MaxRepeatCount100}    1
    set ipmi test cycles    ${MaxRepeatCount2000}
    switch to centos diag tool
    wedge400c run ipmi command stress test    #for wedge
    minipack2 run ipmi command stress test    #for mp2
    Log Info  ===== End of META_STRESS_COM_TCG1_04_IPMI_Interface_Stress_Test =====


META_STRESS_COM_TCG1_05_COMe_NVMe_SSD_RW_Stress_Test
    [Documentation]  Synopsis=> This test checks the function of NVMe SSD RW access.
    [Tags]  META_STRESS_COM_TCG1_05_COMe_NVMe_SSD_RW_Stress_Test  common  wedge400c  wedge400  minipack2
    Log Info  ===== Start of META_STRESS_COM_TCG1_05_COMe_NVMe_SSD_RW_Stress_Test =====
    Set Testcase Timeout  ${Timeout10000}
    #Set Global Variable     ${StressLoopTime1800}   60
    set nvme stress loop time  ${StressLoopTime10000}
    switch to centos diag tool
    run nvme access stress test
    Log Info  ===== End of META_STRESS_COM_TCG1_05_COMe_NVMe_SSD_RW_Stress_Test =====


META_STRESS_COM_TCG1_06_Loopback_EEPROM_Access_Stress_Test
    [Documentation]  Synopsis=> This test checks the function of EEPROM access.
    [Tags]  META_STRESS_COM_TCG1_06_Loopback_EEPROM_Access_Stress_Test  meta_stress  wedge400c  wedge400
    Log Info  ===== Start of META_STRESS_COM_TCG1_06_Loopback_EEPROM_Access_Stress_Test =====
    #Set Testcase Timeout  ${Timeout8000}
    #Set Global Variable     ${StressLoopTime1800}    60
    #set eeprom stress loop time  ${StressLoopTime1800}
    switch to centos diag tool
    meta run eeprom access stress test    #for wedge
    Log Info  ===== End of META_STRESS_COM_TCG1_06_Loopback_EEPROM_Access_Stress_Test =====


META_STRESS_COM_TCG1_07_BMC_And_CPU_OOB_Link_Stress_Test
    [Documentation]  Synopsis=> This test checks the function of BMC and CPU OOB link.
    [Tags]  META_STRESS_COM_TCG1_07_BMC_And_CPU_OOB_Link_Stress_Test  common  wedge400c  wedge400  minipack2
    Log Info  ===== Start of META_STRESS_COM_TCG1_07_BMC_And_CPU_OOB_Link_Stress_Test =====
    Set Testcase Timeout  ${Timeout10000}
    #Set Global Variable     ${StressLoopTime900}    60
    set bmc cpu link stress loop time  ${StressLoopTime10000}
    switch to centos diag tool
    run bmc cpu oob link access stress test
    Log Info  ===== End of META_STRESS_COM_TCG1_07_BMC_And_CPU_OOB_Link_Stress_Test =====


META_STRESS_COM_TCG1_08_BMC_And_CPU_Internal_USB_Network_Stress_Test
    [Documentation]  Synopsis=> This test checks the function of BMC and CPU internal USB network link.
    [Tags]  META_STRESS_COM_TCG1_08_BMC_And_CPU_Internal_USB_Network_Stress_Test  common  wedge400c  wedge400  minipack2
    Log Info  ===== Start of META_STRESS_COM_TCG1_08_BMC_And_CPU_Internal_USB_Network_Stress_Test =====
    Set Testcase Timeout  ${Timeout10000}
    #Set Global Variable     ${StressLoopTime900}    60
    set bmc cpu link stress loop time  ${StressLoopTime10000}
    switch to centos diag tool
    run bmc cpu internal usb network stress test
    Log Info  ===== End of META_STRESS_COM_TCG1_08_BMC_And_CPU_Internal_USB_Network_Stress_Test =====


META_STRESS_COM_TCG1_09_Sensor_Reading_Stress-Idle
    [Documentation]  Synopsis=> This test checks the sensor readings under cpu idle condition.
    [Tags]  META_STRESS_COM_TCG1_09_Sensor_Reading_Stress-Idle  meta_stress  wedge400c  wedge400  minipack2
    Log Info  ===== Start of META_STRESS_COM_TCG1_09_Sensor_Reading_Stress-Idle =====
    #Set Testcase Timeout  ${Timeout3600}
    #Set Global Variable     ${MaxRepeatCount5}       1
    #Set Global Variable     ${StressLoopTime1800}    600
    #set sensor reading stress cycles  ${MaxRepeatCount5}
    #set auto load script stress loop time  ${StressLoopTime1800}
    FOR    ${INDEX}    IN RANGE    1    21
        Print Loop Info  ${INDEX}   ${MaxRepeatCount20}
        run sensor option u and verify GB run test     #for wedge
        minipack2 run sensor reading idle stress test    #for mp2
    END
    exit sdk mode    #for w400c
    Log Info  ===== Start of META_STRESS_COM_TCG1_09_Sensor_Reading_Stress-Idle =====


META_STRESS_COM_TCG1_10_COMe_Memory_Stress_Test
    [Documentation]  Synopsis=> This test runs the COMe memory stress test.
    [Tags]  META_STRESS_COM_TCG1_10_COMe_Memory_Stress_Test  common   wedge400c  wedge400  minipack2
    Log Info  ===== Start of META_STRESS_COM_TCG1_10_COMe_Memory_Stress_Test =====
    #Set Testcase Timeout  ${Timeout8000}
    #Set Global Variable     ${StressLoopTime900}    60
    set come memory stress loop time  ${StressLoopTime10000}
    switch to centos
    run come memory test
    Log Info  ===== End of META_STRESS_COM_TCG1_10_COMe_Memory_Stress_Test =====


META_STRESS_COM_TCG1_11_COMe_CPU_Stress_Test
    [Documentation]  Synopsis=> This test runs the cpu stress test.
    [Tags]  META_STRESS_COM_TCG1_11_COMe_CPU_Stress_Test  common  wedge400c  wedge400  minipack2
    Log Info  ===== Start of META_STRESS_COM_TCG1_11_COMe_CPU_Stress_Test =====
    #Set Testcase Timeout  ${Timeout8000}
    #Set Global Variable     ${StressLoopTime900}    60
    set cpu stress loop time  ${StressLoopTime10000}
    switch to centos
    run cpu stress test
    Log Info  ===== End of META_STRESS_COM_TCG1_11_COMe_CPU_Stress_Test =====


META_STRESS_COM_TCG1_12_OpenBMC_Memory_Stress_Test
    [Documentation]  Synopsis=> This test checks the function of openbmc memory.
    [Tags]  META_STRESS_COM_TCG1_12_OpenBMC_Memory_Stress_Test  common  wedge400c  wedge400  minipack2
    Log Info  ===== Start of META_STRESS_COM_TCG1_12_OpenBMC_Memory_Stress_Test =====
    #Set Testcase Timeout  ${Timeout30000}
    #Set Global Variable     ${StressLoopTime1800}    60
    set openbmc memory stress loop time  ${StressLoopTime21000}
    switch to openbmc check tool
    run openbmc memory stress test  100M 2
    Log Info  ===== End of META_STRESS_COM_TCG1_12_OpenBMC_Memory_Stress_Test =====


META_STRESS_COM_TCG1_13_OpenBMC_I2C_Bus_Scan_Stress_Test
    [Documentation]  Synopsis=> This test checks the function of openbmc i2c scan.
    [Tags]  META_STRESS_COM_TCG1_13_OpenBMC_I2C_Bus_Scan_Stress_Test  wedge400c  wedge400  minipack2
    Log Info  ===== Start of META_STRESS_COM_TCG1_13_OpenBMC_I2C_Bus_Scan_Stress_Test =====
    Set Testcase Timeout  ${Timeout10000}
    #Set Global Variable     ${StressLoopTime1800}    60
    set i2c scan stress loop time  ${StressLoopTime10000}
    switch to openbmc check tool
    wedge400c run openbmc i2c scan stress test    #for wedge400c
    minipack2 run openbmc i2c scan stress test    #for mp2
    wedge400 run openbmc i2c scan stress test     #for w400
    Log Info  ===== End of META_STRESS_COM_TCG1_13_OpenBMC_I2C_Bus_Scan_Stress_Test =====


META_STRESS_COM_TCG1_14_TPM_Module_Access_Stress_test
    [Documentation]  Synopsis=> This test checks the function of TPM access.
    [Tags]  META_STRESS_COM_TCG1_14_TPM_Module_Access_Stress_test  wedge400c  wedge400  minipack2
    Log Info  ===== Start of META_STRESS_COM_TCG1_14_TPM_Module_Access_Stress_test =====
    #Set Testcase Timeout  ${Timeout4500}
    #Set Global Variable     ${MaxRepeatCount20}    1
    set tpm access test cycles    ${MaxRepeatCount1000}
    switch to centos diag tool
    run tpm access stress test    #for wedge
    minipack2 run tpm access stress test    #for mp2
    Log Info  ===== End of META_STRESS_COM_TCG1_14_TPM_Module_Access_Stress_test =====


META_STRESS_COM_TCG1_15_Each_Port_Enable_Disable_Stress_Test
    [Documentation]  Synopsis=> This test runs the ports link stress test for each port.
    [Tags]  META_STRESS_COM_TCG1_15_Each_Port_Enable_Disable_Stress_Test  meta_stress  wedge400c  wedge400  minipack2
    Log Info  ===== Start of META_STRESS_COM_TCG1_15_Each_Port_Enable_Disable_Stress_Test =====
    Set Testcase Timeout  ${Timeout30000}
    #Set Global Variable     ${MaxRepeatCount10}    1
    #set port linkup test stress cycles    ${MaxRepeatCount10}
    #set port linkup test stress time    ${StressLoopTime60}
    set port enable disable test stress cycles    ${MaxRepeatCount25}
    set port enable disable test stress time    ${StressLoopTime60}
    switch to centos diag tool
    FOR    ${INDEX}    IN RANGE    1    3
        Print Loop Info  ${INDEX}   ${MaxRepeatCount2}
        w400 run port enable disable test  False
    END
    minipack2 run port enable disable test  False
    FOR    ${INDEX}    IN RANGE    1    91
        Print Loop Info  ${INDEX}   ${MaxRepeatCount25}
        wedge400c run port enable disable test
    END
    Log Info  ===== Enable of META_STRESS_COM_TCG1_15_Each_Port_Enable_Disable_Stress_Test =====

META_STRESS_COM_TCG1_16_SDK_Re-Init_Stress_Test
    [Documentation]  Synopsis=> This test runs the SDK re-init stress test.
    [Tags]  META_STRESS_COM_TCG1_16_SDK_Re-Init_Stress_Test  meta_stress  wedge400c  wedge400  minipack2
    Log Info  ===== Start of META_STRESS_COM_TCG1_16_SDK_Re-Init_Stress_Test =====
    Set Testcase Timeout  ${Timeout8000}
    #Set Global Variable     ${MaxRepeatCount10}    1
    set re init test stress cycles    ${MaxRepeatCount70}
    set re init test stress time    ${StressLoopTime60}
    switch to centos
    w400 run sdk re init test
    minipack2 run sdk re init test
    FOR    ${INDEX}    IN RANGE    1    51
        Print Loop Info  ${INDEX}   ${MaxRepeatCount50}
        wedge400c run sdk re init test
    END
    Log Info  ===== End of META_STRESS_COM_TCG1_16_SDK_Re-Init_Stress_Test =====

META_STRESS_COM_TCG1_17_Snake_Traffic_Test
    [Documentation]  Synopsis=> This test runs the snake traffic test.
    [Tags]  META_STRESS_COM_TCG1_17_Snake_Traffic_Test  meta_stress  wedge400c  wedge400  minipack2
    Log Info  ===== Start of META_STRESS_COM_TCG1_17_Snake_Traffic_Test =====
    Set Testcase Timeout  ${Timeout8000}
    set snake traffic test stress time  ${StressLoopTime8000}
    switch to centos
    wedge400c run snake traffic test
    w400 run snake traffic test
    minipack2 run snake traffic test
    Log Info  ===== End of testCase META_STRESS_COM_TCG1_17_Snake_Traffic_Test =====
##### End - Facebook Common STRESStem Stress Test Case Group 1 #####

####################### TCG2 stress test ########################
META_STRESS_COM_TCG2_02_Chassis_Power_Cycling_Stress_Test
    [Documentation]  Synopsis=> This test runs chassis power cycle, run about 5h.
    [Tags]  META_STRESS_COM_TCG2_02_Chassis_Power_Cycling_Stress_Test  meta_stress  wedge400c  wedge400  minipack2
    Log Info  ===== Start of META_STRESS_COM_TCG2_02_Chassis_Power_Cycling_Stress_Test =====
    #Set Testcase Timeout  ${Timeout8000}
    #Print Loop Info  ${INDEX}   ${MaxRepeatCount2}
    set snake traffic test stress time  ${StressLoopTime80}
    FOR    ${INDEX}    IN RANGE    1    21
        Critical Step  1  switch to centos
        Step  1  come side driver auto load check
        Step  2  come side sdk traffic check
        Step  3  fw version check in come side
        Step  4  pcie and disk scan test in come side
        Step  5  ipv6 ping test  ${centos_mode}
        Step  6  check dev ttyusb0
        Step  7  current version check in bmc side  ${openbmc_mode}
        Step  8  sensor info check in bmc side
        Step  9  fru info check in bmc side
        Step  10  power cycle chassis test  ${openbmc_mode}
    END
    Log Info  ===== End of testCase META_STRESS_COM_TCG2_02_Chassis_Power_Cycling_Stress_Test =====

META_STRESS_COM_TCG2_03_COMe_Warm_Reset_from_High_Loading_Test
    [Documentation]  Synopsis=> This test runs COMe Warm Reset High loading Test, sdk in background, run about 4h.
    [Tags]  META_STRESS_COM_TCG2_03_COMe_Warm_Reset_from_High_Loading_Test  meta_stress  wedge400c  wedge400  minipack2
    Log Info  ===== Start of META_STRESS_COM_TCG2_03_COMe_Warm_Reset_from_High_Loading_Test =====
    #Set Testcase Timeout  ${Timeout8000}
    #Print Loop Info  ${INDEX}   ${MaxRepeatCount2}
    set snake traffic test stress time  ${StressLoopTime1800}
    FOR    ${INDEX}    IN RANGE    1    21
        Critical Step  1  switch to centos
        Step  1  come side driver auto load check
        Step  2  warm reset sdk traffic check  ${centos_mode}
        Step  3  fw version check in come side
        Step  4  pcie and disk scan test in come side
        Step  5  ipv6 ping test  ${centos_mode}
        Step  6  come warm reset test  ${centos_mode}
    END
    Log Info  ===== End of testCase META_STRESS_COM_TCG2_03_COMe_Warm_Reset_from_High_Loading_Test =====
    [Teardown]  Run Keyword If Test Failed  come warm reset test  ${centos_mode}

META_STRESS_COM_TCG2_04_COMe_Power_On_And_Off_Stress_Test
    [Documentation]  Synopsis=> This test runs COMe Power On/Off Test, run about 4h.
    [Tags]  META_STRESS_COM_TCG2_04_COMe_Power_On_And_Off_Stress_Test  meta_stress  wedge400c  wedge400  minipack2
    Log Info  ===== Start of META_STRESS_COM_TCG2_04_COMe_Power_On_And_Off_Stress_Test =====
    #Set Testcase Timeout  ${Timeout8000}
    #Print Loop Info  ${INDEX}   ${MaxRepeatCount2}
    set snake traffic test stress time  ${StressLoopTime120}
    FOR    ${INDEX}    IN RANGE    1    16
        Critical Step  1  switch to centos
        Step  1  come side driver auto load check
        Step  2  come side sdk traffic check
        Step  3  fw version check in come side
        Step  4  pcie and disk scan test in come side
        Step  5  ipv6 ping test  ${centos_mode}
        Step  6  check dev ttyusb0
        Step  7  current version check in bmc side  ${openbmc_mode}
        Step  8  sensor info check in bmc side
        Step  9  fru info check in bmc side
        Step  10  power on and off test  ${openbmc_mode}  ${WEDGE400_POWER_RESET}
    END
    Log Info  ===== End of testCase META_STRESS_COM_TCG2_04_COMe_Power_On_And_Off_Stress_Test =====

META_STRESS_COM_TCG2_05_COMe_Hard_Reset_Stress_Test
    [Documentation]  Synopsis=> This test runs COMe Hard Reset Test, run about 4h.
    [Tags]  META_STRESS_COM_TCG2_05_COMe_Hard_Reset_Stress_Test  meta_stress  wedge400c  wedge400  minipack2
    Log Info  ===== Start of META_STRESS_COM_TCG2_05_COMe_Hard_Reset_Stress_Test =====
    #Set Testcase Timeout  ${Timeout8000}
    #Print Loop Info  ${INDEX}   ${MaxRepeatCount2}
    set snake traffic test stress time  ${StressLoopTime120}
    FOR    ${INDEX}    IN RANGE    1    21
        Critical Step  1  switch to centos
        Step  1  come side driver auto load check
        Step  2  come side sdk traffic check
        Step  3  fw version check in come side
        Step  4  pcie and disk scan test in come side
        Step  5  ipv6 ping test  ${centos_mode}
        Step  6  check dev ttyusb0
        Step  7  current version check in bmc side  ${openbmc_mode}
        Step  8  sensor info check in bmc side
        Step  9  fru info check in bmc side
        Step  10  power on and off test  ${openbmc_mode}  ${MP2_POWER_RESET}
    END
    Log Info  ===== End of testCase META_STRESS_COM_TCG2_05_COMe_Hard_Reset_Stress_Test =====

META_STRESS_COM_TCG2_06_Primary_BIOS_Update_Stress_Test
    [Documentation]  Synopsis=> This test runs bios update Test, run about 3.5h.
    [Tags]  META_STRESS_COM_TCG2_06_Primary_BIOS_Update_Stress_Test  meta_stress  wedge400c  wedge400  minipack2  critical
    Log Info  ===== Start of META_STRESS_COM_TCG2_06_Primary_BIOS_Update_Stress_Test =====
    #Set Testcase Timeout  ${Timeout8000}
    #Print Loop Info  ${INDEX}   ${MaxRepeatCount2}
    set snake traffic test stress time  ${StressLoopTime5}
    Step  1  copy image file  ${openbmc_mode}  ${BIOSImage}
    FOR    ${INDEX}    IN RANGE    1    11
        Critical Step  1  switch to openbmc
        Step  2  check bmc or bios master status  ${BMCImage}
        Step  3  check bmc or bios master status  ${BIOSImage}
        Step  4  check scm fw version
        Step  5  fw update check  ${FlashLow}  ${BIOSImage}
        Step  6  fw update check  ${FlashHigh}  ${BIOSImage}
    END
    Step  7  power cycle chassis test  ${openbmc_mode}
    Log Info  ===== End of testCase META_STRESS_COM_TCG2_06_Primary_BIOS_Update_Stress_Test =====


META_STRESS_COM_TCG2_07_CPLD_Online_Update_Stress_Test
    [Documentation]  Synopsis=> This test runs cpld update Test, run about 5h.
    [Tags]  META_STRESS_COM_TCG2_07_CPLD_Online_Update_Stress_Test  meta_stress  wedge400c  wedge400  minipack2  critical
    Log Info  ===== Start of META_STRESS_COM_TCG2_07_CPLD_Online_Update_Stress_Test =====
    #Set Testcase Timeout  ${Timeout8000}
    Step  1  copy image file  ${openbmc_mode}  ${CPLDImage}
    FOR    ${INDEX}    IN RANGE    1    16
        Print Loop Info  ${INDEX}   ${MaxRepeatCount2}
        set snake traffic test stress time  ${StressLoopTime5}
        Critical Step  1  switch to openbmc
        Step  2  check bmc or bios master status  ${BMCImage}
        Step  3  check all fw version
        Step  4  cpld update fw check  ${FlashLow}  ${CPLDImage}
        Step  5  cpld update fw check  ${FlashHigh}  ${CPLDImage}
    END
    Log Info  ===== End of testCase META_STRESS_COM_TCG2_07_CPLD_Online_Update_Stress_Test =====

META_STRESS_COM_TCG2_08_FPGA_Online_Update_Stress_Test
    [Documentation]  Synopsis=> This test runs fpga update Test, run about 5h.
    [Tags]  META_STRESS_COM_TCG2_08_FPGA_Online_Update_Stress_Test  meta_stress  wedge400c  wedge400  minipack2  critical
    Log Info  ===== Start of META_STRESS_COM_TCG2_08_FPGA_Online_Update_Stress_Test =====
    #Set Testcase Timeout  ${Timeout8000}
    Step  1  copy image file  ${openbmc_mode}  ${FPGAImage}
    FOR    ${INDEX}    IN RANGE    1    16
        Print Loop Info  ${INDEX}   ${MaxRepeatCount2}
        set snake traffic test stress time  ${StressLoopTime5}
        Critical Step  1  switch to openbmc
        Step  2  check bmc or bios master status  ${BMCImage}
        Step  3  check all fw version
        Step  4  fpga update fw check  ${FlashLow}  ${FPGAImage}
        Step  5  fpga update fw check  ${FlashHigh}  ${FPGAImage}
    END
    Log Info  ===== End of testCase META_STRESS_COM_TCG2_08_FPGA_Online_Update_Stress_Test =====

META_STRESS_COM_TCG2_09_Full_Loading_Stress_Test
    [Documentation]  Synopsis=> This test runs full loading Test, run about 5h.
    [Tags]  META_STRESS_COM_TCG2_09_Full_Loading_Stress_Test  meta_stress  wedge400c  wedge400  minipack2
    Log Info  ===== Start of META_STRESS_COM_TCG2_09_Full_Loading_Stress_Test =====
    #Set Testcase Timeout  ${Timeout8000}
    FOR    ${INDEX}    IN RANGE    1    51
        Print Loop Info  ${INDEX}   ${MaxRepeatCount2}
        set snake traffic test stress time  ${StressLoopTime80}
        set auto load script stress loop time  ${StressLoopTime60}
        Critical Step  1  switch to centos
        Step  1  check some log files  False
        Step  2  warm reset sdk traffic check  ${centos_mode}
        Step  3  check some log files  True
        Step  4  check sdk result and exit  sdk_env=background
    END
    Log Info  ===== End of testCase META_STRESS_COM_TCG2_09_Full_Loading_Stress_Test =====

META_STRESS_COM_TCG2_11_System_Idle_Or_Working_State_Swap_Test
    [Documentation]  Synopsis=> This test runs idle and working swap Test, run about 2.5h.
    [Tags]  META_STRESS_COM_TCG2_11_System_Idle_Or_Working_State_Swap_Test  meta_stress  wedge400c  wedge400  minipack2
    Log Info  ===== Start of META_STRESS_COM_TCG2_11_System_Idle_Or_Working_State_Swap_Test =====
    #Set Testcase Timeout  ${Timeout8000}
    FOR    ${INDEX}    IN RANGE    1    21
        Print Loop Info  ${INDEX}   ${MaxRepeatCount2}
        set snake traffic test stress time  ${StressLoopTime120}
        Critical Step  1  switch to centos
        Step  1  fw version check in come side
        Step  2  come side sdk traffic check
        Step  3  come side idle check  ${centos_mode}
    END
    Log Info  ===== End of testCase META_STRESS_COM_TCG2_11_System_Idle_Or_Working_State_Swap_Test =====

META_STRESS_COM_TCG2_12_System_Idle_Stress_Test
    [Documentation]  Synopsis=> This test runs system idle Test, run about 8h.
    [Tags]  META_STRESS_COM_TCG2_12_System_Idle_Stress_Test  meta_stress  wedge400c  wedge400  minipack2
    Log Info  ===== Start of META_STRESS_COM_TCG2_12_System_Idle_Stress_Test =====
    #Set Testcase Timeout  ${Timeout8000}
    #Print Loop Info  ${INDEX}   ${MaxRepeatCount2}
    set snake traffic test stress time  ${StressLoopTime3600}
    FOR    ${INDEX}    IN RANGE    1    7
        Critical Step  1  switch to centos
        Step  1  check system idle test
    END
    Log Info  ===== End of testCase META_STRESS_COM_TCG2_12_System_Idle_Stress_Test =====

META_STRESS_COM_TCG2_13_BIC_Update_Stress_Test
    [Documentation]  Synopsis=> This test runs bic update Test, run about 5h.
    [Tags]  META_STRESS_COM_TCG2_13_BIC_Update_Stress_Test  meta_stress  wedge400c  wedge400  minipack2  critical
    Log Info  ===== Start of META_STRESS_COM_TCG2_13_BIC_Update_Stress_Test =====
    #Set Testcase Timeout  ${Timeout8000}
    Step  1  copy image file  ${openbmc_mode}  ${BICImage}
    FOR    ${INDEX}    IN RANGE    1    21
        Print Loop Info  ${INDEX}   ${MaxRepeatCount2}
        set snake traffic test stress time  ${StressLoopTime5}
        Critical Step  1  switch to openbmc
        Step  2  check bmc or bios master status  ${BMCImage}
        Step  3  check bmc or bios master status  ${BIOSImage}
        Step  4  check scm fw version
        Step  5  fw update check  ${FlashLow}  ${BICImage}
        Step  6  fw update check  ${FlashHigh}  ${BICImage}
    END
    Log Info  ===== End of testCase META_STRESS_COM_TCG2_13_BIC_Update_Stress_Test =====

META_STRESS_COM_TCG2_14_COMe_Warm_Reset_Stress_Test
    [Documentation]  Synopsis=> This test runs come warm reset Test, run about 4h.
    [Tags]  META_STRESS_COM_TCG2_14_COMe_Warm_Reset_Stress_Test  meta_stress  wedge400c  wedge400  minipack2
    Log Info  ===== Start of META_STRESS_COM_TCG2_14_COMe_Warm_Reset_Stress_Test =====
    #Set Testcase Timeout  ${Timeout8000}
    FOR    ${INDEX}    IN RANGE    1    41
        Print Loop Info  ${INDEX}   ${MaxRepeatCount2}
        set snake traffic test stress time  ${StressLoopTime1800}
        Critical Step  1  switch to centos
        Step  1  come side driver auto load check
        Step  2  fw version check in come side
        Step  3  pcie and disk scan test in come side
        Step  4  ipv6 ping test  ${centos_mode}
        Step  5  come warm reset test  ${centos_mode}
    END
    Log Info  ===== End of testCase META_STRESS_COM_TCG2_14_COMe_Warm_Reset_Stress_Test =====

META_STRESS_COM_TCG2_15_Master_BMC_Online_Update_Stress_Test
    [Documentation]  Synopsis=> This test runs bmc update Test, run about 3.5h.
    [Tags]  META_STRESS_COM_TCG2_15_Master_BMC_Online_Update_Stress_Test  meta_stress  wedge400c  wedge400  minipack2  critical
    Log Info  ===== Start of META_STRESS_COM_TCG2_15_Master_BMC_Online_Update_Stress_Test =====
    #Set Testcase Timeout  ${Timeout8000}
    Step  1  copy image file  ${openbmc_mode}  ${BMCImage}
    FOR    ${INDEX}    IN RANGE    1    21
        Print Loop Info  ${INDEX}   ${MaxRepeatCount2}
        set snake traffic test stress time  ${StressLoopTime5}
        Critical Step  1  switch to openbmc
        Step  2  check bmc or bios master status  ${BMCImage}
        Step  3  fw update check  ${FlashLow}  ${BMCImage}
        Step  4  fw update check  ${FlashHigh}  ${BMCImage}
    END
    Log Info  ===== End of testCase META_STRESS_COM_TCG2_15_Master_BMC_Online_Update_Stress_Test =====

META_STRESS_COM_TCG2_16_OpenBMC_Swap_Stress_Test
    [Documentation]  Synopsis=> This test runs openbmc swap Test, run about 2.5h.
    [Tags]  META_STRESS_COM_TCG2_16_OpenBMC_Swap_Stress_Test  meta_stress  wedge400c  wedge400  minipack2
    Log Info  ===== Start of META_STRESS_COM_TCG2_16_OpenBMC_Swap_Stress_Test =====
    #Set Testcase Timeout  ${Timeout8000}
    FOR    ${INDEX}    IN RANGE    1    26
        Print Loop Info  ${INDEX}   ${MaxRepeatCount2}
        set snake traffic test stress time  ${StressLoopTime3600}
        Critical Step  1  switch to openbmc
        Step  1  check scm fw version
        Step  2  eMMC check in bmc side
        Step  3  check bmc or bios master status  ${BMCImage}
        Step  4  diag switch to bmc slave region
        Step  5  diag switch to bmc master region
    END
    Log Info  ===== End of testCase META_STRESS_COM_TCG2_16_OpenBMC_Swap_Stress_Test =====

META_STRESS_COM_TCG2_19_Reset_Port_Link_Stress_Test
    [Documentation]  Synopsis=> This test runs reset port link test, run about 6h.
    [Tags]  META_STRESS_COM_TCG2_19_Reset_Port_Link_Stress_Test  meta_stress  wedge400  minipack2
    Log Info  ===== Start of META_STRESS_COM_TCG2_19_Reset_Port_Link_Stress_Test =====
    Critical Step  1  switch to centos
    Step  1  init sdk check
    FOR    ${INDEX}    IN RANGE    1    11
        Print Loop Info  ${INDEX}   ${MaxRepeatCount2}
        set snake traffic test stress time  ${StressLoopTime80}
        Step  2  check reset port link test
    END
    Log Info  ===== Enable of META_STRESS_COM_TCG2_19_Reset_Port_Link_Stress_Test =====
    [Teardown]  exit sdk env test

META_STRESS_COM_TCG2_23_Sol_Stress_Test
    [Documentation]  Synopsis=> This test runs sol stress Test, run about 2h.
    [Tags]  META_STRESS_COM_TCG2_23_Sol_Stress_Test  meta_stress  wedge400c  wedge400  minipack2
    Log Info  ===== Start of META_STRESS_COM_TCG2_23_Sol_Stress_Test =====
    #Set Testcase Timeout  ${Timeout8000}
    FOR    ${INDEX}    IN RANGE    1    901
        Print Loop Info  ${INDEX}   ${MaxRepeatCount2}
        set snake traffic test stress time  ${StressLoopTime1800}
        Critical Step  1  switch to centos
        Step  1  check sol stress test
    END
    Log Info  ===== End of testCase META_STRESS_COM_TCG2_23_Sol_Stress_Test =====
    [Teardown]  clean log file    filePath=/home    logfile=test.log

META_STRESS_COM_TCG2_SPEC_03_All_Ports_Enable_Disable_Link_Stress_Test
    [Documentation]  Synopsis=> This test runs all ports link stress test for BRM chip, run about 2h.
    [Tags]  META_STRESS_COM_TCG2_SPEC_03_All_Ports_Enable_Disable_Link_Stress_Test  meta_stress  wedge400  minipack2
    Log Info  ===== Start of META_STRESS_COM_TCG2_SPEC_03_All_Ports_Enable_Disable_Link_Stress_Test =====
    set port enable disable test stress cycles    ${MaxRepeatCount25}
    set port enable disable test stress time    ${StressLoopTime60}
    Step  1  switch to centos diag tool
    Step  2  w400 run port enable disable test  True
    Step  3  minipack2 run port enable disable test  True
    Log Info  ===== Enable of META_STRESS_COM_TCG2_SPEC_03_All_Ports_Enable_Disable_Link_Stress_Test =====

META_STRESS_SPEC_TCG2_10_CPU_Mgmt_Port_Performance_Test
    [Documentation]  Synopsis=> This test runs CPU Mgmt port performance test.
    [Tags]  META_STRESS_SPEC_TCG2_10_CPU_Mgmt_Port_Performance_Test  SPEC_10  meta_stress
    Log Info  ===== Start of META_STRESS_SPEC_TCG2_10_CPU_Mgmt_Port_Performance_Test =====
    #Set Testcase Timeout  ${Timeout8000}
    FOR    ${INDEX}    IN RANGE    1    ${MaxLoopNum}
        Print Loop Info  ${INDEX}   ${MaxRepeatCount2}
        set auto load script stress loop time  ${StressLoopTime21600}
        Critical Step  1  switch to centos
        Step  1  check iperf tool  path=/home
        Step  2  check cpu mgmt port test
    END
    Log Info  ===== End of testCase META_STRESS_SPEC_TCG2_10_CPU_Mgmt_Port_Performance_Test =====

META_STRESS_SPEC_TCG2_20_Optics_Lpmode_Link_Stress_Test
    [Documentation]  Synopsis=> This test runs optics lpmode link stress test.
    [Tags]  META_STRESS_SPEC_TCG2_20_Optics_Lpmode_Link_Stress_Test  SPEC_20  meta_stress  w400
    Log Info  ===== Start of META_STRESS_SPEC_TCG2_20_Optics_Lpmode_Link_Stress_Test =====
    #Set Testcase Timeout  ${Timeout8000}
    Critical Step  1  switch to centos diag tool
    Step  1  check qsfp on or off test
    Step  2  init sdk from remote shell
    FOR    ${INDEX}    IN RANGE    1    ${MaxLoopNum}
        Print Loop Info  ${INDEX}   ${MaxRepeatCount2}
        set auto load script stress loop time  ${StressLoopTime21600}
        Step  3  init sdk and low power mode  type=on
        Step  4  init sdk and low power mode  type=off
        Step  5  check sdk traffic test
    END
    Log Info  ===== End of testCase META_STRESS_SPEC_TCG2_20_Optics_Lpmode_Link_Stress_Test =====
    [Teardown]  exit sdk env test

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
    [Arguments]    ${CUR_INDEX}    ${LOOP_CNT}
    Log Info  ********************************************************
    Log Info  *** Test Command Loop \#: ${CUR_INDEX} / ${LOOP_CNT} ***
    Log Info  ********************************************************

Print Repeat Info
    [Arguments]    ${CUR_LOOP}    ${MAX_LOOP}
    Log Info  ************************************************************
    Log Info  *** Test Repeat Loop \#: ${CUR_LOOP} / ${MAX_LOOP} ***
    Log Info  ************************************************************


