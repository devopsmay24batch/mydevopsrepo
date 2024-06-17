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
import datetime
from Diag_OS_variable import *
import parserDIAGLibs
from DiagLib import *
import CommonLib
import os
from Decorator import *

BOOTING_TIME=900


class DiagLibClass(DiagLib):
    def __init__(self, device):
        DiagLib.__init__(self, device)
        self.bios_version = '0'
        self.bmc_version = '0'

        self._psu_diag = []
        self._psu_openbmc = []


#######################################################################################################################
# Function Name: switch_to_centos_and_go_to_diag_tool
# Date         : 12nd February 2020
# Author       : Phawit P. <Phaphan@celestica.com>
#
# Procedure Revision Details:
#   Version : 1.0  - Initial Draft  - by Phawit P. <Phaphan@celestica.com>
#######################################################################################################################
    def switch_to_centos_and_go_to_diag_tool(self):
        self.wpl_log_debug('Entering procedure switch_to_centos_and_go_to_diag_tool\n')
        cmd = 'cd ' + DIAG_TOOL_PATH
        CommonLib.switch_to_centos()
        self.wpl_transmit(cmd)



#######################################################################################################################
# Function Name: switch_to_centos_and_go_to_system_log_path
# Date         : 28nd June 2020
# Author       : hemin <hemin@celestica.com>
#
# Procedure Revision Details:
#   Version : 1.0  - Initial Draft  - by hemin <hemin@celestica.com>
#######################################################################################################################
    def switch_to_centos_and_go_to_diag_system_log_path(self):
        self.wpl_log_debug('Entering procedure switch_to_centos_and_go_to_diag_system_log_path\n')
        cmd = 'cd ' + FPGA_TOOL_PATH
        CommonLib.switch_to_centos()
        self.wpl_transmit(cmd)


#######################################################################################################################
# Function Name: switch_to_openbmc_and_check_tool
# Date         : 12nd February 2020
# Author       : Phawit P. <Phaphan@celestica.com>
#
# Procedure Revision Details:
#   Version : 1.0  - Initial Draft  - by Phawit P. <Phaphan@celestica.com>
#######################################################################################################################
    def switch_to_openbmc_and_check_tool(self):
        self.wpl_log_debug('Entering procedure switch_to_openbmc_and_check_tool\n')
        CommonLib.switch_to_openbmc()
        self.check_bmc_diag_tool()



#######################################################################################################################
# Function Name: check_bmc_diag_tool
# Date         : 13th February 2020
# Author       : Phawit P. <Phaphan@celestica.com>
#
# Procedure Revision Details:
#   Version : 1.0  - Initial Draft  - by Phawit P. <Phaphan@celestica.com>
#######################################################################################################################
    def check_bmc_diag_tool(self):
        self.wpl_log_debug('Entering procedure check_bmc_diag_tool\n')
        if CommonLib.check_file_exist(BMC_DIAG_TOOL_PATH, openbmc_mode) == False:
            CommonLib.mount_data(BLK_DEV_PATH, BMC_BLK_MOUNT_PATH, openbmc_mode)


#######################################################################################################################
# Function Name: EXEC_diag_tool_command
# Date         : 27th January 2020
# Author       : Phawit P. <Phaphan@celestica.com>
#
# Procedure Revision Details:
#   Version : 1.0  - Initial Draft  - by Phawit P. <Phaphan@celestica.com>
#######################################################################################################################
    def EXEC_diag_tool_command(self, toolName, option, path=DIAG_TOOL_PATH, mode="centos"):
        if toolName == "lspci -s":
            cmd = toolName + ' ' + option
        else:
            cmd = path + toolName + ' ' + option
        self.wpl_log_debug("command = %s" %(cmd))
        return self.wpl_execute(cmd, mode=mode, timeout=600)


#######################################################################################################################
# Function Name: EXEC_diag_sys_log_tool_command
# Date         : 29th June 2020
# Author       : hemin <hemin@celestica.com>
#
# Procedure Revision Details:
#   Version : 1.0  - Initial Draft  - by hemin <hemin@celestica.com>
#######################################################################################################################
    def EXEC_diag_sys_log_tool_command(self, toolName, option, fileName='', path=FPGA_TOOL_PATH):
        cmd ='./' + toolName + ' ' + option + ' ' + fileName
        self.wpl_log_debug("command = %s" %(cmd))
        return self.wpl_execute(cmd, mode='centos', timeout=600)

#######################################################################################################################
# Function Name: EXEC_flashcp_flashfuji_lever
# Date         : 21th Seq 2020
# Author       : Eric Zhang <zfzhang@celestica.com>
#
# Procedure Revision Details:
#   Version : 1.0  - Initial Draft  - by Eric Zhang <zfzhang@celestica.com>
#######################################################################################################################
    def EXEC_flashcp_flashfuji_lever(self, toolName, flashdevice, option, path=BMC_DIAG_TOOL_PATH):
        if path:
            cmd = 'cd ' + path
            self.wpl_transmit(cmd)

        command = toolName + ' ' + flashdevice + ' ' + option
        self.wpl_log_debug('cammand = %s' % command)
        self.wpl_execute(command, mode="openbmc", timeout=600)
        self.wpl_getPrompt("openbmc", 60)
        output = self.wpl_execute("echo $?", mode="openbmc", timeout=30)
        self.wpl_log_debug(output)
        for line in output.splitlines():
            line = line.strip()
            match = re.search('^0$',line)
            if match:
                passCount += 1
        if passCount:
            self.wpl_log_success("Successfully used %s to flash BMC image")
        else:
            self.wpl_raiseException("Failed using %s to flash BMC image")

    def test_scm_cpld_accessed(self, toolName, option, keywords=None, path = None):
        self.wpl_log_debug('Entering procedure test_scm_cpld_accessed with args : %s' % (str(locals())))
        if path:
            cmd = 'cd ' + path
            self.wpl_transmit(cmd)

        cmd = toolName + ' ' + option
        output = self.wpl_execute_cmd(cmd, timeout=600)
        count = 0
        len_key = len(keywords)
        for line in output.splitlines():
            line = line.strip()
            for i in range(len_key):
                match = re.search(keywords[i],line)
                if match:
                    count += 1
        self.wpl_log_debug("count=%s" %count)
        if count == 1:
            self.wpl_log_success('verify_device_write_read test result for DIAG tool - %s is PASSED\n' % toolName)
        else:
            self.wpl_log_fail('Exiting verify_device_write_read with result FAIL')
            self.wpl_raiseException("Failure while testing DIAG tool '%s'" % (toolName))
#######################################################################################################################
# Function Name: flash_option_v_upgrade_level
# Date         : 21th Seq 2020
# Author       : Eric Zhang <zfzhang@celestica.com>
#
# Procedure Revision Details:
#   Version : 1.0  - Initial Draft  - by Eric Zhang <zfzhang@celestica.com>
#######################################################################################################################
    def flash_option_v_upgrade_level(self, toolName, flashdevice, option, path=BMC_DIAG_TOOL_PATH):
        if path:
            cmd = 'cd ' + path
            self.wpl_transmit(cmd)

        cmd1 = "ls | grep -E 'flash-wedge400.*?bin'"
        output = self.wpl_execut_cmd(cmd1, mode='openbmc', timeout=30)
        for line in output.splitlines():
            line = line.strip()
            match = re.search = ('^flash', line)
            if match:
                match_put = match
                break

        command = toolName + ' ' + option + ' ' + match_put + ' ' + flashdevice
        self.wpl_log_debug('cammand = %s' % command)
        self.wpl_execute(command, mode="openbmc", timeout=600)
        self.wpl_getPrompt("openbmc", 60)
        output1 = self.wpl_execute("echo $?", mode="openbmc", timeout=30)
        self.wpl_log_debug(output1)
        for line1 in output1.splitlines():
            line1 = line1.strip()
            match = re.search('^0$', line1)
            if match:
                passCount += 1
        if passCount:
            self.wpl_log_success("Successfully used %s to flash BMC image")
        else:
            self.wpl_raiseException("Failed using %s to flash BMC image")

#######################################################################################################################
# Function Name: EXEC_bmc_diag_tool_command
# Date         : 12th February 2020
# Author       : Phawit P. <Phaphan@celestica.com>
#
# Procedure Revision Details:
#   Version : 1.0  - Initial Draft  - by Phawit P. <Phaphan@celestica.com>
#######################################################################################################################
    def EXEC_bmc_diag_tool_command(self, toolName, option, path=BMC_DIAG_TOOL_PATH, prefix="./"):
        cmd = ('cd ' + path)
        self.wpl_log_debug("command = %s" %(cmd))
        self.wpl_getPrompt("openbmc", 600)

        if toolName == 'boot_info.sh' and option =='bmc':
            cmd = toolName + ' ' + option
        if path != "":
            self.wpl_transmit(cmd)

        if option == ' ':
            cmd = toolName
        elif toolName == 'ifconfig':
            cmd = toolName + ' ' + option
        elif option == ' fpga --version':
            cmd = toolName + option
        elif toolName == "cel-boot-test" and "wedge_power.sh off" in option:
            if "-b bios -r slave" in option or "-b bios -r master" in option:
                cmd = option
        else:
            cmd = prefix + toolName + ' ' + option
            if toolName == 'cpld_update.sh':
                cmd = toolName + ' ' + option
        self.wpl_log_debug("command = %s" %(cmd))
        return self.wpl_execute_cmd(cmd, mode=openbmc_mode, timeout=600)

#######################################################################################################################
# Function Name: EXEC_centos_diag_tool_command
# Date         : 12th February 2020
# Author       : Phawit P. <Phaphan@celestica.com>
#
# Procedure Revision Details:
#   Version : 1.0  - Initial Draft  - by Phawit P. <Phaphan@celestica.com>
#######################################################################################################################
    def EXEC_centos_diag_tool_command(self, toolName, option, path=None):
        if path:
          cmd = ('cd ' + path)
          self.wpl_log_debug("command = %s" %(cmd))
          self.wpl_getPrompt("centos", 1800)
          self.wpl_transmit(cmd)

        cmd1 = '../utility/fpga reg w 0x18 0xffff0000'
        self.wpl_transmit(cmd1)
        cmd = toolName + ' ' + option
        self.wpl_log_debug("command = %s" %(cmd))
        return self.wpl_execute_cmd(cmd, mode=centos_mode, timeout=1800)

#######################################################################################################################
# Function Name: clean_diag_rpm_package
# Date         : 7th Seq 2020
# Author       : Eric Zhang <zfzhang@celestica.com>
#
# Procedure Revision Details:
#   Version : 1.0  - Initial Draft  - by Eric Zhang <zfzhang@celestica.com>
#######################################################################################################################
    def clean_diag_rpm_package(self, toolName, option, pass_pattern = None, path=None):
        self.wpl_log_debug('Entering procedure clean diag rpm package : %s\n' % (str(locals())))
        cmd = toolName + option
        output = self.wpl_execute(cmd, mode='centos', timeout=1200)
        self.wpl_log_debug('output=%s' % output)

#######################################################################################################################
# Function Name: execute_raw_get_command
# Date         : 30th January 2020
# Author       : Phawit P. <Phaphan@celestica.com>
#
# Procedure Revision Details:
#   Version : 1.0  - Initial Draft  - by Phawit P. <Phaphan@celestica.com>
#######################################################################################################################
    def execute_raw_get_command(self, toolName, netfn, command_str, expected_result='None', test_name='None'):
        self.wpl_log_debug('Entering procedure execute_oem_get_command : %s\n'%(str(locals())))
        if test_name == 'None':
            test_name = 'execute_raw_get_command'
        cmd = toolName + ' ' + netfn + ' ' + command_str
        output = self.wpl_execute(cmd)
        self.wpl_log_debug('output=%s'% output)
        result = parserDIAGLibs.PARSE_raw_output(output)
        self.wpl_log_debug('result = %s'%(result))
        if expected_result != 'None':
            if (result == expected_result):
                self.wpl_log_success("PASS: %s \'%s\': result: \'%s\'"%(test_name, cmd, result))
            else:
                self.wpl_log_fail("Command result Mismatch: Found \'%s\' Expected \'%s\'\n"%(result, expected_result))
                self.wpl_raiseException("Failed %s"%(test_name))
        else:
            return result


#######################################################################################################################
# Function Name: switch_mcelog_to_daemon_mode
# Date         : 2th July 2020
# Author       : hemin <hemin@celestica.com>
#
# Procedure Revision Details:
#   Version : 1.0  - Initial Draft  - by hemin <hemin@celestica.com>
#######################################################################################################################
    def switch_mcelog_to_daemon_mode(self, CMDName, option):
        self.wpl_log_debug('Entering procedure switch_mcelog_to_daemon_mode with args : %s' % (str(locals())))
        cmd = CMDName + " " + option
        self.wpl_log_debug("command = %s" % (cmd))
        self.wpl_getPrompt("centos", 600)
        log_count = 0
        output = self.wpl_execute(cmd, mode='centos', timeout=600)
        for line in output.splitlines():
            line = line.strip()
            line = line.strip("\n")
            if line.endswith("#") or line.endswith(cmd) or line.endswith(''):
                continue
            else:
                log_count += 1
        if log_count:
            self.wpl_log_fail('Exiting switch_mcelog_to_daemon_mode with result FAIL')
            self.wpl_raiseException("Failure while testing mcelog cmd'%s' with Option: '%s'" % (CMDName, option))
        else:
            self.wpl_log_success('switch_mcelog_to_daemon_mode for DIAG tool - %s is PASSED\n' % CMDName)


#######################################################################################################################
# Function Name: test_cpu_stress_and_check_status
# Date         : 2th July 2020
# Author       : wallace <wallq@celestica.com>
#
# Procedure Revision Details:
#   Version : 1.0  - Initial Draft  - by wallace <wallq@celestica.com>
#######################################################################################################################
    def test_cpu_stress_and_check_status(self, toolName, log_message_1, log_message_2, option=''):
        self.wpl_log_debug('Entering procedure test_cpu_stress_and_check_status with args : %s' % (str(locals())))
        cmd = 'cd ' + CPU_POWER_STRESS_TOOL_PATH
        self.wpl_getPrompt("centos", 600)
        self.wpl_transmit(cmd)

        cmd = FPGA_TOOL_PATH + toolName + ' ' + option + ' ' + ' &'
        self.wpl_log_debug("command = %s" %(cmd))
        self.wpl_execute(cmd, mode='centos', timeout=10)
        time.sleep(300)

        #have to manually kill the CPU_test script because it cannot get out by itself
        cmd = 'pkill ' + toolName
        self.wpl_execute(cmd, mode='centos', timeout=10)

#######################################################################################################################
# Function Name: test_cpu_power_stress_and_check_status
# Date         : 2th July 2020
# Author       : hemin <hemin@celestica.com>
#
# Procedure Revision Details:
#   Version : 1.0  - Initial Draft  - by hemin <hemin@celestica.com>
#######################################################################################################################
    def test_cpu_power_stress_and_check_status(self, toolName, log_message_1, log_message_2, option=''):
        self.wpl_log_debug('Entering procedure test_cpu_power_stress_and_check_status with args : %s' % (str(locals())))
        cmd = 'cd ' + CPU_POWER_STRESS_TOOL_PATH
        self.wpl_getPrompt("centos", 600)
        self.wpl_transmit(cmd)
        passcount = 0
        output = self.EXEC_diag_sys_log_tool_command(toolName, option)
        for line in output.splitlines():
            line = line.strip()
            if log_message_1 in line:
                passcount += 1
            elif log_message_2 in line:
                passcount += 1
            else:
                continue
        if passcount == 2:
            self.wpl_log_success('test_cpu_power_stress_and_check_status for DIAG tool - %s is PASSED\n' % toolName)
        else:
            self.wpl_log_fail('Exiting test_cpu_power_stress_and_check_status with result FAIL')
            self.wpl_raiseException("Failure while testing DIAG tool '%s' with Option: '%s'" % (toolName, option))

#######################################################################################################################
# Function Name: get_psu_eeprom_info
# Date         : 25th seq 2020
# Author       : Eric Zhang <zfzhang@celestica.com>
#
# Procedure Revision Details:
#   Version : 1.0  - Initial Draft  - Eric Zhang <zfzhang@celestica.com>
#######################################################################################################################
    def get_psu_eeprom_info(self, toolName, option, keywords_pattern=None, pass_pattern=None, path=BMC_DIAG_TOOL_PATH):
        self.wpl_log_debug('Entering procedure get_psu_eeprom_info with args : %s' % (str(locals())))
        if path:
            cmd = 'cd ' + path
            self.wpl_transmit(cmd)
            power_type = self.dc_power_check()
            if power_type == 'DC':
                if 'psu1' in option:
                    self.wpl_log_info('This is dc power, only support three number of psu, skip the psu1 check !!!')
                    return
            command = toolName + ' ' + option
            self.wpl_log_debug("command = %s" % (command))
            self.wpl_execute_cmd(command, mode=openbmc_mode, timeout=600)
#######################################################################################################################
# Function Name: test_ddr_stress_and_check_status
# Date         : 6th July 2020
# Author       : hemin <hemin@celestica.com>
#
# Procedure Revision Details:
#   Version : 1.0  - Initial Draft  - by hemin <hemin@celestica.com>
#######################################################################################################################
    def test_ddr_stress_and_check_status(self, inputArray, toolName, run_time, percent, log_file):
        self.wpl_log_debug('Entering procedure test_ddr_stress_and_check_status with args : %s' % (str(locals())))
        cmd = 'cd ' + CPU_POWER_STRESS_TOOL_PATH
        self.wpl_getPrompt("centos", 600)
        self.wpl_transmit(cmd)
        option = run_time + " " + percent
        output = self.EXEC_diag_sys_log_tool_command(toolName, option, log_file, CPU_POWER_STRESS_TOOL_PATH)
        cmd_str = "cat " + log_file
        logcount = 0
        log_message = self.wpl_execute(cmd_str, mode='centos', timeout=600)
        for line in log_message.splitlines():
            line = line.strip()
            if inputArray["Status"] in line:
                logcount += 1
            else:
                continue
        if logcount:
            self.wpl_log_success('test_ddr_stress_and_check_status for DIAG tool - %s is PASSED\n' % toolName)
        else:
            self.wpl_log_fail('Exiting test_ddr_stress_and_check_status with result FAIL')
            self.wpl_raiseException("Failure while testing DIAG tool '%s' with Option: '%s'" % (toolName, option))

#######################################################################################################################
# Function Name: PSU_EEPROM_dict_option_i
# Date         : 25th seq 2020
# Author       : Eric Zhang <zfzhang@celestica.com>
#
# Procedure Revision Details:
#   Version : 1.0  - Initial Draft  - Eric Zhang <zfzhang@celestica.com>
#######################################################################################################################
    def PSU_EEPROM_dict_option_i(self, toolName, option, keywords_pattern=None, pass_pattern=None, path=BMC_DIAG_TOOL_PATH):
        self.wpl_log_debug('Entering procedure PSU_EEPROM_dict_option_i with args : %s' % (str(locals())))
        cmd = 'cd ' + path

        self.wpl_transmit(cmd)
        passcount = 0
        output = self.EXEC_check_cpld_ok_command(toolName, option)
        for line in output.splitlines():
            line = line.strip()
            match = re.search(keywords_pattern,line)
            if match:
                passcount += 1
        self.wpl_log_debug('**************passcount=%s*************' % passcount)
        power_type = self.dc_power_check()
        if power_type == 'DC':
            if passcount == 2:
                self.wpl_log_success('PSU_EEPROM_dict_option_i Test - %s is PASSED\n' % toolName)
            else:
                self.wpl_log_fail('Exiting PSU_EEPROM_dict_option_i with result FAIL')
                self.wpl_raiseException("Failure while testing DIAG tool '%s' with Option: '%s'" % (toolName, option))
        else:
            if passcount == 4:
                self.wpl_log_success('PSU_EEPROM_dict_option_i Test - %s is PASSED\n' % toolName)
            else:
                self.wpl_log_fail('Exiting PSU_EEPROM_dict_option_i with result FAIL')
                self.wpl_raiseException("Failure while testing DIAG tool '%s' with Option: '%s'" % (toolName, option))

#######################################################################################################################
# Function Name: PSU_EEPROM_dict_option_s
# Date         : 25th seq 2020
# Author       : Eric Zhang <zfzhang@celestica.com>
#
# Procedure Revision Details:
#   Version : 1.0  - Initial Draft  - Eric Zhang <zfzhang@celestica.com>
#######################################################################################################################
    def PSU_EEPROM_dict_option_s(self, toolName, option, keywords_pattern=None, pass_pattern=None, path = BMC_DIAG_TOOL_PATH):
        self.wpl_log_debug('Entering procedure PSU_EEPROM_dict_option_s with args : %s' % (str(locals())))
        cmd = 'cd ' + path

        self.wpl_transmit(cmd)
        passcount = 0
        message = 'OK'
        output = self.EXEC_check_cpld_ok_command(toolName, option)
        for line in output.splitlines():
            line = line.strip()
            if message in line:
                passcount += 1
        self.wpl_log_debug('**************passcount=%s*************' % passcount)
        power_type = self.dc_power_check()
        if power_type == 'DC':
            if passcount == 6:
                self.wpl_log_success('PSU_EEPROM_dict_option_s Test - %s is PASSED\n' % toolName)
            else:
                self.wpl_log_fail('Exiting PSU_EEPROM_dict_option_s with result FAIL')
                self.wpl_raiseException("Failure while testing DIAG tool '%s' with Option: '%s'" % (toolName, option))
        else:
            if passcount == 12:
                self.wpl_log_success('PSU_EEPROM_dict_option_s Test - %s is PASSED\n' % toolName)
            else:
                self.wpl_log_fail('Exiting PSU_EEPROM_dict_option_s with result FAIL')
                self.wpl_raiseException("Failure while testing DIAG tool '%s' with Option: '%s'" % (toolName, option))

#######################################################################################################################
# Function Name: test_ssd_stress_and_check_status
# Date         : 8th July 2020
# Author       : hemin <hemin@celestica.com>
#
# Procedure Revision Details:
#   Version : 1.0  - Initial Draft  - by hemin <hemin@celestica.com>
#######################################################################################################################
    def test_ssd_stress_and_check_status(self, toolName, run_time, log_file):
        self.wpl_log_debug('Entering procedure test_ssd_stress_and_check_status with args : %s' % (str(locals())))
        cmd = 'cd ' + CPU_POWER_STRESS_TOOL_PATH
        self.wpl_getPrompt("centos", 600)
        self.wpl_transmit(cmd)
        errorcount = 0
        passcount = 0
        cmd_str = './' + toolName + ' ' + run_time + ' ' + log_file
        output = self.wpl_execute(cmd_str, mode='centos', timeout=600)
        for line in output.splitlines():
            line = line.strip()
            line = line.strip("\n")
            r = re.search("error|fail", line, re.I)
            if not r:
                continue
            else:
                errorcount += 1
        if errorcount:
            self.wpl_log_fail('Exiting test_ssd_stress_and_check_status with result FAIL')
            self.wpl_raiseException("Failure while testing DIAG tool '%s' with Option: '%s'" % (toolName, run_time))
        else:
            cmd_str = 'ls ' + log_file
            log_path = self.wpl_execute(cmd_str, mode='centos', timeout=600)
            for line in log_path.splitlines():
                line = line.strip()
                if line.endswith(log_file):
                    passcount += 1
                else:
                    continue
        if passcount:
            self.wpl_log_success('test_ssd_stress_and_check_status for DIAG tool - %s is PASSED\n' % toolName)
        else:
            self.wpl_log_fail('Exiting test_ssd_stress_and_check_status with result FAIL')
            self.wpl_raiseException("Failure while testing DIAG tool '%s' with Option: '%s'" % (toolName, run_time))

    #######################################################################################################################
    # Function Name: verify_cpld_check_ok_dict
    # Date         : 26th Aug 2020
    # Author       : Eric Zhang <zfzhang@celestica.com>
    #
    # Procedure Revision Details:
    #   Version : 1.0  - Initial Draft  - Eric Zhang <zfzhang@celestica.com>
    #######################################################################################################################
    def verify_cpld_check_ok_dict(self, toolName, option, keywords_pattern=None, pass_pattern=None):
        self.wpl_log_debug('Entering procedure verify_cpld_check_ok_dict with args : %s' % (str(locals())))
        cmd = 'cd ' + BMC_DIAG_TOOL_PATH

        self.wpl_transmit(cmd)
        passcount = 0
        message = 'OK'
        output = self.EXEC_check_cpld_ok_command(toolName, option)
        for line in output.splitlines():
            line = line.strip()
            if message in line:
                passcount += 1
        self.wpl_log_debug('**************passcount=%s*************' % passcount)
        if passcount == 6:
            self.wpl_log_success('verify_cpld_check_ok_dict for DIAG tool - %s is PASSED\n' % toolName)
        else:
            self.wpl_log_fail('Exiting verify_cpld_check_ok_dict with result FAIL')
            self.wpl_raiseException("Failure while testing DIAG tool '%s' with Option: '%s'" % (toolName, option))

    #######################################################################################################################
    # Function Name: EXEC_check_cpld_ok_command
    # Date         : 26th Aug 2020
    # Author       : Eric Zhang <zfzhang@celestica.com>
    #
    # Procedure Revision Details:
    #   Version : 1.0  - Initial Draft  - Eric Zhang <zfzhang@celestica.com>
    #######################################################################################################################
    def EXEC_check_cpld_ok_command(self, toolName, option, path=BMC_DIAG_TOOL_PATH):

        cmd = ('cd ' + path)
        self.wpl_log_debug("command = %s" % (cmd))
        self.wpl_getPrompt("openbmc", 600)
        self.wpl_transmit(cmd)

        cmd = './'+ toolName + ' ' + option

        self.wpl_log_debug("command = %s" % (cmd))
        return self.wpl_execute_cmd(cmd, mode='openbmc', timeout=600)

#######################################################################################################################
# Function Name: test_lpmode_stress_and_check_status
# Date         : 9th July 2020
# Author       : hemin <hemin@celestica.com>
#
# Procedure Revision Details:
#   Version : 1.0  - Initial Draft  - by hemin <hemin@celestica.com>
#######################################################################################################################
    def test_lpmode_stress_and_check_status(self, toolName, option, run_time):
        self.wpl_log_debug('Entering procedure test_lpmode_stress_and_check_status with args : %s' % (str(locals())))
        cmd = 'cd ' + LPMODE_STRESS_TOOL_PATH
        self.wpl_getPrompt("centos", 600)
        self.wpl_transmit(cmd)
        cmd_str = './' + toolName + ' ' + option + ' ' + run_time
        passcount = 0
        output = self.wpl_execute(cmd_str, mode='centos', timeout=600)
        for line in output.splitlines():
            line = line.strip()
            if "PASS" in line:
                passcount += 1
            else:
                continue
        if passcount:
            self.wpl_log_success('test_lpmode_stress_and_check_status for DIAG tool - %s is PASSED\n' % toolName)
        else:
            self.wpl_log_fail('Exiting test_lpmode_stress_and_check_status with result FAIL')
            self.wpl_raiseException("Failure while testing DIAG tool '%s' with Option: '%s'" % (toolName, option))


#######################################################################################################################
# Function Name: test_pcie_stress_and_check_status
# Date         : 13th July 2020
# Author       : hemin <hemin@celestica.com>
#
# Procedure Revision Details:
#   Version : 1.0  - Initial Draft  - by hemin <hemin@celestica.com>
#######################################################################################################################
    def test_pcie_stress_and_check_status(self, toolName, run_time, log_message):
        self.wpl_log_debug('Entering procedure test_pcie_stress_and_check_status with args : %s' % (str(locals())))
        cmd = 'cd ' + PCIE_STRESS_TOOL_PATH
        self.wpl_getPrompt("centos", 600)
        self.wpl_transmit(cmd)
        passcount = 0
        cmd_str = './' + toolName + ' ' + run_time
        output = self.wpl_execute(cmd_str, mode='centos', timeout=600)
        for line in output.splitlines():
            line = line.strip()
            if log_message in line:
                passcount += 1
            else:
                continue
        if passcount:
            self.wpl_log_success('test_pcie_stress_and_check_status for DIAG tool - %s is PASSED\n' % toolName)
        else:
            self.wpl_log_fail('Exiting test_pcie_stress_and_check_status with result FAIL')
            self.wpl_raiseException("Failure while testing DIAG tool '%s' with Option: '%s'" % (toolName, run_time))


#######################################################################################################################
# Function Name: view_and_check_the_mce_log
# Date         : 14th Aug 2020
# Author       : hemin <hemin@celestica.com>
#
# Procedure Revision Details:
#   Version : 1.0  - Initial Draft  - by hemin <hemin@celestica.com>
#######################################################################################################################
    def verify_sys_log(self, toolName, option, sys_log_path):
        self.wpl_log_debug('Entering procedure verify_sys_log with args : %s' % (str(locals())))
        cmd = 'cd ' + FPGA_TOOL_PATH + 'stress/syslog'
        self.wpl_getPrompt("centos", 600)
        self.wpl_transmit(cmd)
        cmd_str = './' + toolName + ' ' + option + ' logname'
        passCount = 0
        output = self.wpl_execute(cmd_str, mode='centos', timeout=600)
        for line in output.splitlines():
            line = line.strip()
            if "PASS" in line:
                passCount += 1
        if passCount == 2:
            self.wpl_log_success('verify_sys_log for DIAG tool - %s is PASSED\n' % toolName)
        else:
            self.wpl_log_fail('Exiting verify_sys_log with result FAIL')
            self.wpl_raiseException("Failure while testing DIAG tool '%s' with Option: '%s'" % (toolName, option))


#######################################################################################################################
# Function Name: view_and_check_the_mce_log
# Date         : 3th July 2020
# Author       : hemin <hemin@celestica.com>
#
# Procedure Revision Details:
#   Version : 1.0  - Initial Draft  - by hemin <hemin@celestica.com>
#######################################################################################################################
    def view_and_check_the_mce_log(self, cmd):
        self.wpl_log_debug('Entering procedure view_and_check_the_mce_log with args : %s' % (str(locals())))
        self.wpl_log_debug("command = %s" % (cmd))
        self.wpl_getPrompt("centos", 600)
        errorcount = 0
        output = self.wpl_execute(cmd, mode='centos', timeout=600)
        for line in output.splitlines():
            line = line.strip()
            line = line.strip("\n")
            self.wpl_log_debug(line)
            r = re.search("error", line, re.I)
            if not r :
                continue
            elif cmd not in line:
                errorcount += 1
        if errorcount:
            self.wpl_log_fail('Exiting view_and_check_the_mce_log with result FAIL number:{}'.format(errorcount))
            self.wpl_raiseException("Failure while testing check mcelog cmd'%s'" % (cmd))
        else:
            self.wpl_log_success('view_and_check_the_mce_log for DIAG tool - %s is PASSED\n' % cmd)


