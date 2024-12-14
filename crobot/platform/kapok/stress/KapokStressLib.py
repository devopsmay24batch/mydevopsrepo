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
import re
from Decorator import *
import time
from KapokStressVariable import *
import KapokConst
workDir = CRobot.getWorkDir()
sys.path.append(os.path.join(workDir, 'common', 'commonlib'))
import CommonLib
import CommonKeywords
from KapokSdkVariable import *
import KapokSdkLib
from KapokSdkLib  import  get_port_infos_regexp , check_output , run_command
try:
    from Device import Device
    import DeviceMgr
except Exception as err:
    log.cprint(str(err))

device = DeviceMgr.getDevice()
devicename = os.environ.get("deviceName", "")

def StressOnieConnect():
    log.debug("Entering OnieTestCase procedure: OnieConnect")
    device.loginOnie()
    return

def StressOnieDisconnect():
    global libObj
    log.debug("Entering OnieTestCase procedure: OnieDisconnect")
    device.disconnect()
    return

def Log_Info(msg):
    device.log_info(msg)

@logThis
def verify_ddr_stress_test():
    device.sendMsg(cat_ddr_log)
    output = device.read_until_regexp(cat_ddr_log_regexp, timeout=60)
    CommonLib.execute_check_dict('DUT', cmd="", mode=None, patterns_dict=cat_ddr_log_pattern, timeout=60, line_mode=True, check_output=output)

@logThis
def onie_self_update(update="new"):
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

@logThis
def config_static_ip(interface="eth0", mode=Const.ONIE_RESCUE_MODE):

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

@logThis
def verify_onie_and_cpld_version(version="new"):
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

@logThis
def scanHWInfo():
    cmd = 'cd /root/diag \n'
    device.sendMsg(cmd)

    scan_i2c = './cel-i2c-test --all \n'
    device.sendMsg(scan_i2c)
    try:
        device.read_until_regexp('I2C test \: Passed', timeout=10)
    except:
        raise Exception('Scan I2C BUS Info failed')

    scan_pcie = './cel-pci-test --all \n'
    device.sendMsg(scan_pcie)
    try:
        device.read_until_regexp('PCIe test \: Passed', timeout=10)
    except:
        raise Exception('Scan PCIE Info failed')

    scan_ssd = 'smartctl -a /dev/sda |grep SATA \n'
    device.sendMsg(scan_ssd)
    try:
        device.read_until_regexp('current\: 6\.0 Gb\/s', timeout=10)
    except:
        raise Exception('Scan SSDisk Info failed')

@logThis
def upgrade_cpld():

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

@logThis
def check_cpld_version():

    sys_cpld_version = CommonLib.get_swinfo_dict("SYS_CPLD").get("newVersion", "NotFound")
    fan_cpld_version = CommonLib.get_swinfo_dict("FAN_CPLD").get("newVersion", "NotFound")

    log.info("sys_cpld:{}, fan_cpld: {}".format(sys_cpld_version, fan_cpld_version))
    sys_cpld_version_pattern = { sys_cpld_version : "^{}".format(sys_cpld_version) }
    fan_cpld_version_pattern = { fan_cpld_version : "^{}".format(fan_cpld_version) }
    CommonLib.execute_check_dict(Const.DUT, get_sys_cpld_version_cmd, mode=Const.ONIE_RESCUE_MODE,
                patterns_dict=sys_cpld_version_pattern, timeout=10)
    CommonLib.execute_check_dict(Const.DUT, get_fan_cpld_version_cmd, mode=Const.ONIE_RESCUE_MODE,
                patterns_dict=fan_cpld_version_pattern, timeout=10)

@logThis
def warm_stress_reboot():
    device.sendMsg(reboot_cmd)
    device.read_until_regexp(KapokConst.ONIE_DISCOVERY_PROMPT, timeout=KapokConst.BOOT_TIME)
    device.sendCmdRegexp(KapokConst.STOP_ONIE_DISCOVERY_KEY + "\n", device.promptOnie, timeout=KapokConst.BOOT_TIME)
    device.getPrompt(Const.ONIE_INSTALL_MODE)

@logThis
def stress_prbs_rx(cmd,portnum):
    if str(portnum) == "32":
        output = device.sendCmdRegexp(cmd+"\n", prbs_rx_pattern,timeout=600)
    elif str(portnum) == "128":
        output = device.sendCmdRegexp(cmd+"\n", prbs_rx_pattern_port128, timeout=600)
    else:
        raise Exception("No available portnum")
    device.log_debug("output"+str(output))
    stress_check_port_BER(cmd,output,port_pattern=stress_BER_port_pattern)

@logThis
def stress_check_port_BER(cmd,output,port_pattern):
    fail_port = []
    match_flag = 0
    for line in output.splitlines():
        match = re.search(port_pattern, line)
        if match:
            match_flag = 1
            BER_value = float(match.group(1))
            if BER_value >= stress_port_BER_tolerance:
                fail_port.append(str(line))
    if fail_port:
        device.raiseException("{} failed with ports:{}".format(cmd, fail_port))
    elif match_flag == 0:
        device.raiseException("Command failed with didn't match ports information")
    else:
        device.log_success("{}".format(cmd))

@logThis
def run_sfp_all_test(cmd,pattern):
    path = '/root/diag/'
    device.sendMsg('cd ' + path + '\r\n')
    CommonLib.execute_check_dict('DUT', cmd, mode=Const.BOOT_MODE_DIAGOS, patterns_dict=pattern,
                                 timeout=15)

@logThis
def check_speed_profile(cmd):
    CommonLib.execute_check_dict('DUT', cmd, mode=Const.BOOT_MODE_DIAGOS, patterns_dict=fail_dict,
                                 timeout=15,is_negative_test=True)

