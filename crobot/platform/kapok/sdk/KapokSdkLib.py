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
import os
import sys
import Logger as log
import CRobot
import Const
import KapokConst
import re
from Decorator import *
import time
from functools import partial
import YamlParse
import KapokCommonLib

workDir = CRobot.getWorkDir()
sys.path.append(os.path.join(workDir, 'common', 'commonlib'))
sys.path.append(os.path.join(workDir, 'platform/kapok'))

import CommonLib
try:
    from Device import Device
    import DeviceMgr
except Exception as err:
    log.cprint(str(err))
device = DeviceMgr.getDevice()
if "briggs" in device.name:
    from BriggsSdkVariable import *
else:
    from KapokSdkVariable import *
run_command = partial(CommonLib.run_command, deviceObj=device, prompt=device.promptDiagOS)
def OnieConnect():
    log.debug("Entering OnieTestCase procedure: OnieConnect")
    device.loginOnie()
    return

def OnieDisconnect():
    global libObj
    log.debug("Entering OnieTestCase procedure: OnieDisconnect")
    device.disconnect()
    return

def add_flush_and_delay(timeout=3):
    #add more delay to make sure the cat process completed, to avoid the output message messup
    time.sleep(timeout)
    device.flush()
    time.sleep(1)

def check_output(output, patterns=[""], timeout=60, line_mode=True, is_negative_test=False, remark=""):
    device.log_debug('Entering procedure check_output ')
    passCount = 0
    patternNum = len(patterns)
    device.log_debug('output = ***%s***' % output)
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
    device.log_debug('passCount = %s' %passCount)
    device.log_debug('patternNum = %s' %patternNum)
    ret_code = 0
    if remark:
        description = remark
    else:
        description = "All patterns "
    if passCount == patternNum:
        ret_code = 1
        device.log_success('%s is PASSED\n' %description)
    else:
        device.log_fail('Exiting check_output with result FAIL, {} fail with pattern: {}'.format(remark, mismatch_pattern))
    return ret_code

def check_load_user(cmd, pattern_dict={}, port_sum_pattern={}, port_total=None, prompt_str=None, timeout=3600):
    device.log_debug('Entering procedure check_load_user with args : %s' %(str(locals())))
    cmd_path = "cd {}".format(SDK_PATH)
    device.sendCmd(cmd_path)
    finish_prompt = "{}".format(prompt_str)
    output=device.sendCmdRegexp(cmd,"SDK process is Running|Innovium Switch PCIe Driver opened successfully",timeout=15)
    if re.search("SDK process is Running", output):
        device.sendCmd("./cls_shell exit","closed successfully",timeout=15)
        output = device.sendCmd(cmd,"Innovium Switch PCIe Driver opened successfully",timeout=15)
    CommonLib.execute_check_dict('DUT', cmd="", mode=None, patterns_dict=pattern_dict, timeout=50, line_mode=True, check_output=output)
    # if port_sum_pattern:
    #     execute_check_num(cmd="", mode=None, patterns_dict=port_sum_pattern, path=None, expected_num=port_total,
    #                                timeout=50, check_output=output, remark="")
    output=device.sendCmdRegexp('\n',finish_prompt,timeout=60)
    if re.search(prompt_str, output):
        device.log_info('%s is PASSED\n' %cmd)
    else:
        device.raiseException("Didn't get prompt %s \n" %prompt_str)

def exit_console_mode(previous_prompt=None, dest_prompt=None, exit_cmd="exit"):
    device.log_debug('Entering procedure exit_console_mode with args : %s' %(str(locals())))
    device.sendMsg("\n")
    output = device.read_until_regexp(previous_prompt, timeout=10)
    device.log_info("readMSG:***{}***".format(output))
    match = re.search(previous_prompt, output, re.M)
    if match:
        device.sendMsg("{}\n\n".format(exit_cmd))
        output_ext = device.read_until_regexp(dest_prompt, timeout=10)
        if re.search(dest_prompt, output_ext):
            device.log_info('Exit to %s is PASSED\n'%dest_prompt )
        else:
            device.raiseException("exit to %s promptstr failed . \n" %dest_prompt)
    else:
        device.sendMsg("\n")
        output_dst = device.readUntil(dest_prompt, timeout=2)
        match_dest = re.search(dest_prompt, output_dst, re.M)
        if match_dest:
            device.log_info('current prompt is already %s\n'%dest_prompt )
        device.log_info("Didn't get prompt %s, exit won't be sent. \n" %previous_prompt)

def get_port_infos_regexp(portmode,link=False,FEC=False):
    if not FEC:
        if not link:
            if '1-32:COPPER_1X400G' in str.upper(portmode):
                var_expectedDict = PAM4_400G_32_pattern
            elif '1-32:COPPER_4X100G' in str.upper(portmode):
                var_expectedDict = PAM4_100G_128_pattern
            elif '1-32:COPPER_1X100G' in str.upper(portmode):
                var_expectedDict = NRZ_100G_32_pattern
            elif '1-32:COPPER_1X40G' in str.upper(portmode):
                var_expectedDict = NRZ_40G_32_pattern
            elif '1-32:COPPER_4X25G' in str.upper(portmode):
                var_expectedDict = NRZ_25G_128_pattern
            elif '1-32:COPPER_4X10G' in str.upper(portmode):
                var_expectedDict = NRZ_10G_128_pattern
            elif '1-32:COPPER_2X100G' in str.upper(portmode):
                var_expectedDict = NRZ_100G_64_pattern
            elif '1-32:COPPER_1X200G' in str.upper(portmode):
                var_expectedDict = NRZ_200G_32_pattern
            elif '23-32:COPPER_4X25' in str.upper(portmode):
                var_expectedDict = copper_1_8_9_22_23_32_pattern
            elif '25-32:1X100G' in str.upper(portmode):
                var_expectedDict = copper_1_20_21_24_25_32_pattern
            elif '25-32:COPPER_4X100G' in str.upper(portmode):
                var_expectedDict = copper_1_20_21_24_25_32_4x100_pattern
            else:
                device.raiseException('unrecognizable port mode [%s], return. \n ' % (portmode))
                return
        else:
            if '1-32:COPPER_1X400G' in str.upper(portmode):
                var_expectedDict = PAM4_400G_32_link_pattern
            elif '1-32:COPPER_4X100G' in str.upper(portmode):
                var_expectedDict = PAM4_100G_128_link_pattern
            elif '1-32:COPPER_1X100G' in str.upper(portmode):
                var_expectedDict = NRZ_100G_32_link_pattern
            elif '1-32:COPPER_1X40G' in str.upper(portmode):
                var_expectedDict = NRZ_40G_32_link_pattern
            elif '1-32:COPPER_4X25G' in str.upper(portmode):
                var_expectedDict = NRZ_25G_128_link_pattern
            elif '1-32:COPPER_4X10G' in str.upper(portmode):
                var_expectedDict = NRZ_10G_128_link_pattern
            elif '1-32:COPPER_2X100G' in str.upper(portmode):
                var_expectedDict = NRZ_100G_64_link_pattern
            elif '23-32:COPPER_4X25' in str.upper(portmode):
                var_expectedDict = copper_1_8_9_22_23_32_link_pattern
            elif '25-32:1X100G' in str.upper(portmode):
                var_expectedDict = copper_1_20_21_24_25_32_link_pattern
            elif '25-32:COPPER_4X100G' in str.upper(portmode):
                var_expectedDict = copper_1_20_21_24_25_32_4x100_link_pattern
            else:
                device.raiseException('unrecognizable port mode [%s], return. \n ' % (portmode))
                return
    else:
        if '32X400' in str.upper(portmode):
            var_expectedDict = integrator_400G_32_pattern
        elif '32X200' in str.upper(portmode):
            var_expectedDict = integrator_200G_32_pattern
        elif '32X100' in str.upper(portmode):
            var_expectedDict = integrator_100G_32_pattern
        elif '32X40' in str.upper(portmode):
            var_expectedDict = integrator_40G_32_pattern
        elif '128X100' in str.upper(portmode):
            var_expectedDict = integrator_100G_128_pattern
        elif '128X25' in str.upper(portmode):
            var_expectedDict = integrator_25G_128_pattern
        elif '128X10' in str.upper(portmode):
            var_expectedDict = integrator_10G_128_pattern
        elif '64X100-1' in str.upper(portmode):
            var_expectedDict = integrator_100G_64_1_pattern
            return var_expectedDict
        elif '64X100' in str.upper(portmode):
            var_expectedDict = integrator_100G_64_pattern
        else:
            device.raiseException('unrecognizable port mode [%s], return. \n ' % (portmode))
            return
    return var_expectedDict

def get_list_regexp_rate(port_start,port_end,rate):
    return_pattern = []
    for i in range(int(port_start), int(port_end)+1):
        regexp = "\|.* "+str(i)+" .*:.*:.*:.*"+str(rate)+".*:.*:.*:.*:.*"+str(rate)+".*:.*\|"
        return_pattern.append(regexp)
    return return_pattern

def source_cmd_function(portmode,portnum):
    device.log_debug("Entering procedure source_cmd.\n")
    enable_cmd = "port enable 1-" + str(portnum) + "\r\n"
    disable_cmd = "port disable 1-" + str(portnum) + "\r\n"
    if "PAM4_400G_32" in str.upper(portmode) and "fenghuang" in device.name:
        device.sendMsg(disable_cmd)
        device.sendMsg(PAM4_400G_32_source_preemphasis)
        output = device.read_until_regexp(PAM4_400G_32_source_preemphasis_regexp, timeout=60)
        ret_code = check_output(output, patterns=PAM4_400G_32_source_preemphasis_pattern)
        if ret_code == 0:
            device.raiseException("failed cmd is {}".format(PAM4_400G_32_source_preemphasis))
        device.sendMsg(PAM4_400G_32_source_rx_gs)
        output = device.read_until_regexp(PAM4_400G_32_source_rx_gs_regexp, timeout=60)
        ret_code1 = check_output(output, patterns=PAM4_400G_32_source_rx_gs_pattern)
        if ret_code1 == 0:
            device.raiseException("failed cmd is {}".format(PAM4_400G_32_source_rx_gs))
        device.sendMsg(enable_cmd)
        device.sendMsg(shell_sleep_10)
    else:
        device.sendMsg(source_cmd)
        output = device.read_until_regexp(source_cmd_regexp, timeout=60)
        ret_code2 = check_output(output, patterns=source_cmd_pattern)
        if ret_code2 == 0:
            device.raiseException("failed cmd is {}".format(source_cmd))

def source_config(portmode,portnum,FEC=False):
    device.log_debug("Entering procedure source_config.\n")
    diagtest_cmd = "diagtest snake config -p 1-" + str(portnum) + " -lb NONE -v"
    output = device.sendCmdRegexp(diagtest_cmd, "NONE.*1",timeout=60)
    ret_code = check_output(output, patterns=['NONE.*1'])
    if ret_code == 0:
        device.raiseException("failed cmd is {}".format(diagtest_cmd))
    device.sendMsg(shell_sleep_10)
    add_flush_and_delay(timeout=20)
    output=device.sendCmd(show_port_info,port_info_finish_prompt,timeout=60)

                                                
