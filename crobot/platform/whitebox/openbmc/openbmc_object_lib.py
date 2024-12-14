import re
from inspect import getframeinfo, stack
import time
import yaml
import Logger as log
import CommonLib
import random
import Const
import Const
import YamlParse
import pexpect
import getpass
import os
import traceback
import parser_openbmc_lib
import json
from openbmc_variable import *
from datetime import datetime, timedelta
from dataStructure import nestedDict, parser
from errorsModule import noSuchClass, testFailed
from SwImage import SwImage
from Server import Server
import sys
import getpass
import WhiteboxLibAdapter
import whitebox_lib
from whitebox_lib import *
from WhiteboxDevice import WhiteboxSessionDevice, WhiteboxDevice
from subprocess import Popen, PIPE
import subprocess
# try:
#     import DeviceMgr
# except Exception as err:
#     log.cprint(str(err))

#deviceObj = DeviceMgr.getDevice()

# Cline local command: execute_local_cmd
# ssh to DUT command: ssh_command
# ssh_command_run_ipmi_set_cmd : ssh send ipmi command. (ssh os, send remote ipmi command)
# run_ipmi_set_cmd : send ipmi command remotely or ssh send command. (ssh os or openbmc)


def execute_local_cmd(cmd, timeout=60):
    log.debug('\r\nexecute_local_cmd cmd[%s]' %cmd)
    output = ''
    errs = ''
    proc = Popen(cmd, stdout = PIPE, stderr = PIPE, shell = True, encoding='latin-1')
    try:
        # wait for process to complete
        output, errs = proc.communicate(timeout=timeout)
        log.debug(output)
    except Exception as err:
        # clean up if error occurs
        proc.kill()
        log.debug(output)
        raise RuntimeError(str(err))
    # TODO: workaround for openbmc ipmi command known issue to avoid command script stop.
    exp_str = 'Get SDR 0092 command failed: Invalid data field in request\n'
    if errs.strip(exp_str) == '':
        log.debug('\r\nSuccessfully execute_local_cmd cmd: [%s]' %cmd)
        return output
    else:
        log.debug('\r\nFail to execute_local_cmd cmd: [%s]' % cmd)
        raise RuntimeError(str(errs))


def ssh_command(username, hostip, password, command, title_p=False, end=False):
    key_password = "Password" if title_p else "password"
    ssh_newkey = 'Are you sure you want to continue connecting'
    log.info(command)
    child = pexpect.spawn('ssh -l %s %s %s' % (username, hostip, command))
    i = child.expect([pexpect.TIMEOUT, ssh_newkey, '%s: ' % key_password])
    if i == 0:  # Timeout
        print('ERROR_1!')
        print('SSH could not login. Here is what SSH said:')
        # print(child.before, child.after)
        return None
    if i == 1:  # SSH does not have the public key. Just accept it.
        child.sendline('yes')
        child.sendline('\r')
        child.expect('%s: ' % key_password)
        i = child.expect([pexpect.TIMEOUT, '%s: ' % key_password])
        if i == 0:
            # Timeout
            print('ERROR_2!')
            print('SSH could not login. Here is what SSH said:')
            #print(child.before, child.after)
            return None
    child.sendline(password)
    # log.debug(str(child))
    if end:
        child.expect(pexpect.EOF, timeout=180)
        output = child.before.strip().decode('utf-8')
        log.info(output)
        return output
    else:
        return child


def ssh_command_search_pattern(patterns, username, hostip, password, command, title_p=False):
    if isinstance(patterns, list) or isinstance(patterns, tuple):
        pattern_list = patterns
    else:
        pattern_list = [patterns]
    output = ssh_command(username, hostip, password, command, title_p, end=True)
    for p in pattern_list:
        r = re.compile(p)
        result = r.search(output)
        if result:
            log.info('detected pattern: ' + p)
        else:
            log.error('failed to detect pattern: ' + p)
            raise AssertionError('failed to detect pattern:%s' % p)


def get_deviceinfo_from_config(device, expect):
    """
    :param expect: managementIProot|UserNameroot|Password|bmcIP|bmcPassword|bmcUserName
    """
    deviceInfo = YamlParse.getDeviceInfo()
    deviceDict = deviceInfo[device]
    output = deviceDict.get(expect)
    log.info(output)
    return output


def get_ssh_info(device, type='os'):
    deviceInfo = YamlParse.getDeviceInfo()
    deviceDict = deviceInfo[device]
    # deviceType = deviceDict['deviceType']
    # device_obj = WhiteboxSessionDevice(deviceDict)
    if type == 'os':
        username = deviceDict['rootUserName']
        ip = deviceDict['managementIP']
        password = deviceDict['rootPassword']
    else:
        username = deviceDict['bmcUserName']
        ip = deviceDict['bmcIP']
        password = deviceDict['bmcPassword']
    return username, ip, password