@logThis
def run_asc_update_test():

    device.sendMsg("dhclient" + '\r\n')
    devicename = os.environ.get("deviceName", "")
    if "fenghuangv2" in devicename.lower():
        dev_type = DeviceMgr.getDevice(devicename).get('cardType')
        if dev_type == '1PPS':
            ASC_type = dev_type + '_ASC'
        else:
            ASC_type = 'I2C_ASC'

    destination_path = CommonLib.get_swinfo_dict(ASC_type).get("localImageDir", "NotFound")
    filelist = ["Phoenix_ASC0.hex", "Phoenix_ASC1.hex"]
    devicename = os.environ.get("deviceName", "")
    if "fenghuangv2" in devicename.lower():
        dev_type = DeviceMgr.getDevice(devicename).get('cardType')
        if dev_type == '1PPS':
            filelist.append("Phoenix_ASC2_for_1pps_REV2.hex")

        else:
            filelist.append("Phoenix_ASC2_for_i2c_REV2.hex")

    asc_path = CommonLib.get_swinfo_dict(ASC_type).get("hostImageDir", "NotFound")
    CommonLib.tftp_get_files(Const.DUT, file_list=filelist, src_path=asc_path, dst_path=destination_path)
    device.sendMsg("cd ../fw" + '\r\n')
    asc3_index = verify_asc3_exist('ls')
    log.info('asc3 exist %s' % asc3_index)
    asc_update_cmd0 = 'asc_fwupd_arm -w --bus 21 --addr 0x60 -f Phoenix_ASC0.hex --force'
    asc_update_cmd1 = 'asc_fwupd_arm -w --bus 21 --addr 0x61 -f Phoenix_ASC1.hex --force'
    if "fenghuangv2" in devicename.lower():
        dev_type = DeviceMgr.getDevice(devicename).get('cardType')
        if dev_type == '1PPS':
            asc_update_cmd2 = 'asc_fwupd_arm -w --bus 21 --addr 0x62 -f Phoenix_ASC2_for_1pps_REV2.hex --force'

        else:
            asc_update_cmd2 = 'asc_fwupd_arm -w --bus 21 --addr 0x62 -f Phoenix_ASC2_for_i2c_REV2.hex --force'
    asc_update_cmd_list = []
    if asc3_index == 'yes':
        asc_update_cmd_list = [
            asc_update_cmd0, asc_update_cmd1, asc_update_cmd2
        ]
    else:
        asc_update_cmd_list = [
            asc_update_cmd0, asc_update_cmd1
        ]
    for asc_cmd in asc_update_cmd_list:
        passcount = 0
        output = CommonLib.execute_command(asc_cmd)
        keywords_pattern = ['\[100\%\]', 'PASS']
        for pattern in keywords_pattern:
            match = re.search(pattern, output)
            if match:
                passcount += 1

        if passcount == len(keywords_pattern):
            log.success("ASC command {} test Passed!".format(asc_cmd))
        else:
            raise Exception("ASC command {} test Failed!".format(asc_cmd))

@logThis
def verify_asc3_exist(asc_cmd):

    output = CommonLib.execute_command(asc_cmd)
    true_message = 'Phoenix_ASC2.hex'
    count = ''
    if true_message in output:
        count = 'yes'
    else:
        count = 'no'

    return count

@logThis
def check_asc_version():

    device.sendMsg('cd /root/fw' + '\r\n')
    index = verify_asc3_exist('ls')
    log.info('asc3 exist %s ' % index)
    check_asc_cmd = []
    if index == 'yes':
        check_asc_cmd = ['asc_fwupd_arm -r --bus 21 --addr 0x60',
                         'asc_fwupd_arm -r --bus 21 --addr 0x61',
                         'asc_fwupd_arm -r --bus 21 --addr 0x62']
    else:
        check_asc_cmd = ['asc_fwupd_arm -r --bus 21 --addr 0x60',
                         'asc_fwupd_arm -r --bus 21 --addr 0x61']
    for cmd in check_asc_cmd:
        output = CommonLib.execute_command(cmd)
        match = re.search('fail|error', output, re.I)
        if not match:
            log.success("check asc {} version test Passed!".format(cmd))
        else:
            raise Exception("check asc {} version test Passed!".format(cmd))

@logThis
def fhv2downloadstressAndRecoveryDiagOS():
    stress_file=["fenghuangv2/stress_test.tar.xz"]
    fhv2_run_command("mkdir /root/tools")
    CommonLib.tftp_get_files(Const.DUT, dst_path="/root/tools",file_list=stress_file, timeout=400)
    cmd_list = ["tar -xf stress_test.tar.xz"]
    output = fhv2_run_command(cmd_list, timeout=300)
    CommonLib.execute_check_dict("DUT", "", patterns_dict=fail_dict, timeout=10,
                                 check_output=output, is_negative_test=True)

def fhv2getDhcpIP(interface="eth0", mode=Const.BOOT_MODE_DIAGOS):
    log.debug("Entering OnieLib class procedure: getDhcpIP")

    cmd = "dhclient"
    CommonLib.execute_check_dict('DUT', cmd, mode=mode, patterns_dict=fail_dict,
                                 timeout=25, is_negative_test=True)

def fhv2_run_command(cmd, mode=None, timeout=60, CR=True):
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
def change_phy_config_file():
    switch_diag_path('/root/diag/configs')
    server_ip = DeviceMgr.getDevice('PC').managementIP
    log.info('server_ip: ' + server_ip)
    ip = CommonLib.check_ip_address('DUT', 'eth0', mode=Const.BOOT_MODE_DIAGOS)
    log.info('ip: ' + ip)
    cmd = "sed -i 's/%s/%s/' %s" % (r'169.254.46.201', server_ip, 'phys.yaml')
    device.executeCmd(cmd)
    cmd = "sed -i 's/%s/%s/' %s" % (r'169.254.46.202', ip, 'phys.yaml')
    device.executeCmd(cmd)
    device.executeCmd('cat %s | grep server_ip:' % ('phys.yaml'))

@logThis
def softReset(cmd):
    CommonLib.transmit(cmd)
    device.read_until_regexp(KapokConst.STOP_AUTOBOOT_PROMPT, 200)
    device.sendMsg(KapokConst.STOP_AUTOBOOT_KEY)
    device.getPrompt(Const.BOOT_MODE_DIAGOS)

@logThis
def run_pci_all_test():
       path = '/root/diag/'
       device.sendMsg('cd ' + path + '\r\n')
       pciAllTest = CommonLib.exec_cmd("./cel-pci-test --all")
       CommonKeywords.should_match_a_regexp(pciAllTest, 'PCIe test : Passed')
       log.info('PCIe status successful')

@logThis
def readWriteScratchPadRegister():
    devicename = os.environ.get("deviceName", "")
    if "fenghuangv2" in devicename.lower():
        dev_type = DeviceMgr.getDevice(devicename).get('cardType')
        if dev_type == 'FPGA':
            default_val = device.executeCmd('cat /sys/devices/xilinx/accel-i2c/scratch')
        else:
            default_val = device.executeCmd('cat /sys/devices/xilinx/pps-i2c/scratch')
    if '0x00000000' in default_val:
        log.success('read_scratchpad_register successfull.')
    else:
        raise RuntimeError('read_scratchpad_register failed!')
    if "fenghuangv2" in devicename.lower():
        dev_type = DeviceMgr.getDevice(devicename).get('cardType')
        if dev_type == 'FPGA':
            device.executeCmd('echo 0x12345678 > /sys/devices/xilinx/accel-i2c/scratch')
            write_val = device.executeCmd('cat /sys/devices/xilinx/accel-i2c/scratch')
        else:
            device.executeCmd('echo 0x12345678 > /sys/devices/xilinx/pps-i2c/scratch')
            write_val = device.executeCmd('cat /sys/devices/xilinx/pps-i2c/scratch')
    if '0x12345678' in write_val:
        log.success('write_scratchpad_register successfull.')
    else:
        raise RuntimeError('write_scratchpad_register failed!')
    if "fenghuangv2" in devicename.lower():
        dev_type = DeviceMgr.getDevice(devicename).get('cardType')
        if dev_type == 'FPGA':
            device.executeCmd('echo default_val > /sys/devices/xilinx/accel-i2c/scratch')
        else:
            device.executeCmd('echo default_val > /sys/devices/xilinx/pps-i2c/scratch')





