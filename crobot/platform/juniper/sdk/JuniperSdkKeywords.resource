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

change dir to sdk path
    change dir
        ...  path=${sdk_path}
        ...  mode=${diagos_mode}

exit sdk mode
    send a line  command=exit
    send a line  command=exit
    open prompt  console=${diagos_mode}  sec=10

exit remote shell mode
    send a line  command=./cls_shell exit
    send a line  command=exit
    open prompt  console=${diagos_mode}  sec=10



load sdk mode
    send a line  command=./${SDK_SCRIPT}
    read until pattern  pattern=${BCM_promptstr}  sec=30


check all port up status
    verify all port status
        ...  port_status_pattern=${port_up_status}
        ...  port_cmd=${ps_cd_cmd}
        ...  port_search_pattern=${port_pattern}


check all port down status
    verify all port status
        ...  port_status_pattern=${port_down_status}
        ...  port_cmd=${ps_cd_cmd}
        ...  port_search_pattern=${port_pattern}

check port loopback mode
    [Arguments]  ${mode_pattern}
    verify all port status
        ...  port_status_pattern=${mode_pattern}
        ...  port_cmd=${ps_cd_cmd}
        ...  port_search_pattern=${port_pattern}


clear all port counter
    change ports status and check pattern
        ...  port_cmd=${clear_c_cmd}
        ...  patterns=${fail_pattern}
    change ports status and check pattern
        ...  port_cmd=${show_c_cmd}
        ...  patterns=${fail_pattern}

let cpu send packages
    change ports status and check pattern
        ...  port_cmd=${let_CPU_send_package_cmd}
        ...  patterns=${fail_pattern}

sleep 300s
    change ports status and check pattern
        ...  port_cmd=${sleep_300s_cmd}
        ...  patterns=${sleep_pattern}
        ...  timeout=350

stop traffic
    change ports status and check pattern
        ...  port_cmd=${stop_traffic_cmd}
        ...  patterns=${fail_pattern}