def execute_commands_ssh(device, commands, username, hostip, password):
    deviceInfo = YamlParse.getDeviceInfo()
    deviceDict = deviceInfo[device]
    # deviceType = deviceDict['deviceType']
    device_obj = WhiteboxSessionDevice(deviceDict)
    device_obj.connect(username, hostip, password=password)
    if isinstance(commands, list):
        cmds = commands
    else:
        cmds = [commands]
    output = []
    for cmd in cmds:
        o = device_obj.executeCmd(cmd)
        output.append(o)
    return output


def shell_command_ssh(device, cmd, username=None, hostip=None, password=None):
    deviceInfo = YamlParse.getDeviceInfo()
    deviceDict = deviceInfo[device]
    if username is None and hostip is None:
        username = deviceDict['rootUserName']
        hostip = deviceDict['managementIP']
        password = deviceDict['rootPassword']
    child = whitebox_lib.ssh_command(username, hostip, password, cmd)
    child.expect(pexpect.EOF, timeout=30)
    output = child.before.strip().decode('utf-8')
    log.info(output)
    return output

def run_ipmi_cmd(bmcusername=None, bmcip=None, bmcpassword=None, cmd=None, remote=False):
    log.debug("Entering run_ipmi_cmd with args : %s" % (str(locals())))
    if remote:
        cmd1 = 'ipmitool -I lanplus -H %s -C 17 -U %s -P %s %s' % (bmcip, bmcusername, bmcpassword, cmd)
        output = execute_local_cmd(cmd1)
        log.info(output)
        test_name = 'run_ipmi_cmd'
    else:
        cmd1 = 'ipmitool ' + cmd
        output = ssh_command(bmcusername, bmcip, bmcpassword, cmd1, end=True)
        log.info(output)
        test_name = 'ssh_command_run_ipmi_cmd'
    parsed_output = parser_openbmc_lib.parse_oem_rsp_code(output)
    error_msg = r'.*No such file or directory'
    match_error = re.search(error_msg, output)
    #time.sleep(1)
    if not parsed_output and match_error is None:
        log.success("Successfully %s, execute \'%s\'" % (test_name, cmd1))
        return output
    else:
        #        log.fail("%s"%(match_error.group(0)))
        #        raise testFailed("Failed %s"%(test_name))
        if parsed_output["code"]:
            log.fail("Command error: rsp=\'%s\', \'%s\'\n" % (parsed_output["code"], parsed_output["message"]))
        elif "invalid" in parsed_output:
            log.fail("Invalid command: %s" % (parsed_output["invalid"]))
        elif match_error:
            log.fail("%s" % (match_error.group(0)))
        else:
            log.fail("Unknown error")
        raise testFailed("Failed %s" % (test_name))


def wait_pattern(device, patterns, timeout=300):
    log.debug('Entering procedure wait_pattern with args : %s\n' % (str(locals())))
    err_count = 0
    deviceObj = WhiteboxDevice.getDeviceObject(device)
    if isinstance(patterns, list) or isinstance(patterns, tuple):
        pattern_list = patterns
    else:
        pattern_list = [patterns]
    deviceObj.flush()
    deviceObj.setConnectionTimeout(timeout)
    for p in pattern_list:
        output = deviceObj.read_until_regexp(p)
        log.info("detected pattern: " + p)
        deviceObj.flush()


def wait_prompt(device, prompt_type='bmc', timeout=300):
    log.debug('Entering procedure wait_prompt with args : %s\n' % (str(locals())))
    # deviceObj = WhiteboxDevice.getDeviceObject(device)
    REGEX = BOOT_REGEX if prompt_type == 'bmc' else OS_BOOT_REGEX
    # if prompt_type == 'os':
    #     prompt = Const.BOOT_MODE_DIAGOS
    # else:
    #     prompt = Const.BOOT_MODE_OPENBMC
    # deviceObj.getPrompt(prompt, timeout)
    wait_pattern(device, REGEX, timeout)


def parse_keywords(regex, output):
    log.debug('Entering procedure parse_simple_keyword with args : %s\n' % (str(locals())))
    match = re.search(regex, output)
    if match:
        log.fail("Found: %s" % (match.group(0)))
        return "fail"
    else:
        log.success("Not found keyword: %s" % (regex))
        return "success"


def call_openbmc_class(device):
    """Call the class Openbmc info"""
    return OpenbmcInfo(device)


def call_fru_class(device):
    """Call the class fru"""
    return FRUIpmi(device)


def call_sel_class(device):
    """Call the class sel"""
    return SELIpmi(device)


def call_sensor_class(device):
    """Call the class Sensor"""
    return SensorIpmi(device)


def call_firmware_class(device):
    """Call the class Firmware"""
    return Firmware(device)


def call_variables(obj_name, var_name):
    if hasattr(obj_name, var_name):
        return getattr(obj_name, var_name)
    else:
        return None


