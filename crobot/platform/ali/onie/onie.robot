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
Documentation       Tests to verify Onie functions described in the Onie function SPEC for the project migaloo  shamu.

Variables         AliOnieVariable.py
Variables         ../AliCommonVariable.py
Variables         Const.py

Library           AliOnieLib.py
Library           OnieLib.py
Library           ../AliCommonLib.py
Library           CommonLib.py

Resource          AliOnieKeywords.resource
Resource          CommonKeywords.resource

Suite Setup       Onie Connect Device
Suite Teardown    Onie Disconnect Device

** Variables ***

*** Variables ***
${LoopCnt}      1
${MAX_LOOP}     3

*** Test Cases ***
# *** comment ***

ALI_ONIE_COMM_TC_010_Update_ONIE_via_SSD
    [Documentation]  This test checks the updating ONIE via DHCP+TFTP
    [Tags]  ALI_ONIE_COMM_TC_010_Update_ONIE_via_SSD  migaloo  shamu
    [Timeout]  60 min 00 seconds
    Step  1  boot Into Onie Update Mode
    Step  2  get dhcp ip address  DUT  eth0  ONIE
    Step  3  prepare onie updater  usb  True
    Step  3  check auto update onie  usb
    [Teardown]  prepare onie updater  usb  False


ALI_ONIE_COMM_TC_003_ONIE_Booting_Mode_Check
    [Documentation]  Checks each supportted ONIE mode
    [Tags]  ALI_ONIE_COMM_TC_003_ONIE_Booting_Mode_Check  migaloo  shamu
    [Timeout]  30 min 00 seconds
    ##  @ISSUE  an unexpected print out will make this case failed:
    #discEXT4-fs (sda3): couldn't mount as ext3 due to feature incompatibilities
    #over: installer mode detected.  Running installer.
    Step  1  switch onie mode and check output  installer
    Step  2  switch onie mode and check output  update
    Step  3  switch onie mode and check output  rescue
#    Step  4  switch onie mode and check output  uninstall   @TEMP_DISABLED, will uninstall diagos

ALI_ONIE_COMM_TC_004_Install_Sonic_via_USB
    [Documentation]  This test checks the Installing ONIE via TFTP
    [Tags]  ALI_ONIE_COMM_TC_004_Install_Sonic_via_USB  migaloo  shamu
    [Timeout]  60 min 00 seconds
    [Setup]  boot Into Onie Install Mode
    Step  1  get dhcp ip address  DUT  eth0  ONIE
    Step  2  prepare os installer  usb  True
    Step  3  check auto install DiagOS  usb
    Step  4  boot Into Onie Install Mode
    Step  5  prepare os installer  usb  False
    Step  6  boot Into DiagOS Mode

ALI_ONIE_COMM_TC_016_Uninstall_Sonic_Test
    [Documentation]  This test checks Uninstall Sonic Test(2 Sonic Installed)
    [Tags]  ALI_ONIE_COMM_TC_016_Uninstall_Sonic_Test  migaloo  shamu
    [Timeout]  60 min 00 seconds
    Step  1  install DiagOs Under Sonic  oldVersion=True
    Step  2  check grub menu  hasTwoSonic=True
    Step  3  check new installed os  oldVersion=True
    Step  4  check original os
    Step  5  reboot To DiagOS   ##come to active os
    Step  6  install DiagOs Under Sonic  oldVersion=False
    Step  7  reboot To DiagOS   ##come to active os
    Step  8  check new installed os  oldVersion=False
    Step  9  uninstall DiagOs Under Sonic  oldVersion=True
    Step  10  check grub menu  hasTwoSonic=False
    Step  11  reboot to onie mode  ${ONIE_INSTALL_MODE}
    Step  12  reboot To DiagOS
    Step  13  uninstall DiagOS Under onie
    [Teardown]  Run Keywords  boot Into Onie install Mode
    ...  AND  install DiagOS  http

ALI_ONIE_COMM_TC_024_Install_Sonic_and_Uninstall_Sonic_Repeatly
    [Tags]     ALI_ONIE_COMM_TC_024_Install_Sonic_and_Uninstall_Sonic_Repeatly  migaloo
    [Timeout]  60 min 00 seconds
    FOR    ${INDEX}    IN RANGE    1    ${MAX_LOOP}
        Step  1  uninstall DiagOS Under onie
        Step  2  install DiagOS  http
    END

