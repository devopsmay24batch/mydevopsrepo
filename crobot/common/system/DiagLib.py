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
import Logger as log
from functools import partial
from Decorator import *
import re
import Logger as log
import CommonLib
import CommonKeywords
import Const
import time
from DiagLibAdapter import *
from Diag_OS_variable import *
from datetime import datetime
from dataStructure import nestedDict, parser
from SwImage import SwImage
from pexpect import pxssh


import getpass
try:
    from Device import Device
    import DeviceMgr
    import Const
    import CommonLib
    from Diag_OS_variable import *


except Exception as err:
    log.cprint(str(err))

device = DeviceMgr.getDevice()

run_command = partial(CommonLib.run_command, deviceObj=device, prompt=device.promptDiagOS)
time.sleep(10)





class DiagLib:
    def __init__(self, device):
        self.device = DeviceMgr.getDevice()


    # connection related API
    def loginDevice(self):
        log.debug("Entering DiagLib class procedure: loginDevice")
        return self.device.login()


    def disconnectDevice(self):
        log.debug("Entering DiagLib class procedure: disconnectDevice")
        return self.device.disconnect()


    def ssh_login_bmc(self):
        CommonLib.ssh_login_bmc(Const.DUT)
        self.device = DeviceMgr.getDevice()


    def ssh_disconnect(self):
        CommonLib.ssh_disconnect(Const.DUT)
        self.device = DeviceMgr.getDevice()


    # power cycle related wrapper API
    def wpl_powerCycleDeviceToDiagOS(self):
        log.debug("Entering DiagLib class procedure: powerCycleDeviceToDiagOS")
        output = self.wpl_powerCycleDevice()
        output1 = self.wpl_waitForDiagPrompt()
        output += output1
        return output


    def wpl_powerCycleDeviceToOnie(self):
        log.debug("Entering DiagLib class procedure: powerCycleDeviceToOnie")
        output = self.wpl_powerCycleDevice()
        output1 = self.wpl_waitForOniePrompt()
        output += output1
        return output


    def wpl_powerCycleDeviceToCentOS(self):
        log.debug("Entering DiagLib class procedure: powerCycleDeviceToCentOS")
        output = self.wpl_powerCycleDevice()
        output1 = self.wpl_waitForCentOSPrompt()
        output += output1
        return output


    def wpl_powerCycleDeviceToOpenBmc(self):
        log.debug("Entering DiagLib class procedure: powerCycleDeviceToOpenBmc")
        output = self.wpl_powerCycleDevice()    
        output1 = self.wpl_waitForOpenBmcPrompt()
        output += output1
        return output


    def wpl_powerCycleDevice(self):
        log.debug("Entering DiagLib class procedure: powerCycleDevice")
        return self.device.powerCycleDevice()


   ### boot mode related wrapper APIs
    def wpl_grubBootIntoDiagOS(self):
        log.debug("Entering DiagLib class procedure: grubBootIntoDiagOS")
        return self.device.grubBootIntoDiagOS()


    def wpl_grubBootIntoOnie(self):
        log.debug("Entering DiagLib class procedure: grubBootIntoOnie")
        return self.device.grubBootIntoOnieEnv()


    def wpl_bootIntoOnieInstallMode(self):
        log.debug("Entering DiagLib class procedure: bootIntoOnieInstallMode")
        return self.device.bootIntoOnieInstallMode()


    def wpl_bootIntoOnieRescueMode(self):
        log.debug("Entering DiagLib class procedure: bootIntoOnieRescueMode")
        return self.device.bootIntoOnieRescueMode()


    def wpl_bootIntoDiagOS(self):
        log.debug("Entering DiagLib class procedure: bootIntoDiagOS")
        return self.device.bootIntoDiagOS()


    def wpl_bootIntoBios(self):
        log.debug("Entering DiagLib class procedure: bootIntoBios")
        return self.device.bootIntoDiagOS()


    def wpl_getCurrentBootMode(self):
         return self.device.getCurrentBootMode()


    ### wait prompt related wrapper APIs
    def wpl_waitForDiagPrompt(self):
        log.debug("Entering DiagLib class procedure: waitForDiagPrompt")
        output = self.wpl_waitForGrubPrompt()
        output1 = self.wpl_grubBootIntoDiagOS()
        output += output1
        return output


    def wpl_waitForOniePrompt(self):
        log.debug("Entering DiagLib class procedure: waitForOniePrompt")
        output = self.wpl_waitForGrubPrompt()
        output1 = self.wpl_grubBootIntoOnie()
        output += output1
        return output


    def wpl_waitForCentOSPrompt(self):
        log.debug("Entering DiagLib class procedure: waitForCentOSPrompt")
        output = self.device.waitForLoginPrompt("centos", 600)
        return output


    def wpl_waitForOpenBmcPrompt(self):
        log.debug("Entering DiagLib class procedure: waitForOpenBmcPrompt")
        output = self.device.waitForLoginPrompt("openbmc", 600)
        return output


    def wpl_waitForGrubPrompt(self):
        log.debug("Entering DiagLib class procedure: waitForGrubPrompt")
        return self.device.waitForGrubPrompt()


    def wpl_getPrompt(self, mode=None, timeout=60, idleTimeout=60, logFile='None'):
        return self.device.getPrompt(mode, timeout, idleTimeout, logFile)


    def wpl_getCurrentPromptStr(self):
        return self.device.getCurrentPromptStr()


    def wpl_getDiagOSPromptStr(self):
        return self.device.promptDiagOS


    def wpl_getBmcPromptStr(self):
        return self.device.promptBmc


    ### send/receive related wrapper APIs ###
    def wpl_sendline(self, cmd, CR=True):
        if (CR == True):
            msg = (cmd + '\r')
        else:
            msg = cmd
        return self.device.sendMsg(msg)


    def wpl_transmit(self, cmd, CR=True):
        return self.wpl_sendline(cmd, CR)


    def wpl_sendCmd(self, cmd, prompt):
        return self.device.sendCmd(cmd, prompt)


    def wpl_execute(self, cmd, mode=None, timeout=60):
        return self.device.execute(cmd, mode, timeout)

    def wpl_execute_cmd(self, cmd, mode=None, timeout=60):
        return self.device.executeCmd(cmd, mode, timeout)

    def wpl_receive(self, rcv_str, timeout=60):
        return self.device.receive(rcv_str, timeout)


    def wpl_flush(self):
        return self.device.flush()


    def wpl_exec_local_cmd(self, cmd, timeout=10):
        return self.device.execute_local_cmd(cmd, timeout)


    def wpl_sendCmdRegexp(self, cmd, promptRegexp, timeout=300):
        return self.device.sendCmdRegexp(cmd, promptRegexp, timeout)


    ### log related wrapper APIs ###
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


    def wpl_enable_terminal_log_file(self, enable_flag):
        return self.device.set_terminal_log_file(enable_flag)


    def wpl_disable_terminal_log_file(self, disable_flag):
        return self.device.set_terminal_log_file(disable_flag)


    def wpl_send_output_to_log_file(self, output, logFile):
        return self.device.send_output_to_log_file(output, logFile)


    ### misc. wrapper API ###
    def wpl_raiseException(self, msg):
        raise RuntimeError(msg)


    def wpl_displayDiagOSversion(self):
        log.debug("Entering DiagLib class procedure: displayDiagOsversion")
        return self.device.displayDiagOSVersion()


    def set_verbose_level(self, verb_level):
        cmd = ('export VERB_LEVEL=' + str(verb_level))
        return self.wpl_execute(cmd)


    def wpl_get_pc_scp_username(self):
        return self.device.pc_scp_username


    def wpl_get_pc_scp_password(self):
        return self.device.pc_scp_password


    def wpl_get_pc_scp_ip(self):
        return self.device.pc_scp_ip


    def wpl_get_pc_scp_ipv6(self):
        return self.device.pc_scp_ipv6


    def wpl_get_pc_scp_static_ipv6(self):
        return self.device.pc_scp_static_ip


    def wpl_get_jenkins_scp_username(self):
        return self.device.jenkins_scp_username


    def wpl_get_jenkins_scp_password(self):
        return self.device.jenkins_scp_password


    def wpl_get_jenkins_scp_ip(self):
        return self.device.jenkins_scp_ip


    def wpl_get_jenkins_scp_ipv6(self):
        return self.device.jenkins_scp_ipv6


    def wpl_get_jenkins_scp_static_ipv6(self):
        return self.device.jenkins_scp_static_ip


    def wpl_get_bmc_username(self):
        return self.device.bmcUserName


    def wpl_get_bmc_password(self):
        return self.device.bmcPassword


    def wpl_sdk_switch_to_bmc(self):
        return self.device.trySwitchToBmc()


    def wpl_bmc_switch_to_sdk(self):
        return self.device.trySwitchToCpu()