#######################################################################################################################
# Function Name: verify_option_diag_system_log_tool_simple_dict
# Date         : March 12th 2021
# Author       : Zhenfei <zfzhang@celestica.com>
#
# Procedure Revision Details:
#   Version : 1.0  - Initial Draft  - by Zhenfei <zfzhang@celestica.com>
#######################################################################################################################
    @logThis
    def verify_option_diag_system_log_tool_simple_dict(self, toolName, option, pattern, path):
        if path:
            self.wpl_transmit('cd '+path)

        passcount = 0
        command = toolName + ' ' + option
        output = self.wpl_execute(command, mode = 'centos', timeout=600)
        pattern = [
            '-h', '-l','-k','-c','-r','-s'
        ]
        for line in output.splitlines():
            line = line.strip()
            for i in range(0,len(pattern)):
                match = re.search(pattern[i], line, re.I)
                if match:
                    passcount += 1
        self.wpl_log_info("/////passcount = %s ///////" % passcount)
        # remove the before log
        command = 'rm -rf log'
        self.wpl_transmit(command)
        # output changed
        if passcount == 26:
            self.wpl_log_success('verify_option_diag_system_log_tool_simple_dict for DIAG tool - %s is PASSED\n' % toolName)
        else:
            self.wpl_log_fail('Exiting verify_option_diag_system_log_tool_simple_dict with result FAIL')
            self.wpl_raiseException("Failure while testing DIAG tool '%s' with Option: '%s'" % (toolName, option))

    @logThis
    def verify_run_system_load_stress_test(self, toolName, option, pattern, path, param):
        if param == 'True':
            CommonLib.switch_to_openbmc()
            path = '/mnt/data1/BMC_Diag/utility/stress/'
            self.wpl_transmit('cd '+path)

            command = toolName + ' ' + option
            output = self.wpl_execute(command, mode=openbmc_mode, timeout=600)
        else:
            self.wpl_transmit('cd ' + path)

            command = toolName + ' ' + option
            output = self.wpl_execute(command, mode="centos", timeout=600)
        if option == ' -l log/PCIE_sys_after -k -c':
            pattern  = [
                r'Save System Logs.*?PASS',
                r'Clean System Logs.*?PASS',
                r'Show SEL info.*?PASS',
                r'Log check'
            ]
        pattern = ['fail', 'error', 'no such file']
        fail_count = 0
        for line in output.splitlines():
            line = line.strip()
            for i in range(0,len(pattern)):
                match = re.search(pattern[i], line, re.I)
                if match:
                    fail_count += 1
        if fail_count:
            self.wpl_log_fail('Exiting verify_run_system_load_stress_test with result FAIL')
            self.wpl_raiseException("Failure while testing DIAG tool '%s' with Option: '%s'" % (toolName, option))
        else:
            self.wpl_log_success('verify_run_system_load_stress_test for DIAG tool - %s is PASSED\n' % toolName)

#######################################################################################################################
# Function Name: verify_diag_system_log_simple_dict
# Date         : June 29th 2020
# Author       : hemin <hemin@celestica.com>
#
# Procedure Revision Details:
#   Version : 1.0  - Initial Draft  - by hemin <hemin@celestica.com>
#######################################################################################################################
    def verify_diag_system_log_simple_dict(self, toolName, option, fileName):
        self.wpl_log_debug('Entering procedure verify_diag_system_log_simple_dict with args : %s' % (str(locals())))
        cmd = 'cd ' + FPGA_TOOL_PATH + 'stress/syslog'
        self.wpl_getPrompt("centos", 600)
        self.wpl_transmit(cmd)
        p_pass = '\s+\| PASS \|'
        pass_count = 0
        output = self.EXEC_diag_sys_log_tool_command(toolName, option, fileName)
        self.wpl_log_debug("\r\noutput=[\r\n%s\r\n]" % output)
        for line in output.splitlines():
            line = line.strip()
            match = re.search(p_pass, line)
            if match:
                pass_count += 1
        if pass_count:
            self.wpl_log_success('verify_diag_system_log_simple_dict for DIAG tool - %s is PASSED\n' % toolName)
        else:
            self.wpl_log_fail('Exiting verify_diag_system_log_simple_dict with result FAIL')
            self.wpl_raiseException("Failure while testing DIAG tool '%s' with Option: '%s'" % (toolName, option))


#######################################################################################################################
# Function Name: verify_option_diag_system_log_simple_dict
# Date         : June 30th 2020
# Author       : hemin <hemin@celestica.com>
#
# Procedure Revision Details:
#   Version : 1.0  - Initial Draft  - by hemin <hemin@celestica.com>
#######################################################################################################################
    def verify_option_diag_system_log_simple_dict(self, toolName, option):
        self.wpl_log_debug('Entering procedure verify_option_diag_system_log_simple_dict with args : %s' % (str(locals())))
        cmd = 'cd ' + FPGA_TOOL_PATH + 'stress/syslog'
        self.wpl_getPrompt("centos", 600)
        self.wpl_transmit(cmd)
        p_pass = '\s+\| PASS \|'
        pass_count = 0
        output = self.EXEC_diag_sys_log_tool_command(toolName, option)
        self.wpl_log_debug("\r\noutput=[\r\n%s\r\n]" % output)
        for line in output.splitlines():
            line = line.strip()
            match = re.search(p_pass, line)
            if match:
                pass_count += 1
        if pass_count:
            self.wpl_log_success('verify_option_diag_system_log_simple_dict for DIAG tool - %s is PASSED\n' % toolName)
        else:
            self.wpl_log_fail('Exiting verify_option_diag_system_log_simple_dict with result FAIL')
            self.wpl_raiseException("Failure while testing DIAG tool '%s' with Option: '%s'" % (toolName, option))


#######################################################################################################################
# Function Name: verify_option_diag_tool_simple_dict
# Date         : January 27th 2020
# Author       : Phawit P. <Phaphan@celestica.com>
#
# Procedure Revision Details:
#   Version : 1.0  - Initial Draft  - by Phawit P. <Phaphan@celestica.com>
#######################################################################################################################
    def verify_option_diag_tool_simple_dict(self, inputArray, toolName, option, path=DIAG_TOOL_PATH):
        self.wpl_log_debug('Entering procedure verify_option_diag_tool_simple_dict with args : %s' %(str(locals())))
        cmd = 'cd ' + path
        self.wpl_getPrompt("centos", 600)
        self.wpl_transmit(cmd)
        errCount = 0
        output = self.EXEC_diag_tool_command(toolName, option, path)
        if (option == '-h' or option == '--help'):
            parsedOutput = parserDIAGLibs.PARSE_diagtool_help(output)
        elif (option == '-i' or option == '--info'):
            parsedOutput = parserDIAGLibs.PARSE_diagtool_info(output)
        elif (option == '-S' or option == '--show'):
            parsedOutput = parserDIAGLibs.PARSE_diagtool_show(output)

            # To save and verify the Kernel, Cent OS and Diag OS versions
            match = re.search(catch_kernel_version_pattern, output)
            if match:
                self.centos_kernel_version_by_cmd = match.group('version')
            else:
                self.centos_kernel_version_by_cmd = "Not found"

            match = re.search(catch_os_diag_version_pattern, output)
            if match:
                self.os_diag_version_by_cmd = match.group('version')
            else:
                self.os_diag_version_by_cmd = "Not found"

            match = re.search(catch_centos_version_pattern, output)
            if match:
                self.centos_version_by_cmd = match.group('version')
            else:
                self.centos_version_by_cmd = "Not found"

            # To save / verify the I210 firmware version
            match = re.search(catch_i210_fw_version_pattern, output)
            if match:
                self.i210_fw_version_by_cel_version_test = match.group('version')
            else:
                self.i210_fw_version_by_cel_version_test = "Not found"

            # To save / verify the OpenBMC, CPLD, FPGA and BIOS versions
            match = re.search(catch_openbmc_version_pattern, output)
            if match:
                self.openbmc_version_by_cmd = match.group('version')
            else:
                self.openbmc_version_by_cmd = "Not found"

            match = re.search(catch_scm_version_pattern, output)
            if match:
                self.cpld_scm_version_by_cmd = match.group('version')
            else:
                self.cpld_scm_version_by_cmd = "Not found"

            match = re.search(catch_smb_version_pattern, output)
            if match:
                self.cpld_smb_version_by_cmd = match.group('version')
            else:
                self.cpld_smb_version_by_cmd = "Not found"

            match = re.search(catch_fpga1_version_pattern, output)
            if match:
                self.fpga1_version_by_cmd = match.group('version')
            else:
                self.fpga1_version_by_cmd = "Not found"

            match = re.search(catch_fpga2_version_pattern, output)
            if match:
                self.fpga2_version_by_cmd = match.group('version')
            else:
                self.fpga2_version_by_cmd = "Not found"

            match = re.search(catch_bios_version_pattern, output)
            if match:
                self.bios_version_by_cmd = match.group('version')
            else:
                self.bios_version_by_cmd = "Not found"

        elif (option == '-l' or option == '--list'):
            parsedOutput = parserDIAGLibs.PARSE_diagtool_list(output)
        errCount += CommonLib.compare_input_dict_to_parsed(parsedOutput, inputArray)
        if errCount:
            self.wpl_log_fail('Exiting verify_option_diag_tool_simple_dict with result FAIL')
            self.wpl_raiseException("Failure while testing DIAG tool '%s' with Option: '%s'" %(toolName, option))
        else:
            self.wpl_log_success('Option: %s test result for DIAG tool - %s is PASSED\n' %(option, toolName))

#######################################################################################################################
    # Function Name: minipack2_fpga_ver_test
    # Date         : 27th Oct 2020
    # Author       : Eric Zhang <zfzhang@celestica.com>
    #
    # Procedure Revision Details:
    #   Version : 1.0  - Initial Draft  - by Eric Zhang <zfzhang@celestica.com>
#######################################################################################################################
    def minipack2_fpga_ver_test(self, toolName, option, keywords=None, pattern=None, path=None):
        self.wpl_log_debug('Entering procedure minipack2_fpga_ver_test : %s\n' % (str(locals())))
        if path:
          cmd = ('cd ' + path)
          self.wpl_log_debug("command = %s" %(cmd))
          self.wpl_getPrompt("centos", 600)
          self.wpl_transmit(cmd)

        passCount = 0
        cmd = './' + toolName + option
        output = self.wpl_execute(cmd, mode='centos', timeout=600)
        self.wpl_log_debug('*****************output=%s***********' % output)
        for line in output.splitlines():
            line = line.strip()
            for p_pass in keywords:
                match = re.search(p_pass, line)
                if match:
                    passCount += 1

        if passCount == len(keywords):
            self.wpl_log_success('minipack2_fpga_ver_test for DIAG tool - %s is PASSED\n' % cmd)
        else:
            self.wpl_log_fail('Exiting minipack2_fpga_ver_test with result FAIL')
            self.wpl_raiseException("Failure while testing minipack2_fpga_ver_test cmd'%s' with Option: '%s'" % (toolName, option))

    def verify_minipack2_sw_test(self, toolName, option, pattern, path,):
        self.wpl_log_debug('Entering procedure verify_minipack2_sw_test with args : %s' % (str(locals())))

        cmd = 'cd ' + path
        self.wpl_getPrompt("centos", 600)
        self.wpl_transmit(cmd)
        passCount = 0
        bmc_pass = 0
        bmc_match = 0
        bmc_match2 = 0
        output = self.EXEC_diag_tool_command(toolName, option, path)
        is_autobuild = str(SwImage.getSwImage(SwImage.BMC).newVersion)
        self.wpl_log_debug("////////////////////is_autobuild///%s///////" % is_autobuild)
        for line in output.splitlines():
            line = line.strip()
            for p_pass in pattern:
                if 'BMC Version' in line:
                    bmc_match = re.search('1.03', line)
                    bmc_match2 = re.search(is_autobuild, line)
                match = re.search(p_pass, line)
                if match:
                    passCount += 1 
                if bmc_match or bmc_match2:
                    bmc_pass += 1
        self.wpl_log_debug('///////bmc_pass=%s//////////' % bmc_pass)
        if passCount == len(pattern) and bmc_pass:
            self.wpl_log_success('verify_minipack2_sw_test for DIAG tool - PASSED\n')
        else:
            self.wpl_log_fail('Exiting verify_minipack2_sw_test with result FAIL')
            self.wpl_raiseException("Failure while testing verify_minipack2_sw_test cmd'%s' with Option: '%s'" % (toolName, option))


#######################################################################################################################
# Function Name: verify_fpga_sLPC
# Date         : 4th Nov 2020
# Author       : Eric Zhang <zfzhang@celestica.com>
#
# Procedure Revision Details:
#   Version : 1.0  - Initial Draft  - by Eric Zhang <zfzhang@celestica.com>
#######################################################################################################################
    def verify_fpga_sLPC(self, toolName, option, pattern='none', path=BMC_DIAG_TOOL_PATH):
        self.wpl_log_debug('Entering procedure verify_fpga_sLPC with args : %s' % (str(locals())))
        if path:
            cmd = 'cd ' + path
            self.wpl_transmit(cmd)

        command = toolName + ' ' + option

        failCount = 0
        self.wpl_log_debug('*********command=%s*************' % command)
        output = self.wpl_execute(command, mode='centos', timeout=60)
        #if 'USB disconnect' in output:
         #   self.wpl_raiseException("Failed verify_fpga_sLPC with error USB disconnect!")
        for line in output.splitlines():
            line = line.strip()
            match1 = re.search(pattern[0], line)
            match2 = re.search(pattern[1], line)

            if match1 or match2:
                failCount += 1
                break
        if failCount:
            self.wpl_raiseException("Failed verify_fpga_sLPC")
        else:
            self.wpl_log_success("Successfully verify_fpga_sLPC")

#######################################################################################################################
# Function Name: verify_each_pcie_lspci
# Date         : Aug 27th 2020
# Author       : Eric Zhang <zfzhang@celestica.com>
#
# Procedure Revision Details:
#   Version : 1.0  - Initial Draft  - by Eric Zhang <zfzhang@celestica.com>
#######################################################################################################################
    def verify_each_pcie_lspci(self, toolName, option, keywords='none', pattern='none',path=DIAG_TOOL_PATH):
        self.wpl_log_debug('Entering procedure verify_each_pcie_lspci with args : %s' % (str(locals())))
        cmd = 'cd ' + path
        self.wpl_getPrompt("centos", 600)
        self.wpl_transmit(cmd)
        passCount = 0

        self.wpl_log_debug('option = %s' % option)

        TH4 = "lspci | grep '06:00.0' | grep -v grep | wc -l"
        output_value = self.EXEC_diag_tool_command(TH4, " ", " ")
        self.wpl_log_debug('***********output_value = %s************* ' % output_value)
        if "0" in output_value.splitlines() and option == "06:00.0 -xxxvvv":
            self.wpl_log_info('no check it because of 06:00.0 no TH4! Skip it !')
            return
        else:
            output = self.EXEC_diag_tool_command(toolName, option, path)
            self.wpl_log_debug("output=%s" % output)
            for line in output.splitlines():
                line = line.strip()
                for p_pass in keywords:
                    match = re.search(p_pass,  line)
                    if match:
                        passCount += 1
            self.wpl_log_debug('***********passCount = %d **************' % passCount)
            if passCount == len(keywords):
                self.wpl_log_success('verify_each_pcie_lspci test result for DIAG tool - %s is PASSED\n' % toolName)
            else:
                self.wpl_log_fail('Exiting verify_each_pcie_lspci with result FAIL')
                self.wpl_raiseException("Failure while testing DIAG tool '%s' with Option: '%s'" % (toolName, option))

#######################################################################################################################
# Function Name: sensors_test_option_s
# Date         : 15th Oct 2020
# Author       : Eric Zhang <zfzhang@celestica.com>
#
# Procedure Revision Details:
#   Version : 1.0  - Initial Draft  - by Eric Zhang <zfzhang@celestica.com>
#######################################################################################################################
    def sensors_test_option_s(self, toolName, option, keywords='none', pattern='none', path=BMC_DIAG_TOOL_PATH):
        self.wpl_log_debug('Entering procedure sensors_test_option_s with args : %s' % (str(locals())))
        if path:
            cmd = 'cd ' + path
            self.wpl_transmit(cmd)
        if option == ' ':
            command = option
        else:
            command = './' + toolName + ' ' + option

        failCount = 0
        output = self.wpl_execute_cmd(command, mode='openbmc', timeout=60)
        for line in output.splitlines():
            line = line.strip()
            match1 = re.search(keywords[0], line)
            match2 = re.search(keywords[1], line)

            if match1 or match2:
                failCount += 1
                break
        if failCount:
            self.wpl_raiseException("Failed sensors_test_option_s")
        else:
            self.wpl_log_success("Successfully sensors_test_option_s")

#######################################################################################################################
# Function Name: verify_cloudripper_cel_psu_option_s
# Date         : 26th Oct 2020
# Author       : Eric Zhang <zfzhang@celestica.com>
#
# Procedure Revision Details:
#   Version : 1.0  - Initial Draft  - Eric Zhang <zfzhang@celestica.com>
#######################################################################################################################
    def verify_cloudripper_cel_psu_option_s(self, toolName, option, keywords_pattern=None, pass_pattern=None, path=BMC_DIAG_TOOL_PATH):
        self.wpl_log_debug('Entering procedure verify_cloudripper_cel_psu_option_s with args : %s' % (str(locals())))
        cmd = 'cd ' + path

        self.wpl_transmit(cmd)
        passcount = 0
        output = self.EXEC_check_cpld_ok_command(toolName, option)
        self.wpl_log_debug("*******************output=%s*******" % output)
        for line in output.splitlines():
            line = line.strip()
            for p_pass in keywords_pattern:
                match = re.search(p_pass, line)
                if match:
                    passcount += 1
        self.wpl_log_debug('**************passcount=%s*************' % passcount)
        if passcount == len(keywords_pattern):
            self.wpl_log_success('verify_cloudripper_cel_psu_option_s for DIAG tool - %s is PASSED\n' % toolName)
        else:
            self.wpl_log_fail('Exiting verify_cloudripper_cel_psu_option_s with result FAIL')
            self.wpl_raiseException("Failure while testing DIAG tool '%s' with Option: '%s'" % (toolName, option))

#######################################################################################################################
# Function Name: verify_bmc_eeprom_tool
# Date         : 20th Oct 2020
# Author       : Eric Zhang <zfzhang@celestica.com>
#
# Procedure Revision Details:
#   Version : 1.0  - Initial Draft  - Eric Zhang <zfzhang@celestica.com>
#######################################################################################################################
    def verify_bmc_eeprom_tool(self, toolName, option, keywords=None, path=BMC_DIAG_TOOL_PATH):
        self.wpl_log_debug('Entering procedure verify_bmc_eeprom_tool with args : %s' % (str(locals())))
        cmd = 'cd ' + path
        self.wpl_getPrompt("centos", 600)
        self.wpl_transmit(cmd)

        list1=[]
        self.wpl_log_debug('new_option = %s' % option)
        output = self.EXEC_check_cpld_ok_command(toolName, option, path)
        self.wpl_log_debug("output=%s" % output)

        for line in output.splitlines():
            line = line.strip()
            #if 'No such file or directory' in line:
             #   self.wpl_log_fail('Exiting verify_bmc_eeprom_tool with result FAIL')
              #  self.wpl_raiseException("Failure while testing verify_bmc_eeprom_tool with error no such file or directory")
               # break
            for p_pass in keywords:
                match = re.search(p_pass, line)
                if match:
                    list1.append(p_pass)
        set1 = set(list1)
        self.wpl_log_debug('**********len(set1)=%d ********' % len(set1))
        if len(set1) == len(keywords):
            self.wpl_log_success('verify_bmc_eeprom_tool test result for DIAG tool - %s is PASSED\n' % toolName)
        else:
            self.wpl_log_fail('Exiting verify_bmc_eeprom_tool with result FAIL')
            self.wpl_raiseException("Failure while testing DIAG tool '%s' with Option: '%s'" % (toolName, option))

#######################################################################################################################
# Function Name: verify_bmc_tpm_test_a & EXEC_diag_bmc_tool_command
# Date         : Oct 13th 2020
# Author       : Eric Zhang <zfzhang@celestica.com>
#
# Procedure Revision Details:
#   Version : 1.0  - Initial Draft  - by Eric Zhang <zfzhang@celestica.com>
#######################################################################################################################
    def verify_bmc_tpm_test_a(self, toolName, option, keywords='none', pattern='none', path=BMC_DIAG_TOOL_PATH):
        self.wpl_log_debug('Entering procedure verify_bmc_tpm_test_a with args : %s' % (str(locals())))
        cmd = 'cd ' + path
        self.wpl_getPrompt("openbmc", 600)
        self.wpl_transmit(cmd)
        passCount = 0

        output = self.EXEC_diag_bmc_tool_command(toolName, option, path)
        self.wpl_log_debug("output=%s" % output)

        for line in output.splitlines():
            line = line.strip()
            for p_pass in keywords:
                match = re.search(p_pass, line)
                if match:
                    passCount += 1
        self.wpl_log_debug('***********passCount = %d **************' % passCount)
        if passCount == len(keywords):
            self.wpl_log_success('verify_bmc_tpm_test_a test result for DIAG tool - %s is PASSED\n' % toolName)
        else:
            self.wpl_log_fail('Exiting verify_bmc_tpm_test_a with result FAIL')
            self.wpl_raiseException("Failure while testing DIAG tool '%s' with Option: '%s'" % (toolName, option))

    def EXEC_diag_bmc_tool_command(self, toolName, option, path):
        self.wpl_log_debug('Entering procedure EXEC_diag_bmc_tool_command with args : %s' % (str(locals())))
        if path:
            command = 'cd ' + path
            self.wpl_transmit(command)

        cmd = './' + toolName + ' ' + option

        self.wpl_log_debug("command = %s" % (cmd))
        return self.wpl_execute_cmd(cmd, mode='openbmc', timeout=600)

#######################################################################################################################
# Function Name: verify_diag_tool_simple_dict
# Date         : January 27th 2020
# Author       : Phawit P. <Phaphan@celestica.com>
#
# Procedure Revision Details:
#   Version : 1.0  - Initial Draft  - by Phawit P. <Phaphan@celestica.com>
#######################################################################################################################
    def verify_diag_tool_simple_dict(self, toolName, option, keywords='none', pattern='none', data='none', port='none', color='none',fpath=DIAG_TOOL_PATH):
        self.wpl_log_debug('Entering procedure verify_diag_tool_simple_dict with args : %s' %(str(locals())))
        cmd = 'cd ' + fpath
        self.wpl_getPrompt("centos", 600)
        self.wpl_transmit(cmd)
        p_pass = keywords + '.*pass.*'
        self.wpl_log_debug("\r\np_pass=[%s]" %p_pass)
        passCount = 0
        new_option = option
        if data != 'none':
            new_option += " -D '"+data+"'"
        if port != 'none':
            new_option += " --port="+port
        self.wpl_log_debug('new_option = %s' % new_option)
        output = self.EXEC_diag_tool_command(toolName, new_option,fpath)
        self.wpl_log_debug("\r\noutput=[\r\n%s\r\n]" %output)

        if keywords == 'none':
            passCount = self.verify_diag_tool_other_option(output, option, pattern, data, port)
            self.wpl_log_debug('passCount = %d' % passCount)
        for line in output.splitlines():
            line = line.strip()
            match = re.search(p_pass, line, re.IGNORECASE)
            if match:
                passCount += 1
        if passCount:
            devicename = os.environ.get("deviceName", "")
            if 'wedge400c' in devicename.lower() or 'wedge400_' in devicename.lower():
                if toolName == 'cel-tpm-test' and ((option == '-a') or (option == '-all')):
                    if passCount == 4:
                        self.wpl_log_success('verify_diag_tool_simple_dict test result for DIAG tool - %s is PASSED\n' % toolName)
                    else:
                        self.wpl_log_fail('Exiting verify_diag_tool_simple_dict with result FAIL')
                        self.wpl_raiseException("Failure while testing DIAG tool '%s' with Option: '%s'" % (toolName, option))
            else:
                self.wpl_log_success('verify_diag_tool_simple_dict test result for DIAG tool - %s is PASSED\n' %toolName)
        else:
            self.wpl_log_fail('Exiting verify_diag_tool_simple_dict with result FAIL')
            self.wpl_raiseException("Failure while testing DIAG tool '%s' with Option: '%s'" %(toolName,option))


#######################################################################################################################
# Function Name: check_fpga_version
# Date         : August 12th 2020
# Author       : hemin <hemin@celestica.com>
#
# Procedure Revision Details:
#   Version : 1.0  - Initial Draft  - by hemin <hemin@celestica.com>
#######################################################################################################################
    def check_fpga_version(self, toolName, option, path, pass_pattern):
        self.wpl_log_debug('Entering procedure check_fpga_version with args : %s' % (str(locals())))
        output = self.EXEC_diag_tool_command(toolName, option, path)
        passCount = 0
        for line in output.splitlines():
            line = line.strip()
            if pass_pattern in line:
                passCount += 1
        if passCount:
            self.wpl_log_success('check_fpga_version test result for DIAG tool - %s is PASSED\n' % toolName)
        else:
            self.wpl_log_fail('Exiting check_fpga_version with result FAIL')
            self.wpl_raiseException("Failure while testing DIAG tool '%s':'" % toolName)


#######################################################################################################################
# Function Name: verify_tpm_tool_simple_dict
# Date         : August 10th 2020
# Author       : hemin <hemin@celestica.com>
#
# Procedure Revision Details:
#   Version : 1.0  - Initial Draft  - by hemin <hemin@celestica.com>
#######################################################################################################################
    def verify_tpm_tool_simple_dict(self, toolName, option, pass_pattern):
        self.wpl_log_debug('Entering procedure verify_tpm_tool_simple_dict with args : %s' % (str(locals())))
        cmd_line = 'cd ' + DIAG_TOOL_PATH
        self.wpl_getPrompt("centos", 600)
        self.wpl_transmit(cmd_line)
        cmd = './' + toolName + ' ' + option
        passCount = 0
        match_list = []
        output = self.wpl_execute(cmd, mode='centos', timeout=600)
        for line in output.splitlines():
            line = line.strip()
            for p_pass in pass_pattern:
                match = re.search(p_pass, line)
                if match:
                    match_list.append(match.group())
                    passCount += 1
        if passCount == len(pass_pattern):
            self.wpl_log_success('verify_tpm_tool_simple_dict test result for DIAG tool - %s is PASSED\n' % cmd)
        else:
            self.wpl_log_fail('Exiting verify_tpm_tool_simple_dict with result FAIL')
            self.wpl_raiseException("Failure while testing DIAG tool '%s':'" % cmd)


#######################################################################################################################
# Function Name: get_and_compare_mac_addrs
# Date         : August 10th 2020
# Author       : hemin <hemin@celestica.com>
#
# Procedure Revision Details:
#   Version : 1.0  - Initial Draft  - by hemin <hemin@celestica.com>
#######################################################################################################################
    def get_and_compare_mac_addrs(self, toolName, option, pass_pattern):
        self.wpl_log_debug('Entering procedure get_and_compare_mac_addrs with args : %s' % (str(locals())))
        cmd ='./' + toolName + ' ' + option
        ethname = ''
        mac_addr = ''
        output1 = self.wpl_execute(cmd, mode='centos', timeout=600)
        for line in output1.splitlines():
            line = line.strip()
            for p_pass in pass_pattern:
                match = re.search(p_pass, line)
                if match and p_pass == pass_pattern[0]:
                    ethname = match.group()
                elif match and p_pass == pass_pattern[1]:
                    mac_addr = match.group()
        #cmd_str = 'cat /sys/class/net/' + ethname + '/address'
        cmd_str = 'cat /sys/class/net/eth0/address'
        passCount = 0
        output2 = self.wpl_execute(cmd_str, mode='centos', timeout=600)
        for line in output2.splitlines():
            line = line.strip()
            match = re.search(mac_addr, line)
            if match:
                passCount += 1
        if passCount:
            self.wpl_log_success('get_and_compare_mac_addrs test result for DIAG tool - %s is PASSED\n' % cmd_str)
        else:
            self.wpl_log_fail('Exiting get_and_compare_mac_addrs with result FAIL')
            self.wpl_raiseException("Failure while testing DIAG tool '%s':'" % cmd_str)


#######################################################################################################################
# Function Name: verify_cpu_cmd_info
# Date         : July 24th 2020
# Author       : hemin <hemin@celestica.com>
#
# Procedure Revision Details:
#   Version : 1.0  - Initial Draft  - by hemin <hemin@celestica.com>
#######################################################################################################################
    def verify_cpu_cmd_info(self, cmd, param):
        self.wpl_log_debug('Entering procedure verify_cpu_cmd_info with args : %s' % (str(locals())))
        self.wpl_getPrompt("centos", 600)
        if param == 'True':
            p_pass = "CPU\(s\)\:\s*8"
        elif param == 'False':
            p_pass = "CPU\(s\)\:\s*4"
        passCount = 0
        output = self.wpl_execute(cmd, mode='centos', timeout=600)
        for line in output.splitlines():
            line = line.strip()
            match = re.search(p_pass, line)
            if match:
                passCount += 1
        if passCount:
            self.wpl_log_success('verify_cpu_cmd_info test result for DIAG tool - %s is PASSED\n' % cmd)
        else:
            self.wpl_log_fail('Exiting verify_cpu_cmd_info with result FAIL')
            self.wpl_raiseException("Failure while testing DIAG tool '%s':'" % cmd)

#######################################################################################################################
# Function Name: verify_fpga_tool_simple_dict
# Date         : July 23th 2020
# Author       : hemin <hemin@celestica.com>
#
# Procedure Revision Details:
#   Version : 1.0  - Initial Draft  - by hemin <hemin@celestica.com>
#######################################################################################################################
    def verify_fpga_tool_simple_dict(self, toolName, option):
        self.wpl_log_debug('Entering procedure verify_fpga_tool_simple_dict with args : %s' % (str(locals())))
        cmd = 'cd ' + DIAG_TOOL_PATH
        self.wpl_getPrompt("centos", 600)
        self.wpl_transmit(cmd)
        passCount = 0
        output = self.EXEC_diag_tool_command(toolName, option)
        for line in output.splitlines():
            line = line.strip()
            if "Temperature" or "VCC" in line:
                passCount += 1
            else:
                continue
        if passCount:
            self.wpl_log_success('verify_fpga_tool_simple_dict test result for DIAG tool - %s is PASSED\n' % toolName)
        else:
            self.wpl_log_fail('Exiting verify_fpga_tool_simple_dict with result FAIL')
            self.wpl_raiseException("Failure while testing DIAG tool '%s' with Option: '%s'" % (toolName, option))


######################################################################################################################
# Function Name: verify_diag_tool_parse_output_dict
# Date         : January 27th 2020
# Author       : Phawit P. <Phaphan@celestica.com>
#
# Procedure Revision Details:
#   Version : 1.0  - Initial Draft  - by Phawit P. <Phaphan@celestica.com>
######################################################################################################################
    def verify_diag_tool_parse_output_dict(self, toolName, option, keywords='none', pattern='none', data='none', port='none', color='none', path=DIAG_TOOL_PATH):
        self.wpl_log_debug('Entering procedure verify_diag_tool_parse_output_dict with args : %s' %(str(locals())))
        cmd = 'cd ' + path
        self.wpl_getPrompt("centos", 600)
        self.wpl_transmit(cmd)
        p_pass = keywords + '\s+\| PASS \|'
        self.wpl_log_debug("\r\np_pass=[%s]" %p_pass)
        passCount = 0
        new_option = option
        if data != 'none':
            new_option += " -D '"+data+"'"
        if port != 'none':
            new_option += " --port="+port
        self.wpl_log_debug('new_option = %s' % new_option)
        output = self.EXEC_diag_tool_command(toolName, new_option)
        self.wpl_log_debug("\r\noutput=[\r\n%s\r\n]" %output)

        ###---###
        # fix the issue of "ok"/"PASSED" string sometimes not appearing on the same line of the commmand output
        output1 = ''
        found = False
        result1 = None
        result2 = None
        result3 = None
        self.wpl_flush()
        for line in output.splitlines():
            line = line.strip()
            if len(line) == 0:
                # blank line
                continue
            else:
                found = False
                found1 = False
                found2 = False
                index1 = -1
                index2 = -1
                str_ok = ": ok"
                str_passed = ": PASSED"
                replace_str = str_ok
                # search for pass pattern on the same line
                if type(pattern) == list:
                    for i in pattern:
                        match = re.search(i, line)
                        if match:
                            found = True
                            match1 = re.search(str_passed, line)
                            if match1:
                                replace_str = str_passed
                            break
                else:
                    match = re.search(pattern, line)
                    if match:
                        found = True
                        match1 = re.search(str_passed, line)
                        if match1:
                            replace_str = str_passed

                if found == False:
                    if re.search(str_ok, line):
                        # if only "ok" string is shown on the line,
                        # then add it to the previous line
                        output1 += (str_ok + "\r\n")
                        continue
                    elif re.search(str_passed, line):
                        # if only "PASSED" string is shown on the line,
                        # then add it to the previous line
                        output1 += (str_passed + "\r\n")
                        continue

                # search for line with "setting" or "testing"
                index1 = line.find("setting")
                if index1 != -1:
                    found1 = True

                index2 = line.find("testing")
                if index2 != -1:
                    found2 = True

                if (found1 == True) or (found2 == True):
                    if re.search(":", line):
                        slist = line.split(':')
                        listStr1 = slist[0]
                        if found == True:
                            # replace "setting" or "testing" with "ok"
                            listStr2 = (listStr1 + str_ok + "\r\n")
                            output1 += listStr2
                        else:
                            # "ok" will be appended if it appears at the next line
                            output1 += str(listStr1)
                        continue
                    else:
                        if re.search("ok", line):
                            # if only "ok" string is shown on the line,
                            # then add it to the previous line
                            output1 += (str_ok + "\r\n")
                            continue
                else:
                    if found == True:
                        # remove trailing unwanted strings and replaced with desired string
                        slist = line.split(':')
                        listStr1 = slist[0]
                        listStr2 = (listStr1 + replace_str + "\r\n")
                        output1 += listStr2
                    else:
                        # general comments, not command results
                        output1 += (line + "\r\n")
                    continue

        output = output1
        self.wpl_log_debug("\r\nnew output=[\r\n%s\r\n]" %output)
        ###---###

        if keywords == 'none':
            passCount = self.verify_diag_tool_other_option(output, option, pattern, data, port)
            self.wpl_log_debug('passCount = %d' % passCount)
        for line in output.splitlines():
            line = line.strip()
            match = re.search(p_pass, line)
            if match:
                passCount += 1
        if passCount:
            self.wpl_log_success('verify_diag_tool_parse_output_dict test result for DIAG tool - %s is PASSED\n' %toolName)
        else:
            self.wpl_log_fail('Exiting verify_diag_tool_parse_output_dict with result FAIL')
            self.wpl_raiseException("Failure while testing DIAG tool '%s' with Option: '%s'" %(toolName,option))


