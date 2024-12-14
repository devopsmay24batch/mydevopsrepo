###############################################################################
# LEGALESE:   "Copyright (C) 2019-2021, Celestica Corp. All rights reserved." #
#                                                                             #
# This source code is confidential, proprietary, and contains trade           #
# secrets that are the sole property of Celestica Corp.                       #
# Copy and/or distribution of this source code or disassembly or reverse      #
# engineering of the resultant object code are strictly forbidden without     #
# the written consent of Celestica Corp.                                      #
#                                                                             #
###############################################################################
import sys
import os
import time
import re
import CRobot
workDir = CRobot.getWorkDir()
sys.path.append(workDir)
sys.path.append(os.path.join(workDir, 'common', 'commonlib'))
sys.path.append(os.path.join(workDir, 'platform', 'juniper'))

from common.commonlib import CommonLib
from common.commonlib import CommonKeywords
from JuniperSdkVariable import *
from JuniperCommonVariable import *
from crobot import Logger as log
import DeviceMgr
from crobot.SwImage import SwImage
from crobot.Decorator import logThis
from time import sleep
from common.sdk import SdkCommonLib
import JuniperCommonLib


device = DeviceMgr.getDevice()


@logThis
def loginDevice():
    device.loginDiagOS()


@logThis
def sdkDisconnect():
    return device.disconnect()


@logThis
def verify_load_sdk(option=''):
    cmd = "./%s %s"%(SDK_SCRIPT, option)
    # device.executeCmd('killall -9 %s' % BCM_USER)   # this can stop the bcm.user process!
    # SdkCommonLib.stopBcmProcess()
    prompt = device.promptDiagOS if option == '-d' else BCM_promptstr
    output = device.executeCommand(cmd, prompt, timeout=90)
    status = SdkCommonLib.checkOutput(output, patterns=fail_pattern, is_negative_test=True)
    if not status:
        raise Exception("Find errors when execute {}.".format(cmd))
    else:
        log.info('%s is PASSED\n' %cmd)


@logThis
def check_port_status():
    output = device.executeCommand(ps_cmd, BCM_promptstr, timeout=30)
    success = SdkCommonLib.checkOutput(output, patterns=port_status_patterns)
    if success:
        log.success('check_port_status successfully.')
    else:
        raise RuntimeError('check_port_status failed!')

@logThis
def check_epdm_link_status():
    output = device.executeCommand("epdm link all", BCM_promptstr, timeout=30)
    success = SdkCommonLib.checkOutput(output, patterns=epdm_link_patterns)
    if success:
        log.success('check_epdm_link_status successfully.')
    else:
        raise RuntimeError('check_epdm_link_status failed!')

@logThis
def check_phy_info():
    output = device.executeCommand('epdm phy info all', BCM_promptstr)
    CommonKeywords.should_match_ordered_regexp_list(output, phy_info_patterns)
    log.success('check_phy_info successfully.')


@logThis
def check_mdio_advisor():
    output = device.executeCommand('config show rate_ext_mdio_divisor', BCM_promptstr)
    CommonKeywords.should_match_a_regexp(output, mdio_advisor_pattern)
    log.success('check_mdio_advisor successfully.')


@logThis
def check_uplink_prbs_sys_side():
    output = device.executeCommand(uplink_prbs_get, BCM_promptstr)   ##@issue, this cmd always failed first time
    output = device.executeCommand(uplink_prbs_get, BCM_promptstr)
    CommonKeywords.should_match_a_regexp(output, "PRBS OK!")
    time.sleep(300)
    output = device.executeCommand('epdm prbs get ce0 lane=all if=sys', BCM_promptstr)
    success = SdkCommonLib.checkOutput(output, patterns=uplink_prbs_patterns)
    if not success:
        raise RuntimeError('check_uplink_prbs_sys_side failed!')

    output = device.executeCommand(uplink_prbs_get, BCM_promptstr)
    CommonKeywords.should_match_a_regexp(output, "PRBS OK!")
    log.success('check_uplink_prbs_sys_side successfully.')


@logThis
def check_uplink_prbs_line_side():
    output = device.executeCommand('epdm prbs get ce0 lane=all if=line', BCM_promptstr)
    success = SdkCommonLib.checkOutput(output, patterns=uplink_prbs_patterns)
    if not success:
        raise RuntimeError('check_uplink_prbs_line_side failed!')

    log.success('check_uplink_prbs_line_side successfully.')

@logThis
def phy_prbs_test():
    card_type = JuniperCommonLib.get_card_type()
    CommonLib.change_dir(sdk_path)
    verify_load_sdk(option='-a')
    check_epdm_link_status()
    if card_type in ["48MP", "48F"]:  ####@todo need add other cord type process
        CommonLib.run_cmd("epdm prbs set ce0 tx_rx=0 p=5 lane=all inv=0 if=line", BCM_promptstr)
        time.sleep(300)
        check_uplink_prbs_line_side()

    log.success('phy_prbs_test successfully.')

@logThis
def Check_port_link_status_and_link_speed(action):
    portminspeed_num = '1000'
    portmaxspeed_num = '10000'
    cmd = 'ps'
    output = device.executeCommand(cmd, BCM_promptstr, timeout=60)
    if not re.search('down', output):
        log.success("Check_port_link_status_and_link_speed up successfull")
    else:
        raise RuntimeError("Check_port_link_status_and_link_speed up fail")
    cmd1 = 'epdm link all'
    output2 = device.executeCommand(cmd1, BCM_promptstr, timeout=60)
    patten = 'miura\s.*0x2\d\s+(\d+)\s+.*'
    for line in output2.splitlines():
        speed = re.search(patten, line)
        if speed:
            speeds = speed.group(1)
    log.info(speeds)
    if action == 'minimum' and speeds == portminspeed_num:
        log.success("Check_port_link_status_and_link_speed successffully")
    elif action == 'maximum' and speeds == portmaxspeed_num:
        log.success("Check_port_link_status_and_link_speed successffully")
    else:
        raise RuntimeError("Check_port_link_status_and_link_speed fail")

@logThis
def Change_all_port_speed_to(action):
    minimum_cmd = 'portminspeed.soc'
    maximum_cmd = 'portmaxspeed.soc'
    portminspeed_num = '1000'
    portmaxspeed_num = '10000'
    if action == 'minimum':
        output = device.executeCommand(minimum_cmd, BCM_promptstr, timeout=60)
        log.info(output)
    elif action == 'maximum':
        output = device.executeCommand(maximum_cmd, BCM_promptstr, timeout=60)
        log.info(output)
    else:
        log.debug("There is no action")
    pattern = '.*second=(\d+) speed1=(\d+)'
    speed = re.search(pattern, output).group(2)
    log.info(speed)
    if speed == portminspeed_num:
        log.success("Change_all_port_speed_to_{} successfully".format(action))
    elif speed == portmaxspeed_num:
        log.success("Change_all_port_speed_to_{} successfully".format(action))
    else:
        raise RuntimeError("Change_all_port_speed_to_{} fail".format(action))
