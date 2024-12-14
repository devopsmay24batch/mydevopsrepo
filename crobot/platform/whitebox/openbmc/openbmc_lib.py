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
from copy import copy
from BIOS_variable import *
from openbmc_variable import *
from datetime import datetime, timedelta
from dataStructure import nestedDict, parser
from errorsModule import noSuchClass, testFailed
from SwImage import SwImage
from Server import Server
from pexpect import pxssh
import sys
import getpass
import WhiteboxLibAdapter
import whitebox_lib
from whitebox_lib import *
from WhiteboxDevice import WhiteboxSessionDevice, WhiteboxDevice
from subprocess import Popen, PIPE
import subprocess
from openbmc_object_lib import *

try:
    import parser_openbmc_lib as parserOpenbmc
    import DeviceMgr
    from Device import Device

except Exception as err:
    log.cprint(str(err))


# deviceObj = DeviceMgr.getDevice()

# Cline local command: execute_local_cmd
# ssh to DUT command: ssh_command
# ssh_command_run_ipmi_set_cmd : ssh send ipmi command. (ssh os, send remote ipmi command)
# run_ipmi_set_cmd : send ipmi command remotely or ssh send command. (ssh os or openbmc)

def watchdog_do_not_log_bit(dev_info, wdg_not_reset=False):
    ipmi_sel = SELIpmi(dev_info)
    ipmi_sel.sel_clear()
    not_log_bit = [0x81, 0x01]
    for value in not_log_bit:
        set_cmd = f'raw 0x06 0x24 {str(value)} 0x00 0x00 0x00 0x32 0x00'  # time set 5 seconds.
        ipmi_sel.ipmi_raw_cmd(set_cmd)
        wdg_status = ipmi_sel.ipmi_raw_cmd(device_global_cmd_list['watchdog_get'])
        assert wdg_status[0] == value
        assert wdg_status[6] == 0x32
        assert wdg_status[7] == 0x00
        if wdg_not_reset:
            time.sleep(1)
            continue
        ipmi_sel.ipmi_dev_global_cmd('watchdog_reset')
        time.sleep(6)
        wdg_status = ipmi_sel.ipmi_raw_cmd(device_global_cmd_list['watchdog_get'])
        assert wdg_status[0] == value
        assert wdg_status[6] == 0x00
        assert wdg_status[7] == 0x00
        ipmi_sel.sel_list_get()
        if value == 0x81:
            log.info("Check sel do_not_log bit set to 1.")
            ipmi_sel.check_sel_list_unexpect_event(error_messages_list)
        else:
            log.info("Check sel do_not_log bit set to 0.")
            assert ipmi_sel.sel_list[-1]['Type'] == 'Timer expired'
        time.sleep(2)


def watchdog_time_use_set(dev_info):
    ipmi_sel = SELIpmi(dev_info)
    time_use_byte = {'BIOS_FRB2': 0x01,
                     'BIOS_POST': 0x02,
                     'OS_LOAD': 0x03,
                     'SMS_OS': 0x04,
                     'OEM': 0x05}
    for time_use, value in time_use_byte.items():
        log.info("Set the watchdog time use: %s" % time_use)
        set_cmd = f'raw 0x06 0x24 {str(value)} 0x00 0x00 0x00 0x32 0x00'
        ipmi_sel.sel_clear()
        ipmi_sel.ipmi_raw_cmd(set_cmd)
        wdg_status = ipmi_sel.ipmi_raw_cmd(device_global_cmd_list['watchdog_get'])
        assert wdg_status[0] == value
        assert wdg_status[6] == 0x32
        assert wdg_status[7] == 0x00
        ipmi_sel.ipmi_dev_global_cmd('watchdog_reset')
        time.sleep(6)
        wdg_status = ipmi_sel.ipmi_raw_cmd(device_global_cmd_list['watchdog_get'])
        assert wdg_status[0] == value
        assert wdg_status[6] == 0x00
        assert wdg_status[7] == 0x00
        ipmi_sel.sel_list_get()
        assert ipmi_sel.sel_list[-1]['Type'] == 'Timer expired'


def watchdog_timeout_action_set(dev_info):
    ipmi_sel = SELIpmi(dev_info)
    timeout_act_byte = {'no_action': 0x00,
                        'hard_reset': 0x01,
                        'power_down': 0x02,
                        'power_cycle': 0x03}
    sel_type = {'no_action': 'Timer expired',
                'hard_reset': 'Hard reset',
                'power_down': 'Power down',
                'power_cycle': 'Power cycle'}
    for timeout_act, value in timeout_act_byte.items():
        log.info("Set the watchdog time use: %s" % timeout_act)
        set_cmd = f'raw 0x06 0x24 0x05 {str(value)} 0x00 0x00 0x32 0x00'
        ipmi_sel.sel_clear()
        ipmi_sel.ipmi_raw_cmd(set_cmd)
        wdg_status = ipmi_sel.ipmi_raw_cmd(device_global_cmd_list['watchdog_get'])
        assert wdg_status[0] == 0x05
        assert wdg_status[1] == value
        assert wdg_status[6] == 0x32
        assert wdg_status[7] == 0x00
        ipmi_sel.ipmi_dev_global_cmd('watchdog_reset')
        time.sleep(6)
        wdg_status = ipmi_sel.ipmi_raw_cmd(device_global_cmd_list['watchdog_get'])
        assert wdg_status[0] == 0x05
        assert wdg_status[1] == value
        assert wdg_status[6] == 0x00
        assert wdg_status[7] == 0x00
        ipmi_sel.sel_list_get()
        assert ipmi_sel.sel_list[-1]['Type'] == sel_type[timeout_act]
        time.sleep(5)
        if timeout_act != 'no_action':
            if timeout_act == 'hard_reset':
                ipmi_sel.check_openbmc_info('power_status', 'on')
            else:
                ipmi_sel.check_openbmc_info('power_status', 'off')
                if timeout_act == 'power_cycle':
                    time.sleep(25)
                    ipmi_sel.check_openbmc_info('power_status', 'on')
                else:
                    time.sleep(25)
                    ipmi_sel.check_openbmc_info('power_status', 'off')
                    ipmi_sel.ipmi_power_control('power on')
            WhiteboxLibAdapter.ConnectDevice(ipmi_sel.device, 'os', login=False)
            wait_prompt(ipmi_sel.device, 'os')
            WhiteboxLibAdapter.DisconnectDevice(ipmi_sel.device, 'os')


