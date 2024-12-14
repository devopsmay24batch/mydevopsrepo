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
# Script       : BIOS.robot                                                                                           #
# Date         : July 29, 2020                                                                                        #
# Author       : James Shi <jameshi@celestica.com>                                                                    #
# Description  : This script will validate BIOS                                                                       #
#                                                                                                                     #
# Script Revision Details:                                                                                            #
#   Initial Draft for bios testing                                                                                    #
#######################################################################################################################

*** Settings ***
Documentation       Tests to verify BIOS functions described in the BIOS function SPEC for the whiteboxproject.

# Force Tags        bios
Variables         BIOS_variable.py
Library           ../WhiteboxLibAdapter.py
Library           whitebox_lib.py
Library           common_lib.py
Library           bios_menu_lib.py
Library           openbmc_lib.py
Resource          BIOS_keywords.robot
Resource          CommonResource.robot

Suite Setup       OS Connect Device
Suite Teardown    OS Disconnect Device

** Variables ***
# It is recommended to use <{ScriptName}|{FeatureName}|{DomainName}_Variable> file for variable declaration with help of
# setting table. This section should keep blank.
#In extreme case if script requires variable then it should be defined in this table with documentaiton tag

*** Test Cases ***
CONSR-BIOS-BSUP-0001-0001
###reboot_method(ac_cycle|reboot|dc_cycle)  ipmitool_cmd(power cycle|power reset|power on)
    [Documentation]  This test checks the BIOS programming functions by dc cycle
    [Tags]     CONSR-BIOS-BSUP-0001-0001  CONSR-BIOS-BSUP-0009-0001  CONSR-BIOS-STRS-0002-0001  tyr-se  tyr
    [Timeout]  20 min 00 seconds
    [Setup]  prepare BIOS images
    Sub-Case  CONSR-BIOS-BSUP-0001-0001_1  upgrade bios and dc cycle to check version
    Sub-Case  CONSR-BIOS-BSUP-0001-0001_2  common FW check list
    Sub-Case  CONSR-BIOS-BSUP-0001-0001_3  downgrade bios and dc cycle to check version
    Sub-Case  CONSR-BIOS-BSUP-0001-0001_4  common FW check list
    [Teardown]  clean all

CONSR-BIOS-STRS-0005-0001
    [Documentation]  This test checks BIOS/OS reboot function
    [Tags]     CONSR-BIOS-STRS-0005-0001  tyr  tyr-se
    [Timeout]  10 min 00 seconds
    Sub-Case  CONSR-BIOS-STRS-0005-0001_1  reboot os to check bios function
    Sub-Case  CONSR-BIOS-STRS-0005-0001_2  common FW check list

CONSR-BIOS-STRS-0007-0001
###reboot_method(ac_cycle|reboot|dc_cycle)  ipmitool_cmd(power cycle|power reset|power on)
    [Documentation]  This test checks the BIOS programming functions by reboot
    [Tags]     CONSR-BIOS-STRS-0007-0001  tyr  tyr-se
    [Timeout]  20 min 00 seconds
    [Setup]  prepare BIOS images
    Sub-Case  CONSR-BIOS-STRS-0007-0001_1  upgrade bios and reboot to check version
    Sub-Case  CONSR-BIOS-STRS-0007-0001_2  common FW check list
    Sub-Case  CONSR-BIOS-STRS-0007-0001_3  downgrade bios and reboot to check version
    Sub-Case  CONSR-BIOS-STRS-0007-0001_4   common FW check list
    [Teardown]  clean images  DUT  BIOS

CONSR-BIOS-STRS-0008-0001
    [Documentation]  This test checks system idle stress
    [Tags]     CONSR-BIOS-STRS-0008-0001  tyr  tyr-se
    [Timeout]  20 min 00 seconds
    Sub-Case  CONSR-BIOS-STRS-0008-0001_1  Idle overnight
    Sub-Case  CONSR-BIOS-STRS-0008-0001_2  common FW check list

*** Keywords ***
OS Connect Device
    OSConnect

OS Disconnect Device
    OSDisconnect
