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
import re
import copy
from collections import OrderedDict
import Logger as log
import CRobot
from crobot import Const
from Decorator import *
from time import sleep

workDir = CRobot.getWorkDir()
sys.path.append(os.path.join(workDir, 'common', 'commonlib'))
sys.path.append(os.path.join(workDir, 'platform/kapok'))
from KapokOnieVariable import *
import CommonLib
from common.commonlib import CommonKeywords
import KapokCommonLib
import KapokConst
from crobot.SwImage import SwImage

try:
    from Device import Device
    import DeviceMgr
except Exception as err:
    log.cprint(str(err))

device = DeviceMgr.getDevice()
devicename = os.environ.get("deviceName", "")

def OnieConnect():
    log.debug("Entering OnieTestCase procedure: OnieConnect")
    device.loginOnie()
    return


def OnieDisconnect():
    global libObj
    log.debug("Entering OnieTestCase procedure: OnieDisconnect")
    device.disconnect()
    return

############### Onie related keywords begin
def displayOnieVersion():
    log.debug("Entering OnieLib class procedure: displayOnieVersion")
    return device.sendCmd("onie-sysinfo -v", device.promptOnie)

def fetchFileWithTftp(cmd, Image_item, mode, use_src_dir=False):
    log.debug("Entering OnieLib class procedure: fetchFileWithTftp")
    max_retry_cnt = 3
    cur_cnt = 0
    tftp_server_ip = CommonLib.get_device_info("PC").get("managementIP", "")
    Image_info_dict = CommonLib.get_swinfo_dict(Image_item)
    file_src_path = ""  # package under root path is latest version
    if use_src_dir:
        file_src_path = Image_info_dict.get("hostImageDir", "NotFound")
    file_dst_path = Image_info_dict.get("localImageDir", "NotFound")
    file_name = Image_info_dict.get("newImage", "NotFound")
    fetch_cmd = cmd.format(tftp_server_ip, os.path.join(file_src_path, file_name))
    for cur_cnt in range(max_retry_cnt):
        log.info("Loop cnt: " + str(cur_cnt+1))
        device.getPrompt(mode)
        device.sendMsg('cd '+file_dst_path+'\r\n')
        output = CommonLib.execute_command(fetch_cmd, mode=mode)
        match = re.search('(no such | fail | error)', output, re.I)
        if match:
            log.info('tftp fail, try again.')
            cur_cnt += 1
        else:
            log.info('Tftp successed from server')
            break
    if cur_cnt == max_retry_cnt:
        log.fail('Unkonw issue occurs.')

def getTheCurrentOniePartitionAndErase(MODE):
    log.debug("Entering OnieLib class procedure: getTheCurrentOniePartitionAndErase")
    cmd = display_onie_partition_cmd
    output = CommonLib.execute_check_dict('DUT', cmd, mode=MODE, patterns_dict=fail_dict,
                                          path=onie_file_local_path, timeout=5, is_negative_test=True)
    if output:
        onie_partition_match = re.search(onie_partition_pattern, output)
        if onie_partition_match:
            onie_partition = onie_partition_match.group(1)
            erase_cmd = onie_partition_erase_cmd.format(onie_partition)
            CommonLib.execute_check_dict('DUT', erase_cmd, mode=MODE, patterns_dict=onie_erase_pattern,
                                         path=onie_file_local_path, timeout=300)
            return onie_partition
        else:
            return "mtd4"
    else:
        raise Exception("Failed to display onie partition.")


def flashcpInstallOnie(onie_partition, MODE):
    log.debug("Entering OnieLib class procedure: flashcpInstallOnie")
    if ("tianhe" in devicename.lower()) or ("51.2t" in devicename.lower()) or ("tigrisv2" in devicename.lower()):
        output = CommonLib.execute_command(onie_partition, timeout=60)
        res = re.search(onie_partition_pattern, output)
        if res:
            onie_partition = res.group(1)
    Image_info_dict = CommonLib.get_swinfo_dict("ONIE_Installer")
    image_name = Image_info_dict.get("newImage", "NotFound")
    image_path = Image_info_dict.get("localImageDir", "NotFound")
    cmd = flashcp_upgrade_onie_cmd.format(image_name, onie_partition)
    CommonLib.execute_check_dict('DUT', cmd, mode=MODE, patterns_dict=fail_dict,
                                          path=image_path, timeout=600, is_negative_test=True)


def verifyOnieVersion():
    log.debug("Entering OnieLib class procedure: verifyOnieVersion")
    error_count = 0
    p1 = r'ONIE\s+([\d.]+)'
    cmd = get_versions_cmd
    Image_info_dict = CommonLib.get_swinfo_dict("ONIE_Installer")
    onie_version = Image_info_dict.get("newVersion", "NotFound")
    output = device.executeCmd(cmd, mode=Const.BOOT_MODE_ONIE, timeout=60)
    res = re.search(p1, output)
    if res:
        getOnieVer = res.group(1)
        if getOnieVer == onie_version:
            log.success('successfully match onie version, getVer: %s, expectVer: %s'%(getOnieVer, onie_version))
        else:
            error_count += 1
            log.fail('Verify onie version fail, getVer: %s, expectVer: %s'%(getOnieVer, onie_version))
    else:
        error_count += 1
        log.fail('Onie version match fail!')
    if error_count > 0:
        raise Exception('Failed run verifyOnieVersion')
    #onie_version_pattern = { "ONIE  %s"%(onie_version): "^ONIE\s+%s"%(onie_version)}
    #CommonLib.execute_check_dict('DUT', cmd, mode=Const.BOOT_MODE_ONIE, patterns_dict=onie_version_pattern, timeout=6)

@logThis
def onieUpdateCurrentVersion(onie_self_update_current_ver_cmd):
    flag = False
    device.sendMsg(onie_self_update_current_ver_cmd + " \n")
    output = device.read_until_regexp(KapokConst.STOP_AUTOBOOT_PROMPT, timeout=2000)
    for each in output.splitlines():
        if each == "The FW version you upgrade is same to the previous version!":
            flag = True
            break
    if ("tianhe" in devicename.lower()) or ("51.2t" in devicename.lower()) or ("tigrisv2" in devicename.lower()):
        # enter onie
        device.sendMsg(KapokConst.STOP_AUTOBOOT_KEY)
        device.sendMsg(ubootDefaultTool1 + '\n')
        device.sendMsg(ubootDefaultTool2 + '\n')
        device.sendMsg(ubootDefaultTool3 + '\n')
        device.read_until_regexp(ACTIVATE_CONSOLE_PROMPT, timeout=500)
        device.sendMsg("\n")
        onie_discovery_stop_cmd = KapokConst.STOP_ONIE_DISCOVERY_KEY
        device.sendCmdRegexp(onie_discovery_stop_cmd, device.promptOnie, timeout=60)
        check_cpld_fw_in_onie_update(output)
    else:
        pass1 = output.splitlines().count("| PASS! |")
        pass2 = len(re.findall("[+].*PASS.*[+]",output))
        if pass1 == 3 and pass2 ==2 and flag==True:
            log.success("ONIE can be updated from current version to current version.")
            log.info("======================= Expected OUTPUT =========================")
            log.info("3 occurence of '| PASS! |'")
            log.info("2 occurence of '+  PASS  +'")
            log.info("======================= Expected OUTPUT =========================")
        else:
            log.fail("Error in updating ONIE from current version to current version.")

@logThis
def onieUpdateHigherVersion():
    updater_info_dict = CommonLib.get_swinfo_dict("ONIE_higher")
    filename = updater_info_dict.get("newImage", "NotFound")
    file_path = updater_info_dict.get("hostImageDir", "NotFound")
    server_ip = CommonLib.get_device_info("PC").get("managementIP","")
    log.debug("Prompt: {}".format(device.promptOnie))
    if not server_ip:
        raise Exception("Didn't find server IP.")
    updater_cmd = "onie-self-update tftp://{}/{}".format(server_ip, os.path.join(file_path, filename))
    if "tianhe" in devicename.lower():
        expect_message = ACTIVATE_CONSOLE_PROMPT
    else:
        expect_message = KapokConst.ONIE_DISCOVERY_PROMPT
    timeout_message = "tftp: timeout|tftp: read error"
    finish_prompt = "{}|{}".format(expect_message, timeout_message)
    retry = 3
    for i in range(retry):
        output = device.sendCmdRegexp(updater_cmd, finish_prompt, timeout=2000)
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

@logThis
def check_onie_higher_version():
    cmd='get_versions'+' \n'
    Image_info_dict = CommonLib.get_swinfo_dict("ONIE_higher")
    onie_version = Image_info_dict.get("newVersion", "NotFound")
    onie_version_pattern = { "ONIE  %s"%(onie_version): "^ONIE\s+%s"%(onie_version)}

    CommonLib.execute_check_dict('DUT', cmd, mode=Const.BOOT_MODE_ONIE, patterns_dict=onie_version_pattern,
                                 timeout=10)

@logThis
def check_onie_latest_version():
    error_count = 0
    p1 = r'ONIE[ \t]+([\d\.]+)'
    log.info('Switch to onie rescue mode firstly!')
    KapokCommonLib.bootIntoOnieRescueMode()
    cmd='get_versions'
    # device.sendMsg(cmd)
    output = device.executeCmd(cmd, timeout=60)
    res = re.search(p1, output)
    if res:
        currentVersion = res.group(1)
        if currentVersion == onieNewVer:
            log.info('Get current onie version is %s'%currentVersion)
        else:
            log.info('Get version is diff, GetVer: %s, ExpectVer: %s'%(currentVersion, onieNewVer))
            log.info('#### need to update to current latest version %s ####'%onieNewVer)
            onieUpdateCurrentVersion(onieCurrentImgCmd)
    else:
        error_count += 1
        log.fail('Can not get the current latest onie version.')
    if error_count > 0:
        raise Exception('Failed run check_onie_latest_version')

@logThis
def check_onie_current_version():
    error_count = 0
    p1 = r'ONIE[ \t]+([\d\.]+)'
    #log.info('Switch to onie rescue mode firstly!')
    #KapokCommonLib.bootIntoOnieRescueMode()
    cmd='get_versions'
    # device.sendMsg(cmd)
    output = device.executeCmd(cmd, timeout=60)
    res = re.search(p1, output)
    if res:
        currentVersion = res.group(1)
        if currentVersion == onieNewVer:
            log.info('Get current onie version is %s'%currentVersion)
        else:
            error_count += 1
            log.fail('Get version is diff, GetVer: %s, ExpectVer: %s'%(currentVersion, onieNewVer))
    else:
        error_count += 1
        log.fail('Can not get the current onie version.')
    if error_count > 0:
        raise Exception('Failed run check_onie_current_version')

@logThis
def onieUpdateProductionVersion():
    updater_info_dict = CommonLib.get_swinfo_dict("ONIE_production")
    filename = updater_info_dict.get("newImage", "NotFound")
    file_path = updater_info_dict.get("hostImageDir", "NotFound")
    server_ip = CommonLib.get_device_info("PC").get("managementIP","")
    log.debug("Prompt: {}".format(device.promptOnie))
    if not server_ip:
        raise Exception("Didn't find server IP.")
    updater_cmd = "onie-self-update tftp://{}/{}".format(server_ip, os.path.join(file_path, filename))
    if "tianhe" in devicename.lower():
        expect_message = ACTIVATE_CONSOLE_PROMPT
    else:
        expect_message = KapokConst.ONIE_DISCOVERY_PROMPT
    timeout_message = "tftp: timeout|tftp: read error"
    finish_prompt = "{}|{}".format(expect_message, timeout_message)
    retry = 3
    for i in range(retry):
        output = device.sendCmdRegexp(updater_cmd, finish_prompt, timeout=2000)
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

@logThis
def onieUpdateCustomerVersion():
    updater_info_dict = CommonLib.get_swinfo_dict("ONIE_customer")
    filename = updater_info_dict.get("newImage", "NotFound")
    file_path = updater_info_dict.get("hostImageDir", "NotFound")
    server_ip = CommonLib.get_device_info("PC").get("managementIP","")
    log.debug("Prompt: {}".format(device.promptOnie))
    if not server_ip:
        raise Exception("Didn't find server IP.")
    updater_cmd = "onie-self-update tftp://{}/{}".format(server_ip, os.path.join(file_path, filename))
    if "tianhe" in devicename.lower():
        expect_message = ACTIVATE_CONSOLE_PROMPT
    else:
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

@logThis
def check_onie_production_version():
    cmd='get_versions'+' \n'
    Image_info_dict = CommonLib.get_swinfo_dict("ONIE_production")
    onie_version = Image_info_dict.get("newVersion", "NotFound")
    onie_version_pattern = { "ONIE  %s"%(onie_version): "^ONIE\s+%s"%(onie_version)}

    CommonLib.execute_check_dict('DUT', cmd, mode=Const.BOOT_MODE_ONIE, patterns_dict=onie_version_pattern,
                                 timeout=10)


@logThis
def check_onie_customer_version():
    cmd='get_versions'+' \n'
    Image_info_dict = CommonLib.get_swinfo_dict("ONIE_customer")
    onie_version = Image_info_dict.get("newVersion", "NotFound")
    onie_version_pattern = { "ONIE  %s"%(onie_version): "^ONIE\s+%s"%(onie_version)}

    CommonLib.execute_check_dict('DUT', cmd, mode=Const.BOOT_MODE_ONIE, patterns_dict=onie_version_pattern,
                                 timeout=10)


def verifyOnieAndCPLDVersion(version="new"):
    log.debug("Entering OnieLib class procedure: verifyOnieAndCPLDVersion")
    escapeString = CommonLib.escapeString

    cmd = get_versions_cmd
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

def verifyOnieSysInfo():
    log.debug("Entering OnieLib class procedure: verifyOnieSysInfo")

    cmd = get_sys_info_cmd
    path = diag_bin_path
    Image_info_dict = CommonLib.get_swinfo_dict("ONIE_Installer")
    onie_version = Image_info_dict.get("newVersion", "NotFound")
    onie_version_pattern = { "ONIE  %s"%(onie_version): "^ONIE\s+%s"%(onie_version)}

    CommonLib.execute_check_dict('DUT', cmd, mode=Const.BOOT_MODE_ONIE, patterns_dict=sys_info_pass_pattern,
                                 path=path, timeout=6)


def clearImageFile(item_name, mode=Const.ONIE_RESCUE_MODE):
    log.debug("Entering OnieLib class procedure: clearImageFile")

    Image_info_dict = CommonLib.get_swinfo_dict(item_name)
    image_name = Image_info_dict.get("newImage", "NotFound")
    image_path = Image_info_dict.get("localImageDir", "NotFound")

    cmd = "rm {}".format(os.path.join(image_path, image_name))
    CommonLib.execute_check_dict('DUT', cmd, mode=mode, patterns_dict=fail_dict,
                                 timeout=6, is_negative_test=True)


def getDhcpIP(interface="eth0", mode=Const.BOOT_MODE_DIAGOS):
    log.debug("Entering OnieLib class procedure: getDhcpIP")
    devicename = os.environ.get("deviceName", "")
    if  "tianhe" in devicename.lower():
        cmd = "udhcpc eth0"
    else:
        cmd = "dhclient"
    CommonLib.execute_check_dict('DUT', cmd, mode=mode, patterns_dict=fail_dict,
                                 timeout=60, is_negative_test=True)


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


def run_command(cmd, mode=None, timeout=60, CR=True):
    log.debug("Entering OnieLib class procedure: run_command")

    prompt_dict = { Const.BOOT_MODE_UBOOT  : device.promptUboot,
                    Const.BOOT_MODE_ONIE   : device.promptOnie,
                    Const.BOOT_MODE_DIAGOS : device.promptDiagOS
            }
    if not mode:
        mode = device.currentBootMode
    promptStr = prompt_dict.get(mode, "")
    if isinstance(cmd, str):
        cmd_list = [ cmd ]
    elif isinstance(cmd,list):
        cmd_list = cmd
    else:
        raise Exception("run_command not support run {}".format(type(cmd)))
    output = ""
    for cmdx in cmd_list:
        due_prompt = cmdx.lstrip()[:5]
        finish_prompt = "{}[\s\S]+{}".format(due_prompt, promptStr)
        if CR:
            cmdx += "\n"
        device.sendMsg(cmdx)
        output += device.read_until_regexp(finish_prompt, timeout=timeout)

    return output

@logThis
@timeThis
def setUbootIP():
    uboot_ip = CommonLib.Get_Not_Occupied_IP()
    server_ip = CommonLib.get_device_info("PC").get("managementIP","")
    set_uboot_ip_cmd = "setenv ipaddr {}".format(uboot_ip)
    set_server_ip_cmd = "setenv serverip {}".format(server_ip)
    check_connective_cmd = "ping {}".format(server_ip)
    cmd_list = [set_uboot_ip_cmd, set_server_ip_cmd, check_connective_cmd, " "]
    output = ""
    for cmd in cmd_list:
        output += run_command(cmd, mode=Const.BOOT_MODE_UBOOT, timeout=10)

    check_pattern = {"host ... is alive": "host.*?is alive"}

    CommonLib.execute_check_dict(Const.DUT, "", patterns_dict=check_pattern, check_output=output)
    devicename = os.environ.get("deviceName", "")
    #if  "tianhe" in devicename.lower():
        #run_command("sf erase 0x1000000 +$filesize && sf write 0xa0000000 0x1000000 $filesize", mode=Const.BOOT_MODE_UBOOT, timeout=300)


def installOnieUnderUboot():
    log.debug("Entering OnieLib class procedure: installOnieUnderUboot")
    onie_file = CommonLib.get_swinfo_dict("ONIE_Installer").get("newImage", "NotFound")
    set_onie_file_cmd = "setenv oniefile {}".format(onie_file)
    run_upload_onie_cmd = "run uploadonie"
    sf_probe_cmd = "sf probe 0"
    sf_read_cmd = "sf read ${loadaddr} ${onieflashaddr} ${onie_sz.b}"
    set_boot_args_cmd = "setenv bootargs console=$consoledev,$baudrate onie_dhcp=eth0"
    devicename = os.environ.get("deviceName", "")
    dev_type = DeviceMgr.getDevice(devicename).get('cardType')
    # if  "tianhe" in devicename.lower():
    #     if dev_type == '1PPS':
    #         set_onie_boot_args_cmd = "setenv onie_bootm_args '#celestica_cs8274_12v_21'"
    #         set_dtb_file_cmd = 'setenv dtb_file celestica_cs8274-r0_12v_21.dtb'
    #         set_sf_read_cmd = 'sf read 0x80001000 0xd00000 0x100000; env exists mcinitcmd && fsl_mc lazyapply dpl 0x80001000'
    #     else:
    #         set_onie_boot_args_cmd = "setenv onie_bootm_args '#celestica_cs8264_12v_21'"
    #         set_dtb_file_cmd =  'setenv dtb_file celestica_cs8264-r0_12v_21.dtb'
    # else:
    if "fenghuangv2" in devicename.lower():
        if dev_type == '1PPS':
            set_onie_boot_args_cmd = "setenv onie_bootm_args '#celestica_cs8260_12v_21_1PPS'"
            set_dtb_file_cmd =  'setenv dtb_file celestica_cs8260-r0_12v_21_1PPS.dtb'
        else:
            set_onie_boot_args_cmd = "setenv onie_bootm_args '#celestica_cs8260_12v_21'"
            set_dtb_file_cmd =  'setenv dtb_file celestica_cs8260-r0_12v_21.dtb'
    bootm_cmd = "bootm ${loadaddr}${onie_bootm_args}\n"
    # if "tianhe" in devicename.lower():
    #     cmd_list = [PRINT_VER_CMD, set_onie_file_cmd, run_upload_onie_cmd, sf_probe_cmd,
    #                 sf_read_cmd, set_boot_args_cmd, set_onie_boot_args_cmd, set_dtb_file_cmd, set_sf_read_cmd]
    # else:
    if "fenghuangv2" in devicename.lower():
        cmd_list = [PRINT_VER_CMD, set_onie_file_cmd, run_upload_onie_cmd, sf_probe_cmd,
                sf_read_cmd, set_boot_args_cmd, set_onie_boot_args_cmd, set_dtb_file_cmd]
    else:
        cmd_list = [PRINT_VER_CMD, set_onie_file_cmd, run_upload_onie_cmd]
    output = ""
    for cmd in cmd_list:
        if cmd == run_upload_onie_cmd:
            upload_log = ""
            for i in range(3):
                upload_log = run_command(cmd, mode=Const.BOOT_MODE_UBOOT, timeout=600)
                if not "Failed" in upload_log:
                    break
            output += upload_log
        else:
            # if "tianhe" in devicename.lower():
            #     output += run_command(cmd, mode=Const.BOOT_MODE_UBOOT, timeout=1200)
            # else:
            output += run_command(cmd, mode=Const.BOOT_MODE_UBOOT, timeout=60)
    if "fenghunagv2" in devicename.lower():
        device.sendMsg(bootm_cmd)
    else:
        device.sendMsg(ubootDefaultTool3 + '\n')
    CommonLib.execute_check_dict(Const.DUT, "", patterns_dict=fail_dict, check_output=output, is_negative_test=True)
    device.read_until_regexp(ACTIVATE_CONSOLE_PROMPT, timeout=KapokConst.BOOT_TIME)
    device.sendMsg("\n")
    onie_discovery_stop_cmd = KapokConst.STOP_ONIE_DISCOVERY_KEY
    device.sendCmdRegexp(onie_discovery_stop_cmd, device.promptOnie, timeout=10)

@logThis
def get_onie_image_name(update="new"):
    ## only get the image name
    updater_info_dict = CommonLib.get_swinfo_dict("ONIE_updater")
    if update == "new":
        filename = updater_info_dict.get("newImage", "NotFound")
    else:
        filename = updater_info_dict.get("oldImage", "NotFound")
    return filename

@logThis
def get_onie_image(update="new"):
    ## the image include path and image name
    updater_info_dict = CommonLib.get_swinfo_dict("ONIE_updater")
    if update == "new":
        filename = updater_info_dict.get("newImage", "NotFound")
        file_path = updater_info_dict.get("hostImageDir", "NotFound")
    else:
        filename = updater_info_dict.get("oldImage", "NotFound")
        file_path = updater_info_dict.get("oldhostImageDir", "NotFound")
    onieImg = file_path + '/' + filename
    return onieImg

