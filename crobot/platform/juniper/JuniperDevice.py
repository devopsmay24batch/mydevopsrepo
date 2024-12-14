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

from crobot.Device import Device
import Logger as log
import Const
from JuniperConst import *


class JuniperDevice(Device):

    def __init__(self, deviceDict):
        super().__init__(deviceDict)
        log.debug("Entering JuniperDevice class procedure: __init__")
        self.using_pem = -1
        self.promptUboot = deviceDict['promptUboot']
        self.promptSdk = 'BCM.0>|IVM:0>|IVM>'

    def loginDiagOS(self):
        log.debug("Entering JuniperDevice class procedure: loginDiagOS")
        self.telnetConnect.open_connection(self.consoleIP, port=self.consolePort, terminal_emulation=True, terminal_type="vt100", window_size="400x100")
        try:
            self.getPrompt(Const.BOOT_MODE_DIAGOS)
        except:
            log.info('Can not boot into DiagOS, maybe DiagOS is not installed')
            self.getPrompt(Const.BOOT_MODE_CENTOS)
        return ''

    def getPrompt(self, mode=None, timeout=60, idleTimeout=60, logFile='None'):
        log.debug('Entering JuniperDevice getPrompt with args : %s\n' % (str(locals())))
        output = ''
        outStr = ''
        LogMsg = ''
        self.flush()
        promptList = [self.promptUboot, self.promptOnie, self.loginPromptDiagOS, self.promptDiagOS, Const.promptPython3, self.promptSdk]
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
                log.cprint(output)
                outStr += output
            except:
                LogMsg = "\r\ngetPrompt result: FAIL4"
                log.debug(LogMsg)
                errMsg = "\r\nCannot get prompt within %d seconds"%timeout
                raise RuntimeError(errMsg)
                return errMsg

        if re.search(self.promptUboot, outStr):             # uboot prompt
            log.debug("\nDetected uboot prompt.\n")
            self.currentBootMode = Const.BOOT_MODE_UBOOT
        elif re.search(self.promptOnie, outStr):           # onie prompt
            log.debug("\nDetected onie prompt.\n")
            self.currentBootMode = Const.BOOT_MODE_ONIE
        elif re.search(self.loginPromptDiagOS, outStr):    # diagOS login prompt
            log.debug("\nLogin to DiagOS.\n")
            currentPromptStr = self.__loginToDiagOS()
            self.currentBootMode = Const.BOOT_MODE_DIAGOS
        elif re.search(self.promptDiagOS, outStr):         # diagOS prompt
            log.debug("\nDetected diagos prompt.\n")
            self.currentBootMode = Const.BOOT_MODE_DIAGOS
        elif re.search(Const.promptPython3, outStr):
            log.debug("\nLogin to python3, will get back to centos mode soon.\n")
            self.sendMsg("\r")
            time.sleep(1)
            self.currentBootMode = Const.BOOT_MODE_PYTHON3
        else:
            log.debug("\nError in getPrompt. Unknown prompt.\n")

        if mode is not None:
            LogMsg = ("\r\nrequested promptStr: %s" %mode)
            LogMsg += ("\r\ncurrent prompt mode: %s" %self.currentBootMode)
            log.debug(LogMsg)

            if self.currentBootMode != mode:
                if mode == Const.BOOT_MODE_DIAGOS:
                    output = self.__bootIntoDiagOS()
                    modeStr = "DiagOS Mode"
                elif mode == Const.ONIE_INSTALL_MODE:
                    output = self.__bootIntoOnieMode(Const.ONIE_INSTALL_MODE)
                    modeStr = "Onie Install Mode"
                elif mode == Const.ONIE_RESCUE_MODE:
                    output = self.__bootIntoOnieMode(Const.ONIE_RESCUE_MODE)
                    modeStr = "Onie Rescue Mode"
                elif mode == Const.ONIE_UPDATE_MODE:
                    output = self.__bootIntoOnieMode(Const.ONIE_UPDATE_MODE)
                    modeStr = "Onie Update Mode"
                elif mode == Const.BOOT_MODE_ONIE:
                    output = self.__bootIntoOnieMode(Const.BOOT_MODE_ONIE)
                    modeStr = "Onie Mode"
                elif mode == Const.BOOT_MODE_UBOOT:
                    output = self.__bootIntoUbootMode()
                    modeStr = "Uboot Mode"
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

        self.sendMsg("\r\n")
        return self.currentBootMode

    def execute(self, cmd, mode=None, exe_timeout=60, checkLoginPrompt=True):
        raise RuntimeError('Not allowed to use the function execute, it have bugs! pls use executeCmd, sendCmd etc.')

    def executeCmd(self, cmd, mode=None, timeout=60):
        log.debug('Entering JuniperDevice executeCmd with args : %s\n' % (str(locals())))
        if mode != None:
            self.getPrompt(mode, timeout)
        self.flush()

        if self.currentBootMode == Const.BOOT_MODE_UBOOT:
            prompt = "{}[\s\S]+{}".format(cmd.lstrip()[:5], self.promptUboot)
            ret = self.sendCmdRegexp(cmd, prompt, timeout)
            # Ask U-Boot for does not repeat the last command for ENTER Key
            self.sendline(" ")

            return ret

        cmd = 'time ' + cmd
        return self.sendCmdRegexp(cmd, Const.TIME_REG_PROMPT, timeout)

    def __loginToDiagOS(self):
        log.debug("Entering Device class procedure: __loginToDiagOS")
        self.sendMsg(self.rootUserName)

        try:
            self.sendMsg('\r\n')
            if 'login' in self.loginPromptDiagOS:
                self.sendMsg(self.rootUserName)
            time.sleep(3)
            #output = self.readUntil("Password:", timeout=10)
            #log.cprint(output)
            self.sendMsg(self.rootPassword)
        except:
            pass

        self.sendMsg('\r\n')
        time.sleep(1)
        self.read_until_regexp(self.promptDiagOS)

    def rebootToDiag(self):
        log.debug("Entering JuniperDevice class procedure: rebootTODiag")
        self.sendCmd('reboot')
        self.read_until_regexp(self.loginPromptDiagOS, BOOT_TIME)
        self.getPrompt(Const.BOOT_MODE_DIAGOS)