def fan_status_monitor(dev_info):
    ipmi_sensor = SensorIpmi(dev_info)
    fsc_status = ipmi_sensor.ipmi_oem_cmd('get_fsc_mode')
    # 01: Manual Mode, 00: Automatic Mode(FSC)
    assert fsc_status[3] == 0x00, "The cooling FSC mode is not active!"
    log.info('Change the cooling management to manual mode.')
    ipmi_sensor.ipmi_oem_cmd('dis_fsc_mode')
    time.sleep(1)
    fsc_status = ipmi_sensor.ipmi_oem_cmd('get_fsc_mode')
    assert fsc_status[3] == 0x01, "The cooling management set to manual mode failed!"
    # fan speed control test
    for tar_pwm in range(100, 40, -10):
        log.info("Set cooling speed pwm %s" % tar_pwm)
        set_cmd = oem_cmd_list['set_fan_pwm'] + ' ' + str(tar_pwm)
        ipmi_sensor.ipmi_raw_cmd(set_cmd)
        time.sleep(15)
        ipmi_sensor.refresh_sensor()
        for sen in ipmi_sensor.fan_pwm_sensor:
            if sen['sensor_name'] == 'FanPWM_peer':
                continue
            assert tar_pwm - 2 < float(sen['value']) < tar_pwm + 2, "Set cooling speed pwm failed!. %s" % sen
        log.success("Set cooling speed pwm %s successfully." % tar_pwm)
    log.info("Restore the fsc mode:")
    ipmi_sensor.ipmi_oem_cmd('set_fsc_mode')
    fsc_status = ipmi_sensor.ipmi_oem_cmd('get_fsc_mode')
    assert fsc_status[3] == 0x00, "The cooling management set to automatic mode failed!"


def check_default_multi_node_info(info_a, info_b):
    """
    byte 1 SlotID:            00h – canister A, 01h – canister B
    byte 2 Role:              01h – Master, 02h - Slave
    byte 3 Peer Alive status: 00h: not alive, 01h: alive
    """
    openbmc_info_a = OpenbmcInfo(info_a)
    openbmc_info_b = OpenbmcInfo(info_b)
    expect_a = [0x00, 0x01, 0x01]
    expect_b = [0x01, 0x02, 0x01]
    mulit_info_a = openbmc_info_a.ipmi_oem_cmd('multi-node_info')
    multi_info_b = openbmc_info_b.ipmi_oem_cmd('multi-node_info')
    assert mulit_info_a == expect_a, "The default multi-node A info is %s. Actural: %s" % (expect_a, mulit_info_a)
    assert multi_info_b == expect_b, "The default multi-node B info is %s. Actural: %s" % (expect_b, multi_info_b)


def check_muli_node_role_change(info_a, info_b):
    openbmc_info_a = OpenbmcInfo(info_a)
    openbmc_info_b = OpenbmcInfo(info_b)
    expect_b = [0x01, 0x01, 0x00]
    log.info("Reset the master role node:")
    WhiteboxLibAdapter.ConnectDevice(openbmc_info_a.device, 'bmc')
    openbmc_info_a.ipmi_dev_global_cmd('cold_reset')
    wait_pattern(openbmc_info_a.device, BOOT_REGEX[0], timeout=120)
    multi_info_b = openbmc_info_b.ipmi_oem_cmd('multi-node_info')
    for r in range(20):
        multi_info_b = openbmc_info_b.ipmi_oem_cmd('multi-node_info')
        if multi_info_b == expect_b:
            log.info("The multi-node B role is changed!")
            break
        time.sleep(1)
    wait_pattern(openbmc_info_a.device, BOOT_REGEX[2], timeout=180)
    WhiteboxLibAdapter.DisconnectDevice(openbmc_info_a.device, 'bmc')
    assert multi_info_b == expect_b, "The multi-node B info should change to %s. Actural: %s" % (expect_b, multi_info_b)
    openbmc_info_a.wait_for_bmc_dev_available()
    check_default_multi_node_info(info_a, info_b)


def check_sensor_threshold_set(dev_info):
    sensor = SensorIpmi(dev_info)
    threshold = sensor.thresholds_cmd(sensor.temp_sensor[2])
    restore_threshold = copy(threshold[1:])
    change_threshold = [x + 2*((threshold[0] >> i) & 0b1) for i, x in enumerate(threshold[1:])]
    output = sensor.thresholds_cmd(sensor.temp_sensor[2], True, *change_threshold)
    assert output[1:] == change_threshold, "Failed to set the sensor threshold values."
    output2 = sensor.thresholds_cmd(sensor.temp_sensor[2], True, *restore_threshold)
    assert output2[1:] == restore_threshold, "Failed to restore the sensor threshold values."


def restore_system_power(dev):
    openbmc_info = OpenbmcInfo(dev)
    WhiteboxLibAdapter.DisconnectDevice(openbmc_info.device, 'bmc')
    WhiteboxLibAdapter.DisconnectDevice(openbmc_info.device, 'os')
    current_power = openbmc_info.check_openbmc_info('power_status', get_status=True)
    WhiteboxLibAdapter.ConnectDevice(openbmc_info.device, 'os', login=False)
    if current_power == 'off':
        openbmc_info.ipmi_power_control('power on')
        wait_prompt(openbmc_info.device, 'os')
    else:
        try:
            ssh_command(openbmc_info.os_username, openbmc_info.os_ip, openbmc_info.os_passwd, 'uname', end=True)
        except Exception:
            openbmc_info.ipmi_power_control('power cycle')
            wait_prompt(openbmc_info.device, 'os')
    WhiteboxLibAdapter.DisconnectDevice(openbmc_info.device, 'os')
    openbmc_info.wait_for_bmc_dev_available()


def check_bmc_kcs_communicate(device, decide=True):
    """
    Check if system can communicate with BMC with default KCS port 0xca0
    :param device:product under test
    :param decide: True/False
    """
    cmd = "dmesg | grep ipmi"
    res = shell_command_ssh(device, cmd)
    if "ipmi_si" not in res:
        if decide:
            whitebox_lib.PRINTE(
                "Fail!  System can't communicate with BMC with default KCS port 0xca0. Response:\n%s" % res)


def set_time_delay(seconds):
    log.debug('Entering procedure set_time_delay with args : %s\n' % (str(locals())))
    log.info('set time delay %s s' % seconds)
    time.sleep(int(seconds))


def run_ipmi_cmd_sel_clear(device):
    sel = SELIpmi(device)
    sel.sel_clear()


def ipmi_standard_cmd(dev_info, cmd, exp_result):
    log.debug('Entering procedure ipmi_standard_cmd with args : %s\n' % (str(locals())))
    openbmc_info = OpenbmcInfo(dev_info)
    openbmc_info.wait_for_bmc_dev_available()
    openbmc_info.check_openbmc_info_raw(cmd, exp_result)