@logThis
def onie_self_update_test(imgType="new"):
    #1. get onie image
    getOnieImg = get_onie_image(imgType)
    #2. update onie
    update_cmd = onieSelfUpdateTool + ' tftp://' + server_ipv4 + '/' + getOnieImg
    stopAutoUboot = KapokConst.STOP_AUTOBOOT_PROMPT
    output = device.sendCmdRegexp(update_cmd, stopAutoUboot, timeout=1800)
    device.sendMsg(KapokConst.STOP_AUTOBOOT_KEY)
    device.sendMsg(ubootDefaultTool1 + '\n')
    device.sendMsg(ubootDefaultTool2 + '\n')
    device.sendMsg(ubootDefaultTool3 + '\n')
    device.read_until_regexp(stopAutoUboot, KapokConst.BOOT_TIME)
    device.sendMsg(KapokConst.STOP_AUTOBOOT_KEY)
    device.sendMsg(switch_onie_mode_cmd['rescue'] + '\n')
    device.read_until_regexp(ACTIVATE_CONSOLE_PROMPT, KapokConst.BOOT_TIME)
    device.sendMsg("\n")
    onie_discovery_stop_cmd = KapokConst.STOP_ONIE_DISCOVERY_KEY
    device.sendCmdRegexp(onie_discovery_stop_cmd, device.promptOnie, timeout=10)
    #3. check cpld info
    check_cpld_fw_in_onie_update(output)

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


def autoUpdateInUpdateMode():
    log.debug("Entering OnieLib class procedure: autoUpdateInUpdateMode")

    device.getPrompt(Const.BOOT_MODE_UBOOT)
    log.info("Beginning to switch to ONIE update mode to do self updating...")
    device.sendMsg("run onie_update\n")
    device.readUntil("Updating CPLDs", timeout=600)
    device.read_until_regexp(KapokConst.STOP_AUTOBOOT_PROMPT, timeout=KapokConst.BOOT_TIME)
    device.read_until_regexp(KapokConst.ONIE_DISCOVERY_PROMPT, timeout=KapokConst.BOOT_TIME)
    device.sendMsg("\n")
    device.sendMsg(KapokConst.STOP_ONIE_DISCOVERY_KEY)
    device.read_until_regexp(device.promptOnie, timeout=10)

@logThis
def fhv2autoUpdateInUpdateMode():
    device.getPrompt(Const.BOOT_MODE_UBOOT)
    log.info("Beginning to switch to ONIE update mode to do self updating...")
    device.sendMsg("run onie_update\n")
    output = device.read_until_regexp(KapokConst.STOP_AUTOBOOT_PROMPT, timeout=KapokConst.UPDATE_TIME)
    if "tianhe" in devicename.lower() or "tigrisv2" in devicename.lower() or "51.2t" in devicename.lower():
        device.sendMsg('123\r')
        device.sendMsg(ubootDefaultTool1 + '\n')
        device.sendMsg(ubootDefaultTool2 + '\n')
        device.sendMsg(ubootDefaultTool3 + '\n')
    device.read_until_regexp(KapokConst.ONIE_DISCOVERY_PROMPT, timeout=KapokConst.UPDATE_TIME)
    device.sendMsg("\n")
    log.info('#### Run command [%s]. ####' % KapokConst.STOP_ONIE_DISCOVERY_KEY)
    device.sendMsg(KapokConst.STOP_ONIE_DISCOVERY_KEY)
    device.read_until_regexp(device.promptOnie, timeout=10)
    if "tianhe" in devicename.lower() or "tigrisv2" in devicename.lower() or "51.2t" in devicename.lower():
        check_cpld_fw_in_onie_update(output)

@logThis
def check_cpld_fw_in_onie_update(output):
    error_count = 0
    pass1 = output.splitlines().count("| PASS! |")
    pass2 = len(re.findall("[+].*PASS.*[+]", output))
    fail1 = output.splitlines().count("| FAIL! |")
    fail2 = len(re.findall("[+].*FAIL.*[+]", output))
    #pass_percentage = len(re.findall(r'\[100%\]', output))
    if fail1 or fail2:
        error_count += 1
        log.fail('Find onie update fail, pls see update log.')
    else:
        pass_num = pass1 + pass2
        #if pass_percentage == pass_num and pass_num >= 10:
        if pass_num >= 9:
            log.success('onie update successfully!')
            log.info('####################################################################')
            log.info('Check cpld/fpga update status when onie update:')
            log.info('Total pass num is %d' % pass_num)
            log.info('####################################################################')
        else:
            error_count += 1
            log.fail('Find to update fail info.')
    if error_count:
        raise Exception('Failed run onie_self_update_test')

def checkBootingOutput(mode=None):
    log.debug("Entering OnieLib class procedure: checkBootingOutput")

    detect_prompt = {"installer": INSTALLER_MODE_DETECT_PROMPT,
                     "update"  : UPDATE_MODE_DETECT_PROMPT,
                     "rescue"   :  RESCUE_MODE_DETECT_PROMPT,
                     "Uninstall": UNINSTALL_MODE_DETECT_PROMPT
            }
    if mode == "Uninstall":
        output = device.read_until_regexp(KapokConst.STOP_AUTOBOOT_PROMPT, timeout=KapokConst.BOOT_TIME)
        device.sendMsg("{}\n".format(KapokConst.STOP_AUTOBOOT_KEY))
        output += device.read_until_regexp(device.promptUboot, timeout=10)
    else:
        output = device.read_until_regexp(ACTIVATE_CONSOLE_PROMPT, timeout=KapokConst.BOOT_TIME)
        device.sendMsg("\n")
        output += device.read_until_regexp(device.promptOnie, timeout=10)

    updater_info = CommonLib.get_swinfo_dict("ONIE_updater")
    onie_version = updater_info.get("newVersion", "NotFound")
    check_pattern = {"Version : %s"%onie_version: "Version.*?%s"%onie_version }
    expect_prompt = detect_prompt.get(mode, "NotFound")
    check_pattern.update({ expect_prompt: expect_prompt })

    CommonLib.execute_check_dict("DUT", "", patterns_dict=check_pattern,
                                 timeout=60, check_output=output)


def switchAndCheckOutput(mode):
    log.debug("Entering OnieLib class procedure: switchAndCheckOutput")

    switch_cmd = switch_onie_mode_cmd.get(mode, "NotFound")
    if switch_cmd == "powerCycle":
        device.powerCycleDevice()
    else:
        device.sendMsg(switch_cmd)
        device.sendMsg("\n")

    checkBootingOutput(mode)


def switchAndCheckBooting(mode, pattern_dict=AUTO_DISCOVERY_PATTERN, save_log=False,
                            finish_prompt=ACTIVATE_CONSOLE_PROMPT, negative_check=True):
    log.debug("Entering OnieLib class procedure: switchAndCheckBooting")
    switch_cmd = switch_onie_mode_cmd.get(mode, "NotFound")
    if switch_cmd == "powerCycle":
        device.powerCycleDevice()
    else:
        device.getPrompt(Const.BOOT_MODE_UBOOT)
        device.sendMsg(switch_cmd)
        device.sendMsg("\n")
    output = device.read_until_regexp(finish_prompt, timeout=600)
    #if "tianhe" in devicename.lower():
    #    p1 = 'discover: Rescue mode detected. No discover stopped.'
    #    res = re.search(p1, output)
    #    if res:
    #        log.success('switch to onie rescue successfully.')
    #    else:
    #        raise Exception('Found fail or error info!')
    #else:
    if save_log:
        with open(server_tmp_file, "w") as fh:
            fh.write(output)
    if pattern_dict:
        pattern_dict = CommonLib.filter_passpattern('onie_tc14', pattern_dict)
        CommonLib.execute_check_dict("DUT", "", patterns_dict=pattern_dict,
                                     timeout=60, check_output=output, is_negative_test=negative_check)
    return output


@logThis
def checkSearchOrder(output, search_pattern=None):
    result_list = []
    for pattern in search_pattern:
        result_list.append( {pattern : []} )

    for i, line in enumerate(output.splitlines()):
        for item in result_list:
            pattern = list(item.keys())[0] + " \.\.\."
            if re.search(pattern, line):
                list(item.values())[0].append(i)

    result_list.sort(key=lambda x: list(x.values())[0])
    pattern_order = [list(x.keys())[0] for x in result_list]
    for i in range(len(search_pattern)):
        if search_pattern[i] != pattern_order[i]:
            error_message = "Search index {} should be {}, but got {} first".format(search_pattern[i],
                            pattern_order[i])
            raise Exception(error_message)
    log.info("searched order: {}".format(pattern_order))


@logThis
def checkFileSearchOrder(mode, search_pattern):

    output = switchAndCheckBooting(mode, pattern_dict={}, finish_prompt=INSTALLER_SLEEPING_PATTERN)
    checkSearchOrder(output, search_pattern=search_pattern)


@logThis
def checkRescueDiscoveryStop():

    switchAndCheckBooting("rescue", pattern_dict=DISCOVERY_STOP_PATTERN,
                          finish_prompt=ACTIVATE_CONSOLE_PROMPT, negative_check=False)

def switchToDiagOS():
    log.debug("Entering OnieLib class procedure: switchToDiagOS")

    KapokCommonLib.bootIntoDiagOSMode()

def parseSyseeprom(output):
    log.debug("Entering OnieLib class procedure: parseSyseeprom")

    backup_value = copy.deepcopy(TLV_Value_Test1)
    for key, value in backup_value.items():
        backup_value[key][1] = ""

    item_num = 0
    for key, value in backup_value.items():
        pattern = "{}\s+{}\s+\d+\s+(.*)$".format(key, value[0].replace(".", "\."))
        match = re.search(pattern, output, re.M)
        if match:
            backup_value[key][1] = match.group(1).strip()
            item_num += 1
        else:
            log.info("Not found: {}".format(key))

    if  item_num == 0:
        return {}
    else:
        return backup_value


def saveDUTInfoToServer(cmd_list, mode=Const.ONIE_RESCUE_MODE,
                              server_file=server_tmp_file):
    log.debug("Entering OnieLib class procedure: saveDUTInfoToServer")

    output = ""
    for cmd in cmd_list:
        output += CommonLib.execute_command(cmd, mode=mode)
    with open(server_file, "w") as fh:
        fh.write(output)
    log.info("Saved printout to server file: {}".format(server_file))


def parseSingleValue(output, pattern):
    log.debug("Entering OnieLib class procedure: parseSingleValue")

    match = re.search(pattern, output, re.M)
    parsed_value = ""
    if match:
        parsed_value = match.group(1).strip()

    return parsed_value


def backupSyseepromAndWriteProtectValue():
    log.debug("Entering OnieLib class procedure: backupSyseepromAndWriteProtectValue")

    cmd_list = [ONIE_SYSEEPROM_CMD, QUERY_EEPROM_WRITE_PROTECTION_CMD]
    saveDUTInfoToServer(cmd_list)


def restoreSyseepromAndWriteProtectValue():
    log.debug("Entering OnieLib class procedure: restoreSyseepromAndWriteProtectValue")

    saved_log = ""
    with open(server_tmp_file, 'r') as fh:
        saved_log = fh.read()

    TLV_Value_dict = parseSyseeprom(saved_log)
    Write_Protect_Value = parseSingleValue(saved_log, VALUE_PATTERN)
    restore_flag = 0
    if TLV_Value_dict:
        enableEepromWrite()
        writeTlvValueToEeprom(TLV_Value_dict)
        restore_flag += 1
        log.info("TLV EEPROM values are restored.")
    else:
        log.error("TLV EEPROM values restoring failed.")

    if Write_Protect_Value:
        disableEepromWrite(Write_Protect_Value)
        log.info("Closing EEPROM write successfully.")
        restore_flag += 1
    else:
        log.error("Closing EEPROM write failed.")



def getOnieTlvValue():
    log.debug("Entering OnieLib class procedure: getOnieTlvValue")

    output = CommonLib.execute_command(ONIE_SYSEEPROM_CMD, mode=Const.ONIE_RESCUE_MODE)
    backup_value = parseSyseeprom(output)
    if backup_value:
        log.info("{} is got.".format(backup_value))
    else:
        raise Exception("Got EEPROM TSV value failed")

    return backup_value


def checkOnieTlvValueExisted():
    log.debug("Entering OnieLib class procedure: checkOnieTlvValueExisted")

    tlv_value_dict = getOnieTlvValue()
    null_list = []
    for key, value in tlv_value_dict.items():
        if not value[1]:
            null_list.append(key)
    if null_list:
        log.info("TLV value is not got in items: {}".format(null_list))


def enableEepromWrite():
    log.debug("Entering OnieLib class procedure: enableEepromWrite")

    output = CommonLib.execute_command(QUERY_EEPROM_WRITE_PROTECTION_CMD, mode=Const.ONIE_RESCUE_MODE)
    protect_value = parseSingleValue(output, VALUE_PATTERN)
    if not protect_value:
        raise Exception("Didn't get EEPROM write protection value.")

    CommonLib.execute_check_dict("DUT", ENABLE_EEPROM_WRITE_CMD, mode=Const.ONIE_RESCUE_MODE,
                                 patterns_dict=fail_dict, timeout=10, is_negative_test=True)

    return protect_value


def writeTlvValueToEeprom(TLV_Value):
    log.debug("Entering OnieLib class procedure: writeTlvValueToEeprom")

    enableEepromWrite()
    cmd = QUERY_EEPROM_WRITE_PROTECTION_CMD
    run_command(QUERY_EEPROM_WRITE_PROTECTION_CMD)

    output = ""
    for key, value in TLV_Value.items():
        if not value[1]:
            continue
        log.info("Write value for {}".format(key))
        if value[0] in ("0xFD", ): #unset first before setting for "0xFD"
            for i in range(3):
                cmd = 'onie-syseeprom -s {}'.format(value[0].lower())
                output += run_command(cmd, timeout=10)
        cmd = 'onie-syseeprom -s {}={}'.format(value[0].lower(), value[1])
        if key in ("Manufacture Date", "Vendor Extension"):
            cmd = 'onie-syseeprom -s {}="{}"'.format(value[0].lower(), value[1])
        output += run_command(cmd, timeout=10)

    CommonLib.execute_check_dict("DUT", "", patterns_dict=fail_dict, timeout=10,
                                check_output=output, is_negative_test=True)


def checkTlvValueFromEeprom(TLV_Value):
    log.debug("Entering OnieLib class procedure: checkTlvValueFromEeprom")

    onie_syseeprom_info = CommonLib.execute_command(ONIE_SYSEEPROM_CMD, mode=Const.ONIE_RESCUE_MODE)
    parsed_value = parseSyseeprom(onie_syseeprom_info)
    fail_count = 0
    for key, value in TLV_Value.items():
        parsed = parsed_value.get(key, "NotFound")
        if parsed != value:
            if value[0] in ("0x26",) and parsed[1].lstrip("0") == value[1].lstrip("0"):
                continue
            else:
                log.error("Key: {}, value : {}, expected: {}".format(key, parsed, value))
                fail_count += 1

    if fail_count:
        raise Exception("Read value is not match written value.")


def disableEepromWrite(write_protect_value):
    log.debug("Entering OnieLib class procedure: disableEepromWrite.")

    CommonLib.execute_command(QUERY_EEPROM_WRITE_PROTECTION_CMD, mode=Const.ONIE_RESCUE_MODE)
    disable_write_cmd = copy.deepcopy(DISABLE_EEPROM_WRITE_CMD)
    disable_write_cmd = disable_write_cmd.format(write_protect_value)
    CommonLib.execute_check_dict(Const.DUT, disable_write_cmd, patterns_dict=fail_dict,
                                 timeout=10, is_negative_test=True)

def LoadSdkShell():
    log.debug("Entering OnieLib class procedure: LoadSdkShell")

    path = 'cd ' + sdk_shell_path
    device.sendCmd(path)

    cmd = auto_load_user + '\n'
    device.sendMsg(cmd)
    pre_prompt = "IVM:0>"
    output = device.read_until_regexp(pre_prompt,timeout=60)
    passCount = 0
    log.debug("******output=%s******" % output)
    for line in output.splitlines():
        line = line.strip()
        match = re.search('dynamic create preemphasis file done', line)
        if match:
            passCount += 1

    if passCount == 1:
        log.info('%s is PASSED\n' % cmd)
    else:
        log.fail('Exiting execute_check_cmd with result FAIL. {}'.format(cmd))
        raise Exception("Failure with  items: {}".format(cmd))

def CheckPortLinksStatus():
    log.debug("Entering OnieLib class procedure: CheckPortLinksStatus")
    cmd = check_ports_link_status_cmd + '\n'
    pass_pattern = {}
    for i in range(1, 33):
        patternname = "port " + str(i)
        regexp = ".*" + str(i) + ".*ETH.*ISG.*8.*sysport.*" + str(i) + "\).*400G.*UP.*LINK_UP"
        pass_pattern.update({patternname: regexp})
    device.sendMsg(cmd)
    pre_prompt = "IVM:0>"
    output = device.read_until_regexp(pre_prompt,timeout=60)
    log.debug("******output=%s******" % output)
    CommonLib.execute_check_dict("DUT", "", patterns_dict=pass_pattern, timeout=60,
                                check_output=output)

def ExitSdkShell():
    log.debug("Entering OnieLib class procedure: ExitSdkShell")

    cmd = exit_sdk_shell + '\n'
    device.sendMsg(cmd)

    if device.read_until_regexp('ONIE', timeout=60):
        log.info('%s is PASSED\n' % cmd)
    else:
        log.fail('Exiting execute_check_cmd with result FAIL. {}'.format(cmd))
        raise Exception("Failure with  items: {}".format(cmd))

def verifyOnieInstallModeWorks():
    log.debug("Entering OnieLib class procedure: verifyOnieInstallModeWorks")

    cmd = "ls -l | grep '^d'|wc -l"
    device.sendMsg(cmd)
    command = cmd + '\n'
    output = device.executeCmd(command)
    log.debug("*******output=%s********" % output)
    count = 0
    for line in output.splitlines():
        line = line.strip()
        match = re.search("^0", line)
        if match:
            count += 1

    if count == 0:
        log.info('%s is PASSED\n' % cmd)
    else:
        log.fail('Exiting execute_check_dict with result FAIL. {}'.line)
        raise Exception("Failure while execute: '{}', with items: '{}'".format(cmd, line))


def checkOnieSysInfo():
    log.debug("Entering OnieLib class procedure: checkOnieSysInfo.")

    cmd = "onie-sysinfo"
    pattern = [ "arm64-celestica_cs8200-r0",
                "arm64-celestica_cs8210-r0",
                "arm64-celestica_cs8260-r0",
                "arm64-celestica_cs8264-r0"
    ]
    output = device.executeCmd(cmd)
    CommonKeywords.should_match_one_of_regexp_list(output, pattern)


def checkOnieSysInfoV():
    log.debug("Entering OnieLib class procedure: checkOnieSysInfoV.")

    cmd = "onie-sysinfo -v"
    oine_version = CommonLib.get_swinfo_dict("ONIE_Installer").get("newVersion", "NotFound")
    pattern = { oine_version: oine_version.replace(".", "\.")}

    CommonLib.execute_check_dict(Const.DUT, cmd, patterns_dict=pattern, timeout=10)


@logThis
def checkPsuInfo():
    cmd = 'psu_info'
    p1 = 'Passed'
    if "tigrisv2" in devicename.lower():
        output = CommonLib.execute_command(cmd, timeout=120)
        if p1 in output:
            log.success('Check psu info pass!')
        else:
            raise Exception('Check psu info fail!')
    else:
        if "48v" in devicename.lower():
            pattern = {'vin': '[\d.]+\s+V', 'vout': '[\d.]+\s+V', 'current': '[\d.]+\s+A', 'power': '[\d.]+\s+W', 'temp': '[\d.]+\s+C', 'status_word0': '0x\w+'}
        else:
            pattern = {'voltage': '\d{2}\.\d{2}\s+V', 'current': '\d{2}\.\d{2}\s+A', 'power': '\d{2}\.\d{2}\s+W'}
        CommonLib.execute_check_dict(Const.DUT, cmd, patterns_dict=pattern, timeout=10)

@logThis
def checkFanInfo():
    cmd = 'fan_info \n'
    passCount = 0
    pattern_list = list()
    for i in range(1, 7):
        tmp_list = ['PWM\s+\|\s+\d.*\d+.*\d+', 'RPM\s+\|\s+\d.*\d+.*\d+']
        regexp = 'fan\-' + str(i) + '\sPanel.*Present.*F2B'
        tmp_list.insert(0, regexp)
        pattern_list.extend(tmp_list)
    device.sendMsg(cmd)
    for pattern in pattern_list:
        device.read_until_regexp(pattern)
        passCount += 1
    if passCount == len(pattern_list):
        log.info("check fan info Success!")
    else:
        log.fail("check fan info failed")
        raise Exception("check fan info failed")


@logThis
def checkThermalInfo():
    cmd = 'thermal_info'
    pattern_list = []
    devicename = os.environ.get("deviceName", "")
    if "tianhe" in devicename.lower():
        for i in range(1, 10):
            regexp = str(i)+'.*lm75.*\d\.\d.*\d{2,3}\.\d.*\d{2,3}\.\d{2}'
            pattern_list.append(regexp)
        for i in range(10, 14):
            regexp = str(i)+'.*sa56004.*\d\.\d.*\d{2,3}\.\d.*\d{2,3}\.\d{2}'
            pattern_list.append(regexp)
        for i in range(14, 29):
            regexp = str(i)+'.*asc10.*\d\.\d.*\d{2,3}\.\d.*\d{2,3}\.\d{2}'
            pattern_list.append(regexp)
        if "48v" in devicename.lower():
            for i in range(29, 36):
                regexp = str(i) + '.*tps.*\d\.\d.*\d{2,3}\.\d.*\d{2,3}\.\d{2}'
                pattern_list.append(regexp)
            regexp = '36.*q50sn12.*\d\.\d.*\d{2,3}\.\d.*\d{2,3}\.\d{2}'
            pattern_list.append(regexp)
            regexp = '37.*ltc42.*\d\.\d.*\d{2,3}\.\d.*\d{2,3}\.\d{2}'
            pattern_list.append(regexp)
            for i in range(38, 45):
                regexp = str(i)+'.*CPU.*\d\.\d.*\d{2,3}\.\d.*\d{2,3}\.\d{2}'
                pattern_list.append(regexp)
        else:
            for i in range(29, 35):
                regexp = str(i)+'.*tps.*\d\.\d.*\d{2,3}\.\d.*\d{2,3}\.\d{2}'
                pattern_list.append(regexp)
            for i in range(35, 42):
                regexp = str(i)+'.*CPU.*\d\.\d.*\d{2,3}\.\d.*\d{2,3}\.\d{2}'
                pattern_list.append(regexp)
    else:
        for i in range(1, 10):
            regexp = str(i)+'.*lm75.*\d\.\d.*\d{2,3}\.\d.*\d{2,3}\.\d{2}'
            pattern_list.append(regexp)
        for i in range(10, 19):
            regexp = str(i)+'.*asc10.*\d\.\d.*\d{2,3}\.\d.*\d{2,3}\.\d{2}'
            pattern_list.append(regexp)
        for i in range(19, 24):
            regexp = str(i)+'.*tps.*\d\.\d.*\d{2,3}\.\d.*\d{2,3}\.\d{2}'
            pattern_list.append(regexp)
        for i in range(24, 28):
            regexp = str(i)+'.*CPU.*\d\.\d.*\d{2,3}\.\d.*\d{2,3}\.\d{2}'
            pattern_list.append(regexp)
    pattern_list.append('.*app.*\d\.\d.*\d{2,3}\.\d.*\d{2,3}\.\d{2}')
    passCount = 0
    output = device.executeCmd(cmd)
    for line in output.splitlines():
        for pattern in pattern_list:
            if re.search(pattern, line):
                passCount += 1
                continue
    if passCount == len(pattern_list):
        log.info("check thermal Success!")
    else:
        log.fail("check thermal failed")
        raise Exception("check thermal failed")


