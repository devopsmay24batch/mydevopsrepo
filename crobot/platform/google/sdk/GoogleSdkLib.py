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
import GoogleConst
import re
from Decorator import *
import time
from functools import partial
import YamlParse
import GoogleCommonLib
import CommonKeywords

workDir = CRobot.getWorkDir()
sys.path.append(os.path.join(workDir, 'common', 'commonlib'))
sys.path.append(os.path.join(workDir, 'platform/Google'))

import CommonLib
try:
    from Device import Device
    import DeviceMgr
except Exception as err:
    log.cprint(str(err))
device = DeviceMgr.getDevice()
from GoogleSdkVariable import *
import GoogleSdkVariable as var
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

# ..........................  Common Functions ..........................
@logThis
def gotoSuperUser():
    output = run_command("pwd", prompt=var.sonic_prompt)
    if "root@sonic:" in output:
        log.info("Already in super-user mode.")
    else:
        output = run_command("sudo -s", prompt=var.sonic_prompt)
        log.info("Entered Super-User mode.")

def enter_sonic_credentials():
    device.sendCmd(device.userName, "Password:", timeout=3)
    device.sendCmd(device.password, timeout=5)

def getSnakeFileFromServer():
    output = run_command("ls", prompt=var.sonic_prompt, timeout=3)
    if var.cd_snake_cmd in output:
        log.info("Snake file already present")
        return
    output = run_command("curl -O http://192.168.0.1/" + var.cd_snake_cmd, prompt=var.sonic_prompt, timeout=35)
    if "Connection timed out" in output:
        log.info("Error in fetching file from server.\n")

@logThis
def change_dir_to_sdk_path():
    sdk_image = CommonLib.get_swinfo_dict("SDK").get("newImage", "NotFound")
    try:
        run_command("pwd", prompt=var.sdk_prompt, timeout=1)
        log.info("Already in sdk dir.")
    except:

        # If in SDK mode.
        output = run_command("\n", prompt="sdklt.0>|BCM.0>|" + var.sonic_prompt, timeout=5)
        if "sdklt.0>" in output:
            run_command("exit", prompt=".*BCM.0>.*", timeout=5)
            run_command("exit", prompt=var.sonic_prompt, timeout=5)
        elif "BCM.0>" in output:
            run_command("exit", prompt=var.sonic_prompt, timeout=5)

        # Enter SDK directory
        output = run_command("cd {}".format(var.sdk_path), prompt=var.sonic_prompt, timeout=3)
        if "No such file or directory" in output:

            # Fetch from server and install SDK
            gotoSuperUser()
            log.info("File doesn't exist...downloading and installing from server...")
            output = device.sendCmd("curl -O http://192.168.0.1/" + sdk_image, var.sonic_prompt, timeout=60)
            if "Connection timed out" in output:
                raise Exception("Error in fetching the SDK image from server.")
            device.sendCmd("dpkg -i " + sdk_image, var.sonic_prompt, timeout=15)
        output = run_command("cd {}".format(var.sdk_path), prompt=var.sonic_prompt, timeout=3)
        if output:
            log.info("Entered into diag dir..")
            getSnakeFileFromServer()
            gotoSuperUser()

@logThis
def enter_Into_SDK(tool, port_mode):
    gotoSuperUser()
    output = run_command("./auto_load_user.sh", prompt=var.sonic_prompt, timeout=2)
    if "rmmod: ERROR:" in output or "rmmod: not found" in output:
        log.info("ERROR in AUTO LOAD USER.\nThis error will not be fixed as this is the SDK limitation and will not impact other function...\nSkipping the error check...\n")

    # ERROR CHECK SKIPPED

    cmd = "./{} -y {}".format(tool, port_mode)
    run_command(cmd, prompt="BCM.0>", timeout=10)
    log.info("Logged into SDK mode.")

@logThis
def Exit_From_Sdk():
    output = run_command("\n", prompt="BCM.0>|" + var.sonic_prompt, timeout=5)
    if "BCM.0>" in output:
        run_command('exit', prompt=var.sdk_prompt, timeout=3)