class OpenbmcInfo(object):
    def __init__(self, device_info):
        if isinstance(device_info, str):
            self.device = device_info
            self.bmcusername, self.bmcip, self.bmcpasswd = get_ssh_info(device_info, 'bmc')
            self.os_username, self.os_ip, self.os_passwd = get_ssh_info(device_info, 'os')
        else:
            if len(device_info) != 7:
                raise RuntimeError("The device info error")
            self.device, self.bmcip, self.bmcusername, self.bmcpasswd,\
                self.os_ip, self.os_username, self.os_passwd = device_info

    def get_mc_info(self):
        commands = []
        cmd = 'ipmitool {}'
        commands.append(cmd.format('mc info'))
        commands.append(cmd.format('lan print 1'))
        commands.append(cmd.format('lan print 2'))
        commands.append(cmd.format('sensor list'))
        execute_commands_ssh(self.device, commands, self.bmcusername, self.bmcip, self.bmcpasswd)

    def check_openbmc_info(self, info_type, exp_info=None, get_status=False, rm=True):
        """
        check status : 'bmc_version', 'product_id', 'power_status', 'policy_status'
        """
        log.debug("Entering check_openbmc_info with args : %s" % (str(locals())))
        command = openbmc_info_map[info_type][0]
        p = openbmc_info_map[info_type][1]
        output = run_ipmi_cmd(self.bmcusername, self.bmcip, self.bmcpasswd, command, rm)
        match = re.search(p, output)
        if match:
            checked_info = match.group(1).strip()
            if exp_info is None and get_status:
                log.info("Successfully get the openbmc_info %s: %s" % (info_type, checked_info))
                return checked_info
            if checked_info == exp_info:
                log.info("Successfully check_openbmc_info %s: %s" % (info_type, checked_info))
                return checked_info
            else:
                log.error("openbmc_info %s mismatch: %s, %s" % (info_type, checked_info, exp_info))
                raise Exception("openbmc_info %s mismatch: %s, %s" % (info_type, checked_info, exp_info))
        else:
            log.error("Fail to parse check_openbmc_info %s" % info_type)
            raise Exception("Fail to parse check_openbmc_info %s" % info_type)

    def check_openbmc_info_raw(self, command, exp_info, rm=True):
        output_raw = self.ipmi_raw_cmd(command, rm)
        exp_raw = self._raw_update(exp_info)
        for i in range(len(output_raw)):
            assert output_raw[i] == exp_raw[i], ("The raw command output is mismatch. output: %s, expect: %s"
                                                 % (output_raw, exp_raw))

    def ipmi_power_control(self, command, rm=True):
        log.debug("Entering send the %s command: %s" % (command, str(locals())))
        output = self._ipmi_cmd('chassis', command, rm)
        if command in chassis_policy_cmd_list:
            match = re.search(policy_cmd_output, output)
            if match:
                log.success("IPMI command “Set Power Restore Policy” executed successfully")
            else:
                log.fail("Failed! IPMI command “Set Power Restore Policy” not executed :{output}")
                raise Exception("Failed! IPMI command “Set Power Restore Policy” not executed")

    def ipmi_dev_global_cmd(self, command, rm=True):
        log.debug("Entering send the %s command: %s" % (command, str(locals())))
        self._ipmi_cmd('device_global', command, rm)

    def ipmi_oem_cmd(self, command, rm=True):
        log.debug("Entering send the %s command: %s" % (command, str(locals())))
        output_str = self._ipmi_cmd('oem', command, rm)
        output_raw = self._raw_update(output_str)
        return output_raw

    def ipmi_raw_cmd(self, command, rm=True):
        log.debug("Entering send the raw command: %s" % str(locals()))
        output_str = self._ipmi_cmd('raw', command, rm)
        output_raw = self._raw_update(output_str)
        return output_raw

    def wait_for_bmc_dev_available(self):
        """wait 2 mins for the bmc device available."""
        log.debug('Entering procedure wait_for_bmc_dev_available with args : %s\n' % (str(locals())))
        cmd = device_global_cmd_list['get_device_id']
        for i in range(12):
            o = self.ipmi_raw_cmd(cmd)
            in_process = (o[2] >> 7) & 0b1
            if not in_process:
                log.info("openbmc Device Available")
                return
            log.info("openbmc Device not Available. Wait for 10s retry.")
            time.sleep(10)
        raise testFailed("Openbmc device not available in 2 minutes.")

    def _ipmi_cmd(self, cmd_type, command, rm=True):
        cmd_type_list = {'chassis': chassis_cmd_list,
                         'device_global': device_global_cmd_list,
                         'oem': oem_cmd_list}
        log.debug("Entering %s ipmi cmd: %s" % (cmd_type, str(locals())))
        if cmd_type == 'raw':
            output = run_ipmi_cmd(self.bmcusername, self.bmcip, self.bmcpasswd, command, remote=rm)
            return output
        cmd_list = cmd_type_list[cmd_type]
        if command not in cmd_list.keys():
            raise testFailed("The command is invalid.")
        output = run_ipmi_cmd(self.bmcusername, self.bmcip, self.bmcpasswd, cmd_list[command], remote=rm)
        return output

    def _raw_update(self, output_str):
        output = [int(x, base=16) for x in output_str.split()]
        return output


