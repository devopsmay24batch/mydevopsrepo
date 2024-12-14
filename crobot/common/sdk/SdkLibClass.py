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
import Logger as log
try:
  import re, time
  import json
  import Const
  from functools import partial
  from Sdk_variable import *
  import parserSDKLibs
  from SdkLib import *
  import DeviceMgr
  import Logger as log
  import Device as device
  from errorsModule import noSuchClass, testFailed
  import CommonLib
  from Decorator import *
except Exception as err:
  log.cprint(err)

BOOTING_TIME = 300
#the real info need to be checked will usually be after line 1000, avoid checking from line 1 will save some time
default_begin_check_line = 100
#set the read range to make it more efficient while not risk losing some info
default_read_range = 1000
tmp_output_file_locally = '/tmp/dut_output'
end_of_cmd_mark = 'is not defined'


class SdkLibClass(SdkLib):
    def __init__(self, device):
        SdkLib.__init__(self, device)
        CommonLib.switch_to_centos()
        localbin_python3 = '/usr/local/bin/python3'
        bin_python3 = '/usr/bin/python3'
        self.run_command = partial(CommonLib.run_command, deviceObj=self.device, prompt=self.device.promptDiagOS)
        if CommonLib.check_file_exist(localbin_python3, 'centos') == 1:
          self.python3 = localbin_python3
          self.wpl_log_debug('got the python3 %s' % localbin_python3)
        elif CommonLib.check_file_exist(bin_python3, 'centos') == 1:
          self.python3 = bin_python3
          self.wpl_log_debug('got the python3 %s' % bin_python3)
        else:
          self.wpl_raiseException('failed to get python3')

    ###############################################################################################
    # Function Name: write_output_to_local_file
    # Date         : 30th June 2020
    # Author       : Wallace Qiu. <wallq@celestica.com>
    #
    # Procedure Revision Details:
    #   Version : 1.0  - Initial Draft  - by Wallace Qiu. <wallq@celestica.com>
    ###############################################################################################

    def write_output_to_local_file(self, output, filename):
        self.wpl_log_debug('************* Entering procedure write_output_to_local_file with args : %s\n' %(str(locals())))
        f = open(filename, 'w+')
        f.write(output)
        f.flush()
        time.sleep(1)
        f.close()

    ###############################################################################################
    # Function Name: read_from_local_file
    # Date         : 30th June 2020
    # Author       : Wallace Qiu. <wallq@celestica.com>
    #
    # Procedure Revision Details:
    #   Version : 1.0  - Initial Draft  - by Wallace Qiu. <wallq@celestica.com>
    ###############################################################################################
    def read_from_local_file(self, begin, readrange, pass_message, filename):
        self.wpl_log_debug('************* Entering procedure read_from_local_file with args : %s\n' %(str(locals())))
        output, default_max_lines = '', 2000

        f = open(filename, 'r')
        while begin < default_max_lines:
            count = 0
            while count < readrange:
              temp = f.readline()
              if pass_message in temp:
                 log.cprint('got the expected message [%s]' % pass_message)
                 time.sleep(1)
                 f.close()
                 return output
              output += temp
              count += 1
            begin += readrange

        f.close()
        return output

    ###############################################################################################
    # Function Name: read_from_dut_file_by_block
    # Date         : 30th June 2020
    # Author       : Wallace Qiu. <wallq@celestica.com>
    #
    # Procedure Revision Details:
    #   Version : 1.0  - Initial Draft  - by Wallace Qiu. <wallq@celestica.com>
    ###############################################################################################
    def read_from_dut_file_by_block(self, begin, readrange, pass_message, filename, max_lines=None):
        self.wpl_log_debug('************* Entering procedure read_from_dut_file_by_block with args : %s\n' %(str(locals())))
        line_num_cmd = "wc -l %s |awk '{print $1}'"%(filename)
        line_num_str = self.wpl_execute_cmd(line_num_cmd, mode='centos')
        match = re.search("^(\d+)\s*$", line_num_str, re.M)
        if match:
            line_num = int(match.group(1))
        else:
            line_num = 4000
        output, default_max_lines = '', line_num
        if max_lines:
          default_max_lines = max_lines

        while begin < default_max_lines:
          cmd = "awk '{if (NR>%s && NR<%s) print $0}' %s" % (begin, begin+readrange, filename)
          cmd +=  ";" + "sleep 1"
          temp = self.wpl_execute_cmd(cmd, mode='centos', timeout=200)
          output += temp
          if re.search(pass_message, temp):
             log.cprint('got the expected message [%s]' % pass_message)
             time.sleep(1)
             break
          begin += readrange
          self.wpl_flush()

        if begin >= default_max_lines:
           self.wpl_raiseException('read beyond the max lines without getting the expected message [%s], break.' % pass_message)

        return output

    ###############################################################################################
    # Function Name: read_from_dut_file_from tail
    # Date         : 4th Sept. 2020
    # Author       : Yang, Xuecun <yxcun@celestica.com>
    #
    # Procedure Revision Details:
    #   Version : 1.0  - Initial Draft  - by Yang, Xuecun <yxcun@celestica.com>
    ###############################################################################################
    def read_from_dut_file_from_tail(self, pass_message, filename, tail_num=40):
        self.wpl_log_debug('************* Entering procedure read_from_dut_file_from_tail with args : %s\n' %(str(locals())))
        content = ""
        read_cmd = "tail -{} {}".format(tail_num, filename)
        content = self.wpl_execute_cmd(read_cmd, mode='centos', timeout=200)
        match = re.search(pass_message, content)
        if not match:
           self.wpl_raiseException("Didn't get the expected message [%s]." % pass_message)

        return content

    ###############################################################################################
    # Function Name: generate_parsedOutput_from_dut_file_by_block
    # Date         : 30th June 2020
    # Author       : Wallace Qiu. <wallq@celestica.com>
    #
    # Procedure Revision Details:
    #   Version : 1.0  - Initial Draft  - by Wallace Qiu. <wallq@celestica.com>
    ###############################################################################################
    def generate_parsedOutput_from_dut_file_by_block(self, begin, readrange, pass_message, filename, generate_parsed_dict_func, *param):
        self.wpl_log_debug('************* Entering procedure generate_parsedOutput_from_dut_file_by_block with args : %s\n' %(str(locals())))
        line_num_cmd = "wc -l %s |awk '{print $1}'"%(filename)
        line_num_str = self.wpl_execute_cmd(line_num_cmd, mode='centos')
        match = re.search("^(\d+)\s*$", line_num_str, re.M)
        if match:
            line_num = int(match.group(1))
        else:
            line_num = 4000
        parsedOutput, default_max_lines = {}, line_num

        while begin < default_max_lines:
          cmd = "awk '{if (NR>%s && NR<%s) print $0}' %s" % (begin, begin+readrange, filename)
          finish_prompt = "{}[\s\S]+{}".format(cmd[:3], self.device.promptDiagOS)
          temp = self.device.sendCmdRegexp(cmd, finish_prompt, timeout=160)
          time.sleep(0.5)
          self.wpl_flush()
          if parserSDKLibs.PARSE_port_ber == generate_parsed_dict_func:
            #the initial -1 port is the starting port number which will be added by 1 everytime the PARSE_port_ber processes it.
            temp_parsed = generate_parsed_dict_func(temp, len(parsedOutput)-1)
            if temp_parsed:
              parsedOutput.update(temp_parsed)
              log.cprint('updated parsed_output')
          else:
            parsedOutput = generate_parsed_dict_func(temp)

          if re.search(pass_message, temp):
             log.cprint('got the expected message [%s]' % pass_message)
             time.sleep(1)
             break
          begin += readrange

        if begin >= default_max_lines:
           self.wpl_raiseException('read beyond the max lines without getting the expected message [%s], break.' % pass_message)

        return parsedOutput

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
        self.device.sendCmd("exit()")
        time.sleep(1)
        self.device.sendCmd("\x03")
        time.sleep(1)
        self.device.sendMsg("\n")
        self.device.read_until_regexp(self.device.promptDiagOS, timeout=10)

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

    def get_ipv6_addr(self, eth_tool, dhcp_tool, timeout=20):
        ipformat = r'inet6 (2001.*)\sprefixlen'
        ipList = []
        self.device.sendCmd(dhcp_tool)
        time.sleep(6)
        output = self.device.sendCmdRegexp(eth_tool, self.device.promptDiagOS, timeout=80)
        self.wpl_log_info(output)
        for line in output.splitlines():
            line = line.strip()
            match = re.search(ipformat, line)
            if match:
                ip = match.group(1).strip()
                ipList.append(ip)
                self.wpl_log_success('Successfully get ip address: %s' % (ip))
        return ipList

    def prepare_sdk_soc_images(self, eth_tool, dhcp_tool, scp_ip, usrname, pasrd, local_path, scp_path):
        self.get_ipv6_addr(eth_tool, dhcp_tool)
        time.sleep(5)
        cmd = 'scp -6 -r ' + usrname + '@' + '[' + scp_ip + ']' + ':' + local_path + '/*' + ' ' + scp_path
        self.device.sendCmd(cmd)
        time.sleep(5)
        self.wpl_log_info("////local path = %s " % local_path)
        self.wpl_log_info("////scp_path = %s " % scp_path)
        promptList = ["(yes/no)", "password:"]
        patternList = re.compile('|'.join(promptList))
        output1 = self.device.read_until_regexp(patternList, 200)
        #self.wpl_log_info('output1: ' + str(output1))
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
        #self.device.read_until_regexp(cmd1, self.device.promptDiagOS, timeout=50)
        #time.sleep(5)
        self.wpl_flush()
        self.device.sendMsg("\n")

    ###############################################################################################
    # Function Name: run_script_into_centos
    # Date         : 30th June 2020
    # Author       : Wallace Qiu. <wallq@celestica.com>
    #
    # Procedure Revision Details:
    #   Version : 1.0  - Initial Draft  - by Wallace Qiu. <wallq@celestica.com>
    ###############################################################################################
    def run_script_into_centos(self, cmd, pass_message, timeout=60):
        try:
          self.device.sendCmdRegexp(cmd, pass_message, timeout=timeout)

        except Exception as err:
          self.wpl_flush()
          time.sleep(10)
          self.device.readMsg()

          self.wpl_log_debug("Didn't get expected log message in {}s.".format(timeout))

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
        if fec:
          if '8X50G_QSFP_4X50G' in str.upper(portmode):
              var_expectedDict = portFEC_DD_8X50G_QSFP_4X50G
          elif '4X50G_QSFP_4X25G' in str.upper(portmode):
              var_expectedDict = portFEC_DD_4X50G_QSFP_4X25G
          elif '8X50G_QSFP_4X25G' in str.upper(portmode):
              var_expectedDict = portFEC_DD_8X50G_QSFP_4X25G
          elif '4X25G_QSFP_4X25G' in str.upper(portmode):
              var_expectedDict = portFEC_DD_4X25G_QSFP_4X25G
          elif '4X25G_QSFP_2X2X25G' in str.upper(portmode):
              var_expectedDict = portFEC_DD_4X25G_QSFP_2X2X25G
          elif '32x1x8x50g' in str.lower(portmode):
              var_expectedDict = portFEC_DD_8X50G
          elif '32x1x4x50g' in str.lower(portmode):
              var_expectedDict = portFEC_DD_4X50G
          else:
            self.wpl_log_debug('unrecognizable FEC port mode [%s], return. \n '%(portmode))
            return None

        else:
          if '8X50G_QSFP_4X50G' in str.upper(portmode):
              var_expectedDict = portStatusDD_8X50G_QSFP_4X50G
          elif '8X50G_QSFP_4X25G' in str.upper(portmode):
              var_expectedDict = portStatusDD_8X50G_QSFP_4X25G
          elif '4X50G_QSFP_4X25G' in str.upper(portmode):
              var_expectedDict = portStatusDD_4X50G_QSFP_4X25G
          elif '4X25G_QSFP_4X25G' in str.upper(portmode):
              var_expectedDict = portStatusDD_4X25G_QSFP_4X25G
          elif '4X25G_QSFP_2X2X25G' in str.upper(portmode):
              var_expectedDict = portStatusDD_4X25G_QSFP_2X2X25G
          else:
            self.wpl_log_debug('unrecognizable port mode [%s], return. \n '%(portmode))
            return

        return var_expectedDict


    ###############################################################################################
    # Function Name: load_sdk_init_with_portcheck
    # Date         : 30th June 2020
    # Author       : Wallace Qiu. <wallq@celestica.com>
    #
    # Procedure Revision Details:
    #   Version : 1.0  - Initial Draft  - by Wallace Qiu. <wallq@celestica.com>
    ###############################################################################################
    def load_sdk_init_with_portcheck(self, portmode, expectedPortDict, expectedResult, devicePhase=None):
        self.wpl_log_debug('************* Entering procedure load_sdk_init_with_portcheck with args : %s\n' %(str(locals())))

        failCount = 0

        if devicePhase == 'EVT1':
            boardVer = '0'
        elif devicePhase == 'EVT2':
            boardVer = '1'

        if CommonLib.check_file_exist(SDK_SCRIPT, 'centos') != 1:
            self.wpl_log_debug('did not get the file %s, return' % SDK_SCRIPT)
            self.wpl_raiseException("load_sdk_init_with_portcheck")
            return

        pass_message = '- Done!'
        cmd = '%s %s -c init -p %s > %s ' %(self.python3, SDK_SCRIPT, portmode, tmp_output_file_on_dut)
        self.run_script_into_centos(cmd, pass_message, 200)
        self.getback_2_centos()

        pass_message = r'GB Initialization Test.* PASS'
        cmd = 'grep -n "%s" %s' % (pass_message, tmp_output_file_on_dut)
        output = self.device.sendCmdRegexp(cmd, pass_message, timeout=5)

        cmd = 'cat %s' % tmp_output_file_on_dut
        pass_message = 'INIT Test Command'
        output = self.device.sendCmdRegexp(cmd, pass_message, timeout=250)
        #add more delay to make sure the cat process completed, to avoid the output message messup
        time.sleep(5)
        self.wpl_flush()

        parsedPortDict = parserSDKLibs.PARSE_port_link_status(output)
        parsedTestResult = parserSDKLibs.PARSE_test_result(output)

        # verify port number
        failCount += self.verify_port_count(parsedPortDict)

        # verify port status
        failCount += self.verify_port_status_no_check_seq(parsedPortDict, expectedPortDict)

        #verify test result
        failCount += self.verify_test_result(parsedTestResult, expectedResult)

        if failCount:
            self.wpl_raiseException('load_sdk_init_with_portcheck failed with %s failures' % failCount)
        else:
            self.wpl_log_success('load_sdk_init_with_portcheck mode %s passed. ' % portmode)


    ###############################################################################################
    # Function Name: load_sdk_init
    # Date         : 30th June 2020
    # Author       : Wallace Qiu. <wallq@celestica.com>
    #
    # Procedure Revision Details:
    #   Version : 1.0  - Initial Draft  - by Wallace Qiu. <wallq@celestica.com>
    ###############################################################################################
    def load_sdk_init(self, portmode):
        self.wpl_log_debug('************* Entering procedure load_sdk_init with args : %s\n' %(str(locals())))

        if CommonLib.check_file_exist(SDK_SCRIPT, 'centos') != 1:
            self.wpl_log_debug('did not get the file %s, return' % SDK_SCRIPT)
            self.wpl_raiseException("load_sdk_init")
            return

        pass_message = '- Done!'
        pass_message = sdkConsole
        cmd = '%s %s -c all --run_case 1 -p %s > %s ' %(self.python3, SDK_SCRIPT, portmode, tmp_output_file_on_dut)
        self.run_script_into_centos(cmd, pass_message, 200)

    ###############################################################################################
    # Function Name: run_port_linkup_test
    # Date         : 30th June 2020
    # Author       : Wallace Qiu. <wallq@celestica.com>
    #
    # Procedure Revision Details:
    #   Version : 1.0  - Initial Draft  - by Wallace Qiu. <wallq@celestica.com>
    ###############################################################################################
    def run_port_linkup_test(self, portmode):
        self.wpl_log_debug('************* Entering procedure run_port_linkup_test with args : %s\n' %(str(locals())))

        if CommonLib.check_file_exist(SDK_SCRIPT, 'centos') != 1:
            self.wpl_log_debug('did not get the file %s, return' % SDK_SCRIPT)
            self.wpl_raiseException("run_port_linkup_test")
            return

        pass_message = r'-do_port_linkup_validation_test- TEST.* PASS'
        cmd = '%s %s -c all --run_case 6 -p %s ' %(self.python3, SDK_SCRIPT, portmode)
        end_pattern = pass_message + "|" + sdkConsole
        output1 =self.device.sendCmdRegexp(cmd, end_pattern, timeout=3600)
        match = re.search(pass_message, output1)
        if not match:
            self.wpl_raiseException('%s failed'%cmd)

    ###############################################################################################
    # Function Name: check_sdk_port_status
    # Date         : 30th June 2020
    # Author       : Wallace Qiu. <wallq@celestica.com>
    #
    # Procedure Revision Details:
    #   Version : 1.0  - Initial Draft  - by Wallace Qiu. <wallq@celestica.com>
    ###############################################################################################
    def check_sdk_port_status(self, expectedResult, portmode):
        self.wpl_log_debug('************* Entering procedure check_sdk_port_status with args : %s\n' %(str(locals())))
        failCount = 0

        expectedPortDict = self.select_expected_status_dict(portmode)
        #pass_message = 'INIT Test Command'
        pass_message = 'META Wedge400C Run Test All.*PASS'
        output = self.read_from_dut_file_by_block(default_begin_check_line, default_read_range, pass_message, tmp_output_file_on_dut)
        self.add_flush_and_delay()
        parsedPortDict = parserSDKLibs.PARSE_port_link_status_with_unexpected_return(output)
        parsedTestResult = parserSDKLibs.PARSE_test_result(output)

        # verify port number
        failCount += self.verify_port_count(parsedPortDict, portmode)

        # verify port status
        failCount += self.verify_port_status_no_check_seq(parsedPortDict, expectedPortDict)

        #verify test result
        failCount += self.verify_test_result(parsedTestResult, expectedResult)

        if failCount:
            self.wpl_raiseException('check_sdk_port_status failed with %s failures' % failCount)
        else:
            self.wpl_log_success('check_sdk_port_status mode %s passed. ' % portmode)

    ###############################################################################################
    # Function Name: check_port_ber
    # Date         : 30th June 2020
    # Author       : Wallace Qiu. <wallq@celestica.com>
    #
    # Procedure Revision Details:
    #   Version : 1.0  - Initial Draft  - by Wallace Qiu. <wallq@celestica.com>
    ###############################################################################################
    def check_port_ber(self, portmode, berThreshold):
        self.wpl_log_debug('************* Entering procedure check_port_ber with args : %s\n' %(str(locals())))
        failCount = 0

        cmd = '%s %s -c ber -p %s ' %(self.python3, SDK_SCRIPT, portmode)
        output = self.wpl_execute_cmd(cmd, mode='centos', timeout=800)
        parsedOutput = parserSDKLibs.PARSE_port_ber(output)

        ### verify all port ber < 1e-10
        for i in ALL_PORT_NUM:
            failInPort = 0
            for berValue in parsedOutput[i]:
                if berValue >= berThreshold:
                    self.wpl_log_fail('The number %d Port: %s BER is greater than %s'%(i, berValue, berThreshold))
                    failCount += 1
                    failInPort += 1
            if failInPort == 0:
                self.wpl_log_success('The number %d Port: All BER are less than %s'%(i, berThreshold))

        if failCount:
            self.wpl_raiseException('check_port_ber %s mode failed with %s failures' % (portmode, failCount))
        else:
            self.wpl_log_success('check_port_ber mode %s passed. ' % portmode)

    ###############################################################################################
    # Function Name: run_port_loopback_test
    # Date         : 30th June 2020
    # Author       : Wallace Qiu. <wallq@celestica.com>
    #
    # Procedure Revision Details:
    #   Version : 1.0  - Initial Draft  - by Wallace Qiu. <wallq@celestica.com>
    ###############################################################################################
    def run_port_loopback_test(self, portmode, loopback_type, timeout=1200, full_log=True):
        self.wpl_log_debug('************* Entering procedure run_port_loopback_test with args : %s\n' %(str(locals())))
        finish_prompt = r"{}|{}".format(self.device.promptDiagOS, sdkConsole)

        cmd = '%s %s -c all --run_case 7 -o %s -p %s 2>&1 |tee %s' %(self.python3, SDK_SCRIPT, loopback_type, portmode, tmp_output_file_on_dut)
        if not full_log:
            cmd = '%s -u %s -c loopback -o %s -p %s > %s' %(self.python3, SDK_SCRIPT, loopback_type, portmode, tmp_output_file_on_dut)
        pass_message = r'%s[\s\S]+(%s)' % (cmd[:30], finish_prompt)
        output = self.run_script_into_centos(cmd, pass_message, timeout)

    ###############################################################################################
    # Function Name: check_port_loopback_status
    # Date         : 30th June 2020
    # Author       : Wallace Qiu. <wallq@celestica.com>
    #
    # Procedure Revision Details:
    #   Version : 1.0  - Initial Draft  - by Wallace Qiu. <wallq@celestica.com>
    ###############################################################################################
    def check_port_loopback_status(self, loopback_type):
        failCount = 0

        #pass_message = r'GB Mac Ports %s Loopback Test.*?PASS' % (loopback_type)
        pass_message = r'.*Loopback Test.*?PASS'
        output = self.read_from_dut_file_from_tail(pass_message, tmp_output_file_on_dut)
        parsedOutput = parserSDKLibs.PARSE_test_result(output)

        failCount += self.verify_test_result(parsedOutput, pass_message)

        if failCount:
            self.wpl_raiseException('check_port_loopback %s mode failed with %s failures' % (loopback_type, failCount))
        else:
            self.wpl_log_success('check_port_loopback mode %s passed. ' % loopback_type)

    ###############################################################################################
    # Function Name: run_mac_port_ber_test
    # Date         : 30th June 2020
    # Author       : Wallace Qiu. <wallq@celestica.com>
    #
    # Procedure Revision Details:
    #   Version : 1.0  - Initial Draft  - by Wallace Qiu. <wallq@celestica.com>
    ###############################################################################################
    def run_mac_port_ber_test(self, portmode):
        self.wpl_log_debug('************* Entering procedure run_mac_port_ber_test with args : %s\n' %(str(locals())))

        cmd = '%s %s -c all --run_case 5 -p %s |tee %s ' %(self.python3, SDK_SCRIPT, portmode, tmp_output_file_on_dut)
        if portmode in cloudripper_port_mode:
            cmd = '%s %s -c ber -p %s -b 1e-6 |tee %s ' %(self.python3, SDK_SCRIPT, portmode, tmp_output_file_on_dut)
        pass_message = r'META Wedge400C Run Test All.*(PASS|{})'.format(sdkConsole)

        timeout = 4100
        self.run_script_into_centos(cmd, pass_message, timeout)
        self.add_flush_and_delay()

    ###############################################################################################
    # Function Name: check_mac_port_ber_status
    # Date         : 30th June 2020
    # Author       : Wallace Qiu. <wallq@celestica.com>
    #
    # Procedure Revision Details:
    #   Version : 1.0  - Initial Draft  - by Wallace Qiu. <wallq@celestica.com>
    ###############################################################################################
    def check_mac_port_ber_status(self, portmode, berThreshold):
        self.wpl_log_debug('************* Entering procedure check_mac_port_ber_status with args : %s\n' %(str(locals())))
        failCount = 0

        pass_message = r'META Wedge400C Run Test All.*PASS'
        parsedOutput = self.generate_parsedOutput_from_dut_file_by_block(default_begin_check_line, default_read_range, pass_message, tmp_output_file_on_dut, parserSDKLibs.PARSE_port_ber)

        # verify all port ber < 1e-10

        expected_port_numbers = 79 if '4X25G_QSFP_2X2X25G' in str.upper(portmode) else 48
        for i in range(0, expected_port_numbers):
            failInPort = 0
            if i >= len(parsedOutput):
                self.wpl_log_fail("Didn't get port {} BER info ".format(i))
                failCount += 1
                break
            for berValue in parsedOutput[i]:
                if berValue >= berThreshold:
                    self.wpl_log_fail('The number %d Port: %s BER is greater than %s'%(i, berValue, berThreshold))
                    failCount += 1
                    failInPort += 1
            if failInPort == 0:
                self.wpl_log_success('The number %d Port: All BER are less than %s'%(i, berThreshold))

        output = self.read_from_dut_file_by_block(default_begin_check_line, default_read_range, pass_message, tmp_output_file_on_dut)
        parsed_index_groups = parserSDKLibs.PARSE_port_ber_lane_status(output, berThreshold)
        if parsed_index_groups != {}:
          self.wpl_log_debug('------ found unusual BER values ------')
          failCount += len(parsed_index_groups)

        if failCount:
            self.wpl_raiseException('check_mac_port_ber_status, portmode: %s, the ber-lane status: %s'%(portmode, parsed_index_groups))
        else:
            self.wpl_log_success('check_mac_port_ber_status mode %s passed. ' % portmode)

    ###############################################################################################
    # Function Name: check_port_fec
    # Date         : 30th June 2020
    # Author       : Wallace Qiu. <wallq@celestica.com>
    #
    # Procedure Revision Details:
    #   Version : 1.0  - Initial Draft  - by Wallace Qiu. <wallq@celestica.com>
    ###############################################################################################
    def check_port_fec(self, portmode, expectedFECDict, expectedResult, devicePhase=None):
        self.wpl_log_debug('************* Entering procedure check_port_fec with args : %s\n' %(str(locals())))
        failCount = 0

        cmd = '%s -c l2_cpu -p %s -d 5' %(SDK_SCRIPT, portmode)
        self.wpl_transmit(cmd)
        output = self.wpl_receive(sdkConsole, timeout=300)
        parsedOutput = parserSDKLibs.PARSE_port_fec(output)
        failCount += self.verify_port_status_no_check_seq(parsedOutput, expectedFECDict)

        cmd2 = 'tc.mph.print_mac_up()'
        self.wpl_transmit(cmd2)
        output2 = self.wpl_receive(sdkConsole, timeout=300)
        parsedTestResult = parserSDKLibs.PARSE_test_result(output2)
        failCount += self.verify_test_result(parsedTestResult, expectedResult)

        cmd3 = 'exit()'
        self.wpl_transmit(cmd3)
        self.wpl_flush()
        self.wpl_getPrompt('centos')

        if failCount:
            self.wpl_raiseException('check_port_fec %s mode failed with %s failures' % (portmode, failCount))
        else:
            self.wpl_log_success('check_port_fec mode %s passed. ' % portmode)

    ###############################################################################################
    # Function Name: run_default_port_info_test
    # Date         : 30th June 2020
    # Author       : Wallace Qiu. <wallq@celestica.com>
    #
    # Procedure Revision Details:
    #   Version : 1.0  - Initial Draft  - by Wallace Qiu. <wallq@celestica.com>
    ###############################################################################################
    def run_default_port_info_test(self, portmode):
        self.wpl_log_debug('************* Entering procedure run_default_port_info_test with args : %s\n' %(str(locals())))
        failCount = 0

        cmd = '%s %s -c l2_cpu -p %s -d 5' %(self.python3, SDK_SCRIPT, portmode)
        pass_message = r'L2 snake traffic with cpu injection.*PASS'
        end_pattern = pass_message + "|" + sdkConsole
        output1 = self.device.sendCmdRegexp(cmd, end_pattern, timeout=3600)
        match = re.search(pass_message, output1)
        if not match:
            self.wpl_raiseException('%s failed'%cmd)
        self.add_flush_and_delay()

        cmd2 = 'tc.mph.print_mac_up(); finish'
        self.wpl_log_debug('Begin running tc.mph.print_mac_up()')
        output =self.device.sendCmdRegexp(cmd2, end_of_cmd_mark, timeout=300)

        #remove the end of cmd mark to avoid its mix with the output
        output = output.replace(end_of_cmd_mark, '')
        self.wpl_log_debug('Copying the processed output to local tmp file')
        self.write_output_to_local_file(output, tmp_output_file_locally)
        time.sleep(2)

    ###############################################################################################
    # Function Name: check_default_port_info_status
    # Date         : 30th June 2020
    # Author       : Wallace Qiu. <wallq@celestica.com>
    #
    # Procedure Revision Details:
    #   Version : 1.0  - Initial Draft  - by Wallace Qiu. <wallq@celestica.com>
    ###############################################################################################
    def check_default_port_info_status(self, portmode):
        self.wpl_log_debug('************* Entering procedure check_default_port_info_status with args : %s\n' %(str(locals())))
        failcount = 0

        expectedFECDict = self.select_expected_status_dict(portmode, fec=True)
        output = self.read_from_local_file(0, default_read_range, end_of_cmd_mark, tmp_output_file_locally)

        parsedOutput = parserSDKLibs.PARSE_port_fec_with_unexpected_return(output)
        self.wpl_log_debug(str(parsedOutput))
        failcount += self.verify_port_status_no_check_seq(parsedOutput, expectedFECDict)
        if failcount:
          self.wpl_raiseException('check_default_port_info_status %s mode failed with %s failures' % (portmode, failcount))
        else:
          self.wpl_log_success('check_default_port_info_status mode %s passed. ' % portmode)

    ###############################################################################################
    # Function Name: check_temperature
    # Date         : 30th June 2020
    # Author       : Wallace Qiu. <wallq@celestica.com>
    #
    # Procedure Revision Details:
    #   Version : 1.0  - Initial Draft  - by Wallace Qiu. <wallq@celestica.com>
    ###############################################################################################
    def check_temperature(self, expectedResult):
        self.wpl_log_debug('************* Entering procedure check_temperature with args : %s\n' %(str(locals())))
        temperature_ok, voltage_ok = '-do_sensor_test.*TEST.*?PASS', 'META Wedge400C Run Test All.*PASS'
        failCount = 0
        cmd = '%s %s -c all --run_case 2' %(self.python3, SDK_SCRIPT)
        pass_message = sdkConsole
        output = self.device.sendCmdRegexp(cmd, pass_message, timeout=3000)
        self.add_flush_and_delay()

        check_keywords = [temperature_ok, voltage_ok]
        failCount += parserSDKLibs.PARSE_test_result_more_keywords(output, check_keywords)
        failCount += parserSDKLibs.PARSE_port_value_range_check(output, r'TEMPERATURE_\d=(\d+\.\d+)', (temperature_range_min, temperature_range_max))
        failCount += parserSDKLibs.PARSE_port_value_range_check(output, r'VOLTAGE_\d=(\d+\.\d+)', (voltage_range_min, voltage_range_max))

        if failCount:
            self.wpl_raiseException('check_temperature failed with %s failures' % failCount)
        else:
            self.wpl_log_success('check_temperature passed ')


    ###############################################################################################
    # Function Name: check_max_power
    # Date         : 30th June 2020
    # Author       : Wallace Qiu. <wallq@celestica.com>
    #
    # Procedure Revision Details:
    #   Version : 1.0  - Initial Draft  - by Wallace Qiu. <wallq@celestica.com>
    ###############################################################################################
    def check_max_power(self, expectedResult, devicePhase=None):
        self.wpl_log_debug('************* Entering procedure check_max_power with args : %s\n' %(str(locals())))
        failCount = 0
        cmd = '%s %s -c max_power ' %(self.python3, SDK_SCRIPT)

        self.wpl_transmit(cmd)
        output = self.wpl_receive(sdkConsole, timeout=300)

        cmd3 = 'exit()'
        self.wpl_transmit(cmd3)
        self.wpl_flush()
        self.wpl_getPrompt('centos')

        # parsedOutput = parserSDKLibs.PARSE_test_result(output)
        # failCount += self.verify_test_result(parsedOutput, expectedResult)
        # if failCount:
        #     raise testFailed("check_max_power")


    ###############################################################################################
    # Function Name: check_memory_bist
    # Date         : 30th June 2020
    # Author       : Wallace Qiu. <wallq@celestica.com>
    #
    # Procedure Revision Details:
    #   Version : 1.0  - Initial Draft  - by Wallace Qiu. <wallq@celestica.com>
    ###############################################################################################
    def check_memory_bist(self, expectedResult):
        self.wpl_log_debug('************* Entering procedure check_memory_bist with args : %s\n' %(str(locals())))
        failCount = 0
        cmd = '%s %s -c bist 2>&1 > %s ' %(self.python3, SDK_SCRIPT, tmp_output_file_on_dut)
        self.run_script_into_centos(cmd, expectedResult, 100)
        self.wpl_log_success('memory BIST check PASS.')

    ###############################################################################################
    # Function Name: test_traffic
    # Date         : 30th June 2020
    # Author       : Wallace Qiu. <wallq@celestica.com>
    #
    # Procedure Revision Details:
    #   Version : 1.0  - Initial Draft  - by Wallace Qiu. <wallq@celestica.com>
    ###############################################################################################
    def test_traffic(self, portmode, runningTime, test_level):

        self.wpl_log_debug('************* Entering procedure test_%s_traffic with args : %s\n' %(test_level, str(locals())))
        cpu_level = 'l2_cpu' if test_level == 'L2' else 'l3_cpu'

        pass_message = r'%s snake traffic with cpu injection.* PASS' % (test_level)
        cmd = '%s %s -c %s -d %d -p %s  ' %(self.python3, SDK_SCRIPT, cpu_level, runningTime, portmode)
        output1 = self.device.sendCmdRegexp(cmd, pass_message, timeout=runningTime+400)
        #add more delay to make sure the cat process completed, to avoid the output message messup
        self.add_flush_and_delay()

        parsedPortDict = parserSDKLibs.PARSE_port_link_status_with_unexpected_return(output1)
        parsedTestResult = parserSDKLibs.PARSE_test_result(output1)

        cmd2 = 'tc.mph.print_mac_stats(); finish'
        self.wpl_log_debug('Begin running tc.mph.print_mac_stats()')
        finish_prompt = "{}[\s\S]+{}".format(cmd2[:5], sdkConsole)
        output =self.device.sendCmdRegexp(cmd2, finish_prompt, timeout=300)

        #remove the end of cmd mark to avoid its mix with the output
        output = output.replace(end_of_cmd_mark, '')
        self.wpl_log_debug('Copying the processed output to local tmp file')
        self.write_output_to_local_file(output1 + output, tmp_output_file_locally)
        self.add_flush_and_delay()

    ###############################################################################################
    # Function Name: check_traffic_status
    # Date         : 30th June 2020
    # Author       : Wallace Qiu. <wallq@celestica.com>
    #
    # Procedure Revision Details:
    #   Version : 1.0  - Initial Draft  - by Wallace Qiu. <wallq@celestica.com>
    ###############################################################################################
    def check_traffic_status(self, portmode):
        self.wpl_log_debug('************* Entering procedure check_traffic_status with args : %s\n' %(str(locals())))
        failCount = 0

        expectedDict = self.select_expected_status_dict(portmode)
        output = self.read_from_local_file(0, default_read_range, end_of_cmd_mark, tmp_output_file_locally)

        parsedOutput = parserSDKLibs.PARSE_port_traffic(output)
        self.wpl_log_debug(str(parsedOutput))

        failCount += self.verify_no_packet_loss(parsedOutput)
        if failCount:
            self.wpl_raiseException('check_traffic_status mode %s failed with %s failures' % (portmode, failCount))
        else:
            self.wpl_log_success('check_traffic_status mode %s passed with no packet loss' % portmode)

        self.add_flush_and_delay()

    ###############################################################################################
    # Function Name: verify_sdk_version
    # Date         : 30th June 2020
    # Author       : Wallace Qiu. <wallq@celestica.com>
    #
    # Procedure Revision Details:
    #   Version : 1.0  - Initial Draft  - by Wallace Qiu. <wallq@celestica.com>
    ###############################################################################################
    def verify_sdk_version(self, expectedResultDict):
        self.wpl_log_debug('************* Entering procedure verify_sdk_version with args : %s\n' %(str(locals())))
        cmd = '%s %s -c all --run_case 10 ' %(self.python3, SDK_SCRIPT)
        pass_message = sdkConsole
        output = self.device.sendCmdRegexp(cmd, pass_message, timeout=120)
        log.cprint(output)
        self.wpl_flush()

        for line in output.split('\n'):
          if 'Show Version Test' in line:
            self.wpl_log_debug('------ got the version info ------')
            p1 = r'.*Show Version Test.*%s.*%s.*%s.*%s.*' % expectedResultDict
            if re.search(p1, line):
              self.wpl_log_success('sdk version check is ok')
              return

        raise testFailed("verify_sdk_version, expect: {}".format(expectedResultDict))


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
    # Function Name: verify_port_status_check_seq
    # Date         : 30th June 2020
    # Author       : Wallace Qiu. <wallq@celestica.com>
    #
    # Procedure Revision Details:
    #   Version : 1.0  - Initial Draft  - by Wallace Qiu. <wallq@celestica.com>
    ###############################################################################################
    def verify_port_status_check_seq(self, parsedPortDict, expectedPortDict):
        self.wpl_log_debug('************* Entering procedure verify_port_status_check_seq with args : %s\n' %(str(locals())))
        failcount = 0

        for portNumber in ALL_PORT_NUM:
          self.wpl_log_info('--------------------- trying to find match for the Link Number: %d'%(portNumber))
          expectedStatus = expectedFECDict[portNumber]
          parsedStatus = parsedOutput['port_number'][portNumber]
          failcount += CommonLib.compare_input_dict_to_parsed(parsedStatus, expectedStatus, True)

        return failcount

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
        ALL_PORTs = expectedPortDict.keys()
        try:
          for portNumber_expected in ALL_PORTs:
            expectedStatus = expectedPortDict[portNumber_expected]

            #do not need to match item by item, can get one matching item in the whole parsed list is ok
            find = 0
            for portNumber_parsed, _ in enumerate(parsedPortDict['port_number']):
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
            if find >= len(ALL_PORTs):
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
        if re.search(expectedTestResult, parsedInfoDict.get('Test Result', '')):
            self.wpl_log_success('Test Result: %s' %(expectedTestResult))
        else:
            self.wpl_log_fail('Didn\'t get test Result: %s'%(str(expectedTestResult)))
            failCount += 1
        return failCount


    ###############################################################################################
    # Function Name: verify_no_packet_loss
    # Date         : 30th June 2020
    # Author       : Wallace Qiu. <wallq@celestica.com>
    #
    # Procedure Revision Details:
    #   Version : 1.0  - Initial Draft  - by Wallace Qiu. <wallq@celestica.com>
    ###############################################################################################
    def verify_no_packet_loss(self, parsedDict):
        self.wpl_log_debug('************* Entering procedure verify_test_result with args : %s\n' %(str(locals())))
        failCount = 0
        lossByte = parsedDict['tx_bytes'] - parsedDict['rx_bytes']
        speedDiff = parsedDict['tx_gbps'] - parsedDict['tx_gbps']
        if lossByte == 0:
            self.wpl_log_success('No packet loss')
        else:
            self.wpl_log_fail('Found packet loss')
            failCount += 1
        if speedDiff != 0:
            self.wpl_log_fail('Tx speed is not equal as Rx speed')
            failCount += 1
        return failCount


    ###############################################################################################
    # Function Name: get_board_version
    # Date         : 30th June 2020
    # Author       : Wallace Qiu. <wallq@celestica.com>
    #
    # Procedure Revision Details:
    #   Version : 1.0  - Initial Draft  - by Wallace Qiu. <wallq@celestica.com>
    ###############################################################################################
    def get_board_version(self, devicePhase):
        self.wpl_log_debug('************* Entering procedure get_board_version with args : %s\n' %(str(locals())))
        boardVer = ''
        if devicePhase.upper() == 'EVT1':
            boardVer = '0'
        elif devicePhase.upper() == 'EVT2':
            boardVer = '1'
        return boardVer


    ###############################################################################################
    # Function Name: run_manufacture_test
    # Date         : 9th July 2020
    # Author       : Xuecun Yang <yxcun@celestica.com>
    #
    # Procedure Revision Details:
    #   Version : 1.0  - Initial Draft  - by Xuecun Yang <yxcun@celestica.com>
    ###############################################################################################

    def run_manufacture_test(self):
        pass_message = r'META Wedge400C Run Test All.*PASS'
        failCount = 0
        cmd = '%s -u %s -c all --run_case 1 2>&1 |tee %s ' %(self.python3, SDK_SCRIPT, tmp_output_file_on_dut)
        self.device.sendCmdRegexp(cmd, pass_message, 5000)
        #add more delay to make sure the cat process completed, to avoid the output message messup
        self.add_flush_and_delay()
        self.getback_2_centos()

        output = self.read_from_dut_file_by_block(default_begin_check_line, default_read_range, pass_message, tmp_output_file_on_dut)
        check_keywords = ['META Wedge400C Run Test All.*PASS']
        failCount += parserSDKLibs.PARSE_test_result_more_keywords(output, check_keywords)
        if failCount > 0:
            self.wpl_raiseException('get_manufacturing_output failed with %d failures' % (failCount))
        else:
            self.wpl_log_success('get_manufacturing_output passed. ')


    ##############################################################################################
    # Function Name: reinit_test
    # Date         : 30th June 2020
    # Author       : Wallace Qiu. <wallq@celestica.com>
    #
    # Procedure Revision Details:
    #   Version : 1.0  - Initial Draft  - by Wallace Qiu. <wallq@celestica.com>
    ###############################################################################################
    def reinit_test(self):
        self.wpl_log_debug('************* Entering procedure reinit_test with args : %s\n' %(str(locals())))

        if CommonLib.check_file_exist(SDK_SCRIPT, 'centos') != 1:
            self.wpl_log_debug('did not get the file %s, return' % SDK_SCRIPT)
            self.wpl_raiseException("load_sdk_init")
            return

        pass_message = sdkConsole+'.*'
        cmd = '%s %s -c all --run_case 1 2>&1 |tee %s ' %(self.python3, SDK_SCRIPT, tmp_output_file_on_dut)
        self.run_script_into_centos(cmd, pass_message, 1600)

    ###############################################################################################
    # Function Name: check_reinit_port_status
    # Date         : 30th June 2020
    # Author       : Wallace Qiu. <wallq@celestica.com>
    #
    # Procedure Revision Details:
    #   Version : 1.0  - Initial Draft  - by Wallace Qiu. <wallq@celestica.com>
    ###############################################################################################
    def check_reinit_port_status(self, expectedResult):
        self.wpl_log_debug('************* Entering procedure check_reinit_port_status with args : %s\n' %(str(locals())))
        failCount = 0

        pass_message = 'META Wedge400C Run Test All.*PASS'
        output = self.read_from_dut_file_from_tail(pass_message, tmp_output_file_on_dut, tail_num=40)
        time.sleep(15)
        self.add_flush_and_delay()

        failCount += parserSDKLibs.PARSE_test_result_more_keywords(output, expectedResult, True)
        if failCount:
            self.wpl_raiseException('check_reinit_port_status failed with %s failures' % failCount)
        else:
            self.wpl_log_success('check_reinit_port_status passed. ')

    ##############################################################################################
    # Function Name: run_port_enable_disable
    # Date         : 30th June 2020
    # Author       : Wallace Qiu. <wallq@celestica.com>
    #
    # Procedure Revision Details:
    #   Version : 1.0  - Initial Draft  - by Wallace Qiu. <wallq@celestica.com>
    ###############################################################################################
    def run_port_enable_disable(self):
        self.wpl_log_debug('************* Entering procedure run_port_enable_disable with args : %s\n' %(str(locals())))

        if CommonLib.check_file_exist(SDK_SCRIPT, 'centos') != 1:
            self.wpl_log_debug('did not get the file %s, return' % SDK_SCRIPT)
            self.wpl_raiseException("load_sdk_init")
            return

        pass_message = sdkConsole+'.*'
        cmd = '%s %s -c all --run_case 6 2>&1 |tee %s ' %(self.python3, SDK_SCRIPT, tmp_output_file_on_dut)
        self.run_script_into_centos(cmd, pass_message, 800)

    ###############################################################################################
    # Function Name: check_port_enable_disable_status
    # Date         : 30th June 2020
    # Author       : Wallace Qiu. <wallq@celestica.com>
    #
    # Procedure Revision Details:
    #   Version : 1.0  - Initial Draft  - by Wallace Qiu. <wallq@celestica.com>
    ###############################################################################################
    def check_port_enable_disable_status(self, expectedResult):
        self.wpl_log_debug('************* Entering procedure check_port_enable_disable_status with args : %s\n' %(str(locals())))
        failCount = 0

        pass_message = 'META Wedge400C Run Test All.*PASS'
        output = self.read_from_dut_file_by_block(default_begin_check_line, default_read_range, pass_message, tmp_output_file_on_dut)
        self.add_flush_and_delay()

        failCount += parserSDKLibs.PARSE_test_result_more_keywords(output, expectedResult, True)
        if failCount:
            self.wpl_raiseException('check_port_enable_disable_status failed with %s failures' % failCount)
        else:
            self.wpl_log_success('check_port_enable_disable_status passed. ')