@logThis
def run_i2c_update_test():
    device_name = device.name
    card_type = CommonLib.get_device_info(device_name).get("cardType")
    fpga_type = '1PPS_FPGA' if card_type == "1PPS" else 'I2C_FPGA'
    destination_path = CommonLib.get_swinfo_dict(fpga_type).get("localImageDir", "NotFound")
    filelist = CommonLib.get_swinfo_dict(fpga_type).get("newImage")
    filelists = [filelist]
    log.info('filelist=%s' % filelist)
    asc_path = CommonLib.get_swinfo_dict(fpga_type).get("hostImageDir", "NotFound")
    if not os.path.exists(destination_path):
        log.debug('path not exist, mkdir it')
        device.sendMsg("mkdir " + destination_path + '\r\n')
    CommonLib.tftp_get_files(Const.DUT, file_list=filelists, src_path=asc_path, dst_path=destination_path)
    device.sendMsg("cd " + destination_path + '\r\n')
    if "1PPS" == card_type:
        mtd_path = '/dev/mtd6'
    else:
        mtd_path = '/dev/mtd5'
    update_command = 'flashcp -v ' + filelist + ' ' + mtd_path
    pattern = [
        #r'Erasing block.*?\(100\%\)',
        #r'Writing kb.*?\(100\%\)',
        r'Verifying kb.*?\(100\%\)'
    ]
    pass_count = 0
    output = device.executeCmd(update_command, timeout=300)
    for line in output.splitlines():
        line = line.strip()
        for i in range(len(pattern)):
            match = re.search(pattern[i], line)
        if match:
            pass_count += 1

    log.info("passcount=%s" % pass_count)
    if pass_count >= len(pattern):
        log.info("I2C Update Success!")
    else:
        log.fail("Updating failed!")
        raise Exception("Updating failed!")
@logThis
def cat_i2c_version():

    devicename = os.environ.get("deviceName", "")
    dev_type = DeviceMgr.getDevice(devicename).get('cardType')
    cmd = 'cat /sys/devices/xilinx/accel-i2c/version'
    fpga_type = 'I2C_FPGA'
    if dev_type == '1PPS':
        cmd = 'cat /sys/devices/xilinx/pps-i2c/version'
        fpga_type = '1PPS_FPGA'
    output = device.executeCmd(cmd)
    match = re.search("(fail|error)", output, re.I)
    if match:
        log.fail("log failed, please check output")
        raise Exception("log failed, please check output")
    pattern = r'^0x[0-9A-Fa-f]{3}$'
    for line in output.splitlines():
        match = re.search(pattern, line)
        if match:
            version = match.group(0)
            break
    expected_ver = SwImage.getSwImage(fpga_type).newVersion
    if version == expected_ver:
        log.success('current fpga version: {} match expected: {}.'.format(version, expected_ver))
    else:
        raise RuntimeError('current fpga version: {} do not match expected: {}!'.format(version, expected_ver))



def checkOnieOsRelease():
    log.debug("Entering OnieLib class procedure: checkOnieOsRelease.")

    cmd = "cat /etc/os-release"
    oine_version = CommonLib.get_swinfo_dict("ONIE_Installer").get("newVersion", "NotFound")
    onie_version = oine_version + '\s*'
    #version_pattern = 'VERSION="{}"'.format(oine_version)
    version_pattern = 'VERSION="%s"' % onie_version
    pattern = { 'NAME="onie"'   : 'NAME="onie"',
                'ID=linux'      : 'ID=linux',
                version_pattern : version_pattern.replace(".", "\.")
            }

    CommonLib.execute_check_dict(Const.DUT, cmd, patterns_dict=pattern, timeout=10)


def rebootAndCheckCannotFindImage():
    log.debug("Entering OnieLib class procedure: rebootAndCheckCannotFindImage.")

    expect_message = "ERROR: can't get kernel image"
    try:
        device.sendCmdRegexp("reboot", expect_message, timeout=KapokConst.BOOT_TIME)
    except:
        raise Exception("Timeout: Didn't get expected message: {}".format(expect_message))


def upgradeCpld():
    log.debug("Entering OnieLib class procedure: upgradeCpld")

    filelist = ["default_vme_list.cfg", "default_vme_list_without_tpm.cfg"]
    sys_cpld_file = CommonLib.get_swinfo_dict("SYS_CPLD").get("newImage", "NotFound")
    fan_cpld_file = CommonLib.get_swinfo_dict("FAN_CPLD").get("newImage", "NotFound")
    filelist.extend([sys_cpld_file, fan_cpld_file])
    filepath = CommonLib.get_swinfo_dict("FAN_CPLD").get("hostImageDir", "NotFound")
    destination_path = vmetool_path

    CommonLib.tftp_get_files(Const.DUT, file_list=filelist, src_path=filepath, 
                             dst_path=destination_path)

    update_sys_cmd = "{} {}".format(vmetool, sys_cpld_file)
    update_fan_cmd = "{} -f {}".format(vmetool, fan_cpld_file)
    cmd_dict = OrderedDict({ "SYS_CPLD": update_sys_cmd, "FAN_CPLD": update_fan_cmd })
    pass_pattern = {"| PASS! |" : "\|\s+PASS!\s+\|"}
    for item, cmd in cmd_dict.items():
        try:
            CommonLib.execute_check_dict(Const.DUT, cmd, patterns_dict=pass_pattern,
                                         path=vmetool_path, timeout=600)
        except:
            raise Exception("Upgrade {} failed.".format(item))

@logThis
def fenghuangv2_upgrade_cpld():
    filelist=[]
    sys_cpld_file = CommonLib.get_swinfo_dict("SYS_CPLD").get("newImage", "NotFound")
    fan_cpld_file = CommonLib.get_swinfo_dict("FAN_CPLD").get("newImage", "NotFound")
    filelist.extend([sys_cpld_file, fan_cpld_file])
    filepath = CommonLib.get_swinfo_dict("FAN_CPLD").get("hostImageDir", "NotFound")
    device.sendCmd("rm -rf {}".format(vmetool_path), timeout=60)
    device.sendCmd("mkdir {}".format(vmetool_path) ,timeout=60)
    CommonLib.tftp_get_files(Const.DUT, file_list=filelist, src_path=filepath,
                             dst_path=vmetool_path)
    update_sys_cmd = "{} -s {}".format(vmetool, sys_cpld_file)
    update_fan_cmd = "{} -f {}".format(vmetool, fan_cpld_file)
    cmd_dict = OrderedDict({ "SYS_CPLD": update_sys_cmd, "FAN_CPLD": update_fan_cmd })
    pass_pattern = {"| PASS! |" : "\|\s+PASS!\s+\|"}
    for item, cmd in cmd_dict.items():
        try:
            CommonLib.execute_check_dict(Const.DUT, cmd, patterns_dict=pass_pattern,
                                         path=vmetool_path, timeout=600)
        except:
            raise Exception("Upgrade {} failed.".format(item))

def checkCpldVersion():
    log.debug("Entering OnieLib class procedure: checkCpldVersion")
    sys_cpld_version = CommonLib.get_swinfo_dict("SYS_CPLD").get("newVersion", "NotFound")
    fan_cpld_version = CommonLib.get_swinfo_dict("FAN_CPLD").get("newVersion", "NotFound")
    if "tianhe" in devicename.lower():
        come_cpld_version = CommonLib.get_swinfo_dict("COME_CPLD").get("newVersion", "NotFound")[:-2]
        log.info("sys_cpld:{}, fan_cpld: {}, come_cpld: {}".format(sys_cpld_version, fan_cpld_version, come_cpld_version))
    else:
        log.info("sys_cpld:{}, fan_cpld: {}".format(sys_cpld_version, fan_cpld_version))
    sys_cpld_version_pattern = { sys_cpld_version : "^{}".format(sys_cpld_version) }
    fan_cpld_version_pattern = { fan_cpld_version : "^{}".format(fan_cpld_version) }
    CommonLib.execute_check_dict(Const.DUT, get_sys_cpld_version_cmd, mode=Const.ONIE_RESCUE_MODE,
                patterns_dict=sys_cpld_version_pattern, timeout=10)
    CommonLib.execute_check_dict(Const.DUT, get_fan_cpld_version_cmd, mode=Const.ONIE_RESCUE_MODE,
                patterns_dict=fan_cpld_version_pattern, timeout=10)
    if "tianhe" in devicename.lower():
        come_cpld_version_pattern = {come_cpld_version: "^{}".format(come_cpld_version)}
        CommonLib.execute_check_dict(Const.DUT, get_come_cpld_version_cmd, mode=Const.ONIE_RESCUE_MODE,
                                     patterns_dict=come_cpld_version_pattern, timeout=10)

def getDeviceIp(interface, mode=Const.ONIE_INSTALL_MODE):
     log.debug("Entering OnieLib class procedure: getDeviceIp")

     return CommonLib.get_ip_address(Const.DUT, interface, mode)


def checkOnieTelnet():
    log.debug("Entering OnieLib class procedure: checkOnieTelnet")

    from robot.libraries.Telnet import TelnetConnection
    device_ip = getDeviceIp("eth0")
    log.info("Telnet to {}  ...".format(device_ip))
    telnetObj = TelnetConnection(device_ip)
    output = telnetObj.read_until_regexp(device.promptOnie)
    cmd_list = [get_versions_cmd, ONIE_SYSEEPROM_CMD]
    for cmd in cmd_list:
        telnetObj.write_bare(cmd + "\n")
        prompt = "{}[\s\S]+{}".format(cmd[:5], device.promptOnie)
        output = telnetObj.read_until_regexp(prompt)
    telnetObj.write_bare("exit\n")
    telnetObj.close_connection()
    log.info("Telnet session was closed.")

    CommonLib.execute_check_dict("DUT", "", patterns_dict=fail_dict, timeout=10,
                                check_output=output, is_negative_test=True)


@logThis
def formatDisk(cmd="mkfs.ext3 /dev/sda3", umount_mnt=True):

    if umount_mnt:
        output = run_command("mount", timeout=10)
        if re.search("/mnt", output):
            run_command(["cd /", "umount /mnt"], timeout=10)

    device.sendMsg(cmd + "\n")
    output = device.read_until_regexp("roceed anyway\? \(y,n\)\s+", timeout=90)
    device.sendMsg("y\n")
    output += device.read_until_regexp(device.promptOnie, timeout=60)
    fdisk_l_cmd = "fdisk -l \n"
    output += run_command(fdisk_l_cmd, timeout=5 )

    CommonLib.execute_check_dict("DUT", "", patterns_dict=fail_dict, timeout=10,
                                check_output=output, is_negative_test=True)

@logThis
def tryToAccessDiagOS():

    is_exit = False
    KapokCommonLib.bootIntoUboot()
    device.sendMsg('\r')
    device.sendMsg('run diag_bootcmd \n')
    try:
        out = device.read_until_regexp("ERROR: can't get kernel image!", 10)
    except:
        is_exit = True
        device.read_until_regexp(device.loginPromptDiagOS, 120)
        device.sendMsg(device.rootUserName)
        device.sendMsg('\r')
        out = device.read_until_regexp('|'.join(["Password:", device.promptDiagOS]), 10)
        if "Password:" in out:
            device.sendMsg(device.rootPassword)
            device.sendMsg('\r')
            device.read_until_regexp(device.promptDiagOS)
    else:
        KapokCommonLib.powerCycleToOnieRescueMode()
    if is_exit:
        log.debug("DiagOS exist")
        raise Exception("DiagOS exist")

@logThis
def mountDisk(cmd="mount /dev/sda3 /mnt"):

    cmd_list = ["cd /", "fdisk -l", cmd, "cd /mnt", "ls"]
    output = run_command(cmd_list, timeout=10)

    CommonLib.execute_check_dict("DUT", "", patterns_dict=fail_dict, timeout=10,
                                check_output=output, is_negative_test=True)


@logThis
@timeThis
def downloadImagesAndRecoveryDiagOS():

    diagos_files = CommonLib.get_swinfo_dict("DIAGOS").get("newImage")
    rootfs_file = diagos_files[:1]
    rename_files = ['rootfs.cpio.gz']
    run_command("cd /root" )   #unzip file in /root to avoid space full issue
    log.info("rootfs_file: {}, rename_files: {}".format(rootfs_file, rename_files))
    CommonLib.tftp_get_files(Const.DUT, file_list=rootfs_file, renamed_file_list=rename_files, timeout=400)
    cmd_list = ["gunzip rootfs.cpio.gz", "cd /mnt", "cpio -i < /root/rootfs.cpio"]
    output = run_command(cmd_list, timeout=300)
    CommonLib.execute_check_dict("DUT", "", patterns_dict=fail_dict, timeout=10,
                                check_output=output, is_negative_test=True)

    run_command("cd ./root")
    uimage_dtb = diagos_files[1:]
    rename_uimage_dtb = ["uImage", "celestica_cs8200-r0.dtb"]
    CommonLib.tftp_get_files(Const.DUT, file_list=uimage_dtb, renamed_file_list=rename_uimage_dtb, timeout=400)
    cmd_list = ["sync", "cd /", "umount /mnt"]
    output = run_command(cmd_list, timeout=300)
    CommonLib.execute_check_dict("DUT", "", patterns_dict=fail_dict, timeout=10,
                                check_output=output, is_negative_test=True)

@logThis
@timeThis
def fhv2downloadImagesAndRecoveryDiagOS():

    diagos_file_name = CommonLib.get_swinfo_dict("DIAGOS").get("newImage")
    hostImageDir = CommonLib.get_swinfo_dict("DIAGOS").get("hostImageDir")
    diagos_file = ["{}/{}".format(hostImageDir,diagos_file_name)]
    CommonLib.tftp_get_files(Const.DUT, file_list=diagos_file, dst_path="/root", timeout=400)
    install_diagos_cmd = "onie-nos-install {}".format(diagos_file_name)
    output = device.sendCmdRegexp(install_diagos_cmd, INSTALLER_MODE_DETECT_PROMPT, timeout=900)
    CommonLib.execute_check_dict("DUT", "", patterns_dict=RECOVERY_DIAG_PATTERN, timeout=60,
                                check_output=output)

@logThis
@timeThis
def fhv2downloadstressAndRecoveryDiagOS():
    stress_file=["fenghuangv2/stress_test.tar.xz"]
    run_command("mkdir /root/tools")
    CommonLib.tftp_get_files(Const.DUT, dst_path="/root/tools",file_list=stress_file, timeout=400)
    cmd_list = ["tar -xf stress_test.tar.xz"]
    output = run_command(cmd_list, timeout=300)
    CommonLib.execute_check_dict("DUT", "", patterns_dict=fail_dict, timeout=10,
                                 check_output=output, is_negative_test=True)

@logThis
def createPartion(p_type="p", size="+5400M"):

    fdisk_cmd = "fdisk /dev/sda"
    wait_cmd_p = "Command \(m for help\):"
    wait_action_p = "Command action[\s\S]+primary partition \(1-4\)"
    first_cylinder_p = "First cylinder.*?:\s"
    last_cylinder_p = "Last cylinder.*?:\s"
    new_partition_p = "Selected partition\s+(\d)"

    device.sendMsg(fdisk_cmd + "\n")
    device.read_until_regexp(wait_cmd_p, timeout=10)
    device.sendMsg("n\n")
    device.read_until_regexp(wait_action_p, timeout=10)
    device.sendMsg("{}\n".format(p_type))
    output = device.read_until_regexp(first_cylinder_p, timeout=10)
    device.sendMsg("\n")
    device.read_until_regexp(last_cylinder_p, timeout=10)
    device.sendMsg("{}\n".format(size))
    device.read_until_regexp(wait_cmd_p, timeout=10)
    device.sendMsg("{}\n".format(p_type))
    device.read_until_regexp(wait_cmd_p, timeout=10)
    device.sendMsg("w\n")
    device.read_until_regexp(device.promptOnie, timeout=10)
    partition_match = re.search(new_partition_p, output)
    if partition_match:
        partition = "/dev/sda{}".format(partition_match.group(1))
    else:
        raise Exception("Selected partition is not existed.")
    target_disk = partition
    fdisk_l_cmd = "fdisk -l \n"
    output = run_command(fdisk_l_cmd, timeout=5)
    if not re.search(target_disk, output):
        raise Exception("No {} existed.".format(target_disk))


@logThis
def deletePartion(p_number="4"):

    target_disk = "/dev/sda{}".format(p_number)
    fdisk_l_cmd = "fdisk -l \n"
    prompt = "{}[\s\S]+{}".format(fdisk_l_cmd[:5], device.promptOnie)
    output = device.sendCmdRegexp(fdisk_l_cmd, prompt, timeout=5 )
    if not re.search(target_disk, output):
        log.info("No {} existed.".format(target_disk))
        return

    fdisk_cmd = "fdisk /dev/sda"
    wait_cmd_p = "Command \(m for help\):"
    select_partition_p = "Partition number.*?:\s"
    device.sendMsg(fdisk_cmd + "\n")
    device.read_until_regexp(wait_cmd_p, timeout=10)
    device.sendMsg("d\n")
    device.read_until_regexp(select_partition_p, timeout=10)
    device.sendMsg("{}\n".format(p_number))
    device.read_until_regexp(wait_cmd_p, timeout=10)
    device.sendMsg("w\n")
    device.read_until_regexp(device.promptOnie, timeout=10)

@logThis
def checkFileSystemUtilities():

    for cmd in file_system_utilities_commands.values():
        if cmd == "mkfs.ext3 /dev/sda4":
           device.sendMsg(cmd + '\n')
           finish_prompt = "mkfs[\s\S]+{}".format(device.promptOnie)
           format_flag = 0
           try:
               device.read_until_regexp(' \(y,n\) ', timeout=10)
               device.sendMsg("y\n")
           except:
               if DeviceMgr.usingSsh == True:
                   output = str(device.child.before)
               elif DeviceMgr.usingSsh == False:
                   output = str(device.telnetConnect.before)
               if not re.search(finish_prompt, output):
                   raise Exception("Format disk failed.")
               format_flag = 1
           if not format_flag:
               output = device.read_until_regexp('ONIE',timeout=10)
        else:
            device.sendMsg(cmd+'\n')
            output = device.read_until_regexp('ONIE',timeout=10)
        CommonLib.execute_check_dict("DUT", "", patterns_dict=fail_dict, timeout=10, check_output=output, is_negative_test=True)

@logThis
def installerDiscoveryCheck(timeout=300):

    device.sendMsg("reboot\n")
    output = device.read_until_regexp(KapokConst.ONIE_DISCOVERY_PROMPT, timeout=KapokConst.BOOT_TIME)
    time_start = time.time()
    while True:
        output += device.readMsg()
        time_duration = time.time() - time_start
        if time_duration > timeout:
            break
        time.sleep(1)

    device.read_until_regexp(KapokConst.ONIE_DISCOVERY_PROMPT, timeout=KapokConst.BOOT_TIME)
    device.sendCmdRegexp(KapokConst.STOP_ONIE_DISCOVERY_KEY + "\n", device.promptOnie, timeout=KapokConst.BOOT_TIME)
    discovery_times = len(re.findall(KapokConst.ONIE_DISCOVERY_PROMPT, output))
    if discovery_times == 0:
        raise Exception("ONIE Service Discovery didn't start.")
    else:
        log.info("ONIE Service Discovery {} times in {}s".format(discovery_times, timeout))
    discovery_log = output.split(KapokConst.ONIE_DISCOVERY_PROMPT)[1]
    tftp_search_p = "tftp:.*?onie-installer.*?$"
    request_tftp_times = len(re.findall(tftp_search_p, discovery_log, re.M))
    if request_tftp_times == 0:
        raise Exception("Didn't find tftp request afer ONIE Service Discovery.")
    elif request_tftp_times < 10:
        raise Exception("Tftp request times number is only {}!".format(request_tftp_times))

@logThis
def onieIfconfigEth0():
    cmd = 'fw_printenv'
    output = CommonLib.execute_command(cmd,timeout=10)
    p1 = 'eth1addr=d6:4e:4e:ff:4e:03'
    if 'tianhe' in devicename.lower():
        if re.search(p1, output):
            log.fail('Should not find etht1addr.')
            raise Exception('Failed run onieIfconfigEth0')
        pattern = {
            "arch": "arch=arm",
            "autoload": "autoload=n"
        }
        CommonLib.execute_check_dict("DUT", "", patterns_dict=pattern, timeout=10, check_output=output)
    else:
        pattern = {
                "arch":"arch=arm",
                "autoload":"autoload=n"
                }
        CommonLib.execute_check_dict("DUT", "", patterns_dict=pattern, timeout=10, check_output=output)

    cmd2 = 'ifconfig eth0'
    output2 = CommonLib.execute_command(cmd2,timeout=10)
    pattern = {
        "inet addr" : "inet addr:\d+\.+\d+\.*"
    }
    CommonLib.execute_check_dict("DUT", "", patterns_dict=pattern, timeout=10, check_output=output2)

@logThis
def setEth1Addr():
    eth1_cmd = "setenv eth1addr "
    device.sendMsg(eth1_cmd+'\n')
    eth1_cmd += setenvaddr
    device.sendMsg(eth1_cmd+'\n')
    savenv_cmd = "saveenv"
    if 'tianhe' in devicename.lower():
        savenv_pattern = {
            "save env": "Saving Environment to SPIFlash...",
            "erasing and writing flash": "Erasing SPI flash...Writing to SPI flash...done"
        }
    else:
        savenv_pattern = {
            "save env" : "Saving Environment to SPI Flash...",
            "erasing and writing flash" : "Erasing SPI flash...Writing to SPI flash...done"
        }
    output = CommonLib.execute_command(savenv_cmd,timeout=10)
    CommonLib.execute_check_dict("DUT", "", patterns_dict=savenv_pattern, timeout=10, check_output=output)