def multiple_source_config(portnum1,portnum2):
    device.log_debug("Entering procedure multiple_source_config.\n")
    diagtest_cmd1 = "diagtest snake config -p " + str(portnum1) + " -lb NONE -v -id 1"
    diagtest_cmd2 = "diagtest snake config -p " + str(portnum2) + " -lb NONE -v -id 2"
    output1 = device.sendCmdRegexp(diagtest_cmd1, "NONE.*1",timeout=60)
    output2 = device.sendCmdRegexp(diagtest_cmd2, "NONE.*2", timeout=60)
    ret_code1 = check_output(output1, patterns=['NONE.*1'])
    if ret_code1 == 0:
        device.raiseException("failed cmd is {}".format(diagtest_cmd1))
    ret_code2 = check_output(output2, patterns=['NONE.*2'])
    if ret_code2 == 0:
        device.raiseException("failed cmd is {}".format(diagtest_cmd2))

def multiple_start_traffic():
    device.log_debug("Entering procedure multiple_start_traffic.\n")
    start_traffic_500_cmd_id1 = str(start_traffic_500_cmd) +" -id 1"
    start_traffic_500_cmd_id2 = str(start_traffic_500_cmd) + " -id 2"
    device.sendCmdRegexp(start_traffic_500_cmd_id1,sdkConsole)
    device.sendCmdRegexp(start_traffic_500_cmd_id2, sdkConsole)

def multiple_stop_traffic():
    device.log_debug("Entering procedure multiple_stop_traffic.\n")
    stop_traffic_cmd_id1 = str(stop_traffic_cmd) +" -id 1"
    stop_traffic_cmd_id2 = str(stop_traffic_cmd) +" -id 2"
    device.sendCmdRegexp(stop_traffic_cmd_id1,sdkConsole,timeout=60)
    device.sendCmdRegexp(stop_traffic_cmd_id2, sdkConsole,timeout=60)

def multiple_check_port_rate(cmd,portnum,portrate,portstart):
    device.log_debug("Entering procedure multiple_check_port_rate.\n")
    add_flush_and_delay()
    device.sendMsg(cmd)
    check_rate_regexp = '\|.* '+str(portnum)+' .*:.*:.*:.*:.*:.*:.*:.*:.*\|'
    output = device.read_until_regexp(check_rate_regexp, timeout=60)
    check_rate_patterns = get_list_regexp_rate(portstart,portnum,portrate)
    ret_code = check_output(output, patterns=check_rate_patterns)
    if ret_code == 0:
        device.raiseException("failed cmd is {}".format(check_rate))

def multiple_check_port_counter(portnum):
    device.log_debug("Entering procedure multiple_check_port_counter.\n")
    add_flush_and_delay()
    device.sendMsg(check_counters)
    check_rate_regexp = '\|.* '+str(portnum)+' .*\|.*\|.*\|.*\|.*\|.*\|.*\|.*\|.*\|.*\|.*\|'
    output = device.read_until_regexp(check_rate_regexp, timeout=60)
    Frames_String,Bytes_String = get_frames_and_bytes(1,output)
    Frames_String1,Bytes_String1 = get_frames_and_bytes(21,output)
    check_packages_patterns = get_list_regexp_total_packages(1,20,Frames_String, Bytes_String)
    check_packages_patterns1 = get_list_regexp_total_packages(21,portnum,Frames_String1,Bytes_String1)
    ret_code = check_output(output, patterns=check_packages_patterns)
    if ret_code == 0:
        device.raiseException("failed cmd is {}".format(check_counters))
    ret_code1 = check_output(output, patterns=check_packages_patterns1)
    if ret_code1 == 0:
        device.raiseException("failed cmd is {}".format(check_counters))

def start_traffic(portmode):
    device.log_debug("Entering procedure start_traffic.\n")
    if "PAM4_100G_128" in str.upper(portmode):
        device.sendCmdRegexp(start_traffic_1000_cmd, sdkConsole)
    else:
        device.sendCmdRegexp(start_traffic_500_cmd,sdkConsole)

def check_port_rate(portnum,portrate):
    device.log_debug("Entering procedure check_port_rate.\n")
    add_flush_and_delay()
    device.sendMsg(check_rate)
    check_rate_regexp = '\|.* '+str(portnum)+' .*:.*:.*:.*:.*:.*:.*:.*:.*\|'
    output = device.read_until_regexp(check_rate_regexp, timeout=60)
    check_rate_patterns = get_list_regexp_rate(1,portnum,portrate)
    ret_code = check_output(output, patterns=check_rate_patterns)
    if ret_code == 0:
        device.raiseException("failed cmd is {}".format(check_rate))

def stop_traffic():
    device.log_debug("Entering procedure stop_traffic.\n")
    device.sendCmdRegexp(stop_traffic_cmd,sdkConsole)

def get_frames_and_bytes(numberstart,string):
    regexp_string = '\|.* '+str(numberstart)+' .*\|.*\|.*\|.*\|.*\|.*\|.*\|.*\|.*\|.*\|.*\|'
    x = re.findall(regexp_string, string)
    Frames_return = str(x[0]).split("|")[2].strip()
    Bytes_return = str(x[0]).split("|")[5].strip()
    return Frames_return,Bytes_return

def get_list_regexp_total_packages(portstart,port,frames,bytes):
    return_pattern = []
    for i in range(int(portstart), int(port) + 1):
        regexp = "\|.* "+str(i)+" .*\|.*"+str(frames)+".*\|.*"+str(frames)+".*\|.*0.*\|.*"+str(bytes)+".*\|.*"+str(bytes)+".*\|.*"+str(frames)+".*\|.*"+str(frames)+".*\|.*0.*\|.*"+str(bytes)+".*\|.*"+str(bytes)+".*\|"
        return_pattern.append(regexp)
    return return_pattern

def check_port_counter(portnum):
    device.log_debug("Entering procedure check_port_counter.\n")
    add_flush_and_delay()
    device.sendMsg(check_counters)
    check_rate_regexp = '\|.* '+str(portnum)+' .*\|.*\|.*\|.*\|.*\|.*\|.*\|.*\|.*\|.*\|.*\|'
    output = device.read_until_regexp(check_rate_regexp, timeout=60)
    Frames_String,Bytes_String = get_frames_and_bytes(1,output)
    check_packages_patterns = get_list_regexp_total_packages(1,portnum,Frames_String,Bytes_String)
    ret_code = check_output(output, patterns=check_packages_patterns)
    if ret_code == 0:
        device.raiseException("failed cmd is {}".format(check_counters))

def remove_config():
    device.log_debug("Entering procedure remove_config.\n")
    device.sendMsg(remove_config_cmd)
    output = device.read_until_regexp(remove_config_regexp, timeout=60)
    ret_code = check_output(output, patterns=remove_config_pattern)
    if ret_code == 0:
        device.raiseException("failed cmd is {}".format(remove_config_cmd))

def clear_counters():
    device.log_debug("Entering procedure clear_counters.\n")
    device.sendMsg(clear_devport)
    device.read_until_regexp(clear_devport, timeout=60)
    add_flush_and_delay()
    device.sendMsg(clear_hardware)
    device.read_until_regexp(clear_hardware, timeout=60)
    add_flush_and_delay()

def check_port_status(portmode,portnum):
    device.log_debug("Entering procedure check_port_status.\n")
    if str(portnum) == "all":
        enable_cmd = "port enable all\r\n"
    else:
        enable_cmd = "port enable 1-" + str(portnum) + "\r\n"
    device.sendMsg(enable_cmd)
    time.sleep(300)
    # device.sendMsg(shell_sleep_30)
    output=device.sendCmd(show_port_info,port_info_finish_prompt,timeout=60)
    port_infos_pattern = get_port_infos_regexp(portmode,link=True)
    ret_code = check_output(output, patterns=port_infos_pattern)
    if ret_code == 0:
        device.raiseException("failed cmd is {}".format(show_port_info))

def check_fec_port_status(portmode,portnum):
    device.log_debug("Entering procedure check_fec_port_status.\n")
    enable_cmd="port enable 1-"+str(portnum)+"\r\n"
    device.sendMsg(enable_cmd)
    device.sendMsg(shell_sleep_10)
    device.sendCmdRegexp(show_port_info,sdkConsole,timeout=150)
    output = device.read_until_regexp(port_info_finish_prompt, timeout=60)
    port_infos_pattern = get_port_infos_regexp(portmode,FEC=True)
    ret_code = check_output(output, patterns=port_infos_pattern)
    if ret_code == 0:
        device.raiseException("failed cmd is {}".format(show_port_info))

def check_port_infomation(portmode):
    device.log_debug("Entering procedure check_port_infomation.\n")
    for i in range(0,2):
        output=run_command(show_port_info,prompt=port_info_finish_prompt,timeout=60)
    port_infos_pattern = get_port_infos_regexp(portmode)
    ret_code = check_output(output, patterns=port_infos_pattern)
    if ret_code == 0:
        device.raiseException("failed cmd is {}".format(show_port_info))
    add_flush_and_delay()

def check_sdk_version():
    device.log_debug("Entering procedure check_sdk_version.\n")
    device.sendMsg(CatReadMe)
    output = device.read_until_regexp(CatReadMe_regexp, timeout=10)
    ret_code = check_output(output, patterns=CatReadMe_pattern)
    device.sendMsg(ifcs)
    output = device.read_until_regexp(ifcs_regexp, timeout=10)
    ret_code1 = check_output(output, patterns=ifcs_pattern)
    if ret_code == 0:
        device.raiseException("{} failed.".format(CatReadMe))
    if ret_code1 == 0:
        device.raiseException("{} failed.".format(ifcs))

@logThis
def briggs_credo_init():
    cmd_path = "cd {}".format(SDK_PATH)
    device.sendCmd(cmd_path)
    device.sendCmdRegexp(credo_init, credo_init_pattern,timeout=200)

@logThis
def get_briggs_port_cmd_regexp(portmode):
    if 'PAM4_400G_32' in str.upper(portmode):
        var_expectedDict_sixteen = PAM4_400G_32_sixteen_cmd
        var_expectedDict = PAM4_400G_32_cmd
    elif 'PAM4_100G_128' in str.upper(portmode):
        var_expectedDict_sixteen = PAM4_100G_128_sixteen_cmd
        var_expectedDict = PAM4_100G_128_cmd
    elif 'NRZ_100G_32' in str.upper(portmode):
        var_expectedDict_sixteen = NRZ_100G_32_sixteen_cmd
        var_expectedDict = NRZ_100G_32_cmd
    elif 'NRZ_40G_32' in str.upper(portmode):
        var_expectedDict_sixteen = NRZ_40G_32_sixteen_cmd
        var_expectedDict = NRZ_40G_32_cmd
    elif 'NRZ_25G_128' in str.upper(portmode):
        var_expectedDict_sixteen = NRZ_25G_128_sixteen_cmd
        var_expectedDict = NRZ_25G_128_cmd
    elif 'NRZ_10G_128' in str.upper(portmode):
        var_expectedDict_sixteen = NRZ_10G_128_sixteen_cmd
        var_expectedDict = NRZ_10G_128_cmd
    else:
        device.raiseException('unrecognizable port mode [%s], return. \n ' % (portmode))
        return
    return var_expectedDict_sixteen,var_expectedDict

def load_user_mode(cmd=None, patterns=init_pass_pattern, port_sum_pattern=init_port_pattern,
                     port_total=32, is_negative_test=False, timeout=3600):
    device.sendMsg("./cls_shell exit\r\n")
    time.sleep(35)
    device.log_debug("Entering procedure load_user_mode.\n")
    if "briggs" in device.name:
        briggs_credo_init()
        sixteen_port_cmd,load_cmd = get_briggs_port_cmd_regexp(cmd)
        device.sendCmdRegexp(sixteen_port_cmd, sixteen_port_cmd_pattern, timeout=200)
        return check_load_user(load_cmd, pattern_dict=patterns, port_sum_pattern=port_sum_pattern,
                               port_total=port_total, prompt_str=sdkConsole, timeout=timeout)
    else:
        return check_load_user(cmd, pattern_dict=patterns, port_sum_pattern=port_sum_pattern,
                                   port_total=port_total, prompt_str=sdkConsole, timeout=timeout)