def run_openbmc_utility_test(device,toolName, optionStr):
    device=Device.getDeviceObject(device)
    #CommonLib.switch_to_openbmc()

    cmd =   toolName + ' ' + optionStr
    output = device.execute(cmd, 'openbmc', 10)
    log.info('output=[%s]' %output)
    log.info("Checking \'%s\' output..." %(toolName))
    for line in output.splitlines():
        if re.search('failed', line, re.IGNORECASE):
            log.fail('FW Util test failed')
            raiseException('%s Command failed' %toolName)
    log.success('Checked \'%s\' output OK.' %(toolName))
    CommonLib.switch_to_centos()

def check_unidiag_system_versions(device):
    deviceObj=Device.getDeviceObject(device)
    #diag_system_version_pattern = get_diag_system_versiopattern_listn_pattern(device)

    c1=run_command('unidiag',prompt='>>>')
    #try:
    #  CommonKeywords.should_match_ordered_regexp_list(c1,diag_system_version_pattern)
    #except:
    #  raise RuntimeError("Unidiag actual and expected system versions mismatched" )
    #time.sleep(5)
    #log.success("Unidiag System versions are verifed successfully with latest versions.")



@logThis
def exit_unidiag_interface(device):
   device= Device.getDeviceObject(device)
   for i in range(5):
       device.sendCmd('q')
       try:
           device.read_until_regexp('exit', timeout=5)
           break
       except Exception:
           continue
   device.sendCmd('\r')
   log.success("Exited from Unidiag interface successfully.")


