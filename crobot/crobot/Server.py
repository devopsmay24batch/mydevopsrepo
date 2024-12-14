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

from Session import Session
import Logger as log
import YamlParse
import Const
import pexpect

class Server(Session):

    def __init__(self, deviceDict, needLogin = True):
        super().__init__()
        log.debug("Entering Server class procedure: __init__")
        self.deviceDict = deviceDict
        self.name = deviceDict['name']
        self.deviceType = deviceDict['deviceType']
        self.platform = deviceDict['platform']
        self.username = deviceDict['username']
        self.password = deviceDict['password']
        self.rootUserName = deviceDict['rootUserName']
        self.rootPassword = deviceDict['rootPassword']
        self.scpUsername = deviceDict['scpUsername']
        self.scpPassword = deviceDict['scpPassword']
        self.managementIP = deviceDict['managementIP']
        self.managementIPV6 = deviceDict['managementIPV6']
        self.staticIPV6 = deviceDict['staticIPV6']
        self.prompt = deviceDict['prompt']

        if needLogin:
            self.connect(self.username, self.managementIP)
            self.loginDev(self.username, self.password)

    def getCurrentPromptStr(self):
        return self.prompt

    def get(self, key):
        return self.deviceDict[key]

    def loginDev(self, username, password):
        log.debug('Entering Session class procedure loginDev with args : %s\n' % (str(locals())))
        if self.protocol == Const.PROTOCOL_TELNET:
            self.child.sendline(username)
            try:
                self.child.expect(Const.PSW_PROMT, 10)
            except pexpect.TIMEOUT:
                raise RuntimeError("can't login device")
        try:
            result = self.child.expect(['(y/n)', 'password:',  self.prompt], 20)
            if result == 0:
                self.child.sendline('y')
                self.child.expect('password:')
            self.child.sendline(password)
        except Exception as err:
            out = self.child.before
            log.cprint(str(out))
            log.cprint(str(err))
            raise RuntimeError("login device failed")

    @classmethod
    def getServer(cls, serverName, needLogin = False):
        deviceInfo = YamlParse.getDeviceInfo()
        deviceDict = deviceInfo[serverName]
        return Server(deviceDict, needLogin)
