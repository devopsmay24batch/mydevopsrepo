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
import os, sys
import Logger as log
import traceback

SdkLibObj, deviceObj = None, None

try:
  from SdkLibClass import *
  import DeviceMgr
  deviceObj = DeviceMgr.getDevice()
except Exception as err:
  log.cprint(str(err))
  raise Exception(traceback.format_exc())


###################################################################################
# Wrapper Library Functions
###################################################################################
def Sdk_Device_Connect():
    return SdkConnect()


def Sdk_Device_Disconnect():
    try:
        SdkDisconnect()
    except:
        log.fail("Disconnect Device failed.")


def SdkSetLibraryOrder():
    return SdkSetLibraryOrder()


def SdkInitTestLibrary(device):
    SdkInitTestLibrary(device)


###################################################################################
# Specific Library Functions
###################################################################################
def SdkConnect():
    #connect_to_script_topology_devices(reset_ixia_ports='0',ixnetwork_host='1')
    global deviceObj
    deviceObj.login()


def SdkDisconnect():
    global deviceObj
    SdkLibObj.disconnect_device()

###################################################################################
# Init Test Library Functions
###################################################################################
def SdkSetLibraryOrder():
    return

def SdkInitTestLibrary(device):
    log.cprint('Entering SdkInitTestLibrary')
    global SdkLibObj
    SdkLibObj = SdkLibClass(deviceObj)
    SdkLibObj.change_NIC()


###################################################################################
# Get Library Object Functions
###################################################################################
def getSdkLibObj():
    global SdkLibObj
    return SdkLibObj
