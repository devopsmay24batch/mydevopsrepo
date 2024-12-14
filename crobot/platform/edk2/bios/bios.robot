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
#Library           ../WhiteboxLibAdapter.py
#Library           whitebox_lib.py
#Library           common_lib.py
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























*** Keywords ***
OS Connect Device
    OSConnect

OS Disconnect Device
    OSDisconnect
