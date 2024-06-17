###############################################################################
# LEGALESE:   "Copyright (C) 2019-2021, Celestica Corp. All rights reserved." #
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
from crobot import Logger as log
from crobot import Const
import AliConst
from crobot.Decorator import logThis

class AliDevice(Device):

    @logThis
    def __init__(self, deviceDict):
        super().__init__(deviceDict)
        self.promptUboot = deviceDict['promptUboot']

    @logThis
    def loginDiagOS(self):
        self.telnetConnect.open_connection(self.consoleIP, port=self.consolePort)
        return self.getPrompt(Const.BOOT_MODE_DIAGOS, timeout=120)

    @logThis
    def loginBmc(self):
        self.telnetConnect.open_connection(self.consoleIP, port=self.consolePort)
        return self.getPrompt(Const.BOOT_MODE_OPENBMC, timeout=120)

    @logThis
    def loginOnie(self):
        self.telnetConnect.open_connection(self.consoleIP, port=self.consolePort)
        return self.getPrompt(Const.BOOT_MODE_ONIE, timeout=120)

    @logThis
    def loginBios(self):
        self.telnetConnect.open_connection(self.consoleIP, port=self.consolePort, \
             terminal_emulation=True, terminal_type="vt100", window_size="400x100")
        return self.getPrompt(Const.BOOT_MODE_DIAGOS, timeout=120)

    @logThis
    def getPrompt(self, mode=None, timeout=60, idleTimeout=60, logFile='None'):
        """" this function used to change mode, i.e. get into the expected prompt/mode"""

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
        promptList = [self.promptUboot, self.promptGrub, self.promptOnie, self.promptDiagOS, self.promptBmc, \
            self.loginPromptDiagOS, self.loginPromptBmc, altBmcLoginPrompt, Const.promptPython3, self.promptSdk, \
            self.promptUboot, AliConst.PROMPT_UEFI]
        self.setConnectionTimeout(timeout)
        patternList = re.compile('|'.join(promptList))
        try:
            try:
                output = self.read_until_regexp(patternList)
            except:
                self.sendCmd('')
                time.sleep(3)
                self.sendMsg(Const.KEY_CTRL_C)  #this will make boot into onie in a case
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
                    self.sendMsg(Const.KEY_CTRL_C)
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
            log.debug("\nDetected diagos prompt.\n")
            self.currentBootMode = Const.BOOT_MODE_DIAGOS
        elif re.search(self.promptBmc, outStr):            # bmc prompt
            log.debug("\nDetected bmc prompt.\n")
            self.currentBootMode = Const.BOOT_MODE_BMC
        elif re.search(self.loginPromptDiagOS, outStr):    # diagOS login prompt
            log.debug("\nLogin to DiagOS.\n")
            currentPromptStr = self.loginToDiagOS()
            self.currentBootMode = Const.BOOT_MODE_DIAGOS
        elif re.search(self.loginPromptBmc, outStr) or re.search(altBmcLoginPrompt, outStr):       # bmc login prompt
            log.debug("\nLogin to BMC.\n")
            currentPromptStr = self.loginToBMC()
            self.currentBootMode = Const.BOOT_MODE_BMC
        elif re.search(Const.promptPython3, outStr):
            log.debug("\nLogin to python3, will get back to centos mode soon.\n")
            self.sendMsg("\r")
            self.sendCmd('exit()')
            time.sleep(1)
            self.currentBootMode = Const.BOOT_MODE_PYTHON3
        elif re.search(self.promptUboot, outStr):             # uboot prompt
            log.debug("\nDetected uboot prompt.\n")
            self.currentBootMode = Const.BOOT_MODE_UBOOT
        elif re.search(AliConst.PROMPT_UEFI, outStr):
            log.debug("\nDetected UEFI prompt.\n")
            self.currentBootMode = Const.BOOT_MODE_UEFI
        else:
            log.debug("\nError in getPrompt. Unknown prompt.\n")

        if mode is not None:
            currentPromptMode = self.currentBootMode
            LogMsg = ("\r\nrequested promptStr: %s" %mode)
            LogMsg += ("\r\ncurrent prompt mode: %s" %currentPromptMode)
            log.debug(LogMsg)

            if currentPromptMode != mode:
                if mode == Const.BOOT_MODE_DIAGOS:
                    self.__bootIntoDiagOS()
                elif mode in [Const.ONIE_INSTALL_MODE, Const.ONIE_RESCUE_MODE, Const.ONIE_UPDATE_MODE, Const.BOOT_MODE_ONIE]:
                    self.__bootIntoOnieMode(mode)
                elif mode == Const.BOOT_MODE_OPENBMC:
                    self.__bootIntoOpenbmcMode()
                elif mode == Const.BOOT_MODE_UBOOT:
                    self.__bootIntoUbootMode()
                elif mode == Const.BOOT_MODE_UEFI:
                    self.__bootIntoUefiMode()
                else:
                    LogMsg = "\r\nUnknown requested boot prompt."
                    raise RuntimeError(LogMsg)

        return self.getCurrentPromptStr()

    @logThis
    def __bootIntoOpenbmcMode(self):
        self.switchToBmc()
        if self.currentBootMode == Const.BOOT_MODE_UBOOT:
            self.sendMsg('\r')
            self.sendCmd('reset')
            self.read_until_regexp(self.loginPromptBmc, AliConst.BOOT_TIME)
            self.loginToBMC()
            return ''

    @logThis
    def __bootIntoUbootMode(self):
        self.switchToBmc()
        if self.currentBootMode == Const.BOOT_MODE_UBOOT:
            log.info('Already in Uboot mode')
            return ''
        elif self.currentBootMode == Const.BOOT_MODE_OPENBMC:
            self.__rebootToUboot()
            return ''

    @logThis
    def __rebootToUboot(self):
        self.sendCmd('reboot')
        self.read_until_regexp(AliConst.STOP_AUTOBOOT_PROMPT, AliConst.BOOT_TIME)
        self.sendCmd(AliConst.STOP_AUTOBOOT_KEY)
        time.sleep(1)
        self.read_until_regexp(self.promptUboot)
        self.sendMsg('\r')
        self.currentBootMode = Const.BOOT_MODE_UBOOT

    @logThis
    def __bootIntoUefiMode(self):
        self.switchToCpu()
        if self.currentBootMode == Const.BOOT_MODE_DIAGOS or self.currentBootMode == Const.BOOT_MODE_ONIE:
            if self.currentBootMode == Const.BOOT_MODE_DIAGOS:
                self.sendCmd('sudo su')
            output = self.executeCmd('efibootmgr')
            boot_entry_pattern = r'(?i)Boot(\d+).*UEFI: Built-in EFI Shell'
            match = re.search(boot_entry_pattern, output)
            if match:
                boot_entry = match.group(1)
            else:
                msg = "Cannot found 'UEFI: Built-in EFI Shell' in boot entries"
                log.debug(msg)
                raise RuntimeError(msg)

            output = self.executeCmd('efibootmgr -n %s'%(boot_entry))
            if 'BootNext: %s'%(boot_entry) in output:
                log.debug("Setting next boot successfully")
            else:
                msg = "Failed to set next boot"
                log.debug(msg)
                raise RuntimeError(msg)

            self.sendCmd('reboot')
            self.read_until_regexp(AliConst.PROMPT_UEFI, AliConst.BOOT_TIME)
            self.flush()
            self.sendMsg('\r\n')
            time.sleep(1)
            self.currentBootMode = Const.BOOT_MODE_UEFI

    @logThis
    def __bootIntoOnieMode(self, onieBootMode):
        if onieBootMode == Const.BOOT_MODE_ONIE:
            onieBootMode = Const.ONIE_INSTALL_MODE

        if self.currentBootMode == Const.BOOT_MODE_OPENBMC:
            self.switchToCpu()

        if self.currentBootMode == Const.BOOT_MODE_ONIE:
            self.currentBootMode = self.parseOnieMode()

        if self.currentBootMode == onieBootMode:
            log.info("Already in " + onieBootMode)
            return ''

        if self.currentBootMode == Const.BOOT_MODE_DIAGOS:
            self.sendCmd('sudo su')

        self.sendCmd('reboot')
        output = self.readUntil("will be executed automatically in", AliConst.BOOT_TIME)
        self.toTopOnieMenuItem(output)
        time.sleep(1)

        self.toOnieMode(onieBootMode)

        return ''

    def toOnieMode(self, onieBootMode):
        if onieBootMode == Const.ONIE_INSTALL_MODE:
            self.sendMsg('\r')
            self.read_until_regexp('Starting ONIE Service Discovery', AliConst.ONIE_BOOT_TIME)
            self.sendCmd('')
            mode = self.parseOnieMode()
            if mode is not Const.ONIE_INSTALL_MODE:
                raise RuntimeError('Can not boot into onie discovery mode')
            self.currentBootMode = Const.ONIE_INSTALL_MODE
        if onieBootMode == Const.ONIE_RESCUE_MODE:
            self.keyDown(1)
            self.sendMsg('\r')
            self.read_until_regexp('Please press Enter to activate this console', AliConst.ONIE_BOOT_TIME)
            self.sendCmd('')
            mode = self.parseOnieMode()
            if mode is not Const.ONIE_RESCUE_MODE:
                raise RuntimeError('Can not boot into onie rescue mode')
            self.currentBootMode = Const.ONIE_RESCUE_MODE
        if onieBootMode == Const.ONIE_UPDATE_MODE:
            self.keyDown(3)
            self.sendMsg('\r')
            self.read_until_regexp('Starting ONIE Service Discovery', AliConst.ONIE_BOOT_TIME)
            self.sendCmd('')
            mode = self.parseOnieMode()
            if mode != Const.ONIE_UPDATE_MODE:
                raise RuntimeError('Can not boot into onie update mode')
            self.currentBootMode = Const.ONIE_UPDATE_MODE

    @logThis
    def parseOnieMode(self):
        self.sendCmd('onie-stop')
        time.sleep(5)
        output = self.executeCmd('onie-stop')
        if 'Rescue' in output:
            currentOnieMode = Const.ONIE_RESCUE_MODE
        elif 'update' in output:
            currentOnieMode = Const.ONIE_UPDATE_MODE
        elif 'installer' in output:
            currentOnieMode = Const.ONIE_INSTALL_MODE
        else:
            raise RuntimeError('unknown onie mode')
        return currentOnieMode

    def toOnieMenu(self):
        for i in range(4):
            self.sendMsg(Const.KEY_CTRL_C)
            time.sleep(2)

    def toTopOnieMenuItem(self, output):
        if 'SONiC-OS-' in output:
            log.info('SONIC installed.')
            self.toOnieMenu()
            self.sendMsg('\r')
        time.sleep(1)
        for i in range(4):
            self.sendMsg(Const.KEY_CTRL_A)
            time.sleep(1)
        time.sleep(5)

    def keyDown(self, count):
        for i in range(count):
            self.sendMsg(Const.KEY_DOWN)
            time.sleep(3)

    @logThis
    def __bootIntoDiagOS(self):
        if self.currentBootMode == Const.BOOT_MODE_OPENBMC or self.currentBootMode == Const.BOOT_MODE_PYTHON3:
            self.switchToCpu()

        if self.currentBootMode == Const.BOOT_MODE_ONIE:
            log.debug("Detect boot mode: %s" %(str(self.currentBootMode)))
            #stop onie discovery messages
            self.sendCmd("onie-stop")
            log.debug("Rebooting device to boot into DiagOS...")
            self.sendCmd("reboot")
            output = self.readUntil("will be executed automatically in", 180)
            self.toDiagOS()

        if self.currentBootMode == Const.BOOT_MODE_UEFI:
            self.sendMsg("\r\n")
            self.sendMsg("exit")
            self.sendMsg("\r\n")
            time.sleep(3)
            self.readUntil(self.loginPromptDiagOS, AliConst.BOOT_TIME)
            self.loginToDiagOS()

        self.sendCmd('sudo su')
        return ''

    def toDiagOS(self):
        time.sleep(2)
        # self.sendMsg(Const.KEY_CTRL_A)
        # time.sleep(1)
        self.sendMsg('\r')
        output = self.readUntil(self.loginPromptDiagOS, AliConst.BOOT_TIME)
        self.loginToDiagOS()

    @logThis
    def switchToCpu(self, timeout=None):
        self.trySwitchToCpu()
        self.sendCmd('')
        self.sendCmd(Const.KEY_CTRL_C)
        self.sendCmd('')
        time.sleep(2)
        promptList = [self.promptDiagOS, self.loginPromptDiagOS, self.promptSdk, self.promptOnie, AliConst.PROMPT_UEFI]
        patternList = re.compile('|'.join(promptList))
        output = self.read_until_regexp(patternList, timeout or AliConst.BOOT_TIME) # give a long time for case of cpu is rebooting
        log.cprint(output)
        self.currentBootMode = self.getBootMode(output)
        if self.currentBootMode  not in [Const.BOOT_MODE_DIAGOS, Const.BOOT_MODE_ONIE, Const.BOOT_MODE_UEFI]:
            raise RuntimeError("In switchToCpu, can't switch to CPU!")
        return ''

    @logThis
    def switchToBmc(self):
        self.trySwitchToBmc()
        self.sendCmd('')
        self.sendCmd('')
        time.sleep(2)
        output = self.read_until_regexp(self.promptUboot + '|' + self.promptBmc + '|' + self.loginPromptBmc, AliConst.BOOT_TIME) # give a long time for case of bmc is rebooting
        if re.search(self.loginPromptBmc, output):
            output = self.loginToBMC()
        self.currentBootMode = Const.BOOT_MODE_OPENBMC
        if re.search(self.promptUboot, output):
            self.currentBootMode = Const.BOOT_MODE_UBOOT
        return output

    def execute(self, cmd, mode=None, exe_timeout=60, checkLoginPrompt=True):
        raise RuntimeError('Not allowed to use the function execute, it have bugs! pls use executeCmd, sendCmd etc.')

    @logThis
    def loginToDiagOS(self):
        self.sendCmd('')
        self.sendCmd(Const.KEY_CTRL_C)
        self.sendCmd('')
        time.sleep(2)
        output = self.telnetConnect.login(self.rootUserName, self.rootPassword)
        ret = self.sendMsg("\r\n")
        output = self.read_until_regexp(self.promptDiagOS, timeout=3)
        self.sendCmd('sudo su')
        self.currentBootMode = Const.BOOT_MODE_DIAGOS
        return self.currentBootMode

    @logThis
    def loginToBMC(self):
        self.sendCmd('')
        self.sendCmd('')
        time.sleep(2)
        output = self.telnetConnect.login(self.bmcUserName, self.bmcPassword)
        ret = self.sendMsg("\r\n")
        output = self.read_until_regexp(self.promptBmc, 3)
        self.currentBootMode = Const.BOOT_MODE_OPENBMC
        return self.currentBootMode

    @logThis
    def powerCycleToMode(self, mode):
        if mode == Const.BOOT_MODE_OPENBMC:
            self.switchToBmc()
            self.powerCycleDevice()
            self.read_until_regexp('login:', timeout=AliConst.BOOT_TIME)
            time.sleep(30)
            self.getPrompt(Const.BOOT_MODE_OPENBMC)
        else:
            self.switchToCpu()
            self.powerCycleDevice()
            output = self.readUntil("will be executed automatically in", AliConst.BOOT_TIME)
            if mode == Const.BOOT_MODE_DIAGOS:
                self.toDiagOS()
            else:
                self.toTopOnieMenuItem(output)
                time.sleep(1)
                self.toOnieMode(mode)
    @logThis
    def getBootMode(self, msgStr):
        self.setConnectionTimeout(15)

        self.sendMsg('\r\n')
        time.sleep(1)
        msgStr = self.readMsg()

        if re.search(self.loginPromptDiagOS, msgStr):
            return self.loginToDiagOS()
        if re.search(self.promptOnie, msgStr):
            log.debug("Boot mode: ONIE\r\n")
            return Const.BOOT_MODE_ONIE
        elif re.search(self.promptDiagOS, msgStr):
            log.debug("Boot mode: DIAGOS\r\n")
            return Const.BOOT_MODE_DIAGOS
        elif re.search(self.promptUboot, msgStr):
            log.debug("Boot mode: UBOOT\r\n")
            return Const.BOOT_MODE_UBOOT
        elif re.search(AliConst.PROMPT_UEFI, msgStr):
            log.debug("Boot mode: UEFI\r\n")
            return Const.BOOT_MODE_UEFI
        else:
            LogMsg = ("Unknown boot mode,  msgStr: " + str(msgStr))
            LogMsg += "\r\ngetBootMode result: FAIL\r\n"
            log.debug(LogMsg)
            raise RuntimeError(LogMsg)

def isShamuUnit(self):
    return "shamu" in self.name.lower()