ALI_ONIE_COMM_TC_005_Install_Sonic_via_Static_IP+TFTP
    [Documentation]  This test checks the Installing Sonic via TFTP
    [Tags]  ALI_ONIE_COMM_TC_005_Install_Sonic_via_Static_IP+TFTP  migaloo  shamu
    [Timeout]  30 min 00 seconds
    [Setup]  boot Into Onie install Mode
    Step  1  get dhcp ip address  DUT  eth0  ONIE
    Step  2  install DiagOS  tftp
    Step  3  boot Into Onie Install Mode
    Step  4  boot Into DiagOS Mode

ALI_ONIE_COMM_TC_006_Install_Sonic_via_Static_IP+HTTP
    [Documentation]  This test checks the Installing Sonic via HTTP
    [Tags]  ALI_ONIE_COMM_TC_006_Install_Sonic_via_Static_IP+HTTP  migaloo  shamu
    [Timeout]  30 min 00 seconds
    [Setup]  boot Into Onie install Mode
    Step  1  get dhcp ip address  DUT  eth0  ONIE
    Step  2  install DiagOS  http
    Step  3  boot Into Onie Install Mode
    Step  4  boot Into DiagOS Mode

ALI_ONIE_COMM_TC_007_Install_Sonic_via_DHCP+TFTP
    [Documentation]  This test checks the Installing ONIE via TFTP
    [Tags]  ALI_ONIE_COMM_TC_007_Install_Sonic_via_DHCP+TFTP  migaloo  shamu
    [Timeout]  60 min 00 seconds
    [Setup]  prepare os installer  tftp  True
    Step  1  reboot to onie mode  ${ONIE_INSTALL_MODE}
    Step  2  get dhcp ip address  DUT  eth0  ONIE
    Step  3  check auto install DiagOS  tftp
    Step  4  boot Into Onie Install Mode
    Step  5  boot Into DiagOS Mode
    [Teardown]  prepare os installer  tftp  False

#ALI_ONIE_COMM_TC_009_Install_Second_OS_via_ONIE
#    [Documentation]  This test checks the Installing ONIE via TFTP
#    [Tags]  ALI_ONIE_COMM_TC_009_Install_Second_OS_via_ONIE  migaloo  shamu
#    [Timeout]  30 min 00 seconds
#    [Setup]  boot Into Diag OS Mode
#    Step  1  prepare images  DIAGOS
#    Step  2  install DiagOS  under sonic

ALI_ONIE_COMM_TC_011_Update_ONIE_via_Static_IP+TFTP
    [Documentation]  This test checks the updating ONIE via Static IP+TFTP
    [Tags]  ALI_ONIE_COMM_TC_011_Update_ONIE_via_Static_IP+TFTP  migaloo  shamu
    [Timeout]  30 min 00 seconds
    [Setup]  boot Into Onie update Mode
    Step  1  get dhcp ip address  DUT  eth0  ONIE
    Step  2  update onie  tftp

ALI_ONIE_COMM_TC_012_Update_ONIE_via_Static_IP+HTTP
    [Documentation]  This test checks the updating ONIE via Static IP+HTTP
    [Tags]  ALI_ONIE_COMM_TC_012_Update_ONIE_via_Static_IP+HTTP  migaloo  shamu
    [Timeout]  30 min 00 seconds
    [Setup]  boot Into Onie update Mode
    Step  1  get dhcp ip address  DUT  eth0  ONIE
    Step  2  update onie  http

ALI_ONIE_COMM_TC_013_Update_ONIE_via_DHCP+TFTP
    [Documentation]  This test checks the updating ONIE via DHCP+TFTP
    [Tags]  ALI_ONIE_COMM_TC_013_Update_ONIE_via_DHCP+TFTP  migaloo  shamu
    [Timeout]  60 min 00 seconds
    [Setup]  prepare onie updater  tftp  True
    Step  1  reboot to onie mode  ${ONIE_UPDATE_MODE}
    Step  2  get dhcp ip address  DUT  eth0  ONIE
    Step  3  check auto update onie  tftp
    [Teardown]  prepare onie updater  tftp  False

ALI_ONIE_COMM_TC_017_ONIE_Rescue_Mode
    [Documentation]  This test checks the updating ONIE via DHCP+HTTP
    [Tags]  ALI_ONIE_COMM_TC_017_ONIE_Rescue_Mode  migaloo  shamu
    [Timeout]  60 min 00 seconds
    Step  1  switch onie mode and check output  rescue
    Step  2  should have no discovery message
    Step  3  get dhcp ip address  DUT  eth0  ONIE
    Step  4  check Onie Tlv Value Existed

