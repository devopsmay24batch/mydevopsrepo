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

*** Keywords ***

Write TLV Value And Read To Check
    [Arguments]  ${TLV_VALUE}
    write Tlv Value To Eeprom  ${TLV_VALUE}
    power Cycle To Onie Rescue Mode
    check Tlv Value From Eeprom  ${TLV_VALUE}
