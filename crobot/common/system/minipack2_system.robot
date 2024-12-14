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
# Script       : minipack2_system.robot                                                                               #
# Date         : Aug 07, 2020                                                                                         #
# Author       : TK                                                                                                   #
# Description  : This script will run all minipack2 system stress tests.                                              #
#                                                                                                                     #
# Script Revision Details:                                                                                            #

#######################################################################################################################

*** Settings ***
Documentation     This suite will perform all minipack2 system stress tests.

Library           Keyword_Resource.py
Resource          Resource.robot
Library           DiagLibAdapter.py

Suite Setup       Diag Connect Device
Suite Teardown    Diag Disconnect Device


*** Test Cases ***
##### Start - Facebook Minipack2 System Stress Test Case Group 1 #####
FB_SYS_COM_TCG1-00_Precondition_Check_Test
    [Documentation]  Synopsis=> This test executes precondition checks before starting any stress test.
    [Tags]  FB_SYS_COM_TCG1-00_Precondition_Check_Test  minipack2
    [Setup]  set verbose level
    Log Info  ===== Start of FB_SYS_COM_TCG1-00_Precondition_Check_Test =====
    Set Testcase Timeout  ${Timeout1800}
    #minipack2 check all system sw fw versions
    #check usb disk presence
    #check cpu and openbmc ipv6 interface
    switch to centos diag tool
    #startup default port group
    check psu connection
    check emmc available space
    remove all cpu logs
	check all cpu test tools and fw version
    check all bmc test directories and fw version
    Log Info  ===== End of FB_SYS_COM_TCG1-00_Precondition_Check_Test =====


FB_SYS_COM_TCG1-01_Sensor_Reading_Stress_High_Loading
    [Documentation]  Synopsis=> This test checks the sensor readings under cpu high loading condition.
    [Tags]  FB_SYS_COM_TCG1-01_Sensor_Reading_Stress_High_Loading  minipack2
    Log Info  ===== Start of testCase FB_SYS_COM_TCG1-01_Sensor_Reading_Stress_High_Loading =====
    Set Testcase Timeout  ${Timeout3600}
    #Set Global Variable     ${MaxRepeatCount5}       1
    #Set Global Variable     ${StressLoopTime1800}    600
    set sensor reading stress cycles  ${MaxRepeatCount5}
    set auto load script stress loop time  ${StressLoopTime1800}
	#switch to centos diag tool
	#startup default port group
    minipack2 run sensor reading high loading stress test
    Log Info  ===== Start of testCase FB_SYS_COM_TCG1-01_Sensor_Reading_Stress_High_Loading =====


FB_SYS_COM_TCG1-02_FPGA_PCIE_Bus_Stress_Test
    [Documentation]  Synopsis=> This test checks the function of FPGA PCIE bus.
    [Tags]  FB_SYS_COM_TCG1-02_FPGA_PCIE_Bus_Stress_Test  common  minipack2
    Log Info  ===== Start of testCase FB_SYS_COM_TCG1-02_FPGA_PCIE_Bus_Stress_Test =====
    [Setup]  ssh login bmc
    Set Testcase Timeout  ${Timeout3600}
    #Set Global Variable     ${StressLoopTime1800}    60
    set fpga stress loop time  ${StressLoopTime1800}
    switch to centos diag tool
    run fpga pcie bus stress test
    [Teardown]  ssh disconnect
    Log Info  ===== End of testCase FB_SYS_COM_TCG1-02_FPGA_PCIE_Bus_Stress_Test =====


FB_SYS_COM_TCG1-03_OpenBMC_Utility_Stability_Test
    [Documentation]  Synopsis=> This test checks the stability of openbmc utility.
    [Tags]  FB_SYS_COM_TCG1-03_OpenBMC_Utility_Stability_Test  minipack2
    Log Info  ===== Start of testCase FB_SYS_COM_TCG1-03_OpenBMC_Utility_Stability_Test =====
    Set Testcase Timeout  ${Timeout3600}
    #Set Global Variable     ${MaxRepeatCount200}    1
    set openbmc utility test cycles    ${MaxRepeatCount200}
    switch to openbmc check tool
    minipack2 run openbmc utility stability test
    Log Info  ===== End of testCase FB_SYS_COM_TCG1-03_OpenBMC_Utility_Stability_Test =====