def load_daemon_mode(cmd=None, patterns=init_pass_pattern, port_sum_pattern=init_port_pattern,
                     port_total=32, is_negative_test=False, timeout=3600):
    device.log_debug("Entering procedure load_daemon_mode.\n")
    return check_load_user(cmd, pattern_dict=patterns, port_sum_pattern=port_sum_pattern,
                                   port_total=port_total, prompt_str='ONIE', timeout=timeout)

def exit_user_mode(pre_prompt=sdkConsole, dest_prompt='ONIE', exit_cmd="exit"):
    device.log_debug("Entering procedure exit_mode.\n")
    exit_console_mode(previous_prompt=pre_prompt, dest_prompt=dest_prompt, exit_cmd=exit_cmd)

def change_dir_to_sdk_path():
    device.log_debug("Entering procedure change_dir_to_sdk_path.\n")
    device.getPrompt(Const.BOOT_MODE_ONIE)
    var_path = SDK_PATH
    cmd = "cd " + var_path
    output = device.sendCmd(cmd,device.promptOnie)
    ret_code = check_output(output, patterns=fail_pattern, is_negative_test=True)
    if ret_code == 0:
        device.raiseException("{} failed.".format(cmd))

def rescue_mode_change_dir_to_sdk_path():
    device.log_debug("Entering procedure rescue_mode_change_dir_to_sdk_path.\n")
    device.getPrompt(Const.ONIE_RESCUE_MODE)
    var_path = SDK_PATH
    cmd = "cd " + var_path
    output = device.sendCmd(cmd,device.promptOnie)
    ret_code = check_output(output, patterns=fail_pattern, is_negative_test=True)
    if ret_code == 0:
        device.raiseException("{} failed.".format(cmd))

def check_port_BER(cmd,output,port_pattern):
    device.log_debug("Entering procedure check_port_BER.\n")
    fail_port = []
    match_flag = 0
    for line in output.splitlines():
        match = re.search(port_pattern, line)
        if match:
            match_flag = 1
            BER_value = float(match.group(1))
            if BER_value >= port_BER_tolerance:
                fail_port.append(str(line))
    if fail_port:
        device.raiseException("{} failed with ports:{}".format(cmd, fail_port))
    elif match_flag == 0:
        device.raiseException("Command failed with didn't match ports information")
    else:
        device.log_success("{}".format(cmd))

def enable_prbs_tx():
    device.log_debug("Entering procedure enable_prbs_tx.\n")
    device.sendCmdRegexp(prbs_tx_enable_cmd, prbs_finish_pattern,timeout=200)

def enable_prbs_rx_and_check_counter():
    device.log_debug("Entering procedure enable_prbs_rx_and_check_counter.\n")
    output = device.sendCmdRegexp(prbs_rx_enable_cmd, prbs_finish_pattern,timeout=600)
    check_port_BER(prbs_rx_enable_cmd,output,port_pattern=BER_port_pattern)

def check_prbs_ber():
    device.log_debug("Entering procedure check_prbs_ber.\n")
    output = device.sendCmdRegexp(prbs_ber_check_cmd, prbs_finish_pattern, timeout=9000)
    check_port_BER(prbs_ber_check_cmd, output, port_pattern=BER_port_pattern)

def source_dac_cmd_function():
    device.log_debug("Entering procedure source_dac_cmd_function.\n")
    device.sendCmdRegexp(lt_enable_cmd, sdkConsole,timeout=10)
    device.sendCmdRegexp(rx_ctle_set_DAC_cmd, sdkConsole,timeout=10)

def prbs_tx_31_53g():
    device.log_debug("Entering procedure prbs_tx_31_53g.\n")
    device.sendCmdRegexp(prbs_tx_31_53g_cmd, sdkConsole, timeout=60)

def prbs_rx_31_53g_30_1():
    device.log_debug("Entering procedure prbs_rx_31_53g_30_1.\n")
    output = device.sendCmdRegexp(prbs_rx_31_53g_30_1_cmd, prbs_rx_31_53g_30_1_pattern,timeout=600)
    device.log_debug("output"+str(output))
    check_port_BER(prbs_rx_31_53g_30_1_cmd,output,port_pattern=BER_port_pattern)

def sleep_5S():
    device.log_debug("Entering procedure sleep_5S.\n")
    time.sleep(5)

def ber_check():
    device.log_debug("Entering procedure ber_check.\n")
    output = device.sendCmdRegexp(rack_ber_check_cmd, rack_ber_check_pattern, timeout=600)
    check_port_BER(rack_ber_check_cmd,output,port_pattern=BER_port_pattern)

def prbs_tx_31_25g():
    device.log_debug("Entering procedure prbs_tx_31_25g.\n")
    device.sendCmdRegexp(prbs_tx_31_25g_cmd, sdkConsole, timeout=60)

def prbs_rx_31_25g_5(portnum):
    device.log_debug("Entering procedure prbs_rx_31_25g_5.\n")
    if str(portnum) == "32":
        output = device.sendCmdRegexp(prbs_rx_31_25g_5_cmd, prbs_rx_31_25g_5_pattern,timeout=600)
    else:
        output = device.sendCmdRegexp(prbs_rx_31_25g_5_cmd, prbs_rx_31_25g_5_pattern_port128, timeout=600)
    device.log_debug("output"+str(output))
    check_port_BER(prbs_rx_31_25g_5_cmd,output,port_pattern=BER_port_pattern)

def prbs_rx_31_10g_300(portnum):
    device.log_debug("Entering procedure prbs_rx_31_10g_300.\n")
    if str(portnum) == "32":
        output = device.sendCmdRegexp(prbs_rx_31_10g_300_cmd, prbs_rx_31_10g_300_pattern,timeout=3600)
    elif str(portnum) == "64":
        output = device.sendCmdRegexp(prbs_rx_31_10g_300_cmd, prbs_rx_31_10g_300_pattern_port64,timeout=3600)
    device.log_debug("output" + str(output))
    check_port_BER(prbs_rx_31_10g_300_cmd, output, port_pattern=BER_port_pattern)

def prbs_rx_31_25g_2160(portnum):
    device.log_debug("Entering procedure prbs_rx_31_25g_2160.\n")
    if str(portnum) == "32":
        output = device.sendCmdRegexp(prbs_rx_31_25g_2160_cmd, prbs_rx_31_25g_2160_pattern,timeout=3600)
    else:
        output = device.sendCmdRegexp(prbs_rx_31_25g_2160_cmd, prbs_rx_31_25g_2160_pattern_port128, timeout=3600)
    device.log_debug("output"+str(output))
    check_port_BER(prbs_rx_31_25g_2160_cmd,output,port_pattern=BER_port_pattern)

def prbs_tx_31_10g():
    device.log_debug("Entering procedure prbs_tx_31_10g.\n")
    device.sendCmdRegexp(prbs_tx_31_10g_cmd, sdkConsole, timeout=60)

def prbs_rx_31_10g_5(portnum):
    device.log_debug("Entering procedure prbs_rx_31_10g_5.\n")
    if str(portnum) == "32":
        output = device.sendCmdRegexp(prbs_rx_31_10g_5_cmd, prbs_rx_31_10g_5_pattern,timeout=600)
    elif str(portnum) == "64":
        output = device.sendCmdRegexp(prbs_rx_31_10g_5_cmd, prbs_rx_31_10g_5_pattern_port64,timeout=600)
    else:
        output = device.sendCmdRegexp(prbs_rx_31_10g_5_cmd, prbs_rx_31_10g_5_pattern_port128, timeout=600)
    device.log_debug("output"+str(output))
    check_port_BER(prbs_rx_31_10g_5_cmd,output,port_pattern=BER_port_pattern)

def prbs_rx_31_10g_2160(portnum):
    device.log_debug("Entering procedure prbs_rx_31_10g_2160.\n")
    if str(portnum) == "32":
        output = device.sendCmdRegexp(prbs_rx_31_10g_2160_cmd, prbs_rx_31_10g_2160_pattern,timeout=3600)
    elif str(portnum) == "64":
        output = device.sendCmdRegexp(prbs_rx_31_10g_2160_cmd, prbs_rx_31_10g_2160_pattern_port64,timeout=3600)
    else:
        output = device.sendCmdRegexp(prbs_rx_31_10g_2160_cmd, prbs_rx_31_10g_2160_pattern_port128, timeout=3600)
    device.log_debug("output"+str(output))
    check_port_BER(prbs_rx_31_10g_2160_cmd,output,port_pattern=BER_port_pattern)

def sfp_detect_tool_test():
    device.log_debug("Entering procedure sfp_detect_tool_test.\n")
    output = device.sendCmdRegexp(sfp_detect_tool_cmd, sfp_detect_tool_finish_prompt, timeout=3600)
    ret_code = check_output(output, patterns=sfp_detect_tool_pattern)
    if ret_code == 0:
        device.raiseException("failed cmd is {}".format(sfp_detect_tool_cmd))

def knet_l2_show():
    device.log_debug("Entering procedure knet_l2_show.\n")
    output = device.sendCmdRegexp(knet_l2_show_cmd, knet_l2_show_finish_prompt, timeout=180)
    ret_code = check_output(output, patterns=knet_l2_show_pattern)
    if ret_code == 0:
        device.raiseException("failed cmd is {}".format(knet_l2_show_cmd))

def qsfp_test():
    device.log_debug("Entering procedure qsfp_test.\n")
    output = device.sendCmdRegexp(qsfp_cmd, qsfp_finish_prompt, timeout=180)
    ret_code = check_output(output, patterns=qsfp_pattern,line_mode=False)
    if ret_code == 0:
        device.raiseException("failed cmd is {}".format(qsfp_cmd))

def ess_test():
    log.debug("Entering procedure ess_test.\n")
    import KapokCommonLib
    while True:
        if YamlParse.getTestCaseInfo()['stopCase']:
            log.info('User let stop case!!')
            return
        else:
            log.info('Continue run case.')
        KapokCommonLib.powerCycleToDiagOS()
        time.sleep(100)
        device.sendCmd('cd /root/')
        device.sendCmd('chmod 777 ./ess_traffic_test.sh')
        out = device.executeCmd('./ess_traffic_test.sh', timeout=120)
        device.log_debug('output: ' + str(out))
        if 'Traffic test FAIL' in out:
            raise RuntimeError('Traffic test FAIL')

def sleep_time(timevalue):
    device.log_debug("Entering procedure sleep.\n")
    time.sleep(int(timevalue))

@logThis
def fhv2DiagdownloadImagesAndRecoveryDiagOS():
    INSTALLER_MODE_DETECT_PROMPT = 'discover: installer mode detected'
    RECOVERY_DIAG_PATTERN = {"installer mode detected": "installer mode detected"}
    diagos_file_name = CommonLib.get_swinfo_dict("DIAGOS").get("newImage")
    hostImageDir = CommonLib.get_swinfo_dict("DIAGOS").get("hostImageDir")
    diagos_file = ["{}/{}".format(hostImageDir,diagos_file_name)]
    CommonLib.tftp_get_files(Const.DUT, file_list=diagos_file, dst_path="/root", timeout=400)
    install_diagos_cmd = "onie-nos-install {}".format(diagos_file_name)
    output = device.sendCmdRegexp(install_diagos_cmd, INSTALLER_MODE_DETECT_PROMPT, timeout=900)
    CommonLib.execute_check_dict("DUT", "", patterns_dict=RECOVERY_DIAG_PATTERN, timeout=60,
                                check_output=output)

