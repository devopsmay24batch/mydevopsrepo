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

class SEASTONELib():
    def __init__(self):
        log.debug("Entering Seastone class procedure: __init__")
        import DeviceMgr
        self.device = DeviceMgr.getDevice()

    def loginDevice(self):
        log.debug("Entering Seastoning class procedure: login")
        self.device.telnetConnect.open_connection(self.device.consoleIP, port=self.device.consolePort)
        self.device.tryLogin()
        log.cprint(self.device.currentBootMode)
    
    def loginDevice1(self):
        log.debug("Entering Seastoning class procedure: login for BMC")
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
    log.debug("Entering SeastoneCommonLib procedure: DiagOSConnect")
    device.loginDiagOS()
    device.sendMsg('dhclient -v ma1 \r')
    return

def DiagOSDisconnect():
    global libObj
    log.debug("Entering SeastoneCommonLib procedure: DiagOSDisconnect")
    device.disconnect()
    return

libObj = None

def OSConnect():
    global libObj
    log.debug("Entering Seastone procedure: OSConnect")
    libObj = SEASTONELib()
    libObj.loginDevice()
    return

def ConnectESMB():
    global libObj
    log.debug("Entering Seastone procedure: ConnectESMB")
    libObj = SEASTONELib()
    libObj.loginDevice1()
    return

def OSDisconnect():
    global libObj
    log.debug("Entering Seastone procedure: OSDisconnect")
    libObj.disconnectDevice()
    return
                                                  

def powerCycleToDiagOS():
    log.debug("Entering SeastoneCommonLib procedure: powerCycleToDiagOS")
    return device.powerCycleToMode(Const.BOOT_MODE_DIAGOS)

def powerCycleToUboot():
    log.debug("Entering SeastoneCommonLib procedure: powerCycleToUboot")
    return device.powerCycleToMode(Const.BOOT_MODE_UBOOT)

def powerCycleToOnieRescueMode():
    log.debug("Entering SeastoneCommonLib procedure: powerCycleToOnieRescueMode")
    return device.powerCycleToMode(Const.ONIE_RESCUE_MODE)

def powerCycleToOnieInstallMode():
    log.debug("Entering SeastoneCommonLib procedure: powerCycleToOnieInstallMode")
    return device.powerCycleToMode(Const.ONIE_INSTALL_MODE)

def powerCycleToOnieUpdateMode():
    log.debug("Entering SeastoneCommonLib procedure: powerCycleToOnieUpdateMode")
    return device.powerCycleToMode(Const.ONIE_UPDATE_MODE)

def bootIntoDiagOSMode():
    log.debug("Entering SeastoneCommonLib procedure: bootIntoDiagOSMode")
    return device.getPrompt(Const.BOOT_MODE_DIAGOS)

def bootIntoUboot():
    log.debug("Entering SeastoneCommonLib procedure: bootIntoUboot")
    return device.getPrompt(Const.BOOT_MODE_UBOOT)

def bootIntoOnieInstallMode():
    log.debug("Entering OnieLib class procedure: bootIntoOnieInstallMode")
    return device.getPrompt(Const.ONIE_INSTALL_MODE)

def bootIntoOnieUpdateMode():
    log.debug("Entering OnieLib class procedure: bootIntoOnieUpdateMode")
    return device.getPrompt(Const.ONIE_UPDATE_MODE)

