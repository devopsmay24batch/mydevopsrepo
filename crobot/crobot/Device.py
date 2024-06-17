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
import Const
import Logger as log
import time
import sys
import re
from TelnetDevice import TelnetDevice
from subprocess import Popen, PIPE
# from Session import Session
from Decorator import deprecated


class Device(TelnetDevice):

    def __init__(self, deviceDict):
        super().__init__()

        log.debug("Entering Device class procedure: __init__")
        self.deviceDict = deviceDict

        self.name = deviceDict['name']
        self.os = deviceDict['os']
        self.deviceType = deviceDict['deviceType']
        self.consoleIP = deviceDict['consoleIP']
        self.consolePort = int(deviceDict['consolePort'])
        self.bmcConsoleIP = deviceDict['bmcConsoleIP']
        self.bmcConsolePort = int(deviceDict['bmcConsolePort'])
        self.keysSwitchToCpu = deviceDict['keysSwitchToCpu']
        self.keysSwitchToBmc = deviceDict['keysSwitchToBmc']
        self.userName = deviceDict['userName']
        self.password = deviceDict['password']
        self.rootUserName = deviceDict['rootUserName']
        self.rootPassword = deviceDict['rootPassword']
        self.bmcUserName = deviceDict['bmcUserName']
        self.bmcPassword = deviceDict['bmcPassword']
        self.managementIP = deviceDict['managementIP']
        self.managementMask = deviceDict['managementMask']
        self.platform = deviceDict['platform']
        self.managementInterface = deviceDict['managementInterface']
        self.powerCyclerName = deviceDict['powerCycler']
        self.powerCyclerPort = deviceDict['powerCyclerPort']
        self.poeTesters = deviceDict['poeTesters']
        self.epsList = deviceDict['epsList']
        self.promptOnie = deviceDict['promptOnie']
        self.promptDiagOS = deviceDict['promptDiagOS']
        self.promptGrub = deviceDict['promptGrub']
        self.promptBmc = deviceDict['promptBmc']
        self.loginPromptBmc = deviceDict['loginPromptBmc']
        self.loginPromptDiagOS = deviceDict['loginPromptDiagOS']
        self.loginPromptESM = deviceDict['loginPromptESM']
        self.ESMUserName = deviceDict['ESMUserName']
        self.ESMUserPassword = deviceDict['ESMUserPassword']
        self.promptSdk = 'BCM.0>|IVM:0>'
        self.unidiagPrompt = 'unidiag|Unidiag'

        import DeviceMgr
        self.powerCycler = DeviceMgr.getPowerCycler(self.powerCyclerName, self.powerCyclerPort)
        self.pc_server = DeviceMgr.getServerInfo('PC')
        self.pc_scp_username = self.pc_server.scpUsername
        self.pc_scp_password = self.pc_server.scpPassword
        self.pc_scp_ip = self.pc_server.managementIP
        self.pc_scp_ipv6 = self.pc_server.managementIPV6
        self.pc_scp_static_ip = self.pc_server.staticIPV6
        self.jenkins_server = DeviceMgr.getServerInfo('JENKINS')
        self.jenkins_scp_username = self.jenkins_server.scpUsername
        self.jenkins_scp_password = self.jenkins_server.scpPassword
        self.jenkins_scp_ip = self.jenkins_server.managementIP
        self.jenkins_scp_ipv6 = self.jenkins_server.managementIPV6
        self.jenkins_scp_static_ip = self.jenkins_server.staticIPV6

        # self.platformDevice = DeviceMgr.getPlatformDevice(deviceName)
        self.currentBootMode = None
        self.keywords = None

    def get(self, key):
        return self.deviceDict[key]

    # for that bmc and cpu share a console, need consider these cases:
    #  current mode is cpu, user have ever login
    #  current mode is cpu, user have not ever login
    #  current mode is bmc, user have ever login bmc， and user have ever login cpu
    #  current mode is bmc, user have ever login bmc， and user have not ever login cpu
    #  current mode is bmc, user have not ever login bmc， and user have ever login cpu
    #  current mode is bmc, user have not ever login bmc， and user have not ever login cpu
    def login(self):
        log.debug("Entering Device class procedure: login")
        self.telnetConnect.open_connection(self.consoleIP, port=self.consolePort)
        self.tryLogin()
        log.cprint(self.currentBootMode)
        if self.currentBootMode != None and self.currentBootMode != Const.BOOT_MODE_BMC and self.currentBootMode != Const.BOOT_MODE_OPENBMC:
            return

        # bmc and cpu share one console, and in bmc mode
        if self.consoleIP == self.bmcConsoleIP:
            output = self.switchToCpu()

    # for that bmc and cpu share a console, need consider similar cases as login
    def loginBmc(self):
        log.debug("Entering Device class procedure: loginBmc")
        self.telnetConnect.open_connection(self.bmcConsoleIP, port=self.bmcConsolePort)
        self.tryLoginBmc()
        if self.currentBootMode == Const.BOOT_MODE_BMC or self.currentBootMode == Const.BOOT_MODE_OPENBMC:
            return

        # bmc and cpu share one console, and in cpu mode
        if self.consoleIP == self.bmcConsoleIP:
            self.switchToBmc()

    def tryLoginBmc(self):
        log.debug("Entering Device class procedure: tryLoginBmc")
        try:
            ret = self.sendMsg("\r\n")
            altBmcLoginPrompt = 'None'
            loginStr = self.loginPromptBmc
            if re.search('.', loginStr):
                # strip off the hostname in login prompt
                slist = loginStr.split('.')
                str1 = str(slist[0])
                # alternate bmc login prompt string
                altBmcLoginPrompt = (str1 + ' ' + 'login:')
            output = self.read_until_regexp(self.promptBmc + '|' + self.loginPromptBmc + '|' + altBmcLoginPrompt, 20)
            print('Theoutput is',output)
            if re.search(self.promptBmc, output):
                log.debug('ITS MODE_BMC')
                self.currentBootMode = Const.BOOT_MODE_BMC
                return

            self.setConnectionTimeout(5)
            log.debug('Sending the desired username/password to login')
            print('Sending {} as username and {} as password '.format(self.bmcUserName,self.bmcPassword))
            output = self.telnetConnect.login(self.bmcUserName, self.bmcPassword)
            ret = self.sendMsg("\r\n")
            output = self.readUntil(self.promptBmc, 3)
            self.currentBootMode = self.getBootMode(output)
        except Exception as err:
            log.cprint(str(err))
            log.debug("tryLoginBmc failed")

    def loginToNEWBMC(self):
        log.debug("Entering Device class procedure: loginToNEWBMC")
        self.sendMsg('\r\n')
        time.sleep(10)
        self.sendMsg(self.bmcUserName)

        try:
            self.sendMsg('\r\n')
            time.sleep(1)
            output = self.readUntil("Password:", timeout=3)
            log.cprint(output)
            self.sendMsg(self.bmcPassword)
        except:
            pass

        self.sendMsg('\r\n')
        time.sleep(1)
        self.read_until_regexp(self.promptBmc)

    def tryLogin(self):
        log.debug("Entering Device class procedure: tryLogin")
        try:
            self.sendMsg('\r\n')
            altBmcLoginPrompt = 'None'
            loginStr = self.loginPromptBmc
            if re.search('.', loginStr):
                # strip off the hostname in login prompt
                slist = loginStr.split('.')
                str1 = str(slist[0])
                # alternate bmc login prompt string
                altBmcLoginPrompt = (str1 + ' ' + 'login:')
            promptList = [self.promptDiagOS, self.promptBmc, self.loginPromptDiagOS, self.loginPromptBmc,
                          altBmcLoginPrompt, self.promptSdk, self.loginPromptESM]
            patternList = re.compile('|'.join(promptList))
            output = self.read_until_regexp(patternList, 20)
            log.debug(output)

            if re.search(self.loginPromptESM, output):
                #Login for ESM console
                res=self.sendMsg(self.ESMUserName)
                self.sendMsg("\r")
                time.sleep(2)
                output2=self.read_until_regexp("Password: ", 20)
                log.debug(output2)
                self.sendMsg(self.ESMUserPassword)
                self.sendMsg("\r")
                time.sleep(2)
                self.sendMsg("\r")
                time.sleep(2)
                #output3 = self.until_regexp("ESM\s\w\s.*#", timeout=5)
                #log.debug(output3)
                return

            if re.search(self.promptSdk, output):
                # Issue 'exit' command to exit SDK prompt to diagOS prompt
                log.debug("\nDetected SDK prompt.\n")
                self.sendMsg("exit")
                self.sendMsg("\r\n")
                time.sleep(3)
                output = self.read_until_regexp(patternList, 20)
                log.debug(output)

            if re.search(self.loginPromptDiagOS, output):
                self.setConnectionTimeout(5)
                output = self.telnetConnect.login(self.rootUserName, self.rootPassword)
                ret = self.sendMsg("\r\n")
                output = self.readUntil(self.promptDiagOS, timeout=3)
                log.debug(output)
                self.currentBootMode = self.getBootMode(output)
                return

            elif re.search(self.loginPromptBmc, output) or re.search(altBmcLoginPrompt, output):
                self.setConnectionTimeout(5)
                output = self.telnetConnect.login(self.bmcUserName, self.bmcPassword)
                ret = self.sendMsg("\r\n")
                output = self.readUntil(self.promptBmc, timeout=3)
                log.debug(output)
                self.currentBootMode = self.getBootMode(output)
                return

            else:
                self.currentBootMode = self.getBootMode(output)
                return

        except Exception as err:
            log.debug("tryLogin failed")
            # raise RuntimeError("tryLogin failed")
            # try:
            #     self.currentBootMode = self.getBootMode(err)
            # except Exception as err:
            #     pass

    def trySwitchToBmc(self):
        log.debug("Entering Device class procedure: trySwitchToBmc")
        for key in self.keysSwitchToBmc:
            log.cprint(key)
            self.sendMsg(key)
            time.sleep(0.5)
        self.sendMsg("\r\n")
        time.sleep(1)
        self.sendMsg("\r\n")
        time.sleep(1)
        return ''

    def switchToBmc(self):
        log.debug("Entering Device class procedure: switchToBmc")
        self.trySwitchToBmc()
        self.tryLoginBmc()
        if self.currentBootMode != Const.BOOT_MODE_BMC and self.currentBootMode != Const.BOOT_MODE_OPENBMC:
            raise RuntimeError("In Device.switchToBmc, can't switch to BMC!")
        return ''

    def switchToCpu(self):
        log.debug("Entering Device class procedure: switchToCpu")
        self.trySwitchToCpu()
        self.tryLogin()
        if self.currentBootMode != Const.BOOT_MODE_DIAGOS and self.currentBootMode != Const.BOOT_MODE_ONIE and self.currentBootMode != Const.BOOT_MODE_CENTOS and self.currentBootMode != Const.BOOT_MODE_PYTHON3:
            raise RuntimeError("In Device.switchToCpu, can't switch to CPU!")
        return ''

    def trySwitchToCpu(self):
        log.debug("Entering Device class procedure: trySwitchToCpu")
        for key in self.keysSwitchToCpu:
            log.cprint(key)
            self.sendMsg(key)
            time.sleep(0.5)
        self.sendMsg("\r\n")
        time.sleep(1)
        self.sendMsg("\r\n")
        return ''

    def disconnectBmc(self):
        log.debug("Entering Device class procedure: disconnectBmc")
        self.telnetConnect.close_connection()
        pass

    def getBootMode(self, msgStr):
        log.debug("Entering Device class procedure: getBootMode")
        self.setConnectionTimeout(15)
        LogMsg = ''
        altBmcLoginPrompt = 'None'
        loginStr = self.loginPromptBmc
        if re.search('.', loginStr):
            # strip off the hostname in login prompt
            slist = loginStr.split('.')
            str1 = str(slist[0])
            # alternate bmc login prompt string
            altBmcLoginPrompt = (str1 + ' ' + 'root:')
        # login to diagOS first if currently at diagOS prompt
        if re.search(self.loginPromptDiagOS, msgStr):
            output = self.loginToDiagOS()
            # output = self.telnetConnect.login(self.rootUserName, self.rootPassword)  this failed in a case.
            self.sendMsg('\r\n')
            time.sleep(1)
            msgStr = self.readMsg()

        # login to bmc first if currently at bmc prompt
        elif re.search(self.loginPromptBmc, msgStr) or re.search(altBmcLoginPrompt, msgStr):
            output = self.telnetConnect.login(self.bmcUserName, self.bmcPassword)
            log.debug(output)
            self.sendMsg('\r\n')
            time.sleep(1)
            msgStr = self.readMsg()

        if re.search(self.promptOnie, msgStr):
            log.debug("Boot mode: ONIE\r\n")
            return Const.BOOT_MODE_ONIE
        elif re.search(self.promptDiagOS, msgStr):
            if "sonic" in str(self.os):
                log.debug("Boot mode: CENTOS\r\n")
                return Const.BOOT_MODE_CENTOS
            else:
                log.debug("Boot mode: DIAGOS\r\n")
                return Const.BOOT_MODE_DIAGOS
        elif re.search(self.promptBmc, msgStr):
            if "sonic" in str(self.os):
                log.debug("Boot mode: OPENBMC\r\n")
                return Const.BOOT_MODE_OPENBMC
            else:
                log.debug("Boot mode: BMC\r\n")
                return Const.BOOT_MODE_BMC
        elif re.search(self.promptGrub, msgStr):
            log.debug("Boot mode: GRUB\r\n")
            return Const.BOOT_MODE_GRUB
        elif ">" in str(msgStr):
            log.debug("Boot mode: GRUB\r\n")
            return Const.BOOT_MODE_GRUB
        elif re.search(self.ESMprompt, msgStr):
            log.debug("Boot mode: Lenovo ESM\r\n")
            return
        else:
            LogMsg = ("Unknown boot mode,  msgStr: " + str(msgStr))
            LogMsg += "\r\ngetBootMode result: FAIL\r\n"
            log.debug(LogMsg)
            raise RuntimeError(LogMsg)

    def getCurrentBootMode(self):
        log.debug("Entering Device class procedure: getCurrentBootMode")
        return self.currentBootMode

    def setCurrentBootMode(self, CurrentBootMode):
        log.debug("Entering Device class procedure: setCurrentBootMode")
        LogMsg = ''
        bootMode = CurrentBootMode.upper()
        if bootMode == Const.BOOT_MODE_ONIE:
            LogMsg = "Set boot mode: ONIE\r\n"
        elif bootMode == Const.BOOT_MODE_DIAGOS:
            LogMsg = "Set boot mode: DIAGOS\r\n"
        elif bootMode == Const.BOOT_MODE_CENTOS:
            LogMsg = "Set boot mode: CENTOS\r\n"
        elif bootMode == Const.BOOT_MODE_BMC:
            LogMsg = "Set boot mode: BMC\r\n"
        elif bootMode == Const.BOOT_MODE_OPENBMC:
            LogMsg = "Set boot mode: OPENBMC\r\n"
        elif bootMode == Const.BOOT_MODE_GRUB:
            LogMsg = "Set boot mode: GRUB\r\n"
        elif bootMode == Const.BOOT_MODE_PYTHON3:
            LogMsg = "Set boot mode: PYTHON3\r\n"
        else:
            LogMsg = ("Unknown boot mode: " + str(bootMode))
            LogMsg += "\r\nsetCurrentBootMode result: FAIL\r\n"
            log.debug(LogMsg)
            raise RuntimeError(LogMsg)

        log.debug(LogMsg)
        self.currentBootMode = bootMode
        return LogMsg

    def powerCycle(self):
        log.debug("Entering Device class procedure: powerCycle")
        return self.powerCycler.powerCycle()

    def powerCycleDevice(self):
        log.debug("Entering Device class procedure: powerCycleDevice")
        return self.powerCycler.powerCycleDevice()

    def bootIntoOnieInstallMode(self):
        log.debug("Entering Device class procedure: bootIntoOnieInstallMode")
        return self.bootIntoOnieMode(Const.ONIE_INSTALL_MODE)

    def bootIntoOnieRescueMode(self):
        log.debug("Entering Device class procedure: bootIntoOnieRescueMode")
        return self.bootIntoOnieMode(Const.ONIE_RESCUE_MODE)

    def bootIntoOnieMode(self, ONIE_BOOT_MODE):
        log.debug("Entering Device class procedure: bootIntoOnieMode")
        # check whether at DiagOS login prompt
        self.setConnectionTimeout(5)
        LogMsg = ''
        self.sendMsg('\r\n')
        time.sleep(1)
        output = self.readMsg()
        if "login:" in output:
            # login to DiagOS first
            output = self.loginToDiagOS()
            if "result: FAIL" in output:
                LogMsg = "\r\nFail to login to DiagOS."
                LogMsg = "\r\nbootIntoOnieMode result: FAIL"
                log.debug(LogMsg)
                raise RuntimeError(LogMsg)
            else:
                self.currentBootMode = Const.BOOT_MODE_DIAGOS

        # get boot mode
        self.sendMsg('\r\n\r\n\r\n')
        time.sleep(1)
        output = self.readMsg()
        self.currentBootMode = self.getBootMode(output)
        if self.currentBootMode == Const.BOOT_MODE_ONIE:
            output = self.onieBootIntoOnieMode(ONIE_BOOT_MODE)
            if "result: FAIL" in output:
                LogMsg = "\r\nbootIntoOnieMode result: FAIL"
                log.debug(LogMsg)
                raise RuntimeError(LogMsg)

        elif self.currentBootMode == Const.BOOT_MODE_DIAGOS:
            LogMsg = ("\r\nDetect boot mode: %s" % (str(self.currentBootMode)))
            LogMsg += ("\r\nRebooting device to boot into Onie %s..." % (str(ONIE_BOOT_MODE)))
            log.debug(LogMsg)
            # reboot system
            self.sendMsg('\r')
            self.sendMsg("reboot")
            self.sendMsg('\r')
            output = ''
            try:
                output = self.readUntil("reboot")
                log.debug(output)
            except Exception as err:
                LogMsg = "\r\nFail to reboot system from DiagOS."
                LogMsg += "\r\nbootIntoOnieMode result: FAIL"
                log.debug(LogMsg)
                raise RuntimeError(LogMsg)

        else:
            LogMsg = ("\r\nDetect boot mode: %s" % (str(self.currentBootMode)))
            LogMsg += "\r\nPower cycling device to boot into Onie..."
            log.debug(LogMsg)
            # power cycle system
            output = self.powerCycle()
            if "result: FAIL" in output:
                LogMsg = "\r\nbootIntoOnieMode result: FAIL"
                log.debug(LogMsg)
                raise RuntimeError(LogMsg)

        # wait for grub prompt first if system reboot or power cycle
        output1 = self.waitForGrubPrompt()
        if "result: FAIL" in output1:
            LogMsg = "\r\nbootIntoOnieMode result: FAIL"
            log.debug(LogMsg)
            raise RuntimeError(LogMsg)

        # boot into required onie mode
        output2 = self.grubBootIntoOnie(ONIE_BOOT_MODE)
        if "result: FAIL" in output2:
            LogMsg = "\r\nbootIntoOnieMode result: FAIL"
            log.debug(LogMsg)
            raise RuntimeError(LogMsg)

        # update currentBootMode
        self.setCurrentBootMode(Const.BOOT_MODE_ONIE)
        output4 = "\r\nbootIntoOnieMode result: PASS"
        log.debug(output4)
        time.sleep(1)
        return output4

    def onieBootIntoOnieMode(self, ONIE_BOOT_MODE):
        LogMsg = ("\r\nRebooting device to boot into Onie %s..." % (str(ONIE_BOOT_MODE)))
        log.debug(LogMsg)
        log.cflush()
        self.setConnectionTimeout(5)
        self.sendMsg("\r")
        time.sleep(1)

        # stop onie discovery messages
        self.sendMsg("onie-stop")
        self.sendMsg("\r")
        time.sleep(1)
        log.cflush()

        # set ONIE boot mode
        LogMsg = ("\r\nSet Onie boot mode: %s..." % (str(ONIE_BOOT_MODE)))
        log.debug(LogMsg)
        log.cflush()
        if ONIE_BOOT_MODE == Const.ONIE_RESCUE_MODE:
            self.sendMsg("onie-boot-mode -o rescue")
        elif ONIE_BOOT_MODE == Const.ONIE_UNINSTALL_MODE:
            self.sendMsg("onie-boot-mode -o uninstall")
        elif ONIE_BOOT_MODE == Const.ONIE_UPDATE_MODE:
            self.sendMsg("onie-boot-mode -o update")
        elif ONIE_BOOT_MODE == Const.ONIE_EMBED_MODE:
            self.sendMsg("onie-boot-mode -o embed")
        else:  # default onie install mode
            self.sendMsg("onie-boot-mode -o install")
        self.sendMsg("\r")
        time.sleep(1)
        mode_set = 0
        self.sendMsg("onie-boot-mode")
        self.sendMsg("\r")
        time.sleep(1)
        output2 = self.readMsg()
        if ONIE_BOOT_MODE == Const.ONIE_RESCUE_MODE:
            if "rescue" in output2:
                mode_set = 1
        elif ONIE_BOOT_MODE == Const.ONIE_UNINSTALL_MODE:
            if "uninstall" in output2:
                mode_set = 1
        elif ONIE_BOOT_MODE == Const.ONIE_UPDATE_MODE:
            if "update" in output2:
                mode_set = 1
        elif ONIE_BOOT_MODE == Const.ONIE_EMBED_MODE:
            if "embed" in output2:
                mode_set = 1
        else:  # default onie install mode
            if "install" in output2:
                mode_set = 1
        log.debug(output2)
        log.cflush()

        if mode_set == 0:
            LogMsg = ("\r\nFail to set Onie boot mode: %s" % (str(ONIE_BOOT_MODE)))
            LogMsg += "\r\nonieBootIntoOnieMode result: FAIL"
            log.debug(LogMsg)
            raise RuntimeError(LogMsg)

        # reboot system
        time.sleep(1)
        self.sendMsg("reboot")
        self.sendMsg("\r")
        try:
            output3 = self.readUntil("reboot")
            log.debug(output3)
        except Exception as err:
            LogMsg = "\r\nFail to reboot system."
            LogMsg += "\r\nonieBootIntoOnieMode result: FAIL"
            log.debug(LogMsg)
            raise RuntimeError(LogMsg)

        LogMsg = "\r\nonieBootIntoOnieMode result: PASS"
        log.debug(LogMsg)
        return LogMsg

    def waitForOnieBootUpPrompt(self, ONIE_BOOT_MODE, lastMsg):
        output1 = ''
        LogMsg = ''
        self.setConnectionTimeout(60)
        # wait for Onie boot up
        OnieBootPrompt = "activate this console"
        try:
            output1 = self.readUntil(OnieBootPrompt)
            output1 += "\r\nSuccessfully booted up Onie."
            log.debug(output1)
            log.cflush()
        except Exception as err:
            LogMsg = output1
            LogMsg += "\r\nFail to boot up to Onie."
            LogMsg += "\r\nwaitForOnieBootUpPrompt result: FAIL"
            log.debug(LogMsg)
            raise RuntimeError(LogMsg)

        # wait for onie mode string
        if ONIE_BOOT_MODE == Const.ONIE_RESCUE_MODE:
            cmdStrMode = "Rescue Mode"
        elif ONIE_BOOT_MODE == Const.ONIE_UNINSTALL_MODE:
            cmdStrMode = "Uninstall Mode"
        elif ONIE_BOOT_MODE == Const.ONIE_UPDATE_MODE:
            cmdStrMode = "Update Mode"
        elif ONIE_BOOT_MODE == Const.ONIE_EMBED_MODE:
            cmdStrMode = "Embed Mode"
        else:  # default onie install mode
            cmdStrMode = "Install Mode"
        outputMode = ''
        match = re.search(cmdStrMode, lastMsg)
        if match:
            outputMode = ("\r\nSuccessfully found Onie %s" % (cmdStrMode))
            log.debug(outputMode)
            log.cflush()
        else:
            match = re.search(cmdStrMode, output1)
            if match:
                outputMode = ("\r\nSuccessfully found Onie %s" % (cmdStrMode))
                log.debug(outputMode)
                log.cflush()
            else:
                LogMsg = outputMode
                LogMsg += ("\r\nFail to wait for Onie %s" % (cmdStrMode))
                LogMsg += "\r\nwaitForOnieBootUpPrompt result: FAIL"
                log.debug(LogMsg)
                raise RuntimeError(LogMsg)

        # wait for Onie boot prompt
        output2 = ''
        OnieCmdPrompt = self.promptOnie
        self.sendMsg('\r')
        try:
            output2 = self.readUntil(OnieCmdPrompt)
            output2 += "\r\nSuccessfully enter into Onie prompt."
            log.debug(output2)
            log.cflush()
        except Exception as err:
            LogMsg = output2
            LogMsg += "\r\nFail to enter into Onie prompt."
            LogMsg += "\r\nwaitForOnieBootUpPrompt result: FAIL"
            log.debug(LogMsg)
            raise RuntimeError(LogMsg)

        return output2

    def loginToDiagOS(self):
        log.debug("Entering Device class procedure: loginToDiagOS")
        output1 = ''
        LogMsg = ''
        output = self.loginToOS(self.rootUserName, self.rootPassword, self.promptDiagOS)
        if "result: FAIL" in output:
            LogMsg = "\r\nloginToDiagOS result: FAIL"
            log.debug(LogMsg)
            raise RuntimeError(LogMsg)
        else:
            LogMsg = "\r\nloginToDiagOS result: PASS"
            log.debug(LogMsg)
            self.sendMsg('\r\n')
            time.sleep(1)
            output1 = self.readMsg()
            # return the prompt string
            return output1


    def loginToBMC(self):
        log.debug("Entering Device class procedure: loginToBMC")
        output1 = ''
        LogMsg = ''
        output = self.loginToOS(self.bmcUserName, self.bmcPassword, self.promptBmc)
        if "result: FAIL" in output:
            LogMsg = "\r\nloginToBMC result: FAIL"
            log.debug(LogMsg)
            raise RuntimeError(LogMsg)
        else:
            LogMsg = "\r\nloginToBMC result: PASS"
            log.debug(LogMsg)
            self.sendMsg('\r\n')
            time.sleep(1)
            output1 = self.readMsg()
            # return the prompt string
            return output1

    def loginToOS(self, Username, Password, OSprompt):
        log.debug("Entering Device class procedure: loginToOS")
        print('Username is:',Username)
        print('Password is',Password)
        print('OSprompt is',OSprompt)
        self.setConnectionTimeout(5)

        output = ''
        LogMsg = ("\r\nLogging in to OS...")
        self.sendMsg("\r\n")
        try:
            # wait for login prompt and send username to login to OS
            output = self.readUntil('login:')
            LogMsg += (output + ' ' + Username)
            self.sendMsg(Username)
            self.sendMsg('\r')
        except Exception as err:
            LogMsg += "\r\nError: Unable to wait for login prompt."
            LogMsg += "\r\nloginToOS login result: FAIL"
            log.debug(LogMsg)
            raise RuntimeError(LogMsg)

        output = ''
        try:
            # wait for password prompt and send password
            output = self.readUntil("Password:")
            LogMsg += (output + ' ' + Password)
            self.sendMsg(Password)
            self.sendMsg('\r')
        except Exception as err:
            LogMsg += "\r\nError: Invalid user name."
            LogMsg += "\r\nloginToOS login result: FAIL"
            log.debug(LogMsg)
            raise RuntimeError(LogMsg)

        LogMsg1 = ''
        output = ''
        try:
            # wait for shell prompt
            output = self.read_until_regexp(OSprompt)
            LogMsg1 += output
            LogMsg1 += ("\r\nSuccessfully login to OS.")
        except Exception as err:
            LogMsg1 += LogMsg
            LogMsg1 += output
            LogMsg1 += "\r\nError: Invalid password."
            LogMsg1 += "\r\nloginToOS login result: FAIL"
            log.debug(LogMsg1)
            raise RuntimeError(LogMsg1)
            return LogMsg1

        LogMsg += LogMsg1
        LogMsg += "\r\nloginToOS login result: PASS"
        return LogMsg

    def bootIntoDiagOS(self):
        log.debug("Entering Device class procedure: bootIntoDiagOS")
        self.setConnectionTimeout(5)
        # check whether at DiagOS login prompt
        self.sendMsg("\r\n")
        time.sleep(1)
        LogMsg = ''
        output = self.readMsg()
        if "login:" in output:
            # login to DiagOS first
            output = self.loginToDiagOS()
            if "result: FAIL" in output:
                LogMsg = "\r\nFail to login to DiagOS."
                LogMsg = "\r\nbootIntoOnieMode result: FAIL"
                log.debug(LogMsg)
                raise RuntimeError(LogMsg)
            else:
                self.currentBootMode = Const.BOOT_MODE_DIAGOS
        # get boot mode
        self.currentBootMode = self.getBootMode(output)
        if self.currentBootMode == Const.BOOT_MODE_DIAGOS:
            LogMsg = ("\r\nDetect boot mode: %s" % (str(self.currentBootMode)))
            LogMsg += "\r\nbootIntoDiagOS result: PASS"
            log.debug(LogMsg)
            return LogMsg
        elif self.currentBootMode == Const.BOOT_MODE_ONIE:
            LogMsg = ("\r\nDetect boot mode: %s" % (str(self.currentBootMode)))
            log.debug(LogMsg)
            log.cflush()
            self.setConnectionTimeout(5)
            self.sendMsg("\r")
            time.sleep(1)
            # stop onie discovery messages
            self.sendMsg("onie-stop")
            self.sendMsg("\r")
            time.sleep(1)
            LogMsg += "\r\nRebooting device to boot into DiagOS..."
            log.debug(LogMsg)
            log.cflush()

            # reboot system
            self.sendMsg("reboot")
            self.sendMsg('\r')
            try:
                output = self.readUntil("reboot")
                log.debug(output)
            except Exception as err:
                LogMsg = "\r\nFail to reboot system from ONIE."
                LogMsg += "\r\nbootIntoDiagOS result: FAIL"
                log.debug(LogMsg)
                raise RuntimeError(LogMsg)
        else:
            LogMsg = ("\r\nDetect boot mode: %s" % (str(self.currentBootMode)))
            LogMsg += "\r\nPower cycling device to boot into DiagOS..."
            log.debug(LogMsg)
            # power cycle system
            output = self.powerCycle()
            if "result: FAIL" in output:
                LogMsg = "\r\nbootIntoDiagOS result: FAIL"
                log.debug(LogMsg)
                raise RuntimeError(LogMsg)

        # wait for grub prompt first if system reboot or power cycle
        output1 = self.waitForGrubPrompt()
        if "result: FAIL" in output1:
            LogMsg = "\r\nbootIntoDiagOS result: FAIL"
            log.debug(LogMsg)
            raise RuntimeError(LogMsg)

        # boot into Diag OS from grub
        output2 = self.grubBootIntoDiagOS()
        if "result: FAIL" in output2:
            LogMsg = "\r\nbootIntoDiagOS result: FAIL"
            log.debug(LogMsg)
            raise RuntimeError(LogMsg)

        # update currentBootMode
        self.setCurrentBootMode(Const.BOOT_MODE_DIAGOS)
        LogMsg = "\r\nbootIntoDiagOS result: PASS"
        log.debug(LogMsg)
        time.sleep(1)
        return LogMsg

    def bootIntoBios(self):
        log.debug("Entering Device class procedure: bootIntoBios")
        # To be implemented
        pass

    # different device have different way to get OS version, but here give a default implementation
    def displayDiagOSVersion(self):
        log.debug("Entering Device class procedure: displayDiagOSVersion")
        version = self.sendCmd("uname -a", self.promptDiagOS)  # need replace it with minipack2's
        LogMsg = "Version:\r\n"
        LogMsg += version
        log.debug(LogMsg)
        time.sleep(1)
        return version

    def displayOSVersion(self):
        log.debug("Entering Device class procedure: displayDiagOSVersion")
        version = self.sendCmd("uname -a", self.getPrompt())
        LogMsg = "Version:\r\n"
        LogMsg += version
        log.debug(LogMsg)
        time.sleep(1)
        return version

    def waitForGrubPrompt(self):
        log.debug("Entering Device class procedure: waitForGrubPrompt")
        self.setConnectionTimeout(90)
        output = self.readUntil("command-line")
        log.debug(output)
        enter_grub_prompt = 0
        self.setConnectionTimeout(1)
        for count in range(1, 50):
            # send 'esc' character to stop grub autoboot
            self.sendMsg('\033')
            # send 'c' character to enter grub prompt
            self.sendMsg('c')
            output1 = ''
            try:
                output1 = self.readUntil(self.promptGrub)
                enter_grub_prompt = 1
                log.debug(output1)
                break
            except Exception as err:
                continue

        LogMsg = ''
        if enter_grub_prompt == 0:
            LogMsg = "waitForGrubPrompt result: FAIL"
            log.debug(LogMsg)
            raise RuntimeError(LogMsg)
        else:
            LogMsg = "waitForGrubPrompt result: PASS"
            log.debug(LogMsg)

        time.sleep(1)
        return LogMsg

    def waitForGrubPromptImmediate(self):
        enter_grub_prompt = 0
        self.setConnectionTimeout(1)
        for count in range(1, 50):
            # send 'esc' character to stop grub autoboot
            self.sendMsg('\033')
            # send 'c' character to enter grub prompt
            self.sendMsg('c')
            output1 = ''
            try:
                output1 = self.readUntil(self.promptGrub)
                enter_grub_prompt = 1
                log.debug(output1)
                break
            except Exception as err:
                continue

        LogMsg = ''
        if enter_grub_prompt == 0:
            LogMsg = "waitForGrubPromptImmediate result: FAIL"
            log.debug(LogMsg)
            raise RuntimeError(LogMsg)
        else:
            LogMsg = "waitForGrubPromptImmediate result: PASS"
            log.debug(LogMsg)

        time.sleep(1)
        return LogMsg

    def grubSendMsg(self, grubMsg):
        self.setConnectionTimeout(10)
        LogMsg = ''
        self.sendMsg('\r')
        for retry_count in range(1, 10):
            time.sleep(1)
            for ch in grubMsg:
                self.sendMsg(ch)
                time.sleep(0.1)
            self.sendMsg('\r')
            time.sleep(3)
            try:
                output = self.readMsg()
                if "error" in output:
                    # retry
                    LogMsg = output
                    LogMsg += ("\n          Retry[%s]...\n" % (retry_count))
                    log.debug(LogMsg)
                    self.sendMsg('\r')
                    time.sleep(0.5)
                    output1 = self.readMsg()
                    continue
                else:
                    break
            except Exception as err:
                LogMsg = output
                LogMsg += "\r\nFail to read grub message."
                LogMsg += "\r\ngrubSendMsg result: FAIL"
                log.debug(LogMsg)
                raise RuntimeError(LogMsg)
        if retry_count == 10:
            LogMsg = output
            LogMsg += "\r\nMaximum retry exceeded."
            LogMsg += "\r\ngrubSendMsg result: FAIL"
            log.debug(LogMsg)
            raise RuntimeError(LogMsg)

        outputMsg = output
        return outputMsg

    def grubSendCmd(self, grubCmd):
        self.setConnectionTimeout(10)
        LogMsg = ''
        self.sendMsg('\r')
        for retry_count in range(1, 10):
            time.sleep(1)
            for ch in grubCmd:
                self.sendMsg(ch)
                time.sleep(0.1)
            self.sendMsg('\r')
            time.sleep(3)
            try:
                output = self.readUntil(self.promptGrub)
                if "error" in output:
                    # retry
                    LogMsg = output
                    LogMsg += ("\n          Retry[%s]...\n" % (retry_count))
                    log.debug(LogMsg)
                    log.cflush()
                    self.sendMsg('\r')
                    time.sleep(0.5)
                    output1 = self.readUntil(self.promptGrub)
                    continue
            except Exception as err:
                LogMsg = "\r\nFail to wait for grub prompt."
                LogMsg += "\r\ngrubSendCmd result: FAIL"
                log.debug(LogMsg)
                raise RuntimeError(LogMsg)
            # check for error again as grub error message might come after grub prompt
            outputMsg = self.readMsg()
            if "error" in outputMsg:
                # retry
                LogMsg = outputMsg
                LogMsg += ("\r\n          Retry[%s]...\r\n" % (retry_count))
                log.debug(LogMsg)
                self.sendMsg('\r')
                time.sleep(0.5)
                outputMsg1 = self.readUntil(self.promptGrub)
                continue
            else:
                break
        if retry_count == 10:
            LogMsg = output
            LogMsg += "\r\nMaximum retry exceeded."
            LogMsg += "\r\ngrubSendCmd result: FAIL"
            log.debug(LogMsg)
            raise RuntimeError(LogMsg)

        outputMsg = "\r\ngrub> "
        outputMsg += grubCmd
        if "clear" in grubCmd:
            outputMsg += output
        else:
            outputMsg += "\r\n"
            output = output.strip()
            outputMsg += output

        return outputMsg

    def grubSendBlankLines(self, numLines):
        # send some blank lines to grub to prevent messages get overwritten at console
        rcmdStr = ''
        for rcount in range(1, numLines):
            rcmdStr += "\r\n"
        routput = self.grubSendCmd(rcmdStr)
        # trim trailing "grub>" string
        routput = routput[:-5]
        log.debug(routput)
        log.cflush()

    def grubBootIntoDiagOS(self):
        log.debug("Entering Device class procedure: grubBootIntoDiagOS")
        self.setConnectionTimeout(30)

        LogMsg = ''
        # clear grub screen
        clr_cmdStr = "clear"
        clr_output = self.grubSendCmd(clr_cmdStr)
        # trim trailing "grub>" string
        clr_output = clr_output[:-5]
        log.debug(clr_output)
        log.cflush()
        if "result: FAIL" in clr_output:
            LogMsg = "\r\nFail to clear grub screen."
            LogMsg += "\r\ngrubBootIntoDiagOS result: FAIL"
            log.debug(LogMsg)
            raise RuntimeError(LogMsg)

        self.grubSendBlankLines(5)

        # prepare to search root HDD and EDA-DIAG parition
        cmdStr = "search --no-floppy --label --set=root EDA-DIAG"
        output = self.grubSendCmd(cmdStr)
        if "result: FAIL" in output:
            LogMsg = output
            LogMsg += "\r\nFail to search root EDA-DIAG partition."
            LogMsg += "\r\ngrubBootIntoDiagOS result: FAIL"
            log.debug(LogMsg)
            raise RuntimeError(LogMsg)
        else:
            # trim trailing "grub>" string
            output = output[:-5]
            log.debug(output)
            log.cflush()

        self.grubSendBlankLines(5)

        # search root HDD and EDA-DIAG partition
        cmdStr1 = "echo \x24root"
        output1 = self.grubSendMsg(cmdStr1)
        match = re.search('hd\d+,gpt(\d+)', output1)
        if match:
            # root HDD and EDA-DIAG partition found
            rootStr = match.group(0)
            partStr = match.group(1)
            log.debug(output1)
            log.cflush()
        else:
            LogMsg = output1
            LogMsg += "\r\nFail get root HDD and partition"
            LogMsg += "\r\ngrubBootIntoDiagOS result: FAIL"
            log.debug(LogMsg)
            raise RuntimeError(LogMsg)

        self.grubSendBlankLines(5)

        # prepare Linux kernel boot command
        cmdStr2 = ("linux (%s)/boot/ngos.linux quiet console=ttyS0,115200 root=/dev/mmcblk0p%s rw" % (rootStr, partStr))
        output2 = self.grubSendCmd(cmdStr2)
        if "result: FAIL" in output2:
            LogMsg = output2
            LogMsg += "\r\nFail to send Linux kernel boot string"
            LogMsg += "\r\ngrubBootIntoDiagOS result: FAIL"
            log.debug(LogMsg)
            raise RuntimeError(LogMsg)
        else:
            # trim trailing "grub>" string
            output2 = output2[:-5]
            log.debug(output2)
            log.cflush()

        self.grubSendBlankLines(5)

        # prepare Linux initrd boot command
        cmdStr3 = ("initrd (%s)/boot/ngos.initrd" % rootStr)
        output3 = self.grubSendCmd(cmdStr3)
        if "result: FAIL" in output3:
            LogMsg = output3
            LogMsg = "\r\nFail to send Linux initrd boot string"
            LogMsg += "\r\ngrubBootIntoDiagOS result: FAIL"
            log.debug(LogMsg)
            raise RuntimeError(LogMsg)
        else:
            # trim trailing "grub>" string
            output3 = output3[:-5]
            log.debug(output3)
            log.cflush()

        self.grubSendBlankLines(5)

        # boot to DiagOS
        cmdStr4 = "boot"
        output4 = self.grubSendMsg(cmdStr4)
        if "result: FAIL" in output4:
            LogMsg = output4
            LogMsg = "\r\nFail to send Linux boot command"
            LogMsg += "\r\ngrubBootIntoDiagOS result: FAIL"
            log.debug(LogMsg)
            raise RuntimeError(LogMsg)
        else:
            log.debug(output4)
            log.cflush()

        # wait for DiagOS boot prompt
        output5 = ''
        DiagOSBootPrompt = self.promptDiagOS
        # trim last 3 character ':~#'
        DiagOSBootPrompt = DiagOSBootPrompt[:-3]
        try:
            output5 = self.read_until_regexp(DiagOSBootPrompt)
            output5 += "\r\nSuccessfully booted up to DiagOS."
            log.debug(output5)
            log.cflush()
        except Exception as err:
            LogMsg = output5
            LogMsg += "\r\nFail to boot up to DiagOS."
            LogMsg += "\r\ngrubBootIntoDiagOS result: FAIL"
            log.debug(LogMsg)
            raise RuntimeError(LogMsg)

        # login to DiagOS
        output6 = self.loginToDiagOS()
        if "result: FAIL" in output6:
            LogMsg = "\r\nFail to login to DiagOS."
            LogMsg = "\r\ngrubBootIntoDiagOS result: FAIL"
            log.debug(LogMsg)
            raise RuntimeError(LogMsg)

        output7 = "\r\ngrubBootIntoDiagOS result: PASS"
        LogMsg += output7
        log.debug(LogMsg)
        log.cflush()
        return output7

    def grubBootIntoOnieEnv(self):
        log.debug("Entering Device class procedure: grubBootIntoOnieEnv")
        LogMsg = ''
        output = self.grubBootIntoOnie(Const.ONIE_DEFAULT_MODE)
        if "result: FAIL" in output:
            LogMsg = "\r\nFail to boot into Onie environment."
            LogMsg += "\r\ngrubBootIntoOnieEnv result: FAIL"
            log.debug(LogMsg)
            raise RuntimeError(LogMsg)
        LogMsg = "\r\ngrubBootIntoDiagOSEnv result: PASS"
        log.debug(LogMsg)
        log.cflush()
        return LogMsg

    def grubBootIntoOnie(self, ONIE_MODE):
        log.debug("Entering Device class procedure: grubBootIntoOnie")
        self.setConnectionTimeout(30)
        LogMsg = ''

        # clear grub screen
        clr_cmdStr = "clear"
        clr_output = self.grubSendCmd(clr_cmdStr)
        # trim trailing "grub>" string
        clr_output = clr_output[:-5]
        log.debug(clr_output)
        log.cflush()
        if "result: FAIL" in clr_output:
            LogMsg = "\r\nFail to clear grub screen."
            LogMsg += "\r\ngrubBootIntoOnie result: FAIL"
            log.debug(LogMsg)
            raise RuntimeError(LogMsg)

        cmdStr = "setparams \x27ONIE\x27"
        output = self.grubSendCmd(cmdStr)
        if "result: FAIL" in output:
            LogMsg = output
            LogMsg += "\r\nFail to set ONIE parameter"
            LogMsg += "\r\ngrubBootIntoOnie result: FAIL"
            log.debug(LogMsg)
            raise RuntimeError(LogMsg)
        else:
            # trim trailing "grub>" string
            output = output[:-5]
            log.debug(output)
            log.cflush()

        self.grubSendBlankLines(5)

        cmdStr1 = "search --no-floppy --label --set=root \x27EFI System\x27"
        output1 = self.grubSendCmd(cmdStr1)
        if "result: FAIL" in output1:
            LogMsg = output1
            LogMsg += "\r\nFail to search root EFI partition."
            LogMsg += "\r\ngrubBootIntoOnie result: FAIL"
            log.debug(LogMsg)
            raise RuntimeError(LogMsg)
        else:
            # trim trailing "grub>" string
            output1 = output1[:-5]
            log.debug(output1)
            log.cflush()

        self.grubSendBlankLines(5)

        # prepare EFI chainloader
        cmdStr2 = "chainloader /EFI/onie/grubx64.efi"
        output2 = self.grubSendCmd(cmdStr2)
        if "result: FAIL" in output2:
            LogMsg = output2
            LogMsg += "\r\nFail to set EFI chainloader"
            LogMsg += "\r\ngrubBootIntoOnie result: FAIL"
            log.debug(LogMsg)
            raise RuntimeError(LogMsg)
        else:
            # trim trailing "grub>" string
            output2 = output2[:-5]
            log.debug(output2)
            log.cflush()

        self.grubSendBlankLines(5)

        # boot to OnieOS
        cmdStr3 = "boot"
        output3 = self.grubSendMsg(cmdStr3)
        if "result: FAIL" in output3:
            LogMsg = output3
            LogMsg = "\r\nFail to send Linux boot command"
            LogMsg += "\r\ngrubBootIntoOnie result: FAIL"
            log.debug(LogMsg)
            raise RuntimeError(LogMsg)
        else:
            log.debug(output3)
            log.cflush()

        output4 = self.waitForGrubPromptImmediate()
        if "result: FAIL" in output4:
            LogMsg = "\r\nbootIntoOnieMode result: FAIL"
            log.debug(LogMsg)
            raise RuntimeError(LogMsg)

        # clear grub screen
        clr_cmdStr = "clear"
        clr_output = self.grubSendCmd(clr_cmdStr)
        # trim trailing "grub>" string
        clr_output = clr_output[:-5]
        log.debug(clr_output)
        log.cflush()
        if "result: FAIL" in clr_output:
            LogMsg = "\r\nFail to clear grub screen."
            LogMsg += "\r\ngrubBootIntoOnie result: FAIL"
            log.debug(LogMsg)
            raise RuntimeError(LogMsg)

        # set ONIE parameter
        if ONIE_MODE == Const.ONIE_RESCUE_MODE:
            cmdStr = "setparams \x27ONIE: Rescue\x27"
            cmdStr1 = "onie_debugargs=\x22\x22"
            cmdStr2 = "onie_rescue"
        elif ONIE_MODE == Const.ONIE_UNINSTALL_MODE:
            cmdStr = "setparams \x27ONIE: Uninstall OS\x27"
            cmdStr1 = "onie_debugargs=\x22\x22"
            cmdStr2 = "onie_uninstall"
        elif ONIE_MODE == Const.ONIE_UPDATE_MODE:
            cmdStr = "setparams \x27ONIE: Update ONIE\x27"
            cmdStr1 = "onie_debugargs=\x22\x22"
            cmdStr2 = "onie_update"
        elif ONIE_MODE == Const.ONIE_EMBED_MODE:
            cmdStr = "setparams \x27ONIE: Embed ONIE\x27"
            cmdStr1 = "onie_debugargs=\x22\x22"
            cmdStr2 = "onie_embed"
        else:  # default onie install mode
            cmdStr = "setparams \x27ONIE: Install OS\x27"
            cmdStr1 = "onie_debugargs=\x22\x22"
            cmdStr2 = "onie_install"

        output5 = self.grubSendCmd(cmdStr)
        if "result: FAIL" in output5:
            LogMsg = output5
            LogMsg += "\r\nFail to set ONIE parameter"
            LogMsg += "\r\ngrubBootIntoOnie result: FAIL"
            log.debug(LogMsg)
            raise RuntimeError(LogMsg)
        else:
            # trim trailing "grub>" string
            output = output5[:-5]
            log.debug(output)
            log.cflush()

        self.grubSendBlankLines(5)

        output6 = self.grubSendCmd(cmdStr1)
        if "result: FAIL" in output6:
            LogMsg = output6
            LogMsg += "\r\nFail to set ONIE parameter"
            LogMsg += "\r\ngrubBootIntoOnie result: FAIL"
            log.debug(LogMsg)
            raise RuntimeError(LogMsg)
        else:
            # trim trailing "grub>" string
            output = output6[:-5]
            log.debug(output)
            log.cflush()

        self.grubSendBlankLines(5)

        lastMsg = self.grubSendMsg(cmdStr2)
        if "result: FAIL" in lastMsg:
            LogMsg = lastMsg
            LogMsg += "\r\nFail to set ONIE parameter"
            LogMsg += "\r\ngrubBootIntoOnie result: FAIL"
            log.debug(LogMsg)
            raise RuntimeError(LogMsg)
        else:
            log.debug(lastMsg)
            log.cflush()

        # wait for ONIE boot up
        output7 = self.waitForOnieBootUpPrompt(ONIE_MODE, lastMsg)
        if "result: FAIL" in output7:
            LogMsg = "\r\nFail to wait for Onie boot up prompt."
            LogMsg += "\r\ngrubBootIntoOnie result: FAIL"
            log.debug(LogMsg)
            raise RuntimeError(LogMsg)

        output8 = "\r\ngrubBootIntoOnie result: PASS"
        log.debug(output8)
        log.cflush()
        return output8

    def getCurrentPromptStr(self):
        if self.currentBootMode == Const.BOOT_MODE_ONIE:
            return self.promptOnie
        elif self.currentBootMode == Const.BOOT_MODE_BMC:
            return self.promptBmc
        elif self.currentBootMode == Const.BOOT_MODE_DIAGOS:
            return self.promptDiagOS
        elif self.currentBootMode == Const.BOOT_MODE_GRUB:
            return self.promptGrub
        elif self.currentBootMode == Const.BOOT_MODE_CENTOS:
            return self.promptDiagOS
        elif self.currentBootMode == Const.BOOT_MODE_OPENBMC:
            return self.promptBmc
        else:
            return None

    def getCurrentPromptMode(self):
        if self.currentBootMode == Const.BOOT_MODE_ONIE:
            return "onie"
        elif self.currentBootMode == Const.BOOT_MODE_BMC:
            return "openbmc"  # openbmc and bmc should be same mode !
        elif self.currentBootMode == Const.BOOT_MODE_DIAGOS:
            return "diagos"
        elif self.currentBootMode == Const.BOOT_MODE_GRUB:
            return "grub"
        elif self.currentBootMode == Const.BOOT_MODE_CENTOS:
            return "centos"
        elif self.currentBootMode == Const.BOOT_MODE_OPENBMC:
            return "openbmc"
        else:
            return None

    def checkForLoginPrompt(self, message):
        output = None
        altBmcLoginPrompt = 'None'
        loginStr = self.loginPromptBmc
        if re.search('.', loginStr):
            # strip off the hostname in login prompt
            slist = loginStr.split('.')
            str1 = str(slist[0])
            # alternate bmc login prompt string
            altBmcLoginPrompt = (str1 + ' ' + 'login:')

        if "login:" in str(message):
            self.flush()
            altBmcLoginPrompt = 'None'
            loginStr = self.loginPromptBmc
            if re.search('.', loginStr):
                # strip off the hostname in login prompt
                slist = loginStr.split('.')
                str1 = str(slist[0])
                # alternate bmc login prompt string
                altBmcLoginPrompt = (str1 + ' ' + 'login:')

            if re.search(self.loginPromptBmc, message) or re.search(altBmcLoginPrompt, message):
                output = self.loginToBMC()
                log.debug(output)
            else:
                output = self.loginToDiagOS()
                log.debug(output)

        elif "Password:" in str(message):
            self.flush()
            self.sendMsg("\r\n")
            time.sleep(5)
            output = self.readMsg()
            if re.search(self.loginPromptBmc, message) or re.search(altBmcLoginPrompt, message):
                output = self.loginToBMC()
                log.debug(output)
            else:
                output = self.loginToDiagOS()
                log.debug(output)

        return output

    @deprecated("""Do not recommend to use this API, it have bugs:
                     1. can't get the whole result of a cmd sometime.
                     2. break a output line sometime. """)
    def execute(self, cmd, mode=None, exe_timeout=60, checkLoginPrompt=True):
        log.debug('Entering Device execute with args : %s\n' % (str(locals())))
        output = ''
        output1 = ''
        output2 = ''
        LogMsg = ''

        if mode is not None:
            log.debug("execute mode=%s" % mode)
            MODE_STR = mode.upper()
            output = self.getPrompt(mode, timeout=exe_timeout)
            currentBootMode = self.getBootMode(output)

            LogMsg = ("\r\nrequested boot mode: %s" % MODE_STR)
            LogMsg += ("\r\ncurrent boot mode: %s" % currentBootMode)
            log.debug(LogMsg)
        else:
            log.debug("execute mode=None")
            output = self.getPrompt(mode=None, timeout=exe_timeout)
            currentBootMode = self.getBootMode(output)
            LogMsg = ("\r\ncurrent boot mode: %s" % currentBootMode)
            log.debug(LogMsg)

        currentPromptStr = self.getCurrentPromptStr()
        log.debug("\r\nwait for prompt string: %s, timeout: %s" % (currentPromptStr, exe_timeout))

        # send commands
        for linestr in cmd.splitlines():
            log.debug("\r\ncmd: [%s]\n" % linestr)
            self.setConnectionTimeout(exe_timeout)
            output1 = ''
            output2 = ''
            output3 = ''
            LogMsg = ''
            cnt = exe_timeout
            found_prompt = 0
            self.flush()
            time.sleep(1)
            self.sendMsg(linestr)
            self.sendMsg("\r\n")
            time.sleep(1)
            cnt = int(cnt / 2)
            output1 = self.readMsg()
            output2 = output1.strip()
            if len(output2) != 0:
                output += output1
            time.sleep(1)
            self.sendMsg("\r\n")
            self.setConnectionTimeout(2)
            # update display at 2 seconds interval while waiting for prompt
            for i in range(1, cnt):
                output1 = self.readMsg()
                output2 = output1.strip()
                if len(output2) == 0:
                    time.sleep(2)
                    continue

                output += output1
                log.debug("%s\n" % output2)
                if checkLoginPrompt:
                    output3 = self.checkForLoginPrompt(output2)
                    if output3 is not None:
                        found_prompt = 1
                        output += output2
                        break

                if re.search(self.promptDiagOS, output2):
                    found_prompt = 1
                    log.debug("\r\nDetected %s" % self.promptDiagOS)
                    break

                elif re.search(self.promptBmc, output2):
                    found_prompt = 1
                    log.debug("\r\nDetected %s" % self.promptBmc)
                    break

                else:
                    time.sleep(2)
                    continue

            if found_prompt == 0:
                break

        if self.enable_terminal_log_file != '0':
            self.send_output_to_log_file(output)

        if found_prompt == 0:
            LogMsg = "\r\nexecute result1: FAIL"
            log.debug(LogMsg)
            raise RuntimeError(LogMsg)

        return output

    def getPrompt(self, mode=None, timeout=60, idleTimeout=60, logFile='None'):
        """" this function used to change mode, i.e. get into the expected prompt/mode"""

        log.debug('Entering procedure getPrompt with args : %s\n' % (str(locals())))
        output = ''
        outStr = ''
        LogMsg = ''
        self.flush()
        self.sendMsg('\r\n')
        altBmcLoginPrompt = 'None'
        loginStr = self.loginPromptBmc
        if re.search('.', loginStr):
            # strip off the hostname in login prompt
            slist = loginStr.split('.')
            str1 = str(slist[0])
            # alternate bmc login prompt string
            altBmcLoginPrompt = (str1 + ' ' + 'login:')
        promptList = [self.promptGrub, self.promptOnie, self.promptDiagOS, self.promptBmc, self.loginPromptDiagOS,
                      self.loginPromptBmc, altBmcLoginPrompt, Const.promptPython3, self.promptSdk, self.unidiagPrompt]
        # promptList = [self.promptGrub, self.promptOnie, self.promptDiagOS, self.promptBmc, self.loginPromptDiagOS, self.loginPromptBmc, altBmcLoginPrompt]
        self.setConnectionTimeout(timeout)
        patternList = re.compile('|'.join(promptList))
        LogMsg = ''
        try:
            try:
                output = self.read_until_regexp(patternList)
            except:
                self.sendMsg('\x03')
                output += self.read_until_regexp(patternList)
            log.debug(output)
            outStr += output
        except:
            LogMsg = "\r\ngetPrompt result: FAIL1"
            log.debug(LogMsg)
            errMsg = "\r\nCannot get prompt within %d seconds" % timeout
            raise RuntimeError(errMsg)

        if re.search(self.promptSdk, outStr):  # SDK prompt
            # Issue 'exit' command to exit SDK prompt to diagOS prompt
            log.debug("\nDetected SDK prompt...Exit...\n")
            self.sendMsg("exit")
            self.sendMsg("\r\n")
            time.sleep(3)
            try:
                try:
                    output = self.read_until_regexp(patternList)
                except:
                    self.sendMsg('\x03')
                    output += self.read_until_regexp(patternList)
                log.debug(output)
                outStr += output
            except:
                LogMsg = "\r\ngetPrompt result: FAIL4"
                log.debug(LogMsg)
                errMsg = "\r\nCannot get prompt within %d seconds" % timeout
                raise RuntimeError(errMsg)

        if re.search(self.promptGrub, outStr):  # grub prompt
            log.debug("\nDetected grub prompt.\n")
            self.currentBootMode = Const.BOOT_MODE_GRUB
        elif re.search(self.promptOnie, outStr):  # onie prompt
            log.debug("\nDetected onie prompt.\n")
            self.currentBootMode = Const.BOOT_MODE_ONIE
        elif re.search(self.promptDiagOS, outStr):  # diagOS prompt
            if 'sonic' in self.os:
                log.debug("\nDetected centos prompt.\n")
                self.currentBootMode = Const.BOOT_MODE_CENTOS
            else:
                log.debug("\nDetected diagos prompt.\n")
                self.currentBootMode = Const.BOOT_MODE_DIAGOS
        elif re.search(self.promptBmc, outStr):  # bmc prompt
            if 'sonic' in self.os:
                log.debug("\nDetected openbmc prompt.\n")
                self.currentBootMode = Const.BOOT_MODE_OPENBMC
            else:
                log.debug("\nDetected bmc prompt.\n")
                self.currentBootMode = Const.BOOT_MODE_BMC
        elif re.search(self.loginPromptDiagOS, outStr):  # diagOS login prompt
            log.debug("\nLogin to DiagOS.\n")
            currentPromptStr = self.loginToDiagOS()
            if 'sonic' in self.os:
                self.currentBootMode = Const.BOOT_MODE_CENTOS
            else:
                self.currentBootMode = Const.BOOT_MODE_DIAGOS
        elif re.search(self.loginPromptBmc, outStr) or re.search(altBmcLoginPrompt, outStr):  # bmc login prompt
            log.debug("\nLogin to BMC.\n")
            currentPromptStr = self.loginToBMC()
            if 'sonic' in self.os:
                self.currentBootMode = Const.BOOT_MODE_OPENBMC
            else:
                self.currentBootMode = Const.BOOT_MODE_BMC
        elif re.search(self.unidiagPrompt, outStr):             # Undiag prompt
            log.debug("\nDetected Unidag Prompt \n")
            for i in range(0,5):
                self.sendMsg('q\r')
                time.sleep(2)
                if self.read_until_regexp == 'exit':
                    self.sendMsg('\r')
                    log.success("Exited from Unidiag interface successfully.")
                    break
            self.currentBootMode = Const.BOOT_MODE_DIAGOS
        elif re.search(Const.promptPython3, outStr):
            log.debug("\nLogin to python3, will get back to centos mode soon.\n")
            self.sendMsg("\r")
            time.sleep(1)
            self.currentBootMode = Const.BOOT_MODE_PYTHON3
        else:
            log.debug("\nError in getPrompt. Unknown prompt.\n")

        if mode is not None:
            mode_str = mode.lower()
            currentPromptMode = self.getCurrentPromptMode()
            LogMsg = ("\r\nrequested promptStr: %s" % mode_str)
            LogMsg += ("\r\ncurrent prompt mode: %s" % currentPromptMode)
            log.debug(LogMsg)

            if currentPromptMode != mode_str:
                if "diagos" in mode_str:
                    output = self.bootIntoDiagOS()
                    modeStr = "DiagOS Mode"
                elif "onie install" in mode_str:
                    output = self.bootIntoOnieInstallMode()
                    modeStr = "Onie Install Mode"
                elif "onie rescue" in mode_str:
                    output = self.bootIntoOnieRescueMode()
                    modeStr = "Onie Rescue Mode"
                elif "centos" in mode_str:
                    output = self.switchToCpu()
                    modeStr = "CentOS Mode"
                elif "openbmc" in mode_str:
                    output = self.switchToBmc()
                    modeStr = "OpenBMC Mode"
                # To be implmented for other supported boot modes if any.
                else:
                    LogMsg = "\r\nUnknown requested boot prompt."
                    LogMsg += "\r\ngetPrompt result: FAIL2"
                    log.debug(LogMsg)
                    raise RuntimeError(LogMsg)

                outStr += output

        if self.enable_terminal_log_file != '0':
            if logFile != 'None':
                self.send_output_to_log_file(outStr, logFile)

        if mode is not None:
            if "result: FAIL" in output:
                LogMsg += output
                LogMsg += ("\r\nFail to enter %s mode." % modeStr)
                LogMsg += "\r\ngetPrompt result: FAIL3"
                log.debug(LogMsg)
                raise RuntimeError(LogMsg)

        self.sendMsg("\r\r")
        return self.getCurrentPromptStr()

    def raiseException(self, msg):
        raise RuntimeError(msg)

    def log_debug(self, msg):
        return log.debug(msg)

    def log_error(self, msg):
        return log.error(msg)

    def log_info(self, msg):
        return log.info(msg)

    def log_success(self, msg):
        return log.success(msg)

    def log_fail(self, msg):
        return log.fail(msg)

    def waitForLoginPrompt(self, mode, timeout, logFile='None'):
        log.debug("\r\nEntering procedure waitForLoginPrompt.")
        output = ''
        output1 = ''
        output2 = ''
        output3 = ''
        LogMsg = ''
        found = 0
        found_prompt = 0
        cnt = timeout
        self.flush()
        self.setConnectionTimeout(2)
        for i in range(1, cnt):
            time.sleep(1)
            output1 = self.readMsg()
            output2 = output1.strip()
            if len(output2) == 0:
                continue
            elif "Starting" in output1:
                found = 1
                output = output1
                log.debug(output1)
                break

        if found == 0:
            LogMsg = "\nError: Timeout waiting for system boot up. "
            LogMsg += "\nwaitForLoginPrompt result: FAIL"
            log.debug(LogMsg)
            raise RuntimeError(LogMsg)

        # wait for login prompt and perform login
        for i in range(1, cnt):
            output1 = self.readMsg()
            output2 = output1.strip()
            if len(output2) == 0:
                time.sleep(2)
                continue

            output += output1
            log.debug("%s" % output1)
            output2 = self.checkForLoginPrompt(output1)
            if output2 is not None:
                found_prompt = 1
                output += output2
                break

            elif re.search(self.promptDiagOS, output1):
                found_prompt = 1
                log.debug("%s" % self.promptDiagOS)
                break

            elif re.search(self.promptBmc, output1):
                found_prompt = 1
                log.debug("%s" % self.promptBmc)
                break

            else:
                time.sleep(1)
                continue

        if self.enable_terminal_log_file != '0':
            if logFile != 'None':
                self.send_output_to_log_file(output, logFile)

        if found_prompt == 0:
            LogMsg = "\nwaitForLoginPrompt result: FAIL"
            log.debug(LogMsg)
            raise RuntimeError(LogMsg)

        # switch to desired mode
        output3 = self.getPrompt(mode, timeout, logFile)
        output += output3

        log.debug("\r\nwaitForLoginPrompt result: PASS")

        return output

    def execute_local_cmd(self, cmd, timeout=10, return_errs=False):
        log.debug('\r\nexecute_local_cmd cmd[%s]' % cmd)
        output = ''
        errs = ''
        proc = Popen(cmd, stdout=PIPE, stderr=PIPE, shell=True, encoding='latin-1')
        try:
            # wait for process to complete
            output, errs = proc.communicate(timeout=timeout)
            log.debug(output)
        except Exception as err:
            # clean up if error occurs
            proc.kill()
            log.debug(output)
            raise RuntimeError(str(err))

        log.debug('\r\nSuccessfully execute_local_cmd cmd: [%s]' % cmd)
        if return_errs:
            return output, errs
        return output

    @classmethod
    def getDeviceObject(cls, deviceName):
        import DeviceMgr
        return DeviceMgr.getDevice(deviceName)