def configStaticIP(interface="eth0", mode=Const.ONIE_RESCUE_MODE):
    log.debug("Entering OnieLib class procedure: configStaticIP")

    deviceName = os.environ.get("deviceName", "")
    log.debug("deviceName: {}".format(deviceName))
    device_ip = CommonLib.Get_Not_Occupied_IP()
    if not device_ip:
        raise Exception("No available device_ip is found")
    else:
        log.info("Settting static IP: {}".format(device_ip))
    deviceInfo = CommonLib.get_device_info(deviceName)
    net_mask = deviceInfo.get("managementMask","")
    status = "up"
    CommonLib.config_management_interface("DUT", interface, device_ip, net_mask, status, mode)

def onieSelfUpdate(update="new"):
    log.debug("Entering OnieLib class procedure: onieSelfUpdate")

    updater_info_dict = CommonLib.get_swinfo_dict("ONIE_updater")
    if update == "new":
        filename = updater_info_dict.get("newImage", "NotFound")
        file_path = updater_info_dict.get("hostImageDir", "NotFound")
    else:
        filename = updater_info_dict.get("oldImage", "NotFound")
        file_path = updater_info_dict.get("oldhostImageDir", "NotFound")
    server_ip = CommonLib.get_device_info("PC").get("managementIP","")
    log.debug("Prompt: {}".format(device.promptOnie))
    if not server_ip:
        raise Exception("Didn't find server IP.")
    updater_cmd = "onie-self-update tftp://{}/{}".format(server_ip, os.path.join(file_path, filename))
    expect_message = KapokConst.ONIE_DISCOVERY_PROMPT
    timeout_message = "tftp: timeout|tftp: read error"
    finish_prompt = "{}|{}".format(expect_message, timeout_message)
    retry = 3
    for i in range(retry):
        output = device.sendCmdRegexp(updater_cmd, finish_prompt, timeout=1200)
        if re.search(expect_message, output):
            break
        elif re.search(timeout_message, output):
            log.info("{}, retry left {} times.".format(timeout_message, retry-i-1))
            if i == retry - 1:
                raise Exception("tftp failed, after tried {} times".format(retry))
            continue
    device.sendMsg("\n")
    onie_discovery_stop_cmd = KapokConst.STOP_ONIE_DISCOVERY_KEY

    device.sendCmdRegexp(onie_discovery_stop_cmd, device.promptOnie, timeout=10)

def verifyOnieAndCPLDVersion(version="new"):
    log.debug("Entering OnieLib class procedure: verifyOnieAndCPLDVersion")
    escapeString = CommonLib.escapeString

    cmd = "get_versions"
    Image_info_dict = CommonLib.get_swinfo_dict("ONIE_Installer")
    onie_version = Image_info_dict.get("%sVersion"%version, "NotFound")
    onie_version_pattern = { "ONIE  %s"%(onie_version): "^ONIE\s+%s"%(escapeString(onie_version))}
    CPLD_version_dict = CommonLib.get_swinfo_dict("CPLD").get("%sVersion"%version, {})
    Uboot_version = CommonLib.get_swinfo_dict("UBOOT").get("%sVersion"%version, "")
    Uboot_pattern = escapeString(Uboot_version)
    onie_version_pattern.update({ Uboot_version: Uboot_pattern })

    for key_type, value in CPLD_version_dict.items():
        pattern_name = "{}  {}".format(key_type, value)
        pattern = "{}\s+{}".format(key_type, escapeString(value))
        onie_version_pattern.update({pattern_name: pattern})


    CommonLib.execute_check_dict('DUT', cmd, mode=Const.BOOT_MODE_ONIE, patterns_dict=onie_version_pattern,
                                 timeout=6)

@logThis
def checkversionbeforethetest():
    sys_cpld_version = CommonLib.get_swinfo_dict('CPLD').get('newVersion').get('SYSCPLD')
    cpld_dict = CommonLib.get_swinfo_dict('CPLD')
    led_cpld1_version = cpld_dict.get('newVersion').get('LEDCPLD1')
    led_cpld2_version = cpld_dict.get('newVersion').get('LEDCPLD2')
    fan_cpld = cpld_dict.get('newVersion').get('FANCPLD')
    uboot_version = CommonLib.get_swinfo_dict("UBOOT").get("newVersion", "NotFound")
    uboot_version = uboot_version.replace('(', '\(')
    uboot_version = uboot_version.replace(')', '\)')
    uboot_version = uboot_version.replace('+', '\+')
    log.cprint(uboot_version)
    onie_version = CommonLib.get_swinfo_dict("ONIE_Installer").get("newVersion", "NotFound")
    devicename = os.environ.get("deviceName", "")
    if "fenghuangv2" in devicename.lower():
        dev_type = DeviceMgr.getDevice(devicename).get('cardType')
        if dev_type == '1PPS':
            ASC_type = dev_type + '_ASC'
            ASC = CommonLib.get_swinfo_dict(ASC_type)
            ic2fpga = CommonLib.get_swinfo_dict(ASC_type).get("1pps", "NotFound")
        else:
            ASC_type = 'I2C_ASC'
            ic2fpga = CommonLib.get_swinfo_dict(ASC_type).get("fpga", "NotFound")
        uc_app = CommonLib.get_swinfo_dict("UC").get("newVersion", "NotFound").get("uC_app")
        uC_bl = CommonLib.get_swinfo_dict("UC").get("newVersion", "NotFound").get("uC_bl")
        asc10_0 = CommonLib.get_swinfo_dict(ASC_type).get("newVersion", "NotFound").get("ASC10-0")
        asc10_1 = CommonLib.get_swinfo_dict(ASC_type).get("newVersion", "NotFound").get("ASC10-1")
        asc10_2 = CommonLib.get_swinfo_dict(ASC_type).get("newVersion", "NotFound").get("ASC10-2")
        hw_dict = {'uc_app': uc_app, 'uc_bl': uC_bl, 'ASC10-0': asc10_0, 'ASC10-1': asc10_1, 'ASC10-2': asc10_2,
                   'I2CFPGA': ic2fpga}
        cpld_version_dict = {'SYSCPLD': sys_cpld_version, 'SWLEDCPLD1': led_cpld1_version,
                             'SWLEDCPLD2': led_cpld2_version, 'U-BOOT': uboot_version, 'ONIE': onie_version,
                             'FANCPLD': fan_cpld}
        check_version_cmd = 'get_versions'
        output = device.executeCmd(check_version_cmd)
    elif "tianhe" in devicename.lower():
        come_cpld_version = cpld_dict.get('newVersion').get('COMECPLD', "NotFound")
        asc10_0 = CommonLib.get_swinfo_dict('1PPS_ASC').get("newVersion", "NotFound").get("ASC10-0")
        asc10_1 = CommonLib.get_swinfo_dict('1PPS_ASC').get("newVersion", "NotFound").get("ASC10-1")
        asc10_2 = CommonLib.get_swinfo_dict('1PPS_ASC').get("newVersion", "NotFound").get("ASC10-2")
        asc10_3 = CommonLib.get_swinfo_dict('1PPS_ASC').get("newVersion", "NotFound").get("ASC10-3")
        asc10_4 = CommonLib.get_swinfo_dict('1PPS_ASC').get("newVersion", "NotFound").get("ASC10-4")
        ppsfpga = CommonLib.get_swinfo_dict('1PPS_ASC').get("1pps", "NotFound")
        hw_dict = {
            'ASC10-0': asc10_0,
            'ASC10-1': asc10_1,
            'ASC10-2': asc10_2,
            'ASC10-3': asc10_3,
            'ASC10-4': asc10_4,
            '1PPSFPGA': ppsfpga
        }
        cpld_version_dict = {
            'SYSCPLD': sys_cpld_version,
            'COMECPLD': come_cpld_version,
            'SWLEDCPLD1': led_cpld1_version,
            'SWLEDCPLD2': led_cpld2_version,
            'U-BOOT': uboot_version,
            'ONIE': onie_version,
            'FANCPLD': fan_cpld
        }
        check_version_cmd = 'get_versions'
        output = device.executeCmd(check_version_cmd)
    else:
        uc_app = CommonLib.get_swinfo_dict("UC").get("newVersion", "NotFound").get("uC_app")
        uC_bl = CommonLib.get_swinfo_dict("UC").get("newVersion", "NotFound").get("uC_bl")
        asc1 = CommonLib.get_swinfo_dict("ASC").get("newVersion", "NotFound").get("ASC1")
        asc2 = CommonLib.get_swinfo_dict("ASC").get("newVersion", "NotFound").get("ASC2")
        hw_dict = {'uc_app': uc_app, 'uc_bl': uC_bl, 'ASC1': asc1, 'ASC2': asc2}
        cpld_version_dict = {'SystemCPLD': sys_cpld_version, 'LEDCPLD1': led_cpld1_version,
                             'LEDCPLD2': led_cpld2_version, 'FANCPLD': fan_cpld, 'U-BOOT': uboot_version,
                             'ONIE': onie_version}
        export_cmd_list = ['export LD_LIBRARY_PATH=/root/diag/output', 'export CEL_DIAG_PATH=/root/diag']
        get_hw_version_path = '/root/diag'
        get_hw_versions_tool = 'cel-system-test'
        get_hw_versions_option = '--all'
        for cmd in export_cmd_list:
            device.executeCmd(cmd)
        cmd = 'cd ' + get_hw_version_path
        device.executeCmd(cmd)
        check_cmd = './' + get_hw_versions_tool + ' ' + get_hw_versions_option
        output = device.executeCmd(check_cmd)
    hw_dict.update(cpld_version_dict)
    keys_list = list(hw_dict.keys())
    values_list = list(hw_dict.values())
    passpattern = list()
    if len(keys_list) == len(values_list):
        for i in range(0, len(keys_list)):
            passpattern.append(keys_list[i] + '.*' + values_list[i])
    else:
        log.fail("get versions is failed")
        device.raiseException("Failure while get versions info")
    log.debug('passpattern=%s' % passpattern)
    passCount = 0
    fail_pattern = []

    for pattern in passpattern:
        found = False
        for line in output.splitlines():
            if re.search(pattern, line, re.IGNORECASE):
                log.debug('the matched version:%s' % line)
                found = True
                passCount += 1
                break
        if not found:
            fail_pattern.append(pattern.replace('.*', ': '))
    if passCount == len(passpattern):
        log.success("verify version is passed")
    else:
        log.fail("verify versions failed, not matched version: {}".format(str(fail_pattern)))
        device.raiseException("Failure while verify versions info")

@logThis
def checkdriverversion(pattern):
    check_driver_cmd = "lsmod"
    output = device.executeCmd(check_driver_cmd)
    CommonLib.execute_check_dict("DUT", "", patterns_dict=pattern, timeout=60,
                                check_output=output)


@logThis
def DiagformatDisk(fail_dict,cmd="mkfs.ext3 /dev/sda3", umount_mnt=True):

    if umount_mnt:
        output = run_command("mount", prompt=device.promptOnie,timeout=10)
        if re.search("/mnt", output):
            run_command(["cd /", "umount /mnt"], prompt=device.promptOnie,timeout=10)

    device.sendMsg(cmd + "\n")
    output = device.read_until_regexp("roceed anyway\? \(y,n\)\s+", timeout=90)
    device.sendMsg("y\n")
    output += device.read_until_regexp(device.promptOnie, timeout=60)
    fdisk_l_cmd = "fdisk -l \n"
    output += run_command(fdisk_l_cmd,prompt=device.promptOnie, timeout=5 )

    CommonLib.execute_check_dict("DUT", "", patterns_dict=fail_dict, timeout=10,
                                check_output=output, is_negative_test=True)

