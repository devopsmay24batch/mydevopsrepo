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
Documentation       Tests to verify Onie functions described in the Onie function SPEC for the project Midstone100X

Variables         midstone100X_variable.py
Library           midstone100X_onielib.py
#Library           OnieLib.py
Library           ../ali/AliCommonLib.py
Library           ../WhiteboxLibAdapter.py
Library           CommonLib.py

Resource          CommonKeywords.resource

#Suite Setup       Onie Connect Device
#Suite Teardown    Onie Disconnect Device

** Variables ***

*** Test Cases ***
ONIE_Booting_Mode_Check
    [Documentation]  Checks each supportted ONIE mode
    [Tags]  ONIE_Booting_Mode_Check  TC_003  Midstone100X
    [Setup]     OS Connect Device
    independent_step  1  SetRootHostName
    independent_step  2  SwitchOnieModeAndCheckOutput  installer
    independent_step  3  SwitchOnieModeAndCheckOutput  update
    independent_step  4  SwitchOnieModeAndCheckOutput  rescue
    independent_step  5  SwitchOnieModeAndCheckOutput  uninstall
    independent_step  6  Onie Disconnect Device
    [Teardown]  Run Keyword If Test Failed
    ...  Run Keywords
    ...  Onie Connect Device  AND
    ...  SwitchOnieModeAndCheckOutput  uninstall  AND
    ...  Onie Disconnect Device


Install_Sonic_via_Static_IP+TFTP
    [Documentation]  This test checks the Installing Sonic via TFTP
    [Tags]  Install_Sonic_via_Static_IP+TFTP  TC_005  Midstone100X
    [Setup]     Onie Connect Device
    independent_step  1  RebootToOnieMode  ${ONIE_INSTALL_MODE}
    independent_step  2  SetOnieStaticIp  eth0  ${set_onie_static_ip}
    independent_step  3  InstallDiagOS  ${PROTOCOL_TFTP}
    independent_step  4  SetRootHostName
    independent_step  5  SwitchOnieModeAndCheckOutput  installer
    independent_step  6  SetWait  60
    independent_step  7  exec_cmd  reboot
    independent_step  8  connect  sonic  60  180
    independent_step  9  Onie Disconnect Device
    [Teardown]  Run Keyword If Test Failed
    ...  Run Keywords
    ...  Onie Connect Device  AND
    ...  SwitchOnieModeAndCheckOutput  uninstall  AND
    ...  InstallSonicLocal  AND
    ...  Onie Disconnect Device


Install_Sonic_via_Static_IP+HTTP
    [Documentation]  This test checks the Installing Sonic via HTTP
    [Tags]  Install_Sonic_via_Static_IP+HTTP  TC_006  Midstone100X
    [Setup]     OS Connect Device
    independent_step  1  RebootToOnieMode  ${ONIE_INSTALL_MODE}
    independent_step  2  SetOnieStaticIp  eth0  ${set_onie_static_ip}
    independent_step  3  InstallDiagOS  ${PROTOCOL_HTTP}
    independent_step  4  SetRootHostName
    independent_step  5  SwitchOnieModeAndCheckOutput  installer
    independent_step  6  SetWait  60
    independent_step  7  exec_cmd  reboot
    independent_step  8  connect  sonic  60  180
    independent_step  9  Onie Disconnect Device
    [Teardown]  Run Keyword If Test Failed
    ...  Run Keywords
    ...  OS Connect Device  AND
    ...  RebootToOnieMode  ${ONIE_INSTALL_MODE}  AND
    ...  InstallSonicLocal  AND
    ...  Onie Disconnect Device


Install_Sonic_via_DHCP+TFTP
    [Documentation]  This test checks the Installing ONIE via TFTP
    [Tags]  Install_Sonic_via_DHCP+TFTP  TC_007  Midstone100X
    [Setup]     OS Connect Device
    independent_step  1  RebootToOnieMode  ${ONIE_INSTALL_MODE}
    independent_step  2  InstallDiagOS  ${PROTOCOL_TFTP}
    independent_step  3  SetRootHostName
    independent_step  4  SwitchOnieModeAndCheckOutput  installer
    independent_step  5  SetWait  60
    independent_step  6  exec_cmd  reboot
    independent_step  7  connect  sonic  60  180
    independent_step  8  Onie Disconnect Device
    [Teardown]  Run Keyword If Test Failed
    ...  Run Keywords
    ...  OS Connect Device  AND
    ...  RebootToOnieMode  ${ONIE_INSTALL_MODE}  AND
    ...  InstallSonicLocal  AND
    ...  Onie Disconnect Device