def verifyCanAccessIntegratorMode(port_mode):

    modeName_cmd = 'integrator_mode'
    option = '-m'
    modes_char = port_mode
    final_cmd = modeName_cmd + ' ' + option + ' ' + modes_char + '\n'
    device.sendMsg(final_cmd)
    pre_prompt = "IVM:0>"
    output = device.read_until_regexp(pre_prompt, timeout=120)
    if 'fenghuangv2' in devicename.lower():
        if Innovinum_success in output:
            log.info('%s is PASSED\n' % final_cmd)
        else:
            log.fail('Exiting execute_check_cmd with result FAIL. {}'.format(final_cmd))
            raise Exception("Failure with  items: {}".format(final_cmd))

@logThis
def quitSdkShell():

    cmd = 'cd ' + sdk_shell_path + '\n'
    device.sendMsg(cmd)
    cmd1 = 'ps'
    output = run_command(cmd1,timeout=20)
    if "{innovium.user}" in output:
 
        cmd = './cls_shell exit'
        device.sendMsg(cmd+'\n')
        sleep(10)
        output1 = device.read_until_regexp('ONIE', timeout=60)
        count = 0
        for line in output1.splitlines():
            line = line.strip()
            match_string = "Innovium Switch PCIe Driver closed successfully"
            match = re.search(match_string, line)
            if match:
                count+=1
        if count:
            log.info('%s is PASSED\n' % cmd)
        else:
            log.fail('Exiting execute_check_cmd with result FAIL. {}'.format(cmd))
            raise Exception("Failure with  items: {}".format(cmd))
    else:
        log.info('Already quit sdk shell!')

@logThis
def fpp_speed_dict_check(portMode):
    demo32_100_dict = {}
    demo32_40_dict = {}
    demo32_400_dict = {}
    demo128_10_dict = {}
    demo128_25_dict = {}
    demo128_100_dict = {}
    demo64_100_dict = {}
    demo100_40_dict = {}
    demo100_18_dict = {}
    demo100_25_dict = {}
    # 32x400, 32x100, 32x40
    for i in range(1, 33):
        demo32_100_dict[str(i)] = '100'
        demo32_40_dict[str(i)] = '40'
        demo32_400_dict[str(i)] = '400'
    # 64x100, 64x100-1
    for i in range(1, 65):
        demo64_100_dict[str(i)] = '100'
    # 128x100[sfp_detect, empty_value, 1-32:4x100G], 128x25, 128x10
    for i in range(1, 129):
        demo128_10_dict[str(i)] = '10'
        demo128_25_dict[str(i)] = '25'
        demo128_100_dict[str(i)] = '100'
    # 1-2:4x100G;3-4:40G
    for i in range(1, 9):
        demo100_40_dict[str(i)] = '100'
    demo100_40_dict['9'] = '40'
    demo100_40_dict['10'] = '40'
    # 1:4x100G;2-15:100G
    for i in range(1, 19):
        demo100_18_dict[str(i)] = '100'
    # 1:4x100G;2-15:100G;16-32:4x25G
    for i in range(1, 19):
        demo100_25_dict[str(i)] = '100'
    for k in range(19, 87):
        demo100_25_dict[str(k)] = '25'
    if portMode == '32x400':
        return demo32_400_dict
    elif portMode == '32x100' or portMode == '32x100_copper':
        return demo32_100_dict
    elif portMode == '32x40':
        return demo32_40_dict
    elif portMode == '64x100' or portMode == '64x100-1' or portMode == '64x100_copper':
        return demo64_100_dict
    elif (portMode == '128x100') or (portMode == 'sfp_detect') or (portMode == '1-32:4x100G') or (portMode == empty_value):
        return demo128_100_dict
    elif portMode == '128x25' or portMode == '128x25_copper':
        return demo128_25_dict
    elif portMode == '128x10' or portMode == '128x10_copper':
        return demo128_10_dict
    elif portMode == '1-2:4x100G;3-4:40G':
        return demo100_40_dict
    elif portMode == '1:4x100G;2-15:100G':
        return demo100_18_dict
    elif portMode == '1:4x100G;2-15:100G;16-32:4x25G':
        return demo100_25_dict

@logThis
def enableSomePortAndVerifyPortEnable(port_number1,port_number2, port_mode):
    cmd = 'ifcs show devport'
    device.sendMsg(cmd+'\n')
    output = device.read_until_regexp("IVM:0>", timeout=60)
    if 'fenghuangv2' in devicename.lower():
        enable_cmd = 'port enable' + ' ' + port_number1 + '-' + port_number2
        log.debug("********enable_md=%s*********" % enable_cmd)
        device.sendMsg(enable_cmd+'\n')
        time.sleep(300)
        device.sendMsg(cmd+'\n')
        time.sleep(5)
    device.sendMsg('exit'+'\n')
    final_output = device.read_until_regexp("ONIE", timeout=120)
    #check port num and speed
    error_count = 0
    speed_dict = {}
    # fpp_speed_dict_check()
    p1 = r'\|\s+(\d+)\s+\|\s+ETH\s+\|.*\|\s+\(sysport:\s+(\d+)\)\s+\|\s+(\d+)G\s+\|'
    for line in output.splitlines():
        line = line.strip()
        match = re.search(p1, line, re.IGNORECASE)
        if match:
            port_num = match.group(2)
            port_speed = match.group(3)
            speed_dict[port_num] = port_speed
    log.info('#### Get the port speed: %s ####' % str(speed_dict))
    if len(speed_dict) == int(FPPS_COUNT_PATTERN[port_mode]):
        log.success('Get the fpp [%s] port num is [%d] pass.' % (port_mode, len(speed_dict)))
        if port_mode == '32x400':
            res = check_fpp_speed(speed_dict, fpp_speed_dict_check(port_mode))
            if res:
                error_count += 1
        elif port_mode == '32x100' or port_mode == '32x100_copper':
            res = check_fpp_speed(speed_dict, fpp_speed_dict_check(port_mode))
            if res:
                error_count += 1
        elif port_mode == '32x40':
            res = check_fpp_speed(speed_dict, fpp_speed_dict_check(port_mode))
            if res:
                error_count += 1
        elif port_mode == '64x100' or port_mode == '64x100-1' or port_mode == '64x100_copper':
            res = check_fpp_speed(speed_dict, fpp_speed_dict_check(port_mode))
            if res:
                error_count += 1
        elif port_mode == '128x100' or port_mode == 'sfp_detect':
            res = check_fpp_speed(speed_dict, fpp_speed_dict_check(port_mode))
            if res:
                error_count += 1
        elif port_mode == '128x25' or port_mode == '128x25_copper':
            res = check_fpp_speed(speed_dict, fpp_speed_dict_check(port_mode))
            if res:
                error_count += 1
        elif port_mode == '128x10' or port_mode == '128x10_copper':
            res = check_fpp_speed(speed_dict, fpp_speed_dict_check(port_mode))
            if res:
                error_count += 1
    else:
        error_count += 1
    if error_count:
        raise Exception('Failed run enableSomePortAndVerifyPortEnable')

@logThis
def compareOnieUbootaddress():
    cmd = 'fw_printenv'
    output = CommonLib.execute_command(cmd, timeout=10)
    cmd_pattern = {
            "arch":"arch=arm",
            "autoload":"autoload=n"
    }
    CommonLib.execute_check_dict("DUT", "", patterns_dict=cmd_pattern, timeout=10, check_output=output)

    cmd2 = 'ifconfig eth0'
    output2 = CommonLib.execute_command(cmd2,timeout=10)
    count = 0
    for line in output2.splitlines():
        line = line.strip()
        match = re.search(setenvaddr,line,re.I)
        if match:
            count+=1
    if count == 0:
        log.fail('Exiting execute_check_cmd with result FAIL. {}'.format(cmd2))
        raise Exception("Failure with  items: {}".format(cmd2))
    elif count == 1:
        log.info('%s is PASSED\n' % cmd2)

@logThis
def addTestParameters(param=''):

    fw_cmd = 'fw_setenv'
    test_cmd = 'testenv' + param
    parameters_cmd = 'mytestenv' + param

    command = fw_cmd + ' ' + test_cmd + ' ' + parameters_cmd

    device.sendMsg(command+'\n')
    device.read_until_regexp('Proceed with update \[N\/y\]\? ', timeout=10)
    device.sendMsg("y\n")
    output = device.read_until_regexp("ONIE",timeout=10)
    CommonLib.execute_check_dict("DUT", "", patterns_dict=fail_dict, timeout=10, check_output=output, is_negative_test=True)

@logThis
def printenvOnUboot():
    set_default_env_cmd = 'env default -a\n'
    device.sendMsg(set_default_env_cmd)
    save_cmd = 'saveenv\n'
    device.sendMsg(save_cmd)
    cmd = "printenv"
    output = CommonLib.execute_command(cmd, timeout=10)
    pattern = {
        "printenv failed" : "Environment size:.*?"
    }
    CommonLib.execute_check_dict("DUT", "", patterns_dict=pattern, timeout=20, check_output=output)

@logThis
def restoreUbootEnv():
    env_default = 'env default -a'
    save_cmd = 'savee'
    device.sendMsg(env_default + '\n')
    device.read_until_regexp('Resetting to default environment', timeout=60)
    device.sendMsg(save_cmd+'\n')
    device.read_until_regexp('OK', timeout=60)
    device.sendMsg('reset\n')
    device.read_until_regexp(KapokConst.STOP_AUTOBOOT_PROMPT, timeout=100)
    device.sendMsg("{}\n".format(KapokConst.STOP_AUTOBOOT_KEY))
    device.read_until_regexp(device.promptUboot, timeout=100)
    if 'tianhe' in devicename.lower():
        error_count = 0
        p1 = 'Environment size: \d+/\d+ bytes'
        log.info('#### run command: %s ####'%ubootEnvTool)
        device.sendMsg(ubootEnvTool+'\n')
        output = device.read_until_regexp(p1, timeout=60)
        testEnvLst.append(setenvaddr)
        for pattern in testEnvLst:
            if re.search(pattern, output):
                error_count += 1
                log.fail('Should not show the [%s].'%pattern)
        if error_count:
            raise Exception('Failed run restoreUbootEnv')

@logThis
def checkSsdHealth():

    check_cmd = "smartctl -a /dev/sda1"
    output = run_command(check_cmd, timeout=5)
    ssd_info_dict = CommonLib.parseDict(output=output, pattern_dict=SSD_INFO_PATTERN, sep_field=":")
    CommonLib.execute_check_dict("DUT", "", patterns_dict=SSD_HEALTH_PATTERN, timeout=10, check_output=output)
    for key, value in ssd_info_dict.items():
        if not value.strip():
            raise Exception("No value found for {} in SSD information.".format(key))

@logThis
def checkFscCode():
    check_cmd = "cat /root/driver/install.sh"
    output = run_command(check_cmd, timeout=5)
    CommonLib.execute_check_dict("DUT", "", patterns_dict=fsc_check_pattern, timeout=5, check_output=output, line_mode=False)

@logThis
def get_percent_according_to_pattern(output):
    rt=re.findall('\d+',output)
    return rt[23]

@logThis
def getfanspeedpercent():
    check_cmd = "ps"
    output = run_command(check_cmd, timeout=5)
    CommonLib.execute_check_dict("DUT", "", patterns_dict=ps_fsc_check_pattern, timeout=5, check_output=output,
                                 line_mode=False)
    check_cmd = "fan_ctrl --show"
    output = run_command(check_cmd, timeout=5)
    CommonLib.execute_check_dict("DUT", "", patterns_dict=ps_fsc_check_percent_pattern, timeout=5, check_output=output,
                                 line_mode=False)
    fan_speed_percent=get_percent_according_to_pattern(output)
    min_speed=int(int(fan_speed_percent)*255/100-10)
    max_speed=int(int(fan_speed_percent)*255/100+10)
    return (str(min_speed)+','+str(max_speed))

@logThis
def checkFanSpeed(speed):
    minspeed=str(speed).split(",")[0]
    maxspeed = str(speed).split(",")[1]
    log.info("fan min speed: {},fan max speed: {}".format(minspeed,maxspeed))
    fan_num_pattern = "(fan.*?)\s+Panel"
    pwm_speed_pattern = "PWM\s+\|\s+\d\s+\|\s+(\d+)\s+\|\s+(\d+)"

    cmd_list = ["cd /root/diag", "cat README |grep export",
                "export LD_LIBRARY_PATH=/root/diag/output",
                "export CEL_DIAG_PATH=/root/diag",
                "./cel-fan-test --show"
                ]
    output = run_command(cmd_list, timeout=20)
    fan_speed_dict = {}
    SPEED_FOUND_FLAG = 0
    for line in output.splitlines():
        fan_num_match = re.search(fan_num_pattern, line)
        pwm_speed_match = re.search(pwm_speed_pattern, line)
        fan_num = ""
        if fan_num_match:
            fan_num = fan_num_match.group(1).strip()
            fan_speed_dict.setdefault(fan_num, [])
        if pwm_speed_match:
            SPEED_FOUND_FLAG = 1
            pwm_max_speed = int(pwm_speed_match.group(1).strip())
            pwm_speed = int(pwm_speed_match.group(2).strip())
            fan_speed_dict.setdefault(fan_num, []).append(pwm_speed)
            if  pwm_speed < int(minspeed) or pwm_speed > int(maxspeed):
                raise Exception("{} fan speed is {}, exceed 50% of max speed {}".format(fan_num, pwm_speed, pwm_max_speed))
    if not SPEED_FOUND_FLAG:
        raise Exception("Not found fan speed info")
    log.info("fan speed: {}".format(fan_speed_dict))

@logThis
def fanCtrlShow(speed):
    cmd = 'fan_ctrl --show'
    pattern_list = list()
    for i in range(1, 7):
        regexp1 = 'fan\-' + str(i) + '\sFront is\s' + speed
        regexp2 = 'fan\-' + str(i) + '\sPanel is\s' + speed
        pattern_list.append(regexp1)
        pattern_list.append(regexp2)
    output = device.executeCmd(cmd)
    passCount = 0
    for line in output.splitlines():
        for pattern in pattern_list:
            if re.search(pattern, line):
                passCount += 1
                continue
    if passCount == len(pattern_list):
        log.info("check fan Success!")
    else:
        log.fail("check fan failed")
        raise Exception("check fan failed")

@logThis
def setFanCtrl(option, speed=None):
    cmd = 'fan_ctrl ' + option
    output = device.executeCmd(cmd)
    regexp = ''
    passCount = 0
    if speed:
        regexp = 'Changing fan speed to ' + speed
    else:
        regexp = 'Reset to normal mode'
    for line in output.splitlines():
        if re.search(regexp, line):
            passCount += 1
    if passCount:
        log.info("Set fan speed Success!")
    else:
        log.fail("Set fan speed failed")
        raise Exception("Set fan speed failed")

@logThis
def checkFanCtrl():
    fanCtrlShow('[4,5][0-9]\%')
    setFanCtrl('--stressed', speed='100\%')
    time.sleep(10)
    fanCtrlShow('100\%')
    setFanCtrl('--reset')
    time.sleep(20)
    fanCtrlShow('[4,5][0-9]\%')
    setFanCtrl('--fixed 30', speed='30\%')
    time.sleep(10)
    fanCtrlShow('30\%')
    setFanCtrl('--fixed 70', speed='70\%')
    time.sleep(10)
    fanCtrlShow('70\%')
    setFanCtrl('--fixed 100', speed='100\%')
    time.sleep(10)
    fanCtrlShow('100\%')
    setFanCtrl('--reset')
    time.sleep(20)
    fanCtrlShow('[4,5][0-9]\%')

@logThis
def checkQsfpAccess():

    port_id = 1
    qsfp_no_exist = []
    qsfp_absent_pattern = "X"*16
    for i2c_no in I2C_BUS_NO_LIST:
        check_cmd = "i2cdump -f -y {} 0x50".format(i2c_no)
        output = run_command(check_cmd, timeout=3)
        if re.search(qsfp_absent_pattern, output):
            qsfp_no_exist.append({"PORT ID":port_id, "I2C_BUS NO": i2c_no})
        port_id += 1
    if qsfp_no_exist:
        raise Exception("QSFP not exist in the ports: {}".format(qsfp_no_exist))

@logThis
def fenghuangv2checkQsfpAccess():

    port_id = 1
    qsfp_no_exist = []
    qsfp_absent_pattern = "X"*16
    for i2c_no in fhv2_I2C_BUS_NO_LIST:
        check_cmd = "i2cdump -f -y {} 0x50".format(i2c_no)
        output = run_command(check_cmd, timeout=3)
        if re.search(qsfp_absent_pattern, output):
            qsfp_no_exist.append({"PORT ID":port_id, "I2C_BUS NO": i2c_no})
        port_id += 1
    if qsfp_no_exist:
        raise Exception("QSFP not exist in the ports: {}".format(qsfp_no_exist))

@logThis
def checkLoadedDriver(mode):

    device.sendMsg("\n")
    run_command(KapokConst.STOP_ONIE_DISCOVERY_KEY, mode=Const.BOOT_MODE_ONIE, timeout=3)
    cpld_revision_pattern = 'CPLD Versions==.*?Revision Type\s+(\d+)"'
    booting_log = ""
    with open(server_tmp_file, "r") as fh:
        booting_log = fh.read()
    cpld_revision_type = ""
    cpld_revision_match = re.search(cpld_revision_pattern, booting_log, re.S)
    if cpld_revision_match:
        cpld_revision_type = cpld_revision_match.group(1)
        log.info("Found cpld_revision_type: {}".format(cpld_revision_type))
    else:
        log.info("Didn't find cpld_revision_type")
    CHECK_DRIVER_PATTERN = copy.deepcopy(LOADED_DRIVER_PATTERN)
    if cpld_revision_type == "19":
        CHECK_DRIVER_PATTERN.update({"psu_dps800"     : "psu_dps800.*?Live"})
    elif cpld_revision_type == "21":
        CHECK_DRIVER_PATTERN.update({"lm25066"        : "lm25066"})
    else:
        log.info("Check default driver info.")
    check_cmd = "lsmod"
    output = run_command(check_cmd, mode=Const.BOOT_MODE_ONIE, timeout=3)
    if mode in ("update", "rescue") and "ipd" in CHECK_DRIVER_PATTERN.keys():
        CHECK_DRIVER_PATTERN.pop("ipd")
    CommonLib.execute_check_dict("DUT", "", patterns_dict=CHECK_DRIVER_PATTERN, timeout=5,
                                check_output=output)
    CommonLib.execute_check_dict("DUT", "", patterns_dict=EXCLUDE_LOAD_DRIVER_PATTERN, timeout=5,
                                is_negative_test=True, check_output=output)

@logThis
def fhv2checkLoadedDriver(mode):

    device.sendMsg("\n")
    run_command(KapokConst.STOP_ONIE_DISCOVERY_KEY, mode=Const.BOOT_MODE_ONIE, timeout=3)
    cpld_revision_pattern = 'CPLD Versions==.*?Revision Type\s+(\d+)"'
    booting_log = ""
    with open(server_tmp_file, "r") as fh:
        booting_log = fh.read()
    cpld_revision_type = ""
    cpld_revision_match = re.search(cpld_revision_pattern, booting_log, re.S)
    if cpld_revision_match:
        cpld_revision_type = cpld_revision_match.group(1)
        log.info("Found cpld_revision_type: {}".format(cpld_revision_type))
    else:
        log.info("Didn't find cpld_revision_type")
    CHECK_DRIVER_PATTERN = copy.deepcopy(FENGHUANGV2_LOADED_DRIVER_PATTERN)
    if cpld_revision_type == "19":
        CHECK_DRIVER_PATTERN.update({"psu_dps800"     : "psu_dps800.*?Live"})
    elif cpld_revision_type == "21":
        CHECK_DRIVER_PATTERN.update({"lm25066"        : "lm25066"})
    else:
        log.info("Check default driver info.")
    check_cmd = "lsmod"
    output = run_command(check_cmd, mode=Const.BOOT_MODE_ONIE, timeout=3)
    if mode in ("update", "rescue") and "ipd" in CHECK_DRIVER_PATTERN.keys():
        CHECK_DRIVER_PATTERN.pop("ipd")
    CommonLib.execute_check_dict("DUT", "", patterns_dict=CHECK_DRIVER_PATTERN, timeout=5,
                                check_output=output)
    CommonLib.execute_check_dict("DUT", "", patterns_dict=EXCLUDE_LOAD_DRIVER_PATTERN, timeout=5,
                                is_negative_test=True, check_output=output)

@logThis
def checkDriverVersion():

    driver_version = CommonLib.get_swinfo_dict("BSP_DRIVER").get("newVersion", "NotFound")
    driver_path = CommonLib.get_swinfo_dict("BSP_DRIVER").get("localImageDir", "NotFound")
    check_cmd = "head releaseNotes | grep Version"
    version_pattern = {
            "Version <{}>".format(driver_version) : "Version.*?{}".format(CommonLib.escapeString(driver_version))
            }
    CommonLib.execute_check_dict("DUT", check_cmd, mode=Const.BOOT_MODE_ONIE, path =driver_path,
                                patterns_dict=version_pattern, timeout=5)

@logThis
def fhv2checkDriverVersion():

    driver_version = CommonLib.get_swinfo_dict("BSP_DRIVER").get("newVersion", "NotFound")
    driver_path = CommonLib.get_swinfo_dict("BSP_DRIVER").get("localImageDir", "NotFound")
    check_cmd = "head *eleaseNotes | grep Version"
    version_pattern = {
            "Version <{}>".format(driver_version) : "Version.*?{}".format(CommonLib.escapeString(driver_version))
            }
    CommonLib.execute_check_dict("DUT", check_cmd, mode=Const.BOOT_MODE_ONIE, path =driver_path,
                                patterns_dict=version_pattern, timeout=5)


