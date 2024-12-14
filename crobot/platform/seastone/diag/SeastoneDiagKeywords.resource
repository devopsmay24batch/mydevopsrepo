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

Power cycle test
   Step  1  SEASTONECommonLib.Powercycle Device   DUT


Enter bios now
  enter_into_bios_setup  DUT

Switch to come
   SEASTONECommonLib.Switch To Cpu1  DUT
