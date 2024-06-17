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
import re

import CRobot
workDir = CRobot.getWorkDir()
sys.path.append(workDir)
sys.path.append(os.path.join(workDir, 'common', 'commonlib'))
sys.path.append(os.path.join(workDir, 'platform', 'ali'))

from common.commonlib import CommonLib
from common.commonlib import CommonKeywords
from AliSdkVariable import *
from AliCommonVariable import *
from crobot import Logger as log
import DeviceMgr
from crobot.SwImage import SwImage
from crobot.Decorator import logThis
from time import sleep
from common.sdk import SdkCommonLib
from common.sdk import SdkLibAdapter


device = DeviceMgr.getDevice()


@logThis
def loginDevice():
    device.loginDiagOS()
    device.sendCmd('sudo su')


@logThis
def sdkDisconnect():
    return device.disconnect()


@logThis
def installSdk():
    sdkImage = SwImage.getSwImage(SwImage.SDK)
    device.executeCmd('cd /tmp/')
    device.executeCmd('rm -fr ' + sdk_path)
    device.executeCmd('unzip -j {} -d {}'.format(sdkImage.newImage, sdk_path))
    device.executeCmd('cd ' + sdk_path)
    device.executeCmd("chmod +x %s %s" % (SDK_SCRIPT, BCM_USER))


@logThis
def checkSdkversion():
    sdkImage = SwImage.getSwImage(SwImage.SDK)
    device.executeCmd('cd ' + sdk_path)
    device.read_until_regexp(device.getCurrentPromptStr())  #
    output = device.executeCmd('cat {}'.format(sdk_version_file))
    version = parseSdkVersion(output)

    if version.lstrip('v') != sdkImage.newVersion.lstrip('v'):
        raise RuntimeError("current version {} do not match the expected versjon {}".format(version, sdkImage.newVersion))
    else:
        log.success("current version {} match the expected versjon {}".format(version, sdkImage.newVersion))

@logThis
def parseSdkVersion(output):
    lines = output.splitlines()
    for line in lines:
        match = re.search(r'(\d+\.\d+\.\d+)', line.strip())
        if match:
            return match.group(1).strip()
    raise RuntimeError('Can not parse sdk version')

@logThis
def verifyLoadSDK(option='', pattern=[]):
    cmd = "./%s %s"%(SDK_SCRIPT, option)
    device.executeCmd('killall -9 %s' % BCM_USER)   # this can stop the bcm.user process!
    SdkCommonLib.stopBcmProcess()
    prompt = device.promptDiagOS if option == '-d' else BCM_promptstr
    output = device.executeCommand(cmd, prompt, timeout=20)
    # SdkCommonLib.checkOutput(output, patterns=pattern, remark="")
    status = SdkCommonLib.checkOutput(output, patterns=fail_pattern, is_negative_test=True)
    if not status:
        # raise Exception("Find errors when execute {}.".format(cmd))
        pass  ## @ISSUE @WORKAROUND sal_config_refresh: cannot read file: config.bcm, variables not loaded, when run case 015 on unit 4001
    else:
        log.info('%s is PASSED\n' %cmd)

@logThis
def setSnakeVlanToAllPorts(port_cmd=set_snake_vlan_200G_cmd):
    patterns = fail_pattern
    output = ""
    for port_cmd in (port_cmd, pvlan_show_cmd, vlan_show_cmd):
        output += CommonLib.run_command(port_cmd, deviceObj=device,
                prompt=BCM_promptstr.replace(".","\."), timeout=300)
    check_status = SdkCommonLib.checkOutput(output, patterns=patterns, is_negative_test=True)
    if not check_status:
        raise Exception("Execute {} failed.".format(port_cmd))

@logThis
def set200gSoc(port_cmd=set_snake_vlan_200G_cmd):
    patterns = fail_pattern
    output = device.executeCommand(port_cmd, BCM_promptstr, timeout=300)
    check_status = SdkCommonLib.checkOutput(output, patterns=patterns, is_negative_test=True)
    if not check_status:
        raise Exception("Execute {} failed.".format(port_cmd))