class SensorIpmi(OpenbmcInfo):

    def __init__(self, device):
        super().__init__(device)
        self._update()

    def return_variables(self, var_name):
        return getattr(self, var_name)

    def _update(self):
        self.sensor_list = []
        self.temp_sensor = []
        self.current_sensor = []
        self.voltage_sensor = []
        self.fan_sensor = []
        self.power_sensor = []
        self.other_sensor = []
        self.non_discrete_sensor = []
        self.fan_pwm_sensor = []
        self.sensor_type_map = {'degrees C': self.temp_sensor,
                                'Amps': self.current_sensor,
                                'RPM': self.fan_sensor,
                                'Watts': self.power_sensor,
                                'Volts': self.voltage_sensor
                                }
        cmd = 'sensor list'
        output = run_ipmi_cmd(self.bmcusername, self.bmcip, self.bmcpasswd, cmd, remote=True)
        for line in output.split('\n'):
            if not line:
                continue
            s1 = re.match(sensor_disc_check_p, line)
            s2 = re.match(sensor_discrete, line) if s1['type'] == 'discrete' else re.match(sensor_non_disc, line)
            self.sensor_list.append(s2.groupdict())
        self.sdr_list = []
        # TODO: the number of sensors is mismatch with the sdr info.
        # cmd = 'raw 0x04 0x20 0x00'
        # sensor_info_raw = run_ipmi_cmd(self.bmcusername, self.bmcip, self.bmcpasswd, cmd, True)
        # sensor_num = int(sensor_info_raw.split()[0], base=16)
        cmd1 = 'sdr elist'
        sdr_elist_output = run_ipmi_cmd(self.bmcusername, self.bmcip, self.bmcpasswd, cmd1, True)
        for line in sdr_elist_output.split('\n'):
            if not line:
                continue
            o = re.match(sdr_elist_p, line)
            self.sdr_list.append(o.groupdict())
        for sen in self.sensor_list:
            for sd in self.sdr_list:
                if sd['sensor_name'] == sen['sensor_name']:
                    sen['sensor_id'] = sd['sensor_id']
                    break
            if sen['type'] in self.sensor_type_map.keys():
                self.sensor_type_map[sen['type']].append(sen)
                self.non_discrete_sensor.append(sen)
            else:
                pwm_s = re.search('Fan', sen['sensor_name'])
                if pwm_s:
                    self.fan_pwm_sensor.append(sen)
                    self.non_discrete_sensor.append(sen)
                else:
                    self.other_sensor.append(sen)

    def refresh_sensor(self):
        self._update()

    def verify_normal_status(self, sen_type=None):
        abnormal_sensor = []
        check_sensor_list = self.sensor_type_map[sensor_type_info[sen_type]] if sen_type in sensor_type_info.keys() \
            else self.non_discrete_sensor
        abnormal_sensor.extend(sensor for sensor in check_sensor_list if sensor['status'] not in 'ok|na')
        if abnormal_sensor:
            for ab in abnormal_sensor:
                log.info("Sensor %s status is %s." % (ab['sensor_name'], ab['status']))
            raise RuntimeError("verify sensor status fail.")
        else:
            log.info("The sensor status is normal.")

    def thresholds_cmd(self, sensor, setting=False,
                       lnc=None, lcr=None, lnr=None, unc=None, ucr=None, unr=None):
        """
        Get threshold return:
        byte1: bit mask for 6 threshold values. (bit mask: [7:6]: reserved. [5~0]: unr, ucr, unc, lnr, lcr, lnc)
        byte2: lower non-critical
        byte3: lower critical
        byte4: lower non-recoverable
        byte5: upper non-critical
        byte6: upper critical
        byte7: upper non-recoverable
        """
        sensor_idx = int(sensor['sensor_id'], base=16)
        raw_cmd_get = 'raw 0x04 0x27 ' + str(sensor_idx)
        output_raw_data = self.ipmi_raw_cmd(raw_cmd_get)
        if setting:
            log.info("Setting the sensor thresholds value.")
            req_date = [sensor_idx]
            req_date.extend(output_raw_data)
            if unr is not None and (req_date[1] >> 5 & 0b1):
                if not isinstance(unr, int):
                    unr = int(unr, base=16)
                req_date[7] = unr & 0xff
            if ucr is not None and (req_date[1] >> 4 & 0b1):
                if not isinstance(ucr, int):
                    ucr = int(ucr, base=16)
                req_date[6] = ucr & 0xff
            if unc is not None and (req_date[1] >> 3 & 0b1):
                if not isinstance(unc, int):
                    unc = int(unc, base=16)
                req_date[5] = unc & 0xff
            if lnr is not None and (req_date[1] >> 2 & 0b1):
                if not isinstance(lnr, int):
                    lnr = int(lnr, base=16)
                req_date[4] = lnr & 0xff
            if lcr is not None and (req_date[1] >> 1 & 0b1):
                if not isinstance(lcr, int):
                    lcr = int(lcr, base=16)
                req_date[3] = lcr & 0xff
            if lnc is not None and (req_date[1] & 0b1):
                if not isinstance(lnc, int):
                    lnc = int(lnc, base=16)
                req_date[2] = lnc & 0xff
            raw_req_date = ' '.join(["0x%02x" % (b & 0xff) for b in req_date])
            raw_cmd_set = 'raw 0x04 0x26 ' + raw_req_date
            self.ipmi_raw_cmd(raw_cmd_set)
            time.sleep(10)
            setting_o_raw = self.ipmi_raw_cmd(raw_cmd_get)
            log.info("After setting the sensor thresholds, %s" % setting_o_raw)
            return setting_o_raw
        else:
            log.info("The sensor %s thresholds is %s" % (sensor_idx, output_raw_data))
            return output_raw_data