#  .....................  BRIXIA_SDK_TC_004_32x2x400G_Port_Status_Test  .............................

def checkPortStatusFunction(output, ptn, name, msg):
    for each in ptn:
        if not re.search(each, output):
            log.info(str(each))
            raise Exception("Error in port {} status. Some of them not {}.".format(name, msg))


@logThis
def checkPortLinkStatus():
    try:
        output = run_command('ls', prompt="BCM.0>", timeout=10)
    except:
        raise Exception("Device not entered into SDK mode.")
    time.sleep(5)
    output = device.sendCmd('ps', "BCM.0>")

    checkPortStatusFunction(output, var.link_up_63_status_pattern, "link", "UP")
    checkPortStatusFunction(output, var.link_speed_63_status_pattern, "speed", "400G")

    device.sendCmd('port cd en=0', 'BCM.0>')
    time.sleep(7)

    output = run_command('ps cd', prompt='BCM.0>', timeout=10)
    checkPortStatusFunction(output, var.disabled_port_63_status_pattern, "disabled", "!ena")

    run_command('port cd en=1', prompt='BCM.0>', timeout=10)
    time.sleep(7)
    output = run_command('ps cd', prompt='BCM.0>', timeout=10)
    checkPortStatusFunction(output, var.link_up_63_status_pattern, "link", "UP")

#  .....................   Port Loopback Test  .............................

@logThis
def set_Port_And_Check(mac_status_pattern, lb_cmd, ps_cmd):
    run_command(lb_cmd, prompt="BCM.0>", timeout=10)
    output = run_command(ps_cmd, prompt="BCM.0>", timeout=10)
    checkPortStatusFunction(output, mac_status_pattern, "LoopBack", "MAC")

@logThis
def run_snake_traffic_test(snake_cmd):
    output = run_command(snake_cmd, prompt="BCM.0>", timeout=30)
    r = re.findall("Error:.*", output)
    if len(r):
        raise Exception("Error in setting snake VLAN.\n" + r[0] + "\n")


def send_packet_to_all_ports(pckt_gen_cmd, sleep_time):
    run_command("clear c", prompt="BCM.0>", timeout=3)
    run_command("show c", prompt="BCM.0>", timeout=3)

    output = run_command(pckt_gen_cmd, prompt="BCM.0>", timeout=3)
    if "Packet generate, length=512" not in output:
        raise Exception("Error in packet generation.")
    run_command("sleep " + sleep_time, prompt="BCM.0>", timeout=int(sleep_time) + 2)

def stop_traffic_and_check_counter(stop_cmd):
    run_command(stop_cmd, prompt="BCM.0>", timeout=3)
    output = run_command("show c", prompt="BCM.0>")

    r1 = re.findall(".*TPKT.*", output)
    r2 = re.findall(".*RPKT.*", output)

    for i in range(len(r1)):
        tx_rx = r1[i].split(":")[-1].split("+")
        tpkt_TX = tx_rx[0].strip()
        tpkt_RX = tx_rx[1]

        tx_rx = r2[i].split(":")[-1].split("+")
        rpkt_TX = tx_rx[0].strip()
        rpkt_RX = tx_rx[1]

        condition1 = tpkt_TX == tpkt_RX
        condition2 = rpkt_TX == rpkt_RX
        condition3 = tpkt_TX == rpkt_RX

        if not condition1 and condition2 and condition3:
            raise Exception("Error found in TX RX. Both are not same for\n" + str(r1[i]) + "\n" + str(r2[i]))

    log.success("All ports TX and RX are same.")
    log.success("Port Loopback Test Passed Succesfully.")


@logThis
def Log_Info(msg):
    device.log_info(msg)

@logThis
def check_bcm_ver():
    output = run_command('version', prompt="BCM.0>", timeout=10)
    if var.BCM_ver not in output:
        raise Exception("Version mismatched")
    log.success("BCM version matched")