@logThis
def sfpStressTest(cmd_list, patterns_dict):
    cmd = 'cd /root/diag'
    device.sendCmd(cmd,'#',timeout=10)
    time.sleep(10)
    for cmd in cmd_list:
        try:
            CommonLib.execute_check_dict('DUT', cmd=cmd, patterns_dict=patterns_dict, timeout=2500)
        except:
            raise Exception('sfp stress test failed')




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
        log.info(cmdx)
        log.info(due_prompt)
        finish_prompt = "{}[\s\S]+{}".format(due_prompt, promptStr)
        if CR:
            cmdx += "\n"
        device.sendMsg(cmdx)
        output += device.read_until_regexp(finish_prompt, timeout=timeout)

    return output



@logThis
def ubootRovBitsTest(a):
    a=int(a)
    i = 1
    flag = 0
    while i <= a:
        log.info("Starting reboot iteration: " + str(i))
        device.sendMsg("reboot \n")
        device.read_until_regexp("ONIE: Starting ONIE Service Discovery", timeout=260)
        device.sendMsg("\n \n \n onie-discovery-stop \n \n")
        output = device.executeCmd("fw_setenv -f rov_bits")
        time.sleep(20)
        if re.search("Error|error",output):
            flag = 1
        if flag == 1:
            log.fail("Error encounter executing rov_bits stress at " + str(i) + " iteration" )
            break
        i+=1
        if i == a and flag == 0:
            log.success("No error executing " + str(a) + "  reboots of rov_bits")
            break


@logThis
def verifydevicetests():
    pat = 'cd /root/diag'
    i = 1
    limit = 5
    flag = 0
    err = "Error|error"
    string1 = 'I2C test : Passed'
    string2 = 'PCIe test : Passed'
    string3 = 'Sys test : Passed'
    string4= 'Storage test : Passed'
    while  i <= limit:
        log.info("Starting Reboot Iteration :  " + str(i) )
        device.sendMsg("reboot\n")
        device.read_until_regexp(KapokConst.STOP_AUTOBOOT_PROMPT, 300)

        device.sendMsg(KapokConst.STOP_AUTOBOOT_KEY)
        device.getPrompt(Const.BOOT_MODE_DIAGOS)

        run_command(pat)
        device.sendMsg('./cel-i2c-test --all\n')
        output1 = device.read_until_regexp(string1,20)

        device.sendMsg('./cel-pci-test --all\n')
        output2 = device.read_until_regexp(string2,20)

        device.sendMsg('./cel-system-test --all\n')
        output3 = device.read_until_regexp(string3,20)

        device.sendMsg("./cel-storage-test --all\n")
        output4 = device.read_until_regexp(string4,100)

        condition = re.search(output1,err) or re.search(output2,err) or  re.search(output3,err) or re.search(output4,err)
        if not condition:
            flag+= 1
        i+= 1

        if i > limit:
            break


    if flag == limit:
         log.success("Iterations run : {} \nPassed : {}".format(limit,flag))
    else:
         log.fail("Iterations run : {} \nPassed : {}".format(limit,flag))


@logThis
def DetectPCIEDevice():
    device.log_debug('Entering procedure DetectPCIEDevice  with args : %s' %(str(locals())))
    cmd_path = remote_shell_load_sdk
    cmd = device.sendCmd(cmd_path)
    finish_prompt = "{}".format("Innovium Standalone Command Shell.")
    output=device.sendCmdRegexp(cmd,finish_prompt,timeout=15)
    device.read_until_regexp(sdkConsole,timeout=100)
    cmd2 = device.sendCmd(show_port_info)
    output2 = device.sendCmdRegexp(cmd2,port_info_finish_prompt,timeout=15)
    device.read_until_regexp(sdkConsole)
    device.sendCmd('diagtest serdes aapl 31 0 "aapl serdes -display"')
    device.read_until_regexp(sdkConsole)
    device.sendCmd(exit_cmd)
    device.read_until_regexp(SDK_PATH_New)
    dev_cmd = 'lspci'
    cmd3 = device.sendCmd(dev_cmd)
    output3 = device.sendCmdRegexp(cmd3,SDK_PATH_New +'#',timeout=15)
    pass_dict = {
                'Ethernet controller' : 'Device 1c36:0001',
                'SATA controller' : 'Device 1c36:0031',
                'Ethernet controller' : 'Device 1d98:1b58',
                'PCI bridge' : 'Device 1c36:0031',
                'Memory controller' : 'Device 1d0f:8571'
     }
    CommonLib.execute_check_dict("DUT", "", patterns_dict=pass_dict, timeout=60, check_output=output3, is_negative_test=False)

@logThis
def ChangeToSdkPath():
    device.log_debug("Entering procedure change_dir_to_sdk_path.\n")
    var_path = SDK_PATH_New
    cmd = "cd " + var_path
    device.read_until_regexp(device.promptDiagOS,timeout=60)
    device.executeCmd(cmd)

@logThis
def consoleCheck():
     device.log_debug('Entering procedure console_check with args : %s' %(str(locals())))
     cmd = 'console'
     device.read_until_regexp(sdkConsole,timeout=10)
     cmd = device.sendCmd(cmd)
     finish_prompt = "{}".format("Innovium command shell.")
     output=device.sendCmdRegexp(cmd,finish_prompt,timeout=15)
     device.read_until_regexp('>>>',timeout=10)
     device.sendCmd('from aux_port_cel import *')
     device.read_until_regexp('>>>',timeout=10)
     cmd1 = 'aux_traffic_test()'
     output = device.sendCmdRegexp(cmd1,"aux port unconfig .... end",timeout=60)
     pattern = 'result: [ Passed ]'
     if pattern in output:
         log.success("Expected pattern {}  matched".format(pattern))
     else:
         log.fail("Expected pattern {} din't match".format(pattern))
     device.read_until_regexp('>>>',timeout=10)
     cmd2 = device.sendCmd('exit()')
     output=device.sendCmdRegexp(cmd2,sdkConsole,timeout=15)

@logThis
def auto_load_user():
     device.log_debug('Entering procedure auto_load_user with args : %s' %(str(locals())))
     cmd1 = remote_shell_load_sdk
     cmd2 = PAM4_400G_32
     cmd = device.sendCmd("{} {}".format(cmd1,cmd2))
     finish_prompt = "{}".format("Innovium Standalone Command Shell.")
     output=device.sendCmdRegexp(cmd,finish_prompt,timeout=15)