@logThis
def check_system_pcie_scan(device):
   device=Device.getDeviceObject(device)
   check_stress_test(device,'j','PCIe Scan Stress',pcie_pattern,param='loop',param_value='1')


@logThis
def check_stress_test(device,option_key,option_name,pattern_list,param=None,param_value=None):
    #deviceObj=Device.getDeviceObject(device)
    flag="1"
    if (param is None) and (param_value is None):
       param=""
       param_value=""
       flag="0"

    if "minipack3" in devicename.lower():
        log.info("Entering into the stress menu with 'g' key")
        deviceObj.sendCmd('g')      ###Getting into the stress menu test
        time.sleep(3)
        device.sendCmd(option_key)
        time.sleep(5)
        c4=device.read_until_regexp("press any key to continue",timeout=10)
        deviceObj.sendCmd('\n')
        log.success('This feature is currently TBD')
        return

    else:
        log.info("Entering into the stress menu with 'h' key")
        deviceObj.sendCmd('h')      ###Getting into the stress menu test
    time.sleep(3)
    #deviceObj.sendCmd(option_key)
    time.sleep(2)
    log.info("Pressing option '%s' to move in '%s' submenu " %(option_key, option_name))

    if flag == "1":
        device.sendCmd(option_key)
        time.sleep(2)
        new_timeout=int(param_value)*100
        c1=device.read_until_regexp("Please input the mode you are going to run test", timeout=10)
        deviceObj.sendCmd(param)
        c2=device.read_until_regexp("Please input the number of loops", timeout=10)
        deviceObj.sendCmd(param_value)
        c3=device.read_until_regexp("All tests are finished. Press \[Enter\] to proceed",timeout=new_timeout)
        device.sendCmd('\n')
        time.sleep(2)
        device.sendCmd('\n')
        c4=device.read_until_regexp("press any key to continue",timeout=10)
        deviceObj.sendCmd('\n')
        CommonKeywords.should_match_ordered_regexp_list(c4,pattern_list)
    else:
        device.sendCmd(option_key)
        time.sleep(5)
        c1=device.read_until_regexp('Do you want to start',timeout=200)
        device.sendCmd('y \r')
        c4=device.read_until_regexp("press any key to continue",timeout=10)
        deviceObj.sendCmd('\n')