#######################################################################################################################
# Function Name: check_output
# Date         : July 31th 2020
# Author       : Yang, Xuecun <yxcun@celestica.com>
#
# Procedure Revision Details:
#   Version : 1.0  - Initial Draft  - by Yang, Xuecun <yxcun@celestica.com>
#######################################################################################################################
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
# Function Name: execute_check_dict
# Date         : Aug. 18th 2020
# Author       : Yang, Xuecun <yxcun@celestica.com>
#
# Procedure Revision Details:
#   Version : 1.0  - Initial Draft  - by Yang, Xuecun <yxcun@celestica.com>
#######################################################################################################################
    def execute_check_dict(self, cmd, mode=None, patterns_dict={}, path=None, timeout=900, line_mode=True, is_negative_test=False, check_output=None, remark=""):
        self.wpl_log_debug('Entering procedure execute_check_dict with args : %s' %(str(locals())))
        passCount = 0
        patternNum = len(patterns_dict)
        self.wpl_log_debug('path:**{}**, cmd:**{}** '.format(path, cmd))
        if path:
            self.wpl_transmit('cd ' + path)
        if check_output:
            output = check_output
        else:
            output = self.wpl_execute_cmd(cmd, mode=mode, timeout=timeout)

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
        mismatch_key_name = set(pattern_all)-set(pass_p) if not is_negative_test else set(pass_p)
        self.wpl_log_debug('passCount = %s' %passCount)
        self.wpl_log_debug('patternNum = %s' %patternNum)
        cmd = cmd.strip("\n")
        if remark:
            description = remark + ":" + cmd
        else:
            description = "commands:{}".format(cmd)
        if passCount == patternNum:
            self.wpl_log_success('%s is PASSED\n' %description)
        else:
            cmd_str = cmd
            if cmd:
                cmd_str = "while execute '{}' ".format(cmd)
            self.wpl_log_fail('Exiting execute_check_cmd with result FAIL. {}'.format(remark))
            self.wpl_raiseException("Failure {}with  items: {}".format(cmd_str, mismatch_key_name))


