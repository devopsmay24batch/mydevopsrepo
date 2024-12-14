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
import os, time
import re

from Session import Session
import Logger as log
import Const


class SessionDevice(Session):

    def __init__(self, deviceDict):
        super().__init__()

        log.debug("Entering SessionDevice class procedure: __init__")
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
        self.bmcIP = deviceDict['managementIP']
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
        self.promptSdk = 'BCM.0>'
        self.cpuIP = ""
        self.enable_terminal_log_file = '0'
        self.currentBootMode = None
        self.esmbBmcIP=deviceDict.get('esmbManagementIP')
    def set_terminal_log_file(self, set_flag):
        if set_flag == '0':
            log.debug("Disable terminal log file feature.")
        else:
            log.debug("Enable terminal log file feature.")

        self.enable_terminal_log_file = set_flag


    def loginCpu(self):
        log.debug("Entering SessionDevice class procedure: login")
        self.connect(self.rootUserName, self.bmcIP)
        self.loginToBMC()
        self.getPrompt(Const.BOOT_MODE_CENTOS)

    def loginBmc(self):
        log.debug("Entering SessionDevice class procedure: loginBmc")
        try:
            self.connect(self.bmcUserName, self.bmcIP)
            self.loginToBMC()
        except Exception as err:
            cridential_changed = "REMOTE HOST IDENTIFICATION HAS CHANGED"
            cridential_changed_matched = re.search(cridential_changed, str(self.child.before))
            if self.protocol == Const.PROTOCOL_SSH and cridential_changed_matched:
                log.info("Warning: %s, remove it's host key from known_hosts file."%cridential_changed)
                os.system("ssh-keygen -R %s"%self.bmcIP)
                self.connect(self.bmcUserName, self.bmcIP)
                self.loginToBMC()
            else:
                raise Exception(str(err))
        self.getPrompt(Const.BOOT_MODE_OPENBMC)

    def loginToBMC(self):
        self.loginDev(self.bmcUserName, self.bmcPassword)

    def loginToDiagOS(self):
        self.loginDev(self.rootUserName, self.rootPassword)

    def trySwitchToBmc(self):
        log.debug("Entering SessionDevice class procedure: trySwitchToBmc")
        for key in self.keysSwitchToBmc:
            log.cprint(key)
            self.sendMsg(key)
            time.sleep(0.5)
        self.sendMsg("\r\n")
        time.sleep(1)
        self.sendMsg("\r\n")
        time.sleep(1)
        return ''

    def trySwitchToCpu(self):
        log.debug("Entering SessionDevice class procedure: trySwitchToCpu")
        for key in self.keysSwitchToCpu:
            log.cprint(key)
            self.sendMsg(key)
            time.sleep(0.5)
        self.sendMsg("\r\n")
        time.sleep(4)
        self.sendMsg("\r\n")
        return ''

    def switchToBmc(self):
        log.debug("Entering SessionDevice class procedure: switchToBmc")
        self.flush()
        self.trySwitchToBmc()
        out = self.receive(Const.MATCH_ALL,5)
        # if 'login' in out:
        #     self.loginToBMC()
        self.currentBootMode = self.getBootMode(out)
        log.cprint('currentBootMode: ' + self.currentBootMode)
        if self.currentBootMode not in [Const.BOOT_MODE_BMC, Const.BOOT_MODE_OPENBMC]:
            raise RuntimeError("In SessionDevice.switchToBmc, can't switch to BMC!")
        return ''


    def switchToCpu(self):
        log.debug("Entering SessionDevice class procedure: switchToCpu")
        self.flush()
        self.trySwitchToCpu()
        self.flush()
        self.sendCmd('')
        out = self.receive(Const.MATCH_ALL, 5)
        if 'login' in out:
            self.loginToDiagOS()
        self.currentBootMode = self.getBootMode(out)
        log.cprint('currentBootMode: ' + self.currentBootMode)
        if self.currentBootMode not in [Const.BOOT_MODE_DIAGOS, Const.BOOT_MODE_ONIE, Const.BOOT_MODE_CENTOS, Const.BOOT_MODE_PYTHON3]:
            raise RuntimeError("In SessionDevice.switchToCpu, can't switch to CPU!")
        return ''

    def getCurrentPromptMode(self):
        if self.currentBootMode == Const.BOOT_MODE_ONIE:
            return "onie"
        elif self.currentBootMode == Const.BOOT_MODE_BMC:
            return "bmc"
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

    def getBootMode(self, msgStr):
        log.debug('Entering SessionDevice class procedure getBootMode with args : %s\n' % (str(locals())))
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
        #login to diagOS first if currently at diagOS prompt
        if re.search(self.loginPromptDiagOS, msgStr):
            self.loginToDiagOS()
            self.sendMsg('\r\n')
            time.sleep(1)
            msgStr = self.readMsg()
            log.cprint('msgStr: ' + msgStr)

        # login to bmc first if currently at bmc prompt
        elif re.search(self.loginPromptBmc, msgStr) or re.search(altBmcLoginPrompt, msgStr):
            self.loginToBMC()
            self.sendMsg('\r\n')
            time.sleep(1)
            msgStr = self.readMsg()
            log.cprint('msgStr: ' + msgStr)

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
        else:
            LogMsg = ("Unknown boot mode,  msgStr: " + str(msgStr))
            LogMsg += "\r\ngetBootMode result: FAIL\r\n"
            log.debug(LogMsg)
            raise RuntimeError(LogMsg)
            return None

    def getPrompt(self, mode=None, timeout=60, idleTimeout=60, logFile='None'):
        log.debug('Entering SessionDevice class procedure getPrompt with args : %s\n' % (str(locals())))
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
        promptList = [self.promptGrub, self.promptOnie, self.promptDiagOS, self.promptBmc, self.loginPromptDiagOS, self.loginPromptBmc, altBmcLoginPrompt, Const.promptPython3, self.promptSdk]
        #promptList = [self.promptGrub, self.promptOnie, self.promptDiagOS, self.promptBmc, self.loginPromptDiagOS, self.loginPromptBmc, altBmcLoginPrompt]
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
            errMsg = "\r\nCannot get prompt within %d seconds"%timeout
            raise RuntimeError(errMsg)
            return errMsg

        if re.search(self.promptSdk, outStr):         # SDK prompt
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
                errMsg = "\r\nCannot get prompt within %d seconds"%timeout
                raise RuntimeError(errMsg)
                return errMsg

        if re.search(self.promptGrub, outStr):             # grub prompt
            log.debug("\nDetected grub prompt.\n")
            self.currentBootMode = Const.BOOT_MODE_GRUB
        elif re.search(self.promptOnie, outStr):           # onie prompt
            log.debug("\nDetected onie prompt.\n")
            self.currentBootMode = Const.BOOT_MODE_ONIE
        elif re.search(self.promptDiagOS, outStr):         # diagOS prompt
            if 'sonic' in self.os:
                log.debug("\nDetected centos prompt.\n")
                self.currentBootMode = Const.BOOT_MODE_CENTOS
            else:
                log.debug("\nDetected diagos prompt.\n")
                self.currentBootMode = Const.BOOT_MODE_DIAGOS
        elif re.search(self.promptBmc, outStr):            # bmc prompt
            if 'sonic' in self.os:
                log.debug("\nDetected openbmc prompt.\n")
                self.currentBootMode = Const.BOOT_MODE_OPENBMC
            else:
                log.debug("\nDetected bmc prompt.\n")
                self.currentBootMode = Const.BOOT_MODE_BMC
        elif re.search(self.loginPromptDiagOS, outStr):    # diagOS login prompt
            log.debug("\nLogin to DiagOS.\n")
            currentPromptStr = self.loginToDiagOS()
            if 'sonic' in self.os:
                self.currentBootMode = Const.BOOT_MODE_CENTOS
            else:
                self.currentBootMode = Const.BOOT_MODE_DIAGOS
        elif re.search(self.loginPromptBmc, outStr) or re.search(altBmcLoginPrompt, outStr):       # bmc login prompt
            log.debug("\nLogin to BMC.\n")
            currentPromptStr = self.loginToBMC()
            if 'sonic' in self.os:
                self.currentBootMode = Const.BOOT_MODE_OPENBMC
            else:
                self.currentBootMode = Const.BOOT_MODE_BMC
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
            LogMsg = ("\r\nrequested promptStr: %s" %mode_str)
            LogMsg += ("\r\ncurrent prompt mode: %s" %currentPromptMode)
            log.debug(LogMsg)

            if currentPromptMode != mode_str:
                if "centos" in mode_str:
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
                    return LogMsg

                outStr += output

        if self.enable_terminal_log_file != '0':
            if logFile != 'None':
                self.send_output_to_log_file(outStr, logFile)

        if mode is not None:
            if "result: FAIL" in output:
                LogMsg += output
                LogMsg += ("\r\nFail to enter %s mode." %modeStr)
                LogMsg += "\r\ngetPrompt result: FAIL3"
                log.debug(LogMsg)
                raise RuntimeError(LogMsg)
                return LogMsg

        self.sendMsg("\r\r")
        return self.getCurrentPromptStr()

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