@logThis
def verifyAllPortStatus(port_status_pattern, port_cmd, port_search_pattern, prompt_str=BCM_promptstr):
    output = device.executeCommand(port_cmd, prompt_str, timeout=100)
    port_status_pattern = ".*?".join(port_status_pattern)
    port_status_count = len(re.findall(port_status_pattern, output))
    port_sum = len(re.findall(port_search_pattern, output))
    if port_sum == 0:
        raise Exception("Didn't find port info")
    if port_sum == port_status_count:
        log.success('verifyAllPortStatus is passed\n')
    else:
        raise Exception("Normal ports:{}, total ports:{} \n".format(port_status_count, port_sum))

@logThis
def verifyRemotePortStatus(port_status_pattern=port_up_status):
    device.executeCmd(cls_shell_port_status)
    #output = device.sendCmdRegexp('', r'{}[\s\S]+{}'.format('cd0', device.promptDiagOS), timeout=60)
    output = device.sendCmdRegexp('', r'cd127.*?RS544-2xN', timeout=60)
    device.sendCmd('')
    port_status_pattern = ".*?".join(port_status_pattern)
    port_status_count = len(re.findall(port_status_pattern, output))
    port_sum = len(re.findall(port_pattern, output))
    if port_sum == 0:
        raise Exception("Didn't find port info")
    if port_sum == port_status_count:
        log.success('verifyAllPortStatus is passed\n')
    else:
        raise Exception("Normal ports:{}, total ports:{} \n".format(port_status_count, port_sum))

@logThis
def verifyAllPortData(patterns=port_XLMIB_RPKT_pattern):
    err_count = 0
    match_flag = 0
    first_data = []
    changePortsStatus(show_c_cmd)
    finish_prompt = "{}[\s\S]+{}".format(show_c_cmd[:5], BCM_promptstr)
    output = device.read_until_regexp(finish_prompt, timeout=300)
    # output = mockup_output
    for line in output.splitlines():
        match = re.search(patterns, line)
        if match:
            match_flag = 1
            port_name = match.group(1)
            val1 = match.group(2).strip()
            val2 = match.group(3).strip()
            data = [port_name, val1, val2]
            if not first_data:
                first_data = data
            elif first_data[1:] != data[1:]:
                log.fail("Port data is different:{} <==> {}".format(first_data, data))
                err_count += 1
    if not match_flag:
        log.fail('Port data is not found')
        err_count += 1
    if err_count:
        raise Exception("verifyAllPortData failed")
    log.success('verifyAllPortData is passed\n')

@logThis
def changePortsStatus(port_cmd, timeout=30):
    device.sendMsg("\r\n")
    device.readMsg()
    for cmd in port_cmd.split("\n"):
        device.sendCmd(cmd)
        sleep(8)

@logThis
def changePortsStatusAndCheckPattern(port_cmd, patterns, timeout=100):
    changePortsStatus(port_cmd)
    is_negative_test = False
    if patterns == fail_pattern:
        is_negative_test = True
    finish_prompt = "{}[\s\S]+{}".format(port_cmd[:5], BCM_promptstr)
    output = device.read_until_regexp(finish_prompt, timeout=timeout)
    check_status = SdkCommonLib.checkOutput(output, patterns=patterns, is_negative_test=is_negative_test)
    if not check_status:
        raise Exception("Execute {} failed.".format(port_cmd))

@logThis
def checkBcmVersion():
    output = device.executeCommand('version', BCM_promptstr)
    version = parseBcmVersion(output)
    if version == BCM_VERSION:
        log.info('check bcm version successfully.')
    else:
        raise RuntimeError('check bcm version failed!')

@logThis
def parseBcmVersion(output):
    for line in output.splitlines():
        match = re.search('Release: sdk-(\d+.\d+.\d+) built', line)
        if match:
            return match.group(1).strip()
    raise RuntimeError('Can not parse bcm version from output!')