FB_SYS_COM_TCG1-04_IPMI_Interface_Stress_Test
    [Documentation]  Synopsis=> This test checks the function of IPMI interface.
    [Tags]  FB_SYS_COM_TCG1-04_IPMI_Interface_Stress_Test  minipack2
    Log Info  ===== Start of testCase FB_SYS_COM_TCG1-04_IPMI_Interface_Stress_Test =====
    Set Testcase Timeout  ${Timeout1800}
    #Set Global Variable     ${MaxRepeatCount100}    1
    set ipmi test cycles    ${MaxRepeatCount100}
    switch to centos diag tool
    minipack2 run ipmi command stress test
    Log Info  ===== End of testCase FB_SYS_COM_TCG1-04_IPMI_Interface_Stress_Test =====


FB_SYS_COM_TCG1-05_COMe_NVMe_SSD_RW_Stress_Test
    [Documentation]  Synopsis=> This test checks the function of NVMe SSD RW access.
    [Tags]  FB_SYS_COM_TCG1-05_COMe_NVMe_SSD_RW_Stress_Test  common  minipack2
    Log Info  ===== Start of testCase FB_SYS_COM_TCG1-05_COMe_NVMe_SSD_RW_Stress_Test =====
    Set Testcase Timeout  ${Timeout3600}
    #Set Global Variable     ${StressLoopTime1800}   60
    set nvme stress loop time  ${StressLoopTime1800}
    switch to centos diag tool
    run nvme access stress test
    Log Info  ===== End of testCase FB_SYS_COM_TCG1-05_COMe_NVMe_SSD_RW_Stress_Test =====


# Temporary disabled, waiting for minipack2 system stress test specifications to be updated by SVT.
#FB_SYS_COM_TCG1-06_Loopback_EEPROM_Access_Stress_Test
#    [Documentation]  Synopsis=> This test checks the function of EEPROM access.
#    [Tags]  FB_SYS_COM_TCG1-06_Loopback_EEPROM_Access_Stress_Test  minipack2
#    Log Info  ===== Start of testCase FB_SYS_COM_TCG1-06_Loopback_EEPROM_Access_Stress_Test =====
#    Set Testcase Timeout  ${Timeout3600}
#    #Set Global Variable     ${StressLoopTime1800}    60
#    set eeprom stress loop time  ${StressLoopTime1800}
#    switch to centos diag tool
#    minipack2 run eeprom access stress test
#    Log Info  ===== End of testCase FB_SYS_COM_TCG1-06_Loopback_EEPROM_Access_Stress_Test =====


FB_SYS_COM_TCG1-07_BMC_And_CPU_OOB_Link_Stress_Test
    [Documentation]  Synopsis=> This test checks the function of BMC and CPU OOB link.
    [Tags]  FB_SYS_COM_TCG1-07_BMC_And_CPU_OOB_Link_Stress_Test  common  minipack2
    Log Info  ===== Start of FB_SYS_COM_TCG1-07_BMC_And_CPU_OOB_Link_Stress_Test =====
    Set Testcase Timeout  ${Timeout3600}
    #Set Global Variable     ${StressLoopTime900}    60
    set bmc cpu link stress loop time  ${StressLoopTime900}
    switch to centos diag tool
    run bmc cpu oob link access stress test
    Log Info  ===== End of testCase FB_SYS_COM_TCG1-07_BMC_And_CPU_OOB_Link_Stress_Test =====


FB_SYS_COM_TCG1-08_BMC_And_CPU_Internal_USB_Network_Stress_Test
    [Documentation]  Synopsis=> This test checks the function of BMC and CPU internal USB network link.
    [Tags]  FB_SYS_COM_TCG1-08_BMC_And_CPU_Internal_USB_Network_Stress_Test  common  minipack2
    Log Info  ===== Start of FB_SYS_COM_TCG1-08_BMC_And_CPU_Internal_USB_Network_Stress_Test =====
    Set Testcase Timeout  ${Timeout3600}
    #Set Global Variable     ${StressLoopTime900}    60
    set bmc cpu link stress loop time  ${StressLoopTime900}
    switch to centos diag tool
    run bmc cpu internal usb network stress test
    Log Info  ===== End of testCase FB_SYS_COM_TCG1-08_BMC_And_CPU_Internal_USB_Network_Stress_Test =====