@logThis
def show_port_counter():
    device.log_debug("Entering procedure show_port_counter.\n")
#    add_flush_and_delay()
    device.read_until_regexp(sdkConsole,timeout=5)
    cmd = 'ifcs show counters devport'
    device.sendCmdRegexp(cmd,sdkConsole,timeout=10)
    device.sendCmdRegexp(exit_cmd,SDK_PATH_New)
    device.sendCmdRegexp('ifconfig eth1',SDK_PATH_New,timeout=3)
    device.sendCmdRegexp('ethtool -S eth1',SDK_PATH_New,timeout=5)
    device.read_until_regexp(SDK_PATH_New,timeout=2)
    device.sendCmd('\n')
@logThis
def checkBerLevels(portmode,portnum):
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
    cmd_lst = [prbs_en_cmd.format(portnum),prbs_set_cmd.format(portnum),prbs_sync_cmd.format(portnum)]
    KapokSdkLib.run_command(cmd_lst,prompt='IVM:0>',timeout=120)
    KapokSdkLib.run_command('shell sleep 86400',prompt='IVM:0>',timeout=86460)
    Ber_check = KapokSdkLib.run_command(prbs_get_cmd.format(portnum),prompt='IVM:0>',timeout=60)
    time.sleep(10)
    Ber_check = KapokSdkLib.run_command(prbs_get_cmd.format(portnum),prompt='IVM:0>',timeout=60)
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
    output=KapokSdkLib.run_command(cmd_lst2,prompt='IVM:0>',timeout=60)



########################################################################################################
##1. diag function
@logThis
def create_and_switch_stress_path(path):
    cmd = 'mkdir -p ' + path
    device.executeCommand(cmd, device.promptDiagOS)
    switch_diag_path(path)

@logThis
def switch_diag_path(path):
    cmd = "cd " + path
    p1 = "can't cd"
    output = device.executeCommand(cmd, device.promptDiagOS)
    if re.search(p1, output):
        log.fail('switch folder fail!')
        raise Exception('Change %s path failed!' % (path))
    else:
        log.info('Switch the folder successfully!')

@logThis
def read_register_value(cmd, pattern):
    output = device.executeCmd(cmd)
    fail_count = 0
    if pattern in output:
        log.success('Read register [%s] successfull.'%pattern)
    else:
        fail_count += 1
        log.fail('Read register [%s] fail.'%pattern)
    return fail_count

@logThis
def write_register_value(cmd):
    device.executeCmd(cmd)

@logThis
def check_pcie_stress_test(tool, pcieCmd):
    p1 = r'PCIe test : Passed'
    error_count = 0
    readCmd = 'cat ' + tool
    writeCmd = 'echo 0x12345678 > ' + tool
    writeOriginalCmd = 'echo 0x00000000 > ' + tool
    error_count += read_register_value(readCmd, '0x00000000')
    write_register_value(writeCmd)
    time.sleep(1)
    error_count += read_register_value(readCmd, '0x12345678')
    write_register_value(writeOriginalCmd)
    time.sleep(1)
    error_count += read_register_value(readCmd, '0x00000000')
    switch_diag_path(diag_tools_path)
    output = device.executeCmd(pcieCmd)
    if p1 in output:
        log.success('Check PCIe test pass!')
    else:
        error_count += 1
        log.fail('Check PCIe test fail!')
    if error_count:
        raise Exception('Failed run check_pcie_stress_test')

@logThis
def check_lspci_test(cmd):
    pass_count = 0
    output = device.executeCmd(cmd)
    pattern_lst = [r'0000:00:00.0\s+PCI\s+bridge:\s+Freescale\s+Semiconductor\s+Inc\s+Device\s+(\w+)\s+\(rev\s+\d+\)',
                  r'0000:01:00.0\s+Ethernet\s+controller:\s+Device\s+(.*)\s+\(rev\s+\d+\)',
                  r'0001:00:00.0\s+PCI\s+bridge:\s+Freescale\s+Semiconductor\s+Inc\s+Device\s+(\w+)\s+\(rev\s+\d+\)',
                  r'0001:01:00.0\s+Memory\s+controller:\s+Amazon\.com,\s+Inc\.\s+Device\s+(\d+)'
                  ]
    for pattern in pattern_lst:
        if re.search(pattern, output):
            pass_count += 1
    if pass_count == 4:
        log.success('Check lspci test pass!')
    else:
        raise Exception('Failed run check_lspci_test')

@logThis
def exit_sdk_env_in_diag_side():
    device.sendCmdRegexp('exit', device.promptDiagOS, timeout=60)

@logThis
def check_and_scan_some_devices_info():
    error_count = 0
    p1 = r'I2C test : Passed'
    p2 = r'Storage test : Passed'
    p3 = r'Sys test : Passed'
    p4 = r'Temp test : Passed'
    p5 = r'DCDC test : Passed'
    #1. check pcie test
    check_pcie_stress_test(scratchTool, PCIeTool)
    #2. check i2c test
    output = device.executeCmd(I2C_TOOL)
    if p1 in output:
        log.success('Check i2c test pass!')
    else:
        error_count += 1
        log.fail('Check i2c test fail!')
    #3. check ssd test
    output = device.executeCmd(SSD_TOOL, timeout=900)
    if p2 in output:
        log.success('Check ssd test pass!')
    else:
        error_count += 1
        log.fail('Check ssd test fail!')
    #4. check system test
    output = device.executeCmd(SYS_TOOL, timeout=900)
    if p3 in output:
        log.success('Check system test pass!')
    else:
        error_count += 1
        log.fail('Check system test fail!')
    #5. check temp test
    output = device.executeCmd(TEMP_TOOL, timeout=900)
    if p4 in output:
        log.success('Check temp test pass!')
    else:
        error_count += 1
        log.fail('Check temp test fail!')
    #6. check dcdc test
    output = device.executeCmd(DCDC_TOOL, timeout=900)
    if p5 in output:
        log.success('Check dcdc test pass!')
    else:
        error_count += 1
        log.fail('Check dcdc test fail!')
    if error_count:
        raise Exception('Failed run check_and_scan_some_devices_info')

@logThis
def run_diag_all_test(cmd):
    pass_count = 0
    error_count = 0
    p1 = r'Total:(\d+),\s+Failed:\s+(\d+),\s+Passed:(\d+)\s+\|'
    output = device.executeCmd(cmd, timeout=1500)
    res = re.search(p1, output)
    if res:
        totalNum = res.group(1)
        failNum = res.group(2)
        passNum = res.group(3)
        if (int(failNum) == 0) and (int(totalNum) == int(passNum)):
            pass_count += 1
            log.success('Check diag all test pass!')
        else:
            error_count += 1
            log.fail('Check diag all fail!')
    if error_count or pass_count == 0:
        raise Exception('Failed run run_diag_all_test')