@logThis
def PCIE_Ver_check():
    run_command('dsh', prompt="sdklt.0>", timeout=3)
    output = run_command('PCIEphy fwinfo', prompt="sdklt.0>", timeout=3)
    PCIE_FW_Loader_ver = CommonLib.get_swinfo_dict("PCIE").get("newVersion").get("PCIe_FW_loader_version")
    PCIE_FW_ver = CommonLib.get_swinfo_dict("PCIE").get("newVersion").get("PCIe_FW_version")
    PCIE_Loader_ver_pat = "PCIe FW loader version: " +PCIE_FW_Loader_ver
    PCIE_ver_pat = "PCIe FW version: " +PCIE_FW_ver
    if str(PCIE_Loader_ver_pat) in output:
        log.success("PCIE Loader Version matched")
    else:
        raise Exception("PCIE Loader Version mismatched")

    if str(PCIE_ver_pat) in output:
        log.success("PCIE Version matched")
    else:
        raise Exception("PCIE Version mismatched")

    run_command('exit', prompt="BCM.0>", timeout=3)

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

@logThis
def check_port_status(portmode):
    output = run_command('ps', prompt="BCM.0>", timeout=10)
    time.sleep(10)
    output = run_command('ps', prompt="BCM.0>", timeout=10)
    time.sleep(10)
    if portmode =='64x4x100':
         port_infos_pattern= brixiaV2_TH4G_64x4x100_pattern
    elif portmode =='32x8x50':
         port_infos_pattern= brixiaV2_TH4G_32x8x50_pattern
    else:
        port_infos_pattern = brixiaV2_TH4G_256x1x100_pattern
    ret_code = check_output(output, patterns=port_infos_pattern)
    if ret_code == 0:
        device.raiseException("Port status check failed")

@logThis
def disable_port_check(portmode):
    if portmode =='64x4x100':
        run_command('port cd en=0', prompt="BCM.0>", timeout=10)
        output1 = run_command('ps cd', prompt="BCM.0>", timeout=20)
        time.sleep(10)
        d_pat =  brixiaV2_TH4G_64x4x100_d_pattern
    elif portmode =='32x8x50':
        run_command('port cd en=0', prompt="BCM.0>", timeout=10)
        output1 = run_command('ps cd', prompt="BCM.0>", timeout=20)
        time.sleep(10)
        d_pat =  brixiaV2_TH4G_32x8x50_d_pattern

    else:
        run_command('port ce en=0', prompt="BCM.0>", timeout=10)
        output1 = run_command('ps ce', prompt="BCM.0>", timeout=20)
        time.sleep(10)
        d_pat = brixiaV2_TH4G_256x1x100_d_pattern
    ret_code = check_output(output1, patterns=d_pat)
    if ret_code == 0:
        device.raiseException("Disabling port failed")
    time.sleep(5)
    
@logThis
def enable_port_check(portmode):
    if portmode =='64x4x100':
        run_command('port cd en=1', prompt="BCM.0>", timeout=10)
        for i in range(1,3):
            output2 = run_command('ps cd', prompt="BCM.0>", timeout=20)
            time.sleep(10)
        e_pat =  brixiaV2_TH4G_64x4x100_e_pattern

    elif portmode =='32x8x50':
        run_command('port cd en=1', prompt="BCM.0>", timeout=10)
        for i in range(1,3):
            output2 = run_command('ps cd', prompt="BCM.0>", timeout=20)
            time.sleep(10)
        e_pat =  brixiaV2_TH4G_32x8x50_e_pattern
    else:
        run_command('port ce en=1', prompt="BCM.0>", timeout=10)
        for i in range(1,3):
            output2 = run_command('ps ce', prompt="BCM.0>", timeout=20)
            time.sleep(10)
        e_pat =  brixiaV2_TH4G_256x1x100_e_pattern

    ret_code = check_output(output2, patterns=e_pat)
    if ret_code == 0:
        device.raiseException("Enable port failed")