@logThis
def DiagmountDisk(fail_dict,cmd="mount /dev/sda3 /mnt"):

    cmd_list = ["cd /", "fdisk -l", cmd, "cd /mnt", "ls"]
    output = run_command(cmd_list, prompt=device.promptOnie,timeout=10)

    CommonLib.execute_check_dict("DUT", "", patterns_dict=fail_dict, timeout=10,
                                check_output=output, is_negative_test=True)

@logThis
def DiagdownloadImagesAndRecoveryDiagOS(fail_dict):

    diagos_files = CommonLib.get_swinfo_dict("DIAGOS").get("newImage")
    rootfs_file = diagos_files[:1]
    rename_files = ['rootfs.cpio.gz']
    run_command("cd /root",prompt=device.promptOnie )   #unzip file in /root to avoid space full issue
    log.info("rootfs_file: {}, rename_files: {}".format(rootfs_file, rename_files))
    CommonLib.tftp_get_files(Const.DUT, file_list=rootfs_file, renamed_file_list=rename_files, timeout=400)
    cmd_list = ["gunzip rootfs.cpio.gz", "cd /mnt", "cpio -i < /root/rootfs.cpio"]
    output = run_command(cmd_list, prompt=device.promptOnie,timeout=300)
    CommonLib.execute_check_dict("DUT", "", patterns_dict=fail_dict, timeout=10,
                                check_output=output, is_negative_test=True)
    run_command("rm /root/rootfs.cpio", prompt=device.promptOnie)
    run_command("rm -rf /mnt/root/*", prompt=device.promptOnie)
    run_command("cp -rf /root/* /mnt/root/", prompt=device.promptOnie)
    run_command("cd ./root",prompt=device.promptOnie)
    uimage_dtb = diagos_files[1:]
    rename_uimage_dtb = ["uImage", "celestica_cs8200-r0.dtb"]
    CommonLib.tftp_get_files(Const.DUT, file_list=uimage_dtb, renamed_file_list=rename_uimage_dtb, timeout=400)
    cmd_list = ["sync", "cd /", "umount /mnt"]
    output = run_command(cmd_list, prompt=device.promptOnie,timeout=300)
    CommonLib.execute_check_dict("DUT", "", patterns_dict=fail_dict, timeout=10,
                                check_output=output, is_negative_test=True)

def setOnieFppEnv(speed_mode):
    device.log_debug("Entering procedure setOnieFppEnv.\n")
    import KapokCommonLib
    KapokCommonLib.bootIntoUboot()
    cmd = 'setenv onie_fpp ' + speed_mode + '\n'
    device.sendMsg(cmd)
    device.sendMsg('saveenv \n')
    device.read_until_regexp('OK')
    KapokCommonLib.bootIntoOnieInstallMode()

def checkPRBS(fpp_option):
    device.log_debug("Entering procedure checkPRBS.\n")

    cmd = 'onie_port_cmd ' + fpp_option + ' prbs --enable'
    out = CommonLib.execute_command(cmd)
    match = re.search('diagtest serdes prbs.*', out)
    if match:
        pass
    else:
        raise Exception('enable prbs failed')

    cmd = 'onie_port_cmd ' + fpp_option + ' prbs --run --time=300'
    out = CommonLib.execute_command(cmd)
    match = re.search('diagtest serdes prbs set.*', out)
    if match:
        pass
    else:
        raise Exception('run prbs failed')

    cmd = 'onie_port_cmd ' + fpp_option + ' prbs --sync'
    out = CommonLib.execute_command(cmd)
    match = re.search('sync in process, please wait', out)
    if match:
        pass
    else:
        raise Exception('sync prbs failed')

    time.sleep(300)
    fail_list = list()
    fail_list2 = list()
    for i in range(0,2):
        cmd = 'onie_port_cmd ' + fpp_option + ' prbs --get'
        out = CommonLib.execute_command(cmd)
    for line in out.splitlines():
        if re.search('FAIL', line):
            fail_list.append(line)
    if fail_list:
        log.debug('fail line=%s' %fail_list)
        time.sleep(120)
        out = CommonLib.execute_command(cmd)
        for line in out.splitlines():
            if re.search('FAIL', line):
                fail_list2.append(line)
        for fail_line in fail_list2:
            if fail_line in fail_list:
                log.debug('fail line=%s' %fail_list2)
                raise Exception('check prbs failed')
    else:
        log.success('check prbs succeeded')

@logThis
def port_enable_and_check_status(sumport):
    import CommonKeywords
    enable_port_cmd = 'port enable 1-' + str(sumport)
    device.sendMsg(enable_port_cmd + '\n')
    ifcs_cmd = show_port_info
    pattern = []
    for i in range(1,int(sumport)+1):
        temp = str(i) + '.*UP[ \t]+\|[ \t]+LINK_UP.*'
        pattern.append(temp)
        time.sleep(1)
    log.info('*******pattern=%s ' % pattern)
    for i in range(0,2):
        output=run_command('ifcs show devport',prompt='IVM:0>',timeout=60)
    CommonKeywords.should_match_ordered_regexp_list(output, pattern)

@logThis
def run_each_speed(command_list,sumport):
    import CommonKeywords
    device.sendMsg('cd ' + SDK_PATH + '\n')
    for cmd in command_list:
        output = run_command(cmd,prompt='IVM:0>',timeout=100)
        pattern = []
        for i in range(1,int(sumport)+1):
            temp = str(i) + '.*UP[ \t]+\|[ \t]+LINK_UP.*'
            pattern.append(temp)
            time.sleep(1)
          #  log.info('*******pattern=%s ' % pattern)
        for i in range(0,2):
            output1=run_command('ifcs show devport',prompt='IVM:0>',timeout=60)
            time.sleep(10)
        try:
           check =  CommonKeywords.should_match_ordered_regexp_list(output1, pattern)
        except Exception as e:
            log.fail(str(e))
            log.fail('cmd %s is fail.' % cmd)
        device.sendMsg('exit'+'\r\n')
        time.sleep(1)
        currentmode = device.getCurrentPromptMode()
        if currentmode == 'onie':
            log.info('Entered into sdk console')
        else:
            device.raiseException('Occured falws. please check output!')
    if str("Not found pattern:") in check:
        raise Exception("FEC Enable test failed due to port status")



def setDefaultOnieFpp():
    device.log_debug("Entering procedure setDefaultOnieFpp.\n")
    KapokCommonLib.bootIntoUboot()
    cmd = '''setenv onie_fpp ""''' + '\n'
    device.sendMsg(cmd)
    device.sendMsg('saveenv \n')
    device.read_until_regexp('OK')
    device.sendMsg('reset\n')
    device.read_until_regexp(KapokConst.STOP_AUTOBOOT_PROMPT, timeout=100)
    device.sendMsg(KapokConst.STOP_AUTOBOOT_KEY)
    KapokCommonLib.bootIntoOnieInstallMode()
    device.read_until_regexp(device.promptOnie, timeout=100)
    cmd = 'ifconfig -a \n'
    fppCount = 0
    device.sendMsg(cmd)
    try:
        device.read_until_regexp('fpp\d+\-\d\t+.*')
        fppCount += 1
    except Exception as err:
        log.cprint(str(err))
    if fppCount:
        log.fail('failed to set default fpp mode')
        raise Exception('failed to set default fpp mode')
    else:
        log.success('set default fpp mode passed')

@logThis
def portEnabled():
    cmd = './integrator_mode -m "sfp_detect" -d \n'
    device.sendMsg(cmd)
    time.sleep(120)
  #  device.read_until_regexp('Port Enabled set')
    device.read_until_regexp('Integrator mode config done')

@logThis
def showDevport(pattern):
    cmd = './cls_shell ifcs show devport \n'
    device.sendMsg(cmd)
    output = device.read_until_regexp(port_info_finish_prompt, timeout=60)
    ret_code = check_output(output, pattern)
    if ret_code == 0:
        device.raiseException("failed to check devport info")

@logThis
def diagtestKnetShow(pattern=None):
    cmd = './cls_shell diagtest knet show \n'
    device.sendMsg(cmd)
    output = device.read_until_regexp('show l2vni table', timeout=60)
    output += device.read_until_regexp('ONIE\:', timeout=100)
    if not pattern:
        matchCount = 0
        for line in output.splitlines():
            if re.search('Member\s+\:\s+\(sysport\:.*\)', line):
                matchCount += 1
        if matchCount == 128:
            log.success('check diagtest knet info passed')
        else:
            raise Exception('failed to check diagtest knet info')
    else:
        ret_code = check_output(output, pattern)
        if ret_code == 0:
            device.raiseException("failed to check knet info")

@logThis
def exitVlanSetting(mark=False):
    cmd1 = './cls_shell exit \n'
    cmd2 = './integrator_mode -m "sfp_detect" -k -d \n'
    device.sendMsg(cmd1)
    device.read_until_regexp('Innovium Switch PCIe Driver closed successfully', timeout=30)
    if mark:
        device.sendMsg(cmd2)
        device.read_until_regexp('Knet config done', timeout=100)

@logThis
def remoteShellCheckPortInfo():
    change_dir_to_sdk_path()
    enable_remote_shell_cmd = './auto_load_user.sh  -d \n'
    device.sendCmd(enable_remote_shell_cmd,'#',timeout=10)
    device.sendCmd("./cls_shell exit",'#',timeout=10)
    device.sendCmd(enable_remote_shell_cmd,'#',timeout=10)
    device.read_until_regexp('misc config', timeout=40)
    time.sleep(30)
    show_port_info_cmd = './cls_shell ifcs show devport \n'
    for i in range(0,2):
        output=run_command(show_port_info_cmd,prompt=port_info_finish_prompt,timeout=60)
    ret_code = check_output(output, patterns=PAM4_400G_32_link_pattern)
    if ret_code == 0:
        exit_cmd = './cls_shell exit \n'
        device.sendMsg(exit_cmd)
        device.raiseException("failed cmd is {}".format(show_port_info_cmd))

    exit_cmd = './cls_shell exit \n'
    device.sendMsg(exit_cmd)
    device.read_until_regexp('Innovium Switch PCIe Driver closed successfully', timeout=20)

@logThis
def remoteShellSaveLogToFile():
    cmd = './auto_load_user.sh -df /tmp/sdk.log \n'
    device.sendMsg(cmd)
    device.read_until_regexp('misc config end', timeout=30)
    time.sleep(30)
    show_port_info_cmd = './cls_shell ifcs show devport \n'
    device.sendMsg(show_port_info_cmd)
    device.read_until_regexp('ONIE\:.*', timeout=60)

    cat_log_cmd = 'cat /tmp/sdk.log'
    output = device.executeCmd(cat_log_cmd, timeout=10)
    ret_code = check_output(output, patterns=PAM4_400G_32_link_pattern)
    if ret_code == 0:
        exit_cmd = './cls_shell exit \n'
        device.sendMsg(exit_cmd)
        device.raiseException("failed cmd is {}".format(show_port_info_cmd))

    exit_cmd = './cls_shell exit \n'
    device.sendMsg(exit_cmd)
    device.read_until_regexp('Innovium Switch PCIe Driver closed successfully', timeout=20)