#######################################################################################################################
# Function Name: execute_check_num
# Date         : Aug. 18th 2020
# Author       : Yang, Xuecun <yxcun@celestica.com>
#
# Procedure Revision Details:
#   Version : 1.0  - Initial Draft  - by Yang, Xuecun <yxcun@celestica.com>
#######################################################################################################################
    def execute_check_num(self, cmd, mode=None, patterns_dict={}, path=None, expected_num=port_total,
            timeout=900, check_output=None, remark=""):
        self.wpl_log_debug('Entering procedure execute_check_num with args : %s' %(str(locals())))
        passCount = 0
        self.wpl_log_debug('path:**{}**, cmd:**{}** '.format(path, cmd))
        if path:
            self.wpl_transmit('cd ' + path)
        if check_output:
            output = check_output
        else:
            if mode:
                self.wpl_getPrompt(mode)
            finish_prompt = "{}[\s\S]+{}".format(cmd[:30].rstrip(), self.device.promptDiagOS)
            output = self.device.sendCmdRegexp(cmd + "\n", finish_prompt, timeout=timeout)
        self.wpl_log_debug('output = ***%s***' % output)
        pattern_name = list(patterns_dict.keys())[0]
        pattern = list(patterns_dict.values())[0]
        passCount = len(re.findall(pattern, output, re.M|re.S))
        cmd = cmd.strip("\n")
        if passCount == expected_num:
            self.wpl_log_success('%s is PASSED\n' %cmd)
        else:
            cmd_str = cmd
            if cmd:
                cmd_str = "while execute '{}' ".format( cmd )
            self.wpl_log_fail('Exiting execute_check_num with result FAIL. '.format(remark))
            self.wpl_raiseException("Failure {}with  item: '{}'\npass num: {}, expected num:{}".format(cmd_str,
                pattern_name, passCount, expected_num))

    def execute_check_shell_port(self, cmd, patterns_dict={}, expect_value=" ", remark=False):
        self.wpl_log_debug('Entering procedure execute_check_shell_port with args : %s' % (str(locals())))
        passCount = 0
        port_sum = 0
        self.device.sendMsg(cmd + '\n')
        time.sleep(5)
        self.device.sendMsg(Const.KEY_CTRL_C)
        finish_prompt = "{}[\s\S]+{}".format(cmd[:5], self.device.promptDiagOS)
        output = self.device.readUntil(finish_prompt, timeout=60)
        port_sum = len(re.findall(expect_value, output))
        pattern_name = list(patterns_dict.keys())[0]
        pattern = list(patterns_dict.values())[0]
        passCount = len(re.findall(pattern, output, re.M | re.S))
        if remark:
            if passCount == 0 and passCount == port_sum:
                self.wpl_log_success('%s is PASSED\n' % cmd)
            else:
                self.wpl_raiseException("execute_check_shell_port is FAIL")
        else:
            if passCount and passCount == port_sum:
                self.wpl_log_success('%s is PASSED\n' % cmd)
            else:
                self.wpl_raiseException("Exiting execute_check_shell_port with result FAIL")

