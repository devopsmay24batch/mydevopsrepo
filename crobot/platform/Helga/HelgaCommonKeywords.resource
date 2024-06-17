###############################################################################
# LEGALESE:   "Copyright (C) 2020-      Celestica Corp. All rights reserved." #
#                                                                             #
# This source code is confidential, proprietary, and contains trade           #
# secrets that are the sole property of Celestica Corp.                       #
# Copy and/or distribution of this source code or disassembly or reverse      #
# engineering of the resultant object code are strictly forbidden without     #
# the written consent of Celestica Corp.                                      #
#                                                                             #
###############################################################################

*** Settings ***
Resource        CommonKeywords.resource


*** Keywords ***
uboot boot to diagos
    [Documentation]  Get U-Boot prompt and reboot to DiagOS

    open prompt  console=${diagos_mode}  sec=300


Kapok reboot to U-Boot and enter to Diag OS
    [Documentation]  Fenghuang reboot to U-Boot and enter to Diag OS

    open prompt  ${uboot_mode}  120
    open prompt  ${diagos_mode}  300
