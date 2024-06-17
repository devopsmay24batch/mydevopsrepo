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
########################################
### Import Robot-Framework Libraries ###
########################################
from robot.libraries.BuiltIn import BuiltIn


#######################
### Custom Keywords ###
#######################
def critical_step(StepNumber, name):
    return BuiltIn().run_keyword(name)


def step(StepNumber, name, *args):
   return BuiltIn().run_keyword(name, *args)


def sub_case(case_name, name):
    return BuiltIn().run_keyword(name)