@logThis
def set_Port_Loopback(mac_status_pattern, lb_cmd, ps_cmd):
    run_command(lb_cmd, prompt="BCM.0>", timeout=5)
    output = run_command(ps_cmd, prompt="BCM.0>", timeout=5)
    ret_code = check_output(output, patterns=mac_status_pattern)
    if ret_code == 0:
        raise Exception("Setting Loopback for all ports failed ")


@logThis
def set_snake_vlan():
    run_command("vlan clear", prompt="BCM.0>", timeout=5)
    run_command("vlan remove 1 pbm=all", prompt="BCM.0>", timeout=5)
    run_command(xe0_270, prompt="BCM.0>", timeout=5)
    run_command(xe1_271, prompt="BCM.0>", timeout=5)
    output1 =  run_command("pvlan show", prompt="BCM.0>", timeout=10)
    if not xe0_270_pat and xe1_271_pat in output1:
        raise Exception("pvlan setting failed for ports xe0 and xe1")
    run_command("vlan show", prompt="BCM.0>", timeout=10)

@logThis
def Load_and_initialize():
    gotoSuperUser()
    output1 = run_command("/etc/init.d/opennsl-modules stop", prompt=var.sdk_path) 
    pass_str = "Unload OpenNSL kernel modules... done."
    if pass_str in output1:
        log.info("Unload is passed")
    elif "mknod:" in output1:
        log.info("OpenNSL is reloaded ")
        
    output2 = run_command("./auto_load_user.sh", prompt=var.sonic_prompt, timeout=2)
    if "rmmod: ERROR:" in output2 or "rmmod: not found" in output2:
        log.info("ERROR in AUTO LOAD USER.\nSkipping the error check...\n")
    
    mode1 = run_command("./bcm.user -y {}".format(tool_32x8x50),prompt = "BCM.0>", timeout=30)
    run_command("exit")
    mode2 = run_command("./bcm.user -y {}".format(tool_64x4x100),prompt = "BCM.0>", timeout=30)
    run_command("exit")
    mode3 = run_command("./bcm.user -y {}".format(tool_256x1x100),prompt = "BCM.0>", timeout=30)
    run_command("exit")

#  .....................  Port_BER_Test  .............................

def compare_ber(current, threshold):
    a = "{:.9f}".format(float(current))
    b = "{:.9f}".format(float(threshold))
    if a > b:
        return False
    return True

@logThis
def run_PRBS_and_BER_test():
    output = run_command('dsh', prompt='sdklt.0>', timeout=2)
    if "sdklt.0>" not in output:
        raise Exception("Error in entering the sdklt.0> mode.")

    for each in var.phydiag_cmds:
        run_command(each, prompt="sdklt.0>", timeout=20)
        time.sleep(2)
    run_command("sleep 100", prompt="sdklt.0>", timeout=105)
    time.sleep(30)
    output = run_command(var.phydiag_cmds[-1] , prompt='sdklt.0>', timeout=30)
    time.sleep(30)
    output = run_command(var.phydiag_cmds[-1] , prompt='sdklt.0>', timeout=30)

    if "Nolock" in output or "LossOfLock" in output:
        err_out = re.findall(".*LossOfLock.*|.*NoLock.*", output)
        raise Exception("ERROR in BER display. Some port has Nolock/LossOfLock status.\n" + str(err_out))
    else:
        ber_list = re.findall(".*e-.*", output)
        for each in ber_list:
            i = each.split(':')[-1].strip()
            if not compare_ber(i, "1e-5"):
                raise Exception("ERROR in BER values. Some of the value are greater then threshold (1e-5).\nERROR in BER " + str(i))
    log.success("BER Test Passed Successfully.")

@logThis
def stop_PRBS_and_clear():
    run_command("phydiag 1-270 prbsstat stop", prompt="sdklt.0>", timeout=2)
    run_command("phydiag 1-270 prbsstat clear", prompt="sdklt.0>", timeout=2)
    run_command('exit', prompt='BCM.0>', timeout=2)

