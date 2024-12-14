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
import re
import time

from Device import Device
from SessionDevice import SessionDevice
import Logger as log
import Const
import YamlParse
import pexpect
import sys
from WhiteboxPowerCycler import WhiteboxPowerCycler


class WhiteboxDevice(Device):
    def __init__(self, deviceDict):
        super().__init__(deviceDict)
        log.debug("Entering WhiteboxDevice class procedure: __init__")
        self.promptESMA = 'ESM\s\w\s.*[>#]'
        self.promptESMB = 'ESM\s\w\s.*[>#]'
        self.BOOT_MODE_ESMA = 'ESM\s\w\s.*[>#]'
        self.BOOT_MODE_ESMB = 'ESM\s\w\s.*[>#]'
        self.bmcIP = deviceDict['bmcIP']
        self.esmbConsoleIP = deviceDict.get('esmbConsoleIP')
        self.esmbConsolePort = deviceDict.get('esmbConsolePort')
        deviceInfo = YamlParse.getPowerCyclerInfo()
        dict = deviceInfo[self.powerCyclerName]
        self.powerCycler = WhiteboxPowerCycler(dict, self.powerCyclerPort)

    #   whitebox platform specific implementations, overwrite the functions of parent class begin:
    def login(self):
        log.debug("Entering WhiteboxDevice class procedure: login")
        self.telnetConnect.open_connection(self.consoleIP, port=self.consolePort)
        self.sendCmd(' ')
        return self.getPrompt(Const.BOOT_MODE_CENTOS)

    def loginOS(self):
        log.debug("Entering WhiteboxDevice class procedure: loginOS")
        self.telnetConnect.open_connection(self.consoleIP, port=self.consolePort)
        self.__getPrompt(Const.BOOT_MODE_DIAGOS)
        return ''

    def loginESMA(self):
        log.debug("Entering WhiteboxDevice class procedure: loginESMA")
        self.telnetConnect.open_connection(self.consoleIP, port=self.consolePort)
        self.__getPrompt(self.BOOT_MODE_ESMA)
        return ''

    def loginESMB(self):
        log.debug("Entering WhiteboxDevice class procedure: loginESMB")
        self.telnetConnect.open_connection(self.consoleIP, port=self.consolePort)
        self.__getPrompt(self.BOOT_MODE_ESMB)
        return ''

    def __getPrompt(self, mode=None, timeout=60, idleTimeout=60, logFile='None'):
        log.debug('Entering WhiteboxDevice getPrompt with args : %s\n' % (str(locals())))
        output = ''
        outStr = ''
        LogMsg = ''
        modeStr = ""
        self.flush()
        promptList = [self.promptESMA, self.promptESMB, self.loginPromptDiagOS, self.promptDiagOS]
        self.setConnectionTimeout(timeout)
        patternList = re.compile('|'.join(promptList))
        LogMsg = ''
        self.sendCmd('')
        try:
            try:
                output = self.read_until_regexp(patternList)
            except:
                self.sendMsg('\x03')
                output += self.read_until_regexp(patternList)
            log.cprint(output)
            outStr += output
        except:
            LogMsg = "\r\ngetPrompt result: FAIL1"
            log.debug(LogMsg)
            errMsg = "\r\nCannot get prompt within %d seconds" % timeout
            raise RuntimeError(errMsg)

        if re.search(self.promptESMA, outStr):  # ESMA prompt
            log.debug("\nDetected ESM A.\n")
            self.currentBootMode = self.BOOT_MODE_ESMA
        elif re.search(self.promptESMB, outStr):  # ESMB prompt
            log.debug("\nDetected ESM B.\n")
            self.currentBootMode = self.BOOT_MODE_ESMB
        elif re.search(self.loginPromptDiagOS, outStr):  # diagOS login prompt
            log.debug("\nLogin to DiagOS.\n")
            currentPromptStr = self.__loginToDiagOS()
            self.currentBootMode = Const.BOOT_MODE_DIAGOS
        elif re.search(self.promptDiagOS, outStr):  # diagOS prompt
            log.debug("\nDetected diagos prompt.\n")
            self.currentBootMode = Const.BOOT_MODE_DIAGOS
        else:
            log.debug("\nError in getPrompt. Unknown prompt.\n")

        if mode is not None:
            LogMsg = ("\r\nrequested promptStr: %s" % mode)
            LogMsg += ("\r\ncurrent prompt mode: %s" % self.currentBootMode)
            log.debug(LogMsg)

            if self.currentBootMode != mode:
                if mode == Const.BOOT_MODE_DIAGOS:
                    output = self.__bootIntoDiagOS()
                    modeStr = "DiagOS Mode"
                elif mode == self.BOOT_MODE_ESMB:
                    modeStr = "EMS B Mode"
                elif mode == self.BOOT_MODE_ESMA:
                    modeStr = "ESM A Mode"
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

        self.sendMsg("\r\n")
        return self.currentBootMode

    def __loginToDiagOS(self):
        log.debug("Entering Device class procedure: __loginToDiagOS")
        self.sendMsg(self.rootUserName)

        try:
            self.sendMsg('\r\n')
            time.sleep(1)
            output = self.readUntil("Password:", timeout=3)
            log.cprint(output)
            self.sendMsg(self.rootPassword)
        except:
            pass

        self.sendMsg('\r\n')
        time.sleep(1)
        self.read_until_regexp(self.promptDiagOS)

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
                      self.loginPromptBmc, altBmcLoginPrompt, Const.promptPython3, self.promptSdk]
        self.setConnectionTimeout(timeout)
        patternList = re.compile('|'.join([x for x in promptList if x]))
        LogMsg = ''
        try:
            try:
                output = self.read_until_regexp(patternList)
            except:
                self.sendMsg('\r\n')
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

        if self.promptGrub and re.search(self.promptGrub, outStr):  # grub prompt
            log.debug("\nDetected grub prompt.\n")
            self.currentBootMode = Const.BOOT_MODE_GRUB
        elif self.promptOnie and re.search(self.promptOnie, outStr):  # onie prompt
            log.debug("\nDetected onie prompt.\n")
            self.currentBootMode = Const.BOOT_MODE_ONIE
        elif self.promptDiagOS and re.search(self.promptDiagOS, outStr):  # diagOS prompt
            if 'sonic' in self.os:
                log.debug("\nDetected centos prompt.\n")
                self.currentBootMode = Const.BOOT_MODE_CENTOS
            else:
                log.debug("\nDetected diagos prompt.\n")
                self.currentBootMode = Const.BOOT_MODE_DIAGOS
        elif self.promptBmc and re.search(self.promptBmc, outStr):  # bmc prompt
            if 'sonic' in self.os:
                log.debug("\nDetected openbmc prompt.\n")
                self.currentBootMode = Const.BOOT_MODE_OPENBMC
            else:
                log.debug("\nDetected bmc prompt.\n")
                self.currentBootMode = Const.BOOT_MODE_BMC
        elif self.loginPromptDiagOS and re.search(self.loginPromptDiagOS, outStr):  # diagOS login prompt
            log.debug("\nLogin to DiagOS.\n")
            currentPromptStr = self.loginToDiagOS()
            if 'sonic' in self.os:
                self.currentBootMode = Const.BOOT_MODE_CENTOS
            else:
                self.currentBootMode = Const.BOOT_MODE_DIAGOS
        elif (self.loginPromptBmc and re.search(self.loginPromptBmc, outStr)) \
                or (altBmcLoginPrompt and re.search(altBmcLoginPrompt, outStr)):  # bmc login prompt
            log.debug("\nLogin to BMC.\n")
            currentPromptStr = self.loginToBMC()
            if 'sonic' in self.os:
                self.currentBootMode = Const.BOOT_MODE_OPENBMC
            else:
                self.currentBootMode = Const.BOOT_MODE_BMC
        elif Const.promptPython3 and re.search(Const.promptPython3, outStr):
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

    def powerCycleDevice1(self):
        log.debug("Entering Device class procedure: powerCycleDevice1")
        return self.powerCycler.powerCycleDevice1()

    def powerCycleDevice2(self):
        log.debug("Entering Device class procedure: powerCycleDevice2")
        return self.powerCycler.powerCycleDevice2()

    def powerCycleDevice3(self):
        log.debug("Entering Device class procedure: powerCycleDevice3")
        return self.powerCycler.powerCycleDevice3()

    def poweroffDevice1(self):
        log.debug("Entering Device class procedure: poweroffDevice1")
        return self.powerCycler.poweroffDevice1()

    def poweronDevice1(self):
        log.debug("Entering Device class procedure: poweronDevice1")
        return self.powerCycler.poweronDevice1()

    def poweroffDevice3(self):
        log.debug("Entering Device class procedure: poweroffDevice3")
        return self.powerCycler.poweroffDevice3()

    def poweronDevice3(self):
        log.debug("Entering Device class procedure: poweronDevice3")
        return self.powerCycler.poweronDevice3()

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