class SELIpmi(OpenbmcInfo):

    def __init__(self, device):
        super().__init__(device)
        self.sel_list = []
        self.sel_elist = []
        self._update()

    def _update(self):
        pass

    # TODO: no sel log added, when doing openbmc sel clear action.
    def _check_sel_sum(self):
        sel_info_cmd = 'raw 0x0a 0x40'
        sel_sum_pattern = r'^\s(\w\w\s\w\w\s\w\w)\s.+'
        zero_sel = '51 00 00'
        sel_info_o = run_ipmi_cmd(self.bmcusername, self.bmcip, self.bmcpasswd, sel_info_cmd, True)
        match = re.search(sel_sum_pattern, sel_info_o)
        if match.group(1) == zero_sel:
            log.info("Zero sel log.")
            return True
        else:
            return False

    def sel_list_get(self):
        self.sel_list = []
        if self._check_sel_sum():
            return
        cmd = 'sel list'
        output = run_ipmi_cmd(self.bmcusername, self.bmcip, self.bmcpasswd, cmd, remote=True)
        for line in output.split('\n'):
            if not line:
                continue
            s = re.match(sel_list_pattern, line.lstrip())
            self.sel_list.append(s.groupdict())

    def sel_elist_get(self):
        self.sel_list_get()
        self.sel_elist = []
        if self._check_sel_sum():
            return
        cmd = 'sel elist'
        output = run_ipmi_cmd(self.bmcusername, self.bmcip, self.bmcpasswd, cmd, remote=True)
        for line in output.split('\n'):
            if not line:
                continue
            s = re.match(sel_elist_pattern, line.lstrip())
            self.sel_elist.append(s.groupdict())

    def sel_clear(self):
        log.debug('Entering procedure run_ipmi_cmd_sel_clear with args : %s\n' % (str(locals())))
        err_count = 0
        cmd = 'sel clear'
        cmd1 = 'raw 0x0a 0x40'
        error_msg = r'(.*command failed.+error)'
        successful_msg_1 = 'Clearing SEL'
        # spec version: 0x51, number of logs: 0x00 0x00
        successful_msg_2 = '51 00 00'
        sel_sum_pattern = r'^\s(\w\w\s\w\w\s\w\w)\s.+'
        output = run_ipmi_cmd(self.bmcusername, self.bmcip, self.bmcpasswd, cmd, True)
        time.sleep(10)
        output1 = run_ipmi_cmd(self.bmcusername, self.bmcip, self.bmcpasswd, cmd1, True)
        match_err = re.search(error_msg, output)
        if match_err:
            log.fail("Found error: %s" % (match_err.group(1)))
            err_count += 1
        match_1 = re.search(successful_msg_1, output)
        match_2 = re.search(sel_sum_pattern, output1)
        if match_1:
            log.info("run_ipmi_cmd_sel_clear")
        else:
            log.error("mismatch %s" % successful_msg_1)
            err_count += 1
        if match_2.group(1) == successful_msg_2:
            log.info("run_ipmi_cmd_sel_clear")
        else:
            log.error("mismatch %s" % output1)
            err_count += 1
        if err_count:
            raise testFailed("run_ipmi_cmd_sel_clear")

    def check_sel_list_unexpect_event(self, messages_list):
        log.debug('Entering procedure check_sel_list_unexpect_event with args : %s\n' % (str(locals())))
        sel_info_cmd = 'raw 0x0a 0x40'
        sel_sum_pattern = r'^\s(\w\w\s\w\w\s\w\w)\s.+'
        zero_sel = '51 00 00'
        sel_info_o = run_ipmi_cmd(self.bmcusername, self.bmcip, self.bmcpasswd, sel_info_cmd, True)
        match = re.search(sel_sum_pattern, sel_info_o)
        if match.group(1) == zero_sel:
            log.info("No sel log added.")
            return
        err_count = 0
        cmd = 'sel list'
        output = run_ipmi_cmd(self.bmcusername, self.bmcip, self.bmcpasswd, cmd, remote=True)
        log.info(output)
        messages_list = messages_list.split(",")
        for msg in messages_list:
            if parse_keywords(msg, output) == "fail":
                err_count += 1
        #check_full_fan_speed(bmcip, bmcusername, bmcpassword)
        if err_count == 0:
            log.success("Successfully check_sel_list_unexpect_event")
        else:
            log.fail("check sel list unexpect event fail")
            raise testFailed("check_sel_list_unexpect_event fail")


