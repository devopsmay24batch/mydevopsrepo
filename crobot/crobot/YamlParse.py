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
import yaml

def stringToDict(string):
    return yaml.load(string)

def parse(filename):
    file = open(filename, 'r', encoding="utf-8")
    str = file.read()
    file.close()

    # change string to dict
    dict = yaml.load(str, Loader=yaml.FullLoader)
    #dict = yaml.load(str)
    return dict


def getTestConfig():
    return parse('../config/TestConfig.yaml')


def getDeviceInfo():
    return parse('../config/DeviceInfo.yaml')


def getPoeTesterInfo():
    return parse('../config/PoeTesters.yaml')


def getPowerCyclerInfo():
    return parse('../config/PowerCyclers.yaml')


def getEpsInfo():
    return parse('../config/EpsInfo.yaml')

def getServerInfo():
    return parse('../config/DeviceInfo.yaml')


def getSwImageInfo():
    return parse('../config/SwImages.yaml')

def getTestSuitInfo():
    return parse('../config/TestSuits.yaml')

def getTestCaseInfo():
    return parse('../config/TestCases.yaml')

def getEepromConfig():
    return parse('../config/EepromConfig.yaml')

def getStressConfig():
    return parse('../config/StressCycle.yaml')

def getKeyListConfig():
    return parse('../config/KeyList.yaml')