@logThis
def setOnieFppMode(port_mode):
    set_fpp_mode_cmd = 'setenv onie_fpp "{}"'.format(port_mode)
    cmd_list = [set_fpp_mode_cmd, "saveenv"]
    output = run_command(cmd_list, timeout=60)
    if 'fenghuangv2' in devicename.lower():
        if port_mode == "sfp_detect" and "fail" in output: #replaceholder for "" mode
            log.info('sfp_detect mode is not present, use "" as default.')
            set_fpp_mode_cmd = 'setenv onie_fpp ""'
            cmd_list = [set_fpp_mode_cmd, "saveenv"]
            output += run_command(cmd_list, timeout=60)
    device.sendMsg("reset\n")
    output += device.readUntil(KapokConst.ONIE_DISCOVERY_PROMPT, timeout=KapokConst.BOOT_TIME)
    device.sendMsg("\n")
    output += run_command(KapokConst.STOP_ONIE_DISCOVERY_KEY, mode=Const.BOOT_MODE_ONIE, timeout=3)
    check_config_pattern = ""
    if port_mode in ("sfp_detect", ""):
        check_config_pattern = "(dynamic config\. mode is.*?1-1.*?;2-2:.*?;3-3.*?)\n"
    elif ":" in port_mode:
        check_config_pattern = "(dynamic config\. mode is.*?fec-def.*?)\n"
    elif "32" in port_mode:
        port_sum = port_mode.split("x")[0]
        bandwidth = port_mode.split("x")[1]
        check_config_pattern = "(dynamic config\. mode is.*?1-{}:.*?1x{}:fec-def.*?)\n".format(port_sum,bandwidth)
    elif port_mode in "64x100":
        check_config_pattern = "(dynamic config\. mode is.*?fec-def.*?)\n"
    elif port_mode in "64x100-1":
        check_config_pattern = "(dynamic config\. mode is.*?1-32:.*?2x100:.*?fec-dis.*?)\n"
    elif port_mode in "128x100" or "128x25" or "128x10":
        bandwidth = port_mode.split("x")[1]
        check_config_pattern = "(dynamic config\. mode is.*?1-32:.*?4x{}:.*?fec-def.*?)\n".format(bandwidth)

    else:
        port_sum = port_mode.split("x")[0]
        bandwidth = port_mode.split("x")[1]
        port_number = '{0:g}'.format(int(port_sum)/32)
        check_config_pattern =  "(dynamic config\. mode is.*?32.*?{}.*?{}G)".format(port_number, bandwidth)
    check_config_match = re.search(check_config_pattern, output)
    if check_config_match:
        log.info("Found {} port config setting message:\n  {}".format(port_mode,
            check_config_match.group(1)))
    else:
        log.info("Expect port config: {}".format(CommonLib.get_readable_strings(check_config_pattern)))
        raise Exception("Didn't found correct port config setting for mode : {}".format(port_mode))


@logThis
def checkFppInfo(port_mode):
    error_count = 0
    fpp_info_pattern = "(fpp[\d\-]+)\s+(.*?)TX bytes"
    ip_pattern = "inet addr:.*?Bcast:"
    output = run_command("ifconfig -a", mode=Const.BOOT_MODE_ONIE, timeout=5)
    fpp_ip_not_exist = []
    find_fpps = re.findall(fpp_info_pattern, output, re.S)
    if not find_fpps and port_mode not in ("sfp_detect", ):
        raise Exception("Didn't find any fpp interface.")
    else:
        #1. fpp num check.
        fpp_lst = []
        for fpp in find_fpps:
            fpp_num = fpp[0]
            fpp_lst.append(fpp_num)
        fpp_lst.sort()
        demo1Lst = []  #32
        demo2Lst = []  #64
        demo4Lst = []  #128
        demo5Lst = []  #10
        demo6Lst = []  #18
        demo7Lst = []  #86
        for i in range(1, 33):
            fpp1Val = 'fpp' + str(i)
            fpp2Val1 = 'fpp' + str(i) + '-1'
            fpp2Val2 = 'fpp' + str(i) + '-2'
            fpp2Val3 = 'fpp' + str(i) + '-3'
            fpp2Val4 = 'fpp' + str(i) + '-4'
            demo1Lst.append(fpp1Val); demo2Lst.append(fpp2Val1); demo2Lst.append(fpp2Val2); demo4Lst.append(fpp2Val1);
            demo4Lst.append(fpp2Val2); demo4Lst.append(fpp2Val3); demo4Lst.append(fpp2Val4)
        for i in range(1, 3):
            fpp5Val1 = 'fpp' + str(i) + '-1'
            fpp5Val2 = 'fpp' + str(i) + '-2'
            fpp5Val3 = 'fpp' + str(i) + '-3'
            fpp5Val4 = 'fpp' + str(i) + '-4'
            demo5Lst.append(fpp5Val1); demo5Lst.append(fpp5Val2); demo5Lst.append(fpp5Val3); demo5Lst.append(fpp5Val4)
        demo5Lst.append('fpp3')
        demo5Lst.append('fpp4')
        for i in range(1, 5):
            fpp6Val = 'fpp1-' + str(i)
            demo6Lst.append(fpp6Val)
            demo7Lst.append(fpp6Val)
        for i in range(2, 16):
            fpp6Val = 'fpp' + str(i)
            demo6Lst.append(fpp6Val)
            demo7Lst.append(fpp6Val)
        for i in range(16, 33):
            fpp7Val1 = 'fpp' + str(i) + '-1'
            fpp7Val2 = 'fpp' + str(i) + '-2'
            fpp7Val3 = 'fpp' + str(i) + '-3'
            fpp7Val4 = 'fpp' + str(i) + '-4'
            demo7Lst.append(fpp7Val1); demo7Lst.append(fpp7Val2); demo7Lst.append(fpp7Val3); demo7Lst.append(fpp7Val4)
        fpp_mode_lst = ['32x', '64x', '128x']
        demoLst = [demo1Lst, demo2Lst, demo4Lst]
        demo1Lst.sort(); demo2Lst.sort(); demo4Lst.sort(); demo5Lst.sort(); demo6Lst.sort(); demo7Lst.sort()
        for i in range(0, len(fpp_mode_lst)):
            mode_num = fpp_mode_lst[i].split('x')[0]
            if fpp_mode_lst[i] in port_mode:
                if len(fpp_lst) == int(mode_num):
                    log.success('Get the fpp num is [%d] pass.'%(len(fpp_lst)))
                    if fpp_lst == demoLst[i]:
                        log.success('Check fpp breakout mode pass, get value is %s'%fpp_lst)
                    else:
                        error_count += 1
                        log.fail('Check fpp breakout mode fail, getValue is %s, expectValue is %s'%(fpp_lst, demoLst[i]))
                else:
                    error_count += 1
                    log.fail('Get the fpp num is [%d] fail.'%(len(fpp_lst)))
        if port_mode == '1-32:4x100G' or port_mode == 'sfp_detect' or port_mode == empty_value:
            res = check_fpp_breakout_count(128, fpp_lst, demo4Lst)
            if res:
                error_count += 1
        elif port_mode == '1-2:4x100G;3-4:40G':
            res = check_fpp_breakout_count(10, fpp_lst, demo5Lst)
            if res:
                error_count += 1
        elif port_mode == '1:4x100G;2-15:100G':
            res = check_fpp_breakout_count(18, fpp_lst, demo6Lst)
            if res:
                error_count += 1
        elif port_mode == '1:4x100G;2-15:100G;16-32:4x25G':
            res = check_fpp_breakout_count(86, fpp_lst, demo7Lst)
            if res:
                error_count += 1
        #2. check speed
        speed_dict = {}
        cmd = 'cd ' + sdk_shell_path + '\n'
        run_command(cmd, mode=Const.BOOT_MODE_ONIE, timeout=5)
        cmd = './cls_shell ifcs show devport \n'
        output = run_command(cmd, mode=Const.BOOT_MODE_ONIE, timeout=20)
        p1 = r'\|\s+(\d+)\s+\|\s+ETH\s+\|.*\|\s+\(sysport:\s+(\d+)\)\s+\|\s+(\d+)G\s+\|'
        for line in output.splitlines():
            line = line.strip()
            match = re.search(p1, line, re.IGNORECASE)
            if match:
                port_num = match.group(2)
                port_speed = match.group(3)
                speed_dict[port_num] = port_speed
        log.info('#### Get the port speed: %s ####'%str(speed_dict))
        if len(speed_dict) == int(FPPS_COUNT_PATTERN[port_mode]):
            log.success('Get the fpp [%s] port num is [%d] pass.'%(port_mode, len(speed_dict)))
            if port_mode == '32x400':
                res = check_fpp_speed(speed_dict, fpp_speed_dict_check(port_mode))
                if res:
                    error_count += 1
            elif port_mode == '32x100':
                res = check_fpp_speed(speed_dict, fpp_speed_dict_check(port_mode))
                if res:
                    error_count += 1
            elif port_mode == '32x40':
                res = check_fpp_speed(speed_dict, fpp_speed_dict_check(port_mode))
                if res:
                    error_count += 1
            elif port_mode == '64x100' or port_mode == '64x100-1':
                res = check_fpp_speed(speed_dict, fpp_speed_dict_check(port_mode))
                if res:
                    error_count += 1
            elif port_mode == '128x100' or port_mode == '1-32:4x100G' or port_mode == 'sfp_detect' or port_mode == empty_value:
                res = check_fpp_speed(speed_dict, fpp_speed_dict_check(port_mode))
                if res:
                    error_count += 1
            elif port_mode == '128x25':
                res = check_fpp_speed(speed_dict, fpp_speed_dict_check(port_mode))
                if res:
                    error_count += 1
            elif port_mode == '128x10':
                res = check_fpp_speed(speed_dict, fpp_speed_dict_check(port_mode))
                if res:
                    error_count += 1
            elif port_mode == '1-2:4x100G;3-4:40G':
                res = check_fpp_speed(speed_dict, fpp_speed_dict_check(port_mode))
                if res:
                    error_count += 1
            elif port_mode == '1:4x100G;2-15:100G':
                res = check_fpp_speed(speed_dict, fpp_speed_dict_check(port_mode))
                if res:
                    error_count += 1
            elif port_mode == '1:4x100G;2-15:100G;16-32:4x25G':
                res = check_fpp_speed(speed_dict, fpp_speed_dict_check(port_mode))
                if res:
                    error_count += 1
        else:
            error_count += 1
            log.fail('Fail check the fpp [%s] port num, get [%d], expect [%d]'%(port_mode, len(speed_dict), int(FPPS_COUNT_PATTERN[port_mode])))
    if error_count:
        raise Exception('Failed run checkFppInfo')

@logThis
def check_fpp_speed(speedDict, demoDict):
    errCount = 0
    for key, value in speedDict.items():
        if demoDict[key] == value:
            log.success('Fpp Port-%s get the speed is %s'%(key, value))
        else:
            errCount += 1
            log.fail('Fail fpp port-%s speed, get [%s], expect [%s]'%(key, value, demoDict[key]))
    return errCount

@logThis
def check_fpp_breakout_count(numVal, fppLst, demoLst):
    errorCount = 0
    if len(fppLst) == numVal:
        log.success('Get the fpp num is [%d] pass.' % (len(fppLst)))
        if fppLst == demoLst:
            log.success('Check fpp breakout mode pass, get value is %s' % fppLst)
        else:
            errorCount += 1
            log.fail('Check fpp breakout mode fail, getValue is %s, expectValue is %s' % (fppLst, demoLst))
    else:
        errorCount += 1
        log.fail('Get the fpp num is [%d] fail.' % (len(fppLst)))
    return errorCount

@logThis
def checkQsfpType():
    pattern = "(P\d+)\s*:\s+(.*?)\n"
    cmd = "sfp_detect_tool"
    output = run_command(cmd, timeout=3)
    not_exist_list = []
    ports_info = re.findall(pattern, output)
    if ports_info:
        log.info("Found {} ports".format(len(ports_info)))
    else:
        raise Exception("Didn't found any QSFP modules in all ports.")
    for portno, qsfp_type in ports_info:
        if "NONE_READ" in qsfp_type:
            not_exist_list.append(portno)
    if not_exist_list:
        error_message = "Not found QSFP type info in {} ports,".format(len(not_exist_list))
        error_message += " such as: {}".format(not_exist_list[:5])
        raise Exception(error_message)


@logThis
def checkQsfpManufactureInfo():
    pattern = "(Port.*?):(.*?)(?=Port|ONIE)"
    cmd = "qsfp"
    output = run_command(cmd, timeout=30)
    not_exist_list = []
    ports_info = re.findall(pattern, output, re.S)
    if ports_info:
        log.info("Found {} ports".format(len(ports_info)))
    else:
        raise Exception("Didn't found any QSFP Manufacture info.")
    for portno, qsfp_type in ports_info:
        if "NO_MODULE" in qsfp_type:
            not_exist_list.append(portno)
    if not_exist_list:
        error_message = "Not found QSFP Manufacture info in {} ports,".format(len(not_exist_list))
        error_message += " such as: {}".format(not_exist_list[:5])
        raise Exception(error_message)

@logThis
def checkSfpInfo():
    cmd = 'sfp_eeprom'
    passCount = 0
    output = device.executeCmd(cmd)
    for line in output.splitlines():
        if re.search('Passed', line):
            passCount += 1
    if passCount == 32:
        log.info('check sfp info passed')
    else:
        log.fail('failed to check sfp info')
        raise Exception('failed to check sfp info')

@logThis
def changeModeTest():
    device.getPrompt(Const.ONIE_INSTALL_MODE)
    device.getPrompt(Const.BOOT_MODE_DIAGOS)
    out = device.executeCmd('pwd')
    log.cprint(out)
    device.getPrompt(Const.ONIE_INSTALL_MODE)
    device.getPrompt(Const.ONIE_RESCUE_MODE)
    device.getPrompt(Const.ONIE_UPDATE_MODE)
    device.getPrompt(Const.ONIE_INSTALL_MODE)
    device.getPrompt(Const.BOOT_MODE_UBOOT)
    device.getPrompt(Const.BOOT_MODE_DIAGOS)

@logThis
def check_platform_info():
    output = CommonLib.execute_command(cat_onie_platform_cmd,timeout=10)
    CommonLib.execute_check_dict("DUT", "", patterns_dict=cat_onie_platform_cmd_pattern, timeout=10, check_output=output)

@logThis
def check_sys_eeprom():
    output = CommonLib.execute_command(cat_sys_eeprom_cmd,timeout=10)
    CommonLib.execute_check_dict("DUT", "", patterns_dict=cat_sys_eeprom_cmd_pattern, timeout=10, check_output=output)

@logThis
def renameOnieImage(onieMode, toBackup=True):
    #server = DeviceMgr.getDevice('PC')
    server = Device.getDeviceObject('PC')
    time.sleep(60)
    server.executeCmd('cd ' + tftp_root_path, timeout=60)
    imageObj = SwImage.getSwImage(onieMode)
    image = imageObj.newImage
    if 'diagos' in image:
        res = image[11:]
        image = 'onie' + res
    if toBackup:
        server.executeCmd('mv {} {}'.format(image, image + '.bk'))
    else:
        server.executeCmd('mv {} {}'.format(image + '.bk', image))

@logThis
def setInterfaceIP():
    log.debug("Entering OnieLib class procedure: configInterfaceIP")
    deviceName = os.environ.get("deviceName", "")
    log.debug("deviceName: {}".format(deviceName))
    device_ip = CommonLib.Get_Not_Occupied_IP()
    if not device_ip:
        raise Exception("No available device_ip is found")
    else:
        set_ip_cmd = "ifconfig eth0 {} up".format(device_ip)
        device.executeCmd(set_ip_cmd)
        device.executeCmd('ifconfig')
        #log.info("Settting static IP: {}".format(device_ip))
        #ping server
        log.info('Ping server: ')
        CommonLib.exec_ping('DUT', server_ipv4, 3)

@logThis
def onieNOSSelfUpdate(update="new"):
    log.debug("Entering OnieLib class procedure: onieNOSSelfUpdate")
    updater_info_dict = CommonLib.get_swinfo_dict("DIAGOS")
    if update == "new":
        filename = updater_info_dict.get("newImage", "NotFound")
        file_path = updater_info_dict.get("hostImageDir", "NotFound")
    else:
        filename = updater_info_dict.get("oldImage", "NotFound")
        file_path = updater_info_dict.get("oldhostImageDir", "NotFound")
    server_ip = server_ipv4
    log.debug("Prompt: {}".format(device.promptOnie))
    if not server_ip:
        raise Exception("Didn't find server IP.")
    updater_cmd = "onie-nos-install tftp://{}/{}".format(server_ip, os.path.join(file_path, filename))
    expect_message = KapokConst.ONIE_DISCOVERY_PROMPT
    timeout_message = "tftp: timeout|tftp: read error"
    finish_prompt = "{}|{}".format(expect_message, timeout_message)
    retry = 3
    for i in range(retry):
        output = device.sendCmdRegexp(updater_cmd, finish_prompt, timeout=2000)
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

@logThis
def checkDiagOSVer():
    diag_os_version=CommonLib.get_swinfo_dict('DIAGOS').get('newVersion','NotFound')
    cmd ="get_versions"
    output= device.executeCmd(cmd, mode=Const.BOOT_MODE_DIAGOS).splitlines()
    if re.search(str(diag_os_version),str(output),re.I):
        log.success("DIAGOS Version matched: " +diag_os_version)
    else:
        raise Exception("DIAGOS version is mismatched")

@logThis
def autoUpdateInInstallMode():
    log.debug("Entering OnieLib class procedure: autoUpdateInInstallMode")
    device.getPrompt(Const.BOOT_MODE_UBOOT)
    log.info("Beginning to switch to ONIE update mode to do self updating...")
    device.sendMsg("run onie_bootcmd\n")
    device.readUntil("OK", timeout=600)
#    device.read_until_regexp(KapokConst.STOP_AUTOBOOT_PROMPT, timeout=KapokConst.BOOT_TIME)
    device.read_until_regexp(KapokConst.ONIE_DISCOVERY_PROMPT, timeout=KapokConst.BOOT_TIME)
    device.sendMsg("\n")
    device.sendMsg(KapokConst.STOP_ONIE_DISCOVERY_KEY)
    device.read_until_regexp(device.promptOnie, timeout=10)

@logThis
def ssh_connect():
    if 'tianhe' in devicename.lower():
        device_ip = get_eth_ip_addr('eth0')
    else:
        device_ip = getDeviceIp('eth0')
    if device_ip != 0:
        err_msg = 'Permission denied'
        unitObj = DeviceMgr.getDevice('DUT')
        oniePrmpt = unitObj.promptOnie
        deviceObj = Device.getDeviceObject('PC')
        cmd = 'ssh root@' + device_ip
        deviceObj.sendCmd(cmd, timeout=60)
        promptList = ["(y/n)", "(yes/no)", "password:", "ONIE"]
        patternList = re.compile('|'.join(promptList))
        output = deviceObj.read_until_regexp(patternList, 60)
        if re.search("(y/n)", output):
            deviceObj.transmit("yes")
            deviceObj.read_until_regexp('ONIE')
        elif re.search("(yes/no)", output):
            deviceObj.transmit("yes")
            deviceObj.read_until_regexp('ONIE')
        promptList1 = [err_msg, oniePrmpt]
        patternList1 = re.compile('|'.join(promptList1))
        output1 = deviceObj.read_until_regexp(patternList1, 60)
        if re.search(oniePrmpt, output1):
            log.success("SSH success from server to onie")
            cmd_list = [get_versions_cmd, ONIE_SYSEEPROM_CMD]
            for cmd in cmd_list:
                 unitObj.executeCmd(cmd)
            deviceObj.sendCmd("exit")
        elif re.search(err_msg, output1):
            log.fail("SSH Permission denied")
            raise Exception("Failed find error info.")
        else:
            log.fail("ssh failed from server to onie")
            raise Exception("Failed run ssh_connect")


@logThis
def onieSelfUpdateNoForce(cmd_tftp, image):
    device.executeCmd(cmd_tftp)
    sleep(10)
    cmd_update = "onie-self-update " + image + " --noforce \n"
    output = device.sendCmdRegexp(cmd_update, KapokConst.STOP_AUTOBOOT_PROMPT, timeout=1800)
    device.sendMsg(KapokConst.STOP_AUTOBOOT_KEY)
    device.sendMsg(ubootDefaultTool1 + '\n')
    device.sendMsg(ubootDefaultTool2 + '\n')
    device.sendMsg(ubootDefaultTool3 + '\n')
    device.read_until_regexp(KapokConst.STOP_AUTOBOOT_PROMPT, KapokConst.BOOT_TIME)
    device.sendMsg(KapokConst.STOP_AUTOBOOT_KEY)
    device.sendMsg(switch_onie_mode_cmd['rescue'] + '\n')
    device.read_until_regexp(ACTIVATE_CONSOLE_PROMPT, KapokConst.BOOT_TIME)
    device.sendMsg("\n")
    device.sendCmdRegexp(KapokConst.STOP_ONIE_DISCOVERY_KEY, device.promptOnie, timeout=10)
    return output

@logThis
def compareVersions(FW_names):
    global FW_CHANGED
    
    output = device.executeCmd("get_versions")
    FW_versions_after = []

    for name in FW_names:
        r = re.findall( name + ".*", output)[0]
        version = r.split(" ")[-1]
        if version.endswith("\r"):
            version = version[:len(version)-1]
        if "(" in version:
            version = version.split("(")[0]
        FW_versions_after.append(version)
    
    flag = 1
    FW_list = []
    for index in FW_CHANGED.keys():
        if FW_versions_after[index] != FW_CHANGED[index][1]:
            flag = 0
            FW_list.append(FW_CHANGED[index])
    if flag == 0:
        for each in FW_list:
            log.fail("{} was not updated to {} version.".format(each[0], each[1]))
        raise Exception("Some FW were not updated to required version.")
    else:
        for index in FW_CHANGED.keys():
            each = FW_CHANGED[index]
            log.success("{} was successfully updated to {} version.".format(each[0], each[1]))


@logThis
def getSwInfo(value):
    tftp_IP = DeviceMgr.getServerInfo('PC').managementIP
    updater_info_dict = CommonLib.get_swinfo_dict("ONIE_updater")
    if value == "new":
        filename = updater_info_dict.get("newImage", "NotFound")
        file_path = updater_info_dict.get("hostImageDir", "NotFound")
    else:
        filename = updater_info_dict.get("oldImage", "NotFound")
        file_path = updater_info_dict.get("oldhostImageDir", "NotFound")
    sw_image_path = os.path.join(file_path,filename)
    return (tftp_IP, sw_image_path)