@logThis
def diag_reboot_test():
    log.info('Start to run reboot command:')
    device.sendMsg("reboot\n")
    device.read_until_regexp(KapokConst.STOP_AUTOBOOT_PROMPT, 300)
    device.sendMsg(KapokConst.STOP_AUTOBOOT_KEY)
    device.getPrompt(Const.BOOT_MODE_DIAGOS)

@logThis
def unzip_ddr_ssd_tool(cmdLst):
    # download_snake_file(cmdLst)
    time.sleep(1)
    NameLst = cmdLst[0].split('.')
    folderName = NameLst[0]
    delFolder = 'rm -rf ' + folderName
    device.executeCmd(delFolder, timeout=100)
    #unzip stress.zip
    cmd = 'unzip ' + cmdLst[0]
    device.executeCmd(cmd, timeout=100)
    switch_diag_path(folderName)
    authCmd = 'chmod 777 *'
    device.executeCmd(authCmd, timeout=100)

@logThis
def run_ddr_stress_test(tool, runTime, ddrLog):
    p1 = r'Status: PASS - please verify no corrected errors'
    fastTime = int(runTime) + 900
    change_time = "sed -i 's/43200/%s/' %s" % (runTime, tool)
    device.executeCmd(change_time)
    cmd = './' + tool
    device.executeCmd(cmd, timeout=fastTime)
    logCmd = 'cat ' + ddrLog
    output = device.executeCmd(logCmd, timeout=300)
    if p1 in output:
        log.success('Check ddr stress pass!')
    else:
        raise Exception('Failed run run_ddr_stress_test')

@logThis
def modify_ssd_loop_and_run_test(tool, runLoop, patternLst):
    pass_count = 0
    error_count = 0
    checkLoopCmd = 'cat %s |grep "seq"' % (tool)
    change_loop = "sed -i 's/seq 1 5/seq 1 %s/' %s" % (runLoop, tool)
    loopRes = device.executeCmd(checkLoopCmd)
    if str(runLoop) in loopRes:
        log.info('Have changed the loop, start to run.')
    else:
        device.executeCmd(change_loop)
    cmd = './' + tool
    output = device.executeCmd(cmd, timeout=2400)
    if 'error' in output:
        error_count += 1
        log.fail('Find some errrors info.')
    for line in output.splitlines():
        line = line.strip()
        for pattern in patternLst:
            if re.search(pattern, line):
                pass_count += 1
    total_count = runLoop * 3
    if error_count == 0 and (total_count == pass_count):
        log.success('Run ssd stress test pass!')
    else:
        raise Exception('Failed run modify_ssd_loop_and_run_test')

@logThis
def run_diag_tool_test(tool, pattern, caseType):
    cmd = './' + tool
    output = device.executeCmd(cmd, timeout=300)
    if pattern in output:
        log.success('Check %s test pass!'%caseType)
    else:
        raise Exception('Failed run run_diag_tool_test')


@logThis
def set_i2c_bus_speed_profile(cmd):
    write_register_value(cmd)

@logThis
def asc10_fw_update_test(cmdLst, pattern):
    pass_count = 0
    for cmd in cmdLst:
        output = device.executeCmd(cmd, timeout=800)
        if pattern in output:
            pass_count += 1
            log.success('update fw [%s] pass.'%cmd)
    if pass_count == len(cmdLst):
        log.success('ASC10 fw update all pass!')
    else:
        raise Exception('Failed run asc10_fw_update_test')

@logThis
def get_fw_version(image, verType):
    imageObj = CommonLib.get_swinfo_dict(image)
    fw_version = imageObj.get(verType, "NotFound")
    return fw_version

@logThis
def get_asc_verison(imageName, verType):
    newVerObj = get_fw_version(imageName, verType)
    asc10_0_Ver = newVerObj.get('ASC10-0', "NotFound")
    asc10_1_Ver = newVerObj.get('ASC10-1', "NotFound")
    asc10_2_Ver = newVerObj.get('ASC10-2', "NotFound")
    asc10_3_Ver = newVerObj.get('ASC10-3', "NotFound")
    asc10_4_Ver = newVerObj.get('ASC10-4', "NotFound")
    asc10Lst = [asc10_0_Ver, asc10_1_Ver, asc10_2_Ver, asc10_3_Ver, asc10_4_Ver]
    return asc10Lst

@logThis
def check_asc10_fw_version_test(verCmd):
    p1 = r'CRC:\s+(\w+)'
    expect_ver_lst = get_asc_verison('1PPS_ASC', 'newVersion')
    get_ver_lst = []
    for cmd in verCmd:
        output = device.executeCmd(cmd, timeout=100)
        for line in output.splitlines():
            line = line.strip()
            res = re.search(p1, line)
            if res:
                getVer = res.group(1)
                get_ver_lst.append(getVer)
    if get_ver_lst == expect_ver_lst:
        log.success('Check asc10 fw version pass.')
    else:
        raise Exception('Failed run check_asc10_fw_version_test')

@logThis
def get_cpld_verison(imageName, verType):
    newVerObj = get_fw_version(imageName, verType)
    syscpld_Ver = newVerObj.get('SYSCPLD', "NotFound")
    comecpld_Ver = newVerObj.get('COMECPLD', "NotFound")
    ledcpld1_Ver = newVerObj.get('LEDCPLD1', "NotFound")
    ledcpld2_Ver = newVerObj.get('LEDCPLD2', "NotFound")
    fan_Ver = newVerObj.get('FANCPLD', "NotFound")
    cpldLst = [syscpld_Ver, comecpld_Ver, ledcpld1_Ver, ledcpld2_Ver, fan_Ver]
    return cpldLst

@logThis
def cpld_and_fpga_fw_update_test(cmdLst):
    error_count  = 0
    p1 = '\|\s+PASS!\s+\|'
    p2 = 'Verifying kb:\s+\d+/\d+\s+\(100%\)'
    for i in range(0, len(cmdLst)):
        if i == 3:
            device.executeCmd(FAN_PKILL, timeout=800)
        output = device.executeCmd(cmdLst[i], timeout=800)
        if i == 4:
            if re.search(p2, output):
                log.success('Update 1pps fpga fw [%s] pass.'%cmdLst[i])
            else:
                error_count += 1
                log.fail('Update 1pps fpga fw [%s] fail.'%cmdLst[i])
        else:
            if re.search(p1, output):
                log.success('Update cpld fw [%s] pass.'%cmdLst[i])
            else:
                error_count += 1
                log.fail('Update cpld fw [%s] fail.' % cmdLst[i])
    if error_count:
        raise Exception('Failed run cpld_and_fpga_fw_update_test')