#######################################################################################################################
# Function Name: check_load_HSDK
# Date         : July 31th 2020
# Author       : Yang, Xuecun <yxcun@celestica.com>
#
# Procedure Revision Details:
#   Version : 1.0  - Initial Draft  - by Yang, Xuecun <yxcun@celestica.com>
#######################################################################################################################
    def check_load_HSDK(self, cmd, pattern=[]):
        self.wpl_log_debug('Entering procedure check_load_HSDK with args : %s' %(str(locals())))
        cmd_path = "cd {}".format(SDK_PATH)
        self.device.sendCmd(cmd_path)
        time.sleep(2)
        output = self.device.sendCmdRegexp(cmd, BCM_promptstr,  timeout=20)
        check_status = self.check_output(output, patterns=pattern,remark="")
        if output.endswith(BCM_promptstr):
            self.wpl_log_info('%s is PASSED\n' %cmd)
            time.sleep(10)
        else:
            self.wpl_raiseException("%s didn't get BCM prompt %s \n" %BCM_promptstr)

    def check_load_HSDK_w400(self, cmd, pattern=[]):
        self.wpl_log_debug('Entering procedure check_load_HSDK with args : %s' %(str(locals())))
        cmd_path = "cd {}".format(SDK_PATH)
        self.device.sendCmd(cmd_path)
        time.sleep(2)
        output = self.device.sendCmdRegexp(cmd, BCM_promptstr,  timeout=20)
        check_status = self.check_output(output, patterns=pattern,remark="")
        if output.endswith(BCM_promptstr):
            self.wpl_log_info('%s is PASSED\n' %cmd)
            time.sleep(5)
            cmd1 = 'ps'
            self.device.sendCmdRegexp(cmd1, BCM_promptstr, timeout=20)
        else:
            self.wpl_raiseException("%s didn't get BCM prompt %s \n" %BCM_promptstr)

    def pcie_lsmod_check_w400(self, cmd):
        self.wpl_log_debug('Entering procedure pcie_lsmod_check_w400 with args : %s' % (str(locals())))
        self.device.sendMsg(cmd + '\n')
        finish_prompt = "{}[\s\S]+{}".format(cmd[:5], self.device.promptDiagOS)
        output = self.device.readUntil(finish_prompt, timeout=60)
        #output = self.device.sendCmdRegexp(cmd, self.device.promptDiagOS,  timeout=20)
        if 'Hardware Error' in output:
            self.wpl_raiseException("%s check the result failed, finding the HW error! \n" % cmd)

    def do_power_system_w400(self):
        self.wpl_log_debug('Entering procedure do_power_system_w400 with args : %s' % (str(locals())))
        CommonLib.switch_to_openbmc()
        time.sleep(5)
        cmd = 'wedge_power.sh reset -s'
        booting_msg = 'Starting kernel'
        self.wpl_transmit(cmd)
        output = self.device.readUntil(booting_msg, timeout=Const.BOOTING_TIME)
        time.sleep(180)
        self.wpl_getPrompt(Const.BOOT_MODE_OPENBMC, timeout=Const.BOOTING_TIME)
        self.wpl_getPrompt(Const.BOOT_MODE_CENTOS, timeout=Const.BOOTING_TIME)
        self.wpl_getPrompt(Const.BOOT_MODE_OPENBMC)
        time.sleep(10)