@logThis
def checkFaultInUpgrading(output):
    fail_flag = 0
    r = re.findall(".* updated version and running version are the same", output)
    FW_name_list = []
    message = "Updating {} to the target version:"
    for each in r:
        a = each.split(" ")
        name = " ".join(a[:len(a)-8])
        FW_name_list.append(name)

    for each in FW_name_list:
        if output.count(message.format(each)) > 1:
            fail_flag = 1
            log.fail(each + " current & target versions are same. Still it is upgrading.")
    if fail_flag == 1:
        raise Exception("ERROR in upgrading the FWs. Upgrading even if the target and current versions are same.")

@logThis
def onieUpdateViaNoForceOnONIE(value):
    tftp_IP, sw_image_path = getSwInfo(value)
    cmd_tftp = tftp_get_onie_file_cmd.format(tftp_IP, sw_image_path)
    image = sw_image_path.split('/')[-1]
    output = onieSelfUpdateNoForce(cmd_tftp, image)

    #Check fault in upgrading process.
    checkFaultInUpgrading(output)

    #Check if upgrades are done correctly.
    splitOut = output.splitlines()
    sw_image_info = {}
    r = re.findall("running version : .*", output)
    for each in r:
        if each.endswith('\r'):
            each = each[:len(each)-1]
        index = splitOut.index(each)
        FW_name = splitOut[index-1].replace('=','')
        FW_name = FW_name.replace('Update','').strip()
        sw_image_info[FW_name] = [splitOut[index], splitOut[index+1]]

    for key in sw_image_info.keys():
        running = sw_image_info[key][0].split(':')[-1].strip()
        target = sw_image_info[key][1].split(':')[-1].strip()
        if running == target:
            log.info(key + " running and target version are same. --> " + target)
        else:
            log.info("{} running and target version mismatched. It will be updated from {} to {}.".format(key, running, target))
            FW_CHANGED[list(sw_image_info.keys()).index(key)] = [key, target]




@logThis
def getFileAndUpdate(value):
    a = DeviceMgr.getServerInfo('PC').managementIP
    updater_info_dict = CommonLib.get_swinfo_dict("ONIE_updater")
    if value == "new":
        filename = updater_info_dict.get("newImage", "NotFound")
        file_path = updater_info_dict.get("hostImageDir", "NotFound")
    else:
        filename = updater_info_dict.get("oldImage", "NotFound")
        file_path = updater_info_dict.get("oldhostImageDir", "NotFound")
    b = os.path.join(file_path, filename)
    cmd = "tftp -g {} -r {}".format(a,b)
    log.info('#### Download image cmd: %s ####'%cmd)
    # log.info(filename)
    run_command(cmd)
    cmd1 = "chmod 777 {}".format(filename)
    run_command(cmd1)
    cmd2 = "./" + "{}".format(filename)
    log.info('#### update onie cmd: %s ####'%cmd2)
    output = device.sendCmdRegexp(cmd2, KapokConst.STOP_AUTOBOOT_PROMPT, timeout=2000)
    device.sendMsg(KapokConst.STOP_AUTOBOOT_KEY)
    device.sendMsg(ubootDefaultTool1 + '\n')
    device.sendMsg(ubootDefaultTool2 + '\n')
    device.sendMsg(ubootDefaultTool3 + '\n')
    device.read_until_regexp(KapokConst.STOP_AUTOBOOT_PROMPT, KapokConst.BOOT_TIME)
    device.sendMsg(KapokConst.STOP_AUTOBOOT_KEY)
    device.sendMsg(switch_onie_mode_cmd['rescue'] + '\n')
    device.read_until_regexp(ACTIVATE_CONSOLE_PROMPT, KapokConst.BOOT_TIME)
    device.sendMsg("\n")
    onie_discovery_stop_cmd = KapokConst.STOP_ONIE_DISCOVERY_KEY
    device.sendCmdRegexp(onie_discovery_stop_cmd, device.promptOnie, timeout=10)
    ## add and check cpld version
    check_cpld_fw_in_onie_update(output)


def checkOnieSystemversion(value):
    log.debug("Entering OnieLib class procedure: checkOnieSysInfoV.")
    checkversionbeforethetest(value)
    cmd = "onie-sysinfo -v"
    cmd1= value+ "Version"
    oine_version = CommonLib.get_swinfo_dict("ONIE_Installer").get(cmd1, "NotFound")
    pattern = { oine_version: oine_version.replace(".", "\.")}
    CommonLib.execute_check_dict(Const.DUT, cmd, patterns_dict=pattern, timeout=10)






@logThis
def checkversionbeforethetest(value):
    cmdver = value + 'Version'
    sys_cpld_version = CommonLib.get_swinfo_dict('CPLD').get(cmdver).get('SYSCPLD')
    cpld_dict = CommonLib.get_swinfo_dict('CPLD')
    led_cpld1_version = cpld_dict.get(cmdver).get('LEDCPLD1')
    led_cpld2_version = cpld_dict.get(cmdver).get('LEDCPLD2')
    fan_cpld = cpld_dict.get(cmdver).get('FANCPLD')
    uboot_version = CommonLib.get_swinfo_dict("UBOOT").get(cmdver, "NotFound")
    onie_version = CommonLib.get_swinfo_dict("ONIE_Installer").get(cmdver, "NotFound")
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
        uc_app = CommonLib.get_swinfo_dict("UC").get(cmdver, "NotFound").get("uC_app")
        uC_bl = CommonLib.get_swinfo_dict("UC").get(cmdver, "NotFound").get("uC_bl")
        asc10_0 = CommonLib.get_swinfo_dict(ASC_type).get(cmdver, "NotFound").get("ASC10-0")
        asc10_1 = CommonLib.get_swinfo_dict(ASC_type).get(cmdver, "NotFound").get("ASC10-1")
        asc10_2 = CommonLib.get_swinfo_dict(ASC_type).get(cmdver, "NotFound").get("ASC10-2")
        hw_dict = {'uc_app': uc_app, 'uc_bl': uC_bl, 'ASC10-0': asc10_0, 'ASC10-1': asc10_1, 'ASC10-2': asc10_2,
                   'I2CFPGA': ic2fpga}
        cpld_version_dict = {'SYSCPLD': sys_cpld_version, 'SWLEDCPLD1': led_cpld1_version,
                             'SWLEDCPLD2': led_cpld2_version,'U-BOOT': uboot_version,'ONIE': onie_version,
                             'FANCPLD': fan_cpld}
        check_version_cmd = 'get_versions'
        output = device.executeCmd(check_version_cmd)
    elif "tianhe" in devicename.lower():
        dev_type = DeviceMgr.getDevice(devicename).get('cardType')
        if dev_type == '1PPS':
            ASC_type = dev_type + '_ASC'
            # ASC = CommonLib.get_swinfo_dict(ASC_type)
            ic2fpga = CommonLib.get_swinfo_dict(ASC_type).get("1pps", "NotFound")
        else:
            ASC_type = 'I2C_ASC'
            ic2fpga = CommonLib.get_swinfo_dict(ASC_type).get("fpga", "NotFound")
        asc10_0 = CommonLib.get_swinfo_dict(ASC_type).get(cmdver, "NotFound").get("ASC10-0")
        asc10_1 = CommonLib.get_swinfo_dict(ASC_type).get(cmdver, "NotFound").get("ASC10-1")
        asc10_2 = CommonLib.get_swinfo_dict(ASC_type).get(cmdver, "NotFound").get("ASC10-2")
        asc10_3 = CommonLib.get_swinfo_dict(ASC_type).get(cmdver, "NotFound").get("ASC10-3")
        asc10_4 = CommonLib.get_swinfo_dict(ASC_type).get(cmdver, "NotFound").get("ASC10-4")
        hw_dict = {'ASC10-0': asc10_0, 'ASC10-1': asc10_1, 'ASC10-2': asc10_2,
                   'ASC10-3': asc10_3, 'ASC10-4': asc10_4, '1PPSFPGA': ic2fpga}
        cpld_version_dict = {'SYSCPLD': sys_cpld_version, 'SWLEDCPLD1': led_cpld1_version,
                             'SWLEDCPLD2': led_cpld2_version, 'U-BOOT': uboot_version, 'ONIE': onie_version,
                             'FANCPLD': fan_cpld}
        check_version_cmd = 'get_versions'
        output = device.executeCmd(check_version_cmd)
    else:
        uc_app = CommonLib.get_swinfo_dict("UC").get(cmdver, "NotFound").get("uC_app")
        uC_bl = CommonLib.get_swinfo_dict("UC").get(cmdver, "NotFound").get("uC_bl")
        asc1 = CommonLib.get_swinfo_dict("ASC").get(cmdver, "NotFound").get("ASC1")
        asc2 = CommonLib.get_swinfo_dict("ASC").get(cmdver, "NotFound").get("ASC2")
        hw_dict = {'uc_app': uc_app, 'uc_bl': uC_bl, 'ASC1': asc1, 'ASC2': asc2}
        cpld_version_dict = {'SystemCPLD': sys_cpld_version, 'LEDCPLD1': led_cpld1_version,
                             'LEDCPLD2': led_cpld2_version, 'FANCPLD': fan_cpld,'U-BOOT': uboot_version,'ONIE': onie_version}
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
            passpattern.append('^' + keys_list[i] + '.*' + CommonLib.escapeString(values_list[i]))
    else:
        log.fail("get versions is failed")
        device.raiseException("Failure while get versions info")
    log.debug('passpattern=%s' % passpattern)
    passCount = 0
    match_list = list()
    for line in output.splitlines():
        line = line.strip()
        for pattern in passpattern:
            if re.search(pattern, line, re.IGNORECASE):
                log.debug('the matched version:%s' % line)
                match_list.append(pattern)
                passCount += 1
    if passCount == len(passpattern):
        log.success("verify version is passed")
    else:
        log.fail("not match pattern is: %s" % list(set(passpattern) - set(match_list)))
        device.raiseException("Failure while verify versions info")
    return
                                 
@logThis
def OnieUpdate(update):
    error_count = 0
    updater_info_dict = CommonLib.get_swinfo_dict("ONIE_updater")
    if update == "new":
        filename = updater_info_dict.get("newImage", "NotFound")
        file_path = updater_info_dict.get("hostImageDir", "NotFound")
    else:
        filename = updater_info_dict.get("oldImage", "NotFound")
        file_path = updater_info_dict.get("oldhostImageDir", "NotFound")
    server_ip = CommonLib.get_device_info("PC").get("managementIP","")
    log.debug("Prompt: {}".format(device.promptOnie))
    updater_cmd = "tftp -g {} -r {}".format(server_ip, os.path.join(file_path, filename))
    update_pattern = "100%"
    device.read_until_regexp(device.promptOnie)
    output = device.executeCmd(updater_cmd, timeout=600)
    if update_pattern in output:
        log.success("Update pattern {} matched".format(update_pattern))
        device.read_until_regexp(device.promptOnie)
        permission_cmd = "chmod 777 {}".format(filename)
        output = device.sendCmdRegexp(permission_cmd, device.promptOnie, timeout=15)
        noforce_cmd = "./{} --noforce".format(filename)
        if device.promptOnie:
            # output = device.sendCmdRegexp(noforce_cmd, KapokConst.ONIE_DISCOVERY_PROMPT, timeout=2000)
            #device.read_until_regexp(KapokConst.ONIE_DISCOVERY_PROMPT, timeout=KapokConst.BOOT_TIME)
            output = device.sendCmdRegexp(noforce_cmd, KapokConst.STOP_AUTOBOOT_PROMPT, timeout=2000)
            device.sendMsg(KapokConst.STOP_AUTOBOOT_KEY)
            device.sendMsg(ubootDefaultTool1 + '\n')
            device.sendMsg(ubootDefaultTool2 + '\n')
            device.sendMsg(ubootDefaultTool3 + '\n')
            device.read_until_regexp(KapokConst.ONIE_DISCOVERY_PROMPT, KapokConst.BOOT_TIME)
            device.sendMsg("\n")
            device.sendMsg(KapokConst.STOP_ONIE_DISCOVERY_KEY+"\n")
            device.read_until_regexp(device.promptOnie, timeout=10)
            device.sendMsg("\n")
            log.info('################# Start to check the all modules fw update info ####################')
            ###First check version if they are the same, then check the keyword 'same'
            current_pattern = r'running version :\s+([\w.]+)'
            target_pattern = r'target version :\s+([\w.]+)'
            if '51.2t' in device.name:
                p1 = 'sysCPLD Update[\s\S]+COME CPLD Update'
                p2 = 'COME CPLD Update[\s\S]+FANCPLD Update'
                p3 = 'FANCPLD Update[\s\S]+1PPS-FPGA_0 Update'
                p4 = '1PPS-FPGA_0 Update[\s\S]+1PPS-FPGA_1 Update'
                p5 = '1PPS-FPGA_1 Update[\s\S]+ASC10-0 Update'
                p6 = 'ASC10-0 Update[\s\S]+ASC10-1 Update'
                p7 = 'ASC10-1 Update[\s\S]+ASC10-2 Update'
                p8 = 'ASC10-2 Update[\s\S]+ASC10-3 Update'
                p9 = 'ASC10-3 Update[\s\S]+ASC10-4 Update'
                p10 = 'ASC10-4 Update[\s\S]+ASC10-5 Update'
                p11 = 'ASC10-5 Update[\s\S]+ASC10-6 Update'
                p12 = 'ASC10-6 Update[\s\S]+Please power down your machine and restart'
                logLst = [p1, p2, p3, p4, p5, p6, p7, p8, p9, p10, p11, p12]
                pat1 = 'sysCPLD updated version and running version are the same'
                pat2 = 'COME CPLD updated version and running version are the same'
                pat3 = 'FANCPLD updated version and running version are the same'
                pat4 = '1PPS-FPGA updated version and running version are the same'
                pat5 = 'ASC10-0 updated version and running version are the same'
                pat6 = 'ASC10-1 updated version and running version are the same'
                pat7 = 'ASC10-2 updated version and running version are the same'
                pat8 = 'ASC10-3 updated version and running version are the same'
                pat9 = 'ASC10-4 updated version and running version are the same'
                pat10 = 'ASC10-5 updated version and running version are the same'
                pat11 = 'ASC10-6 updated version and running version are the same'
                patternLst = [pat1, pat2, pat3, pat4, pat4, pat5, pat6, pat7, pat8, pat9, pat10, pat11]
            elif 'tianhe' in device.name:
                p1 = 'SYSFPGA Update[\s\S]+COME CPLD Update'
                p2 = 'COME CPLD Update[\s\S]+CPLD2&3 Update'
                p3 = 'CPLD2&3 Update[\s\S]+FANCPLD Update'
                p4 = 'FANCPLD Update[\s\S]+1PPS-FPGA Update'
                p5 = '1PPS-FPGA Update[\s\S]+ASC10-0 Update'
                p6 = 'ASC10-0 Update[\s\S]+ASC10-1 Update'
                p7 = 'ASC10-1 Update[\s\S]+ASC10-2 for 1PPS Update'
                p8 = 'ASC10-2 for 1PPS Update[\s\S]+Come ASC0 Update'
                p9 = 'Come ASC0 Update[\s\S]+Come ASC1 Update'
                p10 = 'Come ASC1 Update[\s\S]+Fws update done'
                logLst = [p1, p2, p3, p4, p5, p6, p7, p8, p9, p10]
                pat1 = 'SYSFPGA updated version and running version are the same'
                pat2 = 'COME CPLD updated version and running version are the same'
                pat3 = 'CPLD2&3 updated version and running version are the same'
                pat4 = 'FANCPLD updated version and running version are the same'
                pat5 = '1PPS-FPGA updated version and running version are the same'
                pat6 = 'ASC10-0 updated version and running version are the same'
                pat7 = 'ASC10-1 updated version and running version are the same'
                pat8 = 'ASC10-2 updated version and running version are the same'
                pat9 = 'COME-ASC-0 updated version and running version are the same'
                pat10 = 'COME-ASC-1 updated version and running version are the same'
                patternLst = [pat1, pat2, pat3, pat4, pat5, pat6, pat7, pat8, pat9, pat10]
            elif 'tigrisv2' in device.name:
                p1 = 'SYSFPGA Update[\s\S]+FPGA Update'
                p2 = 'FPGA Update[\s\S]+COME CPLD Update'
                p3 = 'COME CPLD Update[\s\S]+FAN CPLD Update'
                p4 = 'FAN CPLD Update[\s\S]+ASC10-0 baseboard Update'
                p5 = 'ASC10-0 baseboard Update[\s\S]+ASC10-1 for baseboard Update'
                p6 = 'ASC10-1 for baseboard Update[\s\S]+ASC10-2 for baseboard Update'
                p7 = 'ASC10-2 for baseboard Update[\s\S]+Come ASC0 Update'
                p8 = 'Come ASC0 Update[\s\S]+Come ASC1 Update'
                p9 = 'Come ASC1 Update[\s\S]+The system is going down NOW'
                logLst = [p1, p2, p3, p4, p5, p6, p7, p8, p9]
                pat1 = 'SYSFPGA updated version and running version are the same'
                pat2 = 'FPGA updated version and running version are the same'
                pat3 = 'COME CPLD updated version and running version are the same'
                pat4 = 'FAN CPLD updated version and running version are the same'
                pat5 = 'ASC10-0 updated version and running version are the same'
                pat6 = 'ASC10-1 updated version and running version are the same'
                pat7 = 'ASC10-2 updated version and running version are the same'
                pat8 = 'COME-ASC-0 updated version and running version are the same'
                pat9 = 'COME-ASC-1 updated version and running version are the same'
                patternLst = [pat1, pat2, pat3, pat4, pat5, pat6, pat7, pat8, pat9]
            elif 'fenghuangv2' in device.name:
                p1 = 'CPLD2&3 Update[\s\S]+FANCPLD Update'
                p2 = 'FANCPLD Update[\s\S]+I2CFPGA REV2 Update'
                p3 = 'I2CFPGA REV2 Update[\s\S]+ASC10-0 Update'
                p4 = 'ASC10-0 Update[\s\S]+ASC10-1 Update'
                p5 = 'ASC10-1 Update[\s\S]+ASC10-2 for I2C FPGA Update'
                p6 = 'ASC10-2 for I2C FPGA Update[\s\S]+The system is going down NOW'
                logLst = [p1, p2, p3, p4, p5, p6]
                pat1 = 'CPLD2&3 updated version and running version are the same'
                pat2 = 'FANCPLD updated version and running version are the same'
                pat3 = 'I2CFPGA REV2 updated version and running version are the same'
                pat4 = 'ASC10-0 updated version and running version are the same'
                pat5 = 'ASC10-1 updated version and running version are the same'
                pat6 = 'ASC10-2 updated version and running version are the same'
                patternLst = [pat1, pat2, pat3, pat4, pat5, pat6]
            for i in range(0, len(logLst)):
                res = re.search(logLst[i], output)
                getString = res.group(0)
                res1 = re.search(current_pattern, getString)
                res2 = re.search(target_pattern, getString)
                if res1:
                    current_ver = res1.group(1)
                if res2:
                    target_ver = res2.group(1)
                if current_ver == target_ver:
                    if patternLst[i] in getString:
                        log.success('Check device [%s] current and target version [%s] is the same!' % (logLst[i].split()[0], target_ver))
                    else:
                        error_count += 1
                        log.fail('Device [%s] current [%s] and target [%s] ver is same, but it maybe still update!!!' % (logLst[i].split()[0], current_ver, target_ver))
                else:
                    log.info('Device [%s] current [%s] and target [%s] version is diff, need to update!' % (logLst[i].split()[0], current_ver, target_ver))
            if error_count:
                raise Exception("Device versions matched to latest but Upgrade is still progressing...")
        else:
            raise Exception("Onie Update via noforce Failed")
    else:
        raise Exception("Onie Update pattern match fail")