FB_SYS_COM_TCG1-09_Sensor_Reading_Stress-Idle
    [Documentation]  Synopsis=> This test checks the sensor readings under cpu idle condition.
    [Tags]  FB_SYS_COM_TCG1-09_Sensor_Reading_Stress-Idle  minipack2
    Log Info  ===== Start of testCase FB_SYS_COM_TCG1-09_Sensor_Reading_Stress-Idle =====
    Set Testcase Timeout  ${Timeout3600}
    #Set Global Variable     ${MaxRepeatCount5}       1
    #Set Global Variable     ${StressLoopTime1800}    600
    set sensor reading stress cycles  ${MaxRepeatCount5}
    set auto load script stress loop time  ${StressLoopTime1800}
	#switch to centos diag tool
	#startup default port group
	minipack2_run_sensor_reading_idle_stress_test
    Log Info  ===== Start of testCase FB_SYS_COM_TCG1-09_Sensor_Reading_Stress-Idle =====


FB_SYS_COM_TCG1-10_COMe_Memory_Stress_Test
    [Documentation]  Synopsis=> This test runs the COMe memory stress test.
    [Tags]  FB_SYS_COM_TCG1-10_COMe_Memory_Stress_Test  common  minipack2
    Log Info  ===== Start of testCase FB_SYS_COM_TCG1-10_COMe_Memory_Stress_Test =====
    Set Testcase Timeout  ${Timeout3600}
    #Set Global Variable     ${StressLoopTime900}    60
    set come memory stress loop time  ${StressLoopTime900}
    switch to centos
    run come memory test
    Log Info  ===== End of testCase FB_SYS_COM_TCG1-10_COMe_Memory_Stress_Test =====


FB_SYS_COM_TCG1-11_COMe_CPU_Stress_Test
    [Documentation]  Synopsis=> This test runs the cpu stress test.
    [Tags]  FB_SYS_COM_TCG1-11_COMe_CPU_Stress_Test  common  minipack2
    Log Info  ===== Start of testCase FB_SYS_COM_TCG1-11_COMe_CPU_Stress_Test =====
    Set Testcase Timeout  ${Timeout3600}
    #Set Global Variable     ${StressLoopTime900}    60
    set cpu stress loop time  ${StressLoopTime900}
    switch to centos
    run cpu stress test
    Log Info  ===== End of testCase FB_SYS_COM_TCG1-11_COMe_CPU_Stress_Test =====


FB_SYS_COM_TCG1-12_OpenBMC_Memory_Stress_Test
    [Documentation]  Synopsis=> This test checks the function of openbmc memory.
    [Tags]  FB_SYS_COM_TCG1-12_OpenBMC_Memory_Stress_Test  common  minipack2
    Log Info  ===== Start of FB_SYS_COM_TCG1-12_OpenBMC_Memory_Stress_Test =====
    [Setup]  ssh login bmc
    Set Testcase Timeout  ${Timeout3600}
    #Set Global Variable     ${StressLoopTime1800}    60
    set openbmc memory stress loop time  ${StressLoopTime1800}
    switch to openbmc check tool
    run openbmc memory stress test  100M 2
    [Teardown]  ssh disconnect
    Log Info  ===== End of testCase FB_SYS_COM_TCG1-12_OpenBMC_Memory_Stress_Test =====


FB_SYS_COM_TCG1-13_OpenBMC_I2C_Bus_Scan_Stress_Test
    [Documentation]  Synopsis=> This test checks the function of openbmc i2c scan.
    [Tags]  FB_SYS_COM_TCG1-13_OpenBMC_I2C_Bus_Scan_Stress_Test  minipack2
    Log Info  ===== Start of FB_SYS_COM_TCG1-13_OpenBMC_I2C_Bus_Scan_Stress_Test =====
    Set Testcase Timeout  ${Timeout3600}
    #Set Global Variable     ${StressLoopTime1800}    60
    set i2c scan stress loop time  ${StressLoopTime1800}
    switch to openbmc check tool
    minipack2 run openbmc i2c scan stress test
    Log Info  ===== End of testCase FB_SYS_COM_TCG1-13_OpenBMC_I2C_Bus_Scan_Stress_Test =====


