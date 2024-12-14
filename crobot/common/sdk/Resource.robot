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
*** Keywords ***
Set Library Order
    Set Library Search Order     ScriptTopoModule

Init Test Library
    SdkInitTestLibrary   device=DUT

Check SDK initialization
    [Arguments]  ${port_mode}
    step  1  run sdk initialization  ${port_mode}
    step  2  go to centos
    step  3  check sdk port status  ${port_mode}

port default info test
    [Arguments]  ${port_mode}
    step  1  run default port info test  ${port_mode}
    step  2  check default port info status  ${port_mode}
    step  3  go to centos

check loopback test
    [Arguments]  ${port_mode}  ${loopback_type}
    Step  1  run port loopback test  ${port_mode}  ${loopback_type}
    step  2  go to centos
    step  3  check port loopback status  ${loopback_type}

verify loopback test
    [Arguments]  ${port_mode}  ${loopback_type}
    Step  1  run port loopback test  ${port_mode}  ${loopback_type}  full_log=False
    step  2  go to centos
    step  3  check port loopback status  ${loopback_type}

test L2 traffic
    [Arguments]  ${port_mode}
    Step  1  run test L2 traffic  ${port_mode}
    step  2  check L2 traffic status  ${port_mode}
    step  3  go to centos

test L3 traffic
    [Arguments]  ${port_mode}
    Step  1  run test L3 traffic  ${port_mode}
    step  2  check L3 traffic status  ${port_mode}
    step  3  go to centos

check and exit BCM user
    Step  1  verify remote shell  ${check_exit_bcm_user}  ${fail_dict}
    step  2  verify remote shell  ${check_bcm_user}  ${bcm_user}