def verify_bmc_user(device, username, bmcip, password, rsp_device_id):
    log.debug("Entering verify_bmc_user with args : %s" % (str(locals())))
    default_username, default_ip, default_passwd = get_ssh_info(device, 'bmc')
    user_list_cmd = 'user list 1'
    user_count = 0
    user_output = run_ipmi_cmd(default_username, default_ip, default_passwd, user_list_cmd, remote=True)
    for user_line in user_output.split('\n'):
        if user_line == '':
            continue
        user_l = user_line.split()
        if user_l[0] == rsp_device_id and user_l[1] == username:
            user_count += 1
            log.info("Successfully Detect the user:%s in the user list" % username)
    if user_count:
        cmd = 'mc info'
        output = run_ipmi_cmd(username, bmcip, password, cmd, True)
        log.info(output)
        log.info("Successfully Use the username:%s to communicate with openbmc" % username)
    else:
        log.error("fail to Use the username:%s to communicate with openbmc" % username)
        raise RuntimeError('verify_bmc_user')


def verify_add_openbmc_user(device, bmcusername, bmcpassword, bmcusrlist_id, new_username=None):
    log.debug("Entering verify_add_openbmc_user with args : %s" % (str(locals())))
    default_username, default_ip, default_passwd = get_ssh_info(device, 'bmc')
    cmd1 = 'user set name %s %s' % (bmcusrlist_id, bmcusername)
    cmd2 = 'user set password %s %s' % (bmcusrlist_id, bmcpassword)
    cmd3 = 'user enable %s' % bmcusrlist_id

    cmd4 = 'raw 6 0x43 0x91 %s 4 0' % hex(int(bmcusrlist_id))
    raw_pw_cmd1 = 'ipmitool raw 0x06 0x47 %s 0x02 0x74 0x65 0x73 0x74 ' \
                  '00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00' % hex(int(bmcusrlist_id) + 0x80)
    raw_pw_cmd2 = 'ipmitool raw 0x06 0x47 %s 0x02 0x74 0x65 0x73 0x74 ' \
                  '00 00 00 00 00 00 00 00 00 00 00 00' % hex(int(bmcusrlist_id))
    run_ipmi_cmd(default_username, default_ip, default_passwd, cmd1, remote=True)
    run_ipmi_cmd(default_username, default_ip, default_passwd, cmd2, remote=True)
    run_ipmi_cmd(default_username, default_ip, default_passwd, cmd3, remote=True)
    run_ipmi_cmd(default_username, default_ip, default_passwd, cmd4, remote=True)
    verify_user_password_is_valid(device, bmcusrlist_id, bmcpassword, byte='16', result=True)
    verify_user_password_is_valid(device, bmcusrlist_id, bmcpassword, byte='20', result=False)
    verify_bmc_user(device, bmcusername, default_ip, bmcpassword, bmcusrlist_id)
    run_ipmi_cmd(default_username, default_ip, default_passwd, raw_pw_cmd1, remote=True)
    run_ipmi_cmd(default_username, default_ip, default_passwd, raw_pw_cmd2, remote=True)
    verify_bmc_user(device, bmcusername, default_ip, 'test', bmcusrlist_id)
    if not new_username:
        new_username_cmd = 'ipmitool user set name %s %s' % (bmcusrlist_id, new_username)
        run_ipmi_cmd(default_username, default_ip, default_passwd, new_username_cmd, remote=True)
        verify_bmc_user(device, new_username, default_ip, 'test', bmcusrlist_id)


def verify_user_password_is_valid(device, bmcusrlist_id, bmcpassword, byte, result):
    log.debug("Entering verify_user_password_is_valid with args : %s" % (str(locals())))
    default_username, default_ip, default_passwd = get_ssh_info(device, 'bmc')
    err_count = 0
    cmd1 = 'user test %s %s %s' % (bmcusrlist_id, byte, bmcpassword)
    p3 = 'Success'
    p4 = 'Failure: wrong password size'
    error_msg = r'.*No such file or directory'
    timeout = 30
    if result:
        output = run_ipmi_cmd(default_username, default_ip, default_passwd, cmd1)
        log.cprint(str(output))
        match = re.search(p3, output)
        if match:
            log.success("Successfully verify_user_password_is_valid: %s" % (match.group(0)))
        else:
            log.fail("Fail to find Success")
            err_count += 1
    else:
        output = run_ipmi_cmd(default_username, default_ip, default_passwd, cmd1)
        log.cprint(str(output))
        match = re.search(p4, output)
        if match:
            log.success("Successfully verify_user_password_is_not_valid: %s" % (match.group(0)))
        else:
            log.fail("Fail to find Failure: wrong password size")
            err_count += 1
    if err_count:
        raise RuntimeError('verify_user_password_is_valid FAIL')


def verify_openbmc_watchdog_timer_ar(bmcip, bmcusername, bmcpassword, remote=False, expected_result=None):
    log.debug("Entering verify_openbmc_watchdog_timer with args : %s" % (str(locals())))
    err_count = 0
    # 01 00 00 00 1f 00 1f 00
    p = r'\d+\s+\d+\s+\d+'
    if remote:
        cmd = 'ipmitool -H %s -U %s -P %s mc info' % (bmcip, bmcusername, bmcpassword)
        # cmd = 'i2cget -y -f 1 0x61 0x02'
        child = ssh_command(bmcusername, bmcip, bmcpassword, cmd)
        child.expect(pexpect.EOF, timeout=30)
        output = child.before.strip().decode('utf-8')
        log.info(output)
    else:
        cmd = 'ipmitool raw 0x06 0x25'
        child = ssh_command(bmcusername, bmcip, bmcpassword, cmd)
        child.expect(pexpect.EOF, timeout=30)
        output = child.before.strip().decode('utf-8')
        log.info(output)
    match = re.search(p, output)
    if match:
        if expected_result != None:
            watchdogtimercmd = match.group().strip()
            if watchdogtimercmd == expected_result:
                log.info("Successfully get atchdogtimer : %s" % (watchdogtimercmd))
            else:
                log.error("get watchdogtimer failed: %s, %s" % (watchdogtimercmd, expected_result))
                err_count += 1
    else:
        log.error("Fail to parse watchdogtimercmd")
        err_count += 1
    if err_count:
        raise RuntimeError('verify_openbmc_watchdog_timer')


def verify_add_sel_entry_ar(bmchostip, bmcusername, bmcuserpassword):
    log.debug("Entering verify_add_sel_entry with args : %s" % (str(locals())))
    err_count = 0
    cmd1 = 'sel list|wc -l'
    count_first = run_ipmi_cmd(bmcusername, bmchostip, bmcuserpassword, cmd1)
    cmd2 = 'raw 0x0a 0x44 00 04 02 0xf3 02 34 56 01 80 04 12 00 0x6f 05 00 00'
    run_ipmi_cmd(bmcusername, bmchostip, bmcuserpassword, cmd2)
    # verify_ipmi_set_cmd(device, cmd2)
    count_last = run_ipmi_cmd(bmcusername, bmchostip, bmcuserpassword, cmd1)
    p = 'Memory'
    if int(count_first) + 1 == int(count_last):
        log.success("Successfully create a sel log")
    else:
        log.error("fail to create a sel log")
        err_count += 1
    cmd3 = 'sel list'
    # output = deviceObj.sendCmdRegexp(cmd3, Const.TIME_REG_PROMPT, timeout=30)
    output = run_ipmi_cmd(bmcusername, bmchostip, bmcuserpassword, cmd3)
    match = re.search(p, output)
    if match:
        log.success("Successfully create sel log related to memory")
    else:
        log.error("FAIL: the sel log is not related to memory")
        err_count += 1
    if err_count:
        raise testFailed("Failed verify_add_sel_entry")