@logThis
def minipack3_check_system_i2c_scan(device):
   device=Device.getDeviceObject(device)
   log.info("Pressing option h ")
   deviceObj.sendCmd('h')
   time.sleep(5)

   log.info("Pressing option d ")
   deviceObj.sendCmd('d')
   time.sleep(5)



@logThis
def minipack3_check_system_cpu_stress(device):
    deviceObj=Device.getDeviceObject(device)
    c1=run_command('unidiag',prompt='>>>')
    log.info("Pressing option g ")
    deviceObj.sendCmd('g')
    time.sleep(5)

    log.info("Pressing option b ")
    deviceObj.sendCmd('b')
    time.sleep(5)

    c4=deviceObj.read_until_regexp("press any key to continue",timeout=10)
    deviceObj.sendCmd('\n')

    try:
      CommonKeywords.should_match_ordered_regexp_list(c4,cpu_pattern)
    except:
      raise RuntimeError("CPU Test Failed" )
    time.sleep(5)
    log.success("CPU test passed!")



##################################################################################################################
def check_sdk_load_and_initialization(device, port_group_cmd):
    """
    Checks the SDK load and initialization for a given device and port group.

    Args:
        device (str): The device name.
        port_group_cmd (str): The port group command.

    Raises:
        RuntimeError: If the 'load and initialization test' fails.

    Returns:
        None
    """

    flag= False
    port_group=port_group_cmd.split()[-1]
    if "minerva_j3" in devicename.lower():
        port_group_cmd=port_group_cmd+" "+port_enable_tag
    load_into_bcm_prompt(device, port_group_cmd)
    device= Device.getDeviceObject(device)
    device.sendCmd('\n')
    time.sleep(5)
    if "minipack3" in devicename.lower() or "minerva" in devicename.lower():
        CommonLib.run_command(port_enable_cmd,deviceObj=device, prompt=BCM_prompt)
        c1=CommonLib.run_command(portdump_status_cmd,deviceObj=device, prompt=BCM_prompt)
        if not check_port_status_output(c1, "passed"):
            flag=True
            log.fail("Port status check failed")

    device.sendCmd(exit_BCM_Prompt)
    if flag:
        raise RuntimeError("'load and initialization test' failed")
    log.success("'load and initialization test' passed successfully for "+port_group +" port group")


def load_into_bcm_prompt(device, port_group_cmd):
    """
    Loads into the BCM.0> prompt with given port group.

    Args:
        device (str): The device to load into the BCM.0> prompt.
        port_group_cmd (str): The port group command to execute.

    Returns:
        None
    """
    device= Device.getDeviceObject(device)
    devicename = os.environ.get("deviceName", "")
    log.info(devicename)
    CommonLib.run_command(port_group_cmd ,deviceObj=device, prompt=BCM_prompt,timeout=30)
    log.success('successfully loaded into BCM.0> Prompt')


def change_to_centos(device):
    """
    Change the device to CentOS operating system.

    Args:
        device (str): The name of the device.

    Returns:
        None
    """
    device= Device.getDeviceObject(device)
    time.sleep(1)
    device.sendMsg("\n")
    device.sendCmd('cd')
    device.read_until_regexp(device.promptDiagOS, timeout=10)

def change_dir_to_sdk_path():
    log.debug("Entering procedure change_dir_to_sdk_path.\n")

    var_path = SDK_PATH
    var_mode = centos_mode
    return CommonLib.change_dir(var_path, var_mode)


def change_dir_to_default():
    log.debug("Entering procedure change_dir_to_default.\n")

    return CommonLib.change_dir()

