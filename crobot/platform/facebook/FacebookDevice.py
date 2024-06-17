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
import Logger as log
import Const
import os

class FacebookDevice(Device):

    def __init__(self, deviceDict):
        super().__init__(deviceDict)
        log.debug("Entering FacebookDevice class procedure: __init__")
        self.using_pem = -1

    ############ dell platform specific implementations, overwrite the functions of parent class begin:
    def login(self):
        log.debug("Entering FacebookDevice class procedure: login")
        self.telnetConnect.open_connection(self.consoleIP, port=self.consolePort)
        return self.getPrompt(Const.BOOT_MODE_CENTOS, timeout=Const.BOOTING_TIME)

    def loginBmc(self):
        log.debug("Entering FacebookDevice class procedure: loginBmc")
        self.telnetConnect.open_connection(self.bmcConsoleIP, port=self.bmcConsolePort)
        devicename = os.environ.get("deviceName", "")
        if 'minipack2' in devicename.lower():
            self.checkDiagOsStatus()
        return self.getPrompt(Const.BOOT_MODE_OPENBMC)

    def checkDiagOsStatus(self):
        log.debug("Entering FacebookDevice class procedure: checkDiagOsStatus")
        self.tryLoginBmc()
        self.sendMsg("\r\n sol.sh \r\n")
        time.sleep(10)
        self.setConnectionTimeout(60)
        self.sendMsg("\r\n")
        self.readMsg()
        self.sendMsg("\r\n")
        try:
            self.sendMsg("\r\n")
            output = self.read_until_regexp(self.promptDiagOS + '|' + self.loginPromptDiagOS, 30)
            if re.search(self.promptDiagOS  + '|' + self.loginPromptDiagOS, output):
                log.info("login to COMe side.")
                return
        except Exception as err:
            log.cprint(str(err))
            log.debug("tryLoginCOMe failed")
            log.fail("tryLoginCOMe failed, It maybe hang up!!!")
            self.switchToBmc()
            self.powerCycleChassis(Const.BOOT_MODE_OPENBMC)

    def switchToCpu(self):
        log.debug("Entering Facebook Device class procedure: switchToCpu")
        #send "sol.sh" command to switch into CentOS
        diagPrompt = ''
        output = ''
        output1 = ''
        output2 = ''
        output3 = ''
        outStr = ''
        enter_centos_prompt = 0
        self.setConnectionTimeout(15)
        for count in range(1, 10):
            self.flush()
            self.setConnectionTimeout(15)
            #sol.sh
            for key in self.keysSwitchToCpu:
                time.sleep(0.1)
                self.sendMsg(key)

            self.sendMsg("\n")
            time.sleep(10)
            self.sendMsg("\r\r\n")
            time.sleep(2)
            output = ''
            output1 = ''
            output2 = ''
            output3 = ''
            output1 = self.readMsg()
            log.debug(output1)
            output += output1
            output2 = output1.strip()
            output3 = output2.splitlines()
            if len(output3) == 0:
                LogMsg = "switchToCpu result: FAIL"
                log.debug(LogMsg)
                raise RuntimeError(LogMsg)
            outStr = str(output3[-1])

            if "BCM.0>" in str(outStr):
                output1 = ''
                output2 = ''
                output3 = ''
                # Issue 'exit' command to exit SDK prompt to diagOS prompt
                log.debug("\nDetected SDK prompt...Exit...\n")
                self.sendMsg("exit")
                self.sendMsg("\r\r\n")
                time.sleep(3)
                output1 = self.readMsg()
                log.debug(output1)
                output += output1
                output2 = output1.strip()
                output3 = output2.splitlines()
                if len(output3) == 0:
                    LogMsg = "switchToCpu result: FAIL"
                    log.debug(LogMsg)
                    raise RuntimeError(LogMsg)
                outStr = str(output3[-1])

            # if at login prompt, then login first
            if "login:" in str(outStr):
                log.debug(outStr)
                self.flush()
                if ("bmc" in str(outStr)) or ("sonic" in str(outStr)):
                    output1 = self.loginToBMC()
                    log.debug(output1)
                    log.debug("Retry switching into CentOS...\n")
                    continue
                else:
                    output1 = self.loginToDiagOS()
                    log.debug(output1)
                    enter_centos_prompt = 1
                    log.debug("Successfully switched into CentOS.\n")
                break

            elif ("unidiag" in str(output1)) or ("Unidiag" in str(output1)):
                log.info("Unidiag prompt detected")
                for i in range(0,5):
                    self.sendMsg("q\r")
                    time.sleep(2)
                    if self.read_until_regexp == 'exit':
                        self.sendMsg('\r')
                        log.success("Exited from Unidiag interface successfully.")
                        break

            elif "Password:" in str(outStr):
                self.flush()
                self.sendMsg("\r\n")
                time.sleep(5)
                output1 = self.readMsg()
                if ("bmc" in str(outStr)) or ("sonic" in str(outStr)):
                    output1 = self.loginToBMC()
                    log.debug(output1)
                    log.debug("Retry switching into CentOS...\n")
                    continue
                else:
                    output1 = self.loginToDiagOS()
                    log.debug(output1)
                    enter_centos_prompt = 1
                    log.debug("Successfully switched into CentOS.\n")
                break

            elif re.search(self.promptDiagOS, outStr):
                self.flush()
                enter_centos_prompt = 1
                log.debug("Successfully switched into CentOS.\n")
                break

            elif re.search(self.promptBmc, outStr):
                self.flush()
                # still at openbmc prompt, retry...
                log.debug("Retry switching into CentOS...\n")
                continue

            elif re.search(Const.promptPython3, outStr):
                #switch to CentOS mode whenever it is in python3
                self.flush()
                self.sendMsg("exit()")
                # still at python3 prompt, retry...
                log.debug("Retry switching into CentOS...\n")
                continue

            else:
                # wait for system to boot up to centos
                log.debug("Waiting for system to boot into CentOS...\n")
                self.sendMsg("\r\r\n")
                time.sleep(2)
                for i in range(1, 600):
                    time.sleep(1)
                    output1 = self.readMsg()
                    output += output1
                    log.debug("%s\n" %output1)

                    if ("unidiag" in str(output1)) or ("Unidiag" in str(output1)) or ("System Version" in str(output1)) or ("localhost login: root (automatic login)" in str(output1)):
                        log.info("Unidiag prompt detected")
                        for i in range(0,5):
                            self.sendMsg("q\r")
                            time.sleep(2)
                            if self.read_until_regexp == 'exit':
                                self.sendMsg('\r')
                                log.success("Exited from Unidiag interface successfully.")
                                break

                    elif "login:" in str(output1):
                        if ("bmc" in str(output1)) or ("sonic" in str(output1)):
                            output1 = self.loginToBMC()
                            output += output1
                            log.debug(output1)
                            continue
                        else:
                            output1 = self.loginToDiagOS()
                            output += output1
                            log.debug(output1)
                            enter_centos_prompt = 1
                            log.debug("Successfully switched into CentOS.\n")
                        break

                    elif re.search(self.promptDiagOS, output1):
                        enter_centos_prompt = 1
                        log.debug("Successfully switched into CentOS.\n")
                        break
                    else:
                        continue
                if enter_centos_prompt == 1:
                    break

        LogMsg = ''
        if enter_centos_prompt == 0:
            LogMsg = "switchToCpu result1: FAIL"
            log.debug(LogMsg)
            raise RuntimeError(LogMsg)
        else:
            LogMsg = "switchToCpu result1: PASS"
            log.debug(LogMsg)

        self.currentBootMode = Const.BOOT_MODE_CENTOS
        time.sleep(1)
        return output


    def switchToBmc(self):
        log.debug("Entering Facebook Device class procedure: switchToBmc")
        output = ''
        output1 = ''
        output2 = ''
        output3 = ''
        outStr = ''
        enter_openbmc_prompt = 0
        for count in range(1, 10):
            self.flush()
            self.setConnectionTimeout(10)
            # ctrl + l, x
            for key in self.keysSwitchToBmc:
                time.sleep(0.3)
                self.sendMsg(key)

            time.sleep(3)
            self.sendMsg("\r\n")
            time.sleep(2)
            output = ''
            output1 = self.readMsg()
            log.debug(output1)
            output += output1
            output2 = output1.strip()
            output3 = output2.splitlines()
            outStr = str(output3[-1])

            # if at bmc login prompt, then login first
            if "login:" in str(outStr):
                self.flush()
                if ("bmc" in str(outStr)) or ("sonic" in str(outStr)):
                    output1 = self.loginToBMC()
                    log.debug(output1)
                    enter_openbmc_prompt = 1
                    log.debug("Successfully switched into openBMC.\n")
                else:
                    output1 = self.loginToDiagOS()
                    log.debug(output1)
                    log.debug("Retry switching into openBMC...\n")
                    continue
                break

            elif "Password:" in str(outStr):
                self.flush()
                self.sendMsg("\r\n")
                time.sleep(5)
                output1 = self.readMsg()
                if ("bmc" in str(outStr)) or ("sonic" in str(outStr)):
                    output1 = self.loginToBMC()
                    log.debug(output1)
                    enter_openbmc_prompt = 1
                    log.debug("Successfully switched into openBMC.\n")
                else:
                    output1 = self.loginToDiagOS()
                    log.debug(output1)
                    log.debug("Retry switching into openBMC...\n")
                    continue
                break

            elif re.search(self.promptBmc, outStr):
                self.flush()
                enter_openbmc_prompt = 1
                log.debug("Successfully switched into openBMC.\n")
                break

            elif re.search(self.promptDiagOS, outStr):
                self.flush()
                # still at centos prompt, retry...
                log.debug("Retry switching into openbmc...\n")
                continue

            elif re.search("unidiag", output1.lower()):
                log.info("Unidiag prompt detected")
                for i in range(0,5):
                    self.sendMsg("q\r")
                    time.sleep(2)
                    if self.read_until_regexp == 'exit':
                        self.sendMsg('\r')
                        log.success("Exited from Unidiag interface successfully.")
                log.debug("Retry switching into openbmc...\n")
                continue

            else:
                # wait for system to boot up to openbmc
                log.debug("Waiting for system to boot into OpenBmc...\n")
                self.sendMsg('\r\r\n')
                time.sleep(2)
                for i in range(1, 600):
                    time.sleep(1)
                    LogMsg = ''
                    output1 = self.readMsg()
                    output += output1
                    log.debug("%s\n" %output1)

                    if "login:" in str(output1):
                        self.flush()
                        if ("bmc" in str(output1)) or ("sonic" in str(output1)):
                            output1 = self.loginToBMC()
                            output += output1
                            log.debug(output1)
                            enter_openbmc_prompt = 1
                            log.debug("Successfully switched into OpenBmc.\n")
                        else:
                            output1 = self.loginToDiagOS()
                            output += output1
                            log.debug(output1)
                            log.debug("Retry switching into openBMC...\n")
                            continue
                        break
                    elif re.search(self.promptBmc, output1):
                        self.flush()
                        enter_openbmc_prompt = 1
                        log.debug("Successfully switched into OpenBmc.\n")
                        break
                    else:
                        continue

                if enter_openbmc_prompt == 1:
                    break

        LogMsg = ''
        if enter_openbmc_prompt == 0:
            LogMsg = "switchToBmc result1: FAIL"
            log.debug(LogMsg)
            raise RuntimeError(LogMsg)
        else:
            LogMsg = "switchToBmc result1: PASS"
            log.debug(LogMsg)

        self.currentBootMode = Const.BOOT_MODE_OPENBMC
        time.sleep(1)
        return output

    def trySwitchToCpu(self):
        log.debug("Entering FacebookDevice class procedure: trySwitchToCpu")
        self.sendMsg("\r\n sol.sh \r\n")
        time.sleep(10)
        self.sendMsg("\r\r\n")
        time.sleep(2)

        return ''

    def powerCycleDeviceToDiagOS(self):
        log.debug("Entering FacebookDevice class procedure: powerCycleDeviceToDiagOS")
        output = self.powerCycle()
        output += self.waitForBmcLoginPrompt()
        self.tryLoginBmc()
        self.sendMsg("\r\n sol.sh \r\n")
        # log.cprint(str(output1))
        output += self.waitForDeviceLoginPrompt()
        self.tryLogin()
        if self.currentBootMode != Const.BOOT_MODE_CENTOS:
            raise RuntimeError("can't boot into DiagOS")
        return output

    ############ platform specific implementations, overwrite the function of parent class end

    # this is the method we power cycle a chassis at most cases, because half units connected
    # with power shelf and can't be power cycle by PDU
    def powerCycleChassis(self, mode):
        log.debug("Entering FacebookDevice class procedure: powerCycleChassis")
        devicename = os.environ.get("deviceName", "")
        cmd = 'wedge_power.sh reset -s'
        cmd1 = 'wedge_power.sh status'
        cmd2 = 'fw-util all --version'
        reset_msg = 'Power reset'
        booting_msg = 'Starting kernel ...'
        self.getPrompt(Const.BOOT_MODE_OPENBMC)
        self.sendline(cmd)
        # self.receive(reset_msg)
        output = self.receive(booting_msg, timeout=Const.BOOTING_TIME)
        time.sleep(120)
        self.getPrompt(Const.BOOT_MODE_OPENBMC, timeout=Const.BOOTING_TIME)
        self.sendline(cmd1)
        self.sendline('\n')
        self.sendline(cmd2)
        if 'minipack3' in devicename.lower():
            time.sleep(120)
        self.getPrompt(Const.BOOT_MODE_CENTOS, timeout=Const.BOOTING_TIME)
        self.getPrompt(mode)
        time.sleep(10)
        return output

    def reset(self, cmd, prompt):
        log.debug('Entering FacebookDevice class procedure reset : %s\n ' % (str(locals())))
        bootMode =  self.currentBootMode
        self.sendMsg('\r\n')
        self.sendCmd(cmd)
        self.sendMsg('\r\n')
        self.waitForBmcLoginPrompt()
        self.tryLoginBmc()
        if self.currentBootMode != Const.BOOT_MODE_OPENBMC:
            raise RuntimeError("Can't boot into BMC")

        if prompt.lower() == Const.BOOT_MODE_CENTOS.lower():
            self.sendMsg("\r\n sol.sh \r\n")
            # log.cprint(str(output1))
            self.waitForDeviceLoginPrompt()
            self.tryLogin()
            if self.currentBootMode != Const.BOOT_MODE_CENTOS:
                raise RuntimeError("can't boot into DiagOS")

    def waitForBmcLoginPrompt(self):
        log.debug("Entering FacebookDevice class procedure: waitForBmcLoginPrompt")
        # time.sleep(100)
        self.setConnectionTimeout(300)
        self.sendMsg("\r\n")
        self.readMsg()
        # log.cprint(output)
        self.sendMsg("\r\n")
        altBmcLoginPrompt = 'None'
        loginStr = self.loginPromptBmc
        if re.search('.', loginStr):
            # strip off the hostname in login prompt
            slist = loginStr.split('.')
            str1 = str(slist[0])
            # alternate bmc login prompt string
            altBmcLoginPrompt = (str1 + ' ' + 'root:')
        output = self.read_until_regexp(self.loginPromptBmc + '|' + altBmcLoginPrompt)
        log.cprint(output)

        self.setConnectionTimeout(5)
        return output

    def waitForDeviceLoginPrompt(self):
        log.debug("Entering FacebookDevice class procedure: waitForDeviceLoginPrompt")
        time.sleep(100)
        self.setConnectionTimeout(150)
        self.sendMsg("\r\n")
        self.readMsg()
        self.sendMsg("\r\n")
        output = self.readUntil(Const.LOGIN_PROMT)
        # log.cprint(output)
        self.setConnectionTimeout(5)
        return output

    def is_using_pem(self):
        if self.using_pem != -1:
            return True if self.using_pem == 1 else False

        log.debug('Entering procedure is_using_pem with args : %s' % (str(locals())))
        self.getPrompt(Const.BOOT_MODE_OPENBMC)
        cmd = 'cd /mnt/data1/BMC_Diag/bin'
        self.transmit(cmd)
        cmd = 'pem-util pem2 --get_pem_info'
        output = self.executeCmd(cmd)
        match = re.search('is not present', output)
        match1 = re.search('command not found', output)
        if match or match1:
            log.info("This unit use PSU")
            self.using_pem = 0
            return False
        else:
            log.info("This unit use PEM")
            self.using_pem = 1
            return True

    def isMinipack2TH4Presence(self):
        log.debug('Entering procedure isMinipack2TH4Presence: %s\n'%(str(locals())))
        self.getPrompt(Const.BOOT_MODE_CENTOS)
        cmd = "lspci | grep '06:00.0'"
        output = self.executeCmd(cmd)
        log.info('output: ' + output)
        for line in output.splitlines():
            line = line.strip()
            if re.search('06:00.0', line, re.IGNORECASE):
                if re.search(cmd, line):
                    continue
                log.info("*** Found TH4 ***\n")
                return True

        log.info('*** TH4 not found ! ***')
        return False