@logThis
def toLtMode():
    device.sendCmd('dsh')

@logThis
def checkPciePhyFwInfo():
    output = device.executeCommand('PCIEphy fwinfo', SDKLT_PROMPT)
    versions = SwImage.getSwImage('TH4_PCIE_FLASH').newVersion
    parsed_output = CommonLib.parse_fw_version(output)
    err_count = CommonLib.compare_input_dict_to_parsed(parsed_output, versions)
    if err_count:
        raise RuntimeError("Failure while verify_fw_version with result FAIL")

@logThis
def verifyPrbsBer():
    output = CommonLib.run_cmd(prbs_stat_cmd, SDKLT_PROMPT)
    SdkCommonLib.check_port_ber(output, BER_PORT_PATTERN, PORT_BER_TOLERANCE)

# @logThis
# def bcmSleep(seconds):
#     output = device.executeCommand('sleep ' + seconds, BCM_promptstr)
#     check_status = SdkCommonLib.checkOutput(output, patterns='Sleeping for {} seconds'.format(seconds))
#     if not check_status:
#         raise Exception("Execute {} failed.".format('sleep'))

@logThis
def execCintCmd(cmd):
    device.sendCmd('cint')
    device.executeCommand(cmd + ';', CINT_PROMPT)
    device.sendCmd('quit;')

@logThis
def updatePcieFw():
    output = device.executeCommand('pciephy fwload {}'.format(SwImage.getSwImage('TH4_PCIE_FLASH').newImage), SDKLT_PROMPT)
    success = SdkCommonLib.checkOutput(output, patterns=['PCIE firmware updated successfully'])
    if success:
        log.success('updatePcieFw successfully.')
    else:
        raise RuntimeError('updatePcieFw failed!')

@logThis
def toShellMode():
    device.sendCmd('shell', device.promptDiagOS)

@logThis
def test10gKR():
    output = device.executeCmd(test_10gkr_cmd)
    device.sendCmd('exit')
    if re.search(test_10gkr_pass_pattern, output):
        log.success('test0gKR successfully.')
    else:
        raise RuntimeError('test0gKR failed!')

@logThis
def checkPhyInfo():
    output = device.executeCommand('phy info', SDKLT_PROMPT)
    CommonKeywords.should_match_ordered_regexp_list(output, phy_info_pattern)
    log.success('checkPhyInfo successfully.')

@logThis
def checkCommonUcodeVersion():
    output = device.executeCommand('phy diag 1-262 dsc', SDKLT_PROMPT, timeout=900)
    for line in output.splitlines():
        match = re.search(common_ucode_pattern, line)
        if match:
            version = match.group(1)
            if version != common_ucode_version:
                log.info('line: ' + line)
                raise RuntimeError('the version found: {} does not match expected: {}'.format(version, common_ucode_version))
    log.success('checkCommonUcodeVersion successfully.')

@logThis
def exitSdkRemote():
    CommonLib.run_cmd(cls_shell_exit, device.promptDiagOS)
    if SdkCommonLib.findBcmProcess():
        SdkCommonLib.stopBcmProcess()
        raise RuntimeError('exitSdkRemote failed!')
    else:
        log.success('exitSdkRemote successfully.')


@logThis
def CheckPciePhyFwInfoForShamu():
    output = device.executeCommand('PCIEphy fwinfo', SDKLT_PROMPT)
    versions = SwImage.getSwImage('PCIE_FLASH_SHAMU').newVersion
    parsed_output: object = CommonLib.parse_fw_version(output)
    err_count = CommonLib.compare_input_dict_to_parsed(parsed_output, versions)
    if err_count:
        raise RuntimeError("Failure while verify_fw_version with result FAIL")


@logThis
def updatePcieFwForShamu():
    output = device.executeCommand('pciephy fwload {}'.format(SwImage.getSwImage('PCIE_FLASH_SHAMU').newImage), SDKLT_PROMPT)
    success = SdkCommonLib.checkOutput(output, patterns=['PCIE firmware updated successfully'])
    if success:
        log.success('updatePcieFw successfully.')
    else:
        raise RuntimeError('updatePcieFw failed!')


