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

class NumPlus():
    """  to simulate the operation of ++unm of C++
    Usage(e.g.):
    numPlus = NumPlus(-1)
    Log_Info("Latest BMC version from SwImage: [%s]" %fw_ver_array[numPlus()])
    Log_Info("Latest TPM version from SwImage: [%s]" %fw_ver_array[numPlus()])
    ...
    """
    def __init__(self, num):
        self.num = num

    def plus(self):
        self.num += 1
        return self.num

    def __call__(self):
        return self.plus()


class NumMinus():
    """  to simulate the operation of --unm of C++
    Usage (e.g.):
    numMinus = NumMinus(10)
    Log_Info("Latest BMC version from SwImage: [%s]" %fw_ver_array[numMinus()])
    Log_Info("Latest TPM version from SwImage: [%s]" %fw_ver_array[numMinus()])
    ...
    """
    def __init__(self, num):
        self.num = num

    def minus(self):
        self.num -= 1
        return self.num

    def __call__(self):
        return self.minus()