@logThis
def runEssScript():
        device.sendMsg('./cls_shell exit'+' \n')
        time.sleep(25)
        cmd = './cel_test/ess_traffic_test_32x400.sh'
        device.sendMsg(cmd+' \n')
        device.read_until_regexp('Traffic test: Passed',timeout=1500)

@logThis
def check_port_info():
    device.log_debug("Entering procedure check_port_infomation.\n")
    output = device.sendCmdRegexp(show_port_info,sdkConsole,timeout=90)
    if (output!=0):
        return output
    else:
        device.raiseException("Failed to check port info")

@logThis
def check_port_enable(portmode,portnum):
    device.log_debug("Entering procedure check_port_enable.\n")
    if str(portnum) == "all":
        enable_cmd = "port enable all"
    else:
        enable_cmd = "port enable 1-" + str(portnum) + "\r\n"
    output = device.sendCmdRegexp(enable_cmd,sdkConsole,timeout=90)
    time.sleep(300)
    output1 = device.sendCmdRegexp(show_port_info,sdkConsole,timeout=90)
    port_infos_pattern = get_port_infos_regexp(portmode,link=True)
    ret_code = check_output(output1, patterns=port_infos_pattern)
    if ret_code == 0:
        device.raiseException("failed cmd is {}".format(show_port_info))





@logThis
def port_disable_and_check_status(sumport):
    import CommonKeywords
    disable_port_cmd = 'port disable 1-' + str(sumport)
    device.sendMsg(disable_port_cmd + '\n')
    ifcs_cmd = show_port_info
    pattern = []
    for i in range(1,int(sumport)+1):
        temp = str(i) + '.*DOWN[ \t]+\|[ \t]+DISABLED.*'
        pattern.append(temp)
        time.sleep(1)
    log.info('*******pattern=%s ' % pattern)
    device.sendMsg(ifcs_cmd)
    device.read_until_regexp(ifcs_cmd, timeout=60)
    time.sleep(6)
    output = device.read_until_regexp('IVM', timeout=60)
    CommonKeywords.should_match_ordered_regexp_list(output, pattern)

@logThis
def Log_Info(msg):
    device.log_info(msg)


@logThis
def clearPortCounters():
    device.log_debug("Entering procedure clear counter\n")
    diagtest_cmd = "ifcs clear counters devport"
    output = device.sendCmdRegexp(diagtest_cmd, "IVM.*",timeout=60)
    ret_code = check_output(output, patterns=[''])

@logThis
def checkBerLevel(portmode,portnum):
    output1 = device.sendCmdRegexp(show_port_info,sdkConsole,timeout=90)
    time.sleep(10)
    output1 = device.sendCmdRegexp(show_port_info,sdkConsole,timeout=90)
    pattern = []
    if portmode == "-m 1-32:optics_2x100G:down-p2:fec-dis":
        for i in range(1,11):
            if(i % 2 != 0):
                temp = str(i) + '.*UP[ \t]+\|[ \t]+LINK_UP.*'
                pattern.append(temp)
            if(i % 2 == 0):
                temp = str(i) + '.*DOWN[ \t]+\|[ \t]+DISABLED.*'
                pattern.append(temp)
    else:
        pattern = get_port_infos_regexp(portmode,link=True)

    try:
        ret_code = check_output(output1, patterns=pattern)
    except Exception as err:
        if ret_code == 0:
            log.fail(str(err))
    cmd_lst = [prbs_en_cmd.format(portnum),prbs_set_cmd.format(portnum),prbs_sync_cmd.format(portnum),'shell sleep 40']
    output=run_command(cmd_lst,prompt='IVM:0>',timeout=60)
    Ber_check = run_command(prbs_get_cmd.format(portnum),prompt='IVM:0>',timeout=60)
    time.sleep(10)
    Ber_check = run_command(prbs_get_cmd.format(portnum),prompt='IVM:0>',timeout=60)
    output1="\n".join(Ber_check.split("\n")[7:-2]).strip('\n')
    pattern = []
    if portmode == "-m 1-32:optics_2x100G:down-p2:fec-dis":
        for i in range(1,11):
            if(i % 2 != 0):
                for j in range(1,5):
                    temp = str(i) + '.*SYNC.*PASS.*'
                    pattern.append(temp)
            if(i % 2 == 0):
                for j in range(1,5):
                    temp = str(i) + '.*LINK_DOWN_NO_SYNC.*FAIL.*'
                    pattern.append(temp)
        try:
            ret_code = check_output(output1, patterns=pattern)
        except Exception as err:
            if ret_code == 0:
                raise Exception(str(err))
                log.info("BER Check Failed!!")
        log.success("BER Check Passed!!")
    else:
        for each in output1.splitlines():
            if not re.search("PASS",each,re.IGNORECASE):
                raise Exception("BER Check FAILED!!")
        log.success("BER Check Passed!!")
    cmd_lst2=[prbs_clear_cmd.format(portnum),prbs_mode_en_cmd.format(portnum)]
    output=run_command(cmd_lst2,prompt='IVM:0>',timeout=60)




@logThis
def load_prbs_mode(cmd=None, patterns=init_pass_pattern, port_sum_pattern=init_port_pattern,
                     port_total=32, is_negative_test=False, timeout=3600):
    device.sendMsg("./cls_shell exit\r\n")
    time.sleep(35)
    device.log_debug("Entering procedure load_user_mode.\n")
    return check_load_user(cmd, pattern_dict=patterns, port_sum_pattern=port_sum_pattern,
                                   port_total=port_total, prompt_str='#', timeout=timeout)


#####################################################################################################
@logThis
def switch_sdk_folder_path(path):
    device.getPrompt(Const.BOOT_MODE_ONIE)
    device.sendMsg('\n')
    cmd = "cd " + path
    p1 = "can't cd"
    output = device.executeCommand(cmd, device.promptOnie)
    if re.search(p1, output):
        log.fail('switch folder fail!')
        raise Exception('Change %s path failed!' % (path))
    else:
        log.info('Switch the folder successfully!')

@logThis
def load_user_mode_tianhe(tool, option=None):
    if option == None:
        cmd = tool
    else:
        cmd = tool + ' ' + option
    device.sendMsg("./cls_shell exit\r\n")
    time.sleep(35)
    device.executeCommand(cmd, device.promptSdk, timeout=300)

@logThis
def get_new_image_name(image_type):
    imageObj = CommonLib.get_swinfo_dict(image_type)
    imageName = imageObj.get("newImage", "NotFound")
    return imageName

@logThis
def get_sub_new_image_version(image_type, name):
    imageObj = CommonLib.get_swinfo_dict(image_type)
    nameObj = imageObj.get(name, "NotFound")
    newVer = nameObj.get("newVersion", "NotFound")
    return newVer

@logThis
def check_sdk_version_tianhe(cmd1, cmd2):
    pass_count = 0
    error_count = 0
    sdkImage = get_new_image_name('SDK')
    ifcsVer = get_sub_new_image_version('SDK', 'IFCS')
    device.sendMsg(cmd1)
    output = device.read_until_regexp(CatReadMe_regexp, timeout=10)
    if sdkImage in output:
        pass_count += 1
        log.success('Check the sdk image name [%s] is pass.'%sdkImage)
    else:
        error_count += 1
        log.fail('Check the sdk image name [%s] is fail.'%sdkImage)
    device.sendMsg(cmd2)
    output = device.read_until_regexp(ifcs_regexp, timeout=10)
    if ifcsVer in output:
        pass_count += 1
        log.success('Check the sdk IFCS version [%s] is pass.' % ifcsVer)
    else:
        error_count += 1
        log.fail('Check the sdk IFCS version [%s] is fail.' % ifcsVer)
    if error_count or pass_count == 0:
        raise Exception('Failed run check_sdk_version_tianhe')

@logThis
def check_sdk_diff_load_user_mode(tool, showCmd, option=None):
    pass_count = 0
    p1 = 'Total devport count: (\d+)'
    p2 = r'\|[ \t]+(\d+) \|[ \t]+ETH \|[ \t]+ISG\d+ \|[ \t]+\d \|[ \t]+(\d) \| \(sysport:\s+\d+\) \|[ \t]+(\d+G) \|[ \t]+(UP|DOWN) \|'
    #1. init sdk
    load_user_mode_tianhe(tool, option)
    time.sleep(2)
    #2. show port count
    output = run_command(showCmd, prompt=port_info_finish_prompt, timeout=80)
    time.sleep(2)
    #3. exit sdk mode
    exit_user_mode()
    #4. check port count result
    for line in output.splitlines():
        res1 = re.search(p1, line)
        if res1:
            total_count = int(res1.group(1)) - 8
        # log.info('####%s####'%line)
        res = re.search(p2, line)
        if res:
            portNum = res.group(1)
            portSpeed = res.group(3)
            if (option == None) or ('1x400G' in option):
                if portSpeed == '400G':
                    pass_count += 1
                    log.info('The Port-%s get the speed is %s'%(portNum, portSpeed))
            elif ('4x100G' in option) or ('1x100G' in option) or ('2x100G' in option):
                if portSpeed == '100G':
                    pass_count += 1
                    log.info('The Port-%s get the speed is %s'%(portNum, portSpeed))
            elif ('1x40G' in option):
                if portSpeed == '40G':
                    pass_count += 1
                    log.info('The Port-%s get the speed is %s'%(portNum, portSpeed))
            elif ('4x25G' in option):
                if portSpeed == '25G':
                    pass_count += 1
                    log.info('The Port-%s get the speed is %s'%(portNum, portSpeed))
            elif ('4x10G' in option) or ('1x10G' in option):
                if portSpeed == '10G':
                    pass_count += 1
                    log.info('The Port-%s get the speed is %s'%(portNum, portSpeed))
    if total_count == pass_count:
        log.success('Check devport count %s pass.'%total_count)
    else:
        raise Exception('Failed run total count is %d, pass count is %d'%(total_count, pass_count))

@logThis
def check_ber_level_test(tool, option, option2=''):
    p1 = r'copper %s BER Test ----------  PASS'%option
    if option2:
        cmd = tool + option + ' ' + option2
    else:
        cmd = tool + option
    output = CommonLib.execute_command(cmd, timeout=300)
    if p1 in output:
        log.success('Check %s ber pass.'%option)
    else:
        raise Exception('Failed run check_ber_level_test')

@logThis
def check_double_port_status(cmd):
    time.sleep(30)
    pass_count = 0
    p1 = r'\|[ \t]+(\d+) \|[ \t]+ETH \|[ \t]+ISG\d+ \|[ \t]+\d \|[ \t]+(\d) \| \(sysport:\s+\d+\) \|[ \t]+(\d+G) \|[ \t]+(\w+) \|'
    p2 = 'Total devport count: (\d+)'
    device.sendCmd(cmd)
    output = device.read_until_regexp(sdkConsole + '|' + device.promptOnie, timeout=60)
    for line in output.splitlines():
        res1 = re.search(p2, line)
        if res1:
            total_count = int(res1.group(1)) - 8
        res = re.search(p1, line)
        if res:
            portNum = res.group(1)
            portSpeed = res.group(3)
            portStatus = res.group(4)
            if int(portNum) % 2 == 0:
                if portStatus == 'DOWN':
                    pass_count += 1
                    log.success('The Port-%s get the speed is %s, Status is %s' % (portNum, portSpeed, portStatus))
            else:
                if portStatus == 'UP':
                    pass_count += 1
                    log.success('The Port-%s get the speed is %s, Status is %s' % (portNum, portSpeed, portStatus))
    if total_count == pass_count:
        log.success('Check devport status pass.')
    else:
        raise Exception('Failed run port status, total is %d, pass count is %d'%(total_count, pass_count))