class WhiteboxSessionDevice(SessionDevice):

    def __init__(self, deviceDict):
        super().__init__(deviceDict)
        log.debug("Entering WhiteboxSessionDevice class procedure: __init__")

    def connect(self, username, ipAddr, port=None, protocol=Const.PROTOCOL_SSH, password=None):
        log.debug('Entering Session class procedure connect with args : %s\n' % (str(locals())))
        self.username = username
        self.ipAddr = ipAddr
        self.protocol = protocol

        if self.protocol == Const.PROTOCOL_SSH:
            if password is None:
                cmd = "ssh -o StrictHostKeyChecking=no -l %s " % self.username
            else:
                cmd = "ssh -l %s " % self.username
        else:
            cmd = "telnet "
        cmd += ipAddr
        if port != None:
            cmd += ' ' + str(port)
        # cmd += '\n'
        log.info('cmd: %s' % (cmd))
        #  for using of pexpect, refer  https://pexpect.readthedocs.io/en/stable/overview.html
        self.child = pexpect.spawn(cmd, encoding='utf-8')
        if password is not None:
            key_password = "assword"
            ssh_newkey = 'Are you sure you want to continue connecting'
            i = self.child.expect([pexpect.TIMEOUT, ssh_newkey, '%s: ' % key_password])
            if i == 0:  # Timeout
                print('ERROR_1!')
                print('SSH could not login. Here is what SSH said:')
                # print(child.before, child.after)
                return None
            if i == 1:  # SSH does not have the public key. Just accept it.
                self.child.sendline('yes')
                self.child.sendline('\r')
                self.child.expect('%s: ' % key_password)
                i = self.child.expect([pexpect.TIMEOUT, '%s: ' % key_password])
                if i == 0:
                    # Timeout
                    print('ERROR_2!')
                    print('SSH could not login. Here is what SSH said:')
                    # print(child.before, child.after)
                    return None
                self.child.sendline(password)
            if i == 2:
                self.child.sendline(password)
                #        log.debug(str(child))
        # self.child = pexpect.spawn(cmd)
        self.child.sendline()
        # self.child.logfile = sys.stdout
        # self.child.logfile_read = sys.stdout
        return self.child
