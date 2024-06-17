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
Documentation       This Suite will validate all bmc functions:

Library           BmcLibAdapter.py

Suite Setup       Bmc Connect Device
Suite Teardown    Bmc Disconnect Device

*** Variables ***

*** Test Cases ***
send test
    sendTest


*** Keywords ***
Bmc Connect Device
    BmcConnect

Bmc Disconnect Device
    BmcDisconnect



