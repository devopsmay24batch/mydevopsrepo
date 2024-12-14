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
from robot.libraries.Telnet import Telnet
import Const
import pexpect
import sys
import re
import time
import Logger as log
from Decorator import logThis

class TelnetDevice(object):
    def __init__(self):
        self.telnetConnect = Telnet()
        self.enable_terminal_log_file = '0'

    def set_terminal_log_file(self, set_flag):
        if set_flag == '0':
            log.debug("Disable terminal log file feature.")
        else:
            log.debug("Enable terminal log file feature.")

        self.enable_terminal_log_file = set_flag

    def login(self):
        pass

    def disconnect(self):
        self.telnetConnect.close_connection()
        time.sleep(5)
        return

###### frequently used functions begin ########

    def readUntil(self, msgStr, timeout = None):
        log.debug('Entering procedure readUntil with args : %s\n' % (str(locals())))
        if timeout == None:
            return self.telnetConnect.read_until(msgStr)

        self.setConnectionTimeout(timeout)
        ret = self.telnetConnect.read_until(msgStr)
        self.setConnectionTimeout(Const.TELNET_CONN_TIMEOUT_DEFAULT)
        return  ret

    def read_until_regexp(self, pattern_list, timeout=None):
        log.debug('Entering procedure read_until_regexp with args : %s\n' % (str(locals())))
        if timeout == None:
            output = self.telnetConnect.read_until_regexp(pattern_list)
            self.output = output
            return output

        self.setConnectionTimeout(timeout)
        output = self.telnetConnect.read_until_regexp(pattern_list)
        self.setConnectionTimeout(Const.TELNET_CONN_TIMEOUT_DEFAULT)
        self.output = output
        return output

    def sendMsg(self, msg):
        return self.telnetConnect.write_bare(msg)

    def sendCmd(self, cmd, promptStr = None, timeout = None):
        log.debug('Entering procedure sendCmd with args : %s\n' % (str(locals())))
        self.telnetConnect.write(cmd)
        if promptStr == None:
            return ''

        if timeout == None:
            ret = self.telnetConnect.read_until(promptStr)
            self.send_output_to_log_file(ret)
            return ret

        self.setConnectionTimeout(timeout)
        ret =  self.telnetConnect.read_until(promptStr)
        self.setConnectionTimeout(Const.TELNET_CONN_TIMEOUT_DEFAULT)
        self.send_output_to_log_file(ret)
        return ret

    def sendCmdRegexp(self, cmd, promptRegexp, timeout =Const.TELNET_CONN_TIMEOUT_DEFAULT):
        log.debug('Entering procedure sendCmdRegexp with args : %s\n' % (str(locals())))
        self.setConnectionTimeout(timeout)
        self.telnetConnect.write(cmd)
        ret = self.telnetConnect.read_until_regexp(promptRegexp)
        sys.stdout.flush()
        self.setConnectionTimeout(Const.TELNET_CONN_TIMEOUT_DEFAULT)
        self.send_output_to_log_file(ret)
        return ret

    @logThis
    def executeCmd(self, cmd, mode=None, timeout=60):
        """ this function can't be used on the mode not supporting time operation ! """

        if mode != None:
            self.getPrompt(mode, timeout)
        cmd = 'time ' + cmd
        self.flush()
        return self.sendCmdRegexp(cmd, Const.TIME_REG_PROMPT, timeout)

    @logThis
    def executeCommand(self, cmd, prompt, mode=None, timeout=60):
        """ this function can be used on the mode not supporting time operation """

        if mode != None:
            self.getPrompt(mode, timeout)
        self.flush()
        due_prompt = self.escapeString(cmd.lstrip()[:5])
        finish_prompt = "{}[\s\S]+{}".format(due_prompt, prompt)
        return self.sendCmdRegexp(cmd, finish_prompt, timeout)


    @logThis
    def runCmd(self, cmd, prompt, mode=None, timeout=60):
        """ this api will check the exit code after execute it;
         this api can be used in the mode do not support time operation
         :param prompt: the prompt after executing the cmd
        """
        output = self.executeCommand(cmd, prompt, mode, timeout)
        out = self.executeCommand('echo $?', prompt)
        for line in out.splitlines():
            if re.search(r'^0$', line):
                log.success('check exit code successfully.')
                return output
        raise RuntimeError('check exit code failed!')


    @logThis
    def execCmd(self, cmd, mode=None, timeout=60):
        """ this api will check the exit code after execute it, can be used in the mode support time operation """

        output = self.executeCmd(cmd, mode, timeout)
        self.check_exit_code()
        return output


    def flush(self):
        self.sendMsg('\r\n')
        self.readMsg()
        self.output = ''
        self.telnetConnect.before = ''
        self.telnetConnect.after = ''
        self.telnetConnect.buffer= ''
        return


    @logThis
    def check_exit_code(self):
        out = self.executeCmd('echo $?')
        for line in out.splitlines():
            if re.search(r'^0$', line):
                log.success('check exit code successfully.')
                return
        raise RuntimeError('check exit code failed!')

###### frequently used functions end ########

    def readMsg(self):
        output = self.telnetConnect.read()
        self.output = output
        return output

    def transmit(self, cmd, CR=True, WP=False):
        if WP == False:
            return self.sendline(cmd, CR)
        else:
            patternList = re.compile(r'^(root@)([\w,\:,\/,\d,\-]+)*#')
            self.sendline(cmd, CR)
            output = self.read_until_regexp(patternList)
            self.send_output_to_log_file(output)
            return output

    def sendline(self, cmd='', CR=True):
        if (CR == True):
            msg = (cmd + '\r\n')
        else:
            msg = cmd
        return self.sendMsg(msg)

    def receive(self, pattern_str, timeout=60):
        self.setConnectionTimeout(timeout)
        time.sleep(3)
        if isinstance(pattern_str, str):
            if '<match all>' in pattern_str:
                output = self.readMsg()
                self.output = output
                return output
            else:
                pattern_list = re.compile(pattern_str)
                output = self.readUntil(pattern_str)
                self.output = output
                return output
        else:
            pattern_list = re.compile('|'.join(pattern_str))
            try:
                output = self.read_until_regexp(pattern_list)
                self.output = output
                return output
            except pexpect.EOF as err:
                try:
                    output = self.telnetConnect.before
                    self.output = output
                    raise
                except:
                    raise
            except pexpect.TIMEOUT as err:
                output = self.telnetConnect.before
                self.output = output
                raise

    def send_output_to_log_file(self, output, logFile=Const.UART_LOG):
        if self.enable_terminal_log_file != '0':
            # save stdout
            old_stdout = sys.stdout
            with open(logFile, 'a+') as fd:
                sys.stdout = fd
                # write output to log file
                for line in output.splitlines(True):
                    lineStr = line.strip()
                    if len(lineStr) == 0:
                        continue
                    else:
                        print("%s" %line)
            # restore stdout
            sys.stdout = old_stdout

    def escapeString(self, string):
        special_characters = {
            '.' : '\.',
            '*' : '\*',
            '(' : '\(',
            ')' : '\)',
            '?' : '\?',
            '|' : '\|',
            '+' : '\+',
            '$' : '\$',
            '[' : '\[',
            ']' : '\]'
        }
        for key, value in special_characters.items():
            string = string.replace(key, value)

        return string

    def setConnectionTimeout(self, timeout):
        """ should not use this function outside TelnetDevice, it should be a private method"""
        return self.telnetConnect.set_timeout(timeout)