#######################################################################################################################
# Function Name: check_load_user
# Date         : august 28th 2020
# Author       : Yang, Xuecun <yxcun@celestica.com>
#
# Procedure Revision Details:
#   Version : 1.0  - Initial Draft  - by Yang, Xuecun <yxcun@celestica.com>
#######################################################################################################################
    def check_load_user(self, cmd, pattern_dict={}, port_sum_pattern={}, port_total=None, prompt_str=None, timeout=3600):
        self.wpl_log_debug('Entering procedure check_load_user with args : %s' %(str(locals())))
        cmd_path = "cd {}".format(SDK_PATH)
        self.wpl_sendCmd(cmd_path)
        self.device.read_until_regexp(self.device.promptDiagOS, timeout=10)
        finish_prompt = "{}[\s\S]+({}|{})".format(cmd[:5], prompt_str, self.device.promptDiagOS)
        self.device.readMsg()
        self.wpl_transmit(cmd)
        output=""
        try:
            output = self.device.read_until_regexp(finish_prompt, timeout=timeout)
        except:
            self.wpl_log_info("No match was found and timeout was reached")
            self.add_flush_and_delay(timeout=60)
            output = self.device.read_until_regexp(finish_prompt, timeout=60)
        self.execute_check_dict(cmd="", mode=None, patterns_dict=pattern_dict, timeout=50, line_mode=True, check_output=output)
        if port_sum_pattern:
            self.execute_check_num(cmd="", mode=None, patterns_dict=port_sum_pattern, path=None, expected_num=port_total,
                                   timeout=50, check_output=output, remark="")

        if output.endswith(prompt_str):
            self.wpl_log_info('%s is PASSED\n' %cmd)
        else:
            self.wpl_raiseException("Didn't get prompt %s \n" %prompt_str)


#######################################################################################################################
# Function Name: init_load_user
# Date         : Oct. 28th 2020
# Author       : Yang, Xuecun <yxcun@celestica.com>
#
# Procedure Revision Details:
#   Version : 1.0  - Initial Draft  - by Yang, Xuecun <yxcun@celestica.com>
#######################################################################################################################
    def init_load_user(self, cmd, pattern_dict={}, prompt_str=None, timeout=1200):
        self.wpl_log_debug('Entering procedure check_load_user with args : %s' %(str(locals())))
        cmd_path = "cd {}".format(SDK_PATH)
        self.wpl_transmit(cmd_path)
        self.device.read_until_regexp(self.device.promptDiagOS, timeout=10)
        finish_prompt = "{}[\s\S]+({}|{})".format(cmd[:30], prompt_str, self.device.promptDiagOS)
        self.device.readMsg()
        cmd = "{} >{}".format(cmd, tmp_output_file_on_dut)
        output = ""
        try:
            output = self.device.sendCmdRegexp(cmd, finish_prompt, timeout=timeout)
        except:
            self.wpl_log_info("No match was found and timeout was reached")
        try:
            self.exit_console_mode(previous_prompt=prompt_str, dest_prompt=self.device.promptDiagOS, exit_cmd="exit()")
        except:
            self.wpl_log_info("Didn't get '{}' or exit to prompt '{}', directly exit.".format(prompt_str, self.device.promptDiagOS))
            self.device.sendMsg("exit()")
        try:
            read_taillog_cmd = "tail -30 {}".format(tmp_output_file_on_dut)
            finish_prompt = "{}[\s\S]+({}|{})".format(read_taillog_cmd[:5], prompt_str, self.device.promptDiagOS)
            self.device.sendCmdRegexp(read_taillog_cmd, finish_prompt, timeout=15)
            cmd = "python3 /tmp/{} -t 'dict' -p '{}'".format(check_log_script_file_list[0], json.dumps(pattern_dict))
            self.execute_check_dict(cmd=cmd, mode=None, patterns_dict=check_log_pass_pattern, timeout=10, line_mode=True)
        except:
            self.wpl_raiseException("Test failed.")

