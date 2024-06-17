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

*** Settings ***
Documentation       Tests to verify BIOS functions described in the BIOS function SPEC for the whiteboxproject.

Variables         BIOS_variable.py

Library           ../../whitebox/WhiteboxLibAdapter.py
Library           ../../whitebox/whitebox_lib.py
Library           bios_menu_lib.py
Library           openbmc_lib.py
Library           bios_lib.py
Library           ../SEASTONECommonLib.py

Resource          BIOS_keywords.robot
Resource          CommonResource.robot

Suite Setup       DiagOS Connect Device
Suite Teardown    DiagOS Disconnect Device

** Variables ***
# It is recommended to use <{ScriptName}|{FeatureName}|{DomainName}_Variable> file for variable declaration with help of
# setting table. This section should keep blank.
#In extreme case if script requires variable then it should be defined in this table with documentaiton tag

# -- Important --
# It is required to set default BIOS Password if not already set to run the below test-cases
# except for CONSR-BIOS-BSST-0012-0001 

*** Test Cases ***






























*** Keywords ***
DiagOS Connect Device
    DiagOSConnect

DiagOS Disconnect Device
    DiagOSDisconnect