@logThis
def check_cpld_fw_version_test(cmd):
    getVerLst = []
    expect_lst = get_cpld_verison('CPLD', 'newVersion')
    FPGA_VER = get_fw_version('1PPS_FPGA', 'newVersion')
    expect_lst.append(FPGA_VER)
    p1 = r'SYSCPLD\s+(\w+)'
    p2 = r'COMECPLD\s+(\w+)'
    p3 = r'SWLEDCPLD1\s+(\w+)'
    p4 = r'SWLEDCPLD2\s+(\w+)'
    p5 = r'FANCPLD\s+(\d+)'
    p6 = r'1PPSFPGA\s+(\w+)'
    patternLst = [p1, p2, p3, p4, p5, p6]
    output = device.executeCmd(cmd, timeout=100)
    for pattern in patternLst:
        res = re.search(pattern, output)
        if res:
            get_ver = res.group(1)
            getVerLst.append(get_ver)
    if getVerLst == expect_lst:
        log.success('Check cpld and fpga version pass.')
    else:
        raise Exception('Failed run check_cpld_fw_version_test')

@logThis
def run_uboot_rov_bits_test(cmd):
    write_register_value(cmd)

@logThis
def onie_reboot_to_install_mode(cmd='reboot'):
    log.info('Start to run reboot command:')
    device.sendMsg(cmd + "\n")
    device.read_until_regexp(KapokConst.ONIE_DISCOVERY_PROMPT, 600)
    device.sendMsg(KapokConst.STOP_ONIE_DISCOVERY_KEY + '\n')
    device.getPrompt(Const.BOOT_MODE_ONIE)
    device.sendMsg(KapokConst.STOP_ONIE_DISCOVERY_KEY + '\n')

@logThis
def switch_onie_path(path):
    cmd = "cd " + path
    p1 = "can't cd"
    output = device.executeCommand(cmd, device.promptOnie)
    if re.search(p1, output):
        log.fail('switch folder fail!')
        raise Exception('Change %s path failed!' % (path))
    else:
        log.info('Switch the folder successfully!')

@logThis
def run_sdk_xe_port_stress_test(tool, option, consoleCmdLst, showCmd):
    error_count = 0
    pass_count = 0
    p1 = 'result:\s+\[ Passed \]'
    p2 = r'\|\s+32\s+\|.*'
    p3 = r'\d+'
    cmd = tool + ' ' + option
    device.executeCommand(cmd, device.promptSdk, timeout=300)
    device.executeCommand(CLEAR_COUNTER_CMD1, device.promptSdk, timeout=30)
    device.executeCommand(CLEAR_COUNTER_CMD2, device.promptSdk, timeout=30)
    for cmd in consoleCmdLst:
        time.sleep(1)
        output = device.executeCommand(cmd, '>>>', timeout=300)
    if re.search(p1, output):
        log.success('Check aux traffic test pass')
    else:
        error_count += 1
        log.fail('Check aux traffic test fail.')
    device.executeCommand('exit()', device.promptSdk, timeout=30)
    output1 = device.executeCommand(showCmd, device.promptSdk, timeout=300)
    device.executeCommand('exit', device.promptOnie, timeout=30)
    for line in output1.splitlines():
        line = line.strip()
        res = re.search(p2, line)
        if res:
            pass_count += 1
            getValueLst = re.findall(p3, line)
            RxError = getValueLst[3]
            TxError = getValueLst[8]
            RxFramesAll = getValueLst[1]
            TxFramesAll = getValueLst[6]
            RxBytesAll = getValueLst[4]
            TxBytesAll = getValueLst[9]
            if (int(RxError) == 0) and (RxError == TxError) and (int(RxFramesAll) > 0) and (RxFramesAll == TxFramesAll) and (RxBytesAll == TxBytesAll):
                pass_count += 1
                log.success('Check traffic counter test pass')
            else:
                error_count += 1
                log.fail('Check traffic counter test fail')
    if error_count and pass_count == 0:
        raise Exception('Failed run run_sdk_xe_port_stress_test!')

@logThis
def check_xfi0_counter_result(cmd1, cmd2):
    pass_count = 0
    error_count = 0
    output1 = device.executeCommand(cmd1, device.promptOnie, timeout=300)
    RX_Pattern = 'RX packets:(\d+) errors:(\d+) dropped:\d+ overruns:\d+ frame:\d+'
    TX_Pattern = 'TX packets:(\d+) errors:(\d+) dropped:\d+ overruns:\d+ carrier:\d+'
    counter_pattern = 'RX bytes:(\d+) \(.* MiB\)  TX bytes:(\d+) \(.* MiB\)'
    for line in output1.splitlines():
        line = line.strip()
        RX_RES = re.search(RX_Pattern, line)
        TX_RES = re.search(TX_Pattern, line)
        COUNTER_RES = re.search(counter_pattern, line)
        if RX_RES:
            pass_count += 1
            rx_packtes = RX_RES.group(1)
            rx_errors = RX_RES.group(2)
        elif TX_RES:
            pass_count += 1
            tx_packtes = TX_RES.group(1)
            tx_errors = TX_RES.group(2)
        elif COUNTER_RES:
            pass_count += 1
            RX_Bytes = COUNTER_RES.group(1)
            TX_Bytes = COUNTER_RES.group(2)
    if (int(rx_packtes) == int(tx_packtes)) and (int(rx_errors) == int(tx_errors)) and (int(rx_errors) == 0):
        pass_count += 1
        log.success('Check RX and TX packets pass!')
    elif int(RX_Bytes) == int(TX_Bytes):
        pass_count += 1
        log.success('Check TX and RX Bytes pass!')
    else:
        error_count += 1
        log.fail('Check cmd [%s] fail!'%cmd1)
    output2 = device.executeCommand(cmd2, device.promptOnie, timeout=300)
    HW_RX_FR = '\[hw\] rx frames: (\d+)'
    HW_RX_Bytes = '\[hw\] rx bytes: (\d+)'
    HW_TX_FR = '\[hw\] tx frames: (\d+)'
    HW_TX_Bytes = '\[hw\] tx bytes: (\d+)'
    for line in output2.splitlines():
        line = line.strip()
        HW_RX_RES = re.search(HW_RX_FR, line)
        HW_TX_RES = re.search(HW_TX_FR, line)
        HW_RX_BY_RES = re.search(HW_RX_Bytes, line)
        HW_TX_BY_RES = re.search(HW_TX_Bytes, line)
        if HW_RX_RES:
            pass_count += 1
            rx_frames = HW_RX_RES.group(1)
        elif HW_TX_RES:
            pass_count += 1
            tx_frames = HW_TX_RES.group(1)
        elif HW_RX_BY_RES:
            pass_count += 1
            hw_rx_bytes = HW_RX_BY_RES.group(1)
        elif HW_TX_BY_RES:
            hw_tx_bytes = HW_TX_BY_RES.group(1)
    if (int(rx_frames) == int(tx_frames)) and (int(hw_rx_bytes) == int(hw_tx_bytes)) and (int(rx_frames) == int(rx_packtes)) and (int(hw_rx_bytes) == int(RX_Bytes)):
        pass_count += 1
        log.success('Check xfi0 nic counter pass!')
    else:
        error_count += 1
        log.fail('Check cmd [%s] fail!'%cmd2)
    if error_count or pass_count != 9:
        raise Exception('Failed run check_xfi0_counter_result!')

