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
Documentation       This Suite will validate all Onie functions:

Library           OnieLib.py

Suite Setup       Onie Connect Device
Suite Teardown    Onie Disconnect Device

*** Variables ***

*** Test Cases ***

*** Keywords ***
Onie Connect Device
    OnieConnect

Onie Disconnect Device
    OnieDisconnect