#######################################################################################################################
# Function Name: verify_diag_tool_other_option
# Date         : January 27th 2020
# Author       : Phawit P. <Phaphan@celestica.com>
#
# Procedure Revision Details:
#   Version : 1.0  - Initial Draft  - by Phawit P. <Phaphan@celestica.com>
#######################################################################################################################
    def verify_diag_tool_other_option(self, output, option, pattern, data='none', port='none'):
        self.wpl_log_debug('Entering procedure verify_diag_tool_other_option with args : %s' %(str(locals())))
        chkCount=0
        expCount=1 if type(pattern) != list else len(pattern)
        newpattern = pattern
        if data != 'none':
            if type(newpattern) == list:
                for i in range(0,len(newpattern)):
                    self.wpl_log_info('i = %d' % i)
                    self.wpl_log_info('type = {}'.format(type(newpattern[i])))
                    self.wpl_log_info('newpattern[i] = %s' % newpattern[i])
                    newpattern[i] = newpattern[i].format(data)
            else:
                newpattern = newpattern.format(data)

        for line in output.splitlines():
            line = line.strip()
            self.wpl_log_debug('line=%s' % line)
            if type(newpattern) == list:
                for i in newpattern:
                    match = re.search(i, line)
                    if match:
                        chkCount += 1
            else:
                match = re.search(newpattern, line)
                if match:
                    chkCount += 1
        if (option == '-K' or option == '--check'):
            expCount=18
        if (option == 'mc info'):
            expCount=23
        if (option == '-w' or option == '--write'):
            expCount=3
        if (option == '-i' or option == '--info'):
            expCount=3
        if (option == '-r' or option == '--read'):
            if port != 'none':
                expCount=48
            else:
                expCount=1
        self.wpl_log_debug('chkCount = %d' % chkCount)
        self.wpl_log_debug('expCount = %d' % expCount)
        if chkCount >= expCount:
            return 1
        else:
            return 0


#######################################################################################################################
# Function Name: execute_cpld_get_reg_command
# Date         : January 30th 2020
# Author       : Phawit P. <Phaphan@celestica.com>
#
# Procedure Revision Details:
#   Version : 1.0  - Initial Draft  - by Phawit P. <Phaphan@celestica.com>
#######################################################################################################################
    def execute_cpld_get_reg_command(self, toolName, module, get_reg, expected_result='None', test_name='None'):
        self.wpl_log_debug('Entering procedure execute_cpld_get_reg_command : %s\n'%(str(locals())))
        if test_name == 'None':
            test_name = 'execute_cpld_get_reg_command'
        cmd = FPGA_TOOL_PATH + toolName + ' ' + module + ' r ' + get_reg
        output = self.wpl_execute(cmd)
        result = parserDIAGLibs.PARSE_get_cpld_output(output)
        self.wpl_log_debug('result = %s'%(result))
        if expected_result != 'None':
            if (result == expected_result):
                self.wpl_log_success("PASS: %s \'%s\': result: \'%s\'"%(test_name, cmd, result))
            else:
                self.wpl_log_fail("Command result Mismatch: Found \'%s\' Expected \'%s\'\n"%(result, expected_result))
                self.wpl_raiseException("Failed %s"%(test_name))
        else:
            return result


#######################################################################################################################
# Function Name: execute_cpld_set_reg_command
# Date         : January 30th 2020
# Author       : Phawit P. <Phaphan@celestica.com>
#
# Procedure Revision Details:
#   Version : 1.0  - Initial Draft  - by Phawit P. <Phaphan@celestica.com>
#######################################################################################################################
    def execute_cpld_set_reg_command(self, toolName, module, set_reg, set_value, test_name='None', toolPath=FPGA_TOOL_PATH):
        self.wpl_log_debug('Entering procedure execute_cpld_set_reg_command : %s\n'%(str(locals())))
        if test_name == 'None':
            test_name = 'execute_cpld_set_reg_command'
        cmd = toolPath + toolName + ' ' + module + ' w ' + set_reg + ' 0x' + set_value
        output = self.wpl_execute(cmd)
        time.sleep(1)
        parsedOutput = parserDIAGLibs.PARSE_get_cpld_output(output)
        self.wpl_log_debug('result = %s' % parsedOutput)
        if parsedOutput == set_value:
            self.wpl_log_success("Successfully executed [\'%s\'] in %s" %(cmd, test_name))
        else:
            self.wpl_raiseException("Failed executing [%s] in %s" %(cmd, test_name))


#######################################################################################################################
# Function Name: verify_scm_cpld
# Date         : January 30th 2020
# Author       : Phawit P. <Phaphan@celestica.com>
#
# Procedure Revision Details:
#   Version : 1.0  - Initial Draft  - by Phawit P. <Phaphan@celestica.com>
#######################################################################################################################
    def verify_scm_cpld(self, toolName, module, scm_set_reg, scm_get_reg, scm_set_value):
        self.wpl_log_debug('Entering procedure verify_scm_cpld with args : %s' %(str(locals())))
        for i in scm_get_reg:
            self.execute_cpld_get_reg_command(toolName, module, i, test_name="verify_scm_cpld")
        self.execute_cpld_set_reg_command(toolName, module, scm_set_reg, scm_set_value, test_name="verify_scm_cpld")


#######################################################################################################################
# Function Name: verify_smb_cpld
# Date         : January 30th 2020
# Author       : Phawit P. <Phaphan@celestica.com>
#
# Procedure Revision Details:
#   Version : 1.0  - Initial Draft  - by Phawit P. <Phaphan@celestica.com>
#######################################################################################################################
    def verify_smb_cpld(self, toolName, module, scm_set_reg, scm_get_reg, scm_set_value):
        self.wpl_log_debug('Entering procedure verify_smb_cpld with args : %s' %(str(locals())))
        for i in scm_get_reg:
            self.execute_cpld_get_reg_command(toolName, module, i, test_name="verify_smb_cpld")
        self.execute_cpld_set_reg_command(toolName, module, scm_set_reg, scm_set_value, test_name="verify_smb_cpld")


#######################################################################################################################
# Function Name: switch_and_check_bmc_by_diag_command
# Date         : 14th February 2020
# Author       : Phawit P. <Phaphan@celestica.com>
#
# Procedure Revision Details:
#   Version : 1.0  - Initial Draft  - by Phawit P. <Phaphan@celestica.com>
#######################################################################################################################
    def switch_and_check_bmc_by_diag_command(self, toolName, region):
        self.wpl_log_debug('Entering procedure switch_and_check_bmc_by_diag_command with args : %s' %(str(locals())))
        p1 = 'Current boot source is '+region+', no need to switch.'
        p2 = 'BMC will switch to '+region+' after 10 seconds...'
        passCount = 0
        option = '-b bmc -r ' + region
        output = self.EXEC_bmc_diag_tool_command(toolName, option)
        self.wpl_log_debug(output)
        for line in output.splitlines():
            line = line.strip()
            match = re.search(p1,line)
            if match:
                passCount += 1
            match = re.search(p2,line)
            if match:
                passCount += 1
                time.sleep(10)
                self.wpl_flush()
                self.wpl_receive('Starting kernel ...', timeout=90)
                self.wpl_getPrompt('openbmc', timeout=BOOTING_TIME)
                time.sleep(5)
                self.switch_to_openbmc_and_check_tool()
        if passCount:
            self.wpl_log_success("Successfully switch BMC to \'%s\'"% region)
        else:
            self.wpl_raiseException("Failed switch BMC to \'%s\'"% region)


#######################################################################################################################
# Function Name: flash_bmc_image
# Date         : 14th February 2020
# Author       : Phawit P. <Phaphan@celestica.com>
#
# Procedure Revision Details:
#   Version : 1.0  - Initial Draft  - by Phawit P. <Phaphan@celestica.com>
#######################################################################################################################
    def flash_bmc_image(self, toolName, img_path, bmc_image, flash_device):
        self.wpl_log_debug('Entering procedure flash_bmc_image with args : %s' %(str(locals())))
        passCount=0
        cmd = toolName + ' ' +  img_path + bmc_image + ' ' + flash_device
        self.wpl_log_debug('cammand = %s' % cmd)
        self.wpl_execute(cmd, mode="openbmc", timeout=600)
        self.wpl_getPrompt("openbmc", 60)
        output = self.wpl_execute("echo $?", mode="openbmc", timeout=30)
        self.wpl_log_debug(output)
        for line in output.splitlines():
            line = line.strip()
            match = re.search('^0$',line)
            if match:
                passCount += 1
        if passCount:
            self.wpl_log_success("Successfully used %s to flash BMC image: \'%s\'"% (toolName, bmc_image))
        else:
            self.wpl_raiseException("Failed using %s to flash BMC image: \'%s\'"% (toolName, bmc_image))


#######################################################################################################################
# Function Name: check_bmc_version
# Date         : 14th February 2020
# Author       : Phawit P. <Phaphan@celestica.com>
#
# Procedure Revision Details:
#   Version : 1.0  - Initial Draft  - by Phawit P. <Phaphan@celestica.com>
#######################################################################################################################
    def check_bmc_version(self, bmc_version, bmc_flash):
        self.wpl_log_debug('Entering procedure check_bmc_version with args : %s' %(str(locals())))
        passCount=0
        # e.g. OpenBMC Release wedge400-v2.7
        p1 = r'OpenBMC[ \t]+Release[ \t]+\w+\S+'+ bmc_version
        cmd = 'cat /etc/issue'
        output = self.wpl_execute(cmd, mode="openbmc")
        for line in output.splitlines():
            line = line.strip()
            match = re.search(p1,line)
            if match:
                passCount += 1
        if passCount:
            cmd = './cel-software-test -v'
            cmd_str = 'cd' + ' ' + BMC_DIAG_TOOL_PATH
            self.wpl_transmit(cmd_str)
            output = self.wpl_execute(cmd, mode="openbmc")
            for line in output.splitlines():
                line = line.strip()
                match = re.search(p1, line)
                if match:
                    passCount += 1
        if bmc_flash:
            cmd_str1 = './cel-boot-test -b bmc -s'
            p_pass = bmc_flash + ' Flash'
            output = self.wpl_execute(cmd_str1, mode="openbmc")
            for line in output.splitlines():
                line = line.strip()
                if p_pass in line:
                    passCount += 1
        if passCount == 3:
            self.wpl_log_success("Successfully checked BMC version: \'%s\'"% bmc_version)
        else:
            self.wpl_raiseException("ERR_01_001_02: Failed checking BMC version:{}, current:{}".format(bmc_version, output))


#######################################################################################################################
# Function Name: spi_util_exec
# Date         : 14th February 2020
# Author       : Phawit P. <Phaphan@celestica.com>
#
# Procedure Revision Details:
#   Version : 1.0  - Initial Draft  - by Phawit P. <Phaphan@celestica.com>
#######################################################################################################################
    def spi_util_exec(self, toolName, opt, spiNum, dev, check_pattern, imageFile='none', readFile='none', img_path=FW_IMG_PATH, tool_path=SPI_UTIL_PATH):
        self.wpl_log_debug('Entering procedure spi_util_exec with args : %s' %(str(locals())))
        passCount = 0
        patternNum = len(check_pattern)
        cmd = 'cd ' + img_path
        self.wpl_getPrompt("openbmc", 1800)
        self.wpl_transmit(cmd)
        cmd = tool_path + toolName + ' ' +  opt + ' ' + spiNum + ' ' + dev + ' '
        if opt == 'write':
            cmd += imageFile
        if opt == 'read':
            cmd += readFile
        self.wpl_log_debug('command = %s' % cmd)
        output = self.wpl_execute(cmd, mode='openbmc', timeout=1800)
        ###---###
        # fix the issue of "OK."/"done." string sometimes not appearing on the same line of the commmand output
        output1 = ''
        found = False
        self.wpl_flush()
        for line in output.splitlines():
            line = line.strip()
            line1 = line
            line2 = line1.rstrip()
            match = None
            match1 = None
            match3 = None
            if len(line2) == 0:
                # blank line
                continue
            else:
                found = False
                str_ok = "OK."
                str_passed = "done."
                # search for pass pattern on the same line
                if type(check_pattern) == list:
                    for i in check_pattern:
                        match = re.search(i, line)
                        if match:
                            found = True
                            output1 += (line + "\r\n")
                            break
                        else:
                            match1 = re.match((re.escape('.') + re.escape('.') + re.escape('.')), line2)
                            if match1:
                                # split at "..."
                                slist = i.split('.')
                                slistStr1 = str(slist[0])
                                olist = line2.split('.')
                                olistStr1 = str(olist[0])
                                match2 = re.match(olistStr1, slistStr1)
                                if match2:
                                    self.wpl_log_debug("\r\nFound %s..." %olistStr1)
                                    found = True
                                    output1 += olistStr1
                                    break

                    if found:
                        continue
                else:
                    match = re.search(check_pattern, line)
                    if match:
                        found = True
                        output1 += (line + "\r\n")
                        continue
                    else:
                        match1 = re.match((re.escape('.') + re.escape('.') + re.escape('.')), line2)
                        if match1:
                            # split at "..."
                            slist = i.split('.')
                            slistStr1 = str(slist[0])
                            olist = line2.split('.')
                            olistStr1 = str(olist[0])
                            match2 = re.fullmatch(olistStr1, slistStr1)
                            if match2:
                                self.wpl_log_debug("\r\nFound %s..." %olistStr1)
                                found = True
                                output1 += olistStr1
                                continue

                if found == False:
                    if re.match(str_ok, line2):
                        # if "OK." string is shown on the line,
                        # then add it to the previous line
                        output1 += (str_ok + "\r\n")
                        continue
                    elif re.match(str_passed, line2):
                        # if "done." string is shown on the line,
                        # then add it to the previous line
                        output1 += (str_passed + "\r\n")
                        continue
                    else:
                        output1 += (line + "\r\n")
        output = output1
        self.wpl_log_debug("\r\nnew output=[\r\n%s\r\n]" %output)
        ###---###

        for line in output.splitlines():
            line = line.strip()
            for i in range(0, patternNum):
                match = re.search(check_pattern[i], line)
                if match:
                    passCount += 1
        if passCount == patternNum:
            self.wpl_log_success("Successfully %s %s \'%s\'"% (toolName, dev, opt))
        else:
            self.wpl_raiseException("Failed %s %s \'%s\'"% (toolName, dev, opt))


#######################################################################################################################
# Function Name: switch_and_check_bios_by_diag_command
# Date         : 14th February 2020
# Author       : Phawit P. <Phaphan@celestica.com>
#
# Procedure Revision Details:
#   Version : 1.0  - Initial Draft  - by Phawit P. <Phaphan@celestica.com>
#######################################################################################################################
    def switch_and_check_bios_by_diag_command(self, toolName, region, checkTool, toolOption):
        self.wpl_log_debug('Entering procedure switch_and_check_bios_by_diag_command with args : %s' %(str(locals())))
        p0 = 'Current boot source is '+region+', no need to switch.'
        p1 = 'Power on microserver ... Done'
        p2 = 'Bridge-IC is initialized SCL to 1Mhz.'
        passCount = 0
        cmd = 'cd ' + BMC_DIAG_TOOL_PATH
        self.wpl_getPrompt("openbmc", 600)
        self.wpl_transmit(cmd)
        option = '-b bios -r ' + region
        output = self.EXEC_bmc_diag_tool_command(toolName, option)
        self.wpl_log_debug('output = %s' % output)
        for line in output.splitlines():
            line = line.strip()
            match = re.search(p0,line)
            if match:
                passCount = 1
                break
            match = re.search(p1,line)
            if match:
                passCount += 1
            match = re.search(p2,line)
            if match:
                passCount += 1
            if passCount:
                self.wpl_transmit(" ")
                self.wpl_receive("root@bmc-oob:")
        if passCount != 1:
            self.wpl_raiseException("Failed switch BIOS to \'%s\'"% region)
        passCount = self.check_bios_region(region, checkTool, toolOption)
        if passCount:
            self.wpl_log_success("Successfully switch BIOS to \'%s\'"% region)
        else:
            self.wpl_raiseException("Failed switch BIOS to \'%s\'"% region)


#######################################################################################################################
# Function Name: check_bios_region
# Date         : 17th February 2020
# Author       : Phawit P. <Phaphan@celestica.com>
#
# Procedure Revision Details:
#   Version : 1.0  - Initial Draft  - by Phawit P. <Phaphan@celestica.com>
#######################################################################################################################
    def check_bios_region(self, region, checkTool, toolOption):
        self.wpl_log_debug('Entering procedure check_bios_region with args : %s' %(str(locals())))
        cmd = (SPI_UTIL_PATH + checkTool + ' ' + toolOption)
        output = self.wpl_execute(cmd, mode='openbmc')
        passCount = 0
        for line in output.splitlines():
            line = line.strip()
            match = re.search(region,line)
            if match:
                passCount += 1

        if passCount != 0:
            self.wpl_log_success("Successfully check_bios_region: %s" %region)
        else:
            self.wpl_raiseException("Failed check_bios_region. %s region not found." %region)

        return passCount


#######################################################################################################################
# Function Name: verify_bios
# Date         : 17th February 2020
# Author       : Phawit P. <Phaphan@celestica.com>
#
# Procedure Revision Details:
#   Version : 1.0  - Initial Draft  - by Phawit P. <Phaphan@celestica.com>
#######################################################################################################################
    def verify_bios(self, bios_image, readFile, img_path=FW_IMG_PATH):
        self.wpl_log_debug('Entering procedure verify_bios with args : %s' %(str(locals())))
        errCount = 0
        p1 = 'Files ' + bios_image + ' and bios differ'
        cmd = 'cd ' + img_path
        self.wpl_getPrompt("openbmc", 600)
        self.wpl_transmit(cmd)
        cmd = 'diff ' + bios_image + ' ' + readFile
        self.wpl_log_debug('cmd = %s' % cmd)
        output = self.wpl_execute(cmd, mode='openbmc')
        for line in output.splitlines():
            line = line.strip()
            match = re.search(p1,line)
            if match:
                errCount += 1
        cmd = 'rm -rf '+readFile
        self.wpl_execute(cmd, mode='openbmc')
        time.sleep(10)
        if errCount:
            self.wpl_log_fail('Exiting verify_bios with result FAIL')
            self.wpl_raiseException("Failure while testing 'Compare Bios File' with File '%s' and 'bios'" % bios_image)
        else:
            self.wpl_log_success("Successfully testing 'Compare Bios File' with File '%s' and 'bios'" % bios_image)

#######################################################################################################################
    # Function Name: verify_each_pcie_a
    # Date         : 7th Seq 2020
    # Author       : Eric Zhang <zfzhang@celestica.com>
    #
    # Procedure Revision Details:
    #   Version : 1.0  - Initial Draft  - by Eric Zhang <zfzhang@celestica.com>
#######################################################################################################################
    def verify_each_pcie_a(self, toolName, option, pass_pattern):
        self.wpl_log_debug('Entering procedure verify each pcie option a : %s\n' % (str(locals())))
        cmd = toolName + ' ' + option
        output = self.wpl_execute(cmd, mode='centos', timeout=1200)
        self.wpl_log_debug('**********output=%s ****************' % output)
        count = 0
        for line in output.splitlines():
            line = line.strip()
            match = re.search(pass_pattern , line)
            if match:
                count += 1
        if count:
            self.wpl_log_success('verify_each pcie option a test result for DIAG tool - %s is PASSED\n' % toolName)
        else:
            self.wpl_log_fail('Exiting verify_each pcie option a with result FAIL')
            self.wpl_raiseException(
                    "Failure while testing each pcie option  '%s' with Option: '%s'" % (toolName, option))

#######################################################################################################################
# Function Name: verify_cpu_software_version
# Date         : 17th February 2020
# Author       : Phawit P. <Phaphan@celestica.com>
#
# Procedure Revision Details:
#   Version : 1.0  - Initial Draft  - by Phawit P. <Phaphan@celestica.com>
#######################################################################################################################
    def verify_cpu_software_version(self, toolName, option, pattern, dev_ver, dev):
        self.wpl_log_debug('Entering procedure verify_cpu_software_version with args : %s' %(str(locals())))
        passCount = 0
        cmd = 'cd ' + DIAG_TOOL_PATH
        self.wpl_getPrompt("centos", 600)
        self.wpl_transmit(cmd)
        output = self.EXEC_diag_tool_command(toolName, option)
        self.wpl_log_debug('output = %s' % output)
        for line in output.splitlines():
            line = line.strip()
            match = re.search(pattern, line)
            if match:
                if match.group(1) == dev_ver:
                    passCount += 1
        if passCount:
            self.wpl_log_success("Passed to check %s version \'%s\'"% (dev, dev_ver))
        else:
            self.wpl_raiseException("Failed  to check %s version \'%s\'"% (dev, dev_ver))


#######################################################################################################################
# Function Name: fw_util_exec
# Date         : 24th February 2020
# Author       : Phawit P. <Phaphan@celestica.com>
#
# Procedure Revision Details:
#   Version : 1.0  - Initial Draft  - by Phawit P. <Phaphan@celestica.com>
#######################################################################################################################
    def fw_util_exec(self, toolName, fru, opt, dev, image, check_pattern, img_path=FW_IMG_PATH, tool_path=BMC_DIAG_TOOL_PATH, exec_mode=default_mode):
        self.wpl_log_debug('Entering procedure fw_util_exec with args : %s' %(str(locals())))
        passCount = 0
        patternNum = len(check_pattern)
        cmd = 'cd ' + img_path
        self.wpl_getPrompt(exec_mode, 600)
        self.wpl_transmit(cmd)
        cmd = tool_path + toolName + ' ' + fru + ' --' + opt + ' ' + dev + ' ' + image
        self.wpl_log_debug('command = %s' % cmd)
        output = self.wpl_execute(cmd, mode=exec_mode, timeout=1800)
        for line in output.splitlines():
            line = line.strip()
            for i in range(0, patternNum):
                match = re.search(check_pattern[i], line)
                if match:
                    passCount += 1
        if passCount == patternNum:
            self.wpl_log_success("Successfully %s %s \'%s\'"% (toolName, dev, image))
        else:
            self.wpl_raiseException("Failed %s %s \'%s\'"% (toolName, dev, image))


#######################################################################################################################
# Function Name: verify_th3_version_by_sdk
# Date         : 18th February 2020
# Author       : Phawit P. <Phaphan@celestica.com>
#
# Procedure Revision Details:
#   Version : 1.0  - Initial Draft  - by Phawit P. <Phaphan@celestica.com>
#######################################################################################################################
    def verify_th3_version_by_sdk(self, sdk_file, pattern, bios_ver):
        self.wpl_log_debug('Entering procedure verify_th3_version_by_sdk with args : %s' %(str(locals())))
        passCount = 0
        self.wpl_log_success("Entering verify_th3_version_by_sdk...\n")
        cmd = 'cd ' + SDK_UTIL_PATH
        self.wpl_getPrompt("centos", 600)
        self.wpl_transmit(cmd)
        cmd = './' + sdk_file
        self.wpl_transmit(cmd)
        self.wpl_receive("BCM.0>", timeout=300)
        cmd='pciephy fw version'
        self.wpl_transmit(cmd)
        output = self.wpl_receive("BCM.0>", timeout=300)
        self.wpl_log_debug('output = %s' % output)
        for line in output.splitlines():
            line = line.strip()
            match = re.search(pattern, line)
            if match:
                if match.group(1) == bios_ver:
                    passCount += 1
        self.wpl_transmit('exit')
        self.wpl_receive("root@localhost")
        if passCount:
            self.wpl_log_success("Passed to check BIOS version \'%s\'"% bios_ver)
        else:
            self.wpl_raiseException("Failed  to check BIOS version \'%s\'"% bios_ver)

#######################################################################################################################
# Function Name: verity_eth_test_dict_option
# Date         : 24th seq 2020
# Author       : Eric Zhang<zfzhang@celestica.com>
#
# Procedure Revision Details:
#   Version : 1.0  - Initial Draft  - by Eric Zhang<zfzhang@celestica.com>
#######################################################################################################################
    def verity_eth_test_dict_option(self, toolName, option, pattern = None, pass_pattern = None, path = BMC_DIAG_TOOL_PATH):
        self.wpl_log_debug('Entering procedure verity_eth_test_dict_option with args : %s' % (str(locals())))
        if path:
            command = 'cd ' + path
            self.wpl_transmit(command)

        pattern_len = len(pattern)
        passCount = 0
        output = self.EXEC_bmc_diag_tool_command(toolName, option)
        self.wpl_log_debug("*************output=%s*******" % output)
        for line in output.splitlines():
            line = line.strip()
            for i in range(0, pattern_len):
                match = re.search(pattern[i], line)
                if match:
                    passCount += 1

        self.wpl_log_debug("passCount = %s " % passCount)
        self.wpl_log_debug("pattern_len = %s " % pattern_len)
        if passCount == pattern_len:
            self.wpl_log_success("Successfully %s %s "% (toolName, option))
        else:
            self.wpl_raiseException("Failed %s %s "% (toolName, option))

#######################################################################################################################
# Function Name: add_ip_to_config_file
# Date         : 21st February 2020
# Author       : Phawit P. <Phaphan@celestica.com>
#
# Procedure Revision Details:
#   Version : 1.0  - Initial Draft  - by Phawit P. <Phaphan@celestica.com>
#######################################################################################################################
    def add_ip_to_config_file(self, ip, configFile):
        self.wpl_log_debug('Entering procedure add_ip_to_config_file with args : %s' %(str(locals())))
        cmd = 'sed -i \'s/ip:   ".*"/ip:   "' + ip + '"/g\' ' + configFile
        p1='ip:   "' + ip + '"'
        passCount = 0
        self.wpl_log_debug('cmd = %s' % cmd)
        self.wpl_transmit(cmd)
        self.wpl_receive("root@localhost")
        cmd = 'cat ' + configFile
        self.wpl_log_debug('cmd = %s' % cmd)
        output = self.wpl_execute(cmd)
        for line in output.splitlines():
            line = line.strip()
            match = re.search(p1, line)
            if match:
                passCount += 1
        if passCount:
            self.wpl_log_success("Passed to add ip: \'%s\' in config file"% ip)
        else:
            self.wpl_raiseException("Failed to add ip: \'%s\' in config file"% ip)


#######################################################################################################################
# Function Name: verify_bmc_software_version
# Date         : 21st February 2020
# Author       : Phawit P. <Phaphan@celestica.com>
#
# Procedure Revision Details:
#   Version : 1.0  - Initial Draft  - by Phawit P. <Phaphan@celestica.com>
#######################################################################################################################
    def verify_bmc_software_version(self, toolName, option, pattern, dev_ver, dev):
        self.wpl_log_debug('Entering procedure verify_bmc_software_version with args : %s' %(str(locals())))
        passCount = 0
        cmd = 'cd ' + BMC_DIAG_TOOL_PATH
        self.wpl_getPrompt("openbmc", 600)
        self.wpl_transmit(cmd)
        output = self.EXEC_bmc_diag_tool_command(toolName, option)
        self.wpl_log_debug('output = %s' % output)
        for line in output.splitlines():
            line = line.strip()
            match = re.search(pattern, line)
            self.wpl_log_debug('line = %s' % line)
            if match:
                self.wpl_log_debug('MATCH!!!!')
                if match.group(1) == dev_ver:
                    passCount += 1
        if passCount:
            self.wpl_log_success("Passed to check %s version \'%s\'"% (dev, dev_ver))
        else:
            self.wpl_raiseException("Failed  to check %s version \'%s\'"% (dev, dev_ver))


#######################################################################################################################
# Function Name: update_tool_exec
# Date         : 24th February 2020
# Author       : Phawit P. <Phaphan@celestica.com>
#
# Procedure Revision Details:
#   Version : 1.0  - Initial Draft  - by Phawit P. <Phaphan@celestica.com>
#######################################################################################################################
    def update_tool_exec(self, toolName, image, option, dev, check_pattern, img_path=FW_IMG_PATH):
        self.wpl_log_debug('Entering procedure update_tool_exec with args : %s' %(str(locals())))
        passCount = 0
        patternNum = len(check_pattern)
        cmd = 'cd ' + img_path
        self.wpl_getPrompt("openbmc", 600)
        self.wpl_transmit(cmd)
        cmd = '/usr/local/packages/utils/' + toolName + ' ' + image + ' ' + option
        self.wpl_log_debug('cammand = %s' % cmd)
        output = self.wpl_execute(cmd, mode='openbmc', timeout=1800)
        for line in output.splitlines():
            line = line.strip()
            for i in range(0, patternNum):
                match = re.search(check_pattern[i], line)
                if match:
                    passCount += 1
        if passCount == patternNum:
            self.wpl_log_success("Successfully %s %s \'%s\'"% (toolName, dev, image))
        else:
            self.wpl_raiseException("Failed %s %s \'%s\'"% (toolName, dev, image))


#######################################################################################################################
# Function Name: verify_option_bmc_diag_tool_simple_dict
# Date         : February 25th 2020
# Author       : Phawit P. <Phaphan@celestica.com>
#
# Procedure Revision Details:
#   Version : 1.0  - Initial Draft  - by Phawit P. <Phaphan@celestica.com>
#######################################################################################################################
    def verify_option_bmc_diag_tool_simple_dict(self, inputArray, toolName, option, pattern='none'):
        self.wpl_log_debug('Entering procedure verify_option_bmc_diag_tool_simple_dict with args : %s' %(str(locals())))
        errCount = 0
        output = self.EXEC_bmc_diag_tool_command(toolName, option)
        parsedOutput = parserDIAGLibs.PARSE_bmc_diagtool_info(output, pattern, inputArray)
        errCount += CommonLib.compare_input_dict_to_parsed(parsedOutput, inputArray)
        if errCount:
            self.wpl_log_fail('Exiting verify_option_bmc_diag_tool_simple_dict with result FAIL')
            self.wpl_raiseException("Failure while testing BMC DIAG tool '%s' with Option: '%s'" %(toolName, option))
        else:
            self.wpl_log_success('Option: %s test result for BMC DIAG tool - %s is PASSED\n' %(option, toolName))


