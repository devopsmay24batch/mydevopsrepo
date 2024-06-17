##############################################################################
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
Variables         MoonstoneOnieVariable.py

Library          ../../../common/commonlib/CommonLib.py
Library          ../MOONSTONECommonLib.py
Library           MoonstoneOnieLib.py
Library           bios_menu_lib.py


Resource          MoonstoneOnieKeywords.robot
Resource          CommonResource.robot

Suite Setup       Onie Connect Device
Suite Teardown    Onie Disconnect Device

*** Variables ***

*** Test Cases ***

MOONSTONE_ONIE_TC_02_Confirm_ONIE_Version
    [Documentation]  This test checks the ONIE version
    [Tags]  common  MOONSTONE_ONIE_TC_02_Confirm_ONIE_Version  ONIE
    [Timeout]  20 min 00 seconds
    Step  1  ONIE Boot Log Version


MOONSTONE_ONIE_TC_05_ONIE_Update_via_Static_IP+TFTP
    [Documentation]  This test checks the Installing ONIE via Static IP+TFTP
    [Tags]  common  MOONSTONE_ONIE_TC_05_ONIE_Update_via_Static_IP+TFTP  smoke  ONIE 
    [Timeout]  20 min 00 seconds
    Step  1  Switch_ONIE_Mode  ${ONIE_UPDATE_MODE}
    Step  2  Set Onie Static IP  eth0  ${static_ip}   
    Step  3  Update Onie  ${version}  ${PROTOCOL_TFTP}
    Step  4  get Onie Version


MOONSTONE_ONIE_TC_06_ONIE_Update_via_DHCP_IP+TFTP
    [Documentation]  This test checks the Installing ONIE via DHCP IP+TFTP
    [Tags]  common  MOONSTONE_ONIE_TC_06_ONIE_Update_via_DHCP_IP+TFTP  ONIE
    [Timeout]  20 min 00 seconds
    Step  1  Switch_ONIE_Mode  ${ONIE_UPDATE_MODE}
    Step  2  Check Onie dhcp IP  
    Step  3  Update Onie  ${version}  ${PROTOCOL_TFTP}
    Step  4  get Onie Version

MOONSTONE_ONIE_TC_07_ONIE_Update_via_HTTP
    [Documentation]  This test checks the Installing ONIE via HTTP
    [Tags]  common  MOONSTONE_ONIE_TC_07_ONIE_Update_via_HTTP  smoke  ONIE
    [Timeout]  20 min 00 seconds
    Step  1  Switch_ONIE_Mode  ${ONIE_UPDATE_MODE}
    Step  2  Update Onie  ${version}  ${PROTOCOL_HTTP}
    Step  3  get Onie Version

MOONSTONE_ONIE_TC_09_Install_OS_via_Static_IP+TFTP
    [Documentation]  This test checks the Installing ONL via Static IP+TFTP
    [Tags]  common  MOONSTONE_ONIE_TC_09_Install_OS_via_Static_IP+TFTP  smoke  ONIE 
    [Timeout]  20 min 00 seconds
    Step  1  Switch_ONIE_Mode  ${ONIE_INSTALL_MODE}
    Step  2  Set Onie Static IP  eth0  ${static_ip}
    Step  3  Install diagos  ${version}  ${PROTOCOL_TFTP}
    Step  4  get onl version 

MOONSTONE_ONIE_TC_10_Install_OS_via_DHCP_IP+TFTP
    [Documentation]  This test checks the Installing ONL via Dhcp IP+TFTP
    [Tags]  common  MOONSTONE_ONIE_TC_10_Install_OS_via_DHCP_IP+TFTP  ONIE
    [Timeout]  20 min 00 seconds
    Step  1  Switch_ONIE_Mode  ${ONIE_INSTALL_MODE}
    Step  2  check onie dhcp IP
    Step  3  Install diagos  ${version}  ${PROTOCOL_TFTP}
    Step  4  get onl version


MOONSTONE_ONIE_TC_11_Install_OS_via_Static_HTTP
    [Documentation]  This test checks the Installing ONL via Static HTTP
    [Tags]  common  MOONSTONE_ONIE_TC_11_Install_OS_via_Static_HTTP  smoke  ONIE  
    [Timeout]  20 min 00 seconds
    Step  1  Switch_ONIE_Mode  ${ONIE_INSTALL_MODE}
    Step  2  Install diagos  ${version}  ${PROTOCOL_HTTP}
    Step  3  get onl version


MOONSTONE_ONIE_TC_13_Uninstall_OS
    [Documentation]  This test checks the uninstall of NOS
    [Tags]  common  MOONSTONE_ONIE_TC_13_Uninstall_OS  ONIE  
    [Timeout]  20 min 00 seconds
    Step  1  Switch_ONIE_Mode  ${ONIE_UNINSTALL_MODE}
    Step  2  Install diagos  ${version}  ${PROTOCOL_TFTP}
    Step  3  get onl version

MOONSTONE_ONIE_TC_14_Install_and_Uninstall_OS
    [Documentation]  This test checks the install and uninstall of NOS
    [Tags]  common  MOONSTONE_ONIE_TC_14_Install_and_Uninstall_OS  ONIE
    [Timeout]  20 min 00 seconds
    FOR  ${CYCLE}  IN RANGE  0  2	
    Step  1  Switch_ONIE_Mode  ${ONIE_UNINSTALL_MODE}
    Step  2  Install diagos  ${version}  ${PROTOCOL_TFTP}
    Step  3  get onl version
    END
 
MOONSTONE_ONIE_TC_15_ONIE_Rescue_Mode
    [Documentation]  This test checks entering onie rescue mode 
    [Tags]  common  MOONSTONE_ONIE_TC_15_ONIE_Rescue_Mode  ONIE 
    [Timeout]  20 min 00 seconds
    Step  1  Switch_ONIE_Mode  ${ONIE_RESCUE_MODE}
    Step  2  get onie version

#not to run until the onie i2set feature is given
MOONSTONE_ONIE_TC_16_Burn_Sys_eeprom
    [Documentation]  This test checks eeprom write operation
    [Tags]  common  MOONSTONE_ONIE_TC_16_Burn_Sys_eeprom  ONIE 
    [Timeout]  20 min 00 seconds
    Step  1  Switch_ONIE_Mode  ${ONIE_INSTALL_MODE}
    Step  2  disable write protect
    Step  3  burn eeprom
    Step  4  enable write protect

MOONSTONE_ONIE_TC_17_Confirm_Sys_eeprom
    [Documentation]  This test checks eeprom read operation
    [Tags]  common  MOONSTONE_ONIE_TC_17_Confirm_Sys_eeprom  ONIE 
    [Timeout]  20 min 00 seconds
    Step  1  Switch_ONIE_Mode  ${ONIE_INSTALL_MODE}
    Step  2  read eeprom
 
MOONSTONE_ONIE_TC_19_Run_ONIE_for_Long_Time
    [Documentation]  This test checks onie stability
    [Tags]  common  MOONSTONE_ONIE_TC_19_Run_ONIE_for_Long_Time  ONIE
    [Timeout]  20 min 00 seconds
    Step  1  Stability Onie Run  
    


*** Keywords ***
Onie Connect Device
    OnieConnect

Onie Disconnect Device
    OnieDisconnect