FB_SYS_COM_TCG1-14_TPM_Module_Access_Stress_test
    [Documentation]  Synopsis=> This test checks the function of TPM access.
    [Tags]  FB_SYS_COM_TCG1-14_TPM_Module_Access_Stress_test  minipack2
    Log Info  ===== Start of FB_SYS_COM_TCG1-14_TPM_Module_Access_Stress_test =====
    Set Testcase Timeout  ${Timeout3600}
    #Set Global Variable     ${MaxRepeatCount20}    1
    set tpm access test cycles    ${MaxRepeatCount20}
    switch to centos diag tool
    minipack2 run tpm access stress test
    Log Info  ===== End of testCase FB_SYS_COM_TCG1-14_TPM_Module_Access_Stress_test =====


FB_SYS_COM_TCG1-15_Each_Port_Enable_Disable_Stress_Test
    [Documentation]  Synopsis=> This test runs the ports link stress test for each port.
    [Tags]  FB_SYS_COM_TCG1-15_Each_Port_Enable_Disable_Stress_Test  depend_sdk  minipack2
    Log Info  ===== Start of FB_SYS_COM_TCG1-15_Each_Port_Enable_Disable_Stress_Test =====
    Set Testcase Timeout  ${Timeout1800}
    #Set Global Variable     ${MaxRepeatCount10}    1
    set port enable disable test stress cycles    ${MaxRepeatCount10}
    set port enable disable test stress time    ${StressLoopTime60}
    switch to centos diag tool
    startup default port group
    minipack2 run port enable disable test  False
    Log Info  ===== Enable of FB_SYS_COM_TCG1-15_Each_Port_Enable_Disable_Stress_Test =====


FB_SYS_COM_TCG1-16_SDK_Re-Init_Stress_Test
    [Documentation]  Synopsis=> This test runs the SDK re-init stress test.
    [Tags]  FB_SYS_COM_TCG1-16_SDK_Re-Init_Stress_Test  depend_sdk  minipack2
    Log Info  ===== Start of FB_SYS_COM_TCG1-16_SDK_Re-Init_Stress_Test =====
    Set Testcase Timeout  ${Timeout3600}
    #Set Global Variable     ${MaxRepeatCount10}    1
    set re init test stress cycles    ${MaxRepeatCount10}
    set re init test stress time    ${StressLoopTime60}
    switch to centos
    minipack2 run sdk re init test
    Log Info  ===== End of FB_SYS_COM_TCG1-16_SDK_Re-Init_Stress_Test =====


FB_SYS_COM_TCG1-17_Snake_Traffic_Test
    [Documentation]  Synopsis=> This test runs the snake traffic test.
    [Tags]  FB_SYS_COM_TCG1-17_Snake_Traffic_Test  depend_sdk  minipack2
    Log Info  ===== Start of FB_SYS_COM_TCG1-17_Snake_Traffic_Test =====
    Set Testcase Timeout  ${Timeout3600}
    #Set Global Variable  ${StressLoopTime1800}    300
    set snake traffic test stress time  ${StressLoopTime1800}
    switch to centos
	#startup default port group
    minipack2 run snake traffic test
    Log Info  ===== End of testCase FB_SYS_COM_TCG1-17_Snake_Traffic_Test =====
##### End - Facebook Minipack2 System Stress Test Case Group 1 #####


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
    Log Info  ********************************************************
    Log Info  *** Test Command Loop \#: ${CUR_INDEX} / ${LOOP_CNT} ***
    Log Info  ********************************************************

Print Repeat Info
    [Arguments]    ${CUR_LOOP}    ${MAX_LOOP}
    Log Info  ************************************************************
    Log Info  *** Test Repeat Loop \#: ${CUR_LOOP} / ${MAX_LOOP} ***
    Log Info  ************************************************************