def run_ipmi_get_cmd_ar(bmcip, bmcusername, bmcpassword, cmd, expected_result='None'):
    log.debug('Entering procedure run_ipmi_get_cmd_ar with args : %s\n' % (str(locals())))
    err_count = 0

    output = run_ipmi_cmd(bmcip, bmcusername, bmcpassword, cmd)
    result = parserOpenbmc.parse_oem_output(output)
    error_msg = r'.*No such file or directory'
    if expected_result != 'None':
        if result == expected_result:
            log.success(
                "run cmd \'%s\': return result: \'%s\' match with expected! %s " % (cmd, result, expected_result))
        else:
            log.fail("Command result Mismatch: Found \'%s\' Expected \'%s\'\n" % (result, expected_result))
            err_count += 1
        if err_count:
            raise testFailed("Failed run_ipmi_get_cmd_ar")
    else:
        if result != '' and re.search(error_msg, result) is None:
            log.success("Successfully execute '%s'" % (cmd))
            return result
        else:
            log.fail("failed to execute %s" % (cmd))
            err_count += 1

        if err_count:
            raise testFailed("Failed run_ipmi_get_cmd_ar")


def verify_openbmc_lan_info(bmcip, bmcusername, bmcpassword, cmd, expected):
    log.debug('Entering procedure verify_bmc_lan_info with args : %s\n' % (str(locals())))
    err_count = 0
    output = run_ipmi_cmd(bmcip, bmcusername, bmcpassword, cmd)
    log.info('output: %s' % (output))
    for (k, v) in expected.items():
        p = '%s\s+:\s+(.+)' % k
        match = re.search(p, output)
        if match:
            value = match.group(1).strip()
            if value == v:
                log.success("Successfully verify_bmc_lan_info: expected[%s]=%s" % (k, v))
            else:
                err_count += 1
                log.fail("%s acctual: %s mismatch expected: %s" % (k, value, v))
        else:
            err_count += 1
            log.error("Can't find %s in the log" % k)
    if err_count:
        raise testFailed("Failed verify_bmc_lan_info")


def whitebox_exec_ping_ar(device, username, hostip, userpassword, count, expected='None'):
    log.debug("Entering whitebox_exec_ping with args : %s" % (str(locals())))
    log.debug("Execute the ping from Device:%s to ip:%s" % (device, hostip))
    cmd = "ping %s -c %s" % (hostip, str(count))
    success_msg = str(count) + ' packets transmitted, ' + str(count) + ' (packets )?received, 0% packet loss'
    loss_msg = '100% packet loss'
    output = execute_local_cmd(cmd, timeout=30)
    log.info('output: %s' % (output))
    if expected == 'None':
        match = re.search(success_msg, output)
        if match:
            log.success("Found: %s" % (match.group(0)))
            log.success("ping to %s" % hostip)
        else:
            log.fail("ping to %s" % hostip)
            raise RuntimeError("Ping to destination IP address failed")
    elif expected == 'loss':
        match = re.search(loss_msg, output)
        if match:
            log.success("Found: %s" % (match.group(0)))
            log.success("ping to " + hostip + " get 100% packet loss")
        else:
            log.fail("ping to " + hostip + " did not get 100% packet loss")
            raise RuntimeError("Ping to destination IP address with loss expected failed")


def verify_openbmc_lan_address(bmcip, bmcusername, bmcpassword, expected_result):
    log.debug("Entering verify_openbmc_power_status args : %s" % (str(locals())))
    err_count = 0
    cmd = 'lan print 1'
    # IP Address              : 192.168.10.110
    p1 = r'\s+(\d+).(\d+).(\d+).(\d+)'
    log.info(cmd)
    output = run_ipmi_cmd(bmcusername, bmcip, bmcpassword, cmd, remote=False)
    log.info(output)
    match = re.search(p1, output)
    if match:
        if expected_result != None:
            lan1ip_address = match.group().strip()
            if lan1ip_address == expected_result:
                log.info("Successfully get lan1 ip address: %s" % (lan1ip_address))
            else:
                log.error("get lan1 ip address failed: %s, %s" % (lan1ip_address, expected_result))
                err_count += 1
    else:
        log.error("Fail to parse lan1ip_address")
        err_count += 1
    if err_count:
        raise RuntimeError('ssh_command_verify_openbmc_lan_address')


def verify_openbmc_lan_status(bmcip, bmcusername, bmcpassword, expected_result):
    log.debug("Entering vverify_openbmc_power_status args : %s" % (str(locals())))
    err_count = 0
    cmd = 'lan print 1'
    # IP Address Source       : Static Address
    p1 = r'Static'
    log.info(cmd)
    output = run_ipmi_cmd(bmcusername, bmcip, bmcpassword, cmd, remote=False)
    log.info(output)
    match = re.search(p1, output)
    if match:
        if expected_result != None:
            lan1ip_status = match.group().strip()
            if lan1ip_status == expected_result:
                log.info("Successfully get lan1 ip status: %s" % (lan1ip_status))
            else:
                log.error("get lan1 ip status failed: %s, %s" % (lan1ip_status, expected_result))
                err_count += 1
    else:
        log.error("Fail to parse lan1ip_status")
        err_count += 1
    if err_count:
        raise RuntimeError('ssh_command_verify_openbmc_lan_status')


def whitebox_exec_ping_openbmc(device, bmcusername, bmcip, bmcpassword, count, expected='None'):
    log.debug("Entering whitebox_exec_ping with args : %s" % (str(locals())))
    log.debug("Execute the ping from Device:%s to ip:%s" % (device, bmcip))
    cmd = "ping %s -c %s" % (bmcip, str(count))
    success_msg = str(count) + ' packets transmitted, ' + str(count) + ' (packets )?received, 0% packet loss'
    loss_msg = '100% packet loss'
    output = execute_local_cmd(cmd, timeout=30)
    log.info('output: %s' % (output))
    if expected == 'None':
        match = re.search(success_msg, output)
        if match:
            log.success("Found: %s" % (match.group(0)))
            log.success("ping to %s" % bmcip)
        else:
            log.fail("ping to %s" % bmcip)
            raise RuntimeError("Ping to destination IP address failed")
    elif expected == 'loss':
        match = re.search(loss_msg, output)
        if match:
            log.success("Found: %s" % (match.group(0)))
            log.success("ping to " + bmcip + " get 100% packet loss")
        else:
            log.fail("ping to " + bmcip + " did not get 100% packet loss")
            raise RuntimeError("Ping to destination IP address with loss expected failed")