Update_ONIE_via_Static_IP+TFTP
    [Documentation]  This test checks the updating ONIE via Static IP+TFTP
    [Tags]  Update_ONIE_via_Static_IP+TFTP  TC_011  Midstone100X
    [Setup]  OS Connect Device
    independent_step  1  RebootToOnieMode  ${ONIE_UPDATE_MODE}
    independent_step  2  SetOnieStaticIp  eth0  ${set_onie_static_ip}
    independent_step  3  UpdateOnie  new  ${PROTOCOL_TFTP}
    independent_step  4  RebootToOnieMode  ${ONIE_UPDATE_MODE}
    independent_step  5  SetOnieStaticIp  eth0  ${set_onie_static_ip}
    ${onie_version_now}  GetOnieVersion
    ${onie_version_1}  UpdateOnie  old  ${PROTOCOL_TFTP}
    independent_step  6  CheckInfoEqual  ${onie_version_now}  ${onie_version_1}  False
    independent_step  7  RebootToOnieMode  ${ONIE_UPDATE_MODE}
    independent_step  8  SetOnieStaticIp  eth0  ${set_onie_static_ip}
    ${onie_version_1_1}  GetOnieVersion
    independent_step  9  CheckInfoEqual  ${onie_version_1_1}  ${onie_version_1}
    ${onie_version_2}  UpdateOnie  new  ${PROTOCOL_TFTP}
    independent_step  10  CheckInfoEqual  ${onie_version_1}  ${onie_version_2}  False
    independent_step  11  Onie Disconnect Device
    [Teardown]  Run Keyword If Test Failed
    ...  Run Keywords
    ...  Onie Connect Device  AND
    ...  RebootToOnieMode  ${ONIE_UPDATE_MODE}  AND
    ...  Onie Disconnect Device


Update_ONIE_via_Static_IP+HTTP
    [Documentation]  This test checks the updating ONIE via Static IP+HTTP
    [Tags]  Update_ONIE_via_Static_IP+HTTP  TC_012  Midstone100X
    [Setup]  Onie Connect Device
    independent_step  1  RebootToOnieMode  ${ONIE_UPDATE_MODE}
    independent_step  2  SetOnieStaticIp  eth0  ${set_onie_static_ip}
    independent_step  3  UpdateOnie  new  ${PROTOCOL_HTTP}
    independent_step  4  RebootToOnieMode  ${ONIE_UPDATE_MODE}
    independent_step  5  SetOnieStaticIp  eth0  ${set_onie_static_ip}
    ${onie_version_now}   GetOnieVersion
    ${onie_version_1}  UpdateOnie  old  ${PROTOCOL_HTTP}
    independent_step  6  CheckInfoEqual  ${onie_version_now}  ${onie_version_1}  False
    independent_step  7  RebootToOnieMode  ${ONIE_UPDATE_MODE}
    independent_step  8  SetOnieStaticIp  eth0  ${set_onie_static_ip}
    ${onie_version_1_1}  GetOnieVersion
    independent_step  9  CheckInfoEqual  ${onie_version_1_1}  ${onie_version_1}
    ${onie_version_2}  UpdateOnie  new  ${PROTOCOL_HTTP}
    independent_step  10  CheckInfoEqual  ${onie_version_1}  ${onie_version_2}  False
    independent_step  11  Onie Disconnect Device
    [Teardown]  Run Keyword If Test Failed
    ...  Run Keywords
    ...  Onie Connect Device  AND
    ...  RebootToOnieMode  ${ONIE_UPDATE_MODE}  AND
    ...  Onie Disconnect Device


Update_ONIE_via_DHCP+TFTP
    [Documentation]  This test checks the updating ONIE via DHCP+TFTP
    [Tags]  Update_ONIE_via_DHCP+TFTP  TC_013  Midstone100X
    [Setup]  Onie Connect Device
    independent_step  1  RebootToOnieMode  ${ONIE_UPDATE_MODE}
    independent_step  2  UpdateOnie  new  ${PROTOCOL_TFTP}
    independent_step  3  RebootToOnieMode  ${ONIE_UPDATE_MODE}
    ${onie_version_now}   GetOnieVersion
    ${onie_version_1}  UpdateOnie  old  ${PROTOCOL_TFTP}
    independent_step  4  CheckInfoEqual  ${onie_version_now}  ${onie_version_1}  False
    independent_step  5  RebootToOnieMode  ${ONIE_UPDATE_MODE}
    ${onie_version_1_1}  GetOnieVersion
    independent_step  6  CheckInfoEqual  ${onie_version_1_1}  ${onie_version_1}
    ${onie_version_2}  UpdateOnie  new  ${PROTOCOL_TFTP}
    independent_step  7  CheckInfoEqual  ${onie_version_1}  ${onie_version_2}  False
    independent_step  8  Onie Disconnect Device
    [Teardown]  Run Keyword If Test Failed
    ...  Run Keywords
    ...  Onie Connect Device  AND
    ...  RebootToOnieMode  ${ONIE_UPDATE_MODE}  AND
    ...  Onie Disconnect Device