#########################################################TC 17,18,19#############################
@logThis
def set_snake_and_Check_vlan(portmode,snake_cmd):
    output = run_command(snake_cmd, prompt="BCM.0>", timeout=30)
    r = re.findall("Error:.*", output)
    if len(r):
        raise Exception("Error in setting snake VLAN.\n" + r[0] + "\n")
    run_command("pvlan show",prompt="BCM.0>",timeout=10)
    output1 = run_command("vlan show",prompt="BCM.0>",timeout=10)
    if portmode == '32x8x50':
        port_infos_pattern = vlan_pattern_32x8x50
    elif portmode == '64x4x100':
        port_infos_pattern = vlan_pattern_64x4x100
    else:
        port_infos_pattern = vlan_pattern_256x1x100
    ret_code = check_output(output1,patterns=port_infos_pattern)
    if ret_code ==0:
        device.raiseException("vlan check failed")

@logThis
def check_ports(portmode):
    time.sleep(5)
    if portmode == '64x4x100':
        output = run_command("ps cd",prompt="BCM.0>",timeout =30)
        port_infos_pattern= brixiaV2_TH4G_64x4x100_e_pattern
    elif portmode == '32x8x50':
        output = run_command("ps cd",prompt="BCM.0>",timeout =30)
        port_infos_pattern= brixiaV2_TH4G_32x8x50_e_pattern
    else:
        output = run_command("ps ce",prompt="BCM.0>",timeout =30)
        port_infos_pattern = brixiaV2_TH4G_256x1x100_e_pattern
    ret_code = check_output(output, patterns=port_infos_pattern)
    if ret_code == 0:
        device.raiseException("Port status check failed")

#####################################################################################################
#TC 3,25
@logThis
def Default_Port_Check():

    gotoSuperUser()
    run_command("./bcm.user -y brixiaV2-TH4G-64x4x100.yml",prompt="BCM.0>",timeout = 10)
    time.sleep(5)
    check_port_status('64x4x100')
    run_command("exit")
    run_command("./bcm.user -y brixiaV2-TH4G-32x8x50.yml",prompt="BCM.0>",timeout = 10)
    time.sleep(5)
    check_port_status('32x8x50')
    run_command("exit")
    run_command("./bcm.user -y brixiaV2-TH4G-256x1x100.yml",prompt="BCM.0>",timeout = 30)
    time.sleep(5)
    check_port_status('256x1x100')
    run_command("exit")

@logThis
def set_prbs_and_stop():

     run_command('dsh',prompt='sdklt.0>',timeout =5)
     run_command('phydiag 50,152 prbs set p=3',prompt='sdklt.0>',timeout =5)
     output1 = run_command('phydiag 50,152 prbsstat start interval=30',prompt='sdklt.0>',timeout =10)
     pattern = "PRBSStat thread started ..."
     if re.search(pattern,output1):
         log.success("PRBSSTAT Started")
     else:
         raise Exception("PRBSSTAT not started")
     output2 = run_command("phydiag 50,152 prbs get",prompt='sdklt.0>')
     CommonKeywords.should_match_ordered_regexp_list(output2,var.prbs)
     run_command("sleep 60",prompt='sdklt.0>',timeout =63)
     output3 = run_command("phydiag 50,152 prbs get",prompt='sdklt.0>')
     CommonKeywords.should_match_ordered_regexp_list(output3,var.prbs)
     output4 = run_command('phydiag 50,152 prbsstat stop',prompt='sdklt.0>',timeout =10)
     pattern = "Stopping PRBSStat thread"
     if re.search(pattern,output4):
         log.success("PRBSSTAT Stopped")
     else:
         raise Exception("Error in stopping prbsstat")
     run_command('phydiag 50,152 prbs clear',prompt='sdklt.0>',timeout =5)
     run_command('exit',prompt='BCM.0>')
###########################################################################################################


# ............................ 10G_KR_L2_CPU_Traffic_Test ............................