ALI_ONIE_COMM_TC_018_Update_MAC_Address_in_ONIE
    [Tags]  ALI_ONIE_COMM_TC_018_Update_MAC_Address_in_ONIE  migaloo  shamu
    [Timeout]  60 min 00 seconds
    [Setup]  boot Into Onie rescue Mode
    ${mac} =  get mac address  DUT  eth0
    Step  1  execute command  onie-syseeprom -s 0x24=${test_mac1}
    Step  2  reboot to onie mode  ${ONIE_RESCUE_MODE}
    BuiltIn.Sleep  60
    Step  3  verify mac address  ${test_mac1}
    Step  4  power cycle to mode  ${ONIE_RESCUE_MODE}
    Step  5  verify mac address  ${test_mac1}
    [Teardown]  restore mac address  ${mac}

ALI_ONIE_COMM_TC_019_ONIE_System_Information
    [Tags]  ALI_ONIE_COMM_TC_019_ONIE_System_Information  migaloo  shamu
    [Timeout]  60 min 00 seconds
    Step  1  switch onie mode and check output  rescue
    Step  2  check discovery message  false
    Step  3  check ip addr  eth0
#    Step  4  check syseeprom   @todo
    Step  5  check onie sys info  ${onie_sysinfo}
    Step  6  check onie sys info v

ALI_ONIE_COMM_TC_020_Management_Port_Link_Test
    [Tags]  ALI_ONIE_COMM_TC_020_Management_Port_Link_Test  migaloo  shamu
    [Timeout]  60 min 00 seconds
    Step  1  boot Into Onie rescue Mode
    Step  3  check ip addr  eth0
    Step  4  exec ping  DUT  ${tftp_server_ipv4}  4
    ${ip} =  get random ip  PC
    Step  5  config management interface  DUT  eth0  ${ip}  255.255.255.0  up
    Step  6  exec ping  DUT  ${tftp_server_ipv4}  4

ALI_ONIE_COMM_TC_022_TLV_EEPROM_R/W_Test
    [Tags]  ALI_ONIE_COMM_TC_022_TLV_EEPROM_R/W_Test  migaloo  shamu
    [Timeout]  60 min 00 seconds
    [Setup]  boot Into Onie rescue Mode
    ${BackupValue} =  get Onie Tlv Value
    Step  1  Write TLV Value And Read To Check  ${TLV_Value_Test1}
    Step  2  Write TLV Value And Read To Check  ${TLV_Value_Test2}
    [Teardown]  Run Keywords  write Tlv Value To Eeprom  ${BackupValue}
    ...  AND  reboot to onie mode  ${ONIE_RESCUE_MODE}

ALI_ONIE_COMM_TC_014_Update_ONIE_via_DHCP+HTTP
    [Documentation]  This test checks the updating ONIE via DHCP+HTTP
    [Tags]  ALI_ONIE_COMM_TC_014_Update_ONIE_via_DHCP+HTTP  migaloo  shamu
    [Timeout]  60 min 00 seconds
    [Setup]  prepare onie updater  http  True
    Step  1  reboot to onie mode  ${ONIE_UPDATE_MODE}
    Step  2  get dhcp ip address  DUT  eth0  ONIE
    Step  3  check auto update onie  http
    [Teardown]  prepare onie updater  http  False

ALI_ONIE_COMM_TC_023_ONIE_Reboot_Multi-times_Test
    [Tags]     ALI_ONIE_COMM_TC_023_ONIE_Reboot_Multi-times_Test  migaloo
    [Timeout]  60 min 00 seconds
    FOR    ${INDEX}    IN RANGE    1    ${MAX_LOOP}
        Step  1  reboot to onie mode  ${ONIE_UPDATE_MODE}
        Step  2  reboot to onie mode  ${ONIE_RESCUE_MODE}
        Step  3  reboot to onie mode  ${ONIE_INSTALL_MODE}
    END

ALI_ONIE_COMM_TC_008_Install_Sonic_via_DHCP+HTTP
    [Documentation]  This test checks the Installing ONIE via TFTP
    [Tags]  ALI_ONIE_COMM_TC_008_Install_Sonic_via_DHCP+HTTP  migaloo  shamu
    [Timeout]  60 min 00 seconds
    [Setup]  prepare os installer  http  True
    Step  1  reboot to onie mode  ${ONIE_INSTALL_MODE}
    Step  2  get dhcp ip address  DUT  eth0  ONIE
    Step  3  check auto install DiagOS  http
    Step  4  boot Into Onie Install Mode
    Step  5  boot Into DiagOS Mode
    [Teardown]  prepare os installer  http  False

*** Keywords ***
Onie Connect Device
    onieConnect

Onie Disconnect Device
    onieDisconnect