class FRUIpmi(OpenbmcInfo):

    def __init__(self, device):
        super().__init__(device)
        cmd = 'fru list'
        output = run_ipmi_cmd(self.bmcusername, self.bmcip, self.bmcpasswd, cmd, remote=True)
        self._update(output)

    def _update(self, sensor_list):
        pass


class Firmware(OpenbmcInfo):

    def __init__(self, device):
        super().__init__(device)
        server_info = YamlParse.getDeviceInfo()
        server_dict = deviceInfo['PC']
        self.image_s_ip = server_dict.get('managementIP')
        self.image_s_user = server_dict.get('username')
        self.image_s_passwd = server_dict.get('password')
        self.update_path = ''
        self.activation_table = {'bmc': self._openbmc_update,
                                 'bios': self._bios_spi_flash,
                                 'cpld': self._cpld_JTAG,
                                 'retimer': self._retimer_update,
                                 'psu': self._PSU_I2C_update}
        imageInfo = YamlParse.getSwImageInfo()
        if device[-5:] == '_peer':
            self.dev_name_a = device.rstrip('_peer') + '_A_'
            self.dev_name_b = device.rstrip('_peer') + '_B_'
            self.dev_name = self.dev_name_b
        else:
            self.dev_name_a = device + '_A_'
            self.dev_name_b = device + '_B_'
            self.dev_name = self.dev_name_a
        self.firmware_info_bmc_a = imageInfo[self.dev_name_a + 'BMC']
        self.firmware_info_bmc_b = imageInfo[self.dev_name_b + 'BMC']
        self.firmware_info_bmc = imageInfo[self.dev_name + 'BMC']
        self.firmware_info_bios_b = imageInfo[self.dev_name_b + 'BIOS']
        self.firmware_info_bios = imageInfo[self.dev_name + 'BIOS']
        self.firmware_info_cpld_a = imageInfo[self.dev_name_a + 'CPLD']
        self.firmware_info_cpld_b = imageInfo[self.dev_name_b + 'CPLD']
        self.firmware_info_cpld = imageInfo[self.dev_name + 'CPLD']
        self.firmware_info_psu = imageInfo[self.dev_name + 'PSU']
        self.firmware_info_Retimer = imageInfo[self.dev_name + 'Retimer']
        bmc_image = [self.firmware_info_bmc['hostImageDir'],
                     self.firmware_info_bmc['oldImage'],
                     self.firmware_info_bmc['newImage']]
        bios_image = [self.firmware_info_bios['hostImageDir'],
                      self.firmware_info_bios['oldImage'],
                      self.firmware_info_bios['newImage']]
        cpld_image = [self.firmware_info_cpld['hostImageDir'],
                      self.firmware_info_cpld['oldImage'],
                      self.firmware_info_cpld['newImage']]
        psu_image = [self.firmware_info_psu['hostImageDir'],
                     self.firmware_info_psu['oldImage'],
                     self.firmware_info_psu['newImage']]
        retimer_image = [self.firmware_info_Retimer['hostImageDir'],
                         self.firmware_info_Retimer['oldImage'],
                         self.firmware_info_Retimer['newImage']]
        self.image_list = {'bmc': bmc_image, 'bios': bios_image, 'cpld': cpld_image,
                           'retimer': retimer_image, 'psu': psu_image}

    def check_fw_version(self,
                         bmc_version='current',
                         bios_version='current',
                         cpld_version='current',
                         psu_version='current'):
        # bmc_version/bios_version option is 'old' or 'current'.
        # TODO: PSU and retimer version check.
        bmc_ver = 'oldVersion' if bmc_version == 'old' else 'newVersion'
        bios_ver = 'oldVersion' if bios_version == 'old' else 'newVersion'
        cpld_ver = 'oldVersion' if cpld_version == 'old' else 'newVersion'
        psu_ver = 'oldVersion' if psu_version == 'old' else 'newVersion'
        bmc_cmd = 'mc info'
        bmc_p = r'Firmware Revision\s+:\s+(\S+)'
        bios_cmd = 'dmidecode -s bios-version'
        # TODO: check cpld version via i2c command.
        cpld_rel_ver_cmd = 'i2cget -f -y 1 0x61 0x02'
        cpld_test_ver_cmd = 'i2cget -f -y 1 0x61 0x03'
        psu_ver_cmd = 'i2cget -f -y 10 0x58 0xd9 i 2'
        bmc_ver_chk_output = run_ipmi_cmd(self.bmcusername, self.bmcip, self.bmcpasswd, bmc_cmd, True)
        bios_ver_chk_output = ssh_command(self.os_username, self.os_ip, self.os_passwd, bios_cmd, end=True)
        cpld_rel_ver = ssh_command(self.bmcusername, self.bmcip, self.bmcpasswd, cpld_rel_ver_cmd, end=True)
        cpld_test_ver = ssh_command(self.bmcusername, self.bmcip, self.bmcpasswd, cpld_test_ver_cmd, end=True)
        psu_ver_check_ouput = ssh_command(self.bmcusername, self.bmcip, self.bmcpasswd, psu_ver_cmd, end=True)
        p1 = re.search(bmc_p, bmc_ver_chk_output)
        bmc_current = p1.group(1).strip()
        bios_current = bios_ver_chk_output
        cpld_current = [cpld_rel_ver, cpld_test_ver]
        psu_current = psu_ver_check_ouput
        if bmc_current == self.firmware_info_bmc[bmc_ver] and\
                bios_current == self.firmware_info_bios[bios_ver] and\
                cpld_current == self.firmware_info_cpld[cpld_ver] and\
                psu_current == self.firmware_info_psu[psu_ver]:
            return True
        else:
            log.info("Firmware version mismatch. Current: BMC:%s, BIOS:%s, CPLD:%s, PSU:%s "
                     "Expect: BMC:%s, BIOS:%s, CPLD:%s, PSU:%s"
                     % (bmc_current, bios_current, cpld_current, psu_current,
                        self.firmware_info_bmc[bmc_ver],
                        self.firmware_info_bios[bios_ver],
                        self.firmware_info_cpld[cpld_ver],
                        self.firmware_info_psu[psu_ver]))
            raise testFailed("Firmware version check failed")

    def firmware_flash(self, fw_type, upgrade=True, backup=False):
        """ upgrade: True/False, upgrade or downgrade the firmware."""
        # TODO: BIOS ,CPLD and Retimer firmware program
        self.update_path = '/tmp/'
        if upgrade:
            firmware_image = self.image_list[fw_type][0] + '/' + self.image_list[fw_type][2]
            image = self.image_list[fw_type][2]
        else:
            firmware_image = self.image_list[fw_type][0] + '/' + self.image_list[fw_type][1]
            image = self.image_list[fw_type][1]
        self._download_image_files(firmware_image)
        self.activation_table[fw_type](image, backup)

    def _download_image_files(self, image):
        key_password = "password"
        ssh_newkey = 'Are you sure you want to continue connecting'
        complete_tag = '100%'
        cmd = 'scp %s@%s:%s %s@%s:%s' % (self.image_s_user, self.image_s_ip, image,
                                         self.bmcusername, self.bmcip, self.update_path)
        child = pexpect.spawn(cmd)
        for passwd in [self.bmcpasswd, self.image_s_passwd]:
            i = child.expect([pexpect.TIMEOUT, ssh_newkey, '%s: ' % key_password])
            if i == 0:  # Timeout
                print('ERROR_1!')
                print('SSH could not login. Here is what SSH said:')
                # print(child.before, child.after)
                return None
            if i == 1:  # SSH does not have the public key. Just accept it.
                child.sendline('yes')
                child.sendline('\r')
                child.expect('%s: ' % key_password)
                i = child.expect([pexpect.TIMEOUT, '%s: ' % key_password])
                if i == 0:
                    # Timeout
                    print('ERROR_2!')
                    print('SSH could not login. Here is what SSH said:')
                    # print(child.before, child.after)
                    return None
            child.sendline(passwd)
        #        log.debug(str(child))
        c = child.expect([complete_tag, pexpect.TIMEOUT])
        if c:
            log.fail("download failed")
            return None
        child.expect(pexpect.EOF, timeout=60)
        return child

    def _openbmc_update(self, image, backup=False):
        img_name = 'image-bmc1' if backup else 'image-bmc0'
        flash_path = '/run/initramfs/'
        cmd = 'cp %s%s %s%s' % (self.update_path, image, flash_path, img_name)
        ssh_command(self.bmcusername, self.bmcip, self.bmcpasswd, cmd, end=True)
        self._reboot_or_program(flash_bmc=True, backup=backup)

    def _reboot_or_program(self, flash_bmc=False, backup=False):
        if flash_bmc:
            WhiteboxLibAdapter.ConnectDevice(self.device, 'bmc')
            ssh_command(self.bmcusername, self.bmcip, self.bmcpasswd, 'reboot', end=True)
            # wait for the openbmc execute reboot action
            time.sleep(1)
            if backup:
                wait_pattern(self.device, OPENBMC_FLASH_BACKUP_REGEX, timeout=800)
            else:
                wait_pattern(self.device, OPENBMC_FLASH_REGEX, timeout=800)
            wait_pattern(self.device, BOOT_REGEX, timeout=180)
            WhiteboxLibAdapter.DisconnectDevice(self.device, 'bmc')
        else:
            # self.ipmi_power_control('power cycle')
            self.ipmi_power_control('power off')
            time.sleep(10)
            self.ipmi_power_control('power on')
            WhiteboxLibAdapter.ConnectDevice(self.device, 'os', login=False)
            wait_prompt(self.device, 'os', timeout=500)
            WhiteboxLibAdapter.DisconnectDevice(self.device, 'os')
        time.sleep(5)
        self.wait_for_bmc_dev_available()

    def _bios_spi_flash(self, image, backup=False):
        self.ipmi_power_control('power off')
        log.info("Wait for 15 seconds for CPU power off.")
        time.sleep(15)
        self.check_openbmc_info('power_status', 'off')
        default_backup = self.bios_boot(backup=backup)
        bios_flash_command = 'flashcp -v /tmp/%s  /dev/mtd/bios' % image
        ssh_command_search_pattern(BIOS_SPI_FLASH_REGEX,
                                   self.bmcusername,
                                   self.bmcip,
                                   self.bmcpasswd,
                                   bios_flash_command)
        # switch back to bios boot option
        self.bios_boot(backup=default_backup)
        self._reboot_or_program()

    def bios_boot(self, backup):
        check_result = False
        expect_val = 0x00 if backup else 0x01
        value = self.ipmi_oem_cmd('get_bios_boot')
        default_value = True if value[0] == 0x00 else False
        if value[0] == expect_val:
            check_result = True
        else:
            if backup:
                log.info("Switch CPU<->pri BIOS, BMC<->sec BIOS")
                self.ipmi_oem_cmd('set_bios_pri')
            else:
                log.info("Switch BMC<->pri BIOS, CPU<->sec BIOS")
                self.ipmi_oem_cmd('set_bios_sec')
            value = self.ipmi_oem_cmd('get_bios_boot')
            if value[0] == expect_val:
                check_result = True
        if check_result:
            log.info("Switch the bios spi boot.")
        else:
            log.fail("Failed to switch bios boot spi flash!")
            raise RuntimeError
        return default_value

    def _cpld_JTAG(self, image, backup=False):
        cmd1 = 'raw 0x3a 0x24 0x01 0x96 0x00 0x00'
        cmd2 = 'raw 0x3a 0x24 0x01 0x14 0x00 0x00'
        cmd3 = 'cpldprog -p /tmp/%s -R' % image
        run_ipmi_cmd(self.bmcusername, self.bmcip, self.bmcpasswd, cmd1, True)
        time.sleep(0.5)
        run_ipmi_cmd(self.bmcusername, self.bmcip, self.bmcpasswd, cmd2, True)
        # TODO: send cpld program cmd and refresh via ssh will cause the ssh terminal hang.
        # send program cmd via serial port.
        device_inf = WhiteboxLibAdapter.ConnectDevice(self.device, 'bmc', login=True)
        device_inf.device.sendCmd(cmd3, CPLD_JTAG_REGEX[0])
        wait_pattern(self.device, [CPLD_JTAG_REGEX[1], CPLD_JTAG_REGEX[2]], timeout=300)
        wait_pattern(self.device, BOOT_REGEX, timeout=300)
        WhiteboxLibAdapter.DisconnectDevice(self.device, 'bmc')
        # wait for OS boot up.
        WhiteboxLibAdapter.ConnectDevice(self.device, 'os', login=False)
        wait_prompt(self.device, 'os')
        WhiteboxLibAdapter.DisconnectDevice(self.device, 'os')
        self.wait_for_bmc_dev_available()

    def _PSU_I2C_update(self, image, backup=False):
        psu_prog_cmd = 'psu-util.sh -f /tmp/%s' % image
        output = ssh_command(self.bmcusername, self.bmcip, self.bmcpasswd, psu_prog_cmd, end=True)
        p = r'Update completed'
        match = re.search(p, output)
        if match:
            log.info("PSU update complete.")
        else:
            log.fail(output)
            raise RuntimeError

    def _retimer_update(self, image, backup=False):
        cmd1 = 'i2cset -y -f 13 0x71 0x01'
        cmd2 = 'retimer-util eeprom_update_direct 13 0x50 /tmp/retimer-image-name'
        pass

