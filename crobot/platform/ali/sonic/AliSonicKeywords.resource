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
Resource        CommonKeywords.resource

*** Keywords ***


check monitor status
    [Documentation]  verify monitor status
    [Arguments]
    ...  ${console}=${diagos_mode}
    ...  ${pattern}=active \\(running\\)
    ...  ${option}=--no-pager

    execute command and verify with a pattern
    ...  console=${console}
    ...  command=systemctl status poap.service ${option}
    ...  pattern=${pattern}
    ...  msg=Failed to verify status poap.service!
    execute command and verify with a pattern
    ...  console=${console}
    ...  command=systemctl status swsdk.service ${option}
    ...  pattern=${pattern}
    ...  msg=Failed to verify status swsdk.service!