def ask_info_with_tester_ar(hostip, username, password, bmcip, bmcusername, \
                            bmcpassword, dutusername, dutpassword):
    log.debug('Entering procedure verify_sol_function with args : %s\n' % (str(locals())))
    err_count = 0
    # cmd1 = 'ipmitool -H %s -C 17 -U %s -P %s -I lanplus sol activate' % (bmcip, bmcusername, bmcpassword)
    p1 = hostip
    p2 = bmcip
    # p3 = 'SOL session closed by BMC'
    s = pxssh.pxssh()
    hostname = hostip
    s.login(hostname, username, password, login_timeout=60)

    s.sendline('ifconfig')
    s.prompt()
    time.sleep(3)
    output = s.before.strip().decode('utf-8')
    log.info(output)


def verify_openbmc_fru_print_ar(bmcip, bmcusername, bmcpassword, cmd, expected):
    log.debug('Entering procedure verify_bmc_lan_info with args : %s\n' % (str(locals())))
    err_count = 0
    output = run_ipmi_cmd(bmcip, bmcusername, bmcpassword, cmd)
    log.info('output: %s' % (output))
    for (k, v) in expected.items():
        p = '%s\s+:\s+(.+)' % k
        match = re.search(p, output)
        if match:
            value = match.group(1).strip()
            if value == v:
                log.success("Successfully verify_bmc_fru_print: expected[%s]=%s" % (k, v))
            else:
                err_count += 1
                log.fail("%s actual: %s mismatch expected: %s" % (k, value, v))
        else:
            err_count += 1
            log.error("Can't find %s in the log" % k)
    if err_count:
        raise testFailed("Failed verify_bmc_fru_print")


def Console_Prompt_User(userinfo):
    log.info("\033[1;31;40m%s \033[0m" % (userinfo))
    log.info("\033[1;34;40mWaiting...... \033[0m")
    time.sleep(20)


def compare_info_before_and_after_ar(output1, output2):
    log.debug(
        'Entering procedure compare_fru_info_before_and_after_reset_powercycle with args : %s\n' % (str(locals())))
    count = 0
    output1_split = output1.splitlines()
    for line in output1_split:
        count = count + 1
        if count > 2 and '(' not in line and '[' not in line:
            match = re.search(line, output2)
            if match:
                log.info("succesfully verified {}".format(line))
            else:
                log.fail("Fail to verify {}".format(line))
                raise RuntimeError("Fru info mismatch before and after")


def compare_mc_info_before_and_after_ar(output1, output2):
    log.debug('Entering procedure compare_mc_info_before_and_after_reset with args : %s\n' % (str(locals())))
    pattern1 = "Firmware Revision.*: (\S+)"
    pattern2 = "Manufacturer ID.*: (\S+)"
    pattern3 = "Manufacturer Name.*: Unknown \((\S+)\)"
    pattern4 = "Product ID.*: (\S+) \((\S+)\)"
    pattern5 = "Product Name.*: Unknown \((\S+)\)"
    output1_split = output1.splitlines()
    for line in output1_split:
        match1 = re.search(pattern1, line)
        match2 = re.search(pattern2, line)
        match3 = re.search(pattern3, line)
        match4 = re.search(pattern4, line)
        match5 = re.search(pattern5, line)
        if match1:
            version = match1.group(1)
        if match2:
            mfg_id = match2.group(1)
        if match3:
            mfg_name = match3.group(1)
        if match4:
            pdct_id_1 = match4.group(1)
            pdct_id_2 = match4.group(2)
        if match5:
            pdct_name = match5.group(1)
    pattern1 = "Firmware Revision.*: {}".format(version)
    pattern2 = "Manufacturer ID.*: {}".format(mfg_id)
    pattern3 = "Manufacturer Name.*: Unknown \({}\)".format(mfg_name)
    pattern4 = "Product ID.*: {} \({}\)".format(pdct_id_1, pdct_id_2)
    pattern5 = "Product Name.*: Unknown \({}\)".format(pdct_name)
    match1 = re.search(pattern1, output2)
    match2 = re.search(pattern2, output2)
    match3 = re.search(pattern3, output2)
    match4 = re.search(pattern4, output2)
    match5 = re.search(pattern5, output2)
    if match1:
        log.info("Firmware Revision check successful")
    else:
        log.info("Firmware Revision check Failed")
        raise RuntimeError("Firmware Revision check Failed")
    if match2:
        log.info("Manufacturer ID check successful")
    else:
        log.info("Manufacturer ID check Failed")
        raise RuntimeError("Manufacturer ID check Failed")
    if match3:
        log.info("Manufacturer Name check successful")
    else:
        log.info("Manufacturer Name check Failed")
        raise RuntimeError("Manufacturer Name check Failed")
    if match4:
        log.info("Product ID check successful")
    else:
        log.info("Product ID check Failed")
        raise RuntimeError("Product ID check Failed")
    if match4:
        log.info("Product Name check successful")
    else:
        log.info("Product Name check Failed")
        raise RuntimeError("Product Name check Failed")


def verify_cmd_output_message_ar(bmcip, bmcusername, bmcpassword, cmd, messages_list):
    log.debug('Entering procedure verify_cmd_output_message with args : %s\n' % (str(locals())))
    output = run_ipmi_cmd(bmcip, bmcusername, bmcpassword, cmd, remote=False)
    err_count = 0
    messages_list = messages_list.split(",")
    for msg in messages_list:
        if parse_keywords(msg, output) == "fail":
            err_count += 1
    if err_count == 0:
        log.success("Successfully verify '%s' output message" % cmd)
    else:
        log.fail("verify_%s_output_message fail" % cmd)
        raise testFailed("verify '%s' output message fail" % cmd)


def verify_cmd_sensor_message_ar(bmcusername, bmcip, bmcpassword, cmd, sensor_vlts, expected_result, countsen):
    log.debug('Entering procedure verify_cmd_output_message with args : %s\n' % (str(locals())))
    output = run_ipmi_cmd(bmcusername, bmcip, bmcpassword, cmd, remote=False)
    sensorf_count = 0
    sensor_th_data = []
    for line in output.splitlines():
        for sensor_dt in sensor_vlts.split(','):
            match = re.search(sensor_dt, line)
            if match:
                log.success("Successfully verify the sensor threshold'%s' output message" % cmd)
                log.info(match.group())
                sensor_th_data.append(match.group())
                sensorf_count += 1
            else:
                log.info("verify_%s_output_message not found" % cmd)
    sensor_th_data_sort = list((set(sensor_th_data)))
    sensor_th_data_sort.sort()
    sensor_th_data_sort_ar = str(sensor_th_data_sort)
    sensorf_countc = str(sensorf_count)
    if sensor_th_data_sort_ar == expected_result:
        log.info("verify %s sensor threshold match" % (sensor_th_data_sort_ar))
    else:
        log.fail(
            "verify  %s sensor threshold Not match with expected %s sensor" % (sensor_th_data_sort_ar, expected_result))
        raise testFailed("verify '%s' output message fail" % cmd)
    if sensorf_countc == countsen:
        log.info("verify %s sensor threshold match" % (sensorf_countc))
    else:
        log.fail("verify  %s sensor threshold Not match with expected %s sensor" % (sensorf_countc, countsen))
        raise testFailed("verify '%s' output message fail" % cmd)