@logThis
def set_and_check_vlan_port():
    for each in var.vlan_port_cmds:
        run_command(each, prompt="BCM.0>", timeout=2)

    output = run_command("pvlan show; vlan show", prompt="BCM.0>", timeout=5)
    condition1 = re.search("Port xe0 default VLAN is 270", output)
    condition2 = re.search("Port xe1 default VLAN is 271", output)
    condition3 = re.search("vlan 270.*ports xe.*", output)
    condition4 = re.search("vlan 271.*ports xe.*", output)
    if not condition1 and condition2 and condition3 and condition4:
        raise Exception("Error in assigning VLAN to xe ports.")

    time.sleep(5)
    output = run_command("ps xe", prompt="BCM.0>", timeout=3)
    if not re.search(var.xe_port_ptn.format('0'), output) or not re.search(var.xe_port_ptn.format('1'), output):
        raise Exception("Error in link status. One or both the links are DOWN.")


# .................... BRIXIA_SDK_TC_029_SDK_Reinit_Stress_Test ....................

@logThis
def run_reinit_stress_test(loop_count):
    device.sendMsg("./reinit.sh \r\n")
    device.read_until_regexp(".*times test end.*", timeout=800 * 60) 
    output = device.read_until_regexp('root@sonic:' + var.sdk_path + '#')

    init_test = re.findall("## Init Test:.*", output)[0].split(':')[1].split(' ')
    port_up_test = re.findall("## Port UP Test:.*", output)[0].split(':')[1].split(' ')
    traffic_test = re.findall("## Traffic Test:.*", output)[0].split(':')[1].split(' ')

    init_test = int([i for i in init_test if i != ''][0])
    port_up_test = int([i for i in port_up_test if i != ''][0])
    traffic_test = int([i for i in traffic_test if i != ''][0])

    if init_test + port_up_test + traffic_test != 3 * loop_count:
        raise Exception("Error in reinit stress test.")
    log.success("Reinit Stress Test passes successfully.")


# .............. TC 30 ..............

def check_enabling_disabling_port():
    cmd = "port cd0-cd63 en="

    run_command(cmd + "0", prompt="BCM.0>", timeout=3)
    log.debug("Sleeping for 10 seconds.")
    time.sleep(30)
    output = run_command("ps cd", prompt="BCM.0>", timeout=5)
    for each in var.disabled_port_63_status_pattern:
        if not re.search(each, output):
            raise Exception("Error in disabling the port.\n Concerned pattern -> " + each)
    log.info("All ports successfully disabled.")

    run_command(cmd + "1", prompt="BCM.0>", timeout=3)
    log.debug("Sleeping for 10 seconds.")
    time.sleep(30)
    output = run_command("ps cd", prompt="BCM.0>", timeout=5)
    for each in var.link_up_63_status_pattern:
        if not re.search(each, output):
            raise Exception("Error in enabling the port.\n Concerned pattern -> " + each)
    log.info("All ports successfully enabled.")


# ............... TC_21 ...............

@logThis
def check_Current_PCIe_firmware(flag=0):
    PCIE_FW_Loader_ver = CommonLib.get_swinfo_dict("PCIE").get("newVersion").get("PCIe_FW_loader_version")

    run_command("dsh", prompt="sdklt.0>", timeout=3)
    run_command("seti iproc 0x508c0000 0", prompt="sdklt.0>", timeout=3)
    output = run_command("PCIEphy fwinfo", prompt="sdklt.0>", timeout=3)

    if flag == 0 and "PCIe FW loader version: {}".format(PCIE_FW_Loader_ver) not in output:
        log.info("PCIe FW version is not latest.\nUpdating PCIe FW Now...")
    else:
        log.info("PCIe FW version is latest.")

    if flag == 1:
        version = re.findall(".*PCIe FW loader version:.*", output)[0].split(':')[1].strip()
        if version != PCIE_FW_Loader_ver:
            raise Exception(
                "The firmware version does not matches the required version {}.".format(check_Current_PCIe_firmware))
        else:
            log.success("PCIe FW upgrade test passed.")
        run_command("exit", prompt="BCM.0>", timeout=3)


