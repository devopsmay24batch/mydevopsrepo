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

check power mtp
    Step  1  powercycle_pdu1  DUT  ${mtp_ip}  ${mtp_comm}


check power brixia
    Step  1  powercycle_pdu1  DUT  ${brixia_ip}  ${brixia_comm}

AC power device
    Step  1  check powercycle device  DUT   ${brixia_ip}  ${brixia_comm}



