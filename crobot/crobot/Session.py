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
import pexpect
import Logger as log
import Const
import time
import sys
import re
class Session:

    def __init__(self):
        self.child = None
        self.output = ''
        self.timeout = 10

    def connect(self, username, ipAddr, port=None, protocol=Const.PROTOCOL_SSH):
        log.debug('Entering Session class procedure connect with args : %s\n' % (str(locals())))
        self.username = username
        self.ipAddr = ipAddr
        self.protocol = protocol

        if self.protocol == Const.PROTOCOL_SSH:
            cmd = "ssh -o StrictHostKeyChecking=no -l %s " % self.username
        else:
            cmd = "telnet "
        cmd += ipAddr
        if port != None:
            cmd +=  ' ' + str(port)
        # cmd += '\n'
        log.info('cmd: %s' %(cmd))

        #  for using of pexpect, refer  https://pexpect.readthedocs.io/en/stable/overview.html
        self.child = pexpect.spawn(cmd, encoding='utf-8')
        # self.child = pexpect.spawn(cmd)
        self.child.sendline()
        self.child.logfile = sys.stdout
        self.child.logfile_read = sys.stdout

    def disconnect(self):
        self.child.close()
        self.child.logfile_read.close()

    def loginDev(self, username, password):
        log.debug('Entering Session class procedure loginDev with args : %s\n' % (str(locals())))
        if self.protocol == Const.PROTOCOL_TELNET:
            self.child.sendline(username)
            try:
                self.child.expect(Const.PSW_PROMT, 10)
            except pexpect.TIMEOUT:
                raise RuntimeError("can't login device")
        try:
            self.child.sendline()
            self.child.expect('password:', 20)
            self.child.sendline(password)
        except Exception as err:
            out = self.child.before
            log.cprint(str(out))
            log.cprint(str(err))
            raise RuntimeError("login device failed")

    def setConnectionTimeout(self, timeout):
        self.timeout = timeout

    def sendMsg(self, msg):
        return str(self.child.send(msg))

    def transmit(self, cmd, CR=True):
        log.debug('Entering Session class procedure transmit with args : %s\n' % (str(locals())))
        if CR:
            return str(self.child.sendline(cmd))
        else:
            return str(self.send(cmd))

    def sendCmd(self, cmd, promptStr = None, timeout = None):
        log.debug('Entering Session class procedure sendCmd with args : %s\n' % (str(locals())))
        self.child.sendline(cmd)
        if promptStr == None:
            return ''
        if timeout == None:
            timeout = self.timeout
        return self.readUntil(promptStr, timeout)

    def readMsg(self):
        out =  str(self.child.read_nonblocking(1024, 10))
        log.info(out)
        return out

    def readUntil(self, msgStr, timeout = None):
        log.debug('Entering Session class procedure readUntil with args : %s\n' % (str(locals())))
        if timeout is None:
            timeout = self.timeout
        out = ''
        if int(timeout) < int(Const.SSH_MAX_TIMEOUT):
            try:
                self.child.expect(msgStr, timeout)
                out = str(self.child.before + self.child.after)
                log.info('output is: ' + out)
            except pexpect.exceptions.TIMEOUT as err:
                out = str(self.child.before)
                log.info('timeout, and output is: ' + out)
                raise pexpect.exceptions.TIMEOUT(str(err))
            return out

        count = timeout // Const.SSH_MAX_TIMEOUT + 1
        for i in range(count):
            try:
                self.child.expect(msgStr, Const.SSH_MAX_TIMEOUT)
                out = str(self.child.before + self.child.after)
                log.info(out)
                return out
            except:
                log.info('Try the {} time'.format(i + 1))
                out = str(self.child.before)
                self.child.sendline(' ')
                pass
        log.info(out)
        raise RuntimeError('Timeout: Wait expected string {} Failed!'.format(msgStr))

    def read_until_regexp(self, pattern_list, timeout=None):
        log.debug('Entering Session class procedure read_until_regexp with args : %s\n' % (str(locals())))
        return self.readUntil(pattern_list, timeout)

    def sendCmdRegexp(self, cmd, promptRegexp, timeout=Const.TELNET_CONN_TIMEOUT_DEFAULT):
        log.debug('Entering Session class procedure sendCmdRegexp with args : %s\n' % (str(locals())))
        self.child.sendline(cmd)
        return self.readUntil(promptRegexp, timeout)

    def execute(self, cmd, mode=None, exe_timeout=60):
        log.debug('Entering Session class procedure execute with args : %s\n' % (str(locals())))
        if mode != None:
            self.getPrompt(mode, exe_timeout)
        self.child.sendline()
        self.child.expect(self.getCurrentPromptStr(), 3)
        self.flush()
        self.child.sendline(cmd + ' 2>&1')
        return self.readUntil(self.getCurrentPromptStr(), exe_timeout)

    def receive(self, pattern, timeout=-1):
        try:
            cpl = self.child.compile_pattern_list(pattern)
            self.child.expect(cpl,timeout)
            out = self.child.before + self.child.after
            log.info(str(out))
            return str(out)
        except pexpect.EOF as err:
            out = self.child.before
            log.info(str(out))
            raise RuntimeError("Connection to device is terminated!")
        except pexpect.TIMEOUT as err:
            out = self.child.before
            log.info(str(out))
            if pattern != Const.MATCH_ALL:
                raise RuntimeError("Prompt cannot be reached!")
            else:
                return str(out)
        except Exception as err:
            log.cprint(str(err))

    def flush(self):
        self.receive(Const.MATCH_ALL,1)
        self.output = ''
        self.child.before = ''
        self.child.after = ''
        self.child.buffer= ''
        self.child.flush()

    def getCurrentPromptStr(self):
        pass

    def executeCmd(self, cmd, mode=None, timeout=60):
        log.debug('Entering Session class executeCmd with args : %s\n' % (str(locals())))
        if mode != None:
            self.getPrompt(mode, timeout)
        cmd = 'time ' + cmd
        self.flush()
        return self.sendCmdRegexp(cmd, Const.TIME_REG_PROMPT, timeout)
