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
from GoogleConst import *


class GoogleDevice(Device):

    def __init__(self, deviceDict):
        super().__init__(deviceDict)
        log.debug("Entering GoogleDevice class procedure: __init__")
        self.using_pem = -1
        self.promptUboot = deviceDict['promptUboot']
        self.promptSdk = 'BCM.0>|IVM:0>|IVM>'

    def loginDiagOS(self):
        log.debug("Entering GoogleDevice class procedure: loginDiagOS")
        self.telnetConnect.open_connection(self.consoleIP, port=self.consolePort, terminal_emulation=True, terminal_type="vt100", window_size="400x100")
        try:
            self.getPrompt(Const.BOOT_MODE_DIAGOS)
        except:
            log.info('Can not boot into DiagOS, maybe DiagOS is not installed')
            self.getPrompt(Const.BOOT_MODE_UBOOT)
        return ''

    def loginOnie(self):
        log.debug("Entering GoogleDevice class procedure: loginOnie")
        self.telnetConnect.open_connection(self.consoleIP, port=self.consolePort,terminal_emulation=True, terminal_type="vt100", window_size="400x100")
        try:
            self.getPrompt(Const.BOOT_MODE_ONIE)
        except:
            log.info('Can not boot into onie, maybe onie is not installed')
            self.getPrompt(Const.BOOT_MODE_UBOOT)  #
        return ''

    def getPrompt(self, mode=None, timeout=60, idleTimeout=60, logFile='None'):
        log.debug('Entering GoogleDevice getPrompt with args : %s\n' % (str(locals())))
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


    def __bootIntoOnieMode(self, onieBootMode):
        log.debug('Entering procedure __bootIntoOnieMode : %s\n' % (str(locals())))

        if self.currentBootMode == onieBootMode:
            log.info("Already in " + onieBootMode)
            return ''

        if self.currentBootMode == Const.BOOT_MODE_UBOOT:
            self.bootOnieFromUboot(onieBootMode)
            return ''

        if self.currentBootMode == Const.BOOT_MODE_ONIE:
            self.flush()
            output = self.executeCmd('onie-discovery-stop')
            currentOnieMode = self.parseOnieMode(output)
            if onieBootMode == currentOnieMode:
                log.info("Already in " + onieBootMode)
                return ''
            self.rebootToOnie(onieBootMode)

        if self.currentBootMode == Const.BOOT_MODE_DIAGOS:
            self.rebootToOnie(onieBootMode)
        return ''

    def rebootToOnie(self, onieBootMode):
        log.debug('Entering procedure rebootToOnie : %s\n' % (str(locals())))
        self.__rebootToUboot()
        self.bootOnieFromUboot(onieBootMode)

    def rebootToDiagOS(self):
        log.debug('Entering procedure rebootToDiagOS : %s\n' % (str(locals())))
        self.sendCmd('reboot')
        self.read_until_regexp(STOP_AUTOBOOT_PROMPT, BOOT_TIME)
        self.stopAutoBoot()
        self.bootDiagOSFromUboot()

    def bootOnieFromUboot(self, onieBootMode):
        log.debug('Entering procedure bootOnieFromUboot : %s\n' % (str(locals())))
        cmd = self.getOnieBootCmd(onieBootMode)
        self.sendMsg('\r')
        # self.sendMsg(Const.KEY_DEL)
        out = self.sendCmd(cmd)
        # self.read_until_regexp(self.promptOnie, BOOT_TIME)
        if onieBootMode in [Const.BOOT_MODE_ONIE, Const.ONIE_INSTALL_MODE, Const.ONIE_UPDATE_MODE]:
            self.read_until_regexp('Starting ONIE Service Discovery', BOOT_TIME)
            self.sendCmd("\n")
            self.sendCmd('onie-discovery-stop')
        if onieBootMode == Const.ONIE_RESCUE_MODE:
            self.read_until_regexp('Please press Enter to activate this console', BOOT_TIME)
            self.sendCmd('')

        self.currentBootMode = Const.BOOT_MODE_ONIE
        out = self.executeCmd('onie-sysinfo')
        if 'celestica_cs8200' in out or 'celestica_cs8210' in out or 'celestica_cs8260' in out:
            log.info('boot in {} success.'.format(onieBootMode))
        else:
            raise RuntimeError(log.info('boot in {} failed!'.format(onieBootMode)))


    def stopAutoBoot(self):
        log.debug('Entering procedure stopAutoBoot')
        self.sendCmd(STOP_AUTOBOOT_KEY)
        time.sleep(1)

    def parseOnieMode(self, output):
        log.debug('Entering procedure parseOnieMode : %s\n' % (str(locals())))
        if 'Rescue' in output:
            currentOnieMode = Const.ONIE_RESCUE_MODE
        elif 'update' in output:
            currentOnieMode = Const.ONIE_UPDATE_MODE
        elif 'installer' in output:
            currentOnieMode = Const.ONIE_INSTALL_MODE
        else:
            raise RuntimeError('unknown onie mode')
        return currentOnieMode

    def getOnieBootCmd(self, onie_boot_mode):
        log.debug('Entering procedure getOnieBootCmd : %s\n' % (str(locals())))
        if onie_boot_mode in [Const.ONIE_INSTALL_MODE, Const.BOOT_MODE_ONIE]:
            cmd = 'run onie_bootcmd'
        elif onie_boot_mode == Const.ONIE_UPDATE_MODE:
            cmd = 'run onie_update'
        elif onie_boot_mode == Const.ONIE_UNINSTALL_MODE:
            cmd = 'run onie_uninstall'
        elif onie_boot_mode == Const.ONIE_RESCUE_MODE:
            cmd = 'run onie_rescue'
        else:
            raise RuntimeError('Invalid onie mode: ' + onie_boot_mode)
        return cmd

    def __bootIntoUbootMode(self):
        log.debug("Entering Device class procedure: __bootIntoUbootMode")
        if self.currentBootMode == Const.BOOT_MODE_UBOOT:
            log.info('Already in Uboot mode')
            return ''
        self.__rebootToUboot()
        return ''

    def __rebootToUboot(self):
        log.debug("Entering Device class procedure: __rebootToUboot")
        self.sendCmd('reboot')
        self.read_until_regexp(STOP_AUTOBOOT_PROMPT, BOOT_TIME)
        self.stopAutoBoot()
        self.read_until_regexp(self.promptUboot)
        self.sendMsg('\r')
        self.currentBootMode = Const.BOOT_MODE_UBOOT

    def __bootIntoDiagOS(self):
        log.debug("Entering Device class procedure: __bootIntoDiagOS")
        if self.currentBootMode == Const.BOOT_MODE_ONIE:
            self.rebootToDiagOS()
            return ''
        if self.currentBootMode == Const.BOOT_MODE_UBOOT:
            self.bootDiagOSFromUboot()
            return ''

    def bootDiagOSFromUboot(self):
        self.sendMsg('\r')
        out = self.sendCmd('run diag_bootcmd', self.promptUboot)
        out = self.read_until_regexp(self.loginPromptDiagOS, BOOT_TIME)
        self.sendMsg(self.rootUserName)
        self.sendMsg('\r')
        out = self.read_until_regexp('|'.join(["Password:", self.promptDiagOS]),10)
        if "Password:" in out:
            self.sendMsg(self.rootPassword)
            self.sendMsg('\r')
            self.read_until_regexp(self.promptDiagOS)

        self.currentBootMode = Const.BOOT_MODE_DIAGOS

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

    def powerCycleToMode(self, mode):
        self.powerCycleDevice()
        self.read_until_regexp(STOP_AUTOBOOT_PROMPT, BOOT_TIME)
        self.stopAutoBoot()
        return self.getPrompt(mode)

    def getBootMode(self, msgStr):
        log.debug("Entering Device class procedure: getBootMode")
        self.setConnectionTimeout(15)

        self.sendMsg('\r\n')
        time.sleep(1)
        msgStr = self.readMsg()

        LogMsg = ''
        if re.search(self.loginPromptDiagOS, msgStr):
            output = self.telnetConnect.login(self.rootUserName, self.rootPassword)
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
        elif re.search(self.promptUboot, msgStr):
            log.debug("Boot mode: UBOOT\r\n")
            return Const.BOOT_MODE_UBOOT
        else:
            LogMsg = ("Unknown boot mode,  msgStr: " + str(msgStr))
            LogMsg += "\r\ngetBootMode result: FAIL\r\n"
            log.debug(LogMsg)
            raise RuntimeError(LogMsg)

    def execute(self, cmd, mode=None, exe_timeout=60, checkLoginPrompt=True):
        raise RuntimeError('Not allowed to use the function execute, it have bugs! pls use executeCmd, sendCmd etc.')

    def executeCmd(self, cmd, mode=None, timeout=60):
        log.debug('Entering GoogleDevice executeCmd with args : %s\n' % (str(locals())))
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

