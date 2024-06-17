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
#######################################################################################################################
# Script       : BIOS_keywords.robot                                                                                  #
# Date         : July 29, 2020                                                                                        #
# Author       : James Shi <jameshi@celestica.com>                                                                    #
# Description  : This script used as keywords in bios.robot                                                           #
#                                                                                                                     #
# Script Revision Details:                                                                                            #
#   Initial Draft for BIOS testing                                                                                    #
#######################################################################################################################

*** Settings ***
Variables         BIOS_variable.py

Library           whitebox_lib.py
Library           openbmc_lib.py
#Library           common_lib.py
Library           bios_menu_lib.py
Library           CommonLib.py
Library           OperatingSystem
#Library           ../WhiteboxLibAdapter.py
#Library           ../ses/ses_lib.py
#Library           ../bmc/bmc_lib.py
Library           bios_lib.py

Resource          BIOS_keywords.robot
Resource          CommonResource.robot
#Resource          BMC_keywords.robot

*** Keywords ***
Enter bios now
  enter_into_bios_setup  DUT  ${bios_pass}


Enter bios as user
  enter_into_bios_setup  DUT  ${user_pass}

check bios basic
   bios_basic  DUT  ${bios_pass}

leave bios
   exit bios menu  DUT

boot sonic via bios
    check sonic boot via bios  DUT

check the microcode
   check_cpu_microcode  DUT


access bios via shell
   enter bios with shell

AC power device
   Step  1  EDK2CommonLib.Powercycle Device   DUT   no


chuck it
   Step  1  exit bios shelll  DUT
   Step  2  exit the shell


Power me up
   Step  1   EDK2CommonLib.Powercycle Device   DUT   yes

exit the shell
    EDK2CommonLib.exit the shell