def check_l2_cpu_traffic(device, port_group_cmd):
    """
    Function to check L2 CPU traffic on a device.

    Args:
        device (str): The device name.
        port_group_cmd (str): The port group command.

    Raises:
        RuntimeError: If the L2 CPU Traffic test fails.

    Returns:
        None
    """

    flag= False
    if "minipack3" in devicename.lower()  or  "minerva" in devicename.lower():
        load_into_bcm_prompt(device,port_group_cmd)
        device= Device.getDeviceObject(device)
        time.sleep(5)
        device.sendCmd('\n')

        c1=CommonLib.run_command(portdump_status_cmd,deviceObj=device,prompt=BCM_prompt)
        if not check_port_status_output(c1, "passed"):
            flag=True
            log.fail("Port status check failed")
        else:
            log.info("Port status check passed")


        time.sleep(5)
        device.sendCmd(clear_c_command)
        time.sleep(10)

        c1_1 = CommonLib.run_command(show_c_cmd,deviceObj=device,prompt=BCM_prompt)
        if not check_show_c_output(c1_1, False):
            flag=True
            log.fail("show c output is incorrect")

        time.sleep(10)
        log.info(str(datetime.now()))


        if "minipack3" in devicename.lower():
            device.sendCmd(traffic_test_cmd+ ' 300')
        else:
            if port_group_cmd=='./auto_load_user.sh':
                device.sendCmd(traffic_test_cmd+'300s')
            else:
                device.sendCmd(traffic_test_cmd+'128')
        c2=device.read_until_regexp(traffic_test_end_regex, timeout=500)
        log.info(str(datetime.now()))
        time.sleep(10)


        if "minipack3" in devicename.lower():
            c2=CommonLib.run_command(portdump_counters_cmd,deviceObj=device,prompt=BCM_prompt)

        if not check_traffic_test_output(c2):
            flag=True
            log.fail("CPU L2 Traffic test failed")


        if port_group_cmd!='./auto_load_user.sh' and "minerva_th5" in devicename.lower():
            c3 = CommonLib.run_command(show_c_cmd,deviceObj=device,prompt=BCM_prompt)
            if not check_show_c_output(c3, True):
                flag=True
                log.fail("show c output is incorrect")


    if "minerva_j3" in devicename.lower():
        device= Device.getDeviceObject(device)
        c1=CommonLib.run_command(port_group_cmd+L2_cpu_traffic_cmd+" "+port_enable_tag,deviceObj=device,prompt=BCM_prompt, timeout=1500)
        if not ((L2_cpu_traffic_passed_pattern in c1) and (check_CPU_L2_traffic_test_output(c1))):
            flag=True
            log.fail("Counters Consistency Check Failed (l2_cpu_traffic test failed)")

        else:
            log.info('Counters Consistency Check passed (l2_cpu_traffic passed successfully)')

    if flag:
        raise RuntimeError("'L2 CPU Traffic test' failed")
    log.success("'L2 CPU Traffic test' passed successfully for "+port_group_cmd.split()[-1] +" port group")


def change_to_centos_from_BCM_Prompt(device):
    """
    Changes the device to CentOS from BCM Prompt.

    Args:
        device (str): The device name.

    Returns:
        None
    """
    device= Device.getDeviceObject(device)
    time.sleep(3)
    device.sendCmd(exit_BCM_Prompt)
    time.sleep(1)
    device.sendCmd("\x03")
    time.sleep(1)
    device.sendMsg("\n")
    device.sendCmd('cd')
    device.read_until_regexp(device.promptDiagOS, timeout=10)


def check_port_status_output(output, result):
    """
    Checks the output of port status and returns True if all output is correct, False otherwise.

    Args:
        output (str): The output of the portump status all command.

    Returns:
        bool: True if all output is correct, False otherwise.
    """
    output_lst = output.splitlines()
    portdump_pattern_regex=portdump_pass_pattern_regex
    if result=='failed':
        portdump_pattern_regex=portdump_failed_pattern_regex

    for item in output_lst:
        if re.search(portdump_pass_pattern[0], item):
            try:
                CommonKeywords.should_match_a_regexp(item,portdump_pattern_regex)
            except:
                log.fail(item)
                return False
    return True


@logThis
def check_system_i2c_scan(device):
   device=Device.getDeviceObject(device)
   check_stress_test(device,'g','I2c Scan Stress',i2c_pattern,param='loop',param_value='1')