@logThis
def CheckFwVersion(Version):
    cmd = get_versions_cmd
    Image_info_dict = CommonLib.get_swinfo_dict("ONIE_updater")
    onie_version = Image_info_dict.get("newVersion", "NotFound")
    cpld_version = CommonLib.get_swinfo_dict("CPLD")
    sys_cpld_version = cpld_version.get("newVersion").get("SYSCPLD")
    fan_cpld_version = cpld_version.get("newVersion").get("FANCPLD")
    led_cpld1_version =cpld_version.get('newVersion').get('LEDCPLD1')
    led_cpld2_version =cpld_version.get('newVersion').get('LEDCPLD2')
    devicename = os.environ.get("deviceName", "")
    if "fenghuangv2" in devicename.lower():
        dev_type = DeviceMgr.getDevice(devicename).get('cardType')
        if dev_type == '1PPS':
            ASC_type = dev_type + '_ASC'
            ASC = CommonLib.get_swinfo_dict(ASC_type)
            i2c_fpga_version = CommonLib.get_swinfo_dict(ASC_type).get("1pps", "NotFound")
            if Version == 'new':
                i2c_asc10_0 = CommonLib.get_swinfo_dict(ASC_type).get('newVersion').get('ASC10-0',"NotFound")
                i2c_asc10_1 = CommonLib.get_swinfo_dict(ASC_type).get('newVersion').get('ASC10-1',"NotFound")
                i2c_asc10_2 = CommonLib.get_swinfo_dict(ASC_type).get('newVersion').get('ASC10-2',"NotFound")
            else:
                i2c_asc10_0 = CommonLib.get_swinfo_dict(ASC_type).get('oldVersion').get('ASC10-0',"NotFound")
                i2c_asc10_1 = CommonLib.get_swinfo_dict(ASC_type).get('oldVersion').get('ASC10-1',"NotFound")
                i2c_asc10_2 = CommonLib.get_swinfo_dict(ASC_type).get('oldVersion').get('ASC10-2',"NotFound")
        else:
            ASC_type = 'I2C_ASC'
            i2c_fpga_version = CommonLib.get_swinfo_dict(ASC_type).get("fpga", "NotFound")
            if Version == 'new':
                i2c_asc10_0 = CommonLib.get_swinfo_dict(ASC_type).get('newVersion').get('ASC10-0',"NotFound")
                i2c_asc10_1 = CommonLib.get_swinfo_dict(ASC_type).get('newVersion').get('ASC10-1',"NotFound")
                i2c_asc10_2 = CommonLib.get_swinfo_dict(ASC_type).get('newVersion').get('ASC10-2',"NotFound")
            else:
                i2c_asc10_0 = CommonLib.get_swinfo_dict(ASC_type).get('oldVersion').get('ASC10-0',"NotFound")
                i2c_asc10_1 = CommonLib.get_swinfo_dict(ASC_type).get('oldVersion').get('ASC10-1',"NotFound")
                i2c_asc10_2 = CommonLib.get_swinfo_dict(ASC_type).get('oldVersion').get('ASC10-2',"NotFound")
    if Version == 'new':
        if "tianhe" in devicename.lower():
            ASCObj = CommonLib.get_swinfo_dict("1PPS_ASC")
            i2c_asc10_0 = ASCObj.get('newVersion').get('ASC10-0',"NotFound")
            i2c_asc10_1 = ASCObj.get('newVersion').get('ASC10-1',"NotFound")
            i2c_asc10_2 = ASCObj.get('newVersion').get('ASC10-2',"NotFound")
            i2c_asc10_3 = ASCObj.get('newVersion').get('ASC10-3',"NotFound")
            i2c_asc10_4 = ASCObj.get('newVersion').get('ASC10-4',"NotFound")
            i2c_fpga_version = ASCObj.get('1pps',"NotFound")
            #onie_version = Image_info_dict.get("newVersion", "NotFound")
            onie_version_pattern = {"ONIE  %s" % (onie_version): "^ONIE\s+%s" % (onie_version),
                                    "SYSCPLD  %s" % (sys_cpld_version): "^SYSCPLD\s+%s" % (sys_cpld_version),
                                    "FANCPLD  %s" % (fan_cpld_version): "^FANCPLD\s+%s" % (fan_cpld_version),
                                    "SWLEDCPLD1  %s" % (led_cpld1_version): "^SWLEDCPLD1\s+%s" % (led_cpld1_version),
                                    "SWLEDCPLD2  %s" % (led_cpld2_version): "^SWLEDCPLD2\s+%s" % (led_cpld2_version),
                                    "ASC10-0  %s" % (i2c_asc10_0): "^ASC10-0\s+%s" % (i2c_asc10_0),
                                    "ASC10-1  %s" % (i2c_asc10_1): "^ASC10-1\s+%s" % (i2c_asc10_1),
                                    "ASC10-2  %s" % (i2c_asc10_2): "^ASC10-2\s+%s" % (i2c_asc10_2),
                                    "ASC10-3  %s" % (i2c_asc10_3): "^ASC10-3\s+%s" % (i2c_asc10_3),
                                    "ASC10-4  %s" % (i2c_asc10_4): "^ASC10-4\s+%s" % (i2c_asc10_4),
                                    "1PPSFPGA  %s" % (i2c_fpga_version): "^1PPSFPGA\s+%s" % (i2c_fpga_version)}
        else:
            onie_version = Image_info_dict.get("newVersion", "NotFound")
            onie_version_pattern = { "ONIE  %s"%(onie_version): "^ONIE\s+%s"%(onie_version),
                                 "SYSCPLD  %s"%(sys_cpld_version): "^SYSCPLD\s+%s"%(sys_cpld_version),
                                 "FANCPLD  %s"%(fan_cpld_version): "^FANCPLD\s+%s"%(fan_cpld_version),
                                 "SWLEDCPLD1  %s"%(led_cpld1_version): "^SWLEDCPLD1\s+%s"%(led_cpld1_version),
                                 "SWLEDCPLD2  %s"%(led_cpld2_version): "^SWLEDCPLD2\s+%s"%(led_cpld2_version),
                                 "ASC10-0  %s"%(i2c_asc10_0): "^ASC10-0\s+%s"%(i2c_asc10_0),
                                 "ASC10-1  %s"%(i2c_asc10_1): "^ASC10-1\s+%s"%(i2c_asc10_1),
                                 "ASC10-2  %s"%(i2c_asc10_2): "^ASC10-2\s+%s"%(i2c_asc10_2),
                                 "I2CFPGA  %s"%(i2c_fpga_version): "^I2CFPGA\s+%s"%(i2c_fpga_version)}
    else:
         onie_version = Image_info_dict.get("oldVersion", "NotFound")
         onie_version_pattern = { "ONIE  %s"%(onie_version): "^ONIE\s+%s"%(onie_version)}
    CommonLib.execute_check_dict('DUT', cmd, mode=Const.BOOT_MODE_ONIE, patterns_dict=onie_version_pattern,
                                 timeout=6)

@logThis
def switch_onie_folder_path(path):
    cmd = 'cd ' + path
    p1 = "No such file or directory"
    output = device.executeCommand(cmd, device.promptOnie)
    if re.search(p1, output):
        log.fail('switch folder fail!')
        raise Exception('Change %s path failed!'%(path))
    else:
        log.info('Switch the folder successfully!')

@logThis
def delete_image_file(path, fileLst):
    for img in fileLst:
        cmd = 'rm -rf ' + path + '/' + img
        device.executeCmd(cmd, timeout=60)

@logThis
def tftp_download_image_file(hostPath, imageFileLst):
    error_count = 0
    p1 = '100%'
    #1. create unit folder
    cmd = 'mkdir -p ' + hostPath
    device.executeCmd(cmd)
    #2. copy image
    switch_onie_folder_path(hostPath)
    for img in imageFileLst:
        cmd = 'tftp -g ' + server_ipv4 + ' -r ' + img
        output = device.executeCmd(cmd, timeout=120)
        res = re.search(p1, output)
        if res:
            log.success('Copy Image [%s] successfully!'%img)
        else:
            error_count += 1
            log.fail('copy [%s] fail'%img)
    if error_count > 0:
        raise Exception('Copy image failed!')

@logThis
def tianhe_upgrade_cpld(tool, optionLst, imgLst):
    switch_onie_folder_path(localCpldPath)
    error_count = 0
    p1 = r'\| PASS! \|'
    for i in range(0, len(imgLst)):
        time.sleep(2)
        cmd = tool + optionLst[i] + imgLst[i]
        if i == 1:
            device.executeCmd(disableFCS, timeout=60)
        output = device.executeCmd(cmd, timeout=600)
        res = re.search(p1, output)
        if res:
            log.success('update [%s] image successfully'%imgLst[i])
        else:
            error_count += 1
            log.fail('update [%s] image fail'%imgLst[i])
    if error_count > 0:
        raise Exception('Failed run tianhe_upgrade_cpld')

@logThis
def get_mtd_device(pattern):
    output = device.executeCmd(mtdCmd, timeout=60)
    res = re.search(pattern, output)
    if res:
        mtdDev = res.group(1)
        log.info('get mtd device.')
    else:
        log.fail('Can not get mtd device.')
        raise Exception('Failed run get_mtd_device')
    return mtdDev

@logThis
def pps_fpga_upgrade_test(tool, option, img):
    p1 = r'Verifying kb:.*\(100%\)'
    devTool = get_mtd_device(fpgaDevPattern)
    cmd = tool + option + img + ' /dev/' + devTool
    output = device.executeCmd(cmd, timeout=300)
    res = re.search(p1, output)
    if res:
        log.success('Update 1pps fpga [%s] successfully'%img)
    else:
        log.fail('Update 1pps fpga [%s] fail.'%img)
        raise Exception('Failed run pps_fpga_upgrade_test')

@logThis
def onie_auto_update_in_install_mode():
    device.getPrompt(Const.BOOT_MODE_UBOOT)
    log.info("Beginning to switch to ONIE update mode to do self updating...")
    p1 = 'ONIE: NOS install successful: tftp://' + server_ipv4 + '/' + INSTALLER_FILE_SEARCH_ORDER[1]
    device.sendCmdRegexp("run onie_bootcmd\n", p1, timeout=1200)
    device.read_until_regexp(KapokConst.STOP_AUTOBOOT_PROMPT, timeout=KapokConst.BOOT_TIME)
    device.sendMsg(KapokConst.STOP_AUTOBOOT_KEY)
    device.sendCmdRegexp("run diag_bootcmd\n", ACTIVATE_CONSOLE_PROMPT, timeout=900)
    # device.read_until_regexp(KapokConst.ONIE_DISCOVERY_PROMPT, timeout=KapokConst.BOOT_TIME)
    device.sendMsg("\n")
    device.sendMsg(KapokConst.STOP_ONIE_DISCOVERY_KEY)
    device.read_until_regexp(device.promptDiagOS, timeout=10)

@logThis
def check_driver_information_test(typeValue, driveTool, patternLst):
    #1. enter uboot mode
    device.getPrompt(Const.BOOT_MODE_UBOOT)
    #2. run onie mode and check driver info.
    cmd = 'run ' + typeValue
    error_count = 0
    p2 = r'Version <([\d.]+)>'
    device.sendCmdRegexp(cmd, ACTIVATE_CONSOLE_PROMPT, timeout=600)
    device.sendMsg("\n")
    device.sendMsg(KapokConst.STOP_ONIE_DISCOVERY_KEY)
    device.read_until_regexp(device.promptOnie, timeout=10)
    time.sleep(20)
    #3. lsmod dirive check
    switch_onie_folder_path(onieDrivePath)
    output = device.executeCmd(driveTool, Const.BOOT_MODE_ONIE, timeout=300)
    for line in patternLst:
        res = re.search(line, output)
        if res:
            log.success('Find drive info: %s'%res.group(0))
        else:
            error_count += 1
            log.fail('Can not find the drive info: %s'%res.group(0))
    #4. check drive version
    #driveObj = CommonLib.get_swinfo_dict("BSP_DRIVER")
    #expect_drive_ver = driveObj.get("newVersion", "NotFound")
    #output = device.executeCmd(readDriveVer, Const.BOOT_MODE_ONIE, timeout=300)
    #mat = re.search(p2, output)
    #if mat:
    #    getDriveVer = mat.group(1)
    #    if getDriveVer == expect_drive_ver:
    #        log.success('Check drive version pass, getVer: %s, expectVer: %s'%(getDriveVer, expect_drive_ver))
    #    else:
    #        error_count += 1
    #        log.fail('Check drive version fail, getVer: %s, expectVer: %s'%(getDriveVer, expect_drive_ver))
    if error_count:
        raise Exception('Failed run check_driver_information_test')

@logThis
def check_onie_rescue_booting_mode():
    error_count = 0
    p1 = 'ONIE: Starting ONIE Service Discovery'
    p2 = 'discover: Rescue mode detected.  Installer disabled.'
    device.getPrompt(Const.BOOT_MODE_UBOOT)
    cmd = switch_onie_mode_cmd['rescue']
    output = device.sendCmdRegexp(cmd, ACTIVATE_CONSOLE_PROMPT, timeout=600)
    device.sendMsg("\n")
    device.sendMsg(KapokConst.STOP_ONIE_DISCOVERY_KEY)
    device.read_until_regexp(device.promptOnie, timeout=10)
    if re.search(p1, output):
        error_count += 1
        log.fail('discovery service should be closed.')
    if re.search(p2, output):
        log.success('Switch to rescue mode successfully, installer is disabled.')
    else:
        error_count += 1
        log.fail('Switch to rescue mode fail.')
    if error_count:
        raise Exception('Failed run check_onie_rescue_booting_mode')

@logThis
def compare_onie_mac_address_in_rescue_mode(tool, demoMac):
    error_count = 0
    p1 = r'HWaddr\s+([\w:]+)'
    output = CommonLib.execute_command(tool, timeout=10)
    if re.search(demoMac, output):
        log.success('Get the eth1addr: %s'%demoMac)
    else:
        error_count += 1
        log.fail('Do not find eth1addr: %s'%demoMac)
    output2 = CommonLib.execute_command('ifconfig eth0', timeout=10)
    res = re.search(p1, output2)
    if res:
        get_eth0_mac = res.group(1).lower()
        if get_eth0_mac == demoMac:
            error_count += 1
            log.fail('Fail, the eth0 mac should be fixed.')
        else:
            log.success('Check eth0 mac address pass.')
    else:
        error_count += 1
        log.fail('Can not match mac address.')
    if error_count:
        raise Exception('Failed run compare_onie_mac_address_in_uboot_mode.')

@logThis
def check_some_test_parameters_in_uboot_mode(tool, patterhLst):
    error_count = 0
    output = CommonLib.execute_command(tool, timeout=60)
    for pattern in patterhLst:
        res = re.search(pattern, output)
        if res:
            log.success('Get the set test env param [%s].'%pattern)
        else:
            error_count += 1
            log.fail('Can not find [%s].'%pattern)
    if error_count:
        raise Exception('Failed run check_some_test_parameters_in_uboot_mode')

#@logThis
#def check_onie_rescue_booting_mode():
#    error_count = 0
#    p1 = 'ONIE: Starting ONIE Service Discovery'
#    p2 = 'discover: Rescue mode detected.  Installer disabled.'
#    device.getPrompt(Const.BOOT_MODE_UBOOT)
#    cmd = switch_onie_mode_cmd['rescue']
#    output = device.sendCmdRegexp(cmd, ACTIVATE_CONSOLE_PROMPT, timeout=600)
#    device.sendMsg("\n")
#    device.sendMsg(KapokConst.STOP_ONIE_DISCOVERY_KEY)
#    device.read_until_regexp(device.promptOnie, timeout=10)
#    if re.search(p1, output):
#        error_count += 1
#        log.fail('discovery service should be closed.')
#    if re.search(p2, output):
#        log.success('Switch to rescue mode successfully, installer is disabled.')
#    else:
#        error_count += 1
#        log.fail('Switch to rescue mode fail.')
#    if error_count:
#        raise Exception('Failed run check_onie_rescue_booting_mode')

@logThis
def get_dhcp_ip_and_ping_server():
    pattern = '5 packets transmitted, 5 packets received, 0% packet loss'
    device.sendMsg('\r\n')
    time.sleep(1)
    msgStr = device.readMsg()
    if re.search(device.promptDiagOS, msgStr):
        if "tigrisv2" in devicename.lower():
            cmd = 'dhcp'
        else:
            cmd = 'udhcpc'
    else:
        cmd = 'udhcpc'
    CommonLib.execute_command(cmd, timeout=120)
    CommonLib.execute_command('ifconfig', timeout=120)
    pingCmd = 'ping ' + server_ipv4 + ' -c 5'
    output = CommonLib.execute_command(pingCmd, timeout=120)
    if re.search(pattern, output):
        log.success('Ping server ip pass.')
    else:
        log.fail('Ping server ip fail.')
        raise Exception('Failed run get_dhcp_ip_and_ping_server')

@logThis
def get_eth_ip_addr(eth_device):
    p1 = r'inet addr:([\d.]+)  Bcast'
    cmd = 'ifconfig ' + eth_device
    output = run_command(cmd)
    res = re.search(p1, output)
    if res:
        get_ip = res.group(1)
        log.info('#### get unit ip is %s ####'%get_ip)
        return get_ip
    else:
        raise Exception('Failed run get_eth_ip_addr')

@logThis
def read_and_backup_tlv_eeprom(sysCmd):
    cmd_list = [ sysCmd ]
    saveDUTInfoToServer(cmd_list, mode=Const.ONIE_RESCUE_MODE, server_file=server_tmp_file)

@logThis
def check_eeprom_wp_status(enableValue, wpCmd):
    error_count = 0
    p1 = '^\d'
    cmd = 'cat ' + wpCmd
    output = CommonLib.execute_command(cmd, timeout=60)
    for line in output.splitlines():
        line = line.strip()
        res = re.search(p1, line)
        if res:
            if res.group(0) == enableValue:
                log.success('check eeprom wp status is %s'%(res.group(0)))
            else:
                error_count += 1
                log.fail('check eeprom wp status [%s] fail.'%(res.group(0)))
    if error_count:
        raise Exception('Failed run check_eeprom_wp_status')

@logThis
def check_store_tlv_system_eeprom(sysBK, testValue='False'):
    p1 = r'(0x\w{2})[ \t]+\d+[ \t]+(.*)'
    #p2 = r'0x01|0x03|0xFE|0x2F|0xFD'
    p2 = r'0x01|0x03|0xFE|0x2F'
    store_dict = {}
    ##1. get eeprom value
    if testValue == 'True':
        cmd = sysBK
        output = CommonLib.execute_command(cmd, timeout=60)
        for line in output.splitlines():
            line = line.strip()
            res = re.search(p1, line)
            if res:
                if re.search(p2, line):
                    continue
                expectKey = res.group(1)
                expectValue = res.group(2)
                store_dict[expectKey] = expectValue
    else:
        log.info('#### get server side tlv store eeprom %s ####'%sysBK)
        with open(sysBK) as ff:
            for line in ff:
                line = line.strip()
                res = re.search(p1, line)
                if res:
                    if re.search(p2, line):
                        continue
                    expectKey = res.group(1)
                    expectValue = res.group(2)
                    store_dict[expectKey] = expectValue
    log.info('#### get the eeprom value as the below: ####')
    log.info(store_dict)
    return store_dict

@logThis
def write_tlv_system_eeprom(testValue, writeCmd):
    error_count = 0
    log.info('#### 1. Will write the below of TEST demo tlv eeprom value:')
    log.info(testValue)
    log.info('#### 2. Start to write TEST demo tlv eeprom: ####')
    for key, value in testValue.items():
        cmd = writeCmd + key + '=' + value
        CommonLib.execute_command(cmd, timeout=120)
    log.info('#### 3. read TEST demo tlv eeprom value dict ####')
    read_test_value_dict = check_store_tlv_system_eeprom(ONIE_SYSEEPROM_CMD, 'True')
    log.info('#### 4. check TEST demo tlv eeprom value ####')
    for key, value in read_test_value_dict.items():
        key = key.lower()
        if key == '0x25' or key == '0xfd':
            value = f'\"{value}\"'
        if testValue[key] == value:
            log.success('Write test tlv eeprom [%s] value [%s] pass.'%(key, value))
        else:
            error_count += 1
            log.fail('Write test tlv eeprom [%s] value [%s] fail.'%(key, value))
    if error_count:
        raise Exception('Failed run write_tlv_system_eeprom')

@logThis
def power_cycle_unit_to_rescue_mode():
    KapokCommonLib.powerCycleToOnieRescueMode()

@logThis
def read_and_check_tlv_test_eeprom_value(sysCmd, testDict):
    error_count = 0
    read_test_value_dict = check_store_tlv_system_eeprom(sysCmd, 'True')
    for key, value in read_test_value_dict.items():
        key = key.lower()
        if key == '0x25' or key == '0xfd':
            value = f'\"{value}\"'
        if testDict[key] == value:
            log.success('check test tlv eeprom [%s] value [%s] pass.'%(key, value))
        else:
            error_count += 1
            log.fail('check test tlv eeprom [%s] value [%s] fail.'%(key, value))
    if error_count:
        raise Exception('Failed run read_and_check_tlv_test_eeprom_value')

@logThis
def check_and_reset_sfp_eeprom(sftTool):
    passCount = 0
    error_count = 0
    output = device.executeCmd(sftTool)
    for line in output.splitlines():
        if re.search('Passed', line):
            passCount += 1
    if passCount == 34:
        log.info('check sfp info passed')
    else:
        error_count += 1
        log.fail('failed to check sfp info')
    reset_cmd = sftTool + ' --reset'
    CommonLib.execute_command(reset_cmd, timeout=120)
    if error_count:
        raise Exception('failed to check sfp info')

@logThis
def read_sfp_eeprom_value(sfpTool, pattern):
    pass_count = 0
    error_count = 0
    for i in range(1, 33):
        # 1. read eeprom
        option1 = ' --port ' + str(i) + ' --read 0'
        option2 = ' --port ' + str(i) + ' --read 1'
        cmd1 = sfpTool + option1
        cmd2 = sfpTool + option2
        output1 = CommonLib.execute_command(cmd1, timeout=120)
        output2 = CommonLib.execute_command(cmd2, timeout=120)
        # 2. check AWS result:
        for line in output1.splitlines():
            line = line.strip()
            res = re.search(pattern, line)
            if res:
                pass_count += 1
        if pass_count > 0:
            pass_count = 0
            log.success('Read port-%d sft eeprom pass.'%i)
        else:
            error_count += 1
            log.fail('Read port-%d sft eeprom fail.'%i)
    return error_count

@logThis
def read_and_write_aws_eeprom(sfpTool, pattern, test_pattern, lpmode_option):
    error_count = 0
    #1. read sfp eeprom
    error_count += read_sfp_eeprom_value(sfpTool, pattern)
    #2. write AwS sfp eeprom
    for i in range(1, 33):
        enable_lpmode_cmd = sfpTool + ' --port ' + str(i) + lpmode_option
        write_test_cmd = sfpTool + ' --port ' + str(i) + write_test_stp_option
        for cmd in [enable_lpmode_cmd, write_test_cmd]:
            CommonLib.execute_command(cmd, timeout=120)
    #3. read test eeprom
    error_count += read_sfp_eeprom_value(sfpTool, test_pattern)
    #4. write default eeprom.
    for i in range(1, 33):
        write_cmd = sfpTool + ' --port ' + str(i) + write_stp_option
        CommonLib.execute_command(write_cmd, timeout=120)
    #5. read original eeprom
    error_count += read_sfp_eeprom_value(sfpTool, pattern)
    if error_count:
        raise Exception('Failed run read_and_write_aws_eeprom')

@logThis
def check_eth0_ip_and_onie_version(typeValue):
    error_count = 0
    #1. check ip addr
    get_dhcp_ip_and_ping_server()
    #2. get onie current version
    p1 = r'ONIE[ \t]+([\d\.]+)'
    onieObj = CommonLib.get_swinfo_dict("ONIE_updater")
    onie_current_version = onieObj.get(typeValue + "Version", "NotFound")
    output = CommonLib.execute_command(get_versions_cmd, timeout=120)
    res = re.search(p1, output)
    if res:
        get_onie_version = res.group(1)
        if get_onie_version == onie_current_version:
            log.success('Get the current version is %s'%get_onie_version)
        else:
            error_count += 1
            log.fail('fail, get version is %s, expect version is %s'%(get_onie_version, onie_current_version))
    if error_count:
        raise Exception('Failed run check_eth0_ip_and_onie_version')

@logThis
def restore_original_tlv_eeprom_value(bkValue, tlvCmd):
    store_value_dict = check_store_tlv_system_eeprom(bkValue)
    #1. write orginal value
    for key, value in store_value_dict.items():
        key = key.lower()
        if key == '0x25' or key == '0xfd':
            cmd = tlvCmd + key + '="' + value + '"'
        else:
            cmd = tlvCmd + key + '=' + value
        CommonLib.execute_command(cmd, timeout=120)
    check_store_tlv_system_eeprom(ONIE_SYSEEPROM_CMD, 'True')
    power_cycle_unit_to_rescue_mode()

@logThis
def check_tpm_info(tmpTool, expectValue):
    p1 = '(.*):\s+(.*)'
    demo_dict = {}
    error_count = 0
    output = CommonLib.execute_command(tmpTool, timeout=120)
    for line in output.splitlines():
        line = line.strip()
        res = re.search(p1, line)
        if res:
            key = res.group(1)
            value = res.group(2)
            demo_dict[key] = value
    del demo_dict['serial_number']
    log.info('#### Get the tpm dict: %s ####'%str(demo_dict))
    for key, value in demo_dict.items():
        if expectValue[key] == value:
            log.success('Check %s value is %s passed.'%(key, value))
        else:
            error_count += 1
            log.fail('Check %s value is %s failed.'%(key, value))
    if error_count:
        raise Exception('Failed run check_tpm_info.')

