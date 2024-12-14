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

BOOT_TIME = 480
ONIE_BOOT_TIME = 200

STOP_AUTOBOOT_PROMPT = r'autoboot.*stop with \'Delete\' key'
STOP_AUTOBOOT_KEY = '\x1b[3~'

PROMPT_PYTHON = '>>> $'
PROMPT_UEFI = r'(Shell>|\w+:\\[\w\\]*>)'