@logThis
def run_odd_ber_test(cmdLst, pattern):
    pass_count = 0
    error_count = 0
    p1 = r'\|\s+(\d+)\s:\s+([0123])\s:\s+ISG\d+\s+:\s+\d\s+:\s+PRBS31\s+:\s+\d+\s+:\s+\w+\s+:\s+(.*)\s+:\s+(\w+)\s+\|'
    for cmd in cmdLst:
        time.sleep(1)
        device.sendCmd(cmd)
    output = device.read_until_regexp(device.promptOnie, timeout=300)
    for line in output.splitlines():
        res = re.search(p1, line)
        if res:
            portNum = res.group(1)
            laneNum = res.group(2)
            laneBer = res.group(3)
            portStatus = res.group(4)
            if int(portNum) % 2 != 0:
                if portStatus == 'PASS':
                    if (int(laneNum) == 0) or (int(laneNum) == 1) or (int(laneNum) == 2) or (int(laneNum) == 3):
                        pass_count += 1
                        log.success('Check Port-%s lane-%s ber result is pass.'%(portNum, laneNum))
                elif portStatus == 'FAIL':
                    error_count += 1
                    log.fail('Check Port-%s lane-%s ber result is fail, get the value is %s'%(portNum, laneNum, laneBer))
    if (error_count == 0) and (pass_count == int(pattern)):
        log.success('Check port BER PASS!')
    else:
        raise Exception('Fail run_ber_test, Expect pass num is %s, Get pass num is %d'%(pattern, pass_count))

@logThis
def show_port_status_test(cmd, speedType=''):
    time.sleep(50)
    pass_count = 0
    error_count = 0
    total_count = 0
    p1 = r'\|[ \t]+(\d+) \|[ \t]+ETH \|[ \t]+ISG\d+ \|[ \t]+\d \|[ \t]+(\d) \| \(sysport:\s+\d+\) \|[ \t]+(\d+G) \|[ \t]+(\w+) \|'
    p2 = 'Total devport count: (\d+)'
    device.sendCmd(cmd)
    output = device.read_until_regexp(sdkConsole, timeout=60)
    for line in output.splitlines():
        res1 = re.search(p2, line)
        if res1:
            total_count = int(res1.group(1)) - 8
        res = re.search(p1, line)
        if res:
            portNum = res.group(1)
            portSpeed = res.group(3)
            portStatus = res.group(4)
            if speedType == '10_1':
                if (int(portNum) in range(1, 33)) or (int(portNum) in range(61, 101)):
                    if (portSpeed == '25G') and (portStatus == 'UP'):
                        pass_count += 1
                        log.success('The Port-%s get the speed is %s, Status is %s' % (portNum, portSpeed, portStatus))
                    elif (portSpeed == '25G') and (portStatus == 'DOWN'):
                        error_count += 1
                        log.fail('The Port-%s get the speed is %s, Status is %s' % (portNum, portSpeed, portStatus))
                elif int(portNum) in range(33, 61):
                    if (portSpeed == '100G') and (portStatus == 'UP'):
                        pass_count += 1
                        log.success('The Port-%s get the speed is %s, Status is %s' % (portNum, portSpeed, portStatus))
                    elif (portSpeed == '100G') and (portStatus == 'DOWN'):
                        error_count += 1
                        log.fail('The Port-%s get the speed is %s, Status is %s' % (portNum, portSpeed, portStatus))
            elif speedType == '10_2':
                if (int(portNum) in range(1, 21)) or (int(portNum) in range(37, 45)):
                    if (portSpeed == '100G') and (portStatus == 'UP'):
                        pass_count += 1
                        log.success('The Port-%s get the speed is %s, Status is %s' % (portNum, portSpeed, portStatus))
                    elif (portSpeed == '100G') and (portStatus == 'DOWN'):
                        error_count += 1
                        log.fail('The Port-%s get the speed is %s, Status is %s' % (portNum, portSpeed, portStatus))
                elif int(portNum) in range(21, 37):
                    if (portSpeed == '10G') and (portStatus == 'UP'):
                        pass_count += 1
                        log.success('The Port-%s get the speed is %s, Status is %s' % (portNum, portSpeed, portStatus))
                    elif (portSpeed == '10G') and (portStatus == 'DOWN'):
                        error_count += 1
                        log.fail('The Port-%s get the speed is %s, Status is %s' % (portNum, portSpeed, portStatus))
            elif speedType == '10_3':
                if (int(portNum) in range(1, 21)) or (int(portNum) in range(37, 69)):
                    if (portSpeed == '100G') and (portStatus == 'UP'):
                        pass_count += 1
                        log.success('The Port-%s get the speed is %s, Status is %s' % (portNum, portSpeed, portStatus))
                    elif (portSpeed == '100G') and (portStatus == 'DOWN'):
                        error_count += 1
                        log.fail('The Port-%s get the speed is %s, Status is %s' % (portNum, portSpeed, portStatus))
                elif int(portNum) in range(21, 37):
                    if (portSpeed == '10G') and (portStatus == 'UP'):
                        pass_count += 1
                        log.success('The Port-%s get the speed is %s, Status is %s' % (portNum, portSpeed, portStatus))
                    elif (portSpeed == '10G') and (portStatus == 'DOWN'):
                        error_count += 1
                        log.fail('The Port-%s get the speed is %s, Status is %s' % (portNum, portSpeed, portStatus))
            else:
                if portStatus == 'UP':
                    pass_count += 1
                    log.success('The Port-%s get the speed is %s, Status is %s' % (portNum, portSpeed, portStatus))
                elif portStatus == 'DOWN':
                    error_count += 1
                    log.fail('The Port-%s get the speed is %s, Status is %s' % (portNum, portSpeed, portStatus))
    if (error_count == 0) and (total_count == pass_count):
        log.success('Check devport status pass.')
    else:
        raise Exception('Failed run port status, total is %d, pass count is %d'%(total_count, pass_count))

@logThis
def run_ber_test(cmdLst, pattern):
    pass_count = 0
    error_count = 0
    p1 = r'\|\s+(\d+)\s:\s+([0123])\s:\s+ISG\d+\s+:\s+\d\s+:\s+PRBS31\s+:\s+0\s+:\s+SYNC\s+:\s+(.*)\s+:\s+(\w+)\s+\|'
    for cmd in cmdLst:
        time.sleep(1)
        device.sendCmd(cmd)
    output = device.read_until_regexp(device.promptOnie, timeout=300)
    for line in output.splitlines():
        res = re.search(p1, line)
        if res:
            portNum = res.group(1)
            laneNum = res.group(2)
            laneBer = res.group(3)
            portStatus = res.group(4)
            if portStatus == 'PASS':
                if (int(laneNum) == 0) or (int(laneNum) == 1) or (int(laneNum) == 2) or (int(laneNum) == 3):
                    pass_count += 1
                    log.success('Check Port-%s lane-%s ber result is pass.'%(portNum, laneNum))
            elif portStatus == 'FAIL':
                error_count += 1
                log.fail('Check Port-%s lane-%s ber result is fail, get the value is %s'%(portNum, laneNum, laneBer))
    if (error_count == 0) and (pass_count == int(pattern)):
        log.success('Check port BER PASS!')
    else:
        raise Exception('Fail run_ber_test, Expect pass num is %s, Get pass num is %d'%(pattern, pass_count))

@logThis
def check_load_prbs_mode(tool, option):
    p1 = 'Knet config done'
    p2 = 'misc config end'
    run_command(SDK_SHELL_EXIT, prompt=device.promptOnie, timeout=80)
    time.sleep(5)
    cmd = './' + tool + ' ' + option
    output = device.executeCommand(cmd, device.promptOnie, timeout=300)
    if (p1 in output) or (p2 in output):
        log.success('Run sdk load prbs pass!')
    else:
        raise Exception('Failed run check_load_prbs_mode')

@logThis
def check_shell_port_status(cmd):
    time.sleep(10)
    pass_count = 0
    p1 = r'\|[ \t]+(\d+) \|[ \t]+ETH \|[ \t]+ISG\d+ \|[ \t]+\d \|[ \t]+(\d) \| \(sysport:\s+\d+\) \|[ \t]+(\d+G) \|[ \t]+(\w+) \|'
    p2 = 'Total devport count: (\d+)'
    output=run_command(cmd, prompt=device.promptOnie, timeout=60)
    for line in output.splitlines():
        res1 = re.search(p2, line)
        if res1:
            total_count = int(res1.group(1)) - 8
        res = re.search(p1, line)
        if res:
            portNum = res.group(1)
            portSpeed = res.group(3)
            portStatus = res.group(4)
            if portStatus == 'UP':
                pass_count += 1
                log.success('The Port-%s get the speed is %s, Status is %s' % (portNum, portSpeed, portStatus))
    if total_count == pass_count:
        log.success('Check devport status pass.')
    else:
        raise Exception('Failed run port status, total is %d, pass count is %d'%(total_count, pass_count))

@logThis
def enable_or_disable_prbs_test(tool, option, pattern):
    pass_count = 0
    error_count = 0
    p1 = r'PRBS mode-en set to (\d)'
    cmd = tool + ' ' + option + pattern
    output = device.executeCommand(cmd, device.promptOnie, timeout=60)
    for line in output.splitlines():
        res = re.search(p1, line)
        if res:
            pass_count += 1
            getValue = res.group(1)
            if getValue == pattern:
                log.success('enable or disable prbs pass.')
            else:
                error_count += 1
                log.fail('set prbs fail.')
    if error_count or pass_count == 0:
        raise Exception('Failed run enable_or_disable_prbs_test')

@logThis
def exit_sdk_shell_mode(cmd):
    run_command(cmd, prompt=device.promptOnie, timeout=60)

@logThis
def check_shell_ber_test(cmdLst, pattern, caseType=''):
    pass_count = 0
    error_count = 0
    p1 = r'\|\s+(\d+)\s:\s+(\d+)\s:\s+ISG\d+\s+:\s+\d\s+:\s+PRBS31\s+:\s+\d+\s+:\s+(SYNC|NO_SYNC)\s+:\s+(.*)\s+:\s+(\w+)\s+\|'
    for cmd in cmdLst:
        time.sleep(2)
        device.sendCmd('\n')
        output = CommonLib.execute_command(cmd, timeout=600)
    for line in output.splitlines():
        res = re.search(p1, line)
        if res:
            portNum = res.group(1)
            laneNum = res.group(2)
            laneBer = res.group(4)
            portStatus = res.group(5)
            if caseType == '64x100-1G':
                if int(portNum) % 2 != 0:
                    if portStatus == 'PASS':
                        pass_count += 1
                        log.success('Check Port-%s lane-%s ber result is pass.' % (portNum, laneNum))
                    elif portStatus == 'FAIL':
                        error_count += 1
                        log.fail('Check Port-%s lane-%s ber fail, get the value is %s' % (portNum, laneNum, laneBer))
            else:
                if portStatus == 'PASS':
                    pass_count += 1
                    log.success('Check Port-%s lane-%s ber result is pass.' % (portNum, laneNum))
                elif portStatus == 'FAIL':
                    error_count += 1
                    log.fail('Check Port-%s lane-%s ber fail, get the value is %s' % (portNum, laneNum, laneBer))
    if (error_count == 0) and (pass_count == int(pattern)):
        log.success('Check port BER PASS!')
    else:
        raise Exception('Fail run_ber_test, Expect pass num is %s, Get pass num is %d'%(pattern, pass_count))

