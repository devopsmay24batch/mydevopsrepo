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
import os
import sys

curDir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.join(curDir, '../commonlib'))
sys.path.append(os.path.join(curDir, '../../crobot'))

from DiagLibClass import *

DiagLibObj = None
DevObj = None


###################################################################################
# Wrapper Library Functions
###################################################################################
def WPL_Diag_Device_Connect():
    return DiagConnect()


def WPL_Diag_Device_Disconnect():
    return DiagDisconnect()


def WPL_DiagSetLibraryOrder():
    return DiagSetLibraryOrder()


def WPL_DiagInitTestLibrary(device):
    return DiagInitTestLibrary(device)


###################################################################################
# CRobot Specific Wrapper Library Functions
###################################################################################
def DiagConnect():
    global DiagLibObj
    log.debug("Entering DiagTestCase procedure: DiagConnect")
    DiagLibObj = DiagLibClass(DevObj)
    return DiagLibObj.loginDevice()


def DiagDisconnect():
    global DiagLibObj
    log.debug("Entering DiagTestCase procedure: DiagDisconnect")
    return DiagLibObj.disconnectDevice()


###################################################################################
# Init Test Library Functions
###################################################################################
def DiagSetLibraryOrder():
    return


def DiagInitTestLibrary(device):
    return


###################################################################################
# Get Library Object Functions
###################################################################################
def getDiagLibObj():
    global DiagLibObj
    return DiagLibObj


