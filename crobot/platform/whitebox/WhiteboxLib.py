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

# Old Code Before PR http://10.204.112.49:8080/c/CLSRobot/+/3823
# ----------------------------------------------------------------------------

# import Logger as log
#
# class WhiteboxLib():
#    def __init__(self):
#        log.debug("Entering Whitebox class procedure: __init__")
#        import DeviceMgr
#        self.device = DeviceMgr.getDevice()
#
#    def loginDevice(self):
#        log.debug("Entering Whitebox class procedure: login")
#        self.device.telnetConnect.open_connection(self.device.consoleIP, port=self.device.consolePort)
#        self.device.tryLogin()
#        log.cprint(self.device.currentBootMode)
#
#    def loginDevice1(self):
#        log.debug("Entering Whitebox class procedure: login")
#        self.device.telnetConnect.open_connection(self.device.esmbConsoleIP, port=self.device.esmbConsolePort)
#        self.device.tryLogin()
#        log.cprint(self.device.currentBootMode)
#
#    def disconnectDevice(self):
#        try:
#            self.device.trySwitchToCpu()
#        except Exception:
#            pass
#        finally:
#            return self.device.disconnect()


# This Change is after PR http://10.204.112.49:8080/c/CLSRobot/+/3823
# -------------------------------------------------------------------------------

import Logger as log
import re


class WhiteboxLib():
    def __init__(self, device=None):
        log.debug("Entering Whitebox class procedure: __init__")
        import DeviceMgr
        self.device = DeviceMgr.getDevice(device)
        try:
            self.ESMprompt = self.device.deviceDict['ESMprompt']
        except:
            self.ESMprompt = 'ESM\s\S\s=\>'

    def loginDevice(self):
        log.debug("Entering Whitebox class procedure: login")
        self.device.telnetConnect.open_connection(self.device.consoleIP, port=self.device.consolePort)
        self.whiteboxlib_tryLogin()
        log.cprint(self.device.currentBootMode)

    def loginDevice1(self):
        log.debug("Entering Whitebox class procedure: login")
        self.device.telnetConnect.open_connection(self.device.esmbConsoleIP, port=self.device.esmbConsolePort)
        self.whiteboxlib_tryLogin()
        log.cprint(self.device.currentBootMode)

    def disconnectDevice(self):
        try:
            self.device.trySwitchToCpu()
        except Exception:
            pass
        finally:
            return self.device.disconnect()

    # This function is similar to trylogin function inside master/crobot/crobot/Device.py. These changes
    # tries to solve the timeout problem that occurs when there is no Login Prompt
    def whiteboxlib_tryLogin(self):
        log.debug("Entering Whitebox class procedure: whiteboxlib_tryLogin")
        try:
            self.device.sendMsg('\r\n')
            altBmcLoginPrompt = 'None'
            loginStr = self.device.loginPromptBmc
            if re.search('.', loginStr):
                # strip off the hostname in login prompt
                slist = loginStr.split('.')
                str1 = str(slist[0])

                # alternate bmc login prompt string
                altBmcLoginPrompt = (str1 + ' ' + 'login:')
            promptList = [self.device.promptDiagOS, self.device.promptBmc, self.device.loginPromptDiagOS,
                          self.device.loginPromptBmc,
                          altBmcLoginPrompt, self.device.promptSdk, self.device.loginPromptESM, self.ESMprompt]
            patternList = re.compile('|'.join([x for x in promptList if x]))
            output = self.device.read_until_regexp(patternList, 20)
            log.debug(output)

            if self.device.loginPromptESM and re.search(self.device.loginPromptESM, output):
                # Login for ESM console
                res = self.device.sendMsg(self.device.ESMUserName)
                self.device.sendMsg("\r")
                time.sleep(2)
                output2 = self.device.read_until_regexp("Password: ", 20)
                log.debug(output2)
                self.device.sendMsg(self.device.ESMUserPassword)
                self.device.sendMsg("\r")
                time.sleep(2)
                self.device.sendMsg("\r")
                time.sleep(2)
                return

            if self.device.promptSdk and re.search(self.device.promptSdk, output):
                # Issue 'exit' command to exit SDK prompt to diagOS prompt
                log.debug("\nDetected SDK prompt.\n")
                self.device.sendMsg("exit")
                self.device.sendMsg("\r\n")
                time.sleep(3)
                output = self.device.read_until_regexp(patternList, 20)
                log.debug(output)

            if self.device.loginPromptDiagOS and re.search(self.device.loginPromptDiagOS, output):
                self.device.setConnectionTimeout(5)
                output = self.device.telnetConnect.login(self.device.rootUserName, self.device.rootPassword)
                ret = self.device.sendMsg("\r\n")
                output = self.device.readUntil(self.device.promptDiagOS, timeout=3)
                log.debug(output)
                self.device.currentBootMode = self.device.getBootMode(output)
                return

            elif (self.device.loginPromptBmc and re.search(self.device.loginPromptBmc, output)) \
                    or (altBmcLoginPrompt and re.search(altBmcLoginPrompt, output)):
                self.device.setConnectionTimeout(5)
                output = self.device.telnetConnect.login(self.device.bmcUserName, self.device.bmcPassword)
                ret = self.device.sendMsg("\r\n")
                output = self.device.readUntil(self.device.promptBmc, timeout=3)
                log.debug(output)
                self.device.currentBootMode = self.device.getBootMode(output)
                return

            else:
                self.device.currentBootMode = self.device.getBootMode(output)
                return

        except Exception as err:
            log.debug("tryLogin failed")