@logThis
def run_sdk_reinit_stress_test(tool, option, runCycle):
    p1 = '[DiagTest result]: copper 1x400 L2snake Test ----------  PASS'
    cmd = tool + ' ' + str(runCycle) + ' ' + option
    output = device.executeCommand(cmd, device.promptOnie, timeout=1200)
    if p1 in output:
        log.success('Check sdk reinit test pass!')
    else:
        raise Exception('Failed run run_sdk_reinit_stress_test!')

@logThis
def ifcs_clear_port_counter(cmdLst):
    for cmd in cmdLst:
        time.sleep(2)
        #output = device.executeCommand(cmd, device.promptSdk, timeout=180)
        device.sendCmd(cmd)
        device.read_until_regexp(device.promptSdk, timeout=120)
    # device.flush()
    # time.sleep(2)
    # check_snake_port_status_test(showCmd, 'UP')

@logThis
def sdk_snake_traffic_test(cmdLst):
    pass_count = 0
    error_count = 0
    p1 = r'\s+\d+\s+'
    for cmd in cmdLst:
        time.sleep(2)
        # output = device.executeCommand(cmd, device.promptSdk, timeout=300)
        device.sendCmd(cmd)
        output = device.read_until_regexp(device.promptSdk, timeout=300)
    for line in output.splitlines():
        line = line.strip()
        if 'Devport stats rate calculation' in line:
            continue
        resLst = re.findall(p1, line)
        if resLst:
            pass_count += 1
            getLst = [item.strip() for item in resLst]
            portNum = getLst[0]
            rxFrames = getLst[1]
            rxBytes = getLst[2]
            rxErrors = getLst[3]
            txFrames = getLst[4]
            txBytes = getLst[5]
            txErrors = getLst[6]
            if (int(rxFrames) == int(txFrames)) and (int(rxBytes) == int(txBytes)) and (int(txErrors) == int(rxErrors)) and (int(txErrors) == 0):
                log.success('Check Port-%s snake counter pass!'%portNum)
            else:
                error_count += 1
                log.fail('Check Port-%s snake counter fail!'%portNum)
    if error_count or (pass_count != 32):
        raise Exception('Failed run sdk_snake_traffic_test')

@logThis
def disable_or_enable_port_test(cmd):
    # device.executeCommand(cmd, device.promptSdk, timeout=30)
    device.sendCmd(cmd)
    output = device.read_until_regexp(device.promptSdk, timeout=300)

@logThis
def shell_sleep_test(tool, option):
    cmd = tool + ' ' + option
    disable_or_enable_port_test(cmd)

@logThis
def exit_sdk_env_in_onie_side():
    device.sendCmdRegexp('exit', device.promptOnie, timeout=60)


@logThis
def check_snake_port_status_test(cmd, status):
    time.sleep(30)
    pass_count = 0
    error_count = 0
    total_count = 0
    p1 = r'\|[ \t]+(\d+) \|[ \t]+ETH \|[ \t]+ISG\d+ \|[ \t]+\d \|[ \t]+(\d) \| \(sysport:\s+\d+\) \|[ \t]+(\d+G) \|[ \t]+(\w+) \|'
    p2 = 'Total devport count: (\d+)'
    # output = device.executeCommand(cmd, device.promptSdk, timeout=300)
    device.sendCmd(cmd)
    output = device.read_until_regexp(device.promptSdk, timeout=300)
    for line in output.splitlines():
        res1 = re.search(p2, line)
        if res1:
            total_count = int(res1.group(1)) - 8
        res = re.search(p1, line)
        if res:
            portNum = res.group(1)
            portSpeed = res.group(3)
            portStatus = res.group(4)
            if status == 'DOWN':
                if portStatus == status:
                    pass_count += 1
                    log.success('The Port-%s get the speed is %s, Status is %s' % (portNum, portSpeed, portStatus))
                else:
                    error_count += 1
                    log.fail('The Port-%s get the speed is %s, Status is %s' % (portNum, portSpeed, portStatus))
            elif status == 'UP':
                if portStatus == status:
                    pass_count += 1
                    log.success('The Port-%s get the speed is %s, Status is %s' % (portNum, portSpeed, portStatus))
                else:
                    error_count += 1
                    log.fail('The Port-%s get the speed is %s, Status is %s' % (portNum, portSpeed, portStatus))
    if (error_count == 0) and (total_count == pass_count):
        log.success('Check devport status pass.')
    else:
        raise Exception('Failed run check_snake_port_status_test, total is %d, pass count is %d'%(total_count, pass_count))

@logThis
def check_devport_counter(cmd1, cmd2):
    pass_count = 0
    error_count = 0
    p1 = r'\s+\d+\s+'
    device.sendCmd(cmd1)
    output = device.read_until_regexp(device.promptSdk, timeout=300)
    for line in output.splitlines():
        line = line.strip()
        resLst = re.findall(p1, line)
        if resLst:
            pass_count += 1
            getLst = [item.strip() for item in resLst]
            portNum = getLst[0]
            rxFrames = getLst[1]
            rxErrors = getLst[3]
            rxBytes = getLst[4]
            txFrames = getLst[6]
            txErrors = getLst[8]
            txBytes = getLst[9]
            if int(portNum) == 0:
                continue
            if (int(rxFrames) == int(txFrames)) and (int(rxBytes) == int(txBytes)) and (int(rxErrors) == int(txErrors)) and (int(rxErrors) == 0):
                log.success('Check devport-%s snake counter pass!'%portNum)
            else:
                error_count += 1
                log.fail('Check devport-%s snake counter fail!'%portNum)
    time.sleep(2)
    device.sendCmd(cmd2)
    device.read_until_regexp(device.promptSdk, timeout=300)
    if error_count and (pass_count != 32):
        raise Exception('Failed run check_devport_counter')

@logThis
def onie_idle_stress_test(tool, runTime):
    p1 = r'Curr Date info : ([\d-]+)\s+([\d:]+)'
    pass_count = 0
    cmd = './' + tool
    output1 = device.executeCmd(cmd, timeout=300)
    for line in output1.splitlines():
        line = line.strip()
        res1 = re.search(p1, line)
        if res1:
            pass_count += 1
            date_before = res1.group(1)
            time_before = res1.group(2)
            day1 = date_before.split('-')[-1]
            hour1 = time_before.split(':')[0]
            break
    idleHour = int(runTime) // 3600
    log.info('============= Start idle %d hours ==============' % idleHour)
    time.sleep(runTime)
    output2 = device.executeCmd(cmd, timeout=300)
    for line in output2.splitlines():
        line = line.strip()
        res1 = re.search(p1, line)
        if res1:
            pass_count += 1
            date_after = res1.group(1)
            time_after = res1.group(2)
            day2 = date_after.split('-')[-1]
            hour2 = time_after.split(':')[0]
            break
    if int(day1) == int(day2):
        getTime = int(hour2) - int(hour1)
        if getTime == idleHour:
            log.success('Check onie idle pass!')
        else:
            raise Exception('Check onie idle fail!')
    else:
        getTime = (24 - int(hour2)) + int(hour1)
        if getTime == idleHour:
            log.success('Check onie idle pass!')
        else:
            raise Exception('Check onie idle fail!')