#######################################################################################################################
# Function Name: exit_BCM_mode
# Date         : Aug. 3th 2020
# Author       : Yang, Xuecun <yxcun@celestica.com>
#
# Procedure Revision Details:
#   Version : 1.0  - Initial Draft  - by Yang, Xuecun <yxcun@celestica.com>
#######################################################################################################################
    def exit_BCM_mode(self):
        self.wpl_log_debug('Entering procedure exit_BCM_mode with args : %s' %(str(locals())))

        self.exit_idl_status()
        SDKLT_prompt = SDKLT_array.get("SDKLT_prompt")
        out = self.device.receive(Const.MATCH_ALL, 3)
        match = re.search(SDKLT_prompt, out)
        if match:
            self.exit_SDKLT()
        self.device.sendCmd("quit")
        output_ext = self.device.readUntil(self.device.promptDiagOS, timeout=3)
        if self.device.promptDiagOS in output_ext:
            self.wpl_log_info('Exit BCM mode is PASSED\n')
        else:
            self.wpl_raiseException("get diag OS promptstr failed . \n")
        self.stop_block_process()

#######################################################################################################################
# Function Name: exit_console_mode
# Date         : Aug. 28th 2020
# Author       : Yang, Xuecun <yxcun@celestica.com>
#
# Procedure Revision Details:
#   Version : 1.0  - Initial Draft  - by Yang, Xuecun <yxcun@celestica.com>
#######################################################################################################################
    def exit_console_mode(self, previous_prompt=None, dest_prompt=None, exit_cmd="exit()"):
        self.wpl_log_debug('Entering procedure exit_console_mode with args : %s' %(str(locals())))

        self.device.sendMsg("\r\n")
        output = self.device.read_until_regexp([previous_prompt, dest_prompt],  timeout=10)
        self.wpl_log_info("readMSG:***{}***".format(output))
        match = re.search(previous_prompt, output, re.M)
        if match:
            self.device.sendMsg("{}\r\n".format(exit_cmd))
            output_ext = self.device.read_until_regexp(dest_prompt, timeout=3)
            if re.search(dest_prompt, output_ext):
                self.wpl_log_info('Exit to %s is PASSED\n'%dest_prompt )
            else:
                self.wpl_raiseException("exit to %s promptstr failed . \n" %dest_prompt)
        else:
            self.device.sendMsg("\r\n")
            output_dst = self.device.readUntil(dest_prompt, timeout=2)
            match_dest = re.search(dest_prompt, output_dst, re.M)
            if match_dest:
                self.wpl_log_info('current prompt is already %s\n'%dest_prompt )
            self.wpl_log_info("Didn't get prompt %s, exit won't be sent. \n" %previous_prompt)


#######################################################################################################################
# Function Name: check_BCM_version
# Date         : Aug. 3th 2020
# Author       : Yang, Xuecun <yxcun@celestica.com>
#
# Procedure Revision Details:
#   Version : 1.0  - Initial Draft  - by Yang, Xuecun <yxcun@celestica.com>
#######################################################################################################################
    def check_BCM_version(self):
        self.wpl_log_debug('Entering procedure check_BCM_version with args : %s' %(str(locals())))
        # output = self.device.readMsg()
        # match = re.search(BCM_promptstr, output, re.M)
        # if match:
        self.device.sendCmd("version")
        output_ext = self.device.read_until_regexp(BCM_promptstr, timeout=10)
        match_version = re.search(BCM_VERSION, output_ext, re.M)
        if match_version:
            self.wpl_log_info('checking BCM version is PASSED\n')
        else:
            self.wpl_raiseException("Checking BCM version failed . \n")
        # else:
        #     self.wpl_log_info("Didn't get BCM prompt %s \n" %BCM_promptstr)


#######################################################################################################################
# Function Name: enter_SDKLT
# Date         : Aug. 3th 2020
# Author       : Yang, Xuecun <yxcun@celestica.com>
#
# Procedure Revision Details:
#   Version : 1.0  - Initial Draft  - by Yang, Xuecun <yxcun@celestica.com>
#######################################################################################################################
    def enter_SDKLT(self):
        self.wpl_log_debug('Entering procedure enter_SDKLT with args : %s' %(str(locals())))
        SDKLT_prompt = SDKLT_array.get("SDKLT_prompt")
        self.device.sendCmd(SDKLT_array.get("SDKLT_tool", ""))
        output_ext = self.device.readUntil(SDKLT_prompt, timeout=3)
        if output_ext.endswith(SDKLT_array.get("SDKLT_prompt")):
            self.wpl_log_info('enter_SDKLT is successful\n')
        else:
            self.wpl_raiseException("enter_SDKLT failed, output:{} . \n".format(output_ext))


#######################################################################################################################
# Function Name: check_PCIe_version
# Date         : Aug. 3th 2020
# Author       : Yang, Xuecun <yxcun@celestica.com>
#
# Procedure Revision Details:
#   Version : 1.0  - Initial Draft  - by Yang, Xuecun <yxcun@celestica.com>
#######################################################################################################################
    def check_PCIe_version(self):
        self.wpl_log_debug('Entering procedure check_PCIe_version with args : %s' %(str(locals())))
        SDKLT_prompt = SDKLT_array.get("SDKLT_prompt")
        PCIE_CMD = SDKLT_array["PCIE_INFO_CMD"]
        PCIE_VERSION = SDKLT_array["PCIe_version"]
        self.wpl_log_debug('//////pcie version = %s //////' % PCIE_VERSION)
        self.device.sendCmd(PCIE_CMD)
        output_ext = self.device.readUntil(SDKLT_prompt, timeout=5)
        match_version = re.search(PCIE_VERSION, output_ext, re.M)
        if match_version:
            self.wpl_log_info('check_PCIe_version is PASSED\n')
        else:
            self.wpl_raiseException("Check PCIe FW version failed, expected: {} . \n".format(PCIE_VERSION))


#######################################################################################################################
# Function Name: exit_SDKLT
# Date         : Aug. 3th 2020
# Author       : Yang, Xuecun <yxcun@celestica.com>
#
# Procedure Revision Details:
#   Version : 1.0  - Initial Draft  - by Yang, Xuecun <yxcun@celestica.com>
#######################################################################################################################
    def exit_SDKLT(self):
        self.wpl_log_debug('Entering procedure enter_SDKLT with args : %s' %(str(locals())))
        SDKLT_prompt = SDKLT_array.get("SDKLT_prompt")

        self.device.sendCmd("quit")
        output_ext = self.device.readUntil(BCM_promptstr, timeout=3)
        if output_ext.endswith(BCM_promptstr):
            self.wpl_log_info('exit_SDKLT is successful\n')
        else:
            self.wpl_raiseException("exit_SDKLT failed, output:{} . \n".format(output_ext))


#######################################################################################################################
# Function Name: startup_default_port
# Date         : Aug. 3th 2020
# Author       : Yang, Xuecun <yxcun@celestica.com>
#
# Procedure Revision Details:
#   Version : 1.0  - Initial Draft  - by Yang, Xuecun <yxcun@celestica.com>
#######################################################################################################################
    def startup_default_port(self, use_xphyback=True, init_cmd=None):
        self.wpl_log_debug('Entering procedure startup_default_port with args : %s' %(str(locals())))
        check_status = 0
        cmd = ""
        output = ""
        check_xphy_cmd = "p_num=`ps -ef |grep xphyback |grep -v grep |wc -l`"
        output += self.run_command(check_xphy_cmd, deviceObj=self.device)
        if use_xphyback:
            cpu_tech_name = self.get_cpu_tech()
            xphyback = xphyback_dict.get(cpu_tech_name)
            cmd = "./{}& sleep 5; ".format(xphyback)
            output += self.run_command(cmd, deviceObj=self.device)
        if use_xphyback and init_cmd:
            cmd = 'sleep 1; [ "$p_num" -eq "0" ] && {} ;'.format(init_cmd)
        elif use_xphyback == False and init_cmd:
            cmd = init_cmd
        #devicename = os.environ.get("deviceName", "")
        #if 'minipack2_dc' in devicename.lower():
        #    if 'seq 3 6' in cmd:
        #        return
        output += self.run_command(cmd, deviceObj=self.device, timeout=3600)
        check_xphy_cmd = "sleep 2; ps -ef |grep xphyback |grep -v grep "
        output += self.run_command(check_xphy_cmd, deviceObj=self.device)
        check_status = self.check_output(output, patterns=fail_pattern, line_mode=True,
                is_negative_test=True, remark="startup_default_port")

        if check_status:
            self.wpl_log_info('startup_default_port is passed\n')
        else:
            self.wpl_raiseException("startup_default_port failed")

#######################################################################################################################
    # Function Name: verify_TH4L
    # Date         : Apr. 26th 2021
    # Author       : Eric Zhang <zfzhang@celestica.com>
    #
    # Procedure Revision Details:
    #   Version : 1.0  - Initial Draft  - by Eric Zhang <zfzhang@celestica.com>
#######################################################################################################################
    def verify_TH4L(self, verify_th4L_command):
        CommonLib.switch_to_centos()
        time.sleep(2)
        fin_len = ''
        output = self.device.executeCmd(verify_th4L_command, timeout=60)
        self.wpl_log_info("/////output=%s ///////" % output)
        if 'b992' in output:
            fin_len = len_600
        else:
            fin_len = len_295
        return fin_len

