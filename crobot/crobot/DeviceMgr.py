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

import Const
import Logger as log
from Const import DUT
from Const import SSH_DUT
import traceback

curDir = os.path.dirname(os.path.abspath(__file__))
parentDir = os.path.dirname(curDir)
sys.path.append(parentDir)
sys.path.append(os.path.join(parentDir, 'platform'))
sys.path.append(os.path.join(parentDir, 'platform', 'dell'))
sys.path.append(os.path.join(parentDir, 'platform', 'facebook'))
sys.path.append(os.path.join(parentDir, 'platform', 'whitebox'))
sys.path.append(os.path.join(parentDir, 'platform', 'kapok'))
sys.path.append(os.path.join(parentDir, 'platform', 'ali'))
sys.path.append(os.path.join(parentDir, 'platform', 'juniper'))
sys.path.append(os.path.join(parentDir, 'platform', 'google'))
sys.path.append(os.path.join(parentDir, 'platform', 'edk2'))
sys.path.append(os.path.join(parentDir, 'platform', 'seastone'))
sys.path.append(os.path.join(parentDir, 'platform', 'moonstone'))
sys.path.append(os.path.join(parentDir, 'platform', 'goldstone'))
sys.path.append(os.path.join(parentDir, 'platform', 'Helga'))

try:
    from Device import Device
    from Server import Server
    import YamlParse
    from PowerCycler import PowerCycler
    from DellDevice import DellDevice
    from FacebookDevice import FacebookDevice
    from WhiteboxDevice import WhiteboxDevice
    from KapokDevice import KapokDevice
    from AliDevice import AliDevice
    from JuniperDevice import JuniperDevice
    from GoogleDevice import GoogleDevice
    from SessionDevice import SessionDevice
    from EDK2Device import EDK2Device
    from SEASTONEDevice import SEASTONEDevice
    from MOONSTONEDevice import MOONSTONEDevice
    from GOLDSTONEDevice import GOLDSTONEDevice
    from HelgaDevice import HelgaDevice
except Exception as err:
    log.cprint(str(err))
    log.cprint(traceback.format_exc())

devices = {}
usingSsh = False

def getPowerCycler(powerCyclerName, powerCyclerPort):
    deviceInfo = YamlParse.getPowerCyclerInfo()
    dict = deviceInfo[powerCyclerName]
    pc = PowerCycler(dict, powerCyclerPort)
    return pc

def getServerInfo(serverName):
    serverInfo = YamlParse.getServerInfo()
    dict = serverInfo[serverName]
    svr = Server(dict, False)
    return svr

def getDevice(deviceName = None):
    global devices
    try:
        if deviceName == None or deviceName == DUT:  # should get the current device running test on
            if usingSsh:
                return getDutDevice(SSH_DUT)
            else:
                return getDutDevice(DUT)
        else:
            if deviceName in devices.keys():
                return devices[deviceName]
            devices[deviceName] = getTheDevice(deviceName)
            return devices[deviceName]
    except Exception as err:
        log.cprint(str(err))
        log.cprint(traceback.format_exc())        


def getDutDevice(device):
    global devices
    if device in devices.keys():
        return devices[device]
    else:
        deviceName = os.environ['deviceName']
        devices[device] = getTheDevice(deviceName)
        return devices[device]


def getTheDevice(deviceName):
    deviceInfo = YamlParse.getDeviceInfo()
    deviceDict = deviceInfo[deviceName]
    deviceType = deviceDict['deviceType']
    platform = deviceDict['platform']

    if usingSsh:
        return SessionDevice(deviceDict)
    if deviceType == 'server':
        return Server(deviceDict)

    if platform == Const.PLATFORM_DELL:
        return DellDevice(deviceDict)
    elif platform == Const.PLATFORM_FACEBOOK:
        return FacebookDevice(deviceDict)
    elif platform == Const.PLATFORM_KAPOK:
        return KapokDevice(deviceDict)
    elif platform == Const.PLATFORM_WHITEBOX:
        return WhiteboxDevice(deviceDict)
    elif platform == Const.PLATFORM_ALI:
        return AliDevice(deviceDict)
    elif platform == Const.PLATFORM_JUNIPER:
        return JuniperDevice(deviceDict)
    elif platform == Const.PLATFORM_GOOGLE:
        return GoogleDevice(deviceDict)
    elif platform == Const.PLATFORM_EDK2:
        return EDK2Device(deviceDict)
    elif platform == Const.PLATFORM_SEASTONE:
        return SEASTONEDevice(deviceDict)
    elif platform == Const.PLATFORM_MOONSTONE:
        return MOONSTONEDevice(deviceDict)
    elif platform == Const.PLATFORM_GOLDSTONE:
        return GOLDSTONEDevice(deviceDict)
    elif platform == Const.PLATFORM_HELGA:
        return HelgaDevice(deviceDict)
    else:
        return Device(deviceDict)

def getDeviceObject(deviceName):
    return getDevice(deviceName)