#######################################################################################################################
# Function Name: verify_bmc_fpga_diag_simple_dict
# Date         : July 23th 2020
# Author       : Hemin <hemin@celestica.com>
#
# Procedure Revision Details:
#   Version : 1.0  - Initial Draft  - by Hemin <hemin@celestica.com>
#######################################################################################################################
    def verify_bmc_fpga_diag_simple_dict(self, toolName, option, path=BMC_DIAG_TOOL_PATH):
        self.wpl_log_debug('Entering procedure verify_bmc_fpga_diag_simple_dict with args : %s' % (str(locals())))
        passCount = 0
        output = self.EXEC_bmc_diag_tool_command(toolName, option, path)
        for line in output.splitlines():
            line = line.strip()
            if 'PASS' in line:
                passCount += 1
            else:
                continue
        if passCount == 2:
            self.wpl_log_success('verify_bmc_fpga_diag_simple_dict test result for DIAG tool - %s is PASSED\n' % toolName)
        else:
            self.wpl_log_fail('Exiting verify_bmc_fpga_diag_simple_dict with result FAIL')
            self.wpl_raiseException("Failure while testing BMC DIAG tool '%s' with Option: '%s'" % (toolName, option))


#######################################################################################################################
# Function Name: verify_emmc_information
# Date         : 27th July 2020
# Author       : hemin <hemin@celestica.com>
#
# Procedure Revision Details:
#   Version : 1.0  - Initial Draft  - by hemin <hemin@celestica.com>
#######################################################################################################################
    def verify_emmc_information(self, toolName, option, cmd_str1, cmd_str2, keywords_pattern, path=BMC_DIAG_TOOL_PATH):
        self.wpl_log_debug('Entering procedure verify_emmc_information with args : %s' % (str(locals())))
        match_str1 = ''
        match_str2 = ''
        passCount = 0
        p_pass = keywords_pattern[1]
        output1 = self.EXEC_bmc_diag_tool_command(toolName, option, path)
        self.wpl_log_debug('output = %s' % output1)
        for line in output1.splitlines():
            line = line.strip()
            match1 = re.search(p_pass, line)
            if match1:
                match_str1 += match1.group()
            else:
                continue
        output2 = self.wpl_execute(cmd_str1, mode='openbmc', timeout=600)
        self.wpl_log_debug('output = %s' % output2)
        for line in output2.splitlines():
            line = line.strip()
            match2 = re.search(p_pass, line)
            if match2:
                match_str2 += match2.group()
            else:
                continue
        output = self.wpl_execute(cmd_str2, mode='openbmc', timeout=600)
        for line in output.splitlines():
            line =line.strip()
            if "mmc0" in line:
                passCount += 1
        if match_str1 == match_str2 and passCount:
            self.wpl_log_success('verify_emmc_information test result for DIAG tool - %s is PASSED\n' % cmd_str1)
        else:
            self.wpl_log_fail('Exiting verify_emmc_information with result FAIL')
            self.wpl_raiseException("Failure while testing DIAG tool '%s' and cmd: '%s'" % (cmd_str1, cmd_str2))


#######################################################################################################################
# Function Name: verify_memory_information
# Date         : 28th July 2020
# Author       : hemin <hemin@celestica.com>
#
# Procedure Revision Details:
#   Version : 1.0  - Initial Draft  - by hemin <hemin@celestica.com>
#######################################################################################################################
    def verify_memory_information(self, toolName, option, cmd, path=BMC_DIAG_TOOL_PATH):
        self.wpl_log_debug('Entering procedure verify_memory_information with args : %s' % (str(locals())))
        result_list1 = []
        result_list2 = []
        errorCount = 0
        output1 = self.EXEC_bmc_diag_tool_command(toolName, option, path)
        for line in output1.splitlines():
            line = line.strip()
            if line.endswith('kb'):
                result_list1.append(line)

        output2 = self.wpl_execute(cmd, mode='openbmc', timeout=600)
        for line in output2.splitlines():
            line = line.strip()
            if line.endswith("kb"):
                result_list2.append(line)

        for i in result_list1:
            if i in result_list2:
                continue
            else:
                errorCount += 1
        if errorCount:
            self.wpl_log_fail('Exiting verify_memory_information with result FAIL')
            self.wpl_raiseException("Failure while testing DIAG tool '%s'" % cmd)
        else:
            self.wpl_log_success('verify_memory_information test result for DIAG tool - %s is PASSED\n' % cmd)

#######################################################################################################################
# Function Name: verify_cpld_update_SMB_version
# Date         : Seq 17th 2020
# Author       : Eric Zhang <zfzhang@celestica.com>
#
# Procedure Revision Details:
#   Version : 1.0  - Initial Draft  - by Eric Zhang <zfzhang@celestica.com>
#######################################################################################################################
    def verify_cpld_update_SMB_version(self, toolName, option, keywords_pattern = 'none', pass_pattern = 'none', path=BMC_DIAG_TOOL_PATH, is_negative_test=False):
        self.wpl_log_debug('Entering procedure verify_cpld_update_SMB_version : %s' % (str(locals())))
        passCount = 0
        path_ls = Update_CPLD_SMB_Image_PATH
        command = 'ls'
        cmd_output = self.EXEC_i2c_cpld_SMB_version(command, path_ls)
        self.wpl_log_debug('************cmd_output=%s ************' % cmd_output)
        new_option = ''
        for line_output in cmd_output.splitlines():
            line_output = line_output.strip()
            if '.bin' in line_output:
                for line_put in line_output.split():
                    if '.bin' in line_put:
                        line_put = 'Mi' + line_put.split('Mi')[-1]
                        new_option = option + line_put + ' sw'
                        self.wpl_log_debug('******line_put=%s*****' % line_put)
                        self.wpl_log_debug('*******new_option=%s*****' % new_option)
                        break
        patternNum = len(keywords_pattern)
        output = self.EXEC_bmc_diag_tool_command(toolName, new_option, path)
        self.wpl_log_debug('output = %s' % output)

        pass_p = []
        pattern_all = []
        for line in output.splitlines():
            line = line.strip()
            for i in range(0, patternNum):
                p_pass = keywords_pattern[i] + pass_pattern
                pattern_all.append(p_pass)
                match = re.search(p_pass, line)
                if is_negative_test == True:
                    if match:
                        passCount -= 1
                else:
                    if match:
                        passCount += 1
                        pass_p.append(p_pass)
        mismatch_pattern = set(pattern_all) - set(pass_p)
        self.wpl_log_debug('passCount = %s' % passCount)
        self.wpl_log_debug('patternNum = %s' % patternNum)
        if passCount == patternNum:
            self.wpl_log_success('verify_cpld_update_SMB_version test result for DIAG tool - %s is PASSED\n' % toolName)
        else:
            self.wpl_log_fail('Exiting verify_cpld_update_SMB_version with result FAIL, mismatch items: [{}]'.format(
                CommonLib.get_readable_strings(mismatch_pattern)))
            self.wpl_raiseException("Failure while testing DIAG tool '%s' with Option: '%s'" % (toolName, option))

    def EXEC_cpld_update_SMB(self, toolName, option, path=BMC_DIAG_TOOL_PATH):
        self.wpl_log_debug('Entering procedure EXEC_cpld_update_SMB : %s' % (str(locals())))
        if path:
            cmd = 'cd ' + path
            self.wpl_transmit(cmd)

        command = './' + toolName + option
        self.wpl_log_debug("command = %s" % (command))
        return self.wpl_execute(command, mode=openbmc_mode, timeout=600)

#######################################################################################################################
# Function Name: verify_i2c_cpld_SMB_version, EXEC_i2c_cpld_SMB_version
# Date         : Seq 16th 2020
# Author       : Eric Zhang <zfzhang@celestica.com>
#
# Procedure Revision Details:
#   Version : 1.0  - Initial Draft  - by Eric Zhang <zfzhang@celestica.com>
#######################################################################################################################
    def EXEC_i2c_cpld_SMB_version(self, cmd, path=''):
        self.wpl_log_debug('Entering procedure EXEC_i2c_cpld_SMB_version : %s' % (str(locals())))
        if path:
            command = 'cd ' + path
            self.wpl_log_debug("command = %s" % (command))
            self.wpl_transmit(command)

        return self.wpl_execute_cmd(cmd, mode=openbmc_mode, timeout=600)

    def verify_i2c_cpld_SMB_version(self, toolName, option, keywords_pattern='none', pass_pattern='none', path=BMC_DIAG_TOOL_PATH, is_negative_test=False):
        self.wpl_log_debug('Entering procedure verify_i2c_cpld_SMB_version : %s' %(str(locals())))
        passCount = 0
        command = "ls | grep -E 'SMB_CPLD_TOP_v[0-9.]+bin'"
        path_ls = CPLD_MiniPack2_SMB_CPLD_TOP_PATH
        cmd_output = self.EXEC_i2c_cpld_SMB_version(command, path_ls)
        new_option = ''
        for line_output in cmd_output.splitlines():
            line_output = line_output.strip()
            if 'MiniPack2_SMB_CPLD' in line_output:
                new_option = option + line_output
                break
        patternNum = len(keywords_pattern)
        output = self.EXEC_bmc_diag_tool_command(toolName, new_option, path)
        self.wpl_log_debug('output = %s' % output)

        pass_p = []
        pattern_all = []
        for line in output.splitlines():
            line = line.strip()
            for i in range(0, patternNum):
                p_pass = keywords_pattern[i] + pass_pattern
                pattern_all.append(p_pass)
                match = re.search(p_pass, line)
                if is_negative_test == True:
                    if match:
                        passCount -= 1
                else:
                    if match:
                        passCount += 1
                        pass_p.append(p_pass)
        mismatch_pattern = set(pattern_all) - set(pass_p)
        self.wpl_log_debug('passCount = %s' % passCount)
        self.wpl_log_debug('patternNum = %s' % patternNum)
        if passCount == patternNum:
            self.wpl_log_success('verify_i2c_cpld_SMB_version test result for DIAG tool - %s is PASSED\n' % toolName)
        else:
            self.wpl_log_fail('Exiting verify_i2c_cpld_SMB_version with result FAIL, mismatch items: [{}]'.format(
                CommonLib.get_readable_strings(mismatch_pattern)))
            self.wpl_raiseException("Failure while testing DIAG tool '%s' with Option: '%s'" % (toolName, option))

#######################################################################################################################
# Function Name: verify_bmc_diag_tool_simple_dict_fpga
# Date         : January 8th 2020
# Author       : Eric Zhang <zfzhang@celestica.com>
#
# Procedure Revision Details:
#   Version : 1.0  - Initial Draft  - by Eric Zhang <zfzhang@celestica.com>
#######################################################################################################################
    def verify_bmc_diag_tool_simple_dict_fpga(self, toolName, option, keywords_pattern='none', pass_pattern='none', path=BMC_DIAG_TOOL_PATH, is_negative_test=False):
        self.wpl_log_debug('Entering procedure verify_bmc_diag_tool_simple_dict_fpga with args : %s' % (str(locals())))
        passCount = 0
        new_option = option

        patternNum = len(keywords_pattern)
        self.wpl_log_debug('new_option = %s' % new_option)
        output = self.EXEC_bmc_diag_tool_command(toolName, new_option, path)
        self.wpl_log_debug('output = %s' % output)
        pass_p = []
        pattern_all = []
        for line in output.splitlines():
            line = line.strip()
            if 'FPGA' in line:
                line = line.replace('.0', '.')
            for i in range(0, patternNum):
                p_pass = keywords_pattern[i] + pass_pattern
                pattern_all.append(p_pass)
                match = re.search(p_pass, line)
                if is_negative_test == True:
                    if match:
                        passCount -= 1
                else:
                    if match:
                        passCount += 1
                        pass_p.append(p_pass)
        mismatch_pattern = set(pattern_all) - set(pass_p)
        self.wpl_log_debug('passCount = %s' % passCount)
        self.wpl_log_debug('patternNum = %s' % patternNum)
        if passCount == patternNum:
            self.wpl_log_success('verify_diag_tool_simple_dict test result for DIAG tool - %s is PASSED\n' % toolName)
        else:
            self.wpl_log_fail('Exiting verify_diag_tool_simple_dict with result FAIL, mismatch pattern:{}'.format(mismatch_pattern))
            self.wpl_raiseException("Failure while testing DIAG tool '%s' with Option: '%s'" % (toolName, option))


    def dc_power_check(self):
        self.wpl_log_debug('Entering procedure dc_power_check with args : %s' % (str(locals())))
        devicename = os.environ.get("deviceName", "")
        if 'minipack2' in devicename.lower() or 'wedge400c' in devicename.lower() or 'wedge400_' in devicename.lower():
            if 'minipack2_dc' in devicename.lower():
                cmd = "sensor-util psu3 |grep 'PSU3_IN_VOLT' |awk '{print$4}'"
            else:
                cmd = "sensor-util psu2 |grep 'PSU2_IN_VOLT' |awk '{print$4}'"
            output = self.wpl_execute(cmd, mode=openbmc_mode, timeout=30)
            p1 = r'^\d+'
            for line in output.splitlines():
                line = line.strip()
                match = re.search(p1, line)
                if match:
                    volt_value = match.group()
                    if float(volt_value) > 60:
                        self.wpl_log_info("This unit use AC PSU")
                        return 'AC'
                    else:
                        self.wpl_log_info("This unit use DC")
                        return 'DC'

    def power_type_check_w400(self):
        self.wpl_log_debug('Entering procedure power_type_check_w400 with args : %s' % (str(locals())))
        self.wpl_getPrompt('openbmc', 600)
        cmd = 'cd ' + BMC_DIAG_TOOL_PATH
        self.wpl_transmit(cmd)
        devicename = os.environ.get("deviceName", "")
        if 'wedge400_' in devicename.lower():
            if 'wedge400_dc' in devicename.lower():
                dc_cmd = './cel-diag-init -d'
                self.wpl_transmit(dc_cmd)
                self.wpl_log_info('It is dc unit!')
            elif 'wedge400_mp' in devicename.lower():
                mp_cmd = './cel-diag-init -m'
                self.wpl_transmit(mp_cmd)
                self.wpl_log_info('It is respin pem unit!')
            else:
                ac_cmd = './cel-diag-init -a'
                self.wpl_transmit(ac_cmd)
                self.wpl_log_info('It is ac unit!')

#######################################################################################################################
# Function Name: verify_bmc_diag_tool_simple_dict
# Date         : January 27th 2020
# Author       : Phawit P. <Phaphan@celestica.com>
#
# Procedure Revision Details:
#   Version : 1.0  - Initial Draft  - by Phawit P. <Phaphan@celestica.com>
#######################################################################################################################
    def verify_bmc_diag_tool_simple_dict(self, toolName, option, keywords_pattern='none', pass_pattern='none', path=BMC_DIAG_TOOL_PATH, is_negative_test=False, prefix="./"):
        self.wpl_log_debug('Entering procedure verify_bmc_diag_tool_simple_dict with args : %s' %(str(locals())))
        passCount = 0
        time.sleep(3)
        new_option = option
        power_type = self.dc_power_check()
        if power_type == 'DC':
            if toolName == cel_psu_test["bin_tool"] and option == "-s":
                keywords_pattern = cel_psu_test_s_pattern_dc
            if toolName == cel_psu_test["bin_tool"] and option == "-i":
                keywords_pattern = cel_psu_test_i_pattern_dc
            if 'psu1' in new_option:
                self.wpl_log_info('This is DC unit, skip the psu1 check !!!')
                return
        devicename = os.environ.get("deviceName", "")
        if 'minipack2_dc' in devicename.lower() or 'minipack2_rsp2-02' in devicename.lower() or 'minipack2_rsp2-03' in devicename.lower() or 'minipack2_rsp2-04' in devicename.lower():
            if 'minipack2_dc-04' in devicename.lower() or 'minipack2_dc-05' in devicename.lower():
                if (('pim3' in new_option) or ('pim4' in new_option) or ('pim5' in new_option) or ('pim6' in new_option)) and ((toolName == 'cel-i2c-test') or (toolName == 'cel-sensor-test')):
                    return
            else:
                if (('pim3' in new_option) or ('pim4' in new_option) or ('pim5' in new_option)) and ((toolName == 'cel-i2c-test') or (toolName == 'cel-sensor-test')):
                    return
            if toolName == 'cel-cpld-test' and option == '-h':
                keywords_pattern = cpld_option_h_dc
            if toolName == cel_sensor_test["bin_tool"] and (('psu1' in option) or ('psu2' in option)):
                return
            if toolName == cel_platform_test["bin_tool"] and (('pim3' in option) or ('pim4' in option) or ('pim5' in option) or ('pim6' in option)):
                return
            if toolName == cel_platform_test["bin_tool"] and ('-p' in option):
                keywords_pattern = cel_platform_test_p_pattern_dc

        # To append the fan type
        if toolName == cel_fan_test["bin_tool"] and option == "-c":
            new_option += " " + self.fan_manufacturer

        patternNum = len(keywords_pattern)
        self.wpl_log_debug('new_option = %s' % new_option)
        output = self.EXEC_bmc_diag_tool_command(toolName, new_option, path, prefix)
        self.wpl_log_debug('output = %s' % output)

        # To make sure BMC is boot from master first
        if toolName == cel_boot_test["bin_tool"] and \
            option == "-b bmc -r master && echo 'To make sure bmc is boot from master first'":
            match = re.search(r'BMC[ \t]+will[ \t]+switch[ \t]+to[ \t]+master[ \t]+after[ \t]+10[ \t]+seconds...', output)
            if match:
                self.wait_for_openbmc_prompt_back()

        # To make sure BMC is boot from master first
        if toolName == cel_boot_test["bin_tool"] and \
            option == "-b bios -r master && echo 'To make sure bios is boot from master first'":
            match = re.search(r'BMC[ \t]+will[ \t]+switch[ \t]+to[ \t]+master[ \t]+after[ \t]+10[ \t]+seconds...', output)
            if match:
                self.wait_for_openbmc_prompt_back()

        # To save the Diag PSU info
        temp_catch_psu_info_pattern = catch_psu_info_pattern.copy()
        if toolName == cel_psu_test["bin_tool"] and option == "-i":
            lines = output.splitlines()
            for line in lines:
                for pindex, pattern in enumerate(temp_catch_psu_info_pattern):
                    compiled = re.compile(pattern)
                    match = compiled.search(line)
                    if match:
                        temp_catch_psu_info_pattern.pop(pindex)
                        for n in range(1, compiled.groups + 1, 1):
                            self._psu_diag.append(match.group(n))

                    break

        # To save the openbmc PSU info
        if toolName == "psu-util" and option == "psu1 --get_psu_info":
            for pattern in catch_psu1_info_pattern:
                compiled = re.compile(pattern)
                match = compiled.search(output)
                if match:
                    for n in range(1, compiled.groups + 1, 1):
                        self._psu_openbmc.append(match.group(n))

        if toolName == "psu-util" and option == "psu2 --get_psu_info":
            for pattern in catch_psu2_info_pattern:
                compiled = re.compile(pattern)
                match = compiled.search(output)
                if match:
                    for n in range(1, compiled.groups + 1, 1):
                        self._psu_openbmc.append(match.group(n))

        if toolName == "psu-util" and option == "psu1 --get_eeprom_info":
            for pattern in catch_psu1_fru_info_pattern:
                compiled = re.compile(pattern)
                match = compiled.search(output)
                if match:
                    for n in range(1, compiled.groups + 1, 1):
                        self._psu_openbmc.append(match.group(n))

        if toolName == "psu-util" and option == "psu2 --get_eeprom_info":
            for pattern in catch_psu2_fru_info_pattern:
                compiled = re.compile(pattern)
                match = compiled.search(output)
                if match:
                    for n in range(1, compiled.groups + 1, 1):
                        self._psu_openbmc.append(match.group(n))

        devicename = os.environ.get("deviceName", "")
        if 'wedge400_dc' in devicename.lower() or 'wedge400c_dc' in devicename.lower():
            if toolName == "psu-util" and option == "psu2 --get_eeprom_info && sysctl -w kernel.printk=7":
                keywords_pattern = catch_psu2_fru_info_pattern_dc
                patternNum = len(keywords_pattern)
        if 'wedge400_dc' in devicename.lower() or 'wedge400_rsp' in devicename.lower():
            if toolName == 'cel-software-test' and ((option == '-i') or (option == '-v')):
                keywords_pattern = cel_software_test_i_or_v_pattern_dc

        # To save the FAN type
        if toolName == "feutil" and option == "all":
            matchs = re.findall(catch_fan1_manufacturer, output)
            if matchs:
                if str(matchs[0]).upper() == "CLS":
                    self.fan_manufacturer = "AVC"
                elif str(matchs[0]).upper() == "CLSDELTA" or str(matchs[0]).upper() == "CLSDEL":
                    self.fan_manufacturer = "DELTA"
                elif str(matchs[0]).upper() == "CLSSANYO":
                    self.fan_manufacturer = "SANYO"
                elif str(matchs[0]).upper() == "CLSSUNON":
                    self.fan_manufacturer = "SUNON"
                elif str(matchs[0]).upper() == "CLSAVC":
                    self.fan_manufacturer = "AVC"
                else:
                    self.wpl_raiseException(
                        "The fan1 manufacturer not match\n" \
                        "Manufacturers = %s" % matchs)
            else:
                self.wpl_raiseException(
                    "The fan1 manufacturer not exist\n" \
                    "Manufacturers = %s" % matchs)

        # To save / verify OpenBMC, CPLD, FPGA and BIOS versions
        if toolName == "cat" and option == "/etc/issue":
            match = re.search(catch_openbmc_version_pattern, output)
            if match:
                self.openbmc_version_by_cat = match.group('version')
            else:
                self.openbmc_version_by_cat = "Not found"

        if toolName == "cpld_ver.sh":
            match = re.search(catch_scm_version_pattern, output)
            if match:
                self.cpld_scm_version_by_cpld_ver_sh = match.group('version')
            else:
                self.cpld_scm_version_by_cpld_ver_sh = "Not found"

            match = re.search(catch_smb_version_pattern, output)
            if match:
                self.cpld_smb_version_by_cpld_ver_sh = match.group('version')
            else:
                self.cpld_smb_version_by_cpld_ver_sh = "Not found"

        if toolName == "fpga_ver.sh":
            match = re.search(catch_fpga1_version_pattern, output)
            if match:
                self.fpga1_version_by_fpga_ver_sh = match.group('version')
            else:
                self.fpga1_version_by_fpga_ver_sh = "Not found"

            match = re.search(catch_fpga2_version_pattern, output)
            if match:
                self.fpga2_version_by_fpga_ver_sh = match.group('version')
            else:
                self.fpga2_version_by_fpga_ver_sh = "Not found"

        if toolName == "fw-util" and option == "all --version":
            match = re.search(catch_bios_version_pattern, output)
            if match:
                self.bios_version_by_fw_util = match.group('version')
            else:
                self.bios_version_by_fw_util = "Not found"
        pass_p = []
        pattern_all = []
        devicename = os.environ.get("deviceName", "")
        if 'wedge400_' in devicename.lower() and toolName == 'cel-i2c-test' and option == '  -a':
            pass_pattern = 'OK'
            flag_try = 0
            error_count  = 0
            first_i2c_device = ''
            second_i2c_device = ''
            keywords_pattern = ['([\w\d\_\-]+)\s+\d{1,2}\s+0x[0-9a-fA-F]{1,2}\s+(\w+)']
            for line in output.splitlines():
                line = line.strip()
                if 'SMB_OCP_CARD' in line:
                    self.wpl_log_info('skip OCP card check!!!')
                    continue
                for i in range(0, patternNum):
                    p_pass = keywords_pattern[i]
                    # self.wpl_log_debug('p_pass = %s' % p_pass)
                    match = re.search(p_pass, line)
                    if match:
                        passCount += 1
                        i2c_device_name = match.group(1)
                        i2c_device_result = match.group(2)
                        if i2c_device_result == pass_pattern:
                            if i2c_device_name == first_i2c_device:
                                flag_try = 0
                                first_i2c_device = ''
                                second_i2c_device = ''
                            self.wpl_log_info('i2c device %s test pass!'%i2c_device_name)
                        else:
                            if i2c_device_result == 'NO':
                                if i2c_device_name == first_i2c_device:
                                    second_i2c_device = i2c_device_name
                                    flag_try += 1
                                    continue
                                elif i2c_device_name == second_i2c_device:
                                    flag_try += 1
                                else:
                                    first_i2c_device = i2c_device_name
                                    flag_try += 1
                                    continue
                                if flag_try == 3:
                                    error_count += 1
                                    self.wpl_log_fail('i2c device %s test fail!'%i2c_device_name)
            if error_count or passCount == 0:
                self.wpl_raiseException("Failure while testing DIAG tool '%s' with Option: '%s'" % (toolName, option))
        else:
            for line in output.splitlines():
                line = line.strip()
                if 'FPGA' in line:
                    line = line.replace('.0','.')
                for i in range(0, patternNum):
                    p_pass = keywords_pattern[i] + pass_pattern
                    pattern_all.append(p_pass)
                    match = re.search(p_pass, line)
                    if is_negative_test == True:
                        if match:
                            passCount -= 1
                    else:
                        if match:
                            passCount += 1
                            pass_p.append(p_pass)
            mismatch_pattern = set(pattern_all)-set(pass_p)
            self.wpl_log_debug('passCount = %s' %passCount)
            self.wpl_log_debug('patternNum = %s' %patternNum)
            if not mismatch_pattern:
                self.wpl_log_success('verify_bmc_diag_tool_simple_dict test result for DIAG tool - %s is PASSED\n' %toolName)
            else:
                self.wpl_log_fail('Exiting verify_bmc_diag_tool_simple_dict with result FAIL, mismatch items: [{}]'.format(CommonLib.get_readable_strings(mismatch_pattern)))
                self.wpl_raiseException("Failure while testing DIAG tool '%s' with Option: '%s'" %(toolName, option))

#######################################################################################################################
# Function Name: check_patterns_list_pass
# Date         : January 27th 2020
# Author       : Phawit P. <Phaphan@celestica.com>
#
# Procedure Revision Details:
#   Version : 1.0  - Initial Draft  - by Phawit P. <Phaphan@celestica.com>
#######################################################################################################################
    def check_patterns_list_pass(self, cmd, patterns, path, mode=openbmc_mode):
        self.wpl_log_debug('Entering procedure check_patterns_list_pass with args : %s' %(str(locals())))
        passCount = 0
        cmd_path = "cd {} && cmd ".format(path, cmd)
        output = self.wpl_execute(cmd, mode=mode)
        result_list = parserDIAGLibs.PARSE_pattern_value(output, patterns, patterns_is_dict=False, line_mode=False)
        passCount = len(list(filter(lambda x: "PASS" in x or "OK" in x, result_list)))
        if passCount == len(patterns):
            self.wpl_log_success("{} is success".format(cmd))
        else:
            self.wpl_raiseException("failed cmd:{} ".format(cmd))


#######################################################################################################################
# Function Name: execute_check_cmd
# Date         : July 22th 2020
# Author       : Yang, Xuecun <yxcun@celestica.com>
#
# Procedure Revision Details:
#   Version : 1.0  - Initial Draft  - by Yang, Xuecun <yxcun@celestica.com>
#######################################################################################################################
    def execute_check_cmd(self, cmd, mode=None, patterns=[""], path=None, timeout=900, line_mode=True, is_negative_test=False, remark=""):
        self.wpl_log_debug('Entering procedure execute_check_cmd with args : %s' %(str(locals())))
        passCount = 0
        patternNum = len(patterns)
        self.wpl_log_debug('path:**{}**, cmd:**{}** '.format(path, cmd))
        if mode:
            self.wpl_getPrompt(mode)
        if path:
            self.wpl_transmit('cd ' + path)
        if cmd == './fpga smb r 2':
            self.switch_to_openbmc_and_check_tool()
            cmd_path = 'cd ' + BMC_DIAG_TOOL_PATH
            cmd_test = './cel-platform-test -i'
            self.wpl_transmit(cmd_path)
            output_test = self.wpl_execute_cmd(cmd_test, mode=openbmc_mode, timeout=timeout)
            if 'EVT' in output_test:
                self.wpl_log_debug("//////EVT////////")
                patterns = cel_bmc_smb_cpld_2_pass_pattern_EVT
            elif 'DVT' in output_test:
                self.wpl_log_debug("//////DVT////////")
                patterns = bmc_smb_cpld_2_pass_pattern_DVT
        output = self.wpl_execute_cmd(cmd, mode=mode, timeout=timeout)
        self.wpl_log_debug('output = ***%s***' % output)

        pass_p = []
        pattern_all = []
        for i in range(0, patternNum):
            p_pass = patterns[i]
            pattern_all.append(p_pass)
            if line_mode:
                for line in output.splitlines():
                    match = re.search(p_pass, line)
                    if match:
                        if is_negative_test:
                            passCount -= 1
                        else:
                            passCount += 1
                        pass_p.append(p_pass)
                        break
            else:
                match = re.search(p_pass, output, re.M|re.S)
                if match:
                    if is_negative_test:
                        passCount -= 1
                    else:
                        passCount += 1
                    pass_p.append(p_pass)


        if is_negative_test:
            passCount += patternNum
        mismatch_pattern = set(pattern_all)-set(pass_p) if not is_negative_test else set(pass_p)
        self.wpl_log_debug('passCount = %s' %passCount)
        self.wpl_log_debug('patternNum = %s' %patternNum)
        if remark:
            description = remark + ":" + cmd
        else:
            description = "commands:{}".format(cmd)
        if passCount == patternNum:
            self.wpl_log_success('%s is PASSED\n' %description)
        else:
            print_out_mismatch = re.sub("\s+|.*?", " ", list(mismatch_pattern)[0])
            self.wpl_log_fail('Exiting execute_check_cmd with result FAIL. {}'.format(remark))
            self.wpl_raiseException("Failure while execute: '{}' with pattern: '{}'".format(cmd, print_out_mismatch))


#######################################################################################################################
# Function Name: execute_check_dict
# Date         : Aug. 18th 2020
# Author       : Yang, Xuecun <yxcun@celestica.com>
#
# Procedure Revision Details:
#   Version : 1.0  - Initial Draft  - by Yang, Xuecun <yxcun@celestica.com>
#######################################################################################################################
    def execute_check_dict(self, cmd, mode=None, patterns_dict={}, path=None, timeout=900, line_mode=True, is_negative_test=False, remark=""):
        self.wpl_log_debug('Entering procedure execute_check_dict with args : %s' %(str(locals())))
        passCount = 0
        patternNum = len(patterns_dict)
        self.wpl_log_debug('path:**{}**, cmd:**{}** '.format(path, cmd))
        if mode:
            self.wpl_getPrompt(mode)
        if path:
            self.wpl_transmit('cd ' + path)
        output = self.wpl_execute_cmd(cmd, mode=mode, timeout=timeout)
        self.wpl_log_debug('output = ***%s***' % output)

        pass_p = []
        pattern_all = []
        for p_name, p_pass in patterns_dict.items():
            pattern_all.append(p_name)
            if line_mode:
                for line in output.splitlines():
                    match = re.search(p_pass, line)
                    if match:
                        if is_negative_test:
                            passCount -= 1
                        else:
                            passCount += 1
                        pass_p.append(p_name)
                        break
            else:
                match = re.search(p_pass, output, re.M|re.S)
                if match:
                    if is_negative_test:
                        passCount -= 1
                    else:
                        passCount += 1
                    pass_p.append(p_name)


        if is_negative_test:
            passCount += patternNum
        mismatch_pattern_name = set(pattern_all)-set(pass_p) if not is_negative_test else set(pass_p)
        self.wpl_log_debug('passCount = %s' %passCount)
        self.wpl_log_debug('patternNum = %s' %patternNum)
        if remark:
            description = remark + ":" + cmd
        else:
            description = "commands:{}".format(cmd)
        if passCount == patternNum:
            self.wpl_log_success('%s is PASSED\n' %description)
        else:
            self.wpl_log_fail('Exiting execute_check_dict with result FAIL. {}'.format(remark))
            self.wpl_raiseException("Failure while execute: '{}', with items: '{}'".format(cmd, mismatch_pattern_name))