def bootIntoOnieRescueMode():
    log.debug("Entering OnieLib class procedure: bootIntoOnieRescueMode")
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
    log.debug("Entering procedure: run_command")

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
def powercycle_pdu1(device,a,b):

    userName ='admn'
    password = 'admn'
    product = 'powercycler'
    managementIP = a
    managementPort = ''
    managementPrompt = 'Switched CDU:'
    powerCyclerPort1 = b
    log.debug("Entering powerCycleDevice1 class procedure: poweronDevice1")
    log.debug("powerCyclerPort1=[%s]" %str(powerCyclerPort1))
    print(managementPrompt)
    if 'Switched CDU' in managementPrompt:
        log.debug('Entered Power terminal')
        str1 = 'Username'
        str2 = 'Password'
        str3 = 'successful'
        on = 'REBOOT '
        off='REBOOT '
        output = ''
        cmd = ("telnet " + managementIP + " " + managementPort + "\n")
        # issue telnet command
        child = pexpect.spawn(cmd)

        time.sleep(1)
        child.expect (str1, timeout=15)

        time.sleep(1)
        str_username = str(userName)
        LogMsg = str("\nsending username: [%s]" %str_username)
        log.debug(LogMsg)
        child.send(str_username)
        child.send('\x0d')

        time.sleep(1)
        child.expect (str2, timeout=15)

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
        if isinstance(powerCyclerPort1, list):
            for port in powerCyclerPort1:
                cmd_off = off + str(port)
                log.debug(cmd_off)
                child.send(cmd_off)
                child.send('\x0d')
                log.debug("power off")
                child.expect (str3, timeout=15)

        else:
            cmd_off = (off + str(powerCyclerPort1))
            log.debug(cmd_off)
            child.send(cmd_off)
            child.send('\x0d')
            log.debug("power off")
            child.expect (str3, timeout=15)

        # wait for system to fully power off including fans
        time.sleep(30)

        LogMsg = str("%s\n%s\n" %(child.before, child.after))
        output += LogMsg
        log.debug(LogMsg)

        # terminate telnet session
        time.sleep(2)
        child.sendcontrol(']')
        time.sleep(2)
        child.sendline("q")
        time.sleep(2)

        LogMsg = "Closed powerCycler telnet session."
        log.debug(LogMsg)
         

        log.debug('Sleeping 150s post reboot')^M
        time.sleep(150)   ##Waiting for DUT module to load 
        device.loginToDiagOS()

        return output


@logThis
def check_server_seastone(device, host_ip, host_name, host_passwd, server_prompt):
    deviceObj = Device.getDeviceObject(device)
    devicePc = Device.getDeviceObject('PC')
    deviceObj.executeCmd("dhclient -v ma1")
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
    print('The value of c2 is ',c2)


@logThis
def switchToCpu1(device):
        device = Device.getDeviceObject(device)
        log.debug("Entering Seasonte CommonLib: switchToCpu")
        device.trySwitchToCpu()

@logThis
def powercycle_DVT(device):
    device = Device.getDeviceObject(device)
    userName ='admin'
    password = 'sysadmin@123'
    product = 'powercycler'
    managementIP = '10.208.83.158'
    managementPort = ''
    managementPrompt = 'EN2.0>'
    powerCyclerPort1 = ['21','24']
    log.debug("Entering powerCycleDevice1 class procedure: poweronDevice1")
    log.debug("powerCyclerPort1=[%s]" %str(powerCyclerPort1))
    print(managementPrompt)
    if 'EN2.0' in managementPrompt:
        log.debug('Entered Power terminal')
        str1 = 'Username'
        str2 = 'password:'
        str3 = 'SUCCESS'
        output = ''
        cmd = ('ssh ' + userName + '@' + managementIP)
        # issue telnet command
        child = pexpect.spawn(cmd)


        time.sleep(1)
        child.expect (str2, timeout=15)

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
        if isinstance(powerCyclerPort1, list):
            for port in powerCyclerPort1:
                cmd_off = 'dev outlet 1 ' + str(port) + ' off'
                log.debug(cmd_off)
                child.send(cmd_off)
                child.send('\x0d')
                log.debug("power off")
                child.expect (str3, timeout=15)
                time.sleep(2)

        else:
            cmd_off = (off + str(powerCyclerPort1))
            log.debug(cmd_off)
            child.send(cmd_off)
            child.send('\x0d')
            log.debug("power off")
            child.expect (str3, timeout=15)

        # power off psu
        if isinstance(powerCyclerPort1, list):
            for port in powerCyclerPort1:
                cmd_off = 'dev outlet 1 ' + str(port) + ' on'
                log.debug(cmd_off)
                child.send(cmd_off)
                child.send('\x0d')
                log.debug("power off")
                child.expect (str3, timeout=15)
                time.sleep(2)

        else:
            cmd_off = (off + str(powerCyclerPort1))
            log.debug(cmd_off)
            child.send(cmd_off)
            child.send('\x0d')
            log.debug("power off")
            child.expect (str3, timeout=15)


        # wait for system to fully power off including fans
        time.sleep(30)

        LogMsg = str("%s\n%s\n" %(child.before, child.after))
        output += LogMsg
        log.debug(LogMsg)

        # terminate telnet session
        time.sleep(2)
        child.sendcontrol(']')
        time.sleep(2)
        child.sendline("q")
        time.sleep(2)

        LogMsg = "Closed powerCycler telnet session."
        log.debug(LogMsg)

        device.read_until_regexp("localhost login:", timeout=500)
        log.debug('Sleeping 60s post reboot')
        time.sleep(120)   ##Waiting for DUT module to load 
        device.loginToDiagOS()

        return output


