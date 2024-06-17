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
import re
import sys
import time
import Logger as log


######################################################################
### Data structure classes for dictionary creation for portability ###
######################################################################
class parser(dict):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__dict__ = self


    def getValue(self, key):
        log.info("search key: %s" %key)
        if key in self.__dict__:
            value_list = []
            value = str(self.get(key))
            log.info("search value: %s" %value)
            value_list.append(value)
            return value_list


class nestedDict(dict):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__dict__ = self


