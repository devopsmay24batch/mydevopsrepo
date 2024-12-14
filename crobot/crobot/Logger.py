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
import sys
import logging
from inspect import getframeinfo, stack


def cprint(message):
    caller = getframeinfo(stack()[1][0])
    sys.__stdout__.write("%s:%d - %s\n" % (caller.filename, caller.lineno, message))
    sys.__stdout__.flush()

def print(message):
    sys.__stdout__.write("%s" %(message))
    sys.__stdout__.flush()


def cflush():
    sys.__stdout__.flush()


def info(msgObj):
    if isinstance(msgObj, dict):    # if object is dictionary type
        LogMsg = '\r\n{'
        for x in msgObj:
            keystr = str(x)
            valstr = msgObj[x]
            LogMsg += ('\r\n[%s, %s]\,' %(keystr, valstr))
        LogMsg += '\r\n}'

    else:    # if object is string message type
        LogMsg = ("\r\n" + msgObj + "\r\n")

    logging.info(LogMsg)
    print(LogMsg)


def debug(message):
    LogMsg = ("\r\n" + message + "\r\n")
    logging.debug(LogMsg)
    print(LogMsg)


def warning(message):
    LogMsg = ("\r\nWARNING: " + message + "\r\n")
    logging.warning(LogMsg)
    print(LogMsg)


def error(message):
    LogMsg = ("\r\nERROR: " + message + "\r\n")
    logging.error(LogMsg)
    print(LogMsg)


def success(message):
    LogMsg = ("\r\nPASS: " + message + "\r\n")
    logging.info(LogMsg)
    print(LogMsg)


def fail(message):
    LogMsg = ("\r\nFAIL: " + message + "\r\n")
    logging.error(LogMsg)
    print(LogMsg)