@logThis
def check_onie_initargs_and_bootargs(tool1, tool2, res1, res2):
    error_count = 0
    KapokCommonLib.bootIntoUboot()
    toolCmdLst = [tool1, tool2]
    resLst = [res1, res2]
    for i in range(0, 2):
        output = CommonLib.execute_command(toolCmdLst[i], timeout=120)
        if resLst[i] in output:
            log.success('Check %s is passed.'%toolCmdLst[i])
        else:
            error_count += 1
            log.fail('Check fail, do not match result: %s'%resLst[i])
    cmd = switch_onie_mode_cmd['rescue']
    device.sendCmdRegexp(cmd, ACTIVATE_CONSOLE_PROMPT, timeout=600)
    device.sendMsg("\n")
    device.sendMsg(KapokConst.STOP_ONIE_DISCOVERY_KEY)
    device.read_until_regexp(device.promptOnie, timeout=10)
    if error_count:
        raise Exception('Failed run check_onie_initargs_and_bootargs')


############### Onie related keywords end

############### wrapper of Device related keyword begin, just transmit the calling to Device Object

@logThis
def try_reboot_to_onie_install_mode(cmd='reboot'):
    device.sendMsg(cmd + "\n")
    device.read_until_regexp(ACTIVATE_CONSOLE_PROMPT, timeout=500)
    device.sendMsg("\n")
    onie_discovery_stop_cmd = KapokConst.STOP_ONIE_DISCOVERY_KEY
    device.sendCmdRegexp(onie_discovery_stop_cmd, device.promptOnie, timeout=60)

def try_reboot_to_diag_mode(cmd='reboot'):
    device.sendMsg(cmd + "\n")
    device.read_until_regexp(KapokConst.STOP_AUTOBOOT_PROMPT, KapokConst.BOOT_TIME)
    device.sendMsg(KapokConst.STOP_AUTOBOOT_KEY)
    device.sendMsg(DIAG_BOOT_CMD + '\n')
    device.read_until_regexp(ACTIVATE_CONSOLE_PROMPT, KapokConst.BOOT_TIME)
    device.sendMsg("\n")
    onie_discovery_stop_cmd = KapokConst.STOP_ONIE_DISCOVERY_KEY
    device.sendCmdRegexp(onie_discovery_stop_cmd, device.promptDiagOS, timeout=30)

def try_reboot_to_onie_rescue_mode(cmd='reboot'):
    device.sendMsg(cmd + "\n")
    device.read_until_regexp(KapokConst.STOP_AUTOBOOT_PROMPT, KapokConst.BOOT_TIME)
    device.sendMsg(KapokConst.STOP_AUTOBOOT_KEY)
    device.sendMsg(switch_onie_mode_cmd['rescue'] + '\n')
    device.read_until_regexp(ACTIVATE_CONSOLE_PROMPT, KapokConst.BOOT_TIME)
    device.sendMsg("\n")
    onie_discovery_stop_cmd = KapokConst.STOP_ONIE_DISCOVERY_KEY
    device.sendCmdRegexp(onie_discovery_stop_cmd, device.promptOnie, timeout=30)

@logThis
def switch_diag_folder_path(path):
    cmd = 'cd ' + path
    p1 = "No such file or directory"
    output = device.executeCommand(cmd, device.promptDiagOS)
    if re.search(p1, output):
        log.fail('switch folder fail!')
        raise Exception('Change %s path failed!'%(path))
    else:
        log.info('Switch the folder successfully!')

@logThis
def get_image_version_from_yaml(ImageName, typeValue):
    imageObj = CommonLib.get_swinfo_dict(ImageName)
    current_version = imageObj.get(typeValue + "Version", "NotFound")
    return current_version

@logThis
def check_onie_version_by_system_info_tool(tool, pattern):
    p1 = r'ONIE\s+([\d.]+)'
    pass_count = 0
    error_count = 0
    cmd = './' + tool
    switch_diag_folder_path('/root/diag/')
    expect_onie_version = get_image_version_from_yaml('ONIE_Installer', 'new')
    output = CommonLib.execute_command(cmd, timeout=120)
    if pattern in output:
        log.success('Check sys info tool pass!')
    else:
        error_count += 1
        log.fail('Check sys info tool fail!')
    res = re.search(p1, output)
    if res:
        pass_count += 1
        getVer = res.group(1)
        if getVer == expect_onie_version:
            log.success('Check onie version [%s] pass!'%getVer)
        else:
            error_count += 1
            log.fail('Check onie version fail, getVer:[%s], expectVer:[%s]'%(getVer, expect_onie_version))
    if error_count or pass_count == 0:
        raise Exception('Failed run check_onie_version_by_system_info_tool')

@logThis
def check_onie_kernel_image_and_boot_to_diagos(diagCmd, cmd='reboot'):
    p1 = 'ERROR: can\'t get kernel image!'
    error_count = 0
    device.sendMsg(cmd + "\n")
    output = device.read_until_regexp(device.promptUboot, timeout=500)
    if p1 in output:
        log.success('check erase onie image pass!')
    else:
        error_count += 1
        log.fail('check erase onie image fail!')
    device.sendMsg(diagCmd + "\n")
    device.read_until_regexp(ACTIVATE_CONSOLE_PROMPT, timeout=500)
    device.sendMsg("\n")
    if error_count:
        raise Exception('Failed run check_onie_kernel_image_and_boot_to_diagos')

@logThis
def check_network_and_ping_dhcp_server(dev='eth0'):
    pattern = '5 packets transmitted, 5 packets received, 0% packet loss'
    get_eth_ip_addr(dev)
    pingCmd = 'ping ' + server_ipv4 + ' -c 5'
    output = CommonLib.execute_command(pingCmd, timeout=120)
    if re.search(pattern, output):
        log.success('Ping server ip pass.')
    else:
        raise Exception('Ping server ip fail.')

##51.2t
@logThis
def check_onie_all_version(verType):
    error_count = 0
    pass_count = 0
    onie_ver = get_image_version_from_yaml('ONIE_updater', verType)
    uboot_ver = get_image_version_from_yaml('UBOOT', verType)
    cpld_dict = get_image_version_from_yaml('CPLD', verType)
    fpga_dict = get_image_version_from_yaml('1PPS_FPGA', verType)
    asc_dict = get_image_version_from_yaml('1PPS_ASC', verType)
    if "51.2t" in device.name:
        sysCpld_ver = cpld_dict.get('SYSCPLD', "NotFound")
        fanCpld_ver = cpld_dict.get('FPCBCPLD', "NotFound")
        comeCpld_ver = cpld_dict.get('COMECPLD', "NotFound")
        fpga0_ver = fpga_dict.get('PPS_FPGA_0', "NotFound")
        fpga1_ver = fpga_dict.get('PPS_FPGA_1', "NotFound")
        come0_ver = asc_dict.get('ASC10-0-COME', "NotFound")
        come1_ver = asc_dict.get('ASC10-1-COME', "NotFound")
        asc0_ver = asc_dict.get('ASC10-0', "NotFound")
        asc1_ver = asc_dict.get('ASC10-1', "NotFound")
        asc2_ver = asc_dict.get('ASC10-2', "NotFound")
        asc3_ver = asc_dict.get('ASC10-3', "NotFound")
        asc4_ver = asc_dict.get('ASC10-4', "NotFound")
        asc5_ver = asc_dict.get('ASC10-5', "NotFound")
        asc6_ver = asc_dict.get('ASC10-6', "NotFound")
        expect_dict = {
            'ONIE': onie_ver,
            #'DiagOS': diag_ver,
            'U-BOOT': uboot_ver,
            'SYSCPLD': sysCpld_ver,
            'FPCBCPLD': fanCpld_ver,
            'COMECPLD': comeCpld_ver,
            'PPS_FPGA_0': fpga0_ver,
            'PPS_FPGA_1': fpga1_ver,
            'ASC10-0-COME': come0_ver,
            'ASC10-1-COME': come1_ver,
            'ASC10-0': asc0_ver,
            'ASC10-1': asc1_ver,
            'ASC10-2': asc2_ver,
            'ASC10-3': asc3_ver,
            'ASC10-4': asc4_ver,
            'ASC10-5': asc5_ver,
            'ASC10-6': asc6_ver,
        }
        pattern_lst = [
            '(SYSCPLD)\s+(0x\d+)',
            '(COMECPLD)\s+(0x\d+)',
            '(FPCBCPLD)\s+(\d+)',
            '(PPS_FPGA_0)\s+([\d.]+)',
            '(PPS_FPGA_1)\s+([\d.]+)',
            '(U-BOOT)\s+(.*)',
            '(ONIE)\s+([\d.]+)',
            '(ASC10-0 \(COME\))\s+(\w+)\(0x\d+\)',
            '(ASC10-1 \(COME\))\s+(\w+)\(0x\d+\)',
            '(ASC10-0)\s+(\w+)\(0x\w+\)',
            '(ASC10-1)\s+(\w+)\(0x\w+\)',
            '(ASC10-2)\s+(\w+)\(0x\w+\)',
            '(ASC10-3)\s+(\w+)\(0x\w+\)',
            '(ASC10-4)\s+(\w+)\(0x\w+\)',
            '(ASC10-5)\s+(\w+)\(0x\w+\)',
            '(ASC10-6)\s+(\w+)\(0x\w+\)',
        ]
    elif "tigrisv2" in device.name:
        sysCpld_ver = cpld_dict.get('SystemCPLD', "NotFound")
        fanCpld_ver = cpld_dict.get('FANCPLD', "NotFound")
        comeCpld_ver = cpld_dict.get('COMeCPLD', "NotFound")
        come0_ver = asc_dict.get('ASC10-0-COME', "NotFound")
        come1_ver = asc_dict.get('ASC10-1-COME', "NotFound")
        asc0_ver = asc_dict.get('ASC10-0', "NotFound")
        asc1_ver = asc_dict.get('ASC10-1', "NotFound")
        asc2_ver = asc_dict.get('ASC10-2', "NotFound")
        expect_dict = {
            'ONIE': onie_ver,
            'U-BOOT': uboot_ver,
            'SystemCPLD': sysCpld_ver,
            'FANCPLD': fanCpld_ver,
            'COMeCPLD': comeCpld_ver,
            'FPGA': fpga_dict,
            'ASC10-0-COME': come0_ver,
            'ASC10-1-COME': come1_ver,
            'ASC10-0': asc0_ver,
            'ASC10-1': asc1_ver,
            'ASC10-2': asc2_ver,
        }
        pattern_lst = [
            '(SystemCPLD)\s+(0x\d+)',
            '(COMeCPLD)\s+(0x\d+)',
            '(FANCPLD)\s+(\d+)',
            '(FPGA)\s+(\w+)',
            '(U-BOOT)\s+(.*)',
            '(ONIE)\s+([\d.]+)',
            '(COMe ASC10-0)\s+(\w+)\(0x\d+\)',
            '(COMe ASC10-1)\s+(\w+)\(0x\d+\)',
            '(ASC10-0)\s+(\w+)\(0x\w+\)',
            '(ASC10-1)\s+(\w+)\(0x\w+\)',
            '(ASC10-2)\s+(\w+)\(0x\w+\)',
        ]
    elif "tianhe" in device.name:
        sysCpld_ver = cpld_dict.get('SYSCPLD', "NotFound")
        fanCpld_ver = cpld_dict.get('FANCPLD', "NotFound")
        comeCpld_ver = cpld_dict.get('COMECPLD', "NotFound")
        LED1Cpld_ver = cpld_dict.get('SWLEDCPLD1', "NotFound")
        LED2Cpld_ver = cpld_dict.get('SWLEDCPLD2', "NotFound")
        asc0_ver = asc_dict.get('ASC10-0', "NotFound")
        asc1_ver = asc_dict.get('ASC10-1', "NotFound")
        asc2_ver = asc_dict.get('ASC10-2', "NotFound")
        asc3_ver = asc_dict.get('ASC10-3', "NotFound")
        asc4_ver = asc_dict.get('ASC10-4', "NotFound")
        expect_dict = {
                'ONIE': onie_ver,
                'U-BOOT': uboot_ver,
                'SYSCPLD': sysCpld_ver,
                'FANCPLD': fanCpld_ver,
                'COMECPLD': comeCpld_ver,
                'SWLEDCPLD1': LED1Cpld_ver,
                'SWLEDCPLD2': LED2Cpld_ver,
                '1PPSFPGA': fpga_dict,
                'ASC10-0': asc0_ver,
                'ASC10-1': asc1_ver,
                'ASC10-2': asc2_ver,
                'ASC10-3': asc3_ver,
                'ASC10-4': asc4_ver,
        }
        pattern_lst = [
                '(SYSCPLD)\s+(0x\d+)',
                '(COMECPLD)\s+(0x\d+)',
                '(SWLEDCPLD1)\s+(0x\d+)',
                '(SWLEDCPLD2)\s+(0x\d+)',
                '(FANCPLD)\s+(\d+)',
                '(1PPSFPGA)\s+(0x\d+)',
                '(U-BOOT)\s+(.*)',
                '(ONIE)\s+([\d.]+)',
                '(ASC10-0)\s+(\w+)',
                '(ASC10-1)\s+(\w+)',
                '(ASC10-2)\s+(\w+)',
                '(ASC10-3)\s+(\w+)',
                '(ASC10-4)\s+(\w+)',
        ]
    log.info('[########### Expect the version is: \n %s ]'%(str(expect_dict)))
    cmd = get_versions_cmd
    output = CommonLib.execute_command(cmd, timeout=120)
    get_dict = {}
    for line in output.splitlines():
        line = line.strip()
        for pattern in pattern_lst:
            res = re.search(pattern, line)
            if res:
                getKey = res.group(1)
                getValue = res.group(2)
                if getKey == 'ASC10-0 (COME)':
                    getKey = 'ASC10-0-COME'
                elif getKey == 'ASC10-1 (COME)':
                    getKey = 'ASC10-1-COME'
                elif getKey == 'COMe ASC10-0':
                    getKey = 'ASC10-0-COME'
                elif getKey == 'COMe ASC10-1':
                    getKey = 'ASC10-1-COME'
                get_dict[getKey] = getValue
    log.info('[############ Get the version dict is: \n %s]'%str(get_dict))
    for key, value in get_dict.items():
        if expect_dict[key] == value:
            pass_count += 1
            log.success('Check %s version is %s'%(key, value))
        else:
            error_count += 1
            log.fail('Check %s version fail, getVer is %s, expectVer is %s'%(key, value, expect_dict[key]))
    log.info('============== get pass_count=%d ===================='%pass_count)
    log.info('++++++++++++++ expect version check number=%d ++++++++++++++'%len(expect_dict))
    if error_count or pass_count != len(expect_dict):
        raise Exception('Failed run check_onie_all_version!')

@logThis
def change_the_diagos_image_name(onieMode):
    server = Device.getDeviceObject('PC')
    time.sleep(60)
    server.executeCmd('cd ' + tftp_root_path, timeout=60)
    imageObj = SwImage.getSwImage(onieMode)
    image = imageObj.newImage
    cmd = 'ls ' + image
    server.sendMsg(cmd)
    server.sendMsg('\n')
    output = server.executeCmd(cmd, timeout=60)
    if 'No such file or directory' in output:
        raise Exception('Do not find image file: [%s]'%image)
    else:
        res = image[11:]
        new_image = 'onie' + res
        server.executeCmd('mv {} {}'.format(image, new_image))
        log.info('==== Get the new image name is [%s] ===='%new_image)

@logThis
def restore_diagos_image_name(onieMode):
    server = Device.getDeviceObject('PC')
    time.sleep(60)
    server.executeCmd('cd ' + tftp_root_path, timeout=60)
    imageObj = SwImage.getSwImage(onieMode)
    image = imageObj.newImage
    res = image[11:]
    current_image = 'onie' + res
    cmd = 'ls ' + current_image
    server.sendMsg(cmd)
    server.sendMsg('\n')
    output = server.executeCmd(cmd, timeout=60)
    if 'No such file or directory' in output:
        raise Exception('Do not find image file: [%s]'%image)
    else:
        server.executeCmd('mv {} {}'.format(current_image, image))

@logThis
def check_onie_tlv_and_some_sys_info(tlvCmd, sysLst):
    pass_count = 0
    error_count = 0
    #1. get tlv info
    tlv_pn_pattern = 'Part Number\s+0x\d+\s+\d+\s+([\w-]+)'
    tlv_sn_pattern = 'Serial Number\s+0x\d+\s+\d+\s+(\w+)'
    tlv_onie_pattern = 'ONIE Version\s+0x\d+\s+\d+\s+([\d.]+)'
    output = CommonLib.execute_command(tlvCmd, timeout=120)
    for line in output.splitlines():
        line = line.strip()
        res_pn = re.search(tlv_pn_pattern, line)
        res_sn = re.search(tlv_sn_pattern, line)
        res_onie = re.search(tlv_onie_pattern, line)
        if res_pn:
            pass_count += 1
            getPnValue = res_pn.group(1)
        if res_sn:
            pass_count += 1
            getSnValue = res_sn.group(1)
        if res_onie:
            pass_count += 1
            getOnieValue = res_onie.group(1)
    if pass_count == 3:
        log.info('##### Get the tlv info as the below:\n PN: %s, SN: %s, ONIE: %s #####'%(getPnValue, getSnValue, getOnieValue))
        expect_tlvLst = [getSnValue, getPnValue, getOnieValue, getOnieValue]
    else:
        error_count += 1
    #2. check sys info
    for i in range(0, len(sysLst)):
        output = CommonLib.execute_command(sysLst[i], timeout=120)
        if expect_tlvLst[i] in output:
            log.success('Check cmd [%s] get the value [%s] is the same with tlv'%(sysLst[i], expect_tlvLst[i]))
        else:
            error_count += 1
            log.fail('Check cmd [%s] get the value [%s] is the diff with tlv' % (sysLst[i], expect_tlvLst[i]))
    if error_count:
        raise Exception("Failed run check_onie_tlv_and_some_sys_info")

@logThis
def check_temp_info(cmd):
    p1 = 'Sensors test : Passed'
    output = CommonLib.execute_command(cmd, timeout=120)
    if p1 in output:
        log.success('Check temp info pass!')
    else:
        raise Exception('Check temp info fail!')

@logThis
def ssh_dhcp_connect_from_onie_side():
    log.info('############ SSH jenkins server from onie side #####################')
    serverObj = Device.getDeviceObject('PC')
    time.sleep(60)
    output = serverObj.executeCmd('ls ' + tftp_root_path, timeout=60)
    if 'ssh_test' in output:
        log.success('SSH login to server pass!')
    else:
        raise Exception('SSH login fail!')

@logThis
def ssh_dut_connect_from_server_side():
    error_count = 0
    log.info('##################### SSH onie from jenkins server side #####################')
    if 'tianhe' in devicename.lower():
        device_ip = get_eth_ip_addr('eth0')
    else:
        device_ip = getDeviceIp('eth0')
    deviceObj = DeviceMgr.getDevice('DUT')
    oniePrmpt = deviceObj.promptOnie
    err_msg = 'Permission denied'
    serverObj = Device.getDeviceObject('PC')
    host_cmd = 'rm -rf /root/.ssh/known_hosts'
    serverObj.transmit(host_cmd)
    cmd = 'ssh ' + device_ip
    serverObj.sendCmd(cmd, timeout=5)
    promptList = ["(y/n)", "(yes/no)", oniePrmpt]
    patternList = re.compile('|'.join(promptList))
    output = serverObj.read_until_regexp(patternList, 30)
    if re.search("(y/n)", output):
        serverObj.transmit("y")
    elif re.search("(yes/no)", output):
        serverObj.transmit("yes")
    elif re.search(oniePrmpt, output):
        log.info('login the onie successfully!')
    else:
        error_count += 1
        log.fail("pattern mismatch")
    promptList1 = [err_msg, oniePrmpt]
    patternList1 = re.compile('|'.join(promptList1))
    serverObj.read_until_regexp(patternList1, 10)
    output = serverObj.executeCmd('get_versions', timeout=60)
    if 'U-BOOT' in output:
        log.success('SSH login to DUT pass!')
    else:
        error_count += 1
        log.fail('SSH login to DUT fail!')
    if error_count:
        raise Exception('Failed run ssh_dut_connect_from_server_side')

@logThis
def uut_via_telnet_login_onie_from_server_side():
    error_count = 0
    if 'tianhe' in devicename.lower():
        device_ip = get_eth_ip_addr('eth0')
    else:
        device_ip = getDeviceIp('eth0')
    deviceObj = DeviceMgr.getDevice('DUT')
    oniePrmpt = deviceObj.promptOnie
    err_msg = 'Permission denied'
    serverObj = Device.getDeviceObject('PC')
    serverObj.transmit('\n')
    cmd = 'telnet ' + device_ip
    serverObj.sendCmd(cmd, timeout=5)
    output = serverObj.read_until_regexp(oniePrmpt, 30)
    if re.search(oniePrmpt, output):
        log.info('login the onie successfully!')
    else:
        error_count += 1
        log.fail("pattern mismatch")
    output = serverObj.executeCmd('get_versions', timeout=60)
    if 'U-BOOT' in output:
        log.success('telnet login to DUT pass!')
    else:
        error_count += 1
        log.fail('telnet login to DUT fail!')
    if error_count:
        raise Exception('Failed run uut_via_telnet_login_onie_from_server_side')

@logThis
def check_onie_sysinfo_and_version(cmdLst):
    error_count = 0
    p1 = INSTALLER_FILE_SEARCH_ORDER[2][15:]
    p2 = get_image_version_from_yaml('ONIE_Installer', 'new')
    for i in range(0, len(cmdLst)):
        output = CommonLib.execute_command(cmdLst[i], timeout=120)
        if i == 0:
            if p1 in output:
                log.success('Check onie sysinfo [%s] pass!'%p1)
            else:
                error_count += 1
                log.fail('Check onie sysinfo fail, don\'t find [%s] info.!'%p1)
        if i != 0:
            if p2 in output:
                log.success('Check onie version [%s] pass!'%p2)
            else:
                error_count += 1
                log.fail('Check onie version [%s] fail!'%p2)
    if error_count:
        raise Exception('Failed run check_onie_sysinfo_and_version')


