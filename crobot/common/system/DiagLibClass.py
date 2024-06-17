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
import pathlib
import sys
import re
from Decorator import *
import time
import pexpect
from Diag_OS_variable import *
import parserDIAGLibs
from DiagLib import *
import CommonLib
import Const
from InitFrameworkLib import *
from Utils import NumPlus
sys.path.append("..")
from sdk import *
import Logger as log
from datetime import datetime

BOOTING_TIME=600


class DiagLibClass(DiagLib):
    def __init__(self, device):
        DiagLib.__init__(self, device)
        self.pwr_supply_type = '0'
        self.bmc_version = '0'
        self.bmc_update_max_cycles = '0'
        self.bmc_update_loop_count = '0'
        self.bios_version = '0'
        self.bios_update_max_cycles = '0'
        self.bios_update_loop_count = '0'
        self.bic_version = '0'
        self.bic_update_max_cycles = '0'
        self.bic_update_loop_count = '0'
        self.old_syscpld_version = '0'
        self.old_pwrcpld_version = '0'
        self.old_scmcpld_version = '0'
        self.old_fcmcpld_version = '0'
        self.syscpld_version = '0'
        self.pwrcpld_version = '0'
        self.scmcpld_version = '0'
        self.fcmcpld_version = '0'
        self.cpld_update_max_cycles = '0'
        self.cpld_update_loop_count = '0'
        self.fpga1_version = '0'
        self.fpga2_version = '0'
        self.fpga_update_max_cycles = '0'
        self.fpga_update_loop_count = '0'
        self.fpga_stress_time = '0'
        self.ipmi_stress_time = '0'
        self.ipmi_stress_cycles = '0'
        self.cpu_stress_time = '0'
        self.openbmc_utility_stress_time = '0'
        self.openbmc_utility_stress_cycles = '0'
        self.COMe_memory_stress_time = '0'
        self.nvme_stress_time = '0'
        self.eeprom_stress_time = '0'
        self.bmc_cpu_link_stress_time = '0'
        self.openbmc_memory_stress_cycles = '0'
        self.openbmc_memory_stress_time = '0'
        self.tpm_access_stress_time = '0'
        self.tpm_access_stress_cycles = '0'
        self.serdes_max_cycles = '0'
        self.python3_path = ''
        self.snake_traffic_test_time = '0'
        self.board_type = '0'
        self.re_init_cycles = '0'
        self.re_init_stress_time = '0'
        self.port_enable_disable_stress_cycles = '0'
        self.port_enable_disable_stress_time = '0'
        self.port_linkup_stress_cycles = '0'
        self.port_linkup_stress_time = '0'
        self.auto_load_script_stress_time = '0'
        self.sensor_reading_max_cycles = '0'
        self.eloop_init = '0'


#######################################################################################################################
# Function Name: init_system_test
# Date         : 14th May 2020
# Author       : TK NG<tikng@celestica.com>
#
# Procedure Revision Details:
#   Version : 1.0  - Initial Draft  - by TK NG<tikng@celestica.com>
#######################################################################################################################
    def init_system_test(self):
        self.wpl_log_debug('Entering procedure init_system_test with args : %s' % (str(locals())))
        self.wpl_getPrompt(openbmc_mode)
        cmd = ('cd ' + BMC_DIAG_TOOL_PATH)
        self.wpl_transmit(cmd)

        devicename = os.environ.get("deviceName", "")
        if 'wedge400_' in devicename.lower():
            self.power_type_check_w400()
            return

        # Note: Minipack2 only supports psu and no pem.
        # check for psu1 ~ psu4 presence
        for i in range(1,5):
            cmd1 = ('psu-util psu%s --get_psu_info' %(str(i)))
            output1 = self.wpl_execute(cmd1, mode=openbmc_mode, timeout=30)
            pattern1 = r'MFR_'
            match1 = re.search(pattern1, output1, re.IGNORECASE)
            if match1:
                self.wpl_log_info("Detected PSU%s present." %(str(i)))
                if 'wedge400c_rsp' in devicename.lower() or 'minipack2_rsp' in devicename.lower():
                    cmd2 = './cel-diag-init -r'
                elif 'wedge400c_dc' in devicename.lower() or 'minipack2_dc' in devicename.lower():
                    cmd2 = './cel-diag-init -c'
                else:
                    cmd2 = './cel-diag-init -a'
                self.wpl_log_info(cmd2)
                self.wpl_transmit(cmd2)
                self.wpl_getPrompt(openbmc_mode)
                self.pwr_supply_type = 'psu'
                self.wpl_log_success("Successfully init_system_test.")
                return

        # no psu found, check for pem1 ~ pem2 presence
        pem1_found = False
        pem2_found = False
        for i in range(1,3):
            cmd3 = ('pem-util pem%s --get_pem_info' %(str(i)))
            output3 = self.wpl_execute(cmd3, mode=openbmc_mode, timeout=30)
            pattern3 = (r'PEM%s_' %(str(i)))
            match3 = re.search(pattern3, output3, re.IGNORECASE)
            if match3:
                if i == 1:
                    pem1_found = True
                    self.wpl_log_info("Detected PEM1 present.")
                else:
                    pem2_found = True
                    self.wpl_log_info("Detected PEM2 present.")

        if (pem1_found == True) or (pem2_found == True):
            self.wpl_log_info("This unit uses PEM")
            if 'wedge400c_rsp' in devicename.lower():
                cmd4 = './cel-diag-init -m'
            else:
                cmd4 = './cel-diag-init -p'
            self.wpl_log_info(cmd4)
            self.wpl_transmit(cmd4)
            self.pwr_supply_type = 'pem'

            if pem1_found == True:
                self.wpl_log_fail('PEM1 detected. System should not be installed with PEM1.')
                self.wpl_raiseException("Failure while init_system_test.")
        else:
            self.wpl_log_fail('Unable to detect PSU or PEM presence !')
            self.wpl_raiseException("Failure while init_system_test.")

        self.wpl_getPrompt(openbmc_mode)
        self.wpl_log_success("Successfully init_system_test.")


#######################################################################################################################
# Function Name: switch_to_centos_and_go_to_diag_tool
# Date         : 12nd February 2020
# Author       : Phawit P. <Phaphan@celestica.com>
#
# Procedure Revision Details:
#   Version : 1.0  - Initial Draft  - by Phawit P. <Phaphan@celestica.com>
#######################################################################################################################
    def switch_to_centos_and_go_to_diag_tool(self, logFilename='None'):
        self.wpl_log_debug('Entering procedure switch_to_centos_and_go_to_diag_tool\n')
        cmd = 'cd ' + DIAG_TOOL_PATH
        CommonLib.switch_to_centos(logFilename)
        self.wpl_transmit(cmd)


#######################################################################################################################
# Function Name: switch_to_openbmc_and_check_tool
# Date         : 12nd February 2020
# Author       : Phawit P. <Phaphan@celestica.com>
#
# Procedure Revision Details:
#   Version : 1.0  - Initial Draft  - by Phawit P. <Phaphan@celestica.com>
#######################################################################################################################
    def switch_to_openbmc_and_check_tool(self, logFilename='None'):
        self.wpl_log_debug('Entering procedure switch_to_openbmc_and_check_tool\n')
        CommonLib.switch_to_openbmc(logFilename)
        self.check_bmc_diag_tool()


#######################################################################################################################
# Function Name: check_test_directories
# Date         : 14th May 2020
# Author       : TK NG<tikng@celestica.com>
#
# Procedure Revision Details:
#   Version : 1.0  - Initial Draft  - by TK NG<tikng@celestica.com>
#######################################################################################################################
    def check_test_directories(self):
        self.wpl_log_debug('Entering procedure check_test_directories\n')

        if CommonLib.check_file_exist(BMC_DIAG_TOOL_PATH, openbmc_mode) == False:
            CommonLib.mount_data(BLK_DEV_PATH, BMC_BLK_MOUNT_PATH, openbmc_mode)

        CommonLib.create_dir(BMC_TEST_DIR_AUTOMATION, openbmc_mode)
        CommonLib.create_dir(BMC_TEST_DIR_AUTOMATION_SYS_LOG, openbmc_mode)
        CommonLib.create_dir(BMC_TEST_DIR_AUTOMATION_LOGFILE, openbmc_mode)
        CommonLib.create_dir(BMC_TEST_DIR_AUTOMATION_BIC, openbmc_mode)
        CommonLib.create_dir(BMC_TEST_DIR_AUTOMATION_BIOS, openbmc_mode)
        CommonLib.create_dir(BMC_TEST_DIR_AUTOMATION_BMC, openbmc_mode)
        CommonLib.create_dir(BMC_TEST_DIR_AUTOMATION_DIAG, openbmc_mode)
        CommonLib.create_dir(BMC_TEST_DIR_AUTOMATION_CPLD, openbmc_mode)
        CommonLib.create_dir(BMC_TEST_DIR_AUTOMATION_FPGA, openbmc_mode)
        CommonLib.create_dir(BMC_TEST_DIR_AUTOMATION_OOB, openbmc_mode)

        ##add fw vrsion check
        cmd = 'cd ' + BMC_DIAG_TOOL_PATH
        self.wpl_transmit(cmd)
        cmd = './cel-software-test -v'
        self.wpl_execute(cmd, mode=openbmc_mode, timeout=60)
        self.wpl_log_success("Successfully check_test_directories.")


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
    def EXEC_diag_tool_command(self, toolName, option, path=DIAG_TOOL_PATH, time_out=600):
        cmd = path + toolName + ' ' + option
        self.wpl_log_debug("command = %s" %(cmd))
        return self.wpl_execute(cmd, mode='centos', timeout=time_out)


#######################################################################################################################
# Function Name: EXEC_bmc_diag_tool_command
# Date         : 12th February 2020
# Author       : Phawit P. <Phaphan@celestica.com>
#
# Procedure Revision Details:
#   Version : 1.0  - Initial Draft  - by Phawit P. <Phaphan@celestica.com>
#######################################################################################################################
    def EXEC_bmc_diag_tool_command(self, toolName, option, path=BMC_DIAG_TOOL_PATH):
        cmd = ('cd ' + path)
        self.wpl_log_debug("command = %s" %(cmd))
        self.wpl_getPrompt("openbmc", 600)
        self.wpl_transmit(cmd)

        cmd = './' + toolName + ' ' + option
        self.wpl_log_debug("command = %s" %(cmd))
        return self.wpl_execute(cmd, mode=openbmc_mode, timeout=600)


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
# Function Name: verify_option_diag_tool_simple_dict
# Date         : January 27th 2020
# Author       : Phawit P. <Phaphan@celestica.com>
#
# Procedure Revision Details:
#   Version : 1.0  - Initial Draft  - by Phawit P. <Phaphan@celestica.com>
#######################################################################################################################
    def verify_option_diag_tool_simple_dict(self, inputArray, toolName, option):
        self.wpl_log_debug('Entering procedure verify_option_diag_tool_simple_dict with args : %s' %(str(locals())))
        cmd = 'cd ' + DIAG_TOOL_PATH
        self.wpl_getPrompt("centos", 600)
        self.wpl_transmit(cmd)
        errCount = 0
        output = self.EXEC_diag_tool_command(toolName, option)
        if (option == '-h' or option == '--help'):
            parsedOutput = parserDIAGLibs.PARSE_diagtool_help(output)
        elif (option == '-i' or option == '--info'):
            parsedOutput = parserDIAGLibs.PARSE_diagtool_info(output)
        elif (option == '-S' or option == '--show'):
            parsedOutput = parserDIAGLibs.PARSE_diagtool_show(output)
        elif (option == '-l' or option == '--list'):
            parsedOutput = parserDIAGLibs.PARSE_diagtool_list(output)
        errCount += CommonLib.compare_input_dict_to_parsed(parsedOutput, inputArray)
        if errCount:
            self.wpl_log_fail('Exiting verify_option_diag_tool_simple_dict with result FAIL')
            self.wpl_raiseException("Failure while testing DIAG tool '%s' with Option: '%s'" %(toolName, option))
        else:
            self.wpl_log_success('Option: %s test result for DIAG tool - %s is PASSED\n' %(option, toolName))


#######################################################################################################################
# Function Name: verify_diag_tool_simple_dict
# Date         : January 27th 2020
# Author       : Phawit P. <Phaphan@celestica.com>
#
# Procedure Revision Details:
#   Version : 1.0  - Initial Draft  - by Phawit P. <Phaphan@celestica.com>
#######################################################################################################################
    def verify_diag_tool_simple_dict(self, toolName, option, keywords='none', pattern='none', data='none', port='none', color='none'):
        self.wpl_log_debug('Entering procedure verify_diag_tool_simple_dict with args : %s' %(str(locals())))
        cmd = 'cd ' + DIAG_TOOL_PATH
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

        if keywords == 'none':
            passCount = self.verify_diag_tool_other_option(output, option, pattern, data, port)
            self.wpl_log_debug('passCount = %d' % passCount)
        for line in output.splitlines():
            line = line.strip()
            match = re.search(p_pass, line, re.IGNORECASE)
            if match:
                passCount += 1
        if passCount:
            self.wpl_log_success('verify_diag_tool_simple_dict test result for DIAG tool - %s is PASSED\n' %toolName)
        else:
            self.wpl_log_fail('Exiting verify_diag_tool_simple_dict with result FAIL')
            self.wpl_raiseException("Failure while testing DIAG tool '%s' with Option: '%s'" %(toolName,option))


######################################################################################################################
# Function Name: verify_diag_tool_parse_output_dict
# Date         : January 27th 2020
# Author       : Phawit P. <Phaphan@celestica.com>
#
# Procedure Revision Details:
#   Version : 1.0  - Initial Draft  - by Phawit P. <Phaphan@celestica.com>
######################################################################################################################
    def verify_diag_tool_parse_output_dict(self, toolName, option, keywords='none', pattern='none', data='none', port='none', color='none'):
        self.wpl_log_debug('Entering procedure verify_diag_tool_simple_dict with args : %s' %(str(locals())))
        cmd = 'cd ' + DIAG_TOOL_PATH
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
                        match = re.search(i, line, re.IGNORECASE)
                        if match:
                            found = True
                            match1 = re.search(str_passed, line, re.IGNORECASE)
                            if match1:
                                replace_str = str_passed
                            break
                else:
                    match = re.search(pattern, line, re.IGNORECASE)
                    if match:
                        found = True
                        match1 = re.search(str_passed, line, re.IGNORECASE)
                        if match1:
                            replace_str = str_passed

                if found == False:
                    if re.search(str_ok, line, re.IGNORECASE):
                        # if only "ok" string is shown on the line,
                        # then add it to the previous line
                        output1 += (str_ok + "\r\n")
                        continue
                    elif re.search(str_passed, line, re.IGNORECASE):
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
                        if re.search("ok", line, re.IGNORECASE):
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
            match = re.search(p_pass, line, re.IGNORECASE)
            if match:
                passCount += 1
        if passCount:
            self.wpl_log_success('verify_diag_tool_simple_dict test result for DIAG tool - %s is PASSED\n' %toolName)
        else:
            self.wpl_log_fail('Exiting verify_diag_tool_simple_dict with result FAIL')
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
        expCount=0
        newpattern = pattern
        if data != 'none':
            if type(newpattern) == list:
                for i in range(0, len(newpattern)):
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
                    match = re.search(i, line, re.IGNORECASE)
                    if match:
                        chkCount += 1
            else:
                match = re.search(newpattern, line, re.IGNORECASE)
                if match:
                    chkCount += 1
        if (option == '-K' or option == '--check'):
            expCount=18
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
        if chkCount == expCount:
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
        cmd = UTILITY_TOOL_PATH + toolName + ' ' + module + ' r ' + get_reg
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
    def execute_cpld_set_reg_command(self, toolName, module, set_reg, set_value, test_name='None', toolPath=UTILITY_TOOL_PATH):
        self.wpl_log_debug('Entering procedure execute_cpld_set_reg_command : %s\n'%(str(locals())))
        if test_name == 'None':
            test_name = 'execute_cpld_set_reg_command'
        cmd = toolPath + toolName + ' ' + module + ' w ' + set_reg + ' ' + set_value
        output = self.wpl_execute(cmd)
        time.sleep(1)
        parsedOutput = parserDIAGLibs.PARSE_get_cpld_output(output)
        self.wpl_log_debug('result = %s' % parsedOutput)
        output_value = ('0x' + parsedOutput)
        if output_value == set_value:
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
        p2 = 'BMC will switch to '+region+' after \d{1,2} seconds...'
        passCount = 0
        option = '-b bmc -r ' + region
        output = self.EXEC_bmc_diag_tool_command(toolName, option)
        self.wpl_log_debug(output)
        for line in output.splitlines():
            line = line.strip()
            match = re.search(p1, line, re.IGNORECASE)
            if match:
                passCount += 1
            match = re.search(p2, line, re.IGNORECASE)
            if match:
                passCount += 1
                time.sleep(10)
                self.wpl_flush()
                self.wpl_receive('Starting kernel ...', timeout=90)
                self.wpl_getPrompt('openbmc', timeout=BOOTING_TIME)
                time.sleep(35)
                cmd = boot_info_util + ' ' + 'bmc'
                var_pattern = bmcModePattern
                output1 = self.wpl_execute(cmd, mode="openbmc", timeout=30)
                for line in output1.splitlines():
                    line = line.strip()
                    match1 = re.search(var_pattern, line, re.IGNORECASE)
                    if match1:
                        getCurrentMode = match1.group(1)
                        if getCurrentMode.lower() == region:
                            self.wpl_log_success("Successfully get BMC mode is [%s]" % region)
                        else:
                            passCount -= 1
                            self.wpl_log_fail("Failed get BMC mode is [%s]" % getCurrentMode)
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
        cmd = toolName + ' ' +  img_path + '/' + bmc_image + ' ' + flash_device
        self.wpl_log_debug('cammand = %s' % cmd)
        self.wpl_execute(cmd, mode="openbmc", timeout=600)
        self.wpl_getPrompt("openbmc", 60)
        output = self.wpl_execute("echo $?", mode="openbmc", timeout=30)
        self.wpl_log_debug(output)
        for line in output.splitlines():
            line = line.strip()
            match = re.search('^0$', line)
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
    def check_bmc_version(self, bmc_version):
        self.wpl_log_debug('Entering procedure check_bmc_version with args : %s' %(str(locals())))
        passCount=0
        # e.g. OpenBMC Release wedge400-v2.7
        p1 = 'OpenBMC Release'
        cmd = 'cat /etc/issue'
        output = self.wpl_execute(cmd, mode="openbmc")
        for line in output.splitlines():
            line = line.strip()
            match = re.search(p1, line, re.IGNORECASE)
            if match:
                if 'v' in line:
                    slist = line.split('v')
                    version_str = str(slist[1])
                else:
                    ## for daily build version(OpenBMC Release wedge400-2a8a5376337-CLS_main)
                    slist = line.split('-')
                    version_str = str(slist[1]) + '-' + str(slist[2])
                if version_str == bmc_version:
                    passCount += 1
                    break
        if passCount:
            self.wpl_log_success("Successfully checked BMC version: \'%s\'"% bmc_version)
        else:
            self.wpl_raiseException("ERR_01_001_02: Failed checking BMC version")


#######################################################################################################################
# Function Name: spi_util_exec
# Date         : 14th February 2020
# Author       : Phawit P. <Phaphan@celestica.com>
#
# Procedure Revision Details:
#   Version : 1.0  - Initial Draft  - by Phawit P. <Phaphan@celestica.com>
#######################################################################################################################
    def spi_util_exec(self, toolName, opt, spiNum, dev, check_pattern, imageFile='none', readFile='none', img_path=FW_IMG_PATH, tool_path=SPI_UTIL_PATH, logFile='None'):
        self.wpl_log_debug('Entering procedure spi_util_exec with args : %s' %(str(locals())))
        passCount = 0
        patternNum = len(check_pattern)
        cmd = 'cd ' + img_path
        self.wpl_getPrompt("openbmc", 600)
        self.wpl_transmit(cmd)
        cmd = tool_path + toolName + ' ' +  opt + ' ' + spiNum + ' ' + dev + ' '
        if opt == 'write':
            cmd += imageFile
        if opt == 'read':
            cmd += readFile
        self.wpl_log_debug('command = %s' % cmd)
        output = self.wpl_execute(cmd, mode='openbmc', timeout=1800)

        if logFile != 'None':
            self.wpl_send_output_to_log_file(output, logFile)

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
                        match = re.search(i, line, re.IGNORECASE)
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
                    match = re.search(check_pattern, line, re.IGNORECASE)
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
                match = re.search(check_pattern[i], line, re.IGNORECASE)
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
        self.wpl_log_debug('Entering procedure switch_and_check_bios_by_diag_cammand with args : %s' %(str(locals())))
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
            match = re.search(p0, line, re.IGNORECASE)
            if match:
                passCount = 1
                break
            match = re.search(p1, line, re.IGNORECASE)
            if match:
                passCount += 1
            match = re.search(p2, line, re.IGNORECASE)
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
            match = re.search(region, line, re.IGNORECASE)
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
            match = re.search(p1, line, re.IGNORECASE)
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
        time.sleep(3)
        self.wpl_execute(cmd, mode='centos')
        output = self.EXEC_diag_tool_command(toolName, option)
        self.wpl_log_debug('output = %s' % output)
        for line in output.splitlines():
            line = line.strip()
            match = re.search(pattern, line, re.IGNORECASE)
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
    def fw_util_exec(self, toolName, fru, opt, dev, image, check_pattern, img_path=FW_IMG_PATH, tool_path=BMC_DIAG_TOOL_PATH, exec_mode=default_mode, logFile='None'):
        self.wpl_log_debug('Entering procedure fw_util_exec with args : %s' %(str(locals())))
        passCount = 0
        patternNum = len(check_pattern)
        cmd = 'cd ' + img_path
        self.wpl_getPrompt(exec_mode, 600)
        self.wpl_transmit(cmd)
        cmd = tool_path + toolName + ' ' + fru + ' --' + opt + ' ' + dev + ' ' + img_path + '/' + image
        self.wpl_log_debug('command = %s' % cmd)
        output = self.wpl_execute(cmd, mode=exec_mode, timeout=1800)

        for line in output.splitlines():
            line = line.strip()
            for i in range(0, patternNum):
                match = re.search(check_pattern[i], line, re.IGNORECASE)
                if match:
                    passCount += 1

        if logFile != 'None':
            self.wpl_send_output_to_log_file(output, logFile)

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
        sdk_prompt = MINIPACK2_SDK_PROMPT
        self.wpl_receive(sdk_prompt, timeout=300)
        cmd='pciephy fw version'
        self.wpl_transmit(cmd)
        output = self.wpl_receive(sdk_prompt, timeout=300)
        self.wpl_log_debug('output = %s' % output)
        for line in output.splitlines():
            line = line.strip()
            match = re.search(pattern, line, re.IGNORECASE)
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
            match = re.search(p1, line, re.IGNORECASE)
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
            match = re.search(pattern, line, re.IGNORECASE)
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
    def update_tool_exec(self, toolName, image, option, dev, check_pattern, img_path, toolPath, logFile='None'):
        self.wpl_log_debug('Entering procedure update_tool_exec with args : %s' %(str(locals())))
        passCount = 0
        patternNum = len(check_pattern)
        cmd = 'cd ' + img_path
        self.wpl_getPrompt("openbmc", 600)
        self.wpl_transmit(cmd)
        cmd = toolPath + toolName + ' ' + image + ' ' + option
        self.wpl_log_debug('cammand = %s' % cmd)
        output = self.wpl_execute(cmd, mode='openbmc', timeout=1800)
        for line in output.splitlines():
            line = line.strip()
            for i in range(0, patternNum):
                match = re.search(check_pattern[i], line, re.IGNORECASE)
                if match:
                    passCount += 1

        if logFile != 'None':
            self.wpl_send_output_to_log_file(output, logFile)

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
# Function Name: verify_bmc_diag_tool_simple_dict
# Date         : January 27th 2020
# Author       : Phawit P. <Phaphan@celestica.com>
#
# Procedure Revision Details:
#   Version : 1.0  - Initial Draft  - by Phawit P. <Phaphan@celestica.com>
#######################################################################################################################
    def verify_bmc_diag_tool_simple_dict(self, toolName, option, keywords_pattern='none', pass_pattern='none', path=BMC_DIAG_TOOL_PATH):
        self.wpl_log_debug('Entering procedure verify_bmc_diag_tool_simple_dict with args : %s' %(str(locals())))
        passCount = 0
        new_option = option
        patternNum = len(keywords_pattern)
        self.wpl_log_debug('new_option = %s' % new_option)
        output = self.EXEC_bmc_diag_tool_command(toolName, new_option, path)
        self.wpl_log_debug('output = %s' % output)
        for line in output.splitlines():
            line = line.strip()
            for i in range(0, patternNum):
                p_pass = keywords_pattern[i] + pass_pattern
                # self.wpl_log_debug('p_pass = %s' % p_pass)
                match = re.search(p_pass, line, re.IGNORECASE)
                if match:
                    passCount += 1
        self.wpl_log_debug('passCount = %s' % passCount)
        self.wpl_log_debug('patternNum = %s' % patternNum)
        if passCount == patternNum:
            self.wpl_log_success('verify_diag_tool_simple_dict test result for DIAG tool - %s is PASSED\n' %toolName)
        else:
            self.wpl_log_fail('Exiting verify_diag_tool_simple_dict with result FAIL')
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
            self.wpl_log_debug('line = %s'%(line))
            match = re.search(p1, line)
            if match:
                val_str = line
                break
        return val_str


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
        if new_read == data:
            self.wpl_log_success('verify_device_write_read test result for DIAG tool - %s is PASSED\n' %toolName)
        else:
            self.wpl_log_fail('Exiting verify_device_write_read with result FAIL')
            self.wpl_raiseException("Failure while testing DIAG tool '%s'" %(toolName))


#######################################################################################################################
# Function Name: get_current_bmc_version
# Date         : 14th May 2020
# Author       : TK NG<tikng@celestica.com>
#
# Procedure Revision Details:
#   Version : 1.0  - Initial Draft  - by TK NG<tikng@celestica.com>
#######################################################################################################################
    def get_current_bmc_version(self):
        self.wpl_log_debug('Entering procedure get_current_bmc_version with args : %s' %(str(locals())))
        current_bmc_version=''
        p1 = 'OpenBMC Release'
        cmd = 'cat /etc/issue'
        output = self.wpl_execute(cmd, mode="openbmc")
        for line in output.splitlines():
            line = line.strip()
            match = re.search(p1, line, re.IGNORECASE)
            if match:
                current_bmc_version = self.extract_bmc_fw_version(line)
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
            match = re.search(region, line, re.IGNORECASE)
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
    def flash_fw_image(self, toolName, img_path, bmc_image, flash_device, logFile='None'):
        self.wpl_log_debug('Entering procedure flash_fw_image with args : %s' %(str(locals())))
        passCount=0
        cmd = toolName + ' -v ' + img_path + '/' + bmc_image + ' ' + flash_device
        self.wpl_log_debug('command = %s' % cmd)
        self.wpl_flush()
        output = self.wpl_execute(cmd, mode="openbmc", timeout=600)
        for line in output.splitlines():
            line = line.strip()
            # e.g. Verifying kb: 21337/21337 (100%)
            match = re.search(r'^Verifying\skb:\s[\d+,\/]+\s[\(,100%,\)]+', line, re.IGNORECASE)
            if match:
                passCount += 1

        if logFile != 'None':
            self.wpl_send_output_to_log_file(output, logFile)

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
    def flash_update_and_verify_bmc(self, toolName, img_path, downgrade_bmc_image, upgrade_bmc_image, bmc_downgrade_ver, bmc_upgrade_ver, flash_device, logFile='None', uartLog='None'):
        self.wpl_log_debug('Entering procedure flash_update_and_verify_bmc with args : %s' %(str(locals())))

        update_bmc_image = ''
        found = False
        upgrade_bmc_flag = False
        upper_bmc_major_ver = 0
        upper_bmc_minor_ver = 0
        update_bmc_version = bmc_upgrade_ver
        # extract bmc image version
        upper_bmc_version = update_bmc_version
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

            if logFile != 'None':
                loop_cnt = int(self.bmc_update_loop_count)
                if self.check_local_file_exists(logFile) == True:
                    if loop_cnt == 0:
                        self.remove_local_file(logFile)

                # write date/time to log file
                cmd = ('touch ' + logFile)
                self.wpl_log_debug("command = %s" %cmd)
                self.wpl_flush()
                output = self.wpl_exec_local_cmd(cmd)
                self.wpl_log_debug(output)

                cmd = ('echo \"[$(date +\'%cF_%cH-%cM-%cS\')] now version is %s\" | tee -a %s > /dev/null' %('%','%','%','%', current_bmc_version, logFile))
                self.wpl_log_debug("command = %s" %cmd)
                self.wpl_flush()
                output = self.wpl_exec_local_cmd(cmd)
                self.wpl_log_debug(output)

                # update test loop count
                loop_cnt += 1
                self.bmc_update_loop_count = str(loop_cnt)
                cmd = ('echo \"[$(date +\'%cF_%cH-%cM-%cS\')] -------------Test Loop %s------------\" | tee -a %s > /dev/null' %('%','%','%','%', self.bmc_update_loop_count, logFile))
                self.wpl_log_debug("command = %s" %cmd)
                self.wpl_flush()
                output = self.wpl_exec_local_cmd(cmd)
                self.wpl_log_debug(output)

                if upgrade_bmc_flag == True:
                    self.wpl_log_debug('Performing BMC firmware upgrade to %s...\n' %update_bmc_image)
                    cmd = ('echo \"[$(date +\'%cF_%cH-%cM-%cS\')] Upgrade to %s\" | tee -a %s > /dev/null' %('%','%','%','%', bmc_upgrade_ver, logFile))
                else:
                    self.wpl_log_debug('Performing BMC firmware downgrade to %s...\n' %update_bmc_image)
                    cmd = ('echo \"[$(date +\'%cF_%cH-%cM-%cS\')] Downgrade to %s\" | tee -a %s > /dev/null' %('%','%','%','%', bmc_downgrade_ver, logFile))

                self.wpl_log_debug("command = %s" %cmd)
                self.wpl_flush()
                output = self.wpl_exec_local_cmd(cmd)
                self.wpl_log_debug(output)

            self.flash_fw_image(toolName, img_path, update_bmc_image, flash_device, logFile)

            if upgrade_bmc_flag == True:
                self.bmc_version = bmc_upgrade_ver
                self.wpl_log_success('Successfully flash upgraded BMC firmware using DIAG tool - %s\n' %toolName)
            else:
                self.bmc_version = bmc_downgrade_ver
                self.wpl_log_success('Successfully flash downgraded BMC firmware using DIAG tool - %s\n' %toolName)

            # verify bmc fw version after reboot
            self.wpl_log_debug('Reboot to verify BMC firmware version...\n')
            CommonLib.reboot("openbmc", uartLog)
            self.switch_to_openbmc_and_check_tool(uartLog)
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
            match = re.search(search_str, line, re.IGNORECASE)
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
    def check_current_bmc_version(self, bmc_downgrade_ver, bmc_upgrade_ver):
        self.wpl_log_debug('Entering procedure check_current_bmc_version with args : %s' %(str(locals())))
        lower_bmc_version = ''
        upper_bmc_version = ''

        current_bmc_version = self.get_current_bmc_rel_version()
        if current_bmc_version is None:
            self.wpl_raiseException("Failed check_current_bmc_version")

        if self.bmc_version != '0':
            # extract last updated version
            updated_bmc_version = self.bmc_version
            if current_bmc_version == updated_bmc_version:
                self.wpl_log_success('check_current_bmc_version test result is PASS.\n')
                return
            else:
                self.wpl_raiseException("Failed check_current_bmc_version. Current bmc version not equal to last updated version.")

        # bmc have not been updated yet
        # extract bmc downgrade version
        slist = bmc_downgrade_ver.split('-')
        lower_bmc_version = str(slist[0])

        # extract bmc upgrade version
        slist1 = bmc_upgrade_ver.split('-')
        upper_bmc_version = str(slist1[0])

        if current_bmc_version == lower_bmc_version:
            self.wpl_log_success('check_current_bmc_version test result is PASS.')
            return current_bmc_version
        elif current_bmc_version == upper_bmc_version:
            self.wpl_log_success('check_current_bmc_version test result is PASS.')
            return current_bmc_version
        else:
            # current_bmc_version not equals to upper nor lower version
            self.wpl_raiseException("Failed check_current_bmc_version.")


#######################################################################################################################
# Function Name: extract_fw_version
# Date         : 14th May 2020
# Author       : TK NG<tikng@celestica.com>
#
# Procedure Revision Details:
#   Version : 1.0  - Initial Draft  - by TK NG<tikng@celestica.com>
#######################################################################################################################
    def extract_fw_version(self, fw_version_str):
        self.wpl_log_debug('Entering procedure extract_fw_version with args : %s' %(str(locals())))

        match = re.search('_v', fw_version_str, re.IGNORECASE)
        if match:
            found = True
        else:
            match1 = re.search('-v', fw_version_str, re.IGNORECASE)
            if match1:
                found = True
            else:
                found = False

        if found == False:
             self.wpl_raiseException("Failed extract_fw_version. Version string not found.")
        else:
            slist = fw_version_str.split('v')
            fw_version = str(slist[1])
            return fw_version


#######################################################################################################################
# Function Name: verify_option_bmc_tool_system_dict
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

        passCount = 0
        self.wpl_getPrompt("openbmc", 600)

        # write register data: i2cset -f -y 12 0x3e 0x20 0x00
        cmd = setToolName + ' ' + option  + ' ' + bus + ' ' + chip_addr + ' ' + data_addr + ' ' + value
        self.wpl_log_debug("command = [%s]" %(cmd))
        self.wpl_execute(cmd, mode=openbmc_mode, timeout=600)

        # verify register data
        passCount = self.verify_i2c_register(verifyToolName, option, bus, chip_addr, data_addr, value)

        if passCount:
            self.wpl_log_success("Successfully set_and_verify_i2c_register.")
        else:
            self.wpl_raiseException("Failure in set_and_verify_i2c_register.")


#######################################################################################################################
# Function Name: verify_i2c_register
# Date         : 14th May 2020
# Author       : TK NG<tikng@celestica.com>
#
# Procedure Revision Details:
#   Version : 1.0  - Initial Draft  - by TK NG<tikng@celestica.com>
#######################################################################################################################
    def verify_i2c_register(self, verifyToolName, option, bus, chip_addr, data_addr, value):
        self.wpl_log_debug('Entering procedure verify_i2c_register with args : %s' %(str(locals())))

        passCount = 0
        self.wpl_getPrompt("openbmc", 600)

        # read register data: i2cget -f -y 12 0x3e 0x20
        cmd1 = verifyToolName + ' ' + option  + ' ' + bus + ' ' + chip_addr + ' ' + data_addr
        self.wpl_log_debug("command = [%s]" %(cmd1))
        output = self.wpl_execute(cmd1, mode=openbmc_mode, timeout=600)
        self.wpl_log_debug("output=[%s]" %output)

        # verify register data
        for line in output.splitlines():
            line = line.strip()
            if line == value:
                passCount = 1
                break

        if passCount:
            self.wpl_log_success("Successfully verify_i2c_register.")
        else:
            self.wpl_raiseException("Failure in verify_i2c_register.")

        return passCount


#######################################################################################################################
# Function Name: set_max_bios_update_cycles
# Date         : 14th May 2020
# Author       : TK NG<tikng@celestica.com>
#
# Procedure Revision Details:
#   Version : 1.0  - Initial Draft  - by TK NG<tikng@celestica.com>
#######################################################################################################################
    def set_max_bios_update_cycles(self, max_cycles):
        self.wpl_log_debug('Entering procedure set_max_bios_update_cycles with args : %s' %(str(locals())))

        self.bios_update_max_cycles = str(max_cycles)

        self.wpl_log_success('Successfully set_max_bios_update_cycles: [%s] cycles.\n' %(str(max_cycles)))


#######################################################################################################################
# Function Name: flash_update_master_bios
# Date         : 14th May 2020
# Author       : TK NG<tikng@celestica.com>
#
# Procedure Revision Details:
#   Version : 1.0  - Initial Draft  - by TK NG<tikng@celestica.com>
#######################################################################################################################
    def flash_update_master_bios(self, toolName, fru, opt, dev, check_pattern, downgrade_image, upgrade_image, downgrade_ver, upgrade_ver, img_path, tool_path, logFile='None'):
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

            if logFile != 'None':
                loop_cnt = int(self.bios_update_loop_count)
                if self.check_local_file_exists(logFile) == True:
                    if loop_cnt == 0:
                        self.remove_local_file(logFile)

                # write date/time to log file
                cmd = ('touch ' + logFile)
                self.wpl_log_debug("command = %s" %cmd)
                self.wpl_flush()
                output = self.wpl_exec_local_cmd(cmd)
                self.wpl_log_debug(output)

                cmd = ('echo \"[$(date +\'%cF_%cH-%cM-%cS\')] now version is %s\" | tee -a %s > /dev/null' %('%','%','%','%', current_bios_version, logFile))
                self.wpl_log_debug("command = %s" %cmd)
                self.wpl_flush()
                output = self.wpl_exec_local_cmd(cmd)
                self.wpl_log_debug(output)

                # update test loop count
                loop_cnt += 1
                self.bios_update_loop_count = str(loop_cnt)
                cmd = ('echo \"[$(date +\'%cF_%cH-%cM-%cS\')] -------------Test Loop %s------------\" | tee -a %s > /dev/null' %('%','%','%','%', self.bios_update_loop_count, logFile))
                self.wpl_log_debug("command = %s" %cmd)
                self.wpl_flush()
                output = self.wpl_exec_local_cmd(cmd)
                self.wpl_log_debug(output)

                if upgrade_bios_flag == True:
                    self.wpl_log_debug('Performing BIOS firmware upgrade to %s...\n' %update_bios_image)
                    cmd = ('echo \"[$(date +\'%cF_%cH-%cM-%cS\')] Upgrade to %s\" | tee -a %s > /dev/null' %('%','%','%','%', upgrade_ver, logFile))
                else:
                    self.wpl_log_debug('Performing BIOS firmware downgrade to %s...\n' %update_bios_image)
                    cmd = ('echo \"[$(date +\'%cF_%cH-%cM-%cS\')] Downgrade to %s\" | tee -a %s > /dev/null' %('%','%','%','%', downgrade_ver, logFile))

                self.wpl_log_debug("command = %s" %cmd)
                self.wpl_flush()
                output = self.wpl_exec_local_cmd(cmd)
                self.wpl_log_debug(output)

            # perform BIOS upgrade/downgrade
            self.fw_util_exec(toolName, fru, opt, dev, update_bios_image, check_pattern, img_path, tool_path, "openbmc", logFile)

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
    def switch_and_verify_master_bios_version(self, logFile='None'):
        self.wpl_log_debug('Entering procedure switch_and_verify_master_bios_version with args : %s' %(str(locals())))

        if self.bios_version == '0':
            self.wpl_raiseException("Failed switch_and_verify_master_bios_version, BIOS update version not found.")
        else:
            self.wpl_log_debug('waiting for system to bootup...\n')
            CommonLib.switch_to_centos(logFile)
            self.switch_to_openbmc_and_check_tool(logFile)
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
# Function Name: backup_uart_log_file
# Date         : 14th May 2020
# Author       : TK NG<tikng@celestica.com>
#
# Procedure Revision Details:
#   Version : 1.0  - Initial Draft  - by TK NG<tikng@celestica.com>
#######################################################################################################################
    def backup_uart_log_file(self, logFile, prefix, check_diag_path, srcPath, destPath):
        self.wpl_log_debug('Entering procedure backup_uart_log_file with args : %s' %(str(locals())))

        srcLogFile = srcPath + logFile
        if CommonLib.check_file_exist(srcLogFile, openbmc_mode) == False:
            self.wpl_log_debug("%s file not found." %srcLogFile)
            return

        if check_diag_path:
            # diag path must be mounted first
            self.check_bmc_diag_tool()

        # check whether log with '-' in filename
        match = re.search('-', logFile)
        if match:
            num_section = 3
        else:
            num_section = 2

        max_file_num = 0
        # list all files, excluding sub-directories
        cmd = ('ls -p %s | grep -v /$' %destPath)
        self.wpl_log_debug("command = %s" % cmd)
        self.wpl_flush()
        output = self.wpl_execute(cmd, mode=openbmc_mode, timeout=300)

        # fix the output filename not on same line
        addLine = False
        output1 = ''
        new_output = ''
        previous_line = ''
        for sline in output.splitlines():
            line = sline.strip()
            if len(line) == 0:
                # blank line
                continue
            else:
                if re.search(".log", line, re.IGNORECASE):
                    if addLine:
                        new_output = previous_line + line + '\r\n'
                        output1 = output1 + new_output
                        previous_line = ''
                        addLine = False
                    else:
                        output1 += (line + '\r\n')
                else:
                    addLine = True
                    previous_line = previous_line + line
                    if re.search(".log", previous_line, re.IGNORECASE):
                        new_output = previous_line + '\r\n'
                        output1 = output1 + new_output
                        previous_line = ''
                        addLine = False

        output = output1
        self.wpl_log_debug('%s' %output)
        errCount = 0
        for line in output.splitlines():
            filename = line.strip()
            match1 = re.search(prefix, filename, re.IGNORECASE)
            if match1:
                slist = filename.split('.')
                nameStr = str(slist[0])
                # get the highest file number
                if num_section == 2:
                    slist1 = nameStr.split('_')
                    tmp_number = str(slist1[2])
                else:
                    slist1 = nameStr.split('-')
                    tmp_number = str(slist1[3])
                file_number = int(tmp_number)
                if max_file_num == 0:
                    max_file_num = file_number
                else:
                    if file_number > max_file_num:
                        max_file_num = file_number

        max_file_num += 1
        new_filename = (prefix + str(max_file_num) + '.log')

        cmd = ('cp %s %s%s' %(srcLogFile, destPath, new_filename))
        self.wpl_log_debug("command = %s" % cmd)
        self.wpl_execute(cmd, mode=openbmc_mode, timeout=60)

        self.wpl_log_success('Successfully backup_uart_log_file.\n')


#######################################################################################################################
# Function Name: flash_update_bic
# Date         : 14th May 2020
# Author       : TK NG<tikng@celestica.com>
#
# Procedure Revision Details:
#   Version : 1.0  - Initial Draft  - by TK NG<tikng@celestica.com>
#######################################################################################################################
    def flash_update_bic(self, toolName, fru, opt, dev, check_pattern, downgrade_image, upgrade_image, downgrade_ver, upgrade_ver, img_path, tool_path, logFile='None'):
        self.wpl_log_debug('Entering procedure flash_update_bic with args : %s' %(str(locals())))
        update_bic_image = ''
        found = False
        upgrade_bic_flag = False
        upper_bic_major_ver = 0
        upper_bic_minor_ver = 0
        cur_bic_major_ver = 0
        cur_bic_minor_ver = 0
        update_bic_version = upgrade_ver

        # extract bic version
        # e.g. v1.11
        slist = update_bic_version.split('v')
        tmp_str = str(slist[1])
        slist1 = tmp_str.split('.')
        upper_bic_major_str = str(slist1[0])
        upper_bic_minor_str = str(slist1[1])
        upper_bic_major_ver = int(upper_bic_major_str)
        upper_bic_minor_ver = int(upper_bic_minor_str)

        self.wpl_log_debug('upper_bic_major_ver: [%s]' %upper_bic_major_ver)
        self.wpl_log_debug('upper_bic_minor_ver: [%s]' %upper_bic_minor_ver)

        current_bic_version = self.get_current_bic_version(fw_util_tool, "scm", "--version", FW_UTIL_PATH)
        if current_bic_version == '0':
            self.wpl_raiseException("Failed flash_update_bic. Unable to get current bic version.")
        else:
            slist2 = current_bic_version.split('v')
            tmp_str1 = str(slist2[1])
            slist3 = tmp_str1.split('.')
            cur_major_str = str(slist3[0])
            cur_minor_str = str(slist3[1])
            cur_bic_major_ver = int(cur_major_str)
            cur_bic_minor_ver = int(cur_minor_str)

            self.wpl_log_debug('cur_bic_major_ver=[%s]' %cur_bic_major_ver)
            self.wpl_log_debug('cur_bic_minor_ver=[%s]' %cur_bic_minor_ver)

            if cur_bic_major_ver < upper_bic_major_ver:
                # need to perform upgrade
                update_bic_image = upgrade_image
                upgrade_bic_flag = True
            elif cur_bic_major_ver > upper_bic_major_ver:
                # need to perform downgrade
                update_bic_image = downgrade_image
                upgrade_bic_flag = False
            else:
                if cur_bic_minor_ver < upper_bic_minor_ver:
                    # need to perform upgrade
                    update_bic_image = upgrade_image
                    upgrade_bic_flag = True
                else:
                    # need to perform downgrade
                    update_bic_image = downgrade_image
                    upgrade_bic_flag = False

            if logFile != 'None':
                loop_cnt = int(self.bic_update_loop_count)
                if self.check_local_file_exists(logFile) == True:
                    if loop_cnt == 0:
                        self.remove_local_file(logFile)

                # write date/time to log file
                cmd = ('touch ' + logFile)
                self.wpl_log_debug("command = %s" %cmd)
                self.wpl_flush()
                output = self.wpl_exec_local_cmd(cmd)
                self.wpl_log_debug(output)

                cmd = ('echo \"[$(date +\'%cF_%cH-%cM-%cS\')] now version is %s\" | tee -a %s > /dev/null' %('%','%','%','%', current_bic_version, logFile))
                self.wpl_log_debug("command = %s" %cmd)
                self.wpl_flush()
                output = self.wpl_exec_local_cmd(cmd)
                self.wpl_log_debug(output)

                # update test loop count
                loop_cnt += 1
                self.bic_update_loop_count = str(loop_cnt)
                cmd = ('echo \"[$(date +\'%cF_%cH-%cM-%cS\')] -------------Test Loop %s------------\" | tee -a %s > /dev/null' %('%','%','%','%', self.bic_update_loop_count, logFile))
                self.wpl_log_debug("command = %s" %cmd)
                self.wpl_flush()
                output = self.wpl_exec_local_cmd(cmd)
                self.wpl_log_debug(output)

                if upgrade_bic_flag == True:
                    self.wpl_log_debug('Performing BIC firmware upgrade to %s...\n' %update_bic_image)
                    cmd = ('echo \"[$(date +\'%cF_%cH-%cM-%cS\')] Upgrade to %s\" | tee -a %s > /dev/null' %('%','%','%','%', upgrade_ver, logFile))
                else:
                    self.wpl_log_debug('Performing BIC firmware downgrade to %s...\n' %update_bic_image)
                    cmd = ('echo \"[$(date +\'%cF_%cH-%cM-%cS\')] Downgrade to %s\" | tee -a %s > /dev/null' %('%','%','%','%', downgrade_ver, logFile))

                self.wpl_log_debug("command = %s" %cmd)
                self.wpl_flush()
                output = self.wpl_exec_local_cmd(cmd)
                self.wpl_log_debug(output)

            # perform BIOS upgrade/downgrade
            self.fw_util_exec(toolName, fru, opt, dev, update_bic_image, check_pattern, img_path, tool_path, "openbmc", logFile)

            if upgrade_bic_flag == True:
                self.bic_version = upgrade_ver
                self.wpl_log_success('Successfully flash upgraded BIC firmware using DIAG tool - %s\n' %toolName)
            else:
                self.bic_version = downgrade_ver
                self.wpl_log_success('Successfully flash downgraded BIC firmware using DIAG tool - %s\n' %toolName)


#######################################################################################################################
# Function Name: extract_bic_fw_version
# Date         : 14th May 2020
# Author       : TK NG<tikng@celestica.com>
#
# Procedure Revision Details:
#   Version : 1.0  - Initial Draft  - by TK NG<tikng@celestica.com>
#######################################################################################################################
    def extract_bic_fw_version(self, fw_version_str):
        self.wpl_log_debug('Entering procedure extract_bic_fw_version with args : %s' %(str(locals())))
        found = False

        # 'xg1_snowflake_111.bin'
        match = re.search('_', fw_version_str)
        if match:
            found = True

        if found == False:
             self.wpl_raiseException("Failed extract_bic_fw_version. Version string not found.")
        else:
            slist = fw_version_str.split('_')
            tmp_str = str(slist[2])
            slist1 = tmp_str.split('.')
            fw_version = str(slist1[0])
            return fw_version


#######################################################################################################################
# Function Name: wedge400_power_reset
# Date         : 14th May 2020
# Author       : TK NG<tikng@celestica.com>
#
# Procedure Revision Details:
#   Version : 1.0  - Initial Draft  - by TK NG<tikng@celestica.com>
#######################################################################################################################
    def wedge400_power_reset(self, toolName, operation, option, tool_path, logFile):
        self.wpl_log_debug('Entering procedure wedge400_power_reset with args : %s' %(str(locals())))

        cmd = 'cd /'
        self.wpl_log_debug("command = %s" % cmd)
        self.wpl_flush()
        output = self.wpl_execute(cmd, mode=openbmc_mode, timeout=300)
        self.wpl_log_debug('%s' %output)

        cmd = (tool_path + toolName + ' ' + operation + ' ' + option)
        self.wpl_log_debug("command = %s" % cmd)
        self.wpl_flush()
        output = self.wpl_execute(cmd, mode=openbmc_mode, timeout=300)
        self.wpl_log_debug('%s' %output)

        self.switch_to_openbmc_and_check_tool(logFile)
        # wait for cpu to boot up to centos
        CommonLib.switch_to_centos(logFile)
        self.switch_and_check_bmc_by_diag_command(diag_bmc_boot_bin, "master")

        self.wpl_log_success('Successfully wedge400_power_reset.\n')


#######################################################################################################################
# Function Name: set_max_bic_update_cycles
# Date         : 14th May 2020
# Author       : TK NG<tikng@celestica.com>
#
# Procedure Revision Details:
#   Version : 1.0  - Initial Draft  - by TK NG<tikng@celestica.com>
#######################################################################################################################
    def set_max_bic_update_cycles(self, max_cycles):
        self.wpl_log_debug('Entering procedure set_max_bic_update_cycles with args : %s' %(str(locals())))

        self.bic_update_max_cycles = str(max_cycles)

        self.wpl_log_success('Successfully set_max_bic_update_cycles: [%s] cycles.\n' %(str(max_cycles)))


#######################################################################################################################
# Function Name: remove_file
# Date         : 14th May 2020
# Author       : TK NG<tikng@celestica.com>
#
# Procedure Revision Details:
#   Version : 1.0  - Initial Draft  - by TK NG<tikng@celestica.com>
#######################################################################################################################
    def remove_file(self, file_path_name):
        self.wpl_log_debug('Entering procedure remove_file with args : %s' %(str(locals())))

        # check whether file exists
        cmd = ('sudo rm -f %s' %file_path_name)
        self.wpl_log_debug('command = %s' %cmd)
        self.wpl_flush()
        output = self.wpl_execute(cmd, mode=openbmc_mode, timeout=300)
        self.wpl_log_debug('%s' %output)


#######################################################################################################################
# Function Name: check_local_file_exists
# Date         : 14th May 2020
# Author       : TK NG<tikng@celestica.com>
#
# Procedure Revision Details:
#   Version : 1.0  - Initial Draft  - by TK NG<tikng@celestica.com>
#######################################################################################################################
    def check_local_file_exists(self, file_path_name):
        self.wpl_log_debug('Entering procedure check_local_file_exists with args : %s' %(str(locals())))

        # check whether file exists
        p1 = 'No such file or directory'
        cmd = ("ls %s" %file_path_name)
        #self.wpl_log_debug("command = %s" %cmd)
        output = self.wpl_exec_local_cmd(cmd)
        errCount = 0
        if len(output) == 0:
            errCount = 1
        else:
            for line in output.splitlines():
                line = line.strip()
                match = re.search(p1, line, re.IGNORECASE)
                if match:
                    errCount+=1
                    break
        if errCount:
            self.wpl_log_debug("[check_local_file_exists] %s not exist." %file_path_name)
            # file not exist
            return False
        else:
            self.wpl_log_debug("[check_local_file_exists] %s exist." %file_path_name)
            # file exists
            return True


#######################################################################################################################
# Function Name: remove_local_file
# Date         : 14th May 2020
# Author       : TK NG<tikng@celestica.com>
#
# Procedure Revision Details:
#   Version : 1.0  - Initial Draft  - by TK NG<tikng@celestica.com>
#######################################################################################################################
    def remove_local_file(self, file_path_name):
        self.wpl_log_debug('Entering procedure remove_local_file with args : %s' %(str(locals())))

        # check whether file exists
        cmd = ('rm -f %s' %file_path_name)
        self.wpl_log_debug("command = %s" %cmd)
        self.wpl_flush()
        output = self.wpl_exec_local_cmd(cmd)
        self.wpl_log_debug('%s' %output)


#######################################################################################################################
# Function Name: verify_bic_version
# Date         : 14th May 2020
# Author       : TK NG<tikng@celestica.com>
#
# Procedure Revision Details:
#   Version : 1.0  - Initial Draft  - by TK NG<tikng@celestica.com>
#######################################################################################################################
    def verify_bic_version(self, toolName, fru, opt, toolPath):
        self.wpl_log_debug('Entering procedure verify_bic_version with args : %s' %(str(locals())))

        current_bic_ver = self.get_current_bic_version(toolName, fru, opt, toolPath)
        self.wpl_log_debug("Current bic version: [%s]" %current_bic_ver)
        self.wpl_log_debug("Last flash update bic version: [%s]" %self.bic_version)

        if current_bic_ver == self.bic_version:
            self.wpl_log_success('Successfully verify_bic_version.\n')
        else:
            self.wpl_raiseException("ERR_01_001_01: Failed verify_bic_version.")


#######################################################################################################################
# Function Name: check_local_log_file
# Date         : 14th May 2020
# Author       : TK NG<tikng@celestica.com>
#
# Procedure Revision Details:
#   Version : 1.0  - Initial Draft  - by TK NG<tikng@celestica.com>
#######################################################################################################################
    def check_local_log_file(self, logFile, prefix, check_diag_path, srcPath, destPath):
        self.wpl_log_debug('Entering procedure check_local_log_file with args : %s' %(str(locals())))

        srcLogFile = srcPath + logFile
        if self.check_local_file_exists(srcLogFile) == False:
            self.wpl_log_debug("%s file not found." %srcLogFile)
            return "None"

        if check_diag_path:
            # diag path must be mounted first
            self.check_bmc_diag_tool()

        # check whether log with '-' in filename
        match = re.search('-', logFile)
        if match:
            num_section = 3
        else:
            num_section = 2

        max_file_num = 0

        # list all files in openbmc, excluding sub-directories
        cmd = ('ls -p %s | grep -v /$' %destPath)
        self.wpl_log_debug("command = %s" % cmd)
        self.wpl_flush()
        output = self.wpl_execute(cmd, mode=openbmc_mode, timeout=300)

        # fix the output filename not on same line
        addLine = False
        output1 = ''
        new_output = ''
        previous_line = ''
        for sline in output.splitlines():
            line = sline.strip()
            if len(line) == 0:
                # blank line
                continue
            else:
                if re.search(".gitignore", line, re.IGNORECASE):
                    continue
                if re.search(".html", line, re.IGNORECASE):
                    continue
                if re.search(".xml", line, re.IGNORECASE):
                    continue

                if re.search(".log", line, re.IGNORECASE):
                    if addLine:
                        new_output = previous_line + line + '\r\n'
                        output1 = output1 + new_output
                        previous_line = ''
                        addLine = False
                    else:
                        output1 += (line + '\r\n')
                else:
                    addLine = True
                    previous_line = previous_line + line
                    if re.search(".log", previous_line, re.IGNORECASE):
                        new_output = previous_line + '\r\n'
                        output1 = output1 + new_output
                        previous_line = ''
                        addLine = False

        output = output1
        self.wpl_log_debug('%s' %output)
        errCount = 0
        for line in output.splitlines():
            filename = line.strip()
            match1 = re.search(prefix, filename, re.IGNORECASE)
            if match1:
                slist = filename.split('.')
                nameStr = str(slist[0])
                # get the highest file number
                if num_section == 2:
                    slist1 = nameStr.split('_')
                    tmp_number = str(slist1[2])
                else:
                    slist1 = nameStr.split('-')
                    tmp_number = str(slist1[3])
                file_number = int(tmp_number)
                if max_file_num == 0:
                    max_file_num = file_number
                else:
                    if file_number > max_file_num:
                        max_file_num = file_number

        max_file_num += 1
        new_filename = (prefix + str(max_file_num) + '.log')

        # rename to new filename
        destLogFile = srcPath + new_filename
        cmd = ("mv %s %s" %(srcLogFile, destLogFile))
        self.wpl_log_debug("command = %s" %cmd)
        self.wpl_flush()
        output = self.wpl_exec_local_cmd(cmd)
        self.wpl_log_debug('%s' %output)

        self.wpl_log_success('check_local_log_file: [%s]' %new_filename)
        return new_filename


#######################################################################################################################
# Function Name: get_current_cpld_versions
# Date         : 14th May 2020
# Author       : TK NG<tikng@celestica.com>
#
# Procedure Revision Details:
#   Version : 1.0  - Initial Draft  - by TK NG<tikng@celestica.com>
#######################################################################################################################
    def get_current_cpld_versions(self, toolName, toolPath, cpldType='all'):
        self.wpl_log_debug('Entering procedure get_current_cpld_versions with args : %s' %(str(locals())))
        cmd = 'cd ' + toolPath
        self.wpl_getPrompt("openbmc", 600)
        self.wpl_transmit(cmd)
        optionStr = ' '
        errCount = 0
        current_syscpld_version = '0'
        current_pwrcpld_version = '0'
        current_scmcpld_version = '0'
        current_fcmcpld_version = '0'
        output = self.EXEC_bmc_system_tool_command(toolName, optionStr, toolPath)
        self.wpl_log_debug(output)
        parsedOutput = parserDIAGLibs.PARSE_CPLD_Versions(output)

        current_syscpld_version = parsedOutput.getValue('SYSCPLD_VER')[0]
        if current_syscpld_version == None:
            self.wpl_raiseException("current_syscpld_version not found !")
        else:
            self.wpl_log_success('Found current_syscpld_version: [%s]' %current_syscpld_version)

        current_pwrcpld_version = parsedOutput.getValue('PWRCPLD_VER')[0]
        if current_pwrcpld_version == None:
            self.wpl_raiseException("current_pwrcpld_version not found !")
        else:
            self.wpl_log_success('Found current_pwrcpld_version: [%s]' %current_pwrcpld_version)

        current_scmcpld_version = parsedOutput.getValue('SCMCPLD_VER')[0]
        if current_scmcpld_version == None:
            self.wpl_raiseException("current_scmcpld_version not found !")
        else:
            self.wpl_log_success('Found current_scmcpld_version: [%s]' %current_scmcpld_version)

        current_fcmcpld_version = parsedOutput.getValue('FCMCPLD_VER')[0]
        if current_fcmcpld_version == None:
            self.wpl_raiseException("current_fcmcpld_version not found !")
        else:
            self.wpl_log_success('Found current_fcmcpld_version: [%s]' %current_fcmcpld_version)

        if cpldType == 'smb':
            return current_syscpld_version
        elif cpldType == 'pwr':
            return current_pwrcpld_version
        elif cpldType == 'scm':
            return current_scmcpld_version
        elif cpldType == 'fcm':
            return current_fcmcpld_version
        else:
            cpld_versions = ('[' + current_syscpld_version + ', ' + current_pwrcpld_version + ', ' + current_scmcpld_version + ', ' + current_fcmcpld_version + ']')
            return cpld_versions


#######################################################################################################################
# Function Name: flash_update_cpld
# Date         : 14th May 2020
# Author       : TK NG<tikng@celestica.com>
#
# Procedure Revision Details:
#   Version : 1.0  - Initial Draft  - by TK NG<tikng@celestica.com>
#######################################################################################################################
    def flash_update_cpld(self, dev, cpldType, toolName, check_pattern, downgrade_image, upgrade_image, downgrade_ver, upgrade_ver, img_path, tool_path, logFile='None'):
        self.wpl_log_debug('Entering procedure flash_update_cpld with args : %s' %(str(locals())))
        update_cpld_image = ''
        found = False
        upgrade_cpld_flag = False
        upper_cpld_major_ver = 0
        upper_cpld_minor_ver = 0
        cur_cpld_major_ver = 0
        cur_cpld_minor_ver = 0

        if (cpldType == 'smb') or (cpldType == 'pwr') or (cpldType == 'scm') or (cpldType == 'fcm'):
             self.wpl_log_debug('Performing %s cpld update...' %cpldType)
        else:
            self.wpl_raiseException("Failed flash_update_cpld. Unknown cpld type: [%s]." %cpldType)

        update_cpld_version = upgrade_ver

        # extract cpld version
        slist1 = update_cpld_version.split('.')
        upper_cpld_major_str = str(slist1[0])
        upper_cpld_minor_str = str(slist1[1])
        upper_cpld_major_ver = int(upper_cpld_major_str)
        upper_cpld_minor_ver = int(upper_cpld_minor_str)

        self.wpl_log_debug('upper %s cpld major ver: [%s]' %(cpldType, upper_cpld_major_ver))
        self.wpl_log_debug('upper %s cpld minor ver: [%s]' %(cpldType, upper_cpld_minor_ver))

        current_cpld_version = self.get_current_cpld_versions(cpld_version_tool, SPI_UTIL_PATH, cpldType)
        if current_cpld_version == '0':
            self.wpl_raiseException("Failed flash_update_cpld. Unable to get current %s cpld version." %cpldType)
        else:
            # save current cpld version
            if cpldType == 'smb':
                self.old_syscpld_version = current_cpld_version
            elif cpldType == 'pwr':
                self.old_pwrcpld_version = current_cpld_version
            elif cpldType == 'scm':
                self.old_scmcpld_version = current_cpld_version
            else:
                self.old_fcmcpld_version = current_cpld_version

            slist2 = current_cpld_version.split('.')
            cur_major_str = str(slist2[0])
            cur_minor_str = str(slist2[1])
            cur_cpld_major_ver = int(cur_major_str)
            cur_cpld_minor_ver = int(cur_minor_str)

            self.wpl_log_debug('current %s cpld major ver=[%s]' %(cpldType, cur_cpld_major_ver))
            self.wpl_log_debug('current %s cpld minor ver=[%s]' %(cpldType, cur_cpld_minor_ver))

            if cur_cpld_major_ver < upper_cpld_major_ver:
                # need to perform upgrade
                update_cpld_image = upgrade_image
                upgrade_cpld_flag = True
            elif cur_cpld_major_ver > upper_cpld_major_ver:
                # need to perform downgrade
                update_cpld_image = downgrade_image
                upgrade_cpld_flag = False
            else:
                if cur_cpld_minor_ver < upper_cpld_minor_ver:
                    # need to perform upgrade
                    update_cpld_image = upgrade_image
                    upgrade_cpld_flag = True
                else:
                    # need to perform downgrade
                    update_cpld_image = downgrade_image
                    upgrade_cpld_flag = False

            # 15.15 (f.f) is a special test version
            if (cur_cpld_major_ver == 15) and (cur_cpld_minor_ver == 15):
                # need to perform upgrade
                update_cpld_image = upgrade_image
                upgrade_cpld_flag = True

            if logFile != 'None':
                loop_cnt = int(self.cpld_update_loop_count)
                if self.check_local_file_exists(logFile) == True:
                    if loop_cnt == 0:
                        self.remove_local_file(logFile)

                # write date/time to log file
                cmd = ('touch ' + logFile)
                self.wpl_log_debug("command = %s" %cmd)
                self.wpl_flush()
                output = self.wpl_exec_local_cmd(cmd)
                self.wpl_log_debug(output)

                cmd = ('echo \"[$(date +\'%cF_%cH-%cM-%cS\')] now %s cpld version is %s\" | tee -a %s > /dev/null' %('%','%','%','%', cpldType, current_cpld_version, logFile))
                self.wpl_log_debug("command = %s" %cmd)
                self.wpl_flush()
                output = self.wpl_exec_local_cmd(cmd)
                self.wpl_log_debug(output)

                # update test loop count
                loop_cnt += 1
                self.cpld_update_loop_count = str(loop_cnt)
                cmd = ('echo \"[$(date +\'%cF_%cH-%cM-%cS\')] -------------Test Loop %s------------\" | tee -a %s > /dev/null' %('%','%','%','%', self.cpld_update_loop_count, logFile))
                self.wpl_log_debug("command = %s" %cmd)
                self.wpl_flush()
                output = self.wpl_exec_local_cmd(cmd)
                self.wpl_log_debug(output)

                if upgrade_cpld_flag == True:
                    self.wpl_log_debug('Performing %s cpld firmware upgrade to %s...\n' %(cpldType, update_cpld_image))
                    cmd = ('echo \"[$(date +\'%cF_%cH-%cM-%cS\')] Upgrade to %s\" | tee -a %s > /dev/null' %('%','%','%','%', upgrade_ver, logFile))
                else:
                    self.wpl_log_debug('Performing %s cpld firmware downgrade to %s...\n' %(cpldType, update_cpld_image))
                    cmd = ('echo \"[$(date +\'%cF_%cH-%cM-%cS\')] Downgrade to %s\" | tee -a %s > /dev/null' %('%','%','%','%', downgrade_ver, logFile))

                self.wpl_log_debug("command = %s" %cmd)
                self.wpl_flush()
                output = self.wpl_exec_local_cmd(cmd)
                self.wpl_log_debug(output)

            # perform CPLD upgrade/downgrade
            self.update_tool_exec(toolName, update_cpld_image, ' ', dev, check_pattern, img_path, tool_path, logFile)

            if upgrade_cpld_flag == True:
                if cpldType == 'smb':
                    self.syscpld_version = upgrade_ver
                elif cpldType == 'pwr':
                    self.pwrcpld_version = upgrade_ver
                elif cpldType == 'scm':
                    self.scmcpld_version = upgrade_ver
                else:
                    self.fcmcpld_version = upgrade_ver

                self.wpl_log_success('Successfully flash upgraded %s cpld firmware using DIAG tool - %s\n' %(cpldType, toolName))
            else:
                if cpldType == 'smb':
                    self.syscpld_version = downgrade_ver
                elif cpldType == 'pwr':
                    self.pwrcpld_version = downgrade_ver
                elif cpldType == 'scm':
                    self.scmcpld_version = downgrade_ver
                else:
                    self.fcmcpld_version = downgrade_ver

                self.wpl_log_success('Successfully flash downgraded %s cpld firmware using DIAG tool - %s\n' %(cpldType, toolName))

            # wait for system power cycle
            time.sleep(60)
            self.wpl_log_info("Waiting for openbmc prompt...")
            self.wpl_getPrompt("openbmc", 600)
            self.wpl_log_info("Done.")


#######################################################################################################################
# Function Name: verify_cpld_versions_after_flash_update
# Date         : 14th May 2020
# Author       : TK NG<tikng@celestica.com>
#
# Procedure Revision Details:
#   Version : 1.0  - Initial Draft  - by TK NG<tikng@celestica.com>
#######################################################################################################################
    def verify_cpld_versions_after_flash_update(self, toolName, toolPath, cpldType='all'):
        self.wpl_log_debug('Entering procedure verify_cpld_versions_after_flash_update with args : %s' %(str(locals())))
        cmd = 'cd ' + toolPath
        self.wpl_getPrompt("openbmc", 600)
        self.wpl_transmit(cmd)
        optionStr = ' '
        errCount = 0
        current_syscpld_version = '0'
        current_pwrcpld_version = '0'
        current_scmcpld_version = '0'
        current_fcmcpld_version = '0'
        output = self.EXEC_bmc_system_tool_command(toolName, optionStr, toolPath)
        self.wpl_log_debug(output)
        parsedOutput = parserDIAGLibs.PARSE_CPLD_Versions(output)

        current_syscpld_version = parsedOutput.getValue('SYSCPLD_VER')[0]
        if current_syscpld_version == None:
            self.wpl_raiseException("current sys cpld version not found !")
        else:
            self.wpl_log_debug('Previous sys cpld version: [%s]' %self.old_syscpld_version)
            self.wpl_log_debug('Current sys cpld version: [%s]' %current_syscpld_version)
            if self.old_syscpld_version == current_syscpld_version:
                self.wpl_log_debug('Previous and current sys cpld versions matched. Pass.')
            else:
                 self.wpl_raiseException('Previous and current sys cpld versions do not match ! Fail')

        current_pwrcpld_version = parsedOutput.getValue('PWRCPLD_VER')[0]
        if current_pwrcpld_version == None:
            self.wpl_raiseException("current pwr cpld version not found !")
        else:
            self.wpl_log_debug('Previous pwr cpld version: [%s]' %self.old_pwrcpld_version)
            self.wpl_log_debug('Current pwr cpld version: [%s]' %current_pwrcpld_version)
            if self.old_pwrcpld_version != current_pwrcpld_version:
                self.wpl_log_debug('Previous and current pwr cpld versions do not matched. Pass.')
            else:
                 self.wpl_raiseException('Previous and current pwr cpld versions match ! Fail')

        current_scmcpld_version = parsedOutput.getValue('SCMCPLD_VER')[0]
        if current_scmcpld_version == None:
            self.wpl_raiseException("current scm cpld version not found !")
        else:
            self.wpl_log_debug('Previous scm cpld version: [%s]' %self.old_scmcpld_version)
            self.wpl_log_debug('Current scm cpld version: [%s]' %current_scmcpld_version)
            if self.old_scmcpld_version == current_scmcpld_version:
                self.wpl_log_debug('Previous and current scm cpld versions matched. Pass.')
            else:
                 self.wpl_raiseException('Previous and current scm cpld versions do not match ! Fail')

        current_fcmcpld_version = parsedOutput.getValue('FCMCPLD_VER')[0]
        if current_fcmcpld_version == None:
            self.wpl_raiseException("current fcm cpld version not found !")
        else:
            self.wpl_log_debug('Previous fcm cpld version: [%s]' %self.old_fcmcpld_version)
            self.wpl_log_debug('Current fcm cpld version: [%s]' %current_fcmcpld_version)
            if self.old_fcmcpld_version == current_fcmcpld_version:
                self.wpl_log_debug('Previous and current fcm cpld versions matched. Pass.')
            else:
                 self.wpl_raiseException('Previous and current fcm cpld versions do not match ! Fail')

        self.wpl_log_success('verify_cpld_versions_after_flash_update test result: PASS')


#######################################################################################################################
# Function Name: verify_cpld_versions_after_flash_update
# Date         : 14th May 2020
# Author       : TK NG<tikng@celestica.com>
#
# Procedure Revision Details:
#   Version : 1.0  - Initial Draft  - by TK NG<tikng@celestica.com>
#######################################################################################################################
    def verify_cpld_versions_after_pwr_cycle(self, toolName, toolPath, cpldType='all'):
        self.wpl_log_debug('Entering procedure verify_cpld_versions_after_pwr_cycle with args : %s' %(str(locals())))
        cmd = 'cd ' + toolPath
        self.wpl_getPrompt("openbmc", 600)
        self.wpl_transmit(cmd)
        optionStr = ' '
        errCount = 0
        current_syscpld_version = '0'
        current_pwrcpld_version = '0'
        current_scmcpld_version = '0'
        current_fcmcpld_version = '0'
        output = self.EXEC_bmc_system_tool_command(toolName, optionStr, toolPath)
        self.wpl_log_debug(output)
        parsedOutput = parserDIAGLibs.PARSE_CPLD_Versions(output)

        current_syscpld_version = parsedOutput.getValue('SYSCPLD_VER')[0]
        if current_syscpld_version == None:
            self.wpl_raiseException("current_syscpld_version not found !")
        else:
            self.wpl_log_debug('Update syscpld version: [%s]' %self.syscpld_version)
            self.wpl_log_debug('Current syscpld version: [%s]' %current_syscpld_version)
            if self.syscpld_version == current_syscpld_version:
                self.wpl_log_debug('Current and update syscpld versions [%s] matched. Pass.' %current_syscpld_version)
            else:
                self.wpl_raiseException('Current and update syscpld versions do not match ! Fail')

        current_pwrcpld_version = parsedOutput.getValue('PWRCPLD_VER')[0]
        if current_pwrcpld_version == None:
            self.wpl_raiseException("current_pwrcpld_version not found !")
        else:
            self.wpl_log_debug('Update pwrcpld version: [%s]' %self.pwrcpld_version)
            self.wpl_log_debug('Current pwrcpld version: [%s]' %current_pwrcpld_version)
            if self.pwrcpld_version == current_pwrcpld_version:
                self.wpl_log_debug('Current and update pwrcpld versions [%s] matched. Pass' %current_pwrcpld_version)
            else:
                self.wpl_raiseException('Current and update pwrcpld versions do not match ! Fail.')

        current_scmcpld_version = parsedOutput.getValue('SCMCPLD_VER')[0]
        if current_scmcpld_version == None:
            self.wpl_raiseException("current_scmcpld_version not found !")
        else:
            self.wpl_log_debug('Update scmcpld version: [%s]' %self.scmcpld_version)
            self.wpl_log_debug('Current scmcpld version: [%s]' %current_scmcpld_version)
            if self.scmcpld_version == current_scmcpld_version:
                self.wpl_log_debug('Current and update scmcpld versions [%s] matched. Pass.' %current_scmcpld_version)
            else:
                self.wpl_raiseException('Current and update scmcpld versions do not match ! Fail.')

        current_fcmcpld_version = parsedOutput.getValue('FCMCPLD_VER')[0]
        if current_fcmcpld_version == None:
            self.wpl_raiseException("current_fcmcpld_version not found !")
        else:
            self.wpl_log_debug('Update fcmcpld version: [%s]' %self.fcmcpld_version)
            self.wpl_log_debug('Current fcmcpld version: [%s]' %current_fcmcpld_version)
            if self.fcmcpld_version == current_fcmcpld_version:
                self.wpl_log_debug('Current and update fcmcpld versions [%s] matched. Pass.' %current_fcmcpld_version)
            else:
                self.wpl_raiseException('Current and update fcmcpld versions do not match ! Fail.')

        self.wpl_log_success('verify_cpld_versions_after_flash_update test result: PASS')


#######################################################################################################################
# Function Name: set_max_openbmc_update_cycles
# Date         : 14th May 2020
# Author       : TK NG<tikng@celestica.com>
#
# Procedure Revision Details:
#   Version : 1.0  - Initial Draft  - by TK NG<tikng@celestica.com>
#######################################################################################################################
    def set_max_openbmc_update_cycles(self, max_cycles):
        self.wpl_log_debug('Entering procedure set_max_openbmc_update_cycles with args : %s' %(str(locals())))

        self.bmc_update_max_cycles = str(max_cycles)

        self.wpl_log_success('Successfully set_max_openbmc_update_cycles: [%s] cycles.\n' %(str(max_cycles)))


#######################################################################################################################
# Function Name: set_max_cpld_update_cycles
# Date         : 14th May 2020
# Author       : TK NG<tikng@celestica.com>
#
# Procedure Revision Details:
#   Version : 1.0  - Initial Draft  - by TK NG<tikng@celestica.com>
#######################################################################################################################
    def set_max_cpld_update_cycles(self, max_cycles):
        self.wpl_log_debug('Entering procedure set_max_cpld_update_cycles with args : %s' %(str(locals())))

        self.cpld_update_max_cycles = str(max_cycles)

        self.wpl_log_success('Successfully set_max_cpld_update_cycles: [%s] cycles.\n' %(str(max_cycles)))


#######################################################################################################################
# Function Name: check_system_log_dir_exists
# Date         : 14th May 2020
# Author       : TK NG<tikng@celestica.com>
#
# Procedure Revision Details:
#   Version : 1.0  - Initial Draft  - by TK NG<tikng@celestica.com>
#######################################################################################################################
    def check_system_log_dir_exists(self):
        self.wpl_log_debug('Entering procedure check_system_log_dir_exists\n')
        CommonLib.create_dir(AUTOMATION_ROOT_LOG_PATH, openbmc_mode)
        CommonLib.create_dir(SYSTEM_CONSOLE_LOG_PATH, openbmc_mode)


#######################################################################################################################
# Function Name: set_max_fpga_update_cycles
# Date         : 14th May 2020
# Author       : TK NG<tikng@celestica.com>
#
# Procedure Revision Details:
#   Version : 1.0  - Initial Draft  - by TK NG<tikng@celestica.com>
#######################################################################################################################
    def set_max_fpga_update_cycles(self, max_cycles):
        self.wpl_log_debug('Entering procedure set_max_fpga_update_cycles with args : %s' %(str(locals())))

        self.fpga_update_max_cycles = str(max_cycles)

        self.wpl_log_success('Successfully set_max_fpga_update_cycles: [%s] cycles.\n' %(str(max_cycles)))


#######################################################################################################################
# Function Name: read_cpld_fpga_bic_fw_versions
# Date         : 14th May 2020
# Author       : TK NG<tikng@celestica.com>
#
# Procedure Revision Details:
#   Version : 1.0  - Initial Draft  - by TK NG<tikng@celestica.com>
#######################################################################################################################
    def read_cpld_fpga_bic_fw_versions(self, toolName, dev, option, toolPath, logFile='None'):
        self.wpl_log_debug('Entering procedure read_cpld_fpga_bic_fw_versions with args : %s' %(str(locals())))
        cmd = 'cd ' + toolPath
        self.wpl_getPrompt("openbmc", 600)
        self.wpl_transmit(cmd)
        errCount = 0
        optionStr = (dev + ' ' + option)
        current_syscpld_version = '0'
        current_pwrcpld_version = '0'
        current_scmcpld_version = '0'
        current_fcmcpld_version = '0'
        current_fpga1_version = '0'
        current_fpga2_version = '0'
        current_bridge_version = '0'
        current_bridge_bootloader_version = '0'
        current_cpld_version = '0'
        output = self.EXEC_bmc_system_tool_command(toolName, optionStr, toolPath)
        self.wpl_log_debug(output)
        if logFile != 'None':
            self.wpl_send_output_to_log_file(output, logFile)

        parsedOutput = parserDIAGLibs.PARSE_CPLD_FPGA_BIC_Versions(output)

        # fcmcpld
        current_fcmcpld_version = parsedOutput.getValue('FCMCPLD_VER')[0]
        if current_fcmcpld_version == None:
            self.wpl_raiseException("current fcmcpld version not found !")
        else:
            self.wpl_log_success('Found current fcmcpld version: [%s]' %current_fcmcpld_version)

        # pwrcpld
        current_pwrcpld_version = parsedOutput.getValue('PWRCPLD_VER')[0]
        if current_pwrcpld_version == None:
            self.wpl_raiseException("current pwrcpld version not found !")
        else:
            self.wpl_log_success('Found current pwrcpld version: [%s]' %current_pwrcpld_version)

        # scmcpld
        current_scmcpld_version = parsedOutput.getValue('SCMCPLD_VER')[0]
        if current_scmcpld_version == None:
            self.wpl_raiseException("current scmcpld version not found !")
        else:
            self.wpl_log_success('Found current scmcpld version: [%s]' %current_scmcpld_version)

        # smbcpld
        current_smbcpld_version = parsedOutput.getValue('SMBCPLD_VER')[0]
        if current_smbcpld_version == None:
            self.wpl_raiseException("current smbcpld version not found !")
        else:
            self.wpl_log_success('Found current smbcpld version: [%s]' %current_smbcpld_version)

        # fpga1
        current_fpga1_version = parsedOutput.getValue('FPGA1_VER')[0]
        if current_fpga1_version == None:
            self.wpl_raiseException("current fpga1 version not found !")
        else:
            self.wpl_log_success('Found current fpga1 version: [%s]' %current_fpga1_version)

        # fpga2
        current_fpga2_version = parsedOutput.getValue('FPGA2_VER')[0]
        if current_fpga2_version == None:
            self.wpl_raiseException("current fpga2 version not found !")
        else:
            self.wpl_log_success('Found current fpga2 version: [%s]' %current_fpga2_version)

        # Bridge
        current_bridge_version = parsedOutput.getValue('BRIDGE_VER')[0]
        if current_bridge_version == None:
            self.wpl_raiseException("current bridge version not found !")
        else:
            self.wpl_log_success('Found current bridge version: [%s]' %current_bridge_version)

        # Bridge BootLoader
        current_bridge_bootloader_version = parsedOutput.getValue('BRIDGE_BOOTLOADER_VER')[0]
        if current_bridge_bootloader_version == None:
            self.wpl_raiseException("current bridge bootloader version not found !")
        else:
            self.wpl_log_success('Found current bridge bootloader version: [%s]' %current_bridge_bootloader_version)

        # CPLD
        current_cpld_version = parsedOutput.getValue('CPLD_VER')[0]
        if current_cpld_version == None:
            self.wpl_raiseException("current cpld version not found !")
        else:
            self.wpl_log_success('Found current cpld version: [%s]' %current_cpld_version)

        self.wpl_log_success('Successfully read_cpld_fpga_bic_fw_versions.\n')


#######################################################################################################################
# Function Name: platform_read_fw_sw_util_versions
# Date         : 14th May 2020
# Author       : TK NG<tikng@celestica.com>
#
# Procedure Revision Details:
#   Version : 1.0  - Initial Draft  - by TK NG<tikng@celestica.com>
#######################################################################################################################
    def platform_read_fw_sw_util_versions(self, toolName, optionStr, toolPath, toolName1, optionStr1, toolPath1, platform):
        self.wpl_log_debug('Entering procedure platform_read_fw_sw_util_versions with args : %s' %(str(locals())))

        cmd = 'cd ' + toolPath
        self.wpl_getPrompt("openbmc", 600)
        self.wpl_transmit(cmd)

        FW_ARRAY = []
        current_bmc_version = '0'
        current_tpm_version = '0'
        current_fcmcpld_version = '0'
        current_pwrcpld_version = '0'
        current_scmcpld_version = '0'
        current_smbcpld_version = '0'
        current_fpga1_version = '0'
        current_fpga2_version = '0'
        current_bridge_version = '0'
        current_bridge_bootloader_version = '0'
        current_bios_version = '0'
        current_cpld_version = '0'
        current_me_version = '0'
        current_pvccin_version = '0'
        current_ddrab_version = '0'
        current_p1v05_version = '0'
        current_diag_version = '0'

        output = self.EXEC_bmc_system_tool_command(toolName, optionStr, toolPath)
        self.wpl_log_debug(output)
        if platform == 'wedge400c':
            parsedOutput = parserDIAGLibs.WEDGE400C_PARSE_FW_UTIL_Versions(output)
        else:
            parsedOutput = parserDIAGLibs.CLOUDRIPPER_PARSE_FW_UTIL_Versions(output)

        # BMC
        current_bmc_version = parsedOutput.getValue('BMC_VER')[0]
        if current_bmc_version == 'NA':
            self.wpl_raiseException("current BMC version not found !")
        else:
            if 'dirty' in current_bmc_version:
                FW_ARRAY.append(current_bmc_version)
                self.wpl_log_success('Found current BMC version: [%s]' %current_bmc_version)
            else:
                if len(current_bmc_version) >= 4:
                    if re.search(r'^0\.[\d]+', current_bmc_version):
                        vstr = current_bmc_version
                        vlist = vstr.split('.')
                        if len(vlist) == 2:
                            # e.g. bmc version in ImageInfo.yaml shows 0.3 instead of 0.30
                            # so, remove trailing decimal point zeros from version to match
                            bmc_ver = float(current_bmc_version)
                            current_bmc_version = str(bmc_ver)
                FW_ARRAY.append(current_bmc_version)
                self.wpl_log_success('Found current BMC version: [%s]' %current_bmc_version)

        # TPM
        current_tpm_version = parsedOutput.getValue('TPM_VER')[0]
        if current_tpm_version == 'NA':
            self.wpl_raiseException("current TPM version not found !")
        else:
            FW_ARRAY.append(current_tpm_version)
            self.wpl_log_success('Found current TPM version: [%s]' %current_tpm_version)

        # FCMCPLD
        current_fcmcpld_version = parsedOutput.getValue('FCMCPLD_VER')[0]
        if current_fcmcpld_version == 'NA':
            self.wpl_raiseException("current FCMCPLD version not found !")
        else:
            FW_ARRAY.append(current_fcmcpld_version)
            self.wpl_log_success('Found current FCMCPLD version: [%s]' %current_fcmcpld_version)

        # PWRCPLD
        current_pwrcpld_version = parsedOutput.getValue('PWRCPLD_VER')[0]
        if current_pwrcpld_version == 'NA':
            self.wpl_raiseException("current PWRCPLD version not found !")
        else:
            FW_ARRAY.append(current_pwrcpld_version)
            self.wpl_log_success('Found current PWRCPLD version: [%s]' %current_pwrcpld_version)

        # SCMCPLD
        current_scmcpld_version = parsedOutput.getValue('SCMCPLD_VER')[0]
        if current_scmcpld_version == 'NA':
            self.wpl_raiseException("current SCMCPLD version not found !")
        else:
            FW_ARRAY.append(current_scmcpld_version)
            self.wpl_log_success('Found current SCMCPLD version: [%s]' %current_scmcpld_version)

        # SMBCPLD
        current_smbcpld_version = parsedOutput.getValue('SMBCPLD_VER')[0]
        if current_smbcpld_version == 'NA':
            self.wpl_raiseException("current SMBCPLD version not found !")
        else:
            FW_ARRAY.append(current_smbcpld_version)
            self.wpl_log_success('Found current SMBCPLD version: [%s]' %current_smbcpld_version)

        # FPGA1
        current_fpga1_version = parsedOutput.getValue('FPGA1_VER')[0]
        if current_fpga1_version == 'NA':
            self.wpl_raiseException("current FPGA1 version not found !")
        else:
            FW_ARRAY.append(current_fpga1_version)
            self.wpl_log_success('Found current FPGA1 version: [%s]' %current_fpga1_version)

        # FPGA2
        current_fpga2_version = parsedOutput.getValue('FPGA2_VER')[0]
        if current_fpga2_version == 'NA':
            self.wpl_raiseException("current FPGA2 version not found !")
        else:
            FW_ARRAY.append(current_fpga2_version)
            self.wpl_log_success('Found current FPGA2 version: [%s]' %current_fpga2_version)

        # BRIDGE IC
        current_bridge_version = parsedOutput.getValue('BRIDGE_VER')[0]
        if current_bridge_version == 'NA':
            self.wpl_raiseException("current BRIDGE IC version not found !")
        else:
            FW_ARRAY.append(current_bridge_version)
            self.wpl_log_success('Found current BRIDGE IC version: [%s]' %current_bridge_version)

        # BRIDGE IC BOOTLOADER
        current_bridge_bootloader_version = parsedOutput.getValue('BRIDGE_BOOTLOADER_VER')[0]
        if current_bridge_bootloader_version == 'NA':
            self.wpl_raiseException("current BRIDGE IC BOOTLOADER version not found !")
        else:
            FW_ARRAY.append(current_bridge_bootloader_version)
            self.wpl_log_success('Found current BRIDGE IC BOOTLOADER version: [%s]' %current_bridge_bootloader_version)

        # BIOS
        current_bios_version = parsedOutput.getValue('BIOS_VER')[0]
        if current_bios_version == 'NA':
            self.wpl_raiseException("current BIOS version not found !")
        else:
            FW_ARRAY.append(current_bios_version)
            self.wpl_log_success('Found current BIOS version: [%s]' %current_bios_version)

        # CPLD
        current_cpld_version = parsedOutput.getValue('CPLD_VER')[0]
        if current_cpld_version == 'NA':
            self.wpl_raiseException("current cpld version not found !")
        else:
            FW_ARRAY.append(current_cpld_version)
            self.wpl_log_success('Found current cpld version: [%s]' %current_cpld_version)

        # ME
        current_me_version = parsedOutput.getValue('ME_VER')[0]
        if current_me_version == 'NA':
            self.wpl_raiseException("current ME version not found !")
        else:
            FW_ARRAY.append(current_me_version)
            self.wpl_log_success('Found current ME version: [%s]' %current_me_version)

        # PVCCIN
        current_pvccin_version = parsedOutput.getValue('PVCCIN_VER')[0]
        if current_pvccin_version == 'NA':
            self.wpl_raiseException("current PVCCIN version not found !")
        else:
            FW_ARRAY.append(current_pvccin_version)
            self.wpl_log_success('Found current PVCCIN version: [%s]' %current_pvccin_version)

        # DDRAB
        current_ddrab_version = parsedOutput.getValue('DDRAB_VER')[0]
        if current_ddrab_version == 'NA':
            self.wpl_raiseException("current DDRAB version not found !")
        else:
            FW_ARRAY.append(current_ddrab_version)
            self.wpl_log_success('Found current DDRAB version: [%s]' %current_ddrab_version)

        # P1V05
        current_p1v05_version = parsedOutput.getValue('P1V05_VER')[0]
        if current_p1v05_version == 'NA':
            self.wpl_raiseException("current P1V05 version not found !")
        else:
            FW_ARRAY.append(current_p1v05_version)
            self.wpl_log_success('Found current P1V05 version: [%s]' %current_p1v05_version)

        # DIAG
        cmd1 = 'cd ' + toolPath1
        self.wpl_getPrompt("openbmc", 600)
        self.wpl_transmit(cmd1)

        output1 = self.EXEC_bmc_system_tool_command(toolName1, optionStr1, toolPath1)
        self.wpl_log_debug(output1)
        found = 0
        p1='DIAG[ \t]+:\s+([\d]+\.[\d]+\.[\d]+)'
        for line in output1.splitlines():
            line = line.strip()
            match1 = re.search(p1, line, re.IGNORECASE)
            if match1:
                found += 1
                diag_version = match1.group(1)
                current_diag_version = str(diag_version)
                FW_ARRAY.append(current_diag_version)
                self.wpl_log_success('Found current DIAG version: [%s]' %current_diag_version)

        if found == 0:
            self.wpl_raiseException("current DIAG version not found !")

        self.wpl_log_success('Successfully platform_read_fw_sw_util_versions.\n')
        return FW_ARRAY


#######################################################################################################################
# Function Name: read_fpga_pcie_fw_versions
# Date         : 14th May 2020
# Author       : TK NG<tikng@celestica.com>
#
# Procedure Revision Details:
#   Version : 1.0  - Initial Draft  - by TK NG<tikng@celestica.com>
#######################################################################################################################
    def read_fpga_pcie_fw_versions(self, toolName1, toolName2, logFile='None'):
        self.wpl_log_debug('Entering procedure read_fpga_pcie_fw_versions with args : %s' %(str(locals())))

        p1=fpga1_pcie_device_id_string
        p3=fpga2_pcie_device_id_string
        str1 = ''
        str2 = ''

        CommonLib.switch_to_centos(logFile)

        # fpga1
        cmd = toolName1
        self.wpl_log_debug("command = %s" % cmd)
        self.wpl_flush()
        output = self.wpl_execute(cmd, mode=centos_mode, timeout=60)
        if logFile != 'None':
            self.wpl_send_output_to_log_file(output, logFile)

        self.wpl_log_debug('%s' %output)
        found = 0
        for line in output.splitlines():
            pcieDeviceID1 = line.strip()
            match1 = re.search(p1, pcieDeviceID1, re.IGNORECASE)
            if match1:
                found = 1
                str1 = p1
                break

        if found:
            self.wpl_log_success('Found FGPA pcie1 device: [%s]' %str1)
        else:
            self.wpl_raiseException('FPGA pcie1 device not found ! Fail.')

        # fpga2
        cmd = toolName2
        self.wpl_log_debug("command = %s" % cmd)
        self.wpl_flush()
        output = self.wpl_execute(cmd, mode=centos_mode, timeout=60)
        self.wpl_log_debug('%s' %output)
        if logFile != 'None':
            self.wpl_send_output_to_log_file(output, logFile)

        found = 0
        for line in output.splitlines():
            pcieDeviceID2 = line.strip()
            match3 = re.search(p3, pcieDeviceID2, re.IGNORECASE)
            if match3:
                found = 1
                str2 = p3
                break

        if found:
            self.wpl_log_success('Found FGPA pcie2 device: [%s]' %str2)
        else:
            self.wpl_raiseException('FPGA pcie2 device not found ! Fail.')

        self.wpl_log_success('Successfully read_fpga_pcie_fw_versions.\n')


#######################################################################################################################
# Function Name: get_current_fpga_version
# Date         : 14th May 2020
# Author       : TK NG<tikng@celestica.com>
#
# Procedure Revision Details:
#   Version : 1.0  - Initial Draft  - by TK NG<tikng@celestica.com>
#######################################################################################################################
    def get_current_fpga_version(self, toolName, option, toolPath, dev):
        self.wpl_log_debug('Entering procedure get_current_fpga_version with args : %s' %(str(locals())))
        cmd = 'cd ' + toolPath
        self.wpl_getPrompt("openbmc", 600)
        self.wpl_transmit(cmd)
        errCount = 0
        current_fpga_version = '0'
        output = self.EXEC_bmc_system_tool_command(toolName, option, toolPath)
        self.wpl_log_debug(output)
        parsedOutput = parserDIAGLibs.PARSE_FPGA_Versions(output)

        if dev == 'DOM_FPGA_FLASH1':
            current_fpga_version = parsedOutput.getValue('FPGA1_VER')[0]
            if current_fpga_version == None:
                self.wpl_raiseException("current fpga1 version not found !")
            else:
                self.wpl_log_success('Found current fpga1 version: [%s]' %current_fpga_version)

        elif dev == 'DOM_FPGA_FLASH2':
            current_fpga_version = parsedOutput.getValue('FPGA2_VER')[0]
            if current_fpga_version == None:
                self.wpl_raiseException("current fpga2 version not found !")
            else:
                self.wpl_log_success('Found current fpga2 version: [%s]' %current_fpga_version)

        return current_fpga_version



#######################################################################################################################
# Function Name: flash_update_fpga_firmware
# Date         : 14th May 2020
# Author       : TK NG<tikng@celestica.com>
#
# Procedure Revision Details:
#   Version : 1.0  - Initial Draft  - by TK NG<tikng@celestica.com>
#######################################################################################################################
    def flash_update_fpga_firmware(self, toolName, opt, spiNum, dev, check_pattern, downgrade_image, upgrade_image,
                                              downgrade_ver, upgrade_ver, img_path, tool_path, logFile='None'):
        self.wpl_log_debug('Entering procedure flash_update_fpga_firmware with args : %s' %(str(locals())))
        update_fpga_image = ''
        found = False
        upgrade_fpga_flag = False
        upper_fpga_major_ver = 0
        upper_fpga_minor_ver = 0
        update_fpga_version = upgrade_ver

        # extract fpga version
        slist1 = update_fpga_version.split('.')
        upper_fpga_major_str = str(slist1[0])
        upper_fpga_minor_str = str(slist1[1])
        upper_fpga_major_ver = int(upper_fpga_major_str)
        upper_fpga_minor_ver = int(upper_fpga_minor_str)

        self.wpl_log_debug('upper %s major ver: [%s]' %(dev, upper_fpga_major_ver))
        self.wpl_log_debug('upper %s minor ver: [%s]' %(dev, upper_fpga_minor_ver))

        current_fpga_version = self.get_current_fpga_version(fpga_software_test, '-v', BMC_DIAG_TOOL_PATH, dev)
        if current_fpga_version == '0':
            self.wpl_raiseException("Failed flash_update_fpga_firmware")
        else:
            slist2 = current_fpga_version.split('.')
            cur_major_str = str(slist2[0])
            cur_minor_str = str(slist2[1])
            cur_fpga_major_ver = int(cur_major_str)
            cur_fpga_minor_ver = int(cur_minor_str)

            self.wpl_log_debug('current %s major ver=[%s]' %(dev, cur_fpga_major_ver))
            self.wpl_log_debug('current %s minor ver=[%s]' %(dev, cur_fpga_minor_ver))

            if cur_fpga_major_ver < upper_fpga_major_ver:
                # need to perform upgrade
                update_fpga_image = upgrade_image
                upgrade_fpga_flag = True
            elif cur_fpga_major_ver > upper_fpga_major_ver:
                # need to perform downgrade
                update_fpga_image = downgrade_image
                upgrade_fpga_flag = False
            else:
                if cur_fpga_minor_ver < upper_fpga_minor_ver:
                    # need to perform upgrade
                    update_fpga_image = upgrade_image
                    upgrade_fpga_flag = True
                else:
                    # need to perform downgrade
                    update_fpga_image = downgrade_image
                    upgrade_fpga_flag = False

            if logFile != 'None':
                loop_cnt = int(self.fpga_update_loop_count)
                if self.check_local_file_exists(logFile) == True:
                    if loop_cnt == 0:
                        self.remove_local_file(logFile)

                # write date/time to log file
                cmd = ('touch ' + logFile)
                self.wpl_log_debug("command = %s" %cmd)
                self.wpl_flush()
                output = self.wpl_exec_local_cmd(cmd)
                self.wpl_log_debug(output)

                cmd = ('echo \"[$(date +\'%cF_%cH-%cM-%cS\')] now version is %s\" | tee -a %s > /dev/null' %('%','%','%','%', current_fpga_version, logFile))
                self.wpl_log_debug("command = %s" %cmd)
                self.wpl_flush()
                output = self.wpl_exec_local_cmd(cmd)
                self.wpl_log_debug(output)

                # update test loop count
                loop_cnt += 1
                self.fpga_update_loop_count = str(loop_cnt)
                cmd = ('echo \"[$(date +\'%cF_%cH-%cM-%cS\')] -------------Test Loop %s------------\" | tee -a %s > /dev/null' %('%','%','%','%', self.fpga_update_loop_count, logFile))
                self.wpl_log_debug("command = %s" %cmd)
                self.wpl_flush()
                output = self.wpl_exec_local_cmd(cmd)
                self.wpl_log_debug(output)

                if upgrade_fpga_flag == True:
                    self.wpl_log_debug('Performing FPGA firmware upgrade to %s...\n' %update_fpga_image)
                    cmd = ('echo \"[$(date +\'%cF_%cH-%cM-%cS\')] Upgrade to %s\" | tee -a %s > /dev/null' %('%','%','%','%', upgrade_ver, logFile))
                else:
                    self.wpl_log_debug('Performing FPGA firmware downgrade to %s...\n' %update_fpga_image)
                    cmd = ('echo \"[$(date +\'%cF_%cH-%cM-%cS\')] Downgrade to %s\" | tee -a %s > /dev/null' %('%','%','%','%', downgrade_ver, logFile))

                self.wpl_log_debug("command = %s" %cmd)
                self.wpl_flush()
                output = self.wpl_exec_local_cmd(cmd)
                self.wpl_log_debug(output)

            # perform FPGA upgrade/downgrade
            self.spi_util_exec(toolName, opt, spiNum, dev, check_pattern, update_fpga_image, 'none', img_path, tool_path, logFile)

            if upgrade_fpga_flag == True:
                if dev == 'DOM_FPGA_FLASH1':
                    self.fpga1_version = upgrade_ver
                    self.wpl_log_success('Successfully flash upgraded FPGA1 firmware using DIAG tool - %s\n' %toolName)
                else:
                    self.fpga2_version = upgrade_ver
                    self.wpl_log_success('Successfully flash upgraded FPGA2 firmware using DIAG tool - %s\n' %toolName)
            else:
                if dev == 'DOM_FPGA_FLASH1':
                    self.fpga1_version = downgrade_ver
                    self.wpl_log_success('Successfully flash downgraded FPGA1 firmware using DIAG tool - %s\n' %toolName)
                else:
                    self.fpga2_version = downgrade_ver
                    self.wpl_log_success('Successfully flash downgraded FPGA2 firmware using DIAG tool - %s\n' %toolName)


#######################################################################################################################
# Function Name: verify_fpga_versions_after_flash_update
# Date         : 14th May 2020
# Author       : TK NG<tikng@celestica.com>
#
# Procedure Revision Details:
#   Version : 1.0  - Initial Draft  - by TK NG<tikng@celestica.com>
#######################################################################################################################
    def verify_fpga_versions_after_flash_update(self, toolName, option, toolPath):
        self.wpl_log_debug('Entering procedure verify_fpga_versions_after_flash_update with args : %s' %(str(locals())))

        current_fpga1_version = self.get_current_fpga_version(toolName, option, toolPath, 'DOM_FPGA_FLASH1')
        if current_fpga1_version == '0':
            self.wpl_raiseException("Failed get_current fpga1 version")
        else:
            if current_fpga1_version == self.fpga1_version:
                self.wpl_log_success('Successfully verified FPGA1 version[%s]' %self.fpga1_version)
            else:
                self.wpl_raiseException('Failed verify FPGA1 version. Update FPGA version:[%s]; Current FPGA version:[%s]' %(self.fpga1_version, current_fpga1_version))

        current_fpga2_version = self.get_current_fpga_version(toolName, option, toolPath, 'DOM_FPGA_FLASH2')
        if current_fpga2_version == '0':
            self.wpl_raiseException("Failed get current fpga2 version")
        else:
            if current_fpga2_version == self.fpga2_version:
                self.wpl_log_success('Successfully verified FPGA2 version[%s]' %self.fpga2_version)
            else:
                self.wpl_raiseException('Failed verify FPGA2 version. Update FPGA2 version:[%s]; Current FPGA2 version:[%s]' %(self.fpga2_version, current_fpga2_version))


#######################################################################################################################
# Function Name: get_pwd
# Date         : 14th May 2020
# Author       : TK NG<tikng@celestica.com>
#
# Procedure Revision Details:
#   Version : 1.0  - Initial Draft  - by TK NG<tikng@celestica.com>
#######################################################################################################################
    def get_pwd(self):
        self.wpl_log_debug('Entering procedure get_pwd')

        cmd = 'pwd'
        self.wpl_log_debug("command = %s" %cmd)
        self.wpl_flush()
        output = self.wpl_exec_local_cmd(cmd)
        self.wpl_log_debug('%s' %output)
        outputStr = output.strip()

        return outputStr


#######################################################################################################################
# Function Name: set_fpga_stress_time
# Date         : 14th May 2020
# Author       : TK NG<tikng@celestica.com>
#
# Procedure Revision Details:
#   Version : 1.0  - Initial Draft  - by TK NG<tikng@celestica.com>
#######################################################################################################################
    def set_fpga_stress_time(self, stress_time):
        self.wpl_log_debug('Entering procedure set_fpga_stress_time with args : %s' %(str(locals())))

        self.fpga_stress_time = str(stress_time)

        self.wpl_log_success('Successfully set_fpga_stress_time: [%s] seconds.\n' %stress_time)


#######################################################################################################################
# Function Name: perform_fpga_pcie_bus_stress_test
# Date         : 14th May 2020
# Author       : TK NG<tikng@celestica.com>
#
# Procedure Revision Details:
#   Version : 1.0  - Initial Draft  - by TK NG<tikng@celestica.com>
#######################################################################################################################
    def perform_fpga_pcie_bus_stress_test(self, toolName, runTime, toolPath):
        self.wpl_log_debug('Entering procedure perform_fpga_pcie_bus_stress_test : %s\n'%(str(locals())))

        # clear all the logs first
        cmd = 'dmesg -C'
        output = self.wpl_execute(cmd)
        cmd = 'cat /dev/null > /var/log/messages'
        output = self.wpl_execute(cmd)
        cmd = 'cat /dev/null > /var/log/mcelog'
        output = self.wpl_execute(cmd)

        cmd = 'cd ' + toolPath
        self.wpl_getPrompt("centos", 600)
        self.wpl_transmit(cmd)
        time.sleep(1)

        # execute fpga_stress.sh script
        cmd1 = './' + toolName + ' ' + runTime
        output = self.wpl_execute(cmd1)
        time.sleep(2)

        # check background process to determine whether process has completed
        max_loop_time = int(self.fpga_stress_time)
        # allow some more time for process to complete
        count = max_loop_time + 1800
        i = 0
        complete_flag = False
        test_started = False
        t1 = time.time()
        t2 = t1
        while complete_flag == False:
            time.sleep(1)
            i += 1
            cmd = 'ps ww'
            output = self.wpl_execute(cmd)
            if i == 1:
                self.wpl_log_debug('start checking ps output: %s' %output)

            match1 = re.search('fpga_io', output, re.IGNORECASE)
            if match1:
                test_started = True
                continue
            else:
                match2 = re.search('PCIE_BAR0_R_stress', output, re.IGNORECASE)
                if match2:
                    test_started = True
                    continue
                else:
                    match3 = re.search('PCIE_CFG_R_stress', output, re.IGNORECASE)
                    if match3:
                        test_started = True
                        continue
                    else:
                        complete_flag = True
                        t2 = time.time()
                        time_diff = int(t2 - t1)
                        if time_diff >= max_loop_time:
                            break
                        else:
                            # restart test process since max_loop_time have not reached
                            i = 0
                            complete_flag = False
                            test_started = False
                            output = self.wpl_execute(cmd1)
                            time.sleep(2)
                            continue

            t2 = time.time()
            time_diff = int(t2 - t1)
            if time_diff > count:
                self.wpl_raiseException("Timeout executing perform_fpga_pcie_bus_stress_test using \'%s\' tool." %(toolName))
            else:
                if (time_diff >= max_loop_time) and (time_diff < count):
                    if (time_diff % 300) == 0:
                        self.wpl_log_info('***Time elapsed: [%s] seconds***' %time_diff)

        self.wpl_log_debug('ps output = %s' %output)

        if test_started == False:
            self.wpl_raiseException("Error: FPGA PCIE background stress test process not started.")

        # check for error message in /var/log/messages
        cmd = 'cat /var/log/messages | grep -i'
        pattern = 'error'
        result = self.check_command_output(cmd, pattern)
        if result == False:
            self.wpl_log_fail('Error message found in /var/log/messages.')
            self.wpl_raiseException("Failed to perform_fpga_pcie_bus_stress_test")

        # check for fail message in /var/log/messages
        cmd = 'cat /var/log/messages | grep -i'
        pattern = 'fail'
        result = self.check_command_output(cmd, pattern)
        if result == False:
            self.wpl_log_fail('Fail message found in /var/log/messages.')
            self.wpl_raiseException("Failed to perform_fpga_pcie_bus_stress_test")

        self.wpl_log_info('Check /var/log/messages for error and fail messages...PASS')

        # check for error message in dmesg
        cmd = 'dmesg | grep -i'
        pattern = 'error'
        result = self.check_command_output(cmd, pattern)
        if result == False:
            self.wpl_log_fail('Error message found in dmesg.')
            self.wpl_raiseException("Failed to perform_fpga_pcie_bus_stress_test")

        # check for fail message in dmesg
        cmd = 'dmesg | grep -i'
        pattern = 'fail'
        result = self.check_command_output(cmd, pattern)
        if result == False:
            self.wpl_log_fail('Fail message found in dmesg.')
            self.wpl_raiseException("Failed to perform_fpga_pcie_bus_stress_test")

        self.wpl_log_info('Check dmesg for error and fail messages...PASS')

        # check for error message in /var/log/mcelog
        cmd = 'cat /var/log/mcelog | grep -i'
        pattern = 'error'
        result = self.check_command_output(cmd, pattern)
        if result == False:
            self.wpl_log_fail('Error message found in /var/log/mcelog.')
            self.wpl_raiseException("Failed to perform_fpga_pcie_bus_stress_test")

        # check for fail message in /var/log/mcelog
        cmd = 'cat /var/log/mcelog | grep -i'
        pattern = 'fail'
        result = self.check_command_output(cmd, pattern)
        if result == False:
            self.wpl_log_fail('Fail message found in /var/log/mcelog.')
            self.wpl_raiseException("Failed to perform_fpga_pcie_bus_stress_test")

        self.wpl_log_info('Check /var/log/mcelog for error and fail messages...PASS')

        self.wpl_log_success("Successfully completed perform_fpga_pcie_bus_stress_test using \'%s\' tool for %s seconds. PASSED." %(toolName, runTime))


#######################################################################################################################
# Function Name: check_command_output
# Date         : 14th May 2020
# Author       : TK NG<tikng@celestica.com>
#
# Procedure Revision Details:
#   Version : 1.0  - Initial Draft  - by TK NG<tikng@celestica.com>
#######################################################################################################################
    def check_command_output(self, cmd, err_pattern):
        self.wpl_log_debug('Entering procedure check_command_output: %s\n'%(str(locals())))

        command = (cmd + ' ' + '"' + err_pattern + '"')
        output = self.wpl_execute(command)
        for line in output.splitlines():
            line = line.strip()
            match = re.search(cmd, line, re.IGNORECASE)
            if match:
                continue

            match1 = re.search(err_pattern, line, re.IGNORECASE)
            if match1:
                if 'error' in err_pattern:
                    self.wpl_log_fail('Detected error message in output:\r\n[%s]' %line)
                elif 'fail' in err_pattern:
                    self.wpl_log_fail('Detected fail message in output:\r\n[%s]' %line)
                else:
                    self.wpl_log_fail('Detected:\r\n[%s]' %line)
                return False

        return True


#######################################################################################################################
# Function Name: set_ipmi_stress_time
# Date         : 14th May 2020
# Author       : TK NG<tikng@celestica.com>
#
# Procedure Revision Details:
#   Version : 1.0  - Initial Draft  - by TK NG<tikng@celestica.com>
#######################################################################################################################
    def set_ipmi_stress_time(self, stress_time):
        self.wpl_log_debug('Entering procedure set_ipmi_stress_time with args : %s' %(str(locals())))

        self.ipmi_stress_time = str(stress_time)

        self.wpl_log_success('Successfully set_ipmi_stress_time: [%s] seconds.\n' %stress_time)


#######################################################################################################################
# Function Name: set_ipmi_stress_cycles
# Date         : 14th May 2020
# Author       : TK NG<tikng@celestica.com>
#
# Procedure Revision Details:
#   Version : 1.0  - Initial Draft  - by TK NG<tikng@celestica.com>
#######################################################################################################################
    def set_ipmi_stress_cycles(self, max_cycles):
        self.wpl_log_debug('Entering procedure set_ipmi_stress_cycles with args : %s' %(str(locals())))

        self.ipmi_stress_cycles = str(max_cycles)

        self.wpl_log_success('Successfully set_ipmi_stress_cycles: [%s] cycles.\n' %(str(max_cycles)))


#######################################################################################################################
# Function Name: perform_ipmi_interface_stress_test
# Date         : 14th May 2020
# Author       : TK NG<tikng@celestica.com>
#
# Procedure Revision Details:
#   Version : 1.0  - Initial Draft  - by TK NG<tikng@celestica.com>
#######################################################################################################################
    def perform_ipmi_interface_stress_test(self, toolName, optionStr, pattern, toolPath):
        self.wpl_log_debug('Entering procedure perform_ipmi_interface_stress_test : %s\n'%(str(locals())))

        cmd = 'cd ' + toolPath
        self.wpl_getPrompt("centos", 600)
        self.wpl_transmit(cmd)
        time.sleep(1)

        found = False
        max_cycles = int(self.ipmi_stress_cycles)
        t1 = time.time()
        for i in range(0, max_cycles):
            self.wpl_log_info('************************************************************')
            self.wpl_log_info('*** Test Repeat Loop #: %s / %s ***' %((i+1), str(max_cycles)))
            self.wpl_log_info('************************************************************')

            # execute ipmi command
            cmd = './' + toolName + ' ' + optionStr
            output = self.wpl_execute(cmd)

            self.wpl_log_info("Checking \'%s\' output..." %(toolName))

            for line in output.splitlines():
                match = re.search('root@', line, re.IGNORECASE)
                if match:
                    continue

                line = line.strip()
                if len(line) == 0:
                    # blank line
                    continue
                else:
                    #self.wpl_log_info('%s' %line)
                    found = False
                    for i in pattern:
                        match1 = re.search(i, line, re.IGNORECASE)
                        if match1:
                            self.wpl_log_info('Found: %s' %line)
                            found = True
                            break
                    if found:
                       continue
                    else:
                        match2 = re.search('error', line, re.IGNORECASE)
                        if match2:
                            self.wpl_log_fail('Error in \'%s\' output: [%s]' %(toolName, line))
                        else:
                            match3 = re.search('fail', line, re.IGNORECASE)
                            if match3:
                                self.wpl_log_fail('Failed \'%s\' command: [%s]'  %(toolName, line))
                            else:
                                self.wpl_log_fail('Unrecognized \'%s\' output: [%s]' %(toolName, line))
                        self.wpl_raiseException("Failed perform_ipmi_interface_stress_test.")

            self.wpl_log_success("Checked \'%s\' output: PASSED." %(toolName))

            t2 = time.time()
            time_diff = int(t2 - t1)
            self.wpl_log_info('***Time elapsed: [%s] seconds***' %time_diff)

        self.wpl_log_success("Successfully perform_ipmi_interface_stress_test using \'%s\' tool. PASSED." %toolName)


#######################################################################################################################
# Function Name: diagLib_exec_ping
# Date         : 14th May 2020
# Author       : TK NG<tikng@celestica.com>
#
# Procedure Revision Details:
#   Version : 1.0  - Initial Draft  - by TK NG<tikng@celestica.com>
#######################################################################################################################
    def diagLib_exec_ping(self, ipAddr, count, mode, dest_mode, expected):
        self.wpl_log_debug('Entering procedure diagLib_exec_ping: %s\n'%(str(locals())))

        time.sleep(2)

        if mode != dest_mode:
            if dest_mode == 'centos':
                CommonLib.switch_to_centos()
                tmp_ipAddr = self.diagLib_check_centos_ip_address(ipAddr)
                CommonLib.switch_to_openbmc()
            else:
                CommonLib.switch_to_openbmc()
                tmp_ipAddr = self.diagLib_check_openbmc_ip_address(ipAddr)
                CommonLib.switch_to_centos()

        else:  # mode == dest_mode
            if dest_mode == 'centos':
                tmp_ipAddr = self.diagLib_check_centos_ip_address(ipAddr)
            else:
                tmp_ipAddr = self.diagLib_check_openbmc_ip_address(ipAddr)

        time.sleep(2)

        return CommonLib.exec_ping(Const.DUT, tmp_ipAddr, count, mode, expected)


#######################################################################################################################
# Function Name: diagLib_check_centos_ip_address
# Date         : 14th May 2020
# Author       : TK NG<tikng@celestica.com>
#
# Procedure Revision Details:
#   Version : 1.0  - Initial Draft  - by TK NG<tikng@celestica.com>
#######################################################################################################################
    def diagLib_check_centos_ip_address(self, ipAddr):
        self.wpl_log_debug('Entering procedure diagLib_check_centos_ip_address with args : %s' %(str(locals())))

        # check whether dhcp ipv6 still present, if not request from dhcp server
        var_centos_ipAddr = ''
        preferred_network = ''
        tmp_ipAddr = ipAddr
        if re.search(':', tmp_ipAddr):
            slist = tmp_ipAddr.split(':')
            preferred_network = slist[0]
        else:
            self.wpl_raiseException('Error: Unable to get valid centos IPV6 network.')

        var_interface = centos_eth_params['interface']
        ipList = CommonLib.check_ip_address_list(Const.DUT, var_interface, 'centos', preferred_network, True)
        if ipList is None:
            dLibObj.wpl_raiseException('Error: Unable to get preferred IPV6 address in centos.')
        else:
            for ipAddr in ipList:
                self.wpl_log_info('Searching preferred ip address: %s...'%(ipAddr))
                match = re.search(preferred_network, ipAddr)
                if match:
                    var_centos_ipAddr = ipAddr
                    found = True
                    self.wpl_log_info('Found preferred ip address: %s'%(var_centos_ipAddr))
                    break

            if found:
                return var_centos_ipAddr
            else:
                dLibObj.wpl_raiseException('Error: Unable to get preferred IPV6 address in centos.')


#######################################################################################################################
# Function Name: diagLib_check_openbmc_ip_address
# Date         : 14th May 2020
# Author       : TK NG<tikng@celestica.com>
#
# Procedure Revision Details:
#   Version : 1.0  - Initial Draft  - by TK NG<tikng@celestica.com>
#######################################################################################################################
    def diagLib_check_openbmc_ip_address(self, ipAddr):
        self.wpl_log_debug('Entering procedure diagLib_check_openbmc_ip_address with args : %s' %(str(locals())))

        # check whether dhcp ipv6 still present, if not request from dhcp server
        var_openbmc_ipAddr = ''
        preferred_network = ''
        tmp_ipAddr = ipAddr
        if re.search(':', tmp_ipAddr):
            slist = tmp_ipAddr.split(':')
            preferred_network = slist[0]
        else:
            self.wpl_raiseException('Error: Unable to get valid openbmc IPV6 network.')

        var_interface = openbmc_eth_params['interface']
        ipList = CommonLib.check_ip_address_list(Const.DUT, var_interface, 'openbmc', preferred_network, True)
        if ipList is None:
            dLibObj.wpl_raiseException('Error: Unable to get preferred IPV6 address in openbmc.')
        else:
            for ipAddr in ipList:
                self.wpl_log_info('Searching preferred ip address: %s...'%(ipAddr))
                match = re.search(preferred_network, ipAddr)
                if match:
                    var_openbmc_ipAddr = ipAddr
                    found = True
                    self.wpl_log_info('Found preferred ip address: %s'%(var_openbmc_ipAddr))
                    break

            if found:
                return var_openbmc_ipAddr
            else:
                dLibObj.wpl_raiseException('Error: Unable to get preferred IPV6 address in openbmc.')


#######################################################################################################################
# Function Name: set_openbmc_utility_stress_time
# Date         : 14th May 2020
# Author       : TK NG<tikng@celestica.com>
#
# Procedure Revision Details:
#   Version : 1.0  - Initial Draft  - by TK NG<tikng@celestica.com>
#######################################################################################################################
    def set_openbmc_utility_stress_time(self, stress_time):
        self.wpl_log_debug('Entering procedure set_openbmc_utility_stress_time with args : %s' %(str(locals())))

        self.openbmc_utility_stress_time = str(stress_time)

        self.wpl_log_success('Successfully set_openbmc_utility_stress_time: [%s] seconds.\n' %stress_time)


#######################################################################################################################
# Function Name: set_openbmc_utility_stress_cycles
# Date         : 14th May 2020
# Author       : TK NG<tikng@celestica.com>
#
# Procedure Revision Details:
#   Version : 1.0  - Initial Draft  - by TK NG<tikng@celestica.com>
#######################################################################################################################
    def set_openbmc_utility_stress_cycles(self, max_cycles):
        self.wpl_log_debug('Entering procedure set_openbmc_utility_stress_cycles with args : %s' %(str(locals())))

        self.openbmc_utility_stress_cycles = str(max_cycles)

        self.wpl_log_success('Successfully set_openbmc_utility_stress_cycles: [%s] cycles.\n' %(str(max_cycles)))


#######################################################################################################################
# Function Name: start_openbmc_utility_stability_test
# Date         : 14th May 2020
# Author       : TK NG<tikng@celestica.com>
#
# Procedure Revision Details:
#   Version : 1.0  - Initial Draft  - by TK NG<tikng@celestica.com>
#######################################################################################################################
    def start_openbmc_utility_stability_test(self, toolName1, optionList1, patternList1, toolName2, optionList2, patternList2, toolPath, openbmc_ipAddr, centos_ipAddr):
        self.wpl_log_debug('Entering procedure start_openbmc_utility_stability_test : %s\n'%(str(locals())))

        loop_flag = False
        cmd = 'cd ' + toolPath
        CommonLib.switch_to_openbmc('None')
        self.wpl_transmit(cmd)

        self.check_system_log_dir_exists()

        #stress_time = int(self.openbmc_utility_stress_time)
        t1 = time.time()
        #while loop_flag == False:
        max_cycles = int(self.openbmc_utility_stress_cycles)
        for i in range(0, max_cycles):
            self.wpl_log_info('************************************************************')
            self.wpl_log_info('*** Test Repeat Loop #: %s / %s ***' %((i+1), str(max_cycles)))
            self.wpl_log_info('************************************************************')
            complete_flag = False
            found1 = False
            index = 1
            count1 = 0
            count2 = 0
            output1 = ''
            output2 = ''

            for fwOptStr in optionList1:
                logFileName1 = ('%sfwUtilLogFile%s.log' %(SYSTEM_CONSOLE_LOG_PATH, str(index)))
                #cmd1 = ('%s %s > %s&' %(toolName1, str(fwOptStr), logFileName1))
                cmd1 = ('%s %s' %(toolName1, str(fwOptStr)))
                cmd1Path = (cmd1 + ' > %s&' %logFileName1)
                pattern1 = patternList1[count1]
                index += 1
                for bicOptStr in optionList2:
                    logFileName2 = ('%sbicUtilLogFile%s.log' %(SYSTEM_CONSOLE_LOG_PATH, str(index)))
                    #cmd2 = ('%s %s > %s&' %(toolName2, str(bicOptStr), logFileName2))
                    cmd2 = ('%s %s' %(toolName2, str(bicOptStr)))
                    cmd2Path = (cmd2 + ' > %s&' %logFileName2)
                    pattern2 = patternList2[count2]
                    index += 1
                    # run both commands at the background in parallel
                    self.wpl_log_debug(cmd1Path)
                    self.wpl_log_debug(cmd2Path)
                    self.wpl_transmit(cmd2Path)
                    self.wpl_transmit(cmd1Path)
                    complete_flag = False
                    # wait for both background process to complete
                    while complete_flag == False:
                        output = self.wpl_execute('ps', mode=openbmc_mode, timeout=60)
                        if re.search(toolName1, output, re.IGNORECASE):
                            continue
                        if re.search(toolName2, output, re.IGNORECASE):
                            continue
                        complete_flag = True
                    count2 += 1

                    time.sleep(1)
                    self.wpl_log_debug("Checking output of command[%s]..." % cmd1)

                    # check output of fw-util
                    cmd = ('cat %s' %logFileName1)
                    output1 = self.wpl_execute(cmd)
                    self.wpl_log_success("Lines1[%s]" %output1)
                    for pt in pattern1:
                        found1 = False
                        for line1 in output1.splitlines():
                            match1 = re.search(pt, line1, re.IGNORECASE)
                            if match1:
                                found1 = True
                                break
                        if found1 == False:
                            raise RuntimeError("Line pattern[%s] not found in cmd[%s] output." %(pt, cmd1))

                    if self.openbmc_utility_check_output(output1):
                        raise RuntimeError("Command[%s] Failed." %cmd1)

                    self.wpl_log_success("Check command[%s] output: Passed." % cmd1)

                    self.wpl_log_debug("Checking output of command[%s]..." % cmd2)

                    # check output of bic-util
                    cmd = ('cat %s' %logFileName2)
                    out2 = self.wpl_execute(cmd)
                    if re.search("sensor_num:", out2, re.IGNORECASE):
                        output2 = self.cleanup_output(out2)
                    else:
                        output2 = out2

                    for pt in pattern2:
                        found2 = False
                        for line2 in output2.splitlines():
                            match2 = re.search(pt, line2, re.IGNORECASE)
                            if match2:
                                found2 = True
                                break
                        if found2 == False:
                            raise RuntimeError("Line pattern[%s] not found in cmd[%s] output." %(pt, cmd2))

                    if self.openbmc_utility_check_output(output2):
                        raise RuntimeError("Command[%s] Failed." %cmd2)

                    self.wpl_log_success("Check command[%s] output: Passed." % cmd2)

                    # make sure openbmc OS still alive
                    self.diagLib_exec_ping(openbmc_ipAddr, 5, 'openbmc', 'openbmc', 'None')
                    self.wpl_log_success('Checked openbmc still alive.')

                    # make sure centos OS still alive
                    self.diagLib_exec_ping(centos_ipAddr, 5, 'openbmc', 'centos', 'None')
                    self.wpl_log_success('Checked centos still alive.')

                count1 += 1
                count2 = 0

            #time.sleep(1)
            t2 = time.time()
            time_diff = int(t2 - t1)
            self.wpl_log_info('***Time elapsed: [%s]***' %(str(time_diff)))

            #if time_diff > stress_time:
            #    # test completed
            #    break

        self.wpl_log_success("Successfully start_openbmc_utility_stability_test using \'%s\' and \'%s\' tools. PASSED." %(toolName1, toolName2))

    def get_cpu_tech(self):
        self.wpl_log_debug('Entering procedure get_cpu_tech with args : %s' %(str(locals())))
        p_16nm = "^cpu_16nm=\d+"
        p_7nm = "^cpu_7nm=\d+"
        match_flag = 0
        tech_name = "16nm"
        for pim in range(1,9):
            cmd_16nm = "echo cpu_16nm=$(./fpga mdio r pim={} type=1f phy=1 0x5200cb20 ".format(pim)
            cmd_16nm += "|grep ':' |awk -F: '{print $2}' |grep -Eo '0+[1-9]+')\n"
            cmd_7nm = "echo cpu_7nm=$(./fpga mdio r pim={} type=1f phy=1 0x5201D000 ".format(pim)
            cmd_7nm += "|grep ':' |awk -F: '{print $2}' |grep -Eo '0+[1-9]+')\n"
            finish_prompt = "\ncpu_[\s\S]+{}".format(self.device.promptDiagOS.replace("@","\@"))
            output = self.device.sendCmdRegexp(cmd_16nm, finish_prompt, timeout=3)
            output += self.device.sendCmdRegexp(cmd_7nm, finish_prompt, timeout=3)
            if re.search(p_16nm, output, re.M):
                match_flag = 1
            elif re.search(p_7nm, output, re.M):
                 tech_name = "7nm"
                 match_flag = 1
            if match_flag:
                log.info("Find CPU tech: {}".format(tech_name))
                break

        if match_flag == 0:
            self.wpl_log_info("Warning: didn't get CPU transistor technology, use 16nm as default.")

        return tech_name

    def startup_default_port(self, use_xphyback=True, init_cmd=None):
        self.wpl_log_debug('Entering procedure startup_default_port with args : %s' %(str(locals())))
        cmd = ""
        check_status = 0
        pim_counts = 0
        pim_counts = self.mp2_pim_count()
        if pim_counts == 3:
            init_cmd = xphy_init_mode2_pim5
        elif pim_counts == 4:
            init_cmd = xphy_init_mode2_pim4
            
        cmd = 'cd ' + sdk_working_dir + '/v*'
        self.wpl_transmit(cmd)
        if use_xphyback:
            cpu_tech_name = self.get_cpu_tech()
            xphyback = xphyback_dict.get(cpu_tech_name)
            cmd = "./{}& sleep 5; ".format(xphyback)
        if init_cmd:
            cmd += init_cmd + "; sleep 1; "
        if use_xphyback and init_cmd:
            cmd = "p_num=`ps -ef |grep xphyback |grep -v grep |wc -l`; if [[ $p_num -eq 0 ]];then {} fi;".format(cmd)
        elif use_xphyback == False and init_cmd:
            cmd = init_cmd
        cmd += "\n sleep 2; ps -ef |grep xphyback |grep -v grep "
        finish_prompt = "{}[\s\S]+{}".format("tty.*?xphyback", self.device.promptDiagOS)
        output = self.device.sendCmdRegexp(cmd, finish_prompt, timeout=1800)
        check_status = self.check_output(output, patterns=fail_pattern, line_mode=True, is_negative_test=True, remark="startup_default_port")

        if check_status:
            self.wpl_log_info('startup_default_port is passed\n')
        else:
            self.wpl_raiseException("startup_default_port failed")

    def check_output(self, output, patterns=[""], timeout=60, line_mode=True, is_negative_test=False, remark=""):
        self.wpl_log_debug('Entering procedure check_output ')
        passCount = 0
        patternNum = len(patterns)
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
                match = re.search(p_pass, output, re.M)
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
        ret_code = 0
        if remark:
            description = remark
        else:
            description = "All patterns "
        if passCount == patternNum:
            ret_code = 1
            self.wpl_log_success('%s is PASSED\n' %description)
        else:
            self.wpl_log_fail('Exiting check_output with result FAIL, {} fail with pattern: {}'.format(remark, mismatch_pattern))

        return ret_code
#######################################################################################################################
# Function Name: perform_openbmc_utility_stability_test
# Date         : 14th May 2020
# Author       : TK NG<tikng@celestica.com>
#
# Procedure Revision Details:
#   Version : 1.0  - Initial Draft  - by TK NG<tikng@celestica.com>
#######################################################################################################################
    def perform_openbmc_utility_stability_test(self, toolName1, optionStr1, patternList1, toolName2, optionStr2, patternList2, toolPath, fw_ver_array, var_platform):
        self.wpl_log_debug('Entering procedure perform_openbmc_utility_stability_test : %s\n'%(str(locals())))

        cmd = 'cd ' + toolPath
        CommonLib.switch_to_openbmc()
        self.wpl_transmit(cmd)

        max_cycles = int(self.openbmc_utility_stress_cycles)
        t1 = time.time()
        for i in range(0, max_cycles):
            self.wpl_log_info('************************************************************')
            self.wpl_log_info('*** Test Repeat Loop #: %s / %s ***' %((i+1), str(max_cycles)))
            self.wpl_log_info('************************************************************')

            found1 = False
            found2 = False
            output1 = ''
            output2 = ''

            # execute bic-util command
            cmd2 = ('%s %s' %(toolName2, optionStr2))
            output2 = self.wpl_execute(cmd2)

            self.wpl_log_info('Checking \'%s\' output...' %toolName2)

            # check bic-util output
            for line2 in output2.splitlines():
                match2 = re.search('root@', line2, re.IGNORECASE)
                if match2:
                    continue

                line2 = line2.strip()
                if len(line2) == 0:
                    # blank line
                    continue
                else:
                    #self.wpl_log_info('%s' %line2)
                    found2 = False
                    for j in patternList2:
                        match2 = re.search(j, line2, re.IGNORECASE)
                        if match2:
                            self.wpl_log_info('Found: %s' %line2)
                            found2 = True
                            break

                    if found2:
                        continue
                    else:
                        match5 = re.search('error', line2, re.IGNORECASE)
                        if match5:
                            self.wpl_log_fail('Error in \'%s\' output: [%s]' %(toolName2, line2))
                        else:
                            match6 = re.search('fail', line2, re.IGNORECASE)
                            if match6:
                                self.wpl_log_fail('Failed \'%s\' command: [%s]'  %(toolName2, line2))
                            else:
                                self.wpl_log_fail('Unrecognized \'%s\' output: [%s]' %(toolName2, line2))
                        self.wpl_raiseException('Failed perform_openbmc_utility_stability_test.')

            self.wpl_log_success("Checked \'%s\' output: PASSED." %toolName2)

            # execute fw-util command
            cmd1 = ('%s %s' %(toolName1, optionStr1))
            output1 = self.wpl_execute(cmd1)

            self.wpl_log_info('Checking \'%s\' output...' %toolName1)

            # check fw-util output
            for line1 in output1.splitlines():
                match1 = re.search('root@', line1, re.IGNORECASE)
                if match1:
                    continue

                line1 = line1.strip()
                if len(line1) == 0:
                    # blank line
                    continue
                else:
                    #self.wpl_log_info(line1)
                    found1 = False
                    for i in patternList1:
                        match1 = re.search(i, line1, re.IGNORECASE)
                        if match1:
                            found1 = True
                            if var_platform == 'wedge400c_cloudripper':
                                result = self.check_fw_versions(line1, fw_ver_array)
                                if result:
                                    self.wpl_raiseException('Failed perform_openbmc_utility_stability_test.')
                            elif var_platform == 'minipack2':
                                result = self.minipack2_check_fw_versions(line1, fw_ver_array)
                                if result:
                                    self.wpl_raiseException('Failed perform_openbmc_utility_stability_test.')
                            break

                    if found1:
                        continue
                    else:
                        # skip known issue
                        if re.search('Error getting version of fscd', line1, re.IGNORECASE):
                            continue

                    #    match3 = re.search('error', line1, re.IGNORECASE)
                     #   if match3:
                      #      self.wpl_log_fail('Error in \'%s\' output: [%s]' %(toolName1, line1))
                       # else:
                         #   match4 = re.search('fail', line1, re.IGNORECASE)
                        #    if match4:
                       #         self.wpl_log_fail('Failed \'%s\' command: [%s]'  %(toolName1, line1))
                      #      else:
                     #           self.wpl_log_fail('Unrecognized \'%s\' output: [%s]' %(toolName1, line1))
                    #    self.wpl_raiseException('Failed perform_openbmc_utility_stability_test.')

            self.wpl_log_success("Checked \'%s\' output: PASSED." %toolName1)

            t2 = time.time()
            time_diff = int(t2 - t1)
            self.wpl_log_info('***Time elapsed: [%s]***' %(str(time_diff)))

        # check centos status
        self.wpl_log_info('Checking centos status...')
        CommonLib.switch_to_centos()
        cmd3 = 'ps'
        self.wpl_log_info('command = %s' % cmd3)
        output3 = self.wpl_execute(cmd3)
        if re.search('bash', output3, re.IGNORECASE):
            self.wpl_log_info('Checked centos status: PASSED.')
            self.wpl_log_success("Successfully perform_openbmc_utility_stability_test using \'%s\' and \'%s\' tools. PASSED." %(toolName1, toolName2))
        else:
            self.wpl_log_fail('Error: no output from \'%s\' command in centos.\r\n' %cmd3)
            self.wpl_log_info('Checked centos status: FAILED.')
            self.wpl_raiseException('Failed to perform_openbmc_utility_stability_test.')


#######################################################################################################################
# Function Name: check_fw_versions
# Date         : 14th May 2020
# Author       : TK NG<tikng@celestica.com>
#
# Procedure Revision Details:
#   Version : 1.0  - Initial Draft  - by TK NG<tikng@celestica.com>
#######################################################################################################################
    def check_fw_versions(self, versionStr, fw_ver_array):
        self.wpl_log_debug('Entering procedure check_fw_versions: %s\n'%(str(locals())))

        found = 0
        fwStr = '0'
        fw_name = ['BMC', 'TPM', 'FCMCPLD', 'PWRCPLD', 'SCMCPLD', 'SMBCPLD', 'DOMFPGA1', 'DOMFPGA2', 'Bridge-IC Version', 'Bridge-IC Bootloader Version', 'BIOS', 'CPLD', 'ME', 'PVCCIN', 'DDRAB', 'P1V05']

        for i in range(0,16):
            fwStr = fw_name[i]

            if re.search('ALTBMC', versionStr, re.IGNORECASE):
                continue

            if re.search(fwStr, versionStr, re.IGNORECASE):
                fw_ver = fw_ver_array[i]
                found = 1
                break

        if found:
            if re.search(fw_ver, versionStr, re.IGNORECASE):
                self.wpl_log_info('Found %s' %versionStr)
                return 0
            else:
                # return error
                self.wpl_log_fail('Error: %s version not match[%s]. Expected %s.\r\n' %(fwStr, versionStr, fw_ver))
                return 1
        else:
            # non-version string
            return 0


#######################################################################################################################
# Function Name: minipack2_check_fw_versions
# Date         : 14th May 2020
# Author       : TK NG<tikng@celestica.com>
#
# Procedure Revision Details:
#   Version : 1.0  - Initial Draft  - by TK NG<tikng@celestica.com>
#######################################################################################################################
    def minipack2_check_fw_versions(self, versionStr, fw_ver_array):
        self.wpl_log_debug('Entering procedure minipack2_check_fw_versions: %s\n'%(str(locals())))

        found = 0
        fwStr = '0'
        fw_name = ['BMC', 'TPM', 'FCMCPLD B', 'FCMCPLD T', 'PWRCPLD L', 'PWRCPLD R', 'SCMCPLD', 'SMBCPLD', 'IOB FPGA', 'PIM1 DOMFPGA', 'PIM2 DOMFPGA', 'PIM3 DOMFPGA', 'PIM4 DOMFPGA', 'PIM5 DOMFPGA', 'PIM6 DOMFPGA', 'PIM7 DOMFPGA', 'PIM8 DOMFPGA', 'Bridge-IC Version', 'Bridge-IC Bootloader Version', 'BIOS', 'CPLD', 'ME', 'PVCCIN', 'DDRAB', 'P1V05']

        for i in range(0,len(fw_name)):
            fwStr = fw_name[i]

            if re.search('ALTBMC', versionStr, re.IGNORECASE):
                continue

            if re.search(fwStr, versionStr, re.IGNORECASE):
                fw_ver = fw_ver_array[i]
                found = 1
                break

        if found:
            if re.search(fw_ver, versionStr, re.IGNORECASE):
                self.wpl_log_info('Found %s' %versionStr)
                return 0
            else:
                # return error
                self.wpl_log_fail('Error: %s version not match[%s]. Expected %s.\r\n' %(fwStr, versionStr, fw_ver))
                return 1
        else:
            # non-version string
            return 0


#######################################################################################################################
# Function Name: cleanup_output
# Date         : 14th May 2020
# Author       : TK NG<tikng@celestica.com>
#
# Procedure Revision Details:
#   Version : 1.0  - Initial Draft  - by TK NG<tikng@celestica.com>
#######################################################################################################################
    def cleanup_output(self, output):
        self.wpl_log_debug('Entering procedure cleanup_output: %s\n'%(str(locals())))

        addLine = False
        output1 = ''
        previous_line = ''
        for sline in output.splitlines():
            addLine = False
            line = sline.strip()
            if re.search(r'(^type:[ \t]([\d]+))', line, re.IGNORECASE):
                if re.search(r'(rb_exp:[ \t]([\d]+)),$', line, re.IGNORECASE):
                    output1 += (line + '\r\n')
                    addLine = True

            if addLine == False:
                line1 = line.strip()
                if len(line1) == 0:
                    continue
                else:
                    if re.search(".log", line, re.IGNORECASE):
                        slist = line.split('.')
                        listStr1 = slist[1]
                        slist1 = listStr1.split('g')
                        listStr2 = slist1[1]
                        previous_line = listStr2
                        continue

                    if len(previous_line) == 0:
                        previous_line = line1
                    else:
                        new_output = previous_line + line1 + '\r\n'
                        output1 = output1 + new_output
                        previous_line = ''

        return output1


#######################################################################################################################
# Function Name: openbmc_utility_check_output
# Date         : 14th May 2020
# Author       : TK NG<tikng@celestica.com>
#
# Procedure Revision Details:
#   Version : 1.0  - Initial Draft  - by TK NG<tikng@celestica.com>
#######################################################################################################################
    def openbmc_utility_check_output(self, output):
        self.wpl_log_debug('Entering procedure openbmc_utility_check_output: %s\n'%(str(locals())))

        for sline in output.splitlines():
            if re.search(r'error', sline, re.IGNORECASE):
                self.wpl_log_fail("Error found in output: [%s]" %sline)
                return 1

            if re.search(r'Read wrong version', sline, re.IGNORECASE):
                self.wpl_log_fail("Error message found: Read wrong version. Return error code: ERR_01_006_01.")
                return 1

            if re.search(r'BIC I2C hang', sline, re.IGNORECASE):
                self.wpl_log_fail("Error message found: BIC I2C hang. Return error code: ERR_01_006_02.")
                return 1

            if re.search(r'get_dev_id failed', sline, re.IGNORECASE):
                self.wpl_log_fail("Error message found: get_dev_id failed. Return error code: ERR_01_007_01.")
                return 1

            if re.search(r'get_gpio failed', sline, re.IGNORECASE):
                self.wpl_log_fail("Error message found: get_gpio failed. Return error code: ERR_01_007_02.")
                return 1

            if re.search(r'get_gpio_config failed', sline, re.IGNORECASE):
                self.wpl_log_fail("Error message found: get_gpio_config failed. Return error code: ERR_01_007_03.")
                return 1

            if re.search(r'get_config failed', sline, re.IGNORECASE):
                self.wpl_log_fail("Error message found: get_config failed. Return error code: ERR_01_007_04.")
                return 1

            if re.search(r'get_post_code failed', sline, re.IGNORECASE):
                self.wpl_log_fail("Error message found: get_post_code failed. Return error code: ERR_01_007_05.")
                return 1

            if re.search(r'get_sdr failed', sline, re.IGNORECASE):
                self.wpl_log_fail("Error message found: get_sdr failed. Return error code: ERR_01_007_06.")
                return 1

            if re.search(r'read_sensor failed', sline, re.IGNORECASE):
                self.wpl_log_fail("Error message found: read_sensor failed. Return error code: ERR_01_007_07.")
                return 1

            if re.search(r'read_fruid failed', sline, re.IGNORECASE):
                self.wpl_log_fail("Error message found: read_fruid failed. Return error code: ERR_01_007_08.")
                return 1

            if re.search(r'read_mac failed', sline, re.IGNORECASE):
                self.wpl_log_fail("Error message found: read_mac failed. Return error code: ERR_01_007_09.")
                return 1

            return 0


#######################################################################################################################
# Function Name: set_nvme_stress_time
# Date         : 14th May 2020
# Author       : TK NG<tikng@celestica.com>
#
# Procedure Revision Details:
#   Version : 1.0  - Initial Draft  - by TK NG<tikng@celestica.com>
#######################################################################################################################
    def set_nvme_stress_time(self, stress_time):
        self.wpl_log_debug('Entering procedure set_nvme_stress_time with args : %s' %(str(locals())))

        self.nvme_stress_time = str(stress_time)

        self.wpl_log_success('Successfully set_nvme_stress_time: [%s] seconds.\n' %stress_time)


#######################################################################################################################
# Function Name: perform_nvme_access_stress_test
# Date         : 14th May 2020
# Author       : TK NG<tikng@celestica.com>
#
# Procedure Revision Details:
#   Version : 1.0  - Initial Draft  - by TK NG<tikng@celestica.com>
#######################################################################################################################
    def perform_nvme_access_stress_test(self, toolName, optionStr, toolName1, optionStr1, runTime, toolPath, patternList, patternList1):
        self.wpl_log_debug('Entering procedure perform_nvme_access_stress_test with args : %s' %(str(locals())))
        cmd = 'cd ' + toolPath
        self.wpl_getPrompt("centos", 600)
        self.wpl_transmit(cmd)

        # clear mcelog
        cmd = 'cat /dev/null > /var/log/mcelog'
        output = self.wpl_execute(cmd)

        self.check_nvme_smartctl_info(toolName1, optionStr1, patternList1)

        complete_flag = False
        found = False
        t1 = time.time()
        while complete_flag == False:
            time.sleep(1)

            # execute fio command
            cmd = './' + toolName + ' ' + optionStr
            output = self.wpl_execute(cmd, 'centos', 900)
            self.wpl_log_info('output=[%s]' %output)

            self.wpl_log_info("Checking \'%s\' output..." %(toolName))

            for line in output.splitlines():
                if re.search('NVMe SSD R/W test failed', line, re.IGNORECASE):
                    self.wpl_log_fail('NVMe SSD R/W test failed')
                    self.wpl_raiseException('%s command failed. Error code: ERR_02_006_01' %toolName)

                if re.search('error|fail', line, re.IGNORECASE):
                    self.wpl_log_fail('Error|Fail message found in \"%s\" command output: [%s]' %(toolName, line))
                    self.wpl_raiseException('Failed to perform_nvme_access_stress_test')

            for i in patternList:
                self.wpl_log_debug('searching pattern: [%s]' %i)

                found = False
                for line in output.splitlines():
                    match = re.search('root@', line, re.IGNORECASE)
                    if match:
                        continue

                    line = line.strip()
                    if len(line) == 0:
                        # blank line
                        continue
                    else:
                        match1 = re.search(i, line, re.IGNORECASE)
                        if match1:
                            found = True
                            break

                if found:
                    continue
                else:
                    self.wpl_log_fail('Error: Pattern[%s] not found in output\r\n' %i)
                    self.wpl_raiseException('Failed to perform_nvme_access_stress_test')

            self.wpl_log_success('Checked \'%s\' output OK.' %(toolName))

            t2 = time.time()
            time_diff = int(t2 - t1)
            if time_diff > int(runTime):
                complete_flag = True
                break

        # check for error message in /var/log/mcelog
        cmd = 'cat /var/log/mcelog | grep -i'
        pattern = 'error'
        result = self.check_command_output(cmd, pattern)
        if result == False:
            self.wpl_log_fail('Error message found in /var/log/mcelog')
            self.wpl_raiseException('Failed to perform_nvme_access_stress_test.')

        # check for fail message in /var/log/mcelog
        cmd = 'cat /var/log/mcelog | grep -i'
        pattern = 'fail'
        result = self.check_command_output(cmd, pattern)
        if result == False:
            self.wpl_log_fail('Fail message found in /var/log/mcelog')
            self.wpl_raiseException('Failed to perform_nvme_access_stress_test.')

        self.wpl_log_info('Check /var/log/mcelog for error and fail messages...PASS')

        self.check_nvme_smartctl_info(toolName1, optionStr1, patternList1)

        self.wpl_log_success("Successfully perform_nvme_access_stress_test using \'%s\' tool for %s seconds. PASSED." %(toolName, runTime))


#######################################################################################################################
# Function Name: check_nvme_smartctl_info
# Date         : 14th May 2020
# Author       : TK NG<tikng@celestica.com>
#
# Procedure Revision Details:
#   Version : 1.0  - Initial Draft  - by TK NG<tikng@celestica.com>
#######################################################################################################################
    def check_nvme_smartctl_info(self, toolName, optionStr, patternList):
        self.wpl_log_debug('Entering procedure check_nvme_smartctl_info with args : %s' %(str(locals())))

        # execute nvme command
        cmd = (toolName + ' ' + optionStr)
        output = self.wpl_execute(cmd, 'centos', 900)
        self.wpl_log_info('output=[%s]' %output)

        self.wpl_log_info("Checking nvme smartctl information...")

        for line in output.splitlines():
            self.wpl_log_info('%s' %line)

            match = re.search('root@', line, re.IGNORECASE)
            if match:
                continue

            line = line.strip()
            if len(line) == 0:
                # blank line
                continue
            else:
                found = False
                for i in patternList:
                    match1 = re.search(i, line, re.IGNORECASE)
                    if match1:
                        found = True
                        break

                if found:
                    continue
                else:
                    self.wpl_log_fail('Error: Pattern not found in output[%s].\r\n' %line)
                    self.wpl_raiseException('Failed to check_nvme_smartctl_info.')

        self.wpl_log_success("Successfully check_nvme_smartctl_info. PASSED.")


#######################################################################################################################
# Function Name: set_eeprom_stress_time
# Date         : 14th May 2020
# Author       : TK NG<tikng@celestica.com>
#
# Procedure Revision Details:
#   Version : 1.0  - Initial Draft  - by TK NG<tikng@celestica.com>
#######################################################################################################################
    def set_eeprom_stress_time(self, stress_time):
        self.wpl_log_debug('Entering procedure set_eeprom_stress_time with args : %s' %(str(locals())))

        self.eeprom_stress_time = str(stress_time)

        self.wpl_log_success('Successfully set_eeprom_stress_time: [%s] seconds.\n' %stress_time)


#######################################################################################################################
# Function Name: perform_eeprom_stress_test
# Date         : 12th May 2021
# Author       : Eric Zhang<zfzhang@celestica.com>
#
# Procedure Revision Details:
#   Version : 1.0  - Initial Draft  - by Eric Zhang<zfzhang@celestica.com>
#######################################################################################################################
    @logThis
    def perform_eeprom_access_stress_test(self, initTool, initOption, initToolPath, resetTool, resetOption1, resetOption2, resetToolPath, toolName, optionStr, toolPath, patternList):

        CommonLib.switch_to_centos()

        CommonLib.change_dir(initToolPath)
        
        cmd = 'cd ' + resetToolPath
        self.wpl_getPrompt("centos", 600)
        self.wpl_log_info('cmd=[%s]' %cmd)
        self.wpl_transmit(cmd)

        time.sleep(2)

        cmd = './' + resetTool + ' ' + resetOption1
        self.wpl_log_info('cmd=[%s]' %cmd)
        self.wpl_execute_cmd(cmd, 'centos', 3000)

        time.sleep(2)

        cmd = './' + resetTool + ' ' + resetOption2
        self.wpl_log_info('cmd=[%s]' %cmd)
        self.wpl_execute(cmd, 'centos', 300)

        time.sleep(2)

        cmd = 'cd ' + toolPath
        self.wpl_getPrompt("centos", 600)
        self.wpl_log_info('cmd=[%s]' %cmd)
        self.wpl_transmit(cmd)

        time.sleep(2)
        # default port is 48, cloudripper only need 32, so use below command replace it
        import os
        devicename = os.environ.get("deviceName", "")
        if "cloudripper" in devicename.lower():
            cmd = "sed -i 's/48/32/g' temp_volt_limit"
            self.device.sendMsg(cmd + '\r\n')

        cmd = './' + toolName + ' ' + optionStr
        self.wpl_log_info('cmd=[%s]' % cmd)
        output = self.wpl_execute(cmd, 'centos', 8000)
        self.wpl_log_debug('output=[%s]' % output)
        passcount = 0
        failcount = 0
        patternList = [
            r'p\d\d#:.*?V.*?pass',
            r'p\d\d#:.*C.*pass'
        ]
        fail_patternList = [
            r'p\d\d#:.*?V.*?fail',
            r'p\d\d#:.*?C.*?fail'
        ]
        for line in output.splitlines():
                line = line.strip()
                for i in range(0, len(patternList)):
                    match = re.search(patternList[i], line)
                    if match:
                        passcount += 1
                for m in range(0, len(fail_patternList)):
                    fail_match = re.search(fail_patternList[m], line)
                    if fail_match:
                        failcount += 1
        self.wpl_log_info("///////passcount=%s/////////" % passcount)
        self.wpl_log_info("///////failcount=%s/////////" % failcount)
        if passcount  and failcount == 0:
            self.wpl_log_success("Successfully perform_eeprom_access_stress_test using \'%s\' tool. PASSED." % toolName)
        elif failcount:
            self.wpl_log_fail("failed perform_eeprom_access_stress_test with output fail")
            self.wpl_raiseException("output fail")
        else:
            self.wpl_log_fail("Failed perform_eeprom_access_stress_test using \'%s\' tool. PASSED." % toolName)
            self.wpl_raiseException("Failed perform_eeprom_access_stress_test using \'%s\' tool. PASSED." % toolName)
               

#######################################################################################################################
# Function Name: eeprom_output_is_start_line
# Date         : 14th May 2020
# Author       : TK NG<tikng@celestica.com>
#
# Procedure Revision Details:
#   Version : 1.0  - Initial Draft  - by TK NG<tikng@celestica.com>
#######################################################################################################################
    def eeprom_output_is_start_line(self, line, start_pattern_list):
        self.wpl_log_debug('Entering procedure eeprom_output_is_start_line: %s\n'%(str(locals())))

        for i in start_pattern_list:
            match = re.search(i, line, re.IGNORECASE)
            if match:
                return True

        return False


#######################################################################################################################
# Function Name: set_bmc_cpu_link_stress_time
# Date         : 14th May 2020
# Author       : TK NG<tikng@celestica.com>
#
# Procedure Revision Details:
#   Version : 1.0  - Initial Draft  - by TK NG<tikng@celestica.com>
#######################################################################################################################
    def set_bmc_cpu_link_stress_time(self, stress_time):
        self.wpl_log_debug('Entering procedure set_bmc_cpu_link_stress_time with args : %s' %(str(locals())))

        self.bmc_cpu_link_stress_time = str(stress_time)

        self.wpl_log_success('Successfully set_bmc_cpu_link_stress_time: [%s] cycles.\n' %(str(stress_time)))


#######################################################################################################################
# Function Name: start_bmc_cpu_oob_link_stress_test
# Date         : 14th May 2020
# Author       : TK NG<tikng@celestica.com>
#
# Procedure Revision Details:
#   Version : 1.0  - Initial Draft  - by TK NG<tikng@celestica.com>
#######################################################################################################################
    def start_bmc_cpu_network_link_stress_test(self, username, password, fileName, filePath, fileSize_MB, destPath, openbmc_ipAddr, centos_ipAddr, net_interface):
        self.wpl_log_debug('Entering procedure start_bmc_cpu_network_link_stress_test : %s\n'%(str(locals())))

        complete_flag = False
        cmd = ('cd ' + filePath)
        self.wpl_transmit(cmd)

        filePathName = filePath + '/' + fileName
        if self.check_and_create_test_file(filePathName, fileSize_MB):
            self.wpl_raiseException("Failed start_bmc_cpu_network_link_stress_test")

        logFileName = ('%s/ping.log' %filePath)

        t1 = time.time()

        stress_time = int(self.bmc_cpu_link_stress_time)

        while complete_flag == False:
            time.sleep(1)
            # ping openbmc at the background
            cmd = ('ping6 %s -I %s' %(openbmc_ipAddr, net_interface))
            cmd1 = (cmd + ' > %s&' %logFileName)
            self.wpl_log_debug(cmd1)
            self.wpl_transmit(cmd1)
            time.sleep(10)

            # copy file from cpu side to bmc side
            output1 = 0
            fileList = []
            fileList.append(fileName)
            #scp -6 /tmp/test.dat root@[fe80::2e0:ecff:fedc:eb96%eth0]:/mnt/data1/
            output1 = CommonLib.copy_files_through_scp(Const.DUT, username, password, openbmc_ipAddr, fileList, filePath, destPath, 'centos', True, True, net_interface, 7200)
            if output1:
                if re.search("eth", net_interface, re.IGNORECASE):
                    self.wpl_log_debug('Error copy_files_through_scp. Error code: ERR_02_007_01')
                else:
                    self.wpl_log_debug('Error copy_files_through_scp. Error code: ERR_02_008_01')
                self.wpl_raiseException("Failed copy_files_through_scp")

            time.sleep(1)
            self.delete_test_file(destPath, fileName)

            # stop ping background process
            output2 = ''
            cmd2 = ('ps -aux | grep \"ping6\"')
            self.wpl_log_debug(cmd2)
            output2 = self.wpl_execute(cmd2, mode=centos_mode, timeout=30)
            if output2 is not None:
                # stop background ping process
                self.wpl_log_debug("%s" %output2)
                for line in output2.splitlines():
                    line = line.strip()
                    if re.search(r'root@', line, re.IGNORECASE):
                        continue
                    if re.search('grep', line, re.IGNORECASE):
                        continue
                    self.wpl_log_debug("[%s]" %line)
                    match = re.search('ping6', line, re.IGNORECASE)
                    if match:
                        match1 = re.search(r'root([ \t])+(\d+)([ \t])+((\d+).(\d+))', line, re.IGNORECASE)
                        if match1:
                            pid = match1.group(2)
                            cmd3 = ('kill -SIGINT %s' %str(pid))
                            self.wpl_log_debug(cmd3)
                            self.wpl_transmit(cmd3)
                            time.sleep(3)
                            self.wpl_transmit('\r\n')
            else:
                self.wpl_log_debug('ping background process not running')
                self.wpl_raiseException("Failed bmc and cpu network link stress test")

            time.sleep(1)
            output4 = ''

            # check for ping packet lost
            cmd = ('cat %s | grep \"0' %logFileName)
            cmd4 = cmd + '% ' + 'packet loss\"'
            self.wpl_log_debug(cmd4)
            output4 = self.wpl_execute(cmd4, mode=centos_mode, timeout=30)
            if output4 is not None:
                match4 = re.search("0\% packet loss", output4, re.IGNORECASE)
                if match4:
                    self.wpl_log_success("0\% packet loss")
                else:
                    self.wpl_log_debug('Packet lost detected in ping')
                    self.wpl_raiseException("Failed bmc and cpu network link stress test")
            else:
                self.wpl_log_debug('Packet lost detected in ping')
                self.wpl_raiseException("Failed bmc and cpu network link stress test")

            t2 = time.time()
            time_diff = int(t2 - t1)

            self.wpl_log_success('Checked scp and ping output pass.')
            self.wpl_log_info('***Time elapsed: [%s]***' %(str(time_diff)))

            if time_diff > stress_time:
                # test completed
                complete_flag = True
                break

        self.wpl_log_success("Successfully completed bmc and cpu network link stress test. PASSED.")


#######################################################################################################################
# Function Name: check_and_create_test_file
# Date         : 14th May 2020
# Author       : TK NG<tikng@celestica.com>
#
# Procedure Revision Details:
#   Version : 1.0  - Initial Draft  - by TK NG<tikng@celestica.com>
#######################################################################################################################
    def check_and_create_test_file(self, filePathName, fileSize_MB):
        log.debug('Entering procedure check_and_create_test_file with args : %s\n' %(str(locals())))

        # /tmp/testFile5g.bin
        if CommonLib.check_file_exist(filePathName, centos_mode) == True:
            return 0

        p1 = r'(.+) records in'
        p2 = r'(.+) records out'
        p3 = 'No such file or directory'

        cmd = ('dd if=/dev/zero of=%s bs=1M count=%s' %(filePathName, fileSize_MB))
        self.wpl_log_debug("command = %s" % cmd)
        self.wpl_flush()
        timeout = 1800
        output = self.wpl_execute(cmd, mode=centos_mode, timeout=timeout)
        match1 = re.search(p1, output, re.IGNORECASE)
        match2 = re.search(p2, output, re.IGNORECASE)
        match3 = re.search(p3, output, re.IGNORECASE)
        if match1 and match2:
            log.success("Successfully check_and_create_test_file")
            return 0
        elif match3:
            log.fail("%s" %(p3))
        else:
            log.fail("Unknown error")

        return 1


#######################################################################################################################
# Function Name: delete_test_file
# Date         : 14th May 2020
# Author       : TK NG<tikng@celestica.com>
#
# Procedure Revision Details:
#   Version : 1.0  - Initial Draft  - by TK NG<tikng@celestica.com>
#######################################################################################################################
    def delete_test_file(self, filePath, fileName):
        log.debug('Entering procedure delete_test_file with args : %s\n' %(str(locals())))

        CommonLib.switch_to_openbmc()
        cmd = 'rm -f %s/%s' %(filePath, fileName)
        self.wpl_log_debug("command = %s" % cmd)
        self.wpl_transmit(cmd)
        self.wpl_flush()


#######################################################################################################################
# Function Name: set_openbmc_memory_stress_cycles
# Date         : 14th May 2020
# Author       : TK NG<tikng@celestica.com>
#
# Procedure Revision Details:
#   Version : 1.0  - Initial Draft  - by TK NG<tikng@celestica.com>
#######################################################################################################################
    def set_openbmc_memory_stress_cycles(self, max_cycles):
        self.wpl_log_debug('Entering procedure set_openbmc_memory_stress_cycles with args : %s' %(str(locals())))

        self.openbmc_memory_stress_cycles = str(max_cycles)

        self.wpl_log_success('Successfully set_openbmc_memory_stress_cycles: [%s] cycles.\n' %(str(max_cycles)))


#######################################################################################################################
# Function Name: set_openbmc_memory_stress_time
# Date         : 14th May 2020
# Author       : TK NG<tikng@celestica.com>
#
# Procedure Revision Details:
#   Version : 1.0  - Initial Draft  - by TK NG<tikng@celestica.com>
#######################################################################################################################
    def set_openbmc_memory_stress_time(self, stress_time):
        self.wpl_log_debug('Entering procedure set_openbmc_memory_stress_time with args : %s' %(str(locals())))

        self.openbmc_memory_stress_time = str(stress_time)

        self.wpl_log_success('Successfully set_openbmc_memory_stress_time: [%s] seconds.\n' %stress_time)


#######################################################################################################################
# Function Name: perform_openbmc_memory_stress_test
# Date         : 14th May 2020
# Author       : TK NG<tikng@celestica.com>
#
# Procedure Revision Details:
#   Version : 1.0  - Initial Draft  - by TK NG<tikng@celestica.com>
#######################################################################################################################
    def perform_openbmc_memory_stress_test(self, toolName, optionStr, toolPath, maxCycles, patternList):
        self.wpl_log_debug('Entering procedure perform_openbmc_memory_stress_test with args : %s' %(str(locals())))

        complete_flag = False
        stress_time = int(self.openbmc_memory_stress_time)
        t1 = time.time()

        while complete_flag == False:
            time.sleep(1)

            cmd = 'cd ' + toolPath
            new_cmd = 'mkdir -p' + toolPath
            self.wpl_getPrompt("openbmc", 600)
            self.wpl_transmit(cmd)

            optionStr = optionStr + ' '
            found = False

            # execute memtester command
            cmd = './' + toolName + ' ' + optionStr
            self.wpl_log_info(cmd)
            output = self.wpl_execute(cmd, 'openbmc', 6000)
            self.wpl_log_info('%s' %output)

            ###---###
            # fix the issue of "ok" string sometimes not appearing on the same line of the commmand output
            output1 = ''
            previousStr = ''
            for line in output.splitlines():
                line = line.strip()
                if len(line) == 0:
                    # blank line
                    continue
                else:
                    replace_flag = False
                    found = False
                    found1 = False
                    found2 = False
                    found3 = False
                    if re.search(":", line):
                        found = True
                    if re.search("setting", line, re.IGNORECASE):
                        found1 = True
                    if re.search("testing", line, re.IGNORECASE):
                        found2 = True
                    if re.search("ok", line, re.IGNORECASE):
                        found3 = True

                    if (found):
                        if found3:
                            replace_flag = True

                        slist = line.split(':')
                        listStr1 = slist[0]
                        previousStr = ''
                        if replace_flag:
                            listStr2 = (str(listStr1) + ' : ok\r\n')
                            output1 = output1 + listStr2
                        else:
                            previousStr = (str(listStr1) + ' : ')
                    else:
                        if found3:
                            output1 = output1 + previousStr + 'ok\r\n'
                            previousStr = ''
                        else:
                            if len(previousStr):
                                if found1 or found2:
                                    continue
                                else:
                                    output1 += (line + '\r\n')
                                    previousStr = ''
                            else:
                                output1 += (line + '\r\n')

            output = output1
            self.wpl_log_info('checking output[\r\n%s\r\n]' %output)
            ###---###

            for line in output.splitlines():
                self.wpl_log_debug('%s' %line)

                match = re.search('root@', line, re.IGNORECASE)
                if match:
                    continue

                match1 = re.search('memtester|Copyright|Licensed', line, re.IGNORECASE)
                if match1:
                    continue

                line = line.strip()
                if len(line) == 0:
                    # blank line
                    continue
                else:
                    found = False
                    for i in patternList:
                        match2 = re.search(i, line, re.IGNORECASE)
                        if match2:
                            found = True
                            break
                    if found:
                        continue
                    else:
                        self.wpl_log_fail('Error in output[%s]\r\n' %line)
                        self.wpl_raiseException('Failed to perform_openbmc_memory_stress_test.')

                match3 = re.search('Bmc Memery test Failed', line, re.IGNORECASE)
                if match3:
                    self.wpl_log_fail('Failed to perform_openbmc_memory_stress_test.')
                    self.wpl_raiseException('%s command failed. Error code: ERR_01_009_01' %toolName)

                match4 = re.search('error|fail', line, re.IGNORECASE)
                if match4:
                    self.wpl_log_fail('Error|Fail message found in \"%s\" command output: [%s]' %(toolName, line))
                    self.wpl_raiseException('Failed to perform_openbmc_memory_stress_test.')

            t2 = time.time()
            time_diff = int(t2 - t1)

            self.wpl_log_success('Checked \'%s\' with option \'%s\' output pass.' %(toolName, optionStr))
            self.wpl_log_info('***Time elapsed: [%s]***' %(str(time_diff)))

            if time_diff > stress_time:
                # test completed
                complete_flag = True
                break

        self.wpl_log_success("Successfully perform_openbmc_memory_stress_test using \'%s\' tool. PASSED." %toolName)


#######################################################################################################################
# Function Name: set_i2c_scan_stress_time
# Date         : 14th May 2020
# Author       : TK NG<tikng@celestica.com>
#
# Procedure Revision Details:
#   Version : 1.0  - Initial Draft  - by TK NG<tikng@celestica.com>
#######################################################################################################################
    def set_i2c_scan_stress_time(self, stress_time):
        self.wpl_log_debug('Entering procedure set_i2c_scan_stress_time with args : %s' %(str(locals())))

        self.i2c_scan_stress_time = str(stress_time)

        self.wpl_log_success('Successfully set_i2c_scan_stress_time: [%s] seconds.\n' %stress_time)


#######################################################################################################################
# Function Name: perform_i2c_scan_stress_test
# Date         : 14th May 2020
# Author       : TK NG<tikng@celestica.com>
#
# Procedure Revision Details:
#   Version : 1.0  - Initial Draft  - by TK NG<tikng@celestica.com>
#######################################################################################################################
    def perform_i2c_scan_stress_test(self, toolName, optionArrayList, keyList, runTime, toolPath, patternArrayList, platform):
        self.wpl_log_debug('Entering procedure perform_i2c_scan_stress_test with args : %s' %(str(locals())))

        if (platform == 'wedge400c') or (platform == 'minipack2'):
            # init DC PEM or AC PSU
            self.init_system_test()
        
        devicename = os.environ.get("deviceName", "")
        if 'wedge400_dc' in devicename.lower():
            patternArrayList = cel_openmbc_i2c_pattern_list_w400_dc
        elif 'wedge400_rsp' in devicename.lower():
            cmd = 'pem-util pem2 --get_pem_info'
            output = self.wpl_execute_cmd(cmd, mode=openbmc_mode, timeout=30)
            match = re.search('is not present', output)
            if match:
                self.wpl_log_info("This unit use PSU")
                patternArrayList = cel_openmbc_i2c_pattern_list_w400_rsp_ac
            else:
                self.wpl_log_info("This unit use PEM")
                patternArrayList = cel_openmbc_i2c_pattern_list_w400_rsp_pem
        elif 'wedge400_mp' in devicename.lower():
            patternArrayList = cel_openmbc_i2c_pattern_list_w400_mp

        pim_counts = 0
        pim_counts = self.mp2_pim_count()

        cmd = 'cd ' + toolPath
        self.wpl_getPrompt("openbmc", 600)
        self.wpl_transmit(cmd)

        ## dc pim check
        if pim_counts == 3:
            keyList = minipack2_cel_openmbc_i2c_dev_key_list_pim5
        elif pim_counts == 4:
            keyList = minipack2_cel_openmbc_i2c_dev_key_list_pim4

        complete_flag = False
        found = False
        t1 = time.time()
        while complete_flag == False:
            time.sleep(2)

            for key in keyList:
                optionStr = optionArrayList[key]
                patternList = patternArrayList[key]

                # execute cel-i2c-test command
                cmd = './' + toolName + ' ' + optionStr
                self.wpl_log_info(cmd)
                output = self.wpl_execute(cmd, 'openbmc', 300)
                self.wpl_log_info('%s' %output)
                self.wpl_log_info("Checking \'%s\' output..." %(toolName))

                detect_read_fail = 0
                detect_retry = 0
                remove_text = False
                read_failed_flag = False
                retry_flag = False
                output1 = output
                # scan for errors first
                for line in output1.splitlines():
                    if remove_text == True:
                        if re.search('NO', line):
                            output = output.replace(line, "\n")
                            remove_text = False
                            # Temporary ignore 'SMB_OCP_Debug_card' read failure for cloudripper
                            if re.search('SMB_OCP_CARD', line):
                                detect_read_fail -= 1
                            continue

                    if re.search('Error: Read failed', line, re.IGNORECASE):
                        detect_read_fail += 1
                        read_failed_flag = True
                        remove_text = True
                        continue

                    if re.search('RETRY', line, re.IGNORECASE):
                        detect_retry += 1
                        retry_flag = True
                        remove_text = True
                        continue

                    if re.search('OK', line, re.IGNORECASE):
                        if detect_read_fail == 0:
                            if detect_retry:
                                detect_retry = 0

                    if re.search('Bmc I2c Scan Check Failed', line, re.IGNORECASE):
                        self.wpl_log_fail('Failed to perform_i2c scan_stress_test.')
                        self.wpl_raiseException('%s command failed. Error code: ERR_01_014_01' %toolName)

                    if re.search('error|fail', line, re.IGNORECASE):
                        # other errors or failures
                        self.wpl_log_fail('Error|Fail message found in \"%s\" command output: [%s]' %(toolName, line))
                        self.wpl_raiseException('Failed to perform_i2c scan_stress_test.')

                    if re.search('Error|Fail', line, re.IGNORECASE):
                        # other errors or failures
                        self.wpl_log_fail('[%s] found in %s command output.' %(line, toolName))
                        self.wpl_raiseException('Failed to perform_i2c scan_stress_test.')

                if detect_read_fail > 1:
                    # only allow 1 read fail and 1 retry
                    self.wpl_log_fail('Detected [Error: Read failed] in %s command output.' %toolName)
                    self.wpl_raiseException('Failed to perform_i2c scan_stress_test')

                #if detect_read_fail:
                #    if detect_read_fail != detect_retry:
                #        # only allow 1 read fail and 1 retry
                #        self.wpl_log_fail('Detected [Error: Read failed] in %s command output.' %toolName)
                #        self.wpl_raiseException('Failed to perform_i2c scan_stress_test')

                if read_failed_flag:
                    output = output.replace('Error: Read failed', "\n")

                if retry_flag:
                    if re.search('RETRY!', output, re.IGNORECASE):
                        output = output.replace('RETRY!', "\n")
                    if re.search('RETRY', output, re.IGNORECASE):
                        output = output.replace('RETRY', "\n")
                error_count = 0
                for line in output.splitlines():
                    line = line.strip()
                    if len(line) == 0:
                        # blank line
                        continue
                    else:
                        self.wpl_log_debug('%s' %line)

                        match = re.search('root@', line, re.IGNORECASE)
                        if match:
                            continue

                        found = False
                        p1 = r'(\w+)[ \t]+(\d|bus)+[ \t]+'
                        mat = re.search(p1, line)
                        get_i2c_item = mat.group(1)
                        for i in patternList:
                            match1 = re.search(i, line, re.IGNORECASE)
                            if match1:
                                found = True
                                break
                        if found:
                            if error_count > 0:
                                if get_i2c_item == get_fail_item:
                                    error_count = 0
                            continue
                        else:
                            get_fail_item = mat.group(1)
                            error_count += 1
                # possibly new utility output format
                if error_count > 0:
                    self.wpl_log_fail('Detected unrecognized output')
                    self.wpl_raiseException('Failed to perform_i2c scan_stress_test')

                self.wpl_log_success('Checked \'%s\' with option \'%s\' output pass.' %(toolName, optionStr))

            t2 = time.time()
            time_diff = int(t2 - t1)
            if time_diff > int(runTime):
                complete_flag = True
                break

        self.wpl_log_success("Successfully perform_i2c scan_stress_test using \'%s\' tool for %s seconds. PASSED." %(toolName, runTime))


#######################################################################################################################
# Function Name: set_tpm_access_stress_time
# Date         : 14th May 2020
# Author       : TK NG<tikng@celestica.com>
#
# Procedure Revision Details:
#   Version : 1.0  - Initial Draft  - by TK NG<tikng@celestica.com>
#######################################################################################################################
    def set_tpm_access_stress_time(self, stress_time):
        self.wpl_log_debug('Entering procedure set_tpm_access_stress_time with args : %s' %(str(locals())))

        self.tpm_access_stress_time = str(stress_time)

        self.wpl_log_success('Successfully set_tpm_access_stress_time: [%s] seconds.\n' %stress_time)


#######################################################################################################################
# Function Name: set_tpm_access_stress_cycles
# Date         : 14th May 2020
# Author       : TK NG<tikng@celestica.com>
#
# Procedure Revision Details:
#   Version : 1.0  - Initial Draft  - by TK NG<tikng@celestica.com>
#######################################################################################################################
    def set_tpm_access_stress_cycles(self, max_cycles):
        self.wpl_log_debug('Entering procedure set_tpm_access_stress_cycles with args : %s' %(str(locals())))

        self.tpm_access_stress_cycles = str(max_cycles)

        self.wpl_log_success('Successfully set_tpm_access_stress_cycles: [%s] cycles.\n' %(str(max_cycles)))


#######################################################################################################################
# Function Name: set_tpm_access_stress_time
# Date         : 14th May 2020
# Author       : TK NG<tikng@celestica.com>
#
# Procedure Revision Details:
#   Version : 1.0  - Initial Draft  - by TK NG<tikng@celestica.com>
#######################################################################################################################
    def perform_tpm_access_stress_test(self, toolName, verifyToolName, optionStr, verifyOptionStr, runTime, toolPath, verifyToolPath, patternList):
        self.wpl_log_debug('Entering procedure perform_tpm_access_stress_test with args : %s' %(str(locals())))

        #complete_flag = False
        #t1 = time.time()
        #while complete_flag == False:
        max_cycles = int(self.tpm_access_stress_cycles)
        for k in range(0, max_cycles):
            self.wpl_log_info('************************************************************')
            self.wpl_log_info('*** Test Repeat Loop #: %s / %s ***' %((k+1), str(max_cycles)))
            self.wpl_log_info('************************************************************')
            time.sleep(1)

            found = False
            found1 = False
            cmd = 'cd ' + toolPath
            self.wpl_getPrompt("centos", 600)
            self.wpl_transmit(cmd)

            # execute cel-tpm-test command
            cmd = './' + toolName + ' ' + optionStr
            self.wpl_log_info(cmd)
            output = self.wpl_execute(cmd, 'centos', 300)
            self.wpl_log_info('%s' %output)
            self.wpl_log_info('Checking output...')

            err_match1 = re.search('TPM Module Access test failed', output, re.IGNORECASE)
            if err_match1:
                self.wpl_log_fail('Failed to perform_tpm_access_stress_test.')
                self.wpl_raiseException('%s command failed. Error code: ERR_01_015_01' %toolName)

            err_match2 = re.search('error|fail', output, re.IGNORECASE)
            if err_match2:
                self.wpl_log_fail('Error|Fail message found in \"%s\" command output.' %toolName)
                self.wpl_raiseException('Failed to perform_tpm_access_stress_test')

            for i in patternList:
                #self.wpl_log_debug("Checking pattern \'%s\' in output..." %i)
                found = False
                for line in output.splitlines():
                    #self.wpl_log_debug('%s' %line)

                    match = re.search('root@', line, re.IGNORECASE)
                    if match:
                        continue

                    line = line.strip()
                    if len(line) == 0:
                        # blank line
                        continue
                    else:
                        match1 = re.search(i, line, re.IGNORECASE)
                        if match1:
                            self.wpl_log_success('Found \'%s\'.' %(line))
                            found = True
                            break

                if found:
                    continue
                else:
                    self.wpl_log_fail('Pattern[%s] not found in output\r\n' %i)
                    self.wpl_raiseException('Failed to perform_tpm access_stress_test')

            self.wpl_log_success('Checked \'%s\' with option \'%s\' output pass.' %(toolName, optionStr))

#            cmd1 = 'cd ' + verifyToolPath
#            self.wpl_getPrompt("centos", 600)
#            self.wpl_transmit(cmd1)
#
#            for pcrNum in range(0,8):
#                # execute eltt2 command
#                cmd2 = './' + verifyToolName + ' ' + verifyOptionStr + ' ' + str(pcrNum)
#                #self.wpl_log_debug('***cmd[%s]***' %cmd2)
#                output2 = self.wpl_execute(cmd2, 'centos', 300)
#                self.wpl_log_debug('%s' %output2)
#                self.wpl_log_info("Verifying output with \'%s\'..." %(verifyToolName))
#
#                err_match3 = re.search('TPM Module Access test failed', output2, re.IGNORECASE)
#                if err_match3:
#                    self.wpl_log_fail('Failed to perform_tpm_access_stress_test.')
#                    self.wpl_raiseException('%s command failed. Error code: ERR_01_015_01' %verifyToolName)
#
#                err_match4 = re.search('error|fail', output2, re.IGNORECASE)
#                if err_match4:
#                    self.wpl_log_fail('Error|Fail message found in %s command output.' %verifyToolName)
#                    self.wpl_raiseException('Failed to perform_tpm_access_stress_test')
#
#                for line2 in output2.splitlines():
#                    match2 = re.search('root@', line2, re.IGNORECASE)
#                    if match2:
#                        continue
#
#                    line2Str = line2.strip()
#                    if len(line2Str) == 0:
#                        # blank line
#                        continue
#                    else:
#                        if re.search(r'Read([ \t])+PCR([ \t])+(\d+)+([ \t])+\(SHA\-256\):', line2, re.IGNORECASE):
#                            line2Str = ('Read PCR %s \(SHA-256\):' %pcrNum)
#
#                        self.wpl_log_info('Verifying [%s]' %line2Str)
#
#                        found1 = False
#                        for line3 in output.splitlines():
#                            match3 = re.search('root@', line3, re.IGNORECASE)
#                            if match3:
#                                continue
#
#                            line3 = line3.strip()
#                            if len(line3) == 0:
#                                # blank line
#                                continue
#                            else:
#                                match4 = re.search(line2Str, line3, re.IGNORECASE)
#                                if match4:
#                                    self.wpl_log_success('Found \'%s\'.' %(line2Str))
#                                    found1 = True
#                                    break
#
#                        if found1:
#                            continue
#                        else:
#                            self.wpl_log_fail('Output string[%s] not found.\r\n' %line2Str)
#                            self.wpl_raiseException('Failed to perform_tpm access_stress_test')

            #t2 = time.time()
            #time_diff = int(t2 - t1)
            #if time_diff > int(runTime):
            #    complete_flag = True
            #    break

        self.wpl_log_success("Successfully perform_tpm_access_stress_test using \'%s\' tool. PASSED." %toolName)


#######################################################################################################################
# Function Name: set_serdes_stability_max_cycles
# Date         : 14th May 2020
# Author       : TK NG<tikng@celestica.com>
#
# Procedure Revision Details:
#   Version : 1.0  - Initial Draft  - by TK NG<tikng@celestica.com>
#######################################################################################################################
    def set_serdes_stability_max_cycles(self, max_cycles):
        self.wpl_log_debug('Entering procedure set_serdes_stability_max_cycles with args : %s' %(str(locals())))

        self.serdes_max_cycles = str(max_cycles)

        self.wpl_log_success('Successfully set_serdes_stability_max_cycles: [%s] cycles.\n' %(str(max_cycles)))


#######################################################################################################################
# Function Name: init_sdk_ports(port_mode)
# Date         : 14th May 2020
# Author       : TK NG<tikng@celestica.com>
#
# Procedure Revision Details:
#   Version : 1.0  - Initial Draft  - by TK NG<tikng@celestica.com>
#######################################################################################################################
    def init_sdk_ports(self, cmdStr, toolName, optionStr, portMode):
        self.wpl_log_debug('Entering procedure init_sdk_ports with args : %s' %(str(locals())))

        pass_message = '- Done!'
        cmd = '%s %s %s %s > %s ' %(cmdStr, toolName, optionStr, portMode, tmp_file_on_dut)
        self.wpl_log_debug(cmd)
        output = self.wpl_sendCmdRegexp(cmd, pass_message, 200)
        self.wpl_log_debug(output)

        self.wpl_log_success('Successfully init_sdk_ports.\n')


###############################################################################################
# Function Name: select_expected_status_dict
# Date         : 30th June 2020
# Author       : Wallace Qiu. <wallq@celestica.com>
#
# Procedure Revision Details:
#   Version : 1.0  - Initial Draft  - by Wallace Qiu. <wallq@celestica.com>
###############################################################################################
    def select_expected_status_dict(self, portmode, fec=False):
        log.debug('************* Entering procedure select_expected_status_dict with input [%s]\n '%(str(locals())))

        portModeStr = str.upper(portmode)

        if fec:
          if '8X50G_QSFP_4X50G' in portModeStr:
              var_expectedDict = portFEC_DD_8X50G_QSFP_4X50G
          elif '4X50G_QSFP_4X25G' in portModeStr:
              var_expectedDict = portFEC_DD_4X50G_QSFP_4X25G
          elif '8X50G_QSFP_4X25G' in portModeStr:
              var_expectedDict = portFEC_DD_8X50G_QSFP_4X25G
          elif '4X25G_QSFP_4X25G' in portModeStr:
              var_expectedDict = portFEC_DD_4X25G_QSFP_4X25G
          elif '4X25G_QSFP_2X2X25G' in portModeStr:
              var_expectedDict = portFEC_DD_4X25G_QSFP_2X2X25G
          else:
              self.wpl_log_debug('Error: Invalid FEC port mode [%s]. \n '%(portmode))
              return None
        else:
          if '8X50G_QSFP_4X50G' in portModeStr:
              var_expectedDict = portStatusDD_8X50G_QSFP_4X50G
          elif '8X50G_QSFP_4X25G' in portModeStr:
              var_expectedDict = portStatusDD_8X50G_QSFP_4X25G
          elif '4X50G_QSFP_4X25G' in portModeStr:
              var_expectedDict = portStatusDD_4X50G_QSFP_4X25G
          elif '4X25G_QSFP_4X25G' in portModeStr:
              var_expectedDict = portStatusDD_4X25G_QSFP_4X25G
          elif '4X25G_QSFP_2X2X25G' in portModeStr:
              var_expectedDict = portStatusDD_4X25G_QSFP_2X2X25G
          else:
              self.wpl_log_debug('Error: Invalid port mode [%s]. \n '%(portmode))
              return None

        return var_expectedDict


###############################################################################################
# Function Name: read_from_dut_file_by_block
# Date         : 30th June 2020
# Author       : Wallace Qiu. <wallq@celestica.com>
#
# Procedure Revision Details:
#   Version : 1.0  - Initial Draft  - by Wallace Qiu. <wallq@celestica.com>
###############################################################################################
    def read_from_dut_file_by_block(self, begin, readrange, pass_message, filename):
        self.wpl_log_debug('************* Entering procedure read_from_dut_file_by_block with args : %s\n' %(str(locals())))
        output, default_max_lines = '', 2000
        while begin < default_max_lines:
          cmd = "awk '{if (NR>%s && NR<%s) print $0}' %s" % (begin, begin+readrange, filename)
          temp = self.wpl_execute(cmd, mode='centos', timeout=200)
          output += temp
          if pass_message in temp:
             log.cprint('got the expected message [%s]' % pass_message)
             time.sleep(1)
             break
          begin += readrange
          self.wpl_flush()

        if begin >= default_max_lines:
           self.wpl_raiseException('read beyond the max lines without getting the expected message [%s], break.' % pass_message)

        return output


###############################################################################################
# Function Name: verify_port_count
# Date         : 30th June 2020
# Author       : Wallace Qiu. <wallq@celestica.com>
#
# Procedure Revision Details:
#   Version : 1.0  - Initial Draft  - by Wallace Qiu. <wallq@celestica.com>
###############################################################################################
    def verify_port_count(self, parsedPortDict, portmode='dd_8x50g_qsfp_4x50g'):
        self.wpl_log_debug('************* Entering procedure verify_port_count with args : %s\n' %(str(locals())))
        failCount = 0
        actualPortCount = 0

        for item in parsedPortDict['port_number']:
            actualPortCount += 1
        self.wpl_log_debug('Actual port count : %s\n' %actualPortCount)

        if 'QSFP_2X2X25G' in str.upper(portmode):
          if (actualPortCount == ALL_PORT_COUNT_2X2X25G):
              self.wpl_log_success('Number of expected port: %d\n' %actualPortCount)
          else:
              self.wpl_log_fail('Expected number of port not found. Expected: %d Found: %d\n' %(ALL_PORT_COUNT_2X2X25G, actualPortCount))
              failCount += 1
        else:
          if (actualPortCount == ALL_PORT_COUNT):
              self.wpl_log_success('Number of expected port: %d\n' %actualPortCount)
          else:
              self.wpl_log_fail('Expected number of port not found. Expected: %d Found: %d\n' %(ALL_PORT_COUNT, actualPortCount))
              failCount += 1
        return failCount


###############################################################################################
# Function Name: verify_port_status_no_check_seq
# Date         : 30th June 2020
# Author       : Wallace Qiu. <wallq@celestica.com>
#
# Procedure Revision Details:
#   Version : 1.0  - Initial Draft  - by Wallace Qiu. <wallq@celestica.com>
###############################################################################################
    def verify_port_status_no_check_seq(self, parsedPortDict, expectedPortDict):
        self.wpl_log_debug('************* Entering procedure verify_port_status_no_check_seq with args : %s\n' %(str(locals())))
        failCount = 0
        try:
          for portNumber_expected in ALL_PORT_NUM:
            expectedStatus = expectedPortDict[portNumber_expected]

            #do not need to match item by item, can get one matching item in the whole parsed list is ok
            find = 0
            for portNumber_parsed in ALL_PORT_NUM:
              self.wpl_log_debug('Presently portnumber parsed is %d, the left ports are %s.\n' % (portNumber_parsed, str(len(parsedPortDict['port_number']))))
              self.wpl_log_debug(str(parsedPortDict['port_number'][portNumber_parsed]))
              parsedStatus = parsedPortDict['port_number'][portNumber_parsed]
              find += 1
              self.wpl_log_info('--------------------- trying to find match for the Link Number: %d'%(portNumber_expected))
              if 0 == CommonLib.compare_input_dict_to_parsed(parsedStatus, expectedStatus, False):
                self.wpl_log_info('******************** find match for the Link Number: %d.\n'%(portNumber_expected))
                #need to remove the already matched item to avoid one parsed item matching several in the expectedDict
                del parsedPortDict['port_number'][portNumber_parsed]
                break
            if find >= len(ALL_PORT_NUM):
               self.wpl_log_info('--------- failed to find match for the Link Number: %d, expected value is %s.'%(portNumber_expected, expectedStatus))
               failCount += 1

        except Exception as err:
          self.wpl_log_debug(err)
          failCount += 1

        return failCount


###############################################################################################
# Function Name: verify_test_result
# Date         : 30th June 2020
# Author       : Wallace Qiu. <wallq@celestica.com>
#
# Procedure Revision Details:
#   Version : 1.0  - Initial Draft  - by Wallace Qiu. <wallq@celestica.com>
###############################################################################################
    def verify_test_result(self, parsedInfoDict, expectedTestResult):
        self.wpl_log_debug('************* Entering procedure verify_test_result with args : %s\n' %(str(locals())))
        failCount = 0
        if parsedInfoDict['Test Result'] == expectedTestResult:
            self.wpl_log_success('Test Result: %s' %(expectedTestResult))
        else:
            self.wpl_log_fail('Test Result: %s'%(str(parsedInfoDict['Test Result'])))
            failCount += 1
        return failCount


###############################################################################################
# Function Name: getback_2_centos
# Date         : 30th June 2020
# Author       : Wallace Qiu. <wallq@celestica.com>
#
# Procedure Revision Details:
#   Version : 1.0  - Initial Draft  - by Wallace Qiu. <wallq@celestica.com>
###############################################################################################
    def getback_2_centos(self, timeout=3):
        self.wpl_log_debug('************* Entering procedure getback_2_centos. \n')
        time.sleep(timeout)
        cmd = 'exit() '
        self.wpl_transmit(cmd)
        self.wpl_flush()
        time.sleep(timeout)


###############################################################################################
# Function Name: add_flush_and_delay
# Date         : 30th June 2020
# Author       : Wallace Qiu. <wallq@celestica.com>
#
# Procedure Revision Details:
#   Version : 1.0  - Initial Draft  - by Wallace Qiu. <wallq@celestica.com>
###############################################################################################
    def add_flush_and_delay(self, timeout=3):
        #add more delay to make sure the cat process completed, to avoid the output message messup
        time.sleep(timeout)
        self.wpl_flush()
        time.sleep(1)


#######################################################################################################################
# Function Name: flash_update_and_verify_bmc_ver
# Date         : 14th May 2020
# Author       : TK NG<tikng@celestica.com>
#
# Procedure Revision Details:
#   Version : 1.0  - Initial Draft  - by TK NG<tikng@celestica.com>
#######################################################################################################################
    def flash_update_and_verify_bmc_ver(self, toolName, img_path, downgrade_bmc_image, upgrade_bmc_image, bmc_downgrade_ver, bmc_upgrade_ver, flash_device, logFile='None', uartLog='None'):
        self.wpl_log_debug('Entering procedure flash_update_and_verify_bmc_ver with args : %s' %(str(locals())))

        # e.g.
        # upgrade_bmc_image=[flash-wedge400-v3.0-786-g6f5b68d2fb]
        # downgrade_bmc_image=[flash-wedge400-v3.0-775-g81407665fb]
        # upgrade_ver=[6f5b68d2fb-dirty]
        # downgrade_ver=[81407665fb-dirty]

        update_bmc_image = ''
        found = False
        upgrade_bmc_flag = False

        upVersion = bmc_upgrade_ver
        ulist = upVersion.split('-')
        upper_bmc_version = str(ulist[0])

        downVersion = bmc_downgrade_ver
        dlist = downVersion.split('-')
        lower_bmc_version = str(dlist[0])

        current_bmc_version = self.get_current_bmc_rel_version()
        if current_bmc_version is None:
            self.wpl_raiseException("Failed flash_update_and_verify_bmc_ver")
        else:
            # check whether to upgrade or downgrade BMC
            result = self.compare_bmc_versions(current_bmc_version, upper_bmc_version)
            if result == 2:
                # current_bmc_version < upper_bmc_version
                # need to perform upgrade
                update_bmc_image = upgrade_bmc_image
                upgrade_bmc_flag = True
            else:
                # current_bmc_version >= upper_bmc_version
                # need to perform downgrade
                update_bmc_image = downgrade_bmc_image
                upgrade_bmc_flag = False

            if logFile != 'None':
                loop_cnt = int(self.bmc_update_loop_count)
                if self.check_local_file_exists(logFile) == True:
                    if loop_cnt == 0:
                        self.remove_local_file(logFile)

                # write date/time to log file
                cmd = ('touch ' + logFile)
                self.wpl_log_debug("command = %s" %cmd)
                self.wpl_flush()
                output = self.wpl_exec_local_cmd(cmd)
                self.wpl_log_debug(output)

                cmd = ('echo \"[$(date +\'%cF_%cH-%cM-%cS\')] now version is %s\" | tee -a %s > /dev/null' %('%','%','%','%', current_bmc_version, logFile))
                self.wpl_log_debug("command = %s" %cmd)
                self.wpl_flush()
                output = self.wpl_exec_local_cmd(cmd)
                self.wpl_log_debug(output)

                # update test loop count
                loop_cnt += 1
                self.bmc_update_loop_count = str(loop_cnt)
                cmd = ('echo \"[$(date +\'%cF_%cH-%cM-%cS\')] -------------Test Loop %s------------\" | tee -a %s > /dev/null' %('%','%','%','%', self.bmc_update_loop_count, logFile))
                self.wpl_log_debug("command = %s" %cmd)
                self.wpl_flush()
                output = self.wpl_exec_local_cmd(cmd)
                self.wpl_log_debug(output)

                if upgrade_bmc_flag == True:
                    self.wpl_log_debug('Performing BMC firmware upgrade to %s...\n' %update_bmc_image)
                    cmd = ('echo \"[$(date +\'%cF_%cH-%cM-%cS\')] Upgrade to %s\" | tee -a %s > /dev/null' %('%','%','%','%', bmc_upgrade_ver, logFile))
                else:
                    self.wpl_log_debug('Performing BMC firmware downgrade to %s...\n' %update_bmc_image)
                    cmd = ('echo \"[$(date +\'%cF_%cH-%cM-%cS\')] Downgrade to %s\" | tee -a %s > /dev/null' %('%','%','%','%', bmc_downgrade_ver, logFile))

                self.wpl_log_debug("command = %s" %cmd)
                self.wpl_flush()
                output = self.wpl_exec_local_cmd(cmd)
                self.wpl_log_debug(output)

            self.flash_fw_image(toolName, img_path, update_bmc_image, flash_device, logFile)

            if upgrade_bmc_flag == True:
                self.bmc_version = upper_bmc_version
                self.wpl_log_success('Successfully flash upgraded BMC firmware using DIAG tool - %s\n' %toolName)
            else:
                self.bmc_version = lower_bmc_version
                self.wpl_log_success('Successfully flash downgraded BMC firmware using DIAG tool - %s\n' %toolName)

            # verify bmc fw version after reboot
            self.wpl_log_debug('Reboot to verify BMC firmware version...\n')
            CommonLib.reboot("openbmc", uartLog)
            self.switch_to_openbmc_and_check_tool(uartLog)
            self.switch_and_check_bmc_by_diag_command(diag_bmc_boot_bin, "master")
            if upgrade_bmc_flag == True:
                self.check_bmc_update_version(upper_bmc_version)
            else:
                self.check_bmc_update_version(lower_bmc_version)

            self.wpl_log_success('Successfully flash_update_and_verify_bmc_ver.\n')


#######################################################################################################################
# Function Name: extract_bmc_fw_version
# Date         : 14th May 2020
# Author       : TK NG<tikng@celestica.com>
#
# Procedure Revision Details:
#   Version : 1.0  - Initial Draft  - by TK NG<tikng@celestica.com>
#######################################################################################################################
    def extract_bmc_fw_version(self, fw_version_str):
        self.wpl_log_debug('Entering procedure extract_bmc_fw_version with args : %s' %(str(locals())))

        # BMC version format: OpenBMC Release wedge400-81407665fb-dirty
        match = re.search('wedge400-', fw_version_str, re.IGNORECASE)
        if match:
            found = True
        else:
            self.wpl_raiseException("Failed extract_bmc_fw_version. Version string not found.")

        slist = fw_version_str.split('-')
        # extract '81407665fb'
        fw_version = str(slist[1])

        return fw_version


#######################################################################################################################
# Function Name: get_current_bmc_rel_version
# Date         : 14th May 2020
# Author       : TK NG<tikng@celestica.com>
#
# Procedure Revision Details:
#   Version : 1.0  - Initial Draft  - by TK NG<tikng@celestica.com>
#######################################################################################################################
    def get_current_bmc_rel_version(self):
        self.wpl_log_debug('Entering procedure get_current_bmc_rel_version with args : %s' %(str(locals())))
        current_bmc_version=''
        p1 = 'OpenBMC Release'
        cmd = 'cat /etc/issue'
        output = self.wpl_execute(cmd, mode="openbmc")
        for line in output.splitlines():
            line = line.strip()
            match = re.search(p1, line, re.IGNORECASE)
            if match:
                current_bmc_version = self.extract_bmc_fw_version(line)
                self.wpl_log_debug('Current BMC firmware version: %s\n' %current_bmc_version)
                return current_bmc_version

        self.wpl_raiseException("ERR_01_001_01: Failed to get current BMC firmware version")


#######################################################################################################################
# Function Name: compare_bmc_versions
# Date         : 14th May 2020
# Author       : TK NG<tikng@celestica.com>
#
# Procedure Revision Details:
#   Version : 1.0  - Initial Draft  - by TK NG<tikng@celestica.com>
#######################################################################################################################
    def compare_bmc_versions(self, version1, version2):
        self.wpl_log_debug('Entering procedure compare_bmc_versions with args : %s' %(str(locals())))

        # compare 2 version strings:
        # returns 1 if version1 is greater
        # returns 2 if version2 is greater
        # returns 0 if both versions are the same
        if version1 == version2:
            self.wpl_log_debug('version1 == version2')
            return 0

        len1 = len(version1)
        len2 = len(version2)
        # version format: '81407665fb'
        if len1 > len2:
            # version 1 > version 2
            self.wpl_log_debug('version1 > version2')
            return 1
        elif len1 < len2:
            # version 2 > version 1
            self.wpl_log_debug('version2 > version1')
            return 2
        else:
            # compare each character in the version
            for i in range(0, len1):
                if version1[i] == version2[i]:
                    continue
                elif version1[i] > version2[i]:
                    self.wpl_log_debug('version1 > version2')
                    return 1
                else:
                    self.wpl_log_debug('version2 > version1')
                    return 2


#######################################################################################################################
# Function Name: check_bmc_update_version
# Date         : 14th February 2020
# Author       : Phawit P. <Phaphan@celestica.com>
#
# Procedure Revision Details:
#   Version : 1.0  - Initial Draft  - by Phawit P. <Phaphan@celestica.com>
#######################################################################################################################
    def check_bmc_update_version(self, bmc_version):
        self.wpl_log_debug('Entering procedure check_bmc_update_version with args : %s' %(str(locals())))
        passCount=0
        # e.g. OpenBMC Release wedge400-81407665fb-dirty
        p1 = 'OpenBMC Release'
        cmd = 'cat /etc/issue'
        output = self.wpl_execute(cmd, mode="openbmc")
        for line in output.splitlines():
            line = line.strip()
            match = re.search(p1, line, re.IGNORECASE)
            if match:
                slist = line.split('-')
                version_str = str(slist[1])
                if version_str == bmc_version:
                    passCount += 1
                    break
        if passCount:
            self.wpl_log_success("Successfully checked BMC update version: \'%s\'"% bmc_version)
        else:
            self.wpl_raiseException("ERR_01_001_02: Failed checking BMC update version")


#######################################################################################################################
# Function Name: detect_usb_disk
# Date         : 14th May 2020
# Author       : TK NG<tikng@celestica.com>
#
# Procedure Revision Details:
#   Version : 1.0  - Initial Draft  - by TK NG<tikng@celestica.com>
#######################################################################################################################
    def detect_usb_disk(self, toolName, option):
        self.wpl_log_debug('Entering procedure detect_usb_disk with args : %s' %(str(locals())))
        passCount=0
        p1 = r'/dev/sda'

        cmd = (toolName + ' ' + option)
        output = self.wpl_execute(cmd, mode="centos")
        for line in output.splitlines():
            line = line.strip()
            match = re.search(p1, line, re.IGNORECASE)
            if match:
                passCount += 1
                break

        if passCount:
            self.wpl_log_success("Successfully detected usb disk: /dev/sda")
        else:
            self.wpl_raiseException("Failed to detect_usb_disk.")


#######################################################################################################################
# Function Name: platform_get_current_sdk_version
# Date         : 14th May 2020
# Author       : TK NG<tikng@celestica.com>
#
# Procedure Revision Details:
#   Version : 1.0  - Initial Draft  - by TK NG<tikng@celestica.com>
#######################################################################################################################
    def platform_get_current_sdk_version(self, initTool, initOption, toolPath):
        self.wpl_log_debug('Entering procedure platform_get_current_sdk_version: %s\n'%(str(locals())))

        sdk_version = '0'

        CommonLib.switch_to_centos()

        CommonLib.change_dir(toolPath)

        # make sure no auto_load_user.py process running in the background
        self.check_and_terminate_sdk_tool_process(initTool)

        # read sdk version for Wedge400c or Cloudripper platform
        cmd = ('python3 %s %s' %(initTool, initOption))
        self.wpl_log_info(cmd)
        self.wpl_transmit(cmd)
        pattern_list = 'root@'
        output = self.wpl_receive('pci_dev is present', timeout=60)
        output1 = self.wpl_receive(pattern_list, timeout=180)
        time.sleep(2)
        self.wpl_transmit('exit()')
        self.wpl_flush()
        self.wpl_log_info(output)
        self.wpl_log_info(output1)

        found1 = False
        found2 = False
        #make sure the platform is Wedge400c or Cloudripper
        Pass_Message1 = r'Test[ \t]+\|[ \t]+Test[ \t]+\|[ \t]+Wedge400c&Cloudripper[ \t]+\|[ \t]+Wedge400c&Cloudripper[ \t]+.*?'
        #0 | Show Version         |         V2.0.3        |       2020-08-24      | 1.32.0.1a | 0.21.2.1238  |
        Pass_Message2 = r'0[ \t]+\|[ \t]+Show Version[ \t]+\|[ \t]+V([\d]+\.[\d]+\.[\d]+)[ \t]+\|[ \t]+([\d]+-[\d]+-[\d]+)[ \t]+.*?'

        for line in output1.splitlines():
            #self.wpl_log_debug('%s' %line)
            if (found1 == True) and (found2 == True):
                break

            line = line.strip()
            if len(line) == 0:
                # blank line
                continue
            else:
                match1 = re.search(Pass_Message1, line, re.IGNORECASE)
                if match1:
                    found1 = True
                    continue

                match2 = re.search(Pass_Message2, line, re.IGNORECASE)
                if match2:
                    sdk_version = match2.group(1)
                    found2 = True

        if (found1 == True) and (found2 == True):
            self.wpl_log_debug("Successfully platform_get_current_sdk_version: \'%s\'" %sdk_version)
        else:
            self.wpl_raiseException('Failed platform_get_current_sdk_version.')

        return sdk_version


#######################################################################################################################
# Function Name: minipack2_get_current_sdk_version
# Date         : 14th May 2020
# Author       : TK NG<tikng@celestica.com>
#
# Procedure Revision Details:
#   Version : 1.0  - Initial Draft  - by TK NG<tikng@celestica.com>
#######################################################################################################################
    def minipack2_get_current_sdk_version(self, toolName, option, toolPath):
        self.wpl_log_debug('Entering procedure minipack2_get_current_sdk_version with args : %s' %(str(locals())))

        found = False
        sdk_version = '0'
        cmd = 'cd ' + toolPath
        self.wpl_getPrompt("centos", 60)
        self.wpl_transmit(cmd)

        output = self.EXEC_diag_tool_command(toolName, option, toolPath, 60)
        self.wpl_log_debug('output = %s' %output)
        p1 = r'SDK Diag:\s+v([\d]+\.[\d]+\.[\d]+)'

        for line in output.splitlines():
            line = line.strip()
            match = re.search(p1, line, re.IGNORECASE)
            if match:
                sdk_version = match.group(1)
                found = True
                break

        if found:
            self.wpl_log_debug("Successfully minipack2_get_current_sdk_version: \'%s\'" %sdk_version)
        else:
            self.wpl_raiseException("Failed minipack2_get_current_sdk_version.")

        return sdk_version


#######################################################################################################################
# Function Name: get_current_diagos_version
# Date         : 14th May 2020
# Author       : TK NG<tikng@celestica.com>
#
# Procedure Revision Details:
#   Version : 1.0  - Initial Draft  - by TK NG<tikng@celestica.com>
#######################################################################################################################
    def get_current_diagos_version(self, toolName, option, toolPath):
        self.wpl_log_debug('Entering procedure get_current_diagos_version with args : %s' %(str(locals())))

        found = False
        os_version = '0'
        cmd = 'cd ' + toolPath
        self.wpl_getPrompt("centos", 60)
        self.wpl_transmit(cmd)

        output = self.EXEC_diag_tool_command(toolName, option, toolPath, 60)
        self.wpl_log_debug('output = %s' %output)
        p1 = r'OS Diag:\s+([\d]+\.[\d]+\.[\d]+)'

        for line in output.splitlines():
            line = line.strip()
            match = re.search(p1, line, re.IGNORECASE)
            if match:
                os_version = match.group(1)
                found = True
                break

        if found:
            self.wpl_log_debug("Successfully get_current_diagos_version: \'%s\'" %os_version)
        else:
            self.wpl_raiseException("Failed to get_current_diagos_version.")

        return os_version

    def exit_sdk_mode_for_sensor_test(self):
        self.wpl_log_debug('Entering procedure exit_sdk_mode_for_sensor_test: %s\n' % (str(locals())))

        self.device.sendMsg("sol.sh\r\n")
        time.sleep(2)
        self.device.sendMsg('\r\n')
        message_pattern = 'CTRL-l + b : Send Break'
        exit_cmd = 'exit()'
        message = self.device.readUntil(message_pattern, timeout=1200)
        if message:
            self.device.sendMsg("{}\r\n".format(exit_cmd))
            deviceObj.getPrompt(centos_mode)
            log.info("Successfully exit sdk mode")

    def power_type_check_w400(self):
        self.wpl_log_debug('Entering procedure power_type_check_w400 with args : %s' % (str(locals())))
        self.wpl_getPrompt('openbmc', 600)
        cmd = 'cd ' + BMC_DIAG_TOOL_PATH
        self.wpl_transmit(cmd)
        cmd = 'pem-util pem2 --get_pem_info'
        output = self.wpl_execute_cmd(cmd, mode=openbmc_mode, timeout=30)
        match = re.search('is not present', output)
        if match:
            self.wpl_log_info("This unit use PSU")
            cmd1 = "sensor-util psu2 |grep 'PSU2_IN_VOLT' |awk '{print$4}'"
            output1 = self.wpl_execute_cmd(cmd1, mode=openbmc_mode, timeout=30)
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
                        self.wpl_log_info("This unit use DC PSU")
                        if 'wedge400_dc' in devicename.lower() or 'wedge400c_dc' in devicename.lower():
                            cmd3 = './cel-diag-init -c'
                        else:
                            cmd3 = './cel-diag-init -d'
                        self.wpl_transmit(cmd3)
        else:
            self.wpl_log_info("This unit use PEM")
            if 'rsp' in devicename.lower():
                self.wpl_log_info("This machine is Respin PEM unit")
                cmd = './cel-diag-init -m'
                self.wpl_transmit(cmd)
            else:
                cmd = './cel-diag-init -p'
                self.wpl_transmit(cmd)

    def test_GB_run_with_sensor_test(self, toolName, option, message, pattern, path):
        self.wpl_log_debug('Entering procedure test_GB_run_with_sensor_test: %s\n' % (str(locals())))

        devicename = os.environ.get("deviceName", "")
        if 'wedge400_' in devicename.lower():
            CommonLib.switch_to_openbmc()
            self.wpl_getPrompt(openbmc_mode, timeout=60)
            self.wpl_log_debug('switch to openbmc successfully')
        else:
            if path:
                self.wpl_transmit('cd ' + path)

            cmd = toolName + ' ' + option
            self.device.sendMsg(cmd+'\r\n')
            line = self.device.readUntil(message,timeout=300)
            if line:
                self.wpl_log_info('//////////finding the matching///////')
                time.sleep(100)
                CommonLib.switch_to_openbmc()
                self.wpl_getPrompt(openbmc_mode, timeout=60)
                self.wpl_log_debug('switch to openbmc successfully')
            else:
                self.wpl_raiseException('Can not capture the message %s' % pattern_line)

        new_path = '/mnt/data1/BMC_Diag/bin'
        new_command = './cel-sensor-test -u'

        self.wpl_transmit('cd ' + new_path)
        self.device.sendMsg('\r\n')
        time.sleep(5)
        self.device.sendMsg('\r\n')
        output = self.wpl_execute_cmd(new_command, mode=openbmc_mode, timeout=1800)
        time.sleep(10)
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
            message = self.device.readUntil(message_pattern, timeout=1200)
            if message:
                self.device.sendMsg("{}\r\n".format(exit_cmd))
                deviceObj.getPrompt(centos_mode)
                log.info("Successfully exit sdk mode")
            self.wpl_raiseException('GB temp failed, please see output!')


#######################################################################################################################
# Function Name: wedge400c_perform_detect_all_eloop_modules
# Date         : 14th May 2020
# Author       : TK NG<tikng@celestica.com>
#
# Procedure Revision Details:
#   Version : 1.0  - Initial Draft  - by TK NG<tikng@celestica.com>
#######################################################################################################################
    def wedge400c_perform_detect_all_eloop_modules(self, initTool, initOption, initToolPath, resetTool, resetOption1, resetOption2, resetOption3, resetToolPath, reInit_SDK):
        self.wpl_log_debug('Entering procedure wedge400c_perform_detect_all_eloop_modules with args : %s' %(str(locals())))

        if (self.eloop_init == '0') or (reInit_SDK == True):
            CommonLib.switch_to_centos()

            CommonLib.change_dir(initToolPath)

            # make sure no auto_load_user.py process running in the background
            self.check_and_terminate_sdk_tool_process(initTool)

            self.wpl_log_info("Running auto_load_user.py...")
            cmd = 'python3' + ' ' + initTool + ' ' + initOption
            quit = 'exit()'
            self.wpl_log_info('cmd=[%s]' %cmd)
            self.wpl_transmit(cmd)
            pattern_list = SDK_WAIT_PATTERN_LIST
            output = self.wpl_receive(pattern_list,timeout=SDK_TIMEOUT2)
            time.sleep(2)
            self.wpl_log_debug(output)
            output = output.strip()
            #lastStr = output.split()[-1]
            if re.search(COMMON_SDK_PROMPT_II, output):
                self.wpl_log_info('cmd=[%s]' %quit)
                self.wpl_transmit(quit)
                self.wpl_flush()
            else:
                self.wpl_log_fail('Failed running auto_load_user.py.')
                self.wpl_raiseException('Failed wedge400c_perform_detect_all_eloop_modules')

            found = False
            Pass_Messg = SNAKE_TRAFFIC_PASS_MSG
            for line in output.splitlines():
                #self.wpl_log_debug('%s' %line)
                line = line.strip()
                if len(line) == 0:
                    # blank line
                    continue
                else:
                    match = re.search(Pass_Messg, line, re.IGNORECASE)
                    if match:
                        found = True
                        break

            if found == False:
                self.wpl_log_fail('Failed running auto_load_user.py: GB Initialization Test pass message not found.')
                self.wpl_raiseException('Failed wedge400c_perform_detect_all_eloop_modules.')
            else:
                self.wpl_log_info("Successfully run auto_load_user.py.")

            cmd = 'cd ' + resetToolPath
            self.wpl_getPrompt("centos", SDK_TIMEOUT1)
            self.wpl_log_info('cmd=[%s]' %cmd)
            self.wpl_transmit(cmd)

            time.sleep(2)

            cmd = './' + resetTool + ' ' + resetOption1
            self.wpl_log_info('cmd=[%s]' %cmd)
            self.wpl_execute(cmd, 'centos', SDK_TIMEOUT1)

            time.sleep(2)

            cmd = './' + resetTool + ' ' + resetOption2
            self.wpl_log_info('cmd=[%s]' %cmd)
            self.wpl_execute(cmd, 'centos', SDK_TIMEOUT1)

            time.sleep(2)

            cmd = './' + resetTool + ' ' + resetOption3
            self.wpl_log_info('cmd=[%s]' %cmd)
            self.wpl_execute(cmd, 'centos', SDK_TIMEOUT1)

            time.sleep(2)

            self.eloop_init == '1'
            self.wpl_log_success("Successfully run wedge400c_perform_detect_all_eloop_modules.")


#######################################################################################################################
# Function Name: remove_all_system_log_files
# Date         : 14th May 2020
# Author       : TK NG<tikng@celestica.com>
#
# Procedure Revision Details:
#   Version : 1.0  - Initial Draft  - by TK NG<tikng@celestica.com>
#######################################################################################################################
    def remove_all_system_log_files(self, exec_mode):
        self.wpl_log_debug('Entering procedure remove_all_system_log_files with args : %s' %(str(locals())))

        cmd = ('rm -rf /var/log/*')
        self.wpl_log_debug("command = %s" %cmd)
        self.wpl_flush()
        output = self.wpl_execute(cmd, mode=exec_mode, timeout=300)
        self.wpl_log_debug('%s' %output)


#######################################################################################################################
# Function Name: check_all_test_tools_exist
# Date         : 14th May 2020
# Author       : TK NG<tikng@celestica.com>
#
# Procedure Revision Details:
#   Version : 1.0  - Initial Draft  - by TK NG<tikng@celestica.com>
#######################################################################################################################
    def check_all_test_tools_exist(self, toolPath1, toolPath2, exec_mode):
        self.wpl_log_debug('Entering procedure check_all_test_tools_exist with args : %s' %(str(locals())))

        if CommonLib.check_file_exist(toolPath1, exec_mode) == False:
            self.wpl_log_fail("Error: Tool path not found [%s]." %toolPath1)
            self.wpl_raiseException("Failed check_all_test_tools_exist.")

        if CommonLib.check_file_exist(toolPath2, exec_mode) == False:
            self.wpl_log_fail("Error: Tool path not found [%s]." %toolPath2)
            self.wpl_raiseException("Failed check_all_test_tools_exist.")
        ## add fw version check
        cmd = 'cd ' + toolPath1
        self.wpl_transmit(cmd)
        cmd = './cel-version-test -S'
        self.wpl_execute(cmd, exec_mode, 300)
        self.wpl_log_success('Successfully check_all_test_tools_exist.\n')


#######################################################################################################################
# Function Name: check_available_storage_space
# Date         : 14th May 2020
# Author       : TK NG<tikng@celestica.com>
#
# Procedure Revision Details:
#   Version : 1.0  - Initial Draft  - by TK NG<tikng@celestica.com>
#######################################################################################################################
    def check_available_storage_space(self, toolName, dirPath, pattern, exec_mode):
        self.wpl_log_debug('Entering procedure check_available_storage_space with args : %s' %(str(locals())))

        cmd = 'cd ' + dirPath
        self.wpl_getPrompt(exec_mode, 600)
        self.wpl_transmit(cmd)

        cmd = toolName
        output = self.wpl_execute(cmd, exec_mode, 300)
        self.wpl_log_debug('output=[%s]' %output)
        found = False

        for line in output.splitlines():
            self.wpl_log_info('%s' %line)

            line = line.strip()
            if len(line) == 0:
                # blank line
                continue
            else:
                match = re.search(pattern, line, re.IGNORECASE)
                if match:
                    found = True
                    disk_usage = int(match.group(5))
                    break

        if found == False:
            self.wpl_log_fail("Error: Disk info not found for %s." %dirPath)
            self.wpl_raiseException("Failed check_available_storage_space.")
        else:
            if disk_usage < 95:
                self.wpl_log_info("Passed: Disk usage info %s < 95 percent." %str(disk_usage))
                self.wpl_log_success('Successfully check_available_storage_space.\n')
            else:
                self.wpl_log_fail("Error: Insufficient disk space [%s percent used] for running tests." %str(disk_usage))
                self.wpl_raiseException("Failed check_available_storage_space.")


#######################################################################################################################
# Function Name: check_ttyusb0_mounted
# Date         : 8th June 2021
# Author       : Jeff Gong<jgong@celestica.com>
#
# Procedure Revision Details:
#   Version : 1.0  - Initial Draft  - by Jeff Gong<jgong@celestica.com>
#######################################################################################################################
    def check_ttyusb0_mounted(self, toolName, dirPath, pattern, exec_mode):
        self.wpl_log_debug('Entering procedure check_ttyusb0_mount with args : %s' % (str(locals())))
        cmd = 'cd ' + dirPath
        self.wpl_log_debug("command = %s" % cmd)
        self.wpl_getPrompt(exec_mode, 600)
        self.wpl_transmit(cmd)

        cmd = 'ls ' + toolName
        output = self.wpl_execute(cmd, exec_mode, 300)
        if 'ttyUSB0' in output:
            self.wpl_log_info("Passed: find the device ttyUSB0.")
            self.wpl_log_success('Successfully check_ttyusb0_mounted.\n')
        else:
            self.wpl_log_fail("Error: do not find the device ttyUSB0.")
            self.wpl_raiseException("Failed check_ttyusb0_mounted.")


#######################################################################################################################
# Function Name: check_system_pem_psu_slot_connection
# Date         : 22th March 2021
# Author       : Zhen Fei Zhang<zfzhang@celestica.com>
#
# Procedure Revision Details:
#   Version : 1.0  - Initial Draft  - by Zhen Fei Zhang<zfzhang@celestica.com>
#######################################################################################################################
    def check_system_pem_psu_slot_connection(self, toolName1, toolName2, toolPath, exec_mode, pattern):
        self.wpl_log_debug('Entering procedure check_system_pem_psu_slot_connection with args : %s' % (str(locals())))

        cmd = 'cd ' + toolPath
        self.wpl_log_debug("command = %s" %cmd)
        self.wpl_getPrompt(exec_mode, 600)
        self.wpl_transmit(cmd)

        psu_or_pem_command = 'pem-util pem2 --get_pem_info'
        verify_output = self.wpl_execute(psu_or_pem_command, exec_mode, timeout=180)
        devicename = os.environ.get("deviceName", "")
        if 'PEM2 is not present!' in verify_output:
            cmd = ('./' + toolName2 + ' -s')
            if 'wedge400_dc' in devicename.lower() or 'wedge400c_dc' in devicename.lower():
                init_cmd = './cel-diag-init -c'
                self.wpl_transmit(init_cmd)
                pattern = [
                    r'PSU2 Present.*?OK',
                    r'PSU2 ACOK.*?OK',
                    r'PSU2 DCOK.*?OK'
                ]
            else:
                if 'rsp' in devicename.lower():
                    init_cmd = './cel-diag-init -r'
                else:
                    init_cmd = './cel-diag-init -a'
                self.wpl_transmit(init_cmd)
                pattern = [
                    r'PSU1 Present.*?OK',
                    r'PSU1 ACOK.*?OK',
                    r'PSU1 DCOK.*?OK',
                    r'PSU2 Present.*?OK',
                    r'PSU2 ACOK.*?OK',
                    r'PSU2 DCOK.*?OK'
                ]
        else:
            if 'rsp' in devicename.lower() or 'wedge400_mp' in devicename.lower():
                self.wpl_log_info('It is respin pem unit!')
                init_cmd = './cel-diag-init -m'
            else:
                init_cmd = './cel-diag-init -p'
            self.wpl_transmit(init_cmd)
            cmd = ('./' + toolName1 + ' -s')
            pattern = [
                r'PEM2 Present.*?OK',
                r'PEM2 ACOK.*?OK',
                r'PEM2 PWROK.*?OK'
            ]
        self.wpl_log_debug("command = %s" %cmd)
        output = self.wpl_execute(cmd, exec_mode, timeout=180)
        self.wpl_log_debug('output=[%s]' %output)
        passcount = 0
        for line in output.splitlines():
            line = line.strip()
            for i in range(0,len(pattern)):
                match = re.search(pattern[i], line)
                if match:
                    passcount += 1

        self.wpl_log_debug("/////////passcount=%s////////" % passcount)
        if len(pattern) == passcount:
            self.wpl_log_success('Successfully check_system_pem_psu_slot_connection pass')
        else:
            self.wpl_log_fail("Error: PSU1 or PSU2 can not be matched")
            self.wpl_raiseException("Failed check_system_pem_psu_slot_connection.")

#######################################################################################################################
# Function Name: sensor_reading
# Date         : 29th Jun 2020
# Author       : Noah yang<noahyang@celestica.com>
#
# Procedure Revision Details:
#   Version : 1.0  - Initial Draft  - by Noah yang<noahyang@celestica.com>
#######################################################################################################################
    def sensor_reading(self, toolName, optionStr, toolPath, platform):
        self.wpl_log_debug('Entering procedure sensor_reading: %s\n'%(str(locals())))

        self.wpl_getPrompt(openbmc_mode, SDK_TIMEOUT1)

        #### Determine whether it is a w400 machine
        devicename = os.environ.get("deviceName", "")
        if 'minipack2' in devicename.lower():
            cmd = 'cd ' + BMC_DIAG_TOOL_PATH
            self.wpl_transmit(cmd)
            if 'rsp' in devicename.lower():
                self.wpl_log_info("This machine is Respin unit")
                cmd = './cel-diag-init -r'
                self.wpl_transmit(cmd)
            elif 'dc' in devicename.lower():
                self.wpl_log_info("This machine is dc unit")
                cmd = './cel-diag-init -c'
                self.wpl_transmit(cmd)
            else:
                self.wpl_log_info("This machine is ac unit")
                cmd = './cel-diag-init -a'
                self.wpl_transmit(cmd)
        else:
            self.power_type_check_w400()
        #    # replace AC or DC sensor config file
        #    self.replace_sensor_cfg_and_diag_init()

        CommonLib.change_dir(toolPath)

        Fail = 'FAIL'
        cmd = ('./%s %s' %(toolName, optionStr))
        p1 = 'No such file or directory'

        max_cycles = int(self.sensor_reading_max_cycles)
        for i in range(0, max_cycles):
            self.wpl_log_info('************************************************************')
            self.wpl_log_info('*** Test Repeat Loop #: %s / %s ***' %((i+1), str(max_cycles)))
            self.wpl_log_info('************************************************************')

            output = self.wpl_execute(cmd,mode=None,timeout=700)
            match = re.search(p1, output, re.IGNORECASE)
            if match:
                self.wpl_log_fail('Failed sensor_reading: No such file or directory')
                return 1
            else:
                self.wpl_log_info('checking %s output...' %toolName)
                for line in output.splitlines():
                    #self.wpl_log_info('%s' %line)

                    line = line.strip()
                    if len(line) == 0:
                        continue

                    if 'psu1 is not present!' in line:
                        continue
                    elif 'psu2 is not present!' in line:
                        continue
                    elif 'pem1 is not present!' in line:
                        continue
                    elif 'pem2 is not present!' in line:
                        continue
                    elif 'SYSTEM_AIRFLOW' in line:
                        continue
                    elif re.search(': na', line, re.IGNORECASE):
                        self.wpl_log_fail('Failed sensor_reading: Found \"NA\" string in sensor reading: [%s]' %line)
                        return 1
                    elif re.search('ucr', line, re.IGNORECASE):
                        self.wpl_log_fail('Failed sensor_reading: Found \"UCR\" string in sensor reading: [%s]' %line)
                        return 1
                    elif re.search('unc', line, re.IGNORECASE):
                        self.wpl_log_fail('Failed sensor_reading: Found \"UNC\" string in sensor reading: [%s]' %line)
                        return 1
                    elif re.search('unr', line, re.IGNORECASE):
                        self.wpl_log_fail('Failed sensor_reading: Found \"UNR\" string in sensor reading: [%s]' %line)
                        return 1
                    elif re.search('lcr', line, re.IGNORECASE):
                        self.wpl_log_fail('Failed sensor_reading: Found \"LCR\" string in sensor reading: [%s]' %line)
                        return 1
                    elif re.search('lnc', line, re.IGNORECASE):
                        self.wpl_log_fail('Failed sensor_reading: Found \"LNC\" string in sensor reading: [%s]' %line)
                        return 1
                    elif re.search('lnr', line, re.IGNORECASE):
                        self.wpl_log_fail('Failed sensor_reading: Found \"LNR\" string in sensor reading: [%s]' %line)
                        return 1
                    elif re.search('error', line, re.IGNORECASE):
                        self.wpl_log_fail('Failed sensor_reading: Found error string in sensor reading: [%s]' %line)
                        return 1
                self.wpl_log_success('%s result pass' %toolName)

        return 0


#######################################################################################################################
# Function Name: cpu_stress
# Date         : 29th Jun 2020
# Author       : Noah yang<noahyang@celestica.com>
#
# Procedure Revision Details:
#   Version : 1.0  - Initial Draft  - by Noah yang<noahyang@celestica.com>
#######################################################################################################################
    def cpu_stress(self,stress_time):
        self.wpl_log_debug('Entering procedure cpu_stress: %s\n'%(str(locals())))
        Fail = 'Cpu Stress test failed'
        cmd = 'stress --cpu 8 --timeout ' + stress_time
        self.wpl_log_info(cmd)
        output = self.wpl_execute(cmd,mode=None,timeout=7500)
        self.wpl_log_info("Checking output...")
        match = re.search(Fail, output, re.IGNORECASE)
        if match:
            self.wpl_raiseException('CPU stress test fail: ERR_02_010_01')
        else:
            self.wpl_log_success('CPU Stress test pass')


#######################################################################################################################
# Function Name: set_cpu_stress_time
# Date         : 29th Jun 2020
# Author       : Noah yang<noahyang@celestica.com>
#
# Procedure Revision Details:
#   Version : 1.0  - Initial Draft  - by Noah yang<noahyang@celestica.com>
#######################################################################################################################
    def set_cpu_stress_time(self, stress_time):
        self.wpl_log_debug('Entering procedure set_cpu_stress_time with args : %s' %(str(locals())))

        self.cpu_stress_time = str(stress_time)

        self.wpl_log_success('Successfully set_cpu_stress_time: [%s] seconds.\n' %stress_time)


#######################################################################################################################
# Function Name: COMe_memory_stress
# Date         : 1th July 2020
# Author       : Noah yang<noahyang@celestica.com>
#
# Procedure Revision Details:
#   Version : 1.0  - Initial Draft  - by Noah yang<noahyang@celestica.com>
#######################################################################################################################
    def COMe_memory_stress(self,stress_time):
        self.wpl_log_debug('Entering procedure COMe_memory_stress: %s\n'%(str(locals())))
        Fail = 'Cpu Stress test failed'
        cmd = ('stressapptest -s %s -m 8 -i 8 -C 8 -M  -l'%(stress_time))
        self.wpl_log_info(cmd)
        output = self.wpl_execute(cmd,mode=None,timeout=7500)
        self.wpl_log_info('Checking output...')
        match = re.search(Fail, output, re.IGNORECASE)
        if match:
            self.wpl_raiseException('COME memory stress test fail: ERR_02_009_01')
        else:
            self.wpl_log_success('COMe memory stress test pass')


#######################################################################################################################
# Function Name: set_come_memory_stress_time
# Date         : 1th July 2020
# Author       : Noah yang<noahyang@celestica.com>
#
# Procedure Revision Details:
#   Version : 1.0  - Initial Draft  - by Noah yang<noahyang@celestica.com>
#######################################################################################################################
    def set_come_memory_stress_time(self, stress_time):
        self.wpl_log_debug('Entering procedure set_come_memory_stress_time with args : %s' %(str(locals())))

        self.COMe_memory_stress_time = str(stress_time)

        self.wpl_log_success('Successfully set_come_memory_stress_time: [%s] seconds.\n' %stress_time)


#######################################################################################################################
# Function Name: set_auto_load_script_stress_time
# Date         : 14th May 2020
# Author       : TK NG<tikng@celestica.com>
#
# Procedure Revision Details:
#   Version : 1.0  - Initial Draft  - by TK NG<tikng@celestica.com>
#######################################################################################################################
    def set_auto_load_script_stress_time(self, stress_time):
        self.wpl_log_debug('Entering procedure set_auto_load_script_stress_time with args : %s' %(str(locals())))

        self.auto_load_script_stress_time = str(stress_time)

        self.wpl_log_success('Successfully set_auto_load_script_stress_time: [%s] seconds.\n' %stress_time)


#######################################################################################################################
# Function Name: set_sensor_reading_stress_max_cycle
# Date         : 1th July 2020
# Author       : Noah yang<noahyang@celestica.com>
#
# Procedure Revision Details:
#   Version : 1.0  - Initial Draft  - by Noah yang<noahyang@celestica.com>
#######################################################################################################################
    def set_sensor_reading_stress_max_cycle(self, max_cycle):
        self.wpl_log_debug('Entering procedure set_sensor_reading_stress_max_cycle with args : %s' %(str(locals())))

        self.sensor_reading_max_cycles = str(max_cycle)

        self.wpl_log_success('Successfully set_sensor_reading_stress_max_cycle: [%s] loops.\n' %max_cycle)

    @logThis
    def run_sensor_with_init_stress_test(self, toolName, option, bmc_path, toolName1, option1, sdk_path):

        CommonLib.switch_to_centos()
        if sdk_path:
            cmd = 'cd ' + sdk_path
            self.device.sendMsg(cmd+'\n')

        cmd1 = toolName + option
        self.device.sendMsg(cmd1 + '\n')
       # pattern_line = "completed successfully. Using regular LLD implementation"
       # line = self.device.readUntil(pattern_line, timeout=60)
        #if line:
        #self.wpl_log_debug("///////finding the line match!///////////")
        CommonLib.switch_to_openbmc()
        self.wpl_getPrompt(openbmc_mode, timeout=60)
        self.wpl_log_debug('switch to openbmc successfully')
        #else:
           # self.wpl_raiseException('Can not capture the message %s' % pattern_line)
           # CommonLib.change_dir(SYSTEM_SDK_PATH, CENTOS_MODE)

        #CommonLib.switch_to_openbmc()
        if bmc_path:
            cmd = 'cd ' + bmc_path
            self.device.sendMsg(cmd + '\n')

        command = toolName1 + option1
        passcount = 0
        output = self.wpl_execute(command,mode=openbmc_mode, timeout=900)
        match_pattern = [
        r'SMB_GB_HIGH_TEMP.*?C',
        r'SMB_GB_TEMP1.*?C',
        r'SMB_GB_TEMP2.*?C',
        r'SMB_GB_TEMP3.*?C',
        r'SMB_GB_TEMP4.*?C',
        r'SMB_GB_TEMP5.*?C',
        r'SMB_GB_TEMP6.*?C',
        r'SMB_GB_TEMP7.*?C',
        r'SMB_GB_TEMP8.*?C',
        r'SMB_GB_TEMP9.*?C',
        r'SMB_GB_TEMP10.*?C',
        r'check_sensor_util_status.*PASS'
        ]
        pattern_list = []
        for line in output.splitlines():
            line = line.strip()
            for i in range(0,len(match_pattern)):
                match = re.search(match_pattern[i], line)

                if match:
                    passcount += 1
                    pattern_list.append(match_pattern[i])
        self.wpl_log_info("/////passcount=%s///////" % passcount)
        self.wpl_log_info("/////list length is %s///////" % len(pattern_list))
        if passcount == len(pattern_list):
            self.wpl_log_info('Successfully run_sensor_with_init_stress_test: [%s]' % command)
            CommonLib.switch_to_centos()
            time.sleep(300)
            CommonLib.switch_to_centos()
            CommonLib.change_dir(SYSTEM_SDK_PATH, centos_mode)
        else:
            CommonLib.switch_to_centos()
            time.sleep(300)
            CommonLib.switch_to_centos()
            CommonLib.change_dir(SYSTEM_SDK_PATH, centos_mode)
            self.wpl_log_info('Failed to run_sensor_with_init_stress_test: [%s]' % command)
            self.wpl_raiseException('Failed test GB_temp, please see output.')
#######################################################################################################################
# Function Name: sdk_for_init_sensor
# Date         : 1th July 2020
# Author       : Noah yang<noahyang@celestica.com>
#
# Procedure Revision Details:
#   Version : 1.0  - Initial Draft  - by Noah yang<noahyang@celestica.com>
#######################################################################################################################
    def sdk_for_init_sensor(self):
        self.wpl_log_debug('Entering procedure run_sdk_for_init_sensor: %s\n'%(str(locals())))
        cmd = 'python3 auto_load_user.py -c l2_cpu -d 1'
        quit = 'exit()'
        self.wpl_transmit(cmd)
        Pass_Messg = SNAKE_TRAFFIC_PASS_MSG
        output = self.wpl_receive(Pass_Messg,timeout=300)
        time.sleep(30)
        self.wpl_transmit(quit)
        self.wpl_flush()


#######################################################################################################################
# Function Name: sdk_for_init_sensor_high_load
# Date         : 13th July 2020
# Author       : Noah yang<noahyang@celestica.com>
#
# Procedure Revision Details:
#   Version : 1.0  - Initial Draft  - by Noah yang<noahyang@celestica.com>
#######################################################################################################################
    def sdk_for_init_sensor_high_load(self):
        self.wpl_log_debug('Entering procedure sdk_for_init_sensor_high_load: %s\n'%(str(locals())))
        cmd = 'python3 auto_load_user.py -c l2_cpu -d 2000'
        quit = 'exit()'
        self.wpl_transmit(cmd)
        Pass_Messg = SNAKE_TRAFFIC_PASS_MSG
        output = self.wpl_receive(Pass_Messg,timeout=2300)
        time.sleep(30)
        self.wpl_transmit(quit)
        self.wpl_flush()


#######################################################################################################################
# Function Name: sdk_for_init_sensor_loading
# Date         : 14th May 2020
# Author       : TK NG<tikng@celestica.com>
#
# Procedure Revision Details:
#   Version : 1.0  - Initial Draft  - by TK NG<tikng@celestica.com>
#######################################################################################################################
    def sdk_for_init_sensor_loading(self, toolName, optionStr, toolPath, logFile, passMsg, testType, dut_platform):
        self.wpl_log_debug('Entering procedure run_sdk_for_init_sensor_loading: %s\n'%(str(locals())))

        # remove auto_load_user_output.log
        cmd = ('rm -f %s' %logFile)
        self.wpl_execute(cmd, mode=centos_mode, timeout=60)
        self.wpl_flush()
        CommonLib.change_dir(toolPath)

        if 'high' in testType:
            # run sdk traffic test process in background
            cmd1 = ('%s %s > %s&' %(toolName, optionStr, logFile))
            self.wpl_log_info(cmd1)
            self.wpl_transmit(cmd1)
            self.wpl_flush()
            time.sleep(10)
            if self.check_background_sdk_tool_process(toolName) == True:
                self.wpl_log_info('Successfully started SDK tool process in background: [%s]' %cmd1)
            else:
                self.wpl_log_info('Failed to start SDK tool process in background: [%s]' %cmd1)
                self.wpl_raiseException('Failed sdk_for_init_sensor_loading')
        else: # idle testType
            # run sdk init and wait for process to complete
            sdk_console = ""
            match = re.search('wedge400c|cloudripper', dut_platform, re.IGNORECASE)
            if match:
                cmd2 = ('%s %s' %(toolName, optionStr))
                quit = 'exit()'
                pattern_list = SDK_WAIT_PATTERN_LIST
                sdk_console = COMMON_SDK_PROMPT
            else:
                cmd2 = ('./%s %s' %(toolName, optionStr))
                quit = 'exit'
                pattern_list = MINIPACK2_SDK_WAIT_PATTERN_LIST
                sdk_console = MINIPACK2_SDK_PROMPT

            self.wpl_log_info('cmd=[%s]' %cmd2)
            self.wpl_transmit(cmd2)
            time_out = self.auto_load_script_stress_time
            output = self.wpl_receive(pattern_list,timeout=time_out)
            time.sleep(2)
            self.wpl_log_debug(output)
            output = output.strip()
            lastStr = output.split()[-1]
            if re.search(sdk_console, lastStr):
                time.sleep(3)
                self.wpl_log_info('cmd=[%s]' %quit)
                self.wpl_transmit(quit)
                self.wpl_flush()
            else:
                self.wpl_log_fail('Failed running auto_load_user script.')
                self.wpl_raiseException('Failed sdk_for_init_sensor_loading')

            found = False
            for line in output.splitlines():
                #self.wpl_log_debug('%s' %line)
                line = line.strip()
                if len(line) == 0:
                    # blank line
                    continue
                else:
                    match = re.search(passMsg, line, re.IGNORECASE)
                    if match:
                        found = True
                        break

            if found == False:
                self.wpl_log_fail('Failed running auto_load_user script.')
                self.wpl_raiseException('Failed sdk_for_init_sensor_loading')
            else:
                self.wpl_log_success('Successfully run: %s' %cmd2)


#######################################################################################################################
# Function Name: perform_sensor_reading_high_loading_stress_test
# Date         : 14th May 2020
# Author       : TK NG<tikng@celestica.com>
#
# Procedure Revision Details:
#   Version : 1.0  - Initial Draft  - by TK NG<tikng@celestica.com>
#######################################################################################################################
    def perform_sensor_reading_loading_stress_test(self, toolName, optionStr, toolPath, logFile, completeMsg, passMsg, sensorToolName, sensorToolOption, sensorToolPath, testType, dut_platform):
        self.wpl_log_debug('Entering procedure perform_sensor_reading_loading_stress_test: %s\n'%(str(locals())))

        if 'high' in testType:
            self.wpl_log_success('Performing sensor reading high loading stress test.')
        else:
            self.wpl_log_success('Performing sensor reading idle stress test.')

        CommonLib.switch_to_centos()

        TH4_Present = True
        if dut_platform == 'minipack2':
            # check for TH4 presence
            TH4_Present = self.minipack2CheckTH4Presence()

        if TH4_Present:
            # make sure no auto_load_user.py process running in the background
            self.check_and_terminate_sdk_tool_process(toolName)

            # high load testType: run auto_load_user.py process in the background
            # idle testType: run auto_load_user process and wait for it to complete
            self.sdk_for_init_sensor_loading(toolName, optionStr, toolPath, logFile, passMsg, testType, dut_platform)

        # run sensor reading stress test
        status = self.sensor_reading(sensorToolName, sensorToolOption, sensorToolPath, dut_platform)

        if 'high' in testType:
            if TH4_Present:
                CommonLib.switch_to_centos()

                # allow some more time for process to complete
                count = 2*int(self.auto_load_script_stress_time)
                completion_flag = False
                timeout_flag = False
                t1 = time.time()
                t2 = t1
                output = ''
                self.wpl_log_info("waiting for %s process to complete..." %toolName)
                # wait for auto_load_user.py script to complete
                while (completion_flag == False):
                    cmd = ('cat %s | grep \"%s\"' %(logFile, completeMsg))
                    self.wpl_log_debug(cmd)
                    output = self.wpl_execute(cmd, mode=centos_mode, timeout=300)
                    if re.search(completeMsg, output, re.IGNORECASE):
                        self.wpl_log_info("%s process completed." %toolName)
                        completion_flag = True
                        break
                    t2 = time.time()
                    time_diff = int(t2 - t1)
                    if time_diff > count:
                        timeout_flag = True
                        break
                    time.sleep(60)

                time.sleep(3)
                self.check_and_terminate_sdk_tool_process(toolName)

                if timeout_flag == True:
                    self.wpl_raiseException('Error: timeout running %s script.' %toolName)
                else:
                    cmd3 = ('cat %s | grep \"%s\"' %(logFile, passMsg))
                    self.wpl_log_info(cmd3)
                    self.wpl_transmit(cmd3)
                    output3 = self.wpl_receive(passMsg, timeout=300)
                    self.wpl_log_info(output3)
                    match3 =  re.search(passMsg, output3, re.IGNORECASE)
                    if match3 is None:
                        self.wpl_raiseException('Error running %s script' %toolName)

            if status:
                self.wpl_raiseException('Failed sensor reading high loading stress test.')
            else:
                self.wpl_log_success('Successfully perform sensor reading high loading stress test.')
        else:
            if status:
                self.wpl_raiseException('Failed sensor reading idle stress test.')
            else:
                self.wpl_log_success('Successfully perform sensor reading idle stress test.')


#######################################################################################################################
    def w400_perform_sensor_reading_loading_stress_test(self, toolName, optionStr, toolPath, startTraffic, portStatusPattern, stopTraffic, exitTraffic, runTime, sensorToolName, sensorToolOption, sensorToolPath, testType, dut_platform):
        self.wpl_log_debug('Entering procedure w400_perform_sensor_reading_loading_stress_test: %s\n'%(str(locals())))

        bcm_tool = 'bcm.user'
        self.check_and_terminate_sdk_tool_process(bcm_tool)
        t1 = time.time()
        if 'high' in testType:
            self.wpl_log_success('Performing sensor reading high loading stress test.')
        else:
            self.wpl_log_success('Performing sensor reading idle stress test.')
        CommonLib.switch_to_centos()
        CommonLib.change_dir(toolPath)

        #### start sdk traffic
        traffic_info = 'Completed the snake traffic setting'
        pattern_info = 'misc config end'
        self.wpl_log_info('***running auto_load_user.sh***')
        cmd = './' + toolName + ' ' + optionStr
        self.wpl_log_info('cmd=[%s]' % cmd)
        self.wpl_transmit(cmd)
        output = self.wpl_receive(pattern_info, timeout=80)
        if re.search('fail', output, re.IGNORECASE):
            self.wpl_raiseException('Failed run sdk init test.')
        else:
            self.wpl_log_info('sdk init pass, will start traffic test.')
            output1 = self.device.sendCmdRegexp('./' + startTraffic, traffic_info, timeout=80)
            if 'Completed the snake' in output1:
                self.wpl_log_info('running traffic test.')
                self.device.sendMsg('\n')
                time.sleep(3)
            else:
                self.wpl_raiseException('Failed run sdk traffic.')

        # run sensor reading stress test
        self.wpl_sdk_switch_to_bmc()
        result1 = self.sensor_reading(sensorToolName, sensorToolOption, sensorToolPath, dut_platform)

        # stop cpu traffic stress test
        self.wpl_bmc_switch_to_sdk()
        result2 = self.w400_stop_cpu_traffic_stress_test(stopTraffic)
        if result2:
            self.wpl_log_fail('Failed minipack2_stop_cpu_traffic_stress_test.')
            self.wpl_raiseException('Failed minipack2_perform_sensor_reading_high_loading_stress_test')

        # exit SDK
        self.wpl_execute_cmd('./' + exitTraffic)

        t2 = time.time()
        time_diff = int(t2 - t1)
        self.wpl_log_debug('Total test time: [%s]' % (str(time_diff)))

        if result1:
            self.wpl_sdk_switch_to_bmc()
            self.wpl_log_fail('Failed sensor_reading.')
            self.wpl_raiseException('Failed minipack2_perform_sensor_reading_high_loading_stress_test')
        else:
            self.wpl_log_success('Successfully run minipack2_perform_sensor_reading_high_loading_stress_test.')

#######################################################################################################################
    def w400_stop_cpu_traffic_stress_test(self, stop_traffic_cmd):
        self.wpl_log_debug('Entering procedure w400_stop_cpu_traffic_stress_test: %s\n' % (str(locals())))
        #stop cpu traffic
        self.wpl_log_info('*** stop cpu traffic ***')
        self.wpl_log_info('cmd=[%s]' % stop_traffic_cmd)
        self.device.sendCmdRegexp('./' + stop_traffic_cmd, self.device.promptDiagOS, timeout=80)
        time.sleep(2)


#######################################################################################################################
# Function Name: platform_set_snake_traffic_test_stress_time
# Date         : 14th May 2020
# Author       : TK NG<tikng@celestica.com>
#
# Procedure Revision Details:
#   Version : 1.0  - Initial Draft  - by TK NG<tikng@celestica.com>
#######################################################################################################################
    def platform_set_snake_traffic_test_stress_time(self, stress_time):
        self.wpl_log_debug('Entering procedure platform_set_snake_traffic_test_stress_time: %s\n'%(str(locals())))

        self.snake_traffic_test_time = str(stress_time)

        self.wpl_log_success('Successfully platform_set_snake_traffic_test_stress_time: %s\n'%(str(stress_time)))


#######################################################################################################################
# Function Name: perform_snake_traffic_stress_test
# Date         : 20th July 2020
# Author       : Noah yang<noahyang@celestica.com>
#
# Procedure Revision Details:
#   Version : 1.0  - Initial Draft  - by Noah yang<noahyang@celestica.com>
#######################################################################################################################
    def perform_snake_traffic_stress_test(self, toolName, toolPath, runTime, portMode):
        self.wpl_log_debug('Entering procedure perform_snake_traffic_stress_test: %s\n'%(str(locals())))

        CommonLib.switch_to_centos()

        CommonLib.change_dir(toolPath)

        # make sure no auto_load_user.py process running in the background
        self.check_and_terminate_sdk_tool_process(toolName)

        cmd = ('python3 %s -c l2_cpu -d %s -p %s'%(toolName, runTime, portMode))
        self.wpl_transmit(cmd)
        pattern_list = SDK_WAIT_PATTERN_LIST
        output = self.wpl_receive(pattern_list,timeout=SDK_TIMEOUT2)
        #self.wpl_log_debug('output = [%s]' %output)

        time.sleep(1)
        self.wpl_transmit('exit()')
        self.wpl_flush()

        found = False
        Pass_Messg = SNAKE_TRAFFIC_PASS_MSG
        for line in output.splitlines():
            #self.wpl_log_debug('%s' %line)
            line = line.strip()
            if len(line) == 0:
                # blank line
                continue
            else:
                match = re.search(Pass_Messg, line, re.IGNORECASE)
                if match:
                    found = True
                    break

        if found == False:
            self.wpl_raiseException('Failed perform_snake_traffic_stress_test')
        else:
            self.wpl_log_success("Successfully run perform_snake_traffic_stress_test for %s seconds. PASSED." %runTime)


#######################################################################################################################
# Function Name: get_board_type
# Date         : 20th July 2020
# Author       : Noah yang<noahyang@celestica.com>
#
# Procedure Revision Details:
#   Version : 1.0  - Initial Draft  - by Noah yang<noahyang@celestica.com>
#######################################################################################################################
    def get_board_type(self):
        self.wpl_log_debug('Entering procedure get_board_type: %s\n'%(str(locals())))
        cmd = './cel-platform-test -i'
        board_type ='Wedge-400C'
        Err = 'No such file or directory'
        output = self.wpl_execute(cmd)
        match = re.search(Err, output, re.IGNORECASE)
        if match:
           self.wpl_raiseException('No such file or directory')
        else:
            if re.search(board_type, output, re.IGNORECASE):
               self.board_type = str(1)
            else:
               self.board_type = str(0)

        self.wpl_log_success('get_board_type:%s \n'%(output))


#######################################################################################################################
# Function Name: SDK_re_init_test
# Date         : 14th May 2020
# Author       : TK NG<tikng@celestica.com>
#
# Procedure Revision Details:
#   Version : 1.0  - Initial Draft  - by TK NG<tikng@celestica.com>
#######################################################################################################################
    def SDK_re_init_test(self, cycle, stress_time, toolPath):
        self.wpl_log_debug('Entering procedure SDK_re_init_test: %s\n'%(str(locals())))

        CommonLib.switch_to_centos()

        CommonLib.change_dir(toolPath)

        # make sure no auto_load_user.py process running in the background
        self.check_and_terminate_sdk_tool_process(SDK_TOOL)

        # 1 cycle takes about 1160 seconds
        t1 = time.time()

        cmd = 'python3 %s -c all --run_case 1'%(SDK_TOOL)
        self.wpl_log_info(cmd)
        self.wpl_transmit(cmd)
        pattern_list = SDK_WAIT_PATTERN_LIST
        output = self.wpl_receive(pattern_list,timeout=SDK_TIMEOUT2)

        t2 = time.time()
        time_diff = int(t2 - t1)
        self.wpl_log_info('Total test time: [%s]' %(str(time_diff)))

        time.sleep(2)
        self.wpl_transmit('exit()')
        self.wpl_flush()
        #self.wpl_log_info(output)

        found = False
        found1 = False
        found2 = False
        Pass_Message = GB_INIT_PASS_MSG
        Pass_Message1 = r'1[ \t]+\|[ \t]+Reload SDK\(MBIST\) Test[ \t]+\|[ \t]+1[ \t]+\|[ \t]+1[ \t]+\|.*PASS'
        #0 | GB Init Test                   |    10 |    10 |    10 |     0 | none
        Pass_Message2 = r'META Wedge400C Run Test All.*?PASS'
        for line in output.splitlines():
            #self.wpl_log_debug('%s' %line)
            if (found == True) and (found1 == True) and (found2 == True):
                break

            line = line.strip()
            if len(line) == 0:
                # blank line
                continue
            else:
                match = re.search(Pass_Message, line, re.IGNORECASE)
                if match:
                    found = True
                    continue

                match1 = re.search(Pass_Message1, line, re.IGNORECASE)
                if match1:
                    found1 = True
                    continue

                match2 = re.search(Pass_Message2, line, re.IGNORECASE)
                if match2:
                    found2 = True

        if (found == True) and (found1 == True) and (found2 == True):
            self.wpl_log_success('Successfully run SDK_re_init_test: PASSED.')
        else:
            self.wpl_raiseException('Failed SDK_re_init_test.')


#######################################################################################################################
# Function Name: platform_set_re_init_test_stress_cycles
# Date         : 14th May 2020
# Author       : TK NG<tikng@celestica.com>
#
# Procedure Revision Details:
#   Version : 1.0  - Initial Draft  - by TK NG<tikng@celestica.com>
#######################################################################################################################
    def platform_set_re_init_test_stress_cycles(self, cycles):
        self.wpl_log_debug('Entering procedure platform_set_re_init_test_stress_cycles: %s\n'%(str(locals())))

        self.re_init_cycles = str(cycles)

        self.wpl_log_success('Successfully platform_set_re_init_test_stress_cycles: cycles[%s].\n' %(cycles))


#######################################################################################################################
# Function Name: platform_set_re_init_test_stress_time
# Date         : 14th May 2020
# Author       : TK NG<tikng@celestica.com>
#
# Procedure Revision Details:
#   Version : 1.0  - Initial Draft  - by TK NG<tikng@celestica.com>
#######################################################################################################################
    def platform_set_re_init_test_stress_time(self, stress_time):
        self.wpl_log_debug('Entering procedure platform_set_re_init_test_stress_time: %s\n'%(str(locals())))

        self.re_init_stress_time = str(stress_time)

        self.wpl_log_success('Successfully platform_set_re_init_test_stress_time: stress_time[%s] seconds.\n' %(stress_time))


#######################################################################################################################
# Function Name: platform_set_port_linkup_test_stress_cycles
# Date         : 14th May 2020
# Author       : TK NG<tikng@celestica.com>
#
# Procedure Revision Details:
#   Version : 1.0  - Initial Draft  - by TK NG<tikng@celestica.com>
#######################################################################################################################
    def platform_set_port_linkup_test_stress_cycles(self, cycles):
        self.wpl_log_debug('Entering procedure platform_set_port_linkup_test_stress_cycles: %s\n'%(str(locals())))

        self.port_linkup_stress_cycles = str(cycles)

        self.wpl_log_success('Successfully platform_set_port_linkup_test_stress_cycles: cycles[%s].\n' %(cycles))


#######################################################################################################################
# Function Name: platform_set_port_linkup_stress_time
# Date         : 14th May 2020
# Author       : TK NG<tikng@celestica.com>
#
# Procedure Revision Details:
#   Version : 1.0  - Initial Draft  - by TK NG<tikng@celestica.com>
#######################################################################################################################
    def platform_set_port_linkup_stress_time(self, stress_time):
        self.wpl_log_debug('Entering procedure platform_set_port_linkup_stress_time: %s\n'%(str(locals())))

        self.port_linkup_stress_time = str(stress_time)

        self.wpl_log_success('Successfully platform_set_port_linkup_stress_time: stress_time[%s] seconds.\n' %(stress_time))


#######################################################################################################################
# Function Name: perform_port_enable_disable_stress_test
# Date         : 14th May 2020
# Author       : TK NG<tikng@celestica.com>
#
# Procedure Revision Details:
#   Version : 1.0  - Initial Draft  - by TK NG<tikng@celestica.com>
#######################################################################################################################
    def perform_port_enable_disable_stress_test(self, initTool, initOption, toolPath, cycles):
        self.wpl_log_debug('Entering procedure perform_port_enable_disable_stress_test: %s\n'%(str(locals())))

        CommonLib.switch_to_centos()

        CommonLib.change_dir(toolPath)

        # make sure no auto_load_user.py process running in the background
        self.check_and_terminate_sdk_tool_process(SDK_TOOL)

        t1 = time.time()
        cmd = ('python3 %s %s' %(initTool, initOption))
        self.wpl_log_info(cmd)
        self.wpl_transmit(cmd)
        pattern_list = SDK_WAIT_PATTERN_LIST
        output = self.wpl_receive(pattern_list,timeout=SDK_TIMEOUT2)

        t2 = time.time()
        time_diff = int(t2 - t1)
        self.wpl_log_info('Total test time: [%s]' %(str(time_diff)))

        time.sleep(2)
        self.wpl_transmit('exit()')
        self.wpl_flush()
        #self.wpl_log_info(output)

        found = False
        found1 = False
        found2 = False
        Pass_Message = GB_PORT_LINKUP_PASS_MSG
        Pass_Message1 = r'6[ \t]+\|[ \t]+Port Link-UP Validation Test[ \t]+\|[ \t]+1[ \t]+\|[ \t]+1[ \t]+\|.*PASS'
        Pass_Message2 = 'META Wedge400C Run Test All.*PASS'

        for line in output.splitlines():
            #self.wpl_log_debug('%s' %line)
            if (found == True) and (found1 == True) and (found2 == True):
                break

            line = line.strip()
            if len(line) == 0:
                # blank line
                continue
            else:
                match = re.search(Pass_Message, line, re.IGNORECASE)
                if match:
                    found = True
                    continue

                match1 = re.search(Pass_Message1, line, re.IGNORECASE)
                if match1:
                    found1 = True
                    continue

                match2 = re.search(Pass_Message2, line, re.IGNORECASE)
                if match2:
                    found2 = True

        if (found == True) and (found1 == True) and (found2 == True):
            self.wpl_log_success('Successfully perform_port_enable_disable_stress_test: PASSED.')
        else:
            self.wpl_raiseException('Failed perform_port_enable_disable_stress_test.')


#######################################################################################################################
    def w400_perform_port_enable_disable_stress_test(self, AllPort, initTool, initToolPath, bcmVlanCmd, bcmDDTrafficCmd, bcm56TrafficCmd, stressCycles, runTime, bcmStopDDCmd, bcmStop56Cmd, upStatus, downStatus, portStatusCmd, setPortCmd, portEnable, portDisable, bcmDDCounters, bcm56Counters, rpktPattern, tpktPattern):
        self.wpl_log_debug('Entering procedure w400_perform_port_enable_disable_stress_test with args : %s' % (str(locals())))

        CommonLib.switch_to_centos()
        CommonLib.change_dir(initToolPath)

        #1. make sure no auto_load_user.py process running in the background
        self.check_and_terminate_sdk_tool_process('bcm.user')

        #2. run auto_load_user.sh
        initOption = ''
        status = self.w400_sdk_init_check(initTool, initOption, SDK_TIMEOUT1)
        if status == 0:
            self.wpl_log_info('Successfully run auto_load_user.sh')
        else:
            if status == 1:
                self.minipack2_exit_sdk()
            self.wpl_raiseException('Failed w400_perform_port_enable_disable_stress_test.')
        time.sleep(5)

        #3. execute 'ps cd' command and check ports status, pattern1 is up status
        self.wpl_log_info('***checking all ports status***')
        result1 = self.w400_check_port_status(portStatusCmd, upStatus, 'enable')
        if result1 == 0:
            self.wpl_log_info('All ports status are up.')
        else:
            self.minipack2_exit_sdk()
            self.wpl_raiseException('Failed w400_perform_port_enable_disable_stress_test.')
        time.sleep(1)

        #4. start port enable or disable test
        found = False
        max_cycles = int(stressCycles)
        for i in range(0, max_cycles):
            self.wpl_log_info('************************************************************')
            self.wpl_log_info('*** Test Repeat Loop #: %s / %s ***' % ((i + 1), str(max_cycles)))
            self.wpl_log_info('************************************************************')

            # disable port
            self.w400_set_each_port(AllPort, setPortCmd, portDisable, SDK_TIMEOUT1)
            time.sleep(3)
            result2 = self.w400_check_port_status(portStatusCmd, downStatus, 'disable')
            if result2 == 0:
                self.wpl_log_info('Successfully disabled all ports')
            else:
                self.wpl_raiseException('Failed w400_perform_port_enable_disable_stress_test')

            # enable port
            self.w400_set_each_port(AllPort, setPortCmd, portEnable, SDK_TIMEOUT1)
            time.sleep(8)
            result3 = self.w400_check_port_status(portStatusCmd, upStatus, 'enable')
            if result3 == 0:
                self.wpl_log_info('Successfully enabled all ports')
            else:
                self.wpl_raiseException('Failed w400_perform_port_enable_disable_stress_test')

            ## traffic test
            result4 = self.w400_perform_cpu_traffic_check(bcmVlanCmd, bcmDDTrafficCmd, bcm56TrafficCmd, runTime, bcmStopDDCmd, bcmStop56Cmd, bcmDDCounters, rpktPattern, tpktPattern, bcm56Counters)
            if result4:
                self.wpl_raiseException('Failed w400_perform_port_enable_disable_stress_test')

        #5. exit BCM>
        self.minipack2_exit_sdk()
        self.wpl_log_success('Successfully run w400_perform_port_enable_disable_stress_test.\n')


#######################################################################################################################
    def w400_SDK_re_init_test(self, initTool, initOption, initToolPath, bcmVlanCmd, bcmDDTrafficCmd, bcm56TrafficCmd, runTime, bcmStopDDCmd, bcmStop56Cmd, portStatusCmd, upStatus, trafficCounters, rpktPattern, tpktPattern):
        self.wpl_log_debug('Entering procedure w400_SDK_re_init_test: %s\n'%(str(locals())))

        CommonLib.switch_to_centos()
        CommonLib.change_dir(initToolPath)

        max_cycles = int(self.re_init_cycles)
        for i in range(0, max_cycles):
            self.wpl_log_info('************************************************************')
            self.wpl_log_info('*** Test Repeat Loop #: %s / %s ***' %((i+1), str(max_cycles)))
            self.wpl_log_info('************************************************************')
            # 1. run auto_load_user.sh
            status = self.w400_sdk_init_check(initTool, initOption, SDK_TIMEOUT1)
            if status == 0:
                self.wpl_log_info('Successfully run auto_load_user.sh')
            else:
                if status == 1:
                    self.minipack2_exit_sdk()
                self.wpl_raiseException('Failed w400_SDK_re_init_test.')
            time.sleep(5)

            # 2. execute 'ps cd' command and check ports status, upStatus is up status
            self.wpl_log_info('***checking all ports status***')
            result1 = self.w400_check_port_status(portStatusCmd, upStatus, 'enable')
            if result1 == 0:
                self.wpl_log_info('All ports status are up.')
            else:
                self.minipack2_exit_sdk()
                self.wpl_raiseException('Failed w400_SDK_re_init_test.')
            time.sleep(1)

            #3. traffic test and counters
            result2 = self.w400_perform_cpu_traffic_check(bcmVlanCmd, bcmDDTrafficCmd, bcm56TrafficCmd, runTime, bcmStopDDCmd, bcmStop56Cmd, trafficCounters, rpktPattern, tpktPattern)
            if result2:
                self.wpl_raiseException('Failed w400_SDK_re_init_test')

            #4. exit sdk
            self.minipack2_exit_sdk()

        self.wpl_log_success('Successfully run w400_SDK_re_init_test: PASSED.')


#######################################################################################################################
    def w400_perform_snake_traffic_stress_test(self, initTool, initOption, initToolPath, bcmTrafficCmd, runTime, bcmPortCmd, bcmUpStatus, bcmStopDDTrafficCmd, bcmStop56TrafficCmd, bcmTrafficCounters, rpktPattern, tpktPattern):
        self.wpl_log_debug('Entering procedure w400_perform_snake_traffic_stress_test with args : %s' %(str(locals())))

        # check bcm.user in background first.
        bcm_tool = 'bcm.user'
        self.check_and_terminate_sdk_tool_process(bcm_tool)
        #1. start traffic test
        result = self.w400_start_cpu_traffic_stress_test(initTool, initOption, initToolPath, bcmTrafficCmd, runTime, bcmPortCmd, bcmUpStatus)
        if result:
            self.wpl_raiseException('Failed w400_perform_snake_traffic_stress_test')

        #2. stop traffic test
        stop_cmd_list = [bcmStopDDTrafficCmd, bcmStop56TrafficCmd]
        for cmd1 in stop_cmd_list:
            result1 = self.w400_run_traffic_cmd(cmd1, SDK_TIMEOUT1)
            if result1:
                self.wpl_log_fail('Error stopping cpu traffic.')
                self.wpl_raiseException('Failed w400_perform_snake_traffic_stress_test')
                # self.minipack2_exit_sdk()
                return 1
            time.sleep(3)

        #3. check port counters
        speed_message = '400and200G'
        result2 = self.w400_cpu_traffic_check_port_counters(bcmTrafficCounters, speed_message, rpktPattern, tpktPattern)
        if result2:
            self.wpl_raiseException('Failed w400_perform_cpu_traffic_check.')
            # self.minipack2_exit_sdk()
            return 1

        #4. exit sdk
        self.minipack2_exit_sdk()

        self.wpl_log_success("Successfully run w400_perform_snake_traffic_stress_test for %s seconds. PASSED." %runTime)


#######################################################################################################################
    def w400_sdk_init_check(self, initTool, initOption, sdkTimeout):
        self.wpl_log_debug('Entering procedure w400_sdk_init_check with args : %s' %(str(locals())))

        # run auto_load_user.sh
        self.wpl_log_info('***running auto_load_user.sh***')
        cmd = './' + initTool + ' ' + initOption
        self.wpl_log_info('cmd=[%s]' %cmd)
        self.wpl_transmit(cmd)
        pattern_list = MINIPACK2_SDK_PROMPT
        output = self.wpl_receive(pattern_list, timeout=sdkTimeout)
        # self.wpl_log_info('output=[%s]' %output)
        if re.search('misc config end', output, re.IGNORECASE):
            # success
            return 0
        else:
            self.wpl_log_fail('Failed w400_sdk_init_check.')
            return 1


#######################################################################################################################
    def w400_check_port_status(self, portStatusCmd, pattern, message):
        self.wpl_log_debug('Entering procedure w400_check_port_status with args : %s' %(str(locals())))

        pattern_list = MINIPACK2_SDK_PROMPT

        # port status
        cmd = portStatusCmd
        self.wpl_log_info('cmd=[%s]' %cmd)
        self.wpl_transmit(cmd)
        output = self.wpl_receive(pattern_list,timeout=SDK_TIMEOUT1)
        #self.wpl_log_debug('output=[%s]' %output)
        time.sleep(1)
        # self.wpl_log_info("Checking \'%s\' output..." %(cmd))

        port_count = 0
        for line in output.splitlines():
            line = line.strip()
            match2 = re.search(pattern, line, re.IGNORECASE)
            if match2:
                port_count += 1

        if port_count == 48:
            self.wpl_log_info("Checked \'%s\' output status: PASSED" % (cmd))
            return 0
        else:
            self.wpl_log_fail('Error: Only %s number of ports counter information found ! Expected 48 ports status information.' %(str(port_count)))
            return 1


#######################################################################################################################
    def w400_set_each_port(self, AllPort, setPortCmd, portOption, sdkTimeout):
        self.wpl_log_debug('Entering procedure w400_set_each_port with args : %s' %(str(locals())))

        if portOption == 'en=0':
            ## disable port
            self.wpl_log_info('***Disable each port***')
        else:
            self.wpl_log_info('***enable each port***')
        pattern_list = MINIPACK2_SDK_WAIT_PATTERN_LIST
        max_ports = 48
        if AllPort == 'True':
            cmd = setPortCmd + '0-cd47 ' + portOption
            self.wpl_log_info('cmd=[%s]' % cmd)
            self.wpl_transmit(cmd)
            self.wpl_receive(pattern_list, timeout=sdkTimeout)
            time.sleep(1)
        else:
            for i in range(0, max_ports):
                cmd = ('%s%s %s' %(setPortCmd, str(i), portOption))
                self.wpl_log_info('cmd=[%s]' %cmd)
                self.wpl_transmit(cmd)
                self.wpl_receive(pattern_list, timeout=sdkTimeout)
                time.sleep(0.5)


#######################################################################################################################
    def w400_perform_cpu_traffic_check(self, bcmVlanCmd, bcmDDTrafficCmd, bcm56TrafficCmd, runTime, bcmStopDDCmd, bcmStop56Cmd, bcmDDCounters, rpktPattern, tpktPattern, bcm56Counters=None):
        self.wpl_log_debug('Entering procedure w400_perform_cpu_traffic_check: %s\n'%(str(locals())))

        #1. run snake_xxx.soc command
        status = self.w400_run_traffic_cmd(bcmVlanCmd, SDK_TIMEOUT1)
        if status == 0:
            self.wpl_log_info('Successfully run snake_xxx.soc command.')
        else:
            self.wpl_log_fail('Failed run snake_xxx.soc command.')
            #self.minipack2_exit_sdk()
            return 1
        time.sleep(1)

        #2. clear counters
        clear_counters = 'clear c'
        status = self.w400_run_traffic_cmd(clear_counters, SDK_TIMEOUT1)
        if status == 0:
            self.wpl_log_info('Successfully cleared port counters.')
        else:
            self.wpl_log_fail('Error clearing port counters.')
            #self.minipack2_exit_sdk()
            return 1
        time.sleep(1)

        #3. start cpu traffic
        traffic_cmd_list = [bcmDDTrafficCmd, bcm56TrafficCmd]
        for cmd in traffic_cmd_list:
            status = self.w400_run_traffic_cmd(cmd, SDK_TIMEOUT1)
            if status == 0:
                self.wpl_log_info('Successfully started cpu cmd=[%s] traffic.' % cmd)
            else:
                self.wpl_log_fail('Error starting cpu traffic.')
                #self.minipack2_exit_sdk()
                return 1
            time.sleep(1)

        #4. sleep for runTime seconds
        # runTime = 'sleep 60'
        status = self.w400_run_traffic_cmd(runTime, SDK_TIMEOUT1)
        if status == 0:
            self.wpl_log_info('Successfully sleep for %s seconds.' %(str(runTime)))
        else:
            self.wpl_log_fail('Error sleeping for %s seconds.' %(str(runTime)))
            #self.minipack2_exit_sdk()
            return 1
        time.sleep(1)

        #5. stop cpu traffic
        stop_cmd_list = [bcmStopDDCmd, bcmStop56Cmd]
        for cmd1 in stop_cmd_list:
            result1 = self.w400_run_traffic_cmd(cmd1, SDK_TIMEOUT1)
            if result1:
                self.wpl_log_fail('Error stopping cpu traffic.')
                #self.minipack2_exit_sdk()
                return 1
            time.sleep(3)

        #6. check port counters
        counters_cmd_list = [bcmDDCounters, bcm56Counters]
        for cmd2 in counters_cmd_list:
            if cmd2 == None:
                continue
            var_index = counters_cmd_list.index(cmd2)
            if var_index == 0:
                speed_message = '400G'
            if var_index == 1:
                speed_message = '200G'
            result2 = self.w400_cpu_traffic_check_port_counters(cmd2, speed_message, rpktPattern, tpktPattern)
            if result2:
                self.wpl_raiseException('Failed w400_perform_cpu_traffic_check.')
                #self.minipack2_exit_sdk()
                return 1

        # exit SDK
        #self.minipack2_exit_sdk()

        self.wpl_log_success('Successfully w400_perform_cpu_traffic_check: PASSED.')
        return 0


#######################################################################################################################
    def w400_start_cpu_traffic_stress_test(self, initTool, initOption, initToolPath, bcmTrafficCmd, runTime, bcmPortCmd, bcmUpStatus):
        self.wpl_log_debug('Entering procedure w400_start_cpu_traffic_stress_test with args : %s' %(str(locals())))

        CommonLib.switch_to_centos()
        CommonLib.change_dir(initToolPath)

        # make sure no auto_load_user.py process running in the background
        #self.check_and_terminate_sdk_tool_process(initTool)

        #1. run auto_load_user.sh
        status = self.w400_sdk_init_check(initTool, initOption, SDK_TIMEOUT2)
        if status == 0:
            self.wpl_log_info('Successfully run auto_load_user.sh')
        else:
            self.wpl_log_fail('Error running auto_load_user.sh script.')
            #if status == 1:
                #self.minipack2_exit_sdk()
            return 1
        time.sleep(5)

        #2. execute 'ps cd' command and check ports status, pattern1 is up status
        self.wpl_log_info('***checking all ports status***')
        result1 = self.w400_check_port_status(bcmPortCmd, bcmUpStatus, 'enable')
        if result1 == 0:
            self.wpl_log_info('All ports status are up.')
        else:
            self.minipack2_exit_sdk()
            self.wpl_raiseException('Failed w400_start_cpu_traffic_stress_test.')
        time.sleep(1)

        #3. clear counters
        clear_counters = 'clear c'
        status = self.w400_run_traffic_cmd(clear_counters, SDK_TIMEOUT1)
        if status == 0:
            self.wpl_log_info('Successfully cleared port counters.')
        else:
            self.wpl_log_fail('Error clearing port counters.')
            # self.minipack2_exit_sdk()
            return 1
        time.sleep(1)

        #4. start cpu traffic
        status = self.w400_run_traffic_cmd(bcmTrafficCmd, SDK_TIMEOUT1)
        if status == 0:
            self.wpl_log_info('Successfully started cpu traffic.')
        else:
            self.wpl_log_fail('Error starting cpu traffic.')
            #self.minipack2_exit_sdk()
            return 1
        time.sleep(1)

        if int(runTime) != 0:
            # sleep for runTime second
            status = self.w400_sleep_and_wait(runTime)
            if status == 0:
                self.wpl_log_info('Successfully run w400_start_cpu_traffic_stress_test.')
            else:
                self.wpl_log_fail('Error sleeping for %s seconds.' %(str(runTime)))
                #self.minipack2_exit_sdk()
                return 1
        return 0


#######################################################################################################################
    def w400_run_traffic_cmd(self, bcm_traffic_cmd, sdkTimeout):
        self.wpl_log_debug('Entering procedure w400_run_traffic_cmd with args : %s' %(str(locals())))

        cmd = bcm_traffic_cmd
        self.wpl_log_info('***running cmd=[%s] test***' % cmd)
        self.wpl_transmit(cmd)
        pattern_list = ['Unknown command', MINIPACK2_SDK_PROMPT]
        output = self.wpl_receive(pattern_list, timeout=sdkTimeout)
        # self.wpl_log_info('output=[%s]' %output)
        if 'Unknown command' in output:
            self.wpl_log_fail('Failed w400_run_traffic_cmd.')
            return 1
        else:
            # success
            return 0


#######################################################################################################################
    def w400_cpu_traffic_check_port_counters(self, counters_cmd, speed_message, rpkt_pattern, tpkt_pattern):
        self.wpl_log_debug('Entering procedure w400_cpu_traffic_check_port_counters with args : %s' %(str(locals())))

        # dump counters for all ports
        self.wpl_log_info('***check %s port counters***' % speed_message)
        cmd = counters_cmd
        self.wpl_log_info('cmd=[%s]' %cmd)
        self.wpl_transmit(cmd)
        sdk_console = MINIPACK2_SDK_PROMPT
        pattern_list = MINIPACK2_SDK_WAIT_PATTERN_LIST
        output = self.wpl_receive(pattern_list,timeout=SDK_TIMEOUT1)
        self.wpl_log_debug('output=[%s]' %output)

        #e.g. Port0~Port15  couters (tx=121005984, rx=121005984)         passed
        rp_len = len(re.findall(rpkt_pattern, output))
        tp_len = len(re.findall(tpkt_pattern, output))
        if 'cd0-cd15' in counters_cmd and rp_len == 16:
            self.wpl_log_info('The %s counters number is ok!\n' % speed_message)
        elif 'cd16-cd47' in counters_cmd and rp_len == 32:
            self.wpl_log_info('The %s counters number is ok!\n' % speed_message)
        else:
            if rp_len == 48:
                self.wpl_log_info('The %s counters number is ok!\n' % speed_message)
            else:
                self.wpl_log_info('The %s counters number is failed!\n' % speed_message)
                return 1
        if rp_len and tp_len == rp_len:
            rp_lst = re.findall(rpkt_pattern, output)
            tp_lst = re.findall(tpkt_pattern, output)
            if rp_lst and rp_lst == tp_lst:
                self.wpl_log_info('The value is the same\n')
            else:
                self.wpl_raiseException("The value is different\n")
                return 1
        else:
            self.wpl_log_info('Tx counter[%s] and Rx counter[%s] does not match.' %(tp_len, rp_len))
            return 1
        self.wpl_log_info('All Tx counters and Rx counters matched. PASSED.')
        return 0


#######################################################################################################################
    def w400_sleep_and_wait(self, runTime):
        self.wpl_log_debug('Entering procedure w400_sleep_and_wait with args : %s' %(str(locals())))

        # sleep for runTime seconds
        self.wpl_log_info('***sleep for %s seconds***' %(str(runTime)))
        cmd = 'sleep ' + str(runTime)
        waitTime = int(runTime) + int(SDK_TIMEOUT1)
        self.wpl_log_info('cmd=[%s]' %cmd)
        self.wpl_transmit(cmd)
        pattern_list = MINIPACK2_SDK_WAIT_PATTERN_LIST
        output = self.wpl_receive(pattern_list, timeout=waitTime)
        if re.search('Error|Fail', output, re.IGNORECASE):
            self.wpl_log_info('output=[%s]' %output)
            self.wpl_log_fail('Failed w400_sleep_and_wait: [Error/Fail] message found.')
            return 1
        else:
            # success
            return 0


#######################################################################################################################
# Function Name: replace_sensor_cfg_and_diag_init
# Date         : 29th Jun 2020
# Author       : Noah yang<noahyang@celestica.com>
#
# Procedure Revision Details:
#   Version : 1.0  - Initial Draft  - by Noah yang<noahyang@celestica.com>
#######################################################################################################################
    def replace_sensor_cfg_and_diag_init(self):
        self.wpl_log_debug('Entering procedure replace_sensor_cfg_and diag_init: %s\n'%(str(locals())))

        CommonLib.change_dir(BMC_DIAG_TOOL_PATH)
        cmd = './cel-psu-test -s'
        output = self.wpl_execute(cmd)
        psu_type = 'device.cfg sets PSU_PEM_TYPE not PSU'
        if re.search(psu_type, output, re.IGNORECASE):
            self.wpl_log_debug('Detected system installed with PEM type.')
            init = './cel-diag-init -d'
            flag = 1
        else:
            self.wpl_log_debug('Detected system installed with PSU type.')
            init = './cel-diag-init -a'
            flag = 0

        output = self.wpl_execute(init)

        if flag == 1:
            replace = ('cp %s/sensors.cfg %s' %(BMC_DIAG_DC_CONFIG_PATH, BMC_DIAG_CONFIG_PATH))
        else:
            replace = ('cp %s/sensors.cfg %s' %(BMC_DIAG_AC_CONFIG_PATH, BMC_DIAG_CONFIG_PATH))

        output = self.wpl_execute(replace)
        p1 = 'No such file or directory'
        if re.search(p1, output, re.IGNORECASE):
            if flag == 1:
                self.wpl_log_info('sensors.cfg file not found in \'%s\' path. Using default sensor.cfg file.' %BMC_DIAG_DC_CONFIG_PATH)
            else:
                self.wpl_log_info('sensors.cfg file not found in \'%s\' path. Using default sensor.cfg file.' %BMC_DIAG_AC_CONFIG_PATH)
            return 1

        self.wpl_log_success('successfully replaced the sensor config file')
        return 0


#######################################################################################################################
# Function Name: check_and_terminate_sdk_tool_process
# Date         : 14th May 2020
# Author       : TK NG<tikng@celestica.com>
#
# Procedure Revision Details:
#   Version : 1.0  - Initial Draft  - by TK NG<tikng@celestica.com>
#######################################################################################################################
    def check_and_terminate_sdk_tool_process(self, toolName):
        self.wpl_log_debug('Entering procedure check_and_terminate_sdk_tool_process: %s\n'%(str(locals())))
        output1 = ''
        self.wpl_getPrompt(centos_mode, SDK_TIMEOUT1)

        self.wpl_log_info('***Check for any existing \'%s\' process running in background***' %toolName)
        cmd1 = ('ps -aux | grep \"%s\"' %toolName)
        self.wpl_log_info(cmd1)
        output1 = self.wpl_execute(cmd1, mode=centos_mode, timeout=60)
        self.wpl_log_debug("%s" %output1)
        for line in output1.splitlines():
            line = line.strip()
            if len(line) == 0:
                # blank line
                continue
            else:
                if re.search('grep', line, re.IGNORECASE):
                    continue
                self.wpl_log_debug("[%s]" %line)
                match = re.search(toolName, line, re.IGNORECASE)
                if match:
                    match1 = re.search(r'^root([ \t])+(\d+)([ \t])+((\d+).(\d+))', line, re.IGNORECASE)
                    if match1:
                        self.wpl_log_info('***Found existing \'%s\' process running, terminate the process.***' %toolName)
                        pid = match1.group(2)
                        cmd2 = ('kill -9 %s' %str(pid))
                        self.wpl_log_info(cmd2)
                        self.wpl_transmit(cmd2)
                        time.sleep(3)
                        self.wpl_transmit('\r\n')
                        break

        self.wpl_getPrompt(centos_mode, 60)


#######################################################################################################################
# Function Name: check_background_sdk_tool_process
# Date         : 14th May 2020
# Author       : TK NG<tikng@celestica.com>
#
# Procedure Revision Details:
#   Version : 1.0  - Initial Draft  - by TK NG<tikng@celestica.com>
#######################################################################################################################
    def check_background_sdk_tool_process(self, toolName):
        self.wpl_log_debug('Entering procedure check_background_sdk_tool_process: %s\n'%(str(locals())))
        output1 = ''
        self.wpl_getPrompt(centos_mode, SDK_TIMEOUT1)
        cmd1 = ('ps -aux | grep \"%s\"' %toolName)
        self.wpl_log_info(cmd1)
        time.sleep(5)
        output1 = self.wpl_execute(cmd1, mode=centos_mode, timeout=60)
        self.wpl_log_debug(output1)
        found = False
        for line in output1.splitlines():
            line = line.strip()
            if len(line) == 0:
                # blank line
                continue
            else:
                if re.search('grep', line, re.IGNORECASE):
                    continue
                match = re.search(toolName, line, re.IGNORECASE)
                if match:
                    self.wpl_log_info(line)
                    found = True
                    break

        self.wpl_getPrompt(centos_mode, 60)

        return found


#######################################################################################################################
# Function Name: minipack2_read_diag_bmc_cpld_fpga_bic_fw_versions
# Date         : 14th May 2020
# Author       : TK NG<tikng@celestica.com>
#
# Procedure Revision Details:
#   Version : 1.0  - Initial Draft  - by TK NG<tikng@celestica.com>
#######################################################################################################################
    def minipack2_read_fw_sw_util_versions(self, toolName, optionStr, toolPath, toolName1, optionStr1, toolPath1):
        self.wpl_log_debug('Entering procedure minipack2_read_fw_sw_util_versions with args : %s' %(str(locals())))

        FW_ARRAY = []
        current_bmc_version = '0'
        current_tpm_version = '0'
        current_fcmcpld_B_version = '0'
        current_fcmcpld_T_version = '0'
        current_pwrcpld_L_version = '0'
        current_pwrcpld_R_version = '0'
        current_smbcpld_version = '0'
        current_scmcpld_version = '0'
        current_iob_fpga_version = '0'
        current_fpga1_version = '0'
        current_fpga2_version = '0'
        current_fpga3_version = '0'
        current_fpga4_version = '0'
        current_fpga5_version = '0'
        current_fpga6_version = '0'
        current_fpga7_version = '0'
        current_fpga8_version = '0'
        current_bridge_version = '0'
        current_bridge_bootloader_version = '0'
        current_bios_version = '0'
        current_cpld_version = '0'
        current_me_version = '0'
        current_pvccin_version = '0'
        current_ddrab_version = '0'
        current_p1v05_version = '0'
        current_diag_version = '0'

        cmd = 'cd ' + toolPath
        self.wpl_getPrompt("openbmc", 600)
        self.wpl_transmit(cmd)

        output = self.EXEC_bmc_system_tool_command(toolName, optionStr, toolPath)
        self.wpl_log_debug(output)
        parsedOutput = parserDIAGLibs.MINIPACK2_PARSE_FW_UTIL_Versions(output)

        # BMC
        current_bmc_version = parsedOutput.getValue('BMC_VER')[0]
        if current_bmc_version == 'NA':
            self.wpl_log_fail("Current BMC version not found !")
            self.wpl_raiseException("Failed minipack2_read_fw_sw_util_versions.")
        else:
            if len(current_bmc_version) >= 4:
                if re.search(r'^0\.[\d]+', current_bmc_version):
                    vstr = current_bmc_version
                    vlist = vstr.split('.')
                    if len(vlist) == 2:
                        # e.g. bmc version in ImageInfo.yaml shows 0.3 instead of 0.30
                        # so, remove trailing decimal point zeros from version to match
                        bmc_ver = float(current_bmc_version)
                        current_bmc_version = str(bmc_ver)
            FW_ARRAY.append(current_bmc_version)
            self.wpl_log_success('Found current BMC version: [%s]' %current_bmc_version)

        # TPM
        current_tpm_version = parsedOutput.getValue('TPM_VER')[0]
        if current_tpm_version == 'NA':
            self.wpl_log_fail("Current TPM version not found !")
            self.wpl_raiseException("Failed minipack2_read_fw_sw_util_versions.")
        else:
            FW_ARRAY.append(current_tpm_version)
            self.wpl_log_success('Found current TPM version: [%s]' %current_tpm_version)

        # FCMCPLD_B_VER
        current_fcmcpld_B_version = parsedOutput.getValue('FCMCPLD_B_VER')[0]
        if current_fcmcpld_B_version == 'NA':
            self.wpl_log_fail("Current FCMCPLD_B version not found !")
            self.wpl_raiseException("Failed minipack2_read_fw_sw_util_versions.")
        else:
            FW_ARRAY.append(current_fcmcpld_B_version)
            self.wpl_log_success('Found current FCMCPLD_B version: [%s]' %current_fcmcpld_B_version)

        # FCMCPLD_T_VER
        current_fcmcpld_T_version = parsedOutput.getValue('FCMCPLD_T_VER')[0]
        if current_fcmcpld_T_version == 'NA':
            self.wpl_log_fail("Current FCMCPLD_T version not found !")
            self.wpl_raiseException("Failed minipack2_read_fw_sw_util_versions.")
        else:
            FW_ARRAY.append(current_fcmcpld_T_version)
            self.wpl_log_success('Found current FCMCPLD_T version: [%s]' %current_fcmcpld_T_version)

        # PWRCPLD_L_VER
        current_pwrcpld_L_version = parsedOutput.getValue('PWRCPLD_L_VER')[0]
        if current_pwrcpld_L_version == 'NA':
            self.wpl_log_fail("Current PWRCPLD_L version not found !")
            self.wpl_raiseException("Failed minipack2_read_fw_sw_util_versions.")
        else:
            FW_ARRAY.append(current_pwrcpld_L_version)
            self.wpl_log_success('Found current PWRCPLD_L version: [%s]' %current_pwrcpld_L_version)

        # PWRCPLD_R_VER
        current_pwrcpld_R_version = parsedOutput.getValue('PWRCPLD_R_VER')[0]
        if current_pwrcpld_R_version == 'NA':
            self.wpl_log_fail("Current PWRCPLD_R version not found !")
            self.wpl_raiseException("Failed minipack2_read_fw_sw_util_versions.")
        else:
            FW_ARRAY.append(current_pwrcpld_R_version)
            self.wpl_log_success('Found current PWRCPLD_R version: [%s]' %current_pwrcpld_R_version)

        # SCMCPLD
        current_scmcpld_version = parsedOutput.getValue('SCMCPLD_VER')[0]
        if current_scmcpld_version == 'NA':
            self.wpl_log_fail("Current SCMCPLD version not found !")
            self.wpl_raiseException("Failed minipack2_read_fw_sw_util_versions.")
        else:
            FW_ARRAY.append(current_scmcpld_version)
            self.wpl_log_success('Found current SCMCPLD version: [%s]' %current_scmcpld_version)

        # SMBCPLD
        current_smbcpld_version = parsedOutput.getValue('SMBCPLD_VER')[0]
        if current_smbcpld_version == 'NA':
            self.wpl_log_fail("Current SMBCPLD version not found !")
            self.wpl_raiseException("Failed minipack2_read_fw_sw_util_versions.")
        else:
            FW_ARRAY.append(current_smbcpld_version)
            self.wpl_log_success('Found current SMBCPLD version: [%s]' %current_smbcpld_version)

        # IOB_FPGA
        current_iob_fpga_version = parsedOutput.getValue('IOB_FPGA_VER')[0]
        if current_iob_fpga_version == 'NA':
            self.wpl_log_fail("Current IOB FPGA version not found !")
            self.wpl_raiseException("Failed minipack2_read_fw_sw_util_versions.")
        else:
            FW_ARRAY.append(current_iob_fpga_version)
            self.wpl_log_success('Found current IOB FPGA version: [%s]' %current_iob_fpga_version)

        # PIM1_FPGA
        current_fpga1_version = parsedOutput.getValue('PIM1_FPGA_VER')[0]
        if current_fpga1_version == 'NA':
            self.wpl_log_fail("Current PIM1 FPGA version not found !")
            self.wpl_raiseException("Failed minipack2_read_fw_sw_util_versions.")
        else:
            FW_ARRAY.append(current_fpga1_version)
            self.wpl_log_success('Found current FPGA1 version: [%s]' %current_fpga1_version)

        # PIM2_FPGA
        current_fpga2_version = parsedOutput.getValue('PIM2_FPGA_VER')[0]
        if current_fpga2_version == 'NA':
            self.wpl_log_fail("Current PIM2 FPGA version not found !")
            self.wpl_raiseException("Failed minipack2_read_fw_sw_util_versions.")
        else:
            FW_ARRAY.append(current_fpga2_version)
            self.wpl_log_success('Found current FPGA2 version: [%s]' %current_fpga2_version)

        # PIM3_FPGA
        current_fpga3_version = parsedOutput.getValue('PIM3_FPGA_VER')[0]
        if current_fpga3_version == 'NA':
            self.wpl_log_fail("Current PIM3 FPGA version not found !")
            self.wpl_raiseException("Failed minipack2_read_fw_sw_util_versions.")
        else:
            FW_ARRAY.append(current_fpga3_version)
            self.wpl_log_success('Found current FPGA3 version: [%s]' %current_fpga3_version)

        # PIM4_FPGA
        current_fpga4_version = parsedOutput.getValue('PIM4_FPGA_VER')[0]
        if current_fpga4_version == 'NA':
            self.wpl_log_fail("Current PIM4 FPGA version not found !")
            self.wpl_raiseException("Failed minipack2_read_fw_sw_util_versions.")
        else:
            FW_ARRAY.append(current_fpga4_version)
            self.wpl_log_success('Found current FPGA4 version: [%s]' %current_fpga4_version)

        # PIM5_FPGA
        current_fpga5_version = parsedOutput.getValue('PIM5_FPGA_VER')[0]
        if current_fpga5_version == 'NA':
            self.wpl_log_fail("Current PIM5 FPGA version not found !")
            self.wpl_raiseException("Failed minipack2_read_fw_sw_util_versions.")
        else:
            FW_ARRAY.append(current_fpga5_version)
            self.wpl_log_success('Found current FPGA5 version: [%s]' %current_fpga5_version)

        # PIM6_FPGA
        current_fpga6_version = parsedOutput.getValue('PIM6_FPGA_VER')[0]
        if current_fpga6_version == 'NA':
            self.wpl_log_fail("Current PIM6 FPGA version not found !")
            self.wpl_raiseException("Failed minipack2_read_fw_sw_util_versions.")
        else:
            FW_ARRAY.append(current_fpga6_version)
            self.wpl_log_success('Found current FPGA6 version: [%s]' %current_fpga6_version)

        # PIM7_FPGA
        current_fpga7_version = parsedOutput.getValue('PIM7_FPGA_VER')[0]
        if current_fpga7_version == 'NA':
            self.wpl_log_fail("Current PIM7 FPGA version not found !")
            self.wpl_raiseException("Failed minipack2_read_fw_sw_util_versions.")
        else:
            FW_ARRAY.append(current_fpga7_version)
            self.wpl_log_success('Found current FPGA7 version: [%s]' %current_fpga7_version)

        # PIM8_FPGA
        current_fpga8_version = parsedOutput.getValue('PIM8_FPGA_VER')[0]
        if current_fpga8_version == 'NA':
            self.wpl_log_fail("Current PIM8 FPGA version not found !")
            self.wpl_raiseException("Failed minipack2_read_fw_sw_util_versions.")
        else:
            FW_ARRAY.append(current_fpga8_version)
            self.wpl_log_success('Found current FPGA8 version: [%s]' %current_fpga8_version)

        # BRIDGE IC
        current_bridge_version = parsedOutput.getValue('BRIDGE_VER')[0]
        if current_bridge_version == 'NA':
            self.wpl_log_fail("Current BRIDGE version not found !")
            self.wpl_raiseException("Failed minipack2_read_fw_sw_util_versions.")
        else:
            FW_ARRAY.append(current_bridge_version)
            self.wpl_log_success('Found current BRIDGE version: [%s]' %current_bridge_version)

        # BRIDGE IC BOOTLOADER
        current_bridge_bootloader_version = parsedOutput.getValue('BRIDGE_BOOTLOADER_VER')[0]
        if current_bridge_bootloader_version == 'NA':
            self.wpl_log_fail("Current BRIDGE BOOTLOADER version not found !")
            self.wpl_raiseException("Failed minipack2_read_fw_sw_util_versions.")
        else:
            FW_ARRAY.append(current_bridge_bootloader_version)
            self.wpl_log_success('Found current BRIDGE BOOTLOADER version: [%s]' %current_bridge_bootloader_version)

        # BIOS
        current_bios_version = parsedOutput.getValue('BIOS_VER')[0]
        if current_bios_version == 'NA':
            self.wpl_log_fail("Current BIOS version not found !")
            self.wpl_raiseException("Failed minipack2_read_fw_sw_util_versions.")
        else:
            FW_ARRAY.append(current_bios_version)
            self.wpl_log_success('Found current BIOS version: [%s]' %current_bios_version)

        # CPLD
        current_cpld_version = parsedOutput.getValue('CPLD_VER')[0]
        if current_cpld_version == 'NA':
            self.wpl_log_fail("Current CPLD version not found !")
            self.wpl_raiseException("Failed minipack2_read_fw_sw_util_versions.")
        else:
            FW_ARRAY.append(current_cpld_version)
            self.wpl_log_success('Found current CPLD version: [%s]' %current_cpld_version)

        # ME
        current_me_version = parsedOutput.getValue('ME_VER')[0]
        if current_me_version == 'NA':
            self.wpl_log_fail("Current ME version not found !")
            self.wpl_raiseException("Failed minipack2_read_fw_sw_util_versions.")
        else:
            FW_ARRAY.append(current_me_version)
            self.wpl_log_success('Found current ME version: [%s]' %current_me_version)

        # PVCCIN
        current_pvccin_version = parsedOutput.getValue('PVCCIN_VER')[0]
        if current_pvccin_version == 'NA':
            self.wpl_log_fail("Current PVCCIN version not found !")
            self.wpl_raiseException("Failed minipack2_read_fw_sw_util_versions.")
        else:
            FW_ARRAY.append(current_pvccin_version)
            self.wpl_log_success('Found current PVCCIN version: [%s]' %current_pvccin_version)

        # DDRAB
        current_ddrab_version = parsedOutput.getValue('DDRAB_VER')[0]
        if current_ddrab_version == 'NA':
            self.wpl_log_fail("Current DDRAB version not found !")
            self.wpl_raiseException("Failed minipack2_read_fw_sw_util_versions.")
        else:
            FW_ARRAY.append(current_ddrab_version)
            self.wpl_log_success('Found current DDRAB version: [%s]' %current_ddrab_version)

        # P1V05
        current_p1v05_version = parsedOutput.getValue('P1V05_VER')[0]
        if current_p1v05_version == 'NA':
            self.wpl_log_fail("Current P1V05 version not found !")
            self.wpl_raiseException("Failed minipack2_read_fw_sw_util_versions.")
        else:
            FW_ARRAY.append(current_p1v05_version)
            self.wpl_log_success('Found current P1V05 version: [%s]' %current_p1v05_version)

        # DIAG
        cmd1 = 'cd ' + toolPath1
        self.wpl_getPrompt("openbmc", 600)
        self.wpl_transmit(cmd1)

        output1 = self.EXEC_bmc_system_tool_command(toolName1, optionStr1, toolPath1)
        self.wpl_log_debug(output1)
        found = 0
        p1='Diag[ \t]+version:\s*([\d]+\.[\d]+\.[\d]+)'
        for line in output1.splitlines():
            line = line.strip()

            match1 = re.search(p1, line, re.IGNORECASE)
            if match1:
                found += 1
                current_diag_version = match1.group(1)
                FW_ARRAY.append(current_diag_version)
                self.wpl_log_success('Found current DIAG version: [%s]' %current_diag_version)

        if found == 0:
            self.wpl_log_fail("Current DIAG version not found !")
            self.wpl_raiseException("Failed minipack2_read_fw_sw_util_versions.")

        self.wpl_log_success('Successfully run minipack2_read_fw_sw_util_versions.\n')
        return FW_ARRAY


#######################################################################################################################
# Function Name: get_current_psu_fw_versions
# Date         : 14th May 2020
# Author       : TK NG<tikng@celestica.com>
#
# Procedure Revision Details:
#   Version : 1.0  - Initial Draft  - by TK NG<tikng@celestica.com>
#######################################################################################################################
    def get_current_psu_fw_versions(self, toolName, max_psu, optionStr, toolPath):
        self.wpl_log_debug('Entering procedure get_current_psu_fw_versions with args : %s' % (str(locals())))

        FW_ARRAY = []
        psu_pri_ver = '0'
        psu_sec_ver = '0'
        self.wpl_getPrompt(openbmc_mode)
        cmd = ('cd ' + toolPath)
        self.wpl_transmit(cmd)
        num_psu = max_psu + 1

        # get primary and secondary FW versions
        for i in range(1,num_psu):
            cmd1 = ('%s psu%s %s' %(toolName, str(i), optionStr))
            output1 = self.wpl_execute(cmd1, mode=openbmc_mode, timeout=30)
            pattern1 = (r'PRI_FW_VER[ \t]+\(0xDD\)[ \t]+:[ \t]+([\d]+\.[\d]+)')
            pattern2 = (r'SEC_FW_VER[ \t]+\(0xD7\)[ \t]+:[ \t]+([\d]+\.[\d]+)')
            found1 = False
            found2 = False
            match1 = re.search(pattern1, output1, re.IGNORECASE)
            if match1:
                psu_pri_ver = match1.group(1)
                FW_ARRAY.append(psu_pri_ver)
                self.wpl_log_info("Found currrent PSU%s primary FW version: [%s]" %(str(i), psu_pri_ver))
            else:
                self.wpl_log_fail("Currrent PSU%s primary FW version not found." %(str(i)))
                self.wpl_raiseException("Failed get_current_psu_fw_versions.")

            match2 = re.search(pattern2, output1, re.IGNORECASE)
            if match2:
                psu_sec_ver = match2.group(1)
                FW_ARRAY.append(psu_sec_ver)
                self.wpl_log_info("Found currrent PSU%s secondary FW version: [%s]" %(str(i), psu_sec_ver))
            else:
                self.wpl_log_fail("Currrent PSU%s secondary FW version not found." %(str(i)))
                self.wpl_raiseException("Failed get_current_psu_fw_versions.")

        self.wpl_log_success('Successfully run get_psu_fw_versions.\n')
        return FW_ARRAY


#######################################################################################################################
# Function Name: minipack2_get_TH4_versions
# Date         : 14th May 2020
# Author       : TK NG<tikng@celestica.com>
#
# Procedure Revision Details:
#   Version : 1.0  - Initial Draft  - by TK NG<tikng@celestica.com>
#######################################################################################################################
    def minipack2_get_TH4_versions(self, toolName, toolPath):
        self.wpl_log_debug('Entering procedure minipack2_get_TH4_versions with args : %s' %(str(locals())))

        CommonLib.switch_to_centos()

        CommonLib.change_dir(toolPath)

        # make sure no auto_load_user.py process running in the background
        self.check_and_terminate_sdk_tool_process(toolName)

        # run auto_load_user.sh
        initOption = ''
        status = self.minipack2_sdk_init_check(toolName, initOption, SDK_TIMEOUT1)
        if status == 0:
            self.wpl_log_info('Successfully run auto_load_user.sh')
        else:
            #if status == 1:
            #    self.minipack2_exit_sdk()
            self.wpl_raiseException('Failed minipack2_sdk_init_check.')
        time.sleep(5)

        # issue bsh command
        dsh_cmd = 'dsh'
        pattern_list1 = ['Error', 'sdklt.0>']
        self.wpl_log_info('cmd=[%s]' %dsh_cmd)
        self.wpl_transmit(dsh_cmd)
        output1 = self.wpl_receive(pattern_list1,timeout=SDK_TIMEOUT1)
        time.sleep(3)

        # issue pciephy command
        fwinfo_cmd = 'pciephy fwinfo'
        self.wpl_log_info('cmd=[%s]' %fwinfo_cmd)
        self.wpl_transmit(fwinfo_cmd)
        output2 = self.wpl_receive(pattern_list1,timeout=SDK_TIMEOUT1)
        time.sleep(3)

        pattern1 = (r'PCIe[ \t]+FW[ \t]+loader[ \t]+version:[ \t]+((\d+).(\d+))')
        pattern2 = (r'PCIe[ \t]+FW[ \t]+version:[ \t]+([\w,\d]+)')
        fw_loader_ver = '0'
        fw_ver = '0'
        fw_array = []

        found1 = False
        found2 = False
        for line in output2.splitlines():
            self.wpl_log_info('%s' %line)

            line = line.strip()
            if len(line) == 0:
                # blank line
                continue
            else:
                match1 = re.search(pattern1, line, re.IGNORECASE)
                if match1:
                    fw_loader_ver = match1.group(1)
                    fw_array.append(fw_loader_ver)
                    self.wpl_log_info("Found TH4 PCIe FW loader version: [%s]" %fw_loader_ver)
                    found1 = True

                match2 = re.search(pattern2, line, re.IGNORECASE)
                if match2:
                    fw_ver = match2.group(1)
                    fw_array.append(fw_ver)
                    self.wpl_log_info("Found TH4 PCIe FW version: [%s]" %fw_ver)
                    found2 = True

        # issue exit command twice to exit
        exit_cmd = 'exit'
        self.wpl_log_info('cmd=[%s]' %exit_cmd)
        self.wpl_transmit(exit_cmd)
        pattern_list = MINIPACK2_SDK_WAIT_PATTERN_LIST
        output3 = self.wpl_receive(pattern_list,timeout=SDK_TIMEOUT1)
        time.sleep(3)

        self.wpl_log_info('cmd=[%s]' %exit_cmd)
        self.wpl_transmit(exit_cmd)
        self.wpl_getPrompt("openbmc", SDK_TIMEOUT1)

        if found1 == False:
            self.wpl_log_fail('Error: TH4 PCIe FW Loader version not found.')
            self.wpl_raiseException('Failed minipack2_get_TH4_version')

        if found2 == False:
            self.wpl_log_fail('Error: TH4 PCIe FW version not found.')
            self.wpl_raiseException('Failed minipack2_get_TH4_version')

        self.wpl_log_success("Successfully run minipack2_get_TH4_version.")
        return fw_array


#######################################################################################################################
# Function Name: minipack2_init_and_check_all_eloop_modules
# Date         : 14th May 2020
# Author       : TK NG<tikng@celestica.com>
#
# Procedure Revision Details:
#   Version : 1.0  - Initial Draft  - by TK NG<tikng@celestica.com>
#######################################################################################################################
    def mp2_pim_count(self):
        self.wpl_log_debug('Entering procedure mp2_pim_count with args : %s' % (str(locals())))
        pim_count_na = 0
        CommonLib.switch_to_openbmc()
        cmd = "fpga_ver.sh"
        output = self.wpl_execute(cmd)
        p1 = r'DOMFPGA is not detected'
        for line in output.splitlines():
            mat = re.search(p1, line)
            if mat:
                pim_count_na += 1
        #CommonLib.switch_to_centos()
        cmd = "sol.sh"
        self.wpl_log_info('cmd=[%s]' % cmd)
        self.wpl_transmit(cmd)
        time.sleep(2)
        return pim_count_na

    def minipack2_init_and_check_all_eloop_modules(self, sdkBackTool, initTool, initOption, sdkTool, initToolPath, max_phy_pims, xphy_init_status_list, reInit_SDK=False):
        self.wpl_log_debug('Entering procedure minipack2_init_and_check_all_eloop_modules with args : %s' %(str(locals())))

        # check for TH4 presence
        TH4_Present = self.minipack2CheckTH4Presence()

        if (self.eloop_init == '0') or (reInit_SDK == True):
            if TH4_Present:
                CommonLib.switch_to_centos()

                CommonLib.change_dir(initToolPath)

                # make sure no xphyback process running in the background
                self.check_and_terminate_sdk_tool_process(sdkBackTool)

                # make sure no auto_load_user process running in the background
                self.check_and_terminate_sdk_tool_process(sdkTool)

                # execute sdkBack tool in background
                cmd = ('./' + sdkBackTool + ' &')
                self.wpl_getPrompt("centos", SDK_TIMEOUT1)
                self.wpl_log_info('cmd=[%s]' %cmd)
                self.wpl_transmit(cmd)

                time.sleep(2)

                list_count = len(xphy_init_status_list)

                # execute xphy init tool
                pim_counts = 0
                pim_counts = self.mp2_pim_count()
                pim_limit = max_phy_pims + 1
                for i in range(1,pim_limit):
                    if pim_counts == 3 and ((i == 3) or (i == 4) or (i == 5)):
                        continue
                    if pim_counts == 4 and ((i == 3) or (i == 4) or (i == 5) or (i == 6)):
                        continue
                    cmd = ('./' + initTool + ' ' + initOption.format(i))
                    self.wpl_log_info('cmd=[%s]' %cmd)
                    output = self.wpl_execute(cmd , mode=centos_mode, timeout=300)

                    for pat in xphy_init_status_list:
                        pattern = pat
                        #self.wpl_log_info('search pattern=[%s]' %pattern)
                        found = False
                        for line in output.splitlines():
                            #self.wpl_log_debug('%s' %line)

                            line = line.strip()
                            if len(line) == 0:
                                # blank line
                                continue
                            else:
                                if re.search(pattern, line, re.IGNORECASE):
                                    self.wpl_log_info('found [%s]' %line)
                                    found = True
                                    break

                        if found == False:
                            slist = pattern.split(',')
                            listStr = slist[0]
                            self.wpl_log_fail('Error: xphy init failed for %s' %listStr)
                            self.wpl_raiseException('Failed minipack2_init_and_check_all_eloop_modules')

                    self.wpl_log_info('Successfully xphy init pim%s' %str(i))

                self.eloop_init = '1'
                self.wpl_log_success("Successfully run minipack2_init_and_check_all_eloop_modules.")


#######################################################################################################################
# Function Name: platform_set_port_enable_disable_test_stress_cycles
# Date         : 14th May 2020
# Author       : TK NG<tikng@celestica.com>
#
# Procedure Revision Details:
#   Version : 1.0  - Initial Draft  - by TK NG<tikng@celestica.com>
#######################################################################################################################
    def platform_set_port_enable_disable_test_stress_cycles(self, stressCycles):
        self.wpl_log_debug('Entering procedure platform_set_port_enable_disable_test_stress_cycles with args : %s' %(str(locals())))

        self.port_enable_disable_stress_cycles = str(stressCycles)

        self.wpl_log_success('Successfully platform_set_port_enable_disable_test_stress_cycles: [%s] cycles.\n' %(str(stressCycles)))


#######################################################################################################################
# Function Name: platform_set_port_enable_disable_test_stress_time
# Date         : 14th May 2020
# Author       : TK NG<tikng@celestica.com>
#
# Procedure Revision Details:
#   Version : 1.0  - Initial Draft  - by TK NG<tikng@celestica.com>
#######################################################################################################################
    def platform_set_port_enable_disable_test_stress_time(self, stressTime):
        self.wpl_log_debug('Entering procedure platform_set_port_enable_disable_test_stress_time with args : %s' %(str(locals())))

        self.port_enable_disable_stress_time = str(stressTime)

        self.wpl_log_success('Successfully platform_set_port_enable_disable_test_stress_time: [%s] seconds.\n' %(str(stressTime)))


#######################################################################################################################
# Function Name: minipack2_perform_port_enable_disable_stress_test
# Date         : 14th May 2020
# Author       : TK NG<tikng@celestica.com>
#
# Procedure Revision Details:
#   Version : 1.0  - Initial Draft  - by TK NG<tikng@celestica.com>
#######################################################################################################################
    def minipack2_perform_port_enable_disable_stress_test(self, AllPort, initTool, initToolPath, bcm_set_vlan_cmd, bcm_cpu_start_traffic_cmd, stressCycles, runTime, bcm_cpu_stop_traffic_cmd, pattern1, portStatusCmd, setPortCmd, portEnableOption, portDisableOption):
        self.wpl_log_debug('Entering procedure minipack2_perform_port_enable_disable_stress_test with args : %s' %(str(locals())))

        pim_counts = 0
        pim_counts = self.mp2_pim_count()

        CommonLib.switch_to_centos()
        CommonLib.change_dir(initToolPath)

        # make sure no auto_load_user.py process running in the background
        self.check_and_terminate_sdk_tool_process(initTool)

        # run auto_load_user.sh
        initOption = ''
        status = self.minipack2_sdk_init_check(initTool, initOption, SDK_TIMEOUT1)
        if status == 0:
            self.wpl_log_info('Successfully run auto_load_user.sh')
        else:
            if status == 1:
                self.minipack2_exit_sdk()
            self.wpl_raiseException('Failed minipack2_perform_port_enable_disable_stress_test.')

        time.sleep(5)

        # execute 'ps' command and check ports status
        # mp2 dc unit set lb mac for no loopback
        self.wpl_log_info('***setting lb mac about not pluging the loopback***')
        devicename = os.environ.get("deviceName", "")
        if 'minipack2_dc' in devicename.lower():
            status = self.mp2_lb_mac_set(pim_counts)
            if status == 0:
                self.wpl_log_info('Successfully set mp2 dc lb mac')
            else:
                self.wpl_log_fail('Error running set mp2 dc lb mac.')
                # if status == 1:
                # self.minipack2_exit_sdk()
                return 1
            time.sleep(5)
        self.wpl_log_info('***checking all ports status***')
        status = self.minipack2_check_port_status('ps cd', 'up', 'enable')
        if status == 0:
            self.wpl_log_info('All ports status are up.')
        else:
            self.minipack2_exit_sdk()
            self.wpl_raiseException('Failed minipack2_perform_port_enable_disable_stress_test.')

        time.sleep(1)

        #pattern1 = r'ena\/([ \t])+speed\/([ \t])+link([ \t])+auto([ \t])+STP([ \t])+lrn([ \t])+max([ \t])+cut([ \t])+loop'
        #pattern2 = r'port([ \t])+link([ \t])+Lns([ \t])+duplex([ \t])+scan([ \t])+neg\?([ \t])+state([ \t])+pause([ \t])+discrd([ \t])+ops([ \t])+medium([ \t])+frame([ \t])+thru([ \t])+FEC([ \t])+back'

        found = False
        max_cycles = int(stressCycles)
        for i in range(0, max_cycles):
            self.wpl_log_info('************************************************************')
            self.wpl_log_info('*** Test Repeat Loop #: %s / %s ***' %((i+1), str(max_cycles)))
            self.wpl_log_info('************************************************************')

            # disable port
            self.minipack2_disable_each_port(AllPort, setPortCmd, portDisableOption, SDK_TIMEOUT1)

            time.sleep(3)

            status = self.minipack2_check_port_status(portStatusCmd, '!ena', 'disable')
            if status == 0:
                self.wpl_log_info('Successfully disabled all ports')
            else:
                self.wpl_raiseException('Failed minipack2_perform_port_enable_disable_stress_test')

            # enable port
            self.minipack2_enable_each_port(AllPort, setPortCmd, portEnableOption, SDK_TIMEOUT1)

            time.sleep(8)

            status = self.minipack2_check_port_status(portStatusCmd, 'up', 'enable')
            if status == 0:
                self.wpl_log_info('Successfully enabled all ports')
            else:
                self.wpl_raiseException('Failed minipack2_perform_port_enable_disable_stress_test')

            result = self.minipack2_perform_cpu_traffic_check(initTool, initOption, initToolPath, bcm_set_vlan_cmd, bcm_cpu_start_traffic_cmd, runTime, bcm_cpu_stop_traffic_cmd, pattern1)
            if result:
                self.wpl_raiseException('Failed minipack2_perform_port_enable_disable_stress_test')

        # exit BCM>
        self.minipack2_exit_sdk()

        self.wpl_log_success('Successfully run minipack2_perform_port_enable_disable_stress_test.\n')


#######################################################################################################################
# Function Name: minipack2_check_port_status
# Date         : 14th May 2020
# Author       : TK NG<tikng@celestica.com>
#
# Procedure Revision Details:
#   Version : 1.0  - Initial Draft  - by TK NG<tikng@celestica.com>
#######################################################################################################################
    def minipack2_check_port_status(self, portStatusCmd, pattern, message):
        self.wpl_log_debug('Entering procedure minipack2_check_port_status with args : %s' %(str(locals())))

        pattern_list = ['Error', MINIPACK2_SDK_PROMPT]

        # port status
        cmd = portStatusCmd
        self.wpl_log_info('cmd=[%s]' %cmd)
        self.wpl_transmit(cmd)
        output = self.wpl_receive(pattern_list,timeout=SDK_TIMEOUT1)
        #self.wpl_log_debug('output=[%s]' %output)
        time.sleep(1)

        self.wpl_log_info("Checking \'%s\' output..." %(cmd))
        port_count = 0

        for line in output.splitlines():
            match1 = re.search('error|fail', line, re.IGNORECASE)
            if match1:
                self.wpl_log_fail('Failed to %s port: \'%s\'' %(message, line))
                return 1

            line = line.strip()
            if len(line) == 0:
                # blank line
                continue
            else:
                match2 = re.search(r'cd(\d+)', line, re.IGNORECASE)
                if match2:
                    match3 = re.search(pattern, line, re.IGNORECASE)
                    if match3:
                        port_count += 1
                        continue
                    else:
                        self.wpl_log_fail('Failed to %s port: \'%s\'' %(message, line))
                        return 2

        if port_count != 128:
            self.wpl_log_fail('Error: Only %s number of ports counter information found ! Expected 128 ports status information.' %(str(port_count)))
            return 3

        self.wpl_log_info("Checked \'%s\' output status: PASSED" %(cmd))
        return 0


#######################################################################################################################
# Function Name: minipack2_perform_eeprom_stress_test
# Date         : 14th May 2020
# Author       : TK NG<tikng@celestica.com>
#
# Procedure Revision Details:
#   Version : 1.0  - Initial Draft  - by TK NG<tikng@celestica.com>
#######################################################################################################################
    def minipack2_perform_eeprom_access_stress_test(self, initTool, initOption, initToolPath, resetTool, resetOption1, resetOption2, resetToolPath, toolName, optionStr, runTime, toolPath, patternList1, patternList2, patternList3, start_pattern_list):
        self.wpl_log_debug('Entering procedure minipack2_perform_eeprom_access_stress_test with args : %s' %(str(locals())))

        CommonLib.switch_to_centos()

        CommonLib.change_dir(initToolPath)

        # check for TH4 presence
        TH4_Present = self.minipack2CheckTH4Presence()

        if TH4_Present:
            # make sure no auto_load_user.py process running in the background
            self.check_and_terminate_sdk_tool_process(initTool)

            # run auto_load_user.sh
            status = self.minipack2_sdk_init_check(initTool, initOption, SDK_TIMEOUT2)
            if status == 0:
                self.wpl_log_info('Successfully run auto_load_user.sh')
            else:
                if status == 1:
                    self.minipack2_exit_sdk()
                self.wpl_log_fail('Error running auto_load_user.sh script.')
                self.wpl_raiseException('Failed minipack2_perform_eeprom_access_stress_test.')
            time.sleep(5)

            # exit BCM>
            self.minipack2_exit_sdk()

            cmd = 'cd ' + resetToolPath
            self.wpl_getPrompt("centos", SDK_TIMEOUT1)
            self.wpl_log_info('cmd=[%s]' %cmd)
            self.wpl_transmit(cmd)

            time.sleep(2)

            # reset on
            #cmd = './' + resetTool + ' ' + resetOption1
            #self.wpl_log_info('cmd=[%s]' %cmd)
            #self.wpl_execute(cmd, 'centos', 300)

            #time.sleep(2)

            # reset off
            cmd = './' + resetTool + ' ' + resetOption2
            self.wpl_log_info('cmd=[%s]' %cmd)
            self.wpl_execute(cmd, 'centos', SDK_TIMEOUT1)

            time.sleep(2)

        cmd = 'cd ' + toolPath
        self.wpl_getPrompt("centos", SDK_TIMEOUT1)
        self.wpl_log_info('cmd=[%s]' %cmd)
        self.wpl_transmit(cmd)

        complete_flag = False
        found = False
        #t1 = time.time()
        while complete_flag == False:
            time.sleep(1)

            # execute temp_volt_limit command
            cmd = './' + toolName + ' ' + optionStr
            self.wpl_log_info('cmd=[%s]' %cmd)
            output = self.wpl_execute(cmd, 'centos', 1200)
            self.wpl_log_debug('output=[%s]' %output)

            result = re.search('eeprom information', output, re.IGNORECASE)
            if result is None:
                self.wpl_log_fail('Error: No module present')
                self.wpl_raiseException('Failed minipack2_perform_eeprom_access_stress_test')

            # fix output not on same line
            start_section = 0
            end_section = 0
            blank_count = 0
            previous_line = ''
            output1 = ''
            for line in output.splitlines():
                match = re.search(r'^Pim([ \t])+#(\d+)([ \t])+Port([ \t])+#(\d+)', line, re.IGNORECASE)
                if match:
                    start_section = 1

                match1 = re.search(r'^m(\d+)([ \t])+p(\d+)#', line, re.IGNORECASE)
                if match1:
                    end_section = 1

                line = line.lstrip()
                line = line.rstrip('\r\n')
                if len(line) == 0:
                    if (start_section == 1) and (end_section == 0):
                        # blank line
                        blank_count = blank_count + 1
                    continue
                else:
                    # if within the section
                    if (start_section == 1) and (end_section == 0):
                        if blank_count:
                            if self.eeprom_output_is_start_line(line, start_pattern_list):
                                previous_line = line
                                blank_count = 0
                            else:
                                previous_line = previous_line + line
                                output1 = (output1 + previous_line + '\r\n')
                                previous_line = ''
                                blank_count = 0
                        else:
                            if len(previous_line) != 0:
                                output1 = (output1 + previous_line + '\r\n')
                            previous_line = line
                    else:
                        if len(previous_line) != 0:
                            output1 = (output1 + previous_line + '\r\n')
                        previous_line = line
                        start_section = 0
                        end_section = 0
                        blank_count = 0

            if len(previous_line) != 0:
                output1 = (output1 + previous_line + '\r\n')

            output = output1
            #self.wpl_log_debug('new output[%s]' %output)

            self.wpl_log_info("Checking \'%s\' output..." %(toolName))

            for line in output.splitlines():
                self.wpl_log_info('%s' %line)

                match = re.search('root@', line, re.IGNORECASE)
                if match:
                    continue

                line = line.strip()
                if len(line) == 0:
                    # blank line
                    continue
                else:
                    match2 = re.search('No module present', line, re.IGNORECASE)
                    if match2:
                        self.wpl_log_fail('Error: No module present')
                        self.wpl_raiseException('Failed minipack2_perform_eeprom_access_stress_test')

                    match3 = re.search('Module EEPROM Access failed', line, re.IGNORECASE)
                    if match3:
                       self.wpl_log_fail('[%s] command failed.' %toolName)
                       self.wpl_raiseException('Failed minipack2_perform_eeprom_access_stress_test')

                    match4 = re.search('error|fail', line, re.IGNORECASE)
                    if match4:
                        self.wpl_log_fail('Error|Fail message found in \"%s\" command output: [%s]' %(toolName, line))
                        self.wpl_raiseException('Failed minipack2_perform_eeprom_access_stress_test')

                    found = False
                    for i in patternList1:
                        match1 = re.search(i, line, re.IGNORECASE)
                        if match1:
                            found = True
                            break
                    if found:
                        continue
                    else:
                        for i in patternList2:
                            match1 = re.search(i, line, re.IGNORECASE)
                            if match1:
                                found = True
                                break
                        if found:
                            continue
                        else:
                            for i in patternList3:
                                match1 = re.search(i, line, re.IGNORECASE)
                                if match1:
                                    found = True
                                    break
                            if found:
                                continue
                            else:
                                self.wpl_log_fail('Error: Unrecognized output[%s]\r\n' %line)
                                self.wpl_raiseException('Failed minipack2_perform_eeprom_access_stress_test')

            self.wpl_log_success('Checked \'%s\' output OK.' %(toolName))

            # only need to run for 1 cycle
            complete_flag = True

            #t2 = time.time()
            #time_diff = int(t2 - t1)
            #if time_diff > int(runTime):
            #    complete_flag = True
            #    break

        self.wpl_log_success("Successfully run minipack2_perform_eeprom_access_stress_test using \'%s\' tool. PASSED." %toolName)


#######################################################################################################################
# Function Name: vlan_check_output
# Date         : 14th May 2020
# Author       : TK NG<tikng@celestica.com>
#
# Procedure Revision Details:
#   Version : 1.0  - Initial Draft  - by TK NG<tikng@celestica.com>
#######################################################################################################################
    def vlan_check_output(self, cmd, output, pattern1, pattern2='None', pattern3='None', pattern4='None'):
        self.wpl_log_debug('Entering procedure vlan_check_output: %s\n'%(str(locals())))

        sdk_console = MINIPACK2_SDK_PROMPT

        for line in output.splitlines():
            self.wpl_log_info('%s' %line)

            match = re.search(sdk_console, line, re.IGNORECASE)
            if match:
                continue

            match1 = re.search(cmd, line, re.IGNORECASE)
            if match1:
                continue

            line = line.strip()
            if len(line) == 0:
                # blank line
                continue
            else:
                match2 = re.search('error', line, re.IGNORECASE)
                if match2:
                    self.wpl_log_fail('Error message found in \"%s\" command output: [%s]' %(bcm_set_vlan_cmd, line))
                    return 1

                match3 = re.search('fail', line, re.IGNORECASE)
                if match3:
                    self.wpl_log_fail('Fail message found in \"%s\" command output: [%s]' %(bcm_set_vlan_cmd, line))
                    return 1

                match4 = re.search(pattern1, line, re.IGNORECASE)
                if match4:
                    continue
                else:
                    if pattern2 != 'None':
                        match5 = re.search(pattern2, line, re.IGNORECASE)
                        if match5:
                            continue

                    if pattern3 != 'None':
                        match6 = re.search(pattern3, line, re.IGNORECASE)
                        if match6:
                            continue

                    if pattern3 != 'None':
                        match7 = re.search(pattern4, line, re.IGNORECASE)
                        if match7:
                            continue

                    self.wpl_log_fail('Error: Unrecognized output in \"%s\" command: [%s]' %(cmd, line))
                    return 1

        return 0


#######################################################################################################################
# Function Name: minipack2_perform_snake_traffic_stress_test
# Date         : 14th May 2020
# Author       : TK NG<tikng@celestica.com>
#
# Procedure Revision Details:
#   Version : 1.0  - Initial Draft  - by TK NG<tikng@celestica.com>
#######################################################################################################################
    def minipack2_perform_snake_traffic_stress_test(self, initTool, initOption, initToolPath, bcm_set_vlan_cmd, bcm_cpu_start_traffic_cmd, runTime, bcm_cpu_stop_traffic_cmd, pattern1):
        self.wpl_log_debug('Entering procedure minipack2_perform_snake_traffic_stress_test with args : %s' %(str(locals())))

        result = self.minipack2_start_cpu_traffic_stress_test(initTool, initOption, initToolPath, bcm_set_vlan_cmd, bcm_cpu_start_traffic_cmd, runTime, pattern1)
        if result:
            self.wpl_raiseException('Failed minipack2_perform_snake_traffic_stress_test')

        result2 = self.minipack2_stop_cpu_traffic_stress_test(bcm_cpu_stop_traffic_cmd)
        if result2:
            self.wpl_log_fail('Error stopping cpu traffic.')
            self.wpl_raiseException('Failed minipack2_perform_snake_traffic_stress_test')

        result1 = self.minipack2_cpu_traffic_check_port_counters()

        self.minipack2_exit_sdk()

        if result1:
            self.wpl_raiseException('Failed minipack2_perform_snake_traffic_stress_test')

        self.wpl_log_success("Successfully run minipack2_perform_snake_traffic_stress_test for %s seconds. PASSED." %runTime)


#######################################################################################################################
# Function Name: minipack2_start_cpu_traffic_stress_test
# Date         : 14th May 2020
# Author       : TK NG<tikng@celestica.com>
#
# Procedure Revision Details:
#   Version : 1.0  - Initial Draft  - by TK NG<tikng@celestica.com>
#######################################################################################################################
    def minipack2_start_cpu_traffic_stress_test(self, initTool, initOption, initToolPath, bcm_set_vlan_cmd, bcm_cpu_start_traffic_cmd, runTime, pattern1):
        self.wpl_log_debug('Entering procedure minipack2_start_cpu_traffic_stress_test with args : %s' %(str(locals())))

        pim_counts = 0
        pim_counts = self.mp2_pim_count()

        CommonLib.switch_to_centos()
        CommonLib.change_dir(initToolPath)

        # make sure no auto_load_user.py process running in the background
        self.check_and_terminate_sdk_tool_process(initTool)

        # run auto_load_user.sh
        status = self.minipack2_sdk_init_check(initTool, initOption, SDK_TIMEOUT2)
        if status == 0:
            self.wpl_log_info('Successfully run auto_load_user.sh')
        else:
            self.wpl_log_fail('Error running auto_load_user.sh script.')
            #if status == 1:
                #self.minipack2_exit_sdk()
            return 1

        time.sleep(5)

        # mp2 dc unit set lb mac for no loopback
        devicename = os.environ.get("deviceName", "")
        if 'minipack2_dc' in devicename.lower():
            status = self.mp2_lb_mac_set(pim_counts)
            if status == 0:
                self.wpl_log_info('Successfully set mp2 dc lb mac')
            else:
                self.wpl_log_fail('Error running set mp2 dc lb mac.')
                # if status == 1:
                # self.minipack2_exit_sdk()
                return 1
            time.sleep(5)

        # execute linespeed200G.soc command
        status = self.minipack2_run_linespeed(bcm_set_vlan_cmd, pattern1, SDK_TIMEOUT1)
        if status == 0:
            self.wpl_log_info('Successfully run linespeed200G.soc command.')
        else:
            self.wpl_log_fail('Failed linespeed200G.soc command.')
            #self.minipack2_exit_sdk()
            return 1

        time.sleep(1)

        # execute 'pvlan show' command
        status = self.minipack2_run_pvlan_show(SDK_TIMEOUT1)
        if status == 0:
            self.wpl_log_info('Successfully run pvlan show command.')
        else:
            self.wpl_log_info('Failed pvlan show command.')
            #self.minipack2_exit_sdk()
            return 1

        time.sleep(1)

        # execute 'vlan show'
        status = self.minipack2_run_vlan_show(SDK_TIMEOUT1)
        if status == 0:
            self.wpl_log_info('Successfully run vlan show command.')
        else:
            self.wpl_log_info('Failed vlan show command.')
            #self.minipack2_exit_sdk()
            return 1

        time.sleep(3)

        # execute 'ps' command
        status = self.minipack2_check_port_status('ps', 'up', 'enable')
        if status == 0:
            self.wpl_log_info('All ports link status are up')
        else:
            self.wpl_log_info('Failed minipack2_check_port_status.')
            #self.minipack2_exit_sdk()
            return 1

        time.sleep(1)

        # clear counters
        status = self.minipack2_clear_port_counters(SDK_TIMEOUT1)
        if status == 0:
            self.wpl_log_info('Successfully cleared port counters.')
        else:
            self.wpl_log_fail('Error clearing port counters.')
            #self.minipack2_exit_sdk()
            return 1

        time.sleep(1)

        # show counters
        status = self.minipack2_show_port_counters(SDK_TIMEOUT1)
        if status == 0:
            self.wpl_log_info('Successfully cleared port counters.')
        else:
            self.wpl_log_fail('Error showing port counters.')
            #self.minipack2_exit_sdk()
            return 1

        time.sleep(1)

        # start cpu traffic
        status = self.minipack2_start_cpu_traffic(bcm_cpu_start_traffic_cmd, SDK_TIMEOUT1)
        if status == 0:
            self.wpl_log_info('Successfully started cpu traffic.')
        else:
            self.wpl_log_fail('Error starting cpu traffic.')
            #self.minipack2_exit_sdk()
            return 1

        time.sleep(1)

        if int(runTime) != 0:
            # sleep for runTime second
            status = self.minipack2_sleep_and_wait(runTime)
            if status == 0:
                self.wpl_log_info('Successfully run minipack2_start_cpu_traffic_stress_test.')
            else:
                self.wpl_log_fail('Error sleeping for %s seconds.' %(str(runTime)))
                #self.minipack2_exit_sdk()
                return 1

        return 0


#######################################################################################################################
# Function Name: minipack2_stop_cpu_traffic_stress_test
# Date         : 14th May 2020
# Author       : TK NG<tikng@celestica.com>
#
# Procedure Revision Details:
#   Version : 1.0  - Initial Draft  - by TK NG<tikng@celestica.com>
#######################################################################################################################
    def minipack2_stop_cpu_traffic_stress_test(self, bcm_cpu_stop_traffic_cmd):
        self.wpl_log_debug('Entering procedure minipack2_stop_cpu_traffic_stress_test with args : %s' %(str(locals())))

        # stop cpu traffic
        self.wpl_log_info('***stop cpu traffic test***')
        cmd = bcm_cpu_stop_traffic_cmd
        self.wpl_log_info('cmd=[%s]' %cmd)
        self.wpl_transmit(cmd)
        pattern_list = MINIPACK2_SDK_WAIT_PATTERN_LIST
        output = self.wpl_receive(pattern_list,timeout=SDK_TIMEOUT1)
        self.wpl_log_debug('output=[%s]' %output)
        time.sleep(1)
        if re.search('Error|Fail', output, re.IGNORECASE):
            self.wpl_log_fail('Error stopping cpu traffic test.')
            return 1
        else:
            return 0


#######################################################################################################################
# Function Name: minipack2_cpu_traffic_show_counter
# Date         : 14th May 2020
# Author       : TK NG<tikng@celestica.com>
#
# Procedure Revision Details:
#   Version : 1.0  - Initial Draft  - by TK NG<tikng@celestica.com>
#######################################################################################################################
    def minipack2_cpu_traffic_show_counter(self):
        self.wpl_log_debug('Entering procedure minipack2_cpu_traffic_show_counter with args : %s' %(str(locals())))

        # show counters
        self.wpl_log_info('***show cpu traffic counters***')
        cmd = 'show c'
        self.wpl_log_info('cmd=[%s]' %cmd)
        self.wpl_transmit(cmd)
        sdk_console = MINIPACK2_SDK_PROMPT
        pattern_list = MINIPACK2_SDK_WAIT_PATTERN_LIST
        output7 = self.wpl_receive(pattern_list,timeout=SDK_TIMEOUT1)
        self.wpl_log_debug('output=[%s]' %output7)

        # e.g. XLMIB_TBYT.cd0                        :        97,715,478,260     +97,715,478,260
        var_pattern4 = "([\w,\_,\d]+)\.cd([\d]+)[ \t]+:[ \t]+([\,,\d]+)[ \t]+\+([\,,\d]+)"
        for line in output7.splitlines():
            #self.wpl_log_debug('%s' %line)
            match = re.search(sdk_console, line, re.IGNORECASE)
            if match:
                continue

            line = line.strip()
            if len(line) == 0:
                # blank line
                continue
            else:
                match = re.search(var_pattern4, line, re.IGNORECASE)
                if match:
                    counter1 = match.group(3)
                    counter2 = match.group(4)
                    if counter1 == counter2:
                        self.wpl_log_info('Tx counter[%s] and Rx counter[%s] matched. PASSED.' %(counter1, counter2))
                        return 0
                    else:
                        self.wpl_log_fail('Tx counter[%s] and Rx counter[%s] does not match.' %(counter1, counter2))
                        return 1


#######################################################################################################################
# Function Name: minipack2_cpu_traffic_check_port_counters
# Date         : 14th May 2020
# Author       : TK NG<tikng@celestica.com>
#
# Procedure Revision Details:
#   Version : 1.0  - Initial Draft  - by TK NG<tikng@celestica.com>
#######################################################################################################################
    def minipack2_cpu_traffic_check_port_counters(self):
        self.wpl_log_debug('Entering procedure minipack2_cpu_traffic_check_port_counters with args : %s' %(str(locals())))

        # dump counters for all ports
        self.wpl_log_info('***check all port counters***')
        cmd = 'portdump counters all'
        self.wpl_log_info('cmd=[%s]' %cmd)
        self.wpl_transmit(cmd)
        sdk_console = MINIPACK2_SDK_PROMPT
        pattern_list = MINIPACK2_SDK_WAIT_PATTERN_LIST
        output = self.wpl_receive(pattern_list,timeout=SDK_TIMEOUT1)
        self.wpl_log_debug('output=[%s]' %output)

        #e.g. Port128  couters (tx=121005984, rx=121005984)         passed
        var_pattern = r'Port([\d]+)[ \t]+couters[ \t]+\(tx=([\d]+)\,[ \t]+rx=([\d]+)\)[ \t]+passed'
        port_count = 0
        for line in output.splitlines():
            #self.wpl_log_debug('%s' %line)
            match = re.search(sdk_console, line, re.IGNORECASE)
            if match:
                continue

            line = line.strip()
            if len(line) == 0:
                # blank line
                continue
            else:
                match = re.search(var_pattern, line, re.IGNORECASE)
                if match:
                    counter1 = match.group(2)
                    counter2 = match.group(3)
                    if counter1 == counter2:
                        port_count += 1
                        self.wpl_log_info('%s: Tx counter[%s] and Rx counter[%s] matched.' %(line, counter1, counter2))
                    else:
                        self.wpl_log_info('Tx counter[%s] and Rx counter[%s] does not match.' %(counter1, counter2))
                        self.wpl_log_fail('%s: FAILED' %line)
                        return 1

        if port_count != 128:
            self.wpl_log_fail('Error: Only %s number of ports counter information found ! Expected 128 ports counter information.' %(str(port_count)))
            return 1

        self.wpl_log_info('All Tx counters and Rx counters matched. PASSED.')
        return 0


#######################################################################################################################
# Function Name: minipack2_sdk_init_check
# Date         : 14th May 2020
# Author       : TK NG<tikng@celestica.com>
#
# Procedure Revision Details:
#   Version : 1.0  - Initial Draft  - by TK NG<tikng@celestica.com>
#######################################################################################################################
    def mp2_lb_mac_set(self, pim_counts):
        if pim_counts == 4:
            cmd = lb_mac_pimNum4_200G_200G
            #self.device.sendMsg(cmd + '\n')
            self.wpl_log_info('cmd=[%s]' % cmd)
            self.wpl_transmit(cmd)
            output = self.wpl_receive(MINIPACK2_SDK_PROMPT, timeout=SDK_TIMEOUT1)
            time.sleep(2)
        elif pim_counts == 3:
            cmd = lb_mac_pimNum5_200G_200G
            self.wpl_log_info('cmd=[%s]' % cmd)
            self.wpl_transmit(cmd)
            output = self.wpl_receive(MINIPACK2_SDK_PROMPT, timeout=SDK_TIMEOUT1)
            time.sleep(2)
        if re.search('Error', output, re.IGNORECASE):
            self.wpl_log_fail('Failed mp2_lb_mac_set: [Error] message found.')
            return 1
        else:
            return 0

    def minipack2_sdk_init_check(self, initTool, initOption, sdkTimeout):
        self.wpl_log_debug('Entering procedure minipack2_sdk_init_check with args : %s' %(str(locals())))

        # run auto_load_user.sh
        self.wpl_log_info('***running auto_load_user.sh***')
        cmd = './' + initTool + ' ' + initOption
        self.wpl_log_info('cmd=[%s]' %cmd)
        self.wpl_transmit(cmd)
        pattern_list = MINIPACK2_SDK_WAIT_PATTERN_LIST1
        output = self.wpl_receive(pattern_list, timeout=sdkTimeout)
        self.wpl_log_info('output=[%s]' %output)
        if re.search('Error', output, re.IGNORECASE):
            self.wpl_log_fail('Failed minipack2_sdk_init_check: [Error] message found.')
            return 1
        elif re.search(MINIPACK2_SDK_PROMPT_NOTH4, output):
            self.wpl_log_info('in MINIPACK2_SDK_PROMPT_NOTH4')

            self.wpl_transmit('exit')
            return 3
        else:
            if re.search(NO_SUCH_FILE_STR, output, re.IGNORECASE):
                self.wpl_log_fail('Failed minipack2_sdk_init_check: [%s].' %NO_SUCH_FILE_STR)
                return 2
            else:
                # success
                return 0


#######################################################################################################################
# Function Name: minipack2_exit_sdk
# Date         : 14th May 2020
# Author       : TK NG<tikng@celestica.com>
#
# Procedure Revision Details:
#   Version : 1.0  - Initial Draft  - by TK NG<tikng@celestica.com>
#######################################################################################################################
    def minipack2_exit_sdk(self):
        self.wpl_log_debug('Entering procedure minipack2_exit_sdk with args : %s' %(str(locals())))

        # exit BCM>
        self.wpl_log_info('***exit SDK***')
        cmd = 'exit'
        self.wpl_log_info('cmd=[%s]' %cmd)
        self.wpl_transmit(cmd)
        self.wpl_flush()
        self.wpl_getPrompt(centos_mode, 60)


#######################################################################################################################
# Function Name: minipack2_run_linespeed
# Date         : 14th May 2020
# Author       : TK NG<tikng@celestica.com>
#
# Procedure Revision Details:
#   Version : 1.0  - Initial Draft  - by TK NG<tikng@celestica.com>
#######################################################################################################################
    def minipack2_run_linespeed(self, bcm_set_vlan_cmd, vlan_pattern, sdkTimeout):
        self.wpl_log_debug('Entering procedure minipack2_run_linespeed with args : %s' %(str(locals())))

        # execute linespeed200G.soc command
        self.wpl_log_info('***running linespeed200G.soc***')
        cmd = bcm_set_vlan_cmd
        self.wpl_log_info('cmd=[%s]' %cmd)
        self.wpl_transmit(cmd)
        pattern_list = MINIPACK2_SDK_WAIT_PATTERN_LIST
        output = self.wpl_receive(pattern_list, timeout=sdkTimeout)
        self.wpl_log_info('output=[%s]' %output)
        result = self.vlan_check_output(cmd, output, vlan_pattern, 'None', 'None', 'None')
        if result:
            self.wpl_log_fail('Failed minipack2_run_linespeed.')
            return 1
        else:
            # success
            return 0


#######################################################################################################################
# Function Name: minipack2_clear_port_counters
# Date         : 14th May 2020
# Author       : TK NG<tikng@celestica.com>
#
# Procedure Revision Details:
#   Version : 1.0  - Initial Draft  - by TK NG<tikng@celestica.com>
#######################################################################################################################
    def minipack2_clear_port_counters(self, sdkTimeout):
        self.wpl_log_debug('Entering procedure minipack2_clear_port_counters with args : %s' %(str(locals())))

        # clear counters
        self.wpl_log_info('***clear counter***')
        cmd = 'clear c'
        self.wpl_log_info('cmd=[%s]' %cmd)
        self.wpl_transmit(cmd)
        pattern_list = MINIPACK2_SDK_WAIT_PATTERN_LIST
        output = self.wpl_receive(pattern_list,timeout=sdkTimeout)
        self.wpl_log_info('output=[%s]' %output)
        if re.search('Error|Fail', output, re.IGNORECASE):
            self.wpl_log_fail('Failed minipack2_clear_port_counters: [Error/Fail] message found.')
            return 1
        else:
            # success
            return 0


#######################################################################################################################
# Function Name: minipack2_show_port_counters
# Date         : 14th May 2020
# Author       : TK NG<tikng@celestica.com>
#
# Procedure Revision Details:
#   Version : 1.0  - Initial Draft  - by TK NG<tikng@celestica.com>
#######################################################################################################################
    def minipack2_show_port_counters(self, sdkTimeout):
        self.wpl_log_debug('Entering procedure minipack2_show_port_counters with args : %s' %(str(locals())))

        # show counters
        self.wpl_log_info('***show counters***')
        cmd = 'show c'
        self.wpl_log_info('cmd=[%s]' %cmd)
        self.wpl_transmit(cmd)
        pattern_list = MINIPACK2_SDK_WAIT_PATTERN_LIST
        output = self.wpl_receive(pattern_list,timeout=sdkTimeout)
        self.wpl_log_info('output=[%s]' %output)
        if re.search('Error|Fail', output, re.IGNORECASE):
            self.wpl_log_fail('Failed minipack2_show_port_counters: [Error/Fail] message found.')
            return 1
        else:
            # success
            return 0


#######################################################################################################################
# Function Name: minipack2_start_cpu_traffic
# Date         : 14th May 2020
# Author       : TK NG<tikng@celestica.com>
#
# Procedure Revision Details:
#   Version : 1.0  - Initial Draft  - by TK NG<tikng@celestica.com>
#######################################################################################################################
    def minipack2_start_cpu_traffic(self, bcm_cpu_start_traffic_cmd, sdkTimeout):
        self.wpl_log_debug('Entering procedure minipack2_start_cpu_traffic with args : %s' %(str(locals())))

        # start cpu traffic
        self.wpl_log_info('***start cpu traffic***')
        cmd = bcm_cpu_start_traffic_cmd
        self.wpl_log_info('cmd=[%s]' %cmd)
        self.wpl_transmit(cmd)
        pattern_list = MINIPACK2_SDK_WAIT_PATTERN_LIST
        output = self.wpl_receive(pattern_list, timeout=sdkTimeout)
        self.wpl_log_info('output=[%s]' %output)
        if re.search('Error|Fail', output, re.IGNORECASE):
            self.wpl_log_fail('Failed minipack2_start_cpu_traffic: [Error/Fail] message found.')
            return 1
        else:
            # success
            return 0


#######################################################################################################################
# Function Name: minipack2_sleep_and_wait
# Date         : 14th May 2020
# Author       : TK NG<tikng@celestica.com>
#
# Procedure Revision Details:
#   Version : 1.0  - Initial Draft  - by TK NG<tikng@celestica.com>
#######################################################################################################################
    def minipack2_sleep_and_wait(self, runTime):
        self.wpl_log_debug('Entering procedure minipack2_sleep_and_wait with args : %s' %(str(locals())))

        # sleep for runTime seconds
        self.wpl_log_info('***sleep for %s seconds***' %(str(runTime)))
        cmd = 'sleep ' + str(runTime)
        waitTime = int(runTime) + int(SDK_TIMEOUT1)
        self.wpl_log_info('cmd=[%s]' %cmd)
        self.wpl_transmit(cmd)
        pattern_list = MINIPACK2_SDK_WAIT_PATTERN_LIST
        output = self.wpl_receive(pattern_list, timeout=waitTime)
        if re.search('Error|Fail', output, re.IGNORECASE):
            self.wpl_log_info('output=[%s]' %output)
            self.wpl_log_fail('Failed minipack2_sleep_and_wait: [Error/Fail] message found.')
            return 1
        else:
            # success
            return 0


#######################################################################################################################
# Function Name: minipack2_run_pvlan_show
# Date         : 14th May 2020
# Author       : TK NG<tikng@celestica.com>
#
# Procedure Revision Details:
#   Version : 1.0  - Initial Draft  - by TK NG<tikng@celestica.com>
#######################################################################################################################
    def minipack2_run_pvlan_show(self, sdkTimeout):
        self.wpl_log_debug('Entering procedure minipack2_run_pvlan_show with args : %s' %(str(locals())))

        # execute 'pvlan show' command
        self.wpl_log_info('***running pvlan show***')
        cmd = 'pvlan show'
        self.wpl_log_info('cmd=[%s]' %cmd)
        self.wpl_transmit(cmd)
        pattern_list = MINIPACK2_SDK_WAIT_PATTERN_LIST
        output = self.wpl_receive(pattern_list, timeout=sdkTimeout)
        self.wpl_log_debug('output=[%s]' %output)
        vlan_pattern1 = "Port([ \t])+cpu([\d])+([ \t])+default([ \t])+VLAN([ \t])+is([ \t])+([\d])+"
        vlan_pattern2 = "Port([ \t])+cd([\d])+([ \t])+default([ \t])+VLAN([ \t])+is([ \t])+([\d])+"
        vlan_pattern3 = "Port([ \t])+lb([\d])+([ \t])+default([ \t])+VLAN([ \t])+is([ \t])+([\d])+"
        vlan_pattern4 = "Port([ \t])+xe([\d])+([ \t])+default([ \t])+VLAN([ \t])+is([ \t])+([\d])+"
        result = self.vlan_check_output(cmd, output, vlan_pattern1, vlan_pattern2, vlan_pattern3, vlan_pattern4)
        if result:
            self.wpl_log_fail('Failed minipack2_run_pvlan_show.')
            return 1
        else:
            # success
            return 0


#######################################################################################################################
# Function Name: minipack2_run_vlan_show
# Date         : 14th May 2020
# Author       : TK NG<tikng@celestica.com>
#
# Procedure Revision Details:
#   Version : 1.0  - Initial Draft  - by TK NG<tikng@celestica.com>
#######################################################################################################################
    def minipack2_run_vlan_show(self, sdkTimeout):
        self.wpl_log_debug('Entering procedure minipack2_run_vlan_show with args : %s' %(str(locals())))

        # execute 'vlan show'
        self.wpl_log_info('***running vlan show***')
        cmd = 'vlan show'
        self.wpl_log_info('cmd=[%s]' %cmd)
        self.wpl_transmit(cmd)
        pattern_list = MINIPACK2_SDK_WAIT_PATTERN_LIST
        output = self.wpl_receive(pattern_list,timeout=SDK_TIMEOUT1)
        self.wpl_log_debug('output=[%s]' %output)
        vlan_pattern1 = r'vlan([ \t])+(\d+)([ \t])+ports([ \t])+cpu\,xe([ \t])+\(([\w,\d]+)\)\,([ \t])+(\w+)([ \t])+xe([ \t])+\(([\w,\d]+)\)([ \t])+([\w,\_]+)'
        vlan_pattern2 = r'vlan([ \t])+(\d+)([ \t])+ports([ \t])+cd([\d]+)([\-,\,]+)cd([\d]+)([ \t])+\(([\w,\d]+)\)\,([ \t])+(\w+)([ \t])+cd([\d]+)([\-,\,]+)cd([\d]+)([ \t])+\(([\w,\d]+)\)([ \t])+([\w,\_]+)'
        result = self.vlan_check_output(cmd, output, vlan_pattern1, vlan_pattern2, 'None', 'None')
        if result:
            self.wpl_log_fail('Failed minipack2_run_vlan_show.')
            return 1
        else:
            # success
            return 0


#######################################################################################################################
# Function Name: minipack2_enable_each_port
# Date         : 14th May 2020
# Author       : TK NG<tikng@celestica.com>
#
# Procedure Revision Details:
#   Version : 1.0  - Initial Draft  - by TK NG<tikng@celestica.com>
#######################################################################################################################
    def minipack2_enable_each_port(self, AllPort, setPortCmd, portEnableOption, sdkTimeout):
        self.wpl_log_debug('Entering procedure minipack2_enable_each_port with args : %s' %(str(locals())))

        # enable each port
        self.wpl_log_info('***Enable each port***')
        pattern_list = MINIPACK2_SDK_WAIT_PATTERN_LIST
        max_ports = 128
        if AllPort == 'True':
            cmd = setPortCmd + '0-cd127 ' + portEnableOption
            self.wpl_log_info('cmd=[%s]' % cmd)
            self.wpl_transmit(cmd)
            self.wpl_receive(pattern_list, timeout=sdkTimeout)
            time.sleep(1)
        else:
            for i in range(0, max_ports):
                cmd = ('%s%s %s' %(setPortCmd, str(i), portEnableOption))
                self.wpl_log_info('cmd=[%s]' %cmd)
                self.wpl_transmit(cmd)
                self.wpl_receive(pattern_list, timeout=sdkTimeout)
                time.sleep(0.5)


#######################################################################################################################
# Function Name: minipack2_disable_each_port
# Date         : 14th May 2020
# Author       : TK NG<tikng@celestica.com>
#
# Procedure Revision Details:
#   Version : 1.0  - Initial Draft  - by TK NG<tikng@celestica.com>
#######################################################################################################################
    def minipack2_disable_each_port(self, AllPort, setPortCmd, portDisableOption, sdkTimeout):
        self.wpl_log_debug('Entering procedure minipack2_enable_each_port with args : %s' %(str(locals())))

        # disable each port
        self.wpl_log_info('***Disable each port***')
        pattern_list = MINIPACK2_SDK_WAIT_PATTERN_LIST
        max_ports = 128
        if AllPort == 'True':
            cmd = setPortCmd + '0-cd127 ' + portDisableOption
            self.wpl_log_info('cmd=[%s]' % cmd)
            self.wpl_transmit(cmd)
            self.wpl_receive(pattern_list, timeout=sdkTimeout)
            time.sleep(1)
        else:
            for i in range(0, max_ports):
                cmd = ('%s%s %s' %(setPortCmd, str(i), portDisableOption))
                self.wpl_log_info('cmd=[%s]' %cmd)
                self.wpl_transmit(cmd)
                self.wpl_receive(pattern_list, timeout=sdkTimeout)
                time.sleep(0.5)


#######################################################################################################################
# Function Name: minipack2CheckTH4Presence
# Date         : 14th May 2020
# Author       : TK NG<tikng@celestica.com>
#
# Procedure Revision Details:
#   Version : 1.0  - Initial Draft  - by TK NG<tikng@celestica.com>
#######################################################################################################################
    def minipack2CheckTH4Presence(self):
        self.wpl_log_debug('Entering procedure minipack2CheckTH4Presence: %s\n'%(str(locals())))
        return self.device.isMinipack2TH4Presence()


#######################################################################################################################
# Function Name: minipack2_perform_sensor_reading_high_loading_stress_test
# Date         : 14th May 2020
# Author       : TK NG<tikng@celestica.com>
#
# Procedure Revision Details:
#   Version : 1.0  - Initial Draft  - by TK NG<tikng@celestica.com>
#######################################################################################################################
    def minipack2_perform_sensor_reading_high_loading_stress_test(self, initTool, initOption, initToolPath, set_vlan_cmd, start_traffic_cmd, stop_traffic_cmd, runTime, pattern1, sensorToolName, sensorToolOption, sensorToolPath):
        self.wpl_log_debug('Entering procedure minipack2_perform_sensor_reading_high_loading_stress_test: %s\n'%(str(locals())))

        t1 = time.time()

        # check for TH4 presence
        TH4_Present = self.minipack2CheckTH4Presence()

        if TH4_Present:
            # start cpu traffic stress test
            result = self.minipack2_start_cpu_traffic_stress_test(initTool, initOption, initToolPath, set_vlan_cmd, start_traffic_cmd, 0, pattern1)
            if result:
                result2 = self.minipack2_stop_cpu_traffic_stress_test(stop_traffic_cmd)
                if result2:
                    self.wpl_log_fail('Failed minipack2_stop_cpu_traffic_stress_test.')
                self.wpl_raiseException('Failed minipack2_perform_sensor_reading_high_loading_stress_test')
            self.wpl_sdk_switch_to_bmc()
        else:
            CommonLib.switch_to_openbmc()

        # run sensor reading stress test
        result1 = self.sensor_reading(sensorToolName, sensorToolOption, sensorToolPath, 'minipack2')

        if TH4_Present:
            self.wpl_bmc_switch_to_sdk()

            # stop cpu traffic stress test
            result2 = self.minipack2_stop_cpu_traffic_stress_test(stop_traffic_cmd)
            if result2:
                self.wpl_log_fail('Failed minipack2_stop_cpu_traffic_stress_test.')
                self.wpl_raiseException('Failed minipack2_perform_sensor_reading_high_loading_stress_test')

            # exit SDK
            self.minipack2_exit_sdk()

        t2 = time.time()
        time_diff = int(t2 - t1)
        self.wpl_log_debug('Total test time: [%s]' %(str(time_diff)))

        if result1:
            if TH4_Present:
                self.wpl_sdk_switch_to_bmc()

            self.wpl_log_fail('Failed sensor_reading.')
            self.wpl_raiseException('Failed minipack2_perform_sensor_reading_high_loading_stress_test')
        else:
            self.wpl_log_success('Successfully run minipack2_perform_sensor_reading_high_loading_stress_test.')


#######################################################################################################################
# Function Name: minipack2_SDK_re_init_test
# Date         : 14th May 2020
# Author       : TK NG<tikng@celestica.com>
#
# Procedure Revision Details:
#   Version : 1.0  - Initial Draft  - by TK NG<tikng@celestica.com>
#######################################################################################################################
    def minipack2_SDK_re_init_test(self, initTool, initOption, initToolPath, bcm_set_vlan_cmd, bcm_cpu_start_traffic_cmd, runTime, bcm_cpu_stop_traffic_cmd, pattern1):
        self.wpl_log_debug('Entering procedure minipack2_SDK_re_init_test: %s\n'%(str(locals())))

        CommonLib.switch_to_centos()

        CommonLib.change_dir(initToolPath)

        max_cycles = int(self.re_init_cycles)
        for i in range(0, max_cycles):
            self.wpl_log_info('************************************************************')
            self.wpl_log_info('*** Test Repeat Loop #: %s / %s ***' %((i+1), str(max_cycles)))
            self.wpl_log_info('************************************************************')

            result = self.minipack2_perform_cpu_traffic_check(initTool, initOption, initToolPath, bcm_set_vlan_cmd, bcm_cpu_start_traffic_cmd, runTime, bcm_cpu_stop_traffic_cmd, pattern1)
            if result:
                self.wpl_raiseException('Failed minipack2_SDK_re_init_test.')

        self.wpl_log_success('Successfully run minipack2_SDK_re_init_test: PASSED.')


#######################################################################################################################
# Function Name: minipack2_perform_cpu_traffic_check
# Date         : 14th May 2020
# Author       : TK NG<tikng@celestica.com>
#
# Procedure Revision Details:
#   Version : 1.0  - Initial Draft  - by TK NG<tikng@celestica.com>
#######################################################################################################################
    def minipack2_perform_cpu_traffic_check(self, initTool, initOption, initToolPath, bcm_set_vlan_cmd, bcm_cpu_start_traffic_cmd, runTime, bcm_cpu_stop_traffic_cmd, pattern1):
        self.wpl_log_debug('Entering procedure minipack2_perform_cpu_traffic_check: %s\n'%(str(locals())))

        # make sure no auto_load_user.py process running in the background
        self.check_and_terminate_sdk_tool_process(initTool)

        time.sleep(1)
        pim_counts = 0
        pim_counts = self.mp2_pim_count()
        # run auto_load_user.sh
        status = self.minipack2_sdk_init_check(initTool, initOption, SDK_TIMEOUT1)
        if status == 0:
            self.wpl_log_info('Successfully run auto_load_user.sh.')
        else:
            self.wpl_log_fail('Error running auto_load_user.sh script.')
            #if status == 1:
            #    self.minipack2_exit_sdk()
            return 1

        time.sleep(8)
        # mp2 dc unit set lb mac for no loopback
        devicename = os.environ.get("deviceName", "")
        if 'minipack2_dc' in devicename.lower():
            status = self.mp2_lb_mac_set(pim_counts)
            if status == 0:
                self.wpl_log_info('Successfully set mp2 dc lb mac')
            else:
                self.wpl_log_fail('Error running set mp2 dc lb mac.')
                # if status == 1:
                # self.minipack2_exit_sdk()
                return 1
            time.sleep(5)
        # execute 'ps' command and check ports status
        self.wpl_log_info('***checking all ports status***')
        status = self.minipack2_check_port_status('ps cd', 'up', 'enable')
        if status == 0:
            self.wpl_log_info('All ports status are up.')
        else:
            self.wpl_log_fail('Failed minipack2_check_port_status.')
            #self.minipack2_exit_sdk()
            return 1

        time.sleep(1)

        # execute linespeed200G.soc command
        status = self.minipack2_run_linespeed(bcm_set_vlan_cmd, pattern1, SDK_TIMEOUT1)
        if status == 0:
            self.wpl_log_info('Successfully run linespeed200G.soc command.')
        else:
            self.wpl_log_fail('Failed linespeed200G.soc command.')
            #self.minipack2_exit_sdk()
            return 1

        time.sleep(1)

        # clear counters
        status = self.minipack2_clear_port_counters(SDK_TIMEOUT1)
        if status == 0:
            self.wpl_log_info('Successfully cleared port counters.')
        else:
            self.wpl_log_fail('Error clearing port counters.')
            #self.minipack2_exit_sdk()
            return 1

        time.sleep(1)

        # start cpu traffic
        status = self.minipack2_start_cpu_traffic(bcm_cpu_start_traffic_cmd, SDK_TIMEOUT1)
        if status == 0:
            self.wpl_log_info('Successfully started cpu traffic.')
        else:
            self.wpl_log_fail('Error starting cpu traffic.')
            #self.minipack2_exit_sdk()
            return 1

        time.sleep(1)

        # sleep for runTime seconds
        status = self.minipack2_sleep_and_wait(runTime)
        if status == 0:
            self.wpl_log_info('Successfully sleep for %s seconds.' %(str(runTime)))
        else:
            self.wpl_log_fail('Error sleeping for %s seconds.' %(str(runTime)))
            #self.minipack2_exit_sdk()
            return 1

        time.sleep(1)

        # stop cpu traffic
        result1 = self.minipack2_stop_cpu_traffic_stress_test(bcm_cpu_stop_traffic_cmd)
        if result1:
            self.wpl_log_fail('Error stopping cpu traffic.')
            #self.minipack2_exit_sdk()
            return 1

        time.sleep(5)

        # check port counters
        result2 = self.minipack2_cpu_traffic_check_port_counters()
        if result2:
            self.wpl_raiseException('Failed minipack2_perform_cpu_traffic_check.')
            #self.minipack2_exit_sdk()
            return 1

        # exit SDK
        #self.minipack2_exit_sdk()

        self.wpl_log_success('Successfully run minipack2_perform_cpu_traffic_check: PASSED.')
        return 0


#######################################################################################################################
# Function Name: cloudripper_perform_detect_all_eloop_modules
# Date         : 14th May 2020
# Author       : TK NG<tikng@celestica.com>
#
# Procedure Revision Details:
#   Version : 1.0  - Initial Draft  - by TK NG<tikng@celestica.com>
#######################################################################################################################
    def cloudripper_perform_detect_all_eloop_modules(self, initTool, initOption, initToolPath, reInit_SDK=False):
        self.wpl_log_debug('Entering procedure cloudripper_perform_detect_all_eloop_modules with args : %s' %(str(locals())))

        if (self.eloop_init == '0') or (reInit_SDK == True):
            CommonLib.switch_to_centos()

            CommonLib.change_dir(initToolPath)

            # make sure no auto_load_user.py process running in the background
            self.check_and_terminate_sdk_tool_process(initTool)

            self.wpl_log_info("Running auto_load_user.py...")
            cmd = 'python3' + ' ' + initTool + ' ' + initOption
            self.wpl_log_info('cmd=[%s]' %cmd)
            self.wpl_transmit(cmd)
            pattern_list = SDK_WAIT_PATTERN_LIST
            output = self.wpl_receive(pattern_list,timeout=SDK_TIMEOUT2)
            time.sleep(2)
            self.wpl_log_debug('output = [%s]' %output)
            output = output.strip()
            #lastStr = output.split()[-1]
            if re.search(COMMON_SDK_PROMPT_II, output):
                quit = 'exit()'
                self.wpl_log_info('cmd=[%s]' %quit)
                self.wpl_transmit(quit)
                self.wpl_flush()
            else:
                self.wpl_log_fail('Failed running auto_load_user.py.')
                self.wpl_raiseException('Failed cloudripper_perform_detect_all_eloop_modules.')

            found = False
            Pass_Messg = GB_INIT_PASS_MSG
            for line in output.splitlines():
                #self.wpl_log_debug('%s' %line)
                line = line.strip()
                if len(line) == 0:
                    # blank line
                    continue
                else:
                    match = re.search(Pass_Messg, line, re.IGNORECASE)
                    if match:
                        found = True
                        break

            if found == False:
                self.wpl_log_fail('Failed running auto_load_user.py: GB Initialization Test pass message not found')
                self.wpl_raiseException('Failed cloudripper_perform_detect_all_eloop_modules.')
            else:
                self.wpl_log_info("Successfully run auto_load_user.py.")
                self.eloop_init = '1'
                self.wpl_log_success("Successfully run cloudripper_perform_detect_all_eloop_modules.")


#######################################################################################################################
# Function Name: cloudripper_perform_snake_traffic_stress_test
# Date         : 14th May 2020
# Author       : TK NG<tikng@celestica.com>
#
# Procedure Revision Details:
#   Version : 1.0  - Initial Draft  - by TK NG<tikng@celestica.com>
#######################################################################################################################
    def cloudripper_perform_snake_traffic_stress_test(self, toolName, toolPath, runTime, portMode):
        self.wpl_log_debug('Entering procedure cloudripper_perform_snake_traffic_stress_test: %s\n'%(str(locals())))

        CommonLib.switch_to_centos()

        CommonLib.change_dir(toolPath)

        # make sure no auto_load_user.py process running in the background
        self.check_and_terminate_sdk_tool_process(toolName)

        ##################################################################################
        ### e.g.
        #python3 auto_load_user.py -c l2_cpu -p 32x1x8x50g -m 2 -v 0,1,2,3 -d 60
        #python3 auto_load_user.py -c l2_cpu -p 32x1x8x50g -m 2 -v 4,5,6,7 -d 60 -n
        #python3 auto_load_user.py -c l2_cpu -p 32x1x8x50g -m 2 -v 8,9,10,11 -d 60 -n
        #python3 auto_load_user.py -c l2_cpu -p 32x1x8x50g -m 2 -v 12,13,14,15 -d 60 -n
        #python3 auto_load_user.py -c l2_cpu -p 32x1x8x50g -m 2 -v 20,21,22,23 -d 60 -n
        #python3 auto_load_user.py -c l2_cpu -p 32x1x8x50g -m 2 -v 24,25,26,27 -d 60 -n
        #python3 auto_load_user.py -c l2_cpu -p 32x1x8x50g -m 2 -v 28,29,30,31 -d 60 -n
        ##################################################################################

        #PORT_LIST = []
        #PORT_LIST.append('0,1,2,3')
        #PORT_LIST.append('4,5,6,7')
       # PORT_LIST.append('8,9,10,11')
       # PORT_LIST.append('12,13,14,15')
       # PORT_LIST.append('20,21,22,23')
      #  PORT_LIST.append('24,25,26,27')
      #  PORT_LIST.append('28,29,30,31')

      #  count = 0
      #  for PLIST in PORT_LIST:
      #      if count == 0:
        import os
        devicename = os.environ.get("deviceName", "")
        if "cloudripper" in devicename.lower():
                cmd = ('python3 %s -c l2_cpu -p %s '%(toolName, portMode))
        elif "minipack2" in devicename.lower():
                portMode = 'dd_8x50g_qsfp_4x50g'
                cmd = ('python3 %s -c l2_cpu -p %s -m 2 -v %s -d %s -n'%(toolName, portMode))
        self.wpl_log_info(cmd)
        self.wpl_transmit(cmd)
        pattern_list = SDK_WAIT_PATTERN_LIST
        output = self.wpl_receive(pattern_list,timeout=SDK_TIMEOUT2)
        self.wpl_log_debug('output = [%s]' %output)

        time.sleep(1)
        self.wpl_transmit('exit()')
        self.wpl_flush()

        found = False
        Pass_Messg = SNAKE_TRAFFIC_PASS_MSG
        for line in output.splitlines():
                #self.wpl_log_debug('%s' %line)
            line = line.strip()
            if len(line) == 0:
                    # blank line
                continue
            else:
                match = re.search(Pass_Messg, line, re.IGNORECASE)
                if match:
                    found = True
                    break

        if found == False:
            self.wpl_raiseException('Failed cloudripper_perform_snake_traffic_stress_test.')
        else:
            self.wpl_log_info('L2 snake traffic with cpu injection: PASSED')
        #    count += 1

        self.wpl_log_success("Successfully run cloudripper_perform_snake_traffic_stress_test. PASSED.")

#######################################################################################################################
    @logThis
    def dc_power_check(self):
        devicename = os.environ.get("deviceName", "")
        if 'minipack2' in devicename.lower():
            cmd = "sensor-util psu3 |grep 'PSU3_IN_VOLT' |awk '{print$4}'"
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

#######################################################################################################################
    @logThis
    def check_psu_slot_connection_test(self, toolName, option, pattern, path):

        self.wpl_getPrompt('openbmc', 600)
        power_type = self.dc_power_check()
        if power_type == 'DC':
            pattern = psu_connection_pattern_dc
        if path:
            self.wpl_transmit('cd ' + path)

        cmd = ('./' + toolName + option)
        passcount = 0
        output = self.wpl_execute(cmd, 'openbmc', timeout=180)
        self.wpl_log_debug("//////////output=%s///////" % output)
        for line in output.splitlines():
            line = line.strip()
            for i in range(0,len(pattern)):
                match = re.search(pattern[i], line)
                if match:
                    passcount += 1
        self.wpl_log_debug("//////////passcount=%s///////" % passcount)
        if passcount == len(pattern):
            self.wpl_log_success('Successfully check_psu_slot_connection_test pass')
        else:
            self.wpl_log_fail("Error: PSU can not be matched")
            self.wpl_raiseException("Failed check_psu_slot_connection_test.")

#######################################################################################################################
    @logThis
    def driver_auto_load_check(self, toolName, option, pattern):
        self.wpl_getPrompt(centos_mode, 60)
        cmd = toolName + ' ' + option
        p1 = r'^\d{2}'
        passcount = 0
        output = self.wpl_execute(cmd, mode=None, timeout=180)
        for line in output.splitlines():
            line = line.strip()
            match = re.search(p1, line)
            if match:
                passcount += 1
                deviceID = match.group(0)
                if deviceID == pattern:
                    self.wpl_log_success('Successfully get the device ID is %s' % deviceID)
                else:
                    self.wpl_log_fail("Error: device ID not be matched, get value: %s, expect value: %s" % deviceID,  pattern)
                    self.wpl_raiseException("Failed driver_auto_load_check.")
        if passcount < 1:
            self.wpl_log_fail("Error: Do not find the match info.")
            self.wpl_raiseException("Failed driver_auto_load_check.")

#######################################################################################################################
    @logThis
    def run_fw_version_check_in_come_side(self, toolName, option, pattern, expect):
        cmd = './' + toolName + ' ' + option    #./cel-version-test --show
        count = 0
        getVerLst = []
        output = self.wpl_execute(cmd, mode=None, timeout=180)
        ## get the version value from log
        for line in output.splitlines():
            line = line.strip()
            for value in pattern:
                match = re.search(value, line)
                if match:
                    count += 1
                    getVerKey = match.group(1)
                    getVerValue = match.group(2)
                    expectVerValue = expect[getVerKey]
                    if getVerValue == expectVerValue:
                        self.wpl_log_success('Successfully expect [%s] value is %s' % (getVerKey, getVerValue))
                    else:
                        self.wpl_log_fail("Error: the [%s] version is diff, get_version: %s, expect_version: %s" % (getVerKey, getVerValue, expectVerValue))
                        self.wpl_raiseException("Failed FW version check in COMe side.")
                        raise testFailed("Failed FW version check in COMe side.")

#######################################################################################################################
    @logThis
    def run_eMMC_check_in_bmc_side(self, fdiskTool):
        countError = 0
        CommonLib.switch_to_openbmc()
        emmc_dev = fdiskTool + " | grep 'mmcblk0:' | wc -l"
        emmc_size = fdiskTool + " |grep 'mmcblk0:' |awk '{print $3}'"
        emmc_dev_pattern = r'^\d'
        emmc_size_pattern = r'^\d\.\d{2}'
        expect_emmc_num = '1'
        expect_emmc_size = '7.28'
        emmc_tool_lst = [emmc_dev, emmc_size]
        emmc_pattern_lst = [emmc_dev_pattern, emmc_size_pattern]
        expect_emmc_lst = [expect_emmc_num, expect_emmc_size]
        for i in range(0, 2):
            time.sleep(3)
            output = self.wpl_execute(emmc_tool_lst[i], mode=None, timeout=180)
            for line in output.splitlines():
                line = line.strip()
                match = re.search(emmc_pattern_lst[i], line)
                if match:
                    if line >= expect_emmc_lst[i]:
                        self.wpl_log_success('Successfully get the usb num is %s' % (line))
                    else:
                        countError += 1
                        self.wpl_log_fail("Error: get value: %s, expect value: %s." % (line, expect_emmc_lst[i]))
        if countError >= 1:
            self.wpl_raiseException("Failed run_eMMC_check_in_bmc_side.")

#######################################################################################################################
    @logThis
    def run_pcie_and_disk_scan_test_in_come_side(self, toolName, pcieNum_Tool, pcieNum, pcieBusLst, busPatternLst, fdiskTool):
        self.wpl_log_info('====== Read all the PCIe data ======')
        self.wpl_transmit(toolName)
        count = 0
        count_error = 0
        self.wpl_transmit('\n')
        time.sleep(3)
        ##1. check pcie num
        output = self.wpl_execute(pcieNum_Tool, mode=None, timeout=180)
        p1 = r'^\d{2}'
        for line in output.splitlines():
            line = line.strip()
            match = re.search(p1, line)
            if match:
                if line == pcieNum:
                    self.wpl_log_success('Successfully expect PCIe num is %s' % (line))
                else:
                    count_error += 1
                    self.wpl_log_fail("Error: Get the PCIe number is diff, get value: %s, expect value: %s." % (line, pcieNum))
        ##2. check pcie bus info
        for i in range(len(pcieBusLst)):
            time.sleep(5)
            output = self.wpl_execute(pcieBusLst[i], mode=None, timeout=180)
            for line in output.splitlines():
                line = line.strip()
                match1 = re.search(busPatternLst[i][0], line)
                match2 = re.search(busPatternLst[i][1], line)
                if match1:
                    count += 1
                    pcie_device_id = match1.group(1)
                if match2:
                    count += 1
                    pcie_device_speed = match2.group(1)
            if count == 2:
                count = 0
                self.wpl_log_success('Successfully the device [%s] get the speed is %s' % (pcie_device_id, pcie_device_speed))
            else:
                count_error += 1
                self.wpl_log_fail("Error: can not get the match value about [%s]" % (pcie_device_id))
        ##3. fdisk scan
        self.wpl_log_info('====== Check fdisk scan ======')
        usbdev_cmd = usbdev_tool
        ssddev_cmd = ssddev_tool
        p2 = r'^\d'
        self.wpl_transmit(fdiskTool)
        fdiskToolLst = [usbdev_cmd, ssddev_cmd]
        fdiskExpectValue = [usbdev_num, ssddev_num]
        for i in range(0,2):
            time.sleep(3)
            output = self.wpl_execute(fdiskToolLst[i], mode=None, timeout=180)
            for line in output.splitlines():
                line = line.strip()
                match = re.search(p2, line)
                if match:
                    if line == fdiskExpectValue[i]:
                        self.wpl_log_success('Successfully get the usb num is %s' % (line))
                    else:
                        count_error += 1
                        self.wpl_log_fail("Error: Get the usb/ssd number is diff, get value: %s, expect value: %s." % (line, fdiskExpectValue[i]))
        self.wpl_log_info('====== check eMMC in bmc side ======')
        ##4. eMMC check in bmc side
        self.run_eMMC_check_in_bmc_side(fdiskTool)
        if count_error >= 1:
            self.wpl_raiseException("Failed run_pcie_and_disk_scan_test_in_come_side.")
            raise testFailed("Failed run_pcie_and_disk_scan_test_in_come_side.")

#######################################################################################################################
    @logThis
    def run_ipv6_ping_test(self, toolName, ethNum, usb0Num):
        come_eth0_ipv6 = ''
        come_usb0_ipv6 = ''
        bmc_eth0_ipv6 = ''
        bmc_usb0_ipv6 = ''
        counterLanNumLst = [ethNum, usb0Num]
        p1 = r'^\d'
        count_error = 0
        for cmd in counterLanNumLst:
            output = self.wpl_execute(cmd, mode=None, timeout=180)
            for line in output.splitlines():
                line = line.strip()
                match = re.search(p1, line)
                if match:
                    if line == '1':
                        self.wpl_log_success('Successfully get the current lan num is %s' % (line))
                    else:
                        count_error += 1
                        self.wpl_log_fail("Error: Get the eth0/usb0 number is diff, get value: %s, expect value: 1." % line)

        ##1. get COMe side ipv6 address:
        eth_tool = 'ifconfig eth0'
        dhcp_tool = 'dhclient -6 eth0'
        self.get_ipv6_address(eth_tool, dhcp_tool)
        come_eth0_pattern = r'inet6[ \t]+(2001:db8:0:.*)[ \t]+prefixlen'
        come_usb0_pattern = r'inet6[ \t]+(fe80::ff:.*)[ \t]+prefixlen'
        output = self.wpl_execute(toolName, mode=None, timeout=180)
        for line in output.splitlines():
            line = line.strip()
            match1 = re.search(come_eth0_pattern, line)
            match2 = re.search(come_usb0_pattern, line)
            if match1:
                come_eth0_ipv6 = match1.group(1)
            if match2:
                come_usb0_ipv6 = match2.group(1)

        ##2. get bmc side ipv6 address:
        CommonLib.switch_to_openbmc()
        bmc_eth0_pattern = r'inet6[ \t]+addr:[ \t]+(2001:db8:0:.*)/\d{2,3}[ \t]+Scope:Global'
        bmc_usb0_pattern = r'inet6[ \t]+addr:[ \t]+(fe80::ff:.*)/\d{2,3}[ \t]+Scope:Link'
        output = self.wpl_execute(toolName, mode=None, timeout=180)
        for line in output.splitlines():
            line = line.strip()
            match3 = re.search(bmc_eth0_pattern, line)
            match4 = re.search(bmc_usb0_pattern, line)
            if match3:
                bmc_eth0_ipv6 = match3.group(1)
            if match4:
                bmc_usb0_ipv6 = match4.group(1)

        #3. ping come
        ping_eth_come_cmd = 'ping6 -c 5 ' + come_eth0_ipv6
        ping_usb0_come_cmd = 'ping6 -c 5 ' + come_usb0_ipv6 + '%usb0'
        ping_remote_server_cmd = 'ping6 -c 5 ' + server_ipv6
        # ping bmc
        ping_eth_bmc_cmd = 'ping6 -c 5 ' + bmc_eth0_ipv6
        ping_usb0_bmc_cmd = 'ping6 -c 5 ' + bmc_usb0_ipv6 + '%usb0'
        ping_bmc_cmd_lst = [ping_eth_bmc_cmd, ping_usb0_bmc_cmd, ping_remote_server_cmd]
        ping_come_cmd_lst = [ping_eth_come_cmd, ping_usb0_come_cmd, ping_remote_server_cmd]
        ping_pattern = r'5[ \t]+packets transmitted,[ \t]+5[ \t]+received,[ \t]+(\d)%[ \t]+packet loss,[ \t]+time[ \t]+(\d{3})ms'
        ping_cmd = [ping_come_cmd_lst, ping_bmc_cmd_lst]
        for i in range(0,2):
            if i == 1:
                CommonLib.switch_to_centos()
            for cmd in ping_cmd[i]:
                output = self.wpl_execute(cmd, mode=None, timeout=180)
                for line in output.splitlines():
                    line = line.strip()
                    match = re.search(ping_pattern, line)
                    if match:
                        lossPacket = match.group(1)
                        if lossPacket == '0':
                            self.wpl_log_success('Successfully ping ip [%s]' % (cmd[11:]))
                        else:
                            count_error += 1
                            self.wpl_log_fail("Error: ping ip [%s] fail, package loss %s%" % (cmd[11:], lossPacket))

        if (count_error > 0):
            self.wpl_raiseException("Failed run_ipv6_ping_test.")
            raise testFailed("Failed run_ipv6_ping_test.")

#######################################################################################################################
    @logThis
    def run_current_version_check_in_bmc_side(self, toolName, option, bmc_ver_tool, boot_util, Expect_bmc):
        scm_cmd = toolName + option
        bmc_ver_cmd = bmc_ver_tool
        boot_flash_cmd =  boot_util + ' bmc'
        p1 = r'BIOS Version:[ \t]+(\w+)'
        p2 = r'OpenBMC Release[ \t]+(wedge400|fuji)-v(.*)'
        p3 = r'Current Boot Code Source:[ \t]+(\w+)[ \t]+Flash'
        p4 = r'Bridge-IC Version: (v.*)'
        tool_cmd_lst = [scm_cmd, bmc_ver_cmd, boot_flash_cmd]
        pattern_lst = [p1, p2, p3, p4]
        expect_lst = [BIOS_Ver, Expect_bmc, BMC_boot_type, BIC_Ver]
        count_error = 0
        for i in range(0,3):
            output = self.wpl_execute(tool_cmd_lst[i], mode=None, timeout=180)
            for line in output.splitlines():
                line = line.strip()
                if i == 0:
                    match1 = re.search(pattern_lst[3], line)
                    if match1:
                        get_value = match1.group(1)
                        if get_value == expect_lst[3]:
                            self.wpl_log_success('Successfully get value is %s' % (get_value))
                        else:
                            count_error += 1
                            self.wpl_log_fail("Error: get the value [%s] is failed, expect is %s" % (get_value, expect_lst[3]))
                match = re.search(pattern_lst[i], line)
                if match:
                    if i == 1:
                        get_value = match.group(2)
                    else:
                        get_value = match.group(1)
                    if get_value == expect_lst[i]:
                        self.wpl_log_success('Successfully get value is %s' % (get_value))
                    else:
                        count_error += 1
                        self.wpl_log_fail("Error: get the value [%s] is failed, expect is %s" % (get_value, expect_lst[i]))

        if (count_error > 0):
            self.wpl_raiseException("Failed run_current_version_check_in_bmc_side.")
   
#######################################################################################################################
    @logThis
    def run_sensor_info_check_in_bmc_side(self, toolName, option, pattern, expect):
        cmd = toolName + option
        count_error = 0
        output = self.wpl_execute(cmd, mode=openbmc_mode, timeout=180)
        for line in output.splitlines():
            line = line.strip()
            if 'SYSTEM_AIRFLOW' in line:
                continue
            match = re.search(pattern, line)
            if match:
                sensorName = match.group(1)
                sensorRes = match.group(3)
                if sensorRes == expect:
                    self.wpl_log_success('Successfully [%s] status is [%s]' % (sensorName, sensorRes))
                else:
                    count_error += 1
                    self.wpl_log_fail("Error: sensor [%s] status is [%s]" % (sensorName, match.group(0)))

        if (count_error > 0):
            self.wpl_raiseException("Failed run_current_version_check_in_bmc_side.")

#######################################################################################################################
    @logThis
    def fru_cmd_and_log_check(self, lstCmd, pattern, resDict):
        err_msg = r'([E|e]rror)|(No such file or directory)|(Fail.*)|(command not found)'
        output = self.wpl_execute(lstCmd, mode=openbmc_mode, timeout=180)
        err_match = re.search(err_msg, output)
        if err_match:
            self.wpl_log_fail("Found error: %s" % (err_match.group(0)))
        for line in output.splitlines():
            line = line.strip()
            if '---------------' in line:
                continue
            match = re.search(pattern, line)
            if match:
                key = match.group(1).strip()
                resDict[key] = match.group(2).strip()
        #self.wpl_log_info(resDict)

#######################################################################################################################
    @logThis
    def run_fru_info_check_in_bmc_side(self, tool_lst, tool_path_lst, eeprom_tool, fan_eeprom_tool):
        devicename = os.environ.get("deviceName", "")
        ##1. read util tool data
        p1 = r'(.+): (.+)'
        p2 = r'(\w+)\s+= (.+)'
        weutilDict = {};  feutilDict = {};  seutilDict = {};  peutilDict = {}; peutil1Dict = {}; peutil2Dict = {};
        peutil3Dict = {}; peutil4Dict = {}; peutil5Dict = {}; peutil6Dict = {}; peutil7Dict = {}; peutil8Dict = {}
        utilDictLst = [weutilDict, feutilDict, seutilDict, peutilDict]
        peutilDictLst = [peutil1Dict, peutil2Dict, peutil3Dict, peutil4Dict, peutil5Dict,
                         peutil6Dict, peutil7Dict, peutil8Dict]
        err_msg = r'([E|e]rror)|(No such file or directory)|(Fail.*)|(command not found)'
        # feutil check
        fcm_feutil_cmd = tool_lst[1] + ' fcm';  fcmT_feutil_cmd = tool_lst[1] + ' fcm-t'
        fcmB_feutil_cmd = tool_lst[1] + ' fcm-b';  fan1_feutil_cmd = tool_lst[1] + ' 1'
        fan2_feutil_cmd = tool_lst[1] + ' 2';  fan3_feutil_cmd = tool_lst[1] + ' 3'
        fan4_feutil_cmd = tool_lst[1] + ' 4';  fan5_feutil_cmd = tool_lst[1] + ' 5'
        fan6_feutil_cmd = tool_lst[1] + ' 6';  fan7_feutil_cmd = tool_lst[1] + ' 7'
        fan8_feutil_cmd = tool_lst[1] + ' 8'
        wedge_feutil_cmd = [fcm_feutil_cmd, fan1_feutil_cmd, fan2_feutil_cmd, fan3_feutil_cmd, fan4_feutil_cmd]
        mp2_feutil_cmd = [fcmT_feutil_cmd, fcmB_feutil_cmd, fan1_feutil_cmd, fan2_feutil_cmd, fan3_feutil_cmd,
                          fan4_feutil_cmd, fan5_feutil_cmd, fan6_feutil_cmd, fan7_feutil_cmd, fan8_feutil_cmd]
        fcmFeDict = {};  fcmTFeDict = {};  fcmBFeDict = {}; fan1FeDict = {}; fan2FeDict = {};
        fan3FeDict = {}; fan4FeDict = {}; fan5FeDict = {}; fan6FeDict = {}; fan7FeDict = {}; fan8FeDict = {}
        wedge_feutil_lst = [fcmFeDict, fan1FeDict, fan2FeDict, fan3FeDict, fan4FeDict]
        mp2_feutil_lst = [fcmTFeDict, fcmBFeDict, fan1FeDict, fan2FeDict, fan3FeDict,
                          fan4FeDict, fan5FeDict, fan6FeDict, fan7FeDict, fan8FeDict]
        if 'minipack2' in devicename.lower():
            for i in range(len(mp2_feutil_cmd)):
                self.fru_cmd_and_log_check(mp2_feutil_cmd[i], p1, mp2_feutil_lst[i])
        else:
            for i in range(len(wedge_feutil_cmd)):
                self.fru_cmd_and_log_check(wedge_feutil_cmd[i], p1, wedge_feutil_lst[i])

        ##weutil/seutil/peutil check
        for i in range(0,4):
            if i == 1:
                continue
            if i == 3:
                if 'minipack2' in devicename.lower():
                    for k in range(2,10):
                        peutil_cmd = tool_lst[i] + ' ' + str(k)
                        self.fru_cmd_and_log_check(peutil_cmd, p1, peutilDictLst[k-2])
            else:
                self.fru_cmd_and_log_check(tool_lst[i], p1, utilDictLst[i])

        #2. read eeprom data
        smbDict = {}; scmDict = {}; fcmDict = {}; fcmTDict = {}; fcmBDict = {}; fan1Dict = {}; fan2Dict = {};
        fan3Dict = {}; fan4Dict = {}; fan5Dict = {}; fan6Dict = {}; fan7Dict = {}; fan8Dict = {}; pim1Dict = {};
        pim2Dict = {}; pim3Dict = {}; pim4Dict = {}; pim5Dict = {}; pim6Dict = {}; pim7Dict = {}; pim8Dict = {}
        simDict = {}
        if 'wedge400' in devicename.lower():
            smb_cmd = './' + eeprom_tool + ' -e SMB';    scm_cmd = './' + eeprom_tool + ' -e SCM'
            fcm_cmd = './' + eeprom_tool + ' -e FCM';    fan1_cmd = './' + eeprom_tool + ' -e FAN 1'
            fan2_cmd = './' + eeprom_tool + ' -e FAN 2'; fan3_cmd = './' + eeprom_tool + ' -e FAN 3'
            fan4_cmd = './' + eeprom_tool + ' -e FAN 4'
            eeprom_fru_cmd = [smb_cmd, scm_cmd, fcm_cmd, fan1_cmd, fan2_cmd, fan3_cmd, fan4_cmd]
            eeprom_fru_lst = [smbDict, scmDict, fcmDict, fan1Dict, fan2Dict, fan3Dict, fan4Dict]
            eeprom_path = 'cd ' + tool_path_lst[6]
            self.wpl_transmit(eeprom_path)
            for i in range(0, 7):
                self.fru_cmd_and_log_check(eeprom_fru_cmd[i], p2, eeprom_fru_lst[i])
        elif 'minipack2' in devicename.lower():
            sim_path = 'cd ' +  tool_path_lst[0]; fcmT_path = 'cd ' + tool_path_lst[1]
            fcmB_path = 'cd ' + tool_path_lst[2]; fan_path = 'cd ' + tool_path_lst[3]
            scm_path = 'cd ' + tool_path_lst[4];  pim_path = 'cd ' + tool_path_lst[5]
            mp2_fru_lst = [simDict, scmDict, fcmTDict, fcmBDict]
            mp2_fan_fru_lst = [fan1Dict, fan2Dict, fan3Dict, fan4Dict, fan5Dict, fan6Dict, fan7Dict, fan8Dict]
            mp2_pim_fru_lst = [pim1Dict, pim2Dict, pim3Dict, pim4Dict, pim5Dict, pim6Dict, pim7Dict, pim8Dict]
            for i in range(0,4):
                if i == 0:
                    self.wpl_transmit(sim_path)
                elif i == 1:
                    self.wpl_transmit(scm_path)
                elif i == 2:
                    self.wpl_transmit(fcmT_path)
                elif i == 3:
                    self.wpl_transmit(fcmB_path)
                self.fru_cmd_and_log_check('./' + eeprom_tool, p2, mp2_fru_lst[i])
            ##get fan/pim eeprom for mp2
            for k in range(1,3):
                if k == 1:
                    self.wpl_transmit(fan_path)
                elif k == 2:
                    self.wpl_transmit(pim_path)
                for i in range(1,9):
                    output = self.wpl_execute('./' + fan_eeprom_tool + ' ' + str(i), mode=None, timeout=180)
                    err_match = re.search(err_msg, output)
                    if err_match:
                        self.wpl_log_fail("Found error: %s" % (err_match.group(0)))
                    for line in output.splitlines():
                        line = line.strip()
                        if '---------------' in line:
                            continue
                        match = re.search(p2, line)
                        if match:
                            key = match.group(1).strip()
                            if k == 1:
                                mp2_fan_fru_lst[i-1][key] = match.group(2).strip()
                            elif k == 2:
                                mp2_pim_fru_lst[i-1][key] = match.group(2).strip()
                    # if k == 1:
                    #     self.wpl_log_info(mp2_fan_fru_lst[i-1])
                    # elif k == 2:
                    #     self.wpl_log_info(mp2_pim_fru_lst[i-1])

        ##3. compare the data
        wedge_util_lst = [weutilDict, fcmFeDict, fan1FeDict, fan2FeDict, fan3FeDict, fan4FeDict, seutilDict]
        mp2_util_lst = [weutilDict, fcmTFeDict, fcmBFeDict, fan1FeDict, fan2FeDict, fan3FeDict, fan4FeDict,
                        fan5FeDict, fan6FeDict, fan7FeDict, fan8FeDict, seutilDict, peutil1Dict, peutil2Dict,
                        peutil3Dict, peutil4Dict, peutil5Dict, peutil6Dict, peutil7Dict, peutil8Dict]
        wedge_util_name = ['weutil', 'feutil-fcm', 'feutil-fan1', 'feutil-fan2', 'feutil-fan3', 'feutil-fan4', 'seutil']
        mp2_util_name = ['weutil', 'feutil-fcmT', 'feutil-fcmB', 'feutil-fan1', 'feutil-fan2', 'feutil-fan3',
                         'feutil-fan4', 'feutil-fan5', 'feutil-fan6', 'feutil-fan7', 'feutil-fan8', 'seutil',
                         'peutil-1', 'peutil-2', 'peutil-3', 'peutil-4', 'peutil-5', 'peutil-6', 'peutil-7', 'peutil-8']
        util_name = [wedge_util_name, mp2_util_name]
        util_lst = [wedge_util_lst, mp2_util_lst]

        wedge_fru_lst = [smbDict, fcmDict, fan1Dict, fan2Dict, fan3Dict, fan4Dict, scmDict]
        mp2_fru_lst = [simDict, fcmTDict, fcmBDict, fan1Dict, fan2Dict, fan3Dict, fan4Dict, fan5Dict, fan6Dict,
                       fan7Dict, fan8Dict, scmDict, pim1Dict, pim2Dict, pim3Dict, pim4Dict, pim5Dict, pim6Dict,
                       pim7Dict, pim8Dict]
        eeprom_lst = [wedge_fru_lst, mp2_fru_lst]
        #change util log
        err_count = 0
        for k in range(len(util_lst)):
            if k == 0 and 'wedge400' in devicename.lower():
                check_util_lst = util_lst[k]
                check_fru_lst = eeprom_lst[k]
                check_util_name_lst = util_name[k]
            elif k == 1 and 'minipack2' in devicename.lower():
                check_util_lst = util_lst[k]
                check_fru_lst = eeprom_lst[k]
                check_util_name_lst = util_name[k]
            else:
                continue
            for i in range(len(check_util_lst)):
                outDict = {}
                self.wpl_transmit('\n')
                self.wpl_log_info('=============== util %s log format change ===============' % (check_util_name_lst[i]))
                for key, val in check_util_lst[i].items():
                    if key in map_key_dict:
                        mapping_key = map_key_dict[key]
                    else:
                        mapping_key = re.sub(r'\s|-', '_', key).lower()
                    if mapping_key == 'product_name':
                        outDict[mapping_key] = val
                    elif mapping_key == 'format_version':
                        outDict[mapping_key] = hex(int(val))
                    elif mapping_key == 'system_manufacturing_date':
                        outDict[mapping_key] = datetime.strptime(val, '%m-%d-%y').strftime('%Y%m%d')
                    elif re.search(r'^N\/?-?A-?', val):
                        outDict[mapping_key] = 'NA'
                    else:
                        outDict[mapping_key] = re.sub('-|:', '', val)
                    outDict[mapping_key] = outDict[mapping_key].upper()
                    self.wpl_log_info("%s: %s --> %s: %s" % (key, val, mapping_key, outDict[mapping_key]))
                #change eeprom log
                if 'magic_word' in check_fru_lst[i]:
                    del check_fru_lst[i]['magic_word']
                for key, val in check_fru_lst[i].items():
                    if re.search(r'^N\/?-?A-?', val) and val != 'NA':
                        self.wpl_log_info("%s: %s --> %s: NA" % (key, val, key))
                        check_fru_lst[i][key] = 'NA'
                    check_fru_lst[i][key] = check_fru_lst[i][key].upper()
                #compare util and eeprom
                self.wpl_log_info("=========== comparing util with eeprom output =========== ")
                err_count += CommonLib.compare_input_dict_to_parsed(outDict, check_fru_lst[i], highlight_fail=True)
                if err_count:
                    self.wpl_log_fail("failed comparing util and eeprom log")
        if (err_count > 0):
            self.wpl_raiseException("Failed run_fru_info_check_in_bmc_side.")

#######################################################################################################################
    @logThis
    def run_power_cycle_chassis_test(self, var_toolName, var_option):
        cmd = var_toolName + var_option
        booting_msg = 'Starting kernel'
        self.wpl_transmit(cmd)
        output = self.wpl_receive(booting_msg, timeout=Const.BOOTING_TIME)
        time.sleep(180)
        self.wpl_getPrompt(Const.BOOT_MODE_OPENBMC, timeout=Const.BOOTING_TIME)
        self.wpl_getPrompt(Const.BOOT_MODE_CENTOS, timeout=Const.BOOTING_TIME)
        self.wpl_getPrompt(Const.BOOT_MODE_OPENBMC)
        time.sleep(10)
        return output
   
#######################################################################################################################
    @logThis
    def run_power_on_and_off_test(self, toolName, option1, option2):
        power_on_cmd = toolName + option1
        power_off_cmd = toolName + option2
        p1 = 'CentOS Linux'
        self.wpl_transmit(power_off_cmd)
        time.sleep(5)
        self.wpl_sendline("\r")
        self.wpl_transmit(power_on_cmd)
        self.wpl_sendline("sol.sh")
        self.wpl_receive('CTRL-l + b : Send Break', timeout=10)
        output = self.wpl_receive(self.device.loginPromptDiagOS, timeout=600)
        res = re.search(p1, output)
        if res:
            self.wpl_log_info('find the keyword, wait enter the centos!')
            self.wpl_getPrompt(Const.BOOT_MODE_CENTOS, timeout=Const.BOOTING_TIME)
        else:
            self.wpl_raiseException("wait_enter_centos fail")

#######################################################################################################################
    @logThis
    def run_warm_reset_sdk_traffic_check(self, toolName, toolPath, runTime, portMode):
        CommonLib.change_dir(toolPath)
        cmd = ('python3 %s -c l2_cpu -d %s -p %s > temp.txt &' % (toolName, runTime, portMode))
        self.wpl_transmit(cmd)
        time.sleep(10)
        ps_cmd = 'ps -aux |grep ' + toolName + " |grep -v 'grep'"
        output = self.wpl_execute(ps_cmd, mode=None, timeout=180)
        match = re.search(portMode, output)
        if match:
            self.wpl_log_info('Successfuly run sdk in background mode.')
        else:
            self.wpl_raiseException("Fail run sdk in background mode.")

#######################################################################################################################
    @logThis
    def run_warm_reset_sdk_traffic_check_w400(self, bcmTool, toolPath, toolName, option, catTool, clsTool, trafficTool):
        CommonLib.change_dir(toolPath)
        self.check_and_terminate_sdk_tool_process(bcmTool)
        count = 0
        time.sleep(2)
        p1 = '^cd\d{1,2}\(.*\)[ \t]+up.*'
        sdkIntCmd = './' + toolName + option
        portCmd = './' + clsTool + ' ps cd'
        InitCmdLst = [sdkIntCmd, catTool, truncateTool, portCmd]
        for cmd in InitCmdLst:
            time.sleep(3)
            output = self.wpl_execute(cmd, mode=None, timeout=60)
            self.wpl_transmit('\n')
            self.wpl_receive(self.device.promptDiagOS, timeout=90)
            #self.wpl_flush()
        output = self.wpl_execute(catTool, mode=None, timeout=60)
        for line in output.splitlines():
            line = line.strip()
            res = re.search(p1, line)
            if res:
                count += 1
        if count == 48:
            self.wpl_log_info('All port is up status!')
        else:
            self.wpl_log_fail("Found port have down status")
        ##set vlan
        self.wpl_log_info('============ start to set the VLAN, then traffic test ============')
        vlanCmd = './' + clsTool + ' ' + trafficTool
        clearTool = './' + clsTool + ' clear c'
        DDTrafficCmd = './' + clsTool + ' '+ w400_DD_traffic_cmd
        FiveSixTrafficCmd = './' + clsTool + ' ' + w400_56_traffic_cmd
        CmdLst = [vlanCmd, clearTool, DDTrafficCmd, FiveSixTrafficCmd]
        for cmd in CmdLst:
            time.sleep(3)
            self.wpl_transmit('\n')
            output = self.wpl_execute(cmd, mode=None, timeout=90)
            self.wpl_receive(self.device.promptDiagOS, timeout=90)

#######################################################################################################################
    @logThis
    def run_warm_reset_sdk_traffic_check_mp2(self, toolName, option, toolPath, toolLst, trafficLst):
        error_count = 0
        p1 = 'gb_parinit pim8 ret 0'
        p2 = '^\d+'
        CommonLib.change_dir(toolPath)
        ##1. check the bcm.user in background first.
        self.check_and_terminate_sdk_tool_process(toolLst[0])
        ##2. init mp2 sdk
        xphybackCmd = './' + toolLst[1] + ' &'
        initCmd = './' + toolLst[2] + ' ' + toolLst[3]
        initCmdLst = [xphybackCmd, initCmd]
        for cmd in initCmdLst:
            time.sleep(3)
            output = self.wpl_execute(cmd, mode=None, timeout=600)
        for line in output.splitlines():
            line = line.strip()
            res = re.search(p1, line)
            if res:
                self.wpl_log_success('Successfully run sdk init!')
        ##3. run sdk:
        autoLoadCmd = './' + toolName + option
        portCmd = './' + trafficLst[0] + ' ps cd'
        runCmdLst = [autoLoadCmd, toolLst[4], toolLst[5], portCmd]
        for cmd in runCmdLst:
            time.sleep(5)
            self.wpl_execute(cmd, mode=None, timeout=180)
            # self.wpl_transmit('\n')
            # self.wpl_receive(self.device.promptDiagOS, timeout=90)
        upPortCmd = toolLst[4] + " |egrep -a 'cd.*\(' |grep -c 'up'"
        upCheckCmdLst = [toolLst[4], upPortCmd]
        for cmd in upCheckCmdLst:
            output = self.wpl_execute(cmd, mode=None, timeout=60)
        for line in output.splitlines():
            line = line.strip()
            res = re.search(p2, line)
            if res:
                if int(res.group(0)) == 128:
                    self.wpl_log_info('All port is up status!')
                else:
                    error_count += 1
                    self.wpl_log_fail("Found port have down status")
        ##4. set vlan and start traffic:
        vlanCmd = './' + trafficLst[0] + ' ' + trafficLst[1]
        clearCmd = './' + trafficLst[0] + ' ' + 'clear c'
        trafficCmd = './' + trafficLst[0] + ' ' + trafficLst[2]
        trafficCmdLst = [vlanCmd, clearCmd, trafficCmd]
        for cmd in trafficCmdLst:
            time.sleep(3)
            self.wpl_transmit('\n')
            self.wpl_execute(cmd, mode=None, timeout=90)

#######################################################################################################################
    @logThis
    def run_come_warm_reset_test(self, toolName):
        p1 = 'CentOS Linux'
        self.wpl_transmit(toolName)
        output = self.wpl_receive(self.device.loginPromptDiagOS, timeout=600)
        res = re.search(p1, output)
        if res:
            self.wpl_log_info('find the keyword, wait enter the centos!')
            self.wpl_getPrompt(Const.BOOT_MODE_CENTOS, timeout=Const.BOOTING_TIME)
        else:
            self.wpl_raiseException("wait_enter_centos fail")

#######################################################################################################################
    @logThis
    def get_ipv6_address(self, eth_tool, dhcp_tool, timeout=20):
        ipformat = r'inet6 (2001.*)\sprefixlen'
        ipList = []
        self.wpl_transmit(dhcp_tool)
        time.sleep(6)
        #output = self.device.sendCmdRegexp(eth_tool, self.device.promptDiagOS, timeout=80)
        output = self.wpl_execute(eth_tool, mode=None, timeout=180)
        self.wpl_log_info(output)
        for line in output.splitlines():
            line = line.strip()
            match = re.search(ipformat, line)
            if match:
                ip = match.group(1).strip()
                ipList.append(ip)
                self.wpl_log_success('Successfully get ip address: %s' % (ip))
        return ipList

#######################################################################################################################
    @logThis
    def run_copy_sdk_soc_files_for_BCM(self, eth_tool, dhcp_tool, scp_ip, usrname, pasrd, local_path, scp_path):
        self.get_ipv6_address(eth_tool, dhcp_tool)
        time.sleep(5)
        devicename = os.environ.get("deviceName", "")
        if 'wedge400_' in devicename.lower():
            cmd = 'scp -6 -r ' + usrname + '@' + '[' + scp_ip + ']' + ':' + local_path + '/*' + ' ' + scp_path
        else:
            cmd = 'scp -6 -r ' + usrname + '@' + '[' + scp_ip + ']' + ':' + local_path + '/' + mp2_traffic_script + ' ' + scp_path
        self.wpl_transmit(cmd)
        time.sleep(5)
        self.wpl_log_info("////local path = %s " % local_path)
        self.wpl_log_info("////scp_path = %s " % scp_path)
        promptList = ["(yes/no)", "password:"]
        patternList = re.compile('|'.join(promptList))
        output1 = self.device.read_until_regexp(patternList, 200)
        # self.wpl_log_info('output1: ' + str(output1))
        match1 = re.search("(yes/no)", output1)
        match3 = re.search("password:", output1)
        if match1:
            self.device.transmit("yes")
            self.device.receive("password:")
            self.device.transmit("%s" % pasrd)
        elif match3:
            self.device.transmit("%s" % pasrd)
        else:
            self.wpl_log_fail("pattern mismatch")
        # self.device.read_until_regexp(cmd1, self.device.promptDiagOS, timeout=50)
        # time.sleep(5)
        self.device.sendMsg("\n")
        self.wpl_receive(self.device.promptDiagOS, timeout=90)
        self.wpl_flush()

#######################################################################################################################
    @logThis
    def run_check_scm_fw_version(self, toolName, option, scm_pattern, scm_expect, bmc_ver_tool, Expect_bmc):
        scm_cmd = toolName + option
        bmc_ver_cmd = bmc_ver_tool
        count_error = 0
        p1 = r'OpenBMC Release[ \t]+(wedge400|fuji)-v(.*)'
        output = self.wpl_execute(bmc_ver_cmd, mode=None, timeout=180)
        for line in output.splitlines():
            line = line.strip()
            match = re.search(p1, line)
            if match:
                get_bmc_value = match.group(2)
                if get_bmc_value == Expect_bmc:
                    self.wpl_log_success('Successfully get bmc version is %s' % (get_bmc_value))
                else:
                    count_error += 1
                    self.wpl_log_fail("Error: get the bmc value [%s] is failed, expect is %s" % (get_bmc_value, Expect_bmc))
        ## scm version check:
        output = self.wpl_execute(scm_cmd, mode=None, timeout=180)
        for line in output.splitlines():
            line = line.strip()
            for value in scm_pattern:
                match = re.search(value, line)
                if match:
                    getVerKey = match.group(1)
                    getVerValue = match.group(2)
                    expectVerValue = scm_expect[getVerKey]
                    if getVerValue == expectVerValue:
                        self.wpl_log_success('Successfully expect [%s] value is %s' % (getVerKey, getVerValue))
                    else:
                        count_error += 1
                        self.wpl_log_fail("Error: the [%s] version is diff, get_version: %s, expect_version: %s" % (getVerKey, getVerValue, expectVerValue))
        if (count_error > 0):
            self.wpl_raiseException("Failed run_current_version_check_in_bmc_side.")

#######################################################################################################################
    @logThis
    def run_check_bmc_or_bios_master_status(self, toolName, option, pattern, expect):
        cmd = toolName + option
        count_error = 0
        output = self.wpl_execute(cmd, mode=openbmc_mode, timeout=180)
        for line in output.splitlines():
            line = line.strip()
            match = re.search(pattern, line, re.IGNORECASE)
            if match:
                get_mode = match.group(1)
                if get_mode == expect:
                    self.wpl_log_success('Successfully current mode is %s' % (get_mode))
                else:
                    if (get_mode == 'slave') or (get_mode == 'Slave'):
                        switchCmd = cmd + ' reset master'
                        if 'bmc' in option:
                            self.wpl_transmit(switchCmd)
                            time.sleep(10)
                            kernel_info = 'Starting kernel ...'
                            self.wpl_receive(kernel_info, timeout=350)
                            time.sleep(100)
                            self.wpl_getPrompt('openbmc', timeout=BOOTING_TIME)
                        else:
                            self.wpl_transmit(switchCmd)
                            time.sleep(10)
                            booting_msg = 'Power reset microserver'
                            cmd1 = 'wedge_power.sh reset'
                            self.wpl_transmit(cmd1)
                            self.wpl_receive(booting_msg, timeout=Const.BOOTING_TIME)
                            time.sleep(3)
                            self.wpl_getPrompt(Const.BOOT_MODE_CENTOS, timeout=Const.BOOTING_TIME)
                            self.wpl_getPrompt(Const.BOOT_MODE_OPENBMC)
                            time.sleep(10)
                        output = self.wpl_execute(cmd, mode=openbmc_mode, timeout=180)
                        for line in output.splitlines():
                            line = line.strip()
                            match = re.search(pattern, line, re.IGNORECASE)
                            if match:
                                current_mode = match.group(1)
                                if current_mode == 'Master' or current_mode == 'master':
                                    self.wpl_log_success('Successfully current mode is %s'%(res.group(1)))
                                else:
                                    count_error += 1
                                    self.wpl_log_fail("Error switch mode fail")
        if (count_error > 0):
            self.wpl_raiseException("Failed run_check_bmc_or_bios_master_status.")

#######################################################################################################################
    @logThis
    def run_copy_image_file(self, image, eth_tool, dhcp_tool, scp_ip, usrname, pasrd, host_path, local_path, ImageLst):
        #1. check the ipv6 address
        self.get_ipv6_address(eth_tool, dhcp_tool)
        time.sleep(5)
        #2. check local folder
        cmd = 'ls ' + local_path[:11]
        output = self.wpl_execute(cmd, mode=None, timeout=180)
        match = re.search(image, output)
        if match:
            self.wpl_log_info('%s folder has existence.'% image)
        else:
            cmd = 'mkdir ' + local_path[:11] + image
            self.wpl_execute(cmd, mode=None, timeout=180)
        #3. copy image
        for item in ImageLst:
            self.wpl_log_info("////host path = %s " % host_path)
            self.wpl_log_info("////local_path = %s " % local_path)
            time.sleep(5)
            cmd = 'scp -6 -r ' + usrname + '@' + '[' + scp_ip + ']' + ':' + host_path + '/' + item + ' ' + local_path
            self.wpl_transmit(cmd)
            promptList = ["(yes/no)", "password:"]
            patternList = re.compile('|'.join(promptList))
            output1 = self.device.read_until_regexp(patternList, 200)
            match1 = re.search("(yes/no)", output1)
            match3 = re.search("password:", output1)
            if match1:
                self.device.transmit("yes")
                self.device.receive("password:")
                self.device.transmit("%s" % pasrd)
            elif match3:
                self.device.transmit("%s" % pasrd)
            else:
                self.wpl_log_fail("pattern mismatch")
            CurPromptStr = self.device.getCurrentPromptStr()
            CurPromptStr = CurPromptStr if CurPromptStr else "100%|No such file"
            output = self.device.read_until_regexp(CurPromptStr, timeout=90)
            p0 = ".*100\%"
            p1 = "No such file or directory"
            if re.search(p0, output):
                self.wpl_log_success("Successfully copy file: %s" % (item))
            elif re.search(p1, output):
                self.wpl_log_fail("%s" % (p1))
                self.wpl_raiseException("Failed run_copy_image_file.")

#######################################################################################################################
    @logThis
    def run_check_all_fw_version(self, toolName, option, all_pattern, all_expect):
        all_cmd = toolName + ' ' +  option
        count_error = 0
        getDict = {}
        output = self.wpl_execute(all_cmd, mode=None, timeout=180)
        for line in output.splitlines():
            line = line.strip()
            for value in all_pattern:
                match = re.search(value, line)
                if match:
                    getVerKey = match.group(1)
                    getVerValue = match.group(2)
                    getDict[getVerKey] = getVerValue

        for key, value in getDict.items():
            if all_expect[key] == value:
                self.wpl_log_success('Successfully expect [%s] value is %s' % (key, value))
            else:
                count_error += 1
                self.wpl_log_fail("Error: the [%s] version is diff, get_version: %s, expect_version: %s" % (key, value, all_expect[key]))
        if (count_error > 0):
            self.wpl_raiseException("Failed run_current_version_check_in_bmc_side.")

#######################################################################################################################
    @logThis
    def run_fw_online_update_check(self, image, toolName, toolLst, imageLst, option, imagePath, pattern, expect, exec_mode=default_mode, logFile='None'):
        passCount = 0
        errCount = 0
        currentVerDict = {}
        patternNum = len(pattern)
        devicename = os.environ.get("deviceName", "")
        cmd = 'cd ' + imagePath
        self.wpl_getPrompt(exec_mode, 600)
        self.wpl_transmit(cmd)
        ## First check fw version, then update fw.
        p1 = r'(.*):[ \t]+(.*)'
        output = self.wpl_execute(toolName, mode=exec_mode, timeout=1800)
        for line in output.splitlines():
            line = line.strip()
            match = re.search(p1, line)
            if match:
                keyName = match.group(1)
                valueName = match.group(2)
                currentVerDict[keyName] = valueName
        for key, value in currentVerDict.items():
            if expect[key] == value:
                self.wpl_log_info('The version is same, not need to update!')
            else:
                self.wpl_log_info('#### %s version is diff, need to update, getVer is %s, expectVer is %s ####'%(key, value, expect[key]))
                if image == 'CPLD':
                    if 'wedge400' in devicename.lower():
                        if key == 'SMB_SYSCPLD':
                            cmd = toolLst[0] + ' ' + imagePath + '/' + imageLst[0] + ' ' + option
                        elif key == 'FCMCPLD':
                            cmd = toolLst[1] + ' ' + imagePath + '/' + imageLst[1] + ' ' + option
                        elif key == 'SMB_PWRCPLD':
                            cmd = toolLst[2] + ' ' + imagePath + '/' + imageLst[2] + ' ' + option
                        elif key == 'SCMCPLD':
                            cmd = toolLst[3] + ' ' + imagePath + '/' + imageLst[3] + ' ' + option
                    elif 'minipack2' in devicename.lower():
                        if key == "SMBCPLD":
                            cmd = toolLst[0] + ' ' + "SMB -f " + imagePath + '/' + imageLst[0] + ' ' + option
                        elif key == "FCMCPLD B":
                            cmd = toolLst[0] + ' ' + "FCM-B -f " + imagePath + '/' + imageLst[1] + ' ' + option
                        elif key == "FCMCPLD T":
                            cmd = toolLst[0] + ' ' + "FCM-T -f " + imagePath + '/' + imageLst[1] + ' ' + option
                        elif key == "PWRCPLD L":
                            cmd = toolLst[0] + ' ' + "PWR-L -f " + imagePath + '/' + imageLst[2] + ' i2c'
                        elif key == "PWRCPLD R":
                            cmd = toolLst[0] + ' ' + "PWR-R -f " + imagePath + '/' + imageLst[2] + ' i2c'
                        elif key == "SCMCPLD":
                            cmd = toolLst[0] + ' ' + "SCM -f " + imagePath + '/' + imageLst[3] + ' ' + option
                elif image == 'FPGA':
                    if 'wedge400' in devicename.lower():
                        if key == 'DOMFPGA1':
                            cmd = toolLst[0] + ' ' + imagePath + '/' + imageLst[0]
                        elif key == 'DOMFPGA2':
                            return 'pass'
                            #cmd = toolLst[1] + ' ' + imagePath + '/' + imageLst[0]
                    elif 'minipack2' in devicename.lower():
                        if (key == 'IOB FPGA'):
                            cmd = toolLst[2] + ' ' + imagePath + '/' + imageLst[1]
                        elif (key == 'PIM1 DOMFPGA'):
                            pattern = ['done']
                            cmd = toolLst[0] + ' ' + imagePath + '/' + imageLst[0]
                            cmd += "; sleep 35; "
                            cmd += toolLst[1]
                        elif (key == 'PIM2 DOMFPGA') or (key == 'PIM3 DOMFPGA') or (key == 'PIM4 DOMFPGA') or \
                                (key == 'PIM5 DOMFPGA') or (key == 'PIM6 DOMFPGA') or (key == 'PIM7 DOMFPGA') or (key == 'PIM8 DOMFPGA'):
                            return 'pass'
                self.wpl_log_info('[command = %s]' % cmd)
                output = self.wpl_execute(cmd, mode=exec_mode, timeout=1800)
                for line in output.splitlines():
                    line = line.strip()
                    for i in range(0, patternNum):
                        match = re.search(pattern[i], line, re.IGNORECASE)
                        if match:
                            passCount += 1
                if logFile != 'None':
                    self.wpl_send_output_to_log_file(output, logFile)
                if passCount == patternNum:
                    passCount = 0
                    self.wpl_log_success("Successfully update the [%s] fw"%key)
                    if 'pim_upgrade' in cmd:
                        output1 = self.wpl_execute(toolName, mode=exec_mode, timeout=180)
                        for line in output1.splitlines():
                            line = line.strip()
                            match1 = re.search(p1, line)
                            if match1:
                                keyName = match1.group(1)
                                valueName = match1.group(2)
                                if keyName == "IOB FPGA":
                                    continue
                                else:
                                    currentVerDict[keyName] = valueName
                        for k, v in currentVerDict.items():
                            if k == "IOB FPGA":
                                continue
                            elif expect[k] == v:
                                self.wpl_log_success("Successfully get the [%s] version is [%s]" % (k, v))
                            else:
                                errCount += 1
                                self.wpl_log_fail('Failed get the %s fw' % k)
                else:
                    errCount += 1
                    self.wpl_log_fail('Failed update the %s fw'%key)
        if errCount > 0:
            self.wpl_raiseException("Failed run_fw_online_update_check")
        else:
            return 'pass'

#######################################################################################################################
    @logThis
    def run_verify_cpld_update_version(self, toolName, pattern, expect):
        getVerDict = {}
        errCount = 0
        self.wpl_log_info('#### [command = %s] ####' % toolName)
        output = self.wpl_execute(toolName, mode=openbmc_mode, timeout=180)
        for line in output.splitlines():
            line = line.strip()
            match = re.search(pattern, line)
            if match:
                keyName = match.group(1)
                valueName = match.group(2)
                getVerDict[keyName] = valueName
        for key, value in getVerDict.items():
            if expect[key] == value:
                self.wpl_log_success("Successfully get the %s fw is %s" % (key, value))
            else:
                errCount += 1
                self.wpl_log_fail('Failed get version is %s, expect version is %s' % (value, expect[key]))
        if errCount > 0:
            self.wpl_raiseException("Failed run_verify_cpld_update_version")

#######################################################################################################################
    @logThis
    def run_come_side_idle_check(self, toolName, option):
        cmd = toolName + ' ' + option
        output = self.wpl_execute(cmd, mode=None, timeout=1800)

#######################################################################################################################
    @logThis
    def run_check_system_idle_test(self, toolName, log_path, stress_time):
        pass_count = 0
        cmd = 'cd /home'
        p1 = r'\[root@(localhost|fb\w+)[ \t]+home\]#'
        pathCmd = 'cd ' + log_path
        self.wpl_sendline('\n')
        self.wpl_transmit(cmd)
        #self.wpl_flush()
        time.sleep(int(stress_time))
        self.wpl_getPrompt(mode='openbmc')
        self.wpl_transmit(pathCmd)
        output = self.wpl_execute(toolName, mode=None, timeout=1800)
        for line in output.splitlines():
            line = line.strip()
            match = re.search(p1, line)
            if match:
                pass_count += 1
                self.wpl_log_success("Successfully match the home path.")
        if pass_count == 0:
            self.wpl_raiseException("Failed run_check_system_idle_test")

#######################################################################################################################
    @logThis
    def run_check_some_log_files(self, status, toolName, option, stress_time, mce_tool, dmesg_tool, log_path):
        p1 = '^0'
        p2 = 'stress:[ \t]+info:[ \t]+\[\d+\][ \t]+successful run completed in[ \t]+\d+s'
        #p3 = '\[\d\]\+?[ \t]+Done[ \t]+stressapptest -s \d+ -m 8 -i 8 -C 8 -M -l'
        p3 = '\[\d\]\+?[ \t]+Done[ \t]+stressapptest\s+-s'
        pass_count = 0
        pattern_count = 0
        mceCmd = log_path + mce_tool
        dmesgCmd = log_path + dmesg_tool
        clearToolLst = [mceCmd, dmesgCmd]
        if status == 'False':
            self.wpl_log_info('#### First clear the log, then run stress test. ####')
            for i in clearToolLst:
                clearCmd = 'echo 0 > ' + i
                self.wpl_execute(clearCmd, mode=None, timeout=60)
                time.sleep(2)
        elif status == 'True':
            stressAppCmd = toolName + ' -s ' + stress_time + option
            stressCmd = 'stress --cpu 8 --timeout ' + stress_time
            self.wpl_execute(stressAppCmd, mode=None, timeout=8000)
            time.sleep(5)
            self.wpl_transmit('\n')
            output = self.wpl_execute(stressCmd, mode=None, timeout=8000)
            for line in output.splitlines():
                line = line.strip()
                match1 = re.search(p2, line)
                match2 = re.search(p3, line)
                if match1:
                    pattern_count += 1
                    self.wpl_log_success("Successfully run stress cpu test.")
                if match2:
                    pattern_count += 1
                    self.wpl_log_success("Successfully run stressapp test.")
            if pattern_count == 2:
                self.wpl_log_success("Successfully run stress test.")
            else:
                self.wpl_raiseException("Failed run stress test.")
        ##check log result:
        for i in clearToolLst:
            catcmd = 'cat ' + i
            output = self.wpl_execute(catcmd, mode=None, timeout=180)
            for line in output.splitlines():
                line = line.strip()
                match = re.search(p1, line)
                if match:
                    pass_count += 1
                    self.wpl_log_info("Passed to check the log file.")
        if pass_count == 2:
            self.wpl_log_success("Successfully check the log file.")
        else:
            self.wpl_raiseException("Failed run_check_some_log_files")

#######################################################################################################################
    @logThis
    def run_check_sdk_result_and_exit_w400(self, sdk_env, sdkToolPath, stopTrafficLst, counterTool, rpkt_pattern, tpkt_pattern, exitSdkTool):
        error_count = 0
        CommonLib.change_dir(sdkToolPath)
        self.wpl_log_info('#### stop traffic test ####')
        for cmd in stopTrafficLst:
            self.wpl_execute(cmd, mode=None, timeout=180)
        self.wpl_transmit(truncateTool)
        self.wpl_transmit('\n')
        self.wpl_log_info('#### counter traffic result ####')
        self.wpl_transmit(counterTool)
        output = self.wpl_execute('cat temp.txt', mode=None, timeout=180)
        rp_lst = re.findall(rpkt_pattern, output)
        tp_lst = re.findall(tpkt_pattern, output)
        rp_len = len(rp_lst)
        tp_len = len(tp_lst)
        ##1. counter match the port number
        if (rp_len == 48) and (tp_len == 48):
            self.wpl_log_info('match the port num is [%s]'%rp_len)
        ##2. check the value left and right
        counter_lst = [rp_lst, tp_lst]
        for k in counter_lst:
            for tup in k:
                if tup[0] == tup[1]:
                    self.wpl_log_info('Successfully left and right value is the same!')
                else:
                    error_count += 1
                    self.wpl_log_fail('Failed left value [%s] != right value [%s]'%(tup[0], tup[1]))
        ##3. check all port CDMIB_RPKT and CDMIB_TPKT value
        for i in range(rp_len):
            if rp_lst[i] == tp_lst[i]:
                self.wpl_log_info('Successfully CDMIB_RPKT and CDMIB_TPKT value is the same!')
            else:
                error_count += 1
                self.wpl_log_fail('Failed CDMIB_RPKT value [%s] != CDMIB_TPKT value [%s]' % (rp_lst[i], tp_len[i]))
        ##4. exit sdk env
        self.wpl_execute(exitSdkTool, mode=None, timeout=180)
        self.wpl_transmit('rm temp.txt')
        if error_count > 0:
            self.wpl_raiseException("Failed run_check_sdk_result_and_exit_w400") 

#######################################################################################################################
    @logThis
    def run_check_sdk_result_and_exit_mp2(self, sdk_env, sdkToolPath, stopTraffic_lst, pattern):
        count = 0
        CommonLib.change_dir(sdkToolPath)
        if sdk_env == 'background':
            self.wpl_log_info('#### stop traffic, then counter data test ####')
            stopCmd = './' + stopTraffic_lst[0] + ' ' + stopTraffic_lst[1]
            clearCmd = stopTraffic_lst[2]
            echoCmd = './' + stopTraffic_lst[0] + ' echo'
            counterCmd = './' + stopTraffic_lst[0] + ' ' + stopTraffic_lst[3]
            tempCmd = './' + stopTraffic_lst[0] + ' -'
            snake_lst = [stopCmd, clearCmd, echoCmd, counterCmd, tempCmd, stopTraffic_lst[5]]
            for cmd in snake_lst:
                time.sleep(3)
                output = self.wpl_execute(cmd, mode=None, timeout=300)
            for line in output.splitlines():
                line = line.strip()
                match = re.search(pattern, line)
                if match:
                    count += 1
            if count == 128:
                self.wpl_log_success("Successfully counter the sdk traffic.")
            else:
                self.wpl_raiseException("Failed run_check_sdk_result_and_exit_mp2")
            ## exit sdk env:
            cmd = './' + stopTraffic_lst[0] + ' exit'
            self.wpl_execute(cmd, mode=None, timeout=180)
            self.wpl_transmit('rm temp.txt')

#######################################################################################################################
    @logThis
    def run_check_sdk_result_and_exit_w400c(self, sdk_env, toolName, pattern):
        pass_count = 0
        if sdk_env == 'background':
            output = self.wpl_execute(toolName, mode=None, timeout=300)
            for line in output.splitlines():
                line = line.strip()
                match = re.search(pattern, line)
                if match:
                    pass_count += 1
            if pass_count == 1:
                self.wpl_log_success("Successfully counter the sdk traffic.")
            else:
                self.wpl_raiseException("Failed run_check_sdk_result_and_exit_w400c")

#######################################################################################################################
    @logThis
    def run_check_sol_stress_test(self, toolName, option, path, bmc_path, bmc_log):
        error_count = 0
        cmd = toolName + ' ' + path + '/' + option
        self.wpl_execute(cmd, mode=None, timeout=30)
        come_path = 'ls ' + path
        output = self.wpl_execute(come_path, mode=None, timeout=30)
        match = re.search(option, output)
        if match:
            self.wpl_log_success("Successfully find the test.log file in COMe side.")
            CommonLib.switch_to_openbmc()
            output1 = self.wpl_execute(bmc_path, mode=None, timeout=30)
            match1 = re.search(bmc_log, output1)
            if match1:
                self.wpl_log_success("Successfully find the mTerm_wedge.log file in bmc side.")
            else:
                error_count += 1
                self.wpl_log_fail('Do not find the mTerm_wedge.log file.')
        else:
            error_count += 1
            self.wpl_log_fail('Do not find the test.log file.')
        if error_count > 0:
            self.wpl_raiseException("Failed run_create_a_test_log_file_in_come_side")

#######################################################################################################################
    @logThis
    def run_clean_log_file(self, path, file, toolName):
        cmd = toolName + ' ' + path + '/' + file
        self.wpl_execute(cmd, mode=None, timeout=30)

#######################################################################################################################
    @logThis
    def run_init_sdk_check_w400(self, toolName, option, toolPath, toolLst):
        CommonLib.change_dir(toolPath)
        self.check_and_terminate_sdk_tool_process(toolLst[0])
        error_count = 0
        p1 = '^\d+'
        time.sleep(2)
        sdkIntCmd = './' + toolName + option
        portCmd = './' + toolLst[2] + ' ps cd'
        portUpCmd = toolLst[1] + " |grep -a cd |grep up|awk -F'[(]' '{print $1}'|wc |awk '{print $1}'"
        InitCmdLst = [sdkIntCmd, toolLst[1], toolLst[3], portCmd, portUpCmd]
        for cmd in InitCmdLst:
            time.sleep(3)
            output = self.wpl_execute(cmd, mode=None, timeout=60)
        for line in output.splitlines():
            line = line.strip()
            res = re.search(p1, line)
            if res:
                if int(res.group(0)) == 48:
                    self.wpl_log_info('All port is up status!')
                else:
                    error_count += 1
                    self.wpl_log_fail("Found port have down status")
        ##. clear log
        self.wpl_execute(toolLst[-1], mode=None, timeout=60)
        if error_count > 0:
            self.wpl_raiseException('Failed run_init_sdk_check_w400')

#######################################################################################################################
    @logThis
    def run_init_sdk_check(self, toolName, option, toolPath, toolLst):
        error_count = 0
        p1 = 'gb_parinit pim8 ret 0'
        p2 = '^cd\d{1,2}\(.*\)[ \t]+up.*'
        p3 = '^\d+'
        CommonLib.change_dir(toolPath)
        ##1. check the bcm.user in background and delete temp.txt log first
        self.wpl_transmit('rm temp.txt > /dev/null')
        self.check_and_terminate_sdk_tool_process(toolLst[0])
        ##2. init mp2 sdk
        xphybackCmd = './' + toolLst[1] + ' &'
        initCmd = './' + toolLst[2] + ' ' + toolLst[3]
        initCmdLst = [xphybackCmd, initCmd]
        for cmd in initCmdLst:
            time.sleep(3)
            output = self.wpl_execute(cmd, mode=None, timeout=600)
        for line in output.splitlines():
            line = line.strip()
            res = re.search(p1, line)
            if res:
                self.wpl_log_success('Successfully run sdk init!')
        ##3. run sdk:
        autoLoadCmd = './' + toolName + option
        portCmd = './' + toolLst[-1] + ' ps cd'
        runCmdLst = [autoLoadCmd, toolLst[4], toolLst[5], portCmd]
        for cmd in runCmdLst:
            self.wpl_execute(cmd, mode=None, timeout=180)
            time.sleep(5)
            self.wpl_transmit('\n')
            self.wpl_receive(self.device.promptDiagOS, timeout=90)
            # self.wpl_flush()
        self.wpl_execute(toolLst[4], mode=None, timeout=60)
        portUpCmd = toolLst[4] + " |egrep -a 'cd.*\(' |grep -c 'up'"
        output = self.wpl_execute(portUpCmd, mode=None, timeout=80)
        for line in output.splitlines():
            line = line.strip()
            res = re.search(p3, line)
            if res:
                if int(res.group(0)) == 128:
                    self.wpl_log_info('All port is up status!')
                else:
                    error_count += 1
                    self.wpl_log_fail("Found port have down status")
        if error_count > 0:
            self.wpl_raiseException('Failed run_init_sdk_check')

#######################################################################################################################
    @logThis
    def run_check_reset_port_link_test(self, clsTool, option, stress_time, toolLst):
        p1 = '^\d+'
        p2 = '^PASSED'
        error_count = 0
        pass_count = 0
        ##1. reset PMD
        self.wpl_log_info('****** run sdk reset PMD command ******')
        reset_cmd = './' + clsTool + ' ' + option
        self.wpl_execute(reset_cmd, mode=None, timeout=180)
        ##2. run sdk
        echoCmd = './' + clsTool + ' echo'
        pscdCmd = './' + clsTool + ' ps cd'
        portUpCmd = toolLst[0] + " |egrep -a 'cd.*\(' |grep -c 'up'"
        sdkCmdLst = [toolLst[4], echoCmd, pscdCmd, toolLst[0], portUpCmd]
        for cmd in sdkCmdLst:
            time.sleep(2)
            output = self.wpl_execute(cmd, mode=None, timeout=120)
        for line in output.splitlines():
            line = line.strip()
            res = re.search(p1, line)
            if res:
                if int(res.group(0)) == 128:
                    self.wpl_log_info('All port is up status!')
                else:
                    error_count += 0
                    self.wpl_log_fail("Found port have down status")
        ##3. run traffic
        vlanCmd = './' + clsTool + ' ' + toolLst[1]
        clearCmd = './' + clsTool + ' clear c'
        trafficCmd = './' + clsTool + ' ' + toolLst[2]
        trafficTime = 'sleep ' + stress_time
        stratTrafficCmdLst = [vlanCmd, clearCmd, trafficCmd, trafficTime]
        for cmd in stratTrafficCmdLst:
            time.sleep(3)
            self.wpl_execute(cmd, mode=None, timeout=900)
        ##4. stop traffic and counter the data
        stopCmd = './' + clsTool + ' ' + toolLst[3]
        counterCmd = './' + clsTool + ' ' + toolLst[5]
        waitCmd = './' + clsTool + ' - > /dev/null'
        resultCmd = toolLst[0] + " |grep 'port counters check test' |awk '{print $5}'"
        counterDataCmdLst = [stopCmd, toolLst[4], echoCmd, counterCmd, waitCmd, toolLst[0], resultCmd]
        for cmd in counterDataCmdLst:
            time.sleep(3)
            output = self.wpl_execute(cmd, mode=None, timeout=900)
        for line in output.splitlines():
            line = line.strip()
            res = re.search(p2, line)
            if res:
                pass_count += 1
                self.wpl_log_success('Successfully counter the sdk traffic')
        ##5. exit sdk env
        #self.wpl_execute(toolLst[-1], mode=None, timeout=90)
        #self.wpl_transmit('rm temp.txt > /dev/null')
        if (error_count > 0) or (pass_count <= 0):
            self.wpl_raiseException("Failed run_check_reset_port_link_test")

#######################################################################################################################
    @logThis
    def run_check_reset_port_link_test_w400(self, clsTool, option, stress_time, toolLst):
        p1 = '^\d+'
        error_count = 0
        ##1. reset PMD
        self.wpl_log_info('****** run sdk reset PMD command ******')
        reset_cmd = './' + clsTool + ' ' + option
        self.wpl_execute(reset_cmd, mode=None, timeout=180)
        ##2. run sdk
        echoCmd = './' + clsTool + ' echo'
        pscdCmd = './' + clsTool + ' ps cd'
        portUpCmd = toolLst[0] + " |grep -a cd |grep 'up'|awk -F'[(]' '{print $1}'|wc |awk '{print $1}'"
        sdkCmdLst = [toolLst[1], echoCmd, pscdCmd, toolLst[0], portUpCmd]
        for cmd in sdkCmdLst:
            time.sleep(2)
            output = self.wpl_execute(cmd, mode=None, timeout=120)
        for line in output.splitlines():
            line = line.strip()
            res = re.search(p1, line)
            if res:
                if int(res.group(0)) == 48:
                    self.wpl_log_info('All port is up status!')
                else:
                    error_count += 1
                    self.wpl_log_fail("Found port have down status")
        ##3. run traffic
        vlanCmd = './' + clsTool + ' ' + toolLst[2]
        clearCmd = './' + clsTool + ' clear c'
        trafficDDCmd = './' + clsTool + ' ' + toolLst[3]
        traffic56Cmd = './' + clsTool + ' ' + toolLst[4]
        trafficTime = 'sleep ' + stress_time
        stratTrafficCmdLst = [vlanCmd, clearCmd, trafficDDCmd, traffic56Cmd, trafficTime]
        for cmd in stratTrafficCmdLst:
            time.sleep(3)
            self.wpl_execute(cmd, mode=None, timeout=900)
        ##4. stop traffic and counter the data
        stopCmd = './' + toolLst[5]
        counterDataCmdLst = [stopCmd, toolLst[1], echoCmd, toolLst[6], toolLst[0]]
        for cmd in counterDataCmdLst:
            time.sleep(3)
            output = self.wpl_execute(cmd, mode=None, timeout=900)
        rp_lst = re.findall(toolLst[-2], output)
        tp_lst = re.findall(toolLst[-1], output)
        rp_len = len(rp_lst)
        tp_len = len(tp_lst)
        ##counter match the port number
        if (rp_len == 48) and (tp_len == 48):
            self.wpl_log_info('match the port num is [%s]' % rp_len)
        ##check the value left and right
        counter_lst = [rp_lst, tp_lst]
        for k in counter_lst:
            for tup in k:
                if tup[0] == tup[1]:
                    self.wpl_log_info('Successfully TX and RX value is the same!')
                else:
                    error_count += 1
                    self.wpl_log_fail('Failed TX value [%s] != RX value [%s]' % (tup[0], tup[1]))
        ##check all port CDMIB_RPKT and CDMIB_TPKT value
        for i in range(rp_len):
            if rp_lst[i] == tp_lst[i]:
                self.wpl_log_info('Successfully CDMIB_RPKT and CDMIB_TPKT value is the same!')
            else:
                error_count += 1
                self.wpl_log_fail('Failed CDMIB_RPKT value [%s] != CDMIB_TPKT value [%s]' % (rp_lst[i], tp_len[i]))
        ##5. exit sdk env
        #self.wpl_execute(toolLst[-3], mode=None, timeout=180)
        #self.wpl_transmit('rm temp.txt > /dev/null')
        if error_count > 0:
            self.wpl_raiseException("Failed run_check_reset_port_link_test_w400")

#######################################################################################################################
    @logThis
    def run_check_iperf_tool(self, toolName, iperfTool, username, password, server_ip, filePath, path):
        cmd = toolName + path
        output = self.wpl_execute(cmd, mode=None, timeout=180)
        match = re.search('iperf', output)
        if match:
            self.wpl_log_success('Successfully check iperf tool in home folder.')
        else:
            self.wpl_log_info('Need to copy the iperf tool from server side.')
            CommonLib.copy_files_through_scp(Const.DUT, username, password, server_ip, iperfTool, filePath, path)

#######################################################################################################################
    @logThis
    def ssh_login_server_side(self, username, passwd, host_ip, host_prompt):
        server_prompt = host_prompt[4:]
        cmd = 'ssh ' + username + '@' + host_ip
        self.device.sendCmd(cmd)
        promptList = ["(y/n)", "(yes/no)", "password:"]
        patternList = re.compile('|'.join(promptList))
        output = self.device.read_until_regexp(patternList, 120)
        if re.search("(y/n)", output):
            self.device.sendCmd("yes")
            self.device.read_until_regexp("password:")
            self.device.sendCmd(passwd)
            self.device.read_until_regexp(server_prompt)
        elif re.search("(yes/no)", output):
            self.device.sendCmd("yes")
            self.device.read_until_regexp("password:")
            self.device.sendCmd(passwd)
            self.device.read_until_regexp(server_prompt)
        elif re.search("password:", output):
            self.device.sendCmd(passwd)
            self.device.read_until_regexp(server_prompt)
        else:
            self.wpl_log_fail("pattern mismatch")
        self.device.sendline('\n')

#######################################################################################################################
    @logThis
    def run_check_cpu_mgmt_port_test(self, toolName, server_option, stress_time, serverToolLst):
        error_count = 0
        unitCmd = './' + toolName + ' -c ' + serverToolLst[2] + ' -p 12345 -i 1 -t ' + stress_time + ' -P 2'
        serverCmd = './' + toolName + server_option + ' > temp.txt &'
        switchPath = 'cd /home'
        delLogCmd = 'rm -rf temp.txt > /dev/null'
        ##1. login server, then run iperf
        self.ssh_login_server_side(serverToolLst[0], serverToolLst[1], serverToolLst[2], serverToolLst[3])
        self.device.sendline(switchPath)
        self.device.sendline(delLogCmd)
        self.device.sendCmd(serverCmd)
        time.sleep(2)
        self.device.sendline('exit')
        ##2. run iperf in unit
        self.wpl_transmit(switchPath)
        output = self.wpl_execute(unitCmd, mode=None, timeout=21800)
        ##3. check the client speed
        p1 = '\[SUM\]  0\.0\-21600\.0 sec.+GBytes[ \t]+(\d+) Mbits/sec'
        p2 = '^\d+'
        for line in output.splitlines():
            line = line.strip()
            res = re.search(p1, line)
            if res:
                if int(res.group(1)) > 900:
                    self.wpl_log_info('Successfully the client side iperf.')
                else:
                    error_count += 1
                    self.wpl_log_fail('Failed client side.')
        time.sleep(2)
        ##4. check server side speed
        catCmd = 'cat temp.txt'
        serverValue = "cat temp.txt |grep  '\[SUM\]  0.0-21600.0' |awk '{print $6}'"
        self.ssh_login_server_side(serverToolLst[0], serverToolLst[1], serverToolLst[2], serverToolLst[3])
        self.device.sendline(switchPath)
        self.device.sendCmd(catCmd)
        time.sleep(2)
        output = self.device.executeCmd(serverValue)
        for line in output.splitlines():
            line = line.strip()
            res = re.search(p2, line)
            if res:
                if int(res.group(0)) > 900:
                    self.wpl_log_info('Successfully the server side iperf.')
                else:
                    error_count += 1
                    self.wpl_log_fail('Failed server side.')
        self.device.sendCmd('exit')
        if error_count > 0:
            self.wpl_raiseException("Failed run_check_cpu_mgmt_port_test")

#######################################################################################################################
    @logThis
    def run_exit_sdk_env_test(self, clearTool, exit_sdk_tool):
        cmdToolLst = [clearTool, exit_sdk_tool]
        for cmd in cmdToolLst:
            self.wpl_execute(cmd, mode=None, timeout=180)

#######################################################################################################################
    @logThis
    def run_check_qsfp_on_or_off_test(self, toolName, optionLst):
        lpmodeCmd = './' + toolName + ' ' + optionLst[0]
        resetOnCmd = './' + toolName + ' ' + optionLst[1]
        resetOffCmd = './' + toolName + ' ' + optionLst[2]
        toolCmdLst = [lpmodeCmd, resetOnCmd, resetOffCmd]
        for cmd in toolCmdLst:
            time.sleep(5)
            self.wpl_execute(cmd, mode=None, timeout=180)

#######################################################################################################################
    @logThis
    def run_init_sdk_from_remote_shell(self, toolName, option, BCMTool, clsTool, clearTool, psceTool, TailTool, sdkPath, pattern):
        p1 = '^\d+'
        error_count = 0
        CommonLib.change_dir(sdkPath)
        #1. check bcm.user and cel_shell in background first
        self.check_and_terminate_sdk_tool_process(BCMTool)
        time.sleep(2)
        self.check_and_terminate_sdk_tool_process(clsTool)
        #2. init sdk
        initCmd = './' + toolName + ' ' + option
        psceCmd = './' + clsTool + ' ' + psceTool
        catTool = 'cat temp.txt'
        var_upPort = 'tail -n +3 temp.txt ' + pattern
        cmdLst = [initCmd, catTool, clearTool, psceCmd, TailTool, var_upPort]
        for cmd in cmdLst:
            time.sleep(2)
            output = self.wpl_execute(cmd, mode=None, timeout=800)
        for line in output.splitlines():
            line = line.strip()
            res = re.search(p1, line)
            if res:
                if int(res.group(0)) == 48:
                    self.wpl_log_info('Successfully match up port number.')
                else:
                    error_count += 1
                    self.wpl_log_fail('Failed have port down.')
        self.wpl_execute(clearTool, mode=None, timeout=800)
        if error_count > 0:
            self.wpl_raiseException("Failed run_init_sdk_from_remote_shell")

#######################################################################################################################
    @logThis
    def run_init_sdk_and_low_power_mode(self, toolLst, pathLst, lpmodeTool, pattern):
        p1 = '^\d+'
        error_count = 0
        #1. switch to centos, then check lpmode
        CommonLib.change_dir(pathLst[1])
        qsfpTool = './' + toolLst[-1] + ' ' + lpmodeTool
        self.wpl_transmit(qsfpTool)
        time.sleep(5)
        #2. run lpmode, check port status
        CommonLib.change_dir(pathLst[0])
        echoCmd = './' + toolLst[0] + ' ' + toolLst[4]
        psceCmd = './' + toolLst[0] + ' ' + toolLst[2]
        offPort = 'tail -n +3 temp.txt ' + pattern
        cmdToolLst = [toolLst[1], echoCmd, psceCmd, toolLst[3], offPort]
        for cmd in cmdToolLst:
            output = self.wpl_execute(cmd, mode=None, timeout=800)
        for line in output.splitlines():
            line = line.strip()
            res = re.search(p1, line)
            if res:
                if int(res.group(0)) == 48:
                    self.wpl_log_info('Successfully match port number.')
                else:
                    error_count += 1
                    self.wpl_log_fail('Failed match error, get num is %s, expect is %d.'%(res.group(0), 48))
        self.wpl_execute(toolLst[1], mode=None, timeout=800)
        if error_count > 0:
            self.wpl_raiseException("Failed run_init_sdk_from_remote_shell")

#######################################################################################################################
    @logThis
    def run_check_sdk_traffic_test(self, clsTool, option, stress_time, toolLst):
        error_count = 0
        #1. set vlan, then traffic
        vlanCmd = './' + clsTool + ' ' + option
        clearCmd = './' + clsTool + ' clear c'
        trafficCmd = './' + clsTool + ' ' + toolLst[2]
        runTime = 'sleep ' + str(stress_time)
        stopTraffic = './' + clsTool + ' ' + toolLst[3]
        echoCmd = './' + clsTool + ' ' + toolLst[4]
        trafficCmdLst = [vlanCmd, clearCmd, trafficCmd, runTime, stopTraffic, toolLst[1], echoCmd, toolLst[5]]
        for cmd in trafficCmdLst:
            time.sleep(5)
            output = self.wpl_execute(cmd, mode=None, timeout=8000)
        #2. check counter result
        rp_lst = re.findall(toolLst[-2], output)
        tp_lst = re.findall(toolLst[-1], output)
        rp_len = len(rp_lst)
        tp_len = len(tp_lst)
        ##counter match the port number
        if (rp_len == 48) and (tp_len == 48):
            self.wpl_log_info('match the port num is [%s]' % rp_len)
        ##check the value left and right
        counter_lst = [rp_lst, tp_lst]
        for k in counter_lst:
            for tup in k:
                if tup[0] == tup[1]:
                    self.wpl_log_info('Successfully TX and RX value is the same!')
                else:
                    error_count += 1
                    self.wpl_log_fail('Failed TX value [%s] != RX value [%s]' % (tup[0], tup[1]))
        ##check all port CDMIB_RPKT and CDMIB_TPKT value
        for i in range(rp_len):
            if rp_lst[i] == tp_lst[i]:
                self.wpl_log_info('Successfully CDMIB_RPKT and CDMIB_TPKT value is the same!')
            else:
                error_count += 1
                self.wpl_log_fail('Failed CDMIB_RPKT value [%s] != CDMIB_TPKT value [%s]' % (rp_lst[i], tp_len[i]))
        #3. clear temp.txt log
        self.wpl_execute(toolLst[1], mode=None, timeout=80)
        if error_count > 0:
            self.wpl_raiseException("Failed run_check_sdk_traffic_test")

#######################################################################################################################
    @logThis
    def run_mp2_sdk_init_quick(self, bcmTool, xphybackTool, xphyTool, init_options, sdkPath):
        p1 = 'gb_parinit pim8 ret 0'
        CommonLib.change_dir(sdkPath)
        ##1. check the bcm.user in background first.
        self.check_and_terminate_sdk_tool_process(bcmTool)
        ##2. init mp2 sdk
        xphybackCmd = './' + xphybackTool + ' &'
        initCmd = './' + xphyTool + ' ' + init_options
        initCmdLst = [xphybackCmd, initCmd]
        for cmd in initCmdLst:
            time.sleep(3)
            output = self.wpl_execute(cmd, mode=None, timeout=600)
        for line in output.splitlines():
            line = line.strip()
            res = re.search(p1, line)
            if res:
                self.wpl_log_success('Successfully run mp2 sdk init!')

#######################################################################################################################
    @logThis
    def run_mp2_come_side_sdk_traffic_check(self, sdkToolLst, stress_time, counterTool):
        count = 0
        error_count = 0
        port_count = 0
        #1. run sdk
        cmd = './' + sdkToolLst[0]
        self.wpl_transmit(cmd)
        self.wpl_receive(SDK_BCM_PROMPT, timeout=120)
        #2. port status
        portStatusCmd = sdkToolLst[2]
        p1 = r'^cd\d+\([ \d]+\)[ \t]+(up).*'
        p3 = 'port counters check test PASSED'
        p2 = '^Port\d+[ \t]+couters[ \t]+\(tx=\d+, rx=\d+\)[ \t]+passed'
        time.sleep(2)
        self.wpl_transmit(portStatusCmd)
        output = self.wpl_receive(SDK_BCM_PROMPT, timeout=120)
        for line in output.splitlines():
            line = line.strip()
            res = re.search(p1, line)
            if res:
                count += 1
        if count == 128:
            self.wpl_log_success('Successfully All ports link status are up!')
        else:
            error_count += 1
            self.wpl_log_fail("Failed found port down.")
        #3. set vlan and traffic
        traffic_time = 'sleep ' + str(stress_time)
        trafficCmdLst = [sdkToolLst[1], sdkToolLst[3], sdkToolLst[-2], traffic_time, sdkToolLst[-1], counterTool]
        for cmd in trafficCmdLst:
            time.sleep(2)
            self.wpl_transmit(cmd)
            output = self.wpl_receive(SDK_BCM_PROMPT, timeout=120)
        for line in output.splitlines():
            line = line.strip()
            res = re.search(p2, line)
            if res:
                port_count += 1
        if port_count == 128:
            self.wpl_log_success('Successfully counter all ports are pass!')
        else:
            error_count += 1
            self.wpl_log_fail("Failed port counter is different.")
        #4. exit sdk
        self.wpl_transmit('exit')
        self.wpl_receive(self.device.promptDiagOS, timeout=90)
        if error_count > 0:
            self.wpl_raiseException("Failed run_mp2_come_side_sdk_traffic_check.")

