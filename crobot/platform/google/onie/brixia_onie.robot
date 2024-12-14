###############################################################################
# LEGALESE:   "Copyright (C) 2019-2021, Celestica Corp. All rights reserved." #
#                                                                             #
# This source code is confidential, proprietary, and contains trade           #
# secrets that are the sole property of Celestica Corp.                       #
# Copy and/or distribution of this source code or disassembly or reverse      #
# engineering of the resultant object code are strictly forbidden without     #
# the written consent of Celestica Corp.                                      #
#                                                                             #
###############################################################################

*** Settings ***
Documentation       This Suite will validate all Onie functions:

Variables         Const.py
Variables         GoogleOnieVariable.py

Library          ../../../common/commonlib/CommonLib.py
Library          ../GoogleCommonLib.py
Library           GoogleOnieLib.py

Resource          GoogleOnieKeywords.robot

Suite Setup       Onie Connect Device
Suite Teardown    Onie Disconnect Device

*** Variables ***

*** Test Cases ***
ONIE_TC_001_xxxx
    [Documentation]  This test checks onie info
    [Tags]  common  ONIE_TC_001_xxxx  brixia
    [Timeout]  20 min 00 seconds
    [Setup]  xxxx
    Step  1  Check onie info
    Step  2  xxxx
    [Teardown]  xxxx

BRIXIA_ONIE_TC_01_ONIE_install_by_pxeboot_Test
    [Documentation]  This test checks ONIE System Information
    [Tags]   BRIXIA_ONIE_TC_01_ONIE_install_by_pxeboot_Test   brixia  test1
    [Setup]   boot into pxeboot
    Step  1  boot into embed
    Step  2  Boot to Onie rescue mode
    Step  3  test onie    ${sysinfo}   ${sysinfo_version}
    Step  4  boot into pxeboot
    Step  5  boot into shell
    Step  6  Boot to Onie rescue mode
    Step  7  check system information    ${sysinfo}   ${sysinfo_version}




BRIXIA_ONIE_TC_02_OS_INSTALL_VIA_DHCP_IP_HTTP
    [Documentation]  This test checks Install sonic via http
    [Tags]     BRIXIA_ONIE_TC_02_OS_INSTALL_VIA_DHCP_IP_HTTP   onie  test2
    [Setup]   boot into pxeboot
    Step  1   boot to onie rescue mode
    Step  2   check onie auto install  yes


BRIXIA_ONIE_TC_03_OS_INSTALL_VIA_DHCP_IP_HTTP_1
    [Documentation]  This test checks Install sonic via http
    [Tags]     BRIXIA_ONIE_TC_03_OS_INSTALL_VIA_DHCP_IP_HTTP_1   onie  test3
    [Setup]   boot into pxeboot
    Step  1   boot to onie rescue mode
    Step  2   check onie auto install


BRIXIA_ONIE_TC_04_OS_INSTALL_VIA_DHCP_IP_HTTP_2
    [Documentation]  This test checks Install sonic via http
    [Tags]     BRIXIA_ONIE_TC_03_OS_INSTALL_VIA_DHCP_IP_HTTP_2   onie  test4
    [Setup]   boot into pxeboot
    Step  1   boot to onie rescue mode
    Step  2   check onie http


BRIXIA_ONIE_TC_16_ONIE_IDLE_TEST
    [Documentation]   This tests check onie behaviour when left idle
    [Tags]  BRIXIA_ONIE_TC_16_ONIE_IDLE_TEST  onie  test16
    [Setup]  boot into pxeboot
    Step  1  check onie idle



BRIXIA_ONIE_TC_12_ONIE_System_Information
    [Documentation]  This test checks ONIE System Information
    [Tags]   BRIXIA_ONIE_TC_12_ONIE_System_Information   brixia  test12
    [Setup]   boot into pxeboot
    Step   1   Boot to Onie rescue mode
    Step   2   check system information    ${sysinfo}   ${sysinfo_version}


BRIXIA_ONIE_TC_09_RESCUE_MODE_BOOT_TEST
    [Documentation]  This tests checks operation in onie rescue mode
    [Tags]   BRIXIA_ONIE_TC_09_RESCUE_MODE_BOOT_TEST  onie  test9
    ${ip} =  get ip address from config  PC
    [Setup]  boot into pxeboot
    Step  1  Boot to Onie rescue mode
    Step  2  check new operation
    Step  3  exec_ping  DUT  ipAddress=${ip}  count=3
    Step  4  boot to sonic



BRIXIA_ONIE_TC_10_UNINSTALL_OS
     [Documentation]  This test checks Uninstall Sonic OS
     [Tags]  BRIXIA_ONIE_TC_10_UNINSTALL_OS  onie  test10
     [Setup]  boot into pxeboot
     Step  1  boot to rescue onie mode
     Step  2  check onie uninstall




BRIXIA_ONIE_TC_11_Install_and_Uninstall_Sonic_OS_Repeatedly
    [Documentation]  This test checks Install and Uninstall Sonic OS Repeatedly
    [Tags]    BRIXIA_ONIE_TC_11_Install_and_Uninstall_Sonic_OS_Repeatedly   brixia  test11
    ${Current_Loop}  Evaluate  100-1
    FOR    ${INDEX}    IN RANGE    1   3

       Step  0   boot into pxeboot
       Step  1   Boot to rescue onie mode
       Step  2   check onie uninstall
       Step  3   boot into pxeboot
       Step  4   boot to onie rescue mode
       Step  5   check onie http
    END


BRIXIA_ONIE_TC_14_ONIE_REBOOT_MULTITIMES__TEST
    [Documentation]  This test checkS onie reboot multiple times
    [Tags]    BRIXIA_ONIE_TC_14_ONIE_REBOOT_MULTITIMES__TEST   brixia  test14
    [Setup]  boot into pxeboot
    Step  1  boot to onie rescue mode
    FOR    ${INDEX}    IN RANGE    1   11
        Step  2   check reboot onie
    END
    Step  3  boot to sonic
BRIXIA_ONIE_TC_05_OS_Install_Via_DHCP_IP+HTTP_3
     [Documentation]   This tests check onie behaviour when left idle
     [Tags]  BRIXIA_ONIE_TC_05_OS_Install_Via_DHCP_IP+HTTP_3   onie  test5
     [Setup]  boot into pxeboot
     Step  1  boot into auto rescue

BRIXIA_ONIE_TC_06_OS_Install_Via_DHCP_IP+HTTP_4
     [Documentation]   This tests check onie behaviour when left idle
     [Tags]  BRIXIA_ONIE_TC_06_OS_Install_Via_DHCP_IP+HTTP_4   onie  test6
     [Setup]  boot into pxeboot
     Step  1  boot into rescue mode
BRIXIA_ONIE_TC_07_ONIE_Update_Via_DHCP_IP+TFTP
    [Documentation]   This test upgrade the onie version
    [Tags]  BRIXIA_ONIE_TC_07_ONIE_Update_Via_DHCP_IP+TFTP   onie  test7
    [Setup]  boot into pxeboot
    Step  1  boot into rescue version

BRIXIA_ONIE_TC_08_ONIE_Update_Via_DHCP_IP+HTTP
    [Documentation]   This test upgrade the onie version
    [Tags]  BRIXIA_ONIE_TC_08_ONIE_Update_Via_DHCP_IP+HTTP   onie  test8
    [Setup]  boot into pxeboot
    Step  1  boot into rescue version



*** Keywords ***
Onie Connect Device
    OnieConnect

Onie Disconnect Device
    OnieDisconnect
