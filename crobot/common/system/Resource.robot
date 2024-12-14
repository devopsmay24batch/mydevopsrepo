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



*** Variables ***
${LOOP_CNT}            1
##### Maximum repeat loop count #####
${MaxRepeatCount2}     2
${MaxRepeatCount5}     5
${MaxRepeatCount10}    10
${MaxRepeatCount20}    20
${MaxRepeatCount25}    25
${MaxRepeatCount50}    50
${MaxRepeatCount70}    70
${MaxRepeatCount100}   100
${MaxRepeatCount200}   200
${MaxRepeatCount700}   700
${MaxRepeatCount800}   800
${MaxRepeatCount1000}   1000
${MaxRepeatCount1500}   1500
${MaxRepeatCount2000}   2000
##### Stress loop time in seconds #####
${StressLoopTime2}     2
${StressLoopTime5}     5
${StressLoopTime60}    60
${StressLoopTime80}    80
${StressLoopTime120}   120
${StressLoopTime900}   900
${StressLoopTime1800}  1800
${StressLoopTime3600}  3600
${StressLoopTime7200}  7200
${StressLoopTime8000}  8000
${StressLoopTime10000}  10000
${StressLoopTime21000}  21000
${StressLoopTime21600}  21600
${StressLoopTime25500}  25500
##### Test case timeout in seconds #####
${Timeout1800}         1800
${Timeout3600}         3600
${Timeout4500}         4500
${Timeout8000}         8000
${Timeout10000}        10000
${Timeout18000}        18000
${Timeout30000}        30000



*** Keywords ***
WPL Set Library Order
    WPL_DiagSetLibraryOrder


WPL Init Test Library
    WPL_DiagInitTestLibrary   device=None


#Critical Step
#    [Arguments]    ${step_num}    ${function_name}
#    diag critical step  StepNumber=${step_num}  name=${function_name}


#Step
#    [Arguments]    ${step_num}    ${function_name}
#    diag step  StepNumber=${step_num}  name=${function_name}


#Sub-Case
#    [Arguments]    ${sub_case_name}    ${function_name}
#    diag subcase  case_name=${sub_case_name}  name=${function_name}

prepare MEM_TEST images
    create dir  ${workspace_sys}/MEM_TEST  ${OPENBMC_MODE}
    get dhcp ip address  DUT  eth0  ${OPENBMC_MODE}
    download images  DUT  MEM_TEST