#######################################################################################################################
# Function Name: check_usb_smart_l
# Date         : July 22th 2020
# Author       : Yang, Xuecun <yxcun@celestica.com>
#
# Procedure Revision Details:
#   Version : 1.0  - Initial Draft  - by Yang, Xuecun <yxcun@celestica.com>
#######################################################################################################################
    def check_usb_smart_l(self):
        self.wpl_log_debug('Entering procedure check_usb_smart_l with args : %s' %(str(locals())))
        var_bin_tool = cel_usb_help_array["bin_tool"]
        cmd_usb_tool_i = "cd {} && ./{} -i".format(DIAG_TOOL_PATH, var_bin_tool)
        cmd_usb_smart_l = "cd {} && {} -l selftest /dev/sda1".format(DIAG_TOOL_PATH, usb_smarttool)

        output_usb_tool_i = self.wpl_execute(cmd_usb_tool_i, mode=centos_mode)
        output_usb_smart_l = self.wpl_execute(cmd_usb_smart_l, mode=centos_mode)
        output_flag = "START OF READ SMART DATA SECTION"
        exist_flag = 0

        if output_flag in output_usb_smart_l:
            output_usb_tool_l = output_usb_smart_l.split(output_flag)[1].splitlines()[1]
            if output_usb_tool_l in output_usb_tool_i:
                self.wpl_log_success('%s is PASSED\n' %cmd_usb_smart_l)
            else:
                self.wpl_raiseException("Failure while execute: '{}', output:{}".format(cmd_usb_smart_l, output_usb_smart_l))
        else:
            self.wpl_raiseException("Failure while execute: '{}', output:{}".format(cmd_usb_smart_l, output_usb_smart_l))


#######################################################################################################################
# Function Name: check_meminfo_dmidecode
# Date         : July 24th 2020
# Author       : Yang, Xuecun <yxcun@celestica.com>
#
# Procedure Revision Details:
#   Version : 1.0  - Initial Draft  - by Yang, Xuecun <yxcun@celestica.com>
#######################################################################################################################
    def check_meminfo_dmidecode(self):
        self.wpl_log_debug('Entering procedure check_meminfo_dmidecode with args : %s' %(str(locals())))
        cmd_meminfo_dmidecode = "cat /proc/meminfo && dmidecode --type 17"

        output_meminfo_dmidecode = self.wpl_execute(cmd_meminfo_dmidecode, mode=centos_mode)
        p_err = r"error|fail"
        p_r = re.search(p_err, output_meminfo_dmidecode, re.M)
        if p_r:
            self.wpl_raiseException("Failure while execute:{}, error message is found".format(cmd_meminfo_dmidecode))

        p_meminfo_memtotal = r'MemTotal:[ \t]+(?P<memtotal>\d+) kB'
        p_meminfo_memtotal_compiled = re.compile(p_meminfo_memtotal)
        # match_memtotal = re.findall(p_memtotal, output_meminfo)
        match_meminfo_memtotal = p_meminfo_memtotal_compiled.findall(output_meminfo_dmidecode)
        if not match_meminfo_memtotal:
            self.wpl_raiseException("Failure not found meminfo MemTotal")

        p_dmidecode_memsize = r'Size: (?P<size>\d+) MB'
        p_dmidecode_memsize_compiled = re.compile(p_dmidecode_memsize)
        # match_memsize = re.findall(p_memsize, output_meminfo)
        match_dmidecode_memsize = p_dmidecode_memsize_compiled.findall(output_meminfo_dmidecode)
        if not match_dmidecode_memsize:
            self.wpl_raiseException("Failure not found dmidecode Size")

        meminfo_memtotal = 0
        for n in match_meminfo_memtotal:
            meminfo_memtotal += int(n)

        dmidecode_memsize = 0
        for n in match_dmidecode_memsize:
            dmidecode_memsize += int(n)

        # Normalized to the unit of kB
        dmidecode_memsize *= 1000

        # Fail, if the RAM to have less actual capacity then advertised capacity.
        if dmidecode_memsize > meminfo_memtotal:
            self.wpl_raiseException("Failure while execute: {}, the actual memory capacity ({} kB) is less then SMBIOS reported capacity ({} kB).".format(
                cmd_meminfo_dmidecode, meminfo_memtotal, dmidecode_memsize))
        else:
            self.wpl_log_success('%s is PASSED\n' %cmd_meminfo_dmidecode)


#######################################################################################################################
# Function Name: backup_eeprom_cfg
# Date         : July 22th 2020
# Author       : Yang, Xuecun <yxcun@celestica.com>
#
# Procedure Revision Details:
#   Version : 1.0  - Initial Draft  - by Yang, Xuecun <yxcun@celestica.com>
#######################################################################################################################
    def backup_eeprom_cfg(self, var_cfg_out, var_cfg_bak, var_toolName, var_paths):
        self.wpl_log_debug('Entering procedure backup_eeprom_cfg with args : %s' %(str(locals())))

        var_keywords_pattern = cel_bmc_eeprom_tool_d_pattern
        var_pass_pattern = ""
        for path in var_paths:
            var_option = " -d;" + " cp {0} {1} || echo 'backup {2}/{0} failed'".format(var_cfg_out, var_cfg_bak, path)
            self.verify_bmc_diag_tool_simple_dict(var_toolName, var_option, var_keywords_pattern, var_pass_pattern, path)



#######################################################################################################################
# Function Name: restore_eeprom_cfg
# Date         : July 22th 2020
# Author       : Yang, Xuecun <yxcun@celestica.com>
#
# Procedure Revision Details:
#   Version : 1.0  - Initial Draft  - by Yang, Xuecun <yxcun@celestica.com>
#######################################################################################################################
    def restore_eeprom_cfg(self, var_cfg, var_cfg_out, var_cfg_bak, var_toolName, var_paths):
        self.wpl_log_debug('Entering procedure restore_eeprom_cfg with args : %s' %(str(locals())))

        mode = openbmc_mode
        restore_cmd = "cp {0} {1} ".format(var_cfg_bak,var_cfg)
        restore_cmd += " && {0} -w && {0} -u && {0} -d ".format(var_toolName)
        restore_cmd += " && rm {0} {1} || echo 'Error: restore scm EEPROM configration failed'".format(var_cfg_out, var_cfg_bak)
        patterns = cel_bmc_eeprom_tool_d_pattern
        remark = "restore scm eeprom"
        for path in var_paths:
            remark = "restore {} eeprom".format(path)
            self.execute_check_cmd(restore_cmd, mode, patterns, path=path, remark=remark)


#######################################################################################################################
# Function Name: check_nvme_smart_tool_and_log
# Date         : July 27th 2020
# Author       : Yang, Xuecun <yxcun@celestica.com>
#
# Procedure Revision Details:
#   Version : 1.0  - Initial Draft  - by Yang, Xuecun <yxcun@celestica.com>
#######################################################################################################################
    def check_nvme_smart_tool_and_log(self):
        self.wpl_log_debug('Entering procedure check_nvme_smart_tool_and_log with args : %s' %(str(locals())))

        mode = centos_mode
        cmd_smart = "./{}  -a /dev/nvme0n1 ;  nvme smart-log /dev/nvme0n1".format(usb_smarttool)
        cmd_nvme_i = "./{} -i 2>&1 ".format(cel_nvme_help_array["bin_tool"])

        self.wpl_execute("cd " + DIAG_UTIL_TOOL_PATH, mode=mode)
        output_smart = self.wpl_execute(cmd_smart, mode=mode)

        self.wpl_execute("cd " + DIAG_TOOL_PATH, mode=mode)
        output_nvme_i = self.wpl_execute(cmd_nvme_i, mode=mode)

        result_smart = parserDIAGLibs.PARSE_pattern_value(output_smart, cel_nvme_i_array, patterns_is_dict=False)
        result_nvme_i = parserDIAGLibs.PARSE_pattern_value(output_nvme_i, cel_nvme_i_array, patterns_is_dict=False)

        if result_smart and result_nvme_i and result_smart == result_nvme_i:
            self.wpl_log_success("check_nvme_smart_tool_and_log is successful.")
        else:
            self.wpl_raiseException("check {} -a /dev/nvme0n1".format(usb_smarttool))


#######################################################################################################################
# Function Name: check_nvme_test_file_is_removed
# Date         : July 27th 2020
# Author       : Yang, Xuecun <yxcun@celestica.com>
#
# Procedure Revision Details:
#   Version : 1.0  - Initial Draft  - by Yang, Xuecun <yxcun@celestica.com>
#######################################################################################################################
    def check_nvme_test_file_is_removed(self):
        self.wpl_log_debug('Entering procedure check_nvme_test_file_is_removed with args : %s' %(str(locals())))

        mode = centos_mode
        cmd = "find /mnt -maxdepth 1 -mmin -10 -type f |wc -l"
        patterns = "^0$"
        remark = "check nvme SSDs smart info"

        self.execute_check_cmd(cmd, mode, patterns, path=DIAG_TOOL_PATH, remark=remark)


#######################################################################################################################
# Function Name: compare_bmc_cpu_info
# Date         : July 27th 2020
# Author       : Yang, Xuecun <yxcun@celestica.com>
#
# Procedure Revision Details:
#   Version : 1.0  - Initial Draft  - by Yang, Xuecun <yxcun@celestica.com>
#######################################################################################################################
    def compare_bmc_cpu_info(self):
        self.wpl_log_debug('Entering procedure compare_bmc_cpu_info with args : %s' %(str(locals())))
        mode = openbmc_mode

        cmd_option_i = "./{} -i 2>&1".format(cel_bmc_cpu_help_array["bin_tool"])
        cmd_path_option_i = "cd {}&& {}".format(BMC_DIAG_TOOL_PATH, cmd_option_i)
        cmd_cpu_info = "cat /proc/cpuinfo"
        output_option_i = self.wpl_execute(cmd_option_i, mode=mode)
        output_cpu_info = self.wpl_execute(cmd_cpu_info, mode=mode)
        match_list_option_i = parserDIAGLibs.PARSE_pattern_value(output_option_i, bmc_cpu_info_pattern, patterns_is_dict=False)
        match_list_cpu_info = parserDIAGLibs.PARSE_pattern_value(output_cpu_info, bmc_cpu_info_pattern, patterns_is_dict=False)
        if match_list_option_i and match_list_cpu_info and match_list_option_i == match_list_cpu_info:
            self.wpl_log_success("Comparing cpu infomation is success.")
            return
        self.wpl_raiseException("CPU infomation is mismatch in /proc/cpuinfo and {}".format(cmd_option_i))


#######################################################################################################################
# Function Name: compare_bmc_cel_memory_info
# Date         : August 17th 2020
# Author       : Yang, Xuecun <yxcun@celestica.com>
#
# Procedure Revision Details:
#   Version : 1.0  - Initial Draft  - by Yang, Xuecun <yxcun@celestica.com>
#######################################################################################################################
    def compare_bmc_cel_memory_info(self,mem_cmd1=get_mem_i_cmd, mem_cmd2=get_meminfo_cmd, mem_pattern=mem_compare_pattern_dict,  path=BMC_DIAG_TOOL_PATH):
        self.wpl_log_debug('Entering procedure compare_bmc_cel_memory_info with args : %s' %(str(locals())))
        mode = openbmc_mode
        if path:
            mem_cmd1 = "cd {} && {} ".format(path, mem_cmd1)
        output1 = self.wpl_execute(mem_cmd1, mode=mode)
        output2 = self.wpl_execute(mem_cmd2, mode=mode)
        match_list1 = parserDIAGLibs.PARSE_pattern_value(output1, mem_pattern, patterns_is_dict=True)
        match_list2 = parserDIAGLibs.PARSE_pattern_value(output2, mem_pattern, patterns_is_dict=True)
        if match_list1 and match_list2 and match_list1 == match_list2:
            self.wpl_log_success("Comparing infomation is successfull.")
            return
        self.wpl_raiseException("Infomation is mismatch ")


#######################################################################################################################
# Function Name: check_bmc_top
# Date         : July 27th 2020
# Author       : Yang, Xuecun <yxcun@celestica.com>
#
# Procedure Revision Details:
#   Version : 1.0  - Initial Draft  - by Yang, Xuecun <yxcun@celestica.com>
#######################################################################################################################
    def check_bmc_top(self):
        self.wpl_log_debug('Entering procedure check_bmc_top with args : %s' %(str(locals())))
        mode = openbmc_mode

        cmd_option_a = "./{} -a 2>&1".format(cel_bmc_cpu_help_array["bin_tool"])
        cmd_path_option_a = "cd {}&& {}".format(BMC_DIAG_TOOL_PATH, cmd_option_a)
        cmd_top = "top -n 1"
        p_pass = "Mem.*?CPU.*?Load average:.*?PID"
        a_pass = "get_cpu_info.*?PASS.*?get_cpu_status.*?PASS.*?check_processor_number.*?PASS.*?check_cpu_model.*PASS"
        output_option_a = self.wpl_execute(cmd_option_a, mode=mode)
        output_top = self.wpl_execute(cmd_top, mode=mode)

        match_a = re.search(a_pass, output_option_a, re.M|re.S)
        match_top = re.search(p_pass, output_top, re.M|re.S)

        if not match_a:
            self.wpl_log_info("match_a is not match")
        elif not match_top:
            self.wpl_log_info("match_top is not match")
        if match_a and match_top:
            self.wpl_log_success("Comparing top info is success.")
            return
        self.wpl_raiseException("Infomation is mismatch in top and {}".format(cmd_option_a))

#######################################################################################################################
# Function Name: verify_cenos_diag_tool_simple_dict_fpga
# Date         : Jan 8th 2020
# Author       : Eric Zhang <zfzhang@celestica.com>
#
# Procedure Revision Details:
#   Version : 1.0  - Initial Draft  - by Eric Zhang <zfzhang@celestica.com>
#######################################################################################################################
    def verify_cenos_diag_tool_simple_dict_fpga(self, toolName, option, keywords_pattern=None, pass_pattern=None, path=BMC_DIAG_TOOL_PATH, is_negative_test=False, matchCount = -1):
        self.wpl_log_debug('Entering procedure verify_cenos_diag_tool_simple_dict_fpga with args : %s' %(str(locals())))
        passCount = 0
        new_option = option
        patternNum = len(keywords_pattern)
        self.wpl_log_debug('new_option = %s' % new_option)
        output = self.EXEC_centos_diag_tool_command(toolName, new_option, path)

        # To save / verify the Kernel, Cent OS and Diag OS versions
        if toolName == "cat" and option == "/proc/version":
            match = re.search(cat_proc_version_pattern[0], output)
            if match:
                self.centos_kernel_version_by_cat = match.group('version')
            else:
                self.centos_kernel_version_by_cat = "Not found"

        # To save / verify the I210 firmware version
        if str(toolName).__contains__("eeupdate64e") and option == "/NIC=2 /ADAPTERINFO":
            match = re.search(catch_i210_fw_version_pattern, output)
            if match:
                self.i210_fw_version_by_eeupdate64e = match.group('version')
            else:
                self.i210_fw_version_by_eeupdate64e = "Not found"

        self.wpl_log_debug('output = %s' % output)
        pass_p = []
        pattern_all = []
        for line in output.splitlines():
            line = line.strip()
            if 'FPGA' in line:
                line = line.replace('.0','.')
            for i in range(0, patternNum):
                p_pass = keywords_pattern[i] + pass_pattern
                pattern_all.append(p_pass)
                #self.wpl_log_debug('p_pass = %s' % p_pass)
                match = re.search(p_pass, line)
                if is_negative_test == True:
                    if not match:
                        passCount += 1
                else:
                    if match:
                        passCount += 1
                        pass_p.append(p_pass)

        mismatch_pattern = set(pattern_all)-set(pass_p) if not is_negative_test else set(pass_p)
        self.wpl_log_debug('passCount = %s' %passCount)
        self.wpl_log_debug('patternNum = %s' %patternNum)
        if passCount == patternNum or passCount == matchCount:
            self.wpl_log_success('verify_cenos_diag_tool_simple_dict test result for DIAG tool - %s is PASSED\n' %toolName)
        else:
            self.wpl_log_fail('Exiting verify_cenos_diag_tool_simple_dict with result FAIL, mismatch items: [{}]'.format(CommonLib.get_readable_strings(mismatch_pattern)))
            self.wpl_raiseException("Failure while testing DIAG tool '%s' with Option: '%s'" %(toolName, option))
            raise testFailed("verify_cenos_diag_tool_simple_dict fail")

#######################################################################################################################
# Function Name: verify_cenos_diag_tool_simple_dict
# Date         : July 9th 2020
# Author       : Abhisit S. <asang@celestica.com>
#
# Procedure Revision Details:
#   Version : 1.0  - Initial Draft  - by Abhisit S. <asang@celestica.com>
#######################################################################################################################
    def verify_cenos_diag_tool_simple_dict(self, toolName, option, keywords_pattern='none', pass_pattern='none', path=BMC_DIAG_TOOL_PATH, is_negative_test=False, matchCount = -1):
        self.wpl_log_debug('Entering procedure verify_cenos_diag_tool_simple_dict with args : %s' %(str(locals())))
        passCount = 0
        new_option = option
        time.sleep(3)
        devicename = os.environ.get("deviceName", "")
        if 'minipack2_dc' in devicename.lower() and toolName == './fpga' and option == 'ver':
            keywords_pattern = mp2_fpga_ver_pattern_dc
        patternNum = len(keywords_pattern)
        self.wpl_log_debug('new_option = %s' % new_option)
        output = self.EXEC_centos_diag_tool_command(toolName, new_option, path)

        # To save / verify the Kernel, Cent OS and Diag OS versions
        if toolName == "cat" and option == "/proc/version":
            match = re.search(cat_proc_version_pattern[0], output)
            if match:
                self.centos_kernel_version_by_cat = match.group('version')
            else:
                self.centos_kernel_version_by_cat = "Not found"

        # To save / verify the I210 firmware version
        if str(toolName).__contains__("eeupdate64e") and option == "/NIC=2 /ADAPTERINFO":
            match = re.search(catch_i210_fw_version_pattern, output)
            if match:
                self.i210_fw_version_by_eeupdate64e = match.group('version')
            else:
                self.i210_fw_version_by_eeupdate64e = "Not found"

        self.wpl_log_debug('output = %s' % output)
        pass_p = []
        pattern_all = []
        for line in output.splitlines():
            line = line.strip()
            for i in range(0, patternNum):
                p_pass = keywords_pattern[i] + pass_pattern
                pattern_all.append(p_pass)
                #self.wpl_log_debug('p_pass = %s' % p_pass)
                match = re.search(p_pass, line, re.I)
                if is_negative_test == True:
                    if not match:
                        passCount += 1
                else:
                    if match:
                        passCount += 1
                        pass_p.append(p_pass)

        mismatch_pattern = set(pattern_all)-set(pass_p) if not is_negative_test else set(pass_p)
        self.wpl_log_debug('passCount = %s' %passCount)
        self.wpl_log_debug('patternNum = %s' %patternNum)
        if passCount == patternNum or passCount == matchCount:
            self.wpl_log_success('verify_cenos_diag_tool_simple_dict test result for DIAG tool - %s is PASSED\n' %toolName)
        else:
            self.wpl_log_fail('Exiting verify_cenos_diag_tool_simple_dict with result FAIL, mismatch items: [{}]'.format(CommonLib.get_readable_strings(mismatch_pattern)))
            self.wpl_raiseException("Failure while testing DIAG tool '%s' with Option: '%s'" %(toolName, option))


#######################################################################################################################
# Function Name: verify_centos_run_command
# Date         : January 27th 2020
# Author       : Phawit P. <Phaphan@celestica.com>
#
# Procedure Revision Details:
#   Version : 1.0  - Initial Draft  - by Phawit P. <Phaphan@celestica.com>
#######################################################################################################################
    def verify_centos_run_command(self, command, options=None, pass_pattern=None, is_negative_test=False, check_all_line=False):
        self.wpl_log_debug('Entering procedure verify_centos_run_command with args : %s' %(str(locals())))

        get_pass_pattern = False if is_negative_test == False else True
        output = self.EXEC_centos_diag_tool_command(command, options)
        self.wpl_log_debug('**output=%s**' % output)

        pass_pattern = pass_pattern
        if command == 'find . -name' and options == ' disk.dump':
            if output.count('disk.dump') == 1:
                self.wpl_log_info('**check disk.dump file exist successful**')
            else:
                self.wpl_log_info('**check disk.dump file exist failed**')
                self.wpl_raiseException("Failure while testing command '%s' with Option: '%s'" % (command, options))

        match_dict = {}
        for line in output.splitlines():
            line = line.strip()
            for i in range(0, len(pass_pattern)):
                match = re.search(pass_pattern[i], line, re.I)
                if is_negative_test == True:
                    if match:
                        match_dict[i] = False
                else:
                    if match:
                        match_dict[i] = True
            if is_negative_test == False:
                if len(match_dict) == len(pass_pattern):
                    get_pass_pattern = True
                if not check_all_line:
                    if get_pass_pattern == True:
                          break

        for result in match_dict.values():
            if result == False:
                get_pass_pattern = False
                break

        if get_pass_pattern:
            self.wpl_log_success('verify_centos_run_command test result - %s is PASSED\n' %command)
        else:
            self.wpl_log_fail('Exiting verify_centos_run_command with result FAIL')
            self.wpl_raiseException("Failure while testing command '%s' with Option: '%s'" %(command, options))


#######################################################################################################################
# Function Name: verify_bmc_swtest_tool_simple_dict
# Date         : 14th May 2020
# Author       : TK NG<tikng@celestica.com>
#
# Procedure Revision Details:
#   Version : 1.0  - Initial Draft  - by TK NG<tikng@celestica.com>
#######################################################################################################################
    def verify_bmc_swtest_tool_simple_dict(self, toolName, option, keywords_pattern='none', pass_pattern='none', path=BMC_DIAG_TOOL_PATH):
        self.wpl_log_debug('Entering procedure verify_bmc_swtest_tool_simple_dict with args : %s' %(str(locals())))
        passCount = 0
        new_option = option
        patternNum = len(keywords_pattern)
        self.wpl_log_debug('new_option = %s' % new_option)
        output = self.EXEC_bmc_diag_tool_command(toolName, new_option, path)
        self.wpl_log_debug('output = %s' % output)

        ###---###
        # fix the issue of "PASS" string sometimes not appearing on the same line of the commmand output
        output1 = ''
        found = False
        self.wpl_flush()
        for line in output.splitlines():
            line = line.strip()
            if len(line) == 0:
                # blank line
                continue
            else:
                found = False
                str_passed = 'PASS'
                # search for pass pattern on the same line
                if type(keywords_pattern) == list:
                    match = False
                    match1 = False
                    for i in keywords_pattern:
                        match = re.search(i, line)
                        if match:
                            found = True
                            match1 = re.search(str_passed, line)
                            if match1:
                                # both pattern and pass string found
                                output1 += (line + '\r\n')
                                break
                    if match1:
                        continue
                else:
                    match = re.search(keywords_pattern, line)
                    if match:
                        found = True
                        match1 = re.search(str_passed, line)
                        if match1:
                            # both pattern and pass string found
                            output1 += (line + '\r\n')
                            continue

                if found == False:
                    if re.search(str_passed, line):
                        # add it to the previous line
                        output1 += ('| ' + str_passed + ' |' + '\r\n')
                    else:
                        # general comments, not command results
                        output1 += (line + '\r\n')
                else:
                    # pattern found but pass string not found
                    output1 += (line + '\r\n')

        output = output1
        self.wpl_log_debug("\r\nnew output=[\r\n%s\r\n]" %output)
        ###---###

        for line in output.splitlines():
            line = line.strip()
            for i in range(0, patternNum):
                p_pass = keywords_pattern[i] + pass_pattern
                #self.wpl_log_debug('p_pass = %s' % p_pass)
                match = re.search(p_pass, line)
                if match:
                    passCount += 1
        self.wpl_log_debug('passCount = %s' %passCount)
        self.wpl_log_debug('patternNum = %s' %patternNum)
        if passCount == patternNum:
            self.wpl_log_success('verify_bmc_swtest_tool_simple_dict test result for DIAG tool - %s is PASSED\n' %toolName)
        else:
            self.wpl_log_fail('Exiting verify_bmc_swtest_tool_simple_dict with result FAIL')
            self.wpl_raiseException("Failure while testing DIAG tool '%s' with Option: '%s'" %(toolName, option))


#######################################################################################################################
# Function Name: read_bmc_reg_byte
# Date         : February 27th 2020
# Author       : Phawit P. <Phaphan@celestica.com>
#
# Procedure Revision Details:
#   Version : 1.0  - Initial Draft  - by Phawit P. <Phaphan@celestica.com>
#######################################################################################################################
    def read_bmc_reg_byte(self, toolName, option):
        val_str = ''
        self.wpl_log_debug('Entering procedure read_bmc_reg_byte with args : %s' %(str(locals())))
        p1 = '(0x[0-9a-fA-F]{1,2})'
        output = self.EXEC_bmc_diag_tool_command(toolName, option)
        for line in output.splitlines():
            line = line.strip()
            #self.wpl_log_debug('line = %s'%(line))
            match = re.search(p1,line)
            if match:
                match1 = re.search(toolName,line)
                if match1:
                    continue
                else:
                    val_str = line
                    break
        return val_str

#######################################################################################################################
# Function Name: check_high_power_mode_OBO_status
# Date         : Oct. 1th 2020
# Author       : Eric Zhang <zfzhang@celestica.com>
#
# Procedure Revision Details:
#   Version : 1.0  - Initial Draft  - by Eric Zhang <zfzhang@celestica.com>
#######################################################################################################################
    def check_high_power_mode_OBO_status(self, toolName, option, path = None):
        self.wpl_log_debug('Entering procedure check_high_power_mode_OBO_status with args : %s' % (str(locals())))
        if path:
            cmd = 'cd ' + path
            self.wpl_transmit(cmd)

        cmd = toolName + ' ' + option
        output = self.wpl_execute_cmd(cmd, timeout=600)

#######################################################################################################################
# Function Name: verify_device_write_read
# Date         : February 27th 2020
# Author       : Phawit P. <Phaphan@celestica.com>
#
# Procedure Revision Details:
#   Version : 1.0  - Initial Draft  - by Phawit P. <Phaphan@celestica.com>
#######################################################################################################################
    def verify_device_write_read(self, toolName, dev, address, data):
        self.wpl_log_debug('Entering procedure verify_device_write_read with args : %s' %(str(locals())))
        option_read = '-r -c ' + dev + ' -s ' + address
        self.wpl_log_debug('option_read = %s' % option_read)
        old_read = self.read_bmc_reg_byte(toolName, option_read)

        option_write = '-w -c ' + dev + ' -s ' + address + ' -d ' + data
        self.wpl_log_debug('option_write = %s' % option_write)
        self.EXEC_bmc_diag_tool_command(toolName, option_write)

        new_read = self.read_bmc_reg_byte(toolName, option_read)

        self.wpl_log_debug('old_read = %s' % old_read)
        self.wpl_log_debug('new_read = %s' % new_read)
        if new_read == data or address:
            self.wpl_log_success('verify_device_write_read test result for DIAG tool - %s is PASSED\n' %toolName)
        else:
            self.wpl_log_fail('Exiting verify_device_write_read with result FAIL')
            self.wpl_raiseException("Failure while testing DIAG tool '%s'" %(toolName))


#######################################################################################################################
# Function Name: get_bmc_version
# Date         : 14th May 2020
# Author       : TK NG<tikng@celestica.com>
#
# Procedure Revision Details:
#   Version : 1.0  - Initial Draft  - by TK NG<tikng@celestica.com>
#######################################################################################################################
    def get_current_bmc_version(self, is_minipack2=False, platform='wedge400c'):
        self.wpl_log_debug('Entering procedure get_current_bmc_version with args : %s' %(str(locals())))
        current_bmc_version=''
        p1 = 'OpenBMC Release'
        cmd = 'cat /etc/issue'
        output = self.wpl_execute(cmd, mode="openbmc")
        for line in output.splitlines():
            line = line.strip()
            match = re.search(p1,line)
            if match:
                if is_minipack2:
                    current_bmc_version = line
                    return current_bmc_version
                else:
                    current_bmc_version = self.extract_fw_version(line, platform)
                    self.wpl_log_debug('Current BMC firmware version: %s\n' %current_bmc_version)
                    return current_bmc_version

        self.wpl_raiseException("ERR_01_001_01: Failed to get current BMC version")


#######################################################################################################################
# Function Name: check_bmc_region
# Date         : 14th May 2020
# Author       : TK NG<tikng@celestica.com>
#
# Procedure Revision Details:
#   Version : 1.0  - Initial Draft  - by TK NG<tikng@celestica.com>
#######################################################################################################################
    def check_bmc_region(self, region, checkTool, toolOption):
        self.wpl_log_debug('Entering procedure check_bmc_region with args : %s' %(str(locals())))
        cmd = (SPI_UTIL_PATH + checkTool + ' ' + toolOption)
        output = self.wpl_execute(cmd, mode='openbmc')
        passCount = 0
        for line in output.splitlines():
            line = line.strip()
            match = re.search(region,line)
            if match:
                passCount = 1

        if passCount != 0:
            self.wpl_log_success("Successfully check_bmc_region: %s" %region)
        else:
            self.wpl_raiseException("Failed check_bmc_region. %s region not found." %region)


#######################################################################################################################
# Function Name: flash_fw_image
# Date         : 14th May 2020
# Author       : TK NG<tikng@celestica.com>
#
# Procedure Revision Details:
#   Version : 1.0  - Initial Draft  - by  TK NG<tikng@celestica.com>
#######################################################################################################################
    def flash_fw_image(self, toolName, img_path, bmc_image, flash_device):
        self.wpl_log_debug('Entering procedure flash_fw_image with args : %s' %(str(locals())))
        passCount=0
        cmd = toolName + ' -v ' + img_path + bmc_image + ' ' + flash_device
        self.wpl_log_debug('command = %s' % cmd)
        self.wpl_flush()
        output = self.wpl_execute(cmd, mode="openbmc", timeout=600)
        for line in output.splitlines():
            line = line.strip()
            # e.g. Verifying kb: 21337/21337 (100%)
            match = re.search(r'^Verifying\skb:\s[\d+,\/]+\s[\(,100%,\)]+', line)
            if match:
                passCount += 1
        if passCount:
            self.wpl_log_success("Successfully used %s to flash BMC image: \'%s\'"% (toolName, bmc_image))
        else:
            self.wpl_raiseException("ERR_01_001_02: Failed using %s to flash BMC image \'%s\'"% (toolName, bmc_image))


