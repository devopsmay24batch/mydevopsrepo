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
from dataStructure import nestedDict, parser
import CommonLib
import Const
import DeviceMgr
#from Device import Device
import Logger as log

BOOTING_TIME = 300

class SdkLib:
    def __init__(self, device):
        self.device = device


    def ssh_login_bmc(self):
        CommonLib.ssh_login_bmc(Const.DUT)
        self.device = DeviceMgr.getDevice()


    def ssh_disconnect(self):
        CommonLib.ssh_disconnect(Const.DUT)
        self.device = DeviceMgr.getDevice()


    def set_verbose_level(self, verb_level):
        cmd = ('export VERB_LEVEL=' + str(verb_level))
        return self.wpl_execute(cmd)


    def powerCycleToCentOS(self):
        self.wpl_powerCycle()
        return self.wpl_getPrompt('centos', timeout=BOOTING_TIME)


    def powerCycleToOpenBmc(self):
        self.wpl_powerCycle()
        return self.wpl_getPrompt('openbmc', timeout=BOOTING_TIME)


    #######################################
    ### Wrapper Device Library Function ###
    #######################################
    def wpl_transmit(self, cmd, CR=True):
        return self.wpl_sendline(cmd, CR)


    def wpl_sendline(self, cmd, CR=True):
        if (CR == True):
            msg = (cmd + '\r')
        else:
            msg = cmd
        return self.device.sendMsg(msg)


    def wpl_sendCmd(self, cmd, prompt=None):
        return self.device.sendCmd(cmd, prompt)


    def wpl_flush(self):
        return self.device.flush()


    def wpl_receive(self, rcv_str, timeout=60):
        return self.device.receive(rcv_str, timeout)


    def wpl_execute(self, cmd, mode=None, timeout=60):
        return self.device.execute(cmd, mode, timeout)

    def wpl_execute_cmd(self, cmd, mode=None, timeout=60):
        return self.device.executeCmd(cmd, mode, timeout)


    def wpl_getPrompt(self, mode=None, timeout=60, idleTimeout=60):
        return self.device.getPrompt(mode, timeout, idleTimeout)


    def wpl_getCurrentPromptStr(self):
        return self.device.getCurrentPromptStr()


    def wpl_getDiagOSPromptStr(self):
        return self.device.promptDiagOS


    def wpl_getBmcPromptStr(self):
        return self.device.promptBmc


    def wpl_getCurrentBootMode(self):
         return self.device.getCurrentBootMode()


    def wpl_powerCycle(self):
        return self.device.powerCycle()


    def wpl_raiseException(self, msg):
        raise RuntimeError(msg)


    def wpl_log_debug(self, msg):
        return log.debug(msg)


    def wpl_log_error(self, msg):
        return log.error(msg)


    def wpl_log_info(self, msg):
        return log.info(msg)


    def wpl_log_success(self, msg):
        return log.success(msg)


    def wpl_log_fail(self, msg):
        return log.fail(msg)