@logThis
def VerifyPrbsBerForShamu():
    output = CommonLib.run_cmd(prbs_stat_cmd_for_shamu, BCM_promptstr)
    SdkCommonLib.check_port_ber(output, BER_PORT_PATTERN, PORT_BER_TOLERANCE_FOR_SHAMU)


@logThis
def CheckCommonUcodeVersionForShamu():
    output = device.executeCommand('dsh -c "phy diag 1-69 dsc"', BCM_promptstr, timeout=900)
    for line in output.splitlines():
        match = re.search(common_ucode_pattern, line)
        if match:
            version = match.group(1)
            if version != common_ucode_version_for_shamu:
                log.info('line: ' + line)
                raise RuntimeError('Failed,serdes Ucode version is {} does not match expected: {}'.format(version, common_ucode_version_for_shamu))
    log.success('Each port serdes Ucode version is {},version info check successfully.'.format(common_ucode_version_for_shamu))


@logThis
def CheckLaneConfigInformationForShamu():
    output = device.executeCommand('dsh -c "phy diag 1-69 dsc config"', BCM_promptstr, timeout=900)
    for line in output.splitlines():
        match = re.search(error_pattern, line)
        if match:
            raise RuntimeError('Failed,error or fail info appears in this lane configuration information.')
    log.success('Check all port lane configuration information successfully,not found any error!')

@logThis
def Test10gKRForShamu():
    output = device.executeCmd(test_10gkr_cmd_for_shamu)
    # device.sendCmd('exit')
    if re.search(test_10gkr_pass_pattern_kr_test_for_shamu, output):
        log.success('test10gKR successfully.')
    else:
        raise RuntimeError('test10gKR failed!')


@logThis
def VerifyRemoteSDKVersionForShamu():
    device.executeCmd('killall -9 bcm.user')
    device.executeCmd('./auto_load_user.sh bcm56780_a0-generic-40x200.config.yml -d')
    device.executeCmd('chmod 777 /usr/local/bin/cel_bcmshell')
    background_test = device.executeCmd('cel_bcmshell version')
    if background_test:
        log.success('SDK is already running in the background of the OS.')
        output = device.executeCmd(cls_shell_sdk_version)
        if re.search(test_remote_SDK_version_test_for_shamu, output):
            log.success('SDK version check successfully.')
        else:
            raise RuntimeError('SDK version check failed!')
    else:
        raise RuntimeError('cel_bcmshell test appear error!')


@logThis
def ExitSDKRemoteForShamu():
    CommonLib.run_cmd(cls_shell_exit, device.promptDiagOS)
    if SdkCommonLib.findBcmProcess():
        SdkCommonLib.stopBcmProcess()
        raise RuntimeError('exitSDKRemote failed!')
    else:
        log.success('exitSdkRemote successfully.')


def SetSnakeVlanToAllPortsForShamu():
    return SdkLibAdapter.set_snake_vlan_to_all_ports(port_cmd=set_snake_vlan_200G_cmd_for_shamu)


def LetCPUSendPackagesForShamu():
    return SdkLibAdapter.let_CPU_send_packages(port_cmd=let_CPU_send_package_cmd_for_shamu, port_len='')


def StopTrafficForShamu():
    return SdkLibAdapter.stop_traffic(port_cmd=stop_traffic_cmd_for_shamu)


@logThis
def VerifyAllPortDataForShamu(patterns=port_TX_RX_pattern):
    err_count = 0
    match_flag = 0
    changePortsStatus(show_c_cd_cmd)
    finish_prompt = "{}[\s\S]+{}".format(show_c_cd_cmd[:5], BCM_promptstr)
    output = device.read_until_regexp(finish_prompt, timeout=300)
    for line in output.splitlines():
        match = re.search(patterns, line)
        if match:
            match_flag = 1
            port_name = match.group(1)
            val1 = match.group(2).strip()
            val2 = match.group(3).strip()
            if val1 != val2:
                log.fail("Port {} data is different:{} <==> {}".format(port_name, val1, val2))
                err_count += 1
    if not match_flag:
        log.fail('Port data is not found')
        err_count += 1
    if err_count:
        raise Exception("verifyAllPortData failed")
    log.success('verifyAllPortData is passed\n')