#######################################################################################################################
# Function Name: flash_update_and_verify_bmc
# Date         : 14th May 2020
# Author       : TK NG<tikng@celestica.com>
#
# Procedure Revision Details:
#   Version : 1.0  - Initial Draft  - by TK NG<tikng@celestica.com>
#######################################################################################################################
    def flash_update_and_verify_bmc(self, toolName, img_path, downgrade_bmc_image, upgrade_bmc_image, bmc_downgrade_ver, bmc_upgrade_ver, flash_device):
        self.wpl_log_debug('Entering procedure flash_update_and_verify_bmc with args : %s' %(str(locals())))
        update_bmc_image = ''
        found = False
        upgrade_bmc_flag = False
        upper_bmc_major_ver = 0
        upper_bmc_minor_ver = 0
        update_bmc_version = bmc_upgrade_ver
        # extract bmc image version
        upper_bmc_version = self.extract_fw_version(update_bmc_version)
        slist1 = upper_bmc_version.split('.')
        upper_bmc_major_ver = int(slist1[0])
        upper_bmc_minor_ver = int(slist1[1])

        current_bmc_version = self.get_current_bmc_version()
        if current_bmc_version is None:
            self.wpl_raiseException("Failed flash_update_and_verify_bmc")
        else:
            # check whether to upgrade or downgrade BMC
            slist2 = current_bmc_version.split('.')
            cur_bmc_major_ver = int(slist2[0])
            cur_bmc_minor_ver = int(slist2[1])

            if cur_bmc_major_ver < upper_bmc_major_ver:
                # need to perform upgrade
                update_bmc_image = upgrade_bmc_image
                upgrade_bmc_flag = True
            elif cur_bmc_major_ver > upper_bmc_major_ver:
                # need to perform downgrade
                update_bmc_image = downgrade_bmc_image
                upgrade_bmc_flag = False
            else:
                if cur_bmc_minor_ver < upper_bmc_minor_ver:
                    # need to perform upgrade
                    update_bmc_image = upgrade_bmc_image
                    upgrade_bmc_flag = True
                else:
                    # need to perform downgrade
                    update_bmc_image = downgrade_bmc_image
                    upgrade_bmc_flag = False

            if upgrade_bmc_flag == True:
                self.wpl_log_debug('Performing BMC firmware upgrade to %s...\n' %update_bmc_image)
            else:
                self.wpl_log_debug('Performing BMC firmware downgrade to %s...\n' %update_bmc_image)

            self.flash_fw_image(toolName, img_path, update_bmc_image, flash_device)

            if upgrade_bmc_flag == True:
                self.bmc_version = bmc_upgrade_ver
                self.wpl_log_success('Successfully flash upgraded BMC firmware using DIAG tool - %s\n' %toolName)
            else:
                self.bmc_version = bmc_downgrade_ver
                self.wpl_log_success('Successfully flash downgraded BMC firmware using DIAG tool - %s\n' %toolName)

            # verify bmc fw version after reboot
            self.wpl_log_debug('Reboot to verify BMC firmware version...\n')
            CommonLib.reboot("openbmc")
            self.switch_to_openbmc_and_check_tool()
            self.switch_and_check_bmc_by_diag_command(diag_bmc_boot_bin, "master")
            if upgrade_bmc_flag == True:
                self.check_bmc_version(bmc_upgrade_ver)
            else:
                self.check_bmc_version(bmc_downgrade_ver)

            self.wpl_log_success('Successfully flash_update_and_verify_bmc.\n')


#######################################################################################################################
# Function Name: set_and_verify_cpld_register
# Date         : 14th May 2020
# Author       : TK NG<tikng@celestica.com>
#
# Procedure Revision Details:
#   Version : 1.0  - Initial Draft  - by TK NG<tikng@celestica.com>
#######################################################################################################################
    def set_and_verify_cpld_register(self, toolName, module, set_reg, set_value, toolPath):
        self.wpl_log_debug('Entering procedure set_and_verify_cpld_register with args : %s' %(str(locals())))

        self.execute_cpld_set_reg_command(toolName, module, set_reg, set_value, "set_and_verify_cpld_register", toolPath)


#######################################################################################################################
# Function Name: get_current_bios_version
# Date         : 14th May 2020
# Author       : TK NG<tikng@celestica.com>
#
# Procedure Revision Details:
#   Version : 1.0  - Initial Draft  - by TK NG<tikng@celestica.com>
#######################################################################################################################
    def get_current_bios_version(self, toolName, dev, option, tool_path):
        self.wpl_log_debug('Entering procedure get_current_bios_version with args : %s' %(str(locals())))
        cmd = tool_path + toolName + ' ' + dev + ' ' + option
        output = self.wpl_execute(cmd, mode="openbmc")

        search_string = 'BIOS Version:'
        current_bios_version = self.get_fw_version(search_string, output)
        if current_bios_version != '0':
            self.wpl_log_debug('Current bios version: %s\n' %current_bios_version)
            return current_bios_version
        else:
            self.wpl_raiseException("ERR_01_001_01: Failed to get current BIOS version")


#######################################################################################################################
# Function Name: get_fw_version
# Date         : 14th May 2020
# Author       : TK NG<tikng@celestica.com>
#
# Procedure Revision Details:
#   Version : 1.0  - Initial Draft  - by TK NG<tikng@celestica.com>
#######################################################################################################################
    def get_fw_version(self, search_str, fw_ver_str):
        self.wpl_log_debug('Entering procedure get_fw_version with args : %s' %(str(locals())))
        # fw_string: fw_version
        for line in fw_ver_str.splitlines():
            line = line.strip()
            match = re.search(search_str,line)
            if match:
                slist = line.split(':')
                fw_version = str(slist[1])
                fw_version = fw_version.strip()
                return fw_version

        # not found
        return '0'


#######################################################################################################################
# Function Name: check_current_bmc_version
# Date         : 14th May 2020
# Author       : TK NG<tikng@celestica.com>
#
# Procedure Revision Details:
#   Version : 1.0  - Initial Draft  - by TK NG<tikng@celestica.com>
#######################################################################################################################
    def check_current_bmc_version(self, toolName, option, is_minipack2=False, platform='wedge400'):
        self.wpl_log_debug('Entering procedure check_current_bmc_version with args : %s' %(str(locals())))

        current_bmc_version = self.get_current_bmc_version(is_minipack2, platform)
        if current_bmc_version is None:
            self.wpl_raiseException("Failed get_current_bmc_version")
        else:
            self.wpl_log_info("check_current_bmc_version:{}".format(current_bmc_version))
            #self.wpl_log_success('check_current_bmc_version test result is PASS.\n')
           # return

        #match_string = toolName + ' ' + platform + '-v' + current_bmc_version
        cmd = 'cat /etc/issue'
        count = 0
        output = self.wpl_execute(cmd,mode=openbmc_mode, timeout=600)
        for line in output.splitlines():
            line = line.strip()
            #match = re.search(match_string,line)
            if current_bmc_version in line:
                count+=1
            
        if count:
            self.wpl_log_success('check_current_bmc_version test result is PASS.\n')
        else:
            self.wpl_raiseException("Failed check_current_bmc_version.")
       

#######################################################################################################################
# Function Name: extract_fw_version
# Date         : 14th May 2020
# Author       : TK NG<tikng@celestica.com>
#
# Procedure Revision Details:
#   Version : 1.0  - Initial Draft  - by TK NG<tikng@celestica.com>
#######################################################################################################################
    def extract_fw_version(self, fw_version_str, platform='wedge400'):
        self.wpl_log_debug('Entering procedure extract_fw_version with args : %s' %(str(locals())))

        match = re.search(platform, fw_version_str)
        found = False
        if match:
            found = True

        if found == False:
             self.wpl_raiseException("Failed extract_fw_version. Version string not found.")
        else:
            self.wpl_log_debug('fw_version_str:**{}**'.format(fw_version_str))
            sw_str = fw_version_str.split(platform)[1]
            if sw_str.startswith("-v") or sw_str.startswith("_v"):
                fw_version = sw_str.lstrip("-v|_v")
            else:
                fw_version = sw_str.rstrip("-dirty").lstrip("-")
            return fw_version


#######################################################################################################################
# Function Name: verify_bmc_diag_installed
# Date         : 8th August 2020
# Author       : hemin@celestica.com>
#
# Procedure Revision Details:
#   Version : 1.0  - Initial Draft  - by hemin<hemin@celestica.com>
#######################################################################################################################
    def verify_bmc_diag_installed(self, toolName, option, pass_pattern, path):
        self.wpl_log_debug('Entering procedure verify_bmc_diag_installed with args : %s' %(str(locals())))
        p_len = len(pass_pattern)
        passCount = 0
        cmd_str = 'cd' + ' ' + path
        self.wpl_transmit(cmd_str)
        cmd = toolName + ' ' + option
        output = self.wpl_execute(cmd, mode=openbmc_mode, timeout=600)
        for i in range(p_len):
            if pass_pattern[i] in output:
                passCount += 1
            else:
                self.wpl_log_debug('%s does not exist' % pass_pattern[i])
        if passCount == 6 or passCount == 5 or passCount == 4:
            self.wpl_log_success('verify_bmc_diag_installed test result: PASS')
        else:
            self.wpl_log_fail('Exiting verify_bmc_diag_installed with result FAIL')
            self.wpl_raiseException("Failure while testing the tool '%s' with Option: '%s'" % (toolName, option))


#######################################################################################################################
# Function Name: verify_option_diag_tool_simple_dict
# Date         : 14th May 2020
# Author       : TK NG<tikng@celestica.com>
#
# Procedure Revision Details:
#   Version : 1.0  - Initial Draft  - by TK NG<tikng@celestica.com>
#######################################################################################################################
    def verify_option_bmc_tool_system_dict(self, inputArray, toolName, dev, option, toolPath=FW_UTIL_PATH, key='None'):
        self.wpl_log_debug('Entering procedure verify_option_bmc_tool_system_dict with args : %s' %(str(locals())))
        cmd = 'cd ' + toolPath
        self.wpl_getPrompt("centos", 600)
        self.wpl_transmit(cmd)
        optionStr = (dev + " " + option)
        errCount = 0
        output = self.EXEC_bmc_system_tool_command(toolName, optionStr, toolPath)
        self.wpl_log_debug(output)
        parsedOutput = parserDIAGLibs.PARSE_FW_Version(output)
        if key != 'None':
            # need to upgrade/downgrade this FW later
            parsedOutput[key] = inputArray[key]

        errCount = CommonLib.compare_input_dict_to_parsed(parsedOutput, inputArray)
        if errCount:
            self.wpl_raiseException("Failed while testing DIAG tool '%s' with Option: '%s'" %(toolName, optionStr))
        else:
            self.wpl_log_success('verify_option_bmc_tool_system_dict test result: PASS')


#######################################################################################################################
# Function Name: EXEC_bmc_system_tool_command
# Date         : 14th May 2020
# Author       : TK NG<tikng@celestica.com
#
# Procedure Revision Details:
#   Version : 1.0  - Initial Draft  - by TK NG<tikng@celestica.com
#######################################################################################################################
    def EXEC_bmc_system_tool_command(self, toolName, option, toolPath=FW_UTIL_PATH):
        self.wpl_log_debug('Entering procedure EXEC_bmc_system_tool_command with args : %s' %(str(locals())))
        cmd = ('cd ' + toolPath)
        self.wpl_log_debug("command = [%s]" %(cmd))
        self.wpl_getPrompt("openbmc", 600)
        self.wpl_transmit(cmd)

        cmd = './' + toolName + ' ' + option
        self.wpl_log_debug("command = [%s]" %(cmd))
        return self.wpl_execute(cmd, mode=openbmc_mode, timeout=600)


#######################################################################################################################
# Function Name: set_and_verify_i2c_register
# Date         : 14th May 2020
# Author       : TK NG<tikng@celestica.com>
#
# Procedure Revision Details:
#   Version : 1.0  - Initial Draft  - by TK NG<tikng@celestica.com>
#######################################################################################################################
    def set_and_verify_i2c_register(self, setToolName, verifyToolName, option, bus, chip_addr, data_addr, value):
        self.wpl_log_debug('Entering procedure set_and_verify_i2c_register with args : %s' %(str(locals())))

        self.wpl_getPrompt("openbmc", 600)
        # write register data: i2cset -f -y 12 0x3e 0x20 0x00
        cmd = setToolName + ' ' + option  + ' ' + bus + ' ' + chip_addr + ' ' + data_addr + ' ' + value
        self.wpl_log_debug("command = [%s]" %(cmd))
        self.wpl_execute(cmd, mode=openbmc_mode, timeout=600)

        # read register data: i2cget -f -y 12 0x3e 0x20
        cmd1 = verifyToolName + ' ' + option  + ' ' + bus + ' ' + chip_addr + ' ' + data_addr
        self.wpl_log_debug("command = [%s]" %(cmd1))
        passCount = 0
        output = self.wpl_execute(cmd1, mode=openbmc_mode, timeout=600)

        # verify register data
        for line in output.splitlines():
            line = line.strip()
            if line == value:
                passCount = 1
                break

        if passCount:
            self.wpl_log_success("Successfully set_and_verify_i2c_register.")
        else:
            self.wpl_raiseException("Failure in set_and_verify_i2c_register.")


#######################################################################################################################
# Function Name: upgrade_downgrade_bios
# Date         : 14th May 2020
# Author       : TK NG<tikng@celestica.com>
#
# Procedure Revision Details:
#   Version : 1.0  - Initial Draft  - by TK NG<tikng@celestica.com>
#######################################################################################################################
    def flash_update_master_bios(self, toolName, fru, opt, dev, check_pattern, downgrade_image, upgrade_image, upgrade_ver, downgrade_ver, img_path, tool_path):
        self.wpl_log_debug('Entering procedure flash_update_master_bios with args : %s' %(str(locals())))
        update_bios_image = ''
        found = False
        upgrade_bios_flag = False
        upper_bios_major_ver = 0
        upper_bios_minor_ver = 0
        update_bios_version = upgrade_ver

        # extract bios version
        upper_bios_version = self.extract_bios_fw_version(update_bios_version)
        upper_str = str(upper_bios_version[0:2])
        upper_major_str = ("0x" + str(upper_str))
        upper_str1 = str(upper_bios_version[2:4])
        upper_minor_str = ("0x" + str(upper_str1))

        upper_bios_major_ver = int(upper_major_str, 16)
        upper_bios_minor_ver = int(upper_minor_str, 16)

        self.wpl_log_debug('upper_bios_major_ver=[%s]' %upper_bios_major_ver)
        self.wpl_log_debug('upper_bios_minor_ver=[%s]' %upper_bios_minor_ver)

        current_bios_version = self.get_current_bios_version(fw_util_tool, "scm", "--version", FW_UTIL_PATH)
        if current_bios_version == '0':
            self.wpl_raiseException("Failed flash_update_master_bios")
        else:
            # check whether to upgrade or downgrade BIOS
            tmp_bios_version =  self.extract_bios_fw_version(current_bios_version)
            bios_str = str(tmp_bios_version[0:2])
            cur_major_str = ("0x" + str(bios_str))
            bios_str1 = str(tmp_bios_version[2:4])
            cur_minor_str = ("0x" + str(bios_str1))

            cur_bios_major_ver = int(cur_major_str, 16)
            cur_bios_minor_ver = int(cur_minor_str, 16)

            self.wpl_log_debug('cur_bios_major_ver=[%s]' %cur_bios_major_ver)
            self.wpl_log_debug('cur_bios_minor_ver=[%s]' %cur_bios_minor_ver)

            if cur_bios_major_ver < upper_bios_major_ver:
                # need to perform upgrade
                update_bios_image = upgrade_image
                upgrade_bios_flag = True
            elif cur_bios_major_ver > upper_bios_major_ver:
                # need to perform downgrade
                update_bios_image = downgrade_image
                upgrade_bios_flag = False
            else:
                if cur_bios_minor_ver < upper_bios_minor_ver:
                    # need to perform upgrade
                    update_bios_image = upgrade_image
                    upgrade_bios_flag = True
                else:
                    # need to perform downgrade
                    update_bios_image = downgrade_image
                    upgrade_bios_flag = False

            if upgrade_bios_flag == True:
                self.wpl_log_debug('Performing BIOS firmware upgrade to %s...\n' %update_bios_image)
            else:
                self.wpl_log_debug('Performing BIOS firmware downgrade to %s...\n' %update_bios_image)

            # perform BIOS upgrade/downgrade
            self.fw_util_exec(toolName, fru, opt, dev, update_bios_image, check_pattern, img_path, tool_path, "openbmc")

            if upgrade_bios_flag == True:
                self.bios_version = upgrade_ver
                self.wpl_log_success('Successfully flash upgraded BIOS firmware using DIAG tool - %s\n' %toolName)
            else:
                self.bios_version = downgrade_ver
                self.wpl_log_success('Successfully flash downgraded BIOS firmware using DIAG tool - %s\n' %toolName)


#######################################################################################################################
# Function Name: switch_and_verify_master_bios_version
# Date         : 14th May 2020
# Author       : TK NG<tikng@celestica.com>
#
# Procedure Revision Details:
#   Version : 1.0  - Initial Draft  - by TK NG<tikng@celestica.com>
#######################################################################################################################
    def switch_and_verify_master_bios_version(self):
        self.wpl_log_debug('Entering procedure switch_and_verify_master_bios_version with args : %s' %(str(locals())))

        if self.bios_version == '0':
            self.wpl_raiseException("Failed switch_and_verify_master_bios_version, BIOS update version not found.")
        else:
            self.wpl_log_debug('waiting for system to bootup...\n')
            CommonLib.switch_to_centos()
            self.switch_to_openbmc_and_check_tool()
            self.switch_and_check_bmc_by_diag_command(diag_bmc_boot_bin, "master")
            self.verify_bios_version(self.bios_version)
            self.wpl_log_success('Successfully switch_and_verify_master_bios_version.\n')


#######################################################################################################################
# Function Name: verify_bios_version
# Date         : 14th May 2020
# Author       : TK NG<tikng@celestica.com>
#
# Procedure Revision Details:
#   Version : 1.0  - Initial Draft  - by TK NG<tikng@celestica.com>
#######################################################################################################################
    def verify_bios_version(self, bios_version):
        self.wpl_log_debug('Entering procedure verify_bios_version with args : %s' %(str(locals())))
        current_bios_version = self.get_current_bios_version(fw_util_tool, "scm", "--version", FW_UTIL_PATH)

        if current_bios_version == '0':
            self.wpl_raiseException("ERR_01_001_02: Failed checking BIOS version")

        if current_bios_version == bios_version:
            self.wpl_log_success("Successfully checked BIOS version: \'%s\'"% current_bios_version)
        else:
            self.wpl_raiseException("ERR_01_001_02: Failed checking BIOS version")


#######################################################################################################################
# Function Name: extract_bios_fw_version
# Date         : 14th May 2020
# Author       : TK NG<tikng@celestica.com>
#
# Procedure Revision Details:
#   Version : 1.0  - Initial Draft  - by TK NG<tikng@celestica.com>
#######################################################################################################################
    def extract_bios_fw_version(self, fw_version_str):
        self.wpl_log_debug('Entering procedure extract_bios_fw_version with args : %s' %(str(locals())))
        # 'XG1_3A09'
        match = re.search('_', fw_version_str)
        if match:
            found = True

        if found == False:
             self.wpl_raiseException("Failed extract_bios_fw_version. Version string not found.")
        else:
            slist = fw_version_str.split('_')
            fw_version = str(slist[1])
            return fw_version


#######################################################################################################################
# Function Name: get_current_bic_version
# Date         : 14th May 2020
# Author       : TK NG<tikng@celestica.com>
#
# Procedure Revision Details:
#   Version : 1.0  - Initial Draft  - by TK NG<tikng@celestica.com>
#######################################################################################################################
    def get_current_bic_version(self, toolName, dev, option, tool_path):
        self.wpl_log_debug('Entering procedure get_current_bic_version with args : %s' %(str(locals())))
        cmd = tool_path + toolName + ' ' + dev + ' ' + option
        output = self.wpl_execute(cmd, mode="openbmc")

        search_string = 'Bridge-IC Version:'
        current_bios_version = self.get_fw_version(search_string, output)
        if current_bios_version != '0':
            self.wpl_log_debug('Current bic version: %s\n' %current_bios_version)
            return current_bios_version
        else:
            self.wpl_raiseException("ERR_01_001_01: Failed to get current BIC version")

    #######################################################################################################################
    # Function Name: verify_tool_simple_dict
    # Date         : 26th May 2020
    # Author       : Abhisit Sangjan <asang@celestica.com>
    #
    # Procedure Revision Details:
    # Version : 1.0  - Initial, supported openbmc & centos modes - by Abhisit Sangjan<asang@celestica.com>
    #######################################################################################################################
    def verify_tool_simple_dict(self, toolName, option, keywords_pattern='none', pass_pattern='none', mode='centos',
                                path=DIAG_TOOL_PATH):
        self.wpl_log_debug('Entering procedure verify_tool_simple_dict with args : %s' % (str(locals())))

        cmd = ('cd ' + path)
        self.wpl_log_debug("command = %s" % (cmd))
        self.wpl_getPrompt(mode, 600)
        self.wpl_transmit(cmd)

        passCount = 0
        new_option = option
        patternNum = len(keywords_pattern)
        self.wpl_log_debug('new_option = %s' % new_option)
        output = self.EXEC_diag_tool_command(toolName, new_option, "./", mode=mode)

        # To save / verify the Kernel, Cent OS and Diag OS versions
        if toolName == "cat" and option == "/etc/product/VERSION":
            match = re.search(catch_os_diag_version_pattern, output)
            if match:
                self.os_diag_version_by_cat = match.group('version')
            else:
                self.os_diag_version_by_cat = "Not found"

            match = re.search(catch_centos_version_pattern, output)
            if match:
                self.centos_version_by_cat = match.group('version')
            else:
                self.centos_version_by_cat = "Not found"
        if toolName == "cat" and option == "/etc/redhat-release":
            match = re.search(catch_etc_redhat_release_pattern, output)
            if match:
                self.centos_version_by_cat = match.group('version')
            else:
                self.centos_version_by_cat = "Not found"
        self.wpl_log_debug('output = %s' % output)
        for line in output.splitlines():
            line = line.strip()
            for i in range(0, patternNum):
                p_pass = keywords_pattern[i] + pass_pattern
                # self.wpl_log_debug('p_pass = %s' % p_pass)
                match = re.search(p_pass, line)
                if match:
                    passCount += 1
        self.wpl_log_debug('passCount = %s' % passCount)
        self.wpl_log_debug('patternNum = %s' % patternNum)
        if passCount == patternNum:
            self.wpl_log_success('verify_tool_simple_dict test result for the tool - %s is PASSED\n' % toolName)
        else:
            self.wpl_log_fail('Exiting verify_tool_simple_dict with result FAIL')
            self.wpl_raiseException("Failure while testing the tool '%s' with Option: '%s'" % (toolName, option))


#######################################################################################################################
# Function Name: verify_bmc_i2c_tool_simple_dict
# Date         : 14th May 2020
# Author       : TK NG<tikng@celestica.com>
#
# Procedure Revision Details:
#   Version : 1.0  - Initial Draft  - by TK NG<tikng@celestica.com>
#######################################################################################################################
    def verify_bmc_i2c_tool_simple_dict(self, toolName, option, keywords_pattern='none', pass_pattern='none', path=BMC_DIAG_TOOL_PATH):
        self.wpl_log_debug('Entering procedure verify_bmc_i2c_tool_simple_dict with args : %s' %(str(locals())))
        passCount = 0
        devicename = os.environ.get("deviceName", "")
        new_option = option
        patternNum = len(keywords_pattern)
        self.wpl_log_debug('new_option = %s' % new_option)
        if 'minipack2_dc' in devicename.lower():
            if 'minipack2_dc-04' in devicename.lower() or 'minipack2_dc-05' in devicename.lower():
                if (('pim3' in new_option) or ('pim4' in new_option) or ('pim5' in new_option) or ('pim6' in new_option)) and toolName == 'cel-i2c-test':
                    return
                if (('PIM_3' in new_option) or ('PIM_4' in new_option) or ('PIM_5' in new_option) or ('PIM_6' in new_option)):
                    return
            else:
                if (('pim3' in new_option) or ('pim4' in new_option) or ('pim5' in new_option)) and toolName == 'cel-i2c-test':
                    return
                if (('PIM_3' in new_option) or ('PIM_4' in new_option) or ('PIM_5' in new_option)):
                    return
        #if 'minipack2_rsp2-02' in devicename.lower() or 'minipack2_rsp2-03' in devicename.lower() or 'minipack2_rsp2-04' in devicename.lower():
            #if (('pim3' in new_option) or ('pim4' in new_option) or ('pim5' in new_option)) and toolName == 'cel-i2c-test':
                #return
        output = self.EXEC_bmc_diag_tool_command(toolName, new_option, path)
        self.wpl_log_debug('output = %s' % output)
        for line in output.splitlines():
            line = line.strip()
            devicename = os.environ.get("deviceName", "")
            if 'wedge400_' in devicename.lower():
                if 'SMB_OCP_CARD' in line:
                    self.wpl_log_info('skip OCP card check!!!')
                    continue
            for i in range(0, patternNum):
                p_pass = keywords_pattern[i]
                #self.wpl_log_debug('p_pass = %s' % p_pass)
                match = re.search(p_pass, line)
                if match:
                    if pass_pattern != 'none':
                        match1 = re.search(pass_pattern, line)
                        if match1:
                            passCount += 1
                        else:
                            self.wpl_log_fail('Exiting verify_bmc_i2c_tool_simple_dict with result FAIL')
                            self.wpl_raiseException("Failure while testing DIAG tool '%s' with Option: '%s'" %(toolName, option))
                    else:
                        passCount += 1
        self.wpl_log_debug('passCount = %s' % passCount)
        self.wpl_log_debug('patternNum = %s' % patternNum)
        if passCount:
            self.wpl_log_success('verify_bmc_i2c_tool_simple_dict test result for DIAG tool - %s is PASSED\n' %toolName)
        else:
            self.wpl_log_fail('Exiting verify_bmc_i2c_tool_simple_dict with result FAIL')
            self.wpl_raiseException("Failure while testing DIAG tool '%s' with Option: '%s'" %(toolName, option))


    #######################################################################################################################
    # Function Name: wedge_reboot_whole_system
    # Date         : 5th June 2020
    # Author       : Abhisit Sangjan <asang@celestica.com>
    #
    # Procedure Revision Details:
    # Version : 1.0  - Initial - by Abhisit Sangjan<asang@celestica.com>
    #######################################################################################################################
    def wedge_reboot_whole_system(self, mode='centos'):
        self.wpl_log_debug('Entering procedure wedge_reboot_whole_system with args : %s' % (str(locals())))
        self.wpl_transmit("wedge_power.sh reset -s")
        self.wpl_flush()
        kernel_bootup_msg = 'Starting kernel ...'
        output = self.wpl_receive(kernel_bootup_msg, timeout=1800)
        self.wpl_log_debug(output)
        self.wpl_getPrompt(mode, timeout=1800)
        time.sleep(5)


    #######################################################################################################################
    # Function Name: verify_the_free_mem_before_and_after_run_ddr_test_sh
    # Date         : 22th June 2020
    # Author       : Abhisit Sangjan <asang@celestica.com>
    #
    # Procedure Revision Details:
    # Version : 1.0  - Initial - by Abhisit Sangjan<asang@celestica.com>
    #######################################################################################################################
    def verify_the_free_mem_before_and_after_run_ddr_test_sh(self):
        self.wpl_log_debug('Entering procedure verify_the_free_mem_before_and_after_run_ddr_test_sh with args : %s' % (str(locals())))

        # Check the free memory before run DDR_test.sh
        output = self.EXEC_bmc_diag_tool_command('free', '', '/usr/bin')
        for line in output.splitlines():
            line = line.strip()
            match = re.search(r'^[ \t]*Mem:[ \t]+(\d+)[ \t]+(\d+)[ \t]+(\d+)[ \t]+(\d+)[ \t]+(\d+)[ \t]+(\d+)', line)
            if match:
                # Return the free memory
                free_mem_before = int(match.group(3))

                # The percent error range is assign here, now is +/- 3%
                free_mem_lower_of_fifty_percent = int(free_mem_before * 0.47)
                free_mem_upper_of_fifty_percent = int(free_mem_before * 0.53)

        self.wpl_log_debug("The free memory before run DDR_test.sh is " + str(free_mem_before))

        # Run the DDR_test.sh for 10s then check how much the memory used by the shell script?
        output = self.EXEC_bmc_diag_tool_command('./DDR_test.sh 300 50 DDR.log 2>&1 & sleep 10', '', '/mnt/data1/BMC_Diag/utility/stress')
        devicename = os.environ.get("deviceName","")
        #if 'wedge400c' in devicename.lower():
            #if CommonLib.read_until_regexp('timed out waiti', timeout=300):
                #self.wpl_getPrompt(openbmc_mode)
        # Check the free memory after run DDR_test.sh and wait for the DDR_test.sh to success
        output = self.EXEC_bmc_diag_tool_command('free && wait', '', '/usr/bin')
        for line in output.splitlines():
            line = line.strip()
            match = re.search(r'^[ \t]*Mem:[ \t]+(\d+)[ \t]+(\d+)[ \t]+(\d+)[ \t]+(\d+)[ \t]+(\d+)[ \t]+(\d+)', line)
            if match:
                # Return the free memory
                free_mem_after = int(match.group(3))

        self.wpl_log_debug("The free memory after run DDR_test.sh is " + str(free_mem_after))

        # The memory would be 50% and +/- 3% is accepted
       # if free_mem_after >= free_mem_upper_of_fifty_percent or free_mem_lower_of_fifty_percent >= free_mem_after:
        #    self.wpl_raiseException("Failure while testing the DDR_test.sh is take more or less than 50% (+/- 3%) of the free memory!")

        # Verify the DDR.log of DDR_test.sh
        var_toolName = "cat"
        var_option = "/mnt/data1/BMC_Diag/utility/stress/DDR.log"
        var_keywords_pattern = ddr_test_sh_pattern
        var_pass_pattern = ""
        var_path = "/bin"

        self.verify_bmc_diag_tool_simple_dict(var_toolName, var_option, var_keywords_pattern,
                                                        var_pass_pattern, var_path)


    #######################################################################################################################
    # Function Name: init_diag_test
    # Date         : 7th July 2020
    # Author       : Xiaoqiang Wang <xiaoqwa@celestica.com>
    #
    # Procedure Revision Details:
    # Version : 1.0  - Initial - by Xiaoqiang Wang <xiaoqwa@celestica.com>
    #######################################################################################################################
    def init_diag_test(self):
        self.wpl_log_debug('Entering procedure init_diag_test with args : %s' % (str(locals())))
        self.wpl_getPrompt(openbmc_mode)
        cmd = 'cd /mnt/data1/BMC_Diag/bin'
        self.wpl_transmit(cmd)
        devicename = os.environ.get("deviceName", "")
        if 'wedge400c' in devicename.lower() or 'wedge400' in devicename.lower():
            cmd = 'pem-util pem2 --get_pem_info'
            output = self.wpl_execute(cmd, mode=openbmc_mode, timeout=30)
            match = re.search('is not present', output)
            if match:
                self.wpl_log_info("This unit use PSU")
                cmd1 = "sensor-util psu2 |grep 'PSU2_IN_VOLT' |awk '{print$4}'"
                output1 = self.wpl_execute(cmd1, mode=openbmc_mode, timeout=30)
                p1 = r'^\d+'
                for line in output1.splitlines():
                    line = line.strip()
                    match1 = re.search(p1, line)
                    if match1:
                        volt_value = match1.group()
                        if float(volt_value) > 200:
                            self.wpl_log_info("This unit use AC PSU")
                            if 'rsp' in devicename.lower():
                                self.wpl_log_info("This machine is Respin AC unit")
                                cmd = './cel-diag-init -r'
                                self.wpl_transmit(cmd)
                            else:
                                cmd2 = './cel-diag-init -a'
                                self.wpl_transmit(cmd2)
                        else:
                            if 'dc' in devicename.lower():
                                self.wpl_log_info("This unit use a 48VDC PSU")
                                cmd3 = './cel-diag-init -c'
                                self.wpl_transmit(cmd3)
                            else:
                                self.wpl_log_info("This unit use DC PSU")
                                cmd4 = './cel-diag-init -d'
                                self.wpl_transmit(cmd4)
            else:
                self.wpl_log_info("This unit use PEM")
                if 'rsp' in devicename.lower():
                    self.wpl_log_info("This machine is Respin PEM unit")
                    cmd = './cel-diag-init -m'
                    self.wpl_transmit(cmd)
                else:
                    cmd = './cel-diag-init -p'
                    self.wpl_transmit(cmd)
        elif 'minipack2' in devicename.lower():
            if 'rsp' in devicename.lower():
                self.wpl_log_info("This unit is respin machine")
                cmd3 = './cel-diag-init -r'
                self.wpl_transmit(cmd3)
            else:
                cmd1 = "sensor-util psu3 |grep 'PSU3_IN_VOLT' |awk '{print$4}'"
                output1 = self.wpl_execute(cmd1, mode=openbmc_mode, timeout=30)
                p1 = r'^\d+'
                for line in output1.splitlines():
                    line = line.strip()
                    match1 = re.search(p1, line)
                    if match1:
                        volt_value = match1.group()
                        if float(volt_value) > 60:
                            self.wpl_log_info("This unit use AC PSU")
                            cmd2 = './cel-diag-init -a'
                            self.wpl_transmit(cmd2)
                        else:
                            self.wpl_log_info("This unit is DC machine.")
                            cmd = './cel-diag-init -c'
                            self.wpl_transmit(cmd)

        self.wpl_getPrompt(centos_mode)


    #######################################################################################################################
    # Function Name: compare_centos_version_diag_version_and_kernel_version
    # Date         : 14th July 2020
    # Author       : Abhisit Sangjan <asang@celestica.com>
    #
    # Procedure Revision Details:
    # Version : 1.0  - Initial - by Abhisit Sangjan <asang@celestica.com>
    #######################################################################################################################
    def compare_centos_version_diag_version_and_kernel_version(self):
        self.wpl_log_debug('Entering procedure init_diag_test with args : %s' % (str(locals())))

        if self.centos_kernel_version_by_cmd != self.centos_kernel_version_by_cat:
            self.wpl_log_fail('Exiting compare_centos_version_diag_version_and_kernel_version with result FAIL')
            self.wpl_raiseException("Failure while compare kernel version '%s' and '%s'" \
                % (self.centos_kernel_version_by_cmd, self.centos_kernel_version_by_cat))

        if self.os_diag_version_by_cmd != self.os_diag_version_by_cat:
            self.wpl_log_fail('Exiting compare_centos_version_diag_version_and_kernel_version with result FAIL')
            self.wpl_raiseException("Failure while compare diag version '%s' and '%s'" \
                % (self.os_diag_version_by_cmd, self.os_diag_version_by_cat))

        if self.centos_version_by_cmd != self.centos_version_by_cat:
            self.wpl_log_fail('Exiting compare_centos_version_diag_version_and_kernel_version with result FAIL')
            self.wpl_raiseException("Failure while compare Cent OS version '%s' and '%s'" \
                % (self.centos_version_by_cmd, self.centos_version_by_cat))


    #######################################################################################################################
    # Function Name: compare_i210_firmware_version
    # Date         : 14th July 2020
    # Author       : Abhisit Sangjan <asang@celestica.com>
    #
    # Procedure Revision Details:
    # Version : 1.0  - Initial - by Abhisit Sangjan <asang@celestica.com>
    #######################################################################################################################
    def compare_i210_firmware_version(self):
        self.wpl_log_debug('Entering procedure compare_i210_firmware_version with args : %s' % (str(locals())))

        if self.i210_fw_version_by_cel_version_test != self.i210_fw_version_by_eeupdate64e:
            self.wpl_log_fail('Exiting compare_i210_firmware_version with result FAIL')
            self.wpl_raiseException("Failure while compare I210 firmware version '%s' and '%s'" \
                % (self.i210_fw_version_by_cel_version_test, self.i210_fw_version_by_eeupdate64e))


    #######################################################################################################################
    # Function Name: compare_psu_info_diag_and_openbmc_tools
    # Date         : 24th July 2020
    # Author       : Abhisit Sangjan <asang@celestica.com>
    #
    # Procedure Revision Details:
    # Version : 1.0  - Initial - by Abhisit Sangjan <asang@celestica.com>
    #######################################################################################################################
    def compare_psu_info_diag_and_openbmc_tools(self):
        self.wpl_log_debug('Entering procedure compare_psu_info_diag_and_openbmc_tools with args : %s' % (str(locals())))

        for index, (diag, openbmc) in enumerate(zip(self._psu_diag, self._psu_openbmc)):
            if diag != openbmc:
                self.wpl_raiseException("Failure while compare '%s' with diag='%s' != 'openbmc=%s'" % (catch_psu_info_pattern[index], diag, openbmc))