def common_check_patern_2(output, p, testname, expect=True):
    if expect:
        match = re.search(p, output)
        if match:
            log.info("Successfully {}: {}".format(testname, p))
        else:
            log.fail("Fail to {}".format(testname))
            raise RuntimeError("{}".format(testname))
    else:
        match = re.search(p, output)
        if match:
            log.fail("Fail to {}".format(testname))
            raise RuntimeError("{}".format(testname))
        else:
            log.info("Successfully {}: {}".format(testname, p))


def run_curl_get(resource, bmcIP=None, bmcUserName=None, bmcPassword=None, auth=True):
    if bmcIP:
        cmd = "curl -k https://" + bmcIP + resource
        if auth:
            cmd = cmd + " -u " + bmcUserName + ":" + bmcPassword
    else:
        global device
        device = DeviceMgr.getDevice()
        cmd = "curl -k https://" + device.bmcIP + resource
        if auth:
            cmd = cmd + " -u " + device.bmcUserName + ":" + device.bmcPassword
    log.success(cmd)
    arg_list = cmd.split(' ')
    output = subprocess.check_output(arg_list)
    log.success(str(output))
    return json.loads(output)


def get_key_value(dictionary, key, value=None):
    tmp = list(find_keys(dictionary, key))
    if tmp != []:
        log.success("Key %s is Present" % (key))
        out = tmp[0]
        log.info("Value of the key {} is {}".format(key, str(out)))
        if value:
            log.info("Expected values for the key {} is {}".format(key, value))
            if str(out) == value:
                log.success("Expected value of the key {} is present".format(key))
            else:
                raise testFailed("Expected value of the key {} is not present".format(key))
    else:
        log.fail("Key %s is not Present" % (key))
        show_unit_info(device)
        raise testFailed("Key %s is not Present" % (key))


def find_keys(node, kv):
    if isinstance(node, list):
        for i in node:
            for x in find_keys(i, kv):
                yield x
    elif isinstance(node, dict):
        if kv in node:
            yield node[kv]
        for j in node.values():
            for x in find_keys(j, kv):
                yield x


def verify_all_fans(dictionary, count):
    output = str(dictionary)
    count = int(count)
    for i in range(0, count):
        value = "/redfish/v1/Chassis/artemis_motherboard/Thermal#/Fans/{}".format(i)
        match = re.search(value, output)
        if match:
            log.info("Fan {} present".format(i))
        else:
            log.info("Fan {} not present".format(i))
            raise testFailed("Fan {} not present".format(i))


def verify_all_temperatures(dictionary, count):
    output = str(dictionary)
    count = int(count)
    for i in range(0, count):
        value = "/redfish/v1/Chassis/artemis_motherboard/Thermal#/Temperatures/{}".format(i)
        match = re.search(value, output)
        if match:
            log.info("temperatures {} present".format(i))
        else:
            log.info("temperatures {} not present".format(i))
            raise testFailed("temperatures {} not present".format(i))


def verify_count_Health(dictionary, exp_count):
    output = str(dictionary)
    exp_count = int(exp_count)
    actual_count = 0
    output = output.split("Status")
    pattern = "'Health': 'OK'"
    for line in output:
        log.info(line)
        match = re.search(pattern, line)
        if match:
            actual_count = actual_count + 1
    log.info("Actual count of Health status OK is {}".format(actual_count))
    if exp_count == actual_count:
        log.info("Health status checked verification is successful")
    else:
        log.info("Health status checked verification failed")
        raise testFailed("Health status checked verification failed")


def verify_count_State(dictionary, exp_count):
    output = str(dictionary)
    exp_count = int(exp_count)
    actual_count = 0
    output = output.split("Status")
    pattern = "'State': 'Enabled'"
    for line in output:
        log.info(line)
        match = re.search(pattern, line)
        if match:
            actual_count = actual_count + 1
    log.info("Actual count of state Enabled is {}".format(actual_count))
    if exp_count == actual_count:
        log.info("Enabled state checked verification is successful")
    else:
        log.info("Enabled status checked verification failed")
        raise testFailed("Enabled status checked verification failed")


def run_curl_post(resource, filename, bmcIP=None, bmcUserName=None, bmcPassword=None, auth=True):
    cmd = "curl -k -X POST https://" + bmcIP + resource + " -T " + filename + " -H " + "Content-Type:application/octet-stream"
    log.info(cmd)
    if auth:
        cmd = cmd + " -u " + bmcUserName + ":" + bmcPassword
    log.success(cmd)
    arg_list = cmd.split(' ')
    try:
        output = subprocess.check_output(arg_list)
    except:
        log.fail("Failed to execute curl POST command")
        show_unit_info(device)
        raise testFailed("Failed to execute curl POST command")
    log.success(str(output))
    return json.loads(output)


def common_check_pattern(output, p, testname, expect=True):
    if expect:
        match = re.search(p, output)
        if match:
            log.info("Successfully {}: {}".format(testname, p))
        else:
            log.fail("Fail to {}".format(testname))
            raise RuntimeError("{}".format(testname))
    else:
        match = re.search(p, output)
        if match:
            log.fail("Fail to {}".format(testname))
            raise RuntimeError("{}".format(testname))
        else:
            log.info("Successfully {}: {}".format(testname, p))


def dc_cycle_server_1(bmcip, bmcusername, bmcpassword):
    cmd = 'ipmitool -I lanplus -H {} -U {} -P {} power cycle -C 17'.format(bmcip, bmcusername, bmcpassword)
    p = 'Chassis Power Control\W\s+Cycle'
    output = execute_local_cmd(cmd)
    common_check_pattern(output, p, 'dc_cycle_server', expect=True)


def run_ipmi_get_cmd_success_ar(bmcip, bmcusername, bmcpassword, cmd, reg, expected_result='None'):
    log.debug('Entering procedure run_ipmi_get_cmd_ar with args : %s\n' % (str(locals())))
    err_count = 0
    output = run_ipmi_cmd(bmcip, bmcusername, bmcpassword, cmd)
    log.info(output)
    match = re.search(reg, output)
    result = match.group().strip()
    error_msg = r'.*No such file or directory'
    if expected_result != 'None':
        if result == expected_result:
            log.success("run cmd %s: return result: %s match with expected: %s " % (cmd, result, expected_result))
        else:
            log.fail("Command result Mismatch: Found \'%s\' Expected \'%s\'\n" % (result, expected_result))
            err_count += 1
        if err_count:
            raise testFailed("Failed run_ipmi_get_cmd_ar")
    else:
        if result != '' and re.search(error_msg, result) is None:
            log.success("Successfully execute %s,return result is: %s " % (cmd, result))
            return result
        else:
            log.fail("failed to execute %s" % (cmd))
            err_count += 1
        if err_count:
            raise testFailed("Failed run_ipmi_get_cmd_ar")


