# LEGALESE:   "Copyright (C) 2019-2020, Celestica Corp. All rights reserved." #
#                                                                             #
# This source code is confidential, proprietary, and contains trade           #
# secrets that are the sole property of Celestica Corp.                       #
# Copy and/or distribution of this source code or disassembly or reverse      #
# engineering of the resultant object code are strictly forbidden without     #
# the written consent of Celestica Corp.                                      #
#                                                                             #
###############################################################################
import os
import Const
import Logger as log
import YamlParse
from Decorator import *
import CommonLib
import re
import GoogleConst
import pexpect
try:
    from Device import Device
    import DeviceMgr
except Exception as err:
    log.cprint(str(err))

device = DeviceMgr.getDevice()

import Logger as log

class GOLDSTONELib():
    def __init__(self):
        log.debug("Entering GoldstoneCommonLib class procedure: __init__")
        import DeviceMgr
        self.device = DeviceMgr.getDevice()

    def loginDevice(self):
        log.debug("Entering GoldstoneCommonLib class procedure: login")
        self.device.telnetConnect.open_connection(self.device.consoleIP, port=self.device.consolePort)
        self.device.tryLogin()
        log.cprint(self.device.currentBootMode)
    
    def loginDevice1(self):
        log.debug("Entering GoldstoneCommonLib class procedure: login for BMC")
        self.device.telnetConnect.open_connection(self.device.bmcConsoleIP, port=self.device.bmcConsolePort)
        self.device.loginToNEWBMC()

    def disconnectDevice(self):
        try:
            self.device.trySwitchToCpu()
        except Exception:
            pass
        finally:
            return self.device.disconnect()


@logThis
def powercycle_device(device):
    deviceObj =  Device.getDeviceObject(device)
    deviceObj.powerCycleDevice()
    log.debug('Sleeping for 200s for device to come up')
    time.sleep(220)


def DiagOSConnect():
    log.debug("Entering GoldstoneCommonLib class procedure: DiagOSConnect")
    log.info(str(device.name))
    device.loginDiagOS()
    device.sendMsg('dhclient -v ma1 \r')
    return

def DiagOSDisconnect():
    global libObj
    log.debug("Entering GoldstoneCommonLib class procedure: DiagOSDisconnect")
    device.sendCmd('exit')
    device.disconnect()
    return

libObj = None

def OSConnect():
    global libObj
    log.debug("Entering GoldstoneCommonLib class procedure: OSConnect")
    libObj = GOLDSTONELib()
    libObj.loginDevice()
    return

def ConnectESMB():
    global libObj
    log.debug("Entering GoldstoneCommonLib class procedure: ConnectESMB")
    libObj = GOLDSTONELib()
    libObj.loginDevice1()
    return

def OSDisconnect():
    global libObj
    log.debug("Entering GoldstoneCommonLib class procedure: OSDisconnect")
    libObj.disconnectDevice()
    return
                                                  

def powerCycleToDiagOS():
    log.debug("Entering GoldstoneCommonLib class procedure: powerCycleToDiagOS")
    return device.powerCycleToMode(Const.BOOT_MODE_DIAGOS)

def powerCycleToUboot():
    log.debug("Entering GoldstoneCommonLib class procedure: powerCycleToUboot")
    return device.powerCycleToMode(Const.BOOT_MODE_UBOOT)

def powerCycleToOnieRescueMode():
    log.debug("Entering GoldstoneCommonLib class procedure: powerCycleToOnieRescueMode")
    return device.powerCycleToMode(Const.ONIE_RESCUE_MODE)

def powerCycleToOnieInstallMode():
    log.debug("Entering GoldstoneCommonLib class procedure: powerCycleToOnieInstallMode")
    return device.powerCycleToMode(Const.ONIE_INSTALL_MODE)

def powerCycleToOnieUpdateMode():
    log.debug("Entering GoldstoneCommonLib class procedure: powerCycleToOnieUpdateMode")
    return device.powerCycleToMode(Const.ONIE_UPDATE_MODE)

def bootIntoDiagOSMode():
    log.debug("Entering GoldstoneCommonLib class procedure: bootIntoDiagOSMode")
    return device.getPrompt(Const.BOOT_MODE_DIAGOS)

def bootIntoUboot():
    log.debug("Entering GoldstoneCommonLib class procedure: bootIntoUboot")
    return device.getPrompt(Const.BOOT_MODE_UBOOT)

def bootIntoOnieInstallMode():
    log.debug("Entering GoldstoneCommonLib class procedure: bootIntoOnieInstallMode")
    return device.getPrompt(Const.ONIE_INSTALL_MODE)

def bootIntoOnieUpdateMode():
    log.debug("Entering GoldstoneCommonLib class procedure: bootIntoOnieUpdateMode")
    return device.getPrompt(Const.ONIE_UPDATE_MODE)

def bootIntoOnieRescueMode():
    log.debug("Entering GoldstoneCommonLib class procedure: bootIntoOnieRescueMode")
    device.getPrompt(Const.ONIE_RESCUE_MODE)

@logThis
def get_data_from_yaml(name):
    stressInfo = YamlParse.getStressConfig()
    return stressInfo[name]

@logThis
def setTimeToSleep(para):
    import time
    time.sleep(int(para))