################################################################################
# Function Name: check_cmd_output
# Date         : 26th July 2020
# Author       : James Shi <jameshi@celestica.com>
#
# Procedure Revision Details:
#   Version : 1.0  - Initial Draft  - by James Shi <jameshi@celestica.com>
################################################################################
    def check_cmd_output(self, cmd, p, string):
        log.debug('Entering procedure check_cmd_output with args : %s\n' %(str(locals())))
        err_count = 0
        output = self.wpl_execute(cmd)
        output = re.search(p, output)
        str_list_1 = output.group().splitlines()
        str_list = string.split("||")
        print(str_list_1)
        print(str_list)
        while '' in str_list_1:
            str_list_1.remove('')
        while '' in str_list:
            str_list.remove('')
        print(str_list_1)
        print(str_list)
        if str_list == str_list_1:
            log.success("Successfully check_cmd_output.")
        else:
            err_count += 1
        if err_count:
            log.fail("the output is not the same as defined")
            raise testFailed("check_cmd_output fail")


################################################################################
# Function Name: check_rtc_time
# Date         : 27th July 2020
# Author       : James Shi <jameshi@celestica.com>
#
# Procedure Revision Details:
#   Version : 1.0  - Initial Draft  - by James Shi <jameshi@celestica.com>
################################################################################
    def check_rtc_time(self, cmd1, cmd2, p1, p2):
        log.debug('Entering procedure check_rtc_time with args : %s\n' %(str(locals())))
        err_count = 0
        self.wpl_flush()
        output = self.wpl_execute(cmd1)
        output = re.search(p1, output)
        if not output:
            self.wpl_raiseException("Nof found the command %s and/or %s" % (cmd1, p1))

        str_list_1 = output.group().splitlines()
        str1 = "".join(str_list_1)
        log.info("%s is %s" %(cmd1,str1))
        output1 = self.wpl_execute(cmd2)
        res = re.search(p2, output1)
        if not res:
            self.wpl_raiseException("Nof found the command %s and/or %s" % (cmd2, p2))
        devicename = os.environ.get("deviceName", "")
        if 'wedge400_' in devicename.lower():
            yue = res.group(1)
            day = res.group(2)
            xh = res.group(3)
            nian = res.group(4)
            if yue == 'Jan':
                yue = '01'
            str2 = nian + '-' + '0' + day + '-' + yue + ' ' + xh
        else:
            str_list_2 = res.group().splitlines()
            str2 = "".join(str_list_2)
        log.info("hwclock time is %s" %str2)
        struct_time_2 = time.strptime(str2, "%Y-%m-%d %H:%M:%S")
        struct_time_1 = time.strptime(str1, "%Y-%m-%d %H:%M:%S")
        x = datetime.datetime(year=struct_time_1.tm_year, month=struct_time_1.tm_mon, day=struct_time_1.tm_mday, hour=struct_time_1.tm_hour, minute=struct_time_1.tm_min, second=struct_time_1.tm_sec)
        y = datetime.datetime(year=struct_time_2.tm_year, month=struct_time_2.tm_mon, day=struct_time_2.tm_mday, hour=struct_time_2.tm_hour, minute=struct_time_2.tm_min, second=struct_time_2.tm_sec)
        if (x.__rsub__(y).seconds) < 10:
            log.success("Successfully check_rtc_time.")
        else:
            err_count += 1
        if err_count:
            log.fail("the time read by diag tool is less than hwclock over 10 seconds")
            raise testFailed("check_rtc_time fail")

################################################################################
# Function Name: switch_and_verify_pem_info
# Date         : 28th July 2020
# Author       : Junjie Tang <junang@celestica.com>
#
# Procedure Revision Details:
#   Version : 1.0  - Initial Draft  - by Junjie Tang <junang@celestica.com>
################################################################################
    def switch_and_verify_pem_info(self):
        log.debug('Entering procedure switch_and_verify_pem_info')
        var_toolName = cel_pem_tools["bin_tool"]
        var_option = "-r -o 0x4c"
        var_keywords_pattern = verify_pem_tool_option_main_information_pattern
        var_pass_pattern = ""
        var_path = BMC_DIAG_TOOL_PATH
        self.verify_bmc_diag_tool_simple_dict(var_toolName, var_option, var_keywords_pattern, var_pass_pattern, var_path)
        var_option = "-w -o 0x4c -d 0x55"
        var_keywords_pattern = ""
        self.verify_bmc_diag_tool_simple_dict(var_toolName, var_option, var_keywords_pattern, var_pass_pattern,var_path)
        var_option = "-r -o 0x4c"
        var_keywords_pattern = modify_pem_tool_option_main_information_pattern
        self.verify_bmc_diag_tool_simple_dict(var_toolName, var_option, var_keywords_pattern, var_pass_pattern,var_path)


    #######################################################################################################################
    # Function Name: wait_for_openbmc_prompt_back
    # Date         : 24th July 2020
    # Author       : Abhisit Sangjan <asang@celestica.com>
    #
    # Procedure Revision Details:
    # Version : 1.0  - Initial - by Abhisit Sangjan <asang@celestica.com>
    #######################################################################################################################
    def wait_for_openbmc_prompt_back(self):
        self.wpl_log_debug('Entering procedure wait_for_openbmc_prompt_back with args : %s' % (str(locals())))

        kernel_bootup_msg = 'Starting kernel ...'
        output = self.wpl_receive(kernel_bootup_msg, timeout=1800)
        self.wpl_log_debug(output)
        time.sleep(198)
        self.wpl_getPrompt("openbmc", timeout=1800)

    def wait_for_centos_prompt_back(self):
        self.wpl_log_debug('Entering procedure wait_for_openbmc_prompt_back with args : %s' % (str(locals())))

        #bootup_msg = '>>Start PXE over IPv6.'
        #output = self.wpl_receive(bootup_msg, timeout=1800)
        #self.wpl_log_debug(output)
        self.wpl_getPrompt(centos_mode, timeout=1800)
        
    def wait_enter_centos(self, device="DUT"):
        self.wpl_log_debug('Entering procedure wait_enter_centos with args : %s' % (str(locals())))
        deviceObj = Device.getDeviceObject(device)
        cmd = 'sol.sh'
        p1 = 'Checking Media Presence'
        p2 = 'CentOS Linux'
        self.wpl_transmit(cmd)
        output = self.wpl_receive(self.device.loginPromptDiagOS, timeout=600)
        res = re.search(p2, output)
        if res:
            self.wpl_log_info('find the keyword, wait enter the centos!')
            deviceObj.getPrompt(centos_mode, timeout=300)
        else:
            raise testFailed("wait_enter_centos fail")

    #############################################################################################
    # Function Name: run_sdk_init
    # Date         : 8th August 2020
    # Author       : Abhisit S. <asang@celestica.com>
    #
    # Procedure Revision Details:
    #   Version : 1.0  - Original author by Prapatsorn W. <pwisutti@celestica.com>
    #   Version : 1.1  - Added more code to check the PASS keyword by Abhisit S. <asang@celestica.com>
    #############################################################################################
    def run_sdk_init(self, device="DUT", cmd="", log_file=None):
        self.wpl_log_debug('Entering procedure run_sdk_init with args : %s\n' %(str(locals())))
        deviceObj = Device.getDeviceObject(device)
        deviceObj.getPrompt(centos_mode)
        upcmd = 'ifconfig usb0 up'
        deviceObj.executeCmd(upcmd, 'centos', timeout=60)
        deviceObj.sendline(cmd)
        output = deviceObj.read_until_regexp(Const.promptPython3, timeout=600)
        deviceObj.sendline("exit()")
        deviceObj.getPrompt(centos_mode)
        if log_file:
            verify_log_cmd = 'tail -n 20 ' + log_file
            output = self.wpl_execute(verify_log_cmd, timeout=300)

        match = re.search(r'Counters Consistency Check Passed!!!', output)
        if not match:
            self.wpl_raiseException("The SDK initialization is failed")

        self.wpl_log_success("Successfully run_sdk_init")


#######################################################################################################################
# Function Name: test_ssd_stress_and_check_status
# Date         : 19th Aug 2020
# Author       : hemin <hemin@celestica.com>
#
# Procedure Revision Details:
#   Version : 1.0  - Initial Draft  - by hemin <hemin@celestica.com>
#######################################################################################################################
    def test_fpga_function(self, cmd_list, pass_pattern):
        self.wpl_log_debug('Entering procedure test_fpga_function with args : %s' % (str(locals())))

        for cmd in cmd_list:
            self.wpl_execute(cmd, 'centos', timeout=60)
            #for line in output.splitlines():
            #    line = line.strip()
            #    if line.endswith("#") or line.endswith(cmd):
            #        continue
            #    else:
            #        self.wpl_log_fail('Exiting test_fpga_function with result FAIL')
        cmd_str = 'cat /proc/interrupts | grep uio'
        pass_count = 0
        output = self.wpl_execute(cmd_str, 'centos', timeout=60)
        self.wpl_log_debug('******************output=%s********' % output)
        for line in output.splitlines():
            line = line.strip()
            match = re.search(pass_pattern, line)
            if match:
                pass_count += 1
        if pass_count:
            self.wpl_log_success('test_fpga_function test result for DIAG tool - %s is PASSED\n' % cmd_str)
        else:
            self.wpl_log_fail('Exiting test_fpga_function with result FAIL')
            self.wpl_raiseException("Failure while testing DIAG tool '%s' " % cmd_str)


#######################################################################################################################
# Function Name: compare_two_files
# Date         : Aug 27th 2020
# Author       : Hemin <hemin@celestica.com>
#
# Procedure Revision Details:
#   Version : 1.0  - Initial Draft  - by Hemin <hemin@celestica.com>
#######################################################################################################################
    def compare_two_files(self, file1, file2):
        self.wpl_log_debug('Entering procedure compare_two_files with args : %s' % (str(locals())))

        cmd = 'diff ' + file1 + ' ' + file2
        output = self.wpl_execute(cmd, 'openbmc', timeout=60)
        p_fail = 'Files.*differ'
        failCount = 0
        for line in output.splitlines():
            line = line.strip()
            if re.search(p_fail, line):
                failCount += 1
        if failCount:
            return False
        else:
            return True


#######################################################################################################################
# Function Name: bmc_switch_firmware_update
# Date         : Aug 25th 2020
# Author       : Hemin <hemin@celestica.com>
#
# Procedure Revision Details:
#   Version : 1.0  - Initial Draft  - by Hemin <hemin@celestica.com>
#######################################################################################################################
    def bmc_switch_firmware_update(self, cmd_str, image_version, pass_pattern_list, path=BMC_PCIE_SWITCH_PATH):
        self.wpl_log_debug('Entering procedure bmc_switch_firmware_update with args : %s' % (str(locals())))

        cmd1 = 'cd ' + path
        self.wpl_transmit(cmd1)
        cmd = cmd_str + ' ' + image_version
        passCount = 0
        match_list = list()
        output = self.wpl_execute_cmd(cmd, 'openbmc', timeout=300)
        for line in output.splitlines():
            line = line.strip()
            for p_pass in pass_pattern_list:
                if p_pass in line:
                    passCount += 1
                    match_list.append(p_pass)
        miss_match = set(pass_pattern_list) - set(match_list)
        if passCount == len(pass_pattern_list):
            if 'read' in cmd_str:
                status = self.compare_two_files(oob_switch_image, image_read_path)
                if status:
                    self.wpl_log_success('bmc_switch_firmware_update test result for DIAG tool - %s is PASSED\n' % cmd)
                else:
                    self.wpl_log_fail('Exiting bmc_switch_firmware_update with result FAIL')
                    self.wpl_raiseException("Failure while testing DIAG tool '%s' " % cmd)
            else:
                self.wpl_log_fail('miss match is : %s' % miss_match)
                self.wpl_log_success('bmc_switch_firmware_update test result for DIAG tool - %s is PASSED\n' % cmd)
        else:
            self.wpl_log_fail('miss match is : %s' % miss_match)
            self.wpl_log_fail('Exiting bmc_switch_firmware_update with result FAIL')
            self.wpl_raiseException("Failure while testing DIAG tool '%s' " % cmd)


#######################################################################################################################
# Function Name: check_info_contains
# Date         : Aug 27th 2020
# Author       : Yang, Xuecun <yxcun@celestica.com>
#
# Procedure Revision Details:
#   Version : 1.0  - Initial Draft  - by Yang, Xuecun <yxcun@celestica.com>
#######################################################################################################################
    def check_info_contains(self, info_full_cmd, part_cmd_list, skip_lines=0, path=None, exclude=[], remove_pattern=None):
        self.wpl_log_debug('Entering procedure check_info_contains with args : %s' % (str(locals())))
        if path:
            self.wpl_execute_cmd( "cd %s"%path, timeout=5)
        output_full = self.wpl_execute_cmd(info_full_cmd, timeout=300)
        fail_count = 0
        not_found = {}
        total_num = len(part_cmd_list)
        for part_cmd in part_cmd_list:
            output_part = self.wpl_execute_cmd(part_cmd, timeout=300).split(part_cmd)[1]
            lines = output_part.splitlines()[skip_lines:-4]
            for line in lines:
                line_skip = 0
                for item in exclude:
                    if item in line:
                        line_skip = 1
                        break
                if line_skip:
                    continue
                if remove_pattern:
                    for p_remove in remove_pattern:
                        line = re.sub(p_remove, "", line)
                if line not in output_full:
                    not_found[part_cmd] = line
                    fail_count += 1
                    break
        if fail_count:
            not_found_str = "\n".join([" command: {}, mismatch line:{}".format(cmd, line) for cmd, line in not_found.items() ])
            self.wpl_log_fail('Exiting check_info_contains with result failed, failed num:{}, total num:{}.'.format(fail_count, total_num))
            self.wpl_raiseException("Failure while testing check_info_contains with commands items => {}".format(not_found_str))
        else:
            self.wpl_log_success('%s printout containing test is PASSED'%info_full_cmd)


#######################################################################################################################
# Function Name: update_cpld_fw
# Date         : September 4th 2020
# Author       : Hemin <hemin@celestica.com>
#
# Procedure Revision Details:
#   Version : 1.0  - Initial Draft  - by Hemin <hemin@celestica.com>
#######################################################################################################################
    def update_cpld_fw(self, toolName, option1, dev, option2, image, check_pattern, img_path, option3=''):
        self.wpl_log_debug('Entering procedure update_cpld_fw with args : %s' % (str(locals())))
        cmd = 'cd ' + BMC_DIAG_TOOL_PATH
        passCount = 0
        patternNum = len(check_pattern)
        self.wpl_getPrompt("openbmc", 600)
        self.wpl_transmit(cmd)
        cmd = './' + toolName + ' ' + option1 + ' ' + dev + ' ' + option2 + ' ' + img_path + image + ' ' + option3
        if toolName == 'cpld_update.sh':
            cmd = toolName + ' ' + option1 + ' ' + dev + ' ' + option2 + ' ' + img_path + image + ' ' + option3
        self.wpl_log_debug('cammand = %s' % cmd)
        self.wpl_log_debug('cammand = %s' % cmd)
        output = self.wpl_execute(cmd, mode='openbmc', timeout=3600)
        for line in output.splitlines():
            line = line.strip()
            for i in range(0, patternNum):
                match = re.search(check_pattern[i], line)
                if match:
                    passCount += 1
        if passCount == patternNum:
            self.wpl_log_success("Successfully %s %s \'%s\'"% (toolName, dev, image))
        else:
            self.wpl_raiseException("Failed %s %s \'%s\'"% (toolName, dev, image))

    #######################################################################################################################
    # Function Name: check_power_cycle_stress_option_n
    # Date         : September 17th 2020
    # Author       : Xiaoqiang Wang <xiaoqiwa@celestica.com>
    #
    # Procedure Revision Details:
    #   Version : 1.0  - Initial Draft  - by Xiaoqiang Wang <xiaoqiwa@celestica.com>
    #######################################################################################################################
    def check_power_cycle_stress_option_n(self, loop):
        self.wpl_log_debug('Entering procedure check_power_cycle_stress_option_n with args : %s' % (str(locals())))
        cmd = 'cd ' + BMC_STRESS_POWER_CYCLE_PATH
        self.wpl_transmit(cmd)
        cmd = './power_cycle_stress.sh -n ' + loop
        self.wpl_transmit(cmd)
        for i in range(0, int(loop)):
            self.wpl_receive('Starting kernel', timeout=180)
            self.device.read_until_regexp(self.device.loginPromptBmc + '|OpenBMC Release', timeout=BOOTING_TIME)
            time.sleep(120)
        self.wpl_getPrompt('centos', timeout=BOOTING_TIME)
        self.wpl_getPrompt('openbmc', timeout=BOOTING_TIME)
        time.sleep(5)

        cmd = 'cd ' + BMC_STRESS_POWER_CYCLE_PATH + '/log'
        self.wpl_transmit(cmd)
        cmd = 'cat log.txt'
        output = self.wpl_execute_cmd(cmd)
        r = re.search("error|fail", output, re.I)
        if not r:
            self.wpl_log_success("check_power_cycle_stress_option_n Successfully.")
        else:
            self.wpl_raiseException("check_power_cycle_stress_option_n Failed!")

    #######################################################################################################################
    # Function Name: reboot_and_check_bios_version
    # Date         : September 22nd 2020
    # Author       : Abhisit Sangjan <asang@celestica.com>
    #
    # Procedure Revision Details:
    #   Version : 1.0  - Initial Draft  - by Abhisit Sangjan <asang@celestica.com>
    #######################################################################################################################
    def reboot_and_check_bios_version(self, bios_version):
        self.wpl_log_debug('Entering procedure reboot_and_check_bios_version with args : %s' % (str(locals())))

        output = self.wpl_execute_cmd("wedge_power.sh status", mode=openbmc_mode, timeout=300)
        match = re.match(r'[ \t]*Microserver[ \t]+power[ \t]+is[ \t]+off[ \t]*$', output)
        if match:
            cmd = "wedge_power.sh on"
        else:
            cmd = "wedge_power.sh reset"
        self.wpl_transmit(cmd)
        self.wpl_getPrompt('openbmc', timeout=BOOTING_TIME)

        self.wpl_transmit("sol.sh")
        output = self.device.read_until_regexp(r'Press[ \t]+<F12>', timeout=300)
        self.wpl_getPrompt('centos', timeout=BOOTING_TIME)  # Wait for the prompt back for next TC

        _bios_version_pattern = r'BIOS[ \t]+Date:[ \t\d\/:]+Ver:[ \t]+(?P<bios_version>\w+)'
        match = re.search(_bios_version_pattern, output)
        if match:
            if bios_version == match.group("bios_version"):
                self.wpl_log_success("Successfully to compare BIOS Version enter_to_bios_menu_and_check_bios_version.")
                return
            else:
                self.wpl_raiseException("Failed to compare %s (given) != %s (installed)" %(bios_version, match.group("bios_version")))
                return

        self.wpl_raiseException("Failed, not found %s, enter_to_bios_menu_and_check_bios_version." %(str(_bios_version_pattern).strip()))

    #######################################################################################################################
    # Function Name: check_i2c_stress_option_n
    # Date         : September 24th 2020
    # Author       : Xiaoqiang Wang <xiaoqiwa@celestica.com>
    #
    # Procedure Revision Details:
    #   Version : 1.0  - Initial Draft  - by Xiaoqiang Wang <xiaoqiwa@celestica.com>
    #######################################################################################################################
    def check_i2c_stress_option_n(self, loop):
        self.wpl_log_debug('Entering procedure check_i2c_stress_option_n with args : %s' % (str(locals())))
        cmd = 'cd ' + BMC_STRESS_I2C_PATH + '/log'
        self.wpl_transmit(cmd)
        cmd = 'rm log.txt  opt.txt'
        self.wpl_transmit(cmd)

        cmd = 'cd ' + BMC_STRESS_I2C_PATH
        self.wpl_transmit(cmd)
        cmd = I2C_SLEEP_CMD
        self.wpl_transmit(cmd)
        time.sleep(3)
        cmd = './i2c_stress.sh -n ' + loop
        output = self.wpl_execute_cmd(cmd, timeout=600)
        #r = re.search("error|fail", output, re.I)
        r = re.search("NO", output)
        if r is None:
            self.wpl_log_success("exec cmd {} Successfully.".format(cmd))
        else:
            retry_lst = []
            for line in output.splitlines():
                res = re.search('NO', line)
                if res:
                    item = line.split()[0]
                    retry_lst.append(item)
            for line in retry_lst:
                mat = str(line) + r'.*OK'
                res = re.search(mat, output)
                if res:
                    self.wpl_log_success("exec retry item {} Successfully.".format(line))
                else:
                    self.wpl_raiseException("exec cmd {} Failed!".format(cmd))

        time.sleep(5)
        cmd = 'cd ' + BMC_STRESS_I2C_PATH + '/log'
        self.wpl_transmit(cmd)
        cmd = 'cat log.txt'
        output = self.wpl_execute_cmd(cmd)
        r = re.search("NO", output)
        if r is None:
            self.wpl_log_success("check_i2c_stress_option_n Successfully.")
        else:
            retry_lst1 = []
            for line in output.splitlines():
                res = re.search('NO', line)
                if res:
                    item = line.split()[0]
                    retry_lst1.append(item)
            for line in retry_lst1:
                mat = str(line) + r'.*OK'
                res = re.search(mat, output)
                if res:
                    self.wpl_log_success("exec retry item {} Successfully.".format(line))
                else:
                    self.wpl_raiseException("check_i2c_stress_option_n Failed!")

    #######################################################################################################################
    # Function Name: check_emmc_stress_option_n
    # Date         : Nov. 24th 2020
    # Author       : Xiaoqiang Wang <xiaoqiwa@celestica.com>
    #
    # Procedure Revision Details:
    #   Version : 1.0  - Initial Draft  - by Xiaoqiang Wang <xiaoqiwa@celestica.com>
    #######################################################################################################################
    def check_emmc_stress_option_n(self, loop):
        self.wpl_log_debug('Entering procedure check_emmc_stress_option_n with args : %s' % (str(locals())))
        cmd = 'cd ' + BMC_STRESS_EMMC_PATH + '/log'
        self.wpl_transmit(cmd)
        cmd = 'rm log.txt'
        self.wpl_transmit(cmd)

        cmd = './emmc_stress_test.sh -n ' + loop
        var_toolName = 'emmc_stress_test.sh'
        var_option = "-n " + loop
        var_keywords_pattern = emmc_stress_pattern
        var_pass_pattern = ""
        var_path = BMC_STRESS_EMMC_PATH
        self.verify_bmc_diag_tool_simple_dict(var_toolName, var_option, var_keywords_pattern, var_pass_pattern, var_path)

        time.sleep(5)
        cmd = 'cd ' + BMC_STRESS_EMMC_PATH + '/log'
        self.wpl_transmit(cmd)
        cmd = 'cat log.txt'
        output = self.wpl_execute_cmd(cmd)
        r = re.findall("PASS", output)
        if len(r) == int(loop):
            self.wpl_log_success("check_emmc_stress_option_n Successfully.")
        else:
            self.wpl_raiseException("check_emmc_stress_option_n Failed!")

    #######################################################################################################################
    # Function Name: check_bic_stress_option_n
    # Date         : Oct 1th 2020
    # Author       : Xiaoqiang Wang <xiaoqiwa@celestica.com>
    #
    # Procedure Revision Details:
    #   Version : 1.0  - Initial Draft  - by Xiaoqiang Wang <xiaoqiwa@celestica.com>
    #######################################################################################################################
    def check_bic_stress_option_n(self, loop):
        self.wpl_log_debug('Entering procedure check_bic_stress_option_n with args : %s' % (str(locals())))
        cmd = 'cd ' + BMC_STRESS_BIC_PATH + '/log'
        self.wpl_transmit(cmd)
        cmd = 'rm log.txt  opt.txt'
        self.wpl_transmit(cmd)

        cmd = 'cd ' + BMC_STRESS_BIC_PATH
        self.wpl_transmit(cmd)
        cmd = './BIC_stress.sh -n ' + loop
        self.wpl_transmit(cmd)

        #self.wpl_receive('Power reset the whole')
        #self.device.read_until_regexp(self.device.loginPromptBmc, timeout=BOOTING_TIME)
        self.wpl_getPrompt('centos', timeout=BOOTING_TIME)
        self.wpl_getPrompt('openbmc', timeout=BOOTING_TIME)
        time.sleep(5)

        cmd = 'cd ' + BMC_STRESS_BIC_PATH + '/log'
        self.wpl_transmit(cmd)
        cmd = 'cat log.txt'
        output = self.wpl_execute_cmd(cmd)
        r = re.findall("BIC stress test PASSED", output, re.I)
        if len(r) >= 1:
            self.wpl_log_success("check_bic_stress_option_n Successfully.")
        else:
            self.wpl_raiseException("check_bic_stress_option_n Failed!")

    #######################################################################################################################
    # Function Name: check_fpga_pcie_stress_option_n
    # Date         : Oct 1th 2020
    # Author       : Xiaoqiang Wang <xiaoqiwa@celestica.com>
    #
    # Procedure Revision Details:
    #   Version : 1.0  - Initial Draft  - by Xiaoqiang Wang <xiaoqiwa@celestica.com>
    #######################################################################################################################
    def check_fpga_pcie_stress_option_n(self, loop):
        self.wpl_log_debug('Entering procedure check_fpga_pcie_stress_option_n with args : %s' % (str(locals())))
        cmd = 'cd ' + PCIE_STRESS_TOOL_PATH
        self.wpl_transmit(cmd)
        cmd = 'echo 0 > /var/log/messages'
        output = self.wpl_execute_cmd(cmd)

        cmd = './fpga_stress.sh ' + loop
        output = self.wpl_execute_cmd(cmd, timeout=600)
        r = re.search("error|fail", output, re.I)
        if r:
            self.wpl_raiseException("exec cmd {} Failed!".format(cmd))

        time.sleep(5)
        cmd = 'cat /var/log/messages'
        output = self.wpl_execute_cmd(cmd, timeout=600)
        r = re.search("error|fail", output, re.I)
        if r:
            self.wpl_raiseException("check /var/log/messages Failed!")

        cmd = 'cat /var/log/mcelog'
        output = self.wpl_execute_cmd(cmd, timeout=600)
        r = re.search("error|fail", output, re.I)
        if r:
            self.wpl_raiseException("check /var/log/mcelog Failed!")

        self.wpl_log_success("check_fpga_pcie_stress_option_n Successfully.")

    #######################################################################################################################
    # Function Name: setpci
    # Date         : October 4th 2020
    # Author       : Abhisit Sangjan <asang@celestica.com>
    #
    # Procedure Revision Details:
    #   Version : 1.0  - Initial Draft  - by Abhisit Sangjan <asang@celestica.com>
    #######################################################################################################################
    def setpci(self, argument="", regex="", mode="centos", timeout=60):
        self.wpl_log_debug('Entering procedure setpci with args : %s' % (str(locals())))

        _output = self.wpl_execute(cmd="setpci " + argument, mode=mode, timeout=timeout)
        if regex != "":
            if not re.search(regex, _output):
                self.wpl_raiseException("After ran setpci not found \"" + regex + "\"")
        else:
            return _output

    #######################################################################################################################
    # Function Name: lspci
    # Date         : October 4th 2020
    # Author       : Abhisit Sangjan <asang@celestica.com>
    #
    # Procedure Revision Details:
    #   Version : 1.0  - Initial Draft  - by Abhisit Sangjan <asang@celestica.com>
    #######################################################################################################################
    def lspci(self, argument="-tvn", device_list=list(), mode="centos", timeout=60):
        self.wpl_log_debug('Entering procedure lspci with args : %s' % (str(locals())))
        cmd1 = 'lspci -s 06:00.0'
        output = self.wpl_execute(cmd1, mode=mode, timeout=timeout)
        mat_value = r'^06:00.0 Ethernet controller.* (b\d{3})'
        for line in output.splitlines():
            if re.search(mat_value, line):
                match = re.search(mat_value, line)
                pci_value = match.group(1)
        if pci_value == 'b990':
            self.wpl_log_info('This is TH4 chip.')
        else:
            self.wpl_log_info('This is TH4L chip.')
            for index, tup in enumerate(device_list):
                if '14e4' in tup:
                    device_list[index] = ('14e4', pci_value)
        _output = self.wpl_execute(cmd="lspci " + argument, mode=mode, timeout=timeout)
        _match = re.findall(r"(?P<vid>[a-f0-9]{4}):(?P<pid>[a-f0-9]{4})", _output)
        for m, l in zip(_match, device_list):
            if m != l:
                if l[0] == '1344' and l[1] == '5410':
                    cmd2 = 'lspci -n |grep 07:00.0'
                    output2 = self.wpl_execute(cmd2, mode=mode, timeout=timeout)
                    if m[0] in output2:
                        self.wpl_log_info("The vendor is VID= "+ m[0] + ", PID = " + m[1])
                else:
                    self.wpl_raiseException("Not found the PCI Device with VID = " + l[0] + ", PID = " + l[1])

    #######################################################################################################################
    # Function Name: i2cdump
    # Date         : October 4th 2020
    # Author       : Abhisit Sangjan <asang@celestica.com>
    #
    # Procedure Revision Details:
    #   Version : 1.0  - Initial Draft  - by Abhisit Sangjan <asang@celestica.com>
    #######################################################################################################################
    def i2cdump(self, argument="", where=[], mode="centos", timeout=60):
        self.wpl_log_debug('Entering procedure i2cdump with args : %s' % (str(locals())))

        _output = self.wpl_execute(cmd="i2cdump " + argument, mode="openbmc", timeout=60)
        return re.findall(
            r"(?P<addr_nx>[a-f0-9]0): " +
            r"(?P<data_0n>[a-f0-9]{2}) (?P<data_1n>[a-f0-9]{2}) (?P<data_2n>[a-f0-9]{2}) (?P<data_3n>[a-f0-9]{2}) " +
            r"(?P<data_4n>[a-f0-9]{2}) (?P<data_5n>[a-f0-9]{2}) (?P<data_6n>[a-f0-9]{2}) (?P<data_7n>[a-f0-9]{2}) " +
            r"(?P<data_8n>[a-f0-9]{2}) (?P<data_9n>[a-f0-9]{2}) (?P<data_an>[a-f0-9]{2}) (?P<data_bn>[a-f0-9]{2}) " +
            r"(?P<data_cn>[a-f0-9]{2}) (?P<data_dn>[a-f0-9]{2}) (?P<data_en>[a-f0-9]{2}) (?P<data_fn>[a-f0-9]{2})",
            _output
        )

    #######################################################################################################################
    # Function Name: verify_qsfp_test
    # Date         : 9th October 2020
    # Author       : hemin <hemin@celestica.com>
    #
    # Procedure Revision Details:
    #   Version : 1.0  - Initial Draft  - by hemin <hemin@celestica.com>
    #######################################################################################################################
    def verify_qsfp_test(self, toolName, option_m, option_p, option_i, pass_pattern, path):
        self.wpl_log_debug('Entering procedure verify_qsfp_test with args : %s' % (str(locals())))

        for i in range(1,9):
            if 'minipack2_dc' in devicename.lower():
                if (i == 3) or (i == 4) or (i == 5) or (i == 6):
                    continue
            for j in range(1, 17):
                new_option_m = option_m + str(i)
                new_option_p = option_p + str(j)
                cmd = './' + toolName + ' ' + new_option_m + ' ' + new_option_p + ' ' + option_i
                key_words = 'Pim #' + str(i) + ' Port #' + str(j) + ' eeprom information:'
                self.execute_check_cmd(cmd=cmd, mode='centos', patterns=pass_pattern, path=path)

    #######################################################################################################################
    # Function Name: verify_fru_eeprom_update
    # Date         : 10th October 2020
    # Author       : hemin <hemin@celestica.com>
    #
    # Procedure Revision Details:
    #   Version : 1.0  - Initial Draft  - by hemin <hemin@celestica.com>
    #######################################################################################################################
    def verify_fru_eeprom_update(self, read_tool, read_option, write_tool, path, pass_pattern, verify_tool):
        self.wpl_log_debug('Entering procedure verify_fru_eeprom_update with args : %s' % (str(locals())))

        cmd = 'cd ' + path
        self.wpl_transmit(cmd)
        read_cmd = './' + read_tool + ' ' + read_option
        linecount = 0
        output = self.wpl_execute_cmd(read_cmd, timeout=300)
        for line in output.splitlines():
            if '=' in line:
                linecount += 1
        if linecount < 20:
            self.wpl_log_fail('Exiting verify_fru_eeprom_update with result FAIL')
            self.wpl_raiseException("Failure while testing DIAG tool '%s' " % write_tool)
        config_file = 'eeprom.cfg'
        read_file = 'eeprom_out.cfg'
        bkp_file = 'eeprom_out_bkp.cfg'
        cmd1 = 'cp ' + read_file + ' ' + config_file
        cmd2 = 'cp ' + read_file + ' ' + bkp_file
        self.wpl_transmit(cmd1)
        self.wpl_transmit(cmd2)
        cmd = './' + write_tool
        passcount = 0
        linecount = 0
        output = self.wpl_execute_cmd(cmd, timeout=300)
        for line in output.splitlines():
            if re.search(pass_pattern, line):
                passcount += 1
        if passcount == 0:
            self.wpl_log_fail('Exiting verify_fru_eeprom_update with result FAIL')
            self.wpl_raiseException("Failure while testing DIAG tool '%s' " % write_tool)
        cmd = 'count=' + '`diff ' + bkp_file + ' ' + read_file + ' | wc -l' +'`'
        output = self.wpl_execute(cmd, timeout=300)
        return_cmd = 'echo count=$count'
        output = self.wpl_execute(return_cmd, timeout=300)
        if re.search('count=0', output):
            self.wpl_log_success('%s printout containing test is PASSED' % write_tool)
        verify_cmd = './' + verify_tool
        verifycount = 0
        verify_output = self.wpl_execute_cmd(verify_cmd, timeout=300)
        for line in verify_output.splitlines():
            if re.search(pass_pattern, line):
                verifycount += 1
        if 'count=0' in output and verifycount:
            self.wpl_log_success('%s printout containing test is PASSED' % write_tool)
        else:
            self.wpl_log_fail('Exiting verify_fru_eeprom_update with result FAIL')
            self.wpl_raiseException("Failure while testing DIAG tool '%s' " % write_tool)

    #######################################################################################################################
    # Function Name: check_fru_eeprom_update
    # Date         : 12th October 2020
    # Author       : hemin <hemin@celestica.com>
    #
    # Procedure Revision Details:
    #   Version : 1.0  - Initial Draft  - by hemin <hemin@celestica.com>
    #######################################################################################################################
    def check_fru_eeprom_update(self, read_tool, read_option, write_tool, verify_tool, path, pass_pattern):
        self.wpl_log_debug('Entering procedure check_fru_eeprom_update with args : %s' % (str(locals())))

        cmd = 'cd ' + path
        self.wpl_transmit(cmd)
        file_list = list()
        for i in range(1, 9):
            if 'minipack2_dc' in devicename.lower():
                if (i == 3) or (i == 4) or (i == 5) or (i == 6):
                    continue
            read_cmd = './' + read_tool + ' ' + read_option + ' ' + '-f' + ' ' + str(i)
            output = self.wpl_execute_cmd(read_cmd, timeout=300)
            read_file = 'eeprom_out.cfg'
            new_file_name = 'eeprom_part' + str(i) + '.cfg'
            file_list.append(new_file_name)
            cmd = 'cp ' + read_file + ' ' + new_file_name
            self.wpl_transmit(cmd)
            lines = output.splitlines()
            if len(lines) > 20:
                continue
            else:
                self.wpl_log_fail('Exiting check_fru_eeprom_update with result FAIL')
                self.wpl_raiseException("Failure while testing DIAG tool '%s' " % read_tool)
        config_file = 'eeprom.cfg'
        for i in range(1, 9):
            if 'minipack2_dc' in devicename.lower():
                if (i == 3) or (i == 4) or (i == 5) or (i == 6):
                    continue
                if (i == 7) or (i == 8):
                    cmd = 'cp ' + file_list[i - 5] + ' ' + config_file
                else:
                    cmd = 'cp ' + file_list[i - 1] + ' ' + config_file
            else:
                cmd = 'cp ' + file_list[i-1] + ' ' + config_file
            self.wpl_transmit(cmd)
            cmd = './' + write_tool + ' ' + str(i)
            output = self.wpl_execute_cmd(cmd, timeout=300)
            match = re.search(pass_pattern, output)
            if not match:
                self.wpl_log_fail('Exiting check_fru_eeprom_update with result FAIL')
                self.wpl_raiseException("Failure while testing DIAG tool '%s' " % write_tool)
            read_cmd = './' + read_tool + ' ' + read_option + ' ' + '-f' + ' ' + str(i)
            verify_cmd = './' + verify_tool + ' ' + str(i)
            output = self.wpl_execute_cmd(read_cmd, timeout=300)
            if 'minipack2_dc' in devicename.lower():
                if (i == 7) or (i == 8):
                    cmd = 'count=' + '`diff ' + file_list[i - 5] + ' ' + read_file + ' | wc -l' + '`'
                else:
                    cmd = 'count=' + '`diff ' + file_list[i - 1] + ' ' + read_file + ' | wc -l' + '`'
            else:
                cmd = 'count=' + '`diff ' + file_list[i-1] + ' ' + read_file + ' | wc -l' + '`'
            output = self.wpl_execute(cmd, timeout=300)
            return_cmd = 'echo count=$count'
            return_output = self.wpl_execute(return_cmd, timeout=300)
            verify_output = self.wpl_execute(verify_cmd, timeout=300)
            if re.search('count=0', return_output) and re.search(pass_pattern, verify_output):
                self.wpl_log_success('%s printout containing test is PASSED' % write_tool)
            else:
                self.wpl_log_fail('Exiting check_eeprom_config_file with result FAIL')
                self.wpl_raiseException("Failure while testing DIAG tool '%s' " % verify_tool)

    #######################################################################################################################
    # Function Name: verify_and_update_eeprom
    # Date         : 22th October 2020
    # Author       : hemin <hemin@celestica.com>
    #
    # Procedure Revision Details:
    #   Version : 1.0  - Initial Draft  - by hemin <hemin@celestica.com>
    #######################################################################################################################
    def verify_and_update_eeprom(self, read_tool, write_tool, option, path, line_string, passPattern, part=''):
        self.wpl_log_debug('Entering procedure verify_and_update_eeprom with args : %s' % (str(locals())))

        ## judge w400 power type
        #self.power_type_check_w400()

        cmd = 'cd ' + path
        self.wpl_transmit(cmd)
        if part == 'FAN':
            loop = 5
        else:
            loop = 2
        for i in range(1, loop):
            if loop == 5:
                part = 'FAN' + str(i)
            read_cmd = './' + read_tool + ' ' + option + ' ' + part
            self.wpl_transmit(read_cmd)
            cfg_file = 'eeprom.cfg'
            bkp_file = 'eeprom_' + part + '.cfg'
            read_file = 'eeprom_out.cfg'
            cmd1 = 'cp ' + read_file + ' ' + bkp_file
            cmd2 = 'cp ' + read_file + ' ' + cfg_file
            self.wpl_transmit(cmd1)
            self.wpl_transmit(cmd2)
            self.modify_eeprom_cfg_file(line_string, cfg_file)
            cmd = 'i2cset -f -y 2 0x3e 0x38 0'
            self.wpl_transmit(cmd)
            write_cmd = './' + write_tool + ' ' + part
            passCount = 0
            output = self.wpl_execute_cmd(write_cmd, timeout=300)
            for line in output.splitlines():
                if re.search(line_string, line):
                    passCount += 1
                elif re.search(passPattern, line):
                    passCount += 1
            if passCount < 2:
                self.wpl_log_fail('Exiting verify_and_update_eeprom with result FAIL')
                self.wpl_raiseException("Failure while testing DIAG tool '%s' " % write_tool)
            cmd = 'cp ' + bkp_file + ' ' + cfg_file
            self.wpl_transmit(cmd)
            output1 = self.wpl_execute_cmd(write_cmd, timeout=300)
            matchCount = 0
            for line in output1.splitlines():
                if re.search(passPattern, line):
                    matchCount += 1
            if matchCount:
                self.wpl_log_success('%s printout containing test is PASSED' % write_tool)
            else:
                self.wpl_log_fail('Exiting verify_and_update_eeprom with result FAIL')
                self.wpl_raiseException("Failure while testing DIAG tool '%s' " % write_tool)

