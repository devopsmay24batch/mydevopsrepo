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
import time
import Logger as log
from TelnetDevice import TelnetDevice
import pexpect
from crobot.PowerCycler import PowerCycler

class GooglePowerCycler(PowerCycler):

    def __init__(self, powerCyclerDict, powerCyclerPort):
        super().__init__(powerCyclerDict, powerCyclerPort)

        log.debug("Entering GooglePowerCycler class procedure: __init__")
        self.powerCyclerPort1 = powerCyclerDict['powerCyclerPort1']
        self.powerCyclerPort2 = powerCyclerDict['powerCyclerPort2']
        self.powerCyclerPort3 = powerCyclerDict['powerCyclerPort3']


    def login(self):
        log.debug("Entering PowerCycler class procedure: login")
        self.telnetConnect.open_connection(self.managementIP, port=self.managementPort)
        self.telnetConnect.set_telnetlib_log_level('DEBUG')
        #self.telnetConnect.set_default_log_level('DEBUG')
        self.sendMsg('\r\n')
        output = ''
        LogMsg = ''
        try:
            # wait for user name prompt and send user name
            output = self.readUntil("User Name :")
            LogMsg += (output + ' ' + self.userName)
            self.sendCmd(self.userName)
        except Exception as err:
            LogMsg += "\r\nPowerCycler Error: Timeout waiting for User Name prompt."
            LogMsg += "\r\nPowerCycler login result: FAIL"
            log.debug(LogMsg)
            raise RuntimeError(LogMsg)
            return LogMsg

        output = ''
        try:
            # wait for password prompt and send password
            output = self.readUntil("Password  :")
            LogMsg += (output + ' ' + self.password)
            self.sendCmd(self.password)
        except Exception as err:
            LogMsg += "\r\nPowerCycler Error: Invalid user name."
            LogMsg += "\r\nPowerCycler login result: FAIL"
            log.debug(LogMsg)
            raise RuntimeError(LogMsg)
            return LogMsg

        output = ''
        try:
            # wait for shell prompt
            output = self.readUntil(self.managementPrompt)
            LogMsg += output
        except Exception as err:
            LogMsg += "\r\nPowerCycler Error: Invalid password."
            LogMsg += "\r\nPowerCycler login result: FAIL"
            log.debug(LogMsg)
            raise RuntimeError(LogMsg)
            return LogMsg

        LogMsg += "\r\nPowerCycler login result: PASS"
        log.debug(LogMsg)
        return LogMsg


    def disconnect(self):
        log.debug("Entering PowerCycler class procedure: disconnect")
        pass


    def sendMsg(self, msg):
        return self.telnetConnect.write_bare(msg)


    def sendCmd(self, cmd):
        return self.telnetConnect.write(cmd)


    def readUntil(self, wait_str):
        return self.telnetConnect.read_until(wait_str)


    def powerOff(self):
        log.debug("Entering PowerCycler class procedure: powerOff")
        log.debug("powerCyclerPort=[%s]" %str(self.powerCyclerPort))
        self.sendCmd("olOff " + str(self.powerCyclerPort))
        LogMsg = ''
        try:
            # wait for shell prompt
            output = self.readUntil(self.managementPrompt)
            LogMsg += output
            LogMsg += "\r\nPowerCycler power off result: PASS"
            log.debug(LogMsg)
        except Exception as err:
            LogMsg += "\r\nPowerCycler power off result: FAIL"
            log.debug(LogMsg)
            raise RuntimeError(LogMsg)
        return LogMsg


    def powerOn(self):
        log.debug("Entering PowerCycler class procedure: powerOn")
        log.debug("powerCyclerPort=[%s]" %str(self.powerCyclerPort))
        self.sendCmd("olOn " + str(self.powerCyclerPort))
        LogMsg = ''
        try:
            # wait for shell prompt
            output = self.readUntil(self.managementPrompt)
            LogMsg += output
            LogMsg += "\r\nPowerCycler power on result: PASS"
            log.debug(LogMsg)
        except Exception as err:
            LogMsg += "\r\nPowerCycler power on result: FAIL"
            log.debug(LogMsg)
            raise RuntimeError(LogMsg)
        return LogMsg


    def powerCycle(self):
        log.debug("Entering PowerCycler class procedure: powerCycle")
        LogMsg = ''
        #login to powerCycler
        result = self.login()
        if "result: FAIL" in result:
            LogMsg = "powerCycler login result: FAIL"
            log.debug(LogMsg)
            raise RuntimeError(LogMsg)
            return LogMsg
        time.sleep(1)

        #power off DUT
        result = self.powerOff()
        if "result: FAIL" in result:
            LogMsg = "powerCycler power off result: FAIL"
            log.debug(LogMsg)
            raise RuntimeError(LogMsg)
            return LogMsg
        time.sleep(3)

        #power on DUT
        result = self.powerOn()
        if "result: FAIL" in result:
            LogMsg = "powerCycler power on result: FAIL"
            log.debug(LogMsg)
            raise RuntimeError(LogMsg)
            return LogMsg
        time.sleep(1)

        #disconnect from powerCycler
        self.disconnect()

        LogMsg = "PowerCycle result: PASS"
        log.debug(LogMsg)
        time.sleep(1)
        return LogMsg

    def powerCycleDevice2(self):
        """ this function support powercycle device by power off/on multi pud ports"""
        
        log.debug("Entering powerCycleDevice2 class procedure: powerCycle")
        log.debug("powerCyclerPort2=[%s]" %str(self.powerCyclerPort2))
        print(self.managementPrompt)
        if 'Switched PDU' in self.managementPrompt:
            str1 = 'Username'
            str2 = 'Password'
            str3 = 'successful'
            on = 'On '
            off = 'Off '
        elif 'Switched CDU' in self.managementPrompt:
            str1 = 'Username'
            str2 = 'Password'
            str3 = 'successful'
            on = 'On '
            off = 'Off '
        elif 'apc' in self.managementPrompt:
            str1 = 'User Name'
            str2 = 'Password'
            str3 = 'successful'
            on = 'olOn '
            off = 'olOff '
        else:
            str1 = 'Username'
            str2 = 'Password'
            str3 = 'successful'
            on = 'On '
            off = 'Off '
        output = ''
        cmd = ("telnet " + self.managementIP + " " + self.managementPort + "\n")
        # issue telnet command
        child = pexpect.spawn(cmd)

        time.sleep(1)
        child.expect (str1, timeout=15)

        time.sleep(1)
        str_username = str(self.userName)
        LogMsg = str("\nsending username: [%s]" %str_username)
        log.debug(LogMsg)
        child.send(str_username)
        child.send('\x0d')

        time.sleep(1)
        child.expect (str2, timeout=15)

        time.sleep(1)
        str_password = str(self.password)
        LogMsg = str("\nsending password: [%s]" %str_password)
        log.debug(LogMsg)
        child.send(str_password)
        child.send('\x0d')

        # wait for prompt
        time.sleep(1)
        LogMsg = ("\nwaiting for prompt...")
        log.debug(LogMsg)
        child.expect (self.managementPrompt, timeout=15)
        time.sleep(1)

        # power off psu
        if isinstance(self.powerCyclerPort2, list):
            for port in self.powerCyclerPort2:
                cmd_off = off + str(port)
                child.send(cmd_off)
                child.send('\x0d')
                child.expect (str3, timeout=15)

        else:
            cmd_off = (off + str(self.powerCyclerPort2))
            child.send(cmd_off)
            child.send('\x0d')
            child.expect (str3, timeout=15)

        # wait for system to fully power off including fans
        time.sleep(30)

        # power on psu
        if isinstance(self.powerCyclerPort2, list):
            for port in self.powerCyclerPort2:
                cmd_on = on + str(port)
                child.send(cmd_on)
                child.send('\x0d')
                child.expect (str3, timeout=15)
        else:
            cmd_on = (on + str(self.powerCyclerPort2))
            child.send(cmd_on)
            child.send('\x0d')
            child.expect (str3, timeout=15)


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

        return output

    def powerCycleDevice3(self):
        """ this function support powercycle device by power off/on multi pud ports"""
        
        log.debug("Entering powerCycleDevice3 class procedure: powerCycle")
        log.debug("powerCyclerPort3=[%s]" %str(self.powerCyclerPort3))
        print(self.managementPrompt)
        if 'Switched PDU' in self.managementPrompt:
            str1 = 'Username'
            str2 = 'Password'
            str3 = 'successful'
            on = 'On '
            off = 'Off '
        elif 'Switched CDU' in self.managementPrompt:
            str1 = 'Username'
            str2 = 'Password'
            str3 = 'successful'
            on = 'On '
            off = 'Off '
        elif 'apc' in self.managementPrompt:
            str1 = 'User Name'
            str2 = 'Password'
            str3 = 'successful'
            on = 'olOn '
            off = 'olOff '
        else:
            str1 = 'Username'
            str2 = 'Password'
            str3 = 'successful'
            on = 'On '
            off = 'Off '
        output = ''
        cmd = ("telnet " + self.managementIP + " " + self.managementPort + "\n")
        # issue telnet command
        child = pexpect.spawn(cmd)

        time.sleep(1)
        child.expect (str1, timeout=15)

        time.sleep(1)
        str_username = str(self.userName)
        LogMsg = str("\nsending username: [%s]" %str_username)
        log.debug(LogMsg)
        child.send(str_username)
        child.send('\x0d')

        time.sleep(1)
        child.expect (str2, timeout=15)

        time.sleep(1)
        str_password = str(self.password)
        LogMsg = str("\nsending password: [%s]" %str_password)
        log.debug(LogMsg)
        child.send(str_password)
        child.send('\x0d')

        # wait for prompt
        time.sleep(1)
        LogMsg = ("\nwaiting for prompt...")
        log.debug(LogMsg)
        child.expect (self.managementPrompt, timeout=15)
        time.sleep(1)

        # power off psu
        if isinstance(self.powerCyclerPort3, list):
            for port in self.powerCyclerPort3:
                cmd_off = off + str(port)
                child.send(cmd_off)
                child.send('\x0d')
                child.expect (str3, timeout=15)

        else:
            cmd_off = (off + str(self.powerCyclerPort3))
            child.send(cmd_off)
            child.send('\x0d')
            child.expect (str3, timeout=15)

        # wait for system to fully power off including fans
        time.sleep(30)

        # power on psu
        if isinstance(self.powerCyclerPort3, list):
            for port in self.powerCyclerPort3:
                cmd_on = on + str(port)
                child.send(cmd_on)
                child.send('\x0d')
                child.expect (str3, timeout=15)
        else:
            cmd_on = (on + str(self.powerCyclerPort3))
            child.send(cmd_on)
            child.send('\x0d')
            child.expect (str3, timeout=15)


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

        return output

    def powerCycleDevice1(self):
        """ this function support powercycle device by power off/on multi pud ports"""
        
        log.debug("Entering powerCycleDevice1 class procedure: powerCycle")
        log.debug("powerCyclerPort1=[%s]" %str(self.powerCyclerPort1))
        print(self.managementPrompt)
        if 'Switched PDU' in self.managementPrompt:
            str1 = 'Username'
            str2 = 'Password'
            str3 = 'successful'
            on = 'On '
            off = 'Off '
        elif 'Switched CDU' in self.managementPrompt:
            str1 = 'Username'
            str2 = 'Password'
            str3 = 'successful'
            on = 'On '
            off = 'Off '
        elif 'apc' in self.managementPrompt:
            str1 = 'User Name'
            str2 = 'Password'
            str3 = 'successful'
            on = 'olOn '
            off = 'olOff '
        else:
            str1 = 'Username'
            str2 = 'Password'
            str3 = 'successful'
            on = 'On '
            off = 'Off '
        output = ''
        cmd = ("telnet " + self.managementIP + " " + self.managementPort + "\n")
        # issue telnet command
        child = pexpect.spawn(cmd)

        time.sleep(1)
        child.expect (str1, timeout=15)

        time.sleep(1)
        str_username = str(self.userName)
        LogMsg = str("\nsending username: [%s]" %str_username)
        log.debug(LogMsg)
        child.send(str_username)
        child.send('\x0d')

        time.sleep(1)
        child.expect (str2, timeout=15)

        time.sleep(1)
        str_password = str(self.password)
        LogMsg = str("\nsending password: [%s]" %str_password)
        log.debug(LogMsg)
        child.send(str_password)
        child.send('\x0d')

        # wait for prompt
        time.sleep(1)
        LogMsg = ("\nwaiting for prompt...")
        log.debug(LogMsg)
        child.expect (self.managementPrompt, timeout=15)
        time.sleep(1)

        # power off psu
        if isinstance(self.powerCyclerPort1, list):
            for port in self.powerCyclerPort1:
                cmd_off = off + str(port)
                log.debug(cmd_off)
                child.send(cmd_off)
                child.send('\x0d')
                log.debug("power off")
                child.expect (str3, timeout=15)

        else:
            cmd_off = (off + str(self.powerCyclerPort1))
            log.debug(cmd_off)
            child.send(cmd_off)
            child.send('\x0d')
            log.debug("power off")
            child.expect (str3, timeout=15)

        # wait for system to fully power off including fans
        time.sleep(30)

        # power on psu
        if isinstance(self.powerCyclerPort1, list):
            for port in self.powerCyclerPort1:
                cmd_on = on + str(port)
                child.send(cmd_on)
                child.send('\x0d')
                child.expect (str3, timeout=15)
        else:
            cmd_on = (on + str(self.powerCyclerPort1))
            child.send(cmd_on)
            child.send('\x0d')
            child.expect (str3, timeout=15)


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

        return output

    def poweronDevice1(self):
        """ this function support power ON device by power ON multi pud ports"""

        log.debug("Entering powerCycleDevice1 class procedure: poweronDevice1")
        log.debug("powerCyclerPort1=[%s]" %str(self.powerCyclerPort1))
        print(self.managementPrompt)
        if 'Switched PDU' in self.managementPrompt:
            str1 = 'Username'
            str2 = 'Password'
            str3 = 'successful'
            on = 'On '
        elif 'Switched CDU' in self.managementPrompt:
            str1 = 'Username'
            str2 = 'Password'
            str3 = 'successful'
            on = 'On '
        elif 'apc' in self.managementPrompt:
            str1 = 'User Name'
            str2 = 'Password'
            str3 = 'successful'
            on = 'olOn '
        else:
            str1 = 'Username'
            str2 = 'Password'
            str3 = 'successful'
            on = 'On '
        output = ''
        cmd = ("telnet " + self.managementIP + " " + self.managementPort + "\n")
        # issue telnet command
        child = pexpect.spawn(cmd)

        time.sleep(1)
        child.expect (str1, timeout=15)

        time.sleep(1)
        str_username = str(self.userName)
        LogMsg = str("\nsending username: [%s]" %str_username)
        log.debug(LogMsg)
        child.send(str_username)
        child.send('\x0d')

        time.sleep(1)
        child.expect (str2, timeout=15)

        time.sleep(1)
        str_password = str(self.password)
        LogMsg = str("\nsending password: [%s]" %str_password)
        log.debug(LogMsg)
        child.send(str_password)
        child.send('\x0d')

        # wait for prompt
        time.sleep(1)
        LogMsg = ("\nwaiting for prompt...")
        log.debug(LogMsg)
        child.expect (self.managementPrompt, timeout=15)
        time.sleep(1)

        # power on psu
        if isinstance(self.powerCyclerPort1, list):
            for port in self.powerCyclerPort1:
                cmd_on = on + str(port)
                child.send(cmd_on)
                child.send('\x0d')
                child.expect (str3, timeout=15)
        else:
            cmd_on = (on + str(self.powerCyclerPort1))
            child.send(cmd_on)
            child.send('\x0d')
            child.expect (str3, timeout=15)


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

        return output

    def poweroffDevice1(self):
        """ this function support power off device by power off multi pud ports"""

        log.debug("Entering powerCycleDevice1 class procedure: poweroffDevice1")
        log.debug("powerCyclerPort1=[%s]" %str(self.powerCyclerPort1))
        print(self.managementPrompt)
        if 'Switched PDU' in self.managementPrompt:
            str1 = 'Username'
            str2 = 'Password'
            str3 = 'successful'
            off = 'Off '
        elif 'Switched CDU' in self.managementPrompt:
            str1 = 'Username'
            str2 = 'Password'
            str3 = 'successful'
            off = 'Off '
        elif 'apc' in self.managementPrompt:
            str1 = 'User Name'
            str2 = 'Password'
            str3 = 'successful'
            off = 'olOff '
        else:
            str1 = 'Username'
            str2 = 'Password'
            str3 = 'successful'
            off = 'Off '
        output = ''
        cmd = ("telnet " + self.managementIP + " " + self.managementPort + "\n")
        # issue telnet command
        child = pexpect.spawn(cmd)

        time.sleep(1)
        child.expect (str1, timeout=15)

        time.sleep(1)
        str_username = str(self.userName)
        LogMsg = str("\nsending username: [%s]" %str_username)
        log.debug(LogMsg)
        child.send(str_username)
        child.send('\x0d')

        time.sleep(1)
        child.expect (str2, timeout=15)

        time.sleep(1)
        str_password = str(self.password)
        LogMsg = str("\nsending password: [%s]" %str_password)
        log.debug(LogMsg)
        child.send(str_password)
        child.send('\x0d')

        # wait for prompt
        time.sleep(1)
        LogMsg = ("\nwaiting for prompt...")
        log.debug(LogMsg)
        child.expect (self.managementPrompt, timeout=15)
        time.sleep(1)

        # power off psu
        if isinstance(self.powerCyclerPort1, list):
            for port in self.powerCyclerPort1:
                cmd_off = off + str(port)
                log.debug(cmd_off)
                child.send(cmd_off)
                child.send('\x0d')
                log.debug("power off")
                child.expect (str3, timeout=15)

        else:
            cmd_off = (off + str(self.powerCyclerPort1))
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

        return output

    def poweronDevice3(self):
        """ this function support power ON device by power ON multi pud ports"""

        log.debug("Entering powerCycleDevice1 class procedure: poweronDevice3")
        log.debug("powerCyclerPort3=[%s]" %str(self.powerCyclerPort3))
        print(self.managementPrompt)
        if 'Switched PDU' in self.managementPrompt:
            str1 = 'Username'
            str2 = 'Password'
            str3 = 'successful'
            on = 'On '
        elif 'Switched CDU' in self.managementPrompt:
            str1 = 'Username'
            str2 = 'Password'
            str3 = 'successful'
            on = 'On '
        elif 'apc' in self.managementPrompt:
            str1 = 'User Name'
            str2 = 'Password'
            str3 = 'successful'
            on = 'olOn '
        else:
            str1 = 'Username'
            str2 = 'Password'
            str3 = 'successful'
            on = 'On '
        output = ''
        cmd = ("telnet " + self.managementIP + " " + self.managementPort + "\n")
        # issue telnet command
        child = pexpect.spawn(cmd)

        time.sleep(1)
        child.expect (str1, timeout=15)

        time.sleep(1)
        str_username = str(self.userName)
        LogMsg = str("\nsending username: [%s]" %str_username)
        log.debug(LogMsg)
        child.send(str_username)
        child.send('\x0d')

        time.sleep(1)
        child.expect (str2, timeout=15)

        time.sleep(1)
        str_password = str(self.password)
        LogMsg = str("\nsending password: [%s]" %str_password)
        log.debug(LogMsg)
        child.send(str_password)
        child.send('\x0d')

        # wait for prompt
        time.sleep(1)
        LogMsg = ("\nwaiting for prompt...")
        log.debug(LogMsg)
        child.expect (self.managementPrompt, timeout=15)
        time.sleep(1)

        # power on psu
        if isinstance(self.powerCyclerPort3, list):
            for port in self.powerCyclerPort3:
                cmd_on = on + str(port)
                child.send(cmd_on)
                child.send('\x0d')
                child.expect (str3, timeout=15)
        else:
            cmd_on = (on + str(self.powerCyclerPort3))
            child.send(cmd_on)
            child.send('\x0d')
            child.expect (str3, timeout=15)


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

        return output

    def poweroffDevice3(self):
        """ this function support power off device by power off multi pud ports"""

        log.debug("Entering powerCycleDevice1 class procedure: poweroffDevice3")
        log.debug("powerCyclerPort3=[%s]" %str(self.powerCyclerPort3))
        print(self.managementPrompt)
        if 'Switched PDU' in self.managementPrompt:
            str1 = 'Username'
            str2 = 'Password'
            str3 = 'successful'
            off = 'Off '
        elif 'Switched CDU' in self.managementPrompt:
            str1 = 'Username'
            str2 = 'Password'
            str3 = 'successful'
            off = 'Off '
        elif 'apc' in self.managementPrompt:
            str1 = 'User Name'
            str2 = 'Password'
            str3 = 'successful'
            off = 'olOff '
        else:
            str1 = 'Username'
            str2 = 'Password'
            str3 = 'successful'
            off = 'Off '
        output = ''
        cmd = ("telnet " + self.managementIP + " " + self.managementPort + "\n")
        # issue telnet command
        child = pexpect.spawn(cmd)

        time.sleep(1)
        child.expect (str1, timeout=15)

        time.sleep(1)
        str_username = str(self.userName)
        LogMsg = str("\nsending username: [%s]" %str_username)
        log.debug(LogMsg)
        child.send(str_username)
        child.send('\x0d')

        time.sleep(1)
        child.expect (str2, timeout=15)

        time.sleep(1)
        str_password = str(self.password)
        LogMsg = str("\nsending password: [%s]" %str_password)
        log.debug(LogMsg)
        child.send(str_password)
        child.send('\x0d')

        # wait for prompt
        time.sleep(1)
        LogMsg = ("\nwaiting for prompt...")
        log.debug(LogMsg)
        child.expect (self.managementPrompt, timeout=15)
        time.sleep(1)

        # power off psu
        if isinstance(self.powerCyclerPort3, list):
            for port in self.powerCyclerPort3:
                cmd_off = off + str(port)
                log.debug(cmd_off)
                child.send(cmd_off)
                child.send('\x0d')
                log.debug("power off")
                child.expect (str3, timeout=15)

        else:
            cmd_off = (off + str(self.powerCyclerPort3))
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

        return output

    def powerCycleDevice(self):
        """ this function support powercycle device by power off/on multi pud ports"""
        
        log.debug("Entering powerCycleDevice class procedure: powerCycle")
        log.debug("powerCyclerPort=[%s]" %str(self.powerCyclerPort))
        print(self.managementPrompt)
        if 'Switched PDU' in self.managementPrompt:
            str1 = 'Username'
            str2 = 'Password'
            str3 = 'successful'
            on = 'On '
            off = 'Off '
        elif 'Switched CDU' in self.managementPrompt:
            str1 = 'Username'
            str2 = 'Password'
            str3 = 'successful'
            on = 'On '
            off = 'Off '
        elif 'apc' in self.managementPrompt:
            str1 = 'User Name'
            str2 = 'Password'
            str3 = 'successful'
            on = 'olOn '
            off = 'olOff '
        else:
            str1 = 'Username'
            str2 = 'Password'
            str3 = 'successful'
            on = 'On '
            off = 'Off '
        output = ''
        cmd = ("telnet " + self.managementIP + " " + self.managementPort + "\n")
        # issue telnet command
        child = pexpect.spawn(cmd)

        time.sleep(1)
        child.expect (str1, timeout=15)

        time.sleep(1)
        str_username = str(self.userName)
        LogMsg = str("\nsending username: [%s]" %str_username)
        log.debug(LogMsg)
        child.send(str_username)
        child.send('\x0d')

        time.sleep(1)
        child.expect (str2, timeout=15)

        time.sleep(1)
        str_password = str(self.password)
        LogMsg = str("\nsending password: [%s]" %str_password)
        log.debug(LogMsg)
        child.send(str_password)
        child.send('\x0d')

        # wait for prompt
        time.sleep(1)
        LogMsg = ("\nwaiting for prompt...")
        log.debug(LogMsg)
        child.expect (self.managementPrompt, timeout=15)
        time.sleep(1)

        # power off psu
        if isinstance(self.powerCyclerPort, list):
            for port in self.powerCyclerPort:
                cmd_off = off + str(port)
                child.send(cmd_off)
                child.send('\x0d')
                child.expect (str3, timeout=15)

        else:
            cmd_off = (off + str(self.powerCyclerPort))
            child.send(cmd_off)
            child.send('\x0d')
            child.expect (str3, timeout=15)

        # wait for system to fully power off including fans
        time.sleep(30)

        # power on psu
        if isinstance(self.powerCyclerPort, list):
            for port in self.powerCyclerPort:
                cmd_on = on + str(port)
                child.send(cmd_on)
                child.send('\x0d')
                child.expect (str3, timeout=15)
        else:
            cmd_on = (on + str(self.powerCyclerPort))
            child.send(cmd_on)
            child.send('\x0d')
            child.expect (str3, timeout=15)


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

        return output