@logThis
def upgrade_PCIe_firmware_and_reboot():
    output = run_command("PCIEphy fwload pciefw-r5-m7_v2p10.bin", prompt="sdklt.0>", timeout=3)
    if not re.search("PCIE firmware updated successfully.* Please reset the system.*", output):
        raise Exception("Error in upgrading PCIe firmware.")

    run_command("exit", prompt="BCM.0>", timeout=3)
    Exit_From_Sdk()
    run_command("reboot", prompt="Debian GNU/Linux 10 sonic ttyS0", timeout=300)
    enter_sonic_credentials()
    gotoSuperUser()


# ............... TC_31 ...............

@logThis
def check_port_up_status():
    time.sleep(30)
    output = run_command("ps cd", prompt="BCM.0>", timeout=5)
    for each in var.link_up_63_status_pattern:
        if not re.search(each, output):
            raise Exception("Some of the ports are down.\n Concerned pattern -> " + each)


@logThis
def power_cycle_the_device():
    time.sleep(15)
    device.sendMsg(var.power_cycle_cmd + '\r\n')
    device.read_until_regexp("Debian GNU/Linux 10 sonic ttyS0", timeout=200)
    enter_sonic_credentials()
    gotoSuperUser()


# ............... TC_24 ...............

def check_serdes_version():
    der_type = "SerDes type          = osprey7_v2l8p2"
    run_command("dsh", prompt="sdklt.0>", timeout=3)
    device.sendMsg("phydiag 1-270 dsc \r\n")
    output = device.read_until_regexp("sdklt.0>", timeout=150)
    output = output.splitlines()

    index = output.index(der_type)
    try:
        while index:
            ucode_version = output[index - 2]
            if ucode_version != "Common Ucode Version = " + var.ucode:
                raise Exception("ERROR")
            output = output[:index] + output[index + 1:]
            index = output.index(der_type)
    except:
        log.info("Serdes Version Check Passed.")
    run_command("exit", prompt="BCM.0>", timeout=3)
#TC26
@logThis
def Temperature_check():
    run_command('dsh', prompt="sdklt.0>", timeout=3)
    output = device.sendCmd("HealthMONitor TEMPerature","sdklt.0>",timeout=40)
    first = re.findall("Sensor.*Hist Max",output)[0]
    last = re.findall(".*sdklt.0>.*",output)[0]
    output = output.splitlines()
    i = output.index(first)
    j = output.index(last)
    output = output[i+1: j]
    for each in output:
        a = each.split(' ')
        a = [i for i in a if i != '']
        current = a[1]
        mint = a[2]
        maxt = a[3]
    if not mint<current<maxt:
        raise Exception("Temp check Failed!!! Current temperature is not normal!!")
    log.success("Temp check passed!")

    device.sendCmd('exit',"BCM.0>",timeout=5)
@logThis
def set_snake_check_temp(snake_cmd):
    Temperature_check()
    output2 = run_command(snake_cmd, prompt="BCM.0>", timeout=10)
    r = re.findall("Error:.*", output2)
    if len(r):
        raise Exception("Error in setting snake VLAN.\n" + r[0] + "\n")
    send_packet_to_all_ports(cd_pckt_gen_cmd,"300")
    Temperature_check()
    device.sendCmd("pvlan set cd63 1888",'BCM.0>',timeout=10)
#########################################################################################
@logThis
def UpdatePositiveVoltageDroop():
    run_command('dsh',prompt='sdklt.0>',timeout =5)
    cmd_lst=[
            'tr 518 Scenario=4 Topology=1 VdOpt=17 CutThruMode=1 Count=22 PktSize=292 RunMode=MAC TestPhase=1',
            'tr 518 Scenario=4 Topology=1 VdOpt=17 CutThruMode=1 Count=22 PktSize=292 RunMode=MAC TestPhase=3',
            'tr 518 Scenario=4 Topology=1 VdOpt=17 CutThruMode=1 Count=22 PktSize=292 RunMode=MAC TestPhase=2'
            ]
    output=run_command(cmd_lst,prompt='sdklt.0>',timeout=300)
    output=output.splitlines()
    for each in output:
        if re.search("Error:",each):
            raise Exception("Error reported!! Bug found")
    device.sendCmd('exit',"BCM.0>",timeout=5)