@logThis
def minipack3_run_tpm_test(device):
    deviceObj=Device.getDeviceObject(device)
    c1=run_command('unidiag',prompt='>>>')
    log.info("Pressing option c ")
    deviceObj.sendCmd('c')
    time.sleep(5)

    log.info("Pressing option g ")
    deviceObj.sendCmd('g')
    time.sleep(5)

    log.info("Pressing option g ")
    deviceObj.sendCmd('g')
    time.sleep(5)

    log.info("Pressing option b ")
    deviceObj.sendCmd('b')
    time.sleep(5)


    c4=deviceObj.read_until_regexp("press any key to continue",timeout=10)
    deviceObj.sendCmd('\n')

    try:
      CommonKeywords.should_match_ordered_regexp_list(c4,tpm_vendor)
    except:
      raise RuntimeError("Actual and expected vendor version mismatchedi" )
    time.sleep(5)
    log.success("Actual and expected vendor version is verified successfully.")

def check_show_c_output(output, present):
    if not present:
        if len(output.splitlines())==2:
            log.info(output)
            log.fail("There are some counters present after clearing")
            return False
    output_lst= output.splitlines()
    for item in output_lst:
        counters= re.search('\S+\s+:\s+(\S+)\s+\+(\S+)', item)
        if counters:
            if counters.group(1)!=counters.group(2):
                log.fail(item)
                return False
    log.info("show c output is correct")
    return True

def check_traffic_test_output(output):
    """
    Checks the output of a traffic test and verifies if it matches the expected pattern.

    Args:
        output (str): The output of the traffictest all.

    Returns:
        bool: True if the output matches the expected pattern, False otherwise.
    """
    output_lst = output.splitlines()
    for item in output_lst:
        if re.search(portdump_pass_pattern[0], item):
            try:
                CommonKeywords.should_match_a_regexp(item,portdump_pass_pattern_regex)

                tx_rx= re.search('tx=(\d+),\s+rx=(\d+)', item)
                if tx_rx:
                    if tx_rx.group(1)!=tx_rx.group(2):
                        log.fail("tx rx not equal for "+ item)
                        return False
                log.info("tx rx equal for "+item)

            except:
                log.fail(item)
                return False
    log.info('traffic test output is correct')
    return True


def check_port_status(device, port_group_cmd, port_disable_command, port_enable_command):
    """
    Check the status of a port on a device.

    Args:
        device (str): The device name.
        port_group_cmd (str): The command to load the port group.
        port_disable_command (str): The command to disable the port.
        port_enable_command (str): The command to enable the port.

    Raises:
        RuntimeError: If the port status check fails.

    Returns:
        None
    """


    flag= False
    port_group = port_group_cmd.split()[-1]
    if "minerva_j3" in devicename.lower():
        port_group_cmd= port_group_cmd+' '+port_enable_tag
    load_into_bcm_prompt(device,port_group_cmd)
    device= Device.getDeviceObject(device)

    time.sleep(15)
    c1=CommonLib.run_command(portdump_status_cmd,deviceObj=device,prompt=BCM_prompt)
    if not verify_port_status(c1,port_group_cmd,port_enable_status):
        flag=True


    CommonLib.run_command(port_disable_command,deviceObj=device,prompt=BCM_prompt)
    time.sleep(15)

    c2=CommonLib.run_command(portdump_status_cmd,deviceObj=device,prompt=BCM_prompt)
    if not verify_port_status(c2,port_group_cmd,port_disable_status):
        flag=True

    CommonLib.run_command(port_enable_command,deviceObj=device,prompt=BCM_prompt)
    time.sleep(15)

    c3=CommonLib.run_command(portdump_status_cmd,deviceObj=device,prompt=BCM_prompt)
    if not verify_port_status(c3,port_group_cmd,port_enable_status):
        flag=True

    if flag:
        raise RuntimeError("'Port_Status_Test' failed")
    log.success("'Port_Status_Test' passed successfully for "+port_group +" port group")