def verify_get_ip6_ar(bmcusername, bmcip, bmcpassword, expected='none'):
    log.debug('Entering procedure verify_get_ip6_Function with args : %s\n' % (str(locals())))
    cmd = "ip a |grep fe80"
    outputip6 = ssh_command(bmcusername, bmcip, bmcpassword, cmd, end=True)
    log.info(outputip6)
    p = r'fe80::[\d\w]{3}:[\d\w]{4}:[\d\w]{4}:[\d\w]{4}'
    match = re.findall(p, outputip6)
    lanip6_1 = match[0]
    lanip6_2 = match[1]
    if expected == 'lan_1':
        log.info(str(lanip6_1))
        return lanip6_1
    if expected == 'lan_2':
        log.info(str(lanip6_2))
        return lanip6_2


def verify_ssh_ping6_function_ar(bmcusername, bmcip, bmcpassword, username, hostip, password, ipaddr='None', count='30',
                                 expected='None'):
    log.debug('Entering procedure verify_ssh_ping6_Function with args : %s\n' % (str(locals())))
    err_count = 0
    success_msg = '(\d+)\s+packets transmitted,\s+(\d+)\s+received,\s+(\d+)% packet loss'
    loss_msg = str(count) + ' packets transmitted, ' + '0 packets received, 100% packet loss'
    ipaddr1 = verify_get_ip6_ar(bmcusername, bmcip, bmcpassword, expected='lan_1')
    time.sleep(1)
    ipaddr2 = verify_get_ip6_ar(bmcusername, bmcip, bmcpassword, expected='lan_2')
    if ipaddr == 'ip1':
        cmd = "time ping6 %s -c %s" % (ipaddr1, count)
        # timeout_1 = count
    if ipaddr == 'ip2':
        cmd = "time ping6 %s -c %s" % (ipaddr2, count)
        # timeout_1 = count
    output = ssh_command(username, hostip, password, cmd, end=True)
    log.info(output)
    if expected == 'None':
        match = re.search(success_msg, output)
        if match:
            transmitted_packets = match.group(1).strip()
            received_packets = match.group(2).strip()
            rate = match.group(3).strip()
            if rate == '0':
                log.info("Found: %s" % (match.group(0)))
                log.success("ssh ping6 to %s" % ipaddr)
            else:
                if int(transmitted_packets) - int(received_packets) == 1:
                    log.info("Found: %s, one packet lost at the beginning is acceptable" % (match.group(0)))
                    log.success("ssh ping6 to %s" % ipaddr)
                else:
                    err_count += 1
                    log.fail("ssh ping6 to %s, %s" % (ipaddr, match.group(0)))
        else:
            err_count += 1
            log.fail("ssh ping6 to %s" % ipaddr)
    elif expected == 'loss':
        match = re.search(loss_msg, output)
        if match:
            log.success("Found: %s" % (match.group(0)))
            log.success("ssh ping6 to " + ipaddr + " get 100% packet loss")
        else:
            log.fail("ssh ping6 to " + ipaddr + " did not get 100% packet loss")
            raise RuntimeError("SSH Ping6 to destination IP address with loss expected failed")
    else:
        err_count += 1
        log.fail("Please input the right keywords")
    if err_count:
        raise RuntimeError("SSH Ping6 to destination IP address failed")


def enter_and_exit_bios_option_ar(device, username, dutip, passwd):
    log.debug('Entering procedure enter_and_exit_bios_option with args : %s\n' % (str(locals())))
    WhiteboxLibAdapter.ConnectDevice(device, 'os')
    time.sleep(5)
    ssh_command(username, dutip, passwd, 'ipmitool power cycle', end=True)
    time.sleep(1)
    wait_pattern(device, 'AMI', timeout=200)
    wait_pattern(device, 'ART', timeout=200)
    time.sleep(10)
    send_key(device, "KEY_ENTER")
    time.sleep(1)
    send_key(device, "KEY_ENTER")
    time.sleep(1)
    send_key(device, "KEY_ESC")
    time.sleep(1)
    send_key(device, "KEY_ENTER")
    time.sleep(1)


def verify_sol_function_ar(dev_info):
    log.debug('Entering procedure verify_sol_function with args : %s\n' % (str(locals())))
    err_count = 0
    openbmc_info = OpenbmcInfo(dev_info)
    cmd_prompt = get_deviceinfo_from_config(openbmc_info.device, 'promptDiagOS')
    login_prompt = get_deviceinfo_from_config(openbmc_info.device, 'loginPromptDiagOS')
    s_log = ssh_command(openbmc_info.bmcusername, openbmc_info.bmcip, openbmc_info.bmcpasswd, '-p 2200 ', end=False)
    s_log.sendline('exit')
    e = s_log.expect([login_prompt, 'Password:'], timeout=30)
    if e:
        s_log.sendline('\n')
        s_log.expect(login_prompt, timeout=30)
    log.info("Active SOL, try to login.")
    s_log.sendline(openbmc_info.os_username)
    s_log.expect('Password:', timeout=30)
    s_log.sendline(openbmc_info.os_passwd)
    s_log.sendline('ip a')
    s_log.expect(openbmc_info.os_ip, timeout=30)
    output = s_log.after.strip().decode('utf-8')
    log.info(output)
    match1 = re.search(openbmc_info.os_ip, output)
    if match1:
        log.info("Successfully active SOL")
    else:
        log.error("FAIL to active SOL")
        err_count += 1
    s_log.sendline('exit')
    s_log.expect(login_prompt, timeout=180)
    s_log.sendline('\n~.')
    s_log.expect(pexpect.EOF, timeout=180)
    output = s_log.before.strip().decode('utf-8')
    log.info(output)
    match2 = re.search('close', output)
    if match2:
        log.info("Successful to close SOL")
    else:
        log.error("FAIL to close  SOL")
        err_count += 1
    if err_count:
        raise testFailed("Failed to verify the SOL Function!")