#######################################################################################################################
# Function Name: verify_all_port_status
# Date         : Aug. 4th 2020
# Author       : Yang, Xuecun <yxcun@celestica.com>
#
# Procedure Revision Details:
#   Version : 1.0  - Initial Draft  - by Yang, Xuecun <yxcun@celestica.com>
#######################################################################################################################
    def mp2_pim_number(self):
        self.wpl_log_debug('Entering procedure mp2_pim_number with args : %s' % (str(locals())))
        pim_count_na = 0
        CommonLib.switch_to_openbmc()
        cmd = "fpga_ver.sh"
        self.device.sendMsg(cmd + '\n')
        finish_prompt = "{}[\s\S]+{}".format(cmd[:5], self.device.promptBmc)
        output = self.device.readUntil(finish_prompt, timeout=100)
        p1 = r'DOMFPGA is not detected'
        for line in output.splitlines():
            mat = re.search(p1, line)
            if mat:
                pim_count_na += 1
        CommonLib.switch_to_centos()
        return pim_count_na

    def port_lb_mac_set(self, port_type, pim_NA_sum):
        self.wpl_log_debug('Entering procedure port_lb_mac_set with args : %s' % (str(locals())))
        if pim_NA_sum == 4:
            if port_type == '200G':
                cmd = lb_mac_pimNum4_200G_200G
                self.device.sendMsg(cmd + '\n')
                time.sleep(2)
            elif port_type == '400G':
                cmd = lb_mac_pimNum4_400G_200G
                self.device.sendMsg(cmd + '\n')
                time.sleep(2)
            elif port_type == '100G':
                cmd = lb_mac_pimNum4_200G_100G
                self.device.sendMsg(cmd + '\n')
                time.sleep(2)
        elif pim_NA_sum == 3:
            if port_type == '200G':
                cmd = lb_mac_pimNum5_200G_200G
                self.device.sendMsg(cmd + '\n')
                time.sleep(2)
            elif port_type == '400G':
                cmd = lb_mac_pimNum5_400G_200G
                self.device.sendMsg(cmd + '\n')
                time.sleep(2)
            elif port_type == '100G':
                cmd = lb_mac_pimNum5_200G_100G
                self.device.sendMsg(cmd + '\n')
                time.sleep(2)
        output = self.device.readUntil(BCM_promptstr, timeout=100)

    def verify_all_port_status(self, port_status_pattern=port_up_status, port_cmd=ps_cd_cmd,
            port_search_pattern=port_pattern, prompt_str=BCM_promptstr):
        self.wpl_log_debug('Entering procedure verify_all_port_status with args : %s' %(str(locals())))
        self.device.sendMsg(port_cmd+'\n')
        finish_prompt = "{}[\s\S]+{}".format(port_cmd[:5], prompt_str)
        output = self.device.readUntil(finish_prompt, timeout=100)
        port_status_pattern = ".*?".join(port_status_pattern)
        port_status_count = len(re.findall(port_status_pattern, output))
        #devicename = os.environ.get("deviceName", "")
        #if 'minipack2_dc' in devicename.lower():
        #    if 'down' in port_status_pattern:
        #        port_search_pattern = port_pattern_dc_down
        #    else:
        #        port_search_pattern = port_pattern_dc
        #mat = re.findall(port_search_pattern, output)
        #self.wpl_log_info(port_search_pattern)
        #self.wpl_log_info(mat)
        port_sum = len(re.findall(port_search_pattern, output))
        if port_sum == 0:
            self.wpl_raiseException("Didn't find port info")

        if port_sum == port_status_count:
            self.wpl_log_info('verify_all_port_status is passed, pass number is %d\n'%(port_sum))
        else:
            self.wpl_raiseException("Normal ports:{}, total ports:{} \n".format(port_status_count, port_sum))

    def verify_all_port_status_w400(self, port_cmd=ps_cd_cmd, port_rpkt=" ",
            port_tpkt=" ", prompt_str=BCM_promptstr):
        self.wpl_log_debug('Entering procedure verify_all_port_status_w400 with args : %s' % (str(locals())))
        rp_lst = []
        tp_lst = []
        self.device.sendMsg(port_cmd + '\n')
        finish_prompt = "{}[\s\S]+{}".format(port_cmd[:5], prompt_str)
        output = self.device.readUntil(finish_prompt, timeout=100)
        rp_len = len(re.findall(port_rpkt, output))
        tp_len = len(re.findall(port_tpkt, output))
        if rp_len and tp_len == rp_len:
            rp_lst = re.findall(port_rpkt, output)
            tp_lst = re.findall(port_tpkt, output)
            if rp_lst and rp_lst == tp_lst:
                self.wpl_log_info('The value is the same\n')
            else:
                self.wpl_raiseException("The value is different\n")
        else:
            self.wpl_raiseException("Didn't find port info")

    def verify_all_port_status_w400_th3(self, port_cmd=ps_cd_cmd, port_rpkt=" ",
            port_tpkt=" ", prompt_str=BCM_promptstr):
        self.wpl_log_debug('Entering procedure verify_all_port_status_w400_th3 with args : %s' % (str(locals())))
        rp_lst = []
        tp_lst = []
        self.device.sendMsg(port_cmd + '\n')
        finish_prompt = "{}[\s\S]+{}".format(port_cmd[:5], prompt_str)
        output = self.device.readUntil(finish_prompt, timeout=100)
        for line in output.splitlines():
            match_rp = re.search(port_rpkt, line)
            match_tp = re.search(port_tpkt, line)
            if match_rp:
                rp_lst.append(match_rp.group(1))
                rp_lst.append(match_rp.group(2))
            if match_tp:
                tp_lst.append(match_tp.group(1))
                tp_lst.append(match_tp.group(2))
        if rp_lst and rp_lst == tp_lst:
            self.wpl_log_info('The value is the same\n')
        else:
            self.wpl_raiseException("The value is different\n")

    def check_show_temp(self, temp_cmd=" ", avg_temp=" ", max_temp=" ", prompt_str=BCM_promptstr):
        self.wpl_log_debug('Entering procedure check_show_temp with args : %s' % (str(locals())))
        self.device.sendMsg(temp_cmd + '\n')
        finish_prompt = "{}[\s\S]+{}".format(temp_cmd[:7], prompt_str)
        output = self.device.readUntil(finish_prompt, timeout=100)
        aver_match = re.search(avg_temp, output)
        max_match = re.search(max_temp, output)
        if aver_match:
            aver_temp_value = float(aver_match.group(1))
        if max_match:
            max_temp_value = float(max_match.group(1))
        self.wpl_log_info("get the averge value is {}, max value is {}".format(aver_temp_value, max_temp_value))
        return [aver_temp_value, max_temp_value]

    def check_value_cmp(self, first_value, sencond_value):
        self.wpl_log_debug('Entering procedure check_value_cmp with args : %s' % (str(locals())))
        if first_value < sencond_value:
            self.wpl_log_info('check_value_cmp is passed\n')
        else:
            self.wpl_raiseException("Check fail, Normal value:{}, high value:{} \n".format(first_value, sencond_value))

    def check_lst_cmp(self, normal, traffic, traffic_after):
        self.wpl_log_debug('Entering procedure check_lst_cmp with args : %s' % (str(locals())))
        if normal<traffic and normal<traffic_after and traffic>traffic_after:
            self.wpl_log_info('check_lst_cmp is passed\n')
        else:
            self.wpl_raiseException("Check fail, Normal value:{}, traffic value:{}, traffic_after value:{} \n".format(normal, traffic, traffic_after))

#######################################################################################################################
# Function Name: change_ports_status
# Date         : Aug. 5th 2020
# Author       : Yang, Xuecun <yxcun@celestica.com>
#
# Procedure Revision Details:
#   Version : 1.0  - Initial Draft  - by Yang, Xuecun <yxcun@celestica.com>
#######################################################################################################################
    def change_ports_status(self, port_config_cmd=port_disable_cmd):
        self.wpl_log_debug('Entering procedure change_ports_status with args : %s' %(str(locals())))
        self.device.sendMsg("\r\n")
        output = self.device.readMsg()
        self.wpl_log_info("{}".format(output))
        for cmd in port_config_cmd.split("\n"):
            self.device.sendCmd(cmd)
            time.sleep(8)

    def get_th3_core_power(self, port_cmd=" "):
        self.wpl_log_debug('Entering procedure get_th3_core_power with args : %s' %(str(locals())))
        core_th3_value = ''
        self.device.sendMsg("\r\n")
        for cmd in port_cmd.split("\n"):
            self.device.sendCmd(cmd)
            time.sleep(8)
        finish_prompt = "{}[\s\S]+{}".format(port_cmd[:5], self.device.promptBmc)
        output = self.device.readUntil(finish_prompt, timeout=100)
        # th3_core_value = re.findall(r'TH3 Core Output Power\:\s+([\d\.]+) W', output)
        for line in output.splitlines():
            match = re.search(r'TH3 Core Output Power:\s+(.*) W', line)
            if match:
                core_th3_value = match.group(1)
        self.wpl_log_info('get th3 core value is: %s'%(core_th3_value))
        return float(core_th3_value)

    def change_to_sdk_bcm(self, cmd, prompt_str=BCM_promptstr):
        self.wpl_log_debug('Entering procedure change_to_sdk_bcm with args : %s' % (str(locals())))
        self.device.sendCmd(cmd)
        time.sleep(3)
        self.device.sendMsg("\r\n")
        output = self.device.readUntil(prompt_str, timeout=100)


#######################################################################################################################
# Function Name: check_port_PRBS
# Date         : Aug. 6th 2020
# Author       : Yang, Xuecun <yxcun@celestica.com>
#
# Procedure Revision Details:
#   Version : 1.0  - Initial Draft  - by Yang, Xuecun <yxcun@celestica.com>
#######################################################################################################################
    def check_port_PRBS(self, port_pattern=PRBS_port_pattern):
        self.wpl_log_debug('Entering procedure check_port_PRBS with args : %s' %(str(locals())))
        self.change_ports_status(port_config_cmd=get_port_PRBS_status_cmd)
        time.sleep(25)
        self.change_ports_status(port_config_cmd=get_port_PRBS_status_cmd)
        prompt_str = SDKLT_array["SDKLT_prompt"]
        output = self.device.readUntil(prompt_str, timeout=100)
        fail_port = []
        match_flag = 0
        for line in output.splitlines():
            match = re.search(port_pattern, line)
            if match:
                match_flag = 1
                port_no = match.group(1)
                port_status = match.group(2)
                if port_no in port_exclude:
                    continue
                if PRBS_ok not in port_status:
                    fail_port.append(port_no)

        if fail_port or match_flag == 0:
            self.wpl_raiseException("{} failed with ports:{}".format(get_port_PRBS_status_cmd, fail_port))
        else:
             self.wpl_log_success("{}".format(get_port_PRBS_status_cmd))

#######################################################################################################################
# Function Name: check_port_BER
# Date         : Aug. 6th 2020
# Author       : Yang, Xuecun <yxcun@celestica.com>
#
# Procedure Revision Details:
#   Version : 1.0  - Initial Draft  - by Yang, Xuecun <yxcun@celestica.com>
#######################################################################################################################
    def check_port_BER(self, level_cmd=set_prbs_run_PRBS_cmd, level_cmd_second=get_port_BER_level_cmd_second, port_pattern=BER_port_pattern, value_tolerance=port_BER_tolerance):
        self.wpl_log_debug('Entering procedure check_port_BER with args : %s' %(str(locals())))
        prompt_str = SDKLT_array["SDKLT_prompt"]
        finish_prompt = "{}[\s\S]+{}".format(level_cmd[:5], prompt_str)
        self.change_ports_status(port_config_cmd=level_cmd)
        time.sleep(25)
        output = self.device.read_until_regexp(finish_prompt, timeout=100)
        self.change_ports_status(port_config_cmd=level_cmd_second)
        output += self.device.read_until_regexp(finish_prompt, timeout=100)
        fail_port = []
        match_flag = 0
        for line in output.splitlines():
            match = re.search(port_pattern, line)
            if match:
                match_flag = 1
                port_no = match.group(1)
                BER_value = float(match.group(2))
                if port_no in port_exclude:
                    continue
                if BER_value >= port_BER_tolerance:
                    fail_port.append(port_no)

        if fail_port:
            self.wpl_raiseException("{} failed with ports:{}".format(get_port_BER_level_cmd, fail_port))
        elif match_flag == 0:
            self.wpl_raiseException("Command failed with didn't match ports information")
        else:
             self.wpl_log_success("{}".format(get_port_BER_level_cmd))

#######################################################################################################################
# Function Name: read_and_check_port
# Date         : Aug. 7th 2020
# Author       : Yang, Xuecun <yxcun@celestica.com>
#
# Procedure Revision Details:
#   Version : 1.0  - Initial Draft  - by Yang, Xuecun <yxcun@celestica.com>
#######################################################################################################################
    def read_and_check_port(self, patterns, is_negative_test=True):
        self.wpl_log_debug('Entering procedure read_and_check_port with args : %s' %(str(locals())))
        output = ""
        for i in range(10):
            time.sleep(10)
            output += self.device.readMsg()
            if output.rstrip().endswith(".0>"):
                break
        self.check_output(output, patterns=patterns, is_negative_test=is_negative_test)

#######################################################################################################################
# Function Name: check_XLMIB_RPKT
# Date         : Aug. 7th 2020
# Author       : Yang, Xuecun <yxcun@celestica.com>
#
# Procedure Revision Details:
#   Version : 1.0  - Initial Draft  - by Yang, Xuecun <yxcun@celestica.com>
#######################################################################################################################
    def check_XLMIB_RPKT(self, pattern=port_XLMIB_RPKT_pattern, output=""):
        self.wpl_log_debug('Entering procedure check_XLMIB_RPKT with args : %s' %(str(locals())))
        match_flag = 0
        first_data = []
        for line in output.splitlines():
            match = re.search(pattern, line)
            if match:
                match_flag = 1
                port_no = match.group(1)
                value1 = match.group(2)
                value2 = match.group(3)
                data = [port_no, value1, value2]
                if not first_data:
                    first_data = data
                elif first_data[1:] != data[1:]:
                    self.wpl_raiseException("Ports data is different:{} <==> {}".format(first_data, data))

        if match_flag == 0:
            self.wpl_raiseException("Port data is not found.")