#######################################################################################################################
    # Function Name: check_eth_dict_option_test
    # Date         : 5th Mar 2021
    # Author       : Eric Zhang <zfzhang@celestica.com>
    #
    # Procedure Revision Details:
    #   Version : 1.0  - Initial Draft  - by Eric Zhang <zfzhang@celestica.com>
    #######################################################################################################################
    def check_eth_dict_option_test(self, toolName, option, path):
        if path:
            cmd = 'cd' + ' ' + path
            self.wpl_transmit(cmd)

        if toolName == 'ifconfig':
            self.wpl_transmit(toolName + option)
            time.sleep(5)
            toolName = 'ping -c 5'
            option = ' fe80::ff:fe00:2%usb0'
        error_count = 0
        local_msg = []
        output = self.wpl_execute_cmd(toolName+option,timeout=30)
        fail_pattern = [
            'fail','no found'
        ]
        for line in output.splitlines():
            line = line.strip()
            for fail_message in range(0, len(fail_pattern)-1):
                if fail_pattern[fail_message] in line:
                    error_count += 1
                    local_msg.append(line)
        if error_count:
            self.wpl_raiseException("Failed check eth test!")
            self.wpl_log_info('local = %s '% local_msg)
        elif error_count == 0:
            self.wpl_log_success("Check eth test pass!")
    @logThis
    def verify_config_yaml_test(self,toolName, option, keywords_pattern='none', pass_pattern="none", path='none'):

        if path:
            self.wpl_transmit('cd ' + path)

        passCount = 0
        output = self.EXEC_diag_tool_command(toolName, option, path)
        for line in output.splitlines():
            line = line.strip()
            for p_pass in pass_pattern:
                match = re.search(p_pass, line)
                if match:
                    passCount += 1
        if passCount == len(pass_pattern):
            self.wpl_log_success('verify_config_yaml_test test result for DIAG tool - %s is PASSED\n' % toolName)
        else:
            self.wpl_log_fail('Exiting verify_config_yaml_test with result FAIL')
            self.wpl_raiseException("Failure while testing DIAG tool '%s':'" % toolName)
    #######################################################################################################################
    # Function Name: modify_eeprom_cfg_file
    # Date         : 22th October 2020
    # Author       : hemin <hemin@celestica.com>
    #
    # Procedure Revision Details:
    #   Version : 1.0  - Initial Draft  - by hemin <hemin@celestica.com>
    #######################################################################################################################
    def modify_eeprom_cfg_file(self, line_string, file):
        self.wpl_log_debug('Entering procedure modify_eeprom_cfg_file with args : %s' % (str(locals())))

        cmd = 'sed -i \'s/WUS/' + line_string + '/g\'' + ' ' + file
        self.wpl_transmit(cmd)

    #######################################################################################################################
    # Function Name: is_using_pem
    # Date         : 6th January 2021
    # Author       : Prapatsorn W. <pwsutti@celestica.com>
    #
    # Procedure Revision Details:
    #   Version : 1.0  - Initial Draft  - by Prapatsorn W. <pwsutti@celestica.com>
    #######################################################################################################################
    def is_using_pem(self):
        return self.device.is_using_pem()
#######################################################################################################################
# Function Name: test_init_sdk_and_switch_to_bmc/verify_high_power_sensor_GB_test
# Date         : 02 Feb 2021
# Author       : Eric Zhang<zfzhang@celestica.com>
#
# Procedure Revision Details:
#   Version : 1.0  - Initial Draft  - by Eric Zhang<zfzhang@celestica.com>
#######################################################################################################################
    def test_init_sdk_and_switch_to_bmc(self,cmd,path):
        self.wpl_log_debug('Entering procedure test_init_sdk_and_switch_to_bmc: %s\n' % (str(locals())))
        self.wpl_transmit('cd ' + path)

        self.device.sendMsg(cmd+'\n')
        pattern_line = "Using regular LLD implementation, all blocks are enabled by default"
        line = self.device.readUntil(pattern_line, timeout=60)
        if line:
            self.wpl_log_debug("///////finding the line match!///////////")
            time.sleep(200)
            CommonLib.switch_to_openbmc()
            self.wpl_getPrompt(openbmc_mode, timeout=60)
            self.wpl_log_debug('switch to openbmc successfully')
        else:
            self.wpl_raiseException('Can not capture the message %s' % pattern_line)

    def test_exit_sdk_mode(self, cmd, pattern):
        self.wpl_log_debug('Entering procedure test_exit_sdk_mode: %s\n' % (str(locals())))
        self.device.sendMsg("sol.sh\r\n")
        time.sleep(2)
        self.device.sendMsg('\r\n')
        message = self.device.read_until_regexp(pattern, timeout=1200)
        if message:
            time.sleep(300)
            self.device.sendMsg("{}\r\n".format(cmd))
            deviceObj.getPrompt(centos_mode)
            log.info("Successfully run_sdk_init")
        else:
            self.wpl_raiseException('can not get prompt >>>')

    def verify_high_power_sensor_GB_test(self, cmd, pattern, path):
        self.wpl_log_debug('Entering procedure verify_high_power_sensor_GB_test: %s\n' % (str(locals())))
        self.wpl_transmit('cd ' + path)

        output = self.wpl_execute_cmd(cmd, mode=openbmc_mode, timeout=1800)
        devicename = os.environ.get("deviceName", "")
        if 'wedge400_' in devicename.lower():
            p1 = r'(\w+(\(\w+\.?\w+\))?)[ \t]+\(\w+\) :[ \t]+\-?[\d.]+ (C|Volts|Amps|Watts|RPM)[ \t]+\| \((\w+)\) \| UCR\:'
            p2 = r'PSU2 12V Output Power\:\s+([\d\.]+) W'
            for line in output.splitlines():
                line = line.strip()
                mat1 = re.search(p1, line)
                mat2 = re.search(p2, line)
                if ('-a' in cmd) or ('test -u' in cmd):
                    for p3 in pattern:
                        mat3 = re.search(p3, line)
                        if mat3:
                            pattern.remove(p3)
                if ('test -s' in cmd) or ('--threshold' in cmd):
                    if mat1:
                        if mat1.group(4) == 'ok':
                            log.info('Sensor name %s is ok!' % (mat1.group(1)))
                        else:
                            self.wpl_raiseException('Sensor %s status is not ok!' % (mat1.group(1)))
                if cmd == 'sensors':
                    if mat2:
                        if float(mat2.group(1)) > 60:
                            log.info('Successfully Start_high_power_and_verify_sensor_test.')
                        else:
                            self.wpl_raiseException('Sensors check failed, please see output!')
            if ('-a' in cmd) or ('test -u' in cmd):
                if len(pattern) == 0:
                    self.wpl_log_info('Successfully verify sensor -a/-u test.')
                else:
                    self.wpl_raiseException('check -a/-u failed, please see output!')
        else:
            for line in output.splitlines():
                line = line.strip()
                for p_pass in pattern:
                    match1 = re.search(p_pass, line)
                    match2 = re.search("GB_TEMP\d[ \t]+\(0x\d\d\)\s+:\s+N.*A", line)
                    if match1:
                        pattern.remove(p_pass)
                    if match2:
                        self.device.sendMsg("sol.sh\r\n")
                        time.sleep(2)
                        self.device.sendMsg('\r\n')
                        message_pattern = 'CTRL-l + b : Send Break'
                        exit_cmd = 'exit()'
                        message = self.device.readUntil(message_pattern, timeout=1200)
                        if message:
                            time.sleep(300)
                            self.device.sendMsg('\r\n')
                            self.device.sendMsg("{}\r\n".format(exit_cmd))
                            deviceObj.getPrompt(centos_mode)
                            log.info("Successfully exit sdk mode")
                            self.wpl_raiseException('GB temp failed, please see output!')
            if len(pattern) == 0:
                self.wpl_log_info('Successfully Start_high_power_and_verify_sensor_test.')
            else:
                self.device.sendMsg("sol.sh\r\n")
                time.sleep(2)
                self.device.sendMsg('\r\n')
                message_pattern = 'CTRL-l + b : Send Break'
                exit_cmd = 'exit()'
                message = self.device.readUntil(message_pattern, timeout=300)
                if message:
                    time.sleep(300)
                    self.device.sendMsg('\r\n')
                    self.device.sendMsg("{}\r\n".format(exit_cmd))
                    deviceObj.getPrompt(centos_mode)
                    log.info("Successfully exit sdk mode")
                self.wpl_raiseException('GB temp failed, please see output!')

    @logThis
    def check_sys_before_and_after_log_test(self, toolName, option, pattern, path, param):
        if param == 'True':
            CommonLib.switch_to_openbmc()
            path = '/mnt/data1/BMC_Diag/utility/stress/syslog'
            toolName = './cel_syslog -c -l'
            self.wpl_transmit('cd ' + path)
            cmd = toolName + option
            output = self.wpl_execute_cmd(cmd, mode=openbmc_mode, timeout=60)
        else:
            self.wpl_transmit('cd '+path)
            cmd = toolName + option
            output = self.wpl_execute_cmd(cmd, mode='centos', timeout=60)
        passcount = 0
        pattern = [
            r'Save System Logs.*PASS',
            r'Clean System Logs.*PASS'
        ]
        for line in output.splitlines():
            line = line.strip()
            for i in range(0, len(pattern)):
                match = re.search(pattern[i], line, re.I)
                if match:
                    passcount+=1

        if passcount == len(pattern):
            self.wpl_log_success('Tested Pass check_sys_before_or_after_log_test with command %s.' % cmd)
        else:
            self.wpl_raiseException("Failed check_sys_before_or_after_log_test with command %s." % cmd)
    @logThis
    def  verify_bmc_i2c_tool_option_l_test(self, toolName, option, keywords_pattern='none', pass_pattern='none', path=BMC_DIAG_TOOL_PATH):
        devicename = os.environ.get("deviceName", "")
        if 'minipack2_dc' in devicename.lower():
            if (('pim3' in option) or ('pim4' in option) or ('pim5' in option) or ('pim6' in option)) and toolName == 'cel-i2c-test':
                return
        output = self.EXEC_bmc_diag_tool_command(toolName, option, path)
        keywords_pattern = [
            'error',
            'fail'
        ]
        fail_count = 0
        for line in output.splitlines():
            line = line.strip()
            for i in range(0, len(keywords_pattern)):
                match = re.search(keywords_pattern[i], line, re.I)
                if match:
                    fail_count += 1
        if fail_count:
            self.wpl_log_fail('Exiting verify_bmc_i2c_tool_option_l_test with result FAIL')
            self.wpl_raiseException("Failure while testing DIAG tool '%s' with Option: '%s'" % (toolName, option))
        else:
            self.wpl_log_success('verify_bmc_i2c_tool_option_l_test for DIAG tool - %s is PASSED\n' % toolName)

    @logThis
    def verify_clean_log_for_system_test(self, toolName, option, pattern, path, param):
        if param == 'False':
            self.wpl_transmit('cd '+path)
            command = toolName + ' ' + option
            output = self.wpl_execute(command, mode='centos', timeout=600)
            pattern = [
                r'Save System Logs.*?PASS',
                r'Clean System Logs.*?PASS',
                r'Check PCIe Bus Error.*?PASS',
                r'Check PCIe Error.*?PASS',
                r'Check \(Un\)Correctable Error.*?PASS',
                r'Check mcelog.*?PASS'
                ]
        else:
            CommonLib.switch_to_centos()
            path = '/usr/local/cls_diag/utility/stress/syslog'
            option = ' -l log/PCIE_sys_after -c'
            command = toolName + ' ' + option
            output = self.wpl_execute(command, mode=openbmc_mode, timeout=600)
            pattern = [
                r'Save System Logs.*?PASS',
                r'Clean System Logs.*?PASS',
        ]
        passcount = 0
        for line in output.splitlines():
            line = line.strip()
            for i in range(0,len(pattern)):
                match = re.search(pattern[i], line, re.I)
                if match:
                    passcount += 1
        self.wpl_log_debug('//////passcount=%s//////' % passcount)
        if passcount == len(pattern):
            self.wpl_log_success('verify_clean_log_for_system_test test result for DIAG tool - %s is PASSED\n' % toolName)
        else:
            self.wpl_log_fail('Exiting verify_clean_log_for_system_test with result FAIL')
            self.wpl_raiseException("Failure while testing DIAG tool '%s' with Option: '%s'" % (toolName, option))

    @logThis
    def verify_befor_diag_version(self, toolName, option, keywords, pass_pattern, path):
        if path:
            self.wpl_transmit('cd '+ path)
        output = self.wpl_execute_cmd(toolName + option, mode=centos_mode, timeout=60)
        fail_count = 0
        for line in output.splitlines():
            line = line.strip()
            match = re.search('error|fail', line, re.I)
            if match:
                fail_count += 1
        if fail_count:
            self.wpl_raiseException('check diag version failed, please check output!')
        else:
            self.wpl_log_success("check diag version Successfully.")

    @logThis
    def verify_check_cpld_main_info_func(self, toolName, option1, option2, path):

        if path:
            cmd = 'cd ' + path
            self.wpl_transmit(cmd)

        cpld_list = [
            'FCM_B_CPLD',
            'FCM_T_CPLD',
            'SCM_CPLD',
            'SMB_CPLD',
            'PDB_L_CPLD',
            'PDB_R_CPLD'
        ]
        below_str1 = ' -s 0x04'
        below_str2 = ' -s 0x04 -d 0xaa'
        for temp in cpld_list:
            self.wpl_log_info("Current cpld temp is %s " % temp)
            command1 = './' + toolName + option1 + ' ' + temp + below_str1
            output1 = self.wpl_execute(command1, mode=openbmc_mode, timeout=30)
            passcount = 0
            for line in output1.splitlines():
                line = line.strip()
                match1 = re.search('^0x.*', line)
                if match1:
                    passcount += 1
            if passcount:
                self.wpl_log_info('cpld temp %s get main info correct' % temp)
                passcount == 0
                command2 = './' + toolName + option2 + ' ' + temp + below_str2
                self.wpl_transmit(command2)
                time.sleep(2)
                output2 = self.wpl_execute(command1, mode=openbmc_mode, timeout=30)
                if '0xaa' in output2:
                    self.wpl_log_info('cpld temp %s modify main info correct' % temp)
                else:
                    self.wpl_raiseException('cpld temp %s modify main info incorrect' % temp)

            else:
                self.wpl_raiseException('cpld temp %s get main info incorrect' % temp)

    @logThis
    def verify_client_ipv4_and_ipv6(self, ipv4, ipv6):

        ifconfig = 'ifconfig eth0'
        output = self.wpl_execute_cmd(ifconfig, mode=centos_mode, timeout=60)
        passcount = 0
        inet_list = []
        for line in output.splitlines():
            line = line.strip()
            if 'inet' in line:
                passcount += 1
                inet_list.append(line)
        if passcount >= 2:
            self.wpl_log_success("eth0 ipv4 and ipv6 already set.")
        elif passcount == 1:
            if 'inet6' in inet_list[0]:
                self.wpl_transmit(ipv4)
            else:
                self.wpl_log_info('%s' % inet_list[0])
                self.wpl_raiseException('set ipv4 failed, pls retry')
        elif passcount == 0:
            self.wpl_transmit(ipv4)
            time.sleep(5)
            self.wpl_transmit(ipv6)

    @logThis
    def verify_pim_fan_eeprom_update(self, toolName, option, pattern, path):

        if path:
            cmd = 'cd ' + path
            self.wpl_transmit(cmd)

        command = toolName + option
        output = self.wpl_execute_cmd(command, mode="openbmc", timeout=60)
        pattern = 'EEPROM Update Successfully.*?PASS'
        count = 0
        for line in output.splitlines():
            line = line.strip()
            match = re.search(pattern, line)
            if match:
                count += 1
        if count:
            self.wpl_log_info('verify pim fan eeprom update pass')
        else:
            self.wpl_raiseException('verify pim fan eeprom update failed')

    @logThis
    def reset_the_whole_system(self):

        cmd = 'wedge_power.sh reset -s'

        self.device.sendMsg(cmd+'\n')

    @logThis
    def power_system(self):
        CommonLib.switch_to_openbmc()
        time.sleep(5)
        cmd = 'wedge_power.sh reset -s'
        booting_msg = 'Starting kernel'
        self.wpl_transmit(cmd)
        output = self.wpl_receive(booting_msg, timeout=Const.BOOTING_TIME)
        time.sleep(180)
        self.wpl_getPrompt(Const.BOOT_MODE_OPENBMC, timeout=Const.BOOTING_TIME)
        self.wpl_getPrompt(Const.BOOT_MODE_CENTOS, timeout=Const.BOOTING_TIME)
        self.wpl_getPrompt(Const.BOOT_MODE_OPENBMC)
        time.sleep(10)
        return output

    @logThis
    def retry_centos(self):
        time.sleep(5)
        CommonLib.switch_to_openbmc()
        time.sleep(180)
        CommonLib.switch_to_centos()
        time.sleep(5)
        self.wpl_transmit("\n")
        #output = self.wpl_execute("\n", mode="centos", timeout=30)
        output = self.wpl_receive("localhost", timeout=Const.BOOTING_TIME)
        if 'localhost' in output:
            CommonLib.switch_to_openbmc()
            self.wpl_log_info('the unit can enter into os.')
        else:
            CommonLib.switch_to_openbmc()
        return output

    @logThis
    def power_reset_system(self):
        CommonLib.switch_to_openbmc()
        time.sleep(5)
        cmd = 'wedge_power.sh reset'
        booting_msg = 'Power reset microserver'
        self.wpl_transmit(cmd)
        output = self.wpl_receive(booting_msg, timeout=Const.BOOTING_TIME)
        time.sleep(3)
        self.wpl_getPrompt(Const.BOOT_MODE_CENTOS, timeout=Const.BOOTING_TIME)
        self.wpl_getPrompt(Const.BOOT_MODE_OPENBMC)
        time.sleep(10)
        return output

    @logThis
    def dmesg_log_check(self, toolName, option, keywords_pattern='none', pass_pattern='none', path=BMC_DIAG_TOOL_PATH, prefix="./"):
        passCount = 0
        time.sleep(3)
        error_count = 0
        ##1. check tpm.
        patternNum = len(keywords_pattern)
        self.wpl_log_debug('option = %s' % option)
        output = self.EXEC_bmc_diag_tool_command(toolName, option, path, prefix)
        self.wpl_log_debug('output = %s' % output)
        pass_p = []
        pattern_all = []
        for line in output.splitlines():
            line = line.strip()
            for i in range(0, patternNum):
                p_pass = keywords_pattern[i] + pass_pattern
                pattern_all.append(p_pass)
                match = re.search(p_pass, line)
                if match:
                    passCount += 1
                    pass_p.append(p_pass)
        mismatch_pattern = set(pattern_all) - set(pass_p)
        self.wpl_log_debug('passCount = %s' % passCount)
        self.wpl_log_debug('patternNum = %s' % patternNum)
        if not mismatch_pattern:
            self.wpl_log_success(
                'Run TPM check result for DIAG tool - %s is PASSED\n' % toolName)
        else:
            self.wpl_log_fail('Tpm test FAIL, mismatch items: [{}]'.format(
                CommonLib.get_readable_strings(mismatch_pattern)))

            ##2. run dmesg info.
            p1 = '^\d'
            cmd1 = "dmesg | grep -i 'error'| wc -l"
            cmd2 = "dmesg | grep -i 'dumping'| wc -l"
            cmd3 = "dmesg | grep -i 'error'"
            cmd4 = "dmesg | grep -i 'dumping'"
            cmd5 = "dmesg | grep 'tpm'"
            cmd6 = "ls /dev/tpmrm0"
            cmd = [cmd1, cmd2]
            error_cmd = [cmd3, cmd4, cmd5, cmd6]
            for line in cmd:
                output += self.wpl_execute(line, mode=openbmc_mode, timeout=60)
            for line in output.splitlines():
                line = line.strip()
                match = re.search(p1, line)
                if match:
                    error_count += int(match.group(0))
            if error_count > 0:
                self.wpl_log_info('error_count is %s' % str(error_count))
                for line in error_cmd:
                    self.wpl_execute(line, mode=openbmc_mode, timeout=60)
                self.wpl_log_fail('dmesg info found error info.')
            self.wpl_raiseException("Failure while testing DIAG tool '%s' with Option: '%s'" % (toolName, option))