def verify_led_set_status_ar(bmcip, bmcusername, bmcpassword, offsetv):
    err_count = 0
    led_get_set_dic = {}
    led_set1 = 'i2c bus=1 0xC2 0x00' + ' ' + offsetv + ' 0x01'
    led_set2 = 'i2c bus=1 0xC2 0x00' + ' ' + offsetv + ' 0x02'
    led_set3 = 'i2c bus=1 0xC2 0x00' + ' ' + offsetv + ' 0x03'
    led_set4 = 'i2c bus=1 0xC2 0x00' + ' ' + offsetv + ' 0x04'
    led_set5 = 'i2c bus=1 0xC2 0x00' + ' ' + offsetv + ' 0x08'
    led_set6 = 'i2c bus=1 0xC2 0x00' + ' ' + offsetv + ' 0x0c'
    led_set7 = 'i2c bus=1 0xC2 0x00' + ' ' + offsetv + ' 0x10'
    led_set8 = 'i2c bus=1 0xC2 0x00' + ' ' + offsetv + ' 0x20'
    led_set9 = 'i2c bus=1 0xC2 0x00' + ' ' + offsetv + ' 0x30'
    led_set10 = 'i2c bus=1 0xC2 0x00' + ' ' + offsetv + ' 0x40'
    led_set11 = 'i2c bus=1 0xC2 0x00' + ' ' + offsetv + ' 0x80'
    led_set12 = 'i2c bus=1 0xC2 0x00' + ' ' + offsetv + ' 0xc0'
    led_set13 = 'i2c bus=1 0xC2 0x00' + ' ' + offsetv + ' 0x00'
    led_get_set_dic['01'] = led_set1
    led_get_set_dic['02'] = led_set2
    led_get_set_dic['03'] = led_set3
    led_get_set_dic['04'] = led_set4
    led_get_set_dic['08'] = led_set5
    led_get_set_dic['0c'] = led_set6
    led_get_set_dic['10'] = led_set7
    led_get_set_dic['20'] = led_set8
    led_get_set_dic['30'] = led_set9
    led_get_set_dic['40'] = led_set10
    led_get_set_dic['80'] = led_set11
    led_get_set_dic['c0'] = led_set12
    led_get_set_dic['00'] = led_set13
    for led_rsp, led_set_cmd in led_get_set_dic.items():
        out_put_set_led = run_ipmi_cmd(bmcip, bmcusername, bmcpassword, led_set_cmd, remote=True)
        # log.info("LED set successful %s" %(led_set_cmd))
        out_put_get_led = run_ipmi_cmd(bmcip, bmcusername, bmcpassword, 'i2c bus=1 0xC2 0x01', remote=True)
        # log.info("The respond for led value successful %s"  %(led_rsp))
        p = r'\s[\d\w]{2}\s'
        match = re.search(p, out_put_get_led)
        rsp_value = match.group().strip()
        if rsp_value == led_rsp:
            log.success("verify led get value: %s; match with expected %s ." % (rsp_value, led_rsp))
        elif rsp_value != led_rsp:
            for i in range(30):
                out_put_set_led = run_ipmi_cmd(bmcip, bmcusername, bmcpassword, led_set_cmd, remote=True)
                out_put_get_led = run_ipmi_cmd(bmcip, bmcusername, bmcpassword, 'i2c bus=1 0xC2 0x01', remote=True)
                p = r'\s[\d\w]{2}\s'
                match = re.search(p, out_put_get_led)
                rsp_value = match.group().strip()
                if rsp_value == led_rsp:
                    log.success("verify led get value: %s; match with expected %s ." % (rsp_value, led_rsp))
                    break
        else:
            log.fail("verify led get value: %s; Not match with expected %s . " % (rsp_value, led_rsp))
            err_count += 1
    if err_count:
        raise RuntimeError('Verify led set value Fail!')


def verify_ssd_on_off_status_ar(bmcip, bmcusername, bmcpassword, offset_ssd):
    err_count = 0
    ssd_get_set_dic = {}
    ssd_set1 = 'i2c bus=1 0xC2 0x00' + ' ' + offset_ssd + ' 0x01'
    ssd_set2 = 'i2c bus=1 0xC2 0x00' + ' ' + offset_ssd + ' 0x02'
    ssd_set3 = 'i2c bus=1 0xC2 0x00' + ' ' + offset_ssd + ' 0x04'
    ssd_set4 = 'i2c bus=1 0xC2 0x00' + ' ' + offset_ssd + ' 0x08'
    ssd_set5 = 'i2c bus=1 0xC2 0x00' + ' ' + offset_ssd + ' 0x10'
    ssd_set6 = 'i2c bus=1 0xC2 0x00' + ' ' + offset_ssd + ' 0x20'
    ssd_set7 = 'i2c bus=1 0xC2 0x00' + ' ' + offset_ssd + ' 0x40'
    ssd_set8 = 'i2c bus=1 0xC2 0x00' + ' ' + offset_ssd + ' 0x80'
    ssd_set9 = 'i2c bus=1 0xC2 0x00' + ' ' + offset_ssd + ' 0xff'
    ssd_set10 = 'i2c bus=1 0xC2 0x00' + ' ' + offset_ssd + ' 0x00'
    ssd_get_set_dic['01'] = ssd_set1
    ssd_get_set_dic['02'] = ssd_set2
    ssd_get_set_dic['04'] = ssd_set3
    ssd_get_set_dic['08'] = ssd_set4
    ssd_get_set_dic['10'] = ssd_set5
    ssd_get_set_dic['20'] = ssd_set6
    ssd_get_set_dic['40'] = ssd_set7
    ssd_get_set_dic['80'] = ssd_set8
    ssd_get_set_dic['ff'] = ssd_set9
    ssd_get_set_dic['00'] = ssd_set10

    for ssd_rsp, ssd_set_cmd in ssd_get_set_dic.items():
        out_put_set_ssd = run_ipmi_cmd(bmcip, bmcusername, bmcpassword, ssd_set_cmd)
        log.info("ssd turn on and off successful %s" % (ssd_set_cmd))
        out_put_get_ssd = run_ipmi_cmd(bmcip, bmcusername, bmcpassword, 'i2c bus=1 0xC2 0x01')
        log.info("The respond for ssd value successful %s" % (ssd_rsp))
        p = r'\s[\d\w]{2}\s'
        match = re.search(p, out_put_get_ssd)
        rsp_value = match.group().strip()
        if rsp_value == ssd_rsp:
            log.success("verify ssd on and off value: %s; match with expected %s ." % (rsp_value, ssd_rsp))
        elif rsp_value != ssd_rsp:
            for i in range(10):
                out_put_set_ssd = run_ipmi_cmd(bmcip, bmcusername, bmcpassword, ssd_set_cmd, remote=True)
                out_put_get_ssd = run_ipmi_cmd(bmcip, bmcusername, bmcpassword, 'i2c bus=1 0xC2 0x01', remote=True)
                p = r'\s[\d\w]{2}\s'
                match = re.search(p, out_put_get_ssd)
                rsp_value = match.group().strip()
                if rsp_value == ssd_rsp:
                    log.success("verify ssd on and off value: %s; match with expected %s ." % (rsp_value, ssd_rsp))
                    break
        else:
            log.fail("verify ssd on and off value: %s; Not match with expected %s . " % (rsp_value, ssd_rsp))
            err_count += 1
    if err_count:
        raise RuntimeError('Verify ssd turn on and turn off command Fail!')