Update_ONIE_via_DHCP+HTTP
    [Documentation]  This test checks the updating ONIE via DHCP+HTTP
    [Tags]  Update_ONIE_via_DHCP+HTTP  TC_014  Midstone100X
    [Setup]  Onie Connect Device
    independent_step  1  RebootToOnieMode  ${ONIE_UPDATE_MODE}
    independent_step  2  UpdateOnie  new  ${PROTOCOL_HTTP}
    independent_step  3  RebootToOnieMode  ${ONIE_UPDATE_MODE}
    ${onie_version_now}   GetOnieVersion
    ${onie_version_1}  UpdateOnie  old  ${PROTOCOL_HTTP}
    independent_step  4  CheckInfoEqual  ${onie_version_now}  ${onie_version_1}  False
    independent_step  5  RebootToOnieMode  ${ONIE_UPDATE_MODE}
    ${onie_version_1_1}  GetOnieVersion
    independent_step  6  CheckInfoEqual  ${onie_version_1_1}  ${onie_version_1}
    ${onie_version_2}  UpdateOnie  new  ${PROTOCOL_HTTP}
    independent_step  7  CheckInfoEqual  ${onie_version_1}  ${onie_version_2}  False
    independent_step  8  Onie Disconnect Device
    [Teardown]  Run Keyword If Test Failed
    ...  Run Keywords
    ...  Onie Connect Device  AND
    ...  RebootToOnieMode  ${ONIE_UPDATE_MODE}  AND
    ...  Onie Disconnect Device


ONIE_Rescue_Mode
    [Documentation]  TC_014
    [Tags]  ONIE_Rescue_Mode  TC_014  Midstone100X
    [Setup]  Onie Connect Device
    independent_step  1  SwitchOnieModeAndCheckOutput  rescue
    independent_step  2  ShouldHaveNoDiscoveryMessage
    independent_step  3  get_dhcp_ip_address  DUT  eth0  ONIE
    ${init_value}  GetOnieTlvValue
    ${init_value_code}  GetOnieTlvValue  True
    independent_step  4  SetOnieTlvValue  decide=False
    independent_step  5  SetTlvWriteProtectionClose
    independent_step  6  SetOnieTlvValue
    ${error_value}  GetOnieTlvValue
    independent_step  6  CheckInfoEqual  ${error_value}  ${init_value}  False
    independent_step  7  SetPduStatusConnectOs  sonic  reboot  ${pdu_port}  60
    independent_step  8  RebootToOnieMode  ${ONIE_RESCUE_MODE}
    ${error_value_ac}  GetOnieTlvValue
    independent_step  9  CheckInfoEqual  ${error_value}  ${error_value_ac}
    independent_step  10  SetTlvWriteProtectionClose
    independent_step  11  SetOnieTlvValue  ${init_value_code}
    independent_step  12  SetPduStatusConnectOs  sonic  reboot  ${pdu_port}  60
    independent_step  13  RebootToOnieMode  ${ONIE_RESCUE_MODE}
    independent_step  14  Onie Disconnect Device
    [Teardown]  Run Keyword If Test Failed
    ...  Run Keywords
    ...  Onie Connect Device  AND
    ...  RebootToOnieMode  ${ONIE_RESCUE_MODE}  AND
    ...  SetTlvWriteProtectionClose  AND
    ...  SetOnieTlvValue  ${init_value_code}  AND
    ...  RebootToOnieMode  ${ONIE_RESCUE_MODE}  AND
    ...  Onie Disconnect Device


Update_MAC_Address_in_ONIE
    [Documentation]  space
    [Tags]  Update_MAC_Address_in_ONIE  TC_018  Midstone100X
    [Setup]  Onie Connect Device
    independent_step  1  RebootToOnieMode  ${ONIE_UPDATE_MODE}
    ${mac} =  get_mac_address  DUT  eth0
    independent_step  2  execute_command  onie-syseeprom -s 0x24=${test_mac1}
    independent_step  3  SetWait  10
    independent_step  4  SetPduStatusConnectOs  sonic  reboot  ${pdu_port}  60
    independent_step  5  RebootToOnieMode  ${ONIE_RESCUE_MODE}
    independent_step  6  VerifyMacAddress  ${test_mac1}
    [Teardown]  Run Keywords
    ...  RestoreMacAddress  ${mac}  AND
    ...  ExeWithoutRule  reboot  AND
    ...  connect  sonic  120  180  AND
    ...  Onie Disconnect Device


Stress_install_uninstall_sonic
    [Documentation]  Repeat uninstall and install sonic
    [Tags]  Stress_install_uninstall_sonic  Midstone100X
    [Setup]  OS Connect Device
    FOR  ${index}  IN RANGE  0  ${loop_num}
        independent_step  1  uninstallOS
        independent_step  2  InstallSonicLocal
    END
    independent_step  3  Onie Disconnect Device
    [Teardown]  Run Keyword If Test Failed
    ...  Run Keywords
    ...  Onie Connect Device  AND
    ...  RebootToOnieMode  ${ONIE_INSTALL_MODE}  AND
    ...  InstallSonicLocal  AND
    ...  Onie Disconnect Device


*** Keywords ***
Onie Connect Device
    OnieConnect

Onie Disconnect Device
    OSDisconnect

OS Connect Device
    OSConnect