@logThis
def check_the_port_fec_test(tool, option):
    pass_count = 0
    error_count = 0
    p1 = r'\[DiagTest result\]:\s+(.*)\s+(FEC|Preemphassis|Traffic)\s+Test\s+\-+\s+(\w+)'
    cmd = tool + option
    output = device.executeCommand(cmd, device.promptOnie, timeout=900)
    for line in output.splitlines():
        res = re.search(p1, line)
        if res:
            portMode = res.group(1)
            portStatus = res.group(3)
            if portStatus == 'PASS':
                pass_count += 1
                log.success('Check Port %s fec result is %s!'%(portMode, portStatus))
            elif portStatus == 'FAIL':
                error_count += 1
                log.fail('Check Port %s fec result is %s!'%(portMode, portStatus))
    if error_count or pass_count == 0:
        raise Exception('Failed run check_the_port_fec_test')

@logThis
def remote_shell_load_test(cmd):
    run_command(SDK_SHELL_EXIT, prompt=device.promptOnie, timeout=80)
    time.sleep(5)
    device.executeCommand(cmd, device.promptOnie, timeout=300)

@logThis
def run_memory_test_in_background(cmdLst):
    for cmd in cmdLst:
        time.sleep(2)
        device.executeCommand(cmd, device.promptDiagOS, timeout=300)

@logThis
def verify_the_mem_test_is_running(cmd):
    p1 = '6000M'
    p2 = r'(\d+) root'
    output = device.executeCommand(cmd, device.promptDiagOS, timeout=300)
    if p1 in output:
        log.success('mem test is still running in background')
        for line in output.splitlines():
            res = re.search(p2, line)
            if res:
                pidValue = res.group(1)
    else:
        raise Exception('mem do not run in background')
    return pidValue

@logThis
def download_snake_file(cmdLst):
    dhcpTool = 'udhcpc'
    device.executeCommand(dhcpTool, device.promptDiagOS, timeout=300)
    for fileName in cmdLst:
        time.sleep(1)
        cmd = 'tftp -g ' + server_ip + ' -r ' + fileName
        device.executeCommand(cmd, device.promptDiagOS, timeout=300)

@logThis
def run_snake_test_suite(cmdLst):
    error_count = 0
    cmd1 = 'tar -zxvf ' + cmdLst[0]
    cmd2 = 'chmod +x ' + cmdLst[1]
    cmd3 = './' + cmdLst[1]
    #1. untar file
    device.executeCommand(cmd1, device.promptDiagOS, timeout=300)
    time.sleep(1)
    #2. change the run authority
    device.executeCommand(cmd2, device.promptDiagOS, timeout=300)
    #3. run 5 times
    pattern_lst = ['SNAKE_TESTSUITE_PFSTATUS: PASS',
                   'ECC_PFSTATUS: PASS',
                   'ECC_UE_PFSTATUS: PASS',
                   'ECC_CE_PFSTATUS: PASS',
                   'AGG_PFSTATUS: ECC_PASS_SNAKE_TESTSUITE_PASS',
                   'TCAM_TEST_STATUS: PASS',
                   'MASTER_ASIC_TEMPERATURE_TEST_STATUS: PASS',
                   'REMOTE_ASIC_TEMPERATURE_TEST_STATUS: PASS'
                    ]
    for i in range(1, 6):
        output = device.executeCommand(cmd3, device.promptDiagOS, timeout=300)
        pass_count = 0
        for pattern in pattern_lst:
            if pattern in output:
                pass_count += 1
        if pass_count == len(pattern_lst):
            log.success('Check time-%d snake test suite pass!'%i)
        else:
            error_count += 1
            log.fail('Check time-%d snake test suite fail!'%i)
    if error_count:
        raise Exception('Failed run run_snake_test_suite')

@logThis
def monitor_mem_test_complete(cmd):
    pass_count = 0
    p1 = 'Mem test : Passed'
    log.info('Run the below cmd: [%s]'%cmd)
    output = device.executeCommand(cmd, p1, timeout=1200)
    if p1 in output:
        pass_count += 1
        log.success('Check mem test log pass, click ctrl+c exit')
        #device.executeCommand(Const.KEY_CTRL_C, 'Done', timeout=120)
        device.sendMsg(Const.KEY_CTRL_C + '\n')
        device.read_until_regexp('Done', timeout=120)
    # #2. kill pid
    # pidRes = verify_the_mem_test_is_running(PS_TOOL)
    # if pidRes:
    #     cmd = 'kill ' + pidRes
    #     device.executeCommand(cmd, device.promptDiagOS, timeout=300)
    if pass_count == 0:
        raise Exception('Failed run monitor_mem_test_complete')

@logThis
def check_mem_result(cmd):
    output = device.executeCommand(cmd, device.promptDiagOS, timeout=300)
    p1 = 'Mem test : Passed'
    if p1 in output:
        log.success('Check mem test log pass!')
    else:
        raise Exception('Failed run check_mem_result')

@logThis
def check_the_mem_usage_log(cmd):
    p1 = 'Mem:\s+\d+\s+\d+\s+(\d+)\s+'
    error_count = 0
    output = device.executeCommand(cmd, device.promptDiagOS, timeout=300)
    for line in output.splitlines():
        res = re.search(p1, line)
        if res:
            getValue = res.group(1)
            if int(getValue) < 400000:
                error_count += 1
                log.fail('Check mem free value is lt 400M, get value is %s.'%getValue)
    if error_count:
        raise Exception('Failed run check_the_mem_usage_log')

@logThis
def switch_sdk_folder_in_diag_mode(path):
    cmd = "cd " + path
    p1 = "can't cd"
    output = device.executeCommand(cmd, device.promptDiagOS)
    if re.search(p1, output):
        log.fail('switch folder fail!')
        raise Exception('Change %s path failed!' % (path))
    else:
        log.info('Switch the folder successfully!')

@logThis
def port_enable_all_test(cmd):
    device.sendCmdRegexp(cmd, sdkConsole, timeout=90)

@logThis
def set_uboot_parameters_then_enter_onie_bootcmd_mode(cmd):
    #device.sendMsg(cmd + '\n')
    pass_count = 0
    p1 = r'fpp\d+-\d+'
    device.sendCmdRegexp(cmd, device.promptUboot, timeout=90)
    time.sleep(1)
    device.sendCmdRegexp('savee', 'OK', timeout=90)
    time.sleep(1)
    device.sendCmdRegexp('reset', KapokConst.ONIE_DISCOVERY_PROMPT, timeout=300)
    device.executeCommand('onie-discovery-stop', device.promptOnie, timeout=300)
    time.sleep(1)
    output = device.executeCommand('ifconfig -a', device.promptOnie, timeout=300)
    for line in output.splitlines():
        res = re.search(p1, line)
        if res:
            pass_count += 1
    if pass_count == 128:
        log.success('Check onie fpp num is %d'%pass_count)
    else:
        raise Exception('Failed check onie fpp number is %d'%pass_count)

@logThis
def check_default_vlan(cmd, pattern):
    pass_count = 0
    p1 = r'Total l2vni count: (\d+)'
    output = device.executeCommand(cmd, device.promptOnie, timeout=300)
    for line in output.splitlines():
        res = re.search(p1, line)
        if res:
            getValue = res.group(1)
            if getValue == pattern:
                pass_count += 1
                log.success('Total l2vni count is %s'%getValue)
                break
    if pass_count == 0:
        raise Exception('Failed run check_default_vlan')

@logThis
def bootup_into_onie_bootcmd_mode():
    device.sendCmdRegexp('reboot', KapokConst.ONIE_DISCOVERY_PROMPT, timeout=300)
    device.executeCommand('onie-discovery-stop', device.promptOnie, timeout=300)

@logThis
def check_knet_l2_information(cmd, pattern):
    pass_count = 0
    p1 = r'Total l2_entry count: (\d+)'
    output = device.executeCommand(cmd, device.promptOnie, timeout=300)
    for line in output.splitlines():
        res = re.search(p1, line)
        if res:
            getValue = res.group(1)
            if getValue == pattern:
                pass_count += 1
                log.success('Total l2_entry count is %s' % getValue)
                break
    if pass_count == 0:
        raise Exception('Failed run check_knet_l2_information')


@logThis
def check_qsfp_tool_test(cmd):
    vendor_count = 0
    pn_count = 0
    sn_count = 0
    p1 = r'Port (\d+):'
    p2 = r'Vendor: (\w+)'
    p3 = r'Part Number: (\w+)'
    p4 = r'Serial Number: (\w+)'
    output = device.executeCommand(cmd, device.promptOnie, timeout=300)
    for line in output.splitlines():
        res1 = re.search(p1, line)
        res2 = re.search(p2, line)
        res3 = re.search(p3, line)
        res4 = re.search(p4, line)
        if res2:
            portVendor = res2.group(1)
            if portVendor == 'AWS':
                vendor_count += 1
        elif res3:
            portPN = res3.group(1)
            if portPN == 'F0OZZGIGA030A':
                pn_count += 1
        elif res4:
            sn_count += 1
    log.info('#########1. vendor [AWS] number is %d'%vendor_count)
    log.info('#########2. PN [F0OZZGIGA030A] number is %d'%pn_count)
    log.info('#########3. SN number is %d'%sn_count)
    if (vendor_count != 32) or (pn_count != 32) or (sn_count != 32):
        raise Exception('Failed run check_qsfp_tool_test')

@logThis
def integrator_mode_config_test(tool, option, showCmd, portEnable):
    load_user_mode_tianhe('./' + tool, option)
    time.sleep(10)
    show_port_status_test(showCmd)
    time.sleep(1)
    port_enable_all_test(portEnable)
    time.sleep(10)
    show_port_status_test(showCmd)
    time.sleep(1)
    device.sendCmdRegexp('exit', device.promptOnie, timeout=60)

@logThis
def get_dhcp_ip():
    dhcpTool = 'udhcpc'
    device.executeCommand(dhcpTool, device.promptDiagOS, timeout=100)

@logThis
def update_diagos_and_onie_test():
    #1. check diag and onie version
    onie_version = CommonLib.get_swinfo_dict("ONIE_Installer").get("newVersion", "NotFound")
    diag_version = CommonLib.get_swinfo_dict("DIAGOS").get("newVersion", "NotFound")
    cmd = 'get_versions'
    p1 = r'DIAGOS\s+(\d+)'
    p2 = r'ONIE\s+([.\d]+)'
    output = run_command(cmd, prompt=device.promptDiagOS, timeout=30)
    for line in output.splitlines():
        line = line.strip()
        diagres = re.search(p1, line)
        onieres = re.search(p2, line)
        if onieres:
            getOnieVer = onieres.group(1)
            if getOnieVer == onie_version:
                log.info('Get the onie version [%s] is new, don\'t need to update!'%getOnieVer)
            else:
                log.info('Get the onie version [%s] is old, need to update to [%s]!'%(getOnieVer, onie_version))
                #2. do onie update
                KapokCommonLib.bootIntoOnieRescueMode()
                onieSelfUpdate('new')
                verifyOnieAndCPLDVersion('new')
        elif diagres:
            getDiagver = diagres.group(1)
            if getDiagver == diag_version:
                log.info('Get the diag version [%s] is new, don\'t need to update!' % getDiagver)
            else:
                log.info('Get the diag version [%s] is old, need to update to [%s]!' % (getDiagver, diag_version))
                #2. do diag update
                KapokCommonLib.bootIntoOnieRescueMode()
                fhv2DiagdownloadImagesAndRecoveryDiagOS()




