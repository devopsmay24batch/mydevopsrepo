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

#Critical Step
#    [Arguments]    ${step_num}    ${function_name}
#    critical step  StepNumber=${step_num}  name=${function_name}
#
#
#Step
#     [Arguments]    ${step_num}    ${function_name}
#     openbmc step  StepNumber=${step_num}  name=${function_name}


Sub-Case
    [Arguments]    ${sub_case_name}    ${function_name}
    sub_case  case_name=${sub_case_name}  name=${function_name}
