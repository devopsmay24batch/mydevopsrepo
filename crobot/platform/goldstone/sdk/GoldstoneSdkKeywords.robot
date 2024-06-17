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
Library         Collections
Resource        CommonKeywords.resource


*** Keywords ***
Diag Check network connectivity
    [Arguments]  ${MODE}
    execute_check_dict  DUT  ${ifconfig_a_cmd}  mode=${MODE}
    ...  patterns_dict=${fail_dict}  timeout=5  is_negative_test=True
    ${ip} =  get ip address from config  PC
    exec_ping  DUT  ipAddress=${ip}  count=5  mode=${MODE}

Self Update Onie
    [Arguments]  ${version}
    Step  1  boot Into Onie Rescue Mode
    Step  2  config Static IP
    Step  3  onie Self Update  update=${version}
    Step  4  verify Onie And CPLD Version  version=${version}