def run_command(cmd, deviceObj=None, prompt=None, timeout=60, CR=True):
    log.debug("Entering GoldstoneCommonLib class procedure: run_command")

    promptStr = prompt
    if not prompt:
        mode = deviceObj.currentBootMode
        prompt_dict = { Const.BOOT_MODE_UBOOT  : deviceObj.promptUboot,
                        Const.BOOT_MODE_ONIE   : deviceObj.promptOnie,
                        Const.BOOT_MODE_DIAGOS : deviceObj.promptDiagOS
                }
        promptStr = prompt_dict.get(mode, "")
    if isinstance(cmd, str):
        cmd_list = [ cmd ]
    elif isinstance(cmd,list):
        cmd_list = cmd
    else:
        raise Exception("run_command not support run {}".format(type(cmd)))
    output = ""
    print('The length of cmd is : ',len(cmdx))
    for cmdx in cmd_list:
        if len(cmdx) > 50:
            due_prompt = escapeString(cmdx.lstrip()[len(cmdx)-50:50-len(cmdx)])
            print('Due prompt:',due_prompt)
        else:
            due_prompt = escapeString(cmdx.lstrip()[:5])
            print('Due prompt:',due_prompt)
        #due_prompt = escapeString(cmdx.lstrip()[:5])
        finish_prompt = "{}[\s\S]+{}".format(due_prompt, promptStr)
        if CR:
            cmdx += "\n"
        deviceObj.sendMsg(cmdx)
        output += deviceObj.read_until_regexp(finish_prompt, timeout=timeout)

    return output



####################################################################################################################
@logThis
def powerCycle(device):
    device = Device.getDeviceObject(device)
    powerCyclerDict = YamlParse.getPowerCyclerInfo()[device.powerCyclerName]
    userName = powerCyclerDict['userName']
    password = powerCyclerDict['password']
    managementIP = powerCyclerDict['managementIP']
    managementPrompt = powerCyclerDict['managementPrompt']
    loginPrompt = powerCyclerDict['loginPrompt']
    CmdStatus = powerCyclerDict['CmdStatus']
    powerCyclerPorts = device.powerCyclerPort
    if 'EN2.0' in managementPrompt:
        log.debug('Entered Power terminal')
        loginPrompt = 'password:'
        str3 = 'SUCCESS'
        output = ''
        cmd = ('ssh -o StrictHostKeyChecking=no ' + userName + '@' + managementIP)
        # issue telnet command
        child = pexpect.spawn(cmd)


        time.sleep(1)
        child.expect (loginPrompt, timeout=15)

        time.sleep(1)
        str_password = str(password)
        LogMsg = str("\nsending password: [%s]" %str_password)
        log.debug(LogMsg)
        child.send(str_password)
        child.send('\x0d')

        # wait for prompt
        time.sleep(1)
        LogMsg = ("\nwaiting for prompt...")
        log.debug(LogMsg)
        child.expect (managementPrompt, timeout=15)
        time.sleep(1)

        # power off psu
        if isinstance(powerCyclerPorts, list):
            for port in powerCyclerPorts:
                cmd_off = 'dev outlet 1 ' + str(port) + ' off'
                log.debug(cmd_off)
                child.send(cmd_off)
                child.send('\x0d')
                log.debug("power off")
                child.expect (CmdStatus, timeout=15)
                time.sleep(2)

        else:
            cmd_off = (off + str(powerCyclerPorts))
            log.debug(cmd_off)
            child.send(cmd_off)
            child.send('\x0d')
            log.debug("power off")
            child.expect (CmdStatus, timeout=15)

        LogMsg = str("%s\n%s\n" %(child.before, child.after))
        output += LogMsg
        log.debug(LogMsg)

        # wait for system to fully power off including fans
        time.sleep(60)

        # power on psu
        if isinstance(powerCyclerPorts, list):
            for port in powerCyclerPorts:
                cmd_on = 'dev outlet 1 ' + str(port) + ' on'
                log.debug(cmd_on)
                child.send(cmd_on)
                child.send('\x0d')
                log.debug("power on")
                child.expect (CmdStatus, timeout=15)
                time.sleep(2)

        else:
            cmd_on = (on + str(powerCyclerPorts))
            log.debug(cmd_on)
            child.send(cmd_on)
            child.send('\x0d')
            log.debug("power on")
            child.expect (CmdStatus, timeout=15)


        LogMsg = str("%s\n%s\n" %(child.before, child.after))
        output += LogMsg
        log.debug(LogMsg)

        child.close()
        LogMsg = "Closed powerCycler ssh session."
        log.debug(LogMsg)

        device.read_until_regexp("localhost login:", timeout=500)
        log.debug('Sleeping 120s post reboot')
        time.sleep(120)   ##Waiting for DUT module to load 
        device.loginToDiagOS()

        return output
    else:
        log.info("Only Enlogic powercycler supported. Skipping powercycler")

@logThis
def check_server_goldstone(device, host_ip, host_name, host_passwd, server_prompt):
    deviceObj = Device.getDeviceObject(device)
    devicePc = Device.getDeviceObject('PC')
    cmd = 'ssh ' + host_name + '@' + host_ip
    deviceObj.sendCmd(cmd)
    promptList = ["(y/n)", "(yes/no)", "password:"]
    patternList = re.compile('|'.join(promptList))
    output = deviceObj.read_until_regexp(patternList, 20)
    if re.search("(y/n)", output):
        deviceObj.sendCmd("yes")
        deviceObj.read_until_regexp("password:")
        deviceObj.sendCmd(host_passwd)
        deviceObj.read_until_regexp(server_prompt)
    elif re.search("(yes/no)", output):
        deviceObj.sendCmd("yes")
        deviceObj.read_until_regexp("password:")
        deviceObj.sendCmd(host_passwd)
        deviceObj.read_until_regexp(server_prompt)
    elif re.search("password:", output):
        deviceObj.sendCmd(host_passwd)
        deviceObj.read_until_regexp(server_prompt)
    else:
        log.fail("pattern mismatch")
    deviceObj.sendline('\n')



@logThis
def exit_the_server(device):
    device_obj = Device.getDeviceObject(device)
    c2=device_obj.executeCmd('exit')
    # print('The value of c2 is ',c2)