#######################################################################################################################
# Function Name: check_lane_common_version
# Date         : Aug. 10th 2020
# Author       : Yang, Xuecun <yxcun@celestica.com>
#
# Procedure Revision Details:
#   Version : 1.0  - Initial Draft  - by Yang, Xuecun <yxcun@celestica.com>
#######################################################################################################################
    def check_lane_common_version(self, patterns, description="Lane Common Ucode Version"):
        self.wpl_log_debug('Entering procedure check_lane_common_version with args : %s' %(str(locals())))
        SDKLT_prompt = SDKLT_array["SDKLT_prompt"]
        finish_prompt = "{}[\s\S]+{}".format(get_lane_serdes_version_cmd[:5], SDKLT_prompt)
        output = self.device.read_until_regexp(finish_prompt, timeout=1000)
        match_flag = 0
        first_data = []
        lane_num = ""
        common_version = ""
        for line in output.splitlines():
            match_lane = re.search(patterns[0], line)
            match_version = re.search(patterns[1], line)
            if match_lane:
                lane_num = match_lane.group(1)
            if match_version:
                match_flag = 1
                version = match_version.group(1)
                data = [lane_num, version]
                if not first_data:
                    first_data = data
                elif first_data[1:] != data[1:]:
                    self.wpl_raiseException("{} is different:{} <==> {}".format(description, first_data, data))

        if match_flag == 0:
            self.wpl_raiseException("{} data is not found.".format(description))

#######################################################################################################################
# Function Name: disconnect_device
# Date         : Oct. 9th 2020
# Author       : Yang, Xuecun <yxcun@celestica.com>
#
# Procedure Revision Details:
#   Version : 1.0  - Initial Draft  - by Yang, Xuecun <yxcun@celestica.com>
#######################################################################################################################
    def disconnect_device(self):
        self.wpl_log_debug('Entering procedure disconnect_device with args : %s' %(str(locals())))
        self.wpl_flush()
        #wait for long time command's termination
        self.wpl_getPrompt('centos', timeout=1800)
        self.device.readMsg()
        self.device.sendMsg("\r\n")
        time.sleep(0.5)
        prompt = self.device.readMsg()
        for exit_cmd, promptstr in prompt_dict.items():
            promptstr = "{}".format(promptstr)
            match = re.search(promptstr, prompt)
            if match:
                self.device.sendCmd(exit_cmd)
                break

        #use a common command to withdraw from unusual status
        self.wpl_transmit('ls ')
        self.wpl_flush()
        time.sleep(5)

        self.device.sendCmd("\x03")
        self.device.disconnect()

#######################################################################################################################
# Function Name: change_NIC
# Date         : Oct. 9th 2020
# Author       : Yang, Xuecun <yxcun@celestica.com>
#
# Procedure Revision Details:
#   Version : 1.0  - Initial Draft  - by Yang, Xuecun <yxcun@celestica.com>
#######################################################################################################################
    def change_NIC(self, NIC="usb0", state="up"):
        self.wpl_log_debug('Entering procedure change_NIC with args : %s' %(str(locals())))
        self.wpl_getPrompt('centos', timeout=5)
        cmd = "ip addr"
        finish_prompt = "{}[\s\S]+{}".format(cmd[:30].rstrip(), self.device.promptDiagOS)
        output = self.device.sendCmdRegexp(cmd, finish_prompt, timeout=10)
        p = "{}.*?state\s+(\w+)".format(NIC)
        match = re.search(p, output)
        if match:
            current_state = match.group(1)
            if current_state.lower() != state:
                cmd = "ifconfig {} {}".format(NIC, state)
                self.device.sendCmd(cmd)
                time.sleep(5)
                cmd = "ip addr"
                finish_prompt = "{}[\s\S]+{}".format(cmd[:30].rstrip(), self.device.promptDiagOS)
                output = self.device.sendCmdRegexp(cmd, finish_prompt, timeout=5)
                match = re.search(p, output)
                current_state = match.group(1)
                if current_state.lower() == state:
                    log.cprint('Change {} to {} succceded'.format(NIC, state))
                else:
                    log.cprint('Change {} to {} failed, current state: {}'.format(NIC, state, current_state))
            else:
                log.cprint('{} is already {}'.format(NIC, state))
        else:
            log.cprint('Enthernet interface {} is not found'.format(NIC))

#######################################################################################################################
# Function Name: get_CPU_tech
# Date         : Oct. 12th 2020
# Author       : Yang, Xuecun <yxcun@celestica.com>
#
# Procedure Revision Details:
#   Version : 1.0  - Initial Draft  - by Yang, Xuecun <yxcun@celestica.com>
#######################################################################################################################
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

#######################################################################################################################
# Function Name: prepare_check_log_script
# Date         : Oct. 27th 2020
# Author       : Yang, Xuecun <yxcun@celestica.com>
#
# Procedure Revision Details:
#   Version : 1.0  - Initial Draft  - by Yang, Xuecun <yxcun@celestica.com>
#######################################################################################################################
    def create_check_log_script(self, script_file=check_log_script_file_list[0]):
        self.wpl_log_debug('Entering procedure  create_check_log_script')
        cmd = """
cat >{}  <<'EOF'""".format(os.path.join(check_log_script_file_dst_path, script_file))
        cmd += """
#!/usr/bin/env python3
#coding:utf-8
import argparse
import os
import sys
import re
import json

pattern_type_choices = ["str", "list", "dict"]
parser = argparse.ArgumentParser(description="Check log with pattern")
parser.add_argument("-t", "--pattern_type", type=str, default="str", choices=pattern_type_choices)
parser.add_argument("-f", "--pattern_flag", type=str, default="re.S")
parser.add_argument("-p", "--pattern", type=str)
parser.add_argument("-l", "--log_file", type=os.path.expanduser, default="/tmp/dut_output")
parser.add_argument("-m", "--pass_messsage", type=str, default="Checking log PASSED")
parser.add_argument("-ps", "--positive_search", action="store_false")
args = parser.parse_args()

log_file = args.log_file
pattern_type = args.pattern_type
pattern_flag = args.pattern_flag
pass_message = args.pass_messsage
pattern = args.pattern
positive_search = args.positive_search

def check_with_str(log, pattern, pattern_flag, positive_search=True):
    if pattern_flag:
        match = re.search(pattern, log, eval(pattern_flag))
    else:
        match = re.search(pattern, log)
    pass_flag = 0
    if match:
        if positive_search:
            pass_flag = 1
    else:
        if not positive_search:
            pass_flag = 1
    log_tail_30 = log.splitlines()[-30:]
    log_tail_30 = "\\n".join(log_tail_30)
    if pass_flag:
        print("Tail log: ==={}===".format(log_tail_30))
        print(pass_message)
    else:
        print("Tail log: ==={}===".format(log_tail_30))
        print("Checking log FAILED")

    return pass_flag

def check_with_dict(log, patterns, pattern_flag, positive_search=True):
    pass_flag = 0
    match_count = 0
    match_list = []
    mismatch_keys = []
    if not isinstance(patterns, dict):
        print("Checking log FAILED, pattern is not dict.")
        return pass_flag

    pattern_count = len(patterns)
    for key, pattern in patterns.items():

        if pattern_flag:
            match = re.search(pattern, log, eval(pattern_flag))
        else:
            match = re.search(pattern, log)
        if match:
            match_list.append(key)
            match_count += 1
    if positive_search:
        if pattern_count == match_count:
            pass_flag = 1
        else:
            mismatch_keys = list(set(patterns.keys()) - set(match_list))
    else:
        if match_count > 0:
            mismatch_keys = match_list
        else:
            pass_flag = 1

    log_tail_30 = log.splitlines()[-30:]
    log_tail_30 = "\\n".join(log_tail_30)
    if pass_flag:
        print("Tail log: ==={}===".format(log_tail_30))
        print(pass_message)
    else:
        print("Tail log: ==={}===".format(log_tail_30))
        print("Checking log FAILED with items : {}".format(mismatch_keys))

    return pass_flag

def check_with_list(log, patterns, pattern_flag, positive_search=True):
    pass_flag = 0
    match_count = 0
    match_list = []
    mismatch_keys = []
    if not isinstance(patterns, list):
        print("Checking log FAILED, pattern is not list.")
        return pass_flag

    pattern_count = len(patterns)
    for pattern in patterns:

        if pattern_flag:
            match = re.search(pattern, log, eval(pattern_flag))
        else:
            match = re.search(pattern, log)
        if match:
            match_list.append(pattern)
            match_count += 1
    if positive_search:
        if pattern_count == match_count:
            pass_flag = 1
        else:
            mismatch_keys = list(set(patterns) - set(match_list))
    else:
        if match_count > 0:
            mismatch_keys = match_list
        else:
            pass_flag = 1

    log_tail_30 = log.splitlines()[-30:]
    log_tail_30 = "\\n".join(log_tail_30)
    if pass_flag:
        print("Tail log: ==={}===".format(log_tail_30))
        print(pass_message)
    else:
        replace_dict = {".*":" ", "?":"", "+":"", "\\t":" ", "[":"", "]":"", "\s":"", "\S":""}
        mismatch_str = ",".join(mismatch_keys)
        for key,value in replace_dict.items():
            mismatch_str = mismatch_str.replace(key, value)
        print("Tail log: ==={}===".format(log_tail_30))
        print("Checking log FAILED with items : {}".format(mismatch_str))

    return pass_flag

if not os.path.isfile(log_file):
    print("Error: {} is not existed".format(log_file))
    sys.exit()
else:
    log_content = ""
    with open(log_file, 'r') as fh:
        log_content = fh.read()

if pattern_type == "str":
    check_with_str(log_content, pattern, pattern_flag, positive_search)
elif pattern_type == "dict":
    pattern_dict = json.loads(pattern)
    check_with_dict(log_content, pattern_dict, pattern_flag, positive_search)
elif pattern_type == "list":
    pattern_list = json.loads(pattern)
    check_with_list(log_content, pattern_list, pattern_flag, positive_search)
else:
    print("Pattern only supports str, dict and list, The type {}".format(pattern_type))

EOF
        """
        try:
            self.device.sendCmdRegexp(cmd, self.device.promptDiagOS, timeout=10)
        except:
            self.device.sendCmd("\x03")
            try:
                self.device.sendCmdRegexp(cmd, self.device.promptDiagOS, timeout=10)
            except:
                self.device.sendCmd("\x03")
    @logThis
    def exit_idl_status(self):
        try:
            self.device.sendCmdRegexp('quit', self.device.promptDiagOS, timeout=3)
        except:
            self.device.sendCmd("\x03")
            try:
                self.device.sendCmdRegexp('quit', self.device.promptDiagOS, timeout=3)
            except:
                self.device.sendCmd("\x03")

    @logThis
    def stop_block_process(self):
        output = self.device.executeCmd(check_bcm_user, timeout=5)
        lines = output.splitlines()
        for line in lines:
            if re.search('bcm.user -y', line):
                w = re.findall(r'\w+', line)
                self.device.sendCmd('kill -9 ' + w[1])
                break
        # self.wpl_execute_cmd(clean_xphy)