def verify_port_status(output, port_group_cmd, result):
    flag= False
    if "minerva_j3" in devicename.lower():
        if not check_dump_ports_status(output, result):
            flag=True
            log.fail("Port status check failed")
            log.fail("sdk.dapi.dump_ports() is showing 'different result as Expected' as overall status")

    if "minipack3" in devicename.lower() or "minerva_th5" in devicename.lower():
        if not check_port_details_output(output,port_group_cmd,result):
            flag=True
            log.fail("Port status check failed")
            log.fail("Portdump status all is showing 'different result as Expected' as overall status")
    if flag:
      return False
    return True

def check_port_details_output(output,port_group_cmd,result):
    """
    Check the port details output against the port group command and result.

    Args:
        output (str): The output string containing port details.
        port_group_cmd (str): The port group command.
        result (str): The result of the check (passed/failed).

    Returns:
        bool: True if the output matches the result, False otherwise.
    """



    port_speed_type=[]
    port_count_list=[]
    port_grp= port_group_cmd.split()[-1]
    for port_grp_item in port_grp.split('_'):
        port_count_list.append(int(port_grp_item.split('x')[0]))
        port_speed_type.append('('+port_grp_item.split('x')[1]+'G'+')')

    port_speed_regex= '|'.join(port_speed_type)
    port_details_pattern=[]

    if result=="passed":
        port_detail_passed_pattern.insert(2,port_speed_regex)
        port_details_pattern = '([\s+\S+]+)'.join(port_detail_passed_pattern)
        log.info(port_details_pattern)
        del port_detail_passed_pattern[2]
    else:
        port_details_pattern = '([\s+\S+]+)'.join(port_detail_failed_pattern)
        log.info(port_details_pattern)


    output_lst = output.splitlines()
    port_speed_dict={}
    for item in output_lst:
        if re.search(port_detail_passed_pattern[0], item):
            try:
                CommonKeywords.should_match_a_regexp(item,port_details_pattern)
                present = re.search(port_details_pattern, item)
                port_speed_dict[present.group(5)]=port_speed_dict.get(present.group(5), 0)+1
            except:
                log.fail(item)
                return False
    for i in port_count_list:
        log.info(str(i))
    if result=="passed":
        for port,p_count in port_speed_dict.items():
            if not (p_count in port_count_list):
                log.fail("port count is not matching")
                return False
    else:
        port_sum=0
        for p_count in port_speed_dict.values():
            port_sum=port_sum+p_count
        if port_sum!=sum(port_count_list):
            log.fail("port count is not matching ")
            return False
    return True


@logThis
def minipack3_run_oob_test(device):
    deviceObj=Device.getDeviceObject(device)
    c1=run_command('unidiag',prompt='>>>')
    log.info("Pressing option b ")
    deviceObj.sendCmd('b')
    time.sleep(5)

    log.info("Pressing option l ")
    deviceObj.sendCmd('l')
    time.sleep(5)

    c4=deviceObj.read_until_regexp("press any key to continue",timeout=10)
    deviceObj.sendCmd('\n')

    try:
      CommonKeywords.should_match_ordered_regexp_list(c4,oob_test)
    except:
      raise RuntimeError("OOB Test FAILED" )
    time.sleep(5)
    log.success("OOB Test PASSED")



@logThis
def run_tpm_test(device):
    deviceObj=Device.getDeviceObject(device)
    c1=run_command('unidiag',prompt='>>>')
    time.sleep(2)
    log.info("Pressing option c ")
    deviceObj.sendCmd('c')
    time.sleep(5)

    log.info("Pressing option d ")
    deviceObj.sendCmd('d')
    time.sleep(5)

    log.info("Pressing option f ")
    deviceObj.sendCmd('f')
    time.sleep(5)


    log.info("Pressing option b ")
    deviceObj.sendCmd('b')
    time.sleep(5)

    c4=deviceObj.read_until_regexp("press any key to continue",timeout=10)
    deviceObj.sendCmd('\n')

    try:
      CommonKeywords.should_match_ordered_regexp_list(c4,minerva_tpm)
    except:
      raise RuntimeError("Actual and expected vendor version mismatchedi" )
    time.sleep(5)
    log.success("Actual and expected vendor version is verified successfully.")