@logThis
def check_onie_version_test(cmd, caseType):
    error_count = 0
    p1 = r'ONIE[ \t]+([\d\.]+)'
    onieObj = CommonLib.get_swinfo_dict("ONIE_updater")
    onie_current_version = onieObj.get(caseType + "Version", "NotFound")
    output = CommonLib.execute_command(cmd, timeout=120)
    res = re.search(p1, output)
    if res:
        get_onie_version = res.group(1)
        if get_onie_version == onie_current_version:
            log.success('Get the current version is %s' % get_onie_version)
        else:
            error_count += 1
            log.fail('fail, get version is %s, expect version is %s' % (get_onie_version, onie_current_version))
    if error_count:
        raise Exception('Failed run check_eth0_ip_and_onie_version')

@logThis
def check_onie_all_fw_version(cmd, caseType):
    onieObj = CommonLib.get_swinfo_dict("ONIE_updater")
    onie_version = onieObj.get(caseType + "Version", "NotFound")
    ubootObj = CommonLib.get_swinfo_dict("UBOOT")
    uboot_version = ubootObj.get(caseType + "Version", "NotFound")
    cpldObj = CommonLib.get_swinfo_dict("CPLD")
    sys_cpld_version = cpldObj.get(caseType + "Version").get("SYSCPLD")
    come_cpld_version = cpldObj.get(caseType + "Version").get("COMECPLD")
    fan_cpld_version = cpldObj.get(caseType + "Version").get("FANCPLD")
    led_cpld1_version = cpldObj.get(caseType + "Version").get('SWLEDCPLD1')
    led_cpld2_version = cpldObj.get(caseType + "Version").get('SWLEDCPLD2')
    ASCObj = CommonLib.get_swinfo_dict("1PPS_ASC")
    i2c_asc10_0 = ASCObj.get(caseType + "Version").get('ASC10-0', "NotFound")
    i2c_asc10_1 = ASCObj.get(caseType + "Version").get('ASC10-1', "NotFound")
    i2c_asc10_2 = ASCObj.get(caseType + "Version").get('ASC10-2', "NotFound")
    i2c_asc10_3 = ASCObj.get(caseType + "Version").get('ASC10-3', "NotFound")
    i2c_asc10_4 = ASCObj.get(caseType + "Version").get('ASC10-4', "NotFound")
    i2c_fpga_version = ASCObj.get('1pps', "NotFound")
    expect_version_dict = {
        'SYSCPLD': sys_cpld_version,
        'COMECPLD': come_cpld_version,
        'SWLEDCPLD1': led_cpld1_version,
        'SWLEDCPLD2': led_cpld2_version,
        'FANCPLD': fan_cpld_version,
        '1PPSFPGA': i2c_fpga_version,
        'U-BOOT': uboot_version,
        'ONIE': onie_version,
        'ASC10-0': i2c_asc10_0,
        'ASC10-1': i2c_asc10_1,
        'ASC10-2': i2c_asc10_2,
        'ASC10-3': i2c_asc10_3,
        'ASC10-4': i2c_asc10_4
    }
    pattern_lst = [
        r'(SYSCPLD)\s+(0x\d+)',
        r'(COMECPLD)\s+(0x\d+)',
        r'(SWLEDCPLD1)\s+(0x\d+)',
        r'(SWLEDCPLD2)\s+(0x\d+)',
        r'(FANCPLD)\s+(\d)',
        r'(1PPSFPGA)\s+(0x\d+)',
        r'(U-BOOT)\s+(.*)',
        r'(ONIE)\s+([\d.]+)',
        r'(ASC10-0)\s+(\w+)',
        r'(ASC10-1)\s+(\w+)',
        r'(ASC10-2)\s+(\w+)',
        r'(ASC10-3)\s+(\w+)',
        r'(ASC10-4)\s+(\w+)'
    ]
    get_dict = {}
    error_count = 0
    output = CommonLib.execute_command(cmd, timeout=120)
    for line in output.splitlines():
        line = line.strip()
        for pattern in pattern_lst:
            res = re.search(pattern, line)
            if res:
                k = res.group(1)
                v = res.group(2)
                get_dict[k] = v
    log.info('==== Get the version dict: %s ===='%(str(get_dict)))
    for key, value in expect_version_dict.items():
        if get_dict[key] == value:
            log.success('Check %s version [%s] pass!'%(key,value))
        else:
            error_count += 1
            log.fail('Check %s version fail, get: [%s], expect: [%s]'%(key,get_dict[key], value))
    if error_count:
        raise Exception('Failed run check_onie_all_fw_version!')

@logThis
def check_diag_tool_test(cmdLst, patternLst):
    error_count = 0
    for i in range(0, len(cmdLst)):
        cmd = './' + cmdLst[i]
        output = CommonLib.execute_command(cmd, timeout=600)
        if patternLst[i] in output:
            log.success('Check cmd [%s] pass!'%cmdLst[i])
        else:
            error_count += 1
            log.fail('Check cmd [%s] fail!'%cmdLst[i])
    if error_count:
        raise Exception('Failed run check_diag_tool_test!')

@logThis
def check_fw_setenv_test(cmd):
    CommonLib.execute_command(cmd, timeout=60)

@logThis
def check_dhcp_ip_in_onie():
    dhcpTool = 'udhcpc'
    device.executeCommand(dhcpTool, device.promptOnie, timeout=100)

@logThis
def check_ssd_smartctl_test(cmd, ssdSpeed):
    pass_count = 0
    error_count = 0
    p1 = r'SATA Version is:\s+SATA\s+[\d.]+,\s+[\d.]+\s+Gb/s\s+\(current:\s+([\d.]+)\s+Gb/s\)'
    output = device.executeCommand(cmd, device.promptOnie, timeout=300)
    res = re.search(p1, output)
    if res:
        pass_count += 1
        getValue = res.group(1)
        if getValue == ssdSpeed:
            log.success('Check ssd sata link speed [%s] pass!'%getValue)
        else:
            error_count += 1
            log.fail('Check ssd sata link speed fail, get: %s, expect: %s'%(getValue, ssdSpeed))
    if error_count or pass_count == 0:
        raise Exception('Failed run check_ssd_smartctl_test!')