@logThis
def Set200GSocForShamu(port_cmd=set_snake_vlan_200G_cmd_for_shamu):
    patterns = fail_pattern
    output = device.executeCommand(port_cmd, BCM_promptstr, timeout=300)
    check_status = SdkCommonLib.checkOutput(output, patterns=patterns, is_negative_test=True)
    if not check_status:
        raise Exception("Execute {} failed.".format(port_cmd))


@logThis
def CheckPktCounterForShamu():
    due_prompt = 'XLMIB_TBYT'
    finish_prompt = "{}[\s\S]+{}".format(due_prompt, BCM_promptstr)
    output = device.sendCmdRegexp(show_c_cd_cmd, finish_prompt, timeout=300)
    # output = device.executeCommand(show_c_cmd, BCM_promptstr, timeout=300)
    log.cprint(output)
    lines = str(output).splitlines()
    linesIter = iter(lines)

    findMismatch = False

    def parsePktCounter(line, linesIter, txPattern, rxPattern):
        res = re.search(txPattern, line)
        if res:
            pktCount = res.group(2)
            log.info('pktCount: ' + pktCount)
            nextLine = next(linesIter, None)
            if nextLine is None:
                raise RuntimeError('Can not find the next line of Line: \n'.format(line))
            res = re.search(rxPattern, nextLine)
            if res:
                if pktCount != res.group(2):
                    nonlocal findMismatch
                    findMismatch = True
                    log.info('#########These two lines mismatch: ########## \n')
                    log.info('Line 1 : \n'.format(line))
                    log.info('Line 2 : \n'.format(nextLine))
            else:
                raise RuntimeError('Can not find pattern ' + rxPattern)

    while True:
        line = next(linesIter, None)
        if not line:
            break
        res = re.search(tx_rx_pkt_patterns[0], line)
        if not res:
            continue

        parsePktCounter(line, linesIter, tx_rx_pkt_patterns[0], tx_rx_pkt_patterns[1])
        line = next(linesIter).strip()
        parsePktCounter(line, linesIter, tx_rx_pkt_patterns[2], tx_rx_pkt_patterns[3])
        line = next(linesIter).strip()
        parsePktCounter(line, linesIter, tx_rx_pkt_patterns[4], tx_rx_pkt_patterns[5])
        line = next(linesIter).strip()
        parsePktCounter(line, linesIter, tx_rx_pkt_patterns[6], tx_rx_pkt_patterns[7])
        line = next(linesIter).strip()
        parsePktCounter(line, linesIter, tx_rx_pkt_patterns[8], tx_rx_pkt_patterns[9])

    if findMismatch:
        raise RuntimeError('Find mismatch lines !')
    else:
        log.success('checkPktCounter successfully.')


@logThis
def prepare_images_for_shamu_pcie(image_name, mode, host_base_dir=''):
    pcieImage = SwImage.getSwImage(image_name)
    pcieImage.hostBaseDir = host_base_dir
    CommonLib.create_dir(pcieImage.localImageDir, mode)
    CommonLib.get_dhcp_ip_address('DUT', 'eth0', mode)
    CommonLib.download_images('DUT', SwImage.PCIE_FLASH_SHAMU)
    device.executeCmd('chmod 777 /tmp/PCIE/Shamu_bcm56780_pciefw-r5-m7-v2.8.bin')
    device.executeCmd('cp -r /tmp/PCIE/Shamu_bcm56780_pciefw-r5-m7-v2.8.bin /usr/local/CPU_Diag/utility/Shamu_SDK')
