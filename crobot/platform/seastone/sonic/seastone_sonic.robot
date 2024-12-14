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
Documentation       This Suite will vSeastonedate Sonic package

Library           SeastoneSonicLib.py
Library           ../SEASTONECommonLib.py
Library           CommonLib.py
Library           ../diag/SeastoneDiagLib.py
Variables         ../SeastoneCommonVariable.py
Variables         SeastoneSonicVariable.py

Resource          SeastoneSonicKeywords.resource
Resource	  CommonKeywords.resource

Suite Setup       Connect Device
Suite Teardown    Disconnect Device

*** Variables ***


*** Test Cases ***









*** Keywords ***
Connect Device
    Login Device

Disconnect Device
    Sonic Disconnect
